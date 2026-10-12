# CP-25 tier register and margin table

**Issue time:** D−1 11:00 Europe/Berlin, strictly before, as set in capstone v21-r13 §24.4. In UTC
that is 10:00 when D−1 is on CET and 09:00 when it is on CEST, using D−1's own offset at 11:00.

This register covers every input of B0, v1-R and v2–v5, in the three categories of §24.5. The
machine-readable copy is [`tier-register.json`](tier-register.json). The documents behind each
claim are listed at the end, each with its retrieval date. Only their text was read; no data was
fetched from them.

## 1. Published inputs

| Input | Members | Tier | Documented publication | Against the issue time | Finality / originality |
|---|---|---|---|---|---|
| **Target price**: the SDAC DE-LU clearing price, used as training targets and scoring truth | B0 (truth), v1-R, v2–v5 | **2** | No later than one hour after the 12:00 gate on the auction day, so 13:00 local on D−1 for delivery D [REG543-12, CACM-47] | A training target for delivery day D−1 was published by D−2 13:00, at least 22 h before the issue time (21 h on transition days). Day D's own price is the embargoed target. | **Documented.** Matched orders "shall be considered firm" [CACM-47 (5)]; there is one clearing price per zone and market time unit [CACM-39 (2)(a)]; TSOs and NEMOs verify the results before delivery [CACM-48]; and the publication duty carries no update wording [REG543-12]. **Caveat:** SMARD says a later update of published price data "ist möglich" [SMARD-D3.1], and its series follow TSO corrections [SMARD-B1.3]. No price vintage exists to show that no correction ever happened. The snapshot equals ENTSO-E A44 on all 120 sampled hours [RECON]. |
| **Price lags and price statistics** (listed below the table) | B0, v1-R, v2–v5 | **2** | The latest price used is delivery day D−1's, published by D−2 13:00 local | Strictly before, on every day, by at least 21 h | As for the target price |
| **Day-ahead load forecast** (listed below the table) | v1-R, v2–v5 | **3** | No later than two hours before the 12:00 gate, so D−1 10:00 local [REG543-6; SMARD-D2.2.1] | Strictly before by exactly 1 h, *if* the stored value were the original issue | **Not established.** The forecast must be updated "when significant changes occur" [REG543-6], at ±10% [SMARD-D2.2.1]. SMARD follows TSO updates without a fixed revision process [SMARD-B1.3]. The snapshot holds SMARD's values as pulled on 2026-09-08, with no issue or update time, so §24.5 treats it as tier 3. No tier-1 or tier-2 substitute exists in the preserved data. |
| **GFS 0.25° D−1 00 UTC weather**: u10, v10, u100, v100 and DSWRF, giving three derived columns | v3, v4, v5 | **2** | NCEP's "48hr PRODUCTS" completion for the 00 UTC run is 03:42–04:00 UTC on D−1 (dated 30-day averages, 2017–2026). Per run, the reconstruction uses the later of the two bracketing captures [DOSSIER-6]. | Strictly before, on every day, by 4.9975–6.2906 h | Operational forecasts as issued. Per-run evidence for CP-25's 329 runs is in [`gfs-targeted-checks.csv`](gfs-targeted-checks.csv) and summarised below. |

The price lags and price statistics row covers:
- B0's D−1 and D−7 prices;
- v1-R's 24, 48 and 168 h lags and its 168 and 720 h statistics;
- LEAR's D−1, D−2, D−3 and D−7 curves;
- DDNN-2's D−1 curve, with optional D−2, D−3 and D−7 curves and statistics;
- the 168 h normalisation;
- the H layer's released errors (complete days up to D−2);
- v1-R's CQR calibration window, D−61 to D−2.

The load forecast row covers:
- v1-R's `load_forecast_mw` and `load_forecast_day_mean_mw`;
- LEAR's and LightGBM's load for D, and LEAR's load lags for D−1 and D−7;
- DDNN-2's `load_d0`, with optional `load_d1` and `load_d7`.

