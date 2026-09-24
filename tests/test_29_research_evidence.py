"""Presentation plan §9.5: every research record re-derives from its committed source row.

This is the proof of provenance. Every number a public surface renders about CP-10, CP-15, CP-16
or CP-20 is an `EvidenceRecord`, and each record must still be the exact text of one cell in one
committed row of a file whose bytes hash to the blob its evidence tag preserves. The negative
controls corrupt a copy of a record -- the wrong row, policy, aggregation, unit or revision --
and require the check to fail.
"""

from __future__ import annotations

import dataclasses
import subprocess

import pytest

from delu_forecast import research as R


@pytest.fixture(scope="module")
def registry():
    return R.records()


def test_every_record_rederives_from_its_committed_row(registry):
    problems = R.validate_all(registry.values())
    assert not problems, "records that no longer match their source:\n  " + "\n  ".join(problems[:20])
    assert len(registry) > 8000, "the registry is suspiciously small"


def test_every_source_is_the_blob_its_evidence_tag_preserves():
    for path in R.SOURCES:
        R.check_source(path)


def test_the_recorded_blobs_match_the_tags_where_the_tags_exist():
    """CI's shallow checkout has no tags, so this cross-check runs only where they resolve."""
    checked = 0
    for path, source in R.SOURCES.items():
        result = subprocess.run(
            ["git", "rev-parse", "-q", "--verify", f"{source.tag}:{path}"],
            cwd=R.REPO_ROOT, capture_output=True, text=True,
        )
        if result.returncode != 0:
            continue
        assert result.stdout.strip() == source.blob, f"{path} differs from {source.tag}"
        checked += 1
    if checked == 0:
        pytest.skip("no evidence tags in this checkout (shallow CI clone); blobs are checked from bytes")


def test_the_blob_function_is_git_s():
    assert R.blob_sha(b"") == "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"
    assert R.blob_sha(b"hello\n") == "ce013625030ba8dba906f756967f9e9ca394464a"


# -- the cross-checkpoint identities the page relies on -----------------------


REFERENCES = ("B0", "B1", "B2", "B3", "A1")


@pytest.mark.parametrize("policy", REFERENCES)
@pytest.mark.parametrize("score", ("S_MAE", "S_WIS"))
def test_references_are_identical_across_cp15_cp16_and_cp20(policy, score):
    cp15 = R.get(f"cp15.relative_scores.{policy}.{score}").raw
    cp16 = R.get(f"cp16.metrics.{policy}.equal_fold.{score}").raw
    cp20 = R.get(f"cp20.metrics.{policy}.equal_fold.{score}").raw
    assert float(cp15) == float(cp16) == float(cp20), (policy, score, cp15, cp16, cp20)


@pytest.mark.parametrize("scope", ("equal_fold", "pooled", "fold_1", "fold_2", "fold_3", "fold_4", "fold_5"))
def test_cp20_h0_is_cp16_v2_h(scope):
    fields = ("S_MAE", "S_WIS") if scope == "equal_fold" else ("MAE", "WIS", "coverage95", "mean_width95")
    for field in fields:
        h0 = R.get(f"cp20.metrics.H0.{scope}.{field}").raw
        v2h = R.get(f"cp16.metrics.V2-H.{scope}.{field}").raw
        assert h0 == v2h, (scope, field, h0, v2h)


def test_the_crisis_window_hits_agree_with_the_criterion_coverage():
    """C4 takes v2/v3 hit counts from the diagnostics rows and MAE from criterion 4; they must agree."""
    for policy in ("H0", "HG"):
        hits = R.get(f"cp20.diagnostics.{policy}.peak.hit_count95").value
        hours = R.get(f"cp20.diagnostics.{policy}.peak.n_hours").value
        coverage = R.get(f"cp20.criteria.{policy}.c4.peak.coverage95").value
        assert round(coverage * hours) == hits
        assert R.get(f"cp20.criteria.{policy}.c4.peak.MAE").raw == R.get(f"cp20.diagnostics.{policy}.peak.MAE").raw
    assert R.get("cp15.peak.B1.hit_count95").value == R.get("cp20.diagnostics.B1.peak.hit_count95").value


def test_v1s_pooled_error_is_the_same_in_its_report_and_here():
    """The F07 note says v1's own MAE is the same in both records."""
    report = R.get("cp2.development_pooled_metrics.base.final.MAE")
    here = R.get("cp20.metrics.B1.pooled.MAE")
    assert R.display(report) == R.display(here)
    assert R.get("cp2.dm_development.point_vs_naive.n_days").raw == R.get("cp20.metrics.B1.pooled.n_days").raw.split(".")[0]


