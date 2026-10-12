# CP-25: the frozen development inputs, 2019-01-01 to 2026-09-06

**Anchor:** capstone v21-r13 §24.6 (SHA-256 `173799d8…25a8`), governed by §24.2, §24.4 and §24.5.
**Evidence class:** a data checkpoint. Nothing is forecast or scored here.

**The boundary.** No delivery day after 2026-09-06 was fetched, stored or read.
- The newest GFS run is 2026-09-05 00 UTC; its f048 message serves delivery day 2026-09-06.
- Every request passed the guard in `src/cp25/guard.py`.

## 1. What is frozen

| Output | File |
|---|---|
| The manifest, with hashes | [`manifest.json`](manifest.json) |
| GFS weather features for the gaps (329 delivery days) | [`weather-features-gaps.parquet`](weather-features-gaps.parquet) |
| The run manifest, per-message provenance, per-run status, the targeted checks, the AWS listings (per-run availability evidence) and the attempt outcomes | [`gfs-run-manifest.json`](gfs-run-manifest.json), [`gfs-messages.parquet`](gfs-messages.parquet), [`gfs-runs.csv`](gfs-runs.csv), [`gfs-targeted-checks.csv`](gfs-targeted-checks.csv), [`gfs-aws-listing.jsonl`](gfs-aws-listing.jsonl), [`gfs-attempt-outcomes.json`](gfs-attempt-outcomes.json) |
| The conversion-identity control | [`conversion-identity.json`](conversion-identity.json) |
| The inventory | [`inventory-series.json`](inventory-series.json), [`inventory-by-year.csv`](inventory-by-year.csv), [`inventory-gaps.csv`](inventory-gaps.csv), [`inventory-weather-by-year.csv`](inventory-weather-by-year.csv) |
| The tier register, the missing-input rules and the margin table | [`tier-register.md`](tier-register.md), [`tier-register.json`](tier-register.json), [`margin-table.csv`](margin-table.csv), [`margin-days.csv`](margin-days.csv) |
| The new partition specification (a new file; `data/partitions.json` is unchanged) | [`partitions-development.json`](partitions-development.json) |
| The eligibility calendar | [`eligibility-calendar.csv`](eligibility-calendar.csv), [`ineligible-hours.csv`](ineligible-hours.csv) |
| The record masks | [`record-masks.csv`](record-masks.csv), [`record-masks.json`](record-masks.json) |
| The retrieval log | [`retrieval-log.csv`](retrieval-log.csv) (every metered request) |
| Resources, rights, repairs and reproduction | [`resources.json`](resources.json), [`rights-notice.md`](rights-notice.md), [`defects-and-repairs.md`](defects-and-repairs.md), [`reproduce.md`](reproduce.md) |

## 2. Weather for the gaps

**Runs.** The extraction covered 329 GFS 0.25° D−1 00 UTC runs, all v16:
- runs 2022-09-28 to 2023-03-23 (177), serving delivery days 2022-09-29 to 2023-03-24;
- runs 2026-04-07 to 2026-09-05 (152), serving delivery days 2026-04-08 to 2026-09-06.

None lies in the admission inventory. Each one took §15.2's targeted checks:
- an exact AWS listing per lead (object, index, size and `LastModified`);
- the `.idx` record for each of the five fields;
- local decoding, with CP-20's field-by-field metadata validation: grid, level, step, units,
  averaging bounds, operational forecast status and version.

**Result.** All 329 runs were complete: 16,450 messages, with no nonfinite box values.
- CP-20's extractor ran unchanged, by import (`cp20.extract.Extractor`, `cp20.gfs`, `cp20.net`),
  behind CP-25's guard.
- **328 runs** came wholly from AWS.
- **Run 2022-11-30** took four leads (f027, f033, f036, f045) from NCAR d084001. Those leads
  failed GRIB framing on AWS, where the objects had been rewritten that afternoon, and each used
  its one same-product alternate attempt. The four failed lead-tries count as 20 message attempts
  out of the 49,350 allowed.
- **Raw messages** of 7 runs are retained under `.local/` for independent reconstruction. Nothing
  raw is committed.

