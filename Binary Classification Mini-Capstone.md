# Capstone Companion Plan — Binary Classification Mini-Capstone: E-Commerce Card Fraud Detection (IEEE-CIS / Vesta)

## Executive Summary — The Dataset Decision

**Winner: IEEE-CIS Fraud Detection (Vesta Corporation, Kaggle 2019).** After scoring nine candidate datasets against the nine vetting criteria, IEEE-CIS is the decisive choice. It is the only candidate that simultaneously satisfies every hard requirement: real-world provenance (no synthetic asterisk), a "sweet-spot" imbalance (3.5% fraud, 20,663 positive cases — enough imbalance to force the PR-AUC/threshold/cost story, but enough absolute positives for stable evaluation), deep feature-engineering surface (~430+ columns spanning card, address, email, device, and Vesta-engineered features), documented leakage traps that make a killer interview story, a genuine time axis for out-of-time validation, a CPU-friendly footprint (~1.8–2 GB in default dtypes, ~540–650 MB after standard downcasting — comfortable on M3/16 GB), and the strongest possible market alignment: it is functionally identical to the Riskified take-home ("build a logic-based model to detect fraudulent transactions") and the CyberArk "classic prediction homework."

**Runner-up (fallback): Home Credit Default Risk (Kaggle).** Real financial data, multi-table relational structure (strong SQL/feature-engineering story), ~8% default rate, same Kaggle licensing pattern. Chosen as fallback because it survives the same compliance workflow and offers a comparable engineering narrative if IEEE-CIS becomes unavailable.

**Escape-hatch (permissive licensing): the Fraud-Detection-Handbook simulator (Le Borgne, Siblini, Lebichot & Bontempi, 2022, Université Libre de Bruxelles).** Its notebook code is GPL v3.0 and its prose/pictures are CC BY-SA 4.0, so a fully-redistributable synthetic transaction dataset can be regenerated from the published simulator and committed directly to the repo if Kaggle access is ever impossible. Synthetic, so used only as a last resort.

### Scored candidate comparison (each criterion 1–5, weighted; realism/imbalance/FE-depth/leakage/temporal weighted heaviest, market/differentiation as tiebreakers)

| Dataset | Realism | Imbalance | FE depth | Leakage story | Temporal | Size/HW | License | Market fit | Differentiation | **Weighted total** |
|---|---|---|---|---|---|---|---|---|---|---|
| **IEEE-CIS Fraud (Vesta)** | 5 | 5 | 5 | 5 | 5 | 4 | 3 | 5 | 4 | **★ 4.6** |
| Home Credit Default Risk | 5 | 4 | 5 | 4 | 3 | 4 | 3 | 4 | 4 | 4.1 |
| KKBox Churn (WSDM) | 5 | 4 | 5 | 4 | 5 | 3 | 3 | 3 | 4 | 4.0 |
| Fraud-Detection-Handbook sim | 3 | 4 | 4 | 4 | 5 | 5 | 5 | 4 | 3 | 3.9 |
| CICIDS2017 / CSE-CIC-IDS2018 | 4 | 4 | 3 | 3 | 3 | 3 | 4 | 4 | 3 | 3.4 |
| PaySim (synthetic mobile money) | 2 | 4 | 3 | 3 | 4 | 4 | 5 | 3 | 2 | 3.1 |
| ULB Credit Card Fraud | 5 | 3 | 1 | 2 | 2 | 5 | 4 | 4 | 2 | 3.0 |
| Give Me Some Credit | 4 | 4 | 2 | 2 | 1 | 5 | 4 | 3 | 2 | 2.9 |
| IBM Telco Customer Churn | 4 | 3 | 3 | 2 | 1 | 5 | 5 | 3 | 1 | 2.7 |

### Defense of the winner against each criterion

