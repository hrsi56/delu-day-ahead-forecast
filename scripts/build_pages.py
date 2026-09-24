#!/usr/bin/env python3
"""Build the static GitHub Pages site: one scrolling history page (presentation plan §7–§9).

**Why this is not `marimo export html`.** CP-3 measured that export on 2026-09-14 (marimo 0.24.2):
it emits 181 references to `cdn.jsdelivr.net`, so the page cannot render without network, and the
page must make **zero runtime calls**. The measurement is recorded in `reports/cp3/pages_build.json`;
this purpose-built static assembly is the plan's fallback.

**What the page is.** A product-led research case study (plan §7.1): the released v1 product
first, then how successive research generations were compared, newest first, then how the system
works and how to check it. v1's full original report is preserved inside the v1 chapter as an
archive disclosure, with scoped styles, stable anchors and its interactive fan chart unchanged.

**Where the numbers come from.** Research numbers come only from `delu_forecast.research` through
the claim templates in `delu_forecast.research_claims`; v1's numbers come only from
`delu_forecast.claims`. This file types no research number (plan §6 invariant 17). Every research
value in HTML is a `<data>` element carrying its claim and record; every value inside an SVG is a
`<text>` or mark carrying the same attributes; axis ticks carry `data-scale`; structural numerals
(versions, dates, folds, control values) carry `data-structural`.

**Everything is inlined:** CSS in one `<style>`, figures as `data:` URIs, charts as inline SVG and
two small inline scripts (the fan chart, and opening a closed disclosure when a link targets
something inside it). No stylesheet link, font, script src, image src, iframe or beacon.
`tests/test_19_static_page_is_offline.py` asserts that on the built file.

    uv run python scripts/build_pages.py                       # docs/index.html
    uv run python scripts/build_pages.py --specimen DIR        # D1 specimen, token sheet, stress case
    uv run python scripts/build_pages.py --final               # refuse any unpublished-link marker
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import math
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from delu_forecast import research as R  # noqa: E402
from delu_forecast import research_claims as RC  # noqa: E402
from delu_forecast.claims import (  # noqa: E402
    GFS_ATTRIBUTION,
    MLFLOW_RUN_NAMES,
    build_claims,
    limitation_bullets,
    reproducibility_bullets,
)
from delu_forecast.postprocess import QUANTILE_LABELS  # noqa: E402
from delu_forecast.showcase import (  # noqa: E402
    INTERVAL_LEVELS,
    actuals_for_day,
    default_target_day,
    forecast_delivery_day,
    load_champion,
    load_snapshot,
)

OUTPUT = ROOT / "docs" / "index.html"
BUILD_RECORD = ROOT / "reports" / "cp3" / "pages_build.json"
MLFLOW_INDEX = ROOT / "reports" / "presentation" / "mlflow_index.json"
DEMO_CHECK = ROOT / "reports" / "presentation" / "release-checks" / "2026-09-24-demo.json"

#: One dimension, eleven points. The level selector is not a second dimension: it reads two of
#: the nine quantiles already stored at each point.
LOAD_SCALES: tuple[float, ...] = tuple(round(0.90 + 0.02 * index, 2) for index in range(11))

BOLD = re.compile(r"\*\*(.+?)\*\*")
CODE = re.compile(r"`([^`]+)`")

# --------------------------------------------------------------------------- design tokens (§7.3)

#: The D1 starting tokens from plan §7.3. Contrast was computed against white and the canvas;
#: `token_sheet()` recomputes and prints every ratio so a change here is visible.
TOKENS: dict[str, str] = {
    "canvas": "#FAFAFA",
    "surface": "#FFFFFF",
    "border": "#E4E4E7",
    "text": "#18181B",
    "text-2": "#52525B",
    "accent": "#1D4ED8",
    "primary": "#18181B",
    "primary-hover": "#3F3F46",
    "primary-pressed": "#52525B",
    "v1": "#475569",
    "v2": "#6D28D9",
    "v3": "#0F766E",
    "ref": "#71717A",
    "badge-bg": "#F4F4F5",
    "badge-text": "#3F3F46",
    "caveat-rule": "#52525B",
    "grid": "#E4E4E7",
}

SPACE = (4, 8, 12, 16, 24, 32, 48, 64, 96)
FONT_STACK = 'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif'
MONO_STACK = 'ui-monospace, SFMono-Regular, Menlo, Consolas, monospace'

#: Chart geometry. Desktop SVGs render at most 1:1 (13 px text); phones get a dedicated variant
#: whose viewBox fits the 390 px column, so chart text stays at or above 12 px there
#: (plan §6 invariant 23; asserted by tests/test_31_page_structure.py from these constants).
DESKTOP_W = 760
MOBILE_W = 296
CHART_FONT = 13
MOBILE_BREAKPOINT = 820
MOBILE_MAX_W = 440
#: The chart column at a 390 px viewport: 390 − 2 × 16 px gutter − 2 × 12 px panel padding; at 320 px the
#: page uses 12 px gutters and 8 px panel padding (the ≤340 px rule in `css()`).
MOBILE_COLUMN_AT_390 = 390 - 2 * 16 - 2 * 12
MOBILE_COLUMN_AT_320 = 320 - 2 * 12 - 2 * 8
#: Characters of 13 px chart text that fit one phone line.
MOBILE_LINE_CHARS = 39

ROLE_STYLE = {
    "v3": {"color": TOKENS["v3"], "marker": "circle", "filled": True},
    "v2": {"color": TOKENS["v2"], "marker": "square", "filled": True},
    "v1": {"color": TOKENS["v1"], "marker": "triangle", "filled": True},
    "reference": {"color": TOKENS["ref"], "marker": "diamond", "filled": False},
    "study": {"color": TOKENS["ref"], "marker": "circle", "filled": False},
    "control": {"color": TOKENS["ref"], "marker": "square", "filled": False},
}


def relative_luminance(hex_colour: str) -> float:
    rgb = [int(hex_colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a: str, b: str) -> float:
    la, lb = sorted((relative_luminance(a), relative_luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


# --------------------------------------------------------------------------- small helpers


def data_uri(path: Path) -> str:
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()


def esc(value: object) -> str:
    return html.escape(str(value), quote=False)


def attr(value: object) -> str:
    return html.escape(str(value), quote=True)


def S(kind: str, text: str) -> str:
    """A structural numeral in HTML (plan §9.3)."""
    return RC.structural(kind, text)


def ver(label: str) -> str:
    return S("version", label)


def block(key: str, tag: str = "p", cls: str | None = None) -> str:
    """A claim block rendered from its template, wrapped so tests can find it."""
    klass = f' class="{cls}"' if cls else ""
    return f'<{tag}{klass} data-block="{key}">{RC.render(key)}</{tag}>'


def value(record_id: str, claim_id: str, which: str = "value", option: str | None = None) -> str:
    """One research value in HTML, outside a sentence template."""
    token = {"value": "", "ci_low": "|lo", "ci_high": "|hi"}[which] if not option else f"|{option}"
    return RC.render_template(claim_id, "{r:%s%s}" % (record_id, token))


def interval(record_id: str, claim_id: str) -> str:
    return RC.render_template(claim_id, "{r:%s|ci}" % record_id)


def v1(key: str, claim_id: str = "P11") -> str:
    return RC.render_template(claim_id, "{v1:%s}" % key)


def table(frame: pd.DataFrame, *, float_format: str = "{:.4g}") -> str:
    head = "".join(f"<th>{esc(column)}</th>" for column in frame.columns)
    rows = []
    for _, row in frame.iterrows():
        cells = []
        for cell in row:
            if isinstance(cell, float) and cell == cell:
                cells.append(f"<td class='n'>{float_format.format(cell)}</td>")
            elif cell != cell:
                cells.append("<td class='n'></td>")
            else:
                cells.append(f"<td>{esc(cell)}</td>")
        rows.append("<tr>" + "".join(cells) + "</tr>")
    return f"<div class='scroll'><table><thead><tr>{head}</tr></thead><tbody>{''.join(rows)}</tbody></table></div>"


def github(path: str, ref: str = "main", line: int | None = None) -> str:
    anchor = f"#L{line}" if line else ""
    return f"{build_claims()['github_url']}/blob/{ref}/{path}{anchor}"


# --------------------------------------------------------------------------- evidence rows (§7.9)


def mlflow_index() -> dict:
    """The committed index of public MLflow routes, written only after an authorized upload."""
    if MLFLOW_INDEX.exists():
        return json.loads(MLFLOW_INDEX.read_text())
    return {}


def evidence_row(*, compare: str | None, review: tuple[str, str], source: tuple[str, str],
                 extra: list[tuple[str, str]] | None = None) -> str:
    """"Compare experiment runs · Read the review · View source values" (plan §7.9, review §4E).
    An unpublished destination is shown as unavailable, never as a link that looks complete."""
    routes = mlflow_index().get("routes", {})
    items = []
    if compare is not None:
        url = routes.get(compare)
        if url:
            items.append(f'<a class="ev external" href="{attr(url)}">Compare experiment runs</a>')
        else:
            items.append(
                f'<span class="ev is-unavailable" data-unpublished="mlflow:{attr(compare)}">'
                "Compare experiment runs <span class=\"why\">(link added when the runs are published)</span></span>"
            )
    items.append(f'<a class="ev external" href="{attr(review[1])}">{esc(review[0])}</a>')
    items.append(f'<a class="ev external" href="{attr(source[1])}">{esc(source[0])}</a>')
    for label, url in extra or []:
        items.append(f'<a class="ev external" href="{attr(url)}">{esc(label)}</a>')
    return '<p class="evidence-row"><span class="ev-label">Evidence</span>' + "".join(items) + "</p>"


# --------------------------------------------------------------------------- components (§7.4)


def badge(text: str, kind: str = "development") -> str:
    return f'<span class="badge badge-{kind}">{esc(text)}</span>'


def adoption(text: str) -> str:
    return f'<span class="adoption">{_structural_versions(text)}</span>'


def disclosure(ident: str, title: str, body: str, *, open_: bool = False) -> str:
    opened = " open" if open_ else ""
    return (
        f'<details class="disclosure" id="{ident}"{opened}><summary><span class="marker" aria-hidden="true"></span>'
        f"<span>{_structural_versions(title)}</span></summary><div class=\"disclosure-body\">{body}</div></details>"
    )


# --------------------------------------------------------------------------- SVG chart library


class UnitMixError(ValueError):
    """Two units on one axis. The renderer refuses rather than drawing it (plan §7.5, §9.3)."""


@dataclass(frozen=True)
class Row:
    """One mark on a categorical row: a record, drawn in a role's style."""

    label: str
    record_id: str
    role: str
    code: str = ""
    bold: bool = False
    claim: str | None = None


@dataclass
class Scale:
    ident: str
    lo: float
    hi: float
    x0: float
    x1: float
    unit: str

    def __call__(self, value: float) -> float:
        return self.x0 + (value - self.lo) / (self.hi - self.lo) * (self.x1 - self.x0)

    def ticks(self, step: float) -> list[float]:
        first = math.ceil(self.lo / step - 1e-9) * step
        out, tick = [], first
        while tick <= self.hi + 1e-9:
            out.append(round(tick, 10))
            tick += step
        return out


def axis_unit(record_ids: list[str]) -> str:
    """The one unit a set of records shares, or `UnitMixError`."""
    units = {R.get(record_id).unit for record_id in record_ids}
    if len(units) != 1:
        raise UnitMixError(f"one axis cannot carry {sorted(units)}")
    return units.pop()


def tick_text(value: float, step: float) -> str:
    places = max(0, -int(math.floor(math.log10(step)))) if step < 1 else 0
    text = f"{value:.{places}f}"
    return text.replace("-", R.MINUS) if value < 0 else text


def svg_text(x: float, y: float, text: str, *, size: int = CHART_FONT, anchor: str = "start",
             weight: str | None = None, fill: str | None = None, extra: str = "") -> str:
    style = f' font-weight="{weight}"' if weight else ""
    colour = fill or TOKENS["text"]
    if "data-" not in extra and any(ch.isdigit() for ch in text):
        extra += ' data-structural="label"'
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{colour}"'
            f"{style}{extra}>{esc(text)}</text>")


def marker(x: float, y: float, role: str, *, size: float = 6.0, extra: str = "") -> str:
    style = ROLE_STYLE[role]
    colour = style["color"]
    fill = colour if style["filled"] else TOKENS["surface"]
    if style["marker"] == "circle":
        shape = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{size:.1f}" '
    elif style["marker"] == "square":
        s = size * 0.9
        shape = f'<rect x="{x - s:.1f}" y="{y - s:.1f}" width="{2 * s:.1f}" height="{2 * s:.1f}" '
    elif style["marker"] == "triangle":
        s = size * 1.15
        shape = f'<polygon points="{x:.1f},{y - s:.1f} {x + s:.1f},{y + s * 0.8:.1f} {x - s:.1f},{y + s * 0.8:.1f}" '
    else:
        s = size * 1.1
        shape = f'<polygon points="{x:.1f},{y - s:.1f} {x + s:.1f},{y:.1f} {x:.1f},{y + s:.1f} {x - s:.1f},{y:.1f}" '
    # A surface-coloured ring under the mark keeps touching or overlapping marks distinct.
    ring = shape + f'fill="{TOKENS["surface"]}" stroke="{TOKENS["surface"]}" stroke-width="4.6" aria-hidden="true"/>'
    return ring + shape + f'fill="{fill}" stroke="{colour}" stroke-width="1.8"{extra}/>'


def svg_wrap(width: float, height: float, body: str, *, title: str, desc: str, variant: str,
             chart_id: str) -> str:
    tid, did = f"{chart_id}-{variant}-t", f"{chart_id}-{variant}-d"
    return (
        f'<svg class="{variant}" viewBox="0 0 {width:.0f} {height:.0f}" role="img" '
        f'aria-labelledby="{tid} {did}" font-family="{attr(FONT_STACK)}" data-chart="{chart_id}" '
        f'data-variant="{variant}" xmlns="http://www.w3.org/2000/svg">'
        f'<title id="{tid}">{esc(title)}</title><desc id="{did}">{esc(desc)}</desc>{body}</svg>'
    )


def scale_ticks(scale: Scale, step: float, y_top: float, y_bottom: float, *, labels_at: float,
                grid: bool = True, size: int = CHART_FONT) -> str:
    out = []
    for tick in scale.ticks(step):
        x = scale(tick)
        if grid:
            out.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{y_top:.1f}" y2="{y_bottom:.1f}" '
                       f'stroke="{TOKENS["grid"]}" stroke-width="1"/>')
        out.append(svg_text(x, labels_at, tick_text(tick, step), size=size, anchor="middle",
                            fill=TOKENS["text-2"], extra=f' data-scale="{scale.ident}"'))
    return "".join(out)


def ref_line(scale: Scale, at: float, y_top: float, y_bottom: float, *, dash: str | None, colour: str,
             binding: str = "", width: float = 1.4) -> str:
    x = scale(at)
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{y_top:.1f}" y2="{y_bottom:.1f}" stroke="{colour}" '
            f'stroke-width="{width}"{dash_attr}{binding}/>')


HALO = ' paint-order="stroke" stroke="#FFFFFF" stroke-width="4" stroke-linejoin="round"'


def value_label(x: float, y: float, claim_id: str, record_id: str, *, which: str = "value",
                anchor: str = "start", option: str | None = None, size: int = CHART_FONT,
                weight: str | None = None, fill: str | None = None, prefix: str = "") -> str:
    text = prefix + RC.svg_value(record_id, which, option)
    return svg_text(x, y, text, size=size, anchor=anchor, weight=weight, fill=fill,
                    extra=RC.svg_binding(claim_id, record_id, which) + HALO)


@dataclass(frozen=True)
class Ref:
    """A reference line: a value from a record (bound) or a structural value (e.g. zero)."""

    label: str
    record_id: str | None = None
    at: float | None = None
    dash: str | None = "5 4"
    colour: str = TOKENS["text-2"]
    option: str | None = None

    def position(self) -> float:
        return R.get(self.record_id).value if self.record_id else float(self.at)

    def text(self) -> str:
        if self.record_id:
            return self.label.replace("{v}", RC.svg_value(self.record_id, "value", self.option))
        return self.label


@dataclass(frozen=True)
class Panel:
    title: str
    subtitle: str
    rows: tuple[Row, ...]
    domain: tuple[float, float]
    step: float
    refs: tuple[Ref, ...] = ()
    exact_hi: tuple[str, ...] = ()
    scale_id: str = "x"


def _check_panel_units(panel: Panel) -> str:
    return axis_unit([row.record_id for row in panel.rows] + [ref.record_id for ref in panel.refs if ref.record_id])


def _interval_marks(scale: Scale, y: float, record: R.EvidenceRecord, role: str, claim_id: str) -> str:
    if record.interval is None:
        return ""
    colour = ROLE_STYLE[role]["color"]
    lo, hi = scale(record.ci_low), scale(record.ci_high)
    bind_lo = RC.svg_binding(claim_id, record.record_id, "ci_low")
    bind_hi = RC.svg_binding(claim_id, record.record_id, "ci_high")
    return (f'<line x1="{lo:.1f}" x2="{hi:.1f}" y1="{y:.1f}" y2="{y:.1f}" stroke="{colour}" stroke-width="2.4"/>'
            f'<line x1="{lo:.1f}" x2="{lo:.1f}" y1="{y - 6:.1f}" y2="{y + 6:.1f}" stroke="{colour}" stroke-width="2"{bind_lo}/>'
            f'<line x1="{hi:.1f}" x2="{hi:.1f}" y1="{y - 6:.1f}" y2="{y + 6:.1f}" stroke="{colour}" stroke-width="2"{bind_hi}/>')


def _row_value_text(scale: Scale, x_mark: float, y: float, row: Row, claim_id: str, x_right: float,
                    size: int = CHART_FONT, *, x_left: float | None = None) -> str:
    claim_id = row.claim or claim_id
    record = R.get(row.record_id)
    weight = "600" if row.bold else None
    if record.interval is not None:
        low = RC.svg_value(row.record_id, "ci_low")
        if (row.record_id, "ci_high") in RC.EXACT_FIELDS:
            high = "see below"  # printed in full under the plot, never rounded (invariant 9)
        else:
            high = RC.svg_value(row.record_id, "ci_high")
        text = f"{RC.svg_value(row.record_id)} [{low}, {high}]"
        if x_left is not None:
            return svg_text(x_left, y + 4.5, text, size=size, anchor="start",
                            extra=RC.svg_binding(claim_id, row.record_id) + HALO, weight=weight)
        return svg_text(x_right, y + 4.5, text, size=size, anchor="end",
                        extra=RC.svg_binding(claim_id, row.record_id) + HALO, weight=weight)
    near_right = x_mark > x_right - 58
    return value_label(x_mark + (-10 if near_right else 10), y + 4.5, claim_id, row.record_id,
                       anchor="end" if near_right else "start", size=size, weight=weight)


