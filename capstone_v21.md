# Capstone v21-r8 — final-product Space: what it computes and claims (Owner-authorized)

**Owner-authorized amendment, 2026-09-30.** The Owner asked for a plan that makes the Hugging
Face Space the final product's useful, informative tool: trained and updated daily, with a
"Train it yourself" button, anchored by authority and implemented once a final model exists.
New §19 anchors the research side: what the Space computes, what it may claim, and the
in-browser retraining requirement. The presentation side is PUBLISH_RULES 1.2 §7.3 (A9); the
implementation plan is `docs/track-b/final-product-space-plan-2026-09-30.md`. §19 opens no
checkpoint, designates no model, and grants no publication or scheduling authority. Every
existing line is unchanged: the headers below and §§1–18 remain byte for byte. §19 refines §16.3
and §18.2's deferral of in-browser retraining, and it governs only within that scope.

Previous v21-r7 is preserved at `c9dc364:capstone_v21.md`, SHA-256
`e6a4e301d5db080c6427f925f51e2cf69367c42225b292c78050117003aa7b0c`.

**Authority.** On 2026-09-30 the Owner granted task-wide authority for a plan anchored "split by
authority"; the exact words are quoted in
[the amendment record](docs/track-b/capstone_v21-r7-to-v21-r8-amendments.md). The grant acts as a
task-scoped Lockdown suspension. It covers this revision, PUBLISH_RULES 1.2, their records and
directly necessary consistency edits to the programme handoff and `progress.md`, and it ends at
this task's terminal return. The agent drafted this text under that delegated authority; this
is not a claim that the Owner reviewed every sentence.

---

# Capstone v21-r7 — distribution challenger: DDNN only, written in NumPy (Owner-authorized)

**Owner-authorized amendment, 2026-09-30.** The Owner withdrew TabPFN from the programme and
fixed how DDNN is built: from the start, in NumPy only, with PyTorch serving only as a
correctness check on the development machine. New §18 records both decisions for programme work
item 4.6. It opens no checkpoint, authorizes no DDNN execution, spends no budget and designates
no final product. Every existing line is unchanged: the headers below and §§1–17 remain byte for
byte. §18 refines §16.2's TabPFN example and the programme handoff's 4.6 route, and it governs
only within that scope.

Previous v21-r6 is preserved at `270a0a0:capstone_v21.md`, SHA-256
`ee402c4703d176f8181ed82966c978ad84c3c73a0cdb1d3567871f58bc867344`. CP-21's evidence binds those
bytes; v21-r7 neither reopens nor rescores it.

**Authority.** On 2026-09-30 the Owner granted full authority to edit the anchors' treatment of
DDNN and TabPFN, with the two decisions above; the exact words are quoted in
[the amendment record](docs/track-b/capstone_v21-r6-to-v21-r7-amendments.md). The grant acts as a
task-scoped Lockdown suspension. It covers this revision, that record and directly necessary
consistency edits to the programme handoff and `progress.md`, and it ends at this task's
terminal return. The agent drafted this text under that delegated authority; this is not a
claim that the Owner reviewed every sentence.

---

# Capstone v21-r6 — CP-21: three-block LightGBM on top of v3 (ratified)

**Owner-ratified 2026-09-29; CP-21 execution authorized the same day.** The Owner chose programme
work item 4.5 for CP-21, on top of v3: add a LightGBM split into three hour blocks to v3,
retrain, and publish the result for comparison in either outcome. If it improves on v3 under a
rule fixed in advance, it is adopted as v4 and becomes the base for the next extensions.
Otherwise it is documented and published as a not-adopted experiment.

**What was ratified.** The Orchestrator's draft, with two changes by the Owner:

- **D1:** a pooled attribution arm, L-P, tests whether the block split itself helps.
- **D2:** a fourth adoption condition vetoes a resolved per-fold degradation.

The Owner approved D3–D6 as recommended, with the ceilings recomputed for the added arm. New §17
specifies the checkpoint, and one CP-21 row is inserted in §10's table. Apart from that row,
every existing line is unchanged: the headers below and §§1–16 remain byte-for-byte, and §16
remains the final-product authority.

Previous v21-r5 is preserved at `81ab3be:capstone_v21.md`, SHA-256
`a4e178c30c555cc91dfbe338bbcf3e8776d67709d6dc4a72bc4f5892971003c9`.

**Authority.** The Owner granted a task-scoped Lockdown suspension of 2026-09-29. It covers this
revision, [the amendment record](docs/track-b/capstone_v21-r5-to-v21-r6-amendments.md) and
directly necessary consistency edits to the programme handoff, and it ends at that task's
terminal return. The Owner separately authorized the task to commit and push these documents.
That was a task-scoped instruction, not a standing exception. The CP-21 Engineering Lead
receives only the execution authority in §17.11.

---

# Capstone v21-r5 — final-product lifecycle amendment (ratified)

**Owner-authorized documentation amendment · 2026-09-29.** New §16 makes the
Owner-designated final version the product/demo/daily-policy identity and requires daily
retraining and issuance under a frozen policy. It governs future final-product work only.
It does not choose a model, authorize CP-21 or CP-17–19 execution, spend a budget, open
fresh data or grant publication authority. All historical §§1–15 below remain byte-for-byte
unchanged; §16 explicitly refines future §§9–10 and wins only within that stated scope.

Previous v21-r4 is preserved at `evidence/pres-2:capstone_v21.md`, SHA-256
`150bd53fa15067b1d138c95d0912f86a1e92ce74092059be09034758c1926167`.
The Owner approved the named task-scoped Lockdown suspension with “מאשר באופן מלא” after
specifying the final-product identity and page order. See
[amendment record](docs/track-b/capstone_v21-r4-to-v21-r5-amendments.md).
The suspension covers this amendment and necessary document consistency only and expires at
terminal return. Historical CP-20 acceptance remains v21-r4; later research needs its own brief.

---

# Capstone v21-r4 — direct-GFS research amendment (ratified)

**CP-20 ratified and separately authorized to execute · 2026-09-23.** Owner ratifies the
revised §15 specification and all approved ceilings, and authorizes local candidate/evidence
commits and exact immutable packaging under §15.7. This issuance changes status/identities only.
The ratified CP-16 v21-r3 bytes remain at `evidence/cp-16:capstone_v21.md`, SHA256
`67d2176865fea4d6ada0b13bafb128016970d78337d5a936890ddbff7c3ad6ed`.
The historical text below is retained; CP-16 is closed per its landing record, not resumed
by this document. Only new §15 governs the authorized CP-20 weather experiment. CP-17–19 and
all existing substantive requirements remain unchanged.

---

# Capstone v21-r3 — Adaptive forecasting with measured product quality (ratified)

**Owner-ratified resource amendment and CP-16 resumption authorization · 2026-09-23.**
The Owner ratified exactly the §14.5 cap/counting change: **6 full-equivalent H/P passes /
9,000 cumulative policy-days**, retaining the entire **3,730** historical debit and all other
resource ceilings/debits, scientific requirements, candidates, data boundaries, metrics and
claims. The forward-looking rule and resumption conditions are specified in §14.5. This is a
maximum allowance, not a spending target or guaranteed feasibility; no reset or retrospective
monitoring compliance is granted. The Owner expressly authorized resumption under the resulting
consistent anchor/issued brief and these implementing successors without another approval round.

The task-scoped suspension covers this anchor's §14.5 and directly necessary revision/status/
accounting references, plus `docs/track-b/capstone_v21-r2-to-v21-r3-amendments.md` only.
It ends at this Orchestrator task's return and transfers no governance-edit authority to the
Lead. No experiment or executor launch occurs in this document task. The existing authorized
local candidate/evidence workflow and exact immutable packaging remain available to the Lead;
no mainline staging/commits/merges, publication, later checkpoint or other governance edit.

**Resume the existing CP-16 checkpoint.** Preserve `gauntlet/cp-16`, the reviewed candidate
`3a160fd33ed92bb0061144cfbce2323d8b3a7db9`, evidence tip
`41b0e6d222a3d65d474ac5974c6eb7017db317e8`, independent FAIL, interrupted evidence and all
historical limitations. No scientific result follows from that interrupted attempt. The Lead
performs the §14.5 feasibility/accounting and evidence-regeneration conditions before dependent
experimental work. Weather admission under programme §4.1 is not a prerequisite.

Historical issued v21-r2 identities (exact bytes retained at the evidence tip above):

| Historical document | SHA256 |
|---|---|
| `capstone_v21.md`, v21-r2 | `a05700ef6de700a956f6d8725cd45ecbc13f2384f780c309fffc5ba835d80a2d` |
| `docs/track-b/capstone_v21-r1-to-v21-r2-amendments.md` | `09c663359ac2471a8adbc9865d8cbfa2a25e86062aebf8428411bb74614fadab` |
| `docs/track-b/cp-16-v2-brief.md` | `1545089898aa47aa5384f5c6bcd07fda5ec7c0c98649cb44f2adba26cd0667ee` |

Historical prepared identities from the original v21-r2 ratification remain:

| Prepared document ratified by the Owner | Historical SHA256 |
|---|---|
| `capstone_v21.md` | `18ec0abacb80cd490c560f1027e50814e9e7f657ecd96bddf1e096af9ee33469` |
| `docs/track-b/capstone_v21-r1-to-v21-r2-amendments.md` | `af082cf0d7b2ef240cf86aefb43e605f573fbe0debe61f4ebae4a128f8302b89` |
| `docs/track-b/cp-16-v2-brief.md` | `b5c5fd66c985b60e01af8d230f89574d0cea5430e28a1882374725f7dbe920bc` |

