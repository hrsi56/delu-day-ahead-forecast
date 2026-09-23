"""Synthetic-only CP-16 score and frozen bootstrap controls."""
import numpy as np
import pandas as pd
import pytest

from cp16.scoring import (
    BOOTSTRAP_REPLICATES, BOOTSTRAP_SEED, FOLDS, FOLD_WINDOWS, POLICIES,
    QUANTILES, _bootstrap, _conclusions, _evaluate, _indices, _selection, _tables,
    evaluate, score_hourly, validate_predictions,
)


@pytest.fixture(scope="module")
def predictions():
    records = []
    for fold, (start, end) in FOLD_WINDOWS.items():
        for day in pd.date_range(start, end):
            if fold == "fold_3" and day.day == 20 and day.month == 8:
                continue
            for hour in (1, 7, 12, 20, 23):
                for i, policy in enumerate(POLICIES):
                    center = float(2 + i / 10)
                    row = dict(policy=policy, fold=fold, delivery_date=day,
                               timestamp_utc=(day + pd.Timedelta(hours=hour)).tz_localize("Europe/Berlin").tz_convert("UTC"),
                               central=3., scale=2., y_true=0.)
                    row.update(zip(QUANTILES, [center - 10, center - 5, center - 2,
                                               center, center + 2, center + 5, center + 10]))
                    records.append(row)
    return pd.DataFrame(records)


def expected(frame):
    return frame.loc[frame.policy.eq("B0"), ["fold", "timestamp_utc", "delivery_date", "y_true"]]


def test_validation_positive_preserves_inputs_and_production_counts(predictions):
    original = predictions.copy(deep=True)
    validated = validate_predictions(predictions, expected(predictions), production=False)
    pd.testing.assert_frame_equal(predictions, original)
    assert len(validated) == len(predictions)
    with pytest.raises(ValueError, match="10,747"):
        evaluate(predictions, expected(predictions))
    assert BOOTSTRAP_REPLICATES == 2000 and BOOTSTRAP_SEED == 15042


@pytest.mark.parametrize("defect", ["missing", "crossing", "infinite", "duplicate", "date", "truth", "scale", "parity", "policy", "common_deletion"])
def test_reject_invalid_population(predictions, defect):
    bad = predictions.copy(deep=True)
    if defect == "missing":
        bad.loc[0, "p10"] = np.nan
    elif defect == "crossing":
        bad.loc[0, "p10"] = 100
    elif defect == "infinite":
        bad.loc[0, "y_true"] = np.inf
    elif defect == "duplicate":
        bad = pd.concat([bad, bad.iloc[[0]]])
    elif defect == "date":
        bad.loc[0, "delivery_date"] += pd.Timedelta(days=1)
    elif defect == "truth":
        bad.loc[0, "y_true"] = 100
    elif defect == "scale":
        bad.loc[0, "scale"] = 0
    elif defect == "parity":
        bad.loc[bad.policy.eq("V2-H"), "central"] += 1
    elif defect == "policy":
        bad.loc[bad.policy.eq("V2-H"), "policy"] = "A2"
    else:
        bad = bad.loc[~bad.timestamp_utc.eq(bad.iloc[0].timestamp_utc)]
    with pytest.raises(ValueError):
        validate_predictions(bad, expected(predictions), production=False)


def test_independent_emitted_wis_oracle():
    row = dict(policy="B0", fold="fold_1", delivery_date=pd.Timestamp("2020-07-01"),
               timestamp_utc=pd.Timestamp("2020-07-01", tz="UTC"), y_true=12., central=3.)
    row.update(zip(QUANTILES, [0., 2., 4., 5., 6., 8., 10.]))
    result = score_hourly(pd.DataFrame([row])).iloc[0]
    # Median .5*7 + weighted widths .25*2+.1*6+.025*10 + misses 6+4+2.
    assert result.WIS == pytest.approx(16.85 / 3.5)
    assert result.absolute_error == 7 and result.raw_central_absolute_error == 9
    assert result.centering_effect == -2 and result.upper_miss95


@pytest.fixture(scope="module")
def evaluation(predictions):
    return _evaluate(predictions, expected(predictions), production=False, replicates=13)


