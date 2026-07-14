# Program Stage Sequence — Full Ordered Map (v3)

*Built 2026-07-12 by the orchestrator. **Ratified edition** — derived from the current Strategic Anchors: `syllabus_v3_1.md` v3.1, `capstone_V6_2.md` v6.2, and the companion `Binary Classification Mini-Capstone.md` v1.0 (all in project knowledge as of 2026-07-12). Supersedes v2 (2026-07-05). Static by design: no status markers; all position tracking lives in progress.md. On any conflict between this map and the anchors, **the anchors win.***

**v2 → v3 delta.** Expansion release, adopted under the owner decision to optimize hire probability over the calendar envelope. All v2 rows preserved; added: the L5+ PCA rider (LO3 partial reopen), the L-MTX rider (Month 1), the seam optimization section L-OPT + DL+ riders, the Month-2 spectral-EDA block SPEC and CP-1 expansion, the ALG interview-algorithms track (ALG-1/2/3 + DEC-ALG), the CLS-1/CLS-2 classification arc (CLS-1 supersedes C4-1 — do not run both), UNSUP, CAUS (LO2 light reopen), the ERR rider, three spectral interview Q&As in L31, expanded G2/G3/G4 gates, and the post-envelope fraud mini-capstone arc (B-Man3, FM0–FM5, FCP-1–5, G6, Months 6–7). The gap-analysis report and the two extension specs are **historical** — their content is merged into the anchors, and no brief cites them anymore. Load consequence: ~+180h total (~500h → ~680h); per-month math in the appendix.

**Anchor-update note:** progress.md still names the pre-expansion anchors; its Strategic Anchors update to v3.1 / v6.2 / FRD v1.0 with the regeneration at the next session opening. One live conditional until then: if L5 has not yet been briefed, the PCA upgrade rides inside it (SYL Month-0 timing note); if L5 already closed at [REC], the upgrade becomes a Month-1 rider next to L-MTX.

## How to navigate (orchestrator protocol)

1. Read `progress.md` → current position per track + next pending checkpoint.
2. Find the row(s) immediately after the last completed stage on each active track.
3. Read **only** the sources in that row's *Briefing sources* column — nothing else — then write the brief.
4. Brief-format fields come from the constant inputs below, never re-derived per row.

**Constant briefing inputs (stated once — every row inherits these):**

- **Every L / CLS / UNSUP / CAUS row:** prompt fields per ORC §"Type L"; teaching style/calibration per the NotebookLM role doc; depth label from the cited source row.
- **Every M / FM / SPEC row:** brief fields per ORC §"Type B-Claude"; workflow per repo `CLAUDE.md`; the brief points the engineer at the capstone doc (CAP or FRD) for architecture and acceptance criteria, never restates them. FM rows point at the **fraud repo's own** `CLAUDE.md` + FRD once that repo exists (FM0 creates it).
- **Every ALG row:** self-paced supplementary; the 6.006 anchor lectures are watched inside the block as [REC] refreshers, never as separate L-blocks (SYL:Supp "ALG").
- **Every B-Man / C-Man row:** fields per ORC §"Type B-Manual" / §"Type C-Manual".
- **Every C-Claude / C-Research row:** fields per ORC §"Type C-Claude" / §"Type C-Research"; positioning theme + CV cadence from PRG Track C.
- **Every G row:** gate mechanics per ORC §"Verification and checkpoints".

**Source notation:** `SYL` = `syllabus_v3_1.md` · `CAP` = `capstone_V6_2.md` · `FRD` = `Binary Classification Mini-Capstone.md` · `PRG` = `progress.md` · `ORC` = `orchestrator-role.md`. `SYL:M2 "spectral"` = that row of the Month-2 table; `FRD:§11 "M0"` = that milestone in the fraud plan. **Notation guard:** the fraud plan's internal milestones are named M0–M5; this map prefixes them FM/FCP to avoid collision with the flagship's M/CP.

