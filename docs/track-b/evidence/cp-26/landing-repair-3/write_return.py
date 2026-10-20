from pathlib import Path
import json,re,subprocess
ROOT=Path('/Users/djourno/Downloads/PJM');LEAD=ROOT/'.local/worktrees/cp-26/lead';OUT=ROOT/'.local/tmp/cp-26-landing-repair-3'
D=LEAD/'docs/track-b/evidence/cp-26/landing-repair-3';R=json.loads((D/'verification.json').read_text());C=R['checks'];H=R['history_free'];P=R['preservation']
CAND=R['candidate'];ROWS=(D/'inherited-checklist.md').read_text()
rows=ROWS.split('## Complete §24.7 checklist\n',1)[1]
maptext=ROWS.split('## Preserved evidence map\n',1)[1].split('## Complete §24.7 checklist',1)[0]
waits={k:[x['timing']['owner_lock_peak_wait_max'] for x in C[k]['runs']] for k in ('stress-four','stress-quiet')}
number=lambda name:C[name]['steps'][2]['summary']
intro=f'''# Track B Checkpoint Return — CP-26 (landing repair, round 3)

## Status
PASS — under the Owner's explicit round-3 Integration-Critic waiver.

## Identity
- Repository: `/Users/djourno/Downloads/PJM`, DE-LU day-ahead forecasting; checkpoint CP-26, landing repair round 3 only.
- Ratified anchor: `capstone_v21.md`, v21-r17 §24.7, SHA-256 `{P['anchor_sha256']}`.
- Issued brief: `docs/track-b/evidence/cp-26/landing-repair-3-brief.md`; required-brief fields and the unchanged named bar were validated before editing. No material repository-state mismatch was found.
- final_candidate_sha: `{CAND}`. Every new engineering bar binds here.
- evidence_tip_sha: the branch tip after this return and its validation record are committed; its full SHA is supplied in the terminal return. A file cannot contain its own commit SHA.
- `git diff --name-only <final_candidate_sha>..<evidence_tip_sha>`: evidence-only; the full path output is supplied in the terminal return and retained in `.local/artifacts/cp-26-landing-repair-3/evidence-only-delta.txt`.

## Repository state
- Existing branch: `gauntlet/cp-26`, retained for the Owner's LAND; no shared-repository branch or tag was created. Ahead/behind counts and the final tip are supplied in the terminal return.
- Lead worktree: `/Users/djourno/Downloads/PJM/.local/worktrees/cp-26/lead`; no tracked dirt at handover. The same seven untracked run-output groups remain untracked and unchanged: fresh SHA-256 and size comparisons matched all {P['untracked_preservation']['files']:,} files / {P['untracked_preservation']['bytes']:,} bytes against the starting manifest.
- Created for this round: `.local/tmp/cp-26-landing-repair-3/final-check` (new clean detached checkout at the final candidate), and `.local/tmp/cp-26-landing-repair-3/prepared/curated` (detached at main, with only curated candidate paths staged). Both are removed after verification; final evidence-tip curation uses the isolated-index procedure already checked against this actual curated worktree.
- Created history-free scratch repositories: `.local/tmp/cp-26-landing-repair-3/prepared/copy312` and `copy313`, each one commit on its own local `main` branch (`copy312/main`: `{R['scratch_branch_heads']['copy312/main']}`, `copy313/main`: `{R['scratch_branch_heads']['copy313/main']}`), no tags, tree `{H['tree']}`. Removed at cleanup, together with all fresh test environments, test temporary directories and four burners. No other existing worktree is removed.
- Reused the existing `.local/cache/uv`; only locked dependency syncs were used; one allowed network sync populated the missing Python 3.13 wheel in that project-local cache. Retained recovery: the hash manifest for the original untracked files, Git/diff/curation checks and this round's run records in `.local/artifacts/cp-26-landing-repair-3/`; ordinary monitor receipts remain in the existing CP-26 ledger/artifact directory.
- Local `main` and `origin/main` refs remain `647d6eb81b2cf6e0cfaf4152f659d689ff973578`; main's index is empty. Nothing pushed, published, tagged or landed.

## Complete checklist with direct evidence
The following table carries **all 111 original §24.7 clauses separately**. Their scientific PASS at `6f57febe3659b1f902c17f3db31ba41e41136178` and r17 preservation PASS at `f014e5b2f09dc7defa103b3c4ec5796d199c262d` are inherited, not reissued by this Lead. This round performs no scientific computation or new scientific review.

Current preservation evidence is `verification.json`: the reports delta from the scientific candidate is empty; src/data and protected files are unchanged in this round; all previous evidence is unchanged; preserved verdict blobs/hashes and cited candidates are retained. The complete §24.7 bytes have SHA-256 `d5079dad269d321b3373cc2757a0cf28ce6e7f0637a2b18c53c06ef1fed1efae` at all four candidates. R1/R2/R16 and P1–P11 below refer to the **inherited** r17/scientific checks, not newly run scientific work. The original 33,949-payload custody/selected hash checks are not claimed as fresh checks in this round.

{rows}
### Direct locators for the inherited evidence
{maptext}
### Round-3 repair criteria

| # | Checklist item | Status | Direct evidence |
|---|---|---|---|
| R1 | Rich-admin passes 5/5 with four burners and 5/5 quiet; Python 3.12; one-commit curated copy; bytecode allowed | PASS | `verification.json` checks `stress-four` and `stress-quiet`; raw per-run logs in `logs/`; exactly five successes each, zero owner lock timeouts in all ten. |
| R1a | Only the two stale admin lock literals change, citing r14/r15; round-2 waits and all other assertions stay | PASS | `git diff 5671423 {CAND} -- tests/test_cp26_ledger_liveness.py`; two `<0.5` comparisons become `<S.LEDGER_TIMEOUT_SECONDS`, plus a provenance comment. Ready/controller/owner waits remain 20/160/200 s. S.SUPERVISION_POLICY, B.CAPS, freshness, timeouts==0, the 2.0 s observation window, >=3 observations, four workers and every controller assertion are unchanged. |
| R2 | No other test changes; rerun all 452 CP-26 tests under the emulation | PASS | `verification.json` `cp26-four`: {C['cp26-four']['run']['summary']}; `logs/cp26-four.log`. |
| R3 | Workflow's seven steps on the history-free curated tree under Python 3.12 and 3.13 | PASS | `verification.json` `ci3.12` / `ci3.13`, seven exit codes 0 each; suites: {number('ci3.12')}; {number('ci3.13')}. The standalone `python3` guard runs with each environment's bin directory first on PATH, as recorded in `resume.py` / `resume2.py`; both interpreter versions are recorded in their sync results. |
| R3a | Full suite by round 1's curated worktree procedure, and on the full clean candidate | PASS | Curated: {number('curated')}. Full candidate: {number('full')}. `verification.json` and `logs/curated-suite.log`, `logs/full-suite.log`. |
| R4 | Scientific output and mutation scope | PASS | Empty `git diff --stat 6f57feb {CAND} -- reports/`; `git diff --name-only 04f00ea {CAND}` lists only this liveness test and CP-26 evidence. Protected round-3 scopes and prior verdicts retain their blobs. |
| R5 | Owner-waived Critic; Lead checks from clean detached final candidate | PASS | Brief's exact waiver, “מוותר על ה־Critic בסבב 3”; clean detached `final-check` at `{CAND}` before/after checks. No verdict written. The Orchestrator's independent receipt is still to come. |
| C1 | Curated tree identity and path list for LAND | PASS | Verified candidate tree `{H['tree']}`, {H['tree_files']} files, {H['curated_paths']} curated paths; `candidate-curated-paths.txt`. `curated-paths.txt` names the final evidence-tip LAND delta paths, and `tree-paths.txt` lists every file in that tree; final tree hash/count are given with the evidence-tip SHA in the terminal return. Excluded paths: {H['excluded_paths']}; exclusion-rule SHA-256 `7cbd68734f864d78a076800ecb1db273a8b8e50ba00f0bf79b76d24ac72af565`. |

## Integration verdict
- **No new Integration verdict**, as explicitly waived by the Owner for this round. Lead verification is reported as Lead verification.
- `docs/track-b/evidence/cp-26/integration.md` remains round 1's PASS, binding `04f00eac5506c550ed4c775b84dc65a41f86c007`; it and `landing-repair/integration-PASS.md` retain SHA-256 `240378b707b822e9722ba0662eff60d0203ac16f1a333c0e47e090c76a55d36f`.
- Preserved scientific verdict: `cold-rerun-2026-10-15/integration-final-r16-2-PASS.md`, SHA-256 `32fc2af7eef6c030d4a0763c0d2cf3c55d8ed0cc4f4b2428192e9e638f413725`; r17 verdict: `gfs-v21-r17/integration-r17-PASS.md`, SHA-256 `dcde05541851efa5dc9f38ba208ded5bb3c52f150f33650899a8a2087e44c6e8`.
- `python3 scripts/gauntlet.py return cp-26 {CAND} <evidence-tip>` returns exit 1 with **one expected problem**: `the verdict's Candidate SHA line does not cite the final candidate in full`. That follows from the waiver; the preserved round-1 verdict must not be relabelled. No other problem is accepted. Actual output is in `gauntlet-return-check.txt` and the final local receipt.

## Reproduction
The exact commands actually run, working directories, exit codes, durations, interpreter versions and step outputs are in `verification.json`; `run.py` records the initial batches; `resume.py` continues after the contained-temp correction and `resume2.py` continues after the allowed Python 3.13 cache fill; `check.py` prepares the curated tree and runs round 1's suites, and the immutable round-2 `stress_check.py` supplies stress/selection/CI commands. Raw output is in `logs/`.

Starting in this project's Lead worktree after the temporary directories have been removed:

```sh
git --no-pager worktree add --detach /Users/djourno/Downloads/PJM/.local/tmp/cp-26-landing-repair-3/final-check {CAND}
python3 /Users/djourno/Downloads/PJM/.local/tmp/cp-26-landing-repair-3/final-check/docs/track-b/evidence/cp-26/landing-repair-3/check.py prepare --candidate {CAND} --out /Users/djourno/Downloads/PJM/.local/tmp/cp-26-landing-repair-3/prepared
/Users/djourno/Downloads/PJM/.venv/bin/python -B docs/track-b/evidence/cp-26/landing-repair-3/run.py
# The recorded initial workflow exposes the contained-temp discovery issue described below.
/Users/djourno/Downloads/PJM/.venv/bin/python -B docs/track-b/evidence/cp-26/landing-repair-3/resume.py
# After the recorded missing-wheel stop, fill from the lock and finish all remaining checks.
/Users/djourno/Downloads/PJM/.venv/bin/python -B docs/track-b/evidence/cp-26/landing-repair-3/resume2.py
```

All test batches use `scripts/cp26_rebaseline.py monitor --workers 4`, the existing ledger, telemetry opt-outs, BLAS threads 1, CPU only, and no network except the separately recorded `uv sync --locked --dev` cache fill. Test child environments remove inherited CP variables, PYTHONPATH, VIRTUAL_ENV and PYTHONDONTWRITEBYTECODE, point CP26_PROJECT_ROOT to an absent path, and choose a fresh UV_PROJECT_ENVIRONMENT for each interpreter/CI suite. Every original test and other assertion is retained. The two scratch commits used the mandatory secret hooks and `git commit -F`; no guard was bypassed.

The four-burner emulation also includes the existing production-ledger monitor. Its supervisor/watchdog overhead was measured by **round 2**, at about **0.6 core**; this round does not claim a new measurement. No other heavy task was launched alongside the test batches. Four-burner rich-admin test-call times: {min(x['test_seconds'] for x in C['stress-four']['runs']):.3f}–{max(x['test_seconds'] for x in C['stress-four']['runs']):.3f} s; quiet: {min(x['test_seconds'] for x in C['stress-quiet']['runs']):.3f}–{max(x['test_seconds'] for x in C['stress-quiet']['runs']):.3f} s. {"The loaded test-call range agrees with the supplied diagnostic's 20–28 s range." if all(20 <= x['test_seconds'] <= 28 for x in C['stress-four']['runs']) else "The actual loaded test-call range is stated above; timing is reported, not used to loosen an assertion."} The first fresh-environment **whole command** took {C['stress-four']['runs'][0]['seconds']:.2f} s (pytest reported `{C['stress-four']['runs'][0]['summary']}`), including initial process/import/collection overhead; later whole commands took {min(x['seconds'] for x in C['stress-four']['runs'][1:]):.2f}–{max(x['seconds'] for x in C['stress-four']['runs'][1:]):.2f} s. Thus the diagnostic's 20–28 s range matches the warm whole-command runs and the test-call durations, while the cold whole-command overhead is a recorded timing difference. The test still passed without a harness or lock timeout.

**Contained-temp correction and preserved failed run.** The first Python 3.12 workflow suite recorded `{C['initial_ci3.12_failure']['steps'][2]['summary']}`: `test_the_hook_never_fails_outside_a_repository`. Its temporary plain directory was physically inside PJM under the required project-local TMPDIR, so Git discovered PJM instead of reaching a non-repository boundary. The test strips every GIT_* variable, so a ceiling variable cannot fix that fixture. No source, test or locked hook changed. `resume.py` exclusively creates a disposable `.git` file only at the dedicated TMPDIR root, pointing to an absent gitdir, outside every real checkout. Git then has no discoverable valid repository there; the same hook error-handling assertion runs, with an invalid-gitdir diagnostic rather than the usual filesystem-root diagnostic. All four hook tests pass (`{C['hook-boundary']['run']['summary']}`); all later full suites include the unchanged hook tests. The initial failure, corrected rerun, barrier bytes/path and every charge are preserved in `verification.json` and logs. The barrier and temp directories are removed in cleanup.

**Locked-cache correction.** Python 3.13's first offline sync stopped before tests because this project-local cache lacked its pinned llvmlite wheel. The brief permits `uv sync --locked --dev` network access. `sync313.py` performed exactly that sync, with Python downloads disabled and the cache kept inside this project; the complete Python 3.13 workflow then ran offline in a separate fresh environment. The initial sync failure, allowed cache-fill command and corrected seven-step results are all retained. No dependency version, pyproject.toml or uv.lock changed.

The historical attribution was independently checked read-only: full `1c8935404b7d13e74556ef5f7cf67de846803f98` wrote both literals while supervisor.py defined 0.5 s; `a57aba55b79d48895bf1baa3362172e98f05c32c` introduced limits.py's 3.0 s calibration. The controller helper already bounded all four lock metrics by S.LEDGER_TIMEOUT_SECONDS. This is a stale expectation repair under the existing policy.

## Files changed
- `tests/test_cp26_ledger_liveness.py`: the two calibrated lock comparisons and their provenance comment; the full test diff is six lines (+4/-2).
- `landing-repair-3-brief.md`: packages the issued round-3 authority in this round's first commit.
- `landing-repair-3/check.py`: reproducible curated/history-free construction and round-1 suite procedure, retaining secret hooks.
- `landing-repair-3/run.py`, `resume.py`, `resume2.py`, `sync313.py`: exact serial supervised commands and interpreter-specific final guards.
- `landing-repair-3/verification.json`: every current test/command result, ledger charge, tree identity, preservation checks and inherited verdict hashes.
- `landing-repair-3/candidate-curated-paths.txt`, `curated-paths.txt`, `tree-paths.txt`: tested-candidate and final-evidence-tip curation path lists.
- `landing-repair-3/inherited-checklist.md`: the complete inherited 111-clause mapping and exact evidence locators, also embedded above.
- `landing-repair-3/logs/*`: raw command output, labelled by batch, run and step.
- `landing-repair-3/curate.py`, `collect.py`, `write_return.py`, `cleanup.py`, `cleanup-finish.py`: exact curation and preservation/return procedures.
- `landing-repair-3/cleanup.json`: actual cleanup and final repository-state receipts; a Finder .DS_Store creation race interrupted the first temp-directory removal and the bounded retry completed it. Both detached worktrees, all environments/copies, the discovery barrier and the temp root are removed.
- `landing-repair-3/checkpoint-return.md`, `gauntlet-return-check.txt`: this return and its mechanical validation, with the explicit waiver exception.

The final `git status --porcelain=v1`, `git diff --stat`, complete round-3 diff, touched paths and evidence-only delta are retained in `.local/artifacts/cp-26-landing-repair-3/` and linked in the terminal return. Earlier committed evidence is unchanged.

## Elapsed
About 1.5 hours, to the nearest half hour, against the approximately 2-hour timebox.

Test time charged without resetting the ledger: {R['ledger_delta_seconds']:.3f} machine-seconds ({R['ledger_delta_seconds']/3600:.3f} h), across {len(R['ledger_jobs'])} monitored jobs, indices {R['ledger_before']['jobs']}–{R['ledger_after']['jobs']-1}. Cumulative total: {R['ledger_before']['total_seconds']/3600:.3f} → {R['ledger_after']['total_seconds']/3600:.3f} of 500 h. The failed initial suite and failed offline Python 3.13 sync are included in this charge. No running job or new unreconciled duration remains. Burners were stopped, all four PIDs are gone; their {R['burners']['burner_seconds']:.2f} burner-seconds are recorded separately as emulation load, as in round 2.

## Open risk or exact owner action
No further engineering action is needed for this round. The Owner retains LAND/publication authority; the Orchestrator's receipt independently reruns the required items. This return is a local macOS reproduction using Python 3.12/3.13 and the specified CPU emulation.

Interview-answer trigger: why did longer harness waits still leave CI flaky? We traced the remaining failures to r14's literal 0.5 s assertions after r15 had calibrated the unchanged production ledger timeout to 3.0 s, then verified the constant-based assertions with unchanged supervision and scientific outputs.

## Landing report
- Proposed disposition: LAND, using the curated evidence-tip tree supplied in the terminal return; all round-3 bars are green under the explicit waiver.
- Evidence tip to preserve: the full SHA in the terminal return; leave `gauntlet/cp-26` and its existing Lead worktree for the Owner.
- Live documents citing this branch: inherited round-1/round-2 accounting names `progress.md:111`, plus locked `capstone_v21.md:4368`. This list was **not refreshed** by reading orchestration material. Repointing and reclamation are left for the later authorized disposition procedure.
- Proposed commit message: `CP-26: land the re-baseline and calibrated landing-test repairs`.

## Post-return reads
None. No progress.md, syllabus, Track A/C material, orchestrator-role.md or Claude project memory was read; no next-checkpoint work was planned or begun.
'''
intro=re.sub(r'(?<![-\w])git (?!\-\-no-pager)', 'git --no-pager ',intro)
(D/'checkpoint-return.md').write_text(intro)
print('Return contains',len(re.findall(r'^\| \d+ — ',intro,re.M)),'scientific clause rows')
