#!/usr/bin/env python3
"""Drive the public reader routes in a real browser and record what happened (plan §11.3).

HTTP 200 is not a reader route. The demo is a WebAssembly notebook that downloads a Python
runtime before it can forecast anything, so "the page answered" says nothing about whether a
visitor ever sees a forecast. This script opens each route in a **fresh browser context** -- an
empty cache, no cookies, no sign-in -- and records the time to a visible forecast, whether the
two controls change the view, and every console error and failed request on the way.

It needs Playwright, which is deliberately **not** a project dependency: it lives in a separate
tool environment under `.local/tools/`, and this script never runs in CI.

    .local/tools/playwright/bin/python scripts/check_reader_paths.py demo \\
        --engine chrome --engine webkit --viewport 1440x900 --viewport 390x844 \\
        --out reports/presentation/release-checks/<date>-demo.json

`screens` takes full-page screenshots with layout measurements; `charts` photographs every chart
at each width, closed and with every disclosure open, and measures text overlap, clipping and the
smallest rendered text; `route` follows the preview into v1's interactive replay on phones and
records where the page's landmarks fall.

`--engine chrome` drives the installed Google Chrome through Playwright's `channel="chrome"`;
`--engine webkit` drives Playwright's WebKit build, which is the Safari engine but not Safari.
Neither substitutes for a check on a real iPhone, which the record keeps separate.
"""

from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

APP_URL = "https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/"
SPACE_URL = "https://huggingface.co/spaces/Yarden-Viktor/delu-day-ahead-forecast"

#: What "a visible forecast" means on the demo: the identity panel has run and the fan chart
#: has drawn its axis. Both are computed in the browser; neither is in the static HTML.
READY_TEXT = "Maximum absolute deviation"
CHART_TEXT = "EUR/MWh"


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _launch(playwright, engine: str):
    if engine == "chrome":
        return playwright.chromium.launch(channel="chrome", headless=True)
    if engine == "webkit":
        return playwright.webkit.launch(headless=True)
    raise SystemExit(f"unknown engine {engine!r}")


#: The Space's startup state (plan §7.11), or null on a build without the states.
STATE_JS = "() => { const box = document.getElementById('delu-status'); return box ? box.dataset.state : null; }"


def probe_states(playwright, engine: str, url: str, timeout_s: float) -> dict:
    """Force the Space's failure paths and the retry, on a phone viewport (plan §11.3, Demo row)."""
    browser = _launch(playwright, engine)
    record: dict = {"engine": engine, "browser_version": browser.version, "url": url, "viewport": "390x844",
                    "started_utc": _utc()}
    visible = ("() => [...document.querySelectorAll('#delu-status [data-show]')]"
               ".filter(e => e.offsetParent !== null).map(e => e.textContent.trim().slice(0, 60))")

    # 1. A file the app needs fails to load: the failure state appears at once.
    context = browser.new_context(viewport={"width": 390, "height": 844})
    page = context.new_page()
    page.route("**/assets/index-*.js", lambda route: route.abort())
    page.goto(url, wait_until="domcontentloaded")
    page.wait_for_function(f"({STATE_JS})() === 'failure'", timeout=30_000)
    record["asset_failure"] = {
        "state": page.evaluate(STATE_JS), "visible": page.evaluate(visible),
        "report_link": page.get_attribute("#delu-status a", "href"),
    }
    # 2. Retry, with the file available again: the page reloads and the demo starts.
    page.unroute("**/assets/index-*.js")
    page.click("#delu-retry")
    page.wait_for_load_state("domcontentloaded")
    record["retry"] = {"state_after_reload": page.evaluate(STATE_JS)}
    try:
        page.get_by_text(READY_TEXT).first.wait_for(timeout=timeout_s * 1000)
        page.wait_for_function(f"({STATE_JS})() === 'ready'", timeout=5000)
        record["retry"]["reached_ready"] = True
        record["retry"]["visible"] = page.evaluate(visible)
    except Exception as exc:  # the failure is the finding
        record["retry"]["reached_ready"] = False
        record["retry"]["error"] = f"{type(exc).__name__}: {str(exc)[:200]}"
    context.close()

    # 3. The runtime cannot load and marimo reports it: the failure state follows the report at once.
    context = browser.new_context(viewport={"width": 390, "height": 844})
    page = context.new_page()
    page.route("https://cdn.jsdelivr.net/**", lambda route: route.abort())
    start = time.monotonic()
    page.goto(url, wait_until="domcontentloaded")
    page.wait_for_function(f"({STATE_JS})() === 'failure'", timeout=60_000)
    record["runtime_reports_failure"] = {"state": page.evaluate(STATE_JS),
                                         "seconds_to_failure_state": round(time.monotonic() - start, 1),
                                         "visible": page.evaluate(visible)}
    context.close()

    # 4. The runtime hangs with no error (its CDN never answers): only the deadline, not a timer
    #    shown as progress, moves the page to the failure state.
    context = browser.new_context(viewport={"width": 390, "height": 844})
    page = context.new_page()
    page.clock.install()
    page.route("https://cdn.jsdelivr.net/**", lambda route: None)  # never answered
    page.goto(url, wait_until="domcontentloaded")
    before = page.evaluate(STATE_JS)
    page.clock.run_for(60_000)
    at_one_minute = page.evaluate(STATE_JS)
    page.clock.run_for(185_000)
    record["runtime_hangs"] = {"state_at_start": before, "state_at_1_min": at_one_minute,
                               "state_after_deadline": page.evaluate(STATE_JS),
                               "visible": page.evaluate(visible)}
    context.close()
    browser.close()
    return record


