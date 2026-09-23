# CP-15 / CP-16 research update: claim-to-evidence map

**2026-09-23 · Companion to [cp15-cp16-update.md](cp15-cp16-update.md). Local draft for the Owner.**
Each claim in the update is mapped here to a saved file and to a table or row. This file also
lists the gaps, the claims that are withheld, and the exact items left open for the Owner.
Nothing was recalculated, refitted, replayed or downloaded. The update only rounds saved
values for display, except for the H−P MAE upper endpoint, which is always quoted in full.

**How to read row references.**

- `L<n>` is the physical line number in the file. CAP line references bind the original
  v21-r3 bytes at `evidence/cp-16:capstone_v21.md`, not the later CP-20 draft in the working tree.
- For a CSV, `L1` is the header row, so `L2` is the first data row.
- For markdown, `L<n>` is the line that holds the cited table row or sentence.

**Default evidence class.** Every CP-15 and CP-16 result is **`development_post_selection`**
and exploratory ([R16](../../../reports/v2-causal/report.md) L5, [PR16](../cp-16-pass-receipt-2026-09-23.md)
L65, [R15](../../../reports/cp15/report.md) L5).

## Source keys

| Key | File | Named in handoff input list |
|---|---|---|
| R15 | [reports/cp15/report.md](../../../reports/cp15/report.md) | yes |
| C15 | [reports/cp15/criteria.csv](../../../reports/cp15/criteria.csv) | yes |
| RS15 | [reports/cp15/relative_scores.csv](../../../reports/cp15/relative_scores.csv) | yes |
| PK15 | [reports/cp15/peak.csv](../../../reports/cp15/peak.csv) | yes |
| I15 | [docs/track-b/evidence/cp-15/integration.md](../evidence/cp-15/integration.md) | yes |
| L15 | [docs/track-b/cp-15-landing.md](../cp-15-landing.md) | retrieval context (plan §6) |
| R16 | [reports/v2-causal/report.md](../../../reports/v2-causal/report.md) | yes |
| M16 | [reports/v2-causal/metrics.csv](../../../reports/v2-causal/metrics.csv) | yes |
| U16 | [reports/v2-causal/uncertainty.csv](../../../reports/v2-causal/uncertainty.csv) | yes |
| C16 | [reports/v2-causal/criteria.csv](../../../reports/v2-causal/criteria.csv) | yes |
| D16 | [reports/v2-causal/diagnostics.csv](../../../reports/v2-causal/diagnostics.csv) | **no.** It is a saved table in the same report bundle, used only for the H/P peak hit counts (see G3). |
| I16 | [docs/track-b/evidence/cp-16/integration.md](../evidence/cp-16/integration.md) | yes |
| PR16 | [docs/track-b/cp-16-pass-receipt-2026-09-23.md](../cp-16-pass-receipt-2026-09-23.md) | yes |
| LD16 | [docs/track-b/cp-16-landing-2026-09-23.md](../cp-16-landing-2026-09-23.md) | yes (landing/citation map) |
| BR16 | [docs/track-b/cp-16-blocked-receipt-2026-09-23.md](../cp-16-blocked-receipt-2026-09-23.md) | earlier FAIL (preservation requirement) |
| RN16 | [docs/track-b/evidence/cp-16/resumption-notice.md](../evidence/cp-16/resumption-notice.md) | under `evidence/cp-16` (regeneration disclosure) |
| CAP | [capstone_v21.md](../../../capstone_v21.md) | yes (§7 L227–250, §8 L252–273, §14.1 L415–440, §14.3 L495–522, §14.4 L524–555) |
| PLAN | [docs/track-b/v3-plan-handoff-2026-09-22.md](../v3-plan-handoff-2026-09-22.md) | programme context (§2 L99–119, §5.5 L853–875, §5.6 L877–918, §6 L972–1006) |

## Claim map

Status codes:

- **S**: supported by a saved value or verdict.
- **S-d**: supported, but descriptive only.
- **S-h**: historical reported evidence, not re-verified here.
- **I**: an inference drawn from design plus saved values. It may be used only in the wording
  given.
- **Def**: a definition.

### Status, identity and retrieval

