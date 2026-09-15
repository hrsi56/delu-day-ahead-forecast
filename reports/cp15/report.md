# CP-15 — adaptive forecasting comparison, v21-r1

**Engineering status: pending fresh exact-candidate Integration.** The binding review is committed after this report under `docs/track-b/evidence/cp-15/integration.md`; the terminal packet reports its result. The preserved attempt-1 FAIL binds only its original candidate.

**product_feasibility: NOT_DEMONSTRATED. Best observed candidate: A1. Qualified policy: none.** These are development screening results after selection; they do not authorize promotion.

Data: ENTSO-E Transparency Platform; Bundesnetzagentur | SMARD.de — CC BY 4.0.

## Scope and original evaluation hours

The nine-policy comparison uses the original target hours and the fixed 2019 boundary. Long histories expand from 2019-01-01 until 728 preceding calendar days are available, then roll; A4 always uses 84 days. Every training row uses its own causal 168-hour level/scale. The protocol was committed at `bb5e67882fcfdf65b963d25ce785a3999816dfc2` before comparison. No outer score chose a parameter, window, feature or solver tolerance.

| fold | window_start | window_end | n_hours | n_days |
| --- | --- | --- | --- | --- |
| fold_1 | 2020-07-01 | 2020-09-28 | 2160 | 90 |
| fold_2 | 2021-04-01 | 2021-06-29 | 2159 | 90 |
| fold_3 | 2022-07-01 | 2022-09-28 | 2112 | 88 |
| fold_4 | 2025-05-01 | 2025-07-29 | 2160 | 90 |
| fold_5 | 2026-01-08 | 2026-04-07 | 2156 | 90 |

Each of the nine arms has 10,747 original eligible targets (96,723 predictions altogether). The 17-day peak is 2022-08-15 through 2022-08-31, 408 hours; full fold 3 is 2,112 hours on 88 represented days within its unchanged 90-calendar-day window. Ineligible original days/hours remain absent from scoring, and remain explicit empty days in the bootstrap calendar.

## Equal-fold comparison and secondary pooled scores

S_MAE and S_WIS are equal-weight averages of five ratios to B0. MAE and WIS below are secondary observation-weighted pooled values in EUR/MWh. Primary MAE uses the final emitted p50, after signed-error centering.

| policy | S_MAE | S_WIS | MAE | WIS |
| --- | --- | --- | --- | --- |
| B0 | 1.00000 | 1.00000 | 32.81010 | 20.02060 |
| B1 | 1.05185 | 0.98564 | 41.74348 | 25.24793 |
| B2 | 0.65781 | 0.63899 | 20.98425 | 12.66232 |
| B3 | 0.78414 | 0.73991 | 26.32393 | 15.16769 |
| A1 | 0.67229 | 0.64602 | 20.70749 | 12.44968 |
| A2 | 0.77371 | 0.73167 | 25.39572 | 14.77128 |
| A3 | 0.67251 | 0.64719 | 21.43859 | 12.76011 |
| A4 | 0.76466 | 0.73342 | 24.21680 | 14.40719 |
| A5 | 0.67378 | 0.64871 | 21.50099 | 12.80930 |

## Candidate ranking and qualification

| rank | policy | S_MAE | S_WIS | table_order | failed_criteria | qualified | product_feasibility |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | A1 | 0.67229 | 0.64602 | 0 | [1, 2, 5] | False | NOT_DEMONSTRATED |
| 2 | A3 | 0.67251 | 0.64719 | 2 | [1, 2, 5] | False | NOT_DEMONSTRATED |
| 3 | A5 | 0.67378 | 0.64871 | 4 | [1, 2, 5] | False | NOT_DEMONSTRATED |
| 4 | A4 | 0.76466 | 0.73342 | 3 | [1, 2, 5] | False | NOT_DEMONSTRATED |
| 5 | A2 | 0.77371 | 0.73167 | 1 | [1, 2, 4, 5] | False | NOT_DEMONSTRATED |

All six criteria were applied mechanically. `criteria.csv` includes every actual value and limit, including each fold separately. B2/B3 best-per-metric comparisons are diagnostic oracles, not deployable policies. A candidate must pass every criterion to qualify.

