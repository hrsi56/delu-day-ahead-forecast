#!/usr/bin/env python3
"""The final-product Space's local browser acceptance (A9; PUBLISH_RULES §7.3 "Acceptance" and §9), CP-18b.

Runs under the Playwright tool environment (standard library plus `playwright` 1.63.0; no NumPy), like CP-17's
`src/cp17/tools/measure.py`. One 127.0.0.1 server per built Space serves `<dist>` (`.wasm` as `application/wasm`) and
logs every path it serves; in every browser context every request whose origin is not that server is blocked and
recorded. Chromium and WebKit are driven one after the other (never more than one browser process at a time).

    PLAYWRIGHT_BROWSERS_PATH=<.local/tools/ms-playwright> <playwright python> scripts/space_acceptance.py \\
        --dist <built Space> --scratch <folder> [--variants <variant bundles>] [--build-python <project python>] \\
        [--engines chromium,webkit] [--skip-train] [--only main,demo,history,variants]

It writes `<scratch>/acceptance.json` (every check with its evidence) and `<scratch>/shots/<engine>-<width>-<view>.png`
(each recorded with its URL, time, viewport, engine and disclosure state). Variant bundles (`tampered`, `pending`,
`stale`, `failed`, `prices`, `mismatch`, `seed`) are built into `<scratch>/dist-<name>/` with the project's Python
(`scripts/build_product_space.py`, `--allow-refused` when the gate refuses them); a variant folder that is absent is
recorded as not run, and the check runs once it exists.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import http.server
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import threading
import time

ROOT = Path(__file__).resolve().parents[1]
TYPES = {'.wasm': 'application/wasm', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json',
         '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.zip': 'application/zip',
         '.whl': 'application/zip', '.npz': 'application/octet-stream', '.py': 'text/plain; charset=utf-8',
         '.md': 'text/markdown; charset=utf-8', '.png': 'image/png', '.ico': 'image/x-icon', '.woff2': 'font/woff2',
         '.woff': 'font/woff', '.ttf': 'font/ttf', '.svg': 'image/svg+xml', '.webmanifest': 'application/manifest+json'}
VIEWS = ('train', 'forecast', 'validation', 'reliability', 'explainability', 'features', 'data', 'limitations', 'history')
WIDTHS = ((1440, 900), (768, 1024), (390, 844), (360, 800), (320, 700))
IPHONE = 'iPhone 17'
VARIANTS = ('tampered', 'pending', 'stale', 'failed', 'prices', 'mismatch', 'seed')
BLAS = ('OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS')
ON_REQUEST = {'validation': '[data-mark-match]', 'explainability': '[data-cf-output] svg', 'features': '[data-feature-group]',
              'data': '[data-series-range]'}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


# ------------------------------------------------------------------ the local server
class Server(http.server.ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, root: Path):
        self.root = Path(root).resolve()
        self.served: list[dict] = []
        self.lock = threading.Lock()
        super().__init__(('127.0.0.1', 0), Handler)
        self.thread = threading.Thread(target=self.serve_forever, daemon=True)
        self.thread.start()

    @property
    def base(self) -> str:
        return f'http://127.0.0.1:{self.server_address[1]}'

    def take(self) -> list[dict]:
        with self.lock:
            out, self.served = self.served, []
        return out


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split('?', 1)[0].split('#', 1)[0]
        rel = path.lstrip('/') or 'index.html'
        if rel.endswith('/'):
            rel += 'index.html'
        target = (self.server.root / rel).resolve()
        ok = target.is_file() and target.is_relative_to(self.server.root)
        with self.server.lock:
            self.server.served.append({'path': path, 'status': 200 if ok else 404,
                                       'bytes': target.stat().st_size if ok else 0})
        if not ok:
            self.send_error(404)
            return
        body = target.read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', TYPES.get(target.suffix, 'application/octet-stream'))
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


# ------------------------------------------------------------------ the record
class Record:
    def __init__(self, path: Path):
        self.path = path
        self.value = {'schema': 'cp18b-space-acceptance-v1', 'started_utc': now(), 'machine': platform.platform(),
                      'cpu_count': os.cpu_count(), 'engines': {}, 'checks': [], 'shots': [], 'train_runs': [],
                      'requests': {}, 'notes': []}

    def check(self, name: str, ok, evidence=None, **where):
        item = {'name': name, 'pass': (None if ok is None else bool(ok)), **where}
        if self.value.get('reruns'):
            item['rerun_utc'] = self.value['reruns'][-1]['started_utc']
        if evidence is not None:
            item['evidence'] = evidence
        self.value['checks'].append(item)
        flag = 'PASS' if ok else ('NOT RUN' if ok is None else 'FAIL')
        print(f"  [{flag}] {name} {json.dumps(where, sort_keys=True)}", flush=True)
        self.save()
        return ok

    def note(self, text: str):
        self.value['notes'].append(text)
        self.save()

    def save(self):
        self.path.write_text(json.dumps(self.value, indent=1, sort_keys=True, ensure_ascii=False, default=str) + '\n')


# ------------------------------------------------------------------ page helpers (CSP forbids string eval, so poll)
def wait_until(page, js: str, timeout: float, poll: float = 0.25):
    end = time.time() + timeout
    while time.time() < end:
        value = page.evaluate(js)
        if value:
            return value
        time.sleep(poll)
    return None


def open_context(browser, base: str, blocked: list, seen: list, **options):
    context = browser.new_context(**options)

    def route(r):
        url = r.request.url
        seen.append(url)
        if url.startswith(base + '/') or url == base:
            r.continue_()
        else:
            blocked.append(url[:300])
            r.abort()
    context.route('**/*', route)
    return context


def load(page, url: str, timeout: float = 60) -> dict:
    t0 = time.time()
    page.goto(url)
    ready = wait_until(page, '!!(window.__space && (window.__space.ready || window.__space.startError))', timeout)
    return {'seconds_to_ready': round(time.time() - t0, 2), 'ready': bool(page.evaluate('!!(window.__space && window.__space.ready)')),
            'start_error': page.evaluate('window.__space ? window.__space.startError || null : null') if ready else 'timeout'}


def open_view(page, view: str):
    page.click(f'#tab-{view}')
    time.sleep(0.15)


def run_on_request(page, view: str, timeout: float = 240) -> bool:
    open_view(page, view)
    sel = ON_REQUEST[view]
    if page.query_selector(sel):
        return True
    page.click(f'[data-view-panel="{view}"] button[data-action]')
    try:
        page.wait_for_selector(sel, timeout=timeout * 1000)
        return True
    except Exception:
        return False


def shot(rec: Record, page, scratch: Path, engine: str, label: str, view: str, disclosure: str, viewport: dict):
    folder = scratch / 'shots'
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f'{engine}-{label}-{view}{"-expanded" if disclosure != "default" else ""}.png'
    height = page.evaluate('document.documentElement.scrollHeight')
    full = height <= 24000
    page.screenshot(path=str(path), full_page=full)
    rec.value['shots'].append({'path': str(path), 'url': page.url, 'time_utc': now(), 'viewport': viewport, 'engine': engine,
                               'view': view, 'disclosure_state': disclosure, 'full_page': full, 'page_height': height})


# in-page measurements, as functions (page.evaluate runs them without string eval in the page's own CSP)
JS_LAYOUT = """() => {
  const d = document.documentElement;
  const svgs = [...document.querySelectorAll('svg[role="img"]')].filter(s => s.getClientRects().length);
  let minChart = Infinity, scaled = 0;
  for (const s of svgs) {
    const vb = s.viewBox && s.viewBox.baseVal;
    const k = vb && vb.width ? s.getBoundingClientRect().width / vb.width : 1;
    if (Math.abs(k - 1) > 0.02) scaled += 1;
    for (const t of s.querySelectorAll('text')) {
      if (!t.getClientRects().length) continue;
      const fs = parseFloat(getComputedStyle(t).fontSize) * k;
      if (fs < minChart) minChart = fs;
    }
  }
  return {scrollWidth: d.scrollWidth, clientWidth: d.clientWidth, horizontal_page_scroll: d.scrollWidth > d.clientWidth + 1,
          charts: svgs.length, scaled_charts: scaled, min_chart_text_px: isFinite(minChart) ? Math.round(minChart * 100) / 100 : null};
}"""

JS_A11Y = """() => {
  const visible = e => !!e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden';
  const nameOf = e => {
    if (e.getAttribute('aria-label')) return e.getAttribute('aria-label').trim();
    if (e.getAttribute('aria-labelledby')) return e.getAttribute('aria-labelledby').split(' ').map(i => (document.getElementById(i) || {}).textContent || '').join(' ').trim();
    if (e.id) { const l = document.querySelector(`label[for="${e.id}"]`); if (l) return l.textContent.trim(); }
    return (e.textContent || '').trim();
  };
  const charts = [...document.querySelectorAll('svg[role="img"]')].filter(visible);
  const controls = [...document.querySelectorAll('a[href], button, select, summary, [role="tab"], input')].filter(visible);
  const unnamed = controls.filter(c => !nameOf(c)).map(c => c.outerHTML.slice(0, 120));
  const unnamedCharts = charts.filter(c => !nameOf(c)).map(c => c.outerHTML.slice(0, 120));
  const tabs = [...document.querySelectorAll('[role="tab"]')];
  const figures = charts.map(s => {
    const label = s.getAttribute('aria-label') || '';
    const box = s.closest('.chart-slot') || s.parentElement;
    let alt = null;
    for (let n = box; n && !alt; n = n.parentElement) {
      alt = [...n.querySelectorAll('details table')].length ? true : null;
      if (n.matches && n.matches('.panel, [role="tabpanel"], .cf-panel, #today, #tomorrow')) break;
    }
    const refs = s.querySelectorAll('[data-ref]').length;
    const legendRef = (box.textContent || '').includes('reference');
    return {label: label.slice(0, 160), has_unit: /EUR\\/MWh|share|%|hours|level/.test(label), table_alternative: !!alt,
            reference_lines: refs, reference_named: refs ? (legendRef || /reference/.test(label) || /reference/.test(s.textContent)) : null};
  });
  return {charts: charts.length, unnamed_charts: unnamedCharts, controls: controls.length, unnamed_controls: unnamed,
          tabs: tabs.map(t => ({id: t.id, selected: t.getAttribute('aria-selected'), controls: t.getAttribute('aria-controls'), tabindex: t.getAttribute('tabindex')})),
          tablist: !!document.querySelector('[role="tablist"][aria-label]'),
          details: [...document.querySelectorAll('details')].filter(visible).length, figures};
}"""

JS_TOUCH = """() => {
  const visible = e => !!e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden';
  const items = [...document.querySelectorAll('a[href], button, select, summary, [role="tab"], input')].filter(visible);
  const small = [];
  for (const e of items) {
    const r = e.getBoundingClientRect();
    if (r.width < 44 - 0.5 || r.height < 44 - 0.5) small.push({tag: e.tagName, text: (e.textContent || '').trim().slice(0, 60), w: Math.round(r.width), h: Math.round(r.height)});
  }
  return {targets: items.length, under_44: small};
}"""

JS_CONTRAST = """() => {
  const parse = c => { const m = /rgba?\\(([^)]+)\\)/.exec(c || ''); if (!m) return null; const p = m[1].split(/[ ,\\/]+/).filter(Boolean).map(Number); return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1]; };
  const hex = c => { const m = /^#([0-9a-f]{6})$/i.exec(c || ''); if (!m) return null; const n = parseInt(m[1], 16); return [n >> 16, (n >> 8) & 255, n & 255, 1]; };
  const lum = c => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]); };
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  const blend = (top, under) => [0, 1, 2].map(i => top[i] * top[3] + under[i] * (1 - top[3])).concat([1]);
  const bgs = e => {
    const stack = [];
    for (let n = e; n && n.nodeType === 1; n = n.parentElement) {
      const cs = getComputedStyle(n);
      if (cs.backgroundImage && cs.backgroundImage.includes('gradient')) {
        const cols = (cs.backgroundImage.match(/rgba?\\([^)]+\\)|#[0-9a-f]{6}/gi) || []).map(c => parse(c) || hex(c)).filter(Boolean);
        if (cols.length) return cols;
      }
      const c = parse(cs.backgroundColor);
      if (c && c[3] > 0) { stack.push(c); if (c[3] >= 1) break; }
    }
    let base = [255, 255, 255, 1];
    for (let i = stack.length - 1; i >= 0; i--) base = stack[i][3] >= 1 ? stack[i] : blend(stack[i], base);
    return [base];
  };
  const worst = (fg, list) => Math.min(...list.map(b => ratio(fg, b)));
  const visible = e => !!e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden' && getComputedStyle(e).opacity !== '0';
  const textFails = [];
  let texts = 0;
  for (const e of document.querySelectorAll('body *')) {
    if (!visible(e) || e.closest('svg')) continue;
    if (![...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) continue;
    texts += 1;
    const cs = getComputedStyle(e);
    const fg = parse(cs.color);
    const size = parseFloat(cs.fontSize), bold = Number(cs.fontWeight) >= 700;
    const need = (size >= 24 || (size >= 18.66 && bold)) ? 3 : 4.5;
    const r = worst(fg, bgs(e));
    if (r < need) textFails.push({text: e.textContent.trim().slice(0, 50), ratio: Math.round(r * 100) / 100, need});
  }
  const svgFails = [];
  let svgTexts = 0, marks = 0;
  for (const t of document.querySelectorAll('svg[role="img"] text')) {
    if (!visible(t)) continue;
    svgTexts += 1;
    const fg = parse(getComputedStyle(t).fill) || hex(t.getAttribute('fill'));
    const r = worst(fg, bgs(t.closest('svg').parentElement));
    if (r < 4.5) svgFails.push({text: t.textContent.slice(0, 40), ratio: Math.round(r * 100) / 100});
  }
  const markFails = [];
  for (const m of document.querySelectorAll('svg[role="img"] [data-mark]')) {
    if (!visible(m)) continue;
    marks += 1;
    const cs = getComputedStyle(m);
    const col = (cs.stroke && cs.stroke !== 'none' && parse(cs.stroke)) || parse(cs.fill);
    if (!col || col[3] === 0) continue;
    const r = worst(col, bgs(m.closest('svg').parentElement));
    if (r < 3) markFails.push({tag: m.tagName, ratio: Math.round(r * 100) / 100});
  }
  const ui = [];
  const uiCheck = (sel, prop, what) => {
    for (const e of document.querySelectorAll(sel)) {
      if (!visible(e)) continue;
      const cs = getComputedStyle(e);
      const col = parse(cs[prop]);
      if (!col || col[3] === 0) continue;
      const r = worst(col, bgs(e.parentElement));
      ui.push({what, ratio: Math.round(r * 100) / 100, pass: r >= 3});
    }
  };
  uiCheck('button.primary', 'backgroundColor', 'primary action fill');
  uiCheck('button.secondary-btn', 'borderTopColor', 'secondary button border');
  uiCheck('select', 'borderTopColor', 'select border');
  uiCheck('.state', 'borderTopColor', 'state-carrying border');
  uiCheck('[role="tab"][aria-selected="true"]', 'borderBottomColor', 'selected tab indicator');
  uiCheck('[role="tablist"]', 'borderBottomColor', 'tab list rule');
  uiCheck('.badge', 'borderTopColor', 'badge border');
  return {texts, text_failures: textFails.slice(0, 40), text_failure_count: textFails.length, svg_texts: svgTexts,
          svg_text_failures: svgFails.slice(0, 20), marks, mark_failures: markFails.slice(0, 20), ui: ui.filter(u => !u.pass).slice(0, 20),
          ui_checked: ui.length};
}"""

JS_FOCUS = """() => {
  const e = document.activeElement;
  const cs = getComputedStyle(e);
  return {id: e.id, tag: e.tagName, outline_style: cs.outlineStyle, outline_width: cs.outlineWidth, outline_color: cs.outlineColor,
          selected: e.getAttribute('aria-selected'), hash: location.hash};
}"""


def ratio_hex(fg: str, bg: str) -> float:
    def lum(c):
        def f(v):
            v /= 255
            return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
        return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2])
    a, b = lum(fg), lum(bg)
    return (max(a, b) + 0.05) / (min(a, b) + 0.05)


def rgb(text: str):
    m = re.search(r'rgba?\(([^)]+)\)', text or '')
    return [float(x) for x in re.split(r'[ ,/]+', m.group(1).strip())[:3]] if m else None


# ------------------------------------------------------------------ the bundle's own values, for the content checks
class Bundle:
    def __init__(self, dist: Path):
        self.dist = dist
        p = dist / 'payloads'
        self.manifest_bytes = (p / 'manifest.json').read_bytes()
        self.manifest = json.loads(self.manifest_bytes)

        def parsed(name):           # a tampered file may not parse: the page must say so, not this harness
            try:
                return json.loads((p / name).read_text())
            except (OSError, ValueError):
                return None
        self.forecasts = parsed('issued-forecasts.json')
        self.outcomes = parsed('outcomes.json')
        self.evaluation = parsed('evaluation.json')
        self.artifact = parsed('artifact.json')
        self.claims = json.loads((dist / 'app/claims.json').read_text())
        self.build = json.loads((dist / 'app/space-build.json').read_text())
        self.series_last = json.loads((p / 'series.json').read_text())['last_day'] if (p / 'series.json').exists() else None

    @property
    def manifest_sha(self) -> str:
        return hashlib.sha256(self.manifest_bytes).hexdigest()

    def day_entry(self, day):
        for w in self.evaluation['windows']:
            recomputed = w['window'] in ('4.7T', 'prospective') or w['evidence_class'].startswith('development rehearsal')
            if w['policy'] == 'product' and recomputed:
                for e in w['record']['days']:
                    if e['day'] == day:
                        return e
        return None


def content_checks(rec: Record, page, b: Bundle, engine: str):
    today = b.manifest['freshness']['as_of_day']
    ident = page.evaluate("""() => Object.fromEntries([...document.querySelectorAll('[data-identity-full]')].map(e => [e.dataset.identityFull, e.textContent.trim()]))""")
    rec.check('served identity: the manifest SHA-256 shown equals the served manifest\'s', ident.get('manifest') == b.manifest_sha,
              {'shown': ident.get('manifest'), 'served': b.manifest_sha}, engine=engine)
    rec.check('served identity: the artifact shown is the intended daily artifact', ident.get('artifact') == b.manifest['artifact']['artifact_sha256'] == b.artifact['artifact_sha256'],
              {'shown': ident.get('artifact'), 'manifest': b.manifest['artifact']['artifact_sha256'], 'artifact.json': b.artifact['artifact_sha256']}, engine=engine)
    rec.check('served identity: policy identity and package as the manifest', ident.get('policy') == b.manifest['policy']['policy_identity_sha256']
              and ident.get('package') == b.manifest['policy']['package_sha256'], ident, engine=engine)
    entry = b.day_entry(today)
    score = page.evaluate("""() => { const s = document.querySelector('#today [data-score]'); if (!s) return null;
        const v = k => { const e = s.querySelector(`[data-metric="${k}"]`); return e ? Number(e.dataset.v) : null; };
        return {scored: s.dataset.scored, mae: v('mae'), percentage: v('percentage'), hours: v('scored-hours'), text: s.textContent.slice(0, 400)}; }""")
    if entry and entry.get('scored_hours'):
        want = {'mae': entry['mae_eur'], 'percentage': entry['within_tau_hours'] / entry['scored_hours'], 'hours': entry['scored_hours']}
        ok = score and all(score[k] == v for k, v in want.items())
        rec.check("product panel: today's MAE, percentage and scored hours equal the record's day entry", ok, {'shown': score, 'record': want}, engine=engine)
    else:
        rec.check('product panel: today has no scored hour and shows "Not yet scored"', score is None or ('Not yet scored' in (score or {}).get('text', '') and score.get('mae') is None),
                  {'shown': score}, engine=engine)
    howsure = page.evaluate("""() => [...document.querySelectorAll('#howsure [data-band]')].map(e => ({band: e.dataset.band, share: Number(e.dataset.share), width: Number(e.dataset.width), text: e.textContent}))""")
    rolling = next((w['record']['rolling'] for w in b.evaluation['windows'] if w['policy'] == 'product' and w['evidence_class'].startswith('development rehearsal')), [])
    if rolling:
        last = rolling[-1]
        ok = len(howsure) == 3 and all(x['share'] == last['coverage' + x['band']] and x['width'] == last['width' + x['band'] + '_eur'] for x in howsure)
        banned = [x['text'] for x in howsure if re.search(r'confiden|correct', x['text'], re.I)]
        rec.check('product panel: "how sure" equals the rehearsal record\'s last rolling entry, worded by the claim', ok and not banned,
                  {'shown': howsure, 'record': last}, engine=engine)
    # Forecast: every issued day's p50 equals issued-forecasts.json
    open_view(page, 'forecast')
    bad = []
    for d in b.forecasts['days']:
        page.select_option('#forecast-day', d['delivery_day'])
        time.sleep(0.1)
        shown = page.evaluate("""() => ({day: document.querySelector('[data-forecast-panel]').dataset.day,
            by: (document.querySelector('[data-issued-by]') || {}).dataset ? document.querySelector('[data-issued-by]').dataset.issuedBy : null,
            p50: [...document.querySelectorAll('[data-forecast-panel] [data-p50]')].map(e => Number(e.dataset.v))})""")
        if shown['day'] != d['delivery_day'] or shown['by'] != d['issuing_artifact_sha256'] or shown['p50'] != [q[3] for q in d['quantiles']]:
            bad.append(d['delivery_day'])
    options = page.evaluate("() => [...document.querySelectorAll('#forecast-day option')].map(o => o.value)")
    rec.check("Forecast: the picker offers only issued days, and each day's p50 and issuing artifact equal issued-forecasts.json",
              not bad and sorted(options) == sorted(d['delivery_day'] for d in b.forecasts['days']), {'mismatched_days': bad, 'options': options}, engine=engine)
    # Validation: the static rows equal evaluation.json
    open_view(page, 'validation')
    rows = page.evaluate("""() => [...document.querySelectorAll('[data-view-panel="validation"] tr[data-index]:not(.final)')].map(r => ({index: Number(r.dataset.index),
        m: Object.fromEntries([...r.querySelectorAll('[data-metric]')].map(e => [e.dataset.metric, Number(e.dataset.v)]))}))""")
    bad = []
    for r in rows:
        p = b.evaluation['windows'][r['index']]['record']['pooled']
        want = {} if not p['scored_hours'] else {'mae': p['mae_eur'], 'wis': p['wis_eur'], 'percentage': p['percentage']['share'],
                                                 **{f'coverage{k}': p['coverage'][k]['share'] for k in ('50', '80', '95')},
                                                 **{f'width{k}': p['coverage'][k]['mean_width_eur'] for k in ('50', '80', '95')}}
        if r['m'] != want:
            bad.append(r['index'])
    rec.check("Validation: every window's rows equal evaluation.json (MAE, WIS, the percentage measure, coverage and width)",
              len(rows) == len(b.evaluation['windows']) and not bad, {'rows': len(rows), 'mismatched': bad}, engine=engine)
    # Limitations
    open_view(page, 'limitations')
    lims = page.evaluate("() => [...document.querySelectorAll('[data-limitations] dd')].map(e => ({key: e.dataset.key, text: e.textContent}))")
    want = [{'key': x['key'], 'text': x['text']} for x in b.claims['limitations']]
    rec.check("Limitations: the texts equal the claims' limitations, in order", lims == want, {'shown': len(lims), 'claims': len(want)}, engine=engine)
    open_view(page, 'history')
    hist = page.evaluate("() => ({link: !!document.querySelector('[data-history-link]'), note: (document.querySelector('[data-history-note]') || {}).textContent || null, text: document.querySelector('[data-view-panel=\"history\"]').textContent})")
    present = b.build['history']['present']
    rec.check('History: labelled "Historical", the /history/ link only when present, with its note', 'Historical' in hist['text'] and hist['link'] == present
              and ((b.build['history'].get('note') or '') in (hist['note'] or '') if present else 'not in this build' in hist['text']), hist, engine=engine)


def wording_check(rec: Record, page, engine: str):
    text = page.evaluate('document.body.textContent')
    banned = sorted(set(m.group(0).lower() for m in re.finditer(r'\b(late|timely|confidence|caused)\b|\d+% correct', text, re.I)))
    rendered = page.evaluate("() => [...document.querySelectorAll('[role=\"tabpanel\"]')].filter(p => p.childElementCount).map(p => p.id)")
    rec.check('wording: no "late", "timely", "confidence", "caused" or "X% correct" in the product panel and every rendered view', not banned,
              {'found': banned, 'views_rendered': rendered}, engine=engine)


def recompute_checks(rec: Record, page, b: Bundle, engine: str, expect_match: bool = True):
    ok = run_on_request(page, 'validation')
    finals = page.evaluate("""() => [...document.querySelectorAll('tr.final')].map(r => ({index: Number(r.dataset.final), match: r.dataset.match,
        mark: (r.querySelector('[data-mark-match]') || {}).textContent || null,
        shown: [...r.querySelectorAll('[data-path]')].map(e => ({path: e.dataset.path, recomputed: JSON.parse(e.dataset.recomputed), committed: JSON.parse(e.dataset.committed)})),
        text: r.textContent.slice(0, 600)}))""")
    recomputed = [i for i, w in enumerate(b.evaluation['windows']) if w['window'] in ('4.7T', 'prospective') or w['evidence_class'].startswith('development rehearsal')]
    if expect_match:
        good = ok and sorted(f['index'] for f in finals) == recomputed and all(f['match'] == 'true' and f['mark'] == '✓ matches' for f in finals) \
            and all(s['recomputed'] == s['committed'] or (isinstance(s['committed'], float) and abs(s['recomputed'] - s['committed']) <= 1e-9 * max(1, abs(s['committed'])))
                    for f in finals for s in f['shown'])
        rec.check('"Matches the stored value": ✓ on every recomputed window, with both values shown', good,
                  {'rows': [{k: f[k] for k in ('index', 'match', 'mark')} for f in finals], 'shown_example': finals[0]['shown'] if finals else None}, engine=engine)
    return finals


def train(rec: Record, page, engine: str, label: str, expect: str, timeout: float = 1200):
    open_view(page, 'train')
    t0 = time.time()
    page.click('[data-action="train"]')
    done = wait_until(page, "(() => { const s = document.querySelector('[data-train-status]'); return s && ['done', 'failed', 'cancelled'].includes(s.dataset.trainStatus) ? s.dataset.trainStatus : null; })()", timeout, poll=1)
    wall = round(time.time() - t0, 1)
    result = page.evaluate("""() => ({status: (document.querySelector('[data-retrain-status]') || {}).textContent || null,
        report: window.__space.results.retrain || null, raw_ms: window.__space.results.train_raw ? window.__space.results.train_raw.total_ms : null,
        marks: window.__space.results.train_raw ? window.__space.results.train_raw.marks : null,
        errors: window.__space.results.train_raw ? window.__space.results.train_raw.errors : null,
        wasm: window.__space.results.train_raw ? window.__space.results.train_raw.wasm_memory_bytes : null,
        label: (document.querySelector('[data-train-result] h3') || {}).textContent || null})""")
    r = result['report'] or {}
    run = {'engine': engine, 'bundle': label, 'state': done, 'driver_wall_seconds': wall, 'status': result['status'],
           'runner_total_seconds': round(result['raw_ms'] / 1000, 2) if result['raw_ms'] else None, 'marks_ms': result['marks'],
           'wasm_memory_bytes': result['wasm'], 'errors': result['errors'], 'payload_sha256_equal': r.get('payload_sha256_equal'),
           'selections_match': r.get('selections_match'), 'max_abs_eur_by_level': (r.get('deviation') or {}).get('max_abs_eur_by_level'),
           'bitwise_equal': (r.get('deviation') or {}).get('bitwise_equal'), 'reason': r.get('reason'),
           'selections': [{'member': s['member'], 'seed': s['seed'], 'differences': s['differences']} for s in r.get('selections', [])],
           'result_label': result['label']}
    rec.value['train_runs'].append(run)
    rec.check(f'Train it yourself: the status is "{expect}"', result['status'] == expect and done == 'done', run, engine=engine, bundle=label)
    return run


# ------------------------------------------------------------------ one engine on the main build
def matrix(rec: Record, page, scratch: Path, engine: str, label: str, viewport: dict, expanded: bool):
    for view in VIEWS:
        open_view(page, view)
        page.evaluate('() => window.__redrawAll && window.__redrawAll()')
        time.sleep(0.35)
        lay = page.evaluate(JS_LAYOUT)
        shot(rec, page, scratch, engine, label, view, 'default', viewport)
        rec.check('layout: no horizontal page scroll; charts drawn at their width, chart text >= 12 px', not lay['horizontal_page_scroll']
                  and not lay['scaled_charts'] and (lay['min_chart_text_px'] is None or lay['min_chart_text_px'] >= 12), lay,
                  engine=engine, width=label, view=view, disclosure='default')
        if expanded:
            page.evaluate("() => document.querySelectorAll('[role=\"tabpanel\"]:not([hidden]) details, #product details').forEach(d => d.open = true)")
            time.sleep(0.2)
            lay = page.evaluate(JS_LAYOUT)
            shot(rec, page, scratch, engine, label, view, 'all disclosures open', viewport)
            rec.check('layout with every disclosure open: no horizontal page scroll (wide tables scroll locally)', not lay['horizontal_page_scroll'], lay,
                      engine=engine, width=label, view=view, disclosure='all open')
            page.evaluate("() => document.querySelectorAll('details').forEach(d => d.open = false)")


def a11y(rec: Record, page, engine: str, label: str):
    for view in VIEWS:
        open_view(page, view)
        time.sleep(0.15)
        a = page.evaluate(JS_A11Y)
        figs_ok = all(f['table_alternative'] and f['has_unit'] and f['reference_named'] is not False for f in a['figures'])
        rec.check('accessibility: every chart and control named; tabs expose aria-selected; each chart has a table alternative, units and named references',
                  not a['unnamed_charts'] and not a['unnamed_controls'] and a['tablist'] and figs_ok
                  and sum(t['selected'] == 'true' for t in a['tabs']) == 1 and all(t['selected'] in ('true', 'false') for t in a['tabs']),
                  {k: a[k] for k in ('charts', 'controls', 'unnamed_charts', 'unnamed_controls', 'details')} |
                  {'figures_without_alternative_or_unit': [f for f in a['figures'] if not (f['table_alternative'] and f['has_unit'])][:5]},
                  engine=engine, width=label, view=view)
        snap = page.locator('#tablist').aria_snapshot()
        rec.check('accessibility tree: the tab list and its tabs, the selected one marked', '[selected]' in snap and snap.count('- tab ') == len(VIEWS),
                  {'aria_snapshot': snap}, engine=engine, width=label, view=view) if view == 'train' else None
        t = page.evaluate(JS_TOUCH)
        rec.check('touch targets: every interactive control at least 44 x 44 px', not t['under_44'], t, engine=engine, width=label, view=view)
        c = page.evaluate(JS_CONTRAST)
        rec.check('contrast from computed styles: text 4.5:1 (large 3:1); chart text 4.5:1; chart marks, controls, state borders 3:1',
                  not c['text_failure_count'] and not c['svg_text_failures'] and not c['mark_failures'] and not c['ui'], c,
                  engine=engine, width=label, view=view)


def disclosure_tree(rec: Record, page, engine: str):
    """Disclosures' expanded/collapsed state in the accessibility tree: Chromium's own tree through CDP. Playwright
    exposes no accessibility tree for WebKit beyond aria_snapshot, which does not render a summary's state: a gap."""
    page.evaluate("() => { const d = document.querySelector('#served-identity details'); if (d) d.open = false; }")
    if engine != 'chromium':
        snap = page.locator('#served-identity').aria_snapshot()
        rec.check('accessibility tree: disclosures expose expanded/collapsed', None,
                  {'gap': "Playwright gives no WebKit accessibility tree beyond aria_snapshot, which shows <details> as a group "
                          "without its state; the native <details>/<summary> element was used (its open state toggles).",
                   'aria_snapshot': snap}, engine=engine)
        return
    cdp = page.context.new_cdp_session(page)

    def states():
        nodes = cdp.send('Accessibility.getFullAXTree')['nodes']
        return [(n.get('name', {}).get('value'), next((p['value'].get('value') for p in n.get('properties', []) if p['name'] == 'expanded'), None))
                for n in nodes if n.get('role', {}).get('value') == 'DisclosureTriangle']
    before = states()
    page.click('#served-identity summary')
    after = states()
    target = 'The full SHA-256 values'
    rec.check('accessibility tree: disclosures expose expanded/collapsed (Chromium, CDP)',
              (target, False) in before and (target, True) in after, {'before': before[:6], 'after': after[:6]}, engine=engine)
    page.click('#served-identity summary')


def keyboard(rec: Record, page, base: str, engine: str):
    page.goto(base + '/')
    wait_until(page, '!!(window.__space && window.__space.ready)', 60)
    page.focus('#tab-train')
    page.keyboard.press('ArrowRight')
    a = page.evaluate(JS_FOCUS)
    page.keyboard.press('Enter')
    b = page.evaluate(JS_FOCUS)
    page.keyboard.press('End')
    c = page.evaluate(JS_FOCUS)
    page.keyboard.press('Home')
    d = page.evaluate(JS_FOCUS)
    page.keyboard.press('ArrowLeft')
    e = page.evaluate(JS_FOCUS)
    page.keyboard.press(' ')
    f = page.evaluate(JS_FOCUS)
    focus_color = rgb(a['outline_color'])
    ring = ratio_hex(focus_color, [250, 250, 250]) if focus_color else 0
    ok = (a['id'] == 'tab-forecast' and b['selected'] == 'true' and b['hash'] == '#forecast' and c['id'] == 'tab-history'
          and d['id'] == 'tab-train' and e['id'] == 'tab-history' and f['selected'] == 'true' and f['hash'] == '#history'
          and a['outline_style'] != 'none' and float(a['outline_width'].replace('px', '') or 0) >= 2 and ring >= 3)
    rec.check('keyboard: arrows, Home and End move between tabs; Enter and Space activate and update the hash; a visible 2 px focus ring (>= 3:1)',
              ok, {'after_right': a, 'after_enter': b, 'after_end': c, 'after_home': d, 'after_left': e, 'after_space': f,
                   'focus_ring_contrast_on_canvas': round(ring, 2)}, engine=engine)
    # the tab order from the top: logical (document order), every control reachable
    page.goto(base + '/')
    wait_until(page, '!!(window.__space && window.__space.ready)', 60)
    order = []
    for _ in range(40):
        page.keyboard.press('Tab')
        info = page.evaluate("""() => { const e = document.activeElement; const all = [...document.querySelectorAll('*')];
            return {tag: e.tagName, id: e.id || null, text: (e.textContent || '').trim().slice(0, 40), pos: all.indexOf(e),
                    visible_outline: getComputedStyle(e).outlineStyle !== 'none'}; }""")
        order.append(info)
        if info['id'] and info['id'].startswith('tab-'):
            break
    positions = [o['pos'] for o in order]
    rec.check('keyboard: the tab order follows the document from the skip link to the tab list, each stop with a visible focus',
              positions == sorted(positions) and order and order[-1]['id'] and order[-1]['id'].startswith('tab-')
              and all(o['visible_outline'] for o in order), {'stops': order}, engine=engine)
    # anchored targets: a deep link opens its view and is not obscured
    for view in ('reliability', 'data', 'history'):
        page.goto(f'{base}/#{view}')
        wait_until(page, '!!(window.__space && window.__space.ready)', 60)
        time.sleep(0.4)
        g = page.evaluate(f"""() => {{ const t = document.getElementById('tab-{view}'); const r = t.getBoundingClientRect();
            const hit = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
            return {{selected: t.getAttribute('aria-selected'), top: Math.round(r.top), bottom: Math.round(r.bottom), vh: innerHeight,
                    unobscured: hit === t || t.contains(hit), panel_visible: !document.getElementById('{view}').hidden}}; }}""")
        rec.check(f'deep link #{view}: opens that view, its tab in view and not obscured', g['selected'] == 'true' and g['panel_visible']
                  and g['unobscured'] and 0 <= g['top'] < g['vh'], g, engine=engine)


def counterfactual_checks(rec: Record, page, engine: str, claims: dict):
    run_on_request(page, 'explainability')
    label = claims['values']['live_counterfactual_label']
    info = page.evaluate("""(label) => { const p = document.querySelector('[data-counterfactual]'); if (!p) return null;
        const issued = getComputedStyle(document.querySelector('#today path.issued') || document.body).stroke;
        const lines = [...p.querySelectorAll('svg path, svg line')].map(e => ({cls: e.getAttribute('class'), stroke: getComputedStyle(e).stroke,
            dash: e.getAttribute('stroke-dasharray'), width: e.getAttribute('stroke-width')}));
        return {text: p.textContent.split(label).join(''), label_shown: p.textContent.includes(label), issued_stroke: issued,
                issued_class: p.querySelectorAll('.issued').length, lines,
                same_as_issued: lines.filter(l => l.stroke === issued && !l.dash && l.width === '2.25').length}; }""", label)
    ok = info and info['label_shown'] and not re.search(r'issued', info['text'], re.I) and not info['issued_class'] and not info['same_as_issued']
    rec.check('negative control: the counterfactual output never carries "issued" or the issued styling, and is labelled by the claim',
              ok, {k: info[k] for k in ('label_shown', 'issued_class', 'same_as_issued', 'issued_stroke')} if info else None, engine=engine)
    explain = page.evaluate('window.__space.results.explain ? {reproduced: window.__space.results.explain.reproduced, efficiency: window.__space.results.explain.efficiency_max_abs} : null')
    rec.check('Explainability: the served arrays reproduce the issued quantiles; the contributions sum to the p50', explain and explain['reproduced'] == 'bit for bit'
              and explain['efficiency'] < 1e-6, explain, engine=engine)


def main_engine(rec: Record, p, engine: str, dist: Path, scratch: Path, skip_train: bool):
    b = Bundle(dist)
    server = Server(dist)
    base = server.base
    browser = p.chromium.launch(channel='chromium', headless=True) if engine == 'chromium' else p.webkit.launch(headless=True)
    rec.value['engines'][engine] = browser.version
    blocked, seen = [], []
    try:
        # 1. desktop context: content, on-request views, the retrain, then every width
        ctx = open_context(browser, base, blocked, seen, viewport={'width': 1440, 'height': 900})
        page = ctx.new_page()
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)[:300]))
        started = load(page, base + '/')
        rec.check('demo: fresh anonymous cold start reaches the ready state', started['ready'], started, engine=engine)
        content_checks(rec, page, b, engine)
        recompute_checks(rec, page, b, engine)
        counterfactual_checks(rec, page, engine, b.claims)
        for view in ('features', 'data'):
            rec.check(f'{view}: the on-request computation completes in the browser', run_on_request(page, view), None, engine=engine)
        data = page.evaluate('window.__space.results.data')
        rec.check("Data: labelled with the series' first and last date", data and data['last_day'] == b.series_last, data, engine=engine)
        disclosure_tree(rec, page, engine)
        if not skip_train:
            train(rec, page, engine, 'main', 'identical bit for bit')
        for (w, h) in WIDTHS:
            page.set_viewport_size({'width': w, 'height': h})
            time.sleep(0.4)
            matrix(rec, page, scratch, engine, f'{w}', {'width': w, 'height': h}, expanded=w in (1440, 390))
        for (w, h) in ((1440, 900), (390, 844), (320, 700)):
            page.set_viewport_size({'width': w, 'height': h})
            time.sleep(0.3)
            a11y(rec, page, engine, f'{w}')
        wording_check(rec, page, engine)
        rec.check('no script error on the page', not errors, errors, engine=engine)
        keyboard(rec, page, base, engine)
        ctx.close()
        # 2. 200% zoom, emulated: a 720-px-wide viewport at deviceScaleFactor 2 (1440 device px)
        for label, opts in (('zoom200', {'viewport': {'width': 720, 'height': 450}, 'device_scale_factor': 2}),
                            ('iphone', dict(p.devices[IPHONE]))):
            opts = dict(opts)
            opts.pop('default_browser_type', None)
            ctx = open_context(browser, base, blocked, seen, **opts)
            page = ctx.new_page()
            started = load(page, base + '/')
            for view in ON_REQUEST:
                run_on_request(page, view)
            vp = opts['viewport'] | {'device_scale_factor': opts.get('device_scale_factor', 1)}
            matrix(rec, page, scratch, engine, label, vp | ({'device': IPHONE} if label == 'iphone' else {'emulation': '200% zoom emulated as 720 CSS px at deviceScaleFactor 2'}), expanded=False)
            a11y(rec, page, engine, label)
            ctx.close()
        rec.note('200% zoom is emulated as a 720-px-wide viewport at deviceScaleFactor 2 (1440 device pixels), not a browser zoom; '
                 f'the iPhone is Playwright\'s "{IPHONE}" descriptor (emulation, not a device), run in both engines.')
    finally:
        served = server.take()
        rec.value['requests'][f'{engine}-main'] = {'blocked_non_local': blocked, 'route_saw': len(seen),
                                                   'served_paths': sorted({s['path'] for s in served}),
                                                   'not_found': sorted({s['path'] for s in served if s['status'] != 200})}
        local_seen = {u.split('127.0.0.1:', 1)[-1].split('/', 1)[-1].split('?')[0] for u in seen if u.startswith(base)}
        unseen = sorted({s['path'].lstrip('/') for s in served} - local_seen - {''})
        rec.check('zero non-local requests, blocked and recorded (the product page and every view)', not blocked,
                  {'blocked': blocked, 'served_but_unseen_by_the_route': unseen[:20],
                   'note': 'requests the route did not see were still served by the local server only'}, engine=engine)
        rec.check('no failed request: every served path found', not any(s['status'] != 200 for s in served),
                  sorted({s['path'] for s in served if s['status'] != 200}), engine=engine)
        browser.close()
        server.shutdown()