def single_rows(chart_id: str, claim_id: str, panels: list[Panel], *, title: str, desc: str,
                label_width: int = 250, row_h: int = 38, values_inline: bool = True) -> str:
    """Categorical rows with one mark each, optionally with its confidence interval.

    Dot plots (no intervals) put their panels side by side and label each mark. Interval charts
    give every row a value column -- "estimate [low, high]" -- and stack their panels, so an
    interval never collides with its own label. Phones get a dedicated stacked variant."""
    for panel in panels:
        _check_panel_units(panel)
    has_interval = any(R.get(row.record_id).interval for panel in panels for row in panel.rows)
    parts: list[str] = []

    def refs_and_ticks(panel: Panel, scale: Scale, top: float, bottom: float, label_y: float, compact: bool) -> None:
        step = panel.step * (2 if compact and (panel.domain[1] - panel.domain[0]) / panel.step > 6 else 1)
        parts.append(scale_ticks(scale, step, top, bottom, labels_at=bottom + 18))
        for r_index, ref in enumerate(panel.refs):
            binding = RC.svg_binding(claim_id, ref.record_id) if ref.record_id else ""
            parts.append(ref_line(scale, ref.position(), top - 4, bottom, dash=ref.dash, colour=ref.colour,
                                  binding=binding))
            x = scale(ref.position())
            anchor = "middle"
            if x - scale.x0 < 40:
                anchor = "start"
            elif scale.x1 - x < 40:
                anchor = "end"
            parts.append(svg_text(x, label_y - (len(panel.refs) - 1 - r_index) * (17 if compact else 0), ref.text(),
                                  anchor=anchor, fill=ref.colour, extra=binding))

    # ---- desktop
    if has_interval:
        value_w = 196
        y = 0.0
        for panel in panels:
            x0, x1 = label_width + 8, DESKTOP_W - value_w - 8
            scale = Scale(panel.scale_id, panel.domain[0], panel.domain[1], x0, x1, _check_panel_units(panel))
            parts.append(svg_text(0, y + 16, panel.title, weight="600"))
            parts.append(svg_text(0, y + 34, panel.subtitle, fill=TOKENS["text-2"]))
            top = y + 62
            bottom = top + len(panel.rows) * row_h
            refs_and_ticks(panel, scale, top, bottom, y + 54, False)
            for index, row in enumerate(panel.rows):
                cy = top + index * row_h + row_h / 2
                record = R.get(row.record_id)
                parts.append(svg_text(0, cy + 4.5, row.label, weight="600" if row.bold else None))
                parts.append(_interval_marks(scale, cy, record, row.role, row.claim or claim_id))
                parts.append(marker(scale(record.value), cy, row.role,
                                    extra=RC.svg_binding(row.claim or claim_id, row.record_id)))
                parts.append(_row_value_text(scale, 0, cy, row, claim_id, DESKTOP_W))
            y = bottom + 30
            for record_id in panel.exact_hi:
                parts.append(svg_text(0, y + 8, "v2 − pooled control, point-error interval, upper end in full: "
                                      + RC.svg_value(record_id, "ci_high", "exact"), weight="600",
                                      extra=RC.svg_binding("C34", record_id, "ci_high")))
                y += 26
            y += 18
        height = y
    else:
        gap = 40
        panel_w = (DESKTOP_W - label_width - gap * (len(panels) - 1)) / len(panels)
        body_top = 66
        n = len(panels[0].rows)
        body_bottom = body_top + n * row_h
        height = body_bottom + 34
        for index, row in enumerate(panels[0].rows):
            cy = body_top + index * row_h + row_h / 2
            parts.append(svg_text(0, cy + 4.5, row.label, weight="600" if row.bold else None))
        for p_index, panel in enumerate(panels):
            x0 = label_width + p_index * (panel_w + gap) + 8
            x1 = x0 + panel_w - 16
            scale = Scale(panel.scale_id, panel.domain[0], panel.domain[1], x0, x1, _check_panel_units(panel))
            parts.append(svg_text(x0 - 8, 16, panel.title, weight="600"))
            parts.append(svg_text(x0 - 8, 34, panel.subtitle, fill=TOKENS["text-2"]))
            refs_and_ticks(panel, scale, body_top, body_bottom, 54, False)
            for index, row in enumerate(panel.rows):
                cy = body_top + index * row_h + row_h / 2
                record = R.get(row.record_id)
                parts.append(marker(scale(record.value), cy, row.role,
                                    extra=RC.svg_binding(row.claim or claim_id, row.record_id)))
                if values_inline:
                    parts.append(_row_value_text(scale, scale(record.value), cy, row, claim_id, x1))
    desktop = svg_wrap(DESKTOP_W, height, "".join(parts), title=title, desc=desc, variant="d", chart_id=chart_id)

    # ---- phone: stacked panels; each row is its label (wrapped), then its mark, then its values
    parts = []
    y_cursor = 0.0
    for panel in panels:
        x0, x1 = 22.0, MOBILE_W - 18.0  # room for a centred edge tick label such as "−0.12"
        scale = Scale(panel.scale_id, panel.domain[0], panel.domain[1], x0, x1, _check_panel_units(panel))
        parts.append(svg_text(0, y_cursor + 16, panel.title, weight="600"))
        sub_lines = _wrap(panel.subtitle, MOBILE_LINE_CHARS)
        for line_index, line in enumerate(sub_lines):
            parts.append(svg_text(0, y_cursor + 34 + 17 * line_index, line, fill=TOKENS["text-2"]))
        y_cursor += 17 * (len(sub_lines) - 1)
        label_y = y_cursor + 54 + (len(panel.refs) - 1) * 17
        top = label_y + 12
        layout, y = [], top
        for row in panel.rows:
            lines = _wrap(row.label, MOBILE_LINE_CHARS)
            has_ci = R.get(row.record_id).interval is not None
            y_label = y + 15
            y_mark = y_label + 17 * (len(lines) - 1) + 18
            layout.append((row, lines, y_label, y_mark))
            y = y_mark + (40 if has_ci else 26)
        bottom = y
        refs_and_ticks(panel, scale, top, bottom, label_y, True)
        for row, lines, y_label, y_mark in layout:
            record = R.get(row.record_id)
            for line_index, line in enumerate(lines):
                # reference lines cross the label line on a phone; the halo keeps the label legible
                parts.append(svg_text(0, y_label + 17 * line_index, line, weight="600" if row.bold else None,
                                      extra=' data-structural="label"' * any(c.isdigit() for c in line) + HALO))
            if record.interval is not None:
                parts.append(_interval_marks(scale, y_mark, record, row.role, row.claim or claim_id))
                parts.append(_row_value_text(scale, 0, y_mark + 19, row, claim_id, MOBILE_W, x_left=0))
            parts.append(marker(scale(record.value), y_mark, row.role,
                                extra=RC.svg_binding(row.claim or claim_id, row.record_id)))
            if record.interval is None:
                parts.append(_row_value_text(scale, scale(record.value), y_mark, row, claim_id, x1))
        y_cursor = bottom + 34
        for record_id in panel.exact_hi:
            parts.append(svg_text(0, y_cursor + 4, "v2 − pooled control, point error,", fill=TOKENS["text-2"]))
            parts.append(svg_text(0, y_cursor + 21, "upper end in full:", fill=TOKENS["text-2"]))
            parts.append(svg_text(0, y_cursor + 38, RC.svg_value(record_id, "ci_high", "exact"), weight="600",
                                  extra=RC.svg_binding("C34", record_id, "ci_high")))
            y_cursor += 54
        y_cursor += 20
    mobile = svg_wrap(MOBILE_W, y_cursor, "".join(parts), title=title, desc=desc, variant="m", chart_id=chart_id)
    return f'<div class="chart" data-chart-id="{chart_id}">{desktop}{mobile}</div>'


@dataclass(frozen=True)
class MultiRow:
    """A row holding one mark per generation, with its own or a shared scale."""

    label: str
    marks: tuple[tuple[str, str], ...]  # (role, record_id)
    domain: tuple[float, float] | None = None
    ref: Ref | None = None


def multi_rows(chart_id: str, claim_id: str, panels: list[tuple[str, str, tuple[MultiRow, ...], tuple[float, float] | None, float]],
               *, title: str, desc: str, scale_note: str | None = None) -> str:
    """Rows with a mark per generation and a printed values line under each row. A panel with a
    domain shares one scale; a panel whose domain is None gives each row its own labelled scale."""
    roles_short = {"v1": "v1", "v2": "v2", "v3": "v3", "study": "A1", "reference": "ref"}

    def draw(width: float, x_label: float, x0: float, x1: float, panel, top: float, row_h: float,
             label_above: bool) -> tuple[str, float]:
        title_text, subtitle, rows, domain, step = panel
        out = [svg_text(x_label, top + 16, title_text, weight="600"),
               svg_text(x_label, top + 34, subtitle, fill=TOKENS["text-2"])]
        y = top + 50
        for index, row in enumerate(rows):
            record_ids = [record_id for _, record_id in row.marks]
            unit = axis_unit(record_ids + ([row.ref.record_id] if row.ref and row.ref.record_id else []))
            lo, hi = domain if domain is not None else row.domain
            scale = Scale(f"{chart_id}-{index}" if domain is None else "x", lo, hi, x0, x1, unit)
            y_label = y + 14 + (10 if row.ref is not None else 0)
            y_mark = y_label + (18 if label_above else 0)
            out.append(svg_text(x_label, y_label + (0 if label_above else 4.5), row.label, weight="600"))
            out.append(f'<line x1="{x0:.1f}" x2="{x1:.1f}" y1="{y_mark:.1f}" y2="{y_mark:.1f}" stroke="{TOKENS["grid"]}" stroke-width="1"/>')
            if domain is None:
                out.append(svg_text(x0, y_mark + 17, tick_text(lo, 1), size=CHART_FONT, fill=TOKENS["text-2"],
                                    extra=f' data-scale="{scale.ident}"'))
                out.append(svg_text(x1, y_mark + 17, tick_text(hi, 1), size=CHART_FONT, anchor="end",
                                    fill=TOKENS["text-2"], extra=f' data-scale="{scale.ident}"'))
            if row.ref is not None:
                out.append(ref_line(scale, row.ref.position(), y_mark - 9, y_mark + 9, dash=None,
                                    colour=TOKENS["text"], width=2,
                                    binding=RC.svg_binding(claim_id, row.ref.record_id) if row.ref.record_id else ""))
            for role, record_id in row.marks:
                out.append(marker(scale(R.get(record_id).value), y_mark, role, extra=RC.svg_binding(claim_id, record_id)))
            # the values line
            x_text = x0
            pieces = []
            for role, record_id in row.marks:
                pieces.append((roles_short.get(role, role), record_id))
            line_y = y_mark + (34 if domain is None else 20)
            cursor = x0
            for short, record_id in pieces:
                label = svg_text(cursor, line_y, short + " ", fill=TOKENS["text-2"],
                                 extra=' data-structural="version"' if short.startswith("v") else "")
                out.append(label)
                cursor += 8 * len(short) + 6
                text = RC.svg_value(record_id)
                out.append(svg_text(cursor, line_y, text, weight="600",
                                    extra=RC.svg_binding(claim_id, record_id)))
                cursor += 7.6 * len(text) + 14
            if row.ref is not None:
                out.append(svg_text(x1, y_label - (14 if label_above else 10), row.ref.text(), anchor="end",
                                    fill=TOKENS["text-2"],
                                    extra=RC.svg_binding(claim_id, row.ref.record_id) if row.ref.record_id else ""))
            y = line_y + 16
        if domain is not None:
            scale = Scale("x", domain[0], domain[1], x0, x1, "")
            out.append(scale_ticks(scale, step, top + 50, y - 4, labels_at=y + 12, grid=False))
            y += 20
        return "".join(out), y

    desktop_parts, heights = [], []
    gap = 24
    width_each = (DESKTOP_W - gap * (len(panels) - 1)) / len(panels)
    for p_index, panel in enumerate(panels):
        x_label = p_index * (width_each + gap)
        label_w = max(72, round(8.2 * max(len(row.label) for row in panel[2])) + 14)
        body, bottom = draw(DESKTOP_W, x_label, x_label + label_w, x_label + width_each - 18, panel, 0, 0, False)
        desktop_parts.append(body)
        heights.append(bottom)
    note = svg_text(0, max(heights) + 18, scale_note, fill=TOKENS["text-2"]) if scale_note else ""
    desktop = svg_wrap(DESKTOP_W, max(heights) + (30 if scale_note else 8), "".join(desktop_parts) + note,
                       title=title, desc=desc, variant="d", chart_id=chart_id)
    mobile_parts, cursor = [], 0.0
    for panel in panels:
        body, bottom = draw(MOBILE_W, 0, 12, MOBILE_W - 16, panel, cursor, 0, True)
        mobile_parts.append(body)
        cursor = bottom + 18
    if scale_note:
        for line_index, line in enumerate(_wrap(scale_note, MOBILE_LINE_CHARS)):
            mobile_parts.append(svg_text(0, cursor + line_index * 17, line, fill=TOKENS["text-2"]))
        cursor += 17 * len(_wrap(scale_note, MOBILE_LINE_CHARS)) + 6
    mobile = svg_wrap(MOBILE_W, cursor, "".join(mobile_parts), title=title, desc=desc, variant="m", chart_id=chart_id)
    return f'<div class="chart" data-chart-id="{chart_id}">{desktop}{mobile}</div>'


def _wrap(text: str, width: int) -> list[str]:
    words, lines, line = text.split(), [], ""
    for word in words:
        if len(line) + len(word) + 1 > width and line:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    return lines + ([line] if line else [])


def hour_panels(chart_id: str, claim_id: str, series: tuple[tuple[str, str], ...], *, title: str, desc: str) -> str:
    """C5: MAE by local hour, one panel per fold, each fold on its own labelled scale."""
    folds = ("fold_1", "fold_2", "fold_3", "fold_4", "fold_5")
    windows = {fold: R.get(f"cp20.metrics.B0.{fold}.MAE").window for fold in folds}

    def draw(width: float, x0: float, x1: float, top: float, fold: str, plot_h: float) -> tuple[str, float]:
        ids = {role: [f"cp20.diagnostics.{code}.{fold}.hour_{h:02d}.MAE" for h in range(24)] for role, code in series}
        axis_unit([rid for values in ids.values() for rid in values])
        values = [R.get(rid).value for rids in ids.values() for rid in rids]
        hi = max(values) * 1.12
        step = 10 ** math.floor(math.log10(hi / 3))
        step = step * (5 if hi / step > 15 else 2 if hi / step > 6 else 1)
        y_scale = Scale(f"{chart_id}-{fold}", 0, math.ceil(hi / step) * step, top + 30 + plot_h, top + 30, "EUR/MWh")
        x_scale = Scale(f"{chart_id}-hour", 0, 23, x0, x1, "hour")
        window = windows[fold]
        out = [f'<text x="0" y="{top + 16:.1f}" font-size="{CHART_FONT}" font-weight="600" fill="{TOKENS["text"]}">'
               f'<tspan data-structural="fold">Fold {fold[-1]}</tspan> · '
               f'<tspan data-structural="date">{esc(window[0])} to {esc(window[1])}</tspan></text>']
        for tick in y_scale.ticks(y_scale.hi / 2 if y_scale.hi / step > 4 else step):
            y = y_scale(tick)
            out.append(f'<line x1="{x0:.1f}" x2="{x1:.1f}" y1="{y:.1f}" y2="{y:.1f}" stroke="{TOKENS["grid"]}"/>')
            out.append(svg_text(x0 - 6, y + 4.5, tick_text(tick, 1), anchor="end", fill=TOKENS["text-2"],
                                extra=f' data-scale="{y_scale.ident}"'))
        for hour in (0, 6, 12, 18, 23):
            out.append(svg_text(x_scale(hour), top + 30 + plot_h + 17, str(hour), anchor="middle",
                                fill=TOKENS["text-2"], extra=f' data-scale="{x_scale.ident}"'))
        for role, code in series:
            colour = ROLE_STYLE[role]["color"]
            dash = ' stroke-dasharray="5 3"' if role == "v2" else ""
            points = " ".join(f"{x_scale(h):.1f},{y_scale(R.get(rid).value):.1f}" for h, rid in enumerate(ids[role]))
            out.append(f'<polyline points="{points}" fill="none" stroke="{colour}" stroke-width="1.6"{dash}/>')
            for h, rid in enumerate(ids[role]):
                out.append(marker(x_scale(h), y_scale(R.get(rid).value), role, size=3.4,
                                  extra=RC.svg_binding(claim_id, rid)))
        ends = sorted(((y_scale(R.get(ids[role][-1]).value), role) for role, _ in series))
        for index in range(1, len(ends)):
            if ends[index][0] - ends[index - 1][0] < 15:
                ends[index] = (ends[index - 1][0] + 15, ends[index][1])
        for y_end, role in ends:
            out.append(svg_text(x1 + 8, y_end + 4.5, role, weight="600", fill=ROLE_STYLE[role]["color"],
                                extra=' data-structural="version"'))
        return "".join(out), top + 30 + plot_h + 30

    parts, cursor = [], 0.0
    for fold in folds:
        body, cursor = draw(DESKTOP_W, 48, DESKTOP_W - 40, cursor, fold, 90)
        parts.append(body)
    parts.append(svg_text(0, cursor + 14, "x: local delivery hour (Europe/Berlin) · y: MAE, EUR/MWh · each fold on its own scale",
                          fill=TOKENS["text-2"]))
    desktop = svg_wrap(DESKTOP_W, cursor + 24, "".join(parts), title=title, desc=desc, variant="d", chart_id=chart_id)
    parts, cursor = [], 0.0
    for fold in folds:
        body, cursor = draw(MOBILE_W, 44, MOBILE_W - 34, cursor, fold, 96)
        parts.append(body)
    for index, line in enumerate(_wrap("x: local delivery hour · y: MAE, EUR/MWh · each fold on its own scale", MOBILE_LINE_CHARS)):
        parts.append(svg_text(0, cursor + 14 + index * 17, line, fill=TOKENS["text-2"]))
    mobile = svg_wrap(MOBILE_W, cursor + 54, "".join(parts), title=title, desc=desc, variant="m", chart_id=chart_id)
    return f'<div class="chart" data-chart-id="{chart_id}">{desktop}{mobile}</div>'


# --------------------------------------------------------------------------- the v1 preview (§8.1)


def build_chart_payload() -> dict:
    """Precompute the nine quantiles per hour at each load-scale point (v1's fan chart)."""
    champion = load_champion()
    snapshot = load_snapshot()
    target = default_target_day(snapshot)
    actual = actuals_for_day(snapshot, target)

    series: dict[str, list[list[float]]] = {}
    for scale in LOAD_SCALES:
        forecast = forecast_delivery_day(champion, snapshot, target, load_scale=scale)
        series[f"{scale:.2f}"] = [
            [float(row[label]) for label in QUANTILE_LABELS] for _, row in forecast.iterrows()
        ]
        if scale == 1.00:
            hours = [int(value) for value in forecast["local_hour"]]

    flat = [value for rows in series.values() for row in rows for value in row]
    flat += [float(value) for value in actual.to_numpy()]
    low, high = min(flat), max(flat)
    pad = (high - low) * 0.06
    return {
        "delivery_day": target.isoformat(),
        "hours": hours,
        "labels": list(QUANTILE_LABELS),
        "levels": {str(level): list(pair) for level, pair in INTERVAL_LEVELS.items()},
        "scales": [f"{scale:.2f}" for scale in LOAD_SCALES],
        "series": series,
        "actual": [float(value) for value in actual.to_numpy()],
        "domain": [low - pad, high + pad],
    }


