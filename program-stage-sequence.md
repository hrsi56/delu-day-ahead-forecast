# Program Stage Sequence — Full Ordered Map

*Generated 2026-07-02 by the orchestrator. Scheduling aid for the ~6.5-month program.*

**Authority note.** This map is derived from the ratified anchors — `syllabus_v3_0.md` v3.0 and `capstone_V6_1.md` v6.1 — and from `progress.md` (2026-06-14 state). Where this table and the anchors ever disagree, **the anchors win**. Stage IDs **L1–L3 match progress.md**; IDs from **L4 onward are provisional planning labels** — the actual block decomposition is fixed at session briefing (blocks may merge or split). Live status always lives in `progress.md`, not here. Calendar hints on the divider rows assume Month 0 launched 2026-06-09 and runs 5–6 weeks; they shift with reality.

Legend: `L` = learning block (NotebookLM) · `M` / `CP` = capstone milestone / checkpoint (Claude Code) · `G` = Track A month gate · `B-Man` = manual action · `C*` / `CV` / `LI` / `APP` / `REV` = Track C items · `DL`, `SQL`, `C4-x` = supplementary interview-readiness blocks. Depth labels per the syllabus: [AUTH] / [REC] / [APPLIED-AUTH] / [APPLIED-REC].

| Stage | Description |
|---|---|
| **—** | **SETUP (complete)** |
| M0 | Capstone plan ratified (v6.1) + data-layer de-risking spike run, adjudicated, merged to `main` (`docs/spike-feed-status.md`) |
| **—** | **MONTH 0 — Linear Algebra Foundations (launched 2026-06-09; 5–6 weeks → ~mid-July)** |
| L1 | Linear algebra 18.06 — Lectures 1–5 + Strang Ch. 1–2; Gaussian-elimination solver shipped |
| L2 | Linear algebra 18.06 — Lectures 6–10 + Ch. 3 [AUTH]: four fundamental subspaces; deliverable `four_subspaces(A)` |
| L3 | Linear algebra 18.06 — Lectures 14–17 [AUTH]: orthogonality → projections → least squares → Gram–Schmidt; OLS normal-equation deliverable (Month-0 deliverable #1) |
| G0-mid | **Month-0 mid-month gate** (~end June): coding deliverable(s) to date runnable + NotebookLM consolidation verdict — one-line status at next session opening |
| L4 | Eigenvalues, eigenvectors, diagonalization — 18.06 L21–22 + Strang Ch. 5–6 [AUTH] (determinants L18–20 skim only [REC]) |
| L5 | SVD, PCA, condition number [REC] — 18.065 fragments L6–8 + 3Blue1Brown; PCA + condition-number toy notebook on synthetic load/wind/solar/residual-load (Month-0 deliverable #2) — closes Month 0 |
| G0 | **Month-0 close gate:** both coding deliverables runnable + consolidation verdict |
| **—** | **MONTH 1 — Probability, Statistics, Applied Change-Point (~mid-Jul → mid-Aug)** |
| C7 | Networking floor begins (~1h/week, ongoing): former students, BGU alumni, one Tech7 / Gav-Yam Negev meetup per month (C-Manual) |
| L6 | Distributions — Stanford CS109 [AUTH]: Normal, Bernoulli, Poisson, Student-t, empirical |
| L7 | MLE as an optimization principle [AUTH]: likelihood vs. probability, consistency intuition |
| L8 | Hypothesis testing [AUTH]: p-values, one- vs. two-sided, multiple testing — + C4-2 A/B-testing rider [REC, ~4h]: power, sample size, peeking |
| L9 | Bootstrap confidence intervals on metric estimates [AUTH] |
| L10 | Bayes at recognition [REC]: combinatorics, conjugate priors, Bayesian-vs-frequentist frame |
| L11 | Pandas time-series practical block [AUTH, ~1 week]: tz `Europe/Berlin`→UTC, resampling incl. quarter-hour→hour, timestamp joins, lag/rolling features, parquet I/O |
| L12 | DE-LU domain reading [REC, ~3 days spread across Months 1–2]: Lago 2021 §2–3; Trebbien et al. 2023; Hilger et al. 2024 (skim) |
| L13 | Bayesian change-point on the DE-LU price series [APPLIED-AUTH]: `ruptures`; artifact must bracket the 2021–22 crisis onset + late-2022 normalization — validates `crisis_period` / `post_crisis` flags |
| G1 | **Month-1 gate:** hypothesis-testing + bootstrap notebooks + change-point artifact + consolidation verdict |
| **—** | **MONTH 1→2 SEAM** |
| DL | CNN mini-project (B-Claude, standalone, 16h hard cap): CIFAR-10 in PyTorch, ship-at-threshold ~70%+, curves + confusion matrix + README — NOT wired into the capstone |
| **—** | **MONTH 2 — Time-Series CV & Tree ML; capstone M1 lands (~mid-Aug → mid-Sep)** |
| B-Man1 | DagsHub account creation (B-Manual; clerical, any time before M2 logging) |
| L14 | Walk-forward expanding-window CV, 24h embargo, full leakage taxonomy [AUTH] — Hyndman Ch. 5; Lago 2021 §3 |
| L15 | Trees & gradient boosting [AUTH]: split criteria incl. quantile loss; LightGBM mechanics (Ke 2017); RF/bagging, ARIMA framing, FFT at [REC] |
| M1 | **Capstone data layer** (B-Claude): ENTSO-E + SMARD bulk pull 2019-01-01 → pull date, UTC + DST + 15-min handling, feature catalog v1 (climatology, Dunkelflaute, regime flags), KFT/LAG leakage audit |
| CP-1 | Capstone checkpoint 1: feeds + archive depth, ENTSO-E↔SMARD €0.01 reconciliation, R-2 documented, regime flags spot-checked, CC BY attribution |
| SQL | Raw-SQL authoring block begins [APPLIED-AUTH]: parallel filler Months 2–3, 20h hard cap; toy table `ts, price, load, wind, solar` |
| L16 | Month-2 rehearsal deliverable: LightGBM + walk-forward CV + 24h embargo on a single feature set; MAE + pinball on ≥2 folds |
| G2 | **Month-2 gate:** rehearsal deliverable runnable + consolidation verdict (CP-1 status carried up) |
| **—** | **MONTH 3 — Quantile Regression & DM; capstone M2 lands; Track C activates (~mid-Sep → mid-Oct)** |
| L17 | Paper-reading meta-skill (half-day) [REC] |
| C4-1 | Classification & metrics [AUTH-light, 10–12h cap]: logistic, ROC/PR, imbalance, threshold tuning, calibration — one notebook deliverable |
| L18 | Quantile / pinball loss [AUTH] + uncalibrated-quantiles-vs-coverage preview (Angelopoulos & Bates §1–2) |
| L19 | Isotonic regression for quantile crossing [AUTH] |
| L20 | LightGBM deepening [AUTH]: leaf-wise growth, histogram splits, GOSS, EFB |
| L21 | Diebold-Mariano test [AUTH]: loss differential, HAC variance, one- vs. two-sided; Giacomini-White mention |
| M2 | **Capstone baselines + model** (B-Claude): similar-day naïve + seasonal-naïve 168h, Ridge, LightGBM 9-head quantile ensemble on the pinned 3-regime folds, isotonic wired, DM vs. naïve, MLflow → DagsHub, thin CI live |
| CP-2 | Capstone checkpoint 2: ≥5 public MLflow runs on DagsHub, CI green on `main`, DM secondary gate reported |
| TRIG | **Track C phase-trigger fires (post-M2):** continuous activation — recruiter-only open-to-work ON, outreach + target research begin |
| CV-1 | CV iteration #1 (C-Claude): baselines + LightGBM + DM + public MLflow UI link |
| LI-1 | Optional LinkedIn signal on M2 landing (Yarden's call) |
| C4-3a | Timed take-home rehearsal #1 (late Month 3): 4h box + 30-min debrief, no AI inside the box |
| G3 | **Month-3 gate:** SQL block done (LAG/LEAD cold) + consolidation verdict |
| **—** | **MONTH 4 — Calibration, Conformal, Explainability; capstone M3 lands (~mid-Oct → mid-Nov)** |
| L22 | CQR end-to-end [AUTH]: conformity scores, negative-Q subtlety, exchangeability paragraph; EnbPI/SPCI awareness only [REC] |
| L23 | SHAP for tree ensembles [AUTH]: TreeExplainer, summary + dependence plots, correlated-feature pitfalls |
| L24 | Permutation importance [AUTH]: what it answers vs. SHAP |
| L25 | Calibration & reliability diagrams + fan-chart plotting in matplotlib [AUTH] |
| L26 | MLflow remote tracking + Model Registry on DagsHub [REC] |
| M3 | **Capstone diagnostics** (B-Claude): CQR layer on held-out calibration set, SHAP + headline-feature selection, permutation importance, regime-stratified error table (incl. negative-price stratum), reliability diagram raw vs. final |
| CP-3 | Capstone checkpoint 3: 80% coverage ±5pp on ≥4/5 folds; SHAP/permutation top-10 overlap ≥6; stratified table + caveats documented |
| C4-3b | Timed take-home rehearsal #2 (4h box + debrief) |
| C4-4a | Mock interview #1 (late Month 4) |
| CV-2 | CV iteration #2 (C-Claude): conformal + SHAP + regime errors |
| REV | Reviewer recruitment for the stranger test (C-Manual; Month 4 / early Month 5) |
| G4 | **Month-4 gate:** consolidation verdict (CP-3 status carried up) |
| **—** | **MONTH 5 — Ship, Deploy, Apply; capstone M4 + M5 land (~mid-Nov → mid-Dec)** |
| B-Man2 | HF account + initial Spaces setup (B-Manual, start of Month 5) |
| APP | **Active applications begin** — no later than the start of Month 5 (C-Manual, continuous from here) |
| L27 | marimo reactive-notebook patterns [REC]: sliders, state management vs. Jupyter |
| L28 | Reproducibility patterns [AUTH]: `uv` pinning, tagged commit, committed CC-BY snapshot; inference-script patterns (`predict_next_day.py`) |
| L29 | Docker multi-stage build patterns [APPLIED-REC] |
| L30 | HF Spaces deployment mechanics [APPLIED-REC]: Docker SDK, secrets, free-tier hardware, keep-alive cron + 60-day auto-disable, cold-start reality |
| M4 | **Capstone local showcase** (B-Claude): marimo end-to-end locally, champion `pyfunc` registered `Production`, precomputed slider lookup + per-cell OOD flags (M4 spike), CLI smoke test in-container |
| CP-4 | Capstone checkpoint 4: registry tag live, <10s local cold render, all 3 sliders from lookup, grid coverage + OOD flags validated |
| M5 | **Capstone deploy** (B-Claude): multi-stage container → HF Spaces free tier, keep-alive cron configured, CV + LinkedIn updated with Spaces URL + public MLflow URL |
| CP-5 | Capstone checkpoint 5: <30s cold start, registry-or-bundle model load, **stranger test passes on the deployed URL** |
| L31 | Interview prep [AUTH]: the capstone script — leakage audit @12:00 CET gate, exchangeability, regime story, "why the German market, in Israel", "why hourly", "why no gas marker", negative-prices line, "why marimo", "why thin CI" |
| C4-4b | Mock interviews #2–3 (~1h each) |
| CV-3 | CV iteration #3 (C-Claude): deployed showcase + Spaces URL — final CV |
| G5 | **Month-5 gate / program envelope closes:** full artifact live, in-market with full-artifact applications continuing |

**Standing rhythm (not single rows):** C7 networking ~1h/week from Month 1; weekly snapshot refresh of the deployed demo during the application phase; Track C application funnel continuous from the M2 phase-trigger onward.
