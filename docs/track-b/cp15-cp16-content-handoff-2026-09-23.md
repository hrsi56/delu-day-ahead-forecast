# CP-15 / CP-16 local research update — content handoff

**Claude content executor · 2026-09-23.** Work in `/Users/djourno/Downloads/PJM`.
Owner approves corrected bounded execution and carries this handoff to the executor.
Prepare an English research update from accepted evidence only. This serves programme
[4.3R/4.3C](v3-plan-handoff-2026-09-22.md#work-4-3r) and
[§6 local handoff](v3-plan-handoff-2026-09-22.md#section-6); no weather result is needed.
Read `AGENTS.md`; use [capstone v21-r3](../../capstone_v21.md) §§7–8 and §§14.3–14.4
for metric/claims definitions. CP-16 closure is complete: [landing/citation map](cp-16-landing-2026-09-23.md).

**Inputs.** CP-15: [report](../../reports/cp15/report.md), its `criteria.csv`, `relative_scores.csv`,
`peak.csv`, and [Integration PASS](evidence/cp-15/integration.md).
CP-16: [report](../../reports/v2-causal/report.md), its `metrics.csv`, `uncertainty.csv`,
`criteria.csv`, [Integration PASS](evidence/cp-16/integration.md) and
[accepted receipt](cp-16-pass-receipt-2026-09-23.md).
Historical retrieval: `evidence/cp-15` / `evidence/cp-16`; CP-16 candidate
`bf3ca602e32e99e45c7835e3f95148f62b608099`, evidence tip
`5ec8a92a4032569b31a1a4f0bb3c512793d15a78`.
The candidate report's pending-review header predates the final PASS; cite the verdict/receipt
for completion and leave the historical report unchanged.

**Deliverables/allowlist.** Create only `docs/track-b/research-content/cp15-cp16-update.md`
and `docs/track-b/research-content/cp15-cp16-claims.md`: a concise narrative with a score table,
all-six-criteria comparison, up to two chart specifications/captions, a short reusable README/site
summary, and a claim-to-file/table/row map with gaps and withheld claims. Use saved values;
no new statistical calculation or rendering. **8 active hours maximum, one draft and one
evidence-consistency correction round**, both included. Close with supported content and any
remaining gap; no open-ended review. Zero downloads, fits, replays or new experiments.

**Required narrative.** Engineering PASS establishes a valid completed experiment, not product
qualification. CP-15: A1 is best among challengers, while B2 has better primary equal-fold
scores; retain the observed crisis improvement and `product_feasibility = NOT_DEMONSTRATED`.
A1 fails original criteria 1/2/5: criterion 5 fails on **fold-1 MAE 6.81990 > 6.53023**;
its WIS passes criterion 5 in every fold. Both CP-16 H and pooled-residual P pass criterion 5,
so do not attribute that transition to hour-aware intervals. The common blend and residual
construction are plausible contributors; the experiment does not isolate the blend alone.
The incremental hour-aware effect is measured by H−P. H ranks ahead descriptively, but **H–P has
“no demonstrated joint preference”**. WIS supports improvement; the MAE interval upper endpoint
is **+0.000003857628092332211**, not zero. This establishes neither equivalence nor absence
of benefit/harm. **H–B2 meets the exploratory joint-improvement rule**; P–B2 does not.
Both H/P fail original §8 improvement criteria 1–2 and meet 3–6. Preserve mixed outcomes.

Label every reused CP-15/16 result **`development_post_selection`**; comparisons and intervals
are exploratory. Keep equal-fold normalized seven-quantile WIS distinct from pooled metrics
and native v1 nine-quantile pinball. Preserve the earlier FAIL, historical monitoring limits
and regeneration disclosure. Economics stays descriptive; introduce no threshold, product
promotion, live-policy claim or new confirmation. Link existing reproduction instructions;
do not run them. Return local files, source map and exact unresolved claims to the Owner.
No edits to evidence, governance, progress, README or site sources; no staging, commits,
deployment or publication. Presentation layout remains the Owner's.
