# Verdict — M1 / CP-1 — Integration — PASS

- Candidate SHA: `8adddcb62f38198fcffd7b258eaa5075435eecf2`
- Candidate tree: `283a934378e425dfe63155c9a2751acb9fe3afa8`
- Plan / version / bar: `capstone_V6_8.md`, v6.8, §12, **CP-1 (10 items)**. Supporting contract inspected: §4.0, §4.1, §4.2, §5.1–§5.2, §9.3–§9.4 and §9.6.
- Worktree: `/tmp/pjm-cp1-v68-review/critic-cp-1-8adddcb`, a fresh detached checkout supplied in the bounded assignment.
- Worktree clean before and after review: **yes**. Initial HEAD matched the full candidate SHA and `git status --porcelain=v1` was empty. Immediately before this verdict was written, HEAD/tree remained as above, branch identity was `HEAD`, and both status and diff-stat were empty.
- Review isolation: **cooperative**, not a read-only mount. No tracked candidate files, Git index, refs or worktrees were changed. The environment and caches are ignored byproducts. Spectral reproduction went to `/tmp/pjm-cp1-v68-review/critic-spectral`; this verdict is outside the candidate checkout.
- No network request was made. Every uv command used `UV_OFFLINE=true`, including dependency setup; installed locked runtime was CPython 3.13.15 with entsoe-py 0.8.0.
- No subordinate agents were used. No program state was read or written; no later checkpoint was reviewed or planned. Historical verdicts were not acceptance authority.
- The Owner's explicit no-deletion instruction overrides the normal protocol cleanup sentence: **the detached worktree remains intact**.

## Verbatim bar excerpt

The following is the exact ten-item excerpt verified in the candidate Git object and the worktree. It matches the assigned bar. The excerpt is the citation; line numbers are non-binding.

**CP-1 (10 items)**
- [ ] Required snapshot contains **A44, A65/A01, benchmark-only A69, and A75 aggregate VRE** from 2019-01-01 through the pull date, with the ~25h A65/A01 head gap handled (trim or documented head NaNs) and the snapshot hash recorded. **The successful pull is archive-reachability and snapshot-completeness evidence, not pre-gate availability evidence** — there is no separate feed-existence or archive-depth probe.
- [ ] UTC indexing, Berlin 23/25-local-hour identity, PT15M→hour aggregation, chunk stitching with complete bins, missing-quarter fail-closed behavior, and the 2025-10-01 price transition are correct; no nulls in the DA price.
- [ ] The frozen `base` catalog is implemented with calendar/regime features, the A65 load forecast, **calendar-day-matched price lags and D-1-frozen rolling price statistics (§4.0, §4.1)**; the frozen augmented candidate adds **only** the 42-day, D-2-bounded `residual_load_proxy` (§4.1). **A69 and same-day actual columns are rejected by champion inference**, and **every price-derived champion feature satisfies the §5.2 delivery-day availability invariant** — no feature for delivery day `D` consumes a price whose delivery date is `D` or later. **The §9.6 DuckDB artifact expresses the same calendar-day lag and D-1-frozen rolling semantics, including the unavailable/ambiguous-source rule and the exact window lengths. Compliance is determined by those semantics, regardless of whether the SQL uses joins or window functions.**
- [ ] **The five tail partitions are pinned without overlap** (§5.1): Fold 5, Embargo A, the 60-day final-calibration slice, Embargo B, and the final 90-day holdout. `min(fold_5.delivery_date) >= 2025-10-01` is asserted directly rather than derived from a pull date. Calibration and holdout rows are excluded from **every component of every development fold — train, calibration and eval separately — and from every diagnostic window**; holdout outcomes are excluded from every fit and threshold. Each fold's §6.2 calibration slice carries its own one-day embargo, and **every embargo contains exactly one complete delivery day**. The partition and exclusion rules are asserted by a committed test **that asserts each of these rules explicitly rather than implying it** (§9.4 item 8).
- [ ] **ENTSO-E↔SMARD reconciliation** on a fixed stratified sample covering pre-crisis, crisis, post-crisis and the PT15M transition: DA prices agree within €0.01/MWh (both Reg-543 sourced — disagreement indicates an ingestion bug, not a market fact). The whole archive is not re-compared merely because it is available. *(96/96 sample hours already agreed at the 2026-06-12 spike.)*
- [ ] **All nine** targeted repository tests pass (§9.4): chunk stitching, a missing quarter, fall-back DST identity, **day-level delivery-day leakage and the 24h/48h/168h calendar-day lags across 23- and 25-hour days**, transition aggregation **including inclusive-right-endpoint normalization, half-open Berlin slicing and the 92/96/100 quarter counts**, the champion/benchmark schema firewall, the spectral FFT-bin assertion, the residual proxy's 42-day/D-2 boundary plus its DST behaviour on both sides, **the completed partition assertions**, and **A65 daily completeness failing closed**. **A test that passes without exercising its invariant does not satisfy this item.**
- [ ] Data leakage audit records every champion feature as KFT or LAG with justification **against the §5.2 delivery-day availability invariant, naming for each price-derived feature the latest delivery date it can consume**; states the **A65 pre-gate assumption** and the **A75-revision caveat** honestly as assumptions; and confines A69 to the §7.2 benchmark and the §8.3 evaluation stratum. **No feature may be described as gate-available on the strength of a row-wise `t−1` boundary.**
- [ ] Committed snapshot/data folder and README carry the **CC BY 4.0 attribution statement** (ENTSO-E Transparency Platform; Bundesnetzagentur | SMARD.de) and the data cutoff.
- [ ] Three spectral figures and one 3–4 sentence interpretation paragraph are committed (§4.2).
- [ ] **One fresh Integration Critic returns `PASS`** on the final candidate from a clean detached checkout, with a verdict-only delta to the evidence tip.

## Evidence actually inspected

The controlling excerpt and supporting sections above, `AGENTS.md`, the Integration Critic protocol in `engineering-role.md`, and `docs/track-b/gauntlet-templates.md` §2 were inspected directly. The source review covered every module in `src/delu_forecast/`, all nine property-family test files plus `tests/conftest.py`, `sql/feature_queries.sql`, all seven assigned audit/ingestion/reconciliation/spectral/control scripts, `Makefile`, `pyproject.toml`, and `.github/workflows/tests.yml`. The committed `uv.lock` was exercised through a successful locked offline sync.

