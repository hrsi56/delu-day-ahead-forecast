# Verdict — CP-15 — Integration — PASS

- Candidate SHA: `fc4aee038cf898998a292506df62ddb0dcfaf22a`
- Plan / version / bar: `capstone_v21.md`, **v21-r1**, complete §12 supported by §§1–8, 11 and 13.
- Plan SHA256: `44ea4e545d2caa276a36a7a70db6ea044b3975196ead06f3ce59f976c83354b3`.
- Worktree: `/Users/djourno/Downloads/PJM-cp15-r1-critic`, fresh detached candidate checkout supplied by the Lead.
- Worktree clean before and after: **yes**; `git status --porcelain=v1` empty and HEAD equal to the candidate at both boundaries. Final `git diff --quiet` and `git diff --cached --quiet` also exited 0.
- Isolation: procedural read-only review; no read-only mount or enforced sandbox is claimed. No candidate file, index, branch or ref was modified by this Critic. Ignored environments/caches and external `/tmp` reproduction files are the only review byproducts. The Lead owns worktree removal and the later evidence commit.
- **Integration: PASS. product_feasibility: NOT_DEMONSTRATED. Best observed policy: A1. Qualified policy: none.** This certifies the completed development experiment; it does not establish adequate product quality or authorize promotion, publication, or another checkpoint.

## Verbatim bar excerpt

> 1. Verify and report the starting state; preserve other sessions' work, v1/CP-10 evidence and
>    restricted partitions; commit the exact v21 anchor and pre-run protocol before comparison.
> 2. Implement every B0–B3/A1–A5 policy in §5 and the common uncertainty construction in §6;
>    prove genuine rolling fits, warm-up provenance and causal per-origin normalization with fixtures.
> 3. Prove §2 availability, D-2 feedback, single consumption, DST and schema refusal controls;
>    each negative assertion has a positive control, including inherited live-namespace guards.
> 4. Produce predictions on identical original eligible hours and all metrics/diagnostics in §7
>    for every arm; independently check counts, zero crossings, scores and exact window denominators.
> 5. Apply §7 ranking and every §8 criterion mechanically; report both Integration status and
>    product_feasibility, best observed policy, qualified policy or none, and all failed criteria.
> 6. Deliver the pinned Chronos-2 feasibility probe and structural-input feasibility sheet in §5;
>    document genuine access/resource limitations without inventing benchmark results or silently
>    promoting probes into the candidate set. Such probe limitations do not block the core comparison.
> 7. Provide pinned reproduction commands, dependency/input/protocol hashes, seeds, chronological
>    validation records, resource measurements and dependence-aware uncertainty; rerun relevant
>    controls and the existing regression suite, reporting any blockers without a false PASS.
> 8. One fresh independent Integration Critic reviews a clean detached checkout of the exact
>    final_candidate_sha, verifies every checklist item, independently recomputes saved-prediction
>    metrics and performs causal control/representative fit reproduction; commit its verdict only
>    after review. Record commands actually run, exit codes and limitations. No binding PASS means
>    no terminal PASS. Candidate-to-evidence-tip changes are confined to this checkpoint's evidence.

The excerpt was confirmed against the actual candidate file. The excerpt is the citation; section numbering is a convenience.

## Commands actually run

All commands below ran from the detached checkout unless an external artifact path is shown. Exit codes are observed completion codes, not expected values. Output redirections kept full logs outside the checkout.

