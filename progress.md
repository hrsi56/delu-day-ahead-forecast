# Yarden's Triple-Track Progress Log

*Living document. Regenerated in full at the end of every session under the orchestrator-role.md regeneration contract. Last updated: **2026-06-11 (post-conversion audit)**.*

---

## Current Position

### Track A: Learning (Syllabus)
- **Anchor: `syllabus_v3_0.md` v3.0** (authored 2026-06-11; market-conversion alignment for capstone v6.0 — zero pace impact; math arc, depth labels, month structure, time budgets, SQL/CNN/C4 blocks untouched).
- **Phase:** I (Mathematical Foundations). **Month:** 0. **Week:** 1 (launched 2026-06-09).
- **L1 — DONE.** Strang L1–5 + Ch. 1–2; Gaussian-elimination solver shipped.
- **L2 — ACTIVE / in flight.** Strang L6–10 + Ch. 3, [AUTH], four fundamental subspaces; deliverable `four_subspaces(A)`.
- **Next: L3 ∥ Month-0 spike, after L2.** L3 — orthogonality → projections → least squares → Gram–Schmidt (OCW L14–17; verify index at briefing per C5-min); lands the OLS normal-equation deliverable. Then eigen L21–22 [AUTH]; determinants skim [REC]; SVD/PCA + condition number [REC] close Month 0.
- **Next pending checkpoint:** Month-0 **mid-month gate**, ~end of June — coding deliverable(s) runnable + NotebookLM consolidation verdict.

### Track B: Capstone Build
- **Anchor: `capstone_V6_0.md` v6.0** (ratified + audited 2026-06-11). DE-LU via ENTSO-E (primary) + SMARD (secondary). **Milestone: M0** (plan approved).
- **SPIKE BRIEF ISSUED 2026-06-12** — Month-0 ENTSO-E/SMARD de-risking spike (B-Claude, 6–8h hard cap, NOT an early M1). Eight probe questions in priority order: (1) end-to-end token access; (2) **R-2 vintage probe — A65/A01 + A69, harness + preliminary read, final verdict due before M1**; (3) per-series native resolution (PT15M expectation on feature feeds); (4) 15-min price boundary across 2025-10-01; (5) archive depth to 2019-01-01; (6) ENTSO-E↔SMARD cross-pull sample; (7) SMARD THE gas probe (feeds §0.3 reopen — report only); (8) SFTP path. Floor = 1–5 + skeleton + memo; stretch = 6–8. Output: feed-status memo (`docs/spike-feed-status.md`) + repo skeleton + first commits + CP-1 pre-confirmation paragraph.
- **Environment READY (2026-06-12):** ENTSO-E token granted early and loaded as `ENTSOE_API_TOKEN` in Claude Code env; GitHub repo created by Yarden; Claude Code configured with full repo permissions; gh CLI installed. **Pre-flight (stated in-chat): verify `CLAUDE.md` (refreshed engineer-role) + `capstone_V6_0.md` sit at repo root before pasting the brief.**
- **M1** lands in syllabus Month 2; CP-1 activates when M1 starts. M1 brief inherits the **v6.0 §12 binding list** + the audit addition (feature-feed PT15M→hourly aggregation per spike findings).
- **Last commit:** None yet (the spike delivers the first).
- **Pending clerical (B-Manual):** DagsHub account — Months 0–2 (precedes M2). HF account + Spaces — start of Month 5.
- **Next pending checkpoint:** CP-1 (at M1). Before that, the spike's feed-status memo is the de-facto gate on M1 readiness — **Yarden carries its CP-1 pre-confirmation paragraph + the R-2 preliminary read to the next session opening.**

### Track C: Marketing — FROZEN (one-off floor authorized; consumes NO CV-iteration slot)
- Phase-trigger fires continuous activation **after capstone M2** (projected mid-Month 3). Active applications no later than start of Month 5.
- **Geography RATIFIED:** ≤3 office days/week TLV/Herzliya; Beer Sheva base.
- **One-off C2 floor (execute this month):** 1. LinkedIn floor (headline, About, Featured: World Psychiatry, solver, event app) — **PENDING**; recruiter-only open-to-work deferred to M2 trigger. 2. README polish on solver + event-app repos — **PENDING**. 3. Lab-Engineer framing fix — **CLOSED**; do NOT re-add "(transitional role)".
- **C8-research (Month 0–1):** tiered Beer-Sheva-local + ≤3-day-hybrid DS target list. Not yet issued.
- **C7 networking floor (from Month 1, ~1h/week):** former students, BGU alumni, one Tech7 / Gav-Yam Negev meetup per month.
- **Positioning theme (held; survives the pivot):** career-changer from clinical research to industry DS — quantitative forecasting + honest uncertainty communication; World Psychiatry lead-analyst credibility + shipping experience; capstone with regime-aware methodology, walk-forward + embargo, KFT/LAG leakage audit, CQR-calibrated intervals, regime-stratified errors, cloud-backed reproducibility, deployed marimo showcase. "Why the German market, in Israel" carries the transfer answer.
- **Last published artifact:** None. **Pipeline:** empty. **Applications:** not started.
- **CV status:** over the bar to start applying. Three milestone-gated iteration slots remain (after M2, M3, M5).

