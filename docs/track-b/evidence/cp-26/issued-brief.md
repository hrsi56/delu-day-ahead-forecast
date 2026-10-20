# Track B Checkpoint Brief — CP-26 (the re-baseline: B0, v1-R and v2–v5 refit daily on every development day to 2026-09-06)

*Issued by the Orchestrator on 2026-10-12, Asia/Jerusalem.*

## Target
- Repository: DE-LU day-ahead forecasting, `/Users/djourno/Downloads/PJM` (origin
  `hrsi56/delu-day-ahead-forecast`). The checkpoint runs locally, in the Lead's own worktree.
- Authorized checkpoint: CP-26, exactly one.
- Ratified plan anchor: `capstone_v21.md`, revision v21-r13, §24.7, SHA-256
  `173799d818387b9d82db16b9ccd7195afaebbea8e11259809e4a8b704bd525a8`, ratified at
  `d58486da826b337bd58f469e122315c3142e360b`.
  - §24.7 is governed by:
    - §24.2: the boundary, the guard and the exposure ledger;
    - §24.4: the issue time;
    - §24.5: the tiers and the margin rule, as the Owner ruled them (below);
    - §24.8: the content of CP-28's frozen protocol, which CP-26 writes;
    - §24.9: §16.4's "before fresh-data test" row, which CP-26's daily refits of the control meet.
  - **Its inheritances:**
    - §2's released-error rule and target-day embargo;
    - §15.3's missing-weather rule;
    - §16.2;
    - each generation's landed specification: §14 (v2), §15 (v3), §17 (v4) and §23 (v5, DDNN-2).
  - **The Owner's rulings of 2026-10-12** under §24.5 bind this checkpoint:
    `docs/track-b/cp-25-rulings-2026-10-12.md`, SHA-256
    `c7af67f88157277aafd8dd2b1b49e12a1d9ff4b747ca5bdf178fac664fba53c1`.
  - **The publication anchor** is PUBLISH_RULES 1.5, SHA-256
    `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`, for the draft packet only
    (§11). CP-26 publishes nothing.

## Orchestrator-reported expected state
- **Branch / commit:** `main` = `origin/main` at the commit that records CP-26's issue.
  - It is a direct child of `ecd6ca308bcda0b9b12dfc7532da15bf1c02a3f4`, CP-25's closure, and changes
    only `progress.md`.
  - Below them is CP-25's landing, `5336aef` (`land/cp-25`).
  - Only `main` exists, locally and on origin. There is no stash, and no worktree besides the
    primary checkout.
- **Working tree:** the primary checkout `/Users/djourno/Downloads/PJM` is on `main` and clean
  apart from ignored material.
  - **The Orchestrator uses it during CP-26.** Never switch its branch, and never write a tracked
    file in it. Your only writes there are under:
    - `.local/artifacts/cp-26/`: the tools' state, and your ledgers, logs and caches;
    - `.local/tmp/cp-26/`;
    - the worktrees under `.local/worktrees/cp-26/`.

    Keep nothing you need after reclamation inside your worktree.
  - **The canonical brief.** This brief's canonical copy is
    `.local/artifacts/cp-26/issued-brief.md`. Package that file byte for byte, not the pasted text.
- **What already exists:**
  - **The frozen development inputs (CP-25,** `land/cp-25` = `5336aef`) in
    `reports/development-inputs/`, bound by `manifest.json`
    (`f3e8ca15e4466d371de5b6db9c181f77adaa8823ca2e7e0d325182120db32fd9`):
    - `partitions-development.json` (`70c752b9…2749`);
    - `eligibility-calendar.csv` (`8e1e3a70…f56e`): 2,766 of 2,806 days eligible;
    - `record-masks.json` (`d7a8ecef…1adc`);
    - `tier-register.json` (`1a71fd83…c974`), with the margin table and every input's
      missing-input rule;
    - `weather-features-gaps.parquet` (`fbc2517e…ef2f`).

    Also: the boundary guard `src/cp25/guard.py`, and CP-25's retained grids in
    `.local/artifacts/cp-25/weather/` (primary checkout, read-only).
  - **The preserved data:** `data/snapshot.parquet` (`7dd2dc73…7f00`) for prices and the load
    forecast. Also CP-20's committed features `reports/weather-ablation/weather-features.parquet`
    (`66b8264b…1b58`) and its grids in `.local/artifacts/cp-20/weather/runs/`.
  - **The landed member code, imported unchanged through your harness:**
    - v1's recipe (`src/delu_forecast/`) and B0 (`src/delu_forecast/baselines.py`);
    - LEAR (`src/cp15/`);
    - v2's blend and H layer (`src/cp16/`, `land/cp-16` = `d62769c0…a284`);
    - the weather components (`src/cp20/`, `land/cp-20` = `f450bc1a…f7f`);
    - the three-block LightGBM (`src/cp21/`, `land/cp-21` = `4e37cf79…6499`);
    - the H-layer replay (`src/cp22/`);
    - DDNN-2 and v5 (`src/cp24/`, `land/cp-24` = `05e60159…7577`, `evidence/cp-24` = `05b7e618…397e`).

    The landed code refuses any snapshot, boundary or anchor other than its own: see §24.7's
    harness.
  - **The parity references:**
    - committed central vectors under `reports/weather-ablation/`, `reports/block-challenger/`,
      `reports/distribution-challenger/` and `reports/ddnn2/`;
    - CP-24's own parity and determinism records: `reports/ddnn2/v4-parity.json`, and the ensemble
      determinism control in CP-24's attempt-1 controls.
  - **The exposure ledger,** `docs/track-b/exposure-ledger.md`
    (`375fef5d200c400b79840dcc9977ab3d63a95ed85af603c8add3b9a9210d98a6`). Entries 1–5 are assessed
    by the Orchestrator, and your Integration Critic reviews them (§24.2). The Orchestrator keeps
    the file; you report any exposure in your return instead of editing it.
  - **Tools:** `scripts/gauntlet.py`, `scripts/bar.py`, and the SessionStart hook that keeps the
    secret guard on. The primary checkout's `.venv` holds the locked environment.
  - **Not yet:** no CP-26 code or outputs, and no CP-28 protocol.