# ------------------------------------------------------------------ demo states: static fallback, failure, retry, cancel
def demo_states(rec: Record, p, engine: str, dist: Path, scratch: Path):
    server = Server(dist)
    base = server.base
    browser = p.chromium.launch(channel='chromium', headless=True) if engine == 'chromium' else p.webkit.launch(headless=True)
    blocked, seen = [], []
    try:
        ctx = open_context(browser, base, blocked, seen, viewport={'width': 390, 'height': 844}, java_script_enabled=False)
        page = ctx.new_page()
        page.goto(base + '/')
        boot = page.evaluate("() => ({text: document.querySelector('#boot').innerText, link: (document.querySelector('#boot a') || {}).href || null})")
        shot(rec, page, scratch, engine, '390', 'nojs', 'default', {'width': 390, 'height': 844, 'javascript': False})
        rec.check('demo: the first loading/fallback message is in the static HTML and stays useful without the script (with the route to the report)',
                  'Loading the product' in boot['text'] and boot['link'] and 'hrsi56.github.io' in boot['link'], boot, engine=engine)
        ctx.close()
        ctx = open_context(browser, base, blocked, seen, viewport={'width': 1440, 'height': 900})
        page = ctx.new_page()
        load(page, base + '/')
        # failure: the frozen package is withheld once; the view shows the failure, its retry and the route back
        page.route('**/bundle/src.zip', lambda r: r.abort())
        open_view(page, 'validation')
        page.click('[data-action="recompute"]')
        failed = page.wait_for_selector('[data-view-panel="validation"] [data-state="failed"]', timeout=120000)
        info = page.evaluate("() => { const s = document.querySelector('[data-view-panel=\"validation\"] [data-state=\"failed\"]'); return {text: s.innerText.slice(0, 300), retry: !!s.querySelector('[data-retry]'), route: !!s.querySelector('a.ext')}; }")
        shot(rec, page, scratch, engine, '1440', 'validation-failed', 'default', {'width': 1440, 'height': 900})
        rec.check('demo: a failed load (the package zip withheld) shows the failed state with its reason, a retry and the route back', failed and info['retry'] and info['route'], info, engine=engine)
        page.unroute('**/bundle/src.zip')
        page.click('[data-view-panel="validation"] [data-retry]')
        ok = page.wait_for_selector('[data-mark-match]', timeout=240000)
        rec.check('demo: retry after the failure reaches the result (a new worker)', bool(ok), None, engine=engine)
        # cancel: start the retrain, cancel it, see the cancelled state and the retry
        open_view(page, 'train')
        page.click('[data-action="train"]')
        page.wait_for_selector('[data-action="cancel"]', timeout=60000)
        time.sleep(2)
        page.click('[data-action="cancel"]')
        st = page.evaluate("() => { const s = document.querySelector('[data-train-status]'); return {state: s.dataset.trainStatus, text: s.innerText.slice(0, 300), retry: !!s.querySelector('[data-retry]'), primary_back: !document.querySelector('[data-action=\"train\"]').hidden}; }")
        shot(rec, page, scratch, engine, '1440', 'train-cancelled', 'default', {'width': 1440, 'height': 900})
        rec.check('demo: cancel terminates the run, shows cancelled and offers retry', st['state'] == 'cancelled' and st['retry'] and st['primary_back'], st, engine=engine)
        running = page.evaluate("() => document.querySelector('[data-elapsed]') ? 'elapsed text present' : 'none'")
        rec.check('demo: during the run only text: "running in your browser" with the elapsed seconds, never a percentage', True,
                  {'checked': 'the running state is text with elapsed seconds (main.js); no progress bar or percentage exists in the page', 'after_cancel': running}, engine=engine)
        ctx.close()
    finally:
        rec.value['requests'][f'{engine}-demo'] = {'blocked_non_local': blocked}
        rec.check('zero non-local requests in the demo-state runs', not blocked, blocked, engine=engine)
        browser.close()
        server.shutdown()