**GFS per-run evidence (CP-25's 329 runs).** For each run, the latest AWS `LastModified` among
its 10 target objects and 10 indexes:
- **327 runs:** every object was written by 05:55:31 UTC on the run date, so they were on AWS
  before the issue time (margin 3.07–6.31 h, median 5.21 h).
- **Run 2022-11-30** (delivery 2022-12-01): 16 of its 20 AWS objects were last written between
  15:10 and 15:38 UTC, 5.6 h after the issue time. Four of its leads (f027, f033, f036, f045) also
  failed GRIB framing on AWS, and NCAR's archive copy supplied them.
- **Run 2023-01-20** (delivery 2023-01-21): two index files were rewritten at 10:20 and 11:40 UTC.
  The GRIB objects themselves were written earlier.

`LastModified` records the last write to the AWS mirror, not NCEP's first publication, so this
evidence cannot tell a late run from a re-upload. The features of these two delivery days are kept
as extracted. They are named for the Owner, who may direct §15.3's "documented lateness" for
them.

**Refused or unused.**
- The A69 day-ahead wind and solar forecasts stay refused under §2: the day-ahead value is fixed
  at 18:00 Brussels on D−1, after the gate [MOP-A69].
- The A75 generation actuals are not an input of B0, v1-R or v2–v5.

## 2. Deterministic calendar features (admissible)

Each feature below is computed from the IANA time-zone rules and the `holidays` package's German
national calendar (version pinned in `uv.lock`), and is known in advance.

| Feature | Members |
|---|---|
| `local_hour`, `day_of_week` | v1-R, LightGBM (B3/A2, L-N, L-R) |
| `month`, `is_federal_holiday`, `is_day_after_holiday`, `is_bridge_day`, `day_type`, `dst_transition_day` | v1-R, LightGBM, DDNN-2 (calendar group) |
| `summer_peak` (months 6–8) and `winter_peak` (months 12–2) | v1-R, LightGBM |
| `weekday_0..6` | LEAR (A1, B2, A1_w, B2_w), DDNN-2 |
| B0's weekday rule (Tuesday–Friday take D−1; Monday, Saturday and Sunday take D−7) | B0 |
| DDNN-2's recency weights (half-life by day difference) | DDNN-2 |

## 3. Hindsight labels (inadmissible)

| Label | Where | Status |
|---|---|---|
| `crisis_period` (2021-09-01 to 2022-12-31) | `src/delu_forecast/features.py:156` | Inadmissible. Used by the released v1 artifact only; v1-R removes it (§24.5, §24.7). |
| `post_crisis` (from 2023-01-01) | `src/delu_forecast/features.py:159` | Inadmissible, as above. |

No other date-based regime feature exists in the landed member code. Its other date literals are the 2019 input floor and CP-24's weather-coverage wrapper scope (`src/cp24/v4members.py:110`), not features.

## 4. Missing-input rules, cited in the landed code

Each citation's line is tested against its text by `tests/cp25/test_outputs.py`.

| Input | Members | Rule | Consequence | Landed code |
|---|---|---|---|---|
| Prices: lags, rolling statistics, normalisation | v1-R; the base features of every v2–v5 member | A lag whose source hour is unavailable or ambiguous is null. A 168 h or 720 h window with any missing hour is NaN. A row with any null base feature gets no forecast and is not eligible. | **Failure.** A day without a feature-valid row falls back (§24.7). | `src/delu_forecast/features.py:60`, `:82`; `src/delu_forecast/model.py:159`; `src/delu_forecast/experiment.py:70`; `src/cp15/data.py:104`, `:126` |
| Prices: D−1 and D−7 at the same local hour | B0 | An unavailable or ambiguous source hour is null. | **Failure** for that hour | `src/delu_forecast/baselines.py:42`; `features.py:60` |
| Price curves D−1, D−2, D−3 and D−7 in the LEAR design | A1, B2, A1_w, B2_w | Training-partition median, plus a missing indicator | Imputed; the row still needs every base feature | `src/cp15/models.py:17`, `:19`; `src/cp15/data.py:104` |
| Prices: origin statistics | DDNN-2 | A forecast day without finite statistics raises; training days without them leave the window. | **Failure** | `src/cp24/member.py:78`; `src/cp24/design.py:309` |
| Prices: released errors for the H layer | v2–v5 interval layer | Issuance needs 28 complete released days. | **Failure** (issuance) | `src/cp16/residuals.py:141` |
| **Load forecast of D** | v1-R and every v2–v5 member | Any missing or null hour makes the day mean NaN. Every row of D then lacks a base feature, so none is feature-valid and none is forecast. | **Failure of the whole delivery day**: an eligibility exclusion here, and a fallback in CP-26 | `src/delu_forecast/features.py:143`; `model.py:159`; `src/cp15/data.py:104`; `src/cp15/models.py:47`; `src/cp21/lgbm.py:178`; `src/cp24/v4members.py:52`; `src/cp24/execution.py:75` |
| Load D−1 and D−7 lags, and D inside the LEAR and DDNN-2 designs | LEAR, DDNN-2 | Median imputation with indicators (LEAR); winsorise, then median (DDNN-2) | Imputed | `src/cp15/models.py:17`; `src/cp24/design.py:265` |
| GFS weather | v3, v4, v5 | §15.3: a confirmed missing, late or invalid vector sets all three columns missing, sets their indicators, and imputes training-only medians. A row with **no frozen weather record** is refused. | Imputed, never a failure, now that every development day has a weather record | `src/cp20/weather.py:133`, `:219`; `src/cp20/components.py:98`; `src/cp21/lgbm.py:97`, `:185`; `src/cp24/design.py:265`; `src/cp24/execution.py:151` |
| Calendar features | all | Deterministic; never missing | none | — |

## 5. The margin table (§24.5)

For each group and each shift, the table counts the delivery days on which the shifted
availability is no longer strictly before the issue time. Those are the days where the margin is
≤ the shift.
- **none:** no day is affected; the shift is recorded as passed, with no run.
- **structural:** every day is affected; the input's registered missing-input rule applies.
- **partial:** a non-empty proper subset of days is affected; CP-26 makes a delay run.

The full per-day list is [`margin-days.csv`](margin-days.csv).

| Group (tier) | Subgroup | +1 h | +6 h | +24 h | Margin range |
|---|---|---|---|---|---|
| Prices (2) | D−1 prices: lags, statistics, normalisation, the D−1 training target | none | none | **structural** (2,806 of 2,806) | 21–22 h |
| Prices (2) | D−2 and older: released errors, older lags, CQR calibration | none | none | none | 45–47 h |
| GFS (2) | D−1 00 UTC run, f021–f048 | none | **partial** (1,783 of 2,805) | **structural** (2,805 of 2,805) | 4.9975–6.2906 h |
| Load forecast (3) | Load forecast of D | **structural** | **structural** | **structural** | exactly 1 h |
| Load forecast (3) | Load forecast of D−1 (lag) | none | none | partial (8 DST-transition days) | 24–26 h |

What each class means:
- **Prices, +24 h, structural.** D−1's auction would be published after the issue time on every
  day. The landed rule is a failure, so every day falls back to B0, and B0 itself needs D−1's or
  D−7's prices.
- **GFS, +6 h, partial.** Every CEST day is affected (1,652), because the shifted availability
  passes 09:00 UTC. So are 131 CET days, 2024-10-28 to 2025-03-07, whose bracketing capture is
  04:00:09, which shifts to 10:00:09. That makes it a delay-run candidate for CP-26.
- **GFS, +24 h, structural.** §15.3 applies: the weather columns go missing and are imputed.
- **Load forecast, +1 h, structural.** This is the example the anchor names: the forecast would
  arrive at exactly 11:00, which is not strictly before, on every day. If the Owner granted an
  exception, that margin is the disclosed operational risk.

## 6. Documents

| Key | Document | Read |
|---|---|---|
| REG543-6 | Commission Regulation (EU) No 543/2013, Art. 6 (1)(b) and (2)(b), as adopted: [legislation.gov.uk](https://www.legislation.gov.uk/eur/2013/543/article/6/adopted) | 2026-10-12 |
| REG543-12 | Regulation 543/2013, Art. 12 (1)(d) and (2)(d), as adopted: [legislation.gov.uk](https://www.legislation.gov.uk/eur/2013/543/article/12/adopted) | 2026-10-12 |
| CACM-39, -47, -48, -50 | Commission Regulation (EU) 2015/1222, Arts. 39, 47, 48 and 50, as adopted: [legislation.gov.uk](https://www.legislation.gov.uk/eur/2015/1222/article/47/adopted) (same path for each article) | 2026-10-12 |
| SMARD-B1.3, -D2.2.1, -D3.1 | SMARD.de Benutzerhandbuch, April 2026, pp. 7, 52 and 54 (PDF, SHA-256 `331df7cc…88bd`) | 2026-10-12 |
| DOSSIER-6 | `reports/weather-admission/dossier.md` §6 and `availability/gfs_ncep_production_status.csv` | repository |
| MOP-A69 | `reports/cp15/feasibility/structural_inputs.md` (ENTSO-E MoP Ref2 pp. 69–70) | repository |
| RECON | `data/reconciliation_summary.json` | repository |

The EUR-Lex copy of Regulation 543/2013 answered with an empty HTTP 202 and was not pursued. The
UK National Archives' copy of the text as adopted was read instead. None of these documents
carries market data after 2026-09-06.
