> ## ⚠ SUPERSEDED 2026-09-15
>
> **M4 has moved to a new anchor: [`capstone-completion-and-corrections.md`](capstone-completion-and-corrections.md).**
> Its §4 (calibration) and §5 (the frozen 90-day holdout) replace §4–§6 of this document, re-derived
> rather than copied so the stage fits the system that document builds around it.
>
> **This file is not deleted and is not the plan of record.** It is the record of how M4 was reasoned
> out and ratified on 2026-09-15 — the candidate set, the anti-overtuning discipline, the computed
> window, and the four owner decisions with the one Orchestrator recommendation that was overruled
> and why. Read it for the reasoning; build from the new anchor.

# M4 / v2 — Regime-robust calibration, and the product feed

**Status: RATIFIED 2026-09-15 by the owner**, on four decisions recorded in §11. Authored by the
Orchestrator on the owner's instruction of 2026-09-15. It does not amend `capstone_V6_8.md` except
where §4 says so explicitly and the owner granted it; it is a successor stage that begins now that
v6.8's completion definition is met.

**Prerequisite, already met:** M3/CP-3 landed 2026-09-15 (`land/cp-3`), GitHub Pages is live at
<https://hrsi56.github.io/delu-day-ahead-forecast/>, and v1's documentation is closed including the
defect this stage targets.

---

## 0. The one-paragraph statement

v1 ships a forecaster whose intervals are correctly calibrated in the post-crisis regime
(0.9398 against a nominal 0.95 on the one-shot holdout) and **collapse under a structural level
shift** (0.194 against a nominal 0.95 over the August-2022 peak weeks). M4 targets that one
measured defect. It is a **calibration-method** change, not a feature-engineering programme: the
mechanism is that a split-conformal correction is additive while the failure is multiplicative.
A second track adds two gate-legal data sources. **The owner ratified it as in scope on the
grounds that the goal is a working product rather than an experiment** — and a production DE-LU
forecaster that ignores freely available weather forecasts is not a serious product. By
construction it **cannot** touch the crisis regime, and every surface must say so unprompted.

---

## 1. What v1 got right, and what this stage must not undo

Carried forward unchanged and re-ratified by reference:

- The **§5.2 delivery-day availability invariant**. No v2 component may reintroduce a row-wise
  boundary or consume a value unavailable at the 12:00 CET D−1 origin. The existing positive control
  stands: masking delivery-day prices must change the output by exactly `0.0`, and a D−1 mutation
  must move it (currently `220.9433` EUR/MWh).
- **Positive controls on every negative assertion.** A test that something does not happen is
  satisfiable by an inert implementation unless a control proves it can fail.
- **Results are reported, never gated.** No item in this stage requires a favourable number.
  The one hard gate remains correctness: zero quantile-crossing violations after the full pipeline.
- **The frozen v1 champion is not deleted, retrained or superseded in place.** `land/cp-3`,
  `evidence/cp-3`, `models/champion/` and `docs/cp2-model-report.md` stay exactly as they are.
  v2 is a **second** artifact. The v1→v2 comparison is the deliverable.

---

## 2. The defect, stated so it can be falsified

| | |
|---|---|
| Nominal | 95 % |
| Observed, August-2022 peak weeks (408 h / 17 days) | **0.194** |
| Observed, one-shot holdout (2,160 h / 90 days) | 0.9398 |
| fold_3 calibration window | 2022-05-01 … 2022-06-29, mean level ≈ **€198** |
| fold_3 evaluation block | 2022-07-01 … 2022-09-28, mean level **€375.96** |
| Level ratio, calibration → evaluation | **1.90×** |

**Mechanism.** The CQR conformity score is `max(q̂_lo − y, y − q̂_hi)` and its correction is an
**additive** shift in EUR/MWh, estimated on the calibration slice. Residual magnitude in this market
scales with price level. A threshold sized in a €198 world is too narrow in a €376 world. This is
the documented behaviour of split conformal when exchangeability fails — the guarantee is
finite-sample but conditional, and a structural break voids the condition.

