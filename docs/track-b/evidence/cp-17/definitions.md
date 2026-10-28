# §19.5's definitions, frozen at CP-17 before the fresh-data test

**Authority:**
- `capstone_v21.md` v21-r17 §19.5 (section `1d47a505…`);
- the Owner's decision 8 (τ = 10 EUR/MWh) in `docs/track-b/pre-cp-17-rulings-2026-10-25.md` (`d29b0abc…`);
- the brief's item 5 (`9f235cf8…`).

**Implementation:** `src/cp17/scoring.py`, the one implementation:
- the pipeline computes the committed evaluation records with it natively;
- the Space recomputes them with it in the browser.

**Tests:**
- `tests/cp17/test_units.py`, on synthetic inputs;
- `reports/cp17/scoring-check.json`, on two development windows computed natively and recomputed under the
  issuing host.

**Nothing here was chosen after seeing an evaluation outcome.** Every value was fixed beforehand:
- τ is the Owner's;
- the 28-day window and the 1e-9 tolerance are the brief's, as proposed in the Space plan (§4.6, §4.7) before
  any result;
- the scoring check ran after the module was written.

## Inputs and what is scored

A window's input is a set of issued days and the published outcomes:
- **an issued day** has its UTC keys and the seven emitted quantiles at levels .025, .10, .25, .50, .75, .90
  and .975;
- **the published outcomes** map each key to a price.

What is scored:
- **A scored hour** is an issued key with a published price.
- **A missing price is unscored.** That covers a price not published, and one not yet published (pending).
- **A day with no published price is unscored and counted as pending.**
- **Zero and negative prices count as they are.** No measure divides by a price.
- **Partial days score their published hours.** Each day shows its completeness: scored hours over its
  canonical hours (23, 24 or 25).

## The measures

| Measure | Definition | Aggregation over a window |
|---|---|---|
| MAE (EUR/MWh) | \|y − p50\| per scored hour | each day's mean over its scored hours; days weigh equally (§24.7) |
| WIS (EUR/MWh) | §24.7's seven-quantile WIS: `[0.5·\|y−q50\| + Σ_α (α/2)·IS_α] / 3.5`, α = .50, .20, .05, `IS_α = (u−l) + (2/α)(l−y)·1[y<l] + (2/α)(y−u)·1[y>u]` (`cp28.scoring.hourly`) | as MAE |
| **The percentage measure** | 1[\|p50 − y\| ≤ τ] per scored hour, **τ = 10 EUR/MWh**, inclusive | the share over all scored hours of the window, pooled; the denominator is the scored hours with a published price |
| Coverage per band | 1[l ≤ y ≤ u], inclusive, for 50% (p25–p75), 80% (p10–p90) and 95% (p025–p975) | the share over the window's scored hours, with the counts |
| Width per band | u − l | the mean over the same hours |
| Rolling coverage and width | as above | **the last 28 scored delivery days** ending at each scored day, pooled over their hours |
| Reliability diagram | for each level q, 1[y ≤ the q forecast] | the observed share per level, with the counts (at or below, scored hours) |
| Quantile-band PIT | the band of y among the eight bands the seven levels define: (−∞, q.025], (q.025, q.10], …, (q.975, ∞) | the count and share per band, against the nominal shares .025, .075, .15, .25, .25, .15, .075, .025 |

**Ties.** A price equal to an emitted quantile falls in the band that quantile closes, so the PIT agrees with
the reliability diagram's "at or below".

**Labels:**
- **The percentage measure** is "share of scored hours within ±10 EUR/MWh of the published price". It is never
  called accuracy, and never expressed relative to a benchmark. A figure relative to a benchmark is
  improvement, not correctness.
- **Coverage** is worded "nominal 80% interval; measured coverage x% over <window>; mean width w EUR/MWh"
  (Space plan §4.7). It is never "80% confidence".

**B0 as context.** The Space shows the same measures for the similar-day naive, B0, labelled as a reference
and not a target.

## The recomputation check

The Space recomputes every metric of a window from the shipped issued forecasts and outcomes, and compares
it item by item with the committed record (`scoring.recompute_check`):
- **Counts:** an integer in the committed record must be matched exactly.
- **Reals:** a real a matches its committed value b when |a − b| ≤ 1e-9 · max(1, |b|).
- **Strings and flags** must be equal.
- **Mismatch:** a missing or extra item is a mismatch. Any mismatch is shown with both values ("✗") and
  blocks that day's publication, as a product failure.

A count's committed type decides, not the recomputed value's type, because a JSON hop through JavaScript may
write 1.0 as 1. The value is unchanged; only its type is lost.

## Evidence

- **Native against the issuing host.** On 2025-10-01 to 2025-11-30 and 2026-03-01 to 2026-09-06, A1's and B0's
  development records were computed natively and recomputed under Pyodide in Node.js.
  - They match on every item: 2,536 and 7,696 items per policy.
  - They are bit-identical.
  - The windows include a 25-hour and a 23-hour day, 489 negative-price and 11 zero-price hours, and three
    partial days each.
  - Record: `reports/cp17/scoring-check.json`. Its numbers are development post-selection and descriptive.
    They are not part of the definitions.
- **The unit tests:**
  - τ is inclusive;
  - missing, zero and negative prices;
  - pending days, equal date weights, completeness and partial days;
  - the PIT's ties and band counts, coverage, widths and reliability;
  - the 28-day window;
  - the recomputation tolerance.
