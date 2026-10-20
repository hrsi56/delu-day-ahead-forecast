# CP-28 frozen protocol — outcome-blind registration in CP-26

**Protocol identity:** `cp28-stored-forecasts-v1`. This document specifies the future experiment;
it does not authorize CP-28, run an arm, or report a result. The CP-26 Lead commits its exact bytes
on `gauntlet/cp-26` before the first CP-26 score. Its SHA-256 and commit SHA are recorded by the
Lead in the freeze record. No forecast, target value, loss, coverage, ratio, test result, or
CP-26 outcome was inspected to choose the details below.

**Authority:** `capstone_v21.md`, v21-r13, §§24.7–24.8, governed by §§2, 14.2, 24.2, 24.4 and
24.5; anchor SHA-256 `173799d818387b9d82db16b9ccd7195afaebbea8e11259809e4a8b704bd525a8`.
The binding tier ruling is `docs/track-b/cp-25-rulings-2026-10-12.md`, SHA-256
`c7af67f88157277aafd8dd2b1b49e12a1d9ff4b747ca5bdf178fac664fba53c1`.
The issued CP-26 brief is `docs/track-b/evidence/cp-26/issued-brief.md`.

**Distinction:** sections 1–3 and 8 retain the anchor's experiment and decision rules.
The calculation, ordering, startup and failure conventions in sections 4–7 and 9–10 prospectively
resolve implementation details the anchor leaves open. None changes the seven arms, thresholds,
minimum histories, control, one-look rule, or authority gates. An incompatibility with the anchor
is a deficiency to return, never permission to edit this registration after seeing a result.

## 1. Entry, custody and scope

CP-28 requires CP-26's LAND, the Owner's confirmation after CP-26, and its issued brief; its own
LAND remains a later Owner action. Confirmation decides whether this experiment runs, not what
it tests. The frozen protocol lands with CP-26 and is discarded with CP-26 if that checkpoint is
discarded. The proposed CP-28 ceiling is 40 machine-hours, subject to its issued authorization.
No CP-28 fit, arm execution or score is authorized by CP-26.

Only CP-26's nominal forecast ledger supplies the members. The CP-26-ledger identity and hashes
are bound at CP-28 entry without changing this protocol. No new member fit, new source, new
search, new arm, alternative shrinkage, or outcome-selected implementation is allowed. Delivery
days after 2026-09-06 remain closed. The no-load variant and GFS-delay run are descriptive and
cannot supply a member or replace the control.

The control is **nominal v5 as landed, including the load forecast**, under ruling §1. Its central
weights are `w0 = (2/3, 1/6, 1/6)` and its own interval layer remains unchanged. Disclose the
load-history revision risk, target-price tier-2/SMARD caveat, and the accepted timing risks.
The evidence class is `development_post_selection`; CP-28's conditional Holm control does not
make the development calendar fresh. A1's forecasts have already appeared descriptively in
CP-26, and the Owner's decision to run CP-28 follows that report. 4.7T carries the protection.

## 2. Calendar, causal chronology and ledger validity

The scored population is CP-26's frozen eligible delivery calendar from 2020-12-29 through
2026-09-06, against the same CP-25 exclusions. No date is removed because of an observed loss.
The warm-up is 2020-01-01 through 2020-12-28 and is never scored. All eligible scored days are
the primary population. The other CP-26 masks and its year, season, quarter and diagnostic
breakdowns remain descriptive; they do not add gates or change selection.

Each date contains its actual canonical 23/24/25 UTC observations, with Europe/Berlin local-hour
labels. Preserve both repeated autumn hours and leave the spring hour absent. The issue instant
is D−1 11:00 Europe/Berlin: 10:00 UTC in CET and 09:00 UTC in CEST, using D−1's offset.
Inputs must be published strictly before that instant. No target-day price or revealing
same-auction transformation enters any predictor or preprocessing statistic.

At origin D, release a forecast/error date s only if s ≤ D−2 and the complete delivery-day
outcome is available. Consume each issued pair once. Learning inputs, scaler statistics and H
residuals must be reproducible from that historical information set. D−1 price predictors do not
grant D−1 forecast-error feedback. Assemble the issue-time inputs and forecast before adding D's
outcome to any ledger.

