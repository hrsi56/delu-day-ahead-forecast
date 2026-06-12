"""Q6 -- ENTSO-E <-> SMARD cross-pull, day-ahead price (capstone S3, CP-1 reconciliation gate).

Pulls the same sample window's DA price from ENTSO-E (A44, hourly-averaged
since this window is post-MTU-transition) and from SMARD's keyless JSON API
(filter 4169 = day-ahead prices, region DE-LU, hourly resolution), aligns on
UTC timestamp, and reports agreement.

The formal CP-1 gate (>99.9% of overlapping hours within EUR 0.01/MWh) is
M1's job over the full history; here we demonstrate the cross-pull works and
sample prices match.

Usage: uv run scripts/q6_smard_cross.py
"""
from __future__ import annotations

import sys
from datetime import timezone
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from spike.entsoe_helpers import DE_LU, get_client, write_evidence

SMARD_FILTER_DA_PRICE = 4169
SMARD_REGION = "DE-LU"


def fetch_smard_hourly_prices(start_utc: pd.Timestamp, end_utc: pd.Timestamp) -> pd.Series:
    idx = requests.get(
        f"https://www.smard.de/app/chart_data/{SMARD_FILTER_DA_PRICE}/{SMARD_REGION}/index_hour.json", timeout=15
    ).json()
    timestamps = idx["timestamps"]

    # Pick chunks whose ~weekly span overlaps [start_utc, end_utc].
    chunk_ms = 7 * 24 * 3600 * 1000
    needed = [t for t in timestamps if t <= int(end_utc.timestamp() * 1000) and t + chunk_ms >= int(start_utc.timestamp() * 1000)]

    rows = []
    for t in needed:
        url = f"https://www.smard.de/app/chart_data/{SMARD_FILTER_DA_PRICE}/{SMARD_REGION}/{SMARD_FILTER_DA_PRICE}_{SMARD_REGION}_hour_{t}.json"
        data = requests.get(url, timeout=15).json()
        for ts_ms, val in data["series"]:
            ts = pd.Timestamp(ts_ms, unit="ms", tz="UTC")
            if start_utc <= ts <= end_utc and val is not None:
                rows.append((ts, val))

    s = pd.Series({ts: val for ts, val in rows}).sort_index()
    return s


def main() -> None:
    client = get_client()

    # 4-day window, fully in the past, safely non-null on both sides.
    start_local = pd.Timestamp("2026-06-08", tz="Europe/Berlin")
    end_local = pd.Timestamp("2026-06-12", tz="Europe/Berlin")

    entsoe_prices = client.query_day_ahead_prices(DE_LU, start=start_local, end=end_local)
    # Drop any partial hourly bin at the pull-window edge (the requested
    # `end` lands exactly on a quarter-hour, contributing a single point to
    # what would otherwise be a 4-point hourly bin -- a pull-boundary
    # artifact, not a data issue; see docs/spike-feed-status.md Q6).
    bin_sizes = entsoe_prices.resample("1h").size()
    complete_bins = bin_sizes[bin_sizes == 4].index
    entsoe_hourly = entsoe_prices.resample("1h").mean().loc[complete_bins]
    entsoe_hourly_utc = entsoe_hourly.tz_convert("UTC")
    n_dropped = len(bin_sizes) - len(complete_bins)
    print(f"ENTSO-E: {len(entsoe_prices)} raw rows -> {len(entsoe_hourly_utc)} complete hourly bins (UTC), dropped {n_dropped} partial bin(s) at pull edge")

    start_utc = start_local.tz_convert("UTC")
    end_utc = end_local.tz_convert("UTC")
    smard_hourly = fetch_smard_hourly_prices(start_utc, end_utc)
    print(f"SMARD  : {len(smard_hourly)} hourly rows (UTC)")

    common = entsoe_hourly_utc.index.intersection(smard_hourly.index)
    diff = (entsoe_hourly_utc.loc[common] - smard_hourly.loc[common]).abs()
    n_common = len(common)
    n_within_1c = int((diff <= 0.01).sum())
    pct_within_1c = 100 * n_within_1c / n_common if n_common else 0.0

    print(f"\nCommon hours: {n_common}")
    print(f"Within EUR 0.01/MWh: {n_within_1c}/{n_common} ({pct_within_1c:.2f}%)")
    print(f"Max abs diff: {diff.max():.6f} EUR/MWh, mean abs diff: {diff.mean():.6f} EUR/MWh")

    comparison = pd.DataFrame({
        "entsoe": entsoe_hourly_utc.loc[common],
        "smard": smard_hourly.loc[common],
        "abs_diff": diff,
    })
    print("\nHead:\n", comparison.head(6))
    print("\nTail:\n", comparison.tail(6))
    if diff.max() > 0.01:
        worst = comparison.sort_values("abs_diff", ascending=False).head(5)
        print("\nLargest diffs:\n", worst)

    evidence = {
        "probe": "q6_smard_cross",
        "window_local": {"start": str(start_local), "end": str(end_local)},
        "n_entsoe_raw": len(entsoe_prices),
        "n_entsoe_hourly": len(entsoe_hourly_utc),
        "n_partial_bins_dropped_at_pull_edge": n_dropped,
        "n_smard_hourly": len(smard_hourly),
        "n_common_hours": n_common,
        "n_within_1c": n_within_1c,
        "pct_within_1c": pct_within_1c,
        "max_abs_diff": float(diff.max()),
        "mean_abs_diff": float(diff.mean()),
        "sample": {str(k): {"entsoe": float(comparison.loc[k, "entsoe"]), "smard": float(comparison.loc[k, "smard"])} for k in list(common)[:6]},
    }
    out = write_evidence("q6_smard_cross", evidence)
    print(f"\nEvidence written to {out}")


if __name__ == "__main__":
    main()
