# CP-28 r17 GFS note — descriptive, before the seven-arm experiment

**Identity:** `cp28-gfs-postresults-v21-r17`, under the supplement `docs/track-b/evidence/cp-26/cp28-gfs-postresults-addendum-v21-r17.md` (`39f322afa9717c5cfb0b626a1a8430fa9f5fcc0dfdd159123b9d4b48e7db03b4`) and the Owner's ruling `docs/track-b/cp-26-gfs-ruling-2026-10-19.md` (`3b97ff6abdf9a30ddd8c950cf3c459301d757aa1af08f6d8121bc73f92ba2373`).
**Evidence class:** `development_post_selection`; post-results exploration written after CP-26's outcomes were inspected. It is outside CP-28's seven-arm experiment, its multiplicity family and its selection. No fit, search, replay, H-buffer replay, recalibration, new bootstrap or test, download or dependency change was made. It adds no gate and changes no arm, input or control.

## Headline

- On all 2068 paired eligible dates, GFS+6 worsens nominal v5 MAE 18.46 → 21.04 (+2.58; +14.0% (95% +10.3% to +16.1%); n=2068) and WIS 10.87 → 12.55 (+1.68; +15.5% (95% +12.1% to +17.6%); n=2068) (EUR/MWh).
- v4, point only: MAE 18.58 → 21.57 (+2.99; +16.1%; n=2068); WIS 10.93 → 12.83 (+1.90; +17.4%; n=2068).
- v4 MAE on CP-25's GFS+6-affected dates: 18.07 → 22.40 (+4.32; +23.9%; n=1358); on unaffected dates: 19.56 → 20.00 (+0.44; +2.3%; n=710). Unaffected dates still move because the delayed route has its own training, search and residual history.
- v5 MAE on CP-25's GFS+6-affected dates: 17.75 → 21.92 (+4.17; +23.5%; n=1358); on unaffected dates: 19.82 → 19.37 (-0.46; -2.3%; n=710). Unaffected dates still move because the delayed route has its own training, search and residual history.
- Weather-independent v2 against v4, MAE: v2 22.58 vs nominal 18.58 (+21.5%) and GFS+6 21.57 (+4.7%); planning break-even no crossing in [0,1].
- Weather-independent v2 against v4, WIS: v2 13.43 vs nominal 10.93 (+22.9%) and GFS+6 12.83 (+4.7%); planning break-even no crossing in [0,1].
- Weather-independent v2 against v5, MAE: v2 22.58 vs nominal 18.46 (+22.3%) and GFS+6 21.04 (+7.3%); planning break-even no crossing in [0,1].
- Weather-independent v2 against v5, WIS: v2 13.43 vs nominal 10.87 (+23.5%) and GFS+6 12.55 (+7.0%); planning break-even no crossing in [0,1].

## Sources, bound by hash

- `reports/rebaseline/cold-rerun-2026-10-15/scores-manifest.json`: `b9f10917ab471177eda1b5f8ef735ddca5a651fa2e9bb47844497f3a6deaf84d`
- `reports/rebaseline/cold-rerun-2026-10-15/scores/daily.parquet`: `fcbcb24f59b4624d4b2c9f778b157078aad6f7cae553446c3c64df00c44c2a50`
- `reports/rebaseline/cold-rerun-2026-10-15/scores/known_price_states.parquet`: `ab041f73405e1870d6940e01745121127bc48cdabd342d26985476d18fb4eb79`
- `reports/rebaseline/cold-rerun-2026-10-15/scores/hourly.parquet (local only, `.local/artifacts/cp-26/cold-rerun-2026-10-15/r16/final-analysis-inputs/…`)`: `f465d5e780bddaa799bef754ae86ebc3d0928cf3397c354aa23a656fd48be709`
- `reports/rebaseline/cold-rerun-2026-10-15/report.json (local only; inference_endpoints, gfs6)`: `1b1aa805a066cda2da142cb9039fe63dd7a02c9b859f8129bd29b943ec1756d8`
- `reports/development-inputs/margin-days.csv (bound by CP-25 manifest f3e8ca15e446…)`: `4c7d4c8038643c1d012bd4116ab14b085298d68bf2f95d5711ab5f14a34d13e3`
- `docs/track-b/evidence/cp-26/cp28-gfs-postresults-addendum-v21-r17.md`: `39f322afa9717c5cfb0b626a1a8430fa9f5fcc0dfdd159123b9d4b48e7db03b4`
- `docs/track-b/cp-26-gfs-ruling-2026-10-19.md`: `3b97ff6abdf9a30ddd8c950cf3c459301d757aa1af08f6d8121bc73f92ba2373`

## Populations, definitions and calculations