| ID | Claim as used in the update | Source → table/row | Status |
|---|---|---|---|
| C01 | CP-15 Integration **PASS** at candidate `fc4aee038cf898998a292506df62ddb0dcfaf22a`. It certifies the completed experiment, not product quality. | I15 L3, L9 | S |
| C02 | CP-16 Integration **PASS** at candidate `bf3ca602e32e99e45c7835e3f95148f62b608099`, accepted by receipt. The evidence tip is `5ec8a92a4032569b31a1a4f0bb3c512793d15a78`. | I16 L3, L9; PR16 L23–25 | S |
| C03 | Both candidate reports still carry a "pending Integration" header. The verdicts and the receipt are what establish completion, and the reports stay unchanged. | R15 L3; R16 L3; I15 L104 (checklist item 5) | S |
| C04 | Historical retrieval: `evidence/cp-15` = `1bdc75b8ab943092bb8de6ba893defb9e12250d8` and `evidence/cp-16` = `5ec8a92a4032569b31a1a4f0bb3c512793d15a78`. `land/cp-16` = `d62769c0cf23c5c252213da92d7f39684e4aa284`. | L15 L24; LD16 L12–17, L47–52. `git rev-parse` was run read-only on 2026-09-23, and both candidates are reachable from their evidence tags. | S |
| C05 | CP-15 status: `NOT_DEMONSTRATED`, best observed A1, qualified policy none. | R15 L5; I15 L9 | S |
| C06 | CP-16: the original-§8 diagnostic is `not_met` for H and P. The CP-15 status is unchanged. Delivery is not authorized. | R16 L3; PR16 L56–58; I16 L126 | S |

### Population and definitions

| ID | Claim | Source → table/row | Status |
|---|---|---|---|
| C07 | There are 10,747 identical eligible keys, with fold counts 2,160 / 2,159 / 2,112 / 2,160 / 2,156. Fold 3 is 2,112 h over 88 dates. The peak is 2022-08-15..31, 408 h over 17 days. | R15 L11–21; R16 L36; CAP L425–430 | S |
| C08 | Five fold start dates, 2019-01-01 floor, D−1 11:00 UTC origin, D−2 error release | R15 L15–19, L229; R16 L38; CAP L399–400 | S |
| C09 | Policy definitions for B0–B3 and A1–A5 | CAP §5 L150–160 | Def |
| C10 | H and P share the 50/50 A1/B2 central blend and the 28-day buffer. H uses n/(n+56) shrinkage with a 14-day fallback, and P is pooled. Hour-aware pooling is the only difference. | R16 L38; CAP L417–421, L443–470 | Def/S |
| C11 | S_MAE/S_WIS are equal-fold ratios to B0. MAE uses the emitted p50. WIS uses seven quantiles, weights alpha/2 and 1/2, and divisor 3.5. Pooled scores are secondary. Native v1 nine-quantile pinball is distinct. | CAP L232–239, L497–498; R16 L9 | Def |
| C12 | The criteria 1–2 limits are 0.59203 and 0.57509, and the text of criteria 1–6 is quoted. | CAP L257–268; C15 L2–3; C16 L2–3 | Def/S |

### Score table (update § "Score table")

| ID | Row(s) | S_MAE / S_WIS | Pooled MAE / WIS | Fold-3 MAE | Peak hits |
|---|---|---|---|---|---|
| C13 | B0 | RS15 L2; M16 L44 | M16 L2; R15 L29 | M16 L5; R15 L122 | PK15 L7; R15 L152 |
| C14 | B1 v1 replay | RS15 L3; M16 L45 | M16 L8; R15 L30 | M16 L11; R15 L127 | PK15 L8; R15 L153 |
| C15 | B2 | RS15 L4; M16 L46 | M16 L14; R15 L31 | M16 L17; R15 L132 | PK15 L9; R15 L154 |
| C16 | B3 | RS15 L5; M16 L47 | M16 L20; R15 L32 | M16 L23; R15 L137 | PK15 L10; R15 L155 |
| C17 | A1 | RS15 L6; M16 L48 | M16 L26; R15 L33 | M16 L29; R15 L97 | PK15 L2; R15 L147 |
| C18 | A2–A5 (CP-15 only) | RS15 L7–10; R15 L34–37 | R15 L34–37 | R15 L102, L107, L112, L117 | PK15 L3–6; R15 L148–151 |
| C19 | V2-H | M16 L49; R16 L18 | M16 L32 | M16 L35 | D16 L837 (hit_count95 = 377) |
| C20 | V2-P | M16 L50; R16 L19 | M16 L38 | M16 L41 | D16 L977 (hit_count95 = 377) |

All of these rows are status S, with peak values S-d. The reference values that CP-16
re-scored match CP-15 at the displayed precision. For example, the B2 S_MAE is
`0.6578109123747921` in both RS15 L4 and M16 L46.

### CP-15 findings