- Verify this yourself before relying on it, and report any material mismatch.

## Observable outcome
CP-26 closes with the following, bound by one fresh Integration-Critic PASS:

- **the forecast ledger:** every policy and member, at every warm-up and scored origin;
- **the scores and their uncertainty** for B0, v1-R and v2–v5, on the four masks, with stored
  replicates, the diagnostics and the registered breakdowns;
- **the control audit:** v2 → v3, v3 → v4 and v4 → v5, all descriptive;
- **the descriptive rows:** DDNN-2 alone, and v1's released artifact on its holdout;
- **"v5 (no load forecast)"** against v5 (the Owner's ruling 1);
- **the control run with GFS shifted +6 hours,** with its fragility verdict (§24.5);
- **the parity gate's records;**
- **CP-28's frozen protocol,** committed before the first score;
- **the report,** and a draft publication packet.

A complete result in which v5 does not improve on v4 over the full calendar is a valid PASS.

**The return carries a short summary for the Owner's CP-28 decision (§24.2):** the transition audit,
the no-load bound, the GFS +6-hour result, and the fallback counts.

## Complete authoritative checkpoint bar
`capstone_v21.md` v21-r13 §24.7, "CP-26: the re-baseline on every development day (stage 6)": every
item. It is governed by the sections and rulings named in Target.

Verbatim, checked with `scripts/bar.py check` against the anchor at `d58486d`:

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
> - **Search dates:** S_k = 2020-01-01 + 182k days, for k = 0 to 13. Search k serves the origins from
>   S_k up to the day before S_(k+1).
> - **The batches:** consecutive 28-day blocks, tiling backward from S_k − 1.
>   - Only blocks starting on or after 2019-07-01 are kept.
>   - B_k = min(11, the blocks kept), so B_0 = 6.
>   - There is no fold skip rule: every block lies before the search's first origin.
> - **One fit per trial and batch,** on `[max(2019-01-01, b − 728), b)`.
> - **The sampler:** seeded with `SeedSequence([26, k, 0x5A3])`, with 128 trials. Successive halving,
>   the ranking metric and the tie rule follow §23.4.
> - **The ensemble:** the four best distinct configurations, with two seeds each.
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
> - **Nothing enters a policy's or an arm's interval-layer buffer** on a fallback or failed day, so the
>   buffer spans more calendar days. That is disclosed.
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
> - **Review:** CP-26's Integration Critic reviews it.
> - **Custody:** it lands with CP-26. If CP-26 is discarded, the protocol goes with it.
> - **The Owner's later confirmation** decides only whether CP-28 runs, never what it tests.
>
> #### The ledger
>
> Every forecast is stored with its issue instant, training-target cutoff, input vintages, seeds and
> code identity.
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

## Task-specific supporting extract
- **The Owner's rulings** (`docs/track-b/cp-25-rulings-2026-10-12.md`), which complete §24.5 for
  this checkpoint:
  1. **The load forecast** (tier 3) keeps a recorded exception: the main evaluation runs every
     policy with it, as landed, and **the control is v5 as landed.**
     - **"v5 (no load forecast)" is descriptive only.** Its construction is exactly the ruling's
       §1: the load columns removed from LEAR, L-N and L-R; DDNN-2's `load_d0` and its optional
       D−1 and D−7 load groups removed, with the search space adjusted; its 14 searches rerun; and
       the H layer re-estimated on its own errors.
     - **Its parity check:** with the inputs restored, the variant reproduces the as-landed parity
       vectors.
     - **What CP-26 reports:** v5 against the variant, overall and by year and season.
  2. **The target price is tier 2,** with the SMARD caveat disclosed.
  3. **The structural shifts are accepted,** so no run is made for them. The partial **GFS +6-hour
     shift** runs on the control, including its 14 searches, beside the nominal run.
  4. **Two GFS runs are late under §15.3:** deliveries 2022-12-01 (run 2022-11-30 00 UTC) and
     2023-01-21 (run 2023-01-20 00 UTC). Their three derived weather columns are missing, with
     indicators and training-only medians.
- **The ceiling is 485 machine-hours,** the Owner's ruling 1, which raises §24.7's 400 for the
  variant. The timing pilot's stop line is 80% of 485, which is 388.
- **The search schedule:**
  - S_k = 2020-01-01 + 182k days, for k = 0 to 13, the last being 2026-06-24;
  - B_0 = 6, from blocks starting on or after 2019-07-01;
  - seeds `SeedSequence([26, k, 0x5A3])`, with 128 trials;
  - CP-24's ensembles are never reused for a forecast.
- **"The first score"** means the first computation of any evaluation metric on a scored-calendar
  day: a loss, coverage, a ratio or a test. Producing forecasts, and the released errors that feed
  the interval buffers, is not scoring.
- **CP-28's frozen protocol** follows §24.8 in full, including the seven arms A1–A7, the gates,
  Holm across seven arms at α = 0.05, the simplicity order and the failure rules. Any detail §24.8
  leaves open is fixed there without inspecting an outcome.

## Applicable constraints
- **The ceilings:**
  - 485 machine-hours, summed over workers' wall time (the Owner's ruling 1);
  - at most 4 concurrent workers;
  - BLAS 1;
  - CPU only;
  - peak memory 12 GB;
  - no cloud and no GPU.

  The timing pilot runs first, as §24.7 specifies.
