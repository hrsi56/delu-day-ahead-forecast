#!/usr/bin/env python3
"""Write the committed MLflow export for `delu-generations` (presentation plan §10, brief §6).

The export is the only payload the publisher ever uploads. It is built from the evidence layer
(`delu_forecast.research`), never from a live computation, and it is committed, so the pre-commit
secret guard reads every byte of it before it can leave this machine.

    uv run python scripts/mlflow_export.py            # write reports/presentation/mlflow-export/
    uv run python scripts/mlflow_export.py --check    # exit 1 if the committed export is stale

Output: one JSON file per checkpoint (`cp10`, `cp15`, `cp16`, `cp20`, `cp21`) with its parent run and
children, and `manifest.json`, which lists the run keys the registry expects, their parents, every metric key
with its unit and history length, every artifact with its SHA-256, and the source blobs behind them.

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
#: The checkpoints the experiment's description names, as it was published on 2026-09-28. Rewriting that description
#: is a write to the experiment itself, which a checkpoint's upload authority (its runs only) does not cover; the
#: description is therefore pinned, and naming a later checkpoint in it waits for an instruction naming that write.
EXPERIMENT_NOTE_CHECKPOINTS = ("CP-10", "CP-15", "CP-16", "CP-20")
EXPERIMENT_TAGS = {
    "mlflow.experimentKind": "custom_model_development",
    "mlflow.note.content": (
        f"The repository {GITHUB_URL} is the source of truth: every run here mirrors its committed "
        "evidence, and every name, status and description comes from its registry. Each policy evaluated "
        "since v1 appears once, nested under the checkpoint that produced it: "
        + "; ".join(G.mlflow_run_name(G.CHECKPOINTS[code].run_key) for code in EXPERIMENT_NOTE_CHECKPOINTS)
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
    # CP-21 tracked its runs while it ran (capstone v21-r6 §17.9) and drafted this export; the publication fills the
    # identities that exist only at landing (the draft's pending fields) and adds nothing else to its records.
    "cp21": {
        "checkpoint": "CP-21",
        "tracked": True,
        "model_code_sha": "260dcf9fb3f5706cb896991ba7b6edf4cd9494b6",
        "evidence_ref": "evidence/cp-21@1d13f99",
        "evidence_tag": "evidence/cp-21",
        # The terminal return: the evidence tip's commit time, 2026-09-30 03:57:44 +03:00.
        "original_completed_utc": "2026-09-30T00:57:44Z",
        "protocol": "reports/block-challenger/protocol.json",
        "anchor_version": "capstone_v21.md v21-r6 §17",
        "report": "reports/block-challenger/report.md",
        "verdict": "docs/track-b/evidence/cp-21/integration.md",
        "landing": "docs/track-b/cp-21-landing-2026-09-30.md",
        "note": (
            "CP-21 added a three-block LightGBM member to v3's blend of two LEAR forecasts (HGL) and compared it with "
            "v3 under the pre-registered rule cp21-adoption; pooled, block and normalized-block LightGBM study arms "
            "attribute the change. HGL met the four conditions of rule cp21-adoption, the third being this "
            "checkpoint's independent Integration PASS, and was adopted in research as v4. The block split (block "
            "against pooled LightGBM) showed no demonstrated joint preference. development_post_selection."
        ),
    },
}

#: The checkpoints whose runs were tracked while they ran and whose export was drafted inside them (CP-21 on): they
#: are built by the draft's own code path, with the registry's entries in place of the draft entries.
TRACKED = tuple(key for key, spec in CHECKPOINTS.items() if spec.get("tracked"))

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


UNIT_RATIO_CHANGE = "change as a share of the comparator's score"


def metric_unit(key: str) -> str:
    """The unit of any exported metric key, including the per-base contrast families."""
    if key in METRIC_UNITS:
        return METRIC_UNITS[key]
    if key.startswith(("ratio_s_mae_vs_", "ratio_s_wis_vs_")):
        return UNIT_RATIO_CHANGE
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


def datasets(checkpoint: str, policy: str, group: dict, *, weather: bool | None = None) -> list[dict]:
    """`log_input` payloads: digests of the population, the market snapshot and (HG, and CP-21's
    weather-using arms via `weather=True`) the weather features. Nothing but names, digests and
    committed source paths."""
    snapshot = json.loads((ROOT / "reports/cp15/protocol.json").read_text())["input_sha256"]["data/snapshot.parquet"]
    out = [
        {"name": group["population_id"], "digest": group["keys_sha256"][:36], "context": "evaluation",
         "source": "reports/cp15/predictions.parquet" if checkpoint != "cp10" else "reports/cp10/predictions.parquet",
         "sha256": group["keys_sha256"], "profile": f"{group['keys']} evaluation hours"},
        {"name": "market-snapshot", "digest": snapshot[:36], "context": "training",
         "source": "data/snapshot.parquet", "sha256": snapshot, "profile": "committed SMARD/ENTSO-E snapshot"},
    ]
    if (policy == "HG") if weather is None else weather:
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
        if checkpoint in TRACKED:
            files[checkpoint] = {"experiment": EXPERIMENT, "checkpoint": CHECKPOINTS[checkpoint]["checkpoint"],
                                 "runs": tracked_runs(checkpoint)}
            continue
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
                    "identity_changes": {}, "substantive_changes": [],
                    # A run the new export adds is not a change to a published record; it is listed, never hidden.
                    "runs_added": sorted(set(new_runs) - set(old_runs))}
    for key in sorted(set(old_runs) | set(new_runs)):
        if key not in new_runs:
            report["substantive_changes"].append(f"{key}: a published run is missing from the new export")
            continue
        if key not in old_runs:
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
    # Every published run survives, and nothing but names, descriptions and tags changed on any of them.
    report["only_identity"] = set(old_runs) <= set(new_runs) and not report["substantive_changes"]
    return report


def export_at(ref: str) -> dict[str, dict]:
    """The committed export at a Git revision, as parsed JSON."""
    import subprocess

    files = {}
    for name in ("manifest", *G.parent_run_keys()):
        shown = subprocess.run(["git", "show", f"{ref}:reports/presentation/mlflow-export/{name}.json"],
                               cwd=ROOT, capture_output=True, text=True)
        if shown.returncode != 0:
            if name == "manifest":
                raise SystemExit(f"{ref} holds no committed export")
            continue  # a checkpoint registered after that revision: its runs are additions, listed as such
        files[name] = json.loads(shown.stdout)
    return files


# --------------------------------------------------------------------------- CP-21 draft (capstone v21-r6 §17.9)
#
# CP-21 registers nothing public: its registry statuses are dated at landing, and registering a
# generation or branch requires its chapter or card. So its export is a *draft*, built by this
# code path from CP-21's committed evidence and the publication packet's draft registry entries
# (reports/block-challenger/draft-registry.json), and kept outside the published set. Identities
# that exist only at landing are explicit pending fields. The publication block regenerates the
# final export, which must equal this draft apart from those fields.

DRAFT_DIR = ROOT / "reports" / "block-challenger" / "mlflow-export-draft"
DRAFT_REGISTRY = "reports/block-challenger/draft-registry.json"
CP21 = {
    "metrics": "reports/block-challenger/metrics.csv",
    "uncertainty": "reports/block-challenger/uncertainty.csv",
    "criteria": "reports/block-challenger/criteria.csv",
    "diagnostics": "reports/block-challenger/diagnostics.csv",
    "protocol": "reports/block-challenger/protocol.json",
}
#: Each CP-21 run's contrasts: (candidate, base code, metric slug).
DRAFT_CONTRASTS = {
    "cp21/HGL": (("HGL", "HG", "v3"),),
    "cp21/L-P": (("L-P", "HG", "v3"), ("L-P", "B3", "b3")),
    "cp21/L-R": (("L-R", "L-P", "l_p"), ("L-R", "HG", "v3")),
    "cp21/L-N": (("L-N", "L-R", "l_r"), ("L-N", "HG", "v3")),
}


def draft_registry() -> tuple[dict, dict[str, G.Entry], G.Checkpoint]:
    """The packet's draft entries as registry `Entry` objects, and CP-21's draft checkpoint."""
    spec = json.loads((ROOT / DRAFT_REGISTRY).read_text())

    def entry(raw: dict) -> G.Entry:
        fields = dict(raw)
        fields["codes"] = tuple(G.Code(**code) for code in raw["codes"])
        fields["statuses"] = tuple(G.StatusEvent(**event) for event in raw["statuses"])
        for key in ("rules", "sources", "run_keys"):
            fields[key] = tuple(raw[key])
        return G.Entry(**fields)

    entries = {raw["id"]: entry(raw) for raw in spec["entries"]}
    checkpoint = G.Checkpoint(**{**spec["checkpoint"], "children": tuple(spec["checkpoint"]["children"])})
    return spec, entries, checkpoint


def _draft_entry_for(run_key: str, entries: dict[str, G.Entry]) -> G.Entry:
    found = [entry for entry in entries.values() if run_key in entry.run_keys]
    if len(found) != 1:
        raise G.RegistryError(f"{run_key}: {len(found)} draft entries own it")
    return found[0]


def draft_run_name(run_key: str, entries: dict[str, G.Entry], checkpoint: G.Checkpoint) -> str:
    """`registry.mlflow_run_name`'s rule, applied to the draft entries."""
    if "/" not in run_key:
        return f"{entries[checkpoint.owner].name} ({checkpoint.code})"
    entry = _draft_entry_for(run_key, entries)
    code = run_key.split("/", 1)[1]
    note = next((c.note for c in entry.codes if c.code == code and c.experiment == checkpoint.code), "")
    if entry.code_in(checkpoint.code) != code:
        raise G.RegistryError(f"{run_key}: {entry.id} has no code {code} in {checkpoint.code}")
    return f"{entry.name} ({code}{', ' + note if note else ''})"


