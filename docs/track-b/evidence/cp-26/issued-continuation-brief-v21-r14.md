# CP-26 Continuation Brief for Owner Ratification and Delivery

Deliver this entire document to the new Track B Engineering Lead. Preparing this brief does not ratify r14 or restart the experiment. The Owner's delivery of this document as an execution instruction grants the explicit authority stated below. This continues the existing checkpoint and the original Orchestrator-issued brief under research revision r14; do not open another checkpoint.

## Target

- Repository: `/Users/djourno/Downloads/PJM`, DE-LU day-ahead forecasting. Local execution only.
- Authorized checkpoint: CP-26, exactly one, continuing from the delivered candidate.
- Ratified plan anchor: `capstone_v21.md`, v21-r14, complete §24.7, subject to the Owner's ratification through delivery of this brief. SHA-256: `3be866bd10af02cc2b0b956ed91be660dca29a62c0b23b00997bf0b415d100c5`; anchor commit: `332baeb861cec5a58516c58a29a1a3afe1eec909`.

You are the Track B Engineering Lead under the original brief and this Owner addendum. Read `AGENTS.md`, `engineering-role.md`, the exact named anchor, and every supporting section cited by the original brief. §24.7 is governed by §§24.2, 24.4, 24.5, 24.8 and 24.9. Its inheritances are §2, §15.3, §16.2 and the generation specifications in §§14, 15, 17 and 23. Do not select an anchor by its filename's version number. Before the final Integration verdict exists, do not read `progress.md`, `orchestrator-role.md`, the syllabus, or Track A/C materials; they must not influence engineering decisions.

Amendment sheet: `docs/track-b/capstone_v21-r13-to-v21-r14-amendments.md`, SHA-256 `554a3aa4bf81f3fc1cc2319e624295570f919ff1fd4a6d9e2c9f56f8dcf6b79a`.

Controlling CP-28 protocol: `docs/track-b/evidence/cp-26/cp28-frozen-protocol-v21-r14.md`, SHA-256 `2b9286b0e948f59f97de33315a8b4fb3ef121003fc4ba82355b1ccf6585497a8`. It was frozen before any new r14 experimental training. CP-28 arm execution is outside this authorization.

Additional pinned sources:

- `docs/track-b/cp-25-rulings-2026-10-12.md`: `c7af67f88157277aafd8dd2b1b49e12a1d9ff4b747ca5bdf178fac664fba53c1`.
- `docs/PUBLISH_RULES.md`, revision 1.5, for a draft packet only: `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`.
- `reports/development-inputs/manifest.json`: `f3e8ca15e4466d371de5b6db9c181f77adaa8823ca2e7e0d325182120db32fd9`.
- `data/snapshot.parquet`: `7dd2dc73407706ca6bd3c1ad51d201ac0de35eec5ca129ce320cca639f697f00`.
- `docs/track-b/evidence/cp-26/issued-brief.md`: `5e16a134a9dd798733b0393f4f8e2570d03bf251471503d9292966e67e05214b`.
- `docs/track-b/evidence/cp-26/issued-repair-brief-v21-r14.md`: `5b6a0cdfad870da6b59a03ff29576ff6ec98891e941d56986516e6f3f743ff84`.
- `docs/track-b/evidence/cp-26/repair-v21-r14/active-documents.json`: `aa29af82181769afefdb0a4446057dd08f7ebafaac27a398aa2679397a3cadfe`.

Preserve every historical document unchanged. Where the old r13 search schedule conflicts with ratified r14, r14 governs. The repair brief's prohibition on resuming the experiment bounded the repair task that has ended; the new grant below covers continuation. The anchor's historical candidate header records its status when prepared. Record the Owner's ratification in a new authority record without modifying the ratified bytes.

## Orchestrator-reported expected state

The opening expectations were updated from the handover review on 2026-10-13. Verify them yourself:

- The primary checkout is clean on `main`, SHA `647d6eb81b2cf6e0cfaf4152f659d689ff973578`. Do not switch its branch or write tracked files there.
- The existing Lead worktree is `/Users/djourno/Downloads/PJM/.local/worktrees/cp-26/lead`, clean on `gauntlet/cp-26`, tip `fe4f2ea2aa1a64df8db404476a127bf7fe7f883a`, eight commits ahead of main.
- The reviewed repair candidate is `68d5db593e968c8dcff31c35ecccc355799ddd8e`. Source and protocols are unchanged between that candidate and the handover tip; subsequent additions are evidence and handover packaging. These are not the two terminal SHAs of an Integration PASS.
- CP-26 remains INCOMPLETE. The bounded repair is REPAIR_READY. The independent repair review and the reviewing agent's reproduction each passed 88 focused tests. Repair evidence includes 96 parity comparisons under the old settings and 42 search-support lists. These do not constitute an experimental run.
- The five worktrees created for the repair were removed; the Lead worktree remains. The reviewing agent created no refs. No active job remained after its supervised checks.

Before changing anything, verify Git topology, worktrees, tracked state, hashes, the runtime environment and the ledger. An intermediate LAND of the repair onto main is not required to continue this checkpoint. Reuse the existing Lead worktree. Do not rerun `gauntlet start`, recreate the branch, or reset the ledger. This paragraph supersedes the original brief's historical opening assumption that no CP-26 branch or code existed.

Use the locked environment at `/Users/djourno/Downloads/PJM/.venv`. Keep recovery material, caches, logs and new worktrees under the primary checkout's `.local/`. Preserve required evidence in approved durable paths on the candidate branch as well; disposable scratch must not hold its only copy.

## Observable outcome

Complete CP-26 under all of §24.7 and bind the final candidate to a fresh Integration Critic review. Deliver the forecast ledger for every policy and member at every warm-up and measurement origin; scores, uncertainty and stored replicates on all four masks; diagnostics and all registered breakdowns; the v2→v3→v4→v5 control audit; descriptive DDNN-2 and released-v1 holdout rows; the v5 no-load-forecast route; the GFS+6-hour route; parity evidence; the frozen CP-28 protocol; the report; and a local draft publication packet.

A result in which v5 does not improve on v4 is valid. Do not change methods in response to the results. Your checkpoint return to the Owner must summarize the generation transitions, the load-forecast bound, the GFS+6-hour result and fallback counts for the later CP-28 decision.

## Complete authoritative checkpoint bar

The complete §24.7 in the pinned r14 anchor is the acceptance bar. A convenience task list cannot reduce it. The full quotation at the end of this document is reproduced from the named anchor commit. Supporting sections, CP-25 rulings and the original brief remain controlling wherever this addendum does not supersede them.

## Task-specific supporting extract

The search phase is `2020-01-15 + 182k`, k=0..13: three routes, 14 searches per route. B is derived from the support mask and the minimum over all permitted held-out-week selections; it is not hard-coded. Expected reproduction is `[1,7,11,…,11]`, with `251/46` minima in the first window. Use 128 sampled trials, one fit per trial and batch, the r14 seeds, and exactly four distinct effective configurations with two seeds each. A failure does not authorize extra trials, replacement seeds, a subset ensemble, or an ensemble carried forward from an earlier search. Before S0, no native D2 forecast exists.

Keep four statuses separate: native-central validity, interval readiness, the source of the emitted/scored output, and eligibility for a complete-day own error. When insufficient H history is the sole fallback cause, a valid pre-outcome native central with its required issuance scale may contribute its own error exactly once after complete D−2 release. The emitted output remains B0 and remains counted as fallback. Copied fallback errors and member, solver, identity, required-scale or numerical H-construction failures do not enter H. B0 retains raw own errors; v1-R retains CQR, its embargoes and nine heads.

Distinguish CP-25 scoring keys, complete days eligible for H, and complete three-native-member days eligible for CP-28 learning. A partially eligible day remains scored on its frozen keys; do not invent an hour or an exclusion. Persist pending issuances, once-only consumption, issuance scales and buffers across warm-up/measurement, search boundaries, failures and restart, separately for each policy and route.

