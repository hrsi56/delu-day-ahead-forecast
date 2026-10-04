# CP-22 — v4 revised: one pooled member and a dynamic interval layer

`capstone_v21.md` v21-r9 §20 · evidence class **development_post_selection** · population `common-10747h` (10,747 keys, five folds).

## Verdicts

| Status | Result |
|---|---|
| Engineering | Bound to the fresh Integration-Critic verdict on the final candidate (`docs/track-b/evidence/cp-22/integration.md`) |
| `cp22-replacement` | **no replacement: CP-22 stops at its return and the Owner decides; three-block v4 stays current** · first unmet condition: R → 4, M → 4 |
| `cp22-dynamic-layer` | **not applicable: no winner W** |
| `cp22-fast-component` | **not applicable: no winner W** |
| Research | Development finding under the three rules pre-registered on 2026-10-01; one more decision on the same five folds (4.7T carries the protection) |
| Product | v1 remains the released product and the demo; no designation, freeze or Live follows (§16) |

The rules were applied mechanically, in their fixed sequence, from the committed tables (`reports/v4-revision/decisions.json`). A mixed result is no demonstrated joint preference, never equivalence.

## Scores (equal-fold ratios to B0; lower is better)

| Policy | S_MAE | S_WIS | pooled MAE (EUR/MWh) | pooled WIS | pooled 95% coverage | mean 95% width | §8 |
|---|---|---|---|---|---|---|---|
| A-LN | 0.5362 | 0.5056 | 17.54 | 10.24 | 0.938 | 101.65 | met |
| A-LP | 0.5381 | 0.5084 | 17.59 | 10.28 | 0.939 | 102.54 | met |
| A-PN-sel | 0.5358 | 0.5053 | 17.48 | 10.23 | 0.939 | 101.59 | met |
| A1 normalized LEAR | 0.6723 | 0.6460 | 20.71 | 12.45 | 0.942 | 134.33 | reference |
| B0 naive | 1.0000 | 1.0000 | 32.81 | 20.02 | 0.907 | 166.60 | reference |
| B1 (v1) | 1.0518 | 0.9856 | 41.74 | 25.25 | 0.845 | 130.86 | reference |
| B2 daily LEAR | 0.6578 | 0.6390 | 20.98 | 12.66 | 0.930 | 118.86 | reference |
| B3 daily LightGBM | 0.7841 | 0.7399 | 26.32 | 15.17 | 0.926 | 130.98 | reference |
| H0 (v2) | 0.6441 | 0.6160 | 20.23 | 12.05 | 0.939 | 124.64 | reference |
| v3 | 0.5658 | 0.5322 | 18.26 | 10.67 | 0.938 | 106.24 | met |
| v4 (three-block) | 0.5357 | 0.5056 | 17.55 | 10.24 | 0.939 | 101.92 | met |
| M | 0.5343 | 0.5048 | 17.42 | 10.21 | 0.938 | 101.69 | met |
| R | 0.5368 | 0.5066 | 17.52 | 10.25 | 0.938 | 101.78 | met |
| v3+DL | 0.5676 | 0.5553 | 18.30 | 11.15 | 0.942 | 122.26 | met |
| v4+DL | 0.5379 | 0.5281 | 17.65 | 10.71 | 0.941 | 117.70 | met |

## `cp22-replacement` (§20.6), condition by condition

**R against v4** — not met; first unmet condition 4.

1. Non-inferiority: dS_MAE 0.0011 [-0.0031, 0.0054], dS_WIS 0.0010 [-0.0028, 0.0049] → met.
2. All six §8 diagnostics: met.
3. A complete, valid evaluation: all 10,747 keys issued; Engineering PASS is bound to the Integration verdict.
4. No resolved per-fold degradation: not met — fold_4 MAE 0.309 [0.148, 0.423]; fold_4 WIS 0.176 [0.097, 0.231].

**M against v4** — not met; first unmet condition 4.

1. Non-inferiority: dS_MAE -0.0013 [-0.0036, 0.0016], dS_WIS -0.0008 [-0.0030, 0.0022] → met.
2. All six §8 diagnostics: met.
3. A complete, valid evaluation: all 10,747 keys issued; Engineering PASS is bound to the Integration verdict.
4. No resolved per-fold degradation: not met — fold_4 MAE 0.198 [0.051, 0.326]; fold_4 WIS 0.112 [0.024, 0.198].

## `cp22-dynamic-layer`

not applicable: no winner W.

## `cp22-fast-component`

not applicable: no winner W.

