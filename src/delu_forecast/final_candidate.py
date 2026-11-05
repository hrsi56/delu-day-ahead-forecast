"""A1, the final candidate, in v5's comparison: the same 10,747 hours, scored exactly as v5's policies were (PRES-5).

The Owner's decision 28 (2026-11-05) asks for DDNN-2 alone in the published comparison "on the same data they are
compared on there". This module puts A1 -- CP-28's selection, DDNN-2 alone with its own quantiles, frozen at CP-17c --
on v5's population without fitting anything:

- **A1's forecasts** are CP-28's stored hourly forecasts (`reports/cp28/forecast/hourly.parquet`, arm `A1`), read
  where they cover v5's keys. They cover all 10,747. Nothing is refitted, re-tuned or re-issued.
- **The population** is v5's own: CP-15's independent expected keys, the five test periods, the observed prices of
  v5's committed rows, the similar-day naive (B0) as the denominator, equal period weights.
- **The scores** are CP-24's: `cp22.scoring`'s validation, hourly losses (p50 MAE and the seven-quantile WIS),
  per-period tables, equal-fold B0 normalisation and CP-20's seed-15042, 2,000-replicate, 7-day paired block
  bootstrap, the same shared index set (its fingerprint is checked), with `cp24.scoring.with_level`'s 97.5%
  intervals beside the 95% ones.
- **The other policies are not recomputed for publication.** v5's and B0's rows on the page stay CP-24's committed
  rows. Their losses are recomputed here only to pair them with A1's, and `parity.json` records that every one of
  their per-period and equal-fold scores equals CP-24's committed value exactly.
- **v5's adoption rule is not re-run.** A1 against v5 and against B0 are descriptive paired comparisons with the
  rule's intervals; nothing here adopts, selects or ranks.

A1's information set differs from v5's, and `summary.json` states how (issue time, daily refits, its own searches,
the data identity, the CP-26 warm-up that contains the first period). The page says so wherever the row appears.

Run ``python -m delu_forecast.final_candidate`` to write `reports/pres5/a1-in-v5/`, or ``--check`` to compare.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = Path("reports/pres5/a1-in-v5")

#: The inputs, each pinned by SHA-256: the stored forecasts and their manifest (CP-28), v5's rows (CP-24), the saved
#: references B0 and v3 (CP-20) and the independent expected keys (CP-15).
INPUTS = {
    "reports/cp28/forecast/hourly.parquet": "f5cb02a19236edd20c182c2874a5d59628652e6838fe5745aa6ffacf3f53f638",
    "reports/cp28/forecast/arm-days.parquet": None,
    "reports/cp28/forecast/manifest.json": "f092140ed028d18a973bfad11ad9aa0397ad3e492223c4da683bc8e775cf3ce8",
    "reports/ddnn2/attempt-1/predictions.parquet": None,
    "reports/ddnn2/attempt-1/metrics.csv": None,
    "reports/weather-ablation/predictions.parquet": None,
    "reports/cp15/predictions.parquet": None,
}

#: A1's code in this comparison. CP-28 named the arm A1; the code is scoped to this publication's experiment.
CODE = "A1"
#: The policies this pass reads: B0 (the denominator and a comparator), v3 (`HG`, whose scale and level
#: `validate_predictions` checks every unsaved policy against), v5 and A1.
POLICIES = ("B0", "HG", "v5", CODE)
CONTRASTS = ((CODE, "v5", "final_candidate_vs_v5"), (CODE, "B0", "final_candidate_vs_naive"))
ARM_TO_P = {"q025": "p025", "q10": "p10", "q25": "p25", "q50": "p50", "q75": "p75", "q90": "p90", "q975": "p975"}
#: The CP-24 columns every table keeps, in CP-24's order.
COLS = ["fold", "policy", "timestamp_utc", "delivery_date", "y_true", "central", "scale", "level",
        "p025", "p10", "p25", "p50", "p75", "p90", "p975"]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _inputs(root: Path) -> dict[str, str]:
    out = {}
    for rel, expected in INPUTS.items():
        actual = sha256(root / rel)
        if expected is not None and actual != expected:
            raise ValueError(f"{rel}: SHA-256 {actual} is not the pinned {expected}")
        out[rel] = actual
    return out


def _ts(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, utc=True).dt.as_unit("ns")


def a1_rows(root: Path, v5: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """A1's stored forecasts on v5's keys, in CP-24's columns. The truth, scale and level are v5's rows' (the
    population's); scale and level are metadata that no score reads."""
    hourly = pd.read_parquet(root / "reports/cp28/forecast/hourly.parquet",
                             filters=[("arm", "==", "A1")])
    hourly["timestamp_utc"] = _ts(hourly.timestamp_utc)
    keyed = hourly.set_index("timestamp_utc")
    if keyed.index.has_duplicates:
        raise ValueError("A1's stored forecasts repeat a timestamp")
    base = v5.set_index("timestamp_utc")
    got = keyed.reindex(base.index)
    covered = got[list(ARM_TO_P)].notna().all(axis=1)
    out = base[["fold", "delivery_date", "y_true", "scale", "level"]].copy()
    out["central"] = got["native_central"].to_numpy(float)
    for arm, p in ARM_TO_P.items():
        out[p] = got[arm].to_numpy(float)
    out["policy"] = CODE
    out = out.reset_index()[COLS]
    days = pd.read_parquet(root / "reports/cp28/forecast/arm-days.parquet", filters=[("arm", "==", "A1")])
    days["day"] = days["day"].astype(str)
    on = days.set_index("day").reindex(sorted(v5.delivery_date.astype(str).str[:10].unique()))
    coverage = {
        "keys": int(len(base)), "covered_keys": int(covered.sum()),
        "per_fold": {fold: [int(covered[(base.fold == fold).to_numpy()].sum()), int((base.fold == fold).sum())]
                     for fold in sorted(base.fold.unique())},
        "days": int(len(on)),
        "output_source": {str(k): int(v) for k, v in on.output_source.value_counts().items()},
        "fallback_days": int(on.fallback.sum()),
        "scored_by_cp26_cp28": {str(k): int(v) for k, v in on.scored.value_counts().items()},
        "unscored_days": [str(d) for d in on.index[~on.scored.astype(bool)]][:1]
                         + [str(d) for d in on.index[~on.scored.astype(bool)]][-1:],
        "first_stored_forecast_day": str(hourly.loc[hourly.q50.notna(), "day"].astype(str).min()),
    }
    return out, coverage


