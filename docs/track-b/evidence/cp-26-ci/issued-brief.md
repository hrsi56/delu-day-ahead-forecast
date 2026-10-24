# Track B Checkpoint Brief — CP-26-CI (test-only: CP-26's stress tests off GitHub's runner, and a living exposure ledger)

*Issued by the Orchestrator on 2026-10-21, Asia/Jerusalem.*

## Target
- Repository: DE-LU day-ahead forecasting, `/Users/djourno/Downloads/PJM` (origin
  `hrsi56/delu-day-ahead-forecast`).
- Authorized checkpoint: CP-26-CI, exactly one. It is a test-only maintenance round after CP-26's
  landing. No scientific work is reopened.
- Ratified plan anchor: `capstone_v21.md`, revision v21-r17, SHA-256
  `3124451da84c3cd99fae728c371207aace6ae537474f7769d0ff6333ee53e4fc`, on `main`. §24.7's results
  and the PASSes recorded in `docs/track-b/cp-26-landing-2026-10-21.md` are unchanged.
  PUBLISH_RULES 1.5 (SHA-256 `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`) is
  unchanged.

## Orchestrator-reported expected state
- **Branch / commit:**
  - `main` = `origin/main` = `2a9e4fd23b6a33b4a33a6a96d5d398e04200729c`, clean;
  - no `gauntlet/*` branch;
  - `evidence/cp-26` = `ca20331`, a local-only tag;
  - `land/cp-26` = `61658c7`.
- **Start:**
  - run `scripts/gauntlet.py start cp-26-ci`;
  - create `gauntlet/cp-26-ci` from `main` in the worktree `.local/worktrees/cp-26-ci/lead`.
- **What already exists:**
  - **The stress test is flaky on GitHub's runner.**
    `tests/test_cp26_ledger_liveness.py::test_rich_closed_jobs_three_busy_owners_accept_fourth_admin_with_full_future_history`
    has failed once in six runs there. In workflow run 39525927648 at `2a9e4fd`, a docs-only
    commit, attempt 1 failed at line 2199 (`assert job['running']`): after the admin job, one busy
    owner was no longer running. Attempt 2 passed.
  - **Two earlier failure modes are already fixed** (the 15 s wait and the 0.5 s lock limits; CP-26
    landing record, repair rounds 2–3). The Orchestrator's four- and six-burner emulation passes
    the test 10/10 on this 8-core machine, so the emulation does not reproduce this third mode.
  - **GitHub's runner** (`ubuntu-latest`, public repository) has 4 vCPUs. The test runs three
    CPU-bound owners and an admin job, plus their supervisors and watchdogs.
  - **The exposure ledger is pinned.** `src/cp26/harness.py`'s `PINS` binds
    `docs/track-b/exposure-ledger.md` at SHA-256 `375fef5d…` (its bytes at `61658c7`).
    `tests/test_cp26_r15.py` and `tests/test_cp26_repair_contract.py` check the live file against
    it. On 2026-10-21, commit `2abd63b` added one sentence to the ledger and both tests failed on
    `main`; `c1c4647` restored it. §24.2 says the Orchestrator adds every later exposure, and the
    4.7T audit (§24.9) reads the ledger, so it must be able to grow.
- Verify this yourself before relying on it, and report any material mismatch.

## Observable outcome
A final candidate on `gauntlet/cp-26-ci`, bound by one fresh focused Integration-Critic PASS:

- **CP-26's stress tests skip on GitHub's runner,** with a stated reason, and run everywhere else;
- **the live exposure ledger can gain rows** without any test failing, while CP-26's ledger stays
  bound to its exact bytes;
- **the workflow is green** on a history-free copy of the candidate, with GitHub's environment;
- **nothing outside `tests/`** and the new evidence changes.

## Complete authoritative checkpoint bar
The Owner's decision of 2026-10-21 ("(א), עם הסימון stress. עכשיו."), as these items:

1. **The `stress` marker.**
   - **Which tests:** every CP-26 test that starts real CP-26 monitors (`real_monitor`,
     `three_real_monitors`, `arriving_admin_monitor`, or the same through the CLI) with concurrent
     children whose timing the test asserts, at least the rich-admin test above. The return lists
     each marked test and the one-line reason it qualifies. Tests that use no real monitor are not
     marked.
   - **Where they skip:** only when `CI=true` (GitHub sets it) and `RUN_STRESS` is not `1`. The
     reason is shown in pytest's output: CP-26 supervision stress test, run locally because a
     4-vCPU CI runner cannot host it reliably, `RUN_STRESS=1` forces it.
   - **Elsewhere they run by default,** with no environment variable. `pytest -m stress` selects
     exactly them.
   - **No marked test's body or assertion changes.**