def probe_demo(playwright, engine: str, width: int, height: int, url: str, timeout_s: float) -> dict:
    browser = _launch(playwright, engine)
    context = browser.new_context(viewport={"width": width, "height": height})
    page = context.new_page()
    console_errors: list[str] = []
    failed: list[str] = []
    requests = {"count": 0}
    page.on("console", lambda m: console_errors.append(m.text[:300]) if m.type == "error" else None)
    page.on("requestfailed", lambda r: failed.append(f"{r.url[:160]} {r.failure}"))
    page.on("request", lambda r: requests.__setitem__("count", requests["count"] + 1))

    record: dict = {
        "engine": engine,
        "browser_version": browser.version,
        "viewport": f"{width}x{height}",
        "url": url,
        "cache": "fresh browser context: empty cache, no cookies",
        "started_utc": _utc(),
    }
    start = time.monotonic()
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=timeout_s * 1000)
        record["first_static_text"] = page.inner_text("body")[:160]
        record["startup_state_at_first_paint"] = page.evaluate(STATE_JS)
        page.get_by_text(READY_TEXT).first.wait_for(timeout=timeout_s * 1000)
        # the demo draws a desktop and a phone chart and shows one; wait for the visible one
        page.get_by_text(CHART_TEXT).filter(visible=True).first.wait_for(timeout=timeout_s * 1000)
        record["seconds_to_visible_forecast"] = round(time.monotonic() - start, 1)
        record["ready"] = True
        if record["startup_state_at_first_paint"] is not None:
            page.wait_for_function(f"({STATE_JS})() === 'ready'", timeout=5000)
            record["startup_state_when_ready"] = "ready"
    except Exception as exc:  # the failure is the finding, so keep it
        record["ready"] = False
        record["seconds_waited"] = round(time.monotonic() - start, 1)
        record["error"] = f"{type(exc).__name__}: {str(exc)[:300]}"
        record["body_text_at_failure"] = page.inner_text("body")[:400] if not page.is_closed() else None

    if record.get("ready"):
        # Level control: 80 % -> 95 %. The marimo radio is a button with role=radio in a
        # shadow root; Playwright's role locators pierce open shadow roots.
        radio = page.get_by_role("radio", name="95 %")
        before = page.inner_text("body")
        radio.click()
        page.wait_for_timeout(3000)
        record["level_change_to_95"] = {
            "aria_checked": radio.get_attribute("aria-checked"),
            "view_changed": page.inner_text("body") != before,
        }
        # Scenario control: one keyboard step on the slider.
        slider = page.get_by_role("slider").first
        value_before = slider.get_attribute("aria-valuenow")
        before = page.inner_text("body")
        slider.focus()
        page.keyboard.press("ArrowRight")
        page.wait_for_timeout(4000)
        record["scenario_change"] = {
            "from": value_before,
            "to": slider.get_attribute("aria-valuenow"),
            "view_changed": page.inner_text("body") != before,
        }
        record["horizontal_overflow"] = page.evaluate(
            "document.documentElement.scrollWidth > document.documentElement.clientWidth"
        )
    record["requests"] = requests["count"]
    record["failed_requests"] = failed[:20]
    record["console_errors"] = console_errors[:20]
    context.close()
    browser.close()
    return record


