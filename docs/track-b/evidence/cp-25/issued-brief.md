# Track B Checkpoint Brief — CP-25 (our own data gaps: the development inputs to 2026-09-06, their tiers and the issue-time check)

*Issued by the Orchestrator on 2026-10-12, Asia/Jerusalem.*

## Target
- Repository: DE-LU day-ahead forecasting, `/Users/djourno/Downloads/PJM` (origin
  `hrsi56/delu-day-ahead-forecast`). The checkpoint runs locally, in the Lead's own worktree.
- Authorized checkpoint: CP-25, exactly one.
- Ratified plan anchor: `capstone_v21.md`, revision v21-r13, §24.6, SHA-256
  `173799d818387b9d82db16b9ccd7195afaebbea8e11259809e4a8b704bd525a8`, ratified at
  `d58486da826b337bd58f469e122315c3142e360b`.
  - §24.6 is governed by §24.2 (the boundary, the guard and the exposure ledger), §24.4 (the issue
    time) and §24.5 (the tiers, the register's categories, the margin table and the missing-input
    rules).
  - Its inheritances: §1's preserved files; §2's refusal of the post-gate A69 columns and its
    released-error rule; §15.2's GFS source, recipe, fields, leads and targeted checks; and §15.3's
    missing-weather rule.
  - The publication anchor, PUBLISH_RULES 1.5 (`1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`),
    is not triggered: CP-25 publishes nothing.

## Orchestrator-reported expected state
- **Branch / commit:** `main` = `origin/main` at the commit that records CP-25's issue.
  - It is a direct child of `d58486da826b337bd58f469e122315c3142e360b`, the v21-r13
    ratification, and changes only `progress.md`.
  - Only `main` exists, locally and on origin. There is no stash, and no worktree besides the
    primary checkout.
- **Working tree:** the primary checkout `/Users/djourno/Downloads/PJM` is on `main` and clean
  apart from ignored material.
  - **The Orchestrator uses it during CP-25.** Never switch its branch, and never write a tracked
    file in it. Your only writes there are under:
    - `.local/artifacts/cp-25/`: the tools' state, your ledgers, logs and caches, and raw downloads;
    - `.local/tmp/cp-25/`;
    - the worktrees under `.local/worktrees/cp-25/`.

    Keep nothing you need after reclamation inside your worktree.
  - **The canonical brief.** This brief's canonical copy is
    `.local/artifacts/cp-25/issued-brief.md`. Package that file byte for byte, not the pasted text.
