"""Information-boundary controls for the unscored, one-origin probe."""
from datetime import date
import json
from pathlib import Path

import pytest

from cp15 import feasibility_probe as probe


def test_probe_accepts_training_and_refuses_outer_holdout_and_pre2019():
    partitions = json.loads(Path('data/partitions.json').read_text())
    probe.validate_probe_day(date(2020, 4, 1), partitions)
    for day in [date(2018, 12, 31), date(2020, 7, 1), date(2022, 8, 15), date(2026, 7, 1)]:
        with pytest.raises(ValueError, match='proper training'):
            probe.validate_probe_day(day, partitions)


def test_input_projection_never_materializes_delivery_day_targets(monkeypatch, tmp_path):
    import pyarrow.dataset as ds
    real_dataset = ds.dataset
    calls = []

    class GuardedDataset:
        def __init__(self, underlying):
            self.underlying = underlying

        def to_table(self, *, columns, filter):
            result = self.underlying.to_table(columns=columns, filter=filter)
            # Guard the actual rows handed to the model-input code, before pandas.
            times = result.column('timestamp_utc').to_pylist()
            if 'price_eur_mwh' in columns:
                assert all(t.isoformat() < '2020-03-31T22:00:00+00:00' for t in times)
            assert min(times).year >= 2019
            assert max(times).date() <= date(2020, 4, 1)
            assert not any('actual' in c or 'wind' in c or 'solar' in c for c in columns)
            calls.append(columns)
            return result

    monkeypatch.setattr(ds, 'dataset', lambda *a, **kw: GuardedDataset(real_dataset(*a, **kw)))
    monkeypatch.setattr(probe, 'REPORT', tmp_path)
    history, future = probe.prepare_inputs()
    assert len(calls) == 2
    assert 'target' in history and 'target' not in future
    assert len(history) == 168 and len(future) == 24
    assert (history.timestamp.diff().dropna().dt.total_seconds() == 3600).all()
    # The canonical input is regular despite crossing Berlin's spring DST day.
    assert str(history.timestamp.iloc[0]) == '2020-03-24 22:00:00'
    assert str(future.timestamp.iloc[-1]) == '2020-04-01 21:00:00'
