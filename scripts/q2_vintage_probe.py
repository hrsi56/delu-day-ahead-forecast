"""Q2 -- R-2 VRE/load forecast vintage probe (capstone S5.2, S11, S0 item 3).

Question: does the ENTSO-E Transparency Platform archive the as-published
D-1 day-ahead forecasts (A65/A01 load, A69/A01 wind+solar), or overwrite them
with later revisions?

Three subcommands:

  explore   One-shot, same-session diagnostic: checks how revisionNumber and
            data availability behave across delivery dates from 2019 to
            "tomorrow". No cross-day comparison -- just characterizes the
            metadata the API exposes.

  snapshot  Pulls A65/A01 and A69/A01 for a given delivery date *now* and
            saves the full series + revisionNumber + wall-clock pull time to
            data/spike/vintage/<delivery_date>__<pulled_at>.json. Run this
            once now, and again later (next session, a day+ apart) for the
            same delivery date.

  compare   Loads all snapshots for a given delivery date and diffs them
            pairwise: value deltas + revisionNumber changes. This is the
            re-run step that produces the definitive verdict.

Usage:
  uv run scripts/q2_vintage_probe.py explore
  uv run scripts/q2_vintage_probe.py snapshot --delivery-date 2026-06-13
  uv run scripts/q2_vintage_probe.py compare --delivery-date 2026-06-13
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import pandas as pd
from entsoe.exceptions import NoMatchingDataError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from spike.entsoe_helpers import (
    DE_LU,
    EVIDENCE_DIR,
    get_client,
    get_raw_client,
    series_to_dict,
    to_pairs,
    write_evidence,
)

VINTAGE_DIR = EVIDENCE_DIR / "vintage"


def _revision_info(raw_xml: str) -> dict:
    return {
        "revisionNumber": re.findall(r"<revisionNumber>(.*?)</revisionNumber>", raw_xml),
        "createdDateTime": re.findall(r"<createdDateTime>(.*?)</createdDateTime>", raw_xml),
        "n_timeseries": raw_xml.count("<TimeSeries>"),
        "psr_types": re.findall(r"<psrType>(.*?)</psrType>", raw_xml),
    }


def cmd_explore() -> None:
    """Same-session characterization: revisionNumber pattern across delivery
    dates 2019->tomorrow, and same-day availability of load vs VRE forecast."""
    client = get_client()
    raw = get_raw_client()

    rows = []
    for delivery_date, label in [
        ("2026-06-13", "D+1 (tomorrow, may be pre-VRE-deadline)"),
        ("2026-06-11", "D-1 (yesterday)"),
        ("2026-06-05", "D-7"),
        ("2026-05-13", "D-30"),
        ("2025-06-12", "D-365"),
        ("2019-01-15", "near archive start"),
    ]:
        start = pd.Timestamp(delivery_date, tz="Europe/Berlin")
        end = start + pd.Timedelta(days=1)
        row = {"delivery_date": delivery_date, "label": label}
        try:
            xml = raw.query_load_forecast(DE_LU, start=start, end=end, process_type="A01")
            row["load_fc"] = _revision_info(xml)
            row["load_fc"]["status"] = "OK"
        except NoMatchingDataError:
            row["load_fc"] = {"status": "NO_DATA"}
        except Exception as e:  # noqa: BLE001
            row["load_fc"] = {"status": f"ERROR: {type(e).__name__}: {e}"}
        try:
            xml = raw.query_wind_and_solar_forecast(DE_LU, start=start, end=end, process_type="A01")
            row["vre_fc"] = _revision_info(xml)
            row["vre_fc"]["status"] = "OK"
        except NoMatchingDataError:
            row["vre_fc"] = {"status": "NO_DATA"}
        except Exception as e:  # noqa: BLE001
            row["vre_fc"] = {"status": f"ERROR: {type(e).__name__}: {e}"}
        rows.append(row)
        print(delivery_date, label)
        print("  load_fc:", row["load_fc"])
        print("  vre_fc :", row["vre_fc"])

    # Same-pull-twice stability check on a settled day (sanity check only).
    settled = "2026-06-05"
    start = pd.Timestamp(settled, tz="Europe/Berlin")
    end = start + pd.Timedelta(days=1)
    s1 = client.query_wind_and_solar_forecast(DE_LU, start=start, end=end, process_type="A01")
    s2 = client.query_wind_and_solar_forecast(DE_LU, start=start, end=end, process_type="A01")
    identical = s1.equals(s2)
    print(f"\nRepeat-pull stability for {settled} VRE forecast: identical={identical}")

    evidence = {
        "probe": "q2_explore",
        "by_delivery_date": rows,
        "repeat_pull_stability": {"delivery_date": settled, "identical": bool(identical)},
    }
    out = write_evidence("q2_explore", evidence)
    print(f"\nEvidence written to {out}")


def cmd_snapshot(delivery_date: str) -> None:
    client = get_client()
    raw = get_raw_client()
    start = pd.Timestamp(delivery_date, tz="Europe/Berlin")
    end = start + pd.Timedelta(days=1)
    pulled_at = pd.Timestamp.now(tz="UTC")

    snapshot = {
        "delivery_date": delivery_date,
        "pulled_at_utc": str(pulled_at),
    }

    try:
        load_fc = client.query_load_forecast(DE_LU, start=start, end=end, process_type="A01")
        xml = raw.query_load_forecast(DE_LU, start=start, end=end, process_type="A01")
        snapshot["load_fc"] = {
            "status": "OK",
            "revision": _revision_info(xml),
            "series": series_to_dict(load_fc),
        }
        print(f"load_fc: {len(load_fc)} rows, revision={snapshot['load_fc']['revision']['revisionNumber']}")
    except NoMatchingDataError:
        snapshot["load_fc"] = {"status": "NO_DATA"}
        print("load_fc: NO_DATA")

    try:
        vre_fc = client.query_wind_and_solar_forecast(DE_LU, start=start, end=end, process_type="A01")
        xml = raw.query_wind_and_solar_forecast(DE_LU, start=start, end=end, process_type="A01")
        snapshot["vre_fc"] = {
            "status": "OK",
            "revision": _revision_info(xml),
            "series": series_to_dict(vre_fc),
        }
        print(f"vre_fc: {len(vre_fc)} rows, revision={snapshot['vre_fc']['revision']['revisionNumber']}")
    except NoMatchingDataError:
        snapshot["vre_fc"] = {"status": "NO_DATA"}
        print("vre_fc: NO_DATA (VRE forecast deadline is 18:00 Brussels D-1 -- may not be published yet)")

    VINTAGE_DIR.mkdir(parents=True, exist_ok=True)
    fname = f"{delivery_date}__{pulled_at.strftime('%Y%m%dT%H%M%SZ')}.json"
    out = VINTAGE_DIR / fname
    import json

    out.write_text(json.dumps(snapshot, indent=2, default=str))
    print(f"Snapshot written to {out}")


def cmd_compare(delivery_date: str) -> None:
    import json

    files = sorted(VINTAGE_DIR.glob(f"{delivery_date}__*.json"))
    if len(files) < 2:
        print(f"Need >=2 snapshots for {delivery_date} to compare; found {len(files)}.")
        print("Run `snapshot` again later (a different day is best) and re-run `compare`.")
        return

    snaps = [json.loads(f.read_text()) for f in files]
    report = {"delivery_date": delivery_date, "n_snapshots": len(snaps), "files": [f.name for f in files], "pairs": []}

    for i in range(len(snaps) - 1):
        a, b = snaps[i], snaps[i + 1]
        pair = {"from": a["pulled_at_utc"], "to": b["pulled_at_utc"]}
        for key in ("load_fc", "vre_fc"):
            a_block, b_block = a.get(key, {}), b.get(key, {})
            if a_block.get("status") != "OK" or b_block.get("status") != "OK":
                pair[key] = {"a_status": a_block.get("status"), "b_status": b_block.get("status")}
                continue
            a_series, b_series = a_block["series"], b_block["series"]
            common = sorted(set(a_series) & set(b_series))
            diffs = []
            for ts in common:
                av, bv = a_series[ts], b_series[ts]
                if isinstance(av, dict):
                    for col in av:
                        if av.get(col) != b_series[ts].get(col):
                            diffs.append((ts, col, av.get(col), b_series[ts].get(col)))
                elif av != bv:
                    diffs.append((ts, None, av, bv))
            pair[key] = {
                "a_revision": a_block["revision"]["revisionNumber"],
                "b_revision": b_block["revision"]["revisionNumber"],
                "n_common_points": len(common),
                "n_differing_points": len(diffs),
                "sample_diffs": diffs[:5],
            }
        report["pairs"].append(pair)
        print(f"{a['pulled_at_utc']} -> {b['pulled_at_utc']}")
        for key in ("load_fc", "vre_fc"):
            print(f"  {key}: {pair[key]}")

    out = write_evidence(f"q2_compare_{delivery_date}", report)
    print(f"\nComparison written to {out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("explore")
    p_snap = sub.add_parser("snapshot")
    p_snap.add_argument("--delivery-date", required=True, help="YYYY-MM-DD, local (Europe/Berlin) delivery day")
    p_cmp = sub.add_parser("compare")
    p_cmp.add_argument("--delivery-date", required=True)

    args = parser.parse_args()
    if args.cmd == "explore":
        cmd_explore()
    elif args.cmd == "snapshot":
        cmd_snapshot(args.delivery_date)
    elif args.cmd == "compare":
        cmd_compare(args.delivery_date)
