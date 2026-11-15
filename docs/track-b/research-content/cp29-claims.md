# CP-29: claim-to-evidence map

**2026-11-15 · CP-29, the economic evaluation under the Owner's approved contract (decision 32,
`docs/track-b/economic-policy-contract-2026-11-15.md`) and research v21-r20.** The claims written for PRES-7's Business
insights, which renders them; in this round they are on no published surface (the claim layer's `PRES7` surface). Each
is mapped to a committed file and the field it reads. Values here are rounded from the saved values; a rendered surface
binds to the evidence records of `src/delu_forecast/research.py` (`cp29.*`), never to these digits. The rules that
produced them were committed first (`docs/track-b/evidence/cp-29/publication-packet.md` §0).

**Evidence class of every claim:** simulated, development, post-selection. No money was traded; v6 was selected on these
same days (CP-28), so its result is optimistic for v6. Nothing here is prospective, live or 4.7T's.

## Source keys

| Key | File |
|---|---|
| SU29 | [reports/cp29/summary.csv](../../../reports/cp29/summary.csv): the contract's measures per population, scope, source, rule and wear |
| PA29 | [reports/cp29/paired.csv](../../../reports/cp29/paired.csv): the paired differences with their bootstrap intervals |
| DA29 | [reports/cp29/daily.csv](../../../reports/cp29/daily.csv): one row per day, source, rule and wear (the cumulative series) |
| CO29 | [docs/track-b/economic-policy-contract-2026-11-15.md](../economic-policy-contract-2026-11-15.md): the battery, the costs, the rule (decision 32; O58's clarifications in the packet) |
| PK29 | [docs/track-b/evidence/cp-29/publication-packet.md](../evidence/cp-29/publication-packet.md) §0: the rules fixed first |

## Claims

| ID | Claim | Source | Class |
|---|---|---|---|
| C1101 | The setup: a price-taking battery, 1 MW at the grid, 2 MWh usable, 85% round trip, at most one cycle a day, one direction an hour (O58); scheduled from the forecast before the 12:00 auction, settled at the cleared prices, net of €25 per MWh leaving the battery (O58) and €0.10 per MWh bought or sold. | CO29; PK29 §0 | Def |
| C1102 | On P-all's 2,068 days at €25: v6's median-rule schedule earns 257,212 EUR, 0.8953 of perfect foresight's 287,292 EUR; the naive's 220,136 EUR, 0.7662. | SU29 (`P-all`, `all`, wear 25) | S-d |
| C1103 | v6 − the naive, day by day on P-all at €25: +37,077 EUR [95% +32,323, +42,311], paired moving-block bootstrap, 14-day blocks, 2,000 replicates, seed 20261115. | PA29 | S-d |
| C1104 | On P-v5's 358 days at €25: v6 55,708 EUR, v5 55,544 EUR; v6 − v5 +165 EUR [−727, +1,032], an interval spanning zero. | SU29 (`P-v5`); PA29 | S-d |
| C1105 | Losses on P-all at €25: v6's schedule loses on 137 days, at most 97 EUR in a day, maximum drawdown 136 EUR; the naive's loses on 355 days, at most 227 EUR; perfect foresight never loses. | SU29 | S-d |
| C1106 | The wear sensitivity for v6 on P-all: €0, 356,333 EUR (0.9210 of perfect foresight's); €50, 176,202 EUR (0.8495). | SU29 (wear 0, 50) | S-d |
| C1107 | v6's share of perfect foresight's by regime at €25: before the crisis 0.6445 (246 days; perfect foresight earned 22.2 EUR a day on average), the crisis 0.8775 (481), from 2023 0.9118 (1,341). | SU29 (scopes) | S-d |
| C1108 | The limits: simulated, development, post-selection; day-ahead arbitrage only (no intraday, balancing or reserves); hourly; not a trading recommendation, not realized income, not a property of v6 alone, not 4.7T's result; no return or payback (no capital cost). | CO29 §§6, 8, 9 | O |

## Withheld claims

| ID | Withheld | Why |
|---|---|---|
| W56 | An annualized return, internal rate of return, payback or return on investment with a number | No capital cost model exists (contract §6) |
| W57 | A simulated profit called realized, actual or real income, profit, earnings or revenue | Simulated, not realized: no money was traded (contract §§8, 9) |