### Failed checks, with actual values

| policy | criterion | metric | scope | actual | lower_limit | upper_limit | passed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A1 | 1 | S_MAE | equal_fold | 0.67229 | nan | 0.59203 | False |
| A1 | 2 | S_WIS | equal_fold | 0.64602 | nan | 0.57509 | False |
| A1 | 5 | MAE | fold_1 | 6.81990 | nan | 6.53023 | False |
| A2 | 1 | S_MAE | equal_fold | 0.77371 | nan | 0.59203 | False |
| A2 | 2 | S_WIS | equal_fold | 0.73167 | nan | 0.57509 | False |
| A2 | 4 | MAE | peak | 61.40122 | nan | 57.61776 | False |
| A2 | 5 | MAE | fold_1 | 7.04264 | nan | 6.53023 | False |
| A2 | 5 | MAE | fold_2 | 10.30025 | nan | 10.16020 | False |
| A2 | 5 | MAE | fold_3 | 66.44564 | nan | 56.70822 | False |
| A2 | 5 | MAE | fold_4 | 19.22009 | nan | 17.36764 | False |
| A2 | 5 | MAE | fold_5 | 24.87423 | nan | 20.16263 | False |
| A2 | 5 | WIS | fold_1 | 4.18927 | nan | 4.14715 | False |
| A2 | 5 | WIS | fold_2 | 6.75680 | nan | 6.33989 | False |
| A2 | 5 | WIS | fold_3 | 37.89719 | nan | 33.94045 | False |
| A2 | 5 | WIS | fold_4 | 11.40796 | nan | 10.40072 | False |
| A2 | 5 | WIS | fold_5 | 14.11415 | nan | 12.10231 | False |
| A3 | 1 | S_MAE | equal_fold | 0.67251 | nan | 0.59203 | False |
| A3 | 2 | S_WIS | equal_fold | 0.64719 | nan | 0.57509 | False |
| A3 | 5 | MAE | fold_5 | 20.72185 | nan | 20.16263 | False |
| A3 | 5 | WIS | fold_5 | 12.18008 | nan | 12.10231 | False |
| A4 | 1 | S_MAE | equal_fold | 0.76466 | nan | 0.59203 | False |
| A4 | 2 | S_WIS | equal_fold | 0.73342 | nan | 0.57509 | False |
| A4 | 5 | MAE | fold_1 | 7.56131 | nan | 6.53023 | False |
| A4 | 5 | MAE | fold_2 | 11.23396 | nan | 10.16020 | False |
| A4 | 5 | MAE | fold_3 | 62.21004 | nan | 56.70822 | False |
| A4 | 5 | MAE | fold_4 | 18.27917 | nan | 17.36764 | False |
| A4 | 5 | MAE | fold_5 | 22.63487 | nan | 20.16263 | False |
| A4 | 5 | WIS | fold_1 | 4.61560 | nan | 4.14715 | False |
| A4 | 5 | WIS | fold_2 | 7.00397 | nan | 6.33989 | False |
| A4 | 5 | WIS | fold_3 | 36.38710 | nan | 33.94045 | False |
| A4 | 5 | WIS | fold_4 | 11.16950 | nan | 10.40072 | False |
| A4 | 5 | WIS | fold_5 | 13.34281 | nan | 12.10231 | False |
| A5 | 1 | S_MAE | equal_fold | 0.67378 | nan | 0.59203 | False |
| A5 | 2 | S_WIS | equal_fold | 0.64871 | nan | 0.57509 | False |
| A5 | 5 | MAE | fold_5 | 20.59063 | nan | 20.16263 | False |

## Every arm, every full fold

