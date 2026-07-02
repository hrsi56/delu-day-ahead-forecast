# Yarden's Triple-Track Progress Log

*Living document. Regenerated in full at the end of every session under the orchestrator-role.md regeneration contract. Last updated: **2026-07-02 (L2 closed; L3 issued)**.*

---

## Current Position

### Track A: Learning (Syllabus)
- **Anchor: `syllabus_v3_0.md` v3.0.**
- **Phase:** I (Mathematical Foundations). **Month:** 0. **Week:** 3–4 (launched 2026-06-09).
- **L1 — DONE.** Strang L1–5 + Ch. 1–2; Gaussian-elimination solver shipped.
- **L2 — DONE (2026-07-02, Yarden-reported).** Strang L6–10 + Ch. 3, [AUTH], four fundamental subspaces; `four_subspaces(A)` deliverable shipped.
- **L3 — ACTIVE (issued 2026-07-02).** Orthogonality → projections → least squares → Gram–Schmidt (OCW L14–17; verify index at briefing per C5-min); OLS normal-equation deliverable. Runs on silence-means-success.
- **Next after L3:** eigenvalues/eigenvectors L18–22 [AUTH]; determinants skim [REC]; SVD/PCA + condition number [REC] — this is the block that **closes Month 0** and fires the mid-month gate.
- **Pace note:** Month 0 is the binding constraint (5–6 weeks); conversion + spike consumed ~3 days of week 1. L1 and L2 both closed clean. On-plan, though the mid-month gate estimate slides from end-June to ~mid-July.
- **Next pending checkpoint:** Month-0 **mid-month gate**, ~mid-July — coding deliverable(s) runnable + NotebookLM consolidation verdict. **This is the next thing the orchestrator needs from Yarden.**

### Track B: Capstone Build
- **Anchor: `capstone_V6_1.md` v6.1** (on `main`; swapped into PK + NotebookLM). **Milestone: M0** (plan approved; spike complete, adjudicated, and merged). **Data-layer de-risking arc CLOSED — no open capstone actions.**
- **SPIKE — COMPLETE, ADJUDICATED, MERGED.** Branch `claude/modest-bardeen-96zee0` merged into `main` (2026-06-14). Memo `docs/spike-feed-status.md`. Final question status:
  - **Q1/Q3/Q4/Q5/Q6 — VERIFIED** (clean access; feature feeds PT15M across whole 2019+ archive, A44 date-conditional at 2025-10-01; boundary averaging exact to 1e-9; 2019 depth confirmed w/ ~25h A65/A01 head gap; ENTSO-E↔SMARD 96/96 within €0.01).
  - **Q2 (R-2) — VERIFIED, NO OVERWRITE** (2026-06-14): 3-snapshot compare for delivery 2026-06-13 (pre-pub / post-pub / post-delivery) — A65/A01 rev 1→1 and A69/A01 rev 3→3, both 96/96 bit-identical. Archive preserves as-published values; §5.2 fallback not invoked. **CP-1 item 5 = VERIFIED.**
  - **Q7 (gas) — NOT MET, FINAL.** SMARD API = generation volume only, no THE price.
  - **Q8 (SFTP) — CLOSED (2026-06-14).** Port 22 times out from all three machines tested incl. Yarden's M3 → standing local network policy (non-HTTP egress filtering), not ENTSO-E. SFTP ruled out as a fallback route; **no project impact** — it was always the secondary path, the chunked API is verified and sufficient for M1's bulk size, and SMARD is the verified fallback-primary over HTTP.
- **R-2 outcome → no spec change.** Verdict confirmed the favorable branch v6.1 already documents; interview honesty line strengthens to *"post-gate initial publication, archive verified stable ~44h later — bit-identical."* **No v6.2.**
- **M1** lands in syllabus Month 2; CP-1 activates at M1; brief inherits the **v6.1 §12 binding list**. Spike pre-confirmed CP-1 item 1 (full), item 3 (sample-level), item 5 (VERIFIED); rest open by design.
- **Pending clerical (B-Manual):** DagsHub account — Months 0–2 (precedes M2). HF account + Spaces — start of Month 5.
- **Next pending checkpoint:** CP-1 (at M1).

