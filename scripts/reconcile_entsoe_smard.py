#!/usr/bin/env python3
"""Run the pre-pinned ENTSO-E↔SMARD A44 reconciliation sample safely."""

from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
from entsoe import EntsoePandasClient

from delu_forecast.ingest import BERLIN

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_PATH = ROOT / "data" / "reconciliation_sample.json"


def _hourly_entsoe_price(raw: pd.Series, delivery_day: date) -> pd.Series:
    if raw.index.tz is None:
        raise ValueError("ENTSO-E returned a naive timestamp index")
    start_local = pd.Timestamp(delivery_day, tz=BERLIN)
    end_local = pd.Timestamp(delivery_day + timedelta(days=1), tz=BERLIN)
    day = raw.loc[(raw.index >= start_local) & (raw.index < end_local)].tz_convert("UTC")
    if day.isna().any() or day.empty:
        raise ValueError("ENTSO-E day is empty or contains nulls")
    frame = day.rename("value").to_frame()
    frame["hour_utc"] = frame.index.floor("h")
    sizes = frame.groupby("hour_utc")["value"].size()
    invalid = ~sizes.isin((1, 4))
    if invalid.any():
        raise ValueError("ENTSO-E returned an incomplete hourly/quarter-hour bin")
    hourly = frame.groupby("hour_utc")["value"].mean()
    expected_hours = int((end_local.tz_convert("UTC") - start_local.tz_convert("UTC")).total_seconds() // 3600)
    if len(hourly) != expected_hours:
        raise ValueError("ENTSO-E delivery-day hour count does not match Berlin identity")
    hourly.name = "entsoe_eur_mwh"
    hourly.index.name = "timestamp_utc"
    return hourly


def main() -> int:
    token = os.environ.get("ENTSOE_API_TOKEN")
    if not token:
        print("ENTSOE_API_TOKEN is not set", file=sys.stderr)
        return 2
    sample = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
    snapshot = pd.read_parquet(ROOT / "data" / "snapshot.parquet")
    snapshot["timestamp_utc"] = pd.to_datetime(snapshot["timestamp_utc"], utc=True)
    smard = snapshot.set_index("timestamp_utc")["price_eur_mwh"]
    client = EntsoePandasClient(api_key=token)

    comparisons: list[pd.DataFrame] = []
    for item in sample["delivery_days"]:
        delivery_day = date.fromisoformat(item["delivery_date"])
        start = pd.Timestamp(delivery_day, tz=BERLIN)
        end = pd.Timestamp(delivery_day + timedelta(days=1), tz=BERLIN)
        try:
            raw = client.query_day_ahead_prices("DE_LU", start=start, end=end)
            entsoe = _hourly_entsoe_price(raw, delivery_day)
        except Exception:
            # entsoe-py embeds the security token in request URLs and exception
            # text. Suppress the exception object rather than risking a leak.
            print(f"ENTSO-E query failed for {delivery_day}; exception details suppressed", file=sys.stderr)
            return 3
        smard_day = smard.reindex(entsoe.index)
        if smard_day.isna().any():
            print(f"SMARD snapshot lacks a sampled A44 row for {delivery_day}", file=sys.stderr)
            return 4
        frame = pd.DataFrame({"entsoe_eur_mwh": entsoe, "smard_eur_mwh": smard_day})
        frame["abs_diff_eur_mwh"] = (frame["entsoe_eur_mwh"] - frame["smard_eur_mwh"]).abs()
        frame.insert(0, "delivery_date", delivery_day.isoformat())
        frame.insert(1, "stratum", item["stratum"])
        comparisons.append(frame.reset_index())
        print(f"Reconciled {delivery_day}: {len(frame)} hourly rows")

    comparison = pd.concat(comparisons, ignore_index=True)
    tolerance = float(sample["tolerance_eur_mwh"])
    within = comparison["abs_diff_eur_mwh"].le(tolerance + 1e-12)
    fraction = float(within.mean())
    passed = fraction >= float(sample["required_fraction_within_tolerance"])
    comparison.to_csv(ROOT / "data" / "reconciliation.csv", index=False, float_format="%.6f")
    summary = {
        "schema_version": 1,
        "sample_spec_sha256": hashlib.sha256(SAMPLE_PATH.read_bytes()).hexdigest(),
        "sample_days": len(sample["delivery_days"]),
        "overlapping_hours": len(comparison),
        "hours_within_tolerance": int(within.sum()),
        "fraction_within_tolerance": fraction,
        "tolerance_eur_mwh": tolerance,
        "max_abs_diff_eur_mwh": float(comparison["abs_diff_eur_mwh"].max()),
        "mean_abs_diff_eur_mwh": float(comparison["abs_diff_eur_mwh"].mean()),
        "result": "pass" if passed else "fail",
    }
    summary_path = ROOT / "data" / "reconciliation_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest_path = ROOT / "data" / "source_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["reconciliation"] = {
        "status": summary["result"],
        "sample_spec": "data/reconciliation_sample.json",
        "comparison": "data/reconciliation.csv",
        "summary": "data/reconciliation_summary.json",
        "overlapping_hours": summary["overlapping_hours"],
        "fraction_within_tolerance": summary["fraction_within_tolerance"],
        "max_abs_diff_eur_mwh": summary["max_abs_diff_eur_mwh"],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if passed else 5


if __name__ == "__main__":
    raise SystemExit(main())