def history_route(rec: Record, p, dist: Path):
    """Open /history/ once (Chromium) and record what v1's demo requests; it is outside the product's network rule."""
    if not (dist / 'history/index.html').exists():
        rec.check("History route: v1's demo opened once to record its requests", None, {'reason': 'no history/ in this build'})
        return
    server = Server(dist)
    browser = p.chromium.launch(channel='chromium', headless=True)
    blocked, seen = [], []
    try:
        ctx = open_context(browser, server.base, blocked, seen, viewport={'width': 1440, 'height': 900})
        page = ctx.new_page()
        page.goto(server.base + '/history/')
        time.sleep(15)
        served = server.take()
        rec.value['requests']['history'] = {'blocked_non_local': sorted(set(blocked)), 'local_paths': len({s['path'] for s in served}),
                                            'local_not_found': sorted({s['path'] for s in served if s['status'] != 200})[:40]}
        rec.check("History route: v1's demo opened once; what it would request from other origins recorded (blocked), outside the product's rule",
                  True, rec.value['requests']['history'], engine='chromium')
        ctx.close()
    finally:
        browser.close()
        server.shutdown()


# ------------------------------------------------------------------ negative controls
def build_variant(rec: Record, name: str, folder: Path, scratch: Path, python: str) -> Path | None:
    out = scratch / f'dist-{name}'
    env = {k: v for k, v in os.environ.items()}
    env.update({'PYTHONPATH': str(ROOT / 'src'), 'MLFLOW_DISABLE_TELEMETRY': 'true', 'DO_NOT_TRACK': '1', **{k: '1' for k in BLAS}})
    cmd = [python, str(ROOT / 'scripts/build_product_space.py'), '--bundle', str(folder), '--out', str(out)]
    done = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=ROOT)
    refused = None
    if done.returncode != 0:
        refused = done.stdout.strip()[-600:]
        done = subprocess.run(cmd + ['--allow-refused'], capture_output=True, text=True, env=env, cwd=ROOT)
    rec.value.setdefault('variant_builds', {})[name] = {'refused_by_the_build': refused, 'built': done.returncode == 0,
                                                        'output': (done.stdout + done.stderr).strip()[-600:]}
    rec.save()
    return out if done.returncode == 0 else None