### Track C: Marketing — FROZEN (one-off floor authorized; consumes NO CV-iteration slot)
- Phase-trigger fires continuous activation **after capstone M2** (projected mid-Month 3). Active applications no later than start of Month 5.
- **Geography RATIFIED:** ≤3 office days/week TLV/Herzliya; Beer Sheva base.
- **One-off C2 floor (execute this month):** 1. LinkedIn floor (headline, About, Featured: World Psychiatry, solver, event app) — **PENDING**; recruiter-only open-to-work deferred to M2 trigger. 2. README polish on solver + event-app repos — **PENDING**. 3. Lab-Engineer framing fix — **CLOSED**; do NOT re-add "(transitional role)".
- **C8-research (Month 0–1):** tiered Beer-Sheva-local + ≤3-day-hybrid DS target list. Not yet issued.
- **C7 networking floor (from Month 1, ~1h/week):** former students, BGU alumni, one Tech7 / Gav-Yam Negev meetup per month.
- **Positioning theme (held):** career-changer from clinical research to industry DS — quantitative forecasting + honest uncertainty communication; World Psychiatry lead-analyst credibility + shipping experience; capstone with regime-aware methodology, walk-forward + embargo, KFT/LAG leakage audit, CQR-calibrated intervals, regime-stratified errors, cloud-backed reproducibility, deployed marimo showcase. "Why the German market, in Israel" carries the transfer answer.
- **Last published artifact:** None. **Pipeline:** empty. **Applications:** not started.
- **CV status:** over the bar to start applying. Three milestone-gated iteration slots remain (after M2, M3, M5).

---

## Setup State (one-time actions)

- **v6.1 swaps — DONE.** `capstone_V6_1.md` in project knowledge, NotebookLM, and repo `main` (all confirmed 2026-06-14).
- **Repo rename — DONE.** `hrsi56/PJM` → `hrsi56/delu-day-ahead-forecast` (redirect live).
- **Spike branch merge — DONE 2026-06-14** (`claude/modest-bardeen-96zee0` → `main`).
- **SFTP local check — DONE 2026-06-14** (port 22 blocked; Q8 closed, no impact).
- ENTSO-E token, repo, CLAUDE.md + capstone at root — DONE. *(Setup State is now empty of pending actions — section retained per skeleton; will carry the next one-time action when one arises.)*

---

## Strategic Anchors

- **Target:** Industry Data Scientist role within ~6.5 months at NIS 35K. Capstone audience: DS hiring manager, not MLE.
- **Geography:** ≤3 office days/week TLV/Herzliya (ratified 2026-06-10); Beer Sheva base.
- **Anchor docs:** **`capstone_V6_1.md` v6.1** + **`syllabus_v3_0.md` v3.0**, `orchestrator-role.md` / `notebooklm-role.md` / `engineer-role.md` (refreshed 2026-06-11; engineer doc = repo `CLAUDE.md`). Decision records: `change-register-decisions.md`, `de-lu-conversion-memo`, `docs/spike-feed-status.md` (in-repo).
- **Repo:** `hrsi56/delu-day-ahead-forecast`.
- **Depth labels:** [AUTH], [REC], [APPLIED-AUTH], [APPLIED-REC].
- **Budget:** $0 expected run rate; $65/month policy ceiling. Deployment $0.
- **Hardware:** Apple Silicon M3, 16 GB unified memory, CPU only.
- **Language:** English replies (Hebrew input fine).

---

## Standing Scope Decisions (carry forward indefinitely — do not allow back in)

