from __future__ import annotations

from datetime import date
import os

import numpy as np
import pandas as pd
import pytest

from delu_forecast.ingest import BERLIN


STRESS_SKIP_REASON = (
    "CP-26 supervision stress test, run locally because a 4-vCPU CI runner cannot host it "
    "reliably, RUN_STRESS=1 forces it."
)


def pytest_configure(config):
    config.addinivalue_line("markers", "stress: CP-26 real-process supervision timing tests")
    if os.environ.get("CI") == "true" and os.environ.get("RUN_STRESS") != "1":
        # Keep the reason visible in the workflow's unmodified `pytest -q` output.
        if "s" not in config.option.reportchars:
            config.option.reportchars += "s"


def pytest_collection_modifyitems(items):
    if os.environ.get("CI") == "true" and os.environ.get("RUN_STRESS") != "1":
        skip = pytest.mark.skip(reason=STRESS_SKIP_REASON)
        for item in items:
            if item.get_closest_marker("stress"):
                item.add_marker(skip)


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
