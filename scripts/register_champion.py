#!/usr/bin/env python3
"""Register the champion as an MLflow model version with the `champion` alias (§9.1).

**Non-gating by contract.** §9.1: "if the registry or an alias/tag operation is
unavailable at release time, the release proceeds and the failed step is
disclosed." So every remote operation is attempted, every failure is recorded by
name in `reports/cp3/mlflow_registration.json`, and this script exits 0 either
way. It is portfolio evidence, never a runtime dependency -- the deployed Space
loads the bundled artifact and never queries the registry.

The registration record is also the **MLflow surface** CP-3 item 5 binds: it
carries the same claim strings the README, the Pages export and the Space card
render, so `tests/test_17_cross_surface_agreement.py` can check all four offline.

Before anything is pushed, the local artifact's fingerprint is recomputed and
compared to the source run's recorded one. Registering a version that is not the
artifact the holdout evaluated would be the exact claim item 5 forbids, so it is
checked rather than assumed.

    MLFLOW_TRACKING_URI=... MLFLOW_TRACKING_USERNAME=... MLFLOW_TRACKING_PASSWORD=... \
      uv run python scripts/register_champion.py
"""

from __future__ import annotations

import json
import os
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from delu_forecast.claims import build_claims  # noqa: E402
from delu_forecast.showcase import load_champion  # noqa: E402
from delu_forecast.tracking import EXPERIMENT_NAME, configure_tracking, redact  # noqa: E402

REGISTERED_MODEL = "delu-day-ahead-champion"
ALIAS = "champion"
RECORD = ROOT / "reports" / "cp3" / "mlflow_registration.json"
SOURCE_RUN_NAME = "champion::final-fit-and-holdout"


def version_tags(claims) -> dict[str, str]:
    """Release and lineage tags — §9.1's list, plus the item-5 claim strings."""
    C = claims
    return {
        "release_status": "portfolio_release",
        "code_commit": C["champion_code_sha"],
        "snapshot_sha256": C["snapshot_sha256"],
        "artifact_fingerprint_sha256": C["champion_fingerprint"],
        "snapshot_cutoff": C["snapshot_cutoff"],
        "raw_model_fit_cutoff": C["raw_model_fit_cutoff"],
        "final_calibration_window": C["final_calibration_window"],
        "holdout_window": C["holdout_window"],
        "selected_catalog": C["selected_catalog"],
        "catalog_base_loss": C["catalog_base_loss"],
        "catalog_augmented_loss": C["catalog_augmented_loss"],
        "catalog_pct": C["catalog_pct"],
        "holdout_mae_champion": C["holdout_mae_champion"],
        "holdout_mae_naive": C["holdout_mae_naive"],
        "holdout_mae_pct": C["holdout_mae_pct"],
        "holdout_pinball_champion": C["holdout_pinball_champion"],
        "holdout_pinball_naive": C["holdout_pinball_naive"],
        "holdout_pinball_pct": C["holdout_pinball_pct"],
        "holdout_coverage_50": C["holdout_coverage_50"],
        "holdout_coverage_80": C["holdout_coverage_80"],
        "holdout_coverage_95": C["holdout_coverage_95"],
        "holdout_dm_statistic": C["holdout_dm_statistic"],
        "holdout_dm_p_value": C["holdout_dm_p_value"],
        "holdout_dm_effect_size": C["holdout_dm_effect_size"],
        "holdout_dm_label": C["holdout_dm_label"],
        "development_evidence_class": C["development_evidence_class"],
        "development_dm_point_p_value": C["development_dm_point_p_value"],
        "benchmark_strict_loss": C["benchmark_strict_loss"],
        "benchmark_a69_loss": C["benchmark_a69_loss"],
        "benchmark_pct": C["benchmark_pct"],
        "benchmark_limitation": C["benchmark_limitation"],
        "shipped_is_evaluated": C["shipped_is_evaluated"],
        "pages_url": C["pages_url"],
        "space_url": C["space_url"],
    }


