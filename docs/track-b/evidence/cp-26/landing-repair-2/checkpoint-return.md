# Track B Checkpoint Return — CP-26 (landing repair, round 2)

## Status
BLOCKED

## Identity
- Repository `/Users/djourno/Downloads/PJM` (origin `hrsi56/delu-day-ahead-forecast`). Checkpoint CP-26, second landing-repair round, under the Orchestrator's brief of 2026-10-20 (`docs/track-b/evidence/cp-26/landing-repair-2-brief.md`, SHA-256 `cdef3247b23f4944cf56fcabff942aa295f834e1f5787b056b3ff98d4751e464`).
- Ratified anchor: `capstone_v21.md` v21-r17, §24.7, SHA-256 `3124451da84c3cd99fae728c371207aace6ae537474f7769d0ff6333ee53e4fc`, unchanged.
- final_candidate_sha: `da7acf773a19d9f1781e7386189d626019c31ac3`. This is the current candidate, **not reviewed**. No Integration Critic was launched, because bar item 1 cannot be met with the changes the brief allows.
- evidence_tip_sha: the commit that adds this file. A file cannot contain its own commit SHA, so the terminal message states it, with the output of `git diff --name-only da7acf773a19d9f1781e7386189d626019c31ac3..<evidence_tip_sha>`. That delta touches only `docs/track-b/evidence/cp-26/landing-repair-2/`.
- PASSes kept, all unchanged:
  - the scientific PASS, binding `6f57febe3659b1f902c17f3db31ba41e41136178`;
  - the r17 PASS, binding `f014e5b2f09dc7defa103b3c4ec5796d199c262d`;
  - round 1's PASS, binding `04f00eac5506c550ed4c775b84dc65a41f86c007` (verdict `240378b7…d36f`). It is still the canonical `integration.md` and is also preserved byte-identical as `landing-repair/integration-PASS.md`.

## Repository state
- Branch `gauntlet/cp-26`, in the existing Lead worktree `.local/worktrees/cp-26/lead`.
  - The tracked tree is clean.
  - Round 1's seven untracked run outputs are untracked and unchanged.
- `main` = `origin/main` = `647d6eb81b2cf6e0cfaf4152f659d689ff973578`, untouched, with nothing staged. Nothing was pushed, and no tag was created.
- Commits added to `gauntlet/cp-26`, the only branch written:
  - `7564087`: package the brief;
  - `ea373b8`: preserve round 1's verdict;
  - `2aa7539`: the first candidate (patience of 120 s and 160 s);
  - `da7acf7`: the current candidate (160 s and 200 s);
  - the evidence commit.
- Worktrees created and removed: three temporary curated worktrees from `stress_check.py copy` (at `c4816f3`, `2aa7539` and `da7acf7`), each removed right after `git write-tree`.
- Scratch copies and environments under `.local/tmp/cp-26-landing-repair-2/` were removed: three history-free one-commit repositories, their uv environments, and every burner.
- Kept as local recovery material:
  - monitor logs under `.local/artifacts/cp-26/landing-repair-2/logs/`;
  - per-run pytest logs and inner admin logs under `.local/artifacts/cp-26/landing-repair-2/records/`;
  - the candidate's curated path list at `.local/artifacts/cp-26-landing/include-repair-2-da7acf7.txt`.
- No branch or tag was created. Round 1's `critic-1` record in `.local/artifacts/cp-26/critic-open.json` is still open and was left alone.

## Complete checklist with direct evidence
| # | Checklist item | Status | Direct evidence |
|---|---|---|---|
| §24.7 | All 111 clauses, already PASSed, unchanged | Holds | The anchor's SHA-256 at `da7acf7` is `3124451d…`. `git diff --stat 6f57feb da7acf7 -- reports/` is empty. |
| 1 | Rich-admin test 5/5 under the emulation and 5/5 quiet (Python 3.12, history-free copy, `PYTHONDONTWRITEBYTECODE` unset) | **NOT MET**: emulation 3/5, quiet 5/5 | `verification.json` `final_candidate_batches`. Both emulated failures are inside the admin job, on its fixed 0.5 s lock thresholds (admin script line 17), never on a harness wait. Details under *Open risk*. |
| 1a | Only the harness's patience changes | Holds | Controller's wait on the admin: 15 → 160 s. Owners' self-deadline: 30 → 200 s, which is the ready wait (20 s, unchanged) + 160 s + 20 s. The ready wait now reads its unchanged 20 s from the same constants. |
| 1b | Never changed: `S.SUPERVISION_POLICY`, `B.CAPS`, the admin's inner assertions, files outside `tests/` | Holds | `git diff c4816f3 da7acf7 -- src scripts pyproject.toml uv.lock` is empty. In the test, the admin script and the policy and cap assertions are byte-unchanged. |
| 1c | Each changed bound justified by measured durations plus a stated margin | Holds | `landing-repair-2/patience-measurement.json`; see *Changed bounds* below. |
| 2 | No other test changes unless the same emulation shows it failing | Holds | `tests/test_cp26_*.py` and `tests/test_rebaseline_disclosures.py` (24 files) under the emulation at `da7acf7`: `452 passed in 404.44s`. Only one test file changed. |
| 3 | Seven steps green under 3.12 and 3.13 on the history-free copy; full suite green by round 1's procedure | **NOT RUN** | Moot until item 1 can be met. The candidate will change. |
| 4 | Scope | Holds | `git diff --stat 6f57feb da7acf7 -- reports/` is empty. `git diff --name-only 04f00ea da7acf7` lists `tests/test_cp26_ledger_liveness.py` and evidence under `docs/track-b/evidence/cp-26/` only. |
| 5 | One fresh focused Integration Critic | **NOT RUN** | BLOCKED before review. |

