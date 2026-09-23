# Capstone v21-r2 — Adaptive forecasting with measured product quality (ratified)

**Owner ratification and separate CP-16 execution authorization · 2026-09-23.**
The Owner ratified the completed v21-r2 scientific specification and full CP-16 checklist,
and separately authorized execution of CP-16 only under the approved scope, claims contract
and resource ceilings. These grants follow O1–O3 approval and completed O4 document preparation;
they are not inferred from those earlier approvals. The Owner also expressly approved the
resulting status-and-identity-only successor documents without another approval round.

The grant binds these prepared identities, retained as historical inputs:

| Prepared document ratified by the Owner | Historical SHA256 |
|---|---|
| `capstone_v21.md` | `18ec0abacb80cd490c560f1027e50814e9e7f657ecd96bddf1e096af9ee33469` |
| `docs/track-b/capstone_v21-r1-to-v21-r2-amendments.md` | `af082cf0d7b2ef240cf86aefb43e605f573fbe0debe61f4ebae4a128f8302b89` |
| `docs/track-b/cp-16-v2-brief.md` | `b5c5fd66c985b60e01af8d230f89574d0cea5430e28a1882374725f7dbe920bc` |

This successor records that grant only; the experiment, full checklist, ceilings and other
substantive requirements are unchanged. The task-scoped Governance Lockdown suspension
covers only this anchor and its named amendment record for authorization/status reconciliation.
It permits no experiment in the Orchestrator recording task and transfers no governance-edit
authority to the executor. Exact successor identities are recorded downstream in the amendment,
issued brief and handoff, avoiding a self-referential hash.

The historical v21-r1 authority for CP-15 remains preserved byte-for-byte at
`evidence/cp-15:capstone_v21.md`, SHA256
`44ea4e545d2caa276a36a7a70db6ea044b3975196ead06f3ce59f976c83354b3`.
**v21-r2 is now the ratified authority for CP-16.** The research experiment is an intermediate
step toward the unchanged programme live-system objective. CP-15, its v21-r1 record and
substantive §§8–9 remain unchanged.

**Scope of this execution grant:** CP-16 follows only §14 and its issued brief. The original
CP-15-only readiness, methods, paths and handoff below remain historical CP-15 instructions;
they neither govern CP-16 entry nor replace its distinct §14 specification. Completing the
bounded research evaluation may lead to a local result and separate research disposition
without weather admission, 4.7T or live operation. The grant permits the local candidate
branch, candidate/evidence commits and exact immutable document packaging specified by the
brief and engineering role. It grants no mainline change, publication, model promotion,
registry mutation, CP-17/18/19 authority, further governance edit or prospective clock.
Historical CP-15 statements below are retained verbatim except §10's specified CP-16 row.


**Active owner-authorized execution plan · 2026-09-15.** The owner approved execution of the
research recommendation and the necessary plan change. The Orchestrator drafted this exact text
under that delegated authority; this is not a claim that the owner reviewed every sentence.
It replaces v20 for future work. Original v20 remains the historical authority for CP-10.

**Owner-authorized history correction, v21-r1 · 2026-09-16.** The owner approved §5’s
expanding history capped at 728 calendar days, retaining the deliberate 2019-01-01 boundary,
and the directly necessary resumption handoff. This is the exact active revision of
`capstone_v21.md`; the original v21 bytes remain historical authority for CP-15 attempt 1
at evidence tip `193d9cf48c586b9c4b1f43d7a5677b2d5f400832` (original plan SHA256
`62e84ceb4f35190c89faffaee4e8af01c5b3c81f9d78f9f3f68556e25f360065`). Its BLOCKED return
and Integration FAIL are not rescored. The nine-policy set, §8 product criteria and complete
§12 checklist are unchanged. The amendment authorizes one CP-15 resumption brief; it grants
no standing governance-edit permission to the Lead.

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
| B2 | Daily rolling LEAR, raw target | Expanding from 2019-01-01, capped at 728 calendar days |
| B3 | Daily rolling LightGBM central forecast, raw target | Expanding from 2019-01-01, capped at 728 calendar days |
| A1 | B2 with §4 target normalization | Expanding from 2019-01-01, capped at 728 calendar days |
| A2 | B3 with §4 target normalization | Expanding from 2019-01-01, capped at 728 calendar days |
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

