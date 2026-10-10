# DDNN-2: research directions for a second distributional neural network attempt (CP-24 input)

Status: COMPLETE (sections 1-6). Written progressively; finished 2026-10-05.
Author role: independent research analyst (read-only on the repository; no training, no data download).
Date: 2026-10-04.

Scope: day-ahead DE-LU hourly price, seven quantiles plus p50, issued D-1 11:00 UTC; five fixed development
folds (10,747 h, 2020-2026); S_MAE and S_WIS as ratios to B0; same-information rule; NumPy-only DDNN.

Sections (planned):
1. Literature notes
2. Diagnosis of CP-23's DDNN
3. Ranked directions for DDNN-2
4. Recommended role, candidate definition and adoption rule
5. Pitfalls
6. References

Reading log (for independence and audit): I read `reports/distribution-challenger/{report.md, selection.json,
diagnostics/*.csv}`, `src/cp23/{ddnn.py, features.py}`, the row-split and refit logic of `src/cp21/lgbm.py`, the
level/scale definitions in `src/cp15/data.py`, and computed descriptive statistics (no fitting) from
`reports/distribution-challenger/{predictions,members}.parquet`. I deliberately did not read `progress.md`, the
Orchestrator files, or `.local/artifacts/cp-24/orchestrator-state.md`, so that this view is formed independently.
All numbers marked "descriptive" below are computed on the five development folds; they explain CP-23 and choose
nothing for DDNN-2.

---

## 1. Literature notes

### 1.1 Marcjasz, Narajewski, Weron, Ziel (2023): distributional neural networks (DDNN)
Energy Economics 125, 106843 (arXiv:2207.02832). What they actually did (from the paper, Sections 3-5):
- **Data and protocol.** German day-ahead prices 2015-2020; 554 out-of-sample test days; models **re-trained every
  day** on a rolling window; hyperparameters tuned **once**, before the test period, on the first four years
  (1,092 training days + the last 364 days as validation).
- **Representation.** One network for the whole day: inputs are the **full 24-hour vectors** of prices for
  T-1, T-2, T-3 and T-7, load forecasts for T, T-1, T-7, renewable (RES) forecasts for T and T-1, EUA, coal, gas
  and oil closes at T-2, and day-of-week dummies. The output layer emits **24 distributions** (2 or 4 parameters
  each). Two hidden layers.
- **Hyperparameter optimisation (HPO).** Optuna (TPE), **four independent runs of 2,048 trials each**. Search
  space: 14 binary input-group inclusion flags; dropout after the input layer (on/off and rate); neurons per hidden
  layer in [16, 1024]; activation per layer from {elu, relu, sigmoid, softmax, softplus, tanh}; L1 on hidden
  layers (on/off, rate 1e-5..10, log-scale); L1 separately on each distribution parameter's output; Adam learning
  rate 1e-5..1e-1 (log). Validation is "hybrid batch-rolling": **13 recalibrations on successive 28-day batches**
  across the 364-day validation year (not one fixed holdout).
- **Fixed training recipe (not tuned):** input normalisation, NLL loss, Adam, **early stopping with patience 50,
  batch size 32, up to 1,500 epochs**; in the rolling test "the dataframe was shuffled and 20% left out for
  validation" (a random, not a most-recent, early-stopping set).
- **Ensembling.** Four members = the four HPO runs' different architectures (not four seeds of one architecture).
  Probability (vertical) averaging "pEns" vs quantile (horizontal) averaging "qEns".
- **Results (Table 1, CRPS approximated by the mean pinball over 99 percentiles; MAE):** LEAR-QRA 1.575,
  DNN-QRA 1.399, DDNN-N-qEns 1.348, DDNN-JSU-pEns 1.304, DDNN-JSU-qEns **1.299**; MAE LEAR-Ens 4.372, DNN-Ens 3.610,
  DDNN-JSU-pEns 3.542, DDNN-JSU-qEns 3.564. JSU beats Normal by about 3-4% CRPS. **Single HPO runs differ by up to
  10% out-of-sample although they were within 2% in-sample**; the ensemble of runs is what is reliably good.
  Dropout and L1 were "almost never chosen"; selected layers were wide (hundreds of units); the most-selected inputs
  were prices of T-1 and T-2, the load and RES forecasts for T, RES for T-1, and the **gas price**.
- **Relevance here.** (i) The published DDNN gain came with full-day price vectors and fuel/EUA inputs; gas and EUA
  are excluded by this programme's same-information rule, so the published gain is an upper bound. (ii) The LEAR they
  beat was weak on their sample (MAE 4.37 vs 3.61 for DNN-Ens); here the LEAR family (HG) is the strongest member,
  especially in the 2022 crisis. (iii) Their reliability came from ensembling *different* tuned architectures and
  from long, multi-window validation.

### 1.2 Lago, Marcjasz, De Schutter, Weron (2021): open-access EPF benchmark and its DNN (epftoolbox)
Applied Energy 293, 116983 (arXiv:2008.08004; erratum 2021 for DE LEAR metrics).
- **DNN:** feed-forward, two hidden layers, **multivariate framework (one model with 24 outputs)**, Adam. Inputs and
  hyperparameters chosen jointly by TPE (1,500 iterations; "performance barely improves after 1000"). Feature choice
  uses 11 binary flags over 241 candidate inputs, each flag switching a **whole-day vector** (prices of d-1, d-2,
  d-3, d-7; the two exogenous day-ahead forecasts for d, d-1, d-7; day of week). Eight further hyperparameters:
  neurons per layer, activation, dropout, learning rate, batch normalisation, **data preprocessing/scaling technique**
  (the open-source scaler offers several options including an asinh-based "invariant" transform), weight
  initialisation, and an L1 coefficient on every layer's kernel.
- **Validation.** HPO uses the last 42 weeks of the four tuning years. In the daily-recalibrated test, **early
  stopping uses 42 weeks selected at random out of 208**, explicitly "to ensure that the dataset used for optimizing
  the DNN parameters includes up-to-date data"; footnote 11 warns that training without the most recent weeks
  "should be avoided during testing to ensure that the DNN captures new market effects".
- **Ensembles.** DNN-Ens = mean of four DNNs from four independent HPO runs; LEAR-Ens = mean over calibration windows
  of 56, 84, 1,092 and 1,456 days. DNN ensembles were usually better than LEAR, but the LEAR was competitive and far
  cheaper. The paper also fixes best practices (long test periods, DM/GW tests, no test-data contamination).