- **Population.** CP-26's frozen scored calendar, 2020-12-29..2026-09-06 (2,078 dates), on CP-25's frozen eligible keys; a date enters a comparison only where both streams have a scored loss. No date is removed for its loss. Fallback losses stay in as scored (see the fallback status below). Actual DST hours; equal date weights.
- **Daily differential.** Per date, `loss(GFS+6) − loss(nominal)` for MAE and WIS separately, in EUR/MWh; reported as the mean difference and the ratio of paired mean daily losses. No daily percentage is averaged.
- **Breakdowns.** The four CP-26 masks; year (2020 and 2026 partial); pooled season; the three CP-21 hour blocks (night 22–05, solar 10–16, shoulder/peak 06–09 and 17–21, from the stored hourly losses: block mean within date, then dates equally); the two issue-time-known states (negative-price risk; high volatility, with its unknown startup state); and CP-25's frozen GFS+6 affected/unaffected classification joined by delivery date (`reports/development-inputs/margin-days.csv`). That classification is the documented-schedule stress test, not measured live failures.
- **Uncertainty.** Only CP-26's registered primary-14 bootstrap-t intervals for GFS+6 v5 against nominal v5 are reused, and only where their mask/year/season population is the same set of paired dates (checked: equal paired count and difference within 1e-9). Every other figure is a point summary.
- **Planning mixture.** For each compatible population and metric, with N the nominal mean, S the GFS+6 mean and B v2's mean on the same dates: `L(p) = (1−p)·N + p·S` at p = 0, .01, .05, .10, .20, .50, 1, B beside it. **p is a scenario weight, not a measured late-day frequency,** and this is not a chronological replay. Where S > N, `p* = (B−N)/(S−N)` is shown only if it lies in [0, 1].

## Checks against the small source tables

- Hourly-to-daily aggregation: 10340 stream-dates; the stored daily MAE/WIS equal the equal-hour means of the stored hourly losses (max relative difference {'MAE': 4.316192114720736e-16, 'WIS': 4.2054966492059303e-16}), hour counts equal the scoring hours.
- Every reused interval matched its paired count and point difference. The mixture reproduces N at p=0 and S at p=1, and each shown p* reproduces B.

## Fallback status on all eligible dates

- `nominal/v2`: {'native': 2068}
- `nominal/v4`: {'native': 2068}
- `nominal/v5`: {'native': 2050, 'B0': 18}
- `gfs6/v4`: {'native': 2068}
- `gfs6/v5`: {'native': 2068}

## Daily differential, GFS+6 minus nominal

