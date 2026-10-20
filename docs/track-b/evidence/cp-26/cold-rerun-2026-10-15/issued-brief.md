# CP-26 Fresh Baseline Execution Brief for Apple M3 with Separate Run Accounting

You are the Track B Engineering Lead. Complete the new baseline: rerun v1-R through v5 over the entire frozen CP-26 population. Start a fresh scientific run instead of restoring the interrupted run. Prioritize producing the forecasts and baseline results. Do not turn this into a general recovery-framework project.

## Target

- Repository: `/Users/djourno/Downloads/PJM`, local execution only.
- Authorized checkpoint: CP-26, the existing checkpoint; a fresh run within it.
- Ratified plan anchor: `capstone_v21.md`, v21-r14, complete §24.7; SHA-256 `3be866bd10af02cc2b0b956ed91be660dca29a62c0b23b00997bf0b415d100c5`, anchor commit `332baeb861cec5a58516c58a29a1a3afe1eec909`.

Read `AGENTS.md`, `engineering-role.md`, the exact anchor and its supporting §§24.2, 24.4, 24.5, 24.8, 24.9 and inherited §§2, 14, 15, 16.2, 17, 23. The existing original and issued continuation briefs supply unchanged scientific details. Their later operational restore/additive-pricing assumptions are superseded only as stated here. Do not read `progress.md`, `orchestrator-role.md`, the syllabus or Track A/C material.

## Orchestrator-reported expected state

Verify these expectations before relying on them:

- Primary checkout: clean `main` at `647d6eb81b2cf6e0cfaf4152f659d689ff973578`.
- Existing Lead: `/Users/djourno/Downloads/PJM/.local/worktrees/cp-26/lead`, `gauntlet/cp-26`, tip `7b11c8cea6f0815a2034000325076238024f4122`.
- The prior run contains 42 terminal searches and 575 issued origins. Preserve it as historical evidence. Its two untracked exports, `reports/rebaseline/continuation-v21-r14-accounting-3/replay-state.json` and `learning-ledger.json`, are valuable state, not disposable scratch.
- The terminal ledger reports `65.16212464012295` cumulative machine-hours, including retained reserves, with no running jobs. Read the live ledger; never replace it with this snapshot.
- CP-26 remains incomplete and has no Integration PASS.

Reuse the existing branch and locked `/Users/djourno/Downloads/PJM/.venv`. Do not restart the checkpoint tool or create a replacement branch. Preserve existing artifacts and custody records in place; do not spend time repackaging the old run or generating another giant full patch during preparation.

## Observable outcome

Produce the complete new forecast ledger and baseline results for B0, v1-R, v2, v3, v4 and v5. The frozen CP-25 record currently reports **2,068 eligible measurement days** within 2,078 calendar days from 2020-12-29 through 2026-09-06. The Owner's approximate 1,926-day description is not an instruction to select a smaller population. Verify the exact keys/masks from CP-25; retain partial-day and DST rules. The existing calendar has 363 warm-up dates and 2,441 total origins.

First operational milestone: complete the nominal baseline forecasts. Retain the registered no-load and GFS+6 controls and all scoring/inference/reporting obligations required for final CP-26 completion. Prioritize execution order; do not silently delete plan requirements. v1 means the plan's v1-R recipe, with the released-v1 comparison handled as specified.

## Complete authoritative checkpoint bar

All of `capstone_v21.md` v21-r14 §24.7, every item, plus its cited supporting sections and the Owner's CP-25 rulings. The complete text is in the pinned anchor and is already preserved verbatim in `docs/track-b/evidence/cp-26/issued-continuation-brief-v21-r14.md`, SHA-256 `3e689e0cc3dda0cacf21103ce76da86ffa429af2c84ed8ce90c2e5417baa5c0c`. This brief does not reduce that bar. Use its complete checklist for the final return and obtain the exact verbatim excerpt for the final Integration Critic with `scripts/bar.py`.

## Execution priorities

