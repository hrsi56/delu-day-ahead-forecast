# Usage against ceilings

Generated offline by `scripts/ceilings.py` from `.local/weather-admission/logs/`.

| Ceiling (maximum, not target) | Maximum | Used | Basis |
|---|---|---|---|
| Active hours | 16 | ≈1.5 h (nearest half hour) | wall clock: work started ≈12:30Z, return ≈14:05Z on 2026-09-23 |
| Archive products | 2 | 2 | GFS 0.25° (NCAR d084001 + NCAR-linked NOAA AWS copy of the same product), OCF ICON-EU |
| Initialization runs decoded | 24 (12 GFS + 12 ICON) | 22 (12 GFS + 10 ICON) | one decoded bundle per run |
| Decoding attempts (incl. failures/retries) | 48 | 34 (22 success, 12 failure) | `decode_attempts.csv` |
| Native fields per bundle | 6 | GFS 5 (u/v 10 m, u/v 100 m, DSWRF total); ICON 4 (u/v 10 m, ASWDIR_S, ASWDIFD_S; hub u/v unsupported, not retrieved) | |
| Native endpoints | h0–h48 | GFS f021–f048 (3-hourly); ICON steps 22–47 decoded (chunks hold 0–73) | |
| Cumulative transfer | 4 GiB (stop line 3.85 GiB) | **3.426 GiB** (3,678,795,640 bytes, 51,092 requests) | every request metered, headers included; dependencies logged as an interface-counter upper bound |
| Additional disk | 8 GiB | peak 1.87 GiB in `.local/weather-admission/` (`du -sk` 1,959,856 KiB at 13:4xZ, including a 150 MiB package cache); 1.73 GiB retained after cleanup; 3.0 MiB report | `du -sk` |
| Aggregate RSS | 8 GiB | max summed 562 MiB over ≤9 processes (sampled from 13:10Z); single runs 141–160 MiB (`/usr/bin/time`) | `logs/resources.txt` |
| CPU cores | 4 | max ≈1.0 core-equivalent summed; all work I/O-bound | `logs/resources.txt` |
| Machine hours | 8 | ≈1.3 h of machine wall time with network/background jobs (2026-09-23T12:34:54Z–2026-09-23T13:53:45Z); ≈0.07 CPU-h integrated over the sampled span | |
| Cost | $0 | $0 | anonymous/free access; existing HF token |
| Fits / model runs / full-archive downloads | 0 / 0 / 0 | 0 / 0 / 0 | only targeted byte ranges and metadata |

## Transfer by category

| Category | Requests | MiB |
|---|---:|---:|
| sample retrieval (ICON) | 523 | 1,920.2 |
| sample retrieval (GFS) | 2,140 | 695.8 |
| inventory (GFS) | 39,704 | 590.7 |
| inventory (ICON) | 8,458 | 200.6 |
| dependencies | 1 | 39.7 |
| debug/probe/discovery | 122 | 26.7 |
| cross-endpoint comparison | 91 | 25.5 |
| sources and dated captures | 50 | 8.9 |
| access verification | 3 | 0.3 |

The ICON sample figure includes ≈0.75 GiB of duplicate chunk reads caused by a store
wrapper fault (`Mapping.__contains__` downloading values) in the first seven runs; it was
fixed before the last three runs and is counted, not excluded.

HTTP errors: 30 (status counts {'200': 7832, '0': 13, '206': 43230, '400': 3, '404': 12, '504': 2}).
- NCAR connect timeouts were retried and succeeded.
- 404s are genuinely absent objects: the AWS 2021-02-02 indexes, the non-existent 2026
  directory in the ICON tree, and the probe for NCAR `.idx` files.
- 400s were one size-0 range request during structure discovery and the two tests showing
  NCAR rejects suffix ranges.
- 504s were a Wayback CDX query that was not needed.
- DNS/TLS failures came from discovery probes of retired NCAR hostnames.

## Cleanup and retained local material

Removed after the task: `.local/weather-admission/uvcache/` (package cache), empty `tmp/`
and `wheels/`. Retained for review, all Git-ignored under `.local/weather-admission/`:
`cache/gfs/` (raw sampled GRIB2 messages), `cache/icon/` (raw sampled Zarr chunks),
`cache/*inventory*` and `cache/icon_tree/` (inventory responses), `sources/` (dated source
copies), `logs/` (usage, attempts, resources, job logs) and `venv/` (decoder environment).
The Owner may delete them; the report carries their hashes.
