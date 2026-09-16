"""Independent analytic controls for the frozen CP-15 scoring contract."""

import numpy as np
import pandas as pd
import pytest

from cp15.scoring import (
    BOOTSTRAP_SEED, CANDIDATES, FOLDS, FOLD_WINDOWS, POLICIES, QUANTILES,
    UndefinedComparisonError, _summary, bootstrap_daily, evaluate, score_hourly,
    select_candidates, validate_predictions,
)


@pytest.fixture(scope="module")
def predictions():
    records = []
    for fold, (start, end) in FOLD_WINDOWS.items():
        for day in pd.date_range(start, end):
            # One full missing calendar day tests absence without fabricating zero loss.
            if day == pd.Timestamp("2022-08-20"):
                continue
            for hour in (5, 6):
                timestamp = (day + pd.Timedelta(hours=hour)).tz_localize("Europe/Berlin").tz_convert("UTC")
                for i, policy in enumerate(POLICIES):
                    center = float(i + 2)
                    record = dict(policy=policy, fold=fold, delivery_date=day,
                                  timestamp_utc=timestamp, y_true=0., central=center + 1, scale=1.)
                    record.update(dict(zip(QUANTILES, [center - 10, center - 5, center - 2,
                                                        center, center + 2, center + 5, center + 10])))
                    records.append(record)
    return pd.DataFrame(records)


def canonical(frame):
    return frame.loc[frame.policy.eq("B0"), ["fold", "timestamp_utc", "delivery_date", "y_true"]]


def test_exact_nondegenerate_wis_tail_counts_and_centering():
    frame = pd.DataFrame({"policy": ["B0"] * 3, "fold": ["fold_1"] * 3,
                          "timestamp_utc": pd.date_range("2020-07-01", periods=3, freq="h", tz="UTC"),
                          "delivery_date": [pd.Timestamp("2020-07-01")] * 3,
                          "y_true": [5., 12., -2.], "central": [6., 6., 6.]})
    for name, value in zip(QUANTILES, [0., 2., 4., 5., 6., 8., 10.]):
        frame[name] = value
    losses = score_hourly(frame)
    # y=5: widths contribute .25*2 + .1*6 + .025*10 = 1.35.
    # y=12: median 3.5 + widths 1.35 + excesses 6+4+2 = 16.85.
    np.testing.assert_allclose(losses.WIS, [1.35 / 3.5, 16.85 / 3.5, 16.85 / 3.5])
    summary = _summary(losses)
    assert summary["MAE"] == pytest.approx(14 / 3)
    assert summary["RMSE"] == pytest.approx(np.sqrt(98 / 3))
    assert summary["raw_central_MAE"] == 5.
    assert summary["centering_effect"] == pytest.approx(-1 / 3)
    assert summary["bias"] == 0
    assert summary["daily_mean_level_MAE"] == 0
    assert summary["within_day_shape_MAE"] == pytest.approx(14 / 3)
    for level, width in ((50, 2), (80, 6), (95, 10)):
        assert summary[f"coverage{level}"] == pytest.approx(1 / 3)
        assert summary[f"lower_miss_count{level}"] == 1
        assert summary[f"upper_miss_count{level}"] == 1
        assert summary[f"p95_width{level}"] == width
    # Identity holds for this common seven-level grid; it is not native v1 pinball.
    np.testing.assert_allclose(losses.WIS, 2 * losses.mean_pinball_7)


def test_daily_level_is_day_weighted_shape_is_hour_weighted():
    frame = pd.DataFrame({"policy": ["B0"] * 3, "fold": ["fold_1"] * 3,
                          "timestamp_utc": pd.date_range("2020-07-01", periods=3, freq="h", tz="UTC"),
                          "delivery_date": pd.to_datetime(["2020-07-01", "2020-07-02", "2020-07-02"]),
                          "y_true": [0., 0., 0.], "central": [9., 1., 3.]})
    for name in QUANTILES:
        frame[name] = [9., 1., 3.]
    summary = _summary(score_hourly(frame))
    assert summary["daily_mean_level_MAE"] == 5.5
    assert summary["MAE"] == pytest.approx(13 / 3)
    assert summary["within_day_shape_MAE"] == pytest.approx(2 / 3)


