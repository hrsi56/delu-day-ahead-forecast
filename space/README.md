---
title: DE-LU Day-Ahead Price Forecasting
emoji: ⚡
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
short_description: Probabilistic DE-LU day-ahead price forecast, strict-gate, one-shot evaluated
tags:
  - energy
  - time-series
  - probabilistic-forecasting
  - conformal-prediction
  - lightgbm
---

# DE-LU day-ahead price forecasting — interactive deep dive

Probabilistic forecasts of the next delivery day's hourly German–Luxembourg day-ahead
electricity price, with calibrated 50 / 80 / 95 % prediction intervals from a LightGBM
nine-quantile ensemble, CQR-calibrated with isotonic monotonicity last.

**The static report is the primary entry point: [https://hrsi56.github.io/delu-day-ahead-forecast/](https://hrsi56.github.io/delu-day-ahead-forecast/).**
It is CDN-served and performs zero runtime calls. **This card describes the container
bundle, which is not what Hugging Face hosts.** On 2026-07-08 Hugging Face moved the Docker
SDK behind a paid plan, and a free Docker Space sleeps after inactivity. The hosted
interactive demo is therefore a Static Space built from `app/wasm_showcase.py`, which
cannot sleep; this bundle remains runnable locally and is verified under
`docker run --network none` by `make container-verify`.

> **Historical out-of-sample replay — the frozen champion forecasting a 90-day period it never trained on. This is not a live forecast.**

Anything this Space renders over the holdout window 2026-06-09..2026-09-06 is a replay of
a frozen model against a period it never trained on. It is never presented as a live
forecast, and the demo makes no live API call during a session: the champion and the
data snapshot are **bundled in the image**.

## The four cutoffs, stated separately because they are four different dates

| Cutoff | Value |
|---|---|
| `snapshot_cutoff` | 2026-09-06 |
| `raw_model_fit_cutoff` | 2026-04-07 |
| `final_calibration_window` | 2026-04-09..2026-06-07 |
| `holdout_window` | 2026-06-09..2026-09-06 |

The shipped model is exactly the model the holdout evaluated: there is no retrain and no re-tune after the result was opened. The raw-model fit cutoff precedes the snapshot cutoff by
152 delivery days; that is what shipping the evaluated model costs, and
it is stated rather than hidden. The day-ahead price floor moved to −600 EUR/MWh from 2026-05-28, an environment shift the frozen model predates.

## What is deployed

The artifact in this image is the **same bundled champion the holdout evaluated** —
`artifact_fingerprint_sha256` `57e3ad40a7f48bb7896628ce2e5dec61314dea567da9867aede4bf1b0a10e0fb`: the selected
`base` catalog's feature pipeline, 9 LightGBM
quantile heads, four CQR thresholds and the isotonic ordering guard, wrapped in one
`mlflow.pyfunc`. `python_model.pkl` is 30,830,306 bytes =
29.4 MiB (30.8 MB); the whole `models/champion/` directory is
31,623,247 bytes = 30.2 MiB. The frozen snapshot it reads
is pinned at `sha256` `7dd2dc73407706ca6bd3c1ad51d201ac0de35eec5ca129ce320cca639f697f00`.

The pickle's bytes are deliberately not the identity to check — MLflow stamps a fresh
UUID and creation time on every save — so the fingerprint above is computed over the
catalog, the feature list, the nine quantiles, the four thresholds and the nine boosters'
own serializations.


## Selected catalog

| Arm | Pooled raw-head mean pinball loss |
|---|---|
| `base` | `13.015841509664993` |
| `base + residual_load_proxy` | `13.064197422052183` |

Percentage difference (augmented vs base): **+0.371516%**. **Selected catalog:
`base`.** The rule was fixed before fitting; the domain feature did not
earn its place, and that is a reportable result rather than a failure.

## The one-shot holdout

| Metric | Champion | Similar-day naive | Difference |
|---|---|---|---|
| MAE (EUR/MWh) | 25.9078 | 27.7578 | -6.66% |
| Mean pinball loss | 6.7083 | 13.8789 | -51.67% |

Final empirical coverage over 2,160 rows on 90 delivery
days: **0.4407** / **0.7593** /
**0.9398** at the 50 / 80 / 95 % nominal levels. Probabilistic
daily-vector DM against the similar-day naive: statistic **-8.6798**,
p-value **1.98e-18**, standardized effect size
**-1.0478**.

> Pre-specified one-shot holdout DM test on a fixed 90-day window — confirmatory-style, not power-qualified.

## Development evidence, and what it does not say

The five pinned development folds carry `evidence_class =
development_post_selection` — descriptive post-selection evidence, never
confirmatory. **The development point-accuracy DM does not merely fail to show an advantage — it shows a deficit: the test is one-sided (reject if DM < −1.645), the statistic is +1.6228 with p = 0.948, and the champion's median is 28.58% worse than the similar-day naive over the development folds.** The probabilistic win is broad and
the point-accuracy win is not. That is reported here rather than omitted.

## What the post-gate forecast would have been worth

A controlled raw-head ablation, neither arm calibrated: adding the delivery-day A69 VRE
forecast and its named derivatives moves pooled mean pinball loss from
`13.015841509664993` to `10.478714632475889` — **-19.4926%**.

> This uncalibrated raw-head comparison isolates the information content of post-gate A69. It makes no claim about calibrated interval quality and does not make A69 available at the forecast gate.

## Limitations

- **Exchangeability under regime shift.** CQR provides finite-sample marginal coverage guarantees under exchangeability. The walk-forward CV mildly violates exchangeability — the crisis regime is not exchangeable with the pre-crisis regime, and the solar-driven negative-price era is not exchangeable with either — so empirical coverage may diverge from nominal on regime-shift folds. This is documented in the reliability diagram (Section 8.4).
- **Development versus one-shot evidence.** The five-fold development results are descriptive post-selection evidence, never confirmatory: those folds also chose the catalog. Only the 90-day holdout was pre-specified and opened once, and on the development folds the point-accuracy DM shows a deficit, not merely the absence of an advantage.
- **Disclosed assumption — the load forecast.** A65/A01 is pre-gate by explicit assumption, not by measurement: both the existence of the delivery-day load forecast before the 12:00 CET gate and its equality to the archived vector used here are assumed, and the regulatory update provision permits later revisions.
- **Disclosed assumption — the generation archive.** A75 aggregate actual generation is used at its current archived values, which may differ from the values visible in real time despite the D-2 boundary.
- **The measured cost of the strict gate.** The strict-gate design has a measured cost rather than an assumed one: the post-gate A69 forecast is worth 19.4926% of pooled raw-head pinball loss, and the project declines to use it.
- **A two-sided bounded target, live at the floor.** The target is two-sided and bounded: the price is routinely negative and has hit the −500 EUR/MWh floor, which truncates the lower conformity residuals, so the lowest intervals under-cover conditionally near the floor.
- **Coverage divergence.** Empirical coverage diverges from nominal: 0.4407 / 0.7593 / 0.9398 against 50 / 80 / 95 %, so the 50 % interval under-covers by roughly six points on the holdout window. On the crisis stratum it does not merely diverge, it collapses: over the August-2022 peak weeks the 95 % interval covered 0.194 of outcomes. The mechanism is measured — that fold's CQR thresholds were estimated on a May-June 2022 calibration window at a ~198 EUR/MWh level and applied to an evaluation block averaging 376 EUR/MWh, and the conformal correction is additive, not multiplicative. This is what a split-conformal guarantee does when exchangeability breaks; it is the defect the planned v2 targets, and it is not fixed in this release.
- **Model staleness, with all four cutoffs.** The deployed demo applies a frozen model whose raw-model fit cutoff (2026-04-07) precedes the snapshot cutoff (2026-09-06) by 152 delivery days, with the final calibration window 2026-04-09..2026-06-07 and the holdout window 2026-06-09..2026-09-06 — all four cutoffs published separately because they are four different dates.
- **The 15-minute MTU averaging choice.** From 2025-10-01 an hourly price is the mean of four quarter-hour prices, so every hour-level statistic here — the negative-hour tally included — depends on that averaging choice, and a quarter-hour tally differs.
- **Scope.** This is a portfolio artifact, not an operations system: no retraining schedule, no drift gate, no rollback machinery, no monitoring surface, and no multi-day-ahead forecast.
- **Scenario probes.** Scenario perturbations are ceteris-paribus sensitivity probes and may be out of distribution. They hold every other input fixed, so a
  large perturbation asks the model a question it was never trained on.

> The holdout is a single contiguous recent period, so it tests generalization to the most recent regime rather than repeated out-of-sample skill. Its partitions were pinned before development and it was evaluated once, after the complete model and calibration pipeline were frozen, with no subsequent tuning. The 90-day length was fixed by partition design, not by a power calculation, so the Diebold–Mariano result is confirmatory-style but not power-qualified. The model shown is exactly the model evaluated — no refit followed the holdout — so its raw-model fit cutoff precedes the snapshot cutoff by 152 delivery days. Sequential lag features may use earlier holdout observations exactly as they would in live forecasting; no holdout outcome entered fitting or a development decision. Enforcement is procedural: this is a solo build and the discipline is disclosed, not cryptographically guaranteed.

## Reproduction

```bash
git clone https://github.com/hrsi56/delu-day-ahead-forecast
cd delu-day-ahead-forecast
uv sync
uv run python predict_next_day.py          # offline, from the bundled snapshot
make test                                   # invariant suite + the CQR fixture
make train && make holdout                  # reproduce the champion and the holdout
docker build -t delu-showcase . && docker run -p 7860:7860 delu-showcase
```

- **Tagged commit.** Check out the tagged commit and run `uv sync` then `make train`: the champion is rebuilt from the committed snapshot with pinned dependencies and fixed seeds, no extra fetch.
- **MLflow permalinks.** Every decision-bearing run — the three baselines, both catalog candidates, both benchmark arms, the champion's final fit and holdout, and the diagnostics — is public at https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow with snapshot hash, code SHA, fold spec, feature list, seed, hyperparameters, metrics and artifact links. Counting runs there will not give you 'one', and it is not meant to: the tracking server shows several runs named `champion::final-fit-and-holdout`, because the script is deterministic and was re-run while CP-2 was authored — once aborted on the runtime firewall before any outcome was read, and every completed run reproducing the previous run's metrics and artifact fingerprint exactly. “Evaluated exactly once” is a statement about the evaluation decision, not about how many times a deterministic script may be executed — an Integration Critic re-running it from a clean worktree is reproducing the result, not taking a second look at the holdout. No catalog, hyperparameter, threshold or analysis choice was changed after any of them.
- **The registered `champion` alias.** The champion is registered on that MLflow instance as the model `delu-day-ahead-champion` under the `champion` alias, carrying release and lineage tags — `release_status=portfolio_release`, the source run id, the code commit, the snapshot hash and the four cutoffs. It is portfolio evidence only: the deployed demo loads the bundled artifact and never queries the registry.
- **Canonical entry point.** The static GitHub Pages report at https://hrsi56.github.io/delu-day-ahead-forecast/ is the canonical entry point, and the interactive Space at https://huggingface.co/spaces/Yarden-Viktor/delu-day-ahead-forecast is linked from it.
- **DuckDB SQL.** The hand-authored DuckDB queries in `sql/feature_queries.sql` express the same calendar-day lag and D-1-frozen rolling semantics as the canonical Python pipeline, and run against the committed Parquet with `make sql`.
- **The four cutoffs.** All four cutoffs are published separately: snapshot 2026-09-06, raw-model fit 2026-04-07, final calibration 2026-04-09..2026-06-07, holdout 2026-06-09..2026-09-06.
- **Attribution.** Data: ENTSO-E Transparency Platform; Bundesnetzagentur | SMARD.de — CC BY 4.0. Code MIT; the redistributed data stays CC BY 4.0 with attribution, and the trained champion is a derived work of it. See LICENSE and DATA-LICENSE.md.

The DagsHub repository UI is deliberately not linked anywhere: it redirects an anonymous
visitor to a sign-in page, while the `.mlflow` tracking URI above is anonymously readable.