def preview_chart(payload: dict) -> str:
    """A static rendering of v1's saved historical replay: the default day, ×1.00, 80% (P05).
    Its numbers are the replay's own axis; nothing here is a research claim."""
    rows = payload["series"]["1.00"]
    labels = payload["labels"]
    lo_label, hi_label = payload["levels"]["80"]
    li, hi, mi = labels.index(lo_label), labels.index(hi_label), labels.index("p50")
    n = len(payload["hours"])
    lo, top = payload["domain"]

    def draw(width: float, height: float, ml: float, variant: str) -> str:
        mr, mt, mb = 12, 30, 34
        x = lambda i: ml + (width - ml - mr) * (i / (n - 1))  # noqa: E731
        y = lambda v: mt + (height - mt - mb) * (1 - (v - lo) / (top - lo))  # noqa: E731
        span, raw = top - lo, (top - lo) / 5
        magnitude = 10 ** math.floor(math.log10(raw))
        step = next(m * magnitude for m in (1, 2, 2.5, 5, 10) if m * magnitude >= raw)
        out = []
        tick = math.ceil(lo / step) * step
        while tick <= top:
            out.append(f'<line x1="{ml}" x2="{width - mr}" y1="{y(tick):.1f}" y2="{y(tick):.1f}" stroke="{TOKENS["grid"]}"/>')
            out.append(svg_text(ml - 6, y(tick) + 4.5, tick_text(tick, 1), anchor="end", fill=TOKENS["text-2"],
                                extra=' data-scale="preview-price"'))
            tick += step
        for i in range(0, n, 6 if variant == "m" else 3):
            out.append(svg_text(x(i), height - 12, str(payload["hours"][i]), anchor="middle", fill=TOKENS["text-2"],
                                extra=' data-scale="preview-hour"'))
        band = [f"{x(i):.1f},{y(rows[i][hi]):.1f}" for i in range(n)] + \
               [f"{x(i):.1f},{y(rows[i][li]):.1f}" for i in reversed(range(n))]
        out.append(f'<polygon points="{" ".join(band)}" fill="{TOKENS["v1"]}" fill-opacity="0.18"/>')
        median = " ".join(f"{x(i):.1f},{y(rows[i][mi]):.1f}" for i in range(n))
        out.append(f'<polyline points="{median}" fill="none" stroke="{TOKENS["v1"]}" stroke-width="2.4"/>')
        actual = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(payload["actual"]))
        out.append(f'<polyline points="{actual}" fill="none" stroke="{TOKENS["text"]}" stroke-width="1.6" stroke-dasharray="6 4"/>')
        out.append(f'<text x="{ml}" y="16" font-size="{CHART_FONT}" fill="{TOKENS["text-2"]}">EUR/MWh · local hour · '
                   f'<tspan data-structural="date">{esc(payload["delivery_day"])}</tspan></text>')
        return "".join(out)

    title = "v1 historical replay: the default delivery day"
    desc = ("Static rendering of v1's saved historical replay for one holdout delivery day at the unperturbed "
            "load scenario: the median forecast, the 80 percent interval as a shaded band, and the price that "
            "actually cleared as a dashed line. Not a live forecast.")
    desktop = svg_wrap(440, 270, draw(440, 270, 42, "d"), title=title, desc=desc, variant="d", chart_id="preview")
    mobile = svg_wrap(MOBILE_W, 240, draw(MOBILE_W, 240, 40, "m"), title=title, desc=desc, variant="m",
                      chart_id="preview")
    return f'<div class="chart preview-chart" data-chart-id="preview">{desktop}{mobile}</div>'


# --------------------------------------------------------------------------- lineage (§7.7) and planned work (§8.6)


def lineage() -> str:
    """The main line of adopted generations, in plain words; canonical names stay in the chapters."""
    main = [
        ("v1", "released model", "The released demo", "#v1", "v1"),
        ("v2", "a new forecasting approach", "Blended LEAR, hour-aware intervals · adopted in research", "#v2", "v2"),
        ("v3", "adds weather inputs", "Adopted in research · not in the demo", "#v3", "v3"),
    ]
    nodes = "".join(
        f'<li class="node node-{role}"><a href="{href}"><span class="dot" aria-hidden="true"></span>'
        f'<span class="node-name">{ver(label)} · {esc(name)}</span>'
        f'<span class="node-status">{esc(status)}</span></a></li>'
        for label, name, status, href, role in main
    )
    branches = (
        f'<p class="branches-head">Experiments between {ver("v1")} and {ver("v2")}</p>'
        '<ul class="branches" aria-label="Experiments that informed the decisions">'
        f'<li class="branch"><a href="#road-to-v2"><span class="branch-name">Calibration experiment</span>'
        f'<span class="branch-status">{esc(RC.NOT_ADOPTED)} · recalibrating {ver("v1")} was not enough · '
        f'{S("checkpoint", "CP-10")}</span></a></li>'
        f'<li class="branch"><a href="#road-to-v2"><span class="branch-name">Model comparison study</span>'
        f'<span class="branch-status">Informed {ver("v2")} · {S("checkpoint", "CP-15")}</span></a></li></ul>'
    )
    return (
        f'<div class="lineage"><p class="lineage-caption">{ver("v1")} is the released demo. {ver("v2")} changed the '
        f'forecasting approach; {ver("v3")} added weather inputs. The branches show experiments that informed those '
        "decisions.</p>"
        f'<ol class="mainline" aria-label="Adopted generations, oldest first">{nodes}</ol>{branches}</div>'
    )


#: Descriptive names first; work-item numbers and prerequisites are the detail layer.
PLANNED_WORK = (
    ("Alternative model families", "4.6", "DDNN / TabPFN",
     "Does a distributional network, or a tabular foundation model, beat v3?",
     "A licence and resource entry, then one predefined comparison"),
    ("Wind and solar generation forecasts", "4.4V", "VRE",
     "Does an in-house wind and solar generation forecast add information beyond direct weather?",
     "A held-forward generation model, then an ablation"),
    ("Models for different parts of the day", "4.5", "Three-block LightGBM",
     "Does capacity per block help?", "A per-block comparison"),
    ("Combining models", "4.8", "Recombination", "Does combining adopted models help?",
     "A predefined combination test"),
    ("Fresh-data evaluation, then live operation", "4.7T and live", "Final evaluation",
     "How does the final model perform on data that was never used?",
     "The final fresh-data test, then at least 90 live days"),
)


def planned_work() -> str:
    items = "".join(
        f'<li class="planned-item"><p class="planned-name">{esc(name)}</p>'
        f'<dl><dt>Question it will test</dt><dd>{_structural_versions(question)}</dd>'
        f'<dt>Evidence that would decide it</dt><dd>{_structural_versions(evidence)}</dd>'
        f'<dt>Work item</dt><dd>{S("work-item", item)} · {esc(code)}</dd></dl></li>'
        for name, item, code, question, evidence in PLANNED_WORK
    )
    teaser = ("Next, we will test alternative models, renewable-generation forecasts and model combinations, "
              "followed by evaluation on fresh data. These steps are planned, not evaluated.")
    body = (
        "<p>Each item is subject to the active plan and would be compared with the current research model on "
        "identical hours and information. None has a score, a version number or a date.</p>"
        f'<ol class="planned-list">{items}</ol>'
    )
    return (
        '<section class="planned" aria-labelledby="planned-h" data-research="planned">'
        f'<h3 id="planned-h">{esc(RC.PLANNED)}</h3><p>{esc(teaser)}</p>'
        + disclosure("planned-detail", "See planned experiments", body) + "</section>"
    )


_VERSION_WORD = re.compile(r"\b(v\d)\b")
_BARE_NUMBER = re.compile(r"\b(\d+)\b")


_ISO_DATE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")


def _structural_versions(text: str) -> str:
    """Declare version labels, dates and plain counts in fixed copy as structural numerals."""
    escaped = esc(text)
    escaped = _ISO_DATE.sub(lambda m: S("date", m.group(1)), escaped)
    escaped = re.sub(r"(?<![\d>-])((?:19|20)\d{2})(?![\d-])", lambda m: S("date", m.group(1)), escaped)
    escaped = _VERSION_WORD.sub(lambda m: ver(m.group(1)), escaped)
    escaped = re.sub(r"(?<![\w.])(\d{2})%", lambda m: S("level", m.group(1) + "%"), escaped)
    return re.sub(r"(?<![\w>\"-])(\d+)(?= live days)", lambda m: S("count", m.group(1)), escaped)


# --------------------------------------------------------------------------- system view (§7.9)


def system_view() -> str:
    steps = [
        ("Source data and vintages", "ENTSO-E and SMARD prices and load forecasts; for v3, the GFS weather run of the "
         "day before", "implemented"),
        ("Information cutoff", "Only information available before the day-ahead auction; delivery-day prices never "
         "enter", "implemented"),
        ("Features", "Calendar, price lags, load forecast; weather for v3", "implemented"),
        ("Model and interval policy", "v1: LightGBM quantiles with conformal calibration; v2 and v3: blended LEAR "
         "with hour-aware residual intervals", "implemented"),
        ("Evaluation and artifacts", "Five historical test periods, the same hours for every policy; committed "
         "predictions, metrics and reviews", "implemented"),
        ("Report, demo and tracking", "This page, the in-browser v1 demo, and the MLflow mirror of the committed "
         "evidence", "implemented"),
        ("Live operation", "Daily forecasts scored after the fact", "planned"),
    ]
    items = "".join(
        f'<li class="flow-step flow-{state}"><span class="flow-title">{esc(title)}'
        f'{" · planned" if state == "planned" else ""}</span><span class="flow-body">{_structural_versions(body)}</span></li>'
        for title, body, state in steps
    )
    audit = github("docs/data-leakage-audit.md")
    return (
        '<ol class="flow" aria-label="Data flow, from source data to report">' + items + "</ol>"
        '<p class="flow-note"><strong>The information cutoff.</strong> Inputs are restricted to what was available '
        "before the forecast's cutoff, and the price-derived features are tested with controls that fail when the "
        "boundary is crossed. Source-availability assumptions, such as when the archived load forecast was "
        f'first published, are documented rather than measured: <a class="quiet external" href="{attr(audit)}">the '
        "availability assumptions</a>. Dashed outlines mark planned parts.</p>"
    )


# --------------------------------------------------------------------------- charts on the page

_HG_MAE = "cp20.uncertainty.HG-H0.equal_fold.MAE"
_HG_WIS = "cp20.uncertainty.HG-H0.equal_fold.WIS"
FOLDS = ("fold_1", "fold_2", "fold_3", "fold_4", "fold_5")

OVERVIEW_ROWS = (
    ("HG", "v3", "v3 · weather features", True),
    ("H0", "v2", "v2 · blended LEAR, hour-aware intervals", True),
    ("B2", "reference", "Daily LEAR (reference)", False),
    ("A1", "study", "Normalized LEAR (study challenger)", False),
    ("B3", "reference", "Daily LightGBM (reference)", False),
    ("B1", "v1", "v1 · released LightGBM (development replay)", True),
    ("B0", "reference", "Similar-day naive (normalizer)", False),
)


def overview_chart() -> str:
    def panel(field: str, title: str, limit: str) -> Panel:
        return Panel(
            title=title, subtitle="ratio to the naive · lower is better",
            rows=tuple(Row(label, f"cp20.metrics.{code}.equal_fold.{field}", role, code, bold)
                       for code, role, label, bold in OVERVIEW_ROWS),
            domain=(0.5, 1.1), step=0.1,
            refs=(Ref("naive {v}", f"cp20.metrics.B0.equal_fold.{field}", dash=None, colour=TOKENS["text"], option="p=2"),
                  Ref("limit {v}", limit)),
        )

    return single_rows(
        "overview", "P07",
        [panel("S_MAE", "Point forecast error (S_MAE)", "cp20.criteria.HG.c1.equal_fold.S_MAE.upper_limit"),
         panel("S_WIS", "Interval quality (S_WIS)", "cp20.criteria.HG.c2.equal_fold.S_WIS.upper_limit")],
        title="Equal-fold point and interval error of the seven policies, relative to the similar-day naive",
        desc="Two dot plots with one row per policy in the same order. Lower is better. The solid line marks the "
             "naive at one, a reference and not a target; the dashed line marks the plan's diagnostic limit.",
        label_width=262,
    )


def overview_table() -> str:
    rows = []
    for code, role, label, bold in OVERVIEW_ROWS:
        cells = [f'<th scope="row">{_structural_versions(label)} <span class="code">{S("code", code)}</span></th>']
        for field in ("S_MAE", "S_WIS"):
            cells.append(f'<td class="n">{value(f"cp20.metrics.{code}.equal_fold.{field}", "P07")}</td>')
        for field in ("MAE", "WIS"):
            cells.append(f'<td class="n">{value(f"cp20.metrics.{code}.pooled.{field}", "C74")}</td>')
        rows.append("<tr>" + "".join(cells) + "</tr>")
    return (
        '<div class="scroll" role="region" aria-label="The seven policies, table" tabindex="0"><table class="data">'
        "<caption>Equal-fold scores (ratio to the naive) and pooled scores (EUR/MWh), identical hours</caption>"
        '<thead><tr><th scope="col">Policy</th><th scope="col">S_MAE</th><th scope="col">S_WIS</th>'
        '<th scope="col">Pooled MAE, EUR/MWh</th><th scope="col">Pooled WIS, EUR/MWh</th></tr></thead>'
        f"<tbody>{''.join(rows)}</tbody></table></div>"
    )


def fold_table() -> str:
    rows = []
    for fold in FOLDS:
        record = R.get(f"cp20.metrics.B0.{fold}.n_hours")
        first, last = record.window
        crisis = " (the 2022 crisis)" if fold == "fold_3" else ""
        rows.append(
            f'<tr><th scope="row">{S("fold", "Fold " + fold[-1])}{_structural_versions(crisis).replace("2022", S("date", "2022"))}</th>'
            f'<td>{S("date", first)} to {S("date", last)}</td>'
            f'<td class="n">{value(f"cp20.metrics.B0.{fold}.n_days", "P08")}</td>'
            f'<td class="n">{value(f"cp20.metrics.B0.{fold}.n_hours", "P08")}</td></tr>'
        )
    return (
        '<div class="scroll" role="region" aria-label="Development folds" tabindex="0"><table class="data">'
        '<thead><tr><th scope="col">Fold</th><th scope="col">Delivery days</th><th scope="col">Days</th>'
        f'<th scope="col">Hours</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
    )


def c2a_panels() -> list[Panel]:
    return [Panel("Difference, v3 − v2", "normalized score · negative favours v3",
                  (Row("Point error (ΔS_MAE)", _HG_MAE, "v3", bold=True, claim="C69"),
                   Row("Interval score (ΔS_WIS)", _HG_WIS, "v3", bold=True, claim="C70")),
                  domain=(-0.12, 0.02), step=0.02,
                  refs=(Ref("no difference", at=0.0, dash=None, colour=TOKENS["text"]),))]


def c2a_chart() -> str:
    return single_rows(
        "v3-c2a", "C69", c2a_panels(),
        title="v3 minus v2: equal-fold normalized differences with 95 percent confidence intervals",
        desc="Two rows, point error and interval score. Each shows the estimated difference as a dot and its "
             "95 percent confidence interval as a line; both lie wholly left of zero, which favours v3.",
        label_width=230, row_h=56,
    )


def c2b_panels() -> list[Panel]:
    def panel(metric: str, title: str) -> Panel:
        return Panel(title, "EUR/MWh, paired mean daily loss · negative favours v3",
                     tuple(Row(f"Fold {fold[-1]}" + (" (crisis)" if fold == "fold_3" else ""),
                               f"cp20.uncertainty.HG-H0.{fold}.{metric}", "v3") for fold in FOLDS),
                     domain=(-7.0, 1.0), step=1.0,
                     refs=(Ref("no difference", at=0.0, dash=None, colour=TOKENS["text"]),))
    return [panel("MAE", "Point error, v3 − v2"), panel("WIS", "Interval score, v3 − v2")]


def c2b_chart() -> str:
    return single_rows(
        "v3-c2b", "C72", c2b_panels(),
        title="v3 minus v2 per fold, in EUR/MWh, with 95 percent confidence intervals",
        desc="Five folds in two panels. Every point estimate is below zero. In fold 3, the 2022 crisis, the "
             "point-error interval crosses zero.",
        label_width=128, row_h=54,
    )


def c3_panels():
    def rows(metric: str) -> tuple[MultiRow, ...]:
        out = []
        for fold in FOLDS:
            ids = {role: f"cp20.metrics.{code}.{fold}.{metric}" for role, code in (("v1", "B1"), ("v2", "H0"), ("v3", "HG"))}
            top = max(R.get(rid).value for rid in ids.values())
            magnitude = 10 ** math.floor(math.log10(top))
            hi = math.ceil(top * 1.08 / magnitude * 2) * magnitude / 2
            out.append(MultiRow(f"Fold {fold[-1]}", tuple((role, rid) for role, rid in ids.items()), domain=(0.0, hi)))
        return tuple(out)
    return [("MAE by fold, EUR/MWh", "lower is better", rows("MAE"), None, 1.0),
            ("WIS by fold, EUR/MWh", "lower is better", rows("WIS"), None, 1.0)]


def c3_chart() -> str:
    return multi_rows(
        "v3-c3", "C74", c3_panels(),
        title="MAE and WIS per fold for v1, v2 and v3",
        desc="For each fold, three markers on that fold's own scale: v1 triangle, v2 square, v3 circle, with the "
             "values printed underneath.",
        scale_note="Each fold has its own scale, shared by the three generations inside it.",
    )


def c4_panels() -> list[Panel]:
    rows_mae = (Row("v1 · released LightGBM", "cp15.peak.B1.MAE", "v1", bold=True),
                Row("Normalized LEAR (study)", "cp15.peak.A1.MAE", "study"),
                Row("v2", "cp20.criteria.H0.c4.peak.MAE", "v2", bold=True),
                Row("v3", "cp20.criteria.HG.c4.peak.MAE", "v3", bold=True))
    rows_hits = (Row("v1 · released LightGBM", "cp15.peak.B1.hit_count95", "v1", bold=True),
                 Row("Normalized LEAR (study)", "cp15.peak.A1.hit_count95", "study"),
                 Row("v2", "cp20.diagnostics.H0.peak.hit_count95", "v2", bold=True),
                 Row("v3", "cp20.diagnostics.HG.peak.hit_count95", "v3", bold=True))
    return [Panel("MAE, EUR/MWh", "lower is better", rows_mae, domain=(0.0, 300.0), step=50.0),
            Panel("Hours inside the 95% interval", "count of hours in the window", rows_hits, domain=(0.0, 420.0), step=100.0)]


def c4_chart() -> str:
    return single_rows(
        "v3-c4", "C79", c4_panels(),
        title="The 2022 crisis window: point error and hours inside the 95 percent interval",
        desc="Four policies on the matched crisis window, delivery 15 to 31 August 2022. Descriptive only.",
        label_width=210,
    )


def c6_panels():
    def rows(kind: str) -> tuple[MultiRow, ...]:
        out = []
        for level in ("50", "80", "95"):
            field = f"coverage{level}" if kind == "coverage" else f"mean_width{level}"
            marks = tuple((role, f"cp20.metrics.{code}.pooled.{field}") for role, code in (("v1", "B1"), ("v2", "H0"), ("v3", "HG")))
            ref = Ref(f"nominal {level}%", at=int(level) / 100) if kind == "coverage" else None
            out.append(MultiRow(f"{level}% interval", marks, ref=ref))
        return tuple(out)
    return [("Coverage (fraction)", "closer to nominal is better", rows("coverage"), (0.3, 1.0), 0.1),
            ("Mean interval width, EUR/MWh", "narrower at equal coverage is better", rows("width"), (0.0, 140.0), 20.0)]


