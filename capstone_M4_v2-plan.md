# M4 / v2 — Regime-robust calibration

**Status: DRAFT, awaiting owner ratification.** Authored by the Orchestrator 2026-09-15 on the
owner's explicit instruction of the same date. Nothing in this document is in force until the owner
ratifies it. It does not amend `capstone_V6_8.md`; it proposes a successor stage that begins after
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
A second, explicitly secondary track adds two gate-legal data sources that improve the
post-crisis product and, by construction, **cannot** touch the crisis regime.

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

**C-2 — Adaptive Conformal Inference** (Gibbs & Candès, 2021). Update α online from realized
coverage: `α_{t+1} = α_t + γ(target − 1{y_t ∈ C_t})`. Needs the realized outcome of delivery day
D−1 at the D origin — which **is** available and does not violate §5.2, but must be proved with the
same masking control, not assumed. `γ` is selected on folds {1,2,4,5} from a frozen grid.

**C-3 — Mondrian / regime-conditional conformal.** Separate thresholds per regime taxon. **Listed
for completeness and expected to be rejected** under §3 rule 6, because the regime taxonomy is
defined by dates we chose knowing the price history. Included so its rejection is recorded rather
than silent.

**Bar for Track 1:** the fixture discipline v1 established carries over intact — the `n_cal=20`
one-based-rank fixture must still reproduce `{20,19,17,11}` → `Q={8,7,5,−1}` for the unscaled path,
and the scaled path gets its own exact fixture before it is used. Isotonic remains last. Zero
crossings remains the one hard gate.

**Governance dependency.** `capstone_V6_8.md` §13 excludes sequential conformal (EnbPI / SPCI) and
states in its own words that *"Reintroducing sequential conformal work would require a new
owner-ratified amendment."* **C-2 is inside that exclusion. Ratifying this document is that
amendment.** C-1 and C-3 are not excluded by §13 and need no amendment.

---

## 5. Track 2 — data (secondary; does not touch the crisis)

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
| **CP-5** | Data arms *(optional; skippable without affecting CP-4)* | Open-Meteo fixed-lead-time ingest with a §5.2 proof; planned-outage ingest with its vintage assumption disclosed; two-arm rule on folds {4,5}; explicit non-coverage statement on every surface |
| **CP-6** | Freeze and wait | v2 artifact frozen and fingerprinted; interim status published per §7; nothing evaluated |
| **CP-7** | One-shot evaluation | ≥ 2026-12-06; fresh snapshot; one embargo day; opened exactly once; v1 vs v2 on equal footing; the §6 power limitation stated |

Each checkpoint follows the existing execution contract: one brief in, one packet out, one fresh
Integration Critic, `PASS`/`BLOCKED`/`INCOMPLETE`, owner-authored landing.

---

## 10. What this stage is NOT

- **Not a rewrite.** One monolithic LightGBM quantile ensemble, nine heads, as in §6.1.
- **Not a point-forecast programme.** The MAE deficit is a development-fold artifact the holdout
  contradicts; it is not the target.
- **Not a fuel-price layer.** Re-closed on evidence 2026-09-15.
- **Not a crisis fix from data.** Track 2 cannot reach 2022 and must never imply it can.
- **Not a replacement for v1.** v1 ships, stays live, and keeps its failure documented.
- **Not a licence to re-open v1's holdout.** It is spent permanently.

---

## 11. Open questions for the owner

1. **Ratify?** C-2 (ACI) requires the §13 amendment; C-1 and C-3 do not. Ratifying this document
   grants it. Declining C-2 still leaves a coherent stage.
2. **Is CP-5 in or out?** It is genuinely optional and adds real ingest work for a bounded,
   post-crisis-only gain.
3. **Does the 2026-12-06 wait stand?** The alternative is a shorter window with a wider CI and a
   weaker DM, stated as such. My recommendation is that it stands.
