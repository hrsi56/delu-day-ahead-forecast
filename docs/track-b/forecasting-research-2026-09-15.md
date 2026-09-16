# Research decision memo — improving DE-LU forecasting

**2026-09-15 · Orchestrator · research proposal, not a ratified plan or engineering brief.**

**Status after owner authorization:** this memo preserves the research that preceded v21.
The current execution authority is [capstone_v21.md](../../capstone_v21.md), with its fixed
CP-15 comparison and product criteria; proposals below do not add methods to that brief.

Owner instruction: improve predictive quality and demonstrate feasibility; 32% or 40% coverage
of a nominal 95% interval is inadequate. Consider a substantial change of approach.
This memo supersedes the recommendation to make landing/freezing the next programme action.
It does not change CP-10's historical PASS, dispose of its branch, or amend an anchor.

## Recommendation

Test an **adaptive forecasting policy**: estimate the current price level and scale, forecast
departures from that level using market inputs, combine complementary models, and update
uncertainty using errors that have become available. The policy includes its prescribed
retraining and state updates. Its predictions, not just a separate frozen model's predictions,
must eventually be evaluated prospectively.

The first priority is the centre of the distribution. The next priority is reliable, useful
intervals around it. A larger neural model and a market-mechanism model both deserve bounded
challenger experiments; neither should be declared the answer before comparison.

**No new model was trained in this research.** The findings below justify experiments, not a
claim that we have achieved good forecasting or know its achievable maximum.

## 1. What CP-10 actually establishes

Source: the [committed CP-10 report](../../reports/cp10/report.md) on
`gauntlet/cp-10`, candidate `ad3e1a5d5e42d70ea95bbffd01b4563eb2d6d803`, preserved through
evidence tip `4039ce24150b36ea233b043061e68eb2be78cbbe`. The relative link resolves in the primary CP-10-based checkout; the SHAs identify the
evidence independently of that path. The older main-based review worktree does not contain CP-10.

| Reported measurement | v1 | Selected C1 volatility |
|---|---:|---:|
| Full fold 3 median MAE, EUR/MWh | 140.992852 | 141.007963 |
| Full fold 3 nominal 95% coverage | 55.54% | 71.73% |
| August 15–31 nominal 95% coverage | 19.36% | 32.11% |
| Selection-fold pooled mean pinball | 4.466576610 | 4.385529024 |

The report explicitly says the raw model was not refit. Median changes are only small effects
of the final quantile projection. Thus CP-10 did not materially repair the price forecast.
Selecting C1 head spread retrospectively because its peak coverage is 44.12% would neither
respect the original comparison nor satisfy the product objective.

The ACI experiment was also deliberately narrow: a fixed initial residual-score reservoir and
gamma from 0.000001 to 0.00002 per hourly feedback event. The report says it did not test rapid
adaptation or a rolling reservoir. At the largest gamma, even continuous misses would require
about 2,106 hourly updates to move its internal coverage-state parameter from 0.95 to 0.99:
`(0.99 - 0.95) / (0.00002 * 0.95)`. That is about 88 complete 24-hour days, plus release delay.
This is a calculation from the reported update rule, **not** a claim about actual coverage.

**Inference:** this is negative evidence about a specific postprocessing design, not evidence
that adaptive forecasting cannot work. Neither an Engineer implementation error nor success of
an untested replacement follows. CP-10's tests and binding verdict remain intact.

## 2. Research with a plausible connection to this failure

These are primary papers, including explicitly identified recent preprints. Published
improvements use different data, inputs, cutoffs and comparators. Their percentages are not
additive and cannot be transplanted to our backtest.

### A. Adapt the target's level and scale — first priority