## Every §20.5 contrast, with its reading

| Contrast | Role | dS_MAE [95%] | dS_WIS [95%] | ratio S_WIS [95%] | Reading |
|---|---|---|---|---|---|
| A-LN-HG | reference_vs_v3 | -0.0295 [-0.0365, -0.0227] | -0.0266 [-0.0328, -0.0205] | -4.99% [-5.93, -3.82]% | observed joint improvement |
| A-LN-HGL | descriptive_blocks_under_normalization | 0.0006 [-0.0035, 0.0043] | 0.0001 [-0.0035, 0.0038] | 0.01% [-0.68, 0.75]% | no demonstrated joint preference |
| A-LP-HG | reference_vs_v3 | -0.0277 [-0.0351, -0.0179] | -0.0238 [-0.0310, -0.0156] | -4.48% [-5.69, -2.92]% | observed joint improvement |
| A-PN-sel-A-LP | normalized_vs_raw_pooled | -0.0023 [-0.0102, 0.0041] | -0.0030 [-0.0099, 0.0035] | -0.60% [-1.91, 0.68]% | no demonstrated joint preference |
| A-PN-sel-HG | reference_vs_v3 | -0.0300 [-0.0376, -0.0219] | -0.0269 [-0.0336, -0.0192] | -5.05% [-6.12, -3.61]% | observed joint improvement |
| A-PN-sel-M | dropping_the_raw_half | 0.0015 [-0.0025, 0.0048] | 0.0005 [-0.0030, 0.0040] | 0.10% [-0.59, 0.77]% | no demonstrated joint preference |
| HGL-HG | reference_vs_v3 | -0.0301 [-0.0368, -0.0228] | -0.0266 [-0.0327, -0.0204] | -5.01% [-5.95, -3.80]% | observed joint improvement |
| M-HG | reference_vs_v3 | -0.0314 [-0.0382, -0.0229] | -0.0274 [-0.0334, -0.0200] | -5.15% [-6.12, -3.72]% | observed joint improvement |
| M-HGL | replacement | -0.0013 [-0.0036, 0.0016] | -0.0008 [-0.0030, 0.0022] | -0.15% [-0.59, 0.43]% | no demonstrated joint preference |
| R-A-PN-sel | averaging_vs_daily_selection | 0.0010 [-0.0009, 0.0025] | 0.0012 [-0.0006, 0.0026] | 0.25% [-0.12, 0.51]% | no demonstrated joint preference |
| R-HG | reference_vs_v3 | -0.0290 [-0.0366, -0.0210] | -0.0256 [-0.0322, -0.0185] | -4.82% [-5.88, -3.49]% | observed joint improvement |
| R-HGL | replacement | 0.0011 [-0.0031, 0.0054] | 0.0010 [-0.0028, 0.0049] | 0.20% [-0.55, 0.97]% | no demonstrated joint preference |
| R-M | full_vs_minimal_refinement | 0.0025 [-0.0016, 0.0058] | 0.0018 [-0.0018, 0.0049] | 0.35% [-0.34, 0.97]% | no demonstrated joint preference |
| v3+DL-HG | dl_on_v3_descriptive | 0.0018 [-0.0041, 0.0072] | 0.0231 [0.0165, 0.0316] | 4.34% [3.04, 5.88]% | no demonstrated joint preference |
| v4+DL-HG | reference_vs_v3 | -0.0279 [-0.0372, -0.0189] | -0.0041 [-0.0112, 0.0050] | -0.78% [-2.07, 0.91]% | no demonstrated joint preference |
| v4+DL-HGL | dl_on_v4_descriptive | 0.0022 [-0.0041, 0.0077] | 0.0225 [0.0161, 0.0308] | 4.45% [3.12, 6.07]% | no demonstrated joint preference |

Not applicable without a winner W (§20.6): (W+DL) − W, (W+ACI) − W, (W+DL) − (W+ACI) and (W+DLF) − (W+DL); the layer arms on W were not run. The dynamic layer is reported on v4 and v3, descriptively.

Bootstrap: seed 15042, 2,000 replicates of 7-calendar-day blocks within each fold, the shared CP-20 index set (SHA-256 `e1df9a68dc6715aa2ecd9705ef61f504a3fe109ed917d1151ccbc46ea9e0f99b`); every replicate is stored in `replicates.parquet`.

## Per-fold MAE and WIS (EUR/MWh)

