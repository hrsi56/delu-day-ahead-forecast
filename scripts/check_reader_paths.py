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


def _shown(path: Path) -> str:
    """A path for a committed record: from `.local/` on, never the machine's home directory."""
    parts = Path(path).resolve().parts
    return str(Path(*parts[parts.index(".local"):])) if ".local" in parts else str(path)


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _url(target: str) -> str:
    """A local file becomes a file: URI; an http(s) address is used as given, so the same checks run against a
    local server or the public site (PUBLISH_RULES 1.0 A6). Browser-made requests such as a favicon happen over
    HTTP only, so a release record states which of the two it saw."""
    return target if "://" in target else Path(target).resolve().as_uri()


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
  const texts = [...document.querySelectorAll('.chart svg text, svg#chart text, svg#p-chart text')].filter(t => {
    const svg = t.closest('svg'); const box = t.getBoundingClientRect();
    return svg && getComputedStyle(svg).display !== 'none' && box.width > 0 && box.height > 0;
  });
  let smallest = null, where = null;
  for (const t of texts) {
    const svg = t.closest('svg');
    const m = t.getScreenCTM();  // the size a reader sees, border and viewBox scale included
    const scale = m ? Math.hypot(m.a, m.b) : svg.getBoundingClientRect().width / svg.viewBox.baseVal.width;
    const size = parseFloat(t.getAttribute('font-size') || '13') * scale;
    if (smallest === null || size < smallest) {
      smallest = size; where = svg.id === 'chart' ? 'v1-replay' : svg.id === 'p-chart' ? 'product-replay' : svg.dataset.chart + ':' + svg.dataset.variant; }
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
      const b = t.getBoundingClientRect(), m = t.getScreenCTM();
      // the size a reader sees: the text's own screen transform includes the viewBox scale and the chart's border
      const scale = m ? Math.hypot(m.a, m.b) : sb.width / vb;
      return {t: t.textContent.trim().slice(0, 40), x0: b.left, x1: b.right, y0: b.top, y1: b.bottom,
              px: parseFloat(t.getAttribute('font-size') || '13') * scale};
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
  for (const el of document.querySelectorAll('.chart svg *, svg#chart *, svg#p-chart *')) {
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
    url = _url(target)
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
    url = _url(target)
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
            targets += [("v1-replay", page.locator("svg#chart")), ("v1-replay-controls", page.locator("#v1-archive .controls")),
                        ("product-replay", page.locator("svg#p-chart")), ("product-replay-controls", page.locator(".replay-controls"))]
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
  const sizes = [...svg.querySelectorAll('text')].map(t => { const m = t.getScreenCTM();
    return parseFloat(t.getAttribute('font-size')) * (m ? Math.hypot(m.a, m.b) : box.width / svg.viewBox.baseVal.width); });
  return {archive_open: document.getElementById('v1-archive').open, hash: location.hash,
          chart_width_px: Math.round(box.width), viewbox_width: svg.viewBox.baseVal.width,
          smallest_text_px: Math.round(Math.min(...sizes) * 100) / 100}; }"""


PRODUCT_REPLAY_JS = """() => { const svg = document.getElementById('p-chart'), box = svg.getBoundingClientRect();
  const sizes = [...svg.querySelectorAll('g.plot text')].map(t => { const m = t.getScreenCTM();
    return parseFloat(t.getAttribute('font-size')) * (m ? Math.hypot(m.a, m.b) : box.width / svg.viewBox.baseVal.width); });
  return {manual_open: document.getElementById('product-manual').open, hash: location.hash,
          chart_width_px: Math.round(box.width), viewbox_width: svg.viewBox.baseVal.width, marks: svg.querySelectorAll('g.plot *').length,
          smallest_text_px: sizes.length ? Math.round(Math.min(...sizes) * 100) / 100 : null}; }"""


def route(playwright, target: str, out: Path) -> dict:
    """The preview-to-replay route on phones, the archive's own Results link, and landmark positions."""
    browser = _launch(playwright, "chrome")
    url = _url(target)
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
            entry["product_replay"] = page.evaluate(PRODUCT_REPLAY_JS)
            page.screenshot(path=str(out / f"route-product-{width}.png"))
            page.locator("input[name='p-lvl'][value='95']").check()
            page.locator("#p-scale").fill("6")
            page.wait_for_timeout(200)
            entry["product_replay"]["coverage_at_95"] = page.evaluate("document.getElementById('p-cov').textContent.trim()")
            entry["product_replay"]["scenario_caveat_shown"] = page.evaluate("!document.getElementById('p-scenario').hidden")
            entry["product_replay"]["observed_line_hidden"] = page.evaluate(
                "getComputedStyle(document.getElementById('p-legend-actual')).display === 'none'")
            page.get_by_role("link", name="The replay in the archived report").click()
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


# --------------------------------------------------------------------------- discovery routes (PUBLISH_RULES 1.0 A5)

#: Every descriptive route the page advertises from its default view: the product topics, each chapter's
#: "Explore these results", the transition summaries, the preview, the v1 chapter's links and the archive routes.
ROUTES_JS = r"""() => { const routes = [];
  // A link inside a product topic is a second step: it is reached through the topic's own route first.
  const add = (group, a) => { const topic = a.closest('section.topic'); const heading = topic && topic.querySelector('h3[id]');
    routes.push({group, label: a.textContent.trim().replace(/\s+/g, ' '), href: a.getAttribute('href'),
                 visible_by_default: a.checkVisibility(), via: !a.checkVisibility() && heading ? '#' + heading.id : null}); };
  document.querySelectorAll('nav.product-routes a').forEach(a => add('product', a));
  document.querySelectorAll('nav.explore a').forEach(a => add('explore', a));
  document.querySelectorAll('.transition-route a').forEach(a => add('transition', a));
  document.querySelectorAll('.preview-links a[href^="#"]').forEach(a => add('preview', a));
  document.querySelectorAll('.chapter-links a[href^="#"]').forEach(a => add('chapter', a));
  document.querySelectorAll('a.archive-route').forEach(a => add('archive', a));
  return routes; }"""

#: Where a route landed: its target, below the sticky header and in view, with no closed disclosure above it, and
#: the first chart, replay or value table that follows the target inside its section.
LANDING_JS = r"""(href) => { const t = document.getElementById(decodeURIComponent(href.slice(1)));
  if (!t) return {exists: false};
  const header = document.querySelector('.site-header').getBoundingClientRect().bottom, r = t.getBoundingClientRect();
  const closed = []; for (let d = t.closest('details'); d; d = d.parentElement && d.parentElement.closest('details'))
    { if (!d.open) closed.push(d.id || 'details'); }
  // A route to a heading reveals what follows it up to the next heading of the same or a higher level; a route
  // to a whole section reveals the section itself, and is not asked for a chart.
  const level = /^H([1-6])$/.exec(t.tagName), FOLLOWS = Node.DOCUMENT_POSITION_FOLLOWING;
  const next = level ? [...document.querySelectorAll('h1, h2, h3, h4, h5, h6')].find(h => h !== t && !t.contains(h)
      && (t.compareDocumentPosition(h) & FOLLOWS) && Number(h.tagName[1]) <= Number(level[1])) : null;
  const after = !level ? [] : [...document.querySelectorAll('div.chart[data-chart-id], svg#p-chart, svg#chart, table.data')]
    .filter(c => (t.compareDocumentPosition(c) & FOLLOWS) && (!next || (c.compareDocumentPosition(next) & FOLLOWS)));
  let shown = null;
  if (after.length) { const c = after[0], b = c.getBoundingClientRect();
    const drawn = c.matches('div.chart') ? [...c.querySelectorAll('svg')].some(v => v.checkVisibility() && v.getBoundingClientRect().width > 0)
                                         : c.checkVisibility() && b.width > 0;
    shown = {what: c.getAttribute('data-chart-id') || c.id || 'table', visible: drawn, width: Math.round(b.width)}; }
  return {exists: true, heading: t.textContent.trim().replace(/\s+/g, ' ').slice(0, 90), top: Math.round(r.top * 10) / 10,
          header_bottom: Math.round(header * 10) / 10, visible: t.checkVisibility(), below_header: r.top >= header - 1,
          in_view: r.top < innerHeight && r.bottom > 0, closed_ancestors: closed, first_result: shown, hash: location.hash}; }"""


def _landed(result: dict) -> bool:
    return bool(result.get("exists") and result.get("visible") and result.get("below_header") and result.get("in_view")
                and not result.get("closed_ancestors")
                and (result.get("first_result") is None or result["first_result"]["visible"]))


def discovery(playwright, engine: str, target: str, width: int, height: int) -> dict:
    """Follow every advertised route from a fresh, closed default page -- by mouse, by keyboard and as a deep
    link -- and record the label, where it landed and what it revealed (PUBLISH_RULES 1.0 §6, A5)."""
    url = _url(target)
    browser = _launch(playwright, engine)
    context = browser.new_context(viewport={"width": width, "height": height})
    page = context.new_page()
    page.goto(url, wait_until="load")
    routes = page.evaluate(ROUTES_JS)
    results = []
    for item in routes:
        entry = dict(item)
        for method in ("mouse", "keyboard", "deep link"):
            try:
                if method == "deep link":
                    page.goto("about:blank")
                    page.goto(url + item["href"], wait_until="load")
                else:
                    page.goto(url, wait_until="load")
                    if item["via"]:  # a second-step route: open its topic by its own route first
                        page.locator(f'nav.product-routes a[href="{item["via"]}"]').first.click()
                        page.wait_for_timeout(400)
                    link = page.locator(f'a[href="{item["href"]}"]').filter(has_text=item["label"][:40]).first
                    link.scroll_into_view_if_needed(timeout=5000)
                    if method == "mouse":
                        link.click(timeout=5000)
                    else:
                        link.focus()
                        page.keyboard.press("Enter")
                page.wait_for_timeout(500)
                landed = page.evaluate(LANDING_JS, item["href"])
                entry[method] = {**landed, "passed": _landed(landed)}
            except Exception as exc:  # a route that cannot be followed is the finding; keep it and go on
                entry[method] = {"passed": False, "error": f"{type(exc).__name__}: {str(exc)[:200]}"}
        results.append(entry)
    context.close()
    browser.close()
    return {"engine": engine, "viewport": f"{width}x{height}", "routes": results,
            "passed": bool(results) and all(r[m]["passed"] for r in results for m in ("mouse", "keyboard", "deep link"))}


# --------------------------------------------------------------------------- the demo's own controls (review F01)

#: Every interactive element of the demo, through open shadow roots, with its effective target: a radio's label is
#: part of its target, and a slider's hit area is its track, not its thumb (PUBLISH_RULES 1.0 §9, Touch).
DEMO_CONTROLS_JS = r"""() => { const out = []; window.__controls = [];
  const inSentence = el => el.tagName === 'A' && getComputedStyle(el).display === 'inline' && el.parentElement
      && el.parentElement.textContent.trim().length > el.textContent.trim().length + 3;
  const visit = root => root.querySelectorAll('*').forEach(el => {
    const role = el.getAttribute('role') || '', tag = el.tagName.toLowerCase();
    const control = ['slider', 'radio', 'radiogroup', 'button', 'link', 'checkbox', 'switch', 'combobox', 'menuitem', 'tab'].includes(role)
      || tag === 'button' || (tag === 'a' && el.hasAttribute('href')) || ['input', 'select', 'textarea', 'summary'].includes(tag);
    if (control && el.checkVisibility()) {
      let box = el.getBoundingClientRect(); const rootNode = el.getRootNode();
      if (role === 'radio' && el.id) { const l = rootNode.querySelector('label[for="' + el.id + '"]');
        if (l) { const b = l.getBoundingClientRect(); box = {width: b.right - Math.min(box.left, b.left), height: Math.max(box.height, b.height)}; } }
      if (role === 'slider') { const track = el.closest('[data-orientation][id]'); if (track) box = track.getBoundingClientRect(); }
      window.__controls.push(el);
      out.push({index: window.__controls.length - 1, tag, role, text: (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 40),
                in_shadow: rootNode !== document, inline_text_link: inSentence(el),
                width: Math.round(box.width), height: Math.round(box.height)}); }
    if (el.shadowRoot) visit(el.shadowRoot); });
  visit(document); return out; }"""

#: WebKit's own accessibility properties for those elements: an object reference is resolved to an inspector node,
#: which crosses open shadow roots where a selector cannot (the gap the 2026-09-29 review recorded).
WEBKIT_DEMO_AX_JS = r"""
const pw = require(process.env.PW_CORE);
const spec = JSON.parse(process.argv[process.argv.length - 1]);
(async () => {
  const browser = await pw.webkit.launch();
  const page = await browser.newPage({viewport: {width: spec.width, height: spec.height}});
  await page.goto(spec.url);
  await page.getByText(spec.ready).first().waitFor({timeout: spec.timeout * 1000});
  await page.waitForTimeout(1500);
  const controls = await page.evaluate(new Function('return ' + spec.collect)());
  const session = page._connection.toImpl(page).delegate._session;
  await session.send('DOM.getDocument');
  for (const c of controls) {
    const {result} = await session.send('Runtime.evaluate', {expression: 'window.__controls[' + c.index + ']'});
    const {nodeId} = await session.send('DOM.requestNode', {objectId: result.objectId});
    const {properties: p} = await session.send('DOM.getAccessibilityPropertiesForNode', {nodeId});
    Object.assign(c, {ax_role: p.role || '', name: p.label || '', exists: p.exists, ignored: !!p.ignored});
  }
  console.log(JSON.stringify({browser: 'WebKit ' + browser.version(), controls}));
  await browser.close();
})().catch(error => { console.error(String(error && error.stack || error)); process.exit(1); });
"""


def _demo_findings(controls: list[dict]) -> dict:
    unnamed = [f"{c.get('ax_role') or c['role'] or c['tag']}: {c['text']!r}" for c in controls
               if c.get("exists", True) and not c.get("ignored") and not (c.get("name") or "").strip()]
    small = [(c["tag"], c["role"], c["text"], c["width"], c["height"]) for c in controls
             if not c["inline_text_link"] and (c["width"] < 44 or c["height"] < 44)]
    under_24 = [item for item in small if item[3] < 24 or item[4] < 24]
    return {"checked": len(controls), "unnamed": unnamed, "targets_under_44": small, "targets_under_24": under_24,
            "passed": bool(controls) and not unnamed and not small}


#: The focused element, through open shadow roots, and whether it shows a focus indicator (outline or ring).
DEEP_FOCUS_JS = r"""() => { let e = document.activeElement;
  while (e && e.shadowRoot && e.shadowRoot.activeElement) e = e.shadowRoot.activeElement;
  if (!e || e === document.body) return null;
  const s = getComputedStyle(e), ring = (s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) > 0)
    || (s.boxShadow && s.boxShadow !== 'none');
  return {role: e.getAttribute('role') || e.tagName.toLowerCase(), name: (e.getAttribute('aria-label') || e.textContent || '').trim().slice(0, 30),
          visible_focus: ring}; }"""


def _demo_keyboard(page) -> dict:
    """Keyboard operation, the way a keyboard user arrives: the slider moves with an arrow key; the radio group,
    entered at its own tab stop, changes level with an arrow key; Enter opens the notebook menu and Escape closes
    it. marimo's radio group keeps focus on one item while the checked level follows a round trip to the notebook,
    so the check asks whether either arrow key changes the level, and records both."""
    slider = page.get_by_role("slider").first
    slider_before = slider.get_attribute("aria-valuenow")
    slider.focus()
    page.keyboard.press("ArrowRight")
    page.wait_for_timeout(1500)
    slider_after = slider.get_attribute("aria-valuenow")
    focus = {"slider": page.evaluate(DEEP_FOCUS_JS)}

    def level() -> str:
        return page.get_by_role("radio", checked=True).first.get_attribute("value")

    radio_start = level()
    page.get_by_role("radiogroup").first.focus()
    seen = []
    for key in ("ArrowRight", "ArrowLeft"):
        page.keyboard.press(key)
        page.wait_for_timeout(1500)
        seen.append((key, level()))
    focus["radio"] = page.evaluate(DEEP_FOCUS_JS)
    menu = page.locator('[data-testid="notebook-actions-dropdown"] button').first
    menu.focus()
    page.keyboard.press("Enter")
    page.wait_for_timeout(500)
    opened = menu.get_attribute("aria-expanded")
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    focus["menu, after Escape"] = page.evaluate(DEEP_FOCUS_JS)
    return {"focus": focus, "visible_focus": all(item and item["visible_focus"] for item in focus.values()),
            "slider": [slider_before, slider_after], "slider_moved": slider_after != slider_before,
            "radio_start": radio_start, "radio_after_keys": seen,
            "radio_moved": any(value != radio_start for _, value in seen),
            "menu_opened_by_enter": opened == "true", "menu_closed_by_escape": menu.get_attribute("aria-expanded") == "false"}


def demo_controls(playwright, engine: str, url: str, width: int, height: int, timeout_s: float) -> dict:
    """The demo's controls in the engine's own accessibility tree, their target sizes, and keyboard operation of
    the slider, the radio group and the notebook menu (review F01)."""
    record: dict = {"engine": engine, "url": url, "viewport": f"{width}x{height}", "started_utc": _utc(),
                    "cache": "fresh browser context: empty cache, no cookies"}
    if engine == "webkit":
        import os
        import subprocess

        import playwright as _pw

        driver = Path(_pw.__file__).parent / "driver"
        spec = {"url": url, "width": width, "height": height, "ready": READY_TEXT, "timeout": timeout_s,
                "collect": DEMO_CONTROLS_JS}
        result = subprocess.run([str(driver / "node"), "-e", WEBKIT_DEMO_AX_JS, "--", json.dumps(spec)],
                                capture_output=True, text=True, timeout=timeout_s + 120,
                                env={**os.environ, "PW_CORE": str(driver / "package")})
        if result.returncode != 0:
            record.update(error=result.stderr[-600:], passed=False)
            return record
        data = json.loads(result.stdout.strip().splitlines()[-1])
        record.update(browser=data["browser"], method="WebKit's inspector (DOM.getAccessibilityPropertiesForNode), "
                      "nodes resolved from object references through open shadow roots; a private Playwright API")
        controls = data["controls"]
        browser = _launch(playwright, engine)
        page = browser.new_context(viewport={"width": width, "height": height}).new_page()
        page.goto(url, wait_until="domcontentloaded")
        page.get_by_text(READY_TEXT).first.wait_for(timeout=timeout_s * 1000)
        page.wait_for_timeout(1500)
        record["keyboard"] = _demo_keyboard(page)
        browser.close()
    else:
        browser = _launch(playwright, engine)
        page = browser.new_context(viewport={"width": width, "height": height}).new_page()
        page.goto(url, wait_until="domcontentloaded")
        page.get_by_text(READY_TEXT).first.wait_for(timeout=timeout_s * 1000)
        page.wait_for_timeout(1500)
        controls = page.evaluate(DEMO_CONTROLS_JS)
        cdp = page.context.new_cdp_session(page)
        cdp.send("DOM.getDocument", {"depth": 0})
        cdp.send("Accessibility.enable")
        for control in controls:
            handle = cdp.send("Runtime.evaluate", {"expression": f"window.__controls[{control['index']}]"})
            node = cdp.send("DOM.describeNode", {"objectId": handle["result"]["objectId"]})["node"]
            ax = cdp.send("Accessibility.getPartialAXTree", {"backendNodeId": node["backendNodeId"],
                                                              "fetchRelatives": False})["nodes"]
            first = ax[0] if ax else {}
            control.update(ax_role=first.get("role", {}).get("value", ""), name=first.get("name", {}).get("value", ""),
                           exists=bool(first), ignored=bool(first.get("ignored")))
        record.update(browser=f"Chrome {browser.version}",
                      method="Chrome's accessibility tree through the DevTools protocol (Accessibility.getPartialAXTree)")
        record["keyboard"] = _demo_keyboard(page)
        browser.close()
    record["controls"] = controls
    record.update(_demo_findings(controls))
    if "keyboard" in record:
        keys = record["keyboard"]
        record["passed"] = (record["passed"] and keys["slider_moved"] and keys["radio_moved"] and keys["visible_focus"]
                            and keys["menu_opened_by_enter"] and keys["menu_closed_by_escape"])
    return record


# --------------------------------------------------------------------------- the standard's §10 release checks

#: The widths the standard's §10 names; heights are the phone's for the phone widths.
RELEASE_SIZES = ((1440, 900), (768, 1024), (390, 844), (360, 780), (320, 640))
#: Where the cold reader's screens come from (standard §11): one desktop engine, one phone engine.
COLD_READER_VIEWS = (("chrome", 1440, 900), ("webkit", 390, 844))
IPHONE = "iPhone 15"

#: The standard's §1 placements, measured with every disclosure closed.
PLACEMENT_JS = r"""() => {
  const box = e => { if (!e) return null; const r = e.getBoundingClientRect();
    return {top: Math.round((r.top + scrollY) * 10) / 10, bottom: Math.round((r.bottom + scrollY) * 10) / 10}; };
  const q = s => document.querySelector(s);
  const release = q('[data-block="release-rule"]'), actions = q('.actions'), byline = q('.byline a[href="#contribution"]');
  const finding = q('#comparison-finding'), panel = finding && finding.closest('.panel');
  const chart = panel && [...panel.querySelectorAll('svg[role="img"]')].find(s => s.getBoundingClientRect().width > 0);
  const header = q('.site-header');
  return {header_px: header ? Math.round(header.getBoundingClientRect().height * 10) / 10 : null,
          headline: box(q('#headline')), terms: box(q('ul.terms')), finding: box(finding), finding_chart: box(chart),
          release_rule: box(release), demo_action: box(actions), byline: box(byline),
          release_rule_in_disclosure: !!(release && release.closest('details')),
          byline_in_disclosure: !!(byline && byline.closest('details')),
          scroll_width: document.documentElement.scrollWidth, client_width: document.documentElement.clientWidth,
          page_height: document.documentElement.scrollHeight};
}"""

#: The groups the accessibility-tree check reads, by selector, in document order.
AX_GROUPS = {
    "details": "details",
    "summary": "summary",
    "chart": 'svg[role="img"]',
    "control": 'a[href], button, input, select, textarea, summary, [role="button"], [tabindex="0"]',
}
#: A closed disclosure's content stays laid out under `content-visibility: hidden` (the
#: `::details-content` of current Chrome and WebKit), so a bounding box says nothing about whether
#: it is shown; `checkVisibility` does.
VISIBLE_JS = r"""(selector) => [...document.querySelectorAll(selector)].map(e => {
  const r = e.getBoundingClientRect();
  return {visible: e.checkVisibility({visibilityProperty: true, opacityProperty: true}) && (r.width > 0 || r.height > 0),
          text: (e.getAttribute('aria-label') || e.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 50)}; })"""

#: WebKit's own accessibility properties, read through WebKit's inspector protocol
#: (`DOM.getAccessibilityPropertiesForNode`, the data Web Inspector's accessibility panel shows).
#: Playwright 1.63's public API exposes no accessibility tree, so this runs in the Playwright driver's
#: Node, in process, and reaches the page's inspector session through playwright-core's in-process
#: connection (`toImpl`), a private API: if an upgrade removes it, the check fails, never passes.
WEBKIT_AX_JS = r"""
const pw = require(process.env.PW_CORE);
const spec = JSON.parse(process.argv[process.argv.length - 1]);
(async () => {
  const browser = await pw.webkit.launch();
  const page = await browser.newPage({viewport: {width: spec.width, height: spec.height}});
  await page.goto(spec.url);
  await page.waitForTimeout(300);
  const session = page._connection.toImpl(page).delegate._session;
  const read = async () => {
    const out = {};
    for (const [group, selector] of Object.entries(spec.groups)) {
      const {root} = await session.send('DOM.getDocument');
      const {nodeIds} = await session.send('DOM.querySelectorAll', {nodeId: root.nodeId, selector});
      const shown = await page.evaluate(new Function('return ' + spec.visible_js)(), selector);
      out[group] = [];
      for (let i = 0; i < nodeIds.length; i++) {
        const {properties: p} = await session.send('DOM.getAccessibilityPropertiesForNode', {nodeId: nodeIds[i]});
        out[group].push({visible: shown[i].visible, text: shown[i].text, exists: p.exists, ignored: !!p.ignored,
                         role: p.role || '', name: p.label || '', expanded: p.expanded === undefined ? null : p.expanded});
      }
    }
    return out;
  };
  const closed = await read();
  for (let round = 0; round < 8; round++) {
    const summaries = await page.$$('details:not([open]) > summary');
    let acted = 0;
    for (const summary of summaries) {
      if (await summary.isVisible()) { await summary.focus(); await page.keyboard.press('Enter'); acted++; }
    }
    if (!acted) break;
    await page.waitForTimeout(150);
  }
  await page.waitForTimeout(600);
  const opened = await read();
  console.log(JSON.stringify({browser: 'WebKit ' + browser.version(), closed, opened}));
  await browser.close();
})().catch(error => { console.error(String(error && error.stack || error)); process.exit(1); });
"""


def _webkit_ax(url: str, width: int, height: int) -> dict:
    import os
    import subprocess

    import playwright

    driver = Path(playwright.__file__).parent / "driver"
    spec = {"url": url, "width": width, "height": height, "groups": AX_GROUPS, "visible_js": VISIBLE_JS}
    result = subprocess.run([str(driver / "node"), "-e", WEBKIT_AX_JS, "--", json.dumps(spec)],
                            capture_output=True, text=True, timeout=600,
                            env={**os.environ, "PW_CORE": str(driver / "package")})
    if result.returncode != 0:
        raise SystemExit(f"the WebKit accessibility read failed: {result.stderr[-800:]}")
    return json.loads(result.stdout.strip().splitlines()[-1])


def _chrome_ax(playwright, url: str, width: int, height: int) -> dict:
    """Chrome's own accessibility tree, per node, through the DevTools protocol."""
    browser = _launch(playwright, "chrome")
    page = browser.new_page(viewport={"width": width, "height": height})
    page.goto(url, wait_until="load")
    page.wait_for_timeout(300)
    cdp = page.context.new_cdp_session(page)
    cdp.send("Accessibility.enable")

    def read() -> dict:
        page.wait_for_timeout(600)  # Chrome updates its accessibility tree asynchronously after a toggle
        cdp.send("Accessibility.getFullAXTree")  # and serializes it on demand: bring it up to date first
        out = {}
        for group, selector in AX_GROUPS.items():
            root = cdp.send("DOM.getDocument", {"depth": 0})["root"]["nodeId"]
            ids = cdp.send("DOM.querySelectorAll", {"nodeId": root, "selector": selector})["nodeIds"]
            shown = page.evaluate(VISIBLE_JS, selector)
            out[group] = []
            for node_id, dom in zip(ids, shown):
                nodes = cdp.send("Accessibility.getPartialAXTree", {"nodeId": node_id, "fetchRelatives": False})["nodes"]
                node = nodes[0] if nodes else {}
                props = {prop["name"]: prop["value"].get("value") for prop in node.get("properties", [])}
                out[group].append({"visible": dom["visible"], "text": dom["text"], "exists": bool(node),
                                   "ignored": bool(node.get("ignored")), "role": node.get("role", {}).get("value", ""),
                                   "name": node.get("name", {}).get("value", ""), "expanded": props.get("expanded")})
        return out

    closed = read()
    for _ in range(8):
        acted = 0
        for summary in page.query_selector_all("details:not([open]) > summary"):
            if summary.is_visible():
                summary.focus()
                page.keyboard.press("Enter")
                acted += 1
        if not acted:
            break
        page.wait_for_timeout(150)
    record = {"browser": f"Chrome {browser.version}", "closed": closed, "opened": read()}
    browser.close()
    return record


def ax_findings(engine: str, tree: dict) -> dict:
    """The standard's §10 tree rules: disclosures expose an expanded state, charts are named, and no
    control is unnamed. Chrome states a disclosure's state on its summary (DisclosureTriangle);
    WebKit on the details element, which it exposes as the disclosure's group."""
    carrier = "summary" if engine == "chrome" else "details"
    out: dict = {"state_on": carrier}
    for phase, want in (("closed", False), ("opened", True)):
        rows = [row for row in tree[phase][carrier] if row["visible"]]
        wrong = [row["text"] for row in rows if row["expanded"] is not want]
        out[f"disclosures_{phase}"] = {"checked": len(rows), "expanded_state_wrong": wrong}
    for phase in ("closed", "opened"):
        charts = [row for row in tree[phase]["chart"] if row["visible"]]
        controls = [row for row in tree[phase]["control"] if row["visible"]]
        out[f"charts_{phase}"] = {"checked": len(charts),
                                  "unnamed_or_unexposed": [row["text"] for row in charts
                                                           if not row["exists"] or row["ignored"] or not row["name"].strip()
                                                           or row["role"] not in ("image", "img")]}
        out[f"controls_{phase}"] = {"checked": len(controls),
                                    "unnamed_or_unexposed": [f"{row['role']}: {row['text']}" for row in controls
                                                             if not row["exists"] or row["ignored"] or not row["name"].strip()]}
    out["passed"] = (all(out[f"disclosures_{p}"]["checked"] and not out[f"disclosures_{p}"]["expanded_state_wrong"]
                         for p in ("closed", "opened"))
                     and all(out[f"{g}_{p}"]["checked"] and not out[f"{g}_{p}"]["unnamed_or_unexposed"]
                             for g in ("charts", "controls") for p in ("closed", "opened")))
    return out


#: Words that run together on screen although the text has a space between them. A flex or grid container makes
#: each text run and each child element an item of its own, and the space at an item's edge is not rendered:
#: "for <span>v1</span>" shows as "forv1" unless the container sets a gap. Found by the fresh reader, not by a
#: text comparison, which sees the space.
COLLAPSED_SPACE_JS = r"""() => {
  const PHRASING = new Set(['A', 'ABBR', 'B', 'CODE', 'DATA', 'EM', 'I', 'MARK', 'SMALL', 'SPAN', 'STRONG', 'SUB', 'SUP', 'TIME']);
  const words = n => n && n.nodeType === 1 && n.textContent.trim() !== '';
  const out = [];
  for (const el of document.querySelectorAll('body *')) {
    const style = getComputedStyle(el);
    if (!/flex|grid/.test(style.display) || !['normal', '0px'].includes(style.columnGap) || !el.checkVisibility()) continue;
    const kids = [...el.childNodes];
    kids.forEach((node, i) => {
      if (node.nodeType !== 3) return;
      const text = node.textContent, before = kids[i - 1], after = kids[i + 1];
      const merges = text.trim()
        ? (/^\s/.test(text) && words(before)) || (/\s$/.test(text) && words(after))
        : text.length > 0 && words(before) && words(after) && PHRASING.has(before.tagName) && PHRASING.has(after.tagName);
      if (merges) out.push(el.textContent.replace(/\s+/g, ' ').trim().slice(0, 100));
    });
  }
  return [...new Set(out)];
}"""


def _view(playwright, engine: str, url: str, out: Path, *, width: int | None = None, height: int | None = None,
          device: str | None = None) -> dict:
    """One page load with every disclosure closed: placements, overflow, every visible chart's text,
    failed requests and console errors, and a full-page screenshot."""
    browser = _launch(playwright, engine)
    options = dict(playwright.devices[device]) if device else {"viewport": {"width": width, "height": height}}
    options.pop("default_browser_type", None)
    context = browser.new_context(**options)
    page = context.new_page()
    failed: list[str] = []
    errors: list[str] = []
    bad_responses: list[str] = []
    page.on("requestfailed", lambda r: failed.append(f"{r.url[:160]} {r.failure}"))
    page.on("console", lambda m: errors.append(m.text[:300]) if m.type == "error" else None)
    page.on("response", lambda r: bad_responses.append(f"{r.status} {r.url[:160]}") if r.status >= 400 else None)
    page.goto(url, wait_until="load")
    page.wait_for_timeout(1500)  # a browser-made request such as a favicon comes after load
    size = page.viewport_size
    label = device.replace(" ", "-").lower() if device else f"{size['width']}x{size['height']}"
    record: dict = {"engine": engine, "browser": f"{browser.browser_type.name} {browser.version}", "view": label,
                    "viewport": f"{size['width']}x{size['height']}", "placements": page.evaluate(PLACEMENT_JS)}
    def measure_charts() -> dict:
        charts = {}
        for holder in page.locator("div.chart[data-chart-id]").all():
            if holder.is_visible():
                charts[holder.get_attribute("data-chart-id")] = holder.evaluate(CHART_JS)
        return {"checked": len(charts),
                "overlaps": {k: v["overlaps"] for k, v in charts.items() if v["overlaps"]},
                "clipped": {k: v["clipped"] for k, v in charts.items() if v["clipped"]},
                "smallest_text_px": min((v["smallest_text_px"] for v in charts.values()
                                         if v["smallest_text_px"] is not None), default=None)}

    record["charts"] = measure_charts()
    record["collapsed_spaces"] = page.evaluate(COLLAPSED_SPACE_JS)
    shot = out / engine / f"{label}.png"
    shot.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(shot), full_page=True)
    record["screenshot"] = _shown(shot)
    if (engine, size["width"], size["height"]) in COLD_READER_VIEWS and not device:
        record["cold_reader_screens"] = _screens(page, out / "cold-reader" / f"{engine}-{label}")
        record["placement_screens"] = record["cold_reader_screens"]
    elif (size["width"], size["height"]) in A2_SCREENS and not device:
        record["placement_screens"] = _screens(page, out / "placement" / f"{engine}-{label}")
    if record.get("placement_screens"):
        placements, screens = record["placements"], record["placement_screens"]
        header = max([placements["header_px"] or 0] + screens["header_px_seen"])
        record["finding_screen"] = screen_of(placements["finding"]["bottom"], size["height"], header)
    page.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
    page.wait_for_timeout(500)
    record["charts_with_disclosures_open"] = measure_charts()
    record["collapsed_spaces_with_disclosures_open"] = page.evaluate(COLLAPSED_SPACE_JS)
    record["overflow_with_disclosures_open"] = page.evaluate(
        "document.documentElement.scrollWidth - document.documentElement.clientWidth")
    record["failed_requests"] = failed[:20]
    record["console_errors"] = errors[:20]
    record["http_errors"] = bad_responses[:20]
    record["resources_after_document"] = page.evaluate(
        "performance.getEntriesByType('resource').map(e => e.name.slice(0, 160))")[:20]
    context.close()
    browser.close()
    return record


