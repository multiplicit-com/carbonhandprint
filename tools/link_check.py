#!/usr/bin/env python3
"""Check outside links in news items, articles, pages and data files.

Card images are skipped: a broken one shows a plain fallback graphic.

Reports links that look dead, have moved, or may be behind a paywall or
sign-up wall. It never changes any files: fix or replace links by hand.

    python3 tools/link_check.py            # check everything
    python3 tools/link_check.py _news      # check one folder or file

Writes a Markdown report to stdout (and to the GitHub job summary when run
as an Action). Sites that refuse automated checks are listed separately so
they can be opened in a browser.
"""
import concurrent.futures as cf
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', '_site', 'vendor', 'node_modules', '.jekyll-cache', '.github', 'tools'}
EXTS = ('.md', '.html', '.yml', '.yaml')
SKIP_HOSTS = ('carbonhandprint.org', 'localhost', 'example.com', 'fonts.googleapis.com',
              'schema.org', 'www.w3.org', 'w3.org')
URL_RE = re.compile(r'https?://[^\s"\'<>()\[\]{}|\\^`]+')
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
PAYWALL_URL = re.compile(r'paywall|/subscribe|subscription|/login|/signin|sign-in|/register|/account', re.I)
PAYWALL_TEXT = re.compile(r'"isAccessibleForFree"\s*:\s*"?false|subscribers? only|subscribe to (continue|read)|'
                          r'this (article|content) is (for|available to) (subscribers|members)|'
                          r'already a subscriber|create a free account to (continue|read)|piano\.io|tinypass', re.I)


def files(targets):
    for t in targets:
        t = os.path.join(ROOT, t)
        if os.path.isfile(t):
            yield t
            continue
        for d, dirs, fs in os.walk(t):
            dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
            for f in fs:
                if f.endswith(EXTS):
                    yield os.path.join(d, f)


def collect(targets):
    found = {}
    for p in files(targets):
        rel = os.path.relpath(p, ROOT)
        with open(p, encoding='utf-8', errors='ignore') as fh:
            text = '\n'.join(l for l in fh if not l.lstrip().startswith('card_image:'))
            for u in URL_RE.findall(text):
                u = u.rstrip('.,;:\'"')
                host = urllib.parse.urlsplit(u).hostname or ''
                if not host or any(host == h or host.endswith('.' + h) for h in SKIP_HOSTS):
                    continue
                found.setdefault(u, set()).add(rel)
    return found


def same_place(a, b):
    """True if b is a, give or take http(s), www and a trailing slash."""
    def norm(u):
        s = urllib.parse.urlsplit(u)
        host = (s.hostname or '').removeprefix('www.')
        return host, s.path.rstrip('/') or '/', s.query
    return norm(a) == norm(b)


def check(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'text/html,*/*',
                                               'Accept-Language': 'en-GB,en;q=0.9'})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            final, code = r.geturl(), r.status
            body = r.read(400_000).decode('utf-8', errors='ignore') \
                if 'html' in r.headers.get('Content-Type', '') else ''
    except urllib.error.HTTPError as e:
        if e.code in (401, 403, 429, 451, 503):
            return 'blocked', f'{e.code} (site may refuse automated checks)', None
        return 'dead', str(e.code), None
    except Exception as e:  # DNS, TLS, timeouts
        return 'dead', type(e).__name__ + ': ' + str(getattr(e, 'reason', e))[:80], None
    if PAYWALL_URL.search(urllib.parse.urlsplit(final).path) and not PAYWALL_URL.search(url):
        return 'paywall', 'sends readers to a sign-in or subscribe page', final
    if PAYWALL_TEXT.search(body):
        return 'paywall', 'page mentions subscribers or a sign-up wall', None
    if not same_place(url, final):
        if urllib.parse.urlsplit(final).path in ('', '/'):
            return 'dead', 'redirects to the home page', final
        return 'moved', f'{code}, redirected', final
    return 'ok', str(code), None


def main():
    targets = sys.argv[1:] or ['.']
    links = collect(targets)
    print(f'Checking {len(links)} outside links...', file=sys.stderr)
    results = {}
    with cf.ThreadPoolExecutor(8) as ex:
        for url, res in zip(links, ex.map(check, links)):
            results[url] = res
    heads = [('dead', 'Dead or broken'), ('paywall', 'Possible paywall or sign-up wall'),
             ('moved', 'Redirected (check the new page is the same article)'),
             ('blocked', 'Could not check (open these in a browser)')]
    out = [f'# Link check\n\n{len(links)} outside links checked. Nothing has been changed.\n']
    for key, title in heads:
        rows = sorted((u, r) for u, r in results.items() if r[0] == key)
        out.append(f'\n## {title}: {len(rows)}\n')
        for u, (_, note, final) in rows:
            where = ', '.join(sorted(links[u]))
            out.append(f'- {u}\n  - {note}' + (f': {final}' if final else '') + f'\n  - in {where}')
    report = '\n'.join(out) + '\n'
    print(report)
    summary = os.environ.get('GITHUB_STEP_SUMMARY')
    if summary:
        with open(summary, 'a') as fh:
            fh.write(report)


if __name__ == '__main__':
    main()
