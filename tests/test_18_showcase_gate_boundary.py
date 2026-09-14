"""CP-3: nothing in the showcase reintroduces a row-wise boundary (§5.2).

The §5.2 delivery-day availability invariant is law, and CP-1's first attempt
returned PASS while 95.83 % of its rows leaked because every test inherited the
same wrong premise. So each assertion here that something *does not* happen is
paired with a control proving it could.

The reference standard is CP-2's: rebuild the inputs from truncated history and
require bitwise-identical output.
"""

from __future__ import annotations

from datetime import timedelta

import numpy as np
import pandas as pd
import pytest

from delu_forecast.model import FORBIDDEN_CHAMPION_INPUT_COLUMNS
from delu_forecast.postprocess import QUANTILE_LABELS
from delu_forecast.showcase import (
    HISTORY_DAYS,
    INTERVAL_LEVELS,
    actuals_for_day,
    default_target_day,
    delivery_days,
    forecast_delivery_day,
    gate_feasible_frame,
    load_champion,
    load_snapshot,
    quantile_fan,
)

QUANTILES = list(QUANTILE_LABELS)


@pytest.fixture(scope="module")
def champion():
    return load_champion()


@pytest.fixture(scope="module")
def snapshot():
    return load_snapshot()


@pytest.fixture(scope="module")
def target(snapshot):
    return default_target_day(snapshot)


def test_gate_frame_holds_no_row_after_the_delivery_day(snapshot, target):
    frame = gate_feasible_frame(snapshot, target)
    assert pd.Index(frame["delivery_date"].to_numpy()).max() == target
    assert len(frame) > 0


def test_gate_frame_masks_every_delivery_day_price(snapshot, target):
    frame = gate_feasible_frame(snapshot, target)
    on_target = pd.Index(frame["delivery_date"].to_numpy()) == target
    assert on_target.sum() in {23, 24, 25}
    assert frame.loc[on_target, "price_eur_mwh"].isna().all()
    # ... and leaves the history untouched, or the lags would be wrong.
    assert not frame.loc[~on_target, "price_eur_mwh"].isna().any()


def test_gate_frame_carries_no_post_gate_column(snapshot, target):
    frame = gate_feasible_frame(snapshot, target)
    assert not (FORBIDDEN_CHAMPION_INPUT_COLUMNS & set(frame.columns))
    assert "vre_forecast_mw" not in frame.columns


def test_delivery_day_prices_change_nothing_and_a_d_minus_1_price_does(champion, snapshot, target):
    """The paired check. Half one alone is satisfiable by a constant model."""
    masked = forecast_delivery_day(champion, snapshot, target)[QUANTILES].to_numpy()

    unmasked = gate_feasible_frame(snapshot, target, catalog=champion.catalog)
    on_target = pd.Index(unmasked["delivery_date"].to_numpy()) == target
    unmasked.loc[on_target, "price_eur_mwh"] = actuals_for_day(snapshot, target).to_numpy()
    with_day_prices = champion.predict_stages(unmasked)["final"][on_target]
    assert np.array_equal(masked, with_day_prices), (
        "a champion feature for D moved when D's own prices were supplied"
    )

    mutated = snapshot.copy()
    previous = pd.Index(mutated["delivery_date"].to_numpy()) == (target - timedelta(days=1))
    assert previous.sum() > 0
    mutated.loc[previous, "price_eur_mwh"] = mutated.loc[previous, "price_eur_mwh"] + 250.0
    control = forecast_delivery_day(champion, mutated, target)[QUANTILES].to_numpy()
    assert not np.array_equal(masked, control), (
        "positive control failed: mutating a D-1 price left the forecast unchanged, so the "
        "equality above proves nothing"
    )
    assert np.nanmax(np.abs(masked - control)) > 1.0


def test_truncated_history_reproduces_the_whole_snapshot_bitwise(champion, snapshot, target):
    """CP-2's standard, applied to the showcase's own truncation window."""
    short = forecast_delivery_day(champion, snapshot, target, history_days=HISTORY_DAYS)
    long = forecast_delivery_day(champion, snapshot, target, history_days=760)
    assert np.array_equal(short[QUANTILES].to_numpy(), long[QUANTILES].to_numpy())


def test_the_boundary_holds_across_a_run_of_delivery_days(champion, snapshot):
    """One day could be luck. Sweep the last week, including a weekend."""
    days = delivery_days(snapshot)[-7:]
    for day in days:
        masked = forecast_delivery_day(champion, snapshot, day)[QUANTILES].to_numpy()
        frame = gate_feasible_frame(snapshot, day, catalog=champion.catalog)
        on_target = pd.Index(frame["delivery_date"].to_numpy()) == day
        frame.loc[on_target, "price_eur_mwh"] = actuals_for_day(snapshot, day).to_numpy()
        assert np.array_equal(masked, champion.predict_stages(frame)["final"][on_target]), day


def test_the_scenario_control_moves_the_forecast_and_touches_only_the_target_day(
    champion, snapshot, target
):
    """A control that changes nothing is decoration; one that leaks is a defect."""
    base = forecast_delivery_day(champion, snapshot, target)[QUANTILES].to_numpy()
    probed = forecast_delivery_day(champion, snapshot, target, load_scale=1.10)[QUANTILES].to_numpy()
    assert not np.array_equal(base, probed), "the load-forecast probe changed nothing"

    scaled = gate_feasible_frame(snapshot, target, catalog=champion.catalog, load_scale=1.10)
    plain = gate_feasible_frame(snapshot, target, catalog=champion.catalog)
    off_target = pd.Index(plain["delivery_date"].to_numpy()) != target
    assert np.array_equal(
        scaled.loc[off_target, "load_forecast_mw"].to_numpy(),
        plain.loc[off_target, "load_forecast_mw"].to_numpy(),
    ), "the probe altered a day other than the delivery day"
    assert np.array_equal(
        np.nan_to_num(scaled["price_eur_mwh"].to_numpy(), nan=-1e9),
        np.nan_to_num(plain["price_eur_mwh"].to_numpy(), nan=-1e9),
    ), "the probe altered a price"


def test_showcase_output_is_monotone_at_every_level(champion, snapshot, target):
    """The one retained hard gate, on the surface a visitor actually sees."""
    for day in delivery_days(snapshot)[-5:]:
        matrix = forecast_delivery_day(champion, snapshot, day)[QUANTILES].to_numpy()
        assert np.isfinite(matrix).all()
        assert (np.diff(matrix, axis=1) >= 0).all(), f"quantile crossing on {day}"
    fan = quantile_fan(forecast_delivery_day(champion, snapshot, target), 95)
    assert (fan["lower"] <= fan["median"]).all() and (fan["median"] <= fan["upper"]).all()


def test_quantile_fan_rejects_an_unknown_level(champion, snapshot, target):
    forecast = forecast_delivery_day(champion, snapshot, target)
    with pytest.raises(ValueError):
        quantile_fan(forecast, 90)
    assert set(INTERVAL_LEVELS) == {50, 80, 95}