| model | metric | population | slice | value | n | nominal | GFS+6 | diff | change | registered 95% ratio CI |
|---|---|---|---|---|---|---|---|---|---|---|
| v4 | MAE | all_eligible | overall | overall | 2068 | 18.58 | 21.57 | +2.99 | +16.1% | point only |
| v4 | MAE | all_eligible | gfs6_affected | affected | 1358 | 18.07 | 22.40 | +4.32 | +23.9% | point only |
| v4 | MAE | all_eligible | gfs6_affected | unaffected | 710 | 19.56 | 20.00 | +0.44 | +2.3% | point only |
| v4 | MAE | never_scored | overall | overall | 755 | 16.79 | 18.72 | +1.94 | +11.5% | point only |
| v4 | MAE | never_scored | gfs6_affected | affected | 398 | 16.56 | 20.23 | +3.67 | +22.2% | point only |
| v4 | MAE | never_scored | gfs6_affected | unaffected | 357 | 17.05 | 17.05 | +0.00 | +0.0% | point only |
| v4 | MAE | old_fold_2_5 | overall | overall | 358 | 20.72 | 23.72 | +2.99 | +14.4% | point only |
| v4 | MAE | old_fold_2_5 | gfs6_affected | affected | 277 | 22.51 | 26.14 | +3.64 | +16.2% | point only |
| v4 | MAE | old_fold_2_5 | gfs6_affected | unaffected | 81 | 14.62 | 15.41 | +0.79 | +5.4% | point only |
| v4 | MAE | newly_opened | overall | overall | 152 | 16.61 | 21.59 | +4.98 | +30.0% | point only |
| v4 | MAE | newly_opened | gfs6_affected | affected | 152 | 16.61 | 21.59 | +4.98 | +30.0% | point only |
| v4 | MAE | newly_opened | gfs6_affected | unaffected | 0 | — | — | — | — | no paired dates |
| v4 | MAE | all_eligible | year | 2020 | 3 | 13.23 | 11.84 | -1.40 | -10.5% | point only |
| v4 | MAE | all_eligible | year | 2021 | 365 | 14.09 | 16.06 | +1.97 | +13.9% | point only |
| v4 | MAE | all_eligible | year | 2022 | 359 | 34.65 | 38.49 | +3.85 | +11.1% | point only |
| v4 | MAE | all_eligible | year | 2023 | 362 | 15.78 | 17.66 | +1.88 | +11.9% | point only |
| v4 | MAE | all_eligible | year | 2024 | 365 | 15.68 | 19.24 | +3.56 | +22.7% | point only |
| v4 | MAE | all_eligible | year | 2025 | 365 | 14.60 | 17.83 | +3.23 | +22.2% | point only |
| v4 | MAE | all_eligible | year | 2026 | 249 | 16.24 | 19.96 | +3.72 | +22.9% | point only |
| v4 | MAE | all_eligible | season | DJF | 510 | 19.67 | 21.19 | +1.52 | +7.7% | point only |
| v4 | MAE | all_eligible | season | MAM | 550 | 16.31 | 19.15 | +2.84 | +17.4% | point only |
| v4 | MAE | all_eligible | season | JJA | 549 | 16.65 | 20.15 | +3.50 | +21.0% | point only |
| v4 | MAE | all_eligible | season | SON | 459 | 22.41 | 26.60 | +4.19 | +18.7% | point only |
| v4 | MAE | all_eligible | negative_price_risk | 0 | 1044 | 21.70 | 24.25 | +2.55 | +11.7% | point only |
| v4 | MAE | all_eligible | negative_price_risk | 1 | 1024 | 15.40 | 18.84 | +3.44 | +22.3% | point only |
| v4 | MAE | all_eligible | volatility_state | high | 435 | 25.45 | 28.80 | +3.35 | +13.2% | point only |
| v4 | MAE | all_eligible | volatility_state | not_high | 1633 | 16.75 | 19.65 | +2.89 | +17.3% | point only |
| v4 | MAE | all_eligible | volatility_state | unknown | 0 | — | — | — | — | no paired dates |
| v4 | WIS | all_eligible | overall | overall | 2068 | 10.93 | 12.83 | +1.90 | +17.4% | point only |
| v4 | WIS | all_eligible | gfs6_affected | affected | 1358 | 10.77 | 13.49 | +2.72 | +25.2% | point only |
| v4 | WIS | all_eligible | gfs6_affected | unaffected | 710 | 11.23 | 11.57 | +0.34 | +3.1% | point only |
| v4 | WIS | never_scored | overall | overall | 755 | 9.72 | 11.03 | +1.31 | +13.5% | point only |
| v4 | WIS | never_scored | gfs6_affected | affected | 398 | 9.82 | 12.19 | +2.37 | +24.1% | point only |
| v4 | WIS | never_scored | gfs6_affected | unaffected | 357 | 9.61 | 9.74 | +0.13 | +1.3% | point only |
| v4 | WIS | old_fold_2_5 | overall | overall | 358 | 12.05 | 14.06 | +2.00 | +16.6% | point only |
| v4 | WIS | old_fold_2_5 | gfs6_affected | affected | 277 | 13.06 | 15.48 | +2.42 | +18.5% | point only |
| v4 | WIS | old_fold_2_5 | gfs6_affected | unaffected | 81 | 8.60 | 9.18 | +0.58 | +6.8% | point only |
| v4 | WIS | newly_opened | overall | overall | 152 | 10.28 | 13.33 | +3.04 | +29.6% | point only |
| v4 | WIS | newly_opened | gfs6_affected | affected | 152 | 10.28 | 13.33 | +3.04 | +29.6% | point only |
| v4 | WIS | newly_opened | gfs6_affected | unaffected | 0 | — | — | — | — | no paired dates |
| v4 | WIS | all_eligible | year | 2020 | 3 | 6.32 | 5.71 | -0.61 | -9.7% | point only |
| v4 | WIS | all_eligible | year | 2021 | 365 | 8.10 | 9.37 | +1.27 | +15.7% | point only |
| v4 | WIS | all_eligible | year | 2022 | 359 | 19.91 | 22.48 | +2.57 | +12.9% | point only |
| v4 | WIS | all_eligible | year | 2023 | 362 | 9.17 | 10.45 | +1.27 | +13.9% | point only |
| v4 | WIS | all_eligible | year | 2024 | 365 | 9.46 | 11.54 | +2.08 | +22.0% | point only |
| v4 | WIS | all_eligible | year | 2025 | 365 | 8.87 | 10.92 | +2.05 | +23.1% | point only |
| v4 | WIS | all_eligible | year | 2026 | 249 | 9.88 | 12.21 | +2.33 | +23.6% | point only |
| v4 | WIS | all_eligible | season | DJF | 510 | 11.47 | 12.40 | +0.93 | +8.1% | point only |
| v4 | WIS | all_eligible | season | MAM | 550 | 9.64 | 11.47 | +1.83 | +18.9% | point only |
| v4 | WIS | all_eligible | season | JJA | 549 | 9.86 | 12.08 | +2.22 | +22.5% | point only |
| v4 | WIS | all_eligible | season | SON | 459 | 13.13 | 15.82 | +2.69 | +20.5% | point only |
| v4 | WIS | all_eligible | negative_price_risk | 0 | 1044 | 12.68 | 14.37 | +1.69 | +13.3% | point only |
| v4 | WIS | all_eligible | negative_price_risk | 1 | 1024 | 9.14 | 11.25 | +2.12 | +23.2% | point only |
| v4 | WIS | all_eligible | volatility_state | high | 435 | 15.01 | 17.15 | +2.13 | +14.2% | point only |
| v4 | WIS | all_eligible | volatility_state | not_high | 1633 | 9.84 | 11.68 | +1.84 | +18.7% | point only |
| v4 | WIS | all_eligible | volatility_state | unknown | 0 | — | — | — | — | no paired dates |
| v4 | MAE | all_eligible | hour_block | night | 2068 | 12.81 | 14.52 | +1.71 | +13.3% | point only |
| v4 | MAE | all_eligible | hour_block | solar | 2068 | 22.30 | 26.40 | +4.11 | +18.4% | point only |
| v4 | MAE | all_eligible | hour_block | shoulder_peak | 2068 | 20.81 | 24.08 | +3.26 | +15.7% | point only |
| v4 | WIS | all_eligible | hour_block | night | 2068 | 7.67 | 8.88 | +1.21 | +15.7% | point only |
| v4 | WIS | all_eligible | hour_block | solar | 2068 | 12.94 | 15.38 | +2.44 | +18.9% | point only |
| v4 | WIS | all_eligible | hour_block | shoulder_peak | 2068 | 12.25 | 14.35 | +2.10 | +17.2% | point only |
| v5 | MAE | all_eligible | overall | overall | 2068 | 18.46 | 21.04 | +2.58 | +14.0% | +10.3% to +16.1% |
| v5 | MAE | all_eligible | gfs6_affected | affected | 1358 | 17.75 | 21.92 | +4.17 | +23.5% | point only |
| v5 | MAE | all_eligible | gfs6_affected | unaffected | 710 | 19.82 | 19.37 | -0.46 | -2.3% | point only |
| v5 | MAE | never_scored | overall | overall | 755 | 17.20 | 18.33 | +1.13 | +6.6% | -0.2% to +10.6% |
| v5 | MAE | never_scored | gfs6_affected | affected | 398 | 16.27 | 19.91 | +3.64 | +22.4% | point only |
| v5 | MAE | never_scored | gfs6_affected | unaffected | 357 | 18.24 | 16.58 | -1.66 | -9.1% | point only |
| v5 | MAE | old_fold_2_5 | overall | overall | 358 | 20.17 | 23.03 | +2.85 | +14.2% | +11.4% to +19.1% |
| v5 | MAE | old_fold_2_5 | gfs6_affected | affected | 277 | 21.92 | 25.42 | +3.50 | +16.0% | point only |
| v5 | MAE | old_fold_2_5 | gfs6_affected | unaffected | 81 | 14.18 | 14.83 | +0.65 | +4.6% | point only |
| v5 | MAE | newly_opened | overall | overall | 152 | 16.63 | 21.60 | +4.97 | +29.9% | +25.2% to +41.7% |
| v5 | MAE | newly_opened | gfs6_affected | affected | 152 | 16.63 | 21.60 | +4.97 | +29.9% | point only |
| v5 | MAE | newly_opened | gfs6_affected | unaffected | 0 | — | — | — | — | no paired dates |
| v5 | MAE | all_eligible | year | 2020 | 3 | 13.29 | 11.98 | -1.31 | -9.9% | -9.9% to -9.9% |
| v5 | MAE | all_eligible | year | 2021 | 365 | 13.70 | 15.52 | +1.82 | +13.3% | +1.7% to +21.0% |
| v5 | MAE | all_eligible | year | 2022 | 359 | 35.23 | 37.33 | +2.10 | +5.9% | -1.2% to +11.6% |
| v5 | MAE | all_eligible | year | 2023 | 362 | 15.59 | 17.30 | +1.72 | +11.0% | +4.6% to +14.1% |
| v5 | MAE | all_eligible | year | 2024 | 365 | 15.44 | 18.85 | +3.42 | +22.1% | +16.8% to +29.3% |
| v5 | MAE | all_eligible | year | 2025 | 365 | 14.27 | 17.44 | +3.17 | +22.2% | +17.0% to +30.3% |
| v5 | MAE | all_eligible | year | 2026 | 249 | 16.07 | 19.68 | +3.61 | +22.5% | +15.3% to +32.8% |
| v5 | MAE | all_eligible | season | DJF | 510 | 20.24 | 20.46 | +0.22 | +1.1% | -1.0% to +3.0% |
| v5 | MAE | all_eligible | season | MAM | 550 | 16.05 | 18.77 | +2.71 | +16.9% | +14.1% to +22.4% |
| v5 | MAE | all_eligible | season | JJA | 549 | 16.41 | 19.88 | +3.47 | +21.2% | +18.5% to +25.1% |
| v5 | MAE | all_eligible | season | SON | 459 | 21.82 | 25.80 | +3.98 | +18.2% | +13.0% to +21.4% |
| v5 | MAE | all_eligible | negative_price_risk | 0 | 1044 | 21.68 | 23.54 | +1.86 | +8.6% | point only |
| v5 | MAE | all_eligible | negative_price_risk | 1 | 1024 | 15.18 | 18.49 | +3.31 | +21.8% | point only |
| v5 | MAE | all_eligible | volatility_state | high | 435 | 24.80 | 27.83 | +3.03 | +12.2% | point only |
| v5 | MAE | all_eligible | volatility_state | not_high | 1633 | 16.77 | 19.23 | +2.46 | +14.7% | point only |
| v5 | MAE | all_eligible | volatility_state | unknown | 0 | — | — | — | — | no paired dates |
| v5 | WIS | all_eligible | overall | overall | 2068 | 10.87 | 12.55 | +1.68 | +15.5% | +12.1% to +17.6% |
| v5 | WIS | all_eligible | gfs6_affected | affected | 1358 | 10.60 | 13.22 | +2.62 | +24.8% | point only |
| v5 | WIS | all_eligible | gfs6_affected | unaffected | 710 | 11.40 | 11.27 | -0.12 | -1.1% | point only |
| v5 | WIS | never_scored | overall | overall | 755 | 9.96 | 10.81 | +0.85 | +8.5% | +1.8% to +12.4% |
| v5 | WIS | never_scored | gfs6_affected | affected | 398 | 9.68 | 11.97 | +2.29 | +23.6% | point only |
| v5 | WIS | never_scored | gfs6_affected | unaffected | 357 | 10.27 | 9.52 | -0.75 | -7.3% | point only |
| v5 | WIS | old_fold_2_5 | overall | overall | 358 | 11.77 | 13.68 | +1.91 | +16.2% | +12.7% to +21.4% |
| v5 | WIS | old_fold_2_5 | gfs6_affected | affected | 277 | 12.76 | 15.08 | +2.32 | +18.2% | point only |
| v5 | WIS | old_fold_2_5 | gfs6_affected | unaffected | 81 | 8.40 | 8.89 | +0.49 | +5.8% | point only |
| v5 | WIS | newly_opened | overall | overall | 152 | 10.29 | 13.33 | +3.04 | +29.5% | +25.0% to +47.1% |
| v5 | WIS | newly_opened | gfs6_affected | affected | 152 | 10.29 | 13.33 | +3.04 | +29.5% | point only |
| v5 | WIS | newly_opened | gfs6_affected | unaffected | 0 | — | — | — | — | no paired dates |
| v5 | WIS | all_eligible | year | 2020 | 3 | 6.23 | 5.64 | -0.59 | -9.4% | -9.4% to -9.4% |
| v5 | WIS | all_eligible | year | 2021 | 365 | 7.85 | 9.05 | +1.20 | +15.3% | +4.2% to +22.4% |
| v5 | WIS | all_eligible | year | 2022 | 359 | 20.29 | 21.91 | +1.62 | +8.0% | +1.2% to +14.0% |
| v5 | WIS | all_eligible | year | 2023 | 362 | 9.08 | 10.24 | +1.16 | +12.8% | +6.5% to +15.5% |
| v5 | WIS | all_eligible | year | 2024 | 365 | 9.35 | 11.36 | +2.01 | +21.5% | +16.2% to +28.3% |
| v5 | WIS | all_eligible | year | 2025 | 365 | 8.70 | 10.73 | +2.03 | +23.3% | +18.1% to +32.2% |
| v5 | WIS | all_eligible | year | 2026 | 249 | 9.80 | 12.06 | +2.26 | +23.1% | +16.2% to +35.5% |
| v5 | WIS | all_eligible | season | DJF | 510 | 11.78 | 12.09 | +0.31 | +2.6% | +0.3% to +4.4% |
| v5 | WIS | all_eligible | season | MAM | 550 | 9.55 | 11.27 | +1.72 | +18.1% | +15.3% to +24.2% |
| v5 | WIS | all_eligible | season | JJA | 549 | 9.74 | 11.90 | +2.17 | +22.2% | +19.8% to +26.1% |
| v5 | WIS | all_eligible | season | SON | 459 | 12.80 | 15.37 | +2.58 | +20.1% | +15.2% to +23.2% |
| v5 | WIS | all_eligible | negative_price_risk | 0 | 1044 | 12.67 | 14.01 | +1.34 | +10.6% | point only |
| v5 | WIS | all_eligible | negative_price_risk | 1 | 1024 | 9.03 | 11.06 | +2.03 | +22.4% | point only |
| v5 | WIS | all_eligible | volatility_state | high | 435 | 14.68 | 16.68 | +1.99 | +13.6% | point only |
| v5 | WIS | all_eligible | volatility_state | not_high | 1633 | 9.86 | 11.45 | +1.60 | +16.2% | point only |
| v5 | WIS | all_eligible | volatility_state | unknown | 0 | — | — | — | — | no paired dates |
| v5 | MAE | all_eligible | hour_block | night | 2068 | 12.68 | 13.80 | +1.12 | +8.9% | point only |
| v5 | MAE | all_eligible | hour_block | solar | 2068 | 22.26 | 25.96 | +3.70 | +16.6% | point only |
| v5 | MAE | all_eligible | hour_block | shoulder_peak | 2068 | 20.64 | 23.64 | +3.01 | +14.6% | point only |
| v5 | WIS | all_eligible | hour_block | night | 2068 | 7.62 | 8.52 | +0.90 | +11.7% | point only |
| v5 | WIS | all_eligible | hour_block | solar | 2068 | 12.93 | 15.14 | +2.22 | +17.1% | point only |
| v5 | WIS | all_eligible | hour_block | shoulder_peak | 2068 | 12.15 | 14.12 | +1.96 | +16.1% | point only |

