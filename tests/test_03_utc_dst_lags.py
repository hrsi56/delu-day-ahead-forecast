"""§9.4.3: canonical UTC identity retains every real Berlin delivery hour."""
from datetime import date

import pandas as pd

from delu_forecast.features import build_base_features
from conftest import synthetic_snapshot


def test_berlin_identity_survives_both_dst_transitions() -> None:
    snapshot = synthetic_snapshot(date(2025, 3, 1), date(2025, 11, 10))
    features = build_base_features(snapshot)
    expected = pd.date_range('2025-02-28T23:00:00Z', '2025-11-09T23:00:00Z', freq='h', inclusive='left')
    assert features.index.equals(expected)
    assert features.index.is_unique
    local = features.index.tz_convert('Europe/Berlin')
    spring = local[local.date == date(2025, 3, 30)]
    fall = local[local.date == date(2025, 10, 26)]
    assert len(spring) == 23 and 2 not in spring.hour
    assert len(fall) == 25
    repeated = fall[fall.hour == 2]
    assert len(repeated) == 2 and repeated.tz_convert('UTC').is_unique
    assert len({value.utcoffset() for value in repeated}) == 2
    identity = pd.MultiIndex.from_arrays([local.date, local.hour, [value.utcoffset() for value in local]])
    assert identity.is_unique
