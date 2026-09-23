# Verdict — CP-16 — Integration — FAIL

- Candidate SHA: `3a160fd33ed92bb0061144cfbce2323d8b3a7db9`
- Plan / version / bar: `capstone_v21.md`, `v21-r2`, §14.8, all ten items; applicable §§2–9 and complete §14 read.
- Independent Critic canonical agent identity: `/root/integration_critic`.
- Review checkout: `/Users/djourno/Downloads/PJM/.local/worktrees/cp-16/critic`, clean detached HEAD at the candidate throughout review.
- Worktree clean before and after: **yes**; `git status --porcelain=v1` returned empty and `git rev-parse HEAD` returned the full candidate SHA before and after checks. No candidate edits or Git mutations made.
- Verdict scope: the complete acceptance bar. A review could be performed; missing required artifacts and unperformed mandatory checks mean FAIL, not Critic BLOCKED. The Lead's operational BLOCKED return is a separate status.

## Verbatim bar excerpt

The following excerpt was compared byte-for-byte (apart from surrounding blank lines) with the assignment and the committed anchor. It matched.

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


## Commands actually run

All commands except the initial absolute-path assignment read ran with working directory `/Users/djourno/Downloads/PJM/.local/worktrees/cp-16/critic`. The initial assignment read ran from the project root and opened only `.local/tmp/cp-16/integration-assignment.md`; it did not interpret root-checkout code or evidence.