### 1.3 Variance-stabilising transformations (VST)
Uniejewski, Weron, Ziel (2018), "Variance stabilizing transformations for electricity spot price forecasting",
IEEE Trans. Power Systems 33(2), 2219-2229. Prices are first standardised with the calibration window's **median
and MAD**, then transformed (asinh, Box-Cox variants, mirror-log, logistic, probability-integral transforms, ...);
across 12 markets asinh and the normal-PIT were the most reliable, and **asinh is the recommended default** (simple,
defined for negative prices, compresses spikes, approximately linear near zero). Quantiles are equivariant under any
monotone transform, so a predictive distribution fitted in asinh space back-transforms **exactly** at every
quantile level (the median of the transform is the transform of the median). Related: the seasonal-component
idea for NNs (Marcjasz, Uniejewski, Weron 2019, IJF 35(4), 1520-1532) - modelling the price after removing a
long-term level is more accurate than modelling raw prices.

### 1.4 Probabilistic combination: probability vs quantile averaging, QRA and successors
- Lichtendahl, Grushka-Cockayne, Winkler (2013), "Is it better to average probabilities or quantiles?", Management
  Science 59(7), 1594-1611: quantile averaging (Vincentisation) keeps a common location-scale shape and is sharper;
  the linear pool (probability averaging) adds the members' disagreement to the spread. Ranjan and Gneiting (2010,
  JRSS-B 72(1), 71-91) and Gneiting and Ranjan (2013, EJS 7, 1747-1782): a linear pool of *calibrated* members is
  necessarily over-dispersed; it can help when members are *under-dispersed*. Both are means, hence **not robust to
  one member's blow-up**; a median or trimmed mean of member quantiles is the robust variant.
- In EPF, Marcjasz et al. (2023) found qEns and pEns close (CRPS 1.299 vs 1.304), with qEns better in coverage tests.
- QRA: Nowotarski and Weron (2015), Computational Statistics 30(3), 791-803 (quantile regression on member point
  forecasts); LASSO-regularised QRA: Uniejewski and Weron (2021), Energy Economics 95, 105121; point-vs-probabilistic
  combination of NN ensembles: Marcjasz, Uniejewski, Weron (2020), IJF 36(2), 466-479.
- **Postprocessing beats standalone DDNN on long crisis-inclusive tests:** Lipiecki, Uniejewski, Weron (2024),
  "Postprocessing of point predictions for probabilistic forecasting of day-ahead electricity prices: the benefits of
  using isotonic distributional regression", Energy Economics (arXiv:2404.02270): QRA, conformal prediction and IDR
  applied to point forecasts and then combined **outperform DDNN** over two 4.5-year test periods (DE, ES) including
  COVID and 2022; diversity among postprocessors drives the gain. v4's empirical residual layer belongs to this family,
  which is a strong prior that a DDNN will not beat v4 *as an interval method alone*.
- Learned, quantile-specific combination weights: Berrisch and Ziel (2023), "CRPS learning", J. Econometrics 237(2),
  105221 (online, smoothed per-quantile weights; a natural tool for a later learned-weight recombination stage).
- Conformal methods in EPF: Kath and Ziel (2021), IJF 37(2), 777-799; adaptive conformal/online aggregation through
  the 2020-2022 turbulence: Dutot, Zaffran, Feron, Goude (2024), arXiv:2405.15359.

### 1.5 Hyperparameter optimisation practice in EPF
- TPE (Bergstra, Bardenet, Bengio, Kegl 2011, NeurIPS) via hyperopt/Optuna (Akiba et al. 2019, KDD); random search
  is a strong baseline in low effective dimension (Bergstra and Bengio 2012, JMLR 13, 281-305).
- Practice in the two reference papers: HPO **once, before the test period**, on **long validation** (42 weeks; or
  13 rolling 28-day batches over 364 days), with hundreds to thousands of trials, **repeated** (four runs) because
  winners are unstable, and the winners **ensembled** rather than one winner trusted.
- Marcjasz (2020), "Forecasting electricity prices using deep neural networks: a robust hyper-parameter selection
  scheme", Energies 13(18), 4605: grid search evaluated on **long samples** to suppress the noise of local
  optimisation, combined with forecast averaging, gave stable performance over three-year test periods.
- Calibration windows: averaging forecasts across short and long windows beats the best single window
  (Hubicka, Marcjasz, Weron 2019, IEEE Trans. Sustainable Energy 10(1), 321-323; Marcjasz, Serafin, Weron 2018,
  Energies 11(9), 2364) - relevant to adaptivity in regime shifts such as 2022.

### 1.6 Other relevant recent work (brief)
- Olivares, Challu, Marcjasz, Weron, Dubrawski (2023), NBEATSx, IJF 39(2), 884-900: structured deep models on the
  epftoolbox data; out of scope for a NumPy-only DDNN but confirms the value of day-level multi-output designs.
- Barunik and Hanus (2023/2025), "Learning the probability distributions of day-ahead electricity prices",
  arXiv:2310.02867: multi-output nonparametric distribution network on German prices (monotonicity penalty).
- Jedrzejewski, Lago, Marcjasz, Weron (2022), "Electricity price forecasting: the dawn of machine learning", IEEE
  Power and Energy Magazine 20(3), 24-31: overview; LEAR and DNN ensembles as the reference pair.

---

## 2. Diagnosis: why CP-23's DDNN underperformed

### 2.0 Decomposition that frames the diagnosis (descriptive)
Central-forecast MAE per fold (EUR/MWh) from `members.parquet` (L = mean of L-N and L-R):

| Fold | D (DDNN) | L (LightGBM, same information as D) | HG (LEAR blend) | D - L | L - HG |
|---|---|---|---|---|---|
| fold_1 | 5.69 | 4.82 | 5.18 | +0.87 | -0.36 |
| fold_2 | 9.08 | 7.72 | 8.47 | +1.36 | -0.75 |
| fold_3 | 58.84 | 52.16 | 46.72 | +6.68 | +5.44 |
| fold_4 | 16.13 | 13.79 | 14.62 | +2.34 | -0.83 |
| fold_5 | 17.10 | 15.64 | 15.45 | +1.46 | +0.19 |

Two separable gaps follow. **D - L** compares two learners on *identical information*: it measures estimation
(training recipe, staleness, loss), and it is positive in every fold. **L - HG** compares per-hour same-hour-lag
features against LEAR's full-day design: it is negative (L better) outside the crisis and strongly positive in fold 3.
Pooled, D - HG = 3.24 EUR/MWh, of which D - L = 2.52 and L - HG = 0.72.