def _screens(page, folder: Path) -> dict:
    """The page as a reader scrolls it, one viewport at a time, the sticky header on every screen.
    Each step is the viewport less the header, so no line hides under it."""
    folder.mkdir(parents=True, exist_ok=True)
    height = page.viewport_size["height"]
    header = page.evaluate("Math.ceil(document.querySelector('.site-header').getBoundingClientRect().height)")
    total = page.evaluate("document.documentElement.scrollHeight")
    step, offsets, seen = height - header, [], []
    for index in range(200):
        offset = min(index * step, max(total - height, 0))
        page.evaluate(f"window.scrollTo(0, {offset})")
        page.wait_for_timeout(120)
        page.screenshot(path=str(folder / f"screen-{index + 1:02d}.png"))
        offsets.append(offset)
        seen.append(page.evaluate("Math.round(document.querySelector('.site-header').getBoundingClientRect().height * 10) / 10"))
        if offset + height >= total:
            break
    page.evaluate("window.scrollTo(0, 0)")
    return {"folder": _shown(folder), "screens": len(offsets), "step_px": step, "header_px": header, "offsets": offsets,
            "header_px_seen": seen}


#: PUBLISH_RULES 1.0 A2: the comparison's finding is readable within N screens -- 2 at 1440 x 900, 3 at 390 x 844 --
#: where every screen after the first loses the persistent header's height to it.
A2_SCREENS = {(1440, 900): 2, (390, 844): 3}