Raw committed inputs inspected and recomputed were `data/snapshot.parquet`, its SHA-256, `data/source_manifest.json`, `data/partitions.json`, the frozen `data/reconciliation_sample.json`, `data/reconciliation.csv` and `data/reconciliation_summary.json`. Documentation inspection covered `README.md`, `data/README.md`, `docs/data-leakage-audit.md`, `reports/README.md`, and `reports/cp1-v68-availability.md`. The last report's claims were rerun rather than accepted as certification.

All three original PNG figures were opened visually: labels, axes, the three regime curves and daily/weekly ACF references are readable and support the four-sentence interpretation in the root README. Each original PNG and `reports/spectral_peak_bins.csv` then matched fresh output byte-for-byte.

### Independent numerical observations

- Snapshot SHA-256: `7dd2dc73407706ca6bd3c1ad51d201ac0de35eec5ca129ce320cca639f697f00`. There are **67,343 continuous UTC hours**, delivery 2019-01-01 through 2026-09-06, and **zero null prices**. The pull is dated 2026-09-08; documentation identifies 2026-09-06 as the latest source-complete delivery cutoff, rather than implying that the archive pull demonstrates pre-gate availability.
- The 2,806 delivery days contain 8 × 23, 2,791 × 24 and 7 × 25 hours. The documented SMARD fallback route contains all required series; the A65 head gap is zero on that route, while 194 later missing A65 hours are retained and disclosed. Coverage metadata and aggregate VRE sums were independently recomputed from Parquet.
- Every one of the **11 price-derived columns** on all 67,343 rows matched independently selected raw lag sources and raw pre-D rolling windows. Exact lag null counts are **39 / 63 / 183** for D−1 / D−2 / D−7. Eight rolling columns are constant per delivery day and use exactly 168 or 720 canonical hours, with missing history null. SQL lag values agree exactly; maximum SQL rolling error is **6.821210263296962e-13**, below absolute 1e-9 / relative 1e-12.
- A separate Critic calculation enumerated raw A75 windows bounded by Berlin midnights D−43 and D−1 exclusive, required every expected hourly observation, and directly averaged each local clock hour. It agrees for all 67,343 rows; **65,303 norms are valid**, and the maximum numerical norm difference is **2.1827872842550278e-11** (inside absolute 1e-9 / relative 1e-12). The residual subtraction agrees too.
- A separate Critic SQL fault check removed one of the two fall-back source-hour rows. All D−1/D−2/D−7 matches remain null for the calendar-ambiguous hour; all eight rolling values fail closed when that missing hour is in the window. Replacing all target-day prices left SQL lag/rolling values unchanged on an ordinary 24-hour day, a 23-hour spring day and a 25-hour fall day.
- Independent reconciliation arithmetic verified all 120 sample timestamps and strata against the five frozen days; stored SMARD prices match the raw Parquet to **2.842170943040401e-14**, and all stored ENTSO-E↔SMARD differences recompute to **0.0**. An initial Critic assertion demanded exact binary equality across CSV serialization and failed on three values at that tiny scale; rerunning with the script's six-decimal CSV precision (absolute 0.0000005) passes. This is a Critic-oracle precision correction, not a candidate repair or a relaxation of the governing €0.01 tolerance.
- Commit order confirms partition recording precedes the spectral artifact commit, and the frozen sample commit precedes the reconciliation-result commit. There was no archive-wide network comparison.
- A65 daily means are null on the ten incomplete real days, including 2023-10-29 and 2024-10-27 with only 24 of 25 hours. Complete 23/24/25-hour positive fixtures equal direct means before every possible single-hour absence or null is tested.

### Spectral reproduction hashes

| Artifact | SHA-256, identical original and reproduction |
|---|---|
| `fig_welch_periodogram.png` | `4e09646b47c42676b0ba5c509112d52ec55a5ec134e596b3bf743fd1f945eb93` |
| `fig_per_regime_periodogram.png` | `010b0b9c0050d4ea5f6a296d1237a31b4ce981126cad33e8c1f9fae6d7a205d1` |
| `fig_acf_24_168.png` | `232140c2fa3527952c3e5bce87484cdcc6ddf6a17d73d6530f051ba8a3825253` |
| `spectral_peak_bins.csv` | `11d9470f4daaf9de44665cc16a7d187284e5ffbb66b736ec230e84eb1f8e8bf5` |

## Checklist verdict