For B2, B3, A1 and A2, use all admissible history from the later of 2019-01-01 or 728
calendar days before the forecast’s delivery day D, ending at the inherited availability boundary.
Apply this rule to evaluation and genuine warm-up forecasts alike. A4 uses precisely 84
preceding calendar days. Preserve minimum training-row sufficiency checks and every original
evaluation hour.

The 2019 start is deliberate: pre-2018-10-01 DE-AT-LU prices are a different market product.
No pre-2019 inputs are authorized. To count calendar days unambiguously, for a forecast
of delivery day D the long-history dates are `[max(2019-01-01, D - 728 calendar days), D)`
in the inherited market timezone, subject to the unchanged forecast-origin timestamp and
per-input availability filters. The exclusive right endpoint is the start of delivery day D;
it is not permission to use any observation unavailable when the forecast was issued.
A4 analogously uses `[D - 84 calendar days, D)`, subject to the same information boundary.
At early origins the long history expands; once the full 728 days are supported, it rolls.
Use this identical rule for the raw/normalized paired arms;
A3/A5 inherit their components’ histories. Do not extend A4 before 2019 to fill its window.

Predeclare minimum training-row sufficiency and require complete evaluation predictions.
An intentional boundary-limited long window is not itself a missing-history failure under
v21-r1. This does not excuse missing inputs within that window, insufficient eligible training
rows, unavailable row-specific normalization history, or an unsupported warm-up forecast.
Report any such remaining deficiency; do not silently shorten the authorized windows further
or drop a fold. Caching identical historical fits is permitted if cutoffs and identity are preserved.

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
| CP-16 | One existing-input v2 central-blend/hour-aware-versus-pooled research experiment | Ratified §14 specification/checklist; CP-16 execution separately authorized 2026-09-23; no promotion or later-stage authorization |
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
For the owner-authorized v21-r1 resumption, use the retained clean CP-15 worktree on
`gauntlet/cp-15` at `193d9cf48c586b9c4b1f43d7a5677b2d5f400832`, after verifying ownership
and state. The replacement brief supplies the exact revised plan and brief bytes for packaging
on that branch before comparison; the Lead may replace the branch’s working plan with those
exact bytes, but may not author further governance edits. Retain the original plan, protocol,
reports and FAIL verdict as historical evidence of attempt 1: their original committed identity
must remain reachable and any preserved copies must be byte-identical. Do not overwrite or
relabel the old verdict as a new review; if reusing the canonical verdict filename, first retain
the original unchanged at a distinct evidence path and record the mapping in the return.
No branch discard, tag, reclamation or mainline operation is authorized by resumption.
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

## 14. CP-16 — bounded existing-input v2 research experiment

**Complete specification and checklist ratified; CP-16 execution separately authorized
2026-09-23.** The numerical and scientific choices below implement approved O1–O3.
The separate execution grant is recorded above. No new product gate is substituted for §8.

Forecast origin: **D−1 11:00 UTC (12:00 fixed UTC+01:00 CET)**; delivery dates/hours use
**Europe/Berlin**, including 23/24/25-hour days. Inputs retain the **2019-01-01** floor.
Complete released errors are from days **≤D−2**, consumed once under the inherited contract.

Delivery: a local research artifact evaluating both point and interval forecasts for the
Owner/technical reader, as an intermediate step toward the programme's live-system objective.
No commercial exposure, service-level, operational, economic-qualification or promotion claim.
The candidate scope is fixed; negative and mixed results are valid research outcomes.
The existing live-system objective and separate future-stage requirements remain unchanged.

The Lead owns routine engineering fields E1–E4 within this scope, without per-parameter
Owner decisions. It freezes the exact protocol before comparison; it cannot change a
scientific contrast, ceiling or quality rule after seeing results. Material changes or
insufficient allowances require an explicit report rather than silent scope reduction.

### 14.1 Policies, population and information

- **V2-H:** 50/50 mean of genuine issued A1/B2 **central** forecasts, plus the new hour-aware
  standardized signed-residual quantiles below. Do not average already calibrated p50s.
- **V2-P:** exactly the same central forecasts, scale, issued-error history, warm-up,
  target keys, quantile convention and failure policy; use the pooled residual quantiles.
  The only changed element is hour-aware pooling/shrinkage.
