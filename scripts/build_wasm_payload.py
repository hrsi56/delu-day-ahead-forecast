#!/usr/bin/env python3
"""Assemble the browser payload for the WASM showcase (M3.5/CP-3B).

`mlflow.pyfunc` does not load under Pyodide, so the browser runs a
re-implementation: the nine raw boosters as LightGBM text, the base catalog's
preprocessing re-expressed in notebook code, the four CQR thresholds, isotonic
last. Nothing about the model changes -- only where it executes.

What ships, and why each piece is data rather than code:

* `boosters/<label>.txt` -- the nine boosters, `model_to_string()`. Verified
  lossless: a text round-trip reproduces `LGBMRegressor.predict` bitwise on the
  host, and Pyodide's LightGBM reproduces it bitwise too (that measurement is the
  reason this checkpoint is possible at all).
* `champion.json` -- catalog, feature order, the four CQR thresholds, the
  fingerprint, the four cutoffs. Read, never recomputed.
* `series.json` -- the price and load-forecast rows the features are built from,
  carrying `delivery_date` and `local_hour` as the snapshot already computed
  them, so the browser never converts a timezone.
* `calendar.json` -- per delivery day, the UTC epoch hour of its Berlin midnight
  (the D-1 rolling boundary) and the German federal holidays in range. Calendar
  facts are inputs; the feature logic that consumes them is re-expressed in the
  notebook.
* `fixture.json` -- the equivalence fixture: every target day's expected nine
  final quantiles, from the frozen `mlflow.pyfunc` champion. The browser
  recomputes and compares.

The windows are chosen to span all three regimes plus a DST transition, and each
carries 31 days of prior history so the 720-hour rolling window and the D-7 lag
resolve inside the shipped slice rather than falling off its edge.
"""

from __future__ import annotations

import json
import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from delu_forecast.claims import build_claims  # noqa: E402
from delu_forecast.ingest import BERLIN  # noqa: E402
from delu_forecast.postprocess import QUANTILE_LABELS  # noqa: E402
from delu_forecast.schema import catalog_columns  # noqa: E402
from delu_forecast.showcase import (  # noqa: E402
    forecast_delivery_day,
    load_champion,
    load_snapshot,
)

OUT = ROOT / "app" / "public"
MANIFEST = ROOT / "reports" / "cp3b" / "payload.json"

#: 720 canonical hourly observations is 30 delivery days; the D-7 lag needs seven
#: more. 31 days of history is the smallest margin that covers both, and keeping
#: it small keeps the payload honest.
HISTORY_DAYS = 31

#: Target days, chosen to span the three regimes §2 names and a DST transition.
WINDOWS: tuple[tuple[str, date, date], ...] = (
    ("pre-crisis", date(2020, 7, 1), date(2020, 7, 12)),
    ("crisis", date(2022, 8, 1), date(2022, 8, 12)),
    # Round-1 review broke the bridge-day logic and the gate still passed: the
    # fixture held no holiday. These windows exercise every calendar branch -- a
    # Monday bridge before a Tuesday holiday, Friday bridges after Thursday
    # holidays, holidays, and days after holidays.
    ("post-crisis (holidays, bridge days)", date(2023, 10, 2), date(2023, 10, 4)),
    ("post-crisis (holidays, bridge days)", date(2024, 12, 25), date(2024, 12, 27)),
    ("post-crisis (holidays, bridge days)", date(2025, 5, 29), date(2025, 5, 30)),
    # Both DST directions: the 25-hour day, and the two days after it whose
    # calendar-day lags land on the repeated hour and must fail closed.
    ("dst-fall-back", date(2025, 10, 26), date(2025, 10, 28)),
    ("dst-spring-forward", date(2026, 3, 25), date(2026, 3, 31)),
    ("post-crisis (holdout)", date(2026, 8, 26), date(2026, 9, 6)),
)

#: The expected outputs are a committed artifact, not a by-product of the build.
#: The build recomputes them from the frozen champion and refuses to continue if
#: they differ -- so a changed model cannot silently regenerate its own answer
#: key. `--refresh-fixture` rewrites it, deliberately and visibly in git.
COMMITTED_FIXTURE = ROOT / "tests" / "fixtures" / "wasm_equivalence_fixture.json"

#: The day the app renders by default: the last in the snapshot, inside the
#: holdout window, so what it shows is a labelled historical out-of-sample replay.
DEFAULT_DAY = date(2026, 9, 6)