def _draft_records() -> dict[str, R.EvidenceRecord]:
    """CP-21's typed records, built by the evidence layer's own builders from CP-21's committed
    rows, plus one ratio record per equal-fold contrast (§17.5)."""
    windows = R._fold_windows(CP21["metrics"])
    built = (R._metric_records("cp21", "CP-21", CP21["metrics"])
             + R._uncertainty_records("cp21", "CP-21", CP21["uncertainty"], windows)
             + R._criteria_records("cp21", "CP-21", CP21["criteria"], windows)
             + R._diagnostic_records("cp21", "CP-21", CP21["diagnostics"]))
    for line, row in R._rows(CP21["uncertainty"]):
        if row["scope"] != "equal_fold":
            continue
        built.append(R.EvidenceRecord(
            record_id=f"cp21.ratio.{row['candidate']}-{row['baseline']}.{row['metric']}", checkpoint="CP-21",
            generation=None, policy_code=row["candidate"], source_path=CP21["uncertainty"],
            selector=(("scope", "equal_fold"), ("candidate", row["candidate"]), ("baseline", row["baseline"]),
                      ("metric", row["metric"])),
            field="ratio", metric=f"ratio_S_{row['metric']}", unit=UNIT_RATIO_CHANGE, aggregation="equal_fold_ratio",
            population_id="common-10747h", comparator=row["baseline"], evidence_class="development_post_selection",
            window=windows["all"], display_precision=4, raw=row["ratio"], source_line=line,
            ci_low_raw=row["ratio_ci_lower"], ci_high_raw=row["ratio_ci_upper"]))
    out: dict[str, R.EvidenceRecord] = {}
    for record in built:
        if record.record_id in out:
            raise R.EvidenceError(f"duplicate draft record id {record.record_id}")
        out[record.record_id] = record
    return out


class DraftBuilder(Builder):
    """`Builder`, reading CP-21's draft records instead of the published evidence layer."""

    def __init__(self, records: dict[str, R.EvidenceRecord]) -> None:
        super().__init__()
        self.records = records

    def single(self, key: str, record_id: str, which: str = "value") -> None:
        self._add(key, _point(self.records[record_id], 0, which), f"{record_id}#{which}")

    def per_fold(self, key: str, pattern: str, which: str = "value") -> None:
        for index, fold in enumerate(FOLDS, start=1):
            record_id = pattern.format(fold=fold)
            self._add(key, _point(self.records[record_id], index, which), f"{record_id}#{which}")

    def daily(self, path: str, policy: str) -> None:
        points = []
        for _line, row in R._rows(path):
            if row["policy"] != policy or row["scope"] != "daily" or int(float(row["n_hours"])) == 0 or row["MAE"] == "":
                continue
            points.append((row["delivery_date"], row["MAE"]))
        points.sort()
        for index, (day, raw) in enumerate(points):
            self.metrics.setdefault("daily_mae_eur", []).append({"step": index, "timestamp": _ms(day), "value": float(raw)})
        self.provenance["daily_mae_eur"] = [f"{path} (policy {policy}, {len(points)} daily rows)"]


def _draft_scores(builder: DraftBuilder, run_key: str, policy: str) -> None:
    equal, pooled = f"cp21.metrics.{policy}.equal_fold", f"cp21.metrics.{policy}.pooled"
    fold, peak = f"cp21.metrics.{policy}.{{fold}}", f"cp21.diagnostics.{policy}.peak"
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
    builder.daily(CP21["diagnostics"], policy)
    for candidate, base, slug in DRAFT_CONTRASTS[run_key]:
        prefix = f"cp21.uncertainty.{candidate}-{base}"
        for metric, score in (("MAE", "mae"), ("WIS", "wis")):
            equal_record = f"{prefix}.equal_fold.{metric}"
            builder.single(f"delta_s_{score}_vs_{slug}", equal_record)
            builder.single(f"delta_s_{score}_vs_{slug}_ci_low", equal_record, "ci_low")
            builder.single(f"delta_s_{score}_vs_{slug}_ci_high", equal_record, "ci_high")
            ratio = f"cp21.ratio.{candidate}-{base}.{metric}"
            builder.single(f"ratio_s_{score}_vs_{slug}", ratio)
            builder.single(f"ratio_s_{score}_vs_{slug}_ci_low", ratio, "ci_low")
            builder.single(f"ratio_s_{score}_vs_{slug}_ci_high", ratio, "ci_high")
            fold_pattern = f"{prefix}.{{fold}}.{metric}"
            builder.per_fold(f"delta_fold_{score}_eur_vs_{slug}", fold_pattern)
            builder.per_fold(f"delta_fold_{score}_eur_vs_{slug}_ci_low", fold_pattern, "ci_low")
            builder.per_fold(f"delta_fold_{score}_eur_vs_{slug}_ci_high", fold_pattern, "ci_high")


def _draft_blobs(provenance: dict[str, list[str]], records: dict[str, R.EvidenceRecord]) -> dict[str, str]:
    """Each source file's Git blob SHA, computed from its committed bytes (no tag exists yet)."""
    paths = set()
    for sources in provenance.values():
        for source in sources:
            paths.add(source.split(" (policy ")[0] if " (policy " in source else records[source.split("#")[0]].source_path)
    return {path: R.blob_sha(R.source_bytes(path)) for path in sorted(paths)}


def _draft_status_text(entry: G.Entry, pending: str) -> str:
    return f"{entry.status.status} {entry.status.date}" if entry.status.date != pending else f"{entry.status.status} ({pending})"