1. **Start clean scientifically.** Give the new run an explicit identity and empty output, native-fit cache and replay-state directories under `reports/rebaseline/cold-rerun-2026-10-15/` and primary `.local/artifacts/cp-26/cold-rerun-2026-10-15/`. Recompute its searches, fits, warm-up and forecasts. Do not import the old ensembles, partial trial caches, fit caches, forecasts or H/learning state. Reuse unchanged source, frozen inputs, protocols and relevant validation/timing evidence. Check namespace isolation once and preserve old hashes.
2. **Price the fresh run before the full workload.** Calculate current cumulative spending once, plus all new work: 42 fresh searches, daily fits and replay across the entire calendar, persistence/supervision, registered controls, analysis, reporting, review and failure allowance. Use the plan's sealed training-only timing pilot and valid existing measurements where applicable. Earlier successful search jobs resumed partial work; their elapsed time alone is not the cost of 42 cold searches. Establish complete measured coverage or a supported conservative estimate. Include the new pilot's actual cost and growing state/export overhead. Preserve old estimates as history; do not carry an obsolete whole-run estimate and also add its completed actual costs.
3. **Admit only at a supported cumulative total of at most 388 machine-hours.** Before the full workload, complete the forecast described below and record an explicit admission PASS or BLOCKED. PASS means the conservative projected cumulative cost through CP-26 completion, including all historical spending and reserves, is **less than or equal to 388**; it never means permission to exceed 388. The new record may replace the old recovery-specific additive pricing floor and queues prospectively without altering historical charges or scientific rules. On PASS, proceed immediately and continuously through the authorized workload and final review without another per-stage Owner approval. If the total exceeds 388 or contains an unresolved material cost, do not start the full workload; return the numerical blocker.
4. **Train and forecast using the simplest existing viable driver.** Make only the ordinary implementation changes needed for a fresh namespace and reliable execution. Avoid hundreds of unnecessary full reinitializations. Persist normal chronological progress within this new run. Repair a demonstrated execution blocker narrowly; do not require a general identity-migration framework, exhaustive crash matrix or full-size synthetic recovery campaign before training.
5. **Verify proportionately and finish.** Reuse relevant passed tests/parity when their identities and behavior remain applicable. Run only affected checks for new changes and the plan's required gates. No mandatory separate repair Critic or repeated full-suite runs. Complete the full baseline evaluation and one fresh final Integration review once the artifact is ready; a changed candidate after FAIL still requires the appropriate new review.

## MacBook execution policy

The Owner requests maximum efficient sustained execution on the actual machine. Verified hardware on 2026-10-15: Apple M3 (`Mac15,3`), 8 physical/logical cores, 4 performance cores, 4 efficiency cores, and 17,179,869,184 bytes unified memory (16 GiB). This policy adds hardware scheduling instructions to this complete brief; it does not raise any CP-26 ceiling or alter the scientific protocol.

- **Keep useful work running.** Target four registered compute workers for independent work when memory and measured throughput permit. Keep the bounded work queue supplied and dispatch the next permitted task as soon as a slot is free. Do not wait for another chat turn or add arbitrary cooldowns between healthy jobs. Unattended computation may continue at any hour and on every day.
- **Prevent nested oversubscription.** Use one CPU thread per active fit: BLAS/OpenMP/NumExpr thread limits remain 1, and LightGBM/joblib use the fit worker's single-thread allotment. Four workers must not each create four or eight compute threads. A computing coordinator consumes a slot, and a registered pool root retains its reserved slot under the existing observer rules even while coordinating. Four simultaneous fits need an allocation that genuinely fits within four slots, such as four independent one-worker jobs; a pool root plus four children is not four workers. Supervision and accounting remain active under the existing allocation rules.
- **Exploit only legitimate parallelism.** Parallelize existing independent fits/search work where already supported, with deterministic seeds and ranking. Keep H updates, feedback consumption and forecast emission chronological for each policy/route. Do not change fit cadence, causality, numeric recipes or result ordering to increase CPU usage. Do not build a new distributed scheduler or change OS affinity/priority for this task.
- **Use the existing pilot efficiently.** During the required timing work, make at most a short relevant comparison of three versus four workers if both are viable. Choose the configuration with better sustained completed-work throughput, not the highest CPU percentage. Start with four only when available headroom supports it; otherwise use three and admit the fourth when safe. No separate benchmarking campaign is required. Use observed throughput and allocated worker wall time in the completion forecast.
- **Protect unified memory.** Aim for approximately 9–10 GB aggregate worker RSS (decimal GB) when system pressure allows, below the existing hard limit of **12,000,000,000 bytes**. Observe macOS memory pressure and increasing swap activity as well as process RSS. Bound prefetch/context copies. If pressure rises or measured throughput degrades under sustained thermal load, stop admitting extra work and drain toward three or two workers at safe task boundaries; recover toward four when healthy. Apply allocation changes through correctly declared monitored job boundaries; never retroactively reduce worker-wall charges or underdeclare a computing process. Do not kill a valid fit merely to adjust a soft target, disable swap/compression, or weaken the hard memory guard.
- **Run continuously under real supervision.** Use the existing detached, monitored execution mechanism so the run does not depend on an active model turn. Keep its existing `/usr/bin/caffeinate -i -w <supervisor_pid>` lifetime support; idle display sleep is acceptable. Do not change global power settings, bypass lid/power behavior, or create a new cron/LaunchAgent. The computer needs external power and an operating lid/display configuration for uninterrupted service; caffeinate is not a guarantee against lid closure, battery exhaustion, shutdown or OS restart.
- **Retain accountable progress.** Persist normal run checkpoints and logs without unnecessary full restarts or repeated whole-history exports. On a recoverable interruption, continue this new run only from a verified normal checkpoint under the same grant. A budget/ownership/data-integrity guard still stops execution. Do not automatically rerun failed model fits with replacement seeds or repeatedly retry an unresolved operational failure.

