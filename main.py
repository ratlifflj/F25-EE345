from datetime import datetime

import jinja2
from jinja2 import pass_context
from markupsafe import Markup
from dateutil import rrule
from markdown import Markdown

from plugins.more_url_validation import normalize_url

DAYS_OF_THE_WEEK = {"Sun": rrule.SU,
                    "Mon": rrule.MO,
                    "Tue": rrule.TU,
                    "Wed": rrule.WE,
                    "Thu": rrule.TH,
                    "Fri": rrule.FR,
                    "Sat": rrule.SA}


def define_env(env):
    env.config['j2_extensions'] = ['jinja2.ext.do']

    @env.filter
    def markdown(text):
        md = Markdown(
            extensions=env.conf['markdown_extensions'],
            extension_configs=env.conf['mdx_configs'] or {}
        )
        return Markup(md.convert(text))
    # env.filters["markdown"] = env.conf["plugins"]["markdown-filter"].md_filter

    @env.macro
    def doc_env():
        "Document the environment"
        return {name: getattr(env, name) for name in dir(env) if not name.startswith('_')}

    @env.macro
    def parse_date(date):
        return datetime.strptime(date, "%Y-%m-%d")

    @env.macro
    def dates_gen(start, days):
        r = rrule.rrule(rrule.DAILY,
                        byweekday=[DAYS_OF_THE_WEEK[d] for d in days],
                        dtstart=start)
        rs = rrule.rruleset()
        rs.rrule(r)
        return iter(rs)

    @env.macro
    def dates_gen_with_dummies(start, days):
        r = rrule.rrule(rrule.DAILY,
                        byweekday=[DAYS_OF_THE_WEEK[d] for d in days],
                        dtstart=start)
        r_dummy = rrule.rrule(rrule.DAILY,
                              byyearday=[207, 235],
                              dtstart=start)
        rs = rrule.rruleset()
        rs.rrule(r)
        rs.rrule(r_dummy)
        return iter(rs)

    # Only update collections if the plugin is present
    if 'collections' in env.conf['plugins']:
        env.variables.update(env.conf['plugins']['collections'].collections)

    @env.macro
    def deep_get(d, *args, default=None):
        for arg in args:
            d = d.get(arg, None)
            if d is None:
                return default
        return d

    @env.macro
    def merge_dicts(d1, d2):
        output = dict(d2)
        for k, v in d1.items():
            if k in output:
                default_value = d2[k]
                if default_value is dict and v is dict:
                    output[k] = merge_dicts(v, default_value)
                    continue
            output[k] = v
        return output


    @env.filter
    @pass_context
    def url(context, value):
        """ A Template filter to normalize URLs. """
        # exclude page parameter; template urls are always relative to site root (site_dir)
        files = env.conf['plugins']['url-validation'].file_data["files"]  # why is this a thing
        return normalize_url(value, files, page=context['page'], site_url=env.conf['site_url'],
                             treat_relative_as_absolute=True)[0]