**Corollary that constrains the fix.** The point forecast degrades by a *different* mechanism
(shrinkage toward the training level: 61.3 % of fold_3's evaluation block sits above the 99th
percentile of its training data while only 2.45 % exceeds the maximum). **M4 does not claim to fix
the point forecast.** Anything that improves it is a reported side effect.

---

## 3. Anti-overtuning discipline — the binding constraint of this stage

**We already know fold_3's answer.** Every choice made while looking at it is a choice fitted to a
result we have seen. This section is the control, and it is pre-registered here rather than asserted
later.

1. **fold_3 is a diagnostic control, never a selection metric.** No hyperparameter, method variant,
   window length, or scale estimator is chosen by its fold_3 number. Selection runs on
   folds 1, 2, 4, 5 only, pooled, by the same observation-weighted rule v1 used.
2. **The method set is frozen before any v2 code runs.** Section 4 names the candidates exhaustively.
   Adding a candidate after seeing any result requires a written owner amendment and is recorded.
3. **One scalar per candidate, decided in advance.** Selection metric: pooled mean pinball loss over
   folds {1,2,4,5}. Ties default to the *simpler* method, in the order listed in §4.
4. **fold_3 is reported for every candidate, including the losers.** Publishing only the winner's
   crisis number would let a lucky draw masquerade as a fix. The full table ships.
5. **A pre-registered falsification.** If the selected method's fold_3 95 % coverage does not exceed
   v1's 0.194 by at least 0.20 absolute, **the stage reports that the fix did not work** and ships
   v1 as the recommended artifact. This threshold is written now, before any run.
6. **No fold_3-specific parameter may exist.** No crisis flag consumed by the calibrator, no regime
   switch, no per-regime threshold table keyed on a date we chose by looking at prices.

> Rule 5 is the one that makes this stage honest. Without a pre-registered failure condition, a
> calibration change can always be narrated as an improvement.

---

## 4. Track 1 — regime-robust calibration (core; no new data)

Candidates, in increasing order of conceptual surface. **Ties resolve upward in this list.**

**C-1 — Scaled (normalized) conformal.** Divide the conformity score by a locally estimated scale
`σ̂(x)` before taking the order statistic, and multiply back at prediction time. The threshold
becomes multiplicative. Candidate scale estimators, also frozen here: (a) the raw head spread
`q̂_0.95 − q̂_0.05`; (b) a trailing rolling price volatility computed under the §5.2 boundary.

**C-2 — Adaptive Conformal Inference** (Gibbs & Candès, 2021). Update α online from realised
coverage: `α_{t+1} = α_t + γ(target − 1{y_t ∈ C_t})`. `γ` is selected on folds {1,2,4,5} from a
frozen grid. The realisation it reads is **D−2's**, not D−1's — see the lag note below.

**C-3 — Mondrian / regime-conditional conformal. REJECTED 2026-09-15, before any run, and not
implemented.** Separate thresholds per regime taxon would require a regime taxonomy, and ours is
defined by dates chosen *after* seeing the price history — exactly what §3 rule 6 forbids.
Implementing a method already committed to rejection is wasted effort; the rejection is the
deliverable. It is recorded here so the boundary is visible rather than silent.

**Bar for Track 1:** the fixture discipline v1 established carries over intact — the `n_cal=20`
one-based-rank fixture must still reproduce `{20,19,17,11}` → `Q={8,7,5,−1}` for the unscaled path,
and the scaled path gets its own exact fixture before it is used. Isotonic remains last. Zero
crossings remains the one hard gate.

**Governance dependency — GRANTED.** `capstone_V6_8.md` §13 excludes sequential conformal
(EnbPI / SPCI) and states in its own words that *"Reintroducing sequential conformal work would
require a new owner-ratified amendment."* **C-2 is inside that exclusion, and the owner granted the
amendment on 2026-09-15.** It is scoped to C-2 in this stage and to nothing else.

**Why both C-1 and C-2 run, rather than the simpler one alone.** They fail differently, and that is
the point. C-1 assumes residual magnitude scales with price level — a modelling assumption that can
be wrong. C-2 assumes nothing about the mechanism; it watches realised coverage and corrects. Run
C-1 alone and a null result is uninterpretable: you cannot tell whether the calibration is
unfixable or whether you guessed the wrong mechanism. Running both makes the experiment
informative in either direction.

