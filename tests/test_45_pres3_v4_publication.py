"""PRES-3: v4, CP-21's adopted generation, on every surface -- each contract with a negative control.

* The registry holds the publication packet's draft entries exactly as drafted, apart from the identities that exist
  only at landing, which come from the CP-21 landing record.
* The evidence layer reads CP-21's committed rows, pinned by blob; the shared comparison moved to CP-21's rows, which
  equal CP-20's cell for cell on every policy both carry.
* The derived headline quantities -- the verdict of rule `cp21-adoption`, its date, N, the distances in the rule's
  unit, the change as a share of v3's score from CP-21's own bootstrap draws, and the per-period MAE -- re-derive
  from committed rows.
* The headline leads with that verdict and names each metric beside its value (A1); the chapter carries the ladder
  with its bundled first step (C106), the block-split finding as C111 reads it and the peak finding (C120) visibly.
* The comparison chart labels each generation v1-v4 and leaves the met / not-met column to its value table (the
  Owner's direction of 2026-10-01); the comparison `cp20/HG` carries keeps its published names and column.
* Every historical chapter, transition and the product documentation are byte-identical to the published page.
* The planned-work list carries 4.6 as DDNN alone, against the registry's generation, and no TabPFN, on every
  generated surface (research anchor v21-r8 §18.5).
* The final CP-21 export equals CP-21's draft apart from its pending fields, and the publisher refuses any write
  outside the runs an instruction names.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import re
import sys
from decimal import Decimal
from types import SimpleNamespace

import pytest

from delu_forecast import derived as D
from delu_forecast import registry as G
from delu_forecast import research as R
from delu_forecast import research_claims as RC
from delu_forecast.claims import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT / "scripts"))

import build_pages as B  # noqa: E402
import mlflow_export as E  # noqa: E402
import mlflow_publish as P  # noqa: E402
import readme_research  # noqa: E402

PAGE = REPO_ROOT / "docs" / "index.html"
README = REPO_ROOT / "README.md"
CARDS = (REPO_ROOT / "space" / "README.md", REPO_ROOT / "space-wasm" / "README.md")
LANDING = "docs/track-b/cp-21-landing-2026-09-30.md"


@pytest.fixture(scope="module")
def page() -> str:
    return PAGE.read_text()


def _text(html: str) -> str:
    return " ".join(re.sub(r"<[^>]+>", " ", html).split()).replace(" ,", ",").replace(" .", ".")


def _chapter(document: str, ident: str) -> str:
    start = document.index(f'<article class="chapter" id="{ident}"')
    return document[start:document.index("</article>", start) + len("</article>")]


# --------------------------------------------------------------------------- the registry (runbook §2 steps 1-6)


def test_the_registry_holds_the_packets_draft_entries_exactly_apart_from_the_landing_identities():
    _, entries, checkpoint = E.draft_registry()
    for ident, drafted in entries.items():
        entry = G.get(ident)
        for field in dataclasses.fields(drafted):
            if field.name == "statuses":
                continue
            assert getattr(entry, field.name) == getattr(drafted, field.name), (ident, field.name)
        assert [(e.status, e.reason) for e in entry.statuses] == [(e.status, e.reason) for e in drafted.statuses]
        assert all(e.date == "pending-at-landing" for e in drafted.statuses)
        assert [(e.date, e.source) for e in entry.statuses] == [("2026-09-30", LANDING)]
    registered = G.CHECKPOINTS["CP-21"]
    for field in ("code", "run_key", "owner", "evidence_tag", "report", "verdict", "children"):
        assert getattr(registered, field) == getattr(checkpoint, field), field
    assert (registered.evidence_sha, registered.frozen_on, registered.landing) == ("1d13f99", "2026-09-30", LANDING)
    assert G.EVIDENCE_TAGS["evidence/cp-21"] == ("1d13f99", "2026-09-30")


def test_the_adoption_date_and_the_evidence_tag_come_from_the_landing_record():
    landing = (REPO_ROOT / LANDING).read_text()
    assert landing.splitlines()[0].endswith("2026-09-30")
    assert "`evidence/cp-21` | `1d13f99b1ab12f64719b439d0a9d4703bc7e1bdb`" in landing.replace(" / ", " | ") or \
        "| Evidence tip / `evidence/cp-21` | `1d13f99b1ab12f64719b439d0a9d4703bc7e1bdb` |" in landing
    assert "v4's registry name is \"v4 · three-block LightGBM added\"" in landing
    assert G.get("v4").name == "v4 · three-block LightGBM added"


def test_the_packets_code_additions_are_all_entered_and_change_no_published_run_name():
    spec, _, _ = E.draft_registry()
    for addition in spec["code_additions_to_existing_entries"]:
        wanted = G.Code(**addition["code"])
        assert wanted in G.get(addition["entry"]).codes, addition
    # a run's public name reads its code in its own experiment: every published run keeps its name
    for key in G.expected_run_keys():
        if not key.startswith("cp21"):
            assert G.mlflow_run_name(key) == next(
                run["run_name"] for name in ("cp10", "cp15", "cp16", "cp20")
                for run in json.loads((E.EXPORT_DIR / f"{name}.json").read_text())["runs"] if run["run_key"] == key)


def test_the_rule_the_orders_and_the_study_arms():
    spec, _, _ = E.draft_registry()
    rule = G.RULES["cp21-adoption"]
    assert (rule.id, rule.plan, rule.words, rule.set_on, list(rule.provenance)) == (
        spec["rule"]["id"], spec["rule"]["plan"], spec["rule"]["words"], spec["rule"]["set_on"],
        spec["rule"]["provenance"])
    assert G.COMPARISON_ORDER[0] == "v4" and G.COMPARISON_ORDER[1:] == G.V3_COMPARISON_ORDER
    assert G.CRISIS_ORDER[-1] == "v4" and "v4" not in G.V3_CRISIS_ORDER
    assert [(t.predecessor.id, t.successor.id, t.comparator_is_predecessor) for t in G.transitions(newest_first=False)][-1] \
        == ("v3", "v4", True)
    for ident in ("pooled-lightgbm-weather", "block-lightgbm", "normalized-block-lightgbm"):
        entry = G.get(ident)
        assert entry.kind == "study arm" and G.adoption_label(entry) == "Not adopted"
    assert G.current_generation().id == "v4" and G.released().id == "v1"


# --------------------------------------------------------------------------- evidence (steps 7-10)


def test_cp21_rows_are_blob_pinned_and_every_record_re_derives():
    cp21 = [record for record in R.records().values() if record.checkpoint == "CP-21"]
    assert cp21 and R.validate_all(cp21) == []
    for path in {record.source_path for record in cp21}:
        assert R.SOURCES[path].tag == "evidence/cp-21"
        R.check_source(path)


def test_negative_control_a_perturbed_cp21_row_fails(monkeypatch):
    record = R.get("cp21.ratio.HGL-HG.MAE")
    original = R.source_bytes
    target = record.source_path

    def perturbed(path):
        data = original(path)
        return data.replace(record.ci_high_raw.encode(), b"-0.0100000000000000", 1) if path == target else data

    monkeypatch.setattr(R, "source_bytes", perturbed)
    assert any("has changed" in problem for problem in R.validate_all([record]))


def test_the_comparison_moved_to_cp21s_rows_which_equal_cp20s_on_every_shared_policy():
    """The overview draws CP-21's rows (v4 is only there); for the seven policies CP-20 also carries, every
    published cell is identical, so no earlier number on the page changes by the move."""
    compared = 0
    for record_id, record in R.records().items():
        if not record_id.startswith("cp20.metrics."):
            continue
        twin = "cp21." + record_id[len("cp20."):]
        assert R.get(twin).raw == record.raw, twin
        compared += 1
    assert compared > 500
    assert G.COMPARISON_EXPERIMENT == "CP-21" and G.comparison_prefix() == "cp21"


def test_the_derived_headline_quantities():
    assert D.validate_all() == []
    assert D.get("derived.adoption.v4.verdict").value == "met"
    assert D.get("derived.adoption.v4.set_on").value == "2026-09-29"
    assert D.get("derived.adoption.v4.tested").value == "1"
    for score, metric in (("S_MAE", "MAE"), ("S_WIS", "WIS")):
        distance, cell = D.get(f"derived.adoption.v4.distance.{score}"), R.get(f"cp21.uncertainty.HGL-HG.equal_fold.{metric}")
        assert (distance.value, distance.ci_low, distance.ci_high) == (cell.raw, cell.ci_low_raw, cell.ci_high_raw)
        change, ratio = D.get(f"derived.change.v4.{score}"), R.get(f"cp21.ratio.HGL-HG.{metric}")
        # from CP-21's own draws: the ratio and its percentile interval, never a difference over a fixed denominator
        assert Decimal(change.value) == Decimal(ratio.raw) * 100
        assert (Decimal(change.ci_low), Decimal(change.ci_high)) == (Decimal(ratio.ci_low_raw) * 100,
                                                                      Decimal(ratio.ci_high_raw) * 100)
        assert D.display(change) == "−5%"
    assert (D.display(D.get("derived.periods.v4.ordinary_low")), D.display(D.get("derived.periods.v4.ordinary_high")),
            D.display(D.get("derived.periods.v4.stress"))) == ("4.9", "15.0", "47.0")
    assert D.stress_period() == "fold_3"


def test_negative_control_a_condition_not_met_is_not_a_met_verdict():
    spec = D.ADOPTION_RULES["v4"]
    flipped = lambda record_id: "False" if record_id.endswith("condition_4_met") else R.get(record_id).raw  # noqa: E731
    assert D._adoption_verdict(spec, flipped) == "not met"


def test_negative_control_a_rule_date_the_anchor_does_not_state_is_refused():
    spec = dict(D.ADOPTION_RULES["v4"], dated_by=(("capstone_v21.md", "Rule `cp21-adoption` was set on 2026-09-28"),))
    with pytest.raises(D.DerivedError):
        D._adoption_date(spec)


# --------------------------------------------------------------------------- the headline and the opening


def test_the_headline_leads_with_the_rules_verdict_and_names_each_metric(page):
    text = _text(RC.headline())
    assert text.startswith("Met the adoption rule set before the experiment")
    for number, metric in re.findall(r"(−?\d\.\d{4}) \[[^\]]+\] on the (point-error|interval) score", text):
        assert number and metric
    assert len(re.findall(r"\] on the (point-error|interval) score", text)) == 2
    assert "1 policy tested against the rule" in text
    opening = page[page.index('id="headline"'):page.index("</dl>", page.index('id="headline"'))]
    assert _text(RC.headline()) in _text(opening)
    readme = README.read_text()
    assert RC.headline("md") in readme


def test_the_opening_pairs_research_v4_with_released_v1(page):
    pair = page[page.index('class="status-pair"'):page.index("</dl>", page.index('class="status-pair"'))]
    assert 'data-registry="v1"' in pair and 'data-registry="v4"' in pair
    assert "Try the" in page and 'data-structural="version">v1</span> demo' in page


def test_the_terms_follow_the_headline(page):
    assert RC.headline_terms() == ("terms.error_scores", "terms.adoption_rule", "terms.differences", "terms.class")
    terms = page[page.index('class="headline-terms"'):page.index("</dd>", page.index('class="headline-terms"'))]
    for key in RC.headline_terms():
        assert f'data-block="{key}"' in terms
    assert 'data-block="terms.benchmark"' not in terms


# --------------------------------------------------------------------------- the comparison chart


def _chart_texts(chart: str) -> list[list[str]]:
    """The text of each variant (desktop, phone) of a chart's markup."""
    return [[_text(text) for text in re.findall(r"<text[^>]*>(.*?)</text>", svg, re.S)] for svg in chart.split("</svg>")[:2]]


