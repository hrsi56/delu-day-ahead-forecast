"""Metrics and DM machinery checked against hand-computed values.

Every number below is derivable with a pencil, so the test fails if the
implementation drifts rather than merely if it changes.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from delu_forecast.metrics import (
    QUANTILES,
    bootstrap_day_ci,
    daily_pinball_series,
    diebold_mariano,
    interval_coverage,
    newey_west_lrv,
    pinball_matrix,
    point_forecast_quantiles,
    pooled_mean_pinball,
)


def test_pinball_matches_the_definition_including_negative_targets() -> None:
    y = np.array([-10.0])
    q = np.array([[-20.0, -18, -15, -12, -10, -8, -5, -2, 0]])
    losses = pinball_matrix(y, q)
    expected = [max(tau * (-10.0 - value), (tau - 1.0) * (-10.0 - value)) for tau, value in zip(QUANTILES, q[0])]
    assert losses[0].tolist() == pytest.approx(expected)
    assert np.all(losses >= 0.0)


def test_point_forecast_pinball_is_exactly_half_its_absolute_error() -> None:
    """The nine taus are symmetric about 0.5, so a degenerate forecast gives MAE/2."""
    y = np.array([-30.0, 0.0, 55.5])
    f = np.array([12.0, -4.0, 55.5])
    assert pooled_mean_pinball(y, point_forecast_quantiles(f)) == pytest.approx(np.mean(np.abs(y - f)) / 2.0)


def test_coverage_uses_the_right_quantile_pairs() -> None:
    q = np.array([[0.0, 1, 2, 3, 4, 5, 6, 7, 8]])
    assert interval_coverage(np.array([3.5]), q) == {"50": 1.0, "80": 1.0, "95": 1.0}
    assert interval_coverage(np.array([6.5]), q) == {"50": 0.0, "80": 0.0, "95": 1.0}
    assert interval_coverage(np.array([8.5]), q) == {"50": 0.0, "80": 0.0, "95": 0.0}


def test_daily_pinball_averages_over_the_real_hour_count() -> None:
    """A 23-hour day divides by 23, a 25-hour day by 25 -- never by a fixed 24."""
    dates = pd.Index(["a"] * 23 + ["b"] * 25)
    y = np.zeros(48)
    q = np.zeros((48, 9))
    q[:23] = 1.0
    q[23:] = 2.0
    series = daily_pinball_series(y, q, dates)
    assert series.loc["a"] == pytest.approx(0.5)
    assert series.loc["b"] == pytest.approx(1.0)


def test_newey_west_reduces_to_the_sample_variance_at_lag_zero() -> None:
    values = np.array([1.0, -2.0, 3.0, -4.0, 5.0])
    assert newey_west_lrv(values, 0) == pytest.approx(values.var())
    assert newey_west_lrv(values, 2) != pytest.approx(values.var())


def test_dm_sign_direction_and_rejection_threshold() -> None:
    rng = np.random.default_rng(7)
    days = pd.Index([f"d{i:03d}" for i in range(200)])
    naive = pd.Series(rng.normal(10.0, 1.0, 200), index=days)
    # A constant differential has zero long-run variance and no DM statistic, so
    # the advantage carries its own noise -- as a real loss differential does.
    better = pd.Series(naive.to_numpy() - 2.0 + rng.normal(0.0, 0.5, 200), index=days)
    worse = pd.Series(naive.to_numpy() + 2.0 + rng.normal(0.0, 0.5, 200), index=days)
    good = diebold_mariano(better, naive, comparator="n", analysis="a", evidence_class="development_post_selection")
    bad = diebold_mariano(worse, naive, comparator="n", analysis="a", evidence_class="development_post_selection")
    assert good.statistic < -1.645 and good.model_better_at_5pct and good.p_value < 0.05
    assert bad.statistic > 0 and not bad.model_better_at_5pct and bad.p_value > 0.95
    assert good.lag_truncation == int(np.floor(200 ** (1 / 3)))
    expected = -100.0 * (better - naive).mean() / naive.mean()
    assert good.relative_improvement_pct == pytest.approx(expected)
    assert good.relative_improvement_pct == pytest.approx(20.0, abs=1.5)


def test_bootstrap_resamples_days_not_hours() -> None:
    """An hour-level bootstrap would report a far narrower interval; this one must not."""
    rng = np.random.default_rng(11)
    day_effect = rng.normal(0.0, 5.0, 60)
    values = np.repeat(day_effect, 24) + rng.normal(0.0, 0.1, 60 * 24)
    dates = pd.Index(np.repeat(np.arange(60), 24))
    low, high = bootstrap_day_ci(values, dates, reps=500, seed=3)
    hour_low, hour_high = bootstrap_day_ci(values, pd.Index(np.arange(60 * 24)), reps=500, seed=3)
    assert low < values.mean() < high
    # The comparison is the point: resampling hours would understate the interval
    # by roughly sqrt(24), because the 24 rows of one day share a day effect.
    assert (high - low) > 3.0 * (hour_high - hour_low)
