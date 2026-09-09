# CP-1 data-leakage audit

The prediction origin is 12:00 CET on D-1 for delivery day D. Champion runtime
features are either known at that gate (KFT) or lagged observations (LAG). The
model feature matrix is enforced by `src/delu_forecast/schema.py`; delivery-day
A69, every A69 derivative, and same-day actual values are rejected.

For every row of D, every price-derived input must have a delivery date earlier
than D (§5.2, capstone_V6_8.md). A row-wise t−1 edge does not establish gate
availability for a whole-day curve and is retired. Calendar fields are derived
from UTC timestamps converted to Europe/Berlin, not from the number of observed
rows, so missing data cannot masquerade as a DST transition.

| Champion feature | Class | Latest consumed delivery date / justification |
|---|---|---|
| `local_hour`, `day_of_week`, `month`, `is_federal_holiday`, `is_day_after_holiday`, `is_bridge_day`, `day_type`, `dst_transition_day`, `summer_peak`, `winter_peak` | KFT | Deterministic calendar values; no price consumed |
| `crisis_period`, `post_crisis` | KFT | Static date indicators; no price consumed |
| `load_forecast_mw` | KFT by explicit assumption | A65/A01 for D; regulatory pre-gate deadline and archive-vintage assumption below |
| `load_forecast_day_mean_mw` | KFT by explicit assumption | A65/A01 for D; requires every expected UTC hour of the Berlin delivery day, 23/24/25, and propagates any null |
| `price_lag_24h` | LAG | D−1, same Berlin clock hour; unavailable or ambiguous source is null |
| `price_lag_48h` | LAG | D−2, same Berlin clock hour; unavailable or ambiguous source is null |
| `price_lag_168h` | LAG | D−7, same Berlin clock hour; unavailable or ambiguous source is null |
| `price_roll_mean_168h` | LAG | D−1; mean of the final 168 canonical hourly prices ending at the close of D−1 |
| `price_roll_std_168h` | LAG | D−1; sample standard deviation (ddof=1) on that same 168-hour window |
| `price_roll_mean_720h` | LAG | D−1; mean of the final 720 canonical hourly prices ending at the close of D−1 |
| `price_roll_std_720h` | LAG | D−1; sample standard deviation (ddof=1) on that same 720-hour window |
| `price_roll_q05_168h` | LAG | D−1; linearly interpolated 0.05 quantile on the same 168-hour window |
| `price_roll_q50_168h` | LAG | D−1; linearly interpolated 0.50 quantile on the same 168-hour window |
| `price_roll_q95_168h` | LAG | D−1; linearly interpolated 0.95 quantile on the same 168-hour window |
| `negative_price_count_168h` | LAG | D−1; count of prices strictly below zero on the same 168-hour window |
| `residual_load_proxy` (sole augmented addition) | LAG + KFT | No price consumed: A65 for D minus the A75 `vre_norm` over 42 complete delivery days D−43 through D−2 |

Every rolling statistic is computed once per D and broadcast unchanged to all
its rows. Missing history yields null, including at the snapshot head; neither
the observation count nor the D−1 boundary is relaxed. On a fall-back target
both repeated hours match the same unambiguous earlier source hour; if the
**source** hour is ambiguous, it remains null even if just one of the repeated
source rows is present. No adjacent-row fallback exists.

The DuckDB supplementary artifact joins D to D−1/D−2/D−7 on local hour using
an expected calendar grid to count source ambiguity. Its rolling query joins
each local-midnight D boundary to the preceding 168/720 UTC hours, enforces full
counts, and emits one result per delivery date. The offline acceptance audit
compares both Python and SQL to independently selected raw-price windows.

## Two disclosed assumptions

1. **A65 pre-gate assumption.** The regulatory deadline is the basis for KFT.
   Both the pre-gate existence of the vector and its equality to the archived
   vector are assumptions. The regulation also requires updates on significant
   changes, so the archive can contain a later revision. The data pulled after delivery
   are not presented as empirical proof of the exact 12:00 vector.
2. **A75 revision caveat.** The D-2 window uses the archive's current actual-
   generation values. A75 can be revised later, so those values may differ from
   what a live run would have seen. The two-day lag removes same-day leakage; it
   does not erase archive-revision risk.

## Strict A69 boundary

Delivery-day A69 wind/solar forecasts are post-gate. They and the A69-derived
`residual_load_fc` and `dunkelflaute_flag` are absent from both frozen champion
catalogs. `dunkelflaute_flag` may define a post-hoc evaluation stratum; A69 may
enter only the explicitly labelled §7.2 post-gate benchmark. The benchmark
schema differs from the selected champion schema only by the named A69 fields.

## Residual proxy boundary

For a target `(D, local hour h)`, `vre_norm` groups by Europe/Berlin clock hour
while preserving UTC row identity. It averages every A75 observation bearing
`h` over the 42 calendar delivery days D-43 through D-2. Therefore a window
crossing fall-back contains 43 observations for hour 02; one crossing spring-
forward contains 41. Repeated target-hour rows receive the same mean and no
spring-forward row is synthesized. Missing source data invalidates the affected
window rather than shrinking it silently.

## Embargo rationale

The embargo's only job is to break the autocorrelation adjacency between the
last training target and the first validation feature. A 168h-lagged feature of
a validation row reaches back into the training period, but using a known,
already-cleared historical price as an input feature is not leakage; it is what
production has at the 12:00 CET gate. One complete delivery day—including its
23/25-hour DST form—removes the true adjacency. The same one-day boundary is
applied between proper training and each development calibration slice, between
final training and final calibration, and between final calibration and the
holdout.