The three central members, in this fixed order, are:

1. `c_HG`: nominal v3's central forecast before its H residual-median adjustment;
2. `L`: the arithmetic mean of native L-N and L-R central forecasts;
3. `D2`: nominal DDNN-2's native median.

An all-member-valid date requires each member to have a finite native forecast at every expected
canonical key, matching issue time, input/protocol identity and origin. L requires both L-N and
L-R. A substituted B0/control forecast, failed fit, missing key, duplicate UTC key, nonfinite
value, invalid ordering or identity mismatch is not a native member. A1 additionally requires
D2's finite ordered native seven quantiles. Status flags determine validity, not whether a value
happens to equal a fallback vector. Outcomes must likewise cover every actual canonical hour
before a date becomes a released learning row.

For A3–A7, the learning window is the **latest at most 728 all-member-valid released ledger
dates**, not a 728-calendar-day slice. Gaps can lengthen its calendar span. It is shared by A3,
A4, A5, A6 and A7 at D. Count unique delivery dates, not hours or block rows. Dates earlier than
the CP-26 warm-up are not invented. Record available-day count, oldest date, latest date and
calendar span at every origin. This window is distinct from each arm's 28-date H buffer.

## 3. The seven arms — no additions

| Arm | Fixed construction |
|---|---|
| A1 | DDNN-2 alone with its own Johnson SU quantiles; no H layer or learned combination. |
| A2 | Central weights `(1/3, 1/3, 1/3)`; its own H layer. |
| A3 | Global step-0.01 simplex-grid central-MAE fit on the latest at most 728 valid released dates; minimum 364. Deployed weights `0.5*fitted + 0.5*w0`. Before 364: `w0`. |
| A4 | Separate grid fits for night, solar and shoulder/peak on that same window; minimum 728. Deployed block weights `0.25*block_fitted + 0.75*A3_deployed`. Before 728: A3's deployed weights. |
| A5 | Daily-from-scratch NumPy 16→8 tanh→3 softmax meta-learner; minimum 364. Deployed weights `0.5*network_output + 0.5*w0`. Before 364: `w0`. |
| A6 | A3's same fitted grid vector, with no shrinkage. Before 364: `w0`. |
| A7 | A5's same fitted network output, with no shrinkage. Before 364: `w0`. |

A3 and A6 share one fit. A5 and A7 share one fit and one training scaler; only deployment
shrinkage differs. A4 borrows **A3's deployed** vector, never A6's. Each combined arm A2–A7
owns a separate causal H buffer and emits the H layer's seven quantiles. Its emitted p50 may
differ from its weighted central forecast; score the emitted p50. A6 and A7 can reach 100% on
one member. They receive the same gates, and are explicitly exposed to overfitting and regime
lag. All learned arms use `w0` until their minimum history exists. A4 equals A3 until 728 valid
dates exist, so its early/2021 cell tests A3's weights to that extent.

The fixed local-hour blocks are night 22–05, solar 10–16, and shoulder/peak 06–09 plus 17–21.
Each actual hour belongs to exactly one block. Repeated local 02:00 observations both belong
to night; the absent spring observation is not synthesized.

## 4. Grid objectives, ties and arithmetic

Enumerate all 5,151 points as integers `i=0..100`, then `j=0..(100−i)`, with
`w=(i,j,100−i−j)/100`. This is the anchor's lexicographic ascending `(w_HG,w_L)` order;
the index is zero-based in that enumeration. No coordinate rounding or grid refinement occurs.

For A3/A6, minimize the mean across window dates of the mean absolute weighted-central error
over that date's actual hours. For an A4 block, use the mean across window dates of the mean
absolute error over that block's actual hours. Thus each date weighs equally, including DST
dates; pooled hourly weighting cannot change the choice. Historical member forecasts are used
as issued, not regenerated under today's member state.