Historical v21-r1 for CP-15 remains at `evidence/cp-15:capstone_v21.md`, SHA256
`44ea4e545d2caa276a36a7a70db6ea044b3975196ead06f3ce59f976c83354b3`.
v21-r3 is the current CP-16 authority; the research step serves the unchanged live-system
objective. The complete §14.8 checklist and substantive §§8–9 remain unchanged. CP-16 follows
§14 and its issued brief; the original CP-15-only readiness, methods, paths and handoff below
remain historical instructions, not CP-16 entry authority. No publication, model promotion,
registry mutation, CP-17/18/19 authority or prospective clock follows. Original CP-15 text
is preserved except the previously amended §10 CP-16 status row.


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
| CP-16 | One existing-input v2 central-blend/hour-aware-versus-pooled research experiment | Ratified v21-r3 §14 specification/checklist; CP-16 resumption authorized 2026-09-23 under §14.5; no promotion or later-stage authorization |
| CP-20 | Direct-GFS paired ablation: weather-augmented minus no-weather V2-H | Ratified v21-r4 §15; CP-20 execution and §15.7 immutable packaging authorized 2026-09-23; research only |
| CP-21 | Programme 4.5 on top of v3: HG plus a fixed three-block LightGBM member, compared with HG; adoption as v4 or a not-adopted branch under §17.6 | Ratified v21-r6 §17; CP-21 execution authorized 2026-09-29 under §17.11; research only |
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

**Complete specification/checklist remain ratified; CP-16 resumption authorized 2026-09-23.**
O1–O3 remain controlling except the expressly amended §14.5 cap/counting rule in v21-r3.
The resumption grant is recorded above. No new product gate is substituted for §8.

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

### 14.5 Owner-approved numerical ceilings — v21-r3 resumption authorized

These are Owner-approved maximum allowances, **not spending targets, measured costs or
validated runtime estimates**. The CP-16 resumption grant is recorded above. Charge warm-up,
inner fits, controls, failures, corrections and independent reproduction to their applicable
counters under the rule below; carry forward every historical debit. Stop
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
| Residual replay / regeneration | At most **6** full-equivalent H/P passes, **9,000** cumulative policy-days total (750 × 2 × 6), including admission, diagnostics, controls, corrections and independent review; **0** extra scored recipes |
| Saved-reference processing | At most **3** metric-only complete passes across **5** saved reference policies; **0** B0/B1/B3 model refits or new reference calibration |
| Bootstrap / uncertainty | **1** joint 2,000-replicate index set for planned contrasts per analysis pass; at most **3** analysis passes including independent verification; no seed search |
| Compute | **24 machine-hours**, aggregate elapsed execution time of all compute jobs on this one local machine, summed across simultaneous jobs; includes tests/reproduction and failed jobs, excludes human idle time; **4** CPU workers maximum, BLAS threads **1**, **0** GPU/cloud jobs |
| Active human/agent effort | Approximate checkpoint timebox **32 hours**; separate hard ceiling **40 active hours**, including protocol, implementation, corrections and review. No unlimited extension at the approximate timebox. |
| Memory / storage | **10 GiB** aggregate process-tree resident memory; **20 GiB** additional disk including worktrees, environments, caches and outputs; **0 bytes** of new dataset/model downloads |
| Other work / cost | **0** new sources/providers, weather probes, neural candidates, VRE fits, recombination searches, economic runs, operational days, automated schedules or remote mutations; **$0** external cost |

**Forward-looking counting rule — Owner-ratified v21-r3, 2026-09-23.**

Purely synthetic fixture and state tests, which use no real research data, are charged to
the compute, memory, storage and effort ceilings but not to the policy-day counter.

Forecast/state replay using real research data remains charged to the policy-day counter
using the existing policy-day unit, including warm-up, controls, failed attempts and
independent reproduction. Calling a replay a “test” does not exempt it.

Model fitting remains charged to the existing component-day and primitive-fit counters.
This amendment neither changes those units nor creates an additional policy-day charge for
each primitive estimator fit. Real-data replay performed alongside fitting still incurs its
applicable replay charge.

The historical **3,730** debit stands in full under its original accounting basis and is not
re-scored under this rule. The revised cumulative ceiling therefore leaves **5,270** policy-days
for subsequent work under the revised counting rule. Every other resource debit is preserved.
This change is forward-looking. It does not retroactively establish compliant accounting or
monitoring, and it grants no reset. The allowance is a maximum, not a spending target or a
guarantee of feasibility.

**Resumption conditions.** Before further experimental execution, the Lead checks that all
remaining work fits the revised accounting and every other remaining allowance, and reports
the estimate, including admission, production, necessary controls and independent verification.
Historical monitoring gaps remain disclosed. Regenerate evidence from inadequately monitored
work wherever it is required to support scored results or acceptance criteria. Preserve the
original evidence and its limitations; later monitoring does not prove historical compliance.
Preserve the existing candidate branch, evidence, independent FAIL verdict and all debits;
resume the existing checkpoint, without discarding it or restarting from scratch. The Lead
owns feasibility, resource allocation, monitoring repairs and independently verified completion
within this scope; these are execution responsibilities, not further Owner parameter decisions.
The required independent Integration review and complete acceptance criteria remain unchanged;
no scientific result is inferred from the interrupted attempt. Weather admission under
programme §4.1 is not a prerequisite for this resumption.

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
retained for this authorized resumption, declared with its worktrees in the return.
Only the Lead writes checkpoint Git history. No branch/worktree/tag is created during this recording task.

The Owner authorized CP-16 resumption on its existing candidate branch, including local
candidate/evidence commits and byte-for-byte packaging of the supplied v21-r3 anchor,
`docs/track-b/capstone_v21-r2-to-v21-r3-amendments.md` and issued CP-16 brief. Preserve the
previous immutable documents in the existing commit history. The Lead may not author locked
documents, amend its own bar, copy unrelated pending work or stage `progress.md`. This scoped
suspension ends at the Orchestrator's return and does not transfer to the Lead; the resumption
grant persists within §14.5, the issued brief and engineering-role boundaries.

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

The Owner ratified the v21-r3 cap/counting change and authorized CP-16 resumption on
2026-09-23, including its consistent successors. Read `AGENTS.md`, `engineering-role.md`,
this exact ratified revision and `docs/track-b/cp-16-v2-brief.md`. The complete §14.8 checklist
controls; CP-15's §12 is not the CP-16 bar. Preserve the role's information-isolation rules.

Use the approximate 32-hour timebox and all §14.5 hard ceilings; report elapsed hours to the
nearest half hour and active/compute effort separately. Stop at the first exhausted cap,
retain partial evidence and return PASS/BLOCKED/INCOMPLETE under templates §3 as applicable.
A missing required forecast/review cannot support PASS. No automatic additional family,
comparison, budget extension, next-checkpoint planning, mainline action or publication.
Reasoning-capture triggers are named by the Lead in its return; it does not edit Q&A.


## 15. CP-20 — direct-GFS paired research ablation (v21-r4 ratified)

**Ratified and separately authorized for CP-20 execution, 2026-09-23.** Owner approves the
revised three-feature specification and all §15.5 ceilings, including 120 aggregate machine-hours.
Owner D1/D3 select research only; D2 fixes the comparator and endpoint rule below.
This issuance records authority and identities only; the approved scientific and resource
requirements are unchanged. The task-scoped recording suspension ends at the Orchestrator's
terminal return and grants no Lead authority to edit governance. CP-17–19 retain their roles and are not opened. This is programme 4.4D,
not VRE modelling, product qualification, an economic experiment or prospective operation.

### 15.1 Inheritance, population and arms

Inherit §§14.1–14.4 unchanged for original target keys/folds, component training/selection,
normalization, chronology, H residual construction, metrics/diagnostics, bootstrap mechanics
and evidence labels, except the explicitly replaced arms, weather treatment and contrasts
here. Inherit §§2–3, all six §8 diagnostics and §9 restrictions. Preserve historical CP-15/16
results, FAILs, debits and limits. §14 remains the unchanged historical CP-16 contract.

- **H0:** no-weather V2-H exactly as §14.2: inherited A1/B2 50/50 central blend and H layer.
- **HG:** the same A1/B2 recipes with only the §15.2–15.3 weather columns appended to each
  hourly regressor; same 50/50 central blend, price-only A1 scale, H recipe and failure rules.
  Each arm uses its own genuinely issued central errors, but identical buffer dates,
  release/support/update rules. Do not share residual values across different forecasts.
- Same histories, eligible rows, chronological four-penalty selection procedure, numerical
  settings and fixed seed 42; selected penalties may differ because inputs differ. No extra
  interaction, lag, feature subset, blend weight or residual tuning. No pooled-P arm here.
- Reuse identity-verified H0/component caches and five saved B0/B1/B2/B3/A1 references;
  independent representative H0 reproduction must match accepted CP-16 vectors. HG components
  must be fitted with their own causal weather inputs, not relabelled cached no-weather fits.
- Both arms cover exactly §14.1's **10,747** keys (including fold 5 through **2026-04-07**):
  **21,494** contrast rows; with five saved references, **75,229** scored rows. Preserve
  original exclusions; missing weather never removes a target or shortens price history.
- Freeze the existing CP-16 input-manifest's **638 fold/date origins**, 35 training-only
  admission dates and genuine warm-up (2020-05-25 / 2021-02-23 / 2022-05-25 / 2025-03-22 /
  2025-12-02). No earlier warm-up search. The §14.2 60-date limit remains an outer bound.

### 15.2 Admitted source, conversion and one weather recipe

Use only operational **GFS 0.25° D−1 00 UTC** via the dossier's NCAR d084001 / NOAA AWS
endpoints. Admission is accepted for the inventoried scope under its disclosed assumptions:
NCAR-only field presence is inferred from file integrity/size plus sampled version layouts;
public availability before D−1 11:00 UTC is **reconstructed availability**, not a daily-delivery
guarantee. NCEP completion averages do not independently establish public dissemination lag.
Carry these assumptions, known endpoint defects, source fingerprints and the post-sample
radiation-precision-check disclosure into protocol/report. Admission does not certify live use.
ICON remains NOT_ADMITTED and is excluded. No reanalysis, hindcast, later cycle or pre-2019 input.

