# Extraction volume and time estimates (for a later, separately authorized extraction)

These are planning estimates, derived from measurements taken in this task. They are not
budgets and not feasibility claims, and no full extraction was performed. Required runs
are the D−1 00 UTC runs for the union of fold windows (see `sample-manifest.json`).

## Required run counts

| Scope | Runs |
|---|---:|
| GFS union 2019-01-01..2022-09-27 and 2023-04-01..2026-04-06 | 2,468 |
| NCAR-only part (2019-01-01..2020-12-31; AWS starts 2021-01-01) | 731 |
| AWS part (2021-01-01 onward), plus 2021-02-02 from NCAR | 1,737 |
| ICON runs present and field-complete within the archive span, all fold windows | ≈1,630 |

## GFS (ADMITTED scope)

Measured target-message bytes per run are for 5 global messages × 10 leads, whole GRIB2
messages (a message cannot be spatially subset):

| Version | Runs in scope | MiB/run (measured) | Transfer |
|---|---:|---:|---:|
| v14 (to 2019-06-12) | 163 | 33.1 | ≈5.3 GiB |
| v15.1 (2019-06-13..2021-03-22) | 649 | 39.7 | ≈25.2 GiB |
| v16 (from 2021-03-23) | 1,656 | 43.4 | ≈70.2 GiB |
| **Total** | 2,468 | | **≈101 GiB** |

**Time.** Measured wall time per run:
- About 15 s from AWS when unloaded, and 45–130 s under concurrent load. One stall
  needed a retry.
- 240–300 s from NCAR, which needs the jump-and-hop search because it has no index files.

Projected:
- AWS part: about 1,737 × 15–45 s, so 7–22 h sequential or about 2–6 h with 4 workers.
- NCAR part: about 731 × 270 s, so about 55 h sequential or about 14 h with 4 workers.
  At the observed ≈0.6 MB/s, NCAR's 27.6 GiB of payload alone is about 13 h of transfer.

**Cheaper variants to evaluate before a full run.** Neither was tested for equivalence here.
- NCAR NCSS subsetting of only the Germany box: tens of KB per file, about 7 s per
  request, so about 14 h sequential for 7,310 files. The server then decodes the GRIB, so
  its output must first be checked against the local ecCodes decode of the retained raw
  NCAR messages from the five sampled runs.
- Building a full per-file index once per NCAR file, instead of the jump search. This
  needs many header reads per file and is slower on NCAR's latency.

**Local storage** if only the Germany box (34 × 41 points, float32) is kept:
- 5 fields × 10 leads is about 0.28 MB per run, so about 0.7 GiB in total.
- Raw global messages need not be kept (about 101 GiB if they were).

**Local CPU.** ecCodes decoding plus derivation took about 1.3 s of user CPU per run, so
under 1 CPU-hour for all runs.

## ICON (NOT_ADMITTED; shown for §3.2 options only)

Chunk granularity forces about 110–128 MB per run (4 fields × 4 chunks) to cover Germany
for steps 22–47:
- Transfer: about 1,630 runs × ≈115 MB ≈ **175 GiB**.
- Time: at the observed ≈2.5 MB/s, about 20 h of transfer (35–60 s per run).
- Germany box storage (133 × 161 points × 4 fields × 26 steps, float32) is about 8.9 MB
  per run, so about 14.5 GiB; zonal aggregates would be negligible.

## This task's actual spend, for scale

See `usage/transfer.json` and `dossier.md` § Usage. The transfer ceiling (4 GiB) would
cover about 90 GFS runs or about 35 ICON runs of full extraction, so a full extraction
needs its own authorization and budget.
