# Verdict — CP-25 — Integration — PASS

- Candidate SHA: 98f3ef6a964a80d6aa29236f3c2770951a995d94
- Plan / version / bar: `capstone_v21.md`, revision v21-r13 (SHA-256
  `173799d818387b9d82db16b9ccd7195afaebbea8e11259809e4a8b704bd525a8`), "### 24.6 CP-25: our own
  data gaps (stage 5)". Section identity at the candidate: 82 lines, 3,743 bytes, SHA-256
  `2a3e3fa1468cce7c31754efcbdac502b10465994c6241eb225781bede5ef9497`. Governed by §24.2, §24.4
  and §24.5; inherits §1, §2, §15.2 and §15.3.
- Verbatim bar excerpt (the excerpt is the citation; any line number is a courtesy and is non-binding):

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

- Worktree clean before and after: yes. `/Users/djourno/Downloads/PJM/.local/worktrees/cp-25/critic-1`,
  detached at the candidate SHA; `git status --porcelain` empty before the review and after it;
  `HEAD` unchanged. No Git write of any kind was made. Nothing was written inside the worktree:
  all outputs went to `/Users/djourno/Downloads/PJM/.local/tmp/cp-25/critic/`.
- Isolation: cooperative and procedural. No Builder checkout, diff, summary or conversation was
  read. The Lead's `launch-envelope.md` and the ledger's job commands were not opened; the ledger
  was read only for its counts, peaks and job names.

## Commands actually run

`W` = the critic worktree above. `PY` = `/Users/djourno/Downloads/PJM/.venv/bin/python`.
`WX` = `/Users/djourno/Downloads/PJM/.local/artifacts/cp-20/wx-venv/bin/python`.
`S` = `/Users/djourno/Downloads/PJM/.local/tmp/cp-25/critic`.

1. `git -C W status --porcelain; git -C W rev-parse HEAD` → exit 0; empty; `98f3ef6a964a80d6aa29236f3c2770951a995d94`.
2. `cd W && git show main:scripts/bar.py | python3 -I - bar capstone_v21.md "### 24.6 CP-25: our own data gaps (stage 5)" --at 98f3ef6a964a80d6aa29236f3c2770951a995d94 > S/bar-24.6.txt`
   → exit 0; stderr: `plan capstone_v21.md at 98f3ef6a…: sha256 173799d8…25a8; section 82 lines, 3743 bytes, sha256 2a3e3fa1…9497`.
   `shasum -a 256 capstone_v21.md` and of `git show <candidate>:capstone_v21.md` → both `173799d8…25a8`.
3. `shasum -a 256` of the untouchables at the candidate → `data/snapshot.parquet` `7dd2dc73…7f00`,
   `data/partitions.json` `6bee0653…b090`, `pyproject.toml` `aa35326a…4e4a`, `uv.lock` `5d2aecc3…5a94`,
   `DATA-LICENSE.md` `d8349438…8ac6`, `docs/track-b/exposure-ledger.md` `7bd4ed0f…d95b`,
   `reports/weather-ablation/weather-features.parquet` `66b8264b…1b58`,
   `reports/weather-admission/dossier.md` `07826770…5881`, `data/source_manifest.json` `69bc9093…f094`,
   the v21-r12→r13 amendment record `0f3b54ea…5e59`, `docs/PUBLISH_RULES.md` `1bc0c523…f94e`. All as pinned.
4. `git -C W diff --name-status 1459ee2 <candidate>` → exit 0; 49 paths, every one `A` (added):
   `docs/track-b/evidence/cp-25/**`, `reports/development-inputs/**`, `scripts/cp25_data_gaps.py`,
   `src/cp25/**`, `tests/cp25/**`. No `M` or `D`.
   `git -C W diff --quiet 1459ee2 <candidate> -- AGENTS.md CLAUDE.md engineering-role.md orchestrator-role.md notebooklm-role.md docs/track-b/gauntlet-templates.md 'capstone_*' 'syllabus_*' docs/PUBLISH_RULES.md data/ reports/weather-admission reports/weather-ablation reports/v2-causal reports/ddnn2 reports/distribution-challenger reports/cp15 src/cp20 src/delu_forecast src/cp15 pyproject.toml uv.lock DATA-LICENSE.md .claude .githooks`
   → exit 0 (no change). `docs/track-b/` changes outside `evidence/cp-25/`: none.
