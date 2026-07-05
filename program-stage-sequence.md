# Program Stage Sequence — Full Ordered Map (v2, navigation edition)

*Regenerated 2026-07-05 by the orchestrator on explicit rebuild request. Scheduling + navigation aid for the ~6.5-month program.*

**Authority note.** This map is derived from the ratified anchors — `syllabus_v3_0.md` v3.0 and `capstone_V6_1.md` v6.1 — and from `progress.md`. Where this table and the anchors ever disagree, **the anchors win**. Stage IDs **L1–L3 match progress.md**; IDs from **L4 onward are provisional planning labels** — the actual block decomposition is fixed at session briefing (blocks may merge or split). Live status always lives in `progress.md`, not here. Calendar hints on the divider rows assume Month 0 launched 2026-06-09 and runs 5–6 weeks; they shift with reality.

**v1 → v2 delta (2026-07-05 audit).** Full row-by-row audit against both anchors found the v1 sequence complete except three missing scheduled items, now added: **C2** (one-off Track C floor, authorized 2026-06-10), **C8** (target-list research, Months 0–1), **B-Man0** (optional pre-M1 SMARD gas-page check, capstone §0 item 3 narrow residual). Added the **Briefing sources** column (navigation). One note, not a row: L1–L3 span OCW lectures 1–10 + 14–17; the syllabus's nominal "Lectures 1–17" span leaves L11–13 (matrix spaces / graphs / review) uncovered — consistent with the ratified L3 definition in progress.md; verify the live OCW index at briefing per C5-min.

## How to navigate (orchestrator protocol)

1. Read `progress.md` → current position per track + next pending checkpoint.
2. Find the row(s) immediately after the last completed stage on each active track.
3. Read **only** the sources in that row's *Briefing sources* column — nothing else — then write the brief.
4. Brief-format fields come from the constant inputs below, never re-derived per row.

**Constant briefing inputs (stated once — every row inherits these; the column never repeats them):**

- **Every L row:** prompt fields per ORC §"Type L"; teaching style/calibration per the NotebookLM role doc (never restate); depth label from the SYL row cited.
- **Every M row:** brief fields per ORC §"Type B-Claude"; workflow per repo `CLAUDE.md`; the brief **points the engineer at CAP** for architecture and acceptance criteria, never restates them (CAP §12 build-routing note).
- **Every B-Man / C-Man row:** fields per ORC §"Type B-Manual" / §"Type C-Manual".
- **Every C-Claude / C-Research row:** fields per ORC §"Type C-Claude" / §"Type C-Research"; positioning theme + CV cadence from PRG Track C.
- **Every G row:** gate mechanics per ORC §"Verification and checkpoints" (deliverables runnable + NotebookLM consolidation verdict; flag the month-closing L prompt as a checkpoint block).

**Source notation:** `SYL` = `syllabus_v3_0.md` · `CAP` = `capstone_V6_1.md` · `PRG` = `progress.md` · `ORC` = `orchestrator-role.md`. `SYL:M3 "DM"` = the Month-3 table row whose topic contains "DM"; `SYL:Supp-SQL` = the named Supplementary block; `CAP:§7.1` = capstone section. `SYL:Mn-interleave` / `-deliv` / `-parallel` = that month's capstone-interleave / coding-deliverables / parallel-blocks list.

Legend: `L` = learning block (NotebookLM) · `M` / `CP` = capstone milestone / checkpoint (Claude Code) · `G` = Track A month gate · `B-Man` = manual action · `C*` / `CV` / `LI` / `APP` / `REV` = Track C items · `DL`, `SQL`, `C4-x` = supplementary interview-readiness blocks. Depth labels per the syllabus: [AUTH] / [REC] / [APPLIED-AUTH] / [APPLIED-REC].