def load(root: Path):
    """v5's committed rows (CP-24), the saved B0 and v3 rows (CP-20), A1's stored forecasts, and CP-15's keys."""
    saved = pd.read_parquet(root / "reports/weather-ablation/predictions.parquet")
    saved = saved.loc[saved.policy.isin(("B0", "HG"))][COLS]
    v5 = pd.read_parquet(root / "reports/ddnn2/attempt-1/predictions.parquet", filters=[("policy", "==", "v5")])[COLS]
    for frame in (saved, v5):
        frame["timestamp_utc"] = _ts(frame.timestamp_utc)
    a1, coverage = a1_rows(root, v5.copy())
    both = pd.concat([saved, v5, a1], ignore_index=True)
    expected = pd.read_parquet(root / "reports/cp15/predictions.parquet", columns=["fold", "timestamp_utc", "delivery_date"],
                               filters=[("policy", "==", "B0")])
    return both, expected, coverage


def score(root: Path) -> dict:
    """Every table, on v5's population, by CP-24's scoring blocks."""
    from cp20.scoring import _indices
    from cp22.scoring import BOOTSTRAP_REPLICATES, bootstrap, equal_fold_scores, hourly_scores, tables, validate_predictions
    from cp24.scoring import LEVEL_DECISION, with_level

    predictions, expected, coverage = load(root)
    if coverage["covered_keys"] != coverage["keys"]:
        raise ValueError(f"A1's stored forecasts cover {coverage['covered_keys']} of {coverage['keys']} keys")
    frame = validate_predictions(predictions, expected, list(POLICIES), production=True)
    hourly = hourly_scores(frame)
    metrics, _diagnostics, daily = tables(hourly, list(POLICIES))
    scores = equal_fold_scores(metrics, list(POLICIES))
    metrics = pd.concat([metrics, pd.DataFrame([dict(policy=p, fold="all", scope="equal_fold", **scores[p])
                                                for p in POLICIES])], ignore_index=True)
    indices = _indices(BOOTSTRAP_REPLICATES)
    uncertainty, draws, _replicate_scores, meta = bootstrap(daily, list(POLICIES), list(CONTRASTS), indices=indices)
    uncertainty = with_level(uncertainty, draws)
    # The ratio intervals at the decision level, from the same stored draws (cp24.ratios' rule).
    lo = (1 - LEVEL_DECISION) / 2
    eq = draws.loc[draws.scope.eq("equal_fold")]
    ratio_rows = []
    for (candidate, baseline, metric), part in eq.groupby(["candidate", "baseline", "metric"], sort=False):
        ratios = part.sort_values("replicate")["ratio"].to_numpy(float)
        row = uncertainty.loc[uncertainty.scope.eq("equal_fold") & uncertainty.candidate.eq(candidate)
                              & uncertainty.baseline.eq(baseline) & uncertainty.metric.eq(metric)].iloc[0]
        c95 = np.quantile(ratios, [.025, .975], method="linear")
        if (float(c95[0]), float(c95[1])) != (float(row.ratio_ci_lower), float(row.ratio_ci_upper)):
            raise ValueError(f"{candidate}-{baseline} {metric}: the draws do not give the bootstrap's 95% ratio interval")
        c975 = np.quantile(ratios, [lo, 1 - lo], method="linear")
        ratio_rows.append({"candidate": candidate, "baseline": baseline, "metric": metric, "role": row.role,
                           "defined": True, "replicates": int(len(ratios)), "ratio": float(row.ratio),
                           "ratio_ci95_lower": float(c95[0]), "ratio_ci95_upper": float(c95[1]),
                           "ratio_ci97.5_lower": float(c975[0]), "ratio_ci97.5_upper": float(c975[1])})
    ratios = pd.DataFrame(ratio_rows)
    return {"metrics": metrics, "uncertainty": uncertainty, "ratios": ratios, "scores": scores, "meta": meta,
            "coverage": coverage}


