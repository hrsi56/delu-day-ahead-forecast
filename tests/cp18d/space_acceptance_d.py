#!/usr/bin/env python3
"""CP-18d: the final-product Space's local browser acceptance for the Owner's decision 31 and the Space's follow-ups.

Runs under the Playwright tool environment (standard library plus `playwright`), like CP-18c's
`tests/cp18c/space_acceptance.py`, whose local server, record and page helpers it reuses unchanged. One 127.0.0.1
server per built Space; in every browser context every request whose origin is not that server is blocked and
recorded. Chromium and WebKit are driven one after the other, each at 1440 and 390 px.

    PLAYWRIGHT_BROWSERS_PATH=<.local/tools/ms-playwright> <playwright python> tests/cp18d/space_acceptance_d.py \\
        --dist after=<built Space> --dist before=<built Space> --scratch <folder> [--engines chromium,webkit]

Each `--dist` is a local build with `--live` (never published): `after`, a store copy with one day relabelled by the
TEST FIXTURE `tests/cp18d/fixture_after_cutoff.py`, and `before`, the store copy as committed (every day before the
cutoff). The expected values are read from each build's own `app/live-record.json` and `app/claims.json`.

What it checks, per build, engine and width:

- **the label** wherever an issued day is shown: the panel's served day ("Inputs"), every issue-times block (today,
  tomorrow, yesterday, the Forecast view's day, Train it yourself), the record tables, the Forecast picker, the
  Validation per-day table and the per-day chart's tooltips, Explainability and Features; the copy's retrieval time
  "fetched <time> UTC" for a day with the load forecast fetched after the cutoff; the note once per view where such a
  day appears, and never where none does;
- **the counts and the sets**: "N issued days: K ..., M ..." equal to the record; the per-day chart's distinct markers
  (one per scored day with the load forecast fetched after the cutoff) and their legend entry; the Validation rows of
  the set with every input before the cutoff equal to `evaluation_sets`; the cumulative section's two blocks (or one
  block saying the two sets are the same days), each block's rows equal to its set's series; the Reliability panels;
- **the schedule** (`live_schedule`) where the live record lists its days, with the days not issued and their causes;
- no failed or verification state, no script error, no "late" or "timely" on the page, no horizontal page scroll,
  own-origin requests only; screenshots of the product panel, Forecast and Validation, recorded with their SHA-256.

It writes `<scratch>/acceptance-d.json` and `<scratch>/shots/<build>-<engine>-<width>-<view>.png`.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tests/cp18c'))
import space_acceptance as A  # noqa: E402 - CP-18c's server, record and page helpers, unchanged

WIDTHS = ((1440, 900), (390, 844))
BANNED = re.compile(r'\blate\b|\btimely\b', re.I)
AFTER = 'load_forecast_after_cutoff'


def sha_file(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class Expect:
    """What a build should show, from its own records."""

    def __init__(self, dist: Path):
        self.live = json.loads((dist / 'app/live-record.json').read_text())
        self.claims = json.loads((dist / 'app/claims.json').read_text())['values']
        self.manifest = json.loads((dist / 'payloads/manifest.json').read_text())
        r = self.live['record']
        self.issued = {i['day']: i for i in r['issued']}
        by = {c['input_class']: c['issued'] for c in r['input_classes']}
        self.n, self.k, self.m = len(r['issued']), by.get('before_cutoff', 0), by.get(AFTER, 0)
        self.sets = {s['set']: s for s in self.live['evaluation_sets']['sets']}
        self.running = {s['set']: s for s in self.live['running']['sets']}
        self.served_day = self.manifest['artifact']['delivery_day']
        windows = json.loads((dist / 'payloads/evaluation.json').read_text())['windows']
        prod = next(w for w in windows if w['window'] == 'prospective' and w['policy'] == 'product')
        self.scored = [d['day'] for d in prod['record']['days'] if d.get('scored') and d.get('scored_hours')]

    def label(self, day: str) -> str:
        it = self.issued[day]
        if it['input_class'] != AFTER:
            return self.claims['live_input_class_before_cutoff']
        when = it['load_forecast_fetched_utc'][:19].replace('T', ' ')
        return (self.claims['live_input_class_load_forecast_after_cutoff'] + ', '
                + self.claims['live_input_class_fetched'].replace('{time}', when))

    def counts(self) -> str:
        return self.claims['live_input_class_counts'].format(n=self.n, k=self.k, m=self.m)

    def after_days(self) -> list[str]:
        return sorted(d for d, i in self.issued.items() if i['input_class'] == AFTER)


JS_LABELS = """(scope) => [...document.querySelectorAll(scope + ' [data-input-class-day]')].map(e => ({day: e.dataset.inputClassDay,
    cls: e.dataset.inputClass, fetched: e.dataset.fetched, text: e.textContent, visible: !!e.getClientRects().length}))"""
JS_STATES = """() => [...document.querySelectorAll('.state-failed, .state-verification')].filter(e => e.getClientRects().length)
    .map(e => e.textContent.slice(0, 160))"""


def labels_ok(shown: list[dict], x: Expect) -> list[str]:
    problems = []
    for s in shown:
        it = x.issued.get(s['day'])
        if not it:
            problems.append(f"{s['day']}: labelled but not an issued day")
        elif s['cls'] != it['input_class'] or s['text'] != x.label(s['day']) or (s['fetched'] or None) != it['load_forecast_fetched_utc']:
            problems.append(f"{s['day']}: shown {s['cls']} {s['text']!r}, recorded {it['input_class']} {x.label(s['day'])!r}")
    return problems


def notes(page, scope: str) -> int:
    return page.evaluate("(scope) => document.querySelectorAll(scope + ' [data-input-class-note]').length", scope)


def take_shot(rec, page, scratch: Path, name: str, selector: str | None):
    folder = scratch / 'shots'
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f'{name}.png'
    if selector and page.query_selector(selector):
        page.query_selector(selector).screenshot(path=str(path))
    else:
        page.screenshot(path=str(path), full_page=True)
    rec.value['shots'].append({'path': str(path), 'sha256': sha_file(path), 'url': page.url, 'time_utc': A.now(),
                               'selector': selector, 'viewport': page.viewport_size})


def check_build(rec, p, engine: str, build: str, dist: Path, scratch: Path):
    x = Expect(dist)
    server = A.Server(dist)
    base = server.base
    browser = p.chromium.launch(channel='chromium', headless=True) if engine == 'chromium' else p.webkit.launch(headless=True)
    rec.value['engines'][engine] = browser.version
    blocked, seen = [], []
    where = {'engine': engine, 'build': build}
    try:
        for (w, hgt) in WIDTHS:
            at = dict(where, width=str(w))
            ctx = A.open_context(browser, base, blocked, seen, viewport={'width': w, 'height': hgt})
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)[:300]))
            started = A.load(page, base + '/')
            rec.check('the build loads to its ready state', started['ready'], started, **at)
            if not started['ready']:
                ctx.close()
                continue
            texts = []
            # ---- the product panel
            shown = page.evaluate(JS_LABELS, '#product')
            days_shown = sorted({s['day'] for s in shown})
            rec.check('product panel: every issued day shown carries its label as recorded (and the copy\'s time when '
                      'fetched after the cutoff)', not labels_ok(shown, x) and set(days_shown) == set(x.issued),
                      {'days': days_shown, 'problems': labels_ok(shown, x)}, **at)
            times = page.evaluate("""() => [...document.querySelectorAll('#product [data-issue-times]')].map(e => ({day: e.dataset.issueTimes,
                cls: e.dataset.inputClass, inputs: (e.querySelector('[data-time-kind="inputs"]') || {}).textContent || null}))""")
            bad = [t for t in times if t['day'] in x.issued and (t['cls'] != x.issued[t['day']]['input_class'] or x.label(t['day']) not in (t['inputs'] or ''))]
            rec.check('product panel: each day box shows "Inputs" beside its two times', times and not bad, {'boxes': times, 'bad': bad}, **at)
            served = page.evaluate("() => { const e = document.querySelector('[data-time=\"inputs\"]'); return e ? e.textContent : null; }")
            rec.check("product panel: the served day's inputs beside its issue, run and data-refresh times",
                      served == x.label(x.served_day), {'shown': served, 'day': x.served_day, 'want': x.label(x.served_day)}, **at)
            counts = page.evaluate("() => [...document.querySelectorAll('#product [data-input-class-counts]')].map(e => [e.dataset.inputClassCounts, e.textContent])")
            rec.check('product panel: the counts per input class equal the record',
                      len(counts) == 1 and counts[0][0] == f'{x.n}/{x.k}/{x.m}' and x.counts() in counts[0][1], {'shown': counts, 'want': x.counts()}, **at)
            rec.check('product panel: the note once where a day fetched after the cutoff appears, never otherwise',
                      notes(page, '#product') == (1 if x.m else 0), {'notes': notes(page, '#product'), 'm': x.m}, **at)
            sched = page.evaluate("() => [...document.querySelectorAll('#product [data-schedule]')].map(e => e.textContent)")
            listed = page.evaluate("() => [...document.querySelectorAll('#product [data-not-issued]')].map(e => e.dataset.notIssued)")
            want_ni = sorted(d['day'] for d in x.live['record']['not_issued'] + x.live['record']['failed'] + x.live['record'].get('open', []))
            rec.check('product panel: the schedule (live_schedule) where the record lists its days; the days not issued stay listed with their causes',
                      sched == [x.claims['live_schedule']] and sorted(listed) == want_ni, {'schedule': sched, 'listed': listed, 'want': want_ni}, **at)
            texts.append(page.evaluate("() => document.querySelector('#product').innerText"))
            take_shot(rec, page, scratch, f'{build}-{engine}-{w}-product-times', '#times')
            take_shot(rec, page, scratch, f'{build}-{engine}-{w}-product-today', '#today')
            take_shot(rec, page, scratch, f'{build}-{engine}-{w}-product-earlier', '#earlier')
            # ---- Forecast
            A.open_view(page, 'forecast')
            opts = page.evaluate("() => [...document.querySelectorAll('#forecast-day option')].map(o => [o.value, o.textContent])")
            bad = [o for o in opts if (x.issued[o[0]]['input_class'] == AFTER) != (x.claims['live_input_class_load_forecast_after_cutoff'] in o[1])]
            rec.check('Forecast: the picker names each day issued with the load forecast fetched after the cutoff', not bad, {'options': opts}, **at)
            bad = {}
            for day in x.issued:
                page.select_option('#forecast-day', day)
                time.sleep(0.1)
                got = page.evaluate(JS_LABELS, '[data-forecast-panel]')
                if [s['day'] for s in got] != [day] or labels_ok(got, x):
                    bad[day] = got
            rec.check("Forecast: each issued day's panel shows its label", not bad, bad, **at)
            if x.after_days():
                page.select_option('#forecast-day', x.after_days()[0])
                time.sleep(0.2)
            shown = page.evaluate(JS_LABELS, '[data-view-panel="forecast"] [data-issued-record]')
            rec.check('Forecast: the record table labels every issued day', not labels_ok(shown, x) and sorted(s['day'] for s in shown) == sorted(x.issued),
                      labels_ok(shown, x), **at)
            fc = page.evaluate("""() => ({counts: [...document.querySelectorAll('[data-view-panel="forecast"] [data-input-class-counts]')].map(e => e.textContent),
                notes: document.querySelectorAll('[data-view-panel="forecast"] [data-input-class-note]').length,
                schedule: [...document.querySelectorAll('[data-view-panel="forecast"] [data-schedule]')].map(e => e.textContent),
                not_issued: [...document.querySelectorAll('[data-not-issued-list] [data-not-issued]')].map(e => e.dataset.notIssued)})""")
            rec.check('Forecast: the counts, the note once when a day fetched after the cutoff appears, the schedule above the days not issued',
                      len(fc['counts']) == 1 and x.counts() in fc['counts'][0] and fc['notes'] == (1 if x.m else 0)
                      and fc['schedule'] == [x.claims['live_schedule']] and sorted(fc['not_issued']) == want_ni, fc, **at)
            texts.append(page.evaluate("() => document.querySelector('[data-view-panel=\"forecast\"]').innerText"))
            take_shot(rec, page, scratch, f'{build}-{engine}-{w}-forecast-day', '[data-forecast-panel]')
            # ---- Train it yourself
            A.open_view(page, 'train')
            got = page.evaluate(JS_LABELS, '[data-view-panel="train"]')
            rec.check("Train it yourself: the retrained day's label beside its two times; the note only for a day fetched after the cutoff",
                      [s['day'] for s in got] == [x.served_day] and not labels_ok(got, x)
                      and notes(page, '[data-view-panel="train"]') == (1 if x.issued[x.served_day]['input_class'] == AFTER else 0), got, **at)
            # ---- Explainability, Features
            for view in ('explainability', 'features'):
                A.open_view(page, view)
                got = page.evaluate(JS_LABELS, f'[data-view-panel="{view}"]')
                rec.check(f"{view}: the served day's inputs", [s['day'] for s in got] == [x.served_day] and not labels_ok(got, x), got, **at)
            # ---- Validation
            A.open_view(page, 'validation')
            time.sleep(0.3)
            sec = '[data-view-panel="validation"] [data-window="prospective"]'
            rows = page.evaluate(JS_LABELS, sec + ' [data-per-day]')
            rec.check('Validation: the per-day table labels each scored day', not labels_ok(rows, x)
                      and sorted(s['day'] for s in rows) == sorted(x.scored), {'rows': [s['day'] for s in rows], 'problems': labels_ok(rows, x)}, **at)
            marks = page.evaluate("""(sec) => { const box = document.querySelector(sec + ' [data-per-day]');
                const charts = [...box.querySelectorAll('figure.chart')];
                return charts.map(f => ({own: [...f.querySelectorAll('[data-own-marker]')].map(m => [m.dataset.point, m.dataset.ownMarker]),
                    titles: [...f.querySelectorAll('[data-series^="product-"] title')].map(t => t.textContent),
                    legend: (f.querySelector('.legend') || {}).textContent || '', caption: (f.querySelector('figcaption') || {}).textContent || ''})); }""", sec)
            after_scored = [d for d in x.scored if x.issued[d]['input_class'] == AFTER]
            bad = []
            for c in marks:
                if sorted(d for d, _ in c['own']) != after_scored or any(k != 'diamond' for _, k in c['own']):
                    bad.append('markers')
                if len(c['titles']) != len(x.scored) or any(x.label(d) not in t for d, t in zip(x.scored, c['titles'])):
                    bad.append('tooltips')
                if x.counts() not in c['caption']:
                    bad.append('caption')
                if bool(x.m) != (x.claims['live_input_class_load_forecast_after_cutoff'] in c['legend']):
                    bad.append('legend')
            rec.check("Validation: the per-day charts draw the product's days fetched after the cutoff as hollow diamonds, "
                      'with a legend entry, tooltips naming each day\'s label and a caption with the counts',
                      len(marks) == 2 and not bad, {'charts': marks, 'problems': bad, 'after_scored': after_scored}, **at)
            pooled = page.evaluate("""(sec) => [...document.querySelectorAll(sec + ' tr[data-set]')].map(r => ({set: r.dataset.set, policy: r.dataset.policy || r.dataset.setPolicy,
                index: r.dataset.index || null, m: Object.fromEntries([...r.querySelectorAll('[data-metric]')].map(e => [e.dataset.metric, Number(e.dataset.v)]))}))""", sec)
            heads = page.evaluate("""(sec) => [...document.querySelectorAll(sec + ' tr[data-set-head]')].map(r => [r.dataset.setHead, r.dataset.setDays, r.textContent])""", sec)
            bad = []
            for row in pooled:
                s = x.sets[row['set']]
                rec_ = next(w['record'] for w in s['windows'] if w['policy'] == row['policy'])['pooled']
                want = {} if not rec_['scored_hours'] else {'mae': rec_['mae_eur'], 'wis': rec_['wis_eur']}
                if any(row['m'].get(k) != v for k, v in want.items()):
                    bad.append(row)
            heads_ok = [h[0] for h in heads] == ['all', 'before_cutoff'] and all(
                h[1] == str(x.sets[h[0]]['issued_days']) and f"(n = {x.sets[h[0]]['issued_days']} issued days)" in h[2] for h in heads)
            rec.check('Validation: the prospective record under its set\'s heading with its count, and the set with every input before '
                      'the cutoff after it with its count, equal to evaluation_sets', len(pooled) == 4 and not bad and heads_ok
                      and [r['set'] for r in pooled] == ['all', 'all', 'before_cutoff', 'before_cutoff'], {'rows': pooled, 'heads': heads, 'bad': bad}, **at)
            run = page.evaluate("""(sec) => { const o = document.querySelector(sec + ' [data-running-sets]'); if (!o) return null;
                return {mode: o.dataset.runningSets, sets: [...o.querySelectorAll('.running')].map(b => ({set: b.dataset.runningSet, days: b.dataset.setDays,
                    head: (b.querySelector('h5') || {}).textContent || null, charts: b.querySelectorAll('svg[role="img"]').length,
                    rows: [...b.querySelectorAll('tr[data-running-n]')].map(r => [...r.querySelectorAll('[data-mean]')].map(e => Number(e.dataset.v)))})),
                    same: (o.querySelector('[data-sets]') || {}).textContent || ''}; }""", sec)
            want_sets = ['all'] if x.m == 0 else ['before_cutoff', 'all']
            bad = []
            for b in (run or {}).get('sets', []):
                series = x.running[b['set']]['series']
                want_rows = [[q['mean'] for name in ('mae', 'wis', 'mae_vs_B0', 'wis_vs_B0') for q in series[name] if q['n'] == pt['n']] for pt in series['mae']]
                if b['rows'] != want_rows or b['days'] != str(x.running[b['set']]['issued_days']) or f"(n = {x.running[b['set']]['issued_days']} issued days)" not in (b['head'] or ''):
                    bad.append(b['set'])
            same_ok = (x.claims['live_sets_same'].format(n=x.n).lower() in run['same'].lower()) if run and x.m == 0 else True
            rec.check('Validation: the cumulative section, the set with every input before the cutoff and all issued days beside it, '
                      'each with its count and its rows; one block when the two sets are the same days, which it says',
                      run and [b['set'] for b in run['sets']] == want_sets and run['mode'] == ('same' if x.m == 0 else 'apart') and not bad and same_ok,
                      {'shown': run, 'bad': bad}, **at)
            rec.check('Validation: the note once in the view where a day fetched after the cutoff appears',
                      notes(page, '[data-view-panel="validation"]') == (1 if after_scored else 0), notes(page, '[data-view-panel="validation"]'), **at)
            texts.append(page.evaluate("() => document.querySelector('[data-view-panel=\"validation\"]').innerText"))
            take_shot(rec, page, scratch, f'{build}-{engine}-{w}-validation-prospective', sec)
            take_shot(rec, page, scratch, f'{build}-{engine}-{w}-validation-per-day', sec + ' [data-per-day]')
            take_shot(rec, page, scratch, f'{build}-{engine}-{w}-validation-cumulative', sec + ' [data-running-sets]')
            # ---- Reliability
            A.open_view(page, 'reliability')
            rel = page.evaluate("() => [...document.querySelectorAll('[data-reliability][data-set]')].map(e => [e.dataset.set, (e.querySelector('[data-set-days]') || {dataset: {}}).dataset.setDays])")
            rec.check('Reliability: the prospective record, and beside it its days with every input before the cutoff unless the sets are the same',
                      rel == ([['all', str(x.n)]] if x.m == 0 else [['all', str(x.n)], ['before_cutoff', str(x.k)]]), rel, **at)
            # ---- the whole page
            states = []
            for view in A.VIEWS:
                A.open_view(page, view)
                states += page.evaluate(JS_STATES)
                texts.append(page.evaluate(f"() => document.querySelector('[data-view-panel=\"{view}\"]').innerText"))
            states += page.evaluate(JS_STATES)
            rec.check('no failed or verification state on the page or in any view', not states, states, **at)
            words = sorted({m.group(0) for t in texts for m in BANNED.finditer(t)})
            rec.check('the page never says "late" or "timely"', not words, words, **at)
            lay = page.evaluate(A.JS_LAYOUT)
            rec.check('no horizontal page scroll', not lay['horizontal_page_scroll'], lay, **at)
            rec.check('no script error on the page', not errors, errors, **at)
            ctx.close()
    finally:
        served = server.take()
        rec.value['requests'][f'{build}-{engine}'] = {'blocked_non_local': blocked, 'route_saw': len(seen),
                                                     'not_found': sorted({s['path'] for s in served if s['status'] != 200})}
        rec.check('own-origin requests only: zero non-local requests (blocked and recorded)', not blocked, blocked, **where)
        rec.check('no failed request: every served path found', not any(s['status'] != 200 for s in served),
                  sorted({s['path'] for s in served if s['status'] != 200}), **where)
        browser.close()
        server.shutdown()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog='space_acceptance_d.py')
    ap.add_argument('--dist', action='append', required=True, help='name=<built Space>; repeat for each build')
    ap.add_argument('--scratch', type=Path, required=True)
    ap.add_argument('--engines', default='chromium,webkit')
    args = ap.parse_args(argv)
    from playwright.sync_api import sync_playwright
    args.scratch.mkdir(parents=True, exist_ok=True)
    rec = A.Record(args.scratch / 'acceptance-d.json')
    rec.value['schema'] = 'cp18d-space-acceptance-v1'
    builds = dict(item.split('=', 1) for item in args.dist)
    rec.value['builds'] = {}
    for name, dist in builds.items():
        dist = Path(dist).resolve()
        build = json.loads((dist / 'app/space-build.json').read_text())
        rec.value['builds'][name] = {'dist': str(dist), 'space_build_sha256': sha_file(dist / 'app/space-build.json'),
                                     'live_record_sha256': build['live']['sha256'], 'bundle_manifest_sha256': build['bundle']['manifest_sha256'],
                                     'input_classes': build['live']['input_classes']}
    rec.value['playwright'] = __import__('importlib.metadata').metadata.version('playwright')
    t0 = time.time()
    with sync_playwright() as p:
        for engine in args.engines.split(','):
            for name, dist in builds.items():
                print('==', name, engine, flush=True)
                A.guarded(rec, f'{name} {engine}', check_build, rec, p, engine, name, Path(dist).resolve(), args.scratch)
    rec.value['finished_utc'] = A.now()
    rec.value['browser_seconds'] = round(time.time() - t0, 1)
    checks = [c for c in rec.value['checks'] if c['pass'] is not None]
    rec.value['summary'] = {'passed': sum(c['pass'] for c in checks), 'failed': sum(not c['pass'] for c in checks),
                            'not_run': sum(c['pass'] is None for c in rec.value['checks'])}
    rec.save()
    print('summary', rec.value['summary'])
    return 0 if not rec.value['summary']['failed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
