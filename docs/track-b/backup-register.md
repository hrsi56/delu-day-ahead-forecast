# Off-device backup register

**An anchor in the Governance Lockdown's locked set** (`AGENTS.md`). It records every off-device
snapshot of this project: what it holds, where it is, which items exist only there, and how to
restore each item to its original place.

**Authority.** The Owner, 2026-10-20: "אתה מתכנן גיבוי במדויק וכותב לעוגנים קטע שמגדיר את זה
שגיבינו בתור עוגן, ככה שאם איי פעם נצטרך משהו מתוך מה שגיבינו תדע איפה זה בדיוק ואיך לשחזר
למקום הנכון. ואז אתה עושה גיבוי אל ״/Volumes/Samsung/delu-day-ahead-forecast״ (יש לך אישור
והשעיית נעילה לצורך זה)". Each later snapshot, or change to this file, needs the Owner's suspension.

## Why it exists

- **Git and GitHub hold the code and the landed evidence.** GitHub refuses any file over 100 MB, so
  one checkpoint's evidence (CP-26) is kept in a local-only tag.
- **Some outputs cost a retraining or a re-download to rebuild.** The Owner's rule, 2026-10-20:
  nothing is ever retrained or re-downloaded to check something.
- **The rule for what is copied:** only what GitHub cannot restore and the project still needs.
  Caches, environments, test temporaries and Git diffs are not copied.

## The drive and its layout

- **The drive:** the Owner's external drive, volume `Samsung`.
- **The folder:** `/Volumes/Samsung/delu-day-ahead-forecast/`.
- **Inside it,** one folder per snapshot, `snapshot-<date>/`, which holds:
  - `local/`, which mirrors the repository's `.local/`. The file `<snapshot>/local/<path>` restores
    to `/Users/djourno/Downloads/PJM/.local/<path>`. The folder is named without the dot so that
    Finder shows it;
  - `MANIFEST/`:
    - `files.tsv`: the repository path, bytes and SHA-256 of every file;
    - `SHA256SUMS`: the same digests, with paths relative to the snapshot folder;
    - `summary.json`;
    - the scripts that built, copied and checked the snapshot;
    - a `README.md`;
  - `README.md` at the top.
- **The check is `MANIFEST/verify_snapshot.py`.** It only reads: it re-reads every listed file and
  ends with `ALL OK`, or with the number of files that are missing or differ.
- **Snapshots are never overwritten.** A new snapshot gets a new dated folder.

## Snapshot 2026-10-21 — after CP-26's closure

- **Folder:** `/Volumes/Samsung/delu-day-ahead-forecast/snapshot-2026-10-21/`. The manifest also
  has a local copy, `.local/artifacts/backup-2026-10-21/`.
- **Contents:** 145,949 files, 41,290,703,209 bytes, with no symlinks and no hard links.
- **Manifest identities (SHA-256):**

  | File | SHA-256 |
  |---|---|
  | `MANIFEST/files.tsv` | `551b05e7e5329ca9fcfbd4c2421fbbee85ff5a1e6132c19c42ca74c106e68957` |
  | `MANIFEST/SHA256SUMS` | `e915436e5ad96702e2a6bab3770a2a2a8471cf34de058a1967593101cb3f2d22` |
  | `MANIFEST/summary.json` | `d3bfb6c5624130b0903f33d8a7b46dc71a610897a5a7a1a03df3c47caf03ea3e` |
  | `MANIFEST/make_manifest.py` | `70255bb10026b9493794a021fdbc9c0f123cbc143068dc90669ef9ff8cfc874a` |
  | `MANIFEST/verify_snapshot.py` | `47e6b7cf90e513b843b9755d881880bb3e1b5a8bca0ca79950ed95a59e43f0ee` |
  | `MANIFEST/copy_snapshot.py` | `357011f6566a2067fd2c5b6c02499261fd6dd7f5d3fd30cdfcd8837d3cc0ce81` |
