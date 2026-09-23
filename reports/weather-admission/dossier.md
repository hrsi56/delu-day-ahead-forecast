# Weather-archive admission dossier — programme 4.1

**Engineering Lead return · 2026-09-23 · local only.**
- **Authority:** the Owner-carried executor handoff for programme 4.1, anchored on
  `capstone_v21.md` (v21-r3) §§2–3 and on programme plan
  `docs/track-b/v3-plan-handoff-2026-09-22.md` §4.1, §4.B, §5.9 and §3.2.
- **Repository start:** `main` at `110ce15e8b8fff4cc9b08e33e1b948ad9a50c310`.
- **Not done:** no model checkpoint, experiment, fit, full extraction, CP-17 work, governance
  or progress edit, staging, commit or publication.
- **Scope of the result:** historical admission only. It does not certify live suitability,
  which belongs to 4.9.

## 1. Result

| Archive | Folds 1–5 | Fields u10 / v10 / u_hub / v_hub / radiation |
|---|---|---|
| **GFS 0.25°** (NCAR d084001 + NCAR-linked NOAA AWS copy of the same product) | **ADMIT** in all 5 folds | **ADMIT** for all 5 fields (25 of 25 scopes) |
| **OCF ICON-EU** (Hugging Face, revision `d3dea71`) | **NOT_ADMITTED** in all 5 folds | **NOT_ADMITTED** for all 5 fields (25 of 25 scopes) |

The per-scope table, with reasons, coverage counts, decoded versions and the availability
basis for each archive × fold × field, is [`verdicts.csv`](verdicts.csv).

### Why GFS is admitted in every fold

- **Coverage is complete.** All 2,468 required D−1 00 UTC runs are present with all 10
  required leads.
  - The NCAR-only years 2019–2020 (731 runs) are complete. Each of their 7,310 lead files
    has an exact size and ends with the GRIB end section `7777`.
  - AWS from 2021 on (1,737 runs) is complete except 2021-02-02, and NCAR supplies that run.
  - 17,360 of 17,370 AWS `.idx` files were read and all contain the five target records. The
    other 10 belong to the absent 2021-02-02 run (HTTP 404).
- **The two endpoints hold the same product.**
  - On the sampled overlap runs, the target GRIB messages are byte-identical (sha256).
  - Catalog sizes agree for 1,735 of 1,736 overlap runs.
  - The exception is a truncated NCAR copy, 2024-09-15 f039: 251.9 MB against 540.8 MB on
    AWS, with no end marker. AWS supplies that run.
- **Decoded samples pass in every model version.** Twelve runs were decoded, covering v14,
  v15.1 and v16.
- **Publication before D−1 11:00 UTC is reconstructed for every fold.** Dated NCEP
  production-status captures from 2019-01 to 2026-06 bracket each fold and put the 00 UTC
  "48hr PRODUCTS" completion at 03:42–04:00 UTC (30-day running averages).

### Why ICON is not admitted

- **Hub-height wind: FIELD_UNSUPPORTED.** The archive holds 10 m wind and isobaric wind
  only, and pressure levels are not turbine heights.
- **u10, v10 and radiation: ARCHIVE_ABSENCE in every fold.**

| Fold | What is missing |
|---|---|
| 1 and 2 | 2019 history; the archive starts 2020-01-01 |
| 3 | 39 of 847 required runs, including the last 8 evaluation days (2022-09-20..27) and 3 warm-up days |
| 4 | 170 absent runs plus 7 stub files in March 2024 (177 of 850), including 6 warm-up days |
| 5 | The archive ends 2025-08-09, before the whole evaluation window |

- **Isolated field defects:** 2024-01-23 has no `aswdifd_s`, and 2020-02-13 has no 10 m wind.
- **Access and budget:** no access or budget gap contributed. Every ICON gap is archive
  absence, an archive defect or unsupported content.

## 2. Frozen protocol

- **Manifest.** [`sample-manifest.json`](sample-manifest.json) (sha256 `e2e6dbc6…c11e458c`)
  was frozen at **2026-09-23T12:50:58Z**, before any sample retrieval. Selection used only
  file-existence metadata, the dated schedule sources and the plan documents.
  - It fixes the information boundary, required windows, fields, leads, sample runs,
    substitution rule and admission rule.
  - The later radiation-precision criterion (§5.3) is a Lead-fixed check definition, added
    after the frozen generic "averaging checks"; it is disclosed as such.