def test_matched_positive_control_preserves_b1_and_input(predictions):
    original = predictions.copy(deep=True)
    validated = validate_predictions(predictions, canonical(predictions))
    pd.testing.assert_frame_equal(predictions, original)
    assert len(validated) == len(predictions)
    before = predictions.loc[predictions.policy.eq("B1")].set_index(["fold", "timestamp_utc"])
    after = validated.loc[validated.policy.eq("B1")].set_index(["fold", "timestamp_utc"])
    pd.testing.assert_frame_equal(before[list(QUANTILES)].sort_index(), after[list(QUANTILES)].sort_index())


@pytest.mark.parametrize("defect", ["crossing", "missing", "infinite", "duplicate", "unmatched",
                                      "wrong_truth", "wrong_date", "zero_scale", "naive_time"])
def test_invalid_predictions_refused_with_positive_control(predictions, defect):
    validate_predictions(predictions, canonical(predictions))
    broken = predictions.copy()
    if defect == "crossing":
        broken.loc[0, "p025"] = 1000
    elif defect == "missing":
        broken.loc[0, "p90"] = np.nan
    elif defect == "infinite":
        broken.loc[0, "central"] = np.inf
    elif defect == "duplicate":
        broken = pd.concat([broken, broken.iloc[[0]]])
    elif defect == "unmatched":
        broken = broken.iloc[1:]
    elif defect == "wrong_truth":
        broken.loc[0, "y_true"] = 99
    elif defect == "wrong_date":
        broken.loc[0, "delivery_date"] += pd.Timedelta(days=1)
    elif defect == "zero_scale":
        broken.loc[0, "scale"] = 0
    elif defect == "naive_time":
        broken["timestamp_utc"] = broken.timestamp_utc.dt.tz_localize(None)
    with pytest.raises(ValueError):
        validate_predictions(broken, canonical(predictions))


def test_common_row_deletion_and_common_truth_change_caught_by_canonical(predictions):
    stamp = predictions.iloc[0].timestamp_utc
    shortened = predictions.loc[~predictions.timestamp_utc.eq(stamp)]
    with pytest.raises(ValueError, match="original eligible"):
        validate_predictions(shortened, canonical(predictions))
    wrong = predictions.copy()
    wrong.loc[wrong.timestamp_utc.eq(stamp), "y_true"] = 42
    with pytest.raises(ValueError, match="original eligible target"):
        validate_predictions(wrong, canonical(predictions))


def selection_tables():
    records = []
    levels = dict(B0=100., B1=80., B2=60., B3=70., A1=54., A2=54., A3=54., A4=54., A5=54.)
    for policy in POLICIES:
        for fold in FOLDS:
            records.append(dict(policy=policy, fold=fold, MAE=levels[policy], WIS=levels[policy],
                                coverage95=0.90 if fold == "fold_1" else 0.98))
    peak = pd.DataFrame([dict(policy=p, MAE=levels[p], WIS=levels[p], coverage95=0.90) for p in POLICIES])
    return pd.DataFrame(records), peak


def test_inclusive_thresholds_and_table_order_positive_control():
    folds, peak = selection_tables()
    result = select_candidates(folds, peak)
    assert result["criteria"].passed.all()
    assert result["ranking"].policy.tolist() == list(CANDIDATES)
    assert result["selection"]["best_observed_policy"] == "A1"
    assert result["selection"]["qualified_policy"] == "A1"
    assert result["selection"]["product_feasibility"] == "DEMONSTRATED_ON_DEVELOPMENT"


def test_ranking_mae_then_wis_then_table_order_and_separate_qualification():
    folds, peak = selection_tables()
    folds.loc[folds.policy.eq("A1"), "coverage95"] = 1.
    folds.loc[folds.policy.eq("A2"), "WIS"] = 53.
    folds.loc[folds.policy.eq("A3"), "MAE"] = 53.
    folds.loc[folds.policy.eq("A3"), "coverage95"] = 1.
    result = select_candidates(folds, peak)
    assert result["ranking"].policy.tolist() == ["A3", "A2", "A1", "A4", "A5"]
    assert result["selection"]["best_observed_policy"] == "A3"
    assert result["selection"]["qualified_policy"] == "A2"


@pytest.mark.parametrize("metric", ["MAE", "WIS"])
def test_zero_b0_denominator_refuses_selection(metric):
    folds, peak = selection_tables()
    folds.loc[folds.policy.eq("B0") & folds.fold.eq("fold_3"), metric] = 0
    with pytest.raises(UndefinedComparisonError, match="protocol correction"):
        select_candidates(folds, peak)


