# CP-24 — S1 report after pre-fold round 1

- **From:** the CP-24 Engineering Lead. **To:** the Orchestrator, at steering point S1 (capstone v21-r11 §23.6).
- **Time:** 2026-10-05, 11:30 IDT. **Round:** 1 of at most 3 before attempt 1. **Attempt:** none has run.
- **Candidate commit holding this round's evidence:** `645dc92` on `gauntlet/cp-24` (the round's design was committed
  before its search, at `e51ff2a`; its search ledger and ensembles before its gate, at `0a423fb`).
- **What this report carries.** Pre-fold evidence only: the search on validation batches before each fold's
  D0 − 56, and the gate on the 280 days of [D0 − 56, D0). No DDNN-2 or new-policy fit has been made at a warm-up or
  evaluation origin, and no warm-up or evaluation outcome appears here.

## 1. Where CP-24 stands

| Step | Result | Evidence |
|---|---|---|
| Starting state and inputs (item 1–2) | Verified: 112 identities (CP-23's from `evidence/cp-23` objects), the 638-origin manifest and 10,747 keys, saved vectors bitwise consistent, weather regenerated bit for bit, the coverage gap exactly 2022-09-29..2023-03-24 | `reports/ddnn2/preflight/` |
| v4 slice and gate code path | Bitwise parity at 11 covered origins (wrapper included); the unwrapped code refuses a fold-4 gate day | `reports/ddnn2/v4-parity.json` |
| 4.6L′ (item 3) | PASS | `reports/ddnn2/licence-admission.md` |
| §23.7 checks (item 4) | Import audit and 22 finite-difference checks pass; PyTorch reference 32 of 32, tolerances frozen before the first run | `reports/ddnn2/reference-checks.json` |
| 4.6R′ (item 5) | PASS; 128 trials per fold per round; the maximal route fits every ceiling, also in the worst case | `reports/ddnn2/resource-admission.md` |
| Round 1 search (item 6) | 128 trials per fold, 3,464 trial-batch fits (2 failed, ranked last) | `reports/ddnn2/rounds/round-1/search-ledger.json` |
| Round 1 gate (item 6) | **PASS on all four conditions** | `reports/ddnn2/rounds/round-1/gate.json`, `report.md` |

## 2. The round-1 gate (§23.6), pooled over the 280 gate days

| Condition | Result | Values |
|---|---|---|
| G0 every forecast finite and ordered | met | DDNN-2 ensembles and v4's members on every gate day |
| G1 MAE(v5) ≤ MAE(v4) | met | 12.538 vs 12.849 EUR/MWh (−0.312, −2.4%) |
| G2 MAE(D2) ≤ 1.10 × MAE(L) | met | 11.362 vs 13.329 EUR/MWh, ratio 0.852 |
| G3 cap binds on < 0.1% of members' emitted hour-levels | met | 331 of 375,984 (0.088%) |

By fold (gate days only):

| Fold | Gate window | MAE v4 | MAE v5 | MAE D2 | MAE L | MAE HG | Cap share | corr(D2, HG) | corr(D2, L) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2020-03-30..05-24 | 4.871 | 4.859 | 4.284 | 4.511 | 5.497 | 0.326% | 0.889 | 0.927 |
| 2 | 2020-12-29..2021-02-22 | 6.299 | 6.104 | 5.060 | 6.130 | 6.875 | 0.009% | 0.804 | 0.854 |
| 3 | 2022-03-30..05-24 | 22.309 | 21.955 | 19.787 | 22.659 | 24.356 | 0.029% | 0.790 | 0.769 |
| 4 | 2025-01-25..03-21 | 14.527 | 13.821 | 13.174 | 17.405 | 14.361 | 0.004% | 0.840 | 0.782 |
| 5 | 2025-10-07..12-01 | 16.236 | 15.945 | 14.502 | 15.928 | 17.459 | 0.072% | 0.870 | 0.876 |
| pooled | 280 days, 6,714 hours | 12.849 | 12.538 | 11.362 | 13.329 | 13.710 | 0.088% | 0.826 | 0.806 |

- **Excluded training days (§23.6's coverage rule).** Fold 4's gate fits, DDNN-2's and v4's members alike, leave out
  the uncovered delivery days in their windows: 55 at most (the first gate day, 2025-01-25), fewer later. No other
  fold's gate fit excludes a day. Every search fit whose window reaches the gap excludes it (the ledger records the
  count per fit).
- **Reading.** A screen, not a claim: these are point estimates on pre-fold days. On them, v5 is no worse than v4 in
  any fold, and DDNN-2 alone is below L and below HG in every fold. DDNN-2's errors correlate 0.81 with L's and 0.83
  with HG's (CP-23's DDNN correlated 0.83 with L on its folds, per §23.2).
- **G3's margin is thin** (0.088% against 0.1%). Fold 1 carries most of it: its rank-2 member (two tanh layers of 447
  and 198, asinh-MAD target, pinball-only loss) has heavy outer tails, and the cap binds on 0.33% of fold 1's member
  hour-levels. The cap is §23.3's guard, every activation is recorded, and G3 is a gate condition, not a condition of
  `cp24-adoption`.

