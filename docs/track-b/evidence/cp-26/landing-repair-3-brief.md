# Track B Checkpoint Brief — CP-26 (landing repair, round 3: the rich-admin test's stale lock limits)

Issued by the Orchestrator on 2026-10-20, Asia/Jerusalem.

## Target
Repository: DE-LU day-ahead forecasting, /Users/djourno/Downloads/PJM (origin hrsi56/delu-day-ahead-forecast). The work runs locally, in the existing CP-26 Lead worktree.

Authorized checkpoint: CP-26, exactly one, as a third landing-repair round. No scientific work is reopened.

Ratified plan anchor: capstone_v21.md, revision v21-r17 on gauntlet/cp-26, §24.7, SHA-256 3124451da84c3cd99fae728c371207aace6ae537474f7769d0ff6333ee53e4fc.

The PASSes it keeps:

- the scientific Integration PASS, which binds 6f57febe3659b1f902c17f3db31ba41e41136178;
- the r17 PASS, which binds f014e5b2f09dc7defa103b3c4ec5796d199c262d;
- round 1's PASS, which binds 04f00eac5506c550ed4c775b84dc65a41f86c007 (verdict SHA-256 240378b707b822e9722ba0662eff60d0203ac16f1a333c0e47e090c76a55d36f).

This round changes no scientific output.

## Orchestrator-reported expected state
Branch / commit: gauntlet/cp-26 at 5671423b9e73ba8003a17ea9e8eae53332dcaa74, round 2's BLOCKED evidence tip, in the worktree .local/worktrees/cp-26/lead.
Round 2's candidate da7acf773a19d9f1781e7386189d626019c31ac3 is unreviewed. It changes only the rich-admin test's waits: controller 160 s, owners 200 s, ready 20 s.
main = origin/main = 647d6eb81b2cf6e0cfaf4152f659d689ff973578, untouched, with nothing staged.
No cp-26 tag exists.
Working tree: clean, apart from round 1's seven untracked run outputs. Leave them untracked and unchanged.
What already exists:
Round 2's finding, in docs/track-b/evidence/cp-26/landing-repair-2/checkpoint-return.md. With the waits fixed, the test still fails about 1 run in 4 under the emulation. Every failure is the admin job's two literal lock limits, telemetry["peak_hold_seconds"]<0.5 and telemetry["peak_wait_seconds"]<0.5. The worst peaks were a 0.89 s wait and a 0.73 s hold, and no run recorded a lock timeout.

The Orchestrator's check of that finding:

- Commit 1c89354 (2026-10-14, r14) wrote both literals. src/cp26/supervisor.py then had LEDGER_TIMEOUT_SECONDS = 0.5, so the literal meant "under the ledger timeout".
- r15's Owner-approved calibration (2026-10-16), which round 1's liveness repair cites, set src/cp26/limits.py to LEDGER_TIMEOUT_SECONDS = 3.0.
- In the same test, the controller-side helper assert_live_lock_telemetry already bounds wait_seconds, hold_seconds, peak_wait_seconds and peak_hold_seconds by S.LEDGER_TIMEOUT_SECONDS.
- The two literals are therefore stale r14 expectations, of the same kind round 1 repaired.

The Orchestrator's diagnostic. The setup was a scratch, history-free copy of the curated tree at f14a676b…, with round 2's test file from da7acf7 and the two literals replaced by S.LEDGER_TIMEOUT_SECONDS. It ran on Python 3.12 with PYTHONDONTWRITEBYTECODE unset, and was never committed.

| Load | Result |
|---|---|
| four burners | 8/8 pass, 20–28 s per run |
| six burners | 4/4 pass, 23–33 s |

Verify this yourself before relying on it, and report any material mismatch.

## Observable outcome
A new final candidate on gauntlet/cp-26. It has no Integration Critic: the Owner waived the Critic for this round on 2026-10-20 ("מוותר על ה־Critic בסבב 3"). The Orchestrator's own receipt re-runs items 1, 3 and 4 independently. The candidate shows:

- the rich-admin test passes under round 2's emulation and on a quiet machine;
- the workflow's full sequence is green on a history-free single-commit copy of the new curated landing tree;
- every scientific output is byte-identical to 6f57feb;
- the return gives the new curated tree's hash, its file count and its path list, for the Owner's LAND.

