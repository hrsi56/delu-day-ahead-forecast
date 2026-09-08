from datetime import date, timedelta

import numpy as np
import pandas as pd

from delu_forecast.features import residual_proxy_details

from conftest import synthetic_snapshot


def test_residual_proxy_is_42_complete_days_d2_bounded_and_dst_safe() -> None:
    snapshot = synthetic_snapshot(date(2024, 1, 1), date(2024, 12, 5))
    local_dates = pd.to_datetime(snapshot["delivery_date"])
    snapshot["vre_actual_mw"] = (local_dates - pd.Timestamp("2024-01-01")).dt.days * 100 + snapshot["local_hour"]
    details = residual_proxy_details(snapshot)
    local = details.index.tz_convert("Europe/Berlin")

    spring_hour_2 = details.loc[(local.date == date(2024, 4, 20)) & (local.hour == 2)].iloc[0]
    fall_hour_2 = details.loc[(local.date == date(2024, 11, 20)) & (local.hour == 2)].iloc[0]
    assert spring_hour_2["window_observation_count"] == 41
    assert fall_hour_2["window_observation_count"] == 43

    target = date(2024, 4, 20)
    hour_zero = details.loc[(local.date == target) & (local.hour == 0)].iloc[0]
    expected_dates = [target - timedelta(days=43) + timedelta(days=offset) for offset in range(42)]
    expected = np.mean([(value - date(2024, 1, 1)).days * 100 for value in expected_dates])
    assert hour_zero["vre_norm"] == expected
    assert hour_zero["window_end_delivery_date"] == target - timedelta(days=2)

    spring_target = details.loc[local.date == date(2024, 3, 31)]
    assert 2 not in spring_target.index.tz_convert("Europe/Berlin").hour
    fall_target = details.loc[(local.date == date(2024, 10, 27)) & (local.hour == 2)]
    assert len(fall_target) == 2
    assert fall_target["vre_norm"].nunique() == 1
