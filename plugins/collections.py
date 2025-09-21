
from pathlib import Path

import mkdocs
from mkdocs.structure.files import File, Files


class CollectionsPlugin(mkdocs.plugins.BasePlugin):
    config_scheme = (
        ('collections', mkdocs.config.config_options.Type(dict, default={})),
        ('collections_dir', mkdocs.config.config_options.Type(str, default='collections')),
    )

    def __init__(self):
        self.file_to_collection = {}
        self.collections = None

    def on_serve(self, server, config, builder):
        server.watch(self.config['collections_dir'], builder)
        server.watch('data', builder)  # HACK: watch data here, since mkdocs-macros doesn't watch it

    def on_config(self, config):
        self.collections = {name: [] for name in self.config['collections']}

    def on_pre_build(self, config):
        self.file_to_collection.clear()
        for lst in self.collections.values():
            lst.clear()

    def on_files(self, files, config):
        project_dir = Path.cwd()
        files_list = []
        for collection_name in self.config['collections']:
            for file in Path(self.config['collections_dir'], collection_name).iterdir():
                if file.is_file():
                    # rel_path = file.relative_to(project_dir)
                    f = File(str(file),
                             str(project_dir),
                             config['site_dir'],
                             config['use_directory_urls'])
                    files_list.append(f)
                    self.file_to_collection[str(file.resolve())] = collection_name

        return Files(files_list + list(files))
        # # hack to ensure collections get processed first
        # files._files = files_list + files._files
        # files.src_paths.update({file.src_path: file for file in files_list})

    def on_page_markdown(self, markdown, page, config, files):
        collection_name = self.file_to_collection.get(page.file.abs_src_path, None)
        if collection_name:
            self.collections[collection_name].append(page)
            page.meta['template'] = 'noop.html'
