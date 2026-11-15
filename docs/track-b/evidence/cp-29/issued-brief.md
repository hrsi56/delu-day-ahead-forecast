# Track B Checkpoint Brief — CP-29 (the economic evaluation: battery arbitrage on v6's development forecasts)

*Issued by the Orchestrator on 2026-11-15, Asia/Jerusalem, under the Owner's decisions 27, 28 and 32.*

## Target
- Repository: DE-LU day-ahead forecasting, `/Users/djourno/Downloads/PJM` (origin
  `hrsi56/delu-day-ahead-forecast`, public). The checkpoint runs locally, in the Lead's own worktree.
- Authorized checkpoint: CP-29, exactly one.
- **Beside it** runs CP-18d, the live product's round, in another Lead's own worktree. The two share no path.
- **What it does.** It runs the Owner's approved economic-policy contract exactly as written
  (`docs/track-b/economic-policy-contract-2026-11-15.md`, SHA-256 `21a9208573668becd2af3d9e476855e3f8c0e66c85fc9097194bd6deae580889`, decision 32): a price-taking
  1 MW / 2 MWh battery, scheduled the day before from each forecast and settled at the day-ahead clearing price, on
  development days only. It reports the profit of v6, the similar-day naive, v5 where it exists, and perfect
  foresight, under the contract's rule, costs and measures.
- **Why.** PRES-6's Business insights names the gap: no decision-policy evaluation exists (PUBLISH_RULES 1.5 §5.1a).
  The Owner chose battery arbitrage and approved the contract. PRES-7 then shows the result.
- **What follows it:** the Orchestrator's LAND; PRES-7, which publishes the profit chart in Business insights; 4.7T, no
  earlier than 2026-12-04, exactly as registered.
- Ratified plan anchor: `capstone_v21.md`, revision v21-r20, SHA-256 `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`.
  - **The bar** is quoted below: the contract in full (§§1–11); the anchor's §16.3 and §16.4; programme §4.E
    (`docs/track-b/v3-plan-handoff-2026-09-22.md`); PUBLISH_RULES 1.5 §5.1a; r20 §24.14's "What stays exactly as
    registered".
  - **PUBLISH_RULES** `docs/PUBLISH_RULES.md`, revision 1.5, SHA-256
    `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`.
- **The frozen policy, which this round reads and never changes:** CP-17c's freeze, policy identity
  `720fc581be6206eba8ed303e689e63c09272a189564090a547d93fc9e7db62dc`. v6 is A1 in the frozen records.
- **The Owner's decisions:** 1–19 bound by the frozen copies; 20–21 (`owner-decisions-2026-10-29.md`); 22–25
  (`owner-decisions-2026-10-30.md`); 26–27 (`progress.md`); 28 (`owner-decisions-2026-11-05.md`); 29–31
  (`owner-decisions-2026-11-15.md`); 32 (the contract's own header).
- **The Orchestrator's rulings that bind this round** (decision 27): O55 (the contract's choices, its §10) and O56
  (this round beside CP-18d).
- **Execution inputs.** Verify each hash before relying on it:

  | Input | Path | SHA-256 |
  |---|---|---|
  | The approved economic-policy contract (decision 32) | `docs/track-b/economic-policy-contract-2026-11-15.md` | `21a9208573668becd2af3d9e476855e3f8c0e66c85fc9097194bd6deae580889` |
  | CP-28's stored forecasts (v6 = arm A1) | `reports/cp28/forecast/hourly.parquet` | `f5cb02a19236edd20c182c2874a5d59628652e6838fe5745aa6ffacf3f53f638` |
  | CP-28's forecast manifest | `reports/cp28/forecast/manifest.json` | `f092140ed028d18a973bfad11ad9aa0397ad3e492223c4da683bc8e775cf3ce8` |
  | CP-28's daily losses | `reports/cp28/results/daily-losses.parquet` | `7e9c972f24a99627fd7e9ed8fc80ecffbf4b50be55426805d5b574a6ede9b85d` |
  | CP-24's committed predictions (v5) | `reports/ddnn2/attempt-1/predictions.parquet` | `9d3f539fa78e34e65cb495a0e79f8044731e33d5b2d9e95d110a1ce886a05cf9` |
  | The snapshot (cleared prices) | `data/snapshot.parquet` | `7dd2dc73407706ca6bd3c1ad51d201ac0de35eec5ca129ce320cca639f697f00` |
  | The naive's frozen rule | `src/delu_forecast/baselines.py` | `4e234cda6d09366b6136b2c2f4635dabdaa8aefe8d85ef0da41d9ad4912eea52` |
  | PRES-6's publication packet (P-all, P-v5, regimes, bootstrap) | `docs/track-b/evidence/pres-6/publication-packet.md` | `83468823cc363f24a2d3b3031308524e62b6f857a038518d3cb5033549716cb6` |
  | PRES-6's landing record | `docs/track-b/pres-6-landing-2026-11-15.md` | `415e2e7c89a47018546b91ac4bd46f40622440fdbc049b5b39b782196bbc198b` |
  | The locked environment | `uv.lock` | `5d2aecc3d173fef6191cb2bb9d14cd008c0e9cc764700f1352b81d1924465a94` |