| ID | Claim | Source → table/row | Status |
|---|---|---|---|
| C21 | The ranking is A1, A3, A5, A4, A2, and A1 is the best challenger. | R15 L43–47; I15 L90 | S |
| C22 | B2 has better primary equal-fold scores than A1 (0.65781/0.63899 against 0.67229/0.64602). | RS15 L4, L6 | S |
| C23 | A1's pooled MAE and WIS are lower than B2's. The weightings disagree, and the registered equal-fold weighting decides. | R15 L31, L33; M16 L14, L26; I15 L90 | S |
| C24 | Crisis: A1's fold-3 MAE is 51.21276, against v1's 140.99285 and B2's 54.00782. The plan summarizes this as "~64%". | M16 L29, L11, L17; R15 L97, L127, L132; PLAN L110–111 | S (the percentage is quoted from PLAN, not recalculated) |
| C25 | Peak: A1 has 378/408 hits in its 95% intervals, against v1's 79/408. | PK15 L2, L8 | S-d |
| C26 | A1 fails criteria 1, 2 and 5 (0.67229 > 0.59203 and 0.64602 > 0.57509). | C15 L2, L3, L11; R15 L55–57 | S |
| C27 | A1's criterion 5 fails only on **fold-1 MAE: 6.81990 > 6.53023**. Its MAE in folds 2–5 passes. | C15 L11; C15 L12–15 | S |
| C28 | A1's WIS passes criterion 5 in every fold. | C15 L17–21 | S |
| C29 | A1 meets criteria 3, 4 and 6. | C15 L4–10, L16, L22 | S |
| C30 | No CP-15 challenger qualifies. | R15 L43–47; I15 L90 | S |

### CP-16 findings

| ID | Claim | Source → table/row | Status |
|---|---|---|---|
| C31 | H ranks ahead of P descriptively (S_WIS 0.61603 against 0.62872, and S_MAE 0.64407 against 0.64577). This is not a supported winner. | M16 L49–50; R16 L5; PR16 L52 | S |
| C32 | H−P: **no demonstrated joint preference**. | R16 L5, L32; I16 L136; PR16 L53 | S |
| C33 | H−P ΔS_WIS = −0.0126918, interval [−0.0155712, −0.0109119], wholly below zero. | U16 L33; R16 L26 | S |
| C34 | H−P ΔS_MAE = −0.0016954, interval [−0.0036237, **+0.000003857628092332211**]. The upper endpoint is not zero. | U16 L32 (`3.857628092332211e-06`); I16 L136; PR16 L62 | S |
| C35 | This establishes neither equivalence nor absence of benefit or harm. | CAP L542–546; R16 L5; I16 L136 | Def/S |
| C36 | Only H−P measures the added effect of hour awareness. | CAP L419–421 (P differs only in pooling), L534 (primary contrast) | Def |
| C37 | H−B2 meets the exploratory joint-improvement rule. ΔS_MAE = −0.0137388 [−0.0235719, −0.0053442] and ΔS_WIS = −0.0229611 [−0.0336965, −0.0118099]. | U16 L34–35; R16 L32; PR16 L54 | S |
| C38 | P−B2 does not. Its ΔS_MAE interval, −0.0120433 [−0.0212870, −0.0035563], is below zero. Its ΔS_WIS, −0.0102693 [−0.0200602, +0.0006704], spans zero. | U16 L36–37; PR16 L55 | S |
| C39 | H and P fail criteria 1–2 and meet 3–6. | C16 L2–43; R16 L50–91; PR16 L56; I16 L136 | S |
| C40 | H and P pass criterion 5 in every fold for MAE and WIS. Their fold-1 MAE is 6.31080 and 6.34197, against a limit of 6.53023. | C16 L11–15, L17–21 (H); L32–36, L38–42 (P) | S |
| C41 | The shared criterion-5 transition cannot be attributed **uniquely** to hour-aware intervals, because P passes too; H−P measures the incremental effect. | C27 + C40 + C10 | I |
| C42 | The shared blend and residual construction are **plausible contributors**. The experiment does not isolate the blend alone. | CAP L417–421 (no blend-only or residual-only arm); C27, C40 | I (limited to "plausible contributor"; see G1) |
| C43 | Per fold, H has lower WIS than P in all five folds. H has higher MAE than P in folds 2 and 3 (9.45709 against 9.44352, and 51.21362 against 51.05393) and lower MAE in folds 1, 4 and 5. | M16 L33–37 against L39–43; per-fold paired rows U16 L2–3, L8–9, L14–15, L20–21, L26–27 | S-d |
| C44 | B2 keeps a lower fold-1 MAE (6.21927) than H (6.31080) or P (6.34197). | M16 L15, L33, L39 | S-d |
| C45 | Fold-3 MAE is almost the same for A1 (51.21276), H (51.21362) and P (51.05393). | M16 L29, L35, L41 | S-d |
| C46 | Peak: A1 has lower MAE and WIS (49.87670/29.40371) than H (52.50980/30.10205) and P (52.65780/30.85481). Hit counts are 378/377/377. | PK15 L2; C16 L10, L16, L31, L37; D16 L697, L837, L977 | S-d |
| C47 | H and P share the same central blend, with a pooled central MAE of 19.99979. Their emitted p50 MAE is 20.23104 (H) and 20.24313 (P). | M16 L32, L38 (`raw_central_MAE`, `MAE`, `centering_effect`); per-fold central values are equal in L33–37 and L39–43 | S-d |
| C48 | H has narrower pooled mean 95% width (124.63573 against 133.96917). Its pooled 95% coverage is 0.93887, against 0.94222 for P. | M16 L32, L38 (`mean_width95`, `coverage95`) | S-d |