def test_diagnostics_exhaustive_blocks_counts_peak_recovery(evaluation):
    metrics, diagnostics = evaluation["metrics"], evaluation["diagnostics"]
    assert len(metrics) == 49
    for (policy, fold), blocks in diagnostics.loc[diagnostics.scope.eq("block")].groupby(["policy", "fold"]):
        metric = metrics.loc[metrics.policy.eq(policy) & metrics.fold.eq(fold)].iloc[0]
        assert blocks.n_hours.sum() == metric.n_hours
        assert set(blocks.group) == {"night", "solar", "shoulder"}
        assert blocks.hit_count95.sum() == metric.hit_count95
        assert blocks.support_status.eq("eligible").all()
    zero_hours = diagnostics.loc[diagnostics.scope.eq("hour") & diagnostics.group.eq("0")]
    assert len(zero_hours) == 35 and zero_hours.n_hours.eq(0).all()
    assert zero_hours.support_status.eq("support_limited").all()
    peak = diagnostics.loc[diagnostics.scope.eq("peak")]
    assert peak.n_hours.eq(80).all() and peak.n_days.eq(16).all()
    assert peak.calendar_days.eq(17).all() and peak.hit_count95.eq(80).all()
    recovery = diagnostics.loc[diagnostics.scope.eq("recovery")]
    assert len(recovery) == 28 and recovery.n_hours.eq(35).all()
    missing = diagnostics.loc[diagnostics.scope.eq("daily") & diagnostics.delivery_date.eq(pd.Timestamp("2022-08-20"))]
    assert len(missing) == 7 and missing.n_hours.eq(0).all()
    assert missing.MAE.isna().all() and missing.WIS.isna().all()
    assert len(evaluation["uncertainty"]) == 36


def test_support_threshold_56_dates_is_inclusive(predictions):
    local_hour = predictions.timestamp_utc.dt.tz_convert("Europe/Berlin").dt.hour
    days = (predictions.delivery_date - pd.Timestamp("2020-07-01")).dt.days
    remove = predictions.fold.eq("fold_1") & ((local_hour.eq(1) & days.lt(34)) | (local_hour.eq(7) & days.lt(35)))
    scored = score_hourly(predictions.loc[~remove].copy())
    scored["local_hour"] = scored.timestamp_utc.dt.tz_convert("Europe/Berlin").dt.hour
    scored["local_block"] = np.select([scored.local_hour.ge(22) | scored.local_hour.le(5),
                                       scored.local_hour.between(10, 16)], ["night", "solar"], default="shoulder")
    _, diagnostics, _ = _tables(scored)
    part = diagnostics.loc[diagnostics.scope.eq("hour") & diagnostics.fold.eq("fold_1") & diagnostics.policy.eq("V2-H")].set_index("group")
    assert part.loc["1", "n_days"] == 56 and part.loc["1", "support_status"] == "eligible"
    assert part.loc["7", "n_days"] == 55 and part.loc["7", "support_status"] == "support_limited"


def selection_fixture():
    metrics, peaks = [], []
    levels = dict(B0=100., B1=80., B2=60., B3=70., A1=54., **{"V2-H": 54., "V2-P": 54.})
    for policy in POLICIES:
        for fold in FOLDS:
            metrics.append(dict(policy=policy, fold=fold, scope="per_fold", MAE=levels[policy],
                                WIS=levels[policy], coverage95=.90 if fold == "fold_1" else .98))
        peaks.append(dict(policy=policy, scope="peak", MAE=levels[policy], WIS=levels[policy], coverage95=.90))
    return pd.DataFrame(metrics), pd.DataFrame(peaks)


def test_six_criteria_inclusive_limits_and_p_exact_tie():
    metrics, peaks = selection_fixture()
    scores, criteria, ranking = _selection(metrics, peaks)
    assert ranking == ["V2-P", "V2-H"] and criteria.passed.all()
    assert scores["V2-H"]["S_MAE"] == pytest.approx(.54)
    assert set(criteria.criterion) == set(range(1, 7))
    # All six must fail mechanically; original actuals and limits remain.
    metrics.loc[metrics.policy.isin(["V2-H", "V2-P"]), ["MAE", "WIS", "coverage95"]] = [100, 100, .89]
    peaks.loc[peaks.policy.isin(["V2-H", "V2-P"]), ["MAE", "WIS", "coverage95"]] = [100, 100, .89]
    _, criteria, _ = _selection(metrics, peaks, integrity_verified=False)
    for policy in ("V2-H", "V2-P"):
        assert set(criteria.loc[criteria.policy.eq(policy) & ~criteria.passed, "criterion"]) == set(range(1, 7))


