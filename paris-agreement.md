---
layout: page
title: Where the Paris Agreement stands
lede: The 2015 Paris Agreement is still the backbone of global climate action. Ten years on, here are the facts on where it stands, updated after COP31 in November 2026.
permalink: /paris-agreement/
description: A plain-English, regularly updated summary of the Paris Agreement's status, national climate plans, the US withdrawal and COP31.
---

## The agreement in one paragraph

Adopted in December 2015, the Paris Agreement commits almost every country to holding warming "well below" 2 °C above pre-industrial levels, and to pursuing efforts to limit it to 1.5 °C. Each country sets its own targets, called nationally determined contributions (NDCs), and is expected to strengthen them every five years. Progress is checked by a "global stocktake".

## The state of play, late 2026

**The plans don't add up yet.** The UN's latest synthesis covers new plans from 154 countries, about 71% of global emissions. Together with current policies elsewhere, they point to global emissions about **6% below 2019 levels by 2035**. Staying near 1.5 °C needs roughly a **60%** cut over the same period. Projected warming by 2100 is 2.1 to 3.2 °C. ([Climate Home News](https://climatechangenews.com/2026/10/27/national-climate-plans-now-promise-half-the-emission-cuts-expected-by-un))

**1.5 °C will be overshot.** It is now widely accepted that warming will pass 1.5 °C, at least temporarily. The debate has moved to how far and for how long, and how quickly temperatures can be brought back down.

**The United States has left.** President Trump signed an order to withdraw on 20 January 2025, and US withdrawal took effect on 27 January 2026. In January 2026 the administration also announced it would leave the UN climate convention (UNFCCC) itself. ([Harvard EELP](https://eelp.law.harvard.edu/tracker/paris-climate-agreement))

**COP31 made progress but no headline deal.** The summit in Antalya, Türkiye (9 to 22 November 2026) became the longest COP on record. Countries agreed decisions on a just transition, adaptation, climate finance and carbon markets, and launched the second global stocktake, which concludes in 2028. But the presidency's overarching "Antalya pact" was rejected by the EU, the UK and climate-vulnerable nations, chiefly because it did not mention fossil fuels. Around 80 countries backed a separate pledge to get 35% of final energy from electricity by 2035. ([UNFCCC](https://unfccc.int/news/cop31-delivers-important-progress-across-negotiations-and-action-agenda-advancing-implementation-but), [Carbon Brief](https://www.carbonbrief.org/cop31-key-outcomes-agreed-at-the-un-climate-talks-in-antalya))

## Why it matters for your handprint

Global deals set the direction, but they are delivered by millions of decisions at every level: national energy policy, a council's transport plan, a company's product design, a household's choice of boiler. When the international process stalls, those decisions matter more, not less. Telling your representatives that you want their country's plan strengthened is one of the biggest handprint actions available to anyone.

## Articles on the Paris Agreement

{% assign paris = site.posts | where_exp: "p", "p.tags contains 'paris-agreement'" %}
{% if paris.size > 0 %}
<ul class="posts">
{% for post in paris %}<li><a href="{{ post.url | relative_url }}">{{ post.title }}</a><p>{{ post.date | date: "%-d %B %Y" }}{% if post.description %} · {{ post.description }}{% endif %}</p></li>
{% endfor %}</ul>
{% else %}
<p class="meta">Articles coming soon.</p>
{% endif %}

<p class="meta">Last updated 26 November 2026.</p>