Compute deterministic float64 losses in ascending delivery-date and canonical-UTC order. An
objective tie is exact equality of the computed objective, with no epsilon or practical tie band.
Break it by minimum squared Euclidean distance to `w0`, then minimum grid index. For exact
distance ties use the integer comparison
`(6*i−400)^2 + (6*j−100)^2 + (6*(100−i−j)−100)^2`, which is proportional to that squared
distance and avoids rounding the nominal thirds. A4 uses this same nominal-v5 distance rule,
not distance to A3. The 0.5% selection tie in section 8 is a separate rule.

## 5. Causal sixteen-input meta-learner

Use the following column order: HG 7-date MAE, HG 28-date MAE, L 7-date MAE, L 28-date MAE,
D2 7-date MAE, D2 28-date MAE, high-volatility flag, negative-price-risk flag, volatility-unknown
flag, DJF/MAM/JJA/SON one-hot, night/solar/shoulder-peak one-hot. No extra input or target
transformation is permitted. Fit one network across all three blocks; its output is evaluated
once per day/block and then used for every canonical hour in that block.

For the six error features at historical origin s, calculate each member's daily mean absolute
**central** error over its actual hours, using only common all-member-valid dates released by
s−2. Average the last 7 or last 28 such daily errors; do not use calendar interpolation, emitted
H p50 errors, or outcomes later than s−2. If fewer than the requested number exist, use the
available prefix; if none exists, encode zero. This fixed startup convention adds no input flag
and does not discard the first warm-up rows. Log feature-support counts. Training at D rebuilds
each row's features as known at its own issue, never as known at D.

The two price states use complete price vectors published strictly before the historical issue
instant, including D−1 when fully available as a price predictor. They do not use D−1 forecast
errors. Negative-price risk is 1 if any canonical hour in the latest 7 fully known delivery-price
days is negative, else 0. With fewer than 7 known days, use the available prefix, and with none,
use 0; report support. For volatility, form each known day's actual-hour mean price; compute
the sample SD (`ddof=1`) of the latest 28 such means. Compare it strictly with the linear 90th
percentile of the preceding 365 rolling-28-day SD values, excluding the current SD. Require
all 28 means and all 365 reference values; otherwise high-volatility is 0 and volatility-unknown
is 1. Historical price gaps are skipped as fully known-day gaps, with span recorded. The
unknown flag is 0 when supported, including supported states that are not high.

At D, the fit uses one row per retained date and block, with that date's native member hourly
vectors and released actual prices as targets. There is no validation split, early stopping,
checkpoint selection, hyperparameter search or transfer of yesterday's parameters. Let
`H_s` be the date's actual-hour count and `H_sb` its block-hour count. The data loss is

`(1/n) * sum_s sum_b (H_sb/H_s) * mean_{h in b}|sum_m p_sbm*c_smh − y_sh|`.

This is mean daily central MAE while retaining the anchor's within-block hourly loss. The three
block rows of a DST date receive their actual-hour proportions. The available window has at
least 364 dates before a fit is attempted and at most 728.

Standardize **all sixteen inputs**, including flags and one-hots, with the training window's
weighted mean and population SD (`ddof=0`), using the same row weights `H_sb/(n*H_s)`.
For an exactly zero SD use scale 1 after mean subtraction. Save the scaler; apply it to D's
inputs unchanged. No full-calendar statistic, future row or deployment-day input enters it.

Use NumPy float64, stable softmax by subtracting each row's largest logit, eight tanh hidden
units, and three outputs in the fixed member order. Initialize a fresh NumPy `default_rng` from
`SeedSequence([28,D.toordinal(),0x4D4C])`. Draw W1 of shape `(16,8)` then W2 of shape `(8,3)`,
in C order, from Normal(0,0.1); initialize both biases to zero. No additional RNG draw, retry
seed or jitter is used. A5/A7 use exactly the same parameter arrays.

The optimized objective is the data loss above plus
`1e-3*(sum(W1**2)+sum(W2**2))`. The penalty is not divided by row count; its gradient is
`2e-3*W`. Biases are unpenalized. Choose the MAE subgradient `sign(error)`, with 0 at an exact
zero. Train full-batch Adam for exactly 300 updates, learning rate 0.01, β1=0.9, β2=0.999,
ε=1e-8, moments initialized to zero, epoch counter 1 through 300 and usual bias correction:
`theta -= 0.01*m_hat/(sqrt(v_hat)+1e-8)`. Use epsilon outside the square root. There is no
gradient clipping, dropout, mini-batching or learning-rate schedule. Deploy the parameters after
update 300; no best-epoch selection. Any nonfinite input, loss, gradient, moment, parameter or
output, shape error, or inability to complete the fixed fit is a solver failure. A finite
softmax with nonnegative weights summing to one is required.