- **Saved references:** B0, B1, B2, A1; also B3 strictly to report all original §8 comparator
  conditions. No new B3 fit or new challenger. Preserve B1's calibrated/projected seven
  quantiles and original v1 nine-quantile pinball as distinct evidence.
- Compare all seven output policies on the original **10,747** target keys each:
  fold counts **2,160 / 2,159 / 2,112 / 2,160 / 2,156**. Successful complete output totals
  **75,229** policy-target rows. Five 90-calendar-day windows are
  2020-07-01..09-28, 2021-04-01..06-29, 2022-07-01..09-28,
  2025-05-01..07-29, and 2026-01-08..04-07. Full fold 3 has 2,112 hours/88 represented
  days; the peak is **2022-08-15..31, 408 hours/17 days**. Never interchange their denominators.
- Component recipes, 168-hour normalization, daily rolling fits and four-penalty chronological
  inner selection remain those in `reports/cp15/protocol.json`; long training history is
  `[max(2019-01-01,D−728 calendar days),D)`, subject to each origin's availability filter.
  No model/feature/penalty search beyond this inherited component procedure.
- Filter permitted partitions **before materializing inputs**. No spent holdout, reserved tail,
  added market history, post-gate A69, delivery-day actual predictors, or new source admission.
  Outer outcomes can enter later prescribed error updates only after the fixed release rule;
  they never tune the recipe. Preserve inherited A65 vintage-availability and historical
  data-revision assumptions as limitations, not new measured guarantees.

### 14.2 Causal residual construction and fallback

Owner-ratified recipe: for every genuinely issued blend forecast `c_t`, store
`r_t = (y_t − c_t) / s_t`, where `s_t` is **that issuance's** A1 scale: sample SD of the
168 then-available canonical prices, floored at 1 EUR/MWh. At issuance use the current
available `s_D`; never normalize old residuals with today's scale. Both arms use this
same convention, including B2's contribution to the blend.

Retain the most recent **28 complete released delivery days** of blend errors, all ≤D−2.
This inherits CP-15's complete-day convention; it can span more than 28 calendar dates
across gaps. Preserve both canonical repeated-hour observations on a 25-hour day, grouped
by their Europe/Berlin local hour; never synthesize the missing spring hour or deduplicate
UTC timestamps. Update each issued pair exactly once. Report buffer age and represented
calendar span as well as counts.

For each quantile `q` in `.025/.10/.25/.50/.75/.90/.975`, compute linear empirical quantiles
using the CP-15 `numpy.quantile(method=linear)` convention:

- `Q_P(q)`: all canonical hourly residuals in the shared buffer, equal observation weights.
- `Q_h(q)`: residuals from local hour h in that same buffer.
- `w_h = n_h / (n_h + 56)`, where `n_h` is the number of canonical errors at h.
  If h has fewer than **14 distinct complete delivery days**, set `w_h=0`.
- V2-H emits `c_D,h + s_D * [w_h Q_h(q) + (1−w_h) Q_P(q)]`;
  when `w_h=0`, use `Q_P` directly without evaluating an empty `Q_h`.
  V2-P emits `c_D,h + s_D * Q_P(q)`.

The fixed 56 pseudo-observation weight gives roughly one-third hour-specific contribution
at 28 errors/hour. It is a conservative regularization choice motivated by sparse tails,
**not an optimized value or a coverage guarantee**. Convex combinations of ordered quantile
functions preserve order. No tail clipping, isotonic repair or fixed-p50 reset is proposed;
both arms' final p50 includes their own residual median and must be scored as emitted.

Validate the one fixed recipe on a **training-only** admission slice: seven delivery dates
D0−8..D0−2 before each fold's first evaluation day D0. It is an implementation/support
check, not a score-selected configuration search. Freeze it before any new outer scoring;
if it cannot run causally or lacks support, return the deficiency rather than try a new
shrinkage value. These older dates are not claimed to be project-unseen evidence.

Generate/reuse genuine component forecasts from at most the preceding **60 calendar dates**
per fold, continuing daily through the evaluation end. This allowance includes the admission
slice and its own 28-day warm-up. Identify the required dates in E1 before fitting. No
in-sample residuals or hindsight-refitted predictions can fill the buffer. Cached component
forecasts are usable only with verified input/protocol/origin identity and independent
representative reproduction; a cache miss counts as a budgeted refit.

