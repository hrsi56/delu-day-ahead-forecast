from datetime import date

import pandas as pd

from delu_forecast.features import build_base_features

from conftest import synthetic_snapshot


def test_utc_lags_and_berlin_identity_survive_both_dst_transitions() -> None:
    snapshot = synthetic_snapshot(date(2025, 3, 1), date(2025, 11, 10))
    features = build_base_features(snapshot)
    prices = snapshot.set_index("timestamp_utc")["price_eur_mwh"]
    local = features.index.tz_convert("Europe/Berlin")
    selected = features.loc[(local.date == date(2025, 3, 30)) | (local.date == date(2025, 10, 26))]
    assert len(selected.loc[selected.index.tz_convert("Europe/Berlin").date == date(2025, 3, 30)]) == 23
    assert len(selected.loc[selected.index.tz_convert("Europe/Berlin").date == date(2025, 10, 26)]) == 25
    for timestamp, row in selected.iterrows():
        assert row["price_lag_24h"] == prices.loc[timestamp - pd.Timedelta(hours=24)]
        assert row["price_lag_168h"] == prices.loc[timestamp - pd.Timedelta(hours=168)]
    identity = pd.MultiIndex.from_arrays(
        [local.date, local.hour, [int(value.utcoffset().total_seconds() // 60) for value in local]]
    )
    assert identity.is_unique
