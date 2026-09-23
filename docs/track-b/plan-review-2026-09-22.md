# Programme-plan review — 2026-09-22

**Phase 1 critique, recorded before the plan rewrite.** Reviewed input:
`docs/track-b/v3-plan-handoff-2026-09-22.md` (644 lines, 6,056 words).
Role: bounded programme-planning reviewer under the Orchestrator planning router,
with the Owner's explicit read-only analysis and two-document deliverable authority.
No checkpoint execution, policy ratification, reserved-tail scoring, governance edit,
Q&A entry, publication, branch, worktree, tag or commit is authorized or performed.
Existing dirty files are outside this review's edits.

**Verdict: do not execute the received plan.** Its measured motivation is useful, but
it turns restricted experiments into impossibility claims and proposes a release without
an authorized acceptance/release route. Prioritize an archive admission check and a
precisely specified v2 experiment; do not abandon crisis evaluation on the archive claim.

## Verification gate — PASS

Independently calculated from `reports/cp15/predictions.parquet`, without importing the
project's metric implementation. SHA256:
`1a606d613ba5f6af82712a7e44adcaf639ba0ece1b7865f407f559fafafeda92`.
All arms have the identical 10,747 targets and truth; fold counts are
2,160 / 2,159 / 2,112 / 2,160 / 2,156, on 448 represented days.

`S_MAE = mean_f(mean_i |y-p50| / MAE(B0,f))`. WIS uses the seven emitted
quantiles, median weight 0.5, interval weights alpha/2 for alpha .5/.2/.05,
and divisor 3.5; S_WIS is the corresponding equal-fold ratio.

| Arm | Published S_MAE / S_WIS | Independent S_MAE / S_WIS | Verdict |
|---|---|---|---|
| B0 | 1.00000 / 1.00000 | 1.00000000 / 1.00000000 | REPRODUCED |
| B2 | 0.65781 / 0.63899 | 0.65781091 / 0.63899104 | REPRODUCED |
| A1 | 0.67229 / 0.64602 | 0.67229081 / 0.64601509 | REPRODUCED |
| A2 | 0.77371 / 0.73167 | 0.77371353 / 0.73166801 | REPRODUCED |

## Pass A — Are the claims true?

### A1. §5.2: a restricted combination optimum, not an information ceiling

Solve the convex L1 problem exactly by LP over emitted p50 vectors B1/B2/B3/A1/A2/A4.
Minimize `sum_i c_i*t_i`, with `c_i=1/(5*n_fold*MAE_B0_fold)`,
`t_i >= ±(X_i*w-y_i)`, `w>=0`, `sum(w)=1`. The objective is the actual S_MAE.
Separate solves define the per-fold, per-hour and fold×hour variants.

| Combination | Author | Review | Verdict |
|---|---:|---:|---|
| Six-arm mean | 0.67136 | 0.67136167 | REPRODUCED |
| Static convex oracle | 0.63744 | **0.63543811** | REPRODUCED WITH DEVIATION |
| Per-fold convex oracle | 0.62472 | 0.62472363 | REPRODUCED |
| Per-hour convex oracle | 0.63015 | **0.62633976** | REPRODUCED WITH DEVIATION |
| Per-row discrete selection | 0.33445 | 0.33445261 | REPRODUCED |
| Fold×hour convex oracle | not given | 0.60406592 | Additional diagnostic |
| Per-row convex oracle | not given | **0.27245319** | Counterexample to “no weighting scheme” |
| Criterion-1 limit | 0.59203 | 0.90×0.65781091 = 0.59202982 | REPRODUCED |

Static weights in the arm order above are
0.03599364 / 0.47846095 / 0.05453484 / 0.30789722 / 0.10668956 / 0.01642379.
Optimizing *pooled* MAE and then reporting S_MAE gives 0.63742459 static and
0.63010852 per-hour, close to the author's numbers. This is evidence of a likely
objective mismatch, not proof of the unavailable original implementation.

None of the tested restricted fixed partitions clears 0.59203. That supports a
small expected payoff from those particular combinations. It does **not** bound
nonlinear predictors, negative/intercept weights, conditional weights, or a different
model trained on the same inputs. The explicit per-row result already contradicts
“not clairvoyant.” A hypothesis class's optimum is not a Bayes/information bound.
LEAR and LightGBM also consume different representations (cross-hour vectors versus
23 pooled features), despite sharing source categories. No experiment here isolates
“information” from “architecture.” Weather is a promising hypothesis, not the only route.

The document gives incompatible versions of “50/50”: 0.63487 / 0.61383 in §5.2
(reduced QRA grid) versus 0.64466 in §5.3. Averaging the saved emitted A1/B2 vectors
returns **0.64465619 / 0.62002445**; averaging raw central heads gives point score
**0.64069622** before a new residual layer. Do not compare a reduced row/quantile grid
to the full-grid bar or call these the same release. The four-component emitted mean
A1/A3/A5/B2 is another policy: S_MAE **0.64279589**. It double-counts fitted arms:
central weights A1=11/24, A2=5/24, A4=1/12, B2=1/4; its residual layers differ too.

**NOT TESTED:** exact reduced-grid QRA 0.64590 / 0.63423; stacker 0.85456 versus A1
0.68350; leaky stacker 0.52938; learned block weights 0.66175 versus fixed 0.66020.
No preserved executable specification accompanies these rows. A 28-day pooled QRA
failure cannot close literature-style per-hour, longer-window QRA. Ninety-day evaluation
folds do not intrinsically prohibit generating longer *pre-fold* causal training forecasts.
Do not build a controller by default; do not describe all combination research as exhausted.

### A2. §5.3: weak persistence reproduced; unpredictability not established

A1/B2 per-fold MAE reproduces all five rows: 6.81990/6.21927,
9.95336/9.67638, 51.21276/54.00782, 16.74044/16.54061,
19.48164/19.20250. Oracle A1/B2 switching reproduces per-fold **0.65138170**,
per-day **0.59918903**, per-row **0.53054723**.