## 6. Own-error H layers and startup

For each combined arm, retain the most recent 28 complete released **native own-central**
forecast/error dates, all ≤D−2 and consumed once. Store
`r_sh=(y_sh−c_arm,sh)/s_s`, with `s_s` the A1 price scale available at that issuance: sample
SD of its 168 available canonical prices, floored at 1 EUR/MWh. Never renormalize an old
error with today's scale. At D use its own available `s_D`.

For quantiles `.025/.10/.25/.50/.75/.90/.975`, use linear empirical pooled residual quantiles
and local-hour residual quantiles, with equal canonical-observation weights. Hour shrinkage is
`n_h/(n_h+56)`, set to zero below 14 distinct complete dates at that hour. At weight zero use
the pooled quantile without evaluating an empty hourly quantile. Emit
`c_arm,Dh+s_D*(w_h*Q_h+(1−w_h)*Q_pool)`. Do not clip tails, apply isotonic repair, reset p50,
borrow the control's residuals, or use an in-sample residual. Preserve both repeated hours.

Warm-up can produce native **central-only seed issuances** before any complete H-quantile
issuance is requested. A seed requires all native member central forecasts, the causal weights
for that warm-up date, and the issuance's valid scale; its released own errors can establish
the first 28-date H buffer. It is explicitly a central-only warm-up issuance, never a scored
forecast or a fallback. No H quantiles or losses are claimed for it. Once complete H issuance
is requested, fewer than 28 supported dates is a failure under the fixed fallback hierarchy.
This seed phase never extends into the scored calendar. If CP-26's genuine warm-up ledger
does not provide support, report the deficiency; no scored-day seed exemption, hindsight
forecast, zero error, control residual, or fallback error may repair it.

A scored fallback or failed day contributes **nothing** to that arm's H buffer, even if an
unused central vector could have been calculated. A native prior issuance remains admissible
only when its complete outcome is released; record its provenance. Report buffer size, oldest
and latest date, represented calendar span and age on every origin. A frozen learned-weight
startup vector `w0` is a native rule, not an operational fallback, when all members and the H
history are valid. These distinct status labels prevent startup equality with v5 from being
mistaken for a substituted forecast.

## 7. Failures and accounting

Apply the hierarchy without renormalizing a subset of members:

1. A missing or invalid member makes the arm use that day's **complete nominal v5 forecast**,
   including its quantiles. Apply this common-member check to all seven arms; A1 does not
   become a different missing-member experiment.
2. If that control forecast is also missing or invalid, use the complete B0 forecast.
3. A solver failure when every member is valid makes the arm use the complete **A2 forecast**,
   including A2's own H quantiles. If A2 cannot issue natively, follow its control-then-B0
   fallback; never manufacture A2 quantiles.
4. An unsupported H history, unavailable scale or failed H construction follows control then
   B0. A native A1 with invalid own quantiles follows the same hierarchy.
5. If no prescribed complete fallback is available, record a failed issuance and retain its
   calendar row with missing losses. It is missing in every paired comparison involving it.

Fallback copies are scored as emitted and counted, by arm, reason and source; count multiple
causes once in the total-day count and retain cause flags. They are not native-member learning
rows or H-buffer errors. A per-origin solver failure with the prescribed scored fallback does
not erase the whole arm. An unexecuted arm or an arm whose registered stream/tests cannot be
computed receives compound p=1. A required inference cell below 90 complete paired dates is
inconclusive, also p=1. No failure is silently dropped from the fixed-calendar accounting.

## 8. Scores, twenty endpoints, Holm and selection