- **Information boundary.** The origin is D−1 12:00 fixed CET, i.e. **D−1 11:00 UTC**. The
  run is D−1 00 UTC. Delivery days follow the Europe/Berlin calendar, with 23, 24 or 25
  hours.
  - Hour starts relative to the run: CEST days h22–h45, CET days h23–h46, spring-forward
    days h23–h45, fall-back days h22–h46. The union is **h22–h46**.
- **Required windows.** These come from the inherited CP-15 genuine warm-up lineage
  (`reports/cp15/lineage_summary.csv`, sha256 `273e0934…`) under
  `max(2019-01-01, D−728)`:

| Fold | Delivery days | D−1 00 UTC runs | Evaluation | First warm-up |
|---|---|---|---|---|
| 1 | 2019-01-01..2020-09-28 | 2019-01-01..2020-09-27 | 2020-07-01..09-28 | 2020-06-02 |
| 2 | 2019-03-04..2021-06-29 | 2019-03-03..2021-06-28 | 2021-04-01..06-29 | 2021-03-01 |
| 3 | 2020-06-04..2022-09-28 | 2020-06-03..2022-09-27 | 2022-07-01..09-28 | 2022-06-02 |
| 4 | 2023-04-02..2025-07-29 | 2023-04-01..2025-07-28 | 2025-05-01..07-29 | 2025-03-30 |
| 5 | 2023-12-13..2026-04-07 | 2023-12-12..2026-04-06 | 2026-01-08..04-07 | 2025-12-10 |

- **Boundary resolution at D−1.** Delivery day 2019-01-01 would need the 2018-12-31 00 UTC
  run, which is a pre-2019 input. It is not imported. Weather for that delivery day is
  structurally missing under the 2019 floor, is left to the 4.4D missing-input fallback, and
  is excluded from the coverage denominator. The earliest admissible run is 2019-01-01 00 UTC.
- **Admission rule.** ADMIT needs all five of:
  1. verified access;
  2. 100% of required runs present with every required lead or step for the field (either
     GFS endpoint may supply a run);
  3. per-run field presence;
  4. decoded samples of each model version or schema in the fold passing their checks;
  5. dated producer-side evidence of publication before D−1 11:00 UTC that brackets the
     fold window.

  Anything else is NOT_ADMITTED, with a reason class.

## 3. Access (verified, not presumed)

- **NCAR GDEX d084001.** Anonymous THREDDS `fileServer` with HTTP byte ranges (206).
  - Actual coverage was checked, not assumed. The 2026 catalog lists days through
    **2026-09-22**, and that day's files were modified 2026-09-23T12:32Z.
  - The landing page's "stop updating early 2026" warning and its future upper timestamp
    (2026-10-07) are recorded, not relied on.
- **NOAA AWS `noaa-gfs-bdp-pds`.** Anonymous. The bucket starts 2021-01-01, and the path
  gains `atmos/` from v16. The AWS registry and the NCAR landing page link the two copies.
- **OCF ICON-EU.**
  - `whoami` returned an authenticated user account (`Yarden-Viktor`, fine-grained token).
  - A 1-byte ranged read of a gated file returned **206**.
  - All reads were pinned to revision `d3dea71c0edcb04e08e396ab4bf55afd1fdcfcf5`.
  - The token was read from `launchctl` into child processes only. It was never printed,
    logged or written.
- No registration, paid workaround or replacement-provider search was used. Dynamical.org
  and Open-Meteo were not queried.

## 4. Coverage — inventories of every required run

Files: [`inventory/gfs_required_runs.csv`](inventory/gfs_required_runs.csv),
[`inventory/icon_required_runs.csv`](inventory/icon_required_runs.csv),
[`inventory/coverage_by_archive_fold_field.csv`](inventory/coverage_by_archive_fold_field.csv),
[`gaps.csv`](gaps.csv).

### 4.1 GFS