| # | Checklist item | Verdict | Direct evidence |
|---|---|---|---|
| 1 | Required frozen snapshot, source coverage, head-gap treatment and hash | **PASS** | Committed Parquet and manifest contain A44, A65/A01, benchmark A69 and aggregate A75. Independent coverage and aggregate sums agree. The complete-day cutoff is disclosed; no A65 head gap exists on the documented fallback route. The pinned snapshot hash reproduces. Archive completeness is not presented as historical gate-vintage proof. |
| 2 | UTC/DST identity, PT15M aggregation, stitching, missing-quarter behavior, transition, no price nulls | **PASS** | Full snapshot continuity/local identity audit; all 2,806 complete delivery-day counts; production source mappings and aggregation code; chunk-overlap and missing-quarter fixture; transition fixture; actual ENTSO-E normalizer tested at inclusive endpoints with 92/96/100 quarters and half-open Berlin slicing. Feature-feed SMARD energy quarters are correctly summed to hourly-average MW; quarter-hour prices are averaged. No custom A03 parser replaces the pinned client. |
| 3 | Exact two catalogs, delivery-day price availability, A75 proxy and SQL semantics | **PASS** | Catalogs are 25 and 26 columns with only residual_load_proxy added. Full raw price oracles, independent raw A75 oracle, direct schema-firewall inspection/tests and independent SQL damaged-source/target-day mutations pass. Calendar lags use D−1/D−2/D−7; eight rolling values use the exact 168/720-hour windows ending at D−1 and are broadcast per D. The CP-1 runtime-schema validators reject A69 derivatives/same-day actuals and admit the authorized D−2 historical input boundary. |
| 4 | Five pinned tail partitions and explicit exclusions/complete-day embargoes | **PASS** | Fold 5 is 2026-01-08–2026-04-07; Embargo A 2026-04-08; final calibration 2026-04-09–2026-06-07; Embargo B 2026-06-08; holdout 2026-06-09–2026-09-06. The committed test asserts 90/1/60/1/90 lengths, disjointness, contiguity and the post-transition minimum directly; then final calibration and holdout against train/calibration/eval separately for each fold, against every diagnostic and EDA date range, and each embargo as exactly one delivery date with its complete expected UTC grid. The inspected CP-1 paths perform no model fitting or threshold estimation; target-use windows exclude the holdout explicitly. |
| 5 | Fixed stratified ENTSO-E↔SMARD reconciliation | **PASS** | Five pre-pinned days cover pre-crisis, crisis peak, post-crisis, 2025-09-30 and 2025-10-01. All 120 unique sampled hours, dates, strata and arithmetic independently verified; all cross-source differences are 0.0 within €0.01. Sample hash and committed ordering agree. No new source query was needed. |
| 6 | All nine non-vacuous targeted test families | **PASS** | 25 passed in 27.47s. Assertion review confirms negative/zero-crossing monotonicity, whole-day mutation sweeps and direct lag/rolling oracles, DST identity, chunk/missing-quarter and transition normalization, runtime schemas, exact proxy boundaries/DST counts, FFT bins, explicit partitions and A65 complete-day controls. Deliberate attempt1 / all_null_price / over_frozen / all_null_a65 faults respectively produce 10 / 9 / 10 / 3 failed test cases with pytest exit 1 and no collection/setup errors; wrappers exit 0. The thin workflow runs the properties on every push. |
| 7 | Complete leakage audit and honest A65/A75 assumptions | **PASS** | All 26 possible champion columns appear in the KFT/LAG table. Each price lag names its actual source delivery date; every rolling column names D−1 and its exact window/definition. A65 pre-gate existence and archive vintage are explicit assumptions; A75 revision is disclosed separately. A69 is confined to the benchmark/evaluation stratum. Row-wise t−1 is explicitly rejected as whole-day availability evidence. |
| 8 | Attribution and data cutoff in README and data folder | **PASS** | Root README, data README and manifest carry “Data: ENTSO-E Transparency Platform; Bundesnetzagentur \| SMARD.de — CC BY 4.0.” They disclose the snapshot cutoff 2026-09-06 and data README/manifest separately record the pull date. |
| 9 | Three committed spectral figures and 3–4 sentence interpretation | **PASS** | All three original figures visually inspected and reproduced byte-for-byte, along with FFT-bin CSV. Root README has four interpretation sentences linking daily/weekly/half-day price structure to calendar features and regime changes to evaluation, without claiming proxy validation. The generator uses 63,695 EDA-eligible price hours through 2026-04-07, excluding final calibration/holdout. |
| 10 | One fresh Integration PASS at final candidate; verdict-only evidence delta | **PASS — current review** | This is the fresh independent PASS binding the full candidate SHA from a clean detached checkout. **Post-review evidence-commit verification is reserved for the Lead:** after recording this verdict, report evidence_tip_sha and verify `git diff --name-only 8adddcb62f38198fcffd7b258eaa5075435eecf2..<evidence_tip_sha>` contains only `docs/track-b/evidence/cp-1/` paths. That future delta is not claimed verified here; any non-verdict change invalidates this PASS. |

The substantive CP-1 requirements pass at this candidate. No material acceptance gap was found. The disclosed A65 and A75 vintage assumptions remain assumptions. This verdict authorizes no publication, mainline change, disposition or worktree deletion.

Interview-answer capture trigger: the review independently demonstrates why whole-day numerical oracles and positive controls are necessary alongside mutation invariance; the prior row-wise construction and always-null/over-frozen alternatives are now rejected. No interview document was filed by this bounded Critic.

## Commands actually run

All shell commands below ran in `/tmp/pjm-cp1-v68-review/critic-cp-1-8adddcb`. Exit codes are actual process exits. Async sessions were polled to completion; polling did not rerun commands. The three local-image tool calls listed after the shell ledger were read-only visual inspections.

### Command 1 — exit 0

```bash
git rev-parse HEAD && git status --porcelain=v1
```

Observed:

```text
Candidate SHA 8adddcb62f38198fcffd7b258eaa5075435eecf2; status empty.
```

### Command 2 — exit 0

```bash
cat AGENTS.md
```

Observed:

```text
Inspected the exact named files/sections. Findings and evidence are recorded above.
```

### Command 3 — exit 0

```bash
rg -n '^#|Integration Critic|CP-1|§9.4|§9.6' engineering-role.md docs/track-b/gauntlet-templates.md capstone_V6_8.md
```

Observed:

```text
Inspected the exact named files/sections. Findings and evidence are recorded above.
```

### Command 4 — exit 0

```bash
sed -n '34,150p' engineering-role.md
```

Observed:

```text
Inspected the exact named files/sections. Findings and evidence are recorded above.
```

### Command 5 — exit 0

```bash
sed -n '68,125p' docs/track-b/gauntlet-templates.md
```

Observed:

```text
Inspected the exact named files/sections. Findings and evidence are recorded above.
```

### Command 6 — exit 0

```bash
sed -n '91,217p' capstone_V6_8.md
```

Observed:

```text
Inspected the exact named files/sections. Findings and evidence are recorded above.
```

### Command 7 — exit 0

```bash
sed -n '356,398p' capstone_V6_8.md; sed -n '450,463p' capstone_V6_8.md
```

Observed:

```text
Inspected the exact named files/sections. Findings and evidence are recorded above.
```

### Command 8 — exit 0

```bash
rg --files src/delu_forecast tests data reports; cat pyproject.toml Makefile .github/workflows/tests.yml
```

Observed:

```text
Inspected the exact named files/sections. Findings and evidence are recorded above.
```

### Command 9 — exit 0

```bash
sed -n '105,217p' capstone_V6_8.md
```

Observed:

```text
Inspected the exact named files/sections. Findings and evidence are recorded above.
```

### Command 10 — exit 0

```bash
UV_OFFLINE=true uv sync --locked --dev
```

Observed:

```text
Using CPython 3.13.15
Creating virtual environment at: .venv
Resolved 34 packages in 21ms
   Building delu-price-forecast @ file:///private/tmp/pjm-cp1-v68-review/critic-cp-1-8adddcb
      Built delu-price-forecast @ file:///private/tmp/pjm-cp1-v68-review/critic-cp-1-8adddcb
Prepared 1 package in 286ms
Installed 31 packages in 209ms
 + beautifulsoup4==4.15.0
 + certifi==2026.5.20
 + charset-normalizer==3.4.7
 + contourpy==1.3.3
 + cycler==0.12.1
 + delu-price-forecast==0.1.0 (from file:///private/tmp/pjm-cp1-v68-review/critic-cp-1-8adddcb)
 + duckdb==1.5.5
 + entsoe-py==0.8.0
 + fonttools==4.64.0
 + holidays==0.104
 + idna==3.18
 + iniconfig==2.3.0
 + kiwisolver==1.5.1
 + matplotlib==3.11.1
 + numpy==2.4.6
 + packaging==26.2
 + pandas==3.0.3
 + pillow==12.3.0
 + pluggy==1.6.0
 + pyarrow==25.0.1
 + pygments==2.20.0
 + pyparsing==3.3.2
 + pytest==9.1.1
 + python-dateutil==2.9.0.post0
 + pytz==2026.2
 + requests==2.34.2
 + scipy==1.18.1
 + six==1.17.0
 + soupsieve==2.8.4
 + typing-extensions==4.15.0
 + urllib3==2.7.0
```

