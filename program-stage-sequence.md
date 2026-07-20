# Program Stage Sequence — Full Ordered Map (v4)

*Rebuilt 2026-07-15 by the orchestrator on Yarden's explicit request (audit + gap-closure rebuild — the sanctioned path per ORC §"The Program Stage Sequence map"). **Ratified edition** — derived from the current Strategic Anchors: `syllabus_v3_1.md` v3.1, `capstone_V6_2.md` v6.2, and the companion `Binary Classification Mini-Capstone.md` v1.0. Supersedes v3 (2026-07-12). Static by design: no status markers; all position tracking lives in progress.md. On any conflict between this map and the anchors, **the anchors win.***

**v3 → v4 delta (audit release — no scope, sequence, or content change; every v3 row preserved).** All v3 rows carry forward with identical IDs and order. Fixes only:

- **New Executor column.** v3's *Constant briefing inputs* named six row families (L/CLS/UNSUP/CAUS · M/FM/SPEC · ALG · B-Man/C-Man · C-Claude/C-Research · G) and left seven row types outside all of them — SQL, DL, DL+, ERR, C4-3, C4-4, and the DEC/TRIG/APP events. Routing now lives at the row, so no row can fall through the family list.
- **Briefing-sources repairs.** L5 (+ the separate Condition-number row, + the CS229 PCA resource), M1 (+ §0, §1, §9.4, §11 — all four named by §12's own binding list and all four missing from v3), L15 ("adjacent rows" → the actual RF/ARIMA rows), M3 (+ §11 R-1), L31 (+ §6.3, §11 R-1), CP-5 (+ the CPU-Upgrade contingency).
- **Gate repairs.** G3 gains **CP-2 status carried up** (v3 had it on G2/CP-1 and G4/CP-3 but skipped G3, where M2 lands). G5 gains the **Month-5 consolidation verdict** and **CP-4 + CP-5 status carried up**, plus its missing SYL/CAP citations.
- **New row: LI-OTW** — the recruiter-only open-to-work flip, deferred by PRG Track C to the M2 trigger and present in no v3 row.
- **Repo naming.** DL names its own standalone repo (it is a B-Claude build that is neither flagship nor companion — see the *Repos* note below). ALG names its solutions repo.
- **Stale header note removed.** v3 said "progress.md still names the pre-expansion anchors" — false since the 2026-07-12 regeneration.
- **L5 conditional resolved flat.** Yarden confirmed 2026-07-15 that L5 was never issued → the v3.1 PCA upgrade rides **inside L5**. The conditional is retired. *(PRG's Session Log still carries the contradicting line "L5 already issued under old ceiling" — a progress.md correction, not a map one; it lands at the next regeneration.)*

**Verification status.** Rows for Months 0–5 (setup → G5) were audited row-by-row against `syllabus_v3_1.md` and `capstone_V6_2.md` on 2026-07-15. **The FM/FCP/G6 rows were NOT audited against `Binary Classification Mini-Capstone.md`** — that plan is stage-gated (ORC: not read, briefed, or consumed before B-Man3/FM0). They are carried forward **verbatim from v3**, where they were authored at the 2026-07-12 ratification. They are marked ⚠ below and are due one verification pass when the gate opens at B-Man3.

## How to navigate (orchestrator protocol)

1. Read `progress.md` → current position per track + next pending checkpoint.
2. Find the row(s) immediately after the last completed stage on each active track.
3. Read **only** the sources in that row's *Briefing sources* column — nothing else — then write the brief.
4. Brief-format fields come from the constant inputs below; the executor comes from the row's *Executor* column. Neither is re-derived per row.

**Constant briefing inputs (stated once — every row inherits these by executor):**

- **NotebookLM rows:** prompt fields per ORC §"Type L"; teaching style, floor calibration, and the checkpoint consolidation verdict per the NotebookLM role doc; depth label from the cited source row. The L block sets the ceiling only.
- **Claude Code rows:** brief fields per ORC §"Type B-Claude"; workflow per that repo's `CLAUDE.md`; the brief points the engineer at the plan doc for architecture and acceptance criteria, never restates them. **Every such brief names its repo** (column below). FM rows point at the **fraud repo's own** `CLAUDE.md` + FRD once that repo exists (FM0 creates it).
- **Yarden-solo rows** (SQL, ALG, C4-3): self-paced; no brief is written to an executor. The orchestrator schedules them, states the cap and the done-condition, and reads the result at the month gate. **C4-3 is no-AI-inside-the-box by design** (SYL:Supp "C4-3") — that constraint is the block.
- **Yarden-manual rows:** fields per ORC §"Type B-Manual" / §"Type C-Manual".
- **Claude-chat rows:** fields per ORC §"Type C-Claude". **Research-agent rows:** fields per ORC §"Type C-Research" / §"Type B-Research". Positioning theme + CV cadence from PRG Track C.
- **Orchestrator rows** (G, DEC): gate mechanics per ORC §"Verification and checkpoints". Yarden brings the one-line carry-forward status; the orchestrator adjudicates. TRIG/APP are state changes, not blocks — nothing is briefed, the state flips in progress.md.

**Repos (four across the program — the ORC "two repos" line counts only the two that carry a `CLAUDE.md` + a plan doc):**

1. **Flagship** — `hrsi56/delu-day-ahead-forecast` (holds `CLAUDE.md` + `capstone_V6_2.md`). All M/SPEC rows.
2. **CNN mini-project** — standalone, created at DL. **Never the flagship repo** (SYL:Supp "DL" red line: *do not wire into the DE-LU capstone*). No plan doc; the brief carries the scope.
3. **ALG solutions** — public, pattern-organized, created at ALG-1. Yarden-solo, not a Claude Code repo.
4. **Companion fraud** — created at FM0 (holds its own `CLAUDE.md` + the FRD). All FM rows.

**Source notation:** `SYL` = `syllabus_v3_1.md` · `CAP` = `capstone_V6_2.md` · `AWS` = `aws-extension-spec_v1_1.md` · `FRD` = `Binary Classification Mini-Capstone.md` · `PRG` = `progress.md` · `ORC` = `orchestrator-role.md`. `SYL:M2 "spectral"` = that row of the Month-2 table; `FRD:§11 "M0"` = that milestone in the fraud plan. **Notation guard:** the fraud plan's internal milestones are named M0–M5; this map prefixes them FM/FCP to avoid collision with the flagship's M/CP.

Legend: `L` = learning block · `M`/`CP` = flagship milestone/checkpoint · `FM`/`FCP` = fraud milestone/checkpoint · `G` = month/close gate · `B-Man` = manual action · `C*`/`CV`/`LI`/`APP`/`REV` = Track C · `DL`, `SQL`, `C4-x`, `ALG-x`, `CLS-x`, `UNSUP`, `CAUS`, `SPEC` = supplementary/extension blocks · `DEC` = pre-committed decision point · `TRIG` = state change. Depth labels per the syllabus. ⚠ = carried from v3, unverified against the stage-gated FRD.

| Stage | Description | Executor | Briefing sources — read exactly this |
|---|---|---|---|
| **—** | **SETUP (complete)** | | |
| M0 | Capstone plan ratified + data-layer de-risking spike run, adjudicated, merged to `main` (`docs/spike-feed-status.md`); v6.2 amendments merged 2026-07-12 | — | Record only: CAP:§0, §12 "M0"; spike record in-repo |
| **—** | **MONTH 0 — Linear Algebra Foundations (launched 2026-06-09; 5–6 weeks → ~mid-July)** | | |
| L1 | Linear algebra 18.06 — Lectures 1–5 + Strang Ch. 1–2; Gaussian-elimination solver shipped | NotebookLM | SYL:M0 "four fundamental subspaces" row |
| L2 | Linear algebra 18.06 — Lectures 6–10 + Ch. 3 [AUTH]: four fundamental subspaces; deliverable `four_subspaces(A)` | NotebookLM | SYL:M0 "four fundamental subspaces" row · PRG Track A (L2 definition) |
| L3 | Linear algebra 18.06 — Lectures 14–17 [AUTH]: orthogonality → projections → least squares → Gram–Schmidt; OLS normal-equation deliverable (Month-0 deliverable #1) | NotebookLM | SYL:M0 "four fundamental subspaces" row + SYL:M0-deliv #1 · CAP:§7 (Ridge reuses this work) |
| C2 | *(parallel, one-off Track C floor — authorized 2026-06-10)* LinkedIn floor (headline, About, Featured) + README polish on solver + event-app repos; Lab-Engineer framing CLOSED. **Split routing:** README/About copy = C-Claude draft; publishing = C-Manual. **Open-to-work flip is NOT here — deferred to LI-OTW at the M2 trigger** | Claude chat → Yarden | PRG Track C "One-off C2 floor" |
| C8 | *(parallel, Months 0–1)* Target-list research: tiered Beer-Sheva-local + ≤3-day-hybrid TLV/Herzliya DS employer list. **Its take-home-vs-live-screen ratio feeds DEC-ALG at G3** | Research agent | PRG Track C "C8-research" line · SYL:Supp "ALG" (downgrade rule — what DEC-ALG will need) |
| G0-mid | **Month-0 mid-month gate** (~end June): coding deliverable(s) runnable + NotebookLM consolidation verdict | Orchestrator | SYL:M0-deliv |
| L4 | Eigenvalues, eigenvectors, diagonalization — 18.06 L21–22 + Strang Ch. 5–6 [AUTH] (determinants skim [REC]). *Resolves the syllabus's internal span clash: row 1 assigns L18–20 to determinants, row 2 says eigen = L18–22 → eigen runs L21–22, determinants skim L18–20* | NotebookLM | SYL:M0 "Eigenvalues" + "Determinants" rows |
| L5 | SVD, PCA, condition number — 18.065 fragments L6–8 + 3Blue1Brown + **CS229 PCA lecture & 18.065 L6 (the ~2–3h applied upgrade)**; Strang *Linear Algebra and Learning from Data* for condition number. **PCA at [APPLIED-AUTH] (v3.1 LO3 partial reopen — rides inside L5, confirmed 2026-07-15; SVD framing + Eckart–Young stay [REC]); condition number [REC]** — carries the collinearity interview answer (load-forecast × residual-load, a *mechanical* correlation). PCA + condition-number toy notebook (Month-0 deliverable #2). **CHECKPOINT BLOCK — closes Month 0; verdict must confirm the G0-mid AᵀA gap closed** | NotebookLM | SYL:M0 "SVD/PCA" row (upgraded) **+ SYL:M0 "Condition number" row** + Month-0 timing note + SYL:M0-deliv #2 · CAP:§4 · PRG Track A (G0-mid flagged gap) |
| G0 | **Month-0 close gate:** both coding deliverables runnable + consolidation verdict incl. explicit AᵀA-gap-closure statement | Orchestrator | SYL:M0-deliv #1–2 |
| **—** | **MONTH 1 — Probability, Statistics, Applied Change-Point (~mid-Jul → mid-Aug)** | | |
| C7 | Networking floor begins (~1h/week, ongoing) | Yarden | PRG Track C "C7" line |
| L6 | Distributions — Stanford CS109 [AUTH] | NotebookLM | SYL:M1 "Distributions" row |
| L7 | MLE as an optimization principle [AUTH] | NotebookLM | SYL:M1 "MLE" row |
| L8 | Hypothesis testing [AUTH] + C4-2 A/B-testing rider [REC, ~4h] | NotebookLM | SYL:M1 "Hypothesis testing" row + SYL:Supp "C4-2" · CAP:§7.1 |
| L9 | Bootstrap confidence intervals [AUTH] | NotebookLM | SYL:M1 "Bootstrap" row · CAP:§8.3 |
| L10 | Bayes at recognition [REC] | NotebookLM | SYL:M1 "Combinatorics" + "Bayesian vs. frequentist" rows |
| L-MTX | *(parallel filler, ~4h)* 18.065 matrix riders [REC]: L5 PSD/covariance; L8 norms ↔ L1/L2 regularization; L9 four ways to solve least squares (feeds the Month-3 Ridge baseline); L10 condition-number difficulties | NotebookLM | SYL:M1 parallel bullet "18.065 matrix riders" |
| L11 | Pandas time-series practical block [AUTH, ~1 week] | NotebookLM | SYL:M1-parallel "Pandas" bullet · CAP:§4.0 |
| L12 | DE-LU domain reading [REC, spread Months 1–2] | NotebookLM | SYL:M1-parallel "DE-LU domain reading" bullet · CAP:§2 |
| L13 | Bayesian change-point on the DE-LU series [APPLIED-AUTH] (`ruptures`; brackets both regime boundaries) | NotebookLM | SYL:M1 "change-point" row + SYL:M1-deliv #3 · CAP:§2.1, §4 |
| G1 | **Month-1 gate:** hypothesis-testing + bootstrap notebooks + change-point artifact + consolidation verdict | Orchestrator | SYL:M1-deliv #1–3 |
| **—** | **MONTH 1→2 SEAM (~2 weeks: L-OPT precedes DL)** | | |
| L-OPT | **First-principles optimization block [AUTH, ~10h] — runs BEFORE the CNN:** 18.065 L21 (minimizing step-by-step), L22 (gradient descent), L23 (momentum), L25 (SGD); CS229 L2 absorbed as [REC] reinforcement. Framing: GBM = functional gradient descent; feeds both the CNN and the Month-3 LightGBM interview surface | NotebookLM | SYL:"Month 1→2 Seam" section (full table) |
| DL | CNN mini-project (standalone, 16h hard cap): CIFAR-10 in PyTorch, ship-at-threshold ~70%+ (Fashion-MNIST de-scope fallback), NOT wired into the capstone. **Repo: new standalone CNN repo — NOT the flagship repo.** Ship-at-threshold red line is the block's spine | Claude Code | SYL:Supp "DL" (full table + scope red line + routing note) |
| DL+ | **Riders on DL (~5h):** NN structure + backprop [REC] — primary source 18.065 L26–27 (CS229 L11–12 are duplicates, skip); optional enrichment: 18.065 L31–32 Fourier matrix + convolution rule [REC] (bridges the DSP background → CNN → SPEC). **Learning riders, not engineering — issued as their own short L block around the DL build, not folded into the B-Claude brief** | NotebookLM | SYL:"Month 1→2 Seam" section, riders paragraph |
| **—** | **MONTH 2 — Time-Series CV & Tree ML; capstone M1 + spectral EDA land (~+16h parallel; hint mid-Aug → mid-Sep, runs ~5 wks)** | | |
| B-Man1 | DagsHub account creation (before M2 logging) | Yarden | SYL:M2-interleave bullet 1 · CAP:§9.1 |
| L14 | Walk-forward expanding-window CV, 24h embargo, leakage taxonomy [AUTH] (CS229 L8 splits/CV absorbed here as reinforcement) | NotebookLM | SYL:M2 "Walk-forward" row · CAP:§5.1–5.2 |
| L15 | Trees & gradient boosting [AUTH]; **RF/bagging/AdaBoost [REC]** and **ARIMA/SARIMA/ETS [REC]** (the latter carries the 30-second "why not classical methods?" answer — structural reasons only) | NotebookLM | SYL:M2 "Decision tree" + "Gradient boosting" + **"Random forests" + "ARIMA / SARIMA / ETS"** rows · CAP:§6.1 |
| B-Man0 | *(optional, 10 min, pre-M1)* SMARD gas-page browser check | Yarden | CAP:§0 item 3 + §3 SMARD row · PRG Blockers |
| M1 | **Capstone data layer:** ENTSO-E + SMARD bulk pull, UTC/DST/15-min handling incl. chunk-boundary bin integrity, feature catalog v1 (both headline candidates + train-only climatology + regime indicators), KFT/LAG leakage audit, A65/A01 ~25h head gap, R-2 verdict applied. **Repo: flagship.** Verify actual repo/branch state before building | Claude Code | CAP:§12 build-routing note + "M1" + **§0** (ratified decisions, gas reopen closed) + **§1** (D+1 target at the 12:00 CET gate) + §3, §4.0–4.1, §5.1–5.2, **§9.3, §9.4** (invariant tests incl. full-bin clause) + **§11** (R-2 verdict; R-3 fallbacks; R-4) · PRG Notes |
| SPEC | **Spectral EDA of the DE-LU series [APPLIED-AUTH, 6–10h]** (+ ~2h 6.341 U8–U9 theory refresh inside the block): `spectral_eda.py` — detrend → Welch PSD (Hann) with 24h/168h/12h peaks annotated → per-regime periodograms (empirical basis for the 3-regime folds) → ACF cross-check → optional MSTL; README interpretation ¶; showcase figure earmarked for M4 (§10 item 3b); guardrails: no filters/wavelets/frequency-domain forecasting (R-5). **Repo: flagship.** Briefable inside M1 or as a follow-on block — either way closes before CP-1 | Claude Code | CAP:§4.2 (module, figures, acceptance, guardrails) + §11 "R-5" · SYL:M2 "spectral" row (theory-refresh fragments) |
| CP-1 | Capstone checkpoint 1 (expanded at v6.2): full checklist incl. the three §4.2 spectral items — `spectral_eda.py` end-to-end, ≥3 figures committed, 24h/168h peaks annotated, README ¶ links peaks→features and per-regime spectra→folds | Orchestrator | CAP:§12 "CP-1" checklist (incl. the v6.2 items) |
| SQL | Raw-SQL authoring block begins [APPLIED-AUTH]: parallel filler Months 2–3, **20h hard cap**, done when LAG/LEAD window queries write cold. **Self-paced against a real DB — NotebookLM cannot run SQL** (reuse the Supabase instance or local Postgres, toy table `ts, price, load, wind, solar`) | Yarden solo | SYL:Supp "SQL" (full table + setup note + deliverable) |
| ALG-1 | **Interview-algorithms block begins [APPLIED-AUTH]** — Month-2 light start (~2h/wk, ~8h): Arrays & Hashing (12) + Two Pointers (6); 6.006 L4 anchor watched inside the block; Python-idioms sub-block; **solutions repo (public, pattern-organized) + `progress_log.md` created**. **Conflict rule: capstone always wins the week** | Yarden solo | SYL:Supp "ALG" (pattern table rows 1–2, cadence, conflict rule, tracking format) |
| L16 | Month-2 rehearsal deliverable: LightGBM + walk-forward CV + embargo on a single feature set | NotebookLM | SYL:M2 "Coding deliverable (learning-side)" |
| G2 | **Month-2 gate (expanded):** rehearsal deliverable runnable + consolidation verdict + CP-1 status carried up + **ALG: ≥12 problems solved incl. all Arrays/Hashing; idioms sub-block started** | Orchestrator | SYL:M2-deliv · CAP:§12 "CP-1" · SYL:Supp "ALG" done-conditions |
| **—** | **MONTH 3 — Quantile Regression & DM; classification arc; capstone M2 lands; Track C activates (~+28h parallel; hint mid-Sep → mid-Oct, runs ~5–5.5 wks)** | | |
| L17 | Paper-reading meta-skill (half-day) [REC] | NotebookLM | SYL:M3 "Reading scientific papers" row |
| CLS-1 | **Classification theory arc, part 1 [AUTH, ~12h] — supersedes C4-1 (do not run both):** CS229 L3 logistic regression, L4 perceptron + GLMs, L5 GDA + Naive Bayes (generative-vs-discriminative); metrics surface absorbed from old C4-1 (ROC/PR, imbalance, threshold vs stated cost, calibration curve); one notebook deliverable incl. the NB-vs-logistic comparison. Feeds C4-3a directly and, post-envelope, the fraud arc; firewall intact — nothing enters the DE-LU capstone | NotebookLM | SYL:Supp "CLS-1" (full table + deliverable) |
| CLS-2 | **Classification theory arc, part 2 [~8h]:** bias-variance trade-off [AUTH]; SVMs + kernel trick [REC]; ERM/generalization frame [REC], VC recognition-only; deliverables: bias-variance one-pager + kernel one-pager | NotebookLM | SYL:Supp "CLS-2" |
| L18 | Quantile / pinball loss [AUTH] + uncalibrated-quantiles-vs-coverage preview | NotebookLM | SYL:M3 "Quantile loss" + "Uncalibrated quantile" rows · CAP:§6.1, §5.2 |
| L19 | Isotonic regression for quantile crossing [AUTH] | NotebookLM | SYL:M3 "Isotonic" row · CAP:§6.2 |
| L20 | LightGBM deepening [AUTH]: leaf-wise growth, histogram splits, GOSS, EFB | NotebookLM | SYL:M3 "LightGBM mechanics" row |
| L21 | Diebold-Mariano test [AUTH] | NotebookLM | SYL:M3 "Diebold-Mariano" row · CAP:§7.1 |
| ALG-2 | **Algorithms ramp (~5h/wk, ~20h; SQL's completing slot passes to ALG):** Sliding Window (6), Stack (5), Binary Search (6), Heaps/Top-K (5); 6.006 L3 + L8 anchors; re-solve policy live (failed → re-queue +1 week) | Yarden solo | SYL:Supp "ALG" (pattern rows 3–6, cadence, re-solve policy) |
| M2 | **Capstone baselines + model:** similar-day naïve + naïve-168h + Ridge + LightGBM 9-head ensemble on pinned folds, isotonic wired, DM vs. naïve (incl. the pre-committed secondary gate), MLflow → DagsHub, thin CI live. **Repo: flagship** | Claude Code | CAP:§12 "M2" + §6, §7 + §7.1, §5.1, §9.1, §9.4 · SYL:M3-interleave |
| CP-2 | Capstone checkpoint 2: ≥5 public MLflow runs, CI green, DM secondary gate reported | Orchestrator | CAP:§12 "CP-2" checklist |
| TRIG | **Track C phase-trigger fires (post-M2):** continuous activation — applying, recruiter outreach, interview prep, target research. Rules 1/2/4 retire. *State change, not a block* | — (state flip in PRG) | ORC "Track C activation rules" rule 3 · PRG Track C |
| LI-OTW | **Recruiter-only open-to-work flip on LinkedIn** — deferred from the C2 floor to this trigger. One-line manual action; consumes no CV slot | Yarden | PRG Track C "One-off C2 floor" item 1 (deferral clause) |
| CV-1 | CV iteration #1: baselines + LightGBM + DM test + public MLflow UI link (**slot 1 of 3**) | Claude chat | SYL:M5 "Track C interleave" · PRG Track C |
| LI-1 | Optional LinkedIn signal on M2 landing — surface it, Yarden's call, default defer | Claude chat → Yarden | ORC rule 1 |
| C4-3a | Timed take-home rehearsal #1 (late Month 3): **4h hard box, no AI inside the box**, + 30-min debrief naming what was cut (the debrief is the artifact). Classification dataset — consumes CLS-1's output | Yarden solo (no AI) | SYL:Supp "C4-3" + "CLS-1" (feed note) |
| DEC-ALG | **Pre-committed downgrade decision (at G3, from C8 evidence):** if ≥80% of the active funnel is take-home-format → ALG-3 downgrades [APPLIED-AUTH]→[REC] maintenance (1 problem/wk, 2 mocks), freed ~15h → M3–M4 diagnostics + take-home rehearsal | Orchestrator | SYL:Supp "ALG" downgrade rule (verbatim) · C8 output · PRG Track C funnel state |
| G3 | **Month-3 gate (expanded):** SQL block done (LAG/LEAD cold) + consolidation verdict + **CP-2 status carried up** + **ALG: ≥32 problems, patterns through Heaps/Top-K complete; solutions repo public + pattern-organized + DEC-ALG adjudicated** | Orchestrator | SYL:Supp "SQL" done-condition · **CAP:§12 "CP-2"** · SYL:Supp "ALG" done-conditions |
| **—** | **MONTH 4 — Calibration, Conformal, Explainability; capstone M3 lands (~+36h parallel; hint mid-Oct → mid-Nov, runs ~5.5 wks)** | | |
| L22 | CQR end-to-end [AUTH] incl. the negative-Q subtlety; EnbPI/SPCI awareness [REC — skip past] | NotebookLM | SYL:M4 "CQR" + "EnbPI" rows · CAP:§6.2 |
| L23 | SHAP for tree ensembles [AUTH] incl. the correlated-features pitfall | NotebookLM | SYL:M4 "SHAP" row · CAP:§8.1 |
| L24 | Permutation importance [AUTH] | NotebookLM | SYL:M4 "Permutation" row · CAP:§8.2 |
| L25 | Calibration & reliability diagrams + fan-chart plotting [AUTH] | NotebookLM | SYL:M4 "Calibration" + "Fan-chart" rows · CAP:§8.4 |
| L26 | MLflow remote tracking + Model Registry on DagsHub [REC] | NotebookLM | SYL:M4 "MLflow" row · CAP:§9.1 |
| UNSUP | *(parallel, ~7h)* Unsupervised block: k-means [APPLIED-AUTH] (inertia, choosing k, failure modes — appears in take-homes); EM/GMM [REC]; factor analysis recognize-only; clustering notebook on the CLS-1 dataset | NotebookLM | SYL:Supp "UNSUP" |
| CAUS | *(parallel, ~6h)* **LO2 light reopen:** potential-outcomes frame + confounding [REC]; the capstone's no-causal-claim boundary from first principles; A/B experiment-design deepening [APPLIED-AUTH] (power/MDE, randomization units, peeking, CUPED mention) — converts the clinical-research background into a named interview asset | NotebookLM | SYL:Supp "CAUS" |
| M3 | **Capstone diagnostics:** CQR layer on the pinned calibration slice, isotonic last, SHAP + headline-feature selection, permutation importance, regime-stratified error table (n_obs + bootstrap CIs on thin subsets), reliability diagrams. **Repo: flagship** | Claude Code | CAP:§12 "M3" + §6.2, §8.1–8.4, §4.1 + **§11 "R-1"** (name regime-shift failure, don't gloss) · Contingency: CAP:§13 EnbPI reopen (any stratum >10 pp) |
| ERR | **Rider on M3 (~3h):** CS229 L13 error-analysis method [APPLIED-AUTH] applied to the regime-stratified error table — bucket the largest errors, name the dominant failure mode per regime, estimate the fix-ceiling per bucket. **Learning rider on M3's output — an L block after M3 lands, not part of the B-Claude brief** | NotebookLM | SYL:M4 interleave "ERR rider" bullet |
| CP-3 | Capstone checkpoint 3: coverage ±5pp on ≥4/5 folds; SHAP/permutation overlap ≥6; stratified table documented | Orchestrator | CAP:§12 "CP-3" checklist |
| ALG-3 | **Algorithms peak (~5h/wk, ~20h; per DEC-ALG outcome):** Trees + BFS/DFS on grids/graphs (10), Intro 1-D DP (6); 6.006 L9, L10, L15, L16 anchors; **timed-mock protocol: ≥4 × 25-min unseen solves, talking aloud, plain editor, no AI**; block CLOSES by G4 — nothing bleeds into Month 5 | Yarden solo | SYL:Supp "ALG" (pattern rows 7–8, mock protocol, done-conditions) |
| C4-3b | Timed take-home rehearsal #2: **4h hard box, no AI inside the box**, + debrief | Yarden solo (no AI) | SYL:Supp "C4-3" |
| C4-4a | Mock interview #1 (late Month 4): capstone script + classification fundamentals + one cold SQL question | Claude chat (or human peer) | SYL:Supp "C4-4" |
| CV-2 | CV iteration #2: conformal + SHAP + regime errors (**slot 2 of 3**) | Claude chat | SYL:M5 "Track C interleave" · PRG Track C |
| REV | Reviewer recruitment for the stranger test — one technical + one non-technical | Yarden | CAP:§10.1 |
| G4 | **Month-4 gate (expanded):** consolidation verdict + CP-3 status carried up + **ALG: ≥50 problems all patterns, ≥4 timed mocks logged, block closed** | Orchestrator | CAP:§12 "CP-3" · SYL:Supp "ALG" done-conditions · SYL:M4 interleave |
| **—** | **MONTH 5 — Ship, Deploy, Apply; capstone M4 + M5 land (hint slides to ~mid-Dec → mid/late-Jan)** | | |
| B-Man2 | HF account + initial Spaces setup (start of Month 5) | Yarden | SYL:M5-interleave bullet 1 · CAP:§9.2 |
| APP | **Active applications begin** — no later than the start of Month 5 (continuous from here). *State change, not a block* | Yarden | ORC rule 3 · PRG Track C |
| L27 | marimo reactive-notebook patterns [REC] | NotebookLM | SYL:M5 "Marimo" row · CAP:§9.2, §10 |
| L28 | Reproducibility patterns [AUTH] + inference-script patterns [AUTH] | NotebookLM | SYL:M5 "Reproducibility" + "Inference-script" rows · CAP:§9.3 |
| L29 | Docker multi-stage build patterns [APPLIED-REC] | NotebookLM | SYL:M5 "Docker" row · CAP:§9.2 |
| L30 | HF Spaces deployment mechanics [APPLIED-REC] | NotebookLM | SYL:M5 "Hugging Face Spaces" row · CAP:§9.2 |
| M4 | **Capstone local showcase:** marimo end-to-end, champion registered `Production`, slider lookup + per-cell OOD flags (M4 spike validates), **incl. the §10 item-(3b) spectral section — labeled periodogram + one interpretation ¶, static, NO slider**. **Repo: flagship** | Claude Code | CAP:§12 "M4" (incl. the v6.2 scope line) + §9.2, §10 item 3b, §6.1 |
| CP-4 | Capstone checkpoint 4: registry tag live, <10s local cold render, sliders from lookup, OOD flags validated | Orchestrator | CAP:§12 "CP-4" checklist |
| M5 | **Capstone deploy:** container → HF Spaces (Docker SDK, DagsHub token as Secret), registry-first/bundle-fallback load; full §10 reading order exported to **GitHub Pages as the primary portfolio URL**; the Space is linked beneath it as the labeled interactive deep-dive, with the public MLflow UI alongside it. **No keep-alive of any kind.** CV / LinkedIn / README use the Pages URL as the canonical entry point. **Repo: flagship** | Claude Code | CAP:§12 "M5" + §9.2, §9.3, §10 |
| CP-5 | Capstone checkpoint 5: static Pages report loads **< 3 s on a cold cache from an independent connection**, performs zero runtime calls, and is the primary portfolio URL; Space remains warm < 5 s / cold ≤ 30 s with registry-or-bundle load; stranger test starts at Pages and follows the labeled Space link; limitations + reproducibility statements complete; Monday snapshot + static re-export procedure exercised with both surfaces in sync | Orchestrator | CAP:§12 "CP-5" checklist + §10.1 |
| L31 | Interview prep [AUTH]: the capstone script, incl. the three v6.2 spectral Q&As (seasonal features / folds-vs-regimes / where the DSP background helped), the **static-first-touch vs. live-demo rationale**, and the single-zonal-target answer | NotebookLM | SYL:M5 "Interview prep" row (incl. v3.1 additions) · CAP:§13 + **§6.3** (why one zonal target) + **§11 "R-1"** (the project's best interview narrative) |
| C4-4b | Mock interviews #2–3 (~1h each) | Claude chat (or human peer) | SYL:Supp "C4-4" |
| CV-3 | CV iteration #3: deployed showcase with the **GitHub Pages URL as the primary portfolio link**; labeled Space deep-dive + public MLflow UI linked beneath it — **final CV slot (3 of 3)** | Claude chat | SYL:M5 "Track C interleave" · PRG Track C · CAP:§12 "M5" |
| B-Man3 | *(clerical, any time in Month 5)* Kaggle account + API token (`kaggle.json`) + accept `ieee-fraud-detection` competition rules — unblocks FM0. **The companion stage-gate opens here** | Yarden | FRD:§2 (compliance pattern) + Exec Summary (download mechanics) |
| DEC-AWS | **Pre-committed AWS-backbone decision at G5:** adjudicate parked decisions D1–D6 + D8 against the C8 target-list JD cloud-requirement ratio, live funnel/interview signal, and February capacity. A "yes" fires the documented amendment cascade and a stage-map rebuild; until then no AWS arc enters the ratified sequence | Orchestrator | CAP:§1 delta paragraph · AWS:§12 · C8 output · PRG Track C funnel/capacity state |
| G5 | **Month-5 gate / flagship envelope closes:** full artifact live, in-market with full-artifact applications continuing + **Month-5 consolidation verdict** + **CP-4 and CP-5 status carried up + DEC-AWS adjudicated** | Orchestrator | ORC "Goal" · PRG · **CAP:§12 "CP-4" + "CP-5"** · **SYL:M5 interleave** · AWS:§12 |
| **—** | **MONTHS 6–7 — FRAUD MINI-CAPSTONE ⚠ (companion Track B artifact, ~92h at 10–15h/wk; runs INSIDE the active application phase; hint ~mid-Jan → mid-Mar 2027). Rows below carried verbatim from v3 — unverified against the stage-gated FRD; verify in one pass at B-Man3** | | |
| FM0 ⚠ | **Fraud repo + data + EDA** (~15h): repo scaffolded (src layout, ruff/pytest, its own `CLAUDE.md`), Kaggle download script + SHA-256 checksums (raw data .gitignored — never committed), memory-reduced load verified (<1 GB post-downcast), time-based train/val/calib/test splits frozen (0.60/0.15/0.10/0.15 by TransactionDT), leakage audit doc (UID aggregation, random-K-fold trap, target encoding, D-features). **Repo: companion (created here)** | Claude Code | FRD:§2 (data + compliance), §3 (splits), §10 (repo tree), §11 "M0" |
| FCP-1 ⚠ | Fraud checkpoint 1: splits frozen + serialized; leakage audit in `docs/leakage.md`; checksums verified; exact file sizes confirmed from the Kaggle data page | Orchestrator | FRD:§11 "CP-1" checklist |
| FM1 ⚠ | **Baselines** (~12h): trivial (majority + amount-rule, cost-framed) + logistic regression on interpretable features (OOF target encoding); honest out-of-time PR-AUC/ROC-AUC with stratified bootstrap CIs; MLflow runs to DagsHub (`fraud-ieee/...` naming). **Repo: companion** | Claude Code | FRD:§4 (encoding), §5 a–b, §6 (metrics), §8 (tracking), §11 "M1" |
| FCP-2 ⚠ | Fraud checkpoint 2: both baselines logged with out-of-time metrics + CIs | Orchestrator | FRD:§11 "CP-2" checklist |
| FM2 ⚠ | **LightGBM + imbalance** (~18h): natural-distribution primary (defended no-SMOTE position) + `scale_pos_weight` ablation; past-only UID aggregates recomputed per fold; beats baselines with statistical honesty — paired stratified bootstrap CI on ΔPR-AUC excludes zero, DeLong on ΔROC-AUC cross-check. **Repo: companion** | Claude Code | FRD:§4 (anti-leakage checklist), §5 c–d + imbalance position, §6 (comparison tests), §11 "M2" |
| FCP-3 ⚠ | Fraud checkpoint 3: ΔPR-AUC CI excludes zero; ablation logged; ≥8 MLflow runs trajectory on pace | Orchestrator | FRD:§11 "CP-3" checklist + §8 (≥8-run bar) |
| FM3 ⚠ | **Calibration + threshold + cost** (~15h): isotonic on the dedicated calibration slice (Platt comparison); before/after reliability + Brier; expected-cost curve from the FN/FP cost matrix; operating point t* + review-budget alternative; precision/recall/alert-rate at t*. **Repo: companion** | Claude Code | FRD:§1 (cost matrix), §6 (calibration + threshold methodology), §11 "M3" |
| FCP-4 ⚠ | Fraud checkpoint 4: calibrated model + chosen operating point + cost curve committed | Orchestrator | FRD:§11 "CP-4" checklist |
| FM4 ⚠ | **SHAP + slices + demo** (~20h): SHAP beeswarm/dependence + FP post-mortem + TP case study + permutation cross-check; slice analysis (ProductCD/device/amount/time-drift); **Gradio demo on HF Spaces** (threshold slider with live precision/recall/alert-rate, cost calculator, SHAP waterfall; synthetic inputs only — no raw Vesta rows); Docker multi-stage reuse. **Repo: companion** | Claude Code | FRD:§7 (explainability), §6 (slices), §9 (demo spec + Gradio-over-marimo position), §11 "M4" |
| FCP-5 ⚠ | Fraud checkpoint 5: demo live on Spaces; explanation artifacts committed; slice table documented | Orchestrator | FRD:§11 "CP-5" checklist |
| LI-2 ⚠ | Optional LinkedIn signal on FM4 (deployed second artifact) — Yarden's call | Claude chat → Yarden | ORC rule 1 · FRD:§0 (positioning ¶) |
| FM5 ⚠ | **Polish + interview one-pager** (~12h): README narrative arc complete; "walk me through your project" script; the five hardest questions WITH answers (imbalance defense, why PR-AUC, why out-of-time, the leakage story, "is 0.9 a probability?"). **Repo: companion** | Claude Code + Yarden | FRD:§10 (README arc), §11 "M5", §13 (interview-surface map) |
| C-Man-P ⚠ | Portfolio surfaces update (**no CV-iteration slot — the cap of 3 is already consumed**): fraud demo URL + repo pinned on GitHub/LinkedIn Featured; one line added to the existing CV file manually | Yarden | PRG Track C (CV cadence note) · FRD:§0 |
| G6 ⚠ | **Fraud-capstone close gate / program fully closed:** FCP-1–5 all green, FM5 one-pager done, both artifacts live, application funnel running on the two-artifact portfolio | Orchestrator | FRD:§11 (all CP checklists) · ORC "Goal" |

**Standing rhythm (not single rows):** C7 networking ~1h/week from Month 1; weekly Monday refresh of the deployed flagship during the application phase = **snapshot + static re-export + commit**, with the static Pages report and interactive Space kept in sync (CAP:§9.2); Track C application funnel continuous from the M2 phase-trigger onward — from Month 6 the funnel runs on both artifacts; the ALG re-solve queue is a weekly micro-rhythm inside Months 2–4 only (dies at G4).

---

## Appendix — Load & calendar (v3 baseline + v6.2 static-first-touch rider)

Net new hours by month over the v2 baseline (~20–22h/wk budget unchanged):

| Where | Added | What |
|---|---|---|
| Month 0 (closing) | +2–3h | L5 PCA upgrade (rides inside L5 — confirmed 2026-07-15) |
| Month 1 | +4h | L-MTX (parallel filler) |
| Seam | +15h | L-OPT (10) + DL+ riders (5) → seam ≈ 2 weeks |
| Month 2 | +16h | SPEC (8) + ALG-1 (8) |
| Month 3 | +28h | CLS-1 (net ≈ +1 over the absorbed C4-1), CLS-2 (8), ALG-2 (20) |
| Month 4 | +36h | ALG-3 (20) + UNSUP (7) + CAUS (6) + ERR (3) |
| Month 5 | +3–5h | Static first-touch rider: full-report export, GitHub Pages publication, labeled deep-dive links, load/runtime-call gate, and one end-to-end Monday refresh rehearsal; B-Man3 remains clerical |
| Months 6–7 | +92h | Fraud mini-capstone FM0–FM5 |
| **Total** | **≈ +183–185h** | ~500h → ~683–685h (rounded planning envelope remains ~680h) |

Consequences, stated once: Months 2–4 each run ~5–5.5 weeks at the current weekly budget (or the budget rises to ~26–27h/wk to hold 4-week months); the static-first-touch rider is absorbed inside M5's existing window, so **G5 still lands ~mid/late-January 2027**; G6 lands ~March 2027 unless DEC-AWS at G5 ratifies a different post-G5 sequence. **Fixed anchors that do NOT move:** APP begins at the start of program-Month 5 (in-market before the flagship envelope closes), and ALG closes at G4, before APP. The fraud capstone deliberately runs inside the application phase: its theory (CLS-1/2, UNSUP) is complete by end of Month 4, so take-homes arriving from Month 5 onward are covered before the second artifact itself ships.

---

## Appendix — v4 audit trail (what was checked, what was found)

Audited 2026-07-15, row-by-row, Months 0–5, against `syllabus_v3_1.md` v3.1 and `capstone_V6_2.md` v6.2.

**Coverage confirmed complete.** Every syllabus row (Months 0–5 tables, all parallel bullets, the seam table and its riders, all nine supplementary blocks), every coding-deliverable set (M0 #1–2, M1 #1–3, M2 learning-side — the syllabus defines no M3/M4/M5 coding deliverable, so G3/G4/G5 gate on verdict + CP status only), and every capstone milestone, checkpoint, risk, and B-Manual action maps to a row.

**Gaps found and closed in v4:** L5 sources (Condition-number row + CS229 PCA resource) · M1 sources (§0, §1, §9.4, §11) · L15 sources ("adjacent rows" → named rows) · M3 (§11 R-1) · L31 (§6.3, §11 R-1) · CP-5 (CPU-Upgrade contingency) · G3 (CP-2 carry-up) · G5 (Month-5 verdict + CP-4/CP-5 carry-up) · seven row types with no executor (SQL, DL, DL+, ERR, C4-3, C4-4, DEC/TRIG/APP) · DL repo unnamed · LI-OTW row missing entirely · stale anchor-update note · L5 PCA conditional.

**Capstone sections never cited by any row, checked and dispositioned:** §2.2 (reached via §2 at L12) · §5, §8, §9 (section intros; subsections cited) · §6.3 (was uncited — **now on L31**).

**Not audited:** FM0–FM5, FCP-1–5, LI-2, C-Man-P, G6 — the FRD is stage-gated until B-Man3. Rows carried verbatim from v3. One verification pass is owed when the gate opens.

---

*End of Program Stage Sequence — Full Ordered Map (v4).*