def _has_verdict_column(texts: list[str]) -> bool:
    return bool({"Targets", "both met?", "targets:", "met", "not met"} & set(texts))


def test_the_comparison_labels_each_generation_by_its_short_name_and_leaves_the_verdicts_to_its_table(page):
    """The Owner's direction of 2026-10-01: a generation's row reads v1-v4 and its values, without its adopted change
    or a targets column. The met / not-met column (standard §15) is the value table's, beside the canonical names."""
    chart = page[page.index('data-chart-id="overview"'):]
    chart = chart[:chart.index("</div>")]
    generations = [entry for entry in G.comparison_rows() if entry.kind == "generation"]
    for texts in _chart_texts(chart):
        assert {entry.short for entry in generations} <= set(texts)
        assert not [text for text in texts if re.match(r"v\d+ ·", text)]
        assert not _has_verdict_column(texts)
    table = B.overview_table()
    assert '<th scope="col">Both targets</th>' in table
    tested = [entry for entry in G.comparison_rows() if f"derived.criteria.{entry.id}.verdict" in D.records()]
    assert len(tested) == 4
    for entry in tested:
        assert f'data-record="derived.criteria.{entry.id}.verdict"' in table
    for entry in generations:
        assert entry.name in _text(table)


def test_negative_control_the_pinned_comparison_keeps_its_published_names_and_column():
    """`cp20/HG`'s run carries v3's comparison as published, so the live labels could not reach it silently -- and
    the check above does catch a chart that still carries the column and the long names."""
    texts = _chart_texts(B.overview_chart(G.V3_COMPARISON_ORDER, B.V3_EXPERIMENT, pinned=True))[0]
    assert _has_verdict_column(texts)
    assert "v3 · weather features" in texts