## 3. The search (§23.4)

- B = 3, 7, 11, 11, 11 validation batches; 128 trials per fold; successive halving to the best 43 on all batches
  (fold 1: all 128 ran all 3); 3,464 fits, of which 2 failed with a nonfinite loss at epoch 21 (fold 5) and rank last.
- **Each fold's ensemble** (the four best distinct configurations × two seeds; full table in the round report):

| Fold | Rank 1 | Rank 2 | Rank 3 | Rank 4 | Validation pinball, ranks 1–4 (EUR/MWh) |
|---|---|---|---|---|---|
| 1 | [26, 238] softplus, asinh-MAD, κ 1 | [447, 198] tanh, asinh-MAD, κ 0 | [18] softplus, asinh-§4, κ 1 | [107, 74] ELU, z-MAD, κ 0.5 | 1.333, 1.394, 1.413, 1.466 |
| 2 | [98] softplus, asinh-§4, κ 0 | [102, 423] ELU, asinh-§4, κ 0.5 | [30, 27] softplus, asinh-MAD, κ 0 | [127, 69] softplus, z-§4, κ 0 | 1.428, 1.432, 1.458, 1.472 |
| 3 | [23] softplus, z-§4, κ 0.5 | [143, 95] tanh, asinh-§4, κ 0 | [76, 17] softplus, z-§4, κ 0.5 | [41, 29] ELU, asinh-§4, κ 1 | 6.048, 6.193, 6.381, 6.500 |
| 4 | [161, 24] tanh, asinh-MAD, κ 0 | [181, 96] softplus, asinh-MAD, κ 0.5 | [344] softplus, asinh-MAD, κ 0 | [50] ELU, asinh-MAD, κ 0 | 5.006, 5.192, 5.321, 5.428 |
| 5 | [231] tanh, z-MAD, κ 0 | [304] softplus, z-MAD, κ 1 | [317] ELU, z-MAD, κ 0.5 | [480, 107] tanh, z-MAD, κ 0 | 5.126, 5.128, 5.153, 5.167 |

- All 20 chosen configurations include the GFS block; most include the origin price statistics. The space was not
  exhausted at an edge in a way that names an obvious change: widths, depths, activations, transforms and κ all vary
  among the winners.

## 4. Costs so far (§23.11)

| Ceiling | Used | Cap |
|---|---|---|
| DDNN-2 member fits | 5,725 (search 3,465, gate 2,240, 4.6R′ 18, correctness smoke 2) | 40,000 |
| v4-member gate pass | 280 origins, one pass, cached for any later round | 280 |
| Policy-days | 840 (the gate) | 12,000 |
| Rounds before attempt 1 | 1 | 3 |
| Machine-hours | 5.28 | 150 |
| Active hours | 1.94 (the 07:45–11:02 usage-limit gap is recorded as an idle pause) | 50 |
| Peak aggregate RSS / added disk | 2.85 GiB / 0.29 GiB | 10 / 10 GiB |
| Data downloaded, remote writes, cost | 0, 0, $0 | 0, 0, $0 |

Repairs and incidents are in `reports/ddnn2/defects-and-repairs.md`: the search ledger was written by a recorded
post-processing job after `job_search` failed on an infinite metric (no fit repeated); one fit was lost and refitted
at a worker change; the usage-limit gap.

## 5. Proposal

**Freeze round 1's design and run scored attempt 1.**

- The gate passed on all four conditions, and its point estimates are favourable in every fold. §23.6 allows a
  freeze only after a passing gate; this one passed.
- No pre-fold deficiency names a change within §23.3–§23.4. A second round chosen because of these gate windows would
  tune on the screen itself, and it costs a further 128 × 5 trials and 2,240 gate fits for no identified gain.
- G3's thin margin does not bear on the attempt: the cap keeps guarding every emitted quantile, every activation is
  reported (condition 3), and G3 is not re-applied.
- **Projection for attempt 1, against the remaining ceilings with the review reserve:** 636 origins × 8 members =
  5,088 member fits (about 3 machine-hours at the gate's measured 2.2 s per member fit, under an hour of wall time on
  four workers), 1,914 policy-days for the replays, one reference pass and one bootstrap pass for scoring, then the
  controls, the diagnostics and the cold daily cycle. Totals after attempt 1, before review: about 11,300 fits of
  40,000 and about 12 machine-hours of 150. The maximal remaining route (S2, one round and attempt 2) also fits.

**The answers §23.6 allows,** for the record:

1. **Freeze** round 1's design (proposed). I then commit your answer verbatim under `steering/`, freeze attempt 1's
   protocol (it records round 1's design, ensembles, gate dates, excluded days and results), commit it, and only then
   start attempt 1's warm-up fits.
2. **Another round,** with changes you name within §23.3–§23.4, on pre-fold evidence only. Round 2 would rerun the
   search for every fold and the gate (v4's cached members are reused).
3. **Stop.** CP-24 would end as "stopped at the pre-fold gate", with no fold look.

A raise of a §23.11 ceiling is not needed at this point.
