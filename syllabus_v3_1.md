# Accelerated DS Syllabus — v3.1 — for capstone_V6_2.md v6.2 (German DE-LU Lean DS Capstone with Cloud-Backed Showcase)

**Header.** Yarden's target is an industry Data Scientist role within ~6.5 months at NIS 35K. His formal math baseline is high-school level — applied stats and signal processing in practice, no university calculus or linear algebra. Month 0 is the binding constraint and is realistically **5–6 weeks at full depth, not 4**; treat 6 weeks as on-plan. Learning Months 0–1 are math-only and front-loaded; Months 2–5 interleave directly with capstone milestones M1–M5 from `capstone_V6_2.md` v6.2. **Pace decision: accept calendar slip from 6 months to ~6.5 months** rather than tighten KEEP-list authoring blocks. (v2.2 added two short interview-readiness blocks — a raw-SQL authoring block and a standalone DL mini-project — costing ~half a week total, absorbed within existing slack; v2.3 added the four C4 interview-surface blocks at ~24–28h of parallel filler across Months 1–4; **v3.0 is a market-conversion alignment release with zero pace impact** — the ~6.5-month envelope still holds.) The Month 1 Bayesian change-point applied block is a materially stronger interview asset than the time it costs, and the capstone diagnostics (SHAP, permutation, calibration) are where the artifact wins or loses. Cuts come from the KILL and COMPRESS lists, not from KEEP-authoring depth.

