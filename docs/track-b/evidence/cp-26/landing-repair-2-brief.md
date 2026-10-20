# Track B Checkpoint Brief — CP-26 (landing repair, round 2: one load-sensitive stress test)

*Issued by the Orchestrator on 2026-10-20, Asia/Jerusalem.*

## Target
- Repository: DE-LU day-ahead forecasting, `/Users/djourno/Downloads/PJM` (origin
  `hrsi56/delu-day-ahead-forecast`). The work runs locally, in the existing CP-26 Lead worktree.
- Authorized checkpoint: CP-26, exactly one, as a second landing-repair round. No scientific work
  is reopened.
- Ratified plan anchor: `capstone_v21.md`, revision v21-r17 on `gauntlet/cp-26`, §24.7, SHA-256
  `3124451da84c3cd99fae728c371207aace6ae537474f7769d0ff6333ee53e4fc`.
- **The PASSes it keeps:**
  - the scientific Integration PASS, which binds `6f57febe3659b1f902c17f3db31ba41e41136178`;
  - the r17 PASS, which binds `f014e5b2f09dc7defa103b3c4ec5796d199c262d`;
  - the first repair round's PASS, which binds `04f00eac5506c550ed4c775b84dc65a41f86c007` (verdict
    SHA-256 `240378b707b822e9722ba0662eff60d0203ac16f1a333c0e47e090c76a55d36f`).

  This round changes no scientific output.

## Orchestrator-reported expected state
- **Branch / commit:** `gauntlet/cp-26` at `c4816f3b0470190bbaa375086c60262963c47329` (round 1's
  evidence tip), in the worktree `.local/worktrees/cp-26/lead`.
  - `main` = `origin/main` = `647d6eb81b2cf6e0cfaf4152f659d689ff973578`, untouched, with nothing
    staged.
  - No `cp-26` tag exists.
- **Working tree:** clean, apart from round 1's seven untracked run outputs. Leave them untracked
  and unchanged.
