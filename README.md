# DE-LU Day-Ahead Price Forecasting

**What it is (30-second read).** A portfolio-grade probabilistic tool that forecasts the next delivery day's hourly German–Luxembourg (DE-LU) day-ahead electricity price, with calibrated 50 / 80 / 95 % prediction intervals.

- **Problem** — forecast the next delivery day's hourly DE-LU prices at the 12:00 CET day-ahead gate — normally 24 values, 23/25 on DST-transition days — across a three-regime market (the 2021–23 energy crisis, the negative-price/solar era, and Dunkelflaute scarcity).
- **Approach** — a single LightGBM nine-quantile ensemble, CQR-calibrated with isotonic monotonicity last; walk-forward CV with a one-delivery-day embargo and pinned three-regime folds; **strict-gate features only** — the shipped model uses no input published after the gate (the day-ahead wind/solar forecast is measured in a separate post-gate benchmark, never shipped).
- **Feature catalog** — frozen before fitting. Calendar and regime features, the day-ahead load forecast, calendar-day-matched price lags and D-1-frozen rolling statistics, plus one candidate domain feature: a residual-load proxy built from a 42-day trailing mean of actual wind and solar generation ending at D-2. Two catalogs, one comparison, and the shipped one is named in the report — including when the domain feature does not earn its place.
- **Results** — LightGBM vs. similar-day-naïve / 168h-naïve / Ridge, with five-fold DM labeled **development / post-selection**, plus **one pre-specified evaluation on a 90-day holdout** the model never saw — reported once, whatever it says, and labeled *confirmatory-style, not power-qualified*. Three-stage reliability, SHAP, permutation importance, and regime-stratified errors. A separate one-number benchmark measures what the post-gate wind/solar forecast would have been worth.
- **Honest limitations** — regime-shift exchangeability; two disclosed assumptions (the load forecast's pre-gate availability, and revision in the actual-generation archive); the live negative-price floor; and model staleness, with **four cutoffs published separately** — snapshot, raw-model fit, final calibration, and holdout. The shipped model is exactly the model the holdout evaluated: there is no retrain after the result is opened.
- **Demo & reproduction** — the **primary link is the static GitHub Pages report** (CDN-served, no container, no cold start); the interactive marimo Space is one labeled click deeper, and what it renders over the holdout period is a **historical out-of-sample replay**, not a live forecast; `make train` after checking out the tagged commit reproduces the champion from the committed snapshot. The release is **frozen** — there is no scheduled refresh. The static page, the container and the Space bundle are built and verified; publication is the owner's step and is not yet taken — see [`docs/deploy.md`](docs/deploy.md).

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

Percentage difference (augmented vs base): **+0.371516%**.

**Selected catalog: `base`.** The augmented catalog ships only if its unrounded stored pooled
loss is lower; it is not, so the champion ships strict-gate as `base`. The domain feature did not
earn its place on the pooled metric that decides, and that is a reportable result, not a failure.
The fold-level picture is not uniform — the augmented arm is lower on
2 of the 5 folds, and the report gives that table —
but §4.1 fixes the rule as pooled and fixes it before fitting, so the split is disclosed and the
decision is not revisited.

**Development metrics are descriptive post-selection evidence** (`evidence_class =
development_post_selection`), never confirmatory superiority. **The development point-accuracy DM does not merely fail to show an advantage — it shows a deficit: the test is one-sided (reject if DM < −1.645), the statistic is +1.6228 with p = 0.948, and the champion's median is 28.58% worse than the similar-day naive over the development folds.**
Reported here rather than omitted or reframed. The probabilistic daily-vector DM on the same folds reads statistic
-2.5517, p = 0.00536. The champion beats the similar-day
naive on mean pinball loss in 5 of the 5 evaluation
blocks and on median MAE in 3 of 5: the probabilistic win is
broad, the point-accuracy loss is not. The pooled MAE gap of +9.29 EUR/MWh
comes almost entirely from **fold_3**, the crisis-peak block, which contributes
+10.87 of it alone. The mechanism is measured, not assumed: the model did see the crisis — that fold's training ran to 2022-04-29 and included
5,784 crisis hours at a 173 EUR/MWh mean and a 700 EUR/MWh maximum — but **61.3% of the evaluation
block sits above the 99th percentile of everything it ever saw, while only 2.45% exceeds its
maximum.** So this is shrinkage toward the training level, not an extrapolation wall: a leaf's value
is an average over the training rows that fall in it, and the far more numerous moderate-price rows
pull the prediction down. Persistence has no training distribution at all, so it carries the level
for free. Full tables, both DM
analyses, the three-stage reliability read, SHAP, permutation importance and the regime-stratified
table are in [`docs/cp2-model-report.md`](docs/cp2-model-report.md) and `reports/cp2/`.

**One pre-specified holdout evaluation, opened once.** Champion MAE 25.9078 vs
similar-day naive 27.7578 EUR/MWh
(-6.66%); champion mean pinball loss
6.7083 vs 13.8789
(-51.67%); final empirical coverage
0.4407 / 0.7593 /
0.9398 at the 50 / 80 / 95 % nominal levels; probabilistic
daily-vector DM statistic -8.6798, p = 1.98e-18,
standardized effect size -1.0478, over
90 delivery days (2,160 rows).

> Pre-specified one-shot holdout DM test on a fixed 90-day window — confirmatory-style, not power-qualified.

**The shipped model is exactly the model the holdout evaluated: there is no retrain and no re-tune after the result was opened.** The frozen artifact is `models/champion/`, a single
`mlflow.pyfunc` wrapping the 9 quantile heads, the selected catalog's
25-feature pipeline, the four CQR thresholds and the isotonic ordering guard,
fit on 62,688 rows and calibrated on 1,440. Its identity
is `artifact_fingerprint_sha256` `57e3ad40a7f48bb7896628ce2e5dec61314dea567da9867aede4bf1b0a10e0fb`, recorded in
`models/champion/champion_card.json` and computed over the catalog, the feature list, the nine
quantiles, the four thresholds and the nine boosters' own serializations; the pickle's own bytes are
not stable, because MLflow stamps a fresh UUID and creation time on every save.
`python_model.pkl` is 30,830,306 bytes = 29.4 MiB (30.8 MB); the whole
`models/champion/` directory is 31,623,247 bytes = 30.2 MiB. The
snapshot it reads is pinned at `sha256` `7dd2dc73407706ca6bd3c1ad51d201ac0de35eec5ca129ce320cca639f697f00`.

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
calibrated: adding the delivery-day A69 forecast and its derivatives moves pooled mean pinball loss
from `13.015841509664993` to `10.478714632475889` — **-19.4926%**.

> This uncalibrated raw-head comparison isolates the information content of post-gate A69. It makes no claim about calibrated interval quality and does not make A69 available at the forecast gate.

**Experiment records** for every decision-bearing run — the three baselines, both catalog
candidates, both benchmark arms, the champion's final fit and holdout — are public at
<https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow> with snapshot hash, code SHA, fold spec, feature list, seed, hyperparameters,
metrics and artifact links.

Reproduce with `make cp2` after `uv sync`; every stage runs offline and MLflow logging is skipped
silently when `MLFLOW_TRACKING_URI` is unset.

## CP-3 showcase and release

### Three public surfaces — all live

Each one answers a different question, and each stands on its own. The CV carries the first.

| | Surface | Answers | Cost to open |
|---|---|---|---|
| **1** | **[📄 Static report](https://hrsi56.github.io/delu-day-ahead-forecast/)**<br>the primary link | *Can they reason, and will they tell me what went wrong?* The full §10 reading order — data, regimes, catalog, validation design, results, SHAP, regimes, reliability, forecast, limitations, reproduction | **zero network calls.** One self-contained file. Cannot sleep, cannot break when a CDN does, renders offline |
| **2** | **[⚡ Interactive Space](https://huggingface.co/spaces/Yarden-Viktor/delu-day-ahead-forecast)**<br>[direct app](https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/) | *Does the thing actually run?* The champion's own boosters executing in your browser under Pyodide — no server | about 57 MB first visit, 352 requests, 5 hosts; ~1 MB after. **A Static Space executes nothing, so it never sleeps** |
| **3** | **[🔬 MLflow on DagsHub](https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow)** | *Is the decision trail real, or is the README the only evidence?* Every decision-bearing run, anonymously readable — no sign-in | — |

The Space cannot load the packaged `mlflow.pyfunc`, so it runs the champion's own nine boosters, base-catalog preprocessing, four CQR thresholds and isotonic step in the browser — and on a committed 54-day fixture spanning all three regimes, both daylight-saving transitions, and federal holidays and bridge days (1,296 rows, 11,628 quantile values) its output equals the frozen artifact bitwise: maximum absolute deviation 0.0. Opened through huggingface.co, Hugging Face's own page adds its document and 201 requests from huggingface.co, js.stripe.com, cdnjs.cloudflare.com and an AWS WAF host — about 1.2 MB measurable, on a page Hugging Face controls — and runs the app in an iframe. The app alone is at https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/.

**Deployment status: complete.** Pages live; the Static Space live and serving. On 2026-07-08 Hugging
Face moved the Docker and Gradio SDKs behind a paid PRO plan and only Static Spaces stayed free, so
the containerised path could not be hosted at this project's ratified $0 rate. **The container is not
abandoned and not hypothetical** — it builds, and `make container-verify` runs it under
`docker run --network none` with every external host unreachable.

#### The decision trail, addressed directly

Every link below was checked from an **unauthenticated** client. The DagsHub *repository* UI redirects
an anonymous visitor to a sign-in page; the `.mlflow` tracking host does not, which is why every link
here uses it.

| | |
|---|---|
| **[Experiment `delu-cp2`](https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow/#/experiments/0)** | every v1 run, side by side |
| **[Model registry](https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow/#/models)** | the registered champion and its `champion` alias |
| **[Tracking root](https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow)** | if a deep link ever moves, start here |

Runs are named rather than linked by id, because several decision-bearing runs were reproduced and no
single id is canonical — the name is what to search for:

| Run name | What it decided |
|---|---|
| `catalog::base` | the selected catalog's development arm |
| `catalog::base_plus_residual_load_proxy` | the domain-feature arm that lost, by +0.371516% |
| `baseline::similar_day_naive` | the headline comparator |
| `baseline::seasonal_naive_168h` | the second baseline |
| `baseline::ridge` | the third baseline |
| `benchmark::base` | the strict-gate arm of the §7.2 benchmark |
| `benchmark::base+a69` | the post-gate arm -- what the unavailable forecast is worth |
| `champion::final-fit-and-holdout` | the frozen champion and the one-shot holdout |
| `diagnostics::champion` | SHAP, permutation importance, regimes, reliability |

**Where v2 will go.** No v2 run exists yet. When M4 is ratified its runs land in a separate `delu-m4` experiment on the same tracking server, so v1's record stays exactly as the one-shot holdout left it and the two are never mixed in one experiment.

**Run it yourself, offline:**

```bash
uv sync
uv run python predict_next_day.py --level 80 --self-check   # bundled snapshot, no network
uv run marimo run app/showcase.py                            # the container's showcase, server mode
make wasm && make wasm-serve                                 # the Static Space, at http://127.0.0.1:8820
docker build -t delu-showcase . && docker run -p 7860:7860 delu-showcase
make pages                                                   # rebuild docs/index.html
```

`--self-check` is not decoration: it re-runs the delivery day with its own prices masked and
requires bitwise-identical output, then mutates an in-window D−1 price and requires the output to
**move**. A boundary check that can only ever report "nothing changed" is satisfied by a broken
model, so the positive control is part of the check.

### What the shipped model is

`artifact_fingerprint_sha256` `57e3ad40a7f48bb7896628ce2e5dec61314dea567da9867aede4bf1b0a10e0fb` — the `base` catalog's
25-feature pipeline, 9 LightGBM quantile heads, four
CQR thresholds and isotonic last, in one `mlflow.pyfunc`. Snapshot `sha256`
`7dd2dc73407706ca6bd3c1ad51d201ac0de35eec5ca129ce320cca639f697f00`. `python_model.pkl` is 30,830,306 bytes =
29.4 MiB (30.8 MB); the whole `models/champion/` directory is 31,623,247 bytes
= 30.2 MiB.

**The four cutoffs, identical on every surface:** snapshot `2026-09-06` · raw-model fit
`2026-04-07` · final calibration `2026-04-09..2026-06-07` · holdout
`2026-06-09..2026-09-06`.

**The one-shot holdout, as published everywhere else:** MAE 25.9078 vs
27.7578 (-6.66%); mean pinball 6.7083 vs
13.8789 (-51.67%); coverage 0.4407 /
0.7593 / 0.9398; DM statistic -8.6798,
p 1.98e-18, effect -1.0478. Selected catalog
`base` (`13.015841509664993` vs `13.064197422052183`,
+0.371516%). Development evidence class `development_post_selection`, with the
point-accuracy DM at p = 0.948 — a deficit, not merely no advantage
(28.58% worse). Post-gate
benchmark `13.015841509664993` → `10.478714632475889`, **-19.4926%**.

> Pre-specified one-shot holdout DM test on a fixed 90-day window — confirmatory-style, not power-qualified.

> This uncalibrated raw-head comparison isolates the information content of post-gate A69. It makes no claim about calibrated interval quality and does not make A69 available at the forecast gate.

### The replay label is a truthfulness requirement

> Historical out-of-sample replay — the frozen champion forecasting a 90-day period it never trained on. This is not a live forecast.

Anything the Space or the static page renders over the holdout window 2026-06-09..2026-09-06 is that
replay. It is never presented as a live forecast. The one scenario control is likewise labelled:

> Scenario perturbations are ceteris-paribus sensitivity probes and may be out of distribution.

### Honest limitations, stated here as well as on the page

§7.1 requires this paragraph verbatim in the report, and item 5 requires the surfaces to agree, so
it lives here too rather than in one document only:

> The holdout is a single contiguous recent period, so it tests generalization to the most recent regime rather than repeated out-of-sample skill. Its partitions were pinned before development and it was evaluated once, after the complete model and calibration pipeline were frozen, with no subsequent tuning. The 90-day length was fixed by partition design, not by a power calculation, so the Diebold–Mariano result is confirmatory-style but not power-qualified. The model shown is exactly the model evaluated — no refit followed the holdout — so its raw-model fit cutoff precedes the snapshot cutoff by 152 delivery days. Sequential lag features may use earlier holdout observations exactly as they would in live forecasting; no holdout outcome entered fitting or a development decision. Enforcement is procedural: this is a solo build and the discipline is disclosed, not cryptographically guaranteed.

§6.2 requires this one verbatim, for the same reason:

> CQR provides finite-sample marginal coverage guarantees under exchangeability. The walk-forward CV mildly violates exchangeability — the crisis regime is not exchangeable with the pre-crisis regime, and the solar-driven negative-price era is not exchangeable with either — so empirical coverage may diverge from nominal on regime-shift folds. This is documented in the reliability diagram (Section 8.4).

§10 item (11) fixes the complete set, and it is rendered from one place onto every surface — prose
written separately per surface is how a limitation ends up on one page and nowhere else:

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

And one on the environment: The day-ahead price floor moved to −600 EUR/MWh from 2026-05-28, an environment shift the frozen model predates. None of this is engineered around; a floor-aware
tail would reopen scope this project deliberately closed.

### Reproducibility statement

§10 item (12) fixes what a complete one contains, and it too is rendered from one place onto every
surface:

- **Tagged commit.** Check out the tagged commit and run `uv sync` then `make train`: the champion is rebuilt from the committed snapshot with pinned dependencies and fixed seeds, no extra fetch.
- **MLflow permalinks.** Every decision-bearing run — the three baselines, both catalog candidates, both benchmark arms, the champion's final fit and holdout, and the diagnostics — is public at https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow with snapshot hash, code SHA, fold spec, feature list, seed, hyperparameters, metrics and artifact links. Counting runs there will not give you 'one', and it is not meant to: the tracking server shows several runs named `champion::final-fit-and-holdout`, because the script is deterministic and was re-run while CP-2 was authored — once aborted on the runtime firewall before any outcome was read, and every completed run reproducing the previous run's metrics and artifact fingerprint exactly. “Evaluated exactly once” is a statement about the evaluation decision, not about how many times a deterministic script may be executed — an Integration Critic re-running it from a clean worktree is reproducing the result, not taking a second look at the holdout. No catalog, hyperparameter, threshold or analysis choice was changed after any of them.
- **The registered `champion` alias.** The champion is registered on that MLflow instance as the model `delu-day-ahead-champion` under the `champion` alias, carrying release and lineage tags — `release_status=portfolio_release`, the source run id, the code commit, the snapshot hash and the four cutoffs. It is portfolio evidence only: the deployed demo loads the bundled artifact and never queries the registry.
- **Canonical entry point.** The static GitHub Pages report at https://hrsi56.github.io/delu-day-ahead-forecast/ is the canonical entry point, and the interactive Space at https://huggingface.co/spaces/Yarden-Viktor/delu-day-ahead-forecast is linked from it.
- **DuckDB SQL.** The hand-authored DuckDB queries in `sql/feature_queries.sql` express the same calendar-day lag and D-1-frozen rolling semantics as the canonical Python pipeline, and run against the committed Parquet with `make sql`.
- **The four cutoffs.** All four cutoffs are published separately: snapshot 2026-09-06, raw-model fit 2026-04-07, final calibration 2026-04-09..2026-06-07, holdout 2026-06-09..2026-09-06.
- **Attribution.** Data: ENTSO-E Transparency Platform; Bundesnetzagentur | SMARD.de — CC BY 4.0. Code MIT; the redistributed data stays CC BY 4.0 with attribution, and the trained champion is a derived work of it. See LICENSE and DATA-LICENSE.md.

### Link discipline

Every link to the experiment tracking is the `.mlflow` URI. Verified from an unauthenticated client
on 2026-09-14: the DagsHub repository root, `/experiments`, `/models` and `/src/main` all answer
`302 → /user/login` for a connected repository, while <https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow> serves real MLflow content
and live runs anonymously. A link to the repository UI would land a reader on a sign-in page, so
`tests/test_17_cross_surface_agreement.py` fails the build if one reappears on any surface.

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