The default is sustained useful training, not intentional idle time. Adapting concurrency is ordinary execution authority within four workers and the same 388/485-hour limits. Preserve the current heartbeat, ledger and watchdog limits. Hardware observations are a snapshot, not reserved memory or proof that thermal throttling cannot occur.

## Separate run counter and complete pre-launch forecast

Register a unique cold-run ID and a verified live-ledger baseline before charging this new run's preparation or pilot. Maintain two clearly labelled views using the existing accounting mechanism:

- **New-run counter:** begins at **0.000 machine-hours** when registered. Attribute this run's setup, checks, pilot, training, searches, replay, analysis, reporting, review, failures and packaging to that ID. Show measured, reported and reserved components separately. Do not assign the old run's spending or retained historical reserve to this new counter.
- **Cumulative CP-26 counter:** retains all previous spending and reserves and adds every new charge. This is the authoritative account for the 485-hour hard ceiling and the historical component of the 388-hour projection test. Retain other attributable CP-26 charges if they occur; they do not disappear merely because they are outside the new run ID.

Do not create a competing resource ledger or a new accounting framework. Add the minimal run attribution and display needed to the existing verified account. Each real charge appears once in the cumulative total and, if attributable to this run, once in its separate view; these are two views of the same charge, not two charges. Preserve the baseline, original receipts and prior closed scopes. Existing historical costs are approximately 65.162 hours at the recorded snapshot; use actual live values at registration. This grant does not create an additional 485-hour allowance for the new run.

Before launching the full scientific workload, produce a complete, supported conservative forecast:

`projected cumulative completion = current cumulative charged total + all remaining cold-run work + remaining closure costs + additional justified contingency`.

The current total includes the new pilot and other already charged preparation, all earlier runs, reported time and retained reserves. Do not add any of those again. Price all 42 fresh searches, daily fits and chronological replay for all required origins/routes, warm-up, memory/worker scheduling, state growth, supervision and persistence, registered controls, scoring/inference/diagnostics, final report/draft packet, final Integration review, closure and failed-job/recovery allowance. List any reuse of timing evidence with its valid coverage; a resumed search-job runtime is not automatically a cold-search cost. Unsupported material costs prevent admission. Provide a compact component table, the conservative cumulative total, the separate new-run estimate and the expected wall-clock duration at the chosen MacBook concurrency. Reuse existing evidence rather than start an extra benchmarking campaign.

Record the forecast basis, actual cumulative balance and admission result before proceeding. With a supported conservative total **at or below 388 hours**, the Owner's grant below authorizes uninterrupted progression through all remaining CP-26 stages; no separate permission is required after the pilot, before training, between batches, or before analysis and final review. Routine valid checkpoints and safe concurrency changes remain within that grant. Continue to enforce the **485-hour actual cumulative ceiling** and all existing resource, ownership, data and scientific guards. An admission PASS is not permission to ignore a genuine guard failure or a material change that invalidates the approved forecast.

## Applicable constraints