### Changed bounds and the durations behind them
Measured under the emulation with the bounds lifted, on 12 passing runs, including the first run in a fresh environment, which compiles bytecode:
- busy → stop: 19.9–28.9 s. This is an upper bound on the controller's wait on the admin; warm runs stay at or below 22.0 s.
- Checks after the admin returns: 1.8–3.2 s.
- Owner ready → stop: 20.2–29.5 s.
- Ready spread: at most 0.84 s.
- Owners exit at most 0.89 s after `stop`.

The margin assumes a runner core 4× slower than this machine's, times 1.3 for scheduling variance. On `ubuntu-latest` (4 vCPU, which is 2 SMT cores), the free vCPU shares a physical core with a busy owner.
- **Controller's wait:** 28.9 × 4 × 1.3 = 150.3 s, so 160 s.
- **Owners' self-deadline:** 20 s ready wait + 160 s + 20 s for the checks before `stop` (3.2 × 4 × 1.3 = 16.8 s) = 200 s.
- **History of the values:** the first candidate (`2aa7539`) set 120 s and 160 s from warm runs only. Its own fresh-environment run took 28.9 s, which `da7acf7` covers.

With these bounds, no run failed on a harness wait. On a quiet machine, busy → stop already took 12.3–15.5 s, so the old 15 s bound was marginal even with no load.

## Integration verdict
- None for this round. `docs/track-b/evidence/cp-26/integration.md` is still round 1's verdict, binding `04f00eac5506c550ed4c775b84dc65a41f86c007`.

## Reproduction
- **Tool:** `docs/track-b/evidence/cp-26/landing-repair-2/stress_check.py` (stdlib only).
  - `copy --candidate <sha> --out <dir>`: the curated tree by round 1's procedure, then the brief's history-free copy.
  - `burners start|stop --record <json> [--count 3]`: the burners.
  - `stress --copy <dir>/copy --env <fresh env> --out <dir> --label <x> --emulation four-burners|quiet --runs 5`: the rich-admin test.
  - `pytest … 'tests/test_cp26_*.py' tests/test_rebaseline_disclosures.py`: the CP-26 selection.
- **Wrapping:** every test batch ran as `/Users/djourno/Downloads/PJM/.venv/bin/python -B scripts/cp26_rebaseline.py monitor --name landing-repair-2-<x> --workers 4 -- python3 stress_check.py …`, which charges the CP-26 ledger. The burners ran outside it.
- **The outer monitor's own load:** its supervisor and watchdog read the 21 MB production ledger every 0.2 s, using about 0.6 core even with an idle child. Four burners here therefore amount to about 4.6 burners of load, and three to about 3.6. The two settings bracket the brief's four.
- **Curated tree at `da7acf7`:**
  - 856 curated paths, 9,419 excluded;
  - path list SHA-256 `d628beb8…7429`;
  - `git write-tree` = `78a7eabe5874c345f9d035db0d31db2b38c731d0`, with 2,407 files;
  - the one-commit copy has the same tree.

  This is not a LAND tree, because the round is BLOCKED. The baseline at `c4816f3` reproduced the Orchestrator's receipt exactly: 852 paths, `f14a676b…`, 2,403 files.

| Batch (rich-admin unless noted) | Load | Result | Where it failed |
|---|---|---|---|
| baseline `c4816f3` | 4 burners | 0/2 | `TimeoutExpired` at the 15 s controller wait (reproduces the receipt) |
| baseline `c4816f3` | quiet | 1/1 | — |
| diagnostic, bounds lifted to 600/900 s in a scratch copy only | 4 burners | 4/5 and 4/5 | admin line 18, `peak_wait_seconds<0.5` |
| first candidate `2aa7539` | 4 burners | 4/5 | admin line 18; owner peak wait 0.532 s |
| final candidate `da7acf7` | 4 burners | **3/5** | admin line 17 (`peak_hold_seconds<0.5`): hold 0.509 s; and wait 0.892 s with hold 0.705 s |
| final candidate `da7acf7` | quiet | **5/5** | owner peak lock wait 0.23–0.39 s |
| final candidate `da7acf7` | 3 burners (lighter than the brief) | 4/5 | admin line 18; wait 0.814 s, hold 0.733 s |
| final candidate, 452 CP-26 tests | 4 burners | 452/452 | — |