**Features.** CP-20's frozen conversion (`cp20.weather.build_features`) produced 7,897 canonical
hours, all with status `ok`, in exactly CP-20's columns and dtypes.
- **Control:** the same import path re-converts all 2,476 of CP-20's retained runs and reproduces
  CP-20's committed `weather-features.parquet` bit for bit: 59,446 rows, maximum difference 0.0.
- **Coverage:** CP-20's file and this one together hold a weather record for every development
  delivery day, 2,806 days, each exactly once. Delivery 2019-01-01 stays structurally missing
  under §15.3.

## 3. The inventory

Prices and load are not re-pulled. They come from the preserved bytes of `data/snapshot.parquet`
(pulled from SMARD on 2026-09-08, CC BY 4.0).

| Series | Product | Gaps by year | Cause |
|---|---|---|---|
| `price_eur_mwh` | SDAC DE-LU day-ahead price (SMARD 4169). Hourly MTU through 2025-09-30; four 15-minute prices averaged per hour from 2025-10-01. | none in any year | — |
| `load_forecast_mw` | ENTSO-E 6.1.B day-ahead total load forecast (SMARD 411) | 2022: 144 h (6 days); 2023: 49 h (3 days, one of them the repeated fall-back hour on 2023-10-29); 2024: 1 h (the repeated fall-back hour on 2024-10-27) | **Source**: every null hour had zero source quarter-hours |
| A69 wind and solar forecasts (3 columns) | not inputs (§2) | 1 h each in 2023, 2024 and 2025 (onshore and solar); none offshore | source |
| A75 actuals (3 columns) | not inputs | 1 h in 2025 (onshore and solar) | **our extraction**: partial hours fail-closed to null |
| GFS weather | three derived columns | before CP-25: 2022: 94 days and 2023: 83 days (2022-09-29 to 2023-03-24), 2026: 152 days (2026-04-08 to 2026-09-06); after CP-25: none; delivery 2019-01-01 structural | before CP-25, **our extraction** (outside CP-20's scope); 2019-01-01, **structural** (run before the 2019 floor) |
| Calendar features | computed | none | — |

Source, licence, granularity and timezone of each series are in
[`inventory-series.json`](inventory-series.json). Every null hour is listed with its cause in
[`inventory-gaps.csv`](inventory-gaps.csv).

## 4. The eligibility calendar

2,766 of the 2,806 development days are eligible. Exclusions follow only target completeness and
the inputs whose absence makes the as-landed v5 fail. The verdict is the landed `cp15.data.prepare`'s
own, and independent reasons must explain it exactly.

- **30 days, 2019-01-01 to 2019-01-30:** price inputs absent. There is no 720-hour price history
  before the 2019 floor.
- **10 days:** load forecast absent. Eight are whole days: 2022-02-22, 2022-03-24, 2022-07-20,
  2022-07-21, 2022-12-21, 2022-12-22, 2023-03-13 and 2023-08-31. The other two are 2023-10-29 and
  2024-10-27, where one null hour of the 25-hour day nulls the day mean.
- **Target completeness** excludes no day: every canonical hour has a finite price.
- **Weather** excludes no day (§15.3).
- **45 single hours** stay ineligible on otherwise eligible days, as in the landed code: local
  hour 2 after a DST change, whose 24/48/168 h lag is absent or ambiguous. They are listed in
  [`ineligible-hours.csv`](ineligible-hours.csv).

Within §24.7's windows (counted for reference only):
- the scored calendar 2020-12-29 to 2026-09-06 has 2,068 eligible days of 2,078;
- the warm-up 2020-01-01 to 2020-12-28 has 363 of 363.

## 5. The record masks

A day counts as scored if a forecast's loss on it entered a reported result, a selection or an
admission decision. The never-scored mask subtracts §24.6's four sources:

| Source | Days |
|---|---|
| Folds 1–5 evaluation days | 450 |
| v1's holdout, 2026-06-09 to 2026-09-06 | 90 |
| CP-16's training-only admission slices (seven per fold) | 35 |
| CP-24's gate days, five windows of 56 | 280 |
| CP-24's search batches: one round, 43 batches of 28 days | 901 unique |
| **Union (scored)** | **1,639** |

- **Never scored:** 1,167 development days, 1,132 of them eligible.
- **Old-fold days, folds 2–5:** 360 days, 358 of them eligible.
- **Fold 1** (2020-07-01 to 2020-09-28) lies inside CP-26's warm-up.

Days used only to fit or calibrate are listed apart and not subtracted:
- v1's fold calibration windows, 300 days;
- v1's final calibration window, 60 days;
- the genuine warm-up buffer days, 188 days;
- in all, 213 days lie in these windows and in no scored source; they are flagged
  `fit_or_calibrate_only`.

**Audit.** CP-23's per-fold training-only configuration selection (holdout and early-stopping
days) also meets the definition. Each of its five 56-day windows lies wholly inside CP-24's gate
days, so the four named subtractions already cover it. The build refuses if that ever stops being
true.

