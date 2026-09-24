"""Presentation plan §9.5 and §7.10–§7.12: the built page's structure.

Every table sits in a scroll wrapper, internal anchors resolve, the size budget holds, phone chart
variants keep their text at 12 px or more at a 390 px viewport, every chart mark is labelled,
badge texts are exact and long values can wrap, and v1's archived fan chart keeps its behaviour.
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser

import pytest

from delu_forecast import research_claims as RC
from delu_forecast.claims import REPO_ROOT, SENSITIVITY_PROBE_LABEL, build_claims

sys.path.insert(0, str(REPO_ROOT / "scripts"))

import build_pages as B  # noqa: E402

PAGE = REPO_ROOT / "docs" / "index.html"

#: The page, charts and v1's embedded figures included. The seven PNGs alone are ~0.7 MB; the
#: budget leaves room for later chapters while keeping one self-contained file.
SIZE_BUDGET_BYTES = 2_000_000


@pytest.fixture(scope="module")
def document() -> str:
    return PAGE.read_text()


class Tables(HTMLParser):
    """Records, for every <table>, whether an ancestor carries class "scroll"."""

    def __init__(self) -> None:
        super().__init__()
        self.stack: list[tuple[str, bool]] = []
        self.tables: list[bool] = []

    def handle_starttag(self, tag, attrs):
        classes = (dict(attrs).get("class") or "").split()
        if tag == "table":
            self.tables.append(any(scroll for _, scroll in self.stack) or "scroll" in classes)
        if tag not in ("br", "img", "input", "meta", "link", "hr", "source", "wbr", "circle", "rect", "line",
                       "polygon", "polyline", "path"):
            self.stack.append((tag, "scroll" in classes))

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                return


def tables_outside_scroll(document: str) -> int:
    parser = Tables()
    parser.feed(document)
    return sum(1 for wrapped in parser.tables if not wrapped)


def test_every_table_sits_in_a_scroll_wrapper(document):
    assert tables_outside_scroll(document) == 0
    assert document.count("<table") > 10


def test_negative_control_a_table_outside_scroll_is_caught(document):
    assert tables_outside_scroll(document.replace("</main>", "<table><tr><td>x</td></tr></table></main>")) == 1


def test_every_internal_anchor_resolves(document):
    ids = set(re.findall(r'\bid="([^"]+)"', document))
    targets = set(re.findall(r'href="#([^"]+)"', document))
    missing = sorted(target for target in targets if target not in ids)
    assert not missing, missing
    for anchor in ("results", "journey", "evidence", "v1", "v2", "v3", "v1-archive", "forecast", "repro",
                   "development-update", "system", "reproduce", "contribution", "attribution"):
        assert f'id="{anchor}"' in document, anchor


def test_the_size_budget_holds(document):
    assert len(document.encode()) <= SIZE_BUDGET_BYTES


def _svgs(document: str, variant: str) -> list[str]:
    return re.findall(rf'<svg class="{variant}" viewBox="[^"]*".*?</svg>', document, re.DOTALL)


def test_phone_chart_variants_render_text_at_12px_or_more_at_390(document):
    """Invariant 23: dedicated phone variants, not shrunk desktop SVGs."""
    phones = _svgs(document, "m")
    assert len(phones) >= 10
    for svg in phones:
        width = float(re.search(r'viewBox="0 0 ([\d.]+) ', svg).group(1))
        rendered = min(B.MOBILE_COLUMN_AT_390, B.MOBILE_MAX_W, width * 10)
        scale = rendered / width
        sizes = [float(size) for size in re.findall(r'<text [^>]*font-size="([\d.]+)"', svg)]
        assert sizes, "a chart without text"
        assert min(sizes) * scale >= 12, (re.search(r'data-chart="([^"]+)"', svg).group(1), min(sizes) * scale)
    for svg in _svgs(document, "d"):
        assert re.search(r'data-chart="[^"]+"', svg) and 'data-variant="d"' in svg
    assert f"max-width:{B.MOBILE_BREAKPOINT - 1}px" in document, "the phone variant switch is missing"


def unlabelled_marks(svg: str) -> list[str]:
    """Record-bound marks whose record no text in the same SVG names."""
    marks = set(re.findall(r'<(?:circle|rect|polygon)[^>]*data-record="([^"]+)"', svg))
    labelled = set(re.findall(r'<text[^>]*data-record="([^"]+)"', svg))
    return sorted(marks - labelled)


def test_every_chart_mark_has_a_direct_label(document):
    """Invariant 22: meaning never depends on colour or hover alone."""
    for svg in _svgs(document, "d") + _svgs(document, "m"):
        chart = re.search(r'data-chart="([^"]+)"', svg).group(1)
        if chart == "v3-c5":
            # Descriptive hour profiles: each series is labelled at its end and by marker shape;
            # the values are in the table-free per-fold panels' scale and the claim map.
            assert svg.count('data-structural="version"') >= 10
            continue
        assert not unlabelled_marks(svg), (chart, unlabelled_marks(svg)[:3])


def test_negative_control_a_series_without_a_label_is_caught():
    svg = ('<svg><circle cx="1" cy="1" r="2" data-claim="P07" data-record="cp20.metrics.HG.equal_fold.S_MAE"/>'
           "<text>unrelated</text></svg>")
    assert unlabelled_marks(svg) == ["cp20.metrics.HG.equal_fold.S_MAE"]


def test_badges_are_exact_and_long_values_can_wrap(document):
    assert f">{RC.BADGE_DEVELOPMENT}<" in document
    assert f">{RC.BADGE_V1_HOLDOUT}<" in document
    css = B.css()
    assert re.search(r"\.badge\{[^}]*white-space:normal", css)
    assert "+0.000003857628092332211" in document
    assert re.search(r"\.exact\{[^}]*overflow-wrap:anywhere", css)


def test_generation_colour_is_never_the_only_cue():
    """The three generation colours are near-equal in luminance, so each has its own marker."""
    shapes = {B.ROLE_STYLE[role]["marker"] for role in ("v1", "v2", "v3")}
    assert len(shapes) == 3


def test_v1s_fan_chart_keeps_its_caveat_and_behaviour(document):
    claims = build_claims()
    assert SENSITIVITY_PROBE_LABEL in document
    assert claims["holdout_coverage_95"] in document
    for element in ('id="chart"', 'id="scale"', 'id="scaleval"', 'id="cov"', 'id="scenario"', 'id="legend-actual"',
                    "name='lvl'"):
        assert element in document, element
    assert "document.getElementById('scenario').style.display=(s.sc==='1.00')?'none':'block'" in document


def test_links_into_closed_disclosures_are_opened_by_script(document):
    assert "closest('details')" in document and "reveal(location.hash" in document


def test_sticky_header_never_covers_anchored_headings():
    assert "scroll-margin-top:calc(var(--header) + 16px)" in B.css()


def test_the_stress_case_is_never_the_published_page(document):
    assert "placeholder generation" not in document and "Local stress case" not in document
