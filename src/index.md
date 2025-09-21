---
title: Home
heading: Introduction to Foundations of ML
subtitle: Fall 2025
template: no-toc.html
nav_order: 0
description: >-
    Introduction to Foundations of ML, Fall 2025
extra_css: ['schedule.scss']
---


## Announcements {: .mt-4 }
{% for announcement in (announcements | sort(attribute="meta.date", reverse=True))[:3] %}
{% if loop.first %}
{% set expand = True %}
{% endif %}
{% include 'announcement.html' %}
{% endfor %}

{% if announcements | length >= 0 %}
[All Announcements](/announcements.md){: .btn .btn-373 .fs-3}
{% endif %}


{# build up list of days #}

{% set assignment_abbr = {"project": "P", "homework": "H"} %}


{% macro add_entries(days, group, defaults, start, counts) %}
{% if group.default_type == "lecture" %}
    {% set dates = dates_gen_with_dummies(start, group.days) %}
{% else %}
    {% set dates = dates_gen(start, group.days) %}
{% endif %}

{% for day in group.entries %}

{% set type = day.type or group.default_type %}
{% set num = day.num or count(type, counts) %}
{% set date = dates.__next__() %}

{% do day.update({'type': type, 'num': num, 'date': date}) %}
{% do set_week(day, start) %}

{% do merge_in_place(day, defaults.get(type, {})) %}

{% do days.append(day) %}
{% endfor %}
{% endmacro %}

{#
operates on events, since returning ints with macros is hard
will not overwrite existing event.week
#}
{% macro set_week(event, start) %}
{% set week = (event.date - start).days // 7 + 1 %}
{% do event.setdefault('week', week) %}
{% endmacro %}


{% macro add_assignments(assignments, group, defaults, counts) %}
{% for assignment in group.entries %}

{% set type = assignment.type or group.default_type %}
{% set num = assignment.num or count(type, counts) %}

{% do assignment.update({'type': type, 'num': num, 'start': parse_date(assignment.start), 'end': parse_date(assignment.end)}) %}
{% do merge_in_place(assignment, defaults.get(type, {})) %}

{% do add_assignment(assignment, assignments, 'start', start) %}
{% do add_assignment(assignment, assignments, 'end', start) %}
{% endfor %}
{% endmacro %}


{% macro add_assignment(assignment, assignments, type, start) %}
{% set event = {'assignment': assignment, 'type': type, 'date': assignment[type]} %}
{% do set_week(event, start) %}
{% do assignments.append(event) %}
{% do assignment.setdefault(type~"_event", event) %}
{% endmacro %}

{#
merge d2 into d1, in place
dicts are merged recursively; other existing values are not changed
#}
{% macro merge_in_place(d1, d2) %}
{% for k, v in d2.items() %}
{% set existing_val = d1.setdefault(k, v) %}
{% if existing_val != v and existing_val is mapping and v is mapping %}
{% do d1.__setitem__(k, merge_dicts(existing_val, v)) %}
{% endif %}
{% endfor %}
{% endmacro %}

{%- macro count(type, counts) %}
{%- set c = counts[type] %}
{%- if c is undefined %}
{{- -1 }}
{%- else %}
{%- do counts.__setitem__(type, c + 1) %}
{{- c + 1 }}
{%- endif %}
{%- endmacro %}

{% set counts = {} %}
{% if schedule.start_indices %}
{% for type, index in schedule.start_indices.items() %}
{% do counts.__setitem__(type, index - 1) %}
{% endfor %}
{% endif %}

{% set days = [] %}
{% set assignment_dates = [] %}

{% set start = parse_date(schedule.start) %}
{# add lectures and sections #}
{% do add_entries(days, schedule.lectures, schedule.defaults, start, counts) %}
{% do add_entries(days, schedule.sections, schedule.defaults, start, counts) %}
{% set days = days|sort(attribute="date") %}
{# add assignments #}
{% do add_assignments(assignment_dates, schedule.projects, schedule.defaults, counts) %}
{% do add_assignments(assignment_dates, schedule.homeworks, schedule.defaults, counts) %}
{# sort by date; latest to earliest (ties broken by end-date before start-date #}
{% set assignment_dates = assignment_dates|sort(attribute='date,type', reverse=true) %}




{% macro update_assignment_status(events, day, active, status) %}

{% if events %}
{% if events[-1].date <= day.date %}
{% set event = events.pop() %}

{% if event.assignment.type == "project" %}

{% if event.type == "start" %}
{% set active.project = event.assignment %}
{% elif event.type == "end" %}
{% set active.project = none %}
{% endif %}

{% do status.project.append(event.type) %}

{% elif event.assignment.type == "homework" %}

{% if event.type == "start" %}
{% set active.homework = event.assignment %}
{% elif event.type == "end" %}
{% set active.homework = none %}
{% endif %}

{% do status.homework.append(event.type) %}

{% endif %}

{% do update_assignment_status(events, day, active, status) %}
{% else %}

{% if status.project|length == 0 %}
{% do status.project.append("active" if active.project is not none else "inactive") %}
{% endif %}
{% if status.homework|length == 0 %}
{% do status.homework.append("active" if active.homework is not none else "inactive") %}
{% endif %}
{% endif %}
{% endif %}

{% endmacro %}


{% macro increment_lengths(items, amount=1) %}
{% for type in ["project", "homework"] %}
{% set item = items[type] %}
{% if item %}
{% do item.__setitem__('length', item.get('length', 0) + amount) %}
{% endif %}
{% endfor %}
{% endmacro %}


{%- macro classes() %}
{{- varargs[-1] }}
{%- for c in deep_get(schedule.styles, *varargs, default=[]) %} {{ c }}{% endfor %}
{%- endmacro %}


{# first pass to calculate assignment lengths #}
{% set active_assignments = namespace(project=none, homework=none) %}
{% set assignment_dates_copy = assignment_dates[:] %}
{% for day in days %}
{% if loop.changed(day.week) %}
{% do increment_lengths(active_assignments) %}
{% endif %}
{% set status = namespace(project=[], homework=[]) %}
{% do increment_lengths(active_assignments) %}
{% do update_assignment_status(assignment_dates_copy, day, active_assignments, status) %}
{% do increment_lengths(active_assignments) %}
{% endfor %}

## Calendar {: .mt-5 }

{# second pass to output table #}
{% set active_assignments = namespace(project=none, homework=none) %}
<table class="table course-calendar">
<thead>
<tr class="calendar-start">
    <th></th>
    <th>Topic</th>
    <th class="dummy"></th>
    <th>Modules</th>
    <th>homework</th>
</tr>
</thead>
<tbody>
{% for day in days %}

{# update assignment status #}
{% set status = namespace(project=[], homework=[]) %}
{% do update_assignment_status(assignment_dates, day, active_assignments, status) %}

{%- if loop.changed(day.week) %}
<tr class="week-start">
<td colspan="2" class="week-name">Week {{ day.week }}</td>
<td class="dummy"></td>
{% for type in ["project", "homework"] %}
{% if "active" not in status[type] and "end" not in status[type] %}
<td class="{{ type }}-inactive"></td>
{% endif %}
{% endfor %}
</tr>
{%- endif %}
<tr class="row-{{ day.type }}">
<td rowspan="2" class="class-date">{{ day.date.strftime("%a %m/%d") }}</td>
{% if day.is_dummy %}
<td rowspan="2" class="class-data">
</td>
{% else %}
<td rowspan="2" class="class-data">
<div class="class-title">
    {%- if day.is_exam %}
    <span class="class-title-label label-373 label-exam">EXAM OH</span>
    {%- elif day.type == "lecture" %}
    <span class="class-title-label label-373 label-lecture">LEC {{ "{:>02}".format(day.num) }}</span>
    {%- elif day.type == "section" %}
    <span class="class-title-label label-373 label-section">SEC {{ "{:>02}".format(day.num)  }}</span>
    {%- elif day.type == "holiday" %}
    <span class="class-title-label label-373 label-holiday">HOLIDAY</span>
    {%- endif %}

    <span class="class-title-text">{{ day.title }}</span>
</div>
{% set resources = day.get('resources', {}).items()|selectattr(1) %}
{% if resources %}
<div class="class-resources">
{% for res_type, res in resources %}
<div class="resource-group resource-group-{{ res_type }}">
<span class="resource-label">{{ res_type }}:</span>
<span class="{{ classes('resources', res_type, 'resource-links') }}">
{% for res_name, res_url in res.items() %}
{%- if res_url %}
<a href="{{ res_url.format(**day)|url }}" class="{{ classes('resources', res_type, 'resource-link') }} {{ res_name }}">{{ res_name }}</a>
{%- else %}
<a class="{{ classes('resources', res_type, 'resource-link') }} {{ res_name }} disabled">{{ res_name }}</a>
{%- endif %}
{%- if not loop.last and res_type != 'slides' and res_type != 'worksheet' %}, {% endif %}
{% endfor %}
</span>
</div>
{% endfor %}
</div>
{% endif %}
</td>
{% endif %}


<td class="dummy"></td>
{% for type in ["project", "homework"] %}
{% if "active" not in status[type] and "end" not in status[type] %}
<td class="{{ type }}-inactive"></td>
{% endif %}
{% endfor %}
</tr>

<tr class="row-{{ day.type }}">
<td class="dummy"></td>
{% for type in ["project", "homework"] %}
{% if "start" in status[type] %}
{% set assignment = active_assignments[type] %}
{% set real_type = 'exam' if (assignment.type == "homework" and assignment.is_exam) else assignment.type %}
<td rowspan="{{ assignment.length }}" class="assignment {{ real_type }} {{ 'active' if assignment.url }}">
    <span class="assignment-boundary assignment-released">Released</span>
    {% if assignment.url %}
    <a href="{{ assignment.url.format(**assignment)|url }}" class="assignment-link stretched-link">
    {% else %}
    <a class="assignment-link stretched-link disabled">
    {% endif %}
    <div class="assignment-text">
        {%- if real_type == "project" %}
            <span class="assignment-label label-373 label-project">V{{ assignment.num }}</span>
            <div class="assignment-title">{{ assignment.title }}</div>
        {%- elif real_type == "exam" %}
            <span class="assignment-label label-373 label-exam">EXAM {{ assignment.num }}</span>
        {%- elif real_type == "homework" %}
            <span class="assignment-label label-373 label-exercise">HW{{ assignment.num }}</span>
            <div class="assignment-title">{{ assignment.title }}</div>
        {%- endif %}
    </div>
    </a>
    <span class="assignment-boundary assignment-due">Due 11:59pm</span>
</td>
{% elif "active" not in status[type] %}
<td class="{{ type }}-inactive"></td>
{% endif %}
{% endfor %}
</tr>
{% endfor %}
</tbody>
</table>
