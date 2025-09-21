# import os
# import types
# from pathlib import Path
# from mkdocs.structure.files import File, Files
#
#
# COLLECTION_NAMES = ["announcements", "staff"]
#
# file_to_collection = {}
# collections = {name: [] for name in COLLECTION_NAMES}
#
#
# def reset(config):
#     file_to_collection.clear()
#     for lst in collections.values():
#         lst.clear()
#
#
# def add_announcements(files, config):
#     project_dir = Path.cwd()
#     files_list = []
#     for collection_name in COLLECTION_NAMES:
#         for file in (project_dir / "collections" / collection_name).iterdir():
#             if file.is_file():
#                 rel_path = file.relative_to(project_dir)
#                 f = File(str(rel_path),
#                          str(project_dir),
#                          config['site_dir'],
#                          config['use_directory_urls'])
#                 files_list.append(f)
#                 file_to_collection[str(file.resolve())] = collection_name
#
#     return Files(files_list + list(files))
#     # # hack to ensure collections get processed first
#     # files._files = files_list + files._files
#     # files.src_paths.update({file.src_path: file for file in files_list})
#
#
# def store_announcements(markdown, page, config, files):
#     collection_name = file_to_collection.get(page.file.abs_src_path, None)
#     if collection_name:
#         collections[collection_name].append(page)
#         page.meta['template'] = 'noop.html'
#
#
# def on_nav(nav, config, files):
#     load_pages(nav.items, config)
#     traverse(nav.items, None)
#     print(nav)
#
#
# def load_pages(nav, config):
#     for item in nav:
#         if item.is_page:
#             # TODO do we need to make sure this only runs once per object,
#             #  or is the input nav fresh every time?
#             if hasattr(item, "is_patched"):
#                 print("panikkkkkkkkk")
#
#             original_read_source = item.read_source
#
#             def new_read_source(self, cfg):
#                 if self.file.is_modified() and self.markdown is None:
#                     original_read_source(cfg)
#             item.read_source = types.MethodType(new_read_source, item)
#             item.is_patched = True
#             if item.file.is_modified():
#                 item.markdown = None
#             item.read_source(config)
#         elif item.is_section:
#             load_pages(item.children, config)
#
#
# def traverse(nav, parent):
#     for i, item in reversed(list(enumerate(nav))):
#         if item.is_section:
#             sub_children = item.children[1:]
#             index = item.children[0]  # index should always be first child
#             if not index.is_page \
#                     or os.path.basename(index.file.src_path) not in ['index.md', 'README.md'] \
#                     or 'nav_order' not in index.meta:
#                 print(index)
#                 if index.is_page:
#                     print(index.meta)
#                     print(os.path.basename(index.file.src_path))
#                 else:
#                     print("not a page")
#                 print()
#                 del nav[i]
#                 continue
#             else:
#                 index.children = sub_children
#                 traverse(sub_children, index)
#             item = nav[i] = index
#         elif item.is_page:
#             if 'nav_order' not in item.meta:
#                 del nav[i]
#         item.parent = parent
#     nav.sort(key=lambda page: page.meta['nav_order'])
