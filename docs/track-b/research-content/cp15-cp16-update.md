# CP-15 / CP-16 research update: development evidence, post-selection

**2026-09-23 · Local content draft for the Owner. Not published and not staged.**
This serves programme [4.3R/4.3C](../v3-plan-handoff-2026-09-22.md#work-4-3r) and
[§6 local handoff](../v3-plan-handoff-2026-09-22.md#section-6). Every number here is copied from a saved
file and rounded for display. Nothing was recalculated. Each claim is traced in the
[claim-to-evidence map](cp15-cp16-claims.md), which also lists gaps and withheld claims.

> **Evidence class.** Every CP-15 and CP-16 result reused here is **`development_post_selection`**.
> All comparisons and intervals are exploratory. There are no confirmatory, family-wise or
> product claims.

## Status at a glance

| | CP-15 (capstone v21-r1) | CP-16 (capstone v21-r3) |
|---|---|---|
| Engineering | **Integration PASS** at candidate `fc4aee038cf898998a292506df62ddb0dcfaf22a` ([verdict](../evidence/cp-15/integration.md)) | **Integration PASS** at candidate `bf3ca602e32e99e45c7835e3f95148f62b608099` ([verdict](../evidence/cp-16/integration.md), [accepted receipt](../cp-16-pass-receipt-2026-09-23.md)) |
| Product status | `product_feasibility = NOT_DEMONSTRATED`. Best observed challenger A1. Qualified policy: none. | CP-15 status unchanged. The original-§8 diagnostic is `not_met` for both V2-H and V2-P. Delivery is not authorized. |
| Research conclusion | A1 is best among the challengers. Reference B2 has better primary equal-fold scores. | H−P: **no demonstrated joint preference**. H−B2 meets the exploratory joint-improvement rule. P−B2 does not. |
| Historical retrieval | `evidence/cp-15` → `1bdc75b8ab943092bb8de6ba893defb9e12250d8` | `evidence/cp-16` → `5ec8a92a4032569b31a1a4f0bb3c512793d15a78` ([landing map](../cp-16-landing-2026-09-23.md)) |

An Engineering PASS shows that the experiment was completed and valid. It does **not** qualify
a product. Both candidate reports ([CP-15](../../../reports/cp15/report.md), [CP-16](../../../reports/v2-causal/report.md))
still say "pending Integration" in their headers, because they were written before the final
review. Completion is taken from the verdicts and the receipt above. The historical reports
are left unchanged.

## What was compared

- **Population.** Both checkpoints use the same **10,747** original eligible target hours in five
  90-calendar-day folds. The fold counts are 2,160 / 2,159 / 2,112 / 2,160 / 2,156. The folds
  start on 2020-07-01, 2021-04-01, 2022-07-01, 2025-05-01 and 2026-01-08.
  - Full fold 3 (the 2022 crisis) has **2,112 hours on 88 represented dates**.
  - The separate peak slice runs from 2022-08-15 to 2022-08-31: **408 hours, 17 days**.
  - The two denominators are never interchanged.
  - Inputs start no earlier than **2019-01-01**. Forecasts are issued at D−1 11:00 UTC.
    Errors are released for use only from D−2 onward.
- **CP-15 (nine policies).** All reference and challenger forecasts are saved.
  - References: B0 (similar-day naive), B1 (preserved v1 vectors, exact replay), B2 (rolling
    LEAR, raw target) and B3 (rolling LightGBM, raw target).
  - Challengers: A1 (B2 with 168-hour target normalization), A2 (normalized B3), A3 and A5
    (means of normalized components) and A4 (84-day normalized LEAR).
- **CP-16 (two new policies).** Both use the same 50/50 blend of genuine issued A1 and B2
  **central** forecasts. Both use the same causal buffer of standardized errors from the latest
  28 complete released days.
  - **V2-H** shrinks local-hour residual quantiles toward the pooled quantiles, with weight
    n/(n+56) and a pooled fallback below 14 days.
  - **V2-P** uses the pooled quantiles only.
  - Hour-aware pooling is the only difference between H and P.
  - B0, B1, B2, B3 and A1 were re-scored from saved vectors. There were no new reference fits.

## How the scores are defined

| Score | Definition ([capstone](../../../capstone_v21.md) §7 and §14.3) | Role |
|---|---|---|
| **S_MAE, S_WIS** | Mean of the five per-fold ratios to B0, with equal weight per fold. MAE uses the emitted p50. WIS uses seven quantiles, interval weights alpha/2, median weight 1/2 and divisor 3.5. | **Primary** |
| Pooled MAE, WIS | Weighted by observations over all 10,747 hours, in EUR/MWh | Secondary description only |
| Native v1 pinball | v1's original nine-quantile pinball score, kept in the historical v1 records | Historical. It is **not** this WIS, and it is not quoted here. |

Original §8 product criteria are applied without change:

1. S_MAE ≤ 0.90 × the best of B0–B3 (limit **0.59203**).
2. S_WIS ≤ 0.90 × the best of B0–B3 (limit **0.57509**).
3. 95% coverage is between 0.90 and 0.98 in every fold.
4. On the peak, 95% coverage is at least 0.90, and MAE and WIS are no worse than the best of
   B0–B3.
5. In every fold, MAE and WIS are each ≤ 1.05 × the best rolling B2/B3 value.
6. Every forecast is complete, finite and ordered.

## Score table

S-scores are ratios to B0 (lower is better). The other columns are in EUR/MWh, except the last.
A2–A5 exist only in CP-15. They were not re-scored in CP-16.

| Policy | Source | S_MAE | S_WIS | Pooled MAE | Pooled WIS | Fold-3 MAE | Peak 95% hits / 408 |
|---|---|---:|---:|---:|---:|---:|---:|
| B0 naive | reference | 1.00000 | 1.00000 | 32.81010 | 20.02060 | 86.94887 | 384 |
| B1 v1 replay | reference | 1.05185 | 0.98564 | 41.74348 | 25.24793 | 140.99285 | 79 |
| B2 rolling LEAR | reference | 0.65781 | 0.63899 | 20.98425 | 12.66232 | 54.00782 | 364 |
| B3 rolling LightGBM | reference | 0.78414 | 0.73991 | 26.32393 | 15.16769 | 70.61552 | 363 |
| A1 | CP-15 | 0.67229 | 0.64602 | 20.70749 | 12.44968 | 51.21276 | 378 |
| A2 | CP-15 | 0.77371 | 0.73167 | 25.39572 | 14.77128 | 66.44564 | 387 |
| A3 | CP-15 | 0.67251 | 0.64719 | 21.43859 | 12.76011 | 54.55453 | 381 |
| A4 | CP-15 | 0.76466 | 0.73342 | 24.21680 | 14.40719 | 62.21004 | 370 |
| A5 | CP-15 | 0.67378 | 0.64871 | 21.50099 | 12.80930 | 55.11483 | 379 |
| V2-H | CP-16 | 0.64407 | 0.61603 | 20.23104 | 12.04646 | 51.21362 | 377 |
| V2-P | CP-16 | 0.64577 | 0.62872 | 20.24313 | 12.26111 | 51.05393 | 377 |

The peak slice covers only 17 days, so its hit counts are descriptive only. They are not
a claim of statistical significance at the level of individual hours.

## CP-15: best challenger, no qualified policy

- **A1 ranks first among the challengers.** The order is A1, A3, A5, A4, A2. The reference
  **B2 still has better primary equal-fold scores**: 0.65781 / 0.63899 against A1's
  0.67229 / 0.64602.
  - A1's pooled MAE and WIS are lower than B2's (20.70749 / 12.44968 against
    20.98425 / 12.66232).
  - So the two weightings disagree. The registered equal-fold weighting decides, and it keeps
    the crisis fold from being diluted.
- **Crisis improvement against v1.**
  - On full fold 3, A1's MAE is **51.21276**, against **140.99285** for the v1 replay
    ([programme plan §2](../v3-plan-handoff-2026-09-22.md#section-2) summarizes this as ~64%).
    B2's is 54.00782.
  - On the 17-day peak, A1's 95% intervals contain **378/408** outcomes, against v1's
    **79/408**.
  - These are development observations after selection. They are not a product claim.
- **`product_feasibility = NOT_DEMONSTRATED`.** A1 fails original criteria **1, 2 and 5**.
  - Criteria 1 and 2 fail on the equal-fold limits: 0.67229 > 0.59203 and 0.64602 > 0.57509.
  - Criterion 5 fails only on **fold-1 MAE: 6.81990 > 6.53023**. A1's MAE passes in the other
    four folds, and **its WIS passes criterion 5 in every fold**.
  - A1 meets criteria 3, 4 and 6.
  - No CP-15 challenger qualifies.

## CP-16: hour-aware against pooled intervals on a common blend

- **Descriptive ranking.** H ranks ahead of P on S_WIS (0.61603 against 0.62872) and on S_MAE
  (0.64407 against 0.64577). This ranking does not make H a statistically supported winner,
  and it is not a delivery decision.
- **Primary contrast H−P: "no demonstrated joint preference".** This is the only contrast
  that measures the added effect of hour awareness.
  - ΔS_WIS is **−0.0126918**, with 95% interval [−0.0155712, −0.0109119]. This interval lies
    wholly below zero, so the WIS evidence supports an improvement.
  - ΔS_MAE is **−0.0016954**, with interval [−0.0036237, **+0.000003857628092332211**]. The upper
    endpoint is positive, not zero.
  - The frozen rule needs the WIS upper endpoint < 0 **and** the MAE upper endpoint ≤ 0.
    The MAE endpoint fails that test, so the rule is not met.
  - This result shows neither equivalence nor absence of benefit or harm.
- **Secondary contrasts against B2.**
  - **H−B2 meets the exploratory joint-improvement rule.** ΔS_MAE is −0.0137388
    [−0.0235719, −0.0053442]. ΔS_WIS is −0.0229611 [−0.0336965, −0.0118099].
  - **P−B2 does not.** Its ΔS_MAE interval, −0.0120433 [−0.0212870, −0.0035563], lies below
    zero. Its ΔS_WIS, −0.0102693, has an interval [−0.0200602, **+0.0006704**] that spans zero.
- **Original §8 diagnostic.** H and P both **fail criteria 1–2** (S_MAE 0.64407 / 0.64577 against
  a limit of 0.59203; S_WIS 0.61603 / 0.62872 against a limit of 0.57509). Both **meet
  criteria 3–6**.
- **The criterion-5 change is not credited to hour-aware intervals.**
  - A1 failed criterion 5 on fold-1 MAE. H and P both pass criterion 5 in every fold, for MAE
    and WIS alike. Their fold-1 MAE is 6.31080 and 6.34197, against a limit of 6.53023.
  - P has no hour awareness, so the shared criterion-5 transition cannot be attributed
    uniquely to hour awareness. The incremental hour-aware effect is the H−P contrast.
  - The shared A1/B2 central blend and the shared causal residual construction are plausible
    contributors. No arm in the experiment isolates the blend alone.

**Mixed outcomes, kept as recorded (descriptive):**

- **H against P, fold by fold.**
  - H has lower WIS in all five folds.
  - H has lower MAE in folds 1, 4 and 5. It has *higher* MAE in fold 2 (9.45709 against
    9.44352) and fold 3 (51.21362 against 51.05393).
  - The per-fold paired intervals are descriptive only.
- **Fold 1.** B2 keeps a lower fold-1 MAE (6.21927) than either H or P.
- **Crisis.**
  - On full fold 3, MAE is almost the same for A1 (51.21276), H (51.21362) and P (51.05393).
  - On the 17-day peak, A1 has lower MAE and WIS (49.87670 / 29.40371) than H (52.50980 /
    30.10205) or P (52.65780 / 30.85481). The 95% hit counts are A1 378, H 377 and P 377.
- **Central blend against emitted p50.**
  - H and P share the same central blend, with a pooled central MAE of 19.99979.
  - Each layer's residual-median shift raises the pooled emitted-p50 MAE, to 20.23104 for H and
    20.24313 for P.
  - The contract scores the emitted p50. This observation is not grounds for choosing another
    construction.
- **Interval width.** H's lower WIS comes with narrower pooled mean 95% width (124.63573 against
  133.96917 EUR/MWh) and pooled 95% coverage of 0.93887 against 0.94222.

## Preserved history and limitations

- **Earlier failures are preserved.**
  - CP-15 attempt 1 keeps its FAIL: candidate `f8d0ed2a5f0737f0d088c3474b5a9fe77a406f37`, evidence
    tip `193d9cf48c586b9c4b1f43d7a5677b2d5f400832`.
  - CP-16's first attempt (v21-r2) was **BLOCKED**, with an independent Integration **FAIL**
    ([receipt](../cp-16-blocked-receipt-2026-09-23.md)): candidate
    `3a160fd33ed92bb0061144cfbce2323d8b3a7db9`, evidence tip
    `41b0e6d222a3d65d474ac5974c6eb7017db317e8`.
  - That attempt produced no outer scores and supports no research conclusion.
- **Historical monitoring limits.**
  - During the interrupted CP-16 admission, peak memory (RSS) while the monitor was down is
    unknown.
  - Earlier Builder BLAS/concurrency assertions were unsupported.
  - Later monitoring does not prove past compliance, and nothing is certified retroactively.
  - The 3,730 policy-day debit stands.
- **Regeneration disclosure.**
  - The required admission, component and residual-state evidence was regenerated under
    repaired monitoring and verified afresh ([notice](../evidence/cp-16/resumption-notice.md)).
  - The repairs did not change the scientific recipe.
  - An oracle fixture bug was caught, and its failed run (126 pass / 1 fail) is retained.
- **v1 history is unchanged and not re-verified here.**
  - v1 development point-MAE: p=0.948, statistic +1.6228, median 28.58% worse.
  - Original v1 peak coverage: 79/408.
  - CP-10: peak 131/408 and full fold 1,515/2,112.
  - v1 stays the historical fallback. Native v1 pinball is not renamed as WIS.
- **Data assumptions.**
  - Historical availability of the A65 load-forecast vintages, and historical data revisions,
    are inherited assumptions. They are not proven for every issue vintage.
  - The 2019 input floor holds throughout.
- **Statistical limits.**
  - The peak (17 days) is descriptive.
  - The 56-date support rule for hour and block results is a reporting convention, not a power
    calculation.
  - Twenty-eight errors per hour give no guarantee on the nominal tails.
  - Residual intervals are empirical benchmarks. They carry no conformal coverage guarantee.
- **Economics.**
  - CP-15 and CP-16 computed no economic value, and CP-16 excluded economics by contract.
  - Historical battery sensitivities in [plan §5.6](../v3-plan-handoff-2026-09-22.md#section-5) are a
    separate descriptive review sample (444 complete days). They are not restated or extended
    here.
  - This update introduces no threshold.
- **Out of scope.** Nothing here promotes a product, selects a live policy, freezes CP-17,
  starts a prospective clock, gives new confirmation, or publishes anything.
- **Data notice.** ENTSO-E Transparency Platform; Bundesnetzagentur | SMARD.de. Licensed CC BY 4.0.
  [`DATA-LICENSE.md`](../../../DATA-LICENSE.md) controls.

## Reproduction

The existing instructions are [CP-15 reproduction](../../../reports/cp15/reproduction.md) and
[CP-16 reproduction](../../../reports/v2-causal/reproduce.md). They were **not run** for this update.
CP-16 commands charge a cumulative resource ledger. Review normally uses the saved vectors
and independent checks rather than new fits. Exact historical bytes can be retrieved with
`git show evidence/cp-15:<path>` or `git show evidence/cp-16:<path>`.

## Chart specifications (the Owner renders them)

### Chart 1: primary equal-fold scores against the §8 improvement limits

- **Form.** A dot plot with two side-by-side panels, S_MAE and S_WIS. Both panels share one
  category axis: B1, B3, B2, A1, V2-P, V2-H.
- **Axis.** The value axis is the ratio to B0, where lower is better. Use the range 0.55–1.07.
- **Reference lines.**
  - A B0 line at 1.00.
  - A limit line at **0.59203** (S_MAE) and **0.57509** (S_WIS). Label it "§8 criteria 1–2
    limit (0.90 × best B0–B3)".
- **Marks.** Label every point with its value to five decimals.
- **Colour.** Show the references in one neutral tone, A1 in a second hue, and V2-H/V2-P in a
  third.
- **Data.** Rows 44–50 of [`metrics.csv`](../../../reports/v2-causal/metrics.csv) and limits from
  [`criteria.csv`](../../../reports/v2-causal/criteria.csv) rows 2–3.
- **Caption.** "Equal-fold scores, development post-selection. Every policy, including both new
  CP-16 layers, stays above the pre-registered 10% improvement limits (criteria 1–2). B2, a
  reference, scores better than A1 on both primary scores. V2-H and V2-P have the lowest
  observed ratios but do not qualify."

### Chart 2: paired equal-fold differences with 95% intervals

- **Form.** A forest plot with two panels, ΔS_MAE and ΔS_WIS.
- **Rows.** H−P (primary), then H−B2 and P−B2 (secondary).
- **Marks.** Show the point and its 95% percentile interval. Draw a solid line at zero.
- **Required annotation.** At any readable scale, the H−P ΔS_MAE upper endpoint looks like
  zero.
  - Print it as text: **+0.000003857628092332211**.
  - Never snap or round it to 0.
  - Label each row with its frozen-rule status: "no demonstrated joint preference" (H−P,
    P−B2) or "observed joint improvement, exploratory" (H−B2).
- **Data.** Rows 32–37 of [`uncertainty.csv`](../../../reports/v2-causal/uncertainty.csv).
- **Caption.** "Paired moving-block bootstrap (seed 15042, 2,000 replicates, 7-calendar-day
  blocks), exploratory post-selection. H improves WIS over P, but the MAE interval's upper end
  is just above zero, so there is no demonstrated joint preference. This is not equivalence.
  Against B2, only H meets the joint-improvement rule."

## Reusable README / site summary

> **Research update, CP-15 and CP-16 (development, post-selection).** Two independently
> reviewed experiments on the same 10,747 historical target hours are complete and valid. That
> is an Engineering PASS, not product qualification. In CP-15, the normalized rolling LEAR
> challenger A1 had a full-crisis-fold MAE of 51.21 EUR/MWh, against 140.99 for v1. It was the
> best challenger. The rolling LEAR reference B2 still scored better on the primary equal-fold
> measures, and no policy met the pre-registered product criteria (`NOT_DEMONSTRATED`). CP-16
> blended A1 and B2 and compared hour-aware (H) against pooled (P) residual intervals. H ranks
> ahead and improves interval score (WIS), but the point-error interval ends just above zero:
> there is **no demonstrated joint preference**, and no equivalence either. H meets an
> exploratory joint-improvement rule against B2, and P does not. Both still miss the 10%
> improvement criteria. All intervals are exploratory. No product, live policy or economic
> claim follows.
