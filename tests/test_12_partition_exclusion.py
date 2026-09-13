"""Model-layer partition discipline, asserted against the real pinned spec.

`test_08` asserts the partition file's own geometry. This file asserts what the
CP-2 model layer does with it: that the reserved tail never reaches a fit, a
threshold, a development fold component, or a diagnostic window -- and that the
guard which says so can actually fail.
"""

from __future__ import annotations

from datetime import date, timedelta

import numpy as np
import pandas as pd
import pytest

from delu_forecast.folds import (
    TAIL_ORDER,
    excluded_from_development,
    final_fit_window,
    load_partition_spec,
    window_mask,
)
from delu_forecast.partitions import Window

SPEC = load_partition_spec()


def _dates(window: Window) -> list[date]:
    return sorted(window.dates())


def test_reserved_tail_is_disjoint_from_every_fold_component_separately() -> None:
    reserved: set[date] = set()
    for window in excluded_from_development(SPEC):
        reserved |= window.dates()
    for fold in SPEC.development_folds:
        for name in ("proper_training", "calibration_embargo", "calibration", "evaluation_embargo", "evaluation"):
            component: Window = getattr(fold, name)
            overlap = component.dates() & reserved
            assert not overlap, f"{fold.name}.{name} overlaps the reserved tail on {sorted(overlap)[:3]}"


def test_reserved_tail_is_disjoint_from_every_diagnostic_window() -> None:
    reserved: set[date] = set()
    for window in excluded_from_development(SPEC):
        reserved |= window.dates()
    for window in SPEC.diagnostic_windows:
        assert not window.dates() & reserved


def test_final_fit_window_stops_strictly_before_embargo_a() -> None:
    window = final_fit_window(SPEC)
    assert window.end == SPEC.embargo_a.start - timedelta(days=1)
    assert window.end == SPEC.fold("fold_5").evaluation.end
    assert SPEC.embargo_a.start not in window.dates()
    assert not window.dates() & SPEC.final_calibration.dates()
    assert not window.dates() & SPEC.holdout.dates()


def test_every_embargo_holds_exactly_one_complete_delivery_day() -> None:
    embargoes = [SPEC.tail_partitions["embargo_a"], SPEC.tail_partitions["embargo_b"]]
    embargoes += [fold.calibration_embargo for fold in SPEC.development_folds]
    embargoes += [fold.evaluation_embargo for fold in SPEC.development_folds]
    for window in embargoes:
        assert len(window.dates()) == 1, window


def test_tail_partitions_are_contiguous_and_ordered() -> None:
    windows = [SPEC.tail_partitions[name] for name in TAIL_ORDER]
    for left, right in zip(windows[:-1], windows[1:], strict=True):
        assert left.end + timedelta(days=1) == right.start
        assert not left.dates() & right.dates()
    assert windows[-1].end == SPEC.snapshot_cutoff
    assert min(SPEC.tail_partitions["fold_5"].dates()) >= date(2025, 10, 1)


def test_window_mask_guard_is_not_inert() -> None:
    """Positive control: the mask that reports 'no reserved rows' must find them."""
    holdout_day = SPEC.holdout.start
    dates = pd.Index([holdout_day, SPEC.fold("fold_1").evaluation.start])
    mask = window_mask(dates, SPEC.holdout)
    assert mask.tolist() == [True, False]
    assert int(np.count_nonzero(mask)) == 1


def test_assert_no_reserved_rows_raises_when_a_holdout_row_is_smuggled_in() -> None:
    from delu_forecast.experiment import Inputs, assert_no_reserved_rows

    dates = pd.Index([SPEC.fold("fold_1").evaluation.start, SPEC.holdout.start])
    inputs = Inputs(
        snapshot=pd.DataFrame(),
        spec=SPEC,
        index=pd.DatetimeIndex([]),
        delivery_dates=dates,
        target=np.zeros(2),
        wide_features=pd.DataFrame(),
        eligible=np.ones(2, dtype=bool),
    )
    assert_no_reserved_rows(inputs, np.array([True, False]), "clean")
    with pytest.raises(AssertionError, match="reserved tail partition"):
        assert_no_reserved_rows(inputs, np.array([True, True]), "contaminated")
