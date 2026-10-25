# CP-28 draft publication packet

DRAFT_LOCAL. This packet grants no publication, MLflow upload or product activation authority. It follows `docs/track-b/publication-packet-template.md` (`4049c3e1f695034ec45fa185d465fce05ab1183cbded72188306579d7287d01a`) under PUBLISH_RULES 1.5 (`1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`) §11.

## Identity

- Checkpoint CP-28, brief `docs/track-b/evidence/cp-28/issued-brief.md` (`57cb6d53519ede4b709face3000caca13f7358f349c9827773871ec987fb6ba3`).
- Plan `capstone_v21.md` v21-r17 §24.8.
- Evidence tag and final candidate: recorded in the checkpoint return; the tag awaits the Owner's LAND.

## Registry (draft)

| id | kind | name | status |
|---|---|---|---|
| cp28-a1 | study arm | A1 · DDNN-2 alone, with its own Johnson SU quantiles | selected, CP-28 one look, reports/cp28/results/selection.json |
| cp28-a2 | study arm | A2 · equal weights (1/3, 1/3, 1/3), its own H layer | passed, not selected, CP-28 one look, reports/cp28/results/selection.json |
| cp28-a3 | study arm | A3 · global simplex-grid MAE fit on the latest ≤728 dates (min 364), deployed 0.5·fit + 0.5·w0 | passed, not selected, CP-28 one look, reports/cp28/results/selection.json |
| cp28-a4 | study arm | A4 · per-block grid fits (min 728), deployed 0.25·block + 0.75·A3 deployed; before 728 = A3 | passed, not selected, CP-28 one look, reports/cp28/results/selection.json |
| cp28-a5 | study arm | A5 · NumPy 16→8→3 meta-learner (min 364), deployed 0.5·network + 0.5·w0 | passed, not selected, CP-28 one look, reports/cp28/results/selection.json |
| cp28-a6 | study arm | A6 · A3's fit unshrunk (min 364) | passed, not selected, CP-28 one look, reports/cp28/results/selection.json |
| cp28-a7 | study arm | A7 · A5's network unshrunk (min 364) | passed, not selected, CP-28 one look, reports/cp28/results/selection.json |
| cp26-nominal-v5 | control | nominal v5 (control) | comparator |
| cp26-nominal-b0 | reference | B0 similar-day naive | — |

## Claims

**Permitted:**
- On CP-26's development calendar, under a one-look protocol registered before CP-26's first score, A1 passed the compound gates after Holm in all four analyses and was selected.
- Every arm's losses, ratios to the control and to B0, with descriptive intervals, are reported for the same paired dates.

**Withheld:**
- performance on unseen data or live eligibility (development, post-selection)
- a causal contribution of any member
- equivalence from a null result
- economic or trading value
- robustness to late weather (GFS+6 is fragile)

## Headline quantities

- Verdict: met. Eligible policies under the rule: 7. Comparator: nominal v5.
- Rule: §24.8 gates: improvement 0.995 on MAE and WIS; non-inferiority 1.02 in every complete year 2021–2025 and pooled season; compound max; Holm across seven at 0.05; all three sensitivity variants. Registered 2026-10-12 (anchor) and in CP-28's frozen protocol before CP-26's first score.

| arm | MAE vs control | 95% | WIS vs control | 95% |
|---|---|---|---|---|
| A1 | -7% | -9% to -5% | -11% | -13% to -9% |
| A2 | -5% | -6% to -4% | -5% | -5% to -4% |
| A3 | -6% | -6% to -5% | -5% | -6% to -4% |
| A4 | -6% | -7% to -6% | -6% | -7% to -5% |
| A5 | -5% | -6% to -4% | -4% | -5% to -4% |
| A6 | -7% | -9% to -6% | -7% | -8% to -6% |
| A7 | -6% | -8% to -5% | -5% | -6% to -4% |

Percentages are whole numbers and EUR/MWh one decimal on any reading path (PUBLISH_RULES §3.4); full precision is in `publication-packet.json` and `reports/cp28/report.md`.

## Slots, transition and product fields

- Question: Does a registered recombination of v5's three members beat v5 on both primary scores without losing more than 2% in any complete year or season?
- Decision: A1 is the CP-17 freeze candidate (CP-28 one look).
- Transition: none: CP-28 adopts no generation; the selection is a freeze candidate for CP-17.
- Product documentation: inapplicable: the released model does not change in CP-28.
- Final-product fields: unmet trigger: no final-product designation in CP-28.

## MLflow and completion

- Export: `reports/cp28/MLflow-export-draft.json`, local draft, never uploaded.
- INCOMPLETE: editorial, fresh-reader and independent publication review not performed; no public surface changed.
