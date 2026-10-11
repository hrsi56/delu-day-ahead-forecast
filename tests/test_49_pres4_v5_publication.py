"""PRES-4: v5, CP-24's adopted generation, on the research surfaces, with CP-22 and CP-23 as branch cards -- each
contract with a negative control.

* The registry holds CP-24's draft entries as drafted, with the Owner's name for v5 (2026-10-11) and the statuses
  dated and sourced from the CP-24 landing record; CP-22 and CP-23 enter as branches with their study arms; every
  draft's code additions are entered and change no published run name; the lists gain the three checkpoints, their
  evidence tags, their rules, and v5 first in the comparison order.
* CP-22's, CP-23's and CP-24's committed rows are pinned by blob and re-derive; v5's rule `cp24-adoption` decided at
  97.5%, and the headline leads with that verdict at that level (claim map W47); both ratio intervals, at 95% and at
  97.5%, come from CP-24's own draws.
* The coverage limits -- the scored days against the days in the data, none in October to December, one winter --
  re-derive from committed records and read no row after the boundary.
* The comparison draws each row from the newest experiment that carries it, on one population, with the branches'
  candidates as study points; v4's published comparison stays pinned on its MLflow run.
* Every historical chapter, transition and the product documentation are byte-identical to the published page.
* The planned list follows the Owner's programme plan of 2026-10-11 on every generated surface.
* The final exports equal their drafts apart from the pending fields and the Owner's name; no published record
  changes; the publisher admits exactly the authorized runs and the one experiment-description write.
* The Space is unchanged: both generated cards are byte-identical to PRES-3's.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import re
import subprocess
import sys
from types import SimpleNamespace

import pytest

from delu_forecast import derived as D
from delu_forecast import publication_lint as L
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
CARDS = {"space/README.md": "745bbb932d78afbecdca3964af4885d223fd9301cd628bde1744f08e9f71d553",
         "space-wasm/README.md": "c92a2666d76255b24d8e0fb159f97bedcbee0a7a948fb6afeac4b02089bb9a67"}
LANDING24 = "docs/track-b/cp-24-landing-2026-10-11.md"
DRAFTS = {"CP-22": "reports/v4-revision/draft-registry.json",
          "CP-23": "reports/distribution-challenger/draft-registry.json",
          "CP-24": "reports/ddnn2/draft-registry.json"}
LANDINGS = {"CP-22": ("docs/track-b/cp-22-landing-2026-10-04.md", "2026-10-04"),
            "CP-23": ("docs/track-b/cp-23-landing-2026-10-04.md", "2026-10-04"),
            "CP-24": (LANDING24, "2026-10-11")}
#: The published export before PRES-4: main at the brief's issue.
PUBLISHED_REF = "e398a30bb53ecd4c397aad0f34fd122d42e74553"


@pytest.fixture(scope="module")
def page() -> str:
    return PAGE.read_text()


def _text(html: str) -> str:
    return " ".join(re.sub(r"<[^>]+>", " ", html).split()).replace(" ,", ",").replace(" .", ".")


def _chapter(document: str, ident: str) -> str:
    start = document.index(f'<article class="chapter" id="{ident}"')
    return document[start:document.index("</article>", start) + len("</article>")]


def _draft(checkpoint: str) -> dict:
    return json.loads((REPO_ROOT / DRAFTS[checkpoint]).read_text())


# --------------------------------------------------------------------------- the registry (runbook §2 steps 1-6, §3)


#: The fields where the registry departs from a draft entry, each for a recorded reason: the Owner's name for v5; the
#: eight-word subtitle field (standard §5) for CP-23's DDNN alone; and CP-22's branch reason, whose pending clause ("the
#: Owner decides first") the landing record resolved ("the Owner kept v4 unchanged").
DEPARTURES = {("v5", "name"), ("ddnn-alone", "subtitle")}


@pytest.mark.parametrize("checkpoint", sorted(DRAFTS))
def test_the_registry_holds_each_drafts_entries_apart_from_the_landing_identities(checkpoint):
    spec = _draft(checkpoint)
    landing, date = LANDINGS[checkpoint]
    for raw in spec["entries"]:
        entry = G.get(raw["id"])
        for field in dataclasses.fields(entry):
            if field.name in ("statuses", "codes") or (entry.id, field.name) in DEPARTURES:
                continue
            drafted = raw[field.name]
            value = getattr(entry, field.name)
            assert (list(value) if isinstance(value, tuple) else value) == drafted, (entry.id, field.name)
        assert [G.Code(**code) for code in raw["codes"]] == list(entry.codes[:len(raw["codes"])]), entry.id
        assert [(event.date, event.source, event.status) for event in entry.statuses] == [
            (date, landing, event["status"]) for event in raw["statuses"]], entry.id
        if entry.id != "pooled-lightgbm-member-for-v4":
            assert [event.reason for event in entry.statuses] == [event["reason"] for event in raw["statuses"]]
    assert G.get("v5").name == "v5 · DDNN-2 added" and _draft("CP-24")["entries"][0]["name"] == "v5 · DDNN-2 member added"
    assert len(G.get("ddnn-alone").subtitle.split()) <= 8 < len(next(
        raw for raw in _draft("CP-23")["entries"] if raw["id"] == "ddnn-alone")["subtitle"].split())
    assert "the Owner kept v4 unchanged" in G.get("pooled-lightgbm-member-for-v4").status.reason
    assert "v4 נשאר כפי שהוא" in (REPO_ROOT / "capstone_v21.md").read_text()


def test_the_owners_name_and_the_adoption_date_come_from_the_brief_and_the_landing_record():
    v5 = G.get("v5")
    assert (v5.kind, v5.predecessor, v5.comparator, v5.style, v5.anchor) == ("generation", "v4", "v4", "v5", "#v5")
    assert v5.statuses == (G.StatusEvent(G.ADOPTED_IN_RESEARCH, "2026-10-11", LANDING24),)
    landing = (REPO_ROOT / LANDING24).read_text()
    assert landing.splitlines()[0].endswith("2026-10-11") and "adopted in research" in landing
    assert G.current_generation().id == "v5" and G.released().id == "v1" and G.hero().id == "v1"
    for ident in ("ddnn2-alone", "v3-plus-ddnn2"):
        assert G.get(ident).kind == "study arm" and G.adoption_label(G.get(ident)) == "Not adopted"


def test_negative_control_a_status_dated_before_its_predecessor_is_refused():
    v5 = G.get("v5")
    early = dataclasses.replace(v5, statuses=(dataclasses.replace(v5.statuses[0], date="2026-09-01"),))
    entries = tuple(early if entry.id == "v5" else entry for entry in G.entries())
    assert any("adopted before its predecessor" in problem for problem in G.transition_problems(entries))


def test_every_drafts_code_additions_are_entered_and_change_no_published_run_name():
    for checkpoint in DRAFTS:
        for addition in _draft(checkpoint)["code_additions_to_existing_entries"]:
            assert G.Code(**addition["code"]) in G.get(addition["entry"]).codes, (checkpoint, addition)
    published = E.export_at(PUBLISHED_REF) if _has(PUBLISHED_REF) else None
    if published is None:
        pytest.skip("the published export's commit is not in this checkout")
    names = {run["run_key"]: run["run_name"] for name, content in published.items() if name != "manifest"
             for run in content["runs"]}
    assert len(names) == 28 and all(G.mlflow_run_name(key) == name for key, name in names.items())


def test_a_code_names_one_identity_per_experiment_and_a_shared_text_needs_its_experiment():
    assert G.by_code("v5", "CP-23").id == "ddnn-member-on-v4" and G.by_code("v5", "CP-24").id == "v5"
    assert G.generation_of("v5", "CP-23") is None and G.generation_of("v5", "CP-24") == "v5"
    assert R.get("cp23.metrics.v5.equal_fold.S_MAE").generation is None
    assert R.get("cp24.metrics.v5.equal_fold.S_MAE").generation == "v5"
    with pytest.raises(G.RegistryError, match="name the experiment"):
        G.by_code("v5")


def test_negative_control_one_code_naming_two_identities_in_one_experiment_is_refused(monkeypatch):
    twin = dataclasses.replace(G.get("ddnn2-alone"), codes=(G.Code("CP-24", "v5", "common-10747h"),))
    monkeypatch.setattr(G, "_ENTRIES", tuple(twin if entry.id == "ddnn2-alone" else entry for entry in G._ENTRIES))
    G.entries.cache_clear(), G._by_id.cache_clear(), G._by_scoped_code.cache_clear(), G._by_code.cache_clear()
    try:
        with pytest.raises(G.RegistryError, match="two identities in CP-24"):
            G.by_code("v5", "CP-24")
    finally:
        monkeypatch.undo()
        G.entries.cache_clear(), G._by_id.cache_clear(), G._by_scoped_code.cache_clear(), G._by_code.cache_clear()


def _has(ref: str) -> bool:
    return subprocess.run(["git", "cat-file", "-e", f"{ref}^{{commit}}"], cwd=REPO_ROOT, capture_output=True).returncode == 0


def test_the_lists_gain_the_three_checkpoints_tags_and_rules():
    expected = {"CP-22": ("cp22", "pooled-lightgbm-member-for-v4", "evidence/cp-22", "8daf7d0", "2026-10-04"),
                "CP-23": ("cp23", "ddnn-member-on-v4", "evidence/cp-23", "928bc13", "2026-10-04"),
                "CP-24": ("cp24", "v5", "evidence/cp-24", "05b7e61", "2026-10-10")}
    for code, (run_key, owner, tag, sha, frozen) in expected.items():
        checkpoint = G.CHECKPOINTS[code]
        spec = _draft(code)["checkpoint"]
        assert (checkpoint.run_key, checkpoint.owner, checkpoint.evidence_tag, checkpoint.evidence_sha,
                checkpoint.frozen_on) == (run_key, owner, tag, sha, frozen)
        assert (checkpoint.report, checkpoint.verdict, list(checkpoint.children)) == (
            spec["report"], spec["verdict"], spec["children"])
        assert checkpoint.landing == LANDINGS[code][0]
        assert G.EVIDENCE_TAGS[tag] == (sha, frozen)
        if _has(tag):
            full = subprocess.run(["git", "log", "-1", "--format=%H %cd", "--date=format:%Y-%m-%d", tag], cwd=REPO_ROOT,
                                  capture_output=True, text=True).stdout.split()
            assert full[0].startswith(sha) and full[1] == frozen, tag
    sets = {"cp22-replacement": "2026-10-01", "cp22-dynamic-layer": "2026-10-01", "cp22-fast-component": "2026-10-01",
            "cp23-adoption": "2026-10-04", "cp24-adoption": "2026-10-05"}
    assert {rule: G.RULES[rule].set_on for rule in sets} == sets
    for code in DRAFTS:
        for rule in _draft(code)["rules"]:
            assert (G.RULES[rule["id"]].plan, G.RULES[rule["id"]].set_on) == (rule["plan"], rule["set_on"])
    assert G.COMPARISON_ORDER[0] == "v5" and list(G.CHECKPOINTS)[-3:] == ["CP-22", "CP-23", "CP-24"]


# --------------------------------------------------------------------------- evidence (steps 7-10)


def test_the_new_rows_are_blob_pinned_and_every_record_re_derives():
    for path in (*R.CP22_ROWS.values(), *R.CP23_ROWS.values(), *R.CP24_ROWS.values(), "data/source_manifest.json",
                 "data/partitions.json"):
        R.check_source(path)
    new = [record for record in R.records().values() if record.checkpoint in ("CP-22", "CP-23", "CP-24")]
    assert len(new) > 5000 and R.validate_all(new) == []
    assert D.validate_all() == []


def test_negative_control_a_perturbed_cp24_row_fails(monkeypatch):
    path = R.CP24_ROWS["uncertainty"]
    original = R.source_bytes(path)
    doctored = original.replace(b"-0.01333737807223645", b"-0.01333737807223646", 1)
    assert doctored != original
    monkeypatch.setattr(R, "source_bytes", lambda p: doctored if p == path else (REPO_ROOT / p).read_bytes())
    with pytest.raises(R.EvidenceError, match="has changed"):
        R.check_source(path)


def test_both_ratio_intervals_come_from_cp24s_own_draws():
    ratio = {(row["candidate"], row["baseline"], row["metric"]): row for _, row in R._rows(R.CP24_ROWS["ratios"])}
    for metric in ("MAE", "WIS"):
        at95, at975 = R.get(f"cp24.ratio.v5-HGL.{metric}"), R.get(f"cp24.ratio97_5.v5-HGL.{metric}")
        row = ratio[("v5", "HGL", metric)]
        assert at95.raw == at975.raw == row["ratio"]
        # the two files agree on the 95% interval; the 97.5% one is wider, from the same stored draws
        assert (float(at95.ci_low_raw), float(at95.ci_high_raw)) == (float(row["ratio_ci95_lower"]),
                                                                    float(row["ratio_ci95_upper"]))
        assert at975.ci_low < at95.ci_low < at95.ci_high < at975.ci_high < 0
        assert (at95.interval.level, at975.interval.level) == (0.95, 0.975)
        decision = R.get(f"cp24.uncertainty97_5.v5-HGL.equal_fold.{metric}")
        stored = R._json(R.CP24_ROWS["decisions"])["adoption"]["conditions"]["1"]["values"][metric]
        assert (float(decision.ci_low_raw), float(decision.ci_high_raw)) == (stored["ci97.5_lower"], stored["ci97.5_upper"])
    for score in ("S_MAE", "S_WIS"):
        assert D.display(D.get(f"derived.change.v5.{score}")) == D.display(D.get(f"derived.change_decision.v5.{score}"))


def test_the_rules_verdict_date_n_and_distance_re_derive():
    assert {key: D.get(f"derived.adoption.v5.{key}").value for key in ("verdict", "set_on", "tested")} == {
        "verdict": "met", "set_on": "2026-10-05", "tested": "1"}
    distance = D.get("derived.adoption.v5.distance.S_MAE")
    assert distance.inputs == ("cp24.uncertainty97_5.v5-HGL.equal_fold.MAE",)
    assert float(distance.ci_high) < 0 and len(D.ADOPTION_RULES["v5"]["conditions"]) == 5
    assert [D.display(D.get(f"derived.periods.v5.{k}")) for k in ("ordinary_low", "ordinary_high", "stress")] == [
        "4.8", "14.4", "45.5"]
    assert D.stress_period() == "fold_3"


def test_negative_control_a_condition_not_met_is_not_a_met_verdict():
    spec = D.ADOPTION_RULES["v5"]
    value = lambda rid: "False" if rid.endswith("condition_5_met") else R.get(rid).raw  # noqa: E731
    assert D._adoption_verdict(spec, value) == "not met"
    renamed = lambda rid: "v6" if rid.endswith("adoption.candidate") else R.get(rid).raw  # noqa: E731
    assert D._adoption_verdict(spec, renamed) == "not met"


def test_negative_control_a_rule_date_the_anchor_does_not_state_is_refused(monkeypatch):
    monkeypatch.setitem(D.ADOPTION_RULES, "v5", {**D.ADOPTION_RULES["v5"], "dated_by": (
        ("capstone_v21.md", "Pre-registered rule `cp24-adoption`, set 2026-10-06"),)})
    with pytest.raises(D.DerivedError):
        D._adoption_date(D.ADOPTION_RULES["v5"])


# --------------------------------------------------------------------------- the coverage limits


def test_the_coverage_limits_re_derive_from_committed_records():
    facts = {key: D.get(f"derived.coverage.{key}").value for key in D.COVERAGE_KINDS}
    assert facts == {"days": "448", "data_days": "2654", "first_data_day": "2019-01-01", "data_end": "2026-04-07",
                     "q4_days": "0", "winters": "1"}
    dates = json.loads(next(row for _, row in R._rows(R.CP24_ROWS["metrics"])
                            if row["policy"] == "B0" and row["scope"] == "pooled")["represented_dates"])
    assert max(dates) <= R.EVIDENCE_BOUNDARY and not [d for d in dates if d[5:7] in ("10", "11", "12")]


@pytest.mark.parametrize("change, expected", [
    (lambda row, m, p: ({**row, "represented_dates": json.dumps(json.loads(row["represented_dates"])[:-1] + ["2025-11-05"])},
                        m, p), ("q4_days", "1")),
    (lambda row, m, p: ({**row, "represented_dates": json.dumps(json.loads(row["represented_dates"])[:-1] + ["2024-12-05"])},
                        m, p), ("winters", "2")),
])
def test_negative_controls_a_changed_population_changes_the_limits(change, expected):
    facts = D._coverage_facts(*change(*D._coverage_inputs()))
    assert facts[expected[0]] == expected[1]


@pytest.mark.parametrize("change, message", [
    (lambda row, m, p: (row, {**m, "coverage": {"price_eur_mwh": {**m["coverage"]["price_eur_mwh"], "null_rows": 3}}}, p),
     "missing hours"),
    (lambda row, m, p: (row, m, {**p, "eda_cutoff": "2026-04-08"}), "not the evidence boundary"),
    (lambda row, m, p: ({**row, "n_days": "449.0"}, m, p), "day count"),
])
def test_negative_controls_the_limits_refuse_an_uncountable_denominator(change, message):
    with pytest.raises(D.DerivedError, match=message):
        D._coverage_facts(*change(*D._coverage_inputs()))


def test_the_limits_are_stated_in_the_chapter_and_the_transition(page):
    chapter, journey = _text(_chapter(page, "v5")), page[page.index('id="journey"'):page.index('id="chapters"')]
    card = _text(journey[journey.index('data-transition="v4-v5"'):])
    for text in (chapter, card):
        assert "448 of the 2,654 days of data up to the end of the development period" in text
        assert "0 of them fall in October to December" in text
        assert "only 1 winter (December to February) contains any of them" in text
        assert "second decision on a distributional neural network" in text and "planned" not in text.split("winter")[1][:200]


# --------------------------------------------------------------------------- the comparison


def test_the_comparison_is_one_population_with_the_branch_candidates_as_study_points(page):
    assert D.comparison_parity_problems() == []
    sources = {entry.id: G.comparison_source(entry) for entry in G.comparison_rows()}
    assert sources["v5"] == sources["v4"] == sources["naive"] == "CP-24" and sources["v2"] == "CP-22"
    assert sources["ddnn-member-on-v4"] == "CP-23"
    points = [entry for entry in G.comparison_rows() if B.is_branch_point(entry)]
    assert {entry.id for entry in points} == {"v3-plus-pooled-normalized-lightgbm-averaged",
                                              "v3-plus-pooled-lightgbm-pair", "ddnn-member-on-v4"}
    chart = page[page.index('data-chart-id="overview"'):]
    chart = chart[:chart.index("</div>")]
    for entry in points:
        assert B.comparison_role(entry) == "study" and f"{entry.short} (not adopted)" in chart
        source = G.comparison_source(entry)
        assert f'data-record="{G.comparison_prefix(source)}.metrics.{entry.code_in(source)}.equal_fold.S_MAE"' in chart
    assert L.page_consistency_problems(page) == []


def test_negative_control_a_comparison_that_is_not_one_population_is_refused(monkeypatch):
    record = R.get("cp22.metrics.HGL.equal_fold.S_MAE")
    records = dict(R.records())
    records[record.record_id] = dataclasses.replace(record, raw="0.5357")
    monkeypatch.setattr(R, "records", lambda: records)
    problems = D.comparison_parity_problems()
    assert any("v4: S_MAE (equal_fold) differs between CP-24 and CP-22" in problem for problem in problems)
    with pytest.raises(G.RegistryError, match="not one population"):
        B.overview_panels()


def test_v4s_published_comparison_stays_pinned_on_its_run():
    published = json.loads((E.EXPORT_DIR / "cp21.json").read_text())
    run = next(run for run in published["runs"] if run["run_key"] == "cp21/HGL")
    artifact = next(item for item in run["artifacts"] if item["path"] == "charts/overview.svg")
    assert hashlib.sha256(B.standalone_svg(B.overview_chart(G.V4_COMPARISON_ORDER, B.V4_EXPERIMENT)).encode()
                          ).hexdigest() == artifact["sha256"]
    assert ("cp21/HGL", "overview") in B.PINNED_CHARTS
    assert hashlib.sha256(B.standalone_svg(B.overview_chart()).encode()).hexdigest() != artifact["sha256"]


# --------------------------------------------------------------------------- the headline, the chapter, the cards


def test_the_headline_leads_with_the_verdict_at_the_decision_level_and_names_each_metric(page):
    text = re.sub(r"<[^>]+>", "", RC.headline())
    assert text.startswith("Met the adoption rule set before the experiment: both error scores improved on v4's "
                           "(v5 − v4 at 97.5%: ")
    assert "on the point-error score" in text and "on the interval score" in text
    claim, _ = RC.headline_template()
    assert claim == "P53" and RC.headline("md") in README.read_text()
    terms = page[page.index('class="headline-terms"'):page.index("</dd>", page.index('class="headline-terms"'))]
    plain = re.sub(r"<[^>]+>", "", terms)
    assert "with the rule's 97.5% interval" in plain and "DDNN-2: a distributional neural network (DDNN)" in plain
    assert "its five conditions are in the v5 chapter" in plain and 'href="#v5-rule"' in terms


def _standard_definition() -> str:
    """The error scores' definition at first use, as Publication Standard v1 §3.1 prescribes it."""
    text = (REPO_ROOT / "docs" / "track-b" / "publication-standard-v1.md").read_text()
    quoted = re.search(r'\*\*Definition, at first use:\*\* "([^"]+)"', text, flags=re.S).group(1)
    return re.sub(r"\s+", " ", quoted)