Each actual-hour p50 MAE is `|y−q50|`. For α=.50,.20,.05 use the interval score
`IS_alpha=(u−l)+(2/alpha)*(l−y)*1[y<l]+(2/alpha)*(y−u)*1[y>u]`.
The seven-quantile WIS is
`[0.5*|y−q50| + sum_alpha (alpha/2)*IS_alpha]/3.5`.
Average hours within date, then average dates equally. Fallback days enter these averages.
The primary loss is the arm's emitted forecast, not its unadjusted central combination.
Report raw daily losses and ratios to B0 alongside control comparisons. Retain all CP-26-style
mask and diagnostic outputs as descriptive, without selecting gates from them.

Against nominal v5 there are exactly **twenty required one-sided endpoints per arm**:

- two overall improvement endpoints, MAE and WIS, with daily differential
  `d=L_arm−0.995*L_v5` and H0 `E[d]≥0`;
- eighteen non-inferiority endpoints: MAE and WIS within each complete year 2021–2025 and
  each pooled season DJF/MAM/JJA/SON, with `d=L_arm−1.02*L_v5` and H0 `E[d|g]≥0`.

All cells use complete paired date losses; masks are set by calendar and forecast availability,
never by their values. Each required year/season cell needs at least 90 paired dates. Each
endpoint's alternative is strictly negative mean differential. Boundary equality is not an
improvement or non-inferiority rejection. The compound p-value is the largest of the twenty;
any undefined required endpoint or deficient cell sets it to 1. No endpoint correction inside
an arm is added: this is the anchor's intersection-union compound test.

For each analysis variant independently, sort all seven compound p-values ascending, breaking
equal p-values by arm number. Holm step-down compares position j=1..7 with `0.05/(8−j)`;
reject while `p<=threshold` and stop at the first failure. Equivalently report monotone Holm
adjusted p-values `min(1,max_{i<=j}((8−i)*p_(i)))`. Failed and unexecuted arms stay in the
seven-arm family at p=1. An arm passes only if Holm rejects it in the primary analysis **and
each** of the 7-day, 28-day and unstratified-14-day variants. A primary pass that fails any
variant is inconclusive and cannot be adopted. No later look or rerun seed rescues it.

Among passing arms, choose the lowest mean daily WIS on the fixed scored calendar using that
arm's complete paired dates with the control, with paired/missing counts disclosed. Loss
availability is frozen before test calculation; do not select a different comparison population
after seeing WIS. If best WIS is positive, the tie set is exactly passing arms with
`WIS_arm < 1.005*WIS_best`, including the best. If best WIS is zero, only exactly zero-WIS
arms tie. The simpler arm wins in the exact order **A1, A2, A3, A6, A4, A5, A7**. At exactly
0.5% above best the arm is not tied. If no arm passes, nominal v5 is the freeze candidate.

## 9. Prospective bootstrap and test semantics

Use CP-26's paired non-circular moving-block studentized bootstrap: primary block length 14
calendar days, 10,000 replicates, seed 20261012, and Bartlett HAC lag 14. The calendar-year
strata are 2021–2025 and partial 2026, with eligible 2020-12-29..31 joined to 2021. The
7-day and 28-day variants change block length only. The unstratified variant uses 14-day
blocks and removes calendar-year boundaries only; real gaps and endpoint masks still apply.

For each endpoint, split its valid paired-date mask into contiguous calendar runs within its
strata. A missing/excluded date or a date outside that endpoint's year/season cell breaks a
run. Never let a block cross a gap; adjacent observations separated by days are not lag-1
observations. Preserve every original run's sample count in each replicate. Sample with
replacement uniformly from all full non-circular blocks of the specified length within that
run; for a run shorter than the length use its whole length. Append sampled blocks until that
run's count is reached, truncating only the last block's right end. Concatenate the resampled
runs in the original run order, retaining explicit run boundaries. This fixed short-run rule
does not replace a gap with a circular wrap or a new observation.

The deterministic RNG for each variant is a fresh NumPy `default_rng(20261012)`. Visit arms
A1..A7 and endpoints in this order: overall MAE, overall WIS; years ascending with MAE then
WIS; seasons DJF/MAM/JJA/SON with MAE then WIS. Within an endpoint visit strata ascending and
runs ascending by first date. Store every drawn start-index replicate and its test statistic;
an uncomputable endpoint consumes no draw and remains p=1. Restart the same seed for each
variant, never according to a p-value. Preserve all twenty endpoint identities and seven-arm
Holm results for all four variants.

