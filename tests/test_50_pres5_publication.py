"""PRES-5: the publication of the research since v5, with A1, the final candidate, in v5's comparison.

The contracts, each with a negative control where a check could pass vacuously:

- A1's rows on v5's population re-derive from the committed inputs, cover every key, and pair with v5's and the naive's
  scores that equal CP-24's committed rows exactly (the brief's outcome 1: never recomputed for publication);
- the registry holds one final candidate, its status O13's, first in the comparison, with codes scoped by experiment;
- every derived change follows from its committed record; CP-26's and CP-28's records stay on development days;
- the page and the README carry the final candidate's headline (decision 20), the A1 chapter, CP-26's every-day panel
  beside the five periods, the freeze and 4.7T's registered terms, and v1 under the Space's History;
- the archive's figures are the originals' exact pixels, and the page fits the 2.0 MB budget;
- the CP-26 and CP-28 exports mirror their drafts, add runs only, and leave every published run unchanged.
"""
from __future__ import annotations

import html
import io
import json
import re
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

import numpy as np
import pytest

from delu_forecast import compact_figures as CF
from delu_forecast import derived as D
from delu_forecast import final_candidate as FC
from delu_forecast import registry as G
from delu_forecast import research as R
from delu_forecast import research_claims as RC

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_pages  # noqa: E402
import mlflow_export as E  # noqa: E402

PAGE = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
README = (ROOT / "README.md").read_text(encoding="utf-8")


def _text(fragment: str) -> str:
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", fragment)))


# --------------------------------------------------------------------------- A1 on v5's population (outcome 1)


@pytest.fixture(scope="module")
def built() -> dict[str, str]:
    return FC.build(ROOT)


def test_a1_rows_rederive_byte_for_byte(built):
    for name, text in built.items():
        assert (ROOT / FC.OUT / name).read_text() == text, name


def test_a1_covers_every_key_of_v5s_population():
    summary = json.loads((ROOT / FC.OUT / "summary.json").read_text())
    assert summary["coverage"]["covered_keys"] == summary["coverage"]["keys"] == 10747
    assert summary["coverage"]["days"] == 448
    assert {fold: pair[0] == pair[1] for fold, pair in summary["coverage"]["per_fold"].items()} == {
        f"fold_{i}": True for i in range(1, 6)}
    assert summary["coverage"]["output_source"] == {"native": 448} and summary["coverage"]["fallback_days"] == 0
    # the first period lies in CP-26's unscored warm-up, and the chapter says so
    assert summary["coverage"]["scored_by_cp26_cp28"] == {"False": 90, "True": 358}
    assert [item["item"] for item in summary["information_set"]] == [
        "issue time", "fitting", "network search", "data identity and inputs", "the first period", "selection"]


def test_v5_and_the_naive_are_not_recomputed_for_publication():
    parity = json.loads((ROOT / FC.OUT / "parity.json").read_text())
    assert parity["equal"] is True and parity["max_abs_difference"] == 0.0
    # The page's v5 and naive rows are CP-24's records, never PRES-5's.
    assert G.comparison_source(G.get("v5")) == "CP-24" and G.comparison_source(G.get("naive")) == "CP-24"
    rows = (ROOT / FC.OUT / "metrics.csv").read_text().splitlines()[1:]
    assert rows and all(row.startswith("A1,") for row in rows)


def test_the_draws_are_cp24s_shared_index_set():
    summary = json.loads((ROOT / FC.OUT / "summary.json").read_text())
    assert summary["bootstrap"]["index_equals_cp20"] is True
    assert (summary["bootstrap"]["seed"], summary["bootstrap"]["replicates"], summary["bootstrap"]["block_days"]) == (
        15042, 2000, 7)


def test_a_missing_a1_key_is_refused(monkeypatch):
    real = FC.a1_rows

    def short(root, v5):
        out, coverage = real(root, v5)
        coverage = dict(coverage, covered_keys=coverage["keys"] - 1)
        return out, coverage

    monkeypatch.setattr(FC, "a1_rows", short)
    with pytest.raises(ValueError, match="cover"):
        FC.score(ROOT)