def a2_limit(height: float, screens: int, header: float) -> float:
    """N x H - (N - 1) x h: the last document pixel a reader sees in N consecutive screens advanced by the usable
    height H - h, with a persistent header of height h (PUBLISH_RULES 1.0 A2)."""
    return screens * height - (screens - 1) * header


def screen_of(bottom: float, height: float, header: float) -> int:
    """The consecutive screen, advanced by the usable height, on which a document position becomes visible."""
    screen = 1
    while a2_limit(height, screen, header) < bottom:
        screen += 1
    return screen


def placement_findings(view: dict) -> list[str]:
    """The placements of Publication Standard v1 §1, with PUBLISH_RULES 1.0 A2's measured-header rule for the
    comparison's finding (the largest header height observed on the route), as numbers."""
    p, problems = view["placements"], []
    width, height = (int(v) for v in view["viewport"].split("x"))
    if (width, height) in A2_SCREENS and not view["view"].startswith("iphone"):
        if p["headline"]["top"] < 0 or p["headline"]["bottom"] > height:
            problems.append(f"the headline block ends at {p['headline']['bottom']} px, below the first screen ({height})")
        header = max([p.get("header_px") or 0] + list((view.get("placement_screens") or {}).get("header_px_seen") or []))
        screens = A2_SCREENS[(width, height)]
        limit = a2_limit(height, screens, header)
        if p["finding"]["bottom"] > limit:
            problems.append(f"the finding sentence ends at {p['finding']['bottom']} px, beyond {limit} "
                            f"({screens} screens of {height} px with a {header} px header, A2)")
        if header <= 0:
            problems.append("the persistent header was not measured")
    if not p["terms"] or p["terms"]["top"] < p["headline"]["bottom"] or p["terms"]["top"] - p["headline"]["bottom"] > 40:
        problems.append("the terms are not directly below the headline block")
    if p["finding_chart"] and p["finding"]["bottom"] > p["finding_chart"]["top"]:
        problems.append("the finding sentence is not above the comparison's chart")
    if p["release_rule_in_disclosure"] or not p["release_rule"] or not p["demo_action"]:
        problems.append("the release rule is missing or inside a disclosure")
    elif abs(p["release_rule"]["top"] - p["demo_action"]["bottom"]) > 40:
        problems.append("the release rule is not beside the demo action")
    if not p["byline"] or p["byline_in_disclosure"]:
        problems.append("the byline link to the contribution statement is missing")
    if p["scroll_width"] > p["client_width"]:
        problems.append(f"horizontal overflow: {p['scroll_width']} > {p['client_width']}")
    return problems


