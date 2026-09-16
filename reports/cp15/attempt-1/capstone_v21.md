# Capstone v21 — Adaptive forecasting with measured product quality

**Active owner-authorized execution plan · 2026-09-15.** The owner approved execution of the
research recommendation and the necessary plan change. The Orchestrator drafted this exact text
under that delegated authority; this is not a claim that the owner reviewed every sentence.
It replaces v20 for future work. Original v20 remains the historical authority for CP-10.

## 1. Objective, authority and preserved evidence

Deliver a DE-LU day-ahead forecasting product with demonstrably useful point predictions and
uncertainty. A correctly completed experiment is not proof that its resulting model is good.
32% or 40% coverage of nominal 95% intervals is inadequate.

Only **CP-15** is execution-ready in this version. CP-11–CP-14 under v20 are superseded as future
instructions, not silently completed. Later work requires its own complete bar and brief.
CP-10 retains its Integration PASS and unresolved product result. Its branch disposition remains
undecided; nothing here authorizes landing or reclamation.

Preserve `models/champion/`, `data/snapshot.parquet`, `data/partitions.json`,
`docs/cp2-model-report.md`, `reports/cp2/`, `reports/cp10/`, the v1 public report and surfaces,
closed `delu-cp2`, and all existing evidence/landing tags. Preserve p = 0.948 and peak coverage
0.194 exactly as historical results. Never write new research into those artifacts.

AGENTS.md and engineering-role.md continue to govern roles, isolation, candidates and publication.
The owner authorized this task's plan replacement and directly necessary routing/state edits;
this is not a standing suspension for the Engineer. Builder is not Critic. A fresh Integration
verdict must bind the final candidate. **CP-3B item 6 was unmet and is not a precedent.**

## 2. The forecasting task and information boundary

Keep DE-LU hourly day-ahead prices as the target. A delivery date D contains its actual 23/24/25
canonical hours. Do not change the market, horizon, aggregation or target to improve a score.
Use the inherited v1 forecast-origin convention and eligibility contract. Record its exact
timezone, UTC instants and DST handling in the protocol; do not silently reinterpret “CET”.

Every predictor, normalization statistic and training target must have been available at its
historical forecast origin. Preserve the delivery-day masking test (exactly zero change) and
an available D-1 price mutation that moves an appropriate controlled forecast. Preserve refusal
of post-gate A69 and target-day actual columns. Preprocessing is part of this boundary.

For online forecast-error updates retain the conservative **complete delivery day D-2** release
rule, including 23/24/25-hour completeness. Consume each issued forecast/error pair once only.
Do not infer permission to use D-1 feedback from permission to use D-1 price predictors.
Report the delay as a policy restriction, not a universal claim about auction information.

## 3. Data and evidence class

CP-15 uses the existing development periods, folds 1–5, and their original eligible target hours.
All outputs are `development_post_selection`. Fold 3 may now inform exploratory comparison;
this is an explicit change from v20 and cannot make 2022 unseen again. No date-based crisis
feature or fold-specific model parameter is allowed. August 15–31 remains a reporting slice.

Do not read the spent v1 holdout or reserved tail outcomes for fitting, tuning or selection.
Filter admissible partitions before materializing model inputs. Reuse the existing admissible
historical predictor definitions, and add only causal transformations of those predictors here.
Every arm has the same information and target rows. Missing-model forecasts are failures, not
permission to shrink the common evaluation set. Declare exclusions inherited from v1 separately.

Warm-up forecasts must be genuine historical-origin forecasts from admissible pre-evaluation
history. Later observations can train subsequent daily models only after becoming available.
No in-sample fitted residuals masquerading as held-forward calibration errors. Report all data
cutoffs, row masks, hashes, fit/update counts and warm-up boundaries per fold and arm.

New-source research is read-only feasibility work in CP-15. No paid data purchase, data-license
change or deployment is authorized. Existing attribution and DATA-LICENSE.md remain controlling.
Do not use reanalysis as old forecast vintages, revised outages as as-of records, or 2024-only
weather to claim 2022 improvement. Check publication times for proposed cross-border inputs.

## 4. Adaptive representation

Compare forecasting the price directly with forecasting a normalized residual:
`z = (price - level) / scale`, then invert to EUR/MWh at the forecast origin.

For the fixed first comparison, level is the arithmetic mean and scale the sample standard
deviation of the preceding 168 available canonical hourly prices, ending at the inherited
D-1 boundary; scale floor is 1 EUR/MWh. Each training row uses its own historical-origin
statistics, never the evaluation origin's statistics or a full-series transformation.
Normalize price-valued lag predictors with that row's origin-level and scale as well; scale
price differences without subtracting the level. Freeze the unit mapping before comparison.
Other predictors retain the same definitions across paired arms, with any learned scaling fitted
on training data only. Do not delete or clip extreme target outcomes. The raw-price arm is the control.

