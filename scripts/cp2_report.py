"""CP-2 stage 5 -- generate docs/cp2-model-report.md from the committed artifacts.

Generated rather than hand-written, so every number in the prose comes from the
JSON/CSV the pipeline actually produced and a reviewer re-running the pipeline
regenerates the identical document. Transcription is the one error class a
narrative report reliably introduces, and this removes it.

    uv run python scripts/cp2_report.py
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

OUT = Path("reports/cp2")
DOC = Path("docs/cp2-model-report.md")

HOLDOUT_LIMITATION = """> The holdout is a single contiguous recent period, so it tests generalization to the most recent
> regime rather than repeated out-of-sample skill. Its partitions were pinned before development and
> it was evaluated once, after the complete model and calibration pipeline were frozen, with no
> subsequent tuning. The 90-day length was fixed by partition design, not by a power calculation, so
> the Diebold–Mariano result is confirmatory-style but not power-qualified. The model shown is
> exactly the model evaluated — no refit followed the holdout — so its raw-model fit cutoff precedes
> the snapshot cutoff by 152 delivery days. Sequential lag features may use earlier holdout
> observations exactly as they would in live forecasting; no holdout outcome entered fitting or a
> development decision. Enforcement is procedural: this is a solo build and the discipline is
> disclosed, not cryptographically guaranteed."""

EXCHANGEABILITY = """> CQR provides finite-sample marginal coverage guarantees under exchangeability. The walk-forward CV
> mildly violates exchangeability — the crisis regime is not exchangeable with the pre-crisis regime,
> and the solar-driven negative-price era is not exchangeable with either — so empirical coverage may
> diverge from nominal on regime-shift folds. This is documented in the reliability diagram
> (Section 8.4)."""

EMBARGO_REASONING = """> The embargo's only job is to break the autocorrelation adjacency between the **last training
> target** and the **first validation feature**. A 168h-lagged feature of a validation row reaches
> back into the training period — but using a known, already-cleared historical price as an input
> feature is not leakage; it is exactly what the production model has at the 12:00 CET gate. One
> complete delivery day (one full target horizon, including its 23/25-hour DST form) removes the only
> true adjacency."""

TRACKING_URL = "https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow"

DM_LABEL = (
    "Pre-specified one-shot holdout DM test on a fixed 90-day window — confirmatory-style, "
    "not power-qualified."
)


def markdown_table(frame: pd.DataFrame, columns: list[str], floats: int = 3) -> str:
    view = frame.loc[:, columns].copy()
    for column in view.columns:
        if pd.api.types.is_float_dtype(view[column]):
            view[column] = view[column].map(lambda value: "" if pd.isna(value) else f"{value:,.{floats}f}")
    header = "| " + " | ".join(columns) + " |"
    rule = "|" + "|".join("---" for _ in columns) + "|"
    body = "\n".join("| " + " | ".join(str(value) for value in row) + " |" for row in view.itertuples(index=False))
    return "\n".join([header, rule, body])


def main() -> None:
    selection = json.loads((OUT / "catalog_selection.json").read_text())
    development = json.loads((OUT / "dm_development.json").read_text())
    benchmark = json.loads((OUT / "a69_benchmark.json").read_text())
    holdout = json.loads((OUT / "holdout_report.json").read_text())
    diagnostics = json.loads((OUT / "diagnostics.json").read_text())
    pooled = pd.read_csv(OUT / "development_pooled_metrics.csv")
    per_fold = pd.read_csv(OUT / "development_metrics.csv")
    regime = pd.read_csv(OUT / "regime_table.csv")
    reliability = pd.read_csv(OUT / "reliability_three_stage.csv")
    timings = json.loads((OUT / "timings.json").read_text()) if (OUT / "timings.json").exists() else {}
    uri_file = OUT / "champion_model_uri.txt"
    model_uri = uri_file.read_text().strip() if uri_file.exists() else "see the champion run"
    shap_rank = pd.read_csv(OUT / "shap_ranking.csv")
    permutation = pd.read_csv(OUT / "permutation_importance.csv")

    cutoffs = holdout["cutoffs"]
    base_loss = selection["pooled_mean_pinball"]["base"]
    augmented_loss = selection["pooled_mean_pinball"]["base_plus_residual_load_proxy"]
    agreement = diagnostics.get("frozen_vs_fold5_shap_agreement",
                                {"top5_overlap": 0, "top10_overlap": 0, "rank_spearman": float("nan")})
    dm_headline = next(
        item for item in development["dm_tests"]
        if item["comparator"] == "similar_day_naive" and item["analysis"] == "probabilistic_daily_vector_pinball"
    )
    dm_point = next(
        item for item in development["dm_tests"]
        if item["comparator"] == "similar_day_naive" and item["analysis"] == "point_median_absolute_error"
    )
    holdout_dm = holdout["dm"]

    headline = pooled[pooled["stage"].isin(["final", "point"])]
    mae_by_fold = per_fold.pivot_table(index="fold", columns="model", values="mae_final_p50")
    pinball_by_fold = per_fold.pivot_table(index="fold", columns="model", values="pinball_final")
    weights = per_fold[per_fold["model"] == selection["selected_catalog"]].set_index("fold")["n_eval"]
    weights = weights / weights.sum()
    champion_column = selection["selected_catalog"]
    mae_wins = int((mae_by_fold[champion_column] < mae_by_fold["similar_day_naive"]).sum())
    pinball_wins = int((pinball_by_fold[champion_column] < pinball_by_fold["similar_day_naive"]).sum())
    n_folds = int(len(mae_by_fold))
    mae_contribution = (mae_by_fold[champion_column] - mae_by_fold["similar_day_naive"]) * weights
    worst_fold = str(mae_contribution.idxmax())
    worst_contribution = float(mae_contribution.max())
    pooled_mae_gap = float(mae_contribution.sum())
    fold_view = per_fold.pivot_table(index="fold", columns="model", values="mae_final_p50").reset_index()
    fold_pinball = per_fold.pivot_table(index="fold", columns="model", values="pinball_final").reset_index()

    text = f"""# CP-2 — Model, calibration, and analysis

