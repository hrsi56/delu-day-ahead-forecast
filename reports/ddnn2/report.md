# CP-24 — DDNN-2: a literature-faithful DDNN, and v5 = v4 plus a DDNN-2 member

`capstone_v21.md` v21-r11 §23 · evidence class **development_post_selection** · population `common-10747h` (10,747 keys, five folds) · the second DDNN decision on these folds (4.7T carries the protection).

## Verdicts

| Status | Result |
|---|---|
| Engineering | Bound to the fresh Integration-Critic verdict on the final candidate (`docs/track-b/evidence/cp-24/integration.md`) |
| Entry | 4.6L′ PASS · §23.7: import audit, finite-difference checks, PyTorch reference 32 of 32 · 4.6R′ **PASS** (128 trials per fold per round) |
| Pre-fold round 1 | gate **PASS** (`rounds/round-1/gate.json`, `rounds/round-1/report.md`) |
| `cp24-adoption`, attempt 1 | **v5 is adopted in research as v5 ("v5 · DDNN-2 member added", predecessor v4)** · first unmet condition **None** (unmet: none) |
| CP-24's outcome | **v5 adopted in research in scored attempt 1** |
| Research | Development finding under the rule pre-registered on 2026-10-05; DDNN-2 vectors stored for 4.8 |
| Product | v1 remains the released product and the demo; no designation, freeze or Live follows (§16) |

## DDNN-2 as designed (§23.3–§23.4)

- **Round 1 design** (`rounds/round-1/design.json`): 128 trials per fold; changes from the previous round: none.
- **Emission:** the day's feature-valid keys; on a 25-hour day both keys of the repeated hour take that slot's forecast.
- **Ensemble:** four best distinct configurations x two seeds; per-level median of the eight members' EUR/MWh quantiles (mean of the two middle values); p50 = central = D2.
- **Guards:** winsorisation of continuous inputs at the training rows' (0.005, 0.995) quantiles; the cap at +-1.25 x max|z| on the member's training rows (before any asinh); sorting of crossings; every activation counted.
- **Head:** xi = o1, lambda = softplus(o2) + 1e-3, gamma = o3, delta = softplus(o4) + 0.05, per local-hour slot.
- **Held out weeks:** the member's seeded random 20% (rounded, at least one) of the whole Monday-Sunday weeks inside [window start, D-7); PCG64(SeedSequence([seed, 0x5EED])).
- **Loss:** first 20 epochs NLL only; then kappa*NLL + (1-kappa)*mean pinball over the 19-level grid [0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.975]; + l1*sum|W| + l2*sum W^2 over weight matrices; present slots only; rows weighted by recency (mean 1).
- **Minimum rows:** {'held_out_days': 14, 'training_days': 250}.
- **Optimizer:** Adam {'beta1': 0.9, 'beta2': 0.999, 'eps': 1e-08} in PyTorch's update order; Glorot-uniform init, zero biases, output biases at lambda = delta = 1.
- **Stopping:** mean pinball over the seven scored levels in EUR/MWh after inversion and the cap, on the held-out weeks, after every epoch from 21; patience 50; maximum 1000 epochs; best epoch kept (strict improvement); a nonfinite loss stops training and keeps the best epoch (recorded).
- **Window:** [max(2019-01-01, D-728), D) day rows with an eligible target slot and finite origin statistics; pre-fold fits leave out every delivery day without a frozen weather record (§23.6).

## The pre-fold rounds

| Round | G0 | G1 MAE v5 / v4 | G2 D2 / L | G3 cap share | Gate |
|---|---|---|---|---|---|
| 1 | True | 12.538 / 12.849 | 0.8525 | 0.088% | PASS |

v4's gate code path: bit-for-bit parity at 11 covered origins and the unwrapped code's refusal of a fold-4 gate day (`v4-parity.json`).

## Scored attempt 1

Frozen protocol `attempt-1/protocol.json`; vectors `attempt-1/predictions.parquet`, `attempt-1/members.parquet`; tables `metrics.csv`, `uncertainty.csv`, `criteria.csv`.

### Scores (equal-fold ratios to B0; lower is better)