A1 wins **227/448 = 50.66964%** of represented days; crisis **53/88 = 60.22727%**.
Within-fold adjacent-observation lag-1 correlation is **0.07888943** and mean run length
**2.14354**, versus author +0.078 / 2.16. These calculations reset at fold boundaries;
a truly consecutive-calendar-day analysis would also separate missing days. Verdict:
**REPRODUCED WITH DEVIATION**. They establish low unconditional persistence, not
conditional independence given forecast-time features.

The exact original logistic 42.8% / S_MAE 0.69118 is **NOT TESTED**: feature formulas,
regularization, scaling and tie handling are missing. A separately specified illustration
using daily mean origin scale, mean absolute A1−B2 p50 spread, and scale/|level| (floor 1),
StandardScaler plus default LogisticRegression, trained folds 1–3 and tested 4–5, obtains
**51.67%** against **51.11%** majority baseline. This is not a tuned candidate or a recovery
of the original controller. Classification accuracy also ignores the magnitude of loss
on winning/losing days. Deferring controller work is reasonable prioritization; deleting
it as mathematically impossible is not. JEV need not be evaluated to make that distinction.

### A3. §5.6: economic inversion is decision-specific, and the LP is underspecified

Author EUR/day, B0/A1/B2/B3/blend/A2/PF:
**223.12 / 226.49 / 228.66 / 229.89 / 232.28 / 233.83 / 253.91**;
reported PF capture **86.4 / 88.1 / 89.7 / 90.7 / 90.8 / 91.4 / 100%**.
The latter are not the ratios of the displayed pooled EUR/day figures: for example,
233.83/253.91 = 92.09%, not 91.4%. An equal-fold ratio can explain this type of discrepancy,
but the aggregation must be stated.

Review specification: maximize forecast grid revenue minus a throughput cost;
`e_t=e_(t-1)+sqrt(.9)*charge_t-discharge_t/sqrt(.9)`;
0≤charge,discharge≤1 MW; 0≤e≤2 MWh; e_start=e_end=0.
Settle fixed decisions at actual hourly prices. Primary sensitivity sample is **444 complete
23/24/25-hour days**; four incomplete represented days are reported as excluded, never
silently compressed into shorter days. Two absent fold-3 days are already absent in CP-15.
These exclusions are for the economic diagnostic only, not a new statistical evaluation mask.

| Decision specification | B0 | A1 | B2 | B3 | Blend | A2 | PF |
|---|---:|---:|---:|---:|---:|---:|---:|
| Daily closure only, EUR/day | 221.86 | 224.85 | 226.59 | 228.15 | 230.29 | 232.10 | 251.85 |
| At most one internal equivalent cycle, EUR/day | 173.95 | 175.20 | 175.37 | 176.43 | 178.38 | 179.97 | 200.01 |
| One cycle, €10/grid-MWh throughput, exclusive charge/discharge, EUR/day | 134.00 | 135.76 | 136.31 | 135.58 | 139.27 | 139.87 | 161.24 |
| Same €10 variant, equal-fold PF capture % | 67.49 | 73.78 | **77.17** | 70.97 | **77.71** | 75.46 | 100 |
| One cycle, €30/grid-MWh throughput, exclusive charge/discharge, EUR/day | 82.81 | 85.24 | 84.79 | 84.89 | 88.33 | 90.54 | 108.61 |

The one-cycle cap is `sum(discharge/sqrt(.9))<=2`; it permits fractional dispatch and
idle days. Exclusive variants use a binary per-hour charge/discharge mode, i.e. MILP.
The costs are illustrative sensitivities, **not externally established battery economics
or proposed product thresholds**. The uncapped LP runs about **1.97–2.10 equivalent
cycles/day** and has **1,318 simultaneous charge/discharge hour-model instances**, summed
across seven policies. Negative-price loss dissipation is possible in this relaxation;
a daily terminal constraint is not a single-cycle constraint.

Using all 448 represented days with the symmetric-efficiency closure-only LP gives PF
**252.05875**, A2 **232.11914**, blend **230.51297** EUR/day and equal-fold captures
91.41605% / 90.77915%. Putting all loss on charging or discharging changes these further.
The exact original table is **NOT REPRODUCED**; the broad ranking is **REPRODUCED WITH
DEVIATION** under an explicit related formulation. Unknown initial SOC, cycle definition,
missing-day treatment and efficiency split prevent claiming exact replication.

A genuinely different decision reverses the ranking: optional purchase/resale of 1 MWh
at an illustrative fixed €50/MWh contract strike, buying when p50<50, has realized
EUR/target-hour **A1 6.85249, B2 6.81997, A2 6.31212, B3 6.24718, blend 6.87053,
B0 4.79011**, versus PF 7.98876. This is a transparent level-sensitive counterexample,
not an optimized commercial strategy; median-threshold dispatch need not maximize expected profit.

A seeded exploratory paired moving-block bootstrap (seed 15042, 2,000 replicates,
7-calendar-day blocks within each fold, retain missing dates as missing, pooled day-weighted
difference) gives A2 minus blend **+1.806 EUR/day, 95% interval [−0.486, 4.292]**
for closure-only; the €10 one-cycle variant gives **+0.592 [−0.979, 4.914]**.
These are post-selection sensitivities, not a confirmatory superiority test.

Perfect execution and price-taking remain assumptions in every calculation. There are
no bids/fills, imbalance settlements, network tariffs, power-dependent efficiency, degradation
model, intraday recourse, or multi-day SOC continuation. Post-2025 hourly average prices are
not a backtest of actual quarter-hour execution. Losing the artificial daily reset could
change rankings again. For an expected-value objective, distinguish conditional mean from
median and evaluate the actual decision policy. Hourly marginal quantiles also do not
supply the joint scenarios needed by a risk-sensitive intertemporal optimizer.

**Consequence:** retain B3/A2 as economic challengers, but withdraw a general “LightGBM wins
shape” claim. A2 shape MAE actually exceeds B2 in folds 2, 4 and 5; arbitrage depends on
extrema ordering, losses and dispatch constraints, not shape MAE alone. Do not annualize
these selected seasonal windows into realized EUR/MW/year. No economic superiority claim
here has a preregistered inference protocol.