# --------------------------------------------------------------------------- the chapter, the transition, the peak


def test_the_v4_chapter_carries_the_ladder_the_block_split_and_the_peak(page):
    chapter = _text(_chapter(page, "v4"))
    assert "bundled with the training-only choice of model size and the missing-input rule" in chapter  # C106, W23
    assert "not a weather effect on its own" in chapter
    split = _text(RC.render("v4.method.split"))
    assert split in chapter and "no demonstrated joint preference" in split  # C111 exactly, W22
    peak = _text(RC.render("v4.peak"))
    assert peak in chapter and "point error is higher than" in peak  # C120, in the stress-period detail


def test_the_peak_finding_is_on_the_reading_path_not_only_in_a_disclosure(page):
    chapter = _chapter(page, "v4")
    visible = chapter[:chapter.index('data-slot="details"')]
    assert "point error is higher than" in _text(visible)
    transition = page[page.index('data-transition="v3-v4"'):]
    transition = transition[:transition.index("</article>")]
    assert "point error is higher than" in _text(transition)
    assert "no demonstrated joint preference" in _text(transition)


def test_negative_control_a_chapter_without_its_peak_caveat_would_be_caught(page):
    doctored = _chapter(page, "v4").replace("point error is higher than", "point error is similar to")
    assert "point error is higher than" not in _text(doctored[:doctored.index('data-slot="details"')])


