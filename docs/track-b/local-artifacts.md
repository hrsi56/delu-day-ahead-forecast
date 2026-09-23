# Project-local artifact map — 2026-09-16

The owner requires all project-created working material to stay inside the project.
Five sibling Downloads folders were removed. Required source, scientific evidence and decisions
remain committed; recovery copies and handoff packaging are retained locally and ignored by Git.

## Retained local material

- `.local/artifacts/PJM-CP1-v68-handoff/`: Historical CP-1 handoff and diffs.
- `.local/artifacts/PJM-consolidation-backup-2026-09-16/`: Original pending files, superseded v20-r1 draft, prior Q&A copy and consolidation recovery records.
- `.local/artifacts/PJM-cp10-cleanup-2026-09-16/`: CP-10 branch-retirement checks.
- `.local/artifacts/PJM-cp15-landing-record-2026-09-16/`: Landing checks, original pending-file backups, diagnostic logs and reusable comparison caches.
- `.local/artifacts/PJM-cp15-r1-handoff/`: Original Engineering Lead terminal packet and full diffs.

The local `relocation-2026-09-16.json` records old/new paths, retained-file hashes, deleted
cache categories and byte accounting. Retained originals keep historical internal paths; apply
that mapping when following old absolute references. Current project documentation is repointed.

## Removed disposable material

Two retired Python environments, downloaded Hugging Face model cache, generated browser payload,
marimo/Python/pytest caches and temporary validation caches. The active `.venv`, source, pinned
dependency specifications, committed probe identities/results and scientific evidence are unchanged.
No model retraining or new engineering verdict is claimed.

Retained regular-file content: 286,327,196 bytes; removed file content: 2,105,180,117 bytes.
Filesystem allocated space can differ. Retained files were hash-verified after relocation.

## Future locations

- Temporary worktrees: `.local/worktrees/`.
- Scratch work: `.local/tmp/`.
- Handoffs/recovery records: `.local/artifacts/`.
- Required checkpoint evidence: committed `docs/track-b/evidence/` and `reports/` as before.

The `.local/` directory is excluded from Git. It is not an off-device backup, and it is not
the sole copy of required evidence. No outside folder should be created unless the owner
explicitly requests that location.