2. **A living exposure ledger.**
   - **The frozen copy:** commit a byte-identical copy of `61658c7:docs/track-b/exposure-ledger.md`
     as CP-26 evidence, under `docs/track-b/evidence/cp-26/`.
   - **What the tests check instead:**
     - that copy's SHA-256 equals `PINS['docs/track-b/exposure-ledger.md']`;
     - the live ledger still holds every row of the copy's table, verbatim and in order. Rows may
       be added after them, and the prose above the table may change.
   - **What does not change:** `src/cp26/harness.py` and `PINS`.
   - **Every test that reads the live ledger's bytes for an identity** (pinned-file loops, input
     fingerprints) uses the frozen copy, which the return lists.
3. **Proven both ways,** in a scratch copy of the candidate:
   - append a synthetic row to the live ledger, and the full suite passes;
   - alter one row that existed at CP-26, and at least one named test fails.

   The scratch copy is removed afterwards and nothing of it is committed.
4. **The suite, three ways,** each on a history-free single-commit copy of the candidate's tree:
   - with `CI=true` the workflow's seven steps are green under Python 3.12 and 3.13, and the
     stress tests show as skipped with the reason;
   - without `CI`, the full suite is green under Python 3.12 on a quiet machine, stress tests
     included;
   - `RUN_STRESS=1 CI=true` runs them.
5. **Scope:**
   - `git diff --stat main <candidate> -- reports/ src/ data/ scripts/ .github/ pyproject.toml uv.lock`
     is empty;
   - the anchors, the amendment records, `AGENTS.md`, the role files, the backup register and the
     live exposure ledger are unchanged;
   - `tests/conftest.py` may change only to register the marker and the skip. Check first that no
     committed evidence binds its bytes, and say so.
6. **One fresh focused Integration Critic,** from a clean detached checkout of the candidate. It
   checks items 1–5, and reruns item 3 and the `CI=true` Python 3.12 sequence.

## Task-specific supporting extract
- **The history-free copy:**
  1. `git archive <tree> | tar -x -C <tmp>`;
  2. `git init -q -b main`, `git add -A`, `git commit -q --no-verify -m ci` in it;
  3. a fresh `UV_PROJECT_ENVIRONMENT` per interpreter (`UV_PYTHON=3.12` or `3.13`);
  4. `unset PYTHONDONTWRITEBYTECODE`, as on GitHub.
- **The workflow's seven steps** (`.github/workflows/tests.yml`):
  1. `uv sync --locked --dev`;
  2. `uv run python scripts/build_wasm_payload.py`;
  3. `uv run pytest -q`;
  4. `uv run pytest tests/test_10_cqr_order_statistic.py -q`;
  5. `uv run python scripts/verify_release.py`;
  6. `uv run pytest tests/test_22_wasm_equivalence.py -q`;
  7. `python3 scripts/publication_guard.py tree`.
- **Remove** every temporary copy, worktree and environment afterwards.

## Applicable constraints
- **No scientific computation, no retrieval, no remote write, no network** beyond `uv sync` from
  the lock.
- **Never change** `reports/`, `data/`, `src/`, `scripts/`, `.github/`, the root `pyproject.toml`
  or `uv.lock`, the anchors and amendment records, `AGENTS.md`, the role files, the backup register,
  or any committed evidence of earlier chains.
- **The red line (v21-r13 §24.2):** nothing dated after 2026-09-06 is read.
- **Credentials** follow `AGENTS.md` § Credentials; none is needed. Export
  `MLFLOW_DISABLE_TELEMETRY=true` and `DO_NOT_TRACK=1`.
- **Commits:** on `gauntlet/cp-26-ci` only. The first commit packages this brief as
  `docs/track-b/evidence/cp-26-ci/issued-brief.md`.
- **Checks:** run `scripts/gauntlet.py return` on the return. Launch the Critic with `critic-open`,
  `critic-brief` and `critic-close`.
- **Memory:** do not open or edit the files in the Claude memory directory
  (`~/.claude/projects/-Users-djourno-Downloads-PJM/memory/`). Its auto-loaded index informs no
  decision.
- **Owner-facing Git commands** must be non-interactive: `git --no-pager …` and
  `git commit -F <file>`.

## Timebox
About 3 active hours from orientation to the terminal return.

## Owner-only actions already authorized
- **This round,** under the Owner's instruction of 2026-10-21 ("(א), עם הסימון stress. עכשיו.").
  It covers the branch, the worktree, local commits and the brief's packaging.
- **Nothing else:** no mainline operation, push, tag, publication, anchor edit or CP-28 work.

## Stop and return
Return exactly one of PASS / BLOCKED / INCOMPLETE, using templates §3.
- **The return carries:**
  - the final candidate, the evidence tip and the verdict-only delta;
  - the marked tests and their reasons;
  - the tests moved to the frozen ledger copy;
  - item 3's two results.
- Name any interview-answer trigger in one line.

Do not begin CP-28. Do not commit to `main`, publish or push. Leave the branch and worktree for the
Owner's LAND.