def parity(root: Path, metrics: pd.DataFrame) -> dict:
    """B0's, v3's and v5's recomputed per-period and equal-fold scores against CP-24's committed rows: equal, exactly."""
    committed = pd.read_csv(root / "reports/ddnn2/attempt-1/metrics.csv", float_precision="round_trip")
    out, worst = {}, 0.0
    for policy in ("B0", "HG", "v5"):
        mine = metrics.loc[metrics.policy.eq(policy)]
        theirs = committed.loc[committed.policy.eq(policy)]
        for scope, columns in (("per_fold", ("MAE", "WIS", "coverage95", "mean_width95")), ("pooled", ("MAE", "WIS")),
                               ("equal_fold", ("S_MAE", "S_WIS"))):
            a = mine.loc[mine.scope.eq(scope)].set_index("fold").sort_index()
            b = theirs.loc[theirs.scope.eq(scope)].set_index("fold").sort_index()
            if list(a.index) != list(b.index):
                raise ValueError(f"{policy} {scope}: folds differ from CP-24's committed rows")
            for column in columns:
                diff = float(np.max(np.abs(a[column].to_numpy(float) - b[column].to_numpy(float))))
                worst = max(worst, diff)
                out[f"{policy}.{scope}.{column}"] = diff
    return {"max_abs_difference": worst, "equal": worst == 0.0, "by_field": out,
            "against": "reports/ddnn2/attempt-1/metrics.csv",
            "meaning": "v5's, v3's and B0's rows on the page stay CP-24's committed rows; this records that the losses "
                       "paired with A1's here reproduce every one of their scores exactly"}