def _draft_description(entry: G.Entry, note: str, pending: str, *, code: str | None = None, role: str | None = None) -> str:
    parts = [f"{entry.name}: {entry.subtitle}."]
    parts.append(G.status_sentence(entry) if entry.status.date != pending
                 else f"Its status, {entry.status.status}, is dated at landing ({pending}).")
    if code is not None:
        parts.append(f"Code {code}; role {role}.")
    parts.append(note)
    return " ".join(parts)


def _draft_params(protocol: dict, policy: str | None) -> dict[str, str]:
    cp15 = json.loads((ROOT / "reports/cp15/protocol.json").read_text())
    out = {"anchor_version": "capstone_v21.md v21-r6 §17", "protocol_sha256": _file_sha256(CP21["protocol"])}
    if policy is None:
        return out
    out["quantile_set"] = ",".join(str(level) for level in cp15["quantiles"]["levels"])
    out["seed"] = str(protocol["lgbm"]["seed"])
    out["weather_features"] = ",".join(protocol["features"]["weather"]) + " plus missing indicators"
    out["history_window"] = protocol["history"]["window"]
    out["interval_method"] = protocol["h_layer"]["recipe"]
    out["policy_definition"] = protocol["arms"][policy]
    if policy in ("L-P", "L-R", "L-N", "HGL"):
        out["lightgbm"] = "CP-15 B3/A2 recipe, " + protocol["lgbm"]["changed"]
        out["capacity_grid"] = json.dumps(protocol["capacity_grid"], separators=(",", ":"))
        out["capacity_selection"] = protocol["selection"]["inner_split"] + "; " + protocol["selection"]["tie"]
    if policy in ("L-R", "L-N", "HGL"):
        out["blocks"] = json.dumps(protocol["blocks"], separators=(",", ":"))
    if policy == "L-N":
        out["target_transform"] = cp15["normalization"]["target"]
    if policy == "HGL":
        out["blend"] = protocol["blend"]["float_expression"]
    return {key: value[:500] for key, value in out.items()}


def _tracked_runs(entries: dict[str, G.Entry], checkpoint: G.Checkpoint, ident: dict, *,
                  pending: str | None, charts: bool) -> list[dict]:
    """A tracked checkpoint's parent and children, from its committed evidence. `ident` supplies the identities that
    exist only at landing (model code SHA, evidence reference, completion time) and the note; with `pending` they are
    the draft's explicit pending fields, and the published export fills them. Nothing else differs, except that the
    published candidate run carries the page's charts of its chapter (plan §10.6), which no draft could hold."""
    protocol = json.loads((ROOT / CP21["protocol"]).read_text())
    records = _draft_records()
    group = comparability()["common"]
    note = ident["note"]

    def status(entry: G.Entry) -> str:
        return _draft_status_text(entry, pending) if pending else _status_text(entry)

    def describe(entry: G.Entry, **kwargs) -> str:
        return _draft_description(entry, note, pending, **kwargs) if pending else _description(entry, note, **kwargs)

    def readme(run_name: str, blobs: dict[str, str]) -> str:
        return (_draft_readme(run_name, checkpoint, ident, blobs) if pending
                else _tracked_readme(run_name, checkpoint, blobs))

    completed = pending or ident["original_completed_utc"]
    runs = []
    owner = entries[checkpoint.owner]
    parent_tags = {
        "delu.run_key": checkpoint.run_key, "delu.checkpoint": checkpoint.code, "delu.registry_id": owner.id,
        "delu.kind": owner.kind, "delu.public_name": owner.name, "delu.status": status(owner),
        "delu.role": "checkpoint", "delu.evidence_class": "development_post_selection",
        "delu.population_id": group["population_id"], "delu.comparability_id": group["comparability_id"],
        "delu.model_code_sha": ident["model_code_sha"], "delu.evidence_ref": ident["evidence_ref"],
        "delu.backfilled": "false", "delu.original_completed_utc": completed,
        "delu.children": ",".join(f"{checkpoint.run_key}/{code}" for code in checkpoint.children),
        "mlflow.note.content": describe(owner),
    }
    parent = {"run_key": checkpoint.run_key, "parent": None,
              "run_name": draft_run_name(checkpoint.run_key, entries, checkpoint),
              "params": _draft_params(protocol, None), "tags": parent_tags, "metrics": {}, "metric_provenance": {},
              "metric_units": {}, "inputs": [], "comparability": dict(group)}
    parent["artifacts"] = [
        _artifact("summary.json", _canonical({k: v for k, v in parent.items() if k != "metric_provenance"}) + "\n"),
        _artifact("README.md", readme(parent["run_name"], {CP21["protocol"]: R.blob_sha(R.source_bytes(CP21["protocol"]))})),
    ]
    runs.append(parent)
    for code in checkpoint.children:
        run_key = f"{checkpoint.run_key}/{code}"
        entry = _draft_entry_for(run_key, entries)
        builder = DraftBuilder(records)
        _draft_scores(builder, run_key, code)
        blobs = _draft_blobs(builder.provenance, records)
        run_name = draft_run_name(run_key, entries, checkpoint)
        comparator = G.get(entry.comparator).name if entry.comparator in {e.id for e in G.entries()} else entries[entry.comparator].name
        tags = {
            "delu.run_key": run_key, "delu.checkpoint": checkpoint.code, "delu.registry_id": entry.id,
            "delu.kind": entry.kind, "delu.generation": entry.version or "none", "delu.policy_code": code,
            "delu.public_name": entry.name, "delu.status": status(entry), "delu.comparator": comparator,
            "delu.role": "candidate", "delu.adopted": G.adopted_flag(entry),
            "delu.evidence_class": "development_post_selection",
            "delu.population_id": group["population_id"], "delu.comparability_id": group["comparability_id"],
            "delu.model_code_sha": ident["model_code_sha"], "delu.evidence_ref": ident["evidence_ref"],
            "delu.source_blobs": _canonical(blobs), "delu.backfilled": "false", "delu.original_completed_utc": completed,
            "mlflow.note.content": describe(entry, code=code, role="candidate"),
        }
        inputs = datasets("cp21", code, group, weather=True)
        tags["delu.datasets"] = _canonical({dataset["name"]: dataset["sha256"] for dataset in inputs})
        run = {"run_key": run_key, "parent": checkpoint.run_key, "run_name": run_name,
               "params": _draft_params(protocol, code), "tags": tags, "metrics": builder.metrics,
               "metric_provenance": builder.provenance,
               "metric_units": {key: metric_unit(key) for key in builder.metrics}, "inputs": inputs}
        summary = _canonical({k: v for k, v in run.items() if k != "metric_provenance"})
        chart_files = ([(f"charts/{chart_id}.svg", build_pages.standalone_svg(build()))
                        for chart_id, build in build_pages.CHARTS_BY_RUN.get(run_key, ())] if charts else [])
        text = readme(run_name, blobs)
        if chart_files:
            text += ("\nCharts, drawn by the page build from the same records as the report:\n\n"
                     + "".join(f"- `{path}`\n" for path, _ in chart_files))
        run["artifacts"] = ([_artifact("summary.json", summary + "\n"), _artifact("README.md", text)]
                            + [_artifact(path, content) for path, content in chart_files])
        runs.append(run)
    return runs


