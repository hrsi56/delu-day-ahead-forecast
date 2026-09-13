"""CP-2 stage 4 -- SHAP, permutation importance, regime table, reliability (§8).

Which model gets explained, and on which rows, is the only real decision here.
The frozen champion was fit on *every* development row, so SHAP on it over the
validation tail would be in-sample; the holdout is closed to development
diagnostics (§5.1). Fold 5's model on fold 5's eval block is therefore the only
genuinely out-of-sample surface in the development set, and it is the most recent
and fully post-15-minute-transition one. The frozen champion is explained on the
same rows as a secondary, explicitly labelled in-sample read.

    uv run python scripts/cp2_diagnostics.py
"""

from __future__ import annotations

import json
import time
from datetime import date
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
from sklearn.inspection import permutation_importance

from delu_forecast.benchmark import DUNKELFLAUTE_VRE_SHARE_THRESHOLD, dunkelflaute_days
from delu_forecast.experiment import experiment_params, load_inputs, mask_for
from delu_forecast.metrics import (
    COVERAGE_LEVELS,
    QUANTILES,
    bootstrap_day_ci,
    interval_coverage,
    mae,
    pinball_matrix,
    pooled_mean_pinball,
)
from delu_forecast.model import SEED, fit_quantile_heads, predict_raw_heads
from delu_forecast.postprocess import QUANTILE_LABELS
from delu_forecast.tracking import configure_tracking, log_decision_record, record_timing, run

OUT = Path("reports/cp2")
MEDIAN = "p50"
THIN_STRATUM_ROWS = 3_000
CRISIS = (date(2021, 9, 1), date(2022, 12, 31))
DUNKELFLAUTE_WEEK = (date(2024, 12, 9), date(2024, 12, 15))
AUGUST_PEAK = (date(2022, 8, 15), date(2022, 8, 31))


def _fit_fold_model(inputs, fold, catalog):
    train = mask_for(inputs, fold.proper_training)
    return fit_quantile_heads(inputs.matrix(catalog, train), inputs.target[train]), train


def _stratum_metrics(y, matrix, days, label, n_thin=THIN_STRATUM_ROWS):
    if len(y) == 0:
        return {"stratum": label, "n_obs": 0}
    row = {
        "stratum": label,
        "n_obs": int(len(y)),
        "n_days": int(pd.Index(days).nunique()),
        "mae": mae(y, matrix[:, 4]),
        "mean_pinball": pooled_mean_pinball(y, matrix),
    }
    row.update({f"coverage_{k}": v for k, v in interval_coverage(y, matrix).items()})
    if len(y) < n_thin:  # thin subsets carry bootstrap CIs and are read qualitatively
        low, high = bootstrap_day_ci(np.abs(y - matrix[:, 4]), pd.Index(days), seed=SEED)
        row["mae_ci95_low"], row["mae_ci95_high"] = low, high
        low, high = bootstrap_day_ci(pinball_matrix(y, matrix).mean(axis=1), pd.Index(days), seed=SEED)
        row["pinball_ci95_low"], row["pinball_ci95_high"] = low, high
        row["read"] = "qualitative (thin subset)"
    else:
        row["read"] = "quantitative"
    return row


