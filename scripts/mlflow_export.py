#!/usr/bin/env python3
"""Write the committed MLflow export for `delu-generations` (presentation plan §10, brief §6).

The export is the only payload the publisher ever uploads. It is built from the evidence layer
(`delu_forecast.research`), never from a live computation, and it is committed, so the pre-commit
secret guard reads every byte of it before it can leave this machine.

    uv run python scripts/mlflow_export.py            # write reports/presentation/mlflow-export/
    uv run python scripts/mlflow_export.py --check    # exit 1 if the committed export is stale

Output: one JSON file per checkpoint (`cp10`, `cp15`, `cp16`, `cp20`) with its parent run and
children, and `manifest.json`, which lists the 23 run keys, their parents, every metric key with
its unit and history length, every artifact with its SHA-256, and the source blobs behind them.

Determinism: sorted keys, fixed timestamps taken from the evaluation windows (never the clock),
and values copied as the exact committed text of each cell. Tags written only at upload time --
`delu.backfill_tool_sha`, `delu.upload_state`, `delu.package_complete` -- are not in the export.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from delu_forecast import registry as G  # noqa: E402
from delu_forecast import research as R  # noqa: E402
from delu_forecast.claims import GITHUB_URL, PAGES_URL  # noqa: E402

import build_pages  # noqa: E402  (the page's own chart builders, for the chart artifacts)


def _n(record_id: str) -> str:
    """A count in a run description, read from its evidence record (plan §9.1, invariant 17)."""
    return R.display(R.get(record_id), "value")


def _ratio(hits: str, total: str) -> str:
    return f"{_n(hits)}/{_n(total)}"

EXPORT_DIR = ROOT / "reports" / "presentation" / "mlflow-export"
EXPERIMENT = "delu-generations"

#: Experiment-level tags. The kind tag stops MLflow 3.5's UI from asking an anonymous reader to
#: confirm an inferred experiment type (observed in the 2026-09-24 rehearsal). The description says
#: the repository is the source of truth (standard §8), and names the parents from the registry.
EXPERIMENT_TAGS = {
    "mlflow.experimentKind": "custom_model_development",
    "mlflow.note.content": (
        f"The repository {GITHUB_URL} is the source of truth: every run here mirrors its committed "
        "evidence, and every name, status and description comes from its registry. Each policy evaluated "
        "since v1 appears once, nested under the checkpoint that produced it: "
        + "; ".join(G.mlflow_run_name(checkpoint.run_key) for checkpoint in G.CHECKPOINTS.values())
        + ". Development evidence after selection, not a test on new data. v1's own runs are in delu-cp2."
    ),
}
FOLDS = ("fold_1", "fold_2", "fold_3", "fold_4", "fold_5")

# --------------------------------------------------------------------------- the manifest (§10.3)

#: Checkpoint provenance, from the landing records and verdicts: what the registry does not hold.
#: Names, statuses, children and roles come from `delu_forecast.registry` (standard §5).
#: `evidence_ref` names the tag that keeps the reviewed chain reachable, at its evidence tip. The
#: notes carry no status: a run's dated status is the registry's, prepended in `_description()`.
CHECKPOINTS: dict[str, dict] = {
    "cp10": {
        "checkpoint": "CP-10",
        "model_code_sha": "ad3e1a5d5e42d70ea95bbffd01b4563eb2d6d803",
        "evidence_ref": "evidence/cp-15@4039ce2",
        "evidence_tag": "evidence/cp-15",
        "protocol": "reports/cp10/protocol.json",
        "anchor_version": "capstone_v20.md §4, §9 CP-10",
        "report": "reports/cp10/report.md",
        "verdict": "docs/track-b/evidence/cp-10/integration.md",
        "landing": "docs/track-b/cp-15-landing.md",
        "note": (
            "CP-10 recalibrated v1 without refitting it: two scaled-conformal variants and four "
            "adaptive-conformal step sizes, selected on folds 1, 2, 4 and 5. Crisis-window hours inside "
            "the 95% interval rose from "
            f"{_ratio('cp10.peak_windows.v1_reference.covered_95', 'cp10.peak_windows.v1_reference.n_obs')} to "
            f"{_ratio('cp10.peak_windows.c1_price_volatility.covered_95', 'cp10.peak_windows.c1_price_volatility.n_obs')}"
            ", not enough. Scores are v1's "
            "native nine-quantile pinball and coverage; there are no S_ scores here. "
            "development_calibration_comparison."
        ),
    },
    "cp15": {
        "checkpoint": "CP-15",
        "model_code_sha": "fc4aee038cf898998a292506df62ddb0dcfaf22a",
        "evidence_ref": "evidence/cp-15@1bdc75b",
        "evidence_tag": "evidence/cp-15",
        "protocol": "reports/cp15/protocol.json",
        "anchor_version": "capstone_v21.md v21-r1",
        "report": "reports/cp15/report.md",
        "verdict": "docs/track-b/evidence/cp-15/integration.md",
        "landing": "docs/track-b/cp-15-landing.md",
        "note": (
            f"CP-15 compared nine policies on the same {_n('cp15.pooled.B0.n_hours')} development hours: four references "
            "(B0 similar-day naive, B1 v1's development replay, B2 daily LEAR, B3 daily LightGBM) and "
            "five adaptive challengers (A1-A5). A1 was the best challenger, B2 had better primary "
            "scores, and no policy met the product criteria (NOT_DEMONSTRATED). It informed v2. "
            "development_post_selection."
        ),
    },
    "cp16": {
        "checkpoint": "CP-16",
        "model_code_sha": "bf3ca602e32e99e45c7835e3f95148f62b608099",
        "evidence_ref": "evidence/cp-16@5ec8a92",
        "evidence_tag": "evidence/cp-16",
        "protocol": "reports/v2-causal/protocol.json",
        "anchor_version": "capstone_v21.md v21-r3",
        "report": "reports/v2-causal/report.md",
        "verdict": "docs/track-b/evidence/cp-16/integration.md",
        "landing": "docs/track-b/cp-16-landing-2026-09-23.md",
        "note": (
            "CP-16 blends the A1 and B2 central forecasts 50/50 with hour-aware residual intervals "
            "(V2-H) and a pooled-interval control (V2-P). V2-H against B2 meets the exploratory joint "
            "improvement rule; V2-H against V2-P shows no demonstrated joint preference. "
            "development_post_selection."
        ),
    },
    "cp20": {
        "checkpoint": "CP-20",
        "model_code_sha": "3e9ff8b500c2c655fea810ae11886503927f176c",
        "evidence_ref": "evidence/cp-20@a7a9b2e",
        "evidence_tag": "evidence/cp-20",
        "protocol": "reports/weather-ablation/protocol.json",
        "anchor_version": "capstone_v21.md v21-r4 §15",
        "report": "reports/weather-ablation/report.md",
        "verdict": "docs/track-b/evidence/cp-20/integration.md",
        "landing": "docs/track-b/cp-20-landing-2026-09-24.md",
        "note": (
            "CP-20 appended three GFS weather features (mean wind speed at 10 m and 100 m, mean "
            "solar radiation over a fixed regional box) to v2's recipes. HG against H0 (= v2) meets "
            "the joint improvement rule; the gain belongs to the three features together. "
            "development_post_selection."
        ),
    },
}

def children(checkpoint: str) -> tuple[str, ...]:
    """A checkpoint's children, in the registry's order. Each policy appears once per population,
    under the checkpoint that produced it first: the references come from CP-15, v2 from CP-16,
    v3 from CP-20."""
    return G.CHECKPOINTS[CHECKPOINTS[checkpoint]["checkpoint"]].children


def _status_text(entry: G.Entry) -> str:
    return f"{entry.status.status} {entry.status.date}" if entry.status is not None else "none"


def _description(entry: G.Entry, note: str, *, code: str | None = None, role: str | None = None) -> str:
    """A run's description: its registry identity and dated status, then the checkpoint's summary."""
    parts = [f"{entry.name}: {entry.subtitle}."]
    if entry.status is not None:
        parts.append(G.status_sentence(entry))
    if code is not None:
        parts.append(f"Code {code}; role {role}.")
    parts.append(note)
    return " ".join(parts)

#: The base each candidate's paired contrasts are logged against, by run and base code.
CONTRASTS: dict[str, tuple[tuple[str, str, str], ...]] = {
    # (record prefix, record base code, metric slug)
    "cp20/HG": (("cp20.uncertainty.HG-H0", "H0", "v2_h"),),
    "cp16/V2-H": (("cp16.uncertainty.V2-H-V2-P", "V2-P", "v2_p"), ("cp16.uncertainty.V2-H-B2", "B2", "b2")),
    "cp16/V2-P": (("cp16.uncertainty.V2-P-B2", "B2", "b2"),),
    **{
        f"cp15/{candidate}": tuple(
            (f"cp15.bootstrap.{candidate}-{base}", base, base.lower()) for base in ("B0", "B1", "B2", "B3")
        )
        for candidate in ("A1", "A2", "A3", "A4", "A5")
    },
}

# --------------------------------------------------------------------------- metric vocabulary (§10.4)

UNIT_RATIO = "ratio to B0, equal-fold"
UNIT_EUR = "EUR/MWh"
UNIT_FRACTION = "fraction"
UNIT_COUNT = "count"
UNIT_NORM_DIFF = "normalized score difference"
UNIT_EUR_DIFF = "EUR/MWh, paired mean daily loss difference"

#: Every metric name the export may use, with its unit. The name carries the unit: `_eur` for
#: EUR/MWh, `coverage` for fractions, `hits` for counts, `s_` for equal-fold ratios.
METRIC_UNITS: dict[str, str] = {
    "s_mae": UNIT_RATIO, "s_wis": UNIT_RATIO,
    "pooled_mae_eur": UNIT_EUR, "pooled_wis_eur": UNIT_EUR, "pooled_rmse_eur": UNIT_EUR,
    "pooled_bias_eur": UNIT_EUR, "pooled_coverage95": UNIT_FRACTION,
    "fold_mae_eur": UNIT_EUR, "fold_wis_eur": UNIT_EUR, "fold_coverage50": UNIT_FRACTION,
    "fold_coverage80": UNIT_FRACTION, "fold_coverage95": UNIT_FRACTION, "fold_mean_width95_eur": UNIT_EUR,
    "fold_pinball9_eur": UNIT_EUR,
    "peak_mae_eur": UNIT_EUR, "peak_wis_eur": UNIT_EUR, "peak_coverage95": UNIT_FRACTION, "peak_hits95": UNIT_COUNT,
    "daily_mae_eur": UNIT_EUR,
}


def metric_unit(key: str) -> str:
    """The unit of any exported metric key, including the per-base contrast families."""
    if key in METRIC_UNITS:
        return METRIC_UNITS[key]
    if key.startswith(("delta_s_mae_vs_", "delta_s_wis_vs_")):
        return UNIT_NORM_DIFF
    if key.startswith(("delta_fold_mae_eur_vs_", "delta_fold_wis_eur_vs_")):
        return UNIT_EUR_DIFF
    raise KeyError(f"metric {key!r} has no declared unit")


#: Descriptions a reader sees; MLflow joins fold steps with lines, so the step is named here.
STEP_NOTE = {
    "fold": "step = fold index (1-5); timestamp = the fold's last delivery date. Folds are discrete "
            "periods, not a time series.",
    "day": f"step = day index within the {_n('cp15.pooled.B0.n_days')} represented development days; "
           "timestamp = the delivery date.",
    "single": "step 0; timestamp = the last delivery date of the evaluated window.",
}

# --------------------------------------------------------------------------- helpers


def _ms(day: str) -> int:
    return int(datetime.combine(date.fromisoformat(day), datetime.min.time(), tzinfo=timezone.utc).timestamp() * 1000)


def _point(record: R.EvidenceRecord, step: int, which: str = "value") -> dict:
    raw = {"value": record.raw, "ci_low": record.ci_low_raw, "ci_high": record.ci_high_raw}[which]
    return {"step": step, "timestamp": _ms(record.window[1]), "value": float(raw)}


def _canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class Builder:
    """Collects one run's metrics with the record behind every point."""

    def __init__(self) -> None:
        self.metrics: dict[str, list[dict]] = {}
        self.provenance: dict[str, list[str]] = {}

    def single(self, key: str, record_id: str, which: str = "value") -> None:
        record = R.get(record_id)
        self._add(key, _point(record, 0, which), f"{record_id}#{which}")

    def per_fold(self, key: str, pattern: str, which: str = "value") -> None:
        for index, fold in enumerate(FOLDS, start=1):
            record_id = pattern.format(fold=fold)
            record = R.get(record_id)
            self._add(key, _point(record, index, which), f"{record_id}#{which}")

    def daily(self, checkpoint: str, policy: str) -> None:
        series = R.daily_series(checkpoint, policy)
        path = R.DAILY_SOURCES[checkpoint][0]
        for index, point in enumerate(series):
            self.metrics.setdefault("daily_mae_eur", []).append(
                {"step": index, "timestamp": _ms(point.delivery_date), "value": float(point.raw)}
            )
        self.provenance["daily_mae_eur"] = [f"{path} (policy {policy}, {len(series)} daily rows)"]

    def _add(self, key: str, point: dict, source: str) -> None:
        metric_unit(key)  # refuses an undeclared name
        self.metrics.setdefault(key, []).append(point)
        self.provenance.setdefault(key, []).append(source)