def test_a_changed_input_is_refused(monkeypatch):
    monkeypatch.setitem(FC.INPUTS, "reports/cp28/forecast/manifest.json", "0" * 64)
    with pytest.raises(ValueError, match="SHA-256"):
        FC._inputs(ROOT)


# --------------------------------------------------------------------------- the registry (outcome 6)


def test_one_final_candidate_with_o13s_status():
    final = G.final_candidate()
    assert final is not None and final.id == "a1" and final.name == "A1 · DDNN-2 alone"
    assert final.status.status == G.FINAL_CANDIDATE and final.status.date == "2026-10-30"
    assert final.version is None  # selected, never adopted: no version number (W49)
    assert G.released().id == "v1" and G.current_generation().id == "v5"  # decision 21
    assert G.comparison_rows()[0] is final


def test_codes_are_scoped_and_an_unscoped_a1_is_refused():
    assert G.by_code("A1", "CP-28").id == "a1" and G.by_code("A1", "PRES-5").id == "a1"
    assert G.by_code("A1", "CP-15").id == "normalized-lear"
    with pytest.raises(G.RegistryError, match="name the experiment"):
        G.by_code("A1")
    assert G.by_code("nominal/D2/all_eligible", "CP-26").id == "a1"


def test_cp28_is_a_branch_whose_six_other_arms_were_not_selected():
    branch = G.get("recombining-v5s-members")
    assert branch.kind == "branch" and branch.after == "v5" and branch.informed == "a1"
    arms = [G.by_code(code, "CP-28") for code in ("A2", "A3", "A4", "A5", "A6", "A7")]
    assert {arm.kind for arm in arms} == {"study arm"} and {arm.status.status for arm in arms} == {G.NOT_ADOPTED}
    assert G.CHECKPOINTS["CP-28"].owner == branch.id


def test_the_overview_route_lists_only_runs_mlflow_holds():
    kind, runs = G.expected_routes()["compare:overview"]
    assert len(runs) == len(G.comparison_rows()) - 1 and "cp28/A1" not in runs
    assert G.expected_routes()["compare:recombining-v5s-members"][1] == tuple(f"cp28/A{i}" for i in range(1, 8))


# --------------------------------------------------------------------------- records and the red line


def test_every_new_record_rederives():
    pres5 = [record for record_id, record in R.records().items() if record_id.startswith(("pres5.", "cp26.", "cp28."))]
    assert len(pres5) > 600
    assert R.validate_all(pres5) == []
    assert D.validate_all() == []


def test_a_perturbed_cp28_value_fails_to_rederive():
    record = R.get("cp28.arm.A1.WIS.ratio_to_control")
    bad = R.EvidenceRecord(**{**record.__dict__, "raw": "0.95"})
    assert any("committed value" in problem for problem in R.validate_all([bad]))


def test_research_numbers_use_development_days_only():
    """§24.14 P1: no record the publication adds describes a delivery day after 2026-09-06."""
    for record_id, record in R.records().items():
        if record.window is not None:
            assert record.window[1] <= R.RESEARCH_BOUNDARY, record_id
    bound = set(re.findall(r'data-record="([^"]+)"', PAGE))
    assert any(record_id.startswith("cp26.") for record_id in bound)
    for record_id in bound:
        if not D.is_derived(record_id) and record_id in R.records():
            window = R.get(record_id).window
            assert window is None or window[1] <= R.RESEARCH_BOUNDARY, record_id