| Policy | S_MAE | S_WIS | pooled MAE | pooled WIS | pooled 95% coverage | mean 95% width | §8 |
|---|---|---|---|---|---|---|---|
| v5 = (2/3)·HG + (1/6)·L + (1/6)·D2 | 0.5223 | 0.4937 | 17.05 | 9.98 | 0.940 | 100.25 | met |
| v4 (three-block) | 0.5357 | 0.5056 | 17.55 | 10.24 | 0.939 | 101.92 | met |
| v3 + DDNN-2 | 0.5156 | 0.4874 | 16.78 | 9.83 | 0.939 | 99.32 | met |
| v3 | 0.5658 | 0.5322 | 18.26 | 10.67 | 0.938 | 106.24 | met |
| DDNN-2 alone | 0.4785 | 0.4271 | 15.78 | 8.82 | 0.954 | 83.70 | met |
| CP-23's DDNN (saved) | 0.6319 | 0.5706 | 21.20 | 11.85 | 0.925 | 109.18 | saved reference |
| v3 + CP-23's DDNN (saved) | 0.5514 | 0.5211 | 18.01 | 10.50 | 0.939 | 103.64 | saved reference |
| A1 normalized LEAR | 0.6723 | 0.6460 | 20.71 | 12.45 | 0.942 | 134.33 | saved reference |
| B2 daily LEAR | 0.6578 | 0.6390 | 20.98 | 12.66 | 0.930 | 118.86 | saved reference |
| B0 naive | 1.0000 | 1.0000 | 32.81 | 20.02 | 0.907 | 166.60 | saved reference |
| B1 (v1) | 1.0518 | 0.9856 | 41.74 | 25.25 | 0.845 | 130.86 | saved reference |
| B3 daily LightGBM | 0.7841 | 0.7399 | 26.32 | 15.17 | 0.926 | 130.98 | saved reference |
| L = mean(L-N, L-R), point only | 0.5497 | n/a | 18.68 | n/a | n/a | n/a | n/a |

### `cp24-adoption` (§23.9), condition by condition

1. Joint improvement over v4, at the attempts-adjusted level: on the paired v5 - v4 differences, two-sided 97.5% intervals (the 1.25% and 98.75% percentiles of the shared replicates); the upper endpoint of dS_WIS is < 0 and the upper endpoint of dS_MAE is <= 0. → **met**.
2. No regression: v5 meets all six original section-8 diagnostics. → **met**.
3. A complete, valid evaluation: Engineering PASS with a fresh binding Integration verdict; all 10,747 keys issued with finite, ordered quantiles; every guard activation reported. → **met**.
4. No resolved per-fold degradation: no fold has a 95% paired daily-loss interval (v5 - v4) lying entirely above zero, in MAE or in WIS. → **met**.
5. A practical size: both point estimates improve v4's score by at least 0.5%: dS_MAE <= -0.005 x S_MAE(v4) and dS_WIS <= -0.005 x S_WIS(v4). → **met**.

**Decision:** v5 is adopted in research as v5 ("v5 · DDNN-2 member added", predecessor v4).

### Every §23.8 contrast, with its reading

| Contrast | Role | dS_MAE [95%] [97.5%] | dS_WIS [95%] [97.5%] | ratio S_MAE | ratio S_WIS | Reading |
|---|---|---|---|---|---|---|
| D2-D | ddnn2_vs_cp23_ddnn | -0.1534 [-0.1795, -0.1242] [-0.1842, -0.1196] | -0.1436 [-0.1686, -0.1107] [-0.1714, -0.1067] | -24.27% | -25.16% | observed joint improvement |
| D2-HG | ddnn2_alone_vs_lear | -0.0872 [-0.1107, -0.0662] [-0.1136, -0.0641] | -0.1052 [-0.1272, -0.0845] [-0.1299, -0.0809] | -15.42% | -19.76% | observed joint improvement |
| D2-HGL | ddnn2_alone_vs_v4 | -0.0571 [-0.0786, -0.0388] [-0.0811, -0.0360] | -0.0785 [-0.0982, -0.0608] [-0.1013, -0.0588] | -10.67% | -15.53% | observed joint improvement |
| D2-L | ddnn2_alone_vs_same_information_twin_point_only | -0.0712 [-0.0910, -0.0545] [-0.0933, -0.0521] | not defined | -12.94% | n/a | MAE only (L has no interval forecast): lower (better) |
| HGL-HG | lightgbm_as_v3_third_member_beside | -0.0301 [-0.0368, -0.0228] [-0.0379, -0.0217] | -0.0266 [-0.0327, -0.0204] [-0.0336, -0.0197] | -5.32% | -5.01% | observed joint improvement |
| v3+D-HGL | cp23_ddnn_in_lightgbms_place_beside | 0.0157 [0.0081, 0.0232] [0.0069, 0.0241] | 0.0155 [0.0074, 0.0222] [0.0061, 0.0236] | +2.93% | +3.08% | observed joint worsening |
| v3+D2-HG | ddnn2_as_v3_third_member | -0.0501 [-0.0563, -0.0425] [-0.0573, -0.0415] | -0.0448 [-0.0502, -0.0383] [-0.0512, -0.0374] | -8.86% | -8.41% | observed joint improvement |
| v3+D2-HGL | ddnn2_in_lightgbms_place | -0.0200 [-0.0257, -0.0130] [-0.0266, -0.0122] | -0.0181 [-0.0233, -0.0118] [-0.0240, -0.0110] | -3.74% | -3.59% | observed joint improvement |
| v5-HG | reference_vs_v3 | -0.0434 [-0.0491, -0.0366] [-0.0501, -0.0358] | -0.0386 [-0.0437, -0.0326] [-0.0445, -0.0319] | -7.68% | -7.24% | observed joint improvement |
| v5-HGL | adoption_decision | -0.0133 [-0.0161, -0.0096] [-0.0166, -0.0091] | -0.0119 [-0.0143, -0.0087] [-0.0147, -0.0084] | -2.49% | -2.36% | observed joint improvement |
| v5-v3+D2 | lightgbm_still_adds_given_ddnn2 | 0.0067 [0.0033, 0.0097] [0.0028, 0.0100] | 0.0062 [0.0031, 0.0089] [0.0026, 0.0094] | +1.30% | +1.28% | observed joint worsening |