def c6_chart() -> str:
    return multi_rows(
        "v3-c6", "C80", c6_panels(),
        title="Coverage and mean interval width at 50, 80 and 95 percent, pooled",
        desc="For each nominal level, coverage and mean width for v1, v2 and v3. A black tick marks the nominal "
             "coverage. Higher coverage is not better on its own if the intervals widen.",
    )


def v2_chart2_panels() -> list[Panel]:
    def panel(metric: str, title: str) -> Panel:
        return Panel(title, "normalized score · negative favours the first policy",
                     (Row("v2 − daily LEAR", f"cp16.uncertainty.V2-H-B2.equal_fold.{metric}", "v2", bold=True,
                          claim="C37"),
                      Row("v2 − pooled control", f"cp16.uncertainty.V2-H-V2-P.equal_fold.{metric}", "v2",
                          claim="C34" if metric == "MAE" else "C33"),
                      Row("control − daily LEAR", f"cp16.uncertainty.V2-P-B2.equal_fold.{metric}", "control",
                          claim="C38")),
                     domain=(-0.04, 0.01), step=0.01,
                     refs=(Ref("no difference", at=0.0, dash=None, colour=TOKENS["text"]),),
                     exact_hi=("cp16.uncertainty.V2-H-V2-P.equal_fold.MAE",) if metric == "MAE" else ())
    return [panel("MAE", "Point error (ΔS_MAE)"), panel("WIS", "Interval score (ΔS_WIS)")]


def v2_chart2() -> str:
    return single_rows(
        "v2-chart2", "C37", v2_chart2_panels(),
        title="v2's paired equal-fold differences with 95 percent confidence intervals",
        desc="Three contrasts in two panels. Against daily LEAR both intervals lie below zero. Against the pooled "
             "control the interval-score interval is below zero but the point-error interval ends just above zero, "
             "printed in full under the plot.",
        label_width=170, row_h=56,
    )


def v2_chart1_panels() -> list[Panel]:
    rows = (("V2-H", "v2", "v2 · hour-aware intervals", True), ("V2-P", "control", "v2 control · pooled intervals", False),
            ("B2", "reference", "Daily LEAR (reference)", False), ("A1", "study", "Normalized LEAR (study)", False),
            ("B3", "reference", "Daily LightGBM (reference)", False), ("B1", "v1", "v1 (development replay)", True))

    def panel(field: str, title: str, limit: str) -> Panel:
        return Panel(title, "ratio to the naive · lower is better",
                     tuple(Row(label, f"cp16.metrics.{code}.equal_fold.{field}", role, code, bold)
                           for code, role, label, bold in rows),
                     domain=(0.55, 1.1), step=0.1,
                     refs=(Ref("naive {v}", f"cp16.metrics.B0.equal_fold.{field}", dash=None, colour=TOKENS["text"], option="p=2"),
                           Ref("limit {v}", limit)))
    return [panel("S_MAE", "Point error (S_MAE)", "cp16.criteria.V2-H.c1.equal_fold.S_MAE.upper_limit"),
            panel("S_WIS", "Interval quality (S_WIS)", "cp16.criteria.V2-H.c2.equal_fold.S_WIS.upper_limit")]


def v2_chart1() -> str:
    return single_rows(
        "v2-chart1", "C31", v2_chart1_panels(),
        title="Equal-fold scores at the time of v2",
        desc="Six policies from the v2 study; both v2 arms have the lowest ratios but stay above the diagnostic limits.",
        label_width=236,
    )


# --------------------------------------------------------------------------- value tables (§7.5, review R07)


def _label(text: str) -> str:
    """Fixed table copy: versions, dates and levels, plus fold numbers and policy codes, as structural numerals."""
    out = _structural_versions(text)
    out = re.sub(r"\bFold (\d)\b", lambda m: S("fold", "Fold " + m.group(1)), out)
    return re.sub(r"\(([A-Z]\d)\)", lambda m: "(" + S("code", m.group(1)) + ")", out)


def _unit_header(record_id: str) -> str:
    return _label(R.get(record_id).unit)


def values_table(ident: str, claim_id: str, panels: list[Panel]) -> str:
    """Every plotted value of a row chart, with its interval and unit, from the same typed rows."""
    labels = [row.label for row in panels[0].rows]
    head = '<th scope="col">Row</th>' + "".join(
        f'<th scope="col">{_label(panel.title)}<br><span class="unit">{_unit_header(panel.rows[0].record_id)}</span></th>'
        for panel in panels)
    body = []
    for index, label in enumerate(labels):
        cells = [f'<th scope="row">{_label(label)}</th>']
        for panel in panels:
            row = panel.rows[index]
            record = R.get(row.record_id)
            claim = row.claim or claim_id
            text = value(row.record_id, claim)
            if record.interval is not None:
                text += f' <span class="ci">{interval(row.record_id, claim)}</span>'
            cells.append(f'<td class="n exact">{text}</td>')
        body.append("<tr>" + "".join(cells) + "</tr>")
    table_html = (f'<div class="scroll" role="region" aria-label="Values" tabindex="0"><table class="data">'
                  f"<thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table></div>")
    return disclosure(ident, "View values", table_html)


def multi_values_table(ident: str, claim_id: str, panels) -> str:
    parts = []
    for title, _subtitle, rows, _domain, _step in panels:
        roles = [role for role, _ in rows[0].marks]
        head = '<th scope="col">Row</th>' + "".join(f'<th scope="col">{ver(role) if role.startswith("v") else esc(role)}</th>'
                                                    for role in roles)
        body = "".join(
            f'<tr><th scope="row">{_label(row.label)}</th>'
            + "".join(f'<td class="n">{value(record_id, claim_id)}</td>' for _, record_id in row.marks) + "</tr>"
            for row in rows)
        parts.append(f'<div class="scroll" role="region" aria-label="{attr(title)}" tabindex="0"><table class="data">'
                     f"<caption>{_label(title)}</caption><thead><tr>{head}</tr></thead>"
                     f"<tbody>{body}</tbody></table></div>")
    return disclosure(ident, "View values", "".join(parts))


def hour_values_table(ident: str, claim_id: str, series: tuple[tuple[str, str], ...]) -> str:
    head = '<th scope="col">Hour</th>' + "".join(
        f'<th scope="col">{S("fold", "Fold " + fold[-1])} {ver(role)}</th>' for fold in FOLDS for role, _ in series)
    body = []
    for hour in range(24):
        cells = "".join(f'<td class="n">{value(f"cp20.diagnostics.{code}.{fold}.hour_{hour:02d}.MAE", claim_id)}</td>'
                        for fold in FOLDS for _, code in series)
        body.append(f'<tr><th scope="row">{S("hour", str(hour))}</th>{cells}</tr>')
    table_html = ('<div class="scroll" role="region" aria-label="MAE by hour and fold" tabindex="0"><table class="data">'
                  "<caption>MAE by local hour, EUR/MWh</caption>"
                  f"<thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table></div>")
    return disclosure(ident, "View values", table_html)


def legend(roles: tuple[str, ...]) -> str:
    names = {"v1": "v1 · released", "v2": "v2", "v3": "v3", "reference": "reference", "study": "study arm",
             "control": "control arm"}
    items = []
    for role in roles:
        svg = (f'<svg class="legend-mark" viewBox="-8 -8 16 16" width="16" height="16" aria-hidden="true">'
               f'{marker(0, 0, role, size=5)}</svg>')
        items.append(f'<li>{svg}<span>{_structural_versions(names[role])}</span></li>')
    return '<ul class="legend" aria-label="Marker key">' + "".join(items) + "</ul>"


# --------------------------------------------------------------------------- sections


def demo_measurement() -> dict:
    record = json.loads(DEMO_CHECK.read_text())
    run = next(r for r in record["runs"] if r.get("engine") == "chrome" and r.get("viewport") == "1440x900")
    host = record["playwright_host"]
    return {"seconds": run["seconds_to_visible_forecast"], "browser": run["browser_version"],
            "machine": "a Mac" if "Darwin" in host else host,
            "date": record["date"], "path": str(DEMO_CHECK.relative_to(ROOT))}


def header() -> str:
    return (
        '<header class="site-header"><div class="header-inner">'
        '<a class="brand" href="#top" aria-label="DE-LU day-ahead price forecasting, back to the top">'
        '<span class="brand-full">DE-LU day-ahead price forecasting</span>'
        '<span class="brand-short" aria-hidden="true">DE-LU forecasts</span>'
        '<span class="brand-tiny" aria-hidden="true">DE-LU</span></a>'
        '<nav class="main-nav" aria-label="Main"><a href="#research-results">Results</a><a href="#journey">Journey</a>'
        '<a href="#evidence">Evidence</a></nav></div></header>'
    )


def opening(C, payload) -> str:
    demo = demo_measurement()
    measured = (f'<span data-release-check="{attr(demo["path"])}#seconds_to_visible_forecast">'
                f'{esc(demo["seconds"])}</span>')
    details = (
        f"<p>The demo runs the released model on historical delivery days. Change the interval level or load "
        f"scenario to explore its forecasts. Calculations run locally in your browser. In the recorded cold-start "
        f"test, a forecast appeared after {measured} seconds in Chrome {S('version', demo['browser'].split('.')[0])} "
        f"on {esc(demo['machine'])}, measured {S('date', demo['date'])}. Other devices and connections may take longer.</p>"
    )
    return f"""
<section class="opening" id="top" aria-labelledby="title">
 <div class="opening-copy">
  <p class="eyebrow">German–Luxembourg electricity market</p>
  <h1 id="title">Day-ahead electricity forecasts, with uncertainty.</h1>
  <p class="lede">Explore hourly price forecasts and prediction intervals on historical days. See how successive
   research models improved, what failed, and how each result was checked.</p>
  <dl class="status-pair">
   <div class="status status-released"><dt>Demo</dt><dd><span class="gen gen-v1">{ver("v1")}</span> · Released model</dd></div>
   <div class="status status-research"><dt>Research</dt><dd><span class="gen gen-v3">{ver("v3")}</span> · Weather features
    {badge(RC.BADGE_DEVELOPMENT)}</dd></div>
  </dl>
  <div class="actions">
   <a class="btn-primary external" href="{attr(C['space_url'])}"><span>Try the {ver("v1")} demo</span></a>
   <a class="quiet" href="#research-results">Compare model results</a>
   <a class="quiet" href="#evidence">Code and evidence</a>
  </div>
  <p class="startup">Runs in your browser. First visit downloads about {v1("wasm_cold_load_mb", "P13")} MB; startup
   time varies.</p>
  {disclosure("demo-details", "What the demo does and startup details", details)}
 </div>
 <figure class="preview panel">
  <figcaption class="preview-label"><span class="badge badge-replay">Historical forecast · {ver("v1")}</span>
   <span>Forecast and observed price for a held-out day. This is a historical replay, not a live forecast.</span></figcaption>
  {preview_chart(payload)}
  <p class="preview-key"><span class="key-median">Median forecast</span> <span class="key-band">{S("level", "80%")} prediction interval</span>
   <span class="key-actual">Observed price</span></p>
  <p class="preview-links"><a class="quiet" href="#forecast">Explore this forecast</a>
   <span class="preview-note">Opens the replay in the original {ver("v1")} report.</span></p>
 </figure>
 <div class="opening-summary" data-research="opening"><p class="summary-label">Latest research</p>{block("opening.summary")}</div>
</section>"""


def results() -> str:
    hours = value("cp20.metrics.B0.pooled.n_hours", "P07")
    return f"""
<section class="section" id="research-results" aria-labelledby="results-h" data-research="results">
 <h2 id="results-h">How the models compare</h2>
 <figure class="panel analytical" aria-labelledby="overview-title">
  {block("overview.finding", tag="h3", cls="panel-title")}
  <p class="panel-sub">Point-error and interval scores relative to a simple similar-day forecast · the same {hours}
   hours for every policy · development results after selection</p>
  {legend(("v3", "v2", "v1", "reference", "study"))}
  {overview_chart()}
  {block("overview.howto", cls="finding")}
  {block("overview.qualification", cls="qualification")}
  {block("overview.v1pointer", cls="qualification")}
  {evidence_row(compare="overview", review=("Read the review", github("docs/track-b/evidence/cp-20/integration.md")),
                source=("View source values", github("reports/weather-ablation/metrics.csv", "evidence/cp-20", 44)))}
  {disclosure("overview-table", "View values", overview_table())}
 </figure>
 <div class="fairness">
  <h3>A fair comparison</h3>
  {block("overview.fairness")}
  {disclosure("fairness-detail", "Bootstrap settings and the five historical test periods",
              block("overview.fairness.detail") + fold_table())}
 </div>
 {disclosure("definitions", "Definitions, and why v1 scores differently in its own report",
             block("overview.definitions") + block("overview.f07"))}
</section>"""


def chapter_header(gen: str, name: str, when: str, adoption_text: str, badge_text: str | None, badge_kind: str,
                   ident: str) -> str:
    badge_html = badge(badge_text, badge_kind) if badge_text else ""
    return (
        f'<header class="chapter-head"><p class="eyebrow">{_structural_versions(when)}</p>'
        f'<h2 id="{ident}-h"><span class="gen gen-{gen}">{ver(gen)}</span> · {esc(name)}</h2>'
        f'<p class="chapter-meta">{adoption(adoption_text)}{badge_html}</p></header>'
    )


def story(steps: list[tuple[str, str]]) -> str:
    return '<ol class="story">' + "".join(
        f'<li class="story-step"><h3 class="story-label">{esc(label)}</h3>{body}</li>' for label, body in steps
    ) + "</ol>"


def feature_change() -> str:
    return (
        '<div class="feature-change" aria-label="What changed from v2 to v3">'
        f'<div class="fc-col"><p class="fc-head">{ver("v2")} inputs</p><ul><li>price history</li>'
        "<li>load forecast</li><li>calendar</li></ul></div>"
        '<div class="fc-arrow" aria-hidden="true">+</div>'
        f'<div class="fc-col fc-added"><p class="fc-head">added in {ver("v3")}</p><ul>'
        f'<li>wind speed at {S("height", "10 m")}</li><li>wind speed at {S("height", "100 m")}</li>'
        '<li>solar radiation</li></ul><p class="fc-note">each with a missing-data indicator</p></div></div>'
    )


def v3_chapter(*, open_folds: bool = False) -> str:
    cp20 = "evidence/cp-20"
    protocol = "".join(block(key) for key in ("v3.criteria", "v3.controls", "v3.controls.supplement", "v3.review",
                                              "v3.cost", "v3.dependency"))
    protocol += f'<p class="attribution-line"><span data-structural="attribution">{esc(GFS_ATTRIBUTION)}</span></p>'
    folds = (c2b_chart() + values_table("v3-c2b-values", "C72", c2b_panels())
             + '<p class="chart-note">' + _structural_versions("The same periods in absolute terms, for v1, v2 and v3:")
             + "</p>" + c3_chart() + multi_values_table("v3-c3-values", "C74", c3_panels()))
    crisis_note = ('<p class="chart-note">' + _structural_versions(
        "The crisis window, delivery 2022-08-15 to 2022-08-31, is the 17 days of the 2022 price peak inside fold 3; "
        "its figures are for those days only, not the whole fold.").replace("17 days", S("count", "17") + " days")
        .replace("fold 3", "fold " + S("fold", "3")) + "</p>")
    return f"""
<article class="chapter" id="v3" aria-labelledby="v3-h" data-research="v3">
 {chapter_header("v3", "weather features", "Latest research · evaluated 2026-09-24",
                 RC.ADOPTED + " in research · not in the demo", RC.BADGE_DEVELOPMENT, "development", "v3")}
 {block("v3.subtitle", cls="chapter-sub")}
 <div class="change"><h3 class="story-label">What changed</h3>{block("v3.change")}{feature_change()}</div>
 <figure class="panel analytical" aria-labelledby="c2a-title">
  <h3 class="panel-title" id="c2a-title">{_structural_versions("Weather inputs improved both development scores against v2.")}</h3>
  <p class="panel-sub">{_structural_versions("Difference in normalized score, v3 − v2 · paired 95% confidence interval · identical hours · development, post-selection")}</p>
  {c2a_chart()}
  {block("v3.result", cls="finding")}
  {block("v3.caveat.fold3", cls="qualification")}
  {evidence_row(compare="cp20", review=("Read the review", github("docs/track-b/evidence/cp-20/integration.md")),
                source=("View source values", github("reports/weather-ablation/uncertainty.csv", cp20, 12)),
                extra=[("Full report", github("reports/weather-ablation/report.md", cp20))])}
  {values_table("v3-c2a-values", "C69", c2a_panels())}
 </figure>
 <div class="helps-hurts">{block("v3.helps")}{block("v3.hurts")}</div>
 <aside class="caveats" aria-label="What this result does not establish">
  <h3>What this result does not establish</h3>
  {block("v3.caveat.bundle")}{block("v3.caveat.development")}
 </aside>
 <div class="decision"><h3 class="story-label">Decision</h3>{block("v3.decision")}</div>
 <div class="disclosures">
  {disclosure("v3-features", "How the weather features are built", block("v3.recipe") + block("v3.missing") + block("v3.availability"))}
  {disclosure("v3-folds", "Consistency across the five periods", folds, open_=open_folds)}
  {disclosure("v3-crisis", "Crisis window", crisis_note + c4_chart() + values_table("v3-c4-values", "C79", c4_panels()))}
  {disclosure("v3-hours", "Hours of the day", hour_panels("v3-c5", "C82", (("v2", "H0"), ("v3", "HG")),
              title="MAE by local hour, v2 against v3, per fold",
              desc="Five panels, one per fold, each on its own scale: v2 dashed with squares, v3 solid with circles. Descriptive only.")
              + '<p class="chart-note">Descriptive only: no hour or block effect is claimed.</p>'
              + hour_values_table("v3-c5-values", "C82", (("v2", "H0"), ("v3", "HG"))))}
  {disclosure("v3-coverage", "Coverage and interval width", c6_chart() + multi_values_table("v3-c6-values", "C80", c6_panels()))}
  {disclosure("v3-protocol", "Criteria, controls and review", protocol)}
 </div>
</article>"""


def v2_chapter() -> str:
    cp16 = "evidence/cp-16"
    branches = block("v2.branch.cp10") + block("v2.branch.cp15")
    scores = v2_chart1() + block("v2.result.pb2") + block("v2.result.criteria")
    return f"""
<article class="chapter" id="v2" aria-labelledby="v2-h" data-research="v2">
 {chapter_header("v2", "blended LEAR, hour-aware intervals", "Evaluated 2026-09-23 · the road from v1",
                 RC.ADOPTED + " in research · the model v3 builds on", RC.BADGE_DEVELOPMENT, "development", "v2")}
 {block("v2.subtitle", cls="chapter-sub")}
 <div class="road" id="road-to-v2">
  {story([("Problem", block("v2.problem")), ("What informed the change", block("v2.informed")),
          ("What changed", block("v2.change"))])}
 </div>
 <figure class="panel analytical" aria-labelledby="v2c2-title">
  <h3 class="panel-title" id="v2c2-title">{_structural_versions("v2 improved on daily LEAR; the interval-method comparison was inconclusive on joint improvement.")}</h3>
  <p class="panel-sub">{_structural_versions("Difference in normalized score · paired 95% confidence intervals · identical hours · development, post-selection")}</p>
  {v2_chart2()}
  {block("v2.interpretation", cls="finding")}
  {evidence_row(compare="cp16", review=("Read the review", github("docs/track-b/evidence/cp-16/integration.md")),
                source=("View source values", github("reports/v2-causal/uncertainty.csv", cp16, 32)))}
  {values_table("v2-chart2-values", "C37", v2_chart2_panels())}
 </figure>
 <aside class="caveats" aria-label="What this result does not establish"><h3>What this result does not establish</h3>
  {block("v2.limitation")}</aside>
 <div class="decision"><h3 class="story-label">Decision</h3>{block("v2.decision")}</div>
 <div class="disclosures">
  {disclosure("v2-branches", "The two branches before v2", branches)}
  {disclosure("v2-scores", "Scores and criteria at the time of v2", scores + values_table("v2-chart1-values", "C31", v2_chart1_panels()))}
 </div>
</article>"""


