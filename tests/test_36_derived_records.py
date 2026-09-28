"""Publication Standard v1 §3.3 (brief W3): the headline quantities are typed derived records.

Each record is computed from committed rows, re-derived here, and mapped in the claim maps. The
standard's Appendix re-derives exactly, and a perturbed source row fails -- whether the change is
caught by the file's recorded blob or, with the blob rewritten, by the recomputation itself.
"""

from __future__ import annotations

import re
import subprocess

import pytest

from delu_forecast import derived as D
from delu_forecast import registry as G
from delu_forecast import research as R
from delu_forecast import research_claims as RC
from delu_forecast.claims import REPO_ROOT


def show(record_id: str, which: str = "value", style: str | None = None) -> str:
    return D.display(D.get(record_id), which, style=style)


def interval(record_id: str) -> str:
    return f"{show(record_id)} [{show(record_id, 'ci_low')}, {show(record_id, 'ci_high')}]"


# --------------------------------------------------------------------------- the Appendix, exactly


def test_the_distance_from_daily_lear_rederives_exactly():
    assert (show("derived.criteria.v3.distance.S_MAE"), show("derived.criteria.v3.distance.S_WIS")) == ("−14%", "−17%")
    assert (show("derived.criteria.v2.distance.S_MAE"), show("derived.criteria.v2.distance.S_WIS")) == ("−2%", "−4%")


def test_the_change_against_v2_rederives_exactly_with_its_fixed_denominator_interval():
    assert interval("derived.change.v3.S_MAE") == "−12% [−16%, −9%]"
    assert interval("derived.change.v3.S_WIS") == "−14% [−17%, −11%]"


def test_the_per_period_ranges_rederive_exactly():
    def ranged(subject):
        return (f"{show(f'derived.periods.{subject}.ordinary_low')}–{show(f'derived.periods.{subject}.ordinary_high')}",
                show(f"derived.periods.{subject}.stress"))
    assert ranged("v3") == ("5.3–15.6", "48.0")
    assert ranged("naive") == ("8.6–30.5", "86.9")
    assert ranged("v2") == ("6.3–18.7", "51.2")
    assert ranged("daily-lear") == ("6.2–19.2", "54.0")


def test_n_is_eight_and_v3_is_the_only_and_first_policy_to_meet_the_targets():
    assert show("derived.criteria.v3.tested") == "8"
    verdicts = {record.subject: record.value for record in D.records().values() if record.kind == "verdict"}
    assert len(verdicts) == 8, "one identity, one verdict: v2 is not counted twice (V2-H = H0)"
    assert [subject for subject, verdict in verdicts.items() if verdict == "met"] == ["v3"]
    assert show("derived.criteria.v3.first_to_meet") == "yes"
    assert [record.subject for record in D.records().values()
            if record.kind == "first_to_meet" and record.value == "yes"] == ["v3"]


def test_the_rule_margin_is_ten_percent_on_both_scores():
    assert show("derived.rule.margin.S_MAE") == show("derived.rule.margin.S_WIS") == "10%"


def test_the_rule_was_set_on_2026_09_15_and_its_text_is_the_attempt_1_anchors():
    assert show("derived.rule.set_on") == "2026-09-15" == G.RULES["criteria-1-2"].set_on
    anchor = (REPO_ROOT / "capstone_v21.md").read_text()
    attempt_1 = (REPO_ROOT / "reports/cp15/attempt-1/capstone_v21.md").read_text()
    assert D.RULE_DATE_LINE in anchor and D.RULE_DATE_LINE in attempt_1
    assert D.section_8(anchor) == D.section_8(attempt_1)
    assert "S_MAE(m) is at most 0.90 times the lowest S_MAE among B0–B3." in D.section_8(anchor)


def _git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True, text=True)


def test_the_preregistration_preceded_the_results_where_history_is_available():
    """The provenance records in Git (the committed CI checkout is shallow and carries no tags)."""
    if _git("cat-file", "-e", "bb5e67882fcfdf65b963d25ce785a3999816dfc2^{commit}").returncode != 0:
        pytest.skip("Git history is not available in this checkout (shallow CI clone)")
    registered = _git("show", "-s", "--format=%cI", "bb5e678").stdout.strip()
    results = _git("show", "-s", "--format=%cI", "0be8e56").stdout.strip()
    assert registered == "2026-09-16T00:17:04+03:00"
    assert results > registered
    at_registration = _git("show", "bb5e678:capstone_v21.md").stdout
    assert D.section_8(at_registration) == D.section_8((REPO_ROOT / "capstone_v21.md").read_text())
    if _git("rev-parse", "-q", "--verify", "refs/tags/evidence/cp-15").returncode == 0:
        assert _git("merge-base", "--is-ancestor", "bb5e678", "evidence/cp-15").returncode == 0


