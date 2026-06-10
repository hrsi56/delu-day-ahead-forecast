# Yarden's Triple-Track Progress Log

*Living document. Regenerated in full at the end of every session under the orchestrator-role.md regeneration contract. Last updated: **2026-06-10**.*

---

## Current Position

### Track A: Learning (Syllabus)
- **Anchor:** `syllabus_v2_3.md` v2.3 (ratified 2026-06-10).
- **Phase:** I (Mathematical Foundations). **Month:** 0 (Linear Algebra + SVD/PCA recognition). **Week:** 1 (launched 2026-06-09).
- **L1 — DONE.** Strang Lectures 1–5 + Ch. 1–2 reported complete; Gaussian-elimination solver deliverable assumed shipped per session contract (no checkpoint crossed, no flag raised).
- **Active L block: L2** — Strang Lectures 6–10 + Ch. 3, [AUTH], four fundamental subspaces. Deliverable: hand-authored `four_subspaces(A)` (bases for all four subspaces, rank–nullity self-check, full-rank + rank-deficient test cases). Issued 2026-06-10.
- **Next after L2: L3** — orthogonality → projections → least squares → Gram–Schmidt (OCW L14–17; verify lecture numbers against the live OCW index at briefing, per C5-min; L11–13 folded/skimmed as needed). Lands the OLS normal-equation coding deliverable. Then eigenvalues/eigenvectors L21–22 [AUTH]; determinants L18–20 skim [REC]; SVD/PCA + condition number [REC] close Month 0.
- **Pace:** ~6.5 months accepted; Month 0 = 5–6 weeks on-plan. C4 interview-readiness blocks (~24–28h) ride as parallel filler Months 1–4.
- **Next pending checkpoint:** Month-0 **mid-month gate**, ~2.5–3 weeks from launch (≈ end of June) — coding deliverable(s) runnable + NotebookLM consolidation verdict. The L block closing the gate gets the checkpoint flag.

### Track B: Capstone Build
- **Anchor:** `capstone_V5_5.md` v5.5 (ratified 2026-06-10). **Milestone: M0** (plan approved).
- **Next B block: Month-0 data-layer de-risking spike** (B-Claude, **6–8h hard cap — not an early M1**). Confirms: (a) `da_tempset` archive reaches 2019 + schema workable via direct DM2 API; (b) EIA regional gas series IDs (Transco Z6 NNY, TETCO M3) exist + post-2024 gap profile tolerable, Henry Hub `RNGWHHD` backstop confirmed; (c) `load_frcstd_hist` carries Western/RTO; (d) one 30-day verified-LMP pull reconciles total_lmp = SMP+MCC+MLC; (e) **R-4 probe** — PJM Cold Weather Advisory/Alert records 2019→present with issuance timestamps (degraded fallback pre-authorized, v5.5 §4/§11). Output: feed-status memo + **repo skeleton + first commit**.
- **Gated on:** PJM Tools account + Data Miner 2 key (B-Manual) — must land before the spike.
- **M1** (data layer + feature catalog v1 — `temperature_deviation_from_normal` primary, `scarcity_stress` secondary, train-only temperature-aggregate weights, R-4 outcome applied) lands in syllabus Month 2; CP-1 activates when M1 starts. The M1 brief inherits the **v5.5 §12 binding list** — do not restate the spec.
- **Last commit:** None (the spike delivers the first).
- **Pending clerical (B-Manual):** PJM key — NOW, pre-spike. DagsHub account — Months 0–2 (must precede M2 MLflow logging). HF account + Spaces setup — start of Month 5.
- **Next pending checkpoint:** CP-1 (activates at M1, syllabus Month 2). Before that, the spike's feed-status memo is the de-facto gate on M1 readiness.

### Track C: Marketing — FROZEN (one-off floor authorized; consumes NO CV-iteration slot)
- Phase-trigger fires continuous activation **after capstone M2** (projected mid-Month 3). Active applications no later than start of Month 5.
- **Geography RATIFIED:** ≤3 office days/week TLV/Herzliya; Beer Sheva base.
- **One-off C2 floor (execute this month):**
  1. LinkedIn floor — headline, About, Featured projects (World Psychiatry, solver, event app) — **PENDING**. Recruiter-only open-to-work DEFERRED to the M2 phase-trigger.
  2. README polish on the solver + event-app repos (linked from the live CV) — **PENDING**.
  3. Lab-Engineer framing fix — **CLOSED** (verified on live CV: "Income-bridge; managing instrumentation and protocols across 7 concurrent lab courses"). Do NOT re-add "(transitional role)".