**(v3.1 pace amendment, 2026-07-12):** v3.1 is an **expansion release**, adopted under an explicit owner decision to optimize hire probability over the calendar envelope. Net new load ≈ 90–95h inside Months 0–5 (per-month math in the stage map's load appendix): Months 2–4 each run ~5–5.5 weeks at the 20–22h/week budget (or the budget rises to ~26–27h/week to hold 4-week months); the flagship envelope (G5) slides from ~mid-Dec to ~mid/late-January 2027. **Two anchors do not move:** active applications still begin at the start of program-Month 5 (in-market before the envelope closes), and the interview-algorithms block closes at the Month-4 gate, before applications. The post-envelope companion arc (fraud mini-capstone, ~92h, Months 6–7) is scheduled by the stage map, not this syllabus — see the pointer section added at the end (AMD-11).

Every sub-topic carries a depth label: **[AUTH]** (authoring — go deep), **[REC]** (recognition — compressed coverage), **[APPLIED-AUTH]** (use a library, understand output, recognition-level theory — you defend the result in interview), **[APPLIED-REC]** (use a library or config, recognize the pattern, no theory required — you follow a recipe and debug it). Every sub-topic carries a one-sentence link to a `capstone_V6_2.md` v6.2 deliverable.

**v2 → v2.1 delta.** Three surgical edits + two new rows to align with `capstone-lean.md` v5.4: (1) Month 4 MLflow row upgraded from local file-store to DagsHub-hosted remote tracking + Model Registry; (2) Month 5 showcase-format row collapsed from a three-way choice to marimo-mandated; (3) Month 5 reproducibility row updated from SHA-256 hashing to tagged-commit + committed-snapshot patterns; (4) two new [APPLIED-REC] rows added in Month 5 for Docker multi-stage and HF Spaces deployment mechanics; (5) the "Does NOT Teach" MLOps paragraph split into "now at recognition level" vs. "remains out of scope". No changes to Months 0, 1, 2; no changes to the math arc.

**v2.1 → v2.2 delta.** Two additive interview-readiness blocks, no changes to the existing month structure, the math arc, the depth-label vocabulary, or the capstone interleave: (1) a raw-SQL authoring block at [APPLIED-AUTH], parallel filler across Months 2–3, gating the interview funnel rather than a capstone milestone; (2) a standalone deep-learning mini-project at [AUTH] (CNN, outside capstone scope by design), slotted at the Month 1→2 seam. Both are placed to complete before active applications begin (start of Month 5). Pace impact: ~half a week, absorbed within existing slack.

**v2.2 → v2.3 delta.** Alignment release for `capstone_V5_5.md` v5.5 plus five accepted amendments from the 2026-06-10 adjudication (`change-register-decisions.md`); four proposed additions were reviewed and **rejected** and are recorded here so they do not resurface. *Accepted:* (1) **C5-min** — Month 0 resource span corrected to Strang Lectures 1–17; (2) **F8** — the Month 4 conformal row teaches **CQR** explicitly including the **negative-Q subtlety**; (3) **C4** — four interview-surface blocks added; (4) **CL5** — CNN mini-project default dataset → **CIFAR-10**; (5) **Rehearse** — Month 5 interview prep additions. *Rejected (do not re-add):* **LO3** (Month-0 SVD/PCA upgrade to [AUTH] + Eckart–Young), **LO2** (standalone causal block), **SC3-learn** (neural-baseline block), **SC5-learn** (EnbPI block — revives only under the pre-committed reopen condition). Pace impact: ~24–28h of parallel filler, absorbed.

**v2.3 → v3.0 delta (market conversion).** Alignment release for **`capstone_V6_1.md` v6.1** — the PJM Western Hub → German DE-LU conversion ratified 2026-06-11 (PJM geo-blocked from Israel; adjudication in the `de-lu-conversion-memo`). **No change to the math arc, the depth-label vocabulary, the month structure, the time budgets, or the supplementary SQL/CNN/C4 blocks; zero pace impact.** Touched content: all operative capstone references → `capstone_V6_1.md` v6.1; Month 0 — the collinearity interview answer recast from forecast-temperature×load to **load-forecast×residual-load** (a mechanical correlation, a stronger example), and the PCA toy dataset recast as synthetic load/wind/solar/residual-load series; Month 1 — the change-point block now targets the **DE-LU price series and validates two boundaries** (the 2021–22 crisis onset and the late-2022 normalization) instead of the single Elliott break, and the domain-reading block swaps Olivares 2023 (PJM-COMED) for **Trebbien et al. 2023 + Hilger et al. 2024** (German EPF) with Lago 2021 retained; Month 2 — the M1 interleave rewritten for ENTSO-E/SMARD ingestion, the residual-load feature catalog, the Dunkelflaute flag, and the R-2 vintage outcome; the ARIMA interview framing reworded (weather/gas out); a stale §5.4 reference corrected to §5.1; Month 3 — the headline baseline renamed to the **similar-day naïve (Lago convention)** and the fold-scheme reference re-pinned to the v6.1 three-regime scheme; Month 4 — the EnbPI reopen condition reworded (any regime stratum >10 pp), SHAP interleave plots relabeled to `dunkelflaute_flag` and the residual-load headline, fan-chart wording fixed to next-day; Month 5 — the slider set relabeled, the reproducibility row gains the CC BY attribution statement, and interview prep gains **"why the German market, in Israel"**, **"why hourly across the 15-minute transition"**, **"why no gas marker"**, and the **negative-prices / no-log-transform** line as a demonstrated capability; "Does NOT Teach" — the GNN and NBEATSx entries reworded for a single coupled zonal price (the PJM nodal-topology reasoning is obsolete); the SQL block's toy table schema updated. All v2.3 rejected-item records (LO3, LO2, SC3-learn, SC5-learn) carry forward unchanged.

**v3.0 → v3.1 delta (expansion release, 2026-07-12).** Adopts the four-course gap-analysis (6.006 / 18.065 / 6.341x / CS229 audited against this syllabus), the spectral-extension spec v1.0, and the algorithms-block spec v1.0; aligns with `capstone_V6_2.md` v6.2. *Added:* Month-0 PCA upgrade to [APPLIED-AUTH] (**LO3 partially reopened** — PCA only, on interview-frequency evidence; the full [AUTH]+Eckart–Young upgrade **remains rejected**); a Month-1 18.065 matrix rider [REC, ~4h]; a **Month 1→2 seam optimization section** [AUTH, ~10h: 18.065 L21–23, L25] with NN/backprop + optional Fourier riders around the CNN; the Month-2 **spectral-EDA row** [APPLIED-AUTH, 6–10h] replacing the obsolete FFT/spectrograms row (capstone v6.2 §4.2 — the "not used in the lean capstone" claim is retired); the **CLS-1/CLS-2 classification arc** in Month 3 (CLS-1 [AUTH, ~12h] supersedes C4-1; CLS-2 [~8h]: bias-variance [AUTH], SVM/kernels [REC], ERM [REC]); the **ALG interview-algorithms supplementary block** [APPLIED-AUTH, ~48h staggered Months 2–4, NeetCode-driven, 6.006 as backbone]; Month-4 **UNSUP** (~7h: k-means [APPLIED-AUTH], EM/GMM [REC]), **CAUS** (~6h — **LO2 reopened in light form**; the capstone's no-causal-claim boundary is untouched), and the **ERR rider** (CS229 L13 error analysis [APPLIED-AUTH], ~3h on the M3 diagnostics); three spectral interview Q&As in Month 5. *Absorption notes:* CS229 L8 (splits/CV) absorbs into the Month-2 walk-forward row; CS229 L10 (trees/ensembles) was already this syllabus's cited source; CS229 L11–12 are duplicates of the 18.065 L26–27 rider (skip). *Standing rejections:* SC3-learn and SC5-learn carry forward unchanged. *Pointer added:* post-envelope companion arc (Binary Classification Mini-Capstone) — pointer only, stage-gated.

---

## Month 0 — Linear Algebra Foundations + SVD/PCA Recognition Extension

**Time:** 5–6 weeks at 20–22 hrs/week.
**Goal:** Read linear algebra cleanly enough to follow Ridge regression geometry, OLS via normal equations, PCA, and the SHAP "linear in feature space" approximation. Plus a brief SVD/PCA + condition number extension that pays off in interviews.

| Sub-topic | Depth | Resource | Capstone link |
|---|---|---|---|
| Vectors, matrix operations, four fundamental subspaces, OLS via normal equations | [AUTH] | MIT 18.06 (Strang) **Lectures 1–17** (least squares is OCW Lecture 16, Gram–Schmidt 17 — verify against the live OCW index at briefing; Lectures 18–20 are determinants, skim per the [REC] row below); Strang *Introduction to Linear Algebra* Ch. 1–4 | OLS/Ridge baseline (capstone Section 7); feature standardization for the Ridge benchmark |
| Eigenvalues, eigenvectors, diagonalization | [AUTH] | MIT 18.06 Lectures 18–22; Strang Ch. 5–6 | Required prerequisite for the SVD/PCA extension below and for reading correlation structure in the feature catalog |
| SVD as generalization of eigendecomposition; PCA as SVD on centered data matrix; variance-explained interpretation | **[APPLIED-AUTH] (PCA; v3.1 LO3 partial reopen)** — SVD framing and Eckart–Young remain [REC] | Selected fragments from MIT 18.065 (Strang) Lectures 6–8; 3Blue1Brown SVD video; CS229 PCA lecture + 18.065 L6 for the applied upgrade (~2–3h incremental) | Used as the diagnostic tool for detecting multicollinearity in the engineered feature catalog (Section 4 of capstone) |
| Condition number of a matrix; what it implies for multicollinearity among features | [REC] | Same as above; one section of Strang *Linear Algebra and Learning from Data* | Answers the standard interview question *"how would you detect collinearity between the load forecast and residual load?"* (a **mechanical** correlation — residual load is constructed from the load forecast) — *"I'd check the condition number of the standardized feature matrix and inspect the singular value spectrum."* |
| Determinants, abstract eigenvalue properties, Jordan forms | [REC] | Skim only — Strang Ch. 5 last sections | None directly; recognition only for completeness |

**v3.1 timing note:** if L5 has already been briefed or closed at [REC] by the time v3.1 is adopted, the PCA upgrade does not reopen Month 0 — it runs as a ~2–3h Month-1 rider alongside L-MTX (below). Either way the deliverable standard is the [APPLIED-AUTH] one: explain variance-explained, when/why to use PCA, and its limits, cold, in interview.

**Coding deliverables (Yarden ships at the end of the month):**
1. OLS from the normal equation `A^T A x̂ = A^T b` in NumPy on a small synthetic dataset. Plot the projection error vectors.
2. PCA on a 5–10-feature toy correlated dataset (e.g., **synthetic load / wind / solar / residual-load series with engineered correlations** — residual load built as load − wind − solar so the collinearity is mechanical). Report variance-explained per component, the condition number of the standardized feature matrix, and the singular-value spectrum. This is the rehearsal for the same diagnostic on the real capstone feature matrix in Month 2.

**Explicit cuts vs. v1 syllabus:** the Eckart-Young low-rank approximation proof, Frobenius-norm bounds, special-matrix theory (Fourier, circulant, banded), and the bulk of MIT 18.065 are out. The interview-relevant SVD/PCA story is preserved at recognition depth.

---

## Month 1 — Probability, Statistics, and Applied Bayesian Change-Point

**Time:** 4 weeks at 20–22 hrs/week (no slip expected here).
**Goal:** Hypothesis testing fluency for the Diebold-Mariano test, MLE intuition for understanding why quantile loss converges to conditional quantiles, bootstrap for honest confidence intervals on metrics, and an applied change-point block that *validates* the `crisis_period` / `post_crisis` regime flags rather than assuming them.

| Sub-topic | Depth | Resource | Capstone link |
|---|---|---|---|
| Distributions Yarden will actually meet: Normal, Bernoulli, Poisson, Student-t, Empirical | [AUTH] | Stanford CS109 (Piech) selected lectures on random variables, joint distributions, continuous distributions | Foundation for everything else this month |
| MLE as an optimization principle; likelihood vs. probability; consistency intuition | [AUTH] | CS109 lectures on parameter estimation; one chapter of any standard probability text | Why fitting a quantile regression converges to conditional quantiles; foundation for change-point block |
| Hypothesis testing, p-values, one-sided vs. two-sided, multiple testing awareness | [AUTH] | CS109 inference lectures | Diebold-Mariano test (capstone Section 7.1) — p-value reporting in the final results table |
| Bootstrap for confidence intervals on metric estimates | [AUTH] | One short tutorial (Efron's original is overkill; pick the chapter from *All of Statistics* or a focused blog post) | Bootstrap CIs around MAE / pinball loss / coverage estimates in the final results table; CIs on the thin regime strata (Dunkelflaute days, negative-price hours — capstone Section 8.3) |
| Combinatorics, full Bayes derivations, conjugate priors | [REC] | CS109 first lectures only | None — keep at recognition for the change-point block context |
| Bayesian vs. frequentist contrast | [REC] | One short essay (Jaynes or a modern blog post) | Frame for the change-point block |
| **Bayesian change-point detection on the DE-LU day-ahead price series** | **[APPLIED-AUTH]** | `ruptures` library docs + one short paper on PELT / BinSeg; *Bayesian Online Changepoint Detection* (Adams & MacKay 2007) at skim depth | **Capstone Section 4 (regime indicators) and Section 8.3 (regime-stratified error analysis).** The interview payoff is *"I didn't just hard-code the crisis regime — I detected its boundaries empirically: the detector bracketed the 2021–22 onset and the late-2022 normalization. The flags are validated, not assumed."* Bonus teaching point: the onset is diffuse (gas run-up vs. invasion) — a live example of change-point uncertainty. |

**Parallel blocks this month:**
- **Pandas / Python time-series practical block** [AUTH] (~1 week, ADD-1). Index/timezone handling (tz-aware `Europe/Berlin` → UTC), resampling (incl. quarter-hour → hour, rehearsing the capstone §4.0 15-min boundary), joins on timestamps, vectorized lag/rolling features, parquet I/O. Used immediately in every subsequent capstone block.
- **DE-LU domain reading** [REC] (~3 days, spread across Months 1 and 2). Lago 2021 §2–3 (EPF benchmark methodology — retained); **Trebbien et al. 2023, *Energy & AI*** (SHAP on a gradient-boosted model of German day-ahead prices — the capstone's published methodological twin); **Hilger et al. 2024, *Applied Energy*** at skim depth (probabilistic German EPF with regime adaptation). Foundation for the capstone narrative.
- **A/B testing / experimentation** [REC] (~4h, v2.3 C4) — rides on this month's hypothesis-testing block while the machinery is fresh: power, sample size, peeking, randomization units. Full detail in the *Supplementary Interview-Readiness Blocks* section.
- **18.065 matrix riders** [REC] (~4h, v3.1 L-MTX) — parallel filler: L5 positive-definite/PSD and covariance intuition; L8 vector/matrix norms and the L1/L2 ↔ regularization link; L9 the four ways to solve least squares (feeds the Month-3 Ridge baseline directly); L10 condition-number difficulties with Ax=b (extends the Month-0 collinearity answer). Recognition depth only — no derivations authored.
- **DL mini-project (non-capstone)** [AUTH] — slotted at the **Month 1 → Month 2 seam**, after the math slog and before the capstone M1 build ramps. Standalone CNN (**CIFAR-10 default**), explicitly outside capstone scope. Full scope, red line, and routing in the *Supplementary Interview-Readiness Blocks* section below. 16-hour hard cap.

**Coding deliverables:**
1. Hypothesis testing playground notebook: t-tests, chi-square, p-value calculation by hand and by `scipy`.
2. Bootstrap CIs around a synthetic MAE estimate; demonstrate that bootstrap CIs and the textbook normal-approximation CI agree when the residual distribution is well-behaved and diverge when it's heavy-tailed.
3. **Change-point detector on the DE-LU day-ahead price series.** Run `ruptures` with a sensible cost function; report detected breakpoints; verify the breakpoints **bracket the crisis** — one in the 2021-09 → 2022-02 onset window, one near the 2022→2023 normalization. Save the output as the artifact that validates the `crisis_period` / `post_crisis` flags in the capstone feature catalog.

---

## Month 1→2 Seam — First-Principles Optimization (v3.1)

**Time:** ~10h (L-OPT) + the existing 16h-capped CNN build + ~5h of riders; the seam widens from ~1 week to ~2 weeks.
**Goal:** Close the program's first-principles optimization gap **before** the CNN build — gradient descent, momentum, and SGD are directly tested in Israeli DS interviews and underpin both the deep-learning surface and the "gradient boosting = functional gradient descent" framing that carries the Month-3 LightGBM defense.

| Sub-topic | Depth | Resource | Capstone link |
|---|---|---|---|
| Minimizing a function step by step; gradient descent geometry, learning rate, convergence intuition | [AUTH] | 18.065 L21–L22 (Strang) | LightGBM fits trees to negative gradients (capstone §6.1) — this is the principle underneath |
| Momentum / accelerated gradient descent | [AUTH] | 18.065 L23 | Interview surface (optimizer families); feeds the CNN's optimizer choice |
| Stochastic gradient descent: minibatches, noise-as-feature, why SGD generalizes | [AUTH] | 18.065 L25 | CNN training loop; the "SGD vs Adam" interview answer |
| Linear regression by gradient descent (unifying view) | [REC] | CS229 L2 — absorbed as reinforcement, not a separate block | Connects to the Month-0 normal-equations work and the Ridge baseline |

**Riders around the CNN build (v3.1 DL+, ~5h total):** immediately before or during the CNN mini-project, (a) **NN structure + backpropagation** [REC] via 18.065 L26–L27 — primary source; CS229 L11–L12 cover the same ground and are skipped as duplicates; understand backprop, don't memorize it; (b) **optional enrichment:** 18.065 L31–L32 (circulant eigenvectors / Fourier matrix; the convolution rule) [REC] — bridges the signal-processing background to the CNN's convolution operation and to the Month-2 spectral-EDA block. The CNN build itself is unchanged: same 16h hard cap, same scope red line, same routing (see the DL block in *Supplementary Interview-Readiness Blocks*).

## Month 2 — Time-Series, Cross-Validation, and Tree-Based ML — Capstone M1 Interleaves Here

**Time:** ~4 weeks at 20–22 hrs/week.
**Goal:** Walk-forward CV with embargo at full authoring depth, leakage taxonomy that Yarden can recite, gradient-boosting mechanics deep enough to defend LightGBM in an interview, and the "why not classical methods?" answer for ARIMA/SARIMA at the 30-second level.

**Parallel block (non-capstone):** the **SQL raw-query authoring block** begins as light-week filler this month and continues into Month 3 — full detail in the *Supplementary Interview-Readiness Blocks* section. It feeds no capstone milestone; it gates the interview funnel and must be complete before active applications (start of Month 5). **Also this month (v3.1):** the **interview-algorithms block (ALG)** begins its light start — ~2h/week (~8h): Arrays & Hashing + Two Pointers, 6.006 L4 anchor, Python-idioms sub-block, solutions repo + progress log created. Full detail, cadence, downgrade rule, and the capstone-wins conflict rule in the *Supplementary Interview-Readiness Blocks* section.

| Sub-topic | Depth | Resource | Capstone link |
|---|---|---|---|
| Walk-forward expanding-window CV; gap/embargo windows; autocorrelation leakage; the leakage taxonomy (target leakage, train-test contamination, look-ahead bias, group leakage) | [AUTH] | Hyndman & Athanasopoulos *Forecasting: Principles & Practice* Ch. 5; Lago 2021 §3 | Capstone Section 5.1 (24h embargo) and Section 5.2 (KFT/LAG leakage audit anchored at the 12:00 CET gate, incl. the R-2 VRE-vintage caveat) |
| Decision tree splitting: entropy, Gini, MSE, **and quantile loss / pinball loss** | [AUTH] | Stanford CS229 (Ng) decision tree and boosting lectures; Hastie, Tibshirani, Friedman *ESL* Ch. 9–10 selected sections | Capstone Section 6.1 (LightGBM with 9 quantile heads) |
| Gradient boosting: how trees are fit to negative gradients; learning rate, max_depth, min_child_samples, L1/L2 leaf penalties; categorical handling; monotone constraints | [AUTH] | CS229 boosting; Ke et al. 2017 (LightGBM paper) end-to-end | Same — capstone Section 6.1 |
| Random forests, bagging, AdaBoost | [REC] | One 5-minute compare to LightGBM | Recognition only — used to answer "why LightGBM over random forest?" |
| ARIMA / SARIMA / ETS classical methods | [REC] | Hyndman Ch. 8–9 at skim depth | **Interview-question framing only:** Yarden must answer *"Why not classical methods here?"* in 30 seconds with the structural reasons (heavy non-linearity on regime-stress and negative-price days, large feature spaces from load + wind/solar/residual-load + calendar + lags, mature evidence in the EPF literature that GBMs match or beat classical on this data). |
| Spectral EDA of the DE-LU price series: DFT frames and frequency resolution; why the raw periodogram is inconsistent; **Welch's method** (Hann window, averaged modified periodograms, the variance–resolution trade-off); detrend/difference before the periodogram (low-frequency leakage); per-regime spectra as evidence of regime non-stationarity; ACF cross-check; optional MSTL | **[APPLIED-AUTH]** | `scipy.signal.welch` + statsmodels ACF/MSTL; 6.341x U8–U9 selected fragments (~40–50 min theory refresh, inside the block); the existing signal-processing background does the rest | **Capstone v6.2 §4.2** — confirms the 24h/168h/12h seasonal structure behind the calendar/residual-load features and the per-regime spectral change behind the three-regime folds; 6–10h inside M1's window; three CP-1 items + R-5 guardrails per §4.2; one showcase figure earmarked for M4 (§10 item 3b) |

**Capstone interleave (this is when M1 lands):**
- ENTSO-E Transparency API token (B-Manual — request already in flight from Month 0, ahead of the data-layer de-risking spike). SMARD is keyless. DagsHub account creation (B-Manual, must precede M2 logging — schedule clerically in Months 0–2).
- Historical bulk pull from **ENTSO-E (A44 prices, A65/A01 load forecast, A69 VRE forecasts on DE-LU `10Y1001A1001A82H`) + SMARD cross-pull via `entsoe-py` ≥0.7.5** — feed statuses and the **R-2 vintage outcome** pre-confirmed by the Month-0 de-risking spike; window 2019-01-01 → the pull date, UTC-indexed, **15-min boundary handled** (quarter-hours averaged to hourly post-2025-10-01), Fold 5 dates pinned at the pull (capstone §3, §4.0, §5.1).
- Feature catalog v1 implementation, including **`residual_load_deviation_from_normal`** (train-only Fourier climatology fit on the residual-load forecast series) as the primary domain-insight candidate, **`scarcity_stress = relu(load_z)·relu(−vre_z)`** as the secondary, the **train-only Dunkelflaute thresholds**, and the regime indicator features `crisis_period` / `post_crisis` (with the **R-2** vintage outcome — as-published vintages or the pre-authorized as-archived fallback — applied; capstone §4, §5.2, §11).
- KFT/LAG leakage audit drafted (uses the leakage taxonomy from this month's reading; anchored at the 12:00 CET D-1 gate).
- **Spectral EDA (v6.2 §4.2)** lands after the bulk pull (it consumes the ingested series) and before the CV-design work it partly justifies: `spectral_eda.py`, three mandatory figures, README interpretation paragraph. R-5 scope guardrails apply (no filters/wavelets/frequency-domain forecasting).
- CP-1 closes M1 (incl. the ENTSO-E↔SMARD reconciliation gate and the CC BY attribution item) **and the three §4.2 spectral checklist items (v6.2)**.

**Coding deliverable (learning-side, not capstone):**
- LightGBM on a single feature set (need not be the full capstone catalog) with walk-forward CV and 24h embargo, reporting MAE and pinball loss on at least two folds. This is the rehearsal before capstone M2.

---

## Month 3 — Quantile Regression, Isotonic, Diebold-Mariano — Capstone M2 Lands

**Time:** ~4 weeks at 20–22 hrs/week.
**Goal:** The mathematics behind capstone Section 6 and Section 7 at full authoring depth, plus the Diebold-Mariano test wired into the results.

**Parallel blocks (non-capstone):** the **SQL raw-query authoring block** (begun in Month 2) completes this month — see *Supplementary Interview-Readiness Blocks*. 20-hour hard cap across the two months; done when the LAG/LEAD window-function queries can be written cold. **Also this month (v3.1):** the **classification theory arc** lands — **CLS-1** [AUTH, ~12h; supersedes C4-1, whose 10–12h budget it absorbs] early in the month, **CLS-2** [~8h] mid-month — and **timed take-home rehearsal #1** (~4h box) lands late in the month, consuming CLS-1's output. The **ALG block ramps** (~5h/week, ~20h: Sliding Window, Stack, Binary Search, Heaps/Top-K) as SQL completes and frees its slot. Full detail in the Supplementary section. *(v3.1 supersession: wherever this document or its briefs reference C4-1, read CLS-1.)*

| Sub-topic | Depth | Resource | Capstone link |
|---|---|---|---|
| Quantile loss / pinball loss derivation; asymmetric penalty intuition; conditional quantile interpretation; why the median minimizes MAE while quantile loss generalizes this | [AUTH] | Koenker *Quantile Regression* Ch. 1 (selected sections); LightGBM docs on `objective='quantile'` | Capstone Section 6.1 (9 quantile heads), Section 6.2 (motivates split conformal); behaves correctly on the routinely-negative DE-LU target (capstone §5.2 — no log transform) |
| Uncalibrated quantile estimates vs. coverage guarantees — what each means and why they differ | [AUTH] | Angelopoulos & Bates *Gentle Introduction to Conformal Prediction* §1–2 (preview only this month; full read in Month 4) | Capstone Section 6.2 (split conformal motivation) |
| Isotonic regression for quantile crossing; `sklearn.isotonic.IsotonicRegression` | [AUTH] | sklearn docs; one short tutorial | Capstone Section 6.1 (isotonic post-processing) |
| LightGBM mechanics deepening: tree growing strategy (leaf-wise vs. depth-wise), histogram-based splits, GOSS, EFB | [AUTH] | Ke et al. 2017 second pass; LightGBM source code skim | Defends LightGBM choice in interview |
| Diebold-Mariano test: loss differential series, autocorrelation correction (HAC variance), test statistic derivation, one-sided vs. two-sided framing; mention Giacomini-White as the conditional alternative | [AUTH] | Diebold & Mariano 1995 original paper; `scipy.stats` implementation walkthrough | Capstone Section 7.1 (DM test reported in results, comparator = the similar-day naïve) |
| Reading scientific papers efficiently (LightGBM, conformal, SHAP — what Yarden needs vs. exhaustively) | [REC] | Half-day meta-skill block at the start of the month | Pays for itself across the remaining papers this and next month |

**Capstone interleave (this is when M2 lands):**
- **Similar-day naïve baseline (Lago convention: Tue–Fri → same hour previous day; Mon/Sat/Sun → same hour one week prior)** + seasonal-naïve 168h baseline.
- Ridge baseline with the engineered feature catalog (uses the OLS / normal-equation work from Month 0).
- LightGBM quantile ensemble end-to-end with walk-forward CV (24h embargo, **v6.2 three-regime fold scheme: crisis-peak Fold 3 Jul–Sep 2022, negative-price-stress Fold 4 May–Jul 2025, Fold 5 ending at the pull date, fully post-15-min-transition**) and **MLflow logging to the DagsHub-hosted tracking URI**.
- Isotonic post-processing wired in.
- Diebold-Mariano test against the **similar-day naïve**, with statistical significance reported. (CP-2 carries the **pre-committed secondary gate** — Fold-5 p ∈ [0.05, 0.15] + pooled-across-folds DM significant → pass, both numbers reported; capstone §7.1.)
- **Thin CI wired (v6.2):** GitHub Actions runs the capstone §9.4 invariant tests (now four, incl. the 15-min boundary test) on every push — no regression matrix.
- CP-2 closes M2 (≥ 5 MLflow runs publicly visible on DagsHub UI; CI green on `main`).

---

## Month 4 — Calibration, Conformal, and Explainability — Capstone M3 Lands

**Time:** ~4 weeks at 20–22 hrs/week.
**Goal:** The diagnostic stack that distinguishes the artifact from a generic LightGBM tutorial. CQR conformal at full authoring depth (two papers, focused), SHAP at full authoring depth, permutation importance as a complement, reliability diagrams that visibly compare raw and conformal-adjusted intervals.

**Parallel blocks (non-capstone, v2.3 C4):** **timed take-home rehearsal #2** (~4h box) and the **first mock interview** land this month — see *Supplementary Interview-Readiness Blocks*. **Also this month (v3.1):** the **ALG block peaks and closes** (~5h/week, ~20h: Trees + BFS/DFS on grids/graphs, intro 1-D DP, plus the ≥4 timed 25-min mock solves — nothing bleeds into Month 5); the **UNSUP block** (~7h: k-means [APPLIED-AUTH], EM/GMM [REC]) and the **CAUS block** (~6h, LO2 light reopen — causal-inference frame [REC] + A/B experiment-design deepening [APPLIED-AUTH]) run as parallel filler. Full detail in the Supplementary section.

| Sub-topic | Depth | Resource | Capstone link |
|---|---|---|---|
| **Conformalized Quantile Regression (CQR) — the construction the capstone ships:** exchangeability assumption; held-out calibration set; per-pair conformity scores `E_i = max{q̂_lo(x_i)−y_i, y_i−q̂_hi(x_i)}`; symmetric threshold adjustment per interval; finite-sample **per-interval marginal** coverage guarantee; **the negative-Q subtlety** — when the raw heads over-cover, `Q` can be negative and *narrow* the interval, which is why isotonic stays last; **why time-series mildly violates exchangeability and what that means for empirical coverage on regime-shift folds** | [AUTH] | Angelopoulos & Bates *A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification* end-to-end; **Romano, Patterson & Candès 2019 (CQR), §2 minimum** | Capstone Section 6.2 — the exchangeability paragraph the artifact quotes verbatim is the interview centerpiece; the negative-Q point defends the CQR-then-isotonic post-processing order; both behave correctly on negative and zero-crossing intervals (the DE-LU target is routinely negative) |
| EnbPI, SPCI, weighted conformal, online conformal | [REC — skip past] | One paragraph awareness, nothing more | Capstone explicitly does **not** include these; interview-quotable reason in Section 13 of capstone — which carries the **single pre-committed reopen condition** (any regime stratum's empirical coverage diverging > 10 pp from nominal at M3 → EnbPI returns as remediation, comparison only) |
| SHAP for tree ensembles: Shapley values from cooperative game theory, the TreeExplainer algorithm, global vs. local explanations, summary plot, dependence plot, interaction interpretation, **common pitfalls (correlated features producing misleading attributions; SHAP is not a causal explanation)** | [AUTH] | Lundberg & Lee 2017 (KernelSHAP); Lundberg 2020 (TreeSHAP) | Capstone Section 8.1 (SHAP summary + top-10 + two dependence plots); the correlated-features pitfall is live here — load forecast and residual load are mechanically correlated. Trebbien et al. 2023 is the published twin to cite. |
| Permutation importance: `sklearn.inspection.permutation_importance` mechanics; why it answers a different question from SHAP (degradation under shuffling vs. attribution in expectation); when each is misleading | [AUTH] | sklearn docs + one focused tutorial | Capstone Section 8.2 (permutation importance alongside SHAP) |
| Calibration and reliability diagrams: conditional vs. marginal coverage, reliability plots, what coverage divergence indicates, how to read one honestly | [AUTH] | Conformal tutorial above + one short blog post on reliability diagrams | Capstone Section 8.4 (reliability diagram for raw and conformal-adjusted intervals; two-sided bounded-target caveat — the −500 floor is live in this market) |
| Fan-chart and reliability-diagram plotting in matplotlib | [AUTH] | matplotlib docs; one short tutorial (ADD-2) | Capstone Section 8.4 and the next-day quantile fan chart in the final artifact |
| **MLflow with cloud-backed tracking and a Model Registry** — remote tracking URI configuration against a DagsHub-hosted server; logging hyperparameters, per-fold metrics, and artifacts (SHAP plots, reliability diagrams, regime-stratified tables); Model Registry concepts (Staging / Production lifecycle tags); how the public DagsHub UI exposes experiment history to hiring managers via permalink | [REC] | MLflow docs on tracking server + Model Registry; DagsHub MLflow integration docs; one short walkthrough video | Capstone Section 9.1 (DagsHub-hosted MLflow tracking + Model Registry; public read-only UI linked from CV and LinkedIn) |

**Capstone interleave (this is when M3 lands):**
- Split conformal (CQR) calibration layer on top of LightGBM heads, fit on the held-out calibration set.
- SHAP global summary + top-10 + two dependence plots (**`dunkelflaute_flag` × hour-of-day; headline domain feature × `dunkelflaute_flag`** — `residual_load_deviation_from_normal` by default, `scarcity_stress` if SHAP selects it at M3; capstone §8.1).
- Permutation importance on validation tail.
- Regime-stratified error table (crisis / pre-crisis / post-crisis + Dunkelflaute days + **negative-price hours**; n_obs + bootstrap CIs on thin subsets).
- **ERR rider (v3.1, ~3h):** apply the CS229 L13 error-analysis method [APPLIED-AUTH] to the regime-stratified error table — bucket the largest errors, name the dominant failure mode per regime, estimate the ceiling from fixing each bucket. Becomes a standing diagnostic habit and an interview-ready story.
- Reliability diagram for raw and conformal-adjusted intervals at the 50% / 80% / 95% levels.
- CP-3 closes M3.

---

## Month 5 — Artifact, Polish, Containerization, Deployment, Interview Prep — Capstone M4 and M5 Land; Track C Activates

**Time:** ~4 weeks at 20–22 hrs/week, with the final 1–2 weeks shifting partly to Track C (CV iteration, LinkedIn signal, interview prep, applications).
**Goal:** Ship the deployed marimo showcase on Hugging Face Spaces and begin applying. Two [APPLIED-REC] rows this month cover the containerization and deployment patterns Yarden's CV will quote.

| Sub-topic | Depth | Resource | Capstone link |
|---|---|---|---|
| **Marimo as the mandated showcase format** — reactive notebook patterns; how reactive sliders update plots, SHAP attributions, and forecast curves live; UI element conventions (`mo.ui.switch`, `mo.ui.slider`, `mo.ui.dropdown`); state management vs. classical Jupyter | [REC] | marimo docs + one short comparison piece (marimo vs. Jupyter for reactive notebooks) | Capstone Section 10 — marimo is mandated, not chosen; the **three interactive sliders** (**`dunkelflaute_flag` toggle, headline-feature perturbation** — `residual_load_deviation_from_normal` or `scarcity_stress` per the M3 SHAP selection — **quantile-level selector**), served from the precomputed lookup with the per-cell OOD flag, are the centerpiece of the deployed artifact |
| Reproducibility patterns: `pyproject.toml` version pinning via `uv` (incl. `entsoe-py` ≥ 0.7.5); seed-setting across NumPy / sklearn / LightGBM; tagged-release-commit convention; committed Parquet snapshot at the tagged release for reviewer one-step reproducibility; **the CC BY 4.0 attribution statement (ENTSO-E Transparency Platform; Bundesnetzagentur \| SMARD.de) in the README and data folder** | [AUTH] | One short tutorial on `uv` + git tag workflows; pyproject.toml docs | Capstone Section 9.3 — reproducibility statement: pinned deps, tagged commit, committed snapshot (legally redistributable, CC BY), public DagsHub MLflow permalinks |
| Inference-script patterns: idempotent data pulls, defensive smoke tests, clean Parquet output schemas. `predict_next_day.py` ships inside the container as a fallback CLI for cold-start regeneration and local development — not the user-facing artifact | [AUTH] | Pattern reading from real OSS forecasting projects | Capstone Section 9.2 (CLI fallback inside the container) |
| **Docker multi-stage build patterns** — base layer with locked dependencies; application layer with notebook code + data snapshot; why multi-stage matters for HF Spaces image-size limits; layer caching; `.dockerignore` discipline; common gotchas | [APPLIED-REC] | Docker official multi-stage docs; one short HF Spaces Docker tutorial | Capstone Section 9.2 — containerized marimo showcase; the Dockerfile is the M5 deployable artifact |
| **Hugging Face Spaces deployment mechanics** — Spaces SDK selection (Docker mode); `app.py` entry-point conventions; secrets management via Spaces Settings (DagsHub token); free-tier hardware reality (~2 vCPU, 16 GB RAM, 48h sleep timeout); GitHub Actions keep-alive cron pattern and its 60-day auto-disable; cold-start latency expectations and the README "~30s first-load" disclaimer; CPU Upgrade contingency ($0.03/hr ≈ $22/month) if cold start empirically fails CP-5 | [APPLIED-REC] | HF Spaces docs on Docker SDK + secrets + hardware tiers; one short reference deployment from another portfolio project | Capstone Section 9.2 (deployment) + CP-5 (deployed-URL stranger-test) |
| Interview prep: rehearse the leakage audit answer (anchored at the 12:00 CET gate, incl. the R-2 vintage honesty line — *"as-archived, the same convention as the entire published benchmark literature"*), the exchangeability paragraph, the regime-stratified error story (true-OOS crisis-peak Fold 3 + negative-price Fold 4), "why not classical methods?", "why not a neural challenger?", "why not DVC?", "why no live API pulls?", "how did you detect collinearity?" (load forecast × residual load), "what does the DagsHub MLflow UI show?", **"why the German market, in Israel?"** (the 30-second transfer answer: *consequential, noisy, regime-shifting public time series with a published benchmark literature — same problem shape as demand forecasting, fintech risk, ad-spend pacing, anomaly detection on telemetry*), **"why hourly across the 15-minute transition?"** (continuity of a 7.5-year three-regime series beats nine months of quarter-hours; SDAC's no-arbitrage constraint defines the hourly equivalent), **"why no gas marker?"** (no redistributable TTF/THE series; residual load carries the merit-order signal; pre-committed reopen if SMARD's THE data proves CC BY), **negative prices / "why no log transform?"** (pinball, the CQR score, and isotonic are location-equivariant — 573 negative hours in 2025 make this a demonstrated capability, not a caveat), **"why marimo, not Streamlit/Gradio?"**, and **"why a thin CI but no regression matrix?"**, **"how did you choose your seasonal features?"** (the Welch periodogram answer — 24h/168h/12h peaks, Weron 2014 / Lago et al. 2018 as the literature echo; v6.2 §13), **"how do you know your folds respect the regime changes?"** (change-point detection + per-regime periodograms showing spectral non-stationarity; v6.2 §13), and **"where did your signal-processing background help?"** (Welch-vs-raw-periodogram, windowing, variance–resolution; v6.2 §13) **Mock interviews ×2–3 (~1h each, v2.3 C4) run here and in late Month 4**, before applications mature. | [AUTH] | Self-rehearsal against the "What this project is NOT" section of `capstone_V6_2.md` v6.2 | The capstone interview script, prepared explicitly |

**Capstone interleave (this is when M4 and M5 land):**
- HF account + initial Spaces setup (B-Manual block, scheduled at the start of Month 5).
- **M4 lands first — local end-to-end.** Marimo showcase runs locally pulling the registered Production model from DagsHub MLflow and applying CQR thresholds on the snapshot data; `predict_next_day.py` smoke-test passes inside the container. CP-4 closes.
- **M5 lands second — deployed.** Marimo showcase containerized via multi-stage Dockerfile and deployed to HF Spaces free tier; GitHub Actions keep-alive cron configured (60-day auto-disable noted); CV and LinkedIn updated with the live Spaces URL and the public MLflow URL. CP-5 closes.
- **Stranger-test gate happens on the deployed HF Spaces URL, not locally.** Reviewer recruitment is a Track C-Manual block scheduled earlier in Month 4 / early Month 5.

**Track C interleave (begins this month):**
- Per `orchestrator-role.md` Phase-trigger rule, Track C activates continuously after M2 — but the application *pace* picks up in Month 5 as the diagnostic stack and the final artifact become showable.
- CV iteration windows (the three permitted across the year): after M2 (baselines + LightGBM + DM test + public MLflow UI link), after M3 (conformal + SHAP + regime errors), after M5 (deployed marimo showcase + Spaces URL). Each is a C-Claude block.
- LinkedIn signal: optional at M2 landing; surface to Yarden, his call.
- Active applications begin no later than the start of Month 5.

---

## Supplementary Interview-Readiness Blocks (v2.2 + v2.3 additions)

These blocks sit outside the math arc and outside the capstone interleave. None feeds a capstone milestone; all close gaps that surface specifically in the DS interview funnel. They are placed to land before or alongside active applications (start of Month 5) and to double as concrete artifacts during the math-heavy stretch.

### SQL — Raw-Query Authoring Against a Real DB

**Goal:** Author raw SQL cold (no ORM) at the level a DS SQL screen probes. The gap is *authoring fluency*, not relational fundamentals — those are already solid (PK/FK modeling, one-to-many with cascade, transactions, aggregations, conflict-check-before-insert with bulk update), but written through SQLAlchemy, so the raw-query muscle was never exercised. A SQL screen is cold authoring under pressure, which is why this is [APPLIED-AUTH] and not [REC].

| Sub-topic | Depth | Resource | Link |
|---|---|---|---|
| Manual JOINs (inner/left/right/full), multi-table joins | [APPLIED-AUTH] | Mode Analytics SQL Tutorial (Intermediate); PostgreSQL docs (joins) | Mirrors the relational joins the ORM wrote implicitly in the RSVP app — now authored by hand |
| GROUP BY + HAVING, aggregations, DISTINCT, NULL filtering | [APPLIED-AUTH] | Mode Analytics; pgexercises.com (Aggregation set) | The same `func.max`/DISTINCT/NULL logic used via ORM, in raw form |
| Subqueries and CTEs (`WITH`), including chained CTEs | [APPLIED-AUTH] | Mode Analytics (Advanced); PostgreSQL docs (`WITH` queries) | Readable multi-step transforms — the SQL analog of a pandas method chain |
| Window functions: ROW_NUMBER, RANK, DENSE_RANK; **LAG / LEAD**; PARTITION BY + ORDER BY frames | [APPLIED-AUTH] | PostgreSQL docs (Window Functions); pgexercises.com (Window set) | **`LAG(price, 24) OVER (ORDER BY ts)` *is* the capstone lag-24h feature — same idea, SQL surface. Reinforces feature-engineering intuition rather than being disconnected drill.** Most common topic in DS SQL screens. |
| Query-planner internals, EXPLAIN/ANALYZE, indexing strategy | [REC] | Skim only — one short overview | Recognition only — not probed in a DS SQL screen. Do not author. |

**Placement & cap:** Parallel filler across Months 2–3, on the light weeks. **20-hour hard cap.** Complete before active applications (start of Month 5). Modular, 1-hour-chunkable; must not displace math or capstone-authoring depth.

**Setup note:** NotebookLM can't run SQL, so author against a real DB — reuse the existing Supabase instance or spin up local Postgres with a toy capstone-shaped table (**`ts, price, load, wind, solar`**). Trivial; folds into the block, not its own action.

**Coding deliverable:** ~15–20 hand-authored queries of increasing complexity, culminating in 3–4 window-function queries that reproduce the capstone's lag features (lag-24h, lag-168h, rolling stats) in raw SQL. When you can write the LAG/LEAD queries cold, the block is done — do not keep adding query types.

### ALG — Interview Algorithms (v3.1) [APPLIED-AUTH]

**Goal:** Clear the LeetCode-style algorithmic coding screen used by a large share of Israeli DS employers (Wix: SQL + LeetCode-style Python; Lightricks: LeetCode question + classic data-structures round; Gong: algorithmic problem-solving; Mobileye: algorithms proficiency). The instrument is a **NeetCode 150 subset on high-frequency patterns** with MIT 6.006 as the theory backbone — not full-course consumption, and not competitive programming. DS screens are materially easier than SWE screens: the hard graph/DP tail is deliberately trimmed.

| Pattern | Problems | Hours | 6.006 anchor | Example problems |
|---|---|---|---|---|
| Arrays & Hashing | 12 | 11 | L4 | Two Sum; Group Anagrams; Top-K Frequent; Product Except Self |
| Two Pointers | 6 | 5 | (L3 foundation) | Valid Palindrome; 3Sum; Container With Most Water |
| Sliding Window | 6 | 6 | — | Buy/Sell Stock; Longest Substring w/o Repeating; Min Window Substring |
| Stack | 5 | 4 | — | Valid Parentheses; Min Stack; Daily Temperatures |
| Binary Search | 6 | 6 | L3 | Binary Search; Koko Eating Bananas; Rotated Sorted Array |
| Heaps / Top-K | 5 | 5 | L8 | Kth Largest; K Closest Points; Task Scheduler |
| Trees + BFS/DFS (grids & graphs) | 10 | 8 | L9–L10 | Invert Tree; Level-Order; Number of Islands; Clone Graph; Rotting Oranges |
| Intro DP (1-D) | 6 | 5 | L15–L16 | Climbing Stairs; House Robber; Coin Change; LIS |
| Python-idioms sub-block (woven in) | — | 2 | — | `Counter`, `defaultdict`, `heapq`, `sorted(key=…)`, comprehensions, `enumerate`/`zip` |
| **Total** | **~50 target** | **~48h** | | |

**Placement & cadence (staggered — defended):** Month 2 light start (~2h/week, ~8h: patterns 1–2) while SQL is heaviest; Month 3 ramp (~5h/week, ~20h: patterns 3–6) as SQL completes and frees its slot; Month 4 peak (~5h/week, ~20h: patterns 7–8 + mocks). **The block closes at the Month-4 gate — nothing bleeds into Month 5** (applications). Done-conditions: **end Month 2:** ≥12 solved incl. all Arrays/Hashing; **end Month 3:** ≥32 solved through Heaps/Top-K, solutions repo public and pattern-organized; **end Month 4:** ≥50 solved, all patterns, ≥4 timed mocks logged.

**The 6.006 anchors are watched inside the block** as [REC]-style refreshers (a heap primer before Top-K, a BFS/DFS primer before graphs) — never as separate L-blocks; the learning-block sequence stays reserved for the core curriculum.

**Re-solve policy:** any problem failed, or solved only with the solution open, is re-queued and re-solved after 1 week; a pattern is complete only when all its problems pass first-try on the latest attempt. **Tracking:** `progress_log.md` table — Date | Problem | Pattern | Difficulty | First-try? | Time | Re-solve due.

**Month-4 timed-mock protocol:** ≥4 mock solves, each one unseen Medium (or two Easies) in a hard 25-minute box, **talking aloud** (brute force → optimization → complexity), plain editor, no autocomplete/AI. Pass = correct + near-optimal + clear verbal reasoning inside the box. Fails become re-solves.

**Deliverable & signal:** a clean, pattern-organized public solutions repo with 2–3-line approach/complexity notes per solution — a mild profile positive and a spaced-repetition store; the *real* deliverable is screen performance, not repo aesthetics.

**Pre-committed downgrade rule (verbatim):** *If by end of Month 3 the C8 target-list research shows ≥80% of active-funnel companies use a take-home / dataset-assignment format (Riskified/CyberArk-style) rather than a live algorithmic-coding screen, downgrade the remaining Month-4 block from [APPLIED-AUTH] to [REC] maintenance: 1 problem/week, drop the mock protocol to 2 mocks, and reallocate the freed ~15h to the capstone M3–M4 diagnostics and take-home rehearsal.*

**Conflict-resolution rule (verbatim):** *The algorithms block never blocks a capstone milestone (M1–M5) or checkpoint (CP-1–CP-5). In any week where a capstone milestone is at risk or the weekly budget is exceeded, algorithms yields first: skip that week's problems, preserve the re-solve queue, resume the following week. Missed weeks are absorbed by the Month-4 buffer, never by delaying a capstone CP.*

**Anti-goals:** no full 6.006 consumption; no competitive-programming tail (no segment trees, no Dijkstra/Bellman-Ford beyond recognition, no Hard-grinding); no start before Month 2 (Months 0–1 math is the binding constraint); never a portfolio centerpiece.

### DL — Standalone CNN Mini-Project (Outside Capstone Scope)

**Goal:** Ship one artifact that proves end-to-end network build-and-train capability. The gap is a *missing artifact*, not missing knowledge — CNNs and backprop were taught (1-on-1, plus course grade 94), but there is no DL project, no trained model, no repo. Taught + graded = explained knowledge; recruiters buy *proven* doing. The value here is the shipped repo, not theory depth or accuracy.

| Sub-topic | Depth | Resource | Link |
|---|---|---|---|
| CNN architecture in PyTorch (2–3 conv blocks + pooling + 1–2 FC); forward pass, loss, optimizer, training loop | [AUTH] | PyTorch official "Training a Classifier" (CIFAR-10) tutorial; torchvision datasets docs | None by design — standalone. Theory stays at [REC] (already taught), not re-derived. |
| Train/val/test split, curve logging (loss + accuracy), confusion matrix, example predictions | [AUTH] | Same; matplotlib | None — the artifact's evidence layer |
| One regularization round — dropout **or** basic augmentation (not both, not a sweep) | [REC] | torchvision.transforms docs | None — demonstrates awareness, capped at one |
| HP search, transfer learning, deeper nets, SOTA tuning | OUT | — | Red line — explicitly excluded |

**Task:** CNN on **CIFAR-10** (**default, v2.3 CL5** — ship-at-threshold ~70%+), with **Fashion-MNIST** as the de-scope fallback only if the 16-hour cap threatens. NOT time-series. NOT a tabular MLP. PyTorch, CPU/MPS on the M3.

**Scope red line (pre-committed against completionism):**
- Ship at a sane threshold (~90%+ Fashion-MNIST, ~70%+ CIFAR-10 with a basic CNN) → stop.
- No HP sweep / grid / Optuna. No transfer learning / ResNet. No SOTA chase. No deployment, no app.
- **Hard stop:** first clean run clearing the threshold, plus curves + confusion matrix + clean README (seed set, deps pinned) + a "what I'd do with more time" paragraph (where stretch goals get *named*, not built) = DONE. Resist improving it.

**Placement & cap:** Month 1 → Month 2 seam, before the capstone M1 build ramps. **16-hour hard cap, 2–3 focused days.** Lands the artifact ~Month 2 for the first CV pass, and does double-duty as the palate-cleanser between the Months 0–1 math slog and the capstone grind.

**Routing note:** This is a **B-Claude build** (engineer → Claude Code → debug loop), not an L block — flagged standalone, *do not wire into the DE-LU capstone* (no-NN by design; inflating it would break the defended-boundary narrative). It appears in the syllabus only so the learning arc is complete on paper.

### Interview-Surface Blocks (v2.3, C4)

Four blocks closing funnel-specific gaps the program otherwise leaves open. They gate the interview funnel, not a capstone milestone, and all caps are hard — these blocks must never displace math or capstone-authoring depth.

**CLS-1 — Classification theory arc, part 1 (v3.1; supersedes C4-1).** The biggest structural gap in the program: everything taught is regression/forecasting while most Israeli DS screens probe classification, and the flagship artifact is regression-only. CLS-1 upgrades the old C4-1 from [AUTH-light] metrics coverage to a true [AUTH] theory arc, absorbing C4-1's 10–12h budget into ~12h.

| Sub-topic | Depth | Resource | Link |
|---|---|---|---|
| Logistic regression: decision boundary, MLE derivation, regularization | [AUTH] | CS229 L3 | Core interview topic; the interpretable baseline of every classification take-home |
| Perceptron + GLMs — the exponential-family view unifying linear/logistic/Poisson | [AUTH] | CS229 L4 | Elegant interview material; unifies the Month-0 OLS work with classification |
| GDA + Naive Bayes; the generative-vs-discriminative distinction | [AUTH] | CS229 L5 | Classic interview question, asked almost verbatim |
| Metrics surface (absorbed from C4-1): ROC/PR and when each is right, confusion-matrix trade-offs, threshold selection, class imbalance (weights vs resampling vs threshold moving), calibration-curve awareness | [AUTH] | sklearn docs; one focused imbalanced-learning tutorial | Gates the interview funnel; rides the Month-2 tree/boosting intuition |

**Placement & cap:** early Month 3, parallel filler, **~12h**. **Deliverable:** one notebook on a public imbalanced tabular dataset — logistic + LightGBM classifier, a Naive-Bayes-vs-logistic generative/discriminative comparison note, ROC/PR comparison, threshold tuning against a stated cost trade-off, calibration curve. Feeds take-home rehearsal #1 directly. *(Post-envelope, this arc is also the theory prerequisite of the companion classification artifact — see the pointer section; nothing here enters the DE-LU capstone.)*

**CLS-2 — Classification theory arc, part 2 (v3.1).** ~8h, mid/late Month 3, parallel filler: **bias-variance trade-off [AUTH]** (the formal decomposition + the 60-second interview answer — asked constantly); **SVMs: margins + the kernel trick [REC]**; **ERM / generalization frame [REC]** (VC dimension recognition-only). Resources: CS229 L6–L7, L9; ESL selected sections. **Deliverable:** a one-page bias-variance derivation + a kernel one-pager.

**C4-2 — A/B testing / experimentation.** [REC], **~4h**, rides the Month 1 hypothesis-testing block while power/sample-size machinery is fresh: power, sample size, peeking and sequential-testing pitfalls, randomization units. **Deliverable:** a one-page cheat sheet + three worked sample-size calculations. *(v3.1: extended in Month 4 by the CAUS block below.)*

**C4-3 — Timed take-home rehearsals ×2.** Generic tabular classification CSV, **4-hour box**, ship a notebook — the actual funnel format, rehearsed under the actual constraint. One in late Month 3 (consumes C4-1's output), one in Month 4. ~4h each + a 30-minute debrief naming what was cut under time pressure (the debrief is the learning artifact). Routed as B-Claude-free solo work — no AI assistance inside the box, by design.

**C4-4 — Mock interviews ×2–3.** ~1h each, late Month 4 → Month 5, before applications mature. Cover the capstone script (the §13 answers + the protected interview lines), classification fundamentals (C4-1), and a cold SQL question (SQL block). Routed as C-blocks: Claude chat as interviewer with a structured brief, or a human peer where available.

**UNSUP — Unsupervised essentials (v3.1).** ~7h, Month-4 parallel filler: **k-means [APPLIED-AUTH]** — inertia, choosing k, failure modes, when clustering is the wrong tool; it appears in take-homes and screens. **EM/GMM [REC]** — soft assignment, the E/M alternation intuition (CS229 L14); **factor analysis** recognize-only. **Deliverable:** one clustering notebook on the CLS-1 take-home dataset (clusters as EDA, not as the model).

**CAUS — Causal frame + experimentation deepening (v3.1; LO2 reopened in light form).** ~6h, Month-4 parallel filler, extending C4-2: potential-outcomes framing and confounding [REC]; why the capstone deliberately makes **no** causal claim (the §13 boundary, now defensible from first principles rather than by fiat); A/B experiment-design deepening [APPLIED-AUTH] — power/MDE, randomization units, sequential-peeking pitfalls, a CUPED mention. Converts the published clinical-research statistics background (bootstrap-mediation SEM work) into a named interview asset. **Deliverable:** the C4-2 cheat sheet extended to two pages + one fully-designed experiment write-up. *(The "Does NOT Teach" causal boundary is amended, not deleted — see AMD-10.)*

**Firewall note (mirrors the CNN/SQL reconciliation):** none of the four blocks enters the DE-LU capstone. They exist because the interview funnel probes surfaces the capstone deliberately does not cover. The v3.1 additions (ALG, CLS-1/2, UNSUP, CAUS) inherit the same firewall: none enters the DE-LU capstone. The one deliberate exception in v3.1 is the **spectral-EDA block**, which is *not* a supplementary block at all — it is capstone scope (v6.2 §4.2) and lives in the Month-2 table.

## What This Syllabus Does NOT Teach

Each omission below is a deliberate scope decision tied to `capstone_V6_2.md` v6.2. Yarden can quote each in interviews when asked. The 2026-06-10 review explicitly considered and **rejected** four proposed additions to this syllabus (LO3, LO2, SC3-learn, SC5-learn — see the v2.3 delta), and the 2026-06-11 market conversion re-ratified every boundary that survives the data swap — so the boundaries below are re-ratified, not merely inherited.

**Amended at v3.1 (2026-07-12):** two of the four rejection records are partially reopened on new evidence, per the four-course gap analysis. **LO3 — partially reopened:** PCA rises to [APPLIED-AUTH] on interview-frequency grounds (a targeted reopen justified by the funnel, not by the capstone); the original rejection's substance stands — no [AUTH] SVD arc, Eckart–Young stays [REC]. **LO2 — reopened in light form** as the Month-4 CAUS block, converting the clinical-research background into interview surface; the capstone's no-causal-claim boundary is untouched. **SC3-learn and SC5-learn stand unchanged** (the EnbPI pre-committed reopen condition remains the only path back).

**Graph neural networks (CS224W, GraphSAGE, message passing).** *"The lean capstone doesn't use a graph anywhere. DE-LU is a single coupled bidding zone with one zonal clearing price — there is no nodal topology in the target at all. A graph model would earn its place on cross-border flow or nodal redispatch problems; at the bidding-zone level, gradient-boosted trees on the engineered feature catalog cover the same signal more transparently."*

**NBEATSx and other deep time-series architectures.** *"The peer-reviewed EPF evidence shows classical and tree-based baselines within a few percent of deep-learning forecasts on zone-level day-ahead price, and the recent German-market explainability literature (Trebbien et al. 2023) runs on exactly the gradient-boosted model class the capstone ships. Spending the curriculum budget on NBEATSx mechanics would have demonstrated a tool I wouldn't use in the capstone over a tool I would."* *(The Month-3 neural-baseline build block — SC3-learn — was proposed and rejected with capstone SC3; the no-neural-challenger boundary was re-ratified, and again at the v6.1 conversion. The shipped CNN plus the published evidence carry the "can you do DL / why no NN?" pair.)*

> **Note (v2.2 — DL reconciliation):** A standalone CNN mini-project (see *Supplementary Interview-Readiness Blocks*) was added to close the general "no shipped DL artifact" gap. This is consistent with the exclusions in this section, not in tension with them: the exclusions concern the **capstone's** modeling choices, and the capstone still uses **no neural challenger**. The CNN is image classification, deliberately *not* a deep time-series model, and is *not* wired into the DE-LU project. Interview framing stays clean: *"I can build and train networks — here's a shipped CNN — and I chose gradient boosting for the capstone on the merits, not for lack of the alternative."*

**EnbPI, SPCI, and sequential conformal prediction generally.** *"CQR gives finite-sample per-interval marginal coverage guarantees under exchangeability, which is the property an interview reader is most likely to recognize and probe. The sequential variants handle non-exchangeability more aggressively but add conceptual surface area that distracts from the project's core argument. The reliability diagram makes the exchangeability violation visible, and the limitations section names it."* *(An EnbPI learning block — SC5-learn — was proposed and rejected with capstone SC5. Single pre-committed reopen condition, anchored in capstone v6.2 §13: **any regime stratum's** empirical coverage diverging > 10 pp from nominal at M3 → EnbPI returns as remediation and the Month-4 block revives at [APPLIED-AUTH]. Below that threshold, this boundary stands.)*

**Causal inference, DAGs, do-calculus, counterfactual ATE.** *"The capstone makes no causal claim. It makes a predictive claim with calibrated uncertainty. Causal inference is a separate discipline with a separate evidentiary bar, and conflating it with forecasting is one of the more common interview red flags. I deliberately stayed on the predictive side of that line."* *(A standalone causal-inference interview block — LO2 — was proposed and rejected: Months 3–4 filler slack is committed to C4 + SQL, and the published SEM bootstrap-mediation work already carries the interview answer without a new block. Backlog-only.)* *(Amended v3.1: LO2 partially reopened as the CAUS interview-surface block — see Supplementary. The boundary in this paragraph is unchanged: the artifact still makes no causal claim, and CAUS makes that boundary defensible from first principles.)*

**Mixed-integer linear programming, BESS arbitrage, Approximate Dynamic Programming, Pyomo, GLPK.** *"The capstone deliberately stops at the forecast. Wrapping a forecast in a battery-storage optimization or a trading layer either requires real risk infrastructure or it becomes a toy. A toy decision layer would have undermined the project's credibility. The forecast and its honestly-communicated uncertainty are the artifact."*

**MLOps stack — partially in, partially out.** Under v6.2 the boundary is unchanged from v5.5 in structure:

- *In scope at recognition / applied-recognition level:* **Docker multi-stage build patterns** (Month 5 [APPLIED-REC]), **DagsHub-hosted MLflow tracking + Model Registry** (Month 4 [REC]), **Hugging Face Spaces deployment mechanics** (Month 5 [APPLIED-REC]), and **the thin GitHub Actions CI** that runs the capstone's §9.4 invariant tests (now four, incl. the 15-min boundary test) on push — wiring at [APPLIED-REC]-level effort inside the M2 build, not a curriculum topic. Interview-quotable rationale: *"The capstone's MLOps surface is portfolio-grade — containerized marimo on Hugging Face Spaces, backed by a public DagsHub-hosted MLflow Model Registry, with invariant tests running on every push. This demonstrates fluency with the standard ML portfolio-hosting stack and gives hiring managers a publicly inspectable experiment history. It is not enterprise MLOps infrastructure."*
- *Remains explicitly out of scope:* **DVC** (rejected; superseded by pinned deps + tagged commit + committed CC-BY snapshot), **Evidently AI** (no drift monitoring), **FastAPI** (no API layer — the marimo notebook IS the user-facing layer), **CI/CD regression matrices, scheduled retraining cron, automated rollback machinery, drift gates** (the thin invariant-test CI is not a regression matrix — capstone v6.2 §13 holds that line explicitly). Interview-quotable rationale: *"DVC, Evidently, FastAPI, CI/CD regression matrices, and drift monitoring are enterprise MLOps boilerplate. AI-generated code handles them correctly in any real role with a real codebase. Spending portfolio time on them would have demonstrated boilerplate over judgment. The investment instead went into calibration, diagnostics, and interactive uncertainty communication — the parts of a forecasting system that are hard to get right and that signal DS judgment."*

**The full breadth of MIT 18.065 (matrix methods).** *"Selectively useful — SVD, PCA, condition number as a multicollinearity diagnostic. The Eckart-Young proof, low-rank approximation theorems, and special-matrix theory weren't needed for the capstone and didn't earn their place against the math-baseline timeline."* *(A proposal to upgrade Month-0 SVD/PCA to [AUTH] and restore Eckart–Young — LO3 — was reviewed and rejected: Month 0 is the binding constraint, the capstone's use of SVD/PCA is diagnostic and [REC] covers it. If the Month-0 consolidation verdict flags the SVD story as shaky, remediation fires through the existing checkpoint channel — not through a pre-emptive depth upgrade.)*

## Post-Envelope Companion Arc (pointer only — v3.1)

After capstone CP-5 closes and the Month-5 gate passes, a second, standalone Track B artifact begins: the **Binary Classification Mini-Capstone** (IEEE-CIS fraud detection — file: `Binary Classification Mini-Capstone.md` in project knowledge), ~92h across program-Months 6–7, running inside the active application phase. Within *this* syllabus, its learning prerequisites are already complete by the end of Month 4 (CLS-1/2, UNSUP, the metrics-and-calibration surface), so take-homes arriving from Month 5 onward are covered before the artifact itself ships.

**This pointer is deliberately all this syllabus says about it.** No month in this document depends on that plan, and it is **not read, briefed, or consumed before its time** — its execution anchors are the orchestrator instructions and the program-stage-sequence map (rows B-Man3, FM0–FM5, FCP-1–5, G6), which sequence and brief it when its time comes.

---

*End of Accelerated DS Syllabus — v3.1.*