| policy | fold | n_hours | MAE | WIS | coverage95 | hit_count95 | raw_central_MAE | centering_effect | daily_mean_level_MAE | within_day_shape_MAE |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A1 | fold_1 | 2160 | 6.81990 | 4.10386 | 0.93565 | 2021 | 6.71144 | 0.10846 | 5.63408 | 4.83314 |
| A1 | fold_2 | 2159 | 9.95336 | 6.24655 | 0.93145 | 2011 | 9.91501 | 0.03834 | 7.40212 | 6.96495 |
| A1 | fold_3 | 2112 | 51.21276 | 30.45461 | 0.94223 | 1990 | 50.58633 | 0.62643 | 41.62120 | 35.48387 |
| A1 | fold_4 | 2160 | 16.74044 | 10.08696 | 0.94444 | 2040 | 16.71985 | 0.02059 | 9.25786 | 15.53149 |
| A1 | fold_5 | 2156 | 19.48164 | 11.75235 | 0.95640 | 2062 | 19.25121 | 0.23043 | 14.40437 | 14.93592 |
| A2 | fold_1 | 2160 | 7.04264 | 4.18927 | 0.94259 | 2036 | 6.99485 | 0.04779 | 6.09602 | 4.50300 |
| A2 | fold_2 | 2159 | 10.30025 | 6.75680 | 0.93654 | 2022 | 10.41723 | -0.11698 | 8.18812 | 6.77764 |
| A2 | fold_3 | 2112 | 66.44564 | 37.89719 | 0.92614 | 1956 | 64.19543 | 2.25021 | 58.11639 | 35.22305 |
| A2 | fold_4 | 2160 | 19.22009 | 11.40796 | 0.94028 | 2031 | 19.13164 | 0.08844 | 12.89243 | 15.69648 |
| A2 | fold_5 | 2156 | 24.87423 | 14.11415 | 0.93553 | 2017 | 23.85141 | 1.02282 | 20.91413 | 15.40679 |
| A3 | fold_1 | 2160 | 6.38293 | 3.89333 | 0.94028 | 2031 | 6.39935 | -0.01642 | 5.60266 | 4.37082 |
| A3 | fold_2 | 2159 | 9.48396 | 6.11750 | 0.93840 | 2026 | 9.51886 | -0.03489 | 7.40423 | 6.32259 |
| A3 | fold_3 | 2112 | 54.55453 | 31.90469 | 0.93182 | 1968 | 52.81186 | 1.74267 | 46.00855 | 32.93401 |
| A3 | fold_4 | 2160 | 16.77875 | 10.12622 | 0.94167 | 2034 | 16.70435 | 0.07440 | 10.24038 | 14.78787 |
| A3 | fold_5 | 2156 | 20.72185 | 12.18008 | 0.94991 | 2048 | 20.12608 | 0.59576 | 16.70729 | 14.33630 |
| A4 | fold_1 | 2160 | 7.56131 | 4.61560 | 0.92824 | 2005 | 7.41329 | 0.14802 | 5.88181 | 5.65157 |
| A4 | fold_2 | 2159 | 11.23396 | 7.00397 | 0.93793 | 2025 | 11.02525 | 0.20872 | 8.77655 | 7.82767 |
| A4 | fold_3 | 2112 | 62.21004 | 36.38710 | 0.92661 | 1957 | 60.17047 | 2.03956 | 51.96167 | 39.75674 |
| A4 | fold_4 | 2160 | 18.27917 | 11.16950 | 0.94907 | 2050 | 18.18581 | 0.09336 | 11.65882 | 16.88222 |
| A4 | fold_5 | 2156 | 22.63487 | 13.34281 | 0.94805 | 2044 | 22.26027 | 0.37460 | 16.87283 | 17.60070 |
| A5 | fold_1 | 2160 | 6.49136 | 3.96843 | 0.93519 | 2020 | 6.43608 | 0.05528 | 5.63440 | 4.50031 |
| A5 | fold_2 | 2159 | 9.53714 | 6.17244 | 0.93516 | 2019 | 9.57185 | -0.03471 | 7.48057 | 6.45019 |
| A5 | fold_3 | 2112 | 55.11483 | 32.32620 | 0.93419 | 1973 | 53.29271 | 1.82213 | 47.23644 | 33.31899 |
| A5 | fold_4 | 2160 | 16.51071 | 9.96130 | 0.94306 | 2037 | 16.43840 | 0.07231 | 10.12794 | 14.78699 |
| A5 | fold_5 | 2156 | 20.59063 | 12.04736 | 0.95130 | 2051 | 20.02570 | 0.56494 | 16.55211 | 14.29625 |
| B0 | fold_1 | 2160 | 8.63314 | 5.70904 | 0.91991 | 1987 | 8.59059 | 0.04255 | 7.38318 | 6.30310 |
| B0 | fold_2 | 2159 | 16.17163 | 10.88717 | 0.91478 | 1975 | 16.24214 | -0.07051 | 14.46247 | 9.25512 |
| B0 | fold_3 | 2112 | 86.94887 | 51.72696 | 0.87689 | 1852 | 85.65789 | 1.29098 | 76.61560 | 41.74389 |
| B0 | fold_4 | 2160 | 22.98456 | 14.56124 | 0.93981 | 2030 | 22.84527 | 0.13930 | 15.53024 | 20.24672 |
| B0 | fold_5 | 2156 | 30.50341 | 17.91507 | 0.88497 | 1908 | 30.09608 | 0.40733 | 25.71760 | 19.36003 |
| B1 | fold_1 | 2160 | 6.61289 | 4.00263 | 0.89444 | 1932 | 6.64454 | -0.03165 | 5.60753 | 4.44155 |
| B1 | fold_2 | 2159 | 20.03914 | 10.82493 | 0.88328 | 1907 | 20.03907 | 0.00008 | 17.74846 | 9.06583 |
| B1 | fold_3 | 2112 | 140.99285 | 87.93535 | 0.55540 | 1173 | 141.00796 | -0.01511 | 133.39897 | 47.92889 |
| B1 | fold_4 | 2160 | 20.06527 | 11.37095 | 0.96250 | 2079 | 20.10430 | -0.03903 | 13.88752 | 16.44203 |
| B1 | fold_5 | 2156 | 23.16835 | 13.47036 | 0.92393 | 1992 | 23.16431 | 0.00404 | 18.48832 | 15.60450 |
| B2 | fold_1 | 2160 | 6.21927 | 3.94966 | 0.91296 | 1972 | 6.20337 | 0.01590 | 5.31893 | 4.56192 |
| B2 | fold_2 | 2159 | 9.67638 | 6.03799 | 0.93932 | 2028 | 9.75691 | -0.08053 | 7.93171 | 6.60256 |
| B2 | fold_3 | 2112 | 54.00782 | 32.32424 | 0.92330 | 1950 | 54.25156 | -0.24374 | 43.37342 | 38.02323 |
| B2 | fold_4 | 2160 | 16.54061 | 9.90545 | 0.94861 | 2049 | 16.49711 | 0.04350 | 9.48378 | 15.23729 |
| B2 | fold_5 | 2156 | 19.20250 | 11.52601 | 0.92347 | 1991 | 19.00124 | 0.20126 | 14.27843 | 14.89074 |
| B3 | fold_1 | 2160 | 6.50763 | 4.01454 | 0.92546 | 1999 | 6.49496 | 0.01267 | 5.47733 | 4.48301 |
| B3 | fold_2 | 2159 | 11.66336 | 7.23132 | 0.93330 | 2015 | 12.08564 | -0.42228 | 9.84861 | 7.27919 |
| B3 | fold_3 | 2112 | 70.61552 | 39.58339 | 0.90246 | 1906 | 70.65063 | -0.03511 | 59.55232 | 39.04802 |
| B3 | fold_4 | 2160 | 18.39889 | 10.95822 | 0.94167 | 2034 | 18.24632 | 0.15257 | 13.02378 | 15.02396 |
| B3 | fold_5 | 2156 | 25.41005 | 14.58883 | 0.92579 | 1996 | 25.03292 | 0.37712 | 21.03324 | 16.16748 |