Sebastián, González-Guillén and Juan evaluated adaptive standardization on German prices with
an actual **January 2022–May 2023 test period**. Their best conventional LEAR had MAE 28.54;
the best adaptive version had 25.65 EUR/MWh. Models were refit daily. This is unusually relevant
to our regime-shift problem. Their recipe also filters training outliers; that choice needs its
own ablation, and never licenses removing extreme evaluation outcomes.
[Paper, §§4.2–4.5, Tables 1–2](https://arxiv.org/html/2311.02610v3).

Proposed formulation: `forecast price = estimated current level + current scale × forecast residual`.
Every training row must use a level and scale available at that row's historical forecast origin.
Preserve an unnormalized challenger: transformation can remove useful information or lag a shock.

### B. Forecast the changing trend instead of copying it

Chęć, Uniejewski and Weron tested trend-seasonal decomposition on Germany and Spain over
2019–2023. For Germany, their combined extrapolated LEAR variant reports MAE 13.820 versus
14.761 for undecomposed LEAR. Crucially, they extend the series with **forecasts**, not future
observations, before estimating the target-day trend. This supports a separate, causally
estimated level component; it does not justify decomposition fitted to the complete dataset.
[Paper, §§3.5–4.1, Table 1](https://arxiv.org/html/2503.02518v1).

### C. Revisit online uncertainty after improving the forecast

AgACI aggregates ACI experts with different adaptation rates and was demonstrated on
day-ahead electricity prices. It directly addresses sensitivity to one learning rate.
[Zaffran et al., ICML 2022](https://proceedings.mlr.press/v162/zaffran22a.html).
Conformal PID models the evolving error scores themselves; its applications include electricity
**demand**, not a demonstration on our German price crisis.
[Angelopoulos, Candès and Tibshirani](https://arxiv.org/abs/2307.16895).

Proposed comparison: rolling scaled residual calibration versus AgACI; retain PID as a further
challenger if score drift remains. Define delayed feedback, finite-rank failures, cold starts,
and recovery before execution. Raising gamma alone does not resolve the fixed reservoir's tail
limitation. No claim of guaranteed narrow intervals during arbitrary shocks or of per-day 95%
coverage follows from long-run online calibration results.

### D. A neural challenger should use external market inputs

NBEATSx was designed to incorporate exogenous variables and evaluated specifically for
electricity prices. Its authors report improvements up to 5% against established specialist
methods. That makes a small exogenous neural model a useful challenger after strong baselines,
not a reason to launch a large architecture search.
[Olivares et al., paper and author-code link](https://arxiv.org/abs/2104.05522).

### E. Foundation models merit a fair test, not a presumption

A May 2026 Belgian preprint tests 2024 day-ahead prices. Its table reports MAE 12.43 for
Chronos-2 with covariates versus 13.22 for its ML ensemble; the combined model reaches 12.30.
The authors report that the combined model's improvement over the ML ensemble is **not
statistically significant**, and discuss extreme-price weaknesses. They disclose context-length
experimentation, so this is motivation for a strictly separated local comparison.
[Bui et al., §§IV.A–IV.C](https://arxiv.org/html/2605.17045v1).

A July 2026 preprint finds covariate-supported Chronos-2 and a specialist model complementary
on its GridStatus2025 benchmark: MAEs 4.105 and 4.202, versus 3.922 for their ensemble. This is
not a German-crisis result. It explicitly addresses pretraining contamination.
[Pan and Ezzat, §§2–3](https://arxiv.org/html/2607.02623v1).

Proposal: one pinned Chronos-2 challenger with the same eligible inputs and forecast origin.
Historical 2022 performance from a pretrained model cannot by itself prove generalization;
record the training-data uncertainty and require future, timestamped forecasts for confirmation.
Do not silently feed it target-day actuals in place of forecasts or compare unequal horizons.

### F. The deeper structural alternative: a learned merit-order model

Ghelasi and Ziel combine generation costs and capacities with learned parameters. On Germany's
October 2023–October 2024 test, they report MAE 15.23 versus 19.56 for their econometric expert;
a mixed ensemble achieves 12.49. The study **does not test the August 2022 crisis out of sample**.
Its fuel and EUA inputs came from paid Refinitiv data. This supports a structural challenger,
conditional on usable input history, not an immediate open-data reproduction claim.
[Paper, §4, §5.1 and Data Availability](https://arxiv.org/html/2501.02963v1).

Proposed direction: use forecast demand minus forecast wind and solar, available generation and
generation-cost information to estimate the marginal supply price; learn remaining forecasting
errors statistically. This could respond to changed inputs beyond historical price ranges.
Its weaknesses include missing or revised inputs, market coupling, outages and bidding behaviour.

### G. Better information can matter more than a larger model

A 2026 Applied Energy paper reports gains using prices from earlier-publishing markets to
forecast Belgium and Sweden. Its reported German prices are **inputs**, not proof of an equally
available leading signal for DE-LU. We should investigate cross-border forecasts and lagged
prices, while verifying actual publication times. A price from the same coupled auction may
arrive too late for our forecast and cannot be treated as a valid predictor by analogy.
[Mascarenhas et al.](https://www.sciencedirect.com/science/article/pii/S0306261925018070).

## 3. Proposed experiment sequence

This is a research recommendation. Engineering owns implementation under a subsequent brief.
Keep the existing report immutable and give every new result a new research identity.

| Stage | Bounded comparison | Question it resolves |
|---|---|---|
| 0 — diagnosis and information | Daily and hourly signed errors, level/shape error decomposition, upper/lower misses, interval widths; feature availability at issuance | Is the failure principally stale level, daily shape, uncertainty scale, or missing information? |
| 1 — adaptive point forecasts | Existing references; rolling LEAR; same LEAR with causal level/scale normalization; rolling boosted model with and without that transformation | How much is gained by representation and updating rather than architecture? |
| 2 — complementary models | Equal-weight short/long-window ensemble; a prescribed adaptive-weight alternative; one exogenous neural challenger and one Chronos-2 challenger | Does model diversity improve held-forward accuracy and crisis recovery? |
| 3 — predictive distribution | Quantile models/ensemble plus rolling scaled residuals; AgACI alternative; PID only if residual drift warrants it | Can intervals approach nominal coverage while retaining useful width? |
| 4 — structural challenger | Learned merit order plus residual correction, conditional on a verified feature/data feasibility sheet | Is information about current generation economics worth the additional complexity? |

Start stages 0–1 with current admissible historical inputs. Do the structural data feasibility
assessment early, so an unavailable input does not consume a full implementation effort.
Before model selection, freeze the candidate list, small hyperparameter budgets, training windows,
validation boundaries, random seeds and elimination rule. Evaluate all retained candidates on
identical target hours and available information. Measure runtime on the actual machine;
research-paper runtimes are not a local compute estimate.

Use a simple mean ensemble as the control for learned weights. Fit weights only from earlier
out-of-sample predictions. Include a recent signed-error correction as an explicit ablation;
report whether a complex model adds value after that simple correction. Retain ordinary-period
experts so rapid adaptation does not automatically erase useful seasonal history.

For new inputs, record **publication time and revision vintage**, not just delivery timestamp.
The existing plan reports fixed-lead weather only from 2024; such data cannot establish a 2022
improvement. Reanalysis is not a substitute for archived forecasts. Current outage archives do
not automatically reconstruct what was known before an old auction. Paid fuel access and rights
remain unestablished; no token implies that those datasets or permissions exist.

## 4. What counts as a good forecast

The product target remains a nominal **95% interval that behaves near 95%**, alongside accurate
point forecasts. A 40% target has no defensible relationship to that label.

Coverage alone is insufficient. Weighted interval score (WIS) combines interval width and
penalties for misses across levels, along with median error. It makes huge intervals costly.
Report its components, 50/80/95% coverage, and mean/median/tail widths in EUR/MWh.
[Bracher et al., score definition and interpretation](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008618).

**Provisional feasibility objectives, proposed here rather than inherited from a paper:**

- At least **10% lower overall MAE and WIS than the strongest predeclared reference**, not merely
  the weakest naive or v1 model. Report absolute errors and confidence intervals as well.
- Nominal 95% coverage approximately **90–98% overall** as an initial screening band, with an
  explicit aim of calibration near 95%. Also inspect predeclared stress blocks separately:
  ordinary days must not conceal another collapse. This band is not a statistical guarantee.
- Select on predictive loss subject to reliability and a predeclared material-regression limit
  for stress periods; report every candidate that improves one dimension while worsening another.
- Show how rapidly signed bias, interval misses and width recover after a level shift. Report
  first-shock days separately, without removing them from aggregate results.
- Measure failure/stale-forecast frequency and runtime. A system that cannot issue before its
  declared cutoff has not met the forecasting task.

The numerical screening objectives need formal specification before experiments. A universal
EUR/MWh usefulness threshold cannot be inferred without a particular product decision; relative
skill, absolute error and width should therefore all be visible. Coverage on 408 hourly outcomes
is not 408 independent coin flips: uncertainty analysis must preserve daily/serial dependence.
For a 17-day stress window, show exact counts and a day-block uncertainty analysis rather than
pretending a one-percentage-point difference is decisive.

Use chronological rolling evaluation with tuning strictly inside earlier data. The already seen
2022 episode can now inform **explicitly exploratory** development, but cannot become a fresh
confirmatory test. Do not reopen the spent v1 holdout to choose models. A final prospective
evaluation uses a fixed policy and fresh future forecasts; historical gains remain development
evidence. Define stress diagnostics before comparing challengers and never supply hindsight
crisis dates as model features.

## 5. The required paradigm change in the programme

Original v20 freezes weights for the confirmatory model while the daily retrained model supplies
no scientific result. That does not directly establish the forecasting quality of the adaptive
product now requested. The proposed alternative is to freeze **the forecasting policy**:

- Code, data contract, model families, hyperparameters, initial state and update schedule.
- A causal rule for consuming newly available prices and forecast errors, including delay.
- An immutable record of each issued forecast, input vintage, model/state fingerprint and time.
- Predeclared evaluation horizon, metrics and acceptance criteria, with no discretionary tuning
  during the confirmatory run. Prescribed updates continue; changes to the policy start a new run.
- Exact registry versions and fingerprints for initial artifacts and sufficient state lineage
  to reconstruct subsequent forecasts. Preserve the registry-loading correction already drafted.

**This is a proposal to replace a constraint, not silently work around it.** It requires a
subsequent authorized anchor amendment. No anchor was edited during this research.
The new engineering brief must retain a fresh independent Integration verdict bound to its final
candidate. CP-3B's unmet item 6 is not a precedent.

## 6. Decision and limits

Recommend the adaptive target/ensemble path as the first implementation experiment, with
Chronos-2 as a challenger and structural data feasibility investigated alongside the design.
If simple causal level correction removes much of the crisis error, invest in shape and
uncertainty. If it does not, inspect available leading information before spending on a larger
network. If structural inputs are feasible, compare the hybrid directly on the same backtest.

No method can infer an unobserved shock merely because we demand accurate forecasting.
The practical goal is to use information promptly, recover when evidence arrives, and quantify
remaining uncertainty. The evidence supports pursuing substantially better forecasts; it does
not establish an attainable error floor or promise 95% coverage on every future crisis.

This research read engineering reports, not implementation source or tests. It made no new
engineering verification claim, retrieved no secrets, launched no executor, trained no model,
and changed no Engineer artifact or ref. The CP-10 branch remains open pending owner disposition.