- **C8-research (Month 0–1):** C-Research block — tiered Beer-Sheva-local + ≤3-day-hybrid DS target list (who hires, stack, salary bands, office-day policy). Not yet issued.
- **C7 networking floor (from Month 1, ~1h/week):** former students (30 taught 1-on-1), BGU alumni, one Tech7 / Gav-Yam Negev meetup per month.
- **Positioning theme (held):** career-changer from clinical research to industry DS — quantitative forecasting + honest uncertainty communication; World Psychiatry lead-analyst credibility + shipping experience (400+ concurrent-user app, 187M-state search engine); capstone with regime-aware methodology, walk-forward + embargo, KFT/LAG leakage audit, CQR-calibrated intervals, regime-stratified error analysis, cloud-backed reproducibility, deployed marimo showcase.
- **Last published artifact:** None. **Pipeline:** empty (floor starts Month 1). **Applications:** not started.
- **CV status:** over the bar to start applying. Three milestone-gated iteration slots remain (after M2, M3, M5).

---

## Setup State (one-time actions)

- **Project-knowledge swap — DONE** (verified 2026-06-10: project knowledge now holds `syllabus_v2_3.md` + `capstone_V5_5.md` + current `progress.md`; `change-register-decisions.md` retained as decision record).
- **NotebookLM source swap — PENDING-UNCONFIRMED:** the notebook may still hold `syllabus_v2_2.md` + `capstone_V5_4.md`. Replace with `syllabus_v2_3.md` + `capstone_V5_5.md` (keep `notebooklm-role.md`) **before pasting L2**. L1 was unaffected (its content didn't change between versions). Confirm when done and this item closes.
- **Orchestrator-role.md amendment — DONE 2026-06-10:** progress regeneration contract + file delivery + version-note guard added. Yarden swaps the amended file into project instructions.

---

## Strategic Anchors

- **Target:** Industry Data Scientist role within ~6.5 months at NIS 35K. Capstone audience: DS hiring manager, not MLE.
- **Geography:** ≤3 office days/week TLV/Herzliya (ratified 2026-06-10); Beer Sheva base.
- **Anchor docs (mutually consistent as of 2026-06-10):** `capstone_V5_5.md` v5.5, `syllabus_v2_3.md` v2.3, `orchestrator-role.md` (amended 2026-06-10). Executor role docs: `notebooklm-role.md`, `engineer-role.md` (repo `CLAUDE.md`). Decision record: `change-register-decisions.md` — 23 accepted (2 modified), 6 rejected.
- **Depth labels:** [AUTH], [REC], [APPLIED-AUTH], [APPLIED-REC].
- **Budget:** $0 expected run rate; $65/month policy ceiling. Deployment $0 (HF Spaces free + DagsHub free + GitHub Actions free, incl. thin CI).
- **Hardware:** Apple Silicon M3, 16 GB unified memory, CPU only.
- **Language:** English replies (Hebrew input fine).

---

## Standing Scope Decisions (carry forward indefinitely — do not allow back in)

- **No DVC.** Reproducibility = pinned deps + tagged commit + committed Parquet snapshot — plus the M1 redistribution-terms check; if PJM terms restrict, fallback = engineered matrix + regeneration code (v5.5 §9.3).
- **No live API pulls during user sessions.** Weekly manual snapshot refresh (~5 min/week) during the application phase.
- **No paid HF Spaces tier in baseline budget.** CPU Upgrade on standby for CP-5 cold-start failures only.
- **Single monolithic LightGBM** quantile ensemble. **No neural challenger — SC3 REJECTED 2026-06-10** (Olivares 2023 + the shipped CNN cover the question). SC3-learn fell with it.
- **CQR (split conformal) only. No EnbPI / SPCI / Giacomini-White — SC5 REJECTED**, with the single pre-committed reopen condition (v5.5 §13): post-Elliott empirical coverage diverging >10 pp from nominal at M3 → EnbPI returns as remediation, comparison only (SC5-learn revives at [APPLIED-AUTH] only then).
- **LO3 REJECTED** — Month-0 SVD/PCA stays [REC]; no Eckart–Young. **LO2 REJECTED** — no causal block; the SEM background carries the answer. Both recorded inside `syllabus_v2_3.md` ("Does NOT Teach").
- **Forecast + diagnostic report, not a trading product.**
- **Marimo is mandated.** Three sliders served from the precomputed lookup with the per-cell OOD flag.
- **Walk-forward CV with 24h embargo** is non-negotiable — v5.5 fold scheme: winter Fold 4 (Jan–Mar 2025), Fold 5 sliding to the pull date.
- **Stranger-test gate happens on the deployed HF Spaces URL.**
- **Thin GitHub Actions CI on the §9.4 invariant tests is IN** (lands at M2) — still no regression matrix, no scheduled retraining, no drift gates.
- **CP-2 secondary gate pre-committed (F5):** Fold-5 DM p ∈ [0.05, 0.15] + pooled-across-folds DM significant → M2 passes, both numbers reported. Fixed before results — do not relitigate after seeing them.

---

## Session Log

- **2026-05-31 — Baseline.** Project knowledge configured and made internally consistent. Capstone at M0; Track C frozen.
- **2026-06-09 — Program launch.** Readiness confirmed. Track A Month 0 started; **L1 issued** (Strang L1–5 + Ch. 1–2, [AUTH], Gaussian-elimination solver).
- **2026-06-10 — Change-register adjudication; v5.5 + v2.3 ratified.** 23 accepted (2 modified), 6 rejected (SC3, SC3-learn, SC5, SC5-learn, LO3, LO2). Alignment pass caught three stale v2.2 artifacts. progress.md regenerated; one correction owned (launch state restored).
- **2026-06-10 (later) — L1 done; L2 issued.** Yarden reported Lectures 1–5 complete. L2 (four fundamental subspaces, L6–10 + Ch. 3) issued. Month-0 spike surfaced as a parallel option, gated on the PJM key — his call pending.
- **2026-06-10 (later) — Orchestrator instructions amended; progress.md restored.** The interim progress regeneration had silently dropped Setup State, the C2/C7/C8 Track C floor, future-session notes, and two standing decisions — correction owned. Fix: regeneration contract (mandatory skeleton, prune-only-resolved, omission diff, ceiling-not-target) + file delivery + version-note guard written into `orchestrator-role.md`. This file is the first regeneration under the contract; dropped items restored.

---

## Blockers / Open Questions

- **NotebookLM source swap** — done or not? Gates pasting L2 into the notebook (see Setup State).
- **Spike parallelization** — open the Month-0 data-layer spike alongside L2 this session, or stay L-only? If yes, the PJM Data Miner 2 key (B-Manual) lands first.

---

## Notes for Future Sessions

- **L3 pickup:** orthogonality/projections/least squares/Gram–Schmidt (OCW L14–17, verify index per C5-min) — lands the OLS normal-equation deliverable. Eigen L21–22 [AUTH]; determinants 18–20 skim [REC]; SVD/PCA + condition number [REC] close Month 0.
- **Month-0 spike** is the first B-Claude block; schedule alongside Week 1–2 L blocks. PJM key (B-Manual) must precede it. Spike creates the repo (skeleton + first commit).
- **SQL authoring block** [APPLIED-AUTH]: parallel filler Months 2–3, 20h hard cap; done when LAG/LEAD window-function queries can be written cold.
- **CNN mini-project** [AUTH], B-Claude: Month 1→2 seam, 16h hard cap, **CIFAR-10 default** (Fashion-MNIST only as de-scope fallback), ship-at-threshold (~70%+), no HP sweep / transfer learning / deployment. Not wired into the PJM capstone.
- **C4 placements** (v2.3 Supplementary): A/B testing [REC, ~4h] rides Month 1's hypothesis-testing block; classification & metrics [AUTH-light, 10–12h cap] early Month 3; timed take-homes (4h box each) late Month 3 + Month 4; mock interviews ×2–3 late Month 4 → Month 5.
- **Headline feature:** `temperature_deviation_from_normal` (primary); `scarcity_stress` (secondary, promoted only if SHAP earns it at M3). `gas_to_load_ratio` is dead — do not resurrect (v5.5 §4.1).
- **Best interview lines to protect:** KFT/LAG leakage audit (§5.2); exchangeability paragraph (§6.2, verbatim); negative-Q / isotonic-last (§6.2); Bayesian change-point validation of `post_elliott` (Month 1); regime-stratified error story with true-OOS winter Fold 4 (§5.1, §8.3); model-staleness honesty line (§9.3); "why PJM, in Israel" + "why marimo" + "why thin CI, no regression matrix" (Month 5).
- **CP-5 cold-start:** 30s backstop calibrated to HF free tier; the Actions keep-alive cron auto-disables after 60 days of repo inactivity — the README "~30s first-load" disclaimer is the real backstop; commit at least every 60 days or accept the sleep (v5.5 §9.2).
- **CV iteration cadence:** three milestone-gated slots (after M2, M3, M5). Lab-Engineer fix CLOSED; the C2 LinkedIn floor consumed no slot.
- **Track C flips:** recruiter-only open-to-work at the M2 phase-trigger; applications no later than start of Month 5.
- **Routing reminder:** the orchestrator never writes Claude Code prompts; the M1 brief inherits the v5.5 §12 binding list rather than restating the spec.
