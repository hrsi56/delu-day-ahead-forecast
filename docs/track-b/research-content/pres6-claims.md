# PRES-6: claim-to-evidence map

**2026-11-14 · PRES-6, under PUBLISH_RULES 1.5 A8 (triggered by ruling O46) and research v21-r20 §24.14.** The claims
the final product's two new sections render, **Product results** and **Business insights**, for v6 · DDNN-2 alone (A1
in the frozen records; policy `720fc581…`). Each claim is mapped to a committed file and the field it reads. Values here
are rounded from the saved values; the rendered surfaces bind to evidence records of `src/delu_forecast/research.py`,
never to these digits. Every number uses development data only, delivery days through 2026-09-06 (§24.14, P1); the
rules that produced them were committed first (`docs/track-b/evidence/pres-6/publication-packet.md` §0).

**Default evidence class:** `development_post_selection`: v6 was selected on these days (CP-28). Nothing here is
prospective or 4.7T's; the Space shows the live record, "prospective evaluation in progress".

## Source keys

| Key | File |
|---|---|
| PR6 | [reports/pres6/product-results/](../../../reports/pres6/product-results/) — `regimes.csv`, `coverage.csv`, `monthly.csv`, `days.csv`, `bins.csv`, `summary.json`, written by `src/delu_forecast/final_candidate.py --product` |
| DL28 | [reports/cp28/results/daily-losses.parquet](../../../reports/cp28/results/daily-losses.parquet) (CP-28's daily losses: stream A1 = v6, B0 = the naive) |
| FC28 | [reports/cp28/forecast/hourly.parquet](../../../reports/cp28/forecast/hourly.parquet) (v6's stored quantiles, arm A1) |
| P24 | [reports/ddnn2/attempt-1/predictions.parquet](../../../reports/ddnn2/attempt-1/predictions.parquet) (`y_true`, the observed prices of v5's periods) |
| PK6 | [docs/track-b/evidence/pres-6/publication-packet.md](../evidence/pres-6/publication-packet.md) §0 (the rules) |

## Product results (§5.1a)

| ID | Claim | Source | Class |
|---|---|---|---|
| C1001 | On CP-26's 2,068 eligible development days (49,596 scored hours), v6's mean daily point error is 17.19 EUR/MWh [95% 15.45, 19.09] against the similar-day naive's 34.55 [31.09, 38.26], a ratio of 0.4974 [0.4734, 0.5230]; its mean daily interval score 9.68 [8.68, 10.78] against 21.14 [19.13, 23.35], a ratio of 0.4580 [0.4353, 0.4821]. Intervals: §0's paired 14-day moving-block bootstrap, 2,000 draws, seed 20261114. | PR6 `regimes.csv` (`regime` all); DL28 | S-d |
| C1002 | By regime, v6's mean daily point error and interval score, with the naive's and the ratio, each with its interval: before the crisis (246 days) 6.25 and 3.51; in the crisis (481 days) 30.67 and 16.98; from 2023 (1,341 days) 14.36 and 8.20. No regime is thin (≥ 60 days). | PR6 `regimes.csv` | S-d |
| C1003 | v6's intervals cover, over the 2,068 days, 0.4779 of the hours at 50% (mean width 25.5 EUR/MWh), 0.7826 at 80% (51.7) and 0.9437 at 95% (88.8); by regime the crisis is lowest (0.4356, 0.7531, 0.9314) and widest. Coverage with width; the nominal level is a reference, not a target. | PR6 `coverage.csv`; DL28 | S-d |
| C1004 | The month-by-month means of the daily errors over 70 calendar months (2020-12 to 2026-09): v6 below the naive in every month on both scores, highest in the crisis months. | PR6 `monthly.csv` | S-d |
| C1005 | The three rule-chosen days (§0: per regime, the P-v5 day at the regime's median v6 daily MAE): 2021-06-16 (before the crisis, MAE 5.3), 2022-07-26 (crisis, 35.1), 2025-05-02 (from 2023, 12.1), each with v6's median and 50/80/95% intervals against the cleared price. | PR6 `days.csv`, `summary.json` `chosen_days` | S |
| C1006 | Over every scored hour of P-v5 (8,587 hours, 358 days), binned into ten deciles of v6's median forecast, the mean observed price tracks the mean forecast in every bin; the 80% interval holds 0.6868–0.8685 of each bin's hours. | PR6 `bins.csv` | S-d |
| C1007 | v6's explanation: see the packet's §0 and §5b; the source and method follow the Orchestrator's ruling, or the section states the gap. | PK6 | S |

## The publication's wording

| ID | Claim | Source | Class |
|---|---|---|---|
| P67 | **The A8 order (ruling O46):** the product opening, How the product works, **Product results**, **Business insights**, then How the models compare; descriptive routes visible by default. | PUBLISH_RULES §5, A8; O46 | O |
| P68 | **The product finding** (A2's bound under A8): v6's mean daily point error and interval score on every eligible development day against the naive, with their intervals, and its 80% coverage with width; development evidence after selection; the live record is on the Space. | C1001, C1003 | Def, O |
| P69 | **Each graphic names** the policy and artifact (v6, CP-28's stored forecasts, arm A1), the population, its dates and units, and its evidence class. | PUBLISH_RULES §5.1a, §6 | O |
| P70 | **Business insights:** the intended use (a day-ahead hourly price forecast with intervals, issued before the 12:00 auction, for bidding, scheduling and hedging decisions); the measured forecasting implications (C1001–C1003); the gap: no decision policy, cost model or trading simulation has been authorized or run, so there is no profit, value or loss figure, and error reduction and interval coverage are neither profit nor a success rate; the limits. | PUBLISH_RULES §5.1a; the brief's outcome 3 | O |
| P71 | **R1–R7 (Integration review 4):** "the lowest error of the re-baseline's policies" (R1); 4.7T's bootstrap gives "the p-values" (R2); the values table names each code's experiment (R3); the every-day panel's question as a sentence (R5); the live record's wording that holds on both 4.7T branches (R7). | PRES-5's review 4 | O |

## Withheld claims

| ID | Withheld | Why |
|---|---|---|
| W54 | Calling an error, coverage or interval figure a profit, a gain in money, a return or a success rate; or showing a profit curve | No decision-policy or economic evaluation exists (§5.1a; the brief's outcome 3) |
| W55 | Presenting a product result as prospective, live, unused-data or 4.7T evidence | Every product result is development, post-selection (P1; §5.1a) |
