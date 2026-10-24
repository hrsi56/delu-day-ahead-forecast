# CP-26-CI landing — 2026-10-24

**CP-26-CI is closed.** It was a test-only maintenance round after CP-26.

- **CP-26's real-monitor supervision stress tests skip on GitHub's runner,** with the reason shown,
  and run everywhere else.
- **CP-26's exposure ledger is frozen as evidence,** so the live ledger can grow for the 4.7T audit.

No scientific output, source file, script, workflow or dependency changed.

## Identities

| Item | Value |
|---|---|
| Brief | `docs/track-b/evidence/cp-26-ci/issued-brief.md`, SHA-256 `3b6c63fe0ca65c91b999b0de6d579bae6930fd0b7dbc22ad86745ea70881c0d0`, issued 2026-10-21, packaged byte-identical from its canonical file |
| Anchor | `capstone_v21.md` v21-r17, SHA-256 `3124451da84c3cd99fae728c371207aace6ae537474f7769d0ff6333ee53e4fc`, unchanged |
| Final candidate (the Integration PASS binds here) | `9b6a0c38edbdecee202c33fe610c7c4475cf7cfc`; verdict `docs/track-b/evidence/cp-26-ci/integration.md`, SHA-256 `8ea68c51f5691faa078612a90a76330ac44e013fb00d21caf820940eb0dce963` |
| Evidence tip / `evidence/cp-26-ci` (pushed) | `644ac1a98292d573b929e58a65de03907b3aa7fa` |
| Squash landing / `land/cp-26-ci` | `e4a02df93f329649c628bc3819fd2cec7b73e212`, single parent `2a9e4fd`, tree `f9045e740296c279fa7dfab41a7b80272ffcc087`, equal to the evidence tip's |

## Why

- **The rich-admin stress test failed once in six GitHub runs.** At `2a9e4fd`, a docs-only commit,
  attempt 1 of workflow run 39525927648 found a busy owner no longer running after the admin job.
  Attempt 2 passed.
- **The runner is the cause.** GitHub's 4-vCPU runner has to host three CPU-bound owners and an
  admin job, with their supervisors and watchdogs. The two earlier failure modes were already fixed
  in CP-26's repair rounds.
- **The ledger pin.** CP-26's harness pins `docs/track-b/exposure-ledger.md`, so one added sentence
  turned `main` red at `2abd63b`. §24.2 and §24.9 need the ledger to grow.
- **The Owner chose a separate round with a `stress` marker** on 2026-10-21: "(א), עם הסימון stress.
  עכשיו."

## What changed

- **The `stress` marker** covers 15 test functions (16 cases) in `test_cp26_monitor.py`,
  `test_cp26_supervision.py` and `test_cp26_ledger_liveness.py`. They are listed with reasons in
  `docs/track-b/evidence/cp-26-ci/test-contract.md`.
  - `tests/conftest.py` registers the marker. It skips the marked tests only when `CI=true` and
    `RUN_STRESS` is not `1`, and prints the reason.
  - No test body or assertion changed.
  - `pytest -m stress` runs exactly these tests. The Orchestrator runs them in every local receipt.
- **The frozen ledger.** `docs/track-b/evidence/cp-26/exposure-ledger-frozen.md` is byte-identical to
  `61658c7:docs/track-b/exposure-ledger.md` and equals the unchanged harness pin.
  - The two identity tests read the frozen copy.
  - `tests/test_cp26_exposure_ledger.py` requires the live ledger to keep every CP-26 row, verbatim
    and in order. Rows may be added after them.

## The return and its receipt

- **The Lead returned PASS** in about 1.5 of the 3 hours. A fresh Integration Critic passed all six
  items from a clean detached checkout.
- **The Orchestrator's receipt:**
  - `gauntlet.py return` reports 0 problems;
  - the delta is the verdict only;
  - the packaged brief and the frozen ledger match by hash;
  - the forbidden-path diff is empty, and only the 15 decorators were added to existing test files;
  - on a history-free copy of the landed tree with `CI=true` and Python 3.12, the workflow's seven
    steps are green: 2,190 passed and 32 skipped, 16 of them the stress cases with their reason;
  - without `CI`, the 16 stress cases pass;
  - a synthetic row appended to the live ledger passes the ledger and identity tests, and an altered
    CP-26 row fails `test_live_exposure_ledger_preserves_frozen_cp26_rows`.
- **GitHub:** on the temporary branch `ci/cp-26-ci-land-check`, workflow run 40111714100 passed
  every step, with 2,190 passed and 32 skipped. Then `main` and both tags were pushed, and the branch
  was deleted.

## The LAND

The Orchestrator executed the LAND on the Owner's explicit instruction of 2026-10-24, sent from his
phone: "אתה יכול לבצע בעצמך את כל השלבים? אם כן, אני מאשר."

- **Locally:** the squash, the tree check, the commit and both tags.
- **On GitHub:** the temporary-branch check, the push of `main`, `land/cp-26-ci` and
  `evidence/cp-26-ci`, and the deletion of the temporary branch.

## Disclosure

**GitHub no longer runs CP-26's supervision stress tests.** They guard CP-26's operational
supervision code, which no later stage runs. They stay in the suite, and every local receipt runs
them, including the 4-vCPU emulation when timing matters.

## Reclamation

- **`gauntlet.py reclaim cp-26-ci --disposition land`:**
  - a verified bundle, `.local/artifacts/cp-26-ci-reclaim-20261024/gauntlet-cp-26-ci.bundle`;
  - a ref snapshot;
  - the worktree removed;
  - the branch deleted (it was `644ac1a`).
- **Both tags are on GitHub,** so nothing of this round is local-only.
- **No live citation** needed repointing.