This representation, updating and residual correction are hypotheses to test. Daily retraining
alone is neither assumed to solve the regime break nor assumed to reproduce v1's failure exactly.

## 5. CP-15 candidate set and bounded model choices

Pre-register the exact protocol in a candidate-branch commit **before model comparison runs**.
All following arms are required; letters are identifiers, not a predicted ranking.

| ID | Forecast policy | History |
|---|---|---|
| B0 | Existing similar-day naive | Inherited definition |
| B1 | Preserved v1 forecast vectors | Exact development replay, no refit |
| B2 | Daily rolling LEAR, raw target | 728 calendar days |
| B3 | Daily rolling LightGBM central forecast, raw target | 728 calendar days |
| A1 | B2 with §4 target normalization | 728 calendar days |
| A2 | B3 with §4 target normalization | 728 calendar days |
| A3 | Equal arithmetic mean of A1 and A2 central forecasts | Their histories |
| A4 | Normalized daily rolling LEAR | 84 calendar days |
| A5 | Equal arithmetic mean of A1, A2 and A4 central forecasts | Their histories |

Use LEAR's cross-hour price-lag and available exogenous-input structure; no new unavailable
feature can enter under its name. Select its regularization within the current training window
using chronological inner validation, identically for paired arms. Freeze the inner split and
finite penalty grid before comparison. Freeze one implementation and reproducible seed policy.
For B3/A2 use the inherited LightGBM p50 objective and CP-2 hyperparameters, with identical
parameters apart from the specified target transformation. No architecture or hyperparameter
search on outer-fold results. Explain any incompatibility before execution, rather than substitute.

Use precisely 728 or 84 preceding calendar days; filter by inherited admissibility. Predeclare
minimum training-row sufficiency and require complete evaluation predictions. If adequate
prehistory is unavailable, report the exact deficiency; do not silently shorten windows or
drop a fold. Caching identical historical fits is permitted if cutoffs and identity are preserved.

Also perform a **Chronos-2 feasibility probe**, pinned to an exact public model revision, on
admissible training/inner-validation data only: load, memory/runtime and external-input support.
No required full-fold neural benchmark is disguised as completed by this probe. It informs the
next experiment; it cannot win CP-15. Likewise, produce a structural merit-order input feasibility
sheet covering fuel/EUA, load, renewables, capacity/outages, vintage, access, redistribution and
missingness. Do not implement a fuel layer or train a fundamental model in this checkpoint.

## 6. Common uncertainty comparison and point-error diagnosis

For every newly fitted policy and B0, build a common **rolling signed-residual distribution** from
the previous 28 complete delivery days whose issued errors are released by §2. Warm up that
buffer using genuine pre-evaluation predictions of the same policy; freeze the warm-up rule.
For normalized arms store `(actual - issued central forecast) / issued scale`; invert with the
current available scale. Raw arms use unscaled signed errors. Ensemble normalized arms share
the same current §4 scale. No retrospectively recomputed errors from a newly fitted model.

Report the original central forecast separately. The distribution's p50 is the central forecast
plus the buffer's median signed error; it is this final p50 that enters the primary MAE.
Emit quantiles {0.025, 0.10, 0.25, 0.50, 0.75, 0.90, 0.975}. Freeze an empirical quantile
definition (including interpolation and ties) and exact fixtures before execution. This is an
empirical residual benchmark, **not** a finite-sample conformal coverage guarantee. B1 uses its
preserved final quantiles, with the same seven levels, and remains an immutable reference.

The method must produce finite, ordered quantiles without outcome-dependent clipping. Do not
invent extreme endpoints to obtain coverage. Freeze any final projection rule and score the
actual emitted vector. Report raw-central MAE, final-p50 MAE and the effect of residual centering.
Separate daily mean-level error, within-day shape error, signed bias, upper/lower misses, interval
width and post-shift recovery. Preserve aggregate metrics including all stress outcomes.

AgACI/PID and distributional neural methods are candidate directions for the next checkpoint;
they are not authorized additions to this fixed comparison. This first experiment establishes
whether better point forecasts and a simple rolling error model already change feasibility.

## 7. Scores, selection and uncertainty

Report per-fold MAE, RMSE, WIS, 50/80/95% coverage, mean/median/95th-percentile interval width,
miss counts by tail, missing predictions, fit/runtime and memory for every arm, including losers.
Report fold 3 and August 15–31 with their own dates and denominators, never interchange them.
WIS uses central intervals 50/80/95%, weights alpha/2 and median weight 1/2, normalized by 3.5.
Retain native v1 pinball in the historical record; do not rename a seven-quantile WIS as that score.