def test_the_stress_period_is_the_one_the_protocol_names():
    assert D.stress_period() == "fold_3"
    assert show("derived.periods.stress_period") == "fold_3"
    assert R.get("cp20.metrics.B0.fold_3.MAE").window == ("2022-07-01", "2022-09-28")


# --------------------------------------------------------------------------- provenance and binding


def test_every_derived_record_rederives_from_a_fresh_read():
    assert D.validate_all() == []


def test_every_derived_record_names_committed_inputs_and_a_mapped_claim():
    mapped = RC.claim_map_ids()
    for record in D.records().values():
        assert record.claim in mapped, record.record_id
        for record_id in record.inputs:
            R.get(record_id)
        for path in record.sources:
            if "/" in path or path.endswith(".md"):
                assert (REPO_ROOT / path.split(":")[0].split(" ")[0]).exists() or " " in path, path


def test_no_v2_or_later_derived_value_reaches_past_the_development_boundary():
    for record in D.records().values():
        for record_id in record.inputs:
            window = R.get(record_id).window
            assert window is None or window[1] <= R.EVIDENCE_BOUNDARY, (record.record_id, record_id)


def test_derived_values_render_bound_to_their_record():
    html = RC.render_template("P16", "{r:derived.criteria.v3.distance.S_MAE|abs} below; {r:derived.change.v3.S_MAE|ci}")
    assert 'data-record="derived.criteria.v3.distance.S_MAE"' in html and ">14%<" in html
    assert html.count("data-derived=") == 3
    assert RC.render_template("P16", "{r:derived.change.v3.S_MAE}", "md") == "−12%"


# --------------------------------------------------------------------------- negative controls


def _perturbed(monkeypatch, path: str, old: str, new: str, *, rewrite_blob: bool) -> None:
    D.records(), R.records()  # the published records are built from the unperturbed rows
    original = R.source_bytes(path)
    assert original.count(old.encode()) == 1
    changed = original.replace(old.encode(), new.encode())
    real = R.source_bytes
    monkeypatch.setattr(R, "source_bytes", lambda p: changed if p == path else real(p))
    if rewrite_blob:
        source = R.SOURCES[path]
        monkeypatch.setitem(R.SOURCES, path, R.Source(source.path, source.tag, R.blob_sha(changed)))


def test_negative_control_a_perturbed_source_row_fails_its_recorded_blob(monkeypatch):
    _perturbed(monkeypatch, "reports/weather-ablation/metrics.csv", "0.5657606376333641", "0.5957606376333641",
               rewrite_blob=False)
    problems = D.validate_all()
    assert any("derived.criteria.v3" in problem and "has changed" in problem for problem in problems), problems


def test_negative_control_a_perturbed_source_row_fails_its_recomputation(monkeypatch):
    """Even with the blob rewritten to match, the recomputed distance no longer equals the record."""
    _perturbed(monkeypatch, "reports/weather-ablation/metrics.csv", "0.5657606376333641", "0.5957606376333641",
               rewrite_blob=True)
    problems = D.validate_all()
    assert any(problem.startswith("derived.criteria.v3.distance.S_MAE") for problem in problems), problems


def test_negative_control_a_perturbed_interval_endpoint_fails(monkeypatch):
    _perturbed(monkeypatch, "reports/weather-ablation/uncertainty.csv", "-0.05703087928591252", "-0.04703087928591252",
               rewrite_blob=True)
    assert any(problem.startswith("derived.change.v3.S_MAE: interval") for problem in D.validate_all())


def test_negative_control_a_moved_rule_date_fails(monkeypatch):
    real = type(REPO_ROOT).read_text

    def read_text(self, *args, **kwargs):
        text = real(self, *args, **kwargs)
        return text.replace(D.RULE_DATE_LINE, D.RULE_DATE_LINE.replace("09-15", "09-17")) if self.name == "capstone_v21.md" else text

    monkeypatch.setattr(type(REPO_ROOT), "read_text", read_text)
    assert any(problem.startswith("derived.rule.set_on") for problem in D.validate_all())


def test_display_never_rounds_a_whole_percent_across_the_sign():
    assert re.fullmatch(r"−\d+%", show("derived.change.v3.S_MAE", "ci_high"))
