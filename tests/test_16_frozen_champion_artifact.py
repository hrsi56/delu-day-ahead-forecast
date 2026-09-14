"""The frozen artifact is the artifact that ships (§7.1, §12 CP-2 item 5).

These assertions run against `models/champion/` as committed, so they fail if the
artifact drifts from the run that produced the holdout numbers. They are skipped
when the artifact is absent, because the CP-1 tree legitimately has no model.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from delu_forecast.metrics import crossing_violations
from delu_forecast.model import gate_feasible_frame
from delu_forecast.postprocess import QUANTILE_LABELS

MODEL_DIR = Path("models/champion")
CARD = MODEL_DIR / "champion_card.json"
HOLDOUT = Path("reports/cp2/holdout_report.json")
SNAPSHOT = Path("data/snapshot.parquet")

pytestmark = pytest.mark.skipif(not CARD.exists(), reason="no frozen champion in this tree")


def _champion():
    import cloudpickle

    return cloudpickle.loads((MODEL_DIR / "python_model.pkl").read_bytes())


def test_artifact_fingerprint_matches_its_card_and_the_holdout_report() -> None:
    """The one identity that is stable. The pickle's own bytes are not.

    MLflow stamps a fresh `model_uuid` and creation time into `MLmodel` on every
    save, so a byte hash of the directory would report drift that is not there.
    """
    card = json.loads(CARD.read_text())
    champion = _champion()
    assert champion.fingerprint() == card["artifact_fingerprint_sha256"]
    if HOLDOUT.exists():
        report = json.loads(HOLDOUT.read_text())
        assert report["artifact_fingerprint_sha256"] == card["artifact_fingerprint_sha256"]
        assert report["selected_catalog"] == card["catalog"]
        assert report["final_cqr_thresholds"] == card["cqr_thresholds"]
        assert report["retrain_after_holdout"] is False


def test_frozen_champion_predicts_and_never_crosses() -> None:
    champion = _champion()
    snapshot = pd.read_parquet(SNAPSHOT)
    recent = snapshot.tail(24 * 400).reset_index(drop=True)
    output = champion.predict(None, gate_feasible_frame(recent, champion.catalog))
    assert list(output.columns) == list(QUANTILE_LABELS)
    assert len(output) == len(recent)
    values = output.to_numpy()
    finite = np.isfinite(values).all(axis=1)
    assert finite.sum() > 24 * 300
    assert crossing_violations(values[finite]) == 0


def test_artifact_declares_the_pyfunc_flavor_and_ships_its_code() -> None:
    text = (MODEL_DIR / "MLmodel").read_text()
    assert "python_function" in text
    assert (MODEL_DIR / "code" / "delu_forecast" / "model.py").exists()
    assert (MODEL_DIR / "requirements.txt").exists()


def test_card_records_all_four_cutoffs_distinctly() -> None:
    cutoffs = json.loads(CARD.read_text())["cutoffs"]
    for key in ("snapshot_cutoff", "raw_model_fit_cutoff", "final_calibration_window", "holdout_window"):
        assert cutoffs[key]
    assert cutoffs["snapshot_cutoff"] != cutoffs["raw_model_fit_cutoff"]
    assert cutoffs["raw_model_fit_precedes_snapshot_by_delivery_days"] == "152"