### 2.1 Estimation recipe: the network was barely trained, and trained on stale data (confidence: high)
- **Evidence.** Median best epoch 3-8 by configuration (C4: 3; p90 7-24) with ~28-33 epochs run, i.e. the
  inner-validation NLL bottomed out after roughly 200-500 Adam steps and never improved for 25 epochs
  (`diagnostics/epochs.csv`). The D - L gap is roughly **uniform across local hours** (+2 to +3 EUR/MWh at most hours;
  descriptive), which points to estimation, not to any hour-specific information. Seed instability is large: member
  medians spread 6.9 EUR/MWh around the ensemble median and single-seed MAEs are 21.8-22.9 vs 21.2 for the ensemble
  (`seed-stability.csv`).
- **Mechanisms, in order of my confidence.**
  1. *Early stopping on NLL over the last 28 days.* As the network sharpens its training fit, the NLL of a block that
     sits after the training rows (a different regime more often than not) rises because of scale/shape misfit long
     before the location stops improving. NLL is a tail-sensitive criterion on a 672-row, strongly autocorrelated block
     (effectively about four independent weeks), so it stops early and noisily.
  2. *Staleness.* `src/cp23/features.py` trains the kept member on `[max(2019-01-01, D-728), D-28)` and never refits on
     the last 28 days, whereas `src/cp21/lgbm.py` chooses its configuration on the same split and then **refits the
     winner on the whole window**. The DDNN is therefore four weeks staler than its LightGBM twin at every origin.
     Lago et al. (2021, footnote 11) warn precisely against this in testing. A crude descriptive proxy (terciles of the
     28-day level shift) did not show a monotone effect, so the size of this component is unconfirmed; the handicap is
     certain and has no offsetting benefit.
  3. *Loss misalignment for the point forecast.* LightGBM uses the quantile objective at 0.5 (median regression, i.e.
     MAE-optimal); the DDNN's p50 is a by-product of an NLL fit whose capacity also goes to scale and tails.
     Gebetsberger et al. (2018) show maximum likelihood is less robust than minimum-CRPS estimation under
     misspecification and outliers - the situation here.
  4. *Untuned optimisation.* lr 1e-3, batch 256, L2 1e-4, no dropout, no input selection; the literature recipe is
     batch 32, patience 50, up to 1,500 epochs, tuned lr/regularisation (Marcjasz et al. 2023).

### 2.2 Representation: per-hour rows with same-hour lags duplicate LightGBM and miss cross-hour information (confidence: high)
- **Evidence.** D - HG MAE by local hour (descriptive): hour 0 +8.9, 1 +7.4, 2 +6.3, 3 +4.9 ... 16 +0.1, 17 +0.5
  EUR/MWh. LightGBM, fed the same 23 per-hour features, shows the **same night-hour signature** against HG
  (hour 0 +6.5, 1 +4.7, 2 +3.3) and is *better* than HG from 14 to 21 h - so the night deficit belongs to the
  representation, not to the network. The night hours of D are best predicted from the late evening of D-1, which LEAR
  sees (its design has the full 24-hour vectors of D-1, D-2, D-3, D-7; `lear[:, :96]` in `src/cp15/data.py`) and the
  per-hour design does not (its nearest price is the same hour of D-1, ~24 h old). Monday and Sunday gaps are also the
  largest (+4.3 and +5.3), consistent with missing day-profile context.
- **Consequence for the combination.** Error correlation with L is 0.83 vs 0.71 with HG: CP-23's DDNN was a noisier
  LightGBM, and v4 already contains LightGBM, so even a well-trained version of the same representation would add little.
- **Literature.** Both reference DNNs are *day-level, multi-output* networks on whole-day vectors (Lago et al. 2021;
  Marcjasz et al. 2023).

### 2.3 Role design: the distribution was discarded and the point forecast over-weighted (confidence: high)
- In v5 only the DDNN's median entered, at a fixed weight 1/3 (so v5's central = 4/9 HG + 2/9 L + 1/3 D: the weakest
  member received more weight than LightGBM). Its distributional output was replaced by the residual layer.
- The DDNN's relative deficit is smaller on WIS than on MAE (S_WIS +7.2% vs S_MAE +11.7% against v3), i.e. its
  distributional part was relatively better than its centre - the part CP-23 used.
- Forecast-combination theory (Bates and Granger 1969; Timmermann 2006) gives a small optimal weight to a member that
  is both less accurate and highly correlated with the incumbent; the hindsight optimum 0.05-0.10 is exactly that.

### 2.4 Robustness: unbounded tails and a non-robust ensemble average (confidence: high that it is a defect; low-medium that it explains the bulk)
- Descriptive extremes of D: 2021-04-05 (Easter Monday, negative prices) central -970 vs actual -45 EUR/MWh with
  p2.5 = -19,619; 2026-01-20 17:00 UTC central 584 vs actual 194 with p97.5 = 38,488. 13 hours have |z| > 6 for D's
  centre in the normalised scale, none for HG.
