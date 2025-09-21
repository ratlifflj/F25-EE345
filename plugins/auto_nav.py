import logging
import types

import mkdocs.plugins
import mkdocs.utils

log = logging.getLogger(f"mkdocs.custom_plugins.{__name__}")
log.addFilter(mkdocs.utils.warning_filter)

# Warning: this plugin is rather hacky and liable to break with mkdocs updates


class AutoNavPlugin(mkdocs.plugins.BasePlugin):

    def on_nav(self, nav, config, files):
        self.load_pages(nav.items, config)
        self.traverse(nav.items, None)

    def load_pages(self, nav, config):
        for item in nav:
            if item.is_page:
                # a little slow to read/parse every time, but we need nav_order from the metadata
                # to set up the nav properly
                # TODO could replace read_source with custom loading/parsing to make it a bit faster
                #  - read until end of yaml metadata first time; load rest of file next time
                item.read_source(config)

                def new_read_source(self, cfg):
                    pass
                item.read_source = types.MethodType(new_read_source, item)
            elif item.is_section:
                self.load_pages(item.children, config)

    def traverse(self, nav, parent):
        for i, item in reversed(list(enumerate(nav))):
            if item.is_section:
                sub_children = item.children[1:]
                index = item.children[0]  # index should always be first child
                if not index.is_page \
                        or index.file.name != 'index':
                    # exclude and stop traversing children
                    log.info('Excluding from nav: {}'.format(index))
                    del nav[i]
                    continue
                index.children = sub_children
                self.traverse(sub_children, index)
                item = nav[i] = index
                if 'nav_order' not in index.meta:
                    # exclude, but continue traversing children
                    log.info('Excluding from nav: {}'.format(index))
                    del nav[i]
            elif item.is_page:
                if 'nav_order' not in item.meta:
                    del nav[i]
            item.parent = parent
        nav.sort(key=lambda page: page.meta['nav_order'])