- **No retrieval of any kind:** 0 data bytes and 0 remote writes. Every input is local. Any MLflow
  export is a local draft, never uploaded.
- **The red line (§24.2).** No delivery day after 2026-09-06 is read. Route every data read through
  the guard. Do not read, record or mention any market value or event after 2026-09-06.
- **Files that never change:**
  - `data/`;
  - `reports/development-inputs/` and every other file that earlier evidence binds;
  - the landed member code in `src/delu_forecast/`, `src/cp15/`, `src/cp16/`, `src/cp20/`,
    `src/cp21/`, `src/cp22/`, `src/cp24/` and `src/cp25/`. The harness imports it unchanged;
  - the root `pyproject.toml` (`aa35326a…4e4a`) and `uv.lock` (`5d2aecc3…a94`);
  - the anchors, `AGENTS.md`, the role files and the exposure ledger.
- **Long computation** may run unattended in the background, within the ceilings, under your
  ledger. Commit work in progress on `gauntlet/cp-26` at every stage boundary. A usage limit can stop
  you at any moment, and you resume from your last commit and ledgers.
- **Credentials** follow `AGENTS.md` § Credentials; none is needed. Export
  `MLFLOW_DISABLE_TELEMETRY=true` and `DO_NOT_TRACK=1` for any MLflow job.
- **Pinned identities:**
  - the amendment record (`0f3b54ea21fef1d21782cdd40993f23b5d792cc45f638ad15fbdc27b97285e59`);
  - CP-25's landing record (`f33f58985a85803aed04ef48bf9c55db0d7738fac0a7d81db2a9c02d31b11b56`);
  - the packet template `docs/track-b/publication-packet-template.md`
    (`4049c3e1f695034ec45fa185d465fce05ab1183cbded72188306579d7287d01a`);
  - every hash above.
- **Tools:**
  - run `scripts/gauntlet.py start cp-26` first, from the primary checkout;
  - then create your worktree with
    `git -C /Users/djourno/Downloads/PJM worktree add -b gauntlet/cp-26 .local/worktrees/cp-26/lead main`;
  - launch the one Critic with `critic-open`, `critic-brief` and `critic-close`. If you cannot
    start a subagent, end your turn with `critic-open`'s output and ask the Orchestrator to launch
    the Critic with exactly the printed prompt;
  - check the return with `scripts/gauntlet.py return`.
- **Owner-facing Git commands** must be non-interactive: `git --no-pager …` and
  `git commit -F <file>`.

## Timebox
About 60 active hours from orientation to the terminal return. Unattended computation, about 70–120
wall-clock hours at 4 workers, runs alongside and is not counted as active hours.

## Owner-only actions already authorized
- **CP-26's execution** under v21-r13 §24.7, the Owner's rulings and this brief. The Owner's delivery
  of this brief is his grant (§24.10). It covers local `gauntlet/cp-26` candidate and evidence
  commits in your worktree, and the exact packaging of this brief.
- **Nothing else:** no retrieval, mainline operation, push, tag, publication, remote write, MLflow
  upload or governance edit.

## Stop and return
- **First commit.** The first commit on `gauntlet/cp-26` copies the canonical brief byte for byte to
  `docs/track-b/evidence/cp-26/issued-brief.md`.
- **The return.** Return exactly one of PASS / BLOCKED / INCOMPLETE, using templates §3. It
  carries both terminal SHAs and the verdict-only delta, checked with `scripts/gauntlet.py return`.
  - Its "Open risk or exact owner action" section gives the Owner's CP-28 decision summary from
    Observable outcome.
  - Name any exposure (§24.2), and any interview-answer trigger, in one line each.
- **Do not** begin CP-28: write its frozen protocol, but fit, run and score no arm. Do not commit to
  `main`, publish or push. Leave your worktree and branch for the Owner's LAND and the
  Orchestrator's reclamation.
