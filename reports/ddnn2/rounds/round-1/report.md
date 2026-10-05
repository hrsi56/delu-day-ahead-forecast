# Pre-fold round 1 report (CP-24)

- **Before attempt:** 1. **Trials per fold:** 128. **Design:** [`design.json`](design.json); **search ledger:** [`search-ledger.json`](search-ledger.json); **ensembles:** [`ensembles.json`](ensembles.json); **gate:** [`gate.json`](gate.json).
- **Evidence class:** pre-fold, training-only. This report carries no warm-up or evaluation outcome: every fit here trained and forecast before its fold's D0 (the search before D0 − 56).
- **Gate: PASS.**

## The gate (§23.6), pooled over the 280 gate days

| Condition | Met | Values |
|---|---|---|
| G0 finite and ordered | True | every DDNN-2 and v4-member forecast |
| G1 MAE(v5) ≤ MAE(v4) | True | v5 12.538, v4 12.849, difference -0.3117 EUR/MWh |
| G2 MAE(D2) ≤ 1.10 × MAE(L) | True | D2 11.362, L 13.329, ratio 0.8525 |
| G3 cap binds on < 0.1% | True | 331 of 375,984 member hour-levels (0.088%) |

## By fold

| Fold | Gate window | Days | Hours | MAE v4 | MAE v5 | MAE D2 | MAE L | MAE HG | Cap share | corr(D2, HG) | corr(D2, L) | Excluded days (v4 / DDNN-2, max) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fold_1 | 2020-03-30..2020-05-24 | 56 | 1341 | 4.871 | 4.859 | 4.284 | 4.511 | 5.497 | 0.326% | 0.889 | 0.927 | 0 / 0 |
| fold_2 | 2020-12-29..2021-02-22 | 56 | 1344 | 6.299 | 6.104 | 5.060 | 6.130 | 6.875 | 0.009% | 0.804 | 0.854 | 0 / 0 |
| fold_3 | 2022-03-30..2022-05-24 | 56 | 1343 | 22.309 | 21.955 | 19.787 | 22.659 | 24.356 | 0.029% | 0.790 | 0.769 | 0 / 0 |
| fold_4 | 2025-01-25..2025-03-21 | 56 | 1344 | 14.527 | 13.821 | 13.174 | 17.405 | 14.361 | 0.004% | 0.840 | 0.782 | 55 / 55 |
| fold_5 | 2025-10-07..2025-12-01 | 56 | 1342 | 16.236 | 15.945 | 14.502 | 15.928 | 17.459 | 0.072% | 0.870 | 0.876 | 0 / 0 |
| pooled | | 280 | 6714 | 12.849 | 12.538 | 11.362 | 13.329 | 13.710 | 0.088% | 0.826 | 0.806 | |

## The search and each fold's ensemble

### fold_1 (D0 2020-05-25, B = 3, batches 2020-01-06..2020-03-29)

- 128 trials, 384 fits, 0 failed; 128 ran all 3 batches.
- Pinball on the 3 most recent batches: best 1.333, median 1.989, worst 5.023 EUR/MWh.

| Rank | Trial | Layers | Activation | Transform | κ | Half-life | Batch | lr | Dropout | L1 | L2 | Groups | Validation pinball | Validation MAE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | r1-f1-t099 | [26, 238] | softplus | asinh-mad | 1.0 | 365 | 128 | 4.48e-03 | n/a | off | off | price_d2, price_d3, gfs, stats | 1.333 | 4.750 |
| 2 | r1-f1-t052 | [447, 198] | tanh | asinh-mad | 0.0 | None | 128 | 3.51e-03 | 0.08 | off | 2.7e-03 | price_d3, load_d1, gfs, stats | 1.394 | 4.900 |
| 3 | r1-f1-t015 | [18] | softplus | asinh-s4 | 1.0 | 365 | 128 | 5.57e-03 | 0.12 | off | 2.0e-05 | price_d2, load_d1, gfs, stats | 1.413 | 5.038 |
| 4 | r1-f1-t014 | [107, 74] | elu | z-mad | 0.5 | 365 | 32 | 1.44e-03 | 0.11 | off | 7.9e-03 | price_d7, load_d7, gfs, stats, calendar | 1.466 | 5.254 |

### fold_2 (D0 2021-02-23, B = 7, batches 2020-01-28..2020-12-28)

- 128 trials, 641 fits, 0 failed; 43 ran all 7 batches.
- Pinball on the 4 most recent batches: best 1.383, median 2.018, worst 33.373 EUR/MWh.

| Rank | Trial | Layers | Activation | Transform | κ | Half-life | Batch | lr | Dropout | L1 | L2 | Groups | Validation pinball | Validation MAE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | r1-f2-t010 | [98] | softplus | asinh-s4 | 0.0 | 180 | 32 | 8.25e-04 | n/a | 6.1e-06 | 1.7e-03 | price_d3, price_d7, load_d7, gfs, stats, calendar | 1.428 | 5.005 |
| 2 | r1-f2-t006 | [102, 423] | elu | asinh-s4 | 0.5 | None | 64 | 1.37e-03 | 0.18 | 1.1e-04 | off | price_d2, load_d1, load_d7, gfs, stats | 1.432 | 4.986 |
| 3 | r1-f2-t095 | [30, 27] | softplus | asinh-mad | 0.0 | 365 | 128 | 2.52e-04 | 0.17 | off | off | price_d2, gfs, stats | 1.458 | 5.059 |
| 4 | r1-f2-t053 | [127, 69] | softplus | z-s4 | 0.0 | None | 64 | 1.57e-04 | 0.08 | 2.9e-07 | 1.2e-05 | price_d2, gfs, stats, calendar | 1.472 | 5.085 |