## Complete authoritative checkpoint bar
capstone_v21.md v21-r17 §24.7, all 111 clauses, already PASSed and unchanged. Round 1's brief (27d3e1af…) still holds. Round 2's brief (docs/track-b/evidence/cp-26/landing-repair-2-brief.md, SHA-256 cdef3247b23f4944cf56fcabff942aa295f834e1f5787b056b3ff98d4751e464) still holds, with its items 1 and 5 replaced by items 1 and 5 below. This brief's items are the bar for this candidate:

1. Item 1, as amended. The rich-admin test passes 5/5 times under round 2's emulation (four burners) and 5/5 on a quiet machine. Each run uses Python 3.12, a history-free single-commit copy of the curated tree, and PYTHONDONTWRITEBYTECODE unset.
   - The admin job's two lock limits change from the literal 0.5 to S.LEDGER_TIMEOUT_SECONDS, citing r15's calibration and 1c89354. Round 2's waits stay as they are at da7acf7.
   - Nothing else changes: S.SUPERVISION_POLICY and B.CAPS; every other assertion of the admin job: telemetry["timeouts"]==0, freshness, the 2.0 s observation window, at least three observations, and four running workers; every controller-side assertion; every file outside tests/.
2. No other test changes. Round 2's run of all 452 CP-26 tests under the emulation already holds. Rerun it once at the new candidate.
3. The workflow's seven steps are green on a history-free single-commit copy of the new curated tree, under Python 3.12 and 3.13. The full suite is also green on the curated tree by round 1's procedure.
4. Scope:
   - git diff --stat 6f57feb <new candidate> -- reports/ is empty;
   - git diff --name-only 04f00ea <new candidate> lists only tests/test_cp26_ledger_liveness.py and evidence under docs/track-b/evidence/cp-26/.
5. No Integration Critic, under the Owner's waiver above. The Lead runs items 1–4 itself, from a clean detached checkout of the new candidate, and records each command and result in the evidence.

## Task-specific supporting extract
The history-free copy, the workflow's seven steps, the emulation and the cleanup are exactly as in round 2's brief.
Load: state the ledger monitor's overhead, as round 2 measured it (about 0.6 core). Run nothing else heavy during timed runs.

## Applicable constraints
- No scientific computation: no search, fit, forecast, replay, scoring, bootstrap or report regeneration. Test runs only. Count their worker time in the existing ledger, without resetting it.
- No retrieval, no remote write, no network beyond uv sync from the lock.
- Files that never change: reports/, data/ and src/; the anchors and amendment records, AGENTS.md, the role files and the exposure ledger; the root pyproject.toml and uv.lock; every committed evidence file of the earlier chains and of rounds 1 and 2.
- The red line (v21-r13 §24.2): nothing dated after 2026-09-06 is read.
- Credentials follow AGENTS.md § Credentials; none is needed. Export MLFLOW_DISABLE_TELEMETRY=true and DO_NOT_TRACK=1.
- Commits: on gauntlet/cp-26 only; the first commit packages this brief as docs/track-b/evidence/cp-26/landing-repair-3-brief.md; round 1's verdict stays as integration.md, and as its preserved copy landing-repair/integration-PASS.md. This round writes no verdict.
- Checks: run scripts/gauntlet.py return on the return. Its expected problem, that no verdict cites the final candidate, follows from the waiver; state it in the return.
- Memory: do not open or edit the files in the Claude memory directory (~/.claude/projects/-Users-djourno-Downloads-PJM/memory/). Its auto-loaded index informs no decision.
- Owner-facing Git commands must be non-interactive: git --no-pager … and git commit -F <file>.

## Timebox
About 2 active hours from orientation to the terminal return.

## Owner-only actions already authorized
This round, under the Owner's instruction of 2026-10-19 ("אני מאשר לך לעשות הכל"). It covers local gauntlet/cp-26 commits and the brief's packaging.
Nothing else: no mainline operation, push, tag, publication, anchor edit or CP-28 work.

## Stop and return
Return exactly one of PASS / BLOCKED / INCOMPLETE, using templates §3.

The return carries:
- the new final candidate, the evidence tip and the evidence-only delta between them;
- the new curated tree's hash, its file count and its path list;
- the emulation results.

Name any interview-answer trigger in one line.
Do not begin CP-28. Do not commit to main, publish or push. Leave the branch and worktree for the Owner's LAND.
