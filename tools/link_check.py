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
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', '_site', 'vendor', 'node_modules', '.jekyll-cache', '.github', 'tools'}
EXTS = ('.md', '.html', '.yml', '.yaml')
SKIP_HOSTS = ('carbonhandprint.org', 'localhost', 'example.com', 'fonts.googleapis.com',
              'schema.org', 'www.w3.org', 'w3.org', 'facebook.com')
URL_RE = re.compile(r'https?://[^\s"\'<>()\[\]{}|\\^`]+')
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
BOT_UA = 'CarbonHandprintLinkCheck/1.0 (+https://carbonhandprint.org/)'
PAYWALL_URL = re.compile(r'paywall|/subscribe|subscription|/login|/signin|sign-in|/register|/account', re.I)
# Only strong signals: publishers mark paywalled articles with isAccessibleForFree.
PAYWALL_TEXT = re.compile(r'"isAccessibleForFree"\s*:\s*"?false|subscribe to (continue|keep) reading|'
                          r'this (article|story|content) is (only )?(for|available to) (subscribers|members)|'
                          r'create a free account to (continue|keep) reading', re.I)
UNCHECKABLE = (401, 403, 405, 406, 429, 451, 503)


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
                if u.endswith('/') and text[text.find(u) + len(u):][:1] == '{':
                    continue  # template link filled in at build time
                host = urllib.parse.urlsplit(u).hostname or ''
                if not host or host.endswith('.example') or any(host == h or host.endswith('.' + h) for h in SKIP_HOSTS):
                    continue
                found.setdefault(u, set()).add(rel)
    return found


def same_place(a, b):
    """True if b is still a, give or take http(s), www, a trailing slash,
    an added language folder or index page, or added query parameters."""
    def norm(u):
        s = urllib.parse.urlsplit(u)
        path = urllib.parse.unquote(s.path).rstrip('/') or '/'
        return (s.hostname or '').removeprefix('www.'), path, s.query
    (ha, pa, qa), (hb, pb, qb) = norm(a), norm(b)
    if ha != hb:
        return False
    if pa == pb or pb.startswith(pa.rstrip('/') + '/index.'):
        return True
    return pa == '/' and re.fullmatch(r'/[a-z]{2}(-[a-z]{2})?', pb, re.I) is not None


def safe(url):
    """Percent-encode any non-ASCII characters so the request can be sent."""
    s = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit((s.scheme, s.netloc.encode('idna').decode(),
                                    urllib.parse.quote(s.path, safe="/%:@!$&'()*+,;=-._~"),
                                    urllib.parse.quote(s.query, safe="=&%+/:,;@-._~"), s.fragment))


def fetch(url):
    # Wikipedia asks automated clients to name themselves, and refuses browser-like ones.
    ua = BOT_UA if (urllib.parse.urlsplit(url).hostname or '').endswith('wikipedia.org') else UA
    req = urllib.request.Request(safe(url), headers={'User-Agent': ua, 'Accept': 'text/html,*/*',
                                               'Accept-Language': 'en-GB,en;q=0.9'})
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read(400_000).decode('utf-8', errors='ignore') \
            if 'html' in r.headers.get('Content-Type', '') else ''
        return r.geturl(), r.status, body


def check(url):
    for attempt in range(2):
        try:
            final, code, body = fetch(url)
            break
        except urllib.error.HTTPError as e:
            if e.code in (404, 410):
                return 'dead', str(e.code), None
            if attempt == 0 and e.code in (429, 503):
                time.sleep(10)
                continue
            if e.code in UNCHECKABLE:
                return 'blocked', f'{e.code} (site may refuse automated checks)', None
            return 'dead', str(e.code), None
        except Exception as e:  # DNS, TLS, timeouts, dropped connections
            reason = str(getattr(e, 'reason', e))
            if 'Name or service not known' in reason or 'CERTIFICATE' in reason:
                return 'dead', type(e).__name__ + ': ' + reason[:80], None
            if attempt == 0:
                time.sleep(5)
                continue
            return 'blocked', 'no answer: ' + type(e).__name__, None
    if BOT_UA = 'CarbonHandprintLinkCheck/1.0 (+https://carbonhandprint.org/)'
PAYWALL_URL.search(urllib.parse.urlsplit(final).path) and not BOT_UA = 'CarbonHandprintLinkCheck/1.0 (+https://carbonhandprint.org/)'
PAYWALL_URL.search(url):
        return 'paywall', 'sends readers to a sign-in or subscribe page', final
    m = PAYWALL_TEXT.search(body)
    if m:
        return 'paywall', f'page says "{m.group(0)}"', None
    if not same_place(url, final):
        if urllib.parse.urlsplit(final).path in ('', '/'):
            return 'dead', 'redirects to the home page', final
        return 'moved', f'{code}, redirected', final
    return 'ok', str(code), None


def main():
    targets = sys.argv[1:] or ['.']
    links = collect(targets)
    print(f'Checking {len(links)} outside links...', file=sys.stderr)
    # One request at a time per site, with a pause, so no site is hammered.
    by_host = {}
    for u in links:
        by_host.setdefault(urllib.parse.urlsplit(u).hostname, []).append(u)

    def run(urls):
        out = {}
        for i, u in enumerate(urls):
            if i:
                time.sleep(2)
            out[u] = check(u)
        return out
    results = {}
    with cf.ThreadPoolExecutor(8) as ex:
        for res in ex.map(run, by_host.values()):
            results.update(res)
    heads = [('dead', 'Broken or missing (open in a browser to confirm: some sites refuse checks from servers)'), ('paywall', 'Possible paywall or sign-up wall'),
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