Define `S_MAE(m) = mean over five folds of MAE(m,f) / MAE(B0,f)`; similarly define S_WIS.
Use final p50 MAE. Freeze handling of a zero reference denominator: report the comparison as
undefined and request a protocol correction before selection; never divide by an arbitrary epsilon.
The equal fold weighting is deliberate so a crisis fold is not diluted by observation pooling.
Also publish pooled observation-weighted scores as secondary descriptions.

Rank A1–A5 by S_MAE, then S_WIS, then their table order for exact ties. Report the best observed
candidate even if none meets §8. Report separately the highest-ranked candidate meeting §8,
or `none`. No opportunistic replacement of the original CP-10 winner.

Provide dependence-aware uncertainty for paired daily losses using a seeded moving-block
bootstrap: resample 7-consecutive-delivery-day blocks within each fold, 2,000 replicates,
95% percentile intervals, identical resamples for paired models. Keep hourly observations
together. Report the 17-day peak descriptively with exact hit counts; flag its small effective
sample instead of an independent-hour significance claim. Any inferential statement here is
exploratory and subject to selection; no confirmatory p-value is claimed.

## 8. Product feasibility decision — distinct from Integration

These are owner-delegated engineering screening criteria, not literature guarantees or a claim
that we already know the achievable maximum. Apply them without changing them after results.

A1–A5 candidate m has `product_feasibility = DEMONSTRATED_ON_DEVELOPMENT` only if all hold:

1. S_MAE(m) is at most 0.90 times the lowest S_MAE among B0–B3.
2. S_WIS(m) is at most 0.90 times the lowest S_WIS among B0–B3.
3. Nominal 95% coverage is between 0.90 and 0.98 inclusive in **each** full fold.
4. On the matched August 15–31 slice, nominal 95% coverage is at least 0.90; both MAE and WIS
   are no worse than the corresponding best B0–B3 value on that same slice.
5. In every full fold, MAE and WIS are each no more than 1.05 times the corresponding best
   value among the rolling references B2/B3. This is a demanding per-period diagnostic comparator,
   not an implementable oracle being claimed as a deployed baseline.
6. Every eligible target has an issued forecast and finite ordered quantiles; no cherry-picked
   exclusions, suppressed failure days or altered target information.

Otherwise report `product_feasibility = NOT_DEMONSTRATED`, the failed criteria and actual values.
An Integration PASS can certify an honestly negative experiment. It **cannot** authorize freezing,
promotion or the claim that predictive quality is adequate. Put both verdicts at the top of the
report and terminal return. Do not spend time widening intervals to satisfy coverage in isolation.

## 9. Prospective product architecture, after feasibility

The eventual model of record is a **fixed forecasting policy with prescribed updates**: code,
feature contract, hyperparameters, initial state, fit schedule, delayed-error consumption and
failure policy are frozen. Parameter/state updates prescribed by that policy continue; discretionary
retuning or policy changes start a new evaluation. Timestamp forecasts before target revelation.
Measure the predictions that this same policy actually emits, including failures and staleness.

At a future freeze, record exact registry names, numeric versions, run IDs, initialization and
complete-artifact fingerprints. The later evaluator must resolve those versions from the registry,
verify fingerprints before opening outcome data, and refuse wrong/missing versions or altered
artifacts. No moving alias or local fallback substitutes for this read. Preserve per-origin input
vintages, state hashes and forecast lineage sufficient for replay. Test refusals with positive controls.

A future confirmatory horizon is at least 90 consecutive delivery days after policy freeze;
actual run and failure coverage must be reported. Scoring can consume released errors only under
the frozen update rule; the evaluator cannot tune on them. Final analysis rules and operational
metrics must be ratified before that stage starts. **No clock starts in CP-15.**

## 10. Programme sequence

| Checkpoint | Purpose | Authorization in this version |
|---|---|---|
| CP-15 | Adaptive point forecasting and common residual uncertainty; model/data feasibility probes | Complete bar below; execute only on receipt of its brief |
| CP-16 | Evidence-driven neural/structural challengers and adaptive uncertainty, resolving CP-15 limits | Direction only; exact candidates/bar require amendment and a new brief |
| CP-17 | Freeze the selected update policy and register verified initialization | Requires demonstrated feasibility and complete future bar |
| CP-18 | Run the same policy and build the live scorecard from recorded issued predictions | Requires operational and publication authorization |
| CP-19 | Evaluate the preregistered prospective policy | Requires CP-17 plus elapsed horizon and complete future bar |

Failure of CP-15 is a reason to reconsider modelling or information, not to continue to freeze.
Success does not automatically launch CP-16 or justify skipping stronger challengers. All v1
surfaces remain historical until the owner explicitly authorizes publication for a named task.

## 11. Execution resources and scope