`per_fold.csv` also contains RMSE, 50/80/95% coverage, exact hits and lower/upper misses, mean/median/95th-percentile widths, signed bias, missing predictions and crossings. `hourly_losses.csv` retains individual losses; `daily.csv` retains daily level, shape, centering and coverage diagnostics.

## Peak stress, separate from the full crisis fold

| policy | n_hours | n_days | MAE | WIS | coverage95 | hit_count95 | lower_miss_count95 | upper_miss_count95 | mean_width95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A1 | 408 | 17 | 49.87670 | 29.40371 | 0.92647 | 378 | 13 | 17 | 275.86208 |
| A2 | 408 | 17 | 61.40122 | 33.41910 | 0.94853 | 387 | 10 | 11 | 301.73002 |
| A3 | 408 | 17 | 52.02244 | 29.53100 | 0.93382 | 381 | 11 | 16 | 285.36513 |
| A4 | 408 | 17 | 54.58456 | 31.63494 | 0.90686 | 370 | 11 | 27 | 283.46699 |
| A5 | 408 | 17 | 51.47202 | 29.29577 | 0.92892 | 379 | 11 | 18 | 279.69713 |
| B0 | 408 | 17 | 64.19130 | 34.05393 | 0.94118 | 384 | 2 | 22 | 315.01691 |
| B1 | 408 | 17 | 275.25954 | 190.23819 | 0.19363 | 79 | 1 | 328 | 418.23701 |
| B2 | 408 | 17 | 57.61776 | 33.72971 | 0.89216 | 364 | 13 | 31 | 246.48255 |
| B3 | 408 | 17 | 75.20073 | 41.67656 | 0.88971 | 363 | 17 | 28 | 283.66826 |

