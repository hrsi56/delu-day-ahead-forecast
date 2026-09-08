# CP-1 data-leakage audit

The prediction origin is 12:00 CET on D-1 for delivery day D. Champion runtime
features are either known at that gate (KFT) or lagged observations (LAG). The
model feature matrix is enforced by `src/delu_forecast/schema.py`; delivery-day
A69, every A69 derivative, and same-day actual values are rejected.

| Champion feature group | Class | Why it is available |
|---|---|---|
| Local hour, day of week, month, German federal holiday, day-after-holiday, bridge day, day type, DST-transition day, summer/winter flags | KFT | Deterministic calendar values known before the gate |
| `crisis_period`, `post_crisis` | KFT | Static date indicators; no outcome information is used |
| A65/A01 `load_forecast_mw` and delivery-day mean | KFT by explicit assumption | Regulation 543/2013 Art. 6(1)(b)/(2)(b) requires publication before the gate, but this snapshot does not empirically prove which archived vintage was present at 12:00 |
| `price_lag_24h`, `price_lag_48h`, `price_lag_168h` | LAG | Already-cleared prices addressed by fixed UTC offsets |
| 7/30-day price means/stds, 168h price quantiles, 7-day negative-hour count | LAG | Every rolling input is shifted first; its right edge is strictly t-1 (closed-left) |
| `residual_load_proxy` in the sole augmented candidate | LAG + KFT | Delivery-day A65 minus `vre_norm`; the latter uses only A75 actuals from 42 complete delivery days ending at the close of D-2 |

## Two disclosed assumptions

1. **A65 pre-gate assumption.** The regulatory deadline is the basis for KFT.
   The archive can contain a later revision, so the data pulled after delivery
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