### Command 11 — exit 0

```bash
cat src/delu_forecast/features.py
```

Observed:

```text
Inspected the exact named files/sections. Findings and evidence are recorded above.
```

### Command 12 — exit 0

```bash
cat src/delu_forecast/ingest.py
```

Observed:

```text
Inspected the exact named files/sections. Findings and evidence are recorded above.
```

### Command 13 — exit 0

```bash
cat scripts/audit_snapshot.py scripts/audit_delivery_day_features.py
```

Observed:

```text
Inspected the exact named files/sections. Findings and evidence are recorded above.
```

### Command 14 — exit 0

```bash
cat scripts/run_sql_artifact.py scripts/generate_spectral_artifacts.py scripts/check_feature_test_controls.py
```

Observed:

```text
Inspected the exact named files/sections. Findings and evidence are recorded above.
```

### Command 15 — exit 0

```bash
UV_OFFLINE=true uv run --frozen pytest -q
```

Observed:

```text
.........................                                                [100%]
25 passed in 27.47s
```

### Command 16 — exit 0

```bash
UV_OFFLINE=true uv run --frozen python scripts/audit_snapshot.py
```

Observed:

```text
{
  "a65_head_gap_observed_hours": 0,
  "augmented_columns": 26,
  "augmented_complete_rows": 65016,
  "base_columns": 25,
  "base_complete_rows": 66336,
  "delivery_date_cutoff": "2026-09-06",
  "delivery_date_start": "2019-01-01",
  "fold_5_start": "2026-01-08",
  "local_day_row_counts": {
    "23": 8,
    "24": 2791,
    "25": 7
  },
  "price_nulls": 0,
  "reconciliation_status": "pass",
  "rows": 67343,
  "snapshot_sha256": "7dd2dc73407706ca6bd3c1ad51d201ac0de35eec5ca129ce320cca639f697f00",
  "utc_end": "2026-09-06T21:00:00+00:00",
  "utc_start": "2018-12-31T23:00:00+00:00"
}
```

### Command 17 — exit 0

```bash
UV_OFFLINE=true uv run --frozen python scripts/audit_delivery_day_features.py
```

Observed:

```text
{
  "raw_rows_checked": 67343,
  "delivery_days_checked": 2806,
  "price_columns_checked": 11,
  "same_day_price_sources_in_repaired_features": 0,
  "null_calendar_lags": {
    "price_lag_24h": 39,
    "price_lag_48h": 63,
    "price_lag_168h": 183
  },
  "sql_rolling_delivery_days": 2806,
  "sql_max_absolute_error_vs_raw_oracle": 6.821210263296962e-13,
  "null_a65_daily_statistics": [
    {
      "delivery_date": "2022-02-22",
      "expected_hours": 24,
      "available_hours": 0
    },
    {
      "delivery_date": "2022-03-24",
      "expected_hours": 24,
      "available_hours": 0
    },
    {
      "delivery_date": "2022-07-20",
      "expected_hours": 24,
      "available_hours": 0
    },
    {
      "delivery_date": "2022-07-21",
      "expected_hours": 24,
      "available_hours": 0
    },
    {
      "delivery_date": "2022-12-21",
      "expected_hours": 24,
      "available_hours": 0
    },
    {
      "delivery_date": "2022-12-22",
      "expected_hours": 24,
      "available_hours": 0
    },
    {
      "delivery_date": "2023-03-13",
      "expected_hours": 24,
      "available_hours": 0
    },
    {
      "delivery_date": "2023-08-31",
      "expected_hours": 24,
      "available_hours": 0
    },
    {
      "delivery_date": "2023-10-29",
      "expected_hours": 25,
      "available_hours": 24
    },
    {
      "delivery_date": "2024-10-27",
      "expected_hours": 25,
      "available_hours": 24
    }
  ],
  "retired_rowwise_rolling_exposed_rows": 64537,
  "retired_utc_24h_lag_same_day_rows": 7
}
```

### Command 18 — exit 0

```bash
UV_OFFLINE=true uv run --frozen python scripts/run_sql_artifact.py
```

Observed:

```text
data_quality_checks
 null_price_rows  duplicate_utc_rows
               0                   0
source_bin_checks
 bad_load_bins  bad_a69_bins  bad_a75_bins  bad_post_transition_price_bins
             0             0             0                               0
feature_views
 lag_rows  rolling_delivery_days
    67343                   2806
```

### Command 19 — exit 0

```bash
cat tests/test_02_rolling_closed_left.py tests/test_09_a65_daily_completeness.py
```

Observed:

```text
Inspected the exact named files/sections. Findings and evidence are recorded above.
```

### Command 20 — exit 0

```bash
cat tests/test_08_partition_integrity.py src/delu_forecast/partitions.py
```

Observed:

```text
Inspected the exact named files/sections. Findings and evidence are recorded above.
```

### Command 21 — exit 0

```bash
cat tests/test_01_monotonicity.py tests/test_03_utc_dst_lags.py tests/test_04_quarterhour_integrity.py tests/conftest.py
```

Observed:

```text
Inspected the exact named files/sections. Findings and evidence are recorded above.
```

### Command 22 — exit 0

```bash
cat tests/test_05_schema_firewall.py tests/test_06_residual_proxy.py tests/test_07_spectral_labels.py src/delu_forecast/schema.py src/delu_forecast/spectral.py src/delu_forecast/postprocess.py
```

Observed:

```text
Inspected the exact named files/sections. Findings and evidence are recorded above.
```

### Command 23 — exit 0

```bash
cat sql/feature_queries.sql
```

Observed:

```text
Inspected the exact named files/sections. Findings and evidence are recorded above.
```

### Command 24 — exit 0

```bash
cat README.md docs/data-leakage-audit.md data/README.md reports/README.md reports/cp1-v68-availability.md
```

Observed:

```text
Inspected the exact named files/sections. Findings and evidence are recorded above.
```

### Command 25 — exit 0

```bash
cat data/partitions.json data/reconciliation_sample.json data/reconciliation_summary.json data/source_manifest.json
```

Observed:

```text
Inspected the exact named files/sections. Findings and evidence are recorded above.
```

### Command 26 — exit 0