## Orchestrator-reported expected state
- **Branch / commit:** `main` = `origin/main` at the commit that records this brief's issue, a descendant of the commit
  that adds the approved contract (`docs/track-b/economic-policy-contract-2026-11-15.md`). The issue commit changes only
  `progress.md`.
  - **`main` moves during this round.** The live product's daily runner pushes data-only commits to `main`, by the
    author `delu-daily`, touching only `live/`. The LAND assumes a moved `main`.
  - **CP-18d runs beside this round** (O56): its Lead works on `gauntlet/cp-18d` in `.local/worktrees/cp-18d/`, on the
    live product's paths only. The two rounds share no path. Never touch its worktrees or branch.
  - **Tags:** every landed checkpoint's `land/` and `evidence/` tags are pushed, except `evidence/cp-26` = `ca20331`,
    which is **local-only and never pushed**. The rulesets refuse moving or deleting a `land/`, `evidence/` or
    `archive/` tag, and refuse pushing a `gauntlet/*` branch.
- **Working tree:** the primary checkout is on `main` and clean apart from ignored material.
  - **The Orchestrator uses it.** Never switch its branch, and never write a tracked file in it. Your only writes
    there are under `.local/artifacts/cp-29/`, `.local/tmp/cp-29/` and the worktrees under `.local/worktrees/cp-29/`.
  - **The canonical brief** is `.local/artifacts/cp-29/issued-brief.md`. Package that file byte for byte.
- **What already exists for this round:**
  - CP-28's stored forecasts `reports/cp28/forecast/hourly.parquet` (seven arms; v6 = `A1`, 2,431 days from
    2020-01-01 to 2026-09-06, hourly `q025`–`q975`) and its daily losses `reports/cp28/results/daily-losses.parquet`;
  - CP-24's committed predictions `reports/ddnn2/attempt-1/predictions.parquet` (policies `v5`, `v3+D2`, `D2`; 10,747
    hours each over folds 1–5);
  - the snapshot `data/snapshot.parquet`, with every hour's cleared price `price_eur_mwh` (it also holds days after
    2026-09-06: never read them);
  - the naive's frozen rule `delu_forecast.baselines.SIMILAR_DAY_LAG_BY_WEEKDAY`;
  - PRES-6's populations and regimes (`docs/track-b/evidence/pres-6/publication-packet.md` §0) and its bootstrap
    settings;
  - scipy 1.18.1 in the locked environment.
- **Credentials:** none are needed.
- Verify this yourself before relying on it, and report any material mismatch.

## Observable outcome
When this checkpoint closes, after the Orchestrator's LAND, the repository holds the contract's evaluation as committed,
re-derivable records, ready for PRES-7 to show.

1. **The rules fixed before any number** (programme §4.E's engineering items). The packet's §0, committed before the
   first profit is computed, fixes:
   - the solver: `scipy.optimize.linprog` with HiGHS from the locked environment (scipy 1.18.1), its tolerances, and
     the contract's tie-break (among equal optima, the schedule that trades earliest and least), implemented
     deterministically and tested;
   - the exact linear programme: the variables, §2's limits (1 MW at the grid each way, 2 MWh usable, √0.85 on charge
     and on discharge, empty at the start and end of each day, at most 2 MWh discharged from the battery a day), the
     wear cost on energy discharged and the fees on energy bought and sold;
   - the day's hours on daylight-saving days (23 and 25), and the missing-hour rule (not traded, profit zero, counted);
   - the bootstrap's seed;
   - the joins: v6's `q25`, `q50` and `q75` from CP-28's stored forecasts (arm `A1`), v5's `p25`, `p50` and `p75` from
     CP-24's committed predictions, the naive's central vector by its frozen rule from the committed snapshot, and the
     cleared prices from the snapshot, each joined by delivery hour.
2. **The checks before the results:**
   - the naive's central vector equals CP-26's B0 central vector wherever a committed record holds it (parity); if
     none does, the packet says so and shows the rule's code path instead;
   - perfect foresight is never negative on a day, and the optimizer's schedule meets every limit on every day;
   - a brute-force check on a sample of days finds no better schedule than the solver's, within the tolerance;
   - the populations equal PRES-6's: P-all 2,068 days, P-v5 358 days.
3. **The results, exactly the contract's** (§§3, 4 and 6), on P-all and on P-v5:
   - for each source (v6, the naive, v5 on P-v5, perfect foresight) and each rule (the median rule; the risk-aware
     variant for v6 and v5): the daily profit series, the cumulative net profit in EUR, the share of perfect foresight
     captured, the daily distribution, the losing days and the largest daily loss, the maximum drawdown, the trading
     days and the energy cycled;
   - the wear-cost sensitivity: €0 and €50 beside the main €25, for every source and rule;
   - by regime, with counts;
   - the paired differences v6 − naive (P-all, P-v5) and v6 − v5 (P-v5), with 95% intervals from the moving-block
     bootstrap (14-day blocks, 2,000 replicates).
   Nothing else is computed: no other battery, rule, threshold or variant.