Once patience stopped cutting runs off, 19 of 25 dedicated emulated runs passed.
- Five of the six failures are confirmed by the admin's own log, at line 17 or 18 (the two fixed 0.5 s lock thresholds).
- The sixth, in the first diagnostic batch, failed the same way (admin exit 1, never a harness wait), but its log was not kept.
- In the 20 runs that record it, from the first candidate on, the lock-timeout count is 0.

## Files changed
`git diff --stat c4816f3 <evidence tip>`:
- `tests/test_cp26_ledger_liveness.py`: the patience constants (15 → 160 s and 30 → 200 s), with the measured basis in a comment.
- `docs/track-b/evidence/cp-26/landing-repair-2-brief.md`: the issued brief, byte-identical.
- `docs/track-b/evidence/cp-26/landing-repair/integration-PASS.md`: round 1's verdict, preserved byte-identical.
- `docs/track-b/evidence/cp-26/landing-repair-2/stress_check.py`: the copy, emulation and timing tool. The evidence commit adds `--count`.
- `docs/track-b/evidence/cp-26/landing-repair-2/patience-measurement.json`: the durations behind the bounds, and the earlier batches.
- `docs/track-b/evidence/cp-26/landing-repair-2/verification.json`: the final candidate's batches and the ledger charge.
- `docs/track-b/evidence/cp-26/landing-repair-2/checkpoint-return.md`: this return.

## Elapsed
- About 1 active hour against the 2-hour timebox.
- Test time charged to the CP-26 ledger, without a reset: 6,823.5 machine-seconds (1.90 h) across 10 monitored jobs (indices 514–523). The cumulative total moved from 246.44 h to 248.34 h of 500 h.
- Burner load, recorded but not charged: 6,152.6 s. The burners are emulation load, not tests. The ledger's 4-worker cap admits no second job, and the ledger has no entry point for reported time.

## Open risk or exact owner action
**Decision needed.** The patience repair works: with it, no run fails on a harness wait. But the test still fails under the brief's emulation about one run in four. Every failure comes from the admin job's two **fixed 0.5 s lock-telemetry thresholds**, which this brief keeps unchanged:
- one run in five under a load slightly lighter than the brief's;
- six of 25 across all emulated runs.

**Where the 0.5 s comes from.** Both literals were written at `1c89354` (2026-10-14, r14). At that commit, `src/cp26/supervisor.py` had `LEDGER_TIMEOUT_SECONDS = 0.5`, so `< 0.5` meant "below the ledger timeout". r15's calibration set that timeout to 3.0 s (authority: `calibration-v21-r15.json` `policy_tested` and `authority-v21-r16.json` `limits_preserved`, the records round 1 cited). The same test's controller-side check `assert_live_lock_telemetry` already uses `< S.LEDGER_TIMEOUT_SECONDS`.

**Observed peaks:**
- under emulation: wait up to 0.892 s, hold up to 0.733 s;
- quiet: wait up to 0.39 s;
- no lock timeout in any of the 20 runs that record it.

On a real 2-core SMT runner the free vCPU is likely slower than the emulated one, so the failure rate there is unlikely to be lower.

**Smallest exact change to authorize.** In `tests/test_cp26_ledger_liveness.py`, in `test_rich_closed_jobs_three_busy_owners_accept_fourth_admin_with_full_future_history`, replace the admin script's `telemetry["peak_hold_seconds"]<0.5` and `telemetry["peak_wait_seconds"]<0.5` with `<S.LEDGER_TIMEOUT_SECONDS`. That is r15's calibrated 3.0 s, the value the literal equaled when it was written. The admin child already imports `S`.

Any other fixed value is the Orchestrator's call. A value near 1 s would leave little margin over the 0.89 s already observed.

The next round would then rerun item 1 (5/5 under the emulation, 5/5 quiet), items 3–4 and the Critic. Item 2 has already been checked at this candidate.

## Landing report
- **Proposed disposition:** LAND, deferred. Do not land now: as it stands, this stress test is expected to fail on a 4-vCPU runner in a sizeable share of runs. Land after a round that meets item 1.
- **Evidence tip to preserve:** given in the terminal message.
- **Live documents citing this branch,** to repoint on reclamation: as round 1's return listed them, `progress.md:111`, plus the locked §24.7 text at `capstone_v21.md:4368`, which needs no repointing. I did not rerun `gauntlet.py citations`, because it prints `progress.md` text.
- **Proposed commit message:** deferred to the round that meets item 1. That round's curated tree, hash and count replace the values above.

## Post-return reads
After the return was committed and no engineering decision remained, I read the shared auto-memory note `cp-26-landing-in-flight-2026-10-20.md`, which holds Orchestrator-side notes. I read it only to update its CP-26 state line. It informed nothing in this return. No Integration verdict exists in this round.
