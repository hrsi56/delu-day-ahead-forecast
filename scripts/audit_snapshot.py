#!/usr/bin/env python3
"""Recompute the CP-1 snapshot, feature, and partition acceptance properties."""

from __future__ import annotations

import hashlib
import json
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

from delu_forecast.features import AUGMENTED_FEATURES, BASE_FEATURES, build_feature_catalog, residual_proxy_details
from delu_forecast.ingest import BERLIN, SERIES_SPECS
from delu_forecast.partitions import serializable_partition_spec
from delu_forecast.schema import validate_champion_runtime_schema

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "data" / "snapshot.parquet"


def main() -> None:
    digest = hashlib.sha256(SNAPSHOT.read_bytes()).hexdigest()
    recorded = (ROOT / "data" / "snapshot.sha256").read_text(encoding="utf-8").split()[0]
    manifest = json.loads((ROOT / "data" / "source_manifest.json").read_text(encoding="utf-8"))
    assert digest == recorded == manifest["snapshot_sha256"]

    frame = pd.read_parquet(SNAPSHOT)
    frame["timestamp_utc"] = pd.to_datetime(frame["timestamp_utc"], utc=True)
    assert frame["timestamp_utc"].is_unique and frame["timestamp_utc"].is_monotonic_increasing
    expected_index = pd.date_range(frame["timestamp_utc"].min(), frame["timestamp_utc"].max(), freq="h", tz="UTC")
    assert frame["timestamp_utc"].equals(pd.Series(expected_index, name="timestamp_utc"))
    assert min(frame["delivery_date"]) == date(2019, 1, 1)
    cutoff = max(frame["delivery_date"])
    assert cutoff == date.fromisoformat(manifest["snapshot_cutoff_delivery_date"])
    assert not frame["price_eur_mwh"].isna().any()

    local = frame["timestamp_utc"].dt.tz_convert(BERLIN)
    assert (local.dt.date == frame["delivery_date"]).all()
    assert (local.dt.hour == frame["local_hour"]).all()
    identities = pd.MultiIndex.from_frame(frame[["delivery_date", "local_hour", "utc_offset_minutes"]])
    assert identities.is_unique
    for delivery_day, count in frame.groupby("delivery_date").size().items():
        expected = int(
            (
                pd.Timestamp(delivery_day + timedelta(days=1), tz=BERLIN).tz_convert("UTC")
                - pd.Timestamp(delivery_day, tz=BERLIN).tz_convert("UTC")
            ).total_seconds()
            // 3600
        )
        assert count == expected

    transition = frame["delivery_date"] >= date(2025, 10, 1)
    assert frame.loc[transition, "price_source_interval_count"].eq(4).all()
    assert frame.loc[~transition, "price_source_interval_count"].eq(1).all()
    for spec in SERIES_SPECS[1:]:
        counts = frame[f"{spec.column}_source_quarter_count"]
        values = frame[spec.column]
        assert values.loc[counts.isin((1, 2, 3))].isna().all()
        assert values.loc[counts.eq(4)].notna().all()

    partition_file = json.loads((ROOT / "data" / "partitions.json").read_text(encoding="utf-8"))
    expected_partitions = serializable_partition_spec(cutoff)
    assert partition_file == expected_partitions
    assert date.fromisoformat(partition_file["tail_partitions"]["fold_5"]["start"]) >= date(2025, 10, 1)

    sample_path = ROOT / "data" / "reconciliation_sample.json"
    reconciliation = json.loads((ROOT / "data" / "reconciliation_summary.json").read_text(encoding="utf-8"))
    assert reconciliation["sample_spec_sha256"] == hashlib.sha256(sample_path.read_bytes()).hexdigest()
    assert reconciliation["result"] == manifest["reconciliation"]["status"] == "pass"
    assert reconciliation["fraction_within_tolerance"] >= 0.999
    comparison = pd.read_csv(ROOT / "data" / "reconciliation.csv")
    assert len(comparison) == reconciliation["overlapping_hours"] == 120
    assert comparison["abs_diff_eur_mwh"].le(reconciliation["tolerance_eur_mwh"] + 1e-12).all()
    assert {
        "pre_crisis",
        "crisis_peak",
        "post_crisis",
        "pt60m_boundary_side",
        "pt15m_boundary_side",
    } == set(comparison["stratum"])

    base = build_feature_catalog(frame, "base")
    augmented = build_feature_catalog(frame, "base_plus_residual_load_proxy")
    assert tuple(base.columns) == BASE_FEATURES
    assert tuple(augmented.columns) == AUGMENTED_FEATURES
    assert tuple(augmented.columns[:-1]) == tuple(base.columns)
    validate_champion_runtime_schema(base.columns, "base")
    validate_champion_runtime_schema(augmented.columns, "base_plus_residual_load_proxy")
    proxy = residual_proxy_details(frame)
    valid_proxy = proxy["vre_norm"].notna()
    delivery_by_timestamp = frame.set_index("timestamp_utc")["delivery_date"]
    latest_allowed = delivery_by_timestamp.loc[proxy.index[valid_proxy]].map(lambda value: value - timedelta(days=2))
    assert (proxy.loc[valid_proxy, "window_end_delivery_date"].to_numpy() <= latest_allowed.to_numpy()).all()

    report_dir = ROOT / "reports"
    for figure in ("fig_welch_periodogram.png", "fig_per_regime_periodogram.png", "fig_acf_24_168.png"):
        assert (report_dir / figure).stat().st_size > 10_000
    peak_bins = pd.read_csv(report_dir / "spectral_peak_bins.csv")
    assert {24, 168, 12} == set(peak_bins["period_hours"])
    assert (peak_bins["bin_error"] <= peak_bins["fft_bin_width"]).all()

    result = {
        "snapshot_sha256": digest,
        "rows": len(frame),
        "utc_start": frame["timestamp_utc"].min().isoformat(),
        "utc_end": frame["timestamp_utc"].max().isoformat(),
        "delivery_date_start": str(min(frame["delivery_date"])),
        "delivery_date_cutoff": str(cutoff),
        "price_nulls": int(frame["price_eur_mwh"].isna().sum()),
        "local_day_row_counts": frame.groupby("delivery_date").size().value_counts().sort_index().to_dict(),
        "base_columns": len(base.columns),
        "base_complete_rows": int(base.notna().all(axis=1).sum()),
        "augmented_columns": len(augmented.columns),
        "augmented_complete_rows": int(augmented.notna().all(axis=1).sum()),
        "a65_head_gap_observed_hours": manifest["a65_head_gap_observed_hours"],
        "fold_5_start": partition_file["tail_partitions"]["fold_5"]["start"],
        "reconciliation_status": manifest["reconciliation"]["status"],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
