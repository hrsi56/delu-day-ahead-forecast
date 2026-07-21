# capstone_V6_2 → V6_3 — Amendment Sheet

*Authored 2026-07-22 by the orchestrator. Records the **strict-gate methodology amendment** that absorbs the external Codex audit under owner ratification (2026-07-22). Unlike the additive v6.1→v6.2 sheet, this amendment **reworks methodology** — it changes what the shipped model may consume — so it carries a real version bump. The changes are **already applied** in `capstone_V6_3.md` (authored directly, not deferred to a B-Claude apply pass); this sheet is the change record for the amendment chain. No historical chronicle text, no §0 ratified decision, and no surviving §13 boundary was deleted; the v6.0/v6.1/v6.2 delta entries carry forward verbatim.*

**Provenance.** Codex reviewed `capstone_V6_2.md` only (not the syllabus/companion). The orchestrator adjudicated its findings across three review rounds; the owner ratified the strict-gate core plus eight binding execution/governance corrections (recorded in the session plan and progress.md). The gap-% and job-fit scores in the audit are **not** adopted as targets — they undercount the program (SQL has a track, A/B rides the Month-4 CAUS block, classification is the companion).

**Core change.** The Month-0 spike proved that **A69 (the DA wind/solar forecast) is published after the 12:00 gate**, so it is **not known-at-forecast-time**. v6.3 therefore **forbids A69 and every A69-derived feature from the shipped champion**, replaces them with **gate-feasible candidate proxies** whose value is *earned* by matched ablation, and moves A69 into a controlled **post-gate information benchmark** that quantifies the cost of feasibility but never ships.

---

## AMD-1 — Version bump (header, chronicle, §12 M0)

- Title → **v6.3**; end-of-document line → v6.3.
- New chronicle entry after the v6.2+D7 entry: the `v6.2 → v6.3 (2026-07-22; strict-gate methodology amendment + audit-driven corrections)` paragraph (eight numbered items).
- §12 M0 stamp updated: "v6.3 … the **v6.3 strict-gate methodology amendment ratified 2026-07-22**."

## AMD-2 — Strict-gate champion; A69 excluded (§0 items 3/5, §1, §3, §4, §5.2, §11 R-2)

- **§0 item 3** — merit-order signal carried by "a **gate-feasible residual-load proxy**" (A69-based construction confined to the §7 benchmark).
- **§0 item 5** — the champion's climatology fits on the **gate-feasible** proxy series.
- **§1** — constraint list: the CQR bullet gains the three-stage-coverage clause; the slider clause de-ratified (below, AMD-6).
- **§3** — feature table A69 cell marked "post-gate → benchmark-only, never champion features"; the KFT-foundation paragraph rewritten from "as-archived is the expected operative path" to "A69 not KFT → excluded from the champion schema → gate-feasible proxies + §7 benchmark."
- **§4 header + entries** — KFT/LAG note that A69 is neither for the champion; "VRE forecasts" → post-gate/benchmark-only; "Residual load" → two constructions (A69-based benchmark; gate-feasible proxy champion); `dunkelflaute_flag` → post-gate, benchmark-only or evaluation stratum.
- **§5.2** — leakage audit: KFT bullet drops `dunkelflaute_flag`; the VRE bullet becomes the strict-gate resolution with **point-in-time-provenance** requirement; forecast-not-actual guard → **champion/benchmark schema separation** (AMD-7).
- **§11 R-2** — retitled "resolved by strict-gate design"; risk eliminated for the champion by construction; residual concerns are benchmark-only. **R-1** mitigations: `dunkelflaute_flag` reclassified stratum/benchmark.

## AMD-3 — No pre-ratified headline; M2/CP-2 matched-ablation selection (§4.1)