---

## Setup State (one-time actions)

- **ENTSO-E API token — DONE 2026-06-12** (granted early; loaded as `ENTSOE_API_TOKEN` in Claude Code env).
- **Capstone repo — CREATED 2026-06-12** (GitHub; Claude Code full permissions; gh CLI installed). **Pre-flight pending confirmation: `CLAUDE.md` + `capstone_V6_0.md` at repo root** (instructed in-chat 2026-06-12; assume done once the spike runs).
- Project-knowledge + NotebookLM swaps — DONE 2026-06-11.

---

## Strategic Anchors

- **Target:** Industry Data Scientist role within ~6.5 months at NIS 35K. Capstone audience: DS hiring manager, not MLE.
- **Geography:** ≤3 office days/week TLV/Herzliya (ratified 2026-06-10); Beer Sheva base.
- **Anchor docs:** **`capstone_V6_0.md` v6.0** + **`syllabus_v3_0.md` v3.0** (ratified 2026-06-11; audited — consistent), `orchestrator-role.md` / `notebooklm-role.md` / `engineer-role.md` (refreshed 2026-06-11; engineer doc = repo `CLAUDE.md`). Decision records: `change-register-decisions.md`, `de-lu-conversion-memo`.
- **Depth labels:** [AUTH], [REC], [APPLIED-AUTH], [APPLIED-REC].
- **Budget:** $0 expected run rate; $65/month policy ceiling. Deployment $0.
- **Hardware:** Apple Silicon M3, 16 GB unified memory, CPU only.
- **Language:** English replies (Hebrew input fine).

---

## Standing Scope Decisions (carry forward indefinitely — do not allow back in)

- **Market = DE-LU via ENTSO-E + SMARD (ratified 2026-06-11).** PJM dead — do not revisit.
- **No gas/fuel-price layer.** Residual load carries the merit-order signal. **Single reopen:** spike confirms SMARD exposes a CC-BY THE day-ahead series → gas returns as a LAG feature only, never headline (v6.0 §0.3, §13).
- **Hourly target end-to-end across the 15-min MTU transition** (2025-10-01); quarter-hours averaged to hourly. Quarter-hourly target = named future work. Feature feeds likely PT15M from 2019 — aggregated to hourly on ingest (spike confirms).
- **No external weather.** Train-only Fourier climatology on the residual-load forecast series (v6.0 §0.5, §4.1).
- **No DVC.** Pinned deps + tagged commit + committed snapshot — **CC BY 4.0 with attribution** (v6.0 §9.3).
- **No live API pulls during user sessions.** Weekly manual snapshot refresh during the application phase.
- **No paid HF Spaces tier in baseline budget.** CPU Upgrade on standby for CP-5 cold-start only.
- **Single monolithic LightGBM** quantile ensemble. **No neural challenger** (SC3 rejected; shipped CNN + published evidence carry the question).
- **CQR (split conformal) only. No EnbPI / SPCI / Giacomini-White** — single pre-committed reopen (v6.0 §13): any regime stratum's coverage diverging >10 pp at M3 → EnbPI as remediation, comparison only.
- **LO3 REJECTED** — Month-0 SVD/PCA stays [REC]. **LO2 REJECTED** — no causal block.
- **Forecast + diagnostic report, not a trading product.**
- **Marimo is mandated.** Three sliders (Dunkelflaute toggle, headline perturbation, quantile selector) from the precomputed lookup with the per-cell OOD flag.
- **Walk-forward CV with 24h embargo, three-regime pinned fold scheme** (v6.0 §5.1: crisis-peak F3 Jul–Sep 2022; negative-price F4 May–Jul 2025; F5 current tail, fully post-15-min-transition).
- **Stranger-test gate happens on the deployed HF Spaces URL.**
- **Thin GitHub Actions CI on the §9.4 invariant tests is IN** (lands at M2; four mandatory tests incl. the 15-min boundary) — no regression matrix.
- **CP-2 secondary gate pre-committed:** Fold-5 DM p ∈ [0.05, 0.15] + pooled-across-folds DM significant → M2 passes, both numbers reported. **Comparator = similar-day naïve (Lago convention).** Fixed before results.
- **Headline-feature rule:** `residual_load_deviation_from_normal` primary; `scarcity_stress = relu(load_z)·relu(−vre_z)` secondary; SHAP at M3 decides. `gas_to_load_ratio` stays dead.

