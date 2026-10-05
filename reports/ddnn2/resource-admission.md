# 4.6R′ — DDNN-2 training-only resource entry (CP-24)

- **Checkpoint:** CP-24, under `capstone_v21.md` v21-r11 §23.7 (4.6R′), after 4.6L′ (PASS) and the §23.7 correctness
  checks (import audit, finite-difference checks, 32 of 32 PyTorch reference checks).
- **Verdict: PASS.** The machine-readable record is [`resource-admission.json`](resource-admission.json); this file
  restates it.
- **Data:** pre-fold only. Every timing fit is a search-style fit at a validation batch's first day b (fold 1's earliest
  batch 2020-01-06, fold 3's 2022-03-02 and fold 5's 2025-09-09 latest batches), trains on
  [max(2019-01-01, b − 728), b) minus its held-out weeks and the uncovered days (§23.6), and forecasts only that batch's 28
  days: never a gate, warm-up or evaluation day. The record is accuracy-blind: it holds cost, memory, finiteness and order,
  never a score.

## What was measured

| Fit | Inputs | Parameters | Epochs run | Best epoch | Fit seconds | Seconds/epoch | Cap activations | Finite, ordered |
|---|---|---|---|---|---|---|---|---|
| R-largest@fold_1 | 346 | 489,568 | 92 | 42 | 5.07 | 0.0551 | 2 | True |
| R-largest@fold_3 | 346 | 489,568 | 77 | 27 | 9.31 | 0.1209 | 2 | True |
| R-largest@fold_5 | 346 | 489,568 | 71 | 21 | 8.08 | 0.1138 | 14 | True |
| R-random-00@fold_5 | 111 | 33,168 | 129 | 79 | 0.98 | 0.0076 | 6 | True |
| R-random-01@fold_5 | 111 | 6,368 | 86 | 36 | 0.29 | 0.0034 | 8 | True |
| R-random-02@fold_5 | 250 | 52,840 | 508 | 458 | 5.99 | 0.0118 | 0 | True |
| R-random-03@fold_5 | 103 | 7,496 | 113 | 63 | 0.80 | 0.0071 | 3 | True |
| R-random-04@fold_5 | 266 | 61,661 | 85 | 35 | 0.50 | 0.0059 | 2 | True |
| R-random-05@fold_5 | 87 | 5,616 | 117 | 67 | 0.66 | 0.0056 | 0 | True |
| R-random-06@fold_5 | 290 | 37,965 | 187 | 137 | 2.17 | 0.0116 | 0 | True |
| R-random-07@fold_5 | 154 | 7,021 | 117 | 67 | 0.41 | 0.0035 | 0 | True |
| R-random-08@fold_1 | 250 | 146,183 | 98 | 48 | 1.18 | 0.0120 | 0 | True |
| R-random-09@fold_3 | 207 | 9,705 | 76 | 26 | 0.65 | 0.0086 | 0 | True |
| R-random-10@fold_1 | 247 | 21,810 | 164 | 114 | 0.47 | 0.0029 | 3 | True |
| R-random-11@fold_3 | 266 | 22,602 | 143 | 93 | 1.28 | 0.0090 | 41 | True |
| R-smallest@fold_1 | 55 | 2,528 | 74 | 24 | 0.08 | 0.0011 | 3 | True |
| R-smallest@fold_3 | 55 | 2,528 | 104 | 54 | 0.20 | 0.0019 | 0 | True |
| R-smallest@fold_5 | 55 | 2,528 | 98 | 48 | 0.20 | 0.0020 | 0 | True |

- **Extremes of the space:** the smallest network (one layer of 16, batch 128, no optional group) and the largest in
  compute terms (two layers of 512, batch 32, every optional group, dropout 0.5, κ = 0.5, lr 1e-4). The largest took at most
  9.3 s per fit; the smallest at most 0.20 s.
- **A sample of 12 round-1 configurations,** drawn with a dedicated 4.6R′ sampler stream (never the search's):
  mean 1.28 s, 75th percentile 1.20 s, maximum 5.99 s per fit.
- **Peak memory:** 812 MiB per worker process; 3.17 GiB for four, under the 10 GiB cap.
- **Emission:** every member's 28-day emission is finite and ordered; the eight-member ensemble (fold 5's sample) combined by
  the per-level median is finite and ordered, with 0 crossings to restore.
- **Failed fits:** 0.

## Projection against §23.11, with the review reserve

- Search fits are priced at the sample's mean fit time; gate and attempt members at its 75th percentile; the worst case prices
  every gate and attempt member at the largest extreme's time. Attempt fits: 5088 (636 origins with eligible hours x 8 members); gate fits: 2240 per round (280 x 8).
- Search fits per round: sum over folds of N x min(4, B_f) + ceil(N/3) x (B_f - min(4, B_f)), B = [3, 7, 11, 11, 11].
- Active hours: elapsed so far + compute wall at 4 workers + serial Lead work not overlapped by compute (2 h + 0.5 h per round + 3 h per attempt) + the review reserve.
- Review reserve: {"active_hours": 5.0, "bootstrap_passes": 2, "ddnn2_fits": 400, "machine_hours": 6.0, "policy_days": 600, "reference_passes": 1}; other work per attempt: {"ddnn2_fits": 200, "machine_hours": 3.0, "policy_days": 300}.

| Trials per fold per round | Route | DDNN-2 fits | Machine-hours | Active hours | Policy-days | Fits every ceiling | Worst case: machine-hours, active hours, fits |
|---|---|---|---|---|---|---|---|
| 128 | minimal | 11,410 | 14.5 | 14.62 | 3,654 | True |  |
| 128 | maximal | 33,810 | 25.15 | 21.78 | 8,388 | True | 68.22, 32.55, True |
| 32 | minimal | 8,818 | 13.57 | 14.39 | 3,654 | True |  |
| 32 | maximal | 23,442 | 21.46 | 20.86 | 8,388 | True | 64.52, 31.62, True |
| 48 | minimal | 9,242 | 13.73 | 14.42 | 3,654 | True |  |
| 48 | maximal | 25,138 | 22.06 | 21.01 | 8,388 | True | 65.13, 31.78, True |
| 64 | minimal | 9,690 | 13.88 | 14.46 | 3,654 | True |  |
| 64 | maximal | 26,930 | 22.7 | 21.17 | 8,388 | True | 65.77, 31.94, True |
| 96 | minimal | 10,538 | 14.19 | 14.54 | 3,654 | True |  |
| 96 | maximal | 30,322 | 23.91 | 21.47 | 8,388 | True | 66.97, 32.24, True |

## What this record fixes (each frozen protocol repeats it)

- **The trial count: 128 per fold per round** — the largest trial count in [32, 48, 64, 96, 128] at which the maximal route fits every ceiling with the review reserve. The maximal route fits at every candidate count,
  including in the worst case, so the largest is taken.
- **The largest route that fits:** the maximal route (three rounds and attempt 1, then one round and attempt 2).
- **The review reserve:** {"active_hours": 5.0, "bootstrap_passes": 2, "ddnn2_fits": 400, "machine_hours": 6.0, "policy_days": 600, "reference_passes": 1}.

## Disposition

**PASS.** The minimal and the maximal routes fit every §23.11 ceiling with the review reserve, emission is finite and ordered,
and no fit failed. The route continues to the pre-fold rounds (§23.6).