Preserve the CP-25 rulings: nominal retains the load forecast; no-load is the specified descriptive variant, with its own searches and H state; accepted structural shifts do not create extra routes; GFS+6 includes its 14 searches. Handle the two late GFS runs as missing under the frozen rules. Issue time remains D−1 11:00 Europe/Berlin, and the information boundary remains 2026-09-06.

For the historical A4 wording discrepancy in the CP-28 protocol, the specific rule and table govern. Before 364 eligible ledger days, A3=w0 and A4=A3. From 364 through 727 days, A4 uses learned A3. At 728 days, the registered block fit/shrink rule applies. The 364/728 native-ledger gates are separate from the 28 complete own-error days required by H. Do not edit the frozen protocol or execute a CP-28 arm to clarify this.

## Required preparation before experimental training

The full experiment connection remains unfinished; completing it is authorized. The Lead owns architecture and decomposition. Before any new search or training pilot, resolve both operational findings below and preserve meaningful tests of their behavior:

1. **Supervision must remain fresh.** `reconcile_running` currently accepts live monitor/supervisor identities without checking freshness, while the outer monitor waits for exit without checking heartbeat. In the reviewing agent's fixture, an hour-old heartbeat still admitted new compute. Add independent supervision of heartbeat and time/RSS accounting progress, with a defined startup grace period. A supervisor that remains alive but is stopped or wedged does not prove active supervision. Workers must not continue without measurement and cap enforcement. Block new work when supervision is not evidenced, and stop or reconcile only processes whose ownership is verified. Test a SIGSTOP or wedged supervisor with an active worker, launcher loss, shutdown, restart and PID reuse. Preserve request-hash, create_time and independent-receipt safeguards. Do not charge restart idle time as worker runtime or reconcile an unknown duration to zero.
2. **Closed repair accounting must stay closed.** `resource_summary()` currently computes `total - repair_baseline` even when `repair_scope.active=false`; new review charges consequently appeared as repair usage. Freeze a hash-bound terminal repair snapshot from the original evidence, preserve cumulative charges, and account for continuation separately. The original repair charge was `1255.047680753924` seconds; cumulative total at its handover was `4718.739437170931` seconds. Do not reactivate the repair allocation or treat its unused ten-hour allowance as new authority. Test that subsequent charges cannot change closed-scope fields and that historical charges and reserves are neither removed nor counted twice.

Run these tests through the existing monitor and ledger. Process tests must use dedicated processes you create; do not stop another task's process. If verification exposes a further defect in ordinary authorized source, fix and test it within scope without seeking permission for each file.

Before new experimental training, also complete the CLI and task scheduling/resume path. Use fixtures or stubs with proper identities to verify search→fit→forecast ledger→replay→scores/inference. Prove that the production search performs exactly one fit per trial/batch at the batch's first origin, trains only on prior information and forecasts the batch's 28 days without internal refits. Verify search/configuration/seed/input/protocol/code binding for every fit and cache, invalidation of failed members and searches, and equivalent state and forecasts between uninterrupted and resumed execution. Fixture results are not experimental findings.

Explicitly verify that the scoring keys and four masks supplied to the scorer match the frozen CP-25 records; a regenerated mask alone is insufficient. Verify the separation of partial scoring days, complete H days and complete native learning days, including DST. Before evaluation metrics, record all execution details the anchor requires to be frozen prospectively. A CLI flag cannot introduce a scientific method change. Existing parity is preserved evidence; changes affecting forecast/harness behavior or input identity require current parity before the full run. A parity failure requires stopping and reporting to the Owner.

## Applicable constraints

The cumulative ceiling remains **485 machine-hours** under the Owner's ruling. **388 machine-hours** is the projection stop line before the full run. Maximum four concurrent workers in aggregate, BLAS=1, CPU only, aggregate peak memory 12 GB; no cloud or GPU. A coordinator performing computation counts within the worker allocation. Register workers and establish time/memory measurement before computation begins.

The ledger snapshot after the reviewing agent's focused tests was `1885.5643742558896` measured seconds + `97.252` reported seconds + `2826` reserve seconds = `4808.81637425589` seconds, or `1.3357823261821917` machine-hours. Headroom at that snapshot was `483.6642176738178` hours. Subsequent work, including brief validation, can add charges; read the live ledger at startup. These figures do not authorize resetting it or reducing reserves. Ledger: `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26/ledger/budget.json`.