**Failure rule:** with fewer than 28 complete released forecast days, nonfinite component
output, missing required input or failed component fit, record failed issuance and its cause;
there is no stale-component, B0 or zero-error substitution. An incomplete new day cannot enter
the residual buffer; existing valid complete days may remain under the fixed 28-day rule.
Any lost original eligible target prevents a complete evaluation/PASS. Retain expected keys,
failed-row accounting and any explicitly partial summaries without inventing a full score or
silently shrinking denominators. The per-hour small-sample fallback is the pooled layer,
not a fallback for missing common history.

### 14.3 Metrics, diagnostics and causal controls

Re-score emitted p50 MAE and seven-quantile WIS with CP-15's interval weights alpha/2,
median weight 1/2, divisor 3.5; equally average the five fold ratios to B0. Preserve pooled
hour-weighted scores as secondary estimands. Also report all CP-15 §7 metrics: RMSE,
central versus emitted MAE, centering effect, 50/80/95% coverage and width summaries,
tail misses, bias, daily level/shape error, crisis recovery, failures, runtime and memory.
Report every original §8 criterion with actual values and limits, including B0–B3 and
rolling B2/B3 diagnostic comparators; old CP-15 results remain unchanged.

Report per-hour and exhaustive local-time blocks **night 22–05, solar 10–16, shoulder
06–09 plus 17–21**, with actual counts, represented dates, hits and widths. Owner-approved support
rule for block/hour uncertainty statements: at least **56 represented dates** within a fold;
below that, publish descriptive counts but label the comparison support-limited. This is a
reporting convention (two buffer lengths), not a power calculation or a new product gate.
Peak results remain descriptive because there are only 17 days. No demand for nominal-tail
accuracy is inferred from 28 per-hour errors.

Required controls, each with a positive control that can fail: delivery-day price mutation
changes forecasts by exactly 0.0; an available D−1 mutation moves a controlled forecast;
post-gate/target-actual rejection; D−1 error rejection versus D−2 released acceptance;
consume-once/idempotency, no partial-day buffer admission, 23/24/25-hour UTC identity,
row-specific scale and training-only transforms, genuine warm-up provenance, state persistence
and restart replay, stale/wrong cache refusal, expected-row completeness, finite ordered
quantiles, and common central/buffer parity across H/P. Include sparse-hour fallback and
linear-quantile/tie fixtures. Re-run applicable existing regression and live-namespace guards
without making a live mutation. Test execution and code inspection belong to the executing Lead
and Critic, not to this Orchestrator recording task.

### 14.4 Research conclusions and uncertainty — ratified O2 contract

Use seed **15042**, **2,000** paired noncircular **7-calendar-day** moving-block bootstrap
replicates within each full 90-date fold, concatenating/truncating to 90 dates. Resample
identically across policies, retaining all hours in each selected day and preserving missing
calendar dates as missing. Recompute both policy and B0 means within each resampled fold,
then equal-fold normalized score differences. Report 95% percentile intervals; never substitute
zero loss or epsilon for missing/zero denominators. An undefined replicate or comparison is
reported as unresolved uncertainty, not silently discarded/redrawn for a favorable result.

Primary contrast: **H−P** for S_WIS and S_MAE. Secondary contrasts: **H−B2** and **P−B2**
for those same scores. Per-fold paired daily-loss uncertainty remains descriptive. All
intervals are exploratory post-selection, without family-wise or confirmatory claims.

- Rank H/P descriptively by lower S_WIS, then S_MAE, then **P** on exact ties (simpler layer).
  Rank is not a statistically supported winner or a delivery decision.
- State **observed joint improvement** for a contrast only when the S_WIS difference's
  upper interval endpoint is <0 and the S_MAE difference's upper endpoint is ≤0.
  This zero-change reference tests improvement without inventing a tolerated point-loss margin.
- Mixed point/interval outcomes, intervals spanning zero or support failures produce
  **no demonstrated joint preference**, with both metrics shown; no post-hoc tradeoff weight.
  This is not proof of equivalence, absence of benefit or absence of harm. Report the
  direction, magnitude and uncertainty of mixed outcomes explicitly.