The peak has only 17 delivery days. Coverage is descriptive with exact counts, not an independent-hour significance claim. Aggregate metrics include all stress outcomes.

## Recovery and dependence-aware uncertainty

`recovery.csv` reports all nine arms on four consecutive seven-day windows from September 1 through 28, 2022; `daily.csv` also permits inspection without choosing a recovery threshold after outcomes. These diagnostics do not select the winner.

`bootstrap.csv` reports 95% percentile intervals for paired mean daily MAE/WIS differences for every A1–A5 versus B0–B3, by fold and equally across folds. Seed 15042; 2,000 replicates; noncircular blocks of seven consecutive calendar days within each full 90-day fold; all arms share each resample. Hourly observations stay together. Empty original days contribute no loss rather than zero loss. These daily-loss intervals are distinct from the hourly-weighted primary S scores. They are exploratory and subject to selection; no confirmatory p-value is claimed.

## Fit provenance and resources

| fold | policy | direct_logical_fit_calls | direct_fit_seconds | component_policies | component_fit_seconds | shared_fold_wall_seconds | shared_full_command_wall_seconds | shared_process_peak_rss_bytes | cache_hit_origins |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fold_1 | B0 | 0 | 0.00000 | none | 0.00000 | 2384.14480 | 2404.92000 | 653475840 | 1 |
| fold_1 | B1 | 0 | 0.00000 | none | 0.00000 | 2384.14480 | 2404.92000 | 653475840 | 1 |
| fold_1 | B2 | 14280 | 637.67119 | none | 0.00000 | 2384.14480 | 2404.92000 | 653475840 | 1 |
| fold_1 | B3 | 119 | 411.23876 | none | 0.00000 | 2384.14480 | 2404.92000 | 653475840 | 1 |
| fold_1 | A1 | 14280 | 759.29276 | none | 0.00000 | 2384.14480 | 2404.92000 | 653475840 | 1 |
| fold_1 | A2 | 119 | 403.00621 | none | 0.00000 | 2384.14480 | 2404.92000 | 653475840 | 1 |
| fold_1 | A3 | 0 | 0.00000 | A1+A2 | 1162.29897 | 2384.14480 | 2404.92000 | 653475840 | 1 |
| fold_1 | A4 | 14280 | 178.50000 | none | 0.00000 | 2384.14480 | 2404.92000 | 653475840 | 1 |
| fold_1 | A5 | 0 | 0.00000 | A1+A2+A4 | 1340.79897 | 2384.14480 | 2404.92000 | 653475840 | 1 |
| fold_2 | B0 | 0 | 0.00000 | none | 0.00000 | 2594.03892 | 2614.64000 | 645414912 | 0 |
| fold_2 | B1 | 0 | 0.00000 | none | 0.00000 | 2594.03892 | 2614.64000 | 645414912 | 0 |
| fold_2 | B2 | 14500 | 739.50952 | none | 0.00000 | 2594.03892 | 2614.64000 | 645414912 | 0 |
| fold_2 | B3 | 121 | 430.13623 | none | 0.00000 | 2594.03892 | 2614.64000 | 645414912 | 0 |
| fold_2 | A1 | 14500 | 828.61339 | none | 0.00000 | 2594.03892 | 2614.64000 | 645414912 | 0 |
| fold_2 | A2 | 121 | 422.80609 | none | 0.00000 | 2594.03892 | 2614.64000 | 645414912 | 0 |
| fold_2 | A3 | 0 | 0.00000 | A1+A2 | 1251.41948 | 2594.03892 | 2614.64000 | 645414912 | 0 |
| fold_2 | A4 | 14500 | 163.56676 | none | 0.00000 | 2594.03892 | 2614.64000 | 645414912 | 0 |
| fold_2 | A5 | 0 | 0.00000 | A1+A2+A4 | 1414.98623 | 2594.03892 | 2614.64000 | 645414912 | 0 |
| fold_3 | B0 | 0 | 0.00000 | none | 0.00000 | 2459.21267 | 2481.44000 | 598622208 | 0 |
| fold_3 | B1 | 0 | 0.00000 | none | 0.00000 | 2459.21267 | 2481.44000 | 598622208 | 0 |
| fold_3 | B2 | 14040 | 523.91356 | none | 0.00000 | 2459.21267 | 2481.44000 | 598622208 | 0 |
| fold_3 | B3 | 117 | 335.37525 | none | 0.00000 | 2459.21267 | 2481.44000 | 598622208 | 0 |
| fold_3 | A1 | 14040 | 1040.45655 | none | 0.00000 | 2459.21267 | 2481.44000 | 598622208 | 0 |
| fold_3 | A2 | 117 | 337.83990 | none | 0.00000 | 2459.21267 | 2481.44000 | 598622208 | 0 |
| fold_3 | A3 | 0 | 0.00000 | A1+A2 | 1378.29645 | 2459.21267 | 2481.44000 | 598622208 | 0 |
| fold_3 | A4 | 14040 | 212.74333 | none | 0.00000 | 2459.21267 | 2481.44000 | 598622208 | 0 |
| fold_3 | A5 | 0 | 0.00000 | A1+A2+A4 | 1591.03979 | 2459.21267 | 2481.44000 | 598622208 | 0 |
| fold_4 | B0 | 0 | 0.00000 | none | 0.00000 | 2664.45635 | 2685.56000 | 682229760 | 0 |
| fold_4 | B1 | 0 | 0.00000 | none | 0.00000 | 2664.45635 | 2685.56000 | 682229760 | 0 |
| fold_4 | B2 | 14620 | 890.01318 | none | 0.00000 | 2664.45635 | 2685.56000 | 682229760 | 0 |
| fold_4 | B3 | 122 | 346.75952 | none | 0.00000 | 2664.45635 | 2685.56000 | 682229760 | 0 |
| fold_4 | A1 | 14620 | 932.02035 | none | 0.00000 | 2664.45635 | 2685.56000 | 682229760 | 0 |
| fold_4 | A2 | 122 | 343.88978 | none | 0.00000 | 2664.45635 | 2685.56000 | 682229760 | 0 |
| fold_4 | A3 | 0 | 0.00000 | A1+A2 | 1275.91013 | 2664.45635 | 2685.56000 | 682229760 | 0 |
| fold_4 | A4 | 14620 | 142.66567 | none | 0.00000 | 2664.45635 | 2685.56000 | 682229760 | 0 |
| fold_4 | A5 | 0 | 0.00000 | A1+A2+A4 | 1418.57580 | 2664.45635 | 2685.56000 | 682229760 | 0 |
| fold_5 | B0 | 0 | 0.00000 | none | 0.00000 | 2550.43251 | 2571.71000 | 683016192 | 0 |
| fold_5 | B1 | 0 | 0.00000 | none | 0.00000 | 2550.43251 | 2571.71000 | 683016192 | 0 |
| fold_5 | B2 | 14260 | 925.79252 | none | 0.00000 | 2550.43251 | 2571.71000 | 683016192 | 0 |
| fold_5 | B3 | 119 | 260.09352 | none | 0.00000 | 2550.43251 | 2571.71000 | 683016192 | 0 |
| fold_5 | A1 | 14260 | 898.85283 | none | 0.00000 | 2550.43251 | 2571.71000 | 683016192 | 0 |
| fold_5 | A2 | 119 | 251.01152 | none | 0.00000 | 2550.43251 | 2571.71000 | 683016192 | 0 |
| fold_5 | A3 | 0 | 0.00000 | A1+A2 | 1149.86435 | 2550.43251 | 2571.71000 | 683016192 | 0 |
| fold_5 | A4 | 14260 | 207.12555 | none | 0.00000 | 2550.43251 | 2571.71000 | 683016192 | 0 |
| fold_5 | A5 | 0 | 0.00000 | A1+A2+A4 | 1356.98991 | 2550.43251 | 2571.71000 | 683016192 | 0 |