After preparation passes and before the full run, freeze the selection of 14 origins for a training-only timing pilot with evaluation scores sealed. Price **each of all 42 searches**: nominal/noload/gfs6 × k=0..13, with an identified measured or conservative basis. Price daily fits, parity, tests, bootstrap, diagnostics, and failed-job/resume costs too. Include historical measured time, reported time and all reserves. Fourteen daily origins do not estimate 42 searches. Any timing measurement must preserve the registered search space, sampler and seeds and include failed compute. Do not alter a search in response to evaluation scores. If total projected expense exceeds 388 hours, the CLI must actually stop and return the estimate and required decision; a JSON field alone is not an execution gate. Enforce 485 hours and worker/RSS caps throughout. No new compute is permitted with an orphan or unreconciled worker duration.

No retrieval: zero data bytes and zero remote writes. Route every data read through `cp25.guard`. Do not read or mention any market value or event after 2026-09-06. No credentials are needed; any potential use must obey AGENTS without exposing values. Disable telemetry as the original brief requires.

Authorized writable paths for this continuation are CP-26 source in `src/cp26/`, its CLI in `scripts/cp26*.py`, its tests in `tests/test_cp26*.py`, new CP-26 outputs in `reports/rebaseline/`, and new execution/evidence/return records in `docs/track-b/evidence/cp-26/`. Preserve repair outputs and historical evidence unchanged. Fixtures and recovery material under `.local/`, and operational-ledger updates through a controlled accounting mechanism, are authorized.

Do not change landed member code, `src/cp25`, `data/`, frozen inputs, prior results, root `pyproject.toml` or `uv.lock`, the exposure ledger, `progress.md`, anchors, amendment sheets, AGENTS/role files, publication rules or agent configuration. Dependency hashes remain those pinned in the original brief. A necessary locked-file change requires HALT with the exact file and text and an Owner decision. The previous suspension has ended; this brief grants no new Lockdown suspension.

## Timebox

Approximately **60 active hours** from continuation orientation to terminal return. Unattended runtime is charged to the machine ledger and is not active time. The cumulative ceiling and pilot stop line continue to apply; this timebox does not permit exceeding them. Local background computation is authorized with supervision, recovery checkpoints and local commits at stage boundaries.

## Owner-only actions already authorized

**Owner declaration upon delivery:** I, the project Owner, ratify for CP-26 the exact bytes of the v21-r14 anchor, the r13→r14 amendment sheet and the CP-28 protocol identified in Target. I authorize the new Engineering Lead to continue CP-26 on the existing branch from the handover tip, as a binding addendum to the original Orchestrator-issued brief. I authorize correction of both operational findings, completion of the experiment connection and tests, and the pilot and cost projection under the stated conditions. Once the conditions pass, I authorize the searches, training, replay, scoring, inference, reporting and full independent review. This covers all necessary non-destructive local actions within the named paths and ceilings, and local candidate/evidence commits on `gauntlet/cp-26`. Separate permission is not needed for each command or file within this scope.

This grant excludes CP-28 execution, publication, push, tags, remote writes, LAND, writes or commits on main, locked-file changes, and method or ceiling changes. Until the Owner delivers this document as an execution instruction, this declaration is proposed authorization only.

After Owner delivery, retain a canonical copy of this English brief under `.local/artifacts/cp-26/` and copy the same bytes to `docs/track-b/evidence/cp-26/issued-continuation-brief-v21-r14.md` in the first local continuation commit. Do not replace the original issued brief or repair brief. Preserve a new authority record naming the source of the Owner instruction, delivery time, hashes and document lineage. Update identity pins only through the harness's authorized mechanism and log every replaced pin. `CP26_EXPERIMENT_AUTHORIZED=1` may be set inside the consuming process only after this grant; the flag is not authority. The repair candidate SHA is not the new candidate SHA after preparation.

## Stop and return

