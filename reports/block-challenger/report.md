# CP-21 — three-block LightGBM on top of v3 (capstone v21-r6 §17)

**Evidence class: `development_post_selection`.** Every result is a development comparison on CP-20's 10,747 hours after earlier selection on the same five folds; nothing here is a test on new data. Nothing dated after 2026-04-07 was read, scored or used.

## Status at a glance

| Status | Value |
|---|---|
| Research verdict (rule `cp21-adoption`, §17.6, set 2026-09-29) | **v4** |
| Block-split finding (L-R − L-P, §17.5 reading) | **no demonstrated joint preference** |
| Engineering status | bound to the fresh Integration verdict at `docs/track-b/evidence/cp-21/integration.md` (not part of this candidate); an INCOMPLETE or BLOCKED return yields no adoption decision |
| Product status | unchanged: v1 remains the released product and demo; no promotion, freeze, Live, final-product designation or economic claim follows from this research result |
| Original §8 screen (diagnostic) | HG: met, HGL: met, L-N: met, L-P: not_met, L-R: not_met |

## The question and the ladder

HG (v3) blends two linear LEAR forecasts. CP-21 asks whether adding a three-block LightGBM member, built with exactly HG's information (CP-15's 23 LightGBM features plus the three frozen GFS columns and their missing indicators), improves on HG jointly in point and interval accuracy. HGL's central forecast is `A1_w/3 + B2_w/3 + L-N/6 + L-R/6` with HG's own components bit for bit; HG's hour-aware interval layer is re-estimated on HGL's own errors. The weights were fixed before any result and never tuned.

| Step | What it adds | Contrast | Reading |
|---|---|---|---|
| B3 → L-P | Weather — **bundled with training-only capacity selection and the §15.3 missing-input rule** (B3 is a saved CP-15 reference with fixed CP-2 hyperparameters), so not an isolated weather effect | L-P − B3 | observed joint improvement |
| L-P → L-R | The block split (controlled: same rows, target, features, grid, selection rule and H recipe) | L-R − L-P | no demonstrated joint preference |
| L-R → HGL | The blend into v3 | HGL − HG | observed joint improvement |

## Primary contrast and the adoption rule (HGL − HG)

| Score | Paired difference | 95% interval | Change as a share of HG | 95% interval of the share |
|---|---|---|---|---|
| ΔS_MAE | -0.0301 | [-0.0368, -0.0228] | -5.3% | [-6.4%, -4.0%] |
| ΔS_WIS | -0.0266 | [-0.0327, -0.0204] | -5.0% | [-6.0%, -3.8%] |