- **The rule:** every file under `.local/artifacts/` and `.local/weather-admission/`, except:
  - `.local/artifacts/cp-26/continuation-v21-r14/`, the abandoned r14 run. Its committed outputs
    are in `evidence/cp-26`;
  - the Python environments `.local/artifacts/cp-20/wx-venv/` and `.local/weather-admission/venv/`;
  - test temporaries: folders named `pytest-tmp*` or `*-test-tmp`, and `__pycache__`;
  - Git diffs over 10 MB, which can be rebuilt from tags on GitHub or from the CP-26 bundle;
  - `.local/artifacts/cp-26/git-admission-2026-10-19/replay-state.json.gz`, a copy of a file that is
    in the bundle;
  - Finder's `.DS_Store` files.
- **Checked on the drive, 2026-10-21:**
  - `MANIFEST/verify_snapshot.py` re-read all 145,949 files from the drive: `ALL OK`;
  - the CP-26 bundle, read directly from the drive, passed `git bundle verify`;
  - fetched into a scratch clone of `main`, it gave `ca2033120288c6a396fec8c01404f0220523d695` with
    a clean `git fsck`.

### What it holds, and what each item is for

Paths are repository-relative. On the drive, `.local/` is `local/`.

| Item | Path | Size | Needed for | If both copies were lost |
|---|---|---:|---|---|
| **The CP-26 evidence bundle** | `.local/artifacts/cp-26-reclaim-20261020/gauntlet-cp-26.bundle` (SHA-256 `926bf751…72ef34fc`) | 0.56 GB | the full `evidence/cp-26` history: the stored forecast ledger that CP-28 and 4.7T read, the search results, the replay state, every repair round | CP-26 would have to be rerun with training (its ledger reached about 250 machine-hours) |
| **CP-26's stored analysis outputs** | `.local/artifacts/cp-26/cold-rerun-2026-10-15/r16/` (`final-analysis-inputs/`: 9.4 GB of bootstrap replicates, 20 GB of diagnostics, hourly scores, `report.json`; `presentation-inputs/`; the r16 documents and logs) | 32.3 GB | the retention §24.7 requires; any re-check of CP-26's report | recomputable from the ledger without training, at a heavy statistical cost |
| **CP-26's trained models and run state** | `.local/artifacts/cp-26/cold-rerun-2026-10-15/fits/`, `searches/`, `state/` | 1.8 GB | checking any CP-26 forecast without retraining | retraining |
| **CP-26's accounting** | `.local/artifacts/cp-26/ledger/`, `jobs/`, and the run folder's logs and briefs | 0.05 GB | the resource audit | none |
| **Two files of the abandoned run that are cited by hash** | `.local/artifacts/cp-26/continuation-v21-r14-accounting-3-untracked/` | 0.09 GB | the custody records that cite them | none |
| **Weather: CP-20's archive** | `.local/artifacts/cp-20/` (decoded grids, raw samples, ledger, logs) | 1.97 GB | rebuilding or auditing the GFS features | a re-download from NCAR and AWS |
| **Weather: CP-25's gap retrieval** | `.local/artifacts/cp-25/` (`weather/`, docs, ledger) | 0.42 GB | the same, for 2022-09-29 to 2023-03-24 | a re-download |
| **Weather: the admission samples** | `.local/weather-admission/` (`cache/`, `logs/`, `sources/`) | 1.70 GB | the GFS admission's evidence | a re-download |
| **Governance and earlier checkpoints' records** | everything else under `.local/artifacts/`: briefs, launch envelopes, Critic assignments, receipts, landing packets, publication reviews, earlier reclamation bundles | about 2.4 GB | committed documents cite them by path or hash | the citations could no longer be checked |

Per the CP-20 rights notice, decoded grids and raw samples are never redistributed. The drive is a
private copy.

### Items that exist only on the drive

The cleanup of 2026-10-21, approved by the Owner, deleted these locally. They now exist only in this
snapshot:

| Item | Snapshot path | Size | What still holds the same information locally |
|---|---|---:|---|
| CP-26's stored bootstrap outputs | `local/artifacts/cp-26/cold-rerun-2026-10-15/r16/final-analysis-inputs/reports/rebaseline/cold-rerun-2026-10-15/inference/` | 10.1 GB | `report.json`'s `inference_endpoints` (16,024 endpoints) and `inference-manifest.json`, which lists each file's hash |
| CP-26's stored diagnostics | `.../cold-rerun-2026-10-15/diagnostics/`, beside `inference/` | 21.8 GB | `report.json`'s `diagnostic_tables` and `diagnostics-manifest.json` |

CP-28, its no-training supplement and 4.7T read the summaries, which stay local. Copy these two
folders back from the drive only to rebuild CP-26's report from its stored inputs, or to audit the
inference. They never need recomputing.

**Deleted locally and in no snapshot,** because they can be rebuilt or are no longer needed (the
moves are listed in `.local/artifacts/backup-2026-10-21/cleanup-moves.tsv`):

- the abandoned r14 run's local outputs (`.local/artifacts/cp-26/continuation-v21-r14/`). Its
  committed outputs are in `evidence/cp-26`;
- test temporaries;
- ten Git diffs, which can be rebuilt from tags on GitHub or from the CP-26 bundle;
- the compressed replay-state copy;
- the local Space build `dist/`;
- `.local/tmp/`, except 176 files (about 100 MB) that committed records cite by hash. Those stay in
  place, are not in this snapshot, and go into the next one.

## How to restore

Nothing here writes to the drive. Set:

```bash
S=/Volumes/Samsung/delu-day-ahead-forecast/snapshot-2026-10-21
cd /Users/djourno/Downloads/PJM
```

- **Check the copy on the drive first** (read-only): `python3 "$S/MANIFEST/verify_snapshot.py"`.
- **One file or folder, back to its original path,** where `<path>` is the part after `.local/`.
  Never overwrite a newer file. Run it from inside `local/`, so that the path stays relative,
  because macOS's `openrsync` ignores the `/./` marker. Then check what came back:
  ```bash
  (cd "$S/local" && rsync -a --ignore-existing --relative "<path>" /Users/djourno/Downloads/PJM/.local/)
  grep -F "  local/<path>" "$S/MANIFEST/SHA256SUMS" | sed 's#  local/#  .local/#' | shasum -a 256 -c -
  ```
- **The whole snapshot:**
  ```bash
  (cd "$S/local" && rsync -a --ignore-existing . /Users/djourno/Downloads/PJM/.local/)
  cp -R "$S/MANIFEST" .local/tmp/manifest-2026-10-21
  python3 .local/tmp/manifest-2026-10-21/copy_snapshot.py verify /Users/djourno/Downloads/PJM
  ```
- **The `evidence/cp-26` tag.** The bundle needs `647d6eb`, which is in `main`'s history:
  ```bash
  git fetch "$S/local/artifacts/cp-26-reclaim-20261020/gauntlet-cp-26.bundle" refs/heads/gauntlet/cp-26
  git tag evidence/cp-26 FETCH_HEAD
  test "$(git rev-parse evidence/cp-26)" = ca2033120288c6a396fec8c01404f0220523d695 && echo OK
  ```
  While the tag exists locally, one file of the evidence can be read without restoring anything:
  `git show evidence/cp-26:<path>`.
- **Before trusting a restored item,** check it against `SHA256SUMS`, which the table above pins.

## Rules for later snapshots

- **When:** at each closure that leaves local-only evidence, or new outputs that would cost a
  retraining or a re-download.
- **How:** each snapshot gets a new dated folder, `snapshot-<date>/`, with its own `local/` and
  `MANIFEST/`, plus a new section in this register under the Owner's suspension. No script or
  agent writes to the drive.
- **Local deletion** comes only after a verified copy, and with the Owner's approval. Whatever is
  deleted locally is listed under "Items that exist only on the drive".