5. Reproduction step 1: `cd W && PY scripts/cp25_data_gaps.py timed --name critic-tests --workers 1 -- PY -m pytest -q -p no:cacheprovider tests/cp25`
   → exit 0; `103 passed in 0.39s`.
6. Reproduction step 2: `cd W && PY scripts/cp25_data_gaps.py timed --name critic-rebuild --workers 1 -- PY scripts/cp25_data_gaps.py build all --out S/rebuild`
   → exit 0 (69.7 s); summary: 7,897 feature rows, 329 delivery days, status `ok` 7,897, 329 runs
   complete, 16,450 messages, 16,553 requests; calendar 2,806 days, 2,766 eligible, 40 excluded.
   Then `cmp` of each of the 19 rebuilt files against `W/reports/development-inputs/<same name>`
   → 19 of 19 byte-identical.
7. Reproduction step 3: `cd W && PY scripts/cp25_data_gaps.py timed --name critic-identity --workers 1 -- PY -c "<the assignment's conversion_identity one-liner>"`
   → exit 0; `{"rows": 59446, "runs": 2476, "keys_identical": true, "values_bitwise_identical": true, "status_identical": true, "max_abs_difference": 0.0, "committed_sha256": "66b8264b…1b58"}`,
   identical to the committed `conversion-identity.json`.
8. Reproduction step 4: `cd W && PY scripts/cp25_data_gaps.py timed --name critic-scan --workers 1 -- PY scripts/cp25_data_gaps.py scan reports/development-inputs docs/track-b/evidence/cp-25 /Users/djourno/Downloads/PJM/.local/artifacts/cp-25`
   → exit 0; `files_containing_a_value: {}`. In this shell only `ENTSOE_API_TOKEN` was set
   (`variables_set` reported the other four unset), so this scan alone covered one value.
9. Supplementary credential scan (names and paths only): `S/full_scan.py`, which loads `main`'s
   `scripts/secret_guard.py` and uses its in-process `credentials()` (environment, `launchctl`
   and stored exports, never printed) and `_scan()` over every blob the candidate adds, the four
   candidate commit messages, every file under `.local/artifacts/cp-25/` and the critic rebuild;
   run as `PY scripts/cp25_data_gaps.py timed --name critic-fullscan --workers 1 -- /usr/bin/python3 -I S/full_scan.py`
   → exit 0; 1,099 items; values available in-process for all five AGENTS.md credential names
   (the two MLflow names share the DagsHub value) and every other credential-named variable the
   guard collects; findings: none.
10. Reproduction step 5 (optional network re-fetch): **not run.** No network retrieval of any
    kind was made by this review. Step 6 below reconstructs from the retained raw messages instead.
11. Reproduction step 6, independent reconstruction of all 7 retained runs (2022-09-28, 2022-10-29,
    2022-12-31, 2023-03-23, 2026-04-07, 2026-06-20, 2026-09-05):
    - `PY scripts/cp25_data_gaps.py timed --name critic-recon-export --workers 1 -- PY -I S/recon_export.py`
      → exit 0; 350 retained message rows exported from `gfs-messages.parquet`.
    - `PY scripts/cp25_data_gaps.py timed --name critic-recon-decode --workers 1 -- WX -I S/recon_decode.py`
      → exit 0. Per run: 50 of 50 raw-message SHA-256 equal `gfs-messages.parquet`; 50 of 50
      decoded by `cp20.gfs.decode` (which validates every expected key) with no contradiction;
      50 of 50 boxes equal a plain-ecCodes decode sliced from the message's own grid definition
      (rows 55.25..47.0°N, columns 5.5..15.5°E); the decoded array equals the stored
      `runs/<run>.npz` bit for bit; the `.npz` SHA-256 equals its run record; DSWRF quanta equal
      the provenance table.
    - `PY scripts/cp25_data_gaps.py timed --name critic-recon-convert --workers 1 -- PY -I S/recon_convert.py`
      → exit 0. For delivery days 2022-09-29, 2022-10-30 (25 h), 2023-01-01, 2023-03-24,
      2026-04-08, 2026-06-21 and 2026-09-06: `cp20.weather.convert_run` output equals
      `weather-features-gaps.parquet` bit for bit, keys equal, status `ok`, `run_00z` correct; and
      the critic's own NumPy re-implementation of §15.2 (per-cell interpolation h22–h46, speed
      before averaging, DSWRF de-averaging with the −3q bound and clipping, cos-latitude weights)
      differs from the committed values by 0.0 at most.