| Command | Exit | Observed result |
|---|---:|---|
| `pwd && git status --porcelain=v1 && git rev-parse HEAD` | 0 | Correct detached worktree; empty status; exact candidate SHA. |
| `uv sync --frozen --offline --python 3.13.15` | 0 | Created ignored `.venv`; installed frozen core environment and local package, 117 packages. |
| `OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=4 uv run --frozen python scripts/cp15_forecasting.py --inspect > /tmp/cp15-critic-inspect.log 2>&1` | 0 | Original eligible counts 2160/2159/2112/2160/2156. Warm-up starts 2020-06-02, 2021-03-01, 2022-06-02, 2025-03-30, 2025-12-10. |
| `CP15_REQUIRE_SAVED_EVIDENCE=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=4 uv run --frozen pytest -q > /tmp/cp15-critic-tests.log 2>&1` | 0 | **339 passed, zero skips, 158.16 seconds.** Includes the complete independent saved-evidence checker, mutation controls, CP-15 tests and inherited regression suite/live namespace guards. |
| `OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=4 uv run --frozen python -m cp15.reproduce_fit --fold fold_1 --day 2020-07-01 --causal-controls --output /tmp/cp15-critic-fit-2020-07-01.json > /tmp/cp15-critic-fit1.log 2>&1` | 0 | 24 hours for each of eight new central policies; all differences exactly zero; all 74 model records match the saved history, training, target, normalization and model identities. 103.832 seconds. Future-mask difference exactly zero; all five fitted policies move under D-1 positive control. |
| `OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=4 uv run --frozen python -m cp15.reproduce_fit --fold fold_3 --day 2022-08-15 --output /tmp/cp15-critic-fit-2022-08-15.json > /tmp/cp15-critic-fit3.log 2>&1` | 0 | Crisis origin: all eight 24-hour central vectors exactly match; all 74 model records/identity fields match; 42.823 seconds. |
| `uv venv --python 3.12.14 data/cp15-probe-env` | 0 | Created ignored isolated probe environment. |
| `uv pip install --offline --python data/cp15-probe-env/bin/python -r reports/cp15/feasibility/requirements.freeze.txt > /tmp/cp15-critic-probe-install.log 2>&1` | 0 | Installed pinned probe closure offline. |
| `uv run --frozen python -m cp15.reproduce_probe --python data/cp15-probe-env/bin/python --scratch /tmp/cp15-critic-fresh-probe > /tmp/cp15-critic-probe.log 2>&1` | 0 | Fresh external probe completed unscored; context, future-load, input-manifest and forecast-CSV SHA256 all match. 56.432 seconds, sampled peak process-tree RSS 885,112,832 bytes. |
| `uv run --frozen python /tmp/cp15-critic-arithmetic.py > /tmp/cp15-critic-arithmetic.log 2>&1` | 0 | Separate Critic-authored audit importing neither CP-15 scoring/model code nor its test helpers. Recomputed per-fold/peak/pooled point, interval, centering, bias, level and shape metrics from predictions; independently applied six criteria/ranking; checked original preregistration bytes, protected input/payload hashes and historical copies against original Git objects. Largest absolute summary difference 5.684341886080802e-14. |
| `uv run --frozen python /tmp/cp15-critic-provenance.py > /tmp/cp15-critic-provenance.log 2>&1` | 0 | Separate Critic-authored audit verified all **116** manifest digests and **45** resource rows against underlying fit/origin/run/timing records; preserved-path diff empty. |
| `git diff --name-only 193d9cf48c586b9c4b1f43d7a5677b2d5f400832..HEAD` | 0 | Changes confined to CP-15 source/tests/reports/evidence, authorized exact replacement anchor/brief, and package inclusion in `pyproject.toml`; preserved v1/CP-10 data/model/public paths unchanged. |
| `git show --format=fuller --stat bb5e67882fcfdf65b963d25ce785a3999816dfc2` | 0 | Exact v21-r1 anchor/protocol and historical preservation committed before completed comparison. The audit also compares those Git blobs byte-for-byte with the candidate. |
| `git merge-base --is-ancestor fc4aee038cf898998a292506df62ddb0dcfaf22a gauntlet/cp-15` | 0 | Candidate reachable from checkpoint branch at review completion. |
| `git diff --quiet && git diff --cached --quiet && git status --porcelain=v1 && git rev-parse HEAD` | 0 | No tracked/index delta, empty status, unchanged exact candidate. |

Read-only `cat`, `sed`, `rg`, `wc -l`, and `git log --format='%H %s' -8` inspections opened the concrete evidence listed below; all inspection shell invocations returned 0. One initial file inventory used `rg --files cp15 reports/cp15 tests`: `cp15` is not a root directory, so that operand printed “No such file or directory”; the source inventory was immediately corrected to `rg --files src/cp15`. This was an inventory typo, not a missing required artifact. No reproduction or validation failed. External audit scripts and this verdict were written by shell here-docs/Python; those writes exited 0 and did not touch the candidate.

## Evidence actually inspected

