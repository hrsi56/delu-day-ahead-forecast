# 4.6R — DDNN training-only resource entry (CP-23)

- **Verdict: PASS.** Every measured requirement holds, and the projected full run fits
  inside every §21.8 ceiling. The route continues to the frozen pre-run protocol, then 4.6C.
- **Plan:** `capstone_v21.md` v21-r10 §21.4 (4.6R), handoff 4.6R.
- **Machine:** macOS-26.5.2-arm64-arm-64bit-Mach-O, CPU only, BLAS 1 thread, one worker in this job.
- **Machine-readable record:** `reports/distribution-challenger/resource-admission.json`, with
  every fit (configuration, seed, rows, epochs, wall and CPU seconds, weight hash).
- **Run:** `python scripts/cp23_ddnn.py monitor --name resource-admission ... -- python
  scripts/cp23_ddnn.py job resource-admission` (`src/cp23/admission.py`), 2026-10-04T14:58:46Z.

## Order and data

- **The §21.3 checks passed first.** The job refuses to run without a passing PyTorch reference
  record for the exact `src/cp23/ddnn.py` bytes (`reports/distribution-challenger/reference-checks.json`,
  2026-10-04T14:55:17Z, `ddnn.py` SHA-256 `9ee60719bed5ea62…`).
- **Training partitions only.** The two origins are fold 1's and fold 5's genuine warm-up starts. Each
  fold's data was materialised strictly before its first evaluation day (fold 1 through
  2020-06-30, fold 5 through 2026-01-07), so
  no evaluation-fold or reserved outcome was read.
- **Accuracy-blind.** No validation or holdout loss value is reported or used, and nothing is scored.
  The fits ran exactly as the main run will run them: the frozen configurations, four seeds, early
  stopping on the window's last 28 days, and quantile-averaged emission.
- **Scale.** Fold 5's origin has a full 728-day window (16,763 training
  rows), the representative scale. Fold 1's is the shortest a fold starts with
  (10,838 rows). Each fit has
  71 inputs.

## Measured values

| Fold | Origin | Config | Parameters | Training / early-stopping rows | Four-seed fit (s) | Prediction (ms) | Finite / ordered / p50 = central | Rearranged rows |
|---|---|---|---|---|---|---|---|---|
| fold_1 | 2020-05-25 | C1 | 2,436 | 10,838 / 672 | 2.5 | 0.17 | yes / yes / yes | 0 |
| fold_1 | 2020-05-25 | C2 | 3,492 | 10,838 / 672 | 3.3 | 0.20 | yes / yes / yes | 0 |
| fold_1 | 2020-05-25 | C3 | 9,028 | 10,838 / 672 | 4.1 | 0.28 | yes / yes / yes | 0 |
| fold_1 | 2020-05-25 | C4 | 26,244 | 10,838 / 672 | 7.6 | 0.39 | yes / yes / yes | 0 |
| fold_5 | 2025-12-02 | C1 | 2,436 | 16,763 / 672 | 3.8 | 0.15 | yes / yes / yes | 0 |
| fold_5 | 2025-12-02 | C2 | 3,492 | 16,763 / 672 | 5.4 | 0.19 | yes / yes / yes | 0 |
| fold_5 | 2025-12-02 | C3 | 9,028 | 16,763 / 672 | 7.3 | 0.26 | yes / yes / yes | 0 |
| fold_5 | 2025-12-02 | C4 | 26,244 | 16,763 / 672 | 11.0 | 0.41 | yes / yes / yes | 0 |

| Config | Mean fit, full window (s) | Max fit (s) | Mean epochs run | Max epochs run |
|---|---|---|---|---|
| C1 | 0.96 | 1.30 | 54.4 | 74 |
| C2 | 1.36 | 1.50 | 45.6 | 52 |
| C3 | 1.81 | 2.76 | 34.5 | 56 |
| C4 | 2.74 | 3.04 | 30.8 | 34 |

- **Peak memory:** 0.72 GiB resident in the single process (ledger peak
  0.72 GiB, process tree).
- **Load and design:** 1.0 s (fold 1) and
  16.1 s (fold 5).
- **Emission:** the seven CP-15 quantiles and the p50 were finite and ordered for every configuration at
  both origins. The p50 equals the central forecast, the ensemble median. Quantile averaging needed no
  rearrangement.
- **Best epochs** (descriptive, not used): C1 [6, 17, 28, 30, 30, 31, 44, 49], C2 [13, 16, 17, 20, 23, 24, 25, 27],
  C3 [3, 4, 6, 6, 7, 9, 10, 31], C4 [3, 3, 4, 5, 7, 7, 8, 9]. The larger networks reach their best inner-validation
  loss within a few epochs, so early stopping ends them near epoch 30. That is the frozen recipe working
  as designed, and nothing was changed in response.

## Projection against §21.8

| Ceiling | Projected | Maximum | Basis |
|---|---|---|---|
| DDNN fits, main run | 2,624 | 4,000 | 636 origins with eligible hours × 4 seeds, plus 80 selection fits (5 folds × 4 configurations × 4 seeds) |
| DDNN fits, total | 4,560 | 6,000 | main, plus 4.6R 32, controls 240, reproduction 24, daily cycle 100, review 40, repair reserve 1500 |
| Machine-hours | 15.2 | 60 | every fit at the largest configuration's mean full-window time (2.74 s) × 1.5, giving 5.2 h, plus 10 h for replay, scoring, controls, tests and review |
| Policy-days | 4,902 | 8,000 | v5 and v3+D replay 1,276, D issuance 450, HG/v4 parity 1,276, controls 300, daily cycle 100, review 1,500 |
| Aggregate RSS | 3.87 GiB | 10 GiB | four workers at the measured single-process peak, plus 1 GiB for the parent and the monitor |
| Added disk | ≤ 1 GiB | 10 GiB | per-origin caches of a few tens of kB, states, logs, the local MLflow store and two worktrees |
| Workers, BLAS, devices | 4, 1, CPU | 4, 1, CPU | no GPU, MPS or cloud |
| Data, network, cost | 0 data bytes, 0 remote writes, $0 | 0, 0, $0 | the one permitted download (the PyTorch test dependency) is recorded separately in the ledger |

The main run's wall time with four workers is about 0.7 h at the
projected rate. No ceiling is approached, so there is no blocker. 4.6R does not lead to a smaller or
larger experiment: the frozen recipe is the one the protocol commits.
