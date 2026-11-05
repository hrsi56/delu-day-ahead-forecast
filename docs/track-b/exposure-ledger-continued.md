# Exposure ledger, continued — from the live pipeline's start

Research anchor v21-r20 §24.14 item 2 creates this file. It continues `docs/track-b/exposure-ledger.md`, whose pinned
file stays byte for byte, and the audit (§24.2's standard, §24.9) reads the two together. The Orchestrator keeps it;
CP-18c seeds it.

**What changed.** The Owner's decision 28 of 2026-11-05 (`docs/track-b/owner-decisions-2026-11-05.md`, SHA-256
`4daa5617e51208b0994eac925d51078ea43481e6fb1017aec3576c0936490215`) retired the boundary guard for the live pipeline
only. The live pipeline downloads all the data it needs through the present, and trains on it daily. Every research
path keeps the guard, and no agent uses data after 2026-09-06 for any research number, chart, choice or registration
before 4.7T is scored.

**What gets recorded here:** the live pipeline's operation, as one entry, and every later exposure of the project to
data, reports or market events after the development boundary that falls outside that operation, with the date, the
source, what was exposed and what was done.

**The live product's daily fits** are the frozen policy's own operation, not research fits (§24.14 item 3). They sit
outside §24.2's standard's "fit" and are recorded here, through entry 6 and the live record it names.

**This file never records a market value.** An entry describes an exposure, not what was seen.

| # | Date | Source | What happened | Action | Impact assessment |
|---|---|---|---|---|---|
| 6 | 2026-11-05 | The live pipeline (CP-18c; decision 28; r20 §24.14). Its first retrieval was the Lead's availability probe of SMARD's load-forecast series at 08:13:02Z (non-null quarter-hours counted, no value printed); the pipeline's own retrievals began at 08:15:09Z, and the first one archived in the live record at 08:17:13Z (`live/inputs/days/2026-11-06/`) | The live pipeline retrieved and archived, for delivery days 2026-09-07 to 2026-11-06, SMARD's day-ahead prices, ENTSO-E's day-ahead load forecasts and the GFS runs from the AWS archive (`live/inputs/`, each response with its URL, retrieval time, size, SHA-256 and publication evidence). It seeded the live store at the freeze origin, carried it to 2026-11-03, and issued delivery day 2026-11-06 with the frozen A1 on the Owner's Mac (`live/store/`). It reconciled that day's published prices (`live/outcomes/`), built the dated bundle and its prospective record, and then runs daily. The agents operating it read its logs and records only to operate it: retrieval counts and record metadata, the build's availability judgements, the H2 gate, the issuance records, and the bundle's gate and recomputation | The live data is handled by code. Nothing from it entered a research path: CP-25's development downloaders, CP-17c's development builder and every development report still refuse any row after 2026-09-06 (`tests/cp18c/test_guard_two_sides.py`). The development-period displays stay on days through 2026-09-06. Nothing live is labelled 4.7T's | **Nothing 4.7T tests can change after it** (§24.14 item 2, as decision 28's impact assessment). Everything 4.7T tests was frozen, registered and pushed to the public repository before decision 28: `land/cp-17c` on 2026-10-30, and the protocol at its freeze. `refreeze verify` checks the freeze on every run, and it printed `verified` before the first live issuance (the H2 gate's pins check). The live product's issuances, store and scores are its own and never 4.7T's: 4.7T issues its window itself, from the freeze-origin state, on the Owner's Mac, with its own store. Decision 28 used no information after 2026-09-06 |
