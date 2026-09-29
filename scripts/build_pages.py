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
    uv run python scripts/build_pages.py --final               # refuse unless every expected route is verified
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
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from delu_forecast import registry as G  # noqa: E402
from delu_forecast import research as R  # noqa: E402
from delu_forecast import research_claims as RC  # noqa: E402
from delu_forecast import derived as D  # noqa: E402
from delu_forecast.claims import MLFLOW_NEXT_NOTE_BEFORE_UPLOAD as ARCHIVE_TRACKING_NOTE  # noqa: E402
from delu_forecast.claims import (  # noqa: E402
    GFS_ATTRIBUTION,
    MLFLOW_RUN_NAMES,
    build_claims,
    limitation_bullets,
    reproducibility_bullets,
)
from delu_forecast.claims import LIMITATION_KEYS as C_LIMITATION_KEYS  # noqa: E402
from delu_forecast.claims import LIMITATION_LABELS as C_LABELS  # noqa: E402
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
#: The demo's measured start (plan §7.11, PUBLISH_RULES 1.0 §7.1): fresh anonymous cold starts of the public demo,
#: recorded by `scripts/check_reader_paths.py demo`. The page states the record's own browser, machine and dates.
DEMO_CHECK = ROOT / "reports" / "presentation" / "release-checks" / "pres-2-public-demo-baseline.json"
#: The released model's inputs, from its committed card: identity, not a result.
CHAMPION_CARD = ROOT / "models" / "champion" / "champion_card.json"

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


def marker_problems(styles: dict | None = None) -> list[str]:
    """Colour is never the only cue (plan §7.3, invariant 22): every registered generation has a
    marker style, each generation's shape is its own, and no two styles look the same."""
    styles = ROLE_STYLE if styles is None else styles
    problems = []
    generations = [entry.style for entry in G.generations()]
    for style in generations:
        if style not in styles:
            problems.append(f"{style} has no marker style")
    shapes = [styles[style]["marker"] for style in generations if style in styles]
    for style in generations:
        if style in styles and shapes.count(styles[style]["marker"]) > 1:
            problems.append(f"{style} shares its marker shape with another generation")
    looks = [(spec["marker"], spec["filled"], spec["color"]) for spec in styles.values()]
    if len(looks) != len(set(looks)):
        problems.append("two marker styles are identical")
    return problems


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


def block(key: str, tag: str = "p", cls: str | None = None, ident: str | None = None) -> str:
    """A claim block rendered from its template, wrapped so tests can find it."""
    klass = f' class="{cls}"' if cls else ""
    id_attr = f' id="{ident}"' if ident else ""
    return f'<{tag}{id_attr}{klass} data-block="{key}">{RC.render(key)}</{tag}>'


def value(record_id: str, claim_id: str, which: str = "value", option: str | None = None) -> str:
    """One research value in HTML, outside a sentence template."""
    token = {"value": "", "ci_low": "|lo", "ci_high": "|hi"}[which] if not option else f"|{option}"
    return RC.render_template(claim_id, "{r:%s%s}" % (record_id, token))


def interval(record_id: str, claim_id: str, *, exact: bool = False) -> str:
    return RC.render_template(claim_id, "{r:%s|%s}" % (record_id, "ciexact" if exact else "ci"))


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
    """The committed index of verified public MLflow routes. The mirror verifier writes it, never a
    person (standard §8); a route is on the page only once it is in here (§9)."""
    if MLFLOW_INDEX.exists():
        return json.loads(MLFLOW_INDEX.read_text())
    return {}


def mlflow_route(route_id: str) -> str | None:
    """A verified route's URL, or None: a route that is not verified has its link omitted (§9)."""
    return mlflow_index().get("routes", {}).get(route_id, {}).get("url")


@dataclass(frozen=True)
class Audit:
    """An audit-grade record (standard §7): linked only from an evidence row, at its evidence tag,
    and labelled with its type and the date that tag froze it."""

    kind: str
    path: str
    tag: str
    line: int | None = None

    @property
    def date(self) -> str:
        return G.EVIDENCE_TAGS[self.tag][1]

    @property
    def url(self) -> str:
        return github(self.path, self.tag, self.line)

    def label(self) -> str:
        return f"{self.kind}, frozen {self.date}"


def audit_link(item: Audit) -> str:
    """An audit-grade link, "<type>, frozen <date>". The label is one span: an `.ev` link is a flex
    box, and a flex item drops the space before the date that follows it ("frozen2026-09-16")."""
    return (f'<a class="ev external audit" href="{attr(item.url)}" data-evidence-tag="{attr(item.tag)}">'
            f'<span>{esc(item.kind)}, frozen {S("date", item.date)}</span></a>')


def evidence_row(*, compare: str | None = None, audit: tuple[Audit, ...] = ()) -> str:
    """"Compare the runs in MLflow" (reader grade, only once verified) and the audit-grade records
    behind the result, each "<type>, frozen <date>" (standard §7, plan §7.9)."""
    items = []
    url = mlflow_route(compare) if compare else None
    if url:
        items.append(f'<a class="ev external reader" href="{attr(url)}" data-route="{attr(compare)}">'
                     "Compare the runs in MLflow</a>")
    for item in audit:
        items.append(audit_link(item))
    return '<p class="evidence-row"><span class="ev-label">Evidence</span>' + "".join(items) + "</p>"


def checkpoint_audit(code: str, *, source: str | None = None, line: int | None = None,
                     report: bool = True) -> tuple[Audit, ...]:
    """The standard evidence of one checkpoint: its review verdict, its engineering report and,
    when given, the raw rows a chart reads -- all at the checkpoint's evidence tag."""
    checkpoint = G.CHECKPOINTS[code]
    items = [Audit("Review verdict", checkpoint.verdict, checkpoint.evidence_tag)]
    if report:
        items.append(Audit("Engineering report", checkpoint.report, checkpoint.evidence_tag))
    if source:
        items.append(Audit("Raw CSV rows", source, checkpoint.evidence_tag, line))
    return tuple(items)


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
    #: The row's verdict against the targets, bound to its derived record (standard §3.3 a, §15).
    verdict: str | None = None


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


def end_label(value: float) -> str:
    """An axis end or tick label that states its value exactly: 7.5, never a rounded 8."""
    text = f"{value:.3f}".rstrip("0").rstrip(".")
    return text.replace("-", R.MINUS) if value < 0 else text


def tick_text(value: float, step: float) -> str:
    places = max(0, -int(math.floor(math.log10(step)))) if step < 1 else 0
    text = f"{value:.{places}f}"
    return text.replace("-", R.MINUS) if value < 0 else text


def svg_text(x: float, y: float, text: str, *, size: int = CHART_FONT, anchor: str = "start",
             weight: str | None = None, fill: str | None = None, extra: str = "") -> str:
    style = f' font-weight="{weight}"' if weight else ""
    colour = fill or TOKENS["text"]
    if "data-" not in extra and any(ch.isdigit() for ch in text):
        # a chart's fixed wording: a nominal level ("95% interval") or a fold or version label
        extra += ' data-structural="level"' if re.search(r"\d%", text) else ' data-structural="label"'
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{colour}"'
            f"{style}{extra}>{esc(text)}</text>")


def marker(x: float, y: float, role: str, *, size: float = 6.0, extra: str = "", style: dict | None = None) -> str:
    style = style or ROLE_STYLE[role]
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
    #: One display precision per chart (standard §4): "p=N" for every value the panel prints.
    option: str | None = None


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
                    size: int = CHART_FONT, *, x_left: float | None = None, option: str | None = None) -> str:
    claim_id = row.claim or claim_id
    record = R.get(row.record_id)
    weight = "600" if row.bold else None
    if record.interval is not None:
        # "estimate [low, high]", each figure a tspan bound to its own field of the record
        def part(which: str) -> str:
            return (f'<tspan{RC.svg_binding(claim_id, row.record_id, which)}>'
                    f'{esc(RC.svg_value(row.record_id, which, option))}</tspan>')

        body = f'{part("value")} [{part("ci_low")}, {part("ci_high")}]'
        style = f' font-weight="{weight}"' if weight else ""
        x, anchor = (x_left, "start") if x_left is not None else (x_right, "end")
        return (f'<text x="{x:.1f}" y="{y + 4.5:.1f}" font-size="{size}" text-anchor="{anchor}" '
                f'fill="{TOKENS["text"]}"{style}{HALO}>{body}</text>')
    near_right = x_mark > x_right - 58
    return value_label(x_mark + (-10 if near_right else 10), y + 4.5, claim_id, row.record_id,
                       anchor="end" if near_right else "start", size=size, weight=weight, option=option)