## Weather-independent v2 on the same dates

| model | metric | population | slice | value | n | v2 | nominal | GFS+6 | v2 vs nominal | v2 vs GFS+6 |
|---|---|---|---|---|---|---|---|---|---|---|
| v4 | MAE | all_eligible | overall | overall | 2068 | 22.58 | 18.58 | 21.57 | +21.5% | +4.7% |
| v4 | MAE | never_scored | overall | overall | 755 | 20.11 | 16.79 | 18.72 | +19.8% | +7.4% |
| v4 | MAE | old_fold_2_5 | overall | overall | 358 | 23.73 | 20.72 | 23.72 | +14.5% | +0.1% |
| v4 | MAE | newly_opened | overall | overall | 152 | 22.17 | 16.61 | 21.59 | +33.5% | +2.7% |
| v4 | MAE | all_eligible | gfs6_affected | affected | 1358 | 22.17 | 18.07 | 22.40 | +22.7% | -1.0% |
| v4 | MAE | all_eligible | gfs6_affected | unaffected | 710 | 23.38 | 19.56 | 20.00 | +19.5% | +16.9% |
| v4 | WIS | all_eligible | overall | overall | 2068 | 13.43 | 10.93 | 12.83 | +22.9% | +4.7% |
| v4 | WIS | never_scored | overall | overall | 755 | 11.90 | 9.72 | 11.03 | +22.4% | +7.9% |
| v4 | WIS | old_fold_2_5 | overall | overall | 358 | 14.11 | 12.05 | 14.06 | +17.1% | +0.4% |
| v4 | WIS | newly_opened | overall | overall | 152 | 13.59 | 10.28 | 13.33 | +32.2% | +2.0% |
| v4 | WIS | all_eligible | gfs6_affected | affected | 1358 | 13.32 | 10.77 | 13.49 | +23.7% | -1.3% |
| v4 | WIS | all_eligible | gfs6_affected | unaffected | 710 | 13.64 | 11.23 | 11.57 | +21.5% | +17.9% |
| v5 | MAE | all_eligible | overall | overall | 2068 | 22.58 | 18.46 | 21.04 | +22.3% | +7.3% |
| v5 | MAE | never_scored | overall | overall | 755 | 20.11 | 17.20 | 18.33 | +16.9% | +9.7% |
| v5 | MAE | old_fold_2_5 | overall | overall | 358 | 23.73 | 20.17 | 23.03 | +17.7% | +3.1% |
| v5 | MAE | newly_opened | overall | overall | 152 | 22.17 | 16.63 | 21.60 | +33.3% | +2.7% |
| v5 | MAE | all_eligible | gfs6_affected | affected | 1358 | 22.17 | 17.75 | 21.92 | +24.9% | +1.1% |
| v5 | MAE | all_eligible | gfs6_affected | unaffected | 710 | 23.38 | 19.82 | 19.37 | +17.9% | +20.7% |
| v5 | WIS | all_eligible | overall | overall | 2068 | 13.43 | 10.87 | 12.55 | +23.5% | +7.0% |
| v5 | WIS | never_scored | overall | overall | 755 | 11.90 | 9.96 | 10.81 | +19.5% | +10.1% |
| v5 | WIS | old_fold_2_5 | overall | overall | 358 | 14.11 | 11.77 | 13.68 | +19.8% | +3.1% |
| v5 | WIS | newly_opened | overall | overall | 152 | 13.59 | 10.29 | 13.33 | +32.2% | +2.0% |
| v5 | WIS | all_eligible | gfs6_affected | affected | 1358 | 13.32 | 10.60 | 13.22 | +25.7% | +0.7% |
| v5 | WIS | all_eligible | gfs6_affected | unaffected | 710 | 13.64 | 11.40 | 11.27 | +19.7% | +21.0% |

