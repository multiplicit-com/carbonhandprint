"""Check the built site against _data/limited_sources.yml.

Run after `bundle exec jekyll build`. Lists any page where one listed site,
or all listed sites together, go over their share of the page's outside
links. Pages with a single outside link are fine.
"""
import glob
import re
import sys
from urllib.parse import urlparse

import yaml

SKIP = ("carbonhandprint.org", "wikipedia.org", "facebook.com")
cfg = yaml.safe_load(open("_data/limited_sources.yml")) or {}
sites = cfg.get("sites") or []
per_site = cfg.get("per_site", 50)
combined = cfg.get("combined", 66)


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
    total = 0
    for site in sites:
        n = sum(matches(urlparse(u).netloc, site) for u in links)
        total += n
        if n * 100 > per_site * len(links):
            bad += 1
            print(f"{path}: {n} of {len(links)} outside links are from {site}")
    if total * 100 > combined * len(links):
        bad += 1
        print(f"{path}: {total} of {len(links)} outside links are from listed sites")
print("ok" if not bad else f"{bad} problem(s) found")
sys.exit(1 if bad else 0)