12. Independent recomputations, read-only inline `PY -I -` checks run from `W` (each a few
    seconds; they were not wrapped in `timed`, a procedural deviation disclosed here; total under
    two minutes of one worker):
    - **Margin table** from first principles (issue instants from `zoneinfo`, the dossier's capture
      CSV, documented deadlines): D−1 prices 2,806 days, margin 21.0–23.0 h, +1/+6/+24 h affected
      0/0/2,806; D−2 prices 45.0–47.0 h, 0/0/0; GFS 2,805 days, 4.9975–6.2906 h, 0/1,783/2,805
      (1,652 CEST days, all of them, plus 131 CET days 2024-10-28..2025-03-07); load of D 1.0 h,
      2,806/2,806/2,806; load D−1 24.0–26.0 h, 0/0/8. Equal to `margin-table.csv` and `margin-days.csv`.
    - **Eligibility calendar** from the snapshot alone (720 h price history, null load hours,
      finite target): the same 40 excluded days as `eligibility-calendar.csv`; 2,766 eligible.
    - **Record masks** from `data/partitions.json`, `reports/v2-causal/input-manifest.json`,
      `reports/ddnn2/rounds/round-1/gate.json` and `search-ledger.json`: folds 1–5 450, v1 holdout
      90, CP-16 slices 35, CP-24 gate 280 (the windows equal `gate.json` and anchor §23), CP-24
      batches 901 unique of 43; union 1,639; never scored 1,167 (1,132 eligible), set-equal to
      `record-masks.csv`; old folds 2–5 360 (358 eligible); fit-or-calibrate-only 213.
    - **Inventory** null hours by year from the snapshot: price none; load 2022 144 h (6 days),
      2023 49 h (3), 2024 1 h (1), every null hour with zero source quarter-hours; A69 onshore and
      solar 1 h in each of 2023–2025; A75 onshore and solar 1 h in 2025. Equal to `inventory-by-year.csv`.
    - **Retrieval log** (16,553 rows): hosts only `noaa-gfs-bdp-pds.s3.amazonaws.com` (16,472) and
      `tds.gdex.ucar.edu` (81, all under `d084001/2022/20221130`); every object, index and listing
      request parses to one of the 329 manifest runs, the 00 UTC cycle and leads
      f021,024,…,048; newest run 2026-09-05; no query string in any logged URL; 22 network
      failures, each retried.
    - **Message metadata** (`gfs-messages.parquet`, 16,450 rows, 50 per run, unique
      run/lead/field, unique SHA-256): `dataDate` = run date, `dataTime` 0, `endStep` = lead,
      validity = run + lead, wind `instant` at 10/100 m `heightAboveGround` in m s**-1, DSWRF
      `avg` at the surface in W m**-2 with `startStep` L−3 at L≡3 mod 6 and L−6 at L≡0 mod 6,
      `productionStatusOfProcessedData` 0, `typeOfProcessedData` 1, no nonfinite box value; 20
      NCAR messages, all run 2022-11-30 leads f027, f033, f036, f045.
    - **Per-run AWS evidence** from `gfs-aws-listing.jsonl`: all 329 runs list 10 objects and 10
      indexes; 327 runs have every `LastModified` before the issue time (margin 3.07–6.31 h,
      median 5.21 h, latest 05:55:31 UTC); run 2022-11-30 has 16 of 20 stamps at 15:10–15:38 UTC
      and run 2023-01-20 two at 10:20 and 11:40 UTC. Equal to the register's claims.
    - **Weather coverage**: CP-20's file and the gap file share columns and dtypes, have no day
      in common, and together cover all 2,806 development days once (67,343 hours, no duplicate
      instant, every day with its canonical 23/24/25 hours); the only non-`ok` day is 2019-01-01,
      `structural_missing_pre_2019_run`. CP-25's 329 runs overlap neither CP-20's 2,476 runs nor
      the dossier's 2,468 inventoried runs. Newest gap-file instant 2026-09-06 21:00 UTC.
    - **Manifest**: every hash in `manifest.json` (27 outputs, 17 inputs, 11 implementation files,
      7 reused landed files) equals the file at the candidate; no output unhashed.
    - **Citations**: all 25 `file:line` citations of `tier-register.json` and all 22 in
      `tier-register.md` hold the cited text at that line.
    - **Packaging**: `docs/track-b/evidence/cp-25/issued-brief.md` and the canonical
      `.local/artifacts/cp-25/issued-brief.md` both hash `5d2bf393…7703`; the first candidate
      commit (`2220f1c`) adds only that file.