| Endpoint | What was inventoried | Result |
|---|---|---|
| NCAR | One THREDDS catalog per required day (2,468 days), recording presence, size and modified time of f021–f048; plus an exact size and last-4-byte read for every NCAR file used (7,320) | All 2,468 days have all 10 leads. For 2019–2020 and 2021-02-02: all files end with `7777`; smallest 92.0% of its version/lead median; size screen (< 90% of median) flags **0**. Across 2019–2026 the screen flags one file, 2024-09-15 f039, truncated on NCAR only |
| AWS | ListObjectsV2 per day (2021-01-01..2026-04-06, in the fold windows) | 1,736 of 1,737 runs complete with `.idx`; **2021-02-02 00 UTC absent** |
| AWS `.idx` | Suffix read of every required index (17,370) | 17,360 read, all with the five target records; 10 are 404 (the absent 2021-02-02 run); 0 needed a full-file fallback |
| Combined | Chosen endpoint per run | 731 NCAR (field basis: file intact — exact size and `7777` end section — plus the decoded layout of its version) + 1 NCAR fill (2021-02-02, intact) + 1,736 AWS (field basis: idx-verified) = **2,468 of 2,468** |

- **Cross-endpoint compatibility.**
  - For sampled runs 2021-03-23 (first v16 run), 2026-03-28 and 2026-04-06, NCAR and AWS
    file sizes are equal for all 10 leads.
  - All five target messages at f024 and f048 have identical sha256 on both endpoints.
  - Over the 2021–2026 overlap, NCAR catalog sizes agree with AWS byte sizes for 1,735 of
    1,736 runs. The comparison allows for NCAR's catalog truncating sizes to 0.1 MB rather
    than rounding. The column is `ncar_aws_sizes_equal`.
  - The one disagreement is 2024-09-15 f039, where the NCAR copy is truncated (251,945,463
    bytes, no `7777` end section; AWS has 540,827,964 bytes). This single-endpoint defect
    is covered by AWS.
  - The grid is 1440 × 721 at 0.25°, starting 90°N 0°E, in every version.
- **Version and schema changes audited.**
  - v14 → v15.1 on 2019-06-12 12Z; the first v15 00 UTC run is 2019-06-13.
  - v15.1 → v16 on 2021-03-22 12Z; the first v16 00 UTC run is 2021-03-23, and the path
    gains `atmos/`.
  - v16 is current; the NCO code listing shows `gfs.v16.3.33`.
  - The message order changes between versions. The 10 m winds sit at about 67%, 71% and
    79% of the file for v14, v15 and v16.
  - DSWRF stays NCEP-local parameter 0/4/192 in all sampled versions. Its packing precision
    changes from 10 W m⁻² (v14/v15, decimal scale −1) to about 0.02 W m⁻² (v16).

### 4.2 ICON (OCF)

- **Archive span.** The tree listing at the pinned revision has 6,401 run files from
  2020-01-01 00Z to 2025-08-09 18Z; 1,747 of them are 00 UTC runs.
  - Ten files have unpadded names (for example `2023318_0` = 2023-03-18 00Z). They were
    normalised.
- **Field-level inventory.** Each of the 1,650 existing 00 UTC runs inside the fold windows
  was checked from its zip central directory plus array metadata: are all chunk objects for
  the four fields covering the Germany box and steps 22–47 present?
  - **1,641 pass.**
  - 7 are 242–246 kB stubs with no zip end record (2024-03-14, 15, 18, 20, 24, 27 and 29).
  - 2024-01-23 lacks `aswdifd_s`; 2020-02-13 lacks `u_10m`/`v_10m`.
  - 2025-03-07 is stored as **Zarr v3** (`zarr.json`, keys `c/…`) and passes once read as v3.
- **Schemas.**

| Period | Shape (steps × lat × lon) | Isobaric levels | Notes |
|---|---|---|---|
| 2020-01..2023-02 | 93 × 657 × 1097 (lon −23.5..45.0) | 6 | |
| from 2023-03 | 73 or 79 × 657 × 1377 | 20 | |
| all | chunks 37 × 326 × 350 | | Blosc2/zstd; one run in Zarr v3 |

- **Gap structure** (00 UTC runs in the windows). The longest complete stretches are 316
  days in fold 3 (2021-08-09..2022-06-20) and 234 days in fold 4 (2024-06-05..2025-01-24).

