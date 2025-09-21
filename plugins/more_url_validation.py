import logging
import os
import posixpath
import traceback
from urllib.parse import unquote as urlunquote
from urllib.parse import urlparse, urlunparse

import jinja2
import mkdocs
from markdown import Extension
from markdown.treeprocessors import Treeprocessor
from mkdocs.utils import path_to_url, warning_filter

log = logging.getLogger(f"mkdocs.custom_plugins.{__name__}")
log.addFilter(warning_filter)

# unfortunately, it's really hard to get the current file/files from markdown,
# so this code is fairly hacky


class MoreUrlValidationPlugin(mkdocs.plugins.BasePlugin):
    def __init__(self):
        self.file_data = {}

    def on_config(self, config):
        # Note: this will leave the extension in the config for any other mkdocs extensions that
        # read the markdown extensions (so other extensions get the features too)
        config['markdown_extensions'].append(
            RelativePathExtensionReplacement(config['site_url'], self.file_data))

    # runs right before markdown rendering for each page; handles markdown + macros jinja/markdown
    def on_page_markdown(self, markdown, page, config, files):
        self.file_data["page"] = page
        self.file_data["files"] = files
        # ext[:] = [item for item in ext if not isinstance(item, RelativePathExtensionReplacement)]

    # runs right before jinja rendering for each page
    def on_template_context(self, context, template_name, config):
        self.file_data["page"] = context["page"]

    # runs once, before ALL jinja tempaltes render
    def on_env(self, env, config, files):
        self.file_data["files"] = files

        @jinja2.contextfilter
        def better_url_filter(context, value):
            """ A Template filter to normalize URLs. """
            # exclude page parameter; template urls are always relative to site root (site_dir)
            return normalize_url(value, files, page=context['page'], site_url=config['site_url'],
                                 treat_relative_as_absolute=True)[0]

        @jinja2.contextfilter
        def no_validation_url_filter(context, value):
            """ A Template filter to normalize URLs. """
            # exclude page parameter; template urls are always relative to site root (site_dir)
            return normalize_url(value, files, page=context['page'], site_url=config['site_url'],
                                 treat_relative_as_absolute=True, disable_validation=True)[0]
        env.filters['url'] = better_url_filter
        env.filters['page_url'] = no_validation_url_filter  # for urls from page.url


def normalize_url(url, files, page=None, site_url='',
                  treat_relative_as_absolute=False, disable_validation=False):
    """
    Return (absolute url using the site url, url should open in new page (is external or non-html).
    """
    url = path_to_url(url or '.')
    # Allow links to be fully qualified URLs or the current page
    scheme, netloc, path, params, query, fragment = urlparse(url)
    if scheme or netloc:
        return url, True
    if not path:
        return url, False

    absolute = False
    if path.startswith(('/', '\\')):
        path = path[1:]
        absolute = True

    if disable_validation:
        path = posixpath.join(site_url, path)
        is_not_html = False
    else:
        # Determine the filepath of the target.
        file_dir = os.path.dirname(page.file.src_path) \
            if page and not (absolute or treat_relative_as_absolute) else ''
        target_path = os.path.join(file_dir, urlunquote(path))
        target_path = os.path.normpath(target_path).lstrip(os.sep)

        if target_path not in files:
            file = page.file.src_path if page else "[some template file?]"
            log.warning(
                "Documentation file '{}' contains a link to '{}' which is not found "
                "in the documentation files. ({})".format(file, target_path, url)
            )
            if not page:
                traceback.print_stack()
            return url, False

        target_file = files.get_file_from_path(target_path)
        path = posixpath.join(site_url, target_file.url)
        is_not_html = os.path.splitext(target_file.dest_path)[1] != ".html"
    components = (scheme, netloc, path, params, query, fragment)
    return urlunparse(components), is_not_html


class _RelativePathTreeprocessor(Treeprocessor):
    def __init__(self, site_url, file_data):
        self.site_url = site_url
        self.file_data = file_data

    def run(self, root):
        """
        Update urls on anchors and images to make them absolute
        Iterates through the full document tree looking for specific
        tags and then makes them absolute based on the site url
        """
        for element in root.iter():
            if element.tag == 'a':
                key = 'href'
            elif element.tag == 'img':
                key = 'src'
            else:
                continue

            url = element.get(key)
            new_url, set_target = self.path_to_url(url)
            element.set(key, new_url)
            if set_target and element.tag == 'a':
                element.set('target', '_blank')
                element.set('rel', 'noopener noreferrer')

        return root

    def path_to_url(self, url):
        return normalize_url(url,
                             self.file_data["files"],
                             page=self.file_data["page"],
                             site_url=self.site_url)


class RelativePathExtensionReplacement(Extension):
    """
    Replaces the extension created by mkdocs to change handling of absolute links.
    """

    def __init__(self, site_url, file_data):
        self.site_url = site_url
        self.file_data = file_data

    def extendMarkdown(self, md):
        # original_relpath = md.treeprocessors["relpath"]
        relpath = _RelativePathTreeprocessor(self.site_url, self.file_data)
        md.treeprocessors.register(relpath, "relpath", 0)