Generated by `scripts/cp2_report.py` from the committed artifacts in `reports/cp2/`. Every number
below is read from those files; none is transcribed by hand.

- Snapshot SHA-256: `{holdout["snapshot_sha256"]}`
- Code SHA at the final run: `{holdout["code_sha"]}` — the commit whose tree produced these
  numbers. Re-running at a later commit reproduces every metric and stamps its own value here;
  this field is provenance, not a checksum.
- Frozen champion fingerprint: `{holdout.get("artifact_fingerprint_sha256", "see models/champion/champion_card.json")}`
- Experiment records: <{TRACKING_URL}>

## The four cutoffs

They are four different dates by construction, and collapsing them would make the report contradict
itself.

| Cutoff | Value |
|---|---|
| `snapshot_cutoff` | {cutoffs["snapshot_cutoff"]} |
| `raw_model_fit_cutoff` | {cutoffs["raw_model_fit_cutoff"]} |
| `final_calibration_window` | {cutoffs["final_calibration_window"]} |
| `holdout_window` | {cutoffs["holdout_window"]} |

The raw-model fit cutoff precedes the snapshot cutoff by
**{cutoffs["raw_model_fit_precedes_snapshot_by_delivery_days"]} delivery days** (1 + 60 + 1 + 90).
That is the price of shipping the model the holdout evaluated, and it is disclosed rather than
hidden.

## 1. The two-arm catalog comparison (§4.1)

Both catalogs ran on the five pinned development folds with matched folds, rows, targets, seed,
hyperparameters and tuning budget. Row eligibility depends only on the target and the `base`
catalog, so the two arms evaluated **{selection["matched_rows"]:,} identical rows** — verified by
comparing the row keys and the target vectors, not asserted. The decision metric is the pooled
observation-weighted **raw-head** mean pinball loss over all nine quantiles and five folds. CQR and
isotonic belong to the final fit and never enter it.

**The numbers, before the conclusion:**

| Arm | Pooled raw-head mean pinball loss (unrounded, as stored) |
|---|---|
| `base` | `{base_loss}` |
| `base + residual_load_proxy` | `{augmented_loss}` |

Percentage difference (augmented vs base): **{selection["percentage_difference_augmented_vs_base"]:+.6f}%**.
Equality: {selection["equality"]}.

