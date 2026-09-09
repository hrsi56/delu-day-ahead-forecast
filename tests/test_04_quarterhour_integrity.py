import pandas as pd
import pytest

from delu_forecast.ingest import (
    IncompleteQuarterHourBinError,
    SERIES_SPECS,
    aggregate_quarterhours,
    assemble_price_series,
    stitch_chunks,
)


def _raw(start: str, periods: int, values: list[float] | None = None) -> pd.DataFrame:
    index = pd.date_range(start, periods=periods, freq="15min", tz="UTC")
    return pd.DataFrame({"timestamp_utc": index, "value": values or list(range(periods))})


def test_chunk_stitch_missing_quarter_and_series_specific_aggregation() -> None:
    raw = _raw("2025-10-01T00:00:00Z", 8, [10, 20, 30, 40, 1, 2, 3, 4])
    stitched = stitch_chunks([raw.iloc[:5], raw.iloc[4:]])
    assert len(stitched) == 8
    price = aggregate_quarterhours(stitched, SERIES_SPECS[0])
    load = aggregate_quarterhours(stitched, SERIES_SPECS[1])
    assert price.iloc[0] == 25
    assert load.iloc[0] == 100
    with pytest.raises(IncompleteQuarterHourBinError):
        aggregate_quarterhours(stitched.drop(index=2), SERIES_SPECS[1])


def test_smard_filters_map_to_the_four_plan_series() -> None:
    mapping = {spec.column: spec.filter_id for spec in SERIES_SPECS}
    assert mapping["price_eur_mwh"] == 4169
    assert mapping["load_forecast_mw"] == 411
    assert mapping["wind_onshore_forecast_mw"] == 123
    assert mapping["solar_forecast_mw"] == 125
    assert mapping["wind_offshore_forecast_mw"] == 3791
    assert mapping["wind_onshore_actual_mw"] == 4067
    assert mapping["solar_actual_mw"] == 4068
    assert mapping["wind_offshore_actual_mw"] == 1225


def test_price_transition_is_continuous_and_four_quarters_are_averaged() -> None:
    pre = pd.DataFrame(
        {
            "timestamp_utc": pd.date_range("2025-09-30T20:00:00Z", periods=2, freq="h", tz="UTC"),
            "value": [50.0, 60.0],
        }
    )
    post = _raw("2025-09-30T22:00:00Z", 8, [40, 60, 80, 100, 20, 30, 40, 50])
    result = assemble_price_series(pre, post)
    assert result.index.equals(pd.date_range("2025-09-30T20:00:00Z", periods=4, freq="h", tz="UTC"))
    assert result.tolist() == [50.0, 60.0, 70.0, 35.0]


@pytest.mark.parametrize('day,quarters', [('2025-10-26', 100), ('2026-03-29', 92), ('2025-10-01', 96)])
def test_entsoe_inclusive_endpoint_is_normalized_to_half_open_berlin_day(day: str, quarters: int) -> None:
    # Exercise the actual reconciliation normalizer, without a network request.
    from importlib.util import module_from_spec, spec_from_file_location
    from pathlib import Path
    from datetime import timedelta
    spec = spec_from_file_location('reconcile', Path(__file__).resolve().parents[1] / 'scripts/reconcile_entsoe_smard.py')
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    start = pd.Timestamp(day, tz='Europe/Berlin')
    end = pd.Timestamp(start.date() + timedelta(days=1), tz='Europe/Berlin')
    index = pd.date_range(start, end, freq='15min')
    assert len(index) == quarters + 1  # The pinned client's inclusive endpoint.
    raw = pd.Series(range(len(index)), index=index, dtype=float)
    hourly = module._hourly_entsoe_price(raw, start.date())
    assert len(hourly) == quarters // 4
    assert hourly.notna().all()
    assert hourly.index.equals(pd.date_range(start.tz_convert('UTC'), end.tz_convert('UTC'), freq='h', inclusive='left'))
    assert hourly.tolist() == [sum(range(offset, offset + 4)) / 4 for offset in range(0, quarters, 4)]
    milliseconds = raw.copy()
    milliseconds.index = milliseconds.index.as_unit("ms")
    assert module._hourly_entsoe_price(milliseconds, start.date()).tolist() == hourly.tolist()
    # A single surviving quarter must not be mistaken for a PT60M product.
    with pytest.raises(ValueError, match='incomplete'):
        module._hourly_entsoe_price(raw.drop(index=raw.index[1:4]), start.date())