```bash
cat scripts/reconcile_entsoe_smard.py scripts/pull_smard_snapshot.py
```

Observed:

```text
Inspected the exact named files/sections. Findings and evidence are recorded above.
```

### Command 27 — exit 0

```bash
UV_OFFLINE=true uv run --frozen python scripts/generate_spectral_artifacts.py --output-dir /tmp/pjm-cp1-v68-review/critic-spectral
```

Observed:

```text
Generated spectral artifacts from 63,695 EDA-eligible hourly rows through 2026-04-07
```

### Command 28 — exit 0

```bash
UV_OFFLINE=true uv run --frozen python scripts/check_feature_test_controls.py attempt1
```

Observed:

```text
attempt1 pytest_exit= 1
FFFFFFFFFF                                                               [100%]
=========================== short test summary info ============================
FAILED tests/test_02_rolling_closed_left.py::test_whole_delivery_day_price_mutation_sweep_and_positive_control[target0]
FAILED tests/test_02_rolling_closed_left.py::test_whole_delivery_day_price_mutation_sweep_and_positive_control[target1]
FAILED tests/test_02_rolling_closed_left.py::test_whole_delivery_day_price_mutation_sweep_and_positive_control[target2]
FAILED tests/test_02_rolling_closed_left.py::test_lag_source_day_itself_is_dst_and_fails_closed[1-source_day0]
FAILED tests/test_02_rolling_closed_left.py::test_lag_source_day_itself_is_dst_and_fails_closed[1-source_day1]
FAILED tests/test_02_rolling_closed_left.py::test_lag_source_day_itself_is_dst_and_fails_closed[2-source_day0]
FAILED tests/test_02_rolling_closed_left.py::test_lag_source_day_itself_is_dst_and_fails_closed[2-source_day1]
FAILED tests/test_02_rolling_closed_left.py::test_lag_source_day_itself_is_dst_and_fails_closed[7-source_day0]
FAILED tests/test_02_rolling_closed_left.py::test_lag_source_day_itself_is_dst_and_fails_closed[7-source_day1]
FAILED tests/test_02_rolling_closed_left.py::test_missing_price_hour_cannot_shrink_or_extend_a_rolling_window
10 failed in 0.32s
```

### Command 29 — exit 0

```bash
UV_OFFLINE=true uv run --frozen python scripts/check_feature_test_controls.py all_null_price
```

Observed:

```text
all_null_price pytest_exit= 1
FFFFFFFFF.                                                               [100%]
=========================== short test summary info ============================
FAILED tests/test_02_rolling_closed_left.py::test_whole_delivery_day_price_mutation_sweep_and_positive_control[target0]
FAILED tests/test_02_rolling_closed_left.py::test_whole_delivery_day_price_mutation_sweep_and_positive_control[target1]
FAILED tests/test_02_rolling_closed_left.py::test_whole_delivery_day_price_mutation_sweep_and_positive_control[target2]
FAILED tests/test_02_rolling_closed_left.py::test_lag_source_day_itself_is_dst_and_fails_closed[1-source_day0]
FAILED tests/test_02_rolling_closed_left.py::test_lag_source_day_itself_is_dst_and_fails_closed[1-source_day1]
FAILED tests/test_02_rolling_closed_left.py::test_lag_source_day_itself_is_dst_and_fails_closed[2-source_day0]
FAILED tests/test_02_rolling_closed_left.py::test_lag_source_day_itself_is_dst_and_fails_closed[2-source_day1]
FAILED tests/test_02_rolling_closed_left.py::test_lag_source_day_itself_is_dst_and_fails_closed[7-source_day0]
FAILED tests/test_02_rolling_closed_left.py::test_lag_source_day_itself_is_dst_and_fails_closed[7-source_day1]
9 failed, 1 passed in 0.51s
```

### Command 30 — exit 0

```bash
UV_OFFLINE=true uv run --frozen python scripts/check_feature_test_controls.py over_frozen
```

Observed:

```text
over_frozen pytest_exit= 1
FFFFFFFFFF                                                               [100%]
=========================== short test summary info ============================
FAILED tests/test_02_rolling_closed_left.py::test_whole_delivery_day_price_mutation_sweep_and_positive_control[target0]
FAILED tests/test_02_rolling_closed_left.py::test_whole_delivery_day_price_mutation_sweep_and_positive_control[target1]
FAILED tests/test_02_rolling_closed_left.py::test_whole_delivery_day_price_mutation_sweep_and_positive_control[target2]
FAILED tests/test_02_rolling_closed_left.py::test_lag_source_day_itself_is_dst_and_fails_closed[1-source_day0]
FAILED tests/test_02_rolling_closed_left.py::test_lag_source_day_itself_is_dst_and_fails_closed[1-source_day1]
FAILED tests/test_02_rolling_closed_left.py::test_lag_source_day_itself_is_dst_and_fails_closed[2-source_day0]
FAILED tests/test_02_rolling_closed_left.py::test_lag_source_day_itself_is_dst_and_fails_closed[2-source_day1]
FAILED tests/test_02_rolling_closed_left.py::test_lag_source_day_itself_is_dst_and_fails_closed[7-source_day0]
FAILED tests/test_02_rolling_closed_left.py::test_lag_source_day_itself_is_dst_and_fails_closed[7-source_day1]
FAILED tests/test_02_rolling_closed_left.py::test_missing_price_hour_cannot_shrink_or_extend_a_rolling_window
10 failed in 0.51s
```

### Command 31 — exit 0

```bash
UV_OFFLINE=true uv run --frozen python scripts/check_feature_test_controls.py all_null_a65
```

Observed:

```text
all_null_a65 pytest_exit= 1
FFF                                                                      [100%]
=========================== short test summary info ============================
FAILED tests/test_09_a65_daily_completeness.py::test_a65_daily_statistic_requires_every_expected_hour[day0-23]
FAILED tests/test_09_a65_daily_completeness.py::test_a65_daily_statistic_requires_every_expected_hour[day1-24]
FAILED tests/test_09_a65_daily_completeness.py::test_a65_daily_statistic_requires_every_expected_hour[day2-25]
3 failed in 0.09s
```

### Command 32 — exit 0

```bash
sed -n '99,106p' capstone_V6_8.md; sed -n '188,260p' src/delu_forecast/ingest.py
```

Observed:

```text
Inspected the exact named files/sections. Findings and evidence are recorded above.
```

### Command 33 — exit 0

```bash
git log --format='%H %aI %s' -- data/partitions.json data/reconciliation_sample.json data/reconciliation.csv reports/fig_welch_periodogram.png; git rev-parse 'HEAD^{tree}'; git ls-files data reports uv.lock
```