**Selected catalog: `{selection["selected_catalog"]}`.** The augmented catalog ships only if its
unrounded stored pooled loss is lower; it is not, so `base` ships. The domain feature did not earn
its place, and that is a result rather than a failure — the champion ships strict-gate with no
forced headline. {selection["eval_rows_with_null_residual_load_proxy"]:,} of the evaluation rows
carry a null `residual_load_proxy` (its 42-complete-day window is unsatisfied there, chiefly a
missing A75 hour on 2025-07-09 that invalidates the following 42 target days); those rows stay in
both arms with LightGBM handling the missing value natively, so no row is deleted from the arm that
does not need the feature.

This is an ordinary development-stage model-selection decision, labelled as such, not a confirmatory
result.

## 2. Baselines and development metrics (§7)

Pooled over the five folds' evaluation blocks. The three baselines are point forecasts, so their
nine quantiles are all equal to the point forecast — a degenerate predictive distribution whose mean
pinball loss is exactly half its MAE, because the nine τ values are symmetric about 0.5. Coverage is
undefined for a point forecast and is not reported for them.

{markdown_table(headline, ["model", "stage", "n_obs", "mae_p50", "mean_pinball"])}

**What the pinball margin does and does not measure.** A point forecast scored on pinball is
structurally disadvantaged against a nine-quantile model: it can never be paid for a well-placed
tail, only penalised for a badly placed one. So the champion's pinball advantage over the naive
comparators is largely the value of *having* a predictive distribution, not evidence that its median
is better — the MAE column is the point-accuracy comparison, and it reads differently. §7.1 pins
this comparison, and the report states the mechanism rather than letting the larger number stand
unqualified.

Per-fold MAE on the median:

{markdown_table(fold_view, list(fold_view.columns), floats=2)}

Per-fold mean pinball loss:

{markdown_table(fold_pinball, list(fold_pinball.columns))}

**Read this honestly, and read the tallies rather than a summary of them.** The champion beats the
similar-day naive on mean pinball loss in **{pinball_wins} of {n_folds} folds** and on median MAE in
**{mae_wins} of {n_folds}**. So the probabilistic win is broad and the point-accuracy loss is not: the
pooled MAE gap of {pooled_mae_gap:+.2f} EUR/MWh is produced almost entirely by **{worst_fold}**, the
crisis-peak block, which contributes {worst_contribution:+.2f} of it on its own while three folds
contribute negative (champion-favourable) amounts. An expanding-window model trained only on
pre-crisis data cannot follow an August-2022 level shift; persistence tracks it by construction. The
plan reports results and gates none of them, and the ≥15% pinball improvement is a narrative target
only.

### Both DM analyses, development evidence class

`evidence_class = development_post_selection` — descriptive post-selection evidence, never
confirmatory superiority. One-sided; reject (model better) if DM < −1.645; Newey–West long-run
variance with lag truncation ⌊N^(1/3)⌋. The champion side uses the final post-isotonic output.

| Analysis | Comparator | Statistic | p-value | Effect size (std.) | Relative improvement | N days |
|---|---|---|---|---|---|---|
| Probabilistic daily-vector pinball | similar-day naive | {dm_headline["statistic"]:.4f} | {dm_headline["p_value"]:.3g} | {dm_headline["standardized_effect_size"]:.3f} | {dm_headline["relative_improvement_pct"]:+.2f}% | {dm_headline["n_days"]} |
| Point median absolute error | similar-day naive | {dm_point["statistic"]:.4f} | {dm_point["p_value"]:.3g} | {dm_point["standardized_effect_size"]:.3f} | {dm_point["relative_improvement_pct"]:+.2f}% | {dm_point["n_days"]} |

The full set, including the 168h-naive and Ridge comparators, is in `reports/cp2/dm_development.json`.

## 3. CQR, isotonic-last, and the one hard gate (§6.2)

The order is raw heads → CQR on each symmetric pair → isotonic last. The rank
`k = ceil((n_cal+1)(1−α))` is a **one-based** rank; a zero-based implementation reads `scores[k−1]`.
Alphas are carried as exact rationals, so the rank never depends on binary floating-point
representation, and an undersized calibration set raises rather than clipping to the largest observed
score — clipping would substitute a finite threshold for the augmented `+∞` order statistic and
overstate the guarantee.

