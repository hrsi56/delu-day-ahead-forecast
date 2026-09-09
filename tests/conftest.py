from __future__ import annotations

from datetime import date

import numpy as np
import pandas as pd

from delu_forecast.ingest import BERLIN


def synthetic_snapshot(start: date, end_exclusive: date) -> pd.DataFrame:
    start_utc = pd.Timestamp(start, tz=BERLIN).tz_convert("UTC")
    end_utc = pd.Timestamp(end_exclusive, tz=BERLIN).tz_convert("UTC")
    index = pd.date_range(start_utc, end_utc, freq="h", inclusive="left", tz="UTC")
    local = index.tz_convert(BERLIN)
    values = np.arange(len(index), dtype="float64")
    return pd.DataFrame(
        {
            "timestamp_utc": index,
            "delivery_date": local.date,
            "local_hour": local.hour,
            "utc_offset_minutes": [int(value.utcoffset().total_seconds() // 60) for value in local],
            "price_eur_mwh": values - 20.0,
            "load_forecast_mw": 50_000.0 + values % 100,
            "vre_actual_mw": 10_000.0 + values % 50,
        }
    )
