# CP-23 — the DDNN route: v5 = v4 plus a DDNN member

`capstone_v21.md` v21-r10 §21 · evidence class **development_post_selection** · population `common-10747h` (10,747 keys, five folds).

## Verdicts

| Status | Result |
|---|---|
| Engineering | Bound to the fresh Integration-Critic verdict on the final candidate (`docs/track-b/evidence/cp-23/integration.md`) |
| Entry | 4.6L: research use and retention permitted · §21.3: import audit, gradient checks and the PyTorch reference passed (26 of 26) · 4.6R: **PASS** · DDNN admitted to 4.6C |
| `cp23-adoption` | **v5 is not adopted: CP-23 becomes the branch "DDNN member on v4"** · first unmet condition **1** (unmet: 1, 4) |
| Research | Development finding under the rule pre-registered on 2026-10-04; one more decision on the same five folds (4.7T carries the protection) |
| Product | v1 remains the released product and the demo; no designation, freeze or Live follows (§16) |

The rule was applied mechanically to the committed tables (`reports/distribution-challenger/decisions.json`). D and v3+D are never eligible. A mixed result is no demonstrated joint preference, never equivalence.

## DDNN as run

- **Model:** feed-forward network, ELU hidden activations, four linear outputs per row; Johnson SU: xi = o1, lambda = softplus(o2) + 1e-3, gamma = o3, delta = softplus(o4) + 0.05; Y = xi + lambda*sinh((Z - gamma)/delta), Z ~ N(0,1). NumPy and the standard library only (`src/cp23/ddnn.py`; import audit in `tests/cp23/test_numpy_only.py`).
- **Information:** CP-15's 23 normalised LightGBM features (data.lgbm_normalized) with the categoricals ['day_of_week', 'day_type', 'local_hour', 'month'] one-hot encoded, plus the three frozen GFS columns and three missing indicators: 71 inputs. Target: §4: z = (y - level) / scale with each row's own origin statistics; quantiles inverted with the origin's level and scale.
- **Configurations:** C1 [32] (2,436 parameters), C2 [32, 32] (3,492 parameters), C3 [64, 64] (9,028 parameters), C4 [128, 128] (26,244 parameters). Selection: once per fold, before its first origin D0 (its genuine warm-up start), from data before D0 only; fixed for every origin of the fold; the lowest holdout MAE (EUR/MWh) of each configuration's four-seed ensemble median; an exact tie goes to the smaller configuration.
- **Chosen per fold** (`selection.json`): fold_1 C2 (holdout MAE C1 4.92, C2 4.18, C3 4.20, C4 4.23; margin 0.61%); fold_2 C4 (holdout MAE C1 6.04, C2 5.90, C3 5.90, C4 5.78; margin 2.03%); fold_3 C2 (holdout MAE C1 16.25, C2 15.50, C3 16.27, C4 17.46; margin 4.86%); fold_4 C3 (holdout MAE C1 25.68, C2 26.79, C3 25.67, C4 25.85; margin 0.03%); fold_5 C4 (holdout MAE C1 18.47, C2 17.66, C3 19.09, C4 17.64; margin 0.11%).
- **Training:** mean Johnson SU negative log-likelihood + l2 * sum(W^2) over weight matrices; Adam in PyTorch's update order (no weight decay, no amsgrad); learning rate 0.001, batch 256, L2 0.0001; early stopping on the window's last 28 calendar delivery days [D-28, D), training-only inner validation, patience 25, at most 400 epochs; best epoch kept.
- **Ensemble:** seeds [42, 43, 44, 45], quantile averaging at each level; the p50 and D are the ensemble median. History `[max(2019-01-01, D−728), D)`, a fresh fit at every one of the 636 origins with eligible hours.

## Scores (equal-fold ratios to B0; lower is better)