def single_rows(chart_id: str, claim_id: str, panels: list[Panel], *, title: str, desc: str,
                label_width: int = 250, row_h: int = 38, values_inline: bool = True) -> str:
    """Categorical rows with one mark each, optionally with its confidence interval.

    Dot plots (no intervals) put their panels side by side and label each mark. Interval charts
    give every row a value column -- "estimate [low, high]" -- and stack their panels, so an
    interval never collides with its own label. Phones get a dedicated stacked variant. A row may
    carry its verdict against the targets, drawn in a column of its own (standard §15)."""
    for panel in panels:
        _check_panel_units(panel)
    has_interval = any(R.get(row.record_id).interval for panel in panels for row in panel.rows)
    verdicts = [row.verdict for row in panels[0].rows]
    verdict_w = 96 if any(verdicts) else 0
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

    def verdict_text(x: float, y: float, row: Row, anchor: str = "start") -> str:
        if row.verdict is None:
            return svg_text(x, y, "—", anchor=anchor, fill=TOKENS["text-2"], extra=' aria-hidden="true"')
        text = RC.svg_value(row.verdict)
        return svg_text(x, y, text, anchor=anchor, weight="600" if text == "met" else None,
                        extra=RC.svg_binding("P16", row.verdict) + HALO)

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
                parts.append(_row_value_text(scale, 0, cy, row, claim_id, DESKTOP_W, option=panel.option))
            y = bottom + 48
        height = y
    else:
        gap = 40
        panel_w = (DESKTOP_W - label_width - verdict_w - gap * (len(panels) - 1)) / len(panels)
        # a subtitle wraps inside its panel (about 7 px per character of 13 px text)
        sub_chars = max(24, int((panel_w + gap - 8) / 7.0))
        sub_lines = [_wrap(panel.subtitle, sub_chars) for panel in panels]
        extra = 17 * (max(len(lines) for lines in sub_lines) - 1)
        body_top = 66 + extra
        n = len(panels[0].rows)
        body_bottom = body_top + n * row_h
        height = body_bottom + 34
        for index, row in enumerate(panels[0].rows):
            cy = body_top + index * row_h + row_h / 2
            parts.append(svg_text(0, cy + 4.5, row.label, weight="600" if row.bold else None))
            if verdict_w:
                parts.append(verdict_text(DESKTOP_W - verdict_w + 12, cy + 4.5, row))
        if verdict_w:
            parts.append(svg_text(DESKTOP_W - verdict_w + 12, 16, "Targets", weight="600"))
            parts.append(svg_text(DESKTOP_W - verdict_w + 12, 34, "both met?", fill=TOKENS["text-2"]))
        for p_index, panel in enumerate(panels):
            x0 = label_width + p_index * (panel_w + gap) + 8
            x1 = x0 + panel_w - 16
            scale = Scale(panel.scale_id, panel.domain[0], panel.domain[1], x0, x1, _check_panel_units(panel))
            parts.append(svg_text(x0 - 8, 16, panel.title, weight="600"))
            for line_index, line in enumerate(sub_lines[p_index]):
                parts.append(svg_text(x0 - 8, 34 + 17 * line_index, line, fill=TOKENS["text-2"]))
            refs_and_ticks(panel, scale, body_top, body_bottom, 54 + extra, False)
            for index, row in enumerate(panel.rows):
                cy = body_top + index * row_h + row_h / 2
                record = R.get(row.record_id)
                parts.append(marker(scale(record.value), cy, row.role,
                                    extra=RC.svg_binding(row.claim or claim_id, row.record_id)))
                if values_inline:
                    parts.append(_row_value_text(scale, scale(record.value), cy, row, claim_id, x1, option=panel.option))
    desktop = svg_wrap(DESKTOP_W, height, "".join(parts), title=title, desc=desc, variant="d", chart_id=chart_id)

    # ---- phone: stacked panels; each row is its label (wrapped), then its mark, then its values
    parts = []
    y_cursor = 0.0
    for p_index, panel in enumerate(panels):
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
            # the verdict prints once, in the first panel, on its own line under the label
            with_verdict = verdict_w and p_index == 0
            if with_verdict:
                y_mark += 17
            layout.append((row, lines, y_label, y_mark, with_verdict))
            y = y_mark + (40 if has_ci else 26)
        bottom = y
        refs_and_ticks(panel, scale, top, bottom, label_y, True)
        for row, lines, y_label, y_mark, with_verdict in layout:
            record = R.get(row.record_id)
            for line_index, line in enumerate(lines):
                # reference lines cross the label line on a phone; the halo keeps the label legible
                parts.append(svg_text(0, y_label + 17 * line_index, line, weight="600" if row.bold else None,
                                      extra=' data-structural="label"' * any(c.isdigit() for c in line) + HALO))
            if with_verdict:
                y_verdict = y_label + 17 * len(lines)
                parts.append(svg_text(0, y_verdict, "targets:", fill=TOKENS["text-2"], extra=HALO))
                parts.append(verdict_text(62, y_verdict, row))
            if record.interval is not None:
                parts.append(_interval_marks(scale, y_mark, record, row.role, row.claim or claim_id))
                parts.append(_row_value_text(scale, 0, y_mark + 19, row, claim_id, MOBILE_W, x_left=0,
                                             option=panel.option))
            parts.append(marker(scale(record.value), y_mark, row.role,
                                extra=RC.svg_binding(row.claim or claim_id, row.record_id)))
            if record.interval is None:
                parts.append(_row_value_text(scale, scale(record.value), y_mark, row, claim_id, x1, option=panel.option))
        y_cursor = bottom + 54
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
        title_text, subtitle, rows, domain, step, option = panel
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
                out.append(svg_text(x0, y_mark + 17, end_label(lo), size=CHART_FONT, fill=TOKENS["text-2"],
                                    extra=f' data-scale="{scale.ident}"'))
                out.append(svg_text(x1, y_mark + 17, end_label(hi), size=CHART_FONT, anchor="end",
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
                text = RC.svg_value(record_id, "value", option)
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
            out.append(svg_text(x0 - 6, y + 4.5, end_label(tick), anchor="end", fill=TOKENS["text-2"],
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
    parts.append(svg_text(0, cursor + 14, "x: local delivery hour (Europe/Berlin) · y: MAE, EUR/MWh, lower is better · each fold on its own scale",
                          fill=TOKENS["text-2"]))
    desktop = svg_wrap(DESKTOP_W, cursor + 24, "".join(parts), title=title, desc=desc, variant="d", chart_id=chart_id)
    parts, cursor = [], 0.0
    for fold in folds:
        body, cursor = draw(MOBILE_W, 44, MOBILE_W - 34, cursor, fold, 96)
        parts.append(body)
    for index, line in enumerate(_wrap("x: local delivery hour · y: MAE, EUR/MWh, lower is better · each fold on its own scale", MOBILE_LINE_CHARS)):
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
        # The tint alone is about 1.3:1 against the panel; the outline carries the band's extent at 3:1 or more.
        out.append(f'<polygon points="{" ".join(band)}" fill="{TOKENS["v1"]}" fill-opacity="0.18" '
                   f'stroke="{TOKENS["ref"]}" stroke-width="1"/>')
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
    mobile = svg_wrap(MOBILE_W, 164, draw(MOBILE_W, 164, 40, "m"), title=title, desc=desc, variant="m",
                      chart_id="preview")
    return f'<div class="chart preview-chart" data-chart-id="preview">{desktop}{mobile}</div>'


# --------------------------------------------------------------------------- lineage (§7.7) and planned work (§8.6)


PLANNED_WORK = (
    ("Alternative model families", "4.6", "DDNN / TabPFN",
     "Does a distributional network, or a tabular foundation model, beat v3?",
     "One predefined comparison on identical hours"),
    ("Wind and solar generation forecasts", "4.4V", "VRE",
     "Does an in-house wind and solar generation forecast add information beyond direct weather?",
     "A held-forward generation model, then an ablation"),
    ("Models for different parts of the day", "4.5", "Three-block LightGBM",
     "Do separate models for different hours improve forecasts?", "A per-block comparison on identical hours"),
    ("Combining models", "4.8", "Recombination", "Does combining adopted models help?",
     "A predefined combination test"),
    ("Frozen-protocol evaluation, then prospective monitoring", "4.7T and live", "Final evaluation",
     "How does the selected model perform under a frozen evaluation protocol, and then prospectively?",
     "An evaluation window and an evidence classification, both fixed in the protocol before the test"),
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


# --------------------------------------------------------------------------- charts on the page

_HG_MAE = "cp20.uncertainty.HG-H0.equal_fold.MAE"
_HG_WIS = "cp20.uncertainty.HG-H0.equal_fold.WIS"
FOLDS = ("fold_1", "fold_2", "fold_3", "fold_4", "fold_5")

def _rows_of(order, experiment: str) -> tuple[tuple[str, str, str, bool, str | None], ...]:
    """(code, style, label, bold, verdict) for registry entries in a chart's order: the code each
    carries in the experiment whose rows the chart draws, its registry label and its target verdict."""
    out = []
    for entry in (G.get(ident) if isinstance(ident, str) else ident for ident in order):
        verdict = f"derived.criteria.{entry.id}.verdict"
        out.append((entry.code_in(experiment), entry.style, comparison_label(entry, experiment),
                     entry.kind == "generation", verdict if verdict in D.records() else None))
    return tuple(out)


def overview_table() -> str:
    """The comparison's values, exact (standard §4): scores, the target verdict and distance, pooled errors."""
    rows = []
    for entry in G.comparison_rows():
        code = entry.code_in(G.COMPARISON_EXPERIMENT)
        cells = [f'<th scope="row">{_structural_versions(comparison_label(entry))} <span class="code">{S("code", code)}</span></th>']
        for field in ("S_MAE", "S_WIS"):
            cells.append(f'<td class="n exact">{value(f"cp20.metrics.{code}.equal_fold.{field}", "P07", option="exact")}</td>')
        base = f"derived.criteria.{entry.id}"
        if f"{base}.verdict" in D.records():
            cells.append(f'<td>{value(f"{base}.verdict", "P16")}</td>')
            cells.append(f'<td class="n">{value(f"{base}.distance.S_MAE", "P16", option="exact")} / '
                         f'{value(f"{base}.distance.S_WIS", "P16", option="exact")}</td>')
        else:
            cells.append('<td>—</td><td class="n">—</td>')
        for field in ("MAE", "WIS"):
            cells.append(f'<td class="n exact">{value(f"cp20.metrics.{code}.pooled.{field}", "C74", option="exact")}</td>')
        rows.append("<tr>" + "".join(cells) + "</tr>")
    return (
        '<div class="scroll" role="region" aria-label="The seven policies, table" tabindex="0"><table class="data">'
        "<caption>Equal-fold error scores (ratio to the naive), the targets, and pooled errors (EUR/MWh), identical hours</caption>"
        '<thead><tr><th scope="col">Policy</th><th scope="col">Point-error score (S_MAE)</th>'
        '<th scope="col">Interval score (S_WIS)</th><th scope="col">Both targets</th>'
        '<th scope="col">Distance from daily LEAR, point / interval, percent</th>'
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


def _generation_codes() -> tuple[tuple[str, str], ...]:
    """(style, code in the shared comparison) for every generation, oldest first."""
    return tuple((entry.style, entry.code_in(G.COMPARISON_EXPERIMENT)) for entry in G.generations())


def _hour_series() -> tuple[tuple[str, str], ...]:
    """The hour-of-day chart's two series: the current generation's comparator, then the generation."""
    current = G.current_generation()
    comparator = G.get(current.comparator)
    return tuple((entry.style, entry.code_in(G.COMPARISON_EXPERIMENT)) for entry in (comparator, current))


def c2a_panels() -> list[Panel]:
    return [Panel("Difference, v3 − v2", "error-score difference · below zero favours v3",
                  (Row("Point-error score", _HG_MAE, "v3", bold=True, claim="C69"),
                   Row("Interval score", _HG_WIS, "v3", bold=True, claim="C70")),
                  domain=(-0.12, 0.02), step=0.02,
                  refs=(Ref("no difference", at=0.0, dash=None, colour=TOKENS["text"]),))]


def c2a_chart() -> str:
    return single_rows(
        "v3-c2a", "C69", c2a_panels(),
        title="v3 minus v2: equal-fold error-score differences with 95 percent confidence intervals",
        desc="Two rows, the point-error score and the interval score. Each shows the estimated difference as a dot "
             "and its 95 percent confidence interval as a line; both lie wholly left of zero, which favours v3.",
        label_width=230, row_h=56,
    )


def c2b_panels() -> list[Panel]:
    def panel(metric: str, title: str) -> Panel:
        return Panel(title, "EUR/MWh, paired mean daily loss · below zero favours v3",
                     tuple(Row(f"Fold {fold[-1]}" + (" (crisis)" if fold == "fold_3" else ""),
                               f"cp20.uncertainty.HG-H0.{fold}.{metric}", "v3") for fold in FOLDS),
                     domain=(-7.0, 1.0), step=1.0,
                     refs=(Ref("no difference", at=0.0, dash=None, colour=TOKENS["text"]),), option="p=1")
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
            ids = {role: f"cp20.metrics.{code}.{fold}.{metric}" for role, code in _generation_codes()}
            top = max(R.get(rid).value for rid in ids.values())
            magnitude = 10 ** math.floor(math.log10(top))
            hi = math.ceil(top * 1.08 / magnitude * 2) * magnitude / 2
            out.append(MultiRow(f"Fold {fold[-1]}", tuple((role, rid) for role, rid in ids.items()), domain=(0.0, hi)))
        return tuple(out)
    return [("MAE by fold, EUR/MWh", "lower is better", rows("MAE"), None, 1.0, "p=1"),
            ("WIS by fold, EUR/MWh", "lower is better", rows("WIS"), None, 1.0, "p=1")]


def c3_chart() -> str:
    return multi_rows(
        "v3-c3", "C74", c3_panels(),
        title="MAE and WIS per fold for v1, v2 and v3",
        desc="For each fold, three markers on that fold's own scale: v1 triangle, v2 square, v3 circle, with the "
             "values printed underneath.",
        scale_note="Each fold has its own scale, shared by the three generations inside it.",
    )


def c4_panels() -> list[Panel]:
    def crisis_rows(saved: str, evaluated: str) -> tuple[Row, ...]:
        # v1 and the study arm carry CP-15's saved crisis rows; later generations their own checkpoint's.
        rows = []
        for entry in (G.get(ident) for ident in G.CRISIS_ORDER):
            code = entry.code_in(G.COMPARISON_EXPERIMENT)
            record = (saved.format(code=entry.code_in("CP-15")) if entry.code_in("CP-15")
                      else evaluated.format(code=code))
            label = entry.short if entry.kind == "generation" else comparison_label(entry, "CP-15")
            rows.append(Row(label, record, entry.style, bold=entry.kind == "generation"))
        return tuple(rows)

    rows_mae = crisis_rows("cp15.peak.{code}.MAE", "cp20.criteria.{code}.c4.peak.MAE")
    rows_hits = crisis_rows("cp15.peak.{code}.hit_count95", "cp20.diagnostics.{code}.peak.hit_count95")
    window_hours = R.get("cp20.diagnostics.HG.peak.n_hours").value
    nominal = Ref("nominal 95%", at=0.95 * window_hours)  # the target 95% of the window's hours, not an observation
    return [Panel("MAE, EUR/MWh", "lower is better", rows_mae, domain=(0.0, 300.0), step=50.0, option="p=1"),
            Panel("Hours inside the 95% interval", "count of hours in the window · closer to the nominal line is better",
                  rows_hits, domain=(0.0, 420.0), step=100.0, refs=(nominal,))]


def c4_chart() -> str:
    return single_rows(
        "v3-c4", "C79", c4_panels(),
        title="The 2022 crisis window: point error and hours inside the 95 percent interval",
        desc="Four policies on the matched crisis window, delivery 15 to 31 August 2022. Descriptive only.",
        label_width=210,
    )


def c5_chart() -> str:
    return hour_panels("v3-c5", "C82", _hour_series(),
                       title="MAE by local hour, v2 against v3, per fold",
                       desc="Five panels, one per fold, each on its own scale: v2 dashed with squares, v3 solid "
                            "with circles. Descriptive only.")


def standalone_svg(chart_html: str) -> str:
    """A chart's desktop drawing as a standalone SVG file: the page's drawing, plus the width and
    height a viewer needs when the file is shown on its own (they equal the viewBox)."""
    match = re.search(r'<svg class="d".*?</svg>', chart_html, re.DOTALL)
    if match is None:
        raise ValueError("no desktop drawing in this chart")
    width, height = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', match.group(0)).groups()
    drawing = match.group(0).replace("<svg ", f'<svg width="{width}" height="{height}" ', 1)
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + drawing + "\n"


def c6_panels():
    def rows(kind: str) -> tuple[MultiRow, ...]:
        out = []
        for level in ("50", "80", "95"):
            field = f"coverage{level}" if kind == "coverage" else f"mean_width{level}"
            marks = tuple((role, f"cp20.metrics.{code}.pooled.{field}") for role, code in _generation_codes())
            ref = Ref(f"nominal {level}%", at=int(level) / 100) if kind == "coverage" else None
            out.append(MultiRow(f"{level}% interval", marks, ref=ref))
        return tuple(out)
    return [("Coverage (fraction)", "closer to nominal is better", rows("coverage"), (0.3, 1.0), 0.1, None),
            ("Mean interval width, EUR/MWh", "narrower at equal coverage is better", rows("width"), (0.0, 140.0), 20.0,
             "p=1")]


def c6_chart() -> str:
    return multi_rows(
        "v3-c6", "C80", c6_panels(),
        title="Coverage and mean interval width at 50, 80 and 95 percent, pooled",
        desc="For each nominal level, coverage and mean width for v1, v2 and v3. A black tick marks the nominal "
             "coverage. Higher coverage is not better on its own if the intervals widen.",
    )


def v2_chart2_panels() -> list[Panel]:
    """v2's three contrasts. Each row names both policies; below zero favours the first named."""
    v2, lear, control = G.get("v2"), G.get("daily-lear"), G.get("pooled-control")
    rows = ((f"{v2.version} − {G.inline_name(lear)}", "V2-H-B2", "v2", True, "C37", v2.version),
            (f"{v2.version} − {G.inline_name(control)}", "V2-H-V2-P", "v2", False, None, v2.version),
            (f"control − {G.inline_name(lear)}", "V2-P-B2", "control", False, "C38", "the control"))

    def panel(metric: str, title: str) -> Panel:
        return Panel(title, f"error-score difference · below zero favours {v2.version} in the first two rows, "
                            "the control in the third",
                     tuple(Row(label, f"cp16.uncertainty.{pair}.equal_fold.{metric}", role, bold=bold,
                               claim=claim or ("C34" if metric == "MAE" else "C33"))
                           for label, pair, role, bold, claim, _ in rows),
                     domain=(-0.04, 0.01), step=0.01,
                     refs=(Ref("no difference", at=0.0, dash=None, colour=TOKENS["text"]),))
    return [panel("MAE", "Point-error score"), panel("WIS", "Interval score")]


def v2_chart2() -> str:
    return single_rows(
        "v2-chart2", "C37", v2_chart2_panels(),
        title="v2's paired equal-fold error-score differences with 95 percent confidence intervals",
        desc="Three contrasts in two panels. Against daily LEAR both intervals lie below zero. Against the "
             "pooled-interval control the interval-score interval is below zero but the point-error interval ends "
             "just above zero.",
        label_width=190, row_h=56,
    )


def v2_chart1_panels() -> list[Panel]:
    rows = _rows_of(G.V2_SCORES_ORDER, "CP-16")

    def panel(field: str, title: str, limit: str) -> Panel:
        return Panel(title, "ratio to the naive · lower is better",
                     tuple(Row(label, f"cp16.metrics.{code}.equal_fold.{field}", role, code, bold, verdict=verdict)
                           for code, role, label, bold, verdict in rows),
                     domain=(0.55, 1.1), step=0.1,
                     refs=(Ref("naive", at=1.0, dash=None, colour=TOKENS["text"]), Ref("target", limit)),
                     option="p=3")
    return [panel("S_MAE", "Point-error score", "cp16.criteria.V2-H.c1.equal_fold.S_MAE.upper_limit"),
            panel("S_WIS", "Interval score", "cp16.criteria.V2-H.c2.equal_fold.S_WIS.upper_limit")]


def v2_chart1() -> str:
    return single_rows(
        "v2-chart1", "C31", v2_chart1_panels(),
        title="Equal-fold error scores at the time of v2, against the targets",
        desc="Six policies from the v2 study; both v2 arms have the lowest ratios but stay above the targets.",
        label_width=236,
    )


#: The charts the MLflow export attaches to the candidate runs they show (plan §10.6).
CHARTS_BY_RUN = {
    "cp20/HG": (("overview", lambda: overview_chart()), ("v3-c2a", c2a_chart), ("v3-c2b", c2b_chart),
                ("v3-c3", c3_chart), ("v3-c4", c4_chart), ("v3-c5", c5_chart), ("v3-c6", c6_chart)),
    "cp16/V2-H": (("v2-chart1", v2_chart1), ("v2-chart2", v2_chart2)),
}


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
            text = value(row.record_id, claim, option="exact")
            if record.interval is not None:
                text += f' <span class="ci">{interval(row.record_id, claim, exact=True)}</span>'
            cells.append(f'<td class="n exact">{text}</td>')
        body.append("<tr>" + "".join(cells) + "</tr>")
    table_html = (f'<div class="scroll" role="region" aria-label="Values" tabindex="0"><table class="data">'
                  f"<thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table></div>")
    return disclosure(ident, "View values", table_html)


def multi_values_table(ident: str, claim_id: str, panels) -> str:
    parts = []
    for title, _subtitle, rows, _domain, _step, _option in panels:
        roles = [role for role, _ in rows[0].marks]
        head = '<th scope="col">Row</th>' + "".join(f'<th scope="col">{ver(role) if role.startswith("v") else esc(role)}</th>'
                                                    for role in roles)
        body = "".join(
            f'<tr><th scope="row">{_label(row.label)}</th>'
            + "".join(f'<td class="n exact">{value(record_id, claim_id, option="exact")}</td>' for _, record_id in row.marks) + "</tr>"
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
        cells = "".join(f'<td class="n exact">{value(f"cp20.diagnostics.{code}.{fold}.hour_{hour:02d}.MAE", claim_id, option="exact")}</td>'
                        for fold in FOLDS for _, code in series)
        body.append(f'<tr><th scope="row">{S("hour", str(hour))}</th>{cells}</tr>')
    table_html = ('<div class="scroll" role="region" aria-label="MAE by hour and fold" tabindex="0"><table class="data">'
                  "<caption>MAE by local hour, EUR/MWh</caption>"
                  f"<thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table></div>")
    return disclosure(ident, "View values", table_html)


def legend(roles: tuple[str, ...]) -> str:
    names = {**{entry.style: entry.version for entry in G.generations()}, **G.STYLE_LABELS}
    items = []
    for role in roles:
        svg = (f'<svg class="legend-mark" viewBox="-8 -8 16 16" width="16" height="16" aria-hidden="true">'
               f'{marker(0, 0, role, size=5)}</svg>')
        items.append(f'<li>{svg}<span>{_structural_versions(names[role])}</span></li>')
    return '<ul class="legend" aria-label="Marker key">' + "".join(items) + "</ul>"


# --------------------------------------------------------------------------- sections


def demo_measurement(path: Path = DEMO_CHECK) -> dict:
    """The measured start beside the demo action (plan §7.11; PUBLISH_RULES 1.0 §7.1, review F03): the desktop
    Chrome cold start of the public demo, with its browser, machine and date, and the last date on which every
    run in the record reached a forecast. Every value is read from the record; none is typed."""
    record = json.loads(path.read_text())
    runs = record["runs"]
    run = next(r for r in runs if r.get("engine") == "chrome" and r.get("viewport") == "1440x900" and r.get("ready"))
    if not run.get("url", "").startswith("https://"):
        raise ValueError(f"{path.name}: the measured start must come from the public demo, not {run.get('url')!r}")
    verified = [r["started_utc"][:10] for r in runs if r.get("ready")]
    if len(verified) != len(runs):
        raise ValueError(f"{path.name}: a run did not reach a forecast; the page cannot call the demo verified")
    return {"seconds": run["seconds_to_visible_forecast"], "browser": run["browser_version"],
            "machine": "a Mac" if "Darwin" in record["host"] else record["host"],
            "date": run["started_utc"][:10], "verified": max(verified),
            "path": str(path.relative_to(ROOT))}


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


def chapter_sequence(C, archive: str, *, specimen: bool = False) -> str:
    """Every generation's chapter, newest first, in the registry's order. A registered generation
    without a chapter builder is a build error, never a silent omission."""
    builders = {"v3": lambda: v3_chapter(open_folds=specimen), "v2": v2_chapter, "v1": lambda: v1_chapter(C, archive)}
    missing = [version for version in chapter_versions() if version not in builders]
    if missing:
        raise G.RegistryError(f"registered generations without a chapter: {missing}")
    return "".join(builders[version]() for version in chapter_versions())


def opening(C, payload) -> str:
    """The opening (standard §1, §6): title, description, the status pair carrying the headline block
    and the terms it introduces, the actions, the release rule beside the demo action, the preview."""
    demo = demo_measurement()
    released, research = G.released(), G.current_generation()
    measured = (f'<span data-release-check="{attr(demo["path"])}#seconds_to_visible_forecast">'
                f'{esc(demo["seconds"])}</span>')
    # Beside the action, outside any disclosure (review F03): size, measured start, browser, machine and dates.
    startup = (
        f'<p class="startup" data-startup="measured">Runs in your browser: about {v1("wasm_cold_load_mb", "P13")} MB '
        f'on a first visit. A forecast appeared after {measured} s in Chrome '
        f'{S("version", demo["browser"].split(".")[0])} on {esc(demo["machine"])}, public demo, '
        f'{S("date", demo["date"])}; last verified {S("date", demo["verified"])}.</p>'
    )
    terms = "".join(f'<li data-block="{key}">{RC.render(key)}</li>' for key in HEADLINE_TERMS)
    return f"""
<section class="opening" id="top" aria-labelledby="title">
 <div class="opening-copy">
  <p class="eyebrow">German–Luxembourg electricity market</p>
  <h1 id="title">Day-ahead electricity forecasts, with uncertainty.</h1>
  <p class="lede">Explore hourly price forecasts with prediction intervals, and see how research models improved,
   what failed and how it was checked.</p>
  <p class="byline">Led by {esc(RC.OWNER_PUBLIC_NAME)} · <a href="#contribution">Contribution</a></p>
  <dl class="status-pair">
   <div class="status status-released"><dt>Demo</dt><dd class="status-name"><span class="gen gen-{released.style}">{RC.render_template("P23", "{g:released.name}")}</span></dd></div>
   <div class="status status-research"><dt>Research</dt><dd class="status-name"><span class="gen gen-{research.style}">{RC.render_template("P23", "{g:current.name}")}</span></dd>
    <dd class="headline" id="headline" data-block="headline">{RC.headline()}</dd>
    <dd class="headline-terms"><ul class="terms" aria-label="Terms used in the headline">{terms}</ul></dd></div>
  </dl>
 </div>
 <div class="opening-aside">
  <div class="actions">
   <a class="btn-primary external" href="{attr(C['space_url'])}"><span>Try the {ver(released.version)} demo</span></a>
   <a class="quiet" href="#research-results">Compare model results</a>
   <a class="quiet" href="#evidence">Code and evidence</a>
  </div>
  <p class="release-rule" data-block="release-rule">{RC.render_template("P22", "{g:release_rule}")}</p>
  {startup}
 <figure class="preview panel">
  <figcaption class="preview-label"><span class="badge badge-replay">Historical forecast · {ver(released.version)}</span>
   <span>Forecast and observed price for a held-out day. This is a historical replay, not a live forecast.</span></figcaption>
  {preview_chart(payload)}
  <p class="preview-key"><span class="key-median">Median forecast</span> <span class="key-band">{S("level", "80%")} prediction interval</span>
   <span class="key-actual">Observed price</span></p>
  <p class="preview-links"><a class="quiet" href="#product-forecast">Explore this forecast</a>
   <span class="preview-note">Opens the interactive replay in the product documentation.</span></p>
 </figure>
 </div>
</section>"""


#: The terms the headline introduces, defined directly below it (standard §1 ii).
HEADLINE_TERMS = ("terms.error_scores", "terms.targets", "terms.benchmark", "terms.policies", "terms.class")


def _branch_group(entry: G.Entry) -> G.Entry:
    """The generation a branch hangs from: follow `after` until a generation (standard §6)."""
    node = entry
    while node.kind != "generation":
        node = G.get(node.after)
    return node


def branch_card(entry: G.Entry) -> str:
    """A branch card (standard §6): the question, the comparator and the diagnostic that decided it,
    then "Not adopted" with a one-line reason and the evidence."""
    checkpoint = G.CHECKPOINTS[entry.checkpoint]
    status = entry.status
    audit = (Audit("Engineering report", checkpoint.report, checkpoint.evidence_tag),
             Audit("Review verdict", checkpoint.verdict, checkpoint.evidence_tag))
    return (
        f'<li class="branch" id="{entry.anchor[1:]}" data-registry="{entry.id}">'
        f'<p class="branch-head"><span class="branch-name">{esc(entry.name)}</span> '
        f'<span class="adoption">{RC.render_template("P23", "{g:%s.adoption}" % entry.id)}</span> '
        f'{S("date", G.month(status.date))}</p>'
        f'<p class="branch-reason" data-block="branch.{entry.id}.reason">{RC.render(f"branch.{entry.id}.reason")}</p>'
        + disclosure(f"{entry.anchor[1:]}-result", "Question, result and evidence",
                     f'<p class="branch-q" data-block="branch.{entry.id}.question">{RC.render(f"branch.{entry.id}.question")}</p>'
                     f'<p class="branch-result" data-block="branch.{entry.id}.result">'
                     f'{RC.render(f"branch.{entry.id}.result")}</p>' + evidence_row(compare=f"compare:{entry.id}", audit=audit))
        + "</li>"
    )


def lineage() -> str:
    """The main line of adopted generations, oldest first, with the branches attached where they
    belong in time. Nodes, names, statuses and order all come from the registry (standard §5, §6)."""
    nodes = "".join(
        f'<li class="node node-{entry.style}" data-registry="{entry.id}"><a href="{entry.anchor}">'
        f'<span class="dot" aria-hidden="true"></span>'
        f'<span class="node-name">{RC.render_template("P23", "{g:%s.name}" % entry.id)}</span>'
        f'<span class="node-status">{RC.render_template("P23", "{g:%s.adoption}" % entry.id)} · '
        f'{S("date", G.month(entry.status.date))}</span>'
        f'<span class="node-sub">{_structural_versions(entry.subtitle)}</span></a></li>'
        for entry in G.generations()
    )
    groups: dict[str, list[G.Entry]] = {}
    for entry in G.branches():
        groups.setdefault(_branch_group(entry).id, []).append(entry)
    branch_html = ""
    for generation in G.generations():
        entries = groups.get(generation.id, [])
        if not entries:
            continue
        # The next adopted generation comes from the validated predecessor chain, never from version arithmetic.
        later = next((item.successor for item in G.transitions() if item.predecessor.id == generation.id), None)
        span = (f"between {ver(generation.version)} and {ver(later.version)}" if later
                else f"after {ver(generation.version)}")
        plain = (f"between {generation.version} and {later.version}" if later else f"after {generation.version}")
        # A3: a group of rejected branches is never headed as if it were the adopted transition.
        branch_html += (
            f'<h3 class="branches-head" id="branches-{generation.id}">Experiments not adopted {span}</h3>'
            f'<ul class="branches" aria-label="Experiments not adopted {plain}">'
            + "".join(branch_card(entry) for entry in entries) + "</ul>"
        )
    return (
        f'<div class="lineage"><ol class="mainline" aria-label="Adopted generations, oldest first">{nodes}</ol>'
        f"{transitions_html()}{branch_html}</div>"
    )


#: The claim blocks each adopted transition's summary is built from (A3). A transition without them stops the
#: build: a new generation gets its summary written, never an empty card.
TRANSITION_FIELDS = (("change", "What changed"), ("comparator", "Comparator"), ("result", "Result"),
                     ("predecessor", "Against the predecessor"), ("limits", "Not established"))


def transition_card(item: G.Transition) -> str:
    """One adopted transition (PUBLISH_RULES 1.0 A3): predecessor and dates, change, comparator, result with its
    uncertainty and class, what it does not establish, the dated decision, and a route to the comparison."""
    key = f"transition.{item.id}"
    if f"{key}.title" not in RC.BLOCKS_BY_KEY:
        raise ChapterError(f"the adopted transition {item.id} has no summary blocks")
    pred, succ = item.predecessor, item.successor
    fields = [("Predecessor", RC.render_template(
        "P23", "{g:%s.name}. {g:%s.status}" % (pred.id, pred.id)))]
    for name, label in TRANSITION_FIELDS:
        if f"{key}.{name}" in RC.BLOCKS_BY_KEY:
            fields.append((label, f'<span data-block="{key}.{name}">{RC.render(f"{key}.{name}")}</span>'))
        elif name == "predecessor" and item.comparator_is_predecessor:
            continue  # the protocol's comparator is the predecessor: the result row is the predecessor comparison
        elif name in ("change", "comparator", "result", "limits"):
            raise ChapterError(f"{key}.{name} is missing")
    fields.append(("Decision", block(f"{succ.id}.decision", tag="span")))
    rows = "".join(f"<div><dt>{esc(label)}</dt><dd>{body}</dd></div>" for label, body in fields)
    anchor = succ.anchor[1:]
    return (
        f'<article class="transition" id="transition-{item.id}" data-transition="{item.id}" '
        f'aria-labelledby="transition-{item.id}-h">'
        f'<h4 id="transition-{item.id}-h" data-block="{key}.title">{RC.render(f"{key}.title")}</h4>'
        f'<p class="transition-meta">{badge(succ.badge)}</p>'
        f'<dl class="transition-fields">{rows}</dl>'
        f'<p class="transition-route"><a class="quiet in-text" href="#{anchor}-chart-title">The comparison chart and its '
        f'evidence, in the {ver(succ.version)} chapter</a></p></article>'
    )


def transitions_html() -> str:
    cards = "".join(transition_card(item) for item in G.transitions(newest_first=True))
    return (f'<div class="transitions"><h3 class="transitions-head" id="adopted-changes">Adopted changes, newest '
            f"first</h3>{cards}</div>")


def overview_panels() -> list[Panel]:
    rows = []
    for entry in G.comparison_rows():
        code = entry.code_in(G.COMPARISON_EXPERIMENT)
        verdict = f"derived.criteria.{entry.id}.verdict"
        rows.append((entry, code, verdict if verdict in D.records() else None))

    def panel(field: str, title: str, criterion: str) -> Panel:
        return Panel(
            title=title, subtitle="ratio to the naive · lower is better",
            rows=tuple(Row(comparison_label(entry), f"cp20.metrics.{code}.equal_fold.{field}", entry.style, code,
                           entry.kind == "generation", verdict=verdict) for entry, code, verdict in rows),
            domain=(0.5, 1.1), step=0.1,
            refs=(Ref("naive", at=1.0, dash=None, colour=TOKENS["text"]),
                  Ref("target", f"cp20.criteria.HG.{criterion}.equal_fold.{field}.upper_limit")),
            option="p=3",
        )

    return [panel("S_MAE", "Point-error score", "c1"), panel("S_WIS", "Interval score", "c2")]


def comparison_label(entry: G.Entry, experiment: str = G.COMPARISON_EXPERIMENT) -> str:
    """A comparison row's label: the canonical name, qualified by its role in that comparison."""
    note = next((code.note for code in entry.codes if code.experiment == experiment and code.note), "")
    qualifier = note or {"reference": "benchmark", "study arm": "study"}.get(entry.kind, "")
    return f"{entry.name} ({qualifier})" if qualifier else entry.name


def overview_chart() -> str:
    return single_rows(
        "overview", "P07", overview_panels(),
        title="Error scores of the seven policies, relative to the similar-day naive, against the targets",
        desc="Two dot plots with one row per policy in the same order; lower is better. The solid line marks the "
             "naive at one, a reference and not a target; the dashed line marks the target set before the "
             "experiments. The right-hand column says whether a policy met both targets.",
        label_width=262,
    )


def results() -> str:
    """The comparison (standard §1 i, §6): the change against the comparator with its interval and the
    main caveat above the chart; the target in words, with its date, N and a met / not-met column."""
    return f"""
<section class="section" id="research-results" aria-labelledby="results-h" data-research="results">
 <h2 id="results-h">How the models compare</h2>
 <figure class="panel analytical" aria-labelledby="comparison-finding">
  {block("comparison.finding", tag="h3", cls="panel-title finding-title", ident="comparison-finding")}
  {block("comparison.caveat", cls="qualification caveat-line")}
  <p class="panel-sub" data-block="comparison.sub">{RC.render("comparison.sub")}</p>
  {legend(tuple(dict.fromkeys(entry.style for entry in G.comparison_rows())))}
  {overview_chart()}
  <p data-block="comparison.target">{RC.target_sentence()} <span data-block="comparison.census">{RC.census_sentence()}</span></p>
  {block("comparison.howto")}
  {block("comparison.scale")}
  {block("overview.v1pointer", cls="qualification")}
  {evidence_row(compare="compare:overview",
                audit=checkpoint_audit("CP-20", source="reports/weather-ablation/metrics.csv", line=44))}
  {disclosure("overview-table", "View values", overview_table())}
 </figure>
 <div class="fairness">
  <h3>A fair comparison</h3>
  {block("overview.fairness")}
  {disclosure("fairness-detail", "Bootstrap settings and the five historical test periods",
              block("overview.fairness.detail") + fold_table())}
 </div>
 {disclosure("definitions", "Definitions, the policies tested, and why v1 scores differently in its own report",
             block("overview.definitions") + f'<p data-block="comparison.census.detail">{RC.census_detail()}</p>'
             + block("overview.f07"))}
</section>"""


# --------------------------------------------------------------------------- the released product, documented (A4)
#
# PUBLISH_RULES 1.0 §5 and amendment A4: directly after the opening, the maintained documentation of the model the
# registry names as released -- a short orientation, descriptive routes to every subject of §5.1, and the full
# topics in one named disclosure that each route opens. The documentation belongs to the product, not to a
# generation: its heading carries no version, and its content is chosen by the released entry's id. A released
# model without documentation here stops the build, so a replacement can never inherit another model's evidence.

#: "fold 5" in running text, its index declared structural.
FOLD5 = "fold " + RC.structural("fold", "5")

#: The subjects of PUBLISH_RULES 1.0 §5.1 (the original report's 1–12, with its spectral 3b).
PRODUCT_SUBJECTS = ("1", "2", "3", "3b", "4", "5", "6", "7", "8", "9", "10", "11", "12")


class ProductDocsError(RuntimeError):
    """The released model's documentation is missing or incomplete; the page refuses to build."""


@dataclass(frozen=True)
class Topic:
    """One route of the product documentation: its anchor, the route's descriptive label, its heading, the
    §5.1 subjects it covers with their disposition, and its body."""

    anchor: str
    label: str
    heading: str
    subjects: tuple[str, ...]
    body: str
    #: "supported", or "not evaluated" / "inapplicable" with the reason in the body (§5.1).
    disposition: str = "supported"


def _feature_groups() -> tuple[tuple[str, tuple[str, ...]], ...]:
    """The released model's inputs from its committed card, grouped for reading. The grouping is presentation;
    every name comes from the card, and a name the grouping does not place stops the build."""
    features = json.loads(CHAMPION_CARD.read_text())["feature_list"]
    groups = (
        ("Calendar, holidays and season", lambda f: f in ("local_hour", "day_of_week", "month", "day_type",
                                                          "dst_transition_day", "summer_peak", "winter_peak")
         or f.startswith("is_")),
        ("Day-ahead load forecast", lambda f: f.startswith("load_forecast")),
        ("Price of the same hour on earlier days", lambda f: f.startswith("price_lag_")),
        ("Rolling price statistics, frozen at the day before", lambda f: f.startswith("price_roll_")),
        ("Negative prices and regime flags", lambda f: f in ("negative_price_count_168h", "crisis_period", "post_crisis")),
    )
    out, placed = [], set()
    for title, member in groups:
        names = tuple(f for f in features if member(f))
        placed |= set(names)
        out.append((title, names))
    if placed != set(features):
        raise ProductDocsError(f"inputs without a group: {sorted(set(features) - placed)}")
    return tuple(out)


def feature_table() -> str:
    rows = "".join(
        f'<tr><th scope="row">{esc(title)}</th><td>'
        + ", ".join(f'<code>{S("identifier", name)}</code>' for name in names) + "</td></tr>"
        for title, names in _feature_groups())
    return ('<div class="scroll" role="region" aria-label="The released model\'s inputs" tabindex="0"><table class="data">'
            f'<caption>The inputs, by group, as the model card names them</caption><thead><tr><th scope="col">Group</th>'
            f'<th scope="col">Inputs</th></tr></thead><tbody>{rows}</tbody></table></div>')


def _bars(chart_id: str, claim_id: str, rows: tuple[tuple[str, str], ...], *, title: str, desc: str,
          axis: str, domain: tuple[float, float], step: float, role: str) -> str:
    """Horizontal bars from a zero reference, one per (label record, value record), with each value printed.
    A dedicated phone drawing puts the label above its bar (invariant 23)."""
    axis_unit([value for _, value in rows])
    parts = []
    label_w, value_w, row_h = 250, 64, 30
    x0, x1 = label_w, DESKTOP_W - value_w
    scale = Scale(f"{chart_id}-x", domain[0], domain[1], x0, x1, R.get(rows[0][1]).unit)
    top = 8
    for index, (label_record, value_record) in enumerate(rows):
        y = top + index * row_h
        value = R.get(value_record).value
        parts.append(svg_text(0, y + 19, RC.svg_value(label_record), extra=RC.svg_binding(claim_id, label_record)))
        parts.append(f'<rect x="{x0:.1f}" y="{y + 7:.1f}" width="{scale(value) - x0:.1f}" height="16" '
                     f'fill="{ROLE_STYLE[role]["color"]}"{RC.svg_binding(claim_id, value_record)}/>')
        parts.append(value_label(scale(value) + 6, y + 19, claim_id, value_record, option="p=1"))
    bottom = top + len(rows) * row_h
    parts.append(ref_line(scale, 0.0, top, bottom + 4, dash=None, colour=TOKENS["text"], width=1.4))
    parts.append(scale_ticks(scale, step, top, bottom, labels_at=bottom + 20, grid=False))
    parts.append(svg_text(x0, bottom + 40, axis, fill=TOKENS["text-2"]))
    desktop = svg_wrap(DESKTOP_W, bottom + 48, "".join(parts), title=title, desc=desc, variant="d", chart_id=chart_id)
    parts, y = [], 4.0
    m0, m1 = 12.0, MOBILE_W - 52
    mscale = Scale(f"{chart_id}-x", domain[0], domain[1], m0, m1, scale.unit)
    for label_record, value_record in rows:
        value = R.get(value_record).value
        parts.append(svg_text(0, y + 13, RC.svg_value(label_record), extra=RC.svg_binding(claim_id, label_record)))
        parts.append(f'<rect x="{m0:.1f}" y="{y + 20:.1f}" width="{mscale(value) - m0:.1f}" height="12" '
                     f'fill="{ROLE_STYLE[role]["color"]}"{RC.svg_binding(claim_id, value_record)}/>')
        parts.append(value_label(mscale(value) + 6, y + 31, claim_id, value_record, option="p=1"))
        y += 42
    parts.append(scale_ticks(mscale, step * 2, 4, y, labels_at=y + 16, grid=False))
    for index, line in enumerate(_wrap(axis, MOBILE_LINE_CHARS)):
        parts.append(svg_text(0, y + 36 + 17 * index, line, fill=TOKENS["text-2"]))
    height = y + 44 + 17 * len(_wrap(axis, MOBILE_LINE_CHARS))
    mobile = svg_wrap(MOBILE_W, height, "".join(parts), title=title, desc=desc, variant="m", chart_id=chart_id)
    return f'<div class="chart" data-chart-id="{chart_id}">{desktop}{mobile}</div>'


def product_attribution_chart() -> str:
    rows = tuple((f"cp2.diagnostics.frozen_shap.{rank}.feature", f"cp2.diagnostics.frozen_shap.{rank}.mean_abs_shap")
                 for rank in range(1, 11))
    return _bars("product-shap", "P43", rows,
                 title="The ten inputs with the largest mean absolute SHAP value for the released model's median forecast",
                 desc="Horizontal bars from zero, one per input, in EUR/MWh; the same-hour price one day earlier is by "
                      "far the largest. The released artifact explained on fold five's test block, rows it was "
                      "fitted on: an in-sample diagnostic.",
                 axis="mean absolute SHAP value, EUR/MWh · median head · in sample",
                 domain=(0.0, 16.0), step=2.0, role="v1")


#: The calibration stages' marks (a shape each, so no meaning rests on colour).
STAGE_STYLE = {
    "raw": {"color": TOKENS["text-2"], "marker": "circle", "filled": False},
    "post_cqr": {"color": TOKENS["text-2"], "marker": "diamond", "filled": False},
    "final": {"color": TOKENS["v1"], "marker": "triangle", "filled": True},
}
STAGE_NAMES = {"raw": "raw heads", "post_cqr": "after CQR", "final": "final"}
#: The short names on a row's values line, which must fit one panel.
STAGE_SHORT = {"raw": "raw", "post_cqr": "CQR", "final": "final"}


def product_reliability_chart() -> str:
    """Coverage at each nominal level, by calibration stage, for the frozen artifact on its one-shot holdout and
    for the development folds; the nominal level is the reference each row is read against."""
    panels = (("One-shot holdout, the frozen artifact", "cp2.holdout.coverage.{stage}.{level}"),
              ("Development folds, one model per fold", "cp2.reliability.{stage}.{level}"))
    levels = ("50", "80", "95")
    lo, hi = 0.2, 1.0

    def panel(x0: float, x1: float, top: float, name: str, pattern: str) -> tuple[str, float]:
        scale = Scale("product-coverage-x", lo, hi, x0 + 16, x1 - 14, R.UNIT_FRACTION)
        out = [svg_text(x0, top + 16, name, weight="600")]
        y = top + 28
        for level in levels:
            ids = [pattern.format(stage=stage, level=level) for stage in STAGE_STYLE]
            axis_unit(ids)
            out.append(svg_text(x0, y + 16, f"{level}% interval"))
            # one short line per stage, so marks with nearly equal values never hide one another
            first = y + 30
            for index, (stage, record_id) in enumerate(zip(STAGE_STYLE, ids)):
                line_y = first + 14 * index
                out.append(f'<line x1="{x0 + 16:.1f}" x2="{x1 - 14:.1f}" y1="{line_y:.1f}" y2="{line_y:.1f}" '
                           f'stroke="{TOKENS["grid"]}"/>')
                out.append(marker(scale(R.get(record_id).value), line_y, stage, size=5.2, style=STAGE_STYLE[stage],
                                  extra=RC.svg_binding("P46", record_id)))
            out.append(ref_line(scale, int(level) / 100, first - 8, first + 36, dash=None, colour=TOKENS["text"], width=2))
            cursor, values_y = x0, first + 52
            for stage, record_id in zip(STAGE_STYLE, ids):
                out.append(svg_text(cursor, values_y, STAGE_SHORT[stage], fill=TOKENS["text-2"]))
                cursor += 8.6 * len(STAGE_SHORT[stage]) + 6
                text = RC.svg_value(record_id)
                out.append(svg_text(cursor, values_y, text, weight="600", extra=RC.svg_binding("P46", record_id)))
                cursor += 8.0 * len(text) + 12
            y = values_y + 16
        out.append(scale_ticks(scale, 0.2, top + 36, y, labels_at=y + 10, grid=False))
        return "".join(out), y + 22

    desktop_parts, bottoms = [], []
    for index, (name, pattern) in enumerate(panels):
        body, bottom = panel(index * 390, index * 390 + 370, 0, name, pattern)
        desktop_parts.append(body)
        bottoms.append(bottom)
    note = "x: share of hours inside the interval · the black line is the nominal level, a reference, not a target"
    desktop_parts.append(svg_text(0, max(bottoms) + 14, note, fill=TOKENS["text-2"]))
    title = "How often the released model's intervals contained the price, by calibration stage"
    desc = ("Two panels, the frozen artifact on its one-shot holdout and the development folds. For each nominal "
            "level, three short lines: the coverage of the raw heads (open circle), after CQR (open diamond) and "
            "final (filled triangle), with the nominal level as a black vertical line across them.")
    desktop = svg_wrap(DESKTOP_W, max(bottoms) + 24, "".join(desktop_parts), title=title, desc=desc, variant="d",
                       chart_id="product-coverage")
    mobile_parts, cursor = [], 0.0
    for name, pattern in panels:
        body, cursor = panel(0, MOBILE_W, cursor, name, pattern)
        mobile_parts.append(body)
        cursor += 12
    for index, line in enumerate(_wrap(note, MOBILE_LINE_CHARS)):
        mobile_parts.append(svg_text(0, cursor + 14 + 17 * index, line, fill=TOKENS["text-2"]))
    mobile = svg_wrap(MOBILE_W, cursor + 20 + 17 * len(_wrap(note, MOBILE_LINE_CHARS)), "".join(mobile_parts),
                      title=title, desc=desc, variant="m", chart_id="product-coverage")
    return f'<div class="chart" data-chart-id="product-coverage">{desktop}{mobile}</div>'


def stage_legend() -> str:
    items = "".join(
        f'<li><svg class="legend-mark" viewBox="-8 -8 16 16" width="16" height="16" aria-hidden="true">'
        f'{marker(0, 0, stage, size=5, style=style)}</svg><span>{esc(STAGE_NAMES[stage])}</span></li>'
        for stage, style in STAGE_STYLE.items())
    tick = ('<li><svg class="legend-mark" viewBox="-8 -8 16 16" width="16" height="16" aria-hidden="true">'
            f'<line x1="0" x2="0" y1="-7" y2="7" stroke="{TOKENS["text"]}" stroke-width="2"/></svg>'
            "<span>nominal level</span></li>")
    return '<ul class="legend" aria-label="Marker key">' + items + tick + "</ul>"


def regime_table() -> str:
    """CP-2's regime-stratified error for the released recipe's development folds, exact (standard §4)."""
    names = {"all": "All development hours", "pre_crisis": "Before the crisis", "crisis": "The crisis",
             "post_crisis": "After the crisis", "negative_price": "Negative-price hours",
             "dunkelflaute": "Low wind and solar days", "non_flag": "Other days", "weekday": "Weekdays",
             "weekend": "Weekends", "august_2022_peak": "August 2022 peak weeks"}
    body = []
    for key, _, _ in R.CP2_STRATA:
        base = f"cp2.regime.{key}"
        mae = value(f"{base}.mae", "P45", option="exact")
        if f"{base}.mae_ci95_low" in R.records():
            mae += (f' <span class="ci">[{value(f"{base}.mae_ci95_low", "P45", option="exact")}, '
                    f'{value(f"{base}.mae_ci95_high", "P45", option="exact")}]</span>')
        cells = [f'<th scope="row">{_structural_versions(names[key])}</th>',
                 f'<td class="n">{value(f"{base}.n_obs", "P45")}</td>', f'<td class="n">{value(f"{base}.n_days", "P45")}</td>',
                 f'<td class="n exact">{mae}</td>']
        cells += [f'<td class="n exact">{value(f"{base}.coverage_{level}", "P45", option="exact")}</td>' for level in ("50", "80", "95")]
        cells.append(f'<td>{value(f"{base}.read", "P45")}</td>')
        body.append("<tr>" + "".join(cells) + "</tr>")
    caption = _label("The released recipe on its five development folds, by stratum: MAE in EUR/MWh with a day-block "
                     "bootstrap 95% confidence interval for thin subsets, and interval coverage as a fraction of hours")
    heads = "".join(f'<th scope="col">{_label(text)}</th>' for text in (
        "Stratum", "Hours", "Days", "MAE, EUR/MWh", "50% coverage", "80% coverage", "95% coverage", "Reading"))
    return ('<div class="scroll" role="region" aria-label="Errors by regime, the development folds" tabindex="0">'
            f'<table class="data"><caption>{caption}</caption><thead><tr>{heads}</tr></thead>'
            f"<tbody>{''.join(body)}</tbody></table></div>")


def attribution_table() -> str:
    """The released artifact's in-sample ranking beside fold 5's out-of-sample one: two identities, side by side."""
    body = "".join(
        f'<tr><th scope="row">{S("rank", str(rank))}</th>'
        f'<td>{value(f"cp2.diagnostics.frozen_shap.{rank}.feature", "P43")}</td>'
        f'<td class="n exact">{value(f"cp2.diagnostics.frozen_shap.{rank}.mean_abs_shap", "P43", option="exact")}</td>'
        f'<td>{value(f"cp2.diagnostics.fold5_shap.{rank}.feature", "P43")}</td>'
        f'<td class="n exact">{value(f"cp2.diagnostics.fold5_shap.{rank}.mean_abs_shap", "P43", option="exact")}</td></tr>'
        for rank in range(1, 11))
    return ('<div class="scroll" role="region" aria-label="SHAP rankings, released artifact and development model" '
            'tabindex="0"><table class="data"><caption>Mean absolute SHAP value of the median head, EUR/MWh, on '
            f'{FOLD5}\'s test block</caption><thead><tr><th scope="col">Rank</th>'
            '<th scope="col">Released artifact, in sample</th><th scope="col">Value</th>'
            f'<th scope="col">{_label("Fold 5 development model, out of sample")}</th>'
            f'<th scope="col">Value</th></tr></thead><tbody>{body}</tbody></table></div>')


def permutation_table() -> str:
    body = "".join(
        f'<tr><th scope="row">{S("rank", str(rank))}</th>'
        f'<td>{value(f"cp2.diagnostics.permutation.{rank}.feature", "P44")}</td>'
        f'<td class="n exact">{value(f"cp2.diagnostics.permutation.{rank}.importance_mean_mae_increase", "P44", option="exact")}</td>'
        f'<td class="n exact">{value(f"cp2.diagnostics.permutation.{rank}.importance_std", "P44", option="exact")}</td></tr>'
        for rank in range(1, 11))
    return ('<div class="scroll" role="region" aria-label="Permutation importance, the development model" tabindex="0">'
            '<table class="data"><caption>Permutation importance: rise in the median forecast\'s MAE when one input is '
            f'shuffled, EUR/MWh, {FOLD5}\'s development model on its own test block</caption><thead><tr>'
            '<th scope="col">Rank</th><th scope="col">Input</th><th scope="col">MAE increase</th>'
            f'<th scope="col">Standard deviation</th></tr></thead><tbody>{body}</tbody></table></div>')


def product_replay(payload: dict) -> str:
    """Subject 10: the released model's forecast for a held-out day, with its two real controls. It reads the
    same precomputed replay as the preview and the archive (window.__FAN__); nothing is fetched or recomputed."""
    levels = "".join(
        f'<label><input type="radio" name="p-lvl" value="{level}"{" checked" if level == 80 else ""}> '
        f'{S("level", f"{level}%")}</label>' for level in sorted(INTERVAL_LEVELS))
    title = "The released model's forecast for one held-out delivery day"
    desc = ("Median forecast as a line, the chosen prediction interval as a band, and the price that cleared as a "
            "dashed line, for each local hour. A historical replay, not a live forecast.")
    return f"""<figure class="panel analytical product-replay" aria-labelledby="p-replay-title">
 <h4 class="panel-title" id="p-replay-title">Forecast for {S("date", payload["delivery_day"])}, a day of the one-shot holdout</h4>
 <p class="panel-sub">Historical replay · EUR/MWh by local hour (Europe/Berlin) · the frozen released model</p>
 <div class="replay-controls">
  <fieldset><legend>Prediction-interval level</legend>{levels}</fieldset>
  <div class="replay-range"><label for="p-scale">Load-forecast scenario: × <output id="p-scaleval" for="p-scale">{S("control", "1.00")}</output></label>
   <input id="p-scale" type="range" min="0" max="{len(LOAD_SCALES) - 1}" step="1" value="{LOAD_SCALES.index(1.00)}"></div>
 </div>
 <svg id="p-chart" class="replay-chart" viewBox="0 0 760 320" role="img" aria-labelledby="p-chart-t p-chart-d"><title id="p-chart-t">{esc(title)}</title><desc id="p-chart-d">{esc(desc)}</desc><g class="plot"></g></svg>
 <p class="preview-key"><span class="key-median">Median forecast</span> <span class="key-band">Prediction interval</span>
  <span class="key-actual" id="p-legend-actual">Observed price</span></p>
 <p>At the selected level, the frozen model's empirical coverage over the holdout was
  <strong><span id="p-cov" data-claim="P47" data-v1="holdout_coverage_80">{esc(build_claims()["holdout_coverage_80"])}</span></strong>.</p>
 <p class="qualification" id="p-scenario" hidden>A scenario is active: the observed price is hidden, because it belongs to the unperturbed day.</p>
</figure>"""


def v1_product_topics(C, payload) -> tuple[Topic, ...]:
    """The released v1's documentation: the twelve subjects, each from evidence about this model, labelled with
    the model, output and rows it describes (PUBLISH_RULES 1.0 §5.1)."""
    released = G.released()
    # A link standing alone in its paragraph is a target of its own: a full-height `.quiet` link (about 44 px).
    archive = lambda anchor, html_text: f'<a class="quiet archive-route" href="#{anchor}">{html_text}</a>'  # noqa: E731
    limitations = "".join(
        f'<li><strong>{S("name", C_LABELS[key])}.</strong> <span data-claim="P48" data-v1="{key}">{esc(C[key])}</span></li>'
        for key in C_LIMITATION_KEYS)
    run_links = (
        f'<p><a class="quiet external in-text" href="{attr(C["mlflow_experiment_url"])}">'
        f'{ver(released.version)}\'s runs in MLflow</a>: training, the holdout and the diagnostics, readable without '
        f'signing in. <a class="quiet in-text" href="#reproduce">Rebuild this report</a> from saved evidence. '
        f'<a class="quiet external in-text" href="{attr(github("docs/deploy.md"))}">Deployment notes</a>.</p>')
    return (
        Topic("product-data", "Data and the information cutoff", "Data and the information cutoff", ("1",),
              "".join(block(k) for k in ("product.data.target", "product.data.sources", "product.data.cutoff",
                                        "product.data.windows", "product.data.preprocessing"))),
        Topic("product-regimes", "Price regimes and negative prices", "Price regimes and negative prices", ("2",),
              block("product.regimes.periods") + block("product.regimes.why")
              + f'<p>{archive("regimes", "Yearly price levels and negative-hour counts, in the archived report")}</p>'),
        Topic("product-inputs", "The inputs it uses, and why", "The inputs it uses, and why", ("3", "3b"),
              block("product.inputs.catalog") + feature_table() + block("product.inputs.excluded")
              + block("product.inputs.seasonal")
              + f'<p>{archive("spectral", "The spectral figures behind the calendar inputs, in the archived report")}</p>'),
        Topic("product-validation", "How it was tested before release", "How it was tested before release", ("4",),
              "".join(block(k) for k in ("product.validation.design", "product.validation.holdout",
                                        "product.validation.classes", "product.validation.leakage"))),
        Topic("product-results", "Measured results: the one-shot test", "Measured results", ("5",),
              f'<p class="holdout-head">The one-shot holdout {badge(RC.BADGE_V1_HOLDOUT, "holdout")}</p>'
              + block("v1.holdout") + block("product.results.coverage") + block("v1.unflattering")
              + block("product.results.shared")
              + '<p><a class="quiet" href="#definitions">Why these scores differ from its own report</a></p>'),
        Topic("product-attribution", "What drives its forecasts: SHAP chart", "What drives its forecasts", ("6",),
              '<figure class="panel analytical" aria-labelledby="product-attribution-title">'
              + block("product.attribution.headline", tag="h4", cls="panel-title", ident="product-attribution-title")
              + '<p class="panel-sub">Mean absolute SHAP value, EUR/MWh · median head · the released artifact on '
              + FOLD5 + "'s test block · in-sample diagnostic</p>"
              + product_attribution_chart() + block("product.attribution.reading", cls="finding")
              + block("product.attribution.identity", cls="qualification")
              + disclosure("product-attribution-values", "View values, beside the development model's ranking",
                           attribution_table())
              + "</figure>" + block("product.attribution.scope")
              + "<p>" + archive("shap", "The out-of-sample SHAP figures of " + FOLD5
                                + "’s development model, in the archived report") + "</p>"),
        Topic("product-importance", "Input importance and its limits",
              "Which inputs matter, and what that does not show", ("7",),
              block("product.importance.permutation") + permutation_table() + block("product.importance.limits")
              + block("product.importance.sensitivity")),
        Topic("product-failures", "Where it fails: errors by regime", "Where it fails: errors by regime", ("8",),
              block("product.failures.reading") + regime_table() + block("product.failures.identity")),
        Topic("product-reliability", "Interval reliability: coverage chart", "How reliable its intervals are",
              ("9",),
              '<figure class="panel analytical" aria-labelledby="product-reliability-title">'
              + block("product.reliability.headline", tag="h4", cls="panel-title", ident="product-reliability-title")
              + '<p class="panel-sub">Share of hours inside the interval · nominal level as reference · the frozen '
              "artifact on its one-shot holdout, and the development folds</p>"
              + stage_legend() + product_reliability_chart() + block("product.reliability.stages", cls="finding")
              + block("product.reliability.width", cls="qualification") + "</figure>"
              + block("product.reliability.crossings") + block("product.reliability.guarantee")),
        Topic("product-forecast", "Read a forecast: interactive replay", "Read a forecast", ("10",),
              product_replay(payload) + "".join(block(k) for k in ("product.forecast.read", "product.forecast.controls",
                                                                   "product.forecast.demo"))
              + f'<p><a class="quiet external" href="{attr(C["space_url"])}">Try the {ver(released.version)} demo</a></p>'),
        Topic("product-limitations", "Limitations", "Limitations", ("11",),
              block("product.limits.summary") + f'<ul class="limitations">{limitations}</ul>'
              + f'<p><span data-claim="P48" data-v1="floor_change">{esc(C["floor_change"])}</span></p>'),
        Topic("product-run", "Run this product", "Run this product", ("12",),
              "".join(block(k, cls="run") for k in ("product.run.local", "product.run.identity", "product.run.demo"))
              + run_links + block("product.run.historical")),
    )


#: The documentation of each model the registry may name as released. Only v1 has been released.
PRODUCT_DOCS = {"v1": v1_product_topics}


def product_topics(C, payload) -> tuple[Topic, ...]:
    released = G.released()
    builder = PRODUCT_DOCS.get(released.id)
    if builder is None:
        raise ProductDocsError(f"the registry names {released.id} as released, and this page has no documentation "
                               "for it; write its topics before publishing (PUBLISH_RULES 1.0 §5.1)")
    topics = builder(C, payload)
    covered = [subject for topic in topics for subject in topic.subjects]
    missing = [subject for subject in PRODUCT_SUBJECTS if subject not in covered]
    extra = [subject for subject in covered if subject not in PRODUCT_SUBJECTS]
    if missing or extra or len(covered) != len(set(covered)):
        raise ProductDocsError(f"subjects missing {missing}, unknown {extra}, or covered twice: {covered}")
    for topic in topics:
        if topic.disposition not in ("supported", "not evaluated", "inapplicable"):
            raise ProductDocsError(f"{topic.anchor}: disposition {topic.disposition!r}")
    return topics


def product_section(C, payload) -> str:
    """How the product works (A4): the released model's orientation, a route to every topic, and the topics."""
    released = G.released()
    topics = product_topics(C, payload)
    routes = "".join(f'<li><a href="#{topic.anchor}">{esc(topic.label)}</a></li>' for topic in topics)
    bodies = "".join(
        f'<section class="topic" data-topic="{topic.anchor}" data-subjects="{" ".join(topic.subjects)}" '
        f'aria-labelledby="{topic.anchor}"><h3 id="{topic.anchor}">{esc(topic.heading)}</h3>{topic.body}</section>'
        for topic in topics)
    return f"""
<section class="section product" id="product" aria-labelledby="product-h" data-research="product" data-product="{released.id}">
 <h2 id="product-h">How the product works</h2>
 {block("product.lede", cls="product-lede")}
 <nav class="product-routes" aria-label="Topics of how the product works"><ol>{routes}</ol></nav>
 <details class="disclosure product-manual" id="product-manual"><summary><span class="marker" aria-hidden="true"></span><span>All topics in full</span></summary>
  <div class="disclosure-body">{bodies}</div>
 </details>
</section>"""


# --------------------------------------------------------------------------- the chapter grammar (standard §6)

#: The fixed menu a chapter's details come from, in this order.
DETAIL_MENU = ("method", "per-period consistency", "stress period", "coverage and width", "protocol and review")
DETAIL_TITLES = {
    "method": "Method",
    "per-period consistency": "Per-period consistency, including absolute errors",
    "stress period": "The stress period: the 2022 crisis",
    "coverage and width": "Coverage and interval width",
    "protocol and review": "Protocol and review",
}


class ChapterError(ValueError):
    """A chapter that does not fill the grammar's fixed slots. The renderer refuses to draw it."""


@dataclass(frozen=True)
class MainChart:
    """Slot 2: paired differences against the comparator on both primary scores, with 95% intervals."""

    chart_id: str
    claim_id: str
    panels: tuple[Panel, ...]
    title: str
    desc: str
    subtitle: str
    label_width: int = 230
    row_h: int = 56


@dataclass(frozen=True)
class ChapterSlots:
    """The chapter grammar's slots, in order (standard §6)."""

    entry: G.Entry
    question: str                      # 1. the question ...
    change: str                        # 1. ... and the change, drawn with it as one diagram
    chart: MainChart                   # 2. the main chart
    headline: str                      # 2. its claim-bound headline
    reading: str                       # 3. the reading, in one sentence
    not_established: tuple[str, ...]   # 4. at most three things the result does not establish
    decision: str                      # 5. the decision, dated
    evidence: str                      # 6. the evidence row
    details: tuple[tuple[str, str], ...]  # 7. details from the fixed menu


def _comparator_code(entry: G.Entry, experiment: str) -> str | None:
    return G.get(entry.comparator).code_in(experiment) if entry.comparator else None


def slot_problems(slots: ChapterSlots) -> list[str]:
    """Why a chapter does not fill the grammar; empty when it does."""
    problems = []
    for name in ("question", "change", "headline", "reading", "decision", "evidence"):
        if not getattr(slots, name):
            problems.append(f"{slots.entry.id}: the {name} slot is empty")
    for key in (slots.question, slots.headline, slots.reading, slots.decision):
        if key and key not in RC.BLOCKS_BY_KEY:
            problems.append(f"{slots.entry.id}: {key} is not a claim block")
    if not 1 <= len(slots.not_established) <= 3:
        problems.append(f"{slots.entry.id}: {len(slots.not_established)} things not established (one to three)")
    keys = [key for key, _ in slots.details]
    if any(key not in DETAIL_MENU for key in keys):
        problems.append(f"{slots.entry.id}: a detail outside the fixed menu: {[k for k in keys if k not in DETAIL_MENU]}")
    elif keys != sorted(keys, key=DETAIL_MENU.index) or len(keys) != len(set(keys)):
        problems.append(f"{slots.entry.id}: details out of the menu's order, or repeated")
    rows = [row for panel in slots.chart.panels for row in panel.rows]
    if not rows:
        problems.append(f"{slots.entry.id}: the main chart has no rows")
    covered = set()
    for row in rows:
        record = R.get(row.record_id)
        if record.interval is None or record.aggregation != "equal_fold_contrast":
            problems.append(f"{slots.entry.id}: {row.record_id} is not a paired difference with an interval")
            continue
        selector = record.selector_dict()
        experiment = record.checkpoint
        if (selector["candidate"] == slots.entry.code_in(experiment)
                and selector["baseline"] == _comparator_code(slots.entry, experiment)):
            covered.add(selector["metric"])
    if covered != {"MAE", "WIS"}:
        problems.append(f"{slots.entry.id}: the main chart lacks the paired difference against its comparator on "
                        f"both primary scores (has {sorted(covered)})")
    return problems


_DETAIL_HEAD = re.compile(r'<h4 class="detail-head" id="([^"]+)">(.*?)</h4>', re.DOTALL)


def detail_head(ident: str, text: str) -> str:
    """A heading inside a chapter's detail: the landing target of its chart's route (PUBLISH_RULES 1.0 A5)."""
    return f'<h4 class="detail-head" id="{ident}">{_structural_versions(text)}</h4>'


def explore_routes(slots: ChapterSlots) -> str:
    """"Explore these results" (A5): one descriptive route per detail heading, generated from the details
    themselves so a chart cannot be added without its route. Each opens its disclosure (NAV_JS)."""
    routes = [(ident, text) for _, body in slots.details for ident, text in _DETAIL_HEAD.findall(body)]
    if not routes:
        return ""
    items = "".join(f'<li><a class="quiet" href="#{ident}">{text}</a></li>' for ident, text in routes)
    anchor = slots.entry.anchor[1:]
    return (f'<nav class="explore" aria-labelledby="{anchor}-explore-h"><h3 class="story-label" '
            f'id="{anchor}-explore-h">Explore these results</h3><ul>{items}</ul></nav>')


def render_chapter(slots: ChapterSlots, *, open_details: tuple[str, ...] = ()) -> str:
    """The one generic chapter renderer. Every slot is filled, in order, or the build fails."""
    problems = slot_problems(slots)
    if problems:
        raise ChapterError("; ".join(problems))
    entry, chart = slots.entry, slots.chart
    anchor = entry.anchor[1:]
    not_established = "".join(f'<li data-block="{key}">{RC.render(key)}</li>' for key in slots.not_established)
    details = "".join(
        disclosure(f"{anchor}-{key.replace(' ', '-')}", DETAIL_TITLES[key], body, open_=key in open_details)
        for key, body in slots.details)
    return f"""
<article class="chapter" id="{anchor}" aria-labelledby="{anchor}-h" data-research="{anchor}" data-grammar="chapter">
 {chapter_header(entry)}
 <figure class="change-figure" data-slot="question">
  <figcaption><h3 class="story-label">The question</h3>{block(slots.question, cls="question")}</figcaption>
  {slots.change}
 </figure>
 <figure class="panel analytical" aria-labelledby="{anchor}-chart-title" data-slot="main-chart">
  {block(slots.headline, tag="h3", cls="panel-title", ident=f"{anchor}-chart-title")}
  <p class="panel-sub">{_structural_versions(chart.subtitle)}</p>
  {single_rows(chart.chart_id, chart.claim_id, list(chart.panels), title=chart.title, desc=chart.desc,
               label_width=chart.label_width, row_h=chart.row_h)}
  {block(slots.reading, cls="finding reading")}
  {values_table(f"{chart.chart_id}-values", chart.claim_id, list(chart.panels))}
 </figure>
 <aside class="caveats" aria-label="What this result does not establish" data-slot="not-established">
  <h3>What this result does not establish</h3><ul class="not-established">{not_established}</ul>
 </aside>
 <div class="decision" data-slot="decision"><h3 class="story-label">Decision</h3>{block(slots.decision)}</div>
 <div data-slot="evidence">{slots.evidence}</div>
 {explore_routes(slots)}
 <div class="disclosures" data-slot="details">{details}</div>
</article>"""


def chapter_header(entry: G.Entry, *, with_badge: bool = True) -> str:
    """A chapter's header: version, canonical name, subtitle, dated status and badge (standard §5)."""
    badge_html = badge(entry.badge, "development") if with_badge else ""
    name = entry.name.split(" · ", 1)[1]
    status = RC.render_template("P23", "{g:%s.adoption}" % entry.id)
    return (
        f'<header class="chapter-head"><p class="eyebrow"><span class="adoption">{status}</span>'
        f'{S("date", G.month(entry.status.date))}</p>'
        f'<h2 id="{entry.id}-h"><span class="gen gen-{entry.style}">{ver(entry.version)}</span> · {esc(name)}</h2>'
        f'<p class="chapter-sub">{_structural_versions(entry.subtitle)}</p>'
        f'<p class="chapter-meta">{badge_html}</p></header>'
    )


def feature_change() -> str:
    current, comparator = G.current_generation(), G.get(G.current_generation().comparator)
    return (
        f'<div class="feature-change" aria-label="What changed from {comparator.version} to {current.version}">'
        f'<div class="fc-col"><p class="fc-head">{ver(comparator.version)} inputs</p><ul><li>price history</li>'
        "<li>load forecast</li><li>calendar</li></ul></div>"
        '<div class="fc-arrow" aria-hidden="true">+</div>'
        f'<div class="fc-col fc-added"><p class="fc-head">added in {ver(current.version)}</p><ul>'
        f'<li>wind speed at {S("height", "10 m")}</li><li>wind speed at {S("height", "100 m")}</li>'
        '<li>solar radiation</li></ul><p class="fc-note">each with a missing-data indicator</p></div></div>'
    )


def blend_change() -> str:
    v1, v2 = G.get("v1"), G.get("v2")
    return (
        f'<div class="feature-change" aria-label="What changed from {v1.version} to {v2.version}">'
        f'<div class="fc-col"><p class="fc-head">{ver(v1.version)}</p><ul><li>one LightGBM quantile model</li>'
        "<li>conformal intervals from a fixed calibration window</li></ul></div>"
        '<div class="fc-arrow" aria-hidden="true">→</div>'
        f'<div class="fc-col fc-added fc-v2"><p class="fc-head">{ver(v2.version)}</p><ul>'
        f"<li>daily LEAR and normalized LEAR, blended equally</li><li>intervals from recent errors, "
        "by hour of the day</li></ul><p class=\"fc-note\">control: the same blend with pooled intervals</p></div></div>"
    )


def v3_slots(*, open_folds: bool = False) -> ChapterSlots:
    entry = G.get("v3")
    cp20 = "evidence/cp-20"
    protocol = "".join(block(key) for key in ("v3.criteria", "v3.controls", "v3.controls.supplement", "v3.review",
                                              "v3.cost", "v3.dependency"))
    protocol += f'<p class="attribution-line"><span data-structural="attribution">{esc(GFS_ATTRIBUTION)}</span></p>'
    folds = (detail_head("v3-per-period-differences", "Did weather help in every test period?")
             + c2b_chart() + values_table("v3-c2b-values", "C72", c2b_panels())
             + detail_head("v3-absolute-errors", "Absolute errors per test period, for v1, v2 and v3")
             + c3_chart() + multi_values_table("v3-c3-values", "C74", c3_panels())
             + detail_head("v3-hours", "Errors by hour of the day, v2 against v3")
             + '<p class="chart-note">' + _structural_versions("Descriptive only: no hour or block effect is claimed.")
             + "</p>" + c5_chart() + hour_values_table("v3-c5-values", "C82", _hour_series()))
    crisis_note = ('<p class="chart-note">' + _structural_versions(
        "The protocol's stress period is fold 3, the 2022 crisis. Its peak, delivery 2022-08-15 to 2022-08-31, is the "
        "17 days charted here; their figures are for those days only, not the whole period. The dashed line marks 95% "
        "of the window's hours, the nominal target: a computed reference, not an observed count; there is no coverage "
        "guarantee.")
        .replace("17 days", S("count", "17") + " days")
        .replace("fold 3", "fold " + S("fold", "3")) + "</p>")
    stress = (detail_head("v3-crisis", "What happened in the 2022 crisis window") + crisis_note + block("v3.helps")
              + c4_chart() + values_table("v3-c4-values", "C79", c4_panels()))
    coverage = (detail_head("v3-coverage", "Did the intervals get more reliable, or only wider?") + block("v3.hurts")
                + c6_chart() + multi_values_table("v3-c6-values", "C80", c6_panels()))
    method = block("v3.recipe") + block("v3.missing") + block("v3.availability")
    return ChapterSlots(
        entry=entry,
        question="v3.question",
        change=block("v3.change.short") + feature_change(),
        chart=MainChart("v3-c2a", "C69", tuple(c2a_panels()),
                        title="v3 minus v2: equal-fold error-score differences with 95 percent confidence intervals",
                        desc="Two rows, the point-error score and the interval score. Each shows the estimated "
                             "difference as a dot and its 95 percent confidence interval as a line; both lie wholly "
                             "left of zero, which favours v3.",
                        subtitle="Difference in error score, v3 − v2 · paired 95% confidence interval · identical "
                                 "hours · development, post-selection"),
        headline="v3.chart_headline",
        reading="v3.reading",
        not_established=("v3.caveat.bundle", "v3.caveat.fold3", "v3.caveat.class"),
        decision="v3.decision",
        evidence=evidence_row(compare="compare:v3",
                              audit=checkpoint_audit("CP-20", source="reports/weather-ablation/uncertainty.csv", line=12)),
        details=(("method", method), ("per-period consistency", folds), ("stress period", stress),
                 ("coverage and width", coverage), ("protocol and review", protocol)),
    )


def v2_slots() -> ChapterSlots:
    entry = G.get("v2")
    scores = (detail_head("v2-control", "What the pooled-interval control established, and the scores against the targets")
              + v2_chart1() + block("v2.result.pb2") + block("v2.result.criteria")
              + values_table("v2-chart1-values", "C31", v2_chart1_panels()))
    return ChapterSlots(
        entry=entry,
        question="v2.question",
        change=block("v2.problem") + block("v2.change") + blend_change(),
        chart=MainChart("v2-chart2", "C37", tuple(v2_chart2_panels()),
                        title="v2's paired equal-fold error-score differences with 95 percent confidence intervals",
                        desc="Three contrasts in two panels. Against daily LEAR both intervals lie below zero. "
                             "Against the pooled-interval control the interval-score interval is below zero but the "
                             "point-error interval ends just above zero.",
                        subtitle="Difference in error score · paired 95% confidence intervals · identical hours · "
                                 "development, post-selection",
                        label_width=190),
        headline="v2.chart_headline",
        reading="v2.reading",
        not_established=("v2.caveat.attribution", "v2.caveat.split", "v2.caveat.class"),
        decision="v2.decision",
        evidence=evidence_row(compare="compare:v2",
                              audit=checkpoint_audit("CP-16", source="reports/v2-causal/uncertainty.csv", line=32)),
        details=(("protocol and review", scores),),
    )


def v3_chapter(*, open_folds: bool = False) -> str:
    return render_chapter(v3_slots(), open_details=("per-period consistency",) if open_folds else ())


def v2_chapter() -> str:
    return render_chapter(v2_slots())


def v1_holdout_table() -> str:
    """v1's one-shot holdout, exact (standard §4: the reading path rounds and floors; the table does not)."""
    rows = (("MAE, EUR/MWh", "holdout_mae_champion", "holdout_mae_naive"),
            ("Mean pinball loss, EUR/MWh", "holdout_pinball_champion", "holdout_pinball_naive"))
    body = "".join(f'<tr><th scope="row">{esc(label)}</th><td class="n exact">{v1(a)}</td><td class="n exact">{v1(b)}</td></tr>'
                   for label, a, b in rows)
    tests = (f'<tr><th scope="row">Diebold–Mariano statistic</th><td class="n exact" colspan="2">{v1("holdout_dm_statistic")}</td></tr>'
             f'<tr><th scope="row">Diebold–Mariano p-value</th><td class="n exact" colspan="2">{v1("holdout_dm_p_value")}</td></tr>'
             f'<tr><th scope="row">Coverage at {S("level", "50 / 80 / 95%")}</th><td class="n exact" colspan="2">'
             f'{v1("holdout_coverage_50")} / {v1("holdout_coverage_80")} / {v1("holdout_coverage_95")}</td></tr>')
    released = G.released()
    table = ('<div class="scroll" role="region" aria-label="The one-shot holdout, exact values" tabindex="0">'
             '<table class="data"><caption>The one-shot holdout, exact values</caption>'
             f'<thead><tr><th scope="col">Measure</th><th scope="col">{ver(released.version)}</th>'
             '<th scope="col">Similar-day naive</th></tr></thead>'
             f"<tbody>{body}{tests}</tbody></table></div>")
    return disclosure("v1-holdout-values", "View values", table)


def v1_chapter(C, archive: str) -> str:
    entry = G.get("v1")
    return f"""
<article class="chapter" id="v1" aria-labelledby="v1-h" data-research="v1">
 {chapter_header(entry, with_badge=False)}
 {block("v1.what")}
 <div class="panel holdout">
  <p class="holdout-head">The one-shot holdout {badge(RC.BADGE_V1_HOLDOUT, "holdout")}</p>
  {block("v1.holdout")}
  <p class="holdout-label">{v1("holdout_dm_label")}</p>
  {v1_holdout_table()}
 </div>
 {block("v1.unflattering")}
 {block("v1.lesson")}
 <p class="chapter-links"><a class="quiet" href="#product">How the released model works, topic by topic</a>
  <a class="quiet" href="#forecast">The replay in the archived report</a>
  <a class="quiet external" href="{attr(C['space_url'])}">Try the {ver(entry.version)} demo</a></p>
{v1_archive_disclosure(archive)}
</article>"""


def v1_archive_disclosure(archive: str) -> str:
    """v1's archive, the whole disclosure, byte-identical to `af0abb0` (brief W5; invariant 24).
    Frozen: its wrapper notes are part of the record as it was published, and are never edited."""
    return f""" <details class="disclosure archive" id="v1-archive">
  <summary><span class="marker" aria-hidden="true"></span><span>The original {ver("v1")} report (published
   {S("date", "2026-09-15")}), preserved</span></summary>
  <div class="disclosure-body">
   <p class="archive-note">Archived {ver("v1")} report, preserved as published. Its container deployment
    instructions are historical: the current demo runs in your browser, and this report needs no additional
    requests after loading. <a href="#reproduce">Current instructions</a> ·
    <a href="#research-results">Back to the model comparison</a></p>
   <div class="v1-archive">{archive}</div>
   <p class="archive-note"><a href="#research-results">Back to the model comparison</a> · <a href="#v1">Back to v1</a></p>
  </div>
 </details>"""


def planned_work() -> str:
    """Planned work, after the chapters (standard §6, amending plan §7.2): unscored, no version number."""
    current = G.current_generation()
    items = "".join(
        f'<li class="planned-item"><p class="planned-name">{esc(name)}</p>'
        f'<dl><dt>Question it will test</dt><dd>{_structural_versions(question)}</dd>'
        f'<dt>Evidence that would decide it</dt><dd>{_structural_versions(evidence)}</dd>'
        f'<dt>Work item</dt><dd>{S("work-item", item)} · {esc(code)}</dd></dl></li>'
        for name, item, code, question, evidence in PLANNED_WORK
    )
    teaser = ("Next: alternative models, renewable-generation forecasts and model combinations, then an "
              "evaluation of the selected model under a frozen protocol and prospective monitoring.")
    plan = github("docs/track-b/presentation-and-tracking-plan-2026-09-24.md")
    body = (
        "<p>Each item is subject to the research plan, where its conditions are set out, and would be compared "
        f"with {ver(current.version)} on identical hours and information "
        f'(<a class="quiet external in-text" href="{attr(plan)}">the plan</a>).</p>'
        f'<ol class="planned-list">{items}</ol>'
    )
    return (
        '<section class="section planned" id="planned" aria-labelledby="planned-h" data-research="planned">'
        f'<h2 id="planned-h">{esc(RC.PLANNED)}</h2><p>{esc(teaser)}</p>'
        + disclosure("planned-detail", "See planned experiments", body) + "</section>"
    )


#: The system view's data (plan §7.9): each step, what it does, whether it is implemented, and the
#: tools it runs on. The stack line is rendered from these tools, never typed (brief W13).
SYSTEM_VIEW = (
    ("Source data and vintages", "ENTSO-E and SMARD prices and load forecasts; for v3, the GFS run of the day before",
     "implemented", ("Python", "entsoe-py")),
    ("Information cutoff", "Forecast-cutoff checks; source-availability assumptions documented", "implemented",
     ("pandas",)),
    ("Features", "Calendar, price lags, load forecast; weather for v3", "implemented", ("pandas", "NumPy", "DuckDB")),
    ("Model and interval policy", "v1: LightGBM quantiles, conformal calibration; v2 and v3: blended LEAR, "
     "hour-aware intervals", "implemented", ("LightGBM", "scikit-learn")),
    ("Evaluation and artifacts", "Five historical periods, identical hours; committed predictions, metrics and "
     "reviews", "implemented", ("pandas", "Parquet", "GitHub Actions")),
    ("Report, demo and tracking", "This page, the in-browser v1 demo and the MLflow mirror", "implemented",
     ("GitHub Pages", "marimo", "Pyodide", "Hugging Face Static Space", "MLflow on DagsHub")),
    ("Live operation", "Daily forecasts scored after the fact", "planned", ()),
)


def stack_tools() -> tuple[str, ...]:
    """Every tool the implemented steps name, once, in flow order (brief W13)."""
    return tuple(dict.fromkeys(tool for _, _, state, tools in SYSTEM_VIEW if state == "implemented" for tool in tools))


def system_view() -> str:
    items = "".join(
        f'<li class="flow-step flow-{state}"><span class="flow-title">{esc(title)}'
        f'{" · planned" if state == "planned" else ""}</span><span class="flow-body">{_structural_versions(body)}</span></li>'
        for title, body, state, _tools in SYSTEM_VIEW
    )
    audit = github("docs/data-leakage-audit.md")
    tools = stack_tools()
    stack = ", ".join(esc(tool) for tool in tools[:-1]) + " and " + esc(tools[-1])
    return (
        '<ol class="flow" aria-label="Data flow, from source data to report">' + items + "</ol>"
        f'<p class="stack-line" data-stack="system-view"><strong>Built with</strong> {stack}.</p>'
        '<p class="flow-note">Checked in code: controls that fail when a feature crosses the forecast cutoff. '
        f'Assumed and documented: each source\'s historical availability (<a class="quiet external in-text" '
        f'href="{attr(audit)}">the availability assumptions</a>). Dashed outlines mark planned parts.</p>'
    )


def evidence_section(C) -> str:
    """How the system works (with its stack line), then how to rebuild and check it (standard §6)."""
    rebuild = rebuild_measurement()
    runtime = ""
    if rebuild:
        runtime = (f'Measured once on {S("date", rebuild["date"])}: '
                   f'<span data-release-check="{attr(rebuild["path"])}#seconds">{esc(rebuild["seconds"])}</span> s on the '
                   f'build machine ({esc(rebuild["machine"])}), from the release-check record '
                   f'<code>{esc(rebuild["path"])}</code>. It is one measurement, not a benchmark of every revision.')
    experiment = mlflow_route("experiment")
    track = ""
    if experiment:
        track = (f'<p>Every policy evaluated since {ver("v1")} is in the MLflow experiment '
                 f'<a class="quiet external in-text" href="{attr(experiment)}" data-route="experiment">'
                 f"<code>{esc(C['mlflow_next_experiment'])}</code></a>, mirrored from the repository's committed "
                 "evidence; the repository is the source of truth, and this page works without the tracking service.</p>")
    reproduce = (Audit("Reproduction instructions", "reports/weather-ablation/reproduce.md", "evidence/cp-20"),
                 Audit("Reproduction instructions", "reports/v2-causal/reproduce.md", "evidence/cp-16"),
                 Audit("Reproduction instructions", "reports/cp15/reproduction.md", "evidence/cp-15"))
    labelled = "".join(f"<li><span>{label}:</span> {audit_link(item)}</li>"
                       for label, item in zip((ver("v3"), ver("v2"), "the model comparison study"), reproduce))
    return f"""
<section class="section" id="evidence" aria-labelledby="evidence-h">
 <h2 id="evidence-h">How the system works, and how to check it</h2>
 <div id="system" class="system"><h3>How the system works</h3>{system_view()}</div>
 <div id="reproduce" class="reproduce"><h3>Rebuild the report from saved evidence</h3>
  <p>Rebuild the presentation from committed evidence, without fitting models or downloading source data.
   Install the pinned dependencies once (this downloads packages), then rebuild:</p>
  <pre><code>uv sync</code></pre>
  <pre><code>uv run python scripts/rebuild_presentation.py</code></pre>
  {disclosure("rebuild-measurement", "One measured rebuild", f"<p>{runtime}</p>") if runtime else ""}
  <p>Each experiment below has its own full reproduction. To run the released model, see
   <a href="#product-run">Run this product</a>; {ver("v1")}'s original instructions, with the historical container,
   are in <a href="#repro">its archive</a>.</p>
  <div class="evidence-row evidence-list"><span class="ev-label">Evidence</span><ul class="repro-list">{labelled}</ul></div>
 </div>
 <div class="tracking"><h3>Tracking</h3>
  {track}
  <p><a class="quiet external in-text" href="{attr(C['mlflow_experiment_url'])}">Experiment <code>{S("name", C['mlflow_experiment_name'])}</code></a>
   holds {ver("v1")}'s own runs. <a class="quiet external in-text" href="{attr(C['github_url'])}">Code and evidence on GitHub</a></p>
 </div>
</section>"""


def journey() -> str:
    return f"""
<section class="section" id="journey" aria-labelledby="journey-h">
 <span id="development-update" class="anchor-alias" aria-hidden="true"></span>
 <h2 id="journey-h">How it evolved</h2>
 {lineage()}
</section>"""


def chapter_versions() -> tuple[str, ...]:
    """The chapters' order, newest first, from the registry (standard §5, §6)."""
    return tuple(entry.version for entry in G.generations(newest_first=True))


def jump_row(generations: tuple[str, ...] | None = None) -> str:
    return ('<nav class="jump" aria-label="Chapters">'
            + "".join(f'<a href="#{g}">{ver(g)}</a>' for g in generations or chapter_versions()) + "</nav>")


def rail(generations: tuple[str, ...] | None = None) -> str:
    """The generation rail. The page's own routes live in the header only (review §5.1)."""
    known = {entry.version: entry.style for entry in G.generations()}
    links = "".join(f'<li><a href="#{g}" class="rail-{known.get(g, "x")}">'
                    f'<span class="dot" aria-hidden="true"></span>{ver(g)}</a></li>' for g in generations or chapter_versions())
    return ('<nav class="rail" aria-label="Generations"><p class="rail-head">Generations</p><ol>' + links
            + "</ol></nav>")


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
 <blockquote class="statement"><p>{esc(RC.CONTRIBUTION_STATEMENT)}</p>
 <footer>{esc(RC.OWNER_PUBLIC_NAME)}</footer></blockquote>
</section>"""


def attribution(C) -> str:
    return f"""
<section class="section attribution" id="attribution" aria-labelledby="attribution-h">
 <h2 id="attribution-h">Terms and attribution</h2>
 <p><span data-structural="attribution">{esc(C['attribution'])}</span></p>
 <p><span data-structural="attribution">{esc(C['licensing'])}</span></p>
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
.skip{{position:absolute;left:-999px;top:8px;background:var(--surface);padding:0 12px;min-height:44px;display:inline-flex;
 align-items:center;z-index:30}}
.skip:focus{{left:8px}}
/* header and navigation */
.site-header{{position:sticky;top:0;z-index:20;height:var(--header);background:rgba(250,250,250,.97);
 border-bottom:1px solid var(--border)}}
.header-inner{{max-width:var(--content);margin:0 auto;height:100%;display:flex;align-items:center;
 justify-content:space-between;gap:16px;padding:0 24px}}
.brand{{font-weight:650;color:var(--text);text-decoration:none;font-size:15px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
 min-height:44px;display:inline-flex;align-items:center}}
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
.byline{{font-size:14px;line-height:22px;color:var(--text-2);margin:-4px 0 20px}}
.statement footer{{margin-top:10px;font-size:15px;font-weight:600;color:var(--text)}}
.section{{padding:48px 0 16px;border-top:1px solid var(--border)}}
/* opening */
.opening{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.05fr);gap:40px;align-items:start;padding:40px 0 40px}}
.opening-aside .actions{{margin-top:0}}
.opening-aside .preview{{margin-top:16px}}
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
.quiet.in-text{{display:inline;padding:0;line-height:inherit}}
.branches-head{{font-size:13px;font-weight:650;text-transform:uppercase;letter-spacing:.05em;color:var(--text-2);margin:24px 0 0}}
.fc-note{{font-size:14px;color:var(--text-2);margin:6px 0 0}}
.external::after{{content:" \\2197";font-size:.85em}}
.startup{{font-size:14px;line-height:22px;color:var(--text-2);max-width:52ch}}
.preview{{margin:0}}
.preview-label{{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:center;font-size:14px;color:var(--text-2);margin-bottom:8px}}
.preview-key{{font-size:13px;color:var(--text-2);display:flex;gap:16px;flex-wrap:wrap;margin:8px 0 4px}}
.key-median::before{{content:"";display:inline-block;width:18px;height:3px;background:var(--v1);vertical-align:middle;margin-right:6px}}
.key-band::before{{content:"";display:inline-block;width:14px;height:12px;background:rgba(71,85,105,.22);vertical-align:middle;margin-right:6px;
 border-top:1px solid var(--ref);border-bottom:1px solid var(--ref);box-sizing:border-box}}
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
.finding{{margin-top:16px}}
.qualification{{color:var(--text-2)}}
.evidence-row{{display:flex;flex-wrap:wrap;align-items:center;gap:4px 18px;font-size:14px;border-top:1px solid var(--border);
 padding-top:12px;margin:16px 0 0;max-width:none}}
.ev-label{{font-size:13px;font-weight:650;color:var(--text-2);text-transform:uppercase;letter-spacing:.05em}}
.ev{{min-height:44px;display:inline-flex;align-items:center}}
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
.v1-archive .archive-context{{font-size:14px;color:var(--mute);margin:0 0 8px}}
.attribution-line{{font-size:14px;color:var(--text-2)}}
/* system view */
.flow{{list-style:none;padding:0;margin:16px 0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;counter-reset:flow}}
.flow-step{{border:1px solid var(--text-2);border-radius:10px;padding:10px 12px;background:var(--surface);position:relative}}
.flow-step.flow-planned{{border-style:dashed;background:transparent}}
.flow-title{{display:block;font-weight:650;font-size:15px}}
.flow-body{{display:block;font-size:14px;line-height:21px;color:var(--text-2)}}
.flow-note{{font-size:15px}}
pre{{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:12px 16px;overflow-x:auto;max-width:100%}}
.statement{{margin:0;padding:0 0 0 20px;border-left:3px solid var(--border);font-size:16px;line-height:26px;max-width:66ch}}
.site-footer{{max-width:var(--content);margin:0 auto;padding:24px;border-top:1px solid var(--border);font-size:14px;color:var(--text-2)}}
/* the headline block and the terms it introduces (standard §1, §3.4) */
.status-pair{{flex-direction:column;align-items:stretch;gap:10px;margin:20px 0}}
.status-research{{padding:12px 16px 14px}}
.status .status-name{{margin:0 0 6px;font-weight:650}}
.status-released{{display:flex;flex-wrap:wrap;gap:0 10px;align-items:baseline;padding:8px 14px}}
.status-released .status-name{{margin:0}}
.status dd.headline{{font-size:17px;line-height:26px;font-weight:600;margin:0 0 10px;max-width:60ch}}
.status dd.headline .badge{{margin-left:4px;vertical-align:1px;font-weight:600}}
.status dd.headline-terms{{font-weight:400;margin:0}}
.terms{{list-style:none;padding:10px 0 0;margin:0;border-top:1px solid var(--border);font-size:14px;line-height:21px;
 color:var(--text-2);display:grid;gap:4px}}
.terms li{{max-width:72ch}}
.terms strong{{color:var(--text);font-weight:650}}
.release-rule{{font-size:14px;line-height:22px;color:var(--text);max-width:56ch;border-left:3px solid var(--v1);
 padding-left:12px;margin:4px 0 12px}}
/* the comparison's finding (standard §1 i) */
.finding-title{{font-size:19px;line-height:28px;max-width:70ch;margin:0 0 6px}}
.caveat-line{{margin:0 0 12px}}
/* branch cards (standard §6) */
@media (min-width:621px){{.branches{{grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}}}}
.branch details.disclosure{{border-top:1px solid var(--border);margin-top:4px}}
.branch details.disclosure>summary{{font-size:14px;min-height:44px;padding:0}}
.branch .disclosure-body{{padding:0 0 8px}}
.branch{{border:1px solid var(--border);border-radius:10px;padding:10px 14px 4px;background:var(--surface);font-size:14px;line-height:21px}}
.branch p{{margin:0 0 4px;max-width:none}}
.branch .branch-head{{display:flex;flex-wrap:wrap;gap:0 10px;align-items:baseline;color:var(--text-2)}}
.branch .branch-name{{font-weight:650;font-size:16px;color:var(--text)}}
.branch .branch-head .adoption{{margin:0}}
.branch-q{{font-weight:600}}
.branch .evidence-row{{margin-top:6px;padding-top:0;gap:0 14px;border-top:0}}
.node-sub{{display:block;font-size:13px;line-height:19px;color:var(--text-2);margin-top:2px}}
/* the chapter grammar (standard §6) */
.change-figure{{margin:0 0 24px}}
.change-figure figcaption{{margin:0 0 8px}}
.change-figure .question{{font-size:18px;line-height:28px;font-weight:600;margin:0 0 8px}}
.chapter-head .eyebrow{{display:flex;gap:8px;align-items:baseline}}
.chapter-head .eyebrow .adoption{{margin:0}}
.chapter-head .chapter-sub{{font-size:17px;line-height:26px;color:var(--text-2);margin:0 0 8px}}
.not-established{{margin:0;padding-left:20px}}
.not-established li{{margin:0 0 8px;max-width:var(--prose)}}
.reading{{font-weight:500}}
/* the system view's stack line (brief W13) */
.stack-line{{font-size:15px;max-width:none}}
.evidence-list{{display:block}}
.repro-list{{list-style:none;margin:4px 0 0;padding:0}}
.repro-list li{{display:flex;flex-wrap:wrap;gap:0 8px;align-items:center}}
/* phones and narrow windows (§7.10) */
@media (max-width:980px){{
 .opening{{grid-template-columns:minmax(0,1fr);gap:24px;padding-top:28px}}
 .story,.road .story{{grid-template-columns:minmax(0,1fr)}}
 .flow{{grid-template-columns:repeat(2,minmax(0,1fr))}}
 .branches{{grid-template-columns:minmax(0,1fr)}}
}}
@media (max-width:620px){{
 .section{{padding-top:32px}}
 h2{{margin-bottom:14px}}
 .node-sub{{display:none}}
 .mainline{{margin:12px 0 4px;gap:10px}}
 .node-name{{font-size:16px;line-height:23px}}
 .branches-head{{margin-top:14px}}
 .preview.panel{{padding:12px}}
 .preview-label{{margin-bottom:4px}}
 .preview-key{{margin:4px 0 0;gap:4px 12px}}
 .terms{{gap:2px;line-height:19px}}
 .opening{{gap:12px}}
 .mainline{{gap:6px}}
 .branches-head{{margin-top:8px}}
 .section{{padding-top:24px}}
 .preview-note{{display:none}}
 .release-rule{{margin:0 0 8px}}
 .startup{{margin:0 0 4px}}
 .finding-title{{font-size:17px;line-height:25px}}
 .opening{{padding-top:12px;gap:16px}}
 .opening .eyebrow{{margin-bottom:4px}}
 h1{{margin:6px 0 10px}}
 .byline{{margin:-6px 0 12px}}
 .status-pair{{margin:14px 0}}
 .status dd.headline{{font-size:16px;line-height:24px}}
 .branches{{grid-template-columns:minmax(0,1fr)}}
 .header-inner{{padding:0 16px}}
 .brand-full{{display:none}}.brand-short{{display:inline}}
 .main-nav a{{padding:0 8px}}
 .page{{padding:0 16px 64px}}
 h1{{font-size:32px;line-height:1.1}}
 h2{{font-size:25px}}
 .chapter-head h2{{font-size:26px}}
 .lede{{font-size:16px;line-height:25px;margin-bottom:12px}}
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
 .statement{{font-size:16px}}
}}
@media (max-width:440px){{
 .brand-short{{display:none}}.brand-tiny{{display:inline}}
 .reproduce pre{{white-space:pre-wrap;overflow-wrap:anywhere}}
}}
@media (max-width:340px){{
 .header-inner,.page{{padding-left:12px;padding-right:12px}}
 .panel,.preview.panel{{padding:12px 8px}}
 .main-nav a{{padding:0 6px;font-size:14px}}
}}
.opening-copy details.disclosure{{margin-top:4px;border-bottom:1px solid var(--border)}}
.opening-copy details.disclosure>summary{{font-size:14px;font-weight:600;color:var(--text-2)}}
.opening-copy .disclosure-body p{{font-size:14px;line-height:22px;color:var(--text-2)}}
.chapter-sub{{font-size:19px;line-height:29px;color:var(--text);max-width:60ch;margin:0 0 20px}}
.change{{margin:0 0 24px}}

.preview-note{{font-size:13px;color:var(--text-2)}}
td .ci,td .unit,th .unit{{color:var(--text-2);font-weight:400}}
th .unit{{font-size:12px}}
/* how the product works (PUBLISH_RULES 1.0 A4): orientation and routes on the reading path, topics in one disclosure */
.section.product{{padding-top:32px}}
.product-lede{{margin:0 0 12px}}
.product-routes ol{{list-style:none;padding:0;margin:12px 0 16px;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px 12px}}
.product-routes a{{display:flex;align-items:center;min-height:44px;height:100%;padding:6px 12px;border:1px solid var(--border);
 border-radius:10px;background:var(--surface);color:var(--text);text-decoration:none;font-size:14px;line-height:19px;font-weight:550}}
.product-routes a:hover{{border-color:var(--text-2)}}
.topic{{padding:24px 0 8px;border-top:1px solid var(--border)}}
.topic:first-child{{border-top:0;padding-top:4px}}
.topic h3{{font-size:21px;line-height:1.3;margin:0 0 12px}}
.topic .panel{{margin:8px 0 16px}}
.limitations li{{margin:0 0 8px;max-width:var(--prose)}}
[data-structural="command"]{{font-family:var(--mono);font-size:.9em;overflow-wrap:anywhere;background:#F4F4F5;padding:1px 4px;border-radius:4px}}
.run [data-v1="champion_fingerprint"],.run [data-v1="snapshot_sha256"]{{font-family:var(--mono);font-size:.88em;overflow-wrap:anywhere}}
.replay-controls{{display:flex;flex-wrap:wrap;gap:8px 24px;align-items:flex-end;margin:8px 0 12px}}
.replay-controls fieldset{{border:1px solid var(--border);border-radius:8px;padding:0 12px 2px;margin:0}}
.replay-controls legend{{font-size:13px;color:var(--text-2);padding:0 4px}}
.replay-controls fieldset label{{display:inline-flex;align-items:center;gap:6px;min-height:44px;margin-right:14px}}
.replay-range{{display:flex;flex-direction:column}}
.replay-range label{{font-size:14px;color:var(--text-2)}}
.replay-range input{{min-height:44px;width:240px;max-width:100%}}
.replay-chart{{display:block;width:100%;height:auto;border:1px solid var(--border);border-radius:8px;background:var(--surface)}}
/* adopted transitions (A3) and the rejected branches, headed apart */
.transitions-head{{font-size:13px;font-weight:650;text-transform:uppercase;letter-spacing:.05em;color:var(--text-2);margin:28px 0 10px}}
.transition{{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:16px 20px;margin:0 0 16px}}
.transition h4{{font-size:19px;line-height:1.3;margin:0 0 4px}}
.transition-meta{{margin:0 0 8px}}
.transition-fields{{display:grid;grid-template-columns:max-content minmax(0,1fr);gap:6px 18px;margin:0;font-size:15px;line-height:24px}}
.transition-fields div{{display:contents}}
.transition-fields dt{{font-weight:650;color:var(--text-2)}}
.transition-fields dd{{margin:0;max-width:var(--prose)}}
.transition-route{{margin:10px 0 0}}
/* discovery routes (A5): descriptive links from a chapter's summary to the charts inside its details */
.explore{{margin:12px 0 16px}}
.explore ul{{list-style:none;padding:0;margin:0;display:flex;flex-wrap:wrap;gap:0 22px}}
.explore a{{display:inline-flex;align-items:center;min-height:44px}}
.detail-head{{font-size:17px;line-height:1.35;margin:28px 0 8px}}
.disclosure-body>.detail-head:first-child{{margin-top:8px}}
@media (max-width:980px){{.product-routes ol{{grid-template-columns:repeat(3,minmax(0,1fr))}}}}
@media (max-width:620px){{
 .section.product{{padding-top:20px}}
 .product-routes ol{{grid-template-columns:repeat(2,minmax(0,1fr));gap:6px 8px;margin:8px 0 12px}}
 .product-routes a{{padding:4px 10px;font-size:14px;line-height:18px}}
 .transition{{padding:12px 14px}}
 .transition-fields{{grid-template-columns:minmax(0,1fr);gap:0}}
 .transition-fields dt{{margin-top:8px}}
 .topic h3{{font-size:19px}}
}}
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
.v1-archive input[type=range]{{min-height:44px}}
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
.v1-archive .toc a{{display:flex;align-items:center;min-height:44px;padding:0}}
@media (max-width:620px){{.v1-archive .toc{{columns:1}}.v1-archive .kv{{grid-template-columns:1fr}}.v1-archive .kv dd{{margin-bottom:8px}}}}
"""


# --------------------------------------------------------------------------- scripts


CHART_JS = """
(function(){
 var D=window.__FAN__;
 // One fan-chart renderer, two instances over the same precomputed replay (nothing is fetched or recomputed):
 // v1's archived report, whose ids, colours and behaviour are unchanged, and the product documentation's replay.
 function fan(o){
  var W=o.maxW,H=380,ML=58,MR=16,MT=18,MB=34,FS=11,STEP=2;
  var n=D.hours.length,dom=D.domain,svg=o.svg,c=o.colors;
  // Draw at the chart's rendered width, so a phone gets a phone geometry and 12 px text instead of a
  // shrunk desktop drawing. The data, controls and their behaviour are unchanged.
  function geometry(){
   var w=Math.round(svg.getBoundingClientRect().width)||o.maxW;
   W=Math.max(280,Math.min(o.maxW,w));
   var narrow=W<600;
   H=narrow?300:o.maxH;ML=narrow?44:58;MR=narrow?10:16;MT=narrow?22:18;FS=12;STEP=narrow?4:2;
   svg.setAttribute('viewBox','0 0 '+W+' '+H);
  }
  function X(i){return ML+(W-ML-MR)*(n<2?0.5:i/(n-1));}
  function Y(v){return MT+(H-MT-MB)*(1-(v-dom[0])/(dom[1]-dom[0]));}
  function state(){
   var lv=document.querySelector('input[name='+o.level+']:checked').value;
   var sc=D.scales[parseInt(o.scale.value,10)];
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
   var root=o.group?svg.querySelector('g.plot'):svg;
   while(root.firstChild){root.removeChild(root.firstChild);}
   ticks().forEach(function(t){
    root.appendChild(el('line',{x1:ML,x2:W-MR,y1:Y(t),y2:Y(t),stroke:t===0?c.zero:c.grid,'stroke-width':t===0?1.2:1}));
    root.appendChild(el('text',{x:ML-8,y:Y(t)+4,'text-anchor':'end',fill:c.text,'font-size':FS},t));
   });
   for(var i=0;i<n;i+=STEP){
    root.appendChild(el('text',{x:X(i),y:H-12,'text-anchor':'middle',fill:c.text,'font-size':FS},D.hours[i]));
   }
   var up=[],down=[];
   for(var j=0;j<n;j++){up.push(X(j)+','+Y(rows[j][hi]));}
   for(var k=n-1;k>=0;k--){down.push(X(k)+','+Y(rows[k][li]));}
   root.appendChild(el('polygon',{points:up.concat(down).join(' '),fill:c.band,'fill-opacity':c.bandOpacity,stroke:c.bandEdge,'stroke-width':1}));
   var med=[];
   for(var m=0;m<n;m++){med.push(X(m)+','+Y(rows[m][mi]));}
   root.appendChild(el('polyline',{points:med.join(' '),fill:'none',stroke:c.median,'stroke-width':c.medianWidth}));
   if(s.sc==='1.00'){
    var act=[];
    for(var a=0;a<n;a++){act.push(X(a)+','+Y(D.actual[a]));}
    root.appendChild(el('polyline',{points:act.join(' '),fill:'none',stroke:c.actual,'stroke-width':1.6,'stroke-dasharray':'6 4'}));
   }
   root.appendChild(el('text',{x:ML,y:MT-6,fill:c.text,'font-size':FS},
    W<600?('EUR/MWh · local hour · '+D.delivery_day):('EUR/MWh  ·  local hour (Europe/Berlin)  ·  delivery day '+D.delivery_day)));
   o.show(s);
  }
  Array.prototype.forEach.call(document.querySelectorAll('input[name='+o.level+']'),function(r){r.addEventListener('change',draw);});
  o.scale.addEventListener('input',draw);
  if(o.holder){o.holder.addEventListener('toggle',function(){if(o.holder.open){draw();}});}
  var pending=null;
  window.addEventListener('resize',function(){clearTimeout(pending);pending=setTimeout(draw,150);});
  draw();
 }
 fan({svg:document.getElementById('chart'),level:'lvl',scale:document.getElementById('scale'),
  holder:document.getElementById('v1-archive'),maxW:960,maxH:380,group:false,
  colors:{grid:'#eceff3',zero:'#9aa7b4',text:'#5a6a7a',band:'#3a6ea5',bandOpacity:.22,bandEdge:'#3a6ea5',
   median:'#1b3a5c',medianWidth:2.2,actual:'#b03a2e'},
  show:function(s){
   document.getElementById('scaleval').textContent='\\u00d7 '+s.sc;
   document.getElementById('cov').textContent=window.__COV__[s.lv];
   document.getElementById('scenario').style.display=(s.sc==='1.00')?'none':'block';
   document.getElementById('legend-actual').style.display=(s.sc==='1.00')?'inline':'none';
  }});
 var p=document.getElementById('p-chart');
 if(p){fan({svg:p,level:'p-lvl',scale:document.getElementById('p-scale'),holder:document.getElementById('product-manual'),
  maxW:760,maxH:320,group:true,
  colors:{grid:'#E4E4E7',zero:'#71717A',text:'#52525B',band:'#475569',bandOpacity:.18,bandEdge:'#71717A',
   median:'#475569',medianWidth:2.4,actual:'#18181B'},
  show:function(s){
   document.getElementById('p-scaleval').textContent=s.sc;
   document.getElementById('p-scale').setAttribute('aria-valuetext','\\u00d7 '+s.sc);
   var cov=document.getElementById('p-cov');
   cov.textContent=window.__COV__[s.lv];cov.setAttribute('data-v1','holdout_coverage_'+s.lv);
   document.getElementById('p-scenario').hidden=(s.sc==='1.00');
   document.getElementById('p-legend-actual').style.display=(s.sc==='1.00')?'inline':'none';
  }});}
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
    after v1" around the claim set's current note (plan §8.7). One context note sits under the replay's
    heading, so a reader who lands there from the preview learns that its hosting notes are historical
    (final audit F08). Its text, figures, tables and interactive fan chart are otherwise unchanged
    (invariant 24)."""
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
<p class="archive-context">Archived v1 report. The replay below runs in this page; the current interactive demo
runs in your browser, and the container instructions later in this report are historical.</p>
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
<p class="next"><strong>Tracking after v1.</strong> {esc(ARCHIVE_TRACKING_NOTE)}
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


#: The page's own icon, inline (review F02): without one, a browser asks the host for /favicon.ico, a request the
#: offline page must not make and that Pages answered with 404. A `data:` URI is part of the document.
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' "
           "height='16' rx='3' fill='%23475569'/%3E%3Cpath d='M3 11l3-4 3 2 4-5' fill='none' stroke='%23fff' "
           "stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E")

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
    generations = (("v7", "v6", "v5", "v4") if stress else ()) + chapter_versions()
    jump = jump_row(generations)
    chapters = (stress_chapters() if stress else "") + chapter_sequence(C, archive, specimen=specimen)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(TITLE)}</title>
<meta name="description" content="{attr(DESCRIPTION)}">
<link rel="icon" href="{attr(FAVICON)}">
<style>{css()}</style>
</head>
<body>
<a class="skip" href="#main">Skip to the content</a>
{header()}
<div class="page"><div class="with-rail">
{rail(generations)}
<main id="main">
{opening(C, payload)}
{product_section(C, payload)}
{results()}
{journey()}
<section class="section chapters" id="chapters" aria-labelledby="chapters-h">
 <h2 id="chapters-h">How the research improved, newest first</h2>
 {jump}
 {chapters}
</section>
{planned_work()}
{evidence_section(C)}
{contribution()}
{attribution(C)}
</main>
</div></div>
<footer class="site-footer"><p>This report is a self-contained page with no additional runtime requests.
<a href="#attribution">Terms and attribution</a> · <a href="#top">Back to the top</a></p></footer>
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


class RouteCoverageError(RuntimeError):
    """A final build whose verified index does not cover every route the registry expects."""


def route_coverage() -> tuple[list[str], list[str]]:
    """(published, missing): the registry's expected routes that the verified index holds, and
    those it does not. A missing route's link is omitted, never shown as a placeholder (standard §9)."""
    routes = mlflow_index().get("routes", {})
    expected = list(G.expected_routes())
    published = [route for route in expected if routes.get(route, {}).get("url")]
    return published, [route for route in expected if route not in published]


def refuse_incomplete(missing: list[str]) -> None:
    """The final build runs only when the verified index covers every expected route (brief W10)."""
    if missing:
        raise RouteCoverageError(f"final build refused: the verified MLflow index lacks {missing}")


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
    omitted = evidence_row(audit=(Audit("Review verdict", "docs/track-b/evidence/cp-20/integration.md", "evidence/cp-20"),))
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
<p class="outcome-value">{RC.svg_value("cp20.uncertainty.HG-H0.equal_fold.MAE")} headline value (30 px, tabular numerals)</p>
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
 <div class="state"><h4>Evidence row</h4>{evidence_row(compare="compare:v3", audit=checkpoint_audit("CP-20"))}
  <p class="archive-note">A route that is not verified has its link omitted, never a placeholder:</p>{omitted}</div>
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
    parser.add_argument("--final", action="store_true",
                        help="refuse unless the verified MLflow index covers every route the registry expects "
                             "(any build records final: true exactly when it does)")
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
    published, missing = route_coverage()
    if args.final:
        try:
            refuse_incomplete(missing)
        except RouteCoverageError as exc:
            raise SystemExit(str(exc))
    document = build_html()
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
                # Final exactly when nothing is omitted, so a plain rebuild reproduces a final build
                # and an incomplete one can never be recorded as final (standard §9).
                "final": not missing,
                "routes_expected": sorted(G.expected_routes()),
                "routes_published": sorted(published),
                "links_omitted_until_verified": sorted(missing),
                "mlflow_index_verified_at_utc": mlflow_index().get("verified_at_utc"),
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