def release(playwright, target: str, out: Path) -> dict:
    """Every check the standard's §10 requires, on the local page, recorded in one place."""
    url = _url(target)
    views = []
    for engine in ("chrome", "webkit"):
        for width, height in RELEASE_SIZES:
            views.append(_view(playwright, engine, url, out, width=width, height=height))
            print(f"{engine} {width}x{height}: done")
    views.append(_view(playwright, "webkit", url, out, device=IPHONE))
    for view in views:
        view["problems"] = placement_findings(view)
        for key in ("charts", "charts_with_disclosures_open"):
            if view[key]["overlaps"] or view[key]["clipped"]:
                view["problems"].append(f"{key}: chart text overlaps or is clipped")
            if (view[key]["smallest_text_px"] or 99) < 12:
                view["problems"].append(f"{key}: chart text of {view[key]['smallest_text_px']} px")
        for key in ("collapsed_spaces", "collapsed_spaces_with_disclosures_open"):
            if view[key]:
                view["problems"].append(f"{key}: words run together in {view[key]}")
        if view["overflow_with_disclosures_open"] > 0:
            view["problems"].append(f"horizontal overflow of {view['overflow_with_disclosures_open']} px with disclosures open")
        if view["failed_requests"] or view["console_errors"] or view["http_errors"]:
            view["problems"].append("failed requests, HTTP errors or console errors")
        if view["resources_after_document"]:
            view["problems"].append(f"the page fetched {len(view['resources_after_document'])} resource(s) after the document")
    trees = {}
    for engine in ("chrome", "webkit"):
        for width, height in ((1440, 900), (390, 844)):
            tree = _chrome_ax(playwright, url, width, height) if engine == "chrome" else _webkit_ax(url, width, height)
            trees[f"{engine} {width}x{height}"] = {"browser": tree["browser"], **ax_findings(engine, tree)}
            print(f"accessibility tree, {engine} {width}x{height}: passed={trees[f'{engine} {width}x{height}']['passed']}")
    routes = [discovery(playwright, engine, target, width, height)
              for engine in ("chrome", "webkit") for width, height in A2_SCREENS]
    for run in routes:
        print(f"discovery, {run['engine']} {run['viewport']}: {len(run['routes'])} routes, passed={run['passed']}")
    checklist = [a11y(playwright, engine, target) for engine in ("chrome", "webkit")]
    for run in checklist:
        keyboard, touch = run["keyboard"], run["touch_targets_390"]
        run["passed"] = (keyboard["in_document_order"] and not keyboard["without_visible_focus"]
                         and keyboard["summary_toggles_on_enter"] and keyboard["anchor_into_closed_disclosure_opens_it"]
                         and not touch["under_44_count"] and not touch["under_24_count"]
                         and all(not c["below_count"] and not c["non_text"]["below_count"] for c in run["contrast"].values())
                         and all(not z["overflow_px_closed"] and not z["overflow_px_open"] for z in run["zoom_and_reflow"].values()))
    return {
        "check": "Release checks of PUBLISH_RULES 1.0 §9 (Publication Standard v1 §10), the §1 placements with A2's "
                 "measured header, and A5's discovery routes",
        "checked_at_utc": _utc(), "page": target,
        "host": f"{platform.machine()} / {platform.system()} {platform.release()}",
        "not_used": "No real Safari, no real iPhone and no screen reader were used (standard §10); the phone "
                    "widths are emulated viewports, and the iPhone is Playwright's emulated device in WebKit.",
        "engines": {"chrome": "Google Chrome through Playwright's channel='chrome'",
                    "webkit": "Playwright's WebKit build, the Safari engine but not Safari"},
        "views": views,
        "accessibility_trees": trees,
        "accessibility_tree_method": {
            "chrome": "Chrome's own accessibility tree, per node, through the DevTools protocol "
                      "(Accessibility.getPartialAXTree)",
            "webkit": "WebKit's own accessibility properties, per node, through WebKit's inspector protocol "
                      "(DOM.getAccessibilityPropertiesForNode), reached through playwright-core's in-process "
                      "connection, a private API of Playwright 1.63",
        },
        "keyboard_touch_contrast_zoom": checklist,
        "discovery": routes,
        "served_over": "http(s)" if "://" in target else "file (browser-made requests such as a favicon do not occur)",
        "placement_rule": "PUBLISH_RULES 1.0 A2: finding bottom <= N x H - (N - 1) x h, N = 2 at 1440x900 and 3 at "
                          "390x844, h the largest persistent-header height seen on the route",
        "passed": (all(not view["problems"] for view in views) and all(tree["passed"] for tree in trees.values())
                   and all(run["passed"] for run in checklist) and all(run["passed"] for run in routes)),
    }