- Engineering completion is independent of gain. A complete valid negative comparison can
  earn Engineering PASS. Historical CP-15 remains NOT_DEMONSTRATED. A newly evaluated
  policy's original-§8 diagnostic is reported separately as met/not met/unassessed; under
  this research-only route it does not itself authorize promotion, CP-17 or publication.

No new economic calculation, decision optimizer, annualization or net-value gate is included.
Historical economics can be cited only with its original population, assumptions and
post-selection limitations. A material change to this approved economic scope requires Owner authorization and
a complete economic-policy contract before execution; do not insert a battery configuration as an unapproved default here.

### 14.5 Owner-approved numerical ceilings — CP-16 execution authorized

These are Owner-approved maximum allowances, **not spending targets, measured costs or
validated runtime estimates**. The separate CP-16 execution grant is recorded above. Count warm-up, inner fits,
controls, failures, corrections and independent reproduction against the same totals. Stop
on the first exhausted hard cap; retain evidence and return BLOCKED/INCOMPLETE as appropriate.
No model-quality-driven repeat, automatic retry, new family or automatic increase is allowed.

| Dimension | Approved total cap / counting unit |
|---|---|
| New output policies | **2**: H and P; **5** saved reference policies; **7** scored policies total |
| New residual configurations / selection trials | **1** hour-aware recipe + **1** fixed pooled control; **0** alternative residual configurations or outer-score selection trials |
| Central configurations / feature recipes | **2** inherited component configurations (A1/B2), **1** common inherited LEAR feature recipe with prescribed raw/normalized representations, **0** new feature recipes |
| Seeds / ensemble members | **1** inherited model seed, 42; **1** bootstrap seed, 15042; **2** fixed component members per output; **0** seed ensembles |
| Training-only residual admission | **7** interval-issuance dates × **5** folds × **2** output policies = **70** policy-days, within the replay allowance |
| Unique component forecast dates | At most **150** per fold (90 evaluation + 60 preceding) × **5** folds; **750** date-fold keys |
| Main component fitting | At most **1,500** component-day fitting attempts (750 × 2), cache hits require no new fit |
| Total component fitting, including controls/review/failures | **2,000** component-day attempts, including the 1,500 above; remaining **500** cover representative reproduction, controls and necessary defect repair, not a second full model comparison |
| Primitive estimator fits / inherited selection | **240,000** Lasso fit attempts total: 2,000 × 24 hours × (4 inner penalties + 1 final refit). At most **192,000** inner-penalty trials and **48,000** final hourly refits, both subsets of that total. Early failure still counts; a smaller fixture does not create extra attempts. |
| Residual replay / regeneration | At most **3** full-equivalent H/P passes, **4,500** policy-days total (750 × 2 × 3), including admission, diagnostics, controls, corrections and independent review; **0** extra scored recipes |
| Saved-reference processing | At most **3** metric-only complete passes across **5** saved reference policies; **0** B0/B1/B3 model refits or new reference calibration |
| Bootstrap / uncertainty | **1** joint 2,000-replicate index set for planned contrasts per analysis pass; at most **3** analysis passes including independent verification; no seed search |
| Compute | **24 machine-hours**, aggregate elapsed execution time of all compute jobs on this one local machine, summed across simultaneous jobs; includes tests/reproduction and failed jobs, excludes human idle time; **4** CPU workers maximum, BLAS threads **1**, **0** GPU/cloud jobs |
| Active human/agent effort | Approximate checkpoint timebox **32 hours**; separate hard ceiling **40 active hours**, including protocol, implementation, corrections and review. No unlimited extension at the approximate timebox. |
| Memory / storage | **10 GiB** aggregate process-tree resident memory; **20 GiB** additional disk including worktrees, environments, caches and outputs; **0 bytes** of new dataset/model downloads |
| Other work / cost | **0** new sources/providers, weather probes, neural candidates, VRE fits, recombination searches, economic runs, operational days, automated schedules or remote mutations; **$0** external cost |

The fit counts are arithmetic envelopes from the inherited 24-hour/four-penalty recipe,
not a claim that every origin needs refitting or that the caps suffice. E1 must enumerate
actual origins and count primitive calls before launch. If adequate genuine warm-up or required
verification cannot fit within these limits, return a scoped blocker; do not drop hours,
change history or spend an unstated allowance. Distinct caps are simultaneous, not additive.
The Lead chooses work decomposition and how to allocate the totals; no fixed review-round
count is imposed. Corrections require disclosure, preserved invalid evidence and a fresh
exact-candidate review; they do not permit outcome-guided scientific tuning.