def test_the_derived_changes_follow_from_their_records():
    ratio = Decimal(R.get("pres5.ratio.A1-v5.WIS").raw)
    assert Decimal(D.get("derived.change.a1.S_WIS").value) == ratio * 100
    control = Decimal(R.get("cp28.arm.A1.MAE.ratio_to_control").raw)
    assert Decimal(D.get("derived.cp28.A1.MAE").value) == (control - 1) * 100
    assert D.get("derived.cp28.tested").value == "7"
    assert D.display(D.get("derived.cp26.v5-v4.MAE"), "ci_high") == "+1%"  # a span across zero shows its sign


# --------------------------------------------------------------------------- the surfaces (outcomes 1-5)


def test_the_headline_is_the_final_candidates_development_result():
    claim, template = RC.headline_template()
    assert claim == "P60" and "{r:derived.cp28.A1.MAE}" in template and "{r:derived.cp28.tested}" in template
    text = RC.headline("md")
    assert "in point error" in text and "in interval error" in text  # A1: each metric named beside its value
    assert text.endswith("`Development · post-selection`")
    assert RC.headline_terms()[:3] == ("terms.daily_errors", "terms.selection_rule", "terms.final_candidate")


def test_the_opening_pairs_the_final_candidate_with_the_live_product():
    opening = PAGE[PAGE.index('id="top"'):PAGE.index('id="product"')]
    text = _text(opening)
    assert "Live product A1 · DDNN-2 alone" in text and "Final candidate · pending 4.7T A1 · DDNN-2 alone" in text
    assert "prospective evaluation in progress" in text and "Open the live product" in text
    assert "/history/" in opening  # v1's demo, historical (O17)
    assert "Try the v1 demo</span>" not in opening


def test_the_comparison_draws_a1_first_from_its_own_rows():
    results = PAGE[PAGE.index('id="research-results"'):PAGE.index('id="journey"')]
    assert 'data-record="pres5.metrics.A1.equal_fold.S_MAE"' in results
    assert "13 policies" in _text(results)
    assert "comparison.finding.a1" in results


def test_cp26_is_shown_beside_the_five_periods_and_never_pooled():
    panel = PAGE[PAGE.index('id="everyday"'):]
    panel = panel[:panel.index("</figure>")]
    text = _text(panel)
    assert "never pooled with the five periods above" in text
    assert "2,068 eligible days" in text and "development, post-selection" in text
    assert 'data-record="derived.cp26.v5-v4.MAE"' in panel


def test_the_final_candidates_chapter_fills_the_grammar_and_states_its_terms():
    assert build_pages.slot_problems(build_pages.a1_slots()) == []
    chapter = PAGE[PAGE.index('id="final-candidate"'):]
    text = _text(chapter[:chapter.index("</article>")])
    for phrase in ("2026-09-07 to 2026-12-05", "opening no earlier than 2026-12-04", "at most 0.05",
                   "At least 60 of the 90 days", "No runner-up moves up", "It passed the pre-registered test",
                   "It did not pass; the window is spent, and v1 remains the product.", "720fc581",
                   "The comparison shares the hours and prices, not the protocol.", "A description, not a decision"):
        assert phrase in text, phrase


def test_the_registered_terms_are_the_protocols():
    protocol = (ROOT / "docs/track-b/evidence/cp-17/4-7t-frozen-protocol.md").read_text()
    for fragment in ("2026-09-07 to 2026-12-05", "no earlier than 2026-12-04", "**7-day blocks;**",
                     "**10,000 replicates;**", "**at least 60 of the 90 dates paired and scored**",
                     "**No runner-up moves up.**", "α = 0.05"):
        assert fragment in protocol, fragment
    decisions = (ROOT / "docs/track-b/owner-decisions-2026-10-29.md").read_text()
    assert '"It passed the pre-registered test (compound p ≤ 0.05)."' in decisions
    assert "the window is spent, and v1 remains the" in decisions


def test_the_report_shows_no_live_number():
    """The brief's outcome 5: the report shows no live forecast, score or price, and no number after 2026-09-06."""
    for value in re.findall(r'data-record="([^"]+)"', PAGE):
        assert not value.startswith("live"), value
    assert "live/" not in re.sub(r'https://[^"]+', "", PAGE.split("<script>")[0])