| Policy | S_MAE | S_WIS | pooled MAE (EUR/MWh) | pooled WIS | pooled 95% coverage | mean 95% width | §8 |
|---|---|---|---|---|---|---|---|
| v5 = (2/3)·v4 + (1/3)·D | 0.5421 | 0.5127 | 17.96 | 10.41 | 0.937 | 101.86 | met |
| v4 (three-block) | 0.5357 | 0.5056 | 17.55 | 10.24 | 0.939 | 101.92 | met |
| v3+D (DDNN as v3's third member) | 0.5514 | 0.5211 | 18.01 | 10.50 | 0.939 | 103.64 | met |
| v3 | 0.5658 | 0.5322 | 18.26 | 10.67 | 0.938 | 106.24 | met |
| D (DDNN alone) | 0.6319 | 0.5706 | 21.20 | 11.85 | 0.925 | 109.18 | not_met |
| A1 normalized LEAR | 0.6723 | 0.6460 | 20.71 | 12.45 | 0.942 | 134.33 | saved reference |
| B2 daily LEAR | 0.6578 | 0.6390 | 20.98 | 12.66 | 0.930 | 118.86 | saved reference |
| B0 naive | 1.0000 | 1.0000 | 32.81 | 20.02 | 0.907 | 166.60 | saved reference |
| B1 (v1) | 1.0518 | 0.9856 | 41.74 | 25.25 | 0.845 | 130.86 | saved reference |
| B3 daily LightGBM | 0.7841 | 0.7399 | 26.32 | 15.17 | 0.926 | 130.98 | saved reference |

## `cp23-adoption` (§21.6), condition by condition

1. Joint improvement over v4: dS_MAE 0.0064 [-0.0016, 0.0149] (needs upper ≤ 0), dS_WIS 0.0071 [-0.0009, 0.0138] (needs upper < 0) → **not met**. As a share of v4's score: S_MAE 1.20% [-0.29, 2.74]%, S_WIS 1.40% [-0.17, 2.72]%.
2. All six original §8 diagnostics: **met**.
3. A complete, valid evaluation: all 10,747 keys issued with finite, ordered quantiles; Engineering PASS is bound to the Integration verdict.
4. No resolved per-fold degradation: **not met** — fold_3 MAE 1.915 EUR/MWh [0.301, 4.395].

**Outcome:** v5 is not adopted: CP-23 becomes the branch "DDNN member on v4", with condition 1 as the reason.

## Every §21.5 contrast, with its reading

| Contrast | Role | dS_MAE [95%] | dS_WIS [95%] | ratio S_MAE [95%] | ratio S_WIS [95%] | Reading |
|---|---|---|---|---|---|---|
| D-HG | ddnn_alone_vs_v3_descriptive | 0.0661 [0.0315, 0.0949] | 0.0384 [0.0025, 0.0645] | 11.69% [5.42, 16.62]% | 7.22% [0.48, 11.98]% | observed joint worsening |
| D-HGL | ddnn_alone_vs_v4_descriptive | 0.0962 [0.0635, 0.1235] | 0.0651 [0.0299, 0.0898] | 17.97% [11.54, 22.87]% | 12.87% [5.85, 17.66]% | observed joint worsening |
| HGL-HG | lightgbm_as_v3_third_member_beside | -0.0301 [-0.0368, -0.0228] | -0.0266 [-0.0327, -0.0204] | -5.32% [-6.37, -3.97]% | -5.01% [-5.95, -3.80]% | observed joint improvement |
| v3+D-HG | ddnn_as_v3_third_member | -0.0144 [-0.0235, -0.0052] | -0.0111 [-0.0200, -0.0038] | -2.54% [-4.05, -0.91]% | -2.09% [-3.72, -0.71]% | observed joint improvement |
| v5-HG | reference_vs_v3 | -0.0237 [-0.0354, -0.0105] | -0.0196 [-0.0307, -0.0093] | -4.18% [-6.14, -1.85]% | -3.67% [-5.60, -1.73]% | observed joint improvement |
| v5-HGL | adoption_decision | 0.0064 [-0.0016, 0.0149] | 0.0071 [-0.0009, 0.0138] | 1.20% [-0.29, 2.74]% | 1.40% [-0.17, 2.72]% | no demonstrated joint preference |
| v5-v3+D | lightgbm_still_adds_given_ddnn | -0.0093 [-0.0136, -0.0035] | -0.0085 [-0.0122, -0.0040] | -1.68% [-2.47, -0.64]% | -1.62% [-2.30, -0.77]% | observed joint improvement |

Bootstrap: seed 15042, 2,000 replicates of 7-calendar-day blocks within each fold, the shared CP-20 index set (SHA-256 `e1df9a68dc6715aa2ecd9705ef61f504a3fe109ed917d1151ccbc46ea9e0f99b`, equal to CP-20's: True); every replicate is stored in `replicates.parquet`.

## Per-fold MAE and WIS (EUR/MWh)

| Policy | fold_1 MAE / WIS | fold_2 MAE / WIS | fold_3 MAE / WIS | fold_4 MAE / WIS | fold_5 MAE / WIS |
|---|---|---|---|---|---|
| v5 = (2/3)·v4 + (1/3)·D | 5.04 / 3.09 | 7.56 / 4.79 | 48.94 / 27.66 | 13.77 / 8.06 | 15.17 / 8.85 |
| v4 (three-block) | 4.93 / 3.02 | 7.71 / 4.79 | 47.03 / 27.01 | 13.77 / 8.05 | 14.95 / 8.69 |
| v3+D (DDNN as v3's third member) | 5.18 / 3.18 | 7.84 / 4.92 | 48.20 / 27.60 | 14.13 / 8.23 | 15.35 / 8.93 |
| v3 | 5.25 / 3.21 | 8.38 / 5.13 | 48.04 / 27.79 | 14.64 / 8.52 | 15.64 / 9.05 |
| D (DDNN alone) | 5.69 / 3.24 | 9.08 / 5.29 | 58.84 / 32.14 | 16.13 / 9.08 | 17.10 / 9.92 |
| A1 normalized LEAR | 6.82 / 4.10 | 9.95 / 6.25 | 51.21 / 30.45 | 16.74 / 10.09 | 19.48 / 11.75 |
| B2 daily LEAR | 6.22 / 3.95 | 9.68 / 6.04 | 54.01 / 32.32 | 16.54 / 9.91 | 19.20 / 11.53 |
| B0 naive | 8.63 / 5.71 | 16.17 / 10.89 | 86.95 / 51.73 | 22.98 / 14.56 | 30.50 / 17.92 |
| B1 (v1) | 6.61 / 4.00 | 20.04 / 10.82 | 140.99 / 87.94 | 20.07 / 11.37 | 23.17 / 13.47 |
| B3 daily LightGBM | 6.51 / 4.01 | 11.66 / 7.23 | 70.62 / 39.58 | 18.40 / 10.96 | 25.41 / 14.59 |

**v5 − v4 per fold** (paired daily-loss difference, EUR/MWh, 95%):

| Fold | MAE | WIS |
|---|---|---|
| fold_1 | 0.109 [-0.068, 0.244] | 0.075 [-0.004, 0.138] |
| fold_2 | -0.150 [-0.501, 0.106] | 0.003 [-0.270, 0.270] |
| fold_3 | 1.915 [0.301, 4.395] | 0.648 [-0.179, 1.824] |
| fold_4 | -0.005 [-0.341, 0.269] | 0.010 [-0.169, 0.154] |
| fold_5 | 0.220 [-0.191, 0.789] | 0.160 [-0.027, 0.396] |

Fold 3 (2022-07-01..09-28, 2,112 hours / 88 days) is the stress period. Every contrast's per-fold intervals are in `uncertainty.csv` (scopes fold_1..fold_5).

## Coverage with width, stress period and peak

| Policy | cov50 | cov80 | cov95 | mean / median / p95 width95 | fold-3 MAE | peak MAE | peak cov95 |
|---|---|---|---|---|---|---|---|
| v5 = (2/3)·v4 + (1/3)·D | 0.483 | 0.785 | 0.937 | 101.9 / 69.4 / 303.9 | 48.94 | 49.94 | 0.939 |
| v4 (three-block) | 0.496 | 0.790 | 0.939 | 101.9 / 70.1 / 307.6 | 47.03 | 50.09 | 0.936 |
| v3+D (DDNN as v3's third member) | 0.487 | 0.787 | 0.939 | 103.6 / 70.3 / 311.4 | 48.20 | 47.96 | 0.949 |
| v3 | 0.494 | 0.791 | 0.938 | 106.2 / 73.0 / 322.8 | 48.04 | 47.52 | 0.939 |
| D (DDNN alone) | 0.441 | 0.743 | 0.925 | 109.2 / 54.3 / 332.7 | 58.84 | 56.00 | 0.949 |
| A1 normalized LEAR | 0.503 | 0.788 | 0.942 | 134.3 / 94.4 / 372.6 | 51.21 | 49.88 | 0.926 |
| B2 daily LEAR | 0.476 | 0.772 | 0.930 | 118.9 / 88.1 / 355.0 | 54.01 | 57.62 | 0.892 |
| B0 naive | 0.462 | 0.752 | 0.907 | 166.6 / 136.9 / 462.1 | 86.95 | 64.19 | 0.941 |
| B1 (v1) | 0.364 | 0.628 | 0.845 | 130.9 / 97.9 / 387.5 | 140.99 | 275.26 | 0.194 |
| B3 daily LightGBM | 0.466 | 0.767 | 0.926 | 131.0 / 94.9 / 390.6 | 70.62 | 75.20 | 0.890 |

The 17-day peak (2022-08-15..31, 408 hours) is descriptive only: a small effective sample.

## All six original §8 diagnostics, every new policy

| Policy | Criteria not met (criterion: scope metric) |
|---|---|
| v5 = (2/3)·v4 + (1/3)·D | none — all met |
| v3+D (DDNN as v3's third member) | none — all met |
| D (DDNN alone) | 1: equal_fold S_MAE, 5: fold_3 MAE |
| v3 | none — all met |
| v4 (three-block) | none — all met |

The rows, with actual values and limits, are in `criteria.csv`. The emitted p50 is scored; for v5 and v3+D it is the central forecast plus the H layer's median residual, kept separate from the central forecast. For D the p50 is the ensemble median, which is D's central forecast by definition.

## §21.5 diagnostics (descriptive; they choose nothing)

**DDNN's own calibration** (D, pooled; `diagnostics/calibration-by-level.csv`, `diagnostics/pit-histogram.csv`):

| Nominal level | 0.025 | 0.1 | 0.25 | 0.5 | 0.75 | 0.9 | 0.975 |
|---|---|---|---|---|---|---|---|
| Share of actuals at or below | 0.040 | 0.123 | 0.261 | 0.477 | 0.702 | 0.866 | 0.966 |

Central coverage: 50% 0.441, 80% 0.743, 95% 0.925 (mean 95% width 109.2 EUR/MWh). PIT of the quantile-averaged ensemble: mean 0.514, share below 0.05 0.072, share above 0.95 0.070 (uniform = 0.05 each).

**Extrapolation** (`diagnostics/extrapolation.csv`, beside CP-22's tree record): 26 extreme or top-5% days (1 exceeds window max, 7 exceeds window max and top 5pct daily max, 18 top 5pct daily max). Hours forecast above the origin's training-window maximum on those days: D (DDNN alone) 0, v3 1, v4 (three-block) 0, v3+D (DDNN as v3's third member) 0, v5 = (2/3)·v4 + (1/3)·D 0.

**The 2022 peak and fold 4** (`diagnostics/peak-and-fold4.csv`, `diagnostics/fold4-intervals.csv`); fold 4 is the fold where CP-22's candidates were decisively worse than v4.

**Ensemble and seed stability** (`diagnostics/seed-stability.csv`, `diagnostics/epochs.csv`): the ensemble median's pooled MAE is 21.20 EUR/MWh; the single seeds' medians score 42 22.12, 43 21.78, 44 22.91, 45 22.32; the four member medians spread 6.90 EUR/MWh around the ensemble median on average and straddle the actual price in 30.7% of hours.

**The configuration chosen in each fold:** as above (`selection.json`).

## Fit cost and daily cycle (diagnostic, §17.5 D3)

2,624 main-run DDNN member fits (origin 2,544, selection 80), 1.30 single-thread hours in total; median four-seed ensemble per origin 6.5 s (maximum 14.4 s). By configuration: C1 20 fits, median 0.70 s, median best epoch 14; C2 1028 fits, median 0.84 s, median best epoch 5; C3 540 fits, median 1.58 s, median best epoch 6; C4 1036 fits, median 2.67 s, median best epoch 3.

Cold daily cycle of v5 (DDNN members, ensemble, v5 central, H layer, issuance; four workers): median 11.6 s, maximum 38.9 s over 25 origins; every bitwise check passed. v4's own component cycle, measured by CP-21 and not refitted here: median 24.7 s, maximum 69.4 s over 25 origins.

## Integrity

- Controls (`controls.json`): 61 checks, all passed: True. They include delivery-day and future masking (exactly 0.0), the non-uniform D−1 price mutation (moves), future weather (0.0), weather permutation and rearrangement (move), early stopping responding to inner-validation outcomes, the configuration choice unchanged by evaluation outcomes and changed in its losses by holdout outcomes, determinism (a fresh process refits the main run's members bit for bit), restart replay, release and cache refusals, composite parity on every key, and the boundary guard.
- v3 and v4 through CP-23's H-layer replay path reproduce the committed vectors bit for bit on all 10,747 keys: v3 True, v4 True (`parity.json`).
- Independent representative HG and v4 slice, refitted at two origins (`reproduction.json`): bitwise True.
- Scoring reproduces CP-20's and CP-21's committed §8 rows and v4 − v3 intervals: True.
- PyTorch reference (`reference-checks.json`): 26 passed, 1 warning in 4.01s, torch 2.14.1, at the frozen tolerances; the largest error was a small fraction of its bound.

## Resources against the §21.8 ceilings

| Dimension | Used | Cap |
|---|---|---|
| active_seconds | 13267.41 | 144000 |
| additional_disk_bytes | 41816724 | 10737418240 |
| analysis_passes | 1 | 3 |
| data_download_bytes | 0 | 0 |
| ddnn_fits | 2844 | 6000 |
| machine_seconds | 7975.85 | 216000 |
| main_ddnn_fits | 2624 | 4000 |
| policy_days | 3279 | 8000 |
| reference_passes | 1 | 3 |
| remote_writes | 0 | 0 |
| rss_bytes | 3429498880 | 10737418240 |
| workers | 4 | 4 |

all CP-23 work ran on Sunday 2026-10-04 (Asia/Jerusalem); no job ran in or into the Friday 00:00 - Sunday 00:00 window, and every job checked the window before it started

## What this result does not establish

- No confirmatory or out-of-sample claim: development_post_selection on folds already used by CP-15, CP-20, CP-21 and CP-22.
- "No demonstrated joint preference" is not equivalence, and not proof that DDNN cannot help.
- One DDNN design was tested: one architecture family, four configurations, four seeds, a fixed one-third weight. Learned weights belong to 4.8.
- No release, final-product designation, freeze, Live or economic claim; v1 remains the released product.

Reproduction: `reports/distribution-challenger/reproduce.md`. Protocol: `reports/distribution-challenger/protocol.json` (committed before any main-run fit).

