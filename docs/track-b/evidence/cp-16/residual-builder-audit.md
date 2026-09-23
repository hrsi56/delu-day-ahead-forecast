# CP-16 residual Builder execution and resource audit

This handoff records the residual Builder's three actual synthetic test executions and a later static audit of their warm-up/control costs. It is not a checkpoint verdict. The audit did not rerun residual code. The initial failure output below is copied from the actual tool response retained in this task's conversation; it is not reconstructed from another execution.

## Scope and environment

- Builder checkout: `/Users/djourno/Downloads/PJM/.local/worktrees/cp-16/builder-residual`.
- Owned source: `src/cp16/residuals.py` and `tests/cp16/test_residuals.py` in that checkout.
- Interpreter: `/Users/djourno/Downloads/PJM/.venv/bin/python`.
- Test inputs were synthetic; no estimator fitting, external inputs, downloads, or full policy replay occurred.
- No Git mutation or worktree management occurred in this Builder task.
- Pytest temporary data and the two newly created CP-16 `__pycache__` directories were removed after testing. This handoff artifact is retained for Lead import to durable evidence.

## Actual initial failed command and output

Working directory was the Builder checkout above. The exact `cmd` argument was:

```sh
mkdir -p /Users/djourno/Downloads/PJM/.local/tmp/cp-16/residual-pytest && /usr/bin/time -p env PYTHONPATH=/Users/djourno/Downloads/PJM/.local/worktrees/cp-16/builder-residual/src /Users/djourno/Downloads/PJM/.venv/bin/python -m pytest tests/cp16/test_residuals.py -q -s -p no:cacheprovider --basetemp=/Users/djourno/Downloads/PJM/.local/tmp/cp-16/residual-pytest
```

The tool returned exit code `1`, with `wall_time_seconds: 1.820787459`. Its exact output text was:

```text
F.................
CP16_RESIDUAL_RESOURCE_COUNTS={"prediction_calls_including_rejected": 24, "successful_policy_days": 36, "successful_policy_target_rows": 864}

=================================== FAILURES ===================================
_____________ test_d1_rejected_d2_accepted_once_and_copy_immutable _____________

    def test_d1_rejected_d2_accepted_once_and_copy_immutable():
        state = SharedResidualState()
        day = date(2024, 1, 1)
        ix = day_hours(day)
        a1, b2, scale = np.full(len(ix), 10.), np.full(len(ix), 30.), np.full(len(ix), 2.)
        state.issue(day, ix, a1, b2, scale)
        a1[:] = b2[:] = scale[:] = 999
>       ix.values[0] += np.timedelta64(1, 'h')
        ^^^^^^^^^^^^
E       ValueError: assignment destination is read-only

tests/cp16/test_residuals.py:57: ValueError
=========================== short test summary info ============================
FAILED tests/cp16/test_residuals.py::test_d1_rejected_d2_accepted_once_and_copy_immutable
1 failed, 17 passed in 1.07s
real 1.80
user 1.36
sys 0.20
```

The fixture attempted to mutate a pandas timestamp array that was already read-only. The replacement assertion checks that the caller's index array and the saved issuance index do not share memory. The first execution stopped that test before its duplicate-issuance attempt.

## Actual successful commands and output

Both subsequent executions used this exact command, from the same working directory:

```sh
/usr/bin/time -p env PYTHONPATH=/Users/djourno/Downloads/PJM/.local/worktrees/cp-16/builder-residual/src /Users/djourno/Downloads/PJM/.venv/bin/python -m pytest tests/cp16/test_residuals.py -q -s -p no:cacheprovider --basetemp=/Users/djourno/Downloads/PJM/.local/tmp/cp-16/residual-pytest
```

Run 2 returned exit code `0`, with `wall_time_seconds: 1.397589208`. Its exact output text was:

```text
..................
CP16_RESIDUAL_RESOURCE_COUNTS={"prediction_calls_including_rejected": 24, "successful_policy_days": 36, "successful_policy_target_rows": 864}

18 passed in 0.82s
real 1.40
user 1.25
sys 0.13
```

Run 3 returned exit code `0`, with `wall_time_seconds: 1.799184125`. Its exact output text was:

```text
...................
CP16_RESIDUAL_RESOURCE_COUNTS={"prediction_calls_including_rejected": 27, "successful_policy_days": 42, "successful_policy_target_rows": 1008}

19 passed in 1.04s
real 1.80
user 1.42
sys 0.18
```