| Fold | Required | Field-complete | Gap classes |
|---|---|---|---|
| 1 | 636 | 260 (u/v) / 261 (radiation) | 375 outside archive span (2019) or absent; 1 field-incomplete (2020-02-13, no 10 m wind) |
| 2 | 849 | 514 / 515 | 334 outside span or absent; 1 field-incomplete (2020-02-13) |
| 3 | 847 | 808 | 39 run files absent (3 warm-up, 8 evaluation: 2022-09-20..27) |
| 4 | 850 | 673 (u/v) / 672 (radiation) | 170 absent (blocks of up to 57 days in 2024–2025), 7 stubs, 1 missing `aswdifd_s` (2024-01-23); 6 warm-up days (2025-03-29..04-03) |
| 5 | 847 | 450 / 449 | archive ends 2025-08-09; the whole evaluation window and part of the history are absent |

## 5. Decoded evidence (actual values and metadata)

- **Bundles.** 22 were decoded: 12 GFS and 10 ICON (see
  [`decoded/summary.csv`](decoded/summary.csv); per-run JSON in `decoded/`).
  - Every GFS message and ICON chunk was hashed (sha256) before decoding; the list is
    [`hashes/raw_sample_objects.sha256`](hashes/raw_sample_objects.sha256).
  - Decoding was local: ecCodes 2.49 for GRIB2, and zarr 2.18.7 with ocf-blosc2 for ICON.
- **Attempts.** 34 of the 48 allowed: 22 successes and 12 failures, all listed in
  [`usage/decode_attempts.csv`](usage/decode_attempts.csv).
  - 8 ICON attempts failed on a zarr-store wrapper fault before any chunk was read.
  - 1 ICON run was aborted to fix duplicate chunk reads.
  - 2 GFS NCAR runs were aborted while the v14/v15 message locator was calibrated.
  - 1 GFS AWS run was aborted after a connection stall and succeeded on retry.

### 5.1 Samples frozen before retrieval

| GFS run (endpoint, version) | Why | Delivery hours |
|---|---|---|
| 2019-01-01 (NCAR, v14) | earliest admissible run | 24 |
| 2019-03-30 (NCAR, v14) | spring-forward day | **23** |
| 2019-06-13 (NCAR, v15.1) | first FV3 00Z run | 24 |
| 2019-10-26 (NCAR, v15.1) | fall-back day | **25** |
| 2020-10-24 (NCAR, v15.1) | fall-back, folds 2–3 | **25** |
| 2021-03-23 (AWS + NCAR bytes, v16) | first v16 run | 24 |
| 2022-03-26 (AWS, v16) | crisis, spring-forward | **23** |
| 2022-08-25 (AWS, v16) | crisis peak, fold 3 evaluation | 24 |
| 2024-03-30 (AWS, v16) | modern spring-forward | **23** |
| 2024-10-26 (AWS, v16) | modern fall-back | **25** |
| 2026-03-28 (AWS + NCAR bytes, v16) | fold 5 evaluation spring-forward | **23** |
| 2026-04-06 (AWS + NCAR bytes, v16) | last required run | 24 |

The ICON samples were 2020-06-03 (earliest servable required run), 2020-10-24 (25 h),
2021-03-27 (23 h), 2022-03-26 (23 h, crisis), 2022-08-25 (crisis peak),
2023-02-28 (last early-schema run), 2023-03-25 (new schema, 23 h), 2023-04-01
(fold 4 start), 2024-10-26 (25 h) and 2025-07-28 (fold 4 end).

### 5.2 Metadata, units, averaging and alignment

- **GFS.** In every bundle, every lead f021–f048 was checked for all five fields:
  `10u`/`10v` (heightAboveGround 10), `u`/`v` (heightAboveGround **100 m**), and `sdswrf`
  (surface, template 4.8, statistical process 0 = average).
  - Units are m s⁻¹ and W m⁻².
  - All 600 messages are centre `kwbc`, significance of reference time 1 (start of
    forecast), production status 0 (operational) and generating process 2 (forecast) of
    model 96. They are operational forecasts, not analyses, hindcasts or reanalysis.
  - Validity time = init + lead for every message.
  - DSWRF averaging windows reset every 6 h (18–21, 18–24, 24–27 … 42–48). Three-hour
    block means are exact: A(L−3..L) directly when L ≡ 3 (mod 6), and 2·A(L−6..L) − A(L−6..L−3)
    when L ≡ 0 (mod 6).
