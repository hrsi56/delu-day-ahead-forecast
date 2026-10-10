# CP-24 — the simulated LAND (continuation condition 1)

The command is `python -m cp24.landsim` at the final candidate `7949a98f80c81c5a789dd69c213da16c811d345c`. It ran under the CP-24 monitor as jobs
`landsim2-candidate`, `landsim2-main` and `landsim2-main-edits`. The module reads the project repository only.
It builds the squash tree in a fresh scratch repository with one commit, no history and no tags, as CI's shallow
checkout sees it, and runs the steps of `.github/workflows/tests.yml` there. Records and step logs are in
`.local/artifacts/cp-24/landsim2/<run>/`.

| Run | `main` | Squash tree | Later edits | Suite | Other CI steps | Green |
|---|---|---|---|---|---|---|
| candidate | `522d7ea722b5` | `62ad6015e5dd` | none | 1439 passed, 12 skipped | all exit 0 | True |
| main | `7ff6a50cb54a` | `c7758f1cc3d9` | none | 1479 passed, 13 skipped | all exit 0 | True |
| main-edits | `7ff6a50cb54a` | `c7758f1cc3d9` | 8 living files | 3 failed, 1475 passed, 14 skipped | all exit 0 | False |

- **`candidate`** builds the candidate's own tree on its base `522d7ea`, the branch as CI would test it.
- **`main`** is the Owner's LAND, `git merge --squash gauntlet/cp-24` onto today's `main` (`7ff6a50`).
  - The candidate only adds files under CP-24's paths: 118 additions.
  - `main`'s 31 changes since the base touch none of them.
  - So the squash tree is `main` plus the candidate's CP-24 paths.
- **`main-edits`** appends one line to each of these living files after the LAND: `progress.md`, `docs/track-b/cp-0-defects.md`, `AGENTS.md`, `capstone_v21.md`, `README.md`, `docs/index.html`, `scripts/mlflow_export.py`, `tests/cp23/torch-reference/uv.lock`.

**What failed in `main-edits`, and why.** The run had three failures. None of them is a repaired CP-24 test:
- `tests/cp23/test_reference_record.py::test_the_reference_passed_for_the_current_ddnn_code_with_nothing_skipped`
- `tests/cp23/test_saved_evidence.py::test_byte_exact_storage_of_every_manifested_file`
- `tests/cp24/test_reference_record.py::test_the_reference_passed_for_the_current_model_code_with_nothing_skipped`

All three bind the CP-23 test-only lock or `scripts/mlflow_export.py`:
- CP-23's own `test_reference_record` and `test_saved_evidence` bind those files on `main` today.
- `tests/cp24/test_reference_record.py` is part of attempt 1's frozen implementation, so it was left unchanged.
- See `reports/ddnn2/defects-and-repairs.md`, item 12.

A later change to either file must amend CP-23's tests in any case, by the same `AMENDED_BY_…` pattern the Owner
used for CP-21 and CP-23 on 2026-10-10.

Every other CP-24 test stays green with all eight edits, including `progress.md`, `capstone_v21.md`, `AGENTS.md`,
`README.md` and `docs/index.html`. `test_draft_export` skips its fresh-build comparison, with the reason, once
`scripts/mlflow_export.py` changes.

**Earlier runs.**
- Before the repair, the same simulation of `9667fb4` onto `7ff6a50` failed `tests/cp24/test_base_tree.py`, with
  no edits at all: 1 failed, 1474 passed, 13 skipped.
- The superseded candidate `7ea9bdd` gave the same three results as this one (`.local/artifacts/cp-24/landsim/`).

## Correction to `reports/ddnn2/defects-and-repairs.md` item 11

That item, as committed at the final candidate, says the squash tree is green "on `main` as it stands, and again
after simulated later edits to the living files". The second half is wrong.

- The run with later edits is **not** green: 3 failed, 1,475 passed, 14 skipped. All three failures bind CP-23's
  test-only lock or `scripts/mlflow_export.py`, as set out above.
- What holds is narrower: no repaired CP-24 test fails under the edits.

The Integration verdict (observation O1) found this. The correction is recorded here and in the checkpoint return,
not in a new candidate.

## Records

### candidate

```json
{
 "schema": "cp24-land-simulation-v1",
 "main": "522d7ea722b5d215d827d7aed9c56b7a9dec066e",
 "candidate": "7949a98f80c81c5a789dd69c213da16c811d345c",
 "preconditions": {
  "candidate_changes": 118,
  "candidate_only_adds_under_cp24_paths": true,
  "main_changes_since_base": 0,
  "main_touches_no_cp24_path": true,
  "base_is_an_ancestor_of_main": true
 },
 "later_edits": null,
 "scratch_tree": "62ad6015e5ddccdd6e3a36b9d66e80aa6880602a",
 "cp24_files": 118,
 "steps": [
  {
   "step": "payload",
   "exit_code": 0,
   "seconds": 42.0,
   "summary": "wrote /Users/djourno/Downloads/PJM/.local/artifacts/cp-24/landsim2/candidate/tree/reports/cp3b/payload.json",
   "failed": [],
   "tracked_changes_after": 0
  },
  {
   "step": "suite",
   "exit_code": 0,
   "seconds": 230.8,
   "summary": "1439 passed, 12 skipped in 229.91s (0:03:49)",
   "failed": [],
   "tracked_changes_after": 0
  },
  {
   "step": "cqr",
   "exit_code": 0,
   "seconds": 0.5,
   "summary": "8 passed in 0.02s",
   "failed": [],
   "tracked_changes_after": 0
  },
  {
   "step": "verify-release",
   "exit_code": 0,
   "seconds": 0.7,
   "summary": "PASS \u2014 every bound claim agrees on every surface; the static page fetches nothing; the headline, names and statuses agree across surfaces",
   "failed": [],
   "tracked_changes_after": 0
  },
  {
   "step": "wasm",
   "exit_code": 0,
   "seconds": 2.3,
   "summary": "15 passed in 1.72s",
   "failed": [],
   "tracked_changes_after": 0
  },
  {
   "step": "publication-guard",
   "exit_code": 0,
   "seconds": 0.0,
   "summary": "publication-guard: the tree carries no placeholder and a final build record",
   "failed": [],
   "tracked_changes_after": 0
  }
 ],
 "green": true,
 "written_utc": "2026-10-10T19:53:40Z"
}
```

