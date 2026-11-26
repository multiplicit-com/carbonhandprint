---
section: explore
schema_type: CollectionPage
item_list: reading
wide: true
related: reading
layout: page
accent: mustard
title: Reading list
lede: The handprint idea has been taken up by research institutes, universities, standards bodies and large companies. These are the key pieces, oldest first.
permalink: /reading/
description: A dated reading list of articles, research and reports on the carbon handprint concept since 2007.
---

<ol class="timeline">
{% for r in site.data.reading %}  <li><span class="yr">{{ r.when }}</span><span><a href="{{ r.url }}">{{ r.title }}</a>, {{ r.text }}</span></li>
{% endfor %}</ol>

For methods, research reports and company reports, see our [white papers](/white-papers/).

Know of something we've missed, especially from the early years? [Tell us](/contact/).
