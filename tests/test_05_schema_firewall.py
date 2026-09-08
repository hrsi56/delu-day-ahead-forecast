import pytest

from delu_forecast.features import AUGMENTED_FEATURES, BASE_FEATURES
from delu_forecast.schema import (
    BENCHMARK_ADDITIONS,
    validate_benchmark_runtime_schema,
    validate_champion_runtime_schema,
    validate_historical_actual_input,
)


def test_champion_benchmark_runtime_schema_firewall() -> None:
    validate_champion_runtime_schema(BASE_FEATURES, "base")
    validate_champion_runtime_schema(AUGMENTED_FEATURES, "base_plus_residual_load_proxy")
    with pytest.raises(ValueError, match="forbidden"):
        validate_champion_runtime_schema(BASE_FEATURES + ("wind_onshore_forecast_mw",), "base")
    with pytest.raises(ValueError, match="forbidden"):
        validate_champion_runtime_schema(BASE_FEATURES + ("vre_actual_mw",), "base")
    validate_historical_actual_input("vre_actual_mw", latest_delivery_lag_days=-2)
    with pytest.raises(ValueError, match="D-2"):
        validate_historical_actual_input("vre_actual_mw", latest_delivery_lag_days=-1)
    validate_benchmark_runtime_schema(BASE_FEATURES + BENCHMARK_ADDITIONS, "base")
    with pytest.raises(ValueError, match="mismatch"):
        validate_benchmark_runtime_schema(BASE_FEATURES + BENCHMARK_ADDITIONS + ("vre_actual_mw",), "base")
