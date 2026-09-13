"""The mandatory §6.2 CQR fixture, plus the controls that make it discriminating.

A fixture that only checks "the code returns what the code returns" is worthless.
Each assertion below is paired with the specific wrong implementation the plan
names, and the test fails if that wrong implementation would have passed.
"""

from __future__ import annotations

import math
from decimal import Decimal
from fractions import Fraction

import numpy as np
import pytest

from delu_forecast.conformal import (
    PAIR_ALPHAS,
    UndersizedCalibrationSet,
    apply_cqr_thresholds,
    conformity_scores,
    cqr_threshold,
    fit_cqr_thresholds,
    order_statistic_rank,
)
from delu_forecast.postprocess import QUANTILE_LABELS

N_CAL = 20
EXPECTED_ONE_BASED_RANKS = (20, 19, 17, 11)
EXPECTED_ZERO_BASED_POSITIONS = (19, 18, 16, 10)
EXPECTED_THRESHOLDS = (8.0, 7.0, 5.0, -1.0)


def fixture_rows() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Rows j=0..19 with (q_lo, q_hi, y) = (100, 140, 111-j), per §6.2."""
    j = np.arange(N_CAL)
    return np.full(N_CAL, 100.0), np.full(N_CAL, 140.0), 111.0 - j


def test_scores_are_derived_not_supplied() -> None:
    lower, upper, y = fixture_rows()
    scores = conformity_scores(lower, upper, y)
    assert np.array_equal(scores, np.arange(N_CAL) - 11.0)
    assert np.array_equal(np.sort(scores), np.arange(-11.0, 9.0))


def test_ranks_positions_and_thresholds_match_the_plan() -> None:
    lower, upper, y = fixture_rows()
    scores = conformity_scores(lower, upper, y)
    ranks = tuple(order_statistic_rank(N_CAL, alpha) for _, alpha in PAIR_ALPHAS)
    thresholds = tuple(cqr_threshold(scores, alpha) for _, alpha in PAIR_ALPHAS)
    assert ranks == EXPECTED_ONE_BASED_RANKS
    assert tuple(rank - 1 for rank in ranks) == EXPECTED_ZERO_BASED_POSITIONS
    assert thresholds == EXPECTED_THRESHOLDS


def test_zero_based_off_by_one_would_have_been_caught() -> None:
    """`scores[k]` instead of `scores[k-1]`: the exact error §6.2 forbids.

    Without this control the fixture cannot distinguish a correct one-based read
    from an off-by-one that happens to land on a plausible number.
    """
    lower, upper, y = fixture_rows()
    ascending = np.sort(conformity_scores(lower, upper, y))
    wrong: list[float | None] = []
    for _, alpha in PAIR_ALPHAS:
        k = order_statistic_rank(N_CAL, alpha)
        wrong.append(float(ascending[k]) if k < N_CAL else None)
    assert wrong == [None, 8.0, 6.0, 0.0]
    assert tuple(value for value in wrong if value is not None) != EXPECTED_THRESHOLDS[1:]


def test_interpolated_quantile_default_would_have_been_caught() -> None:
    """`np.quantile(scores, 1-alpha)` with linear interpolation is not the rule."""
    lower, upper, y = fixture_rows()
    scores = conformity_scores(lower, upper, y)
    interpolated = tuple(float(np.quantile(scores, 1 - float(alpha))) for _, alpha in PAIR_ALPHAS)
    assert interpolated != EXPECTED_THRESHOLDS
    assert interpolated == pytest.approx((7.05, 6.1, 4.2, -1.5))


def test_rank_is_computed_in_exact_arithmetic() -> None:
    """The product is inexact in binary float; the rank must not depend on that.

    `21 * 0.95` evaluates to 19.949999999999999289..., not 19.95. Swept over
    n_cal = 1..20000 for all four production alphas, `ceil` of the float product
    and of the exact rational agree everywhere -- so this is a hazard the exact
    path forecloses, not a divergence observed in the production range. The test
    records both facts rather than implying a bug that is not there.
    """
    assert Decimal((N_CAL + 1) * 0.95) != Decimal("19.95")
    assert order_statistic_rank(N_CAL, Fraction(1, 20)) == 20
    assert order_statistic_rank(N_CAL, 0.05) == 20
    for n in (19, 20, 39, 40, 59, 1439, 1440, 2159, 2160):
        for alpha, exact in ((0.05, Fraction(1, 20)), (0.10, Fraction(1, 10)),
                             (0.20, Fraction(1, 5)), (0.50, Fraction(1, 2))):
            assert order_statistic_rank(n, alpha) == math.ceil((n + 1) * (1 - exact))


def test_undersized_calibration_set_raises_rather_than_clipping() -> None:
    with pytest.raises(UndersizedCalibrationSet):
        order_statistic_rank(18, Fraction(1, 20))
    order_statistic_rank(19, Fraction(1, 20))
    with pytest.raises(UndersizedCalibrationSet):
        cqr_threshold(np.arange(5.0), Fraction(1, 20))


def test_negative_threshold_narrows_its_pair_and_p50_is_untouched() -> None:
    raw = np.tile(np.arange(9.0) * 10.0, (3, 1))
    thresholds = dict(zip((pair for pair, _ in PAIR_ALPHAS), EXPECTED_THRESHOLDS, strict=True))
    shifted = apply_cqr_thresholds(raw, thresholds)
    position = {label: index for index, label in enumerate(QUANTILE_LABELS)}
    widths_before = raw[:, position["p75"]] - raw[:, position["p25"]]
    widths_after = shifted[:, position["p75"]] - shifted[:, position["p25"]]
    assert np.all(widths_after < widths_before)  # Q = -1 narrows the 50% pair
    outer_before = raw[:, position["p975"]] - raw[:, position["p025"]]
    outer_after = shifted[:, position["p975"]] - shifted[:, position["p025"]]
    assert np.all(outer_after > outer_before)  # Q = +8 widens the 95% pair
    assert np.array_equal(shifted[:, position["p50"]], raw[:, position["p50"]])


def test_fit_thresholds_end_to_end_on_the_fixture() -> None:
    lower, upper, y = fixture_rows()
    matrix = np.zeros((N_CAL, len(QUANTILE_LABELS)))
    position = {label: index for index, label in enumerate(QUANTILE_LABELS)}
    for low, high in (("p025", "p975"), ("p05", "p95"), ("p10", "p90"), ("p25", "p75")):
        matrix[:, position[low]] = lower
        matrix[:, position[high]] = upper
    matrix[:, position["p50"]] = 120.0
    thresholds = fit_cqr_thresholds(matrix, y)
    assert tuple(thresholds[pair] for pair, _ in PAIR_ALPHAS) == EXPECTED_THRESHOLDS