### History, limits and notices

| ID | Claim | Source → table/row | Status |
|---|---|---|---|
| C49 | CP-15 attempt 1 keeps its FAIL: candidate `f8d0ed2a5f0737f0d088c3474b5a9fe77a406f37`, tip `193d9cf48c586b9c4b1f43d7a5677b2d5f400832`. | R15 L225 | S |
| C50 | CP-16's first attempt was BLOCKED, with an independent Integration FAIL: candidate `3a160fd33ed92bb0061144cfbce2323d8b3a7db9`, tip `41b0e6d222a3d65d474ac5974c6eb7017db317e8`. It produced no research conclusion. | BR16 L22–27, L37–43; R16 L114 | S |
| C51 | Monitoring limits: RSS during the monitor gap is unknown, and early BLAS/concurrency assertions were unsupported. None of this is certified retroactively. The 3,730 debit stands. | RN16 L5; PR16 L84–87; R16 L114 | S |
| C52 | Regeneration: the evidence was regenerated under repaired monitoring without changing the recipe. An oracle fixture bug and its failed run (126/1) are retained. | RN16 L5, L13; R16 L114 | S |
| C53 | v1 history: p=0.948, statistic +1.6228, median 28.58% worse, and v1 peak 79/408. CP-10: peak 131/408 and full fold 1,515/2,112. | R15 L227; PLAN L101–103 | S-h |
| C54 | The A65 vintage and revision assumptions are inherited. The 2019 floor holds. Residual intervals carry no conformal guarantee. | R15 L229; R16 L116; CAP L399–400 | S |
| C55 | The 17-day peak is descriptive. The 56-date rule is a reporting convention. Twenty-eight errors per hour give no guarantee on the tails. | RN16 L11; CAP L505–511 | Def/S |
| C56 | CP-15 and CP-16 computed no economics. Battery sensitivities are separate review evidence (PLAN §5.6) and are not restated. | R16 L116; CAP L552–553; PLAN L877–918 | S |
| C57 | There is no promotion, live policy, CP-17, prospective clock or publication. | I15 L9; I16 L9; PR16 L57–58; LD16 L67–77 | S |
| C58 | Data notice: ENTSO-E and SMARD.de, CC BY 4.0. `DATA-LICENSE.md` controls. | R15 L7; R16 L116 | S |
| C59 | The reproduction instructions exist and were not run for this update. | [CP-15](../../../reports/cp15/reproduction.md); [CP-16](../../../reports/v2-causal/reproduce.md) | S |

### Chart and summary sources

| Item | Data rows | Notes |
|---|---|---|
| Chart 1 (equal-fold dot plot) | M16 L44–50; limits C16 L2–3 | The B0 line is at 1.0 by definition. |
| Chart 2 (forest plot) | U16 L32–37 | The H−P MAE endpoint label must use the full value in U16 L32. |
| README/site summary | C05, C21–C24, C31–C39, C57 | The "51.21 / 140.99" figures are the saved values in M16 L29 and L11, rounded to two decimals. |

## Gaps: documented, not resolved by this content