Local Apple M3, 16 GB unified memory. Core comparison is CPU; an optional local MPS feasibility
probe is allowed with its device recorded. $0 expected external cost; the inherited $65/month
ceiling is not spending permission. Set bounded thread/memory use and report measured runtime.
Free public model downloads for the named feasibility probe are allowed after checking its
revision/license; no cloud jobs or subscriptions. No model/data upload, registry mutation,
remote experiment logging, push, PR, release, publication or mainline staging/commit is authorized.

Write new source under `src/cp15/`, driver `scripts/cp15_forecasting.py`, tests under
`tests/test_27_cp15_*.py` or `tests/cp15/`, research outputs under `reports/cp15/`, and verdicts
under `docs/track-b/evidence/cp-15/`. `pyproject.toml` and `uv.lock` may gain necessary pinned
dependencies. Reuse existing engineering code by import; do not modify preserved v1/CP-10 paths.
Large regenerated artifacts may live in a documented ignored cache with hashes and reproduction
commands; commit protocol, summary tables, manifests, report and review evidence.

## 12. Complete CP-15 acceptance checklist

1. Verify and report the starting state; preserve other sessions' work, v1/CP-10 evidence and
   restricted partitions; commit the exact v21 anchor and pre-run protocol before comparison.
2. Implement every B0–B3/A1–A5 policy in §5 and the common uncertainty construction in §6;
   prove genuine rolling fits, warm-up provenance and causal per-origin normalization with fixtures.
3. Prove §2 availability, D-2 feedback, single consumption, DST and schema refusal controls;
   each negative assertion has a positive control, including inherited live-namespace guards.
4. Produce predictions on identical original eligible hours and all metrics/diagnostics in §7
   for every arm; independently check counts, zero crossings, scores and exact window denominators.
5. Apply §7 ranking and every §8 criterion mechanically; report both Integration status and
   product_feasibility, best observed policy, qualified policy or none, and all failed criteria.
6. Deliver the pinned Chronos-2 feasibility probe and structural-input feasibility sheet in §5;
   document genuine access/resource limitations without inventing benchmark results or silently
   promoting probes into the candidate set. Such probe limitations do not block the core comparison.
7. Provide pinned reproduction commands, dependency/input/protocol hashes, seeds, chronological
   validation records, resource measurements and dependence-aware uncertainty; rerun relevant
   controls and the existing regression suite, reporting any blockers without a false PASS.
8. One fresh independent Integration Critic reviews a clean detached checkout of the exact
   final_candidate_sha, verifies every checklist item, independently recomputes saved-prediction
   metrics and performs causal control/representative fit reproduction; commit its verdict only
   after review. Record commands actually run, exit codes and limitations. No binding PASS means
   no terminal PASS. Candidate-to-evidence-tip changes are confined to this checkpoint's evidence.

## 13. Engineering Lead handoff

Read AGENTS.md, engineering-role.md and **this exact plan**, then the supplied CP-15 brief.
Do not read progress.md or orchestrator-role.md before Integration or use them for engineering.
Read engineering artifacts as needed within the information/partition boundary. Source literature
may inform implementation of the specified methods; it cannot expand the fixed candidate set.
The Orchestrator's research memo is not a competing plan or required engineering input.

Owner-authorized preparation files supplied with the brief are immutable inputs. On
`gauntlet/cp-15` only, the Lead may include the exact supplied `AGENTS.md`, `capstone_v21.md`
and brief bytes in its pre-run protocol candidate commit. The corrected rulebook must travel
with the plan because the CP-10 base commit predates its correction. This is narrowly authorized
packaging, not permission to edit governance or stage progress.md/orchestrator-role.md.
Verify the supplied rulebook and plan hashes; record the brief's hash before packaging.
Use a separate checkpoint worktree so the original CP-10 checkout is not switched or cleaned.
Keep one Git writer and the inherited fresh-Critic protocol. All work remains local.

Return PASS/BLOCKED/INCOMPLETE using the canonical §3 template, with product_feasibility beside
the engineering status, both terminal SHAs, verdict path, full checklist, elapsed time and branch/
worktree/tag accounting. Stop at that one return. Do not implement or plan later checkpoints.

Reasoning capture is active under AGENTS.md. The Lead names any interview-answer capture
trigger in one line in its terminal return; only the Orchestrator appends to the Q&A document.
This does not reopen Track A/C or permit the Lead to read or edit the document.

### Research references (motivation, not promised outcomes)

- [Adaptive target standardization](https://arxiv.org/html/2311.02610v3).
- [Forecasting the trend-seasonal component](https://arxiv.org/html/2503.02518v1).
- [AgACI](https://proceedings.mlr.press/v162/zaffran22a.html).
- [Conformal PID](https://arxiv.org/abs/2307.16895).
- [Chronos-2 Belgian study](https://arxiv.org/html/2605.17045v1).
- [Foundation models and specialist ensembles](https://arxiv.org/html/2607.02623v1).
- [Learned merit order](https://arxiv.org/html/2501.02963v1).
- [Weighted interval score](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008618).