- **ICON.**
  - `u_10m`/`v_10m` are instantaneous, height above ground, m s⁻¹.
  - `aswdir_s`/`aswdifd_s` are averages since forecast start, surface, W m⁻².
  - GRIB data type is `fc`. Steps 22–47 are present and contiguous (hourly to 78 h).
  - Hourly means come from (h+1)·A(h+1) − h·A(h). Global radiation = direct + diffuse.
  - The root `history` attribute records a cfgrib conversion in 2023 from OCF's stored DWD
    GRIB files. That is a format conversion, not a re-forecast.
- **Hour support.**
  - GFS: every hour start h22–h46 is bracketed by decoded 3-hourly endpoints (wind
    interpolation h21…h48) and lies in a decoded radiation block ending at h24…h48.
  - ICON: every hour start has its instantaneous step h and radiation endpoints h, h+1 ≤ 47.
  - Checked in every bundle, for 23-, 24- and 25-hour days.
- **Hub level.** GFS 100 m above ground is a documented height-above-ground level near
  typical hub heights, not a pressure level. ICON's archive has no such level, and its
  isobaric winds are not substituted.

### 5.3 Conversion precision (Lead-fixed check definition)

- **GFS.** Negative de-averaged block means are bounded by source packing precision (limit
  −3 quanta).
  - v14/v15 pack DSWRF at 10 W m⁻² (sometimes 1 W m⁻²); the observed minimum is −10 W m⁻²,
    one quantum.
  - v16 packs at 0.016–0.02 W m⁻²; the observed minimum is −0.04.
  - Recipes must clip to zero and disclose the coarser v14/v15 radiation resolution.
- **ICON.** Box-mean hourly radiation is never below −0.003 W m⁻², and at most 9×10⁻⁶ of
  point-hours are below −5 W m⁻².
  - The worst value is −42.7 W m⁻², at one Alpine grid point (47.19°N 12.75°E, h33,
    2023-04-01), in `aswdir_s`.
  - This is a property of DWD's direct-radiation field, not of the decoding.

## 6. Reconstructed availability before D−1 11:00 UTC

- **Sources.** Dated primary-source captures (Wayback raw mode) of the producers' own
  operational pages, with fingerprints in [`sources/fingerprints.csv`](sources/fingerprints.csv).
  The parsed values are in [`availability/`](availability/).
- **GFS** (NCEP production status, 00 UTC GFS, "48hr PRODUCTS" and full-forecast average
  end times, 30-day running averages per the page legend):

| Capture | Version | 48 h products avg end (UTC) | Forecast avg end |
|---|---|---|---|
| 2019-01-21, 2019-04-24 | v14 | 03:42:34, 03:42:29 | F00–F240 04:35 |
| 2019-06-17, 2019-08-18, 2020-10-31 | v15.1 | 03:43:26, 03:43:48, 03:45:31 | F000–F384 04:42–05:06 |
| 2021-04-08 … 2026-06-14 (11 captures) | v16 | 03:51:30–04:00:09 | 05:08–05:16 |
| 2026-09-23 (live page) | v16 | 03:53:34 | 05:13:59 |

- **GFS result.** Every fold window is bracketed; for example, fold 1 has 2019-01-21 before
  and 2020-10-31 after.
  - Each version has a capture whose 30-day window lies wholly inside it: 2019-01-21 and
    2019-04-24 for v14, 2019-08-18 and 2020-10-31 for v15.1, and 2021-12-06 onward for v16.
    2019-06-17 and 2021-04-08 straddle the model changes.
  - The latest 48 h completion is 04:00 UTC, leaving a margin of about 7 h to 11:00 UTC.
  - NCAR `modified` times, 1.5 days after the run, are ingestion times and were not used.
- **ICON** (DWD open-data directory listings for the 00 UTC run, publication timestamps of
  steps 021–048). Steps h21–h48 were published between **02:48 and 03:16** (listing time) on
  every captured day:

| Captures | Listings |
|---|---|
| 2022-03-08, 2022-05-16, 2022-08-16, 2022-12-04 | proxy variables `tot_prec`, `t_2m`, `t_g`, `u` from the same run |
| 2023-01-04, 2024-06-22, 2025-03-25/04-28/04-30, 2025-11-14, 2025-12-12 | the target variables themselves |
| 2020-01-22 | root directories last modified 21 Jan 2020 03:31–03:44 |

- **ICON result.**
  - Timestamps are identical in CET and CEST captures, which points to a fixed time base
    (UTC).
  - Folds 3 and 4 are bracketed. Fold 3's evidence is sparse between 2020-01 and 2022-03.
  - Folds 1, 2 and 5 are not established because the archive does not span them.
  - OCF's own card says collection ran "6–8 hours after forecast initialization". That is
    secondary and consistent with the above.
- **Not claimed.**
  - Schedules and 30-day averages do not prove uninterrupted delivery on every day.
  - Individual late or failed cycles are possible and are not excluded by this evidence.
  - A current schedule alone would not establish historical timing; every fold relies on
    dated captures from its own period.
  - Initialization, archive start and retrieval dates were not used as availability
    evidence.
  - No per-day contemporaneous log was required or claimed.

## 7. Gaps — archive absence versus access/budget

- **GFS:** none in the combined archive. Two single-endpoint defects are each covered by
  the other endpoint:
  - AWS lacks the 2021-02-02 run (NCAR has it, intact).
  - The NCAR copy of 2024-09-15 f039 is truncated (AWS has it, idx-verified).
- **ICON:** every gap is archive-side (see `gaps.csv`):
  - ARCHIVE_ABSENCE: outside the 2020-01-01..2025-08-09 span, or run file absent.
  - ARCHIVE_DEFECT: 7 stub zips.
  - FIELD_INCOMPLETE: 2 runs.
  - FIELD_UNSUPPORTED: hub-height wind.
- **Access gaps:** none. The gated access worked, and no request was refused.
- **Budget gaps:** none. Every planned inventory completed within the caps (§10).
- **Unresolved and open items:**
  - No DWD dated schedule document was found stating ICON-EU release times. ICON
    availability therefore rests on dated DWD server-listing captures.
  - The ICON Zarr v3 run (2025-03-07) was inventoried from metadata only, not decoded.

## 8. Options if weather work proceeds on a scope admission did not cover (§3.2) — not selected

GFS is admitted for the inventoried five-fold scope under the assumptions in §11. A
direct-weather comparison still requires a frozen missing-input rule: weather for delivery
2019-01-01 is structurally missing (§2), and unexpected missing/invalid inputs must be handled
explicitly. Admission is not a no-fallback guarantee. The §3.2 options below concern an
unadmitted extension such as ICON; none is selected by this dossier. The Orchestrator intake
also identifies eight additional runs needed for CP-16-style admission warm-up; these require
a targeted pre-fit check, not an assertion that this inventory already covered them.

1. **Modern folds only, with matched baselines and a scoped claim.**
   - ICON cannot serve fold 5 at all (archive end).
   - Fold 4 lacks 177–178 of 850 required runs, including 6 warm-up days, so it would also
     need a frozen missing-input fallback.
2. **Amended fold dates, keeping the 2019 input floor.**
   - ICON's longest complete 00 UTC stretches are 316 days (2021-08-09..2022-06-20) and
     234 days (2024-06-05..2025-01-24).
   - Any amended fold would need its full 728-day history inside such stretches or an
     explicit missing-input policy.
3. **A strictly causal proxy with its own label.** For example, the admitted GFS input used
   in place of ICON and labelled as GFS, or another as-issued proxy. Reanalysis must never be
   presented as a forecast.
4. **A modern-regime prospective evaluation after policy freeze.** Live DWD open data would
   need 4.9 live-suitability checks. This archive is not updated and cannot supply it.

The Owner chooses. This dossier makes no selection and does not rank the options.

## 9. Lineage requirements carried into any later extraction (4.1 → 4.4D)

A later extraction must record, per value:
- provider/model/version (v14, v15.1 or v16; ICON schema and Zarr format);
- init_time; documented dissemination and reconstructed `available_at` basis; valid_time;
  lead;
- endpoint, retrieval time, message or chunk sha256, source URL and byte range, and dataset
  revision;