| Execution | Passed | Failed | Pytest elapsed seconds | `time -p` real | `time -p` user | `time -p` sys |
|---|---:|---:|---:|---:|---:|---:|
| Run 1 | 17 | 1 | 1.07 | 1.80 | 1.36 | 0.20 |
| Run 2 | 18 | 0 | 0.82 | 1.40 | 1.25 | 0.13 |
| Run 3 | 19 | 0 | 1.04 | 1.80 | 1.42 | 0.18 |
| Sum | 54 | 1 | 2.93 | 5.00 | 4.03 | 0.51 |

These are test/command timings, not total Builder task elapsed time. No independent per-run peak memory measurement was collected. Exact wall-clock start/end timestamps were not recorded in the returned command outputs.

## Static warm-up and control debit

The initially printed resource counters cover prediction calls and successful emitted rows only. They do not include warm-up registrations, and the Builder's earlier 114-policy-day report therefore understated the budget scope. The following corrected audit counts all `SharedResidualState.issue()` attempts, including invalid attempts and warm-up, plus every `predict()` attempt. Each attempt is conservatively charged to both arms. No deduplication is applied.

The counts were derived from the three actual source versions visible in the task's patch/run history; no test was rerun for the audit.

| Test group | Run 1 `issue()` attempts | Run 2 `issue()` attempts | Run 3 `issue()` attempts |
|---|---:|---:|---:|
| D−1/D−2, immutability, duplicate | 1 | 2 | 2 |
| Canonical DST, three parameters | 12 | 12 | 96 |
| Partial issuance | 2 | 2 | 2 |
| Nonfinite truth | 0 | 0 | 1 |
| Late truth | 30 | 30 | 30 |
| Insufficient common history | 28 | 28 | 28 |
| Row-specific scales | 28 | 28 | 28 |
| Hour shrinkage | 28 | 28 | 28 |
| DST support, two parameters | 56 | 56 | 56 |
| Sparse helper | 0 | 0 | 0 |
| Linear quantiles/ties/parity | 56 | 56 | 56 |
| Restart replay | 32 | 32 | 30 |
| Invalid components/scales, three parameters | 87 | 87 | 87 |
| Invalid persisted state | 28 | 28 | 28 |
| **Total** | **388** | **389** | **472** |

| Execution | `issue()` attempts | `predict()` attempts | Two-arm attempt debit | Extra direct-restoration debit | Recommended conservative debit |
|---|---:|---:|---:|---:|---:|
| Run 1 | 388 | 24 | 824 | 0 | 824 |
| Run 2 | 389 | 24 | 826 | 0 | 826 |
| Run 3 | 472 | 27 | 998 | 4 | 1,002 |
| **Total** | **1,249** | **75** | **2,648** | **4** | **2,652 policy-days** |

The final run's extra four policy-days count its two directly restored pending records as registrations too. Earlier versions restored those two records by calling `issue()`, already included in their method-call counts. This additional debit avoids reducing the accounting merely because the restoration implementation changed.

Version differences are exactly:

1. Run 2 reached the duplicate-issuance assertion that Run 1's fixture failure prevented: one additional `issue()` attempt.
2. Run 3 added three 28-day populations and three predictions to the canonical-DST tests: 84 additional `issue()` attempts and three additional `predict()` attempts.
3. Run 3 added the nonfinite-truth test: one additional `issue()` attempt.
4. Run 3 restored two pending records directly into immutable `_Issued` objects, instead of invoking `issue()`: two fewer literal `issue()` calls, conservatively charged separately above.
5. The invalid-persisted-state test was present in all three executions.

Potential overlap is deliberately not deducted. Restart replay predicts the already registered origin day in the original and restored states. This is two literal `issue()`/`predict()` overlaps in each earlier run, and one literal overlap plus one direct-restoration overlap in the final run. Some rejection and scale controls repeat the same state/day too. The conservative debit charges every attempt separately.

For reconciliation only, the successful-prediction counters across the three actual outputs sum to 114 policy-days and 2,736 policy-target rows. These narrower counters must not replace the 2,652-policy-day conservative warm-up/control debit.

## Lead-supplied terminal resource proposal

The Lead supplied the following intended aggregate when requesting this artifact:

| Contribution | Policy-days |
|---|---:|
| Residual Builder conservative warm-up/control debit | 2,652 |
| Lead execution, supplied by Lead | 1,002 |
| Production, supplied by Lead | 76 |
| **Proposed terminal total** | **3,730** |

Only the Builder contribution was audited here. The Lead and production contributions are quoted from the Lead's request, not independently verified by this bounded Builder. The proposal leaves 770 policy-days below a 4,500-policy-day ceiling before any additional unaccounted work. This arithmetic is not a checkpoint certification.
