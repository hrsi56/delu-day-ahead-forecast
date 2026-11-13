"""PRES-5: the publication of the research since v5, with v6 (A1 in the frozen records), the final candidate, in v5's
comparison.

The contracts, each with a negative control where a check could pass vacuously:

- v6's rows on v5's population re-derive from the committed inputs, cover every key, and pair with v5's and the naive's
  scores that equal CP-24's committed rows exactly (the brief's outcome 1: never recomputed for publication);
- the registry holds one final candidate, v6 (ruling O30), its status O13's, first in the comparison, with codes scoped by
  experiment, and CP-28's six other arms as study arms, not selected;
- every derived change follows from its committed record; CP-26's and CP-28's records stay on development days;
- the page and the README carry the final candidate's headline (decision 20), v6's chapter, CP-26's every-day panel
  beside the five periods, the freeze and 4.7T's registered terms, and v1 under the Space's History;
- the archive's figures are the originals' exact pixels (ruling O25), and the page fits the 2.0 MB budget;
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
    assert final is not None and final.id == "v6" and final.name == "v6 · DDNN-2 alone"  # ruling O30
    assert final.kind == "generation" and final.version == "v6" and final.predecessor == "v5"
    assert final.status.status == G.FINAL_CANDIDATE and final.status.date == "2026-10-30"
    assert G.released().id == "v1"  # the last released generation (ruling O27)
    assert G.current_generation() is final and G.comparison_rows()[0] is final
    assert G.FROZEN_LABELS == {"v6": "A1"}


def test_codes_are_scoped_and_an_unscoped_a1_is_refused():
    assert G.by_code("A1", "CP-28").id == "v6" and G.by_code("A1", "PRES-5").id == "v6"
    assert G.by_code("A1", "CP-15").id == "normalized-lear"
    with pytest.raises(G.RegistryError, match="name the experiment"):
        G.by_code("A1")
    assert G.by_code("nominal/D2/all_eligible", "CP-26").id == "v6"


def test_cp28s_six_other_arms_are_study_arms_not_selected():
    arms = [G.by_code(code, "CP-28") for code in ("A2", "A3", "A4", "A5", "A6", "A7")]
    assert {arm.kind for arm in arms} == {"study arm"} and {arm.status.status for arm in arms} == {G.NOT_ADOPTED}
    assert G.CHECKPOINTS["CP-28"].owner == "v6"
    assert not [entry for entry in G.entries() if entry.kind == "branch" and entry.after == "v5"]
    # On the page they are named without their codes, each marked "Not selected" (ruling O30).
    table = PAGE[PAGE.index("Seven arms against"):]
    table = _text(table[:table.index("</table>")])
    assert table.count("Not selected") == 6 and table.count("Selected") == 1
    assert not re.search(r"\bA[2-7]\b", table)


def test_the_overview_route_lists_only_runs_mlflow_holds():
    kind, runs = G.expected_routes()["compare:overview"]
    assert len(runs) == len(G.comparison_rows()) - 1 and "cp28/A1" not in runs
    assert "cp28/A1" in G.expected_routes()["compare:v6"][1]


# --------------------------------------------------------------------------- records and the red line


def test_every_new_record_rederives():
    pres5 = [record for record_id, record in R.records().items() if record_id.startswith(("pres5.", "cp26.", "cp28."))]
    assert len(pres5) > 500
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
    assert Decimal(D.get("derived.change.v6.S_WIS").value) == ratio * 100
    control = Decimal(R.get("cp28.arm.A1.MAE.ratio_to_control").raw)
    assert Decimal(D.get("derived.cp28.A1.MAE").value) == (control - 1) * 100
    assert D.get("derived.cp28.tested").value == "7"
    assert D.display(D.get("derived.cp26.v5-v4.MAE"), "ci_high") == "+1%"  # a span across zero shows its sign


# --------------------------------------------------------------------------- the surfaces (outcomes 1-5)


def test_the_headline_is_the_final_candidates_development_result():
    claim, template = RC.headline_template()
    assert claim == "P60" and "{r:derived.cp28.A1.MAE}" in template and "{r:derived.cp28.tested}" in template
    text = RC.headline("md")
    assert "in point error" in text and "in interval error" in text  # each metric named beside its value
    assert text.endswith("`Development · post-selection`")
    assert RC.headline_terms()[:3] == ("terms.daily_errors", "terms.selection_rule", "terms.final_candidate")


def test_the_opening_pairs_the_final_candidate_with_the_live_product():
    opening = PAGE[PAGE.index('id="top"'):PAGE.index('id="product"')]
    text = _text(opening)
    assert "Live product v6 · DDNN-2 alone" in text and "Final candidate · pending 4.7T v6 · DDNN-2 alone" in text
    assert "prospective evaluation in progress" in text and "Open the live product" in text
    assert "/history/" in opening  # v1's demo, historical (O17)
    assert "Try the v1 demo</span>" not in opening


def test_the_comparison_draws_v6_first_from_its_own_rows():
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
    chapter = PAGE[re.search(r'<article[^>]*id="v6"', PAGE).start():]
    text = _text(chapter[:chapter.index("</article>")])
    for phrase in ("2026-09-07 to 2026-12-05", "opening no earlier than 2026-12-04", "at most 0.05",
                   "At least 60 of the 90 days", "No runner-up moves up", "It passed the pre-registered test",
                   "the window is spent", "720fc581", "A1 in the frozen records",
                   "The comparison shares the hours and prices, not the protocol.", "A description, not a decision"):
        assert phrase in text, phrase
    # The chapter's headings use the public name; the frozen label appears only where the identity is shown (O30).
    assert "How v6 was selected" in text and "How A1" not in text


def test_the_registered_terms_are_the_protocols():
    protocol = " ".join((ROOT / "docs/track-b/evidence/cp-17/4-7t-frozen-protocol.md").read_text().split())
    for fragment in ("2026-09-07 to 2026-12-05", "no earlier than 2026-12-04", "**7-day blocks;**",
                     "**10,000 replicates;**", "**at least 60 of the 90 dates paired and scored**",
                     "**No runner-up moves up.**", "α = 0.05"):
        assert fragment in protocol, fragment
    decisions = " ".join((ROOT / "docs/track-b/owner-decisions-2026-10-29.md").read_text().split())
    assert '"It passed the pre-registered test (compound p ≤ 0.05)."' in decisions
    assert "the window is spent, and v1 remains the" in decisions


def test_the_report_shows_no_live_number():
    """The brief's outcome 5: the report shows no live forecast, score or price, and no number after 2026-09-06."""
    for value in re.findall(r'data-record="([^"]+)"', PAGE):
        assert not value.startswith("live"), value
    assert "live/" not in re.sub(r'https://[^"]+', "", PAGE.split("<script>")[0])