Observed:

```text
368822de297e71f24fd08569815cae0289e65b96 2026-09-08T20:52:46+03:00 Record CP-1 cross-source reconciliation
cd9b6dd6b20b5a91381c07098db005b419989880 2026-09-08T20:49:00+03:00 Pin CP-1 reconciliation sample
e18d1e103d617d450521134df5be899ad671ee01 2026-09-08T20:45:58+03:00 Add CP-1 spectral diagnostics
6a52118f8b96f1222ee821be9fa9fd2bc400c383 2026-09-08T20:43:57+03:00 Build CP-1 data and fixed-feature layer
283a934378e425dfe63155c9a2751acb9fe3afa8
data/README.md
data/partitions.json
data/reconciliation.csv
data/reconciliation_sample.json
data/reconciliation_summary.json
data/snapshot.parquet
data/snapshot.sha256
data/source_manifest.json
reports/README.md
reports/cp1-v68-availability.md
reports/fig_acf_24_168.png
reports/fig_per_regime_periodogram.png
reports/fig_welch_periodogram.png
reports/spectral_peak_bins.csv
uv.lock
```

### Command 34 — exit 1

```bash
UV_OFFLINE=true uv run --frozen python - <<'PY'
from pathlib import Path
import hashlib, json
from datetime import date, timedelta
import numpy as np
import pandas as pd
from delu_forecast.features import residual_proxy_details
r=Path.cwd()
raw=pd.read_parquet(r/'data/snapshot.parquet')
times=pd.DatetimeIndex(raw.timestamp_utc)
local=times.tz_convert('Europe/Berlin')
meta=json.loads((r/'data/source_manifest.json').read_text())
for col, coverage in meta['coverage'].items():
    v=raw[col]
    assert int(v.notna().sum()) == coverage['non_null_rows']
    assert int(v.isna().sum()) == coverage['null_rows']
    assert times[v.notna()][0].isoformat() == coverage['first_valid_utc']
    assert times[v.notna()][-1].isoformat() == coverage['last_valid_utc']
for typ in ('actual','forecast'):
    columns=[f'{component}_{typ}_mw' for component in ('wind_onshore','wind_offshore','solar')]
    np.testing.assert_allclose(raw[f'vre_{typ}_mw'], raw[columns].to_numpy().sum(axis=1), rtol=0, atol=0, equal_nan=True)
comparison=pd.read_csv(r/'data/reconciliation.csv')
comparison['timestamp_utc']=pd.to_datetime(comparison.timestamp_utc,utc=True)
assert comparison.timestamp_utc.is_unique
sample=json.loads((r/'data/reconciliation_sample.json').read_text())
for item in sample['delivery_days']:
    day=date.fromisoformat(item['delivery_date'])
    start=pd.Timestamp(day,tz='Europe/Berlin').tz_convert('UTC')
    end=pd.Timestamp(day+timedelta(days=1),tz='Europe/Berlin').tz_convert('UTC')
    part=comparison.loc[comparison.delivery_date.eq(day.isoformat())]
    expected=pd.date_range(start,end,freq='h',inclusive='left')
    assert pd.DatetimeIndex(part.timestamp_utc).as_unit('ns').equals(expected.as_unit('ns'))
    assert part.stratum.eq(item['stratum']).all()
np.testing.assert_allclose(comparison.smard_eur_mwh, raw.set_index('timestamp_utc').loc[comparison.timestamp_utc,'price_eur_mwh'],atol=0,rtol=0)
diffs=abs(comparison.entsoe_eur_mwh-comparison.smard_eur_mwh)
np.testing.assert_allclose(diffs,comparison.abs_diff_eur_mwh,atol=0,rtol=0)
assert diffs.le(sample['tolerance_eur_mwh']).all()
print('Independent reconciliation: 120/120 exact timestamps, strata, stored SMARD values and difference arithmetic; max difference',diffs.max())
actual=residual_proxy_details(raw)
vre=raw.vre_actual_mw.to_numpy()
hours=local.hour.to_numpy()
expected_norm=np.full(len(raw),np.nan)
counts=np.zeros(len(raw),dtype=int)
for day in sorted(set(local.date)):
    start=pd.Timestamp(day-timedelta(days=43),tz='Europe/Berlin').tz_convert('UTC')
    end=pd.Timestamp(day-timedelta(days=1),tz='Europe/Berlin').tz_convert('UTC')
    first=int(times.searchsorted(start)); last=int(times.searchsorted(end))
    expected_size=int((end-start).total_seconds()/3600)
    valid=last-first==expected_size and np.isfinite(vre[first:last]).all()
    target=np.flatnonzero(local.date==day)
    for hour in set(hours[target]):
        observed=vre[first:last][hours[first:last]==hour]
        rows=target[hours[target]==hour]
        if valid: expected_norm[rows]=observed.mean()
        counts[rows]=len(observed)
np.testing.assert_allclose(actual.vre_norm,expected_norm,atol=1e-9,rtol=1e-12,equal_nan=True)
np.testing.assert_allclose(actual.residual_load_proxy,raw.load_forecast_mw.to_numpy()-expected_norm,atol=1e-9,rtol=1e-12,equal_nan=True)
print('Independent A75 oracle:',len(raw),'rows; valid norms',int(np.isfinite(expected_norm).sum()),'; max error',float(np.nanmax(abs(expected_norm-actual.vre_norm))))
for name in ('fig_welch_periodogram.png','fig_per_regime_periodogram.png','fig_acf_24_168.png','spectral_peak_bins.csv'):
    a=(r/'reports'/name).read_bytes(); b=(Path('/tmp/pjm-cp1-v68-review/critic-spectral')/name).read_bytes()
    assert a==b
    print('Byte-identical',name,hashlib.sha256(a).hexdigest())
PY
```

Observed:

```text
Traceback (most recent call last):
  File "<stdin>", line 33, in <module>
  File "/private/tmp/pjm-cp1-v68-review/critic-cp-1-8adddcb/.venv/lib/python3.13/site-packages/numpy/testing/_private/utils.py", line 1768, in assert_allclose
    assert_array_compare(compare, actual, desired, err_msg=str(err_msg),
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                         verbose=verbose, header=header, equal_nan=equal_nan,
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                         strict=strict)
                         ^^^^^^^^^^^^^^
  File "/private/tmp/pjm-cp1-v68-review/critic-cp-1-8adddcb/.venv/lib/python3.13/site-packages/numpy/testing/_private/utils.py", line 983, in assert_array_compare
    raise AssertionError(msg)
AssertionError: 
Not equal to tolerance rtol=0, atol=0

Mismatched elements: 3 / 120 (2.5%)
Mismatch at indices:
 [102]: 124.96 (ACTUAL), 124.96000000000001 (DESIRED)
 [103]: 173.3 (ACTUAL), 173.29999999999998 (DESIRED)
 [113]: 135.4 (ACTUAL), 135.39999999999998 (DESIRED)
Max absolute difference among violations: 2.84217094e-14
Max relative difference among violations: 2.09909228e-16
 ACTUAL: array([ 3.836000e+01,  3.390000e+01,  3.177000e+01,  3.031000e+01,
        2.992000e+01,  2.906000e+01,  2.900000e+01,  2.910000e+01,
        3.038000e+01,  3.139000e+01,  3.014000e+01,  2.991000e+01,...
 DESIRED: array([ 3.836000e+01,  3.390000e+01,  3.177000e+01,  3.031000e+01,
        2.992000e+01,  2.906000e+01,  2.900000e+01,  2.910000e+01,
        3.038000e+01,  3.139000e+01,  3.014000e+01,  2.991000e+01,...
```

### Command 35 — exit 0

```bash
UV_OFFLINE=true uv run --frozen python - <<'PY'
from pathlib import Path
import hashlib, json
from datetime import date, timedelta
import numpy as np
import pandas as pd
from delu_forecast.features import residual_proxy_details
r=Path.cwd()
raw=pd.read_parquet(r/'data/snapshot.parquet')
times=pd.DatetimeIndex(raw.timestamp_utc)
local=times.tz_convert('Europe/Berlin')
meta=json.loads((r/'data/source_manifest.json').read_text())
for col, coverage in meta['coverage'].items():
    v=raw[col]
    assert int(v.notna().sum()) == coverage['non_null_rows']
    assert int(v.isna().sum()) == coverage['null_rows']
    assert times[v.notna()][0].isoformat() == coverage['first_valid_utc']
    assert times[v.notna()][-1].isoformat() == coverage['last_valid_utc']
for typ in ('actual','forecast'):
    columns=[f'{component}_{typ}_mw' for component in ('wind_onshore','wind_offshore','solar')]
    np.testing.assert_allclose(raw[f'vre_{typ}_mw'], raw[columns].to_numpy().sum(axis=1), rtol=0, atol=0, equal_nan=True)
comparison=pd.read_csv(r/'data/reconciliation.csv')
comparison['timestamp_utc']=pd.to_datetime(comparison.timestamp_utc,utc=True)
assert comparison.timestamp_utc.is_unique
sample=json.loads((r/'data/reconciliation_sample.json').read_text())
for item in sample['delivery_days']:
    day=date.fromisoformat(item['delivery_date'])
    start=pd.Timestamp(day,tz='Europe/Berlin').tz_convert('UTC')
    end=pd.Timestamp(day+timedelta(days=1),tz='Europe/Berlin').tz_convert('UTC')
    part=comparison.loc[comparison.delivery_date.eq(day.isoformat())]
    expected=pd.date_range(start,end,freq='h',inclusive='left')
    assert pd.DatetimeIndex(part.timestamp_utc).as_unit('ns').equals(expected.as_unit('ns'))
    assert part.stratum.eq(item['stratum']).all()
np.testing.assert_allclose(comparison.smard_eur_mwh, raw.set_index('timestamp_utc').loc[comparison.timestamp_utc,'price_eur_mwh'],atol=0.0000005,rtol=0)
print('CSV-to-Parquet maximum error', float(np.max(abs(comparison.smard_eur_mwh.to_numpy()-raw.set_index('timestamp_utc').loc[comparison.timestamp_utc,'price_eur_mwh'].to_numpy()))))
diffs=abs(comparison.entsoe_eur_mwh-comparison.smard_eur_mwh)
np.testing.assert_allclose(diffs,comparison.abs_diff_eur_mwh,atol=0,rtol=0)
assert diffs.le(sample['tolerance_eur_mwh']).all()
print('Independent reconciliation: 120/120 exact timestamps, strata, stored SMARD values and difference arithmetic; max difference',diffs.max())
actual=residual_proxy_details(raw)
vre=raw.vre_actual_mw.to_numpy()
hours=local.hour.to_numpy()
row_dates=local.date
expected_norm=np.full(len(raw),np.nan)
counts=np.zeros(len(raw),dtype=int)
for day in sorted(set(local.date)):
    start=pd.Timestamp(day-timedelta(days=43),tz='Europe/Berlin').tz_convert('UTC')
    end=pd.Timestamp(day-timedelta(days=1),tz='Europe/Berlin').tz_convert('UTC')
    first=int(times.searchsorted(start)); last=int(times.searchsorted(end))
    expected_size=int((end-start).total_seconds()/3600)
    valid=last-first==expected_size and np.isfinite(vre[first:last]).all()
    target=np.flatnonzero(row_dates==day)
    for hour in set(hours[target]):
        observed=vre[first:last][hours[first:last]==hour]
        rows=target[hours[target]==hour]
        if valid: expected_norm[rows]=observed.mean()
        counts[rows]=len(observed)
np.testing.assert_allclose(actual.vre_norm,expected_norm,atol=1e-9,rtol=1e-12,equal_nan=True)
np.testing.assert_allclose(actual.residual_load_proxy,raw.load_forecast_mw.to_numpy()-expected_norm,atol=1e-9,rtol=1e-12,equal_nan=True)
print('Independent A75 oracle:',len(raw),'rows; valid norms',int(np.isfinite(expected_norm).sum()),'; max error',float(np.nanmax(abs(expected_norm-actual.vre_norm))))
for name in ('fig_welch_periodogram.png','fig_per_regime_periodogram.png','fig_acf_24_168.png','spectral_peak_bins.csv'):
    a=(r/'reports'/name).read_bytes(); b=(Path('/tmp/pjm-cp1-v68-review/critic-spectral')/name).read_bytes()
    assert a==b
    print('Byte-identical',name,hashlib.sha256(a).hexdigest())
PY
```

Observed:

```text
CSV-to-Parquet maximum error 2.842170943040401e-14
Independent reconciliation: 120/120 exact timestamps, strata, stored SMARD values and difference arithmetic; max difference 0.0
Independent A75 oracle: 67343 rows; valid norms 65303 ; max error 2.1827872842550278e-11
Byte-identical fig_welch_periodogram.png 4e09646b47c42676b0ba5c509112d52ec55a5ec134e596b3bf743fd1f945eb93
Byte-identical fig_per_regime_periodogram.png 010b0b9c0050d4ea5f6a296d1237a31b4ce981126cad33e8c1f9fae6d7a205d1
Byte-identical fig_acf_24_168.png 232140c2fa3527952c3e5bce87484cdcc6ddf6a17d73d6530f051ba8a3825253
Byte-identical spectral_peak_bins.csv 11d9470f4daaf9de44665cc16a7d187284e5ffbb66b736ec230e84eb1f8e8bf5
```