def _term_problems(page: str) -> list[str]:
    """The headline terms against the text their claims bind (Integration review 1, V2): the error scores'
    definition is the standard's (P21), and the paired difference reads as P53 quotes it."""
    start = page.index('class="headline-terms"')
    terms = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", page[start:page.index("</dd>", start)]))
    p53 = next(line for line in (REPO_ROOT / "docs" / "track-b" / "research-content" / "publication-claims.md"
                                 ).read_text().splitlines() if line.startswith("| P53 |"))
    quoted = re.search(r'the paired difference is defined beneath it at that level \("([^"]+)"', p53).group(1)
    problems = []
    if f"Error scores: {_standard_definition()}." not in terms:
        problems.append("the error scores' term is not the standard's definition (P21)")
    if quoted not in terms:
        problems.append(f"the paired-difference term does not read as P53 quotes it: {quoted!r}")
    return problems


def test_the_headline_terms_read_as_their_claims_bind(page):
    assert _term_problems(page) == []


@pytest.mark.parametrize("old, new", [
    ("averaged over the test periods", "averaged by test period"),
    ("with the rule's", "with its"),
])
def test_negative_controls_a_term_that_drifts_from_its_claim_is_caught(page, old, new):
    start = page.index('class="headline-terms"')
    end = page.index("</dd>", start)
    terms = re.sub(r"\s+", " ", page[start:end])
    assert old in terms
    assert _term_problems(page[:start] + terms.replace(old, new) + page[end:])


