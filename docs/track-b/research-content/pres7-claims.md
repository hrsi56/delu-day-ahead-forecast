# PRES-7: claim-to-evidence map

**2026-11-16 · PRES-7, Business insights with the profit chart, under PUBLISH_RULES 1.5 §5.1a and A8 (O46), the Owner's
decision 32 and the economic contract (`docs/track-b/economic-policy-contract-2026-11-15.md`, §§6, 8, 9).** PRES-7
renders CP-29's claims C1101–C1108 (`cp29-claims.md`) on the page and in the README, moving them from the claim layer's
`PRES7` surface, and adds the claims below. Values here are rounded from the saved values; the rendered surfaces bind
to the evidence records of `src/delu_forecast/research.py` (`cp29.*`), never to these digits. The chart's rules were
committed first (`docs/track-b/evidence/pres-7/publication-packet.md` §0).

**Evidence class of every claim:** simulated, development, post-selection. No money was traded; v6 was selected on these
same days (CP-28), so its result is optimistic for v6. Nothing here is prospective, live or 4.7T's.

## Source keys

| Key | File |
|---|---|
| DA29 | [reports/cp29/daily.csv](../../../reports/cp29/daily.csv): one row per day, source, rule and wear (the cumulative series) |
| SU29 | [reports/cp29/summary.csv](../../../reports/cp29/summary.csv): the contract's measures |
| CO29 | [docs/track-b/economic-policy-contract-2026-11-15.md](../economic-policy-contract-2026-11-15.md): the battery, the costs, the rules |
| PK7 | [docs/track-b/evidence/pres-7/publication-packet.md](../evidence/pres-7/publication-packet.md) §0: the chart's rules |

## Claims

| ID | Claim | Source | Class |
|---|---|---|---|
| C1201 | The profit chart: on P-all's 2,068 days at €25, the running sum of each day's net profit for v6 (median rule), the similar-day naive (median rule) and perfect foresight, ending at 257,212, 220,136 and 287,292 EUR; doing nothing is the zero line. | DA29 (wear 25); SU29 `cumulative_profit_eur`; PK7 §0 | S-d |
| C1202 | The untraded days on P-all at €25: v6's median-rule schedule traded on 1,770 of 2,068 days; 33 days had a forecast hour missing after a clock change (not traded, profit zero, kept); the naive's 11. | SU29 `trading_days`, `missing_days`; CO29 §5 | S-d |
| C1203 | The risk-aware variant (buy at the 75th percentile, sell at the 25th) for v6 on P-all at €25: 1,457 trading days, 39 losing days, largest daily loss 101 EUR, 247,436 EUR, 0.8613 of perfect foresight's. | SU29 (`rule` risk); CO29 §3 | S-d |
| C1204 | The assumptions: a price-taker (filled at the cleared price, moving none); no outage, imbalance or deviation from the schedule; the wear cost and the exchange fee are stated assumptions; the grid-fee exemption is a legal assumption that may change. | CO29 §§2, 8 | O |

C1103's wording on the page: "v6's profit minus the naive's, summed over the days, is +37,077 EUR [+32,323, +42,311]"
(CP-29's "earned +37,077 EUR more than the naive's" put a signed total inside "more"); the claim and its records are
unchanged.

## Withheld claims

| ID | Withheld | Why |
|---|---|---|
| W58 | A live, prospective or future profit, earnings, income or revenue with a number | The report shows no live or prospective profit (the brief's outcome 1); applying the policy to the live record is a separate round (contract §7) |

W54 is narrowed to its first half (O60): a forecast error, coverage or interval figure called a profit, a gain in money,
a return or a success rate. Its second half, which refused any "profit of <number>", is withdrawn: CP-29's simulated
profit, labelled with its class and limits, is now published. W56 and W57 stay.
