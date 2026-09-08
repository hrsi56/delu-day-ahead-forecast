# Frozen CP-1 data snapshot

`snapshot.parquet` is the committed, UTC-indexed hourly snapshot pulled on
2026-09-08. It covers complete Europe/Berlin delivery days from 2019-01-01
through the latest source-complete cutoff used for this pull, 2026-09-06. Its
SHA-256 is recorded in `snapshot.sha256` and `source_manifest.json`.

Data: ENTSO-E Transparency Platform; Bundesnetzagentur | SMARD.de — CC BY 4.0.

## Ingestion route and mapping

The ENTSO-E External API was unavailable during the pull, so the v6.7 §3
fallback-primary route was used: the keyless SMARD `chart_data` API. The live
[SMARD market-data configuration](https://www.smard.de/app/chart_configuration/market_data_configuration.json)
is the mapping authority. The convenience filter table in the checkpoint brief
was checked rather than trusted: `4359` is realized residual load, `715` is
forecast other generation, and `4066` is biomass, so none is used here.

| Plan series | Snapshot field(s) | SMARD filter(s) | Treatment |
|---|---|---|---|
| A44 day-ahead price | `price_eur_mwh` | 4169 | Hourly product before 2025-10-01; mean of four quarter-hour prices afterward |
| A65/A01 load forecast | `load_forecast_mw` | 411 | Sum four quarter-hour MWh quantities to hourly MWh, numerically the hourly-average MW |
| A69 benchmark-only VRE forecast | three forecast components + `vre_forecast_mw` | 123, 3791, 125 | Sum quarters per component, then sum onshore + offshore + solar |
| A75 lagged actual VRE | three actual components + `vre_actual_mw` | 4067, 1225, 4068 | Sum quarters per component, then sum onshore + offshore + solar |

The `*_source_quarter_count` fields preserve the source-bin evidence. A source
hour with one to three non-null quarters fails closed to a null value; it is
never partially summed or averaged. The target has no nulls. The full details,
including all missing counts and first/last valid timestamps, are in
`source_manifest.json`.

## Completeness notes

- The SMARD A65 path has no head gap at 2019-01-01. The approximately 25-hour
  head gap in the plan is an ENTSO-E archive property and was not assumed on
  this route.
- There are 194 fully missing A65 hourly bins, three fully missing onshore/solar
  forecast bins, and one partial onshore/solar actual bin. They remain null and
  downstream catalogs use explicit completeness filtering on matched rows.
- A44 is continuous for all 67,343 hourly rows and has zero nulls. All 8,184
  price hours on or after 2025-10-01 are means of exactly four source quarters.
- The ENTSO-E API returned after the SMARD bulk pull. The sample in
  `reconciliation_sample.json` was committed before querying it; all 120 hours
  across pre-crisis, crisis, post-crisis, and both MTU-boundary sides agreed
  within €0.01/MWh (maximum absolute difference €0.00). The complete comparison
  and summary are committed beside the snapshot.

## Reproduction and audit

```bash
uv sync --locked --dev
uv run python scripts/audit_snapshot.py
uv run pytest -q
uv run python scripts/run_sql_artifact.py
```

The network pull itself is reproducible with `scripts/pull_smard_snapshot.py`;
rerunning it may capture later upstream revisions, so the committed Parquet and
its hash are the immutable reproduction input.
