"""Q3 -- Per-series native resolution, and since when (capstone S4.0).

For A44 (price), A65/A01 (load forecast), A65/A16 (actual load), and
A69/A01 (VRE forecast) on DE-LU: pulls a short sample window at three points
in time (near archive start, pre-MTU-transition, post-MTU-transition) and
reports the inferred resolution (PT15M vs PT60M / points-per-day) for each.

Expectation to test: load/VRE feeds are PT15M well before the price's
2025-10-01 transition.

Usage: uv run scripts/q3_resolution.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
from entsoe.exceptions import NoMatchingDataError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from spike.entsoe_helpers import DE_LU, get_client, to_pairs, write_evidence

WINDOWS = {
    "near_archive_start_2019": ("2019-01-07", "2019-01-10"),
    "pre_mtu_transition_2025": ("2025-06-01", "2025-06-04"),
    "post_mtu_transition_now": ("2026-06-08", "2026-06-11"),
}

SERIES = {
    "A44_price": lambda c, s, e: c.query_day_ahead_prices(DE_LU, start=s, end=e),
    "A65_A01_load_forecast": lambda c, s, e: c.query_load_forecast(DE_LU, start=s, end=e, process_type="A01"),
    "A65_A16_actual_load": lambda c, s, e: c.query_load(DE_LU, start=s, end=e),
    "A69_A01_vre_forecast": lambda c, s, e: c.query_wind_and_solar_forecast(DE_LU, start=s, end=e, process_type="A01"),
}


def main() -> None:
    client = get_client()
    evidence = {"probe": "q3_resolution", "windows": {}}

    for window_name, (start_str, end_str) in WINDOWS.items():
        start = pd.Timestamp(start_str, tz="Europe/Berlin")
        end = pd.Timestamp(end_str, tz="Europe/Berlin")
        n_days = (end - start).days
        print(f"\n=== {window_name}: {start_str} -> {end_str} ({n_days} days) ===")
        evidence["windows"][window_name] = {"start": start_str, "end": end_str}
        for series_name, fn in SERIES.items():
            try:
                data = fn(client, start, end)
                n_rows = len(data)
                freq = pd.infer_freq(data.index)
                points_per_day = n_rows / n_days
                resolution = "PT15M" if abs(points_per_day - 96) < 1 else ("PT60M" if abs(points_per_day - 24) < 1 else f"~{points_per_day:.1f}/day")
                print(f"  {series_name:24s} n={n_rows:4d}  freq={freq!s:6s}  pts/day={points_per_day:5.1f}  -> {resolution}")
                evidence["windows"][window_name][series_name] = {
                    "status": "OK",
                    "n_rows": n_rows,
                    "inferred_freq": str(freq),
                    "points_per_day": points_per_day,
                    "resolution": resolution,
                    "sample": to_pairs(data, n=3),
                }
            except NoMatchingDataError:
                print(f"  {series_name:24s} NO_DATA")
                evidence["windows"][window_name][series_name] = {"status": "NO_DATA"}
            except Exception as e:  # noqa: BLE001
                print(f"  {series_name:24s} ERROR: {type(e).__name__}: {e}")
                evidence["windows"][window_name][series_name] = {"status": "ERROR", "error": f"{type(e).__name__}: {e}"}

    out = write_evidence("q3_resolution", evidence)
    print(f"\nEvidence written to {out}")


if __name__ == "__main__":
    main()