#: The engines the MLflow index names (brief W11): Chromium is driven as the installed Google Chrome.
MLFLOW_ENGINES = {"chromium": "chrome", "webkit": "webkit"}


def mlflow_expected(route: dict, mirror: dict) -> list[str]:
    """What a route must show once the MLflow UI has rendered it: the experiment's name and every
    parent run's name, or, for a comparison, its header and every run's name and ID. The names are
    the committed export's, which the contract test binds to the registry; this tool environment
    does not import the project."""
    names, parents = {}, []
    for path in sorted((ROOT / "reports" / "presentation" / "mlflow-export").glob("*.json")):
        if path.name != "manifest.json":
            for run in json.loads(path.read_text())["runs"]:
                names[run["run_key"]] = run["run_name"]
                if run["parent"] is None:
                    parents.append(run["run_key"])
    if route["kind"] == "experiment":
        return [mirror.get("experiment", "delu-generations")] + [names[key] for key in parents]
    return ([f"Comparing {len(route['run_keys'])} Runs"] + [names[key] for key in route["run_keys"]]
            + [mirror["runs"][key]["run_id"] for key in route["run_keys"]])


def mlflow_route(playwright, engine: str, route_id: str, route: dict, mirror: dict, out: Path,
                 timeout_s: float) -> dict:
    """Open one advertised route anonymously, in a fresh context, and wait for what it must show."""
    browser = _launch(playwright, MLFLOW_ENGINES[engine])
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()
    base = mirror["target"].rstrip("/")
    failed: list[str] = []
    errors: list[str] = []
    api_errors: list[str] = []
    page.on("requestfailed", lambda r: failed.append(f"{r.url[:160]} {r.failure}"))
    page.on("console", lambda m: errors.append(m.text[:300]) if m.type == "error" else None)
    page.on("response", lambda r: api_errors.append(f"{r.status} {r.url[:160]}")
            if r.status >= 400 and r.url.startswith(base) and "api/" in r.url else None)
    expected = mlflow_expected(route, mirror)
    record: dict = {"engine": engine, "browser": f"{browser.browser_type.name} {browser.version}",
                    "url": route["url"], "expected": expected, "started_utc": _utc()}
    missing = expected
    start = time.monotonic()
    try:
        page.goto(route["url"], wait_until="domcontentloaded", timeout=timeout_s * 1000)
        while time.monotonic() - start < timeout_s:
            text = page.inner_text("body")
            missing = [item for item in expected if item not in text]
            if not missing:
                break
            page.wait_for_timeout(500)
    except Exception as exc:  # the failure is the finding
        record["error"] = f"{type(exc).__name__}: {str(exc)[:300]}"
    # A comparison route is settled only when its chart has drawn: a Plotly plot and no loading skeleton. An
    # application shell or an HTTP 200 without the intended chart is not a pass (PUBLISH_RULES 1.0 §8).
    if route["kind"] == "compare" and "error" not in record:
        try:
            page.wait_for_function("document.querySelectorAll('.js-plotly-plot svg.main-svg').length > 0 && "
                                   "document.querySelectorAll('[class*=Skeleton]').length === 0",
                                   timeout=timeout_s * 1000)
        except Exception as exc:  # the unsettled chart is the finding
            record["settle_error"] = f"{type(exc).__name__}: {str(exc)[:200]}"
        record["plots"] = page.locator(".js-plotly-plot svg.main-svg").count()
        record["skeletons"] = page.locator("[class*=Skeleton]").count()
    record["seconds"] = round(time.monotonic() - start, 1)
    record["final_url"] = page.url
    record["missing"] = missing
    shot = out / f"{route_id.replace(':', '-')}-{engine}.png"
    shot.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(shot))
    record["screenshot"] = _shown(shot)
    record["failed_requests"] = failed[:20]
    record["console_errors"] = errors[:20]
    record["api_errors"] = api_errors[:20]
    record["sign_in_redirect"] = "login" in page.url.lower() or "sign" in page.url.lower()
    settled = route["kind"] != "compare" or (record.get("plots", 0) > 0 and not record.get("skeletons")
                                             and "settle_error" not in record)
    record["passed"] = (not missing and "error" not in record and not api_errors and not record["sign_in_redirect"]
                        and settled)
    context.close()
    browser.close()
    return record


