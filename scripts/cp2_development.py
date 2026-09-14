"""CP-2 stage 1 -- baselines, the two-arm catalog comparison, and development DM.

Runs the three §7 baselines and both frozen catalogs on the five pinned folds,
decides the catalog by the one mechanical §4.1 rule, and reports both DM analyses
with `evidence_class = development_post_selection`. Nothing here touches the final
calibration slice or the holdout.

    uv run python scripts/cp2_development.py
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

from delu_forecast.experiment import (
    CATALOG_AUGMENTED,
    CATALOG_BASE,
    baseline_predictions,
    calibration_frame,
    experiment_params,
    load_inputs,
    mask_for,
    pooled_raw_pinball,
    run_arm,
    stacked_frame,
)
from delu_forecast.metrics import (
    QUANTILE_LABELS,
    crossing_violations,
    daily_absolute_error_series,
    daily_pinball_series,
    diebold_mariano,
    interval_coverage,
    mae,
    point_forecast_quantiles,
    pooled_mean_pinball,
)
from delu_forecast.tracking import record_timing, configure_tracking, log_decision_record, public_tracking_url, run

OUT = Path("reports/cp2")
EVIDENCE_CLASS = "development_post_selection"
BASELINE_NAMES = ("similar_day_naive", "seasonal_naive_168h", "ridge")
HEADLINE_COMPARATOR = "similar_day_naive"


def main() -> None:
    started = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    inputs = load_inputs()
    enabled = configure_tracking()
    print(f"eligible rows: {int(inputs.eligible.sum())} / {len(inputs.eligible)}   mlflow: {enabled}")

    # -- baselines -------------------------------------------------------
    baseline_rows: list[pd.DataFrame] = []
    for fold in inputs.spec.development_folds:
        evaluation = mask_for(inputs, fold.evaluation)
        predictions = baseline_predictions(inputs, fold)
        frame = pd.DataFrame(
            {"fold": fold.name, "delivery_date": inputs.delivery_dates[evaluation], "y_true": inputs.target[evaluation]}
        )
        for name, values in predictions.items():
            frame[name] = values
        baseline_rows.append(frame)
        print(f"  baselines {fold.name}: n_eval={int(evaluation.sum())}")
    baselines = pd.concat(baseline_rows, ignore_index=True)
    baselines.to_parquet(OUT / "development_baselines.parquet", index=False)

    # -- the two frozen catalogs ------------------------------------------
    arms: dict[str, list] = {}
    for arm in (CATALOG_BASE, CATALOG_AUGMENTED):
        elapsed = time.time()
        arms[arm] = run_arm(inputs, arm)
        print(f"  arm {arm}: {time.time() - elapsed:.1f}s")
    predictions = pd.concat([stacked_frame(arms[arm]) for arm in arms], ignore_index=True)
    predictions.to_parquet(OUT / "development_predictions.parquet", index=False)
    calibration = pd.concat([calibration_frame(arms[arm]) for arm in arms], ignore_index=True)
    calibration.to_parquet(OUT / "development_calibration_predictions.parquet", index=False)
    (OUT / "development_fold_thresholds.json").write_text(
        json.dumps(
            {
                "note": "recompute these from development_calibration_predictions.parquet: "
                "E_i = max(q_lo - y, y - q_hi) per pair, ascending sort, one-based rank "
                "k = ceil((n_cal+1)(1-alpha)) read as scores[k-1]",
                "alphas": {"p025_p975": 0.05, "p05_p95": 0.10, "p10_p90": 0.20, "p25_p75": 0.50},
                "thresholds": {arm: {item.fold: item.thresholds for item in results} for arm, results in arms.items()},
                "n_calibration": {arm: {item.fold: item.n_calibration for item in results} for arm, results in arms.items()},
            },
            indent=2, sort_keys=True,
        )
        + "\n"
    )

    # -- matched-row proof -------------------------------------------------
    keys = {
        arm: pd.MultiIndex.from_arrays(
            [np.concatenate([item.delivery_dates for item in results]), np.arange(sum(len(i.y_true) for i in results))]
        )
        for arm, results in arms.items()
    }
    if not keys[CATALOG_BASE].equals(keys[CATALOG_AUGMENTED]):
        raise AssertionError("the two arms did not evaluate identical rows")
    y_base = np.concatenate([item.y_true for item in arms[CATALOG_BASE]])
    y_aug = np.concatenate([item.y_true for item in arms[CATALOG_AUGMENTED]])
    if not np.array_equal(y_base, y_aug):
        raise AssertionError("the two arms did not evaluate identical targets")

    # -- §4.1 selection ----------------------------------------------------
    pooled = {arm: pooled_raw_pinball(results) for arm, results in arms.items()}
    difference_pct = 100.0 * (pooled[CATALOG_AUGMENTED] - pooled[CATALOG_BASE]) / pooled[CATALOG_BASE]
    selected = CATALOG_AUGMENTED if pooled[CATALOG_AUGMENTED] < pooled[CATALOG_BASE] else CATALOG_BASE
    proxy_nan_eval = int(
        inputs.wide_features.loc[
            np.logical_or.reduce([mask_for(inputs, f.evaluation) for f in inputs.spec.development_folds]),
            "residual_load_proxy",
        ]
        .isna()
        .sum()
    )
    selection = {
        "rule": "the augmented catalog ships only if its unrounded stored pooled mean "
        "pinball loss is lower; equality defaults to base",
        "metric": "pooled observation-weighted raw-head mean pinball loss over nine quantiles and five folds",
        "pooled_mean_pinball": {arm: repr(value) for arm, value in pooled.items()},
        "pooled_mean_pinball_float": pooled,
        "percentage_difference_augmented_vs_base": difference_pct,
        "selected_catalog": selected,
        "equality": pooled[CATALOG_AUGMENTED] == pooled[CATALOG_BASE],
        "matched_rows": int(len(y_base)),
        "eval_rows_with_null_residual_load_proxy": proxy_nan_eval,
        "seed": 42,
        "evidence_class": EVIDENCE_CLASS,
    }
    print(f"\npooled raw pinball  base={pooled[CATALOG_BASE]!r}  augmented={pooled[CATALOG_AUGMENTED]!r}")
    print(f"percentage difference (augmented vs base) = {difference_pct:+.6f}%   selected: {selected}\n")

    # -- per-fold metric table --------------------------------------------
    rows: list[dict[str, object]] = []
    for arm, results in arms.items():
        for item in results:
            rows.append({"model": arm, "fold": item.fold, **item.metrics})
    for name in BASELINE_NAMES:
        for fold_name, group in baselines.groupby("fold", sort=True):
            degenerate = point_forecast_quantiles(group[name].to_numpy())
            usable = np.isfinite(group[name].to_numpy())
            rows.append(
                {
                    "model": name,
                    "fold": fold_name,
                    "n_eval": float(usable.sum()),
                    "mae_final_p50": mae(group["y_true"].to_numpy()[usable], group[name].to_numpy()[usable]),
                    "pinball_final": pooled_mean_pinball(group["y_true"].to_numpy()[usable], degenerate[usable]),
                }
            )
    table = pd.DataFrame(rows)
    table.to_csv(OUT / "development_metrics.csv", index=False)

    # -- pooled headline metrics -------------------------------------------
    pooled_rows: list[dict[str, object]] = []
    for arm, results in arms.items():
        y = np.concatenate([item.y_true for item in results])
        for stage in ("raw", "post_cqr", "final"):
            matrix = np.concatenate([getattr(item, stage) for item in results], axis=0)
            entry = {
                "model": arm,
                "stage": stage,
                "n_obs": int(len(y)),
                "mae_p50": mae(y, matrix[:, 4]),
                "mean_pinball": pooled_mean_pinball(y, matrix),
                "crossing_violations": crossing_violations(matrix),
            }
            entry.update({f"coverage_{k}": v for k, v in interval_coverage(y, matrix).items()})
            pooled_rows.append(entry)
    for name in BASELINE_NAMES:
        values = baselines[name].to_numpy()
        usable = np.isfinite(values)
        y = baselines["y_true"].to_numpy()[usable]
        pooled_rows.append(
            {
                "model": name,
                "stage": "point",
                "n_obs": int(usable.sum()),
                "mae_p50": mae(y, values[usable]),
                "mean_pinball": pooled_mean_pinball(y, point_forecast_quantiles(values[usable])),
                "crossing_violations": 0,
            }
        )
    pooled_table = pd.DataFrame(pooled_rows)
    pooled_table.to_csv(OUT / "development_pooled_metrics.csv", index=False)

    # -- both DM analyses, champion (selected arm, final output) vs baselines
    champion = arms[selected]
    champion_days = np.concatenate([item.delivery_dates for item in champion])
    champion_y = np.concatenate([item.y_true for item in champion])
    champion_final = np.concatenate([item.final for item in champion], axis=0)
    if not np.array_equal(champion_days, baselines["delivery_date"].to_numpy()):
        raise AssertionError("champion and baseline evaluation rows are not aligned")

    dm_results = []
    model_daily_pinball = daily_pinball_series(champion_y, champion_final, pd.Index(champion_days))
    model_daily_ae = daily_absolute_error_series(champion_y, champion_final[:, 4], pd.Index(champion_days))
    for name in BASELINE_NAMES:
        values = baselines[name].to_numpy()
        usable = np.isfinite(values)
        days = pd.Index(champion_days)[usable]
        naive_daily_pinball = daily_pinball_series(champion_y[usable], point_forecast_quantiles(values[usable]), days)
        naive_daily_ae = daily_absolute_error_series(champion_y[usable], values[usable], days)
        dm_results.append(
            diebold_mariano(
                model_daily_pinball, naive_daily_pinball,
                comparator=name, analysis="probabilistic_daily_vector_pinball", evidence_class=EVIDENCE_CLASS,
            ).to_dict()
        )
        dm_results.append(
            diebold_mariano(
                model_daily_ae, naive_daily_ae,
                comparator=name, analysis="point_median_absolute_error", evidence_class=EVIDENCE_CLASS,
            ).to_dict()
        )
    payload = {
        "selection": selection,
        "dm_tests": dm_results,
        "headline_comparator": HEADLINE_COMPARATOR,
        "dm_note": "one-sided; reject (model better) if DM < -1.645; Newey-West LRV, "
        "lag truncation floor(N^(1/3)); the champion side uses the final post-isotonic output",
        "narrative_target_pinball_improvement_pct": 15.0,
        "narrative_target_is_not_a_gate": True,
    }
    (OUT / "catalog_selection.json").write_text(json.dumps(selection, indent=2, sort_keys=True) + "\n")
    (OUT / "dm_development.json").write_text(json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n")

    # -- MLflow decision-bearing records ------------------------------------
    for arm, results in arms.items():
        y = np.concatenate([item.y_true for item in results])
        final = np.concatenate([item.final for item in results], axis=0)
        with run(f"catalog::{arm}", enabled=enabled, tags={"stage": "development", "evidence_class": EVIDENCE_CLASS}):
            log_decision_record(
                enabled,
                params=experiment_params(arm, inputs, {"selected": arm == selected, "decision_rule": selection["rule"]}),
                metrics={
                    "pooled_raw_mean_pinball": pooled[arm],
                    "pooled_final_mean_pinball": pooled_mean_pinball(y, final),
                    "pooled_final_mae_p50": mae(y, final[:, 4]),
                    "crossing_violations_final": float(crossing_violations(final)),
                    **{f"fold_{item.fold}_pinball_raw": item.metrics["pinball_raw"] for item in results},
                    **{f"coverage_final_{k}": v for k, v in interval_coverage(y, final).items()},
                },
                artifacts=[OUT / "catalog_selection.json", OUT / "development_pooled_metrics.csv"],
            )
    for name in BASELINE_NAMES:
        values = baselines[name].to_numpy()
        usable = np.isfinite(values)
        y = baselines["y_true"].to_numpy()[usable]
        with run(f"baseline::{name}", enabled=enabled, tags={"stage": "development", "evidence_class": EVIDENCE_CLASS}):
            log_decision_record(
                enabled,
                params=experiment_params(CATALOG_BASE, inputs, {"baseline": name, "arm": name}),
                metrics={
                    "pooled_mae": mae(y, values[usable]),
                    "pooled_mean_pinball": pooled_mean_pinball(y, point_forecast_quantiles(values[usable])),
                    "n_obs": float(usable.sum()),
                },
                artifacts=[OUT / "dm_development.json"],
            )

    print(json.dumps(dm_results, indent=2, default=str))
    print(f"\ntracking: {public_tracking_url()}")
    print(f"elapsed {time.time() - started:.1f}s")
    record_timing("development_seconds", time.time() - started)


if __name__ == "__main__":
    main()
