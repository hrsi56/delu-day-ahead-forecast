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
| Evidence tag and tip | `evidence/pres-7` at `<evidence_tip_sha>`, frozen `2026-11-18` (`registry.EVIDENCE_TAGS["evidence/pres-7"]`, checked against the tip's commit date by the return) |
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
CP-29's own tests render. C1101, C1102, C1103, C1104 and C1108 are reworded on every surface, their claims and records
unchanged (the claim map records each change; editorial E1, E3, E5, E6 and A1, A2, A10, A11). Every guard has positive and negative cases (`tests/test_52`,
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
| (b) v6 − the naive, summed over the days | +37,076.8 EUR [+32,322.6, +42,311.2] in the record (`paired.csv`); shown +37,080 [+32,320, +42,310] (four significant figures, editorial E6) | `cp29.paired.p_all.median.v6_minus_naive.w25.total_difference_eur` (`paired.csv`) |
| Its 95% interval | CP-29's paired non-circular moving-block bootstrap: 14-day blocks, 2,000 replicates, seed 20261115 | `research.CP29_INTERVAL` |
| (c) v6 − v5 on P-v5 (358 days) | +165 EUR [−727, +1,032], spanning zero | `cp29.paired.p_v5.median.v6_minus_v5.w25.total_difference_eur` |

## 5. Slot texts, as rendered (standard §6)

Business insights is a product section (§5.1a), not a chapter: no chapter grammar. Its order on the page: the intended
use and the measured implications (PRES-6's, unchanged), the finding panel (C1102 as its heading, the short
qualification, "Explore the evaluation"), then five detail blocks, each under its own heading: the profit chart with
C1201, C1103 and C1202; the setup (C1101); losses, the wear cost, the regimes and the risk-aware variant (C1105, C1106,
C1107, C1203); against v5 (C1104); what the simulation does not show (C1108, C1204, `business.gap`,
`business.limits`); and the evidence row. The README's Business insights paragraph renders, from the claim layer:
`business.use`, `business.measured`, C1101, C1102, the class caveat, C1103, C1202, C1104–C1108, C1204, `business.gap`
and `business.limits`.

The new and reworded blocks of Business insights, as the final build renders them (README form where the block is in
the README):

| Block | Claim | Text |
|---|---|---|
| `economics.setup` | C1101 | **How the forecast was put to use, in a simulation.** A battery trading in the German–Luxembourg day-ahead market: 1 MW at the grid, 2 MWh usable, 85% round trip, empty at the start and the end of each day, at most one cycle a day, and charging or discharging in an hour, never both. Each day before the 12:00 auction it takes the schedule that the forecast's median prices value highest, net of its costs, and does nothing if none pays: the median rule. The schedule is then settled at the cleared prices, net of the battery's wear (€25 per MWh leaving it) and the exchange fees (€0.10 per MWh bought or sold); no grid fees, levies or taxes are charged. |
| `economics.finding` | C1102 | On all 2,068 eligible development days, one 1 MW / 2 MWh battery scheduled each day from v6's forecasts would have earned 257,212 EUR net, 0.8953 of what a perfect forecast would have earned (287,292 EUR). Scheduled from the similar-day naive's forecasts, it would have earned 220,136 EUR, 0.7662 of it. |
| `economics.caveat` | C1108 | Simulated, development, post-selection: no money was traded, and v6 was chosen on these same days, so its result is optimistic for it. Not realized income and not a trading recommendation. |
| `economics.chart` | C1201 | Drawn: the cumulative net profit, in EUR, of one 1 MW / 2 MWh battery (85% round trip, one cycle a day, empty at each day's start and end) on each of the 2,068 eligible development days, 2020-12-29 to 2026-09-06, net of €25 per MWh of wear and €0.10 per MWh traded · scheduled by the median rule from v6's stored forecasts (v6 · DDNN-2 alone, A1 in the frozen records, policy identity 720fc581…), from the similar-day naive's and from the cleared prices themselves (perfect foresight, the ceiling) · doing nothing earns zero, the line at zero · simulated, development, post-selection |
| `economics.difference` | C1103 | Paired over the same days, v6's schedule earned more in total than the naive's, though not on every day: v6's profit minus the naive's, summed over the days, is +37,080 EUR [+32,320, +42,310], the bracket a 95% confidence interval from resampling 14-day blocks of these days, not a forecast for other days. |
| `economics.untraded` | C1202 | **Days not traded.** v6's schedule traded on 1,770 of the 2,068 days. On the others it did nothing: on most, no cycle was expected to pay its costs; on 33, within a week after a clock change, the forecast was missing one hour by design (its input rules fail closed there), and the evaluation's rules, fixed in advance, count such a day as not traded, with zero profit, never dropped. The naive's schedule missed 11 days that way. Every such day stays in the totals and the curve, at zero. |
| `economics.v5` | C1104 | On the 358 days of v5's last four test periods (the eligible days inside them), v6's and v5's schedules earned about the same, 55,708 and 55,544 EUR: a difference of +165 EUR [−727, +1,032], whose 95% interval spans zero: no advantage either way is shown. |
| `economics.risk_aware` | C1203 | A more cautious rule. The risk-aware variant plans as if it buys at the forecast's 75th percentile and sells at its 25th, so it trades only when the spread holds under those prices. With it, v6's schedule traded on 1,457 days and lost money on 39, at most 101 EUR in a day, but earned less: 247,436 EUR, 0.8613 of a perfect forecast's. |
| `economics.limits` | C1108 | **What the result is not.** Hourly, not quarter-hourly. Not a property of v6 alone: it depends on the battery, the costs and the rule above. Not 4.7T's result and not a forecast of future profit. No return or payback is computed: there is no capital cost. |
| `economics.assumptions` | C1204 | **Assumed, not modelled.** The battery is a price-taker: every schedule is filled at the cleared price and moves no price. It is never out of service and never deviates from its schedule. The wear cost and the exchange fee are stated assumptions, and the exemption from grid fees is a legal assumption that may change. |
| `business.gap` | P70 | **Not evaluated.** Only day-ahead arbitrage was simulated, on development days: not intraday trading, balancing energy or reserves, which are a large share of a real battery's income; not a real battery's own costs (its price, financing, grid connection and outages); and not the live product's forecasts, so the report shows no live or prospective profit. Lower forecast error and interval coverage are not profit, and not a success rate of any decision. |
| `business.limits` | P70 | **Limits.** 4.7T, which opens no earlier than 2026-12-04, is v6's one test on new data; the Space shows the live record, prospective evaluation in progress. |

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

## 7. Checks the checkpoint ran

| Check | Result | Record |
|---|---|---|
| **The binding check before editing** (the brief): no record binds the bytes of a file PRES-7 changed: `src/cp26/harness.py` `PINS` lists none of them; `tests/pres5_landed_code.py` records five `src/delu_forecast/` modules at CP-26's landing and compares every other landed module with the working tree, and the four PRES-7 changes there (`research.py`, `research_claims.py`, `registry.py`, `publication_lint.py`) are among the five recorded; no file in the tree holds the SHA-256 or blob of `scripts/build_pages.py`, `scripts/readme_research.py`, the claim layer or the changed tests (a `git grep` of each hash), except earlier evidence records quoting the published page's and README's hashes as history, and `reports/ddnn2/base-tree.json`, which records CP-24's base commit and is checked against that commit, not the tree | pass | the commands in this row, at `5e07f0d3` |
| Each drawn line ends at its record within 1e-9 relative (never bytes) and keeps all 2,068 days in order; a changed row is refused by the blob check, and past it by the record check | pass | `test_52::test_each_line_ends_at_its_record_and_keeps_every_day`, `…a_changed_daily_row_is_refused` |
| The thinning keeps each pixel column's first, lowest, highest and last point | pass | `test_52::test_the_thinning_keeps_…` |
| The chart: three lines and the zero line in both variants, direct labels, distinct dashes; its identity line names battery, costs, policy, artifact, population, dates, units and class; the key's totals bound to their records | pass | `test_52` (two tests) |
| CP-29's C1101–C1108 and C1201–C1204 on the page, as the claim layer renders them; the limits in plain words; "Not evaluated." in place of the gap | pass | `test_52` (three tests) |
| The untraded days and the risk-aware variant bind their records; C1203's "fewer losses … earned less" holds on them; the 33 missing-hour days are zero in the daily rows | pass | `test_52::test_the_untraded_days_and_the_risk_aware_variant_bind_their_records` |
| W54 (narrowed), W56, W57 and W58 find nothing on the page or in the README; each has positive and negative cases | pass | `test_52::test_the_forbidden_claims_are_absent_and_guarded`; `test_51`; `tests/cp29` |
| The lint's rule for CP-29's daily money figures: 22.2 passes, 22 fails, a total with a decimal fails | pass | `test_52::test_a_daily_money_figure_keeps_its_decimal` |
| The README carries the business claims through the claim layer | pass | `test_52::test_the_readme_carries_the_same_business_claims`; `tests/cp29` (O63's successor) |
| O51 item 7: every marker of the comparison's phone variant inside the drawing; the live axis (0.4, 1.1), every pinned one (0.5, 1.1); the old axis would start v6's hexagon left of the drawing | pass | `test_52::test_the_comparisons_phone_axis_holds_every_marker` |
| O51 item 8: the terms defined at first use ("descriptive" directly below the headline, editorial E2); −7% beside −6%, the two ends, the two kinds of interval | pass | `test_52` (two tests) |
| The editorial fixes: no status word in any new or reworded block (E4, with a negative control); a paired money difference at four significant figures, and the lint refusing five (E6); each caveat once (E5) | pass | `test_52::test_no_status_word_…`, `…four_significant_figures`, `…limits_are_on_the_page_in_plain_words` |
| **No number changed** (O51 item 8): outside Business insights, all 1,147 bound values render as on the published page (`a5db292a`, `5e294d40…`), none added or removed; the reading text loses no number, and every number it gains was already on the page: the comparison's new sentence (−7%, 2,068, 2026-09-06, 10,747, 2026-04-07), "14" (the 14-day blocks) and the overview's new `0.4` tick, twice (O51 item 7). Re-run after the editorial fixes: unchanged. A changed value is caught | pass | `test_52::test_the_wording_pass_changed_no_number` (skips without the history; this row records the run) |
| Decision 30: the five `<= 2_000_000` assertions removed (`test_31`, `test_38`, `test_49`, `test_50`, `test_51`); `test_31` checks that `reports/cp3/pages_build.json` states the page's measured bytes, with a negative control; `test_19` keeps the page self-contained | pass | `test_31::test_the_page_size_is_measured_and_recorded` |
| A2 under A8: the product finding after the wording pass above it | 1440×900: 1,714.6 / 1,715.3 px (limit 1,744); 390×844: 2,407.5 / 2,407.3 px (limit 2,420), Chrome / WebKit; margins 28.7 and 12.5 px | the final release check |
| The browser release check over HTTP (Chrome and WebKit; 1440, 768, 390, 360, 320; iPhone emulation; placements, accessibility, keyboard, contrast, charts, requests, A5 discovery of 59 routes) | **pass at the final page** (`7fd8dd2f…`, the candidate's bytes; 2026-11-18 16:26 UTC); the product finding at 1,714.6 / 1,715.3 px (1440×900, limit 1,744) and 2,407.5 / 2,407.3 px (390×844, limit 2,420). Earlier attempts kept: 1 stopped (the page rebuilt during it; no record); 2 passed on `306c6096`'s page; 3 failed one keyboard route ("Measured results: development data": its scroll timed out at 5 s with the machine's load near 50; mouse and deep link passed); 4 passed on `5575920c`'s page; Integration review 1 passed its own run at the candidate's page | `reports/presentation/release-checks/pres-7-local-release.json`; `…-attempt-{2,3,4}.json` |
| The page's size | 2,082,672 bytes, +84,799 over PRES-6's 1,997,873: the profit chart's two variants (the desktop's three polylines thinned to at most four points a pixel column) and the new text | `reports/cp3/pages_build.json` |
| The lint | page 0, README 0, templates 0: PASS | `make lint-publication` |
| The prerelease in a clean worktree (runbook §9 offline checks), `--stage final`, at the candidate `364ac020` (2026-11-18 10:02–10:57 UTC) | pytest 3.13: 3,501 passed, 17 skipped; CI's steps under 3.12: 3,497 passed, 20 skipped, **1 failed**, `tests/cp17c/test_refreeze17c.py::test_the_committed_manifest_verifies_here` ("CPython 3.12.14 here, 3.13.15 pinned": the frozen package pins 3.13; PRES-5's and PRES-6's prereleases recorded the same one); verify, lint, rebuild determinism (tree unchanged) and the publication guard pass; links: **1 failed**, `blob/evidence/pres-7/…/publication-packet.md`, 404 until the Orchestrator pushes the tag (§8.5), no cross-host redirect | `reports/presentation/release-checks/pres-7-candidate-prerelease.json` |

## 8. Publication completion receipt and the Orchestrator's packet

### 8.0 What would be published

| Surface | Reviewed output | Identity | Now public |
|---|---|---|---|
| Report, GitHub Pages | `docs/index.html` at `<final_candidate_sha>`, the `--final` build | `<final_page_sha256>`, `<final_page_bytes>` bytes | 1,997,873 bytes, `5e294d40790f3415c14cf932e94f1351e2e99a0b84d6efd3d2321046d7eccdaa` (PRES-6) |
| README | `README.md` at `<final_candidate_sha>` | `<final_readme_sha256>` | `da9ae187766c895d102676b16a5870540029d471b26687fe78cc3319edc77e1a` |
| Hugging Face Space and its card | **no PRES-7 action**: the live product (CP-18d's since 2026-11-18), published daily by the runner | the runner's latest publication (§8.5) | it moves with each daily run |
| MLflow `delu-generations` | **no PRES-7 action** (§6) | 105 runs, the committed export | 105 runs |

### 8.1 Receipt — intended identities (the Orchestrator and the public checker complete the rest)

| Surface | Intended identity | Action / unchanged rationale | Observed public identity and UTC time | Verification record and result | Outstanding action |
|---|---|---|---|---|---|
| GitHub source / README | `land/pres-7` (the squash of `<evidence_tip_sha>` onto the moved `main`; PRES-7's paths equal the tip's); README `<final_readme_sha256>`, its Business insights paragraph carrying CP-29's claims | push (§8.3) | to fill | `pres-7-publication-receipt.json` (GitHub main); the served README's hash (§8.5) | §8.2–8.3 |
| GitHub Pages | `<final_page_sha256>`: Business insights with the profit chart, A8's order unchanged | deploy by the push (§8.3) | to fill | `pres-7-publication-receipt.json` (Pages); `pres-7-public-report.json`; `pres-7-postdeploy-links.json` | §8.3, §8.5 |
| Public MLflow | unchanged: the committed export's 105 runs and experiment tags | verified unchanged (§6) | to fill | `pres-7-postdeploy-mlflow-mirror.json` | §8.5 |
| Hugging Face Space card | the live product's, as the runner last published it | **no PRES-7 action** | to fill | `pres-7-publication-receipt.json` (Space files) against the runner artifact's build | §8.5 |
| Hugging Face direct demo | the live product at the root; v1 at `history/index.html` | **no PRES-7 action** | to fill | `pres-7-publication-receipt.json` (direct page, by `cp18.publish.normalized`); the report's Space links hop by hop, none ending on another host | §8.5 |

- **Publication-to-MLflow mapping:** unchanged.
- **Final product and daily updates:** CP-18c's (CP-18d's once it lands). The report carries no live record.
- **Completion disposition:** incomplete until these steps and their public checks pass; A12 is decided in §8.6.
- **Authority:** the landing, the push and the Pages deployment are the Orchestrator's, after the return (the brief's
  "Owner-only actions already authorized"; decisions 27, 28 and 32). There is no Space or MLflow step.

Every command below runs from the primary checkout, `/Users/djourno/Downloads/PJM`. None opens a pager or an editor
(`git --no-pager`, `GH_PAGER=cat`). The return gives these commands with `<evidence_tip_sha>`, `<final_page_sha256>`,
`<final_readme_sha256>` filled in. Keep every record a step writes, first failures included.

### 8.2 Step 1 — the LAND, on a moved `main`

PRES-7 branched from the issue commit `a5db292aa0aed68886ea0ab7237cf5fe9a672b65`. Since then `origin/main` moves each day
by the runner's data-only commits (author `delu-daily`, `live/` only), and CP-18d landed beside it on 2026-11-18
(`c61757d8`: `src/cp18/`, `space-product/`, `scripts/build_product_space.py`, `.github/workflows/daily.yml`,
`tests/cp18*`, `reports/cp18d/` and its records). PRES-7's paths (the first command below lists them) are disjoint from
all of those; the overlap check below proves it.

**No daily job may be running** (O47: a push during a run makes the run discard its records). Here and again before
the push:

```bash
GH_PAGER=cat gh run list --workflow daily.yml --limit 6 --json databaseId,status,event,createdAt --jq '.[] | "\(.databaseId) \(.status) \(.event) \(.createdAt)"'
```

Expect every line `completed`. A `queued`, `in_progress` or `waiting` line: wait for it to finish.

```bash
git --no-pager rev-parse --abbrev-ref HEAD
```

Expect `main`.

```bash
git fetch origin && git --no-pager log --format='%h %an %s' main..origin/main && git --no-pager diff --name-only main origin/main | grep -v '^live/' ; echo only-live-checked
```

Expect only `delu-daily` commits and then only `only-live-checked`. Any other path: stop and read it first (CP-18d's
landing, if it pushed, is expected and is checked for overlap below).

```bash
git merge --ff-only origin/main
```

Expect `Fast-forward` (or `Already up to date.`).

```bash
git --no-pager status --porcelain=v1
```

Expect no output (or only the Orchestrator's own edit to `progress.md`). Any other line: stop and resolve it first.

**PRES-7's paths, and no untracked twin:**

```bash
git --no-pager diff --name-only a5db292aa0aed68886ea0ab7237cf5fe9a672b65 <evidence_tip_sha> > .local/artifacts/pres-7/pres7-paths.txt && wc -l < .local/artifacts/pres-7/pres7-paths.txt && grep -c '^live/' .local/artifacts/pres-7/pres7-paths.txt; while IFS= read -r f; do git ls-files --error-unmatch -- "$f" >/dev/null 2>&1 && ! git --no-pager diff --quiet -- "$f" && echo "MODIFIED $f"; git ls-files --error-unmatch -- "$f" >/dev/null 2>&1 || { [ -e "$f" ] && echo "TWIN $f"; }; done < .local/artifacts/pres-7/pres7-paths.txt; echo twins-checked
```

Expect the path count the return gives, then `0` (no `live/` path), then only `twins-checked`.

```bash
git --no-pager diff --name-only a5db292aa0aed68886ea0ab7237cf5fe9a672b65 HEAD | grep -xFf .local/artifacts/pres-7/pres7-paths.txt ; echo overlap-checked
```

Expect only `overlap-checked`: no path changed on both sides (if CP-18d landed first, this is the check that it shares
no path with PRES-7).

```bash
git --no-pager merge --squash gauntlet/pres-7
```

Expect `Squash commit -- not updating HEAD` and the diffstat, with no `CONFLICT` line.

**PRES-7's paths equal the evidence tip's, and every other path equals `main`'s:**

```bash
xargs git --no-pager diff --cached --quiet <evidence_tip_sha> -- < .local/artifacts/pres-7/pres7-paths.txt && test -z "$(git --no-pager diff --cached --name-only HEAD | grep -vxFf .local/artifacts/pres-7/pres7-paths.txt)" && echo STAGED-PRES7-PATHS-EQUAL-EVIDENCE-TIP
```

Expect only `STAGED-PRES7-PATHS-EQUAL-EVIDENCE-TIP`. If it does not print, stop: nothing is committed yet, and
`git reset --merge` restores the index.

**The evidence label's date equals the tip's:** Business insights' evidence row labels the chart's rules "frozen
<date>" from `registry.py::EVIDENCE_TAGS["evidence/pres-7"]`.

```bash
git --no-pager log -1 --format=%cs <evidence_tip_sha> && git --no-pager show <evidence_tip_sha>:src/delu_forecast/registry.py | grep '"evidence/pres-7"'
```

Expect the same date on both lines (`2026-11-18`). A different date: stop and report it.

```bash
git commit -F .local/artifacts/pres-7/land-commit-message.txt
```

Expect `[main <land_sha>] Publish PRES-7: …`. The hooks run and print nothing when clean.

```bash
git tag land/pres-7 HEAD
```

```bash
git tag evidence/pres-7 <evidence_tip_sha>
```

Both print nothing.

```bash
git --no-pager diff --name-only HEAD <evidence_tip_sha> | grep -v '^live/' ; echo landed-tree-checked
```

Expect only `main`'s own movement since `a5db292a` outside `live/` (CP-18d's paths and records if it landed first, any
Orchestrator record), then `landed-tree-checked`.

### 8.3 Step 2 — the push

Re-run the first command of §8.2: no daily job may be running. Then **the value-based secret scan**, over exactly what
the push will send:

```bash
printf '%s %s %s %s\n' refs/heads/main "$(git rev-parse main)" refs/heads/main "$(git rev-parse origin/main)" refs/tags/land/pres-7 "$(git rev-parse land/pres-7)" refs/tags/land/pres-7 0000000000000000000000000000000000000000 refs/tags/evidence/pres-7 "$(git rev-parse evidence/pres-7)" refs/tags/evidence/pres-7 0000000000000000000000000000000000000000 | python3 scripts/secret_guard.py pre-push origin "$(git remote get-url origin)" && echo SECRET-SCAN-CLEAN
```

Expect `SECRET-SCAN-CLEAN`. A `secret-guard: BLOCKED` line means stop and tell no one the value.

```bash
python3 scripts/publication_guard.py tree
```

Expect a PASS line: the landed page is the final build.

```bash
git push origin main land/pres-7 evidence/pres-7
```

Expect `<old>..<first 7 of land_sha>  main -> main` and two `[new tag]` lines. **If the push is refused** because the
runner pushed in between (`fetch first`): never force, rebase or reset. Wait until no daily job runs, `git fetch
origin`, confirm with §8.2's command that the new commits touch only `live/`, merge them with `git merge --no-edit
origin/main` (data-only paths, so no conflict; the tags stay on the squash commit), and push again. GitHub Pages then
serves `docs/`. Read GitHub's CI for the pushed commit before the closure:

```bash
GH_PAGER=cat gh run list --branch main --limit 4
```

### 8.4 Step 3 — no Space upload and no MLflow write

PRES-7 changes nothing on Hugging Face or DagsHub. The Space is CP-18c's (CP-18d's once landed), published daily by the
runner. If the served Space is not what the runner's latest publication record names, that is the live product's to
resolve; do not redeploy under this packet.

### 8.5 Step 4 — the public checks, per surface

Each writes a new record; keep a first failure beside its retry. The Playwright commands need
`PLAYWRIGHT_BROWSERS_PATH=/Users/djourno/Downloads/PJM/.local/tools/ms-playwright`. Wait until Pages has deployed the
push:

```bash
curl -s https://hrsi56.github.io/delu-day-ahead-forecast/ | shasum -a 256
```

Expect `<final_page_sha256>` (now `5e294d40…daa`, PRES-6's).

```bash
curl -s https://raw.githubusercontent.com/hrsi56/delu-day-ahead-forecast/main/README.md | shasum -a 256
```

Expect `<final_readme_sha256>`.

**The Space's build for the receipt, from the runner's latest publication.** CP-18d landed on 2026-11-18
(`c61757d8`): the runner's Actions artifact `daily` now keeps the Space's whole build, recorded before the upload by
`cp18.runner_artifact` (`space-artifact.json`), so the build is taken from the artifact, not assembled (PRES-6's
landing record described the assembly for the earlier, partial artifact). Fetch the latest successful run's artifact,
read-only, and verify it with the live product's own checker:

```bash
RUN=$(GH_PAGER=cat gh run list --workflow daily.yml --status success --limit 1 --json databaseId --jq '.[0].databaseId') && echo "$RUN" && gh run download "$RUN" -n daily -D ".local/tmp/pres-7/runner-$RUN" && MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1 uv run python -m cp18.runner_artifact verify --artifact ".local/tmp/pres-7/runner-$RUN" --out ".local/tmp/pres-7/runner-$RUN-verify.json" && echo RUNNER-ARTIFACT-VERIFIED
```

Expect the run id and `RUNNER-ARTIFACT-VERIFIED`: the whole build is present as recorded, except exactly the fitted
arrays the results step deletes on purpose (`deleted_arrays` in `space-artifact.json`). The Space serves those arrays
(its Explainability view needs them), so fetch each one, anonymously, from the Space:

```bash
B=".local/tmp/pres-7/runner-$RUN/space" && for f in $(python3 -c "import json, sys; print(' '.join(a['path'] for a in json.load(open(sys.argv[1]))['deleted_arrays']))" ".local/tmp/pres-7/runner-$RUN/space-artifact.json"); do curl -sfL -o "$B/$f" "https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/$f" && echo "fetched $f"; done
```

Then the build must equal its own record, every file listed and none extra:

```bash
MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1 uv run python -c "import hashlib, sys, pathlib; from cp18.publish import listed; b = pathlib.Path(sys.argv[1]); files = listed(b); bad = [p for p, f in files.items() if not (b / p).is_file() or hashlib.sha256((b / p).read_bytes()).hexdigest() != f['sha256']]; extra = sorted(str(q.relative_to(b)) for q in b.rglob('*') if q.is_file() and str(q.relative_to(b)) not in files); print('BUILD-EQUALS-ITS-RECORD' if not bad else ('DIFFERS', bad[:5]), 'extra:', extra)" "$B"
```

Expect `BUILD-EQUALS-ITS-RECORD` and an `extra` list that is empty or holds only `app/space-build.json` (a record
cannot list its own hash). A fetched array that differs from the record means the Space moved after `$RUN`: rerun from
the newer run. Then its identity:

```bash
MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1 uv run python -c "import sys, pathlib; sys.path.insert(0, 'scripts'); from build_wasm_space import bundle_sha256; print(bundle_sha256(pathlib.Path(sys.argv[1])))" "$B"
```

**The receipt:** GitHub `main`, Pages, the Space's files and direct page against that build, the public MLflow mirror
and the links, each checked independently and anonymously, every attempt kept:

```bash
MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1 uv run python scripts/publication_receipt.py --landing land/pres-7 --bundle "$B" --expect <the identity just printed> --date pres-7
```

Expect six rows `PASS` and `PASS: wrote reports/presentation/release-checks/pres-7-publication-receipt.json`, with
`pres-7-postdeploy-links.json` and `pres-7-postdeploy-mlflow-mirror.json` beside it; exit 0.
- **The direct page** passes by CP-18c's rule (`cp18.publish.normalized`): the record's `removed_bytes` is the host's
  script and meta run.
- **The links record** lists every hop of every redirect, never followed blindly: every link into the Space must end
  on the Space's own host, `cross_host_redirects` `[]`. The report links into the Space from the opening and v1's
  history; PRES-7 adds no Space link.
- If the Space-files row fails because the Space moved after `$RUN` (a newer run published), rerun from the newer
  run's download.

The browser records:

```bash
PLAYWRIGHT_BROWSERS_PATH=/Users/djourno/Downloads/PJM/.local/tools/ms-playwright .local/tools/playwright/bin/python scripts/check_reader_paths.py release https://hrsi56.github.io/delu-day-ahead-forecast/ --shots .local/artifacts/pres-7/public-report --out reports/presentation/release-checks/pres-7-public-report.json
```

```bash
PLAYWRIGHT_BROWSERS_PATH=/Users/djourno/Downloads/PJM/.local/tools/ms-playwright .local/tools/playwright/bin/python scripts/check_reader_paths.py mlflow-routes --mirror-record reports/presentation/release-checks/pres-7-postdeploy-mlflow-mirror.json --shots .local/artifacts/pres-7/public-mlflow-postdeploy --out reports/presentation/release-checks/pres-7-public-mlflow-routes-postdeploy.json
```

Each passes with `passed` true. GitHub may answer anonymous `blob` requests with 503 after a burst: keep the failed
record, wait, and rerun with a new `--date` (for example `pres-7-retry-1`); a 503 is never a pass. The links to
`blob/evidence/pres-7/…` (Business insights' "The chart's rules" link) answer 404 until the tag is pushed: run the
checks after the push.

### 8.6 Step 5 — A12, then the receipt

**A12 (§10.5).** An independent post-deployment check is required if either:

1. a served surface differs from what the binding independent pre-deployment review covered: Pages' bytes differ from
   `<final_page_sha256>`, the focused recheck's page; or the public MLflow differs from the committed export; or
2. a required public check above fails without a passing targeted retry.

**Where it can add something** even without a trigger: the deployed Business insights in a real browser, both engines,
at 1440 and 390 px: the profit chart's two variants (each line labelled, the zero line, the key's totals equal to the
page's text), its route from "Explore the evaluation" by mouse, keyboard and deep link, and the product finding's
placement after the wording pass (A2 under A8). A checker that wrote none of PRES-7 forms its findings before reading
earlier reviews and writes a dated review under `docs/track-b/` with the per-surface identities, first failures and
retries, and its PASS / FAIL / INCOMPLETE verdict. If `pres-7-public-report.json` already records all of that and
passes on its first attempt, it covers the point, as at PRES-6 (O50).

Then fill §8.1's last three columns from the records. The disposition is complete only when every row is verified.

### 8.7 If publication fails

Stop the rollout and name each affected URL and revision. The identities to restore are Pages
`5e294d40790f3415c14cf932e94f1351e2e99a0b84d6efd3d2321046d7eccdaa` and README `da9ae187…77e1a` (PRES-6). PRES-7 touches
neither the Space nor MLflow. No force-push or history rewrite is part of a recovery, and `main` keeps the runner's
commits: a revert is a new commit on top of them, and a rollback is its own Owner action.

## 9. Applicability matrix

### 9.1 PUBLISH_RULES 1.5, clause by clause (decision 30 superseding §5.2's budget and §14's trigger)

| Clause | Applies? | How PRES-7 meets it, or why not | Evidence |
|---|---|---|---|
| §1.1–§1.3 authority, identities, categories | yes | Rules 1.5, research v21-r20 §§16.3, 24.14 and the contract by the brief's hashes; v6's status unchanged; every new figure a simulated development result | §1; the brief |
| §2 reader contract; A1; A2 | yes | Each money figure names its unit (EUR) and what it is; A2 under A8 on the product finding, re-measured after the wording pass above it, in Chrome and WebKit | §7 |
| §3.1 evidence classes; withheld claims | yes | Every economic figure "simulated, development, post-selection"; nothing live, prospective or 4.7T's; W54 narrowed (O60), W58 added, W56 and W57 kept, W1–W55 in force | §3; `test_52` |
| §3.2 scores, comparisons, uncertainty | yes | The declared benchmark (the naive) and the ceiling (perfect foresight) beside v6; the paired differences with their 95% block-bootstrap intervals; v6 − v5 shown with an interval spanning zero; losses, drawdown, wear sensitivity and regimes beside the total | §4; §5 |
| §3.3 counting | yes | No new rule or verdict; the headline's count names what it counts; the 2,068 days and the untraded days from the committed rows | §4; §5 |
| §3.4 provenance and formatting | yes | Every number a record; money totals whole EUR, daily money figures one decimal (the lint's rule, §7), shares four significant figures | the lint; `test_30`; `test_52` |
| §4 registry, transitions; A3; A10 | no change | No identity added or adopted | §2; §5a |
| §5 page architecture; A8 | yes, in force (O46) | A8's order unchanged; Business insights cites its own evaluated use case with its own chart, duplicating no Product results chart; the comparison changes only by O51 items 7 and 8 | §5c, §5d; `test_51`, `test_52` |
| §5.1 twelve subjects | unchanged | The product is unchanged | §5b |
| §5.1a Business insights | **yes, the decision-policy evaluation now exists** | Cumulative net profit over the full named period (P-all) against the declared benchmark, with units, costs, constraints, the initial condition (empty each day) and risk and loss context; simulated against realized labelled; untraded and missing days kept and counted; no return without capital; no error or coverage figure called a profit or a success rate; no business success percentage | §0; §5; `test_52` |
| §5.2 page budget | **superseded by decision 30** | No limit; the size measured (2,082,672 bytes, +84,799 over PRES-6's 1,997,873), recorded in `reports/cp3/pages_build.json` and checked against the page (`test_31`); the page stays one self-contained file (`test_19`) | §7 |
| §6 charts, discovery; A5 | yes | One new chart: its identity line, direct labels, line styles, a key with each total, the zero line; its route in "Explore the evaluation"; chart text ≥ 12 px at 320 | §5c; §7 |
| §7.1–§7.3 product, live, Space; A7, A9 | the Space's (CP-18c) | The report shows no live panel, number or profit | `test_51`, `test_52` |
| §8 surfaces | yes | Report and README updated and in agreement; MLflow and the Space unchanged | §6, §8 |
| §9 browser and accessibility matrix | yes | The release check over HTTP, both engines, every width, iPhone emulation | §7 |
| §10.1–§10.4 independence, fresh reader, public identity, verdict; A6 | yes | Editorial review, fresh reader (the six questions, then the brief's two) and Integration Critic, none an author of PRES-7 | `editorial.md`, `fresh-reader.md`, `integration.md`; §8.5 |
| §10.5 A12 | yes, after deployment | Its conditions and the useful check | §8.6 |
| §11 packet and order | yes | §0 before drawing; build → editorial → fresh reader → Integration at the candidate → final build → focused recheck → the Orchestrator's steps | this packet |
| §12 baseline coverage | yes | Every number on days through 2026-09-06 | `test_52`; `tests/cp29` |
| §13 acceptance record | yes | §9.2 | — |
| §14 pending triggers | §14's page-size trigger superseded (decision 30) | — | the brief |
| A11 work availability | yes | One usage-limit pause, recorded | the ledger; §10.2 |

### 9.2 The §13 acceptance record

| Area | Record |
|---|---|
| Authority | Rules 1.5 `1bc0c523…f94e` with decision 30; research v21-r20 §§16.3, 24.14; the contract `21a92085…0889` (decision 32, O58); brief `b6a45b60…1175`; rulings O60, O63 |
| Identity | `gauntlet/pres-7` off `a5db292a`; `<final_candidate_sha>`; `<evidence_tip_sha>`; the landing and served identities after the Orchestrator's steps |
| Claims | §0's rules committed before drawing; §4's records with their rows, populations and intervals; C1101–C1108 (CP-29), C1201–C1204 |
| Reader | A8's order; the product finding within A2; the fresh reader's record, with the battery questions |
| Content | Business insights: the use, the measured implications, the evaluated use with its chart, losses, sensitivity, regimes, v6 against v5, the untraded days, the limits, what is not evaluated |
| Charts | One new chart, identified, routed, directly labelled, with its zero line; the comparison's phone axis |
| Accessibility | The engine and width matrix over HTTP |
| Tracking | MLflow unchanged (§6) |
| Release | The prerelease in a clean worktree; the `--final` build; the exact-candidate Integration check; the focused recheck |
| Public check | After the Orchestrator's steps (§8.5–§8.6) |
| Follow-up | §10.3's open items with proposed rulings; the reviews' findings, each dispositioned (§10.4) |

### 9.3 The runbook

| Touchpoint | Status |
|---|---|
| `registry.EVIDENCE_TAGS["evidence/pres-7"]` | added, dated by the evidence tip in the final-build commit; §8.2 checks it before tagging |
| `research.py::SOURCES`, `POPULATIONS` | unchanged: CP-29's sources and populations, registered by CP-29 (O57) |
| `research.py::display` | paired money differences at four significant figures (E6) |
| Claim map and blocks | `pres7-claims.md`; `PRES7_BLOCKS`; CP-29's blocks on the page and README; `business.gap`, `business.limits`, and O51 item 8's blocks reworded; `terms.class_final` |
| `publication_lint` | two precision cases: CP-29's daily money figures one decimal; paired money differences four significant figures |
| `CHARTS_BY_RUN`, `mlflow_export.py` | not needed: no run or route changes |
| Tests | `tests/test_52`; updates to tests 31, 38, 45, 49, 50, 51; `tests/cp29/test_claims.py` under O63 |
| Limits to watch | A2 under A8 on phones (12.5 px) and desktop (28.7 px); chart text ≥ 12 px at 320 |

### 9.4 The brief's observable outcome

| Outcome | Where it is met | Evidence |
|---|---|---|
| 1 The profit chart | Business insights' chart from `daily.csv` by §0; the identity line; C1101–C1108, C1202, C1203 beside it; the limits in plain words; nothing forbidden | §0, §4, §5, §7; `test_52` |
| 2 Business insights' text | the use, the measured implications, the evaluation's result, its limits; "Not evaluated." in place of the gap | §5; `test_51`, `test_52` |
| 3 The order (A8); A2 | unchanged; the product finding re-measured | §7; the release check |
| 4 The README | the same business claims through the claim layer | `test_52::test_the_readme_carries_the_same_business_claims`; `tests/cp29` (O63) |
| 5 Decision 30; O51 items 7, 8; CP-29's items 3–5 | §7; §5's wording table; the untraded days (C1202); `business.gap`; W54 narrowed; the zero line | §5, §7, §10 |
| 6 The page's size | 2,082,672 bytes, recorded | `reports/cp3/pages_build.json` |
| 7 Review | editorial, fresh reader, Integration at the candidate, focused recheck at the final SHA | `docs/track-b/evidence/pres-7/` |
| 8 The packet | §8 | — |

## 10. Rulings, disclosures and open presentation items

### 10.1 The Orchestrator's rulings in this block

| Ruling | What it decides | Where applied |
|---|---|---|
| O60 (in the assignment) | W54 narrows to its "error or coverage called a profit" half; W56 and W57 stay | `research_claims.WITHHELD_PATTERNS`; `pres7-claims.md`; `test_51`, `test_52` |
| O63 (2026-11-16, decision 27) | PRES-7 may make exactly one edit in `tests/cp29/`: `test_claims.py::test_the_blocks_are_written_for_pres7_and_appear_on_no_published_surface` becomes its PRES-7 successor, which asserts that every CP-29 block renders on the page and in the README through the claim layer and binds its `cp29.*` records, with a negative control; the other CP-29 files stay byte-identical; the pin check first | `tests/cp29/test_claims.py::test_the_blocks_render_on_the_page_and_the_readme_through_the_claim_layer` (with its helper `_publication_problems`). The pin check: no record, manifest or test in the tree holds `test_claims.py`'s SHA-256 (`b935aeea…3b13`) or its blob (`991568ef…1567`); CP-29's evidence cites it by name only (`docs/track-b/evidence/cp-29/integration.md`, `publication-packet.md`). `git diff a5db292a -- src/cp29 reports/cp29 tests/cp29` lists only `tests/cp29/test_claims.py` |
| Decision 30 (the Owner, 2026-11-15) | No page-size limit; `docs/PUBLISH_RULES.md` stays unedited (CP-26's harness pins its bytes) | five assertions removed (§7); the size measured and recorded |

### 10.2 Disclosures

- **CP-29's blocks keep their `PRES7` surface** beside `PAGE` and `README`: CP-29's
  `test_each_block_binds_its_records_and_the_claims_hold_on_them`, byte-identical under O63, renders them there.
- **C1103 is reworded** on every surface: CP-29's "earned +37,077 EUR more than the naive's" put a signed total inside
  "more"; it now reads "Paired over the same days, v6's schedule earned more in total than the naive's, though not on
  every day: v6's profit minus the naive's, summed over the days, is +37,080 EUR [+32,320, +42,310], the bracket a 95%
  confidence interval …". Its claim and records are unchanged; the other reworded CP-29 claims are listed in §3.
- **Four PRES-6 tests and two PRES-5 wording pins are updated** for what PRES-7 replaces: `test_51`'s Business insights
  checks (the gap sentence, "no chart", the old W54 profit half, the README's gap) now check the use, the measured
  implications, that the gap sentence is gone and "Not evaluated." stands; `test_51`'s binding check admits CP-29's
  records in Business insights only, with a negative control for Product results; `test_38`'s headline and product-line
  pins carry the new words.
- **The lint's precision rule gains one case:** CP-29's daily money figures (`display_precision` 1: a daily mean,
  median or percentile) follow the one-decimal EUR rule; without it, C1107's "22.2 EUR a day" was refused as a count.
  Totals stay whole.
- **The comparison's axis widens on both variants,** not only the phone's: the fix is to the live comparison's domain,
  which PRES-5 meant to be (0.4, 1.1) for both. On desktop v6's interval-score marker no longer sits left of the axis's
  start. The rows, values and pinned charts are unchanged.
- **Release-check attempt 1 was stopped** (2026-11-16, minutes after 02:35 UTC): the page was rebuilt (the phone chart's
  subtitle and top margin) while it read the page over HTTP, so its record would have mixed two pages. It wrote no
  record; attempt 2 ran on the committed page.
- **Two usage-limit pauses,** recorded in the ledger, the work resumed each time where it stopped: the five-hour limit,
  2026-11-15 ~23:25 to 2026-11-16 02:20 UTC; the weekly limit, 2026-11-16 ~03:05 to 2026-11-17 20:52 UTC, which also
  stopped the editorial review mid-way (it resumed at the same candidate and says so).
- **§0's "thin and dashed" perfect-foresight line** is drawn with the short dash `2 3`, which the key and the chart's
  description call dotted; the naive's dash is `6 4`. §0's identity list is met in the line above the chart (the policy
  identity `720fc581…` added after the editorial review's A5); the naive's frozen rule is stated in Product results'
  caveat directly above.
- **The suite's one failure at `5be0d178`** (`test_45`'s undefined-term control): "7 candidates tested" dropped the word
  "policies" that the term beneath the headline defines. The headline reads "7 candidate policies tested"
  (`bf369d6b`); the next full run is the prerelease (§7).
- **The final candidate's class term is new** (`terms.class_final`, editorial E2): the general `terms.class` also
  serves headline forms whose intervals are the rule's own, where "not the rule's own test" would be false.
  `test_45`'s pin of the final candidate's terms names it.
- **The machine was shared:** CP-18d's Critic and stress runs held the load average near 50 during release-check
  attempt 3 (2026-11-17 21:12 UTC on); its timings are not PRES-7's measurements, and no PRES-7 check depends on
  speed.
- **The A2 margin on phones** narrows from PRES-6's 50.5 px to 12.5 px: every definition above the
  product finding was fitted to add no phone line where it could (measured candidate by candidate in Chrome at 390 px),
  and the remaining growth is one line of the selection-rule term (19 px; with its "Read it" link, the only
  two-line wording, "re-scored every policy daily", would read as an ongoing daily process).

### 10.3 Open presentation items, each with a proposed ruling

1. **A2's phone margin is 12.5 px** (PRES-6: 50.5): the definitions O51 item 8 and the editorial
   review's E2 require sit above the product finding, each fitted to add as few phone lines as it could (§10.2).
   Proposed: accept; anything added above the product finding is re-measured. A later presentation round may win room
   back from the opening without a number change.
2. **The status-word lint scans only the claim layer's root block list** (editorial A16): `PRES5_BLOCKS` onward are
   not scanned, so the pre-existing "the published prices may still be revised" in How the product works passes.
   `test_52` scans PRES-7's own blocks. Proposed: the next presentation round extends `TEMPLATE_SOURCES` to every
   block list and rewords that sentence.
3. **"among 7 arms" in v6's chapter** (editorial A9; outside the brief's opening and comparison): the headline says "7
   candidate policies tested". Proposed: the next presentation round uses the same words there.
4. **PRES-6's fresh reader's other confusions, outside O51 item 8** (packet §5): "point error" beside "point-error
   score"; v1's three numbers; "is not shown there"; the "re-frozen" date; "−2% [−3%, −2%]"; "the trained champion";
   the page-load timings in the hero. Proposed: one more wording pass, as its own presentation round, if the Owner
   wants it; none is a rule violation.
5. **The receipt against the runner's artifact** (PRES-6's O51 item 5): closed by CP-18d's landing, whose runner keeps
   the Space's whole build in its artifact; §8.5 takes the build from it and verifies it with `cp18.runner_artifact`.
   Proposed: closed.
6. **CP-29's open item 1** (a missing cleared-price row would be solved on the remaining hours) stays with the round
   that applies the contract to the live record (contract §7); PRES-7 shows no live number.

### 10.4 The reviews' findings and their dispositions

**The editorial review** (`editorial.md`, at `306c6096`; six violations, seventeen advisories; every bound number
equal to its row; the chart's six polylines byte-identical to the reviewer's own re-derivation). Fixed in the commit
after `bf369d6b` unless stated:

| Finding | Disposition |
|---|---|
| E1 (medium): no initial condition; the chart's line names only the battery's size and the wear cost | **Fixed.** C1101 states "empty at the start and the end of each day"; the line above the chart and the chart's description name the 85% round trip, one cycle a day, the empty start and end, €25 per MWh of wear and €0.10 per MWh traded |
| E2 (medium): "descriptive 95% intervals" first used in the headline, defined at the comparison | **Fixed** directly below the headline: the final candidate's class term, `terms.class_final`, reads "development evidence, not a test on new data; descriptive intervals: not the rule's own test" (the general `terms.class` stays for headline forms whose intervals are the rule's own). The comparison keeps the longer sentence. A2 re-measured (§7) |
| E3 (medium): "the schedule", "the median rule" and "the contract" used before they are defined | **Fixed.** C1102: "one 1 MW / 2 MWh battery scheduled each day from v6's forecasts"; C1101 states the median rule; C1202: "the evaluation's rules, fixed in advance" |
| E4 (low): "What is still not evaluated" uses wording that expires | **Fixed:** "Not evaluated." `test_52` scans every new and reworded block for the standard's status words, with a negative control |
| E5 (low): the class caveat stated twice in Business insights, and "after selection" a third time | **Fixed.** The class caveat stands once, beside the finding (and beside the README's first profit figure); day-ahead only stands once, with what is not evaluated; C1108's rest is "What the result is not"; `business.limits` keeps 4.7T and the live record only |
| E6 (low): a paired money difference at five significant figures | **Fixed:** "+37,080 EUR [+32,320, +42,310]" (`research.display`, four significant figures for `UNIT_EUR_MONEY_DIFF`); the lint's rule `sig4_whole`, with a negative control; totals stay whole EUR (A13: no clause caps a total) |
| A1 "Day by day … earned more" reads as every day | **Adopted:** "Paired over the same days, v6's schedule earned more in total than the naive's, though not on every day" |
| A2 the v5 block | **Adopted:** "whose 95% interval spans zero: no advantage either way is shown" |
| A3 "had no value for one hour"; "shortly after" | **Adopted:** "within a week after a clock change, the forecast was missing one hour" |
| A4 tense | **Kept:** each figure carries its class; the finding's conditional sets the frame |
| A5 packet §0 against the page | **Adopted:** the line above the chart names the policy identity (`720fc581…`); §0's "dashed" perfect-foresight line is drawn with the short dash `2 3`, which the key and the description call dotted (§10.2) |
| A6 the README | **Adopted:** the class caveat beside its first profit figure, and C1202 (the untraded days) carried; C1203 stays a page route |
| A7 README length | **Kept:** one paragraph per section, as the README's other sections |
| A8 "The opening's −7%" in the README | **Adopted:** "The headline's −7%" (both surfaces start with the headline) |
| A9 "arms" against "candidate policies" | **Partly:** the headline says "7 candidate policies tested" ("policies" stays the defined term); v6's chapter's "among 7 arms" is outside the brief's opening and comparison: open item §10.3 |
| A10 contract §9's "a forecast of future profit" | **Adopted** in "What the result is not" |
| A11 no grid fees stated | **Adopted** in C1101 |
| A12 the 10 days of the span outside P-all | **Kept:** "eligible" is defined in Product results directly above; a count of 10 is no committed record |
| A13 totals at six figures | **Kept:** no clause caps a total; the chart's axis is in thousand EUR |
| A14 `business.measured`'s "how to size that allowance" | **Kept:** the risk-aware variant trades only when the spread holds under cautious prices; it does not size an allowance for misses |
| A15 the `evidence/pres-7` label date and link | **Adopted:** the date is set to the evidence tip's at the final build and checked by the return and §8.2; the link answers 404 until the tag is pushed with `main` (§8.3) |
| A16 the status-word lint scans only the claim layer's root block list | **For the Integration check;** `test_52` covers PRES-7's blocks. Extending the lint would also flag the pre-existing "may still be revised" in How the product works: open item §10.3 |
| A17 why the Owner had v6 run early | **Kept:** optional (not in O51 item 8) |
| The reviewer's note on `tests/cp29/test_claims.py` | O63 (§10.1), recorded beside the brief |

**The fresh reader** (`fresh-reader.md`, the page at `5575920c`; 38 desktop and 67 phone screens; the six questions of
§10.2 and the brief's two). Answers 1–5 agree with the records, and answers 7 and 8 with CP-29's records and the
page's limits. Repaired after the reading: C1104 names "v5's last four test periods (the eligible days inside them)";
C1202 says the missing hour is "by design (its input rules fail closed there)". The rest answered or outside PRES-7's
sections (§10.3 item 4), each listed in the record.

**Integration review 1** (`integration-review-1.md`, **PASS** at the candidate `364ac020`; a fresh agent that wrote
none of PRES-7; it re-derived the three series from `daily.csv` and the six drawn polylines exactly, checked all 44
bound `cp29.*` values, the paths, the guards, the browser matrix at the candidate's page and §8's commands; a usage
limit paused it, and it resumed at the same candidate). Its four packet notes, fixed in the final candidate:

| Note | Disposition |
|---|---|
| §5's "as rendered" table predates the editorial fixes, and its README list omits the class caveat and C1202 | **Fixed:** the table is regenerated from the claim layer as the final build renders it; the README list is complete |
| §3 names C1103 as the only reworded CP-29 claim | **Fixed:** C1101, C1102, C1103, C1104 and C1108 (the claim map already recorded each) |
| §7's binding row names three changed `src/delu_forecast/` modules | **Fixed:** four, `research.py` included; all four are among PRES-5's recorded modules, so the conclusion stands |
| §10.2 points to a prerelease row §7 lacked; §7's browser figures were measured on the previous page | **Fixed:** §7 records the prerelease at the candidate and the release check at the final page (whose bytes equal the candidate's) |

The review's note on its own full-suite run (15 failures and errors in `tests/test_22`, which needs the browser payload
CI builds first) is reconciled by the prerelease, which builds it as CI does (3,501 passed, 17 skipped).
