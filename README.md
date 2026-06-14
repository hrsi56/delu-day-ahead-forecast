# DE-LU Day-Ahead Price Forecasting

Probabilistic day-ahead electricity price forecasting for the German-Luxembourg
(DE-LU) bidding zone. See `capstone_V6_1.md` for the full engineering plan.

Data: ENTSO-E Transparency Platform; Bundesnetzagentur | SMARD.de -- CC BY 4.0.

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