Bootstrap: seed 15042, 2,000 replicates of 7-calendar-day blocks within each fold, one shared index set (the same as CP-20's, SHA-256 `e1df9a68dc6715aa…`); share intervals are percentiles of `S_HGL,b / S_HG,b − 1` over the same stored replicates.

| # | Condition (verbatim rule text in protocol.json) | Result |
|---|---|---|
| 1 | Joint improvement over HG: on the paired HGL - HG differences, the upper 95% endpoint of dS_WIS is < 0 and the upper 95% endpoint of dS_MAE is <= 0. | **met** |
| 2 | No regression on the original screen: HGL meets all six original section-8 diagnostics with the saved B0-B3 comparators, as HG does. | **met** |
| 3 | A complete, valid evaluation: Engineering PASS with a fresh binding Integration verdict, and every one of the 10,747 keys issued with finite, ordered quantiles. | **met** — every key issued with finite, ordered quantiles; its Engineering-PASS half is the fresh Integration verdict on this exact candidate |
| 4 | No resolved per-fold degradation: in no fold may HGL - HG be decisively worse in MAE or in WIS, i.e. no fold whose paired daily-loss 95% interval has its lower endpoint > 0, for each of the five folds and both metrics. | **met** |

Per-fold paired daily-loss differences, HGL − HG (condition 4: a fold is decisively worse only if its lower endpoint is above zero):

| Fold | ΔMAE (EUR/MWh) | 95% interval | ΔWIS (EUR/MWh) | 95% interval |
|---|---|---|---|---|
| fold_1 | -0.323 | [-0.491, -0.179] | -0.190 | [-0.280, -0.100] |
| fold_2 | -0.668 | [-1.029, -0.360] | -0.348 | [-0.526, -0.194] |
| fold_3 (stress) | -1.008 | [-2.556, 0.586] | -0.781 | [-1.698, 0.088] |
| fold_4 | -0.864 | [-1.111, -0.629] | -0.471 | [-0.629, -0.322] |
| fold_5 | -0.688 | [-0.970, -0.220] | -0.365 | [-0.505, -0.137] |

## Secondary contrasts (descriptive)

| Contrast | Shows | ΔS_MAE [95%] | ΔS_WIS [95%] | Share of comparator (MAE / WIS) | Joint reading | Single-metric intervals |
|---|---|---|---|---|---|---|
| L-R − L-P | block split | 0.0050 [-0.0084, 0.0142] | 0.0063 [-0.0050, 0.0135] | +0.9% / +1.2% | no demonstrated joint preference | both span zero |
| L-P − B3 | weather, bundled with capacity selection | -0.2056 [-0.2377, -0.1766] | -0.1922 [-0.2278, -0.1659] | -26.2% / -26.0% | observed joint improvement | S_MAE interval below zero (better); S_WIS interval below zero (better) |
| L-N − L-R | target representation | -0.0066 [-0.0304, 0.0144] | -0.0138 [-0.0348, 0.0065] | -1.1% / -2.5% | no demonstrated joint preference | both span zero |
| L-P − HG | standalone vs v3 | 0.0127 [-0.0088, 0.0427] | 0.0155 [-0.0039, 0.0412] | +2.3% / +2.9% | no demonstrated joint preference | both span zero |
| L-R − HG | standalone vs v3 | 0.0177 [-0.0065, 0.0458] | 0.0218 [0.0004, 0.0450] | +3.1% / +4.1% | no demonstrated joint preference | S_WIS interval above zero (worse) |
| L-N − HG | standalone vs v3 | 0.0112 [-0.0080, 0.0324] | 0.0080 [-0.0086, 0.0270] | +2.0% / +1.5% | no demonstrated joint preference | both span zero |

A mixed result is reported as no demonstrated joint preference, never as equivalence; where one metric's interval excludes zero it is stated in the last column.


## Scores, all eleven policies

| Policy | S_MAE | S_WIS | Pooled MAE (EUR/MWh) | Pooled WIS (EUR/MWh) | Pooled 95% coverage |
|---|---|---|---|---|---|
| HGL: v3 + block LightGBM member (candidate) | 0.5357 | 0.5056 | 17.55 | 10.24 | 0.9392 |
| v3 (comparator) | 0.5658 | 0.5322 | 18.26 | 10.67 | 0.9377 |
| L-P: pooled LightGBM (study arm) | 0.5785 | 0.5477 | 19.52 | 11.30 | 0.9358 |
| L-R: three-block LightGBM (study arm) | 0.5835 | 0.5540 | 20.14 | 11.63 | 0.9353 |
| L-N: normalized three-block LightGBM (study arm) | 0.5769 | 0.5402 | 19.48 | 11.15 | 0.9350 |
| v2 | 0.6441 | 0.6160 | 20.23 | 12.05 | 0.9389 |
| normalized LEAR | 0.6723 | 0.6460 | 20.71 | 12.45 | 0.9420 |
| daily LightGBM | 0.7841 | 0.7399 | 26.32 | 15.17 | 0.9258 |
| daily LEAR | 0.6578 | 0.6390 | 20.98 | 12.66 | 0.9296 |
| v1 development replay | 1.0518 | 0.9856 | 41.74 | 25.25 | 0.8452 |
| similar-day naive (normalizer) | 1.0000 | 1.0000 | 32.81 | 20.02 | 0.9074 |

S scores are equal-fold ratios to B0 (lower is better); pooled scores are secondary descriptions.

### Per-fold MAE (EUR/MWh); fold 3 is the stress period (2022-07-01..09-28, 2,112 hours over 88 days)

| Policy | fold_1 | fold_2 | fold_3 (stress) | fold_4 | fold_5 |
|---|---|---|---|---|---|
| HGL | 4.93 | 7.71 | 47.03 | 13.77 | 14.95 |
| HG | 5.25 | 8.38 | 48.04 | 14.64 | 15.64 |
| L-P | 4.93 | 8.50 | 53.57 | 14.23 | 17.10 |
| L-R | 5.00 | 8.45 | 57.25 | 13.82 | 16.98 |
| L-N | 5.27 | 7.65 | 54.20 | 14.91 | 16.14 |
| H0 | 6.31 | 9.46 | 51.21 | 16.12 | 18.73 |
| A1 | 6.82 | 9.95 | 51.21 | 16.74 | 19.48 |
| B3 | 6.51 | 11.66 | 70.62 | 18.40 | 25.41 |
| B2 | 6.22 | 9.68 | 54.01 | 16.54 | 19.20 |
| B1 | 6.61 | 20.04 | 140.99 | 20.07 | 23.17 |
| B0 | 8.63 | 16.17 | 86.95 | 22.98 | 30.50 |

### The 17-day peak, 2022-08-15..31 (408 hours) — descriptive only, small effective sample

On the peak, HGL's MAE is 50.09 EUR/MWh against v3's 47.52 — higher; with 17 days no inference is drawn (the fold-3 paired interval, which contains the peak, is in the primary section).

| Policy | MAE | WIS | 95% coverage | Hits / hours |
|---|---|---|---|---|
| HGL | 50.09 | 28.02 | 0.9363 | 382 / 408 |
| HG | 47.52 | 27.31 | 0.9387 | 383 / 408 |
| L-P | 66.26 | 35.88 | 0.8995 | 367 / 408 |
| L-R | 70.07 | 38.50 | 0.8971 | 366 / 408 |
| L-N | 52.20 | 28.87 | 0.9510 | 388 / 408 |
| H0 | 52.51 | 30.10 | 0.9240 | 377 / 408 |
| A1 | 49.88 | 29.40 | 0.9265 | 378 / 408 |
| B3 | 75.20 | 41.68 | 0.8897 | 363 / 408 |
| B2 | 57.62 | 33.73 | 0.8922 | 364 / 408 |
| B1 | 275.26 | 190.24 | 0.1936 | 79 / 408 |
| B0 | 64.19 | 34.05 | 0.9412 | 384 / 408 |

## Coverage with width (per fold), central versus emitted MAE

| Policy | Fold | Cov 50 | Cov 80 | Cov 95 | 95% width mean / median / p95 | 95% misses low / high | Central MAE | Emitted MAE | Centering effect | Bias | Level MAE | Shape MAE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HGL | fold_1 | 0.483 | 0.785 | 0.938 | 27.8 / 23.8 / 56.3 | 59 / 76 | 4.83 | 4.93 | 0.098 | 0.40 | 4.05 | 3.59 |
| HGL | fold_2 | 0.531 | 0.805 | 0.940 | 54.0 / 48.7 / 94.8 | 65 / 64 | 7.84 | 7.71 | -0.132 | 1.28 | 6.03 | 5.46 |
| HGL | fold_3 | 0.480 | 0.775 | 0.933 | 261.7 / 246.2 / 406.0 | 73 / 68 | 45.86 | 47.03 | 1.169 | 6.62 | 39.80 | 28.93 |
| HGL | fold_4 | 0.483 | 0.783 | 0.934 | 73.3 / 71.7 / 109.7 | 68 / 75 | 13.61 | 13.77 | 0.162 | -0.23 | 8.18 | 12.06 |
| HGL | fold_5 | 0.503 | 0.803 | 0.951 | 96.3 / 96.9 / 160.1 | 47 / 58 | 14.70 | 14.95 | 0.248 | -1.00 | 11.14 | 11.19 |
| HG | fold_1 | 0.481 | 0.782 | 0.934 | 29.2 / 25.1 / 59.4 | 59 / 84 | 5.18 | 5.25 | 0.076 | 0.38 | 4.26 | 3.85 |
| HG | fold_2 | 0.526 | 0.800 | 0.935 | 56.0 / 50.8 / 97.0 | 68 / 72 | 8.47 | 8.38 | -0.089 | 1.08 | 6.54 | 5.90 |
| HG | fold_3 | 0.477 | 0.782 | 0.936 | 272.9 / 258.7 / 420.3 | 62 / 73 | 46.72 | 48.04 | 1.315 | 7.43 | 40.06 | 30.81 |
| HG | fold_4 | 0.478 | 0.781 | 0.932 | 76.3 / 74.9 / 113.4 | 70 / 76 | 14.62 | 14.64 | 0.016 | -0.18 | 8.52 | 13.01 |
| HG | fold_5 | 0.506 | 0.812 | 0.951 | 100.5 / 100.8 / 170.9 | 44 / 62 | 15.45 | 15.64 | 0.190 | -0.90 | 11.65 | 12.00 |
| L-P | fold_1 | 0.504 | 0.778 | 0.933 | 28.2 / 24.4 / 58.7 | 60 / 85 | 4.80 | 4.93 | 0.130 | 0.13 | 3.82 | 3.75 |
| L-P | fold_2 | 0.506 | 0.789 | 0.931 | 61.1 / 55.7 / 115.3 | 71 / 77 | 8.64 | 8.50 | -0.144 | 0.86 | 6.50 | 6.19 |
| L-P | fold_3 | 0.488 | 0.765 | 0.925 | 281.3 / 262.2 / 441.3 | 82 / 77 | 53.88 | 53.57 | -0.308 | 3.32 | 43.54 | 33.42 |
| L-P | fold_4 | 0.487 | 0.799 | 0.938 | 80.8 / 82.1 / 122.4 | 52 / 81 | 13.96 | 14.23 | 0.266 | -1.12 | 8.86 | 12.11 |
| L-P | fold_5 | 0.479 | 0.791 | 0.951 | 100.1 / 103.1 / 153.3 | 46 / 59 | 16.95 | 17.10 | 0.142 | 0.57 | 12.15 | 12.39 |
| L-R | fold_1 | 0.504 | 0.777 | 0.936 | 29.1 / 24.4 / 60.7 | 61 / 78 | 4.87 | 5.00 | 0.129 | 0.25 | 3.93 | 3.77 |
| L-R | fold_2 | 0.518 | 0.786 | 0.931 | 61.7 / 56.1 / 114.1 | 76 / 72 | 8.76 | 8.45 | -0.310 | 0.78 | 6.69 | 6.20 |
| L-R | fold_3 | 0.497 | 0.770 | 0.933 | 291.4 / 268.6 / 462.8 | 74 / 67 | 57.17 | 57.25 | 0.077 | 5.15 | 45.45 | 35.48 |
| L-R | fold_4 | 0.483 | 0.792 | 0.936 | 79.4 / 78.8 / 119.6 | 53 / 85 | 13.70 | 13.82 | 0.122 | -0.73 | 8.43 | 12.05 |
| L-R | fold_5 | 0.475 | 0.794 | 0.940 | 97.3 / 99.8 / 149.6 | 64 / 65 | 16.72 | 16.98 | 0.264 | 0.24 | 12.37 | 12.13 |
| L-N | fold_1 | 0.475 | 0.789 | 0.937 | 29.5 / 25.4 / 60.0 | 63 / 74 | 5.16 | 5.27 | 0.114 | 0.50 | 4.18 | 3.87 |
| L-N | fold_2 | 0.529 | 0.807 | 0.936 | 52.9 / 47.5 / 91.2 | 74 / 65 | 7.64 | 7.65 | 0.002 | 1.10 | 5.61 | 5.70 |
| L-N | fold_3 | 0.466 | 0.748 | 0.934 | 259.4 / 239.7 / 407.0 | 86 / 53 | 53.74 | 54.20 | 0.453 | 11.58 | 44.92 | 30.90 |
| L-N | fold_4 | 0.477 | 0.781 | 0.927 | 81.9 / 81.5 / 119.3 | 67 / 91 | 14.65 | 14.91 | 0.259 | -1.19 | 9.40 | 12.67 |
| L-N | fold_5 | 0.474 | 0.782 | 0.942 | 111.3 / 114.0 / 185.5 | 70 / 56 | 15.77 | 16.14 | 0.366 | -2.04 | 11.80 | 11.88 |

## Blocks (per fold; §14.3 support rule: at least 56 represented dates)

| Policy | Fold | Block | Hours | Represented dates | Support | MAE | WIS | Cov 95 |
|---|---|---|---|---|---|---|---|---|
| HG | fold_1 | night | 720 | 90 | eligible | 3.13 | 1.94 | 0.968 |
| HGL | fold_1 | night | 720 | 90 | eligible | 2.92 | 1.82 | 0.974 |
| L-N | fold_1 | night | 720 | 90 | eligible | 3.37 | 2.02 | 0.982 |
| L-P | fold_1 | night | 720 | 90 | eligible | 3.36 | 2.00 | 0.974 |
| L-R | fold_1 | night | 720 | 90 | eligible | 3.41 | 2.05 | 0.972 |
| HG | fold_2 | night | 719 | 90 | eligible | 6.12 | 3.83 | 0.979 |
| HGL | fold_2 | night | 719 | 90 | eligible | 5.71 | 3.64 | 0.974 |
| L-N | fold_2 | night | 719 | 90 | eligible | 6.31 | 4.06 | 0.947 |
| L-P | fold_2 | night | 719 | 90 | eligible | 6.75 | 4.22 | 0.967 |
| L-R | fold_2 | night | 719 | 90 | eligible | 6.60 | 4.28 | 0.958 |
| HG | fold_3 | night | 704 | 88 | eligible | 35.87 | 21.13 | 0.972 |
| HGL | fold_3 | night | 704 | 88 | eligible | 36.38 | 20.93 | 0.972 |
| L-N | fold_3 | night | 704 | 88 | eligible | 46.09 | 24.99 | 0.960 |
| L-P | fold_3 | night | 704 | 88 | eligible | 45.15 | 25.15 | 0.966 |
| L-R | fold_3 | night | 704 | 88 | eligible | 49.29 | 27.73 | 0.956 |
| HG | fold_4 | night | 720 | 90 | eligible | 8.60 | 5.27 | 0.981 |
| HGL | fold_4 | night | 720 | 90 | eligible | 8.37 | 5.06 | 0.981 |
| L-N | fold_4 | night | 720 | 90 | eligible | 10.07 | 6.09 | 0.965 |
| L-P | fold_4 | night | 720 | 90 | eligible | 9.73 | 5.78 | 0.981 |
| L-R | fold_4 | night | 720 | 90 | eligible | 9.24 | 5.69 | 0.972 |
| HG | fold_5 | night | 716 | 90 | eligible | 9.37 | 5.88 | 0.986 |
| HGL | fold_5 | night | 716 | 90 | eligible | 9.42 | 5.74 | 0.986 |
| L-N | fold_5 | night | 716 | 90 | eligible | 11.91 | 7.03 | 0.975 |
| L-P | fold_5 | night | 716 | 90 | eligible | 12.30 | 7.10 | 0.983 |
| L-R | fold_5 | night | 716 | 90 | eligible | 12.00 | 6.86 | 0.980 |
| HG | fold_1 | shoulder | 810 | 90 | eligible | 5.91 | 3.59 | 0.926 |
| HGL | fold_1 | shoulder | 810 | 90 | eligible | 5.70 | 3.46 | 0.923 |
| L-N | fold_1 | shoulder | 810 | 90 | eligible | 6.04 | 3.59 | 0.917 |
| L-P | fold_1 | shoulder | 810 | 90 | eligible | 5.57 | 3.41 | 0.919 |
| L-R | fold_1 | shoulder | 810 | 90 | eligible | 5.72 | 3.50 | 0.926 |
| HG | fold_2 | shoulder | 810 | 90 | eligible | 8.09 | 4.93 | 0.936 |
| HGL | fold_2 | shoulder | 810 | 90 | eligible | 7.48 | 4.62 | 0.935 |
| L-N | fold_2 | shoulder | 810 | 90 | eligible | 7.45 | 4.51 | 0.941 |
| L-P | fold_2 | shoulder | 810 | 90 | eligible | 8.37 | 5.21 | 0.930 |
| L-R | fold_2 | shoulder | 810 | 90 | eligible | 8.03 | 5.11 | 0.933 |
| HG | fold_3 | shoulder | 792 | 88 | eligible | 49.08 | 28.27 | 0.929 |
| HGL | fold_3 | shoulder | 792 | 88 | eligible | 47.15 | 26.84 | 0.928 |
| L-N | fold_3 | shoulder | 792 | 88 | eligible | 52.52 | 28.77 | 0.939 |
| L-P | fold_3 | shoulder | 792 | 88 | eligible | 53.56 | 30.03 | 0.934 |
| L-R | fold_3 | shoulder | 792 | 88 | eligible | 54.46 | 30.19 | 0.953 |
| HG | fold_4 | shoulder | 810 | 90 | eligible | 16.65 | 9.58 | 0.930 |
| HGL | fold_4 | shoulder | 810 | 90 | eligible | 15.64 | 9.04 | 0.931 |
| L-N | fold_4 | shoulder | 810 | 90 | eligible | 16.04 | 9.56 | 0.923 |
| L-P | fold_4 | shoulder | 810 | 90 | eligible | 15.82 | 9.37 | 0.941 |
| L-R | fold_4 | shoulder | 810 | 90 | eligible | 15.64 | 9.25 | 0.931 |
| HG | fold_5 | shoulder | 810 | 90 | eligible | 18.40 | 10.48 | 0.936 |
| HGL | fold_5 | shoulder | 810 | 90 | eligible | 17.27 | 9.91 | 0.936 |
| L-N | fold_5 | shoulder | 810 | 90 | eligible | 17.58 | 10.33 | 0.930 |
| L-P | fold_5 | shoulder | 810 | 90 | eligible | 18.98 | 10.69 | 0.943 |
| L-R | fold_5 | shoulder | 810 | 90 | eligible | 18.43 | 10.38 | 0.935 |
| HG | fold_1 | solar | 630 | 90 | eligible | 6.85 | 4.17 | 0.905 |
| HGL | fold_1 | solar | 630 | 90 | eligible | 6.25 | 3.82 | 0.914 |
| L-N | fold_1 | solar | 630 | 90 | eligible | 6.46 | 3.85 | 0.910 |
| L-P | fold_1 | solar | 630 | 90 | eligible | 5.92 | 3.75 | 0.905 |
| L-R | fold_1 | solar | 630 | 90 | eligible | 5.88 | 3.76 | 0.906 |
| HG | fold_2 | solar | 630 | 90 | eligible | 11.33 | 6.88 | 0.884 |
| HGL | fold_2 | solar | 630 | 90 | eligible | 10.29 | 6.31 | 0.910 |
| L-N | fold_2 | solar | 630 | 90 | eligible | 9.42 | 5.70 | 0.916 |
| L-P | fold_2 | solar | 630 | 90 | eligible | 10.66 | 6.79 | 0.894 |
| L-R | fold_2 | solar | 630 | 90 | eligible | 11.09 | 6.94 | 0.898 |
| HG | fold_3 | solar | 616 | 88 | eligible | 60.60 | 34.79 | 0.904 |
| HGL | fold_3 | solar | 616 | 88 | eligible | 59.03 | 34.17 | 0.896 |
| L-N | fold_3 | solar | 616 | 88 | eligible | 65.61 | 37.15 | 0.898 |
| L-P | fold_3 | solar | 616 | 88 | eligible | 63.20 | 36.34 | 0.865 |
| L-R | fold_3 | solar | 616 | 88 | eligible | 69.93 | 39.48 | 0.881 |
| HG | fold_4 | solar | 630 | 90 | eligible | 18.95 | 10.86 | 0.881 |
| HGL | fold_4 | solar | 630 | 90 | eligible | 17.55 | 10.18 | 0.884 |
| L-N | fold_4 | solar | 630 | 90 | eligible | 19.00 | 11.12 | 0.887 |
| L-P | fold_4 | solar | 630 | 90 | eligible | 17.34 | 10.59 | 0.887 |
| L-R | fold_4 | solar | 630 | 90 | eligible | 16.73 | 10.20 | 0.902 |
| HG | fold_5 | solar | 630 | 90 | eligible | 19.22 | 10.82 | 0.930 |
| HGL | fold_5 | solar | 630 | 90 | eligible | 18.26 | 10.46 | 0.932 |
| L-N | fold_5 | solar | 630 | 90 | eligible | 19.09 | 11.25 | 0.919 |
| L-P | fold_5 | solar | 630 | 90 | eligible | 20.12 | 11.64 | 0.925 |
| L-R | fold_5 | solar | 630 | 90 | eligible | 20.78 | 12.11 | 0.902 |

Per-hour diagnostics for every policy and fold are in `diagnostics.csv` (scope `hour`).

## Original §8 diagnostics (all six, saved B0–B3 comparators; diagnostic only)

| Policy | Status | Criteria not met |
|---|---|---|
| HGL | met | none |
| HG | met | none |
| L-P | not_met | 4 |
| L-R | not_met | 4, 5 |
| L-N | met | none |

Every row with actual values and limits is in `criteria.csv`.

## Failures and interval-layer fallback

LightGBM fit failures: 0. Every one of the 10,747 keys was issued by every new arm with finite, ordered quantiles; the emitted p50 is kept separate from the central forecast.

| Arm | Hour cells issued | Pooled-fallback cells (w_h = 0) |
|---|---|---|
| HGL | 11592 | 0 |
| L-N | 11592 | 0 |
| L-P | 11592 | 0 |
| L-R | 11592 | 0 |

## Identity, parity and controls (§17.7)

| Check | Result |
|---|---|
| HG through CP-21's H-layer path vs accepted CP-20 vectors (10,747 keys) | bitwise equal: True, largest absolute difference 0.0 |
| HG component cache (638 entries) vs CP-20 fingerprints; evaluation centrals vs accepted HG | verified (preflight/input-verification.json) |
| Frozen weather regenerated from the 2,476 retained grids | bitwise equal (preflight/weather-regeneration.json) |
| HGL blend parity on every key (largest absolute value of c_HGL − ⅔·c_HG − ⅓·mean(L-N, L-R)) | 1.99e-13 EUR/MWh |
| Controls (delivery-day mask, non-uniform D−1 mutation, future/permuted/rearranged weather, training-only selection, pooled–block parity, DST blocks, state/cache refusals, boundary guard, thread count) | all passed: True (49 checks; controls.json) |
| Cold daily cycle refits (A1_w/B2_w vs CP-20; blocks and issued HGL vector vs main run) | all bitwise: True at 25 origins (daily-cycle.json) |

## Fit cost and daily retraining (diagnostic only, Owner decision D3)

Main-run LightGBM fits: 22,260 (17,808 inner, 4,452 final) over 636 origins. Single-thread fit wall time by arm (seconds): L-N 3,414, L-P 2,047, L-R 3,580. Block (L-R) versus pooled (L-P) wall time: 1.75×. Peak worker memory 0.77 GiB. Details: `fit-cost.csv`, `fit-cost-by-origin.csv`, `fits.parquet`, `fit-cost.json`.

HGL's complete daily cycle, measured cold on the M3 with 4 workers at 25 origins (five per fold): median 24.7 s, maximum 69.4 s — features, the A1_w/B2_w refits, the six block selections and fits, the H layer and issuance. v21-r5 §16 still requires any final-product candidate to retrain daily; this measurement is a diagnostic, not a selection criterion.

## Resources at this candidate (§17.8 caps; final totals including review are in the evidence directory)

| Counter | Used | Cap |
|---|---|---|
| active_seconds | 7,343 | 144,000 |
| additional_disk_bytes | 277,359,308 | 21,474,836,480 |
| analysis_passes | 1 | 3 |
| component_attempts | 62 | 1,600 |
| download_bytes | 0 | 0 |
| lgbm_fits | 23,792 | 35,000 |
| machine_seconds | 17,797 | 216,000 |
| main_lgbm_fits | 22,260 | 24,000 |
| policy_days | 3,299 | 10,500 |
| primitive_fits | 7,440 | 192,000 |
| reference_passes | 1 | 3 |
| remote_writes | 0 | 0 |
| rss_bytes | 3,952,017,408 | 10,737,418,240 |
| workers | 4 | 4 |

Machine-hours 4.94 of 60; active hours (upper bound) 2.0 of the 32-hour timebox; 0 bytes downloaded; 0 remote writes.

## What this result does not establish

- It is development evidence after selection on the same five folds; it is not a test on new data, and the fresh-data test 4.7T stays reserved.
- A mixed or non-significant result is not equivalence, absence of benefit or absence of harm.
- The B3 → L-P step bundles weather with capacity selection; no contrast isolates individual weather features.
- The block split is tested on the raw target only (no normalized pooled arm), with one seed.
- No economic, product, promotion or Live claim follows; v1 remains the released product.

## Defects and repairs

Every defect found during the checkpoint, its effect and its repair are in `defects-and-repairs.md`; no committed research output was invalidated and no frozen forecast-path file changed after the pre-run freeze.

## Files

`protocol.json` (frozen pre-run protocol) · `lineage.json` · `predictions.parquet` (four new arms) · `metrics.csv` · `diagnostics.csv` · `uncertainty.csv` · `replicates.parquet` · `replicate-scores.parquet` · `criteria.csv` · `adoption.json` · `fallback.csv` · `failures.csv` · `controls.json` · `hg-parity.json` · `daily-cycle.json` · `fit-cost.*` · `fits.parquet` · `resources.json` · `draft-registry.json` · `mlflow-export-draft/cp21.json` · `mlflow-local.json` · `artifact-manifest.json` · `defects-and-repairs.md` · `fit-cost.md` · `reproduce.md` · `preflight/`.
