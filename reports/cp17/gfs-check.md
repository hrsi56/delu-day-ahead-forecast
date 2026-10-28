# CP-17 item 1 — the A1 GFS check

**Status: the brief's rule is met, so CP-17 stops here and returns BLOCKED for the Owner's decision.**
On the GFS +6 h affected dates, v2 is more than 2% worse than A1's GFS +6 h route on both MAE (+2.27%)
and WIS (+6.68%).

Evidence class `development_post_selection`. Descriptive only, from CP-26's stored forecasts; nothing
was trained. Machine record: [`gfs-check.json`](gfs-check.json); daily rows:
[`gfs-check-daily.csv`](gfs-check-daily.csv); code: `src/cp17/tools/gfs_check.py`.

## What is compared

| Stream | Source in CP-26's forecast ledger |
|---|---|
| A1 nominal | `members.nominal.D2.quantiles`: DDNN-2's own seven Johnson SU quantiles, on nominal weather |
| A1 GFS +6 h | `members.gfs6.D2.quantiles`: DDNN-2 in CP-26's `gfs6` route |
| v2 nominal | `policies.nominal/v2.native_quantiles`: blended LEAR with the H layer; it uses no weather |

- **The `gfs6` route,** as CP-26 ran it (`src/cp26/harness.py`, ruling 3): the three weather columns are
  missing under §15.3 on every one of CP-25's 1,783 GFS +6 h affected dates. This applies in training and at
  the forecast, and the route has its own 14 DDNN-2 searches.
- **Scores:** `cp28.scoring.daily`: p50 MAE and the seven-quantile WIS, in EUR/MWh. Each date is scored on
  CP-25's frozen eligible keys, hours are averaged within a date, and dates weigh equally (§24.7).
- **Calendar:** CP-26's scored dates, 2020-12-29 to 2026-09-06, 2,068 eligible dates.
- **Masks:** CP-25's classification in `reports/development-inputs/margin-days.csv`, group `gfs`, column
  `affected_plus_6h`.
- **Population:** paired. A date counts when all three streams have valid native quantiles on every
  eligible key. A date missing any stream is counted, never filled.

## The table

Mean daily loss in EUR/MWh on the paired dates, with the ratios between streams.

| Mask | Eligible dates | Paired dates | A1 nominal missing | MAE: A1 nominal | MAE: A1 +6 h | MAE: v2 | WIS: A1 nominal | WIS: A1 +6 h | WIS: v2 | v2 vs A1 +6 h, MAE | v2 vs A1 +6 h, WIS | A1 +6 h vs A1 nominal, MAE | A1 +6 h vs A1 nominal, WIS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| affected | 1,358 | 1,354 | 4 | 16.8086 | 21.7073 | 22.2003 | 9.5117 | 12.5014 | 13.3370 | +2.27% | +6.68% | +29.14% | +31.43% |
| unaffected | 710 | 696 | 14 | 16.8528 | 17.2349 | 23.1996 | 9.3957 | 9.6593 | 13.5321 | +34.61% | +40.09% | +2.27% | +2.81% |
| every eligible date | 2,068 | 2,050 | 18 | 16.8236 | 20.1889 | 22.5395 | 9.4723 | 11.5365 | 13.4032 | +11.64% | +16.18% | +20.00% | +21.79% |

- **Missing dates.** v2 and the +6 h route have a native forecast on every eligible date. On 18 dates
  between 2022-12-04 and 2023-06-20, A1 nominal has none: one of its eight members stopped with
  `TrainingFailure: no kept epoch (nonfinite_loss …)`, and CP-26 scored B0 instead.
- **Sensitivity.** Dropping the pairing with A1 nominal leaves all 1,358 affected dates. On them v2 is
  +2.30% worse on MAE and +6.71% on WIS. The conclusion is the same.

## The rule (brief, Observable outcome 1)

> If v2 is more than 2% worse than A1's GFS +6 h route on the affected dates on *both* MAE and WIS, stop and
> return BLOCKED with the table, for the Owner's decision.

v2's excess over A1's +6 h route on the affected dates is +2.27% on MAE and +6.68% on WIS. Both are above 2%,
so the outcome is **BLOCKED**.

## Checks of the arithmetic

Each daily loss here was compared with the losses CP-26 and CP-28 stored themselves:

| Stream | Stored reference | Dates | Equal bit for bit | Largest difference |
|---|---|---:|---:|---:|
| v2, MAE | CP-26 `daily` table, `nominal/v2` | 2,068 | 2,068 | 0 |
| v2, WIS | CP-26 `daily` table, `nominal/v2` | 2,068 | 2,004 | 1.4e-14 |
| A1 nominal, MAE | CP-26 `daily` table, `nominal/D2` | 2,050 | 2,050 | 0 |
| A1 nominal, WIS | CP-26 `daily` table, `nominal/D2` | 2,050 | 1,995 | 1.4e-14 |
| A1 nominal, MAE | CP-28 `daily-losses.parquet`, arm A1 | 2,050 | 2,050 | 0 |
| A1 nominal, WIS | CP-28 `daily-losses.parquet`, arm A1 | 2,050 | 2,050 | 0 |

The 1.4e-14 differences come from summation order in the WIS.

Every ledger file read was checked against CP-26's `scores-manifest.json` (`b9f10917…`). The extract was
checked file by file against the `evidence/cp-26` tree. No date after 2026-09-06 was read.

## What the measurement does and does not say, for the Owner's decision

- **The +6 h route is a different model from the product's A1.** DDNN-2 was trained and searched there with
  the weather missing on about 64% of dates.
- **The case the fallback rule is for was not measured.** That case is a nominally trained A1 meeting a single
  late run, whose missing weather appears only at that forecast. Nominal weather is missing on only three
  dates: 2019-01-01 (structural, before the grids' first run) and the two ruling-4 dates (2022-12-01 and
  2023-01-21). So no nominal training window contains more than two dates with missing weather. Measuring the
  case would be a new switching experiment, which decision 2 excludes.
- **Both options are degraded.** On the affected dates, the +6 h route is about 29% (MAE) and 31% (WIS) worse
  than A1 on nominal weather. v2 is a further 2.3% and 6.7% worse.