MEASURE_JS = """
() => {
  const doc = document.documentElement;
  const texts = [...document.querySelectorAll('.chart svg text, svg#chart text')].filter(t => {
    const svg = t.closest('svg'); const box = t.getBoundingClientRect();
    return svg && getComputedStyle(svg).display !== 'none' && box.width > 0 && box.height > 0;
  });
  let smallest = null, where = null;
  for (const t of texts) {
    const svg = t.closest('svg');
    const scale = svg.getBoundingClientRect().width / svg.viewBox.baseVal.width;
    const size = parseFloat(t.getAttribute('font-size') || '13') * scale;
    if (smallest === null || size < smallest) {
      smallest = size; where = svg.id === 'chart' ? 'v1-replay' : svg.dataset.chart + ':' + svg.dataset.variant; }
  }
  const overflow = [...document.querySelectorAll('body *')].filter(e => {
    const r = e.getBoundingClientRect(); return r.right > doc.clientWidth + 1 && !e.closest('.scroll, pre');
  }).slice(0, 5).map(e => e.tagName + (e.className && e.className.baseVal === undefined ? '.' + e.className : ''));
  return {scrollWidth: doc.scrollWidth, clientWidth: doc.clientWidth,
          horizontal_overflow: doc.scrollWidth > doc.clientWidth,
          chart_texts_measured: texts.length, smallest_chart_text_px: smallest && Math.round(smallest * 100) / 100,
          smallest_at: where, overflowing_elements: overflow};
}
"""


def screens(playwright, pages: list[str], widths: list[int], out: Path, open_all: bool) -> list[dict]:
    """Full-page screenshots at each width, with layout measurements (plan §11.3)."""
    browser = _launch(playwright, "chrome")
    results = []
    for target in pages:
        url = target if "://" in target else Path(target).resolve().as_uri()
        stem = Path(target).stem
        for width in widths:
            context = browser.new_context(viewport={"width": width, "height": 900})
            page = context.new_page()
            page.goto(url, wait_until="load")
            if open_all:
                page.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
            page.wait_for_timeout(300)
            measure = page.evaluate(MEASURE_JS)
            shot = out / f"{stem}-{width}.png"
            page.screenshot(path=str(shot), full_page=True)
            results.append({"page": target, "width": width, "screenshot": str(shot), **measure})
            print(f"{stem} @ {width}: overflow={measure['horizontal_overflow']} "
                  f"smallest chart text={measure['smallest_chart_text_px']} px ({measure['smallest_at']})")
            context.close()
    browser.close()
    return results


CHART_JS = """
(root) => {
  const out = {texts: 0, smallest_text_px: null, overlaps: [], clipped: []};
  const svgs = root.tagName.toLowerCase() === 'svg' ? [root] : [...root.querySelectorAll('svg')];
  for (const svg of svgs.filter(s => s.getBoundingClientRect().width > 0 && getComputedStyle(s).display !== 'none')) {
    const sb = svg.getBoundingClientRect();
    const vb = svg.viewBox.baseVal && svg.viewBox.baseVal.width ? svg.viewBox.baseVal.width : sb.width;
    const boxes = [...svg.querySelectorAll('text')].filter(t => t.textContent.trim()).map(t => {
      const b = t.getBoundingClientRect();
      return {t: t.textContent.trim().slice(0, 40), x0: b.left, x1: b.right, y0: b.top, y1: b.bottom,
              px: parseFloat(t.getAttribute('font-size') || '13') * sb.width / vb};
    });
    out.texts += boxes.length;
    for (const b of boxes) {
      out.smallest_text_px = out.smallest_text_px === null ? b.px : Math.min(out.smallest_text_px, b.px);
      if (b.x0 < sb.left - 1 || b.x1 > sb.right + 1 || b.y0 < sb.top - 1 || b.y1 > sb.bottom + 1) out.clipped.push(b.t);
    }
    for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
      const a = boxes[i], c = boxes[j];
      const ox = Math.min(a.x1, c.x1) - Math.max(a.x0, c.x0), oy = Math.min(a.y1, c.y1) - Math.max(a.y0, c.y0);
      if (ox > 1.5 && oy > 2.5) out.overlaps.push([a.t, c.t]);
    }
  }
  if (out.smallest_text_px !== null) out.smallest_text_px = Math.round(out.smallest_text_px * 100) / 100;
  return out;
}
"""