- **What already exists:**
  - **The preserved development data** (§1), never modified:
    - `data/snapshot.parquet`, SHA-256
      `7dd2dc73407706ca6bd3c1ad51d201ac0de35eec5ca129ce320cca639f697f00`: hourly, 2019-01-01 to
      2026-09-06 (Europe/Berlin), 67,343 rows, from the SMARD route pulled on 2026-09-08
      (`data/source_manifest.json`, `69bc909326b164b2af8d23307edf180d17193fa18c0faf360549761e2ed7f094`);
    - `data/partitions.json`, `6bee065368b721ae8092ba287e04bb6dda0d4bde80909e72380503ba61e0b090`,
      whose `eda_cutoff` is 2026-04-07. It marks v1's final calibration (2026-04-09 to 2026-06-07)
      and holdout (2026-06-09 to 2026-09-06).
  - **The weather.**
    - CP-20's committed features: `reports/weather-ablation/weather-features.parquet`, SHA-256
      `66b8264bb6e124ae0cc540a40ff00d0e9f625cabee6e0ebb6e4605c3e7ea1b58`. They cover delivery days
      2019-01-01 to 2026-04-07, with one gap, 2022-09-29 to 2023-03-24.
    - CP-20's retained decoded grids: `.local/artifacts/cp-20/weather/runs/`, in the primary
      checkout. Read them in place, read-only.
    - The admission dossier: `reports/weather-admission/dossier.md`,
      `0782677030db49aa7976343372a26225bc0154915f6e605d24e64495c0625881`. It holds the NCEP
      schedule evidence for GFS.
    - CP-20's retrieval and extraction code, `src/cp20/` (`net.py`, `gfs.py`, `extract.py`,
      `weather.py`, `inputs.py`), reusable by import, read-only. Both archives are anonymous:
      NCAR GDEX d084001 (THREDDS `fileServer`) and NOAA AWS `noaa-gfs-bdp-pds`.
  - **The landed policies' code,** read-only: v1 (`src/delu_forecast/`), CP-15's LEAR day design
    (`src/cp15/`), and CP-16, CP-20, CP-21 and CP-24's code. You read it to state each input's
    missing-input rule with its file and line; you change none of it.
  - **The earlier records** the masks need: folds 1–5 (`data/partitions.json`); v1's holdout; CP-16's
    training-only admission slices (anchor §14.2 and CP-16's reports); and CP-24's gate days and
    search batches (`reports/ddnn2/`).
  - **Motivation, not the bar:** the stage 3 report (`docs/track-b/data-source-research-2026-10-11.md`)
    and the CP-15 feasibility sheet (`reports/cp15/feasibility/structural_inputs.md`) hold the
    publication-time evidence already gathered for SMARD and ENTSO-E inputs.
  - **The exposure ledger,** `docs/track-b/exposure-ledger.md`
    (`7bd4ed0fcdb73b59ba2cc2b4801db5f7217d87f5fa6a41b6b324f3f0ebfed95b`). The Orchestrator keeps it;
    you report any exposure in your return instead of editing it.
  - **Tools:** `scripts/gauntlet.py`, `scripts/bar.py`, and the SessionStart hook that keeps the
    secret guard on. The primary checkout's `.venv` holds the locked environment.
  - **Not yet:** no CP-25 code, data or reports.
- Verify this yourself before relying on it, and report any material mismatch.

## Observable outcome
CP-25 closes with the frozen development inputs for delivery days 2019-01-01 to 2026-09-06, bound by
one fresh Integration-Critic PASS:

- the manifest with hashes;
- GFS weather features for the gaps, from about 329 new D−1 00 UTC runs;
- the tier register, with the margin table and every input's missing-input rule;
- the new partition specification, the eligibility calendar and the record masks;
- the boundary guard, with its tests;
- the retrieval log.

Nothing is forecast or scored. **The return also carries a short summary for the Owner's rulings
(§24.5):**

- every input's tier, naming any tier-3 input of B0 or v1–v5;
- the target price's finality evidence;
- each tier-2 group's shifts, classed as none, structural or partial.

A complete but negative result is a valid PASS: for example, the load forecast found to be tier 3,
or a structural +1-hour shift.

## Complete authoritative checkpoint bar
`capstone_v21.md` v21-r13 §24.6, "CP-25: our own data gaps (stage 5)": every scope item, output,
ceiling and gate. It is governed by §24.2, §24.4 and §24.5, and by the inheritances named in Target.

Verbatim, checked with `scripts/bar.py check` against the anchor at `d58486d`:

> ### 24.6 CP-25: our own data gaps (stage 5)
>
> **Purpose:** the frozen development inputs for delivery days 2019-01-01 to 2026-09-06, covering
> every input of B0, v1-R and v2–v5, with our gaps filled and every input checked against the new
> issue time.
>
> **Scope:**
>
> 1. **Prices and load are not re-pulled.** They come from the preserved bytes of
>    `data/snapshot.parquet`, which v2–v5 were scored on.
> 2. **Inventory.** For every input series: its source, product, licence, granularity and timezone,
>    and its gaps by year, each with a cause: the source, or our extraction.
> 3. **Weather for the gaps.** GFS 0.25° D−1 00 UTC, with §15.2's source, recipe, fields and leads,
>    for:
>    - delivery days 2022-09-29 to 2023-03-24;
>    - delivery days 2026-04-08 to 2026-09-06.
>
>    That is about 329 runs. They take §15.2's targeted checks for runs outside the inventoried
>    scope, and are not labelled already admitted. CP-20's retained grids are reused as they are.
> 4. **The tier register (§24.5).** For each input, its documented publication time against D−1
>    11:00 Europe/Berlin, strictly before, with evidence:
>    - v1's load inputs, `load_forecast_mw` and `load_forecast_day_mean_mw`;
>    - LEAR's and DDNN-2's load forecast and price lags;
>    - the target price's finality;
>    - GFS, as tier 2 on CP-20's dated NCEP schedule evidence (`reports/weather-admission/dossier.md`),
>      extended to the new issue time, with per-run evidence where it exists;
>    - every calendar feature and hindsight label.
>
>    §2's refusal of the post-gate A69 wind and solar forecast columns stands.
> 5. **The missing-input rule of each input,** stated with its file and line in the landed code, and
>    **the margin table** (§24.5).
> 6. **The new partition specification:** development to 2026-09-06, written as a new file.
> 7. **The eligibility calendar.** The frozen list of eligible delivery days for CP-26, with every
>    exclusion and its reason.
>    - Exclusions follow target completeness, and the inputs whose absence makes the as-landed v5
>      fail: prices and the load forecast.
>    - Weather gaps follow §15.3 and exclude no day.
>    - No model, candidate or score enters the calendar.
> 8. **The record masks,** fixed from existing records before any CP-26 score:
>    - **the days never scored before.** A day counts as scored if a forecast's loss on it entered a
>      reported result, a selection or an admission decision. The mask subtracts:
>      - folds 1–5's evaluation days;
>      - v1's holdout;
>      - CP-16's training-only admission slices;
>      - CP-24's gate days and search batches.
>
>      Days used only to fit or calibrate, such as v1's calibration windows, do not count as scored,
>      and the mask lists them;
>    - the old-fold days, folds 2–5. Fold 1, 2020-07-01 to 2020-09-28, lies inside CP-26's warm-up.
> 9. **The boundary guard (§24.2),** with its tests. Credentials follow `AGENTS.md`: no value in a
>    log, URL or error message, with tests for it.
>
> **Outputs:**
>
> - the manifest with hashes;
> - the weather features for the gaps;
> - the tier register;
> - the partition specification, the eligibility calendar and the masks;
> - the retrieval log.
>
> No raw GRIB bytes or decoded grids are committed, under `DATA-LICENSE.md`.
>
> **Ceilings, proposed:**
>
> - 24 machine-hours, summed over workers' wall time;
> - at most 4 concurrent workers;
> - at most 40 GiB of transient transfer;
> - $0.
>
> The basis is CP-20, which retrieved about 2,100 GFS runs in 5.7 hours.
>
> **Not in CP-25:** any new source (§24.2).
>
> **Gates:**
>
> - this ratified section;
> - the Owner's retrieval approval (free public archives, $0);
> - the issued brief;
> - the LAND.
>
> Then the tier register and the margin table go to the Owner, for the tier and margin rulings
> (§24.5).

## Task-specific supporting extract
- **The GFS runs to fetch:** the 00 UTC run of day D−1 for each missing delivery day D, at §15.2's
  leads f021–f048:
  - delivery days 2022-09-29 to 2023-03-24: runs 2022-09-28 to 2023-03-23 (177);
  - delivery days 2026-04-08 to 2026-09-06: runs 2026-04-07 to 2026-09-05 (152).
- **The guard (§24.2):**
  - rows are refused when their Europe/Berlin delivery day is after 2026-09-06;
  - GFS runs are refused when initialized at or after 2026-09-06 00 UTC, and leads outside
    f021–f048 are refused;
  - the tests named in §24.2: the instants 2026-09-06 21:00 and 22:00 UTC; the 2026-09-06 00 UTC
    run, refused; and the 2026-09-05 00 UTC f048 message, admitted.
- **The issue time (§24.4):** D−1 11:00 Europe/Berlin, strictly before: 10:00 UTC on CET and 09:00
  UTC on CEST.
- **The margin table (§24.5):** for each tier-2 group and each shift (+1, +6 and +24 hours), the days
  on which the shifted availability is no longer strictly before the issue time.
- **"Scored" (§24.6, item 8):** a day counts as scored if a forecast's loss on it entered a reported
  result, a selection or an admission decision. Days used only to fit or calibrate are listed apart.
- **The eligibility calendar (§24.6, item 7):** target completeness, and the inputs whose absence
  makes the as-landed v5 fail (prices and the load forecast). Weather gaps exclude no day.

## Applicable constraints
- **The §24.6 ceilings,** enforced from the first job:
  - 24 machine-hours, summed over workers' wall time;
  - at most 4 concurrent workers;
  - at most 40 GiB of transient transfer;
  - $0.
- **Retrieval:** only the GFS runs above, from the two anonymous archives, under the Owner's
  approval. Documentation pages may be read to establish publication times, but no data is fetched
  from them. No new source is collected (§24.2's short path).
- **The red line (§24.2).** No delivery day after 2026-09-06 is fetched, stored or read. Do not
  read, record or mention any market value or event after 2026-09-06. Report any exposure in your
  return.
- **Files that never change:**
  - `data/snapshot.parquet` and `data/partitions.json` (§1). CP-25's partition specification is a
    new file;
  - every file that earlier evidence binds, including CP-20's committed weather files. CP-25's
    features are new files;
  - the root `pyproject.toml` (`aa35326abbb13dfa4ea8ba1b4b367343b77f895e7724d5dc94e0bdb7637b4e4a`)
    and `uv.lock` (`5d2aecc3d173fef6191cb2bb9d14cd008c0e9cc764700f1352b81d1924465a94`). A new
    dependency, if one is truly needed, gets its own lock outside the root;
  - the anchors, `AGENTS.md`, the role files and the exposure ledger.
- **Licences:** `DATA-LICENSE.md` (`d83494389e322e9f3b4e29d49acaed0486136f69154f81c801e2ef920acb8ac6`)
  is unchanged. No raw GRIB bytes or decoded grids are committed; derived features carry the
  existing weather attribution.
- **Pinned identities:**
  - the amendment record `docs/track-b/capstone_v21-r12-to-v21-r13-amendments.md`, SHA-256
    `0f3b54ea21fef1d21782cdd40993f23b5d792cc45f638ad15fbdc27b97285e59`;
  - PUBLISH_RULES 1.5 and every hash above.
- **Credentials** follow `AGENTS.md` § Credentials. None is needed: both archives are anonymous.
  Export `MLFLOW_DISABLE_TELEMETRY=true` and `DO_NOT_TRACK=1` for any MLflow job.
- **Working files** go under `.local/`. Commit work in progress on `gauntlet/cp-25` at every stage
  boundary. A usage limit can stop you at any moment, and you resume from your last commit and
  ledgers.
- **Tools:**
  - run `scripts/gauntlet.py start cp-25` first, from the primary checkout;
  - then create your worktree with
    `git -C /Users/djourno/Downloads/PJM worktree add -b gauntlet/cp-25 .local/worktrees/cp-25/lead main`;
  - launch the one Critic with `critic-open`, `critic-brief` and `critic-close`. If you cannot
    start a subagent, end your turn with `critic-open`'s output and ask the Orchestrator to launch
    the Critic with exactly the printed prompt;
  - check the return with `scripts/gauntlet.py return`.
- **Owner-facing Git commands** must be non-interactive: `git --no-pager …` and
  `git commit -F <file>`.

## Timebox
About 16 active hours from orientation to the terminal return.

## Owner-only actions already authorized
- **CP-25's execution** under v21-r13 §24.6 and this brief. The Owner's delivery of this brief is
  his grant (§24.10). It covers local `gauntlet/cp-25` candidate and evidence commits in your
  worktree, and the exact packaging of this brief.
- **The retrieval,** approved by the Owner on 2026-10-12: "מאשר אחזור GFS מהארכיונים הציבוריים
  ל־CP-25, ללא עלות" ("I approve retrieving GFS from the public archives for CP-25, at no cost").
  It covers only the runs and leads in the extract above.
- **Nothing else:** no mainline operation, push, tag, publication, remote write, other retrieval or
  governance edit.

## Stop and return
- **First commit.** The first commit on `gauntlet/cp-25` copies the canonical brief byte for byte to
  `docs/track-b/evidence/cp-25/issued-brief.md`.
- **The return.** Return exactly one of PASS / BLOCKED / INCOMPLETE, using templates §3. It
  carries both terminal SHAs and the verdict-only delta, checked with `scripts/gauntlet.py return`.
  - Its "Open risk or exact owner action" section gives the Owner's ruling summary from Observable
    outcome.
  - Name any exposure (§24.2), and any interview-answer trigger, in one line each.
- **Do not** begin, scaffold or plan CP-26: no harness, no forecast, no fit and no score. Do not
  commit to `main`, publish or push. Leave your worktree and branch for the Owner's LAND and the
  Orchestrator's reclamation.