13. Documentation reads, only to check the register's publication-time and finality claims (all
    listed in its §6): the as-adopted texts of Regulation 2015/1222 Art. 47, and Regulation
    543/2013 Arts. 6 and 12, on legislation.gov.uk. They confirm: gate closure "noon market time
    day-ahead" (47(2)); matched orders "shall be considered firm" (47(5)); day-ahead prices
    published "no later than one hour after gate closure" with no update wording (12(2)(d)); the
    day-ahead load forecast published "no later than two hours before the gate closure" and
    "updated when significant changes occur" (6(2)(b)). No data was fetched.
14. Close: `git -C W status --porcelain; git -C W rev-parse HEAD` → exit 0; empty;
    `98f3ef6a964a80d6aa29236f3c2770951a995d94`. Ledger after the review: 5,017 machine-seconds
    (1.39 h) in all, peak 4 workers, 15,823,546,871 bytes transferred; the critic's eight `timed`
    jobs used 1 worker each and 87 s of wall time together, with no transfer.
15. `cd W && git show main:scripts/bar.py | python3 -I - check /Users/djourno/Downloads/PJM/.local/artifacts/cp-25/critic-1/integration.md --source capstone_v21.md@98f3ef6a964a80d6aa29236f3c2770951a995d94`
    → exit 0; `ok: lines 11–92 (3742 bytes) appear in capstone_v21.md@98f3ef6a964a`.

## Evidence actually inspected

- Anchor §§1, 2, 15.2, 15.3, 23 (gate windows), 24.1–24.6 at the candidate; the issued brief.
- `reports/development-inputs/`: `report.md`, `tier-register.md`, `tier-register.json`,
  `manifest.json`, `margin-table.csv`, `margin-days.csv`, `eligibility-calendar.csv`,
  `ineligible-hours.csv`, `record-masks.csv`, `partitions-development.json`,
  `inventory-by-year.csv`, `inventory-gaps.csv`, `retrieval-log.csv`, `gfs-messages.parquet`,
  `gfs-runs.csv`, `gfs-targeted-checks.csv`, `gfs-aws-listing.jsonl`, `gfs-attempt-outcomes.json`,
  `weather-features-gaps.parquet`, `conversion-identity.json`, `resources.json`,
  `rights-notice.md`, `defects-and-repairs.md`.
- Code: `src/cp25/guard.py`, `ledger.py`, `runs.py`, `extract.py`, `features.py`, `calendar.py`,
  `tiers.py`, `inventory.py`, `build.py`; `scripts/cp25_data_gaps.py`; `tests/cp25/test_guard.py`;
  the reused `src/cp20/gfs.py` (decode, validate, box), `src/cp20/weather.py` (conversion,
  missing rule) and `src/cp20/extract.py` (fetcher use); `src/delu_forecast/features.py`
  (calendar, load day mean, hindsight labels); `src/cp24/design.py` (DDNN-2 calendar group).
