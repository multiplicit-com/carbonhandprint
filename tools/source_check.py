"""Check the built site against _data/limited_sources.yml.

Run after `bundle exec jekyll build`. Lists any page where any one listed site
makes up more than half of its outside links (pages with one link are fine).
"""
import glob
import re
import sys
from urllib.parse import urlparse

import yaml

SKIP = ("carbonhandprint.org", "wikipedia.org", "facebook.com")
sites = yaml.safe_load(open("_data/limited_sources.yml")) or []

def matches(host, site):
    host = host.lower().removeprefix("www.")
    return host == site or host.endswith("." + site)

bad = 0
for path in sorted(glob.glob("_site/**/index.html", recursive=True)):
    html = open(path, encoding="utf-8").read()
    links = {u for u in re.findall(r'href="(https?://[^"]+)"', html)
             if not any(s in urlparse(u).netloc for s in SKIP)}
    if len(links) < 2:
        continue
    for site in sites:
        n = sum(matches(urlparse(u).netloc, site) for u in links)
        if n * 2 > len(links):
            bad += 1
            print(f"{path}: {n} of {len(links)} outside links are from {site}")
print("ok" if not bad else f"{bad} page(s) over the limit")
sys.exit(1 if bad else 0)
