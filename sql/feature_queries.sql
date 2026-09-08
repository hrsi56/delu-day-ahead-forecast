-- DuckDB supplementary artifact. The Python feature pipeline is canonical.
-- Run with: uv run python scripts/run_sql_artifact.py

CREATE OR REPLACE VIEW snapshot AS
SELECT * FROM read_parquet('data/snapshot.parquet');

-- 1. Fixed UTC lags. timestamp_utc is canonical; no local-time row arithmetic.
CREATE OR REPLACE VIEW lag_features AS SELECT
    timestamp_utc,
    price_eur_mwh,
    lag(price_eur_mwh, 24) OVER (ORDER BY timestamp_utc) AS price_lag_24h,
    lag(price_eur_mwh, 168) OVER (ORDER BY timestamp_utc) AS price_lag_168h
FROM snapshot
ORDER BY timestamp_utc;

-- 2. Closed-left rolling statistics: the current target is excluded explicitly.
CREATE OR REPLACE VIEW rolling_features AS SELECT
    timestamp_utc,
    avg(price_eur_mwh) OVER (
        ORDER BY timestamp_utc ROWS BETWEEN 168 PRECEDING AND 1 PRECEDING
    ) AS price_roll_mean_168h,
    stddev_samp(price_eur_mwh) OVER (
        ORDER BY timestamp_utc ROWS BETWEEN 168 PRECEDING AND 1 PRECEDING
    ) AS price_roll_std_168h,
    count(*) FILTER (WHERE price_eur_mwh < 0) OVER (
        ORDER BY timestamp_utc ROWS BETWEEN 168 PRECEDING AND 1 PRECEDING
    ) AS negative_price_count_168h
FROM snapshot
ORDER BY timestamp_utc;

-- 3. Null and duplicate scans. A44 nulls and duplicate UTC identities must be zero.
CREATE OR REPLACE VIEW data_quality_checks AS SELECT
    count(*) FILTER (WHERE price_eur_mwh IS NULL) AS null_price_rows,
    count(*) - count(DISTINCT timestamp_utc) AS duplicate_utc_rows
FROM snapshot;

-- 4. Source-bin checks. Feature feeds are four-quarter sums for the whole archive;
-- A44 is one hourly source interval before the MTU transition and four afterward.
CREATE OR REPLACE VIEW source_bin_checks AS SELECT
    count(*) FILTER (WHERE load_forecast_mw IS NOT NULL AND load_forecast_mw_source_quarter_count <> 4) AS bad_load_bins,
    count(*) FILTER (WHERE vre_forecast_mw IS NOT NULL AND (
        wind_onshore_forecast_mw_source_quarter_count <> 4 OR
        wind_offshore_forecast_mw_source_quarter_count <> 4 OR
        solar_forecast_mw_source_quarter_count <> 4
    )) AS bad_a69_bins,
    count(*) FILTER (WHERE vre_actual_mw IS NOT NULL AND (
        wind_onshore_actual_mw_source_quarter_count <> 4 OR
        wind_offshore_actual_mw_source_quarter_count <> 4 OR
        solar_actual_mw_source_quarter_count <> 4
    )) AS bad_a75_bins,
    count(*) FILTER (
        WHERE delivery_date >= DATE '2025-10-01' AND price_source_interval_count <> 4
    ) AS bad_post_transition_price_bins
FROM snapshot;
