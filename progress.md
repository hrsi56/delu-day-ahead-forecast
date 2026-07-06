# Yarden's Triple-Track Progress Log

*Living document. Regenerated in full under the orchestrator-role.md regeneration contract. Last updated: **2026-07-06 (G0-mid CLOSED clean; L4 reissued with remediation emphasis, ACTIVE)**.*

---

## Current Position

### Track A: Learning (Syllabus)
- **Anchor: `syllabus_v3_0.md` v3.0.**
- **Phase:** I (Mathematical Foundations). **Month:** 0, week 4–5 (launched 2026-06-09).
- **L1 — DONE.** Strang L1–5 + Ch. 1–2; Gaussian-elimination solver shipped.
- **L2 — DONE (2026-07-02).** Four fundamental subspaces; `four_subspaces(A)` shipped.
- **L3 — DONE (2026-07-05).** Orthogonality → projections → least squares → Gram–Schmidt; OLS normal-equation deliverable (Month-0 deliverable #1).
- **G0-mid — CLOSED (2026-07-06).** All three artifacts re-ran clean. Verdict: normal-equations-from-projection-geometry, manual Gram–Schmidt, and the four-subspaces map solid at [AUTH]. **Flagged gap:** geometric intuition for AᵀA and the link from its eigenvalues to the condition number of the capstone feature catalog. Determinants/Jordan floor-demonstrated at [REC] during the gate block. **Remediation folded into L4 as a named first-class emphasis — no separate block.**
- **L4 — ACTIVE (reissued 2026-07-06 with remediation emphasis).** Eigen/diagonalization [AUTH] (OCW L21–22 + Strang Ch. 6); AᵀA geometry as first-class objective; determinants skim compressed (floor already demonstrated). Deliverable: symmetric 3×3 diagonalization (hand + NumPy) + AᵀA ellipse/eigenvalue-ratio artifact with the AᵀA → SVD bridge paragraph.
- **L5 — NEXT.** SVD/PCA + condition number [REC]; Month-0 deliverable #2 (PCA/condition-number toy on synthetic load/wind/solar/residual-load). **Flag L5 as a checkpoint block → G0 verdict closes Month 0.**
- **Pace:** on-plan; Month-0 six-week envelope ends ~2026-07-21; L4 + L5 both land by then or flag the slip plainly.
- **Next pending checkpoint:** **G0 (Month-0 close)** — one-line status (deliverables #1–#2 runnable + consolidation verdict) at the opening after L5 wraps.

### Track B: Capstone Build
- **Anchor: `capstone_V6_1.md` v6.1** (in PK + NotebookLM + repo `main`). **Milestone: M0 done**; data-layer de-risking arc CLOSED; no open capstone actions.
- **M1** lands in syllabus Month 2; **CP-1 activates at M1**; brief inherits the v6.1 §12 binding list. Spike pre-confirmed CP-1 items 1 (full), 3 (sample-level), 5 (VERIFIED).
- **Pending clerical (B-Manual):** DagsHub account — before M2. Optional pre-M1: 10-min SMARD gas-page browser check (map row B-Man0).
- **Next pending checkpoint:** CP-1 (at M1).

### Track C: Marketing — FROZEN (one-off floor authorized; consumes NO CV-iteration slot)
- Phase-trigger fires after capstone M2 (projected mid-Month 3). Active applications no later than start of Month 5.
- **Geography RATIFIED:** ≤3 office days/week TLV/Herzliya; Beer Sheva base.
- **One-off C2 floor (authorized 2026-06-10) — still PENDING:** 1. LinkedIn floor (headline, About, Featured: World Psychiatry, solver, event app) — PENDING; recruiter-only open-to-work deferred to M2 trigger. 2. README polish on solver + event-app repos — PENDING. 3. Lab-Engineer framing fix — CLOSED; do NOT re-add "(transitional role)".
- **C8-research (window Months 0–1, closing):** tiered Beer-Sheva-local + ≤3-day-hybrid DS target list. Not yet issued.
- **C7 networking floor (from Month 1, ~1h/week):** former students, BGU alumni, one Tech7 / Gav-Yam Negev meetup per month.
- **Positioning theme (held):** career-changer from clinical research to industry DS — quantitative forecasting + honest uncertainty communication; World Psychiatry lead-analyst credibility + shipping experience; capstone with regime-aware methodology, walk-forward + embargo, KFT/LAG leakage audit, CQR-calibrated intervals, regime-stratified errors, cloud-backed reproducibility, deployed marimo showcase. "Why the German market, in Israel" carries the transfer answer.
- **Last published artifact:** None. **Pipeline:** empty. **Applications:** not started.
- **CV status:** over the bar to start applying. Three milestone-gated iteration slots remain (after M2, M3, M5).

---

## Setup State (one-time actions)

- **`program-stage-sequence.md` v2 swap — DONE** (confirmed mounted 2026-07-05).
- **`orchestrator-role.md` 2026-07-02 revision — DONE** (active as project prompt).
- Earlier items — all DONE (compressed): v6.1 swaps (PK + NotebookLM + repo), repo rename → `hrsi56/delu-day-ahead-forecast`, spike branch merge, SFTP check (Q8 closed), ENTSO-E token, repo + CLAUDE.md + capstone at root.

---

## Strategic Anchors

- **Target:** Industry Data Scientist role within ~6.5 months at NIS 35K. Capstone audience: DS hiring manager, not MLE.
- **Geography:** ≤3 office days/week TLV/Herzliya (ratified 2026-06-10); Beer Sheva base.
- **Anchor docs:** **`capstone_V6_1.md` v6.1** + **`syllabus_v3_0.md` v3.0**; role docs: `orchestrator-role.md` (rev 2026-07-02), `notebooklm-role.md`, engineer doc = repo `CLAUDE.md`. Planning aid (non-anchor): `program-stage-sequence.md` v2 (2026-07-05). Decision records: `change-register-decisions.md`, `de-lu-conversion-memo`, `docs/spike-feed-status.md` (in-repo).
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

- **2026-07-06 — G0-mid CLOSED clean; L4 reissued (ACTIVE).** Verdict: artifacts re-ran clean; L1–L3 core solid at [AUTH]; flagged gap = AᵀA geometry ↔ eigenvalues ↔ condition-number intuition → folded into L4 as first-class remediation emphasis (no separate block); determinants/Jordan floor-demonstrated → L4 skim compressed. C2/C8 question (2026-07-05) still unanswered → moved to Open Questions.
- **2026-07-05 — L3 closed (Yarden-reported); G0-mid checkpoint block + L4 issued.** Same day: stage-map audit vs. both anchors → **map v2 authored + swapped** (navigation column; +C2/C8/B-Man0 rows); orchestrator-role 2026-07-02 revision confirmed live. Tracks B/C untouched.
- **2026-07-02 — L2 closed (Yarden-reported); L3 issued** (not a checkpoint block).
- **2026-06-14 — Data-layer arc closed; L2 resumed.** Q8 SFTP blocked → closed, no impact. Spike branch merged to `main`. v6.1 swaps confirmed. R-2 verdict (no overwrite) stands; no v6.2.
- **2026-06-14 — R-2 verdict closed** (CP-1 item 5 VERIFIED). **2026-06-12 —** R-2 harness authored; spike adjudicated → v6.1; spike brief issued. **2026-06-11 —** conversion memo (PJM geo-blocked → DE-LU); `capstone_V6_0` + `syllabus_v3_0` authored; roles refreshed; audit passed. **2026-06-10 —** amendments; L1 done → L2; change-register adjudication. **2026-06-09 — program launch; L1 issued. 2026-05-31 — baseline.**

---

## Blockers / Open Questions

- **C2 floor + C8 research (Track C, pending since 2026-06-10; Months 0–1 window closing):** issue as blocks or explicitly defer past Month 0? **Asked 2026-07-05 — unanswered; persists until Yarden answers.**
- Optional, non-blocking: 10-min SMARD JS gas-page browser check (pre-M1, epistemic closure on §0.3 — boundary stands either way); `.zshrc` line 137 dangling-source warning, cosmetic.

---

## Notes for Future Sessions

- **L5 (closes Month 0):** flag as **checkpoint block** → G0 verdict. Deliverable #2 = PCA + condition-number toy on synthetic load/wind/solar/residual-load (rehearses the capstone §4 collinearity diagnostic). The G0 verdict should explicitly confirm the G0-mid flagged gap (AᵀA/eigenvalue/condition-number intuition) has closed after L4+L5.
- **Pace watch:** Month-0 six-week envelope ends ~2026-07-21; L4 + L5 both land by then or flag the slip plainly.
- **M1 brief (syllabus Month 2):** inherits the **v6.1 §12 binding list** + M1 cosmetic (verify Dec-2024 / Jan-2025 Dunkelflaute peaks against pulled data; tighten the §2.2 narrative sentence).
- **SQL authoring block** [APPLIED-AUTH]: parallel filler Months 2–3, 20h cap; toy table `ts, price, load, wind, solar`; done when LAG/LEAD window queries write cold.
- **CNN mini-project** [AUTH], B-Claude: Month 1→2 seam, 16h cap, CIFAR-10 default, ship-at-threshold. Not wired into the capstone.
- **DagsHub account** (B-Manual): any time before M2 logging.