| Policy | fold_1 MAE / WIS | fold_2 MAE / WIS | fold_3 MAE / WIS | fold_4 MAE / WIS | fold_5 MAE / WIS |
|---|---|---|---|---|---|
| A-LN | 5.00 / 3.03 | 7.60 / 4.70 | 46.98 / 27.02 | 13.93 / 8.13 | 14.81 / 8.68 |
| A-LP | 4.86 / 2.98 | 7.89 / 4.92 | 46.77 / 27.01 | 13.85 / 8.08 | 15.21 / 8.78 |
| A-PN-sel | 4.97 / 3.01 | 7.54 / 4.66 | 46.56 / 26.91 | 14.15 / 8.26 | 14.82 / 8.68 |
| A1 normalized LEAR | 6.82 / 4.10 | 9.95 / 6.25 | 51.21 / 30.45 | 16.74 / 10.09 | 19.48 / 11.75 |
| B0 naive | 8.63 / 5.71 | 16.17 / 10.89 | 86.95 / 51.73 | 22.98 / 14.56 | 30.50 / 17.92 |
| B1 (v1) | 6.61 / 4.00 | 20.04 / 10.82 | 140.99 / 87.94 | 20.07 / 11.37 | 23.17 / 13.47 |
| B2 daily LEAR | 6.22 / 3.95 | 9.68 / 6.04 | 54.01 / 32.32 | 16.54 / 9.91 | 19.20 / 11.53 |
| B3 daily LightGBM | 6.51 / 4.01 | 11.66 / 7.23 | 70.62 / 39.58 | 18.40 / 10.96 | 25.41 / 14.59 |
| H0 (v2) | 6.31 / 3.86 | 9.46 / 5.98 | 51.21 / 30.22 | 16.12 / 9.55 | 18.73 / 11.03 |
| v3 | 5.25 / 3.21 | 8.38 / 5.13 | 48.04 / 27.79 | 14.64 / 8.52 | 15.64 / 9.05 |
| v4 (three-block) | 4.93 / 3.02 | 7.71 / 4.79 | 47.03 / 27.01 | 13.77 / 8.05 | 14.95 / 8.69 |
| M | 4.89 / 2.99 | 7.68 / 4.76 | 46.25 / 26.79 | 13.97 / 8.16 | 14.96 / 8.69 |
| R | 4.99 / 3.02 | 7.58 / 4.69 | 46.72 / 26.96 | 14.08 / 8.22 | 14.87 / 8.71 |
| v3+DL | 5.31 / 3.35 | 8.49 / 5.56 | 48.29 / 29.30 | 14.51 / 8.67 | 15.57 / 9.24 |
| v4+DL | 4.97 / 3.16 | 7.88 / 5.22 | 47.55 / 28.53 | 13.64 / 8.19 | 14.85 / 8.86 |

Fold 3 (2022-07-01..09-28, 2,112 hours / 88 days) is the stress period. Per-fold paired daily-loss intervals for every contrast are in `uncertainty.csv` (scopes fold_1..fold_5).

## Coverage with width, stress period and peak

| Policy | cov50 | cov80 | cov95 | mean / median / p95 width95 | fold-3 MAE | peak MAE | peak cov95 |
|---|---|---|---|---|---|---|---|
| A-LN | 0.493 | 0.788 | 0.938 | 101.7 / 70.0 / 302.9 | 46.98 | 47.70 | 0.936 |
| A-LP | 0.495 | 0.789 | 0.939 | 102.5 / 70.9 / 308.3 | 46.77 | 50.92 | 0.931 |
| A-PN-sel | 0.490 | 0.790 | 0.939 | 101.6 / 70.2 / 303.7 | 46.56 | 47.67 | 0.939 |
| A1 normalized LEAR | 0.503 | 0.788 | 0.942 | 134.3 / 94.4 / 372.6 | 51.21 | 49.88 | 0.926 |
| B0 naive | 0.462 | 0.752 | 0.907 | 166.6 / 136.9 / 462.1 | 86.95 | 64.19 | 0.941 |
| B1 (v1) | 0.364 | 0.628 | 0.845 | 130.9 / 97.9 / 387.5 | 140.99 | 275.26 | 0.194 |
| B2 daily LEAR | 0.476 | 0.772 | 0.930 | 118.9 / 88.1 / 355.0 | 54.01 | 57.62 | 0.892 |
| B3 daily LightGBM | 0.466 | 0.767 | 0.926 | 131.0 / 94.9 / 390.6 | 70.62 | 75.20 | 0.890 |
| H0 (v2) | 0.499 | 0.791 | 0.939 | 124.6 / 86.3 / 361.7 | 51.21 | 52.51 | 0.924 |
| v3 | 0.494 | 0.791 | 0.938 | 106.2 / 73.0 / 322.8 | 48.04 | 47.52 | 0.939 |
| v4 (three-block) | 0.496 | 0.790 | 0.939 | 101.9 / 70.1 / 307.6 | 47.03 | 50.09 | 0.936 |
| M | 0.495 | 0.790 | 0.938 | 101.7 / 70.2 / 304.8 | 46.25 | 48.98 | 0.941 |
| R | 0.489 | 0.790 | 0.938 | 101.8 / 70.2 / 303.5 | 46.72 | 47.57 | 0.939 |
| v3+DL | 0.505 | 0.803 | 0.942 | 122.3 / 86.1 / 371.1 | 48.29 | 47.23 | 0.953 |
| v4+DL | 0.503 | 0.803 | 0.941 | 117.7 / 81.3 / 362.2 | 47.55 | 49.76 | 0.953 |