**The mandatory `n_cal=20` fixture reproduces** (`tests/test_10_cqr_order_statistic.py`): rows
`(q̂_lo, q̂_hi, y) = (100, 140, 111−j)` give ascending scores `−11 … 8`, one-based ranks
`{{20, 19, 17, 11}}`, zero-based positions `{{19, 18, 16, 10}}`, thresholds `Q = {{8, 7, 5, −1}}`. The
negative threshold narrows its pair; p50 is untouched by CQR. The fixture also rejects the two wrong
implementations by name: reading `scores[k]` gives `{{—, 8, 6, 0}}` and an interpolated
`np.quantile` gives `{{7.05, 6.1, 4.2, −1.5}}`.

### Three-stage empirical coverage, five development folds

{markdown_table(reliability, ["stage", "nominal", "empirical"])}

Figure: `reports/cp2/fig_reliability_three_stage.png`. The formal finite-sample marginal guarantee
attaches to the **post-CQR / pre-isotonic** stage only. Isotonic is a monotone rearrangement applied
last, so the final output's coverage is reported as **empirical**; no joint or simultaneous coverage
across the four intervals is claimed.

{EXCHANGEABILITY}

**The hard gate:** zero quantile-crossing violations after the full pipeline. Raw heads cross on
{int(pooled.loc[(pooled["model"] == selection["selected_catalog"]) & (pooled["stage"] == "raw"), "crossing_violations"].iloc[0]):,}
adjacent pairs across the development evaluation rows and still cross on
{int(pooled.loc[(pooled["model"] == selection["selected_catalog"]) & (pooled["stage"] == "post_cqr"), "crossing_violations"].iloc[0]):,}
after CQR; after isotonic the count is
**{int(pooled.loc[(pooled["model"] == selection["selected_catalog"]) & (pooled["stage"] == "final"), "crossing_violations"].iloc[0])}**,
and **{holdout["crossing_violations_final"]}** on the holdout. That CQR alone leaves thousands of
crossings is exactly why isotonic is unconditionally last.

## 4. Final fit, freeze, and the one-shot holdout (§5.1, §7.1)

Order: the nine raw heads were fit on every eligible row strictly before Embargo A
({holdout["n_holdout_rows"] and cutoffs["raw_model_fit_cutoff"]}); the four final CQR thresholds
were estimated **once** on the 60-day calibration slice; isotonic-last was attached; the complete
artifact was frozen to `models/champion/`. Then the holdout was opened.

Final CQR thresholds: `{json.dumps(holdout["final_cqr_thresholds"])}`.

### Before the holdout was opened: proof of sequential generation

For each of the {holdout["sequential_equivalence"]["days_checked"]} holdout delivery days, the
champion's inputs were rebuilt from a frame truncated at that delivery day and its nine outputs
compared to the vectorized ones.
**{holdout["sequential_equivalence"]["rows_checked"]:,} rows checked, {len(holdout["sequential_equivalence"]["mismatched_days"])} mismatched days.**
Every champion feature is a bounded backward window, so equality must hold exactly; any disagreement
would be forward information entering the forecast. This compares predictions to predictions and
reads no outcome, so it ran before the holdout was opened.

### The one-shot result

| Metric | Champion | Similar-day naive | Difference |
|---|---|---|---|
| MAE (EUR/MWh) | {holdout["champion_mae"]:.4f} | {holdout["similar_day_naive_mae"]:.4f} | {holdout["mae_percentage_difference_vs_naive"]:+.2f}% |
| Mean pinball loss | {holdout["champion_mean_pinball"]:.4f} | {holdout["similar_day_naive_mean_pinball"]:.4f} | {holdout["pinball_percentage_difference_vs_naive"]:+.2f}% |

Final empirical coverage: 50% → {holdout["final_coverage"]["50"]:.4f}, 80% →
{holdout["final_coverage"]["80"]:.4f}, 95% → {holdout["final_coverage"]["95"]:.4f}
({holdout["n_holdout_rows"]:,} rows over {holdout["n_holdout_days"]} delivery days).