def test_the_transition_title_and_the_encoding():
    assert RC.render("transition.v3-v4.title", "md") == "From v3 to v4: adding a three-block LightGBM"
    assert B.TOKENS["v4"] == "#B45309"
    assert B.ROLE_STYLE["v4"] == {"color": "#B45309", "marker": "diamond", "filled": True}
    assert B.marker_problems() == []
    assert B.contrast(B.TOKENS["v4"], B.TOKENS["surface"]) >= 4.5
    assert B.contrast(B.TOKENS["v4"], B.TOKENS["canvas"]) >= 4.5
    legend = B.legend(("v4",))
    assert ">v4</span>" in legend and "#B45309" in legend


# The published PRES-2 page's historical sections, by SHA-256 (the page at 17f354e): a later generation adds its own
# chapter and never rewrites an earlier one.
PUBLISHED_SECTIONS = {
    r'<article class="chapter" id="v3".*?</article>': "9e0c19f406a1a6602ecbe6a7f85220b3cd6de4069f6a341649909c9c93de282f",
    r'<article class="chapter" id="v2".*?</article>': "500c8545e3833f4fb0e5c4abebc90218a7be4e7e0c46153128bbc23507147348",
    r'<article class="chapter" id="v1".*?</article>': "c44c7ebb9a536512ded94cb46df481a9be0080bc8aeee27d598ecebbb36fbbb4",
    r'<section class="section product".*?</section>': "7b8078e57432917624aa767e553045b51739e89fa2e49dd40320a4c47ed7551c",
    r'<article class="transition" id="transition-v2-v3".*?</article>':
        "8fc10b4cea60451946d03a18d3f56963c8b6dc794b67e19cb942f448aad03d2e",
    r'<article class="transition" id="transition-v1-v2".*?</article>':
        "fe749937c3a3097efd312756483e827184ae182b25163f11216202515b309445",
}


