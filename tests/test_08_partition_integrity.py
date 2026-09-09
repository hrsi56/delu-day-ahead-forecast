from datetime import date, timedelta
import json
from pathlib import Path

import pandas as pd

from delu_forecast.partitions import pin_partition_spec, serializable_partition_spec


def test_tail_partitions_and_fold_calibration_embargoes_are_integral() -> None:
    root = Path(__file__).resolve().parents[1]
    committed = json.loads((root / 'data/partitions.json').read_text())
    cutoff = date.fromisoformat(committed['snapshot_cutoff'])
    assert serializable_partition_spec(cutoff) == committed
    spec = pin_partition_spec(cutoff)
    tail = list(spec['tail_partitions'].values())
    assert [len(window.dates()) for window in tail] == [90, 1, 60, 1, 90]
    assert min(tail[0].dates()) >= date(2025, 10, 1)
    assert len(set().union(*(window.dates() for window in tail))) == 242
    for left, right in zip(tail, tail[1:]):
        assert left.end + timedelta(days=1) == right.start
        assert left.dates().isdisjoint(right.dates())

    final_calibration = spec['tail_partitions']['final_calibration'].dates()
    holdout = spec['tail_partitions']['holdout'].dates()
    embargoes = [spec['tail_partitions']['embargo_a'], spec['tail_partitions']['embargo_b']]
    for fold in spec['development_folds']:
        assert len(fold.evaluation.dates()) == 90
        assert len(fold.calibration.dates()) == 60
        assert fold.proper_training.end + timedelta(days=1) == fold.calibration_embargo.start
        assert fold.calibration_embargo.end + timedelta(days=1) == fold.calibration.start
        assert fold.calibration.end + timedelta(days=1) == fold.evaluation_embargo.start
        assert fold.evaluation_embargo.end + timedelta(days=1) == fold.evaluation.start
        for component in (fold.proper_training, fold.calibration, fold.evaluation):
            assert final_calibration.isdisjoint(component.dates())
            assert holdout.isdisjoint(component.dates())  # No holdout targets in fits/thresholds.
        embargoes.extend([fold.calibration_embargo, fold.evaluation_embargo])
    for diagnostic in spec['diagnostic_windows']:
        assert final_calibration.isdisjoint(diagnostic.dates())
        assert holdout.isdisjoint(diagnostic.dates())
    # The spectral diagnostic spans the archive head through eda_cutoff.
    eda_dates = set(pd.date_range('2019-01-01', spec['eda_cutoff'], freq='D').date)
    assert final_calibration.isdisjoint(eda_dates)
    assert holdout.isdisjoint(eda_dates)

    snapshot = pd.read_parquet(root / 'data/snapshot.parquet', columns=['timestamp_utc'])
    utc = pd.DatetimeIndex(snapshot.timestamp_utc)
    local_dates = utc.tz_convert('Europe/Berlin').date
    for embargo in embargoes:
        assert len(embargo.dates()) == 1
        start = pd.Timestamp(embargo.start, tz='Europe/Berlin')
        end = pd.Timestamp(embargo.end + timedelta(days=1), tz='Europe/Berlin')
        expected = pd.date_range(start.tz_convert('UTC'), end.tz_convert('UTC'), freq='h', inclusive='left')
        assert utc[local_dates == embargo.start].as_unit("ns").equals(expected.as_unit("ns"))
