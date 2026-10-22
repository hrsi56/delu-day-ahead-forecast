# CP-26-CI test contract

Authority: the byte-identical `issued-brief.md` in this directory, its complete six-item bar,
and `capstone_v21.md` v21-r17 §§24.2, 24.7 and 24.9. This checkpoint changes tests and adds
evidence only. The research harness, its pins, the completed results and the living ledger
are unchanged.

## Stress inventory

These 15 functions collect as 16 tests (the supervisor SIGSTOP case has two parameters).
Each starts real concurrent supervision and asserts its timing, progress, completion ordering
or elapsed accounting. Only decorators are added; every function body remains identical.

| Module under `tests/` | Function | Why it qualifies |
|---|---|---|
| test_cp26_monitor.py | test_outer_monitor_hard_death_retains_independent_failed_job_receipt | Launcher death after active accounting must retain independently observed completion and elapsed charge. |
| test_cp26_monitor.py | test_supervisor_hard_death_gets_independent_bound_ending_receipt | Live supervisor death must trigger watchdog termination and positive observed runtime. |
| test_cp26_monitor.py | test_registered_detached_worker_is_not_lost_when_parent_exits | Parent completion must trigger orphan detection and termination while the detached worker remains active. |
| test_cp26_supervision.py | test_sigstop_supervisor_stops_verified_worker_even_after_launcher_loss | Both parameter cases require stale-heartbeat takeover, worker termination and independent elapsed accounting. |
| test_cp26_supervision.py | test_supervisor_stopped_inside_ledger_lock_is_killed_before_receipt | A stalled lock must cause termination before a terminal receipt is issued. |
| test_cp26_supervision.py | test_stopped_watchdog_is_detected_by_supervisor | Shutdown after watchdog stoppage must remain within the declared exposure bound. |
| test_cp26_supervision.py | test_launcher_shutdown_receipts_workers_and_watchdog | Launcher termination must complete concurrent worker and watchdog shutdown. |
| test_cp26_supervision.py | test_launcher_enforces_when_both_accounting_loops_are_stopped | The launcher must take over after both accounting loops stop and independently charge terminal duration. |
| test_cp26_ledger_liveness.py | test_three_jobs_keep_fresh_supervision_with_full_future_history | Three concurrent monitors must retain freshness, sampler advancement and bounded lock telemetry. |
| test_cp26_ledger_liveness.py | test_wedged_supervisor_lock_still_gets_independent_ending_receipt | Real lock timeout must lie between the ledger and heartbeat deadlines, followed by independent termination. |
| test_cp26_ledger_liveness.py | test_supervisor_startup_accounting_wait_uses_declared_poll_cadence | The actual startup accounting wait must request the declared 0.2-second poll cadence. |
| test_cp26_ledger_liveness.py | test_duplicate_live_request_refuses_before_spawn_and_preserves_original_clock_and_receipt | A concurrent rejected replay must leave the original observer sequences advancing before normal completion. |
| test_cp26_ledger_liveness.py | test_fast_terminal_job_allows_read_only_late_launcher_binding_and_same_receipt | A patched CLI launch forces completion before launcher binding and requires the same receipt and elapsed charge. |
| test_cp26_ledger_liveness.py | test_rich_closed_jobs_three_busy_owners_accept_fourth_admin_with_full_future_history | Three busy owners plus an arriving admin must retain freshness, sampler advancement and bounded lock telemetry. |
| test_cp26_ledger_liveness.py | test_actual_search_accounting_timeout_aborts_without_fit_or_failed_trial_cache | A monitored child with a concurrent lock holder must time out before any fit or failed-trial cache write. |

`test_real_denied_detached_worker_never_reaches_computation` remains unmarked: it checks
registration denial, an absent computation marker and cleanup, with no timing/progress assertion.
Its `wait(timeout=15)` is harness patience. Tests using only synthetic identities or mocked
monitors are also unmarked.

`tests/conftest.py` registers `stress` and applies the skip only for the exact combination
`CI=true` and `RUN_STRESS != 1`. Its skip reporting makes the reason visible with the workflow's
unchanged `pytest -q`. The reason is:

CP-26 supervision stress test, run locally because a 4-vCPU CI runner cannot host it reliably,
RUN_STRESS=1 forces it.

Before editing conftest, `git grep` over committed `docs/track-b/evidence/` found no explicit
byte binding for its SHA-256 `ae50b3a26ff4a39235a1d0fb5665ca7b5ac51e0e39bc6d6534531b20b552aefd`
or Git blob `080759376f1d56b9ce991285cd37f5167746ac95`. Its eight path references are inspection
records, historical tracebacks and a path listing; none asserts a conftest hash. Historical
candidate trees continue preserving their original bytes.

## Ledger identity and preservation

`docs/track-b/evidence/cp-26/exposure-ledger-frozen.md` is copied byte for byte from
`61658c70520b880d844b1bb54af9973cf2851d9d:docs/track-b/exposure-ledger.md`.
Its SHA-256 is `375fef5d200c400b79840dcc9977ab3d63a95ed85af603c8add3b9a9210d98a6`, the existing
`harness.PINS['docs/track-b/exposure-ledger.md']`. This is new evidence; no earlier evidence
file is overwritten.

The only tests that hash the live ledger for historical identity now resolve that key to the
frozen copy through `tests/cp26_ledger_snapshot.py`:

- `test_cp26_r15.py::test_r15_authority_does_not_relabel_scientific_plan_or_parity`: the
  scientific-input identity loop; its original fingerprint keys and hashes stay unchanged.
- `test_cp26_repair_contract.py::test_anchor_commit_and_landed_base_are_distinct_and_explicit`:
  the harness-pinned identity loop.

`test_cp26_exposure_ledger.py::test_live_exposure_ledger_preserves_frozen_cp26_rows` verifies the
frozen copy's pin and requires the live table to begin with every frozen row, verbatim and in
order, including the header and separator. Later rows and changes to preceding prose are allowed.
The historical harness's runtime identity guard remains frozen; this test-only maintenance does
not authorize another scientific run against an amended ledger.

## Reproduction contract

For each mode below, create a separate history-free tree with `git archive <candidate>`,
extract it inside the project's `.local/`, initialize `main`, add the tree and commit it once
using `git commit -F <message-file>`. Install this repository's secret hooks in that scratch
repository too; never use `--no-verify`. Confirm there is exactly one commit and that its tree
equals `<candidate>^{tree}`. Use a fresh `UV_PROJECT_ENVIRONMENT` for each copy/interpreter,
`UV_PYTHON=3.12` or `3.13`, unset `PYTHONDONTWRITEBYTECODE`, and export
`MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1`. No credentials are needed. Keep temporary files,
caches and pytest temporary roots inside this project.
Set `GIT_CEILING_DIRECTORIES=<copy>/.local/tmp` at the temporary-root boundary: otherwise the
existing session-hook test's intentionally non-repository directory discovers the enclosing
scratch repository. Git repositories explicitly created by other fixtures still work normally.

1. `CI=true`, Python 3.12 and 3.13 separately: run all seven issued workflow commands in order.
   Expect 16 additional skips, each carrying the supervision-stress reason.
2. Unset `CI` and `RUN_STRESS`, Python 3.12 on an otherwise quiet machine: build the WASM
   payload, then run the full suite; the 16 stress cases must run by default.
3. `CI=true RUN_STRESS=1`, Python 3.12: `uv run pytest -m stress -q`; exactly the 16 cases run.
4. In another single-commit copy, build the payload, append a synthetic row to the live ledger
   (and change prose above the table), then run the full suite. All tests must pass. Restore its
   original bytes, alter an existing frozen row, and run the named preservation test. It must fail.
5. `uv run pytest --collect-only -m stress -q` must select exactly the inventory above.

Remove temporary copies and environments after recording outcomes. The final fresh Integration
Critic independently checks the full six-item issued bar, repeats both ledger mutations and the
Python 3.12 CI workflow, and records commands and outcomes in `integration.md`.