#: The exact interval endpoints of v5's change as a share of v4's score (`ratio-intervals.csv` L2–L3), as the
#: Integration review's acceptance test names them.
V5_RATIO_ENDPOINTS = {
    "Point-error score": ("-2.9584699118793495", "-1.793927483038195", "-3.0367905356064449", "-1.6822708947669157"),
    "Interval score": ("-2.7786808736341522", "-1.714496476404881", "-2.8593332937828102", "-1.6208499381219484"),
}


def _ratio_table_problems(page: str) -> list[str]:
    """Each interval cell of v5's exact-ratio table holds both endpoints of its derived record, at full precision
    (Integration review 1, V1): never the point value standing in for an interval."""
    start = page.index('id="v5-ratio-values"')
    table = page[start:page.index("</table>", start)]
    problems = []
    for name, score in (("Point-error score", "S_MAE"), ("Interval score", "S_WIS")):
        row = re.search(r'<th scope="row">%s</th>(.*?)</tr>' % name, table, flags=re.S).group(1)
        cells = re.findall(r"<td[^>]*>(.*?)</td>", row, flags=re.S)
        point, intervals = cells[0], cells[1:]
        expected = []
        for prefix in ("derived.change", "derived.change_decision"):
            record = D.get(f"{prefix}.v5.{score}")
            expected.append((prefix, record.ci_low, record.ci_high))
        if 'data-field' in point or f'data-record="derived.change.v5.{score}"' not in point:
            problems.append(f"{name}: the change column is not the point value")
        if len(intervals) != 2:
            problems.append(f"{name}: {len(intervals)} interval columns")
            continue
        for cell, (prefix, low, high) in zip(intervals, expected):
            found = {field: value for value, field in re.findall(
                r'<data value="([^"]+)"[^>]*data-record="%s\.v5\.%s"[^>]*data-field="(ci_low|ci_high)"'
                % (re.escape(prefix), score), cell)}
            if found != {"ci_low": low, "ci_high": high}:
                problems.append(f"{name}, {prefix}: {found} is not [{low}, {high}]")
    return problems


