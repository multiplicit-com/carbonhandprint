#!/usr/bin/env python3
"""Fill in a link card for a news or response post.

Usage:
    python3 tools/og.py _news/2027-01-15-some-story.md [more files...]

Reads the post's `link:`, fetches that page, and adds `card_image:` (and
`link_title:` if missing) to the front matter, using the page's Open Graph
tags. Run it again with --force to overwrite existing values.
"""
import re, sys, urllib.request, urllib.parse
from html.parser import HTMLParser


class OG(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = {}

    def handle_starttag(self, tag, attrs):
        if tag != "meta":
            return
        a = dict(attrs)
        key = a.get("property") or a.get("name") or ""
        if key.startswith(("og:", "twitter:")) and a.get("content") and key not in self.tags:
            self.tags[key] = a["content"].strip()


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (link preview)"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read(600_000).decode("utf-8", "replace")


def update(path, force):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return print(f"{path}: no front matter")
    fm = m.group(1)
    link = re.search(r"^link:\s*(\S+)", fm, re.M)
    if not link:
        return print(f"{path}: no link")
    if re.search(r"^snippet:\s*true", fm, re.M):
        return print(f"{path}: snippet, no card needed")
    if re.search(r"^card_image:", fm, re.M) and not force:
        return print(f"{path}: already has card_image")
    p = OG()
    try:
        p.feed(fetch(link.group(1)))
    except Exception as e:
        return print(f"{path}: could not fetch {link.group(1)} ({e})")
    image = p.tags.get("og:image") or p.tags.get("twitter:image")
    if image and not image.startswith("http"):
        image = urllib.parse.urljoin(link.group(1), image)
    title = p.tags.get("og:title") or p.tags.get("twitter:title")

    def setfield(fm, key, value):
        line = f'{key}: "{value.replace(chr(34), chr(39))}"'
        if re.search(rf"^{key}:", fm, re.M):
            return re.sub(rf"^{key}:.*$", lambda _: line, fm, flags=re.M) if force else fm
        return fm + "\n" + line

    new = fm
    if image:
        new = setfield(new, "card_image", image)
    if title:
        site = p.tags.get("og:site_name", "")
        src = re.search(r'^source:\s*"?([^"\n]+)"?', fm, re.M)
        for name in filter(None, [site, src.group(1) if src else ""]):
            title = re.sub(rf"\s+[-|–]\s+{re.escape(name)}.*$", "", title, flags=re.I)
        title = re.sub(r"\s+[|]\s+[^|]+$", "", title)
        new = setfield(new, "link_title", title.strip())
    if new == fm:
        return print(f"{path}: no Open Graph tags found")
    open(path, "w", encoding="utf-8").write(text.replace(fm, new, 1))
    print(f"{path}: card_image {image or '-'}")


def main():
    files = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not files:
        sys.exit(__doc__)
    for path in files:
        update(path, "--force" in sys.argv)


if __name__ == "__main__":
    main()
