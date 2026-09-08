from datetime import date, timedelta

from delu_forecast.partitions import pin_partition_spec


def test_tail_partitions_and_fold_calibration_embargoes_are_integral() -> None:
    spec = pin_partition_spec(date(2026, 9, 6))
    tail = list(spec["tail_partitions"].values())
    assert [len(window.dates()) for window in tail] == [90, 1, 60, 1, 90]
    assert min(tail[0].dates()) >= date(2025, 10, 1)
    assert len(set().union(*(window.dates() for window in tail))) == 242
    for left, right in zip(tail, tail[1:]):
        assert left.end + timedelta(days=1) == right.start
        assert left.dates().isdisjoint(right.dates())

    final_calibration = spec["tail_partitions"]["final_calibration"].dates()
    holdout = spec["tail_partitions"]["holdout"].dates()
    for fold in spec["development_folds"]:
        assert len(fold.evaluation.dates()) == 90
        assert len(fold.calibration.dates()) == 60
        assert fold.proper_training.end + timedelta(days=1) == fold.calibration_embargo.start
        assert fold.calibration_embargo.end + timedelta(days=1) == fold.calibration.start
        assert fold.calibration.end + timedelta(days=1) == fold.evaluation_embargo.start
        assert fold.evaluation_embargo.end + timedelta(days=1) == fold.evaluation.start
        assert final_calibration.isdisjoint(fold.evaluation.dates())
        assert holdout.isdisjoint(fold.proper_training.dates())
        assert holdout.isdisjoint(fold.calibration.dates())
        assert holdout.isdisjoint(fold.evaluation.dates())