def mlflow_routes(playwright, mirror: dict, out: Path, timeout_s: float) -> dict:
    """Every route that passed its REST check, in both engines (brief W11); the verifier's `index`
    command reads this record and advertises only the routes that passed everywhere."""
    routes: dict = {}
    for route_id, route in sorted(mirror.get("routes", {}).items()):
        if route.get("rest") != "passed":
            continue
        routes[route_id] = {engine: mlflow_route(playwright, engine, route_id, route, mirror, out, timeout_s)
                            for engine in MLFLOW_ENGINES}
        print(f"{route_id}: " + ", ".join(f"{engine} {'passed' if result['passed'] else 'FAILED ' + str(result['missing'][:3])}"
                                          for engine, result in routes[route_id].items()))
    return {"check": "MLflow routes in a browser, anonymously (brief W11; plan §10.7)",
            "checked_at_utc": _utc(), "target": mirror["target"], "experiment_id": mirror["experiment_id"],
            "host": f"{platform.machine()} / {platform.system()} {platform.release()}",
            "client": "Playwright, a fresh browser context per route and engine; no cookies, no sign-in",
            "viewport": "1440x900", "routes": routes,
            "passed": bool(routes) and all(result["passed"] for per in routes.values() for result in per.values())}


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
    checks = sub.add_parser("release", help="every check of the standard's §10, and the §1 placements")
    checks.add_argument("page")
    checks.add_argument("--shots", type=Path, required=True, help="screenshot folder, under .local/artifacts/")
    checks.add_argument("--out", type=Path, required=True)
    controls = sub.add_parser("demo-a11y", help="the demo's controls: native names, targets and keyboard (F01)")
    controls.add_argument("--engine", action="append", choices=["chrome", "webkit"], required=True)
    controls.add_argument("--viewport", action="append", default=None, help="WIDTHxHEIGHT; repeatable")
    controls.add_argument("--url", default=APP_URL)
    controls.add_argument("--timeout", type=float, default=240.0)
    controls.add_argument("--out", type=Path, required=True)
    routes = sub.add_parser("mlflow-routes", help="open every REST-verified MLflow route in both engines")
    routes.add_argument("--mirror-record", type=Path, required=True, help="the verifier's record (verify --out)")
    routes.add_argument("--timeout", type=float, default=90.0)
    routes.add_argument("--shots", type=Path, required=True, help="screenshot folder, under .local/artifacts/")
    routes.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise SystemExit(
            "Playwright is not installed here. It lives in a tool environment under "
            ".local/tools/, never in the project; see this script's docstring."
        )

    if args.command == "release":
        with sync_playwright() as playwright:
            record = release(playwright, args.page, args.shots)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
        for view in record["views"]:
            if view["problems"]:
                print(f"{view['engine']} {view['view']}: {view['problems']}")
        print(f"wrote {args.out}; passed={record['passed']}")
        return 0 if record["passed"] else 1

    if args.command == "demo-a11y":
        sizes = [tuple(int(v) for v in spec.split("x")) for spec in (args.viewport or ["390x844"])]
        with sync_playwright() as playwright:
            runs = [demo_controls(playwright, engine, args.url, width, height, args.timeout)
                    for engine in args.engine for width, height in sizes]
        for run in runs:
            print(f"{run['engine']} {run['viewport']}: passed={run.get('passed')} unnamed={run.get('unnamed')} "
                  f"under_44={run.get('targets_under_44')} keyboard={run.get('keyboard')}")
        record = {"check": "the demo's controls: names in each engine's own accessibility tree, targets of about "
                           "44 px and keyboard operation (review F01; PUBLISH_RULES 1.0 §7.1, §9)",
                  "checked_at_utc": _utc(), "host": f"{platform.machine()} / {platform.system()} {platform.release()}",
                  "runs": runs, "passed": bool(runs) and all(run.get("passed") for run in runs)}
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
        print(f"wrote {args.out}; passed={record['passed']}")
        return 0 if record["passed"] else 1

    if args.command == "mlflow-routes":
        mirror = json.loads(args.mirror_record.read_text())
        with sync_playwright() as playwright:
            record = mlflow_routes(playwright, mirror, args.shots, args.timeout)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
        print(f"wrote {args.out}; passed={record['passed']}")
        return 0 if record["passed"] else 1

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
