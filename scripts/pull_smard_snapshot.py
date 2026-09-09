#!/usr/bin/env python3
"""Build the frozen CP-1 Parquet snapshot from SMARD fallback-primary data."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date, datetime, timezone
from pathlib import Path

import pandas as pd

from delu_forecast.ingest import (
    BERLIN,
    SERIES_SPECS,
    TRANSITION_LOCAL_DATE,
    aggregate_quarterhours,
    assemble_price_series,
    build_snapshot,
    fetch_smard_series,
    quarterhour_source_counts,
    series_manifest,
    write_parquet,
)
from delu_forecast.partitions import serializable_partition_spec

ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cutoff", type=date.fromisoformat, default=date(2026, 9, 6))
    parser.add_argument("--workers", type=int, default=12)
    parser.add_argument("--output", type=Path, default=ROOT / "data" / "snapshot.parquet")
    return parser.parse_args()


def _coverage(series: pd.Series) -> dict[str, object]:
    valid = series.dropna()
    return {
        "rows": int(len(series)),
        "non_null_rows": int(series.notna().sum()),
        "null_rows": int(series.isna().sum()),
        "first_valid_utc": valid.index.min().isoformat() if len(valid) else None,
        "last_valid_utc": valid.index.max().isoformat() if len(valid) else None,
    }


def main() -> None:
    args = parse_args()
    start_local = pd.Timestamp(date(2019, 1, 1), tz=BERLIN)
    end_local = pd.Timestamp(args.cutoff + pd.Timedelta(days=1), tz=BERLIN)
    start_utc = start_local.tz_convert("UTC")
    end_utc = end_local.tz_convert("UTC")
    transition_utc = pd.Timestamp(TRANSITION_LOCAL_DATE, tz=BERLIN).tz_convert("UTC")

    series: dict[str, pd.Series] = {}
    source_counts: dict[str, pd.Series] = {}
    price_spec = SERIES_SPECS[0]
    print("Fetching A44 hourly-product era from SMARD...")
    price_pre = fetch_smard_series(
        price_spec, start_utc, min(end_utc, transition_utc), resolution="hour", workers=args.workers
    )
    if end_utc > transition_utc:
        print("Fetching A44 quarter-hour-product era from SMARD...")
        price_post = fetch_smard_series(
            price_spec, transition_utc, end_utc, resolution="quarterhour", workers=args.workers
        )
    else:
        price_post = pd.DataFrame(columns=["timestamp_utc", "value"])
    series[price_spec.column] = assemble_price_series(price_pre, price_post)
    price_counts = pd.Series(1, index=series[price_spec.column].index, dtype="int8")
    if not price_post.empty:
        price_counts.loc[quarterhour_source_counts(price_post).index] = quarterhour_source_counts(price_post)
    price_counts.name = "price_source_interval_count"
    source_counts[price_counts.name] = price_counts

    for spec in SERIES_SPECS[1:]:
        print(f"Fetching {spec.plan_series} / {spec.smard_label} (filter {spec.filter_id})...")
        raw = fetch_smard_series(spec, start_utc, end_utc, resolution="quarterhour", workers=args.workers)
        # Non-target feeds fail closed to NaN for partial source bins. The
        # source-count column and manifest retain the evidence so downstream
        # completeness filtering cannot mistake a 1--3-quarter sum for data.
        hourly = aggregate_quarterhours(raw, spec, fail_on_partial=False)
        series[spec.column] = hourly
        counts = quarterhour_source_counts(raw).rename(f"{spec.column}_source_quarter_count")
        source_counts[counts.name] = counts

    snapshot = build_snapshot(series | source_counts)
    expected_index = series[price_spec.column].index
    snapshot = snapshot.reindex(expected_index)
    snapshot.index.name = "timestamp_utc"
    write_parquet(snapshot, args.output)
    digest = hashlib.sha256(args.output.read_bytes()).hexdigest()
    hash_path = args.output.with_suffix(".sha256")
    hash_path.write_text(f"{digest}  {args.output.name}\n", encoding="utf-8")

    manifest = {
        "schema_version": 1,
        "ingestion_route": "SMARD fallback-primary",
        "route_reason": "ENTSO-E External API unavailable during the 2026-09-08 pull; capstone v6.7 section 3 authorizes SMARD fallback-primary.",
        "pulled_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "requested_start_delivery_date": "2019-01-01",
        "snapshot_cutoff_delivery_date": args.cutoff.isoformat(),
        "snapshot_sha256": digest,
        "license": "CC BY 4.0",
        "attribution": "Data: ENTSO-E Transparency Platform; Bundesnetzagentur | SMARD.de — CC BY 4.0.",
        "mapping_authority": "https://www.smard.de/app/chart_configuration/market_data_configuration.json",
        "series_mapping": series_manifest(),
        "coverage": {name: _coverage(value.reindex(expected_index)) for name, value in series.items()},
        "source_bin_integrity": {
            name: {
                "hours_with_four_non_null_quarters": int(value.reindex(expected_index).eq(4).sum()),
                "hours_with_zero_non_null_quarters": int(value.reindex(expected_index).eq(0).sum()),
                "partial_hours_fail_closed_to_null": int(value.reindex(expected_index).isin((1, 2, 3)).sum()),
            }
            for name, value in source_counts.items()
            if name != "price_source_interval_count"
        },
        "a65_head_gap_observed_hours": int(series["load_forecast_mw"].reindex(expected_index).isna().cumprod().sum()),
        "reconciliation": {
            "status": "open",
            "reason": "ENTSO-E External API unavailable; a fixed stratified cross-source comparison cannot be evidenced from one source.",
        },
    }
    manifest_path = args.output.parent / "source_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    partitions_path = args.output.parent / "partitions.json"
    partitions_path.write_text(
        json.dumps(serializable_partition_spec(args.cutoff), indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"snapshot": str(args.output), "sha256": digest, "rows": len(snapshot)}, indent=2))


if __name__ == "__main__":
    main()