The 17-day peak (2022-08-15..31, 408 hours) is descriptive only: a small effective sample.

## All six original §8 diagnostics, every new policy

| Policy | Criteria not met (criterion: scope) |
|---|---|
| A-LN | none — all met |
| A-LP | none — all met |
| A-PN-sel | none — all met |
| M | none — all met |
| R | none — all met |
| v3+DL | none — all met |
| v4+DL | none — all met |
| v3 | none — all met |
| v4 (three-block) | none — all met |

The rows, with actual values and limits, are in `criteria.csv`.

## The Owner's investigation (descriptive; chooses nothing)

**Ladder decomposition of v4 − v3** (equal-fold score differences; the brackets sum to the total exactly: True):

| Step | Change | dS_MAE [95%] | dS_WIS [95%] |
|---|---|---|---|
| v4 → M | the split removed | -0.0013 [-0.0036, 0.0016] | -0.0008 [-0.0030, 0.0022] |
| M → A-PN-sel | the raw half dropped | 0.0015 [-0.0025, 0.0048] | 0.0005 [-0.0030, 0.0040] |
| A-PN-sel → R | averaging over capacities instead of daily selection | 0.0010 [-0.0009, 0.0025] | 0.0012 [-0.0006, 0.0026] |
| v3 → R | v3 to R | -0.0290 [-0.0366, -0.0210] | -0.0256 [-0.0322, -0.0185] |
| v3 → v4 | v3 to v4 (CP-21) | -0.0301 [-0.0368, -0.0228] | -0.0266 [-0.0327, -0.0204] |

Member-weight curve (central forecast, before any interval layer; **oracle, not selectable**): the weight with the lowest central S_MAE for each member is {'L-N': 0.5, 'L-P': 0.45, 'PN-avg': 0.45, 'PN-sel': 0.45, 'mean(PN-sel, L-P)': 0.55, 'v4 member mean(L-N, L-R)': 0.55} (`investigation/member-weight-curve.csv`). The fixed weight is 1/3; no weight is learned (D6).

**Capacity-selection stability** (inner validation, evaluation origins):

| Model | flip rate | winner margin (median) | G1 | G2 | G3 | G4 |
|---|---|---|---|---|---|---|
| PN pooled | 0.540 | 1.11% | 0.22 | 0.21 | 0.25 | 0.33 |
| L-P pooled | 0.503 | 1.28% | 0.21 | 0.15 | 0.28 | 0.36 |
| L-R night | 0.533 | 1.57% | 0.36 | 0.16 | 0.21 | 0.27 |
| L-R solar | 0.483 | 1.63% | 0.40 | 0.17 | 0.23 | 0.19 |
| L-R shoulder | 0.524 | 1.36% | 0.25 | 0.10 | 0.30 | 0.35 |
| L-N night | 0.463 | 1.59% | 0.48 | 0.18 | 0.14 | 0.20 |
| L-N solar | 0.542 | 1.44% | 0.36 | 0.18 | 0.23 | 0.23 |
| L-N shoulder | 0.524 | 1.18% | 0.33 | 0.18 | 0.20 | 0.29 |

**Extrapolation:** 26 extreme or top-5% days, 8 of them above the origin's training-window maximum (`investigation/extrapolation.csv`: actual, window and forecast maxima per member).

**Reaction after the peak began (2022-08-15):**

| Policy | ACI reaction (days) | width reaction (days) |
|---|---|---|
| v4 | not applicable (no ACI) | 12 |
| v4+DL | 3 | 4 |
| v3 | not applicable (no ACI) | 12 |
| v3+DL | 3 | 4 |