@pytest.mark.parametrize("pattern", sorted(PUBLISHED_SECTIONS))
def test_every_historical_section_is_byte_identical_to_the_published_page(page, pattern):
    section = re.search(pattern, page, re.DOTALL).group(0)
    assert hashlib.sha256(section.encode()).hexdigest() == PUBLISHED_SECTIONS[pattern]


def test_negative_control_a_v3_chart_fed_the_current_generation_cannot_redraw_silently(monkeypatch):
    """v3's charts read CP-20's rows for v1-v3 only; asking them to draw v4 fails loudly instead of changing a chapter
    (and a published MLflow artifact) behind the reader's back."""
    monkeypatch.setattr(B, "_hour_series", lambda: B._generation_codes(("v3", "v4"), "CP-21"))
    with pytest.raises(R.EvidenceError):
        B.v3_chapter()


# --------------------------------------------------------------------------- planned work (v21-r8 §18.5)

FORBIDDEN_PLANNED = re.compile(r"TabPFN|tabular foundation model", re.IGNORECASE)


def planned_problems(surfaces: dict[str, str], comparator: str) -> list[str]:
    """The planned list, corrected: 4.6 is DDNN alone against the registry's generation; 4.5 is gone; no generated
    surface names TabPFN or a tabular foundation model."""
    problems = []
    for name, text in surfaces.items():
        for match in FORBIDDEN_PLANNED.finditer(text):
            problems.append(f"{name}: {match.group(0)!r}")
    page = surfaces.get("page", "")
    if page:
        start = page.index('id="planned"')
        section = _text(page[start:page.index("</section>", start)])
        if "4.6 · DDNN" not in section:
            problems.append("page: 4.6 is not DDNN")
        if "4.5" in section or "Three-block LightGBM" in section:
            problems.append("page: 4.5 is still planned")
        if f"improve on {comparator}," not in section:
            problems.append(f"page: 4.6's question does not name {comparator}")
        if f"compared with {comparator} on identical hours" not in section:
            problems.append(f"page: the section's comparator is not {comparator}")
    return problems


def _generated_surfaces() -> dict[str, str]:
    readme = README.read_text()
    blocks = "".join(readme[readme.index(start):readme.index(end)] for start, end in (
        (readme_research.GLANCE_START, readme_research.GLANCE_END), (readme_research.START, readme_research.END)))
    return {"page": PAGE.read_text(), "readme": blocks, **{str(card.relative_to(REPO_ROOT)): card.read_text()
                                                            for card in CARDS}}