**C-2's feedback lag is two delivery days, and it is structural.** At the 12:00 CET D−1 origin,
delivery day D−1 is still in progress, so the most recent *fully observed* day is D−2. No amount of
accumulated history changes this — it is a property of the forecast geometry, not of data
availability. It is also not a problem: the ACI update reads the most recent *available*
realisation, and a two-day lag makes adaptation slightly slower, nothing more. **It must be proved
with the same masking control as every other boundary in this project, not assumed.**

---

## 5. Track 2 — data (IN SCOPE; does not touch the crisis)

**Ratified in on 2026-09-15.** The owner's ground: *the goal now is a working product, not
experiments and not research* — and a production DE-LU forecaster that ignores freely available,
gate-legal weather forecasts is not a serious product. That is correct on the merits, and the
Orchestrator's earlier "defer it" recommendation undersold it.

**Say this on every surface, unprompted:** neither source reaches the crisis regime. This track
improves the product that would actually be deployed. It is not a crisis fix and must never be
presented as one.

| Source | Licence | Coverage | Why it is bounded |
|---|---|---|---|
| **Open-Meteo, fixed lead time** | CC BY 4.0 | **Jan 2024 →** (Previous Runs); ECMWF IFS single runs from 2024-03-14 | The Historical Forecast API reaches 2017 but **stitches short-lead-time runs**, which is look-ahead. Only the fixed-lead-time endpoints are §5.2-legal, and they start in 2024. folds 1, 2 and 3 are unreachable. |
| **ENTSO-E planned outages (A80 / business type A53)** | Same token already held | Full history | **Vintage caveat, identical in class to R-2:** the archive is the current view, not the as-of-gate view, and revision metadata is a confirmed dead end. Planned outages are announced weeks ahead so the distortion is small; **forced outages (A54) are excluded** because for them it is fatal. The residual assumption is disclosed, exactly as A65's pre-gate status is. |

**Gas remains omitted, and this stage re-closes it on fresh evidence.** Re-checked 2026-09-15:
every TTF/THE source found is commercial with redistribution-prohibiting terms (oilpriceapi,
commodities-api, ICE, cbonds); ACER publishes a daily **LNG** assessment, not a hub price; Trading
Hub Europe publishes consumption and market-area monitoring, not a price series; EIA is Henry Hub
and the wrong market. **The §0-item-3 adjudication of 2026-06-12 stands.**

Because the weather feature is null before 2024, it is admitted **only** as an additional arm under
the same pre-registered two-arm rule v1 used, and it must show a lower pooled loss on folds {4,5}
— the only folds where it carries any information — to ship.

---

## 6. The holdout protocol — the part that cannot be rushed

**v1's holdout is spent.** It was opened once, `retrain_after_holdout: false`, and it is the only
confirmatory-class number in the project. v2 needs its own, on data that does not exist yet.

**Sequence, pre-registered:**

1. Build and select **entirely on folds {1,2,4,5}**, with fold_3 as a reported diagnostic only.
2. Freeze the v2 artifact. Record its fingerprint.
3. **Wait.** Accumulate new delivery days past the v1 snapshot cutoff of 2026-09-06.
4. Pull a fresh snapshot, apply a one-delivery-day embargo, evaluate **exactly once**.

**There is no usable buffer to shorten this with, and the date already assumes we use every day
that accrues.** The question was asked and checked rather than assumed. The v1 snapshot is
*fully consumed* through 2026-09-06 — fold_5 → embargo A → final calibration → embargo B → holdout
leaves nothing untouched inside it. What is genuinely new is the days since the v1 holdout ended:
**9 as of 2026-09-15**, fewer once publication lag is applied. 90 new delivery days starting
2026-09-07 completes **2026-12-05**, which is where the target date came from. The accrual is
already priced in; there is nothing to recover.

**Minimum credible window — computed from v1's own holdout, not guessed.** Day-level coverage
standard deviation 0.1149; day-level effective sample size 76.7 of 90 (dependence inflation 1.17×):