- Governance/bar: `AGENTS.md`, `engineering-role.md`, `docs/track-b/gauntlet-templates.md` §2 and the exact `capstone_v21.md` controlling checklist/supporting sections. No `progress.md`, Orchestrator role, syllabus, Track A/C or Q&A content was opened.
- Protocol/state/preservation: `reports/cp15/protocol.json`, `resumption-state.json`, `attempt-1-preservation.json`, Git preregistration `bb5e67882fcfdf65b963d25ce785a3999816dfc2`, original tip `193d9cf48c586b9c4b1f43d7a5677b2d5f400832`, and its mapped original byte blobs. This checks retained historical identity without treating the earlier verdict as this review's authority.
- Implementation: `src/cp15/data.py`, `models.py`, `residuals.py`, `scoring.py`, `reporting.py`, `reproduce_fit.py`, `reproduce_probe.py`, `feasibility_probe.py`, and `scripts/cp15_forecasting.py`. Inspected inherited `features.py`, the `LGBM_PARAMS` definition in `model.py`, and live-namespace tests. The inherited CP-2 LightGBM objective/parameters match the registered B3/A2 parameters; date-based crisis fields are excluded from fitted input matrices.
- Fixtures/checker: all six `tests/cp15/test_*.py` files, especially the complete 1,007-line saved-output checker. Its metric/selection/normalization/feedback/fit/bootstrap calculations do not import CP-15 model or scorer routines. Positive and deliberately broken controls cover arithmetic, common-row deletion, changed truth, order/finite/schema checks, zero denominators, all decision criteria, historical normalization, DST 23/24/25-hour completeness, D-2 timing, duplicate consumption, late truth, backward release, chronological fit records, and live-key detection.
- Saved numerical artifacts actually read through the audits/tests: combined predictions; all five folds' predictions, issued forecasts, fits, feedback, origin and run files; original development prediction vectors; admissible snapshot projection; `per_fold.csv`, `pooled.csv`, `peak.csv`, `daily.csv`, `recovery.csv`, `relative_scores.csv`, `ranking.csv`, `criteria.csv`, `selection.json`, `bootstrap.csv`, `resources.csv`; complete artifact/input digest inventories and execution timing logs. Original rows were rebuilt through the inherited eligibility construction after filtering admissible partitions.
- Narrative and resource records: `report.md`, `reproduction.md`, `implementation-notes.md`, `validation.json`; resource table and lineage production code. Fixed-tolerance Lasso continuation is explicitly documented; unsuccessful numerical fits are not silently accepted as forecasts.
- Feasibility: `feasibility/README.md`, `structural_inputs.md`, `source_retrieval_manifest.json`, `model_verification.json`, `input_manifest.json`, exact requirements freeze, saved/fresh `probe_result.json`, fresh resources/comparison and input/output CSV digests. Sheet covers fuel/EUA, load, renewables, capacity/outages, cross-border/weather timing, vintages, access, redistribution and unmeasured missingness; uncertainties remain explicit.

## Independently observed numerical results

- All nine policies have **10,747** original eligible hours; **96,723** prediction rows, **45** policy/fold summaries. Full fold 3 is **2,112 hours / 88 represented days** within the unchanged 90-calendar-day window. Peak is exactly **408 hours / 17 days**, 2022-08-15–31, for every arm. No missing required forecast, duplicate target, nonfinite emitted quantile, or crossing was found.
- Exact B1 final vectors and raw central values match original development replay. B0 calendar-lag values and A3/A5 arithmetic match independently for every saved issued hour, including warm-up.
- Saved-error replay reconstructs every evaluation interval from immutable issued centers/scales, latest 28 complete released dates and exact linear empirical quantiles. Training, inner-validation and origin-normalization hashes are independently checked for every recorded fit.
- The full saved checker recomputes all daily, pooled, peak and recovery metrics and all **240** bootstrap contrasts using 7-consecutive-calendar-day paired blocks, 2,000 replicates and seed 15042. Empty inherited days remain calendar gaps and never become zero loss. Numeric tolerance is `atol=rtol=2e-12`.

| Policy | S_MAE | S_WIS | Peak 95% hits / 408 |
|---|---:|---:|---:|
| B0 | 1.0000000000 | 1.0000000000 | 384 |
| B1 | 1.0518451348 | 0.9856366964 | 79 |
| B2 | 0.6578109124 | 0.6389910407 | 364 |
| B3 | 0.7841363978 | 0.7399052225 | 363 |
| A1 | 0.6722908121 | 0.6460150916 | 378 |
| A2 | 0.7737135304 | 0.7316680120 | 387 |
| A3 | 0.6725142581 | 0.6471900504 | 381 |
| A4 | 0.7646642404 | 0.7334186815 | 370 |
| A5 | 0.6737799644 | 0.6487132071 | 379 |

