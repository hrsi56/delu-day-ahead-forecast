# Economic-policy contract — battery arbitrage in the day-ahead market (2026-11-15)

**Status: approved by the Owner on 2026-11-15 (decision 32), and frozen by its SHA-256 in the brief of the research
round that runs it, before 4.7T opens.** Nothing in it was computed before the approval. Any change needs a new
approval, dated as such.

**Decision 32, in the Owner's words** (after reading the draft and the Orchestrator's Hebrew summary of it):

> שלח סיכום ליישום ארביטראז' סוללה. ואז ביצוע של כל מה שצריך, ואז PRES-7 שמציג את גרף הרווח.

In English: "Send a summary for implementing battery arbitrage. Then carry out everything that is needed, and then
PRES-7, which shows the profit chart." The Orchestrator reads it as approval of the draft as written; the Owner
changed nothing in it.

**What it is for.** It answers the gap that Business insights names: no decision-policy evaluation exists yet
(PUBLISH_RULES 1.5 §5.1a and A8). The anchor requires the Owner's authorization and a complete economic-policy
contract before any economic run (`capstone_v21.md` §16.3, and the rule "A material change to this approved economic
scope requires Owner authorization and a complete economic-policy contract before execution; do not insert a battery
configuration as an unapproved default"). The contract's required elements are programme §4.E's
(`docs/track-b/v3-plan-handoff-2026-09-22.md` §4.E).

**The Owner's choice (2026-11-15):** battery arbitrage in the DE-LU day-ahead market. He set aside the day-ahead and
intraday spread: it needs intraday prices, a new and paid source, and v6 forecasts the day-ahead price only.

## 1. The use case

A battery owner uses the day-ahead forecast to plan tomorrow's charging and discharging, before the auction closes,
and is paid or charged the day-ahead clearing price.
- **The decision:** on D−1, from the forecast for D issued at D's cutoff (D−1 11:00 Europe/Berlin, v6's issue time),
  fix D's hourly schedule of charging and discharging. The auction's gate closes at 12:00 on D−1.
- **The settlement:** each hour's energy is bought or sold at that hour's cleared day-ahead price.
- **The economic question:** how much of the value that a perfect forecast would earn does each forecast earn, net
  of the stated costs?
- **Descriptive economics** (programme decision D2): there is no pass mark, no required net surplus and no gate. The
  result is reported whatever it is.

## 2. The battery

