# CP-29: battery arbitrage on the development forecasts

**Simulated, development, post-selection.** A simulation of a price-taking battery on the development days, under the Owner's approved economic-policy contract (`docs/track-b/economic-policy-contract-2026-11-15.md`, decision 32). No money was traded. v6 was selected on these same days (CP-28), so its result is optimistic for v6. The rules this round fixed before any number are in `docs/track-b/evidence/cp-29/publication-packet.md` §0.

## What was evaluated

- **The battery:** 1 MW at the grid, 2 MWh usable, 85% round trip (√0.85 on charge and on discharge), empty at the start and the end of each delivery day, at most 2 MWh leaving its terminals a day, and charging or discharging in an hour, never both.
- **The costs:** wear of €25 per MWh leaving the battery's terminals (with €0 and €50 as sensitivity), and an exchange fee of €0.10 per MWh bought and per MWh sold. No grid fees, under the German storage exemption.
- **The rule:** on the day before, the schedule that maximizes the forecast's net value (median rule: the forecast median as the price; risk-aware variant: buy at the 75th percentile, sell at the 25th). If that value is not above zero, the battery does nothing. The schedule is then settled at the cleared day-ahead prices, with the same costs.
- **The sources:** v6 (CP-28's stored forecasts, arm A1), the similar-day naive (its frozen rule, from the committed snapshot), v5 (CP-24's committed predictions, only on P-v5) and perfect foresight (the cleared prices themselves: the ceiling).
- **The populations:** P-all, every eligible development day from 2020-12-29 to 2026-09-06 (2,068 days), and P-v5, the 358 days of v5's test periods 2–5 inside it.

## Checks run before the results

- **The naive's parity:** its central vector equals CP-26's B0 central vector bit for bit wherever a committed record holds it (8 of 8 records), and the frozen package's issued B0 central vector on 5 further days.
- **The solver against a brute force:** on 184 sampled day-source-rule programmes, an exhaustive search over a grid of schedules never beat the solver (none did).
- **The limits:** every one of the 26,964 daily schedules meets every limit; perfect foresight is never negative on a day (its lowest day: 0.00 EUR).
- **The tie-break:** 0 tie-break solves fell back to the previous stage (0 rows), as §0 provides.
- **Days not traded because an hour is missing** (contract §5: kept, counted, profit zero): naive 11, v5 4, v6 33.

## Results on P-all, at the main wear cost (€25 per MWh)

| Source and rule | Cumulative net profit, EUR | Share of perfect foresight | Trading days | Losing days | Largest daily loss, EUR | Maximum drawdown, EUR | Mean / median daily profit, EUR | 5th–95th percentile, EUR | Discharged from the battery, MWh (full cycles) |
|---|---|---|---|---|---|---|---|---|---|
| v6, median rule | 257,212 | 89.5% | 1,770 of 2,068 | 137 (6.6%) | 97 | 136 | 124.4 / 92.1 | −4.3 to 358.6 | 3,482 (1,741) |
| v6, risk-aware variant | 247,436 | 86.1% | 1,457 of 2,068 | 39 (1.9%) | 101 | 101 | 119.6 / 84.9 | 0.0 to 357.7 | 2,796 (1,398) |
| Similar-day naive, median rule | 220,136 | 76.6% | 1,872 of 2,068 | 355 (17.2%) | 227 | 288 | 106.4 / 66.7 | −29.4 to 326.9 | 3,653 (1,827) |
| Perfect foresight (the ceiling) | 287,292 | 100.0% | 1,857 of 2,068 | 0 (0.0%) | 0 | 0 | 138.9 / 109.0 | 0.0 to 370.0 | 3,626 (1,813) |

## Results on P-v5, at the main wear cost

| Source and rule | Cumulative net profit, EUR | Share of perfect foresight | Trading days | Losing days | Largest daily loss, EUR | Maximum drawdown, EUR | Mean / median daily profit, EUR | 5th–95th percentile, EUR | Discharged from the battery, MWh (full cycles) |
|---|---|---|---|---|---|---|---|---|---|
| v6, median rule | 55,708 | 91.0% | 284 of 358 | 21 (5.9%) | 43 | 43 | 155.6 / 124.7 | −2.9 to 462.8 | 558 (279) |
| v6, risk-aware variant | 53,996 | 88.2% | 241 of 358 | 5 (1.4%) | 16 | 16 | 150.8 / 117.3 | 0.0 to 460.4 | 471 (235) |
| Similar-day naive, median rule | 49,120 | 80.2% | 308 of 358 | 60 (16.8%) | 55 | 150 | 137.2 / 103.3 | −27.9 to 458.4 | 605 (303) |
| v5, median rule | 55,544 | 90.7% | 302 of 358 | 35 (9.8%) | 40 | 86 | 155.1 / 120.4 | −10.4 to 461.3 | 585 (292) |
| v5, risk-aware variant | 53,992 | 88.2% | 253 of 358 | 10 (2.8%) | 15 | 15 | 150.8 / 116.5 | 0.0 to 457.9 | 488 (244) |
| Perfect foresight (the ceiling) | 61,231 | 100.0% | 306 of 358 | 0 (0.0%) | 0 | 0 | 171.0 / 145.0 | 0.0 to 490.6 | 600 (300) |

## The wear cost's sensitivity

P-all:

