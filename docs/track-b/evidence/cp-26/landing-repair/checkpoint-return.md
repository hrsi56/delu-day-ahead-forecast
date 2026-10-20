# Track B Checkpoint Return — CP-26 (landing repair)

## Status
PASS

## Identity
- Repository: `/Users/djourno/Downloads/PJM` (origin `hrsi56/delu-day-ahead-forecast`). Checkpoint CP-26, landing repair of its completed candidate, under the Orchestrator's brief of 2026-10-19 (`docs/track-b/evidence/cp-26/landing-repair-brief.md`, SHA-256 `27d3e1afbdcc5f02b88b27f59ed4935ac8bc99918ea8c58124e0cdbb3bd89e3d`).
- Ratified anchor: `capstone_v21.md` v21-r17, §24.7, SHA-256 `3124451da84c3cd99fae728c371207aace6ae537474f7769d0ff6333ee53e4fc`, unchanged by this repair.
- final_candidate_sha: `04f00eac5506c550ed4c775b84dc65a41f86c007`   (every bar binds here)
- evidence_tip_sha: the commit that adds this file; a file cannot contain its own commit SHA, so the terminal message states it, with the output of `git diff --name-only 04f00eac5506c550ed4c775b84dc65a41f86c007..<evidence_tip_sha>`. That delta adds or changes only paths under `docs/track-b/evidence/cp-26/`.
- Earlier bindings kept: the scientific Integration PASS binds `6f57febe3659b1f902c17f3db31ba41e41136178` (evidence `252725e0431826b6d32f1fc8200cfa3baf3750f6`), and the r17 PASS binds `f014e5b2f09dc7defa103b3c4ec5796d199c262d`. The prior evidence tip was `d8f912ad9be0867f11e4b634c2f482792ea5e951`.

## Repository state
- Branch `gauntlet/cp-26`, in the existing Lead worktree `.local/worktrees/cp-26/lead`. Tracked tree clean. These untracked outputs from the completed run stay untracked and unchanged:
  - `reports/rebaseline/cold-rerun-2026-10-15/diagnostics/`, `inference/`, `presentation-v21-r16/report.json`;
  - also present, though the brief did not list them: `report.json` and `scores/hourly.parquet` under the same folder, and `learning-ledger.json` and `replay-state.json` under `reports/rebaseline/continuation-v21-r14-accounting-3/`.
- `main` = `origin/main` = `647d6eb81b2cf6e0cfaf4152f659d689ff973578`, untouched, nothing staged on it; nothing pushed; no tag created.
- Commits added to `gauntlet/cp-26`, the only branch written:
  - `1c59c24`: package the brief;
  - `7fbbff7`: preserve the r17 verdict as `gfs-v21-r17/integration-r17-PASS.md`, byte-identical, before the canonical `integration.md` was replaced;
  - `04f00ea`: the repair, the final candidate;
  - the evidence commit.
- Worktrees created and removed:
  - Lead runs: three temporary worktrees (curated at the baseline, curated at the candidate, full at the candidate), each removed after its run.
  - `critic-1`: opened by `critic-open`; its Critic was stopped by a usage limit before any verdict, and its worktree was removed.
  - `critic-2`: the Integration Critic, closed by `critic-close`.
  - `critic-curated`: the Lead-built curated landing tree for both Critics, rebuilt fresh for `critic-2`, then removed.
- Scratch repositories, outside the project repository, under `.local/tmp/cp-26-landing-repair/`, all removed: the CI simulations (`baseline-scratch-1`, `candidate-scratch-1`, `critic-ci-sim`) and the two bytecode experiments.
- `critic-1` stays open in `.local/artifacts/cp-26/critic-open.json`, because `critic-close` needs a verdict.
- No branch or tag created.

