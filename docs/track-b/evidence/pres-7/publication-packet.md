# PRES-7 publication packet

**PUBLISH_RULES 1.5 §§5.1a, 6 and A8 (O46), with decision 30 superseding §5.2's page budget; the brief
`docs/track-b/evidence/pres-7/issued-brief.md` (SHA-256 `b6a45b60…1175`); the packet template
`docs/track-b/publication-packet-template.md` (`4049c3e1…d01a`); the economic contract
`docs/track-b/economic-policy-contract-2026-11-15.md` (`21a92085…0889`), §§6, 8 and 9.** This section, §0, was
committed before the profit chart was drawn or any of PRES-7's text was written; the rest of the packet follows the
template once the build exists.

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
