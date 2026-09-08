from datetime import date

import pandas as pd

from delu_forecast.features import build_base_features

from conftest import synthetic_snapshot


def test_current_target_cannot_change_its_own_rolling_features() -> None:
    snapshot = synthetic_snapshot(date(2024, 1, 1), date(2024, 2, 20))
    before = build_base_features(snapshot)
    row = before.index[900]
    changed = snapshot.copy()
    changed.loc[changed["timestamp_utc"].eq(row), "price_eur_mwh"] = -999_999.0
    after = build_base_features(changed)
    columns = [column for column in before if column.startswith("price_roll_") or column == "negative_price_count_168h"]
    pd.testing.assert_series_equal(before.loc[row, columns], after.loc[row, columns])