def test_the_planned_list_is_brought_up_to_date():
    names = [name for name, *_ in build_pages.PLANNED_WORK]
    assert names[:2] == ["The one-shot test of v6, from 2026-12-04", "The live trial: prospective evaluation in progress"]
    assert "A re-evaluation on every eligible day" not in names and "Combining models" not in names


def test_the_readme_carries_the_same_claims():
    assert "**Final candidate · pending 4.7T, v6 · DDNN-2 alone.**" in README
    assert RC.headline("md") in README
    assert "### v6 · DDNN-2 alone" in README and "A1 in the frozen records" in README
    assert "Recombination of v5's members" not in README
    assert "history/" in README


def test_v1s_demo_is_linked_by_its_file_never_the_bare_history_route():
    """O44: the Space's static host redirects the bare `/history/` to huggingface.co/history, an unrelated profile
    (CP-18c found it on the Space on 2026-11-13). The report and the README link `history/index.html`."""
    for surface in (PAGE, README):
        assert "hf.space/history/index.html" in surface
        assert not re.search(r"hf\.space/history/(?!index\.html)", surface)
        assert not re.search(r"hf\.space/history(?![/\w])", surface)


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
    pixels[0, 0] = (pixels[0, 0].astype(np.int16) + 1) % 256
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
    assert {run["run_name"] for run in cp28["runs"] if run["run_key"] == "cp28/A1"} == {"v6 · DDNN-2 alone (A1, selected)"}


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
    assert RC.withheld_findings("v6 was adopted")
    assert RC.withheld_findings("A1 is live")
    assert RC.withheld_findings("the same protocol as v5")
    assert not RC.withheld_findings("The live product runs v6, the final candidate; never pooled with the five periods.")
    # PRES-5's guards (W49-W53) find nothing on the page or in the README; the older guards keep their own tests.
    for surface in (_text(PAGE.split("<script>")[0]), README):
        assert not [hit for hit in RC.withheld_findings(surface) if hit.split(":")[0] in ("W49", "W50", "W51", "W52", "W53")]


# --------------------------------------------------------------------------- CP-26's landed code (ruling O34)


def _landed_record_copy(tmp_path: Path) -> Path:
    import shutil

    import pres5_landed_code as L

    copy = tmp_path / "record"
    shutil.copytree(ROOT / L.RECORD, copy)
    return copy