def _scores(builder: Builder, run_key: str, policy: str) -> None:
    checkpoint = run_key.split("/")[0]
    if checkpoint == "cp10":
        base = f"cp10.metrics.{policy}.{{fold}}"
        builder.per_fold("fold_mae_eur", base + ".mae")
        builder.per_fold("fold_pinball9_eur", base + ".mean_pinball")
        builder.per_fold("fold_coverage50", base + ".coverage_50")
        builder.per_fold("fold_coverage80", base + ".coverage_80")
        builder.per_fold("fold_coverage95", base + ".coverage_95")
        peak = f"cp10.peak_windows.{policy}"
        builder.single("peak_mae_eur", f"{peak}.mae")
        builder.single("peak_coverage95", f"{peak}.coverage_95")
        builder.single("peak_hits95", f"{peak}.covered_95")
        return
    if checkpoint == "cp15":
        equal, pooled, fold, peak = (
            f"cp15.relative_scores.{policy}", f"cp15.pooled.{policy}",
            f"cp15.per_fold.{policy}.{{fold}}", f"cp15.peak.{policy}",
        )
        daily = ("CP-15", policy)
    else:
        prefix = checkpoint
        equal, pooled = f"{prefix}.metrics.{policy}.equal_fold", f"{prefix}.metrics.{policy}.pooled"
        fold, peak = f"{prefix}.metrics.{policy}.{{fold}}", f"{prefix}.diagnostics.{policy}.peak"
        daily = ("CP-16" if checkpoint == "cp16" else "CP-20", policy)
    builder.single("s_mae", f"{equal}.S_MAE")
    builder.single("s_wis", f"{equal}.S_WIS")
    for key, column in (("pooled_mae_eur", "MAE"), ("pooled_wis_eur", "WIS"), ("pooled_rmse_eur", "RMSE"),
                        ("pooled_bias_eur", "bias"), ("pooled_coverage95", "coverage95")):
        builder.single(key, f"{pooled}.{column}")
    for key, column in (("fold_mae_eur", "MAE"), ("fold_wis_eur", "WIS"), ("fold_coverage50", "coverage50"),
                        ("fold_coverage80", "coverage80"), ("fold_coverage95", "coverage95"),
                        ("fold_mean_width95_eur", "mean_width95")):
        builder.per_fold(key, f"{fold}.{column}")
    for key, column in (("peak_mae_eur", "MAE"), ("peak_wis_eur", "WIS"), ("peak_coverage95", "coverage95"),
                        ("peak_hits95", "hit_count95")):
        builder.single(key, f"{peak}.{column}")
    builder.daily(*daily)
    for record_prefix, _base_code, slug in CONTRASTS.get(run_key, ()):
        for metric, score in (("MAE", "mae"), ("WIS", "wis")):
            equal_record = f"{record_prefix}.equal_fold.{metric}"
            builder.single(f"delta_s_{score}_vs_{slug}", equal_record)
            builder.single(f"delta_s_{score}_vs_{slug}_ci_low", equal_record, "ci_low")
            builder.single(f"delta_s_{score}_vs_{slug}_ci_high", equal_record, "ci_high")
            fold_pattern = f"{record_prefix}.{{fold}}.{metric}"
            builder.per_fold(f"delta_fold_{score}_eur_vs_{slug}", fold_pattern)
            builder.per_fold(f"delta_fold_{score}_eur_vs_{slug}_ci_low", fold_pattern, "ci_low")
            builder.per_fold(f"delta_fold_{score}_eur_vs_{slug}_ci_high", fold_pattern, "ci_high")


