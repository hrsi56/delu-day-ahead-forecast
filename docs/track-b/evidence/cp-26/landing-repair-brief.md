# Track B Checkpoint Brief — CP-26 (landing repair: five failing tests, and the curated landing tree)

*Issued by the Orchestrator on 2026-10-19, Asia/Jerusalem.*

## Target
- Repository: DE-LU day-ahead forecasting, `/Users/djourno/Downloads/PJM` (origin
  `hrsi56/delu-day-ahead-forecast`). The work runs locally, in the existing CP-26 Lead worktree.
- Authorized checkpoint: CP-26, exactly one, as a landing repair of its completed candidate. No
  scientific work is reopened.
- Ratified plan anchor: `capstone_v21.md`, revision v21-r17 on `gauntlet/cp-26`, §24.7, SHA-256
  `3124451da84c3cd99fae728c371207aace6ae537474f7769d0ff6333ee53e4fc`. §24.7's 111 clauses keep the
  scientific Integration PASS that binds `6f57febe3659b1f902c17f3db31ba41e41136178`, and the r17 PASS
  that binds `f014e5b2f09dc7defa103b3c4ec5796d199c262d`. This repair changes no scientific output.

## Orchestrator-reported expected state
- **Branch / commit:** `gauntlet/cp-26` at `d8f912ad9be0867f11e4b634c2f482792ea5e951`, in the
  worktree `.local/worktrees/cp-26/lead`. `main` = `origin/main` =
  `647d6eb81b2cf6e0cfaf4152f659d689ff973578`, untouched, with nothing staged.
- **Working tree:** the Lead worktree is clean apart from three untracked output folders from the
  completed run (`reports/rebaseline/cold-rerun-2026-10-15/diagnostics/`, `inference/`,
  `presentation-v21-r16/report.json`). Leave them untracked and unchanged.
- **What already exists:**
  - **The five failing tests,** found by the Orchestrator on 2026-10-19, in a clean CI-style run
    (`uv sync --locked --dev`, the browser payload build, then `pytest -q`):

    | Test | Fails at | Observed |
    |---|---|---|
    | `tests/test_cp26_ledger_liveness.py::test_three_jobs_keep_fresh_supervision_with_full_future_history` | `6f57feb` and `d8f912a` | expects timeouts 0.5/10/2 s; finds the r15-calibrated 3/14/8 s |
    | `tests/test_cp26_ledger_liveness.py::test_rich_closed_jobs_three_busy_owners_accept_fourth_admin_with_full_future_history` | `6f57feb` and `d8f912a` | the same |
    | `tests/test_cp26_repair_contract.py::test_anchor_commit_and_landed_base_are_distinct_and_explicit` | `6f57feb` and `d8f912a` | expects anchor commit `332baeb…`; finds `4766a61…` |
    | `tests/test_cp26_search.py::test_search_lineage_changes_when_context_adapter_changes` | `6f57feb` and `d8f912a` | `FileNotFoundError` for `docs/track-b/evidence/cp-26/cold-rerun-2026-10-15/runtime-code-v21-r16.json` in its temporary copy |
    | `tests/test_cp26_r15.py::test_r15_authority_does_not_relabel_scientific_plan_or_parity` | `d8f912a` only | `HarnessError: ratified continuation document identity changed`, after r17 |

    Everything else passes: 2,208 passed and 8 skipped on the curated tree below.
  - **The curated landing.** The candidate's 10,258 changed files hold 3.43 GB, including a 357 MB
    file that GitHub refuses. The Owner approved landing a curated subset on 2026-10-19:
    - every path that `main..<evidence tip>` adds or changes, except those in
      `.local/artifacts/cp-26-landing/exclusion-rule.txt`
      (`7cbd68734f864d78a076800ecb1db273a8b8e50ba00f0bf79b76d24ac72af565`);
    - at `d8f912a` that is 839 files and 44.6 MB.

    The excluded 9,419 files (3.39 GB: the forecast ledger, search results, replay state and the
    abandoned r14 runs) stay in the local evidence tag and a verified bundle. CI on GitHub clones
    `main` only: it has neither those files nor the branch's history.
- Verify this yourself before relying on it, and report any material mismatch.

## Observable outcome
A new final candidate on `gauntlet/cp-26`, bound by one fresh focused Integration-Critic PASS:

- **the full test suite passes,** with zero failures, in a clean CI-style run on the **curated
  landing tree**: a temporary worktree at `main` with the curated paths checked out from the new
  candidate;
- **the scientific outputs are byte-identical** to `6f57feb`: every file under `reports/` and every
  committed score, inference, diagnostic, report and packet file;
- **no test depends** on the `gauntlet/cp-26` commit history, on an excluded file, or on the
  untracked output folders;
- **the return gives the curated tree's hash** (`git write-tree` in that worktree) and its file
  count, for the Owner's LAND.

## Complete authoritative checkpoint bar
`capstone_v21.md` v21-r17 §24.7, all 111 clauses, already PASSed and unchanged, together with this
brief's repair items, which are the bar for this candidate:

1. **The five tests above pass** for a correct reason, not by being skipped, deleted or loosened.
   Each repair is stated:
   - a stale expectation is updated to the authorized value, citing its authority (r15's
     calibration, the r16 commits, r17);
   - a history-dependent check reads recorded identities instead of the branch's Git history;
   - a fixture includes what it needs.
2. **A repair outside `tests/` is allowed only if a guard is wrong under r17.** It is limited to
   `src/cp26/` identity and guard code, never to a forecast, search, scoring, inference or
   reporting path, and it is justified in the return.
3. **The full suite is green on the curated landing tree,** and also on the full candidate tree.
4. **Every scientific output is unchanged:** `git diff --stat 6f57feb <new candidate> -- reports/`
   is empty.
5. **One fresh focused Integration Critic,** from a clean detached checkout of the new candidate,
   checks items 1–4 and reruns the suite on the curated tree.

## Task-specific supporting extract
- **Building the curated tree:**
  1. `git worktree add --detach <tmp> main`;
  2. in it, `git checkout <candidate> --pathspec-from-file=<list>`, where the list is
     `git diff --name-only main <candidate>` minus the exclusion rule;
  3. a fresh environment with `UV_PROJECT_ENVIRONMENT=<tmp-env> uv sync --locked --dev`;
  4. `uv run python scripts/build_wasm_payload.py`;
  5. `uv run pytest -q -p no:cacheprovider`.
- **The full candidate tree** is checked the same way in a detached worktree at the candidate.
- **Remove** both temporary worktrees and environments afterwards.

## Applicable constraints
- **No scientific computation:** no search, fit, forecast, replay, scoring, bootstrap or report
  regeneration. Test runs only. Count their worker time in the existing ledger, without resetting
  it.
- **No retrieval, no remote write, no network.**
- **Files that never change:**
  - `reports/`;
  - `data/`;
  - the anchors and amendment records, `AGENTS.md`, the role files and the exposure ledger;
  - the landed member code (`src/delu_forecast/`, `src/cp15/` to `src/cp25/`);
  - the root `pyproject.toml` and `uv.lock`;
  - every committed evidence file of the earlier chains.
- **The red line (v21-r13 §24.2):** nothing dated after 2026-09-06 is read.
- **Credentials** follow `AGENTS.md` § Credentials; none is needed. Export
  `MLFLOW_DISABLE_TELEMETRY=true` and `DO_NOT_TRACK=1`.
- **Commit** on `gauntlet/cp-26` only; the first commit packages this brief as
  `docs/track-b/evidence/cp-26/landing-repair-brief.md`. Check the return with
  `scripts/gauntlet.py return`. Launch the Critic with `critic-open`, `critic-brief` and
  `critic-close`.
- **Owner-facing Git commands** must be non-interactive: `git --no-pager …` and
  `git commit -F <file>`.

## Timebox
About 4 active hours from orientation to the terminal return.

## Owner-only actions already authorized
- **This repair,** under the Owner's instruction of 2026-10-19 ("אני מאשר לך לעשות הכל"),
  delivered with this brief. It covers local `gauntlet/cp-26` commits and the brief's packaging.
- **Nothing else:** no mainline operation, push, tag, publication, anchor edit or CP-28 work.

## Stop and return
Return exactly one of PASS / BLOCKED / INCOMPLETE, using templates §3.
- The return carries the new final candidate and evidence tip, and the verdict-only delta.
- It also gives the curated tree's hash and file count, and the exact repair of each test.
- Name any interview-answer trigger in one line.

Do not begin CP-28. Do not commit to `main`, publish or push. Leave the branch and worktree for the
Owner's LAND.