def test_cp26s_log_equals_the_recorded_landed_bytes_and_the_new_modules_are_outside_it():
    import pres5_landed_code as L

    log = json.loads((ROOT / "reports/rebaseline/harness-log.json").read_text())["landed_code"]
    assert log == L.landed_code(ROOT)
    record = json.loads((ROOT / L.RECORD / "manifest.json").read_text())
    assert {name: entry["sha256"] for name, entry in record["files"].items()} == {
        name: log[name] for name in record["files"]}
    for added in ("src/delu_forecast/final_candidate.py", "src/delu_forecast/compact_figures.py"):
        assert added in record["added_by_pres5"] and added not in log and (ROOT / added).exists()


def test_a_changed_recorded_copy_fails(tmp_path, monkeypatch):
    import pres5_landed_code as L

    copy = _landed_record_copy(tmp_path)
    target = copy / "registry.py.txt"
    target.write_bytes(target.read_bytes() + b"\n# changed\n")
    monkeypatch.setattr(L, "RECORD", copy)  # an absolute path: `root / RECORD` is the copy
    with pytest.raises(AssertionError):
        L.landed_code(ROOT)


def test_a_recorded_copy_that_no_longer_matches_the_log_fails(tmp_path, monkeypatch):
    """A copy changed together with its own hash and blob passes its own check, and then differs from CP-26's log."""
    import hashlib

    import pres5_landed_code as L

    copy = _landed_record_copy(tmp_path)
    raw = (copy / "research.py.txt").read_bytes() + b"\n# changed\n"
    (copy / "research.py.txt").write_bytes(raw)
    manifest = json.loads((copy / "manifest.json").read_text())
    manifest["files"]["src/delu_forecast/research.py"].update(
        bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(),
        git_blob=hashlib.sha1(b"blob %d\0" % len(raw) + raw).hexdigest())
    (copy / "manifest.json").write_text(json.dumps(manifest))
    monkeypatch.setattr(L, "RECORD", copy)
    log = json.loads((ROOT / "reports/rebaseline/harness-log.json").read_text())["landed_code"]
    assert L.landed_code(ROOT) != log


def test_any_other_landed_file_is_still_compared_with_the_working_tree(tmp_path, monkeypatch):
    import shutil

    import pres5_landed_code as L

    tree = tmp_path / "tree"
    for base in L.H.LANDED_CODE:
        shutil.copytree(ROOT / base, tree / base, ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(ROOT / L.RECORD, tree / L.RECORD)
    log = json.loads((ROOT / "reports/rebaseline/harness-log.json").read_text())["landed_code"]
    assert L.landed_code(tree) == log
    other = tree / "src/delu_forecast/claims.py"
    other.write_bytes(other.read_bytes() + b"\n# changed\n")
    assert L.landed_code(tree) != log


def test_the_evidence_tags_date_is_the_tips():
    """The page labels v6's raw rows "frozen <date>" from the registry; that date is the evidence tip's (Integration
    review 1, F3). Before the tag exists, it is no earlier than the last commit of the rows it labels."""
    date = G.EVIDENCE_TAGS["evidence/pres-5"][1]
    tagged = subprocess.run(["git", "log", "-1", "--format=%cs", "evidence/pres-5"], cwd=ROOT, capture_output=True,
                            text=True)
    if tagged.returncode == 0 and tagged.stdout.strip():
        assert date == tagged.stdout.strip()
        return
    shallow = subprocess.run(["git", "rev-parse", "--is-shallow-repository"], cwd=ROOT, capture_output=True, text=True)
    rows = subprocess.run(["git", "log", "-1", "--format=%cs", "--", "reports/pres5/a1-in-v5"], cwd=ROOT,
                          capture_output=True, text=True)
    commits = subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=ROOT, capture_output=True, text=True)
    if shallow.stdout.strip() != "false" or rows.returncode != 0 or not rows.stdout.strip():
        pytest.skip("no history here to date the rows (a depth-1 checkout)")
    if commits.stdout.strip() == "1":
        # a history-free single-commit copy (the Orchestrator's CI reproduction): its one commit is dated the day the
        # copy was made, not the day the rows were committed, so it cannot date them either
        pytest.skip("no history here to date the rows (a history-free single-commit copy)")
    assert date >= rows.stdout.strip()


# --------------------------------------------------------------------------- what the Space runs (review 2, G1)

#: A sentence saying the Space, its root or its app runs v1 or v1's champion now (PUBLISH_RULES §8; the brief's
#: outcome 5; rulings O26, O27, O29; Integration review 2, G1).
SPACE_RUNS_V1_NOW = (
    re.compile(r"\bThe Space (cannot|can't|can not) load\b"),
    re.compile(r"\bThe app alone is at\b"),
    re.compile(r"\b[Tt]he Space\b[^.]{0,80}\bruns\b[^.]{0,60}\b(champion|v1|released model)\b"),
    re.compile(r"\b[Tt]he (demo|Space's root|app) runs\b[^.]{0,40}\b(champion|v1|released model)\b"),
)


