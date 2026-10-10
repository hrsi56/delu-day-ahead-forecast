# CP-24 work-availability maintenance — 2026-10-10

The Owner requested that CP-24's continuation brief and code also remove calendar blocking
and the associated requirement for an Owner resumption message. This is a bounded maintenance
edit, not an S1/S2 decision, a cap raise or a new research attempt.

The standing authority is `AGENTS.md` § Work availability at main commit
`7ff6a50cb54ad34a7f0e52981e18f990fa0323bb`. It supersedes the scheduling clauses in the original
issued brief and the candidate's v21-r11 anchor. Their historical bytes and hashes stay intact.
The packaged continuation explicitly applies that override and records the changed main state.

## Changes

- `scripts/cp24_ddnn2.py`: remove admission and running-job calendar stops. Keep signals,
  resource limits, cumulative accounting, atomic completion markers and the legacy CLI option.
- `src/cp24/budget.py`: remove the obsolete calendar-window helper.
- `src/cp24/report.py` and `reports/ddnn2/report.md`: replace the unconditional calendar-check
  claim with the current work-availability and resource-accounting rule.
- `tests/cp24/test_work_availability.py`: exercise actual child processes across the former
  boundary and at formerly restricted times; verify admission and live resource-cap stops.
- `docs/track-b/evidence/cp-24/continuation-brief.md`: package the updated continuation;
  the canonical local copy and launch envelope carry exactly the same brief.
- `src/cp24/finalise.py`: include the packaged continuation in generated manifests.
- `reports/ddnn2/artifact-manifest.json`: bind the updated candidate files, including the tests,
  continuation and this record. Original bytes remain at `d637590`.
- This record: preserve authorization, scope and the candidate handoff.

The three updated local operating copies are `.local/artifacts/cp-24/continuation-brief.md`,
`.local/artifacts/cp-24-orchestrator/continuation-envelope.md`, and
`.local/artifacts/cp-24-orchestrator/orchestrator-state.md`. The first two carry the same
continuation; the third records the supersession of earlier calendar notes.

## Validation

20 tests passed: the new CP-24 work-availability tests, existing saved-evidence tests and
base-tree tests. The tests use synthetic resource ledgers under `.local/tmp/cp24-availability/`;
they never update the run's real ledger. Manifest and generated-report checks pass without
changing stored scores or predictions.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /Users/djourno/Downloads/PJM/.venv/bin/python -m pytest -q tests/cp24/test_work_availability.py tests/cp24/test_saved_evidence.py tests/cp24/test_base_tree.py --basetemp=/Users/djourno/Downloads/PJM/.local/tmp/cp24-availability/pytest
```

## Handoff

The Owner explicitly authorized committing these changes on `gauntlet/cp-24` so the next
agent receives the updated brief and code. This local maintenance commit advances the branch
from `d637590`; the next Lead retains it in the candidate for the fresh Integration review. No claim of an Integration PASS
is made here. No main file, original issued brief, anchor, existing Critic snapshot, research
protocol, prediction, score, active ledger or tag is changed by this maintenance.
The task does not start or resume the research run. No branch, worktree or tag was created.

Candidate commit message: `Remove CP-24 calendar gates and continuation-message requirement`.