The dossier inventoried 2,468 runs using CP-15 warm-up. This CP-16-style warm-up requires
**2,476** unique runs: the extra **2023-03-24..31** eight runs must receive targeted GFS
field/lead/availability checks before fitting. Do not label them already admitted. Verify
actual field metadata during extraction, including previously inferred NCAR fields; a material
contradiction to admission or unsupported version/units stops the task with evidence.

Freeze this single conversion before fitting or scoring:

1. Decode u/v at **10 m and 100 m above ground** (m/s) and surface **DSWRF** (W/m²).
   Pressure levels never substitute for above-ground heights. Validate init/valid time,
   grid, forecast status and version per message. Needed endpoints are f021,024,…,048.
   Use the inventoried endpoint; for added runs use AWS first. At most one same-product
   alternate-endpoint attempt per failed object; compare metadata, retain hashes and defects.
2. Wind: linearly interpolate each component between bracketing three-hour endpoints to
   canonical delivery-hour starts **h22–h46**, with no extrapolation. Then compute
   **sqrt(u²+v²) per grid cell**, separately at **10 m and 100 m**, before spatial averaging.
   Radiation: at each grid
   point recover three-hour means from documented six-hour-reset averages: use A(L−3,L)
   directly at L≡3 mod6, otherwise **2A(L−6,L)−A(L−6,L−3)** at L≡0 mod6. Assign the block
   mean to each constituent hour [h,h+1); no solar-shape disaggregation or extra interpolation.
   Validate actual averaging bounds, not lead number alone. For negative block means, permit
   only values ≥−3q, q=max packing quantum of contributing messages; clip those to zero
   before aggregation and log count/magnitude/version. Below −3q or unknown quantum/bounds
   is a conversion failure, not a fitted tolerance. Disclose coarse v14/v15 precision.
3. Use the fixed rectangular proxy **47–55.25°N, 5.5–15.5°E**, inclusive grid centres,
   cosine(latitude) area weights normalized over that fixed grid. Apply them to the per-cell
   wind-speed magnitudes at each height and to converted DSWRF, separately per hour. Mean
   wind speed is the weighted mean of cell speeds, not the magnitude of mean u/v.
   No power curve, capacity weights, learned geographic mask, VRE conversion or provider search. Call it
   a regional weather proxy, not an exact DE-LU polygon or power-generation forecast.
   Do not renormalize over missing cells. Nonfinite required support makes the weather vector
   missing under §15.3. Store grid/weights, units and conversion fingerprints.
4. Append only **three same-target-local-hour weather columns** to each A1/B2 hourly design:
   **mean wind speed at 10 m, mean wind speed at 100 m, mean DSWRF**. Inherited imputation
   adds their **three missing indicators**. The five native extraction fields remain
   **u10, v10, u100, v100 and DSWRF**. No cross-hour expansion or feature search.
   On repeated local hours average the two canonical weather vectors as the inherited LEAR
   local-hour design does; preserve both canonical outputs/targets. A missing spring hour
   remains absent. Require all repeated-hour inputs or mark the local-hour vector missing.

### 15.3 Missing-input and transform rule

Weather for **delivery 2019-01-01 is structurally missing** because its run would be
2018-12-31; do not import it or remove its otherwise eligible training row. For any confirmed
missing/late/nonfinite weather vector after the bounded endpoint attempts, set all three
derived weather columns missing and mark all three indicators. Apply the inherited CP-15 LEAR
imputer/scaler: per-feature **training-partition median**, all-null column → 0, missing
indicator per feature, then training-only StandardScaler. Fit them independently inside each
inner-training split and final training window; never use validation/outer outcomes or future
weather to impute. No interpolation across dates, forward fill or zero-radiation shortcut.
This is the same rule in training, admission, warm-up and evaluation. HG still emits its own
fitted-component/H forecast; it does not switch silently to H0 or borrow H0's residuals.

Complete the required extraction/status ledger before fitting: classify structural missing,
confirmed archive absence, documented lateness and invalid support separately. Failed/unattempted
retrieval due to exhausted resources, absent admission evidence or unknown schema is **BLOCKED**,
not missing-data imputation. Confirmed missing weather is an explicit part of the HG policy;
report dates/counts and all-imputed origins, not an unqualified complete-weather claim.
Price/load/component/state failures retain §14.2's failure rule; weather fallback cannot cure
insufficient common history, an invalid fit or a missing eligible forecast. Freeze the recipe,
conversion fixtures and complete missingness manifest before any fit/outer scoring.

### 15.4 Comparison and claims

The sole primary contrast is **HG − H0**, for each paired equal-fold normalized score.
Use §14.4's seed 15042, one shared 2,000-replicate seven-calendar-day block index set per
analysis pass and its exact paired score-difference/95% percentile procedure. Apply
**upper CI(ΔS_WIS)<0 AND upper CI(ΔS_MAE)≤0** to those differences, not to marginal-score
intervals or point estimates. Otherwise report **no demonstrated joint preference**, with
mixed outcomes/undefined intervals explicit; never equivalence or absence of benefit/harm.
If descriptive ordering is reported, lower S_WIS then S_MAE, with H0 on exact ties; it is not
promotion. Original §8 diagnostics are unchanged for both arms, with saved B0–B3 comparators.
Keep all §14.3 per-fold/hour/block/peak diagnostics and §14.4 scientific limitations.
All results are **development_post_selection**. Historical economics is descriptive only;
zero new economic runs/thresholds. Negative results complete valid research; no result opens
VRE, CP-17–19, public surfaces, live selection or a prospective clock.

### 15.5 Owner-approved ceilings — CP-20 execution authorized

**D4 approved, 2026-09-23:** 120 aggregate machine-hours; all other caps below approved as
drafted. These are **CP-20-specific** ceilings, not feasibility guarantees, estimates or targets.
The Lead retains the existing pre-run feasibility responsibility. No transfer of CP-16's unspent allowance
or reset of its 6,458 policy-days/other debits. Report prior-task totals separately from new
CP-20 increments. Use §14.5's counting units and forward-looking synthetic-test/real-replay/fit
distinctions unchanged. Charge preparation, failures, warm-up, controls, repairs and independent
review to applicable caps. Stop before the first exhausted cap and retain partial evidence.

| Dimension | Owner-approved maximum |
|---|---|
| Policies/configurations | **2** arms, **5** saved references, **7** scored policies; **1** weather feature/conversion/missingness recipe, **1** fixed H recipe; **2** inherited A1/B2 component recipes per arm; **2** components/blend, weight 1/2; **0** additional ensembles/configurations/outer-selection trials |
| Seeds/inner selection | Fixed fitting seed **42**, bootstrap seed **15042**; no seed search; **4** inherited penalties per hourly fit, same chronological inner split/tie rule |
| Dates/main fits | **638** fold/date origins/arm, **35** admission dates/arm within those, ≤**60** warm-up dates/fold; **3,000** main component-day attempts across both arms (contains cache misses; nominal all-fresh need 2×638×2=2,552) |
| All fitting | **4,000** component-day attempts total; **480,000** primitive Lasso attempts: ≤**384,000** inner and ≤**96,000** final refits (4,000×24×(4+1)); retries/solver continuations count, not extra recipes |
| Replay | **9,000** new policy-days total; ≤**6** full-equivalent paired passes (conservative envelope 750×2×6); actual reused/recomputed real-data state work charged under §14.5 |
| References/uncertainty | **3** metric-only full reference passes; **3** bootstrap analysis passes including independent review, **2,000** replicates each; **0** new B0/B1/B3 fits/reference calibration |
| Weather/extraction | **1** product, **2** named access endpoints; **2,476** unique 00 UTC runs; **5** fields×**10** leads/run (≤**123,800** target messages); **3** decode/extraction attempts per target message including retries/review; **160 GiB** cumulative new transfer including metadata, dependencies, failed/duplicate requests; **0** whole global multi-field run-file downloads or unrelated data/model downloads |
| Compute/effort | **120 aggregate machine-hours** including network/extraction jobs, summed across concurrent jobs; **4** workers, BLAS **1**, **0** GPU/cloud; approximate **64-active-hour** timebox, hard **80 active hours** including verification/return |
| Memory/storage/cost | **10 GiB** aggregate process-tree RSS; **40 GiB** additional peak disk including environments/worktrees/cache/evidence; **$0**; inherited admission cache (~1.73 GiB) measured as retained baseline, not deleted or hidden |
| Other work | **0** ICON/VRE/neural candidates, feature/recombination searches, new economic runs, operational days, schedules or remote mutations |

Rationale: the dossier estimates ~101 GiB of target-message payload and ~55 sequential NCAR
hours plus 7–22 AWS hours. Transfer/compute margins cover indexes, failures and review; they do
not prove feasibility. Stream verified messages to bounded regional artifacts; retain original
sample raw files, per-message hashes/URLs and reproducible acquisition records. Do not retain
~101 GiB of globals under a 40 GiB disk cap. No unverified NCSS shortcut is included.
Before dependent work, the Lead completes §14.6 E1–E4 for **CP-20**, estimating extraction,
admission, production, controls and independent verification against every cap. Insufficient
allowance/material discrepancy returns a concrete blocker, not a new unapproved recipe.

### 15.6 Complete CP-20 acceptance checklist

All ten items are mandatory. They inherit the verification standard of §14.8; the weather
additions and H0/HG scope replace CP-16-specific H/P wording, not its scientific safeguards.

1. Verify repository/input state, retain prior evidence and other-session work; after Owner
   ratification/execution grant only, package exact supplied anchor/amendment/brief and commit
   the frozen protocol/input/conversion/missingness/budget manifests before comparison.
2. Close the eight-run admission extension; validate all extracted field/lead/version metadata,
   source/endpoint identity and historical availability basis. Preserve inferred versus decoded
   evidence, 2019 structural missingness and all dossier exceptions; record every extraction gap.
3. Implement exactly H0/HG and the frozen conversion/fallback; show only the predefined weather
   treatment differs. Verify H0 against accepted CP-16 vectors and reproduce representative
   weather-component fits. Training-only admission must precede outer scoring; no tuning to gain.
