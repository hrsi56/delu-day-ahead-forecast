# Stage 4 forecasting evaluation methodology memo

**Date:** 2026-10-12. **Executor:** research agent. **Status:** recommendations for an Owner-ratified protocol and independent criticism; this memo grants no execution or governance authority.

## Summary

1. Evaluate all eligible delivery days in 2020-12-29–2026-04-07; the inclusive calendar contains 1,926 days, before eligibility exclusions.
2. Refit daily on the preceding 728 calendar delivery days, using information available at D−1 11:00 UTC and preserving input vintages.
3. Keep v1–v5 intact; fix v5 as the research control and retain v1 as the released-product comparator. Standalone DDNN-2 remains descriptive.
4. Keep p50 MAE and the existing seven-quantile WIS co-primary; average native hours within days, then weight days equally.
5. Report whole-period B0 ratios, raw losses, untouched historical fold results, and previously unscored days separately.
6. Register year, season, hour, day type and origin-known risk strata; realized negative-price slices support descriptive analysis only.
7. Use paired 14-day blocks, 10,000 replicates and frozen calendar strata; 7/28-day and boundary-crossing variants are sensitivity checks.
8. Test at least 0.5% improvement on both scores and 2% non-inferiority in adequately supported year/season cells; use Holm across policy claims.
9. Allocate developmental family levels of 2.5% to CP-27 and 2.5% to CP-28; freeze all reachable policies before results are inspected.
10. CP-27 tests at most eight source packages, nominates at most one, and requires later chronological confirmation plus vintage and delay gates.
11. CP-28 adds equal and conservatively learned convex quantile averages; learn daily only from earlier, genuinely out-of-sample forecasts.
12. Keep the specified fresh-test and retraining-replay periods closed; freeze one candidate before opening the 90-day test once, with a null outcome permitted.

## Scope and interpretation

The target is the hourly DE-LU price of the single day-ahead coupling auction for delivery day D in Europe/Berlin. Each issued forecast contains p50 and quantiles 0.025, 0.10, 0.25, 0.50, 0.75, 0.90 and 0.975; p50 is the same median as the 0.50 quantile. Delivery days have 23, 24 or 25 native hours. The issue time remains exactly D−1 11:00 UTC.

The brief supplies the five generation definitions, their earlier adoption history and the existing 448 scored days. Those results, their re-evaluation, and CP-27/28 selection remain **post-selection development evidence**. Previously unscored days broaden coverage; they do not undo selection on related historical data. Nominal error controls below describe a prospectively frozen, finite research procedure under its dependence assumptions. They cannot cover unrecorded earlier experimentation or establish fresh confirmation retrospectively.

The fresh test is fixed at **2026-04-08–2026-07-06**; the subsequent daily-retraining replay is **2026-07-07–2026-10-04**. These are scheduling boundaries supplied by the brief. This memo contains no market observations or empirical conclusions from either period. No project data files were opened, market data downloaded or models run. The programme plan and governing anchors were not opened or changed; the supplied brief is the project-specific source.

Throughout, **recommended values are design judgements unless explicitly attributed as published findings**. In particular, 728 days, the block length, margins, source cap, combiner burn-in, shrinkage and resource limits are not universally optimal constants established by the literature.

## Research question 1 Rolling evaluation and training windows

### Recommended choice

Use daily rolling origins with a **728-calendar-day** window, D−728 through D−1. The first window is 2019-01-01–2020-12-28. A calendar window does not become 728 nonmissing observations after gaps. Include a training label only when its publication is evidenced before the current issue cutoff. Delivery completion and day-ahead target availability are different clocks.

Reproduce each generation's existing algorithms, feature contracts, ensemble sizes, seeds, interval construction and embedded tuning rules. CP-26 changes evaluation coverage, not the identities of v1–v5. A common window is defensible if it is the brief's existing capped procedure; an implementation discrepancy must be resolved before results, with the changed procedure named separately.

Historical predictor rows must reproduce their own historical forecast-origin information sets. Fit scalers, feature selection, penalty selection and any interval calibrator using permitted training information only. Do not recompute an old weather predictor using an analysis or a later corrected forecast. Original snapshots can contain revisions already published at that historical origin; undocumented final revisions cannot be substituted for them.

For CP-27/28, freeze the algorithm for any inner adaptation: predictor menu, hyperparameter grid, chronological split dates relative to each origin, tuning score, retuning cadence, seed list, early-stopping rule and maximum fits. Numerical coefficients and a lasso penalty chosen by an already specified training-only rule may change daily. The outer window, architecture menu, scoring weights and adoption criteria may not change after outer losses appear. The default is **no additional architecture search** beyond those registered procedures.

### Alternatives and evidence

Expanding history from 2019-01-01 retains scarce tail examples and reduces sampling variance, but can retain obsolete relationships. A shorter fixed window adapts faster but weakens seasonal and tail estimation. The supplied 2021–2022 stress period makes memory choice consequential; it does not determine which window will win. Register expanding history as a secondary sensitivity, within the same compute ceiling, without allowing it to replace the primary procedure after inspection.

