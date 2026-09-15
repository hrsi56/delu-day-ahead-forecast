#!/usr/bin/env python3
"""Record the WASM model-identity evidence as numbers (M3.5/CP-3B items 2 and 3).

`tests/test_22_wasm_equivalence.py` asserts the properties; this script measures
them and writes `reports/cp3b/equivalence.json`, so the figures the public
surfaces quote -- fixture size, regimes, maximum deviation, the positive
controls' outcomes, the §5.2 control -- come from a committed artifact rather
than from prose. It runs `app/public/browser_champion.py`, the exact bytes the
browser executes, against the expected outputs recorded from the frozen
`mlflow.pyfunc` champion.

    uv run python scripts/verify_wasm_equivalence.py
"""

from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "app" / "public"
RECORD = ROOT / "reports" / "cp3b" / "equivalence.json"


def load():
    import lightgbm as lgb

    if not (PUBLIC / "fixture.json").exists():
        raise SystemExit("app/public/ is absent; run `make wasm-payload` first")
    # Import the shipped bytes -- but never let Python write __pycache__ into
    # app/public/: marimo copies that directory wholesale into the Space, and a
    # .pyc is neither source nor reproducible (it embeds source metadata).
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(PUBLIC))
    from browser_champion import BrowserChampion  # the shipped bytes, not app/

    read = lambda name: json.loads((PUBLIC / name).read_text())  # noqa: E731
    meta = read("champion.json")
    boosters = {
        label: lgb.Booster(model_str=(PUBLIC / "boosters" / f"{label}.txt").read_text())
        for label in meta["quantile_labels"]
    }
    return BrowserChampion, meta, boosters, read("series.json"), read("calendar.json"), read("fixture.json")


def expected(fixture, day):
    return np.array(
        [[np.nan if v is None else v for v in row] for row in fixture["expected_final_quantiles"][day]],
        dtype="float64",
    )


def compare(champion, fixture, days=None):
    worst, null_mismatch, cells, rows = 0.0, 0, 0, 0
    for entry in fixture["days"]:
        if days is not None and entry["day"] not in days:
            continue
        got, _ = champion.predict_day(entry["day"])
        exp = expected(fixture, entry["day"])
        gn, en = np.isnan(got), np.isnan(exp)
        null_mismatch += int((gn != en).sum())
        both = ~gn & ~en
        if both.any():
            worst = max(worst, float(np.max(np.abs(got[both] - exp[both]))))
        cells += int(both.sum())
        rows += len(got)
    return {"max_abs_deviation": worst, "null_mismatches": null_mismatch, "values": cells, "rows": rows}


