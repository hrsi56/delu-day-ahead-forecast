# DE-LU Day-Ahead Price Forecasting

**What it is (30-second read).** A portfolio-grade probabilistic tool that forecasts the next delivery day's hourly German–Luxembourg (DE-LU) day-ahead electricity price, with calibrated 50 / 80 / 95 % prediction intervals.

- **Problem** — forecast the next delivery day's hourly DE-LU prices at the 12:00 CET day-ahead gate — normally 24 values, 23/25 on DST-transition days — across a three-regime market (the 2021–23 energy crisis, the negative-price/solar era, and Dunkelflaute scarcity).
- **Approach** — a single LightGBM nine-quantile ensemble, CQR-calibrated with isotonic monotonicity last; walk-forward CV with a one-delivery-day embargo and pinned three-regime folds; **strict-gate features only** — the shipped model uses no input published after the gate (the day-ahead wind/solar forecast is measured in a separate post-gate benchmark, never shipped).
- **Feature catalog** — frozen before fitting. Calendar and regime features, the day-ahead load forecast, lagged prices and closed-left rolling statistics, plus one candidate domain feature: a residual-load proxy built from a 42-day trailing mean of actual wind and solar generation ending at D-2. Two catalogs, one comparison, and the shipped one is named in the report — including when the domain feature does not earn its place.
- **Results** — LightGBM vs. similar-day-naïve / 168h-naïve / Ridge, with five-fold DM labeled **development / post-selection**, plus **one pre-specified evaluation on a 90-day holdout** the model never saw — reported once, whatever it says, and labeled *confirmatory-style, not power-qualified*. Three-stage reliability, SHAP, permutation importance, and regime-stratified errors. A separate one-number benchmark measures what the post-gate wind/solar forecast would have been worth. *(Live from CP-3.)*
- **Honest limitations** — regime-shift exchangeability; two disclosed assumptions (the load forecast's pre-gate availability, and revision in the actual-generation archive); the live negative-price floor; and model staleness, with **four cutoffs published separately** — snapshot, raw-model fit, final calibration, and holdout. The shipped model is exactly the model the holdout evaluated: there is no retrain after the result is opened.
- **Demo & reproduction** — the **primary link is the static GitHub Pages report** (CDN-served, no container, no cold start); the interactive marimo Space is one labeled click deeper, and what it renders over the holdout period is a **historical out-of-sample replay**, not a live forecast; `make train` after checking out the tagged commit reproduces the champion from the committed snapshot. The release is **frozen** — there is no scheduled refresh. *(Live from CP-3.)*

**Project shape:** three checkpoints — data and features (CP-1), model and analysis (CP-2), showcase and release (CP-3).

Full engineering plan: **`capstone_V6_7.md`** (v6.7). Data: ENTSO-E Transparency Platform; Bundesnetzagentur | SMARD.de — CC BY 4.0.

## Setup

```
uv sync
```

Requires `ENTSOE_API_TOKEN` in the environment (never commit it -- see `.gitignore`).

## Month-0 data-layer spike (historical)

`scripts/q1_*.py` .. `scripts/q8_*.py` are the sample-pull probes behind
`docs/spike-feed-status.md`. Each is runnable standalone:

```
uv run scripts/q1_basic_access.py
```

Evidence JSON is written to `data/spike/` (gitignored scratch, not committed).
