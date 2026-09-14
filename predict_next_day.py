#!/usr/bin/env python3
"""Standalone next-day inference for the frozen champion (§9.2).

Ships inside the container for local development and cold-start regeneration. It
is **not** the user-facing artifact -- that is the static page and the marimo
Space -- and nothing in the release calls it at request time.

Two modes:

* **bundled** (default, offline): the champion and `data/snapshot.parquet` are
  read from the image. No network, no registry, no token. This is the mode the
  release uses.
* **fresh**: pulls the feeds the *selected* catalog needs from SMARD -- lagged
  A44 day-ahead prices and the A65/A01 load forecast, plus 42 trailing days of
  A75 aggregate actual generation when the loaded champion's catalog is
  `base_plus_residual_load_proxy`. The shipped champion selected `base` at CP-2,
  so the A75 feed is not fetched for it; the code path exists and reports which
  feeds it used rather than claiming three unconditionally.

In both modes the forecast frame is assembled by
`delu_forecast.showcase.gate_feasible_frame`, which drops every row dated after
the delivery day and masks the delivery day's own prices. No price whose
delivery date is D or later reaches a feature for D (§5.2).
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
if str(ROOT / "src") not in sys.path and (ROOT / "src").is_dir():
    sys.path.insert(0, str(ROOT / "src"))

from delu_forecast.claims import build_claims  # noqa: E402
from delu_forecast.postprocess import QUANTILE_LABELS  # noqa: E402
from delu_forecast.showcase import (  # noqa: E402
    DEFAULT_MODEL_PATH,
    DEFAULT_SNAPSHOT_PATH,
    INTERVAL_LEVELS,
    actuals_for_day,
    default_target_day,
    delivery_days,
    forecast_delivery_day,
    gate_feasible_frame,
    load_champion,
    load_snapshot,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="predict_next_day.py",
        description="Forecast one DE-LU delivery day from the frozen bundled champion.",
    )
    parser.add_argument(
        "--date",
        type=date.fromisoformat,
        default=None,
        help="delivery day to forecast (YYYY-MM-DD). Default: the last day the source can serve.",
    )
    parser.add_argument(
        "--source",
        choices=("bundled", "fresh"),
        default="bundled",
        help="bundled = the committed snapshot in the image (offline, default); fresh = pull from SMARD.",
    )
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL_PATH)
    parser.add_argument("--snapshot", type=Path, default=DEFAULT_SNAPSHOT_PATH)
    parser.add_argument(
        "--level",
        type=int,
        choices=sorted(INTERVAL_LEVELS),
        default=80,
        help="nominal interval level printed beside the median.",
    )
    parser.add_argument(
        "--load-scale",
        type=float,
        default=1.0,
        help="ceteris-paribus sensitivity probe on the delivery day's load forecast (1.0 = none).",
    )
    parser.add_argument("--json", type=Path, default=None, help="also write the full nine-quantile result here.")
    parser.add_argument(
        "--self-check",
        action="store_true",
        help="run the delivery-day boundary check (masked == unmasked, and a D-1 positive control).",
    )
    return parser.parse_args(argv)


def fresh_snapshot(target_day: date, catalog: str) -> tuple[pd.DataFrame, list[str]]:
    """Pull the feeds the selected catalog needs, history through D-1 plus D's A65."""
    from delu_forecast.ingest import (
        BERLIN,
        SERIES_SPECS,
        TRANSITION_LOCAL_DATE,
        aggregate_quarterhours,
        assemble_price_series,
        fetch_smard_series,
    )

    needed = {"price_eur_mwh", "load_forecast_mw"}
    if catalog == "base_plus_residual_load_proxy":
        needed |= {"wind_onshore_actual_mw", "solar_actual_mw", "wind_offshore_actual_mw"}

    # 720 canonical hourly price observations plus the D-7 lag; 60 days is a wide
    # margin, and the 42-day A75 window fits inside it too.
    start_local = pd.Timestamp(target_day - timedelta(days=60), tz=BERLIN)
    end_local = pd.Timestamp(target_day + timedelta(days=1), tz=BERLIN)
    start_utc, end_utc = start_local.tz_convert("UTC"), end_local.tz_convert("UTC")
    transition_utc = pd.Timestamp(TRANSITION_LOCAL_DATE, tz=BERLIN).tz_convert("UTC")

    series: dict[str, pd.Series] = {}
    used: list[str] = []
    for spec in SERIES_SPECS:
        if spec.column not in needed:
            continue
        if spec.column == "price_eur_mwh":
            pre = (
                fetch_smard_series(spec, start_utc, min(end_utc, transition_utc), resolution="hour")
                if start_utc < transition_utc
                else pd.DataFrame(columns=["timestamp_utc", "value"])
            )
            post = (
                fetch_smard_series(spec, max(start_utc, transition_utc), end_utc, resolution="quarterhour")
                if end_utc > transition_utc
                else pd.DataFrame(columns=["timestamp_utc", "value"])
            )
            series[spec.column] = assemble_price_series(pre, post)
        else:
            raw = fetch_smard_series(spec, start_utc, end_utc, resolution="quarterhour")
            series[spec.column] = aggregate_quarterhours(raw, spec, fail_on_partial=False)
        used.append(f"{spec.plan_series} ({spec.smard_label})")

    # Assembled here rather than through `ingest.build_snapshot`, which refuses null
    # prices -- right for the frozen archive, wrong at the gate, where the delivery
    # day's prices have not cleared yet.
    frame = pd.concat(series.values(), axis=1).sort_index()
    frame.index.name = "timestamp_utc"
    local = frame.index.tz_convert(BERLIN)
    frame.insert(0, "delivery_date", pd.Index(local.date))
    frame.insert(1, "local_hour", local.hour.astype("int8"))
    if catalog == "base_plus_residual_load_proxy":
        frame["vre_actual_mw"] = frame[
            ["wind_onshore_actual_mw", "wind_offshore_actual_mw", "solar_actual_mw"]
        ].sum(axis=1, min_count=3)
    # The frozen snapshot stores every measured column as float64; the live
    # assembly can hand back `object` where two source eras meet, and LightGBM
    # refuses an object column rather than silently coercing it.
    for column in frame.columns:
        if column not in {"delivery_date", "local_hour"}:
            frame[column] = pd.to_numeric(frame[column], errors="coerce").astype("float64")
    return frame.reset_index(), used