def test_the_exact_endpoint_is_printed_in_full():
    record = R.get("cp16.uncertainty.V2-H-V2-P.equal_fold.MAE")
    assert record.ci_high_raw == "3.857628092332211e-06"
    assert R.display(record, "ci_high", style="exact") == "+0.000003857628092332211"
    assert R.exact("-0.057") == "-0.057"


def test_no_v2_or_later_record_reaches_past_the_development_boundary(registry):
    """Plan §6 invariant 10: no v2+ metric uses data after 2026-04-07."""
    late = [
        record.record_id
        for record in registry.values()
        if record.checkpoint in ("CP-15", "CP-16", "CP-20") and record.window
        and record.window[1] > R.EVIDENCE_BOUNDARY
    ]
    assert not late, late[:10]


def test_every_record_declares_its_unit_population_and_class(registry):
    for record in registry.values():
        assert record.unit and record.population_id and record.evidence_class, record.record_id
        base = record.population_id.split("/")[0]
        assert base in R.POPULATIONS, record.population_id
        if record.interval is not None:
            assert record.interval.level == 0.95 and record.interval.replicates == 2000
            assert record.interval.seed == 15042 and record.interval.block_days == 7


def test_the_display_rule_never_shows_a_small_endpoint_as_zero():
    fold3 = R.get("cp20.uncertainty.HG-H0.fold_3.MAE")
    assert R.display(fold3, "ci_high") == "+0.037"
    assert R.display(R.get("cp20.metrics.HG.pooled.n_hours")) == "10,747"
    assert R.display(R.get("cp20.uncertainty.HG-H0.equal_fold.MAE")).startswith(R.MINUS)


def test_daily_series_skip_days_without_hours():
    for checkpoint, policy in (("CP-15", "B0"), ("CP-16", "V2-H"), ("CP-20", "HG")):
        series = R.daily_series(checkpoint, policy)
        assert len(series) == 448, (checkpoint, policy, len(series))
        assert all(point.n_hours > 0 for point in series)
        assert [point.delivery_date for point in series] == sorted(point.delivery_date for point in series)


# -- negative controls: each corruption must be caught ------------------------


def _fails(record) -> str:
    with pytest.raises(R.EvidenceError) as caught:
        R.validate(record)
    return str(caught.value)


def test_negative_control_wrong_row():
    record = R.get("cp20.metrics.HG.fold_3.MAE")
    wrong = dataclasses.replace(record, selector=(("policy", "HG"), ("scope", "per_fold"), ("fold", "fold_4")))
    assert "committed value" in _fails(wrong)


def test_negative_control_wrong_policy():
    record = R.get("cp20.metrics.HG.equal_fold.S_MAE")
    wrong = dataclasses.replace(record, selector=(("policy", "H0"), ("scope", "equal_fold"), ("fold", "all")))
    assert _fails(wrong)
    relabelled = dataclasses.replace(record, policy_code="H0")
    assert "policy" in _fails(relabelled)


def test_negative_control_wrong_aggregation():
    record = R.get("cp20.metrics.HG.pooled.MAE")
    assert "aggregation" in _fails(dataclasses.replace(record, aggregation="equal_fold"))


def test_negative_control_wrong_unit():
    record = R.get("cp20.uncertainty.HG-H0.fold_3.MAE")
    assert "unit" in _fails(dataclasses.replace(record, unit=R.UNIT_NORM_DIFF))
    score = R.get("cp20.metrics.HG.equal_fold.S_MAE")
    assert "unit" in _fails(dataclasses.replace(score, unit=R.UNIT_EUR))


def test_negative_control_wrong_revision(monkeypatch):
    record = R.get("cp20.metrics.HG.equal_fold.S_MAE")
    source = R.SOURCES[record.source_path]
    monkeypatch.setitem(R.SOURCES, record.source_path, dataclasses.replace(source, blob="0" * 40))
    assert "has changed" in _fails(record)


def test_negative_control_wrong_value_and_interval():
    record = R.get("cp20.uncertainty.HG-H0.equal_fold.MAE")
    assert "committed value" in _fails(dataclasses.replace(record, raw="-0.0783"))
    assert "interval" in _fails(dataclasses.replace(record, ci_high_raw="-0.05"))


def test_negative_control_an_unregistered_source():
    record = R.get("cp20.metrics.HG.equal_fold.S_MAE")
    assert "not a registered" in _fails(dataclasses.replace(record, source_path="reports/cp3/link_check.json"))