def test_the_v5_ratio_table_carries_each_interval_at_full_precision(page):
    assert _ratio_table_problems(page) == []
    for name, endpoints in V5_RATIO_ENDPOINTS.items():
        score = "S_MAE" if name == "Point-error score" else "S_WIS"
        records = [D.get(f"{prefix}.v5.{score}") for prefix in ("derived.change", "derived.change_decision")]
        assert (records[0].ci_low, records[0].ci_high, records[1].ci_low, records[1].ci_high) == endpoints


def test_negative_control_a_point_value_in_an_interval_column_is_caught(page):
    start = page.index('id="v5-ratio-values"')
    end = page.index("</table>", start)
    point = B.value("derived.change.v5.S_MAE", "P55", option="exact")
    doctored = re.sub(r"(<th scope=\"row\">Point-error score</th><td[^>]*>.*?</td><td[^>]*>).*?(</td>)",
                      lambda m: m.group(1) + point + m.group(2), page[start:end], count=1, flags=re.S)
    assert doctored != page[start:end]
    assert _ratio_table_problems(page[:start] + doctored + page[end:])


def test_negative_control_an_unknown_option_on_a_derived_record_refuses():
    with pytest.raises(RC.ClaimError):
        RC.render_template("P55", "{r:derived.change.v5.S_MAE|cixact}")