4. Prove §14.8 item 3's causal/state/DST/cache controls, plus positive/negative weather-origin,
   accumulation, units, packing/clipping, aggregation and missingness controls. Verify pre-2019
   refusal and independent reconstruction from retained raw samples without rerunning admission.
5. Produce all original eligible keys for both arms and the required reference metrics; no
   denominator changes. Independently verify emitted p50/ordered vectors, all §14.3 diagnostics
   and support counts, including fallback incidence; inherited failures still preclude PASS.
6. Apply HG−H0 paired endpoint rule and all six original §8 diagnostics; keep point/interval
   effects, uncertainty, negative/mixed findings, post-selection labels and research/product
   distinctions. No promotion, economic threshold or claim of guaranteed availability/coverage.
7. Enforce/report every §15.5 cap from the first job, all attempts and independent review;
   preserve historical debits/monitoring limitations. Exhaustion yields BLOCKED/INCOMPLETE,
   never implicit permission to impute unfinished extraction or shrink evaluation.
8. Supply protocol, lineage, decoded weather/features, predictions, metrics/diagnostics,
   uncertainty, criteria, failure/resource logs, rights notices and executable reproduction
   commands; preserve invalid outputs/repairs and run relevant inherited regression guards.
9. Obtain **one fresh independent Integration-Critic PASS** binding the exact final candidate
   in a clean detached checkout and this entire checklist, with independent saved-vector
   metrics/paired uncertainty and representative conversion/component/causal/state reproduction.
10. Return canonical packet, final candidate and evidence-tip SHAs, evidence-only terminal
    delta, reachable history, all resources and branch/worktree accounting; stop at CP-20's
    local result. No mainline action, publication, later checkpoint or executor self-ratification.

### 15.7 Paths and entry authority

Under the recorded CP-20 execution authorization: `src/cp20/`, `tests/cp20/`,
`scripts/cp20_weather.py`, `reports/weather-ablation/`, `docs/track-b/evidence/cp-20/`,
`pyproject.toml`/`uv.lock` if necessary; ignored material under `.local/{worktrees,artifacts,tmp}/cp-20/`.
Use admitted files read-only from `reports/weather-admission/` and `.local/weather-admission/`;
put extended inventories/extraction evidence in `reports/weather-ablation/`. Preserve CP-15/16
code, reports, data, model registries, public surfaces, Q&A, progress and all other locked files.
Include the exact accepted `reports/weather-admission/` bundle and intake receipt in the
candidate when absent from its base; preserve their manifest identity, without revising them.

Accountable executor: CP-20 Engineering Lead; reviewer: its fresh independent Integration
Critic under `engineering-role.md`. The Owner separately authorizes local
`gauntlet/cp-20` candidate/evidence commits and exact immutable packaging of this ratified
anchor, `docs/track-b/capstone_v21-r3-to-v21-r4-amendments.md` and
`docs/track-b/cp-20-direct-weather-brief.md`, together with the admission package above.
Ratification and CP-20 execution authority are **GRANTED, 2026-09-23**. The Lead owns the
existing pre-run checks, including feasibility and the eight added GFS runs; no further Owner
approval is needed unless a concrete blocker exceeds this scope. No scientific/budget change,
later checkpoint, governance edit, mainline operation or publication is authorized.


## 16. Final-product lifecycle — Owner amendment, v21-r5

### 16.1 Selection, freeze, rollout and evaluation are distinct

When the Owner designates an exact version as final, record that version as the selected
product and the mandatory target of the product panel, primary demo and daily operation.
One policy/version must serve all four roles at completed rollout. A research leader or
new experiment does not replace it automatically. An incoming selection with unfinished
prerequisites remains explicitly selected/pending; do not claim it runnable or relabel the
old demo. The previous product remains identified honestly until the replacement works.

Complete the admitted development and protected unused-data comparison, record the final
selection and qualification disposition, then execute authorized CP-17 freeze and CP-18
operation. Owner designation is a product decision, not statistical proof or permission to
skip those gates. No model, including current HG or immutable v1, is designated by this text.
The §8 historical failed criteria and research evidence classes are unchanged.

### 16.2 What freezes and what updates every day

Freeze code and dependencies, algorithm/architecture, feature and source-availability
contracts, hyperparameters, training-window and label-delay rules, initial artifact/state,
randomness, refit schedule, uncertainty/calibration updates, scoring/decision rules and failure
policy. Store numeric registry versions and initialization fingerprints as §9 requires.

For the selected final product, **daily retraining, eligible input refresh and forecast
issuance are required on every delivery day**. Each successful fit produces a versioned
artifact with its training window, available labels, seed, timestamps and parent/input/state
hashes. Use only information available at the fixed origin. Daily fitting changes weights/state
within the frozen policy, not the adopted generation; discretionary tuning or changing that
policy requires a new freeze and evaluation. Never overwrite an issued forecast after outcomes.

The future brief fixes numeric origin/deadlines, windows, resource ceilings and the exact
meaning of a successful daily fit before the fresh-data replay/final freeze. Input refresh,
residual-state maintenance or TabPFN context replacement alone is not weight training. A
candidate unable to meet daily retraining within admitted licensing/resources needs an explicit
Owner-approved exception specifying its real update mechanism and public wording before live
admission; no alternative cadence or exemption is silently inferred from model family.
Immutable historical v1/reference artifacts remain untouched; this requirement does not
retroactively retrain them or force every research comparator to train daily.

Daily operation covers all delivery days, including DST and Friday/Shabbat. No manual Owner
work is scheduled on Friday/Shabbat; the operational brief must reconcile coverage through an
explicitly authorized unattended schedule and incident/fallback policy. Publication authority,
operator ownership, monitoring, permissions and resources must be settled before launch. This
amendment creates no automation or standing authority to publish externally.

For missing inputs/labels, failed training, resource exhaustion or source outage, apply the
frozen fallback/staleness limits or record failed issuance. Display a failed/skipped fit as
such, even if a valid fallback produces a forecast. Do not count retained weights as a new
successful training run or backfill a late forecast as timely. Failures remain in the record.

### 16.3 What the product and demo expose

The product panel comes first, followed by How the product works, scientific Product results,
Business insights, How the models compare and all remaining sections in their existing order.
[PUBLISH_RULES 1.1](docs/PUBLISH_RULES.md) §§5, 5.1a, 7.2 and A8 define presentation acceptance.
The twelve-subject product coverage follows the actual final policy and its dated artifacts;
the outgoing product's evidence stays historical. The primary demo uses the same product policy,
and identifies the artifact/issue date and whether an interaction is a counterfactual scenario.
An old replay may remain as labelled history, not as a different primary product.

Show today's issued hourly forecasts versus available published outcomes, a defined percentage
performance measure alongside MAE in EUR/MWh, and tomorrow's issued hourly forecasts and prediction
intervals. Freeze the percentage formula, denominator, eligible population, scoring window,
zero/negative-price treatment and any success tolerance before evaluation. A benchmark-relative
percentage is labelled improvement, not correctness. Missing/pending outcomes are unscored;
partial-day scores show completeness. Scoring uses the artifact that issued the prediction,
not a newer fit. Record the price source, publication/revision times and outcome eligibility.

Distinguish nominal prediction-interval level from measured coverage and width on an explicitly
named past window. Neither means a point price has that percentage probability of being correct.
Display separate last-training, data-refresh and issuance times, delivery date/timezone,
freshness and failure state. No data or no evidence means a labelled unavailable state.

Scientific graphics separate development, unused-data and prospective results. Business
interpretation must separate forecast performance from an evaluated economic decision policy.
Cumulative net profit/value, returns or business success rates require a frozen use case,
constraints, costs, benchmark, denominator, complete time series and loss/risk disclosure;
label simulated versus realized results. Without authorized evaluation, show the specific gap
and measured forecasting implications. This is no authorization for trading, a new economic
experiment or a fabricated profitable result; programme §4.E governs such evaluation.

### 16.4 Delivery and acceptance obligations for future briefs

| Stage | Required addition to the full future checkpoint bar |
|---|---|
| Before fresh-data test | Replay the intended daily refit/update and issuance contract; freeze scoring and any evaluated economic policy before outcome access; retain the protected test boundary |
| CP-17 | Owner's final-version designation, prerequisites/disposition, policy/initialization and registry identities, daily fit and failure rules, metric formulas, resource and calendar plan |
| CP-18 | Actual scheduled training/issuance and outcome reconciliation, one product/demo identity, complete documentation/results/business sections, daily public panel and independent public acceptance |
| CP-19 | At least 90 consecutive delivery days after final freeze under §9; count real timely forecasts and failures, verify registry lineage, evaluate without tuning or excluding bad days |

Live observations and the matching demo may be published at authorized CP-18 with the label
“prospective evaluation in progress”; do not wait for CP-19 to show operation, and do not claim
completed validation before it. Public acceptance checks actual hosted output and daily records;
local fixtures do not establish daily operation. Include positive controls for altered identities,
future-label leakage, stale/failed fits, missing/zero/negative prices and partial/DST days, plus
reproducible percentage, interval and authorized business-series derivations. The full existing
independent, browser, accessibility and publication contract still applies.

No checkpoint starts here. The numeric future briefs and approved budgets remain necessary;
this amendment resolves the required product outcome, not experimental results or implementation.


## 17. CP-21 — three-block LightGBM on top of v3 (v21-r6, ratified)

**Ratified by the Owner on 2026-09-29; execution authorized under §17.11.** This is programme
work item 4.5, reframed by the Owner's choice: the three-block LightGBM is tested as an
addition to v3 (HG), not as a replacement for it. The result is published in either outcome
(§17.9). It is adopted as
`v4 · <adopted change>` under §17.6; otherwise it becomes a descriptive branch marked
"Not adopted". CP-21 is research only. It releases no product and triggers no promotion,
CP-17 freeze, prospective clock, economic run or publication by itself. CP-17–CP-19 stay
reserved (§§9–10 and §16).

### 17.1 Question, inheritance and evidence class

