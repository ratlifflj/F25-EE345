# EE345 Website

This repo contains the course website for EE345. Content for this website is almost entirely written in Markdown, and a Gitlab CI runner automatically deploys the contents of this repo to the web. The template was borrowed from the CSE 373 course website and has been modified  specifically for 547.

This website was originally developed by Brian Chan, Howard Xiao, and Aaron Johnston in 20su (CSE273).

## Installation

It's recommended to install everything in a 373-specific python 3.8 environment (e.g. [Miniconda](https://docs.conda.io/en/latest/miniconda.html)).

1. Install requirements from requirements.txt using `pip install -r requirements.txt`.
Note that even if you are using conda, not all requirements are in conda-forge, so it's recommended to still use pip.

2. From the repo root, run `python setup.py develop`
(assuming `python` is your python 3.8 executable)

## Developing Locally

From the repo root, run `mkdocs serve`.

(`mkdocs serve --dirtyreload` exists as well; good for developing single pages, but may require
restarts to reflect changes to nav/theme/collections/includes, and it's not even that much faster
than rebuilding the entire site.)

## Building for Deployment

`mkdocs build --clean`

(By default, outputs to `site` directory.)

## Markdown Notes/Conventions

We use MkDocs, which uses Python-Markdown for its Markdown rendering.

- mostly pretty standard markdown implementation with extensions to match
    [PHP markdown extra](https://michelf.ca/projects/php-markdown/extra/)
- see [differences](https://python-markdown.github.io/#differences)

### Links

All internal links (both relative and absolute) in Markdown get processed by a Markdown extension to

1. check that the file exists
    - else output a warning (which will prevent deployment on master)
2. resolve the file path
    - convert from input (e.g., md, scss, png) to output (e.g., html, css, png)
    - convert any relative links to absolute (i.e., relative to `site_url`/`src` folder
3. prepend `site_url`

Conventions:

- prefer relative links rather than absolute when linking to sibling files
    (e.g., `[project main page](./index.md)`)
    - prefer including `./` to make the relative-ness more obvious
    - (this makes it easier to rename folders)
- prefer absolute links instead of using `../blah` (e.g., `[syllabus](/syllabus.md)`)
    - (this makes it easier to rename folders)
- **NOTE**: relative links are not supported for files in `collections`---they get resolved
    incorrectly.
    Instead, use absolute internal links (e.g., `[syllabus](/syllabus.md)`).
- note: external links are required to link to URLs in `courses.cs.washington.edu` that aren't
    part of the course site (e.g.,
    `[partner form](https://courses.cs.washington.edu/courses/cse373/tools/20su/partner/p1/)`)
    
### Code Blocks

- prefer fenced code blocks (using ```)
- indented code blocks always have line numbers enabled
- note: the theme currently doesn't work perfectly with line highlighting---the highlighting ends
    when the text ends, instead of spanning the full line
    - this probably can't be fixed without changing `pymdownx.highlight.linenums_style` back to the
        default, which the theme doesn't currently display properly

## Other Noteworthy Markdown Extensions

Not a complete list; only the most useful ones

- admonition: use `!!!` to add admonitions (styled as bootstrap alerts by the theme)
- pymdownx.details: use `???` blocks to add details/summary elements 
- markdown_katex: render KaTeX server-side using syntax that matches GitLab's. Surround backticks with dollar signs for inline math, and put "math" after three backticks for a math block (like specifying a language for code). Examples:

$`\sum`$

```math
\sum_{i=1}^{10} i
```

## Noteworthy MkDocs Plugins

- macros: enable Jinja2 support in Markdown files (runs before Markdown)
- custom plugins:
    - append-to-pages: prepend/append text to all Markdown (useful for adding site-wide
        abbreviations or link targets
        - rename pending
    - collections: the logic behind the collections
    - auto-nav: load all page data earlier and use page metadata to set the nav
        - also removes MkDoc's concept of "sections" from the nav... the plugin and theme probably
            should be rewritten to not do this.
    - sass: compile Sass files when building the site
    - url-validation: this MkDocs plugin replaces the default url resolution Markdown extension
        added by MkDocs with one that outputs absolute links

## Setting Up for the Quarter

### CI

Every quarter (after forking the website repo for that quarter), we need to email CSE support to
ask them to set up the runner on the new repo.
(We can't do this ourselves because the runner runs on the CSE web server, which we don't have
permissions for.)

We can use the same `.gitlab-ci.yml`; the only thing that needs to be changed is the value for `courseweb.variables.quarter`.

### Schedule Configuration

All files controlling the schedule can be found in `/data/schedule/`. A detailed setup guide for the schedule at the beginning of the quarter can be found in `/data/schedule/README.md`.

## Notable Files for Modifying this Template

This is a non-exhaustive list of some of the important files you may be looking for as you **modify the template**. If you are simply changing the information on the site (e.g. for a new quarter), it's unlikely you need to touch these files.

- `/src/index.html`: This enormous file is where all the logic for rendering the course calendar is stored, all done with the Jinja2 templating language.
- `/theme/css/base.scss`: Global styles. Page-specific styles are stored in `/src/*.scss`, notably including `schedule.scss` for the calendar.
- `/mkdocs.yml`: Global configurations (includes google analytics, external links in sidebar, acronyms to style).
- `/data/vars.yml`: Quarter-specific URLs like Gradescope and Canvas (not used in many places, if at all).
- `/main.py`: Place python functions here to make them available in template files. Used extensively in `/src/index.html`.
- `/theme/base.html`: The base template of every page, including navigation
- `/theme/content.html`: The wrapper template around content, including page title, etc.
- `/theme/no-toc.html` and `/theme/no-toc-content.html`: The templates for pages without table of contents (e.g. the home page). Extends `base.html`! Look here if you make changes to `base.html` that don't seem to be appearing on the home page.
- `/theme/nav.html`: Overall navigation template, which includes the navigation for mobile.
- `/includes/announcement.html` and `/includes/staffer.html`: Templates for announcements and staffers. These are in their own location because they are rendered via the `/collections/` system, which renders all files within a subfolder.
