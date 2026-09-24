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
        page.get_by_text(READY_TEXT).first.wait_for(timeout=timeout_s * 1000)
        page.get_by_text(CHART_TEXT).first.wait_for(timeout=timeout_s * 1000)
        record["seconds_to_visible_forecast"] = round(time.monotonic() - start, 1)
        record["ready"] = True
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
  const texts = [...document.querySelectorAll('.chart svg text')].filter(t => {
    const svg = t.closest('svg'); const box = t.getBoundingClientRect();
    return svg && getComputedStyle(svg).display !== 'none' && box.width > 0 && box.height > 0;
  });
  let smallest = null, where = null;
  for (const t of texts) {
    const svg = t.closest('svg');
    const scale = svg.getBoundingClientRect().width / svg.viewBox.baseVal.width;
    const size = parseFloat(t.getAttribute('font-size') || '13') * scale;
    if (smallest === null || size < smallest) { smallest = size; where = svg.dataset.chart + ':' + svg.dataset.variant; }
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
    args = parser.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise SystemExit(
            "Playwright is not installed here. It lives in a tool environment under "
            ".local/tools/, never in the project; see this script's docstring."
        )

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
