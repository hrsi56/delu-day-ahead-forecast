"""CP-2 stage 2 -- the §7.2 post-gate information benchmark. One run, one number.

Strict = the selected champion catalog. A69-augmented = the same catalog plus
delivery-day A69 and its named derivatives, and nothing else different: same
rows, same folds, same seed, same hyperparameters, same (zero) tuning budget.

Raw quantile heads only. Neither arm is calibrated, so coverage, interval width
and calibration error are deliberately not computed -- reporting them for an
uncalibrated comparison is what §7.2 forbids.

    uv run python scripts/cp2_benchmark_a69.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from delu_forecast.experiment import (
    experiment_params,
    load_inputs,
    mask_for,
)
from delu_forecast.metrics import mae, pinball_matrix, pooled_mean_pinball
from delu_forecast.model import SEED, fit_quantile_heads, predict_raw_heads
from delu_forecast.schema import BENCHMARK_ADDITIONS
from delu_forecast.tracking import configure_tracking, log_decision_record, run

OUT = Path("reports/cp2")
LIMITATION = (
    "This uncalibrated raw-head comparison isolates the information content of "
    "post-gate A69. It makes no claim about calibrated interval quality and does "
    "not make A69 available at the forecast gate."
)


def run_raw_arm(inputs, arm: str) -> dict[str, object]:
    """Fit on proper-training, predict raw heads on eval. No calibration anywhere."""
    total = 0.0
    count = 0
    absolute = 0.0
    rows = 0
    per_fold: dict[str, float] = {}
    for fold in inputs.spec.development_folds:
        train = mask_for(inputs, fold.proper_training)
        evaluation = mask_for(inputs, fold.evaluation)
        heads = fit_quantile_heads(inputs.matrix(arm, train), inputs.target[train], seed=SEED)
        raw = predict_raw_heads(heads, inputs.matrix(arm, evaluation))
        y = inputs.target[evaluation]
        losses = pinball_matrix(y, raw)
        total += float(losses.sum())
        count += int(losses.size)
        absolute += float(np.abs(y - raw[:, 4]).sum())
        rows += len(y)
        per_fold[fold.name] = pooled_mean_pinball(y, raw)
    return {
        "arm": arm,
        "pooled_mean_pinball": total / count,
        "median_mae": absolute / rows,
        "per_fold_pinball": per_fold,
        "n_obs": rows,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    inputs = load_inputs()
    enabled = configure_tracking()
    selected = json.loads((OUT / "catalog_selection.json").read_text())["selected_catalog"]
    strict_arm = selected
    augmented_arm = f"{selected}+a69"

    strict = run_raw_arm(inputs, strict_arm)
    augmented = run_raw_arm(inputs, augmented_arm)

    # The strict arm is the selected development arm re-fit under identical
    # settings; if it does not reproduce, nothing downstream is trustworthy.
    development = float(
        json.loads((OUT / "catalog_selection.json").read_text())["pooled_mean_pinball_float"][selected]
    )
    reproduced = abs(strict["pooled_mean_pinball"] - development) < 1e-12

    difference = 100.0 * (augmented["pooled_mean_pinball"] - strict["pooled_mean_pinball"]) / strict["pooled_mean_pinball"]
    payload = {
        "headline_metric": "pooled mean pinball loss across nine quantiles and five folds, raw heads",
        "strict_arm": strict,
        "a69_augmented_arm": augmented,
        "a69_columns_added": list(BENCHMARK_ADDITIONS),
        "percentage_difference_a69_vs_strict": difference,
        "value_of_post_gate_information_pct": -difference,
        "calibrated": False,
        "coverage_reported": False,
        "deployable_artifact": False,
        "registry_version": False,
        "strict_arm_reproduces_development_selection_run": reproduced,
        "development_pooled_mean_pinball_for_selected_catalog": development,
        "limitation": LIMITATION,
        "seed": SEED,
    }
    (OUT / "a69_benchmark.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(f"strict   ({strict_arm}): pooled raw pinball = {strict['pooled_mean_pinball']!r}")
    print(f"a69-aug  ({augmented_arm}): pooled raw pinball = {augmented['pooled_mean_pinball']!r}")
    print(f"percentage difference (A69-augmented vs strict) = {difference:+.6f}%")
    print(f"strict arm reproduces the development selection run exactly: {reproduced}")

    for arm, result in ((strict_arm, strict), (augmented_arm, augmented)):
        with run(f"benchmark::{arm}", enabled=enabled, tags={"stage": "post_gate_benchmark", "calibrated": "false"}):
            log_decision_record(
                enabled,
                params=experiment_params(arm, inputs, {"benchmark_arm": arm, "limitation": LIMITATION}),
                metrics={
                    "pooled_raw_mean_pinball": float(result["pooled_mean_pinball"]),
                    "median_mae": float(result["median_mae"]),
                    **{f"fold_{k}_pinball_raw": v for k, v in result["per_fold_pinball"].items()},
                },
                artifacts=[OUT / "a69_benchmark.json"],
            )


if __name__ == "__main__":
    main()