def test_rolling_best_is_metric_and_fold_specific_and_rank_wis_first():
    metrics, peaks = selection_fixture()
    metrics.loc[metrics.policy.eq("B2") & metrics.fold.eq("fold_1"), ["MAE", "WIS"]] = [40, 80]
    metrics.loc[metrics.policy.eq("B3") & metrics.fold.eq("fold_1"), ["MAE", "WIS"]] = [80, 50]
    metrics.loc[metrics.policy.eq("V2-H") & metrics.fold.eq("fold_1"), ["MAE", "WIS"]] = [42, 52.5]
    _, criteria, _ = _selection(metrics, peaks)
    selected = criteria.loc[criteria.policy.eq("V2-H") & criteria.criterion.eq(5) & criteria.scope.eq("fold_1")].set_index("metric")
    assert selected.loc["MAE", "upper_limit"] == 42 and selected.loc["WIS", "upper_limit"] == 52.5
    assert selected.passed.all()
    metrics.loc[metrics.policy.eq("V2-H"), ["MAE", "WIS"]] = [80, 30]
    assert _selection(metrics, peaks)[2][0] == "V2-H"


def test_zero_reference_is_unassessed_no_ranking():
    metrics, peaks = selection_fixture()
    metrics.loc[metrics.policy.eq("B0") & metrics.fold.eq("fold_2"), "WIS"] = 0
    _, criteria, ranking = _selection(metrics, peaks)
    assert ranking is None
    assert criteria.loc[criteria.criterion.eq(2), "status"].eq("unassessed").all()


def test_equal_fold_scores_and_peak_best_metric_specific():
    metrics, peaks = selection_fixture()
    metrics.loc[metrics.policy.eq("B0"), "MAE"] = [10, 20, 40, 80, 160]
    metrics.loc[metrics.policy.eq("V2-H"), "MAE"] = [1, 4, 12, 32, 80]
    peaks.loc[peaks.policy.eq("B2"), ["MAE", "WIS"]] = [50, 70]
    peaks.loc[peaks.policy.eq("B3"), ["MAE", "WIS"]] = [70, 40]
    peaks.loc[peaks.policy.eq("V2-H"), ["MAE", "WIS"]] = [50, 40]
    scores, criteria, _ = _selection(metrics, peaks)
    assert scores["V2-H"]["S_MAE"] == pytest.approx(.3)
    part = criteria.loc[criteria.policy.eq("V2-H") & criteria.criterion.eq(4)].set_index("metric")
    assert part.passed.all()
    assert part.loc["MAE", "upper_limit"] == 50 and part.loc["WIS", "upper_limit"] == 40


def daily_fixture():
    rows = []
    for fi, (fold, (start, end)) in enumerate(FOLD_WINDOWS.items()):
        for day_no, day in enumerate(pd.date_range(start, end)):
            count = 0 if day_no == 17 else (23 if day_no % 2 else 25)
            for pi, policy in enumerate(POLICIES):
                value = (1 + fi) + (day_no + 1) * (pi + 1) / 10
                rows.append(dict(policy=policy, fold=fold, delivery_date=day, n_hours=count,
                                 MAE=value if count else np.nan, WIS=value * (pi + 2) if count else np.nan))
    return pd.DataFrame(rows)


