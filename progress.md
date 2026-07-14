# Yarden's Triple-Track Progress Log

*Living document. Regenerated in full under the orchestrator-role.md regeneration contract. Last updated: **2026-07-12 (expansion ratified — anchors → syllabus v3.1 / capstone v6.2 / companion v1.0 / map v3; track positions unchanged: L5 active, G0 next).***

---

## Current Position

### Track A: Learning (Syllabus)

- **Anchor: `syllabus_v3_1.md` v3.1** (expansion ratified 2026-07-12; supersedes v3.0).
- **Phase:** I (Mathematical Foundations). **Month:** 0, week 5 (launched 2026-06-09).
- **L1 — DONE.** Strang L1–5 + Ch. 1–2; Gaussian-elimination solver shipped.
- **L2 — DONE (2026-07-02).** Four fundamental subspaces; `four_subspaces(A)` shipped.
- **L3 — DONE (2026-07-05).** Orthogonality → projections → least squares → Gram–Schmidt; OLS normal-equation deliverable (Month-0 deliverable #1).
- **G0-mid — CLOSED (2026-07-06).** Artifacts clean; L1–L3 core solid at [AUTH]. Flagged gap (AᵀA geometry ↔ eigenvalues ↔ condition number) folded into L4 as remediation emphasis.
- **L4 — DONE (2026-07-12, Yarden-reported).** Eigen/diagonalization [AUTH]; AᵀA remediation emphasis; deliverables per contract: symmetric 3×3 diagonalization (hand + NumPy) + AᵀA ellipse/eigenvalue-ratio artifact + AᵀA → SVD bridge paragraph.
- **L5 — NEXT (CHECKPOINT BLOCK — closes Month 0).** SVD/PCA + condition number; Month-0 deliverable #2 (PCA + condition-number toy on synthetic load/wind/solar/residual-load with mechanical correlation) + written interview answer + **G0 consolidation verdict**, which must explicitly confirm the G0-mid flagged gap is closed.
  - **v3.1 PCA-upgrade incorporated:** v3.1 raises PCA to **[APPLIED-AUTH]** (LO3 partial reopen — SVD framing + Eckart–Young stay [REC]). this upgrade is folded directly in-block L5. The deliverable standard is the [APPLIED-AUTH] one (explain variance-explained, when/why/limits, defend cold).
- **Pace:** on-plan for Month 0; Month-0 six-week envelope ends ~2026-07-21; L5 is the last block and has ~9 days. **Whole-program envelope stretched by the expansion:** ~+180h net (~500→~680h), Months 2–4 each ~5–5.5 wks at 20–22h/wk; **G5 (flagship live) ~mid/late-Jan 2027; G6 (companion) ~Mar 2027.** Fixed anchors unchanged: applications from start of Month 5; ALG closes at G4.
- **Next pending checkpoint:** **Issue L5.** after that, **G0 (Month-0 close)** — one-line status after L5: deliverables #1–#2 runnable + consolidation verdict incl. gap-closure statement.
- **After G0:** Month 1 opens (distributions → MLE → hypothesis testing (+C4-2 rider) → bootstrap → Bayes [REC]; **+ new v3.1 L-MTX 18.065 matrix rider [REC, ~4h]**; pandas TS week → domain reading → change-point [APPLIED-AUTH]); C7 networking floor begins.

### Track B: Capstone Build

- **Anchor (flagship): `capstone_V6_2.md` v6.2** (in PK; **repo `main` + NotebookLM swap PENDING — see Setup State**). **Milestone: M0 done**; data-layer de-risking arc CLOSED; no open capstone actions.
- **Companion anchor (stage-gated): `Binary Classification Mini-Capstone.md` v1.0** (IEEE-CIS fraud detection). **Not read/briefed/consumed before its arc (B-Man3 in Month 5, FM0 onward in Months 6–7).** Second Track B artifact; runs inside the active application phase.
- **M1** lands in syllabus Month 2; **CP-1 activates at M1**; brief inherits the v6.2 §12 binding list — **now including the §4.2 spectral-EDA block** (module + 3 mandatory figures + README ¶; briefable inside M1 or as a follow-on B-Claude block, closing before CP-1). Spike pre-confirmed CP-1 items 1 (full), 3 (sample-level), 5 (VERIFIED).
- **Pending clerical (B-Manual):** DagsHub account — before M2. Optional pre-M1: 10-min SMARD gas-page browser check (map row B-Man0). **Month 5:** Kaggle account + API token + accept `ieee-fraud-detection` rules (B-Man3) — unblocks FM0.
- **Next pending checkpoint:** CP-1 (at M1) — now carries the three v6.2 spectral checklist items.

### Track C: Marketing — FROZEN (one-off floor authorized; consumes NO CV-iteration slot)

- Phase-trigger fires after capstone M2 (projected mid-Month 3). Active applications no later than start of Month 5. **From Month 6 the funnel runs on both artifacts** (flagship + companion).
- **Geography RATIFIED:** ≤3 office days/week TLV/Herzliya; Beer Sheva base.
- **One-off C2 floor (authorized 2026-06-10) — still PENDING:** 1. LinkedIn floor (headline, About, Featured: World Psychiatry, solver, event app) — PENDING; recruiter-only open-to-work deferred to M2 trigger. 2. README polish on solver + event-app repos — PENDING. 3. Lab-Engineer framing fix — CLOSED; do NOT re-add "(transitional role)".
- **C8-research (window Months 0–1):** tiered Beer-Sheva-local + ≤3-day-hybrid DS target list. Not yet issued. **v3.1 dependency:** its take-home-vs-live-screen ratio now feeds **DEC-ALG at G3** (the ALG downgrade decision).
- **C2 + C8 scheduling — DEFAULT SET 2026-07-12 (awaiting veto):** deferred to the Month-0→1 seam, bundled as one short Track C session right after G0.
- **C7 networking floor (from Month 1, ~1h/week):** former students, BGU alumni, one Tech7 / Gav-Yam Negev meetup per month.
- **Positioning theme (held, +v3.1 companion angle):** career-changer from clinical research to industry DS — quantitative forecasting + honest uncertainty communication; World Psychiatry lead-analyst credibility + shipping experience; flagship with regime-aware methodology, walk-forward + embargo, KFT/LAG leakage audit, CQR-calibrated intervals, regime-stratified errors, cloud-backed reproducibility, deployed marimo showcase (+ spectral-EDA differentiator). Companion fraud artifact adds the decisioning counterpart (class imbalance, cost-based thresholds, calibration) aligned with the Beer-Sheva fraud/cyber weighting. "Why the German market, in Israel" carries the transfer answer.
- **Last published artifact:** None. **Pipeline:** empty. **Applications:** not started.
- **CV status:** over the bar to start applying. Three milestone-gated iteration slots remain (after M2, M3, M5). **Post-slots:** the companion demo reaches the market via a manual portfolio-surface update (C-Man-P), not a fourth CV iteration.

---

## Setup State (one-time actions)

- **ACTION-REQUIRED — v6.2 + v3.1 sync (ratified 2026-07-12):**
  - `capstone_V6_2.md` → **repo `main`** (commit) and **NotebookLM source swap** (version guard) — PENDING (PK confirmed done).
  - `syllabus_v3_1.md` → **NotebookLM source swap** (version guard) — PENDING (PK confirmed done).
  - `Binary Classification Mini-Capstone.md` v1.0 → **PK confirmed present; do NOT load into NotebookLM or any brief until FM0.**
  - `program-stage-sequence.md` **v3 swap** — PENDING confirmation of mount (v3 delivered 2026-07-12; replaces v2).
  - `orchestrator-role.md` **2026-07-12 revision** (two-artifact Track B, companion stage-gate, envelope update) — PENDING confirmation as active project prompt.
- Earlier items — all DONE (compressed): map v2 swap (2026-07-05), orchestrator-role 2026-07-02 revision, v6.1 swaps (PK + NotebookLM + repo), repo rename → `hrsi56/delu-day-ahead-forecast`, spike branch merge, SFTP check (Q8 closed), ENTSO-E token, repo + CLAUDE.md + capstone at root.

---

## Strategic Anchors

- **Target:** Industry Data Scientist role at NIS 35K. Capstone audience: DS hiring manager, not MLE. **Envelope (v3.1 expansion):** flagship live at G5 ~mid/late-Jan 2027; companion at G6 ~Mar 2027; in-market from start of Month 5. Dates = envelope, not a signed-offer guarantee.
- **Geography:** ≤3 office days/week TLV/Herzliya (ratified 2026-06-10); Beer Sheva base.
- **Anchor docs:** **`capstone_V6_2.md` v6.2** (flagship) + **`Binary Classification Mini-Capstone.md` v1.0** (companion, stage-gated) + **`syllabus_v3_1.md` v3.1**; role docs: `orchestrator-role.md` (rev 2026-07-12), `notebooklm-role.md`, engineer doc = repo `CLAUDE.md` (per-repo). Planning aid (non-anchor): `program-stage-sequence.md` v3 (2026-07-12). Decision records: `change-register-decisions.md`, `de-lu-conversion-memo`, `docs/spike-feed-status.md` (in-repo); superseded specs (historical, merged into anchors): four-course gap analysis, spectral-extension-spec v1.0, algorithms-block-spec v1.0.
- **Repos:** flagship `hrsi56/delu-day-ahead-forecast`; companion fraud repo created at FM0 (its own `CLAUDE.md` + companion plan).
- **Depth labels:** [AUTH], [REC], [APPLIED-AUTH], [APPLIED-REC].
- **Budget:** $0 expected run rate; $65/month policy ceiling. Deployment $0. Applies to both repos.
- **Hardware:** Apple Silicon M3, 16 GB unified memory, CPU only.
- **Language:** English replies (Hebrew input fine).

---

## Standing Scope Decisions (carry forward indefinitely — do not allow back in)

- **v3.1 EXPANSION RATIFIED (2026-07-12), optimizing hire probability over calendar.** Adds (all in `syllabus_v3_1.md` / `capstone_V6_2.md`): first-principles optimization block **L-OPT [AUTH]** at the seam (18.065 L21–23, L25) + NN/backprop + optional Fourier **DL+ riders**; Month-1 **L-MTX** matrix rider [REC]; Month-2 **spectral-EDA block [APPLIED-AUTH]** (capstone §4.2, R-5, one showcase figure at M4, 3 CP-1 items, 3 §13 interview Q&As); **CLS-1 [AUTH]** classification arc (supersedes C4-1) + **CLS-2**; **ALG interview-algorithms block [APPLIED-AUTH]** (~48h, staggered Months 2–4, NeetCode-subset + 6.006 backbone, capstone-wins conflict rule, DEC-ALG downgrade rule at G3); Month-4 **UNSUP**, **CAUS**, **ERR rider**; the **companion fraud mini-capstone** (Months 6–7). Guardrails to enforce: hard caps, R-5 (spectral scope creep), DEC-ALG, the capstone-wins weekly conflict rule.
- **LO3 — PARTIALLY REOPENED (2026-07-12):** PCA → **[APPLIED-AUTH]** on interview-frequency grounds; **the [AUTH] SVD arc + Eckart–Young stay [REC]/rejected** (original substance holds). **LO2 — REOPENED in light form** as the Month-4 CAUS block (causal frame [REC] + A/B design [APPLIED-AUTH]); **the capstone's no-causal-claim boundary is untouched.**
- **CLS-1 supersedes C4-1** — wherever any doc/brief says C4-1, read CLS-1. Do not run both.
- **Spectral-EDA is capstone scope, NOT a firewalled supplementary block** (the one v3.1 exception; capstone §4.2). Descriptive only — no filters/wavelets/frequency-domain forecasting; no spectral features in the model catalog at v6.2.
- **Market = DE-LU via ENTSO-E + SMARD (ratified 2026-06-11).** PJM dead — do not revisit.
- **No gas/fuel-price layer — reopen ADJUDICATED NOT MET 2026-06-12, omission FINAL.** SMARD API exposes gas generation volume only, no THE price. Narrow residual: optional pre-M1 browser check of SMARD's JS gas page; re-opens only if it reveals a CC-BY, API-accessible daily THE **price** series (v6.2 §0.3, §13).
- **R-2 vintage — VERIFIED stable (2026-06-14):** TP archive preserves as-published A65/A01 + A69/A01 values (no overwrite); as-archived treatment documented and empirically backed. VRE initial publication is post-gate; the caveat is structural, stated, shared with every published EPF benchmark.
- **Data access — confirmed from two independent sources** (ENTSO-E API primary, SMARD fallback-primary over HTTP). SFTP route unavailable from Yarden's networks — not needed.
- **Hourly target end-to-end across the 15-min MTU transition** (2025-10-01); quarter-hours averaged to hourly (spike-validated). **Feature feeds natively PT15M from 2019 — uniform hourly aggregation at ingest; chunk-boundary bin integrity mandatory** (v6.2 §4.0). Quarter-hourly target = named future work.
- **No external weather.** Train-only Fourier climatology on the residual-load forecast series (v6.2 §0.5, §4.1).
- **No DVC.** Pinned deps + tagged commit + committed snapshot — **CC BY 4.0 with attribution** (v6.2 §9.3). `entsoe-py` pinned 0.8.0.
- **No live API pulls during user sessions.** Weekly manual snapshot refresh during the application phase.
- **No paid HF Spaces tier in baseline budget.** CPU Upgrade on standby for CP-5 cold-start only.
- **Single monolithic LightGBM** quantile ensemble (flagship). **No neural challenger** (SC3 rejected; shipped CNN + published evidence carry the question).
- **CQR (split conformal) only. No EnbPI / SPCI / Giacomini-White** — single pre-committed reopen (v6.2 §13): any regime stratum's coverage diverging >10 pp at M3 → EnbPI as remediation, comparison only.
- **Forecast + diagnostic report, not a trading product.**
- **Marimo is mandated (flagship).** Three sliders (Dunkelflaute toggle, headline perturbation, quantile selector) from the precomputed lookup with the per-cell OOD flag. **+ v6.2:** one static spectral showcase section (labeled periodogram + one ¶), **no spectral slider.** *(Companion demo uses Gradio — separate artifact, FM4.)*
- **Walk-forward CV with 24h embargo, three-regime pinned fold scheme** (v6.2 §5.1: crisis-peak F3 Jul–Sep 2022; negative-price F4 May–Jul 2025; F5 current tail, fully post-15-min-transition).
- **Stranger-test gate happens on the deployed HF Spaces URL.**
- **Thin GitHub Actions CI on the §9.4 invariant tests is IN** (lands at M2; four mandatory tests incl. the extended 15-min aggregation-integrity test) — no regression matrix.
- **CP-2 secondary gate pre-committed:** Fold-5 DM p ∈ [0.05, 0.15] + pooled-across-folds DM significant → M2 passes, both numbers reported. **Comparator = similar-day naïve (Lago convention).** Fixed before results.
- **Headline-feature rule:** `residual_load_deviation_from_normal` primary; `scarcity_stress = relu(load_z)·relu(−vre_z)` secondary; SHAP at M3 decides. `gas_to_load_ratio` stays dead.

---

## Session Log (newest first)

- **2026-07-12 (state-change regen, no position advance) — EXPANSION RATIFIED.** Four documents merged into law: `syllabus_v3_1.md`, `capstone_V6_2.md`, `Binary Classification Mini-Capstone.md` v1.0, `program-stage-sequence.md` v3; `orchestrator-role.md` rev 2026-07-12 (two-artifact Track B + companion stage-gate). Source chain: four-course gap analysis → spectral + algorithms specs → capstone v6.2 amendment sheet (applied) → syllabus v3.1 amendment sheet (applied). LO3 partially reopened (PCA→[APPLIED-AUTH]); LO2 reopened (CAUS). PCA-upgrade rider parked for Month 1 (L5 already issued under old ceiling). Track positions unchanged: L5 active, G0 next, Track B at M0. Sync actions logged in Setup State.
- **2026-07-12 — L4 closed (Yarden-reported).**
- **2026-07-06 — G0-mid CLOSED clean; L4 reissued (ACTIVE).** Verdict: artifacts clean; L1–L3 solid at [AUTH]; flagged gap = AᵀA geometry ↔ eigenvalues ↔ condition-number → folded into L4 as remediation emphasis; determinants/Jordan floor-demonstrated.
- **2026-07-05 — L3 closed; G0-mid checkpoint block + L4 issued.** Same day: stage-map audit → map v2 authored + swapped; orchestrator-role 2026-07-02 revision confirmed live.
- **2026-07-02 — L2 closed; L3 issued** (not a checkpoint block).
- **2026-06-14 — Data-layer arc closed; L2 resumed.** Q8 SFTP blocked → closed, no impact. Spike merged to `main`. v6.1 swaps confirmed. R-2 verdict stands.
- **2026-06 (compressed) —** R-2 verdict closed (CP-1 item 5 VERIFIED, 06-14); R-2 harness + spike adjudication → v6.1 (06-12); conversion memo PJM→DE-LU, `capstone_V6_0` + `syllabus_v3_0` authored (06-11); amendments + change-register adjudication (06-10); program launch, L1 issued (06-09); baseline (05-31).

---

## Blockers / Open Questions

- **v6.2 / v3.1 / map-v3 / orchestrator sync — PENDING confirmation** (see Setup State). Closes on Yarden confirming each swap/mount. Until the repo + NotebookLM swaps land, Claude Code and NotebookLM still hold v6.1/v3.0 — flag if any Month-2 brief issues before the repo swap.
- **C2 floor + C8 research:** default set 2026-07-12 — **defer to the Month-0→1 seam, bundle as one short Track C session right after G0.** Stands unless Yarden vetoes; closes on his confirmation or on execution at the seam.
- Optional, non-blocking: 10-min SMARD JS gas-page browser check (pre-M1, epistemic closure on §0.3 — boundary stands either way); `.zshrc` line 137 dangling-source warning, cosmetic.

---

## Notes for Future Sessions

- **Next opening:** Issue **L5 block**. At this opening, also **confirm the pending v6.2/v3.1/map/orchestrator swaps**. Once L5 is completed, the following opening will require the **G0 one-liner** (both Month-0 deliverables runnable + consolidation verdict incl. explicit AᵀA-gap-closure statement) to close Month 0.
- **Month-1 planning (at G0):** L6–L13 per map v3; **+ L-MTX [REC, ~4h]** (18.065 L5/L8/L9/L10); C7 networking floor starts; C4-2 rider attaches to hypothesis-testing; pandas TS week + domain reading parallel; change-point [APPLIED-AUTH] closes → G1.
- **Seam (Month 1→2, ~2 wks):** **L-OPT [AUTH, ~10h]** (18.065 L21–23, L25; CS229 L2 [REC]) runs **before** the CNN; **DL+ riders (~5h)** NN/backprop [REC] (18.065 L26–27) + optional Fourier (L31–32) with the CNN.
- **M1 brief (syllabus Month 2):** inherits the **v6.2 §12 binding list** (now incl. the **§4.2 spectral-EDA block** — module + 3 figures + README ¶ + R-5) + M1 cosmetic (verify Dec-2024 / Jan-2025 Dunkelflaute peaks; tighten §2.2 sentence). **SPEC** briefable inside M1 or as a follow-on B-Claude block, closing before CP-1.
- **Month-2 parallel starts:** **SQL** [APPLIED-AUTH] (Months 2–3, 20h cap; done when LAG/LEAD write cold) **+ ALG-1** light start (~8h: Arrays/Hashing + Two Pointers, 6.006 L4, solutions repo + progress_log).
- **Month 3:** **CLS-1 [AUTH, ~12h]** (supersedes C4-1) + **CLS-2 (~8h)**; **ALG-2 ramp (~20h)**; take-home rehearsal #1 on a classification dataset; **DEC-ALG at G3** (downgrade ALG if ≥80% of the funnel is take-home format).
- **Month 4:** **ALG-3 peak + close at G4** (mocks: ≥4 × 25-min); **UNSUP (~7h)**, **CAUS (~6h)**, **ERR rider (~3h)** parallel.
- **Month 5:** **B-Man3** (Kaggle account + token + accept `ieee-fraud-detection` rules) unblocks FM0; three spectral interview Q&As in the L31 prep block.
- **Companion arc (Months 6–7, stage-gated):** FM0–FM5 / FCP-1–5 per map v3; **do not read or brief the companion plan before FM0.** Runs inside the application phase; theory (CLS-1/2, UNSUP) already complete by end of Month 4.
- **DagsHub account** (B-Manual): any time before M2 logging.
