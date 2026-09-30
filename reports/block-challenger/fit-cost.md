# CP-21 fit cost and daily retraining — a diagnostic, not a selection criterion

**Owner decision D3 (capstone v21-r6 §17.5).** v21-r5 §16 still requires any final-product candidate to retrain daily, or to obtain an Owner-approved exception before live admission. Measured on the Apple M3 (16 GB, CPU only), LightGBM with one thread per process and at most four processes, BLAS 1.

## LightGBM fits by arm and model (main run, every origin)

| Arm | Model | Origins | Window rows (mean / min / max) | Inner fit wall s (total) | Final fit wall s (total) | CPU s (inner + final) | Median final fit s | Peak worker RSS (GiB) | Selected capacity (count) | Exact ties |
|---|---|---|---|---|---|---|---|---|---|---|
| L-N | night | 636 | 5,505 / 3,830 / 5,812 | 915 | 196 | 1,089 | 0.22 | 0.77 | G1: 272, G2: 123, G3: 95, G4: 146 | 0 |
| L-N | shoulder | 636 | 6,207 / 4,320 / 6,552 | 985 | 248 | 1,210 | 0.28 | 0.77 | G1: 214, G2: 111, G3: 122, G4: 189 | 0 |
| L-N | solar | 636 | 4,827 / 3,360 / 5,096 | 864 | 205 | 1,048 | 0.22 | 0.77 | G1: 223, G2: 117, G3: 140, G4: 156 | 0 |
| L-P | pooled | 636 | 16,539 / 11,510 / 17,460 | 1,598 | 449 | 2,006 | 0.75 | 0.77 | G1: 151, G2: 103, G3: 173, G4: 209 | 0 |
| L-R | night | 636 | 5,505 / 3,830 / 5,812 | 948 | 237 | 1,161 | 0.27 | 0.77 | G1: 209, G2: 118, G3: 128, G4: 181 | 0 |
| L-R | shoulder | 636 | 6,207 / 4,320 / 6,552 | 1,027 | 290 | 1,291 | 0.48 | 0.77 | G1: 174, G2: 72, G3: 180, G4: 210 | 0 |
| L-R | solar | 636 | 4,827 / 3,360 / 5,096 | 892 | 186 | 1,057 | 0.21 | 0.77 | G1: 283, G2: 103, G3: 125, G4: 125 | 0 |

Fits: 22,260 (17,808 inner selection fits on each window minus its last 28 days, 4,452 final refits). Block against pooled: the three L-R block models took 1.75× the single L-P pooled model's wall time (3,580 s against 2,047 s). Per origin and model: `fit-cost-by-origin.csv`; per fit (rows, capacity, validation MAE, wall and CPU seconds, worker memory, tree hash): `fits.parquet`.

## HG component regeneration

HG's A1_w and B2_w were reused from the verified CP-20 cache in the main run (no regeneration). They were refitted only as checks: control 12, daily_cycle 50 component-days, each equal to the CP-20 cache bit for bit (`daily-cycle.json`, `controls.json`).

## HGL's complete daily cycle, measured cold

25 origins, five per fold (five per fold at offsets 0/22/44/66/88 days into the 90-day window (next day with eligible hours)). Each cycle starts cold: the parent loads its data, then a fresh pool of four processes loads its own data and refits A1_w, B2_w and the six block models (L-R and L-N, with capacity selection); the parent blends HGL, loads the persisted interval-layer state, releases, predicts and issues. **Median 24.7 s, maximum 69.4 s** (minimum 11.7 s).

| Fold | Day | Total s | Components s (A1 / B2) | Slowest block s | H layer + issue s | Bitwise checks |
|---|---|---|---|---|---|---|
| fold_1 | 2020-07-01 | 11.7 | 4.6 / 5.0 | 2.0 | 0.01 | pass |
| fold_1 | 2020-07-23 | 12.6 | 5.3 / 6.6 | 2.9 | 0.01 | pass |
| fold_1 | 2020-08-14 | 14.6 | 7.8 / 7.6 | 2.9 | 0.01 | pass |
| fold_1 | 2020-09-05 | 14.7 | 10.3 / 8.9 | 2.7 | 0.01 | pass |
| fold_1 | 2020-09-27 | 15.9 | 8.0 / 9.0 | 2.8 | 0.01 | pass |
| fold_2 | 2021-04-01 | 18.1 | 8.7 / 6.4 | 3.1 | 0.01 | pass |
| fold_2 | 2021-04-23 | 18.0 | 8.3 / 7.0 | 2.5 | 0.01 | pass |
| fold_2 | 2021-05-15 | 18.7 | 8.7 / 6.6 | 2.8 | 0.01 | pass |
| fold_2 | 2021-06-06 | 18.6 | 8.1 / 4.9 | 2.6 | 0.01 | pass |
| fold_2 | 2021-06-28 | 17.9 | 6.8 / 5.7 | 2.7 | 0.01 | pass |
| fold_3 | 2022-07-01 | 24.7 | 7.6 / 3.7 | 2.7 | 0.01 | pass |
| fold_3 | 2022-07-23 | 24.6 | 7.0 / 3.6 | 2.5 | 0.01 | pass |
| fold_3 | 2022-08-14 | 24.5 | 7.0 / 4.0 | 2.4 | 0.01 | pass |
| fold_3 | 2022-09-05 | 28.0 | 8.7 / 3.8 | 3.0 | 0.01 | pass |
| fold_3 | 2022-09-27 | 26.0 | 6.4 / 4.7 | 3.0 | 0.01 | pass |
| fold_4 | 2025-05-01 | 52.3 | 6.8 / 6.6 | 3.1 | 0.01 | pass |
| fold_4 | 2025-05-23 | 64.5 | 7.4 / 7.0 | 4.2 | 0.02 | pass |
| fold_4 | 2025-06-14 | 55.7 | 7.0 / 6.3 | 3.4 | 0.01 | pass |
| fold_4 | 2025-07-06 | 56.2 | 6.7 / 6.3 | 2.7 | 0.01 | pass |
| fold_4 | 2025-07-28 | 57.1 | 7.0 / 7.4 | 3.0 | 0.01 | pass |
| fold_5 | 2026-01-08 | 62.5 | 6.4 / 5.6 | 2.3 | 0.01 | pass |
| fold_5 | 2026-01-30 | 66.1 | 8.3 / 6.3 | 2.3 | 0.01 | pass |
| fold_5 | 2026-02-21 | 65.3 | 7.0 / 6.9 | 2.4 | 0.01 | pass |
| fold_5 | 2026-03-15 | 65.1 | 6.2 / 6.5 | 3.1 | 0.01 | pass |
| fold_5 | 2026-04-06 | 69.4 | 8.0 / 8.6 | 3.3 | 0.01 | pass |

Bitwise checks: the refitted A1_w/B2_w equal CP-20's cached components, the six block fits and their trees equal the main run's, and the issued HGL central and quantile vector equal the committed prediction.