## Planning scenarios: L(p) = (1−p)·N + p·S, with v2 (B) beside it

| model | metric | population | slice | value | p=0 | p=0.01 | p=0.05 | p=0.1 | p=0.2 | p=0.5 | p=1 | B (v2) | break-even |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v4 | MAE | all_eligible | overall | overall | 18.58 | 18.61 | 18.73 | 18.88 | 19.18 | 20.08 | 21.57 | 22.58 | no crossing in [0,1] |
| v4 | MAE | never_scored | overall | overall | 16.79 | 16.81 | 16.88 | 16.98 | 17.18 | 17.76 | 18.72 | 20.11 | no crossing in [0,1] |
| v4 | MAE | old_fold_2_5 | overall | overall | 20.72 | 20.75 | 20.87 | 21.02 | 21.32 | 22.22 | 23.72 | 23.73 | no crossing in [0,1] |
| v4 | MAE | newly_opened | overall | overall | 16.61 | 16.66 | 16.86 | 17.11 | 17.61 | 19.10 | 21.59 | 22.17 | no crossing in [0,1] |
| v4 | MAE | all_eligible | gfs6_affected | affected | 18.07 | 18.12 | 18.29 | 18.50 | 18.94 | 20.23 | 22.40 | 22.17 | 0.948 |
| v4 | MAE | all_eligible | gfs6_affected | unaffected | 19.56 | 19.56 | 19.58 | 19.60 | 19.65 | 19.78 | 20.00 | 23.38 | no crossing in [0,1] |
| v4 | WIS | all_eligible | overall | overall | 10.93 | 10.94 | 11.02 | 11.12 | 11.31 | 11.88 | 12.83 | 13.43 | no crossing in [0,1] |
| v4 | WIS | never_scored | overall | overall | 9.72 | 9.74 | 9.79 | 9.85 | 9.99 | 10.38 | 11.03 | 11.90 | no crossing in [0,1] |
| v4 | WIS | old_fold_2_5 | overall | overall | 12.05 | 12.07 | 12.15 | 12.25 | 12.45 | 13.05 | 14.06 | 14.11 | no crossing in [0,1] |
| v4 | WIS | newly_opened | overall | overall | 10.28 | 10.31 | 10.44 | 10.59 | 10.89 | 11.81 | 13.33 | 13.59 | no crossing in [0,1] |
| v4 | WIS | all_eligible | gfs6_affected | affected | 10.77 | 10.80 | 10.90 | 11.04 | 11.31 | 12.13 | 13.49 | 13.32 | 0.938 |
| v4 | WIS | all_eligible | gfs6_affected | unaffected | 11.23 | 11.23 | 11.24 | 11.26 | 11.30 | 11.40 | 11.57 | 13.64 | no crossing in [0,1] |
| v5 | MAE | all_eligible | overall | overall | 18.46 | 18.49 | 18.59 | 18.72 | 18.98 | 19.75 | 21.04 | 22.58 | no crossing in [0,1] |
| v5 | MAE | never_scored | overall | overall | 17.20 | 17.21 | 17.26 | 17.32 | 17.43 | 17.77 | 18.33 | 20.11 | no crossing in [0,1] |
| v5 | MAE | old_fold_2_5 | overall | overall | 20.17 | 20.20 | 20.31 | 20.46 | 20.74 | 21.60 | 23.03 | 23.73 | no crossing in [0,1] |
| v5 | MAE | newly_opened | overall | overall | 16.63 | 16.68 | 16.88 | 17.13 | 17.62 | 19.11 | 21.60 | 22.17 | no crossing in [0,1] |
| v5 | MAE | all_eligible | gfs6_affected | affected | 17.75 | 17.79 | 17.96 | 18.16 | 18.58 | 19.83 | 21.92 | 22.17 | no crossing in [0,1] |
| v5 | MAE | all_eligible | gfs6_affected | unaffected | 19.82 | 19.82 | 19.80 | 19.78 | 19.73 | 19.60 | 19.37 | 23.38 | S below N: the GFS+6 route is not worse; no break-even |
| v5 | WIS | all_eligible | overall | overall | 10.87 | 10.89 | 10.95 | 11.04 | 11.21 | 11.71 | 12.55 | 13.43 | no crossing in [0,1] |
| v5 | WIS | never_scored | overall | overall | 9.96 | 9.97 | 10.00 | 10.04 | 10.13 | 10.38 | 10.81 | 11.90 | no crossing in [0,1] |
| v5 | WIS | old_fold_2_5 | overall | overall | 11.77 | 11.79 | 11.87 | 11.96 | 12.15 | 12.73 | 13.68 | 14.11 | no crossing in [0,1] |
| v5 | WIS | newly_opened | overall | overall | 10.29 | 10.32 | 10.44 | 10.59 | 10.89 | 11.81 | 13.33 | 13.59 | no crossing in [0,1] |
| v5 | WIS | all_eligible | gfs6_affected | affected | 10.60 | 10.62 | 10.73 | 10.86 | 11.12 | 11.91 | 13.22 | 13.32 | no crossing in [0,1] |
| v5 | WIS | all_eligible | gfs6_affected | unaffected | 11.40 | 11.40 | 11.39 | 11.38 | 11.37 | 11.34 | 11.27 | 13.64 | S below N: the GFS+6 route is not worse; no break-even |

