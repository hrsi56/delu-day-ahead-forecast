# CP-16 reproduction — v21-r3

Use the inherited pinned `uv.lock` environment; this checkpoint installed nothing. Python and package versions are in `input-manifest.json`. All commands must run from the reviewed checkout, on CPU, through the driver monitor with a shared persistent ledger. Do not create a fresh ledger to evade cumulative caps. Each external replay needs remaining authorized allowances; production and review logs show the commands actually run in this checkpoint.

Set these shell variables to project-local paths (the environment is shared read-only across worktrees):

```sh
CP16_PROJECT=/Users/djourno/Downloads/PJM
CP16_PY=/Users/djourno/Downloads/PJM/.venv/bin/python
CP16_BUDGET=/Users/djourno/Downloads/PJM/.local/artifacts/cp-16/budget.json
CP16_LOGS=/Users/djourno/Downloads/PJM/.local/artifacts/cp-16
```

The wrapper sets BLAS/OpenMP/NumExpr threads to1 before imports, uses one serialized process tree, samples RSS and disk, and terminates the process group if monitoring fails or a cap is reached. Never invoke a real-data replay outside it.

A production command has this form, replacing JOB with preflight, admission, controls, comparison or score:

```sh
"$CP16_PY" scripts/cp16_v2.py --monitor --ledger "$CP16_BUDGET" --project-root "$CP16_PROJECT" --log "$CP16_LOGS/reproduction-JOB.log" -- "$CP16_PY" -u scripts/cp16_v2.py --job JOB --ledger "$CP16_BUDGET"
```

The exact order used is metadata/training preflight, synthetic tests, committed protocol, training-only admission, committed admission freeze, causal controls, comparison, score. Admission refuses an existing lineage and comparison refuses an incorrect/completed stage. These are deliberate safeguards against an unaccounted automatic rerun. Reconstruct a full production attempt only in an explicitly allocated project-local output directory, copying the exact input manifest and retaining all old artifacts; use `--output` for that directory. Required protocol remains committed at the candidate before fitting. No scientific knobs change between runs. The interrupted lineage under `attempt-1/` is not an admissible resume cache.

Review should ordinarily use the durable vectors and independent checks, which avoid unnecessary new model fitting:

```sh
"$CP16_PY" scripts/cp16_v2.py --monitor --ledger "$CP16_BUDGET" --project-root "$CP16_PROJECT" --log "$CP16_LOGS/review-tests.log" -- env CP16_REQUIRE_SAVED_EVIDENCE=1 "$CP16_PY" -m pytest tests/cp16 -q -s -p no:cacheprovider --basetemp="$CP16_PROJECT/.local/tmp/cp-16/review-tests"
```

`test_saved_results.py` independently recomputes emitted-vector metrics, every diagnostic/denominator, all six quality criteria, ranking and the paired bootstrap; it reserves one saved-reference and one analysis pass. `test_state_results.py` independently reconstructs every real-data H/P date with exact release/common-buffer/hourly shrinkage and compares all 21,494 new vectors; it charges 1,276 policy-days. A separate real restart/cache refusal control reserves a conservative76 policy-days for the37 warm-up dates plus first evaluated date. Synthetic tests use no research data and carry no new policy-day charge. State tolerances: at most1e-10 absolute plus1e-12 relative; recorded hashes and deterministic state equality are exact. All actual tests and limits belong in the final Critic verdict.

Representative component and causal reproduction:

```sh
"$CP16_PY" scripts/cp16_v2.py --monitor --ledger "$CP16_BUDGET" --project-root "$CP16_PROJECT" --log "$CP16_LOGS/review-components.log" -- "$CP16_PY" tests/cp16/reproduce_components.py --output "$CP16_PROJECT/.local/artifacts/cp-16/review-components.json"
```

This script verifies fresh A1/B2 fits at 2020-07-01/fold1 and 2021-04-01/fold2, exact model/imputer/scaler/training hashes, centers at atol1e-8/rtol1e-10, target/future masking with exactly0.0 change and an available D−1 mutation with strictly nonzero change. It reserves8 policy-days and8 component attempts plus all actual primitive calls. The output is ignored local evidence to import after the clean review; no tracked file is changed by this command.

Applicable inherited guards are tests/test_02_rolling_closed_left.py, test_05_schema_firewall.py, test_08_partition_integrity.py, test_12_partition_exclusion.py, test_24_live_namespace_is_walled_off.py. Additional inherited synthetic transforms/schema fixtures in tests/cp15/test_pipeline.py are run with `-k 'not test_fit_delivery_mask_positive_d1_and_rolling_refit'` to exclude unauthorized A4/B3/A2 fits. Do not run the whole inherited pipeline or read prohibited outcomes merely because a file is named a test.

All input SHA256 values and origin/target keys are in the manifest. Final artifact hashes bind source, tests, reports and current pre-review evidence; the evidence-only terminal additions are verified by Git candidate-to-evidence diff. `resources.json` is the candidate snapshot; `docs/track-b/evidence/cp-16/resource-final.json` includes the complete review debit. Historical invalidated evidence and monitoring limits remain preserved separately. All results are development_post_selection, and nothing here selects or publishes a live policy.