**Question.** HG's central forecast is a blend of two linear LEAR components. Does adding a
three-block LightGBM member, built with exactly HG's information, improve on HG jointly in
point and interval accuracy, on CP-20's development population? HG's hour-aware interval
layer is re-estimated on the new forecast's own issued errors.

**Why on top of v3.** The saved daily LightGBM B3 scores S_MAE 0.7841 / S_WIS 0.7399; HG scores
0.5658 / 0.5322. The programme's optimistic estimate for a standalone per-block LightGBM was
S_MAE 0.73–0.75 (programme §§4.5–4.8). A standalone block model is therefore not a credible
successor. The testable hypothesis is that a nonlinear, block-structured learner adds
information to HG's linear components, particularly from the weather columns. The standalone
arms remain, for attribution only.

**The decomposition.** The Owner added the pooled arm L-P to test the block hypothesis itself.
The arms form a ladder, each step adding one thing:

| Step | What it adds |
|---|---|
| B3 → L-P | Weather |
| L-P → L-R | The block split |
| L-R → HGL | The blend into v3 |

B3 is a saved CP-15 reference with fixed CP-2 hyperparameters. The B3 → L-P step therefore
also includes training-only capacity selection and the §15.3 missing-input rule, and is not an
isolated weather effect. The L-P → L-R step is controlled: L-P and L-R differ only in pooled
versus per-block fitting.

**Inherited unchanged:**

- §§2–3: information boundary and evidence class.
- §4: normalization.
- §§14.1–14.4: population, chronology, the H residual recipe, metrics, bootstrap mechanics and
  limits.
- §§15.1–15.3: weather treatment, frozen features and the missing-input rule.
- All six §8 diagnostics, reported as diagnostics; §9's restrictions; §16.

Only the arms, contrasts, adoption rule, ceilings and deliverables below are new. Historical
CP-15/16/20 results, FAILs, debits and limits are preserved. They are re-scored only as saved
references.

Every CP-21 result is `development_post_selection`. Nothing dated after 2026-04-07 is read,
scored, plotted or used for any choice, and the fresh-data test 4.7T stays reserved.

### 17.2 Arms, comparator and the single adoption candidate (Owner decision D1)

| ID | Role | Construction |
|---|---|---|
| HG | Comparator (v3), saved | CP-20's HG exactly: the saved accepted vectors. Its components A1_w (normalized LEAR) and B2_w (raw LEAR), both with weather, are reused only with verified identity. |
| L-P | Study arm, for attribution | One pooled LightGBM for all 24 hours, on the raw target, with exactly HG's information including weather (§17.3), and HG's H layer on its own issued errors. Never adoption-eligible. |
| L-R | Study arm, for attribution | Three-block LightGBM central forecast on the raw target (§17.3), with HG's H layer (§14.2) on its own issued errors |
| L-N | Study arm, for attribution | L-R with §4 target normalization; otherwise identical |
| HGL | Sole adoption candidate | Central `c = (1/3)·A1_w + (1/3)·B2_w + (1/6)·L-N + (1/6)·L-R`, that is `(2/3)·c_HG + (1/3)·mean(L-N, L-R)`. HG's H layer is re-estimated on HGL's own issued errors. |

**The blend.** The fixed weights give each model family one equal vote: normalized LEAR, raw
LEAR and block LightGBM. They also keep HG's raw/normalized pairing inside the new member. The
weights are set before any CP-21 result and are never tuned; learned or per-block weights
belong to programme 4.8.

**What differs from HG.** HGL differs from HG only by the added member. Its A1_w and B2_w are
HG's own genuinely issued components, identical bit for bit.

**The interval layer.** HGL, L-P, L-R and L-N each use HG's layer on their own issued errors:

- the price-only A1 scale `s_t`;
- the 28-complete-released-day buffer and `w_h = n_h/(n_h+56)`;
- the seven quantiles and the §14.2 failure rule.

Residuals are never shared across forecasts.

**Retraining.** The Owner's "retrain" is met in two ways. The new member is trained at every
origin, and the interval layer is re-estimated on the composite's own errors. HG's components
are deterministic, so refitting them reproduces CP-20's forecasts. The design verifies this
through the fully refitted origins of §17.5 and reuses the verified CP-20 components elsewhere.

**Saved references, metric-only:** B0 (normalizer), B1, B2, B3, A1, H0 (v2) and HG. No
reference is refitted, except for an identity-verified regeneration of HG components on a
cache miss. Eleven policies are scored: 7 saved plus 4 new.

**The block-split claim** is reported from L-R − L-P according to its result (§17.5), not
withheld.

**Out of scope, and why:**

- **A per-block residual-correction model on HG's errors.** It would need genuinely held-forward
  HG forecasts across every training window: a nested full-history HG replay, plus weather
  retrieval for 2022-09-29..2023-03-23. In-sample residuals cannot replace those (§3).
- **A normalized pooled arm.** The split is tested on the raw target only.
- **Seed ensembles.**

These exclusions bound attribution. L-R − L-P isolates the block split on the raw target. No
contrast separates the individual weather features.

### 17.3 Block models, information set and training-only capacity selection

**Blocks.** The blocks are fixed and exhaustive, in Europe/Berlin local hours:

- night: 22–05 (8 hours);
- solar: 10–16 (7 hours);
- shoulder/peak: 06–09 and 17–21 (9 hours).

