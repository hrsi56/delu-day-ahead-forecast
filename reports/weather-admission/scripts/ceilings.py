"""Write usage/ceilings.md from the usage logs, attempt log, resource samples and disk totals (offline)."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPORT = HERE.parent
ROOT = REPORT.parents[1]
LOCAL = ROOT / ".local" / "weather-admission"


def du_k(path: Path) -> int:
    out = subprocess.run(["du", "-sk", str(path)], capture_output=True, text=True, check=True).stdout
    return int(out.split()[0])


def main() -> None:
    use = json.loads((REPORT / "usage" / "transfer.json").read_text())
    recs = [json.loads(l) for l in (LOCAL / "logs" / "usage.jsonl").read_text().splitlines() if l.strip()]
    first = min(r["t_utc"] for r in recs)
    last = max(r["t_utc"] for r in recs)
    import datetime as dt

    span_h = (dt.datetime.fromisoformat(last.replace("Z", "+00:00")) - dt.datetime.fromisoformat(first.replace("Z", "+00:00"))).total_seconds() / 3600
    local_k = du_k(LOCAL)
    report_k = du_k(REPORT)
    cats = "\n".join(f"| {k} | {v['requests']:,} | {v['mib']:,.1f} |" for k, v in use["by_category"].items())
    md = f"""# Usage against ceilings

Generated offline by `scripts/ceilings.py` from `.local/weather-admission/logs/`.

| Ceiling (maximum, not target) | Maximum | Used | Basis |
|---|---|---|---|
| Active hours | 16 | ≈1.5 h (nearest half hour) | wall clock: work started ≈12:30Z, return ≈14:05Z on 2026-09-23 |
| Archive products | 2 | 2 | GFS 0.25° (NCAR d084001 + NCAR-linked NOAA AWS copy of the same product), OCF ICON-EU |
| Initialization runs decoded | 24 (12 GFS + 12 ICON) | 22 (12 GFS + 10 ICON) | one decoded bundle per run |
| Decoding attempts (incl. failures/retries) | 48 | {use['decode_attempts']['total']} ({use['decode_attempts']['success']} success, {use['decode_attempts']['failure']} failure) | `decode_attempts.csv` |
| Native fields per bundle | 6 | GFS 5 (u/v 10 m, u/v 100 m, DSWRF total); ICON 4 (u/v 10 m, ASWDIR_S, ASWDIFD_S; hub u/v unsupported, not retrieved) | |
| Native endpoints | h0–h48 | GFS f021–f048 (3-hourly); ICON steps 22–47 decoded (chunks hold 0–73) | |
| Cumulative transfer | 4 GiB (stop line 3.85 GiB) | **{use['gib']:.3f} GiB** ({use['bytes']:,} bytes, {use['requests']:,} requests) | every request metered, headers included; dependencies logged as an interface-counter upper bound |
| Additional disk | 8 GiB | peak 1.87 GiB in `.local/weather-admission/` (`du -sk` 1,959,856 KiB at 13:4xZ, including a 150 MiB package cache); {local_k / 1024**2:.2f} GiB retained after cleanup; {report_k / 1024:.1f} MiB report | `du -sk` |
| Aggregate RSS | 8 GiB | max summed {use['max_summed_rss_mib']:.0f} MiB over ≤{use['max_concurrent_processes']} processes (sampled from 13:10Z); single runs 141–160 MiB (`/usr/bin/time`) | `logs/resources.txt` |
| CPU cores | 4 | max ≈{use['max_cores_equivalent']:.1f} core-equivalent summed; all work I/O-bound | `logs/resources.txt` |
| Machine hours | 8 | ≈{span_h:.1f} h of machine wall time with network/background jobs ({first}–{last}); ≈{use['integrated_cpu_hours_sampled']:.2f} CPU-h integrated over the sampled span | |
| Cost | $0 | $0 | anonymous/free access; existing HF token |
| Fits / model runs / full-archive downloads | 0 / 0 / 0 | 0 / 0 / 0 | only targeted byte ranges and metadata |

## Transfer by category

| Category | Requests | MiB |
|---|---:|---:|
{cats}

The ICON sample figure includes ≈0.75 GiB of duplicate chunk reads caused by a store
wrapper fault (`Mapping.__contains__` downloading values) in the first seven runs; it was
fixed before the last three runs and is counted, not excluded.

HTTP errors: {use['errors']} (status counts {use['http_status_counts']}).
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
"""
    (REPORT / "usage" / "ceilings.md").write_text(md)
    print(md[:400])


if __name__ == "__main__":
    main()