Ranking is **A1, A3, A5, A4, A2**. A1/A3/A4/A5 fail criteria **1, 2, 5**; A2 fails **1, 2, 4, 5**. Each candidate passes criterion 3 (per-fold 95% coverage) and criterion 6 (complete finite ordered forecasts). Each actual threshold/subcheck in `criteria.csv` is independently checked by the saved-evidence test, including metric-specific peak and B2/B3 comparators. No qualifying policy exists. A1's pooled MAE is better than B2's, but its equal-fold S_MAE does not clear the registered 10% improvement requirement; the declared decision correctly follows the registered weighting.

Production origin reproduction uses the unchanged full statistical protocol, not the smaller synthetic test settings. Its tolerance is `atol=1e-8, rtol=1e-10`, with exact training/target/normalization/model fingerprints required separately. Both sampled origins actually matched **exactly**. On 2020-07-01 the D-and-future price mask plus post-D load mutation changed no forecast/model fingerprint. Adding 500 EUR/MWh only to available D-1 prices moved B2/B3/A1/A2/A4 by maximum absolute differences **485.1702166472 / 39.3735269351 / 425.3605796114 / 190.4457432547 / 287.7812685710**.

The pinned Chronos-2 revision is `29ec3766d36d6f73f0696f85560a422f50e8498c`; model weight SHA256 is `ddcda3c7508bf2528087723e98a20707cc04b7f370ae275a9fd88078ddba4f42`. Its fresh offline reproduction made two CPU calls at the permitted proper-training origin, and changing only future load by 20% moved outputs by **41.91291809082031 EUR/MWh**. It remains unscored and outside the candidate set.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1 | Starting state; preserve other work, v1/CP-10/restricted partitions; exact anchor and pre-run protocol committed before comparison | **PASS** | Recorded resumption state; inspected Git delta; exact preregistration blobs match; all protected path diffs empty; 116 manifest/input checks plus original historical-byte comparisons; model-input projection filters admissible dates before materialization. Review cannot independently recreate another session's historical working-tree status, but the retained state/diff/provenance evidence is consistent. |
| 2 | Every B0–B3/A1–A5 policy; common uncertainty; genuine rolling fits, warm-up provenance and causal normalization | **PASS** | Source/protocol match all nine definitions; every fold fit/issued/feedback/origin record independently replayed; exact B1, B0 and ensemble checks; historical per-row normalization and minimum-window sufficiency; fresh representative production fits and synthetic fixtures. |
| 3 | Availability, D-2, single consumption, DST/schema refusals with positive controls and inherited live guards | **PASS** | 339 passing tests, including full schema/masking/DST/feedback/live namespace controls; full production future-mask zero change; D-1 positive-control movement for all five fitted policies; exact release/error lineage reconstruction. |
| 4 | Same original eligible hours; complete §7 metrics/diagnostics for every arm; independent count/order/score/window checks | **PASS** | 96,723 rows; original eligible sets and targets match each policy; all emitted vectors finite/ordered; own arithmetic audit plus complete saved-evidence checker verify metrics, exact denominators, peak/recovery and bootstrap tables. |
| 5 | Mechanical ranking and all six product criteria; both statuses, best observed/qualified policy and failures | **PASS** | All criteria and subchecks independently reproduce; A1 best, none qualifies; failures listed above and with actuals/limits in candidate report/criteria. Candidate report honestly marks Integration pending; this verdict supplies PASS. The subsequent evidence-only report/terminal packet must carry both statuses without modifying the reviewed statistical candidate. |
| 6 | Pinned Chronos-2 probe and structural input feasibility sheet; honest limitations, no candidate promotion | **PASS** | Fresh isolated offline probe matches four digests, respects proper-training/target projection controls and resource bound. Pinned metadata/license record, documented source retrievals and input-by-input feasibility gaps inspected. No neural score, new fundamental model or new-source performance claim. |
| 7 | Reproduction/dependency/input/protocol hashes, seeds, chronological validation, resources, dependence-aware uncertainty and regression controls | **PASS** | Frozen offline core/probe installs; all 116 manifest files/input/payload hashes verified; 45 resource rows recomputed; 240 bootstrap contrasts independently rederived; recorded numerical failures/repair; 339-test suite passes with no skip; representative exact reproduction succeeds. |
| 8 | Fresh independent exact-candidate clean review; independently recompute metrics and causal/fit reproduction; record commands/limitations; later evidence-only commit | **PASS** | This fresh procedural detached review binds the stated full SHA; clean start/end and branch reachability checked; independent arithmetic and saved-evidence audits plus two production fit reproductions completed. Verdict written outside candidate only after checks. Lead must commit it afterwards, preserve prior-attempt verdict, and verify the candidate-to-evidence-tip delta remains confined to `docs/track-b/evidence/cp-15/`. A future evidence-tip SHA does not yet exist at this review boundary and is not falsely certified here. |