Explain your approach briefly before changing files and report any material mismatch with expected state. Complete the authorized work; do not stop at a plan. Work directly or through bounded, isolated Builders under engineering-role. The Lead remains the sole Git writer. Declare every branch, worktree and cache created, its state and proposed disposition. Do not manage unrelated work or delete a ref.

When all outputs are final, designate the full `final_candidate_sha` and create a new clean detached checkout at exactly that SHA inside `.local/`. Launch a fresh read-only Integration Critic through `critic-open`, `critic-brief`, `critic-close` and the engineering-role protocol. It reviews all of CP-26 against complete §24.7 and its supporting sections, the frozen CP-28 protocol and exposure entries, without relying on a repair PASS or Builder summary. Check quoted extracts with `scripts/bar.py`. This is a new review, not a continuation of repair-review-attempt-2.

CP-26 PASS requires a complete current Integration PASS. Any repair after a verdict changes the candidate; the required review must bind the revised candidate. After the final candidate, the delta through `final_sha` is verdict-only under the return contract; do not include source or report changes in that delta. Validate the return with `scripts/gauntlet.py return`. Do not alter validators or governance contracts to make them pass.

Return exactly PASS / BLOCKED / INCOMPLETE using templates §3, with both terminal SHAs, the complete checklist, measured/reported/reserved resources, Git status, diff stat, full diff, touched files and reasons, limitations, retained local material and a proposed commit message. Declare exposure and interview-answer triggers in one line each; only the Orchestrator files those records. Fill Post-return reads honestly. Report fallback above 1% before CP-28; do not remove it from scoring. Record search/fit failures under the protocol without changing methods. A pilot projection over the stop line, parity failure, exposure or a required locked-file change requires stopping and returning the exact reason.

Leave the Lead worktree and branch for Owner review. Do not begin CP-28 or activate automatic publication. LAND and the decision to execute CP-28 belong to the Owner.

## Verbatim CP-26 bar