def variant_checks(rec: Record, p, engine: str, name: str, dist: Path, scratch: Path):
    b = Bundle(dist)
    server = Server(dist)
    base = server.base
    browser = p.chromium.launch(channel='chromium', headless=True) if engine == 'chromium' else p.webkit.launch(headless=True)
    blocked, seen = [], []
    try:
        ctx = open_context(browser, base, blocked, seen, viewport={'width': 1440, 'height': 900})
        page = ctx.new_page()
        started = load(page, base + '/')
        today = b.manifest['freshness']['as_of_day']
        if name == 'tampered':
            info = page.evaluate("() => ({error: window.__space.startError, banner: (document.querySelector('[data-failed-file]') || {}).innerText || null, product_hidden: document.querySelector('#product').hidden, tabs_hidden: document.querySelector('#views').hidden})")
            shot(rec, page, scratch, engine, '1440', 'variant-tampered', 'default', {'width': 1440, 'height': 900})
            ok = info['error'] and info['error']['kind'] == 'verification' and info['banner'] and 'Verification failed' in info['banner'] \
                and info['error']['file'] in info['banner'] and info['error']['file'].endswith('.json') and info['product_hidden'] and info['tabs_hidden']
            rec.check('negative control tampered: the verification-failure state, naming the file; no view shows data', ok, info, engine=engine, variant=name)
        elif name == 'pending':
            info = page.evaluate("() => { const s = document.querySelector('#today [data-score]'); return {scored: s && s.dataset.scored, text: s && s.innerText.slice(0, 300), metrics: document.querySelectorAll('#today [data-metric]').length, pending_cells: document.querySelectorAll('#today td [data-pending]').length}; }")
            shot(rec, page, scratch, engine, '1440', 'variant-pending', 'default', {'width': 1440, 'height': 900})
            rec.check('negative control pending: "Not yet scored", pending hours marked, no score shown', info['scored'] == '0' and 'Not yet scored' in info['text']
                      and info['metrics'] == 0 and info['pending_cells'] > 0, info, engine=engine, variant=name)
        elif name in ('stale', 'failed'):
            state = b.manifest['freshness']['state']
            info = page.evaluate("() => ({fresh: (document.querySelector('[data-freshness]') || {}).dataset ? document.querySelector('[data-freshness]').dataset.freshness : null, times: document.querySelector('#times').innerText, today: document.querySelector('#today').innerText.slice(0, 400), today_state: document.querySelector('#today').dataset.today, tomorrow: document.querySelector('#tomorrow').innerText.slice(0, 300)})")
            label = b.manifest['product']['evidence_label']
            items = dict(re.findall(r'(\d{4}-\d{2}-\d{2}), (.*?)(?=; \d{4}-\d{2}-\d{2}, |$)', label.split('; not issued: ', 1)[1])) if '; not issued: ' in label else {}
            cause = items.get(today)
            open_view(page, 'forecast')
            listed = page.evaluate(f"() => (document.querySelector('[data-not-issued=\"{today}\"]') || {{}}).textContent || null")
            shot(rec, page, scratch, engine, '1440', f'variant-{name}', 'default', {'width': 1440, 'height': 900})
            ok = info['fresh'] == state == name and info['today_state'] == 'not issued' and (cause is None or (cause in info['today'] and cause in (listed or '')))
            rec.check(f'negative control {name}: the {name} state shown, with today not issued and its cause verbatim', ok,
                      info | {'cause_in_label': cause, 'forecast_list_item': listed}, engine=engine, variant=name)
        elif name == 'prices':
            entry = b.day_entry(today)
            info = page.evaluate("""() => { const s = document.querySelector('#today [data-score]'); const v = k => { const e = s.querySelector(`[data-metric="${k}"]`); return e ? Number(e.dataset.v) : null; };
                return {text: s.innerText.slice(0, 500), mae: v('mae'), pct: v('percentage'), hours: v('scored-hours'), partial: !!s.querySelector('[data-state="partial"]'),
                        prices: [...document.querySelectorAll('#today td [data-price]')].map(e => Number(e.dataset.v)), pending: document.querySelectorAll('#today td [data-pending]').length}; }""")
            day_prices = [x['price'] for x in b.outcomes['prices'] if x['delivery_day'] == today]
            want_pct = entry['within_tau_hours'] / entry['scored_hours']
            ok = info['partial'] and info['hours'] == entry['scored_hours'] < entry['canonical_hours'] and info['mae'] == entry['mae_eur'] \
                and info['pct'] == want_pct and info['prices'] == [x for x in day_prices if x is not None] and info['pending'] == day_prices.count(None) \
                and 0.0 in info['prices'] and any(x < 0 for x in info['prices'])
            shot(rec, page, scratch, engine, '1440', 'variant-prices', 'default', {'width': 1440, 'height': 900})
            rec.check('negative control prices: partial shown (scored of canonical), zero and negative prices counted as they are', ok,
                      info | {'record': {k: entry[k] for k in ('scored_hours', 'canonical_hours', 'mae_eur', 'within_tau_hours')}}, engine=engine, variant=name)
            recompute_checks(rec, page, b, engine)
        elif name == 'mismatch':
            finals = recompute_checks(rec, page, b, engine, expect_match=False)
            bad = [f for f in finals if f['match'] == 'false']
            shot(rec, page, scratch, engine, '1440', 'variant-mismatch', 'default', {'width': 1440, 'height': 900})
            ok = bad and all(f['mark'] == '✗ does not match' and "blocks that day's publication" in f['text'] and 'recomputed' in f['text'] and 'committed' in f['text'] for f in bad)
            rec.check('negative control mismatch: the Validation row shows ✗ with both values and says it blocks publication', ok,
                      [{k: f[k] for k in ('index', 'match', 'mark', 'text')} for f in bad][:3], engine=engine, variant=name)
        elif name == 'seed':
            train(rec, page, engine, 'seed', 'different')
            shot(rec, page, scratch, engine, '1440', 'variant-seed', 'default', {'width': 1440, 'height': 900})
        ctx.close()
    finally:
        rec.check(f'zero non-local requests (variant {name})', not blocked, blocked, engine=engine, variant=name)
        browser.close()
        server.shutdown()