def main() -> int:
    claims = build_claims()
    record: dict[str, object] = {
        "registered_model": REGISTERED_MODEL,
        "alias": ALIAS,
        "gating": "non-gating (§9.1): a registry or metadata-operation failure is disclosed, not fatal",
        "tracking_uri": os.environ.get("MLFLOW_TRACKING_URI", "<unset>"),
        "attempted_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "version_tags": version_tags(claims),
        "steps": {},
        "failures": [],
    }

    def step(name: str, action):
        try:
            value = action()
            record["steps"][name] = {"ok": True, "detail": value}
            print(f"  [ok]   {name}: {value}")
            return value
        except Exception as exc:  # non-gating by contract
            detail = redact(f"{type(exc).__name__}: {exc}")[:400]
            record["steps"][name] = {"ok": False, "detail": detail}
            record["failures"].append(f"{name}: {detail}")
            print(f"  [FAIL] {name}: {detail}", file=sys.stderr)
            return None

    # -- identity first: is the local artifact the one the holdout evaluated? --
    local = load_champion()
    local_fingerprint = local.fingerprint()
    record["local_artifact_fingerprint_sha256"] = local_fingerprint
    record["fingerprint_matches_champion_card"] = local_fingerprint == claims["champion_fingerprint"]
    print(f"local artifact fingerprint: {local_fingerprint}")
    print(f"matches champion_card.json: {record['fingerprint_matches_champion_card']}")
    if not record["fingerprint_matches_champion_card"]:
        record["failures"].append(
            "local artifact fingerprint does not match champion_card.json; nothing was registered"
        )
        RECORD.parent.mkdir(parents=True, exist_ok=True)
        RECORD.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
        print("refusing to register: the local artifact is not the evaluated one", file=sys.stderr)
        return 0

    if not configure_tracking(EXPERIMENT_NAME):
        record["steps"]["configure_tracking"] = {
            "ok": False,
            "detail": "MLFLOW_TRACKING_URI is unset; nothing was attempted",
        }
        record["failures"].append("MLFLOW_TRACKING_URI unset — registration skipped and disclosed")
        RECORD.parent.mkdir(parents=True, exist_ok=True)
        RECORD.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
        print("MLFLOW_TRACKING_URI is unset; registration skipped (non-gating)")
        return 0

    import mlflow
    from mlflow import MlflowClient

    client = MlflowClient()

    def find_source_run() -> str:
        experiment = client.get_experiment_by_name(EXPERIMENT_NAME)
        runs = client.search_runs(
            [experiment.experiment_id],
            filter_string=f"attributes.run_name = '{SOURCE_RUN_NAME}'",
            order_by=["attributes.start_time DESC"],
            max_results=25,
        )
        for run in runs:
            if run.data.params.get("artifact_fingerprint_sha256") == local_fingerprint:
                return run.info.run_id
        raise RuntimeError(
            f"no {SOURCE_RUN_NAME} run carries artifact_fingerprint_sha256={local_fingerprint}"
        )

    run_id = step("find_source_run", find_source_run)
    if run_id is None:
        RECORD.parent.mkdir(parents=True, exist_ok=True)
        RECORD.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
        return 0
    record["source_run_id"] = run_id
    record["version_tags"]["source_run_id"] = run_id
    record["source_run_url"] = f"{claims['mlflow_url']}/#/experiments/0/runs/{run_id}"

    model_uri = step(
        "resolve_model_uri",
        lambda: client.get_run(run_id).data.params.get("champion_model_uri")
        or f"runs:/{run_id}/model",
    )
    record["model_uri"] = model_uri

    step(
        "create_registered_model",
        lambda: client.create_registered_model(
            REGISTERED_MODEL,
            description=(
                "The frozen DE-LU day-ahead champion: nine LightGBM quantile heads, the selected "
                f"{claims['selected_catalog']} catalog's preprocessing, four CQR thresholds and "
                "isotonic last, in one mlflow.pyfunc. This is the artifact the one-shot holdout "
                "evaluated; no refit followed it. Portfolio evidence only — the deployed Space "
                "loads the bundled artifact and never queries this registry."
            ),
        ).name
        if not any(m.name == REGISTERED_MODEL for m in client.search_registered_models())
        else f"{REGISTERED_MODEL} already exists",
    )

    version = step(
        "register_model_version",
        lambda: mlflow.register_model(model_uri, REGISTERED_MODEL, tags={"release_status": "portfolio_release"}).version,
    )
    if version is None:
        RECORD.parent.mkdir(parents=True, exist_ok=True)
        RECORD.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
        return 0
    record["model_version"] = str(version)

    step("set_alias", lambda: (client.set_registered_model_alias(REGISTERED_MODEL, ALIAS, version), f"{ALIAS} -> v{version}")[1])

    applied, refused = [], []
    for key, value in record["version_tags"].items():
        try:
            client.set_model_version_tag(REGISTERED_MODEL, version, key, value)
            applied.append(key)
        except Exception as exc:
            refused.append(f"{key}: {redact(f'{type(exc).__name__}: {exc}')[:160]}")
    record["steps"]["set_version_tags"] = {
        "ok": not refused,
        "detail": f"{len(applied)} applied, {len(refused)} refused",
    }
    record["tags_applied"] = sorted(applied)
    record["tags_refused"] = refused
    if refused:
        record["failures"].extend(refused)
    print(f"  [{'ok' if not refused else 'PARTIAL'}] set_version_tags: {len(applied)} applied, {len(refused)} refused")

    record["registry_url"] = f"{claims['mlflow_url']}/#/models/{REGISTERED_MODEL}"
    record["succeeded"] = not record["failures"]
    RECORD.parent.mkdir(parents=True, exist_ok=True)
    RECORD.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    print(f"\nwrote {RECORD}")
    if record["failures"]:
        print("registration completed with disclosed failures (non-gating):")
        for failure in record["failures"]:
            print(f"  - {failure}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception:  # never let a registry problem take the release down
        traceback.print_exc()
        print("\nregistration failed; §9.1 makes this non-gating", file=sys.stderr)
        raise SystemExit(0)