@pytest.mark.parametrize("text", [
    "v5 was adopted at its 95% decision level",
    "the rule decided at 95%",
])
def test_negative_controls_w47_a_95_percent_decision_interval_is_caught(text):
    assert any(f.startswith("W47") for f in RC.withheld_findings(text))


def test_no_surface_carries_cp24s_withheld_claims(page):
    readme = README.read_text()
    for name, text in (("page", _text(page)), ("readme", readme)):
        found = [f for f in RC.withheld_findings(text) if f[:3] in ("W42", "W43", "W44", "W45", "W46", "W47")]
        assert found == [], (name, found)


@pytest.mark.parametrize("text, wid", [
    ("distributional neural networks do not work for prices", "W42"),
    ("v5 is as good as v4 on the interval score", "W43"),
    ("the quantiles PyTorch produced", "W44"),
    ("try the v5 demo", "W45"),
    ("the gate showed an improvement", "W46"),
])
def test_negative_controls_cp24s_withheld_claims_are_caught(text, wid):
    assert any(f.startswith(wid) for f in RC.withheld_findings(text))


def test_the_v5_chapter_fills_the_grammar_with_both_intervals_and_the_limits(page):
    slots = B.v5_slots()
    assert B.slot_problems(slots) == []
    rows = [row.record_id for panel in slots.chart.panels for row in panel.rows]
    assert rows == ["cp24.uncertainty.v5-HGL.equal_fold.MAE", "cp24.uncertainty97_5.v5-HGL.equal_fold.MAE",
                    "cp24.uncertainty.v5-HGL.equal_fold.WIS", "cp24.uncertainty97_5.v5-HGL.equal_fold.WIS"]
    chapter = _chapter(page, "v5")
    reading = chapter[:chapter.index('data-slot="details"')]
    for key in ("v5.caveat.coverage", "v5.caveat.class", "v5.caveat.alone", "v5.decision", "v5.reading",
                "v5.chart_headline"):
        assert f'data-block="{key}"' in reading, key
    for key in ("v5.leakage", "v5.controls", "v5.rule", "v5.method.arms", "v5.method.arms_lightgbm", "v5.folds"):
        assert f'data-block="{key}"' in chapter, key
    assert "descriptive, never eligible" in _text(chapter) and "never eligible for adoption" in _text(reading)
    # the editorial review's repairs: DDNN-2 alone with its intervals, descriptive; the leakage route visible
    alone = _text(reading[reading.index('data-block="v5.caveat.alone"'):])
    assert "lower, that is better" in alone and "Descriptive only" in alone and alone.count("[") >= 2
    assert 'href="#v5-leakage"' in reading and 'id="v5-leakage"' in chapter
    assert 'id="v5-ratio-values"' in chapter and "View the change as a share of v4" in _text(chapter)
    assert 'id="v5-rule"' in chapter and 'href="#v5-c2a-values"' not in chapter