For the five monitored commands below the exact common prefix was:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/Users/djourno/Downloads/PJM/.local/worktrees/cp-16/critic/src /Users/djourno/Downloads/PJM/.venv/bin/python scripts/cp16_v2.py --monitor --ledger /Users/djourno/Downloads/PJM/.local/artifacts/cp-16/budget.json --project-root /Users/djourno/Downloads/PJM --log LOG -- COMMAND
```

| LOG under `/Users/djourno/Downloads/PJM/.local/artifacts/cp-16/` | COMMAND, appended to the exact prefix | Exit | Observed output |
|---|---|---:|---|
| `critic-tests.log` | `/Users/djourno/Downloads/PJM/.venv/bin/python -m pytest tests/cp16/test_monitor.py tests/cp16/test_budget_inputs.py tests/cp16/test_scoring.py -q -p no:cacheprovider --basetemp=/Users/djourno/Downloads/PJM/.local/tmp/cp-16/critic-tests` | 0 | **34 passed in 4.88s**; monitor elapsed 5.762243s; peak RSS 257785856 bytes; no abort. |
| `critic-guards.log` | `/Users/djourno/Downloads/PJM/.venv/bin/python -m pytest tests/test_02_rolling_closed_left.py tests/test_05_schema_firewall.py tests/test_08_partition_integrity.py tests/test_12_partition_exclusion.py tests/test_24_live_namespace_is_walled_off.py -q -p no:cacheprovider --basetemp=/Users/djourno/Downloads/PJM/.local/tmp/cp-16/critic-guards` | 0 | **25 passed in 3.39s**; monitor elapsed 4.527949s; peak RSS 311836672 bytes; no abort. |
| `critic-audit.log` | `/Users/djourno/Downloads/PJM/.venv/bin/python /Users/djourno/Downloads/PJM/.local/tmp/cp-16/critic/audit.py` | 0 | 19 artifact, 20 implementation and 31 in-scope input hashes matched; exact bar and historical protocol hash matched; 10747 original keys, zero duplicates, fold counts 2160/2159/2112/2160/2156; five required output files absent; only seven fold-1 admission dates. Monitor elapsed 0.558750s. |
| `critic-final-audit.log` | `/Users/djourno/Downloads/PJM/.venv/bin/python /Users/djourno/Downloads/PJM/.local/tmp/cp-16/critic/final_audit.py` | 1 | Raw interrupted lineage hash/prefix preserved. Audit then failed its direct `DatetimeIndex.equals` assertion because JSON timestamps parsed at microsecond precision and Parquet timestamps at millisecond precision. No candidate defect inferred from this failed audit. Monitor elapsed 0.818456s; failed job retained and charged. |
| `critic-final-audit-normalized.log` | `/Users/djourno/Downloads/PJM/.venv/bin/python /Users/djourno/Downloads/PJM/.local/tmp/cp-16/critic/final_audit_normalized.py` | 0 | Printed `datetime64[us, UTC]` versus `datetime64[ms, UTC]` in all five folds; after converting both to nanoseconds, every exact UTC target key matched. Raw interrupted lineage content was preserved except labeled status/additional notices. Monitor elapsed 0.547886s. |

Supporting audit scripts are at the exact command paths above. Each only reads candidate evidence and prints findings. These scripts/logs are retained under authorized `.local` paths for Lead import; no durable candidate source was edited. Unit-test temporary ledgers are synthetic fixtures inside the designated pytest basetemps; every actual review compute job used the existing shared ledger. No new blank production ledger was created.

Read-only shell inspection commands also exited 0: `git status --porcelain=v1`; `git rev-parse HEAD`; `git log -6 --format='%H %s'`; `git show -s --format='%H %ct %s' e625967e20f3f79f2c4d07c9b414065ff0717d02`; `git diff --name-only 6621402b2be9aed85be433432bcffffb56adf3e4 HEAD`; `rg --files reports/v2-causal docs/track-b/evidence/cp-16 src/cp16 tests/cp16`; and `cat`/`sed`/`tail` reads of the evidence and code named below. The baseline-to-candidate path list contains only the three supplied immutable governance documents and authorized CP-16 source, tests, driver, reports and evidence paths. No inherited CP-15, v1, mainline or unrelated program-state path appears. The pre-run commit was reachable and its protocol SHA256 matched `b35bdf131d4620d7a3821c7832d7aea9ea4674500d70db3422a12cb371c355b4`.

## Evidence actually inspected

- Exact assignment; committed `capstone_v21.md`, named amendment and `docs/track-b/cp-16-v2-brief.md`; canonical Integration verdict form in `docs/track-b/gauntlet-templates.md` §2.
- All existing `reports/v2-causal/` artifact types: protocol, input manifest, artifact manifest, lineage, resources, failures, report and reproduction instructions. The JSON audit examined full identities, fold/origin/key collections, admission entries and component-reproduction summaries. It did not refit the reported components.
- `docs/track-b/evidence/cp-16/resource-accounting-audit.md`, `residual-builder-audit.md`, `supervisor-failure-record.json`, raw `interrupted-admission-lineage.json`, and the preserved admission log ending in `KeyboardInterrupt` inside a Lasso fit. Candidate monitor/input/scoring tests and inherited guards were actually rerun as above.
- `src/cp16/inputs.py`, `residuals.py`, `execution.py`, `budget.py`, driver `scripts/cp16_v2.py`, scoring population/metrics/criteria implementation and corresponding monitor/input/scoring tests. Code inspection is not substituted for missing executed causal/component/state verification.
- Saved CP-15 B0 target metadata, projected to fold/timestamp/date only. Exact manifest key comparison and counts were independently performed. The main audit hashed immutable bytes, including snapshot bytes, without materializing prohibited outcomes. Inherited partition tests read timestamp metadata, not held-out outcomes. No spent holdout or reserved-tail outcomes were fitted, scored or selected on.
- Existing shared ledger before review and monitor-written job records. No residual state execution, model fitting, full saved-reference score pass or production bootstrap pass was performed by this Critic. Synthetic scoring fixtures do not constitute independently recomputed saved-prediction metrics.

## Findings

The candidate is explicitly partial. `predictions.parquet`, `metrics.csv`, `diagnostics.csv`, `uncertainty.csv` and `criteria.csv` are absent from `reports/v2-causal/`. Only 7 of 35 required admission dates (14 of 70 policy-days) are recorded. Preserved lineage contains 37 fold-1 origins, 8 fresh component-date pairs, one fold's state, and one cached-date A1/B2 reproduction whose reported differences are exactly zero. Those reported component differences were inspected, not independently reproduced here. There is no outer H/P comparison to score or rank and no new §8 diagnosis.

The intended original population is intact: all 10747 exact UTC keys match the saved reference, with the five mandated fold counts. This establishes population identity only; it does not establish the 75229 required finite ordered prediction rows.

The corrected replay debit is 3730/4500, leaving 770. The recorded planned complete pass requires 1276 policy-days, of which 1200 remain; the shortfall is already 430 before remaining controls and independent reproduction. The full residual suite's conservative 1002-policy-day debit exceeds the remaining allowance. Neither that suite nor a new comparison was run. A smaller synthetic control would not remedy the missing complete evaluation, so further residual spending was avoided. No cap amendment is authorized by this verdict.

Resource enforcement is not fully demonstrated. The admission monitor originally crashed on a disappearing atomic-rename temporary file and left the worker running until explicit interruption. The original worker exit was not reaped; peak RSS in that gap is unknown. The fail-closed repair passes the observed regression tests, but it cannot retrospectively prove uninterrupted enforcement. Early synthetic Builder jobs were also outside the Lead supervisor and retrospectively debited. Their durable command records set `PYTHONPATH` but do not record a BLAS-thread pin, measured thread count, or aggregate concurrency. Consequently the global `resources.json` summary claims `BLAS_threads=1` and `max_CPU_workers=1` are unsupported for all checkpoint jobs. This is an evidence limitation/overclaim, not proof of a CPU or memory ceiling exceedance. Scope those claims to monitored jobs and report the earlier unknowns explicitly.

The review added five monitored jobs, including the failed timestamp-audit attempt, and no fit/replay counts. Their elapsed times total about 12.215 seconds; final exact aggregate machine accounting is in the shared ledger after monitor finalization. The last in-job snapshot was 623.792378 machine-seconds and is not the final ledger total. Fit counts remained 21 component attempts, 17 main component attempts, 2494 primitive calls, 1996 inner and 498 final calls; policy-days remained 3730. No bootstrap/reference production analysis pass was used by this review. Lead must preserve the finalized resource ledger with the terminal packet.

The report correctly distinguishes incomplete Engineering work, historical CP-15 NOT_DEMONSTRATED, unassessed research results and no delivery/promotion authority. An incomplete evaluation is not an honestly negative completed research finding. No predictive benefit, absence of benefit, equivalence or supported preference can be inferred.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1 | Actual state, preserved inputs, committed protocol and identities | PASS | Candidate clean and exact SHA; immutable supplied inputs and current source/artifact identities matched; pre-run protocol commit reachable before recorded admission; authorized baseline delta only; original target keys matched exactly. Resource-accounting completeness is separately failed under item 7. |
| 2 | Fixed blend and frozen H/P constructions admitted on permitted training data | FAIL | Shared implementation visibly uses the fixed central/scale/error state and differs only in hour pooling, but only fold-1 admission exists. Required all-fold training-only admission/freeze is incomplete. Source review cannot certify the whole construction. |
| 3 | Complete causal, component, state, cache, DST and positive/negative controls | FAIL | 25 inherited guards and bounded monitor/input checks pass. Required origin mutation fits, full training admission, independent component and representative state replay were not completed for this review; saved partial logs are insufficient. |
| 4 | Complete original forecasts and exact denominators | FAIL | Original 10747 keys and all fold counts verified; required 75229 output rows absent. No finite/ordered-vector or emitted-p50 claim can be made for missing outputs. |
| 5 | Independently recomputed saved scores, diagnostics and references | FAIL | Synthetic scoring tests pass, including WIS fixture and population refusal. Actual comparison predictions and metric/diagnostic tables are absent, so emitted-vector scores, all references and denominators could not be independently recomputed as required. |
| 6 | Frozen research inference and all six original product diagnostics | FAIL | Rules and separation of statuses are documented, but actual ranking, paired intervals and six diagnostic results are unassessed. Appropriate withholding of conclusions does not complete the evaluation. |
| 7 | Every numeric cap enforced and reported, including failures/review | FAIL | Warm-up accounting corrected to 3730/4500 and work stopped without unauthorized extension. Original supervision gap and early unmonitored Builder resource limits are not certifiable; aggregate BLAS/worker summary claims need qualification. Repairs and final monitored tests do not erase the gap. |
| 8 | Complete durable artifacts, reproducibility, controls and disclosures | FAIL | Partial protocol/lineage/failure/resource evidence, notices and safe checks are present; missing prediction/metric/diagnostic/uncertainty/criteria deliverables and unperformed mandatory reproduction prevent completion. Defects and interrupted evidence are preserved honestly. |
| 9 | Fresh exact-candidate Integration PASS with independent reproduction | FAIL | This is a fresh independent clean-checkout review binding the stated SHA, but mandatory saved-vector recomputation and component/state reproduction are absent; therefore no Integration PASS. |
| 10 | Complete canonical terminal packet and bounded local stop | FAIL | Candidate lacks the terminal checkpoint return and eventual evidence-tip SHA/delta, which necessarily follow review; those must be assembled by Lead. No future-stage or publication work was performed in this review. Even a complete non-PASS return cannot cure items 2–9. |

## On FAIL only

- **Single largest meaningful gap:** the bounded experiment never reached a complete five-fold evaluation. No H/P comparison predictions or downstream scores/diagnostics/uncertainty exist, and the recorded remaining replay allowance is insufficient for the outstanding production work before mandatory review.
- **Exact next acceptance test:** only under properly amended authority sufficient for the complete work, preserve existing debits and invalidated evidence, complete all 35 training-only admission dates and every prescribed causal/control/reproduction check, then produce exactly 75229 finite ordered rows (10747 exact original keys for each of seven policies; fold counts 2160/2159/2112/2160/2156). A fresh independent Critic must recompute emitted-p50 MAE, seven-quantile WIS, equal-fold B0 normalization, all diagnostics, original six §8 criteria and the frozen 2000-replicate paired bootstrap from saved vectors; verify component/state reproduction at component atol 1e-8/rtol 1e-10, scoring atol/rtol 2e-12, and exactly 0.0 leakage with moving positive controls; verify complete instrumented resource evidence; and bind all ten items to a new clean final candidate. Current authority does not permit increasing the replay ceiling or silently omitting required work.

No program-state, Q&A, locked-governance, next-checkpoint, publication or mainline mutation was performed. Lead owns byte-for-byte verdict import, terminal evidence accounting and removal of this checkpoint-created Critic checkout.
