"""Q4 -- 15-minute price boundary across 2025-10-01 (capstone S0 item 4, S4.0, R-4, invariant test 4).

Sample pull of A44 (DE-LU day-ahead price) spanning 2025-09-28 -> 2025-10-04.
Confirms:
  1. entsoe-py's date-switched resolution: hourly before 2025-10-01, 15-min after.
  2. Hourly-averaged series is continuous across the boundary -- no gap, no
     duplicate.
  3. Each post-transition hourly value equals the mean of its four
     quarter-hours.

Usage: uv run scripts/q4_15min_boundary.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from spike.entsoe_helpers import DE_LU, MTU_TRANSITION_DATE, get_client, to_pairs, write_evidence


def main() -> None:
    client = get_client()
    start = pd.Timestamp("2025-09-28", tz="Europe/Berlin")
    end = pd.Timestamp("2025-10-04", tz="Europe/Berlin")

    prices = client.query_day_ahead_prices(DE_LU, start=start, end=end)
    print(f"Raw pull: {len(prices)} rows, {prices.index[0]} .. {prices.index[-1]}")

    transition = pd.Timestamp(MTU_TRANSITION_DATE, tz="Europe/Berlin")
    pre = prices[prices.index < transition]
    post = prices[prices.index >= transition]
    pre_freq = pd.infer_freq(pre.index)
    post_freq = pd.infer_freq(post.index)
    print(f"Pre-transition  ({pre.index[0]} .. {pre.index[-1]}): n={len(pre)}, freq={pre_freq}")
    print(f"Post-transition ({post.index[0]} .. {post.index[-1]}): n={len(post)}, freq={post_freq}")

    # Hourly-average the post-transition quarter-hours, then concat with the
    # (already hourly) pre-transition series.
    post_hourly = post.resample("1h").mean()
    combined = pd.concat([pre, post_hourly]).sort_index()

    # Invariant checks.
    full_range = pd.date_range(combined.index[0], combined.index[-1], freq="1h", tz="Europe/Berlin")
    # DST: Europe/Berlin Oct-2025 has a fall-back day (2025-10-26) with 25
    # local hours -- date_range with tz-aware freq="1h" handles this
    # correctly (25 entries that day), so missing/duplicate checks below are
    # DST-safe for this window (the window ends well before Oct 26 anyway).
    missing = full_range.difference(combined.index)
    duplicated = combined.index[combined.index.duplicated()]
    no_gap_no_dup = len(missing) == 0 and len(duplicated) == 0

    # Post-transition hourly == mean of its 4 quarter-hours, spot-checked.
    spot_checks = []
    for ts in post_hourly.index[:8]:
        quarter_hours = post[(post.index >= ts) & (post.index < ts + pd.Timedelta(hours=1))]
        manual_mean = quarter_hours.mean()
        spot_checks.append({
            "hour": str(ts),
            "n_quarter_hours": len(quarter_hours),
            "hourly_value": round(float(post_hourly.loc[ts]), 6),
            "manual_mean_of_quarters": round(float(manual_mean), 6),
            "match": bool(abs(post_hourly.loc[ts] - manual_mean) < 1e-9),
        })

    print(f"\nContinuity across boundary: missing={len(missing)}, duplicated={len(duplicated)} -> no_gap_no_dup={no_gap_no_dup}")
    print("Spot checks (post-transition hourly == mean of 4 quarter-hours):")
    for c in spot_checks:
        print(f"  {c['hour']}: hourly={c['hourly_value']:.4f} mean_of_quarters={c['manual_mean_of_quarters']:.4f} match={c['match']}")

    print("\nLast pre-transition hours and first post-transition (hourly-avg) hours:")
    print(pre.tail(3))
    print(post_hourly.head(3))

    evidence = {
        "probe": "q4_15min_boundary",
        "window": {"start": str(start), "end": str(end)},
        "raw": to_pairs(prices, n=4),
        "pre_transition": {"n": len(pre), "inferred_freq": str(pre_freq), "last_rows": to_pairs(pre, n=3)["tail"]},
        "post_transition_raw": {"n": len(post), "inferred_freq": str(post_freq), "first_rows": to_pairs(post, n=4)["head"]},
        "post_transition_hourly_avg": {"n": len(post_hourly), "first_rows": to_pairs(post_hourly, n=3)["head"]},
        "continuity": {
            "n_missing_hours": len(missing),
            "n_duplicated_hours": len(duplicated),
            "no_gap_no_dup": no_gap_no_dup,
        },
        "spot_checks_hourly_eq_mean_of_quarters": spot_checks,
        "all_spot_checks_match": all(c["match"] for c in spot_checks),
    }
    out = write_evidence("q4_15min_boundary", evidence)
    print(f"\nEvidence written to {out}")


if __name__ == "__main__":
    main()