Coverage by hour, block and regime: `diagnostics.csv` (hour/block, 56-date support rule) and `investigation/coverage-regime.csv` (terciles of the issued 168-hour scale); each fold's alpha_t path: `investigation/alpha-paths.csv`.

**Sharp changes** (each fold's 5% largest daily-mean changes and the peak's first ten days, each with the three days after; pooled over the event windows, so an overlapping day counts once per event; per offset in `investigation/shock-days.csv`). With no winner W, W, W+DL and W+DLF do not exist; the same windows are reported for v4, v4+DL, v3 and v3+DL:

| Set / policy | hours | MAE | WIS | cov95 |
|---|---|---|---|---|
| largest_daily_mean_change/v3 | 2328 | 20.25 | 12.05 | 0.927 |
| largest_daily_mean_change/v3+DL | 2328 | 20.98 | 13.19 | 0.954 |
| largest_daily_mean_change/v4 | 2328 | 19.59 | 11.54 | 0.937 |
| largest_daily_mean_change/v4+DL | 2328 | 20.47 | 12.75 | 0.956 |
| peak_first_ten_days/v3 | 960 | 44.24 | 24.44 | 0.953 |
| peak_first_ten_days/v3+DL | 960 | 43.29 | 24.70 | 0.969 |
| peak_first_ten_days/v4 | 960 | 46.98 | 25.30 | 0.950 |
| peak_first_ten_days/v4+DL | 960 | 45.12 | 25.47 | 0.969 |

**LEAR's penalty-selection stability (D8)**, from logged selections in the verified CP-20 cache (no refit):

| Component | phase | flip rate | median margin |
|---|---|---|---|
| A1 | evaluation | 0.106 | 6.19% |
| A1 | warm-up | 0.101 | 7.56% |
| B2 | evaluation | 0.103 | 5.84% |
| B2 | warm-up | 0.092 | 7.28% |

## Fit cost and daily cycle (diagnostic, §17.5 D3)

PN: 5088 fits over 636 origins; inner fits 1557 s and full-window fits 1585 s single-thread wall; median per origin 4.98 s for all eight, 2.52 s for R's four full-window fits, 3.06 s for PN-sel's selection and refit. CP-21 L-P: 3.24 s per origin.

Complete cold daily cycle, M: median 19.3 s, maximum 47.6 s over 25 origins, four workers; every bitwise check passed.

Complete cold daily cycle, R: median 17.9 s, maximum 54.9 s over 25 origins, four workers; every bitwise check passed.

## Integrity

- Controls (`controls.json`): 71 checks, all passed: True.
- v3 and v4 through CP-22's H-layer replay path reproduce the committed vectors bit for bit on all 10,747 keys: v3 True, v4 True (`parity.json`).
- Independent representative HG and v4 slice, refitted (`reproduction.json`): bitwise True.
- Scoring reproduces CP-20's and CP-21's committed §8 rows and intervals for v3 and v4: True.

## Resources against the §20.8 ceilings

| Dimension | Used | Cap |
|---|---|---|
| active_seconds | 6565.41 | 115200 |
| additional_disk_bytes | 44411051 | 10737418240 |
| analysis_passes | 1 | 3 |
| component_attempts | 124 | 1600 |
| download_bytes | 0 | 0 |
| lgbm_fits | 5768 | 9000 |
| machine_seconds | 12491.46 | 108000 |
| main_lgbm_fits | 5088 | 6000 |
| policy_days | 6276 | 16000 |
| primitive_fits | 14880 | 192000 |
| reference_passes | 1 | 3 |
| remote_writes | 0 | 0 |
| rss_bytes | 3220520960 | 10737418240 |
| workers | 4 | 4 |

work resumed Saturday 2026-10-03 20:33 IDT, inside the Friday/Shabbat window, on the Owner's explicit written exception (scripts/cp22_owner_calendar_exception.py; ledger events owner_calendar_exception_used); no job ran on Friday or Saturday before that instruction

## What this result does not establish

- No confirmatory or out-of-sample claim: development_post_selection on folds already used by CP-15, CP-20 and CP-21.
- Non-inferiority here means no 95% interval lies entirely above zero; it is not equivalence.
- No release, final-product designation, freeze, Live or economic claim; v1 remains the released product.
- The member weight is fixed at 1/3; the member-weight curve is an oracle and selects nothing.

Reproduction: `reports/v4-revision/reproduce.md`. Protocol: `reports/v4-revision/protocol.json` (committed before any main fit).