### 14.6 Engineering completion fields — Lead-owned, no new Owner ballots

| ID | Field to freeze under the adopted scope | Completion rule |
|---|---|---|
| **E1 — ENGINEERING PRE-RUN** | Exact permitted partition/key manifest, seven-day admission dates, ≤60-day warm-up dates, cache identity, fit/replay counts and missing-data feasibility | Resolve from metadata and permitted training data before comparison; verify support and totals against §14.5. Missing cache is not authority for extra fits. |
| **E2 — ENGINEERING PRE-RUN** | Dependency/code/input hashes, numerical fixtures/tolerances, output schema and exact reproduction commands | Pin inherited recipes and the approved H/P procedure; training-only validation, no new outer-score selection. Refuse discrepancies rather than silently changing the scientific contract. |
| **E3 — ENGINEERING PRE-RUN** | Resource instrumentation, preflight disk/RAM availability, cutoff/abort implementation and atomic evidence saves | Establish how all attempts/jobs count against caps before the first fit; exceeding a cap cannot be hidden by restarting a process. |
| **E4 — ENGINEERING REVIEW IDENTITY** | Lead session identity and a fresh independent Integration Critic's session identity; exact final candidate SHA and detached worktree | Accountable executor is the **Track B Engineering Lead for CP-16**; reviewer is its **independent CP-16 Integration Critic**. The Lead assigns the actual sessions under its role; the Orchestrator does not launch them. Reviewer independence and identities must be recorded, not invented in 4.0a. |

E1–E4 belong to the Lead within the approved scope and ceilings. Complete the prescribed
pre-run feasibility/accounting checks before their dependent fits/comparison. Report a
material scope change or insufficient allowance explicitly; do not return routine engineering
parameters to the Owner for approval or silently weaken the experiment to fit a ceiling.

### 14.7 Paths, isolation and immutable inputs

| Purpose | Authorized CP-16 path envelope |
|---|---|
| New engineering namespace, tests and driver | `src/cp16/`, `tests/cp16/`, `scripts/cp16_v2.py`; exact internal organization belongs to the Lead |
| Dependency consistency if needed | `pyproject.toml`, `uv.lock`; inherit existing stack by default, no model/data downloads |
| Durable protocol and lineage | `reports/v2-causal/protocol.json`, `input-manifest.json`, `lineage.json`, `artifact-manifest.json` |
| Durable experiment outputs | `reports/v2-causal/predictions.parquet`, `metrics.csv`, `diagnostics.csv`, `uncertainty.csv`, `criteria.csv`, `failures.csv`, `resources.json`, `report.md`, `reproduce.md` |
| Independent evidence and terminal return | `docs/track-b/evidence/cp-16/integration.md`, other review evidence within `docs/track-b/evidence/cp-16/`, `checkpoint-return.md` in that directory |
| Checkpoint-local ignored material | `.local/worktrees/cp-16/`, `.local/artifacts/cp-16/`, `.local/tmp/cp-16/`; no sole copy of required evidence here |
| Supplied immutable governance packaging | Exact ratified `capstone_v21.md`, named amendment record, `docs/track-b/cp-16-v2-brief.md`; only expressly authorized byte-for-byte inclusion on the isolated candidate branch |

Preserve `src/cp15/`, `reports/cp15/`, prior evidence, v1 models/data/report/public surfaces,
all other locked documents, Q&A and unrelated pending work. Reuse by import/read without
altering them. All outputs are local. The disposable branch is **`gauntlet/cp-16`**,
created only in the authorized execution task, declared with its worktrees in the return.
Only the Lead writes checkpoint Git history. No branch/worktree/tag is created during this recording task.

The Owner separately authorized CP-16 execution, including the local candidate branch,
candidate/evidence commits and byte-for-byte packaging of the exact supplied ratified anchor,
amendment record and issued brief, including their authorized status-and-identity-only
successors. The Lead may not edit those locked documents, amend its own bar, copy unrelated
pending work or stage `progress.md`. Neither the completed 4.0b suspension nor this recording
suspension transfers to the Lead. The recording suspension is spent at this task's return;
CP-16 execution authority persists within the issued brief and engineering-role boundaries.