## Complete checklist with direct evidence
| # | Checklist item | Status | Direct evidence |
|---|---|---|---|
| §24.7 | All 111 clauses, already PASSed (scientific PASS at `6f57feb`, r17 PASS at `f014e5b`), unchanged | PASS | §24.7 section SHA-256 `423527d9…` identical at `6f57feb`, `f014e5b`, `d8f912a` and `04f00ea`. The anchor is byte-identical from `d8f912a` to `04f00ea`. The repair changes no scientific output (item 4). |
| 1 | The five tests pass for a correct reason; each repair stated | PASS | See *Repairs* below. No test is skipped, deleted or loosened, and no skip or xfail marker was added. Verdict rows 1.1–1.9. |
| 2 | Repair outside `tests/` only if a guard is wrong under r17 | PASS (none) | `git diff d8f912a 04f00ea -- src scripts` is empty. The live guards are right to refuse under r17: they gate compute, and r17 authorizes none. Changing them would also break the run's recorded code identity. |
| 3 | Suite green on the curated landing tree and on the full candidate tree | PASS | Curated tree, the brief's procedure: `2213 passed, 8 skipped`. Full candidate tree: `2213 passed, 8 skipped`. CI's view with no history: `2205 passed, 16 skipped`, and CI's later steps (CQR fixture, `verify_release.py`, WASM equivalence, publication guard) all pass. The Critic reproduced all three counts. |
| 4 | `git diff --stat 6f57feb <new candidate> -- reports/` empty | PASS | Empty. `data/`, `src/`, `pyproject.toml`, `uv.lock`, the anchors and amendment records, `AGENTS.md`, the role files and the exposure ledger are unchanged from `d8f912a`. |
| 5 | One fresh focused Integration Critic from a clean detached checkout; reruns the curated suite | PASS | `docs/track-b/evidence/cp-26/integration.md` (critic-2, SHA-256 `240378b7…d36f`), binding `04f00eac5506c550ed4c775b84dc65a41f86c007`. |
| O1 | No test depends on `gauntlet/cp-26` history, an excluded file or the untracked outputs | PASS | A one-commit repository with no tag, in which no candidate commit resolves, ran green. None of its 16 skips is a CP-26 test; all belong to earlier checkpoints' shallow-clone, missing-tag or anchor-bound skip patterns. The Critic's static audit agrees. |
| O2 | Curated tree hash and file count | PASS | Candidate's curated landing tree: `git write-tree` = `c4e3b0ba914bba33b4d2f27e635705df55a3ad42`, 2,397 files; 846 curated paths of 10,265 changed; 44,801,005 bytes. The CI simulation's one-commit tree has the same hash. The LAND tree at the evidence tip adds only this commit's evidence files; the terminal message gives its hash and count. |

## Repairs
All are in `tests/`, plus new evidence files.
- `test_cp26_ledger_liveness.py`, two tests (`test_three_jobs_keep_fresh_supervision_…` and `test_rich_closed_jobs_three_busy_owners_accept_fourth_admin_…`).
  - Type: **stale expectation.**
  - The supervision policy is r15's calibration, 14 / 8 / 0.2 / 3 s, replacing r14's 10 / 2 / 0.2 / 0.5 s.
  - Authority: the r15 notice; `calibration-v21-r15.json` `policy_tested`; and `authority-v21-r16.json` `limits_preserved`. The tests assert the literal values and cross-check both records.
- `test_cp26_repair_contract.py::test_anchor_commit_and_landed_base_are_distinct_and_explicit`.
  - Type: **stale expectation and history.**
  - r16 (`8070238`) made `4766a61` the anchor commit and kept r14's `332baeb` as the scientific anchor commit.
  - It now reads recorded identities in place of `git show <commit>:<path>`: `authority-v21-r16.json`, the r16-to-r17 amendment record (which names the r16 anchor bytes `27bdc604…`), `active-documents.json`, CP-25's and CP-15's manifests, and the harness log's landed-code map (146 files).
- `test_cp26_search.py::test_search_lineage_changes_when_context_adapter_changes`.
  - Type: **fixture.**
  - Since r16, `search_identity` reads the committed runtime-lineage record, so the fixture now commits a synthetic one.