def target_days() -> list[tuple[str, date]]:
    days = []
    for regime, start, end in WINDOWS:
        day = start
        while day <= end:
            days.append((regime, day))
            day += timedelta(days=1)
    return days


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "boosters").mkdir(exist_ok=True)
    import shutil

    for stale in list(OUT.rglob("__pycache__")):
        shutil.rmtree(stale, ignore_errors=True)
    champion = load_champion()
    snapshot = load_snapshot()
    claims = build_claims()

    # -- the nine boosters, as text ----------------------------------------
    # Base64 of gzip, as text. Two measured platform facts decide the format
    # (live Static Spaces, 2026-09-15). First, Hugging Face serves Static Spaces
    # uncompressed, so shipped compression is the only compression a visitor
    # gets. Second, binary files are stored through Xet and served as a
    # `302 cache-control: no-store` to us.aws.cdn.hf.co with a signed URL that
    # changes on every request -- so a browser can never cache them, and binary
    # gzip boosters would be re-downloaded (11.1 MB) on every visit. Base64 keeps
    # the file ASCII text, which the platform serves directly with an ETag: 3.7 MB
    # more on a first visit, nothing on a repeat one. Lossless either way; the
    # equivalence gate proves the decoded model bitwise. mtime=0 keeps bytes
    # reproducible.
    import base64
    import gzip

    for stale in list((OUT / "boosters").glob("*.txt")) + list((OUT / "boosters").glob("*.txt.gz")):
        stale.unlink()
    booster_bytes, booster_gz_bytes, booster_b64_bytes = {}, {}, {}
    for label in QUANTILE_LABELS:
        text = champion.heads[label].booster_.model_to_string().encode()
        compressed = gzip.compress(text, compresslevel=9, mtime=0)
        encoded = base64.b64encode(compressed)
        (OUT / "boosters" / f"{label}.txt.gz.b64").write_bytes(encoded)
        booster_bytes[label] = len(text)
        booster_gz_bytes[label] = len(compressed)
        booster_b64_bytes[label] = len(encoded)

    # -- champion metadata, read and never recomputed ----------------------
    (OUT / "champion.json").write_text(
        json.dumps(
            {
                "catalog": champion.catalog,
                "features": list(catalog_columns(champion.catalog)),
                "quantile_labels": list(QUANTILE_LABELS),
                "cqr_thresholds": {f"{lo}|{hi}": v for (lo, hi), v in champion.thresholds.items()},
                "artifact_fingerprint_sha256": claims["champion_fingerprint"],
                "snapshot_sha256": claims["snapshot_sha256"],
                "cutoffs": {
                    k: claims[k]
                    for k in (
                        "snapshot_cutoff",
                        "raw_model_fit_cutoff",
                        "final_calibration_window",
                        "holdout_window",
                    )
                },
                "default_day": DEFAULT_DAY.isoformat(),
            },
            indent=1,
            sort_keys=True,
        )
        + "\n"
    )

    # -- the row slice the features are built from -------------------------
    days = target_days()
    keep = set()
    for _, day in days:
        start = day - timedelta(days=HISTORY_DAYS)
        current = start
        while current <= day:
            keep.add(current)
            current += timedelta(days=1)
    dates = pd.Index(snapshot["delivery_date"].to_numpy())
    rows = snapshot.loc[[d in keep for d in dates]].sort_values("timestamp_utc")

    # The snapshot index is datetime64[ms]; going through seconds explicitly
    # avoids inheriting whatever unit the column happens to carry, which is
    # how the first build silently produced an all-NaN feature matrix.
    epoch_hours = np.array(
        [int(ts.timestamp()) // 3600 for ts in pd.to_datetime(rows["timestamp_utc"], utc=True)],
        dtype="int64",
    )
    (OUT / "series.json").write_text(
        json.dumps(
            {
                "epoch_hour": [int(v) for v in epoch_hours],
                "delivery_date": [d.isoformat() for d in rows["delivery_date"]],
                "local_hour": [int(v) for v in rows["local_hour"]],
                "price_eur_mwh": [float(v) for v in rows["price_eur_mwh"]],
                "load_forecast_mw": [float(v) for v in rows["load_forecast_mw"]],
            },
            separators=(",", ":"),
        )
        + "\n"
    )

    # -- calendar facts: the D-1 boundary, and the holidays ----------------
    covered = sorted(keep)
    boundaries = {
        day.isoformat(): int(pd.Timestamp(day, tz=BERLIN).tz_convert("UTC").timestamp() // 3600)
        for day in covered
    }
    import holidays as holidays_pkg

    years = sorted({day.year for day in covered} | {day.year - 1 for day in covered})
    german = holidays_pkg.country_holidays("DE", years=years)
    (OUT / "calendar.json").write_text(
        json.dumps(
            {
                "berlin_midnight_epoch_hour": boundaries,
                "federal_holidays": sorted(d.isoformat() for d in german.keys()),
                "note": (
                    "Calendar facts are inputs. The feature logic that consumes them -- "
                    "is_federal_holiday, is_day_after_holiday, is_bridge_day, day_type -- is "
                    "re-expressed in the notebook and proved equal to the frozen pipeline."
                ),
            },
            indent=1,
            sort_keys=True,
        )
        + "\n"
    )

    # -- the claim set, so the browser retypes nothing ---------------------
    # The WASM page is another public surface. It renders every number from the
    # same dict the README, the Pages export, the Space card and the MLflow
    # record render from; `tests/test_22` asserts this file equals build_claims()
    # exactly, so the page cannot drift from them.
    (OUT / "claims.json").write_text(
        json.dumps(dict(claims.values), indent=1, sort_keys=True) + "\n"
    )

    # -- the module the browser executes -----------------------------------
    # Shipped as data so the notebook fetches exactly the bytes
    # tests/test_22_wasm_equivalence.py imported and checked. Two copies that can
    # drift is how a browser ends up running code nothing verified.
    import hashlib

    module_source = (ROOT / "app" / "browser_champion.py").read_bytes()
    (OUT / "browser_champion.py").write_bytes(module_source)
    module_digest = hashlib.sha256(module_source).hexdigest()

    # -- the equivalence fixture: what the frozen champion says ------------
    expected, per_day = {}, []
    for regime, day in days:
        forecast = forecast_delivery_day(champion, snapshot, day)
        matrix = forecast[list(QUANTILE_LABELS)].to_numpy(dtype="float64")
        # A null here is not a defect: on the spring-forward day the D-1
        # calendar-day lag has no source hour, so the feature is unavailable and
        # the pipeline fails closed rather than inventing a price. The browser
        # must reproduce the null pattern exactly, which makes this the strictest
        # row in the fixture rather than one to drop.
        null_rows = int((~np.isfinite(matrix)).any(axis=1).sum())
        expected[day.isoformat()] = [
            [None if value != value else float(value) for value in row] for row in matrix
        ]
        per_day.append(
            {
                "day": day.isoformat(),
                "regime": regime,
                "rows": int(len(matrix)),
                "fail_closed_rows": null_rows,
                "local_hours": [int(v) for v in forecast["local_hour"]],
            }
        )
    fresh = (
        json.dumps(
            {
                "source": "frozen mlflow.pyfunc champion, models/champion/",
                "artifact_fingerprint_sha256": claims["champion_fingerprint"],
                "days": per_day,
                "expected_final_quantiles": expected,
            },
            separators=(",", ":"),
        )
        + "\n"
    )
    if "--refresh-fixture" in sys.argv or not COMMITTED_FIXTURE.exists():
        COMMITTED_FIXTURE.parent.mkdir(parents=True, exist_ok=True)
        COMMITTED_FIXTURE.write_text(fresh)
        print(f"wrote the committed fixture {COMMITTED_FIXTURE.relative_to(ROOT)}")
    elif COMMITTED_FIXTURE.read_text() != fresh:
        raise SystemExit(
            "the frozen champion no longer reproduces tests/fixtures/wasm_equivalence_fixture.json "
            "— the model or the fixture changed. Nothing is assembled. If the change is intended, "
            "re-run with --refresh-fixture and review the diff."
        )
    (OUT / "fixture.json").write_text(COMMITTED_FIXTURE.read_text())

    total_rows = sum(d["rows"] for d in per_day)
    fail_closed = sum(d["fail_closed_rows"] for d in per_day)
    # claims.json is excluded: scripts/build_wasm_space.py rewrites it last, from
    # the evidence the gate writes after this step, so a size recorded here could
    # only ever describe a file that is about to be replaced.
    sizes = {
        p.name: p.stat().st_size
        for p in sorted(OUT.rglob("*"))
        if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc" and p.name != "claims.json"
    }
    payload_bytes = sum(sizes.values())
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(
        json.dumps(
            {
                "payload_dir": str(OUT.relative_to(ROOT)),
                "browser_champion_sha256": module_digest,
                "uncompressed_bytes": payload_bytes,
                "booster_bytes": booster_bytes,
                "booster_gzip_bytes": booster_gz_bytes,
                "booster_base64_bytes": booster_b64_bytes,
                "file_bytes": sizes,
                "series_rows": int(len(rows)),
                "fixture_days": len(per_day),
                "fixture_rows": total_rows,
                "fixture_fail_closed_rows": fail_closed,
                "regimes": sorted({d["regime"] for d in per_day}),
                "history_days_per_window": HISTORY_DAYS,
                "default_day": DEFAULT_DAY.isoformat(),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    print(f"payload: {payload_bytes:,} bytes across {len(sizes)} files")
    print(f"  boosters: {sum(booster_bytes.values()):,} bytes as text, "
          f"{sum(booster_gz_bytes.values()):,} gzipped, {sum(booster_b64_bytes.values()):,} shipped as base64 text")
    print(f"  series:   {len(rows):,} rows")
    print(f"  fixture:  {len(per_day)} days / {total_rows} rows "
          f"({fail_closed} fail-closed) / regimes {sorted({d['regime'] for d in per_day})}")
    print(f"wrote {MANIFEST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