- Decision-bearing inputs: `data/snapshot.parquet`, `data/partitions.json`,
  `reports/weather-ablation/weather-features.parquet` and `run-manifest.json`,
  `reports/weather-admission/availability/gfs_ncep_production_status.csv` and
  `inventory/gfs_required_runs.csv`, `reports/v2-causal/input-manifest.json`,
  `reports/ddnn2/rounds/round-1/search-ledger.json` and `gate.json`, `reports/cp15/protocol.json`.
- Evidence logs: `docs/track-b/evidence/cp-25/logs/tests-cp25.log`, `tests-full-suite.log`.
- Local state, read only: `.local/artifacts/cp-25/weather/raw/` (7 runs), `runs/*.npz` and
  `*.json` for those runs, `ledger.json` (counts, peaks, job names).

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 0 | Bar identity: the excerpt appears verbatim in `capstone_v21.md` at the candidate; plan hash as the brief records | PASS | Commands 2, 15; plan `173799d8…25a8`; section `2a3e3fa1…9497` |
| P | Purpose: frozen development inputs for 2019-01-01..2026-09-06, every input of B0, v1-R, v2–v5, gaps filled, every input checked against the new issue time | PASS | Items 1–9 below; coverage 2,806 days |
| 1 | Prices and load not re-pulled; from the preserved snapshot bytes | PASS | Snapshot hash unchanged (3); no SMARD or ENTSO-E request in the retrieval log (12); loads read with the row guard (`calendar.load_snapshot`, `inventory.snapshot_inventory`) |
| 2 | Inventory: source, product, licence, granularity, timezone; gaps by year with cause (source or our extraction) | PASS | `inventory-series.json`, `inventory-by-year.csv`, `inventory-gaps.csv`, `inventory-weather-by-year.csv`; counts recomputed (12). Defect D2 (wording, non-blocking) |
| 3a | Weather for the gaps: GFS 0.25° D−1 00 UTC, §15.2 source, recipe, fields, leads; delivery 2022-09-29..2023-03-24 and 2026-04-08..2026-09-06 | PASS | 177 + 152 = 329 runs, all v16, AWS first, one NCAR alternate per failed object (run 2022-11-30, 4 leads); metadata validated (12); features 7,897 h, all `ok` |
| 3b | §15.2's targeted checks for runs outside the inventoried scope; not labelled already admitted | PASS | `gfs-targeted-checks.csv`: `inventoried_by_admission` false ×329, listing 10+10 per run, decoded 50 per run, `metadata_validated` true ×329; no overlap with the 2,468-run inventory |
| 3c | CP-20's retained grids reused as they are | PASS | No CP-20 run refetched (run sets disjoint); conversion identity 59,446 rows bitwise (7); CP-20 files unchanged (4) |
| 3d | Conversion correctness of the new features | PASS | Step 6 reconstruction bit for bit for 7 runs through CP-20's code and an independent re-implementation (11) |
| 4a | Tier register: v1's `load_forecast_mw`, `load_forecast_day_mean_mw` | PASS | Tier 3, originality not established; deadline D−1 10:00 confirmed in Reg. 543/2013 Art. 6(2)(b) (13) |
| 4b | LEAR's and DDNN-2's load forecast and price lags | PASS | Load rows (tier 3) and price-lag rows (tier 2) name LEAR D−1/D−2/D−3/D−7, DDNN-2 `load_d0` and optional lags |
| 4c | The target price's finality | PASS | CACM 47(5), 39(2)(a), 48 and Reg. 543/2013 Art. 12; SMARD's "update possible" caveat disclosed; the Owner's choice preserved |
| 4d | GFS as tier 2 on CP-20's dated NCEP schedule evidence, extended to the new issue time, with per-run evidence where it exists | PASS | Reconstruction = later of the bracketing captures; margins 4.9975–6.2906 h (12); per-run `LastModified` for 329 runs, two exceptions named |
| 4e | Every calendar feature and hindsight label | PASS | Calendar set matches `delu_forecast/features.py`, CP-15's LightGBM list and DDNN-2's calendar group; `crisis_period` and `post_crisis` at `features.py:156`, `:159`, inadmissible |
| 4f | §2's refusal of post-gate A69 wind and solar columns stands | PASS | Register "Refused or unused"; `cp15.data.prepare` refuses non-raw columns |
| 4g | Strictly before D−1 11:00 Europe/Berlin, D−1's own offset | PASS | `guard.issue_time`, `strictly_before`; transition-day tests; nominal margins all > 0 (the build refuses otherwise) |
| 5a | Missing-input rule of each input with file and line in the landed code | PASS | 25 citations hold their text (12); rules read against the cited code |
| 5b | The margin table (§24.5) | PASS | Recomputed exactly (12). Defect D1 (one cell of the markdown copy, non-blocking) |
| 6 | New partition specification, development to 2026-09-06, as a new file | PASS | `partitions-development.json` (new); binds the calendar and mask hashes; `data/partitions.json` unchanged |
| 7 | Eligibility calendar: exclusions by target completeness and v5's failing inputs (prices, load forecast); weather excludes no day; no model, candidate or score | PASS | 40 exclusions recomputed (30 price-history, 10 load); landed `cp15.data.prepare` agrees exactly; no score column |
| 8a | Never-scored mask subtracting folds 1–5, v1 holdout, CP-16 slices, CP-24 gate days and search batches; fit/calibrate-only days listed apart | PASS | Recomputed and set-equal (12). Observation O1 |
| 8b | Old-fold days, folds 2–5; fold 1 inside CP-26's warm-up | PASS | 360 days (358 eligible); fold 1 flagged separately |
| 9a | Boundary guard (§24.2) with its tests: rows 2026-09-06 21:00/22:00 UTC; run 2026-09-06 00 UTC refused; run 2026-09-05 f048 admitted; leads outside f021–f048 refused | PASS | `tests/cp25/test_guard.py`, 103 passed (5); every logged request within scope (12) |
| 9b | Credentials: no value in a log, URL or error message, with tests | PASS | Redaction and scan tests; URL credential refusal tests; scans clean (8, 9) |
| O1 | Output: the manifest with hashes | PASS | All 62 hashes verified (12) |
| O2 | Output: the weather features for the gaps | PASS | Rebuilt byte-identical (6); reconstructed (11) |
| O3 | Output: the tier register | PASS | `tier-register.md`, `.json` |
| O4 | Output: partition specification, eligibility calendar and masks | PASS | Rebuilt byte-identical (6) |
| O5 | Output: the retrieval log | PASS | `retrieval-log.csv`, 16,553 requests, audited (12) |
| R | No raw GRIB bytes or decoded grids committed, under `DATA-LICENSE.md` | PASS | No `.grib2`, `.idx`, `.npz` path; "GRIB" occurs only as text; parquet columns are scalars; `DATA-LICENSE.md` unchanged; `rights-notice.md` present |
| C1 | Ceiling: 24 machine-hours | PASS | 1.39 h in all, the review included |
| C2 | Ceiling: at most 4 concurrent workers | PASS | Peak 4 |
| C3 | Ceiling: at most 40 GiB transient transfer | PASS | 14.74 GiB |
| C4 | Ceiling: $0 | PASS | Two anonymous archives only; `cost_usd` 0 |
| N | Not in CP-25: any new source | PASS | Retrieval hosts are the two admitted GFS archives; documentation pages only, listed |
| G | Gates: ratified section, Owner's retrieval approval, issued brief (the LAND is the Owner's, after this verdict) | PASS | Anchor hash; approval quoted in the brief; brief packaged byte for byte |
| T | Tier register and margin table ready for the Owner's rulings | PASS | `report.md` §7: load forecast tier 3; target finality evidence; shifts classed none / structural / partial |
| §1 | Preserved files untouched | PASS | Commands 3, 4 |
| §2 | Released-error rule unchanged (complete days ≤ D−2) | PASS | Register row for the H layer's released errors, D−2 group margins 45–47 h |
| §15.3 | Missing-weather rule; weather excludes no day; lateness not silently applied | PASS | Rule cited; two per-run exceptions kept as extracted and named for the Owner, not reclassified unilaterally |
| §24.2 | Red line, exposure | PASS | Newest run 2026-09-05, newest feature instant 2026-09-06 21:00 UTC; no exposure by this review (see below) |
| U | Untouchable files byte-identical to `1459ee2`; diff lists only new CP-25 paths | PASS | Commands 3, 4 |
| X1 | Reproduction 1: tests, 103 passed | PASS | Command 5 |
| X2 | Reproduction 2: 19 files byte-identical | PASS | Command 6 |
| X3 | Reproduction 3: conversion identity | PASS | Command 7 |
| X4 | Reproduction 4: credential scan `{}` | PASS | Commands 8, 9 |
| X5 | Reproduction 5: optional network re-fetch | NOT RUN (optional) | No retrieval made; X6 covers reconstruction |
| X6 | Reproduction 6: independent reconstruction from retained raw messages | PASS | Command 11, all 7 runs |