def v1_chapter(C, archive: str) -> str:
    return f"""
<article class="chapter" id="v1" aria-labelledby="v1-h" data-research="v1">
 {chapter_header("v1", "released LightGBM", "Released 2026-09-15 · the product the demo runs",
                 "Released model", None, "holdout", "v1")}
 {block("v1.what")}
 <div class="panel holdout">
  <p class="holdout-head">The one-shot holdout {badge(RC.BADGE_V1_HOLDOUT, "holdout")}</p>
  {block("v1.holdout")}
  <p class="holdout-label">{v1("holdout_dm_label")}</p>
 </div>
 {block("v1.unflattering")}
 {block("v1.lesson")}
 <p class="chapter-links"><a class="quiet" href="#forecast">Explore the interactive replay</a>
  <a class="quiet external" href="{attr(C['space_url'])}">Try the {ver("v1")} demo</a></p>
 <details class="disclosure archive" id="v1-archive">
  <summary><span class="marker" aria-hidden="true"></span><span>The original {ver("v1")} report (published
   {S("date", "2026-09-15")}), preserved</span></summary>
  <div class="disclosure-body">
   <p class="archive-note">Preserved as published, including its interactive fan chart. Its own styles are kept
    separate from the rest of this page. <a href="#research-results">Back to the model comparison</a></p>
   <div class="v1-archive">{archive}</div>
   <p class="archive-note"><a href="#research-results">Back to the model comparison</a> · <a href="#v1">Back to v1</a></p>
  </div>
 </details>
</article>"""


def journey() -> str:
    return f"""
<section class="section" id="journey" aria-labelledby="journey-h">
 <span id="development-update" class="anchor-alias" aria-hidden="true"></span>
 <h2 id="journey-h">How it evolved</h2>
 {lineage()}
 {planned_work()}
</section>"""


def jump_row() -> str:
    return ('<nav class="jump" aria-label="Chapters"><a href="#v3">' + ver("v3") + '</a><a href="#v2">' + ver("v2")
            + '</a><a href="#v1">' + ver("v1") + "</a></nav>")


def rail(generations: tuple[str, ...] = ("v3", "v2", "v1")) -> str:
    """The generation rail. The page's own routes live in the header only (review §5.1)."""
    links = "".join(f'<li><a href="#{g}" class="rail-{g if g in ("v1", "v2", "v3") else "x"}">'
                    f'<span class="dot" aria-hidden="true"></span>{ver(g)}</a></li>' for g in generations)
    return ('<nav class="rail" aria-label="Generations"><p class="rail-head">Generations</p><ol>' + links
            + "</ol></nav>")


def evidence_section(C) -> str:
    rebuild = rebuild_measurement()
    runtime = ""
    if rebuild:
        runtime = (f'The rebuild took <span data-release-check="{attr(rebuild["path"])}#seconds">{esc(rebuild["seconds"])}</span> s '
                   f'on the build machine ({esc(rebuild["machine"])}), measured {S("date", rebuild["date"])}.')
    tracking = mlflow_index().get("routes", {})
    if tracking.get("experiment"):
        track = (f'<p>Experiment runs, metrics and artifacts can be inspected in '
                 f'<a class="quiet external" href="{attr(tracking["experiment"])}">MLflow</a>. The published page is '
                 "built from saved repository evidence and works independently of the tracking service.</p>")
    else:
        track = ('<p>Experiment runs, metrics and artifacts will be inspectable in MLflow once they are published '
                 '<span class="ev is-unavailable" data-unpublished="mlflow:experiment">(link added when the runs '
                 "are published)</span>. This page is built from saved repository evidence and works independently "
                 "of the tracking service.</p>")
    return f"""
<section class="section" id="evidence" aria-labelledby="evidence-h">
 <h2 id="evidence-h">How the system works, and how to check it</h2>
 <div id="system" class="system"><h3>How the system works</h3>{system_view()}</div>
 <div id="reproduce" class="reproduce"><h3>Rebuild the report from saved evidence</h3>
  <p>First install the pinned dependencies; this downloads packages once:</p>
  <pre><code>uv sync</code></pre>
  <p>Then rebuild this page, the README research block, the demo's description cards and the tracking export from the
   committed evidence alone, with no model fit and no data download:</p>
  <pre><code>uv run python scripts/rebuild_presentation.py</code></pre>
  <p>{runtime} Each generation's full experiment has its own reproduction instructions:
   <a class="quiet external" href="{attr(github("reports/weather-ablation/reproduce.md", "evidence/cp-20"))}">{ver("v3")}</a>,
   <a class="quiet external" href="{attr(github("reports/v2-causal/reproduce.md", "evidence/cp-16"))}">{ver("v2")}</a>,
   <a class="quiet external" href="{attr(github("reports/cp15/reproduction.md", "evidence/cp-15"))}">the model comparison</a>,
   and <a href="#repro">{ver("v1")}</a>.</p>
 </div>
 <div class="tracking"><h3>Tracking</h3>
  {track}
  <p><a class="quiet external" href="{attr(C['mlflow_experiment_url'])}">Experiment <code>{esc(C['mlflow_experiment_name'])}</code></a>
   keeps {ver("v1")}'s own runs. <a class="quiet external" href="{attr(C['github_url'])}">Code and evidence on GitHub</a></p>
 </div>
</section>"""


def rebuild_measurement() -> dict | None:
    checks = sorted((ROOT / "reports" / "presentation" / "release-checks").glob("*-rebuild.json"))
    if not checks:
        return None
    record = json.loads(checks[-1].read_text())
    return {"seconds": record["seconds"], "machine": record["machine"], "date": record["date"],
            "path": str(checks[-1].relative_to(ROOT))}


def contribution() -> str:
    return f"""
<section class="section contribution" id="contribution" aria-labelledby="contribution-h">
 <h2 id="contribution-h">Contribution</h2>
 <blockquote class="statement"><p>{esc(RC.CONTRIBUTION_STATEMENT)}</p></blockquote>
</section>"""


def attribution(C) -> str:
    return f"""
<section class="section attribution" id="attribution" aria-labelledby="attribution-h">
 <h2 id="attribution-h">Terms and attribution</h2>
 <p>{esc(C['attribution'])}</p>
 <p>{esc(C['licensing'])}</p>
</section>"""


# --------------------------------------------------------------------------- styles (§7.3–§7.12)


def css() -> str:
    t = TOKENS
    root = ";".join(f"--{name}:{value}" for name, value in t.items())
    return f"""
:root{{{root};--font:{FONT_STACK};--mono:{MONO_STACK};--header:56px;--radius:12px;--content:1200px;--prose:66ch}}
*{{box-sizing:border-box}}
html{{scroll-padding-top:calc(var(--header) + 16px);-webkit-text-size-adjust:100%}}
body{{margin:0;background:var(--canvas);color:var(--text);font:16px/26px var(--font)}}
a{{color:var(--accent);text-underline-offset:3px}}
a:hover{{text-decoration-thickness:2px}}
:focus-visible{{outline:2px solid var(--accent);outline-offset:2px;border-radius:4px}}
[id]{{scroll-margin-top:calc(var(--header) + 16px)}}
code,pre,.code{{font-family:var(--mono);font-size:.9em}}
data{{font-variant-numeric:tabular-nums}}
.skip{{position:absolute;left:-999px;top:8px;background:var(--surface);padding:8px 12px;z-index:30}}
.skip:focus{{left:8px}}
/* header and navigation */
.site-header{{position:sticky;top:0;z-index:20;height:var(--header);background:rgba(250,250,250,.97);
 border-bottom:1px solid var(--border)}}
.header-inner{{max-width:var(--content);margin:0 auto;height:100%;display:flex;align-items:center;
 justify-content:space-between;gap:16px;padding:0 24px}}
.brand{{font-weight:650;color:var(--text);text-decoration:none;font-size:15px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.brand-short,.brand-tiny{{display:none}}
.main-nav{{display:flex;gap:4px}}
.main-nav a{{color:var(--text);text-decoration:none;font-size:15px;padding:0 12px;min-height:44px;display:inline-flex;
 align-items:center;border-radius:8px}}
.main-nav a:hover{{background:#F4F4F5}}
/* page frame */
.page{{max-width:var(--content);margin:0 auto;padding:0 24px 96px}}
.with-rail{{display:block}}
.rail{{display:none}}
@media (min-width:1280px){{
 .with-rail{{display:grid;grid-template-columns:148px minmax(0,1fr);gap:48px;align-items:start}}
 .rail{{display:block;position:sticky;top:calc(var(--header) + 32px);font-size:14px}}
 .jump{{display:none}}
}}
.rail-head{{margin:0 0 8px;color:var(--text-2);font-size:13px;text-transform:uppercase;letter-spacing:.06em}}
.rail ol{{list-style:none;margin:0 0 24px;padding:0}}
.rail a{{display:flex;align-items:center;gap:8px;min-height:36px;color:var(--text);text-decoration:none;
 padding:0 8px;border-radius:8px;border-left:3px solid transparent}}
.rail a[aria-current="true"]{{background:var(--surface);border-left-color:var(--text);font-weight:600}}
.rail .dot{{width:9px;height:9px;border-radius:50%;background:var(--ref)}}
.rail-v1 .dot{{background:var(--v1)}}.rail-v2 .dot{{background:var(--v2)}}.rail-v3 .dot{{background:var(--v3)}}
.jump{{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 24px}}
.jump a{{min-height:44px;min-width:56px;display:inline-flex;align-items:center;justify-content:center;
 border:1px solid var(--border);border-radius:999px;background:var(--surface);color:var(--text);
 text-decoration:none;font-weight:600;padding:0 16px}}
/* type */
h1{{font-size:52px;line-height:1.08;letter-spacing:-.02em;margin:12px 0 16px;max-width:18ch}}
h2{{font-size:30px;line-height:1.2;letter-spacing:-.01em;margin:0 0 24px}}
h3{{font-size:19px;line-height:1.35;margin:0 0 8px}}
p{{margin:0 0 16px;max-width:var(--prose)}}
.eyebrow{{color:var(--text-2);font-size:14px;font-weight:600;letter-spacing:.02em;margin:0 0 8px}}
.lede{{font-size:19px;line-height:30px;color:var(--text-2);max-width:48ch}}
.section{{padding:64px 0 16px;border-top:1px solid var(--border)}}
/* opening */
.opening{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.05fr);gap:48px;align-items:start;padding:48px 0 48px}}
.opening-summary{{grid-column:1 / -1;border-top:1px solid var(--border);padding-top:16px;color:var(--text-2)}}
.opening-summary p{{max-width:none}}
.status-pair{{display:flex;flex-wrap:wrap;gap:12px;margin:24px 0}}
.status{{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:10px 14px}}
.status dt{{font-size:13px;color:var(--text-2);font-weight:600}}
.status dd{{margin:0;font-size:16px;font-weight:600}}
.status .badge{{margin-left:6px;vertical-align:1px}}
.actions{{display:flex;flex-wrap:wrap;align-items:center;gap:8px 20px;margin:8px 0 12px}}
.btn-primary{{display:inline-block;line-height:48px;min-height:48px;padding:0 22px;border-radius:10px;
 background:var(--primary);color:#fff;font-weight:650;text-decoration:none;font-size:16px}}
.btn-primary:hover{{background:var(--primary-hover);color:#fff}}
.btn-primary:active{{background:var(--primary-pressed)}}
.quiet{{display:inline-block;padding:9px 0;line-height:26px;font-weight:550}}
p .quiet,li .quiet{{display:inline;padding:0;line-height:inherit}}
.branches-head{{font-size:13px;font-weight:650;text-transform:uppercase;letter-spacing:.05em;color:var(--text-2);margin:24px 0 0}}
.fc-note{{font-size:14px;color:var(--text-2);margin:6px 0 0}}
.external::after{{content:" \\2197";font-size:.85em}}
.startup{{font-size:14px;line-height:22px;color:var(--text-2);max-width:52ch}}
.preview{{margin:0}}
.preview-label{{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:center;font-size:14px;color:var(--text-2);margin-bottom:8px}}
.preview-key{{font-size:13px;color:var(--text-2);display:flex;gap:16px;flex-wrap:wrap;margin:8px 0 4px}}
.key-median::before{{content:"";display:inline-block;width:18px;height:3px;background:var(--v1);vertical-align:middle;margin-right:6px}}
.key-band::before{{content:"";display:inline-block;width:14px;height:12px;background:rgba(71,85,105,.22);vertical-align:middle;margin-right:6px}}
.key-actual::before{{content:"";display:inline-block;width:18px;border-top:2px dashed var(--text);vertical-align:middle;margin-right:6px}}
.preview-links{{display:flex;gap:4px 20px;flex-wrap:wrap;margin:0}}
/* components */
.panel{{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:24px}}
.preview.panel{{box-shadow:0 1px 2px rgba(24,24,27,.04),0 8px 24px rgba(24,24,27,.06)}}
.badge{{display:inline-block;font-size:13px;line-height:18px;font-weight:600;padding:3px 9px;border-radius:999px;
 border:1px solid #D4D4D8;background:var(--badge-bg);color:var(--badge-text);white-space:normal;max-width:100%}}
.badge-holdout{{background:var(--surface);border-color:var(--text-2);color:var(--text)}}
.badge-replay{{background:var(--surface);border-color:var(--v1);color:var(--v1)}}
.adoption{{font-weight:650;font-size:14px;color:var(--text);margin-right:10px}}
.gen{{font-weight:750;padding:0 2px;border-bottom:3px solid currentColor}}
.gen-v1{{color:var(--v1)}}.gen-v2{{color:var(--v2)}}.gen-v3{{color:var(--v3)}}
.analytical{{margin:0 0 32px}}
.panel-title{{font-size:20px;margin:0 0 4px}}
.panel-sub{{font-size:14px;line-height:22px;color:var(--text-2);margin:0 0 16px;max-width:none}}
.legend{{list-style:none;display:flex;flex-wrap:wrap;gap:6px 18px;padding:0;margin:0 0 12px;font-size:14px}}
.legend li{{display:flex;align-items:center;gap:6px}}
.finding{{font-weight:550;margin-top:16px}}
.qualification{{color:var(--text-2)}}
.evidence-row{{display:flex;flex-wrap:wrap;align-items:center;gap:4px 18px;font-size:14px;border-top:1px solid var(--border);
 padding-top:12px;margin:16px 0 0;max-width:none}}
.ev-label{{font-size:13px;font-weight:650;color:var(--text-2);text-transform:uppercase;letter-spacing:.05em}}
.ev{{min-height:32px;display:inline-flex;align-items:center}}
.ev.is-unavailable{{display:inline;color:var(--text-2)}}
.ev.is-unavailable .why{{display:inline;margin-left:4px;font-style:italic}}
details.disclosure{{border-top:1px solid var(--border);margin:0}}
details.disclosure:last-child{{border-bottom:1px solid var(--border)}}
details.disclosure>summary{{list-style:none;cursor:pointer;min-height:48px;display:flex;align-items:center;gap:10px;
 font-weight:650;padding:6px 0}}
details.disclosure>summary::-webkit-details-marker{{display:none}}
details.disclosure>summary .marker{{width:20px;height:20px;border:1px solid var(--text-2);border-radius:6px;flex:none;position:relative}}
details.disclosure>summary .marker::before,details.disclosure>summary .marker::after{{content:"";position:absolute;
 left:4px;right:4px;top:9px;height:1.5px;background:var(--text)}}
details.disclosure>summary .marker::after{{transform:rotate(90deg)}}
details.disclosure[open]>summary .marker::after{{display:none}}
.disclosure-body{{padding:4px 0 24px}}
.scroll{{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:12px 0 16px}}
table.data{{border-collapse:collapse;font-size:14px;line-height:20px;min-width:100%;font-variant-numeric:tabular-nums}}
table.data caption{{text-align:left;color:var(--text-2);font-size:13px;padding-bottom:6px}}
table.data th,table.data td{{border-bottom:1px solid var(--border);padding:8px 12px;text-align:left;vertical-align:top}}
table.data thead th{{font-size:13px;color:var(--text-2);font-weight:650;white-space:nowrap}}
table.data td.n{{text-align:right;white-space:nowrap;font-family:var(--mono);font-size:13px}}
table.data .code{{color:var(--text-2);font-size:12px;margin-left:4px}}
.exact{{overflow-wrap:anywhere;word-break:break-word}}
/* charts: a dedicated phone variant, never a shrunk desktop SVG (§7.5, invariant 23) */
.chart{{margin:8px 0}}
.chart svg{{display:block;height:auto}}
.chart svg.d{{width:100%;max-width:{DESKTOP_W}px}}
.chart svg.m{{display:none;width:100%;max-width:{MOBILE_MAX_W}px;margin:0 auto}}
.preview-chart svg.d{{max-width:440px}}
@media (max-width:{MOBILE_BREAKPOINT - 1}px){{.chart svg.d{{display:none}}.chart svg.m{{display:block}}}}
.chart-note{{font-size:14px;color:var(--text-2);margin-top:20px}}
/* lineage and planned work */
.lineage-caption{{color:var(--text-2)}}
.mainline{{list-style:none;padding:0;margin:24px 0 8px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));
 gap:0;position:relative}}
.mainline::before{{content:"";position:absolute;left:8px;right:8px;top:14px;height:3px;background:var(--text)}}
.node a{{display:block;position:relative;padding:34px 16px 0 0;color:var(--text);text-decoration:none}}
.node .dot{{position:absolute;top:6px;left:0;width:19px;height:19px;border-radius:50%;border:3px solid var(--canvas)}}
.node-v1 .dot{{background:var(--v1)}}.node-v2 .dot{{background:var(--v2);border-radius:4px}}.node-v3 .dot{{background:var(--v3)}}
.node-name{{display:block;font-weight:700;font-size:17px}}
.node-status{{display:block;font-size:14px;color:var(--text-2)}}
.branches{{list-style:none;padding:0;margin:8px 0 32px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}}
.branch a{{display:block;border:1px solid var(--border);border-radius:10px;padding:10px 12px;color:var(--text);
 text-decoration:none;background:transparent}}
.branch-name{{display:block;font-weight:600;font-size:15px}}
.branch-status{{display:block;font-size:14px;color:var(--text-2)}}
.planned{{margin:16px 0 0}}
.planned-list{{list-style:none;padding:0;margin:12px 0 0;display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}}
.planned-item{{border:1px dashed var(--text-2);border-radius:10px;padding:12px 14px}}
.planned-name{{font-weight:650;margin:0 0 6px}}
.planned-item dl{{margin:0;font-size:14px;line-height:21px}}
.planned-item dt{{color:var(--text-2);font-weight:600;font-size:13px}}
.planned-item dd{{margin:0 0 6px}}
.outcome-badge{{margin:8px 0 0}}
.planned h3{{margin-bottom:4px}}
/* chapters */
.chapters{{padding-top:32px}}
.chapter{{padding:48px 0 32px;border-top:1px solid var(--border)}}
.chapter-head h2{{font-size:32px;margin:0 0 8px}}
.chapter-meta{{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:0 0 24px}}
.story{{list-style:none;padding:0;margin:0 0 24px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}}
.road .story{{grid-template-columns:repeat(2,minmax(0,1fr))}}
.story-label{{font-size:13px;text-transform:uppercase;letter-spacing:.06em;color:var(--text-2);margin:0 0 6px}}
.feature-change{{display:flex;gap:12px;align-items:stretch;font-size:14px;line-height:22px;margin:0 0 24px}}
.fc-col{{border:1px solid var(--border);border-radius:10px;padding:8px 12px;background:var(--surface);flex:1}}
.fc-added{{border:2px solid var(--v3)}}
.fc-col ul{{margin:0;padding-left:18px}}.fc-head{{margin:0 0 4px;font-weight:650}}
.fc-arrow{{align-self:center;font-weight:700;font-size:20px}}
.outcomes{{display:flex;flex-wrap:wrap;gap:16px;align-items:stretch;margin:0 0 24px}}
.outcome{{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:16px 20px;min-width:240px;flex:1}}
.outcome-title{{font-size:14px;color:var(--text-2);margin:0 0 4px;font-weight:600}}
.outcome-value{{font-size:30px;line-height:36px;font-weight:700;margin:0 0 4px;font-variant-numeric:tabular-nums}}
.outcome-interval{{font-size:14px;margin:0;font-variant-numeric:tabular-nums}}
.outcomes-badge{{flex-basis:100%;margin:0}}
.helps-hurts{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;margin:0 0 16px}}
.caveats{{border-left:3px solid var(--caveat-rule);padding:4px 0 4px 20px;margin:8px 0 24px}}
.caveats h3{{font-size:16px}}
.decision{{margin:0 0 24px}}
.holdout{{margin:0 0 24px}}.holdout-head{{font-weight:650;display:flex;gap:10px;flex-wrap:wrap;align-items:center}}
.holdout-label{{font-style:italic;color:var(--text-2)}}
.chapter-links{{display:flex;gap:4px 20px;flex-wrap:wrap}}
.archive-note{{font-size:14px;color:var(--text-2)}}
.attribution-line{{font-size:14px;color:var(--text-2)}}
/* system view */
.flow{{list-style:none;padding:0;margin:16px 0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;counter-reset:flow}}
.flow-step{{border:1px solid var(--text-2);border-radius:10px;padding:10px 12px;background:var(--surface);position:relative}}
.flow-step.flow-planned{{border-style:dashed;background:transparent}}
.flow-title{{display:block;font-weight:650;font-size:15px}}
.flow-body{{display:block;font-size:14px;line-height:21px;color:var(--text-2)}}
.flow-note{{font-size:15px}}
pre{{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:12px 16px;overflow-x:auto;max-width:100%}}
.statement{{margin:0;padding:0 0 0 20px;border-left:3px solid var(--text);font-size:18px;line-height:30px;max-width:64ch}}
.site-footer{{max-width:var(--content);margin:0 auto;padding:24px;border-top:1px solid var(--border);font-size:14px;color:var(--text-2)}}
/* phones and narrow windows (§7.10) */
@media (max-width:980px){{
 .opening{{grid-template-columns:minmax(0,1fr);gap:24px;padding-top:28px}}
 .story,.road .story{{grid-template-columns:minmax(0,1fr)}}
 .flow{{grid-template-columns:repeat(2,minmax(0,1fr))}}
 .branches{{grid-template-columns:minmax(0,1fr)}}
}}
@media (max-width:620px){{
 .header-inner{{padding:0 16px}}
 .brand-full{{display:none}}.brand-short{{display:inline}}
 .main-nav a{{padding:0 8px}}
 .page{{padding:0 16px 64px}}
 h1{{font-size:34px;line-height:1.12}}
 h2{{font-size:25px}}
 .chapter-head h2{{font-size:26px}}
 .lede{{font-size:17px;line-height:27px}}
 .panel{{padding:16px 12px}}
 .mainline{{grid-template-columns:minmax(0,1fr);gap:18px}}
 .mainline::before{{left:8px;right:auto;top:8px;bottom:8px;width:3px;height:auto}}
 .node a{{padding:0 0 0 34px}}
 .node .dot{{top:2px}}
 .helps-hurts{{grid-template-columns:minmax(0,1fr)}}
 .flow{{grid-template-columns:minmax(0,1fr)}}
 .feature-change{{flex-direction:column}}.fc-arrow{{align-self:flex-start}}
 .outcomes{{flex-direction:column}}
 .outcome{{min-width:0}}
 .statement{{font-size:17px}}
}}
@media (max-width:440px){{
 .brand-short{{display:none}}.brand-tiny{{display:inline}}
 .reproduce pre{{white-space:pre-wrap;overflow-wrap:anywhere}}
}}
@media (max-width:340px){{
 .header-inner,.page{{padding-left:12px;padding-right:12px}}
 .panel{{padding:12px 8px}}
 .main-nav a{{padding:0 6px;font-size:14px}}
}}
.opening-copy details.disclosure{{margin-top:4px;border-bottom:1px solid var(--border)}}
.opening-copy details.disclosure>summary{{font-size:14px;font-weight:600;color:var(--text-2)}}
.opening-copy .disclosure-body p{{font-size:14px;line-height:22px;color:var(--text-2)}}
.summary-label{{font-size:13px;font-weight:650;text-transform:uppercase;letter-spacing:.05em;margin:0 0 4px;color:var(--text-2)}}
.opening-summary p[data-block]{{font-size:17px;line-height:27px;color:var(--text)}}
.chapter-sub{{font-size:19px;line-height:29px;color:var(--text);max-width:60ch;margin:0 0 20px}}
.change{{margin:0 0 24px}}
.preview-note{{font-size:13px;color:var(--text-2)}}
td .ci,td .unit,th .unit{{color:var(--text-2);font-weight:400}}
th .unit{{font-size:12px}}
/* v1's archived report: its own scoped styles, deliberately (invariant 24) */
.v1-archive{{--ink:#16202b;--mute:#5a6a7a;--rule:#d7dee6;--band:#3a6ea5;--warn:#8a4b2a;color:var(--ink)}}
.v1-archive .v1-title{{font-size:26px;line-height:1.2;margin:.4em 0 .3em}}
.v1-archive h4{{font-size:20px;margin:2.2em 0 .5em;padding-top:.5em;border-top:1px solid var(--rule)}}
.v1-archive h5{{font-size:14px;margin:1.6em 0 .4em;color:var(--mute);text-transform:uppercase;letter-spacing:.04em}}
.v1-archive p,.v1-archive li{{max-width:74ch;overflow-wrap:break-word}}
.v1-archive a{{color:#1d4e89}}
.v1-archive code,.v1-archive .mono{{font-family:var(--mono);font-size:.88em;overflow-wrap:anywhere}}
.v1-archive .lede{{font-size:17px;color:var(--mute);max-width:74ch}}
.v1-archive .card{{background:#fff;border:1px solid var(--rule);border-radius:10px;padding:16px 20px;margin:18px 0}}
.v1-archive .label{{background:#fff5ec;border-left:4px solid var(--warn);padding:12px 16px;margin:18px 0;border-radius:0 8px 8px 0}}
.v1-archive .label strong{{color:var(--warn)}}
.v1-archive blockquote{{margin:18px 0;padding:12px 18px;border-left:4px solid var(--band);background:#f2f6fb;
 border-radius:0 8px 8px 0;color:#243546}}
.v1-archive blockquote p{{margin:.3em 0}}
.v1-archive table{{border-collapse:collapse;font-size:.87rem;min-width:100%}}
.v1-archive th,.v1-archive td{{border-bottom:1px solid var(--rule);padding:6px 12px;text-align:left;vertical-align:top}}
.v1-archive th{{background:#f0f4f8;font-weight:600}}
.v1-archive td.n{{text-align:right;white-space:nowrap;font-family:var(--mono)}}
.v1-archive figure{{margin:20px 0}}
.v1-archive figure img{{width:100%;height:auto;border:1px solid var(--rule);border-radius:8px;background:#fff}}
.v1-archive figcaption{{font-size:.85rem;color:var(--mute);margin-top:6px}}
.v1-archive figure{{position:relative}}
.v1-archive figure img[data-enlarge]{{cursor:zoom-in}}
.v1-archive figure img[data-enlarge]:focus-visible{{outline:3px solid var(--accent);outline-offset:2px}}
.v1-archive figure:has(img[data-enlarge])::after{{content:"Enlarge";position:absolute;top:8px;right:8px;font-size:12px;
 line-height:18px;padding:2px 8px;border-radius:9px;background:rgba(24,24,27,.72);color:#fff;pointer-events:none}}
dialog.figure-view{{width:min(96vw,1640px);max-width:none;max-height:94vh;padding:0;border:1px solid var(--border);
 border-radius:10px;background:var(--surface)}}
dialog.figure-view::backdrop{{background:rgba(24,24,27,.6)}}
.figure-view .figure-bar{{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:8px 12px;
 border-bottom:1px solid var(--border);position:sticky;top:0;left:0;background:var(--surface)}}
.figure-view .figure-bar p{{margin:0;font-size:14px;color:var(--text-2)}}
.figure-view button{{min-height:44px;min-width:44px;font:inherit;font-weight:600;border:1px solid var(--border);
 border-radius:8px;background:var(--surface);color:var(--text);padding:0 14px;cursor:pointer}}
.figure-view .figure-scroll{{overflow:auto;max-height:calc(94vh - 62px)}}
.figure-view .figure-scroll img{{display:block;width:auto;max-width:none;height:auto}}
.v1-archive .figrow{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}}
.v1-archive .controls{{display:flex;flex-wrap:wrap;gap:22px;align-items:center;margin:16px 0 6px}}
.v1-archive .controls fieldset{{border:1px solid var(--rule);border-radius:8px;padding:8px 14px;margin:0}}
.v1-archive .controls legend{{font-size:.78rem;color:var(--mute);text-transform:uppercase;letter-spacing:.05em}}
.v1-archive .controls label{{margin-right:12px;font-size:.92rem;white-space:nowrap;display:inline-flex;align-items:center;min-height:44px}}
.v1-archive #chart{{width:100%;height:auto;background:#fff;border:1px solid var(--rule);border-radius:8px}}
.v1-archive .surfaces{{border:1px solid #d7dee6;border-radius:8px;padding:14px 16px;margin:18px 0;background:#fbfcfd}}
.v1-archive .surfaces-lead{{margin:0 0 10px}}
.v1-archive .surfaces-table{{width:100%;border-collapse:collapse;margin:0;font-size:.94em}}
.v1-archive .surfaces-table th,.v1-archive .surfaces-table td{{border:1px solid #e2e8ee;padding:7px 9px;text-align:left;vertical-align:top;overflow-wrap:anywhere}}
.v1-archive .surfaces-table th{{background:#eef2f6}}
.v1-archive .trail{{margin:6px 0 12px}}
.v1-archive .next{{margin:10px 0 0;padding-top:9px;border-top:1px dashed #d7dee6;color:#4a5a6a}}
.v1-archive .kv{{display:grid;grid-template-columns:max-content 1fr;gap:4px 18px;font-size:.92rem}}
.v1-archive .kv dt{{font-family:var(--mono);color:var(--mute)}}
.v1-archive .kv dd{{margin:0;overflow-wrap:anywhere}}
.v1-archive .v1-footer{{margin-top:32px;padding-top:14px;border-top:1px solid var(--rule);font-size:.86rem;color:var(--mute)}}
.v1-archive .toc{{font-size:.92rem;columns:2;column-gap:32px}}
.v1-archive .toc a{{display:block;padding:2px 0}}
@media (max-width:620px){{.v1-archive .toc{{columns:1}}.v1-archive .kv{{grid-template-columns:1fr}}.v1-archive .kv dd{{margin-bottom:8px}}}}
"""