PHONES = ((390, 844), (360, 780), (320, 640))

#: Text contrast from computed styles: each visible element with its own text, against the first
#: opaque background up its ancestors (WCAG relative luminance). SVG text is read against white.
CONTRAST_JS = r"""
() => {
  const rgb = c => c.match(/[\d.]+/g).slice(0, 4).map(Number);
  const lum = c => { const v = rgb(c).slice(0, 3).map(x => x / 255)
      .map(x => x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4));
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]; };
  const opaque = c => { const v = rgb(c); return v.length < 4 || v[3] > 0.5; };
  const background = el => { for (let e = el; e; e = e.parentElement) {
      const c = getComputedStyle(e).backgroundColor; if (c && opaque(c)) return c; } return 'rgb(255, 255, 255)'; };
  const hex = h => 'rgb(' + [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16)).join(', ') + ')';
  const out = {checked: 0, below: []};
  for (const el of document.querySelectorAll('body *')) {
    if (![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) continue;
    const r = el.getBoundingClientRect(); if (!r.width || !r.height) continue;
    const s = getComputedStyle(el); if (s.visibility === 'hidden' || Number(s.opacity) === 0) continue;
    const inSvg = !!el.closest('svg'), fill = el.getAttribute('fill');
    const fg = inSvg && fill && fill.startsWith('#') ? hex(fill) : s.color;
    const back = inSvg ? 'rgb(255, 255, 255)' : background(el);
    const a = lum(fg), b = lum(back), ratio = (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
    const size = parseFloat(s.fontSize), large = size >= 24 || (Number(s.fontWeight) >= 700 && size >= 18.66);
    const need = large ? 3 : 4.5;
    out.checked++;
    if (ratio + 1e-9 < need) out.below.push([el.tagName, el.textContent.trim().slice(0, 40), Math.round(ratio * 100) / 100, need]);
  }
  out.below_count = out.below.length; out.below = out.below.slice(0, 25);
  return out;
}
"""

#: Non-text contrast (§7.12, §11.3): every visible chart shape, blended over the white panel with its
#: opacity, needs 3:1 on its fill or its stroke. Exempt: the decorative grid and border colours (the
#: D1 token record calls them decorative) and hidden rings under the marks (aria-hidden).
NONTEXT_JS = r"""
() => {
  const rgb = c => (c.match(/[\d.]+/g) || []).map(Number);
  const lum = v => { const s = v.slice(0, 3).map(x => x / 255)
      .map(x => x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4));
    return 0.2126 * s[0] + 0.7152 * s[1] + 0.0722 * s[2]; };
  const over = (v, a) => v.slice(0, 3).map(x => a * x + (1 - a) * 255);
  const ratio = v => { const a = lum(v), b = 1; return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05); };
  const decorative = new Set(['228,228,231', '255,255,255']);
  const out = {checked: 0, below: []};
  for (const el of document.querySelectorAll('.chart svg *, svg#chart *')) {
    if (!['rect', 'circle', 'polygon', 'polyline', 'line', 'path'].includes(el.tagName)) continue;
    if (el.closest('[aria-hidden="true"]')) continue;
    const r = el.getBoundingClientRect(); if (!r.width && !r.height) continue;
    const s = getComputedStyle(el); if (s.display === 'none' || s.visibility === 'hidden') continue;
    if (el.closest('svg') && getComputedStyle(el.closest('svg')).display === 'none') continue;
    const opacity = Number(s.opacity);
    const best = [];
    for (const [paint, alpha] of [[s.fill, Number(s.fillOpacity)], [s.stroke, Number(s.strokeOpacity)]]) {
      if (!paint || paint === 'none') continue;
      const v = rgb(paint); if (v.length < 3) continue;
      const a = (v.length > 3 ? v[3] : 1) * alpha * opacity;
      if (paint === s.stroke && parseFloat(s.strokeWidth) <= 0) continue;
      best.push([v.slice(0, 3).map(Math.round).join(','), ratio(over(v, a))]);
    }
    if (!best.length || best.every(([key]) => decorative.has(key))) continue;
    const top = Math.max(...best.filter(([key]) => !decorative.has(key)).map(([, q]) => q));
    out.checked++;
    if (top + 1e-9 < 3) out.below.push([el.tagName, (el.closest('[data-chart]') || el.closest('svg')).getAttribute('data-chart') || 'chart',
                                        Math.round(top * 100) / 100]);
  }
  out.below_count = out.below.length; out.below = out.below.slice(0, 25);
  return out;
}
"""

