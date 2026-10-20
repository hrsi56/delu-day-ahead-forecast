# CP-26 landing repair — Integration Critic assignment

Plan: capstone_v21.md
Section: ### 24.7 CP-26: the re-baseline on every development day (stage 6)

## What this review is

A **focused landing-repair review** of CP-26 at `capstone_v21.md` **v21-r17** (SHA-256
`3124451da84c3cd99fae728c371207aace6ae537474f7769d0ff6333ee53e4fc` at the candidate). §24.7's 111
clauses are already PASSed: the scientific Integration PASS binds
`6f57febe3659b1f902c17f3db31ba41e41136178`, and the r17 PASS binds
`f014e5b2f09dc7defa103b3c4ec5796d199c262d`. You do not re-review the science. Confirm only that this
candidate leaves §24.7, the anchor and every scientific output unchanged. Then judge the bar for this
candidate: the issued repair brief's five items, verbatim below.

The issued brief is committed at the candidate as `docs/track-b/evidence/cp-26/landing-repair-brief.md`
(SHA-256 `27d3e1afbdcc5f02b88b27f59ed4935ac8bc99918ea8c58124e0cdbb3bd89e3d`). Read it whole. Its bar, verbatim:

> 1. **The five tests above pass** for a correct reason, not by being skipped, deleted or loosened.
>    Each repair is stated:
>    - a stale expectation is updated to the authorized value, citing its authority (r15's
>      calibration, the r16 commits, r17);
>    - a history-dependent check reads recorded identities instead of the branch's Git history;
>    - a fixture includes what it needs.
> 2. **A repair outside `tests/` is allowed only if a guard is wrong under r17.** It is limited to
>    `src/cp26/` identity and guard code, never to a forecast, search, scoring, inference or
>    reporting path, and it is justified in the return.
> 3. **The full suite is green on the curated landing tree,** and also on the full candidate tree.
> 4. **Every scientific output is unchanged:** `git diff --stat 6f57feb <new candidate> -- reports/`
>    is empty.
> 5. **One fresh focused Integration Critic,** from a clean detached checkout of the new candidate,
>    checks items 1–4 and reruns the suite on the curated tree.

Its observable outcome adds: "**no test depends** on the `gauntlet/cp-26` commit history, on an
excluded file, or on the untracked output folders". Check that too.

## The artifact

- Candidate: `04f00eac5506c550ed4c775b84dc65a41f86c007` on `gauntlet/cp-26`. The prior evidence tip is
  `d8f912ad9be0867f11e4b634c2f482792ea5e951`; `main` is `647d6eb81b2cf6e0cfaf4152f659d689ff973578`.
- Everything this repair changed is `git diff d8f912ad9be0867f11e4b634c2f482792ea5e951 <candidate>`
  (three commits; their messages state each repair). Your clean checkout has the history to check it.
- The tests to judge. The five from the brief:
  - `tests/test_cp26_ledger_liveness.py::test_three_jobs_keep_fresh_supervision_with_full_future_history`
  - `tests/test_cp26_ledger_liveness.py::test_rich_closed_jobs_three_busy_owners_accept_fourth_admin_with_full_future_history`
  - `tests/test_cp26_repair_contract.py::test_anchor_commit_and_landed_base_are_distinct_and_explicit`
  - `tests/test_cp26_search.py::test_search_lineage_changes_when_context_adapter_changes`
  - `tests/test_cp26_r15.py::test_r15_authority_does_not_relabel_scientific_plan_or_parity`

  Three more tests were also repaired. They pass where `gauntlet/cp-26`'s commits or the local
  `evidence/<cp>` tags exist, but fail in a checkout without that history, which is what CI on GitHub has
  (`actions/checkout@v4`, depth 1, no tags):
  - `tests/test_cp26_repair_contract.py::test_original_documents_and_sections_1_through_23_stay_historical`
  - `tests/test_cp26_r15.py::test_original_numeric_functions_are_unchanged_by_r15`
  - `tests/test_cp26_parity.py::test_real_references_are_committed_and_internally_bitwise_consistent`