1. **Realism/provenance (5):** Real card-not-present e-commerce transactions donated by Vesta Corporation. Per the Kaggle competition overview: "Vesta Corporation is the forerunner in guaranteed e-commerce payment solutions. Founded in 1995, Vesta pioneered the process of fully guaranteed card-not-present (CNP) payment transactions… Today, Vesta guarantees more than $18B in transactions annually." Yarden can say "I worked with real transaction data from a guaranteed-payments company processing $18B+ annually" with zero asterisk.
2. **Imbalance (5):** 20,663 fraudulent of 590,540 (3.5%). This is the Goldilocks zone — imbalanced enough that ROC-AUC-vs-PR-AUC, threshold selection, and cost-sensitive evaluation are forced, but with ~20K positives the PR-AUC and operating-point estimates are stable (unlike ULB's 492 positives, which make bootstrap CIs wide and folds unstable).
3. **Feature-engineering depth (5):** ~431 features (400 numerical, 31 categorical) plus relative timestamp and label: TransactionAmt, ProductCD, card1–card6, addr1/addr2, P/R_emaildomain, C1–C14 counts, D1–D15 timedeltas, M1–M9 match flags, V1–V339 Vesta-engineered features, plus identity table (DeviceType, DeviceInfo, id_01–id_38). Supports the entire feature-engineering syllabus: entity (UID) construction, group aggregations, frequency/target encoding, and NaN-structure analysis. This is the polar opposite of ULB's meaningless PCA components (V1–V28) — which is exactly why ULB is rejected as winner despite its realism.
4. **Leakage traps (5):** Documented, teachable, and central to top solutions. Per NVIDIA's write-up of Chris Deotte's 1st-place solution, the winning approach hinged on "the creation of a unique credit card client ID (UID) from card1, addr1, and D1 features leading to additional aggregated features" (the winning ensemble of XGBoost + CatBoost + LGBM reached 0.9459 private-LB AUC). If those UID aggregates are computed across the whole dataset they leak the future, and random K-fold *hides* the leak because it appears in both train and validation folds. This is the single best interview story in the project and rhymes directly with the flagship's leakage-taxonomy block.
5. **Temporal structure (5):** TransactionDT is a relative timestamp; train and test do not overlap in time and have a ~one-month gap between them, so the data was split by time. This enables genuine out-of-time validation, mirroring the flagship's walk-forward CV.
6. **Size vs. hardware (4):** train_transaction loads to ~1.77–1.96 GB in default dtypes; the standard `reduce_mem_usage` downcast (float64→float32/16, int downcasting) cuts this ~50–70% to ~540–650 MB (documented community results: "Mem. usage decreased to 542.35 Mb (69.4% reduction)"), fitting 16 GB comfortably. A single LightGBM fit runs in roughly 5 minutes on CPU (a published TDS walkthrough reports "It took around 5 minutes"). Only risk: naive one-hot expansion of high-cardinality categoricals blows up RAM — mitigated by using LightGBM native categorical handling. Docked one point for the need for memory discipline.
7. **Licensing (3):** Kaggle competition rules prohibit redistributing the raw Competition Data ("You agree not to transmit, duplicate, publish, redistribute or otherwise provide or make available the Competition Data to any party not participating in the Competition"). This does NOT block the project: the trained model, code, derived non-reconstructive artifacts, and demo are fine. Compliance pattern specified below. Docked because raw data cannot be committed.
8. **Market alignment (5):** Best possible. The Riskified take-home is literally, per a Jan-2024 Glassdoor candidate report, being "given access to transactions dataset in redshift and asked to create a logic based model to detect fraudulent transactions," with earlier candidates also asked to "classify some financial transactions" and write "a short report about anomalies you've found in the data." CyberArk gives, per a Glassdoor candidate, "a classic prediction homework assignment" followed by an interview that reviews the assignment and then presents "code snippets containing errors" to fix (e.g., "How random forest can deal with ordering data"). Beer-Sheva's Gav-Yam Negev cluster (CyberArk, Morphisec, Source Defense) over-indexes on fraud/cyber/anomaly classification.
9. **Differentiation (4):** Known-but-respected (a real Kaggle competition with 6,381 teams, not Titanic/Telco bootcamp-tier). Critically, the *typical* public IEEE-CIS project chases public-leaderboard AUC-ROC (repos brand themselves "(Top 12%) 711/6381"), uses random/stratified K-fold (which hides the temporal leak), never calibrates probabilities (AUC is rank-invariant so calibration is skipped), and never selects a cost-based operating threshold. One IEEE-CIS deep-dive states the problem plainly: "even if you include future information in ID aggregation, you won't notice the problem if you are validating with random K-Fold… a situation occurs where the CV score is good, but the Private Leaderboard score collapses significantly. This is not just bad luck; it is a fundamental design flaw." Out-of-time validation, isotonic calibration, and expected-cost thresholds are therefore genuine differentiators that appear almost exclusively in academic papers, not portfolio notebooks.

### Exact compliance pattern (IEEE-CIS raw-data redistribution)

- **Never commit raw data.** `.gitignore` the `data/raw/` directory and all `*.csv` from Kaggle.
- **Download-script-only.** Ship `scripts/download_data.sh` using the Kaggle CLI: `kaggle competitions download -c ieee-fraud-detection -p data/raw/ && unzip …`. README instructs the user to accept competition rules and place their `kaggle.json` token. Record a SHA-256 checksum of each file in `data/CHECKSUMS.txt` for reproducibility (no DVC needed — keep it $0 and simple).
- **What may be committed/deployed:** the trained LightGBM model artifact, the calibration model, feature-engineering code, aggregate metrics, SHAP plots, and *synthetic/fabricated example rows* for the demo. The deployed Hugging Face Space must NOT expose or allow reconstruction of raw Vesta records — it accepts user-entered or synthetic feature vectors only.
- **Runner-up trigger:** if the Kaggle competition data is delisted or access fails, switch to Home Credit Default Risk (identical pattern) or regenerate the Fraud-Detection-Handbook simulator (fully redistributable — commit the data directly).

---

## 0. Project Identity and Positioning

**Elevator pitch.** A production-shaped, take-home-format binary classification project that detects fraudulent e-commerce transactions on the real IEEE-CIS/Vesta dataset. It pairs a LightGBM main model with a logistic-regression interpretable baseline and a trivial baseline, validated out-of-time, calibrated with isotonic regression, and thresholded by explicit expected-cost minimization — then shipped as a containerized Gradio demo on Hugging Face Spaces backed by DagsHub-hosted MLflow. It is deliberately engineered to answer the exact questions Israeli DS interviews ask about imbalance, thresholds, calibration, and leakage.

**How it complements the flagship (does not compete).** The flagship DE-LU electricity-price capstone is *regression + probabilistic forecasting + uncertainty quantification* (LightGBM quantile ensemble, CQR conformal calibration, walk-forward CV, Diebold-Mariano). This project is its mirror image: *classification + class imbalance + decisioning under a cost matrix*. Together they demonstrate the full supervised-learning spectrum with one shared toolchain (LightGBM, MLflow/DagsHub, HF Spaces, Docker multi-stage, isotonic calibration, bootstrap CIs). The portfolio narrative becomes: "I can forecast a continuous quantity with calibrated uncertainty, AND I can build a calibrated, cost-optimal decision system for a rare-event classification problem — using the same disciplined engineering."

**Interview questions this arms him to answer (mapped fully in §13):** how to handle class imbalance; when ROC-AUC is misleading; how to choose a decision threshold; how to validate a fraud model; what target leakage is and how you found/fixed it; "your model outputs 0.9 — is that a probability?"; false-positive vs false-negative cost tradeoffs.

## 1. Problem Definition

**Prediction task.** Entity = a single e-commerce transaction (one row keyed by TransactionID). Label = `isFraud` ∈ {0,1}. Prediction time = the moment the transaction is submitted, before authorization. Features available at prediction time = all transaction-level fields (amount, product code, card/address/email attributes, device/identity signals) and any entity-level aggregates computed **only from strictly prior transactions** (this constraint is the crux of the leakage design in §4).

**Business framing and cost matrix.** This is card-not-present fraud, where two error types have asymmetric, quantifiable costs:
- **False negative (missed fraud):** the merchant/acquirer eats a chargeback. Direct processor chargeback fees run $20–$50 per dispute, but all-in merchant cost per chargeback averages roughly $110–$128 once operational handling, lost goods, and fees are included (ClearSale/Chargeflow 2026, citing Mastercard; Mastercard estimates the average dispute costs merchants at least $74). Model it as `Cost_FN ≈ TransactionAmt + $40` (goods loss + a conservative all-in fee/handling component).
- **False positive (legitimate transaction declined / "false decline"):** lost contribution margin on the order + customer-friction/lifetime-value damage. Model it as `Cost_FP ≈ 0.15 × TransactionAmt + $5`. False declines are Riskified's entire raison d'être; in aggregate the industry loses more to false declines than to fraud itself.

Because Cost_FN per event is larger but false positives are far more numerous at a 3.5% base rate, the optimum is NOT threshold 0.5 — it must be derived from an expected-cost curve (§6). This is the whole point of the project.

**Why binary classification with a decision threshold, not pure scoring.** A fraud system must ultimately *act* — accept, decline, or route to manual review. A pure ranking/score is insufficient; the business needs an operating point that balances chargeback loss against false-decline loss and against a bounded manual-review budget (alert rate). This forces the calibration-and-threshold discipline that distinguishes this project from leaderboard notebooks.

## 2. Data

**Source & size.** IEEE-CIS Fraud Detection (Vesta), Kaggle competition `ieee-fraud-detection`. Merged training set: 590,540 rows, of which 20,663 (3.5%) are fraudulent; each transaction has 431 features (400 numerical, 31 categorical) plus the relative timestamp and label (per the peer-reviewed characterization in arXiv:2211.06675). train_transaction ≈ 394 columns; train_identity = 41 columns (144,233 rows); merged ≈ 434 columns. Test set (unlabeled for the competition) transaction = 506,691 rows. On disk: the packaged download is 107.29 MB zipped (per IEEE DataPort's re-host listing); unzipped CSVs total roughly ~1.2 GB (inferred from reported pandas footprints).

**Schema overview.** `TransactionDT` (relative time), `TransactionAmt`, `ProductCD`, `card1–card6`, `addr1/addr2`, `P_emaildomain`, `R_emaildomain`, `C1–C14` (counting features), `D1–D15` (timedeltas, e.g., days since previous transaction), `M1–M9` (match flags), `V1–V339` (Vesta-engineered ranking/counting/entity features), and identity table `id_01–id_38`, `DeviceType`, `DeviceInfo`. Heavy, structured missingness (many V/id columns >50% NaN with shared NaN-structure groups).

**License & compliance pattern.** Kaggle competition rules (non-redistribution of raw data). Full pattern in the Executive Summary: `.gitignore` raw data, Kaggle-CLI download script, SHA-256 checksums, commit/deploy only derived model + synthetic demo rows.

**Reproducibility mechanics.** Plain bash download script + checksum file. No DVC (keeps it $0 and simple). A `make data` target wraps download → checksum verify → build features → freeze splits.

**Known data-quality issues (from the literature).**
- Extreme, structured missingness; many V-columns are redundant/collinear (Chris Deotte's public EDA groups V-columns by NaN structure and correlation — feature reduction is expected).
- Anonymized/masked feature semantics: only partial documentation, so judgment calls are required and should be documented.
- The public-leaderboard culture encourages test-set leakage exploits; this project explicitly refuses those (documented as a "what I did NOT do" note).

**Dataset-specific leakage traps + handling (this is the interview goldmine).**
- **UID-aggregation leakage:** top solutions build a synthetic client UID (card1 + addr1 + D1) and aggregate D/C/M/amount features by UID. If aggregates are computed over the entire dataset (including future rows), the model sees the future. *Handling:* compute all entity aggregates using only rows strictly earlier in TransactionDT (expanding-window / "past-only" aggregation), and recompute within each CV fold.
- **Random K-fold hides temporal leakage:** because the same leak appears in both train and validation folds under random K-fold, CV looks great while out-of-time performance collapses. *Handling:* time-based split (§3) is mandatory; adversarial validation as a check.
- **Target-encoding leakage:** naive target encoding uses each row's own label. *Handling:* out-of-fold cross-fitted target encoding + smoothing (§4).
- **D-features are relative time deltas**, not absolute — must not be used to reconstruct calendar position in a way that leaks the train/test boundary.

## 3. Validation Design

**Out-of-time split (temporal).** Sort by TransactionDT. Partition into four contiguous, non-overlapping periods:
- **Train** — earliest ~60% of the time span.
- **Validation** — next ~15% (early stopping, hyperparameter selection).
- **Calibration** — next ~10% (fit isotonic calibrator; must be disjoint from train and from test).
- **Test (out-of-time)** — final ~15%, held out until the very end for the single honest evaluation.

Exact boundaries proposal (by TransactionDT quantile): train = [0, 0.60), validation = [0.60, 0.75), calibration = [0.75, 0.85), test = [0.85, 1.0]. With ~590K rows at 3.5% fraud, the test period holds ≈88K rows and ≈3,000 positives — ample for stable PR-AUC and bootstrap CIs.

**Why random K-fold would be wrong.** Fraud is temporally non-stationary (concept drift, evolving attack patterns) and entity aggregates leak across time. Random K-fold both violates the i.i.d.-across-time assumption and masks aggregation leakage, producing optimistic CV that does not survive deployment.

**Relationship to the flagship.** This mirrors the flagship's walk-forward CV philosophy (train-on-past/test-on-future, strict temporal ordering) but differs in that fraud validation uses a single expanding out-of-time holdout with an explicit calibration slice rather than the flagship's three-regime rolling folds — because the classification project needs a dedicated, untouched calibration period for isotonic fitting (a subtlety the flagship handles via conformal calibration on rolling windows).

## 4. Feature Engineering

**Feature catalog plan.**
- **Raw pass-through:** TransactionAmt (+ log and cents-only decimal part), ProductCD, card fields, addr fields, email domains, C/D/M/V families, identity/device fields.
- **Entity-level aggregations (past-only):** UID = card1+addr1+D1; per-UID rolling mean/std/count of TransactionAmt, transaction velocity (time since previous UID transaction), per-UID historical fraud rate (strictly prior).
- **Temporal features:** hour-of-day and day proxies derived from TransactionDT deltas; time-since-last-transaction per UID/card/email.
- **Categorical encoding strategy:** LightGBM native categorical handling for low/medium cardinality; **out-of-fold cross-fitted target encoding with smoothing** for high-cardinality fields (card1, addr1, email domains). Target encoding done the right way: split training into folds, encode each fold using statistics from the *other* folds only, smooth small-category means toward the global mean, and encode test using full-train statistics — exactly the pattern sklearn's `TargetEncoder` implements during `fit_transform`. This is deliberately included because "what is target leakage and how do you do target encoding safely" is a frequent interview question.
- **Missingness as signal:** NaN-count-per-row and NaN-structure-group indicators (missingness is predictive in this dataset); LightGBM handles NaN natively so no imputation is forced.

**Anti-leakage checklist per feature family.**
- Aggregations: computed past-only, recomputed inside each CV fold. ✔
- Target encoding: out-of-fold, smoothed, test encoded from train only. ✔
- Temporal deltas: no feature may encode the absolute train/test boundary. ✔
- Identity joins: no post-transaction identity enrichment. ✔
- Every engineered feature carries a one-line docstring stating "available at prediction time: yes/why."

## 5. Model Hierarchy

- **(a) Trivial baseline:** majority-class predictor (always "not fraud") and a simple amount-threshold rule. Framed with the cost matrix so the "96.5% accuracy but catches zero fraud" fallacy is made explicit — the accuracy-paradox teaching moment.
- **(b) Logistic regression** on a small, interpretable, standardized feature set (amount, a few C/D features, a handful of target-encoded categoricals), with L2 regularization and feature scaling. Serves as the transparent, coefficient-interpretable reference.
- **(c) Main model: LightGBM** with native categorical + NaN handling, early stopping on the validation period, modest depth, PR-AUC/AUC as the eval metric.
- **(d) Explicitly OUT of scope:** deep learning (no benefit on tabular fraud at this scale, heavier compute), stacking/blending ensembles (leaderboard-chasing, not decision-quality), AutoML (obscures the reasoning the interview probes). One line each in the README.

**Class-imbalance handling — defended position.** *Do not use SMOTE.* Train LightGBM on the natural class distribution, relying on ranking quality, and treat imbalance as a threshold-and-calibration problem, not a resampling problem. Rationale, grounded in current literature:
- Yotam Elor (Amazon) & Hadar Averbuch-Elor (Cornell), "To SMOTE, or not to SMOTE?" (arXiv:2201.08528, 2022): "Our results support the known utility of balancing for weak classifiers. However, we find that balancing does not improve prediction performance for the strong ones." Where oversampling helps at all, plain random oversampling ≈ SMOTE, so SMOTE adds complexity for nothing.
- Dal Pozzolo, Caelen, Johnson & Bontempi, "Calibrating Probability with Undersampling for Unbalanced Classification" (IEEE SSCI 2015) proves that resampling/reweighting **distorts posterior probabilities** and requires an explicit prior-correction/recalibration step. Recent work (IJCT 2024) extends the same posterior-bias finding to SMOTE oversampling — one experiment saw false alarms increase 165× while ROC-AUC barely moved.

**The defended plan:** (1) primary LightGBM trained on natural distribution; (2) an ablation run with `scale_pos_weight` tuned, reported side-by-side; (3) because any reweighting distorts probabilities, isotonic recalibration (§6) is applied *after* training and its necessity is demonstrated by a before/after reliability diagram. This "reweighting distorts probabilities → recalibrate" chain is itself a high-signal interview narrative and connects to the flagship's isotonic experience.

## 6. Evaluation Protocol

**Primary metric: PR-AUC (Average Precision).** At 3.5% positives, ROC-AUC is inflated and insensitive to changes in false positives because true negatives dominate; PR-AUC anchors to the positive class and reflects deployment characteristics (alert rate, analyst workload). This follows Takaya Saito & Marc Rehmsmeier, "The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets" (PLoS ONE 10(3):e0118432, 2015; DOI 10.1371/journal.pone.0118432). **Position noted honestly:** McDermott et al., "A Closer Look at AUROC and AUPRC under Class Imbalance" (NeurIPS 2024 / arXiv:2401.06091) push back — "AUPRC, contrary to popular belief, is not superior in cases of class imbalance and might even be a harmful metric… it can unduly favor model improvements in subpopulations with more frequent positive labels" (with a companion *Cell Patterns* 2024 paper arguing ROC-AUC "accurately assesses imbalanced datasets"). Therefore ROC-AUC is reported as a secondary metric and the disagreement is acknowledged — but PR-AUC remains primary given the operational cost focus, since the deployment decision is precision/recall/alert-rate driven.

**Secondary metrics:** ROC-AUC, Brier score, log-loss, and operating-point precision/recall/F1 at the chosen threshold.

**Calibration assessment.** Reliability diagram + Brier score; compare uncalibrated vs isotonic vs Platt. Position: **isotonic regression** is preferred here (large calibration slice, tree-model sigmoidal distortion), consistent with Niculescu-Mizil & Caruana (2005) that isotonic beats Platt when sufficient calibration data is available — and it directly reuses the flagship's isotonic-calibration experience. Platt reported as a comparison.

**Threshold selection.** Build the expected-cost curve over candidate thresholds using the §1 cost matrix: `E[cost](t) = Σ (FN(t)·Cost_FN + FP(t)·Cost_FP)`; pick `t*` minimizing expected cost, and also report the threshold that respects a fixed manual-review budget (alert rate). Show the cost curve as a headline figure. This step is only meaningful *after* calibration — cost-sensitive thresholding requires well-calibrated probabilities, which is why §5→§6 ordering matters.

**Statistical honesty.** Bootstrap confidence intervals (stratified, ~2,000 resamples) on the headline PR-AUC and on the ΔPR-AUC between LightGBM and each baseline — this connects to Yarden's Month-1 bootstrap block. For ROC-AUC comparisons, use the DeLong test (fast and exact for large n via the Sun–Xu 2014 algorithm; with ~88K test rows it is well within its valid regime). **Which applies where:** PR-AUC has no closed-form variance, so use the paired stratified bootstrap on ΔPR-AUC (primary); DeLong on ΔROC-AUC as a secondary cross-check (keep bootstrap stratified given the imbalance, to avoid folds/resamples with zero positives). A difference is claimed "real" only if the bootstrap CI on the difference excludes zero.

**Slice analysis (fairness/robustness).** Report PR-AUC and operating-point precision/recall by ProductCD, by device type, by transaction-amount bucket, and across the test-period timeline (drift check). This is the "does it work for everyone / does it degrade over time" story.

## 7. Explainability

- **Global SHAP:** beeswarm summary + dependence plots on the top features (expect TransactionAmt, card/UID aggregates, C-features, email domain, device signals).
- **Local explanations:** a **false-positive post-mortem** (a legitimate transaction the model flagged — why, and what feature drove it) and a **true-positive case study** (a caught fraud), each with a SHAP waterfall.
- **Permutation-importance cross-check** against SHAP global ranking (agreement/disagreement discussion).
- **Communication artifact:** a one-page "What I'd tell the fraud-ops team" — top drivers, the chosen operating point and its expected cost/alert rate, and the two failure modes to watch. Mirrors the flagship's stakeholder-communication discipline.

## 8. Experiment Tracking and Registry

**MLflow on DagsHub** (consistent with the flagship; $0 tier). What gets logged per run: params (features on/off, LightGBM hyperparameters, threshold policy), metrics per split (train/val/calibration/test PR-AUC, ROC-AUC, Brier, operating-point precision/recall, expected cost), calibration artifacts (reliability diagrams, before/after), SHAP plots, and the cost curve. **Experiment naming:** `fraud-ieee/{baseline|logreg|lgbm|calibration|threshold}-{yymmdd}-{shortdesc}`. **Registry stages:** `Staging` for candidate models, `Production` for the demo-backing model; log the calibrator as a companion artifact. **Minimum bar:** ≥ 8 tracked runs (flagship requires ≥5; set higher here to cover trivial + logistic + several LightGBM variants + the scale_pos_weight ablation + calibration comparison + threshold policies).

## 9. Demo / Deployment

**Recommendation: Gradio** (not marimo) for this classification demo. Justification: the flagship's marimo showcase suits a reactive analytical notebook, but a fraud demo's core interaction is *single-prediction + live threshold/cost manipulation*, which Gradio's input-widget + slider + output-panel model expresses more naturally and with less code. Take the position: Gradio for interactive single-decision demos; marimo for exploratory dashboards.

**What the demo shows:** (1) score a transaction (user-entered or synthetic feature vector — never a raw Vesta record); (2) SHAP waterfall for that decision; (3) a **threshold slider** with live precision/recall/alert-rate readout; (4) a **cost calculator** that recomputes expected cost as the user varies the threshold and the FN/FP cost inputs. This makes the entire §6 story tangible to an interviewer.

**Reuse:** Docker multi-stage build (same pattern as the flagship), deployed to Hugging Face Spaces, $0 run rate.

**Explicitly NOT deployed:** no real-time retraining, no raw data, no PII, no ability to reconstruct Vesta records — synthetic/example inputs only.

## 10. Repo Structure

```
fraud-ieee-cis/
├── README.md                # narrative-driven; the story arc below
├── Makefile                 # data, features, train, evaluate, app targets
├── pyproject.toml           # ruff + pytest config, pinned deps
├── Dockerfile               # multi-stage (build → slim runtime)
├── scripts/
│   └── download_data.sh      # Kaggle CLI + unzip + checksum verify
├── data/
│   ├── raw/                  # .gitignored
│   └── CHECKSUMS.txt
├── src/fraud/
│   ├── data.py               # load, merge, memory-reduce (downcast)
│   ├── splits.py             # time-based train/val/calib/test
│   ├── features.py           # past-only aggregations, OOF target encoding
│   ├── model.py              # logistic + lightgbm
│   ├── calibrate.py          # isotonic/Platt
│   ├── threshold.py          # expected-cost curve, operating point
│   ├── evaluate.py           # PR-AUC, ROC-AUC, bootstrap, DeLong, slices
│   └── explain.py            # SHAP, permutation importance
├── app/                      # Gradio demo
├── tests/                    # pytest for leakage-critical + feature fns
└── notebooks/                # quarantined EDA only
```

**Code-quality bar:** type hints throughout; `ruff` clean; `pytest` covering the leakage-critical functions (past-only aggregation, OOF target encoding, split disjointness) and the cost/threshold math. **README arc:** problem & cost framing → data & compliance → the leakage story → validation design → baselines → LightGBM → calibration → cost-based threshold → SHAP → demo → "five hardest questions."

## 11. Milestones M0–M5 with Checkpoints

Assume ~10–15 focused hours/week alongside the main program. **Completeness over speed** — hours are estimates, not constraints.

**M0 — Repo + data + EDA (~15h). CP-1:** repo scaffolded with src layout, ruff/pytest wired; download script + checksums working; memory-reduction load verified (<1 GB RAM after downcast); time-based splits frozen and serialized; **leakage audit documented** (UID aggregation, random-K-fold trap, target-encoding, D-features) in `docs/leakage.md`; confirm exact per-CSV file sizes from the Kaggle data page.

**M1 — Baselines (~12h). CP-2:** trivial baseline (majority + amount rule) and logistic-regression baseline trained; honest out-of-time PR-AUC/ROC-AUC reported with bootstrap CIs; MLflow runs logged.

**M2 — LightGBM + imbalance handling (~18h). CP-3:** LightGBM beats both baselines on out-of-time PR-AUC with **statistical honesty** — the comparison test is the paired stratified bootstrap CI on ΔPR-AUC (must exclude zero), cross-checked with DeLong on ΔROC-AUC; scale_pos_weight ablation logged.

**M3 — Calibration + threshold + cost (~15h). CP-4:** isotonic calibrator fit on the calibration slice; before/after reliability diagrams + Brier scores committed; expected-cost curve computed; operating point `t*` chosen and its precision/recall/alert-rate reported.

**M4 — SHAP + slice analysis + demo (~20h). CP-5:** SHAP global + local (FP post-mortem, TP case study) and permutation cross-check committed; slice analysis across ProductCD/device/amount/time; **Gradio demo live on HF Spaces** (threshold slider + cost calculator + SHAP waterfall).

**M5 — Polish + README + interview one-pager (~12h).** README narrative complete; "walk me through your project" script written; the **five hardest interview questions with answers** documented (imbalance strategy defense; why PR-AUC; why out-of-time; the leakage you found; "is 0.9 a probability?").

Total ≈ 92 hours ≈ 7–9 weeks at 10–15 h/week.

## 12. Risk Register

| ID | Risk | Likelihood | Impact | Mitigation | Trigger condition |
|---|---|---|---|---|---|
| R-1 | Kaggle dataset delisted / access fails | Low | High | Runner-up (Home Credit) pre-vetted with identical compliance pattern; Fraud-Handbook simulator (GPL v3 code / CC BY-SA 4.0) as fully-redistributable escape hatch | Download script 404s or rules gate changes |
| R-2 | Evaluation instability from imbalance | Low–Med | Med | 3,000+ positives in test period; stratified bootstrap CIs; report CI widths | Bootstrap CI on PR-AUC wider than ~±0.05 |
| R-3 | Leakage discovered late | Med | High | Leakage audit at M0; per-feature-family anti-leakage checklist; pytest on aggregation/encoding functions; adversarial-validation check | Out-of-time PR-AUC ≫ CV PR-AUC gap, or a feature dominates implausibly |
| R-4 | Demo hosting friction | Low | Low–Med | Reuse the flagship's proven HF Spaces + Docker multi-stage pattern; synthetic inputs only | Space build fails or exceeds free-tier limits |
| R-5 | Memory blow-up on M3/16 GB | Low | Med | Downcast dtypes (proven ~50–70% reduction); LightGBM native categoricals (no one-hot); chunked feature building | pandas load exceeds ~4 GB RAM |

## 13. Interview-Surface Map

| Project component | Interview question it arms |
|---|---|
| Natural-distribution training + scale_pos_weight ablation, no SMOTE | "How do you handle class imbalance?" / "When would you use SMOTE?" |
| Expected-cost curve + operating point | "How do you choose a decision threshold?" |
| PR-AUC primary, ROC-AUC secondary | "When is ROC-AUC misleading?" |
| Time-based train/val/calib/test split | "How would you validate a fraud model?" |
| Out-of-fold smoothed target encoding | "What is target leakage?" / "How do you encode high-cardinality categoricals?" |
| Isotonic recalibration + reliability diagram | "Your model outputs 0.9 — is that a probability?" |
| Cost matrix (FN vs FP) | "What's the cost of a false positive vs a false negative here?" |
| UID-aggregation leakage post-mortem | "Tell me about a bug/leak you found and fixed." |
| Bootstrap CI on ΔPR-AUC / DeLong | "How do you know model A is really better than model B?" |
| Slice analysis | "How do you check for robustness / fairness / drift?" |
| SHAP local + global | "How would you explain a decision to a non-technical stakeholder?" |

## Caveats

- Exact per-CSV on-disk byte sizes could not be confirmed from a primary source; the hard number is the 107.29 MB zipped download on IEEE DataPort, with ~1.2 GB unzipped inferred from reported pandas footprints. Confirm from the Kaggle data page at M0.
- Training-time and memory figures vary with fold count, feature count, and hyperparameters; ~5 min per single CPU fit is the most directly comparable reported figure, and the ~540–650 MB post-downcast footprint is a documented community result, not a guarantee for every feature build.
- Column/feature counts appear as 393/394/431/434 across sources depending on whether TransactionID/isFraud and pre/post-merge are counted — all refer to the same dataset (canonical: 590,540 rows, 20,663 frauds, 3.5%).
- The cost numbers ($40 all-in FN component, 15%+$5 FP) are plausible, defensible modeling assumptions calibrated to industry chargeback-cost figures (Mastercard/ClearSale ~$110 all-in per chargeback), not dataset-provided ground truth; they should be presented in interviews as an explicit, adjustable business assumption, and the demo's cost calculator lets the interviewer vary them live.
- The PR-AUC-vs-ROC-AUC literature is not unanimous (NeurIPS 2024 pushback noted); the plan takes PR-AUC as primary but reports both and can defend either position.
- The Riskified and CyberArk take-home descriptions are drawn from candidate self-reports on Glassdoor (2020–2024), not official company documentation; they are consistent across multiple independent reports but should be treated as directional evidence of format, not a guarantee of the current process.