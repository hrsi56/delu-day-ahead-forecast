"""The marimo showcase (§9.2), run in server mode -- `marimo run app/showcase.py`.

Not WASM. The champion and the snapshot are read from the image at startup; the
app makes no live API call during a user session, holds no registry dependency
and has no load-time gate.

Two controls only (§9.2): the fixed quantile-level selector, and one
load-forecast scenario perturbation served by direct local inference. No
multidimensional precomputed grid, no dynamic SHAP, no per-cell OOD system.

Every published number comes from `delu_forecast.claims`, the same dict the
README, the static Pages export and the Space card render from.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", app_title="DE-LU Day-Ahead Price Forecasting")


@app.cell
def _():
    import sys
    from datetime import date
    from pathlib import Path

    import marimo as mo

    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT / "src") not in sys.path:
        sys.path.insert(0, str(ROOT / "src"))

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    from delu_forecast.claims import build_claims
    from delu_forecast.showcase import (
        INTERVAL_LEVELS,
        actuals_for_day,
        default_target_day,
        forecast_delivery_day,
        holdout_replay,
        load_champion,
        load_snapshot,
        quantile_fan,
    )

    C = build_claims()
    return (
        C,
        INTERVAL_LEVELS,
        ROOT,
        actuals_for_day,
        date,
        default_target_day,
        forecast_delivery_day,
        holdout_replay,
        load_champion,
        load_snapshot,
        mo,
        np,
        pd,
        plt,
        quantile_fan,
    )


@app.cell
def _(C, mo):
    mo.md(
        f"""
        # DE-LU day-ahead price forecasting — interactive deep dive

        A probabilistic forecast of the next delivery day's hourly German–Luxembourg
        day-ahead price, with calibrated 50 / 80 / 95 % intervals. **Strict-gate by
        construction:** the shipped model uses no input published after the 12:00 CET
        day-ahead auction gate.

        This Space is the interactive companion to the
        [static report]({C['pages_url']}), which is the primary entry point. The
        decision trail is public at [MLflow on DagsHub]({C['mlflow_url']}).

        > **{C['replay_label']}**

        **The four cutoffs, stated separately because they are four different dates:**

        | Cutoff | Value |
        |---|---|
        | `snapshot_cutoff` | {C['snapshot_cutoff']} |
        | `raw_model_fit_cutoff` | {C['raw_model_fit_cutoff']} |
        | `final_calibration_window` | {C['final_calibration_window']} |
        | `holdout_window` | {C['holdout_window']} |

        {C['shipped_is_evaluated']} Its raw-model fit cutoff precedes the snapshot
        cutoff by {C['staleness_days']} delivery days, which is what shipping the
        evaluated model costs.

        *This demo runs a frozen model on a frozen snapshot. It is not a live service,
        it is never refreshed on a schedule, and it makes no external call while you
        use it.*
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## 1. The data

        One committed Parquet snapshot: 67,343 continuous UTC-indexed hourly rows,
        delivery 2019-01-01 through 2026-09-06, carrying the day-ahead price (A44),
        the day-ahead load forecast (A65/A01), the benchmark-only day-ahead VRE
        forecast (A69) and aggregate actual generation (A75). Quarter-hourly feeds
        are aggregated to hours from exactly four complete bins; the 2025-10-01
        switch to a 15-minute price product is handled as a mean of four
        quarter-hour prices, with no partial bin anywhere in the archive.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## 2. Three regimes in one series

        Annual mean price swept from about €30/MWh in 2020 to about €235/MWh in
        2022 and back to about €89/MWh in 2025 — a crisis and a normalization
        inside one training set. Underneath it, the solar build-out pushed
        negative-price hours from 139 (2021) → 69 (2022) → 301 (2023) → 457 (2024)
        → 576 (2025).

        *The 2025 count is measured on this snapshot's hourly series. After
        2025-10-01 an hour is the mean of four quarter-hour prices, so the tally
        depends on that averaging choice; a quarter-hour tally differs. The price
        is routinely negative and has touched the −500 €/MWh floor, which is why no
        log or Box-Cox transform is applied to the target.*

        Two consequences the whole design follows from: evaluation is stratified
        across all three regimes rather than collapsed into a recent tail, and
        exchangeability — the assumption CQR's coverage guarantee rests on — is
        mildly violated by construction.
        """
    )
    return


@app.cell
def _(C, mo):
    mo.md(
        f"""
        ## 3. Feature catalog — frozen before fitting

        Two catalogs were frozen before any model ran: `base` (calendar and regime
        features, the A65 load forecast, calendar-day-matched price lags at D−1/D−2/D−7,
        and D-1-frozen rolling price statistics), and `base + residual_load_proxy`,
        which adds exactly one domain feature — a residual-load proxy built from a
        42-complete-delivery-day trailing mean of actual wind and solar generation
        ending at D−2.

        **Selected catalog: `{C['selected_catalog']}`.** Pooled observation-weighted
        raw-head mean pinball loss over the five pinned folds, unrounded as stored:

        | Arm | Pooled raw-head mean pinball loss |
        |---|---|
        | `base` | `{C['catalog_base_loss']}` |
        | `base + residual_load_proxy` | `{C['catalog_augmented_loss']}` |

        Percentage difference (augmented vs base): **{C['catalog_pct']}**. The rule was
        fixed before fitting — the augmented catalog ships only if its unrounded stored
        pooled loss is lower. It is not, so the domain feature did not earn its place.
        That is a reportable result, not a failure.
        """
    )
    return


@app.cell
def _(ROOT, mo):
    mo.md(
        f"""
        ## 3b. Why these seasonal features? (spectral view)

        {mo.hstack([
            mo.image(str(ROOT / "reports/fig_welch_periodogram.png"), width=330),
            mo.image(str(ROOT / "reports/fig_per_regime_periodogram.png"), width=330),
            mo.image(str(ROOT / "reports/fig_acf_24_168.png"), width=330),
        ])}

        The Welch periodogram shows pronounced price energy at the 24-hour and
        168-hour cycles with a visible 12-hour harmonic, which is what justifies the
        catalog's hour-of-day and day-of-week structure rather than an assumption that
        electricity "should" be daily-seasonal. The per-regime overlay shows an
        elevated broadband floor and altered seasonal amplitude during the crisis: the
        spectrum itself is not stationary across regimes, which supports reporting
        performance across all three rather than collapsing them into one recent-tail
        summary. The ACF cross-check confirms the same daily and weekly recurrence in
        the time domain, so the conclusion does not rest on one estimator. These are
        price diagnostics only — they neither validate nor justify retaining
        `residual_load_proxy`, which the frozen two-arm comparison alone decides.
        """
    )
    return


@app.cell
def _(C, mo):
    mo.md(
        f"""
        ## 4. Validation design

        Expanding-window walk-forward CV, five development folds, each with a
        **one-complete-delivery-day embargo** (23, 24 or 25 rows as DST requires) and a
        90-day evaluation block, anchored so the blocks span pre-crisis, the crisis peak
        and the post-crisis negative-price era. Five tail partitions were pinned before
        any EDA: fold 5, Embargo A, a 60-day final-calibration slice, Embargo B, and the
        final 90-day holdout.

        **The target is D+1, anchored at the 12:00 CET gate.** Every feature must be
        available at that origin, which is stricter than it sounds: the model emits the
        whole next-day curve at once, so a row-wise `t−1` boundary would admit the
        target curve into its own features. The binding rule is per delivery day —
        for a forecast of day `D`, every price-derived feature may consume only prices
        whose delivery date is earlier than `D`, and rolling statistics are frozen at
        the D−1 boundary for the whole curve.

        **Strict gate.** The day-ahead wind/solar forecast (A69) is not published until
        after the 12:00 gate, so it is excluded from the shipped model entirely rather
        than used as-archived and disclosed. What that exclusion costs is measured in
        section 5.

        **Two disclosed assumptions, stated as assumptions:**

        - {C['assumption_a65']}
        - {C['assumption_a75']}
        """
    )
    return


@app.cell
def _(C, mo):
    mo.md(
        f"""
        ## 5. Results

        ### Development folds — descriptive post-selection evidence

        `evidence_class = {C['development_evidence_class']}`. These folds were also used
        for catalog selection and model development, so their p-values are descriptive,
        never confirmatory, and no result gates anything.

        | Analysis | Comparator | Statistic | p-value | N days |
        |---|---|---|---|---|
        | Probabilistic daily-vector pinball | similar-day naive | {C['development_dm_pinball_statistic']} | {C['development_dm_pinball_p_value']} | {C['development_days']} |
        | Point median absolute error | similar-day naive | {C['development_dm_point_statistic']} | {C['development_dm_point_p_value']} | {C['development_days']} |

        **The point-accuracy test shows no evidence of advantage** (p =
        {C['development_dm_point_p_value']}). Reported, not omitted and not reframed:
        the probabilistic win is broad and the point-accuracy win is not, and the pooled
        MAE gap comes almost entirely from the crisis-peak fold, where an
        expanding-window model trained only on pre-crisis data cannot follow an
        August-2022 level shift and persistence can.

        ### The one-shot holdout — opened exactly once

        | Metric | Champion | Similar-day naive | Difference |
        |---|---|---|---|
        | MAE (EUR/MWh) | {C['holdout_mae_champion']} | {C['holdout_mae_naive']} | {C['holdout_mae_pct']} |
        | Mean pinball loss | {C['holdout_pinball_champion']} | {C['holdout_pinball_naive']} | {C['holdout_pinball_pct']} |

        Final empirical coverage over {C['holdout_rows']} rows on {C['holdout_days']}
        delivery days: **{C['holdout_coverage_50']}** / **{C['holdout_coverage_80']}** /
        **{C['holdout_coverage_95']}** at the 50 / 80 / 95 % nominal levels.
        Probabilistic daily-vector DM against the similar-day naive: statistic
        **{C['holdout_dm_statistic']}**, p-value **{C['holdout_dm_p_value']}**,
        standardized effect size **{C['holdout_dm_effect_size']}**.

        > {C['holdout_dm_label']}

        ### What the post-gate forecast would have been worth

        A controlled ablation on raw heads, neither arm calibrated: adding the
        delivery-day A69 forecast and its named derivatives moves pooled mean pinball
        loss from `{C['benchmark_strict_loss']}` to `{C['benchmark_a69_loss']}` —
        **{C['benchmark_pct']}**.

        > {C['benchmark_limitation']}
        """
    )
    return


@app.cell
def _(ROOT, mo):
    mo.md(
        f"""
        ## 6–7. Explainability

        SHAP on the p50 head (out of sample, fold-5 model on fold 5's evaluation block)
        and permutation importance on the same surface. SHAP explains central tendency,
        not interval width — width is driven by the inter-quantile spread and the CQR
        shift. Neither is the incremental-value test; that is the frozen two-arm
        comparison in section 3.

        {mo.hstack([
            mo.image(str(ROOT / "reports/cp2/fig_shap_summary.png"), width=430),
            mo.vstack([
                mo.image(str(ROOT / "reports/cp2/fig_shap_dependence_price_lag_24h.png"), width=330),
                mo.image(str(ROOT / "reports/cp2/fig_shap_dependence_price_lag_168h.png"), width=330),
            ]),
        ])}
        """
    )
    return


@app.cell
def _(ROOT, mo, pd):
    _shap = pd.read_csv(ROOT / "reports/cp2/shap_ranking.csv").head(10)
    _perm = pd.read_csv(ROOT / "reports/cp2/permutation_importance.csv").head(10)
    mo.hstack(
        [
            mo.vstack([mo.md("**Top 10 by mean |SHAP| (p50 head)**"), mo.ui.table(_shap, selection=None)]),
            mo.vstack([mo.md("**Top 10 by permutation importance**"), mo.ui.table(_perm, selection=None)]),
        ]
    )
    return


@app.cell
def _(ROOT, mo, pd):
    mo.vstack(
        [
            mo.md(
                """
                ## 8. Regime-stratified error

                `n_obs` on every row; thin subsets carry day-block bootstrap 95 %
                confidence intervals and are read qualitatively. Coverage collapses on
                the crisis stratum and on negative-price hours — the bounded target
                truncates the lower conformity residuals near the floor. This is
                disclosed, not engineered around.
                """
            ),
            mo.ui.table(pd.read_csv(ROOT / "reports/cp2/regime_table.csv"), selection=None),
        ]
    )
    return


@app.cell
def _(C, ROOT, mo):
    mo.md(
        f"""
        ## 9. Reliability — three stages

        {mo.image(str(ROOT / "reports/cp2/fig_reliability_three_stage.png"), width=620)}

        Raw LightGBM heads → CQR on each symmetric pair → isotonic last. The formal
        finite-sample marginal guarantee attaches to the **post-CQR / pre-isotonic**
        stage only; the final output's coverage is reported as **empirical**, and no
        joint coverage across the four intervals is claimed.

        The one retained hard gate is a correctness property, not a favourable number:
        zero quantile-crossing violations after the full pipeline. On the selected
        `{C['selected_catalog']}` catalog's development evaluation rows the raw heads
        cross on {C['crossings_development_raw']} adjacent pairs and still cross on
        {C['crossings_development_post_cqr']} after CQR; after isotonic the count is
        {C['crossings_development_final']}, and {C['crossings_holdout_final']} on the
        holdout. That CQR alone leaves thousands of crossings is exactly why isotonic
        is unconditionally last.

        > {C['exchangeability']}
        """
    )
    return


@app.cell
def _(C, mo):
    mo.md(
        f"""
        ## 10. Next-day forecast — the two controls

        The quantile-level selector annotates the interval with the frozen champion's
        own empirical coverage at that level over the 90-day holdout. The load-forecast
        control re-runs local inference on the delivery day's A65 vector, scaled.

        > **{C['sensitivity_probe_label']}** They hold every other input fixed, including
        the price history the lags and rolling statistics are built from, so a large
        perturbation asks the model a question it was never trained on.
        """
    )
    return


@app.cell
def _(INTERVAL_LEVELS, mo):
    level = mo.ui.radio(
        options={f"{value} %": value for value in sorted(INTERVAL_LEVELS)},
        value="80 %",
        label="Prediction-interval level",
        inline=True,
    )
    load_scale = mo.ui.slider(
        start=0.90, stop=1.10, step=0.01, value=1.00,
        label="Load-forecast scenario (× the delivery day's A65 vector)",
        show_value=True,
    )
    mo.hstack([level, load_scale], justify="start", gap=2)
    return level, load_scale


@app.cell
def _(default_target_day, load_champion, load_snapshot):
    champion = load_champion()
    snapshot = load_snapshot()
    target_day = default_target_day(snapshot)
    return champion, snapshot, target_day


@app.cell
def _(
    C,
    actuals_for_day,
    champion,
    forecast_delivery_day,
    level,
    load_scale,
    mo,
    np,
    plt,
    quantile_fan,
    snapshot,
    target_day,
):
    _forecast = forecast_delivery_day(champion, snapshot, target_day, load_scale=load_scale.value)
    _fan = quantile_fan(_forecast, level.value)
    _actual = actuals_for_day(snapshot, target_day)

    _fig, _ax = plt.subplots(figsize=(10, 4.2))
    _hours = _fan["local_hour"].to_numpy()
    _ax.fill_between(_hours, _fan["lower"], _fan["upper"], alpha=0.25,
                     label=f"{level.value}% interval", color="#3a6ea5")
    _ax.plot(_hours, _fan["median"], color="#1b3a5c", lw=2, label="median forecast")
    if load_scale.value == 1.0:
        _ax.plot(_actual.index.to_numpy(), _actual.to_numpy(), color="#b03a2e", lw=1.4,
                 ls="--", label="cleared price (outcome)")
    _ax.axhline(0.0, color="#888", lw=0.8)
    _ax.set_xlabel("local hour (Europe/Berlin)")
    _ax.set_ylabel("EUR/MWh")
    _ax.set_title(f"Delivery day {target_day} — historical out-of-sample replay")
    _ax.legend(loc="upper left", fontsize=8)
    _ax.set_xticks(np.arange(0, len(_hours), 2))
    _fig.tight_layout()

    _note = (
        f"**{C['replay_label']}** Nominal {level.value} %; the frozen champion's "
        f"empirical coverage at this level over the {C['holdout_days']}-day holdout was "
        f"**{C['holdout_coverage_' + str(level.value)]}**."
    )
    if load_scale.value != 1.0:
        _note += (
            f" Scenario active: load forecast × {load_scale.value:.2f}. "
            f"{C['sensitivity_probe_label']} The cleared-price line is hidden while a "
            "scenario is active, because the outcome belongs to the unperturbed day."
        )
    mo.vstack([mo.as_html(_fig), mo.md(_note)])
    return


@app.cell
def _(C, mo):
    mo.md(
        f"""
        ## 11. Honest limitations

        - **Exchangeability under regime shift.** {C['exchangeability']}
        - **Development vs one-shot evidence.** The five-fold results are
          `{C['development_evidence_class']}` — descriptive, post-selection. Only the
          90-day holdout was pre-specified and opened once.
        - **{C['holdout_dm_label']}**
        - **Two disclosed assumptions.** {C['assumption_a65']} {C['assumption_a75']}
        - **The strict-gate design has a measured cost:** {C['benchmark_pct']} of pooled
          raw-head pinball loss. {C['benchmark_limitation']}
        - **A two-sided bounded target.** The price is routinely negative and has hit
          the −500 €/MWh floor, which truncates the lower conformity residuals; coverage
          on negative-price hours is materially worse than nominal.
          {C['floor_change']}
        - **Coverage divergence.** Final empirical coverage is
          {C['holdout_coverage_50']} / {C['holdout_coverage_80']} /
          {C['holdout_coverage_95']} against 50 / 80 / 95 % nominal. The 50 % interval
          under-covers by roughly six points on this window.
        - **Model staleness.** {C['shipped_is_evaluated']} The raw-model fit cutoff
          ({C['raw_model_fit_cutoff']}) precedes the snapshot cutoff
          ({C['snapshot_cutoff']}) by {C['staleness_days']} delivery days, and the
          deployed demo applies a frozen model. All four cutoffs are published
          separately: snapshot {C['snapshot_cutoff']}, raw-model fit
          {C['raw_model_fit_cutoff']}, final calibration
          {C['final_calibration_window']}, holdout {C['holdout_window']}.
        - **The 15-minute MTU averaging choice.** From 2025-10-01 an hourly price is the
          mean of four quarter-hour prices. Any hour-level statistic — including the
          negative-hour tally above — depends on that choice.
        - **This is a portfolio artifact, not an operations system.** No retraining
          schedule, no drift gate, no rollback machinery, no monitoring surface.

        > {C['holdout_limitation']}
        """
    )
    return


@app.cell
def _(C, mo):
    mo.md(
        f"""
        ## 12. Reproducibility

        - **Champion identity.** `artifact_fingerprint_sha256`
          `{C['champion_fingerprint']}` — the catalog, the feature list, the nine
          quantiles, the four CQR thresholds and the nine boosters' own serializations.
          The pickle's bytes are not stable, because MLflow stamps a fresh UUID and
          creation time on every save. `python_model.pkl` is
          {C['champion_pkl_bytes']} bytes = {C['champion_pkl_size']}; the whole
          `models/champion/` directory is {C['champion_dir_bytes']} bytes =
          {C['champion_dir_size']}.
        - **Snapshot.** `sha256` `{C['snapshot_sha256']}`, pinned and committed.
        - **Experiment records.** [{C['mlflow_url']}]({C['mlflow_url']}) — the `.mlflow`
          tracking URI, which is anonymously readable. The DagsHub repository UI is not
          linked, because it redirects an anonymous visitor to a sign-in page.
        - **Code.** [{C['github_url']}]({C['github_url']}); `make train` after checking
          out the tagged commit reproduces the champion from the committed snapshot, and
          `uv run python predict_next_day.py` runs it offline.
        - **SQL.** Four hand-authored DuckDB queries in `sql/feature_queries.sql` express
          the same calendar-day lag and D-1-frozen rolling semantics as the canonical
          Python pipeline.
        - **Compute.** Apple M3, 16 GB, CPU only, no GPU, $0 run rate.

        {C['attribution']}
        """
    )
    return


if __name__ == "__main__":
    app.run()