- §4.1 retitled "Domain-insight candidates (gate-feasible; headline decided at M2/CP-2)."
- Candidates: `gate_feasible_residual_load_proxy`, `expected_scarcity_proxy` (honestly named — a proxy cannot identify tomorrow's *actual* Dunkelflaute).
- **Selection rule** replaced: four pre-specified matched catalogs (strict base; +residual proxy; +scarcity proxy; +both — the 2×2 guards redundancy/interaction). **Retention rule fixed before results:** primary metric = pooled mean pinball loss; retained iff ≥1% relative improvement, raw-head 80% coverage not degraded >2 pp, stable on ≥4/5 folds. Winning catalog **frozen at CP-2 before M3**. **SHAP at M3 explains, is not the incremental-value test.** **"No candidate survives" is acceptable** → champion ships with no forced headline.

## AMD-4 — Post-gate information benchmark (new §7.2)

Controlled ablation from the frozen CP-2 catalog: strict vs. A69-augmented, identical eval rows/folds/base features/preprocessing/seeds/tuning budget/calibration windows, **each variant calibrated separately**, differing only by A69 and its derivatives. Reports five named metrics — MAE, mean pinball loss, empirical coverage, mean interval width, **calibration error** (mean absolute nominal−empirical coverage gap across 50/80/95). **Never the champion.**

## AMD-5 — Three-stage coverage (§1, §6.2, §8.4, §9.4, §10, CP-3, §13)

Coverage reported at raw / post-CQR-pre-isotonic / final-post-isotonic. **The formal marginal guarantee attaches only to the post-CQR stage; final coverage is empirical.** Reliability diagram (§8.4) shows all three; §6.2 coverage claim rewritten; §13 gains the isotonic/CQR interview defense.

## AMD-6 — SHAP/CQR gates de-biased; sliders downstream of selection (§8.1, §9.2, CP-3, CP-4/CP-5)

- **CP-3** — the named-feature requirement (old line 351) **removed**; the SHAP↔permutation overlap (old line 352) made **descriptive, not a ≥6 pass/fail gate**; the CQR-monotonicity item **moved from CP-2 to CP-3**; three-stage coverage + the §7.2 benchmark added.
- **§4.1 / §8.1** — "no headline domain feature" is an allowed, reportable outcome; SHAP is explanation-only.
- **§9.2 / CP-4 / CP-5** — sliders drawn from the champion's **retained** features (quantile selector fixed); `expected_scarcity_proxy` a toggle only if genuinely binary; the UI never justifies retaining a weak feature.

## AMD-7 — Champion/benchmark schema-separation invariant (§9.4)

Old "optional fifth" forecast-not-actual guard → **mandatory fifth invariant**: (a) no A69-touched column reaches the champion schema; (b) the §7.2 benchmark differs from the frozen strict-gate catalog *only* by A69 and derivatives. §13 testing defense updated four → **five** property tests.

## AMD-8 — DuckDB SQL mart (§9.6) + offline data/output-health report (§9.5); reading order & §12 gates

- **§9.6** — DuckDB is the SQL block's real database; the **SQL-A** production subset (window/data-quality queries) integrated and tested at M1 as the canonical feature source; SQL-B interview-fluency through G3; the SQL block becomes a **second firewall exception** alongside spectral EDA.
- **§9.5** — offline batch **data/output-health** report (no labels → no performance-drift claim): freshness / schema conformance / selected-feature distribution shift / interval width / quantile sanity, reference window + as-of + pinned thresholds; generated **M4/CP-4**, static-rendered **CP-5**; ≤~8 h; no services / dashboard / scheduled retraining / AWS.
- **§10 reading order** — item 5 gains the §7.2 benchmark; item 3 gate-feasible; item 9 three-stage; item 10 retained-feature sliders; new item 11b (health snapshot); item 12 gains the DuckDB mart.
- **§12** — M1 brief gains the four v6.3 additions (PIT proof, candidate construction, DuckDB SQL-A, schema invariant); CP-1 gains PIT + SQL-A + schema-separation items and the R-2/climatology/dunkelflaute items reframed; M2/CP-2 gain the 2×2 selection + freeze; M3/CP-3 SHAP-explains + benchmark + three-stage + moved monotonicity; M4/CP-4 health report; M5/CP-5 static render + strict-gate limitations.

## Version-numbering consequence

v6.3 is the current edition. The parked **DEC-AWS** (AWS production backbone, `aws-extension-spec_v1_1.md`), if ratified at G5, now amends **v6.3 → v6.4** (was v6.2 → v6.3). The map cascade for DEC-AWS becomes **v5 → v6**.

## After applying — target-specific source distribution

- **Flagship repo `main`:** `capstone_V6_3.md`, this amendment record, `engineering-role.md`, README, the `docs/spike-feed-status.md` clarification.
- **Project Knowledge:** capstone v6.3, syllabus v3.2, map v5, progress.md, role docs, the parked AWS draft.
- **NotebookLM:** **syllabus v3.2 + capstone v6.3 only** — not the map, the AWS draft, or amendment-history files.

Record each swap separately in progress.md; verify the final repo commit/tree.