| Source and rule | €0 per MWh: profit, EUR (share) | €25 per MWh: profit, EUR (share) | €50 per MWh: profit, EUR (share) |
|---|---|---|---|
| v6, median rule | 356,333 (92.1%) | 257,212 (89.5%) | 176,202 (84.9%) |
| v6, risk-aware variant | 353,809 (91.4%) | 247,436 (86.1%) | 160,065 (77.2%) |
| Similar-day naive, median rule | 322,199 (83.3%) | 220,136 (76.6%) | 139,147 (67.1%) |
| Perfect foresight (the ceiling) | 386,892 (100.0%) | 287,292 (100.0%) | 207,418 (100.0%) |

P-v5:

| Source and rule | €0 per MWh: profit, EUR (share) | €25 per MWh: profit, EUR (share) | €50 per MWh: profit, EUR (share) |
|---|---|---|---|
| v6, median rule | 72,933 (93.0%) | 55,708 (91.0%) | 42,678 (89.2%) |
| v6, risk-aware variant | 72,494 (92.4%) | 53,996 (88.2%) | 40,510 (84.7%) |
| Similar-day naive, median rule | 67,106 (85.6%) | 49,120 (80.2%) | 36,333 (75.9%) |
| v5, median rule | 72,647 (92.6%) | 55,544 (90.7%) | 42,580 (89.0%) |
| v5, risk-aware variant | 72,471 (92.4%) | 53,992 (88.2%) | 40,285 (84.2%) |
| Perfect foresight (the ceiling) | 78,431 (100.0%) | 61,231 (100.0%) | 47,841 (100.0%) |

## By regime (P-all, €25): cumulative profit, EUR (share of perfect foresight)

| Source and rule | All days | Before the crisis (to 2021-08-31) | The crisis (2021-09-01 to 2022-12-31) | From 2023-01-01 |
|---|---|---|---|---|
| Days | 2,068 | 246 | 481 | 1,341 |
| v6, median rule | 257,212 (89.5%) | 3,515 (64.5%) | 83,995 (87.8%) | 169,702 (91.2%) |
| v6, risk-aware variant | 247,436 (86.1%) | 2,650 (48.6%) | 81,609 (85.3%) | 163,177 (87.7%) |
| Similar-day naive, median rule | 220,136 (76.6%) | 333 (6.1%) | 70,407 (73.6%) | 149,396 (80.3%) |
| Perfect foresight (the ceiling) | 287,292 (100.0%) | 5,454 (100.0%) | 95,719 (100.0%) | 186,119 (100.0%) |

## Paired differences, with their uncertainty

Day by day on the same days; the 95% interval from a paired non-circular moving-block bootstrap over days (14-day blocks, 2,000 replicates, seed 20261115). The interval describes how the difference varies across resampled blocks of these development days; it is not a forecast for other days.

| Population | Rule | Difference | Wear, €/MWh | Days | Mean daily difference, EUR [95% interval] | Total difference, EUR [95% interval] |
|---|---|---|---|---|---|---|
| P-all | median | v6 − naive | 25 | 2,068 | +17.9 [+15.6, +20.5] | +37,077 [+32,323, +42,311] |
| P-v5 | median | v6 − naive | 25 | 358 | +18.4 [+13.6, +22.7] | +6,588 [+4,884, +8,114] |
| P-v5 | median | v6 − v5 | 25 | 358 | +0.5 [−2.0, +2.9] | +165 [−727, +1,032] |
| P-v5 | risk-aware | v6 − v5 | 25 | 358 | +0.0 [−2.5, +2.9] | +3 [−889, +1,044] |
| P-all | median | v6 − naive | 0 | 2,068 | +16.5 [+14.1, +19.1] | +34,134 [+29,216, +39,434] |
| P-v5 | median | v6 − naive | 0 | 358 | +16.3 [+11.6, +21.0] | +5,826 [+4,157, +7,501] |
| P-v5 | median | v6 − v5 | 0 | 358 | +0.8 [−1.7, +3.2] | +285 [−598, +1,135] |
| P-v5 | risk-aware | v6 − v5 | 0 | 358 | +0.1 [−2.3, +2.1] | +23 [−810, +748] |
| P-all | median | v6 − naive | 50 | 2,068 | +17.9 [+15.6, +20.5] | +37,055 [+32,286, +42,491] |
| P-v5 | median | v6 − naive | 50 | 358 | +17.7 [+12.9, +21.8] | +6,345 [+4,619, +7,815] |
| P-v5 | median | v6 − v5 | 50 | 358 | +0.3 [−2.3, +2.8] | +97 [−820, +1,003] |
| P-v5 | risk-aware | v6 − v5 | 50 | 358 | +0.6 [−3.0, +5.5] | +225 [−1,086, +1,984] |

## Disclosures (contract §8)

- **A price-taker:** every schedule is filled at the cleared price, with no effect on it.
- **Day-ahead only:** no intraday re-trading, balancing energy or ancillary services. These are a large share of German batteries' revenue in practice, so this measures only the day-ahead arbitrage value of the forecast, not a battery's total income.
- **No outages,** no imbalance and no forecast failure: the schedule is executed exactly.
- **Costs:** only those above. The wear cost and the exchange fee are stated assumptions; the grid-fee exemption is a legal assumption that may change.
- **Hourly, not quarter-hourly:** since 1 October 2025 the market clears in quarter-hours; the hourly price is their average, and a schedule flat within each hour settles exactly at it.
- **Post-selection:** v6 was selected on these days, so its result is optimistic for v6.
- **Simulated, not realized:** no money was traded.

## What it does not claim (contract §9)

- Not a trading recommendation, an investment case or a forecast of future profit.
- Not realized income.
- Not a property of v6 alone: the result depends on the battery, the costs and the rule stated here.
- Not 4.7T's result, and not a test of v6.

No annualized return, internal rate of return, payback or business case is reported: there is no capital cost model. Forecast error and interval coverage are not profit.