### A4. §5.1: cited schedules verified, universal closure rejected

Both named primary pages were fetched directly on 2026-09-22:

- [SMARD forecast data](https://www.smard.de/page/en/wiki-article/5884/206318/forecast-data)
  states submission at 18:00 and next-day provisional publication by 18:00.
- [TenneT wind forecast](https://netztransparenz.tennet.eu/electricity-market/transparency-pages/transparency-germany/network-figures/actual-and-forecast-wind-energy-feed-in)
  states 08:00 estimation and 18:00 publication for its control-area wind product.

**REPRODUCED** for these documented routes; **NOT REPRODUCED** for “any published feed,”
for all German wind/solar being computed at 08:00, and for “a deadline is sufficient to
exclude.” A deadline is an upper bound; an 18:00 deadline permits 10:00 publication.
It does fail to *guarantee* pre-gate availability, which is enough to withhold admission
until positive evidence exists. The actual 18:00 schedule is the stronger route-specific
reason to exclude. Multiple documents describing the same institutional process are not
four independent measurements. The n=1 June observation is consistent, not universal proof.
No new polling experiment is required to reject these two routes, but do not forbid a
bounded documentary search for another documented pre-gate product.

### A5. §4.1: the archive gate was pointed at the wrong dates and API

The universal circa-2021 start claim is **NOT REPRODUCED**. Primary catalog documentation
and an actual 2019 file listing establish older operational forecasts. This review does
not claim full decoded-run coverage or authorize bulk ingestion.

| Provider / specific product | Primary-source finding | Consequence |
|---|---|---|
| [NCAR GDEX d084001, NCEP GFS 0.25°](https://gdex.ucar.edu/datasets/d084001/) | Operational 00/06/12/18 UTC runs from **2015-01-15**, 3-hourly leads through 240 h; winds and shortwave radiation listed; CC BY 4.0. [2019-01-01 files](https://gdex.ucar.edu/datasets/d084001/filelist/20190101/) explicitly include f024/f027/etc. | Historical depth can cover all five folds. Verify exact variables/heights, averaging, historical dissemination, gaps and present continuation. The catalog's future-dated upper bound relative to this review is not used as evidence of future observations. |
| [Open Climate Fix ICON-EU](https://huggingface.co/datasets/openclimatefix/dwd-icon-eu) | **2020-01-01** onward; four run times; 27 early variables include wind components, roughness, pressure-level wind and direct/diffuse radiation. Shape/variable change in March 2023. Gated free access; archive no longer updated. | Crisis training depth is plausible, unlike the plan's conclusion. Native hub-height fields and continuous recent coverage are not established. |
| [OCF ICON-Global](https://huggingface.co/datasets/openclimatefix/dwd-icon-global) | **March 2023**, four daily runs, CC BY 4.0. | No crisis training; prospective later-fold path, pending current coverage. |
| [Dynamical GFS forecast](https://dynamical.org/catalog/noaa-gfs-forecast/) | **2021-05-01**, init_time×lead_time preserved. | Too late for full crisis training, useful as a continuation route. |
| [Dynamical ICON-EU 5-day](https://dynamical.org/catalog/dwd-icon-eu-forecast-5-day/) | **2026-02-10**; current replacement for the old OCF service is not a replacement for its historical depth. | No inherited fold's full training window; do not infer archive continuity from the migration link. |
| [Open-Meteo Historical Forecast](https://open-meteo.com/en/docs/historical-forecast-api) | Stitched initial hours, not D−1 vintages. Table: GFS 2021-03-23; ICON/ICON-EU/ICON-D2 2022-11-24; IFS 0.4° 2022-11-07; IFS 0.25° 2024-02-03; JMA GSM 2016-01-01. | Start dates alone do not admit a feature. IFS HRES 2017 listing does not imply old operational single runs. |
| [Open-Meteo Single Runs](https://open-meteo.com/en/docs/single-runs-api) | IFS HRES **2024-03-14**, most others **2026-04-02**; current text describes early IFS coverage as Cycle 49R1 hindcasts. | Earlier archive is not automatically an as-issued historical run. Even fold 5 needs training before March 2024. |
| [Open-Meteo Previous Runs](https://open-meteo.com/en/docs/previous-runs-api) | Most from January 2024; GFS **2 m temperature** from March 2021; JMA GSM/MSM from 2018. Fixed lead offsets. | A temperature exception is not a wind/radiation archive. GSM is global; MSM is Japan. Per-valid-hour fixed offsets need an origin audit. |
| [DWD live distribution](https://opendata.dwd.de/weather/nwp/icon-eu/) | Current-run directory, not established multiyear retention. OCF documents short retention. | Use an independently validated archive. |
| [ECMWF TIGGE](https://www.ecmwf.int/en/research/projects/tigge) | Multi-centre ensemble archive from October 2006 for scientific research. | Further older archive lead, not admitted here: exact fields, operational access/dissemination and terms remain unchecked. |

The correct first-evaluation-day training starts are **2019-01-01 / 2019-04-04 /
2020-07-03 / 2023-05-04 / 2024-01-11**, computed from max(2019-01-01,D−728).
Fold 1 does not require 2018. A 29-calendar-day nominal warm-up shifts the last four
starts to **2019-03-06 / 2020-06-04 / 2023-04-05 / 2023-12-13**; exact starts can
be earlier around incomplete days. NWP initialization is a further D−1 offset, subject
to the frozen 2019 input boundary: explicitly handle the first admissible training target
instead of silently using a pre-2019 run. “728 days” is a cap on expanding history, not
a universal minimum. Changing evaluation dates need not change that 2019 floor.

Zero price is not zero engineering cost: GFS GRIB access/subsetting, three-hour interpolation,
radiation accumulation and changing NWP model versions are real work. Open-Meteo's
[free-service terms](https://open-meteo.com/en/terms) distinguish data CC BY 4.0 from
service limits (<10,000/day, 5,000/hour, 600/minute); they do not establish a blanket
free bulk bucket with the required historical vintages. No complete v3 feasibility PASS
can follow from this documentation check alone.

### A6. Other evidence and the 19.4926% transfer

| Claim | Author | Independent finding / verdict |
|---|---|---|
| §4.4 A69 value | 19.4926% pooled raw-head pinball | **REPRODUCED** from `reports/cp2/a69_benchmark_predictions.parquet`: 13.01584151→10.47871463, 19.49260734%. Raw p50 pooled MAE 41.75983236→29.93830428. This is a v1 post-gate feature bundle, not a CP-15 or in-house-weather treatment effect. Transfer to S_MAE is **NOT TESTED** and cannot be assumed. |
| §5.4 disagreement | Quintiles 5.90→50.05; crisis r=.075, elsewhere .24–.31; WIS .63425 versus .60691, blend ~0.3% | **NOT REPRODUCED** for a declared six-arm population SD and A1 absolute error: quintiles 6.394→48.639, r by fold .41647/.07601/.00048/.25662/.20023. Exact author arm set, target error, driver fitting and blend unspecified; WIS-driver variants **NOT TESTED**. Qualitative common failure plausible; numerical table is not a reusable protocol. |
| §5.5 hourly width and coverage | Width 134.325, night .993–.998 vs midday .866–.888 | **REPRODUCED WITH DEVIATION**: within-day width range <1.8e−13; per-hour pooled widths 134.32455–134.42098 because hour denominators differ. Coverage and night/midday MAE ranges reproduce. |
| §5.5 A1 oracle / causal WIS | .61009 / .63793 | **REPRODUCED WITH DEVIATION** for oracle: per-fold/hour raw signed p50 residual tails with p50 held fixed gives **.61048**; refitting the residual median gives .60905. Normalized variants differ further. Exact cold-start causal recipe **NOT TESTED**, .63793 retained as unverified. |
| §5.5 four-component oracle | .64280 / .58927; criterion 5 all folds | Point **REPRODUCED** .64279589; fixed-p50 raw-tail oracle WIS **.58936**, **REPRODUCED WITH DEVIATION**. Exact author's criterion-5 claim **NOT TESTED**. Neither this oracle nor its forecasted causal range .589–.638 licenses shipping. |
| §5.7 architecture / block deficit | LEAR 24 fits; pooled LGBM; ratios 1.627/1.173/1.133 | **REPRODUCED** via source and saved predictions: 1.626536/1.172716/1.133081 over 3,579/4,032/3,136 hours. 22/40/38% error shares are approximate, not a forecast of achievable gains. |
| §5.8 level/shape | Level 5.634/7.402/41.621/9.258/14.404; shape 4.833/6.967/35.484/15.531/14.952 | **REPRODUCED WITH DEVIATION** in aggregation: equal-day shape means reproduce exactly; protocol hourly weighting gives 4.83314/6.96495/35.48387/15.53149/14.93592. Level means reproduce. These are non-additive MAE diagnostics, not causal attribution to missing VRE. |

Oracle empirical quantiles minimize a particular in-sample loss in a restricted construction;
they are not a universal lower bound on every future causal interval policy. Therefore “a
causal .589 result is wrong” and “anything outside .589–.638 falsifies all §5” are invalid
acceptance rules. A credible causal policy can be worse or better for specified reasons.
Twenty-eight per-hour residuals also put a 2.5% tail estimate below one expected tail
observation; pooling/shrinkage and coverage uncertainty need explicit design.

## Pass B — Is the plan sound given the claims?

1. **A reporting release and a qualified forecast product are different deliverables.** v2
   can package existing research without NWP, but causally rebuilding intervals is new modelling.
   It has no exact blend definition, no policy initialization/state/update/failure contract,
   no freeze/replay route, and no binding product bar. v21 §10/CP-17 still blocks promotion
   after NOT_DEMONSTRATED. “Cannot be blocked” is false. Provide an owner-chosen research
   release route, or require product feasibility before freezing and shipping.
2. **Repair the dependency graph.** Documentary archive work and content outlining need no
   new model. Full v2, per-block LGBM and DDNN evaluation all need a ratified candidate/protocol
   and brief. v3 needs verified archive admission, released A75 targets and origin-safe weather
   transformations. Recombination follows *any* new arm, including per-block LGBM—not just weather
   or neural models. The presentation can draft existing results now; final claims wait for evidence.
3. **The comparator is a demanding screen, not a logical defect.** v21 §8 explicitly calls
   its per-period best-reference comparison diagnostic. Criteria 1/2 use minima of aggregate
   scores, not an independently deployable per-row policy. A model can legitimately be required
   to beat several references. The Owner may adopt a new useful product bar, but “oracle” is
   not sufficient justification to lower it. Keep §8 and its failure unchanged.
4. **Make the economic decision actionable without pretending to unsee results.** Ask the Owner
   to choose an actual user/decision, capacity/exposure, permitted execution assumptions,
   independently documented annual operating cost and required surplus. Express a gate as
   incremental *net* value versus a deployable reference under that fixed decision, with a
   fixed uncertainty rule. Zero external spend does not imply zero operator cost. If no such
   external rationale exists, report economics as exploratory and do not invent a pass/fail
   percentage. A fresh independent owner specification plus a future freeze can avoid further
   contamination; looking away from a table cannot erase previous selection.
5. **The proposed confirmation is not clean.** `data/partitions.json` assigns 2026-04-08 to
   embargo; 04-09..06-07 to final calibration; 06-08 to embargo; 06-09..09-06 to v1 holdout.
   “Unused” is false. The 152 calendar days are real but not an untouched confirmation sample.
   April 8..September 22 is 168 days only if today's date is included; it is not 168 complete
   outcome days, and the frozen snapshot ends September 6. v21 §9 requires at least **90
   consecutive delivery days after policy freeze**, with lineage and failures. Historical
   rescoring is exploratory even if a particular v2 fit has not consumed those targets.
6. **Test information and architecture separately.** After admission, compare same model with
   and without NWP; compare direct weather features with generated VRE/residual load. Build
   generation-model training features from chronologically held-forward predictions, not in-sample
   fitted generation. Preserve available-at times for A75 labels, capacity changes and normalization.
   The existing causal seasonal/VRE proxy is a useful control. Better load vintages/cross-border
   inputs in the existing feasibility memo are bounded alternatives, not an assertion that
   weather is the only possible information gain.
7. **A model choice must have a zero-cost delivery path.** DDNN browser parity is an untested
   engineering claim; PyTorch/JSU is not a LightGBM booster. TabPFN “licence resolved” is false:
   the retrieved [v1.1 full licence](https://huggingface.co/Prior-Labs/tabpfn_2_5/raw/main/LICENSE)
   restricts eligible users in its preamble, covers outputs in §2(d), gives distribution
   conditions in §3, and disallows hosted services without a separate commercial licence in
   §3(d). A prediction lookup does not remove output-use restrictions. Treat it as a conditional
   research probe, not a free shippable champion. Do not accept terms or buy a licence in this task.
   “Wide” versus “narrow” winning margins are also undefined owner tradeoffs.
8. **Bound the search.** One archive gate, one fixed v2 policy, at most one model-family
   challenger initially, declared budget and stop rules. Neither pretraining contamination of
   German 2022 prices in Chronos nor a clean later-fold cutoff has been verified; label unknown
   and require provenance before any confirmatory language. NBEATSx can consume existing load;
   postponement may be sensible, but “nothing to consume” does not prove no potential value.

## Pass C — Is it written to be executed?

The self-assessment is directionally right but understates the defects. The received file
is **644 lines / 6,056 words**, not ~550; “half non-actionable” is a subjective description,
not a measured fraction. Licence discussion is about 30 lines in the model work item and
should become a short admission condition with a source. Position/release/evidence sections
repeat causal conclusions as certainty. No defined v2 completion or product acceptance
condition exists; runtime speculation is not an effort estimate.

Missing from that self-assessment:

- Conflicting definitions of the blend, full versus reduced score grid, central versus final p50,
  raw versus scaled residuals, equal-day/hour/fold weighting and battery value aggregation.
- No accountable executor, finite experiment budget, explicit dependencies on an authorized brief,
  stop/failure disposition, or distinction between successful engineering and a losing model.
- No preregistered candidate count, training-only tuning protocol, residual release delay,
  warm-up failure rule, DST/missing-hour handling or availability audit for generated features.
- No artifact/state freeze, reproducible cold start, forecast issuance record, missing-input fallback,
  local verification/review, owner landing/publication handoff or rollback to preserved v1.
- No valid calendar gate for the post-freeze confirmation clock; a historical interval is sold
  as if it created clean evidence. No annualization rule or uncertainty on economic claims.
- No archive resource estimate, sample decoding requirement, field-level vintage/coverage matrix,
  storage estimate, changed-model handling, or admission proof for even folds marked “clear.”
- Per-block compute count omits tuning, warm-up, both raw/normalized policies and review;
  ~728 rows/hour applies only at full history and varies with eligibility. Browser compatibility
  and licensing are asserted as conclusions before a minimal proof.
- An instruction to repair unrelated stale paths and tooling/Q&A archaeology expands scope.
  Preserve durable references and capture status, but don't turn a plan into a maintenance queue.

**Rewrite requirements:** put decisions and work first; assign each item a deliverable,
acceptance criterion, active-effort range and stop rule; retain all consequential numbers
in a compact claim ledger; preserve the economic contamination disclosure; carry unresolved
owner decisions forward. Do not retitle research success as product feasibility.

## Reproduction record and limitations

Used the existing `.venv` with NumPy/pandas/SciPy/sklearn; no dependency installation or
forecast-model retraining. LP/MILP solves completed successfully. Source and metrics checks
are independent of the plan author's analysis, **not a governance Integration review**.
Scripts and JSON/CSV outputs are retained under `.local/artifacts/plan-review-2026-09-22/`.
The essential methods, exact inputs and numerical findings above are durable here; executable
harnesses follow so that `.local` is not the sole copy of the analysis. Their output paths
refer to that project-local directory. Run from the repository root with
`OPENBLAS_NUM_THREADS=1 .venv/bin/python <extracted-script-path>`.

Not done: original QRA/stacker reconstruction, exact original battery program, causal interval
rebuild, archive GRIB/Zarr decoding or exhaustive missingness, new-source model fitting,
reserved-tail evaluation, full retraining, operational deployment or visual QA.

Interview-answer capture trigger: a restricted oracle optimum was mistaken for an information
ceiling, and archive/product semantics changed the plan once checked. No Q&A entry filed;
the Owner-supplied next number remains 31, not reverified or changed here.

### Executable evidence: recompute.py

```python
import numpy as np,pandas as pd,json,hashlib
from scipy.optimize import linprog
from scipy.sparse import csr_matrix,eye,hstack,vstack
from pathlib import Path
p=pd.read_parquet('reports/cp15/predictions.parquet'); qcols=['p025','p10','p25','p50','p75','p90','p975']
a={k:v.sort_values(['fold','timestamp_utc']).reset_index(drop=True) for k,v in p.groupby('policy')}
z=a['B0']; y=z.y_true.to_numpy(); folds=z.fold.to_numpy(); hours=z.timestamp_utc.dt.tz_convert('Europe/Berlin').dt.hour.to_numpy(); days=z.delivery_date.to_numpy(); n=len(y)
for k,v in a.items():
 assert np.array_equal(v.timestamp_utc,z.timestamp_utc) and np.array_equal(v.y_true,y)
base={f:np.mean(abs(y[folds==f]-z.p50.to_numpy()[folds==f])) for f in np.unique(folds)}
w=np.array([1/(5*sum(folds==f)*base[f]) for f in folds])
def score(v):return float(w@abs(y-v))
def wis(Q):
 t=.5*abs(y-Q[:,3])
 for alpha,l,u in [(.5,2,4),(.2,1,5),(.05,0,6)]:t+=alpha/2*(Q[:,u]-Q[:,l])+np.maximum(Q[:,l]-y,0)+np.maximum(y-Q[:,u],0)
 return t/3.5
bwis=wis(z[qcols].to_numpy()); ww=np.array([1/(5*sum(folds==f)*bwis[folds==f].mean()) for f in folds])
def oracle(X,mask):
 x=X[mask]; yy=y[mask]; wt=w[mask]; N,K=x.shape
 C=hstack([csr_matrix(x),-eye(N)]); D=hstack([-csr_matrix(x),-eye(N)])
 r=linprog(np.r_[np.zeros(K),wt],A_ub=vstack([C,D]),b_ub=np.r_[yy,-yy],A_eq=csr_matrix(np.r_[np.ones(K),np.zeros(N)][None,:]),b_eq=[1],bounds=[(0,None)]*(K+N),method='highs')
 assert r.success,r.message
 return r.fun,r.x[:K]
res={'hash':hashlib.sha256(Path('reports/cp15/predictions.parquet').read_bytes()).hexdigest(),'gate':{k:[score(v.p50.to_numpy()),float(ww@wis(v[qcols].to_numpy()))] for k,v in a.items()}}
keys=['B1','B2','B3','A1','A2','A4']; X=np.column_stack([a[k].p50 for k in keys]); allmask=np.ones(n,bool)
res['oracle']={'arms':keys,'static':oracle(X,allmask),'per_fold':sum(oracle(X,folds==f)[0] for f in np.unique(folds)),'per_hour':sum(oracle(X,hours==h)[0] for h in range(24)),'per_fold_hour':sum(oracle(X,(hours==h)&(folds==f))[0] for f in np.unique(folds) for h in range(24)),'per_row_selection':float(w@np.min(abs(X-y[:,None]),axis=1)),'per_row_convex':float(w@np.maximum(np.maximum(X.min(axis=1)-y,y-X.max(axis=1)),0)),'mean6':score(X.mean(axis=1))}
blend=(a['A1'].p50.to_numpy()+a['B2'].p50.to_numpy())/2
res['blend']={'emitted_p50':[score(blend),float(ww@wis((a['A1'][qcols].to_numpy()+a['B2'][qcols].to_numpy())/2))],'raw_central':score((a['A1'].central.to_numpy()+a['B2'].central.to_numpy())/2)}
df=pd.DataFrame({'fold':folds,'day':days,'a':abs(y-a['A1'].p50),'b':abs(y-a['B2'].p50)})
daily=df.groupby(['fold','day'])[['a','b']].mean(); wins=(daily.a<daily.b).astype(int)
runs=[]; lagx=[]; lagy=[]
for f,t in wins.groupby(level=0):
 ar=t.to_numpy(); lengths=np.diff(np.r_[0,np.flatnonzero(np.diff(ar))+1,len(ar)]);runs+=lengths.tolist();lagx.extend(ar[:-1]);lagy.extend(ar[1:])
res['switch']={'win_rate':float(wins.mean()),'wins':int(wins.sum()),'days':len(wins),'lag1_within_fold':float(np.corrcoef(lagx,lagy)[0,1]),'mean_run':float(np.mean(runs)),'crisis_wins':float(wins.loc['fold_3'].mean()),'fold_mae':df.groupby('fold')[['a','b']].mean().to_dict(),'oracle_fold':sum(min(np.mean(df.a[folds==f]),np.mean(df.b[folds==f]))/base[f]/5 for f in base),'oracle_day':sum(w[i]* (df.a[i] if wins.loc[(folds[i],days[i])] else df.b[i]) for i in range(n)),'oracle_row':float(w@np.minimum(df.a,df.b))}
res['hour_width']={'min':float((a['A1'].p975-a['A1'].p025).groupby(hours).mean().min()),'max':float((a['A1'].p975-a['A1'].p025).groupby(hours).mean().max())}
res['hourly']=pd.DataFrame({'h':hours,'cov':(y>=a['A1'].p025)&(y<=a['A1'].p975),'mae':df.a}).groupby('h').mean().to_dict()
res['decomposition']={}
for k in ['A1','B2','B3','A2']:
 d=pd.DataFrame({'f':folds,'d':days,'y':y,'p':a[k].p50}); means=d.groupby(['f','d'])[['y','p']].transform('mean');d['shape']=abs((d.y-means.y)-(d.p-means.p));l=d.groupby(['f','d'])[['y','p']].mean();res['decomposition'][k]={'level':abs(l.y-l.p).groupby('f').mean().to_dict(),'shape':d.groupby('f')['shape'].mean().to_dict()}
block=np.where((hours>=22)|(hours<=5),'night',np.where((hours>=10)&(hours<=16),'solar','shoulder'))
res['blocks']={b:{'n':int(sum(block==b)),'B3_B2':float(abs(y-a['B3'].p50)[block==b].mean()/abs(y-a['B2'].p50)[block==b].mean()),'B3':float(abs(y-a['B3'].p50)[block==b].mean())} for b in np.unique(block)}
# Oracle empirical normalized signed residuals conditional on fold/hour, using emitted p50.
for raw in [False,True]:
 v=a['A1'].central.to_numpy() if raw else a['A1'].p50.to_numpy();scale=a['A1'].scale.to_numpy();Q=np.empty((n,7))
 for f in np.unique(folds):
  for h in range(24):
   m=(folds==f)&(hours==h); e=(y[m]-v[m])/scale[m];Q[m]=v[m,None]+scale[m,None]*np.quantile(e,[.025,.1,.25,.5,.75,.9,.975])
 res['interval_oracle_'+('central' if raw else 'p50')]=[score(Q[:,3]),float(ww@wis(Q))]
# Spread diagnosis, emitted six arms.
spread=X.std(axis=1);err=abs(y-a['A1'].p50.to_numpy()); bins=pd.qcut(spread,5,labels=False)
res['spread']={'corr':{f:float(np.corrcoef(spread[folds==f],err[folds==f])[0,1]) for f in base},'quintile_mae':pd.Series(err).groupby(bins).mean().to_dict()}
def default(o):
 if isinstance(o,np.ndarray): return o.tolist()
 if isinstance(o,np.generic):return o.item()
 raise TypeError(type(o))
Path('.local/artifacts/plan-review-2026-09-22/metrics.json').write_text(json.dumps(res,indent=2,default=default))
print(json.dumps(res,indent=2,default=default))
```

### Executable evidence: supplement.py

```python
import numpy as np,pandas as pd,json
from scipy.optimize import linprog
from scipy.sparse import csr_matrix,eye,hstack,vstack
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
p=pd.read_parquet('reports/cp15/predictions.parquet');a={k:v.sort_values(['fold','timestamp_utc']).reset_index(drop=True) for k,v in p.groupby('policy')};z=a['B0'];y=z.y_true.to_numpy();fs=z.fold.to_numpy();hs=z.timestamp_utc.dt.tz_convert('Europe/Berlin').dt.hour.to_numpy();ds=z.delivery_date;N=len(y);base={f:abs(y[fs==f]-z.p50[fs==f]).mean() for f in np.unique(fs)};w=np.array([1/(5*sum(fs==f)*base[f]) for f in fs]);X=np.column_stack([a[k].p50 for k in ['B1','B2','B3','A1','A2','A4']]);out={}
def fit(mask):
 x=X[mask];yy=y[mask];n,k=x.shape;r=linprog(np.r_[np.zeros(k),np.ones(n)/n],A_ub=vstack([hstack([csr_matrix(x),-eye(n)]),hstack([-csr_matrix(x),-eye(n)])]),b_ub=np.r_[yy,-yy],A_eq=csr_matrix(np.r_[np.ones(k),np.zeros(n)][None,:]),b_eq=[1],bounds=(0,None),method='highs');assert r.success;return r.x[:k]
out['pooled_static_scored_equal_fold']=float(w@abs(y-X@fit(np.ones(N,bool))))
pred=np.empty(N)
for h in range(24):
 m=hs==h;pred[m]=X[m]@fit(m)
out['pooled_per_hour_scored_equal_fold']=float(w@abs(y-pred))
# Recompute source nine-quantile benchmark, no fitting.
b=pd.read_parquet('reports/cp2/a69_benchmark_predictions.parquet');qs=np.array([.025,.05,.1,.25,.5,.75,.9,.95,.975]);cols=['raw_p025','raw_p05','raw_p10','raw_p25','raw_p50','raw_p75','raw_p90','raw_p95','raw_p975'];br={}
for k,g in b.groupby('arm'):
 e=g.y_true.to_numpy()[:,None]-g[cols].to_numpy();br[k]={'pinball':float(np.maximum(qs*e,(qs-1)*e).mean()),'MAE':float(abs(e[:,4]).mean())}
out['a69']=br
# Winner persistence, no joining fold boundaries, optionally adjacent calendar days only.
e=pd.DataFrame({'f':fs,'d':ds,'a':abs(y-a['A1'].p50),'b':abs(y-a['B2'].p50),'scale':a['A1'].scale,'spread':abs(a['A1'].p50-a['B2'].p50),'vol':z.scale/z.level.abs().clip(lower=1)})
d=e.groupby(['f','d']).mean();win=(d.a<d.b).astype(int);tr=d.index.get_level_values(0).isin(['fold_1','fold_2','fold_3']);features=['scale','spread','vol'];m=make_pipeline(StandardScaler(),LogisticRegression(max_iter=2000));m.fit(d.loc[tr,features],win[tr]);pred=m.predict(d.loc[~tr,features]);out['controller_illustration']={'features':features,'accuracy':float(np.mean(pred==win[~tr])),'A1_rate':float(win[~tr].mean()),'majority_rate':float(max(win[~tr].mean(),1-win[~tr].mean()))}
# Pooled hour-blind widths are constant within each date; DST creates unequal hour weighting.
out['max_daily_A1_width_range']=float((a['A1'].p975-a['A1'].p025).groupby(ds).agg(lambda t:t.max()-t.min()).max())
out['shape_equal_days']={}
for k in ['A1']:
 d=pd.DataFrame({'f':fs,'d':ds,'y':y,'p':a[k].p50});m=d.groupby(['f','d'])[['y','p']].transform('mean');d['err']=abs(d.y-m.y-d.p+m.p);out['shape_equal_days'][k]=d.groupby(['f','d']).err.mean().groupby('f').mean().to_dict()
# Try clearly defined oracle interval constructions; all in-sample and nondeployable.
q7=np.array([.025,.1,.25,.5,.75,.9,.975]);qcols=['p025','p10','p25','p50','p75','p90','p975']
def wis(q):
 v=.5*abs(y-q[:,3])
 for alpha,l,u in [(.5,2,4),(.2,1,5),(.05,0,6)]:v+=alpha/2*(q[:,u]-q[:,l])+np.maximum(q[:,l]-y,0)+np.maximum(y-q[:,u],0)
 return v/3.5
bw=wis(z[qcols].to_numpy());ww=np.array([1/(5*sum(fs==f)*bw[fs==f].mean()) for f in fs]);out['intervals']={}
for label,central in [('A1_p50',a['A1'].p50.to_numpy()),('A1_central',a['A1'].central.to_numpy()),('ensemble_p50',np.column_stack([a[k].p50 for k in ['A1','A3','A5','B2']]).mean(axis=1))]:
 for normalized in [False,True]:
  scale=a['A1'].scale.to_numpy() if normalized else np.ones(N);Q=np.empty((N,7))
  for f in np.unique(fs):
   for h in range(24):
    ix=(fs==f)&(hs==h);Q[ix]=central[ix,None]+scale[ix,None]*np.quantile((y[ix]-central[ix])/scale[ix],q7)
  out['intervals'][label+str(normalized)]=[float(w@abs(y-Q[:,3])),float(ww@wis(Q))]
Path('.local/artifacts/plan-review-2026-09-22/supplement.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
```

### Executable evidence: dispatch.py

```python
import pandas as pd,numpy as np,json
from scipy.optimize import linprog,milp,Bounds,LinearConstraint
from pathlib import Path
p=pd.read_parquet('reports/cp15/predictions.parquet'); a={k:v.sort_values(['fold','timestamp_utc']).reset_index(drop=True) for k,v in p.groupby('policy')};z=a['B0']; forecasts={k:a[k].p50.to_numpy() for k in ['B0','A1','B2','B3','A2']};forecasts['blend']=(forecasts['A1']+forecasts['B2'])/2;forecasts['PF']=z.y_true.to_numpy(); out={}; dailyrows=[]
# Energy in internal MWh; charge/discharge are grid MWh each hour. Empty at both ends.
for variant,cap,cost,exclusive in [('closure_only',None,0,False),('one_cycle',2,0,False),('one_cycle_cost10',2,10,True),('one_cycle_cost30',2,30,True)]:
 rows=[]; simultaneous=0
 for (f,day),g in z.groupby(['fold','delivery_date']):
  ids=g.index.to_numpy(); t=g.timestamp_utc; expected=int(((pd.Timestamp(day)+pd.Timedelta(days=1)).tz_localize('Europe/Berlin')-pd.Timestamp(day).tz_localize('Europe/Berlin')).total_seconds()/3600)
  if len(ids)!=expected:continue
  N=len(ids);eta=np.sqrt(.9);L=np.tril(np.ones((N,N)));A=np.c_[eta*L,-L/eta];E=A[-1:];U=np.r_[A,-A];b=np.r_[np.ones(N)*2,np.zeros(N)]
  if cap is not None:U=np.r_[U,np.r_[np.zeros(N),np.ones(N)/eta][None,:]];b=np.r_[b,cap]
  for k,pred in forecasts.items():
   ph=pred[ids];c=np.r_[ph+cost,-ph+cost];bounds=[(0,1)]*(2*N)
   if exclusive:
    # charge<=u and discharge<=1-u, u binary; full physical gate for negative prices.
    obj=np.r_[c,np.zeros(N)];con=np.r_[np.c_[U,np.zeros((len(U),N))],np.c_[E,np.zeros((1,N))],np.c_[np.eye(N),np.zeros((N,N)),-np.eye(N)],np.c_[np.zeros((N,N)),np.eye(N),np.eye(N)]]
    lo=np.r_[np.full(len(U),-np.inf),0,np.full(2*N,-np.inf)];hi=np.r_[b,0,np.zeros(N),np.ones(N)]
    r=milp(obj,integrality=np.r_[np.zeros(2*N),np.ones(N)],bounds=Bounds(np.zeros(3*N),np.ones(3*N)),constraints=LinearConstraint(con,lo,hi));x=r.x[:2*N]
   else:
    r=linprog(c,A_ub=U,b_ub=b,A_eq=E,b_eq=[0],bounds=bounds,method='highs');x=r.x
   assert r.success,r.message
   simultaneous+=int(np.sum((x[:N]>1e-7)&(x[N:]>1e-7)))
   profit=float(g.y_true.to_numpy()@(x[N:]-x[:N])-cost*x.sum());rows.append({'fold':f,'day':str(day),'model':k,'profit':profit,'throughput':float(x[N:].sum()/eta)})
 d=pd.DataFrame(rows);m=d.groupby(['fold','model']).profit.mean().unstack();rel=m.div(m.PF,axis=0).mean()*100
 out[variant]={'days':len(d)//7,'EUR_day':d.groupby('model').profit.mean().to_dict(),'equal_fold_percent_PF':rel.to_dict(),'pooled_percent_PF':(d.groupby('model').profit.mean()/d[d.model=='PF'].profit.mean()*100).to_dict(),'simultaneous_hours_all_models':simultaneous,'mean_internal_cycles':(d.groupby('model').throughput.mean()/2).to_dict()};dailyrows.extend([dict(x,variant=variant) for x in rows]);print(variant,json.dumps(out[variant]),flush=True)
# Different decision: one optional 1 MWh buy-and-resell at exogenous contract strike 50 EUR/MWh.
# p50 threshold optimizes forecast proxy; a sensitivity diagnostic, not expected-value optimality.
strike=50;alt={}
for k,pred in forecasts.items():
 payoff=(strike-z.y_true.to_numpy())*(pred<strike);alt[k]=float(payoff.mean())
out['fixed_strike_50_EUR_hour']=alt
Path('.local/artifacts/plan-review-2026-09-22/dispatch.json').write_text(json.dumps(out,indent=2));pd.DataFrame(dailyrows).to_csv('.local/artifacts/plan-review-2026-09-22/dispatch-daily.csv',index=False)
```

### Executable evidence: dispatch_check.py

```python
import numpy as np,pandas as pd,json
from scipy.optimize import linprog
from pathlib import Path
p=pd.read_parquet('reports/cp15/predictions.parquet'); a={k:v.sort_values(['fold','timestamp_utc']).reset_index(drop=True) for k,v in p.groupby('policy')};z=a['B0'];out={}
for ec,ed in [(np.sqrt(.9),np.sqrt(.9)),(.9,1),(1,.9)]:
 rows=[]
 for (f,d),g in z.groupby(['fold','delivery_date']):
  ids=g.index;N=len(ids);L=np.tril(np.ones((N,N)));A=np.c_[ec*L,-L/ed]
  for k in ['B0','A1','B2','B3','A2','blend','PF']:
   ph=g.y_true.to_numpy() if k=='PF' else ((a['A1'].p50+a['B2'].p50)/2).loc[ids].to_numpy() if k=='blend' else a[k].p50.loc[ids].to_numpy()
   r=linprog(np.r_[ph,-ph],A_ub=np.r_[A,-A],b_ub=np.r_[np.ones(N)*2,np.zeros(N)],A_eq=A[-1:],b_eq=[0],bounds=(0,1),method='highs');assert r.success
   rows.append((f,k,float(g.y_true.to_numpy()@(r.x[N:]-r.x[:N]))))
 t=pd.DataFrame(rows,columns=['fold','model','value']);m=t.groupby(['fold','model']).value.mean().unstack();out[str((ec,ed))]={'EUR_day':t.groupby('model').value.mean().to_dict(),'equal_fold_percent_PF':(m.div(m.PF,axis=0).mean()*100).to_dict()}
print(json.dumps(out,indent=2));Path('.local/artifacts/plan-review-2026-09-22/dispatch-check.json').write_text(json.dumps(out,indent=2))
```
