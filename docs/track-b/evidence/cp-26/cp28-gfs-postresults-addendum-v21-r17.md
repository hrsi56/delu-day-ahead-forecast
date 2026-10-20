# CP-28 companion — post-results GFS analysis, v21-r17

**Identity:** `cp28-gfs-postresults-v21-r17`, approved 2026-10-19. This is a new descriptive
analysis contract written **after** CP-26 outcomes were inspected. It does not replace or
retrospectively edit the outcome-blind experiment in `cp28-frozen-protocol-v21-r14.md`
(SHA-256 `2b9286b0e948f59f97de33315a8b4fb3ef121003fc4ba82355b1ccf6585497a8`).
Authority: capstone v21-r17 §§24.5/24.8 and `docs/track-b/cp-26-gfs-ruling-2026-10-19.md`.

## 1. Scope and timing

Produce one bounded descriptive note before CP-28 execution, using only preserved CP-26
forecasts, daily/hourly scores, already computed inference and CP-25 availability records.
Start with the small daily tables; read hourly/member artifacts only for the stated breakdowns
when already available. Approximate analysis timebox: one hour, then report available findings
and missing evidence rather than opening a repair program. Use at most one local CPU worker,
BLAS 1, the existing environment and applicable elapsed-time/RSS accounting; retain all prior
charges and reserves. Do not claim this work is free of compute merely because it needs no fit.

**No retraining or scientific regeneration:** no CP-26 search, member fit, forecast replay,
CP-28 combiner/grid/network fit, H-buffer replay, interval recalibration, new bootstrap/test
family, download, dependency change or new scored decision policy. Reuse existing uncertainty
only where it matches the exact comparison/population. Otherwise report point summaries with
that limitation. The note is development/post-selection exploration, not a fresh confirmation.

This document defines the approved work; its amendment task does not claim the analysis note
is already completed. The CP-28 executor can produce the note as a small pre-execution task
under its issued brief. Missing support or an unfavorable finding is reported without tuning
or adding a success gate. The original seven-arm experiment remains intact.

## 2. Daily differential and concentrated risk

For v4 and v5, form paired daily `loss(GFS+6) − loss(nominal)` separately for MAE and WIS,
with absolute EUR/MWh differences and ratios of paired mean daily losses. Keep CP-25's frozen
keys, actual DST hours, equal date weights and all scored fallback losses. Disclose paired
counts, missing pairs and fallback status; never remove a date for its observed loss. Do not
average daily percentage errors with unstable denominators.

Report all four original masks separately, then existing year, season, three hour-block and
issue-time-known state breakdowns where stored support permits. Join the frozen CP-25
GFS+6 affected/unaffected-date classification by delivery date. These flags represent the
documented-schedule stress test, not measured live failures. If classification or exact keys
cannot be recovered from existing records, state the gap and omit that slice.

Distinguish direct input unavailability from propagated history effects: the delayed route
has its own training/search and residual history. A difference on an unaffected issuance
date can arise from that history. This analysis cannot isolate those mechanisms causally
without another experiment; it must not claim to do so.

Compare the preserved weather-independent nominal v2 with nominal and GFS+6 v4/v5 on the
same available keys/dates. Report its regular-day accuracy cost and stress-scenario tradeoff.
Inspect existing component losses only if stored definitions match; do not manufacture an
HG/L/D2 quantile stream from central values or substitute component central MAE for emitted
p50 MAE. An ex-post best-model envelope, if shown, is an **oracle descriptive bound**, never
an implementable strategy or a selection result.

## 3. Insurance cost and break-even scenarios

For each compatible paired population and metric, let N be the mean nominal v4/v5 loss,
S the mean loss of its complete GFS+6 route and B the mean preserved v2 loss. Show the
planning mixture `L(p)=(1−p)*N+p*S` at p=0, .01, .05, .10, .20, .50 and 1, with B beside it.
This mixes two complete historical regimes algebraically. **p is a scenario weight, not a
measured late-day frequency**, and this is not a chronological replay of occasional delays.

When `S>N`, show `p*=(B−N)/(S−N)` only if it lies in [0,1]; otherwise say no crossing in that
range. Handle `S=N` and `S<N` explicitly rather than inventing a break-even value. Keep MAE
and WIS conclusions separate. With non-random lateness, realized costs depend on the dates
affected; show the affected-date summaries separately and do not translate the all-calendar
14–17% stress deterioration into a universal per-late-day penalty.

This is an accuracy-cost comparison, not trading profit, monetary business value or proof
that v2 is the best operational fallback. Existing intervals do not automatically supply
uncertainty for p*. Do not estimate actual arrival probabilities from CP-25's shifted schedule
counts or fetch new data; those probabilities await the planned live availability measurements.

## 4. Decision-policy recommendation, without fitting one

Use the preceding findings to recommend whether a later simple rule merits an experiment:
use weather-based forecasts when valid inputs are available strictly before issue time, and
a separately validated alternative when they are not. Any richer rule could use only inputs
observable at issuance (for example actual availability, age and released historical errors),
never same-day realized losses or knowledge of the best model in hindsight. Preserve the
fixed issuance deadline; this proposal does not authorize waiting past it or a previous-run
weather fallback.

Do not fit a gate, optimize its thresholds, select a fallback from the full-calendar scores,
splice saved quantiles and claim validation, or deploy anything. A future switching policy
changes its error history and interval calibration, and requires separate prospective
registration, causal evaluation and Owner authority. It is not an eighth CP-28 arm and
cannot replace nominal v5 through this descriptive note.

## 5. Output, custody and CP-28 boundary

Write a short note plus a small machine-readable table under a new, separately named evidence
directory, preserving original output bytes. Identify source paths/hashes, populations,
definitions, counts, calculations, unsupported questions and the post-results evidence class.
Record actual analysis resources under the issued authorization without resetting any ledger.
No broad new testing program is required; check the joins, paired counts, aggregation and
mixture algebra against the small source tables.

The original CP-28 nominal members/control, A1–A7, sixteen meta-learner inputs, learning rules,
own-error layers, one-look rule, twenty endpoints, four Holm families and selection remain
unchanged. Do not run arms on GFS+6 streams, add availability features, add a new hypothesis
family or use this note to select among CP-28 arms. The registered combiner fits in CP-28
are a later authorized experiment, distinct from retraining CP-26 members and from this note.

CP-26's completed baseline PASS is preserved. Owner LAND and later CP-28 confirmation/brief
remain required. The GFS classification remains fragile, all revision/selection limitations
stay disclosed, and CP-18 retains its already planned live availability measurement. No new
publication, live-activation or operational-robustness claim is made.
