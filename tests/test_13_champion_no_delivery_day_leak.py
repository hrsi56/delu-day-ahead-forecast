"""Delivery-day availability at the *champion artifact* boundary (§5.2, §9.4-2).

`test_02` asserts the invariant on the feature layer. CP-1 was refused landing
because a leak survived a green suite, so this file re-asserts it one level up --
on the frozen `mlflow.pyfunc` object that actually ships, whose `predict` builds
its own features. A wrapper, a diagnostic or a convenience helper could
reintroduce a row-wise boundary without touching `features.py`; nothing here
would still pass if one did.

Every "nothing changed" assertion is paired with a positive control that makes
the same machinery report a change, so an inert or all-null implementation fails.
"""

from __future__ import annotations

from datetime import date, timedelta

import numpy as np
import pandas as pd
import pytest
from conftest import synthetic_snapshot

from delu_forecast.conformal import PAIR_ALPHAS
from delu_forecast.model import ChampionModel, Cutoffs, fit_quantile_heads
from delu_forecast.features import build_feature_catalog
from delu_forecast.ingest import BERLIN

START = date(2025, 1, 1)
END = date(2025, 5, 1)
TARGET_DAY = date(2025, 4, 15)
TINY = {
    "objective": "quantile", "n_estimators": 12, "num_leaves": 7, "learning_rate": 0.2,
    "min_child_samples": 5, "n_jobs": 1, "deterministic": True, "force_row_wise": True, "verbose": -1,
}
CUTOFFS = Cutoffs(END, TARGET_DAY, START, TARGET_DAY, TARGET_DAY, END)


def _snapshot() -> pd.DataFrame:
    rng = np.random.default_rng(4)
    frame = synthetic_snapshot(START, END)
    hours = len(frame)
    frame["price_eur_mwh"] = rng.normal(60.0, 40.0, hours)
    frame["load_forecast_mw"] = 50_000 + rng.normal(0, 3_000, hours)
    frame["vre_actual_mw"] = 15_000 + rng.normal(0, 4_000, hours)
    return frame


def _champion(frame: pd.DataFrame, catalog: str) -> ChampionModel:
    features = build_feature_catalog(frame, catalog)
    complete = features.notna().all(axis=1).to_numpy()
    heads = fit_quantile_heads(
        features.loc[complete], frame["price_eur_mwh"].to_numpy()[complete], seed=1, params=TINY
    )
    thresholds = dict(zip((pair for pair, _ in PAIR_ALPHAS), (6.0, 4.0, 2.0, -1.0), strict=True))
    return ChampionModel(heads, catalog, thresholds, CUTOFFS)


def _rows_on(frame: pd.DataFrame, day: date) -> np.ndarray:
    local = pd.DatetimeIndex(frame["timestamp_utc"]).tz_convert(BERLIN)
    return np.array([value == day for value in local.date])


@pytest.mark.parametrize("catalog", ["base", "base_plus_residual_load_proxy"])
def test_mutating_any_hour_of_delivery_day_d_changes_no_prediction_on_d(catalog: str) -> None:
    frame = _snapshot()
    champion = _champion(frame, catalog)
    target_rows = _rows_on(frame, TARGET_DAY)
    assert target_rows.sum() == 24
    reference = champion.predict(None, frame).to_numpy()[target_rows]
    assert np.isfinite(reference).all(), "baseline must be non-null, or the sweep proves nothing"

    for offset in range(int(target_rows.sum())):  # sweep every hour, first and last included
        mutated = frame.copy()
        position = np.flatnonzero(target_rows)[offset]
        mutated.loc[mutated.index[position], "price_eur_mwh"] += 500.0
        observed = champion.predict(None, mutated).to_numpy()[target_rows]
        assert np.array_equal(observed, reference), f"hour {offset} of D leaked into a prediction for D"


def test_mutating_a_d_minus_1_price_does_change_predictions_on_d() -> None:
    """Positive control for the sweep above."""
    frame = _snapshot()
    champion = _champion(frame, "base")
    target_rows = _rows_on(frame, TARGET_DAY)
    reference = champion.predict(None, frame).to_numpy()[target_rows]

    previous = np.flatnonzero(_rows_on(frame, TARGET_DAY - timedelta(days=1)))
    mutated = frame.copy()
    mutated.loc[mutated.index[previous], "price_eur_mwh"] += 500.0
    observed = champion.predict(None, mutated).to_numpy()[target_rows]
    assert not np.array_equal(observed, reference), "control is inert: D-1 must reach D"


def test_actual_generation_is_bounded_at_d_minus_2_with_a_positive_control() -> None:
    frame = _snapshot()
    champion = _champion(frame, "base_plus_residual_load_proxy")
    target_rows = _rows_on(frame, TARGET_DAY)
    reference = champion.predict(None, frame).to_numpy()[target_rows]

    for lag in (0, 1):  # D and D-1 actuals are not yet published at the gate
        mutated = frame.copy()
        rows = np.flatnonzero(_rows_on(frame, TARGET_DAY - timedelta(days=lag)))
        mutated.loc[mutated.index[rows], "vre_actual_mw"] += 9_000.0
        observed = champion.predict(None, mutated).to_numpy()[target_rows]
        assert np.array_equal(observed, reference), f"A75 actuals from D-{lag} reached a prediction for D"

    mutated = frame.copy()
    rows = np.flatnonzero(_rows_on(frame, TARGET_DAY - timedelta(days=2)))
    mutated.loc[mutated.index[rows], "vre_actual_mw"] += 9_000.0
    observed = champion.predict(None, mutated).to_numpy()[target_rows]
    assert not np.array_equal(observed, reference), "control is inert: D-2 actuals must reach D"


def test_runtime_input_firewall_rejects_post_gate_and_same_day_actual_columns() -> None:
    frame = _snapshot()
    champion = _champion(frame, "base")
    for column in ("vre_forecast_mw", "solar_forecast_mw", "dunkelflaute_flag", "residual_load_fc", "actual_load_mw"):
        contaminated = frame.copy()
        contaminated[column] = 1.0
        with pytest.raises(ValueError, match="post-gate A69 and same-day actual"):
            champion.predict(None, contaminated)
    champion.predict(None, frame)  # the clean frame still works


def test_predictions_are_ordered_and_aligned_row_for_row() -> None:
    frame = _snapshot()
    champion = _champion(frame, "base")
    result = champion.predict(None, frame)
    assert len(result) == len(frame)
    values = result.to_numpy()
    finite = np.isfinite(values).all(axis=1)
    assert finite.sum() > 1_000
    assert np.all(np.diff(values[finite], axis=1) >= 0)