---

## Session Log (newest first)

- **2026-06-12 — Spike brief issued.** Token arrived early (loaded as `ENTSOE_API_TOKEN`); repo created + Claude Code configured + gh CLI installed (all Yarden, 2026-06-12). Pre-flight instructed: CLAUDE.md + capstone_V6_0.md at repo root. Eight-question spike brief delivered (floor 1–5, stretch 6–8; R-2 harness may leave a pending verdict with re-run path). Token-grant blocker CLOSED.
- **2026-06-11 (audit) — Post-conversion full-set audit PASSED.** Two spike-scope additions (feature-feed native resolution; vintage probe extended to A65/A01); one cosmetic M1 note (Dec-2024 peak figure). All file swaps confirmed done.
- **2026-06-11 (roles) — Three role docs refreshed** (DE-LU alignment + small hardenings; owner-waived progress that session).
- **2026-06-11 (syllabus) — `syllabus_v3_0.md` authored** (full v2.3 audit; math arc/pace untouched).
- **2026-06-11 (respec) — `capstone_V6_0.md` authored + ratified** (PJM→DE-LU; §6–§10 verbatim; standing decisions amended).
- **2026-06-11 — Conversion memo delivered; PJM confirmed geo-blocked; ENTSO-E open; token email sent; NotebookLM swap #1; L2 started.**
- **2026-06-10 — Orchestrator amendments; L1 done → L2 issued; change-register adjudication (v5.5 + v2.3 ratified).**
- **2026-06-09 — Program launch; L1 issued.** **2026-05-31 — Baseline.**
---

## Blockers / Open Questions

- ~~ENTSO-E token grant~~ — **RESOLVED 2026-06-12** (arrived early).
- None other outstanding.

---

## Notes for Future Sessions

- **Next session opening:** Yarden carries the spike's CP-1 pre-confirmation paragraph + the **R-2 preliminary read** (and the gas-probe yes/no for the §0.3 reopen decision, orchestrator's call). If the R-2 cross-day comparison is pending, schedule its re-run.
- **L3 brief (when triggered):** OCW L14–17 (verify index per C5-min) — OLS normal-equation deliverable. Then eigen L21–22 [AUTH]; determinants skim [REC]; SVD/PCA + condition number [REC] close Month 0 (collinearity example: load×residual-load per v3.0).
- **M1 brief (syllabus Month 2):** inherits v6.0 §12 binding list + feature-feed PT15M→hourly aggregation per spike findings.
- **M1 cosmetic:** verify Dec-2024 / Jan-2025 Dunkelflaute peaks against pulled data; tighten the §2.2 narrative sentence in the report.
- **SQL authoring block** [APPLIED-AUTH]: parallel filler Months 2–3, 20h cap; toy table `ts, price, load, wind, solar`; done when LAG/LEAD window queries write cold.
- **CNN mini-project** [AUTH], B-Claude: Month 1→2 seam, 16h cap, CIFAR-10 default, ship-at-threshold. Not wired into the capstone.
- **C4 placements:** A/B testing [REC, ~4h] rides Month 1; classification & metrics [AUTH-light, 10–12h] early Month 3; timed take-homes late Month 3 + Month 4; mocks ×2–3 late Month 4 → Month 5.
- **Best interview lines to protect:** KFT/LAG leakage audit @ 12:00 CET gate; exchangeability paragraph (verbatim); negative-Q / isotonic-last; change-point validation of the crisis flags; regime-stratified story w/ crisis-peak F3 + negative-price F4; R-2 vintage honesty line; two-sided bounded tail (−500 live; −600 from 2026-05-28); model-staleness; "why the German market, in Israel" + "why hourly" + "why no gas" + negative-prices/no-log + "why marimo" + "why thin CI".
- **CP-5 cold-start:** 30s backstop; Actions cron auto-disables after 60 days of repo inactivity — README disclaimer is the real backstop.
- **CV iteration cadence:** three milestone-gated slots (after M2, M3, M5).
- **Track C flips:** recruiter-only open-to-work at the M2 phase-trigger; applications no later than start of Month 5.
- **Routing reminder:** the orchestrator never writes Claude Code prompts; M briefs inherit the v6.0 §12 binding list rather than restating the spec.