### Diagnostics (descriptive; `attempt-1/diagnostics/`)

- D2's calibration (pooled): 50/80/95% coverage 0.484 / 0.794 / 0.954; PIT below 0.05 0.051, above 0.95 0.045.
- Pooled error correlations: A1~B2 0.768, A1~L 0.744, B2~L 0.735, D2~A1 0.834, D2~B2 0.724, D2~D 0.786, D2~HG 0.826, D2~L 0.803, D~A1 0.703, D~B2 0.627, D~HG 0.706, D~L 0.829, HG~A1 0.935, HG~B2 0.945, HG~L 0.786.
- Guards: 583 capped slot-levels, 12,972 winsorised forecast inputs, 0 crossings restored, 0 nonfinite-loss stops, over 5,088 member fits.
- Guards by fold (every attempt fit; the cap's share of the members' emitted hour-levels, the gate's G3 measure and never a condition, beside the round's gate share; `diagnostics/guards-by-fold.csv`, `diagnostics/guards-by-member.csv`): fold_1 0.103% (gate 0.326%), 35 of 1,016 member fits capped; fold_2 0.132% (gate 0.009%), 40 of 1,016 member fits capped; fold_3 0.030% (gate 0.029%), 19 of 1,000 member fits capped; fold_4 0.010% (gate 0.004%), 8 of 1,040 member fits capped; fold_5 0.067% (gate 0.072%), 23 of 1,016 member fits capped; pooled 0.068% (gate 0.088%), 125 of 5,088 member fits capped.
- Extrapolation: 26 extreme or top-5% days; hours above the window maximum D 0, D2 1, HG 1, HGL 0, v3+D2 1, v5 0.
- Shape blend (descriptive, never eligible): shape-blend WIS 9.86, 95% coverage 0.950; HGL WIS 10.24, 95% coverage 0.939; D2 WIS 8.82, 95% coverage 0.954.
- Also: MAE by local hour, member stability, the 2022 peak, folds 3 and 4, the search beside the folds (`attempt-1/diagnostics/*.csv`); fit cost and the cold daily cycle (`fit-cost.json`, `daily-cycle.json`).

## Resources (§23.11; at the candidate, before the review)

| Ceiling | Cap | Used |
|---|---|---|
| ddnn2_fits | 40000 | 11044 |
| v4_gate_origins | 280 | 280 |
| policy_days | 12000 | 2843 |
| reference_passes | 3 | 1 |
| bootstrap_passes | 6 | 1 |
| scored_attempts | 2 | 1 |
| rounds_before_attempt_1 | 3 | 1 |
| rounds_before_attempt_2 | 1 | 0 |
| machine_hours | 150 | 10.10 |
| active_hours | 50 | 4.00 |
| rss_bytes (GiB) | 10 | 2.85 |
| additional_disk_bytes (GiB) | 10 | 0.67 |
| workers | 4 | 4 |
| data_download_bytes | 0 | 0 |
| remote_writes | 0 | 0 |

Raises (§23.6): none. Calendar: no job ran in or into the Friday 00:00 – Sunday 00:00 window (Asia/Jerusalem); every job checked it before starting.

## Reproduction

See [`reproduce.md`](reproduce.md).