### main

```json
{
 "schema": "cp24-land-simulation-v1",
 "main": "7ff6a50cb54ad34a7f0e52981e18f990fa0323bb",
 "candidate": "7949a98f80c81c5a789dd69c213da16c811d345c",
 "preconditions": {
  "candidate_changes": 118,
  "candidate_only_adds_under_cp24_paths": true,
  "main_changes_since_base": 31,
  "main_touches_no_cp24_path": true,
  "base_is_an_ancestor_of_main": true
 },
 "later_edits": null,
 "scratch_tree": "c7758f1cc3d9d88eea78809147283cd76b40446b",
 "cp24_files": 118,
 "steps": [
  {
   "step": "payload",
   "exit_code": 0,
   "seconds": 41.8,
   "summary": "wrote /Users/djourno/Downloads/PJM/.local/artifacts/cp-24/landsim2/main/tree/reports/cp3b/payload.json",
   "failed": [],
   "tracked_changes_after": 0
  },
  {
   "step": "suite",
   "exit_code": 0,
   "seconds": 234.1,
   "summary": "1479 passed, 13 skipped in 233.12s (0:03:53)",
   "failed": [],
   "tracked_changes_after": 0
  },
  {
   "step": "cqr",
   "exit_code": 0,
   "seconds": 0.5,
   "summary": "8 passed in 0.02s",
   "failed": [],
   "tracked_changes_after": 0
  },
  {
   "step": "verify-release",
   "exit_code": 0,
   "seconds": 0.9,
   "summary": "PASS \u2014 every bound claim agrees on every surface; the static page fetches nothing; the headline, names and statuses agree across surfaces",
   "failed": [],
   "tracked_changes_after": 0
  },
  {
   "step": "wasm",
   "exit_code": 0,
   "seconds": 2.4,
   "summary": "15 passed in 1.81s",
   "failed": [],
   "tracked_changes_after": 0
  },
  {
   "step": "publication-guard",
   "exit_code": 0,
   "seconds": 0.0,
   "summary": "publication-guard: the tree carries no placeholder and a final build record",
   "failed": [],
   "tracked_changes_after": 0
  }
 ],
 "green": true,
 "written_utc": "2026-10-10T19:53:44Z"
}
```

### main-edits

```json
{
 "schema": "cp24-land-simulation-v1",
 "main": "7ff6a50cb54ad34a7f0e52981e18f990fa0323bb",
 "candidate": "7949a98f80c81c5a789dd69c213da16c811d345c",
 "preconditions": {
  "candidate_changes": 118,
  "candidate_only_adds_under_cp24_paths": true,
  "main_changes_since_base": 31,
  "main_touches_no_cp24_path": true,
  "base_is_an_ancestor_of_main": true
 },
 "later_edits": [
  "progress.md",
  "docs/track-b/cp-0-defects.md",
  "AGENTS.md",
  "capstone_v21.md",
  "README.md",
  "docs/index.html",
  "scripts/mlflow_export.py",
  "tests/cp23/torch-reference/uv.lock"
 ],
 "scratch_tree": "c7758f1cc3d9d88eea78809147283cd76b40446b",
 "cp24_files": 118,
 "steps": [
  {
   "step": "payload",
   "exit_code": 0,
   "seconds": 41.6,
   "summary": "wrote /Users/djourno/Downloads/PJM/.local/artifacts/cp-24/landsim2/main-edits/tree/reports/cp3b/payload.json",
   "failed": [],
   "tracked_changes_after": 0
  },
  {
   "step": "suite",
   "exit_code": 1,
   "seconds": 233.7,
   "summary": "3 failed, 1475 passed, 14 skipped in 232.70s (0:03:52)",
   "failed": [
    "FAILED tests/cp23/test_reference_record.py::test_the_reference_passed_for_the_current_ddnn_code_with_nothing_skipped",
    "FAILED tests/cp23/test_saved_evidence.py::test_byte_exact_storage_of_every_manifested_file",
    "FAILED tests/cp24/test_reference_record.py::test_the_reference_passed_for_the_current_model_code_with_nothing_skipped"
   ],
   "tracked_changes_after": 0
  },
  {
   "step": "cqr",
   "exit_code": 0,
   "seconds": 0.5,
   "summary": "8 passed in 0.02s",
   "failed": [],
   "tracked_changes_after": 0
  },
  {
   "step": "verify-release",
   "exit_code": 0,
   "seconds": 0.9,
   "summary": "PASS \u2014 every bound claim agrees on every surface; the static page fetches nothing; the headline, names and statuses agree across surfaces",
   "failed": [],
   "tracked_changes_after": 0
  },
  {
   "step": "wasm",
   "exit_code": 0,
   "seconds": 2.3,
   "summary": "15 passed in 1.77s",
   "failed": [],
   "tracked_changes_after": 0
  },
  {
   "step": "publication-guard",
   "exit_code": 0,
   "seconds": 0.0,
   "summary": "publication-guard: the tree carries no placeholder and a final build record",
   "failed": [],
   "tracked_changes_after": 0
  }
 ],
 "green": false,
 "written_utc": "2026-10-10T19:53:43Z"
}
```