def _tracked_readme(run_name: str, checkpoint: G.Checkpoint, blobs: dict[str, str]) -> str:
    """The draft's README with its pending identities filled: the evidence tag's commit and the landing record."""
    tag = checkpoint.evidence_tag
    lines = [f"# {run_name}", "",
             f"Tracked by {checkpoint.code} from its committed evidence (evidence tag `{tag}` at commit "
             f"`{checkpoint.evidence_sha}`). Development evidence; nothing here is a live or confirmatory result.", "",
             f"- Report: {GITHUB_URL}/blob/{tag}/{checkpoint.report}",
             f"- Independent Integration review: {GITHUB_URL}/blob/{tag}/{checkpoint.verdict}",
             f"- Landing record: {GITHUB_URL}/blob/main/{checkpoint.landing}", f"- Presentation: {PAGES_URL}", "",
             "Source rows at the evidence tag:", ""]
    lines += [f"- {GITHUB_URL}/blob/{tag}/{path} (blob {blob})" for path, blob in blobs.items()]
    return "\n".join(lines) + "\n"


def tracked_runs(key: str) -> list[dict]:
    """A tracked checkpoint's published runs: the draft's code path, with the registry's entries and identities."""
    checkpoint = G.CHECKPOINTS[CHECKPOINTS[key]["checkpoint"]]
    entries = {entry.id: entry for entry in G.entries() if any(run.split("/")[0] == key for run in entry.run_keys)}
    return _tracked_runs(entries, checkpoint, CHECKPOINTS[key], pending=None, charts=True)


def build_draft(name: str = "cp21") -> dict:
    """CP-21's draft export: one file, the checkpoint's parent and its four new policies (CP-22: `build_draft22`)."""
    if name == "cp22":
        return build_draft22()
    if name == "cp23":
        return build_draft23()
    if name != "cp21":
        raise SystemExit("the draft exports are cp21, cp22 and cp23")
    spec, entries, checkpoint = draft_registry()
    runs = _tracked_runs(entries, checkpoint, spec, pending=spec["pending"], charts=False)
    return {"experiment": EXPERIMENT, "checkpoint": checkpoint.code, "status": "draft",
            "pending_fields": spec["pending_fields"], "draft_registry": DRAFT_REGISTRY, "runs": runs}


#: The run tags that carry the draft's pending identities (publication packet §6), and so may differ between the draft
#: and the published export; every other field of every run must be equal.
PENDING_TAGS = ("delu.status", "delu.evidence_ref", "delu.model_code_sha", "delu.original_completed_utc",
                "mlflow.note.content")
#: The README lines that name a pending identity: the evidence tag's commit and the landing record.
PENDING_README_PREFIXES = ("Tracked by ", "- Landing record: ")


def final_vs_draft(draft: dict, runs: list[dict]) -> dict:
    """Compare the published runs of a tracked checkpoint with its draft, record by record (research anchor §17.9):
    the final export must equal the draft apart from the pending fields. Reports every other difference; the only
    addition allowed is a chart artifact the page build draws for the candidate run (plan §10.6)."""
    old = {run["run_key"]: run for run in draft["runs"]}
    new = {run["run_key"]: run for run in runs}
    report: dict = {"run_keys_equal": sorted(old) == sorted(new), "pending_fields": sorted(draft.get("pending_fields", {})),
                    "filled": {}, "chart_artifacts_added": {}, "differences": []}
    for key in sorted(set(old) | set(new)):
        if key not in old or key not in new:
            report["differences"].append(f"{key}: present in only one export")
            continue
        a, b = old[key], new[key]
        for field in ("parent", "run_name", "params", "metrics", "metric_provenance", "metric_units", "inputs",
                      "comparability"):
            if a.get(field) != b.get(field):
                report["differences"].append(f"{key}: {field}")
        for tag in sorted(set(a["tags"]) | set(b["tags"])):
            if a["tags"].get(tag) == b["tags"].get(tag):
                continue
            if (tag in PENDING_TAGS and "pending-at-landing" in str(a["tags"].get(tag))
                    and "pending-at-landing" not in str(b["tags"].get(tag))):
                report["filled"].setdefault(key, []).append(tag)
            else:
                report["differences"].append(f"{key}: tag {tag}")
        old_art = {art["path"]: art for art in a["artifacts"]}
        new_art = {art["path"]: art for art in b["artifacts"]}
        for path in sorted(set(old_art) - set(new_art)):
            report["differences"].append(f"{key}: artifact {path} missing")
        charted = {f"charts/{chart_id}.svg" for chart_id, _ in build_pages.CHARTS_BY_RUN.get(key, ())}
        for path in sorted(set(new_art) - set(old_art)):
            if path in charted:
                report["chart_artifacts_added"].setdefault(key, []).append(path)
            else:
                report["differences"].append(f"{key}: artifact {path} added")
        if "summary.json" in old_art and "summary.json" in new_art:
            body = json.loads(new_art["summary.json"]["content"])
            body["tags"] = {tag: (a["tags"].get(tag) if tag in PENDING_TAGS else value)
                            for tag, value in body["tags"].items()}
            if sha256_text(_canonical(body) + "\n") != old_art["summary.json"]["sha256"]:
                report["differences"].append(f"{key}: summary.json beyond the pending tags")
        if "README.md" in old_art and "README.md" in new_art:
            def lines(text: str) -> list[str]:
                kept = text.split("\nCharts, drawn by the page build")[0].splitlines()
                return [line for line in kept if not line.startswith(PENDING_README_PREFIXES)]
            if lines(old_art["README.md"]["content"]) != lines(new_art["README.md"]["content"]):
                report["differences"].append(f"{key}: README.md beyond the pending identities")
    report["equal_apart_from_pending"] = report["run_keys_equal"] and not report["differences"]
    return report


def _draft_readme(run_name: str, checkpoint: G.Checkpoint, spec: dict, blobs: dict[str, str]) -> str:
    tag = checkpoint.evidence_tag
    lines = [f"# {run_name}", "",
             f"Tracked by CP-21 from its committed evidence (draft export; evidence tag `{tag}` and its commit are "
             f"{spec['pending']}). Development evidence; nothing here is a live or confirmatory result.", "",
             f"- Report: {GITHUB_URL}/blob/{tag}/{checkpoint.report}",
             f"- Independent Integration review: {GITHUB_URL}/blob/{tag}/{checkpoint.verdict}",
             f"- Landing record: {checkpoint.landing}", f"- Presentation: {PAGES_URL}", "",
             "Source rows at the evidence tag:", ""]
    lines += [f"- {GITHUB_URL}/blob/{tag}/{path} (blob {blob})" for path, blob in blobs.items()]
    return "\n".join(lines) + "\n"


def draft_problems(draft: dict) -> list[str]:
    """The draft matches its draft entries: the run keys the draft checkpoint expects, each once,
    each parent CP-21's, each name the rule applied to its entry. Never a count."""
    _, entries, checkpoint = {"CP-22": draft_registry22, "CP-23": draft_registry23}.get(draft.get("checkpoint"), draft_registry)()
    keys = [run["run_key"] for run in draft["runs"]]
    expected = [checkpoint.run_key] + [f"{checkpoint.run_key}/{code}" for code in checkpoint.children]
    problems = []
    if sorted(keys) != sorted(expected) or len(keys) != len(set(keys)):
        problems.append(f"run keys differ from the draft checkpoint: {keys}")
    for run in draft["runs"]:
        if run["run_name"] != draft_run_name(run["run_key"], entries, checkpoint):
            problems.append(f"{run['run_key']}: run name is not the draft entry's")
        want = None if "/" not in run["run_key"] else checkpoint.run_key
        if run["parent"] != want:
            problems.append(f"{run['run_key']}: parent {run['parent']!r}")
    return problems


# --------------------------------------------------------------------------- CP-22 draft (capstone v21-r9 §20.9)
#
# CP-22 registers nothing public either: its draft export is built by the same code path as CP-21's, from CP-22's
# committed evidence and the packet's draft entries (reports/v4-revision/draft-registry.json), outside the published
# set. Under a replacement, v4 keeps its number and gains a dated revision (PUBLISH_RULES 1.3 A10): the current
# revision's run is a child of `cp22`, and CP-21's published runs, the superseded revision's, are untouched.