4. **The records.** Under `reports/cp29/`: the daily rows (one row per day, source, rule and wear cost: the schedule's
   energy, the profit, the forecast's own expected profit), the summaries, and a `--check` that re-derives every summary
   from the daily rows. Every row carries its evidence class: simulated, development, post-selection.
5. **The report** `reports/cp29/report.md`: the method, the results with their uncertainty, the disclosures and "what it
   does not claim" from the contract, in plain words, with no claim beyond them.
6. **The registry entries** PRES-7 needs: the claims for the business section, through the existing claim layer, with
   their evidence tag `evidence/cp-29`, and no page change in this round.

## Complete authoritative checkpoint bar
Verbatim, extracted by `scripts/bar.py bar … --at f118f2bb --quote` from `main` at the issue.
(The excerpt is the citation. Any line number is a courtesy and is non-binding.)

**The contract, "1. The use case"** (the file `21a9208573668becd2af3d9e476855e3f8c0e66c85fc9097194bd6deae580889`; the section 11 lines, 801 bytes, SHA-256 `e734d9f226ecf60fd27a0fe7eae46d42b866350d08e1a54788cf3b6488504765`):

> ## 1. The use case
>
> A battery owner uses the day-ahead forecast to plan tomorrow's charging and discharging, before the auction closes,
> and is paid or charged the day-ahead clearing price.
> - **The decision:** on D−1, from the forecast for D issued at D's cutoff (D−1 11:00 Europe/Berlin, v6's issue time),
>   fix D's hourly schedule of charging and discharging. The auction's gate closes at 12:00 on D−1.
> - **The settlement:** each hour's energy is bought or sold at that hour's cleared day-ahead price.
> - **The economic question:** how much of the value that a perfect forecast would earn does each forecast earn, net
>   of the stated costs?
> - **Descriptive economics** (programme decision D2): there is no pass mark, no required net surplus and no gate. The
>   result is reported whatever it is.

**The contract, "2. The battery"** (the file `21a9208573668becd2af3d9e476855e3f8c0e66c85fc9097194bd6deae580889`; the section 12 lines, 2439 bytes, SHA-256 `9252cafcaaad3c9a9d5395e3aa93e1eb1200966c771845ef602eae48ef369d39`):