- `test_cp26_r15.py::test_r15_authority_does_not_relabel_scientific_plan_or_parity`.
  - Type: **r17 and history.**
  - The live guards demand the r16 anchor bytes and branch commits, so they refuse under r17.
  - The test now binds the same identities through committed records: protocol identity, inputs, input fingerprint (recomputed from the manifest's inputs and the recorded landed code), the k13 plan identity, and parity's 96 checks and reference custody. The records are the execution manifest, the r15 admission, the r16 checks, the runtime lineage and `parity.json`.
- Three more tests failed without history, which CI's depth-1 checkout lacks:
  - `test_original_documents_and_sections_1_through_23_stay_historical` now reads `active-documents.json` plus a recorded §§1–23 SHA-256.
  - `test_original_numeric_functions_are_unchanged_by_r15` now parses the recorded `landing-repair/scientific-base-1e7eb02/` copies, bound by SHA-256, Git blob id and the runtime lineage.
  - `test_real_references_are_committed_and_internally_bitwise_consistent` now reads the blob custody that the parity gate recorded.

## Integration verdict
- Path: `docs/track-b/evidence/cp-26/integration.md`   Result: PASS
- Candidate SHA it binds: `04f00eac5506c550ed4c775b84dc65a41f86c007`
- The r17 verdict that this file replaced is kept byte-identical at `docs/track-b/evidence/cp-26/gfs-v21-r17/integration-r17-PASS.md`.

## Reproduction
- `docs/track-b/evidence/cp-26/landing-repair/ci_check.py --mode worktree|scratch|full --candidate <sha> --out <dir>`, run under `scripts/cp26_rebaseline.py monitor --workers 4`.
  - It uses Python 3.12 and runs offline.
  - It drops CP-run variables, and points `CP26_PROJECT_ROOT` at a missing path.
- Per-run records are in `landing-repair/verification.json`. The Critic's exact commands are in the verdict.

## Files changed
- `tests/test_cp26_ledger_liveness.py`, `tests/test_cp26_parity.py`, `tests/test_cp26_r15.py`, `tests/test_cp26_repair_contract.py`, `tests/test_cp26_search.py`: the repairs above.
- `docs/track-b/evidence/cp-26/landing-repair-brief.md`: the issued brief.
- `docs/track-b/evidence/cp-26/gfs-v21-r17/integration-r17-PASS.md`: the r17 verdict, preserved.
- `docs/track-b/evidence/cp-26/landing-repair/scientific-base-1e7eb02/` (four modules, `manifest.json`): recorded sources for the AST test.
- Evidence commit:
  - `integration.md`: this review's verdict;
  - `landing-repair/critic-assignment.md`, `verification.json`, `ci_check.py`, `cold_experiment.py`, `ci_bytecode_experiment.py`: the Lead's assignment, records and run tools;
  - `landing-repair/checkpoint-return.md`: this return.

## Elapsed
- About 3.5 active hours against the 4-hour timebox. A session usage limit stopped work from about 02:50 to 12:10 IDT; that time is not counted.
- Test time charged to the CP-26 ledger, without a reset: 27,374 machine-seconds (7.60 h) across 20 monitored jobs, bringing the cumulative total from 238.11 to 245.72 of 500 h.
  - Lead: 2.84 h, including two experiments.
  - Stopped Critic: 2.49 h.
  - Final Critic: 2.27 h.
- The first Lead run declared one worker. Every later run declared four, because `test_cp26_ledger_liveness.py` runs up to four processes.

## Open risk or exact owner action
- **LAND is the Owner's.** The curated tree must be built from the evidence tip, not from `04f00ea`. The commit message prepared in `.local/artifacts/cp-26-landing/land-commit-message.txt` still cites the old counts (839 files, 44.6 MB) and the old evidence tip. The terminal message gives the new values.
- **Stress tests on GitHub runners (risk).**
  - The four-process liveness stress tests have never run on a GitHub runner.
  - `test_rich_closed_jobs_…_fourth_admin_…` gives its admin job 15 s; locally that job takes 8.3–9.1 s.
  - Run alone in a venv with no compiled bytecode while `PYTHONDONTWRITEBYTECODE=1` (this machine's shell), it times out; with bytecode allowed, as on CI, it passed every run.
  - A slower runner could still make it flaky.
- **Guards no longer exercised on the real tree (note).**
  - The live CP-26 identity guards refuse on the r17 tree by design, and a landed `main` without branch history refuses too.
  - No test exercises them on the real tree any more; the repaired tests rebuild the same identities from records.
  - Any later reader of the stored outputs, such as r17's post-results supplement, needs a read-only path. `load_scores` and the gates refuse.
  - The test edits also move CP-26's `code_identity` away from the value recorded in the score manifests. That identity includes `tests/test_cp26*.py`; it is otherwise unchanged.

## Landing report
- Proposed disposition: LAND. The candidate is the completed CP-26 with its five failing tests repaired and every scientific output unchanged, under a fresh Integration PASS.
- Evidence tip to preserve: given in the terminal message, for `git tag evidence/cp-26 <evidence_tip_sha>`.
- Live documents citing this branch, to repoint on reclamation: `progress.md:111`. Locked: `capstone_v21.md:4368`, the §24.7 protocol text, which needs no repointing.
- Proposed commit message: given in the terminal message, with the evidence-tip counts.

## Post-return reads
After the Integration verdict, `gauntlet.py citations cp-26` printed one line of `progress.md` from `main`. It was used only for the landing report.
