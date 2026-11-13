"""A6's public checks of the published Space (CP-18c): fresh observations of the public origin in Chromium and WebKit.

Committed after the publication found the History route redirected away from the Space when opened as a directory;
the check follows the page's own History link and requires v1's page on the Space's origin.

    PLAYWRIGHT_BROWSERS_PATH=<ms-playwright> <playwright python> public_check.py --origin <https origin> \
        --manifest <the intended bundle's manifest.json> --out <record.json> --shots <folder>

For each engine and width: the product page from a cold start to its ready state (or its start error), the manifest's
served identity against the intended one, every view opened by its deep link and checked for a failed state, the
History route opened, and every request's host recorded. Requests to any host other than the Space's own origin are
listed (A9's network rule), not hidden. No credential is read; nothing is written anywhere but --out and --shots.
"""
import argparse
import hashlib
import json
import time
import urllib.parse
from pathlib import Path

from playwright.sync_api import sync_playwright

VIEWS = ('train', 'forecast', 'validation', 'reliability', 'explainability', 'features', 'data', 'limitations', 'history')
WIDTHS = (1440, 390)


def wait_until(page, expr, timeout):
    t0 = time.time()
    while time.time() - t0 < timeout:
        if page.evaluate(expr):
            return True
        time.sleep(0.25)
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--origin', required=True)
    ap.add_argument('--manifest', required=True, type=Path)
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--shots', required=True, type=Path)
    ap.add_argument('--history-title', default='DE-LU Day-Ahead Forecast — runs in your browser',
                    help="v1's page title, as its deployed index.html states it (reports/cp18c/history-v1/files)")
    args = ap.parse_args()
    own = urllib.parse.urlparse(args.origin).hostname
    intended = json.loads(args.manifest.read_text())
    args.shots.mkdir(parents=True, exist_ok=True)
    checks = []
    record = {'origin': args.origin, 'started_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
              'intended_artifact': intended['artifact']['artifact_sha256'], 'checks': checks}

    def check(name, ok, **detail):
        checks.append({'check': name, 'passed': bool(ok), **detail})
        print('PASS' if ok else 'FAIL', name, json.dumps(detail, default=str)[:200], flush=True)

    with sync_playwright() as pw:
        for engine in ('chromium', 'webkit'):
            browser = pw.chromium.launch(channel='chromium', headless=True) if engine == 'chromium' else pw.webkit.launch(headless=True)
            for width in WIDTHS:
                ctx = browser.new_context(viewport={'width': width, 'height': 900})
                page = ctx.new_page()
                hosts = {}
                page.on('request', lambda r: hosts.__setitem__(urllib.parse.urlparse(r.url).hostname,
                                                                hosts.get(urllib.parse.urlparse(r.url).hostname, 0) + 1))
                t0 = time.time()
                page.goto(args.origin, wait_until='domcontentloaded', timeout=120000)
                ready = wait_until(page, '!!(window.__space && (window.__space.ready || window.__space.startError))', 180)
                state = page.evaluate('window.__space ? {ready: !!window.__space.ready, error: window.__space.startError || null} : null')
                check(f'{engine} {width}: cold start reaches the ready state', ready and state and state['ready'],
                      seconds=round(time.time() - t0, 1), state=state)
                text = page.inner_text('body')
                check(f'{engine} {width}: the served identity names the intended daily artifact',
                      intended['artifact']['artifact_sha256'][:12] in text)
                check(f'{engine} {width}: the product name and status are shown',
                      'v6 · DDNN-2 alone' in text and 'final candidate · pending 4.7T' in text)
                failed_files = page.evaluate("Array.from(document.querySelectorAll('[data-failed-file]')).map(e => e.dataset.failedFile)")
                check(f'{engine} {width}: no verification failure', not failed_files, failed=failed_files)
                shot = args.shots / f'{engine}-{width}-panel.png'
                page.screenshot(path=str(shot), full_page=False)
                for view in VIEWS:
                    page.evaluate(f"location.hash = '#{view}'")
                    time.sleep(1.5 if view != 'validation' else 4)
                    failed = page.evaluate(f"!!document.querySelector('[data-view-panel=\"{view}\"] [data-state=\"failed\"]')")
                    shown = page.evaluate(f"(() => {{ const p = document.querySelector('[data-view-panel=\"{view}\"]'); return !!p && !p.hidden && p.innerText.trim().length > 0; }})()")
                    check(f'{engine} {width}: view {view} renders without a failed state', shown and not failed)
                others = {h: n for h, n in hosts.items() if h != own}
                check(f'{engine} {width}: the product page requests its own origin only', not others, hosts=hosts)
                ctx.close()
            ctx = browser.new_context(viewport={'width': 1440, 'height': 900})
            page = ctx.new_page()
            page.goto(args.origin, wait_until='domcontentloaded', timeout=120000)
            wait_until(page, '!!(window.__space && (window.__space.ready || window.__space.startError))', 180)
            page.evaluate("location.hash = '#history'")
            time.sleep(1.5)
            href = page.evaluate("(() => { const a = document.querySelector('[data-history-link]'); return a ? a.href : null; })()")
            resp = page.goto(href, wait_until='load', timeout=120000) if href else None
            time.sleep(5)
            final = urllib.parse.urlparse(page.url)
            raw_title = None
            if resp is not None:
                import re
                body = resp.body().decode('utf-8', 'replace')
                m = re.search(r'<title>(.*?)</title>', body)
                raw_title = m.group(1) if m else None
            check(f"{engine}: the Space's own History link opens v1's page on the Space's origin",
                  resp is not None and resp.status == 200 and final.hostname == own and raw_title == args.history_title,
                  href=href, final_url=page.url, status=resp.status if resp else None, served_title=raw_title)
            page.screenshot(path=str(args.shots / f'{engine}-history.png'))
            ctx.close()
            browser.close()
    record['shots'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(args.shots.glob('*.png'))}
    record['passed'] = sum(c['passed'] for c in checks)
    record['failed'] = sum(not c['passed'] for c in checks)
    record['finished_utc'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    args.out.write_text(json.dumps(record, indent=1, sort_keys=True) + '\n')
    print('public checks:', record['passed'], 'passed,', record['failed'], 'failed')


if __name__ == '__main__':
    main()