DRAFT22_DIR = ROOT / "reports" / "v4-revision" / "mlflow-export-draft"
DRAFT22_REGISTRY = "reports/v4-revision/draft-registry.json"
CP22 = {
    "metrics": "reports/v4-revision/metrics.csv",
    "uncertainty": "reports/v4-revision/uncertainty.csv",
    "criteria": "reports/v4-revision/criteria.csv",
    "diagnostics": "reports/v4-revision/diagnostics.csv",
    "protocol": "reports/v4-revision/protocol.json",
    "decisions": "reports/v4-revision/decisions.json",
}
#: Each CP-22 run's contrasts: (candidate, base code, metric slug); "W" is the replacement, when one exists.
DRAFT22_CONTRASTS = {
    "R": (("R", "HGL", "v4"), ("R", "HG", "v3"), ("R", "M", "m"), ("R", "A-PN-sel", "a_pn_sel")),
    "M": (("M", "HGL", "v4"), ("M", "HG", "v3")),
    "A-PN-sel": (("A-PN-sel", "M", "m"), ("A-PN-sel", "A-LP", "a_lp"), ("A-PN-sel", "HG", "v3")),
    "A-LP": (("A-LP", "HG", "v3"),),
    "A-LN": (("A-LN", "HGL", "v4"), ("A-LN", "HG", "v3")),
    "v4+DL": (("v4+DL", "HGL", "v4"), ("v4+DL", "HG", "v3")),
    "v3+DL": (("v3+DL", "HG", "v3"),),
    "W+ACI": (("W+ACI", "W", "w"), ("W+ACI", "HG", "v3")),
    "W+DL": (("W+DL", "W", "w"), ("W+DL", "W+ACI", "w_aci"), ("W+DL", "HG", "v3")),
    "W+DLF": (("W+DLF", "W+DL", "w_dl"), ("W+DLF", "HG", "v3")),
}


def draft_registry22() -> tuple[dict, dict[str, G.Entry], G.Checkpoint]:
    """CP-22's draft entries as registry `Entry` objects, and its draft checkpoint."""
    spec = json.loads((ROOT / DRAFT22_REGISTRY).read_text())

    def entry(raw: dict) -> G.Entry:
        fields = dict(raw)
        fields["codes"] = tuple(G.Code(**code) for code in raw["codes"])
        fields["statuses"] = tuple(G.StatusEvent(**event) for event in raw["statuses"])
        for key in ("rules", "sources", "run_keys"):
            fields[key] = tuple(raw[key])
        return G.Entry(**fields)

    entries = {raw["id"]: entry(raw) for raw in spec["entries"]}
    checkpoint = G.Checkpoint(**{**spec["checkpoint"], "children": tuple(spec["checkpoint"]["children"])})
    return spec, entries, checkpoint


def _interval22() -> R.Interval:
    settings = json.loads((ROOT / CP22["protocol"]).read_text())["uncertainty"]
    return R.Interval(method="paired noncircular moving-block percentile bootstrap", level=0.95, seed=int(settings["seed"]),
                      replicates=int(settings["replicates"]), block_days=int(settings["block_days"]))


def _draft22_records() -> dict[str, R.EvidenceRecord]:
    """CP-22's typed records, by the evidence layer's own builders from CP-22's committed rows, with CP-22's own
    bootstrap settings (its frozen protocol), plus one ratio record per equal-fold contrast (§17.5)."""
    import dataclasses
    interval = _interval22()
    windows = R._fold_windows(CP22["metrics"])
    built = (R._metric_records("cp22", "CP-22", CP22["metrics"])
             + [dataclasses.replace(r, interval=interval)
                for r in R._uncertainty_records("cp22", "CP-22", CP22["uncertainty"], windows)]
             + R._criteria_records("cp22", "CP-22", CP22["criteria"], windows)
             + R._diagnostic_records("cp22", "CP-22", CP22["diagnostics"]))
    for line, row in R._rows(CP22["uncertainty"]):
        if row["scope"] != "equal_fold":
            continue
        built.append(R.EvidenceRecord(
            record_id=f"cp22.ratio.{row['candidate']}-{row['baseline']}.{row['metric']}", checkpoint="CP-22",
            generation=None, policy_code=row["candidate"], source_path=CP22["uncertainty"],
            selector=(("scope", "equal_fold"), ("candidate", row["candidate"]), ("baseline", row["baseline"]),
                      ("metric", row["metric"])),
            field="ratio", metric=f"ratio_S_{row['metric']}", unit=UNIT_RATIO_CHANGE, aggregation="equal_fold_ratio",
            population_id="common-10747h", comparator=row["baseline"], evidence_class="development_post_selection",
            window=windows["all"], display_precision=4, raw=row["ratio"], source_line=line, interval=interval,
            ci_low_raw=row["ratio_ci_lower"], ci_high_raw=row["ratio_ci_upper"]))
    out: dict[str, R.EvidenceRecord] = {}
    for record in built:
        if record.record_id in out:
            raise R.EvidenceError(f"duplicate draft record id {record.record_id}")
        out[record.record_id] = record
    return out


def _draft22_scores(builder: DraftBuilder, code: str, winner: str | None) -> None:
    equal, pooled = f"cp22.metrics.{code}.equal_fold", f"cp22.metrics.{code}.pooled"
    fold, peak = f"cp22.metrics.{code}.{{fold}}", f"cp22.diagnostics.{code}.peak"
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
    builder.daily(CP22["diagnostics"], code)
    for candidate, base, slug in DRAFT22_CONTRASTS[code]:
        base = winner if base == "W" else base
        prefix = f"cp22.uncertainty.{candidate}-{base}"
        for metric, score in (("MAE", "mae"), ("WIS", "wis")):
            equal_record = f"{prefix}.equal_fold.{metric}"
            builder.single(f"delta_s_{score}_vs_{slug}", equal_record)
            builder.single(f"delta_s_{score}_vs_{slug}_ci_low", equal_record, "ci_low")
            builder.single(f"delta_s_{score}_vs_{slug}_ci_high", equal_record, "ci_high")
            ratio = f"cp22.ratio.{candidate}-{base}.{metric}"
            builder.single(f"ratio_s_{score}_vs_{slug}", ratio)
            builder.single(f"ratio_s_{score}_vs_{slug}_ci_low", ratio, "ci_low")
            builder.single(f"ratio_s_{score}_vs_{slug}_ci_high", ratio, "ci_high")
            fold_pattern = f"{prefix}.{{fold}}.{metric}"
            builder.per_fold(f"delta_fold_{score}_eur_vs_{slug}", fold_pattern)
            builder.per_fold(f"delta_fold_{score}_eur_vs_{slug}_ci_low", fold_pattern, "ci_low")
            builder.per_fold(f"delta_fold_{score}_eur_vs_{slug}_ci_high", fold_pattern, "ci_high")