def main() -> None:
    started = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    inputs = load_inputs()
    enabled = configure_tracking()
    selected = json.loads((OUT / "catalog_selection.json").read_text())["selected_catalog"]
    columns = inputs.arm_columns(selected)

    # ---- SHAP and permutation importance, fold 5, out of sample -----------
    fold5 = inputs.spec.fold("fold_5")
    heads, train_mask = _fit_fold_model(inputs, fold5, selected)
    eval_mask = mask_for(inputs, fold5.evaluation)
    x_eval = inputs.matrix(selected, eval_mask)
    y_eval = inputs.target[eval_mask]

    explainer = shap.TreeExplainer(heads[MEDIAN])
    shap_values = explainer.shap_values(x_eval)
    mean_abs = np.abs(shap_values).mean(axis=0)
    ranking = (
        pd.DataFrame({"feature": columns, "mean_abs_shap": mean_abs})
        .sort_values("mean_abs_shap", ascending=False)
        .reset_index(drop=True)
    )
    ranking["rank"] = ranking.index + 1
    ranking.to_csv(OUT / "shap_ranking.csv", index=False)

    plt.figure()
    shap.summary_plot(shap_values, x_eval, show=False, max_display=15)
    plt.title("SHAP - p50 head, champion catalog, fold 5 eval (out of sample)")
    plt.tight_layout()
    plt.savefig(OUT / "fig_shap_summary.png", dpi=130)
    plt.close("all")

    top_two = ranking["feature"].head(2).tolist()
    for feature in top_two:
        plt.figure()
        shap.dependence_plot(feature, shap_values, x_eval, interaction_index="local_hour", show=False)
        plt.tight_layout()
        plt.savefig(OUT / f"fig_shap_dependence_{feature}.png", dpi=130)
        plt.close("all")

    permutation = permutation_importance(
        heads[MEDIAN], x_eval, y_eval, n_repeats=10, random_state=SEED, scoring="neg_mean_absolute_error", n_jobs=1
    )
    permutation_table = (
        pd.DataFrame(
            {
                "feature": columns,
                "importance_mean_mae_increase": permutation.importances_mean,
                "importance_std": permutation.importances_std,
            }
        )
        .sort_values("importance_mean_mae_increase", ascending=False)
        .reset_index(drop=True)
    )
    permutation_table["rank"] = permutation_table.index + 1
    permutation_table.to_csv(OUT / "permutation_importance.csv", index=False)

    merged = ranking.merge(permutation_table, on="feature", suffixes=("_shap", "_perm"))
    rank_agreement = float(merged["rank_shap"].corr(merged["rank_perm"], method="spearman"))

    # ---- frozen champion, same rows, in-sample, for continuity -------------
    import cloudpickle

    frozen = cloudpickle.loads(Path("models/champion/python_model.pkl").read_bytes())
    frozen_shap = shap.TreeExplainer(frozen.heads[MEDIAN]).shap_values(x_eval)
    frozen_ranking = (
        pd.DataFrame({"feature": columns, "mean_abs_shap": np.abs(frozen_shap).mean(axis=0)})
        .sort_values("mean_abs_shap", ascending=False)
        .reset_index(drop=True)
    )
    frozen_ranking["rank"] = frozen_ranking.index + 1
    frozen_ranking.to_csv(OUT / "shap_ranking_frozen_champion_in_sample.csv", index=False)

    # ---- regime-stratified error table -------------------------------------
    predictions = pd.read_parquet(OUT / "development_predictions.parquet")
    predictions = predictions[predictions["arm"] == selected].reset_index(drop=True)
    final = predictions[[f"final_{label}" for label in QUANTILE_LABELS]].to_numpy()
    y = predictions["y_true"].to_numpy()
    days = pd.Index(predictions["delivery_date"].to_numpy())
    weekday = np.array([value.weekday() for value in days])
    flags = dunkelflaute_days(inputs.snapshot)
    is_flag = days.map(flags).to_numpy().astype(bool)

    strata: list[tuple[str, np.ndarray]] = [
        ("all validation folds", np.ones(len(y), dtype=bool)),
        ("Dunkelflaute days (A69 stratum)", is_flag),
        ("non-flag days", ~is_flag),
        ("pre-crisis (< 2021-09-01)", np.array([value < CRISIS[0] for value in days])),
        ("crisis (2021-09-01 .. 2022-12-31)", np.array([CRISIS[0] <= value <= CRISIS[1] for value in days])),
        ("post-crisis (>= 2023-01-01)", np.array([value >= date(2023, 1, 1) for value in days])),
        ("negative-price hours", y < 0.0),
        ("weekday", weekday < 5),
        ("weekend", weekday >= 5),
        ("August-2022 peak weeks", np.array([AUGUST_PEAK[0] <= value <= AUGUST_PEAK[1] for value in days])),
    ]
    rows = [_stratum_metrics(y[mask], final[mask], days[mask], label) for label, mask in strata]

    # One finer stress row from training-period backtesting: the December-2024
    # Dunkelflaute week sits in no eval block, so it is scored with fold 3's
    # model -- the most recent fold whose proper training ends before it. That
    # model is two and a half years stale by then, and the row is labelled so.
    backtest_heads, _ = _fit_fold_model(inputs, inputs.spec.fold("fold_3"), selected)
    week = np.array([DUNKELFLAUTE_WEEK[0] <= value <= DUNKELFLAUTE_WEEK[1] for value in inputs.delivery_dates])
    week &= inputs.eligible
    if week.any():
        raw_week = predict_raw_heads(backtest_heads, inputs.matrix(selected, week))
        entry = _stratum_metrics(
            inputs.target[week], raw_week, inputs.delivery_dates[week],
            "Dec-2024 Dunkelflaute week (backtest, fold-3 model, raw heads, 2.5y stale)",
        )
        entry["read"] = "qualitative (backtest outside every eval block; raw heads, uncalibrated)"
        rows.append(entry)

    regime = pd.DataFrame(rows)
    regime.to_csv(OUT / "regime_table.csv", index=False)
    if int(regime["n_obs"].eq(0).sum()):
        raise AssertionError("a stratum is empty; the table must not render a row without n_obs")

    # ---- three-stage reliability diagram ------------------------------------
    stage_rows = []
    for stage, prefix in (("raw LightGBM", "raw"), ("post-CQR / pre-isotonic", "cqr"), ("final post-isotonic", "final")):
        matrix = predictions[[f"{prefix}_{label}" for label in QUANTILE_LABELS]].to_numpy()
        for level, value in interval_coverage(y, matrix).items():
            stage_rows.append({"stage": stage, "nominal": int(level) / 100.0, "empirical": value})
    reliability = pd.DataFrame(stage_rows)
    reliability.to_csv(OUT / "reliability_three_stage.csv", index=False)

    plt.figure(figsize=(6, 5.5))
    plt.plot([0, 1], [0, 1], "k--", lw=1, label="perfect calibration")
    for stage, group in reliability.groupby("stage", sort=False):
        plt.plot(group["nominal"], group["empirical"], marker="o", label=stage)
    plt.xlabel("nominal coverage")
    plt.ylabel("empirical coverage (five development folds)")
    plt.title("Reliability at three stages (§6.2 / §8.4)")
    plt.legend(loc="upper left", fontsize=8)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUT / "fig_reliability_three_stage.png", dpi=130)
    plt.close("all")

    summary = {
        "shap_surface": "p50 head of the champion catalog's fold-5 model, scored on fold 5's eval block "
        "(2026-01-08..2026-04-07) -- out of sample for that model",
        "shap_top10": ranking.head(10).to_dict("records"),
        "permutation_top10": permutation_table.head(10).to_dict("records"),
        "shap_vs_permutation_rank_spearman": rank_agreement,
        "frozen_champion_shap_top10_in_sample": frozen_ranking.head(10).to_dict("records"),
        "scoping": "SHAP on the p50 head explains central tendency, not interval width. Interval "
        "width is driven by the inter-quantile spread and the CQR shift Q. SHAP explains the "
        "selected champion; it is not the incremental-value test -- that is the §4.1 two-arm "
        "comparison, which selected `base`.",
        "dunkelflaute_definition": "delivery day whose mean A69 VRE forecast is below "
        f"{DUNKELFLAUTE_VRE_SHARE_THRESHOLD:.0%} of its mean A65 load forecast; a post-hoc "
        "evaluation stratum only, never a champion feature",
        "n_dunkelflaute_days_in_snapshot": int(flags.sum()),
        "quantiles": list(QUANTILES),
        "coverage_levels": [name for name, _, _ in COVERAGE_LEVELS],
    }
    (OUT / "diagnostics.json").write_text(json.dumps(summary, indent=2, sort_keys=True, default=str) + "\n")

    print(regime.to_string(index=False))
    print("\nSHAP top 10:\n", ranking.head(10).to_string(index=False))
    print("\nPermutation top 10:\n", permutation_table.head(10).to_string(index=False))
    print(f"\nSHAP vs permutation rank Spearman: {rank_agreement:.3f}")
    print("\nReliability:\n", reliability.to_string(index=False))

    with run("diagnostics::champion", enabled=enabled, tags={"stage": "diagnostics"}):
        log_decision_record(
            enabled,
            params=experiment_params(selected, inputs, {
                "selected_catalog": selected,
                "shap_surface": summary["shap_surface"],
                "dunkelflaute_definition": summary["dunkelflaute_definition"],
            }),
            metrics={"shap_vs_permutation_rank_spearman": rank_agreement},
            artifacts=[
                OUT / "shap_ranking.csv", OUT / "permutation_importance.csv", OUT / "regime_table.csv",
                OUT / "reliability_three_stage.csv", OUT / "fig_shap_summary.png",
                OUT / "fig_reliability_three_stage.png", OUT / "diagnostics.json",
            ],
        )
    record_timing("diagnostics_seconds", time.time() - started)


if __name__ == "__main__":
    main()