L-R and L-N fit one model per block, and a target hour belongs to exactly one block. L-P fits
one pooled model over all 24 hours, on the same rows. On a 25-hour day, both canonical
local-hour-2 observations enter the night block (and L-P's rows). On a 23-hour day the missing
hour stays absent.

**Information set: exactly HG's, for every LightGBM arm.** The features are:

- the inherited CP-15 B3/A2 LightGBM recipe: `reports/cp15/protocol.json`, 23 features, and
  for L-N its price-valued center/scale lists;
- the three frozen §15.2 weather columns for the target local hour;
- their three missing indicators, under the §15.3 training-only median-imputation rule.

Nothing else enters: no other feature, lag, cross-hour weather expansion or source, and no
feature search. LightGBM's native missing-value routing does not replace the §15.3 rule.

**Fixed settings.** Objective: quantile, α = 0.5 (p50). Seed 42, with deterministic
single-seed fits. The other inherited CP-15 parameters stay unchanged, except capacity.

**Capacity grid.** At most four configurations per model: each block model, and L-P's pooled
model. The largest is the inherited setting, 600 trees and 63 leaves; the others have lower
capacity, with fewer leaves, trees or both. The grid is frozen in the pre-run protocol before
any outer scoring and is identical for L-P, L-R and L-N.

**Selection, at every origin and for every model (each block, and L-P's pooled model):**

1. Fit each configuration on the origin's training window, minus its last 28 calendar delivery
   days.
2. Select the lowest validation MAE in EUR/MWh on those 28 days. L-N is inverted before scoring.
   An exact tie goes to the smaller configuration.
3. Refit the selected configuration on the whole window.

This mirrors LEAR's inherited inner selection and uses training data only.

**History.** `[max(2019-01-01, D−728 calendar days), D)`, subject to each origin's availability
filter, as in §14.1.

**Minimum training rows.** L-P keeps the inherited 8,760-row LightGBM minimum, which is
365 × 24. The block equivalent is 365 × block hours: 2,920 (night), 2,555 (solar) and 3,285
(shoulder/peak).

**Cadence.** Every origin gets fresh daily fits, including selection, as §16's daily retraining
would require of a product. An identical historical fit may be cached only with verified input,
protocol and origin identity. A cache miss counts as a budgeted fit.

### 17.4 Population, chronology and failure rule

**Population: CP-20's frozen population.**

- 10,747 original target keys, with fold counts 2,160 / 2,159 / 2,112 / 2,160 / 2,156, over
  448 represented delivery days.
- The CP-16/CP-20 input manifest's 638 fold/date origins, including 35 training-only admission
  dates.
- The same genuine warm-up starts: 2020-05-25 / 2021-02-23 / 2022-05-25 / 2025-03-22 / 2025-12-02.

Each new arm covers every key: 42,988 new policy-target rows, or 118,217 scored rows with the
seven saved references.

**Chronology.** Forecast origin D−1 11:00 UTC; delivery calendar Europe/Berlin; released errors
are ≤ D−2 and consumed once.

**Weather.** Weather comes only from CP-20's retained decoded grids, through the frozen
conversion, verified against CP-20's fingerprints. No weather is retrieved.

**Failure rule.** §14.2's rule applies to every component, including every LightGBM fit. No
stale, B0, HG or zero-error forecast is substituted, and losing an eligible key prevents a
complete evaluation.

**Admission slice.** §14.2's training-only admission slice checks that each new arm runs
causally before any outer scoring. It is not a selection trial.

### 17.5 Metrics, uncertainty and diagnostics

**Scores,** as in §14.3 and §15.4: emitted-p50 MAE and seven-quantile WIS; S_MAE and S_WIS as
equal-fold ratios to B0; pooled scores as secondary descriptions.

**Bootstrap,** as in §14.4 and §15.4: seed 15042, with one shared 2,000-replicate noncircular
index set of 7-calendar-day blocks per analysis pass. Blocks are drawn within each 90-date fold,
identically across policies.

**Contrasts.** The primary contrast is HGL − HG, the adoption contrast. The secondary contrasts
are descriptive:

| Contrast | What it shows |
|---|---|
| L-R − L-P | The block split: the Owner's hypothesis |
| L-P − B3 | Weather, bundled with capacity selection (§17.1) |
| L-N − L-R | Target representation |
| L-P − HG, L-R − HG, L-N − HG | Each standalone arm against v3 |

The block-split finding is stated from L-R − L-P, with §14.4's endpoint reading:

- **observed joint improvement:** the upper endpoint of ΔS_WIS < 0 and of ΔS_MAE ≤ 0;
- **observed joint worsening:** the lower endpoint of ΔS_WIS > 0 and of ΔS_MAE ≥ 0;
- **otherwise, no demonstrated joint preference,** with both metrics' directions shown.

It is a development finding, not an adoption criterion.

**What is reported for each contrast and score:**

- the paired difference, with its 95% percentile interval;
- for publication, the change as a share of the comparator's score, with the interval of that
  ratio taken from the same replicates. For each replicate b,
  `R_b = S_policy,b / S_comparator,b − 1`. The interval is the 2.5/97.5 percentiles of `R_b`,
  and the point value is the full-sample ratio minus one. Every replicate's paired differences
  and ratios are stored (PUBLISH_RULES 1.1 §3.2).

**Per-fold paired daily-loss intervals** are computed for every contrast. For HGL − HG they
feed §17.6's fourth condition; everywhere else they are descriptive. They are built exactly as
CP-20's per-fold intervals: the paired difference of each fold's mean loss, resampled with the
same 7-calendar-day block index set within that fold.

**Diagnostics, for all arms:**

- per fold, per local hour and per block (night, solar, shoulder/peak), with counts and
  represented dates. Block and hour statements follow §14.3's support rule: at least 56
  represented dates per fold.
- coverage at 50/80/95%, always shown with mean, median and 95th-percentile width, and with
  tail misses;
- central versus emitted MAE and the centering effect; bias; daily level and shape error;
- failures, and the H layer's fallback incidence;
- the stress period, fold 3: 2022-07-01..09-28, 2,112 hours over 88 days. The 17-day peak,
  2022-08-15..31 (408 hours), is reported separately and descriptively.
- all six original §8 diagnostics for every new arm, with the saved B0–B3 comparators.

**Fit cost and daily retraining.** The report covers three things:

- LightGBM fits by arm, model (block or pooled) and origin: training rows, selected capacity,
  inner and final fit wall and CPU seconds, and peak memory. The comparison of block and
  pooled costs is part of the report.
- any HG component regeneration;
- HGL's complete daily cycle, measured cold on the M3 with at most 4 workers, at 20 or more
  origins stratified across the five folds, giving the median and the maximum. The cycle
  covers the features, the A1_w/B2_w refits, the six block selections and fits, the H layer and
  issuance. Those refitted components must match CP-20's bit for bit.

**Owner decision D3:** this is a diagnostic only, not a selection criterion. v21-r5 §16 still
requires any final-product candidate to retrain daily, or to obtain an Owner-approved exception
before live admission. The report is written to `reports/block-challenger/`.

### 17.6 Pre-registered adoption rule (Owner decision D2)

Rule `cp21-adoption` was set on 2026-09-29, the date of the Owner's ratification. HGL becomes
v4 if, and only if, all four conditions hold:

1. **Joint improvement over HG.** On the paired HGL − HG differences, the upper 95% endpoint of
   ΔS_WIS is < 0 and the upper 95% endpoint of ΔS_MAE is ≤ 0.
2. **No regression on the original screen.** HGL meets all six original §8 diagnostics with the
   saved B0–B3 comparators, as HG does.
3. **A complete, valid evaluation.** Engineering PASS with a fresh binding Integration verdict,
   and every one of the 10,747 keys issued with finite, ordered quantiles.
4. **No resolved per-fold degradation.** In no fold may HGL − HG be decisively worse in MAE or
   in WIS. A fold is decisively worse when the 95% interval of its paired daily-loss difference
   (§17.5) lies entirely above zero, that is, when its lower endpoint is > 0. This applies to
   each of the five folds and to both metrics.

**Otherwise,** HGL is not adopted and CP-21 becomes a descriptive branch: "Not adopted", with
the first unmet condition and its values as the reason.

**How the rule is applied.** Mechanically. It is not re-weighted, re-thresholded or overridden
after results. A mixed result is reported as no demonstrated joint preference, never as
equivalence. L-P, L-R and L-N are never eligible for adoption, whatever they score. An
INCOMPLETE or BLOCKED return yields no adoption decision and no result to publish.

**What adoption means.** Adoption is a research status. v1 remains the released product and the
demo. No final-product designation (§16), freeze or Live follows from it. An adopted v4 becomes
the base for later extensions. At CP-21's landing, the Owner updates the standing decision
"same information, same opponent", which names HG, so that later extensions face v4 on v4's
information. Adoption is one more selection on the same five folds, so 4.7T's frozen manifest
must carry both v3 and v4.

**Naming** (plan revision 3 §16, decision 2; PUBLISH_RULES 1.1 §4). The version number is
assigned only at adoption, dated at landing.

- **Adopted:** `v4 · <adopted change>` (proposed: "v4 · three-block LightGBM added"), with
  predecessor v3. The A3 transition title is "From v3 to v4: adding a three-block LightGBM".
- **Not adopted:** the branch "Three-block LightGBM on v3", attached after v3.

### 17.7 Causal and integrity controls

Every negative assertion has a positive control that can fail, and that survives the model's
own transforms. The following are required for all new arms.

- **Inherited controls: §14.8 item 3 and §15.6 item 4.**
  - A delivery-day price mutation changes forecasts by exactly 0.0.
  - An available D−1 mutation moves a controlled forecast.
  - Post-gate and target-actual inputs are refused.
  - D−1 errors are refused; D−2 errors are accepted once released.
  - Each error is consumed once, and no partial day enters the buffer.
  - 23/24/25-hour days keep their identity.
  - Transforms are fitted on training data only, and warm-up is genuine.
  - State persists and replays after a restart; a stale or wrong cache is refused.
  - Quantiles are finite and ordered.
- **Transform-aware positive controls for LightGBM.** Trees are invariant to monotone feature
  rescaling, and normalization cancels a uniform price scaling. Weather influence must
  therefore be shown with a non-monotone perturbation, for example a cross-date permutation of
  weather vectors. The D−1 price control on L-N must use a non-uniform mutation.
- **Training-only selection,** for every LightGBM model, block or pooled. Altering outcomes
  after an origin leaves that origin's selected capacity, fits and forecasts exactly unchanged;
  altering inner-validation rows can change them.
- **Pooled–block parity.** L-P and L-R differ only in pooled versus per-block fitting: the same
  rows, target, features, grid, selection rule and H recipe.
- **Block membership and DST.** Every canonical target hour maps to exactly one block; repeated
  and missing local hours are handled as in §17.3.
- **Boundary guard.** Materializing any input or outcome dated after 2026-04-07 fails, with a
  positive control.
- **Blend and layer parity.**
  - HGL's A1_w and B2_w equal HG's bit for bit.
  - `c_HGL − (2/3)·c_HG = (1/3)·mean(L-N, L-R)`, within floating-point tolerance.
  - HGL, L-P, L-R, L-N and HG call the same H-layer code path.
- **HG identity.**
  - Cached components match their CP-20 fingerprints.
  - Independent representative HG reproduction matches the accepted CP-20 vectors.
- **Byte-exact storage** of every hash-bound file.

### 17.8 Ceilings and calendar (Owner decision D4)

**Nature of the caps.** These are Owner-approved maxima, not estimates or targets. They were
approved as recommended on 2026-09-29, then recomputed for the added arm L-P.

- **What counts:** warm-up, admission, inner selection, controls, failures, repairs and
  independent review.
- **At a cap:** stop before the first cap is exhausted and retain the partial evidence. No
  outcome-driven retry, new arm, grid change or automatic increase follows.
- **Debits:** previous debits stay historical. Nothing transfers from CP-16 or CP-20.

| Dimension | Maximum |
|---|---|
| Policies | 4 new (L-P, L-R, L-N, HGL) and 7 saved references: 11 scored. 1 adoption candidate. 0 other arms: no normalized pooled arm, residual-correction model or blend-weight trial. |
| Blend and interval layer | 1 fixed blend (§17.2) and 1 inherited H recipe. 0 alternative weights, residual configurations or outer-score selections. |
| Capacity grid and seeds | At most 4 configurations per model, the same for L-P, L-R and L-N. Fitting seed 42; bootstrap seed 15042. 0 seed ensembles or seed searches. |
| LightGBM fits | At most 24,000 main fit attempts. Nominal all-fresh: 638 origins × (2 block arms × 3 blocks + 1 pooled model) × 5 fits = 22,330. At most 35,000 in total, including controls, reproduction, failures and repairs. |
| HG components | Reuse the verified CP-20 components. With the fully refitted origins of §17.5 or a cache miss: at most 1,600 component-day attempts (nominal 1,276) and 192,000 primitive Lasso attempts. |
| Replay | At most 10,500 new policy-days: about 4 full-equivalent passes of 4 × 638 = 2,552, counted under §14.5's rule. |
| References and uncertainty | At most 3 metric-only reference passes. At most 3 bootstrap analysis passes, including independent review, with 2,000 replicates each. |
| Compute | At most 60 aggregate machine-hours, summed across concurrent jobs and including tests, failures and review. At most 4 concurrent worker threads in total (LightGBM threads × processes ≤ 4); BLAS 1; 0 GPU or cloud. |
| Memory and disk | 10 GiB aggregate RSS. 20 GiB added peak disk, including worktrees, caches, the local MLflow store and outputs. |
| Data, network and cost | 0 bytes of new data or model download. 0 weather retrieval. 0 remote writes (MLflow, Hub, Git remote). $0. |
| Effort | Approximate timebox of 32 active hours. Hard ceiling of 40 active hours, including verification and the return. |

**Basis for the recomputation.** CP-15's pooled daily B3 fits took about 3 seconds each, and a
block model trains on about a third of those rows. Worst case, with single-thread parallel
workers, the 22,330 main fits need about 28 aggregate machine-hours. Controls, reproduction,
review, scoring and tests add about 12. The 60-hour cap leaves a 1.5× margin.

**Calendar: no scheduled work on Friday or Shabbat,** Asia/Jerusalem, from Friday 00:00 to
Sunday 00:00.

- No compute job starts in that window or runs unattended into it. A job that cannot finish
  before Friday 00:00 is not started. A running job is stopped at an atomic checkpoint and
  resumed after Shabbat, on the Owner's message.
- No long unattended run is required or authorized.
- The pause is not a terminal return and is excluded from elapsed hours.
- No Owner action is requested for those days.

**Before dependent work,** the Lead completes §14.6 E1–E4 for CP-21:

- actual origin and fit enumeration;
- the grid, fixtures and cache identities;
- feasibility against every cap and the independent-review allowance.

An insufficient allowance returns a concrete blocker, not a smaller experiment.

### 17.9 Publication packet and MLflow (Owner decision D5)

From CP-21 on, the checkpoint supplies its publication packet (PUBLISH_RULES 1.1 §11;
Publication Standard v1 §12). The landing templates do not carry it yet; that incorporation is
decision D6 of 2026-09-28, a separate governance task. Until then, this section and the brief
carry the step explicitly.

- **Pinned rules:** PUBLISH_RULES 1.1, SHA-256
  `91eea445434718a163f03bcfd82e1db275a9d98311e76eb6cd1365f3707584f3`. It incorporates
  Publication Standard v1 (`01d721c2ba6316ca9a2f707e79da229bef732e91bad22f6ce457fb01e69478cc`) and
  presentation plan revision 3 (`281193740a256a99a1676d53ef61c9babb5f744a7d0fb038927e305d1149812c`).
- **The packet:** `docs/track-b/evidence/cp-21/publication-packet.md`, filling every section of
  `docs/track-b/publication-packet-template.md`:
  - identity;
  - draft registry entries: HGL as a `v4 · …` generation or as the branch, per §17.6; L-P, L-R
    and L-N as study arms; comparator HG; population `common-10747h`;
  - the claim map `docs/track-b/research-content/cp21-claims.md`, with its withheld claims.
    It includes the block-split finding stated from L-R − L-P (§17.5) and the
    B3 → L-P → L-R → HGL ladder, with the bundling in the B3 → L-P step disclosed;
  - the derived headline quantities: the verdict, the rule and its date, the distance from HG,
    N, §17.5's ratio intervals with seed, replicates and block length, and per-fold MAE with
    fold 3 as the stress period;
  - draft slot texts for the outcome the rule yields: the v4 chapter plus the A3 transition, or
    the branch card;
  - §5b and §5d marked not applicable, with the reason: the released product and the
    final-product designation do not change;
  - §8's intended identities for GitHub/README, Pages, MLflow, the Space card and the direct
    demo.
- **The MLflow step:**
  - The experiment is `delu-generations`.
  - Runs are tracked locally only, in `.local/mlruns/cp21`: one parent, `cp21`, and one child
    per new policy (`cp21/HGL`, `cp21/L-P`, `cp21/L-R`, `cp21/L-N`). Their names and tags follow
    the draft entries.
  - A draft export, `reports/block-challenger/mlflow-export-draft/cp21.json`, is built through
    `scripts/mlflow_export.py`'s code path from committed CP-21 evidence and the packet's draft
    entries.
    - **Why a draft.** It stays outside the published set because registry statuses are dated
      at landing, and registering a generation or branch requires its chapter or card.
    - **Pending fields.** Identities that exist only at landing are explicit pending fields:
      the adoption date and source, the evidence-tag commit and the landing record.
  - The published export set is unchanged: `reports/presentation/mlflow-export/`, including its
    `manifest.json`. `mlflow_export.py --check` still passes on it.
  - The publication block registers the entries and regenerates the final export. That export
    must equal the draft apart from the pending fields, and it must change no previously
    published record.
  - There is no public write, no upload and no network call to DagsHub.
- **Public surfaces are unchanged in CP-21.** CP-21 does not regenerate or modify any of the
  following; they belong to the separate publication block after landing:
  - the page;
  - the README's generated blocks;
  - the Space cards and bundles;
  - the public registry's rendered entries;
  - the existing exports.

  CI and `make verify` stay green at the final candidate.
- **Acceptance:** the Integration Critic reviews the packet and the export as artifacts.
  - Every number re-derives from committed rows.
  - Names and statuses follow the draft entries and §17.6's mechanical verdict.
  - The diff touches nothing already published.

Publication itself follows the Owner's LAND in either outcome, as a separate block under
PUBLISH_RULES 1.1: the registry, the chapter or branch card, the page, the README, the MLflow
upload, the Space and the postdeploy checks. See
[the publication plan](docs/track-b/cp-21-publication-plan-2026-09-29.md).

**Owner decision D6:** if v4 is adopted, its chart encoding is amber `#B45309`, a filled
diamond marker and the direct label "v4" (PRES-1 W16(b)).

### 17.10 Complete CP-21 acceptance checklist

All thirteen items are mandatory. Engineering PASS does not require adoption: a complete,
valid "Not adopted" result can pass.

1. Verify the repository and input state, and preserve prior evidence and other sessions'
   work.
   - The ratified anchor and the amendment record are on `main` at the ratification commit;
     verify their SHA-256 against the brief.
   - On `gauntlet/cp-21`, package the issued brief byte for byte as
     `docs/track-b/evidence/cp-21/issued-brief.md`, from its canonical copy
     `.local/artifacts/cp-21/issued-brief.md`, and record its SHA-256.
   - Before any outer scoring, commit the frozen pre-run protocol:
     - the arms, blend weights, block map, feature list and missing rule;
     - the capacity grid, inner split and tie rule;
     - fixtures, seeds, the key/origin manifest and cache identities;
     - budget accounting and the §17.6 rule text.
2. Verify the CP-20 population and manifest identities, and the frozen weather features from
   the retained grids. Reuse HG components only with verified identity, and obtain an
   independent representative HG reproduction that matches the accepted CP-20 vectors. No
   retrieval, and no data after 2026-04-07.
3. Implement exactly L-P, L-R, L-N and HGL, with training-only capacity selection for every
   LightGBM model. Prove three things:
   - HGL differs from HG only by the added member and uses HG's H recipe on its own errors;
   - L-R and L-N differ only in target representation;
   - L-P and L-R differ only in pooled versus per-block fitting.
4. Prove every §17.7 control, pairing each negative assertion with a positive control that
   survives the model's transforms. Rerun the applicable inherited regression and namespace
   guards without a live mutation.
5. Produce all 10,747 keys for each new arm, with finite, ordered quantiles and the emitted p50
   kept separate from the central forecast. Account for failures, exclusions and fallback
   incidence without changing denominators.
6. Score all eleven policies. Independently verify:
   - the emitted-vector scores and the equal-fold normalization;
   - every per-fold, hour, block, stress and peak diagnostic, with its denominators and support
     labels;
   - coverage together with width;
   - all six §8 diagnostics for each new arm.
7. Apply §17.6's four conditions mechanically.
   - Report the primary and secondary contrasts with paired intervals, per-fold intervals, and
     the ratio intervals from the checkpoint's own stored draws.
   - State the block-split finding from L-R − L-P, with §17.5's reading.
   - State the verdict, v4 or not adopted, with the first unmet condition; state mixed and
     negative findings.
   - Keep the Engineering status, the research finding and the product status (v1 released)
     distinct. No promotion, freeze or economic claim.
8. Deliver §17.5's fit-cost and daily-retrain diagnostic in `reports/block-challenger/`.
9. Enforce and report every §17.8 cap from the first job, including controls, failures and
   independent review, and respect the Friday/Shabbat calendar. At an exhausted cap, retain the
   partial evidence and return the applicable non-PASS status.
10. Supply the durable evidence and executable reproduction commands: the protocol, lineage,
    predictions, metrics, diagnostics, uncertainty with stored replicates, criteria, failures,
    resources and the fit-cost report. Store hash-bound files byte for byte, and disclose
    defects, repairs and invalidated outputs.
11. Deliver §17.9's publication packet and draft MLflow export, with public surfaces and the
    published export set unchanged, CI green and no public write.
12. Obtain one fresh, independent Integration-Critic PASS on a clean detached checkout of the
    exact final candidate. The review covers this entire checklist and:
    - independently recomputes the saved-vector metrics, the paired, per-fold and ratio
      intervals and the §17.6 verdict;
    - representatively reproduces HG, a block and a pooled LightGBM selection and fit, and the
      causal and state controls;
    - re-derives the packet and the export.
13. Return the canonical packet (templates §3), together with the publication packet:
    - both terminal SHAs and a verdict-only delta;
    - reachable evidence;
    - all resource totals and elapsed hours;
    - branch and worktree accounting.

    Stop at CP-21's local result.

### 17.11 Paths and entry authority

**Write paths:**

- `src/cp21/`, `tests/cp21/`, `scripts/cp21_blocks.py`;
- `reports/block-challenger/`, `docs/track-b/evidence/cp-21/`;
- `docs/track-b/research-content/cp21-claims.md`;
- `scripts/mlflow_export.py` and its tests, only as needed for the draft export, without
  changing the published export set or any published record;
- `pyproject.toml` and `uv.lock`, only if a necessary pinned dependency is missing. None is
  expected: LightGBM is already pinned.

**Ignored material:** `.local/{worktrees,artifacts,tmp}/cp-21/` and `.local/mlruns/cp21`.

**Read-only:** CP-15/16/20 code and reports; `.local/artifacts/cp-20/` (the weather grids and
the HG component cache); `reports/weather-admission/`.

**Preserve:** v1; the CP-15/16/20 evidence; the public surfaces; Q&A; `progress.md`; every
locked document.

**Roles.** The accountable executor is the CP-21 Engineering Lead. The reviewer is its fresh,
independent Integration Critic under `engineering-role.md`.

**Ratification and CP-21 execution authority: GRANTED by the Owner, 2026-09-29.** The grant
covers:

- CP-21 execution under this section and the issued brief;
- local `gauntlet/cp-21` candidate and evidence commits;
- exact immutable packaging of the issued brief (item 1). The ratified anchor and the
  v21-r5 → v21-r6 amendment record are already on `main`.

**Not authorized:** mainline operations, pushes, tags, publication, remote writes (MLflow,
Hub), data retrieval, governance edits and later checkpoints. The Lead owns E1–E4 and the
pre-run feasibility check, and escalates only a concrete blocker beyond this scope.


## 18. Distribution challenger — DDNN only, written in NumPy (v21-r7)

**Owner amendment, 2026-09-30.** This section governs programme work item 4.6 and every later
use of DDNN in this programme. It is not a checkpoint bar and grants no execution authority. A
future 4.6 brief supplies the bar, budgets and protocol, under the programme handoff, §16 and
the standing decisions in force when it is written.

### 18.1 TabPFN is withdrawn

TabPFN leaves the programme, in every version. It is not a research candidate, a comparator, a
recombination member or a final-product candidate. No TabPFN licence entry, resource entry,
comparison, context construction or weight download will run.

- Programme item 4.6 becomes a single-candidate DDNN route: 4.6L, then 4.6R, then 4.6C.
- The planned TabPFN–DDNN comparison is **withdrawn by Owner decision**, before any run. It is
  not reported as failed, blocked or "not completed", and no TabPFN-versus-DDNN claim is made.
- §16.2's general rule stands: refreshing inputs, residual state or context is not weight
  training. Its TabPFN example no longer names a candidate.
- Bringing TabPFN back needs a new Owner amendment.

**Context, recorded with the decision.** The Owner decided this while weighing an option to
retrain the final product in the browser, so that anyone who wants to check it can. TabPFN is a
pretrained transformer. Its daily update would be context replacement, which §16.2 does not
count as training. It has no runtime under Pyodide, where the current demo executes, and its
licence entry (handoff 4.6L) was unresolved.

### 18.2 DDNN is written from the start in NumPy only

1. **One implementation.** DDNN's model code is written from scratch in this repository and
   depends on NumPy and the Python standard library alone. That covers the network, the
   Johnson SU distributional head and its likelihood, the gradients, the optimizer,
   regularization, the training loop, early stopping, seeding, ensembling and the emission of
   quantiles and p50. No deep-learning framework (PyTorch, TensorFlow or Keras, JAX or the
   like), no other numerical library, no third-party DDNN code and no pretrained weights enter
   it.
2. **Every DDNN number comes from it.** The same code produces every DDNN research result, every
   daily fit and every forecast that any surface shows. No second implementation is written for
   another runtime, and no other implementation's output stands in for its output.
3. **Inputs.** The model code takes its design matrix from the common admitted feature pipeline,
   under the same information, history and causal rules as every other candidate. That pipeline
   is outside this rule.
4. **Purpose and limit.** One code path runs from research to any later server or browser run,
   so the model a visitor might retrain is the model that was evaluated. This section does not
   decide in-browser retraining: whether a daily fit runs in the browser, and what equality with
   the issued artifact it claims, is decided under §16 in the final-product briefs. Training is
   sensitive to floating-point order, so equality between runtimes is measured, never assumed. A
   claim states its measured tolerance, and bitwise identity is claimed only where it was
   measured.

### 18.3 PyTorch is a host-side correctness reference only

PyTorch may be used only on the development machine, inside tests, as an independent reference
that checks the NumPy implementation:

- the forward pass, the Johnson SU log-likelihood and its gradients, and short optimizer
  trajectories on fixed inputs and seeds, at tolerances the 4.6 brief fixes before any
  comparison run;
- alongside finite-difference gradient checks of the NumPy code itself.

PyTorch never trains a model whose output is scored, published or issued, and it never emits a
forecast, quantile, metric or artifact that enters evidence. It is not a runtime dependency of
research, server or browser code; it enters the environment only as a test dependency. The 4.6
brief fixes how those tests are installed and run, so that they cannot be skipped silently. A
failed check blocks DDNN's results until the NumPy code is fixed. A tolerance changes only
through a recorded protocol change, never silently after a failure.

### 18.4 Consequences for the 4.6 route

- **4.6L** becomes a provenance and licence record. The DDNN code is original, under the
  repository's MIT licence, with its method sources cited and no third-party code or weights.
  The record states the licence of each test-only dependency, and its use table still gives
  every use of DDNN's outputs a disposition. Those outputs remain derived from the CC BY 4.0
  data (`DATA-LICENSE.md`).
- **4.6R** gains one entry condition: the §18.3 checks pass before DDNN's resource measurements
  count.
- **4.6C** becomes one predefined comparison between DDNN and the references its brief fixes,
  under the standing information and comparator decisions then in force. If DDNN fails entry,
  no comparison runs, and the failure is reported to 4.7.
- **§16 applies unchanged** if DDNN is ever designated final: daily retraining, not input or
  state refresh alone, or an explicit Owner-approved exception before live admission.
- **Nothing is opened.** DDNN work needs its own brief, D4 allowances and budgets.

### 18.5 What stays as it was

- §§1–17, and every closed checkpoint's evidence, including CP-21's binding of the v21-r6
  bytes.
- PUBLISH_RULES 1.1, unedited. Its sentence "No such exception is granted here to TabPFN,
  immutable v1 or any other model" remains accurate.
- Historical records that name TabPFN: reviews, briefs, claim ledgers, research content and the
  presentation plan. They describe what was planned when they were written.
- The public report. Its planned item "4.6 · DDNN / TabPFN" is corrected by the next authorized
  publication block, not by this amendment.


## 19. Final-product Space — what it computes and claims (v21-r8)

**Owner amendment, 2026-09-30.** This section governs what the final product's Hugging Face
Space computes, what it may claim, and the in-browser retraining requirement. It binds the CP-17
and CP-18 briefs at the final-product rollout of §16. It is not a checkpoint bar and executes
nothing now. Presentation and acceptance are PUBLISH_RULES 1.2 §7.3 (A9). The implementation
plan is `docs/track-b/final-product-space-plan-2026-09-30.md`.

### 19.1 Scope

The Space is the product's interactive tool, under §16.1's single identity for final version,
product, primary demo and daily policy. It serves only the designated final product; v1's frozen
demo remains a labelled history route. The Space computes only from the records the daily
pipeline publishes to it (§19.4). At runtime it fetches nothing from data sources, registries or
tracking services.

### 19.2 One code path

The code that performs the daily fit, issuance and scoring is the code the Space runs in the
browser for §19.3 and §19.5. No second implementation stands in for the product. A component
that cannot run in the browser runtime is reported at CP-17 under §19.3's exception route; it is
never replaced silently.

### 19.3 "Train it yourself" is required

The Owner requires an in-browser retraining action for the final product.

1. **What it does.** In the visitor's browser, it retrains the daily fit of one issued delivery
   day from that fit's shipped training window, with the same code, seed and selection rules.
   It then predicts that day's quantiles.
2. **What it reports.**
   - whether every data-driven selection matched the issued artifact;
   - the largest absolute difference per emitted quantile, in EUR/MWh;
   - one status that states only what was measured: identical bit for bit, within the frozen
     tolerance τ_eq, or different.
3. **What it never does.** It never replaces, rescores or relabels an issued forecast.
4. **The probe.** Before the CP-17 freeze, a feasibility probe on development data measures, for
   the designated policy:
   - browser time and memory;
   - payload sizes;
   - the deviation from the native fit;
   - selection agreement.

   CP-17 freezes τ_eq and the reference runtime from that measurement.
5. **If the policy cannot meet this requirement** within the measured limits, CP-17 returns a
   blocker. Only an explicit Owner exception, with its public wording, lets the product ship
   without the action. The requirement is never dropped silently, and never met by retraining a
   different implementation.

### 19.4 Daily delivery

Each delivery day, the authorized pipeline publishes a dated bundle to the Space: the issued
forecasts, the issuing artifact and its lineage, the reconciled outcomes and the evaluation
records. The bundle's manifest lists every served file with its SHA-256. The Space shows the
served identity and its freshness. A forecast recomputed by a newer fit is never shown or scored
as issued. Delivery needs the separate operational and publication authority of §16.2 and
programme 4.9; this section grants none.

### 19.5 Definitions frozen at CP-17, before the fresh-data test

CP-17's freeze fixes the following before 4.7T:

- **The percentage measure beside MAE:** its formula; the tolerance, which the Owner sets; the
  denominator; eligible and partial-day hours; and zero, negative and missing prices.
  - The proposed form is the share of scored hours within ±τ EUR/MWh.
  - A figure relative to a benchmark is improvement, not correctness.
- **Coverage and width** per nominal band, and the rolling window over scored delivery days.
- **The reliability diagram:** for each emitted quantile level, the observed share of outcomes
  at or below it, with counts.
- **The quantile-band PIT:** the share of outcomes between adjacent emitted quantiles, against
  each band's nominal share.
- **The recomputation check.** The Space recomputes its evaluation metrics from the shipped
  issued forecasts and outcomes, and compares them with the committed records.
  - Counts match exactly; real values match within a frozen tolerance.
  - A mismatch is shown, and blocks that day's publication as a product failure.

Nothing in this list is chosen after seeing evaluation outcomes.

### 19.6 Evaluation windows

Three windows stay separate and are never pooled:

- development, static, from evidence;
- the one-shot fresh-data test (4.7T);
- the prospective record from the run start, "in progress" until CP-19.

v1's holdout stays v1 history.

### 19.7 Attribution and importance

Methods are fixed by component class:

- **a blend:** each component's weight times its forecast, an exact decomposition;
- **linear components:** coefficient times the centered, standardized input;
- **tree components:** per-prediction contributions (TreeSHAP), and gain read from the fitted
  model;
- **a neural component:** a method frozen at CP-17.

All are presented as attribution within one fitted artifact, never as causality or incremental
value.

### 19.8 Data displays

Data and feature views compute from the shipped series. Before the final test, no research
display uses data after 2026-04-07 (standing decision of 2026-09-24). From CP-18, the views run
through the latest published day, labelled with its last date.

### 19.9 What this section does not do

It designates no model, runs no fit, schedules nothing, and grants no publication, credential or
`AGENTS.md` authority. Unattended daily publication needs the Owner's explicit authority before
CP-18's launch. CP-17 and CP-18 still need their complete bars and briefs.