def self_check(model, snapshot: pd.DataFrame, target_day: date) -> dict[str, object]:
    """The delivery-day boundary, proved rather than asserted.

    Two halves, because only the second makes the first meaningful:

    * **masked == unmasked** -- forecasting D with D's own prices present gives
      bitwise the same nine quantiles as forecasting it with them removed. If any
      feature reached into D, removing D would move the output.
    * **positive control** -- mutating an eligible in-window D-1 price *must*
      move the output. A check that only ever asserts "nothing changed" is
      satisfied by a broken model that returns a constant.
    """
    masked = forecast_delivery_day(model, snapshot, target_day)

    unmasked = snapshot.copy()
    frame = gate_feasible_frame(unmasked, target_day, catalog=model.catalog)
    on_target = pd.Index(frame["delivery_date"].to_numpy()) == target_day
    frame.loc[on_target, "price_eur_mwh"] = actuals_for_day(snapshot, target_day).to_numpy()
    stages = model.predict_stages(frame)
    with_day_prices = stages["final"][on_target]

    mutated = snapshot.copy()
    previous = pd.Index(mutated["delivery_date"].to_numpy()) == (target_day - timedelta(days=1))
    mutated.loc[previous, "price_eur_mwh"] = mutated.loc[previous, "price_eur_mwh"] + 250.0
    control = forecast_delivery_day(model, mutated, target_day)

    quantiles = list(QUANTILE_LABELS)
    identical = np.array_equal(masked[quantiles].to_numpy(), with_day_prices)
    moved = not np.array_equal(masked[quantiles].to_numpy(), control[quantiles].to_numpy())
    return {
        "delivery_day": target_day.isoformat(),
        "rows_checked": int(len(masked)),
        "delivery_day_prices_change_nothing": bool(identical),
        "positive_control_d_minus_1_changes_output": bool(moved),
        "max_abs_difference_when_masked": float(
            np.nanmax(np.abs(masked[quantiles].to_numpy() - with_day_prices))
        ),
        "max_abs_difference_positive_control": float(
            np.nanmax(np.abs(masked[quantiles].to_numpy() - control[quantiles].to_numpy()))
        ),
        "passed": bool(identical and moved),
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    claims = build_claims()
    model = load_champion(args.model)

    feeds = ["bundled data/snapshot.parquet (no network)"]
    if args.source == "fresh":
        target = args.date or (date.today() + timedelta(days=1))
        snapshot, feeds = fresh_snapshot(target, model.catalog)
    else:
        snapshot = load_snapshot(args.snapshot)
        target = args.date or default_target_day(snapshot)

    available = set(delivery_days(snapshot))
    if target not in available:
        print(
            f"error: {target} is not in the source. Available: "
            f"{min(available)} .. {max(available)}",
            file=sys.stderr,
        )
        return 2

    forecast = forecast_delivery_day(model, snapshot, target, load_scale=args.load_scale)
    low, high = INTERVAL_LEVELS[args.level]

    holdout_start, holdout_end = (date.fromisoformat(value) for value in claims["holdout_window"].split(".."))
    in_holdout = holdout_start <= target <= holdout_end

    print(f"DE-LU day-ahead forecast — delivery day {target}")
    print(f"  champion        : {claims['selected_catalog']} catalog, "
          f"{claims['champion_quantiles']} quantile heads, CQR then isotonic")
    print(f"  fingerprint     : {claims['champion_fingerprint']}")
    print(f"  source          : {', '.join(feeds)}")
    print(f"  cutoffs         : snapshot {claims['snapshot_cutoff']} · raw-model fit "
          f"{claims['raw_model_fit_cutoff']} · final calibration {claims['final_calibration_window']} "
          f"· holdout {claims['holdout_window']}")
    if in_holdout:
        print(f"  label           : {claims['replay_label']}")
    if args.load_scale != 1.0:
        print(f"  scenario        : load forecast x{args.load_scale:.2f}. {claims['sensitivity_probe_label']}")
    print()
    print(f"  {'hour':>4}  {low:>9}  {'p50':>9}  {high:>9}"
          + ("  " + f"{'actual':>9}" if in_holdout else ""))
    actual = actuals_for_day(snapshot, target) if in_holdout else None
    for _, row in forecast.iterrows():
        line = (f"  {int(row['local_hour']):>4}  {row[low]:>9.2f}  {row['p50']:>9.2f}  {row[high]:>9.2f}")
        if actual is not None:
            observed = actual.get(int(row["local_hour"]), float("nan"))
            line += f"  {observed:>9.2f}"
        print(line)
    print()
    print(f"  {args.level}% nominal; the frozen champion's empirical coverage at this level over the "
          f"{claims['holdout_days']}-day holdout was {claims['holdout_coverage_' + str(args.level)]}.")
    print(f"  {claims['shipped_is_evaluated']}")

    if args.self_check:
        result = self_check(model, snapshot, target)
        print()
        print("  delivery-day boundary self-check:")
        for key, value in result.items():
            print(f"    {key}: {value}")
        if not result["passed"]:
            return 1

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "delivery_day": target.isoformat(),
            "catalog": model.catalog,
            "artifact_fingerprint_sha256": claims["champion_fingerprint"],
            "snapshot_sha256": claims["snapshot_sha256"],
            "cutoffs": {
                key: claims[key]
                for key in ("snapshot_cutoff", "raw_model_fit_cutoff", "final_calibration_window", "holdout_window")
            },
            "source": feeds,
            "load_scale": args.load_scale,
            "historical_out_of_sample_replay": in_holdout,
            "quantiles": [
                {"local_hour": int(row["local_hour"]), **{label: float(row[label]) for label in QUANTILE_LABELS}}
                for _, row in forecast.iterrows()
            ],
        }
        args.json.write_text(json.dumps(payload, indent=2) + "\n")
        print(f"\n  wrote {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