Direct model-fit counts include four chronological validation penalties and one final refit per hourly LEAR model; LGBM has one fit per day. A3/A5 reuse their fitted components; B0/B1 have no fit. Component costs are shown separately, so summing them again would double count. Process RSS and fold wall time are shared measurements repeated for each arm, not invented estimator-specific allocations. Initial input/feature preparation and warm-up boundary discovery are excluded from the fold-loop timer; the separate whole-command wall time includes them, plus process startup/teardown. Ensemble arithmetic and residual emission are included in fold-loop runtime but not separately timed. Cached central forecasts keep original fitting durations; cache counts distinguish execution reuse. Lasso continuation calls are separately recorded in each fit record and do not add statistical grid choices.

`lineage_summary.csv` separates genuine warm-up and evaluation fits. Each `folds/*-fits.parquet` records training/validation dates, row and normalization hashes, selected penalties, model fingerprints, convergence and timing. `*-issued.parquet` preserves the central forecasts and scales that generated errors; `*-feedback.parquet` records one-time D-2 releases; `*-origins.json` binds the latest 28 complete released days and residual hashes used at every evaluation origin. No in-sample fitted residual seeds the buffer.

## Feasibility deliverables

The pinned Chronos-2 probe completed two local CPU inference calls at one proper-training origin, with future load support and a positive control. An offline reproduction matched forecast bytes. It was unscored and does not enter these nine policies. See `feasibility/README.md` for exact revision, license verification, dependency freeze, inputs, process memory, runtime and reproduction. `feasibility/structural_inputs.md` covers fuel, EUA, load, renewables, capacity, outages, cross-border and weather sources with dated primary-source retrievals and explicit vintage, coverage and reuse gaps.

