# CP-28 implementation readings — committed before any arm runs on stored forecasts

**Authority.** `capstone_v21.md` v21-r17 §24.8 and the frozen protocol
`docs/track-b/evidence/cp-26/cp28-frozen-protocol-v21-r14.md` (`2b9286b0…7a8`). This note adds no
rule. It records how `src/cp28/` reads the places where the protocol leaves arithmetic, ordering or
bookkeeping to an implementation. Every reading below follows the protocol's text or CP-26's own
landed conventions. None was chosen from an outcome: when it was written, no CP-28 arm had produced
a forecast on CP-26's ledger, and no CP-28 loss, coverage, ratio or test existed. The Lead had read
CP-26's stored v2/v4/v5 scores for the r17 GFS note (committed `9165c77`) and the CP-26 report's
GFS+6 intervals. Neither informs anything here. Had the protocol been found deficient, it would have
been returned as BLOCKED; nothing found needs that.

## Inputs (protocol §§1–2)

- **Members** come only from CP-26's nominal forecast ledger, through `cp28.reader`. Each of its
  2,441 files is checked against `scores-manifest.json` as it is read, and all were bound at entry
  three ways (`entry-identity.json`). The members use CP-26's own arithmetic
  (`cp26.replay._learning_members`): `c_HG = A1_w/2 + B2_w/2`, bit-identical to CP-26's v3 native
  central (checked on every date); `L = L-N/2 + L-R/2`; `D2` = DDNN-2's stored median.
- **A member is valid** when its CP-26 status is `ok`, its vector is finite on every issuance key,
  and its lineage issue instant equals the frozen D−1 11:00 Europe/Berlin instant. The date must
  also carry the ledger's single protocol identity and its own target-day embargo.
- **A1's own quantiles** are D2's stored seven quantiles, finite and ordered, with the median equal
  to the stored D2 central.
- **The control's forecast** is CP-26's emitted v5 quantiles on the frozen keys, exactly as CP-26
  scored them. On CP-26's own H-shortage dates those are its B0 copy. **B0's forecast** is CP-26's
  emitted B0.
- **The issuance scale** is the A1 price scale that CP-26 stored with that date's valid H centrals
  (≥ 1 EUR/MWh).
- **Outcomes** come from `data/snapshot.parquet` (`7dd2dc73…`), behind the CP-25 boundary guard.
  During the replay they are reachable only through `engine.Truth`, which raises on any key whose
  delivery date is after D−2. They are read for scoring only after the forecasts are committed.
- **The replay** starts at the ledger's first date, 2020-01-01. Learning rows and own errors begin
  at the first complete date with all three native members. No earlier date is invented.

## Arithmetic and order (protocol §4)

- **Weighted central:** `(w_HG·c_HG + w_L·L) + w_D2·D2`, left to right in float64. The grid
  objective and the deployed arms use this same expression; A4, A5 and A7 apply each hour's block
  weights.
- **Grid points:** `(i, j, 100−i−j)/100` as float64, never rounded.
- **A date's grid loss:** hourly absolute errors summed one hour at a time in canonical-UTC order,
  then divided by the date's actual hour count, or the block's for A4.
- **The objective:** the window dates' losses summed one date at a time in ascending order, then
  divided by the number of dates.
- **Exact ties:** float equality, then the protocol's integer distance, then the lowest index. With
  every point tied, three points sit at integer distance 24 and (0.66, 0.17, 0.17) wins.
- **Shared fits and deployment:** A3 and A6 share one grid fit; A5 and A7 share one network fit and
  one scaler. A4 borrows A3's deployed vector. Shrinkage is `0.5·fit + 0.5·w0` (A3, A5) or
  `0.25·block + 0.75·A3_deployed` (A4), computed elementwise in float64.

## The meta-learner (protocol §5)

- **Rows and padding.** One row per (window date, block), ordered by date and then
  night/solar/shoulder-peak. Block hours are padded to 9; padded positions carry zero weight and a
  zero subgradient.
- **Error features at origin s.** The CP-28 learning rows released by s (every complete
  all-member-valid date ≤ s−2), averaged over the last 7 or 28 such dates. A shorter prefix is used
  when that is all there is, and 0 when there are none.
- **When features are built.** Each date's features are computed at its own origin, during the
  replay, and stored. A training row reuses them; nothing is recomputed as known at D.
- **Price states.** CP-26's rules, recomputed from the snapshot for every origin, including the
  2020 warm-up. A fully known day has all its canonical hours, and its documented D−1 13:00
  publication falls strictly before the issue instant. The rolling SD is a two-pass `std(ddof=1)`
  over each 28-day window. A forecast run cross-checks these states against CP-26's
  `known_price_states` table on the scored calendar and records the agreement.
- **Scaler.** Weighted mean and SD use `numpy.average` with row weights `H_sb/(n·H_s)`.
- **Moments.** Adam uses `(1−β1)` and `(1−β2)` as float64 differences.
- **Fixed matrix products.** Matrix products use NumPy's BLAS with one thread. A rerun on the same
  machine reproduces every parameter hash. Another BLAS build may differ in the last bits.

## H layers, startup and failures (protocol §§6–7)

- **The H layer** is the landed `cp16.residuals.SharedResidualState`. It is fed the arm's central as
  both of its blend arguments, exactly as CP-26's v5 used it, with the same `c/2 + c/2 == c` check.
  Each combined arm owns one.
- **Order at each origin:** release ≤ D−2, then fit, then issue, then register D's central and D's
  learning members as pending.
- **Fallback order.** For A1: the common-member check, then its own quantiles, then v5, then B0.
  For combined arms:
  1. the common-member check (→ v5, then B0);
  2. a solver failure (→ A2's complete emitted forecast, whatever A2 emitted);
  3. a missing scale or an invalid central (→ v5, then B0);
  4. H not ready, or a numerical H failure (→ v5, then B0).
  
  Only a valid native central on a complete date, issued before its outcome and with no numerical
  failure, enters the arm's buffer.
- **Warm-up dates** before 2020-12-29 are never scored. They emit no fallback copy, and an arm
  whose H is not ready records `central_only`.
- **Dates with no frozen eligible keys** (CP-25's ten exclusions) record `no_scoring_keys` and
  enter no paired comparison.
- **Startup labels.** `startup_w0` labels a learned arm before its minimum history. It is a native
  rule, not a fallback. A4 records `a3_deployed` between 364 and 728 dates.

## Inference (protocol §§8–9)

- **Population.** The paired population of each arm is the set of dates where both it and the
  control have finite daily losses. It is fixed before any test.
- **Cells.** Overall endpoints use all paired dates and have no 90-date floor. Year cells are
  calendar years 2021–2025, so 2020-12-29..31 enter no year cell, though they join 2021's stratum.
  Season cells pool every year, including those three DJF dates and 2026's partial dates.
- **Draws.** One `rng.integers` call per computable endpoint, shape (replicates, blocks), as in
  CP-26's `draw_plan`. A required cell below 90 dates, or an uncomputable endpoint, consumes no
  draw. `tests/cp28` checks the draw plan and HAC variance against CP-26's functions on synthetic
  data.
- **Descriptive ratio intervals** (to the control and to B0) reuse the primary overall endpoint's
  stored resamples for that arm and metric, and keep every pivot. They are not tests and select
  nothing.
- **Selection WIS** is each passing arm's mean daily WIS over its paired dates with the control.