Legend: `L` = learning block (NotebookLM) · `M`/`CP` = flagship capstone milestone/checkpoint (Claude Code) · `FM`/`FCP` = fraud capstone milestone/checkpoint (Claude Code) · `G` = month/close gate · `B-Man` = manual action · `C*`/`CV`/`LI`/`APP`/`REV` = Track C · `DL`, `SQL`, `C4-x`, `ALG-x`, `CLS-x`, `UNSUP`, `CAUS`, `SPEC` = supplementary/extension blocks · `DEC` = pre-committed decision point. Depth labels per the syllabus.

| Stage | Description | Briefing sources — read exactly this |
|---|---|---|
| **—** | **SETUP (complete)** | |
| M0 | Capstone plan ratified + data-layer de-risking spike run, adjudicated, merged to `main` (`docs/spike-feed-status.md`); v6.2 amendments merged 2026-07-12 | Record only: CAP:§0, §12 "M0"; spike record in-repo |
| **—** | **MONTH 0 — Linear Algebra Foundations (launched 2026-06-09; 5–6 weeks → ~mid-July)** | |
| L1 | Linear algebra 18.06 — Lectures 1–5 + Strang Ch. 1–2; Gaussian-elimination solver shipped | SYL:M0 "four fundamental subspaces" row |
| L2 | Linear algebra 18.06 — Lectures 6–10 + Ch. 3 [AUTH]: four fundamental subspaces; deliverable `four_subspaces(A)` | SYL:M0 "four fundamental subspaces" row · PRG Track A (L2 definition) |
| L3 | Linear algebra 18.06 — Lectures 14–17 [AUTH]: orthogonality → projections → least squares → Gram–Schmidt; OLS normal-equation deliverable (Month-0 deliverable #1) | SYL:M0 "four fundamental subspaces" row + SYL:M0-deliv #1 · CAP:§7 (Ridge reuses this work) |
| C2 | *(parallel, one-off Track C floor — authorized 2026-06-10)* LinkedIn floor (headline, About, Featured) + README polish on solver + event-app repos; Lab-Engineer framing CLOSED | PRG Track C "One-off C2 floor" |
| C8 | *(parallel, Months 0–1)* Target-list research: tiered Beer-Sheva-local + ≤3-day-hybrid TLV/Herzliya DS employer list (C-Research). **Its take-home-vs-live-screen ratio feeds DEC-ALG at G3** | PRG Track C "C8-research" line · SYL:Supp "ALG" (downgrade rule — what DEC-ALG will need) |
| G0-mid | **Month-0 mid-month gate** (~end June): coding deliverable(s) runnable + NotebookLM consolidation verdict | SYL:M0-deliv |
| L4 | Eigenvalues, eigenvectors, diagonalization — 18.06 L21–22 + Strang Ch. 5–6 [AUTH] (determinants skim [REC]) | SYL:M0 "Eigenvalues" + "Determinants" rows |
| L5 | SVD, PCA, condition number — 18.065 fragments L6–8 + 3Blue1Brown; **PCA at [APPLIED-AUTH] (v3.1 LO3 partial reopen; SVD framing + Eckart–Young stay [REC])**; PCA + condition-number toy notebook (Month-0 deliverable #2) — closes Month 0. **Conditional:** if L5 already closed at [REC] before v3.1 adoption, the PCA upgrade runs as a ~2–3h Month-1 rider instead | SYL:M0 "SVD/PCA" row (upgraded) + Month-0 timing note + SYL:M0-deliv #2 · CAP:§4 |
| G0 | **Month-0 close gate:** both coding deliverables runnable + consolidation verdict | SYL:M0-deliv #1–2 |
| **—** | **MONTH 1 — Probability, Statistics, Applied Change-Point (~mid-Jul → mid-Aug)** | |
| C7 | Networking floor begins (~1h/week, ongoing) | PRG Track C "C7" line |
| L6 | Distributions — Stanford CS109 [AUTH] | SYL:M1 "Distributions" row |
| L7 | MLE as an optimization principle [AUTH] | SYL:M1 "MLE" row |
| L8 | Hypothesis testing [AUTH] + C4-2 A/B-testing rider [REC, ~4h] | SYL:M1 "Hypothesis testing" row + SYL:Supp "C4-2" · CAP:§7.1 |
| L9 | Bootstrap confidence intervals [AUTH] | SYL:M1 "Bootstrap" row · CAP:§8.3 |
| L10 | Bayes at recognition [REC] | SYL:M1 "Combinatorics" + "Bayesian vs. frequentist" rows |
| L-MTX | *(parallel filler, ~4h)* 18.065 matrix riders [REC]: L5 PSD/covariance; L8 norms ↔ L1/L2 regularization; L9 four ways to solve least squares (feeds the Month-3 Ridge baseline); L10 condition-number difficulties | SYL:M1 parallel bullet "18.065 matrix riders" |
| L11 | Pandas time-series practical block [AUTH, ~1 week] | SYL:M1-parallel "Pandas" bullet · CAP:§4.0 |
| L12 | DE-LU domain reading [REC, spread Months 1–2] | SYL:M1-parallel "DE-LU domain reading" bullet · CAP:§2 |
| L13 | Bayesian change-point on the DE-LU series [APPLIED-AUTH] (`ruptures`; brackets both regime boundaries) | SYL:M1 "change-point" row + SYL:M1-deliv #3 · CAP:§2.1, §4 |
| G1 | **Month-1 gate:** hypothesis-testing + bootstrap notebooks + change-point artifact + consolidation verdict | SYL:M1-deliv #1–3 |
| **—** | **MONTH 1→2 SEAM (~2 weeks: L-OPT precedes DL)** | |
| L-OPT | **First-principles optimization block [AUTH, ~10h] — runs BEFORE the CNN:** 18.065 L21 (minimizing step-by-step), L22 (gradient descent), L23 (momentum), L25 (SGD); CS229 L2 absorbed as [REC] reinforcement. Framing: GBM = functional gradient descent; feeds both the CNN and the Month-3 LightGBM interview surface | SYL:"Month 1→2 Seam" section (full table) |
| DL | CNN mini-project (B-Claude, standalone, 16h hard cap): CIFAR-10 in PyTorch, ship-at-threshold ~70%+, NOT wired into the capstone | SYL:Supp "DL" |
| DL+ | **Riders on DL (~5h):** NN structure + backprop [REC] — primary source 18.065 L26–27 (CS229 L11–12 are duplicates, skip); optional enrichment: 18.065 L31–32 Fourier matrix + convolution rule [REC] (bridges the DSP background → CNN → SPEC) | SYL:"Month 1→2 Seam" section, riders paragraph |
| **—** | **MONTH 2 — Time-Series CV & Tree ML; capstone M1 + spectral EDA land (~+16h parallel; hint mid-Aug → mid-Sep, runs ~5 wks)** | |
| B-Man1 | DagsHub account creation (B-Manual; before M2 logging) | SYL:M2-interleave bullet 1 · CAP:§9.1 |
| L14 | Walk-forward expanding-window CV, 24h embargo, leakage taxonomy [AUTH] (CS229 L8 splits/CV absorbed here as reinforcement) | SYL:M2 "Walk-forward" row · CAP:§5.1–5.2 |
| L15 | Trees & gradient boosting [AUTH]; RF/bagging, ARIMA at [REC] (CS229 L10 is this row's cited source) | SYL:M2 "Decision tree" + "Gradient boosting" + adjacent rows · CAP:§6.1 |
| B-Man0 | *(optional, 10 min, pre-M1)* SMARD gas-page browser check | CAP:§0 item 3 + §3 SMARD row · PRG Blockers |
| M1 | **Capstone data layer** (B-Claude): ENTSO-E + SMARD bulk pull, UTC/DST/15-min handling, feature catalog v1, KFT/LAG leakage audit | CAP:§12 build-routing note + "M1" + §3, §4.0–4.1, §5.1–5.2, §9.3 · PRG Notes |
| SPEC | **Spectral EDA of the DE-LU series [APPLIED-AUTH, 6–10h]** (B-Claude + ~2h 6.341 U8–U9 theory refresh inside the block): `spectral_eda.py` — detrend → Welch PSD (Hann) with 24h/168h/12h peaks annotated → per-regime periodograms (empirical basis for the 3-regime folds) → ACF cross-check → optional MSTL; README interpretation ¶; showcase figure earmarked for M4 (§10 item 3b); guardrails: no filters/wavelets/frequency-domain forecasting (R-5) | CAP:§4.2 (module, figures, acceptance, guardrails) + §11 "R-5" · SYL:M2 "spectral" row (theory-refresh fragments) |
| CP-1 | Capstone checkpoint 1 (expanded at v6.2): full checklist incl. the three §4.2 spectral items — `spectral_eda.py` end-to-end, ≥3 figures committed, 24h/168h peaks annotated, README ¶ links peaks→features and per-regime spectra→folds | CAP:§12 "CP-1" checklist (incl. the v6.2 items) |
| SQL | Raw-SQL authoring block begins [APPLIED-AUTH]: parallel filler Months 2–3, 20h hard cap | SYL:Supp "SQL" |
| ALG-1 | **Interview-algorithms block begins [APPLIED-AUTH]** — Month-2 light start (~2h/wk, ~8h): Arrays & Hashing (12) + Two Pointers (6); 6.006 L4 anchor inside the block; Python-idioms sub-block; solutions repo + `progress_log.md` created. **Conflict rule: capstone always wins the week** | SYL:Supp "ALG" (pattern table rows 1–2, cadence, conflict rule, tracking format) |
| L16 | Month-2 rehearsal deliverable: LightGBM + walk-forward CV + embargo on a single feature set | SYL:M2 "Coding deliverable (learning-side)" |
| G2 | **Month-2 gate (expanded):** rehearsal deliverable runnable + consolidation verdict + CP-1 status carried up + **ALG: ≥12 problems solved incl. all Arrays/Hashing; idioms sub-block started** | SYL:M2-deliv · CAP:§12 "CP-1" · SYL:Supp "ALG" done-conditions |
| **—** | **MONTH 3 — Quantile Regression & DM; classification arc; capstone M2 lands; Track C activates (~+28h parallel; hint mid-Sep → mid-Oct, runs ~5–5.5 wks)** | |
| L17 | Paper-reading meta-skill (half-day) [REC] | SYL:M3 "Reading scientific papers" row |
| CLS-1 | **Classification theory arc, part 1 [AUTH, ~12h] — supersedes C4-1 (do not run both):** CS229 L3 logistic regression, L4 perceptron + GLMs, L5 GDA + Naive Bayes (generative-vs-discriminative); metrics surface absorbed from old C4-1 (ROC/PR, imbalance, threshold vs stated cost, calibration curve); one notebook deliverable incl. the NB-vs-logistic comparison. Feeds C4-3a directly and, post-envelope, the fraud arc; firewall intact — nothing enters the DE-LU capstone | SYL:Supp "CLS-1" (full table + deliverable) |
| CLS-2 | **Classification theory arc, part 2 [~8h]:** bias-variance trade-off [AUTH]; SVMs + kernel trick [REC]; ERM/generalization frame [REC], VC recognition-only; deliverables: bias-variance one-pager + kernel one-pager | SYL:Supp "CLS-2" |
| L18 | Quantile / pinball loss [AUTH] + uncalibrated-quantiles-vs-coverage preview | SYL:M3 "Quantile loss" + "Uncalibrated quantile" rows · CAP:§6.1, §5.2 |
| L19 | Isotonic regression for quantile crossing [AUTH] | SYL:M3 "Isotonic" row · CAP:§6.2 |
| L20 | LightGBM deepening [AUTH]: leaf-wise growth, histogram splits, GOSS, EFB | SYL:M3 "LightGBM mechanics" row |
| L21 | Diebold-Mariano test [AUTH] | SYL:M3 "Diebold-Mariano" row · CAP:§7.1 |
| ALG-2 | **Algorithms ramp (~5h/wk, ~20h; SQL's completing slot passes to ALG):** Sliding Window (6), Stack (5), Binary Search (6), Heaps/Top-K (5); 6.006 L3 + L8 anchors; re-solve policy live (failed → re-queue +1 week) | SYL:Supp "ALG" (pattern rows 3–6, cadence, re-solve policy) |
| M2 | **Capstone baselines + model** (B-Claude): naïve + Ridge + LightGBM 9-head ensemble on pinned folds, isotonic wired, DM vs. naïve, MLflow → DagsHub, thin CI live | CAP:§12 "M2" + §6, §7 + §7.1, §5.1, §9.1, §9.4 · SYL:M3-interleave |
| CP-2 | Capstone checkpoint 2: ≥5 public MLflow runs, CI green, DM secondary gate reported | CAP:§12 "CP-2" checklist |
| TRIG | **Track C phase-trigger fires (post-M2):** continuous activation | ORC "Track C activation rules" rule 3 · PRG Track C |
| CV-1 | CV iteration #1 (C-Claude) | SYL:M5 "Track C interleave" · PRG Track C |
| LI-1 | Optional LinkedIn signal on M2 landing | ORC rule 1 |
| C4-3a | Timed take-home rehearsal #1 (late Month 3): 4h box + debrief, on a classification dataset — consumes CLS-1's output | SYL:Supp "C4-3" + "CLS-1" (feed note) |
| DEC-ALG | **Pre-committed downgrade decision (at G3, from C8 evidence):** if ≥80% of the active funnel is take-home-format → ALG-3 downgrades [APPLIED-AUTH]→[REC] maintenance (1 problem/wk, 2 mocks), freed ~15h → M3–M4 diagnostics + take-home rehearsal | SYL:Supp "ALG" downgrade rule (verbatim) · C8 output · PRG Track C funnel state |
| G3 | **Month-3 gate (expanded):** SQL block done (LAG/LEAD cold) + consolidation verdict + **ALG: ≥32 problems, patterns through Heaps/Top-K complete; solutions repo public + pattern-organized + DEC-ALG adjudicated** | SYL:Supp "SQL" done-condition · SYL:Supp "ALG" done-conditions |
| **—** | **MONTH 4 — Calibration, Conformal, Explainability; capstone M3 lands (~+36h parallel; hint mid-Oct → mid-Nov, runs ~5.5 wks)** | |
| L22 | CQR end-to-end [AUTH]; EnbPI/SPCI awareness [REC] | SYL:M4 "CQR" + "EnbPI" rows · CAP:§6.2 |
| L23 | SHAP for tree ensembles [AUTH] | SYL:M4 "SHAP" row · CAP:§8.1 |
| L24 | Permutation importance [AUTH] | SYL:M4 "Permutation" row · CAP:§8.2 |
| L25 | Calibration & reliability diagrams + fan-chart plotting [AUTH] | SYL:M4 "Calibration" + "Fan-chart" rows · CAP:§8.4 |
| L26 | MLflow remote tracking + Model Registry on DagsHub [REC] | SYL:M4 "MLflow" row · CAP:§9.1 |
| UNSUP | *(parallel, ~7h)* Unsupervised block: k-means [APPLIED-AUTH] (inertia, choosing k, failure modes — appears in take-homes); EM/GMM [REC]; factor analysis recognize-only; clustering notebook on the CLS-1 dataset | SYL:Supp "UNSUP" |
| CAUS | *(parallel, ~6h)* **LO2 light reopen:** potential-outcomes frame + confounding [REC]; the capstone's no-causal-claim boundary from first principles; A/B experiment-design deepening [APPLIED-AUTH] (power/MDE, randomization units, peeking, CUPED mention) — converts the clinical-research background into a named interview asset | SYL:Supp "CAUS" |
| M3 | **Capstone diagnostics** (B-Claude): CQR layer, SHAP + headline-feature selection, permutation importance, regime-stratified error table, reliability diagrams | CAP:§12 "M3" + §6.2, §8.1–8.4, §4.1 · Contingency: CAP:§13 EnbPI reopen |
| ERR | **Rider on M3 (~3h):** CS229 L13 error-analysis method [APPLIED-AUTH] applied to the regime-stratified error table — bucket the largest errors, name the dominant failure mode per regime, estimate the fix-ceiling per bucket | SYL:M4 interleave "ERR rider" bullet |
| CP-3 | Capstone checkpoint 3: coverage ±5pp on ≥4/5 folds; SHAP/permutation overlap; stratified table documented | CAP:§12 "CP-3" checklist |
| ALG-3 | **Algorithms peak (~5h/wk, ~20h; per DEC-ALG outcome):** Trees + BFS/DFS on grids/graphs (10), Intro 1-D DP (6); 6.006 L9, L10, L15, L16 anchors; **timed-mock protocol: ≥4 × 25-min unseen solves, talking aloud, plain editor, no AI**; block CLOSES by G4 — nothing bleeds into Month 5 | SYL:Supp "ALG" (pattern rows 7–8, mock protocol, done-conditions) |
| C4-3b | Timed take-home rehearsal #2 (4h box + debrief) | SYL:Supp "C4-3" |
| C4-4a | Mock interview #1 (late Month 4) | SYL:Supp "C4-4" |
| CV-2 | CV iteration #2 (C-Claude): conformal + SHAP + regime errors | SYL:M5 "Track C interleave" · PRG Track C |
| REV | Reviewer recruitment for the stranger test (C-Manual) | CAP:§10.1 |
| G4 | **Month-4 gate (expanded):** consolidation verdict + CP-3 status carried up + **ALG: ≥50 problems all patterns, ≥4 timed mocks logged, block closed** | CAP:§12 "CP-3" · SYL:Supp "ALG" done-conditions |
| **—** | **MONTH 5 — Ship, Deploy, Apply; capstone M4 + M5 land (hint slides to ~mid-Dec → mid/late-Jan)** | |
| B-Man2 | HF account + initial Spaces setup (B-Manual, start of Month 5) | SYL:M5-interleave bullet 1 · CAP:§9.2 |
| APP | **Active applications begin** — no later than the start of Month 5 (continuous from here) | ORC rule 3 · PRG Track C |
| L27 | marimo reactive-notebook patterns [REC] | SYL:M5 "Marimo" row · CAP:§9.2, §10 |
| L28 | Reproducibility patterns [AUTH] | SYL:M5 "Reproducibility" + "Inference-script" rows · CAP:§9.3 |
| L29 | Docker multi-stage build patterns [APPLIED-REC] | SYL:M5 "Docker" row · CAP:§9.2 |
| L30 | HF Spaces deployment mechanics [APPLIED-REC] | SYL:M5 "Hugging Face Spaces" row · CAP:§9.2 |
| M4 | **Capstone local showcase** (B-Claude): marimo end-to-end, champion registered, slider lookup + OOD flags, **incl. the §10 item-(3b) spectral section — labeled periodogram + one interpretation ¶, static, NO slider** | CAP:§12 "M4" (incl. the v6.2 scope line) + §9.2, §10 item 3b, §6.1 |
| CP-4 | Capstone checkpoint 4: registry tag live, <10s local cold render, sliders from lookup, OOD flags validated | CAP:§12 "CP-4" checklist |
| M5 | **Capstone deploy** (B-Claude): container → HF Spaces, keep-alive cron, CV + LinkedIn updated with URLs | CAP:§12 "M5" + §9.2, §9.3, §10 |
| CP-5 | Capstone checkpoint 5: <30s cold start, registry-or-bundle load, stranger test passes on the deployed URL | CAP:§12 "CP-5" checklist + §10.1 |
| L31 | Interview prep [AUTH]: the capstone script, incl. the three v6.2 spectral Q&As (seasonal features / folds-vs-regimes / where the DSP background helped) | SYL:M5 "Interview prep" row (incl. v3.1 additions) · CAP:§13 |
| C4-4b | Mock interviews #2–3 (~1h each) | SYL:Supp "C4-4" |
| CV-3 | CV iteration #3 (C-Claude): deployed showcase + Spaces URL — final CV-slot iteration | SYL:M5 "Track C interleave" · PRG Track C |
| B-Man3 | *(clerical, any time in Month 5)* Kaggle account + API token (`kaggle.json`) + accept `ieee-fraud-detection` competition rules — unblocks FM0 | FRD:§2 (compliance pattern) + Exec Summary (download mechanics) |
| G5 | **Month-5 gate / flagship envelope closes:** full artifact live, in-market with full-artifact applications continuing | ORC "Goal" · PRG |
| **—** | **MONTHS 6–7 — FRAUD MINI-CAPSTONE (companion Track B artifact, ~92h at 10–15h/wk; runs INSIDE the active application phase; hint ~mid-Jan → mid-Mar 2027)** | |
| FM0 | **Fraud repo + data + EDA** (B-Claude, ~15h): repo scaffolded (src layout, ruff/pytest, its own `CLAUDE.md`), Kaggle download script + SHA-256 checksums (raw data .gitignored — never committed), memory-reduced load verified (<1 GB post-downcast), time-based train/val/calib/test splits frozen (0.60/0.15/0.10/0.15 by TransactionDT), leakage audit doc (UID aggregation, random-K-fold trap, target encoding, D-features) | FRD:§2 (data + compliance), §3 (splits), §10 (repo tree), §11 "M0" |
| FCP-1 | Fraud checkpoint 1: splits frozen + serialized; leakage audit in `docs/leakage.md`; checksums verified; exact file sizes confirmed from the Kaggle data page | FRD:§11 "CP-1" checklist |
| FM1 | **Baselines** (B-Claude, ~12h): trivial (majority + amount-rule, cost-framed) + logistic regression on interpretable features (OOF target encoding); honest out-of-time PR-AUC/ROC-AUC with stratified bootstrap CIs; MLflow runs to DagsHub (`fraud-ieee/...` naming) | FRD:§4 (encoding), §5 a–b, §6 (metrics), §8 (tracking), §11 "M1" |
| FCP-2 | Fraud checkpoint 2: both baselines logged with out-of-time metrics + CIs | FRD:§11 "CP-2" checklist |
| FM2 | **LightGBM + imbalance** (B-Claude, ~18h): natural-distribution primary (defended no-SMOTE position) + `scale_pos_weight` ablation; past-only UID aggregates recomputed per fold; beats baselines with statistical honesty — paired stratified bootstrap CI on ΔPR-AUC excludes zero, DeLong on ΔROC-AUC cross-check | FRD:§4 (anti-leakage checklist), §5 c–d + imbalance position, §6 (comparison tests), §11 "M2" |
| FCP-3 | Fraud checkpoint 3: ΔPR-AUC CI excludes zero; ablation logged; ≥8 MLflow runs trajectory on pace | FRD:§11 "CP-3" checklist + §8 (≥8-run bar) |
| FM3 | **Calibration + threshold + cost** (B-Claude, ~15h): isotonic on the dedicated calibration slice (Platt comparison); before/after reliability + Brier; expected-cost curve from the FN/FP cost matrix; operating point t* + review-budget alternative; precision/recall/alert-rate at t* | FRD:§1 (cost matrix), §6 (calibration + threshold methodology), §11 "M3" |
| FCP-4 | Fraud checkpoint 4: calibrated model + chosen operating point + cost curve committed | FRD:§11 "CP-4" checklist |
| FM4 | **SHAP + slices + demo** (B-Claude, ~20h): SHAP beeswarm/dependence + FP post-mortem + TP case study + permutation cross-check; slice analysis (ProductCD/device/amount/time-drift); **Gradio demo on HF Spaces** (threshold slider with live precision/recall/alert-rate, cost calculator, SHAP waterfall; synthetic inputs only — no raw Vesta rows); Docker multi-stage reuse | FRD:§7 (explainability), §6 (slices), §9 (demo spec + Gradio-over-marimo position), §11 "M4" |
| FCP-5 | Fraud checkpoint 5: demo live on Spaces; explanation artifacts committed; slice table documented | FRD:§11 "CP-5" checklist |
| LI-2 | Optional LinkedIn signal on FM4 (deployed second artifact) — Yarden's call | ORC rule 1 · FRD:§0 (positioning ¶) |
| FM5 | **Polish + interview one-pager** (B-Claude + Yarden, ~12h): README narrative arc complete; "walk me through your project" script; the five hardest questions WITH answers (imbalance defense, why PR-AUC, why out-of-time, the leakage story, "is 0.9 a probability?") | FRD:§10 (README arc), §11 "M5", §13 (interview-surface map) |
| C-Man-P | Portfolio surfaces update (C-Manual, no CV-iteration slot — cadence cap of 3 already consumed): fraud demo URL + repo pinned on GitHub/LinkedIn Featured; one line added to the existing CV file manually | PRG Track C (CV cadence note) · FRD:§0 |
| G6 | **Fraud-capstone close gate / program fully closed:** FCP-1–5 all green, FM5 one-pager done, both artifacts live, application funnel running on the two-artifact portfolio | FRD:§11 (all CP checklists) · ORC "Goal" |

**Standing rhythm (not single rows):** C7 networking ~1h/week from Month 1; weekly Monday snapshot refresh of the deployed flagship demo during the application phase (CAP:§9.2); Track C application funnel continuous from the M2 phase-trigger onward — from Month 6 the funnel runs on both artifacts; the ALG re-solve queue is a weekly micro-rhythm inside Months 2–4 only (dies at G4).

---

## Appendix — Load & calendar (v3)

Net new hours by month over the v2 baseline (~20–22h/wk budget unchanged):

| Where | Added | What |
|---|---|---|
| Month 0 (closing) | +2–3h | L5 PCA upgrade (rides L5 if not yet briefed; else a Month-1 rider) |
| Month 1 | +4h | L-MTX (parallel filler) |
| Seam | +15h | L-OPT (10) + DL+ riders (5) → seam ≈ 2 weeks |
| Month 2 | +16h | SPEC (8) + ALG-1 (8) |
| Month 3 | +28h | CLS-1 (net ≈ +1 over the absorbed C4-1), CLS-2 (8), ALG-2 (20) |
| Month 4 | +36h | ALG-3 (20) + UNSUP (7) + CAUS (6) + ERR (3) |
| Month 5 | ~0 | B-Man3 clerical only |
| Months 6–7 | +92h | Fraud mini-capstone FM0–FM5 |
| **Total** | **≈ +180h** | ~500h → ~680h |

Consequences, stated once: Months 2–4 each run ~5–5.5 weeks at the current weekly budget (or the budget rises to ~26–27h/wk to hold 4-week months); **G5 lands ~mid/late-January 2027**; G6 lands ~March 2027. **Fixed anchors that do NOT move:** APP begins at the start of program-Month 5 (in-market before the flagship envelope closes), and ALG closes at G4, before APP. The fraud capstone deliberately runs inside the application phase: its theory (CLS-1/2, UNSUP) is complete by end of Month 4, so take-homes arriving from Month 5 onward are covered before the second artifact itself ships.