| Parameter | Value | Source or reason |
|---|---|---|
| Power | 1 MW, charging and discharging, measured at the grid | A unit size: every result scales with it. 1 MW keeps the battery a price-taker (§6) |
| Usable energy | 2 MWh at the battery's terminals (a two-hour battery) | The common duration of German grid-scale batteries; a decision of the Owner's to confirm |
| Round-trip efficiency | 85%, split evenly: √0.85 ≈ 92.2% on charge and on discharge | NREL Annual Technology Baseline 2025, utility-scale battery storage ([ATB 2025](https://atb.nlr.gov/electricity/2025/utility-scale_battery_storage)); the 2020 edition used the same value |
| State of charge | between 0 and 2 MWh; empty at the start and at the end of each delivery day | Each day stands alone, so no state carries between days and a missing day cannot affect the next |
| Cycles | at most one full cycle a day: at most 2 MWh discharged from the battery per day | Programme §4.E's cycle limit; conservative for battery wear |
| Wear (degradation) cost | **€25 per MWh discharged** as the main value. Sensitivity, reported beside it and never chosen afterwards: €0 and €50 | **An assumption, not a measured cost:** amortizing about €150 per kWh of usable energy for replacement over about 6,000 full cycles (lithium iron phosphate) gives €25 per MWh of throughput. Both inputs are the Orchestrator's round figures. The amortization approach and its limits are discussed in [arXiv 2011.08425](https://arxiv.org/pdf/2011.08425.pdf). A decision of the Owner's to confirm |
| Grid fees, levies and taxes | none | A new storage plant in Germany commissioned before 4 August 2029 is exempt from grid fees on the energy it draws and feeds back into the same grid for 20 years (§ 118 (6) EnWG; for example [Gleiss Lutz](https://www.gleisslutz.com/de/know-how/update-zu-den-netzentgelten-fuer-bess-bnetza-praesentiert-zwischenstand-zur-reform-der-netzentgeltsystematik-agnes) and [pv magazine, May 2026](https://www.pv-magazine.de/2026/05/28/netzentgeltbefreiung-fuer-batteriespeicher-bleibt-aber-das-fenster-schliesst-sich/)). The rules are under reform by the regulator (AgNes), so this is stated as an assumption |
| Exchange and clearing fees | €0.10 per MWh bought and per MWh sold | **An assumption.** EPEX SPOT's member fee schedule was not found in a public source; the value is stated so that it is visible and can be changed |

## 3. The decision rule, fixed in advance

**The main rule (median).** For each delivery day D and each forecast source:
1. Take the source's hourly central forecast for D: the median `q50` (`p50`).
2. Choose the schedule that maximizes the forecast's net value: forecast price times energy sold, minus forecast
   price times energy bought, minus the wear cost on energy discharged, minus the fees, under §2's limits. This is a
   small linear programme over D's hours (23, 24 or 25 on daylight-saving days).
3. If the best schedule's forecast net value is not above zero, the battery does nothing on D.
4. Settle the chosen schedule at D's cleared prices, and charge the same wear cost and fees.

Minimum spread over costs follows from step 3: the battery trades only when the forecast spread covers the
efficiency loss, the wear and the fees.

**One risk-aware variant (quantiles), named now and reported beside the main rule:** the same programme, but each hour's
buying price is the forecast's 75th percentile (`q75`) and each hour's selling price its 25th percentile (`q25`). It
trades only when the spread holds under these cautious prices.
- It uses the quantiles one hour at a time, as cautious price bounds. Marginal quantiles are not a joint scenario
  distribution (programme §4.E), and the variant does not treat them as one.
- It applies only to sources whose hourly quantiles are committed: v6 and v5. The naive's hourly quantiles are not
  committed (PRES-6's landing record), and perfect foresight has no variant.

**Nothing else is tried.** No other rule, battery size, threshold or variant is computed, so none can be chosen after
seeing results. A further variant would need a new approval.

**Fixed by the research round before any number** (programme §4.E's engineering items, written into its packet first):
the solver and its version, its tolerances, and a deterministic tie-break (among equal optima, the schedule that trades
earliest and least); the treatment of a missing hour (§5); the bootstrap's seed.

## 4. The benchmarks

Each is run with the identical battery, costs and rule (programme §4.E: "Match the PF benchmark to each identical
decision specification").

| Benchmark | Forecast | Population |
|---|---|---|
| **v6** (A1 in the frozen records; policy `720fc581…`) | CP-28's stored forecasts, `reports/cp28/forecast/hourly.parquet`, arm `A1`, `q50`, `q25` and `q75` | P-all and P-v5 (§5) |
| **The similar-day naive** (B0) | the cleared price of the similar day by its frozen rule (D−1 on Tuesday to Friday, D−7 on Monday, Saturday and Sunday; `delu_forecast.baselines`), from the committed snapshot. Its central vector is checked against CP-26's B0 parity record before use | P-all and P-v5 |
| **v5** | CP-24's committed predictions, `reports/ddnn2/attempt-1/predictions.parquet`, policy `v5`, `p50`, `p25` and `p75` | P-v5 only, the days where v5's forecasts exist |
| **Perfect foresight** (the ceiling) | the cleared prices themselves | P-all and P-v5 |
| **Doing nothing** | none | profit zero, for reference |

The cleared prices are the committed snapshot's (`data/snapshot.parquet`, `price_eur_mwh`), which hold every hour of
P-all.

## 5. The populations and the data

- **P-all:** every eligible development day, 2020-12-29 to 2026-09-06, 2,068 days: the days CP-26 scored and CP-28
  selected on, as PRES-6 fixed them (`docs/track-b/evidence/pres-6/publication-packet.md` §0).
- **P-v5:** the 358 days of P-all inside v5's test periods 2–5 (2021-04-01 to 2021-06-29, 2022-07-01 to 2022-09-28,
  2025-05-01 to 2025-07-29, 2026-01-08 to 2026-04-07), where v5's forecasts exist.
- **Regimes,** reported with their counts: PRES-6's material regimes (before the energy crisis; the crisis,
  2021-09-01 to 2022-12-31; the market with frequent negative prices, from 2023-01-01).
- **Development data only,** delivery days through 2026-09-06. No market value after that date is read. Every result is
  labelled **simulated, development, post-selection**: v6 was selected on these same days (CP-28), so its result is
  optimistic for v6.
- **A missing hour:** a day with any forecast or price hour missing is not traded (profit zero) and is kept and
  counted, never dropped.
- **Quarter-hours:** since 1 October 2025 the day-ahead market clears in quarter-hours. The snapshot's hourly price is
  their average, and a schedule that is flat within each hour is settled exactly at that average. The evaluation
  does not use quarter-hour shapes, which a real battery could also trade (programme §4.E: hourly results do not
  establish quarter-hour value).

## 6. The measures

For each benchmark, population and rule:
- **cumulative net profit** in EUR over the named period, as a complete daily time series, with the per-day units and
  the battery's size beside it;
- **the share of perfect foresight captured:** the sum of the benchmark's daily profits divided by the sum of perfect
  foresight's, over the same days. Perfect foresight's daily profit is never negative (it can do nothing), so the
  ratio is defined on sums only; a population with zero perfect-foresight profit reports "undefined";
- **the daily profit distribution:** mean, median, 5th and 95th percentiles;
- **losing days:** their number and share, and the largest single-day loss;
- **the maximum drawdown** of the cumulative profit curve;
- **trading days:** how many days the rule traded, and the energy cycled;
- **paired uncertainty:** the daily profit difference v6 minus the naive (and v6 minus v5 on P-v5), with a 95%
  interval from a non-circular moving-block bootstrap over days, blocks of 14 days, 2,000 replicates, the seed fixed
  in the research round's packet before computing. These are the same settings as PRES-6's regime intervals.

**Not reported:** no annualized return, internal rate of return, payback or business case, since there is no capital
cost model; no "success rate". Forecast error and interval coverage are not profit (PUBLISH_RULES §5.1a).

## 7. The freeze, and later scoring

- **The freeze.** Once the Owner approves, this contract is frozen by its SHA-256 before 4.7T opens (no earlier than
  2026-12-04). This meets §16.4's "freeze ... any evaluated economic policy before outcome access". A later change
  needs a new approval and is dated as such.
- **4.7T stays exactly as registered** (r20 §24.14). This contract adds no term, comparator, score or pass condition to
  4.7T, and nothing here changes 4.7T's issuance, window, audit or calendar.
- **After 4.7T is scored and its result published,** the frozen policy may be applied to 4.7T's own issued forecasts
  and the window's cleared prices as a **separate, pre-registered secondary analysis**, labelled as such and never as
  part of 4.7T's verdict. It reads 4.7T's records only after they are final, and changes none of them. It needs its
  own brief.
- **The live record.** The frozen policy may later be applied to the live product's issued forecasts, labelled
  "simulated on the live record, prospective evaluation in progress", in a separate round. The report shows no live
  number until the publication rules allow it.

## 8. Disclosures

- **A price-taker:** every schedule is filled at the cleared price, with no effect on it.
- **Day-ahead only:** no intraday re-trading, no balancing energy, and no ancillary services (frequency containment or
  restoration reserves). In practice these are a large share of German batteries' revenue, so this measures only the
  day-ahead arbitrage value of the forecast, not a battery's total income.
- **No outages,** no imbalance and no forecast failure: the schedule is executed exactly.
- **Costs:** only those in §2. The wear cost and the exchange fee are stated assumptions; the grid-fee exemption is a
  legal assumption that may change.
- **Hourly, not quarter-hourly** (§5).
- **Post-selection** (§5).
- **Simulated, not realized:** no money was traded.

## 9. What it does not claim

- not a trading recommendation, an investment case or a forecast of future profit;
- not realized income;
- not a property of v6 alone: the result depends on the battery, the costs and the rule stated here;
- not 4.7T's result, and not a test of v6.

## 10. Choices the Orchestrator made under decision 27 (for the Owner's after-the-fact review)

1. The rule: a daily linear programme on the median, empty at the start and end of each day, one cycle at most.
2. The risk-aware variant: buy at `q75`, sell at `q25`.
3. The efficiency, 85% (NREL ATB 2025), and the fee assumption, €0.10 per MWh.
4. The populations P-all and P-v5 and the regimes, reused from PRES-6.
5. The measures, the bootstrap settings, and "undefined" for a zero denominator.
6. The freeze before 4.7T, and later scoring only as separate, secondary analyses.

## 11. What the Owner approved (decision 32)

1. **The use case:** a price-taking battery in the day-ahead market (§1).
2. **The battery:** 1 MW / 2 MWh, 85% round trip, one cycle a day (§2).
3. **The wear cost:** €25 per MWh discharged, with €0 and €50 as sensitivity (§2).
4. **No grid fees** under the German exemption, and the €0.10 per MWh exchange fee (§2).
5. **The benchmarks:** the naive, v5 where it exists, and perfect foresight (§4).
6. **Then:** a research round runs this on development data only, under this frozen contract; a presentation round
   (PRES-7) shows it in Business insights, labelled simulated, development and post-selection.
