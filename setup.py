from setuptools import setup
from setuptools import setup, find_packages
setup(
    name='mkdocs-cse373-custom-plugins',
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'collections = plugins.collections:CollectionsPlugin',
            'sass = plugins.sass:SassPlugin',
            'url-validation = plugins.more_url_validation:MoreUrlValidationPlugin',
            'auto-nav = plugins.auto_nav:AutoNavPlugin',
            'append-to-pages = plugins.append_to_pages:AppendToPagesPlugin',
        ],
    }
)
