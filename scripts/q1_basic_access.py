"""Q1 -- End-to-end access probe.

Confirms entsoe-py (>=0.7.5, pinned) authenticates against the ENTSO-E
Transparency Platform with ENTSOE_API_TOKEN and returns DE-LU day-ahead
price data. Notes any 403/429/migration weirdness (capstone R-3).

Usage: uv run scripts/q1_basic_access.py
"""
from __future__ import annotations

import sys

import pandas as pd

sys.path.insert(0, str(__file__.rsplit("/", 2)[0] + "/src"))
from spike.entsoe_helpers import DE_LU, get_client, to_pairs, write_evidence


def main() -> None:
    client = get_client()
    end = pd.Timestamp.now(tz="Europe/Berlin").normalize() + pd.Timedelta(days=1)
    start = end - pd.Timedelta(days=5)

    evidence = {"probe": "q1_basic_access", "query": {"start": str(start), "end": str(end), "area": DE_LU}}
    try:
        prices = client.query_day_ahead_prices(DE_LU, start=start, end=end)
        evidence["status"] = "VERIFIED"
        evidence["summary"] = to_pairs(prices, n=6)
        print(f"OK -- {len(prices)} rows, {prices.index[0]} .. {prices.index[-1]}")
        print(f"Inferred freq: {pd.infer_freq(prices.index)}")
        print(prices.head(6))
        print(prices.tail(6))
    except Exception as e:  # noqa: BLE001 -- probe script, capture everything for the memo
        evidence["status"] = "FAILED"
        evidence["error_type"] = type(e).__name__
        evidence["error"] = str(e)
        print(f"FAILED: {type(e).__name__}: {e}", file=sys.stderr)

    out = write_evidence("q1_basic_access", evidence)
    print(f"Evidence written to {out}")


if __name__ == "__main__":
    main()
