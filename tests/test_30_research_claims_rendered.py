"""Presentation plan §9.5: research claims render only through the claim layer, and only as approved.

The provenance proof is test_29 (every record re-derives from its row). This file checks the
layer above it: every rendered claim exists in the claim layer and a claim map, every numeral in a
research block is bound to a record or declared structural, withheld and stale phrasing is absent,
no v2+ record crosses the development boundary, and the exact H−P endpoint is never rounded.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from delu_forecast import research as R
from delu_forecast import research_claims as RC
from delu_forecast.claims import REPO_ROOT

README = REPO_ROOT / "README.md"
BARE_NUMERAL = re.compile(r"\S*\d\S*")
BOUND = re.compile(r"<data\b[^>]*>.*?</data>|<span data-structural=\"[^\"]+\">.*?</span>", re.DOTALL)
TAG = re.compile(r"<[^>]+>")


def unbound_numerals(fragment: str) -> list[str]:
    """Numerals left once every claim-bound value and declared structural numeral is removed."""
    return BARE_NUMERAL.findall(TAG.sub(" ", BOUND.sub(" ", fragment)))


# -- the claim layer and the maps ----------------------------------------------


def test_every_claim_the_layer_renders_is_in_a_claim_map():
    missing = sorted(RC.all_claim_ids() - RC.claim_map_ids())
    assert not missing, f"claims rendered but absent from both claim maps: {missing}"


def test_the_maps_define_the_withheld_list_w1_to_w21():
    ids = RC.claim_map_ids()
    assert {f"W{n}" for n in range(1, 22)} <= ids


@pytest.mark.parametrize("block", RC.BLOCKS, ids=lambda b: b.key)
def test_every_block_renders_and_binds_every_numeral(block):
    rendered = RC.render(block.key, surface=sorted(block.surfaces)[0])
    assert unbound_numerals(rendered) == [], f"{block.key}: unbound numerals {unbound_numerals(rendered)}"
    for record_id in block.records():
        assert f'data-record="{record_id}"' in rendered
    assert f'data-claim="{block.claim_id}"' in rendered or not block.records()


@pytest.mark.parametrize("block", RC.BLOCKS, ids=lambda b: b.key)
def test_no_block_carries_withheld_or_stale_phrasing(block):
    for target in ("html", "md"):
        text = TAG.sub(" ", RC.render(block.key, target, surface=sorted(block.surfaces)[0]))
        assert not RC.withheld_findings(text), (block.key, RC.withheld_findings(text))
        assert not RC.stale_findings(text), (block.key, RC.stale_findings(text))


def test_every_block_record_is_a_real_record():
    for block in RC.BLOCKS:
        for record_id in block.records():
            R.get(record_id)


# -- guards on the typed fields -------------------------------------------------


def test_date_guard_v2_and_later_records_stay_inside_development():
    for block in RC.BLOCKS:
        for record_id in block.records():
            record = R.get(record_id)
            if record.checkpoint in ("CP-15", "CP-16", "CP-20") and record.window:
                assert record.window[1] <= R.EVIDENCE_BOUNDARY, (block.key, record_id, record.window)


def test_date_guard_negative_control():
    import dataclasses

    record = R.get("cp20.metrics.HG.fold_5.MAE")
    late = dataclasses.replace(record, window=("2026-06-09", "2026-09-06"))
    assert late.window[1] > R.EVIDENCE_BOUNDARY


def test_the_exact_endpoint_is_forced_wherever_it_is_rendered():
    html = RC.render("v2.result.hp")
    assert "+0.000003857628092332211" in html
    assert "0.0000]" not in html and "0.0000<" not in html
    # Even a template that asks for the rounded endpoint gets the full value.
    forced = RC.render_template("C34", "{r:cp16.uncertainty.V2-H-V2-P.equal_fold.MAE|hi}")
    assert "+0.000003857628092332211" in forced


def test_the_readme_block_carries_no_withheld_or_stale_phrasing():
    text = README.read_text()
    block = text[text.index("<!-- research:start -->"):text.index("<!-- research:end -->")]
    assert not RC.withheld_findings(block), RC.withheld_findings(block)
    assert not RC.stale_findings(block), RC.stale_findings(block)


# -- negative controls -----------------------------------------------------------


def test_negative_control_an_undeclared_numeral_is_caught():
    rendered = RC.render_template("C69", "The gain is 7.8% on {r:cp20.metrics.HG.equal_fold.S_MAE}.")
    assert unbound_numerals(rendered) == ["7.8%"]


def test_negative_control_a_structural_numeral_is_not_a_finding():
    rendered = RC.render_template("C69", "In fold {s:fold:3} the value is {r:cp20.metrics.HG.fold_3.MAE}.")
    assert unbound_numerals(rendered) == []


def test_negative_control_a_missing_claim_id_is_caught():
    assert "C999" not in RC.claim_map_ids()
    with pytest.raises(RC.ClaimError):
        RC.svg_binding("C999", "cp20.metrics.HG.equal_fold.S_MAE")


def test_negative_control_an_unknown_record_is_caught():
    with pytest.raises(R.EvidenceError):
        RC.render_template("C69", "{r:cp20.metrics.HG.equal_fold.S_MAX}")


@pytest.mark.parametrize(
    "sentence, withheld",
    [
        ("Hour-aware intervals are better than pooled ones.", "W1"),
        ("The interval ends at +0.0000] so it improves.", "W3"),
        ("This result is statistically significant.", "W7"),
        ("Wind at 100 m drives the gain.", "W17"),
        ("The model passed peer review.", "W18"),
        ("Try the v3 demo in your browser.", "W19"),
        ("v3 is 46% better than v1.", "W20"),
        ("The holdout gave a confirmatory result.", "W21"),
        ("It has a coverage guarantee.", "W15"),
    ],
)
def test_negative_control_withheld_phrasing_is_caught(sentence, withheld):
    assert any(finding.startswith(withheld) for finding in RC.withheld_findings(sentence)), sentence


@pytest.mark.parametrize(
    "sentence",
    [
        "The holdout label is confirmatory-style, not power-qualified.",
        "The development results are never confirmatory.",
        "Residual intervals carry no conformal coverage guarantee.",
        "An independent Integration review within this project's process.",
    ],
)
def test_negative_control_honest_denials_are_not_findings(sentence):
    assert not RC.withheld_findings(sentence), sentence


def test_negative_control_stale_phrasing_is_caught():
    assert RC.stale_findings("Its runs land in a separate `delu-m4` experiment.")
    assert RC.stale_findings("it is the defect the planned v2 targets")


# -- the built page (§9.3 markup contract, §9.5 guards) -----------------------------

import json  # noqa: E402
import sys  # noqa: E402
from html.parser import HTMLParser  # noqa: E402

from delu_forecast.claims import build_claims  # noqa: E402

sys.path.insert(0, str(REPO_ROOT / "scripts"))

import build_pages as B  # noqa: E402

PAGE = REPO_ROOT / "docs" / "index.html"

#: Digits a declared structural *label* may carry: versions, levels, folds, dates, years,
#: checkpoint and policy codes, heights, criterion ranges. Anything else is a typed number.
LABEL_ALLOWED = re.compile(
    r"\bv\d\b|\b\d{1,3}(?:\.\d)?%|\bFold \d\b|\b\d{4}-\d{2}-\d{2}\b|\b(?:19|20)\d{2}\b|\bCP-\d+\b"
    r"|\b[AB]\d\b|\bH0\b|\bV2-[HP]\b|\b\d{2,3} m\b|\b\d–\d\b|\bΔ?S_(?:MAE|WIS)\b"
)


@pytest.fixture(scope="module")
def page() -> str:
    return PAGE.read_text()


class ResearchText(HTMLParser):
    """Collects text inside `data-research` sections that no binding or declaration covers.

    Bound: `<data>` and SVG elements with `data-claim`/`data-record`, `data-v1` values, release-check
    values, `data-scale` ticks, `data-structural` declarations. v1's archived report is excluded:
    its numbers are bound by the v1 claim set (tests 17 and 21)."""

    VOID = {"br", "img", "input", "meta", "link", "hr", "source", "wbr", "circle", "rect", "line", "polygon",
            "polyline", "path"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, str]] = []  # (tag, role)
        self.unbound: list[str] = []
        self.labels: list[str] = []
        self.meta: list[str] = []

    def _role(self, tag: str, attrs: dict) -> str:
        if attrs.get("id") == "v1-archive" or "v1-archive" in (attrs.get("class") or "").split():
            return "archive"
        if tag in ("title", "desc"):
            return "meta"
        if "data-claim" in attrs or "data-v1" in attrs or "data-release-check" in attrs or "data-scale" in attrs:
            return "bound"
        if "data-structural" in attrs:
            return "label" if attrs["data-structural"] == "label" else "bound"
        if "data-research" in attrs:
            return "research"
        return ""

    def handle_starttag(self, tag, attrs):
        if tag in self.VOID:
            return
        self.stack.append((tag, self._role(tag, dict(attrs))))

    def handle_startendtag(self, tag, attrs):
        return

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                return

    def handle_data(self, data):
        roles = [role for _, role in self.stack]
        if "research" not in roles or "archive" in roles or "bound" in roles:
            return
        if not any(ch.isdigit() for ch in data):
            return
        if "meta" in roles:
            self.meta.append(data)
        elif "label" in roles:
            self.labels.append(data)
        elif self.stack and self.stack[-1][0] in ("script", "style"):
            return
        else:
            self.unbound.extend(BARE_NUMERAL.findall(data))


def research_scan(document: str) -> ResearchText:
    parser = ResearchText()
    parser.feed(document)
    return parser


def test_page_research_numerals_are_all_bound_or_declared(page):
    scan = research_scan(page)
    assert not scan.unbound, f"unbound numerals in research sections: {scan.unbound[:20]}"
    bad_labels = [text for text in scan.labels if any(ch.isdigit() for ch in LABEL_ALLOWED.sub("", text))]
    assert not bad_labels, f"structural labels carrying other numbers: {bad_labels[:10]}"
    decimals = [text for text in scan.meta if re.search(r"\d+\.\d+", text)]
    assert not decimals, f"chart titles or descriptions typing a decimal value: {decimals[:5]}"


def test_negative_control_an_unbound_page_numeral_is_caught(page):
    doctored = page.replace('<h2 id="v3-h">', '<h2 id="v3-h">7.8% better ', 1)
    assert "7.8%" in research_scan(doctored).unbound


def test_every_page_claim_is_in_the_layer_and_a_map(page):
    used = set(re.findall(r'data-claim="([^"]+)"', page))
    assert used, "the page renders no claim"
    assert not used - RC.all_claim_ids(), sorted(used - RC.all_claim_ids())
    assert not used - RC.claim_map_ids(), sorted(used - RC.claim_map_ids())


def test_every_page_record_and_v1_key_resolves(page):
    for record_id in set(re.findall(r'data-record="([^"]+)"', page)):
        R.get(record_id)
    claims = build_claims()
    for key in set(re.findall(r'data-v1="([^"]+)"', page)):
        assert key in claims.values, key
    for pointer in set(re.findall(r'data-release-check="([^"]+)"', page)):
        path, _, field = pointer.partition("#")
        record = json.loads((REPO_ROOT / path).read_text())
        if field == "seconds_to_visible_forecast":
            assert any(run.get(field) for run in record["runs"])
        else:
            assert field in record, pointer


def test_every_published_page_block_is_rendered(page):
    missing = [block.key for block in RC.BLOCKS if RC.PAGE in block.surfaces and f'data-block="{block.key}"' not in page]
    assert not missing, missing


def test_the_page_carries_no_withheld_or_stale_phrasing(page):
    research = " ".join(TAG.sub(" ", chunk) for chunk in re.findall(
        r'data-research="[^"]+".*?(?=<details class="disclosure archive"|</article>|</section>)', page, re.DOTALL))
    assert not RC.withheld_findings(research), RC.withheld_findings(research)
    text = TAG.sub(" ", page)
    assert not RC.stale_findings(text), RC.stale_findings(text)


@pytest.mark.parametrize("surface", ["README.md", "space/README.md", "space-wasm/README.md"])
def test_no_surface_carries_stale_status_text(surface):
    assert not RC.stale_findings((REPO_ROOT / surface).read_text()), surface


def test_the_browser_claim_file_is_current_when_present():
    path = REPO_ROOT / "app" / "public" / "claims.json"
    if not path.exists():
        pytest.skip("app/public/ is built by `make wasm-payload`")
    assert json.loads(path.read_text()) == dict(build_claims().values)


def test_placeholder_guard_on_the_final_build(page):
    """Invariant 16: the final build fails while a marker for an unpublished link remains."""
    record = json.loads((REPO_ROOT / "reports/cp3/pages_build.json").read_text())
    if record.get("final"):
        assert not B.unpublished_markers(page)
    with pytest.raises(B.PlaceholderError):
        B.refuse_unpublished('<span data-unpublished="mlflow:cp20">x</span>')
    B.refuse_unpublished("<p>no placeholder</p>")


def test_unit_guard_refuses_two_units_on_one_axis():
    with pytest.raises(B.UnitMixError):
        B.axis_unit(["cp20.metrics.HG.equal_fold.S_MAE", "cp20.metrics.HG.pooled.MAE"])
    assert B.axis_unit(["cp20.metrics.HG.fold_1.MAE", "cp20.metrics.H0.fold_1.MAE"]) == R.UNIT_EUR


def test_negative_control_a_mixed_unit_chart_raises():
    panel = B.Panel("mixed", "", (B.Row("a", "cp20.metrics.HG.equal_fold.S_MAE", "v3"),
                                  B.Row("b", "cp20.metrics.HG.pooled.MAE", "v3")), (0, 1), 0.1)
    with pytest.raises(B.UnitMixError):
        B.single_rows("mixed", "P07", [panel], title="t", desc="d")