def test_the_planned_list_is_brought_up_to_date():
    names = [name for name, *_ in build_pages.PLANNED_WORK]
    assert names[:2] == ["The one-shot test of A1, from 2026-12-04", "The live trial: prospective evaluation in progress"]
    assert "A re-evaluation on every eligible day" not in names and "Combining models" not in names


def test_the_readme_carries_the_same_claims():
    assert "**Final candidate · pending 4.7T, A1 · DDNN-2 alone.**" in README
    assert RC.headline("md") in README
    assert "### A1 · DDNN-2 alone · final candidate, pending 4.7T" in README
    assert "#### Recombination of v5's members" in README
    assert "history/" in README


# --------------------------------------------------------------------------- the budget, without loss


def test_the_archive_figures_are_the_originals_pixels():
    assert CF.check() == []
    for key, original in build_pages.ARCHIVE_FIGURES.items():
        embedded = build_pages.ARCHIVE_FIGURES_EMBEDDED[key]
        assert Path(embedded).name == Path(original).name and embedded.startswith("reports/pres5/compact-figures/")


def test_a_changed_pixel_is_caught(tmp_path, monkeypatch):
    from PIL import Image

    for original in CF.ORIGINALS:
        target = tmp_path / original
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / original).read_bytes())
        copy = tmp_path / CF.copy_path(original)
        copy.parent.mkdir(parents=True, exist_ok=True)
        copy.write_bytes((ROOT / CF.copy_path(original)).read_bytes())
    first = tmp_path / CF.copy_path(CF.ORIGINALS[0])
    pixels = np.asarray(Image.open(first).convert("RGB")).copy()
    pixels[0, 0] = (pixels[0, 0] + 1) % 256
    buffer = io.BytesIO()
    Image.fromarray(pixels, "RGB").save(buffer, "PNG")
    first.write_bytes(buffer.getvalue())
    assert any("pixels differ" in problem for problem in CF.check(tmp_path))


def test_the_page_fits_the_budget():
    assert len(PAGE.encode("utf-8")) <= 2_000_000


# --------------------------------------------------------------------------- MLflow (outcome 7)


def test_the_cp26_and_cp28_exports_mirror_their_drafts():
    assert E.pres5_draft_problems() == []
    cp26 = json.loads((ROOT / "reports/presentation/mlflow-export/cp26.json").read_text())
    cp28 = json.loads((ROOT / "reports/presentation/mlflow-export/cp28.json").read_text())
    assert len(cp26["runs"]) == 53 and len(cp28["runs"]) == 8
    assert {run["run_name"] for run in cp28["runs"] if run["run_key"] == "cp28/A1"} == {"A1 · DDNN-2 alone (A1, selected)"}


def test_no_published_run_changes():
    for name in ("cp10", "cp15", "cp16", "cp20", "cp21", "cp22", "cp23", "cp24"):
        published = subprocess.run(["git", "show", f"evidence/pres-4:reports/presentation/mlflow-export/{name}.json"],
                                   cwd=ROOT, capture_output=True, text=True)
        if published.returncode != 0:
            pytest.skip("the published export is not reachable in this checkout")
        assert (ROOT / f"reports/presentation/mlflow-export/{name}.json").read_text() == published.stdout, name
    note = E.EXPERIMENT_TAGS["mlflow.note.content"]
    assert "(CP-26)" in note and "(CP-28)" in note  # the one authorized experiment-description write


def test_the_withheld_claims_are_guarded():
    assert RC.withheld_findings("A1 was adopted in research as v6")
    assert RC.withheld_findings("A1 is live")
    assert RC.withheld_findings("the same protocol as v5")
    assert not RC.withheld_findings("The live product runs A1, the final candidate; never pooled with the five periods.")
    assert not RC.withheld_findings(_text(PAGE.split("<script>")[0]))
