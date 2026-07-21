# DE-LU Day-Ahead Price Forecasting

**What it is (30-second read).** A portfolio-grade probabilistic tool that forecasts the next delivery day's hourly German–Luxembourg (DE-LU) day-ahead electricity price, with calibrated 50 / 80 / 95 % prediction intervals.

- **Problem** — forecast 24 hourly DE-LU prices at the 12:00 CET day-ahead gate, across a three-regime market (the 2021–23 energy crisis, the negative-price/solar era, and Dunkelflaute scarcity).
- **Approach** — a single LightGBM nine-quantile ensemble, CQR-calibrated with isotonic monotonicity last; walk-forward CV with a 24 h embargo and pinned three-regime folds; **strict-gate features only** — the shipped model uses no input published after the gate (the day-ahead wind/solar forecast is measured in a separate post-gate benchmark, never shipped).
- **Results** — LightGBM vs. similar-day-naïve / 168h-naïve / Ridge, with Diebold–Mariano tests, a three-stage reliability diagram, SHAP, and a regime-stratified error table. *(Live from CP-3.)*
- **Honest limitations** — regime-shift exchangeability, the measured cost of strict-gate feasibility, the live negative-price floor, model staleness.
- **Demo & reproduction** — the **primary link is the static GitHub Pages report** (CDN-served, no container, no cold start); the interactive marimo Space is one labeled click deeper; `make train` after checking out the tagged commit reproduces the champion from the committed snapshot. *(Live from M5.)*

Full engineering plan: **`capstone_V6_3.md`**. Data: ENTSO-E Transparency Platform; Bundesnetzagentur | SMARD.de — CC BY 4.0.

## Setup

```
uv sync
```

Requires `ENTSOE_API_TOKEN` in the environment (never commit it -- see `.gitignore`).

## Month-0 data-layer spike

`scripts/q1_*.py` .. `scripts/q8_*.py` are the sample-pull probes behind
`docs/spike-feed-status.md`. Each is runnable standalone:

```
uv run scripts/q1_basic_access.py
```

Evidence JSON is written to `data/spike/` (gitignored scratch, not committed).