def test_every_test_period_favours_v5_as_the_folds_block_says():
    """The block's sentence is checked against the ten committed per-fold rows, not typed: every 95% interval of
    v5 − v4, in MAE and WIS, lies wholly below zero."""
    rows = [R.get(f"cp24.uncertainty.v5-HGL.{fold}.{metric}") for fold in B.FOLDS for metric in ("MAE", "WIS")]
    assert all(row.ci_high < 0 for row in rows) and len(rows) == 10
    assert "Every test period favours" in RC.render("v5.folds", "md")


def test_negative_control_a_fold_above_zero_would_contradict_the_folds_block():
    rows = [R.get(f"cp24.uncertainty.v5-HGL.{fold}.MAE") for fold in B.FOLDS]
    doctored = [dataclasses.replace(rows[0], ci_high_raw="0.01")] + rows[1:]
    assert not all(row.ci_high < 0 for row in doctored)


def test_the_branch_cards_carry_question_comparator_result_and_dated_reason(page):
    lineage = page[page.index('id="journey"'):page.index('id="chapters"')]
    assert "Experiments not adopted between v4 and v5" in _text(lineage)
    for ident, checkpoint, month in (("pooled-lightgbm-member-for-v4", "CP-22", "October 2026"),
                                     ("ddnn-member-on-v4", "CP-23", "October 2026")):
        entry = G.get(ident)
        card = lineage[lineage.index(f'id="{entry.anchor[1:]}"'):]
        card = card[:card.index("</li>")]
        assert ">Not adopted<" in card and month in _text(card) and entry.status.date == "2026-10-04"
        for part in ("question", "result", "reason"):
            assert f'data-block="branch.{ident}.{part}"' in card
        assert "v4" in _text(RC.render(f"branch.{ident}.question", "md"))
        assert entry.checkpoint == checkpoint and entry.after == "v4" and entry.comparator == "v4"
    deciding = {"pooled-lightgbm-member-for-v4": ("cp22.uncertainty.R-HGL.fold_4.MAE", "cp22.uncertainty.M-HGL.fold_4.MAE"),
                "ddnn-member-on-v4": ("cp23.uncertainty.v5-HGL.fold_3.MAE",)}
    for ident, records in deciding.items():
        template = RC.BLOCKS_BY_KEY[f"branch.{ident}.result"].template
        for record_id in records:
            assert record_id in template and R.get(record_id).ci_low > 0, record_id  # decisively worse


def test_the_readme_follows_the_registry():
    readme = README.read_text()
    research = readme[readme.index(readme_research.START):readme.index(readme_research.END)]
    assert research.index("### v5 · DDNN-2 added") < research.index("### v4 · three-block LightGBM added")
    assert "### Experiments not adopted between v4 and v5" in research
    assert "#### Pooled LightGBM member for v4" in research and "#### DDNN member on v4" in research
    assert RC.render("v5.caveat.coverage", "md") in research
    assert readme_research.build_block() in readme


# --------------------------------------------------------------------------- the historical sections and the encoding


#: The published PRES-3 page's sections, by SHA-256 (the page Pages served on 2026-10-10, 8a1fedd8...): v5 adds its own
#: chapter and transition and never rewrites an earlier one. The PRES-2 sections are held by test_45.
PUBLISHED_SECTIONS = {
    r'<article class="chapter" id="v4".*?</article>': "55b88aedc129c8184b8ae1358f65c7dae3a6ccb4b2fd3fa09496f3db68ff3e03",
    r'<article class="transition" id="transition-v3-v4".*?</article>':
        "ff697293ca095063cf8c3193d678df2fffab7f9615be2d147bd81e5e226056b3",
}