def _draft22_params(protocol: dict, code: str | None, winner: str | None) -> dict[str, str]:
    cp15 = json.loads((ROOT / "reports/cp15/protocol.json").read_text())
    out = {"anchor_version": "capstone_v21.md v21-r9 §20", "protocol_sha256": _file_sha256(CP22["protocol"])}
    if code is None:
        return out
    policy = protocol["policies"][code]
    layers = protocol["interval_layers"]
    central = policy["central"] if policy["central"] != "W" else f"W = {winner}: {protocol['policies'][winner]['central']}"
    out["quantile_set"] = ",".join(str(level) for level in cp15["quantiles"]["levels"])
    out["seed"] = str(protocol["lgbm"]["seed"])
    out["weather_features"] = "v3's three GFS columns plus missing indicators"
    out["history_window"] = protocol["history"]["window"]
    out["policy_definition"] = f"{policy['role']}; central {central}"
    out["member_weight"] = protocol["member_weight"]
    if policy["layer"] == "H":
        out["interval_method"] = layers["H"]
    else:
        dl = layers["DL"]
        out["interval_method"] = (f"{policy['layer']}: " + (layers["ACI"] if policy["layer"] == "ACI" else dl["recency_weight"]))
        out["aci"] = (f"gamma {dl['aci']['gamma_per_day']} per day; clip {json.dumps(dl['aci']['clip'], separators=(',', ':'))}; "
                      f"{dl['aci']['update']}")
        if policy["layer"] == "DLF":
            out["fast_component"] = layers["DLF"]["weights"]
    if code in ("R", "M", "A-PN-sel") or (code.startswith("W") and winner in ("R", "M")):
        out["pn"] = protocol["members"]["PN"]
        out["capacity_grid"] = json.dumps(protocol["capacity_grid"], separators=(",", ":"))
        out["capacity_selection"] = protocol["selection"]["inner_split"] + "; " + protocol["selection"]["tie"]
    return {key: value[:500] for key, value in out.items()}


def _draft22_readme(run_name: str, checkpoint: G.Checkpoint, spec: dict, blobs: dict[str, str]) -> str:
    tag = checkpoint.evidence_tag
    lines = [f"# {run_name}", "",
             f"Tracked by CP-22 from its committed evidence (draft export; evidence tag `{tag}` and its commit are "
             f"{spec['pending']}). Development evidence; nothing here is a live or confirmatory result.", "",
             f"- Report: {GITHUB_URL}/blob/{tag}/{checkpoint.report}",
             f"- Independent Integration review: {GITHUB_URL}/blob/{tag}/{checkpoint.verdict}",
             f"- Landing record: {checkpoint.landing}", f"- Presentation: {PAGES_URL}", "",
             "Source rows at the evidence tag:", ""]
    lines += [f"- {GITHUB_URL}/blob/{tag}/{path} (blob {blob})" for path, blob in blobs.items()]
    return "\n".join(lines) + "\n"


def _draft22_runs(entries: dict[str, G.Entry], checkpoint: G.Checkpoint, spec: dict) -> list[dict]:
    """CP-22's parent and children, from its committed evidence, with the draft's explicit pending fields."""
    protocol = json.loads((ROOT / CP22["protocol"]).read_text())
    winner = json.loads((ROOT / CP22["decisions"]).read_text())["replacement"]["winner"]
    records = _draft22_records()
    group = comparability()["common"]
    pending = spec["pending"]
    note = spec["note"]
    runs = []
    owner = entries[checkpoint.owner]
    parent_tags = {
        "delu.run_key": checkpoint.run_key, "delu.checkpoint": checkpoint.code, "delu.registry_id": owner.id,
        "delu.kind": owner.kind, "delu.public_name": owner.name, "delu.status": _draft_status_text(owner, pending),
        "delu.role": "checkpoint", "delu.evidence_class": "development_post_selection",
        "delu.population_id": group["population_id"], "delu.comparability_id": group["comparability_id"],
        "delu.model_code_sha": spec["model_code_sha"], "delu.evidence_ref": spec["evidence_ref"],
        "delu.backfilled": "false", "delu.original_completed_utc": pending,
        "delu.children": ",".join(f"{checkpoint.run_key}/{code}" for code in checkpoint.children),
        "mlflow.note.content": _draft_description(owner, note, pending),
    }
    parent = {"run_key": checkpoint.run_key, "parent": None,
              "run_name": draft_run_name(checkpoint.run_key, entries, checkpoint),
              "params": _draft22_params(protocol, None, winner), "tags": parent_tags, "metrics": {}, "metric_provenance": {},
              "metric_units": {}, "inputs": [], "comparability": dict(group)}
    parent["artifacts"] = [
        _artifact("summary.json", _canonical({k: v for k, v in parent.items() if k != "metric_provenance"}) + "\n"),
        _artifact("README.md", _draft22_readme(parent["run_name"], checkpoint, spec,
                                               {CP22["protocol"]: R.blob_sha(R.source_bytes(CP22["protocol"]))})),
    ]
    runs.append(parent)
    for code in checkpoint.children:
        run_key = f"{checkpoint.run_key}/{code}"
        entry = _draft_entry_for(run_key, entries)
        builder = DraftBuilder(records)
        _draft22_scores(builder, code, winner)
        blobs = _draft_blobs(builder.provenance, records)
        run_name = draft_run_name(run_key, entries, checkpoint)
        comparator = G.get(entry.comparator).name if entry.comparator in {e.id for e in G.entries()} else entries[entry.comparator].name
        tags = {
            "delu.run_key": run_key, "delu.checkpoint": checkpoint.code, "delu.registry_id": entry.id,
            "delu.kind": entry.kind, "delu.generation": entry.version or "none", "delu.policy_code": code,
            "delu.public_name": entry.name, "delu.status": _draft_status_text(entry, pending), "delu.comparator": comparator,
            "delu.role": "candidate", "delu.adopted": G.adopted_flag(entry),
            "delu.evidence_class": "development_post_selection",
            "delu.population_id": group["population_id"], "delu.comparability_id": group["comparability_id"],
            "delu.model_code_sha": spec["model_code_sha"], "delu.evidence_ref": spec["evidence_ref"],
            "delu.source_blobs": _canonical(blobs), "delu.backfilled": "false", "delu.original_completed_utc": pending,
            "mlflow.note.content": _draft_description(entry, note, pending, code=code, role="candidate"),
        }
        inputs = datasets("cp22", code, group, weather=True)
        tags["delu.datasets"] = _canonical({dataset["name"]: dataset["sha256"] for dataset in inputs})
        run = {"run_key": run_key, "parent": checkpoint.run_key, "run_name": run_name,
               "params": _draft22_params(protocol, code, winner), "tags": tags, "metrics": builder.metrics,
               "metric_provenance": builder.provenance,
               "metric_units": {key: metric_unit(key) for key in builder.metrics}, "inputs": inputs}
        summary = _canonical({k: v for k, v in run.items() if k != "metric_provenance"})
        run["artifacts"] = [_artifact("summary.json", summary + "\n"),
                            _artifact("README.md", _draft22_readme(run_name, checkpoint, spec, blobs))]
        runs.append(run)
    return runs


def build_draft22() -> dict:
    """CP-22's draft export: one file, the checkpoint's parent and every new policy."""
    spec, entries, checkpoint = draft_registry22()
    return {"experiment": EXPERIMENT, "checkpoint": checkpoint.code, "status": "draft",
            "pending_fields": spec["pending_fields"], "draft_registry": DRAFT22_REGISTRY,
            "revisions": spec.get("revisions"), "runs": _draft22_runs(entries, checkpoint, spec)}


# --------------------------------------------------------------------------- CP-23 draft (capstone v21-r10 §21.9)
#
# CP-23 registers nothing public either: its draft export is built by the same code path as CP-21's and CP-22's, from
# CP-23's committed evidence and the packet's draft entries (reports/distribution-challenger/draft-registry.json),
# outside the published set. Adopted, v5 is a generation with predecessor v4; otherwise the branch "DDNN member on v4"
# owns the checkpoint and v5's run. D and v3+D are study arms either way.

