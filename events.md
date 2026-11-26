---
layout: page
wide: true
accent: blue
title: Climate talks and deadlines
lede: Every UN climate conference since the Paris Agreement, what came out of each, and the dates still to come.
permalink: /events/
description: Dates, venues and outcomes of every UN climate conference (COP) since Paris in 2015, plus upcoming COPs and key Paris Agreement deadlines.
---
{% assign now = site.time | date: "%Y-%m-%d" %}{% assign evs = site.data.events | sort: "start" %}
<p class="jump">On this page: <a href="#coming-up">Coming up</a> · <a href="#since-paris">Since Paris</a> · <a href="#deadlines-passed">Deadlines passed</a> · <a href="/paris-agreement/">Where the Paris Agreement stands</a></p>

The UN's yearly climate conference is the COP, the Conference of the Parties. Each year's host is chosen in rotation between world regions. Between COPs, negotiators also meet in Bonn each June. Under the Paris Agreement, every country sets out its own climate plan, called an NDC, and updates it every five years.

## Coming up {#coming-up}

<ol class="events">
{% for e in evs %}{% assign last = e.end | default: e.start | date: "%Y-%m-%d" %}{% if last >= now %}<li class="ev-{{ e.kind }}">
  <span class="ev-when">{% if e.year %}By {{ e.year }}{% elsif e.end %}{{ e.start | date: "%-d %b" }} to {{ e.end | date: "%-d %b %Y" }}{% else %}{{ e.start | date: "%-d %B %Y" }}{% endif %}</span>
  <span class="ev-name">{{ e.name }}{% if e.kind == "deadline" %} <span class="ev-kind">· deadline</span>{% endif %}</span>
  {% if e.place %}<span class="ev-place">{% if e.country %}<a href="{{ '/countries/' | append: e.country | append: '/' | relative_url }}">{{ e.place }}</a>{% else %}{{ e.place }}{% endif %}</span>{% endif %}
  <span class="ev-text">{{ e.text }} <a class="src" href="{{ e.url }}">{{ e.source }}</a></span>
</li>
{% endif %}{% endfor %}</ol>

## Since Paris {#since-paris}

<ol class="events" reversed>
{% assign past = evs | reverse %}{% for e in past %}{% assign last = e.end | default: e.start | date: "%Y-%m-%d" %}{% if last < now and e.kind != "deadline" %}<li class="ev-{{ e.kind }}">
  <span class="ev-when">{{ e.start | date: "%-d %b" }} to {{ e.end | date: "%-d %b %Y" }}</span>
  <span class="ev-name">{{ e.name }}</span>
  {% if e.place %}<span class="ev-place">{% if e.country %}<a href="{{ '/countries/' | append: e.country | append: '/' | relative_url }}">{{ e.place }}</a>{% else %}{{ e.place }}{% endif %}</span>{% endif %}
  <span class="ev-text">{{ e.text }} <a class="src" href="{{ e.url }}">{{ e.source }}</a></span>
</li>
{% endif %}{% endfor %}</ol>

There was no COP in 2020 because of the pandemic. End dates are when talks actually closed, which is often a day or two late.

## Deadlines passed {#deadlines-passed}

<ol class="events">
{% for e in past %}{% assign last = e.end | default: e.start | date: "%Y-%m-%d" %}{% if last < now and e.kind == "deadline" %}<li class="ev-deadline">
  <span class="ev-when">{{ e.start | date: "%-d %B %Y" }}</span>
  <span class="ev-name">{{ e.name }}</span>
  <span class="ev-text">{{ e.text }} <a class="src" href="{{ e.url }}">{{ e.source }}</a></span>
</li>
{% endif %}{% endfor %}</ol>

Countries' own targets, such as their net zero years, are on each [country page](/paris-agreement/#countries).

<script type="application/ld+json">[{% assign first = true %}{% for e in evs %}{% assign last = e.end | default: e.start | date: "%Y-%m-%d" %}{% if last >= now and e.city %}{% unless first %},{% endunless %}{% assign first = false %}{"@context":"https://schema.org","@type":"Event","name":{{ e.name | append: ", UN Climate Change Conference" | jsonify }},"startDate":"{{ e.start | date: '%Y-%m-%d' }}","endDate":"{{ e.end | date: '%Y-%m-%d' }}","eventStatus":"https://schema.org/EventScheduled","eventAttendanceMode":"https://schema.org/OfflineEventAttendanceMode","location":{"@type":"Place","name":{{ e.city | jsonify }},"address":{"@type":"PostalAddress","addressLocality":{{ e.city | jsonify }},"addressCountry":{{ e.country_name | jsonify }}}},"organizer":{"@type":"Organization","name":"UNFCCC","url":"https://unfccc.int/"},"description":{{ e.text | jsonify }},"url":{{ e.url | jsonify }}}{% endif %}{% endfor %}]</script>