> ### 24.7 CP-26: the re-baseline on every development day (stage 6)
>
> **Purpose:** run B0, v1-R and v2–v5 daily on every eligible development day under one protocol.
> The result is the new all-season baseline, and a stored ledger of every member's out-of-sample
> forecasts for CP-28 and 4.7T.
>
> #### Days
>
> - **The scored calendar:** delivery days 2020-12-29 to 2026-09-06, 2,078 calendar days, less
>   CP-25's frozen exclusions.
> - **The warm-up:** delivery days 2020-01-01 to 2020-12-28, forecast the same way and never scored.
>   It only fills interval buffers and CP-28's first ledger.
> - **Four masks are reported separately:**
>   - every eligible day;
>   - the days never scored before (CP-25's mask);
>   - the old-fold days, folds 2–5, re-run under this protocol;
>   - 2026-04-08 to 2026-09-06, newly opened and used earlier by v1.
>
>   The old five-fold results, their S_MAE and S_WIS and their uncertainty stay as the historical
>   record, never overwritten.
>
> #### Policies
>
> - **B0,** the similar-day naive, unchanged.
> - **v1-R (728-day window, no hindsight regime flags):** the released v1 recipe, refit daily, with
>   two declared method changes:
>   - `crisis_period` and `post_crisis` are removed (§24.5);
>   - the training window is 728 days, where v1 expanded from 2019-01-01.
>
>   The rest of the recipe is the `base` catalog, the nine LightGBM quantile heads, CQR, and isotonic
>   ordering, laid out for each origin D as follows:
>   - the heads train on `[max(2019-01-01, D−728), D−62)`;
>   - day D−62 is an embargo;
>   - CQR calibrates on D−61 to D−2;
>   - day D−1 is an embargo.
>   - The thread count follows the worker's allotment; that is not a method change.
>   - **The released artifact** is reported descriptively, on its holdout days only: 2026-06-09 to
>     2026-09-06.
>   - If v1-R cannot be built without a further method change, CP-26 reports v1 through the released
>     artifact and B1's preserved vectors on the old folds, and says so.
> - **v2, v3, v4 and v5,** through the harness below: their landed member code, fixed blend weights,
>   interval layers, seeds and inner tuning rules, unchanged. Only the data identity, the boundary,
>   the weather source, the issue time and the calendar follow this section.
>   - **A tier-3 ruling** may name a variant, built only by the ruling's declared changes (§24.5).
> - **DDNN-2 alone** is descriptive in CP-26. It is a CP-28 arm (§24.8).
>
> #### The harness and the parity gate
>
> - **The harness.** The landed code refuses any snapshot, boundary or anchor other than its own
>   (`src/cp15/data.py`, `src/cp20/inputs.py`, `src/cp24/inputs.py`). CP-26 therefore builds a
>   harness that imports the landed member code unchanged and replaces only:
>   - the data identity: the new partition specification and CP-25's manifest;
>   - the boundary;
>   - the weather source: CP-20's grids plus CP-25's;
>   - the issue-time label;
>   - the identity pins: the protocol revision, the anchor and issued-document hashes, and the lineage
>     checks. Each replaced pin is listed in the harness log.
> - **The parity gate, before the full run.** Under the old settings (11:00 UTC, the old identity and
>   boundary), the harness reproduces the committed central vectors bitwise at sampled old-fold
>   origins:
>   - for A1, B2, A1_w, B2_w, L-N and L-R;
>   - for D2, on CP-24's committed ensembles. Those ensembles check parity only, and never serve a
>     CP-26 forecast;
>   - for B0, and for the assembled v2–v5 central vectors.
>
>   If parity fails, the Lead stops and reports.
>
> #### DDNN-2's training-only search, for CP-26
>
> - **Search dates:** S_k = 2020-01-15 + 182k days, for k = 0 to 13. Search k serves only the origins
>   from S_k up to the day before S_(k+1). Before S_0 there is no native D2 forecast.
> - **The batches:** consecutive 28-day blocks, tiling backward from S_k − 1.
>   - Among blocks starting on or after 2019-07-01, keep up to the 11 newest eligible blocks.
>   - Use exactly the landed DDNN-2 support mask, complete-calendar-week pool and 20% holdout-week
>     count, retaining its exclusion of the most recent seven days. Let N be the supported window
>     days and m the fixed held-out week count. Minimum training support is N minus the sum of the
>     m largest week supports; minimum holdout support is the sum of the m smallest. Accept only
>     minima at least 250 and 14 respectively. Eligibility must hold for every possible split.
>   - Lists depend only on support, are shared by every configuration in a search and are signed
>     before fitting. No seed, loss or convergence filters them. B is computed, never hard-coded:
>     the expected reproduction is [1,7,11,…,11], with first block 2019-12-18..2020-01-14 and minima
>     251/46. The algorithm and frozen inputs govern if a reported count disagrees.
>   - There is no fold skip rule: every block lies before the search's first origin.
> - **One fit per trial and batch,** on `[max(2019-01-01, b − 728), b)`.
> - **The sampler:** seeded with `SeedSequence([26, k, 0x5A3])`, with 128 trials. Successive halving,
>   the ranking metric and the tie rule follow §23.4.
> - **Frozen fit seeds:** trial/batch seed = `26_000_000 + k*100_000 + trial*100 + batch`,
>   trial=0..127 and retained batch=0..10, newest first. Ensemble member seed =
>   `26_000_000 + k*100_000 + 90_000 + 10*rank + repeat`, rank=1..4 and repeat=1..2.
>   These disjoint domains are fixed before fitting and shared across the three routes; no retries
>   with replacement seeds. Sampling space/priors remain the landed permitted space.
> - **The ensemble:** four best distinct effective configurations, two seeds each, exactly eight
>   members. Effective identity excludes trial id; in the no-load variant it also excludes removed
>   load flags. Duplicates consume trials; no extra sampling compensates for them. A configuration
>   failing a required batch cannot rank over all batches.
> - **Search failure:** zero eligible blocks or fewer than four valid effective configurations is
>   recorded. D2 is unavailable throughout that search's service period; the next search remains
>   on schedule. Never extend an earlier ensemble or relax a threshold. One failed daily member
>   invalidates D2 for that date: no median of a successful subset.
> - **CP-24's ensembles are never reused** for a CP-26 forecast.
>
> #### Training and information
>
> - **A daily refit** at every origin, for every member, on `[max(2019-01-01, D−728), D)`, filtered
>   by availability at the issue time. For every scored day the window is exactly 728 days.
> - **A training target enters only once its price was published** before the issue time.
> - **No expanding-window sensitivity** is run under the short path.
>
> #### Scores
>
> - **Primary:**
>   - p50 MAE, and the seven-quantile WIS (50/80/95% intervals, weights α/2, median weight 1/2,
>     divided by 3.5);
>   - each day's loss is the mean over its actual hours, and days weigh equally;
>   - the B0 ratio is the policy's mean daily loss over B0's, reported beside the raw losses.
> - **Secondary:**
>   - the mean of the four pooled-season ratios;
>   - the mean of the five complete-year ratios, 2021 to 2025;
>   - 2020 and 2026, both partial, reported separately; quarters descriptive.
> - **Calibration, descriptive:**
>   - 50/80/95% coverage, the lower and upper exceedance rates and the widths;
>   - quantile hits, and the eight-bin quantile histogram;
>   - Christoffersen's tests;
>   - the memo's moment-test family (HAC lag 14, 100,000 replicates, seed 20261013, Holm at 5%), as
>     a diagnostic only.
> - **Registered breakdowns:**
>   - season (DJF, MAM, JJA, SON);
>   - year and quarter;
>   - local hour;
>   - day type: weekday or weekend, the nationwide holiday flag, and 23-, 24- and 25-hour days;
>   - the 2021–2022 stress label, descriptive;
>   - two states known at the issue time:
>     - negative-price risk: any negative hour in the last 7 fully known delivery days;
>     - high volatility: the standard deviation of the last 28 fully known daily mean prices is above
>       the 90th percentile of the previous 365 such values, using linear percentiles and a strict
>       comparison;
>   - realized-outcome slices, descriptive only.
>
> #### Inference
>
> - **The bootstrap:**
>   - paired, non-circular moving blocks of 14 calendar days, 10,000 replicates, seed 20261012;
>   - drawn within calendar-year strata (the three 2020 days join 2021; 2026 is a partial stratum),
>     never across a real gap;
>   - studentized, with Bartlett HAC at lag 14.
> - **Sensitivity:** 7- and 28-day blocks, and an unstratified 14-day variant.
> - **Secondary tests:**
>   - Diebold–Mariano on daily losses;
>   - Giacomini–White, with these instruments: a constant, the lag-1 differential, a weekend flag,
>     and the two states above;
>   - the 90% Model Confidence Set, descriptive.
>
> #### Failures
>
> - **A failed fit or forecast** is scored, on that day, with B0's forecast as the policy's fallback.
>   Fallback days are counted and reported by policy.
> - **If B0's own inputs are also unavailable,** the policy fails that day. The failure is counted,
>   and the day is scored as missing in every paired comparison involving that policy.
> - **Separate four statuses on every date:** native-central validity, interval readiness, source
>   of the emitted/scored output, and eligibility of the issuance for a complete-day own error.
>   A valid native central and required issuance scale may be stored before its outcome even
>   when fewer than 28 complete released own-error dates force a scored fallback. Its own error
>   may enter once, after complete D−2 release. This applies in warm-up and recovery in measurement.
>   The emitted fallback remains scored and counted as fallback; never revise it retrospectively.
> - **This exception is only for insufficient interval history.** Member, solver, identity, required
>   scale or numerical H-construction failure admits no own error. Copied fallback errors, another
>   policy's errors and forecasts constructed after the outcome never enter. v2–v5 and variants
>   retain their landed H recipe and blend weights; gaps lengthen the represented calendar span.
> - **B0 retains raw own errors**, with no A1-scale requirement. Warm-up may issue central only.
>   In measurement, if its own valid quantiles are unavailable, B0 has no fallback to itself:
>   retain a missing output under paired-comparison rules while a valid pre-outcome native central
>   continues warming its own raw-error buffer. v1-R retains nine heads, embargoes and CQR;
>   it never substitutes an issued-error H buffer for CQR.
> - **If a main policy's fallback days exceed 1% of the calendar,** the Lead reports before CP-28.
>   Every main policy counts, including a tier-3 variant. Delay runs and the revision-contaminated
>   as-landed policies are reported separately.
> - **No day leaves the calendar** after scoring.
>
> #### What CP-26 claims
>
> - **It is a control audit.** For each adopted transition (v2 → v3, v3 → v4, v4 → v5) it reports
>   the paired differences, the ratio intervals and the year and season breakdowns, all
>   descriptive.
> - **No adoption, replacement or demotion follows from it.** If v5 does not improve on v4 over the
>   full calendar, the record says so, and the control (§24.5) stays CP-28's control.
>
> #### CP-28's frozen protocol
>
> - **Author and timing:** the CP-26 Lead writes it from §24.8, without inspecting any outcome, and
>   commits it on `gauntlet/cp-26` before CP-26 computes its first score.
>   The versioned r14 repair protocol is committed before any new search or training pilot;
>   the prior protocol remains historical, with hash-bound supersession recorded.
> - **Review:** CP-26's Integration Critic reviews it.
> - **Custody:** it lands with CP-26. If CP-26 is discarded, the protocol goes with it.
> - **The Owner's later confirmation** decides only whether CP-28 runs, never what it tests.
>
> #### The ledger
>
> Every forecast is stored with its issue instant, training-target cutoff, input vintages, seeds and
> code identity.
>
> Scoring keys permitted by CP-25, a complete canonical day eligible for an own-error buffer,
> and a complete three-native-member day eligible for CP-28 learning are separate predicates.
> A partially eligible day stays measured on its frozen keys, without an invented hour, but a
> partial issuance cannot supply a complete-day error. Full 23/24/25-hour DST dates can.
> Keep pending issuances, once-only consumption, latest released errors and original issuance
> scales continuously across warm-up/measurement, search boundaries, failures and restart.
> Each policy and route owns separate buffers and identity-bound caches. Report buffer counts,
> oldest/latest dates, span and age. No search transition resets this state.
>
> #### Ceilings, proposed
>
> - **400 machine-hours,** summed over workers' wall time, as CP-24's ledger defines it. This
>   includes the warm-up, the parity gate, the searches, the delay runs, the bootstrap, diagnostics,
>   tests and failed jobs.
> - At most 4 concurrent workers; BLAS 1; CPU only; peak memory 12 GB; no cloud and no GPU.
> - **The basis.** The first review projects about 150–165 machine-hours from measured costs per
>   origin.
>   - A run of the control costs about 29 hours of fits, and about 34 with its 14 searches (the second
>     review's reconstruction from CP-24's measured costs).
>   - Under §24.5's margin table, delay runs are expected to be few or none.
>   - **A tier ruling that adds a variant also sets the ceiling it needs:** each variant costs about
>     70–85 machine-hours, and the ruling records the new ceiling.
> - **A timing pilot comes first:** 14 origins, training only, with scores sealed. If it projects
>   more than 80% of the ceiling, the Lead stops and reports before the full run.
>   The current ruling's ceiling is 485 hours and stop line 388. A continuation pilot must price
>   all 42 searches across nominal/no-load/GFS+6, as well as daily fits, parity, tests, failed jobs,
>   bootstrap and diagnostics. Compare total projected expense including historical measured
>   time, reported time and retained reserves with 388; 14 daily origins alone do not price searches.
>   Do not reset the ledger. Unreconciled worker duration or surviving orphan blocks new compute;
>   restart idle time is not measured worker time. The repair itself authorizes at most 10 new
>   machine-hours within 485 and stops before real search, pilot, experimental replay or CP-26 scores.
>
> #### Outputs, gates and publication
>
> - **Outputs:** the ledger; the scores, and the uncertainty with its stored replicates; the
>   diagnostics; the report; CP-28's frozen protocol; and a draft publication packet under
>   PUBLISH_RULES §11.
> - **Gates:**
>   - CP-25's LAND;
>   - the Owner's tier and margin rulings (§24.5);
>   - the issued brief;
>   - the LAND.
> - **Publication:** CP-26's results may be published before 4.7T, under PUBLISH_RULES 1.5's
>   invariant 10. Publishing is a separate decision.
