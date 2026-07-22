# syllabus_v3_1 → v3_2 — Amendment Sheet

*Authored 2026-07-22 by the orchestrator. Aligns the syllabus with **`capstone_V6_3.md` v6.3** (the strict-gate methodology amendment) and repairs two classes of stale content that predate it. The changes are **already applied** in `syllabus_v3_2.md`; this sheet is the change record for the amendment chain. No math-arc content, month structure, depth-label vocabulary, or historical delta entry was deleted. The SQL-A/SQL-B split is net-zero; the v6.3 offline-health rider adds at most ~8 h; the Month-2–4 labels now reflect the already-approved ~5–5.5-week pace; and the stale 6–6.5-month completion header is superseded by the ≈705 h envelope (G5 ~late-Jan/early-Feb 2027; G6 ~late-Mar/early-Apr 2027), with active applications still opening after G3 and no later than Month 5. All prior rejected-item records (LO3, LO2, SC3-learn, SC5-learn) carry forward unchanged.*

**Two drivers.** (1) The v6.3 capstone amendment changes what the shipped model may consume (strict-gate; A69 excluded) and reconciles the SQL supplementary block with a DuckDB production mart — both of which the syllabus must teach correctly. (2) A **pre-existing staleness**: the syllabus's Month-5 deployment rows were never updated when the **D7 static-page rider** landed (2026-07-20), so they still taught the deleted GitHub-Actions keep-alive cron and a Spaces-first portfolio URL. This amendment repairs both.

---

## AMD-1 — Version bump (title, header, anchors, new delta)

- Title → **v3.2 — for capstone_V6_3.md v6.3**; header interleave line and the depth-label deliverable-link line → v6.3; the §13-boundary intro ("tied to `capstone_V6_2.md` v6.2") → v6.3; the Month-5 self-rehearsal anchor → v6.3; operative `v6.2 §13` teaching references → `v6.3 §13`.
- New `v3.1 → v3.2 delta` entry appended after the v3.0→v3.1 delta. **All operative capstone references now point to v6.3**; capstone section numbers are unchanged (v6.3 added §7.2/§9.5/§9.6, renumbered nothing), so existing §-links resolve.

## AMD-2 — SQL block reconciled with DuckDB (SQL block + firewall note)

- **Setup note:** DuckDB is the block's **real database** (reads the capstone Parquet natively) — the toy Postgres/Supabase table is removed.
- **Placement & cap:** the 20-hour cap is preserved and **split SQL-A / SQL-B** — SQL-A a minimal production subset authored at **M1 before CP-1** and integrated + tested as the capstone's DuckDB mart (capstone §9.6); SQL-B the interview-fluency remainder through **G3**.
- **Window-function row:** the polished queries are the capstone mart, not disconnected drill.
- **Firewall note:** the deliberate exceptions become **two** — spectral-EDA and the SQL-A production subset; ALG / CLS-1/2 / UNSUP / CAUS / SQL-B stay firewalled.

## AMD-3 — Stale D7 deployment lines repaired (Month-5 rows)

- HF-Spaces mechanics row: the **GitHub-Actions keep-alive cron is deleted**; the **static GitHub Pages export is the primary portfolio URL**; CPU Upgrade is cold-start mitigation only.
- Capstone-interleave M5 line: no keep-alive cron; static Pages live as the primary URL; CV/LinkedIn link the **Pages URL as primary**, Spaces + MLflow beneath.
- Stranger-test line: **starts at the static Pages URL (< 3 s cold-cache)**, follows the labeled link to the Space.
- CV iteration window (after M5): the **static Pages URL** is the primary portfolio link.

## AMD-4 — A69 / residual-load / R-2 teaching updated to strict-gate

- **Month-1 feature-catalog line:** gate-feasible candidates (one-feature residual arm {`gate_feasible_residual_load_proxy`} and `expected_scarcity_proxy`) share one pinned seasonal-diurnal VRE expectation fit on proper-training-only aggregate A75 (fit target, never runtime), then are decided by M2/CP-2 matched ablation (no pre-ratified headline or lagged-vintage choice); delivery-day A69 is excluded from champion runtime and confined to the §7.2 benchmark; the DuckDB SQL-A mart is canonical.
- **Month-4 SHAP interleave line:** SHAP *explains* the frozen champion's retained features — it does not select; the A69-based `dunkelflaute_flag` appears only in the §7.2 benchmark.
- **Month-5 interview-prep line:** the R-2 "as-archived, same convention as the literature" honesty line → the **strict-gate answer** (A69 post-gate → excluded; gate-feasible proxies; the §7.2 benchmark measures the cost).
- **MLOps-boundary line:** "Under v6.3 …" plus a note that the v6.3 offline data/output-health report (capstone §9.5) is a batch report, not production monitoring.

## AMD-5 — Slider set de-ratified (Month-5 marimo row)

The "three interactive sliders (Dunkelflaute toggle, headline perturbation, quantile selector)" → **sliders drawn from the champion's retained features**, set at CP-4 (quantile selector fixed; no A69-based Dunkelflaute toggle).

## AMD-6 — Track C funnel reconciled

Post-M2 Track C activity is **outreach / prep / pipeline-building only**; **all active submissions gate on SQL-B completion (G3)**; the start-of-Month-5 backstop is unchanged.

## What this amendment does NOT do

- **No syllabus C8 row is invented.** C8's take-home / SQL / A-B / cloud / LLM requirement-ratio scope lives in **progress.md's durable C8 scope and the stage map's C8 row**, not here; the syllabus only *references* C8-dependent decisions (e.g. DEC-ALG). 
- No change to the math arc, the CLS/ALG/UNSUP/CAUS blocks, or the companion pointer.

## Corrective semantic-audit pass (2026-07-22)

- Month 2–4 duration labels now match the approved load model (~5, ~5–5.5, ~5.5 weeks); no curriculum topic was added by that relabel.
- M2/CP-2 now states the **exact four-catalog ablation**, deterministic selection, and catalog freeze; CQR/isotonic are not implemented until M3.
- M3/CP-3 now carries CQR → isotonic-last, all three reliability stages, the final-output coverage gate, and the separately calibrated §7.2 five-metric benchmark.
- Price spectral EDA justifies calendar structure and only motivates testing the residual candidate; it cannot validate or retain that candidate. Per-regime spectra motivate regime-stratified reporting but do not set fold boundaries or prevent leakage. Residual/gas/collinearity interview language is conditional on the CP-2 outcome.
- Operative dependency references use **`entsoe-py==0.8.0`**, matching `pyproject.toml` and `uv.lock`.
- The SQL split remains inside its 20 h cap; the §7.2 comparison is absorbed into the existing M3 diagnostic block; the offline-health report is the only explicit v6.3 load addition (**≤~8 h**).

## After applying — distribution

`syllabus_v3_2.md` swaps into **Project Knowledge** and **NotebookLM** (with capstone v6.3). Record each swap separately in progress.md. The map (v5) and the AWS draft are **not** loaded into NotebookLM.
