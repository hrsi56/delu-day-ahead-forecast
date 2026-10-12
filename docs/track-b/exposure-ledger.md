# Exposure ledger — the red line before 4.7T

Research anchor v21-r13 §24.2 creates this file. The Orchestrator keeps it.

**The red line.** Delivery days from 2026-09-07 stay closed until 4.7T opens. 4.7T covers 2026-09-07
to 2026-12-05.

**What gets recorded:** every known exposure of the project to data, reports or market events
after the development boundary, with the date, source, what was exposed and what was done. Each
entry's impact assessment is recorded before CP-26's first score, and CP-26's Integration Critic
reviews it.

**How the audit uses it.** Before 4.7T opens, the audit (§24.9) applies §24.2's standard:

- no outcome after 2026-09-06 entered any fit, tuning, selection, registration or recorded Owner
  decision;
- incidental exposures block 4.7T only if they could have informed a registered choice.

**This file never records a market value.** An entry describes an exposure, not what was seen.

| # | Date | Source | What happened | Action | Impact assessment |
|---|---|---|---|---|---|
| 1 | 2026-09-08 | The snapshot pull (`data/source_manifest.json`, SMARD route) | The pull that produced `data/snapshot.parquet`. The first v21-r13 plan critic found no committed row after 2026-09-06 | None. The audit verifies the pull's request bounds | Pending, before CP-26's first score |
| 2 | 2026-09-15 | CP-15's retrieval of smard.de pages (`reports/cp15/feasibility/source_retrieval_manifest.json`) | Documentation pages, retrieved for the feasibility sheet | None | Pending, before CP-26's first score |
| 3 | 2026-10-11 | Stage 3's research of provider pages (`docs/track-b/data-source-research-2026-10-11.md`) | Documentation, terms and schedule pages, by the report's own account. The only data query was Elia's record counts, bounded at 2026-04-07 Brussels | None | Pending, before CP-26's first score |
| 4 | 2026-10-12 | The stage 4 research agent (`docs/track-b/stage-4-methodology-memo-2026-10-12.md`) | The agent reported that a search showed it an excerpt from after 2026-04-07, which it discarded. It left no raw material, and the Orchestrator did not look for the excerpt. Its date relative to 2026-09-06 is unknown | None | Pending, before CP-26's first score. It considers whether any value adopted from the memo could carry a market outcome |