#: How A1's information set differs from v5's in these five periods (PUBLISH_RULES §3.2, the brief's outcome 1).
#: Each item names the record that establishes it.
INFORMATION_SET = (
    {"item": "issue time",
     "v5": "D-1 11:00 UTC, the origin of every record before research v21-r13 (capstone_v21.md §24.4)",
     "a1": "D-1 11:00 Europe/Berlin, one or two hours earlier, strictly before the 12:00 gate (§24.4)",
     "source": "capstone_v21.md §24.4; reports/ddnn2/attempt-1/predictions.parquet origin_utc"},
    {"item": "fitting",
     "v5": "CP-24's fold protocol: v5's members fitted for each test period from data before it",
     "a1": "refitted every day on the 728 days before the origin (fewer in 2020), filtered by availability at the "
           "issue time (§24.7, 'Training and information')",
     "source": "capstone_v21.md §24.7; reports/cp28/forecast/fits.parquet"},
    {"item": "network search",
     "v5": "CP-24's DDNN-2 search and ensemble, run inside its own protocol",
     "a1": "CP-26's training-only searches every 182 days from 2020-01-15, each serving only the origins after it; "
           "CP-24's ensembles are never reused (§24.7)",
     "source": "capstone_v21.md §24.7, 'DDNN-2's training-only search'"},
    {"item": "data identity and inputs",
     "v5": "the development snapshot as CP-24 read it",
     "a1": "CP-25's data identity, CP-20's and CP-25's weather grids and the registered input vintages (§24.5, §24.7)",
     "source": "capstone_v21.md §24.5 and §24.7, 'The harness'"},
    {"item": "the first period",
     "v5": "a scored test period",
     "a1": "2020-07-01 to 2020-09-28 lies in CP-26's unscored warm-up (2020-01-01 to 2020-12-28): A1's forecasts "
           "there exist and are stored, but CP-26 and CP-28 never scored them",
     "source": "capstone_v21.md §24.7, 'Days'; reports/cp28/forecast/arm-days.parquet scored"},
    {"item": "selection",
     "v5": "adopted on these five periods under cp24-adoption",
     "a1": "selected by CP-28 on CP-26's every-day calendar, which contains periods 2 to 5; DDNN-2 alone was "
           "already shown, descriptively, as the best single model there before CP-28 ran",
     "source": "reports/cp28/report.md; docs/track-b/cp-28-landing-2026-10-25.md"},
)


def summary(result: dict, inputs: dict[str, str], par: dict) -> dict:
    meta = result["meta"]
    return {
        "schema": "pres5-a1-in-v5-v1",
        "what": "A1, the final candidate, scored on v5's comparison population by CP-24's scoring blocks",
        "population": {"id": "common-10747h", "keys": result["coverage"]["keys"], "days": result["coverage"]["days"],
                       "periods": 5, "weights": "equal period weights", "denominator": "B0, the similar-day naive",
                       "truth": "the observed prices of v5's committed rows"},
        "coverage": result["coverage"],
        "information_set": list(INFORMATION_SET),
        "scores": {p: result["scores"][p] for p in POLICIES},
        "bootstrap": {**{k: meta[k] for k in ("seed", "replicates", "block_days", "index_sha256", "index_equals_cp20",
                                              "method", "ratio_method")}, "levels": [0.95, 0.975]},
        "contrasts": [list(c) for c in CONTRASTS],
        "parity_with_cp24": {"equal": par["equal"], "max_abs_difference": par["max_abs_difference"]},
        "rule": "none applied: v5's adoption rule (cp24-adoption) is not re-run and adopts nothing; A1 was selected by "
                "CP-28's registered rule on another population",
        "evidence_class": "development_post_selection",
        "inputs_sha256": inputs,
        "code": "src/delu_forecast/final_candidate.py",
    }


def render(result: dict, inputs: dict[str, str]) -> dict[str, str]:
    """The committed files' exact text."""
    def csv(frame: pd.DataFrame) -> str:
        buffer = io.StringIO()
        frame.to_csv(buffer, index=False, lineterminator="\n")
        return buffer.getvalue()

    metrics = result["metrics"]
    keep = metrics.loc[metrics.policy.eq(CODE) & metrics.scope.isin(("pooled", "per_fold", "equal_fold"))]
    par = parity(ROOT, metrics)
    if not par["equal"]:
        raise ValueError(f"the recomputed v5/B0/v3 scores differ from CP-24's committed rows by {par['max_abs_difference']}")
    files = {
        "metrics.csv": csv(keep),
        "uncertainty.csv": csv(result["uncertainty"]),
        "ratio-intervals.csv": result["ratios"].to_csv(index=False, float_format="%.17g", lineterminator="\n"),
        "parity.json": json.dumps(par, indent=1, sort_keys=True) + "\n",
        "summary.json": json.dumps(summary(result, inputs, par), indent=1, sort_keys=True, default=str) + "\n",
    }
    return files


def build(root: Path = ROOT) -> dict[str, str]:
    inputs = _inputs(root)
    return render(score(root), inputs)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="compare with the committed files; write nothing")
    args = ap.parse_args(argv)
    files = build(ROOT)
    out = ROOT / OUT
    if args.check:
        same = {name: (out / name).exists() and (out / name).read_text() == text for name, text in files.items()}
        print(json.dumps({"identical_to_committed": same}, sort_keys=True))
        return 0 if all(same.values()) else 12
    out.mkdir(parents=True, exist_ok=True)
    for name, text in files.items():
        (out / name).write_text(text)
    print(json.dumps({"wrote": sorted(str(OUT / name) for name in files)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