- **Market = DE-LU via ENTSO-E + SMARD (ratified 2026-06-11).** PJM dead — do not revisit.
- **No gas/fuel-price layer — reopen ADJUDICATED NOT MET 2026-06-12, omission FINAL.** SMARD API exposes gas generation volume only, no THE price. Narrow residual: optional pre-M1 browser check of SMARD's JS gas page; re-opens only if it reveals a CC-BY, API-accessible daily THE **price** series (v6.1 §0.3, §13).
- **R-2 vintage — VERIFIED stable (2026-06-14):** TP archive preserves as-published A65/A01 + A69/A01 values (no overwrite); as-archived treatment documented and empirically backed. VRE initial publication is post-gate; the caveat is structural, stated, shared with every published EPF benchmark.
- **Data access — confirmed from two independent sources** (ENTSO-E API primary, SMARD fallback-primary over HTTP). SFTP route unavailable from Yarden's networks — not needed.
- **Hourly target end-to-end across the 15-min MTU transition** (2025-10-01); quarter-hours averaged to hourly (spike-validated). **Feature feeds natively PT15M from 2019 — uniform hourly aggregation at ingest; chunk-boundary bin integrity mandatory** (v6.1 §4.0). Quarter-hourly target = named future work.
- **No external weather.** Train-only Fourier climatology on the residual-load forecast series (v6.1 §0.5, §4.1).
- **No DVC.** Pinned deps + tagged commit + committed snapshot — **CC BY 4.0 with attribution** (v6.1 §9.3). `entsoe-py` pinned 0.8.0.
- **No live API pulls during user sessions.** Weekly manual snapshot refresh during the application phase.
- **No paid HF Spaces tier in baseline budget.** CPU Upgrade on standby for CP-5 cold-start only.
- **Single monolithic LightGBM** quantile ensemble. **No neural challenger** (SC3 rejected; shipped CNN + published evidence carry the question).
- **CQR (split conformal) only. No EnbPI / SPCI / Giacomini-White** — single pre-committed reopen (v6.1 §13): any regime stratum's coverage diverging >10 pp at M3 → EnbPI as remediation, comparison only.
- **LO3 REJECTED** — Month-0 SVD/PCA stays [REC]. **LO2 REJECTED** — no causal block.
- **Forecast + diagnostic report, not a trading product.**
- **Marimo is mandated.** Three sliders (Dunkelflaute toggle, headline perturbation, quantile selector) from the precomputed lookup with the per-cell OOD flag.
- **Walk-forward CV with 24h embargo, three-regime pinned fold scheme** (v6.1 §5.1: crisis-peak F3 Jul–Sep 2022; negative-price F4 May–Jul 2025; F5 current tail, fully post-15-min-transition).
- **Stranger-test gate happens on the deployed HF Spaces URL.**
- **Thin GitHub Actions CI on the §9.4 invariant tests is IN** (lands at M2; four mandatory tests incl. the extended 15-min aggregation-integrity test) — no regression matrix.
- **CP-2 secondary gate pre-committed:** Fold-5 DM p ∈ [0.05, 0.15] + pooled-across-folds DM significant → M2 passes, both numbers reported. **Comparator = similar-day naïve (Lago convention).** Fixed before results.
- **Headline-feature rule:** `residual_load_deviation_from_normal` primary; `scarcity_stress = relu(load_z)·relu(−vre_z)` secondary; SHAP at M3 decides. `gas_to_load_ratio` stays dead.

---

## Session Log (newest first)

- **2026-07-02 — L2 closed (Yarden-reported); L3 issued.** Orthogonality/projections/least squares/Gram–Schmidt (OCW L14–17), OLS normal-equation deliverable. Not a checkpoint block. Track B/C untouched this session (no open capstone action; Track C frozen).
- **2026-06-14 — Data-layer arc closed; L2 resumed.** Q8 SFTP confirmed blocked from the M3 (port 22 timeout) → closed, no impact (API + SMARD cover ingestion). Spike branch merged to `main`. v6.1 confirmed swapped into PK + NotebookLM. R-2 verdict (no overwrite) stands; no v6.2. All capstone open actions cleared.
- **2026-06-14 — R-2 verdict closed.** Final snapshot/compare: no overwrite (A65/A01 rev 1→1, A69/A01 rev 3→3, both 96/96 identical). CP-1 item 5 VERIFIED.
- **2026-06-12 (R-2 schedule) — Two engineer messages authored + timed** (post-pub baseline capture; verdict + housekeeping).
- **2026-06-12 (adjudication) — Spike report received; v6.1 authored.** Gas reopen NOT MET; R-2 sharpened; PT15M-everywhere + chunk-boundary + metadata-dead-end folded into spec; entsoe-py pinned 0.8.0.
- **2026-06-12 — Spike brief issued.** Token early; repo + Claude Code + gh CLI ready.
- **2026-06-11 (audit) — Post-conversion full-set audit PASSED.**
- **2026-06-11 (roles) — Three role docs refreshed.**
- **2026-06-11 (syllabus) — `syllabus_v3_0.md` authored.**
- **2026-06-11 (respec) — `capstone_V6_0.md` authored + ratified** (PJM→DE-LU).
- **2026-06-11 — Conversion memo; PJM geo-blocked; ENTSO-E open; token email; NotebookLM swap #1; L2 started.**
- **2026-06-10 — Orchestrator amendments; L1 done → L2 issued; change-register adjudication.**
- **2026-06-09 — Program launch; L1 issued.** **2026-05-31 — Baseline.**