#: Touch targets on a phone: interactive elements outside running text should be about 44 px (plan
#: §11.3); a link inside a sentence is exempt (WCAG 2.5.8's inline exception); 24 px is the floor.
TARGETS_JS = r"""
() => {
  const out = {checked: 0, under_44: [], under_24: []};
  const inSentence = el => el.tagName === 'A' && getComputedStyle(el).display === 'inline' && el.parentElement
      && el.parentElement.textContent.trim().length > el.textContent.trim().length + 3;
  for (const el of document.querySelectorAll('a[href], button, summary, input, [tabindex="0"]')) {
    const r = el.getBoundingClientRect(); if (!r.width || !r.height) continue;
    if (getComputedStyle(el).visibility === 'hidden' || inSentence(el)) continue;
    let w = r.width, h = r.height;
    const label = el.tagName === 'INPUT' && el.closest('label');
    if (label) { const l = label.getBoundingClientRect(); w = Math.max(w, l.width); h = Math.max(h, l.height); }
    out.checked++;
    const item = [el.tagName, (el.textContent || el.getAttribute('aria-label') || el.type || '').trim().replace(/\s+/g, ' ').slice(0, 32),
                  Math.round(w), Math.round(h)];
    if (w < 24 || h < 24) out.under_24.push(item); else if (w < 44 || h < 44) out.under_44.push(item);
  }
  out.under_44_count = out.under_44.length; out.under_24_count = out.under_24.length;
  out.under_44 = out.under_44.slice(0, 30); out.under_24 = out.under_24.slice(0, 30);
  return out;
}
"""

FOCUS_JS = r"""
() => { const el = document.activeElement; if (!el || el === document.body) return null;
  const s = getComputedStyle(el), r = el.getBoundingClientRect();
  const ring = (s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) > 0) || (s.boxShadow && s.boxShadow !== 'none');
  const all = [...document.querySelectorAll('a[href], button, summary, input, [tabindex]')];
  return {tag: el.tagName, text: (el.textContent || el.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' ').slice(0, 40),
          visible_focus: ring, index: all.indexOf(el)}; }
"""


