import mkdocs.plugins
import mkdocs.config.config_options


class AppendToPagesPlugin(mkdocs.plugins.BasePlugin):
    """should run before mkdocs-macros in order for Jinja templating to work"""
    config_scheme = (
        ('prepend', mkdocs.config.config_options.Type(str, default='')),
        ('append', mkdocs.config.config_options.Type(str, default='')),
    )

    def on_page_markdown(self, markdown, page, config, files):
        if self.config['prepend']:
            markdown = self.config['prepend'] + '\n\n' + markdown

        if self.config['append']:
            markdown = markdown + '\n\n' + self.config['append']

        return markdown