| Stage | Description | Briefing sources — read exactly this |
|---|---|---|
| **—** | **SETUP (complete)** | |
| M0 | Capstone plan ratified (v6.1) + data-layer de-risking spike run, adjudicated, merged to `main` (`docs/spike-feed-status.md`) | Record only: CAP:§0, §12 "M0"; spike record in-repo |
| **—** | **MONTH 0 — Linear Algebra Foundations (launched 2026-06-09; 5–6 weeks → ~mid-July)** | |
| L1 | Linear algebra 18.06 — Lectures 1–5 + Strang Ch. 1–2; Gaussian-elimination solver shipped | SYL:M0 "four fundamental subspaces" row |
| L2 | Linear algebra 18.06 — Lectures 6–10 + Ch. 3 [AUTH]: four fundamental subspaces; deliverable `four_subspaces(A)` | SYL:M0 "four fundamental subspaces" row · PRG Track A (L2 definition) |
| L3 | Linear algebra 18.06 — Lectures 14–17 [AUTH]: orthogonality → projections → least squares → Gram–Schmidt; OLS normal-equation deliverable (Month-0 deliverable #1) | SYL:M0 "four fundamental subspaces" row (least squares = OCW L16, G–S = L17 — verify live index, C5-min) + SYL:M0-deliv #1 · CAP:§7 (Ridge reuses this work) |
| C2 | *(parallel, one-off Track C floor — authorized 2026-06-10)* LinkedIn floor (headline, About, Featured) + README polish on solver + event-app repos (C-Claude draft → C-Manual publish); Lab-Engineer framing CLOSED — never re-add "(transitional role)" | PRG Track C "One-off C2 floor" (the three numbered items + their statuses) |
| C8 | *(parallel, Months 0–1)* Target-list research: tiered Beer-Sheva-local + ≤3-day-hybrid TLV/Herzliya DS employer list (C-Research) | PRG Track C "C8-research" line + "Geography RATIFIED" line |
| G0-mid | **Month-0 mid-month gate** (~end June): coding deliverable(s) to date runnable + NotebookLM consolidation verdict — one-line status at next session opening | SYL:M0-deliv (which artifacts exist by now) |
| L4 | Eigenvalues, eigenvectors, diagonalization — 18.06 L21–22 + Strang Ch. 5–6 [AUTH] (determinants L18–20 skim only [REC]) | SYL:M0 "Eigenvalues" row + "Determinants" row |
| L5 | SVD, PCA, condition number [REC] — 18.065 fragments L6–8 + 3Blue1Brown; PCA + condition-number toy notebook on synthetic load/wind/solar/residual-load (Month-0 deliverable #2) — closes Month 0 | SYL:M0 "SVD" + "Condition number" rows (incl. the load-fc×residual-load interview answer) + SYL:M0-deliv #2 · CAP:§4 (the real feature matrix this rehearses) |
| G0 | **Month-0 close gate:** both coding deliverables runnable + consolidation verdict | SYL:M0-deliv #1–2 |
| **—** | **MONTH 1 — Probability, Statistics, Applied Change-Point (~mid-Jul → mid-Aug)** | |
| C7 | Networking floor begins (~1h/week, ongoing): former students, BGU alumni, one Tech7 / Gav-Yam Negev meetup per month (C-Manual) | PRG Track C "C7 networking floor" line |
| L6 | Distributions — Stanford CS109 [AUTH]: Normal, Bernoulli, Poisson, Student-t, empirical | SYL:M1 "Distributions" row |
| L7 | MLE as an optimization principle [AUTH]: likelihood vs. probability, consistency intuition | SYL:M1 "MLE" row |
| L8 | Hypothesis testing [AUTH]: p-values, one- vs. two-sided, multiple testing — + C4-2 A/B-testing rider [REC, ~4h]: power, sample size, peeking | SYL:M1 "Hypothesis testing" row + SYL:Supp "C4-2" · CAP:§7.1 (where p-values land) |
| L9 | Bootstrap confidence intervals on metric estimates [AUTH] | SYL:M1 "Bootstrap" row · CAP:§8.3 (CIs on thin strata) |
| L10 | Bayes at recognition [REC]: combinatorics, conjugate priors, Bayesian-vs-frequentist frame | SYL:M1 "Combinatorics" + "Bayesian vs. frequentist" rows |
| L11 | Pandas time-series practical block [AUTH, ~1 week]: tz `Europe/Berlin`→UTC, resampling incl. quarter-hour→hour, timestamp joins, lag/rolling features, parquet I/O | SYL:M1-parallel "Pandas" bullet · CAP:§4.0 (the discipline this rehearses) |
| L12 | DE-LU domain reading [REC, ~3 days spread across Months 1–2]: Lago 2021 §2–3; Trebbien et al. 2023; Hilger et al. 2024 (skim) | SYL:M1-parallel "DE-LU domain reading" bullet · CAP:§2 (the regime narrative the papers ground) |
| L13 | Bayesian change-point on the DE-LU price series [APPLIED-AUTH]: `ruptures`; artifact must bracket the 2021–22 crisis onset + late-2022 normalization — validates `crisis_period` / `post_crisis` flags | SYL:M1 "change-point" row + SYL:M1-deliv #3 · CAP:§2.1 (the boundaries), §4 "Regime indicators" |
| G1 | **Month-1 gate:** hypothesis-testing + bootstrap notebooks + change-point artifact + consolidation verdict | SYL:M1-deliv #1–3 |
| **—** | **MONTH 1→2 SEAM** | |
| DL | CNN mini-project (B-Claude, standalone, 16h hard cap): CIFAR-10 in PyTorch, ship-at-threshold ~70%+, curves + confusion matrix + README — NOT wired into the capstone | SYL:Supp "DL" (table + scope red line + placement + routing note) |
| **—** | **MONTH 2 — Time-Series CV & Tree ML; capstone M1 lands (~mid-Aug → mid-Sep)** | |
| B-Man1 | DagsHub account creation (B-Manual; clerical, any time before M2 logging) | SYL:M2-interleave bullet 1 · CAP:§9.1 (what the account is for) |
| L14 | Walk-forward expanding-window CV, 24h embargo, full leakage taxonomy [AUTH] — Hyndman Ch. 5; Lago 2021 §3 | SYL:M2 "Walk-forward" row · CAP:§5.1–5.2 |
| L15 | Trees & gradient boosting [AUTH]: split criteria incl. quantile loss; LightGBM mechanics (Ke 2017); RF/bagging, ARIMA framing, FFT at [REC] | SYL:M2 "Decision tree" + "Gradient boosting" + "Random forests" + "ARIMA" + "FFT" rows · CAP:§6.1 |
| B-Man0 | *(optional, 10 min, pre-M1)* SMARD JS gas-page browser check — reopens the gas boundary only if a CC-BY, API-accessible daily THE **price** series appears; otherwise the boundary stands | CAP:§0 item 3 (narrow residual) + §3 SMARD row · PRG Blockers (optional item) |
| M1 | **Capstone data layer** (B-Claude): ENTSO-E + SMARD bulk pull 2019-01-01 → pull date, UTC + DST + 15-min handling, feature catalog v1 (climatology, Dunkelflaute, regime flags), KFT/LAG leakage audit | **CAP:§12 build-routing note (the M1 binding list — the brief's spine)** + §12 "M1" + §3, §4.0–4.1, §5.1–5.2, §9.3 · PRG Notes ("M1 brief" + "M1 cosmetic" items) · EUA optional: CAP:§3 Ember row (wire only if trivially clean) |
| CP-1 | Capstone checkpoint 1: feeds + archive depth, ENTSO-E↔SMARD €0.01 reconciliation, R-2 documented, regime flags spot-checked, CC BY attribution | CAP:§12 "CP-1" checklist · PRG Track B (spike pre-confirmed items 1, 3, 5) |
| SQL | Raw-SQL authoring block begins [APPLIED-AUTH]: parallel filler Months 2–3, 20h hard cap; toy table `ts, price, load, wind, solar` | SYL:Supp "SQL" (table + cap + setup note + done-condition) |
| L16 | Month-2 rehearsal deliverable: LightGBM + walk-forward CV + 24h embargo on a single feature set; MAE + pinball on ≥2 folds | SYL:M2 "Coding deliverable (learning-side)" |
| G2 | **Month-2 gate:** rehearsal deliverable runnable + consolidation verdict (CP-1 status carried up) | SYL:M2-deliv · CAP:§12 "CP-1" (status to carry) |
| **—** | **MONTH 3 — Quantile Regression & DM; capstone M2 lands; Track C activates (~mid-Sep → mid-Oct)** | |
| L17 | Paper-reading meta-skill (half-day) [REC] | SYL:M3 "Reading scientific papers" row |
| C4-1 | Classification & metrics [AUTH-light, 10–12h cap]: logistic, ROC/PR, imbalance, threshold tuning, calibration — one notebook deliverable | SYL:Supp "C4-1" (table + cap + deliverable) |
| L18 | Quantile / pinball loss [AUTH] + uncalibrated-quantiles-vs-coverage preview (Angelopoulos & Bates §1–2) | SYL:M3 "Quantile loss" + "Uncalibrated quantile" rows · CAP:§6.1, §5.2 (no-transform line) |
| L19 | Isotonic regression for quantile crossing [AUTH] | SYL:M3 "Isotonic" row · CAP:§6.2 (why isotonic stays last) |
| L20 | LightGBM deepening [AUTH]: leaf-wise growth, histogram splits, GOSS, EFB | SYL:M3 "LightGBM mechanics" row |
| L21 | Diebold-Mariano test [AUTH]: loss differential, HAC variance, one- vs. two-sided; Giacomini-White mention | SYL:M3 "Diebold-Mariano" row · CAP:§7.1 (incl. the pre-committed secondary gate) |
| M2 | **Capstone baselines + model** (B-Claude): similar-day naïve + seasonal-naïve 168h, Ridge, LightGBM 9-head quantile ensemble on the pinned 3-regime folds, isotonic wired, DM vs. naïve, MLflow → DagsHub, thin CI live | CAP:§12 "M2" + §6 (esp. §6.1 pyfunc packaging), §7 + §7.1, §5.1 (pinned folds), §9.1, §9.4 (thin CI) · SYL:M3-interleave bullets |
| CP-2 | Capstone checkpoint 2: ≥5 public MLflow runs on DagsHub, CI green on `main`, DM secondary gate reported | CAP:§12 "CP-2" checklist (incl. secondary gate + honest fallback) |
| TRIG | **Track C phase-trigger fires (post-M2):** continuous activation — recruiter-only open-to-work ON, outreach + target research begin | ORC "Track C activation rules" rule 3 · PRG Track C |
| CV-1 | CV iteration #1 (C-Claude): baselines + LightGBM + DM + public MLflow UI link | SYL:M5 "Track C interleave" (post-M2 CV window contents) · PRG Track C (positioning theme + 3-slot cadence) |
| LI-1 | Optional LinkedIn signal on M2 landing (Yarden's call) | ORC "Track C activation rules" rule 1 |
| C4-3a | Timed take-home rehearsal #1 (late Month 3): 4h box + 30-min debrief, no AI inside the box | SYL:Supp "C4-3" |
| G3 | **Month-3 gate:** SQL block done (LAG/LEAD cold) + consolidation verdict | SYL:Supp "SQL" done-condition |
| **—** | **MONTH 4 — Calibration, Conformal, Explainability; capstone M3 lands (~mid-Oct → mid-Nov)** | |
| L22 | CQR end-to-end [AUTH]: conformity scores, negative-Q subtlety, exchangeability paragraph; EnbPI/SPCI awareness only [REC] | SYL:M4 "CQR" + "EnbPI" rows · CAP:§6.2 (the verbatim exchangeability paragraph + negative-Q) |
| L23 | SHAP for tree ensembles [AUTH]: TreeExplainer, summary + dependence plots, correlated-feature pitfalls | SYL:M4 "SHAP" row · CAP:§8.1 |
| L24 | Permutation importance [AUTH]: what it answers vs. SHAP | SYL:M4 "Permutation" row · CAP:§8.2 |
| L25 | Calibration & reliability diagrams + fan-chart plotting in matplotlib [AUTH] | SYL:M4 "Calibration" + "Fan-chart" rows · CAP:§8.4 (incl. the two-sided floor caveat) |
| L26 | MLflow remote tracking + Model Registry on DagsHub [REC] | SYL:M4 "MLflow" row · CAP:§9.1 |
| M3 | **Capstone diagnostics** (B-Claude): CQR layer on held-out calibration set, SHAP + headline-feature selection, permutation importance, regime-stratified error table (incl. negative-price stratum), reliability diagram raw vs. final | CAP:§12 "M3" + §6.2 (calibration set), §8.1–8.4, §4.1 (headline selection rule) · Contingency: CAP:§13 EnbPI reopen (any stratum >10 pp → remediation comparison) |
| CP-3 | Capstone checkpoint 3: 80% coverage ±5pp on ≥4/5 folds; SHAP/permutation top-10 overlap ≥6; stratified table + caveats documented | CAP:§12 "CP-3" checklist |
| C4-3b | Timed take-home rehearsal #2 (4h box + debrief) | SYL:Supp "C4-3" |
| C4-4a | Mock interview #1 (late Month 4) | SYL:Supp "C4-4" |
| CV-2 | CV iteration #2 (C-Claude): conformal + SHAP + regime errors | SYL:M5 "Track C interleave" (post-M3 window) · PRG Track C |
| REV | Reviewer recruitment for the stranger test (C-Manual; Month 4 / early Month 5) | CAP:§10.1 (what the reviewers must do) |
| G4 | **Month-4 gate:** consolidation verdict (CP-3 status carried up) | CAP:§12 "CP-3" (status to carry) |
| **—** | **MONTH 5 — Ship, Deploy, Apply; capstone M4 + M5 land (~mid-Nov → mid-Dec)** | |
| B-Man2 | HF account + initial Spaces setup (B-Manual, start of Month 5) | SYL:M5-interleave bullet 1 · CAP:§9.2 |
| APP | **Active applications begin** — no later than the start of Month 5 (C-Manual, continuous from here) | ORC "Track C activation rules" rule 3 · PRG Track C (funnel state) |
| L27 | marimo reactive-notebook patterns [REC]: sliders, state management vs. Jupyter | SYL:M5 "Marimo" row · CAP:§9.2 (sliders), §10 |
| L28 | Reproducibility patterns [AUTH]: `uv` pinning, tagged commit, committed CC-BY snapshot; inference-script patterns (`predict_next_day.py`) | SYL:M5 "Reproducibility" + "Inference-script" rows · CAP:§9.3 (incl. staleness disclosure) + §9.2 (CLI role) |
| L29 | Docker multi-stage build patterns [APPLIED-REC] | SYL:M5 "Docker" row · CAP:§9.2 |
| L30 | HF Spaces deployment mechanics [APPLIED-REC]: Docker SDK, secrets, free-tier hardware, keep-alive cron + 60-day auto-disable, cold-start reality | SYL:M5 "Hugging Face Spaces" row · CAP:§9.2 (sleep/keep-alive) · Contingency: CPU Upgrade line in the same SYL row (fires only on CP-5 cold-start failure) |
| M4 | **Capstone local showcase** (B-Claude): marimo end-to-end locally, champion `pyfunc` registered `Production`, precomputed slider lookup + per-cell OOD flags (M4 spike), CLI smoke test in-container | CAP:§12 "M4" + §9.2 (lookup + OOD + registry-first/bundle-fallback), §6.1 (the one-artifact champion) |
| CP-4 | Capstone checkpoint 4: registry tag live, <10s local cold render, all 3 sliders from lookup, grid coverage + OOD flags validated | CAP:§12 "CP-4" checklist |
| M5 | **Capstone deploy** (B-Claude): multi-stage container → HF Spaces free tier, keep-alive cron configured, CV + LinkedIn updated with Spaces URL + public MLflow URL | CAP:§12 "M5" + §9.2 (deploy), §9.3 (attribution), §10 (reading order the artifact must render) |
| CP-5 | Capstone checkpoint 5: <30s cold start, registry-or-bundle model load, **stranger test passes on the deployed URL** | CAP:§12 "CP-5" checklist + §10.1 |
| L31 | Interview prep [AUTH]: the capstone script — leakage audit @12:00 CET gate, exchangeability, regime story, "why the German market, in Israel", "why hourly", "why no gas marker", negative-prices line, "why marimo", "why thin CI" | SYL:M5 "Interview prep" row · CAP:§13 (every answer, verbatim) + §5.2, §6.2 |
| C4-4b | Mock interviews #2–3 (~1h each) | SYL:Supp "C4-4" |
| CV-3 | CV iteration #3 (C-Claude): deployed showcase + Spaces URL — final CV | SYL:M5 "Track C interleave" (post-M5 window) · PRG Track C |
| G5 | **Month-5 gate / program envelope closes:** full artifact live, in-market with full-artifact applications continuing | ORC "Goal" · PRG |

**Standing rhythm (not single rows):** C7 networking ~1h/week from Month 1; weekly Monday snapshot refresh of the deployed demo during the application phase (CAP:§9.2); Track C application funnel continuous from the M2 phase-trigger onward.