DRAFT23_DIR = ROOT / "reports" / "distribution-challenger" / "mlflow-export-draft"
DRAFT23_REGISTRY = "reports/distribution-challenger/draft-registry.json"
CP23 = {
    "metrics": "reports/distribution-challenger/metrics.csv",
    "uncertainty": "reports/distribution-challenger/uncertainty.csv",
    "criteria": "reports/distribution-challenger/criteria.csv",
    "diagnostics": "reports/distribution-challenger/diagnostics.csv",
    "protocol": "reports/distribution-challenger/protocol.json",
    "decisions": "reports/distribution-challenger/decisions.json",
}
#: Each CP-23 run's contrasts (§21.5): (candidate, base code, metric slug).
DRAFT23_CONTRASTS = {
    "v5": (("v5", "HGL", "v4"), ("v5", "HG", "v3"), ("v5", "v3+D", "v3_d")),
    "D": (("D", "HGL", "v4"), ("D", "HG", "v3")),
    "v3+D": (("v3+D", "HG", "v3"),),
}


def draft_registry23() -> tuple[dict, dict[str, G.Entry], G.Checkpoint]:
    """CP-23's draft entries as registry `Entry` objects, and its draft checkpoint."""
    spec = json.loads((ROOT / DRAFT23_REGISTRY).read_text())

    def entry(raw: dict) -> G.Entry:
        fields = dict(raw)
        fields["codes"] = tuple(G.Code(**code) for code in raw["codes"])
        fields["statuses"] = tuple(G.StatusEvent(**event) for event in raw["statuses"])
        for key in ("rules", "sources", "run_keys"):
            fields[key] = tuple(raw[key])
        return G.Entry(**fields)

    entries = {raw["id"]: entry(raw) for raw in spec["entries"]}
    checkpoint = G.Checkpoint(**{**spec["checkpoint"], "children": tuple(spec["checkpoint"]["children"])})
    return spec, entries, checkpoint


def _interval23() -> R.Interval:
    settings = json.loads((ROOT / CP23["protocol"]).read_text())["uncertainty"]
    return R.Interval(method="paired noncircular moving-block percentile bootstrap", level=0.95, seed=int(settings["seed"]),
                      replicates=int(settings["replicates"]), block_days=int(settings["block_days"]))


def _draft23_records() -> dict[str, R.EvidenceRecord]:
    """CP-23's typed records, by the evidence layer's own builders from CP-23's committed rows, with CP-23's own
    bootstrap settings (its frozen protocol), plus one ratio record per equal-fold contrast (§17.5)."""
    import dataclasses
    interval = _interval23()
    windows = R._fold_windows(CP23["metrics"])
    built = (R._metric_records("cp23", "CP-23", CP23["metrics"])
             + [dataclasses.replace(r, interval=interval)
                for r in R._uncertainty_records("cp23", "CP-23", CP23["uncertainty"], windows)]
             + R._criteria_records("cp23", "CP-23", CP23["criteria"], windows)
             + R._diagnostic_records("cp23", "CP-23", CP23["diagnostics"]))
    for line, row in R._rows(CP23["uncertainty"]):
        if row["scope"] != "equal_fold":
            continue
        built.append(R.EvidenceRecord(
            record_id=f"cp23.ratio.{row['candidate']}-{row['baseline']}.{row['metric']}", checkpoint="CP-23",
            generation=None, policy_code=row["candidate"], source_path=CP23["uncertainty"],
            selector=(("scope", "equal_fold"), ("candidate", row["candidate"]), ("baseline", row["baseline"]),
                      ("metric", row["metric"])),
            field="ratio", metric=f"ratio_S_{row['metric']}", unit=UNIT_RATIO_CHANGE, aggregation="equal_fold_ratio",
            population_id="common-10747h", comparator=row["baseline"], evidence_class="development_post_selection",
            window=windows["all"], display_precision=4, raw=row["ratio"], source_line=line, interval=interval,
            ci_low_raw=row["ratio_ci_lower"], ci_high_raw=row["ratio_ci_upper"]))
    out: dict[str, R.EvidenceRecord] = {}
    for record in built:
        if record.record_id in out:
            raise R.EvidenceError(f"duplicate draft record id {record.record_id}")
        out[record.record_id] = record
    return out


def _draft23_scores(builder: DraftBuilder, code: str) -> None:
    equal, pooled = f"cp23.metrics.{code}.equal_fold", f"cp23.metrics.{code}.pooled"
    fold, peak = f"cp23.metrics.{code}.{{fold}}", f"cp23.diagnostics.{code}.peak"
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
    builder.daily(CP23["diagnostics"], code)
    for candidate, base, slug in DRAFT23_CONTRASTS[code]:
        prefix = f"cp23.uncertainty.{candidate}-{base}"
        for metric, score in (("MAE", "mae"), ("WIS", "wis")):
            equal_record = f"{prefix}.equal_fold.{metric}"
            builder.single(f"delta_s_{score}_vs_{slug}", equal_record)
            builder.single(f"delta_s_{score}_vs_{slug}_ci_low", equal_record, "ci_low")
            builder.single(f"delta_s_{score}_vs_{slug}_ci_high", equal_record, "ci_high")
            ratio = f"cp23.ratio.{candidate}-{base}.{metric}"
            builder.single(f"ratio_s_{score}_vs_{slug}", ratio)
            builder.single(f"ratio_s_{score}_vs_{slug}_ci_low", ratio, "ci_low")
            builder.single(f"ratio_s_{score}_vs_{slug}_ci_high", ratio, "ci_high")
            fold_pattern = f"{prefix}.{{fold}}.{metric}"
            builder.per_fold(f"delta_fold_{score}_eur_vs_{slug}", fold_pattern)
            builder.per_fold(f"delta_fold_{score}_eur_vs_{slug}_ci_low", fold_pattern, "ci_low")
            builder.per_fold(f"delta_fold_{score}_eur_vs_{slug}_ci_high", fold_pattern, "ci_high")


def _draft23_params(protocol: dict, code: str | None) -> dict[str, str]:
    cp15 = json.loads((ROOT / "reports/cp15/protocol.json").read_text())
    out = {"anchor_version": "capstone_v21.md v21-r10 §21", "protocol_sha256": _file_sha256(CP23["protocol"])}
    if code is None:
        return out
    policy = protocol["policies"][code]
    ddnn = protocol["ddnn"]
    out["quantile_set"] = ",".join(str(level) for level in cp15["quantiles"]["levels"])
    out["seeds"] = ",".join(str(seed) for seed in ddnn["ensemble"]["seeds"])
    out["weather_features"] = "v4's three GFS columns plus missing indicators"
    out["history_window"] = ddnn["history"]["window"]
    out["policy_definition"] = f"{policy['role']}; central {policy['central']}"
    out["member_weight"] = protocol["member_weight"]
    out["interval_method"] = protocol["h_layer"] if policy["layer"].startswith("H") else ddnn["emission"]["quantile_function"]
    out["ddnn"] = ddnn["architecture"]["family"] + "; " + ddnn["architecture"]["head"]
    out["ddnn_configurations"] = json.dumps([{k: c[k] for k in ("id", "hidden")} for c in ddnn["configurations"]],
                                            separators=(",", ":"))
    out["ddnn_selection"] = ddnn["selection"]["when"] + "; " + ddnn["selection"]["criterion"] + "; " + ddnn["selection"]["tie"]
    out["ddnn_ensemble"] = ddnn["ensemble"]["combination"]
    return {key: value[:500] for key, value in out.items()}