# --------------------------------------------------------------------------- scripts


CHART_JS = """
(function(){
 var D=window.__FAN__,W=960,H=380,ML=58,MR=16,MT=18,MB=34,FS=11,STEP=2;
 var n=D.hours.length,dom=D.domain;
 var svg=document.getElementById('chart');
 // Draw at the chart's rendered width, so a phone gets a phone geometry and 12 px text instead of a
 // shrunk desktop drawing. The data, controls and their behaviour are unchanged.
 function geometry(){
  var w=Math.round(svg.getBoundingClientRect().width)||960;
  W=Math.max(280,Math.min(960,w));
  var narrow=W<600;
  H=narrow?300:380;ML=narrow?44:58;MR=narrow?10:16;MT=narrow?22:18;FS=12;STEP=narrow?4:2;
  svg.setAttribute('viewBox','0 0 '+W+' '+H);
 }
 function X(i){return ML+(W-ML-MR)*(n<2?0.5:i/(n-1));}
 function Y(v){return MT+(H-MT-MB)*(1-(v-dom[0])/(dom[1]-dom[0]));}
 function state(){
  var lv=document.querySelector('input[name=lvl]:checked').value;
  var sc=D.scales[parseInt(document.getElementById('scale').value,10)];
  return {lv:lv,sc:sc};
 }
 function ticks(){
  var span=dom[1]-dom[0],raw=span/6,mag=Math.pow(10,Math.floor(Math.log(raw)/Math.LN10));
  var step=[1,2,2.5,5,10].map(function(m){return m*mag;}).filter(function(s){return s>=raw;})[0]||mag*10;
  var out=[],v=Math.ceil(dom[0]/step)*step;
  for(;v<=dom[1];v+=step){out.push(Math.round(v*100)/100);}
  return out;
 }
 function el(tag,attrs,text){
  var e=document.createElementNS('http://www.w3.org/2000/svg',tag);
  for(var k in attrs){e.setAttribute(k,attrs[k]);}
  if(text!==undefined){e.textContent=text;}
  return e;
 }
 function draw(){
  geometry();
  var s=state(),pair=D.levels[s.lv],rows=D.series[s.sc];
  if(!pair||!rows){throw new Error('fan chart lookup miss: level '+s.lv+', scale '+s.sc);}
  var li=D.labels.indexOf(pair[0]),hi=D.labels.indexOf(pair[1]),mi=D.labels.indexOf('p50');
  while(svg.firstChild){svg.removeChild(svg.firstChild);}
  ticks().forEach(function(t){
   svg.appendChild(el('line',{x1:ML,x2:W-MR,y1:Y(t),y2:Y(t),stroke:t===0?'#9aa7b4':'#eceff3','stroke-width':t===0?1.2:1}));
   svg.appendChild(el('text',{x:ML-8,y:Y(t)+4,'text-anchor':'end',fill:'#5a6a7a','font-size':FS},t));
  });
  for(var i=0;i<n;i+=STEP){
   svg.appendChild(el('text',{x:X(i),y:H-12,'text-anchor':'middle',fill:'#5a6a7a','font-size':FS},D.hours[i]));
  }
  var up=[],down=[];
  for(var j=0;j<n;j++){up.push(X(j)+','+Y(rows[j][hi]));}
  for(var k=n-1;k>=0;k--){down.push(X(k)+','+Y(rows[k][li]));}
  svg.appendChild(el('polygon',{points:up.concat(down).join(' '),fill:'#3a6ea5','fill-opacity':.22}));
  var med=[];
  for(var m=0;m<n;m++){med.push(X(m)+','+Y(rows[m][mi]));}
  svg.appendChild(el('polyline',{points:med.join(' '),fill:'none',stroke:'#1b3a5c','stroke-width':2.2}));
  if(s.sc==='1.00'){
   var act=[];
   for(var a=0;a<n;a++){act.push(X(a)+','+Y(D.actual[a]));}
   svg.appendChild(el('polyline',{points:act.join(' '),fill:'none',stroke:'#b03a2e','stroke-width':1.6,'stroke-dasharray':'6 4'}));
  }
  svg.appendChild(el('text',{x:ML,y:MT-6,fill:'#5a6a7a','font-size':FS},
   W<600?('EUR/MWh · local hour · '+D.delivery_day):('EUR/MWh  ·  local hour (Europe/Berlin)  ·  delivery day '+D.delivery_day)));
  document.getElementById('scaleval').textContent='\\u00d7 '+s.sc;
  document.getElementById('cov').textContent=window.__COV__[s.lv];
  document.getElementById('scenario').style.display=(s.sc==='1.00')?'none':'block';
  document.getElementById('legend-actual').style.display=(s.sc==='1.00')?'inline':'none';
 }
 Array.prototype.forEach.call(document.querySelectorAll('input[name=lvl]'),function(r){r.addEventListener('change',draw);});
 document.getElementById('scale').addEventListener('input',draw);
 var archive=document.getElementById('v1-archive');
 if(archive){archive.addEventListener('toggle',function(){if(archive.open){draw();}});}
 var pending=null;
 window.addEventListener('resize',function(){clearTimeout(pending);pending=setTimeout(draw,150);});
 draw();
})();
"""

#: Opening a closed disclosure when a link targets something inside it (Safari does not), and a
#: small IntersectionObserver that marks the current generation in the desktop rail (§7.10).
# v1's archived figures are drawn for a wide page; any of them opens at its full size, scrollable on a
# phone. The enlarged view reuses the embedded image, so nothing is fetched.
FIGURE_JS = """
(function(){
 var view=document.getElementById('figure-view'),full=document.getElementById('figure-full');
 if(!view||typeof view.showModal!=='function'){return;}
 var opener=null;
 function open(img){
  opener=img;full.src=img.src;full.alt=img.alt;
  view.showModal();
  // Fit the width on a wide screen; on a phone, about twice the screen width, so the figure's own
  // text reads at roughly 13 px and needs only a short pan.
  var box=view.clientWidth-2,natural=img.naturalWidth||1600;
  full.style.width=Math.min(natural,box<700?Math.max(720,2*box):box)+'px';
  document.getElementById('figure-close').focus();
 }
 Array.prototype.forEach.call(document.querySelectorAll('.v1-archive figure img'),function(img){
  img.setAttribute('data-enlarge','');img.setAttribute('tabindex','0');img.setAttribute('role','button');
  img.setAttribute('aria-label','Enlarge figure: '+img.alt);
  img.addEventListener('click',function(){open(img);});
  img.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();open(img);}});
 });
 document.getElementById('figure-close').addEventListener('click',function(){view.close();});
 view.addEventListener('click',function(e){if(e.target===view){view.close();}});
 view.addEventListener('close',function(){full.removeAttribute('src');if(opener){opener.focus();}});
})();
"""


NAV_JS = """
(function(){
 function reveal(hash,scroll){
  if(!hash||hash.length<2){return;}
  var target=document.getElementById(decodeURIComponent(hash.slice(1)));
  if(!target){return;}
  var node=target,opened=false;
  if(node.tagName==='DETAILS'&&!node.open){node.open=true;opened=true;}
  while(node){var d=node.parentElement?node.parentElement.closest('details'):null;
   if(d&&!d.open){d.open=true;opened=true;}node=d;}
  if(opened||scroll){target.scrollIntoView();}
 }
 document.addEventListener('click',function(e){
  var a=e.target.closest?e.target.closest('a[href^="#"]'):null;
  if(a){reveal(a.getAttribute('href'),false);}
 });
 window.addEventListener('hashchange',function(){reveal(location.hash,false);});
 reveal(location.hash,true);
 var links=document.querySelectorAll('.rail a[href^="#v"]');
 if(!('IntersectionObserver' in window)||!links.length){return;}
 var byId={};Array.prototype.forEach.call(links,function(a){byId[a.getAttribute('href').slice(1)]=a;});
 var io=new IntersectionObserver(function(entries){
  entries.forEach(function(entry){
   if(entry.isIntersecting&&byId[entry.target.id]){
    Array.prototype.forEach.call(links,function(a){a.removeAttribute('aria-current');});
    byId[entry.target.id].setAttribute('aria-current','true');
   }
  });
 },{rootMargin:'-30% 0px -60% 0px'});
 Object.keys(byId).forEach(function(id){var el=document.getElementById(id);if(el){io.observe(el);}});
})();
"""


