# CP-1 v6.8 delivery-day availability evidence

This acceptance audit checks `capstone_V6_8.md` §4.0–§5.2, §9.4, §9.6 and
§12 CP-1. It performs no fitting, threshold estimation, catalog selection or
holdout evaluation. Python remains the canonical feature pipeline; SQL is a
supplementary public artifact.

## Observed artifact checks

- Snapshot SHA-256 remains
  `7dd2dc73407706ca6bd3c1ad51d201ac0de35eec5ca129ce320cca639f697f00`.
  No data was re-pulled or replaced. The committed five-day reconciliation
  remains 120/120 prices within €0.01/MWh, maximum difference €0.00.
- `uv run --frozen pytest -q`: **25 passed**, covering all nine §9.4 property
  families. Parameterization expands the nine families into 25 test cases.
- `uv run --frozen python scripts/audit_snapshot.py`: 67,343 continuous UTC
  hours; zero null prices; 2,806 complete delivery days (8 × 23-hour,
  2,791 × 24-hour, 7 × 25-hour). Catalog sizes remain 25 and 26, with only
  `residual_load_proxy` added. Complete feature rows are now 66,336 / 65,016;
  these counts are reported, not acceptance thresholds.
- `uv run --frozen python scripts/audit_delivery_day_features.py` independently
  selects raw source dates/hours and pre-D windows for **all 11 price columns
  on all 67,343 rows**. Every rolling column equals its raw-value oracle and
  stays constant within each delivery day, including null at the archive head.
  Calendar-lag null counts are 39 / 63 / 183 for D−1 / D−2 / D−7, reflecting
  missing head history and unavailable/ambiguous source hours.
- The same audit compares SQL with those raw-value oracles. SQL emits 67,343
  lag rows and 2,806 rolling delivery-day rows. Largest absolute numerical
  difference observed: approximately **6.8e-13**, below the 1e-9 absolute
  tolerance; lag comparisons are exact. SQL quality and source-bin checks
  are all zero.
- A65 day means fail closed on ten incomplete days. Eight days have no A65
  values; **2023-10-29 and 2024-10-27 have 24 of 25** and now return null for
  their entire delivery day. Complete 23/24/25-hour positive controls equal
  direct means before every possible single-hour deletion/null is tested.
- The three spectral figures and `spectral_peak_bins.csv` reproduce
  byte-for-byte via
  `uv run --frozen python scripts/generate_spectral_artifacts.py --output-dir /tmp/cp1-spectral-check`.
  The script uses 63,695 EDA-eligible hours through 2026-04-07. Existing figures,
  partitions, snapshot, source mapping and A75 proxy construction are retained.

## Feature-by-feature boundaries

The [leakage audit](../docs/data-leakage-audit.md) lists every champion feature.
`price_lag_24h`, `price_lag_48h` and `price_lag_168h` consume only the matching
local hour on D−1, D−2 and D−7 respectively. Localization rejects ambiguous
and unavailable source hours; even a partially observed repeated hour cannot
become an apparently unique source. Repeated target hours retain their two
UTC identities and receive the same valid historical-hour match.

`price_roll_mean_168h`, `price_roll_std_168h`, `price_roll_q05_168h`,
`price_roll_q50_168h`, `price_roll_q95_168h` and `negative_price_count_168h`
consume exactly 168 canonical hours ending at the close of D−1.
`price_roll_mean_720h` and `price_roll_std_720h` consume exactly 720 at that same
boundary. Each statistic is computed once per delivery day and broadcast.
Missing expected observations null the affected statistic instead of extending
or shortening its window. No price-derived feature consumes D or a later date.

The SQL lag query uses a complete expected calendar grid and D−1/D−2/D−7
local-hour joins, including a source-cardinality check. The rolling query uses
local-midnight D boundaries, joins the preceding 168/720 UTC hours, enforces
full non-null counts, and produces one result per D. Both implementations use
sample standard deviation and linear-interpolation quantiles.

## What a green suite alone would miss

Before repair, the unchanged ten-test suite passed against attempt 1. An
independent whole-snapshot source-boundary calculation reproduces **64,537 /
67,343 rows (95.83%)** exposed by its row-wise rolling construction and **seven**
UTC-24h lag rows whose source was the same delivery day. The new checks compare
numbers as well as checking invariance: an all-null or overly old result must
not pass just because changing D prices leaves it unchanged.

The following deliberately faulty controls were run in memory against the new
committed test definitions. They do not alter the working tree. The wrapper
exits successfully only when pytest rejects the fault with assertion failures
(exit 1), rather than failing collection or setup.

| Command suffix for `uv run --frozen python scripts/check_feature_test_controls.py` | Deliberate fault | Observed pytest result |
|---|---|---|
| `attempt1` | Load the preserved attempt-1 feature implementation from Git | 10 failed |
| `all_null_price` | Replace every price-derived column with null | 9 failed, 1 passed |
| `over_frozen` | Move rolling features back one additional delivery day | 10 failed |
| `all_null_a65` | Always return a null A65 daily mean | 3 failed |

Beyond those controls, the snapshot-wide raw oracle and SQL comparison cover
real dates outside the synthetic tests. The fresh detached Integration verdict
is a separate acceptance requirement; neither these results nor this report
certifies the Lead's own work or closes branch disposition/reclamation.

## Scope and retained assumptions

The A65 pre-gate existence and archive-vintage assumption and the A75 archive
revision caveat remain explicit in the README and leakage audit. No new feed,
catalog, model, threshold or paid service was introduced. A65 daily completeness
and price availability are enforced; those checks do not prove historical
pre-gate vintages. Attempt 1's original Integration verdict is retained with a
supersession notice and is not evidence of compliance with v6.8.