def test_bootstrap_independent_scalar_oracle_recomputes_normalizers_and_hours():
    daily, reps = daily_fixture(), 19
    actual, metadata = _bootstrap(daily, replicates=reps)
    rng = np.random.default_rng(15042)
    fold_draws = []
    fold_daily = []
    for fi, fold in enumerate(FOLDS):
        draws, day_draws = [], []
        starts = rng.integers(0, 84, size=(reps, 13))
        for blocks in starts:
            days = [d for b in blocks for d in range(int(b), int(b) + 7)][:90]
            days = [d for d in days if d != 17]
            counts = [23 if d % 2 else 25 for d in days]
            def mean(pi):
                return sum(((1 + fi) + (d + 1) * (pi + 1) / 10) * n for d, n in zip(days, counts)) / sum(counts)
            draws.append((mean(5) - mean(6)) / mean(0))
            day_draws.append(sum(-(d + 1) / 10 for d in days) / len(days))
        fold_draws.append(draws)
        fold_daily.append(day_draws)
    expected = np.percentile(np.mean(fold_draws, axis=0), [2.5, 97.5])
    row = actual.loc[actual.scope.eq("equal_fold") & actual.candidate.eq("V2-H") & actual.baseline.eq("V2-P") & actual.metric.eq("MAE")].iloc[0]
    np.testing.assert_allclose([row.ci_lower, row.ci_upper], expected)
    daily_row = actual.loc[actual.scope.eq("fold_1") & actual.candidate.eq("V2-H") & actual.baseline.eq("V2-P") & actual.metric.eq("MAE")].iloc[0]
    np.testing.assert_allclose([daily_row.ci_lower, daily_row.ci_upper], np.percentile(fold_daily[0], [2.5, 97.5]))
    repeat, again = _bootstrap(daily, replicates=reps)
    pd.testing.assert_frame_equal(actual, repeat)
    assert metadata == again and metadata["shared_index_sets"] == 1


def test_non_circular_indices_and_independent_folds():
    indices = _indices(11)
    assert not np.array_equal(indices["fold_1"], indices["fold_2"])
    for values in indices.values():
        assert values.shape == (11, 90) and values.min() >= 0 and values.max() <= 89
        for start in range(0, 90, 7):
            assert (np.diff(values[:, start:start + 7], axis=1) == 1).all()


@pytest.mark.parametrize("mode", ["missing_date", "zero_denominator"])
def test_undefined_replicate_not_dropped_or_redrawn(mode):
    daily = daily_fixture()
    indices = {fold: np.tile(np.arange(90), (3, 1)) for fold in FOLDS}
    if mode == "missing_date":
        indices["fold_2"][1] = 17  # deterministic synthetic all-missing draw
    else:
        daily.loc[daily.policy.eq("B0") & daily.fold.eq("fold_2") & daily.n_hours.gt(0), ["MAE", "WIS"]] = 0
    result, _ = _bootstrap(daily, replicates=3, indices=indices)
    aggregate = result.loc[result.scope.eq("equal_fold")]
    assert aggregate.status.eq("unresolved_uncertainty").all()
    assert aggregate.ci_lower.isna().all() and aggregate.ci_upper.isna().all()
    assert aggregate.undefined_replicates.eq(1 if mode == "missing_date" else 3).all()
    assert set(_conclusions(result).values()) == {"no demonstrated joint preference"}


@pytest.mark.parametrize("defect", ["removed", "unpaired", "counts"])
def test_daily_grid_rejects_unmatched_inputs(defect):
    daily = daily_fixture()
    if defect == "removed":
        daily = daily.iloc[1:]
    elif defect == "unpaired":
        daily.loc[0, "MAE"] = np.nan
    else:
        daily.loc[0, "n_hours"] = 24
    with pytest.raises(ValueError):
        _bootstrap(daily, replicates=2)


def test_joint_rule_strict_wis_weak_mae_and_mixed_intervals():
    actual, _ = _bootstrap(daily_fixture(), replicates=3)
    mask = actual.scope.eq("equal_fold")
    actual.loc[mask, "status"] = "resolved"
    actual.loc[mask & actual.metric.eq("WIS"), "ci_upper"] = -1
    actual.loc[mask & actual.metric.eq("MAE"), "ci_upper"] = 0
    assert set(_conclusions(actual).values()) == {"observed joint improvement"}
    actual.loc[mask & actual.metric.eq("WIS"), "ci_upper"] = 0
    assert set(_conclusions(actual).values()) == {"no demonstrated joint preference"}
    actual.loc[mask & actual.metric.eq("WIS"), "ci_upper"] = -1
    actual.loc[mask & actual.metric.eq("MAE"), "ci_upper"] = .001
    assert set(_conclusions(actual).values()) == {"no demonstrated joint preference"}