# --------------------------------------------------------------------------- v1's archived report (§8.5)


def v1_archive(payload: dict) -> str:
    """v1's original report, as published on 2026-09-15, preserved inside the v1 chapter.

    Spliced from the CP-3 generator with only these changes: heading levels shift under the chapter,
    the stale development-update card is removed (its anchor survives as an alias), both surfaces
    tables sit in a labelled scroll wrapper, and the superseded release note is relabelled "Tracking
    after v1" around the claim set's current note (plan §8.7).
    Its text, figures, tables and interactive fan chart are otherwise unchanged (invariant 24)."""
    C = build_claims()
    regime = pd.read_csv(ROOT / "reports/cp2/regime_table.csv")
    shap_top = pd.read_csv(ROOT / "reports/cp2/shap_ranking.csv").head(10)
    perm_top = pd.read_csv(ROOT / "reports/cp2/permutation_importance.csv").head(10)
    pooled = pd.read_csv(ROOT / "reports/cp2/development_pooled_metrics.csv")
    reliability = pd.read_csv(ROOT / "reports/cp2/reliability_three_stage.csv")

    coverage = {str(level): C[f"holdout_coverage_{level}"] for level in INTERVAL_LEVELS}
    # §10 item (11): one shared set, rendered onto every surface. The bullets
    # arrive with a `**bold**` lead-in; only that lead-in becomes markup, so the
    # limitation sentence itself reaches the page byte-identical to the other
    # surfaces and the agreement check compares like with like.
    limitations = "\n".join(
        "<li>" + BOLD.sub(r"<strong>\1</strong>", esc(bullet)) + "</li>"
        for bullet in limitation_bullets(C)
    )
    # §10 item (12): the same treatment, so no surface can carry a partial
    # reproducibility statement. `CODE` turns the bullets' own backticks into
    # <code>, after escaping, so the sentence itself stays byte-identical to
    # the Markdown surfaces once markup is stripped.
    reproduction = "\n".join(
        "<li>" + CODE.sub(r"<code>\1</code>", BOLD.sub(r"<strong>\1</strong>", esc(bullet))) + "</li>"
        for bullet in reproducibility_bullets(C)
    )
    RUN_ROWS = "\n".join(
        f"<tr><td><code>{esc(name)}</code></td><td>{esc(what)}</td></tr>"
        for name, what in MLFLOW_RUN_NAMES
    )
    level_inputs = "".join(
        f"<label><input type='radio' name='lvl' value='{level}'"
        f"{' checked' if level == 80 else ''}> {level}&nbsp;%</label>"
        for level in sorted(INTERVAL_LEVELS)
    )

    figures = {
        "welch": data_uri(ROOT / "reports/fig_welch_periodogram.png"),
        "regime_spectrum": data_uri(ROOT / "reports/fig_per_regime_periodogram.png"),
        "acf": data_uri(ROOT / "reports/fig_acf_24_168.png"),
        "shap": data_uri(ROOT / "reports/cp2/fig_shap_summary.png"),
        "dep24": data_uri(ROOT / "reports/cp2/fig_shap_dependence_price_lag_24h.png"),
        "dep168": data_uri(ROOT / "reports/cp2/fig_shap_dependence_price_lag_168h.png"),
        "reliability": data_uri(ROOT / "reports/cp2/fig_reliability_three_stage.png"),
    }

    cutoff_table = f"""
    <div class='scroll'><table><thead><tr><th>Cutoff</th><th>Value</th></tr></thead><tbody>
    <tr><td><code>snapshot_cutoff</code></td><td class='n'>{C['snapshot_cutoff']}</td></tr>
    <tr><td><code>raw_model_fit_cutoff</code></td><td class='n'>{C['raw_model_fit_cutoff']}</td></tr>
    <tr><td><code>final_calibration_window</code></td><td class='n'>{C['final_calibration_window']}</td></tr>
    <tr><td><code>holdout_window</code></td><td class='n'>{C['holdout_window']}</td></tr>
    </tbody></table></div>"""

    return f"""
<h3 class="v1-title">DE-LU day-ahead price forecasting</h3>
<p class="lede">A probabilistic forecast of the next delivery day's hourly German–Luxembourg
day-ahead electricity price, with calibrated 50 / 80 / 95&nbsp;% prediction intervals.
<strong>Strict-gate by construction:</strong> the shipped model uses no input published after the
12:00&nbsp;CET day-ahead auction gate. Evaluated exactly once, on a holdout pinned before
development.</p>

<div class="card">
<p><strong>{esc(C['shipped_is_evaluated'])}</strong></p>
<p>This page is static. It renders from files committed in the repository and makes
<strong>no runtime call</strong> to any external service — no analytics, no fonts, no CDN, no call
to the interactive Space. Everything below, including the chart, works with the network off.</p>
<p class="toc">
<a href="#data">1 · The data</a><a href="#regimes">2 · Three regimes</a>
<a href="#catalog">3 · Feature catalog</a><a href="#spectral">3b · Spectral view</a>
<a href="#method">4 · Validation design</a><a href="#results">5 · Results</a>
<a href="#shap">6–7 · Explainability</a><a href="#regime-table">8 · Regime-stratified error</a>
<a href="#reliability">9 · Reliability</a><a href="#forecast">10 · Next-day forecast</a>
<a href="#limitations">11 · Honest limitations</a><a href="#repro">12 · Reproducibility</a>
</p>
</div>


<h5>The four cutoffs, stated separately because they are four different dates</h5>
{cutoff_table}
<p>The raw-model fit cutoff precedes the snapshot cutoff by <strong>{C['staleness_days']} delivery
days</strong> (1 + 60 + 1 + 90). That is what shipping the evaluated model costs, stated plainly
rather than apologised for; the deployed demo applies a <strong>frozen</strong> model and there is
no scheduled refresh.</p>

<h4 id="data">1 · The data</h4>
<p>One committed Parquet snapshot: <strong>67,343</strong> continuous UTC-indexed hourly rows,
delivery 2019-01-01 through {C['snapshot_cutoff']}, carrying the day-ahead price (A44), the
day-ahead load forecast (A65/A01), the benchmark-only day-ahead VRE forecast (A69) and aggregate
actual generation (A75). Quarter-hourly feeds aggregate to hours from exactly four complete bins,
never a partial one; the 2025-10-01 switch to a 15-minute price product is handled as the mean of
four quarter-hour prices. The snapshot is pinned by SHA-256
<code>{C['snapshot_sha256']}</code> and ships inside the container, so the demo never pulls a feed
while you use it.</p>
<p>{esc(C['attribution'])}</p>

<h4 id="regimes">2 · Three regimes in one series</h4>
<p>The annual mean price swept from about <strong>€30/MWh</strong> in 2020 to about
<strong>€235/MWh</strong> in 2022 and back to about <strong>€89/MWh</strong> in 2025 — a crisis
and a normalization inside one training set. Underneath it, the solar build-out pushed
negative-price hours from <strong>139</strong> (2021) → <strong>69</strong> (2022) →
<strong>301</strong> (2023) → <strong>457</strong> (2024) → <strong>576</strong> (2025).</p>
<p>The 2025 count is measured on this snapshot's hourly series. From 2025-10-01 an hour is the mean
of four quarter-hour prices, so any hour-level tally depends on that averaging choice and a
quarter-hour tally differs. The price is routinely negative and has touched the −500&nbsp;€/MWh
floor, which is why no log or Box-Cox transform is applied to the target: pinball loss, the CQR
score and monotone rearrangement are all location-equivariant and behave correctly through zero.</p>
<p>Two consequences the whole design follows from. Evaluation is stratified across all three
regimes rather than collapsed into a recent tail. And exchangeability — the assumption CQR's
coverage guarantee rests on — is mildly violated by construction, which is disclosed rather than
assumed away.</p>

<h4 id="catalog">3 · Feature catalog — frozen before fitting</h4>
<p>Two catalogs were frozen before any model ran. <code>base</code>: calendar and regime features,
the A65 load forecast, calendar-day-matched price lags at D−1 / D−2 / D−7, and D-1-frozen rolling
price statistics. <code>base + residual_load_proxy</code> adds exactly one domain feature — a
residual-load proxy built from a 42-complete-delivery-day trailing mean of actual wind and solar
generation ending at D−2, which clears the 12:00 gate with a wide margin.</p>
<p>Pooled observation-weighted <em>raw-head</em> mean pinball loss over the five pinned development
folds, matched on rows, seed, hyperparameters and (zero) tuning budget, unrounded as stored:</p>
<div class="scroll"><table><thead><tr><th>Arm</th><th>Pooled raw-head mean pinball loss</th></tr></thead>
<tbody>
<tr><td><code>base</code></td><td class="n">{C['catalog_base_loss']}</td></tr>
<tr><td><code>base + residual_load_proxy</code></td><td class="n">{C['catalog_augmented_loss']}</td></tr>
</tbody></table></div>
<p>Percentage difference (augmented vs base): <strong>{C['catalog_pct']}</strong>.
<strong>Selected catalog: <code>{C['selected_catalog']}</code>.</strong> The rule was fixed before
fitting — the augmented catalog ships only if its unrounded stored pooled loss is lower. It is not,
so the domain feature did not earn its place and the champion ships strict-gate. That is a
reportable result, not a failure, and the comparison was designed so that "no improvement" was a
publishable answer.</p>

<h4 id="spectral">3b · Why these seasonal features? (spectral view)</h4>
<div class="figrow">
<figure><img alt="Welch periodogram of the detrended DE-LU day-ahead price, with 24h, 168h and 12h labels" src="{figures['welch']}"><figcaption>Welch periodogram — Hann window, 50&nbsp;% overlap.</figcaption></figure>
<figure><img alt="Per-regime Welch periodogram overlay for pre-crisis, crisis and normalization" src="{figures['regime_spectrum']}"><figcaption>Per-regime overlay.</figcaption></figure>
<figure><img alt="Autocorrelation of the detrended price with 24h and 168h reference lines" src="{figures['acf']}"><figcaption>ACF cross-check, time domain.</figcaption></figure>
</div>
<p>The Welch periodogram shows pronounced price energy at the 24-hour and 168-hour cycles with a
visible 12-hour harmonic, which is what justifies the catalog's hour-of-day and day-of-week
structure rather than an assumption that electricity "should" be daily-seasonal. The per-regime
overlay shows an elevated broadband floor and altered seasonal amplitude during the crisis: the
spectrum itself is not stationary across regimes, which supports reporting performance across all
three rather than collapsing them into one recent-tail summary. The ACF cross-check confirms the
same daily and weekly recurrence in the time domain, so the conclusion does not rest on a single
estimator. These are price diagnostics only — they neither validate nor justify retaining
<code>residual_load_proxy</code>, which the frozen two-arm comparison alone decides.</p>

<h4 id="method">4 · Validation design</h4>
<p>Expanding-window walk-forward CV with five development folds, each carrying a
<strong>one-complete-delivery-day embargo</strong> — 23, 24 or 25 rows as DST requires, never
hard-coded to 24 — and a 90-day evaluation block, anchored so the blocks span pre-crisis, the
crisis peak and the post-crisis negative-price era. Five tail partitions were pinned before any
EDA: fold&nbsp;5, Embargo&nbsp;A, a 60-day final-calibration slice, Embargo&nbsp;B, and the final
90-day holdout.</p>
<p><strong>The target is D+1, anchored at the 12:00 CET gate</strong>, because that is what the
day-ahead auction clears. That makes the availability rule stricter than it first looks: the model
emits the whole next-day curve at once, so a row-wise <code>t−1</code> boundary would admit the
target curve into its own features. The binding rule is per delivery day — for a forecast of day
<code>D</code>, every price-derived feature may consume only prices whose delivery date is earlier
than <code>D</code>, rolling statistics are frozen at the D−1 boundary for the whole curve, and an
unavailable or ambiguous calendar-day match fails closed to null rather than reaching for a
same-day price.</p>
<p><strong>Strict gate.</strong> The day-ahead wind and solar forecast (A69) is not published until
after the 12:00 gate, so rather than use it as-archived and disclose that, this project excludes it
from the shipped model entirely. Delivery-day A69 is rejected by the champion's runtime schema.
What the exclusion costs is then measured, in section&nbsp;5, instead of being waved at.</p>
<p><strong>Two disclosed assumptions, stated as assumptions rather than as measurements:</strong></p>
<ul>
<li>{esc(C['assumption_a65'])}</li>
<li>{esc(C['assumption_a75'])}</li>
</ul>

<h4 id="results">5 · Results</h4>
<h5>Development folds — descriptive post-selection evidence</h5>
<p><code>evidence_class = {C['development_evidence_class']}</code>. These folds were also used for
catalog selection and model development, so their p-values are descriptive, never confirmatory, and
no result gates anything.</p>
<div class="scroll"><table><thead><tr><th>Analysis</th><th>Comparator</th><th>Statistic</th><th>p-value</th><th>N days</th></tr></thead>
<tbody>
<tr><td>Probabilistic daily-vector pinball</td><td>similar-day naive</td><td class="n">{C['development_dm_pinball_statistic']}</td><td class="n">{C['development_dm_pinball_p_value']}</td><td class="n">{C['development_days']}</td></tr>
<tr><td>Point median absolute error</td><td>similar-day naive</td><td class="n">{C['development_dm_point_statistic']}</td><td class="n">{C['development_dm_point_p_value']}</td><td class="n">{C['development_days']}</td></tr>
</tbody></table></div>
<p><strong>The point-accuracy test does not merely fail to show an advantage — it shows a
deficit.</strong> The test is one-sided (reject if DM &lt; −1.645) and the statistic is
<em>+{C['development_dm_point_statistic_abs']}</em>, p = {C['development_dm_point_p_value']}: the champion's median is
{C['development_dm_point_relative']} against the naive over the development folds. Reported here rather than
omitted or reframed. The
probabilistic win is broad and the point-accuracy win is not: the pooled MAE gap comes almost
entirely from the crisis-peak fold. The mechanism is measured, not assumed: the model did see the
crisis (that fold's training included 5,784 crisis hours at a €173 mean and a €700 maximum), but
<strong>61.3% of the evaluation block sits above the 99th percentile of everything it ever saw while
only 2.45% exceeds its maximum</strong> — shrinkage toward the training level, not an extrapolation
wall. Persistence has no training distribution and carries the level for free. Note also that
a point forecast scored on pinball is structurally disadvantaged against a nine-quantile model, so
the pinball margin is largely the value of <em>having</em> a predictive distribution.</p>
{table(pooled)}

<h5>The one-shot holdout — opened exactly once</h5>
<p>After the catalog, hyperparameters and every implementation choice were frozen, the nine raw
heads were fit on every eligible row strictly before Embargo&nbsp;A, the four CQR thresholds were
estimated once on the 60-day calibration slice, isotonic-last was attached, and that complete
artifact was frozen. Only then was the holdout opened.</p>
<div class="scroll"><table><thead><tr><th>Metric</th><th>Champion</th><th>Similar-day naive</th><th>Difference</th></tr></thead>
<tbody>
<tr><td>MAE (EUR/MWh)</td><td class="n">{C['holdout_mae_champion']}</td><td class="n">{C['holdout_mae_naive']}</td><td class="n">{C['holdout_mae_pct']}</td></tr>
<tr><td>Mean pinball loss</td><td class="n">{C['holdout_pinball_champion']}</td><td class="n">{C['holdout_pinball_naive']}</td><td class="n">{C['holdout_pinball_pct']}</td></tr>
</tbody></table></div>
<p>Final empirical coverage over {C['holdout_rows']} rows on {C['holdout_days']} delivery days:
<strong>{C['holdout_coverage_50']}</strong> / <strong>{C['holdout_coverage_80']}</strong> /
<strong>{C['holdout_coverage_95']}</strong> at the 50 / 80 / 95&nbsp;% nominal levels.
Probabilistic daily-vector Diebold–Mariano against the similar-day naive: statistic
<strong>{C['holdout_dm_statistic']}</strong>, p-value <strong>{C['holdout_dm_p_value']}</strong>,
standardized effect size <strong>{C['holdout_dm_effect_size']}</strong>.</p>
<blockquote><p>{esc(C['holdout_dm_label'])}</p></blockquote>
<p>The result supports a probabilistic-skill claim against the similar-day naive on this window and
nothing wider. It is not a gate, and no superiority claim beyond what it supports is made anywhere
on this page.</p>

<h5>What the post-gate forecast would have been worth</h5>
<p>A controlled ablation on raw quantile heads, neither arm calibrated, identical in every respect
except the added delivery-day A69 forecast and its named derivatives: pooled mean pinball loss
moves from <code>{C['benchmark_strict_loss']}</code> to <code>{C['benchmark_a69_loss']}</code> —
<strong>{C['benchmark_pct']}</strong>. So the project ships an honest model and puts a number on the
value of the information it chose not to use.</p>
<blockquote><p>{esc(C['benchmark_limitation'])}</p></blockquote>

<h4 id="shap">6–7 · Explainability</h4>
<figure><img alt="SHAP summary plot for the p50 head of the champion catalog" src="{figures['shap']}"><figcaption>SHAP summary, p50 head, scored out of sample on fold 5's evaluation block.</figcaption></figure>
<div class="figrow">
<figure><img alt="SHAP dependence plot for price_lag_24h" src="{figures['dep24']}"><figcaption><code>price_lag_24h</code></figcaption></figure>
<figure><img alt="SHAP dependence plot for price_lag_168h" src="{figures['dep168']}"><figcaption><code>price_lag_168h</code></figcaption></figure>
</div>
<div class="figrow">
<div><h5>Top 10 by mean |SHAP|</h5>{table(shap_top)}</div>
<div><h5>Top 10 by permutation importance</h5>{table(perm_top)}</div>
</div>
<p>SHAP on the p50 head explains central tendency, not interval width — width is driven by the
inter-quantile spread and the CQR shift. Neither ranking is the incremental-value test; that is the
frozen two-arm comparison in section&nbsp;3, which selected <code>{C['selected_catalog']}</code>.
The two rankings agree at the top and disagree in the middle, which is the ordinary difference
between attribution in expectation and degradation under shuffling.</p>

<h4 id="regime-table">8 · Regime-stratified error</h4>
<p><code>n_obs</code> on every row. Thin subsets carry day-block bootstrap 95&nbsp;% confidence
intervals — days, not hours, because the rows of one delivery day share a day effect — and are read
qualitatively.</p>
{table(regime)}
<p>Coverage collapses on the crisis stratum and on negative-price hours. The bounded target
truncates the lower conformity residuals near the floor, so the lowest intervals under-cover
conditionally. This is disclosed rather than engineered around: a floor-aware tail would reopen
scope this project deliberately closed.</p>

<h4 id="reliability">9 · Reliability — three stages</h4>
<figure><img alt="Three-stage reliability diagram: raw LightGBM, post-CQR, and final post-isotonic" src="{figures['reliability']}"><figcaption>Raw heads → CQR → isotonic last, at all three nominal levels.</figcaption></figure>
{table(reliability)}
<p>The finite-sample, distribution-free per-interval marginal guarantee attaches to the
<strong>post-CQR / pre-isotonic</strong> output only. Isotonic is a monotone rearrangement applied
last; whenever it moves an endpoint it perturbs the interval, so the final output's coverage is
reported as <strong>empirical</strong>. No joint or simultaneous coverage across the four intervals
is claimed.</p>
<p>The one retained hard gate is a correctness property, not a favourable number: zero
quantile-crossing violations after the full pipeline. On the selected
<code>{C['selected_catalog']}</code> catalog's development evaluation rows, the raw heads cross on
{C['crossings_development_raw']} adjacent pairs and still cross on
{C['crossings_development_post_cqr']} after CQR; after isotonic the count is
{C['crossings_development_final']}, and {C['crossings_holdout_final']} on the holdout. That CQR
alone leaves thousands of crossings is exactly why isotonic is unconditionally last.</p>
<blockquote><p>{esc(C['exchangeability'])}</p></blockquote>

<h4 id="forecast">10 · Next-day forecast</h4>
<div class="label">
<p><strong>{esc(C['replay_label'])}</strong> The delivery day below, {payload['delivery_day']},
falls inside the pinned holdout window {C['holdout_window']}. The dashed line is the price that
actually cleared — an outcome, never a model input.</p>
</div>
<div class="controls">
<fieldset><legend>Prediction-interval level</legend>{level_inputs}</fieldset>
<fieldset><legend>Load-forecast scenario <span id="scaleval" class="mono">&times; 1.00</span></legend>
<input id="scale" type="range" min="0" max="{len(LOAD_SCALES) - 1}" step="1" value="{LOAD_SCALES.index(1.00)}"
 style="width:220px" aria-label="load forecast scenario multiplier">
</fieldset>
</div>
<svg id="chart" viewBox="0 0 960 380" role="img" aria-label="Quantile fan chart for the selected delivery day"></svg>
<p><span class="mono" style="color:#1b3a5c">——</span> median forecast &nbsp;
<span class="mono" style="color:#3a6ea5">▇</span> selected interval &nbsp;
<span id="legend-actual"><span class="mono" style="color:#b03a2e">– –</span> cleared price (outcome)</span></p>
<p>Nominal level selected above; the frozen champion's own empirical coverage at that level over
the {C['holdout_days']}-day holdout was <strong id="cov">{C['holdout_coverage_80']}</strong>.</p>
<div class="label" id="scenario" style="display:none">
<p><strong>{esc(C['sensitivity_probe_label'])}</strong> The scenario holds every other input fixed,
including the price history the lags and rolling statistics are built from, so a large perturbation
asks the model a question it was never trained on. The cleared-price line is hidden while a
scenario is active, because the outcome belongs to the unperturbed day.</p>
</div>
<p class="lede">Want to drive the model yourself? The
<a href="{C['space_url']}">{esc(C['space_link_label'])}</a> runs the champion's own boosters in
your browser, proved bitwise equal to the frozen artifact over {C['wasm_fixture_days']} delivery days.
This page stays the first touch because it downloads nothing and cannot fail when a CDN does.</p>

<h4 id="limitations">11 · Honest limitations</h4>
<ul>
{limitations}
</ul>
<p>{esc(C['floor_change'])}</p>
<blockquote><p>{esc(C['holdout_limitation'])}</p></blockquote>

<h4 id="repro">12 · Reproducibility</h4>

<div class="surfaces">
<p class="surfaces-lead"><strong>Three public surfaces, all live.</strong> Each answers a different
question and each stands on its own. This page is the one that needs no network.</p>
<div class="scroll" role="region" aria-label="Public surfaces" tabindex="0"><table class="surfaces-table">
<thead><tr><th>Surface</th><th>Answers</th><th>Cost to open</th></tr></thead>
<tbody>
<tr><td><strong>📄 Static report</strong> — you are here<br>
<a href="{C['pages_url']}">{C['pages_url']}</a></td>
<td>Can they reason, and will they say what went wrong?</td>
<td><strong>zero network calls</strong></td></tr>
<tr><td><strong>⚡ Interactive Space</strong><br>
<a href="{C['space_url']}">the Space</a> · <a href="{C['space_app_url']}">the app directly</a></td>
<td>Does the thing actually run? The champion's own boosters execute in your browser under
Pyodide — no server.</td>
<td>~{C['wasm_cold_load_mb']}&nbsp;MB first visit, ~1&nbsp;MB after. A Static Space executes
nothing, so it never sleeps.</td></tr>
<tr><td><strong>🔬 MLflow on DagsHub</strong><br>
<a href="{C['mlflow_url']}">the tracking server</a></td>
<td>Is the decision trail real, or is this page the only evidence?</td>
<td>anonymous, no sign-in</td></tr>
</tbody></table></div>

<p><strong>The decision trail, addressed directly.</strong> Every link here was checked from an
unauthenticated client. The DagsHub <em>repository</em> UI redirects an anonymous visitor to a
sign-in page; the <code>.mlflow</code> tracking host does not, which is why every link uses it.</p>
<ul class="trail">
<li><a href="{C['mlflow_experiment_url']}">Experiment <code>{C['mlflow_experiment_name']}</code></a>
— every v1 run, side by side</li>
<li><a href="{C['mlflow_models_url']}">Model registry</a> — the registered champion and its
<code>champion</code> alias</li>
<li><a href="{C['mlflow_url']}">Tracking root</a> — if a deep link ever moves, start here</li>
</ul>
<p>Runs are named rather than linked by id, because several decision-bearing runs were reproduced and
no single id is canonical — the name is what to search for:</p>
<div class="scroll" role="region" aria-label="Decision-bearing runs" tabindex="0"><table class="surfaces-table"><thead><tr><th>Run name</th><th>What it decided</th></tr></thead>
<tbody>
{RUN_ROWS}
</tbody></table></div>
<p class="next"><strong>Tracking after v1.</strong> {esc(C['mlflow_next_note'])}
See <a href="#journey">how it evolved</a>.</p>
</div>

<dl class="kv">
<dt>artifact_fingerprint_sha256</dt><dd><code>{C['champion_fingerprint']}</code></dd>
<dt>snapshot_sha256</dt><dd><code>{C['snapshot_sha256']}</code></dd>
<dt>catalog</dt><dd><code>{C['selected_catalog']}</code>, {C['champion_features']} features,
{C['champion_quantiles']} quantile heads, four CQR thresholds, isotonic last</dd>
<dt>fit / calibration rows</dt><dd>{C['champion_fit_rows']} raw-fit rows,
{C['champion_calibration_rows']} calibration rows</dd>
<dt>artifact size</dt><dd><code>python_model.pkl</code> {C['champion_pkl_bytes']} bytes =
{C['champion_pkl_size']}; the whole <code>models/champion/</code> directory
{C['champion_dir_bytes']} bytes = {C['champion_dir_size']}</dd>
<dt>compute</dt><dd>Apple M3, 16&nbsp;GB, CPU only, no GPU, $0 run rate</dd>
</dl>
<p>The pickle's bytes are deliberately <em>not</em> the identity to check: MLflow stamps a fresh
UUID and creation time into <code>MLmodel</code> on every save and cloudpickle is not
byte-reproducible, so <code>models/champion/</code> changes while the model does not. The
fingerprint is computed over the catalog, the feature list, the nine quantiles, the four thresholds
and the nine boosters' own serializations.</p>
<ul>
{reproduction}
<li><strong>Run it yourself.</strong> Clone
<a href="{C['github_url']}">{C['github_url']}</a>, then <code>uv sync</code>, then
<code>uv run python predict_next_day.py --level 80 --self-check</code> forecasts a delivery day
offline from the bundled snapshot and re-proves the gate boundary as it goes;
<code>make test</code> runs the invariant suite including the CQR order-statistic fixture;
<code>make sql</code> runs the DuckDB queries; and
<code>docker build -t delu-showcase . &amp;&amp; docker run -p 7860:7860 delu-showcase</code>
builds and serves the same image the Space runs, champion and snapshot bundled inside it.</li>
<li><strong>Compute.</strong> Apple M3, 16&nbsp;GB, CPU only, no GPU, $0 run rate; the whole
pipeline — development, benchmark, final fit and diagnostics — runs in well under an hour.</li>
</ul>

<div class="v1-footer">
<p>{esc(C['attribution'])}</p>
<p>Built from the committed artifacts at snapshot <code>{C['snapshot_sha256'][:16]}…</code>.
This page is static and self-contained: every figure is embedded, and it performs zero runtime
calls.</p>
</div>
"""