Let n be an endpoint's paired-date count and `z_t=d_t−mean(d)`. Estimate variance of the mean
as `V=[sum(z_t^2)+2*sum_{l=1..14}(1−l/15)*sum_t z_t*z_(t−l)]/n^2`.
Use only pairs exactly l calendar days apart within a contiguous retained run, with no
cross-stratum or cross-gap pair in the primary/7/28-day analyses. The unstratified analysis
admits calendar-adjacent cross-year pairs. Apply the same formula within resampled run
boundaries, where each sampled sequence advances one pseudo-calendar day; block joins are
ordinary joins within a run, but separate runs are never connected. Do not silently shorten
the HAC lag or change its divisor for a small cell.

The observed studentized statistic is `T=mean(d)/sqrt(V)`. In replicate b, compute its own
variance by that same HAC rule and use
`T_b=(mean(d_b)−mean(d))/sqrt(V_b)` (the centered null distribution). The one-sided p-value
is `(1+count(T_b<=T))/(10000+1)`. Include equal statistics in the lower-tail count. A
nonfinite/nonpositive variance, fewer than two paired observations, or nonfinite replicate
statistic makes the endpoint uncomputable with p=1; do not add a variance floor or silently
discard a replicate. Preserve that cause and all computable records. These conservative
degeneracy conventions also apply when an early learned arm is exactly the control.

For descriptive ratios or paired differences, save the same paired-bootstrap samples and
studentized pivots. Form 95% two-sided studentized intervals with linear 2.5/97.5 percentiles
of the pivots. Ratio inference uses the delta-method daily influence
`(a_t−R*b_t)/mean(b)` for `R=mean(a)/mean(b)` and recomputes it in each replicate; a zero or
nonfinite denominator is undefined. Never use a ratio interval instead of the registered
0.995/1.02 differential endpoint tests. DM, GW, MCS and calibration diagnostics are
descriptive only and cannot rescue an arm or add a selection endpoint.

## 10. Evidence, controls and terminal disclosures

Retain origin-level weights, shared-fit identifiers, training-date lists, scaler statistics,
six error-feature support counts, issue-time state support, parameter/seed identities, native
central vectors, emitted quantiles, all fallback statuses, own-error buffer provenance and
span, daily losses, paired masks, stored bootstrap draws/pivots, twenty endpoint p-values,
four compound/Holm decisions and the exact WIS tie/selection calculation. The ledger must
distinguish weighted central, emitted p50, native-startup equality and operational fallback.

Before any CP-28 scored run, prove causal controls with synthetic or training-only inputs:
target-day masking produces zero change; available past-input mutation produces an appropriate
change; D−1 error mutation produces zero change; D−2 released error can change learning;
duplicate release changes no buffer; future rows change no training/scaler feature; permuted
outcomes cannot move calendar masks; fallback cannot enter a member or arm H history; DST
canonical keys survive; A3/A6 and A5/A7 share the identical unshrunk fits; grid tie order,
Adam/L2 gradient, actual-hour day weighting, one-sided null boundary, twenty-endpoint maximum,
Holm and every sensitivity rule match this text. Positive controls accompany negative ones.

Support or implementation deficiencies do not authorize extra arms, alternate seeds or a
scored-day buffer exemption. Report native warm-up availability and any inability to seed an
arm before its scored start. A required arm that cannot be executed retains p=1. If the issued
CP-28 brief cannot be satisfied with this prospective specification, return the precise
deficiency before scoring rather than selecting a replacement method from CP-26's outcomes.

The final report names the conditional developmental evidence class, exception/risk
disclosures, minimum-history equivalence to v5/A3, fallbacks and failed rows, missing paired
cells, bootstrap degeneracies, all four Holm families and their first unmet conditions, and
the selected candidate or retained nominal control. Any later protocol amendment requires
the applicable Owner authority and a transparent new registration; it is never an unrecorded
repair to this one-look experiment.
