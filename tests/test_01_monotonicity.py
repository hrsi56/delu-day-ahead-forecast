import numpy as np

from delu_forecast.postprocess import SYMMETRIC_PAIRS, cqr_then_isotonic


def test_cqr_then_isotonic_has_zero_crossings_even_for_negative_intervals() -> None:
    raw = np.array(
        [
            [-20, -10, -5, 0, -2, 3, 2, 9, 8],
            [-8, -4, -1, 2, 0, 1, 5, 4, 9],
        ],
        dtype=float,
    )
    thresholds = {pair: value for pair, value in zip(SYMMETRIC_PAIRS, (2.0, -1.0, 3.0, -2.0), strict=True)}
    final = cqr_then_isotonic(raw, thresholds)
    assert np.all(np.diff(final, axis=1) >= 0)
    assert final.shape == raw.shape