@pytest.mark.parametrize("pattern", sorted(PUBLISHED_SECTIONS))
def test_every_historical_section_is_byte_identical_to_the_published_page(page, pattern):
    section = re.search(pattern, page, re.DOTALL).group(0)
    assert hashlib.sha256(section.encode()).hexdigest() == PUBLISHED_SECTIONS[pattern]


def test_the_encoding_is_the_owners():
    assert B.TOKENS["v5"] == "#BE123C"
    assert B.ROLE_STYLE["v5"] == {"color": "#BE123C", "marker": "pentagon", "filled": True}
    assert B.marker_problems() == []
    assert B.contrast(B.TOKENS["v5"], B.TOKENS["surface"]) >= 4.5 and B.contrast(B.TOKENS["v5"], B.TOKENS["canvas"]) >= 4.5
    mark = B.marker(0, 0, "v5")
    assert mark.count("<polygon") == 2 and len(re.findall(r"-?\d+\.\d,-?\d+\.\d", mark)) == 10
    legend = B.legend(("v5",))
    assert ">v5</span>" in legend and "#BE123C" in legend


def test_negative_control_v5_sharing_a_shape_is_caught():
    styles = {**B.ROLE_STYLE, "v5": {**B.ROLE_STYLE["v5"], "marker": "diamond"}}
    assert any("v5 shares its marker shape" in problem for problem in B.marker_problems(styles))


def test_the_page_fits_the_budget_without_compaction(page):
    assert len(page.encode()) <= 2_000_000
    for version in ("v2", "v3"):
        assert f'<article class="chapter" id="{version}"' in page


# --------------------------------------------------------------------------- planned work (the Owner's programme plan)


FORBIDDEN = re.compile(r"TabPFN|tabular foundation model|in-house|4\.6 · DDNN", re.IGNORECASE)


def planned_problems(surfaces: dict[str, str], comparator: str) -> list[str]:
    """The planned list after PRES-4: 4.6 gone; a re-evaluation on every eligible day and new input data added; the
    wind and solar item source-neutral; 4.8 and 4.7T kept; no TabPFN; the comparator the registry's generation."""
    problems = []
    for name, text in surfaces.items():
        planned = text
        if name == "page":
            start = text.index('id="planned"')
            planned = _text(text[start:text.index("</section>", start)])
        for match in FORBIDDEN.finditer(planned):
            problems.append(f"{name}: {match.group(0)!r}")
    page = surfaces.get("page", "")
    if page:
        start = page.index('id="planned"')
        section = _text(page[start:page.index("</section>", start)])
        for item in ("A re-evaluation on every eligible day", "New input data", "fuel and carbon prices",
                     "neighbouring markets", "earlier forecasts that already cover the delivery day",
                     "Wind and solar generation forecasts", "Combining models", "4.8 · Recombination",
                     "4.7T and live · Final evaluation"):
            if item not in section:
                problems.append(f"page: {item!r} is not planned")
        if "4.6" in section or "DDNN" in section:
            problems.append("page: 4.6 is still planned")
        if f"compared with {comparator} on the same days" not in section:
            problems.append(f"page: the section's comparator is not {comparator}")
    return problems


def _generated_surfaces() -> dict[str, str]:
    readme = README.read_text()
    blocks = "".join(readme[readme.index(start):readme.index(end)] for start, end in (
        (readme_research.GLANCE_START, readme_research.GLANCE_END), (readme_research.START, readme_research.END)))
    return {"page": PAGE.read_text(), "readme": blocks, **{name: (REPO_ROOT / name).read_text() for name in CARDS}}


def test_the_planned_list_follows_the_programme_plan_on_every_generated_surface():
    assert planned_problems(_generated_surfaces(), G.current_generation().version) == []
    items = [(name, item) for name, item, *_ in B.planned_items()]
    assert items == [("A re-evaluation on every eligible day", ""), ("New input data", ""),
                     ("Wind and solar generation forecasts", "4.4V"), ("Combining models", "4.8"),
                     ("Frozen-protocol evaluation, then prospective monitoring", "4.7T and live")]
    kept = {item: (name, code, question, evidence) for name, item, code, question, evidence in B.PLANNED_WORK}
    assert kept["4.8"] == ("Combining models", "Recombination", "Does combining adopted models help?",
                           "A predefined combination test")
    assert kept["4.7T and live"] == (
        "Frozen-protocol evaluation, then prospective monitoring", "Final evaluation",
        "How does the selected model perform under a frozen evaluation protocol, and then prospectively?",
        "An evaluation window and an evidence classification, both fixed in the protocol before the test")


@pytest.mark.parametrize("doctored, expected", [
    (lambda s: s.replace("A re-evaluation on every eligible day</p>", "A distributional neural network</p>", 1),
     "is not planned"),
    (lambda s: s.replace("Does a wind and solar generation", "Does an in-house wind and solar generation", 1), "in-house"),
    (lambda s: s.replace("4.4V</span> · VRE", "4.6</span> · DDNN", 1), "4.6"),
    (lambda s: s.replace('compared with <span data-structural="version">v5</span> on the same days',
                         'compared with <span data-structural="version">v4</span> on the same days'), "is not v5"),
    (lambda s: s.replace("neighbouring markets", "TabPFN", 1), "TabPFN"),
])
def test_negative_controls_a_stale_planned_list_is_caught(doctored, expected):
    surfaces = _generated_surfaces()
    surfaces["page"] = doctored(surfaces["page"])
    assert any(expected in problem for problem in planned_problems(surfaces, "v5"))