| Purpose | Requirement | Days |
|---|---|---|
| Coverage CI half-width ±5.0 pp | confirm v2 did not break normal-regime coverage | 24 |
| Coverage CI half-width ±4.0 pp | | 38 |
| Coverage CI half-width ±3.0 pp | | 67 |
| Coverage CI half-width ±2.0 pp | | 149 |
| DM power 0.80, one-sided α=0.05, \|d\|=0.50 | | 25 |
| DM power 0.80, \|d\|=0.30 | | 69 |
| DM power 0.80, \|d\|=0.2165 *(v1's development effect vs naive)* | | 132 |

**Decision: 90 delivery days.** It matches v1's holdout exactly, so the two are compared on equal
footing; it gives ±3.8 pp on coverage; and it reaches 80 % power at \|d\| ≥ 0.26 on the DM.

**Pre-registered limitation, stated now:** a pinball effect smaller than \|d\| ≈ 0.26 **will not be
detectable** at this window, and the report will say so rather than reading a null as a tie.

**Two arms are frozen, not one — this is how Track 2 enters without confounding the result.**
Both tracks would otherwise land in the same one-shot window, and a joint improvement could not be
attributed to either. So **two artifacts are frozen before the wait and both are evaluated on the
same window**: `v2-calibration-only` (Track 1 alone) and `v2-full` (Track 1 + Track 2). That is one
extra evaluation of a pre-frozen artifact, not a second holdout, and it is pre-registered here.

- **Primary endpoint:** interval coverage and pinball, `v2-calibration-only` vs v1. This is the
  question the stage exists to answer.
- **Secondary endpoint:** point accuracy and pinball, `v2-full` vs `v2-calibration-only`. This is
  the data track's own contribution, isolated.
- `v2-full` ships if it does not degrade the primary endpoint. Attribution survives either way.

**Earliest possible test date: 2026-12-06** — 90 delivery days past 2026-09-06, plus the embargo day
and publication lag. Between ratification and that date the stage is in *built-but-untested* status,
and **every surface must say so**.

---

## 7. What the interim status is allowed to claim

Between freeze and the 2026-12-06 evaluation, v2 has **development-class evidence only**. During
that period:

- v1 remains the **recommended artifact** and the one the live surfaces serve.
- v2's validation numbers are published as `development_post_selection`, never as skill.
- The phrase *"we see improvement in validation and do not yet have a reliable test"* is the
  accurate description and should be used verbatim rather than softened.
- fold_3 results are published as a **historical stress diagnostic on a known window**, with the
  §3 rule-5 falsification threshold quoted alongside, so a reader can see what would have counted
  as failure.

---

## 8. fold_3 re-run and the story it supports

The selected method is re-run over fold_3 and compared to v1's 0.194 head to head, with the honest
frame:

> This is a historical stress test on a window whose behaviour we already knew, so it is a
> diagnostic and not evidence of skill. It is also the only crisis we have. Track 2's data cannot
> reach it — gate-legal weather forecasts begin in 2024 — so v2 enters the next structural break
> with a calibration that adapts to level and without a fuel-cost signal, which remains unavailable
> on redistributable terms. Better prepared, not solved.

---

## 9. Checkpoints

| | | Bar |
|---|---|---|
| **CP-4** | Calibration method | All §4 candidates implemented with exact fixtures; selection on folds {1,2,4,5}; full table including fold_3 for every candidate including losers; §3 rule-5 falsification evaluated and reported; zero crossings; positive controls on every negative assertion |
| **CP-5** | Data arms — **IN SCOPE, not optional** | Open-Meteo fixed-lead-time ingest with a §5.2 proof; planned-outage ingest with its vintage assumption disclosed; two-arm rule on folds {4,5}; explicit non-coverage statement on every surface |
| **CP-6** | Freeze and wait | **Both** artifacts frozen and fingerprinted — `v2-calibration-only` and `v2-full`; interim status published per §7; nothing evaluated |
| **CP-7** | One-shot evaluation | ≥ 2026-12-06; fresh snapshot; one embargo day; opened exactly once; primary and secondary endpoints per §6, v1 vs v2 on equal footing; the §6 power limitation stated |

Each checkpoint follows the existing execution contract: one brief in, one packet out, one fresh
Integration Critic, `PASS`/`BLOCKED`/`INCOMPLETE`, owner-authored landing.

**No landing without a verdict that binds the final candidate.** CP-3B landed with its item 6
unmet — recorded at `docs/track-b/evidence/cp-3b/item-6-NOT-COMPLETED.md` — because its review was
cut off twice. **That is not a precedent.** CP-4 decides whether a calibration method works, which
is precisely where an independent verdict is the substance rather than the bookkeeping. Every brief
in this stage says so explicitly.

---

## 10. What this stage is NOT

- **Not a rewrite.** One monolithic LightGBM quantile ensemble, nine heads, as in §6.1.
- **Not a point-forecast programme.** The MAE deficit is a development-fold artifact the holdout
  contradicts; it is not the target.
- **Not a fuel-price layer.** Re-closed on evidence 2026-09-15.
- **Not a crisis fix from data.** Track 2 cannot reach 2022 and must never imply it can. It is in scope as *product*, and only as product.
- **Not a replacement for v1.** v1 ships, stays live, and keeps its failure documented.
- **Not a licence to re-open v1's holdout.** It is spent permanently.

---

## 11. The four decisions, as taken

Recorded 2026-09-15. Each was put to the owner with the Orchestrator's recommendation; where the
two differ, both are stated.

| # | Decision | Taken | Orchestrator's recommendation |
|---|---|---|---|
| 1 | **Ratify, and include C-2 (ACI)** — granting the §13 sequential-conformal amendment, scoped to C-2 in this stage | **Yes** | Same. C-1 alone makes a null result uninterpretable. |
| 1b | **C-3 — document the rejection, do not implement** | **Yes** | Same. |
| 2 | **Track 2 / CP-5 is IN scope** | **Yes** | **Differed.** The Orchestrator recommended deferring it to avoid confounding one one-shot window. The owner ratified it in, on the ground that the goal is a working product rather than an experiment. **That ground is correct, and it is answered rather than overridden:** §6 freezes two artifacts and pre-registers a primary and a secondary endpoint, so attribution survives. |
| 3 | **90 delivery days; 2026-12-06 stands** | **Yes** | Same. |
| 4 | **CP-3B item 6: close it, recorded as NOT COMPLETED** | **Yes** | Same. `docs/track-b/evidence/cp-3b/item-6-NOT-COMPLETED.md`. |

**One owner premise corrected before it entered the plan.** The proposal was that accumulated buffer
days could remove C-2's two-day requirement. Two different things had been conflated:

- **C-2's two-day lag is not a waiting period and no buffer can shorten it.** At the 12:00 CET D−1
  origin, delivery day D−1 is still in progress, so the most recent fully observed day is D−2. That
  is forecast geometry, not data availability. It is also harmless: the update reads the most recent
  available realisation and adapts slightly more slowly.
- **The buffer is real but small, and already counted.** The v1 snapshot is fully consumed through
  2026-09-06; 9 new days exist as of 2026-09-15. 90 new days from 2026-09-07 completes 2026-12-05 —
  which is where the target date came from in the first place.

The owner's conclusion — *we are not waiting idly* — is right. Build, selection and freeze all run
during the accrual. What does not happen is the window getting shorter.

---

## 12. Changes from the 2026-09-15 draft

- Status: DRAFT → **RATIFIED**. C-2's §13 amendment **granted**.
- C-3 moved from *"expected to be rejected"* to **rejected before any run, not implemented**.
- Track 2 moved from *optional/secondary* to **in scope**, with the owner's product rationale stated.
- §6 gained the **two-arm freeze** (`v2-calibration-only`, `v2-full`) with primary and secondary
  endpoints, which is what lets Track 2 be in scope without confounding the one-shot window.
- §6 gained the **buffer arithmetic**, answering the accrual question with numbers.
- §4 gained the **feedback-lag note** and corrected the draft's claim that C-2 reads D−1's outcome.
- §9 gained **no-landing-without-a-binding-verdict**, with CP-3B's unmet item 6 named as the
  non-precedent it is.