### fold_3 (D0 2022-05-25, B = 11, batches 2020-12-09..2022-03-29)

- 128 trials, 813 fits, 0 failed; 43 ran all 11 batches.
- Pinball on the 4 most recent batches: best 9.544, median 12.902, worst 30.314 EUR/MWh.

| Rank | Trial | Layers | Activation | Transform | κ | Half-life | Batch | lr | Dropout | L1 | L2 | Groups | Validation pinball | Validation MAE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | r1-f3-t087 | [23] | softplus | z-s4 | 0.5 | 365 | 32 | 1.44e-04 | n/a | off | 1.7e-03 | price_d3, price_d7, load_d1, gfs | 6.048 | 20.934 |
| 2 | r1-f3-t127 | [143, 95] | tanh | asinh-s4 | 0.0 | 180 | 64 | 3.46e-03 | n/a | 1.8e-04 | off | price_d2, gfs | 6.193 | 21.812 |
| 3 | r1-f3-t033 | [76, 17] | softplus | z-s4 | 0.5 | 365 | 32 | 2.72e-03 | 0.18 | 4.9e-06 | 8.0e-04 | load_d1, gfs, stats | 6.381 | 22.590 |
| 4 | r1-f3-t084 | [41, 29] | elu | asinh-s4 | 1.0 | None | 128 | 1.48e-03 | n/a | 4.5e-04 | 2.6e-06 | price_d7, gfs, stats | 6.500 | 22.115 |

### fold_4 (D0 2025-03-22, B = 11, batches 2024-03-23..2025-01-24)

- 128 trials, 813 fits, 0 failed; 43 ran all 11 batches.
- Pinball on the 4 most recent batches: best 6.398, median 8.474, worst 30.936 EUR/MWh.

| Rank | Trial | Layers | Activation | Transform | κ | Half-life | Batch | lr | Dropout | L1 | L2 | Groups | Validation pinball | Validation MAE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | r1-f4-t079 | [161, 24] | tanh | asinh-mad | 0.0 | 365 | 32 | 1.60e-03 | n/a | 3.3e-05 | 1.1e-03 | price_d2, load_d1, gfs, stats | 5.006 | 17.019 |
| 2 | r1-f4-t103 | [181, 96] | softplus | asinh-mad | 0.5 | 365 | 32 | 3.04e-04 | 0.32 | 6.2e-07 | off | price_d2, load_d1, gfs, stats, calendar | 5.192 | 17.559 |
| 3 | r1-f4-t000 | [344] | softplus | asinh-mad | 0.0 | 365 | 128 | 3.69e-03 | n/a | 1.4e-04 | 1.4e-03 | price_d2, price_d3, load_d1, load_d7, gfs, calendar | 5.321 | 17.737 |
| 4 | r1-f4-t004 | [50] | elu | asinh-mad | 0.0 | None | 128 | 5.01e-03 | 0.28 | 2.3e-06 | 3.0e-04 | price_d2, price_d7, load_d1, load_d7, gfs, stats | 5.428 | 17.804 |

### fold_5 (D0 2025-12-02, B = 11, batches 2024-06-18..2025-10-06)

- 128 trials, 813 fits, 2 failed; 43 ran all 11 batches.
- Pinball on the 4 most recent batches: best 4.621, median 6.139, worst 198.268 EUR/MWh.

| Rank | Trial | Layers | Activation | Transform | κ | Half-life | Batch | lr | Dropout | L1 | L2 | Groups | Validation pinball | Validation MAE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | r1-f5-t042 | [231] | tanh | z-mad | 0.0 | None | 32 | 2.74e-03 | n/a | 6.3e-04 | off | load_d1, gfs, stats | 5.126 | 17.791 |
| 2 | r1-f5-t106 | [304] | softplus | z-mad | 1.0 | 365 | 64 | 6.88e-03 | n/a | off | 1.8e-03 | load_d7, gfs | 5.128 | 17.490 |
| 3 | r1-f5-t026 | [317] | elu | z-mad | 0.5 | 365 | 128 | 1.22e-03 | n/a | off | 4.4e-03 | price_d2, load_d1, load_d7, gfs | 5.153 | 17.192 |
| 4 | r1-f5-t091 | [480, 107] | tanh | z-mad | 0.0 | 180 | 32 | 1.26e-03 | 0.42 | 2.7e-04 | 3.1e-06 | price_d3, price_d7, load_d1, gfs, stats, calendar | 5.167 | 17.692 |

## Costs

- DDNN-2 member fits so far: 5,725 (search 3,465, gate 2,240, 4.6R′ 18).
- Machine-hours so far: 5.28 of 150.
- This round's jobs: v4-gate 1.91 machine-hours; search-r1 0.44 machine-hours; search-r1 1.25 machine-hours; gate-r1 1.47 machine-hours.
- Gate fit seconds: DDNN-2 4986, v4 members 6710 (the v4 pass is one pass, reused across rounds).

## Excluded training days (§23.6)

- Every pre-fold fit leaves out the delivery days without a frozen weather record (2022-09-29..2023-03-24). Per gate day, the number left out is in `gate.json` (`excluded_training_days`); per search fit, in the ledger.
- v4's members on fold 4's gate days: 55 days at most; DDNN-2: 55 at most. Other folds' gate days: none.