### Command 36 — exit 0

```bash
UV_OFFLINE=true uv run --frozen python - <<'PY'
from datetime import date, timedelta
from pathlib import Path
import duckdb
import numpy as np
import pandas as pd
raw=pd.read_parquet('data/snapshot.parquet')
script=Path('sql/feature_queries.sql').read_text().replace("read_parquet('data/snapshot.parquet')",'critic_input')
source=date(2025,10,26)
repeated=raw.index[raw.delivery_date.eq(source)&raw.local_hour.eq(2)]
assert len(repeated)==2
partial=raw.drop(index=repeated[0])
con=duckdb.connect(':memory:'); con.register('critic_input',partial); con.execute(script)
for days in (1,2,7):
    target=source+timedelta(days=days)
    vals=con.execute(f"SELECT price_lag_{days*24}h FROM lag_features WHERE CAST(timezone('Europe/Berlin',timestamp_utc) AS DATE)=? AND hour(timezone('Europe/Berlin',timestamp_utc))=2",[target]).fetchall()
    assert vals==[(None,)],vals
    rolling=con.execute('SELECT * EXCLUDE (delivery_date) FROM rolling_features WHERE delivery_date=?',[target]).fetchone()
    assert all(value is None for value in rolling),rolling
print('SQL damaged-calendar check: all three lags reject a partially observed ambiguous source; all eight rolling statistics reject missing in-window source hour on D+1, D+2, D+7.')
con.close()
for target in (date(2025,2,15),date(2025,3,30),date(2025,10,26)):
    original=duckdb.connect(':memory:'); original.register('critic_input',raw); original.execute(script)
    before=original.execute('SELECT * FROM rolling_features WHERE delivery_date=?',[target]).fetchdf()
    before_lag=original.execute("SELECT * FROM lag_features WHERE CAST(timezone('Europe/Berlin',timestamp_utc) AS DATE)=? ORDER BY timestamp_utc",[target]).fetchdf().drop(columns='price_eur_mwh')
    changed=raw.copy(); changed.loc[changed.delivery_date.eq(target),'price_eur_mwh']=-999999.
    mutated=duckdb.connect(':memory:'); mutated.register('critic_input',changed); mutated.execute(script)
    after=mutated.execute('SELECT * FROM rolling_features WHERE delivery_date=?',[target]).fetchdf()
    after_lag=mutated.execute("SELECT * FROM lag_features WHERE CAST(timezone('Europe/Berlin',timestamp_utc) AS DATE)=? ORDER BY timestamp_utc",[target]).fetchdf().drop(columns='price_eur_mwh')
    pd.testing.assert_frame_equal(before,after); pd.testing.assert_frame_equal(before_lag,after_lag)
    print('SQL target-day price mutation unchanged:',target,len(before_lag),'rows')
    original.close(); mutated.close()
PY
```

Observed:

```text
SQL damaged-calendar check: all three lags reject a partially observed ambiguous source; all eight rolling statistics reject missing in-window source hour on D+1, D+2, D+7.
SQL target-day price mutation unchanged: 2025-02-15 24 rows
SQL target-day price mutation unchanged: 2025-03-30 23 rows
SQL target-day price mutation unchanged: 2025-10-26 25 rows
```

### Command 37 — exit 0

```bash
python3 - <<'PY'
from pathlib import Path
import subprocess
sha='8adddcb62f38198fcffd7b258eaa5075435eecf2'
committed=subprocess.check_output(['git','show',sha+':capstone_V6_8.md'],text=True)
working=Path('capstone_V6_8.md').read_text()
start=committed.index('**CP-1 (10 items)**')
end=committed.index('\n\n',start)
bar=committed[start:end]
assert bar in working
assert len([line for line in bar.splitlines() if line.startswith('- [ ]')])==10
print(bar)
PY
```

Observed:

```text
Exact ten-item CP-1 excerpt extracted from the candidate Git object; same text present in the clean worktree and matches the assigned verbatim bar.
```

### Command 38 — exit 0

```bash
git rev-parse HEAD && git rev-parse 'HEAD^{tree}' && git rev-parse --abbrev-ref HEAD && git status --porcelain=v1 && git diff --stat
```

Observed:

```text
HEAD remains 8adddcb62f38198fcffd7b258eaa5075435eecf2; tree remains 283a934378e425dfe63155c9a2751acb9fe3afa8; detached HEAD; git status --porcelain=v1 and git diff --stat both empty immediately before verdict creation.
```

### Local-image inspection tools

- `view_image({"path":"/tmp/pjm-cp1-v68-review/critic-cp-1-8adddcb/reports/fig_welch_periodogram.png"})` — success; 24h/168h/12h labels and peaks visually inspected.
- `view_image({"path":"/tmp/pjm-cp1-v68-review/critic-cp-1-8adddcb/reports/fig_per_regime_periodogram.png"})` — success; three regime curves, legend and elevated crisis floor inspected.
- `view_image({"path":"/tmp/pjm-cp1-v68-review/critic-cp-1-8adddcb/reports/fig_acf_24_168.png"})` — success; daily/weekly references and recurrence inspected.

No process exit code applies to the image-tool calls. The verdict was written only after the final clean-check command above.

### Post-write artifact validation — exit 0

```bash
python3 - <<'PY'
from pathlib import Path
import subprocess
p=Path('/tmp/pjm-cp1-v68-review/integration-v68.md')
text=p.read_text()
assert text.startswith('# Verdict — M1 / CP-1 — Integration — PASS\n')
assert '| 10 |' in text and 'Post-review evidence-commit verification is reserved for the Lead' in text
plan=Path('capstone_V6_8.md').read_text()
start=plan.index('**CP-1 (10 items)**'); end=plan.index('\n\n',start)
assert plan[start:end] in text
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()=='8adddcb62f38198fcffd7b258eaa5075435eecf2'
assert subprocess.check_output(['git','status','--porcelain=v1'],text=True)==''
print('PASS verdict exists; exact bar and all ten checklist rows present; HEAD unchanged and candidate status still empty.')
PY
```

Observed: PASS verdict exists; exact bar and all ten checklist rows present; HEAD unchanged and candidate status still empty. This check preceded the final ledger addition, with no candidate mutation.