def test_the_planned_list_is_corrected_on_every_generated_surface():
    assert planned_problems(_generated_surfaces(), G.current_generation().version) == []
    items = {item: (name, code, question) for name, item, code, question, _ in B.planned_items()}
    assert set(items) == {"4.6", "4.4V", "4.8", "4.7T and live"}
    assert items["4.6"][1] == "DDNN" and "v4" in items["4.6"][2]


def test_the_other_planned_items_keep_their_content():
    kept = {item: (name, code, question, evidence) for name, item, code, question, evidence in B.PLANNED_WORK}
    assert kept["4.4V"] == ("Wind and solar generation forecasts", "VRE",
                            "Does an in-house wind and solar generation forecast add information beyond direct weather?",
                            "A held-forward generation model, then an ablation")
    assert kept["4.8"] == ("Combining models", "Recombination", "Does combining adopted models help?",
                           "A predefined combination test")
    assert kept["4.7T and live"][0] == "Frozen-protocol evaluation, then prospective monitoring"


@pytest.mark.parametrize("doctored, expected", [
    (lambda s: s.replace("· DDNN</dd>", "· DDNN / TabPFN</dd>"), "TabPFN"),
    (lambda s: s.replace("a distributional neural network", "a tabular foundation model"), "tabular foundation model"),
    (lambda s: s.replace('improve on <span data-structural="version">v4</span>,',
                         'improve on <span data-structural="version">v3</span>,'), "does not name v4"),
    (lambda s: s.replace('<ol class="planned-list">', '<ol class="planned-list"><li>4.5 · Three-block LightGBM</li>'),
     "4.5 is still planned"),
])
def test_negative_controls_a_stale_planned_list_is_caught(doctored, expected):
    surfaces = _generated_surfaces()
    surfaces["page"] = doctored(surfaces["page"])
    assert any(expected in problem for problem in planned_problems(surfaces, "v4"))


def test_negative_control_tabpfn_in_a_space_card_or_the_readme_is_caught():
    surfaces = _generated_surfaces()
    surfaces["space/README.md"] += "\nPlanned: TabPFN.\n"
    surfaces["readme"] += "\nA tabular foundation model is planned.\n"
    problems = planned_problems(surfaces, "v4")
    assert any(p.startswith("space/README.md") for p in problems) and any(p.startswith("readme") for p in problems)


def test_the_claim_guard_w14_is_unchanged():
    patterns = dict(RC.WITHHELD_PATTERNS)
    assert patterns["W14"].pattern == r"\b(Chronos-2|TabPFN|DDNN|VRE) (outperforms|beats|improves)\b"


# --------------------------------------------------------------------------- withheld claims W22-W26


@pytest.mark.parametrize("wid, text", [
    ("W22", "The block split helps the forecast."),
    ("W23", "The gain is a weather effect on its own."),
    ("W24", "Try the v4 demo."),
    ("W25", "The pooled and block models are equivalent."),
    ("W26", "The daily cycle shows qualification for daily operation."),
])
def test_negative_controls_cp21s_withheld_claims_are_caught(wid, text):
    assert any(finding.startswith(wid) for finding in RC.withheld_findings(text))


def test_no_surface_carries_a_withheld_claim(page):
    for text in (page, README.read_text()):
        flat = text[:text.find('<details class="disclosure archive"')] if "v1-archive" in text else text
        assert [f for f in RC.withheld_findings(_text(flat)) if f[:3] in ("W22", "W23", "W24", "W25", "W26")] == []


# --------------------------------------------------------------------------- the MLflow export (step 17)


def test_the_final_cp21_export_equals_the_draft_apart_from_its_pending_fields():
    draft = json.loads((E.DRAFT_DIR / "cp21.json").read_text())
    report = E.final_vs_draft(draft, E.tracked_runs("cp21"))
    assert report["equal_apart_from_pending"], report["differences"]
    assert set(report["filled"]) == {"cp21", "cp21/HGL", "cp21/L-P", "cp21/L-R", "cp21/L-N"}
    assert set(report["chart_artifacts_added"]) == {"cp21/HGL"}
    committed = json.loads((E.EXPORT_DIR / "cp21.json").read_text())
    assert [run["run_name"] for run in committed["runs"]] == [run["run_name"] for run in draft["runs"]]


