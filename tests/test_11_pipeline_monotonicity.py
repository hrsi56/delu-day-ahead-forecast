"""The one retained hard gate: zero crossing violations after CQR-then-isotonic.

`test_01` already asserts monotonicity on two hand-written rows. This file adds
what makes the assertion load-bearing: a positive control proving the detector
can report a violation, adversarial inputs (heavily crossed raw heads, negative
and zero-crossing intervals, threshold signs mixed), and the ordering property
that isotonic -- not CQR -- is what guarantees the result.
"""

from __future__ import annotations

import numpy as np

from delu_forecast.conformal import PAIR_ALPHAS, apply_cqr_thresholds, cqr_then_isotonic, isotonic_last
from delu_forecast.metrics import crossing_violations

PAIRS = tuple(pair for pair, _ in PAIR_ALPHAS)


def test_detector_reports_violations_on_deliberately_crossed_input() -> None:
    """Positive control. Without it, `crossing_violations` could return 0 always."""
    descending = np.tile(np.arange(9.0)[::-1], (4, 1))
    assert crossing_violations(descending) == 4 * 8
    almost = np.tile(np.arange(9.0), (1, 1)).copy()
    assert crossing_violations(almost) == 0
    almost[0, 5] = almost[0, 4] - 1e-12
    assert crossing_violations(almost) == 1  # no tolerance: 1e-12 is a violation


def test_zero_violations_on_adversarial_negative_and_crossing_intervals() -> None:
    rng = np.random.default_rng(20260914)
    raw = rng.normal(loc=-40.0, scale=60.0, size=(4000, 9))  # deliberately unordered
    assert crossing_violations(raw) > 0
    for thresholds in (
        dict(zip(PAIRS, (8.0, 7.0, 5.0, -1.0), strict=True)),
        dict(zip(PAIRS, (-3.0, -2.0, -1.0, -0.5), strict=True)),
        dict(zip(PAIRS, (0.0, 0.0, 0.0, 0.0), strict=True)),
    ):
        final = cqr_then_isotonic(raw, thresholds)
        assert crossing_violations(final) == 0
        assert np.all(np.diff(final, axis=1) >= 0)
    spanning = raw[(raw.min(axis=1) < 0) & (raw.max(axis=1) > 0)]
    assert len(spanning) > 100  # the zero-crossing intervals this market actually produces


def test_cqr_alone_does_not_guarantee_ordering() -> None:
    """Isotonic is last because CQR cannot fix a globally unordered nine-vector."""
    raw = np.array([[-20.0, -10, -5, 0, -2, 3, 2, 9, 8]])
    shifted = apply_cqr_thresholds(raw, dict(zip(PAIRS, (2.0, -1.0, 3.0, -2.0), strict=True)))
    assert crossing_violations(shifted) > 0
    assert crossing_violations(isotonic_last(shifted)) == 0


def test_isotonic_preserves_the_mean_of_each_pooled_block() -> None:
    values = np.array([[5.0, 1.0, 3.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0]])
    result = isotonic_last(values)
    assert np.allclose(result[0, :3], 3.0)
    assert np.isclose(result.sum(), values.sum())