def test_each_criterion_fails_mechanically_and_actual_values_remain():
    folds, peak = selection_tables()
    folds.loc[folds.policy.isin(CANDIDATES), ["MAE", "WIS"]] = 100
    folds.loc[folds.policy.isin(CANDIDATES), "coverage95"] = 0.899
    peak.loc[peak.policy.isin(CANDIDATES), ["MAE", "WIS", "coverage95"]] = [100, 100, 0.899]
    result = select_candidates(folds, peak, integrity_verified=False)
    assert result["selection"]["qualified_policy"] is None
    assert result["selection"]["product_feasibility"] == "NOT_DEMONSTRATED"
    assert result["selection"]["failed_criteria"]["A1"] == [1, 2, 3, 4, 5, 6]
    assert result["criteria"].query("policy == 'A1' and criterion == 3").actual.tolist() == [0.899] * 5


def test_criterion5_best_comparator_is_separate_for_each_fold_and_metric():
    folds, peak = selection_tables()
    # B2 wins MAE and B3 wins WIS in fold 1; winners swap in fold 2.
    for fold, b2_mae, b2_wis, b3_mae, b3_wis in [
            ("fold_1", 40., 80., 80., 50.), ("fold_2", 80., 50., 40., 80.)]:
        folds.loc[folds.policy.eq("B2") & folds.fold.eq(fold), ["MAE", "WIS"]] = [b2_mae, b2_wis]
        folds.loc[folds.policy.eq("B3") & folds.fold.eq(fold), ["MAE", "WIS"]] = [b3_mae, b3_wis]
        folds.loc[folds.policy.eq("A1") & folds.fold.eq(fold), ["MAE", "WIS"]] = [42., 52.5]
    result = select_candidates(folds, peak)
    diagnostic = result["criteria"].query("policy == 'A1' and criterion == 5")
    assert diagnostic.query("scope == 'fold_1' and metric == 'MAE'").upper_limit.item() == 42.
    assert diagnostic.query("scope == 'fold_2' and metric == 'WIS'").upper_limit.item() == 52.5
    assert diagnostic.passed.all()  # exact 1.05 boundary included
    folds.loc[folds.policy.eq("A1") & folds.fold.eq("fold_2"), "WIS"] = 52.5001
    assert 5 in select_candidates(folds, peak)["selection"]["failed_criteria"]["A1"]


def test_end_to_end_exact_peak_recovery_daily_denominators(predictions):
    result = evaluate(predictions, expected_keys=canonical(predictions))
    assert len(result["hourly_losses"]) == len(predictions)
    assert len(result["per_fold"]) == 45
    assert len(result["daily"]) == 4050
    assert len(result["bootstrap"]) == 240
    peak = result["peak"].set_index("policy").loc["B0"]
    assert peak.n_hours == 32 and peak.n_days == 16 and peak.calendar_days == 17
    assert peak.hit_count95 == 32 and peak.coverage95 == 1
    assert result["per_fold"].query("policy == 'B0' and fold == 'fold_3'").n_hours.item() == 178
    assert result["recovery"].query("policy == 'B0'").n_hours.tolist() == [14, 14, 14, 14]
    daily = result["daily"]
    missing_day = daily.loc[daily.policy.eq("B0") & daily.delivery_date.eq(pd.Timestamp("2022-08-20"))].iloc[0]
    assert missing_day.n_hours == 0 and pd.isna(missing_day.MAE) and pd.isna(missing_day.WIS)
    assert result["scoring_metadata"]["eligible_keys_binding"] == "independent_expected_keys"


def bootstrap_fixture():
    rows = []
    for fold, (start, end) in FOLD_WINDOWS.items():
        for d, day in enumerate(pd.date_range(start, end)):
            for i, policy in enumerate(POLICIES):
                value = 2 + d * (i + 1) / 10
                rows.append(dict(fold=fold, delivery_date=day, policy=policy,
                                 MAE=value if d != 17 else np.nan,
                                 WIS=value * 2 if d != 17 else np.nan))
    return pd.DataFrame(rows)


