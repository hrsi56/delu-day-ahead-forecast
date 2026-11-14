# PRES-6 publication packet

**PUBLISH_RULES 1.5 §11 and A8 (triggered, ruling O46); the brief `docs/track-b/evidence/pres-6/issued-brief.md` (SHA-256
`bdb78f02894896d2ee1f249355d23351f972cdb217d4d906d22561172f40e5f6`); the packet template
`docs/track-b/publication-packet-template.md` (`4049c3e1…d01a`).** This section, §0, was committed before any product
result was computed; the rest of the packet follows the template once the results exist.

## §0. Rules fixed before the computation (the brief's outcome 2)

Everything below is decided before any of the numbers it governs is computed or drawn. Nothing is fitted; no other
policy is recomputed. Every value the page shows is derived from committed rows and re-derived by a `--check`.

**The policy and its artifacts.** v6 (A1 in the frozen records; policy `720fc581…`), as CP-28 stored it:
- forecasts: `reports/cp28/forecast/hourly.parquet` (`f5cb02a1…f638`), arm `A1`;
- daily losses: `reports/cp28/results/daily-losses.parquet` (`7e9c972f…b85d`), stream `A1`, with the similar-day naive
  as the reference (stream `B0`);
- observed prices: CP-24's committed rows `reports/ddnn2/attempt-1/predictions.parquet` (`9d3f539f…5cf9`), column
  `y_true`, joined to v6's stored quantiles by delivery hour exactly as PRES-5's `final_candidate.py` joins them.

**The populations.**
- **P-all:** every eligible development day, 2020-12-29 to 2026-09-06, 2,068 days, 49,596 scored hours: the days CP-26
  scored and CP-28 selected on. Every daily figure comes from `daily-losses.parquet`; none is recomputed from hours.
- **P-v5:** the subset of P-all inside v5's five test periods: folds 2–5, 358 days (2021-04-01 to 2021-06-29,
  2022-07-01 to 2022-09-28, 2025-05-01 to 2025-07-29, 2026-01-08 to 2026-04-07), where committed hourly observed prices
  exist. Fold 1 (2020) lies before P-all and is left out.

**The regimes** (§5.1 subject 2, as the page already states them): pre-crisis, 2020-12-29 to 2021-08-31 (246 days of
P-all); the energy crisis, 2021-09-01 to 2022-12-31 (481); the market with frequent negative prices, 2023-01-01 to
2026-09-06 (1,341).

**Forecast against observed.**
- **Days, chosen by a rule:** for each regime, among the days of P-v5 in that regime, the day whose v6 daily MAE
  (from `daily-losses.parquet`) is the regime's median, taking the lower of the two middle days when the count is even.
  One day per regime, three in all. Each is drawn as v6's median with its 50%, 80% and 95% intervals against the
  cleared price, in EUR/MWh, by local hour.
- **The whole-population view:** every scored hour of P-v5, grouped into ten bins of equal count by v6's median
  forecast. For each bin: the mean median forecast, the mean observed price, the number of hours and the share of
  hours inside the 80% interval.

**Error over time.** The daily MAE and the daily interval score (WIS, the committed definition) of v6 and of the naive
on every day of P-all, drawn as their calendar-month means; every day counts once, no smoothing. The daily rows stay
in the committed output.

**Error by regime.** For each regime and for P-all: the number of days and scored hours; the mean daily MAE and WIS of
v6 and of the naive; and v6's ratio to the naive. 95% intervals from a non-circular moving-block bootstrap over the
regime's days, blocks of 14 consecutive days, 2,000 replicates, seed 20261114, resampling v6 and the naive on the same
days (the ratio's interval from the same draws). A regime with fewer than 60 days would be stated as thin; none is.

**Coverage with width.** For each nominal level, 50%, 80% and 95%, for P-all and for each regime, for v6 and for the
naive: coverage, the scored-hour-weighted share of hours inside the interval, and width, the scored-hour-weighted mean
interval width in EUR/MWh, both from `daily-losses.parquet`. The nominal level is drawn as a reference, never as a
target.

**Explanation or sensitivity.** No committed explanation of v6 exists. CP-28's stored `networks.npz` and
`features.parquet` belong to the small-network blend arms (A5, A7): their inputs are member error statistics and their
outputs are blend weights, so they cannot explain v6, which is DDNN-2 alone. The source and method are the subject of
an Orchestrator ruling requested on 2026-11-14 (proposed: the frozen §19.7 method, exact baseline Shapley over the 11
input groups on the issued median, by inference only, from CP-18b's committed A1 artifact for development day
2026-09-05). Until that ruling and its own pre-registration here, nothing is computed; if neither fits, the section
states the gap.

**Evidence class.** Development, post-selection on every figure: v6 was selected on P-all (CP-28). Nothing
prospective: the report shows no live forecast, score or price, and says that the Space shows the live record,
"prospective evaluation in progress".