- Mechanism: the JSU quantile `xi + lambda*sinh((z - gamma)/delta)` with delta floored at 0.05 can produce
  astronomically wide tails and medians; quantile *averaging* across four seeds is a mean, so one member's blow-up
  passes straight into the ensemble (and one third of it into v5's central forecast); inputs are not winsorised and
  ELU extrapolates linearly; the target scale is a non-robust 168-h SD.
- Size: D's top 1% of hours carries 9.4% of its absolute error, the same share as HG (9.4%) and L (8.9%); removing
  D's worst 1% of hours barely changes the D - HG gap except in fold 2, where it flips (+0.61 to -0.42). So blow-ups
  are not the main accuracy story, but they are unacceptable in a product member and they hurt fold 2.

### 2.5 Configuration choice was noise, and the "ensemble" had no architectural diversity (confidence: high on noise, medium on impact)
- One 28-day holdout per fold; winner margins 0.03% (fold 4), 0.11% (fold 5), 0.61% (fold 1); the chosen configuration
  changed from fold to fold (C2, C4, C2, C3, C4). Fold 3's choice was made on April-May 2022 (holdout MAE 15.5) for a
  period that realised 58.8. Four configurations differing only in width (2.4k-26k parameters) is not a search over
  the hyperparameters that matter (lr, regularisation, dropout, inputs).
- Marcjasz et al. (2023): tuned sets that were within 2% in-sample differed by up to 10% out-of-sample; ensembles across
  *different tuned sets* are what is reliable. CP-23's ensemble was four seeds of one set.

### 2.6 Own-distribution miscalibration (confidence: medium-high)
- Central intervals too narrow (coverage 50% 0.441, 80% 0.743) while 95% is near nominal (0.925) and the mean 95% width
  exceeds v4's: too peaked in the middle, too wide in the tails (PIT outer bins 7.2% and 7.0%, interior bins 4.1-4.5%).
- Consistent with (a) in-sample residual scale learned on stale data being smaller than out-of-sample error (2.1),
  (b) quantile averaging, which does not add between-member disagreement to the spread (Lichtendahl et al. 2013).

### 2.7 Crisis (fold 3) (confidence: medium)
- Both nonlinear learners lose to LEAR in fold 3 (L by 5.4, D by 12.1 EUR/MWh). Example: 2022-08-28 (Sunday, level
  580.6, scale 135.8): actual 13.3 at 12:00 UTC (z = -4.18) vs D 317 (z = -1.94) - the depth of solar/weekend dips in
  z-units was underestimated; the weekday/solar structure in z-space is not stationary when volatility jumps.
- The same-information rule excludes gas and EUA, which Marcjasz et al. found among the most-selected inputs; every
  member suffers this, but it removes much of the published DDNN advantage precisely in 2022.

### 2.8 What I do not blame
- The Johnson SU family (literature: JSU beats Normal by 3-4% CRPS); the NumPy implementation (26/26 PyTorch reference
  checks, gradient checks); leakage (61 controls passed). The failure is in design choices, not in code correctness.

**Top three, ranked:** (1) estimation recipe and staleness (2.1); (2) a representation that duplicates LightGBM and
lacks cross-hour information (2.2); (3) role and robustness - a fixed 1/3 point weight for the weakest member, with a
non-robust ensemble average and unbounded tails (2.3, 2.4).

---

## 3. Ranked directions for DDNN-2

Ranking is by expected contribution to the programme's goal (a member that improves v4), weighed by the strength of
the evidence. Directions 1 and 4 are cheap hygiene that every DDNN-2 variant should carry; 2 and 3 are the substantive
bets; 5 is an option inside the search space; 6 is a different use of the same network. Compute estimates assume the
M3, NumPy with one BLAS thread per worker, 4 workers, 636 origins, and CP-23's measured costs (C4 on ~16k per-hour
rows: about 0.1 s per epoch; C2 about 0.03 s per epoch).

### Direction 1 - Train it properly, on recent data, for the score (rank 1)
- **Mechanism.** (a) Every final member must train on data up to D-1: either *refit-to-epoch* (find the stopping epoch
  E* on an inner split, then refit on the full window `[max(2019-01-01, D-728), D)` for E* epochs) or *random-week
  early stopping* (each member holds out its own random 20% of whole calendar weeks, never the most recent 7 days, as
  in Lago et al. 2021 and Marcjasz et al. 2023; across members every week is trained on by most members, a bagging
  effect). (b) Stop on the **mean pinball loss over the seven scored levels**, not on NLL. (c) Align the loss with the
  score: NLL warm-start, then (or jointly) minimise the mean pinball loss over a dense level grid (e.g. 19 or 49
  levels) evaluated on the JSU quantile function - a CRPS approximation whose 0.5-level term is the MAE.
  (d) Train long enough: patience 50, up to 1,000-1,500 epochs, small batches (32-128), learning rate searched.
- **Why here.** D - L is positive in every fold with identical information (2.0), best epochs were 3-8 (2.1), and the
  member was 28 days stale. The point forecast is scored by MAE and the quantiles by WIS (a weighted pinball sum), so a
  pinball-trained JSU optimises what is scored while staying monotone by construction.
- **Evidence.** Lago et al. (2021, footnote 11) on recent data; Marcjasz et al. (2023) recipe (patience 50, batch 32,
  1,500 epochs, random 20% validation); Gebetsberger et al. (2018) minimum-CRPS more robust than ML under
  misspecification; Gneiting and Raftery (2007) and Gneiting (2011) on proper scoring and quantile loss.
- **NumPy complexity.** Low. The pinball gradient is `1{y<q} - tau` times the analytic derivatives of
  `q = xi + lambda*sinh(w)`, `w = (z_tau - gamma)/delta`: dq/dxi = 1, dq/dlambda = sinh(w),
  dq/dgamma = -lambda*cosh(w)/delta, dq/ddelta = -lambda*cosh(w)*w/delta. About 150 lines plus finite-difference and
  PyTorch-reference tests (the reference harness already exists).
- **Compute.** 10-30x CP-23's epochs. Per-hour rows: 5-30 s per member; 8 members x 636 origins = 7-40 CPU-hours,
  about 2-10 h wall on 4 workers. Day-level rows (Direction 2): 5-25 s per member, similar totals. Within CP-23's caps
  (40 active hours, 60 machine hours) if the member count stays at 8.
- **Risks.** Longer training overfits without the regularisation of Direction 3; random-week validation is mildly
  optimistic (autocorrelation across adjacent weeks) - hence whole weeks, never single rows; pinball-only training gives
  weak tail signal - hence the dense grid and NLL warm start.
- **Fix before any fold scoring:** the refit rule (refit-to-epoch or random-week holdout, with the 20% share, the
  "never the last 7 days" rule and per-member split seeds), the stopping metric, patience, max epochs, the loss family
  options and the level grid, the warm-start rule, numeric floors.