---

## Blockers / Open Questions

- **None.** Data-layer de-risking complete; no capstone or setup action outstanding. (Optional, non-blocking: the 10-min SMARD JS gas-page browser check for epistemic closure on §0.3 — boundary stands either way; `.zshrc` line 137 dangling-source warning, cosmetic, fix when it annoys.)

---

## Notes for Future Sessions

- **Next session opening:** no checkpoint pending until the Month-0 mid-month gate. L3 runs on silence-means-success. Nothing for Yarden to carry up.
- **Month-0 mid-month gate (~mid-July):** the next thing the orchestrator needs — coding deliverable(s) runnable (OLS normal-equation + PCA/condition-number toy) + NotebookLM consolidation verdict. Flag the month-closing L block (eigen → determinants → SVD/PCA) as a checkpoint block when issued.
- **R-2 is closed — verified stable.** M1 proceeds with the as-archived documentation as-is; honesty line now evidence-backed.
- **M1 brief (syllabus Month 2):** inherits the **v6.1 §12 binding list** (feature aggregation + chunk-boundary integrity, A65/A01 ~25h head gap, R-2 as-archived documentation [verdict: stable], repo/branch-state verification). Plus the M1 cosmetic below.
- **M1 cosmetic:** verify Dec-2024 / Jan-2025 Dunkelflaute peaks against pulled data; tighten the §2.2 narrative sentence.
- **SQL authoring block** [APPLIED-AUTH]: parallel filler Months 2–3, 20h cap; toy table `ts, price, load, wind, solar`; done when LAG/LEAD window queries write cold.
- **CNN mini-project** [AUTH], B-Claude: Month 1→2 seam, 16h cap, CIFAR-10 default, ship-at-threshold. Not wired into the capstone.
- **C4 placements:** A/B testing [REC, ~4h] rides Month 1; classification & metrics [AUTH-light, 10–12h] early Month 3; timed take-homes late Month 3 + Month 4; mocks ×2–3 late Month 4 → Month 5.
- **Best interview lines to protect:** KFT/LAG leakage audit @ 12:00 CET gate (now w/ the 15:35 asymmetry *and* the no-overwrite verdict as evidence); exchangeability paragraph (verbatim); negative-Q / isotonic-last; change-point validation of the crisis flags; regime-stratified story w/ crisis-peak F3 + negative-price F4; R-2 honesty line ("post-gate publication, archive verified stable ~44h later"); gas-probe closure line ("I checked SMARD's API — volumes, not prices"); data-resilience line ("two independent sources — ENTSO-E API + SMARD fallback-primary"); two-sided bounded tail; model-staleness; "why the German market, in Israel" + "why hourly" + "why marimo" + "why thin CI".
- **CP-5 cold-start:** 30s backstop; Actions cron auto-disables after 60 days of repo inactivity — README disclaimer is the real backstop.
- **CV iteration cadence:** three milestone-gated slots (after M2, M3, M5).
- **Track C flips:** recruiter-only open-to-work at the M2 phase-trigger; applications no later than start of Month 5.
- **Routing reminder:** the orchestrator never writes Claude Code prompts; M briefs inherit the v6.1 §12 binding list rather than restating the spec.
