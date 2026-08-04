# DE-LU Day-Ahead Price Forecasting

**What it is (30-second read).** A portfolio-grade probabilistic tool that forecasts the next delivery day's hourly German–Luxembourg (DE-LU) day-ahead electricity price, with calibrated 50 / 80 / 95 % prediction intervals.

- **Problem** — forecast 24 hourly DE-LU prices at the 12:00 CET day-ahead gate, across a three-regime market (the 2021–23 energy crisis, the negative-price/solar era, and Dunkelflaute scarcity).
- **Approach** — a single LightGBM nine-quantile ensemble, CQR-calibrated with isotonic monotonicity last; walk-forward CV with a 24 h embargo and pinned three-regime folds; **strict-gate features only** — the shipped model uses no input published after the gate (the day-ahead wind/solar forecast is measured in a separate post-gate benchmark, never shipped).
- **Results** — LightGBM vs. similar-day-naïve / 168h-naïve / Ridge, with five-fold DM labeled development/post-selection, a separately sealed one-shot forward-audit status, three-stage reliability, SHAP, and regime-stratified errors. *(Live from CP-3; the forward audit may remain `PENDING_UNDERPOWERED`.)*
- **Honest limitations** — regime-shift exchangeability, the measured cost of strict-gate feasibility, the live negative-price floor, model staleness.
- **Demo & reproduction** — the **primary link is the static GitHub Pages report** (CDN-served, no container, no cold start); the interactive marimo Space is one labeled click deeper; `make train` after checking out the tagged commit reproduces the champion from the committed snapshot. *(Live from M5.)*

Full engineering plan: **`capstone_V6_5.md`**. Data: ENTSO-E Transparency Platform; Bundesnetzagentur | SMARD.de — CC BY 4.0.

## Current status

M0 and the data-feed de-risking spike are complete. The v6.4 governance/statistical-audit amendment is ratified and version-controlled; its operational validation begins only when an authorized CP-1 run starts. **M1 has not started and CP-1 is pending.** Track B begins only from a one-repository/one-checkpoint Orchestrator brief and returns one consolidated evidence packet before any later checkpoint is authorized. The superseded full v6.3 plan remains available in Git history at `0b9c5cb:capstone_V6_3.md`.

Execution contract: `engineering-role.md`. Canonical boundary templates: `docs/track-b/gauntlet-templates.md`. Critic isolation is a plain `git worktree` at the candidate SHA; verdicts are markdown under `docs/track-b/evidence/<checkpoint>/`. These files do not themselves activate CP-1.

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