def a11y(playwright, engine: str, target: str) -> dict:
    """The plan §11.3 report checklist, measured: zoom and reflow, contrast, keyboard and touch."""
    browser = _launch(playwright, engine)
    url = Path(target).resolve().as_uri()
    record: dict = {"engine": engine, "browser_version": browser.version, "page": target}

    def overflow(page) -> int:
        return page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")

    zoom = {}
    for label, width, height in (("1440 at 200%", 720, 450), ("1280 at 200%", 640, 400), ("320 reflow", 320, 640)):
        page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=2)
        page.goto(url, wait_until="load")
        closed = overflow(page)
        page.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
        page.wait_for_timeout(300)
        zoom[label] = {"css_viewport": f"{width}x{height}", "overflow_px_closed": closed,
                       "overflow_px_open": overflow(page)}
        page.close()
    record["zoom_and_reflow"] = zoom

    contrast = {}
    for width, height in ((1440, 900), (390, 844)):
        page = browser.new_page(viewport={"width": width, "height": height})
        page.goto(url, wait_until="load")
        page.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
        page.wait_for_timeout(300)
        contrast[str(width)] = page.evaluate(CONTRAST_JS)
        contrast[str(width)]["non_text"] = page.evaluate(NONTEXT_JS)
        if width == 390:
            record["touch_targets_390"] = page.evaluate(TARGETS_JS)
        page.close()
    record["contrast"] = contrast

    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto(url, wait_until="load")
    # WebKit, like Safari's default, moves Tab between form controls only; Option+Tab reaches links.
    key = "Alt+Tab" if engine == "webkit" else "Tab"
    stops = []
    for _ in range(1000):  # every stop, until focus leaves the page or comes back to the first one
        page.keyboard.press(key)
        stop = page.evaluate(FOCUS_JS)
        if stop is None or (stops and stop["index"] == stops[0]["index"]):
            break
        stops.append(stop)
    indices = [stop["index"] for stop in stops if stop]
    ident = page.locator("details:not([open]) > summary").first.evaluate("s => s.parentElement.id")
    page.locator(f"#{ident} > summary").focus()
    page.keyboard.press("Enter")
    page.wait_for_timeout(150)
    toggled = page.evaluate(f"document.getElementById('{ident}').open")
    page.goto(url + "#forecast", wait_until="load")
    page.wait_for_timeout(400)
    record["keyboard"] = {
        "tab_key": key,
        "first_stop": stops[0]["text"] if stops[0] else None,
        "stops_checked": len(indices),
        "in_document_order": indices == sorted(indices),
        "without_visible_focus": [stop["text"] for stop in stops if stop and not stop["visible_focus"]],
        "summary_toggles_on_enter": toggled,
        "anchor_into_closed_disclosure_opens_it": page.evaluate("document.getElementById('v1-archive').open"),
    }
    page.close()
    browser.close()
    return record


def charts(playwright, target: str, out: Path) -> dict:
    """Every chart at 1,440/390/360/320 px, closed and with every disclosure open (the Owner's D1 review)."""
    browser = _launch(playwright, "chrome")
    url = Path(target).resolve().as_uri()
    results: dict = {}
    for width, height, scale in ((1440, 900, 1), (390, 844, 2), (360, 780, 2), (320, 640, 2)):
        context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=scale)
        page = context.new_page()
        page.goto(url, wait_until="load")
        page.add_style_tag(content=".site-header{position:static !important}")  # keep it off the crops
        for state in ("closed", "open"):
            if state == "open":
                page.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
                page.wait_for_timeout(500)
            targets = [("preview", page.locator(".preview.panel").first)]
            targets += [(h.get_attribute("data-chart-id"), h) for h in page.locator("div.chart[data-chart-id]").all()]
            targets += [("v1-replay", page.locator("svg#chart")), ("v1-replay-controls", page.locator("#v1-archive .controls"))]
            for name, locator in targets:
                if not locator.is_visible():
                    continue
                shot = out / str(width) / state / f"{name}.png"
                shot.parent.mkdir(parents=True, exist_ok=True)
                locator.scroll_into_view_if_needed()
                locator.screenshot(path=str(shot))
                results[f"{width}/{state}/{name}"] = {"screenshot": str(shot), **locator.evaluate(CHART_JS)}
            figures = page.locator("#v1-archive figure img").all()
            if state == "open" and figures:
                results[f"{width}/open/v1-figures"] = [
                    round(f.bounding_box()["width"] / f.evaluate("i => i.naturalWidth"), 3) for f in figures]
        results[f"{width}/overflow_px"] = page.evaluate(
            "document.documentElement.scrollWidth - document.documentElement.clientWidth")
        if width in (1440, 390):
            page.locator("#v1-archive figure img").first.click()
            page.wait_for_timeout(300)
            page.screenshot(path=str(out / str(width) / "figure-view.png"))
            opened = page.evaluate("[document.getElementById('figure-view').open,"
                                   " Math.round(document.getElementById('figure-full').getBoundingClientRect().width),"
                                   " document.activeElement.id]")
            page.keyboard.press("Escape")
            page.wait_for_timeout(150)
            results[f"{width}/figure_view"] = {"open": opened[0], "image_width_px": opened[1], "focus": opened[2],
                                               "closed_by_escape": not page.evaluate(
                                                   "document.getElementById('figure-view').open"),
                                               "focus_after": page.evaluate("document.activeElement.tagName")}
        context.close()
    browser.close()
    return results


