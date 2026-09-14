# DE-LU Day-Ahead Price Forecasting

**What it is (30-second read).** A portfolio-grade probabilistic tool that forecasts the next delivery day's hourly German–Luxembourg (DE-LU) day-ahead electricity price, with calibrated 50 / 80 / 95 % prediction intervals.

- **Problem** — forecast the next delivery day's hourly DE-LU prices at the 12:00 CET day-ahead gate — normally 24 values, 23/25 on DST-transition days — across a three-regime market (the 2021–23 energy crisis, the negative-price/solar era, and Dunkelflaute scarcity).
- **Approach** — a single LightGBM nine-quantile ensemble, CQR-calibrated with isotonic monotonicity last; walk-forward CV with a one-delivery-day embargo and pinned three-regime folds; **strict-gate features only** — the shipped model uses no input published after the gate (the day-ahead wind/solar forecast is measured in a separate post-gate benchmark, never shipped).
- **Feature catalog** — frozen before fitting. Calendar and regime features, the day-ahead load forecast, calendar-day-matched price lags and D-1-frozen rolling statistics, plus one candidate domain feature: a residual-load proxy built from a 42-day trailing mean of actual wind and solar generation ending at D-2. Two catalogs, one comparison, and the shipped one is named in the report — including when the domain feature does not earn its place.
- **Results** — LightGBM vs. similar-day-naïve / 168h-naïve / Ridge, with five-fold DM labeled **development / post-selection**, plus **one pre-specified evaluation on a 90-day holdout** the model never saw — reported once, whatever it says, and labeled *confirmatory-style, not power-qualified*. Three-stage reliability, SHAP, permutation importance, and regime-stratified errors. A separate one-number benchmark measures what the post-gate wind/solar forecast would have been worth. *(Live from CP-3.)*
- **Honest limitations** — regime-shift exchangeability; two disclosed assumptions (the load forecast's pre-gate availability, and revision in the actual-generation archive); the live negative-price floor; and model staleness, with **four cutoffs published separately** — snapshot, raw-model fit, final calibration, and holdout. The shipped model is exactly the model the holdout evaluated: there is no retrain after the result is opened.
- **Demo & reproduction** — the **primary link is the static GitHub Pages report** (CDN-served, no container, no cold start); the interactive marimo Space is one labeled click deeper, and what it renders over the holdout period is a **historical out-of-sample replay**, not a live forecast; `make train` after checking out the tagged commit reproduces the champion from the committed snapshot. The release is **frozen** — there is no scheduled refresh. *(Live from CP-3.)*

**Project shape:** three checkpoints — data and features (CP-1), model and analysis (CP-2), showcase and release (CP-3).

Full engineering plan: **`capstone_V6_8.md`** (v6.8). Data: ENTSO-E Transparency Platform; Bundesnetzagentur | SMARD.de — CC BY 4.0.

## CP-1 data and fixed features

The frozen snapshot contains 67,343 continuous hourly price rows from delivery
2019-01-01 through 2026-09-06. It was pulled from SMARD as the plan-authorized
fallback-primary route while the ENTSO-E External API was unavailable. The
mapping, cutoff, missing-source accounting, CC BY 4.0 attribution, and immutable
SHA-256 are recorded in [`data/README.md`](data/README.md) and
[`data/source_manifest.json`](data/source_manifest.json). When the ENTSO-E API
returned later in the checkpoint, the independently pre-pinned five-day sample
reconciled 120/120 hourly prices within €0.01/MWh (maximum difference €0.00),
including both sides of the 2025-10-01 transition.

The Python layer in `src/delu_forecast/` implements exactly two frozen model
catalogs: `base`, and `base_plus_residual_load_proxy`, whose only added model
feature is the 42-complete-delivery-day, D-2-bounded proxy. The five tail
partitions were pinned in [`data/partitions.json`](data/partitions.json) before
spectral EDA. The complete KFT/LAG classification and the A65/A75 assumptions
are in [`docs/data-leakage-audit.md`](docs/data-leakage-audit.md).

For delivery day D, price lags match the same Berlin clock hour of D-1, D-2,
and D-7; missing or ambiguous source hours yield null. Rolling price statistics
use exactly the final 168 or 720 canonical hourly observations ending at the
close of D-1, with one result broadcast to every row of D. No price feature
consumes a D price. The A65 daily mean requires all 23/24/25 expected hours and
is null for an incomplete day. The runnable [DuckDB queries](sql/feature_queries.sql)
express the same boundaries; Python remains the canonical feature pipeline.
The [v6.8 acceptance audit](reports/cp1-v68-availability.md) records the repair,
whole-snapshot numerical checks, and tests against deliberately faulty variants.

A65 is KFT by **assumption**: both the existence of the delivery-day vector
before the gate and its equality to the archived vector used here are assumed.
The regulatory update provision permits later revisions; archive reachability
does not establish the 12:00 vintage. A75 also uses current archived actuals,
which may differ from the values visible in real time despite the D-2 boundary.

### Why these seasonal features? (spectral view)

The [Welch periodogram](reports/fig_welch_periodogram.png) confirms pronounced
price energy at the 24-hour and 168-hour cycles, with the 12-hour harmonic,
which justifies the catalog's hour-of-day and day-of-week structure. The
[per-regime spectrum](reports/fig_per_regime_periodogram.png) shows an elevated
broadband floor and altered seasonal amplitude during the crisis, supporting
regime-stratified evaluation rather than one recent-tail summary. The
[ACF cross-check](reports/fig_acf_24_168.png) independently shows strong daily
and weekly recurrence in the time domain. These are price diagnostics: they do
not validate or justify retaining `residual_load_proxy`, which the frozen CP-2
two-arm comparison alone decides.

## CP-2 model, calibration and analysis

**The two-arm comparison, numbers first.** The two frozen catalogs were compared once on raw heads
over the five pinned folds with matched rows, seed, hyperparameters and (zero) tuning budget. Pooled
observation-weighted mean pinball loss, unrounded as stored:

| Arm | Pooled raw-head mean pinball loss |
|---|---|
| `base` | `13.015841509664993` |
| `base + residual_load_proxy` | `13.064197422052183` |

Percentage difference (augmented vs base): **+0.3715%**.

**Selected catalog: `base`.** The augmented catalog ships only if its unrounded stored pooled
loss is lower; it is not, so the champion ships strict-gate as `base`. The domain feature did not
earn its place on the pooled metric that decides, and that is a reportable result, not a failure.
The fold-level picture is not uniform — the augmented arm is lower on
2 of the 5 folds, and the report gives that table —
but §4.1 fixes the rule as pooled and fixes it before fitting, so the split is disclosed and the
decision is not revisited.

**Development metrics are descriptive post-selection evidence** (`evidence_class =
development_post_selection`), never confirmatory superiority. The champion beats the similar-day
naive on mean pinball loss in 5 of the 5 evaluation
blocks and on median MAE in 3 of 5: the probabilistic win is
broad, the point-accuracy loss is not. The pooled MAE gap of +9.29 EUR/MWh
comes almost entirely from **fold_3**, the crisis-peak block, which contributes
+10.87 of it alone — an expanding-window model trained only on
pre-crisis data cannot follow an August-2022 level shift, and persistence can. Full tables, both DM
analyses, the three-stage reliability read, SHAP, permutation importance and the regime-stratified
table are in [`docs/cp2-model-report.md`](docs/cp2-model-report.md) and `reports/cp2/`.

**One pre-specified holdout evaluation, opened once.** Champion MAE 25.91 vs
similar-day naive 27.76 EUR/MWh
(-6.7%); champion mean pinball loss
6.708 vs 13.879
(-51.7%); final empirical coverage
0.441 / 0.759 /
0.940 at the 50 / 80 / 95 % nominal levels; probabilistic
daily-vector DM statistic -8.68, p = 2e-18,
standardized effect size -1.05, over
90 delivery days.

> Pre-specified one-shot holdout DM test on a fixed 90-day window — confirmatory-style, not power-qualified.

**The shipped model is exactly the model the holdout evaluated.** There is no retrain and no re-tune
after the result was opened. The frozen artifact is `models/champion/`, a single `mlflow.pyfunc`
wrapping the nine quantile heads, the selected catalog's feature pipeline, the four CQR thresholds
and the isotonic ordering guard. Its identity is the `artifact_fingerprint_sha256` recorded in
`models/champion/champion_card.json`; the pickle's own bytes are not stable, because MLflow stamps a
fresh UUID and creation time on every save.

**Four cutoffs, stated separately because they are four different dates:**

| Cutoff | Value |
|---|---|
| `snapshot_cutoff` | 2026-09-06 |
| `raw_model_fit_cutoff` | 2026-04-07 |
| `final_calibration_window` | 2026-04-09..2026-06-07 |
| `holdout_window` | 2026-06-09..2026-09-06 |

The raw-model fit cutoff precedes the snapshot cutoff by
152 delivery days (1 + 60 + 1 + 90). That
is what shipping the evaluated model costs, and it is stated plainly rather than apologised for.

**What the post-gate forecast would have been worth.** A controlled ablation, raw heads, neither arm
calibrated: adding the delivery-day A69 forecast and its derivatives lowers pooled mean pinball loss
by 19.49%
(`13.015841509664993` → `10.478714632475889`).

> This uncalibrated raw-head comparison isolates the information content of post-gate A69. It makes no claim about calibrated interval quality and does not make A69 available at the forecast gate.

**Experiment records** for every decision-bearing run — the three baselines, both catalog
candidates, both benchmark arms, the champion's final fit and holdout — are public at
<https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow> with snapshot hash, code SHA, fold spec, feature list, seed, hyperparameters,
metrics and artifact links.

Reproduce with `make cp2` after `uv sync`; every stage runs offline and MLflow logging is skipped
silently when `MLFLOW_TRACKING_URI` is unset.

## Setup

```
uv sync
```

Verify the committed CP-1 artifact:

```bash
make test
make audit
make sql
```

The checks above run offline without a token. Only ENTSO-E network queries require
`ENTSOE_API_TOKEN` in the environment (never commit it -- see `.gitignore`).

## Month-0 data-layer spike (historical)

`scripts/q1_*.py` .. `scripts/q8_*.py` are the sample-pull probes behind
`docs/spike-feed-status.md`. Each is runnable standalone:

```
uv run scripts/q1_basic_access.py
```

Evidence JSON is written to `data/spike/` (gitignored scratch, not committed).
