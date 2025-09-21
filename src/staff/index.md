---
title: Staff
nav_order: 98
description: A listing of all the course staff members.
extra_css: ['staff.scss']
---

## Getting Help

If you have a general question that other students could potentially benefit from, considering posting on Discord. 

For logistical questions (such as extenuating circumstances and DRS accomodations), please email Professor Ratliff and the TAs, so we can get back to you as quickly as possible. For sensitive situations, you can also email [Professor Ratliff](mailto:ratliffl&commat;uw&#x0002E;edu) directly if you would feel more comfortable.

We are often available at other times by appointment, and we encourage you to schedule 1:1 appointments whenever you want to talk about concepts, grades, internships, research, or anything else.

## Instructor

<div class="role">
  {% for page in (staff | sort(attribute='meta.name')) if page.meta.role == 'Instructor' %}
    {% include 'staffer.html' %}
    {{ "<hr>" if not loop.last }}
  {% endfor %}
</div>

## Teaching Assistants

<div class="role">
  {% for page in (staff | sort(attribute='meta.name')) if page.meta.role == 'Teaching Assistant' %}
    {% include 'staffer.html' %}
    {{ "<hr>" if not loop.last }}
  {% endfor %}
</div>