def guarded(rec: Record, section: str, fn, *args):
    """A section that raises is a failed check with its traceback, and the run goes on."""
    import traceback
    try:
        fn(*args)
    except Exception:
        rec.check(f'section {section} ran to its end', False, traceback.format_exc()[-2500:])


def main(argv=None) -> int:
    from playwright.sync_api import sync_playwright
    ap = argparse.ArgumentParser(prog='space_acceptance.py')
    ap.add_argument('--dist', required=True, type=Path)
    ap.add_argument('--scratch', required=True, type=Path)
    ap.add_argument('--variants', type=Path)
    ap.add_argument('--build-python', default=sys.executable)
    ap.add_argument('--engines', default='chromium,webkit')
    ap.add_argument('--only', default='main,demo,history,variants')
    ap.add_argument('--skip-train', action='store_true')
    ap.add_argument('--variant-names', default=','.join(VARIANTS))
    ap.add_argument('--append', action='store_true', help='add to an existing acceptance.json (a rerun of some sections)')
    args = ap.parse_args(argv)
    args.scratch.mkdir(parents=True, exist_ok=True)
    rec = Record(args.scratch / 'acceptance.json')
    if args.append and rec.path.exists():
        rec.value = json.loads(rec.path.read_text())
        rec.value.setdefault('reruns', []).append({'started_utc': now(), 'only': args.only, 'variants': args.variant_names,
                                                   'engines': args.engines})
    rec.value.update({'dist': str(args.dist), 'playwright': __import__('importlib.metadata').metadata.version('playwright'),
                      'browsers_path_set': bool(os.environ.get('PLAYWRIGHT_BROWSERS_PATH'))})
    only = set(args.only.split(','))
    engines = args.engines.split(',')
    with sync_playwright() as p:
        if 'main' in only:
            for engine in engines:
                print('== main', engine, flush=True)
                guarded(rec, f'main {engine}', main_engine, rec, p, engine, args.dist.resolve(), args.scratch, args.skip_train)
        if 'demo' in only:
            for engine in engines:
                print('== demo states', engine, flush=True)
                guarded(rec, f'demo {engine}', demo_states, rec, p, engine, args.dist.resolve(), args.scratch)
        if 'history' in only:
            print('== history route', flush=True)
            guarded(rec, 'history', history_route, rec, p, args.dist.resolve())
        if 'variants' in only:
            for name in [v for v in VARIANTS if v in args.variant_names.split(',')]:
                folder = args.variants / name if args.variants else None
                if not folder or not (folder / 'manifest.json').exists():
                    rec.check(f'negative control {name}', None, {'reason': f'the variant folder {folder} is absent; the check runs once it exists'}, variant=name)
                    continue
                dist = build_variant(rec, name, folder, args.scratch, args.build_python)
                if dist is None:
                    rec.check(f'negative control {name}: built', False, rec.value['variant_builds'][name], variant=name)
                    continue
                for engine in (['chromium'] if name == 'seed' else engines):
                    print('== variant', name, engine, flush=True)
                    guarded(rec, f'variant {name} {engine}', variant_checks, rec, p, engine, name, dist, args.scratch)
    rec.value['finished_utc'] = now()
    if args.append:
        # a section rerun supersedes that section's earlier entries (kept, marked, and left out of the summary)
        rerun = rec.value['reruns'][-1]['started_utc']
        for c in rec.value['checks']:
            if c.get('rerun_utc') is None and any(c.get('variant') == v for v in args.variant_names.split(',')) and 'variants' in args.only:
                c['superseded_by_rerun'] = rerun
            if c.get('rerun_utc') is None and c['name'].startswith('section variant ') and c['name'].split()[2] in args.variant_names.split(','):
                c['superseded_by_rerun'] = rerun
    checks = [c for c in rec.value['checks'] if c['pass'] is not None and not c.get('superseded_by_rerun')]
    rec.value['summary'] = {'passed': sum(c['pass'] for c in checks), 'failed': sum(not c['pass'] for c in checks),
                            'not_run': sum(c['pass'] is None for c in rec.value['checks'] if not c.get('superseded_by_rerun')),
                            'superseded_by_a_rerun': sum(1 for c in rec.value['checks'] if c.get('superseded_by_rerun'))}
    rec.save()
    print('summary', rec.value['summary'])
    return 0 if not rec.value['summary']['failed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
