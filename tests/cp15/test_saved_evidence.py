"""Independent saved-output audit; never calls CP-15 scoring or model routines.

Arithmetic, ranking, gates, normalization, and residual replay are computed here.
Only the inherited ``delu_forecast.features.build_base_features`` is reused to
recover the original eligibility contract. Production checks explicitly skip
while predictions.parquet is absent; CP15_REQUIRE_SAVED_EVIDENCE=1 forbids that.
Synthetic mutation controls exercise the checker without production outputs.
This file supplies checks for review, not an Integration verdict.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd
import pytest


ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "reports/cp15"
POLICIES = ("B0", "B1", "B2", "B3", "A1", "A2", "A3", "A4", "A5")
ROLLING = tuple(p for p in POLICIES if p != "B1")
ADAPTIVE = POLICIES[4:]
FOLDS = tuple(f"fold_{i}" for i in range(1, 6))
QUANTILES = ("p025", "p10", "p25", "p50", "p75", "p90", "p975")
PROBABILITIES = np.array([.025, .1, .25, .5, .75, .9, .975])
INTERVALS = ((50, .5, "p25", "p75"), (80, .2, "p10", "p90"),
             (95, .05, "p025", "p975"))


def digest_array(value):
    return hashlib.sha256(np.ascontiguousarray(value).tobytes()).hexdigest()


def calendar_hours(day):
    start = pd.Timestamp(day).tz_localize("Europe/Berlin")
    end = (pd.Timestamp(day) + pd.Timedelta(days=1)).tz_localize("Europe/Berlin")
    return pd.date_range(start, end, freq="h", inclusive="left").tz_convert("UTC")


def normalized_keys(frame):
    out = frame.copy()
    if "timestamp_utc" in out:
        out["timestamp_utc"] = pd.to_datetime(out.timestamp_utc, utc=True)
    if "delivery_date" in out:
        out["delivery_date"] = pd.to_datetime(out.delivery_date).dt.normalize()
    return out


def close(actual, expected):
    np.testing.assert_allclose(actual, expected, rtol=2e-12, atol=2e-12, equal_nan=True)


def independent_summary(frame):
    """Direct formulas, with daily-level means weighted by represented day."""
    if frame.empty:
        result = {c: np.nan for c in ("MAE", "RMSE", "WIS", "mean_pinball_7", "raw_central_MAE",
                                      "centering_effect", "bias", "daily_mean_level_MAE", "within_day_shape_MAE")}
        result.update(n_hours=0, n_days=0, missing_count=0, crossings=0)
        for nominal, *_ in INTERVALS:
            for metric in ("coverage", "mean_width", "median_width", "p95_width"):
                result[f"{metric}{nominal}"] = np.nan
            for metric in ("hit_count", "lower_miss_count", "upper_miss_count"):
                result[f"{metric}{nominal}"] = 0
        return result
    y = frame.y_true.to_numpy(float)
    median = frame.p50.to_numpy(float)
    error = median - y
    daily = frame.assign(_forecast=median, _truth=y).groupby("delivery_date")
    f_day = daily._forecast.transform("mean").to_numpy()
    y_day = daily._truth.transform("mean").to_numpy()
    raw_mae = np.mean(np.abs(frame.central.to_numpy(float) - y))
    result = {
        "n_hours": len(frame), "n_days": frame.delivery_date.nunique(),
        "MAE": np.mean(np.abs(error)), "RMSE": np.sqrt(np.mean(error * error)),
        "raw_central_MAE": raw_mae, "centering_effect": np.mean(np.abs(error)) - raw_mae,
        "bias": np.mean(error),
        "daily_mean_level_MAE": np.mean(np.abs(daily._forecast.mean() - daily._truth.mean())),
        "within_day_shape_MAE": np.mean(np.abs((median - f_day) - (y - y_day))),
        "missing_count": 0, "crossings": 0,
    }
    interval_contributions = []
    for nominal, alpha, low_name, high_name in INTERVALS:
        low, high = frame[low_name].to_numpy(float), frame[high_name].to_numpy(float)
        width = high - low
        below, above = y < low, y > high
        interval_score = width + 2 / alpha * (low - y) * below + 2 / alpha * (y - high) * above
        interval_contributions.append(alpha / 2 * interval_score)
        result.update({
            f"coverage{nominal}": np.mean(~(below | above)),
            f"hit_count{nominal}": np.count_nonzero(~(below | above)),
            f"lower_miss_count{nominal}": np.count_nonzero(below),
            f"upper_miss_count{nominal}": np.count_nonzero(above),
            f"mean_width{nominal}": np.mean(width),
            f"median_width{nominal}": np.median(width),
            f"p95_width{nominal}": np.percentile(width, 95, method="linear"),
        })
    result["WIS"] = np.mean((.5 * np.abs(error) + np.sum(interval_contributions, axis=0)) / 3.5)
    residual = y[:, None] - frame[list(QUANTILES)].to_numpy(float)
    result["mean_pinball_7"] = np.maximum(PROBABILITIES * residual, (PROBABILITIES - 1) * residual).mean()
    return result


def independent_tables(predictions):
    frame = normalized_keys(predictions)
    assert not frame.duplicated(["policy", "timestamp_utc"]).any()
    assert set(frame.policy) == set(POLICIES)
    assert set(frame.fold) == set(FOLDS)
    assert np.isfinite(frame[["y_true", "central", "scale", *QUANTILES]].to_numpy(float)).all()
    assert (frame.scale > 0).all()
    assert (np.diff(frame[list(QUANTILES)].to_numpy(float), axis=1) >= 0).all()
    assert np.array_equal(frame.timestamp_utc.dt.tz_convert("Europe/Berlin").dt.tz_localize(None).dt.normalize(), frame.delivery_date)
    source = frame.loc[frame.policy.eq("B0")].sort_values(["fold", "timestamp_utc"])
    for policy in POLICIES:
        arm = frame.loc[frame.policy.eq(policy)].sort_values(["fold", "timestamp_utc"])
        pd.testing.assert_frame_equal(arm[["fold", "timestamp_utc", "delivery_date", "y_true"]].reset_index(drop=True),
                                      source[["fold", "timestamp_utc", "delivery_date", "y_true"]].reset_index(drop=True))
    records = [{"policy": policy, "fold": fold, **independent_summary(rows)}
               for (policy, fold), rows in frame.groupby(["policy", "fold"])]
    per_fold = pd.DataFrame(records)
    assert len(per_fold) == 45
    peak = pd.DataFrame([{"policy": policy, **independent_summary(rows.loc[
        rows.delivery_date.between("2022-08-15", "2022-08-31")])}
                        for policy, rows in frame.groupby("policy")])
    return per_fold, peak


def independent_diagnostics(predictions, fold_windows):
    """Recompute observation-pooled, represented-day, peak, and recovery scores."""
    frame = normalized_keys(predictions)
    pooled = pd.DataFrame([{"policy": p, **independent_summary(rows)}
                           for p, rows in frame.groupby("policy")])
    daily_records = [{"policy": p, "fold": f, "delivery_date": d, **independent_summary(rows)}
                     for (p, f, d), rows in frame.groupby(["policy", "fold", "delivery_date"])]
    represented = pd.DataFrame(daily_records).set_index(["policy", "fold", "delivery_date"])
    expected_daily = []
    for fold in FOLDS:
        grid = pd.date_range(*fold_windows[fold], freq="D")
        assert len(grid) == 90
        calendar = pd.MultiIndex.from_product([POLICIES, [fold], grid], names=["policy", "fold", "delivery_date"])
        part = represented.reindex(calendar)
        count_columns = [c for c in part if c.startswith("n_") or "_count" in c or c == "crossings"]
        part[count_columns] = part[count_columns].fillna(0).astype(int)
        expected_daily.append(part.reset_index())
    peak_records, recovery_records = [], []
    for policy in POLICIES:
        arm = frame.loc[frame.policy.eq(policy) & frame.fold.eq("fold_3")]
        peak_rows = arm.loc[arm.delivery_date.between("2022-08-15", "2022-08-31")]
        peak_records.append({"policy": policy, "window_start": "2022-08-15", "window_end": "2022-08-31",
                             "calendar_days": 17, **independent_summary(peak_rows)})
        for day in (1, 8, 15, 22):
            start, end = f"2022-09-{day:02}", f"2022-09-{day + 6:02}"
            rows = arm.loc[arm.delivery_date.between(start, end)]
            recovery_records.append({"policy": policy, "fold": "fold_3", "window_start": start,
                                     "window_end": end, "calendar_days": 7, **independent_summary(rows)})
    return {"pooled": pooled, "daily": pd.concat(expected_daily, ignore_index=True),
            "peak": pd.DataFrame(peak_records), "recovery": pd.DataFrame(recovery_records)}


def independent_bootstrap(daily, protocol):
    """Scalar replicate loop, independent from the production vectorized scorer.

    A sampled calendar day contributes its complete daily loss vector or no
    observation. Missing days remain in block geometry and never become zeros.
    """
    replicates, block = protocol["bootstrap"]["replicates"], protocol["bootstrap"]["block_days"]
    seed = protocol["bootstrap_seed"]
    assert (replicates, block, seed) == (2000, 7, 15042)
    rng = np.random.default_rng(seed)
    fold_means, fold_draws = [], []
    results = []

    def intervals(scope, means, draws):
        for ai, candidate in enumerate(ADAPTIVE, start=4):
            for bi, baseline in enumerate(POLICIES[:4]):
                for mi, metric in enumerate(("MAE", "WIS")):
                    contrast = draws[:, ai, mi] - draws[:, bi, mi]
                    low, high = np.percentile(contrast, [2.5, 97.5], method="linear")
                    results.append(dict(scope=scope, candidate=candidate, baseline=baseline, metric=metric,
                                        difference=means[ai, mi] - means[bi, mi],
                                        ci_lower=low, ci_upper=high, replicates=replicates))

    for fold in FOLDS:
        part = daily.loc[daily.fold.eq(fold)]
        assert not part.duplicated(["policy", "delivery_date"]).any()
        dates = pd.DatetimeIndex(sorted(pd.to_datetime(part.delivery_date).unique()))
        assert len(dates) == 90 and dates.equals(pd.date_range(dates[0], dates[-1], freq="D"))
        values = np.empty((90, 9, 2), dtype=float)
        for i, policy in enumerate(POLICIES):
            arm = part.loc[part.policy.eq(policy)].set_index("delivery_date").reindex(dates)
            values[:, i, :] = arm[["MAE", "WIS"]].to_numpy(float)
        represented = np.isfinite(values).all(axis=(1, 2))
        absent = np.isnan(values).all(axis=(1, 2))
        assert (represented | absent).all(), "unpaired or nonfinite daily losses"
        means = values[represented].mean(axis=0)
        draws = np.empty((replicates, 9, 2), dtype=float)
        for replicate in range(replicates):
            starts = rng.integers(0, 84, size=13)
            sampled = np.concatenate([np.arange(start, start + 7) for start in starts])[:90]
            included = sampled[represented[sampled]]
            assert len(included), "empty replicate denominator"
            draws[replicate] = values[included].mean(axis=0)
        intervals(fold, means, draws)
        fold_means.append(means)
        fold_draws.append(draws)
    intervals("equal_fold", np.mean(fold_means, axis=0), np.mean(fold_draws, axis=0))
    return pd.DataFrame(results)


def independent_decision(per_fold, peak):
    table = per_fold.set_index(["policy", "fold"])
    peak = peak.set_index("policy")
    scores = {}
    for policy in POLICIES:
        scores[policy] = {}
        for metric in ("MAE", "WIS"):
            ratios = []
            for fold in FOLDS:
                denominator = table.loc[("B0", fold), metric]
                assert np.isfinite(denominator) and denominator > 0, "undefined B0 comparison"
                ratios.append(table.loc[(policy, fold), metric] / denominator)
            scores[policy][f"S_{metric}"] = np.mean(ratios)
    ranking = sorted(ADAPTIVE, key=lambda p: (scores[p]["S_MAE"], scores[p]["S_WIS"], ADAPTIVE.index(p)))
    criteria = []

    def record(policy, number, metric, scope, actual, low=None, high=None):
        passed = np.isfinite(actual) and (low is None or actual >= low) and (high is None or actual <= high)
        criteria.append(dict(policy=policy, criterion=number, metric=metric, scope=scope,
                             actual=actual, lower_limit=low, upper_limit=high, passed=bool(passed)))

    for policy in ADAPTIVE:
        for number, metric in ((1, "MAE"), (2, "WIS")):
            record(policy, number, "S_" + metric, "equal_fold", scores[policy]["S_" + metric],
                   high=.9 * min(scores[p]["S_" + metric] for p in POLICIES[:4]))
        for fold in FOLDS:
            record(policy, 3, "coverage95", fold, table.loc[(policy, fold), "coverage95"], .9, .98)
        record(policy, 4, "coverage95", "peak", peak.loc[policy, "coverage95"], .9)
        for metric in ("MAE", "WIS"):
            record(policy, 4, metric, "peak", peak.loc[policy, metric],
                   high=min(peak.loc[p, metric] for p in POLICIES[:4]))
            for fold in FOLDS:
                record(policy, 5, metric, fold, table.loc[(policy, fold), metric],
                       high=1.05 * min(table.loc[(p, fold), metric] for p in ("B2", "B3")))
        record(policy, 6, "complete_finite_ordered", "all_eligible", 1, 1)
    failed = {policy: sorted({r["criterion"] for r in criteria if r["policy"] == policy and not r["passed"]})
              for policy in ADAPTIVE}
    qualified = next((policy for policy in ranking if not failed[policy]), None)
    return {"scores": scores, "ranking": ranking, "criteria": pd.DataFrame(criteria),
            "selection": {"best_observed_policy": ranking[0], "qualified_policy": qualified,
                          "product_feasibility": "DEMONSTRATED_ON_DEVELOPMENT" if qualified else "NOT_DEMONSTRATED",
                          "failed_criteria": failed}}


def compare_numeric_table(actual, expected, keys, columns):
    assert not actual.duplicated(keys).any()
    left, right = actual.set_index(keys).sort_index(), expected.set_index(keys).sort_index()
    pd.testing.assert_index_equal(left.index, right.index)
    for column in columns:
        close(left[column].to_numpy(float), right[column].to_numpy(float))


def check_preservation(root):
    record = json.loads((root / "reports/cp15/attempt-1-preservation.json").read_text())
    assert len(record["evidence_tip"]) == 40 and record["mapping"]
    for original, saved in record["mapping"].items():
        preserved = root / saved["preserved_at"]
        assert saved["preserved_at"] != original
        assert hashlib.sha256(preserved.read_bytes()).hexdigest() == saved["sha256"], original


def independent_origin_stats(raw):
    """Use precisely the preceding 168 canonical hours, including DST boundaries."""
    index = pd.DatetimeIndex(pd.to_datetime(raw.timestamp_utc, utc=True))
    y = raw.price_eur_mwh.to_numpy(float)
    days = pd.to_datetime(raw.delivery_date).dt.normalize()
    levels, scales = {}, {}
    for day in days.unique():
        boundary = pd.Timestamp(day).tz_localize("Europe/Berlin").tz_convert("UTC")
        wanted = pd.date_range(end=boundary - pd.Timedelta(hours=1), periods=168, freq="h")
        positions = index.get_indexer(wanted)
        values = y[positions] if (positions >= 0).all() else np.full(168, np.nan)
        levels[day] = float(np.mean(values))
        scales[day] = float(max(np.std(values, ddof=1), 1.))
    return days.map(levels).to_numpy(float), days.map(scales).to_numpy(float)


def check_feedback(issued, feedback, raw):
    """Bind every consumed residual to its issued immutable forecast and scale."""
    issued, raw = normalized_keys(issued), normalized_keys(raw)
    assert not issued.duplicated(["policy", "timestamp_utc"]).any()
    actual = pd.Series(raw.price_eur_mwh.to_numpy(float), index=pd.DatetimeIndex(raw.timestamp_utc))
    groups = {(p, pd.Timestamp(d)): rows.sort_values("timestamp_utc")
              for (p, d), rows in issued.groupby(["policy", "delivery_date"])}
    consumed = feedback.loc[feedback.status.eq("consumed")].copy()
    consumed["feedback_day"] = pd.to_datetime(consumed.feedback_day).dt.normalize()
    consumed["origin"] = pd.to_datetime(consumed.origin).dt.normalize()
    assert not consumed.duplicated(["policy", "feedback_day"]).any(), "feedback consumed twice"
    assert (consumed.feedback_day <= consumed.origin - pd.Timedelta(days=2)).all(), "D-2 violation"
    recovered = {}
    for row in consumed.itertuples(index=False):
        forecast = groups[(row.policy, row.feedback_day)]
        timestamps = pd.DatetimeIndex(forecast.timestamp_utc)
        assert timestamps.equals(calendar_hours(row.feedback_day)), "incomplete feedback day"
        positions = actual.index.get_indexer(timestamps)
        assert (positions >= 0).all()
        truth = actual.to_numpy()[positions]
        assert np.isfinite(truth).all()
        center, scale = forecast.central.to_numpy(float), forecast.scale.to_numpy(float)
        errors = (truth - center) / (scale if row.policy in ADAPTIVE else 1.)
        assert row.n == len(timestamps)
        assert row.issued_center_sha256 == digest_array(center), "issued center lineage"
        assert row.issued_scale_sha256 == digest_array(scale), "issued scale lineage"
        assert row.error_sha256 == digest_array(errors), "released error lineage"
        recovered[(row.policy, row.feedback_day)] = (row.origin, errors)
    # Complete finite issued days must have been released at the first recorded
    # release origin at/after D-2; no suppressing a bad but available error day.
    release_origins = sorted(pd.to_datetime(feedback.origin).unique())
    for (policy, day), forecast in groups.items():
        timestamps = pd.DatetimeIndex(forecast.timestamp_utc)
        positions = actual.index.get_indexer(timestamps)
        if not timestamps.equals(calendar_hours(day)) or (positions < 0).any():
            continue
        if not np.isfinite(actual.to_numpy()[positions]).all():
            continue
        eligible_origins = [pd.Timestamp(d) for d in release_origins if pd.Timestamp(d) >= day + pd.Timedelta(days=2)]
        if eligible_origins:
            assert (policy, day) in recovered, "complete eligible errors suppressed"
            assert recovered[(policy, day)][0] == eligible_origins[0], "released later than available D-2 origin"
    return recovered


def check_reconstructed_intervals(predictions, issued, origins, recovered):
    predictions, issued = normalized_keys(predictions), normalized_keys(issued)
    pred_groups = {(p, pd.Timestamp(d)): rows.sort_values("timestamp_utc")
                   for (p, d), rows in predictions.groupby(["policy", "delivery_date"])}
    issued_groups = {(p, pd.Timestamp(d)): rows.sort_values("timestamp_utc")
                     for (p, d), rows in issued.groupby(["policy", "delivery_date"])}
    checked = 0
    for origin in origins:
        if not origin.get("buffer"):
            continue
        day = pd.Timestamp(origin["delivery_date"])
        for policy in ROLLING:
            available = sorted(d for (p, d), (release, _) in recovered.items() if p == policy and release <= day)
            dates = available[-28:]
            assert len(dates) == 28
            errors = np.concatenate([recovered[(policy, d)][1] for d in dates])
            metadata = origin["buffer"][policy]
            assert metadata["buffer_start"] == str(dates[0].date())
            assert metadata["buffer_end"] == str(dates[-1].date())
            assert metadata["buffer_days"] == 28 and metadata["buffer_hours"] == len(errors)
            assert metadata["buffer_sha256"] == digest_array(errors)
            forecast = pred_groups[(policy, day)]
            issued_day = issued_groups[(policy, day)].set_index("timestamp_utc")
            centers = issued_day.central.reindex(pd.DatetimeIndex(forecast.timestamp_utc)).to_numpy(float)
            scales = issued_day.scale.reindex(pd.DatetimeIndex(forecast.timestamp_utc)).to_numpy(float)
            assert np.isfinite(centers).all() and np.isfinite(scales).all()
            np.testing.assert_array_equal(forecast.central.to_numpy(float), centers)
            quantiles = np.quantile(errors, PROBABILITIES, method="linear")
            expected = centers[:, None] + (scales[:, None] if policy in ADAPTIVE else 1.) * quantiles
            close(forecast[list(QUANTILES)].to_numpy(float), expected)
            checked += 1
    assert checked > 0, "no saved evaluation buffers reconstructed"


@pytest.fixture(scope="module")
def saved():
    if not (REPORT / "predictions.parquet").exists():
        if os.environ.get("CP15_REQUIRE_SAVED_EVIDENCE") == "1":
            pytest.fail("required production predictions.parquet has not arrived")
        pytest.skip("production outputs have not arrived; synthetic checker controls still run")
    return normalized_keys(pd.read_parquet(REPORT / "predictions.parquet"))


@pytest.fixture(scope="module")
def original():
    # Filter before materializing: no reserved-tail or spent-holdout outcomes.
    from delu_forecast.features import build_base_features
    spec = json.loads((ROOT / "data/partitions.json").read_text())
    cutoff = pd.Timestamp("2026-04-07").date()
    raw = pd.read_parquet(ROOT / "data/snapshot.parquet",
                          columns=["timestamp_utc", "delivery_date", "price_eur_mwh", "load_forecast_mw"],
                          filters=[("delivery_date", ">=", pd.Timestamp("2019-01-01").date()),
                                   ("delivery_date", "<=", cutoff)]).reset_index(drop=True)
    raw["timestamp_utc"] = pd.to_datetime(raw.timestamp_utc, utc=True)
    assert raw.timestamp_utc.is_monotonic_increasing and not raw.timestamp_utc.duplicated().any()
    base = build_base_features(raw)
    eligible = base.notna().all(axis=1).to_numpy() & np.isfinite(raw.price_eur_mwh.to_numpy(float))
    level, scale = independent_origin_stats(raw)
    assert np.isfinite(level[eligible]).all() and np.isfinite(scale[eligible]).all()
    return raw, eligible, level, scale, spec


def test_attempt_one_mapping_hashes_remain_exact():
    check_preservation(ROOT)


def test_saved_scores_and_mechanical_decision(saved):
    assert len(saved) == 96723
    assert saved.groupby("policy").size().to_dict() == {p: 10747 for p in POLICIES}
    per_fold, peak = independent_tables(saved)
    actual = pd.read_csv(REPORT / "per_fold.csv")
    compare_numeric_table(actual, per_fold, ["policy", "fold"],
                          [c for c in per_fold if c not in ("policy", "fold")])
    decision = independent_decision(per_fold, peak)
    relative = pd.DataFrame([{"policy": p, **v} for p, v in decision["scores"].items()])
    compare_numeric_table(pd.read_csv(REPORT / "relative_scores.csv"), relative, ["policy"], ["S_MAE", "S_WIS"])
    ranking = pd.read_csv(REPORT / "ranking.csv").sort_values("rank")
    assert ranking.policy.tolist() == decision["ranking"]
    assert ranking["rank"].tolist() == [1, 2, 3, 4, 5]
    for row in ranking.itertuples(index=False):
        assert bool(row.qualified) == (not decision["selection"]["failed_criteria"][row.policy])
        failures = ast.literal_eval(row.failed_criteria) if isinstance(row.failed_criteria, str) else row.failed_criteria
        assert failures == decision["selection"]["failed_criteria"][row.policy]
    criteria = pd.read_csv(REPORT / "criteria.csv")
    compare_numeric_table(criteria, decision["criteria"], ["policy", "criterion", "metric", "scope"],
                          ["actual", "lower_limit", "upper_limit", "passed"])
    selection = json.loads((REPORT / "selection.json").read_text())
    for field, value in decision["selection"].items():
        assert selection[field] == value


def test_saved_diagnostics_and_bootstrap(saved):
    protocol = json.loads((REPORT / "protocol.json").read_text())
    spec = json.loads((ROOT / "data/partitions.json").read_text())
    windows = {f["name"]: (f["evaluation"]["start"], f["evaluation"]["end"])
               for f in spec["development_folds"]}
    diagnostics = independent_diagnostics(saved, windows)
    table_keys = {"pooled": ["policy"], "daily": ["policy", "fold", "delivery_date"],
                  "peak": ["policy", "window_start", "window_end"],
                  "recovery": ["policy", "fold", "window_start", "window_end"]}
    for name, expected in diagnostics.items():
        actual = normalized_keys(pd.read_csv(REPORT / f"{name}.csv"))
        keys = table_keys[name]
        compare_numeric_table(actual, expected, keys, [c for c in expected if c not in keys])
    bootstrap = independent_bootstrap(diagnostics["daily"], protocol)
    assert len(bootstrap) == 240
    compare_numeric_table(pd.read_csv(REPORT / "bootstrap.csv"), bootstrap,
                          ["scope", "candidate", "baseline", "metric"],
                          ["difference", "ci_lower", "ci_upper", "replicates"])


def test_saved_original_rows_and_exact_native_b1(saved, original):
    raw, eligible, _, _, spec = original
    native = pd.read_parquet(ROOT / "reports/cp2/development_predictions.parquet")
    native = native.loc[native.arm.eq("base")]
    raw_days = pd.to_datetime(raw.delivery_date)
    for fold in spec["development_folds"]:
        name, bounds = fold["name"], fold["evaluation"]
        positions = np.flatnonzero(eligible & raw_days.between(bounds["start"], bounds["end"]).to_numpy())
        source = raw.iloc[positions]
        for policy in POLICIES:
            arm = saved.loc[saved.policy.eq(policy) & saved.fold.eq(name)].sort_values("timestamp_utc")
            np.testing.assert_array_equal(arm.timestamp_utc.to_numpy(), source.timestamp_utc.to_numpy())
            np.testing.assert_array_equal(arm.y_true.to_numpy(), source.price_eur_mwh.to_numpy())
        preserved = native.loc[native.fold.eq(name)]
        b1 = saved.loc[saved.policy.eq("B1") & saved.fold.eq(name)].sort_values("timestamp_utc")
        np.testing.assert_array_equal(preserved.y_true.to_numpy(), source.price_eur_mwh.to_numpy())
        np.testing.assert_array_equal(pd.to_datetime(preserved.delivery_date).to_numpy(), pd.to_datetime(source.delivery_date).to_numpy())
        np.testing.assert_array_equal(b1.central.to_numpy(), preserved.raw_p50.to_numpy())
        np.testing.assert_array_equal(b1[list(QUANTILES)].to_numpy(), preserved[["final_" + q for q in QUANTILES]].to_numpy())


def check_issued_policy_definitions(issued, raw):
    issued, raw = normalized_keys(issued), normalized_keys(raw)
    values = issued.pivot(index='timestamp_utc', columns='policy', values='central')
    assert set(values.columns) == set(ROLLING) and np.isfinite(values.to_numpy()).all()
    np.testing.assert_array_equal(values.A3, (values.A1 + values.A2) / 2)
    np.testing.assert_array_equal(values.A5, (values.A1 + values.A2 + values.A4) / 3)
    # Independent calendar-day/local-hour lookup; ambiguous source hours fail closed.
    raw['hour'] = raw.timestamp_utc.dt.tz_convert('Europe/Berlin').dt.hour
    source = raw.groupby(['delivery_date', 'hour']).price_eur_mwh.agg(['first', 'size'])
    unique = source['first'].where(source['size'].eq(1))
    naive = issued.loc[issued.policy.eq('B0')].sort_values('timestamp_utc')
    lag = np.where(naive.delivery_date.dt.dayofweek.isin([1, 2, 3, 4]), 1, 7)
    keys = pd.MultiIndex.from_arrays([
        naive.delivery_date - pd.to_timedelta(lag, unit='D'),
        naive.timestamp_utc.dt.tz_convert('Europe/Berlin').dt.hour,
    ], names=['delivery_date', 'hour'])
    expected = unique.reindex(keys).to_numpy(float)
    assert np.isfinite(expected).all(), 'issued B0 used a missing or ambiguous source hour'
    np.testing.assert_array_equal(naive.central, expected)


def test_saved_issued_errors_and_reconstructed_intervals(saved, original):
    raw, eligible, level, scale, spec = original
    complete = []
    raw_index = pd.DatetimeIndex(raw.timestamp_utc)
    for day, positions in raw.groupby("delivery_date", sort=True).indices.items():
        if eligible[positions].all() and raw_index[positions].equals(calendar_hours(day)):
            complete.append(pd.Timestamp(day))
    for fold in FOLDS:
        issued = pd.read_parquet(REPORT / f"folds/{fold}-issued.parquet")
        feedback = pd.read_parquet(REPORT / f"folds/{fold}-feedback.parquet")
        origins = json.loads((REPORT / f"folds/{fold}-origins.json").read_text())
        issued = normalized_keys(issued)
        check_issued_policy_definitions(issued, raw)
        assert set(issued.policy) == set(ROLLING)
        assert np.isfinite(issued[["central", "level", "scale"]].to_numpy(float)).all()
        assert (issued.scale >= 1).all()
        positions = raw_index.get_indexer(pd.DatetimeIndex(issued.timestamp_utc))
        assert (positions >= 0).all()
        np.testing.assert_array_equal(issued.level.to_numpy(float), level[positions])
        np.testing.assert_array_equal(issued.scale.to_numpy(float), scale[positions])
        bounds = next(f["evaluation"] for f in spec["development_folds"] if f["name"] == fold)
        first, last = pd.Timestamp(bounds["start"]), pd.Timestamp(bounds["end"])
        warmup = [d for d in complete if d <= first - pd.Timedelta(days=2)][-28:]
        assert len(warmup) == 28 and issued.delivery_date.min() == warmup[0]
        origin_days = pd.to_datetime([o["delivery_date"] for o in origins])
        assert origin_days.equals(pd.date_range(warmup[0], last, freq="D"))
        for day, rows in issued.groupby("delivery_date"):
            expected_origin = (day - pd.Timedelta(days=1)).tz_localize("UTC") + pd.Timedelta(hours=11)
            assert pd.to_datetime(rows.origin_utc, utc=True).eq(expected_origin).all()
            assert set(rows.policy) == set(ROLLING)
            reference = rows.loc[rows.policy.eq("B0"), "timestamp_utc"].sort_values().to_numpy()
            for policy in ROLLING:
                np.testing.assert_array_equal(rows.loc[rows.policy.eq(policy), "timestamp_utc"].sort_values().to_numpy(), reference)
        for entry in origins:
            day = pd.Timestamp(entry["delivery_date"])
            expected_origin = (day - pd.Timedelta(days=1)).tz_localize("UTC") + pd.Timedelta(hours=11)
            assert pd.Timestamp(entry["origin_utc"]).tz_convert("UTC") == expected_origin
            counts = issued.loc[issued.delivery_date.eq(day)].groupby("policy").size()
            count = int(counts.iloc[0]) if len(counts) else 0
            assert (counts == count).all()
            declared = entry["issued_hours_per_policy"]
            assert declared == count or declared == {p: count for p in ROLLING}
            evaluation_count = len(saved.loc[saved.fold.eq(fold) & saved.policy.eq("B0") & saved.delivery_date.eq(day)])
            assert entry["eligible_evaluation_hours"] == evaluation_count
            assert np.isfinite(entry["wall_seconds"]) and entry["wall_seconds"] >= 0
            assert entry["max_rss_bytes"] > 0
        recovered = check_feedback(issued, feedback, raw)
        check_reconstructed_intervals(saved.loc[saved.fold.eq(fold)], issued, origins, recovered)


def check_fit_records(fits, raw, eligible, level, scale, expected_hours=None):
    fits = normalized_keys(fits)
    days = pd.to_datetime(raw.delivery_date)
    local_hour = raw.timestamp_utc.dt.tz_convert("Europe/Berlin").dt.hour.to_numpy()
    y = raw.price_eur_mwh.to_numpy(float)
    for _, records in fits.groupby("delivery_date"):
        assert set(records.policy) == {"B2", "B3", "A1", "A2", "A4"}
    for (policy, day), records in fits.groupby(["policy", "delivery_date"]):
        lower = day - pd.Timedelta(days=84 if policy == "A4" else 728)
        if policy != "A4":
            lower = max(lower, pd.Timestamp("2019-01-01"))
        assert lower >= pd.Timestamp("2019-01-01")
        train = np.flatnonzero(eligible & days.ge(lower).to_numpy() & days.lt(day).to_numpy())
        assert len(train) and np.isfinite(level[train]).all() and np.isfinite(scale[train]).all()
        target = ((y - level) / scale)[train] if policy in ADAPTIVE else y[train]
        assert records.n_train.eq(len(train)).all()
        assert pd.to_datetime(records.history_start).eq(lower).all()
        assert pd.to_datetime(records.history_end_exclusive).eq(day).all()
        assert records.train_rows_sha256.eq(digest_array(train)).all()
        assert records.normalization_rows_sha256.eq(digest_array(np.column_stack((level[train], scale[train])))).all()
        if "train_target_sha256" in records:
            assert records.train_target_sha256.eq(digest_array(target)).all()
        assert records.model_sha256.str.fullmatch(r"[0-9a-f]{64}").all()
        if policy in ("B3", "A2"):
            assert len(records) == 1 and len(train) >= 8760
        else:
            required_hours = set(range(24)) if expected_hours is None else expected_hours[day]
            assert len(records) == len(required_hours) and set(records.local_hour) == required_hours
            validation_start = day - pd.Timedelta(days=28)
            for row in records.itertuples(index=False):
                hour_train = train[local_hour[train] == int(row.local_hour)]
                inner = hour_train[days.iloc[hour_train].lt(validation_start).to_numpy()]
                validation = hour_train[days.iloc[hour_train].ge(validation_start).to_numpy()]
                assert len(inner) >= 20 and len(validation) >= 14
                assert row.n_hour_train == len(hour_train)
                assert len(hour_train) >= (40 if policy == "A4" else 365)
                if hasattr(row, "hour_train_rows_sha256"):
                    assert row.hour_train_rows_sha256 == digest_array(hour_train)
                assert pd.Timestamp(row.inner_train_end) == days.iloc[inner].max()
                assert pd.Timestamp(row.validation_start) == days.iloc[validation].min()
                assert pd.Timestamp(row.validation_end) == days.iloc[validation].max()
                assert pd.Timestamp(row.inner_train_end) < validation_start <= pd.Timestamp(row.validation_start)
                assert pd.Timestamp(row.validation_end) < day
                for name, indices in (("inner_train_rows_sha256", inner), ("validation_rows_sha256", validation)):
                    if hasattr(row, name):
                        assert getattr(row, name) == digest_array(indices)
                assert row.selected_relative_alpha in (.001, .01, .1, 1.)
                scores = row.validation_mae_by_alpha
                if isinstance(scores, str):
                    scores = json.loads(scores)
                if isinstance(scores, dict):
                    values = [scores[str(a)] if str(a) in scores else scores[a] for a in (.001, .01, .1, 1.)]
                else:
                    values = list(scores)
                assert len(values) == 4 and np.isfinite(values).all()
                assert row.selected_relative_alpha == (.001, .01, .1, 1.)[int(np.argmin(values))]


def test_saved_fit_window_and_normalization_lineage(saved, original):
    raw, eligible, level, scale, _ = original
    for fold in FOLDS:
        fits = normalized_keys(pd.read_parquet(REPORT / f"folds/{fold}-fits.parquet"))
        issued = normalized_keys(pd.read_parquet(REPORT / f"folds/{fold}-issued.parquet"))
        assert set(fits.delivery_date) == set(issued.delivery_date)
        expected_hours = {day: set(rows.timestamp_utc.dt.tz_convert("Europe/Berlin").dt.hour)
                          for day, rows in issued.groupby("delivery_date")}
        check_fit_records(fits, raw, eligible, level, scale, expected_hours)


def _analytic_predictions():
    rows = []
    for policy in POLICIES:
        for i, fold in enumerate(FOLDS):
            day = pd.Timestamp("2022-08-15") if fold == "fold_3" else pd.Timestamp(2020 + i, 1, 1)
            for hour, y in enumerate((5., 12., -2.)):
                record = dict(policy=policy, fold=fold, delivery_date=day,
                              timestamp_utc=(day + pd.Timedelta(hours=hour)).tz_localize("Europe/Berlin").tz_convert("UTC"),
                              y_true=y, central=6., scale=1.)
                record.update(dict(zip(QUANTILES, (0., 2., 4., 5., 6., 8., 10.))))
                rows.append(record)
    return pd.DataFrame(rows)


def test_independent_arithmetic_exact_fixture():
    folds, peak = independent_tables(_analytic_predictions())
    first = folds.iloc[0]
    close(first.MAE, 14 / 3)
    close(first.RMSE, np.sqrt(98 / 3))
    close(first.WIS, (1.35 + 16.85 + 16.85) / 10.5)
    close(first.raw_central_MAE, 5.)
    close(first.centering_effect, -1 / 3)
    close(first.daily_mean_level_MAE, 0.)
    close(first.within_day_shape_MAE, 14 / 3)
    assert first.hit_count95 == first.lower_miss_count95 == first.upper_miss_count95 == 1
    result = independent_decision(folds, peak)
    assert result["ranking"] == list(ADAPTIVE)
    assert result["selection"]["qualified_policy"] is None


@pytest.mark.parametrize("mutation", ["missing", "duplicate", "crossing", "infinite", "truth"])
def test_independent_row_checker_rejects_mutation(mutation):
    frame = _analytic_predictions()
    independent_tables(frame)
    if mutation == "missing":
        frame = frame.iloc[1:]
    elif mutation == "duplicate":
        frame = pd.concat([frame, frame.iloc[[0]]])
    elif mutation == "crossing":
        frame.loc[0, "p025"] = 999
    elif mutation == "infinite":
        frame.loc[0, "p50"] = np.inf
    else:
        frame.loc[0, "y_true"] = 888
    with pytest.raises(AssertionError):
        independent_tables(frame)


def test_score_checker_detects_changed_saved_score():
    expected, _ = independent_tables(_analytic_predictions())
    compare_numeric_table(expected.copy(), expected, ["policy", "fold"], ["MAE", "WIS"])
    broken = expected.copy()
    broken.loc[0, "WIS"] += .01
    with pytest.raises(AssertionError):
        compare_numeric_table(broken, expected, ["policy", "fold"], ["MAE", "WIS"])


def test_decision_checker_boundaries_oracles_and_zero_reference():
    folds, peak = independent_tables(_analytic_predictions())
    for policy in POLICIES:
        folds.loc[folds.policy.eq(policy), ["MAE", "WIS", "coverage95"]] = [100., 100., .9]
        peak.loc[peak.policy.eq(policy), ["MAE", "WIS", "coverage95"]] = [100., 100., .9]
    folds.loc[folds.policy.isin(ADAPTIVE), ["MAE", "WIS"]] = 90.
    folds.loc[folds.policy.eq("A1") & folds.fold.eq("fold_1"), "coverage95"] = .98
    positive = independent_decision(folds, peak)
    assert positive["selection"]["qualified_policy"] == "A1"
    # Metric-specific best rolling references must not become one chosen model.
    folds.loc[folds.policy.eq("B2") & folds.fold.eq("fold_2"), ["MAE", "WIS"]] = [80., 120.]
    folds.loc[folds.policy.eq("B3") & folds.fold.eq("fold_2"), ["MAE", "WIS"]] = [120., 80.]
    assert 5 in independent_decision(folds, peak)["selection"]["failed_criteria"]["A1"]
    folds.loc[folds.policy.eq("B0") & folds.fold.eq("fold_1"), "MAE"] = 0.
    with pytest.raises(AssertionError, match="undefined B0"):
        independent_decision(folds, peak)


def _feedback_fixture(day="2020-03-29"):
    day = pd.Timestamp(day)
    hours = calendar_hours(day)
    issued = pd.DataFrame(dict(policy="A1", delivery_date=day, timestamp_utc=hours,
                               central=np.full(len(hours), 10.), scale=np.full(len(hours), 2.)))
    raw = pd.DataFrame(dict(timestamp_utc=hours, price_eur_mwh=np.full(len(hours), 14.)))
    feedback = pd.DataFrame([dict(policy="A1", feedback_day=str(day.date()),
                                  origin=str((day + pd.Timedelta(days=2)).date()), status="consumed", n=len(hours),
                                  issued_center_sha256=digest_array(np.full(len(hours), 10.)),
                                  issued_scale_sha256=digest_array(np.full(len(hours), 2.)),
                                  error_sha256=digest_array(np.full(len(hours), 2.)))])
    return issued, feedback, raw


@pytest.mark.parametrize("day,n", [("2020-03-29", 23), ("2020-10-25", 25), ("2020-07-01", 24)])
def test_feedback_checker_dst_positive_control(day, n):
    issued, feedback, raw = _feedback_fixture(day)
    errors = check_feedback(issued, feedback, raw)
    assert len(next(iter(errors.values()))[1]) == n


@pytest.mark.parametrize("mutation", ["early", "twice", "center", "scale", "error", "missing_hour"])
def test_feedback_checker_rejects_mutation(mutation):
    issued, feedback, raw = _feedback_fixture()
    check_feedback(issued, feedback, raw)
    if mutation == "early":
        feedback.loc[0, "origin"] = "2020-03-30"
    elif mutation == "twice":
        feedback = pd.concat([feedback, feedback])
    elif mutation in ("center", "scale", "error"):
        column = {"center": "issued_center_sha256", "scale": "issued_scale_sha256", "error": "error_sha256"}[mutation]
        feedback.loc[0, column] = "0" * 64
    else:
        issued = issued.iloc[:-1]
    with pytest.raises(AssertionError):
        check_feedback(issued, feedback, raw)


def test_independent_normalization_exact_168_and_floor():
    hours = pd.date_range("2020-03-15", "2020-04-02", freq="h", tz="Europe/Berlin").tz_convert("UTC")
    raw = pd.DataFrame(dict(timestamp_utc=hours, delivery_date=hours.tz_convert("Europe/Berlin").date,
                            price_eur_mwh=np.arange(len(hours), dtype=float)))
    level, scale = independent_origin_stats(raw)
    day = pd.Timestamp("2020-03-30")
    mask = pd.to_datetime(raw.delivery_date).eq(day)
    end = hours.get_loc(calendar_hours(day)[0])
    close(level[mask], np.mean(np.arange(end - 168, end)))
    close(scale[mask], np.std(np.arange(end - 168, end), ddof=1))
    raw.price_eur_mwh = 42.
    _, flat = independent_origin_stats(raw)
    close(flat[mask], 1.)


def test_preservation_checker_detects_modified_bytes(tmp_path):
    report = tmp_path / "reports/cp15"
    report.mkdir(parents=True)
    old = report / "old.txt"
    old.write_bytes(b"old evidence")
    record = {"evidence_tip": "a" * 40, "mapping": {"original.txt": {
        "preserved_at": "reports/cp15/old.txt", "sha256": hashlib.sha256(old.read_bytes()).hexdigest()}}}
    (report / "attempt-1-preservation.json").write_text(json.dumps(record))
    check_preservation(tmp_path)
    old.write_bytes(b"changed")
    with pytest.raises(AssertionError):
        check_preservation(tmp_path)


def _interval_fixture():
    recovered, issued, predictions, metadata = {}, [], [], {}
    day = pd.Timestamp("2020-01-30")
    dates = pd.date_range("2020-01-01", periods=28, freq="D")
    errors = np.repeat(np.arange(28, dtype=float), 24)
    # Exact linear quantiles of 0..27, each repeated 24 times.
    quantiles = np.array([0., 2., 6.75, 13.5, 20.25, 25., 27.])
    for policy in ROLLING:
        for i, date in enumerate(dates):
            recovered[(policy, date)] = (date + pd.Timedelta(days=2), np.full(24, float(i)))
        metadata[policy] = {"buffer_start": "2020-01-01", "buffer_end": "2020-01-28",
                            "buffer_days": 28, "buffer_hours": 672, "buffer_sha256": digest_array(errors)}
        for hour in calendar_hours(day)[:2]:
            row = dict(policy=policy, delivery_date=day, timestamp_utc=hour, central=100., scale=3.)
            issued.append(row.copy())
            row.update(dict(zip(QUANTILES, 100 + (3 if policy in ADAPTIVE else 1) * quantiles)))
            predictions.append(row)
    origins = [{"delivery_date": str(day.date()), "buffer": metadata}]
    return pd.DataFrame(predictions), pd.DataFrame(issued), origins, recovered


@pytest.mark.parametrize("mutation", ["none", "quantile", "scale", "buffer_end", "buffer_hash", "missing_day"])
def test_interval_replay_checker_positive_and_mutations(mutation):
    predictions, issued, origins, recovered = _interval_fixture()
    check_reconstructed_intervals(predictions, issued, origins, recovered)
    if mutation == "none":
        return
    if mutation == "quantile":
        predictions.loc[0, "p975"] += 1
    elif mutation == "scale":
        issued.loc[issued.policy.eq("A1"), "scale"] = 4.
    elif mutation == "buffer_end":
        origins[0]["buffer"]["A1"]["buffer_end"] = "2020-01-27"
    elif mutation == "buffer_hash":
        origins[0]["buffer"]["A1"]["buffer_sha256"] = "0" * 64
    else:
        recovered.pop(("A1", pd.Timestamp("2020-01-28")))
    with pytest.raises(AssertionError):
        check_reconstructed_intervals(predictions, issued, origins, recovered)


def _fit_fixture():
    day = pd.Timestamp("2020-04-01")
    hours = pd.date_range("2019-01-01", day, freq="h", tz="Europe/Berlin", inclusive="left").tz_convert("UTC")
    raw = pd.DataFrame(dict(timestamp_utc=hours, delivery_date=hours.tz_convert("Europe/Berlin").date,
                            price_eur_mwh=np.arange(len(hours), dtype=float)))
    eligible, level, scale = np.ones(len(raw), bool), np.zeros(len(raw)), np.ones(len(raw))
    dates = pd.to_datetime(raw.delivery_date)
    records = []
    for policy in ("B2", "B3", "A1", "A2", "A4"):
        lower = day - pd.Timedelta(days=84) if policy == "A4" else pd.Timestamp("2019-01-01")
        train = np.flatnonzero(dates.ge(lower).to_numpy())
        common = dict(policy=policy, delivery_date=day, history_start=str(lower.date()),
                      history_end_exclusive=str(day.date()), n_train=len(train),
                      train_rows_sha256=digest_array(train),
                      normalization_rows_sha256=digest_array(np.column_stack((level[train], scale[train]))),
                      train_target_sha256=digest_array(raw.price_eur_mwh.to_numpy()[train]),
                      model_sha256="a" * 64)
        if policy in ("B3", "A2"):
            records.append(common)
        else:
            for hour in range(24):
                subset = train[hours.tz_convert("Europe/Berlin").hour[train] == hour]
                records.append(common | dict(local_hour=hour, n_hour_train=len(subset),
                    hour_train_rows_sha256=digest_array(subset),
                    inner_train_end="2020-03-03", validation_start="2020-03-04", validation_end="2020-03-31",
                    selected_relative_alpha=.001, validation_mae_by_alpha={"0.001": 1., "0.01": 2., "0.1": 3., "1.0": 4.}))
    return pd.DataFrame(records), raw, eligible, level, scale


@pytest.mark.parametrize("mutation", ["none", "window", "rows_hash", "normalization", "target_hash", "hour_count", "alpha", "missing_fit"])
def test_fit_lineage_checker_positive_and_mutations(mutation):
    fits, raw, eligible, level, scale = _fit_fixture()
    check_fit_records(fits, raw, eligible, level, scale)
    if mutation == "none":
        return
    if mutation == "window":
        fits.loc[0, "history_start"] = "2018-12-31"
    elif mutation == "rows_hash":
        fits.loc[0, "train_rows_sha256"] = "0" * 64
    elif mutation == "normalization":
        level[0] = 1.
    elif mutation == "target_hash":
        fits.loc[0, "train_target_sha256"] = "0" * 64
    elif mutation == "hour_count":
        fits.loc[0, "n_hour_train"] -= 1
    elif mutation == "alpha":
        fits.loc[0, "selected_relative_alpha"] = .01
    else:
        fits = fits.iloc[1:]
    with pytest.raises(AssertionError):
        check_fit_records(fits, raw, eligible, level, scale)


def test_fit_count_follows_issued_local_hours_not_a_fixed_24():
    fits, raw, eligible, level, scale = _fit_fixture()
    day = pd.Timestamp("2020-04-01")
    shortened = fits.loc[~(fits.policy.isin(["B2", "A1", "A4"]) & fits.local_hour.eq(2))]
    assert len(shortened) == 71
    check_fit_records(shortened, raw, eligible, level, scale, {day: set(range(24)) - {2}})
    with pytest.raises(AssertionError):
        check_fit_records(shortened, raw, eligible, level, scale, {day: set(range(24))})


@pytest.fixture(scope="module")
def diagnostic_control():
    frame = _analytic_predictions()
    extras = []
    for policy in POLICIES:
        first = frame.loc[frame.policy.eq(policy) & frame.fold.eq("fold_1")].iloc[0].copy()
        first["timestamp_utc"] += pd.Timedelta(hours=3)
        first["y_true"] = 20.
        extras.append(first)
        recovery = frame.loc[frame.policy.eq(policy) & frame.fold.eq("fold_3")].iloc[0].copy()
        recovery["delivery_date"] = pd.Timestamp("2022-09-01")
        recovery["timestamp_utc"] = calendar_hours("2022-09-01")[0]
        recovery["y_true"] = 11.
        extras.append(recovery)
    frame = pd.concat([frame, pd.DataFrame(extras)], ignore_index=True)
    windows = {}
    for fold, rows in frame.groupby("fold"):
        start = pd.Timestamp("2022-07-01") if fold == "fold_3" else rows.delivery_date.min()
        windows[fold] = (start, start + pd.Timedelta(days=89))
    return independent_diagnostics(frame, windows)


def test_diagnostic_checker_exact_pooling_peak_and_empty_days(diagnostic_control):
    pooled = diagnostic_control["pooled"].set_index("policy").loc["B0"]
    assert pooled.n_hours == 17 and pooled.n_days == 6
    close(pooled.MAE, 91 / 17)
    close(pooled.daily_mean_level_MAE, 1.625)
    close(pooled.within_day_shape_MAE, 5.)
    peak = diagnostic_control["peak"].set_index("policy").loc["B0"]
    assert peak.n_hours == 3 and peak.n_days == 1 and peak.calendar_days == 17
    assert peak.hit_count95 == peak.lower_miss_count95 == peak.upper_miss_count95 == 1
    daily = diagnostic_control["daily"]
    assert len(daily) == 4050
    absent = daily.loc[daily.policy.eq("B0") & daily.delivery_date.eq(pd.Timestamp("2022-08-16"))].iloc[0]
    assert absent.n_hours == 0 and absent.n_days == 0 and pd.isna(absent.MAE) and pd.isna(absent.coverage95)
    recovery = diagnostic_control["recovery"].query("policy == 'B0'").sort_values("window_start")
    assert recovery.n_hours.tolist() == [1, 0, 0, 0]
    close(recovery.MAE.iloc[0], 6.)
    assert recovery.MAE.iloc[1:].isna().all()


@pytest.mark.parametrize("name,column", [("pooled", "MAE"), ("peak", "hit_count95"),
                                         ("daily", "n_hours"), ("recovery", "MAE")])
def test_diagnostic_checker_detects_saved_mutations(diagnostic_control, name, column):
    expected = diagnostic_control[name]
    keys = {"pooled": ["policy"], "peak": ["policy", "window_start", "window_end"],
            "daily": ["policy", "fold", "delivery_date"],
            "recovery": ["policy", "fold", "window_start", "window_end"]}[name]
    compare_numeric_table(expected.copy(), expected, keys, [column])
    altered = expected.copy()
    altered.loc[0, column] += 1
    with pytest.raises(AssertionError):
        compare_numeric_table(altered, expected, keys, [column])


def _bootstrap_daily_fixture():
    records = []
    for i, fold in enumerate(FOLDS):
        for d, date in enumerate(pd.date_range(pd.Timestamp(2020 + i, 1, 1), periods=90)):
            for j, policy in enumerate(POLICIES):
                value = np.nan if d == 17 else 10 + d * (j + 1) / 10
                records.append(dict(fold=fold, policy=policy, delivery_date=date, MAE=value, WIS=2 * value))
    return pd.DataFrame(records)


def _bootstrap_protocol():
    return {"bootstrap_seed": 15042, "bootstrap": {"replicates": 2000, "block_days": 7}}


def test_bootstrap_checker_seed_pairing_and_independent_matrix_oracle():
    daily = _bootstrap_daily_fixture()
    result = independent_bootstrap(daily, _bootstrap_protocol())
    assert len(result) == 240
    # Separate vectorized oracle for fold1; the checker uses scalar replicates.
    rng = np.random.default_rng(15042)
    starts = rng.integers(0, 84, size=(2000, 13))
    sampled = (starts[:, :, None] + np.arange(7)).reshape(2000, -1)[:, :90]
    valid = sampled != 17
    expected_samples = np.where(valid, sampled * .4, 0.).sum(axis=1) / valid.sum(axis=1)
    expected_interval = np.quantile(expected_samples, [.025, .975])
    fold_draws = [expected_samples]
    for fold in FOLDS[1:]:
        next_starts = rng.integers(0, 84, size=(2000, 13))
        next_sampled = (next_starts[:, :, None] + np.arange(7)).reshape(2000, -1)[:, :90]
        next_valid = next_sampled != 17
        draws = np.where(next_valid, next_sampled * .4, 0.).sum(axis=1) / next_valid.sum(axis=1)
        fold_draws.append(draws)
        actual_fold = result.loc[result.scope.eq(fold) & result.candidate.eq("A1")
                                 & result.baseline.eq("B0") & result.metric.eq("MAE")].iloc[0]
        close([actual_fold.ci_lower, actual_fold.ci_upper], np.quantile(draws, [.025, .975]))
    aggregate = result.query("scope == 'equal_fold' and candidate == 'A1' and baseline == 'B0' and metric == 'MAE'").iloc[0]
    close([aggregate.ci_lower, aggregate.ci_upper], np.quantile(np.mean(fold_draws, axis=0), [.025, .975]))
    row = result.query("scope == 'fold_1' and candidate == 'A1' and baseline == 'B0' and metric == 'MAE'").iloc[0]
    close(row.difference, np.mean([.4 * d for d in range(90) if d != 17]))
    close([row.ci_lower, row.ci_upper], expected_interval)
    wis = result.query("scope == 'fold_1' and candidate == 'A1' and baseline == 'B0' and metric == 'WIS'").iloc[0]
    close([wis.ci_lower, wis.ci_upper], 2 * expected_interval)
    pd.testing.assert_frame_equal(result, independent_bootstrap(daily, _bootstrap_protocol()))
    altered = result.copy()
    altered.loc[0, "ci_lower"] += .001
    with pytest.raises(AssertionError):
        compare_numeric_table(altered, result, ["scope", "candidate", "baseline", "metric"], ["ci_lower"])


def test_bootstrap_checker_missing_day_is_not_a_zero_loss():
    daily = _bootstrap_daily_fixture()
    for i, policy in enumerate(POLICIES):
        mask = daily.policy.eq(policy) & daily.MAE.notna()
        daily.loc[mask, ["MAE", "WIS"]] = [i + 1., 2 * i + 2.]
    result = independent_bootstrap(daily, _bootstrap_protocol())
    for row in result.itertuples(index=False):
        expected = POLICIES.index(row.candidate) - POLICIES.index(row.baseline)
        expected *= 2 if row.metric == "WIS" else 1
        close([row.difference, row.ci_lower, row.ci_upper], expected)


@pytest.mark.parametrize("mutation", ["gap", "unpaired", "seed", "replicates", "block"])
def test_bootstrap_checker_refuses_invalid_calendar_or_protocol(mutation):
    daily, protocol = _bootstrap_daily_fixture(), _bootstrap_protocol()
    if mutation == "gap":
        daily = daily.loc[~daily.delivery_date.eq(pd.Timestamp("2020-01-01"))]
    elif mutation == "unpaired":
        daily.loc[0, "MAE"] = np.nan
    elif mutation == "seed":
        protocol["bootstrap_seed"] = 42
    elif mutation == "replicates":
        protocol["bootstrap"]["replicates"] = 1000
    else:
        protocol["bootstrap"]["block_days"] = 1
    with pytest.raises(AssertionError):
        independent_bootstrap(daily, protocol)


@pytest.mark.parametrize('day,source_day', [('2020-01-08','2020-01-07'), ('2020-01-11','2020-01-04')])
@pytest.mark.parametrize('mutation', ['none', 'B0', 'A3', 'A5'])
def test_issued_policy_definition_checker_has_positive_controls(day, source_day, mutation):
    index = pd.date_range('2020-01-01', '2020-01-12', freq='h', inclusive='left', tz='Europe/Berlin').tz_convert('UTC')
    raw = pd.DataFrame({'timestamp_utc': index, 'delivery_date': index.tz_convert('Europe/Berlin').date,
                        'price_eur_mwh': np.arange(len(index), dtype=float)})
    baseline = raw.loc[pd.to_datetime(raw.delivery_date).eq(pd.Timestamp(source_day)), 'price_eur_mwh'].to_numpy()
    target = calendar_hours(day)
    centers = {'B0': baseline, 'B2': baseline+1, 'B3': baseline+2,
               'A1': baseline+3, 'A2': baseline+6, 'A4': baseline+12}
    centers['A3'] = baseline+4.5
    centers['A5'] = baseline+7
    issued = pd.concat([pd.DataFrame({'policy': policy, 'timestamp_utc': target,
        'delivery_date': pd.Timestamp(day), 'central': center}) for policy, center in centers.items()], ignore_index=True)
    if mutation != 'none':
        issued.loc[issued.policy.eq(mutation), 'central'] += 1
        with pytest.raises(AssertionError):
            check_issued_policy_definitions(issued, raw)
    else:
        check_issued_policy_definitions(issued, raw)