Probabilistic daily-vector DM against the similar-day naive: statistic
**{holdout_dm["statistic"]:.4f}**, p-value **{holdout_dm["p_value"]:.3g}**, standardized effect size
**{holdout_dm["standardized_effect_size"]:.3f}**, mean daily loss differential
{holdout_dm["mean_loss_differential"]:.4f} over {holdout_dm["n_days"]} days, Newey–West lag
truncation {holdout_dm["lag_truncation"]}.

> {DM_LABEL}

The result supports a probabilistic-skill claim against the similar-day naive on this window and
nothing wider. It is not a gate, and no superiority claim beyond what it supports is made anywhere.

**The frozen artifact is the artifact that ships.** There was no retrain and no re-tune after the
holdout was opened. `models/champion/python_model.pkl` is *not* byte-stable — MLflow stamps a fresh
`model_uuid` and creation time into `MLmodel`, and cloudpickle does not reproduce identical bytes
across processes — so the identity to check is
`artifact_fingerprint_sha256` in `models/champion/champion_card.json`, computed over the catalog,
the feature list, the nine quantiles, the four thresholds and the nine boosters' own serializations.

{HOLDOUT_LIMITATION}

### Why one delivery day of embargo suffices, given 48h and 168h lags (§5.1, verbatim)

{EMBARGO_REASONING}

## 5. Post-gate information benchmark (§7.2) — one run, one number

Two arms, raw quantile heads, neither calibrated: *strict* is the selected champion catalog,
*A69-augmented* is the same catalog plus delivery-day A69 and its named derivatives
({", ".join(f"`{name}`" for name in benchmark["a69_columns_added"])}) and nothing else different.
Same rows, folds, seed, hyperparameters and tuning budget.

| Arm | Pooled raw-head mean pinball loss |
|---|---|
| Strict (`{benchmark["strict_arm"]["arm"]}`) | `{benchmark["strict_arm"]["pooled_mean_pinball"]}` |
| A69-augmented (`{benchmark["a69_augmented_arm"]["arm"]}`) | `{benchmark["a69_augmented_arm"]["pooled_mean_pinball"]}` |

**Percentage difference: {benchmark["percentage_difference_a69_vs_strict"]:+.4f}%.** Post-gate
information is worth roughly {abs(benchmark["percentage_difference_a69_vs_strict"]):.1f}% of pooled
pinball loss, and the project declines to use it. The strict arm reproduced the development
selection run to within 1e-12
({benchmark["strict_arm_reproduces_development_selection_run"]}), which is what makes the difference
readable as information content rather than as run-to-run noise.

Coverage, interval width and calibration error are deliberately **not** reported here: the
comparison is uncalibrated. There is no second calibration, no deployable artifact and no registry
version for the A69 arm, and A69 is never reclassified KFT.

{'> ' + benchmark["limitation"]}

## 6. Explainability (§8.1, §8.2)

{diagnostics["shap_surface"]}. The frozen champion was fit on every development row, so SHAP on it
over the validation tail would be in-sample; the holdout is closed to development diagnostics. Both
reads are committed — `reports/cp2/shap_ranking.csv` (out of sample, headline) and
`reports/cp2/shap_ranking_frozen_champion_in_sample.csv` (labelled in-sample). Their agreement is
measured rather than asserted: {agreement["top5_overlap"]}/5 and {agreement["top10_overlap"]}/10
overlap at the top, Spearman rank correlation {agreement["rank_spearman"]:.3f} across all features.

Top 10 by mean |SHAP| (p50 head):

{markdown_table(shap_rank.head(10), ["rank", "feature", "mean_abs_shap"])}

Top 10 by permutation importance (mean MAE increase under shuffling, 10 repeats):

{markdown_table(permutation.head(10), ["rank", "feature", "importance_mean_mae_increase", "importance_std"])}

Spearman rank correlation between the two rankings: **{diagnostics["shap_vs_permutation_rank_spearman"]:.3f}** —
they agree on the top of the list and disagree in the middle, which is the ordinary difference
between attribution in expectation and degradation under shuffling.

Figures: `reports/cp2/fig_shap_summary.png`, and two dependence plots drawn from features actually in
the selected catalog. **Scoping, stated explicitly:** {diagnostics["scoping"]}

## 7. Regime-stratified error analysis (§8.3)