@pytest.mark.parametrize("change, expected", [
    (lambda run: run["metrics"]["s_mae"][0].update(value=0.5), "metrics"),
    (lambda run: run.update(run_name=run["run_name"] + " (renamed)"), "run_name"),
    (lambda run: run["tags"].update({"delu.kind": "branch"}), "tag delu.kind"),
    (lambda run: run["params"].update(seed="1"), "params"),
])
def test_negative_controls_a_final_export_that_differs_beyond_the_pending_fields(change, expected):
    draft = json.loads((E.DRAFT_DIR / "cp21.json").read_text())
    runs = E.tracked_runs("cp21")
    change(next(run for run in runs if run["run_key"] == "cp21/HGL"))
    report = E.final_vs_draft(draft, runs)
    assert not report["equal_apart_from_pending"] and any(expected in item for item in report["differences"])


def test_the_experiment_description_is_the_published_one():
    manifest = json.loads((E.EXPORT_DIR / "manifest.json").read_text())
    assert manifest["experiment_tags"] == E.EXPERIMENT_TAGS
    assert "(CP-21)" not in E.EXPERIMENT_TAGS["mlflow.note.content"]


# --------------------------------------------------------------------------- the publisher's authorized-runs guard


class _Client:
    def __init__(self, tags: dict, runs: dict[str, dict | None], exists: bool = True):
        self.experiment = SimpleNamespace(experiment_id="1", tags=tags) if exists else None
        self.runs = runs

    def get_experiment_by_name(self, name):
        return self.experiment

    def search_runs(self, experiment_ids, filter_string, max_results):
        key = re.search(r"= '([^']+)'", filter_string).group(1)
        tags = self.runs.get(key)
        return [] if tags is None else [SimpleNamespace(data=SimpleNamespace(tags=tags), info=SimpleNamespace(run_id=key))]


AUTHORIZED = ("cp21", "cp21/HGL", "cp21/L-P", "cp21/L-R", "cp21/L-N")


def _export_runs() -> dict[str, dict]:
    return {key: {} for key in G.expected_run_keys()}


def _published() -> dict[str, dict | None]:
    out = {}
    for key in G.expected_run_keys():
        if key in AUTHORIZED:
            out[key] = None
        else:
            out[key] = {"delu.upload_state": "complete", **({"delu.package_complete": "true"} if "/" not in key else {})}
    return out


def test_the_write_plan_admits_exactly_the_authorized_runs():
    plan = P.write_plan(_Client(dict(E.EXPERIMENT_TAGS), _published()), _export_runs(), AUTHORIZED)
    assert plan["to_write"] == sorted(AUTHORIZED) and plan["experiment_tags_to_write"] == []


@pytest.mark.parametrize("client, expected", [
    (lambda: _Client({**E.EXPERIMENT_TAGS, "mlflow.note.content": "older"}, _published()), "experiment tag"),
    (lambda: _Client(dict(E.EXPERIMENT_TAGS), {**_published(), "cp20/HG": {"delu.upload_state": "incomplete"}}),
     "run cp20/HG"),
    (lambda: _Client(dict(E.EXPERIMENT_TAGS), {**_published(), "cp15/B0": None}), "run cp15/B0"),
    (lambda: _Client(dict(E.EXPERIMENT_TAGS), {**_published(), "cp20": {"delu.upload_state": "complete"}}),
     "package is not marked complete"),
    (lambda: _Client(dict(E.EXPERIMENT_TAGS), _published(), exists=False), "does not exist"),
])
def test_negative_controls_a_write_outside_the_authorized_runs_refuses_before_writing(client, expected):
    with pytest.raises(P.Refused, match=expected):
        P.write_plan(client(), _export_runs(), AUTHORIZED)
