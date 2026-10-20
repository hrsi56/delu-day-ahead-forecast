# Exposure ledger — the red line before 4.7T

Research anchor v21-r13 §24.2 creates this file. The Orchestrator keeps it.

**The red line.** Delivery days from 2026-09-07 stay closed until 4.7T opens. 4.7T covers 2026-09-07
to 2026-12-05.

**What gets recorded:** every known exposure of the project to data, reports or market events
after the development boundary, with the date, source, what was exposed and what was done. Each
entry's impact assessment is recorded before CP-26's first score, and CP-26's Integration Critic
reviews it. Entries 1–5 were assessed on 2026-10-12. CP-26's Integration Critic reviewed them at
`6f57feb` (verdict `docs/track-b/evidence/cp-26/cold-rerun-2026-10-15/integration-final-r16-2-PASS.md`),
and no CP-26 return reports a new exposure (Orchestrator, 2026-10-21).

**How the audit uses it.** Before 4.7T opens, the audit (§24.9) applies §24.2's standard:

- no outcome after 2026-09-06 entered any fit, tuning, selection, registration or recorded Owner
  decision;
- incidental exposures block 4.7T only if they could have informed a registered choice.

**This file never records a market value.** An entry describes an exposure, not what was seen.

| # | Date | Source | What happened | Action | Impact assessment |
|---|---|---|---|---|---|
| 1 | 2026-09-08 | The snapshot pull (`data/source_manifest.json`, SMARD route) | The pull that produced `data/snapshot.parquet`. The first v21-r13 plan critic found no committed row after 2026-09-06 | None. The audit verifies the pull's request bounds | **None** (Orchestrator, 2026-10-12). The pull requested delivery days 2019-01-01 to 2026-09-06 (`data/source_manifest.json`). SMARD serves weekly buckets, so the last bucket can hold later hours in memory, but `src/delu_forecast/ingest.py:124–126` truncates every bucket to the requested interval before returning. No raw cache is written, and the committed snapshot holds no row after 2026-09-06 (two plan critics and CP-25 checked). Nothing after the boundary was persisted or inspected |
| 2 | 2026-09-15 | CP-15's retrieval of smard.de pages (`reports/cp15/feasibility/source_retrieval_manifest.json`) | Documentation pages, retrieved for the feasibility sheet | None | **None** (Orchestrator, 2026-10-12). The sheet records documentation (reuse terms, publication rules), not market values. The page copies sit in an ignored cache and have not been read since. No v21-r13 choice rests on a market outcome from them |
| 3 | 2026-10-11 | Stage 3's research of provider pages (`docs/track-b/data-source-research-2026-10-11.md`) | Documentation, terms and schedule pages, by the report's own account. The only data query was Elia's record counts, bounded at 2026-04-07 Brussels | None | **None** (Orchestrator, 2026-10-12). The report records no market value, and its shortlist was deferred by the short path. CP-25 used it only for documented publication times |
| 4 | 2026-10-12 | The stage 4 research agent (`docs/track-b/stage-4-methodology-memo-2026-10-12.md`) | The agent reported that a search showed it an excerpt from after 2026-04-07, which it discarded. It left no raw material, and the Orchestrator did not look for the excerpt. Its date relative to 2026-09-06 is unknown | None | **None that could inform a registered choice** (Orchestrator, 2026-10-12). Every value v21-r13 adopted from the memo is methodological: the 728-day window (already the landed rule), 14-day blocks and 10,000 replicates, the seeds, the 0.5% and 2% margins, Holm, the 364- and 728-day histories, the shrinkage, the +1, +6 and +24-hour shifts, and the origin-known state definitions. None is a market outcome or a value tuned on data. The issue-time finding rests on auction-timing papers from 2020. The excerpt's content and date stay unknown, and that is disclosed |
| 5 | 2026-10-12 | CP-25's Lead (`reports/development-inputs/tier-register.md` §6) | EU regulation texts (543/2013, 2015/1222) and SMARD's April 2026 manual, read for publication times; the CP-20 dossier's 2026-09-23 NCEP production-status capture, which is GFS production timing | None | **None** (Orchestrator, 2026-10-12). They are documents, not market data. The Lead reported no market content after 2026-09-06 |