- units; grid (0.25° or 0.0625°) and the zonal aggregation recipe;
- wind height (10 m, 100 m);
- radiation averaging and the de-averaging formula, with clipping and the packing quantum;
- the interpolation rule for hour starts between 3-hourly endpoints;
- missingness, including the structural 2019-01-01 boundary day.

Reject analyses, hindcasts, later updates and stitched products; all sampled GFS messages
are operational forecasts. The 3-hour GFS radiation blocks and the linear wind
interpolation are 4.4D recipe decisions to freeze before scoring. This dossier does not
fix them.

## 10. Usage against ceilings

Measured values are in [`usage/transfer.json`](usage/transfer.json),
[`usage/decode_attempts.csv`](usage/decode_attempts.csv) and `usage/ceilings.md`.

| Ceiling | Maximum | Used |
|---|---|---|
| Active hours | 16 | ≈1.5 h |
| Archive products | 2 | 2 (GFS via NCAR + NOAA AWS; OCF ICON-EU) |
| Initialization runs decoded | 24 (12 + 12) | 22 (12 GFS, 10 ICON) |
| Decoding attempts | 48 | 34 (22 success, 12 failure) |
| Native fields per bundle | 6 | GFS 5 (DSWRF is total radiation); ICON 4 (hub u/v unsupported, not retrieved) |
| Transfer | 4 GiB (stop line 3.85) | **3.43 GiB** (51,092 metered requests) |
| Additional disk | 8 GiB | peak 1.87 GiB; 1.73 GiB retained in `.local/` |
| Aggregate RSS | 8 GiB | ≤ 0.56 GiB summed |
| Machine hours / CPU cores | 8 / 4 | ≈1.3 h wall time; ≤ 1 core-equivalent; ≈0.07 CPU-h sampled |
| Cost / fits / full-archive downloads | $0 / 0 / 0 | $0 / 0 / 0 |

- **Where the transfer went:**
  - ICON samples: 1.88 GiB. That includes about 0.75 GiB of duplicate chunk reads from a
    store-wrapper fault in the first seven runs, found and fixed mid-run, and counted rather
    than excluded.
  - GFS samples: 0.68 GiB.
  - GFS inventory: 0.58 GiB.
  - ICON inventory: 0.20 GiB.
  - Dependencies, discovery, comparisons and sources: 0.10 GiB.
- **Hour ceiling:** the 16-hour stop was not reached.

## 11. Assumptions and exceptions (disclosed)

1. **GFS field presence for NCAR-only 2019–2020 runs** is inferred per run, from:
   - each file's presence, exact size and intact GRIB end section;
   - no file smaller than 92% of its version/lead median;
   - the version's decoded message layout (5 decoded runs across v14 and v15.1; targets lie
     within the first 88% of the file).

   NCAR has no index files, and reading every message header of 7,310 files would cost
   roughly 5 million range requests.
2. **NCEP production-status averages** are production completion times at NCEP.
   Dissemination to public servers is assumed to follow within minutes. The 7 h margin
   absorbs this, but it is not separately evidenced.
3. **ICON listing times** are taken as UTC server times, on the basis of DST invariance. If
   they were CET/CEST local times, the true UTC publication times would be 1–2 h earlier.
4. **The Germany box** (47.0–55.25°N, 5.5–15.5°E) is an evidence domain, not the zonal
   aggregation recipe.
5. **The radiation-precision criterion** (§5.3) was defined after the manifest froze. It
   replaced an ad-hoc −5 W m⁻² floor that was never pre-registered.
6. **Dependency transfer** is logged as an interface-counter delta during installation. That
   is an upper bound, because it includes concurrent traffic.
7. **Resource sampling** began at 13:10Z. The single-run RSS measurements before then
   (150–170 MB per process) were taken with `/usr/bin/time`.

## 12. Files

- `dossier.md` (this file) · `verdicts.csv` · `sample-manifest.json` · `gaps.csv`
- `inventory/` · `availability/` · `decoded/` (per-run JSON + `summary.csv`)
- `sources/fingerprints.csv` + `sources/source-extracts.md` · `usage/` · `hashes/`
- `estimates.md` · `rights-and-service-limits.md` · `reproduction.md` · `scripts/`
- Raw caches, source copies and logs (not committed; account in `usage/ceilings.md`):
  `.local/weather-admission/`