def _draft23_readme(run_name: str, checkpoint: G.Checkpoint, spec: dict, blobs: dict[str, str]) -> str:
    tag = checkpoint.evidence_tag
    lines = [f"# {run_name}", "",
             f"Tracked by CP-23 from its committed evidence (draft export; evidence tag `{tag}` and its commit are "
             f"{spec['pending']}). Development evidence; nothing here is a live or confirmatory result.", "",
             f"- Report: {GITHUB_URL}/blob/{tag}/{checkpoint.report}",
             f"- Independent Integration review: {GITHUB_URL}/blob/{tag}/{checkpoint.verdict}",
             f"- Landing record: {checkpoint.landing}", f"- Presentation: {PAGES_URL}", "",
             "Source rows at the evidence tag:", ""]
    lines += [f"- {GITHUB_URL}/blob/{tag}/{path} (blob {blob})" for path, blob in blobs.items()]
    return "\n".join(lines) + "\n"


def _draft23_runs(entries: dict[str, G.Entry], checkpoint: G.Checkpoint, spec: dict) -> list[dict]:
    """CP-23's parent and children, from its committed evidence, with the draft's explicit pending fields."""
    protocol = json.loads((ROOT / CP23["protocol"]).read_text())
    records = _draft23_records()
    group = comparability()["common"]
    pending = spec["pending"]
    note = spec["note"]
    runs = []
    owner = entries[checkpoint.owner]
    parent_tags = {
        "delu.run_key": checkpoint.run_key, "delu.checkpoint": checkpoint.code, "delu.registry_id": owner.id,
        "delu.kind": owner.kind, "delu.public_name": owner.name, "delu.status": _draft_status_text(owner, pending),
        "delu.role": "checkpoint", "delu.evidence_class": "development_post_selection",
        "delu.population_id": group["population_id"], "delu.comparability_id": group["comparability_id"],
        "delu.model_code_sha": spec["model_code_sha"], "delu.evidence_ref": spec["evidence_ref"],
        "delu.backfilled": "false", "delu.original_completed_utc": pending,
        "delu.children": ",".join(f"{checkpoint.run_key}/{code}" for code in checkpoint.children),
        "mlflow.note.content": _draft_description(owner, note, pending),
    }
    parent = {"run_key": checkpoint.run_key, "parent": None,
              "run_name": draft_run_name(checkpoint.run_key, entries, checkpoint),
              "params": _draft23_params(protocol, None), "tags": parent_tags, "metrics": {}, "metric_provenance": {},
              "metric_units": {}, "inputs": [], "comparability": dict(group)}
    parent["artifacts"] = [
        _artifact("summary.json", _canonical({k: v for k, v in parent.items() if k != "metric_provenance"}) + "\n"),
        _artifact("README.md", _draft23_readme(parent["run_name"], checkpoint, spec,
                                               {CP23["protocol"]: R.blob_sha(R.source_bytes(CP23["protocol"]))})),
    ]
    runs.append(parent)
    for code in checkpoint.children:
        run_key = f"{checkpoint.run_key}/{code}"
        entry = _draft_entry_for(run_key, entries)
        builder = DraftBuilder(records)
        _draft23_scores(builder, code)
        blobs = _draft_blobs(builder.provenance, records)
        run_name = draft_run_name(run_key, entries, checkpoint)
        comparator = G.get(entry.comparator).name if entry.comparator in {e.id for e in G.entries()} else entries[entry.comparator].name
        tags = {
            "delu.run_key": run_key, "delu.checkpoint": checkpoint.code, "delu.registry_id": entry.id,
            "delu.kind": entry.kind, "delu.generation": entry.version or "none", "delu.policy_code": code,
            "delu.public_name": entry.name, "delu.status": _draft_status_text(entry, pending), "delu.comparator": comparator,
            "delu.role": "candidate", "delu.adopted": G.adopted_flag(entry),
            "delu.evidence_class": "development_post_selection",
            "delu.population_id": group["population_id"], "delu.comparability_id": group["comparability_id"],
            "delu.model_code_sha": spec["model_code_sha"], "delu.evidence_ref": spec["evidence_ref"],
            "delu.source_blobs": _canonical(blobs), "delu.backfilled": "false", "delu.original_completed_utc": pending,
            "mlflow.note.content": _draft_description(entry, note, pending, code=code, role="candidate"),
        }
        inputs = datasets("cp23", code, group, weather=True)
        tags["delu.datasets"] = _canonical({dataset["name"]: dataset["sha256"] for dataset in inputs})
        run = {"run_key": run_key, "parent": checkpoint.run_key, "run_name": run_name,
               "params": _draft23_params(protocol, code), "tags": tags, "metrics": builder.metrics,
               "metric_provenance": builder.provenance,
               "metric_units": {key: metric_unit(key) for key in builder.metrics}, "inputs": inputs}
        summary = _canonical({k: v for k, v in run.items() if k != "metric_provenance"})
        run["artifacts"] = [_artifact("summary.json", summary + "\n"),
                            _artifact("README.md", _draft23_readme(run_name, checkpoint, spec, blobs))]
        runs.append(run)
    return runs


def build_draft23() -> dict:
    """CP-23's draft export: one file, the checkpoint's parent and every new policy."""
    spec, entries, checkpoint = draft_registry23()
    return {"experiment": EXPERIMENT, "checkpoint": checkpoint.code, "status": "draft",
            "pending_fields": spec["pending_fields"], "draft_registry": DRAFT23_REGISTRY,
            "revisions": spec.get("revisions"), "runs": _draft23_runs(entries, checkpoint, spec)}


# --------------------------------------------------------------------------- main


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--check", action="store_true", help="exit 1 if the committed export is stale")
    parser.add_argument("--diff-against", metavar="REF", default=None,
                        help="compare the fresh export with the one committed at REF, record by record")
    parser.add_argument("--to", metavar="REF", default=None,
                        help="with --diff-against: compare with the export committed at REF instead of a fresh one")
    parser.add_argument("--out", type=Path, default=None, help="with --diff-against: write the report here")
    parser.add_argument("--draft", metavar="NAME", default=None,
                        help="build a checkpoint's draft export: cp21 (reports/block-challenger/mlflow-export-draft/), "
                             "cp22 (reports/v4-revision/mlflow-export-draft/) or "
                             "cp23 (reports/distribution-challenger/mlflow-export-draft/)")
    args = parser.parse_args()
    if args.draft:
        return draft_main(args.draft, check=args.check)
    files = build_export()
    if args.diff_against:
        report = diff_exports(export_at(args.diff_against), export_at(args.to) if args.to else files)
        report["against"] = args.diff_against
        report["to"] = args.to or "the fresh export"
        text = json.dumps(report, indent=1, sort_keys=True, ensure_ascii=False) + "\n"
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(text)
        print(f"runs {report['runs_old']} -> {report['runs_new']} (added {report['runs_added'] or 'none'}); "
              f"checked {report['checked']}; identity changes on {len(report['identity_changes'])} runs; "
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


def draft_main(name: str, *, check: bool) -> int:
    """Write (or, with --check, verify) the committed draft export. The published set is untouched."""
    draft = build_draft(name)
    problems = draft_problems(draft)
    if problems:
        raise SystemExit("the draft export does not match its draft entries: " + "; ".join(problems))
    findings = outbound_findings(outbound_strings({name: draft}), local_secrets())
    if findings:
        for finding in dict.fromkeys(findings):
            print(f"mlflow-export: BLOCKED - {finding}", file=sys.stderr)
        return 1
    text = json.dumps(draft, indent=1, sort_keys=True, ensure_ascii=False) + "\n"
    directory = {"cp22": DRAFT22_DIR, "cp23": DRAFT23_DIR}.get(name, DRAFT_DIR)
    path = directory / f"{name}.json"
    if check:
        if not path.exists() or path.read_text() != text:
            print(f"the committed draft export is stale: {path.relative_to(ROOT)}")
            return 1
        print("the committed draft export is current")
        return 0
    directory.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    print(f"wrote {path.relative_to(ROOT)}: {len(draft['runs'])} runs (draft; pending fields {sorted(draft['pending_fields'])})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