# --------------------------------------------------------------------------- comparability and datasets


def _keys_digest(path: str, column: str, value: str) -> tuple[str, int]:
    """SHA-256 of the sorted evaluation keys (UTC hour starts) of one policy's committed rows."""
    import pyarrow.parquet as pq

    table = pq.read_table(ROOT / path, columns=[column, "timestamp_utc"]).to_pandas()
    keys = sorted(str(ts.isoformat()) for ts in table.loc[table[column] == value, "timestamp_utc"])
    return sha256_text("\n".join(keys)), len(keys)


def _file_sha256(path: str) -> str:
    digest = hashlib.sha256()
    with open(ROOT / path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def comparability() -> dict[str, dict]:
    """Two comparability groups: CP-15/16/20 share one; CP-10 has its own (§10.5).

    The ID is a SHA-256 over the sorted evaluation keys, the target definition and unit, the
    score and quantile definitions, the aggregation and the reference policy definition, all
    taken from the committed protocols. Matching metric names alone never make runs comparable.
    """
    cp15 = json.loads((ROOT / "reports/cp15/protocol.json").read_text())
    cp10 = json.loads((ROOT / "reports/cp10/protocol.json").read_text())
    common_digest, common_n = _keys_digest("reports/cp15/predictions.parquet", "policy", "B0")
    cp10_digest, cp10_n = _keys_digest("reports/cp10/predictions.parquet", "candidate", "v1_reference")
    target = "DE-LU day-ahead price per delivery hour, EUR/MWh, delivery calendar Europe/Berlin"
    groups = {
        "common": {
            "population_id": "common-10747h",
            "keys_sha256": common_digest,
            "keys": common_n,
            "target": target,
            "scores": {
                "S_MAE": cp15["metrics"]["S_MAE"], "S_WIS": cp15["metrics"]["S_WIS"],
                "primary": cp15["metrics"]["primary"], "WIS": cp15["metrics"]["WIS"],
            },
            "quantiles": cp15["quantiles"]["levels"],
            "aggregation": "equal_fold (primary); pooled observation-weighted (secondary)",
            "reference": "B0 similar-day naive; " + cp15["warmup"]["buffer"],
        },
        "cp10": {
            "population_id": "cp10-fold-block",
            "keys_sha256": cp10_digest,
            "keys": cp10_n,
            "target": target,
            "scores": {"selection_scalar": cp10["selection_scalar"]},
            "quantiles": "v1 nine quantiles",
            "aggregation": "per_fold; selection on folds " + ", ".join(cp10["selection_folds"]),
            "reference": cp10["reference"],
        },
    }
    for group in groups.values():
        group["comparability_id"] = sha256_text(_canonical({k: v for k, v in group.items() if k != "keys"}))
    return groups


def datasets(checkpoint: str, policy: str, group: dict) -> list[dict]:
    """`log_input` payloads: digests of the population, the market snapshot and (HG only) the
    weather features. Nothing but names, digests and committed source paths."""
    snapshot = json.loads((ROOT / "reports/cp15/protocol.json").read_text())["input_sha256"]["data/snapshot.parquet"]
    out = [
        {"name": group["population_id"], "digest": group["keys_sha256"][:36], "context": "evaluation",
         "source": "reports/cp15/predictions.parquet" if checkpoint != "cp10" else "reports/cp10/predictions.parquet",
         "sha256": group["keys_sha256"], "profile": f"{group['keys']} evaluation hours"},
        {"name": "market-snapshot", "digest": snapshot[:36], "context": "training",
         "source": "data/snapshot.parquet", "sha256": snapshot, "profile": "committed SMARD/ENTSO-E snapshot"},
    ]
    if policy == "HG":
        recorded = json.loads((ROOT / "reports/weather-ablation/extraction-summary.json").read_text())
        weather = recorded["files_sha256"]["weather-features.parquet"]
        if _file_sha256("reports/weather-ablation/weather-features.parquet") != weather:
            raise RuntimeError("weather-features.parquet no longer matches its recorded SHA-256")
        out.append({"name": "gfs-weather-features", "digest": weather[:36], "context": "training",
                    "source": "reports/weather-ablation/weather-features.parquet", "sha256": weather,
                    "profile": "three regional GFS features and their status"})
    return out


# --------------------------------------------------------------------------- params (§10.5)


def params(checkpoint: str, policy: str) -> dict[str, str]:
    """Only what the committed protocol states; an unknown value is left out, never guessed."""
    spec = CHECKPOINTS[checkpoint]
    protocol_path = spec["protocol"]
    protocol = json.loads((ROOT / protocol_path).read_text())
    out = {"anchor_version": spec["anchor_version"], "protocol_sha256": _file_sha256(protocol_path)}
    if checkpoint == "cp10":
        cp10 = protocol
        out.update(catalog=cp10["catalog"], isotonic=cp10["isotonic"], evidence_class=cp10["evidence_class"])
        if policy.startswith("c1_"):
            out["scale"] = cp10["spread"] if policy == "c1_head_spread" else (
                f"price volatility over {cp10['volatility_window_hours']} hours, ddof {cp10['volatility_ddof']}")
        if policy.startswith("c2_"):
            out["aci_gamma"] = policy.rsplit("_", 1)[1]
            out["aci_update"] = cp10["aci_update"]
        if policy == "v1_reference":
            out["reference"] = cp10["reference"]
        return out
    cp15 = json.loads((ROOT / "reports/cp15/protocol.json").read_text())
    out["quantile_set"] = ",".join(str(level) for level in cp15["quantiles"]["levels"])
    out["seed"] = str(cp15["seed"])
    out["weather_features"] = "none"
    if policy in ("B2", "A1", "A4", "V2-H", "V2-P", "HG", "A3", "A5"):
        out["lear"] = cp15["lear"]["implementation"]
        out["history_window"] = cp15["history"]["long"] if policy != "A4" else cp15["history"]["short"]
    if policy in ("B3", "A2"):
        out["lightgbm"] = cp15["lgbm"]["fits"]
        out["history_window"] = cp15["history"]["long"]
    if policy in ("A1", "A2", "A4"):
        out["target_transform"] = cp15["normalization"]["target"]
    if policy in ("A3", "A5"):
        out["blend"] = cp15["ensembles"][policy]
    if policy == "B1":
        out["intervals"] = cp15["quantiles"]["B1"]
    else:
        out["interval_method"] = cp15["quantiles"]["method"]
    if checkpoint == "cp16":
        # The ratified contract is carried verbatim inside CP-16's protocol; its policy bullets
        # are the definitions, so they are quoted rather than paraphrased.
        contract = protocol["scientific_contract_verbatim"]
        bullet = next(line for line in contract.splitlines() if line.startswith(f"- **{policy}:**"))
        out["policy_definition"] = bullet[2:].replace("**", "")
        if policy == "V2-H":
            cp20 = json.loads((ROOT / "reports/weather-ablation/protocol.json").read_text())
            out["interval_method"] = cp20["residual_recipe"]
    if checkpoint == "cp20":
        out["policy_definition"] = protocol["arms"][policy]
        out["interval_method"] = protocol["residual_recipe"]
        out["weather_features"] = ",".join(protocol["weather_recipe"]["design_columns"]) + " plus missing indicators"
        out["weather_product"] = protocol["weather_recipe"]["product"]
    return {key: value[:500] for key, value in out.items()}


# --------------------------------------------------------------------------- runs


def _source_blobs(provenance: dict[str, list[str]]) -> dict[str, str]:
    paths = set()
    for sources in provenance.values():
        for source in sources:
            record_id = source.split("#")[0]
            if " (policy " in source:
                paths.add(source.split(" (policy ")[0])
            else:
                paths.add(R.get(record_id).source_path)
    return {path: R.SOURCES[path].blob for path in sorted(paths)}


def _readme(checkpoint: str, run_key: str, run_name: str, blobs: dict[str, str]) -> str:
    spec = CHECKPOINTS[checkpoint]
    tag = spec["evidence_tag"]
    lines = [
        f"# {run_name}",
        "",
        f"Backfilled from committed evidence by the PRES-1 export (`{run_key}`). Development evidence; "
        "nothing here is a live or confirmatory result.",
        "",
        f"- Report: {GITHUB_URL}/blob/{tag}/{spec['report']}",
        f"- Independent Integration review: {GITHUB_URL}/blob/{tag}/{spec['verdict']}",
        f"- Landing record: {GITHUB_URL}/blob/main/{spec['landing']}",
        f"- Presentation: {PAGES_URL}",
        "",
        "Source rows at the evidence tag:",
        "",
    ]
    lines += [f"- {GITHUB_URL}/blob/{tag}/{path} (blob {blob})" for path, blob in blobs.items()]
    return "\n".join(lines) + "\n"


def _artifact(path: str, content: str) -> dict:
    return {"path": path, "sha256": sha256_text(content), "bytes": len(content.encode("utf-8")), "content": content}


def child_run(checkpoint: str, code: str, groups: dict) -> dict:
    spec = CHECKPOINTS[checkpoint]
    run_key = f"{checkpoint}/{code}"
    entry = G.entry_for_run_key(run_key)
    role = G.run_role(run_key)
    group = groups["cp10" if checkpoint == "cp10" else "common"]
    builder = Builder()
    _scores(builder, run_key, code)
    blobs = _source_blobs(builder.provenance)
    run_name = G.mlflow_run_name(run_key)
    note = _description(entry, spec["note"], code=code, role=role)
    tags = {
        "delu.run_key": run_key,
        "delu.checkpoint": spec["checkpoint"],
        "delu.registry_id": entry.id,
        "delu.kind": entry.kind,
        "delu.generation": entry.version or "none",
        "delu.policy_code": code,
        "delu.public_name": entry.name,
        "delu.status": _status_text(entry),
        "delu.comparator": G.get(entry.comparator).name if entry.comparator else "none",
        "delu.role": role,
        "delu.adopted": G.adopted_flag(entry),
        "delu.evidence_class": ("development_calibration_comparison" if checkpoint == "cp10"
                                else "development_post_selection"),
        "delu.population_id": group["population_id"],
        "delu.comparability_id": group["comparability_id"],
        "delu.model_code_sha": spec["model_code_sha"],
        "delu.evidence_ref": spec["evidence_ref"],
        "delu.source_blobs": _canonical(blobs),
        "delu.backfilled": "true",
        "delu.original_completed_utc": "unknown",
        "mlflow.note.content": note,
    }
    if code == "B1":
        tags["delu.v1_record_run"] = "83e475627b6646c885c70f9010c8cf2e"
    inputs = datasets(checkpoint, code, group)
    # The digests also travel as a tag, so they survive on a server without dataset support.
    tags["delu.datasets"] = _canonical({dataset["name"]: dataset["sha256"] for dataset in inputs})
    run = {
        "run_key": run_key,
        "parent": checkpoint,
        "run_name": run_name,
        "params": params(checkpoint, code),
        "tags": tags,
        "metrics": builder.metrics,
        "metric_provenance": builder.provenance,
        "metric_units": {key: metric_unit(key) for key in builder.metrics},
        "inputs": inputs,
    }
    summary = _canonical({k: v for k, v in run.items() if k != "metric_provenance"})
    charts = [(f"charts/{chart_id}.svg", build_pages.standalone_svg(build()))
              for chart_id, build in build_pages.CHARTS_BY_RUN.get(run_key, ())]
    readme = _readme(checkpoint, run_key, run_name, blobs)
    if charts:
        readme += ("\nCharts, drawn by the page build from the same records as the report:\n\n"
                   + "".join(f"- `{path}`\n" for path, _ in charts))
    run["artifacts"] = [
        _artifact("summary.json", summary + "\n"),
        _artifact("README.md", readme),
    ] + [_artifact(path, content) for path, content in charts]
    return run


def parent_run(checkpoint: str, groups: dict) -> dict:
    spec = CHECKPOINTS[checkpoint]
    owner = G.entry_for_run_key(checkpoint)
    run_name = G.mlflow_run_name(checkpoint)
    group = groups["cp10" if checkpoint == "cp10" else "common"]
    tags = {
        "delu.run_key": checkpoint,
        "delu.checkpoint": spec["checkpoint"],
        "delu.registry_id": owner.id,
        "delu.kind": owner.kind,
        "delu.public_name": owner.name,
        "delu.status": _status_text(owner),
        "delu.role": "checkpoint",
        "delu.evidence_class": ("development_calibration_comparison" if checkpoint == "cp10"
                                else "development_post_selection"),
        "delu.population_id": group["population_id"],
        "delu.comparability_id": group["comparability_id"],
        "delu.model_code_sha": spec["model_code_sha"],
        "delu.evidence_ref": spec["evidence_ref"],
        "delu.backfilled": "true",
        "delu.original_completed_utc": "unknown",
        "delu.children": ",".join(f"{checkpoint}/{code}" for code in children(checkpoint)),
        "mlflow.note.content": _description(owner, spec["note"]),
    }
    run = {
        "run_key": checkpoint,
        "parent": None,
        "run_name": run_name,
        "params": {"anchor_version": spec["anchor_version"], "protocol_sha256": _file_sha256(spec["protocol"])},
        "tags": tags,
        "metrics": {},
        "metric_provenance": {},
        "metric_units": {},
        "inputs": [],
        "comparability": {k: v for k, v in group.items()},
    }
    blobs = {spec["protocol"]: R.SOURCES[spec["protocol"]].blob} if spec["protocol"] in R.SOURCES else {}
    run["artifacts"] = [
        _artifact("summary.json", _canonical({k: v for k, v in run.items() if k != "metric_provenance"}) + "\n"),
        _artifact("README.md", _readme(checkpoint, checkpoint, run_name, blobs)),
    ]
    return run


def build_export() -> dict[str, dict]:
    groups = comparability()
    files: dict[str, dict] = {}
    for checkpoint in G.parent_run_keys():
        runs = [parent_run(checkpoint, groups)]
        runs += [child_run(checkpoint, code, groups=groups) for code in children(checkpoint)]
        files[checkpoint] = {"experiment": EXPERIMENT, "checkpoint": CHECKPOINTS[checkpoint]["checkpoint"],
                             "runs": runs}
    files["manifest"] = manifest(files)
    return files


def manifest(files: dict[str, dict]) -> dict:
    runs = []
    for checkpoint in G.parent_run_keys():
        for run in files[checkpoint]["runs"]:
            runs.append({
                "run_key": run["run_key"],
                "parent": run["parent"],
                "run_name": run["run_name"],
                "file": f"{checkpoint}.json",
                "metrics": {key: len(points) for key, points in sorted(run["metrics"].items())},
                "artifacts": {artifact["path"]: artifact["sha256"] for artifact in run["artifacts"]},
                "params": len(run["params"]),
                "tags": len(run["tags"]),
                "inputs": [dataset["name"] for dataset in run["inputs"]],
            })
    parents = [run for run in runs if run["parent"] is None]
    return {
        "experiment": EXPERIMENT,
        "experiment_tags": EXPERIMENT_TAGS,
        "counts": {"parents": len(parents), "children": len(runs) - len(parents), "total": len(runs)},
        "runs": runs,
        "metric_units": {key: metric_unit(key) for run in runs for key in run["metrics"]},
        "step_notes": STEP_NOTE,
        "sources": {path: {"tag": source.tag, "blob": source.blob} for path, source in sorted(R.SOURCES.items())},
        "upload_time_tags": ["delu.backfill_tool_sha", "delu.upload_state", "delu.package_complete"],
    }


def contract_problems(files: dict[str, dict]) -> list[str]:
    """The export matches the registry (standard §11): exactly the run keys it expects, each once,
    each parent the checkpoint that owns it, each name the registry's. Never a count."""
    problems = []
    runs = [run for name, content in files.items() if name != "manifest" for run in content["runs"]]
    keys = [run["run_key"] for run in runs]
    expected = G.expected_run_keys()
    if sorted(keys) != sorted(expected) or len(keys) != len(set(keys)):
        missing = sorted(set(expected) - set(keys))
        extra = sorted(set(keys) - set(expected))
        problems.append(f"run keys differ from the registry (missing {missing}, unregistered {extra})")
    for run in runs:
        key = run["run_key"]
        if key not in expected:
            continue
        if run["run_name"] != G.mlflow_run_name(key):
            problems.append(f"{key}: run name is not the registry's")
        want_parent = None if "/" not in key else key.split("/")[0]
        if run["parent"] != want_parent:
            problems.append(f"{key}: parent {run['parent']!r} is not {want_parent!r}")
        entry = G.entry_for_run_key(key)
        if run["tags"].get("delu.public_name") != entry.name:
            problems.append(f"{key}: public name tag is not the registry's")
    manifest = [run["run_key"] for run in files.get("manifest", {}).get("runs", [])]
    if files.get("manifest") is not None and sorted(manifest) != sorted(keys):
        problems.append("the manifest does not list exactly the exported runs")
    return problems


def render(files: dict[str, dict]) -> dict[str, str]:
    return {f"{name}.json": json.dumps(content, indent=1, sort_keys=True, ensure_ascii=False) + "\n"
            for name, content in files.items()}


# --------------------------------------------------------------------------- outbound scan (§10.8)


def outbound_strings(files: dict[str, dict]):
    """Every string that could leave this machine: names, params, tags, notes, metric keys,
    dataset fields and artifact bytes, with where each one sits."""
    for name, content in files.items():
        if name == "manifest":
            continue
        for run in content["runs"]:
            where = f"{name}:{run['run_key']}"
            yield f"{where} run name", run["run_name"]
            for key, value in run["params"].items():
                yield f"{where} param {key}", f"{key}={value}"
            for key, value in run["tags"].items():
                yield f"{where} tag {key}", f"{key}={value}"
            for key in run["metrics"]:
                yield f"{where} metric key", key
            for dataset in run["inputs"]:
                yield f"{where} dataset {dataset['name']}", _canonical(dataset)
            for artifact in run["artifacts"]:
                yield f"{where} artifact {artifact['path']}", artifact["content"]


def outbound_findings(items, secrets: list[tuple[str, bytes]]) -> list[str]:
    """Where a credential value appears. Names the variable and the place, never the value."""
    findings = []
    for where, text in items:
        data = text.encode("utf-8") if isinstance(text, str) else text
        for name, value in secrets:
            if value in data:
                findings.append(f"the value of {name} appears in {where}")
    return findings


def local_secrets() -> list[tuple[str, bytes]]:
    from secret_guard import credentials

    return credentials()


# --------------------------------------------------------------------------- record-level diff (brief W2)

#: The fields a registry change may alter: names, descriptions and tags. Everything else --
#: parameters, every metric history point, datasets, parents and artifact digests -- must match.
IDENTITY_FIELDS = ("run_name", "tags")


def _runs_by_key(files: dict[str, dict]) -> dict[str, dict]:
    return {run["run_key"]: run for name, content in files.items() if name != "manifest"
            for run in content["runs"]}


#: The artifacts that carry a run's identity: `summary.json` holds its name and tags, and
#: `README.md` its name as the title line. A name change changes their bytes by construction.
IDENTITY_ARTIFACTS = ("summary.json", "README.md")


def _restored_artifact(path: str, content: str, old_run: dict) -> str:
    """The new artifact with the old run's identity fields put back. Its SHA-256 equals the old
    artifact's exactly when nothing but identity changed: byte identity for everything else, and
    content preservation, proven at the digest, for the identity-bearing artifacts."""
    if path == "summary.json":
        body = json.loads(content)
        body.update({field: old_run[field] for field in IDENTITY_FIELDS})
        return _canonical(body) + "\n"
    if path == "README.md":
        return f"# {old_run['run_name']}\n" + content.split("\n", 1)[1]
    return content


def diff_exports(old: dict[str, dict], new: dict[str, dict]) -> dict:
    """Compare two exports record by record: every run, parameter, metric history point, dataset
    and artifact. Returns what changed; `only_identity` is true when nothing but names,
    descriptions and tags did. An artifact passes when its digest is unchanged, or -- only for the
    identity-bearing artifacts -- when restoring the old names and tags reproduces the old digest."""
    old_runs, new_runs = _runs_by_key(old), _runs_by_key(new)
    report: dict = {"runs_old": len(old_runs), "runs_new": len(new_runs), "run_keys_equal": sorted(old_runs) == sorted(new_runs),
                    "checked": {"params": 0, "metric_points": 0, "datasets": 0, "artifacts": 0,
                                "artifacts_digest_unchanged": 0, "artifacts_old_digest_on_restoring_identity": 0},
                    "identity_changes": {}, "substantive_changes": []}
    for key in sorted(set(old_runs) | set(new_runs)):
        if key not in old_runs or key not in new_runs:
            report["substantive_changes"].append(f"{key}: present in only one export")
            continue
        a, b = old_runs[key], new_runs[key]
        changed = {}
        if a["run_name"] != b["run_name"]:
            changed["run_name"] = [a["run_name"], b["run_name"]]
        tag_changes = {k: [a["tags"].get(k), b["tags"].get(k)] for k in sorted(set(a["tags"]) | set(b["tags"]))
                       if a["tags"].get(k) != b["tags"].get(k)}
        if tag_changes:
            changed["tags"] = tag_changes
        if changed:
            report["identity_changes"][key] = changed
        if a["parent"] != b["parent"]:
            report["substantive_changes"].append(f"{key}: parent")
        if a["params"] != b["params"]:
            report["substantive_changes"].append(f"{key}: params")
        report["checked"]["params"] += len(a["params"])
        if a["metrics"] != b["metrics"] or a["metric_units"] != b["metric_units"]:
            report["substantive_changes"].append(f"{key}: metrics")
        report["checked"]["metric_points"] += sum(len(points) for points in a["metrics"].values())
        if a["inputs"] != b["inputs"]:
            report["substantive_changes"].append(f"{key}: datasets")
        report["checked"]["datasets"] += len(a["inputs"])
        old_art = {art["path"]: art for art in a["artifacts"]}
        new_art = {art["path"]: art for art in b["artifacts"]}
        if sorted(old_art) != sorted(new_art):
            report["substantive_changes"].append(f"{key}: artifact paths")
            continue
        for path in sorted(old_art):
            report["checked"]["artifacts"] += 1
            if old_art[path]["sha256"] == new_art[path]["sha256"]:
                report["checked"]["artifacts_digest_unchanged"] += 1
                continue
            if (path in IDENTITY_ARTIFACTS
                    and sha256_text(_restored_artifact(path, new_art[path]["content"], a)) == old_art[path]["sha256"]):
                report["checked"]["artifacts_old_digest_on_restoring_identity"] += 1
                report["identity_changes"].setdefault(key, {}).setdefault("artifacts_identity_only", []).append(path)
                continue
            report["substantive_changes"].append(f"{key}: artifact {path}")
    old_tags = old.get("manifest", {}).get("experiment_tags", {})
    new_tags = new.get("manifest", {}).get("experiment_tags", {})
    report["experiment_tag_changes"] = sorted(k for k in set(old_tags) | set(new_tags) if old_tags.get(k) != new_tags.get(k))
    report["only_identity"] = report["run_keys_equal"] and not report["substantive_changes"]
    return report


def export_at(ref: str) -> dict[str, dict]:
    """The committed export at a Git revision, as parsed JSON."""
    import subprocess

    files = {}
    for name in ("manifest", *G.parent_run_keys()):
        text = subprocess.run(["git", "show", f"{ref}:reports/presentation/mlflow-export/{name}.json"],
                              cwd=ROOT, capture_output=True, text=True, check=True).stdout
        files[name] = json.loads(text)
    return files


# --------------------------------------------------------------------------- main


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--check", action="store_true", help="exit 1 if the committed export is stale")
    parser.add_argument("--diff-against", metavar="REF", default=None,
                        help="compare the fresh export with the one committed at REF, record by record")
    parser.add_argument("--to", metavar="REF", default=None,
                        help="with --diff-against: compare with the export committed at REF instead of a fresh one")
    parser.add_argument("--out", type=Path, default=None, help="with --diff-against: write the report here")
    args = parser.parse_args()
    files = build_export()
    if args.diff_against:
        report = diff_exports(export_at(args.diff_against), export_at(args.to) if args.to else files)
        report["against"] = args.diff_against
        report["to"] = args.to or "the fresh export"
        text = json.dumps(report, indent=1, sort_keys=True, ensure_ascii=False) + "\n"
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(text)
        print(f"runs {report['runs_old']} -> {report['runs_new']}; checked {report['checked']}; "
              f"identity changes on {len(report['identity_changes'])} runs; "
              f"substantive changes: {report['substantive_changes'] or 'none'}; only_identity={report['only_identity']}")
        return 0 if report["only_identity"] else 1
    counts = files["manifest"]["counts"]
    problems = contract_problems(files)
    if problems:
        raise SystemExit("the export does not match the registry: " + "; ".join(problems))
    findings = outbound_findings(outbound_strings(files), local_secrets())
    if findings:
        for finding in dict.fromkeys(findings):
            print(f"mlflow-export: BLOCKED - {finding}", file=sys.stderr)
        return 1
    rendered = render(files)
    if args.check:
        stale = [name for name, text in rendered.items()
                 if not (EXPORT_DIR / name).exists() or (EXPORT_DIR / name).read_text() != text]
        if stale:
            print(f"the committed export is stale: {stale}; run scripts/mlflow_export.py")
            return 1
        print("the committed export is current")
        return 0
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    for name, text in rendered.items():
        (EXPORT_DIR / name).write_text(text)
    print(f"wrote {len(rendered)} files to {EXPORT_DIR.relative_to(ROOT)}: {counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
