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
    for key, surface in (("v2.interpretation", RC.PAGE), ("v2.result.hp", RC.README)):
        html = RC.render(key, surface=surface)
        assert "+0.000003857628092332211" in html, key
        assert "0.0000]" not in html and "0.0000<" not in html, key
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
        ("v3 cuts the error 46% relative to v1.", "W20"),
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


@pytest.mark.parametrize("surface", ["README.md", "space/README.md", "space-wasm/README.md", "app/wasm_showcase.py",
                                     "scripts/build_wasm_space.py"])
def test_no_active_surface_makes_an_absolute_network_claim(surface):
    """Final audit F07: no "fetches nothing", "no server" or "instant report" outside v1's archive."""
    assert not RC.network_absolute_findings((REPO_ROOT / surface).read_text()), surface


def test_the_page_makes_no_absolute_network_claim_outside_the_archive(page):
    before, archive = page.split('<details class="disclosure archive"', 1)
    after = archive.split("</details>", 1)[1] if "</details>" in archive else ""
    assert not RC.network_absolute_findings(TAG.sub(" ", before + after))


def test_negative_control_absolute_network_claims_are_caught():
    assert RC.network_absolute_findings("The static report fetches nothing at all.")
    assert RC.network_absolute_findings("runs in your browser, no server; the first visit")
    assert RC.network_absolute_findings("Read the instant report instead")


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


# -- invariant 17: no generator types a research number (plan §9.1) ---------------------------------

import ast  # noqa: E402

GENERATORS = (REPO_ROOT / "scripts" / "build_pages.py", REPO_ROOT / "scripts" / "mlflow_export.py")
#: v1's archived report is preserved as published (invariant 24); its figures come from v1's claims.
PRESERVED_FUNCTIONS = {"build_pages.py": {"v1_archive"}}
_NUMERAL = re.compile(r"[−-]?\d[\d,]*(?:\.\d+)?(?:/\d[\d,]*)?")
_COUNT_NOUN = re.compile(r"^\s*(?:\w+\s+){0,2}?(days|hours|policies|runs|replicates|hits|folds|windows)\b")


def _research_tokens():
    recs = R.records()
    records = recs.values() if isinstance(recs, dict) else [R.get(record_id) for record_id in recs]
    decimals, counts = set(), set()
    for record in records:
        for which in ("value", "ci_low", "ci_high"):
            try:
                shown = R.display(record, which).replace("−", "-").lstrip("+-")
            except Exception:
                continue
            if "." in shown and len(shown.split(".")[1]) >= 2 and sum(c.isdigit() for c in shown) >= 4:
                decimals.add(shown)
        try:
            number = float(record.value)
        except (TypeError, ValueError):
            continue
        if number.is_integer() and number >= 100:
            counts.add(int(number))
    return decimals, counts


def typed_research_numbers(source: str, name: str, tokens) -> list[str]:
    """Numerals in a generator's string literals that reproduce a research value by hand."""
    decimals, counts = tokens
    tree = ast.parse(source)
    skip = [(node.lineno, node.end_lineno) for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef) and node.name in PRESERVED_FUNCTIONS.get(name, set())]
    found = []
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        if any(start <= node.lineno <= end for start, end in skip):
            continue
        text = node.value
        for match in _NUMERAL.finditer(text):
            token = match.group(0).replace("−", "-").lstrip("-").rstrip(",")
            if "/" in token:  # a hit ratio such as 79/408
                parts = [part.replace(",", "") for part in token.split("/")]
                if all(part.isdigit() for part in parts) and int(parts[1]) in counts and int(parts[1]) >= 100:
                    found.append(f"{name}:{node.lineno} ratio {match.group(0)}")
                continue
            if "." in token:
                if token in decimals:
                    found.append(f"{name}:{node.lineno} value {match.group(0)}")
                continue
            digits = token.replace(",", "")
            if not digits.isdigit():
                continue
            number = int(digits)
            if "," in token and number in counts:
                found.append(f"{name}:{node.lineno} count {match.group(0)}")
            elif (number in counts and not 1900 <= number <= 2099
                  and _COUNT_NOUN.match(text[match.end():])):
                found.append(f"{name}:{node.lineno} count {match.group(0)}")
    return found


@pytest.fixture(scope="module")
def research_tokens():
    return _research_tokens()


def test_no_generator_types_a_research_number(research_tokens):
    for path in GENERATORS:
        found = typed_research_numbers(path.read_text(), path.name, research_tokens)
        assert not found, found


def test_negative_control_typed_research_numbers_are_caught(research_tokens):
    source = (
        'NOTE = "compared nine policies on the same 10,747 development hours"\n'
        'CP10 = "crisis-window coverage rose from 79/408 to 131/408"\n'
        'STEP = "step = day index within the 448 represented development days"\n'
        'SHEET = "<p>−0.0783 headline value</p>"\n'
        'FINE = f"{n} hours, 2026-09-24, line-height 1.08, fill-opacity 0.18"\n'
    )
    found = typed_research_numbers(source, "fixture.py", research_tokens)
    assert any("10,747" in item for item in found)
    assert any("79/408" in item for item in found) and any("131/408" in item for item in found)
    assert any("448" in item for item in found)
    assert any("0.0783" in item for item in found)
    assert not any(":5 " in item for item in found), found


def test_the_readme_labels_differences_as_differences():
    """Final audit F01: −0.0783 is v3 − v2, not a negative score, and the README has no chart to point at."""
    block = README.read_text().split("<!-- research:start -->", 1)[1].split("<!-- research:end -->", 1)[0]
    assert "(v3 − v2)" in block and "Negative values favour v3" in block
    assert "Point-error difference:" in block and "Interval-score difference:" in block
    assert "Normalized point error −" not in block and "Normalized interval score −" not in block
    assert "shown in the chart" not in block
    assert "scores 1.0518 here" not in block