### 14.8 Complete CP-16 acceptance checklist

Every item is mandatory. Engineering PASS does not require a positive research finding; it
does require a complete valid evaluation and fresh binding Integration PASS.

1. Verify actual repository/input state and preserve other sessions' work and all v1/CP-15
   evidence. Commit the exact ratified amendment, execution brief and complete pre-run protocol
   on the authorized CP-16 candidate branch before new model comparison; document input,
   code, dependency, budget and protocol identities and all permitted origin/target keys.
2. Implement only the fixed A1/B2 central blend, the frozen causal hour-aware residual policy
   and the otherwise identical pooled control. Freeze the two constructions on permitted
   training data before outer scoring; prove that their only difference is hour-aware pooling.
3. Prove origin availability, training-only and origin-specific transforms, D−2 release,
   consume-once, genuine warm-up, complete-day/DST identity, sparse-hour fallback, cache
   identity and restart replay, with negative assertions accompanied by positive controls.
   Preserve relevant inherited namespace guards and all prohibited-partition boundaries.
4. Produce forecasts for every original eligible target in all five folds; report exact
   shared key counts, failed issuance and original exclusions, all finite ordered quantiles
   and emitted p50 separately from central. No missing eligible forecasts, altered targets
   or silently reduced denominators can support completed-evaluation PASS.
5. Independently verify emitted-vector scores, original seven-quantile WIS and equal-fold B0
   normalization, all required per-fold/hour/block/peak diagnostics and their denominators.
   Re-score saved B0/B1/B2/A1 references and B3's diagnostic comparisons without new fits or
   overwriting historical evidence. Keep native v1 pinball separate.
6. Apply the frozen research ranking/paired uncertainty/no-preference rule mechanically,
   report both point and interval effects including negative or mixed findings, and report
   all six unchanged original §8 diagnostics. Distinguish Engineering status, historical
   CP-15 product status, new research findings and product/delivery eligibility. No demonstrated
   joint preference is not equivalence or absence of benefit; disclose mixed effects. No post-hoc
   economic threshold or research-to-product promotion is permitted.
7. Enforce and report every adopted numeric resource/candidate cap, counting warm-up, inner
   selection, failed attempts, controls, corrections and independent reproduction. At the
   first exhausted cap retain partial evidence and return the appropriate non-PASS status;
   no unauthorized scope reduction or resource extension can cure an incomplete checklist.
8. Supply durable protocol, lineage, predictions, metrics, diagnostics, uncertainty, failure/
   resource logs, notices, reproducibility manifest and executable reproduction commands.
   Run relevant controls and regression checks; disclose defects/repairs and invalidated
   outputs. All development results retain their post-selection label and inherited limits.
9. Obtain one fresh independent Integration-Critic PASS on a clean detached checkout of
   the exact final candidate, covering this entire checklist, independently recomputed
   saved-prediction metrics and representative causal/component/state reproduction. Preserve
   commands, exit codes and limits; no self-certification or unsupported PASS.
10. Return the complete canonical checkpoint packet, both terminal SHAs and a verdict-only
    candidate-to-evidence delta, reachable evidence, branch/worktree/tag accounting, elapsed
    effort and all resource totals. End at CP-16's local result, including an honest negative
    result; no next checkpoint, final live-policy selection, publication or mainline operation.

### 14.9 Entry authority and terminal boundary

The Owner ratified this specification and separately authorized CP-16 execution on 2026-09-23,
including this status-and-identity-only successor. Read `AGENTS.md`, `engineering-role.md`,
this exact ratified revision and `docs/track-b/cp-16-v2-brief.md`. The complete §14.8 checklist
controls; CP-15's §12 is not the CP-16 bar. Preserve the role's information-isolation rules.

Use the approximate 32-hour timebox and all §14.5 hard ceilings; report elapsed hours to the
nearest half hour and active/compute effort separately. Stop at the first exhausted cap,
retain partial evidence and return PASS/BLOCKED/INCOMPLETE under templates §3 as applicable.
A missing required forecast/review cannot support PASS. No automatic additional family,
comparison, budget extension, next-checkpoint planning, mainline action or publication.
Reasoning-capture triggers are named by the Lead in its return; it does not edit Q&A.