# --------------------------------------------------------------------------- assembly


TITLE = "Forecasting tomorrow's electricity prices · DE-LU day-ahead research"
DESCRIPTION = (
    "The released day-ahead electricity price forecast for Germany and Luxembourg, and how successive "
    "research models were compared and improved, with every number traced to committed evidence."
)


def stress_chapters() -> str:
    """Local-only placeholders that test the rail and chapter summaries at seven generations.
    Never published: `main()` refuses to write them to docs/."""
    out = []
    for n in (7, 6, 5, 4):
        out.append(
            f'<article class="chapter stress" id="v{n}" aria-labelledby="v{n}-h">'
            f'<header class="chapter-head"><p class="eyebrow">Local stress case · placeholder, not a result</p>'
            f'<h2 id="v{n}-h"><span class="gen">{ver(f"v{n}")}</span> · placeholder generation</h2>'
            f'<p class="chapter-meta">{adoption("Placeholder")}{badge(RC.BADGE_DEVELOPMENT)}</p></header>'
            "<p>This block exists only in the local seven-generation stress case, to check the rail, the jump row and "
            "the chapter rhythm. It carries no score.</p></article>"
        )
    return "".join(out)


def build_html(*, specimen: bool = False, stress: bool = False) -> str:
    C = build_claims()
    payload = build_chart_payload()
    coverage = {str(level): C[f"holdout_coverage_{level}"] for level in INTERVAL_LEVELS}
    archive = v1_archive(payload)
    generations = ("v7", "v6", "v5", "v4", "v3", "v2", "v1") if stress else ("v3", "v2", "v1")
    jump = ('<nav class="jump" aria-label="Chapters">' + "".join(f'<a href="#{g}">{ver(g)}</a>' for g in generations)
            + "</nav>")
    chapters = (stress_chapters() if stress else "") + v3_chapter(open_folds=specimen) + v2_chapter() + v1_chapter(C, archive)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(TITLE)}</title>
<meta name="description" content="{attr(DESCRIPTION)}">
<style>{css()}</style>
</head>
<body>
<a class="skip" href="#main">Skip to the content</a>
{header()}
<div class="page"><div class="with-rail">
{rail(generations)}
<main id="main">
{opening(C, payload)}
{journey()}
{results()}
<section class="section chapters" id="chapters" aria-labelledby="chapters-h">
 <h2 id="chapters-h">How the research improved, newest first</h2>
 <p>Each chapter follows one decision: the problem, the change, what was measured, what it does not show, and
  what was decided. Scrolling down goes back in time.</p>
 {jump}
 {chapters}
</section>
{evidence_section(C)}
{contribution()}
{attribution(C)}
</main>
</div></div>
<footer class="site-footer"><p>{esc(C['attribution'])} This page is static and self-contained: every chart and
figure is embedded, and it makes no runtime call. <a href="#top">Back to the top</a></p></footer>
<script>
window.__FAN__={json.dumps(payload, separators=(",", ":"))};
window.__COV__={json.dumps(coverage, separators=(",", ":"))};
</script>
<dialog class="figure-view" id="figure-view" aria-label="Enlarged figure">
<div class="figure-bar"><p>Scroll to see the whole figure.</p><button type="button" id="figure-close">Close</button></div>
<div class="figure-scroll"><img id="figure-full" alt=""></div>
</dialog>
<script>{CHART_JS}</script>
<script>{NAV_JS}</script>
<script>{FIGURE_JS}</script>
</body>
</html>
"""


def unpublished_markers(document: str) -> list[str]:
    """Placeholders for destinations that do not exist yet (plan §6 invariant 16)."""
    return re.findall(r'data-unpublished="([^"]+)"', document)


class PlaceholderError(RuntimeError):
    """A final build that still shows an unpublished destination."""


def refuse_unpublished(document: str) -> None:
    markers = sorted(set(unpublished_markers(document)))
    if markers:
        raise PlaceholderError(f"final build refused: unpublished destinations remain: {markers}")


# --------------------------------------------------------------------------- D1 specimen extras


def token_sheet() -> str:
    """The visual system on one page: tokens with computed contrast, type, and component states."""
    t = TOKENS
    rows = []
    for name, colour in t.items():
        rows.append(f"<tr><th scope=\"row\"><code>--{name}</code></th><td><span class=\"swatch\" style=\"background:{colour}\"></span>"
                    f"<code>{colour}</code></td><td class=\"n\">{contrast(colour, '#FFFFFF'):.2f}</td>"
                    f"<td class=\"n\">{contrast(colour, t['canvas']):.2f}</td></tr>")
    pairs = [("v1", "v2"), ("v1", "v3"), ("v2", "v3")]
    gen = "".join(f"<li>{a} against {b}: {contrast(t[a], t[b]):.2f}:1</li>" for a, b in pairs)
    unavailable = ('<span class="ev is-unavailable" data-unpublished="specimen">Compare these runs in MLflow '
                   '<span class="why">(available after the tracking upload)</span></span>')
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>PRES-1 D1 token sheet</title>
<style>{css()}
.swatch{{display:inline-block;width:18px;height:18px;border-radius:4px;border:1px solid #D4D4D8;vertical-align:-4px;margin-right:8px}}
.state-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;margin:16px 0 32px}}
.state{{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:16px}}
.state h4{{margin:0 0 10px;font-size:13px;color:var(--text-2);text-transform:uppercase;letter-spacing:.05em}}
.force-hover{{background:var(--primary-hover)!important}}.force-pressed{{background:var(--primary-pressed)!important}}
.force-focus{{outline:2px solid var(--accent);outline-offset:2px}}
</style></head><body><div class="page">
<h1 style="font-size:36px">D1 token sheet</h1>
<p>Plan §7.3 starting tokens, as implemented in <code>scripts/build_pages.py</code>. Contrast is computed here from
the hex values (WCAG relative luminance). Normal text needs 4.5:1 and large text 3:1; state-carrying borders, chart
marks and focus indicators need 3:1.</p>
<div class="scroll"><table class="data"><thead><tr><th>Token</th><th>Value</th><th>vs white</th><th>vs canvas</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>
<p><strong>Generation colours against each other</strong> (why labels and marker shapes always come with them):</p>
<ul>{gen}</ul>
<h2>Type scale</h2>
<p style="font-size:52px;line-height:1.08;font-weight:700;margin:0">Opening 52 px</p>
<p style="font-size:30px;font-weight:700;margin:8px 0">Section 30 px · chapter 32 px (26 px on phones)</p>
<p>Body 16 px on 26 px, prose up to 66 characters. Labels 14 px; tables 14 px; chart text 13 px, never below 12 px
as rendered.</p>
<p class="outcome-value">−0.0783 headline value (30 px, tabular numerals)</p>
<h2>Components and states</h2>
<div class="state-grid">
 <div class="state"><h4>Primary action</h4><p><a class="btn-primary" href="#">Default</a></p>
  <p><a class="btn-primary force-hover" href="#">Hover</a></p><p><a class="btn-primary force-focus" href="#">Focus</a></p>
  <p><a class="btn-primary force-pressed" href="#">Pressed</a></p></div>
 <div class="state"><h4>Quiet link</h4><p><a class="quiet" href="#">Default</a></p><p><a class="quiet" style="text-decoration-thickness:2px" href="#">Hover</a></p>
  <p><a class="quiet force-focus" href="#">Focus</a></p><p><a class="quiet external" href="#">External destination</a></p></div>
 <div class="state"><h4>Evidence badge</h4><p>{badge(RC.BADGE_DEVELOPMENT)}</p><p style="max-width:180px">{badge(RC.BADGE_V1_HOLDOUT, "holdout")}</p>
  <p class="archive-note">The long badge wraps rather than truncating.</p></div>
 <div class="state"><h4>Adoption label</h4><p>{adoption(RC.ADOPTED)}</p><p>{adoption(RC.NOT_ADOPTED)}</p><p>{adoption(RC.PLANNED)}</p></div>
 <div class="state"><h4>Evidence row</h4>{evidence_row(compare="specimen", review=("Reviewed result", "#"), source=("Source rows", "#"))}
  <p class="archive-note">Available links; the unavailable state is shown for an unpublished destination:</p><p>{unavailable}</p></div>
 <div class="state"><h4>Disclosure</h4>{disclosure("spec-closed", "Closed", "<p>Body</p>")}{disclosure("spec-open", "Open", "<p>The body of an open disclosure.</p>", open_=True)}</div>
 <div class="state"><h4>Data table with a long exact value</h4><div class="scroll"><table class="data"><thead><tr><th>Contrast</th><th>Upper end</th></tr></thead>
  <tbody><tr><th scope="row">v2 − pooled control</th><td class="exact">{value("cp16.uncertainty.V2-H-V2-P.equal_fold.MAE", "C34", option="exact_hi")}</td></tr></tbody></table></div></div>
 <div class="state"><h4>Lineage nodes</h4>{lineage()}</div>
</div>
</div></body></html>"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--specimen", type=Path, default=None,
                        help="write the D1 specimen (page, token sheet, demo states, stress case) to this directory")
    parser.add_argument("--final", action="store_true", help="refuse any unpublished-link marker")
    args = parser.parse_args()
    if args.specimen:
        out = args.specimen
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(build_html(specimen=True))
        (out / "stress-7.html").write_text(build_html(specimen=True, stress=True))
        (out / "token-sheet.html").write_text(token_sheet())
        sys.path.insert(0, str(ROOT / "scripts"))
        from build_wasm_space import demo_states_specimen

        (out / "demo-states.html").write_text(demo_states_specimen())
        print(f"wrote the D1 specimen to {out}")
        return 0
    document = build_html()
    markers = unpublished_markers(document)
    if args.final:
        try:
            refuse_unpublished(document)
        except PlaceholderError as exc:
            raise SystemExit(str(exc))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(document)
    (OUTPUT.parent / ".nojekyll").write_text("")
    BUILD_RECORD.parent.mkdir(parents=True, exist_ok=True)
    BUILD_RECORD.write_text(
        json.dumps(
            {
                "output": str(OUTPUT.relative_to(ROOT)),
                "bytes": len(document.encode()),
                "load_scale_points": len(LOAD_SCALES),
                "build_path": "purpose-built static assembly (§9.2 fallback)",
                "marimo_export_html_rejected_because": (
                    "measured 2026-09-14 with marimo 0.24.2: `marimo export html` emits 181 "
                    "external references to cdn.jsdelivr.net (frontend JS bundle, CSS and five "
                    "web fonts), so the page cannot render without network. CP-3 item 3 requires "
                    "zero runtime calls."
                ),
                "marimo_export_external_reference_count": 181,
                "marimo_export_external_hosts": ["cdn.jsdelivr.net"],
                "final": bool(args.final),
                "unpublished_markers": sorted(set(markers)),
                "built_on": date.today().isoformat(),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    print(f"wrote {OUTPUT} ({len(document):,} bytes) and {OUTPUT.parent / '.nojekyll'}")
    print(f"wrote {BUILD_RECORD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