def test_bootstrap_matches_independent_seeded_calendar_resampling():
    daily = bootstrap_fixture()
    actual = bootstrap_daily(daily)
    # Independent scalar oracle consumes exactly 13 uniform block starts per replicate.
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    replicate_differences = []
    for _ in range(2000):
        sampled_days = []
        for start in rng.integers(0, 84, size=13):
            sampled_days.extend(range(start, start + 7))
        represented = [d for d in sampled_days[:90] if d != 17]
        # A1's i=4, B0's i=0 => pointwise difference 0.4*d.
        replicate_differences.append(sum(d * .4 for d in represented) / len(represented))
    interval = np.percentile(replicate_differences, [2.5, 97.5])
    row = actual["bootstrap"].query("scope == 'fold_1' and candidate == 'A1' and baseline == 'B0' and metric == 'MAE'").iloc[0]
    assert row.difference == pytest.approx(np.mean([.4 * d for d in range(90) if d != 17]))
    np.testing.assert_allclose([row.ci_lower, row.ci_upper], interval)
    repeat = bootstrap_daily(daily)
    pd.testing.assert_frame_equal(actual["bootstrap"], repeat["bootstrap"])
    wis = actual["bootstrap"].query("scope == 'fold_1' and candidate == 'A1' and baseline == 'B0' and metric == 'WIS'").iloc[0]
    np.testing.assert_allclose([wis.ci_lower, wis.ci_upper], 2 * interval)


def test_bootstrap_missing_day_is_not_zero_loss():
    daily = bootstrap_fixture()
    for i, policy in enumerate(POLICIES):
        mask = daily.policy.eq(policy) & daily.MAE.notna()
        daily.loc[mask, ["MAE", "WIS"]] = [i + 1., i + 2.]
    intervals = bootstrap_daily(daily)["bootstrap"]
    for _, row in intervals.iterrows():
        expected = POLICIES.index(row.candidate) - POLICIES.index(row.baseline)
        np.testing.assert_allclose([row.difference, row.ci_lower, row.ci_upper], expected)


def test_bootstrap_rejects_removed_calendar_days_and_unpaired_missingness():
    daily = bootstrap_fixture()
    bootstrap_daily(daily)  # positive control
    with pytest.raises(ValueError, match="90-day"):
        bootstrap_daily(daily.loc[~daily.delivery_date.eq(pd.Timestamp("2022-07-01"))])
    daily.loc[0, "MAE"] = np.nan
    with pytest.raises(ValueError, match="identically missing"):
        bootstrap_daily(daily)


def test_coverage_includes_interval_endpoints(predictions):
    frame = validate_predictions(predictions).iloc[:2].copy()
    frame["y_true"] = [frame.iloc[0].p025, frame.iloc[1].p975]
    losses = score_hourly(frame)
    assert losses.hit95.all()
    assert not losses.lower_miss95.any() and not losses.upper_miss95.any()


def test_equal_fold_ratios_and_peak_metric_specific_comparators():
    folds, peak = selection_tables()
    folds.loc[folds.policy.eq("B0"), "MAE"] = [10, 20, 40, 80, 160]
    folds.loc[folds.policy.eq("A1"), "MAE"] = [1, 4, 12, 32, 80]
    peak.loc[peak.policy.eq("B2"), ["MAE", "WIS"]] = [50., 70.]
    peak.loc[peak.policy.eq("B3"), ["MAE", "WIS"]] = [70., 40.]
    peak.loc[peak.policy.eq("A1"), ["MAE", "WIS"]] = [50., 40.]
    result = select_candidates(folds, peak)
    assert result["relative_scores"].query("policy == 'A1'").S_MAE.item() == pytest.approx(0.3)
    criteria = result["criteria"].query("policy == 'A1' and criterion == 4")
    assert criteria.passed.all()
    assert criteria.query("metric == 'MAE'").upper_limit.item() == 50.
    assert criteria.query("metric == 'WIS'").upper_limit.item() == 40.
    peak.loc[peak.policy.eq("A1"), "WIS"] = 40.001
    assert 4 in select_candidates(folds, peak)["selection"]["failed_criteria"]["A1"]


@pytest.mark.parametrize("bad", ["missing", "duplicate", "nonfinite"])
def test_selection_cannot_silently_shrink_bad_summaries(bad):
    folds, peak = selection_tables()
    select_candidates(folds, peak)
    if bad == "missing":
        folds = folds.iloc[1:]
    elif bad == "duplicate":
        folds = pd.concat([folds, folds.iloc[[0]]])
    else:
        folds.loc[folds.policy.eq("A1"), "MAE"] = np.nan
    with pytest.raises(ValueError):
        select_candidates(folds, peak)