## Preserved history and limitations

The first attempt remains reachable at evidence tip `193d9cf48c586b9c4b1f43d7a5677b2d5f400832`. Its candidate `f8d0ed2a5f0737f0d088c3474b5a9fe77a406f37` retains its original FAIL. `attempt-1-preservation.json` maps byte-identical copies of its plan, protocol and reports, and `docs/track-b/evidence/cp-15/attempt-1-integration.md` preserves the old verdict. The revised history rule does not rescore or relabel that attempt.

Prior v1 development point-MAE evidence remains p=0.948, statistic +1.6228, median 28.58% worse. Original v1 peak coverage was 79/408; CP-10 peak coverage was 131/408, while its full-fold result was 1,515/2,112. Those records remain distinct and unchanged. Native v1 pinball remains in its historical reports; CP-15 WIS is not renamed as that metric.

The inherited A65 load-forecast availability assumption is preserved; the snapshot does not independently prove every historical issue vintage. Day-ahead D-1 prices are already published at the prior auction. D-2 error feedback is the prescribed conservative policy restriction, not a claim that D-1 prices were unavailable. Origin time is literal fixed CET noon (11:00 UTC), separate from Berlin delivery-day DST. No pre-2019 inputs, spent holdout, reserved-tail outcomes, A69 or target-day actual predictors entered fitting or selection. Residual intervals are empirical benchmarks without a finite-sample conformal guarantee. See `implementation-notes.md` for the recorded fixed-tolerance numerical repair and `reproduction.md` for commands.
