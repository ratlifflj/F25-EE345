---
template: no-toc.html
title: Announcements
description: A feed containing all of the class announcements.
nav_exclude: true
---

{% for announcement in announcements | sort(attribute="meta.date", reverse=True) %}
{% include 'announcement.html' %}
{% endfor %}