The **388-hour cumulative projection gate** and **485-hour cumulative hard ceiling** remain unchanged. All old costs, failed jobs and the 2,826-second retained reserve stay in the authoritative ledger at `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26/ledger/budget.json`. A new run counter starts at zero, as specified below; the cumulative resource account never resets. The previously proposed eight-hour repair-only draft does not govern this fresh-run instruction; the old ten-hour repair allocation remains closed.

Maximum four concurrent workers, BLAS=1, CPU only, aggregate peak RSS 12 GB. Keep live time/memory enforcement, ownership checks, watchdogs and existing liveness limits. Register and charge worker compute, including tests, pilot, failures and review. Do not disable a guard to make progress. Use a minimal targeted fix if a real blocker prevents the simple run.

Zero retrieval and remote writes. All data reads use `cp25.guard`; no real market data after 2026-09-06. Frozen CP-25 keys, inputs, exclusions, issue time, training-target availability, seeds/search space, model recipes, H/CQR rules and scored fallback behavior stay unchanged. The CP-28 protocol remains frozen and no arm is executed. No tuning for favorable results.

Ordinary authorized writes: `src/cp26/`, `scripts/cp26*.py`, `tests/test_cp26*.py`, new cold-run outputs in the directories above, new evidence under `docs/track-b/evidence/cp-26/cold-rerun-2026-10-15/`, and operational ledger updates. Keep actual code/protocol identities truthful. Preserve all historical outputs, briefs and records. Do not edit landed member code, inputs, dependencies, anchors, amendments, governance/agent files, the exposure ledger or program state. No Lockdown suspension is granted.

## Timebox

Approximately **24 active hours**, including orientation through terminal return; unattended training is accounted in machine-hours. Work in the background within the monitored ceilings. Do not treat the timebox as permission to weaken a bar or exceed a resource cap.

## Owner-only actions already authorized

**Owner grant upon delivery:** I authorize the Engineering Lead to execute this fresh CP-26 baseline run, including necessary non-destructive local setup, minimal ordinary code changes, targeted checks, sealed timing/cost assessment, all fresh training/searches/forecasts, evaluation, reporting and independent final review. I expressly authorize a separate new-run counter beginning at zero while retaining every historical charge and the unchanged 485-hour cumulative ceiling. Complete and record the full pre-launch forecast. Once its conservative cumulative total is at or below 388 hours and admission is PASS, continue immediately and continuously without asking me for another per-stage permission. Serial local candidate/evidence commits on the existing `gauntlet/cp-26` branch and permitted isolated Builder/Critic worktrees are authorized. The Lead remains the sole Git writer.

This replaces the proposed restore/repair-only approach, not the ratified scientific plan. It authorizes retaining the previous run unused, not deleting it. No main write/commit, push, tag, publication, remote write, destructive history operation, governance edit or CP-28 execution is authorized. Credentials remain subject to AGENTS; no values may be inspected or emitted.

Preserve the exact delivered brief in the first local cold-run authority commit. Use `docs/track-b/evidence/cp-26/cold-rerun-2026-10-15/issued-brief.md` if that path has not already been issued; otherwise retain its historical bytes and save this revision as `issued-brief-separate-run-counter.md` beside it, with an explicit supersession record. Record the actual Owner delivery, starting tip, new run ID, zero initial run counter and verified cumulative baseline before this run's preparation/pilot compute. Preserve prior authority records and register the new output/cache identity explicitly. The new run must not accidentally dispatch the old restore queue.

## Stop and return

Execute toward the baseline, not another repair program. If the cost gate or a genuine scientific/authority prerequisite blocks execution, return the smallest precise blocker and preserve all work. A necessary locked-file change requires HALT and a new specific Owner suspension; do not prepare that edit.

When complete, designate `final_candidate_sha`, obtain the required fresh read-only Integration review in a new clean detached checkout, preserve its verdict and report the distinct `evidence_tip_sha` under engineering-role. Return PASS / BLOCKED / INCOMPLETE using templates §3 with the complete checklist, actual resources, Git/artifact identities and remaining risks. Show both the final new-run counter and cumulative CP-26 total, with the preserved historical baseline and admission forecast. Reuse existing records instead of repeatedly rebuilding giant handover packets. PASS requires the full current Integration PASS; an unfavorable scientific result may still PASS.

Keep main untouched and all work local. Preserve the old and new runs, account for any worktrees created, and leave the existing Lead/branch for the Owner's review and landing decision.
