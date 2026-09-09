-- DuckDB supplementary artifact. The Python feature pipeline is canonical.
-- Run with: uv run python scripts/run_sql_artifact.py

CREATE OR REPLACE VIEW snapshot AS
SELECT * FROM read_parquet('data/snapshot.parquet');

-- 1. Calendar-day/local-hour sources, including absent/ambiguous source hours.
-- Build the expected UTC grid independently of observed prices: dropping one
-- repeated fall-back row must not turn an ambiguous source into a unique match.
CREATE OR REPLACE VIEW lag_features AS
WITH expected_hours AS (
    SELECT hour_utc,
           CAST(timezone('Europe/Berlin', hour_utc) AS DATE) AS delivery_date,
           hour(timezone('Europe/Berlin', hour_utc)) AS local_hour
    FROM generate_series(
        (SELECT timezone('Europe/Berlin', CAST(min(delivery_date) AS TIMESTAMP)) FROM snapshot),
        (SELECT timezone('Europe/Berlin', CAST(max(delivery_date) + 1 AS TIMESTAMP)) - INTERVAL 1 HOUR FROM snapshot),
        INTERVAL 1 HOUR
    ) AS hours(hour_utc)
), sources AS (
    SELECT e.delivery_date, e.local_hour,
           CASE WHEN count(*) = 1 AND count(s.price_eur_mwh) = 1
                THEN max(s.price_eur_mwh) END AS price
    FROM expected_hours e LEFT JOIN snapshot s ON s.timestamp_utc = e.hour_utc
    GROUP BY e.delivery_date, e.local_hour
)
SELECT target.timestamp_utc, target.price_eur_mwh,
       d1.price AS price_lag_24h, d2.price AS price_lag_48h, d7.price AS price_lag_168h
FROM snapshot target
LEFT JOIN sources d1 ON d1.delivery_date = target.delivery_date - 1 AND d1.local_hour = target.local_hour
LEFT JOIN sources d2 ON d2.delivery_date = target.delivery_date - 2 AND d2.local_hour = target.local_hour
LEFT JOIN sources d7 ON d7.delivery_date = target.delivery_date - 7 AND d7.local_hour = target.local_hour
ORDER BY target.timestamp_utc;

-- 2. One result per delivery day, over exactly 168/720 canonical UTC hours
-- ending at the close of D-1. Broadcast by delivery_date to use on D's curve.
-- Missing history (including the snapshot head) fails closed, never shortens
-- the window. Sample stddev and linearly interpolated quantiles match Python.
CREATE OR REPLACE VIEW rolling_features AS
WITH boundaries AS (
    SELECT DISTINCT delivery_date,
           timezone('Europe/Berlin', CAST(delivery_date AS TIMESTAMP)) AS boundary
    FROM snapshot
), aggregates AS (
    SELECT b.delivery_date,
           count(s.price_eur_mwh) AS count_720,
           count(s.price_eur_mwh) FILTER (WHERE s.timestamp_utc >= b.boundary - INTERVAL 168 HOURS) AS count_168,
           avg(s.price_eur_mwh) AS mean_720,
           stddev_samp(s.price_eur_mwh) AS std_720,
           avg(s.price_eur_mwh) FILTER (WHERE s.timestamp_utc >= b.boundary - INTERVAL 168 HOURS) AS mean_168,
           stddev_samp(s.price_eur_mwh) FILTER (WHERE s.timestamp_utc >= b.boundary - INTERVAL 168 HOURS) AS std_168,
           quantile_cont(s.price_eur_mwh, 0.05) FILTER (WHERE s.timestamp_utc >= b.boundary - INTERVAL 168 HOURS) AS q05,
           quantile_cont(s.price_eur_mwh, 0.50) FILTER (WHERE s.timestamp_utc >= b.boundary - INTERVAL 168 HOURS) AS q50,
           quantile_cont(s.price_eur_mwh, 0.95) FILTER (WHERE s.timestamp_utc >= b.boundary - INTERVAL 168 HOURS) AS q95,
           count(*) FILTER (WHERE s.price_eur_mwh < 0 AND s.timestamp_utc >= b.boundary - INTERVAL 168 HOURS) AS negatives
    FROM boundaries b LEFT JOIN snapshot s
      ON s.timestamp_utc >= b.boundary - INTERVAL 720 HOURS AND s.timestamp_utc < b.boundary
    GROUP BY b.delivery_date
)
SELECT delivery_date,
       CASE WHEN count_168 = 168 THEN mean_168 END AS price_roll_mean_168h,
       CASE WHEN count_168 = 168 THEN std_168 END AS price_roll_std_168h,
       CASE WHEN count_720 = 720 THEN mean_720 END AS price_roll_mean_720h,
       CASE WHEN count_720 = 720 THEN std_720 END AS price_roll_std_720h,
       CASE WHEN count_168 = 168 THEN q05 END AS price_roll_q05_168h,
       CASE WHEN count_168 = 168 THEN q50 END AS price_roll_q50_168h,
       CASE WHEN count_168 = 168 THEN q95 END AS price_roll_q95_168h,
       CASE WHEN count_168 = 168 THEN negatives END AS negative_price_count_168h
FROM aggregates ORDER BY delivery_date;

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