## 6. Tiers, margins and missing-input rules

See [`tier-register.md`](tier-register.md). In short:
- **Prices and the target price:** tier 2, with SDAC result finality documented and SMARD's
  "update possible" caveat disclosed.
- **Day-ahead load forecast:** **tier 3**, because its originality cannot be established.
- **GFS:** tier 2, with per-run evidence for 327 of the 329 new runs and two named exceptions.
- **Calendar features:** admissible. **Hindsight labels** `crisis_period` and `post_crisis`:
  inadmissible.

## 7. Summary for the Owner's rulings (§24.5)

1. **Tiers.**
   - **Tier 3 among the inputs of B0 or v1–v5: the day-ahead load forecast.** It is used by
     v1-R (`load_forecast_mw`, `load_forecast_day_mean_mw`), by LEAR's and LightGBM's load of D
     and LEAR's D−1 and D−7 load lags (v2–v5), and by DDNN-2's `load_d0` (v5).
   - B0 has no tier-3 input.
   - Under §24.5, CP-26 does not start until the Owner rules: a variant without the load
     forecast, or a recorded exception. CP-25 registers no substitute, because none of tier 1 or
     tier 2 exists in the preserved data under the short path.
   - Prices (target and lags) and GFS are tier 2. Calendar features are admissible; the two
     hindsight labels are inadmissible.
2. **The target price's finality.** Documented:
   - CACM Art. 47(5): matched orders are firm.
   - Art. 39(2)(a): one clearing price per zone and MTU.
   - Art. 48: TSOs and NEMOs verify the results before delivery.
   - Reg. 543/2013 Art. 12(2)(d): published no later than one hour after the gate, with no
     update wording.

   Caveat: SMARD's manual says a later update of published price data "ist möglich", and no
   vintage shows that none occurred. The Owner may accept tier 2 or rule otherwise.
3. **Tier-2 groups' shifts:**

   | Group | +1 h | +6 h | +24 h |
   |---|---|---|---|
   | Prices (D−1) | none | none | structural |
   | Prices (D−2 and older) | none | none | none |
   | GFS | none | **partial**: 1,783 of 2,805 days, all CEST days plus 131 CET days | structural |
   | Load forecast (tier 3; for an exception only) | **structural**: deadline D−1 10:00 against issue 11:00 | structural | structural |

4. **GFS per-run exceptions** for the Owner's attention:
   - delivery 2022-12-01 (run 2022-11-30): AWS objects written at 15:10–15:38 UTC;
   - delivery 2023-01-21 (run 2023-01-20): two index files rewritten at 10:20 and 11:40 UTC.

   Both are kept as extracted and may be classed as documented lateness under §15.3.

## 8. Limits, stated plainly

- **Reconstructed availability.** Prices and GFS have availability reconstructed from documented
  deadlines and schedules, not from per-day arrival logs. An SDAC fallback day, or a late GFS run,
  can be later than the schedule. For prices, any delay shorter than 21 h would not cross the
  issue time.
- **What `LastModified` means.** It is the last write to the AWS mirror. It bounds availability on
  AWS from above for 327 runs, and proves nothing about NCEP's own dissemination.
- **The 2026-09-23 NCEP capture.** The dossier's capture of NCEP's production-status page, dated
  2026-09-23, brackets the runs after 2026-06-14. It is production timing for weather runs,
  already committed in the admitted dossier: not a market value or event.