- One new evidence directory, `docs/track-b/evidence/cp-26/landing-repair/scientific-base-1e7eb02/`,
  says it holds the four modules at `1e7eb029f1cbbec6483aea4a7dda0754fd7adf0b`. Verify every byte
  against `git show 1e7eb029f1cbbec6483aea4a7dda0754fd7adf0b:src/cp26/<name>.py`, and verify the
  §§1–23 SHA-256 constant in `tests/test_cp26_repair_contract.py` against
  `git show 5cc3cc083c4340fd8d792eeaf6551a007987a877:capstone_v21.md`.
- The curated landing rule: `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-landing/exclusion-rule.txt`,
  SHA-256 `7cbd68734f864d78a076800ecb1db273a8b8e50ba00f0bf79b76d24ac72af565`. The curated paths are
  `git diff --name-only main <candidate>` minus its lines: a line ending in `/` excludes that folder,
  any other line that file.

## What to verify

1. **Each of the eight repairs**: the repair type (stale expectation, history, fixture), whether
   the cited authority supports the new value or record, and whether the test still checks what it
   checked. Look for skipped, deleted or loosened tests. Check the cited records themselves, for
   example `docs/track-b/evidence/cp-26/cold-rerun-2026-10-15/calibration-v21-r15.json`,
   `authority-v21-r16.json`, `runtime-code-v21-r16.json`, commit `8070238` (r16),
   `docs/track-b/capstone_v21-r16-to-v21-r17-amendments.md`,
   `docs/track-b/evidence/cp-26/repair-v21-r14/active-documents.json`,
   `reports/rebaseline/harness-log.json`, `reports/rebaseline/cold-rerun-2026-10-15/execution-manifest.json`
   and `parity.json`.
2. **Item 2**: whether anything outside `tests/` and `docs/track-b/evidence/cp-26/` changed, and if
   so whether it is allowed.
3. **Item 3**: rerun the suite yourself on the curated landing tree and on the full candidate tree,
   with the commands below.
4. **Item 4**: `git diff --stat 6f57febe3659b1f902c17f3db31ba41e41136178 <candidate> -- reports/` is
   empty. The brief's frozen paths are unchanged against `d8f912ad9be0867f11e4b634c2f482792ea5e951`:
   `reports/`, `data/`, `src/`, `pyproject.toml`, `uv.lock`, the anchors and amendment records,
   `AGENTS.md`, the role files and `docs/track-b/exposure-ledger.md`.
5. **History, exclusions and untracked outputs**: no test depends on them. Use a static audit of
   every Git call and excluded path that the tests reach, and the history-free run below.

## Environments the Lead prepared (verify them; do not trust them)

You make no Git write, so the Lead built the two landing environments. Prove each one's identity
with read-only commands before you use it.