Tashman recommends evaluation over rolling origins, recalibration and diverse periods. Calibration-window studies show that useful window lengths depend on the model and market, and that averaging across windows can reduce the risk of choosing one length. Hubicka et al. study a short/long window set of 28, 56, 84,714,721 and 728 days. These findings motivate an alternative, not an optimality claim for 728. [Tashman 2000](https://doi.org/10.1016/S0169-2070(00)00065-0), [Marcjasz et al. 2018](https://doi.org/10.3390/en11092364), [Hubicka et al. 2019](https://doi.org/10.1109/TSTE.2018.2869557).

A bounded optional multi-window arm would average forecasts from **56, 84,364 and 728 days equally**. It ranks below the primary design because it multiplies fits, may be unsuitable for complex members at short windows, and creates another selectable policy. Exclude it from the recommended initial candidate menu; adding it requires advance inclusion in the policy family and budget. The DDNN study separates daily weight recalibration from an initial hyperparameter search; its cheaper search schedule does not justify cheaper outer evaluation. [Marcjasz et al. 2023, methods](https://arxiv.org/pdf/2207.02832).

### Timing risk requiring an Owner decision

Historical papers describe local-noon auction closure and publication beginning at 12:42. **11:00 UTC is 12:00 CET but 13:00 CEST.** The specified issue can therefore fall after publication in summer; this is an inference from historical timings, not a statement about the closed periods. Verify the historical clock and target-availability conventions before ratifying a pre-auction interpretation. Explicitly exclude target-D auction prices, their transformations and same-auction results that reveal the target even if a generic availability filter would admit them. Preserve 11:00 UTC unless the Owner changes the target experiment. [Kulakov 2020, §2.1](https://doi.org/10.3390/forecast2010002), [Fridgen et al. 2020, Table 1](https://doi.org/10.1016/j.enpol.2020.111523).

The recommendation would be wrong if 728-day fitting materially undertrains an important member, or if legitimate input vintages cannot reproduce the historical control. Those are reasons to register another procedure or reconsider feasibility before execution, not to repair the window after seeing the scores.

## Research question 2 Scores and breakdowns

### Recommended scores and aggregation

For a central interval with miscoverage α, lower bound l and upper bound u, use

`ISα = (u−l) + (2/α)(l−y)1[y<l] + (2/α)(y−u)1[y>u]`.

For α in {0.50, 0.20, 0.05}, keep exactly

`WIS = {0.5|y−p50| + Σα (α/2)ISα}/3.5 = (2/7)Στ ρτ(y−qτ)`.

Here `ρτ(e)=e(τ−1[e<0])`. WIS is proper for the supplied quantiles and preserves the earlier scoring contract. Its approximation to CRPS improves with richer quantile grids; seven nonuniform quantiles do not identify exact CRPS. [Bracher et al. 2021](https://doi.org/10.1371/journal.pcbi.1008618), [Gneiting and Raftery 2007](https://doi.org/10.1198/016214506000001437).

Compute each daily loss as the mean over the day's **actual H_D hours**, then average days equally. Report raw MAE and WIS in the target's price units and `S_k = mean_D L_candidate, k / mean_D L_B0, k`. B0 must have the same frozen quantile and vintage contract for all arms. Reject an undefined or zero denominator; do not invent a small stabilizing constant.

This whole-calendar ratio measures a typical day's absolute loss relative to a common baseline; it is not the average of daily ratios. It preserves model rankings for a fixed metric. Equal weighting of separately normalized periods changes the estimand and can give easy or short periods disproportionate influence. Keep the old equal-fold S_MAE/S_WIS and their original bootstrap results unchanged as the historical record. New full-calendar statistics must not overwrite them.

Report, separately, (a) every eligible day; (b) the fixed mask of previously unscored days; (c) the old-fold day mask under the new procedure, clearly distinguished from the original results. If all 448 historical days lie in the eligible calendar, 1,478 calendar days were not previously scored; the actual eligible count is determined by frozen exclusions. The unscored mask must be fixed from existing records before score inspection, never chosen by observed loss.

Secondary summaries are the mean of the four pooled meteorological-season B0 ratios and the mean of the five complete-year ratios for **2021–2025**. Report partial 2020 and 2026 separately and report each denominator, day count and uncertainty. Neither a three-day 2020 segment nor a partial 2026 year receives the weight of a full year. Quarters remain an additional descriptive table; overlapping years, seasons and quarters are not independent replications.

### Calibration and pre-registered breakdowns

Report 50%, 80% and 95% central coverage, lower and upper exceedance rates, mean interval widths, quantile hit frequencies, and WIS's dispersion/underprediction/overprediction components. Use whole-day block uncertainty. A calibrated but excessively wide forecast can still lose on a proper score; calibration and sharpness must be assessed together. [Gneiting et al. 2007](https://doi.org/10.1111/j.1467-9868.2007.00587.x), [Nowotarski and Weron 2018](https://doi.org/10.1016/j.rser.2017.05.234).

Seven quantiles support an **eight-bin quantile calibration histogram**, with expected probabilities `.025, .075, .15, .25, .25, .15, .075, .025`. Display observed frequency divided by expected probability, rather than expecting equal counts in equally drawn bars. Assign ties deterministically to the upper interval for the descriptive histogram and report the tie rate. Expected bin equality assumes continuous, tie-free targets. Where ties occur, show strict and weak quantile-hit bounds: a valid quantile satisfies `P(Y<qτ) ≤ τ ≤ P(Y≤qτ)`; a deterministic bin allocation must not disqualify a valid discrete forecast. Do not label this an exact PIT. Exact PIT and CRPS remain excluded from the main analysis; an optional reconstructed-CDF analysis needs identical, advance-fixed interpolation and tails for every generation.

For conditional coverage, report Christoffersen's unconditional, first-order independence and conditional-coverage likelihood-ratio statistics as descriptive diagnostics, stating their Bernoulli/Markov assumptions.

Use a separate dependence-aware moment test on each local-hour series on 24-hour days. For an interval with nominal coverage c and hit I_D, define `g_D = (I_D−c, (I_D−c)(I_{D−1}−c), (I_D−c)(I_{D−7}−c))`; form the Wald statistic from its mean and Bartlett HAC covariance at lag 14. Calendar lags must be genuine adjacent dates; exclude a lag product if either day is unavailable. Bootstrap the centered moment vectors in paired day blocks to obtain its null distribution; do not insert centered continuous moments into a Bernoulli likelihood. Restrict equality-based tests to cells without ties at their forecast bounds.

Use one joint three-moment Wald test per model/hour/interval, at least 180 days with all moment components valid, and the centered bootstrap statistic `n_b (g_bar_b−g_bar)' Ω_b^−1 (g_bar_b−g_bar)`, compared with `n g_bar' Ω^−1 g_bar`, where Ω is the HAC covariance of the moment series. Build calendar-lag moments on the original chronology and carry them with blocks; do not form products across artificial sampled-block joins. Singular covariance, insufficient support or ties make that registered diagnostic unavailable with p=1.

Use Holm at **5% across the complete registered moment-test family**: at the maximum menu size, 17 forecast procedures (15 candidates plus B0 and standalone DDNN-2), 24 hours and three intervals give 1,224 joint tests. Use **100,000 replicates, seed 20261013** for this diagnostic family, with the same block/boundary rules as the primary bootstrap. Its minimum attainable p-value is 1/100,001; 10,000 replicates would be unable to meet the first Holm threshold for 1,224 tests. Report Monte Carlo uncertainty near diagnostic thresholds. This tests only the specified finite hit moments, not every possible conditional-calibration failure. Non-rejection is not proof of calibration, especially at 2.5% tails. [Christoffersen 1998](https://doi.org/10.2307/2527341), [Nowotarski and Weron 2015](https://doi.org/10.1007/s00180-014-0523-0).

The breakdown registry is:

| Dimension | Definition and role |
| --- | --- |
| Season | DJF, MAM, JJA, SON by local delivery date; pooled-season safety endpoints |
| Year | Calendar years, with 2020/2026 partial labels; complete-year safety endpoints |
| Quarter | Calendar quarter; descriptive, with partial quarters marked |
| Hour | Local hour 00–23; retain UTC timestamp and autumn fold for duplicate hours |
| Day type | Monday–Friday versus Saturday/Sunday; separate public-holiday indicator; 23/24/25-hour length |
| Holiday | Dates from a frozen, versioned Germany-wide statutory holiday calendar; regional holidays excluded |
| Historical stress | 2021-01-01–2022-12-31 versus its complement; the brief's calendar slice, descriptive |
| Origin-known negative risk | Any negative target value in the seven most recent delivery days whose targets are fully available at issue |
| Origin-known volatility | V_D = standard deviation of the last 28 fully available daily mean prices; high if above the 90th percentile of the previous 365 origin-known V values |
| Realized outcomes | Negative-hour and extreme realized-loss slices; descriptive only, never acceptance endpoints |

For volatility, use sample standard deviation, linear-interpolation empirical percentiles, strict `>` for the high flag, and an unknown flag if fewer than 365 prior V values exist. Training-only history may supply these states; unavailable labels never enter the calculation. These numbers are proposed choices, not fitted change points. They avoid defining a regime from a candidate's future error or from a breakpoint selected on the whole evaluation sample.

### Alternatives and risks

Dense-quantile CRPS is attractive when every member supplies the same complete distribution interface. Here it would add arbitrary tail assumptions or give DDNN an information advantage. Per-hour inferential leaderboards, equal-quarter primary weighting and retrospective crisis boundaries rank lower because they multiply opportunities for selection and answer a different deployment question.

A realized negative-price bucket conditions on the outcome. Its ordinary coverage need not equal nominal coverage even for a correct forecast. Lerch et al. demonstrate how outcome-based extreme-event evaluation can penalize skilful forecasts. Origin-known regimes are safer conditioning variables, but still require enough observations and valid availability. [Lerch et al. 2017](https://doi.org/10.1214/16-STS588).

Day weighting gives a 23-hour day the same total weight as a 25-hour day. If the Owner's objective is instead loss per traded hour or an economic decision loss, that is a different primary estimand and must be chosen before results.

## Research question 3 Dependence inference and multiplicity

### Recommended inferential unit and bootstrap

Use one daily MAE and one daily WIS per policy, paired on the same eligible calendar. Ziel and Weron's vectorized/multivariate DM comparison takes an L1 norm of the hourly error vector and applies a scalar loss-differential test. On 24-hour days it differs from daily mean MAE only by a common factor. It is not a 24-degree-of-freedom joint Wald test. Native-hour daily averaging extends the primary comparison consistently to DST days. [Ziel and Weron 2018, §5.2.1](https://arxiv.org/html/1805.06649).

The primary resampling rule is **paired non-circular moving blocks of 14 calendar days, 10,000 replicates, seed 20261012**. Use identical sampled day indices for every policy, both metrics, B0 and breakdown labels. Resample within fixed calendar-year strata; attach the three days of 2020 to the 2021 stratum, and retain 2026 as a partial stratum. For the CP-27 early/late split, do not cross that boundary. Blocks may not cross a genuine missing-date gap; never concatenate nonadjacent eligible days into an apparently continuous run. Resample each fixed contiguous run separately: choose permissible full-block starts uniformly with replacement and truncate the last drawn block to restore that run's original count; then combine runs with their original fixed counts. A run shorter than the block length retains its complete paired observations, but supplies no within-run resampling uncertainty. If a required contrast materially relies on such a run, its inference is inconclusive; do not interpret an artificially zero variance as certainty.

For a regime or seasonal statistic, draw chronological blocks first and then apply their carried labels. Recompute ratios and denominators inside each replicate. Do not sample only negative or high-volatility days and pretend they were consecutive.

Use a **centered studentized bootstrap test** for mean loss contrasts. For a registered superiority or NI contrast θ, set `T_obs = θ_hat / SE_hat` and `T_b* = (θ_hat_b* − θ_hat) / SE_hat_b*`. Improvement and NI reject in the left tail; `p = (1 + count[T_b* ≤ T_obs])/10,001`. Estimate long-run variance with Bartlett HAC using 14 calendar-day lags, centering within each fixed stratum and combining run/stratum contributions with their fixed counts; never globally demean a heterogeneous timeline. In the original sample, HAC lags mean calendar-day separations inside each contiguous run; in a bootstrap sample they mean consecutive positions in that run's synthetic draw, including its block joins. Re-estimate the standard error in each replicate.

For a reported score ratio R=A/C, studentize with the paired delta-method influence `(L_A − R L_C)/C_bar`, using the same HAC and weighting scheme; the contrast SE is not its ratio SE. Recompute R and its influence in each replicate and use bootstrap-t quantiles for intervals. Report Monte Carlo uncertainty near a gate. Zero or undefined standard errors require a declared degeneracy result, not an improvised significance decision.

The block bootstrap preserves local dependence, including weekly effects, rather than resampling hours or individual days independently. Fourteen days and 10,000 replicates are conservative engineering choices, not a proven optimum. Register **7- and 28-day blocks**, and a **14-day whole-chronology bootstrap allowing calendar-year crossings**, as sensitivity analyses. A candidate that passes the primary gate but fails an otherwise identical required threshold at either 7 or 28 days is **inconclusive**, not accepted; boundary-crossing disagreement also triggers an inconclusive disposition. No favourable variant replaces the primary test. [Künsch 1989](https://doi.org/10.1214/aos/1176347265), [Politis and Romano 1994](https://doi.org/10.1080/01621459.1994.10476870).

Calendar stratification preserves the evaluation's year mixture but omits cross-boundary covariance and does not ensure stationarity within a year. Block procedures and DM/HAC require dependence and moment conditions; 1,926 days do not guarantee validity under arbitrary structural changes or extreme tails. Forecast-instability work supports inspecting the loss path rather than relying on one average. [Giacomini and Rossi 2010](https://doi.org/10.1002/jae.1177).

### Tests and their different questions

| Method | Recommended role and limitation |
| --- | --- |
| DM on daily losses | Secondary unconditional comparison of frozen forecast procedures; Bartlett HAC lag 14; does not establish model truth or erase prior search |
| Vectorized DM | Explained through its daily vector norm; native-hour primary losses already address within-day clustering |
| Hourwise DM | Descriptive diagnostics with Holm correction across all registered contrasts; no winner selected from 24 hourly tests |
| Giacomini–White | Secondary conditional comparison for the fixed-window procedure; instruments fixed as constant, lag-1 daily loss differential, weekend, origin-known negative-risk and high-volatility flags |
| Model Confidence Set | 90% confidence set, range statistic T_R, same block scheme and 10,000 replicates, separately for MAE/WIS; descriptive shortlist only |
| Hansen SPA | Secondary global test at 5% against v5, separately by metric, with consistent recentering/studentization; Holm across its two global tests |
| White Reality Check | Literature comparator; lower-ranked operationally because irrelevant poor alternatives can reduce power |

DM concerns predictive loss differences, not the proposition that one estimated model is correct. The fixed 728-day window is compatible with the original Giacomini–White finite-memory setup; expanding-window sensitivity cannot automatically inherit that result. GW instruments must be known at issue and bounded in number. None of these tests replaces the adoption family. [Diebold and Mariano 1995](https://doi.org/10.1080/07350015.1995.10524599), [Diebold 2015](https://doi.org/10.1080/07350015.2014.983236), [Giacomini and White 2006](https://doi.org/10.1111/j.1468-0262.2006.00718.x).

MCS can retain several policies without declaring a unique best one. SPA and Reality Check address whether any policy in a searched, supplied universe beats a benchmark; a rejected global null does not license every individual admission. MCS survival is not proof of equivalence and its confidence level is not an individual superiority level. [Hansen et al. 2011](https://doi.org/10.3982/ECTA5771), [Hansen 2005](https://doi.org/10.1198/073500105000000063), [White 2000](https://doi.org/10.1111/1468-0262.00152).

### Exact adoption hypotheses and families

For metric k, test meaningful improvement directly:

`H0, k: E[L_candidate, k − 0.995 L_v5, k] ≥ 0`.

Reject only in favour of improvement exceeding **0.5%**. Testing zero improvement and then checking a 0.5% point estimate provides weaker assurance. Also require **2% non-inferiority** for both metrics in each registered complete year and each pooled season containing at least 90 eligible days. The year registry is **2021–2024 for CP-27 early**, **2025 for CP-27 later**, and **2021–2025 for CP-28 full-calendar**; all four pooled seasons are registered in each slice:

`H0, safety, k, g: E[L_candidate, k − 1.02 L_v5, k | g] ≥ 0`.

The 2% margin is an Owner judgement about acceptable local harm. Partial years are descriptive. A registered complete-year or season cell with fewer than 90 eligible days makes the gate inconclusive; it does not silently disappear. Sparse nonrequired regime cells remain descriptive. Non-significance of harm is not evidence of non-inferiority. Do not interpret a missing safety test as a passed test.

For each policy, form `p_policy = max(all required improvement and safety p-values)`. This is an intersection-union gate: every required endpoint must pass. Apply **Holm step-down across policy claims**, using the complete registered family, rather than a separate 5% test for each metric or model. A policy-level compound claim can use this maximum without an extra Bonferroni factor for its conjunctive endpoints; additional separate endpoint claims still need their own multiplicity accounting. [Holm 1979](https://www.jstor.org/stable/4615733).

CP-26 is a control-arm audit, with no fresh superiority claim and no data-chosen replacement of v5. CP-27 receives **α=0.025** across at most eight registered source packages. CP-28 receives **α=0.025** across all possible noncontrol policies: four other generations, up to eight source variants and two combinations, at most **14 hypotheses**. The union bound gives a nominal 5% developmental false-admission budget across these two families only for a fully registered universe and valid marginal tests. Reused development history prevents claiming that this bound covers the whole project search.

Before CP-26 results, freeze the source identities, transforms, algorithms and every reachable CP-28 policy, or a finite algorithmic specification that fully determines them from allowed training history. CP-28's family includes source variants even if CP-27 disqualifies them: they cannot silently vanish from the correction family. Use p=1 for a failed or unexecuted registered policy. An unregistered architecture, source union, tuning variant or second attempt cannot enter the current admission family. Retrospectively appending it to a correction does not make it eligible; any new research family must be specified before its results and remains development evidence. There is **one scheduled look per gate**, with no relaxed second-look rule or alpha recycling.

Romano–Wolf can gain power by exploiting dependence among tests, but requires correctly implemented joint bootstrap step-down inference. Keep it a secondary comparison with Holm, never an alternative gate chosen after results. Benjamini–Hochberg controls an expected false-discovery proportion rather than the probability of any false admission; it ranks lower for selecting one operational candidate, and its original independence guarantee is insufficient for arbitrary dependent policies. [Romano and Wolf 2005](https://doi.org/10.1111/j.1468-0262.2005.00615.x), [Benjamini and Hochberg 1995](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x).

### What could make this recommendation wrong

Strong nonstationarity, long dependence beyond 28 days, weak moments or sparse safety cells can invalidate or weaken the tests. Stratification and robustness checks expose rather than cure those problems. The compound safety gate may be too strict to admit small genuine gains; a null result is acceptable. If the Owner wants trade-offs between WIS and MAE, or a larger safety margin, that utility must replace the joint gate prospectively. The fresh 90-day assessment needs its own registered loss and dependence analysis; the long-history bootstrap setting is not automatically adequate for 90 days.

## Research question 4 Admitting new sources

### Ablation design and chronological gates

Use **add-one source packages against fixed v5**, with no other modelling change. A source package includes its transformations, missingness rules and logically inseparable inputs. Fix at most eight identities and their order by the registry, before results. Shared hyperparameter adaptation must follow the same registered training-only algorithm in the control and source arm; add-one assesses the resulting procedure, not an isolated causal effect of the raw feed.

Leave-one-out can reveal redundancy in a fixed combined feature set but does not establish the incremental value of adding a source to the control. Grouped ablation is preferable when feeds are inseparable. Source unions and a greedy forward search are excluded from the initial menu because they create extra policies. No automatic union of individually successful sources is admitted.

Use an **early admission slice, 2020-12-29–2024-12-31** (1,464 calendar days), and a **later confirmation slice, 2025-01-01–2026-04-07** (462 calendar days). Forecasts still cover every eligible day. Generate and seal the later outputs before opening early losses; do not inspect later labels or scores for source selection. After the early Holm gate at 2.5%, nominate **at most one source**: lowest early WIS among passers, then lower MAE, then registry order. Apply the later gate at 2.5%, with Holm accounting for **all eight potential source claims**, even though only the nominee can be admitted. The early and late conditions are conjunctive gates, not two alternative opportunities to pass.

This split provides a useful chronological stability check and reduces immediate tuning to the same scoring slice. It is not an untouched test: some later dates may already belong to the old folds, and the source family is a development choice. Mask and disclose that overlap. The single fresh test remains essential. Once the later result is seen, a failed nomination ends the admission attempt; no runner-up nomination or changed feature recipe is allowed. Publish the complete retrospective table afterwards as development evidence, retaining both gate results.

A source policy must issue forecasts on the whole eligible control calendar using a fixed **v5 fallback** when its inputs are unavailable. Do not delete difficult dates to make its sample look better. Require at least **364 days of active source use and 60 active days in each meteorological season** across the development calendar; otherwise label it insufficiently supported. Report source availability and performance both as a deployable policy including fallback and descriptively on active days. Control eligibility itself must be frozen independently of any source or candidate.

### Vintage tiers and delay sensitivity

| Tier | Main-evaluation rule | Required evidence and checks |
| --- | --- | --- |
| 1 | Original vintages with publication timestamps enter | Preserve values, origin, publication time, units, geography, revisions and retrieval provenance; enforce issue cutoff |
| 2 | Preserved original values with documented reconstructed availability may enter | Cite the historical release schedule, timezone/DST, latency assumptions and exceptions; explicitly mark the reconstructed timestamp |
| 3 | Revised values without original vintages do not enter | Separate research-only sensitivity, visibly labelled revision-contaminated; no source admission or candidate selection from its score |

For tier 2, move the assumed publication time later by **1, 6 and 24 hours** and rerun the full policy, including feature joins, training rows and daily refits. This tests the availability assumption, not a shift of the values' delivery timestamp. Previously unavailable inputs invoke the registered fallback; they are not carried backwards from a later release.

Require the source's nominal, +1-hour and +6-hour policies to pass the **0.5% joint-improvement gate**, and the +24-hour policy to pass **2% overall non-inferiority** to v5 on both metrics. Include these conjunctive endpoints inside the source-level maximum p-value, with the same early/late source family correction. Apply year/season safety endpoints to each mandatory delay policy. A documented timing uncertainty larger than 24 hours needs a source-specific worst-case delay registered in addition; failure at any delay inside the plausible uncertainty envelope blocks admission. Timing uncertainty without a defensible upper bound blocks tier-2 use.

This is deliberately strict. A source useful only if a reconstructed timestamp is accurate to minutes has fragile evidence. A known daily publication boundary can make a six-hour delay costly; that is evidence about deployability, not a reason to omit the check. The 24-hour check is a degradation safeguard, not a requirement that yesterday's feed retain the full incremental gain. None of these exact delays is a published universal rule.

Test tier 3 separately under the same chronological fitting and scoring definitions, comparing its revised-value variant with the permitted-vintage counterpart where one exists and otherwise with v5. Report optimism or degradation descriptively; revised data are not guaranteed to improve every model. No impressive tier-3 result upgrades the tier or supplies an input to a main combiner.

### Literature and risks

Real-time data research distinguishes the information vintage from the date an observation describes. Croushore and Stark construct snapshots to reproduce historical information sets; the timestamp alone cannot recover an original value. [Croushore and Stark 2001](https://doi.org/10.1016/S0304-4076(01)00072-0).

Stark and Croushore show that latest-available data can produce deceptively smaller MAE/RMSE and can change model specification. Croushore's survey reviews revisions' consequences for forecasting. Their macroeconomic setting supports the methodological warning, not a numerical correction factor for electricity inputs. [Stark and Croushore 2002](https://scholarship.richmond.edu/economics-faculty-publications/2/), [Croushore 2011](https://doi.org/10.1257/jel.49.1.72).

Holm addresses the finite tested family; it does not legitimize a source recipe revised after a near miss or an undocumented schedule chosen after losses. The chronological split sacrifices power and may expose a genuinely regime-specific source. If the Owner prioritizes learning rather than admission, full-period exploratory comparisons are reasonable, but must lose admission authority. The fresh test does not refund alpha or erase the development search.

## Research question 5 Walk forward combinations

### Recommended candidates and learning contract

Keep the five generations and eligible source variants in the frozen candidate universe. Add just **C1**, equal-weight quantile averaging of v1–v5, and **C2**, one learned convex quantile average of those same five generations. DDNN-2 alone is descriptive and is neither an eligible candidate nor a direct extra combiner member; its prescribed contribution inside v5 is retained.

For C2, require **364 earlier scored, jointly available out-of-sample days** before learning weights. Use the latest **728 eligible out-of-sample days**, or all available if between 364 and 728, and update daily. Fit one nonnegative simplex weight vector shared across all seven quantiles and all hours, minimizing mean daily WIS. Then deploy `w = 0.5 w_fitted + 0.5 (1/5, ..., 1/5)`. Resolve multiple minimizers by the solution nearest equal weights in Euclidean distance. Before burn-in, use C1. On combiner-solver failure use C1 only when all five member outputs are valid. If any member output is missing or invalid, use the already available v5 forecast, otherwise B0, as the explicitly registered operational fallback for C1/C2; record the failure and do not renormalize a subset of members. Score fallback days and report their count. Hard resource or forecast-contract breaches still make the affected policy ineligible. Do not retrospectively exclude these days.

The history requirement, finite learning window and 50% shrinkage are conservative design choices. Published DDNN-related QRA uses 182 prior out-of-sample days; that does not establish a sufficient universal minimum. One year here supplies seasonal experience and shrinkage limits unstable weights among correlated generations. [Marcjasz et al. 2023, methods](https://arxiv.org/pdf/2207.02832).

For each member forecast for earlier target day s, record the issue timestamp, training-target cutoff, preprocessing and tuning cutoffs, feature contract and input vintages. Its fit must have excluded s and later target days. A combiner for D may use it only after its verifying target has become available before D's issue cutoff. Future member refits may later train on s; they do not replace the originally stored forecast for s. Produce D's combined forecast before admitting D's target to the meta-training ledger.

Wolpert's stacking construction uses held-out base predictions. In this application, chronological order and publication availability add necessary restrictions: random cross-validation, fitted values, historical forecasts regenerated with later information or fits, and retrospectively optimized whole-period weights do not satisfy the contract. [Wolpert 1992](https://doi.org/10.1016/S0893-6080(05)80023-1).

### Quantile averaging linear pooling and QRA

Vincentization combines `qτ = Σj wj qj, τ`. Linear pooling combines `F = Σj wj Fj` and then inverts F; they are different operations. Shared nonnegative weights preserve quantile ordering when member quantiles are ordered. Vincentization works directly with this seven-quantile interface, while linear pooling requires a complete or reconstructed CDF and fixed tail assumptions. Neither guarantees calibration.

There is no universal winner. Gneiting and Ranjan give conditions under which a nontrivial linear pool is overdispersed; those conditions do not prohibit pooling underdispersed members. An EPF study by Uniejewski, Marcjasz and Weron reports distribution averaging generally outperforming quantile averaging for its particular forecasting construction. That conflict must remain visible. The recommendation here follows the interface, bounded complexity and leakage audit, not a claim of universal superior accuracy. [Gneiting and Ranjan 2013](https://doi.org/10.1214/13-EJS823), [Uniejewski et al. 2019](https://doi.org/10.1016/j.eneco.2018.02.007).

Original QRA regresses outcomes on members' **point forecasts** separately for each requested quantile. It is not the shared-weight convex quantile average proposed for C2. QRA can adjust location and spread but brings more parameters, redundant-predictor sensitivity and crossing risk. Regularized QRA and factor QRA address aspects of those problems. They rank next if the Owner accepts a larger pre-registered family. A QRA arm must fix scaling, predictor set, penalty-selection algorithm, intercept and crossing repair, and fit every component on earlier out-of-sample history. [Nowotarski and Weron 2015](https://doi.org/10.1007/s00180-014-0523-0), [Uniejewski and Weron 2021](https://doi.org/10.1016/j.eneco.2021.105121), [Maciejowska et al. 2016](https://doi.org/10.1016/j.ijforecast.2014.12.004).

Per-hour, per-block and regime-dependent weights rank lower because splitting a correlated forecast panel reduces effective sample size and expands policy choices. If included from the start, a bounded alternative is three fixed local-hour blocks **00–07, 08–15, 16–23**, at least **728 out-of-sample days**, common weights across quantiles and **75% shrinkage toward global weights**. It is excluded from the initial recommendation; a favourable hourly diagnostic cannot create it afterwards. Regional/DST handling must be identical to the primary contract.

### Selection and failure conditions

Apply CP-28's full-family Holm gate and required sensitivity/safety checks against fixed v5. Among qualifying policies, choose lowest full-calendar WIS, subject to MAE's gate. Define practical ties as relative WIS differences below **0.5%**. Among tied qualifying policies, use the fixed priority: original generations, the admitted source variant, C1, then C2; within the original-generation group prefer lower measured reference compute, then registry order. Compare every tie to the lowest-WIS qualifier, so chained pairwise ties cannot enlarge the tolerance. Such a tie-break is a decision rule, not a pairwise claim of superiority.

Only the at-most-one CP-27 admitted source variant may be selected, but all possible variants remain in CP-28's correction universe. If no alternative qualifies, retain v5 as the research candidate. This does not authorize changing the released v1 product. If v5 cannot satisfy vintage or operational requirements, the control must be resolved before the run; do not silently substitute a score-selected control.

C2 could overfit despite shrinkage, fail in rare regimes or improve WIS while harming p50. Shared weights can be too restrictive if members are complementary in particular hours. These risks justify a small family and an unopened later test; they do not justify retrospective weight-regime changes.

## Research question 6 Compute ceilings and refit evidence

### Evidence

Lago et al. report daily recalibration on an i7-6920HQ quad-core laptop: LEAR 1–10 seconds, a LEAR ensemble 20–25 seconds, DNN 2–5 minutes and a DNN ensemble 8–20 minutes. Multiplication by 1,926 gives **10.7–13.4 serial hours for the LEAR ensemble** and **256.8–642 hours for the DNN ensemble**. These are arithmetic extrapolations of that study, not measurements of this repository, LightGBM or NumPy DDNN-2. [Lago et al. 2021, §6.3 and Table 4](https://jesuslago.com/wp-content/uploads/1-s2.0-S0306261921004529-main-1.pdf).

A transferable percentage accuracy loss from weekly instead of daily refitting for these exact policies is **unverified**. The protocol keeps daily refits. Sparse hyperparameter-search recalibrations are not evidence for sparse outer refits. Daily fitting and daily distributional postprocessing also appear in Lipiecki et al.; their postprocessor learns from earlier out-of-sample forecasts. [Lipiecki et al. 2024, methods](https://arxiv.org/html/2404.02270v2).

### Recommended planning ceilings

The following are **proposed ceilings**, deliberately distinguishable from published timings. A reference worker has a maximum of **4 CPU threads and 16 GiB RAM** on one named Owner-approved machine; at most **2 concurrent workers**, no paid external compute and no new GPU allocation. A worker-hour is an hour of execution charged to one such worker, summed across jobs. Also record actual CPU core-hours, memory and wall-clock elapsed time; parallelism does not erase accounting.

| Unit inclusive of all its seeds members and quantiles | Per delivery-day ceiling | 1,926-day upper allowance before overhead |
| --- | --- | --- |
| One unique LEAR ensemble configuration | 60 seconds | 32.1 worker-hours |
| One unique complete LightGBM configuration | 300 seconds | 160.5 worker-hours |
| One unique complete neural ensemble configuration | 1,200 seconds | 642 worker-hours |
| One learned combiner fit on cached forecasts | 30 seconds | 16.05 worker-hours |

Freeze aggregate budgets of **CP-26: 1,400 worker-hours; CP-27: 2,500 worker-hours, at most 300 per source; CP-28: 150 worker-hours**. Reserve **20% within each total** for preprocessing, interval calibration, scoring and validation. Per-source and per-configuration limits do not entitle an arm to exceed the checkpoint total. Bootstrap and diagnostics are charged to that total.

The 300-hour source cap includes nominal and every mandatory delay variant, as well as allocated overhead; it can exclude expensive neural source packages. Before execution and before losses are opened, the unique-fit manifest must fit the 80% fitting reservation of each aggregate budget. Otherwise declare that package infeasible or obtain a prospectively ratified budget revision. Per-day caps are not guarantees that every registered configuration fits the aggregate allowance. These maximum envelopes may still be inappropriate for the Owner's desired elapsed time; they require ratification, not an inference from a paper.

Cache only identical member forecasts, keyed by training dates, as-of input vintages, features, hyperparameters, seeds, code identity and platform assumptions. v4/v5 reuse shared members; C1/C2 learn from the forecast ledger without rerunning base models. Different windows or source features are different fitting jobs. Record expected unique fits before execution so the ceilings are meaningful rather than applied to an unspecified ensemble.

A single ceiling breach marks the affected registered policy computationally failed, records the failure and blocks its admission; use p=1 in its family. The runtime fallback may preserve a complete daily ledger, but it does not turn a failed research arm into an eligible winner. The control's failure blocks acceptance for the checkpoint. Do not change to weekly fits, reduce seeds, skip dates or silently truncate neural epochs in response to a breach. Any restart or changed algorithm must be a new, prospectively budgeted policy; none is authorized by this memo.

A later checkpoint may perform a training-only timing pilot with scores sealed, once separately authorized. It can establish feasibility before an expensive run; it cannot tune the ceiling to tolerate favourable results. The memo's upper bounds could be too low for the existing implementation or unnecessarily high on newer hardware. That uncertainty is why hardware, generation seed counts, unique fits and actual budgets are Owner decisions.

## Protocol skeleton

`B` means a supplied brief constraint; `J` means a recommended judgement requiring ratification. Literature names identify the methodological support, not a source for every exact numeric setting.

| Parameter fixed before results | Recommended value or binding rule | Basis |
| --- | --- | --- |
| Target | Single DE-LU coupled day-ahead auction, hourly delivery prices | B |
| Issue | D−1 11:00 UTC, explicit target-D auction embargo; resolve summer interpretation | B; Kulakov; J |
| Time representation | Europe/Berlin delivery day, UTC hour key and duplicate-hour fold | B; J |
| Output | p50 equals q0.50; Q={.025, .10, .25, .50, .75, .90, .975} | B |
| Development calendar | Inclusive 2020-12-29–2026-04-07; 1,926 calendar days | B; calendar arithmetic |
| Eligibility | Frozen target completeness, information availability and reproducible control rules; no loss-based exclusions | Tashman; J |
| Missing target hours | Exclude incomplete day only by frozen target rule; report each excluded date and reason | J |
| Source/member missing inputs | Prespecified training-only imputation or fixed fallback; never remove a day selectively | J |
| Fit/output failure | Record it; operational fallback preserves ledger; policy fails eligibility if ceiling or contract breached | J |
| Old record | Retain five historical folds, definitions, 448-day mask, scores and old uncertainty unchanged | B |
| New reporting masks | All eligible; never previously scored; old-fold mask; no fresh-evidence claim | B; Diebold |
| Primary window | Last 728 calendar delivery days, D−728…D−1 | B; Marcjasz; J |
| Initial seed span | 2019-01-01–2020-12-28 | B; calendar arithmetic |
| Outer refits | Every eligible delivery day, all registered members | B; Lago |
| Expanding sensitivity | From 2019-01-01; secondary only, within frozen compute budget | J |
| Window averaging | Excluded initially; optional equal {56, 84,364,728} only if registered before results | Hubicka; J |
| CP-26 identities | v1–v5 as supplied, unchanged algorithms/features/blend weights | B |
| B0 | Existing similar-day naive procedure and seven-quantile contract frozen | B |
| Research control | v5 fixed before CP-26; v1 released-product comparator | J |
| DDNN-2 alone | Descriptive; never candidate or standalone direct combination member | B |
| Inner tuning | Existing deterministic training-only rules; any new grid/splits/objective/cadence/fits fixed explicitly | Tashman; J |
| Seeds and ensemble sizes | Preserve and explicitly enumerate existing generation values; no extra search seeds | B; J; identities require execution manifest |
| Preprocessing | Fit from admissible training information, row-origin predictor vintages | Croushore–Stark; J |
| Quantile crossing | Validate q order and finite outputs; preserve existing generation repair; any new repair frozen before run | J |
| MAE | Absolute p50 error | B |
| WIS | 50/80/95% intervals, α/2 interval and .5 median weights, denominator3.5 | B; Bracher |
| Primary aggregation | 1/H_D hourly mean within day, then equal eligible-day weight | J |
| B0 normalization | Ratio of overall mean daily losses, report raw losses beside it | B; J |
| Period weights | Primary day weights; equal four pooled seasons and five complete years secondary | J |
| CRPS/PIT | Exact forms excluded with seven quantiles; reconstruction requires common registered CDF/tails | Gneiting; Bracher |
| Calibration | Coverage, two tail rates, widths, seven hits, eight probability bins | Gneiting; Bracher |
| Diagnostic tests | Descriptive Christoffersen LR; separate coverage/lag1/lag7 moment Wald, HAC14, centered block null; tie-free cells,n≥180;100,000 reps,seed20261013; Holm5% over≤1,224 joint tests | Christoffersen; Holm; J |
| Seasons | DJF/MAM/JJA/SON | J |
| Years/quarters | Calendar; complete/partial labels; no full-year weight to partial periods | J |
| Hour/day types | Native hours; weekday/weekend; nationwide holiday flag; 23/24/25-hour day | J |
| Calendar stress | 2021-01-01–2022-12-31 and complement; descriptive historical label | B; J |
| Negative-risk flag | Any negative hour in latest7 fully known delivery days | J |
| Volatility state | SD of28 fully known daily means; above prior365-state p90; linear percentile, strict comparison | J |
| Outcome regimes | Descriptive only, no conditional-calibration nominal claim or admission power | Lerch |
| Resampling unit | Paired full native day, all policies/metrics/labels synchronized | Ziel–Weron; J |
| Primary bootstrap | Non-circular MBB, 14 calendar days, 10,000 reps, seed20261012 | Künsch; J |
| Bootstrap boundaries | Calendar-year strata;2020 joined to2021; no real-gap or early/late crossing | J |
| Bootstrap test | Centered studentized contrasts, Bartlett HAC lag14 within strata; +1 finite-replicate p rule | DM; block literature; J |
| Bootstrap sensitivities | 7/28 days and14-day unstratified chronological blocks; disagreement means inconclusive | J |
| Improvement margin | More than0.5% on both mean daily scores, tested against.995×v5 | B adapted; J |
| Safety margin | 2% NI on both scores; early years 2021–24, later 2025, full 2021–25 plus four pooled seasons; required cells<90 days are inconclusive | J |
| Compound gate | Maximum required endpoint p, then Holm across all policy claims | Holm; J |
| CP-26 claims | Development/control audit; no data-chosen control or fresh superiority claim | B; J |
| CP-27 family |≤8 frozen source packages, α=.025, full-family Holm | Holm; J |
| Source order | Registry order; no adaptive greedy addition | White; J |
| Source ablation | Add-one vs v5; groups only if inseparable and named; no unregistered unions | J |
| Admission calendar |2020-12-29–2024-12-31, 1,464 calendar days | J |
| Confirmation calendar |2025-01-01–2026-04-07,462 calendar days; old-fold overlap disclosed | J |
| Nomination |At most1 early passer; lowest WIS, then MAE, then registry order | J |
| Confirmation gate |Sameα=.025, account for all8 source claims; no second nominee after failure | Holm; J |
| Source support |≥364 active days and≥60 active days in each season; score all days with fixed fallback | J |
| Tier1 |Original values/vintages with timestamps; main analysis | B |
| Tier2 |Preserved original values; documented reconstructed availability and bounded uncertainty | B |
| Tier2 delays |+1/+6/+24h on availability; refit full policy; extra worst-case if uncertainty exceeds24h | J |
| Tier2 delay acceptance |Nominal/+1/+6 jointly improve.5%;+24 passes2% NI; required season/year checks; any plausible-delay failure blocks | J |
| Tier3 |Separate revised-value sensitivity; no main admission, selection or meta-inputs | B; Croushore |
| CP-28 finite menu |v1–v5, up to8 source variants, C1, C2;14 noncontrol hypotheses | J |
| CP-28 multiplicity |α=.025 Holm across every reachable alternative, including disabled/failed variants with p=1 | Holm; J |
| C1 |Equal convex quantile average of v1–v5 | Forecast-combination literature; J |
| C2 provenance |Earlier genuine member OOF forecasts and already available verifying targets only | Wolpert; B |
| C2 minimum/window |364 scored joint OOF days;latest728 eligible OOF days | J; DDNN context |
| C2 fit/update |Daily mean WIS minimization;global shared nonnegative simplex weights | J |
| C2 regularization |50% shrinkage toward equal weights;nearest-equal minimizer tie | J |
| C2 burn-in/failure | C1 for burn-in/solver failure with valid members; member failure uses v5 then B0; no partial-member average; days retained | J |
| QRA/pooling/block weights |Excluded initial menu;require all settings and family expansion before results | Nowotarski; Uniejewski; J |
| Candidate choice | Gate first,then minimum WIS; ties<.5% versus best prefer original generations,source,C1,C2; compute/registry within generation group | J |
| No passing alternative |Retain v5 research candidate;no requirement to win;live v1 release authority separate | B; J |
| Looks/alpha |One look per scheduled gate;no optional second look or alpha recycling | J |
| MCS |90%, T_R, 10,000 reps, same blocks, separate scores;descriptive | Hansen–Lunde–Nason; J |
| SPA/RC |SPA5% two-metric Holm global diagnostics;RC literature comparator | Hansen; White; J |
| GW |Secondary fixed-window test;constant, lag1 differential, weekend, negative-risk, volatility instruments | Giacomini–White; J |
| Refit ceilings |LEAR 60s, LightGBM 300s, neural 1200s, combiner 30s per complete configuration/day | Lago context; J |
| Machine/concurrency |Named machine;4CPU threads/16GiB worker;≤2 workers;no paid external compute | J |
| Checkpoint ceilings |CP-26 1400, CP-27 2500, CP-28 150 worker-hours;CP-27≤300/source | J |
| Overhead/accounting |20% reserved inside totals;unique fits, core-hours, RAM, elapsed time, caching keys recorded | J |
| Resource breach |Policy failed, p=1;control failure blocks acceptance;no weekly fallback or silent simplification | J |
| Fresh test |2026-04-08–2026-07-06, one frozen candidate, one opening;fresh statistical decision registered separately | B |
| Retraining replay |2026-07-07–2026-10-04;separate interpretation, never extends/tunes the first test | B |

## Published pitfalls and their protocol consequences

| Pitfall | Published example or demonstration | Consequence here |
| --- | --- | --- |
| Data snooping across many specifications | White's Reality Check formalizes comparison against the best result in a searched collection; Hansen's SPA shows why the universe and treatment of poor alternatives matter | Freeze every reachable policy, include failures, report all attempts; selected single-model p-values cannot stand in for the family |
| Regime hindsight | Lerch et al. demonstrate the forecaster's dilemma when evaluation selects extreme realized outcomes; Giacomini–Rossi examines forecast performance under instability | Calendar stress labels are descriptive; origin-known flags are frozen; outcome buckets do not determine admission |
| Selecting and claiming on the same days | Diebold 2015 distinguishes comparisons of forecasts from stronger model claims; the electricity forecasting review by Weron calls for common datasets and robust comparison | Old selections and re-evaluations stay developmental; chronological confirmation is qualified; only the unopened test assesses the frozen winner prospectively |
| Leaking combiner training | Wolpert constructs meta-training from held-out base forecasts; Lipiecki et al. train distributional postprocessors on earlier OOS forecasts | Store forecasts made without their targets, obey time order and publication cutoffs, never replace them by fitted values or forecasts regenerated using later information or fits |
| Correct timestamps but revised values | Croushore–Stark's vintage construction and Stark–Croushore's forecast evaluation show why latest-available histories differ from real-time histories | Tier2 reconstructs availability of original values;it never upgrades corrected histories from tier3 |

The stacking papers demonstrate the construction that prevents leakage; this memo does not allege that their authors leaked or report an invented measured leakage penalty. Likewise, the historical-control observations supplied by this brief are project facts, not empirical findings of the cited papers. [White](https://doi.org/10.1111/1468-0262.00152), [Hansen](https://doi.org/10.1198/073500105000000063), [Lerch et al.](https://doi.org/10.1214/16-STS588), [Giacomini–Rossi](https://doi.org/10.1002/jae.1177), [Diebold](https://doi.org/10.1080/07350015.2014.983236), [Weron](https://doi.org/10.1016/j.ijforecast.2014.08.008), [Wolpert](https://doi.org/10.1016/S0893-6080(05)80023-1).

## Open questions for the Owner

1. **Issue-time interpretation:** does 11:00 UTC define an intentionally restricted-information forecast that may be issued after summer auction publication, or must the product be pre-auction? The protocol cannot make both claims without resolving the historical clock.
2. **Research control:** ratify v5 as the CP-27/28 comparator while v1 remains the released product. Confirm feasibility under the vintage standard before choosing by scores.
3. **Utility and margins:** ratify daily weighting, strict joint improvement, 0.5% practical gain and2% local NI. These are utility choices; literature cannot determine the acceptable trade-off or opportunity cost of an inconclusive result.
4. **Source family:** identify at most eight packages and all transformations before CP-26 results; accept at most one admission and no automatic union, or register a larger finite universe and its cost in advance.
5. **Chronological confirmation:** accept the proposed462-day development confirmation with explicit prior-fold overlap, or use only a pre-fixed previously unscored subset at the cost of less seasonal support. Neither becomes a fresh test by relabelling it.
6. **Tier2 risk tolerance:** ratify the1/6/24-hour gates and require a documented maximum timing uncertainty. Sources with ambiguous corrected values cannot enter regardless of delay tolerance.
7. **Combiner complexity:** start with C1/C2, or pay for additional pre-registered QRA, pooling, window or block-weight policies. Their recipes must precede the losses that might motivate them.
8. **Hardware and maximum elapsed time:** ratify the resource envelope or replace it before execution. Existing seed counts, unique-fit counts and exact machine identity must be supplied in the execution manifest; they cannot be inferred from this research brief.
9. **Fresh-test terminal rule:** ratify its separate hypotheses, margins, small-sample dependence treatment, operational failures and one-opening procedure before any closed-period inspection. The replay must not rescue a failed first test.

## References and verification

Bibliographic identities and DOI strings below were checked against publisher, author or institutional records in this research session. Detailed methodological claims use available original papers or authors' preprints. Where access was limited, the limitation is stated; no quantitative result is reconstructed from memory. The weekly-versus-daily accuracy penalty for this project's exact policies remains **unverified**. No later DE-LU empirical study is used.

1. **Lago, J., Marcjasz, G., De Schutter, B., and Weron, R. (2021).** Forecasting day-ahead electricity prices: A review of state-of-the-art algorithms, best practices and an open-access benchmark. *Applied Energy, 293*, 116983. DOI: [10.1016/j.apenergy.2021.116983](https://doi.org/10.1016/j.apenergy.2021.116983). [Author-hosted full text](https://jesuslago.com/wp-content/uploads/1-s2.0-S0306261921004529-main-1.pdf).
2. **Weron, R. (2014).** Electricity price forecasting: A review of the state-of-the-art with a look into the future. *International Journal of Forecasting, 30*(4), 1030–1081. DOI: [10.1016/j.ijforecast.2014.08.008](https://doi.org/10.1016/j.ijforecast.2014.08.008).
3. **Nowotarski, J., and Weron, R. (2018).** Recent advances in electricity price forecasting: A review of probabilistic forecasting. *Renewable and Sustainable Energy Reviews, 81*, 1548–1568. DOI: [10.1016/j.rser.2017.05.234](https://doi.org/10.1016/j.rser.2017.05.234).
4. **Tashman, L. J. (2000).** Out-of-sample tests of forecasting accuracy: an analysis and review. *International Journal of Forecasting, 16*(4), 437–450. DOI: [10.1016/S0169-2070(00)00065-0](https://doi.org/10.1016/S0169-2070(00)00065-0).
5. **Marcjasz, G., Serafin, T., and Weron, R. (2018).** Selection of Calibration Windows for Day-Ahead Electricity Price Forecasting. *Energies, 11*(9), 2364. DOI: [10.3390/en11092364](https://doi.org/10.3390/en11092364).
6. **Hubicka, K., Marcjasz, G., and Weron, R. (2019).** A Note on Averaging Day-Ahead Electricity Price Forecasts Across Calibration Windows. *IEEE Transactions on Sustainable Energy, 10*(1), 321–323. DOI: [10.1109/TSTE.2018.2869557](https://doi.org/10.1109/TSTE.2018.2869557). Identity, abstract and author-hosted extract verified; publisher full text was inaccessible.
7. **Ziel, F., and Weron, R. (2018).** Day-ahead electricity price forecasting with high-dimensional structures: Univariate vs.multivariate modeling frameworks. *Energy Economics, 70*, 396–420. DOI: [10.1016/j.eneco.2017.12.016](https://doi.org/10.1016/j.eneco.2017.12.016). [Author paper, including DM formulation](https://arxiv.org/html/1805.06649).
8. **Diebold, F. X., and Mariano, R. S. (1995).** Comparing Predictive Accuracy. *Journal of Business & Economic Statistics, 13*(3), 253–263. DOI: [10.1080/07350015.1995.10524599](https://doi.org/10.1080/07350015.1995.10524599).
9. **Diebold, F. X. (2015).** Comparing Predictive Accuracy, Twenty Years Later: A Personal Perspective on the Use and Abuse of Diebold–Mariano Tests. *Journal of Business & Economic Statistics, 33*(1), 1–9. DOI: [10.1080/07350015.2014.983236](https://doi.org/10.1080/07350015.2014.983236).
10. **Giacomini, R., and White, H. (2006).** Tests of Conditional Predictive Ability. *Econometrica, 74*(6), 1545–1578. DOI: [10.1111/j.1468-0262.2006.00718.x](https://doi.org/10.1111/j.1468-0262.2006.00718.x).
11. **Giacomini, R., and Rossi, B. (2010).** Forecast comparisons in unstable environments. *Journal of Applied Econometrics, 25*(4), 595–620. DOI: [10.1002/jae.1177](https://doi.org/10.1002/jae.1177).
12. **Hansen, P. R., Lunde, A., and Nason, J. M. (2011).** The Model Confidence Set. *Econometrica, 79*(2), 453–497. DOI: [10.3982/ECTA5771](https://doi.org/10.3982/ECTA5771).
13. **Hansen, P. R. (2005).** A Test for Superior Predictive Ability. *Journal of Business & Economic Statistics, 23*(4), 365–380. DOI: [10.1198/073500105000000063](https://doi.org/10.1198/073500105000000063).
14. **White, H. (2000).** A Reality Check for Data Snooping. *Econometrica, 68*(5), 1097–1126. DOI: [10.1111/1468-0262.00152](https://doi.org/10.1111/1468-0262.00152).
15. **Romano, J. P., and Wolf, M. (2005).** Stepwise Multiple Testing as Formalized Data Snooping. *Econometrica, 73*(4), 1237–1282. DOI: [10.1111/j.1468-0262.2005.00615.x](https://doi.org/10.1111/j.1468-0262.2005.00615.x).
16. **Holm, S. (1979).** A Simple Sequentially Rejective Multiple Test Procedure. *Scandinavian Journal of Statistics, 6*(2), 65–70. [Publisher archive](https://www.jstor.org/stable/4615733). No DOI identified in the verified archive record.
17. **Benjamini, Y., and Hochberg, Y. (1995).** Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing. *Journal of the Royal Statistical Society: Series B, 57*(1), 289–300. DOI: [10.1111/j.2517-6161.1995.tb02031.x](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x).
18. **Künsch, H. R. (1989).** The Jackknife and the Bootstrap for General Stationary Observations. *The Annals of Statistics, 17*(3), 1217–1241. DOI: [10.1214/aos/1176347265](https://doi.org/10.1214/aos/1176347265).
19. **Politis, D. N., and Romano, J. P. (1994).** The Stationary Bootstrap. *Journal of the American Statistical Association, 89*(428), 1303–1313. DOI: [10.1080/01621459.1994.10476870](https://doi.org/10.1080/01621459.1994.10476870).
20. **Gneiting, T., and Raftery, A. E. (2007).** Strictly Proper Scoring Rules, Prediction, and Estimation. *Journal of the American Statistical Association, 102*(477), 359–378. DOI: [10.1198/016214506000001437](https://doi.org/10.1198/016214506000001437).
21. **Bracher, J., Ray, E. L., Gneiting, T., and Reich, N. G. (2021).** Evaluating epidemic forecasts in an interval format. *PLOS Computational Biology, 17*(2), e1008618. DOI: [10.1371/journal.pcbi.1008618](https://doi.org/10.1371/journal.pcbi.1008618). Correction (2022), *18*(10), e1010592, DOI: [10.1371/journal.pcbi.1010592](https://doi.org/10.1371/journal.pcbi.1010592).
22. **Gneiting, T., Balabdaoui, F., and Raftery, A. E. (2007).** Probabilistic forecasts, calibration and sharpness. *Journal of the Royal Statistical Society: Series B, 69*(2), 243–268. DOI: [10.1111/j.1467-9868.2007.00587.x](https://doi.org/10.1111/j.1467-9868.2007.00587.x).
23. **Christoffersen, P. F. (1998).** Evaluating Interval Forecasts. *International Economic Review, 39*(4), 841–862. DOI: [10.2307/2527341](https://doi.org/10.2307/2527341). [Original paper in university archive](https://users.ssc.wisc.edu/~bhansen/718/Christoffersen1998.pdf).
24. **Nowotarski, J., and Weron, R. (2015).** Computing electricity spot price prediction intervals using quantile regression and forecast averaging. *Computational Statistics, 30*, 791–803. DOI: [10.1007/s00180-014-0523-0](https://doi.org/10.1007/s00180-014-0523-0).
25. **Uniejewski, B., and Weron, R. (2021).** Regularized quantile regression averaging for probabilistic electricity price forecasting. *Energy Economics, 95*, 105121. DOI: [10.1016/j.eneco.2021.105121](https://doi.org/10.1016/j.eneco.2021.105121).
26. **Maciejowska, K., Nowotarski, J., and Weron, R. (2016).** Probabilistic forecasting of electricity spot prices using Factor Quantile Regression Averaging. *International Journal of Forecasting, 32*(3), 957–965. DOI: [10.1016/j.ijforecast.2014.12.004](https://doi.org/10.1016/j.ijforecast.2014.12.004).
27. **Marcjasz, G., Narajewski, M., Weron, R., and Ziel, F. (2023).** Distributional neural networks for electricity price forecasting. *Energy Economics, 125*, 106843. DOI: [10.1016/j.eneco.2023.106843](https://doi.org/10.1016/j.eneco.2023.106843). Methods verified against [authors' preprint](https://arxiv.org/pdf/2207.02832).
28. **Lipiecki, A., Uniejewski, B., and Weron, R. (2024).** Postprocessing of point predictions for probabilistic forecasting of day-ahead electricity prices: The benefits of using isotonic distributional regression. *Energy Economics, 139*, 107934. DOI: [10.1016/j.eneco.2024.107934](https://doi.org/10.1016/j.eneco.2024.107934). [Authors' methods](https://arxiv.org/html/2404.02270v2).
29. **Uniejewski, B., Marcjasz, G., and Weron, R. (2019).** On the importance of the long-term seasonal component in day-ahead electricity price forecasting: Part II—Probabilistic forecasting. *Energy Economics, 79*, 171–182. DOI: [10.1016/j.eneco.2018.02.007](https://doi.org/10.1016/j.eneco.2018.02.007). Comparative pooling conclusion verified in publisher abstract.
30. **Gneiting, T., and Ranjan, R. (2013).** Combining predictive distributions. *Electronic Journal of Statistics, 7*, 1747–1782. DOI: [10.1214/13-EJS823](https://doi.org/10.1214/13-EJS823).
31. **Wolpert, D. H. (1992).** Stacked generalization. *Neural Networks, 5*(2), 241–259. DOI: [10.1016/S0893-6080(05)80023-1](https://doi.org/10.1016/S0893-6080(05)80023-1).
32. **Lerch, S., Thorarinsdottir, T. L., Ravazzolo, F., and Gneiting, T. (2017).** Forecaster's Dilemma: Extreme Events and Forecast Evaluation. *Statistical Science, 32*(1), 106–127. DOI: [10.1214/16-STS588](https://doi.org/10.1214/16-STS588).
33. **Croushore, D., and Stark, T. (2001).** A real-time data set for macroeconomists. *Journal of Econometrics, 105*(1), 111–130. DOI: [10.1016/S0304-4076(01)00072-0](https://doi.org/10.1016/S0304-4076(01)00072-0). [Full text](https://bfi.uchicago.edu/wp-content/uploads/1.pdf).
34. **Stark, T., and Croushore, D. (2002).** Forecasting with a real-time data set for macroeconomists. *Journal of Macroeconomics, 24*(4), 507–531. DOI: [10.1016/S0164-0704(02)00062-9](https://doi.org/10.1016/S0164-0704(02)00062-9). [Author's institutional record](https://scholarship.richmond.edu/economics-faculty-publications/2/).
35. **Croushore, D. (2011).** Frontiers of Real-Time Data Analysis. *Journal of Economic Literature, 49*(1), 72–100. DOI: [10.1257/jel.49.1.72](https://doi.org/10.1257/jel.49.1.72). Publisher abstract and identity verified; full publisher text was inaccessible.
36. **Kulakov, S. (2020).** X-Model: Further Development and Possible Modifications. *Forecasting, 2*(1), 20–35. DOI: [10.3390/forecast2010002](https://doi.org/10.3390/forecast2010002).
37. **Fridgen, G., Michaelis, A., Rinck, M., Schöpf, M., and Weibelzahl, M. (2020).** The search for the perfect match: Aligning power-trading products to the energy transition. *Energy Policy, 144*, 111523. DOI: [10.1016/j.enpol.2020.111523](https://doi.org/10.1016/j.enpol.2020.111523).

## Local handover

Only this new report is an intended repository change. No branch, worktree, tag, commit or retained temporary artifact was created; nothing was staged or published. Suggested commit message for Owner review: `docs: add Stage 4 forecasting evaluation methodology memo`.

Interview-answer trigger for the Orchestrator: why broader historical coverage does not turn selected development evidence into confirmation, and why availability timestamps cannot rehabilitate revised input values. The research agent files no interview entry.
