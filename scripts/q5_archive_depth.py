"""Q5 -- Archive depth at/near 2019-01-01 (capstone S3, CP-1 item 1).

Sample pulls (not bulk) at the 2019-01-01 window edge for A44, A65/A01, and
A69/A01 on DE-LU, confirming non-empty results.

Usage: uv run scripts/q5_archive_depth.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
from entsoe.exceptions import NoMatchingDataError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from spike.entsoe_helpers import DE_LU, get_client, to_pairs, write_evidence

# 2019-01-01 00:00 local is the window start; pull a few days either side of
# it to confirm the platform actually has data right at the edge (not just
# "somewhere in 2019").
START = pd.Timestamp("2018-12-30", tz="Europe/Berlin")
END = pd.Timestamp("2019-01-03", tz="Europe/Berlin")

SERIES = {
    "A44_price": lambda c: c.query_day_ahead_prices(DE_LU, start=START, end=END),
    "A65_A01_load_forecast": lambda c: c.query_load_forecast(DE_LU, start=START, end=END, process_type="A01"),
    "A69_A01_vre_forecast": lambda c: c.query_wind_and_solar_forecast(DE_LU, start=START, end=END, process_type="A01"),
}


def main() -> None:
    client = get_client()
    evidence = {"probe": "q5_archive_depth", "window": {"start": str(START), "end": str(END)}, "series": {}}

    print(f"Window: {START} -> {END}\n")
    for name, fn in SERIES.items():
        try:
            data = fn(client)
            print(f"{name:24s} OK  n={len(data):4d}  {data.index[0]} .. {data.index[-1]}")
            evidence["series"][name] = {"status": "OK", **to_pairs(data, n=4)}
        except NoMatchingDataError:
            print(f"{name:24s} NO_DATA")
            evidence["series"][name] = {"status": "NO_DATA"}
        except Exception as e:  # noqa: BLE001
            print(f"{name:24s} ERROR: {type(e).__name__}: {e}")
            evidence["series"][name] = {"status": "ERROR", "error": f"{type(e).__name__}: {e}"}

    out = write_evidence("q5_archive_depth", evidence)
    print(f"\nEvidence written to {out}")


if __name__ == "__main__":
    main()