- **Curated landing tree (the brief's procedure):** `/Users/djourno/Downloads/PJM/.local/worktrees/cp-26/critic-curated`.
  It is a detached worktree at `main`, with the curated paths checked out from the candidate
  (`git checkout <candidate> --pathspec-from-file=<list>`). Confirm read-only that:
  - `HEAD` is `main`;
  - `git diff --cached --name-only main` is exactly the curated path list you computed;
  - `git diff --cached --name-only <candidate> -- <each curated path>` is empty;
  - nothing is unstaged (`git diff --name-only` is empty).

  The Lead's `git write-tree` there gave tree `c4e3b0ba914bba33b4d2f27e635705df55a3ad42`, with
  2,397 files, 846 of them curated paths (44,801,005 bytes). Match it read-only:
  `git ls-tree -r c4e3b0ba914bba33b4d2f27e635705df55a3ad42` must list the same mode, blob and path as
  `git ls-files -s` in that worktree.
- **CI's view, with no history:** `/Users/djourno/Downloads/PJM/.local/tmp/cp-26-landing-repair/critic-ci-sim`.
  It is a new standalone repository, not a worktree, holding exactly one commit whose tree is the
  curated tree (`git -C <it> rev-parse HEAD^{tree}` should print `c4e3b0ba914bba33b4d2f27e635705df55a3ad42`). It has no tag and no other ref. Confirm `git -C <it> rev-list --all --count` is `1`
  and `git -C <it> tag` is empty. Confirm `git -C <it> ls-tree -r HEAD` matches the curated
  worktree's `git ls-files -s` (mode, blob, path). Confirm the candidate's commits do not resolve
  in it.
- **Full candidate tree:** your own clean critic worktree.

## Reproduction

Run each suite under the CP-26 monitor, which charges the test time to the existing CP-26 ledger
without resetting it. The monitor declares four workers, because `tests/test_cp26_ledger_liveness.py`
runs up to four concurrent processes. The monitor reads and writes only the ledger and job files
under `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26/`; that is accounting, not a Git write.
Run one suite at a time. For TREE in the three trees above, with ENV a fresh directory under
`/Users/djourno/Downloads/PJM/.local/tmp/cp-26-landing-repair/critic-envs/` and NAME `critic-2-<curated|ci-sim|full>`:

```text
/Users/djourno/Downloads/PJM/.venv/bin/python -B <your critic worktree>/scripts/cp26_rebaseline.py monitor \
  --name NAME --workers 4 --log /Users/djourno/Downloads/PJM/.local/artifacts/cp-26/landing-repair/logs/NAME.log -- \
  /usr/bin/env -u CP26_LEDGER -u CP26_MONITORED_JOB -u CP26_JOB_ID -u CP26_JOB_INDEX -u CP26_WORKERS \
  -u PYTHONPATH -u VIRTUAL_ENV -u PYTHONDONTWRITEBYTECODE UV_PROJECT_ENVIRONMENT=ENV/venv UV_PYTHON=3.12 UV_OFFLINE=1 \
  MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1 CP26_PROJECT_ROOT=ENV/absent-project-root \
  /bin/sh -c 'cd TREE && uv sync --locked --dev && uv run python scripts/build_wasm_payload.py && uv run pytest -q -p no:cacheprovider -rfEs'
```

- This is CI's sequence (`.github/workflows/tests.yml`) with Python 3.12, as CI pins it, run
  offline from the local uv cache. This machine's shell exports `PYTHONDONTWRITEBYTECODE=1`; CI does
  not, so the command unsets it.
- `CP26_PROJECT_ROOT` points at a path that does not exist. The default,
  `/Users/djourno/Downloads/PJM`, does not exist on a CI runner, so no test may read this machine's
  ledger or artifacts.
- The payload step prints a warning that the model was saved under Python 3.13; CI shows the same.
- Judge each suite by pytest's own final summary line in the log. The monitor prints a JSON line with
  the job's exit code. The Lead saw one earlier job whose watchdog closed it with
  `supervisor_identity_lost` after pytest had already finished; if that recurs, record it.

**Run budget.** One run per tree is enough. A previous review attempt ended without a verdict,
stopped by a usage limit; it is not evidence for this review. Keep every extra diagnostic run small.

**A behavior to judge.** `tests/test_cp26_ledger_liveness.py::test_rich_closed_jobs_three_busy_owners_accept_fourth_admin_with_full_future_history`
starts four inner monitors, and every inner process (monitor, supervisor, watchdog, child) runs with
`python -B` and imports `cp26.budget`, which imports numpy and pandas. Run alone in a venv that has
never compiled bytecode, with `PYTHONDONTWRITEBYTECODE=1` set, it times out at its controller's
15 s wait for the admin job. With bytecode writing allowed, as on CI, it passed 5 of 5 in the Lead's
runs, the first in a brand-new venv, with the admin job taking 8.3–9.1 s. Inside a full suite it
passed every run. Judge whether this is a defect of the repaired test or an artifact of the
environment. To reproduce, run it alone in a fresh venv both ways: set `TEST` to that node id, then
run the template with the payload step dropped and pytest given `$TEST` under its own
`--basetemp`. Do this once with `PYTHONDONTWRITEBYTECODE=1` added after `-u PYTHONDONTWRITEBYTECODE`,
and once without it. Each run's inner ledger is at
`<basetemp>/*/.local/artifacts/cp-26/ledger/budget.json`; its last four jobs are the three owners and
`ledger-rich-admin`.

**Expected:** zero failures in all three runs. In the history-free run, expect 16 skips, all from
earlier checkpoints' shallow-clone, missing-tag or anchor-bound skips; read the `SKIPPED` lines and
confirm none is a CP-26 test. The curated worktree, which shares the repository's objects, skips
fewer. Also expect `git diff --stat 6f57feb… <candidate> -- reports/` to print nothing.

Do not run any search, fit, forecast, replay, scoring, bootstrap or report regeneration. Make no
network access. Read nothing dated after 2026-09-06 in the data, and do not read `progress.md`, the
syllabus, Track A/C material or `orchestrator-role.md`.