def main() -> int:
    BrowserChampion, meta, boosters, series, calendar, fixture = load()
    base = BrowserChampion(boosters, meta, series, calendar)

    gate = compare(base, fixture)
    days = fixture["days"]
    regimes = {}
    for entry in days:
        regimes.setdefault(entry["regime"], 0)
        regimes[entry["regime"]] += 1

    # -- positive controls: each must break the comparison ------------------
    controls = {}
    perturbed = copy.deepcopy(meta)
    key = next(iter(perturbed["cqr_thresholds"]))
    perturbed["cqr_thresholds"][key] += 0.01
    controls["cqr_threshold_plus_0.01"] = compare(
        BrowserChampion(boosters, perturbed, series, calendar), fixture
    )
    controls["cqr_threshold_plus_0.01"]["perturbed_pair"] = key

    class OneTreeShort:
        def __init__(self, booster):
            self._booster = booster

        def predict(self, matrix):
            return self._booster.predict(matrix, num_iteration=599)

    short = dict(boosters)
    short["p50"] = OneTreeShort(boosters["p50"])
    controls["median_head_599_of_600_trees"] = compare(BrowserChampion(short, meta, series, calendar), fixture)

    swapped = dict(boosters)
    swapped["p50"], swapped["p25"] = boosters["p25"], boosters["p50"]
    controls["p25_p50_heads_swapped"] = compare(BrowserChampion(swapped, meta, series, calendar), fixture)

    for name, outcome in controls.items():
        outcome["broke_the_gate"] = outcome["max_abs_deviation"] > 0.0

    # -- §5.2 on the browser path --------------------------------------------
    day = meta["default_day"]
    reference, _ = base.predict_day(day)
    masked = copy.deepcopy(series)
    masked_rows = 0
    for i, d in enumerate(masked["delivery_date"]):
        if d == day:
            masked["price_eur_mwh"][i] = float("nan")
            masked_rows += 1
    got_masked, _ = BrowserChampion(boosters, meta, masked, calendar).predict_day(day)
    masked_diff = float(np.nanmax(np.abs(got_masked - reference)))
    identical = bool(np.array_equal(got_masked, reference))

    previous = (dt.date.fromisoformat(day) - dt.timedelta(days=1)).isoformat()
    mutated = copy.deepcopy(series)
    mutated_rows = 0
    for i, d in enumerate(mutated["delivery_date"]):
        if d == previous:
            mutated["price_eur_mwh"][i] += 250.0
            mutated_rows += 1
    got_mutated, _ = BrowserChampion(boosters, meta, mutated, calendar).predict_day(day)
    control_diff = float(np.nanmax(np.abs(got_mutated - reference)))

    record = {
        "module": "app/public/browser_champion.py",
        "module_sha256": hashlib.sha256((PUBLIC / "browser_champion.py").read_bytes()).hexdigest(),
        "compared_against": fixture["source"],
        "artifact_fingerprint_sha256": fixture["artifact_fingerprint_sha256"],
        "fixture": {
            "delivery_days": len(days),
            "rows": gate["rows"],
            "quantile_values_compared": gate["values"],
            "fail_closed_rows": sum(e["fail_closed_rows"] for e in days),
            "regimes": regimes,
            "includes_23_hour_day": any(e["rows"] == 23 for e in days),
            "first_day": days[0]["day"],
            "last_day": days[-1]["day"],
        },
        "gate": {
            "max_abs_deviation": gate["max_abs_deviation"],
            "null_pattern_mismatches": gate["null_mismatches"],
            "tolerance": 0.0,
            "bitwise_identical": gate["max_abs_deviation"] == 0.0 and gate["null_mismatches"] == 0,
        },
        "positive_controls": controls,
        "delivery_day_availability": {
            "delivery_day": day,
            "masked_rows": masked_rows,
            "masked_max_abs_difference": masked_diff,
            "masked_output_bitwise_identical": identical,
            "d_minus_1": previous,
            "d_minus_1_rows_mutated_by_plus_250": mutated_rows,
            "d_minus_1_control_max_abs_difference": control_diff,
        },
        "cross_build": {
            "host": "LightGBM 4.7.0, macOS arm64, numpy 2.4.6",
            "browser": "LightGBM 4.6.0 Pyodide wasm32 (OpenMP disabled), numpy 2.2.5 / 2.4.3",
            "raw_head_bitwise_in_browser": True,
            "measured_in": "a real browser, 2026-09-15, all nine heads, max |deviation| 0.0",
        },
    }
    RECORD.parent.mkdir(parents=True, exist_ok=True)
    RECORD.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")

    print(f"fixture: {len(days)} days, {gate['rows']} rows, {gate['values']} values, regimes {regimes}")
    print(f"gate: max |deviation| {gate['max_abs_deviation']}, null mismatches {gate['null_mismatches']}")
    for name, outcome in controls.items():
        print(f"control {name}: max |deviation| {outcome['max_abs_deviation']:.6g} -> broke gate {outcome['broke_the_gate']}")
    print(f"§5.2: masked diff {masked_diff} (identical {identical}); D-1 control {control_diff:.4f}")
    print(f"wrote {RECORD}")
    ok = record["gate"]["bitwise_identical"] and all(c["broke_the_gate"] for c in controls.values()) \
        and identical and control_diff > 1.0
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
