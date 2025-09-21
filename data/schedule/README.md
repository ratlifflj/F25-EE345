# Schedule

This directory contains the [YAML](https://yaml.org/) configuration files that are used to generate the schedule on the course website home page.

## Setting Up for the Quarter

Note that there are separate files for lectures, sections, projects, and exercises. The following is a list of things that need to be considered
at the beginning of the quarter:

1. Change the start date configuration (present in all files). These values must sync up for a correctly rendered calendar.
2. Modify the lecture titles, section titles, and assignments as appropriate for the quarter, and then update released/due dates in projects/exercises files.
3. Clear out content so the calendar only shows an outline of the quarter. The approach for this is different for every type of schedule file as described below.

Note that this template was designed to show the whole quarter from the very beginning, so substantial changes may be needed if you want to reveal the quarter incrementally. 

### Lectures

In `lectures.yml`, the default configuration automatically populates slides for each lecture. To set up for the beginning of each quarter,
create a "blank" entry for each lecture as follows:

```yaml
- title: "Dijkstra's Algorithm"
  resources:
    slides: null
```

This will prevent the default configuration from populating the PDF and PPTX links. Then, when posting slides for a lecture, delete the `slides` key to restore the default URLs for the posted slides. The `slides` key is special: it will display buttons on the calendar. If you want to post additional resources (such as videos, readings, or links), you can create arbitrary additional keys under `resources` that will be displayed with a list of links. For example, the following could be a complete configuration for a single day:

```yaml
- title: "Heaps II, Interviews"
  resources:
    resources:
      video: https://uw.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=a2a664ba-9c43-4c65-a561-ac00016e5a55
      optional review: https://www.gradescope.com/courses/141341/assignments/568567
    careers:
      "A+ Advice for Getting a Software Job (recording)": https://uw.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=0ac5f0a6-178c-4c9c-9e14-ac05016564bc
      "Job Guide": https://docs.google.com/document/d/1chTrHwSC2iv_EU-Br55Hh4YhdozQ7R2RaWVHusMZUuI/view
      "Resume Guide": https://docs.google.com/document/d/1qElLme18XlZNSLDL9CQCRu2ptW19H6JC9NnVMPHofHw/view
```

On the calendar, this will create buttons for the slides (from the defaults, including both PDF and PPTX), a header displaying as "Resources" with links for the video and optional review, and a header displaying as "Careers" with the other links. Note that the first `resources` is part of the configuration but the second `resources` is what gets displayed to students.

### Sections

`sections.yml` is very similar to `lectures.yml`, and uses the same defaults system so everything should be created but `null`ed out at the beginning of the quarter. Note that `worksheet` is a special key (similar to `slides` from lectures) that displays buttons for the blank worksheet and solution. **Note:** if you want to post just the blank worksheet and post the solution afterward, as long as you create a key called `worksheet` it will override _all_ subkeys from the default. For example, the following could be a configuration the night before section, where the worksheet is posted but not the solutions:

```yaml
- title: Algorithmic Analysis
  resources:
    worksheet:
      blank: /sections/section2.pdf
```

The following could then be the complete configuration after section, when the worksheet is fully published (using the defaults) and a playlist of review videos on youtube has been linked:

```yaml
- title: Algorithmic Analysis
  resources:
    resources:
      review videos: https://www.youtube.com/playlist?list=PLEcoVsAaONjeSVPkPvwR05UU_6kQvduPk
```

### Projects

Projects in `projects.yml` are much simpler than lectures or sections: you can create all of the projects ahead of time and simply comment out the `url` key. The presence of a `url` is what colors the project in on the calendar and makes it clickable. **Note:** in addition to commenting out the `url` keys on projects, you need to go to the index.md for the instructions of each project and comment out the `nav_order` key to prevent the instructions from appearing in the navigation. You can find those project instruction index.md files within `/src/projects/`, for example `/src/projects/heap/index.md`. As long as the `nav_order` is not present, it will not be in the navbar, but will _still be available by URL_. This is intended behavior to let TAs run through the projects ahead of their official release, but it means students _could_ find the instructions early. We recommend mitigating this by placing a notice at the top of `index.md`, such as:

```
!!! caution
    This project has not been officially released yet. Its contents might still change as we continue to refine the instructions. Please check back later!
```

### Exercises

Exercises in `exercises.yml` are the same as projects, and even simpler because the instructions are simply linked PDF files. When releasing exercises, don't forget to update the exercises overview at `/src/exercises/index.md`.

### Special Case: Exams

Exams are represented as special exercises in `exercises.yml`, with a special `is_exam: true` key/value pair that causes the schedule rendering template to treat it differently. Exams need to have their numbers specified explicitly, e.g. as `num: 1`. This brings them out of the implicit numbering "flow", so they don't mess up the exercise numbering scheme.

A complete example of an exam that is published (because the `url` is uncommented):

```yaml
- title: Exam I
  is_exam: true
  start: 2020-7-24
  end: 2020-7-25
  num: 1
  url: https://www.gradescope.com/courses/141341/assignments/569908
```

If you choose to hold exam office hours in the corresponding lecture, you can do so by adding the same special `is_exam: true` key/value pair to that lecture as well in `lectures.yml`:

```yaml
- title: "Optional Exam I Office Hours"
  is_exam: true
  num: -1   # Prevents this session from taking up a number
  resources:
    slides:
      null
```

### Special Case: Due Dates on Non-Class Dates

The calendar uses lectures and section configurations to determine what set of days it should render. Unfortunately, this means if you have any deadlines falling on a Tuesday, Saturday, or Sunday, you must create a dummy lecture with `is_dummy: true` so the calendar template renders a blank row to place the deadline in. This would go in `lectures.yml` (the title does not get rendered):

```yaml
- title: "Exam I Due Date"
  is_dummy: true
  num: -1   # Prevents this session from taking up a number
```

### Complete Example: Snapshot of 20Su

The following commit message gives a complete picture of what the website/schedule might look like in the middle of the quarter with some things still unreleased:

https://gitlab.cs.washington.edu/cse373-root/20su/website/-/tree/0f56dc59b8f5cf9f347c0613de1e8b0a2e447190/


## Implementation Details

### Schema

All data files get merged: maps get merged; other values get replaced
(in order given by mkdocs.yml; later entries replace earlier ones; this is all handled by the
mkdocs-macros plugin)

### Schedule

the schedule works in about 3 passes:

1. process each branch of the `schedule` map (class days go into `days` list of class events;
    assignments go into `assignment_dates` list of start/end events (1 of each for each assignment))
2. loop through `assignment_dates` to count the length of each assignment (in table rows),
    using same logic as below
3. actually output a table
    - each event in `days` gets 2 rows:
        1 for the date and data cells,1 for any assignments that start on that date
    - each assignment gets 1 cell on its start date; this cell has rowspan equal to its length
        calculated above
    - (this means that an assignment can end on the same day another releases:
        the ending one uses the top row, and the starting one uses the bottom row)
    - (yes, end events are not used by any of the current templating)
    
#### Input data

All schedule-related items reside in the `schedule` map, which uses the following keys:

- start: (str: YYYY-mm-dd) the course start date
- defaults: a map from item type to some default values for each item of that type
- start_indices: map from item type to number start index for numbering
- styles: a map used to customize css classes of output; currently not used as often as it should be
- \[anything else]: groups of items can be stored as values in `schedule` with any key other than the ones above

Each group of items should be a dictionary with these keys:

- default_type: (str) the default type of each item; can be overridden by specifying `type`
- days: (list of days of the week (3-letter str; title case) the days of the week that the items
    in this group occur on; used (along with `start`) to automatically assign dates to items
- items: (list of `Item`s) the list of items

`Item`: (a map)

- type: (str) a type to override the default type
- title: (str)

#### Output loop

class events will be a map with

- title
- type (str)
- resources (map {group -> map {name -> url} })
- date (datetime object)
- week (int; default populated by templating)
- num (int; default populated by templating)
- (anything else added to the yaml data)

assignment start/end events will be a map with

- date (datetime)
- week (int; default populated by templating)
- assignment (reference to the assignment loaded from the yaml data)
- type (str: start/end)

assignments will be:

- title
- type (str)
- start (datetime)
- start_event (event from above; populated by templating)
- end (datetime)
- end_event (event from above; populated by templating)
- url
- num (int; default populated by templating)
- (anything else added to the yaml data)

#### urls

all urls (resources/assignments) support python string format; ie the templating does a
`url.format(**data)` where data is the day or assignment; mostly useful for accessing `num`