def _space_runs_v1_now(text: str) -> list[str]:
    flat = " ".join(text.split())
    return [match.group(0) for pattern in SPACE_RUNS_V1_NOW for match in pattern.finditer(flat)]


def test_no_surface_says_the_space_runs_v1_now():
    page = PAGE.split("<script>")[0]
    # v1's archive is preserved as published and labelled so; a note outside it says where v1's demo is now.
    archive = re.search(r'<details class="disclosure archive" id="v1-archive">.*?</details>\s*</article>', page, re.S)
    assert archive
    assert not _space_runs_v1_now(_text(page.replace(archive.group(0), "")))
    assert not _space_runs_v1_now(README)
    assert "the Space could not load" in " ".join(README.split())  # v1's demo, dated to its release


def test_negative_control_the_readme_sentence_before_the_repair_is_caught():
    from delu_forecast.claims import build_claims

    claims = build_claims()
    restored = README.replace(
        README[README.index("At v1's release, the Space could not load"):README.index("\n", README.index(
            "At v1's release, the Space could not load"))],
        f'{claims["wasm_identity"]} {claims["wasm_wrapper_disclosure"]}')
    assert len(_space_runs_v1_now(restored)) >= 2  # "The Space cannot load …" and "The app alone is at …"


def test_negative_controls_for_w51_and_w52():
    """PRES-5's guards on pooling CP-26's every-day results with the five periods (W51) and on the live record as
    4.7T's result (W52) catch their sentences, and leave the page's own wording alone (Integration review 2, N1)."""
    assert any(hit.startswith("W51") for hit in RC.withheld_findings("CP-26's results pooled with the five periods"))
    assert not RC.withheld_findings("never pooled with the five periods above")
    assert any(hit.startswith("W52") for hit in RC.withheld_findings("The live record as 4.7T is in progress."))
    assert any(hit.startswith("W52") for hit in RC.withheld_findings("4.7T's result is a pass."))
    assert not RC.withheld_findings("prospective evaluation in progress")


# --------------------------------------------------------------------------- never adopted, in MLflow too (review 3, F1)


def _adopted_problems(exports: dict[str, dict]) -> list[str]:
    """Runs an export tags `delu.adopted = "true"` although their registry entry was never adopted in research or
    released (a final candidate that its own rule selected: W49)."""
    problems = []
    for name, export in exports.items():
        for run in export["runs"]:
            entry = next((e for e in G.entries() if run["run_key"] in e.run_keys), None)
            if entry is None:
                continue
            adopted = any(event.status in (G.ADOPTED_IN_RESEARCH, G.RELEASED) for event in entry.statuses)
            if run["tags"].get("delu.adopted") == "true" and not adopted:
                problems.append(f"{name}: {run['run_key']} ({entry.id})")
    return problems


def test_no_export_calls_v6_adopted():
    exports = {name: json.loads((ROOT / f"reports/presentation/mlflow-export/{name}.json").read_text())
               for name in ("cp26", "cp28")}
    assert _adopted_problems(exports) == []
    # cp28/A1 and CP-26's four D2 masks; the parent cp28 is the checkpoint's own run and carries no adoption tag
    v6_runs = [run for export in exports.values() for run in export["runs"]
               if run["run_key"] in G.get("v6").run_keys and run["run_key"] != "cp28"]
    assert len(v6_runs) == 5
    assert {run["tags"]["delu.adopted"] for run in v6_runs} == {"false"}
    assert {run["tags"]["delu.status"] for run in v6_runs} == {"final candidate 2026-10-30"}


def test_negative_control_a_final_candidate_tagged_adopted_is_caught():
    export = json.loads((ROOT / "reports/presentation/mlflow-export/cp28.json").read_text())
    next(run for run in export["runs"] if run["run_key"] == "cp28/A1")["tags"]["delu.adopted"] = "true"
    assert _adopted_problems({"cp28": export}) == ["cp28: cp28/A1 (v6)"]
    # the rule itself: a final candidate is "false" unless an adoption or a release came first
    final = G.StatusEvent(G.FINAL_CANDIDATE, "2026-10-30", "x", "y")
    assert G.adopted_flag(G.get("v6"), (final,)) == "false"
    assert G.adopted_flag(G.get("v6"), (G.StatusEvent(G.ADOPTED_IN_RESEARCH, "2026-10-01", "x", "y"), final)) == "true"