## What this cannot say

- **Mechanism.** The GFS+6 route differs on unaffected dates too: it has its own 14 searches, training history and residual buffer. These stored outputs cannot separate direct input unavailability from propagated history effects; that would need another experiment.
- **Arrival probabilities.** p is a planning weight. Real late-run frequencies are not estimated from CP-25's shifted schedule and await CP-18's planned live availability measurement. Lateness is unlikely to be random, so realized costs depend on which dates are hit; the affected-date rows are shown separately for that reason, and the all-calendar deterioration is not a per-late-day penalty.
- **Uncertainty beyond v5's registered cells.** v4, v2, hour-block, state, affected/unaffected and every mixture or p* figure are point summaries; no interval exists for them in CP-26's stored inference, and none was computed.
- **Components.** CP-26 stores no scored HG/L/D2 component losses for the GFS+6 route; no component quantile stream was manufactured from central values, and no component central MAE stands in for an emitted p50 MAE.
- **Oracle envelope.** Not shown: an ex-post best-model envelope is not implementable and adds nothing to the decision below.
- **Money.** These are accuracy costs, not trading profit or business value, and not proof that v2 is the best fallback.

## Decision-policy recommendation, without fitting one

On CP-25's 1,358 GFS+6-affected dates the weather-independent v2 sits close to the delayed-weather route and far behind the nominal route: v4 MAE: v2 22.17, GFS+6 22.40 (-1.0%), nominal 18.07 (+22.7%); v4 WIS: v2 13.32, GFS+6 13.49 (-1.3%), nominal 10.77 (+23.7%); v5 MAE: v2 22.17, GFS+6 21.92 (+1.1%), nominal 17.75 (+24.9%); v5 WIS: v2 13.32, GFS+6 13.22 (+0.7%), nominal 10.60 (+25.7%). On unaffected dates v2 costs +17.9% MAE against nominal v5. For the control (v5), switching to v2 when weather is late would not, descriptively, beat the registered delayed-weather handling on the stress dates on both metrics, and against v4 the gain is about one percent. **This note therefore does not recommend an availability-switching experiment on present evidence.** The material cost of late weather is the gap to the on-time nominal route, so the decision-relevant unknown is how often the D−1 00 UTC run actually arrives before the issue time: CP-18's planned live availability measurement. If a rule is studied later, it should use only what is observable at issuance (actual availability and age, released historical errors). The decision is the Owner's.

Any such rule changes its own error history and interval calibration, so it needs a separate prospective registration, causal evaluation and Owner authority. It is not an eighth CP-28 arm, it cannot replace nominal v5 through this note, and it does not authorize waiting past the issue time or a previous-run weather fallback.

## Boundary

CP-28's members, control (nominal v5, with its load forecast), seven arms, sixteen inputs, learning rules, H layers, one-look rule, twenty endpoints, four Holm families and selection are unchanged by this note. The GFS+6 status stays **fragile**, accepted by the Owner as a disclosed research-continuation risk; no robustness, publication or live claim follows.