### Non-blocking defects (documentation only; no number, class, exclusion or ruling changes)

- **D1.** `tier-register.md` §5, row "Prices (2) | D−1 prices: lags, statistics, normalisation,
  the D−1 training target", column "Margin range": says
  **21–22 h**. The computed `margin-table.csv` says 21.0–23.0 h: on a fall-back transition day D−1
  the margin is 23 h. Recommended correction: "21–23 h".
- **D2.** `report.md` §3, `load_forecast_mw` row: calls the single null hours of 2023-10-29 and
  2024-10-27 "the repeated fall-back hour". `inventory-gaps.csv` records them at 2023-10-28 and
  2024-10-26 22:00 UTC, local hour 0: the first hour of the 25-hour day, not the repeated 02:00
  hour. Cause ("source") and the two exclusions are correct.
- **D3.** The committed `docs/track-b/evidence/cp-25/logs/tests-cp25.log` records "102 passed, 1
  deselected", not the 103 the assignment expects; this review's run gave 103 passed.

### Observations for the Owner (not defects against the bar)

- **O1. What counts as "scored".** The mask subtracts exactly the four sources §24.6 item 8 names.
  `report.md` §5 adds an audit that CP-23's training-only configuration selection lies inside
  CP-24's gate days. The same reasoning would reach the training-only inner-validation selections
  of CP-15 (LEAR penalty), CP-21 (capacity, the last 28 days of each window) and CP-22 (PN-sel),
  which the report does not mention. Their earliest inner-validation days fall in the genuine
  warm-up buffers that the mask counts as never scored. Whether training-only inner validation is
  "a selection" or fitting is an interpretation for the Owner; the bar as written is met.
- **O2. Two GFS runs** (deliveries 2022-12-01 and 2023-01-21) have AWS writes after the issue time.
  `LastModified` cannot separate lateness from a re-upload; the features are kept as extracted and
  named for a §15.3 ruling. The outputs hold no comparison of run 2022-11-30's six AWS-sourced leads with NCAR copies.
- **O3. The full suite** (`tests-full-suite.log`) has 3 failures and 12 errors, all in
  `tests/test_22_wasm_equivalence.py`, because the generated `app/public/` is absent. That is
  unrelated to CP-25 and outside this bar.
- **O4. Reconstructed availability for GFS** uses 30-day running-average completion times; for
  runs after 2026-06-14 the later bracket is the dossier's 2026-09-23 capture. That capture is NCEP
  production timing committed at CP-20, not a market value or event; the report discloses it.

### Exposure (§24.2)

None by this review. No delivery day after 2026-09-06 was fetched, stored or read, and no market
value or event after 2026-09-06 was read. The only documents read were the three legislation pages
listed in command 13.

## On FAIL only

Not applicable (PASS).