LANDMARKS_JS = """() => { const y = s => { const e = document.querySelector(s);
    return e ? Math.round(e.getBoundingClientRect().top + scrollY) : null; };
  return {preview: y('.preview.panel'), research_takeaway: y('.opening-summary'), journey: y('#journey'),
          comparison: y('#research-results'), v3: y('#v3'), v2: y('#v2'), v1: y('#v1'), evidence: y('#evidence'),
          page_height: document.documentElement.scrollHeight}; }"""

REPLAY_JS = """() => { const svg = document.getElementById('chart'), box = svg.getBoundingClientRect();
  const sizes = [...svg.querySelectorAll('text')].map(t => parseFloat(t.getAttribute('font-size')) * box.width / svg.viewBox.baseVal.width);
  return {archive_open: document.getElementById('v1-archive').open, hash: location.hash,
          chart_width_px: Math.round(box.width), viewbox_width: svg.viewBox.baseVal.width,
          smallest_text_px: Math.round(Math.min(...sizes) * 100) / 100}; }"""


def route(playwright, target: str, out: Path) -> dict:
    """The preview-to-replay route on phones, the archive's own Results link, and landmark positions."""
    browser = _launch(playwright, "chrome")
    url = Path(target).resolve().as_uri()
    results: dict = {}
    for width, height in PHONES + ((1440, 900),):
        page = browser.new_page(viewport={"width": width, "height": height})
        page.goto(url, wait_until="load")
        page.wait_for_timeout(300)
        marks = page.evaluate(LANDMARKS_JS)
        marks["screens_to_preview"] = round(marks["preview"] / height, 2)
        marks["screens_to_comparison"] = round(marks["comparison"] / height, 2)
        entry = {"viewport": f"{width}x{height}", "landmarks": marks}
        if (width, height) in PHONES:
            page.get_by_role("link", name="Explore this forecast").click()
            page.wait_for_timeout(600)
            entry["replay"] = page.evaluate(REPLAY_JS)
            page.screenshot(path=str(out / f"route-{width}.png"))
            page.locator('#v1-archive a[href="#results"]').first.click()
            page.wait_for_timeout(300)
            entry["archive_results_link_stays_in_v1"] = page.evaluate(
                "!!document.getElementById('results').closest('#v1-archive')")
            page.locator("input[name='lvl'][value='95']").check()
            page.locator("#scale").fill("6")
            page.wait_for_timeout(200)
            entry["replay"]["coverage_at_95"] = page.evaluate("document.getElementById('cov').textContent.trim()")
            entry["replay"]["scenario_caveat_shown"] = page.evaluate(
                "getComputedStyle(document.getElementById('scenario')).display !== 'none'")
        results[entry["viewport"]] = entry
        page.close()
    browser.close()
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    demo = sub.add_parser("demo", help="cold-start the in-browser demo and exercise both controls")
    demo.add_argument("--engine", action="append", choices=["chrome", "webkit"], required=True)
    demo.add_argument("--viewport", action="append", default=None, help="WIDTHxHEIGHT; repeatable")
    demo.add_argument("--url", default=APP_URL)
    demo.add_argument("--timeout", type=float, default=180.0)
    demo.add_argument("--out", type=Path, required=True)
    shots = sub.add_parser("screens", help="full-page screenshots and layout measurements of local pages")
    shots.add_argument("pages", nargs="+")
    shots.add_argument("--width", action="append", type=int, default=None)
    shots.add_argument("--open-all", action="store_true", help="open every disclosure first")
    shots.add_argument("--out", type=Path, required=True)
    shots.add_argument("--record", type=Path, default=None)
    checklist = sub.add_parser("a11y", help="the plan §11.3 report checklist: zoom, contrast, keyboard, touch")
    checklist.add_argument("page")
    checklist.add_argument("--engine", action="append", choices=["chrome", "webkit"], required=True)
    checklist.add_argument("--record", type=Path, required=True)
    states = sub.add_parser("states", help="force the Space's failure paths and the retry")
    states.add_argument("--engine", action="append", choices=["chrome", "webkit"], required=True)
    states.add_argument("--url", default=APP_URL)
    states.add_argument("--timeout", type=float, default=180.0)
    states.add_argument("--out", type=Path, required=True)
    for name, text in (("charts", "photograph and measure every chart at four widths"),
                       ("route", "follow the preview into v1's replay on phones; record landmarks")):
        sub_parser = sub.add_parser(name, help=text)
        sub_parser.add_argument("page")
        sub_parser.add_argument("--out", type=Path, required=True)
        sub_parser.add_argument("--record", type=Path, required=True)
    args = parser.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise SystemExit(
            "Playwright is not installed here. It lives in a tool environment under "
            ".local/tools/, never in the project; see this script's docstring."
        )

    if args.command == "a11y":
        with sync_playwright() as playwright:
            runs = [a11y(playwright, engine, args.page) for engine in args.engine]
        args.record.parent.mkdir(parents=True, exist_ok=True)
        args.record.write_text(json.dumps({"check": "report checklist (plan §11.3)", "checked_at_utc": _utc(),
                                           "host": f"{platform.machine()} / {platform.system()} {platform.release()}",
                                           "runs": runs}, indent=2, sort_keys=True) + "\n")
        print(json.dumps(runs, indent=1)[:6000])
        return 0

    if args.command == "states":
        with sync_playwright() as playwright:
            runs = [probe_states(playwright, engine, args.url, args.timeout) for engine in args.engine]
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps({"check": "Space startup states (plan §7.11, §11.3)", "checked_at_utc": _utc(),
                                        "host": f"{platform.machine()} / {platform.system()} {platform.release()}",
                                        "runs": runs}, indent=2, sort_keys=True) + "\n")
        ok = all(run["asset_failure"]["state"] == "failure" and run["retry"].get("reached_ready")
                 and run["runtime_reports_failure"]["state"] == "failure"
                 and run["runtime_hangs"]["state_at_1_min"] == "loading"
                 and run["runtime_hangs"]["state_after_deadline"] == "failure" for run in runs)
        print(json.dumps(runs, indent=1)[:3000])
        return 0 if ok else 1

    if args.command in ("charts", "route"):
        args.out.mkdir(parents=True, exist_ok=True)
        with sync_playwright() as playwright:
            results = (charts if args.command == "charts" else route)(playwright, args.page, args.out)
        args.record.parent.mkdir(parents=True, exist_ok=True)
        args.record.write_text(json.dumps({"checked_at_utc": _utc(), "results": results}, indent=2) + "\n")
        problems = [key for key, value in results.items() if isinstance(value, dict)
                    and (value.get("overlaps") or value.get("clipped")
                         or (value.get("smallest_text_px") or 99) < 12)]
        problems += [key for key, value in results.items() if key.endswith("overflow_px") and value]
        print("\n".join(problems) or "no overlap, clipping, text under 12 px or horizontal overflow")
        return 1 if problems else 0

    if args.command == "screens":
        args.out.mkdir(parents=True, exist_ok=True)
        with sync_playwright() as playwright:
            results = screens(playwright, args.pages, args.width or [1440, 768, 390, 360], args.out, args.open_all)
        if args.record:
            args.record.parent.mkdir(parents=True, exist_ok=True)
            args.record.write_text(json.dumps({"checked_at_utc": _utc(), "results": results}, indent=2) + "\n")
        return 0

    viewports = [tuple(int(v) for v in spec.split("x")) for spec in (args.viewport or ["1440x900"])]
    runs = []
    with sync_playwright() as playwright:
        for engine in args.engine:
            for width, height in viewports:
                result = probe_demo(playwright, engine, width, height, args.url, args.timeout)
                runs.append(result)
                print(
                    f"{engine:7s} {width}x{height}: ready={result.get('ready')} "
                    f"t={result.get('seconds_to_visible_forecast', result.get('seconds_waited'))}s "
                    f"console_errors={len(result['console_errors'])} failed={len(result['failed_requests'])}"
                )
    record = {
        "check": "demo cold start and controls (plan §11.3, Phase 0)",
        "checked_at_utc": _utc(),
        "host": f"{platform.machine()} / {platform.system()} {platform.release()}",
        "client": "Playwright, fresh browser context per run; unauthenticated",
        "runs": runs,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    print(f"wrote {args.out}")
    return 0 if all(run.get("ready") for run in runs) else 1


if __name__ == "__main__":
    sys.exit(main())