## Limitations and handover boundary

- This review did **not** refit the entire five-fold experiment from scratch. It independently audited all saved row/fit/residual/scoring evidence and refit two representative full production origins, including the required causal controls. The bar explicitly requires representative reproduction, and that check passed.
- Timing was observed during concurrent local validation/probe work. Fresh timings are not isolated throughput estimates. Process RSS is not whole-machine memory, and sampled probe RSS can miss brief peaks.
- Original A65 load-vintage availability is an inherited assumption openly recorded by the plan/protocol; this review does not invent original vintage proof. The feasibility sheet's 16 dated primary-source retrieval records were inspected; no live source refresh or new data acquisition was performed by this Critic. Unverified structural vintage/redistribution/coverage properties remain gaps, not ready inputs.
- The foundation-model probe cannot establish historical out-of-sample accuracy or exclude pretraining overlap. The 17-day peak is descriptive, and all inference is exploratory after selection.
- The negative product decision remains controlling. Nothing here authorizes freezing/promoting a policy, publication, a mainline operation, or later-checkpoint work.
- No engineering changes are requested. The only remaining Lead actions are evidence retention, an evidence-only commit/delta check, accurate terminal reporting, and the delegated cleanup of this review checkout.

## External review artifacts and SHA256

These are the actual outputs of this review. Hashes identify the files even if the Lead relocates copies under the permitted evidence directory. The Critic made no branch/worktree/tag itself; the named review worktree was supplied and remains for Lead cleanup.

```text
faace5553561aab7a8527b07ddbf9b03fee676b4c74477d82df048f86ef7d99c  /tmp/cp15-critic-arithmetic.py
67d994d008f2a30a0fdbc8b2698eabfbc6cb06d9f9a9b637acacffc368cf6c2f  /tmp/cp15-critic-arithmetic.json
ebcecc12e349cfa31a3b50a18288b5e67d7ffe59f6d8ab1b301ac94a248f5d74  /tmp/cp15-critic-provenance.py
4aba832451d5f9420c57c9b9aa2a2a9fc0a65b5e20a9d36877ec6199a6af8179  /tmp/cp15-critic-provenance.json
3308fd6c2612802f78a7d33448fa81f2c7889800b932b7a36417d8f88391bfc4  /tmp/cp15-critic-inspect.log
18979361e883161bb42d9aca967a9d511783cd4b52f1fce043bf758c69ccb36a  /tmp/cp15-critic-tests.log
12b82f277a5c9cca630eef44056aa919c313bf8a23c1729c43169598867b2844  /tmp/cp15-critic-fit-2020-07-01.json
2949bebf4e3237d2d237cb75d7901be6c66f99594748091d84e73cb722085b56  /tmp/cp15-critic-fit-2022-08-15.json
de8ce014622215b78e526fc705db7df2264639b7e635a7b6a48af39c1bdbef86  /tmp/cp15-critic-probe-install.log
530f4a1d75dffc1e882b4b6c8d4416b09d0807ae9cb869e93b8725f08678c9fe  /tmp/cp15-critic-probe.log
c2f27de6f1edab37a21c45d26504d4374fac4007ef03e9815382d115337e3fbe  /tmp/cp15-critic-fresh-probe/reproduction-comparison.json
5802f92432e1f4f320a82166bca2f79c265011905703b8ec29fdb18d6d9fc9dc  /tmp/cp15-critic-fresh-probe/reports/cp15/feasibility/resources.json
```

Interview-answer trigger: the normalized candidate can improve pooled crisis-heavy MAE while failing a deliberately equal-fold, best-reference improvement screen; the fixed decision rule was applied without changing the target or retrospectively relaxing thresholds.