- **What already exists:** the Orchestrator's receipt of round 1, made on 2026-10-20 on this machine
  (8 cores):
  - **Every identity check of the return holds.**
    - `gauntlet.py return` reports 0 problems.
    - The repaired tests' recorded hashes match Git.
    - The curated path list regenerates to the same 852 paths.
    - The landing tree is `f14a676b5192a76c95fb29211131d0b5d6653277`, with 2,403 files.
  - **The workflow's seven steps** ran on a history-free single-commit copy of that tree, with
    `PYTHONDONTWRITEBYTECODE` unset and a fresh environment:
    - **Python 3.12** (the workflow's pin): all green, 2,205 passed and 16 skipped.
    - **Python 3.13:** one failure, while the Orchestrator was also loading the machine.
      `tests/test_cp26_ledger_liveness.py::test_rich_closed_jobs_three_busy_owners_accept_fourth_admin_with_full_future_history`
      raised `subprocess.TimeoutExpired` at `process.communicate(timeout=15)`, line 2169 at
      `c4816f3`.
  - **The emulation of GitHub's runner.** `ubuntu-latest` for a public repository has 4 vCPUs. The
    test starts three CPU-bound busy owners, which leaves about one core for the controller, the
    monitors and the arriving admin job. On this machine, four extra CPU burners
    (`(while :; do :; done) &`, four times) reproduce that: about four free cores, three of them
    taken by the owners. All runs used Python 3.12, the history-free copy, and
    `PYTHONDONTWRITEBYTECODE` unset.

    | Run | Result |
    |---|---|
    | the rich-admin test, quiet | 5/5 pass, about 32–39 s per run together with its sibling |
    | the rich-admin test, under the emulation | **5/5 fail**, the same `TimeoutExpired` at 15 s |
    | all 452 CP-26 tests (`tests/test_cp26_*.py`, `tests/test_rebaseline_disclosures.py`), under the emulation | only this test fails |
    | the rich-admin test under the emulation, in a scratch copy with the controller's wait at 120 s (line 2169) and the busy owners' self-deadline at 150 s (line 2122) | 3/3 pass, with every inner assertion holding; test call 31.7–33.4 s |
  - **The conclusion so far:** the harness's patience is too short for a 4-vCPU runner. The
    supervision property it tests holds. The scratch edit was a diagnostic only, never committed.
- Verify this yourself before relying on it, and report any material mismatch.

## Observable outcome
A new final candidate on `gauntlet/cp-26`, bound by one fresh focused Integration-Critic PASS:

- **the rich-admin test passes** under the emulation above and on a quiet machine, for the stated
  reason;
- **the workflow's full sequence is green** on a history-free single-commit copy of the new
  curated landing tree;
- **every scientific output is byte-identical** to `6f57feb`;
- **the return gives the new curated tree's hash,** its file count and its path list, for the
  Owner's LAND.

## Complete authoritative checkpoint bar
`capstone_v21.md` v21-r17 §24.7, all 111 clauses, already PASSed and unchanged. Round 1's brief
(`docs/track-b/evidence/cp-26/landing-repair-brief.md`, SHA-256
`27d3e1afbdcc5f02b88b27f59ed4935ac8bc99918ea8c58124e0cdbb3bd89e3d`) still holds. This brief adds
the following items, which are the bar for this candidate:

1. **The rich-admin test passes 5 of 5 times under the emulation, and 5 of 5 on a quiet machine.**
   The runs use Python 3.12, a history-free single-commit copy of the curated tree, and
   `PYTHONDONTWRITEBYTECODE` unset.
   - **What may change:** only the harness's patience. That is the controller's wait on the admin
     monitor, the busy owners' self-deadline, and any wait bound those two depend on.
   - **What never changes:**
     - the supervision policy (`S.SUPERVISION_POLICY`, `B.CAPS`);
     - the admin job's inner assertions: freshness, the lock-telemetry thresholds of 0.5 s, the
       2.0 s observation window, at least three observations, and four running workers;
     - any file outside `tests/`.
   - **Each changed bound is justified** by durations measured under the emulation, plus a stated
     margin for a runner slower than this machine's cores.
2. **No other test changes,** unless the same emulation shows it failing. In that case the same rule
   applies, and the test is listed.
3. **The workflow's seven steps are green** on a history-free single-commit copy of the new curated
   tree, under Python 3.12 and 3.13. The full suite is also green on the curated tree by round 1's
   procedure.
4. **Scope:**
   - `git diff --stat 6f57feb <new candidate> -- reports/` is empty;
   - `git diff --name-only 04f00ea <new candidate>` lists only the repaired test files and evidence
     under `docs/track-b/evidence/cp-26/`.
5. **One fresh focused Integration Critic,** from a clean detached checkout of the new candidate.
   It checks items 1–4, reruns item 1's emulation, and reruns the Python 3.12 sequence.

## Task-specific supporting extract
- **The history-free copy:**
  1. build the curated tree by round 1's procedure;
  2. `git archive <tree> | tar -x -C <tmp>`;
  3. in `<tmp>`: `git init -q -b main`, `git add -A`, `git commit -q --no-verify -m ci`.
- **The workflow's steps** (`.github/workflows/tests.yml`):
  1. `uv sync --locked --dev`;
  2. `uv run python scripts/build_wasm_payload.py`;
  3. `uv run pytest -q`;
  4. `uv run pytest tests/test_10_cqr_order_statistic.py -q`;
  5. `uv run python scripts/verify_release.py`;
  6. `uv run pytest tests/test_22_wasm_equivalence.py -q`;
  7. `python3 scripts/publication_guard.py tree`.

  Use `UV_PYTHON=3.12` and a fresh `UV_PROJECT_ENVIRONMENT` per interpreter.
- **The emulation:** start four `(while :; do :; done) &` burners, run, then kill them. Run nothing
  else heavy at the same time, because timing is the measurement.
- **Remove** every temporary copy, worktree, environment and burner afterwards.

## Applicable constraints
- **No scientific computation:** no search, fit, forecast, replay, scoring, bootstrap or report
  regeneration. Test runs only. Count their worker time in the existing ledger, without resetting
  it.
- **No retrieval, no remote write, no network** beyond `uv sync` from the lock.
- **Files that never change:**
  - `reports/`, `data/` and `src/`;
  - the anchors and amendment records, `AGENTS.md`, the role files and the exposure ledger;
  - the root `pyproject.toml` and `uv.lock`;
  - every committed evidence file of the earlier chains and of round 1.
- **The red line (v21-r13 §24.2):** nothing dated after 2026-09-06 is read.
- **Credentials** follow `AGENTS.md` § Credentials; none is needed. Export
  `MLFLOW_DISABLE_TELEMETRY=true` and `DO_NOT_TRACK=1`.
- **Commits:**
  - on `gauntlet/cp-26` only;
  - the first commit packages this brief as
    `docs/track-b/evidence/cp-26/landing-repair-2-brief.md`;
  - round 1's `integration.md` is preserved byte-identical under
    `docs/track-b/evidence/cp-26/landing-repair/`, before it is replaced.
- **Checks:** run `scripts/gauntlet.py return` on the return. Launch the Critic with `critic-open`,
  `critic-brief` and `critic-close`.
- **Owner-facing Git commands** must be non-interactive: `git --no-pager …` and
  `git commit -F <file>`.

## Timebox
About 2 active hours from orientation to the terminal return.

## Owner-only actions already authorized
- **This round,** under the Owner's instruction of 2026-10-19 ("אני מאשר לך לעשות הכל"). It covers
  local `gauntlet/cp-26` commits and the brief's packaging.
- **Nothing else:** no mainline operation, push, tag, publication, anchor edit or CP-28 work.

## Stop and return
Return exactly one of PASS / BLOCKED / INCOMPLETE, using templates §3.
- **The return carries:**
  - the new final candidate, the evidence tip and the verdict-only delta;
  - the new curated tree's hash, its file count and its path list;
  - the measured durations behind each changed bound.
- Name any interview-answer trigger in one line.

Do not begin CP-28. Do not commit to `main`, publish or push. Leave the branch and worktree for the
Owner's LAND.
