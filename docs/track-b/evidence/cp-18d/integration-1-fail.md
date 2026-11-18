# Verdict — CP-18d — Integration — FAIL

- Candidate SHA: ebbf2cb1c59e1f4dc7673e46d19111c2cbfdf952 (`gauntlet/cp-18d`; base `main` = b866e6129e8872f606e6e06eb19f79522dad8508; 17 commits)
- Plan / version / bar: `capstone_v21.md`, revision v21-r20 (file SHA-256 80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6), §24.13 "The publication time (decision 22)" (section 39 lines, 2762 bytes, SHA-256 8b656f9ae608f63ef630fa12f02416f894d99ebd82aa4222d37193af61311f47); with the brief's other quoted bars (§24.13 "The catch-up (decision 23)", §24.13 "For CP-18", §24.14 "What stays exactly as registered", PUBLISH_RULES 1.5 A9), decision 31, and the Orchestrator's rulings O54 and O56.
- Verbatim bar excerpt:

> #### The publication time (decision 22)
>
> - **The information cutoff is unchanged:** D−1 11:00 Europe/Berlin, strictly before (§24.4).
>   - A run may happen at any time after the cutoff.
>   - Its payload holds only inputs published before the cutoff. So a later run issues the same forecast,
>     under the condition below.
> - **"Before the outcome"** in the frozen rules means without access to D's outcome, under the target-day
>   embargo (§24.4). It does not mean wall-clock time.
> - **Availability is judged by publication time against D's own cutoff, never by the run time.** The
>   tier register and the Owner's tier, margin and GFS rulings (§24.5) apply unchanged. This covers each
>   input and the GFS-availability flag (§24.12, decision 11).
>   - **For the live pipeline, CP-18 makes this verifiable** in one of three ways:
>     - each day's inputs are retrieved and archived by the cutoff;
>     - each input is taken from a source that preserves its vintage;
>     - for an input the tier register admits with reconstructed availability (tier 2), its documented
>       schedule.
>   - **A live day whose inputs cannot be shown this way is not issued,** and its cause is recorded.
>   - **4.7T's window keeps its registered vintage terms** (the protocol's §3, "Vintages").
> - **A delivery day is issued or not issued.** There is no "late" status and no "late" label.
> - **What stays recorded:**
>   - each issuance's actual run time, in its lineage (§16.2);
>   - the date of the last training, which the product's panel states.
> - **No public wording claims** that a forecast was published before the auction, or before its outcome.
> - **What this supersedes:**
>   - **§24.4's sentence** "The live product publishes its forecast before 12:00 local. CP-18 fixes the
>     schedule, its deadline and its failure rule; a late forecast is recorded as late." CP-18 fixes the
>     schedule and the failure rule. There is no deadline.
>   - **§16.2's "numeric origin/deadlines".** CP-18's brief fixes the origin and the cutoff, and no
>     deadline.
>   - **§16.4's CP-19 row,** where "count real timely forecasts and failures" becomes "count issued and
>     not-issued delivery days". CP-19's at least 90 consecutive delivery days count every day, issued or
>     not issued.
> - **§16.2's rule stands:** "Do not ... backfill a late forecast as timely". No forecast is labelled timely.
>   A catch-up issuance carries its own run time and relabels nothing.
> - **`AGENTS.md`'s daily-update exception needs no change.** It reads: "A failed or late day is published
>   as failed or stale, never skipped silently or backfilled as timely." Under this section:
>   - a day that is not issued is shown as not issued;
>   - the panel shows the date of its last training;
>   - nothing is labelled timely.

  (The excerpt is the citation. Any line number is a courtesy and is non-binding. Decision 31 supersedes the sentence
  "A live day whose inputs cannot be shown this way is not issued" for D's load forecast only.)
- Worktree clean before and after: yes (`/Users/djourno/Downloads/PJM/.local/worktrees/cp-18d/critic-1`, `git status --porcelain` empty and `HEAD` = ebbf2cb1… at the start, mid-review and at the end). The review spanned a usage-limit pause and a machine restart (2026-11-17 ~22:00 UTC to 2026-11-18 ~09:50 UTC); it continued from where it stopped.

## Commands actually run

`P=/Users/djourno/Downloads/PJM`, `W=$P/.local/worktrees/cp-18d/critic-1`. Every Python step exported
`MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1` and the five `*_NUM_THREADS=1`. Scratch output: `$P/.local/tmp/cp-18d/critic/`.
Critic probe scripts (outside the worktree): `/private/tmp/claude-501/-Users-djourno-Downloads-PJM/0769bd74-9f72-40a4-b83b-ce22e6ed11e8/scratchpad/`.

| # | Command | Exit | Observed output |
|---|---|---|---|
| 1 | `git show main:scripts/gauntlet.py \| python3 -I - critic-brief cp-18d` | 0 | this assignment |
| 2 | `git -C $W status --porcelain`; `git -C $W rev-parse HEAD` | 0 | empty; `ebbf2cb1c59e1f4dc7673e46d19111c2cbfdf952` |
| 3 | `shasum -a 256 $W/docs/track-b/evidence/cp-18d/issued-brief.md` | 0 | `d4fcc76a3c91d52d1558079f3a0d762c5f7f03378f1937289fa1d991e4dcadca` (as assigned) |
| 4 | `git show main:scripts/bar.py \| python3 -I - check $W/docs/track-b/evidence/cp-18d/issued-brief.md --source capstone_v21.md@ebbf2cb1… --source docs/PUBLISH_RULES.md@ebbf2cb1…` | 0 | five `ok`: lines 185–223 (2761 bytes), 227–243 (1100), 247–276 (1990), 280–295 (1160) in capstone_v21.md; 299–312 (832) in PUBLISH_RULES.md |
| 5 | `git show HEAD:<f> \| shasum -a 256` for the brief's 14 execution inputs (the five the round edits at `b866e612`) | 0 | all 14 equal the brief's table; capstone 80341681…, PUBLISH_RULES 1bc0c523… |
| 6 | `git show 1ae3dfbb:docs/track-b/evidence/cp-18d/issued-brief.md \| cmp - $P/.local/artifacts/cp-18d/issued-brief.md`; `git show --stat 1ae3dfbb` | 0 | byte-identical; the first commit adds that one file only; unchanged since |
| 7 | `cd $W && CP17_PROJECT_ROOT=$P PYTHONPATH=src $P/.venv/bin/python -m cp17.tools.refreeze verify docs/track-b/evidence/cp-17c/freeze-manifest.json` | 0 | `verified` |
| 8 | `git -C $W diff --stat b866e612 HEAD -- src/cp17 src/cp17c src/cp25 src/cp26 src/cp28 src/delu_forecast space space-wasm data live docs/index.html README.md docs/PUBLISH_RULES.md capstone_v21.md AGENTS.md progress.md .github/workflows/schedule-probe.yml pyproject.toml uv.lock reports/cp18c docs/track-b/evidence/cp-18c` | 0 | empty |
| 9 | `git -C $W diff --name-only b866e612 HEAD \| grep -Ev '<the brief's allowed paths>'`; `git ls-tree -r -l HEAD \| awk '$4>52428800'` | 1 / 0 | no path outside the allowed paths (62 files); no file over 50 MB (largest 30.8 MB, pre-existing) |
| 10 | grep of each changed path in `src/cp26/harness.py`, `tests/pres5_landed_code.py`, freeze manifests, `reports/cp18c`, `docs/track-b/evidence/cp-18c` | 0 | named only in CP-18c's historical records (verdicts, `scratch-tree-*.json`, `space-build-2026-11-12.json`), which record past builds and bind no current bytes; no pin |
| 11 | `python3 -I scripts/secret_guard.py pre-push origin x` (stdin: `refs/heads/gauntlet/cp-18d ebbf2cb1… refs/heads/x 0000…`) over the 17 commits no remote-tracking ref holds | 0 | no finding (values compared in-process, never printed) |
| 12 | `python3 $P/.local/artifacts/cp-18d/ci-runner.py critic ebbf2cb1… ci312 stress` (2026-11-17 20:57–21:34 UTC; the runner diffed against CP-18c's: paths and the commit message's checkpoint name only) | 1 | 01 leak-scan 0, 02 sync 0, 01a/01b 0, 03 `build_wasm_payload.py` 0 (119.6 s), 04 `pytest -q` **1**: `1 failed, 3527 passed, 79 skipped in 1986.53s`, the failure `tests/test_cp26_monitor.py::test_real_denied_detached_worker_never_reaches_computation` (`subprocess.TimeoutExpired` after 15 s); the runner stops at a failed step, so 05–08 and stress did not run. Machine load average was 37–44 on 8 cores (the Lead's own CI and stress, another session's Playwright, this review's bundle refit). |
| 13 | the same test file alone, in a `git archive` copy of the candidate (`CI=true`, `CP17_PROJECT_ROOT` hidden) and, as a control, of the base `b866e612` | 1 / 1 | the same one test times out at both commits under the same load (`1 failed, 24 passed, 3 skipped`); `git diff --stat b866e612 ebbf2cb1 -- tests/test_cp26_monitor.py src/cp26 scripts/cp26_rebaseline.py` is empty: environmental, not this candidate's |
| 14 | `python3 $P/.local/artifacts/cp-18d/ci-runner.py critic-2 ebbf2cb1c59e1f4dc7673e46d19111c2cbfdf952 ci312 stress` (2026-11-18 10:23:53–10:49:34 UTC, alone, after the Lead's stress run ended; machine load about 4) | 0 | tree 079306318781…, Python 3.12, history-free single commit; ci312: 01 leak-scan 0, 02 `uv sync --locked --dev` 0, 01a/01b 0, 03 `build_wasm_payload.py` 0, 04 `pytest -q` 0 (`3528 passed, 79 skipped in 838.55s`), 05 `test_10_cqr_order_statistic.py` 0 (8 passed), 06 `verify_release.py` 0 (`PASS — every bound claim agrees on every surface …`), 07 `test_22_wasm_equivalence.py` 0 (15 passed), 08 `publication_guard.py tree` 0, 08 stress collection 0 (22 collected); stress: `pytest -m stress -q` 0 (`20 passed, 3 skipped, 3584 deselected in 446.29s`); `complete: true`, scratch removed. Logs: `$P/.local/artifacts/cp-18d/critic-2-validation/` |
| 15 | `fetch_days.py` (read-only `gh api -H "Accept: application/vnd.github.raw" repos/hrsi56/delu-day-ahead-forecast/contents/live/inputs/days/<day>/{manifest.json,<body>}?ref=main`) for 2026-11-16, -17, -18, then `run_fac.py` (`cp18.live.history._Reader`, `market`, `fetched_after_cutoff` inside `cp18.boundary.live(now=2026-11-17T23:00:00Z)`, `PYTHONPATH=$W/src`) | 0 | each day has one load-forecast candidate, not admitted by decision 22; `fetched_after_cutoff` returns it, 24 hours, no NaN: **2026-11-16** with `load_forecast-entsoe-document-00@20261115T111708Zn0002`, fetched 2026-11-15T11:17:20Z (cutoff 2026-11-15T10:00Z), sha256 a8474c50…; **2026-11-17** with `…@20261116T204400Zn0003`, fetched 2026-11-16T20:44:06Z, 1acecebb…; **2026-11-18** with `…@20261117T193039Zn0003`, fetched 2026-11-17T19:30:54Z, f807090b…. The run record `live/store/runs/gh-44157659726-1.json` on `main` (= `origin/main` e4c26e1b) names exactly these records as each day's only reason. |
| 16 | `git archive main live/store`; `LiveStore(...).verify()` and `live_claims.live_record` with the candidate's code | 0 | verifies (last_day 2026-11-15); the five issued CP-18a–c days derive `before_cutoff` from their evidence; open 2026-11-16, -17, -18 (cause `inputs`) |
| 17 | `python3 -I $W/src/cp18/chain.py tick --store <main's live/store> --now <t>` for 2026-11-17T23:00Z, 2026-11-18T05:00Z, 2026-11-18T10:06Z | 0 | `run 2026-11-18` (a retry of the open target day), `run 2026-11-18`, `run 2026-11-19` |
| 18 | `cd $W && PYTHONPATH=src $P/.venv/bin/python -m cp18.schedule_probe measure --raw reports/cp18d/schedule-probe/raw-20261115T023528Z.json --raw …raw-20261115T112542Z.json --raw …raw-20261117T205258Z.json --workflow-file .github/workflows/schedule-probe.yml --out <scratch>`; `cmp` with `reports/cp18d/schedule-probe.json` | 0 / 0 | `measured 30 scheduled runs \| 3 probe days \| 0 missed \| 0 pending`; byte-identical to the committed file. Delays 370–622 min (6 h 10 min – 10 h 22 min), medians rising from 371 min (00:07) to 558–583 min (07:07–09:07); `macos-26` queue 0–604 s |
| 19 | `gh run list --repo hrsi56/delu-day-ahead-forecast --workflow daily.yml --event schedule` (read-only) | 0 | 2026-11-15's scheduled runs created 14:56:06Z, 15:43:30Z, 16:23:27Z, 17:22:45Z, 19:27:26Z (consistent with the report's 7 h 16 min and 7 h 23 min for 07:40 and 08:20) |
| 20 | `gh run view <id> --repo hrsi56/delu-pipeline-dryrun --json …` for 43670023047, 43670025084, 43708842868, 43708849112, 43735265261, 43735984719, 43735995024, 43736042543, 43736103411 (read-only) | 0 | conclusions, heads and jobs equal `reports/cp18d/rehearsal/rehearsal-runs.json` (failure / success / success / success / failure / success / cancelled / success / success) |
| 21 | `cp -R $W/live $S/live` (`S=$P/.local/tmp/cp-18d/critic/space`); `PYTHONPATH=$W/src:$W/tests python $W/tests/cp18d/fixture_after_cutoff.py --live $S/live --day 2026-11-14 --fetched 2026-11-13T10:21:07Z` | 0 | the copy relabelled, re-chained and verified |
| 22 | `python -m cp18.bundle --mode live --root $W --project $P --live $S/live --out $S/bundle --refit --no-retrieval --record $S/r.json` (as specified, no `--now`: as of 2026-11-17) | 0 | `bundle f16c49dd1216b7d9 stale as of 2026-11-17 \| latest issued 2026-11-15 \| publishable` |
| 23 | `python $W/scripts/build_product_space.py --bundle $S/bundle --out $S/dist --live $S/live --history $W/reports/cp18c/history-v1/files` | 0 | `built … \| publishable \| … \| history 805 files` |
| 24 | the same two steps for the unrelabelled copy (`$S/live-before` → `$S/dist-before`), then `PLAYWRIGHT_BROWSERS_PATH=$P/.local/tools/ms-playwright $P/.local/tools/playwright/bin/python -I $W/tests/cp18d/space_acceptance_d.py --dist after=$S/dist --dist before=$S/dist-before --scratch $S/acc --engines chromium,webkit` | 0 / 0 / **1** | `summary {'passed': 184, 'failed': 16}`: two checks fail in all 8 build×engine×width runs, both date-dependent (see R2 below) |
| 25 | steps 22–24 again with `--now 2026-11-15T12:00:00+00:00` on both bundles (`$S/bundle15-{after,before}`, `$S/dist15-*`, `$S/acc15`) | 0 ×4 / **0** | both bundles publishable with the **same** manifest `d12dca187cbc68e1…` (the label is not in the bundle's files); acceptance `{'passed': 200, 'failed': 0, 'not_run': 0}`, Chromium 153.0.8010.12 and WebKit 26.6, Playwright 1.63.0 |
| 26 | `alert_close.py` (the candidate's `cp18.alert.problems`/`alert` with the mocked issues API of `tests/cp18d/test_alert.py`, and `since` computed exactly as `alert.main` does) | 0 | a `not_issued` issue for 2026-11-16 stays **open** after 2026-11-17, -18, -19, -20 and -21 are each issued with all inputs before the cutoff; it closes only at the link after 2026-11-22, when 2026-11-16 leaves the 5-day `RECENT_DAYS` window |
| 27 | `alert_tick.py` (same harness) | 0 | an issue opened by a failed tick (`the chain: the tick job failed. Run: …`, no date) stays **open** after ten later healthy days: it can never close |
| 28 | `alert_key.py` (same harness) | 0 | 2026-11-16 issued with a copy fetched 2026-11-17T08:00Z opens the issue; 2026-11-17 then issued with the copy after the cutoff is **never reported** (`[]`, no comment): its date is already in the text as the earlier day's fetch time |
| 29 | `brew list --pinned`; `brew list --versions node` | 0 | `node`; `node 26.7.0` |
| 30 | `git -C $W status --porcelain`; `git -C $W rev-parse HEAD` (end, 2026-11-18T10:51Z) | 0 | empty; `ebbf2cb1c59e1f4dc7673e46d19111c2cbfdf952` |

## Evidence actually inspected

- The brief (`docs/track-b/evidence/cp-18d/issued-brief.md`), the relayed messages (`orchestrator-messages-as-relayed.md`: the
  2026-11-15 facts, O54, O56), the report (`reports/cp18d/report.md`), and `git -C $W diff b866e612 HEAD` for: `src/cp18/`
  `inputclass.py`, `live/history.py`, `live/build.py`, `live_inputs.py`, `inputs.py`, `live/acquire.py`, `live/archive.py`,
  `live/recorded.py`, `pipeline.py`, `store.py`, `bundle.py`, `evaluation.py`, `running.py`, `spaceglue.py`,
  `live_claims.py`, `acquire.py`, `__main__.py`, `claim.py`, `local.py`, `chain.py`, `window.py`, `alert.py`,
  `schedule_probe.py` (docstring and CLI), `runner_artifact.py` (docstring), `rehearsal.py` (docstring), `scratch.py`;
  `.github/workflows/daily.yml` (whole file); `scripts/build_product_space.py`; `space-product/app/main.js` (decision 31
  surfaces, the not-issued list); the CP-18a/c test diffs; `tests/cp18d/test_chain.py`, `test_alert.py` (whole),
  `test_workflow_d.py` (assertions), `test_claim_o47.py`, `test_controls_d.py`, `test_other_inputs_keep_d22.py`,
  `test_rehearsal_late_day.py`, `test_evaluation_sets.py`, `test_input_class.py` (names and docstrings),
  `fixture_after_cutoff.py`, `space_acceptance_d.py` (docstring and the two failing checks).
- `reports/cp18d/schedule-probe.json` and its three raw collections; `reports/cp18d/rehearsal/rehearsal-runs.json`.
- The built Spaces' `app/live-record.json` and `app/claims.json` (the labels, counts, both sets, the running sets 4/4/4 and
  5/5/5 (issued/scored/paired), `live_schedule`, no bare "A1", no `live_product_designation`), `history/index.html`'s added `og:title`, and the
  screenshots `after-chromium-1440-validation-per-day.png` and `…-validation-cumulative.png`.
- Not read: the Builders' hand-overs and the Lead's ledger (`.local/artifacts/cp-18d/builder-*.md`, `ledger.md`): the
  Builder's story, outside the Critic's inputs. The report's §5 points to the first of these for the proposed display.
  Disclosure: at 09:51Z a `pgrep -fl` of the machine's processes printed, unasked, the command line of another session's
  shell, which held a fragment of the Lead's ledger text (its own CI tallies). It was not used: every result here is
  from this review's own runs.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| O1a | Decision 31: when D's load forecast is not shown before the cutoff, a later retrieval is archived with its time, request and body, and v6 issues D through the frozen chain with that copy | PASS | `history.fetched_after_cutoff` (earliest complete live retrieval, not admitted, not strictly before the cutoff), used only for `p == day` and only when `market` admits none; `build._availability` names the class; `pipeline` unchanged around `cp17.daily`; commands 7, 15; `test_input_class.py`, `test_rehearsal_late_day.py` in command 14's suite |
| O1b | Every other input keeps decision 22's rule; a non-load-forecast input not shown keeps its cause and fallback | PASS | `test_other_inputs_keep_d22.py` (price refused, GFS only clears the frozen flag) in the suite; the rule's code path is `p == day` and `load_forecast` only |
| O1c | Within the lookback, a missed day is issued later with the late copy; never twice; never replaced; no copy leaves the day open with its cause | PASS | `test_controls_d.py` (issued twice, replaced: refused), `test_no_copy_at_all_is_no_copy`; command 15: the three open live days would be issued with their copies (2026-11-15T11:17:20Z, 2026-11-16T20:44:06Z, 2026-11-17T19:30:54Z) if a run reaches them inside the lookback |
| O1d | The label on the issued record, the store, the bundle and every Space surface; with the copy's retrieval time; never "late"/"timely" | PASS | `inputclass` (two classes; refusals); store write and verify refuse a missing label; the bundle refuses an unlabelled day and keeps the frozen schema (command 25: identical manifests for the relabelled and unrelabelled stores); acceptance 200/200 (command 25); no "late"/"timely" in any added public string |
| O1e | The evaluation reports before-cutoff days on their own and all issued days beside them, each with its count (O32, O33) | PASS | `evaluation.class_sets` (all-days set checked against the bundle's prospective window), `running(..., classes=)`; built record: sets 4 and 5 days, running sets 4/4/4 and 5/5/5; screenshots |
| O1f | CP-19's count: a late-copy day is issued and counted with its label | PASS | `LiveStore.days()` carries the class; `live_record['input_classes']` |
| O2a | The measurement from the probe's runs, at least three probe days, with its method | PASS | command 18: recomputed byte-identically; 3 days, 30 runs, 0 missed |
| O2b | The schedule reaches D's load forecast before the cutoff against the measured delays; waits in its job; every job inside 6 h; two acquisitions never write the same day; the idle-workflow rule handled | PASS | the chain (O54) does not depend on the scheduler while alive; tick ≤ 355 min (sleep ≤ 5.75 h), acquire stop-by 340 / timeout 355, run 150, others ≤ 20; one `daily-chain` concurrency group; keep-alive plus data commits; `test_chain.py` 60-day simulations; command 17 |
| O54-1 | Robust to a 12-hour delay or most events dropped; the design and its argument | PASS (with notes) | The argument holds while a chain lives; a broken chain waits for one seed, however late. Notes: a broken chain (a failed `next`) is not alerted, since the alert runs before `next`; the header's "a dispatch by hand acts at once" is not true while a link is in progress (by GitHub's one-pending-run concurrency rule, a hand dispatch queues behind a tick that may sleep 5.75 h and is cancelled when that link dispatches its successor; reasoned from the workflow, not observed); the chain keeps a Linux runner sleeping around the clock, a cost the Orchestrator may want to weigh against "nothing unrelated to the daily production run" |
| O54-2 | The alert: one issue per problem, `issues: write` only, text with day/cause/run link and no credential, **closed automatically once a later day issues with all inputs before the cutoff**, tested for open, comment and close | **FAIL** | Permissions and text: correct. Closing: commands 26–28. (a) an issue stays open while its problem day is within `RECENT_DAYS` = 5 of the target day, however many later days issue cleanly; (b) a failed-tick issue carries no date and never closes; (c) a day's key is matched as a substring of the issue text, so a later day whose date appears as an earlier day's fetch time is never reported. `test_alert.py` passes only because it hands `alert.problems` a `since` that `alert.main` never computes (e.g. `date(2026, 11, 18)` for a 2026-11-16 problem) |
| O3 | O47: a moved `main` touching none of the run's paths re-applies and pushes; never force-push; never outside `live/`; overlap refuses; a test reproduces it | PASS | `claim.publish`/`_reapply` (content and file set checked; `--porcelain` push, no `+`/`-f`); `test_claim_o47.py` (7 tests) in the suite; runner runs 43670023047 and 43708842868 re-applied over `docs/rehearsal/moved-main.md`. Note: `touched` uses `git log --name-only`, which lists no files for a merge commit's own changes |
| O4a | The two "A1" sentences: "v6 · DDNN-2 alone", "A1" only as "A1 in the frozen records"; the designation sentence removed | PASS | built `claims.json`: no bare "A1"; `live_product_designation` gone; `test_space_live.py` change stated |
| O4b | "Runs daily": where a surface says the product runs daily, it describes the schedule; the issued and not-issued days stay visible with their causes | **FAIL** | The Space's `live_schedule` (product panel and Forecast view) says: "each day GitHub's scheduler starts the acquisition several times before the cutoff, and the run after it with a retry; a job may start hours after its scheduled time, or not at all". That is the superseded gate design (f375f99a). In the chain the candidate ships, a scheduled event only seeds a broken chain; the acquisition and the run are started by the chain's own `workflow_dispatch` links, at once. The public sentence misdescribes the schedule. The days and causes are visible (acceptance) |
| O4c | v1's history page: the preview tags name v1 | PASS (open item) | `history/index.html` gains v1's own `og:`/`twitter:` tags, recorded with the inserted span; whether the host's injected tags precede them is visible only after a publication, as the report discloses |
| O4d | None of these changes a number | PASS | the bundle's files are unchanged by the label (command 25); the sets are computed from the served bundle |
| O4e | The runner's artifact holds the whole build apart from the deleted arrays, with the build's record | PASS | `runner_artifact` record/verify; `daily.yml` run job: record step before `*hashes`, upload with `include-hidden-files`; `test_runner_artifact.py`, `test_workflow_d.py` in the suite |
| O5 | The rehearsal: a normal day; a missed acquisition issued with the late copy and labelled; a moved `main`, records kept; the earlier acquisition's schedule and in-job wait; fake credentials, development days | PASS (with note) | command 20 and the record: 43708842868 (2026-08-31 before, 2026-09-01 after-cutoff copy, re-applied records, bundle publishable), 43708849112 (gate sleep 600 s, 9 polls), chain self-dispatch 43735984719… (one chain survives). Note: the pipeline rehearsals ran the tree of f375f99a (before the chain, 449e1017 and 56d76de7); the chain was rehearsed without work, so tick → acquire/run → alert → next was never run end to end on a runner |
| O6a | A negative control for each rule (five) | PASS | `test_input_class.py`/`test_other_inputs_keep_d22.py` (late copy for another input), `test_controls_d.py` (issued twice; replaced; label missing at build, write, verify; evidence contradicting the label), `test_claim_o47.py` (moved `main` touching own paths), all in the suite (command 14: all pass) |
| O6b | CP-18c's tests green; each changed assertion stated beside the test, only that assertion changed | PASS (with note) | every change carries a `CP-18d` comment; the stand-ins' class is a stated helper change; `test_workflow.py`'s `evaluate`/`selected` helpers changed with comments. Note: the rewritten two-year test now asserts the gate (`window.plan`) on the hourly events, which in the shipped workflow only seed the chain, so it tests a schedule that no longer runs |
| O7 | The packet's table | NOT CHECKED | in the Lead's return, after this review, by design |
| F1 | 4.7T stays exactly as registered; nothing the live product issues is 4.7T's | PASS | no 4.7T file, store or tool changed (command 8); no 4.7T run |
| F2 | A1 frozen: no frozen file, manifest, `src/cp17*` or freeze evidence changed; `refreeze verify` prints `verified` | PASS | commands 7, 8 |
| F3 | The red line: no research number, chart or choice uses data after 2026-09-06; the rehearsal on development days only | PASS | rehearsal inputs and `late_day`/`day` refused after 2026-09-06 (`test_workflow_d.py`); the boundary scanners in the suite; the live product is exempt (r20 §24.14) |
| F4 | Decision 22's other rules: the cutoff, judgement by publication time for every other input, run time in the lineage, no deadline | PASS | O1b; the day record keeps `run_started_utc`/`issuance_*`; the chain has no deadline, only retries |
| F5 | Critic and return per templates §§2–3 | PASS (this verdict) | written outside the worktree as assigned |
| C1 | Homebrew's `node` pinned and installed | PASS | command 29 |
| C2 | Credentials: none locally; never printed; fake ones in the scratch repository; telemetry off | PASS | command 11; no secret in any added test or tool; the alert and chain read `GH_TOKEN` in-process only and never print it (`test_the_texts_name_the_retrieval_and_carry_no_credential`) |
| C3 | Allowed paths only; none of the forbidden files | PASS | commands 8, 9 |
| C4 | No earlier evidence binds an edited file's bytes | PASS | command 10; the history-free suite's pin tests pass (command 14) |
| C5 | Tools: `gauntlet.py` flow; the Critic's assignment opens with the memory rule | PASS | the assignment's first line is that rule; this review did not open the memory directory |
| C6 | Owner-facing Git commands non-interactive | NOT CHECKED | they are in the packet (O7) |
| R1 | The history-free CI and `pytest -m stress` (reproduction 4) | PASS | command 14: every workflow step exits 0 and the stress tests pass. Command 12's single failure was a CP-26 timing test under a load average near 40; it fails identically at the base (command 13) and the candidate does not touch it |
| R2 | The Space (reproduction 9): `publishable`, the build, the acceptance in Chromium and WebKit | PASS (with note) | commands 21–25. With the bundle as of the review date (the reproduction as written), two checks fail in every run because `space_acceptance_d.py` expects the not-issued list and the day boxes from the store alone, while the page derives them from the bundle's `as_of_day` (`S.today`): a store copy two days older than the build lists 2026-11-16 and -17 as not issued and has no issued day in the today/tomorrow/yesterday boxes. With `--now 2026-11-15T12:00:00+00:00`, 200/200 pass. The acceptance script is date-dependent; the page behaves as CP-18c designed |
| R3 | The report: every claim checked, every disclosure present | **FAIL** | Accurate except: §2 "The alert … closed by itself once a later day is issued with all inputs before the cutoff" (commands 26–28 show otherwise). Its disclosures are present (the two rehearsal findings, pre1's scanner failures, the gate kept as a part, the stand-ins' helper change, the fixture, the unchanged README/report sentence, three pauses). Not disclosed: the Space's `live_schedule` still describes the gate. Minor: §2 gives the `macos-26` queue as "4 s to about 10 min" (measured 0–604 s); §5 points to an uncommitted hand-over |

## On FAIL only

- Single largest meaningful gap: O54's alert does not close or report as ruled, and its tests hide it: an issue stays
  open for up to five days after a later day issues with all inputs before the cutoff (`RECENT_DAYS` keeps the problem
  day "found"), a failed-tick issue never closes, and a later day issued with the load forecast fetched after the cutoff
  goes unreported when its date already appears in the issue as an earlier day's fetch time. Beside it, the Space's
  public `live_schedule` sentence still describes the superseded hourly-gate schedule, not the chain.
- Exact next acceptance test: a test that drives `cp18.alert.main` (its own `since`, from `--now`) over a store and a
  mocked issues API through consecutive links, and passes only if (1) a not-issued or after-cutoff issue closes in the
  first healthy link after a later day is issued with all inputs before the cutoff, (2) a failed-tick issue closes the
  same way, and (3) a later after-cutoff day is commented even when its date appears in an earlier day's fetch time; and
  the built live Space's `live_schedule` describes the chain (scheduled events only restart a broken chain; the
  acquisition and the run are started by the chain's own links), checked by `space_acceptance_d.py` with 0 failures.