- **May search on training-only data:** the loss weight between NLL and pinball, learning rate, batch size (within
  Direction 3's search, scored on pre-fold windows only).

### Direction 2 - A day-level, multi-output network on whole-day vectors (rank 2)
- **Mechanism.** One row per delivery day; one network emits 24 JSU parameter sets (96 outputs). Inputs, all within
  the same-information rule: the normalised 24-hour price vectors of D-1, D-2, D-3, D-7 (LEAR's 96 price features);
  the TSO load forecast vector for D (and, as optional groups, for D-1 and D-7); the three GFS columns as 24-hour
  vectors for D with day-level missing indicators; day-of-week, day-type and a smooth annual encoding.
  Fallback/diversity variant 2b: keep per-hour rows but append the full normalised D-1 price vector and D-1's last
  four hours to every row.
- **Why here.** It attacks the diagnosed night-hour and weekday deficits (2.2) with the information LEAR uses, and
  gives a learner that is structurally different from LightGBM (lower correlation with L, nonlinear where LEAR is
  linear). Every reference DNN in EPF is built this way.
- **Evidence.** Lago et al. (2021) DNN; Marcjasz et al. (2023) DDNN (inputs T-1, T-2 most selected); Ziel and Weron
  (2018) on multivariate (day-level) versus univariate (per-hour) frameworks and the value of combining both.
- **NumPy complexity.** Medium. Reuse the existing LEAR day design (`lear`, `ln` arrays in `src/cp15/data.py`) and its
  DST convention; output layer of 96 with a slot mask in the loss; emission maps 24 slots to the day's 23/24/25 UTC keys.
- **Compute.** ~500-728 rows per fit, ~250-320 inputs, two hidden layers of 64-256: 1-4 ms per Adam step at batch 32,
  5-25 s per member to convergence. Comparable to Direction 1's totals.
- **Risks.** Small sample (about 500 days at fold 1's start; never more than 728) for a wide input: needs L1/L2,
  dropout and input-group selection (Direction 3); it may correlate strongly with HG (same information), trading one
  redundancy for another - which is why it should be one configuration family inside the ensemble, not the only one;
  DST mapping errors.
- **Fix before scoring:** the exact feature list and grouping, the normalisation, the DST convention (23-hour day:
  masked slot; 25-hour day: rule for the repeated hour), the emission mapping, the minimum-history rule.
- **May search on training-only data:** which optional input groups enter (binary flags, as in both reference papers),
  widths/depth, and whether 2b enters as a second family.

### Direction 3 - Causal per-fold HPO on long rolling validation, and an ensemble of configurations (rank 3)
- **Mechanism.** Before each fold's first origin D0, evaluate random-search trials in a *hybrid batch-rolling* way
  (Marcjasz et al. 2023): for each of the 13 consecutive 28-day batches in `[D0-364, D0)`, train as production would
  (window ending at the batch start) and score the batch (mean pinball over the seven levels; MAE reported). Use
  successive halving to save cost (all trials on the 4 most recent batches, the best third on all 13). Keep the
  **top K = 4 configurations**, train each with 2 seeds (8 members) at every origin, and aggregate by the **median (or a
  fixed trimmed mean) of member quantiles** at each level. Search space: depth {1, 2, 3}; width 16-512 (log);
  activation {elu, softplus, tanh}; input dropout {0, 0.05-0.5}; L1 and L2 rates (log, including 0); learning rate
  1e-4..1e-2 (log); batch {32, 64, 128}; loss weight (Direction 1); input-group flags (Direction 2); VST choice
  (Direction 4); recency half-life (Direction 5).
- **Why here.** CP-23's per-fold choice rested on one 672-row holdout with margins as small as 0.03%; its ensemble had
  no architectural diversity (2.5). Random search is a strong baseline and is trivial to implement without Optuna
  (Bergstra and Bengio 2012); top-K ensembling removes the "winner's curse" of a single argmin.
- **Evidence.** Marcjasz et al. (2023): 4 x 2,048 Optuna trials, out-of-sample spread up to 10% among sets that tied
  in-sample, ensembles of the four sets best; Lago et al. (2021): 1,500 TPE trials, 4-run ensemble; Marcjasz (2020):
  long-sample evaluation for robust selection.
- **NumPy complexity.** Low-medium: a seeded sampler, a batch-rolling evaluator, successive halving, a ledger.
- **Compute.** Per fold about 64 x 4 + 21 x 9, i.e. roughly 450 fits; at 5-25 s per fit that is 0.6-3 CPU-hours
  per fold, 3-15 CPU-hours for five folds, about 1-4 h wall on 4 workers. Fold 1 has only ~17 months of history before
  D0, so its batch count must be smaller (e.g. 5 batches, keeping a 365-day minimum training window) - pre-register it.
- **Risks.** The validation year can differ from the fold (fold 3's validation year ends in May 2022, before the
  peak); HPO can overfit the validation year (mitigated by 13 batches and top-K); cost; non-determinism if BLAS
  threads vary.
- **Fix before scoring:** the search space and its priors, trial budget, sampler seed, the batch dates per fold, the
  halving schedule, the ranking metric, K, seeds, the aggregation rule and its tie rules. Nothing after D0 may inform
  any choice, and the procedure is identical for all five folds.
- **May search on training-only data:** everything inside the declared space, mechanically, by the declared procedure.

### Direction 4 - Robust, variance-stabilised scale and blow-up guards (rank 4; hygiene)
- **Mechanism.** Train in a compressed space `z' = asinh((y - m)/s)` with m and s either the existing section-4 level
  and scale or the median and MAD of the last 168 h (a two-option choice for Direction 3); apply the same transform to
  price inputs; winsorise every input column at its training-window 0.5/99.5% quantiles (fitted on training rows only);
  aggregate members robustly (Direction 3); cap emitted quantiles in normalised space at a bound fixed from training
  data (e.g. 1.25 x the training window's largest |z|) and log every activation of the cap.
- **Why here.** The 2021-04-05 and 2026-01-20 blow-ups (2.4) and 13 hours with |z| > 6. Quantiles back-transform
  exactly through sinh, so nothing is lost at the scored levels. Note the caveat: JSU-in-asinh-space has very heavy
  tails in EUR space (sinh of sinh), which is why the cap is part of this direction, not optional.
- **Evidence.** Uniejewski, Weron, Ziel (2018); Lago et al. (2021) treat the scaling choice as a hyperparameter;
  Marcjasz, Uniejewski, Weron (2019) on removing the long-term level before NN modelling.
- **NumPy complexity.** Low (tens of lines). **Compute:** negligible.
- **Risks.** The transform changes the shape the JSU must fit (it can hurt as well as help - hence searched, not
  imposed); the cap can bias extreme quantiles in genuine scarcity events (fold 3) - set it from training data only and
  report how often it binds.
- **Fix before scoring:** the transform options, m/s definitions and their time windows (ending at the last price
  known at the origin), the winsorisation quantiles, the cap rule, the aggregation rule.
- **May search on training-only data:** the choice between the two (m, s) options and asinh on/off.

### Direction 5 - Recency for regime shifts (rank 5; inside the search space)
- **Mechanism.** Exponentially down-weight old rows in the loss, `w = 0.5**(age/H)`, with H in {none, 365, 180} days,
  or add a 364-day-window member family next to the 728-day one.
- **Why here.** Fold 3 (and the 2026-01 events) are regime shifts; a 728-day uniform window adapts slowly.
- **Evidence.** Averaging across calibration windows beats the best single window (Hubicka, Marcjasz, Weron 2019;
  Marcjasz, Serafin, Weron 2018); LEAR-Ens in Lago et al. (2021) mixes 56-1,456-day windows.
- **NumPy complexity.** Trivial (weighted loss). **Compute:** none for weights; about 2x for a window family.
- **Risks.** Fewer effective samples for a data-hungry learner; it may hurt in calm folds. Searched on pre-fold
  windows only; never chosen because of fold 3.
- **Fix before scoring:** the option set and the weighting formula. **May search:** H within the declared set.

### Direction 6 - Use the distribution, not just the median (rank 6; a role, not a model change)
- **Mechanism.** A conditional-shape blend around v4's own p50:
  `q_tau = p50_v4 + (1 - a)*(H_tau - H_0.5) + a*(D2_tau - D2_0.5)` with a = 1/2 fixed, i.e. quantile averaging of two
  shape providers re-centred on the incumbent's median; or DDNN-2 quantiles as extra regressors in a QRA-type layer.
- **Why here.** DDNN's WIS deficit was smaller than its MAE deficit (2.3); the residual layer is unconditional apart
  from its price-SD scaling and hour shrinkage, whereas a DDNN can widen and skew intervals with load, wind, solar and
  calendar (negative-price Sundays, scarcity evenings).
- **Evidence.** Lipiecki, Uniejewski, Weron (2024): diversity among postprocessors drives the gain;
  Lichtendahl et al. (2013); Berrisch and Ziel (2023) for later learned per-quantile weights.
- **NumPy complexity.** Low. **Compute:** none beyond DDNN-2.
- **Risks.** v4's layer is already well calibrated (coverage 0.496/0.790/0.939), so the upside is modest and S_MAE is
  unchanged by construction; DDNN's own calibration was poor in CP-23 (central intervals too narrow).
- **Fix before scoring:** a, the re-centring formula, the order of operations relative to the H layer's bias
  correction, crossing repair. **May search:** nothing on the folds; a may be fixed by a pre-registered training-only
  rule or kept at 1/2.

---

## 4. How DDNN-2 should serve the programme, and a pre-registered candidate and adoption rule

### 4.1 Recommended role
1. **Primary: a member of v4's nonlinear block, at a structurally fixed weight.** v4 is "2/3 linear block (HG) +
   1/3 nonlinear block (L)", with equal weights inside each block (HG = A1/B2 50/50; L = mean of two LightGBMs).
   DDNN-2 joins the nonlinear block under the same rule:
   **v6 central = 2/3 HG + 1/3 * mean(L, D2) = 2/3 HG + 1/6 L + 1/6 D2**, followed by the H interval layer
   re-estimated on v6's residuals exactly as v4's (same 168-h SD scaling, 28-complete-day buffer, hour shrinkage,
   buffer-median bias correction). The weight follows from v4's own construction rule rather than from any fold
   outcome; it halves CP-23's exposure (1/6 instead of 1/3) and no longer gives the new member more weight than
   LightGBM.
2. **Archive for the learned-weight stage (4.8).** Store DDNN-2's seven quantiles and p50 on all 10,747 keys and
   their warm-ups, so that a later, separately pre-registered learned-weight recombination (e.g. per-quantile CRPS
   learning, Berrisch and Ziel 2023, or rolling constrained LAD weights on errors released up to D-2) can use it
   without another standalone look at the folds.
3. **Interval role (Direction 6): descriptive only in this checkpoint.** It changes only S_WIS, so it cannot satisfy
   a joint rule; if it looks useful, it belongs in 4.8 or in a fresh-data design, not in a second decision here.

### 4.2 DDNN-2 candidate definition (everything below frozen and hashed before any fold scoring)
- **Families (Direction 2).** F-day: day-level, 96 outputs, inputs = normalised 24-h price vectors D-1, D-2, D-3, D-7;
  load-forecast vector for D (optional groups D-1, D-7); GFS 3 x 24 for D with day-level missing indicators;
  day-of-week, day-type, annual sine/cosine. F-hour+: CP-23's 71 per-hour inputs plus the normalised D-1 24-h vector
  and D-1's last four hours. Both use the programme's existing DST convention.
- **Target and guards (Direction 4).** Options {z, asinh(z)} x {section-4 level/scale, 168-h median/MAD with floor},
  searched; inputs winsorised at training-window 0.5/99.5% quantiles; emitted quantiles capped at
  1.25 x the training window's largest |z| (log every activation); crossing repair by sorting (logged).
- **Head and loss (Direction 1).** Johnson SU with CP-23's floors. A fixed NLL warm start (20 epochs), then
  kappa * NLL + (1 - kappa) * mean pinball over a 19-level grid that contains the seven scored levels;
  kappa in {1, 0.5, 0} searched.
- **Training (Direction 1).** Adam; per-member early stopping on the seven-level pinball over a random 20% of whole
  calendar weeks of the window, excluding the most recent 7 days from the holdout pool; patience 50; max 1,000 epochs;
  best epoch kept. Window `[max(2019-01-01, D-728), D)`, optional recency weights with H in {none, 365, 180}
  (Direction 5). Daily refit at every origin, from the fold's warm-up start D0.
- **HPO (Direction 3).** Per fold, before D0, from data before D0 only: random search, 64 trials split equally between
  the two families, hybrid batch-rolling over the 11 consecutive 28-day batches of `[D0-364, D0-56)` (the last 56 days
  before D0 are reserved for the gate in 4.3, so Direction 3's 13 batches become 11 here); fold 1 uses as many batches as a 365-day minimum training window allows
  (pre-register the dates); successive halving (all trials on the 4 most recent batches, best third on all);
  ranking by mean seven-level pinball, ties to the smaller network.
- **Ensemble.** K = 4 configurations, the top 2 of each family, x 2 seeds = 8 members; per-level **median of member
  quantiles** in the normalised space, then inverted; p50 = that median.
- **Use.** v6 as in 4.1.

### 4.3 A training-only gate before the folds are touched
On each fold's reserved pre-D0 window `[D0-56, D0)` (5 x 56 = 280 days; none overlaps a scored fold), run DDNN-2 with
the HPO result, and v4's members with their own unchanged code. Proceed to fold scoring only if, pooled over the 280
days: **(G1)** v6's central MAE <= v4's central MAE (point estimate); **(G2)** D2's MAE <= 1.10 x L's MAE; **(G3)** the
cap binds on fewer than 0.1% of hours. Otherwise stop and report a training-only negative result; the five folds are
not spent. (A screen, not a claim: no interval, no adoption.)

### 4.4 Adoption rule on the folds (one primary contrast: v6 - v4)
Adopt v6 if and only if all hold:
1. **Joint improvement, multiplicity-adjusted.** Paired 7-day block bootstrap within folds, the shared CP-20 index set
   and seed: the upper bounds of the **97.5%** intervals of dS_MAE and dS_WIS are both < 0. (CP-23 used 95%; this is
   the second DDNN look at the same folds, so the 5% is split across the two looks. Reconcile with the programme's own
   protection, 4.7T, by taking whichever is stricter.)
2. **Practical size.** Both point improvements are at least 0.5% of v4's score.
3. **No fold decisively worse.** In every fold, neither the MAE nor the WIS per-fold 95% interval of v6 - v4 lies
   entirely above 0 (fold 3 included).
4. **Diagnostics and validity.** All six section-8 diagnostics met; all 10,747 keys issued with finite, ordered
   quantiles; Engineering PASS; guard activations reported.
5. **Status.** An adoption is development_post_selection and provisional; confirmation is the reserved fresh-data test
   under the same rule at 95%, with nothing re-tuned.
If v6 is not adopted, DDNN-2 is not re-scored at any other fixed weight on these folds; it remains only as an archived
candidate member for 4.8.

Descriptive contrasts (choose nothing): D2 alone vs L, HG and CP-23's D; per-hour gap profile; error correlations with
HG, L and v4; D2's own calibration and PIT; the Direction 6 shape blend; guard and crossing counts; fit cost and the
daily cycle time.

### 4.5 Why this is fair to v4 and protective
- v4 is untouched (members bit-for-bit, same H procedure, same index set); the only change is one added member in the
  block it naturally belongs to, at a weight implied by v4's own rule.
- Every DDNN-2 choice is made from data before each fold's D0 by a mechanical procedure frozen in advance; the only
  outcome-dependent step before scoring is the training-only gate, which can only *prevent* a fold look.
- One primary decision, a stricter interval, a minimum effect size and a per-fold veto; no "repair and rescore" loop.

---

## 5. Pitfalls to avoid

**Normalisation and scaling leakage**
- The origin's level and scale (and any median/MAD option) must use only prices delivered up to D-1 (known at D-1
  11:00 UTC), computed once per origin and applied to every row of D. Never compute "rolling" statistics per forecast
  row, which silently pulls hours of D into the window.
- Input scalers, winsorisation quantiles, weather medians and VST statistics are fitted on the member's own training
  rows only - not on its early-stopping weeks, not on forecast rows, not pooled across folds; each HPO batch refits its
  own. Quantiles are inverted with the origin's level and scale, never the realised ones.
- The aggregation space is a choice: averaging (or taking medians) in normalised or asinh space differs from doing it
  in EUR/MWh. Fix it in the protocol. (Per-level medians and trimmed means preserve quantile order; sorting is still
  logged as a guard.)

**Daylight-saving days**
- Day-level slots: on the 23-hour day mask the missing slot in the loss (never interpolate a target); on the 25-hour
  day define how the repeated local hour enters inputs and how both UTC hours are issued. Issue exactly the day's UTC
  keys (23/24/25). Reuse the LEAR design's existing convention rather than inventing a second one.
- "Lag 24 h" and "same local hour of D-1" differ on DST days; bootstrap blocks are calendar days, not 24-row chunks;
  weather columns on DST days follow the same mapping. Add fixtures for both DST days of every year 2019-2026.

**Early stopping**
- A most-recent holdout that is never trained on makes every member stale (CP-23). A random *row* holdout leaks
  through autocorrelation and stops too late; use whole weeks. Never touch an evaluation fold.
- The best-epoch validation loss is optimistically biased (it is a minimum): do not report it as evidence; use the
  separate gate window.
- Stopping on NLL is tail-dominated under drift; stop on the scored pinball metric.
- Determinism: one BLAS thread per worker, fixed seeds, fixed batch order, restart replay - or bitwise reproducibility
  of early stopping fails across machines and thread counts.

**Crisis extrapolation**
- Without gas and EUA, the level shift is visible only through lagged prices; normalisation makes the target relative,
  but the shape of the z-distribution (weekend and solar dips, evening scarcity) changes when volatility jumps.
- Caps and winsorisation can clip genuine scarcity tails: set them from training data, log every activation, report
  them in fold 3, and do not tune them on fold 3.
- No crisis indicators, period dummies or features built with knowledge of 2022 (causality and the same-information
  rule). Do not choose recency weights, windows or caps because they "fix fold 3".

**Multiple testing on reused folds**
- Every decision on these five folds is development evidence after selection; the chance that one of several looks
  "succeeds" by luck grows with the number of looks. One primary contrast, a stricter level, a minimum effect, a
  per-fold veto, no repair-and-rescore loop, and a running count of looks in the record.
- Design-level selection is real: these directions were partly motivated by CP-23's fold diagnostics (e.g. the
  night-hour gap). Keep choices at the level of literature-backed mechanisms, never fold-specific values; the fresh-data
  test is the only confirmation.
- Do not use hindsight weights (CP-23's 0.05-0.10 optimum) as pre-registered values; derive weights from a structural
  rule (4.1) or learn them causally (4.8).
- Do not narrow the HPO space after seeing any fold outcome; descriptive contrasts must not be read as tests.

**Ensembling**
- Quantile averaging is a mean and inherits any member's blow-up; use a per-level median or a fixed trimmed mean.
- Seed ensembles only reduce variance; diversity needs different configurations or representations.
- Fix the p50 definition (aggregated median) and keep v6's emitted p50 (central plus the H layer's median residual)
  separate from its central forecast, as in CP-23.

**Information timing**
- Errors are released only up to D-2: the H buffer, any learned weights, and any input built from v4's forecasts or
  residuals must respect it. Prices of D-1 are not errors and are usable.
- GFS and TSO load-forecast inputs must be the vintages available before D-1 11:00 UTC; for D-1/D-7 load-forecast
  lags use the forecasts as issued, not actual load. Use the same holiday calendar as LEAR.

**Engineering and operations**
- Compute grows 10-30x versus CP-23; plan the HPO ledger and resumability; set MLflow telemetry off
  (MLFLOW_DISABLE_TELEMETRY and DO_NOT_TRACK) for any tracked job.
- The daily product cycle must still fit: 8 longer-trained members could take 10-50 s per origin on 4 workers;
  measure the cold cycle as CP-23 did.
- NumPy-only: the HPO sampler, pinball loss and guards stay in NumPy and the standard library; PyTorch only in the
  reference tests (extend them to the pinball-on-JSU gradient and to masked multi-output losses).

---

## 6. References

- Akiba, T., Sano, S., Yanase, T., Ohta, T., Koyama, M. (2019). Optuna: A next-generation hyperparameter optimization
  framework. Proc. KDD 2019, 2623-2631. https://doi.org/10.1145/3292500.3330701
- Barunik, J., Hanus, L. (2023, rev. 2025). Learning the probability distributions of day-ahead electricity prices.
  arXiv:2310.02867. https://arxiv.org/abs/2310.02867
- Bates, J. M., Granger, C. W. J. (1969). The combination of forecasts. Operational Research Quarterly 20(4),
  451-468. https://www.jstor.org/stable/3008764
- Bergstra, J., Bardenet, R., Bengio, Y., Kegl, B. (2011). Algorithms for hyper-parameter optimization. NeurIPS 24.
  https://papers.nips.cc/paper/4443-algorithms-for-hyper-parameter-optimization
- Bergstra, J., Bengio, Y. (2012). Random search for hyper-parameter optimization. JMLR 13, 281-305.
  https://jmlr.org/papers/v13/bergstra12a.html
- Berrisch, J., Ziel, F. (2023). CRPS learning. Journal of Econometrics 237(2), 105221.
  https://doi.org/10.1016/j.jeconom.2021.11.008
- Dutot, G., Zaffran, M., Feron, O., Goude, Y. (2024). Adaptive probabilistic forecasting of French electricity spot
  prices. arXiv:2405.15359. https://arxiv.org/abs/2405.15359
- Gebetsberger, M., Messner, J. W., Mayr, G. J., Zeileis, A. (2018). Estimation methods for nonhomogeneous regression
  models: Minimum continuous ranked probability score versus maximum likelihood. Monthly Weather Review 146(12),
  4323-4338. https://doi.org/10.1175/MWR-D-17-0364.1
- Gneiting, T. (2011). Quantiles as optimal point forecasts. International Journal of Forecasting 27(2), 197-207.
  https://doi.org/10.1016/j.ijforecast.2009.12.015
- Gneiting, T., Raftery, A. E. (2007). Strictly proper scoring rules, prediction, and estimation. JASA 102(477),
  359-378. https://doi.org/10.1198/016214506000001437
- Gneiting, T., Ranjan, R. (2013). Combining predictive distributions. Electronic Journal of Statistics 7, 1747-1782.
  https://doi.org/10.1214/13-EJS823
- Hubicka, K., Marcjasz, G., Weron, R. (2019). A note on averaging day-ahead electricity price forecasts across
  calibration windows. IEEE Transactions on Sustainable Energy 10(1), 321-323. https://doi.org/10.1109/TSTE.2018.2869557
- Jedrzejewski, A., Lago, J., Marcjasz, G., Weron, R. (2022). Electricity price forecasting: The dawn of machine
  learning. IEEE Power and Energy Magazine 20(3), 24-31. https://doi.org/10.1109/MPE.2022.3150809
- Johnson, N. L. (1949). Systems of frequency curves generated by methods of translation. Biometrika 36(1/2), 149-176.
  https://doi.org/10.2307/2332539
- Kath, C., Ziel, F. (2021). Conformal prediction interval estimation and applications to day-ahead and intraday power
  markets. International Journal of Forecasting 37(2), 777-799. https://doi.org/10.1016/j.ijforecast.2020.09.006
- Lago, J., Marcjasz, G., De Schutter, B., Weron, R. (2021). Forecasting day-ahead electricity prices: A review of
  state-of-the-art algorithms, best practices and an open-access benchmark. Applied Energy 293, 116983.
  https://doi.org/10.1016/j.apenergy.2021.116983 ; arXiv:2008.08004 https://arxiv.org/abs/2008.08004 ; code:
  https://github.com/jeslago/epftoolbox
- Lichtendahl, K. C., Grushka-Cockayne, Y., Winkler, R. L. (2013). Is it better to average probabilities or
  quantiles? Management Science 59(7), 1594-1611. https://doi.org/10.1287/mnsc.1120.1667
- Lipiecki, A., Uniejewski, B., Weron, R. (2024). Postprocessing of point predictions for probabilistic forecasting of
  day-ahead electricity prices: The benefits of using isotonic distributional regression. Energy Economics.
  arXiv:2404.02270. https://arxiv.org/abs/2404.02270
- Marcjasz, G. (2020). Forecasting electricity prices using deep neural networks: A robust hyper-parameter selection
  scheme. Energies 13(18), 4605. https://www.mdpi.com/1996-1073/13/18/4605
- Marcjasz, G., Narajewski, M., Weron, R., Ziel, F. (2023). Distributional neural networks for electricity price
  forecasting. Energy Economics 125, 106843. https://doi.org/10.1016/j.eneco.2023.106843 ; arXiv:2207.02832
  https://arxiv.org/abs/2207.02832
- Marcjasz, G., Serafin, T., Weron, R. (2018). Selection of calibration windows for day-ahead electricity price
  forecasting. Energies 11(9), 2364. https://doi.org/10.3390/en11092364
- Marcjasz, G., Uniejewski, B., Weron, R. (2019). On the importance of the long-term seasonal component in day-ahead
  electricity price forecasting with NARX neural networks. International Journal of Forecasting 35(4), 1520-1532.
  https://doi.org/10.1016/j.ijforecast.2017.11.009
- Marcjasz, G., Uniejewski, B., Weron, R. (2020). Probabilistic electricity price forecasting with NARX networks:
  Combine point or probabilistic forecasts? International Journal of Forecasting 36(2), 466-479.
  https://doi.org/10.1016/j.ijforecast.2019.07.002
- Nowotarski, J., Weron, R. (2015). Computing electricity spot price prediction intervals using quantile regression
  and forecast averaging. Computational Statistics 30(3), 791-803. https://doi.org/10.1007/s00180-014-0523-0
- Olivares, K. G., Challu, C., Marcjasz, G., Weron, R., Dubrawski, A. (2023). Neural basis expansion analysis with
  exogenous variables: Forecasting electricity prices with NBEATSx. International Journal of Forecasting 39(2),
  884-900. https://doi.org/10.1016/j.ijforecast.2022.03.001 ; arXiv:2104.05522
- Ranjan, R., Gneiting, T. (2010). Combining probability forecasts. Journal of the Royal Statistical Society B 72(1),
  71-91. https://doi.org/10.1111/j.1467-9868.2009.00726.x
- Timmermann, A. (2006). Forecast combinations. In Handbook of Economic Forecasting, Vol. 1, 135-196.
  https://doi.org/10.1016/S1574-0706(05)01004-9
- Uniejewski, B., Weron, R. (2021). Regularized quantile regression averaging for probabilistic electricity price
  forecasting. Energy Economics 95, 105121. https://doi.org/10.1016/j.eneco.2021.105121
- Uniejewski, B., Weron, R., Ziel, F. (2018). Variance stabilizing transformations for electricity spot price
  forecasting. IEEE Transactions on Power Systems 33(2), 2219-2229. https://doi.org/10.1109/TPWRS.2017.2734563
- Ziel, F., Weron, R. (2018). Day-ahead electricity price forecasting with high-dimensional structures: Univariate vs.
  multivariate modeling frameworks. Energy Economics 70, 396-420. https://doi.org/10.1016/j.eneco.2017.12.016

Verification note: Marcjasz et al. (2023) and Lago et al. (2021) details above were read from the arXiv full texts;
the other entries are cited for their main, well-known findings, and their DOIs were not individually re-checked in
this session.
