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

## Added 2026-09-24: CP-20 weather material

Keep these. They are the only copies of the decoded weather and are expensive to rebuild.
Sizes and content are in the [CP-20 landing record](cp-20-landing-2026-09-24.md#retained-local-material).

- `.local/artifacts/cp-20/weather/runs/`: decoded GFS box grids for all 2,476 CP-20 runs.
  New features from the same five fields, leads and box need no download.
- `.local/artifacts/cp-20/weather/raw/`: retained original GRIB sample messages for 23 dates.
- `.local/artifacts/cp-20/`: extraction environment, cached HG component fits, ledger, logs,
  markers and Critic outputs.
- `.local/weather-admission/`: admission samples and recovery files.
- `.local/artifacts/cp20-landing-2026-09-24/`: landing recovery bundle and snapshots.

Per the CP-20 rights notice, decoded grids and raw samples are not redistributed.

## Future locations

- Temporary worktrees: `.local/worktrees/`.
- Scratch work: `.local/tmp/`.
- Handoffs/recovery records: `.local/artifacts/`.
- Required checkpoint evidence: committed `docs/track-b/evidence/` and `reports/` as before.

The `.local/` directory is excluded from Git. It is not an off-device backup, and it is not
the sole copy of required evidence. No outside folder should be created unless the owner
explicitly requests that location.