> ## 2. The battery
>
> | Parameter | Value | Source or reason |
> |---|---|---|
> | Power | 1 MW, charging and discharging, measured at the grid | A unit size: every result scales with it. 1 MW keeps the battery a price-taker (§6) |
> | Usable energy | 2 MWh at the battery's terminals (a two-hour battery) | The common duration of German grid-scale batteries; a decision of the Owner's to confirm |
> | Round-trip efficiency | 85%, split evenly: √0.85 ≈ 92.2% on charge and on discharge | NREL Annual Technology Baseline 2025, utility-scale battery storage ([ATB 2025](https://atb.nlr.gov/electricity/2025/utility-scale_battery_storage)); the 2020 edition used the same value |
> | State of charge | between 0 and 2 MWh; empty at the start and at the end of each delivery day | Each day stands alone, so no state carries between days and a missing day cannot affect the next |
> | Cycles | at most one full cycle a day: at most 2 MWh discharged from the battery per day | Programme §4.E's cycle limit; conservative for battery wear |
> | Wear (degradation) cost | **€25 per MWh discharged** as the main value. Sensitivity, reported beside it and never chosen afterwards: €0 and €50 | **An assumption, not a measured cost:** amortizing about €150 per kWh of usable energy for replacement over about 6,000 full cycles (lithium iron phosphate) gives €25 per MWh of throughput. Both inputs are the Orchestrator's round figures. The amortization approach and its limits are discussed in [arXiv 2011.08425](https://arxiv.org/pdf/2011.08425.pdf). A decision of the Owner's to confirm |
> | Grid fees, levies and taxes | none | A new storage plant in Germany commissioned before 4 August 2029 is exempt from grid fees on the energy it draws and feeds back into the same grid for 20 years (§ 118 (6) EnWG; for example [Gleiss Lutz](https://www.gleisslutz.com/de/know-how/update-zu-den-netzentgelten-fuer-bess-bnetza-praesentiert-zwischenstand-zur-reform-der-netzentgeltsystematik-agnes) and [pv magazine, May 2026](https://www.pv-magazine.de/2026/05/28/netzentgeltbefreiung-fuer-batteriespeicher-bleibt-aber-das-fenster-schliesst-sich/)). The rules are under reform by the regulator (AgNes), so this is stated as an assumption |
> | Exchange and clearing fees | €0.10 per MWh bought and per MWh sold | **An assumption.** EPEX SPOT's member fee schedule was not found in a public source; the value is stated so that it is visible and can be changed |

**The contract, "3. The decision rule, fixed in advance"** (the file `21a9208573668becd2af3d9e476855e3f8c0e66c85fc9097194bd6deae580889`; the section 27 lines, 2036 bytes, SHA-256 `eb9b901bb1e72aea0552a9c96ecef2787c10936d41e946430e47b81b139eaab8`):

> ## 3. The decision rule, fixed in advance
>
> **The main rule (median).** For each delivery day D and each forecast source:
> 1. Take the source's hourly central forecast for D: the median `q50` (`p50`).
> 2. Choose the schedule that maximizes the forecast's net value: forecast price times energy sold, minus forecast
>    price times energy bought, minus the wear cost on energy discharged, minus the fees, under §2's limits. This is a
>    small linear programme over D's hours (23, 24 or 25 on daylight-saving days).
> 3. If the best schedule's forecast net value is not above zero, the battery does nothing on D.
> 4. Settle the chosen schedule at D's cleared prices, and charge the same wear cost and fees.
>
> Minimum spread over costs follows from step 3: the battery trades only when the forecast spread covers the
> efficiency loss, the wear and the fees.
>
> **One risk-aware variant (quantiles), named now and reported beside the main rule:** the same programme, but each hour's
> buying price is the forecast's 75th percentile (`q75`) and each hour's selling price its 25th percentile (`q25`). It
> trades only when the spread holds under these cautious prices.
> - It uses the quantiles one hour at a time, as cautious price bounds. Marginal quantiles are not a joint scenario
>   distribution (programme §4.E), and the variant does not treat them as one.
> - It applies only to sources whose hourly quantiles are committed: v6 and v5. The naive's hourly quantiles are not
>   committed (PRES-6's landing record), and perfect foresight has no variant.
>
> **Nothing else is tried.** No other rule, battery size, threshold or variant is computed, so none can be chosen after
> seeing results. A further variant would need a new approval.
>
> **Fixed by the research round before any number** (programme §4.E's engineering items, written into its packet first):
> the solver and its version, its tolerances, and a deterministic tie-break (among equal optima, the schedule that trades
> earliest and least); the treatment of a missing hour (§5); the bootstrap's seed.

**The contract, "4. The benchmarks"** (the file `21a9208573668becd2af3d9e476855e3f8c0e66c85fc9097194bd6deae580889`; the section 15 lines, 1156 bytes, SHA-256 `b13e3a886789475e7493c52a1d41ea933cfd6507a8b24a2d3d0a409a25067cac`):

> ## 4. The benchmarks
>
> Each is run with the identical battery, costs and rule (programme §4.E: "Match the PF benchmark to each identical
> decision specification").
>
> | Benchmark | Forecast | Population |
> |---|---|---|
> | **v6** (A1 in the frozen records; policy `720fc581…`) | CP-28's stored forecasts, `reports/cp28/forecast/hourly.parquet`, arm `A1`, `q50`, `q25` and `q75` | P-all and P-v5 (§5) |
> | **The similar-day naive** (B0) | the cleared price of the similar day by its frozen rule (D−1 on Tuesday to Friday, D−7 on Monday, Saturday and Sunday; `delu_forecast.baselines`), from the committed snapshot. Its central vector is checked against CP-26's B0 parity record before use | P-all and P-v5 |
> | **v5** | CP-24's committed predictions, `reports/ddnn2/attempt-1/predictions.parquet`, policy `v5`, `p50`, `p25` and `p75` | P-v5 only, the days where v5's forecasts exist |
> | **Perfect foresight** (the ceiling) | the cleared prices themselves | P-all and P-v5 |
> | **Doing nothing** | none | profit zero, for reference |
>
> The cleared prices are the committed snapshot's (`data/snapshot.parquet`, `price_eur_mwh`), which hold every hour of
> P-all.

**The contract, "5. The populations and the data"** (the file `21a9208573668becd2af3d9e476855e3f8c0e66c85fc9097194bd6deae580889`; the section 17 lines, 1418 bytes, SHA-256 `77f5884a46e002e7cb5b6d8bbbd17bc3de44f873511f81c5e1edc6c8554b713e`):

> ## 5. The populations and the data
>
> - **P-all:** every eligible development day, 2020-12-29 to 2026-09-06, 2,068 days: the days CP-26 scored and CP-28
>   selected on, as PRES-6 fixed them (`docs/track-b/evidence/pres-6/publication-packet.md` §0).
> - **P-v5:** the 358 days of P-all inside v5's test periods 2–5 (2021-04-01 to 2021-06-29, 2022-07-01 to 2022-09-28,
>   2025-05-01 to 2025-07-29, 2026-01-08 to 2026-04-07), where v5's forecasts exist.
> - **Regimes,** reported with their counts: PRES-6's material regimes (before the energy crisis; the crisis,
>   2021-09-01 to 2022-12-31; the market with frequent negative prices, from 2023-01-01).
> - **Development data only,** delivery days through 2026-09-06. No market value after that date is read. Every result is
>   labelled **simulated, development, post-selection**: v6 was selected on these same days (CP-28), so its result is
>   optimistic for v6.
> - **A missing hour:** a day with any forecast or price hour missing is not traded (profit zero) and is kept and
>   counted, never dropped.
> - **Quarter-hours:** since 1 October 2025 the day-ahead market clears in quarter-hours. The snapshot's hourly price is
>   their average, and a schedule that is flat within each hour is settled exactly at that average. The evaluation
>   does not use quarter-hour shapes, which a real battery could also trade (programme §4.E: hourly results do not
>   establish quarter-hour value).

**The contract, "6. The measures"** (the file `21a9208573668becd2af3d9e476855e3f8c0e66c85fc9097194bd6deae580889`; the section 18 lines, 1393 bytes, SHA-256 `3eba0aa669aff0700fd50aee9db1642d3a756d8a27a5c09ad039949e918e131c`):

> ## 6. The measures
>
> For each benchmark, population and rule:
> - **cumulative net profit** in EUR over the named period, as a complete daily time series, with the per-day units and
>   the battery's size beside it;
> - **the share of perfect foresight captured:** the sum of the benchmark's daily profits divided by the sum of perfect
>   foresight's, over the same days. Perfect foresight's daily profit is never negative (it can do nothing), so the
>   ratio is defined on sums only; a population with zero perfect-foresight profit reports "undefined";
> - **the daily profit distribution:** mean, median, 5th and 95th percentiles;
> - **losing days:** their number and share, and the largest single-day loss;
> - **the maximum drawdown** of the cumulative profit curve;
> - **trading days:** how many days the rule traded, and the energy cycled;
> - **paired uncertainty:** the daily profit difference v6 minus the naive (and v6 minus v5 on P-v5), with a 95%
>   interval from a non-circular moving-block bootstrap over days, blocks of 14 days, 2,000 replicates, the seed fixed
>   in the research round's packet before computing. These are the same settings as PRES-6's regime intervals.
>
> **Not reported:** no annualized return, internal rate of return, payback or business case, since there is no capital
> cost model; no "success rate". Forecast error and interval coverage are not profit (PUBLISH_RULES §5.1a).

**The contract, "7. The freeze, and later scoring"** (the file `21a9208573668becd2af3d9e476855e3f8c0e66c85fc9097194bd6deae580889`; the section 14 lines, 1151 bytes, SHA-256 `9b71aafd9177ac5340f8596714396ff08484ed832848d2c0b4a707d5907c845e`):

> ## 7. The freeze, and later scoring
>
> - **The freeze.** Once the Owner approves, this contract is frozen by its SHA-256 before 4.7T opens (no earlier than
>   2026-12-04). This meets §16.4's "freeze ... any evaluated economic policy before outcome access". A later change
>   needs a new approval and is dated as such.
> - **4.7T stays exactly as registered** (r20 §24.14). This contract adds no term, comparator, score or pass condition to
>   4.7T, and nothing here changes 4.7T's issuance, window, audit or calendar.
> - **After 4.7T is scored and its result published,** the frozen policy may be applied to 4.7T's own issued forecasts
>   and the window's cleared prices as a **separate, pre-registered secondary analysis**, labelled as such and never as
>   part of 4.7T's verdict. It reads 4.7T's records only after they are final, and changes none of them. It needs its
>   own brief.
> - **The live record.** The frozen policy may later be applied to the live product's issued forecasts, labelled
>   "simulated on the live record, prospective evaluation in progress", in a separate round. The report shows no live
>   number until the publication rules allow it.

**The contract, "8. Disclosures"** (the file `21a9208573668becd2af3d9e476855e3f8c0e66c85fc9097194bd6deae580889`; the section 12 lines, 785 bytes, SHA-256 `ebbe45e7e0928d1311a3cb339ac7d9cf46f11cb5358babde1db7346e80768772`):

> ## 8. Disclosures
>
> - **A price-taker:** every schedule is filled at the cleared price, with no effect on it.
> - **Day-ahead only:** no intraday re-trading, no balancing energy, and no ancillary services (frequency containment or
>   restoration reserves). In practice these are a large share of German batteries' revenue, so this measures only the
>   day-ahead arbitrage value of the forecast, not a battery's total income.
> - **No outages,** no imbalance and no forecast failure: the schedule is executed exactly.
> - **Costs:** only those in §2. The wear cost and the exchange fee are stated assumptions; the grid-fee exemption is a
>   legal assumption that may change.
> - **Hourly, not quarter-hourly** (§5).
> - **Post-selection** (§5).
> - **Simulated, not realized:** no money was traded.

**The contract, "9. What it does not claim"** (the file `21a9208573668becd2af3d9e476855e3f8c0e66c85fc9097194bd6deae580889`; the section 6 lines, 280 bytes, SHA-256 `3952659973529e51957f60db8236c4066db319961116ef024f8e74d134ad8620`):

> ## 9. What it does not claim
>
> - not a trading recommendation, an investment case or a forecast of future profit;
> - not realized income;
> - not a property of v6 alone: the result depends on the battery, the costs and the rule stated here;
> - not 4.7T's result, and not a test of v6.

**The contract, "10. Choices the Orchestrator made under decision 27 (for the Owner's after-the-fact review)"** (the file `21a9208573668becd2af3d9e476855e3f8c0e66c85fc9097194bd6deae580889`; the section 8 lines, 580 bytes, SHA-256 `88ff52ec9fc84534623727a009fb9535786aadc62f89ce4dedacdd55e34f01fd`):

> ## 10. Choices the Orchestrator made under decision 27 (for the Owner's after-the-fact review)
>
> 1. The rule: a daily linear programme on the median, empty at the start and end of each day, one cycle at most.
> 2. The risk-aware variant: buy at `q75`, sell at `q25`.
> 3. The efficiency, 85% (NREL ATB 2025), and the fee assumption, €0.10 per MWh.
> 4. The populations P-all and P-v5 and the regimes, reused from PRES-6.
> 5. The measures, the bootstrap settings, and "undefined" for a zero denominator.
> 6. The freeze before 4.7T, and later scoring only as separate, secondary analyses.

**The contract, "11. What the Owner approved (decision 32)"** (the file `21a9208573668becd2af3d9e476855e3f8c0e66c85fc9097194bd6deae580889`; the section 9 lines, 669 bytes, SHA-256 `c1cf0c3b19fa5527bf99ff0b79b2260198d64442b55c066a8fc444d4db00ea81`):

> ## 11. What the Owner approved (decision 32)
>
> 1. **The use case:** a price-taking battery in the day-ahead market (§1).
> 2. **The battery:** 1 MW / 2 MWh, 85% round trip, one cycle a day (§2).
> 3. **The wear cost:** €25 per MWh discharged, with €0 and €50 as sensitivity (§2).
> 4. **No grid fees** under the German exemption, and the €0.10 per MWh exchange fee (§2).
> 5. **The benchmarks:** the naive, v5 where it exists, and perfect foresight (§4).
> 6. **Then:** a research round runs this on development data only, under this frozen contract; a presentation round
>    (PRES-7) shows it in Business insights, labelled simulated, development and post-selection.

**`capstone_v21.md` v21-r20 §16.3** (the file `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`; the section 30 lines, 2368 bytes, SHA-256 `3bec66a22d7fc86f6dcde441c82328229f94e0d49efe28abf63965ada4568c0e`):

> ### 16.3 What the product and demo expose
>
> The product panel comes first, followed by How the product works, scientific Product results,
> Business insights, How the models compare and all remaining sections in their existing order.
> [PUBLISH_RULES 1.1](docs/PUBLISH_RULES.md) §§5, 5.1a, 7.2 and A8 define presentation acceptance.
> The twelve-subject product coverage follows the actual final policy and its dated artifacts;
> the outgoing product's evidence stays historical. The primary demo uses the same product policy,
> and identifies the artifact/issue date and whether an interaction is a counterfactual scenario.
> An old replay may remain as labelled history, not as a different primary product.
>
> Show today's issued hourly forecasts versus available published outcomes, a defined percentage
> performance measure alongside MAE in EUR/MWh, and tomorrow's issued hourly forecasts and prediction
> intervals. Freeze the percentage formula, denominator, eligible population, scoring window,
> zero/negative-price treatment and any success tolerance before evaluation. A benchmark-relative
> percentage is labelled improvement, not correctness. Missing/pending outcomes are unscored;
> partial-day scores show completeness. Scoring uses the artifact that issued the prediction,
> not a newer fit. Record the price source, publication/revision times and outcome eligibility.
>
> Distinguish nominal prediction-interval level from measured coverage and width on an explicitly
> named past window. Neither means a point price has that percentage probability of being correct.
> Display separate last-training, data-refresh and issuance times, delivery date/timezone,
> freshness and failure state. No data or no evidence means a labelled unavailable state.
>
> Scientific graphics separate development, unused-data and prospective results. Business
> interpretation must separate forecast performance from an evaluated economic decision policy.
> Cumulative net profit/value, returns or business success rates require a frozen use case,
> constraints, costs, benchmark, denominator, complete time series and loss/risk disclosure;
> label simulated versus realized results. Without authorized evaluation, show the specific gap
> and measured forecasting implications. This is no authorization for trading, a new economic
> experiment or a fabricated profitable result; programme §4.E governs such evaluation.

**`capstone_v21.md` v21-r20 §16.4** (the file `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`; the section 19 lines, 1777 bytes, SHA-256 `502c1a588c9fe88e557084cff3fe1c44871c8e0c8fbe42a2284650d3a98a73ab`):

> ### 16.4 Delivery and acceptance obligations for future briefs
>
> | Stage | Required addition to the full future checkpoint bar |
> |---|---|
> | Before fresh-data test | Replay the intended daily refit/update and issuance contract; freeze scoring and any evaluated economic policy before outcome access; retain the protected test boundary |
> | CP-17 | Owner's final-version designation, prerequisites/disposition, policy/initialization and registry identities, daily fit and failure rules, metric formulas, resource and calendar plan |
> | CP-18 | Actual scheduled training/issuance and outcome reconciliation, one product/demo identity, complete documentation/results/business sections, daily public panel and independent public acceptance |
> | CP-19 | At least 90 consecutive delivery days after final freeze under §9; count real timely forecasts and failures, verify registry lineage, evaluate without tuning or excluding bad days |
>
> Live observations and the matching demo may be published at authorized CP-18 with the label
> “prospective evaluation in progress”; do not wait for CP-19 to show operation, and do not claim
> completed validation before it. Public acceptance checks actual hosted output and daily records;
> local fixtures do not establish daily operation. Include positive controls for altered identities,
> future-label leakage, stale/failed fits, missing/zero/negative prices and partial/DST days, plus
> reproducible percentage, interval and authorized business-series derivations. The full existing
> independent, browser, accessibility and publication contract still applies.
>
> No checkpoint starts here. The numeric future briefs and approved budgets remain necessary;
> this amendment resolves the required product outcome, not experimental results or implementation.

**Programme §4.E** (the file `ae77db3cf98bcebfed71e8a1ff8f97440351494eef66bf1cd7ac006e7f651f98`; the section 17 lines, 1148 bytes, SHA-256 `a530a82e2d874f4b7a4c8616ad32c661d06d6b9be2160d9297b5e2b195095723`):

> ### 4.E Economic policy contract
>
> [D1](#decision-d1)–[D3](#decision-d3) retain ownership of exposure, market resolution, external economic rationale and required
> net surplus; descriptive economics remains a valid choice. The future brief must specify the
> forecast functional/objective (conditional mean, median proxy or explicit risk objective),
> cashflow direction, settlement cadence, bids/fills/imbalance assumptions, physical constraints,
> efficiency, initial/terminal SOC, cycles, fees/degradation and other costs. Engineering must
> freeze deterministic optimization tie-breaking, solver/version/tolerances, missing-input and
> failed-issuance execution, aggregation/denominators (including zero/nonpositive perfect-foresight
> value), paired uncertainty and fallback. No values are chosen here.
>
> Hourly complete-day diagnostics in §5.6 do not establish quarter-hour, outage-inclusive
> product value. Marginal quantiles are not a joint scenario distribution for intertemporal
> risk optimization. Match the PF benchmark to each identical decision specification. No new
> trading implementation is commissioned by this contract.
>
> <a id="work-4-9o"></a>

**`docs/PUBLISH_RULES.md` revision 1.5 §5.1a** (the file `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`; the section 19 lines, 1543 bytes, SHA-256 `51b54d5baf606a796386a99bd5d089df7ec976f92e89fdedc16d66163eab5eea`):

> ### 5.1a Final-product results and business interpretation (A8)
>
> **Product results**, directly after How the product works, presents the selected product's
> forecast-versus-observed charts, error over time and by material regimes, explanation/sensitivity
> results, and interval coverage together with width. Each graphic names the policy/artifact,
> population, dates, units and evidence class. Historical development, unused-data evaluation and
> prospective issued forecasts are visibly separate. Use the §5.1 coverage map across these
> adjacent sections; do not transplant another model's evidence or duplicate every topic.
>
> **Business insights**, directly after Product results, explains the intended use, measured
> benefit, losses and limits. Where a decision-policy evaluation exists, show cumulative net
> profit/value over the full named period, against the declared benchmark, with units, costs,
> constraints, initial conditions and risk/loss context. Label simulated/backtested results versus
> realized operation; preserve failed and missing days and disclose capital/denominators for
> returns. Forecast error reduction and interval coverage are not profit or trade-success rates.
> Business success percentages name the decision, formula, denominator and evaluation window.
> If this evaluation is not yet authorized or available, retain the section with the specific
> gap and measured forecasting implications; do not manufacture a profit curve or imply gains.
> Economic modelling stays governed by the research/use-case protocol (programme §4.E).

**`capstone_v21.md` v21-r20 §24.14, "What stays exactly as registered"** (the file `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`; the section 16 lines, 1161 bytes, SHA-256 `0e1f357969f5bad69b4e5dbc4682631196a77b4580381b6ef887cb96b7607c84`):

> #### What stays exactly as registered
>
> - **A1's freeze.** CP-17c's policy identity `720fc581be6206eba8ed303e689e63c09272a189564090a547d93fc9e7db62dc`,
>   its manifest and the frozen package stay unchanged. `refreeze verify` guards them, and the live pipeline
>   calls the package without editing it.
> - **4.7T, in every registered term** (§24.12, §24.13):
>   - the window, delivery days 2026-09-07 to 2026-12-05;
>   - the candidate, the comparators, the scores, the pass conditions, the margins and the failure rules;
>   - the vintage terms (the protocol's §3);
>   - the machine (the Owner's Mac, no cloud) and the H2 checks before its first issuance;
>   - the calendar: it opens no earlier than 2026-12-04, after the price for 2026-12-05 is published;
>   - the audit, the Owner's declaration and his retrieval approval.
> - **4.7T issues its window itself.** Its issuance starts from the freeze-origin state, runs on the Owner's Mac
>   under its terms, and keeps its own store. Nothing the live product issues is 4.7T's issuance or score.
> - **No registered term changes from here until 4.7T is scored.** A proposal to change one returns 4.7T to the
>   Owner as BLOCKED.

**Further items,** which bind this candidate as well:

1. **4.7T stays exactly as registered** (§24.14). Nothing here adds a term to 4.7T, reads 4.7T's records, or uses any
   market value after 2026-09-06.
2. **The red line.** Development data only, delivery days through 2026-09-06. The boundary guard stays on every path of
   this round.
3. **No fit.** Every forecast is a committed, stored one. Nothing frozen changes.
4. **The contract is the authority.** If it is unclear, ask the Orchestrator; never resolve it by looking at results.
5. **Critic and return:** `docs/track-b/gauntlet-templates.md` §§2–3.

Map every applicable item to evidence. The extract below does not narrow this bar.

## Task-specific supporting extract
- **The live product runs every day during this round,** from `main`, on the runner, and CP-18d changes it on its own
  branch. Never touch `src/cp18/`, `live/`, `space-product/`, `.github/`, or CP-18d's worktrees.
- **The ceilings:** 4 local machine-hours, summed over workers' wall time, at most 4 concurrent workers, CPU only. Keep
  a ledger, and stop before a ceiling.

## Applicable constraints
- **Homebrew's `node` stays pinned and installed.**
- **Credentials:** none are needed. Never print, log or echo a credential value. Export `MLFLOW_DISABLE_TELEMETRY=true`
  and `DO_NOT_TRACK=1`.
- **Allowed paths:** `src/cp29/`, `tests/cp29/`, `reports/cp29/`, `docs/track-b/evidence/cp-29/`, and the registry and
  claim layer's entries for CP-29 (`src/delu_forecast/registry.py`, `src/delu_forecast/research_claims.py`), with their
  tests. No anchor, governance file, `docs/PUBLISH_RULES.md`, `progress.md`, the contract, `uv.lock`,
  `pyproject.toml`, frozen record, the report (`docs/index.html`, `README.md`) or live-product path.
- **Before editing a tracked file,** check that no earlier evidence binds its bytes. That includes
  `src/cp26/harness.py`'s `PINS`, `tests/pres5_landed_code.py` and every freeze manifest's governance pins.
- **Tools:**
  1. run `scripts/gauntlet.py start cp-29` first, from the primary checkout;
  2. create the worktree with
     `git -C /Users/djourno/Downloads/PJM worktree add -b gauntlet/cp-29 .local/worktrees/cp-29/lead main`;
  3. run the independent check through `critic-open`, `critic-brief` and `critic-close`. **The first line of the
     Critic's launch assignment** forbids opening the Claude memory directory;
  4. check the return with `scripts/gauntlet.py return`.
- **Memory:** do not open or edit the files in the Claude memory directory
  (`~/.claude/projects/-Users-djourno-Downloads-PJM/memory/`).
- **Owner-facing Git commands** must be non-interactive.

## Timebox
About 10 active hours from orientation to the terminal return.

## Owner-only actions already authorized
- **CP-29's execution** under decisions 27, 28 and 32 and this brief, on `gauntlet/cp-29`. The Orchestrator delivers
  this brief under the Owner's grant, and that delivery is the grant.
- **No external action.** No push, landing, merge or tag on `origin`, no MLflow write, no Space upload, no Pages
  deployment and no governance edit. Those that apply are the Orchestrator's, after the return.

## Stop and return
- **First commit.** The first commit copies the canonical brief byte for byte to
  `docs/track-b/evidence/cp-29/issued-brief.md`.
- **Questions.** If the brief is unclear or wrong, ask the Orchestrator, or stop at the conflict. The anchor, the
  Owner's decisions, the contract and PUBLISH_RULES prevail over this brief.
- **The return.** Return exactly one of PASS / BLOCKED / INCOMPLETE, using templates §3, with both terminal SHAs and
  the verdict-only delta, checked with `scripts/gauntlet.py return`.
  - Its "Open risk or exact owner action" section gives the LAND's commands and every open item, with a proposed
    ruling for each.
  - Name the machine-hours used.
- Leave your worktree and branch for the LAND.