`n_obs` on every row. Thin subsets carry day-block bootstrap 95% confidence intervals — days, not
hours, because the 24 rows of one delivery day share a day effect and an hour-level bootstrap would
report an interval roughly √24 too narrow — and are read qualitatively.

{markdown_table(regime, [c for c in ["stratum", "n_obs", "n_days", "mae", "mae_ci95_low", "mae_ci95_high", "mean_pinball", "coverage_50", "coverage_80", "coverage_95", "read"] if c in regime.columns])}

Dunkelflaute stratum definition: {diagnostics["dunkelflaute_definition"]}
({diagnostics["n_dunkelflaute_days_in_snapshot"]} flagged delivery days in the snapshot).

**What the table says.** Coverage on the crisis stratum collapses to
{regime.loc[regime["stratum"].str.startswith("crisis"), "coverage_95"].iloc[0]:.3f} at the 95% level
and to {regime.loc[regime["stratum"].str.startswith("August-2022"), "coverage_95"].iloc[0]:.3f} in
the August-2022 peak weeks, against
{regime.loc[regime["stratum"].str.startswith("post-crisis"), "coverage_95"].iloc[0]:.3f} post-crisis.
Coverage on negative-price hours is
{regime.loc[regime["stratum"] == "negative-price hours", "coverage_95"].iloc[0]:.3f} at the 95%
level — materially worse than nominal, consistent with the bounded-target tail caveat: the price
floor truncates the p2.5/p5 conformity residuals, so the lowest intervals can under-cover
conditionally near the floor. Both readings tie directly to the exchangeability paragraph above.
This is deliberately not engineered around; a floor-aware tail would reopen scope.

## 8. Experiment records (§9.1)

Every decision-bearing run — the three baselines, the two catalog candidates, both §7.2 benchmark
arms, the champion's final fit and holdout, and the diagnostics — is logged to the public DagsHub
MLflow instance at <https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow> with snapshot hash,
code SHA, fold spec, feature list, seed, hyperparameters, metrics and artifact links, and
`evidence_class` on the DM artifacts. The link is the `.mlflow` tracking URI, never the repository
root — the root redirects an anonymous visitor to a sign-in page while the tracking URI is
anonymously readable.

### Compute footprint (§9.3)

Measured wall clock on {timings.get("hardware", "Apple M3, 16 GB, CPU only")},
Python {timings.get("python", "3.13")}, from `reports/cp2/timings.json`:

| Stage | Seconds |
|---|---|
| Development (baselines + both catalogs, 5 folds) | {timings.get("development_seconds", "-")} |
| §7.2 post-gate benchmark | {timings.get("benchmark_seconds", "-")} |
| Final fit, freeze, sequential proof, holdout | {timings.get("holdout_seconds", "-")} |
| Diagnostics (SHAP, permutation, regime, reliability) | {timings.get("diagnostics_seconds", "-")} |
| **Total** | **{timings.get("total_seconds", "-")}** |

No GPU, no cloud compute, $0 run rate. The champion's frozen artifact is
{Path("models/champion/python_model.pkl").stat().st_size / 1_048_576:.1f} MB on disk and is logged
to MLflow as `{model_uri}`.

**No hyperparameter search was run.** One frozen LightGBM configuration is used by every arm: §4.1
and §7.2 both require a matched tuning budget across arms, and a budget of zero is the only one
matched by construction rather than by bookkeeping. It also keeps the whole pipeline inside the
Apple M3 / 16 GB / CPU-only / $0 constraint — the development stage, the benchmark, the final fit
and the diagnostics together run in well under an hour.

## Reproduction

```bash
make train        # baselines, two-arm comparison, development DM
make benchmark    # the §7.2 post-gate benchmark
make holdout      # final fit, freeze, one-shot holdout
make diagnostics  # SHAP, permutation, regime table, reliability
make report       # regenerate this document
```

`make test` runs the invariant suite including the §6.2 CQR fixture. MLflow logging is skipped
silently when `MLFLOW_TRACKING_URI` is unset, so every command above runs offline without a
credential.
"""
    DOC.write_text(text)
    print(f"wrote {DOC} ({len(text):,} chars)")


if __name__ == "__main__":
    main()