| ID | Gap | Why it stays open |
|---|---|---|
| G1 | **Attribution of the criterion-5 change between the blend and the residual layer.** No arm pairs the blend with CP-15's A1 residual layer, and no arm pairs A1 with the CP-16 layer. This update also does not assert that P's pooled layer is operationally identical to CP-15's residual construction. | Closing it would need a new experiment or an implementation audit. Both are outside a content task, and no new calculation is permitted. |
| G2 | A2–A5 appear only in CP-15. CP-16 did not re-score them. | This follows from CP-16's fixed scope (CAP L422–424). |
| G3 | The H/P peak hit counts (377) come from D16, a saved CP-16 table that is not in the handoff's named input list. | Resolved at intake: retain 377 from accepted CP-16 diagnostics (D16). This is saved evidence, not a new calculation or Owner parameter decision. |
| G4 | No native v1 nine-quantile pinball values are quoted. | They are in historical v1 records that are not among the inputs. |
| G5 | "~64%" is the plan's rounded wording and was not recalculated. | The saved endpoints are 140.99285 and 51.21276. |
| G6 | The v1 p=0.948 statistic and the CP-10 counts are historical, reported evidence. | This task did not re-verify them. B1's 79/408 peak count is saved in PK15 L8. |
| G7 | Historical availability of the A65 vintages is not proven for every issue vintage. | It is an inherited assumption (R15 L229). |
| G8 | Per-hour and block diagnostics (24 hours; night, solar and shoulder blocks) are not summarized. | The handoff asked for a concise scope. No claim is made about hour or block effects (see W9). |
| G9 | Local research scope is approved; public release remains outside this task. | No README/site edit or publication is authorized; public-release decisions can wait without blocking this local draft. |
| G10 | Charts are specified but not rendered, and the layout is not reviewed. | Presentation belongs to the Owner. |

## Withheld claims: do not use

| ID | Withheld claim | Reason / controlling source |
|---|---|---|
| W1 | "Hour-aware intervals (H) are better than pooled (P)" or "H is preferred" | The frozen rule gives no demonstrated joint preference, and only the WIS gain is supported (C32–C34). |
| W2 | "H and P are equivalent", "hour awareness has no effect", "no benefit" or "no harm" | Explicitly not established (CAP L542–546). |
| W3 | Rounding the MAE endpoint to 0.0000 or "≈0" to claim joint improvement | This is prohibited (R16 L32; I16 L136). |
| W4 | "Hour-aware intervals fixed criterion 5" | P passes too (C41). |
| W5 | "The blend alone fixed criterion 5" | The experiment does not isolate it (C42, G1). |
| W6 | Any claim of product feasibility, qualification, readiness, promotion, live-policy selection, a CP-17 freeze or prospective validation | Not authorized (C05, C06, C57). |
| W7 | Confirmatory or significance wording (p-values, "significantly beats B2", family-wise claims) | Exploratory and post-selection only (CAP L534–536). |
| W8 | Any economic value, revenue, battery gain, threshold or annualization | None was computed (C56). Battery sensitivities are separate review evidence with their own population. |
| W9 | Hour or block effects (for example, "better solar-hour coverage") or significance at the peak | Not summarized (G8). The peak has 17 days and is descriptive. |
| W10 | Calling seven-quantile WIS "pinball", or comparing it with native v1 pinball | These are different metrics (C11). |
| W11 | Headlining pooled scores (for example, "A1 beats B2") as primary results | The equal-fold weighting controls (C23). |
| W12 | "CP-16 confirms the earlier review oracles": PLAN §5.5's .589–.638 landing range, the ~2.4% interval-only opportunity, or the author's criterion-5 pass | Those were evaluation-residual oracles or unverified expectations with different recipes (PLAN L853–875). |
| W13 | Presenting the earlier A1+B2 review scores (.64466 / .64070 / .64280) as CP-16 results | Different policies (PLAN L111–113). |
| W14 | Performance claims for weather, VRE, Chronos-2, TabPFN or DDNN | Not tested. The Chronos-2 probe was unscored (R15 L219–221). |
| W15 | A coverage guarantee | Intervals are empirical, with no conformal guarantee (C54). |
| W16 | A statement that this content, CP-16 or a README/site update has been published | CP-16 landing was local only (LD16 L77–78). This content is unpublished. |

## Exact unresolved items returned to the Owner

1. **G1:** the criterion-5 change stays attributed only as "the blend and residual
   construction are plausible contributors; not isolated". No stronger wording is supported.
2. **G3 resolved at intake:** retain the existing accepted D16 hit count 377; no further decision.
3. **G9:** local research scope is approved. Public use remains separately unapproved; nothing
   goes to README or site sources in this task.
4. **G10:** chart rendering/layout remain optional Owner presentation work, not an intake
   prerequisite or executor instruction. Specifications and captions are in the update.
5. **G4 and G6:** native v1 pinball numbers are omitted. The v1 and CP-10 history is quoted as
   reported, not re-verified.
