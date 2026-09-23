# Repository consolidation — 2026-09-16

The owner explicitly authorized resolving pending work, edits, commits, deletions and
consolidation to leave only main. This is task-scoped authority, not a permanent rule change.

## Result

- Sole branch and checkout: `main` at `/Users/djourno/Downloads/PJM`.
- Retired branches: `codex/orchestration-pending` (`4039ce24150b36ea233b043061e68eb2be78cbbe`)
  and `codex/v20-plan-corrections` (`3618658ec16d57795a69c68ccb4cbdab926d73a5`).
  Both tips are verified ancestors of the retained `evidence/cp-15` tag.
- Retired temporary worktrees: `PJM-main-landing` and `PJM-orchestrator-v20-review`.
- No scientific output, model, CP-15 plan/brief, product criterion or verdict changed.
  Product feasibility stays NOT_DEMONSTRATED; no model promotion or next experiment.
- The owner's 30-question Q&A is preserved byte-for-byte. The superseded v20-r1 draft and
  stale 32-question Q&A are preserved in the Git-ignored `.local/artifacts/` directory inside the project, not adopted.

## Pending work resolved

| Files | Resolution |
|---|---|
| README, site and their two generators | Preserve pending documentation work; replace stale planned-CP-15 claims with the completed experiment and unmet product criteria. |
| pages_build.json | Regenerated site build record. |
| orchestrator-role.md, program-stage-sequence.md | Consolidate previously authorized v21 routing updates; no new checkpoint bar. |
| capstone_v20.md | Consolidate previously authorized capture-scope clarification; historical engineering methods unchanged. |
| anchors/cp-10-capstone_v20.md, test_26_cp10_evidence.py | Preserve the exact original CP-10 anchor and check it against the unchanged lineage hash. |
| שאלות תשובות.docx | Keep the owner's exact 30-question copy. |
| Research memo, context-recovery report, historical handover and v20 review | Preserve decision history; mark retired checkout paths and superseded proposals as historical. |
| progress.md, CP-15 landing record | Record one-checkout state and resolve prior pending-work routing. |

The active v21-r1 plan, AGENTS and CP-15 briefs already match main; no duplicate change was needed.

## Verification and recovery

- 84 targeted surface/provenance tests passed; the optional marimo-export control initially
  skipped because its executable was outside PATH, then passed separately with the existing
  environment on PATH: 85 selected tests passed in total.
- README and static site regenerated; whitespace check passed.
- Q&A SHA256 unchanged from the primary pre-cleanup copy; XML has 30 numbered questions.
- CP-10 archived plan exactly matches its original candidate; CP-15 plan/briefs exactly
  match the reviewed evidence tip. No experiment source/results/model changes.
- Both pending checkouts were backed up with per-file hashes before cleanup.

Local recovery packet: `/Users/djourno/Downloads/PJM/.local/artifacts/PJM-consolidation-backup-2026-09-16/`.
It includes the original pending files, binary diffs, manifest, superseded v20-r1 draft,
full consolidation diff and per-file accounting. Backups are inside the project under `.local/artifacts/`, ignored by Git.
