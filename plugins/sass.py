import logging
import os

import mkdocs
import sass
from mkdocs import utils
from mkdocs.structure.files import Files, File

log = logging.getLogger(f"mkdocs.custom_plugins.{__name__}")
log.addFilter(mkdocs.utils.warning_filter)


class SassPlugin(mkdocs.plugins.BasePlugin):

    config_scheme = (
        ('sass_extensions', mkdocs.config.config_options.Type(list, default=['.scss', '.sass'])),
        ('include_dirs', mkdocs.config.config_options.Type(list, default=['sass'])),
    )

    def on_files(self, files: Files, config):
        updated_files = []
        for file in files:
            if os.path.splitext(file.src_path)[1] in self.config['sass_extensions']:
                updated_files.append(SassFile(file, self.config['include_dirs']))
            else:
                updated_files.append(file)
        return Files(updated_files)

    def on_serve(self, server, config, builder):
        for d in self.config['include_dirs']:
            server.watch(d, builder)


class SassFile(File):
    def __init__(self, file, include_dirs):
        self.page = file.page
        self.src_path = file.src_path
        self.abs_src_path = file.abs_src_path
        self.name = file.name
        self.dest_path = _to_css_extension(file.dest_path)
        self.abs_dest_path = _to_css_extension(file.abs_dest_path)
        self.url = _to_css_extension(file.url)

        self.include_dirs = include_dirs

    def copy_file(self, dirty=False):
        """
        Copy source file to destination, ensuring parent directories exist.
        (If dirty is enabled, file will not be updated when imports change;
        only when the file itself does.)
        """
        if dirty and not self.is_modified() and not self._is_include_dirs_modified():
            log.debug("Skip copying unmodified file: '{}'".format(self.src_path))
        else:
            log.debug("Compiling sass file: '{}'".format(self.src_path))
            try:
                css = sass.compile(filename=self.abs_src_path,
                                   output_style='compressed',
                                   include_paths=self.include_dirs)
                output_dir = os.path.dirname(self.abs_dest_path)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                with open(self.abs_dest_path, 'w', encoding="utf-8") as f:
                    f.write(css)
            except sass.CompileError as e:
                log.error("Error compiling sass file '{}': {}".format(self.src_path, e))

    def _is_include_dirs_modified(self):
        if not self.include_dirs:
            return False
        # search for last modified in each include dir
        last_modified_include = max(max(os.path.getmtime(f) for f, _, _ in os.walk(d))
                                    for d in self.include_dirs)
        return os.path.getmtime(self.abs_dest_path) < last_modified_include

    def is_css(self):
        """ Return True if file is a CSS file. """
        return True


def _to_css_extension(path):
    return os.path.splitext(path)[0] + '.css'