# --------------------------------------------------------------------------- the MLflow export (step 17)


@pytest.mark.parametrize("key", ["cp22", "cp23", "cp24"])
def test_each_final_export_equals_its_draft_apart_from_the_pending_fields(key):
    report = E.later_final_vs_draft(key)
    assert report["equal_apart_from_pending"], report["differences"]
    if key == "cp24":
        assert set(report["chart_artifacts_added"]) == {"cp24/v5"}
        assert set(report["renamed_fields"]) == {f"{run}: {field}" for run in ("cp24", "cp24/v5") for field in (
            "run_name", "tag delu.public_name", "tag mlflow.note.content", "artifact summary.json", "artifact README.md")}
    else:
        assert report["chart_artifacts_added"] == {} and report["renamed_fields"] == []


@pytest.mark.parametrize("change, expected", [
    (lambda run: run["metrics"]["s_mae"][0].update(value=0.5), "metrics"),
    (lambda run: run["params"].update(seed="1"), "params"),
    (lambda run: run["tags"].update({"delu.kind": "branch"}), "tag delu.kind"),
])
def test_negative_controls_a_final_export_that_differs_beyond_the_pending_fields(change, expected):
    files = E.build_export()
    change(next(run for run in files["cp24"]["runs"] if run["run_key"] == "cp24/v5"))
    report = E.later_final_vs_draft("cp24", files)
    assert not report["equal_apart_from_pending"] and any(expected in item for item in report["differences"])


def test_no_previously_published_record_changes():
    if not _has(PUBLISHED_REF):
        pytest.skip("the published export's commit is not in this checkout")
    report = E.diff_exports(E.export_at(PUBLISHED_REF), E.build_export())
    assert report["only_identity"] and report["identity_changes"] == {} and report["substantive_changes"] == []
    assert sorted(report["runs_added"]) == sorted(key for key in G.expected_run_keys()
                                                 if key.split("/")[0] in ("cp22", "cp23", "cp24"))
    assert report["experiment_tag_changes"] == ["mlflow.note.content"]


def test_the_experiment_description_names_every_parent():
    note = E.EXPERIMENT_TAGS["mlflow.note.content"]
    for checkpoint in G.CHECKPOINTS.values():
        assert G.mlflow_run_name(checkpoint.run_key) in note
    assert note.count(" (CP-") == len(G.CHECKPOINTS)


# --------------------------------------------------------------------------- the publisher's authorized writes


class _Client:
    def __init__(self, tags: dict, runs: dict[str, dict | None]):
        self.experiment = SimpleNamespace(experiment_id="1", tags=tags)
        self.runs = runs

    def get_experiment_by_name(self, name):
        return self.experiment

    def search_runs(self, experiment_ids, filter_string, max_results):
        key = re.search(r"= '([^']+)'", filter_string).group(1)
        tags = self.runs.get(key)
        return [] if tags is None else [SimpleNamespace(data=SimpleNamespace(tags=tags), info=SimpleNamespace(run_id=key))]


AUTHORIZED = tuple(key for key in G.expected_run_keys() if key.split("/")[0] in ("cp22", "cp23", "cp24"))
DESCRIPTION = ("mlflow.note.content",)


def _published() -> dict[str, dict | None]:
    return {key: None if key in AUTHORIZED else {"delu.upload_state": "complete",
                                                 **({"delu.package_complete": "true"} if "/" not in key else {})}
            for key in G.expected_run_keys()}


def _old_tags() -> dict:
    return {**E.EXPERIMENT_TAGS, "mlflow.note.content": "the description published on 2026-09-28"}


def test_the_write_plan_admits_exactly_the_authorized_runs_and_the_description():
    plan = P.write_plan(_Client(_old_tags(), _published()), {key: {} for key in G.expected_run_keys()}, AUTHORIZED,
                        DESCRIPTION)
    assert plan["to_write"] == sorted(AUTHORIZED) and len(AUTHORIZED) == 16
    assert plan["experiment_tags_to_write"] == ["mlflow.note.content"]


@pytest.mark.parametrize("client, tags, expected", [
    (lambda: _Client(_old_tags(), _published()), (), "experiment tag mlflow.note.content"),
    (lambda: _Client({**_old_tags(), "mlflow.experimentKind": "other"}, _published()), DESCRIPTION,
     "experiment tag mlflow.experimentKind"),
    (lambda: _Client(_old_tags(), {**_published(), "cp21/HGL": {"delu.upload_state": "incomplete"}}), DESCRIPTION,
     "run cp21/HGL"),
])
def test_negative_controls_any_other_write_refuses_before_writing(client, tags, expected):
    with pytest.raises(P.Refused, match=expected):
        P.write_plan(client(), {key: {} for key in G.expected_run_keys()}, AUTHORIZED, tags)


# --------------------------------------------------------------------------- the Space, unchanged


def test_both_space_cards_are_byte_identical_to_pres3s():
    import build_space
    import build_wasm_space

    for name, digest in CARDS.items():
        assert hashlib.sha256((REPO_ROOT / name).read_bytes()).hexdigest() == digest, name
    assert build_space.build_card() == (REPO_ROOT / "space" / "README.md").read_text()
    assert build_wasm_space.build_card() == (REPO_ROOT / "space-wasm" / "README.md").read_text()
    assert "v5" not in (REPO_ROOT / "space-wasm" / "README.md").read_text()
