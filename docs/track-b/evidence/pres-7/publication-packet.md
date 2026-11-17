# PRES-7 publication packet

**PUBLISH_RULES 1.5 §§5.1a, 6 and A8 (O46), with decision 30 superseding §5.2's page budget; the brief
`docs/track-b/evidence/pres-7/issued-brief.md` (SHA-256 `b6a45b60…1175`); the packet template
`docs/track-b/publication-packet-template.md` (`4049c3e1…d01a`); the economic contract
`docs/track-b/economic-policy-contract-2026-11-15.md` (`21a92085…0889`), §§6, 8 and 9.** This section, §0, was
committed before the profit chart was drawn or any of PRES-7's text was written; the rest of the packet follows the
template once the build exists.

## The Orchestrator's rulings in this round (decision 27), beside the brief

- **O60 (in the assignment, 2026-11-16):** W54 narrows to its "error or coverage called a profit" half; W56 and W57 stay
  (CP-29's open item 4).
- **O63 (2026-11-16, after this packet's §0 was committed; it governs no chart rule):** PRES-7 may make exactly one
  edit in `tests/cp29/`. `test_claims.py::test_the_blocks_are_written_for_pres7_and_appear_on_no_published_surface`, a
  test scoped to CP-29's own round, becomes its PRES-7 successor: every CP-29 block renders on the page and in the
  README through the claim layer and binds its `cp29.*` records, with a negative control (an altered number or record
  fails). Every other file in `tests/cp29/`, `src/cp29/` and `reports/cp29/` stays byte-identical. The pin check comes
  first: no evidence binds `test_claims.py`'s bytes (CP-29's evidence cites the test by name only). The edit and the
  check are recorded in §10.1.
- **Decision 30 (the Owner, 2026-11-15):** no page-size limit; `docs/PUBLISH_RULES.md` is not edited (CP-26's harness
  pins its bytes).

## §0. Rules fixed before the chart is drawn

PRES-7 computes nothing new. It renders CP-29's committed rows (`evidence/cp-29`), and every number it shows is either
an evidence record of `src/delu_forecast/research.py` (`cp29.*`) or derived, in the build, from `reports/cp29/daily.csv`
by the rules below. Nothing is fitted, re-solved or chosen after seeing a curve.

**The source.** `reports/cp29/daily.csv` (SHA-256 `bf39cc7b…7ae3`, blob `c0a8794b…acab`, registered under
`evidence/cp-29`). The build checks its blob (`research.check_source`) before reading a row, and stops if it changed.

**The rows drawn.** Wear cost €25 per MWh, the contract's main setting; population P-all, every eligible development
day from 2020-12-29 to 2026-09-06 (2,068 days, one row per day and source); three lines:
- v6 (A1 in the frozen records, CP-28's stored forecasts), the median rule;
- the similar-day naive, the median rule (the benchmark the contract declares);
- perfect foresight (the cleared prices themselves: the ceiling).
The risk-aware variant, v5 (P-v5 only) and the wear costs €0 and €50 are not drawn: they are stated in the text beside
the chart, from their records.

**The series.** For each line, the running sum of `profit_eur` in calendar-day order, the value on a day including that
day. A day that was not traded, whether by choice (no cycle was expected to pay its costs) or because an hour was
missing (contract §5), contributes its committed zero and stays in the series: no day is dropped or filled.

**Doing nothing.** The contract's zero reference is drawn as a horizontal line at 0 EUR, labelled "doing nothing" on
the chart. It is a reference, not a benchmark row: its profit is zero on every day by definition.

**The check before drawing.** Each line's last value must equal its record
`cp29.p_all.all.<source>.<rule>.w25.cumulative_profit_eur` within a relative tolerance of 1e-9, and its number of days
must equal the record's `days` (2,068). The summation order may differ from CP-29's, so the last bits may differ; the
build compares with that stated tolerance, never bytes, and stops on a larger difference.

**The axes.**
- **x:** the calendar date, linear in time, from the first to the last day of P-all; tick labels at each 1 January
  (every year on desktop; on a phone, odd years only, as PRES-6's monthly chart does).
- **y:** cumulative net profit in thousand EUR, for one 1 MW / 2 MWh battery. From the lower of 0 and the lowest point
  of any line, to the first multiple of the tick step at or above perfect foresight's last value; the step from the
  build's existing `_nice_step` rule over that span (four to five ticks). Gridlines at the ticks.

**Thinning for drawing.** A line of 2,068 points is drawn with at most four points per horizontal pixel column of the
plot: in date order, each column's first point, its lowest, its highest and its last. No dip or peak is lost, and the
first and last days are always drawn exactly. The thinning changes no value; the end label and the check use the full
series.

**Labels.** No meaning depends on colour alone: each line carries its name at its right end ("perfect foresight",
"v6", "naive"), with a distinct style (perfect foresight thin and dashed, v6 thick and solid in v6's token, the naive
dashed in the reference token, as Product results draws v6 and the naive). Each line's total is printed in a key below
the chart, bound to its record.

**The identity the graphic carries** (§5.1a): the battery and its costs (C1101); the policy and artifact (v6, A1 in the
frozen records, policy `720fc581…`, CP-28's stored forecasts; the naive's frozen rule; the cleared prices); the
population with its dates (P-all, 2,068 days, 2020-12-29 to 2026-09-06); the units (EUR, cumulative, for one 1 MW /
2 MWh battery); and the evidence class, **simulated, development, post-selection**. In the chart's title and
description and in the line directly above it.

**The text.** CP-29's claims C1101–C1108 render beside the chart through the claim layer, unchanged in meaning; two new
claims add the risk-aware variant (contract §3) and the untraded days (contract §§5–6; CP-29's open item 3), each bound
to `cp29.*` records. `business.gap` is replaced by what is still not evaluated (intraday, reserves, a real battery's
costs, the live record). Nothing prospective, live or 4.7T's is shown.

**The phone axis (O51 item 7).** The live comparison's axis widens to start at 0.4, as PRES-5's comment in
`overview_panels` already states; the condition that should have applied it tests `order` after it has been
reassigned, so it never does. Fixing the condition is the change; the comparison's rows and values do not change, and
every pinned comparison (published in MLflow) keeps its own axis.

**The wording pass (O51 item 8).** No number changes. Checked by extracting every rendered number from the page before
and after the pass, outside the sections PRES-7 adds, and comparing the two lists.

## 1. Identity

| Item | Value |
|---|---|
| Checkpoint | PRES-7, brief `docs/track-b/evidence/pres-7/issued-brief.md` at `b6a45b60…1175` (the first commit, `5e07f0d3`, byte for byte) |
| Governing rules and plan | PUBLISH_RULES 1.5 (`1bc0c523…f94e`), A8 in force (O46), decision 30 superseding §5.2's page budget and §14's trigger; research v21-r20 §16.3 and §24.14; the economic contract (`21a92085…0889`, decision 32) §§6, 8, 9 with O58's clarifications |
| Evidence tag and tip | `evidence/pres-7` at `<evidence_tip_sha>`, frozen `2026-11-16` (`registry.EVIDENCE_TAGS["evidence/pres-7"]`, checked against the tip's commit date by the return) |
| Final reviewed candidate | `<final_candidate_sha>`: the `--final` build of the page and README |
| Report, review verdict, landing record | this packet; `docs/track-b/evidence/pres-7/integration.md` (the Integration verdict at the candidate) and the focused recheck at the final SHA; the landing record is the Orchestrator's |

## 2. The registry entries (standard §5)

**None is added or changed.** PRES-7 evaluates no new identity. v6's entry (A1 in the frozen records, policy
`720fc581…`) stands as PRES-5 entered it, status "final candidate · pending 4.7T" (O13). The one registry change is the
evidence tag `evidence/pres-7`, which dates the chart's rules (this packet's §0) in Business insights' evidence row.
CP-29's sources (`reports/cp29/*.csv`, `evidence/cp-29`) were registered by CP-29 (O57) and are read, not changed.

## 3. The claim map

`docs/track-b/research-content/pres7-claims.md`:
- **C1201–C1204:** the chart's identity line, the untraded days (CP-29's open item 3), the risk-aware variant and the
  contract's §8 assumptions (a price-taker; no outage or deviation; the costs and the grid-fee exemption as
  assumptions);
- **W58:** a live, prospective or future profit, earnings, income or revenue with a number;
- **W54 narrowed (O60):** to its "error, coverage or interval figure called a profit, a gain in money, a return or a
  success rate" half. Its second half, which refused any "profit of <number>", is withdrawn. W56 and W57 stay.

CP-29's C1101–C1108 (`cp29-claims.md`) move onto the page and into the README, keeping CP-29's `PRES7` surface, which
CP-29's own tests render. C1103's wording changes on every surface, its claim and records unchanged (the claim map
records the old and new words). Every guard has positive and negative cases (`tests/test_52`,
`test_the_forbidden_claims_are_absent_and_guarded`; `tests/test_51`, W54's narrowed half; `tests/cp29`, W56 and W57).

## 4. The derived headline quantities (standard §3.3)

**The report's headline is PRES-5's (P60), its numbers unchanged;** its count now says what it counts ("7 candidate
policies tested", O51 item 8). Business insights' finding (C1102) reads CP-29's records; nothing is derived by PRES-7 except the
drawn running sums, each checked against its record:

| Quantity | Value | Record (`reports/cp29/`) |
|---|---|---|
| (a) A pre-specified verdict | none: the contract is descriptive economics, with no pass mark (contract §1) | — |
| Population | P-all, 2,068 eligible development days, 2020-12-29 to 2026-09-06 | `cp29.p_all.all.v6.median.w25.days` (`summary.csv`) |
| v6's cumulative net profit (median rule, €25) | 257,212 EUR, 0.8953 of perfect foresight's | `cp29.p_all.all.v6.median.w25.{cumulative_profit_eur,share_of_perfect_foresight}` |
| The naive's | 220,136 EUR, 0.7662 | `cp29.p_all.all.naive.median.w25.*` |
| Perfect foresight's (the ceiling) | 287,292 EUR | `cp29.p_all.all.perfect_foresight.perfect.w25.cumulative_profit_eur` |
| (b) v6 − the naive, summed over the days | +37,077 EUR [+32,323, +42,311] | `cp29.paired.p_all.median.v6_minus_naive.w25.total_difference_eur` (`paired.csv`) |
| Its 95% interval | CP-29's paired non-circular moving-block bootstrap: 14-day blocks, 2,000 replicates, seed 20261115 | `research.CP29_INTERVAL` |
| (c) v6 − v5 on P-v5 (358 days) | +165 EUR [−727, +1,032], spanning zero | `cp29.paired.p_v5.median.v6_minus_v5.w25.total_difference_eur` |

## 5. Slot texts, as rendered (standard §6)

Business insights is a product section (§5.1a), not a chapter: no chapter grammar. Its order on the page: the intended
use and the measured implications (PRES-6's, unchanged), the finding panel (C1102 as its heading, the short
qualification, "Explore the evaluation"), then five detail blocks, each under its own heading: the profit chart with
C1201, C1103 and C1202; the setup (C1101); losses, the wear cost, the regimes and the risk-aware variant (C1105, C1106,
C1107, C1203); against v5 (C1104); what the simulation does not show (C1108, C1204, `business.gap`,
`business.limits`); and the evidence row. The README's Business insights paragraph renders, from the claim layer:
`business.use`, `business.measured`, C1101–C1108, C1204, `business.gap` and `business.limits`.

The new and reworded blocks (README form where the block is in the README):

| Block | Claim | Text |
|---|---|---|
| `economics.caveat` | C1108 | Simulated, development, post-selection: no money was traded, and v6 was chosen on these same days, so its result is optimistic for it. Not realized income and not a trading recommendation. |
| `economics.chart` | C1201 | Drawn: the cumulative net profit, in EUR, of one 1 MW / 2 MWh battery on each of the 2,068 eligible development days, 2020-12-29 to 2026-09-06, at €25 per MWh of wear · scheduled from v6's stored forecasts (v6 · DDNN-2 alone, A1 in the frozen records; the median rule), from the similar-day naive's and from the cleared prices themselves (perfect foresight, the ceiling) · doing nothing earns zero, the line at zero · simulated, development, post-selection |
| `economics.untraded` | C1202 | Days not traded. v6's schedule traded on 1,770 of the 2,068 days. On the others it did nothing: on most, no cycle was expected to pay its costs; on 33, shortly after a clock change, the forecast had no value for one hour, and the contract counts such a day as not traded, with zero profit, never dropped. The naive's schedule missed 11 days that way. Every such day stays in the curve, at zero. |
| `economics.risk_aware` | C1203 | A more cautious rule. The risk-aware variant plans as if it buys at the forecast's 75th percentile and sells at its 25th, so it trades only when the spread holds under those prices. With it, v6's schedule traded on 1,457 days and lost money on 39, at most 101 EUR in a day, but earned less: 247,436 EUR, 0.8613 of a perfect forecast's. |
| `economics.assumptions` | C1204 | **Assumed, not modelled.** The battery is a price-taker: every schedule is filled at the cleared price and moves no price. It is never out of service and never deviates from its schedule. The wear cost and the exchange fee are stated assumptions, and the exemption from grid fees is a legal assumption that may change. |
| `business.gap` | P70 | **What is still not evaluated.** Only day-ahead arbitrage was simulated, on development days. Intraday trading, balancing energy and reserves, a real battery's own costs (its price, financing, grid connection and outages) and the live product's forecasts have not been evaluated for profit, and the report shows no live or prospective profit. Lower forecast error and interval coverage are not profit, and not a success rate of any decision. |
| `economics.difference` | C1103 | Day by day on the same days, v6's schedule earned more than the naive's: v6's profit minus the naive's, summed over the days, is +37,077 EUR [+32,323, +42,311], the bracket a 95% confidence interval from resampling 14-day blocks of these days, not a forecast for other days. |

**The wording pass (O51 item 8), each change listed.** The opening and the comparison only; no number changed (§7, the
rendered-number diff). Above the product finding, every definition was fitted so as to add no phone line where it
could (A2; §7):

| # | The fresh reader's confusion (PRES-6) | Block | Before | After |
|---|---|---|---|---|
| 1 | "Owner" never introduced (D01) | `product.live` (P61) | "By the Owner's decision, the Space runs v6 · DDNN-2 alone daily …" | "The Owner, the project's lead, has the Space run v6 · DDNN-2 alone daily …" |
| 2 | "re-baseline" used before it is explained (D02) | `terms.selection_rule` (P60) | "set on 2026-10-12, before the re-baseline's first score." | "set on 2026-10-12, before the re-baseline re-scored every policy on every day." |
| 3 | "4.7T" never introduced (D01, D08) | `terms.final_candidate` (P61) | "frozen for 4.7T, its one test, on 90 days registered in advance." | "frozen for 4.7T, its one test on new data: 90 days registered in advance." |
| 4 | "A1 in the frozen records" is jargon (D02) | `terms.final_candidate` (P61) | "v6 (A1 in the frozen records)" | "v6 (named A1 in the frozen records)", its first use |
| 5 | The policy counts keep changing: 7, 13, 25, 16 (D01, D09, D10) | the headline (P60); `comparison.sub` (P07) | "7 policies tested"; "13 policies · …" | "7 candidate policies tested" (the selection's arms; "policies" stays the defined term); "13 policies drawn · …" (the chart's rows). The census sentence already says "25 policies were tested against them [the targets] … 16 later policies met them too" and that "the chart's 13 rows are not that census" |
| 6 | −7% beside −6% on two populations, reconciled only in D13 (D01, D09) | `comparison.caveat.a1` (P62), directly under the comparison's −6% | — | "The opening's −7% is another population, all 2,068 development days to 2026-09-06; this is the five test periods' 10,747 hours, the last on 2026-04-07." |
| 7 | The development period ends as 2026-04-07 (D14) and 2026-09-06 (D03, D06) | the same sentence | — | both ends named, each with its population |
| 8 | "descriptive 95% intervals" (D01) beside "95% confidence intervals … 14-day block resamples" (D03) | `everyday.finding.v6` (C604), where the selection's intervals appear in the comparison | "… with the selection's descriptive 95% intervals." | "… with the selection's descriptive 95% intervals: confidence intervals from resampling 14-day blocks of days, called descriptive because the selection decided by its registered tests, not by them." (CP-28's report: "they are descriptive, never a substitute for the registered 0.995/1.02 tests") |

Not changed (outside the brief's item 8): "point error" beside "point-error score" (the terms already define both,
"Point and interval error" and "Error scores"); v1's three numbers; "is not shown there"; the "re-frozen" date;
"−2% [−3%, −2%]"; "the trained champion"; the page-load timings in the hero. They stay open (§10.3).

### 5a. The adopted transition (A3)

None: no generation is adopted.

### 5b. The product's documentation (A4, under A8)

Unchanged: the product is v6 and "How the product works" keeps its twelve subjects and routes as PRES-6 left them.
Business insights is §5.1a's section, not one of the twelve subjects.

### 5c. The chart routes (A5)

| Chart | Its heading | The route | Where it starts |
|---|---|---|---|
| `business-profit-chart` | `#business-profit` | "Cumulative profit of the battery, day by day, against the naive" | Business insights' "Explore the evaluation" |
| (text) | `#business-setup` | "The battery, its costs and the trading rule" | the same |
| (text) | `#business-losses` | "Losses, the wear cost, the regimes and a more cautious rule" | the same |
| (text) | `#business-v5` | "Against v5 on its test periods, where the interval spans zero" | the same |
| (text) | `#business-limits` | "What the simulation does not show" | the same |

Each route is the only link to its heading, and none shares its first 40 characters with another route on the page
(`test_52::test_the_section_keeps_a8s_place_and_routes_to_its_details`). The chart is Business insights' own evaluated
use case (A8: "business conclusions cite those results and their own evaluated use case"); no Product results chart is
duplicated.

### 5d. Final-product transition / daily operation (A7/A8/A9)

| Field | State |
|---|---|
| Owner designation and lifecycle | unchanged: v6 (A1), "final candidate · pending 4.7T" (O13, O27) |
| One product identity | unchanged; Business insights names v6 (A1 in the frozen records), CP-28's stored forecasts and the median rule |
| Page order | **A8's, unchanged:** the opening → How the product works → Product results → Business insights → How the models compare → the rest (`test_51::test_the_order_is_a8s_product_first`, `test_52`) |
| A2 placement | the product finding `#product-finding`, re-measured after the wording pass above it (§7) |
| Business evidence | **evaluated, as a simulation:** CP-29's contract run on the development days, labelled simulated, development, post-selection; cumulative net profit over P-all against the naive and the ceiling, with the battery, costs, constraints, initial condition (empty each day), losses, drawdown, wear sensitivity, regimes, the untraded days and the limits; no return (no capital cost), no success rate, nothing live |
| Prospective state | in progress since CP-18c's first live day; nothing prospective is published here, and no live profit (contract §7: a separate round) |

## 6. The MLflow export

**No run changes and nothing is uploaded.** PRES-7 registers no new evidence source (CP-29's three were added to the
export manifest's `sources` by O59), adds no MLflow route (Business insights' routes are page anchors), and changes
no run, tag or experiment. `reports/presentation/mlflow_index.json` is unchanged.
