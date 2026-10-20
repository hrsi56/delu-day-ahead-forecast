# Verdict — CP-26 — Integration — FAIL

- Candidate SHA: `f7a0273798a76ad55aad1c69f40893bc149d1f6e`.
- Plan/version/bar: `capstone_v21.md` v21-r16, complete §24.7 at `4766a61cb0c836573406f5a9729997d1b6ee9862`; raw plan SHA-256 `27bdc6046117a543d4bfcaa439651e7bf2a8fa4d0c58af9631b606a358c10fd1`.
- Fresh detached checkout: `/Users/djourno/Downloads/PJM/.local/worktrees/cp-26/critic-final-r16-1`.
- HEAD exact and tracked/untracked status empty before review and immediately before this verdict. Detached `git symbolic-ref -q HEAD` returned 1 both times. Isolation is cooperative read-only, not an OS mount guarantee.
- No Builder checkout/story, prior CP-26 verdict, progress.md, orchestrator-role.md, syllabus or Track A/C was read. No source/output/Git mutation, estimator fit, search/forecast/score/inference/diagnostic/report generation, retrieval, publication or CP-28 execution was performed. Scratch files are confined to this assignment folder. The Lead owns preservation and checkout removal.

## Decision and the largest meaningful gap

**FAIL — required reporting disclosures are absent (F1).** The complete numerical analysis is present and bounded verification passed. However, `src/cp26/reporting.py` lines 529–533 constructs only four generic limitations; the generated report and draft packet carry those four, with none of the mandatory CP-25 qualifications. The load section merely says that the nominal policy retains load under the ruling.

The omitted facts are (a) the tier-3 load history has no original vintages and retains revision risk under the Owner exception, (b) tier-2 target prices retain SMARD's update-possible caveat, (c) price +24h, GFS +24h and load +1h are accepted disclosed operational risks rather than proven safe margins, and (d) the “never scored” mask includes historical training-only inner-validation overlap and is descriptive. These are explicit reporting obligations in `docs/track-b/cp-25-rulings-2026-10-12.md` §§1–4 and its landing record, carried by §24.5 and PUBLISH_RULES §§2,3,11. They are absent from the actual `report.json.limitations`, rendered `report.md`, and packet limitations/slot text. Hashing the ruling as a source does not disclose its substance to a reader. This failure is unrelated to the unfavorable GFS sensitivity or any scientific threshold.

**Exact next acceptance test:** From the same preserved score/inference/diagnostic artifacts, regenerate only the report/draft packet through a narrowly repaired generator and prove both structured and rendered report/packet contain these four source-bound disclosures; add a meaningful negative check that rejects an omitted qualification. Preserve every scientific artifact byte, seed and stored replicate, then submit a new committed candidate for one fresh full Integration review.

## Commands actually run and observed results

All source commands used the fresh checkout above as cwd. Exact bounded bodies are retained as `review.py` (corrected body), `review-results-1.json` (original attempt), `task.json`, `task-2.json`, and raw job requests; canonical requests bind actual command strings. `scripts/bar.py` writes quoted bar bytes to stdout and the plan identity summary to stderr. My original harness merged stderr into stdout and incorrectly compared that merged stream with the quote-only file. Job 479 stopped at that assertion, before any test or science operation. Source inspection at `scripts/bar.py:117–120` established the cause; job 480 separated the initial stderr summary from the merged capture and byte-matched the quoted block. No candidate failure was retried or tolerance weakened.

| Command/check actually executed | Exit | Observed result |
|---|---:|---|
| `git rev-parse HEAD`; `git status --porcelain=v1`; `git symbolic-ref -q HEAD` | 0;0;1 | exact candidate; empty; detached, before and after |
| `/Users/djourno/Downloads/PJM/.venv/bin/python -B scripts/bar.py bar capstone_v21.md '24.7 CP-26: the re-baseline on every development day (stage 6)' --at 4766a61cb0c836573406f5a9729997d1b6ee9862 --quote` | 0 | exact quote-only bytes equal complete-bar-v21-r16.md; raw section 250 lines/15129 bytes, SHA256 423527d92156e47742c0aba593f04b08334e7a9b526f0dbc6208a3c38dcf5b1e |
| `/Users/djourno/Downloads/PJM/.venv/bin/python -B scripts/bar.py check docs/track-b/evidence/cp-26/cold-rerun-2026-10-15/complete-supporting-bar-v21-r16.md --source capstone_v21.md@4766a61cb0c836573406f5a9729997d1b6ee9862` | 0 | all eleven complete supporting quote blocks occur byte-for-byte in the pinned anchor |
| `/Users/djourno/Downloads/PJM/.venv/bin/python -B -m pytest -q -p no:cacheprovider --basetemp /Users/djourno/Downloads/PJM/.local/tmp/cp26-continuation/integration-r16-1/pytest-tmp tests/test_cp26_analysis_inventory.py tests/test_cp26_reporting.py tests/test_cp26_diagnostic_cells.py tests/test_cp26_inference_rng.py tests/test_cp26_r16.py` | 0 | 47 passed in 43.79s; synthetic fixtures, no estimator or production analysis rerun |
| Bounded `review.py`: signed artifact inventory + streaming SHA256, `_validate_completed` for inference and diagnostics, registered score/table validation, direct primary reduction from stored daily rows | 0 | 33,943 files / 32,151,027,114 bytes exact; current analysis code matches; 16,024 inference references and 936 moment references bind protocol/scores/code; 104 raw/ratio reductions agree |
| `git diff --name-only 647d6eb81b2cf6e0cfaf4152f659d689ff973578 -- src/delu_forecast src/cp15 src/cp16 src/cp20 src/cp21 src/cp22 src/cp24 src/cp25` | 0 | empty; landed member source unchanged |
| Read-only `git log --follow` on frozen CP-28 protocol and chronological `git log` on plans/pilot/scores/exposure records | 0 | r14 frozen repair commit 563be855… on Oct13 precedes cold plans 42083d9… Oct15, complete pilot eb0e2de… Oct16 and first committed score manifest at candidate Oct19; exposure assessments predate them |
| Read-only `jq`/`sed`/`rg`/`cat` on named source and signed artifacts; selected schema/status/count/limitations queries | 0 except one exploratory jq field query (5) | actual source/evidence inspected; one query tried `.tables` on inference manifest (that schema uses endpoints), then corrected; no candidate failure was retried |
| Existing supervised launcher, task-3.json | 0 on each of four attempts | DEFERRED_SOFT_MEMORY before registration, macOS pressure 2; supplementary detail.py was never executed and supplies no asserted test result |

The supplementary causal-fixture/whole-ledger check was optional coverage expansion after the required bounded checks. It was not necessary to establish F1; it remains unexecuted and is not represented as scientific failure or BLOCKED. Existing source/evidence inspection and the completed checks are the basis of each clause below. No full production science reproduction is claimed.

## Evidence actually inspected

- Governance/bounded role and verdict template: AGENTS.md, engineering-role.md, gauntlet-templates.md §2. Exact complete §24.7 and supporting §§2,14,15,16.2,17,23,24.2,24.4,24.5,24.8,24.9; the complete verified extracts are preserved below.
- Publication contract: PUBLISH_RULES 1.5 raw SHA256 `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`, incorporated publication-standard-v1.md raw SHA256 `7bb90c4cbd15bde42121d615bd850854610a1aa0b3a776190a58ef481abeb68c`, especially evidence qualification, derived records and checkpoint packet. Public rendering/deployment rules are future publication acceptance, not an authorization to publish here.
- CP-25 landing, rulings and exposure assessments, full frozen CP-28 r14 protocol, execution-protocol.json, registration.json, cold issued brief and r16 issued continuation/authority. The exposure ledger's unknown excerpt remains honestly unknown; its adopted quantities are methodological, not market outcomes. No post-boundary material was sought.
- harness.py, members.py, search.py, replay.py, relevant state.py/execution.py/fits.py paths, scoring.py, inference.py, diagnostics.py, analysis.py, reporting.py, budget.py, limits.py, supervisor.py and raw-kernel bootstrap; specified tests and actual logs. The complete-checklist-ready file was used only to enumerate clause text, not as an acceptance oracle.
- Actual parity.json (96 exact checks), timing-pilot.json (1064 sealed probes), execution/forecast completion, replay/learning state schema and route inventories, sample DST day ledger, actual score tables, all inference/diagnostic file pairs in the custody index, full report.json structured limitations/source fields and report.md/publication-packet/MLflow draft artifacts. Exact large paths/SHA/bytes are the candidate's final-analysis-artifact-index-v21-r16.json and its external custody root.
- Custody root: `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26/cold-rerun-2026-10-15/r16/final-analysis-inputs`. Inventory raw SHA256 `7495b0808bccf1f972c52c175a4df46805093e2032fb68b58b6c89b2edd717e2`; signed inventory digest `ed20bf51c8e61e294b5893982c30b4a973c3ed57d7a5bd956fcbe2c0f126bef3`. Every indexed file's actual byte count and SHA validated, rather than merely trusting an existence list.
- Signed content digests: scores `86abda54558fa965d41f44768f5142611e59c40fc521439913cf3c98de392b49`; inference `74033296ff098f023ae8eaf1fb3883efd9cfdbd8591157565aba9ce95f481590`; diagnostics `e6a0435203a2690c2926e6c23d2b6e9ed1dcd5b21ffe215ac569c690fd7fb6aa`. Exact raw SHA for each is preserved by the inventory. Current executed analysis code identity matches all three.

## Resource/command custody

Canonical account: `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26/ledger/budget.json`. It remains the only resource ledger. Both jobs have independent matching completion receipts, group empty and all worker identities stopped. The settled proof is read-only; no receipt or ledger field was edited. Review-only scratch accounting is a report of canonical observations, not a competing charge ledger.

```json
{
  "review_jobs": [
    {
      "name": "cold-r16-integration-review-1",
      "job_id": "1e3036c945fe4b50886d66649cf96698",
      "job_index": 479,
      "exit_code": 1,
      "wall_seconds": 9.052805040992098,
      "charged_wall_seconds": 9.052805040992098,
      "peak_rss_bytes": 1730297856,
      "request": "/Users/djourno/Downloads/PJM/.local/artifacts/cp-26/jobs/cold-r16-integration-review-1.479.1e3036c945fe4b50886d66649cf96698.request.json",
      "request_sha256": "0aafbea5496d01ede28e5fd9bcfc91f03338db15576e73aa4c0df03f541cceb8",
      "completion_clock": "/Users/djourno/Downloads/PJM/.local/artifacts/cp-26/jobs/cold-r16-integration-review-1.479.1e3036c945fe4b50886d66649cf96698.clock.json",
      "group_empty": true,
      "workers_stopped": true,
      "clock_sha256": "cb50d21b942f5c171d035051843fb7d22668e45300546a218e12048b652c7dab"
    },
    {
      "name": "cold-r16-integration-review-2",
      "job_id": "4972cc83cea547669a203478b47a0695",
      "job_index": 480,
      "exit_code": 0,
      "wall_seconds": 137.11984220899467,
      "charged_wall_seconds": 137.11984220899467,
      "peak_rss_bytes": 2174844928,
      "request": "/Users/djourno/Downloads/PJM/.local/artifacts/cp-26/jobs/cold-r16-integration-review-2.480.4972cc83cea547669a203478b47a0695.request.json",
      "request_sha256": "c4bf4e9d42c9c3caf909d6e1c5ee9c52a8303076cf4dc7ffe12986425ee8ecbd",
      "completion_clock": "/Users/djourno/Downloads/PJM/.local/artifacts/cp-26/jobs/cold-r16-integration-review-2.480.4972cc83cea547669a203478b47a0695.clock.json",
      "group_empty": true,
      "workers_stopped": true,
      "clock_sha256": "9e882f64f9ae205713bea582b4dee2ccbadf3bfcae9b3358c79374219066f632"
    }
  ],
  "settled_ending_proofs": [
    {
      "status": "CLOSING_OBSERVERS_SETTLED",
      "job_id": "1e3036c945fe4b50886d66649cf96698",
      "job_index": 479,
      "worker_identity_count": 4,
      "quiet_seconds": 3.547134749998804,
      "wall_seconds": 4.1169797079928685,
      "maximum_wait_with_read_and_poll_seconds": 17.2
    },
    {
      "status": "CLOSING_OBSERVERS_SETTLED",
      "job_id": "4972cc83cea547669a203478b47a0695",
      "job_index": 480,
      "worker_identity_count": 2,
      "quiet_seconds": 3.5031955000013113,
      "wall_seconds": 3.929658875000314,
      "maximum_wait_with_read_and_poll_seconds": 17.2
    }
  ],
  "launcher_process_seconds": [
    1.0805978339922149,
    0.8668143329996383,
    1.2519037909951294,
    1.0482159579987638,
    1.0320294580014888,
    0.9438697500008857
  ],
  "launcher_process_seconds_total": 6.223431123988121,
  "allocated_worker_wall_seconds_total": 146.17264724998677,
  "soft_deferred_name": "cold-r16-integration-review-3",
  "soft_deferred_registered": false,
  "raw_pre_supervisor_rows": "Not imported by this Critic; Lead owns one-time import from canonical raw receipts; excluded from launcher/operator total.",
  "ledger_accounting_snapshot": {
    "measured_seconds": 846967.1509904255,
    "reported_seconds": 2360.863321947783,
    "reserved_seconds": 7367.7453770840075
  },
  "historical_baseline_hours": 65.16212464012295
}
```

The six launcher process durations total 6.223431123988s and are separate from the 146.172647249987s allocated worker wall charge. Raw monitor/bootstrap pre-supervisor gaps are excluded from that operator total and must be imported once by the Lead from existing canonical receipts. Untimed text inspection/file-writing process durations were not reconstructed or invented. The report's resource snapshot is historical, not a claim to include this later review; its 237.860435382h cumulative snapshot preserves the 65.162124640h baseline. The live account above includes the two review jobs and retains the 2,826s reserve plus all later reserves. Approximate review wall effort: 0.5h, including orientation and bounded validation.

## Complete 111-clause verdict

These are independent assessments. PASS means supported within this read-only review's stated bounded checks and source/artifact inspection, not an invented claim to have rerun every production fit. FAIL binds the actual reporting deficiency; Owner LAND remains not due.

| # | Checklist clause | Verdict | Independent evidence/assessment |
|---|---|---|---|
| 1 | **Purpose:** run B0, v1-R and v2–v5 daily on every eligible development day under one protocol. The result is the new all-season baseline, and a stored ledger of every member's out-of-sample forecasts for CP-28 and 4.7T. | PASS | Verified score-table bytes and registered inventories; 13 streams × 2,078 dates retained, with 2,068/755/358/152 mask support. Forecast completion records 2,441 origins including 363 unscored warm-up dates. See review-results.json daily_population and independent_primary_reduction. |
| 2 | **The scored calendar:** delivery days 2020-12-29 to 2026-09-06, 2,078 calendar days, less CP-25's frozen exclusions. | PASS | Verified score-table bytes and registered inventories; 13 streams × 2,078 dates retained, with 2,068/755/358/152 mask support. Forecast completion records 2,441 origins including 363 unscored warm-up dates. See review-results.json daily_population and independent_primary_reduction. |
| 3 | **The warm-up:** delivery days 2020-01-01 to 2020-12-28, forecast the same way and never scored. It only fills interval buffers and CP-28's first ledger. | PASS | Verified score-table bytes and registered inventories; 13 streams × 2,078 dates retained, with 2,068/755/358/152 mask support. Forecast completion records 2,441 origins including 363 unscored warm-up dates. See review-results.json daily_population and independent_primary_reduction. |
| 4 | **Four masks are reported separately:** | PASS | Verified score-table bytes and registered inventories; 13 streams × 2,078 dates retained, with 2,068/755/358/152 mask support. Forecast completion records 2,441 origins including 363 unscored warm-up dates. See review-results.json daily_population and independent_primary_reduction. |
| 5 | every eligible day; | PASS | Verified score-table bytes and registered inventories; 13 streams × 2,078 dates retained, with 2,068/755/358/152 mask support. Forecast completion records 2,441 origins including 363 unscored warm-up dates. See review-results.json daily_population and independent_primary_reduction. |
| 6 | the days never scored before (CP-25's mask); | FAIL | Verified score-table bytes and registered inventories; 13 streams × 2,078 dates retained, with 2,068/755/358/152 mask support. Forecast completion records 2,441 origins including 363 unscored warm-up dates. See review-results.json daily_population and independent_primary_reduction. FAIL F1 applies to its mandatory interpretation: the CP-25 inner-validation overlap limitation is absent from the report and packet. |
| 7 | the old-fold days, folds 2–5, re-run under this protocol; | PASS | Verified score-table bytes and registered inventories; 13 streams × 2,078 dates retained, with 2,068/755/358/152 mask support. Forecast completion records 2,441 origins including 363 unscored warm-up dates. See review-results.json daily_population and independent_primary_reduction. |
| 8 | 2026-04-08 to 2026-09-06, newly opened and used earlier by v1. | PASS | Verified score-table bytes and registered inventories; 13 streams × 2,078 dates retained, with 2,068/755/358/152 mask support. Forecast completion records 2,441 origins including 363 unscored warm-up dates. See review-results.json daily_population and independent_primary_reduction. |
| 9 | The old five-fold results, their S_MAE and S_WIS and their uncertainty stay as the historical record, never overwritten. | PASS | Read-only git diff against 647d6eb81b2cf6e0cfaf4152f659d689ff973578 is empty for every landed member source directory; historical references remain separately identified in scoring.py/report.md. |
| 10 | **B0,** the similar-day naive, unchanged. | PASS | members.py fit_b0, v1_features, v1_recipe, v1r_windows and fit_v1r; exact base features, two embargoes, nine heads, CQR then isotonic, n_jobs=1; manifest-bound score rows and emitted records. No further method change was found. |
| 11 | **v1-R (728-day window, no hindsight regime flags):** the released v1 recipe, refit daily, with two declared method changes: | PASS | members.py fit_b0, v1_features, v1_recipe, v1r_windows and fit_v1r; exact base features, two embargoes, nine heads, CQR then isotonic, n_jobs=1; manifest-bound score rows and emitted records. No further method change was found. |
| 12 | `crisis_period` and `post_crisis` are removed (§24.5); | PASS | members.py fit_b0, v1_features, v1_recipe, v1r_windows and fit_v1r; exact base features, two embargoes, nine heads, CQR then isotonic, n_jobs=1; manifest-bound score rows and emitted records. No further method change was found. |
| 13 | the training window is 728 days, where v1 expanded from 2019-01-01. | PASS | members.py fit_b0, v1_features, v1_recipe, v1r_windows and fit_v1r; exact base features, two embargoes, nine heads, CQR then isotonic, n_jobs=1; manifest-bound score rows and emitted records. No further method change was found. |
| 14 | The rest of the recipe is the `base` catalog, the nine LightGBM quantile heads, CQR, and isotonic ordering, laid out for each origin D as follows: | PASS | members.py fit_b0, v1_features, v1_recipe, v1r_windows and fit_v1r; exact base features, two embargoes, nine heads, CQR then isotonic, n_jobs=1; manifest-bound score rows and emitted records. No further method change was found. |
| 15 | the heads train on `[max(2019-01-01, D−728), D−62)`; | PASS | members.py fit_b0, v1_features, v1_recipe, v1r_windows and fit_v1r; exact base features, two embargoes, nine heads, CQR then isotonic, n_jobs=1; manifest-bound score rows and emitted records. No further method change was found. |
| 16 | day D−62 is an embargo; | PASS | members.py fit_b0, v1_features, v1_recipe, v1r_windows and fit_v1r; exact base features, two embargoes, nine heads, CQR then isotonic, n_jobs=1; manifest-bound score rows and emitted records. No further method change was found. |
| 17 | CQR calibrates on D−61 to D−2; | PASS | members.py fit_b0, v1_features, v1_recipe, v1r_windows and fit_v1r; exact base features, two embargoes, nine heads, CQR then isotonic, n_jobs=1; manifest-bound score rows and emitted records. No further method change was found. |
| 18 | day D−1 is an embargo. | PASS | members.py fit_b0, v1_features, v1_recipe, v1r_windows and fit_v1r; exact base features, two embargoes, nine heads, CQR then isotonic, n_jobs=1; manifest-bound score rows and emitted records. No further method change was found. |
| 19 | The thread count follows the worker's allotment; that is not a method change. | PASS | members.py fit_b0, v1_features, v1_recipe, v1r_windows and fit_v1r; exact base features, two embargoes, nine heads, CQR then isotonic, n_jobs=1; manifest-bound score rows and emitted records. No further method change was found. |
| 20 | **The released artifact** is reported descriptively, on its holdout days only: 2026-06-09 to 2026-09-06. | PASS | scoring.py RELEASED_REFERENCE_PINS and released-reference reconstruction; report.json has no missing reference and report.md includes historical holdout rows only, distinct from daily refits. |
| 21 | If v1-R cannot be built without a further method change, CP-26 reports v1 through the released artifact and B1's preserved vectors on the old folds, and says so. | N/A (condition not triggered) | Not triggered: v1-R is built by the prescribed recipe; no substitute method was introduced. |
| 22 | **v2, v3, v4 and v5,** through the harness below: their landed member code, fixed blend weights, interval layers, seeds and inner tuning rules, unchanged. Only the data identity, the boundary, the weather source, the issue time and the calendar follow this section. | PASS | harness.py explicit HARNESS_LOG/PINS, members.py imported landed primitives, replay.py landed central arithmetic, and unchanged landed-source git diff; analysis manifest code identities match the candidate exactly. Ruling-specific no-load and GFS+6 adapters are explicit. |
| 23 | **A tier-3 ruling** may name a variant, built only by the ruling's declared changes (§24.5). | PASS | harness.py explicit HARNESS_LOG/PINS, members.py imported landed primitives, replay.py landed central arithmetic, and unchanged landed-source git diff; analysis manifest code identities match the candidate exactly. Ruling-specific no-load and GFS+6 adapters are explicit. |
| 24 | **DDNN-2 alone** is descriptive in CP-26. It is a CP-28 arm (§24.8). | PASS | harness.py explicit HARNESS_LOG/PINS, members.py imported landed primitives, replay.py landed central arithmetic, and unchanged landed-source git diff; analysis manifest code identities match the candidate exactly. Ruling-specific no-load and GFS+6 adapters are explicit. |
| 25 | **The harness.** The landed code refuses any snapshot, boundary or anchor other than its own (`src/cp15/data.py`, `src/cp20/inputs.py`, `src/cp24/inputs.py`). CP-26 therefore builds a harness that imports the landed member code unchanged and replaces only: | PASS | harness.py explicit HARNESS_LOG/PINS, members.py imported landed primitives, replay.py landed central arithmetic, and unchanged landed-source git diff; analysis manifest code identities match the candidate exactly. Ruling-specific no-load and GFS+6 adapters are explicit. |
| 26 | the data identity: the new partition specification and CP-25's manifest; | PASS | harness.py explicit HARNESS_LOG/PINS, members.py imported landed primitives, replay.py landed central arithmetic, and unchanged landed-source git diff; analysis manifest code identities match the candidate exactly. Ruling-specific no-load and GFS+6 adapters are explicit. |
| 27 | the boundary; | PASS | harness.py explicit HARNESS_LOG/PINS, members.py imported landed primitives, replay.py landed central arithmetic, and unchanged landed-source git diff; analysis manifest code identities match the candidate exactly. Ruling-specific no-load and GFS+6 adapters are explicit. |
| 28 | the weather source: CP-20's grids plus CP-25's; | PASS | harness.py explicit HARNESS_LOG/PINS, members.py imported landed primitives, replay.py landed central arithmetic, and unchanged landed-source git diff; analysis manifest code identities match the candidate exactly. Ruling-specific no-load and GFS+6 adapters are explicit. |
| 29 | the issue-time label; | PASS | harness.py explicit HARNESS_LOG/PINS, members.py imported landed primitives, replay.py landed central arithmetic, and unchanged landed-source git diff; analysis manifest code identities match the candidate exactly. Ruling-specific no-load and GFS+6 adapters are explicit. |
| 30 | the identity pins: the protocol revision, the anchor and issued-document hashes, and the lineage checks. Each replaced pin is listed in the harness log. | PASS | harness.py explicit HARNESS_LOG/PINS, members.py imported landed primitives, replay.py landed central arithmetic, and unchanged landed-source git diff; analysis manifest code identities match the candidate exactly. Ruling-specific no-load and GFS+6 adapters are explicit. |
| 31 | **The parity gate, before the full run.** Under the old settings (11:00 UTC, the old identity and boundary), the harness reproduces the committed central vectors bitwise at sampled old-fold origins: | PASS | Actual parity.json inspected: PASS, 96 checks, every bitwise_equal and keys_equal true; all A1/B2/A1_w/B2_w/L-N/L-R/D2/B0/v2–v5 names and nominal/restored-no-load routes present. No estimator rerun. |
| 32 | for A1, B2, A1_w, B2_w, L-N and L-R; | PASS | Actual parity.json inspected: PASS, 96 checks, every bitwise_equal and keys_equal true; all A1/B2/A1_w/B2_w/L-N/L-R/D2/B0/v2–v5 names and nominal/restored-no-load routes present. No estimator rerun. |
| 33 | for D2, on CP-24's committed ensembles. Those ensembles check parity only, and never serve a CP-26 forecast; | PASS | Actual parity.json inspected: PASS, 96 checks, every bitwise_equal and keys_equal true; all A1/B2/A1_w/B2_w/L-N/L-R/D2/B0/v2–v5 names and nominal/restored-no-load routes present. No estimator rerun. |
| 34 | for B0, and for the assembled v2–v5 central vectors. | PASS | Actual parity.json inspected: PASS, 96 checks, every bitwise_equal and keys_equal true; all A1/B2/A1_w/B2_w/L-N/L-R/D2/B0/v2–v5 names and nominal/restored-no-load routes present. No estimator rerun. |
| 35 | If parity fails, the Lead stops and reports. | PASS | Actual parity.json inspected: PASS, 96 checks, every bitwise_equal and keys_equal true; all A1/B2/A1_w/B2_w/L-N/L-R/D2/B0/v2–v5 names and nominal/restored-no-load routes present. No estimator rerun. |
| 36 | **Search dates:** S_k = 2020-01-15 + 182k days, for k = 0 to 13. Search k serves only the origins from S_k up to the day before S_(k+1). Before S_0 there is no native D2 forecast. | PASS | search.py inspected end to end: support-only all-split extrema, 14 dates, fixed 128 draws, separate fixed seed domains, landed halving/ranking, effective-config deduplication without extra trials, exact eight-member validation, immutable failed cache records and service-period refusal. execution-manifest/search-result artifacts and pre-fit committed plans provide actual run evidence. |
| 37 | **The batches:** consecutive 28-day blocks, tiling backward from S_k − 1. | PASS | search.py inspected end to end: support-only all-split extrema, 14 dates, fixed 128 draws, separate fixed seed domains, landed halving/ranking, effective-config deduplication without extra trials, exact eight-member validation, immutable failed cache records and service-period refusal. execution-manifest/search-result artifacts and pre-fit committed plans provide actual run evidence. |
| 38 | Among blocks starting on or after 2019-07-01, keep up to the 11 newest eligible blocks. | PASS | search.py inspected end to end: support-only all-split extrema, 14 dates, fixed 128 draws, separate fixed seed domains, landed halving/ranking, effective-config deduplication without extra trials, exact eight-member validation, immutable failed cache records and service-period refusal. execution-manifest/search-result artifacts and pre-fit committed plans provide actual run evidence. |
| 39 | Use exactly the landed DDNN-2 support mask, complete-calendar-week pool and 20% holdout-week count, retaining its exclusion of the most recent seven days. Let N be the supported window days and m the fixed held-out week count. Minimum training support is N minus the sum of the m largest week supports; minimum holdout support is the sum of the m smallest. Accept only minima at least 250 and 14 respectively. Eligibility must hold for every possible split. | PASS | search.py inspected end to end: support-only all-split extrema, 14 dates, fixed 128 draws, separate fixed seed domains, landed halving/ranking, effective-config deduplication without extra trials, exact eight-member validation, immutable failed cache records and service-period refusal. execution-manifest/search-result artifacts and pre-fit committed plans provide actual run evidence. |
| 40 | Lists depend only on support, are shared by every configuration in a search and are signed before fitting. No seed, loss or convergence filters them. B is computed, never hard-coded: the expected reproduction is [1,7,11,…,11], with first block 2019-12-18..2020-01-14 and minima 251/46. The algorithm and frozen inputs govern if a reported count disagrees. | PASS | search.py inspected end to end: support-only all-split extrema, 14 dates, fixed 128 draws, separate fixed seed domains, landed halving/ranking, effective-config deduplication without extra trials, exact eight-member validation, immutable failed cache records and service-period refusal. execution-manifest/search-result artifacts and pre-fit committed plans provide actual run evidence. |
| 41 | There is no fold skip rule: every block lies before the search's first origin. | PASS | search.py inspected end to end: support-only all-split extrema, 14 dates, fixed 128 draws, separate fixed seed domains, landed halving/ranking, effective-config deduplication without extra trials, exact eight-member validation, immutable failed cache records and service-period refusal. execution-manifest/search-result artifacts and pre-fit committed plans provide actual run evidence. |
| 42 | **One fit per trial and batch,** on `[max(2019-01-01, b − 728), b)`. | PASS | search.py inspected end to end: support-only all-split extrema, 14 dates, fixed 128 draws, separate fixed seed domains, landed halving/ranking, effective-config deduplication without extra trials, exact eight-member validation, immutable failed cache records and service-period refusal. execution-manifest/search-result artifacts and pre-fit committed plans provide actual run evidence. |
| 43 | **The sampler:** seeded with `SeedSequence([26, k, 0x5A3])`, with 128 trials. Successive halving, the ranking metric and the tie rule follow §23.4. | PASS | search.py inspected end to end: support-only all-split extrema, 14 dates, fixed 128 draws, separate fixed seed domains, landed halving/ranking, effective-config deduplication without extra trials, exact eight-member validation, immutable failed cache records and service-period refusal. execution-manifest/search-result artifacts and pre-fit committed plans provide actual run evidence. |
| 44 | **Frozen fit seeds:** trial/batch seed = `26_000_000 + k*100_000 + trial*100 + batch`, trial=0..127 and retained batch=0..10, newest first. Ensemble member seed = `26_000_000 + k*100_000 + 90_000 + 10*rank + repeat`, rank=1..4 and repeat=1..2. These disjoint domains are fixed before fitting and shared across the three routes; no retries with replacement seeds. Sampling space/priors remain the landed permitted space. | PASS | search.py inspected end to end: support-only all-split extrema, 14 dates, fixed 128 draws, separate fixed seed domains, landed halving/ranking, effective-config deduplication without extra trials, exact eight-member validation, immutable failed cache records and service-period refusal. execution-manifest/search-result artifacts and pre-fit committed plans provide actual run evidence. |
| 45 | **The ensemble:** four best distinct effective configurations, two seeds each, exactly eight members. Effective identity excludes trial id; in the no-load variant it also excludes removed load flags. Duplicates consume trials; no extra sampling compensates for them. A configuration failing a required batch cannot rank over all batches. | PASS | search.py inspected end to end: support-only all-split extrema, 14 dates, fixed 128 draws, separate fixed seed domains, landed halving/ranking, effective-config deduplication without extra trials, exact eight-member validation, immutable failed cache records and service-period refusal. execution-manifest/search-result artifacts and pre-fit committed plans provide actual run evidence. |
| 46 | **Search failure:** zero eligible blocks or fewer than four valid effective configurations is recorded. D2 is unavailable throughout that search's service period; the next search remains on schedule. Never extend an earlier ensemble or relax a threshold. One failed daily member invalidates D2 for that date: no median of a successful subset. | PASS | search.py inspected end to end: support-only all-split extrema, 14 dates, fixed 128 draws, separate fixed seed domains, landed halving/ranking, effective-config deduplication without extra trials, exact eight-member validation, immutable failed cache records and service-period refusal. execution-manifest/search-result artifacts and pre-fit committed plans provide actual run evidence. |
| 47 | **CP-24's ensembles are never reused** for a CP-26 forecast. | PASS | search.py inspected end to end: support-only all-split extrema, 14 dates, fixed 128 draws, separate fixed seed domains, landed halving/ranking, effective-config deduplication without extra trials, exact eight-member validation, immutable failed cache records and service-period refusal. execution-manifest/search-result artifacts and pre-fit committed plans provide actual run evidence. |
| 48 | **A daily refit** at every origin, for every member, on `[max(2019-01-01, D−728), D)`, filtered by availability at the issue time. For every scored day the window is exactly 728 days. | PASS | members.py Context/fitters, fits.py identity-bound cache use through replay/execution, target_provenance and stored training cutoffs; 728-day selectors and publication-aware causal inputs remain landed. Full-calendar signed completion and score tables inspected; no expanding-window route exists. |
| 49 | **A training target enters only once its price was published** before the issue time. | PASS | members.py Context/fitters, fits.py identity-bound cache use through replay/execution, target_provenance and stored training cutoffs; 728-day selectors and publication-aware causal inputs remain landed. Full-calendar signed completion and score tables inspected; no expanding-window route exists. |
| 50 | **No expanding-window sensitivity** is run under the short path. | PASS | members.py Context/fitters, fits.py identity-bound cache use through replay/execution, target_provenance and stored training cutoffs; 728-day selectors and publication-aware causal inputs remain landed. Full-calendar signed completion and score tables inspected; no expanding-window route exists. |
| 51 | **Primary:** | PASS | scoring.py emitted quantiles and actual-hour daily aggregation; independently reduced 104 stream/mask/metric primary cells from hash-verified daily rows. Raw means agree within 1e-12 and ratios within 1e-14 representation rounding; no method tolerance was widened. |
| 52 | p50 MAE, and the seven-quantile WIS (50/80/95% intervals, weights α/2, median weight 1/2, divided by 3.5); | PASS | scoring.py emitted quantiles and actual-hour daily aggregation; independently reduced 104 stream/mask/metric primary cells from hash-verified daily rows. Raw means agree within 1e-12 and ratios within 1e-14 representation rounding; no method tolerance was widened. |
| 53 | each day's loss is the mean over its actual hours, and days weigh equally; | PASS | scoring.py emitted quantiles and actual-hour daily aggregation; independently reduced 104 stream/mask/metric primary cells from hash-verified daily rows. Raw means agree within 1e-12 and ratios within 1e-14 representation rounding; no method tolerance was widened. |
| 54 | the B0 ratio is the policy's mean daily loss over B0's, reported beside the raw losses. | PASS | scoring.py emitted quantiles and actual-hour daily aggregation; independently reduced 104 stream/mask/metric primary cells from hash-verified daily rows. Raw means agree within 1e-12 and ratios within 1e-14 representation rounding; no method tolerance was widened. |
| 55 | **Secondary:** | PASS | scoring.py secondary estimands and fixed registered score universe; summaries/local-hour tables validated (5,096 and 2,496 cells), secondary table bytes hash-verified in the full custody inventory; years 2020–2026 and quarter cells retained with undefined support explicit. |
| 56 | the mean of the four pooled-season ratios; | PASS | scoring.py secondary estimands and fixed registered score universe; summaries/local-hour tables validated (5,096 and 2,496 cells), secondary table bytes hash-verified in the full custody inventory; years 2020–2026 and quarter cells retained with undefined support explicit. |
| 57 | the mean of the five complete-year ratios, 2021 to 2025; | PASS | scoring.py secondary estimands and fixed registered score universe; summaries/local-hour tables validated (5,096 and 2,496 cells), secondary table bytes hash-verified in the full custody inventory; years 2020–2026 and quarter cells retained with undefined support explicit. |
| 58 | 2020 and 2026, both partial, reported separately; quarters descriptive. | PASS | scoring.py secondary estimands and fixed registered score universe; summaries/local-hour tables validated (5,096 and 2,496 cells), secondary table bytes hash-verified in the full custody inventory; years 2020–2026 and quarter cells retained with undefined support explicit. |
| 59 | **Calibration, descriptive:** | PASS | diagnostics.py inspected: inclusive coverage with width/exceedances, strict/weak hits and eight upper-tie bins, calendar-adjacent Christoffersen tests, fixed moment family. _validate_completed accepted all 936 cells/Holm rows, exact code/protocol/score bindings and 11,388/26,572/30,368 registered calibration cells. 935 moment cells computable, one bound-tie cell retained. Fixed 100,000/20261013 specification and sample NPZ arrays inspected. |
| 60 | 50/80/95% coverage, the lower and upper exceedance rates and the widths; | PASS | diagnostics.py inspected: inclusive coverage with width/exceedances, strict/weak hits and eight upper-tie bins, calendar-adjacent Christoffersen tests, fixed moment family. _validate_completed accepted all 936 cells/Holm rows, exact code/protocol/score bindings and 11,388/26,572/30,368 registered calibration cells. 935 moment cells computable, one bound-tie cell retained. Fixed 100,000/20261013 specification and sample NPZ arrays inspected. |
| 61 | quantile hits, and the eight-bin quantile histogram; | PASS | diagnostics.py inspected: inclusive coverage with width/exceedances, strict/weak hits and eight upper-tie bins, calendar-adjacent Christoffersen tests, fixed moment family. _validate_completed accepted all 936 cells/Holm rows, exact code/protocol/score bindings and 11,388/26,572/30,368 registered calibration cells. 935 moment cells computable, one bound-tie cell retained. Fixed 100,000/20261013 specification and sample NPZ arrays inspected. |
| 62 | Christoffersen's tests; | PASS | diagnostics.py inspected: inclusive coverage with width/exceedances, strict/weak hits and eight upper-tie bins, calendar-adjacent Christoffersen tests, fixed moment family. _validate_completed accepted all 936 cells/Holm rows, exact code/protocol/score bindings and 11,388/26,572/30,368 registered calibration cells. 935 moment cells computable, one bound-tie cell retained. Fixed 100,000/20261013 specification and sample NPZ arrays inspected. |
| 63 | the memo's moment-test family (HAC lag 14, 100,000 replicates, seed 20261013, Holm at 5%), as a diagnostic only. | PASS | diagnostics.py inspected: inclusive coverage with width/exceedances, strict/weak hits and eight upper-tie bins, calendar-adjacent Christoffersen tests, fixed moment family. _validate_completed accepted all 936 cells/Holm rows, exact code/protocol/score bindings and 11,388/26,572/30,368 registered calibration cells. 935 moment cells computable, one bound-tie cell retained. Fixed 100,000/20261013 specification and sample NPZ arrays inspected. |
| 64 | **Registered breakdowns:** | PASS | scoring.py registered_breakdown_cells/calendar_groups; diagnostics.py known_price_states, calibration_tables and realized_outcome_slices. Complete registered inventories validated, including unavailable and zero-support cells. State definitions use strictly published complete-day prices, latest-seven support, sample SD of 28 means, preceding 365 SDs, linear percentile and strict comparison; realized slices remain descriptive. |
| 65 | season (DJF, MAM, JJA, SON); | PASS | scoring.py registered_breakdown_cells/calendar_groups; diagnostics.py known_price_states, calibration_tables and realized_outcome_slices. Complete registered inventories validated, including unavailable and zero-support cells. State definitions use strictly published complete-day prices, latest-seven support, sample SD of 28 means, preceding 365 SDs, linear percentile and strict comparison; realized slices remain descriptive. |
| 66 | year and quarter; | PASS | scoring.py registered_breakdown_cells/calendar_groups; diagnostics.py known_price_states, calibration_tables and realized_outcome_slices. Complete registered inventories validated, including unavailable and zero-support cells. State definitions use strictly published complete-day prices, latest-seven support, sample SD of 28 means, preceding 365 SDs, linear percentile and strict comparison; realized slices remain descriptive. |
| 67 | local hour; | PASS | scoring.py registered_breakdown_cells/calendar_groups; diagnostics.py known_price_states, calibration_tables and realized_outcome_slices. Complete registered inventories validated, including unavailable and zero-support cells. State definitions use strictly published complete-day prices, latest-seven support, sample SD of 28 means, preceding 365 SDs, linear percentile and strict comparison; realized slices remain descriptive. |
| 68 | day type: weekday or weekend, the nationwide holiday flag, and 23-, 24- and 25-hour days; | PASS | scoring.py registered_breakdown_cells/calendar_groups; diagnostics.py known_price_states, calibration_tables and realized_outcome_slices. Complete registered inventories validated, including unavailable and zero-support cells. State definitions use strictly published complete-day prices, latest-seven support, sample SD of 28 means, preceding 365 SDs, linear percentile and strict comparison; realized slices remain descriptive. |
| 69 | the 2021–2022 stress label, descriptive; | PASS | scoring.py registered_breakdown_cells/calendar_groups; diagnostics.py known_price_states, calibration_tables and realized_outcome_slices. Complete registered inventories validated, including unavailable and zero-support cells. State definitions use strictly published complete-day prices, latest-seven support, sample SD of 28 means, preceding 365 SDs, linear percentile and strict comparison; realized slices remain descriptive. |
| 70 | two states known at the issue time: | PASS | scoring.py registered_breakdown_cells/calendar_groups; diagnostics.py known_price_states, calibration_tables and realized_outcome_slices. Complete registered inventories validated, including unavailable and zero-support cells. State definitions use strictly published complete-day prices, latest-seven support, sample SD of 28 means, preceding 365 SDs, linear percentile and strict comparison; realized slices remain descriptive. |
| 71 | negative-price risk: any negative hour in the last 7 fully known delivery days; | PASS | scoring.py registered_breakdown_cells/calendar_groups; diagnostics.py known_price_states, calibration_tables and realized_outcome_slices. Complete registered inventories validated, including unavailable and zero-support cells. State definitions use strictly published complete-day prices, latest-seven support, sample SD of 28 means, preceding 365 SDs, linear percentile and strict comparison; realized slices remain descriptive. |
| 72 | high volatility: the standard deviation of the last 28 fully known daily mean prices is above the 90th percentile of the previous 365 such values, using linear percentiles and a strict comparison; | PASS | scoring.py registered_breakdown_cells/calendar_groups; diagnostics.py known_price_states, calibration_tables and realized_outcome_slices. Complete registered inventories validated, including unavailable and zero-support cells. State definitions use strictly published complete-day prices, latest-seven support, sample SD of 28 means, preceding 365 SDs, linear percentile and strict comparison; realized slices remain descriptive. |
| 73 | realized-outcome slices, descriptive only. | PASS | scoring.py registered_breakdown_cells/calendar_groups; diagnostics.py known_price_states, calibration_tables and realized_outcome_slices. Complete registered inventories validated, including unavailable and zero-support cells. State definitions use strictly published complete-day prices, latest-seven support, sample SD of 28 means, preceding 365 SDs, linear percentile and strict comparison; realized slices remain descriptive. |
| 74 | **The bootstrap:** | PASS | inference.py calendar_runs/draw_plan/HAC/studentized kernels/GW/MCS inspected; independent synthetic RNG-continuation tests passed. _validate_completed accepted 15,808 bootstrap endpoints, 208 DM/GW entries and eight MCS cells with hash-bound JSON/NPZ pairs, original unavailable statuses and exact candidate code. Fixed 10,000/20261012, four variants and sample full replicate arrays inspected. |
| 75 | paired, non-circular moving blocks of 14 calendar days, 10,000 replicates, seed 20261012; | PASS | inference.py calendar_runs/draw_plan/HAC/studentized kernels/GW/MCS inspected; independent synthetic RNG-continuation tests passed. _validate_completed accepted 15,808 bootstrap endpoints, 208 DM/GW entries and eight MCS cells with hash-bound JSON/NPZ pairs, original unavailable statuses and exact candidate code. Fixed 10,000/20261012, four variants and sample full replicate arrays inspected. |
| 76 | drawn within calendar-year strata (the three 2020 days join 2021; 2026 is a partial stratum), never across a real gap; | PASS | inference.py calendar_runs/draw_plan/HAC/studentized kernels/GW/MCS inspected; independent synthetic RNG-continuation tests passed. _validate_completed accepted 15,808 bootstrap endpoints, 208 DM/GW entries and eight MCS cells with hash-bound JSON/NPZ pairs, original unavailable statuses and exact candidate code. Fixed 10,000/20261012, four variants and sample full replicate arrays inspected. |
| 77 | studentized, with Bartlett HAC at lag 14. | PASS | inference.py calendar_runs/draw_plan/HAC/studentized kernels/GW/MCS inspected; independent synthetic RNG-continuation tests passed. _validate_completed accepted 15,808 bootstrap endpoints, 208 DM/GW entries and eight MCS cells with hash-bound JSON/NPZ pairs, original unavailable statuses and exact candidate code. Fixed 10,000/20261012, four variants and sample full replicate arrays inspected. |
| 78 | **Sensitivity:** 7- and 28-day blocks, and an unstratified 14-day variant. | PASS | inference.py calendar_runs/draw_plan/HAC/studentized kernels/GW/MCS inspected; independent synthetic RNG-continuation tests passed. _validate_completed accepted 15,808 bootstrap endpoints, 208 DM/GW entries and eight MCS cells with hash-bound JSON/NPZ pairs, original unavailable statuses and exact candidate code. Fixed 10,000/20261012, four variants and sample full replicate arrays inspected. |
| 79 | **Secondary tests:** | PASS | inference.py calendar_runs/draw_plan/HAC/studentized kernels/GW/MCS inspected; independent synthetic RNG-continuation tests passed. _validate_completed accepted 15,808 bootstrap endpoints, 208 DM/GW entries and eight MCS cells with hash-bound JSON/NPZ pairs, original unavailable statuses and exact candidate code. Fixed 10,000/20261012, four variants and sample full replicate arrays inspected. |
| 80 | Diebold–Mariano on daily losses; | PASS | inference.py calendar_runs/draw_plan/HAC/studentized kernels/GW/MCS inspected; independent synthetic RNG-continuation tests passed. _validate_completed accepted 15,808 bootstrap endpoints, 208 DM/GW entries and eight MCS cells with hash-bound JSON/NPZ pairs, original unavailable statuses and exact candidate code. Fixed 10,000/20261012, four variants and sample full replicate arrays inspected. |
| 81 | Giacomini–White, with these instruments: a constant, the lag-1 differential, a weekend flag, and the two states above; | PASS | inference.py calendar_runs/draw_plan/HAC/studentized kernels/GW/MCS inspected; independent synthetic RNG-continuation tests passed. _validate_completed accepted 15,808 bootstrap endpoints, 208 DM/GW entries and eight MCS cells with hash-bound JSON/NPZ pairs, original unavailable statuses and exact candidate code. Fixed 10,000/20261012, four variants and sample full replicate arrays inspected. |
| 82 | the 90% Model Confidence Set, descriptive. | PASS | inference.py calendar_runs/draw_plan/HAC/studentized kernels/GW/MCS inspected; independent synthetic RNG-continuation tests passed. _validate_completed accepted 15,808 bootstrap endpoints, 208 DM/GW entries and eight MCS cells with hash-bound JSON/NPZ pairs, original unavailable statuses and exact candidate code. Fixed 10,000/20261012, four variants and sample full replicate arrays inspected. |
| 83 | **A failed fit or forecast** is scored, on that day, with B0's forecast as the policy's fallback. Fallback days are counted and reported by policy. | PASS | state.py and replay.py inspected: separate native/interval/emitted/intake statuses, complete D−2 once-only error release, historical issuance scale, independent route/policy histories, raw B0 error buffer and direct v1-R CQR. Actual report fallback rows retain 18 nominal v5/D2 and eight no-load v5 fallback dates, zero missing eligible dates; full fixed calendar is retained. No main policy exceeds 1%. |
| 84 | **If B0's own inputs are also unavailable,** the policy fails that day. The failure is counted, and the day is scored as missing in every paired comparison involving that policy. | PASS | state.py and replay.py inspected: separate native/interval/emitted/intake statuses, complete D−2 once-only error release, historical issuance scale, independent route/policy histories, raw B0 error buffer and direct v1-R CQR. Actual report fallback rows retain 18 nominal v5/D2 and eight no-load v5 fallback dates, zero missing eligible dates; full fixed calendar is retained. No main policy exceeds 1%. |
| 85 | **Separate four statuses on every date:** native-central validity, interval readiness, source of the emitted/scored output, and eligibility of the issuance for a complete-day own error. A valid native central and required issuance scale may be stored before its outcome even when fewer than 28 complete released own-error dates force a scored fallback. Its own error may enter once, after complete D−2 release. This applies in warm-up and recovery in measurement. The emitted fallback remains scored and counted as fallback; never revise it retrospectively. | PASS | state.py and replay.py inspected: separate native/interval/emitted/intake statuses, complete D−2 once-only error release, historical issuance scale, independent route/policy histories, raw B0 error buffer and direct v1-R CQR. Actual report fallback rows retain 18 nominal v5/D2 and eight no-load v5 fallback dates, zero missing eligible dates; full fixed calendar is retained. No main policy exceeds 1%. |
| 86 | **This exception is only for insufficient interval history.** Member, solver, identity, required scale or numerical H-construction failure admits no own error. Copied fallback errors, another policy's errors and forecasts constructed after the outcome never enter. v2–v5 and variants retain their landed H recipe and blend weights; gaps lengthen the represented calendar span. | PASS | state.py and replay.py inspected: separate native/interval/emitted/intake statuses, complete D−2 once-only error release, historical issuance scale, independent route/policy histories, raw B0 error buffer and direct v1-R CQR. Actual report fallback rows retain 18 nominal v5/D2 and eight no-load v5 fallback dates, zero missing eligible dates; full fixed calendar is retained. No main policy exceeds 1%. |
| 87 | **B0 retains raw own errors**, with no A1-scale requirement. Warm-up may issue central only. In measurement, if its own valid quantiles are unavailable, B0 has no fallback to itself: retain a missing output under paired-comparison rules while a valid pre-outcome native central continues warming its own raw-error buffer. v1-R retains nine heads, embargoes and CQR; it never substitutes an issued-error H buffer for CQR. | PASS | state.py and replay.py inspected: separate native/interval/emitted/intake statuses, complete D−2 once-only error release, historical issuance scale, independent route/policy histories, raw B0 error buffer and direct v1-R CQR. Actual report fallback rows retain 18 nominal v5/D2 and eight no-load v5 fallback dates, zero missing eligible dates; full fixed calendar is retained. No main policy exceeds 1%. |
| 88 | **If a main policy's fallback days exceed 1% of the calendar,** the Lead reports before CP-28. Every main policy counts, including a tier-3 variant. Delay runs and the revision-contaminated as-landed policies are reported separately. | PASS | state.py and replay.py inspected: separate native/interval/emitted/intake statuses, complete D−2 once-only error release, historical issuance scale, independent route/policy histories, raw B0 error buffer and direct v1-R CQR. Actual report fallback rows retain 18 nominal v5/D2 and eight no-load v5 fallback dates, zero missing eligible dates; full fixed calendar is retained. No main policy exceeds 1%. |
| 89 | **No day leaves the calendar** after scoring. | PASS | state.py and replay.py inspected: separate native/interval/emitted/intake statuses, complete D−2 once-only error release, historical issuance scale, independent route/policy histories, raw B0 error buffer and direct v1-R CQR. Actual report fallback rows retain 18 nominal v5/D2 and eight no-load v5 fallback dates, zero missing eligible dates; full fixed calendar is retained. No main policy exceeds 1%. |
| 90 | **It is a control audit.** For each adopted transition (v2 → v3, v3 → v4, v4 → v5) it reports the paired differences, the ratio intervals and the year and season breakdowns, all descriptive. | PASS | report.md and report.json contain all three descriptive generation contrasts, paired differences/ratio intervals, year/season endpoint records and no adoption decision. Unfavorable never-scored/newly-opened v5 comparisons remain visible. The GFS+6 result is explicitly fragile and referred to the later Owner decision. |
| 91 | **No adoption, replacement or demotion follows from it.** If v5 does not improve on v4 over the full calendar, the record says so, and the control (§24.5) stays CP-28's control. | PASS | report.md and report.json contain all three descriptive generation contrasts, paired differences/ratio intervals, year/season endpoint records and no adoption decision. Unfavorable never-scored/newly-opened v5 comparisons remain visible. The GFS+6 result is explicitly fragile and referred to the later Owner decision. |
| 92 | **Author and timing:** the CP-26 Lead writes it from §24.8, without inspecting any outcome, and commits it on `gauntlet/cp-26` before CP-26 computes its first score. The versioned r14 repair protocol is committed before any new search or training pilot; the prior protocol remains historical, with hash-bound supersession recorded. | PASS | Full cp28-frozen-protocol-v21-r14.md reviewed independently against §24.8: seven arms, causal native ledger, exact grids/ties, A3/A6 and A5/A7 shared fits, weighted meta-learner, separate H buffers, complete failure hierarchy, 20 endpoints, four Holm families and selection. Git history places r14 repair at 563be855d918cb7ec3a2b53497414a863dc43431 before the 42083d9 cold plans/pilot and first scored manifest commit. Original protocol is preserved; custody/Owner-confirmation gates remain prospective. |
| 93 | **Review:** CP-26's Integration Critic reviews it. | PASS | Full cp28-frozen-protocol-v21-r14.md reviewed independently against §24.8: seven arms, causal native ledger, exact grids/ties, A3/A6 and A5/A7 shared fits, weighted meta-learner, separate H buffers, complete failure hierarchy, 20 endpoints, four Holm families and selection. Git history places r14 repair at 563be855d918cb7ec3a2b53497414a863dc43431 before the 42083d9 cold plans/pilot and first scored manifest commit. Original protocol is preserved; custody/Owner-confirmation gates remain prospective. |
| 94 | **Custody:** it lands with CP-26. If CP-26 is discarded, the protocol goes with it. | PASS | Full cp28-frozen-protocol-v21-r14.md reviewed independently against §24.8: seven arms, causal native ledger, exact grids/ties, A3/A6 and A5/A7 shared fits, weighted meta-learner, separate H buffers, complete failure hierarchy, 20 endpoints, four Holm families and selection. Git history places r14 repair at 563be855d918cb7ec3a2b53497414a863dc43431 before the 42083d9 cold plans/pilot and first scored manifest commit. Original protocol is preserved; custody/Owner-confirmation gates remain prospective. |
| 95 | **The Owner's later confirmation** decides only whether CP-28 runs, never what it tests. | PASS | Full cp28-frozen-protocol-v21-r14.md reviewed independently against §24.8: seven arms, causal native ledger, exact grids/ties, A3/A6 and A5/A7 shared fits, weighted meta-learner, separate H buffers, complete failure hierarchy, 20 endpoints, four Holm families and selection. Git history places r14 repair at 563be855d918cb7ec3a2b53497414a863dc43431 before the 42083d9 cold plans/pilot and first scored manifest commit. Original protocol is preserved; custody/Owner-confirmation gates remain prospective. |
| 96 | Every forecast is stored with its issue instant, training-target cutoff, input vintages, seeds and code identity. | PASS | Actual forecast ledger schema/sample day, forecast-completion (2,441 through 2026-09-06), replay-state and learning-ledger route identities inspected; execution.py materialize_day embeds native cache payload/provenance, issue/cutoff/vintage/seed/code identities. state.py/replay.py retain partial-score/full-error/three-native-learning predicates, pending/consumed state, historical scale and per-origin buffer support/span/age. No full scientific replay or regeneration was performed. |
| 97 | Scoring keys permitted by CP-25, a complete canonical day eligible for an own-error buffer, and a complete three-native-member day eligible for CP-28 learning are separate predicates. A partially eligible day stays measured on its frozen keys, without an invented hour, but a partial issuance cannot supply a complete-day error. Full 23/24/25-hour DST dates can. Keep pending issuances, once-only consumption, latest released errors and original issuance scales continuously across warm-up/measurement, search boundaries, failures and restart. Each policy and route owns separate buffers and identity-bound caches. Report buffer counts, oldest/latest dates, span and age. No search transition resets this state. | PASS | Actual forecast ledger schema/sample day, forecast-completion (2,441 through 2026-09-06), replay-state and learning-ledger route identities inspected; execution.py materialize_day embeds native cache payload/provenance, issue/cutoff/vintage/seed/code identities. state.py/replay.py retain partial-score/full-error/three-native-learning predicates, pending/consumed state, historical scale and per-origin buffer support/span/age. No full scientific replay or regeneration was performed. |
| 98 | **400 machine-hours,** summed over workers' wall time, as CP-24's ledger defines it. This includes the warm-up, the parity gate, the searches, the delay runs, the bootstrap, diagnostics, tests and failed jobs. | PASS | budget.py/limits.py/supervisor.py and raw-kernel bootstrap inspected; actual canonical ledger retains baseline 65.16212464012295h, 2,826s original reserve plus other reserves, both run views and closed repair scope. Exact 500h cap, named-run 440h admission, four slots, CPU/BLAS1, 12GB, 3/8/14/.2s deadlines and 38.4s ending exposure preserved. Actual 1,064-probe pilot remains sealed and all 42 pairs are priced; analysis-ready admission PASS projects 298.123743557h. Historical 400h/150–165h/29–34h values are explanatory, superseded operationally by the recorded ruling/r16 authority. |
| 99 | At most 4 concurrent workers; BLAS 1; CPU only; peak memory 12 GB; no cloud and no GPU. | PASS | budget.py/limits.py/supervisor.py and raw-kernel bootstrap inspected; actual canonical ledger retains baseline 65.16212464012295h, 2,826s original reserve plus other reserves, both run views and closed repair scope. Exact 500h cap, named-run 440h admission, four slots, CPU/BLAS1, 12GB, 3/8/14/.2s deadlines and 38.4s ending exposure preserved. Actual 1,064-probe pilot remains sealed and all 42 pairs are priced; analysis-ready admission PASS projects 298.123743557h. Historical 400h/150–165h/29–34h values are explanatory, superseded operationally by the recorded ruling/r16 authority. |
| 100 | **The basis.** The first review projects about 150–165 machine-hours from measured costs per origin. | PASS | budget.py/limits.py/supervisor.py and raw-kernel bootstrap inspected; actual canonical ledger retains baseline 65.16212464012295h, 2,826s original reserve plus other reserves, both run views and closed repair scope. Exact 500h cap, named-run 440h admission, four slots, CPU/BLAS1, 12GB, 3/8/14/.2s deadlines and 38.4s ending exposure preserved. Actual 1,064-probe pilot remains sealed and all 42 pairs are priced; analysis-ready admission PASS projects 298.123743557h. Historical 400h/150–165h/29–34h values are explanatory, superseded operationally by the recorded ruling/r16 authority. |
| 101 | A run of the control costs about 29 hours of fits, and about 34 with its 14 searches (the second review's reconstruction from CP-24's measured costs). | PASS | budget.py/limits.py/supervisor.py and raw-kernel bootstrap inspected; actual canonical ledger retains baseline 65.16212464012295h, 2,826s original reserve plus other reserves, both run views and closed repair scope. Exact 500h cap, named-run 440h admission, four slots, CPU/BLAS1, 12GB, 3/8/14/.2s deadlines and 38.4s ending exposure preserved. Actual 1,064-probe pilot remains sealed and all 42 pairs are priced; analysis-ready admission PASS projects 298.123743557h. Historical 400h/150–165h/29–34h values are explanatory, superseded operationally by the recorded ruling/r16 authority. |
| 102 | Under §24.5's margin table, delay runs are expected to be few or none. | PASS | budget.py/limits.py/supervisor.py and raw-kernel bootstrap inspected; actual canonical ledger retains baseline 65.16212464012295h, 2,826s original reserve plus other reserves, both run views and closed repair scope. Exact 500h cap, named-run 440h admission, four slots, CPU/BLAS1, 12GB, 3/8/14/.2s deadlines and 38.4s ending exposure preserved. Actual 1,064-probe pilot remains sealed and all 42 pairs are priced; analysis-ready admission PASS projects 298.123743557h. Historical 400h/150–165h/29–34h values are explanatory, superseded operationally by the recorded ruling/r16 authority. |
| 103 | **A tier ruling that adds a variant also sets the ceiling it needs:** each variant costs about 70–85 machine-hours, and the ruling records the new ceiling. | PASS | budget.py/limits.py/supervisor.py and raw-kernel bootstrap inspected; actual canonical ledger retains baseline 65.16212464012295h, 2,826s original reserve plus other reserves, both run views and closed repair scope. Exact 500h cap, named-run 440h admission, four slots, CPU/BLAS1, 12GB, 3/8/14/.2s deadlines and 38.4s ending exposure preserved. Actual 1,064-probe pilot remains sealed and all 42 pairs are priced; analysis-ready admission PASS projects 298.123743557h. Historical 400h/150–165h/29–34h values are explanatory, superseded operationally by the recorded ruling/r16 authority. |
| 104 | **A timing pilot comes first:** 14 origins, training only, with scores sealed. The general cumulative admission line is an absolute 436.5 machine-hours. For the existing run `cp26-cold-rerun-2026-10-15-01` only, the Owner-approved exception is **440 machine-hours**. The actual cumulative hard ceiling is **500 machine-hours**. Admission is not recalculated as a fraction of that ceiling. Above the applicable admission line, the Lead stops and reports before the full run. A continuation pilot must price all 42 searches across nominal/no-load/GFS+6, as well as daily fits, parity, tests, failed jobs, bootstrap and diagnostics. Compare total projected expense including historical measured time, reported time and retained reserves with the applicable absolute admission line; 14 daily origins alone do not price searches. Do not reset the ledger. Unreconciled worker duration or surviving orphan blocks new compute; restart idle time is not measured worker time. The earlier repair-only scope (10 new machine-hours within its then-485-hour ceiling, excluding real search/pilot/replay/scores) remains closed; it is not reopened or extended by this continuation. | PASS | budget.py/limits.py/supervisor.py and raw-kernel bootstrap inspected; actual canonical ledger retains baseline 65.16212464012295h, 2,826s original reserve plus other reserves, both run views and closed repair scope. Exact 500h cap, named-run 440h admission, four slots, CPU/BLAS1, 12GB, 3/8/14/.2s deadlines and 38.4s ending exposure preserved. Actual 1,064-probe pilot remains sealed and all 42 pairs are priced; analysis-ready admission PASS projects 298.123743557h. Historical 400h/150–165h/29–34h values are explanatory, superseded operationally by the recorded ruling/r16 authority. |
| 105 | **Outputs:** the ledger; the scores, and the uncertainty with its stored replicates; the diagnostics; the report; CP-28's frozen protocol; and a draft publication packet under PUBLISH_RULES §11. | FAIL | FAIL F1: the outputs exist and their 33,943 custody file hashes validate, but report.md/report.json and publication-packet.md/JSON omit the mandatory CP-25 risk/qualification disclosures. Existence and numeric completeness do not satisfy the complete reporting contract. |
| 106 | **Gates:** | PASS | Prerequisite gate records inspected. Owner LAND/publication remain separate future actions; this Integration review cannot perform or claim them. |
| 107 | CP-25's LAND; | PASS | CP-25 landing record read: land/cp-25 at 5336aef9a4afbd42a952e6e130af38a338a199dc; frozen manifest and recorded rulings remain named by CP-26. |
| 108 | the Owner's tier and margin rulings (§24.5); | FAIL | FAIL F1: the Owner tier/margin rulings are present and implemented, but the report and draft packet omit their required load-history revision risk, tier-2 SMARD caveat, accepted structural margins and never-scored overlap disclosure. |
| 109 | the issued brief; | PASS | Exact cold-run issued-brief.md, registration.json and issued-continuation-v21-r16.md read; active authority/pinned anchor and admission identity match the task. Older resource text is preserved historically, with r16 overriding operational limits only. |
| 110 | the LAND. | NOT DUE | NOT DUE: CP-26 LAND is Owner-only after review. It has not occurred and no completion claim is made; this verdict grants no landing authority. |
| 111 | **Publication:** CP-26's results may be published before 4.7T, under PUBLISH_RULES 1.5's invariant 10. Publishing is a separate decision. | PASS | Local draft packet/MLflow export only; publication status pending, no public route receipt, no publication or CP-28 activation. This review performed no remote access/write and stayed within the 2026-09-06 boundary. |


## Supporting requirements verdicts

| Source | Assessment |
|---|---|
| §§2,24.2,24.4 | PASS: canonical DST keys, new issue offset, strict input boundary, complete D−2 error release and guarded real-input path inspected. Exposure assessments reviewed without reconstructing unknown market content. |
| §§14.1–14.2,15.1–15.3,16.2,17.2–17.3,23.3–23.5/23.10 | PASS: imported landed recipes, fixed blends/H/JSU/direct CQR distinctions, fresh origin caches and exact parity retained; no old fold results overwritten, no retry seeds or missing-component subset blend. Applicable causal/integrity source and retained parity inspected; no full estimator reproduction claimed. Historical checkpoint-specific populations, bootstrap levels and resource caps are superseded for CP-26 where §24.7 explicitly says so; their historical records are not regraded. |
| §24.5 and CP-25 rulings §§1–4 | **FAIL F1 in reporting**; route construction/late-weather treatment and GFS fragility result supported. Required substantive risks/overlap qualifications are absent from generated outputs. |
| §§24.8–24.9 frozen CP-28 | PASS prospective specification/custody review. The specific A4 rule controls: A4 follows A3 until 728; before 364 A3 equals control. No new arm/startup date/selection rule was inferred from outcomes and CP-28 has not run. 4.7T/live audit remains a later gate. |
| PUBLISH_RULES 1.5 §11 and incorporated baseline | **FAIL F1**: local draft packet/typed numbers exist with withheld claims and pending lifecycle identities, but the mandatory input-evidence qualifications are missing. No public/deployment completion is claimed. |

## Remaining risks and scope

The GFS+6 analysis is fragile (+14% MAE, +15% WIS on the rounded reading path); that is an honest result for the Owner's later margin decision and does not cause engineering FAIL. Some inference cells are undefined and one moment cell has forecast-bound ties; their conservative statuses remain stored. No favorable outcome threshold gates this verdict. The known load-history, target-price-vintage, structural-margin and mask-overlap limitations must be disclosed before this reporting artifact can pass. No source or data change is implied by that repair.

Interview-capture trigger: the distinction between a numerically complete analysis and required disclosure of its input-evidence limitations is worth preserving; only the Orchestrator may file it.

## Verbatim complete §24.7

> ### 24.7 CP-26: the re-baseline on every development day (stage 6)
>
> **Purpose:** run B0, v1-R and v2–v5 daily on every eligible development day under one protocol.
> The result is the new all-season baseline, and a stored ledger of every member's out-of-sample
> forecasts for CP-28 and 4.7T.
>
> #### Days
>
> - **The scored calendar:** delivery days 2020-12-29 to 2026-09-06, 2,078 calendar days, less
>   CP-25's frozen exclusions.
> - **The warm-up:** delivery days 2020-01-01 to 2020-12-28, forecast the same way and never scored.
>   It only fills interval buffers and CP-28's first ledger.
> - **Four masks are reported separately:**
>   - every eligible day;
>   - the days never scored before (CP-25's mask);
>   - the old-fold days, folds 2–5, re-run under this protocol;
>   - 2026-04-08 to 2026-09-06, newly opened and used earlier by v1.
>
>   The old five-fold results, their S_MAE and S_WIS and their uncertainty stay as the historical
>   record, never overwritten.
>
> #### Policies
>
> - **B0,** the similar-day naive, unchanged.
> - **v1-R (728-day window, no hindsight regime flags):** the released v1 recipe, refit daily, with
>   two declared method changes:
>   - `crisis_period` and `post_crisis` are removed (§24.5);
>   - the training window is 728 days, where v1 expanded from 2019-01-01.
>
>   The rest of the recipe is the `base` catalog, the nine LightGBM quantile heads, CQR, and isotonic
>   ordering, laid out for each origin D as follows:
>   - the heads train on `[max(2019-01-01, D−728), D−62)`;
>   - day D−62 is an embargo;
>   - CQR calibrates on D−61 to D−2;
>   - day D−1 is an embargo.
>   - The thread count follows the worker's allotment; that is not a method change.
>   - **The released artifact** is reported descriptively, on its holdout days only: 2026-06-09 to
>     2026-09-06.
>   - If v1-R cannot be built without a further method change, CP-26 reports v1 through the released
>     artifact and B1's preserved vectors on the old folds, and says so.
> - **v2, v3, v4 and v5,** through the harness below: their landed member code, fixed blend weights,
>   interval layers, seeds and inner tuning rules, unchanged. Only the data identity, the boundary,
>   the weather source, the issue time and the calendar follow this section.
>   - **A tier-3 ruling** may name a variant, built only by the ruling's declared changes (§24.5).
> - **DDNN-2 alone** is descriptive in CP-26. It is a CP-28 arm (§24.8).
>
> #### The harness and the parity gate
>
> - **The harness.** The landed code refuses any snapshot, boundary or anchor other than its own
>   (`src/cp15/data.py`, `src/cp20/inputs.py`, `src/cp24/inputs.py`). CP-26 therefore builds a
>   harness that imports the landed member code unchanged and replaces only:
>   - the data identity: the new partition specification and CP-25's manifest;
>   - the boundary;
>   - the weather source: CP-20's grids plus CP-25's;
>   - the issue-time label;
>   - the identity pins: the protocol revision, the anchor and issued-document hashes, and the lineage
>     checks. Each replaced pin is listed in the harness log.
> - **The parity gate, before the full run.** Under the old settings (11:00 UTC, the old identity and
>   boundary), the harness reproduces the committed central vectors bitwise at sampled old-fold
>   origins:
>   - for A1, B2, A1_w, B2_w, L-N and L-R;
>   - for D2, on CP-24's committed ensembles. Those ensembles check parity only, and never serve a
>     CP-26 forecast;
>   - for B0, and for the assembled v2–v5 central vectors.
>
>   If parity fails, the Lead stops and reports.
>
> #### DDNN-2's training-only search, for CP-26
>
> - **Search dates:** S_k = 2020-01-15 + 182k days, for k = 0 to 13. Search k serves only the origins
>   from S_k up to the day before S_(k+1). Before S_0 there is no native D2 forecast.
> - **The batches:** consecutive 28-day blocks, tiling backward from S_k − 1.
>   - Among blocks starting on or after 2019-07-01, keep up to the 11 newest eligible blocks.
>   - Use exactly the landed DDNN-2 support mask, complete-calendar-week pool and 20% holdout-week
>     count, retaining its exclusion of the most recent seven days. Let N be the supported window
>     days and m the fixed held-out week count. Minimum training support is N minus the sum of the
>     m largest week supports; minimum holdout support is the sum of the m smallest. Accept only
>     minima at least 250 and 14 respectively. Eligibility must hold for every possible split.
>   - Lists depend only on support, are shared by every configuration in a search and are signed
>     before fitting. No seed, loss or convergence filters them. B is computed, never hard-coded:
>     the expected reproduction is [1,7,11,…,11], with first block 2019-12-18..2020-01-14 and minima
>     251/46. The algorithm and frozen inputs govern if a reported count disagrees.
>   - There is no fold skip rule: every block lies before the search's first origin.
> - **One fit per trial and batch,** on `[max(2019-01-01, b − 728), b)`.
> - **The sampler:** seeded with `SeedSequence([26, k, 0x5A3])`, with 128 trials. Successive halving,
>   the ranking metric and the tie rule follow §23.4.
> - **Frozen fit seeds:** trial/batch seed = `26_000_000 + k*100_000 + trial*100 + batch`,
>   trial=0..127 and retained batch=0..10, newest first. Ensemble member seed =
>   `26_000_000 + k*100_000 + 90_000 + 10*rank + repeat`, rank=1..4 and repeat=1..2.
>   These disjoint domains are fixed before fitting and shared across the three routes; no retries
>   with replacement seeds. Sampling space/priors remain the landed permitted space.
> - **The ensemble:** four best distinct effective configurations, two seeds each, exactly eight
>   members. Effective identity excludes trial id; in the no-load variant it also excludes removed
>   load flags. Duplicates consume trials; no extra sampling compensates for them. A configuration
>   failing a required batch cannot rank over all batches.
> - **Search failure:** zero eligible blocks or fewer than four valid effective configurations is
>   recorded. D2 is unavailable throughout that search's service period; the next search remains
>   on schedule. Never extend an earlier ensemble or relax a threshold. One failed daily member
>   invalidates D2 for that date: no median of a successful subset.
> - **CP-24's ensembles are never reused** for a CP-26 forecast.
>
> #### Training and information
>
> - **A daily refit** at every origin, for every member, on `[max(2019-01-01, D−728), D)`, filtered
>   by availability at the issue time. For every scored day the window is exactly 728 days.
> - **A training target enters only once its price was published** before the issue time.
> - **No expanding-window sensitivity** is run under the short path.
>
> #### Scores
>
> - **Primary:**
>   - p50 MAE, and the seven-quantile WIS (50/80/95% intervals, weights α/2, median weight 1/2,
>     divided by 3.5);
>   - each day's loss is the mean over its actual hours, and days weigh equally;
>   - the B0 ratio is the policy's mean daily loss over B0's, reported beside the raw losses.
> - **Secondary:**
>   - the mean of the four pooled-season ratios;
>   - the mean of the five complete-year ratios, 2021 to 2025;
>   - 2020 and 2026, both partial, reported separately; quarters descriptive.
> - **Calibration, descriptive:**
>   - 50/80/95% coverage, the lower and upper exceedance rates and the widths;
>   - quantile hits, and the eight-bin quantile histogram;
>   - Christoffersen's tests;
>   - the memo's moment-test family (HAC lag 14, 100,000 replicates, seed 20261013, Holm at 5%), as
>     a diagnostic only.
> - **Registered breakdowns:**
>   - season (DJF, MAM, JJA, SON);
>   - year and quarter;
>   - local hour;
>   - day type: weekday or weekend, the nationwide holiday flag, and 23-, 24- and 25-hour days;
>   - the 2021–2022 stress label, descriptive;
>   - two states known at the issue time:
>     - negative-price risk: any negative hour in the last 7 fully known delivery days;
>     - high volatility: the standard deviation of the last 28 fully known daily mean prices is above
>       the 90th percentile of the previous 365 such values, using linear percentiles and a strict
>       comparison;
>   - realized-outcome slices, descriptive only.
>
> #### Inference
>
> - **The bootstrap:**
>   - paired, non-circular moving blocks of 14 calendar days, 10,000 replicates, seed 20261012;
>   - drawn within calendar-year strata (the three 2020 days join 2021; 2026 is a partial stratum),
>     never across a real gap;
>   - studentized, with Bartlett HAC at lag 14.
> - **Sensitivity:** 7- and 28-day blocks, and an unstratified 14-day variant.
> - **Secondary tests:**
>   - Diebold–Mariano on daily losses;
>   - Giacomini–White, with these instruments: a constant, the lag-1 differential, a weekend flag,
>     and the two states above;
>   - the 90% Model Confidence Set, descriptive.
>
> #### Failures
>
> - **A failed fit or forecast** is scored, on that day, with B0's forecast as the policy's fallback.
>   Fallback days are counted and reported by policy.
> - **If B0's own inputs are also unavailable,** the policy fails that day. The failure is counted,
>   and the day is scored as missing in every paired comparison involving that policy.
> - **Separate four statuses on every date:** native-central validity, interval readiness, source
>   of the emitted/scored output, and eligibility of the issuance for a complete-day own error.
>   A valid native central and required issuance scale may be stored before its outcome even
>   when fewer than 28 complete released own-error dates force a scored fallback. Its own error
>   may enter once, after complete D−2 release. This applies in warm-up and recovery in measurement.
>   The emitted fallback remains scored and counted as fallback; never revise it retrospectively.
> - **This exception is only for insufficient interval history.** Member, solver, identity, required
>   scale or numerical H-construction failure admits no own error. Copied fallback errors, another
>   policy's errors and forecasts constructed after the outcome never enter. v2–v5 and variants
>   retain their landed H recipe and blend weights; gaps lengthen the represented calendar span.
> - **B0 retains raw own errors**, with no A1-scale requirement. Warm-up may issue central only.
>   In measurement, if its own valid quantiles are unavailable, B0 has no fallback to itself:
>   retain a missing output under paired-comparison rules while a valid pre-outcome native central
>   continues warming its own raw-error buffer. v1-R retains nine heads, embargoes and CQR;
>   it never substitutes an issued-error H buffer for CQR.
> - **If a main policy's fallback days exceed 1% of the calendar,** the Lead reports before CP-28.
>   Every main policy counts, including a tier-3 variant. Delay runs and the revision-contaminated
>   as-landed policies are reported separately.
> - **No day leaves the calendar** after scoring.
>
> #### What CP-26 claims
>
> - **It is a control audit.** For each adopted transition (v2 → v3, v3 → v4, v4 → v5) it reports
>   the paired differences, the ratio intervals and the year and season breakdowns, all
>   descriptive.
> - **No adoption, replacement or demotion follows from it.** If v5 does not improve on v4 over the
>   full calendar, the record says so, and the control (§24.5) stays CP-28's control.
>
> #### CP-28's frozen protocol
>
> - **Author and timing:** the CP-26 Lead writes it from §24.8, without inspecting any outcome, and
>   commits it on `gauntlet/cp-26` before CP-26 computes its first score.
>   The versioned r14 repair protocol is committed before any new search or training pilot;
>   the prior protocol remains historical, with hash-bound supersession recorded.
> - **Review:** CP-26's Integration Critic reviews it.
> - **Custody:** it lands with CP-26. If CP-26 is discarded, the protocol goes with it.
> - **The Owner's later confirmation** decides only whether CP-28 runs, never what it tests.
>
> #### The ledger
>
> Every forecast is stored with its issue instant, training-target cutoff, input vintages, seeds and
> code identity.
>
> Scoring keys permitted by CP-25, a complete canonical day eligible for an own-error buffer,
> and a complete three-native-member day eligible for CP-28 learning are separate predicates.
> A partially eligible day stays measured on its frozen keys, without an invented hour, but a
> partial issuance cannot supply a complete-day error. Full 23/24/25-hour DST dates can.
> Keep pending issuances, once-only consumption, latest released errors and original issuance
> scales continuously across warm-up/measurement, search boundaries, failures and restart.
> Each policy and route owns separate buffers and identity-bound caches. Report buffer counts,
> oldest/latest dates, span and age. No search transition resets this state.
>
> #### Ceilings, proposed
>
> - **400 machine-hours,** summed over workers' wall time, as CP-24's ledger defines it. This
>   includes the warm-up, the parity gate, the searches, the delay runs, the bootstrap, diagnostics,
>   tests and failed jobs.
> - At most 4 concurrent workers; BLAS 1; CPU only; peak memory 12 GB; no cloud and no GPU.
> - **The basis.** The first review projects about 150–165 machine-hours from measured costs per
>   origin.
>   - A run of the control costs about 29 hours of fits, and about 34 with its 14 searches (the second
>     review's reconstruction from CP-24's measured costs).
>   - Under §24.5's margin table, delay runs are expected to be few or none.
>   - **A tier ruling that adds a variant also sets the ceiling it needs:** each variant costs about
>     70–85 machine-hours, and the ruling records the new ceiling.
> - **A timing pilot comes first:** 14 origins, training only, with scores sealed. The general
>   cumulative admission line is an absolute 436.5 machine-hours. For the existing run
>   `cp26-cold-rerun-2026-10-15-01` only, the Owner-approved exception is **440 machine-hours**.
>   The actual cumulative hard ceiling is **500 machine-hours**. Admission is not recalculated
>   as a fraction of that ceiling. Above the applicable admission line, the Lead stops and reports
>   before the full run. A continuation pilot must price
>   all 42 searches across nominal/no-load/GFS+6, as well as daily fits, parity, tests, failed jobs,
>   bootstrap and diagnostics. Compare total projected expense including historical measured
>   time, reported time and retained reserves with the applicable absolute admission line;
>   14 daily origins alone do not price searches.
>   Do not reset the ledger. Unreconciled worker duration or surviving orphan blocks new compute;
>   restart idle time is not measured worker time. The earlier repair-only scope (10 new
>   machine-hours within its then-485-hour ceiling, excluding real search/pilot/replay/scores)
>   remains closed; it is not reopened or extended by this continuation.
>
> #### Outputs, gates and publication
>
> - **Outputs:** the ledger; the scores, and the uncertainty with its stored replicates; the
>   diagnostics; the report; CP-28's frozen protocol; and a draft publication packet under
>   PUBLISH_RULES §11.
> - **Gates:**
>   - CP-25's LAND;
>   - the Owner's tier and margin rulings (§24.5);
>   - the issued brief;
>   - the LAND.
> - **Publication:** CP-26's results may be published before 4.7T, under PUBLISH_RULES 1.5's
>   invariant 10. Publishing is a separate decision.


## Exact supporting extracts, verified against the pinned anchor

# CP-26 exact r16 supporting requirements

Verbatim extracts from capstone_v21.md at 4766a61cb0c836573406f5a9729997d1b6ee9862. Complete §24.7 remains in complete-bar-v21-r16.md. No requirement is narrowed by this packet.

## Supporting section 2

> ## 2. The forecasting task and information boundary
>
> Keep DE-LU hourly day-ahead prices as the target. A delivery date D contains its actual 23/24/25
> canonical hours. Do not change the market, horizon, aggregation or target to improve a score.
> Use the inherited v1 forecast-origin convention and eligibility contract. Record its exact
> timezone, UTC instants and DST handling in the protocol; do not silently reinterpret “CET”.
>
> Every predictor, normalization statistic and training target must have been available at its
> historical forecast origin. Preserve the delivery-day masking test (exactly zero change) and
> an available D-1 price mutation that moves an appropriate controlled forecast. Preserve refusal
> of post-gate A69 and target-day actual columns. Preprocessing is part of this boundary.
>
> For online forecast-error updates retain the conservative **complete delivery day D-2** release
> rule, including 23/24/25-hour completeness. Consume each issued forecast/error pair once only.
> Do not infer permission to use D-1 feedback from permission to use D-1 price predictors.
> Report the delay as a policy restriction, not a universal claim about auction information.


## Supporting section 14

> ## 14. CP-16 — bounded existing-input v2 research experiment
>
> **Complete specification/checklist remain ratified; CP-16 resumption authorized 2026-09-23.**
> O1–O3 remain controlling except the expressly amended §14.5 cap/counting rule in v21-r3.
> The resumption grant is recorded above. No new product gate is substituted for §8.
>
> Forecast origin: **D−1 11:00 UTC (12:00 fixed UTC+01:00 CET)**; delivery dates/hours use
> **Europe/Berlin**, including 23/24/25-hour days. Inputs retain the **2019-01-01** floor.
> Complete released errors are from days **≤D−2**, consumed once under the inherited contract.
>
> Delivery: a local research artifact evaluating both point and interval forecasts for the
> Owner/technical reader, as an intermediate step toward the programme's live-system objective.
> No commercial exposure, service-level, operational, economic-qualification or promotion claim.
> The candidate scope is fixed; negative and mixed results are valid research outcomes.
> The existing live-system objective and separate future-stage requirements remain unchanged.
>
> The Lead owns routine engineering fields E1–E4 within this scope, without per-parameter
> Owner decisions. It freezes the exact protocol before comparison; it cannot change a
> scientific contrast, ceiling or quality rule after seeing results. Material changes or
> insufficient allowances require an explicit report rather than silent scope reduction.
>
> ### 14.1 Policies, population and information
>
> - **V2-H:** 50/50 mean of genuine issued A1/B2 **central** forecasts, plus the new hour-aware
>   standardized signed-residual quantiles below. Do not average already calibrated p50s.
> - **V2-P:** exactly the same central forecasts, scale, issued-error history, warm-up,
>   target keys, quantile convention and failure policy; use the pooled residual quantiles.
>   The only changed element is hour-aware pooling/shrinkage.
> - **Saved references:** B0, B1, B2, A1; also B3 strictly to report all original §8 comparator
>   conditions. No new B3 fit or new challenger. Preserve B1's calibrated/projected seven
>   quantiles and original v1 nine-quantile pinball as distinct evidence.
> - Compare all seven output policies on the original **10,747** target keys each:
>   fold counts **2,160 / 2,159 / 2,112 / 2,160 / 2,156**. Successful complete output totals
>   **75,229** policy-target rows. Five 90-calendar-day windows are
>   2020-07-01..09-28, 2021-04-01..06-29, 2022-07-01..09-28,
>   2025-05-01..07-29, and 2026-01-08..04-07. Full fold 3 has 2,112 hours/88 represented
>   days; the peak is **2022-08-15..31, 408 hours/17 days**. Never interchange their denominators.
> - Component recipes, 168-hour normalization, daily rolling fits and four-penalty chronological
>   inner selection remain those in `reports/cp15/protocol.json`; long training history is
>   `[max(2019-01-01,D−728 calendar days),D)`, subject to each origin's availability filter.
>   No model/feature/penalty search beyond this inherited component procedure.
> - Filter permitted partitions **before materializing inputs**. No spent holdout, reserved tail,
>   added market history, post-gate A69, delivery-day actual predictors, or new source admission.
>   Outer outcomes can enter later prescribed error updates only after the fixed release rule;
>   they never tune the recipe. Preserve inherited A65 vintage-availability and historical
>   data-revision assumptions as limitations, not new measured guarantees.
>
> ### 14.2 Causal residual construction and fallback
>
> Owner-ratified recipe: for every genuinely issued blend forecast `c_t`, store
> `r_t = (y_t − c_t) / s_t`, where `s_t` is **that issuance's** A1 scale: sample SD of the
> 168 then-available canonical prices, floored at 1 EUR/MWh. At issuance use the current
> available `s_D`; never normalize old residuals with today's scale. Both arms use this
> same convention, including B2's contribution to the blend.
>
> Retain the most recent **28 complete released delivery days** of blend errors, all ≤D−2.
> This inherits CP-15's complete-day convention; it can span more than 28 calendar dates
> across gaps. Preserve both canonical repeated-hour observations on a 25-hour day, grouped
> by their Europe/Berlin local hour; never synthesize the missing spring hour or deduplicate
> UTC timestamps. Update each issued pair exactly once. Report buffer age and represented
> calendar span as well as counts.
>
> For each quantile `q` in `.025/.10/.25/.50/.75/.90/.975`, compute linear empirical quantiles
> using the CP-15 `numpy.quantile(method=linear)` convention:
>
> - `Q_P(q)`: all canonical hourly residuals in the shared buffer, equal observation weights.
> - `Q_h(q)`: residuals from local hour h in that same buffer.
> - `w_h = n_h / (n_h + 56)`, where `n_h` is the number of canonical errors at h.
>   If h has fewer than **14 distinct complete delivery days**, set `w_h=0`.
> - V2-H emits `c_D,h + s_D * [w_h Q_h(q) + (1−w_h) Q_P(q)]`;
>   when `w_h=0`, use `Q_P` directly without evaluating an empty `Q_h`.
>   V2-P emits `c_D,h + s_D * Q_P(q)`.
>
> The fixed 56 pseudo-observation weight gives roughly one-third hour-specific contribution
> at 28 errors/hour. It is a conservative regularization choice motivated by sparse tails,
> **not an optimized value or a coverage guarantee**. Convex combinations of ordered quantile
> functions preserve order. No tail clipping, isotonic repair or fixed-p50 reset is proposed;
> both arms' final p50 includes their own residual median and must be scored as emitted.
>
> Validate the one fixed recipe on a **training-only** admission slice: seven delivery dates
> D0−8..D0−2 before each fold's first evaluation day D0. It is an implementation/support
> check, not a score-selected configuration search. Freeze it before any new outer scoring;
> if it cannot run causally or lacks support, return the deficiency rather than try a new
> shrinkage value. These older dates are not claimed to be project-unseen evidence.
>
> Generate/reuse genuine component forecasts from at most the preceding **60 calendar dates**
> per fold, continuing daily through the evaluation end. This allowance includes the admission
> slice and its own 28-day warm-up. Identify the required dates in E1 before fitting. No
> in-sample residuals or hindsight-refitted predictions can fill the buffer. Cached component
> forecasts are usable only with verified input/protocol/origin identity and independent
> representative reproduction; a cache miss counts as a budgeted refit.
>
> **Failure rule:** with fewer than 28 complete released forecast days, nonfinite component
> output, missing required input or failed component fit, record failed issuance and its cause;
> there is no stale-component, B0 or zero-error substitution. An incomplete new day cannot enter
> the residual buffer; existing valid complete days may remain under the fixed 28-day rule.
> Any lost original eligible target prevents a complete evaluation/PASS. Retain expected keys,
> failed-row accounting and any explicitly partial summaries without inventing a full score or
> silently shrinking denominators. The per-hour small-sample fallback is the pooled layer,
> not a fallback for missing common history.
>
> ### 14.3 Metrics, diagnostics and causal controls
>
> Re-score emitted p50 MAE and seven-quantile WIS with CP-15's interval weights alpha/2,
> median weight 1/2, divisor 3.5; equally average the five fold ratios to B0. Preserve pooled
> hour-weighted scores as secondary estimands. Also report all CP-15 §7 metrics: RMSE,
> central versus emitted MAE, centering effect, 50/80/95% coverage and width summaries,
> tail misses, bias, daily level/shape error, crisis recovery, failures, runtime and memory.
> Report every original §8 criterion with actual values and limits, including B0–B3 and
> rolling B2/B3 diagnostic comparators; old CP-15 results remain unchanged.
>
> Report per-hour and exhaustive local-time blocks **night 22–05, solar 10–16, shoulder
> 06–09 plus 17–21**, with actual counts, represented dates, hits and widths. Owner-approved support
> rule for block/hour uncertainty statements: at least **56 represented dates** within a fold;
> below that, publish descriptive counts but label the comparison support-limited. This is a
> reporting convention (two buffer lengths), not a power calculation or a new product gate.
> Peak results remain descriptive because there are only 17 days. No demand for nominal-tail
> accuracy is inferred from 28 per-hour errors.
>
> Required controls, each with a positive control that can fail: delivery-day price mutation
> changes forecasts by exactly 0.0; an available D−1 mutation moves a controlled forecast;
> post-gate/target-actual rejection; D−1 error rejection versus D−2 released acceptance;
> consume-once/idempotency, no partial-day buffer admission, 23/24/25-hour UTC identity,
> row-specific scale and training-only transforms, genuine warm-up provenance, state persistence
> and restart replay, stale/wrong cache refusal, expected-row completeness, finite ordered
> quantiles, and common central/buffer parity across H/P. Include sparse-hour fallback and
> linear-quantile/tie fixtures. Re-run applicable existing regression and live-namespace guards
> without making a live mutation. Test execution and code inspection belong to the executing Lead
> and Critic, not to this Orchestrator recording task.
>
> ### 14.4 Research conclusions and uncertainty — ratified O2 contract
>
> Use seed **15042**, **2,000** paired noncircular **7-calendar-day** moving-block bootstrap
> replicates within each full 90-date fold, concatenating/truncating to 90 dates. Resample
> identically across policies, retaining all hours in each selected day and preserving missing
> calendar dates as missing. Recompute both policy and B0 means within each resampled fold,
> then equal-fold normalized score differences. Report 95% percentile intervals; never substitute
> zero loss or epsilon for missing/zero denominators. An undefined replicate or comparison is
> reported as unresolved uncertainty, not silently discarded/redrawn for a favorable result.
>
> Primary contrast: **H−P** for S_WIS and S_MAE. Secondary contrasts: **H−B2** and **P−B2**
> for those same scores. Per-fold paired daily-loss uncertainty remains descriptive. All
> intervals are exploratory post-selection, without family-wise or confirmatory claims.
>
> - Rank H/P descriptively by lower S_WIS, then S_MAE, then **P** on exact ties (simpler layer).
>   Rank is not a statistically supported winner or a delivery decision.
> - State **observed joint improvement** for a contrast only when the S_WIS difference's
>   upper interval endpoint is <0 and the S_MAE difference's upper endpoint is ≤0.
>   This zero-change reference tests improvement without inventing a tolerated point-loss margin.
> - Mixed point/interval outcomes, intervals spanning zero or support failures produce
>   **no demonstrated joint preference**, with both metrics shown; no post-hoc tradeoff weight.
>   This is not proof of equivalence, absence of benefit or absence of harm. Report the
>   direction, magnitude and uncertainty of mixed outcomes explicitly.
> - Engineering completion is independent of gain. A complete valid negative comparison can
>   earn Engineering PASS. Historical CP-15 remains NOT_DEMONSTRATED. A newly evaluated
>   policy's original-§8 diagnostic is reported separately as met/not met/unassessed; under
>   this research-only route it does not itself authorize promotion, CP-17 or publication.
>
> No new economic calculation, decision optimizer, annualization or net-value gate is included.
> Historical economics can be cited only with its original population, assumptions and
> post-selection limitations. A material change to this approved economic scope requires Owner authorization and
> a complete economic-policy contract before execution; do not insert a battery configuration as an unapproved default here.
>
> ### 14.5 Owner-approved numerical ceilings — v21-r3 resumption authorized
>
> These are Owner-approved maximum allowances, **not spending targets, measured costs or
> validated runtime estimates**. The CP-16 resumption grant is recorded above. Charge warm-up,
> inner fits, controls, failures, corrections and independent reproduction to their applicable
> counters under the rule below; carry forward every historical debit. Stop
> on the first exhausted hard cap; retain evidence and return BLOCKED/INCOMPLETE as appropriate.
> No model-quality-driven repeat, automatic retry, new family or automatic increase is allowed.
>
> | Dimension | Approved total cap / counting unit |
> |---|---|
> | New output policies | **2**: H and P; **5** saved reference policies; **7** scored policies total |
> | New residual configurations / selection trials | **1** hour-aware recipe + **1** fixed pooled control; **0** alternative residual configurations or outer-score selection trials |
> | Central configurations / feature recipes | **2** inherited component configurations (A1/B2), **1** common inherited LEAR feature recipe with prescribed raw/normalized representations, **0** new feature recipes |
> | Seeds / ensemble members | **1** inherited model seed, 42; **1** bootstrap seed, 15042; **2** fixed component members per output; **0** seed ensembles |
> | Training-only residual admission | **7** interval-issuance dates × **5** folds × **2** output policies = **70** policy-days, within the replay allowance |
> | Unique component forecast dates | At most **150** per fold (90 evaluation + 60 preceding) × **5** folds; **750** date-fold keys |
> | Main component fitting | At most **1,500** component-day fitting attempts (750 × 2), cache hits require no new fit |
> | Total component fitting, including controls/review/failures | **2,000** component-day attempts, including the 1,500 above; remaining **500** cover representative reproduction, controls and necessary defect repair, not a second full model comparison |
> | Primitive estimator fits / inherited selection | **240,000** Lasso fit attempts total: 2,000 × 24 hours × (4 inner penalties + 1 final refit). At most **192,000** inner-penalty trials and **48,000** final hourly refits, both subsets of that total. Early failure still counts; a smaller fixture does not create extra attempts. |
> | Residual replay / regeneration | At most **6** full-equivalent H/P passes, **9,000** cumulative policy-days total (750 × 2 × 6), including admission, diagnostics, controls, corrections and independent review; **0** extra scored recipes |
> | Saved-reference processing | At most **3** metric-only complete passes across **5** saved reference policies; **0** B0/B1/B3 model refits or new reference calibration |
> | Bootstrap / uncertainty | **1** joint 2,000-replicate index set for planned contrasts per analysis pass; at most **3** analysis passes including independent verification; no seed search |
> | Compute | **24 machine-hours**, aggregate elapsed execution time of all compute jobs on this one local machine, summed across simultaneous jobs; includes tests/reproduction and failed jobs, excludes human idle time; **4** CPU workers maximum, BLAS threads **1**, **0** GPU/cloud jobs |
> | Active human/agent effort | Approximate checkpoint timebox **32 hours**; separate hard ceiling **40 active hours**, including protocol, implementation, corrections and review. No unlimited extension at the approximate timebox. |
> | Memory / storage | **10 GiB** aggregate process-tree resident memory; **20 GiB** additional disk including worktrees, environments, caches and outputs; **0 bytes** of new dataset/model downloads |
> | Other work / cost | **0** new sources/providers, weather probes, neural candidates, VRE fits, recombination searches, economic runs, operational days, automated schedules or remote mutations; **$0** external cost |
>
> **Forward-looking counting rule — Owner-ratified v21-r3, 2026-09-23.**
>
> Purely synthetic fixture and state tests, which use no real research data, are charged to
> the compute, memory, storage and effort ceilings but not to the policy-day counter.
>
> Forecast/state replay using real research data remains charged to the policy-day counter
> using the existing policy-day unit, including warm-up, controls, failed attempts and
> independent reproduction. Calling a replay a “test” does not exempt it.
>
> Model fitting remains charged to the existing component-day and primitive-fit counters.
> This amendment neither changes those units nor creates an additional policy-day charge for
> each primitive estimator fit. Real-data replay performed alongside fitting still incurs its
> applicable replay charge.
>
> The historical **3,730** debit stands in full under its original accounting basis and is not
> re-scored under this rule. The revised cumulative ceiling therefore leaves **5,270** policy-days
> for subsequent work under the revised counting rule. Every other resource debit is preserved.
> This change is forward-looking. It does not retroactively establish compliant accounting or
> monitoring, and it grants no reset. The allowance is a maximum, not a spending target or a
> guarantee of feasibility.
>
> **Resumption conditions.** Before further experimental execution, the Lead checks that all
> remaining work fits the revised accounting and every other remaining allowance, and reports
> the estimate, including admission, production, necessary controls and independent verification.
> Historical monitoring gaps remain disclosed. Regenerate evidence from inadequately monitored
> work wherever it is required to support scored results or acceptance criteria. Preserve the
> original evidence and its limitations; later monitoring does not prove historical compliance.
> Preserve the existing candidate branch, evidence, independent FAIL verdict and all debits;
> resume the existing checkpoint, without discarding it or restarting from scratch. The Lead
> owns feasibility, resource allocation, monitoring repairs and independently verified completion
> within this scope; these are execution responsibilities, not further Owner parameter decisions.
> The required independent Integration review and complete acceptance criteria remain unchanged;
> no scientific result is inferred from the interrupted attempt. Weather admission under
> programme §4.1 is not a prerequisite for this resumption.
>
> The fit counts are arithmetic envelopes from the inherited 24-hour/four-penalty recipe,
> not a claim that every origin needs refitting or that the caps suffice. E1 must enumerate
> actual origins and count primitive calls before launch. If adequate genuine warm-up or required
> verification cannot fit within these limits, return a scoped blocker; do not drop hours,
> change history or spend an unstated allowance. Distinct caps are simultaneous, not additive.
> The Lead chooses work decomposition and how to allocate the totals; no fixed review-round
> count is imposed. Corrections require disclosure, preserved invalid evidence and a fresh
> exact-candidate review; they do not permit outcome-guided scientific tuning.
>
> ### 14.6 Engineering completion fields — Lead-owned, no new Owner ballots
>
> | ID | Field to freeze under the adopted scope | Completion rule |
> |---|---|---|
> | **E1 — ENGINEERING PRE-RUN** | Exact permitted partition/key manifest, seven-day admission dates, ≤60-day warm-up dates, cache identity, fit/replay counts and missing-data feasibility | Resolve from metadata and permitted training data before comparison; verify support and totals against §14.5. Missing cache is not authority for extra fits. |
> | **E2 — ENGINEERING PRE-RUN** | Dependency/code/input hashes, numerical fixtures/tolerances, output schema and exact reproduction commands | Pin inherited recipes and the approved H/P procedure; training-only validation, no new outer-score selection. Refuse discrepancies rather than silently changing the scientific contract. |
> | **E3 — ENGINEERING PRE-RUN** | Resource instrumentation, preflight disk/RAM availability, cutoff/abort implementation and atomic evidence saves | Establish how all attempts/jobs count against caps before the first fit; exceeding a cap cannot be hidden by restarting a process. |
> | **E4 — ENGINEERING REVIEW IDENTITY** | Lead session identity and a fresh independent Integration Critic's session identity; exact final candidate SHA and detached worktree | Accountable executor is the **Track B Engineering Lead for CP-16**; reviewer is its **independent CP-16 Integration Critic**. The Lead assigns the actual sessions under its role; the Orchestrator does not launch them. Reviewer independence and identities must be recorded, not invented in 4.0a. |
>
> E1–E4 belong to the Lead within the approved scope and ceilings. Complete the prescribed
> pre-run feasibility/accounting checks before their dependent fits/comparison. Report a
> material scope change or insufficient allowance explicitly; do not return routine engineering
> parameters to the Owner for approval or silently weaken the experiment to fit a ceiling.
>
> ### 14.7 Paths, isolation and immutable inputs
>
> | Purpose | Authorized CP-16 path envelope |
> |---|---|
> | New engineering namespace, tests and driver | `src/cp16/`, `tests/cp16/`, `scripts/cp16_v2.py`; exact internal organization belongs to the Lead |
> | Dependency consistency if needed | `pyproject.toml`, `uv.lock`; inherit existing stack by default, no model/data downloads |
> | Durable protocol and lineage | `reports/v2-causal/protocol.json`, `input-manifest.json`, `lineage.json`, `artifact-manifest.json` |
> | Durable experiment outputs | `reports/v2-causal/predictions.parquet`, `metrics.csv`, `diagnostics.csv`, `uncertainty.csv`, `criteria.csv`, `failures.csv`, `resources.json`, `report.md`, `reproduce.md` |
> | Independent evidence and terminal return | `docs/track-b/evidence/cp-16/integration.md`, other review evidence within `docs/track-b/evidence/cp-16/`, `checkpoint-return.md` in that directory |
> | Checkpoint-local ignored material | `.local/worktrees/cp-16/`, `.local/artifacts/cp-16/`, `.local/tmp/cp-16/`; no sole copy of required evidence here |
> | Supplied immutable governance packaging | Exact ratified `capstone_v21.md`, named amendment record, `docs/track-b/cp-16-v2-brief.md`; only expressly authorized byte-for-byte inclusion on the isolated candidate branch |
>
> Preserve `src/cp15/`, `reports/cp15/`, prior evidence, v1 models/data/report/public surfaces,
> all other locked documents, Q&A and unrelated pending work. Reuse by import/read without
> altering them. All outputs are local. The disposable branch is **`gauntlet/cp-16`**,
> retained for this authorized resumption, declared with its worktrees in the return.
> Only the Lead writes checkpoint Git history. No branch/worktree/tag is created during this recording task.
>
> The Owner authorized CP-16 resumption on its existing candidate branch, including local
> candidate/evidence commits and byte-for-byte packaging of the supplied v21-r3 anchor,
> `docs/track-b/capstone_v21-r2-to-v21-r3-amendments.md` and issued CP-16 brief. Preserve the
> previous immutable documents in the existing commit history. The Lead may not author locked
> documents, amend its own bar, copy unrelated pending work or stage `progress.md`. This scoped
> suspension ends at the Orchestrator's return and does not transfer to the Lead; the resumption
> grant persists within §14.5, the issued brief and engineering-role boundaries.
>
> ### 14.8 Complete CP-16 acceptance checklist
>
> Every item is mandatory. Engineering PASS does not require a positive research finding; it
> does require a complete valid evaluation and fresh binding Integration PASS.
>
> 1. Verify actual repository/input state and preserve other sessions' work and all v1/CP-15
>    evidence. Commit the exact ratified amendment, execution brief and complete pre-run protocol
>    on the authorized CP-16 candidate branch before new model comparison; document input,
>    code, dependency, budget and protocol identities and all permitted origin/target keys.
> 2. Implement only the fixed A1/B2 central blend, the frozen causal hour-aware residual policy
>    and the otherwise identical pooled control. Freeze the two constructions on permitted
>    training data before outer scoring; prove that their only difference is hour-aware pooling.
> 3. Prove origin availability, training-only and origin-specific transforms, D−2 release,
>    consume-once, genuine warm-up, complete-day/DST identity, sparse-hour fallback, cache
>    identity and restart replay, with negative assertions accompanied by positive controls.
>    Preserve relevant inherited namespace guards and all prohibited-partition boundaries.
> 4. Produce forecasts for every original eligible target in all five folds; report exact
>    shared key counts, failed issuance and original exclusions, all finite ordered quantiles
>    and emitted p50 separately from central. No missing eligible forecasts, altered targets
>    or silently reduced denominators can support completed-evaluation PASS.
> 5. Independently verify emitted-vector scores, original seven-quantile WIS and equal-fold B0
>    normalization, all required per-fold/hour/block/peak diagnostics and their denominators.
>    Re-score saved B0/B1/B2/A1 references and B3's diagnostic comparisons without new fits or
>    overwriting historical evidence. Keep native v1 pinball separate.
> 6. Apply the frozen research ranking/paired uncertainty/no-preference rule mechanically,
>    report both point and interval effects including negative or mixed findings, and report
>    all six unchanged original §8 diagnostics. Distinguish Engineering status, historical
>    CP-15 product status, new research findings and product/delivery eligibility. No demonstrated
>    joint preference is not equivalence or absence of benefit; disclose mixed effects. No post-hoc
>    economic threshold or research-to-product promotion is permitted.
> 7. Enforce and report every adopted numeric resource/candidate cap, counting warm-up, inner
>    selection, failed attempts, controls, corrections and independent reproduction. At the
>    first exhausted cap retain partial evidence and return the appropriate non-PASS status;
>    no unauthorized scope reduction or resource extension can cure an incomplete checklist.
> 8. Supply durable protocol, lineage, predictions, metrics, diagnostics, uncertainty, failure/
>    resource logs, notices, reproducibility manifest and executable reproduction commands.
>    Run relevant controls and regression checks; disclose defects/repairs and invalidated
>    outputs. All development results retain their post-selection label and inherited limits.
> 9. Obtain one fresh independent Integration-Critic PASS on a clean detached checkout of
>    the exact final candidate, covering this entire checklist, independently recomputed
>    saved-prediction metrics and representative causal/component/state reproduction. Preserve
>    commands, exit codes and limits; no self-certification or unsupported PASS.
> 10. Return the complete canonical checkpoint packet, both terminal SHAs and a verdict-only
>     candidate-to-evidence delta, reachable evidence, branch/worktree/tag accounting, elapsed
>     effort and all resource totals. End at CP-16's local result, including an honest negative
>     result; no next checkpoint, final live-policy selection, publication or mainline operation.
>
> ### 14.9 Entry authority and terminal boundary
>
> The Owner ratified the v21-r3 cap/counting change and authorized CP-16 resumption on
> 2026-09-23, including its consistent successors. Read `AGENTS.md`, `engineering-role.md`,
> this exact ratified revision and `docs/track-b/cp-16-v2-brief.md`. The complete §14.8 checklist
> controls; CP-15's §12 is not the CP-16 bar. Preserve the role's information-isolation rules.
>
> Use the approximate 32-hour timebox and all §14.5 hard ceilings; report elapsed hours to the
> nearest half hour and active/compute effort separately. Stop at the first exhausted cap,
> retain partial evidence and return PASS/BLOCKED/INCOMPLETE under templates §3 as applicable.
> A missing required forecast/review cannot support PASS. No automatic additional family,
> comparison, budget extension, next-checkpoint planning, mainline action or publication.
> Reasoning-capture triggers are named by the Lead in its return; it does not edit Q&A.


## Supporting section 15

> ## 15. CP-20 — direct-GFS paired research ablation (v21-r4 ratified)
>
> **Ratified and separately authorized for CP-20 execution, 2026-09-23.** Owner approves the
> revised three-feature specification and all §15.5 ceilings, including 120 aggregate machine-hours.
> Owner D1/D3 select research only; D2 fixes the comparator and endpoint rule below.
> This issuance records authority and identities only; the approved scientific and resource
> requirements are unchanged. The task-scoped recording suspension ends at the Orchestrator's
> terminal return and grants no Lead authority to edit governance. CP-17–19 retain their roles and are not opened. This is programme 4.4D,
> not VRE modelling, product qualification, an economic experiment or prospective operation.
>
> ### 15.1 Inheritance, population and arms
>
> Inherit §§14.1–14.4 unchanged for original target keys/folds, component training/selection,
> normalization, chronology, H residual construction, metrics/diagnostics, bootstrap mechanics
> and evidence labels, except the explicitly replaced arms, weather treatment and contrasts
> here. Inherit §§2–3, all six §8 diagnostics and §9 restrictions. Preserve historical CP-15/16
> results, FAILs, debits and limits. §14 remains the unchanged historical CP-16 contract.
>
> - **H0:** no-weather V2-H exactly as §14.2: inherited A1/B2 50/50 central blend and H layer.
> - **HG:** the same A1/B2 recipes with only the §15.2–15.3 weather columns appended to each
>   hourly regressor; same 50/50 central blend, price-only A1 scale, H recipe and failure rules.
>   Each arm uses its own genuinely issued central errors, but identical buffer dates,
>   release/support/update rules. Do not share residual values across different forecasts.
> - Same histories, eligible rows, chronological four-penalty selection procedure, numerical
>   settings and fixed seed 42; selected penalties may differ because inputs differ. No extra
>   interaction, lag, feature subset, blend weight or residual tuning. No pooled-P arm here.
> - Reuse identity-verified H0/component caches and five saved B0/B1/B2/B3/A1 references;
>   independent representative H0 reproduction must match accepted CP-16 vectors. HG components
>   must be fitted with their own causal weather inputs, not relabelled cached no-weather fits.
> - Both arms cover exactly §14.1's **10,747** keys (including fold 5 through **2026-04-07**):
>   **21,494** contrast rows; with five saved references, **75,229** scored rows. Preserve
>   original exclusions; missing weather never removes a target or shortens price history.
> - Freeze the existing CP-16 input-manifest's **638 fold/date origins**, 35 training-only
>   admission dates and genuine warm-up (2020-05-25 / 2021-02-23 / 2022-05-25 / 2025-03-22 /
>   2025-12-02). No earlier warm-up search. The §14.2 60-date limit remains an outer bound.
>
> ### 15.2 Admitted source, conversion and one weather recipe
>
> Use only operational **GFS 0.25° D−1 00 UTC** via the dossier's NCAR d084001 / NOAA AWS
> endpoints. Admission is accepted for the inventoried scope under its disclosed assumptions:
> NCAR-only field presence is inferred from file integrity/size plus sampled version layouts;
> public availability before D−1 11:00 UTC is **reconstructed availability**, not a daily-delivery
> guarantee. NCEP completion averages do not independently establish public dissemination lag.
> Carry these assumptions, known endpoint defects, source fingerprints and the post-sample
> radiation-precision-check disclosure into protocol/report. Admission does not certify live use.
> ICON remains NOT_ADMITTED and is excluded. No reanalysis, hindcast, later cycle or pre-2019 input.
>
> The dossier inventoried 2,468 runs using CP-15 warm-up. This CP-16-style warm-up requires
> **2,476** unique runs: the extra **2023-03-24..31** eight runs must receive targeted GFS
> field/lead/availability checks before fitting. Do not label them already admitted. Verify
> actual field metadata during extraction, including previously inferred NCAR fields; a material
> contradiction to admission or unsupported version/units stops the task with evidence.
>
> Freeze this single conversion before fitting or scoring:
>
> 1. Decode u/v at **10 m and 100 m above ground** (m/s) and surface **DSWRF** (W/m²).
>    Pressure levels never substitute for above-ground heights. Validate init/valid time,
>    grid, forecast status and version per message. Needed endpoints are f021,024,…,048.
>    Use the inventoried endpoint; for added runs use AWS first. At most one same-product
>    alternate-endpoint attempt per failed object; compare metadata, retain hashes and defects.
> 2. Wind: linearly interpolate each component between bracketing three-hour endpoints to
>    canonical delivery-hour starts **h22–h46**, with no extrapolation. Then compute
>    **sqrt(u²+v²) per grid cell**, separately at **10 m and 100 m**, before spatial averaging.
>    Radiation: at each grid
>    point recover three-hour means from documented six-hour-reset averages: use A(L−3,L)
>    directly at L≡3 mod6, otherwise **2A(L−6,L)−A(L−6,L−3)** at L≡0 mod6. Assign the block
>    mean to each constituent hour [h,h+1); no solar-shape disaggregation or extra interpolation.
>    Validate actual averaging bounds, not lead number alone. For negative block means, permit
>    only values ≥−3q, q=max packing quantum of contributing messages; clip those to zero
>    before aggregation and log count/magnitude/version. Below −3q or unknown quantum/bounds
>    is a conversion failure, not a fitted tolerance. Disclose coarse v14/v15 precision.
> 3. Use the fixed rectangular proxy **47–55.25°N, 5.5–15.5°E**, inclusive grid centres,
>    cosine(latitude) area weights normalized over that fixed grid. Apply them to the per-cell
>    wind-speed magnitudes at each height and to converted DSWRF, separately per hour. Mean
>    wind speed is the weighted mean of cell speeds, not the magnitude of mean u/v.
>    No power curve, capacity weights, learned geographic mask, VRE conversion or provider search. Call it
>    a regional weather proxy, not an exact DE-LU polygon or power-generation forecast.
>    Do not renormalize over missing cells. Nonfinite required support makes the weather vector
>    missing under §15.3. Store grid/weights, units and conversion fingerprints.
> 4. Append only **three same-target-local-hour weather columns** to each A1/B2 hourly design:
>    **mean wind speed at 10 m, mean wind speed at 100 m, mean DSWRF**. Inherited imputation
>    adds their **three missing indicators**. The five native extraction fields remain
>    **u10, v10, u100, v100 and DSWRF**. No cross-hour expansion or feature search.
>    On repeated local hours average the two canonical weather vectors as the inherited LEAR
>    local-hour design does; preserve both canonical outputs/targets. A missing spring hour
>    remains absent. Require all repeated-hour inputs or mark the local-hour vector missing.
>
> ### 15.3 Missing-input and transform rule
>
> Weather for **delivery 2019-01-01 is structurally missing** because its run would be
> 2018-12-31; do not import it or remove its otherwise eligible training row. For any confirmed
> missing/late/nonfinite weather vector after the bounded endpoint attempts, set all three
> derived weather columns missing and mark all three indicators. Apply the inherited CP-15 LEAR
> imputer/scaler: per-feature **training-partition median**, all-null column → 0, missing
> indicator per feature, then training-only StandardScaler. Fit them independently inside each
> inner-training split and final training window; never use validation/outer outcomes or future
> weather to impute. No interpolation across dates, forward fill or zero-radiation shortcut.
> This is the same rule in training, admission, warm-up and evaluation. HG still emits its own
> fitted-component/H forecast; it does not switch silently to H0 or borrow H0's residuals.
>
> Complete the required extraction/status ledger before fitting: classify structural missing,
> confirmed archive absence, documented lateness and invalid support separately. Failed/unattempted
> retrieval due to exhausted resources, absent admission evidence or unknown schema is **BLOCKED**,
> not missing-data imputation. Confirmed missing weather is an explicit part of the HG policy;
> report dates/counts and all-imputed origins, not an unqualified complete-weather claim.
> Price/load/component/state failures retain §14.2's failure rule; weather fallback cannot cure
> insufficient common history, an invalid fit or a missing eligible forecast. Freeze the recipe,
> conversion fixtures and complete missingness manifest before any fit/outer scoring.
>
> ### 15.4 Comparison and claims
>
> The sole primary contrast is **HG − H0**, for each paired equal-fold normalized score.
> Use §14.4's seed 15042, one shared 2,000-replicate seven-calendar-day block index set per
> analysis pass and its exact paired score-difference/95% percentile procedure. Apply
> **upper CI(ΔS_WIS)<0 AND upper CI(ΔS_MAE)≤0** to those differences, not to marginal-score
> intervals or point estimates. Otherwise report **no demonstrated joint preference**, with
> mixed outcomes/undefined intervals explicit; never equivalence or absence of benefit/harm.
> If descriptive ordering is reported, lower S_WIS then S_MAE, with H0 on exact ties; it is not
> promotion. Original §8 diagnostics are unchanged for both arms, with saved B0–B3 comparators.
> Keep all §14.3 per-fold/hour/block/peak diagnostics and §14.4 scientific limitations.
> All results are **development_post_selection**. Historical economics is descriptive only;
> zero new economic runs/thresholds. Negative results complete valid research; no result opens
> VRE, CP-17–19, public surfaces, live selection or a prospective clock.
>
> ### 15.5 Owner-approved ceilings — CP-20 execution authorized
>
> **D4 approved, 2026-09-23:** 120 aggregate machine-hours; all other caps below approved as
> drafted. These are **CP-20-specific** ceilings, not feasibility guarantees, estimates or targets.
> The Lead retains the existing pre-run feasibility responsibility. No transfer of CP-16's unspent allowance
> or reset of its 6,458 policy-days/other debits. Report prior-task totals separately from new
> CP-20 increments. Use §14.5's counting units and forward-looking synthetic-test/real-replay/fit
> distinctions unchanged. Charge preparation, failures, warm-up, controls, repairs and independent
> review to applicable caps. Stop before the first exhausted cap and retain partial evidence.
>
> | Dimension | Owner-approved maximum |
> |---|---|
> | Policies/configurations | **2** arms, **5** saved references, **7** scored policies; **1** weather feature/conversion/missingness recipe, **1** fixed H recipe; **2** inherited A1/B2 component recipes per arm; **2** components/blend, weight 1/2; **0** additional ensembles/configurations/outer-selection trials |
> | Seeds/inner selection | Fixed fitting seed **42**, bootstrap seed **15042**; no seed search; **4** inherited penalties per hourly fit, same chronological inner split/tie rule |
> | Dates/main fits | **638** fold/date origins/arm, **35** admission dates/arm within those, ≤**60** warm-up dates/fold; **3,000** main component-day attempts across both arms (contains cache misses; nominal all-fresh need 2×638×2=2,552) |
> | All fitting | **4,000** component-day attempts total; **480,000** primitive Lasso attempts: ≤**384,000** inner and ≤**96,000** final refits (4,000×24×(4+1)); retries/solver continuations count, not extra recipes |
> | Replay | **9,000** new policy-days total; ≤**6** full-equivalent paired passes (conservative envelope 750×2×6); actual reused/recomputed real-data state work charged under §14.5 |
> | References/uncertainty | **3** metric-only full reference passes; **3** bootstrap analysis passes including independent review, **2,000** replicates each; **0** new B0/B1/B3 fits/reference calibration |
> | Weather/extraction | **1** product, **2** named access endpoints; **2,476** unique 00 UTC runs; **5** fields×**10** leads/run (≤**123,800** target messages); **3** decode/extraction attempts per target message including retries/review; **160 GiB** cumulative new transfer including metadata, dependencies, failed/duplicate requests; **0** whole global multi-field run-file downloads or unrelated data/model downloads |
> | Compute/effort | **120 aggregate machine-hours** including network/extraction jobs, summed across concurrent jobs; **4** workers, BLAS **1**, **0** GPU/cloud; approximate **64-active-hour** timebox, hard **80 active hours** including verification/return |
> | Memory/storage/cost | **10 GiB** aggregate process-tree RSS; **40 GiB** additional peak disk including environments/worktrees/cache/evidence; **$0**; inherited admission cache (~1.73 GiB) measured as retained baseline, not deleted or hidden |
> | Other work | **0** ICON/VRE/neural candidates, feature/recombination searches, new economic runs, operational days, schedules or remote mutations |
>
> Rationale: the dossier estimates ~101 GiB of target-message payload and ~55 sequential NCAR
> hours plus 7–22 AWS hours. Transfer/compute margins cover indexes, failures and review; they do
> not prove feasibility. Stream verified messages to bounded regional artifacts; retain original
> sample raw files, per-message hashes/URLs and reproducible acquisition records. Do not retain
> ~101 GiB of globals under a 40 GiB disk cap. No unverified NCSS shortcut is included.
> Before dependent work, the Lead completes §14.6 E1–E4 for **CP-20**, estimating extraction,
> admission, production, controls and independent verification against every cap. Insufficient
> allowance/material discrepancy returns a concrete blocker, not a new unapproved recipe.
>
> ### 15.6 Complete CP-20 acceptance checklist
>
> All ten items are mandatory. They inherit the verification standard of §14.8; the weather
> additions and H0/HG scope replace CP-16-specific H/P wording, not its scientific safeguards.
>
> 1. Verify repository/input state, retain prior evidence and other-session work; after Owner
>    ratification/execution grant only, package exact supplied anchor/amendment/brief and commit
>    the frozen protocol/input/conversion/missingness/budget manifests before comparison.
> 2. Close the eight-run admission extension; validate all extracted field/lead/version metadata,
>    source/endpoint identity and historical availability basis. Preserve inferred versus decoded
>    evidence, 2019 structural missingness and all dossier exceptions; record every extraction gap.
> 3. Implement exactly H0/HG and the frozen conversion/fallback; show only the predefined weather
>    treatment differs. Verify H0 against accepted CP-16 vectors and reproduce representative
>    weather-component fits. Training-only admission must precede outer scoring; no tuning to gain.
> 4. Prove §14.8 item 3's causal/state/DST/cache controls, plus positive/negative weather-origin,
>    accumulation, units, packing/clipping, aggregation and missingness controls. Verify pre-2019
>    refusal and independent reconstruction from retained raw samples without rerunning admission.
> 5. Produce all original eligible keys for both arms and the required reference metrics; no
>    denominator changes. Independently verify emitted p50/ordered vectors, all §14.3 diagnostics
>    and support counts, including fallback incidence; inherited failures still preclude PASS.
> 6. Apply HG−H0 paired endpoint rule and all six original §8 diagnostics; keep point/interval
>    effects, uncertainty, negative/mixed findings, post-selection labels and research/product
>    distinctions. No promotion, economic threshold or claim of guaranteed availability/coverage.
> 7. Enforce/report every §15.5 cap from the first job, all attempts and independent review;
>    preserve historical debits/monitoring limitations. Exhaustion yields BLOCKED/INCOMPLETE,
>    never implicit permission to impute unfinished extraction or shrink evaluation.
> 8. Supply protocol, lineage, decoded weather/features, predictions, metrics/diagnostics,
>    uncertainty, criteria, failure/resource logs, rights notices and executable reproduction
>    commands; preserve invalid outputs/repairs and run relevant inherited regression guards.
> 9. Obtain **one fresh independent Integration-Critic PASS** binding the exact final candidate
>    in a clean detached checkout and this entire checklist, with independent saved-vector
>    metrics/paired uncertainty and representative conversion/component/causal/state reproduction.
> 10. Return canonical packet, final candidate and evidence-tip SHAs, evidence-only terminal
>     delta, reachable history, all resources and branch/worktree accounting; stop at CP-20's
>     local result. No mainline action, publication, later checkpoint or executor self-ratification.
>
> ### 15.7 Paths and entry authority
>
> Under the recorded CP-20 execution authorization: `src/cp20/`, `tests/cp20/`,
> `scripts/cp20_weather.py`, `reports/weather-ablation/`, `docs/track-b/evidence/cp-20/`,
> `pyproject.toml`/`uv.lock` if necessary; ignored material under `.local/{worktrees,artifacts,tmp}/cp-20/`.
> Use admitted files read-only from `reports/weather-admission/` and `.local/weather-admission/`;
> put extended inventories/extraction evidence in `reports/weather-ablation/`. Preserve CP-15/16
> code, reports, data, model registries, public surfaces, Q&A, progress and all other locked files.
> Include the exact accepted `reports/weather-admission/` bundle and intake receipt in the
> candidate when absent from its base; preserve their manifest identity, without revising them.
>
> Accountable executor: CP-20 Engineering Lead; reviewer: its fresh independent Integration
> Critic under `engineering-role.md`. The Owner separately authorizes local
> `gauntlet/cp-20` candidate/evidence commits and exact immutable packaging of this ratified
> anchor, `docs/track-b/capstone_v21-r3-to-v21-r4-amendments.md` and
> `docs/track-b/cp-20-direct-weather-brief.md`, together with the admission package above.
> Ratification and CP-20 execution authority are **GRANTED, 2026-09-23**. The Lead owns the
> existing pre-run checks, including feasibility and the eight added GFS runs; no further Owner
> approval is needed unless a concrete blocker exceeds this scope. No scientific/budget change,
> later checkpoint, governance edit, mainline operation or publication is authorized.


## Supporting section 16.2

> ### 16.2 What freezes and what updates every day
>
> Freeze code and dependencies, algorithm/architecture, feature and source-availability
> contracts, hyperparameters, training-window and label-delay rules, initial artifact/state,
> randomness, refit schedule, uncertainty/calibration updates, scoring/decision rules and failure
> policy. Store numeric registry versions and initialization fingerprints as §9 requires.
>
> For the selected final product, **daily retraining, eligible input refresh and forecast
> issuance are required on every delivery day**. Each successful fit produces a versioned
> artifact with its training window, available labels, seed, timestamps and parent/input/state
> hashes. Use only information available at the fixed origin. Daily fitting changes weights/state
> within the frozen policy, not the adopted generation; discretionary tuning or changing that
> policy requires a new freeze and evaluation. Never overwrite an issued forecast after outcomes.
>
> The future brief fixes numeric origin/deadlines, windows, resource ceilings and the exact
> meaning of a successful daily fit before the fresh-data replay/final freeze. Input refresh,
> residual-state maintenance or TabPFN context replacement alone is not weight training. A
> candidate unable to meet daily retraining within admitted licensing/resources needs an explicit
> Owner-approved exception specifying its real update mechanism and public wording before live
> admission; no alternative cadence or exemption is silently inferred from model family.
> Immutable historical v1/reference artifacts remain untouched; this requirement does not
> retroactively retrain them or force every research comparator to train daily.
>
> Daily operation covers all delivery days, including DST. The operational brief supplies an
> explicitly authorized unattended schedule and incident/fallback policy. Publication authority,
> operator ownership, monitoring, permissions and resources must be settled before launch. This
> amendment creates no automation or standing authority to publish externally.
>
> For missing inputs/labels, failed training, resource exhaustion or source outage, apply the
> frozen fallback/staleness limits or record failed issuance. Display a failed/skipped fit as
> such, even if a valid fallback produces a forecast. Do not count retained weights as a new
> successful training run or backfill a late forecast as timely. Failures remain in the record.


## Supporting section 17

> ## 17. CP-21 — three-block LightGBM on top of v3 (v21-r6, ratified)
>
> **Ratified by the Owner on 2026-09-29; execution authorized under §17.11.** This is programme
> work item 4.5, reframed by the Owner's choice: the three-block LightGBM is tested as an
> addition to v3 (HG), not as a replacement for it. The result is published in either outcome
> (§17.9). It is adopted as
> `v4 · <adopted change>` under §17.6; otherwise it becomes a descriptive branch marked
> "Not adopted". CP-21 is research only. It releases no product and triggers no promotion,
> CP-17 freeze, prospective clock, economic run or publication by itself. CP-17–CP-19 stay
> reserved (§§9–10 and §16).
>
> ### 17.1 Question, inheritance and evidence class
>
> **Question.** HG's central forecast is a blend of two linear LEAR components. Does adding a
> three-block LightGBM member, built with exactly HG's information, improve on HG jointly in
> point and interval accuracy, on CP-20's development population? HG's hour-aware interval
> layer is re-estimated on the new forecast's own issued errors.
>
> **Why on top of v3.** The saved daily LightGBM B3 scores S_MAE 0.7841 / S_WIS 0.7399; HG scores
> 0.5658 / 0.5322. The programme's optimistic estimate for a standalone per-block LightGBM was
> S_MAE 0.73–0.75 (programme §§4.5–4.8). A standalone block model is therefore not a credible
> successor. The testable hypothesis is that a nonlinear, block-structured learner adds
> information to HG's linear components, particularly from the weather columns. The standalone
> arms remain, for attribution only.
>
> **The decomposition.** The Owner added the pooled arm L-P to test the block hypothesis itself.
> The arms form a ladder, each step adding one thing:
>
> | Step | What it adds |
> |---|---|
> | B3 → L-P | Weather |
> | L-P → L-R | The block split |
> | L-R → HGL | The blend into v3 |
>
> B3 is a saved CP-15 reference with fixed CP-2 hyperparameters. The B3 → L-P step therefore
> also includes training-only capacity selection and the §15.3 missing-input rule, and is not an
> isolated weather effect. The L-P → L-R step is controlled: L-P and L-R differ only in pooled
> versus per-block fitting.
>
> **Inherited unchanged:**
>
> - §§2–3: information boundary and evidence class.
> - §4: normalization.
> - §§14.1–14.4: population, chronology, the H residual recipe, metrics, bootstrap mechanics and
>   limits.
> - §§15.1–15.3: weather treatment, frozen features and the missing-input rule.
> - All six §8 diagnostics, reported as diagnostics; §9's restrictions; §16.
>
> Only the arms, contrasts, adoption rule, ceilings and deliverables below are new. Historical
> CP-15/16/20 results, FAILs, debits and limits are preserved. They are re-scored only as saved
> references.
>
> Every CP-21 result is `development_post_selection`. Nothing dated after 2026-04-07 is read,
> scored, plotted or used for any choice, and the fresh-data test 4.7T stays reserved.
>
> ### 17.2 Arms, comparator and the single adoption candidate (Owner decision D1)
>
> | ID | Role | Construction |
> |---|---|---|
> | HG | Comparator (v3), saved | CP-20's HG exactly: the saved accepted vectors. Its components A1_w (normalized LEAR) and B2_w (raw LEAR), both with weather, are reused only with verified identity. |
> | L-P | Study arm, for attribution | One pooled LightGBM for all 24 hours, on the raw target, with exactly HG's information including weather (§17.3), and HG's H layer on its own issued errors. Never adoption-eligible. |
> | L-R | Study arm, for attribution | Three-block LightGBM central forecast on the raw target (§17.3), with HG's H layer (§14.2) on its own issued errors |
> | L-N | Study arm, for attribution | L-R with §4 target normalization; otherwise identical |
> | HGL | Sole adoption candidate | Central `c = (1/3)·A1_w + (1/3)·B2_w + (1/6)·L-N + (1/6)·L-R`, that is `(2/3)·c_HG + (1/3)·mean(L-N, L-R)`. HG's H layer is re-estimated on HGL's own issued errors. |
>
> **The blend.** The fixed weights give each model family one equal vote: normalized LEAR, raw
> LEAR and block LightGBM. They also keep HG's raw/normalized pairing inside the new member. The
> weights are set before any CP-21 result and are never tuned; learned or per-block weights
> belong to programme 4.8.
>
> **What differs from HG.** HGL differs from HG only by the added member. Its A1_w and B2_w are
> HG's own genuinely issued components, identical bit for bit.
>
> **The interval layer.** HGL, L-P, L-R and L-N each use HG's layer on their own issued errors:
>
> - the price-only A1 scale `s_t`;
> - the 28-complete-released-day buffer and `w_h = n_h/(n_h+56)`;
> - the seven quantiles and the §14.2 failure rule.
>
> Residuals are never shared across forecasts.
>
> **Retraining.** The Owner's "retrain" is met in two ways. The new member is trained at every
> origin, and the interval layer is re-estimated on the composite's own errors. HG's components
> are deterministic, so refitting them reproduces CP-20's forecasts. The design verifies this
> through the fully refitted origins of §17.5 and reuses the verified CP-20 components elsewhere.
>
> **Saved references, metric-only:** B0 (normalizer), B1, B2, B3, A1, H0 (v2) and HG. No
> reference is refitted, except for an identity-verified regeneration of HG components on a
> cache miss. Eleven policies are scored: 7 saved plus 4 new.
>
> **The block-split claim** is reported from L-R − L-P according to its result (§17.5), not
> withheld.
>
> **Out of scope, and why:**
>
> - **A per-block residual-correction model on HG's errors.** It would need genuinely held-forward
>   HG forecasts across every training window: a nested full-history HG replay, plus weather
>   retrieval for 2022-09-29..2023-03-23. In-sample residuals cannot replace those (§3).
> - **A normalized pooled arm.** The split is tested on the raw target only.
> - **Seed ensembles.**
>
> These exclusions bound attribution. L-R − L-P isolates the block split on the raw target. No
> contrast separates the individual weather features.
>
> ### 17.3 Block models, information set and training-only capacity selection
>
> **Blocks.** The blocks are fixed and exhaustive, in Europe/Berlin local hours:
>
> - night: 22–05 (8 hours);
> - solar: 10–16 (7 hours);
> - shoulder/peak: 06–09 and 17–21 (9 hours).
>
> L-R and L-N fit one model per block, and a target hour belongs to exactly one block. L-P fits
> one pooled model over all 24 hours, on the same rows. On a 25-hour day, both canonical
> local-hour-2 observations enter the night block (and L-P's rows). On a 23-hour day the missing
> hour stays absent.
>
> **Information set: exactly HG's, for every LightGBM arm.** The features are:
>
> - the inherited CP-15 B3/A2 LightGBM recipe: `reports/cp15/protocol.json`, 23 features, and
>   for L-N its price-valued center/scale lists;
> - the three frozen §15.2 weather columns for the target local hour;
> - their three missing indicators, under the §15.3 training-only median-imputation rule.
>
> Nothing else enters: no other feature, lag, cross-hour weather expansion or source, and no
> feature search. LightGBM's native missing-value routing does not replace the §15.3 rule.
>
> **Fixed settings.** Objective: quantile, α = 0.5 (p50). Seed 42, with deterministic
> single-seed fits. The other inherited CP-15 parameters stay unchanged, except capacity.
>
> **Capacity grid.** At most four configurations per model: each block model, and L-P's pooled
> model. The largest is the inherited setting, 600 trees and 63 leaves; the others have lower
> capacity, with fewer leaves, trees or both. The grid is frozen in the pre-run protocol before
> any outer scoring and is identical for L-P, L-R and L-N.
>
> **Selection, at every origin and for every model (each block, and L-P's pooled model):**
>
> 1. Fit each configuration on the origin's training window, minus its last 28 calendar delivery
>    days.
> 2. Select the lowest validation MAE in EUR/MWh on those 28 days. L-N is inverted before scoring.
>    An exact tie goes to the smaller configuration.
> 3. Refit the selected configuration on the whole window.
>
> This mirrors LEAR's inherited inner selection and uses training data only.
>
> **History.** `[max(2019-01-01, D−728 calendar days), D)`, subject to each origin's availability
> filter, as in §14.1.
>
> **Minimum training rows.** L-P keeps the inherited 8,760-row LightGBM minimum, which is
> 365 × 24. The block equivalent is 365 × block hours: 2,920 (night), 2,555 (solar) and 3,285
> (shoulder/peak).
>
> **Cadence.** Every origin gets fresh daily fits, including selection, as §16's daily retraining
> would require of a product. An identical historical fit may be cached only with verified input,
> protocol and origin identity. A cache miss counts as a budgeted fit.
>
> ### 17.4 Population, chronology and failure rule
>
> **Population: CP-20's frozen population.**
>
> - 10,747 original target keys, with fold counts 2,160 / 2,159 / 2,112 / 2,160 / 2,156, over
>   448 represented delivery days.
> - The CP-16/CP-20 input manifest's 638 fold/date origins, including 35 training-only admission
>   dates.
> - The same genuine warm-up starts: 2020-05-25 / 2021-02-23 / 2022-05-25 / 2025-03-22 / 2025-12-02.
>
> Each new arm covers every key: 42,988 new policy-target rows, or 118,217 scored rows with the
> seven saved references.
>
> **Chronology.** Forecast origin D−1 11:00 UTC; delivery calendar Europe/Berlin; released errors
> are ≤ D−2 and consumed once.
>
> **Weather.** Weather comes only from CP-20's retained decoded grids, through the frozen
> conversion, verified against CP-20's fingerprints. No weather is retrieved.
>
> **Failure rule.** §14.2's rule applies to every component, including every LightGBM fit. No
> stale, B0, HG or zero-error forecast is substituted, and losing an eligible key prevents a
> complete evaluation.
>
> **Admission slice.** §14.2's training-only admission slice checks that each new arm runs
> causally before any outer scoring. It is not a selection trial.
>
> ### 17.5 Metrics, uncertainty and diagnostics
>
> **Scores,** as in §14.3 and §15.4: emitted-p50 MAE and seven-quantile WIS; S_MAE and S_WIS as
> equal-fold ratios to B0; pooled scores as secondary descriptions.
>
> **Bootstrap,** as in §14.4 and §15.4: seed 15042, with one shared 2,000-replicate noncircular
> index set of 7-calendar-day blocks per analysis pass. Blocks are drawn within each 90-date fold,
> identically across policies.
>
> **Contrasts.** The primary contrast is HGL − HG, the adoption contrast. The secondary contrasts
> are descriptive:
>
> | Contrast | What it shows |
> |---|---|
> | L-R − L-P | The block split: the Owner's hypothesis |
> | L-P − B3 | Weather, bundled with capacity selection (§17.1) |
> | L-N − L-R | Target representation |
> | L-P − HG, L-R − HG, L-N − HG | Each standalone arm against v3 |
>
> The block-split finding is stated from L-R − L-P, with §14.4's endpoint reading:
>
> - **observed joint improvement:** the upper endpoint of ΔS_WIS < 0 and of ΔS_MAE ≤ 0;
> - **observed joint worsening:** the lower endpoint of ΔS_WIS > 0 and of ΔS_MAE ≥ 0;
> - **otherwise, no demonstrated joint preference,** with both metrics' directions shown.
>
> It is a development finding, not an adoption criterion.
>
> **What is reported for each contrast and score:**
>
> - the paired difference, with its 95% percentile interval;
> - for publication, the change as a share of the comparator's score, with the interval of that
>   ratio taken from the same replicates. For each replicate b,
>   `R_b = S_policy,b / S_comparator,b − 1`. The interval is the 2.5/97.5 percentiles of `R_b`,
>   and the point value is the full-sample ratio minus one. Every replicate's paired differences
>   and ratios are stored (PUBLISH_RULES 1.1 §3.2).
>
> **Per-fold paired daily-loss intervals** are computed for every contrast. For HGL − HG they
> feed §17.6's fourth condition; everywhere else they are descriptive. They are built exactly as
> CP-20's per-fold intervals: the paired difference of each fold's mean loss, resampled with the
> same 7-calendar-day block index set within that fold.
>
> **Diagnostics, for all arms:**
>
> - per fold, per local hour and per block (night, solar, shoulder/peak), with counts and
>   represented dates. Block and hour statements follow §14.3's support rule: at least 56
>   represented dates per fold.
> - coverage at 50/80/95%, always shown with mean, median and 95th-percentile width, and with
>   tail misses;
> - central versus emitted MAE and the centering effect; bias; daily level and shape error;
> - failures, and the H layer's fallback incidence;
> - the stress period, fold 3: 2022-07-01..09-28, 2,112 hours over 88 days. The 17-day peak,
>   2022-08-15..31 (408 hours), is reported separately and descriptively.
> - all six original §8 diagnostics for every new arm, with the saved B0–B3 comparators.
>
> **Fit cost and daily retraining.** The report covers three things:
>
> - LightGBM fits by arm, model (block or pooled) and origin: training rows, selected capacity,
>   inner and final fit wall and CPU seconds, and peak memory. The comparison of block and
>   pooled costs is part of the report.
> - any HG component regeneration;
> - HGL's complete daily cycle, measured cold on the M3 with at most 4 workers, at 20 or more
>   origins stratified across the five folds, giving the median and the maximum. The cycle
>   covers the features, the A1_w/B2_w refits, the six block selections and fits, the H layer and
>   issuance. Those refitted components must match CP-20's bit for bit.
>
> **Owner decision D3:** this is a diagnostic only, not a selection criterion. v21-r5 §16 still
> requires any final-product candidate to retrain daily, or to obtain an Owner-approved exception
> before live admission. The report is written to `reports/block-challenger/`.
>
> ### 17.6 Pre-registered adoption rule (Owner decision D2)
>
> Rule `cp21-adoption` was set on 2026-09-29, the date of the Owner's ratification. HGL becomes
> v4 if, and only if, all four conditions hold:
>
> 1. **Joint improvement over HG.** On the paired HGL − HG differences, the upper 95% endpoint of
>    ΔS_WIS is < 0 and the upper 95% endpoint of ΔS_MAE is ≤ 0.
> 2. **No regression on the original screen.** HGL meets all six original §8 diagnostics with the
>    saved B0–B3 comparators, as HG does.
> 3. **A complete, valid evaluation.** Engineering PASS with a fresh binding Integration verdict,
>    and every one of the 10,747 keys issued with finite, ordered quantiles.
> 4. **No resolved per-fold degradation.** In no fold may HGL − HG be decisively worse in MAE or
>    in WIS. A fold is decisively worse when the 95% interval of its paired daily-loss difference
>    (§17.5) lies entirely above zero, that is, when its lower endpoint is > 0. This applies to
>    each of the five folds and to both metrics.
>
> **Otherwise,** HGL is not adopted and CP-21 becomes a descriptive branch: "Not adopted", with
> the first unmet condition and its values as the reason.
>
> **How the rule is applied.** Mechanically. It is not re-weighted, re-thresholded or overridden
> after results. A mixed result is reported as no demonstrated joint preference, never as
> equivalence. L-P, L-R and L-N are never eligible for adoption, whatever they score. An
> INCOMPLETE or BLOCKED return yields no adoption decision and no result to publish.
>
> **What adoption means.** Adoption is a research status. v1 remains the released product and the
> demo. No final-product designation (§16), freeze or Live follows from it. An adopted v4 becomes
> the base for later extensions. At CP-21's landing, the Owner updates the standing decision
> "same information, same opponent", which names HG, so that later extensions face v4 on v4's
> information. Adoption is one more selection on the same five folds, so 4.7T's frozen manifest
> must carry both v3 and v4.
>
> **Naming** (plan revision 3 §16, decision 2; PUBLISH_RULES 1.1 §4). The version number is
> assigned only at adoption, dated at landing.
>
> - **Adopted:** `v4 · <adopted change>` (proposed: "v4 · three-block LightGBM added"), with
>   predecessor v3. The A3 transition title is "From v3 to v4: adding a three-block LightGBM".
> - **Not adopted:** the branch "Three-block LightGBM on v3", attached after v3.
>
> ### 17.7 Causal and integrity controls
>
> Every negative assertion has a positive control that can fail, and that survives the model's
> own transforms. The following are required for all new arms.
>
> - **Inherited controls: §14.8 item 3 and §15.6 item 4.**
>   - A delivery-day price mutation changes forecasts by exactly 0.0.
>   - An available D−1 mutation moves a controlled forecast.
>   - Post-gate and target-actual inputs are refused.
>   - D−1 errors are refused; D−2 errors are accepted once released.
>   - Each error is consumed once, and no partial day enters the buffer.
>   - 23/24/25-hour days keep their identity.
>   - Transforms are fitted on training data only, and warm-up is genuine.
>   - State persists and replays after a restart; a stale or wrong cache is refused.
>   - Quantiles are finite and ordered.
> - **Transform-aware positive controls for LightGBM.** Trees are invariant to monotone feature
>   rescaling, and normalization cancels a uniform price scaling. Weather influence must
>   therefore be shown with a non-monotone perturbation, for example a cross-date permutation of
>   weather vectors. The D−1 price control on L-N must use a non-uniform mutation.
> - **Training-only selection,** for every LightGBM model, block or pooled. Altering outcomes
>   after an origin leaves that origin's selected capacity, fits and forecasts exactly unchanged;
>   altering inner-validation rows can change them.
> - **Pooled–block parity.** L-P and L-R differ only in pooled versus per-block fitting: the same
>   rows, target, features, grid, selection rule and H recipe.
> - **Block membership and DST.** Every canonical target hour maps to exactly one block; repeated
>   and missing local hours are handled as in §17.3.
> - **Boundary guard.** Materializing any input or outcome dated after 2026-04-07 fails, with a
>   positive control.
> - **Blend and layer parity.**
>   - HGL's A1_w and B2_w equal HG's bit for bit.
>   - `c_HGL − (2/3)·c_HG = (1/3)·mean(L-N, L-R)`, within floating-point tolerance.
>   - HGL, L-P, L-R, L-N and HG call the same H-layer code path.
> - **HG identity.**
>   - Cached components match their CP-20 fingerprints.
>   - Independent representative HG reproduction matches the accepted CP-20 vectors.
> - **Byte-exact storage** of every hash-bound file.
>
> ### 17.8 Ceilings and calendar (Owner decision D4)
>
> **Nature of the caps.** These are Owner-approved maxima, not estimates or targets. They were
> approved as recommended on 2026-09-29, then recomputed for the added arm L-P.
>
> - **What counts:** warm-up, admission, inner selection, controls, failures, repairs and
>   independent review.
> - **At a cap:** stop before the first cap is exhausted and retain the partial evidence. No
>   outcome-driven retry, new arm, grid change or automatic increase follows.
> - **Debits:** previous debits stay historical. Nothing transfers from CP-16 or CP-20.
>
> | Dimension | Maximum |
> |---|---|
> | Policies | 4 new (L-P, L-R, L-N, HGL) and 7 saved references: 11 scored. 1 adoption candidate. 0 other arms: no normalized pooled arm, residual-correction model or blend-weight trial. |
> | Blend and interval layer | 1 fixed blend (§17.2) and 1 inherited H recipe. 0 alternative weights, residual configurations or outer-score selections. |
> | Capacity grid and seeds | At most 4 configurations per model, the same for L-P, L-R and L-N. Fitting seed 42; bootstrap seed 15042. 0 seed ensembles or seed searches. |
> | LightGBM fits | At most 24,000 main fit attempts. Nominal all-fresh: 638 origins × (2 block arms × 3 blocks + 1 pooled model) × 5 fits = 22,330. At most 35,000 in total, including controls, reproduction, failures and repairs. |
> | HG components | Reuse the verified CP-20 components. With the fully refitted origins of §17.5 or a cache miss: at most 1,600 component-day attempts (nominal 1,276) and 192,000 primitive Lasso attempts. |
> | Replay | At most 10,500 new policy-days: about 4 full-equivalent passes of 4 × 638 = 2,552, counted under §14.5's rule. |
> | References and uncertainty | At most 3 metric-only reference passes. At most 3 bootstrap analysis passes, including independent review, with 2,000 replicates each. |
> | Compute | At most 60 aggregate machine-hours, summed across concurrent jobs and including tests, failures and review. At most 4 concurrent worker threads in total (LightGBM threads × processes ≤ 4); BLAS 1; 0 GPU or cloud. |
> | Memory and disk | 10 GiB aggregate RSS. 20 GiB added peak disk, including worktrees, caches, the local MLflow store and outputs. |
> | Data, network and cost | 0 bytes of new data or model download. 0 weather retrieval. 0 remote writes (MLflow, Hub, Git remote). $0. |
> | Effort | Approximate timebox of 32 active hours. Hard ceiling of 40 active hours, including verification and the return. |
>
> **Basis for the recomputation.** CP-15's pooled daily B3 fits took about 3 seconds each, and a
> block model trains on about a third of those rows. Worst case, with single-thread parallel
> workers, the 22,330 main fits need about 28 aggregate machine-hours. Controls, reproduction,
> review, scoring and tests add about 12. The 60-hour cap leaves a 1.5× margin.
>
> **Unattended execution.** No long unattended run is required or authorized.
>
> **Before dependent work,** the Lead completes §14.6 E1–E4 for CP-21:
>
> - actual origin and fit enumeration;
> - the grid, fixtures and cache identities;
> - feasibility against every cap and the independent-review allowance.
>
> An insufficient allowance returns a concrete blocker, not a smaller experiment.
>
> ### 17.9 Publication packet and MLflow (Owner decision D5)
>
> From CP-21 on, the checkpoint supplies its publication packet (PUBLISH_RULES 1.1 §11;
> Publication Standard v1 §12). The landing templates do not carry it yet; that incorporation is
> decision D6 of 2026-09-28, a separate governance task. Until then, this section and the brief
> carry the step explicitly.
>
> - **Pinned rules:** PUBLISH_RULES 1.1, SHA-256
>   `91eea445434718a163f03bcfd82e1db275a9d98311e76eb6cd1365f3707584f3`. It incorporates
>   Publication Standard v1 (`01d721c2ba6316ca9a2f707e79da229bef732e91bad22f6ce457fb01e69478cc`) and
>   presentation plan revision 3 (`281193740a256a99a1676d53ef61c9babb5f744a7d0fb038927e305d1149812c`).
> - **The packet:** `docs/track-b/evidence/cp-21/publication-packet.md`, filling every section of
>   `docs/track-b/publication-packet-template.md`:
>   - identity;
>   - draft registry entries: HGL as a `v4 · …` generation or as the branch, per §17.6; L-P, L-R
>     and L-N as study arms; comparator HG; population `common-10747h`;
>   - the claim map `docs/track-b/research-content/cp21-claims.md`, with its withheld claims.
>     It includes the block-split finding stated from L-R − L-P (§17.5) and the
>     B3 → L-P → L-R → HGL ladder, with the bundling in the B3 → L-P step disclosed;
>   - the derived headline quantities: the verdict, the rule and its date, the distance from HG,
>     N, §17.5's ratio intervals with seed, replicates and block length, and per-fold MAE with
>     fold 3 as the stress period;
>   - draft slot texts for the outcome the rule yields: the v4 chapter plus the A3 transition, or
>     the branch card;
>   - §5b and §5d marked not applicable, with the reason: the released product and the
>     final-product designation do not change;
>   - §8's intended identities for GitHub/README, Pages, MLflow, the Space card and the direct
>     demo.
> - **The MLflow step:**
>   - The experiment is `delu-generations`.
>   - Runs are tracked locally only, in `.local/mlruns/cp21`: one parent, `cp21`, and one child
>     per new policy (`cp21/HGL`, `cp21/L-P`, `cp21/L-R`, `cp21/L-N`). Their names and tags follow
>     the draft entries.
>   - A draft export, `reports/block-challenger/mlflow-export-draft/cp21.json`, is built through
>     `scripts/mlflow_export.py`'s code path from committed CP-21 evidence and the packet's draft
>     entries.
>     - **Why a draft.** It stays outside the published set because registry statuses are dated
>       at landing, and registering a generation or branch requires its chapter or card.
>     - **Pending fields.** Identities that exist only at landing are explicit pending fields:
>       the adoption date and source, the evidence-tag commit and the landing record.
>   - The published export set is unchanged: `reports/presentation/mlflow-export/`, including its
>     `manifest.json`. `mlflow_export.py --check` still passes on it.
>   - The publication block registers the entries and regenerates the final export. That export
>     must equal the draft apart from the pending fields, and it must change no previously
>     published record.
>   - There is no public write, no upload and no network call to DagsHub.
> - **Public surfaces are unchanged in CP-21.** CP-21 does not regenerate or modify any of the
>   following; they belong to the separate publication block after landing:
>   - the page;
>   - the README's generated blocks;
>   - the Space cards and bundles;
>   - the public registry's rendered entries;
>   - the existing exports.
>
>   CI and `make verify` stay green at the final candidate.
> - **Acceptance:** the Integration Critic reviews the packet and the export as artifacts.
>   - Every number re-derives from committed rows.
>   - Names and statuses follow the draft entries and §17.6's mechanical verdict.
>   - The diff touches nothing already published.
>
> Publication itself follows the Owner's LAND in either outcome, as a separate block under
> PUBLISH_RULES 1.1: the registry, the chapter or branch card, the page, the README, the MLflow
> upload, the Space and the postdeploy checks. See
> [the publication plan](docs/track-b/cp-21-publication-plan-2026-09-29.md).
>
> **Owner decision D6:** if v4 is adopted, its chart encoding is amber `#B45309`, a filled
> diamond marker and the direct label "v4" (PRES-1 W16(b)).
>
> ### 17.10 Complete CP-21 acceptance checklist
>
> All thirteen items are mandatory. Engineering PASS does not require adoption: a complete,
> valid "Not adopted" result can pass.
>
> 1. Verify the repository and input state, and preserve prior evidence and other sessions'
>    work.
>    - The ratified anchor and the amendment record are on `main` at the ratification commit;
>      verify their SHA-256 against the brief.
>    - On `gauntlet/cp-21`, package the issued brief byte for byte as
>      `docs/track-b/evidence/cp-21/issued-brief.md`, from its canonical copy
>      `.local/artifacts/cp-21/issued-brief.md`, and record its SHA-256.
>    - Before any outer scoring, commit the frozen pre-run protocol:
>      - the arms, blend weights, block map, feature list and missing rule;
>      - the capacity grid, inner split and tie rule;
>      - fixtures, seeds, the key/origin manifest and cache identities;
>      - budget accounting and the §17.6 rule text.
> 2. Verify the CP-20 population and manifest identities, and the frozen weather features from
>    the retained grids. Reuse HG components only with verified identity, and obtain an
>    independent representative HG reproduction that matches the accepted CP-20 vectors. No
>    retrieval, and no data after 2026-04-07.
> 3. Implement exactly L-P, L-R, L-N and HGL, with training-only capacity selection for every
>    LightGBM model. Prove three things:
>    - HGL differs from HG only by the added member and uses HG's H recipe on its own errors;
>    - L-R and L-N differ only in target representation;
>    - L-P and L-R differ only in pooled versus per-block fitting.
> 4. Prove every §17.7 control, pairing each negative assertion with a positive control that
>    survives the model's transforms. Rerun the applicable inherited regression and namespace
>    guards without a live mutation.
> 5. Produce all 10,747 keys for each new arm, with finite, ordered quantiles and the emitted p50
>    kept separate from the central forecast. Account for failures, exclusions and fallback
>    incidence without changing denominators.
> 6. Score all eleven policies. Independently verify:
>    - the emitted-vector scores and the equal-fold normalization;
>    - every per-fold, hour, block, stress and peak diagnostic, with its denominators and support
>      labels;
>    - coverage together with width;
>    - all six §8 diagnostics for each new arm.
> 7. Apply §17.6's four conditions mechanically.
>    - Report the primary and secondary contrasts with paired intervals, per-fold intervals, and
>      the ratio intervals from the checkpoint's own stored draws.
>    - State the block-split finding from L-R − L-P, with §17.5's reading.
>    - State the verdict, v4 or not adopted, with the first unmet condition; state mixed and
>      negative findings.
>    - Keep the Engineering status, the research finding and the product status (v1 released)
>      distinct. No promotion, freeze or economic claim.
> 8. Deliver §17.5's fit-cost and daily-retrain diagnostic in `reports/block-challenger/`.
> 9. Enforce and report every §17.8 cap from the first job, including controls, failures and
>    independent review. At an exhausted cap, retain the
>    partial evidence and return the applicable non-PASS status.
> 10. Supply the durable evidence and executable reproduction commands: the protocol, lineage,
>     predictions, metrics, diagnostics, uncertainty with stored replicates, criteria, failures,
>     resources and the fit-cost report. Store hash-bound files byte for byte, and disclose
>     defects, repairs and invalidated outputs.
> 11. Deliver §17.9's publication packet and draft MLflow export, with public surfaces and the
>     published export set unchanged, CI green and no public write.
> 12. Obtain one fresh, independent Integration-Critic PASS on a clean detached checkout of the
>     exact final candidate. The review covers this entire checklist and:
>     - independently recomputes the saved-vector metrics, the paired, per-fold and ratio
>       intervals and the §17.6 verdict;
>     - representatively reproduces HG, a block and a pooled LightGBM selection and fit, and the
>       causal and state controls;
>     - re-derives the packet and the export.
> 13. Return the canonical packet (templates §3), together with the publication packet:
>     - both terminal SHAs and a verdict-only delta;
>     - reachable evidence;
>     - all resource totals and elapsed hours;
>     - branch and worktree accounting.
>
>     Stop at CP-21's local result.
>
> ### 17.11 Paths and entry authority
>
> **Write paths:**
>
> - `src/cp21/`, `tests/cp21/`, `scripts/cp21_blocks.py`;
> - `reports/block-challenger/`, `docs/track-b/evidence/cp-21/`;
> - `docs/track-b/research-content/cp21-claims.md`;
> - `scripts/mlflow_export.py` and its tests, only as needed for the draft export, without
>   changing the published export set or any published record;
> - `pyproject.toml` and `uv.lock`, only if a necessary pinned dependency is missing. None is
>   expected: LightGBM is already pinned.
>
> **Ignored material:** `.local/{worktrees,artifacts,tmp}/cp-21/` and `.local/mlruns/cp21`.
>
> **Read-only:** CP-15/16/20 code and reports; `.local/artifacts/cp-20/` (the weather grids and
> the HG component cache); `reports/weather-admission/`.
>
> **Preserve:** v1; the CP-15/16/20 evidence; the public surfaces; Q&A; `progress.md`; every
> locked document.
>
> **Roles.** The accountable executor is the CP-21 Engineering Lead. The reviewer is its fresh,
> independent Integration Critic under `engineering-role.md`.
>
> **Ratification and CP-21 execution authority: GRANTED by the Owner, 2026-09-29.** The grant
> covers:
>
> - CP-21 execution under this section and the issued brief;
> - local `gauntlet/cp-21` candidate and evidence commits;
> - exact immutable packaging of the issued brief (item 1). The ratified anchor and the
>   v21-r5 → v21-r6 amendment record are already on `main`.
>
> **Not authorized:** mainline operations, pushes, tags, publication, remote writes (MLflow,
> Hub), data retrieval, governance edits and later checkpoints. The Lead owns E1–E4 and the
> pre-run feasibility check, and escalates only a concrete blocker beyond this scope.


## Supporting section 23

> ## 23. CP-24 — DDNN-2: a literature-faithful DDNN, and v5 = v4 plus a DDNN-2 member (v21-r11)
>
> ### 23.1 The question, the delegation and the evidence class
>
> **The question.** CP-23's DDNN was admitted but did not help v4 (§21.13). CP-24 asks whether a
> DDNN built as the published work builds it can serve the programme as a member of v4. Such a DDNN
> uses one row per delivery day, a real training-only search, and an ensemble of tuned
> configurations trained up to the day before each forecast. This is the Owner's goal (header).
>
> **What CP-24 decides,** in one checkpoint:
>
> 1. the entry gates (§23.7);
> 2. the per-fold training-only search and a pre-fold gate that must pass before any DDNN-2 or
>    new-policy fit at a warm-up or evaluation origin (§23.4, §23.6);
> 3. at most two pre-registered scored attempts. Each decides `cp24-adoption` (§23.9) for one
>    candidate:
>
>    v5 = (2/3)·c_HG + (1/6)·L + (1/6)·D2.
>
> **Engineering PASS requires neither admission nor adoption.** A complete, valid result can pass
> in any of three forms:
>
> - NOT_ADMITTED;
> - stopped at the pre-fold gate;
> - not adopted.
>
> **Its place in §22's order.** CP-24 runs within §22's item 2 (DDNN), before item 3, by the
> Owner's delegation of 2026-10-04. §22 is otherwise unchanged.
>
> **The roles under the delegation:**
>
> - an independent research agent proposed the directions;
> - the Orchestrator wrote this section and the brief;
> - an independent plan critic reviewed them against the repository;
> - the CP-24 Engineering Lead executes them in its own worktree, with one fresh Integration
>   Critic;
> - the Orchestrator steers only at the points §23.6 names;
> - the Owner lands by hand.
>
> **Disclosed.** Everyone involved knows the results of CP-15, CP-16 and CP-20 to CP-23 on these
> five folds, including CP-23's descriptive diagnosis and its hindsight weight bound of 0.05–0.10.
>
> - **Partly fold-motivated.** The research agent's diagnosis read CP-23's fold-level tables, so
>   DDNN-2's design is partly motivated by fold outcomes. The design is kept at the level of
>   literature-backed mechanisms, and no fold-specific value is used.
> - **Evidence class.** DDNN-2 is the second DDNN decision on the same folds. Its results stay
>   `development_post_selection`, and 4.7T carries the protection.
>
> ### 23.2 Why a second design
>
> CP-23's DDNN differed from the published DDNN (Marcjasz, Narajewski, Weron and Ziel, 2023) and
> the epftoolbox DNN (Lago, Marcjasz, De Schutter and Weron, 2021) in five ways. Each is read from
> CP-23's committed code and tables in the research report
> ([cp-24-research-directions-2026-10-05.md](docs/track-b/cp-24-research-directions-2026-10-05.md)).
>
> 1. **Training.** Each fit trained on `[D−728, D−28)` and early-stopped on the negative
>    log-likelihood (NLL) of `[D−28, D)`. Its median best epoch was 3–8, and there was no refit:
>    - it never trained on the last 28 days, while LEAR and LightGBM refit on their whole window;
>    - on identical inputs it was worse than LightGBM in every fold.
> 2. **Representation.** It used one row per delivery hour with same-hour lags. It saw the previous
>    evening only inside rolling statistics, never as hourly prices. Its errors correlated 0.83
>    with LightGBM's.
> 3. **Selection.** One configuration out of four was chosen per fold, on a 28-day holdout with
>    margins of 0.03–4.9%.
> 4. **Ensemble.** It averaged four seeds of one configuration, and the mean let one member's
>    blow-up through.
> 5. **Role.** Only its median entered v5, at one third: more weight than LightGBM, its
>    better-performing twin.
>
> **This diagnosis selects nothing.** It explains why the design changes. DDNN-2's settings are made
> on training data only (§23.4).
>
> ### 23.3 DDNN-2: what is fixed
>
> - **Code.** §18.2, §18.3 and §21.3 apply, including to the search: NumPy and the standard library
>   only, and analytic gradients, with PyTorch as a test-only reference. The one exception is
>   §21.3's root `uv.lock` pin, which §23.7's test-only lock replaces (the Owner's ruling of
>   2026-10-04, §21.13).
> - **Information.** Exactly v4's sources (§17.3), in DDNN-2's day-level form, as §21.2 already
>   permits for a DDNN.
>   - **What does not bind.** §17.3's and §15.2's per-hour restrictions on cross-hour weather
>     expansion and feature search do not bind DDNN-2. §23.4's inclusion flags choose among these
>     sources on training data only, and add none.
>   - **The subset used:**
>     - the D−1, D−2, D−3 and D−7 price curves;
>     - the TSO day-ahead load forecasts for D, D−1 and D−7;
>     - the three frozen GFS columns for D and their missing indicators (§15.3);
>     - CP-15's LightGBM price statistics at the origin. Over 168 hours: the rolling mean, SD, 5%,
>       50% and 95% quantiles, and the negative-price count. Over 720 hours: the rolling mean and
>       SD;
>     - v4's calendar features: LEAR's weekday dummies and CP-15's LightGBM calendar set, in any
>       encoding of the same information.
>   - **Vintages.** Every input keeps its inherited vintage assumption: CP-15's A65 load forecasts,
>     and CP-20's GFS availability rule. Nothing else enters.
> - **Representation.** One row per delivery day D, with whole-day inputs by Europe/Berlin local
>   hour, under the LEAR design's convention in `src/cp15/data.py`. A repeated local hour averages
>   its two observations, and a missing local hour stays missing until training-only imputation.
>   - **Outputs:** 24 local hours × 4 Johnson SU parameters, in CP-23's parameterisation
>     (`src/cp23/ddnn.py`): ξ = o₁, λ = softplus(o₂) + 10⁻³, γ = o₃, δ = softplus(o₄) + 0.05.
>   - **The loss** covers the present target hours only. A 23-hour day masks its missing slot. On a
>     25-hour day the repeated local hour's target is the mean of its two observations.
>   - **Emission** issues exactly the day's keys, as A1_w and B2_w issue them. On a 25-hour day,
>     both keys of the repeated hour receive that slot's forecast.
> - **Target.** Each row's target and price inputs are normalised with that row's own origin
>   statistics (§4), from prices delivered up to the day before. The search chooses among four
>   forms (§23.4). Quantiles are inverted with the forecast origin's statistics.
> - **Window and refits.** A fresh fit of every member at every origin, on
>   `[max(2019-01-01, D−728), D)`. Optional recency weights belong to the search.
> - **Recency is never dropped.** Each member early-stops on its own seeded random 20% of the
>   window's whole calendar weeks. The holdout pool excludes the most recent 7 days, so every
>   member trains on the days up to D−1 that are outside its own held-out weeks.
> - **Stopping and loss.**
>   - The stopping metric is the mean pinball loss over the seven scored levels, never the NLL.
>   - Patience is 50 epochs, the maximum is 1,000, and the best epoch is kept.
>   - Training starts with 20 NLL epochs, then minimises κ·NLL + (1 − κ)·the mean pinball loss
>     over a 19-level grid that contains the seven scored levels. The search chooses κ.
>   - Best-epoch tracking and patience start after the 20 warm-start epochs.
> - **Guards.**
>   - Every continuous input is winsorised at its training rows' 0.5% and 99.5% quantiles. Binary
>     inputs and missing indicators are never winsorised.
>   - Emitted quantiles are capped at ±1.25 times the largest absolute value of the member's
>     normalised target z on its training rows, before any asinh.
>   - Crossings are restored by sorting.
>
>   Every activation of a guard is recorded.
> - **Ensemble.** Each fold uses its four best configurations (§23.4), with two seeds each: eight
>   member fits per origin.
>   - Members combine by the per-level median of their quantiles in EUR/MWh. With eight members,
>     that is the mean of the two middle values.
>   - The p50 and the central forecast D2 are that median.
>   - The ensemble is fixed through the fold, from its first origin.
>
> ### 23.4 The training-only search
>
> - **When and from what.** Once per fold f, before its warm-up start D0_f, by a procedure
>   identical for every fold. Every search fit trains on data before its batch, so nothing dated on
>   or after D0_f − 56 enters. §23.6's weather-coverage rule applies.
> - **Validation batches.** Consecutive 28-day blocks tile backward from D0_f − 57, the day before
>   the gate window.
>   - A block that meets any fold's warm-up or evaluation day, or that starts before 2020-01-01, is
>     skipped.
>   - B_f = min(11, the blocks kept), taking the most recent. This gives B = 3, 7, 11, 11 and 11
>     for folds 1–5.
>   - The protocol records every batch's dates.
> - **One fit per trial and batch.** Each trial is fitted once per batch, with a recorded fixed
>   seed, on `[max(2019-01-01, b − 728), b)`, where b is the batch's first day. That fit then
>   forecasts the batch's 28 days, as the published batch-rolling scheme does.
> - **The sampler.** Seeded random search, written in NumPy, with 32 to 128 trials per fold per
>   round. 4.6R′'s record fixes the number.
>   - Successive halving: every trial runs on the min(4, B_f) most recent batches, and the best
>     third runs on all B_f.
>   - The ranking metric is the mean seven-level pinball loss in EUR/MWh, after inversion, over the
>     batches each trial ran. MAE is reported beside it.
>   - The fold's ensemble is the four best distinct configurations among the trials that ran all
>     B_f batches, ranked over those batches. Ties go to the network with fewer parameters.
> - **The space,** within these bounds (the protocol fixes the exact space and priors):
>
>   | Hyperparameter | Range |
>   |---|---|
>   | Hidden layers | 1 or 2 |
>   | Width | 16–512 units (log scale) |
>   | Activation | ELU, ReLU, softplus or tanh |
>   | Input dropout | Off, or 0.05–0.5 |
>   | L1 and L2 rates | Each off, or on a log scale |
>   | Adam learning rate | 1e-4–1e-2 (log scale) |
>   | Batch size | 32, 64 or 128 |
>   | Loss weight κ | 1, 0.5 or 0 |
>   | Recency half-life | None, 365 or 180 days |
>   | Optional input groups | Inclusion flags for the D−2, D−3 and D−7 prices, the D−1 and D−7 load forecasts, the GFS block, the origin price statistics, and the day-type and month encodings |
>   | Target transform | z or asinh(z), where z is centred and scaled either by §4's level and scale, or by the median and MAD of the last 168 hours with a floor (Uniejewski, Weron and Ziel, 2018) |
>
>   The D−1 prices and D's load forecast always enter.
> - **What fold f's search never does:**
>   - read any outcome dated on or after D0_f − 56, which covers fold f's gate window, its warm-up
>     and its evaluation;
>   - narrow its space after any fold score exists, except as §23.6 allows attempt 2.
>
>   Like every production fit, a search fit trains on all history before its batch. That history
>   includes earlier folds' warm-up and evaluation days, but no validation batch contains such a
>   day.
>
> ### 23.5 The candidate, the arms and the references
>
> | ID | Role | Central forecast and intervals |
> |---|---|---|
> | v4 | Comparator: CP-21's saved HGL vectors | `(2/3)·c_HG + (1/3)·L`, H layer, as committed |
> | v3 | Reference: saved vectors | As committed |
> | A1, B2 | References: CP-15's no-weather LEAR models, as in CP-23 | As committed |
> | D | Reference: CP-23's DDNN, saved vectors (`evidence/cp-23`) | As committed |
> | v5 | The single eligible candidate of every attempt | `(2/3)·c_HG + (1/6)·L + (1/6)·D2`, with HG's H layer re-estimated on v5's own errors |
> | D2 | Study arm: DDNN-2 alone, never eligible | D2, with its own Johnson SU quantiles and p50 |
> | v3+D2 | Attribution: DDNN-2 in LightGBM's place, never eligible | `(2/3)·c_HG + (1/3)·D2`, H layer on its own errors |
>
> c_HG is the mean of HG's weather components A1_w and B2_w (§17.2). L is v4's LightGBM member,
> `mean(L-N, L-R)`. Both come from the saved vectors.
>
> **The weight.** v4 gives two thirds to LEAR and one third to LightGBM, with equal weights for the
> members inside each third. DDNN-2 joins LightGBM's third by the same rule. The weight is fixed
> before any fit and is never estimated on any data. Two properties follow:
>
> - `c_v5 − c_v4 = (1/6)·(D2 − L)`;
> - LEAR keeps its two thirds.
>
> The weight never changes in CP-24.
>
> **Excluded:**
>
> - learned, per-block or per-fold weights, and any weight estimated on outcomes (4.8, §22);
> - new information (stage 7);
> - other model families, a per-hour network family, and TabPFN;
> - DDNN-2's distribution as v5's interval provider, which stays descriptive (§23.8).
>
> ### 23.6 Steering, the pre-fold gate and the scored attempts
>
> **The pre-fold gate.** Each fold has a gate window G_f = [D0_f − 56, D0_f):
>
> - 2020-03-30..2020-05-24;
> - 2020-12-29..2021-02-22;
> - 2022-03-30..2022-05-24;
> - 2025-01-25..2025-03-21;
> - 2025-10-07..2025-12-01.
>
> Together they make 280 days, none of them a warm-up or evaluation day of any fold.
>
> **What runs on each gate day.** On each gate day D the Lead issues two sets of forecasts, each
> from a fresh fit at that day's origin:
>
> - DDNN-2, with the round's ensemble for the fold;
> - v4's members, with their unchanged code: A1_w and B2_w through `cp21.components`, and L-N and
>   L-R through CP-21's code.
>
> **Proving v4's code path.** The members' committed vectors are reproduced:
>
> - A1_w and B2_w are the `A1` and `B2` columns of
>   `reports/distribution-challenger/members.parquet`;
> - L-N and L-R are in `reports/block-challenger/predictions.parquet`.
>
> Each gate fit trains on all history before D, as production does, including earlier folds'
> warm-up and evaluation days. Nothing of fold f on or after D0_f is read.
>
> **Weather coverage of pre-fold fits.** CP-20's retained grids cover every warm-up and evaluation
> window, but not every date. Delivery days 2022-09-29..2023-03-24 have no frozen weather record,
> and §15.3 makes unattempted weather BLOCKED, never imputed.
>
> - **The rule.** Every pre-fold fit leaves out of its training window every delivery day that has
>   no frozen weather record, whatever its input groups. Pre-fold fits are 4.6R′, the search and
>   the gate. No other window changes.
> - **Where it applies.** It affects fold 4's 56 gate days and the batches of folds 4 and 5 whose
>   windows reach back before 2023-03-25.
> - **v4's members on those gate days** run their unchanged code through a scoped, logged wrapper.
>   The wrapper marks the uncovered days ineligible before the call. Its parity with the committed
>   vectors is proven at covered origins, where it changes nothing.
> - **Limits.** No warm-up or evaluation fit is affected, and no weather is retrieved.
> - **Reporting.** The pre-fold report states the excluded training days of every fit.
>
> **The gate passes if all four of these hold,** pooled over the 280 days as point estimates:
>
> - **G0:** every forecast is finite and ordered;
> - **G1:** v5's central MAE ≤ v4's central MAE, both built from the gate-day members;
> - **G2:** D2's MAE ≤ 1.10 × L's MAE;
> - **G3:** the quantile cap binds on fewer than 0.1% of the members' emitted hour-levels.
>
> The gate is a screen, not a claim. It can only prevent a fold look.
>
> **Rounds.** A round is one search per fold, then the gate, then a pre-fold report. The report
> covers:
>
> - the search ledger, and each fold's ensemble and validation scores;
> - the gate table, by fold and pooled;
> - the error correlations of D2 with HG and L on the gate days;
> - the excluded training days;
> - the costs.
>
> No DDNN-2 or new-policy fit is made at a warm-up or evaluation origin in a round. Reproducing
> v4's or HG's committed vectors at those origins is not such a fit, because it reads no outcome
> that is not already committed. That covers item 2's slice, the gate's code-path proof and the
> wrapper's parity check. There are at most three rounds before
> attempt 1 and one round before attempt 2. Between rounds the design may change within
> §23.3–§23.4, as S1 decides on the Lead's proposal.
>
> **S1: the Orchestrator's steering after each round.** One of three answers:
>
> - **freeze** the latest round's design, only if that round's gate passed;
> - **another round,** with named changes within §23.3–§23.4, on pre-fold evidence only;
> - **stop.**
>
> A failed gate in the last round allowed before an attempt means that attempt cannot run.
>
> - **Before attempt 1,** a stop or an attempt that cannot run ends CP-24 as "stopped at the
>   pre-fold gate", with no fold look.
> - **Before attempt 2,** the same ends the route with attempt 1's result. CP-24's outcome is then
>   the branch "DDNN-2 member on v4", with attempt 1's first unmet condition, and attempt 2 is
>   recorded as stopped at its gate.
>
> **The freeze and scored attempt k.**
>
> - The Lead commits the attempt's frozen protocol (§23.7) before its first warm-up or evaluation
>   fit.
> - Then come the warm-up and evaluation fits, the policies, and one scoring of all five folds.
> - The fitting and scoring entry points refuse to run unless attempt k's frozen protocol is
>   committed and unchanged.
>
> **S2: the Orchestrator's steering after attempt 1,** if attempt 1 is not adopted.
>
> - **When attempt 1 counts as not adopted.** Any of conditions 1, 2, 4 or 5 is unmet on its
>   committed scores, or a completeness clause of condition 3 is. Condition 3's Integration clause
>   is applied at the end, and never by itself triggers attempt 2.
> - **The answer** is one of two:
>   - stop;
>   - attempt 2, once, with named design changes and the recorded diagnosis behind them. Attempt 2
>     then runs its one round and must pass the gate.
>
> **Budget at each step.** Before each round and each attempt, the Lead projects it against every
> remaining ceiling, including the review reserve, and starts it only if it fits. A step that does
> not fit is not available at S1 or S2.
>
> **Bounds that no steering moves:**
>
> - **Attempts.** At most two scored attempts. Each scores the folds once. A repair after scoring
>   that changes any frozen element is a new attempt.
> - **What attempt 2 may change.** Only DDNN-2's design within §23.3–§23.4:
>   - the inputs, the transform, the loss, the training recipe, the guards or the ensemble;
>   - the search's sampler, trial budget or priors, or a wider space.
>
>   Its search reruns from scratch on pre-fold data. It never narrows the space, never removes a
>   configuration that attempt 1's folds disfavoured, and never seeds a trial from attempt 1's
>   ensembles. It never changes:
>   - the weight or v5's formula;
>   - the comparator, the population, the metrics, the gate or the rule.
> - **No outcome-tuned quantity.** No attempt sets any quantity to a value estimated on any warm-up
>   or evaluation outcome, for example a hindsight weight. Anything tuned is tuned on data before
>   D0_f:
>   - the search, on data before D0_f − 56;
>   - S1's choices, on the search ledgers and the gate results, which end at D0_f − 1.
> - **After an adoption,** no further attempt runs.
> - **Nothing else in §23 changes during CP-24.** An S1 or S2 answer may raise only three of
>   §23.11's ceilings, each by a stated amount: member fits up to 60,000, machine-hours up to 200,
>   and active hours up to 70. Every other line of §23.11 never changes, including the attempts,
>   the rounds, data, network and cost.
>   - The answer is committed under `steering/` before use.
>   - The Critic checks the caps against §23.11 together with those committed answers.
>
> **The record.**
>
> - **Committed before acting.** Every S1 and S2 exchange is committed verbatim under
>   `docs/track-b/evidence/cp-24/steering/`, with its time, round and attempt, before the Lead
>   acts on it.
> - **The Orchestrator's limits.** The Orchestrator:
>   - chooses among the Lead's proposals and never prescribes implementation;
>   - does not review the code;
>   - does not see the Critic's work before the verdict file exists.
>
>   The Lead may refuse a steering answer that breaks this section, and says why.
> - **What the delegation sets aside.** For CP-24 only, and without editing the file, the Owner's
>   delegation (header) sets aside two rules of `orchestrator-role.md`:
>   - "You must not launch, spawn, open, or impersonate an Engineering-Lead, Builder, Critic,
>     NotebookLM, research-agent, or content-executor session";
>   - "Yarden carries one brief down and one checkpoint return back".
>
>   For the Critic fallback only, it also sets aside a third rule: "The Orchestrator never reads or
>   manages internal agent exchanges".
>
>   In their place, the Orchestrator:
>   - launches the research agent, the plan critic and the Lead;
>   - exchanges §23.6's steering messages;
>   - launches the Integration Critic only if the Lead cannot. It then passes exactly
>     `critic-open`'s printed prompt, and reads nothing of the review before the verdict file
>     exists.
>
>   No other channel exists. The Orchestrator attends the run, and the Owner is not asked to act
>   before the LAND.
>
> ### 23.7 Entry gates and the frozen protocol
>
> **4.6L′: provenance.** An addendum to CP-23's record, at
> `reports/ddnn2/licence-admission.md`. It records:
>
> - the method sources;
> - that no third-party code or weights were copied;
> - how the test-only reference is reused.
>
> If provenance cannot be established, or the reference's licence is unresolved, DDNN-2 is
> NOT_ADMITTED. The cap is 2 active hours.
>
> **Correctness (§21.3, extended):**
>
> - **The import audit** covers the search and every DDNN-2 module.
> - **Finite-difference checks** cover:
>   - the masked 24-hour Johnson SU loss;
>   - the pinball loss through the Johnson SU quantile function;
>   - L1 and L2;
>   - dropout with fixed masks;
>   - every activation in the space;
>   - every target transform and its inverse.
> - **PyTorch reference checks** cover the forward pass, the losses and their gradients, and short
>   optimizer trajectories, at tolerances frozen before any comparison run.
>   - **The pattern is CP-23's:** an explicitly invoked, non-collected script, like
>     `tests/cp23/torch_reference_checks.py`, and a collected test of its committed record. CI
>     installs only the root lock, so it stays green.
>   - **The lock** is CP-23's test-only lock `tests/cp23/torch-reference/` (its `uv.lock` has
>     SHA-256 `b3164a375e871396e685d0e887972b092fcd0c24a7fe0047167e8fc41c25dfed`), or a new
>     test-only lock under `tests/cp24/` that pins the same versions.
>   - **The root `pyproject.toml` and `uv.lock` never change:** CP-10's and CP-15's evidence binds
>     them.
>   - **A missing reference fails** the explicit run; it never skips.
>
> **4.6R′: training-only resource entry,** at `reports/ddnn2/resource-admission.md`. It runs on
> pre-fold data, after the correctness checks.
>
> - **It measures:**
>   - peak memory;
>   - fit and prediction time at the space's extremes;
>   - finite, ordered emission.
> - **It projects two routes** against §23.11, each with the review reserve:
>   - the minimal route: one round, then attempt 1;
>   - the maximal route: three rounds and attempt 1, then one round and attempt 2.
> - **Its timing fits** forecast only validation-batch days, never a gate, warm-up or evaluation
>   day.
> - **Its record** (`resource-admission.md`) fixes three things, and each frozen protocol repeats
>   them:
>   - the trial count, at least 32 per fold per round, sized so that the maximal route fits;
>   - the largest route that fits, if the maximal route does not fit at 32 trials;
>   - the review reserve.
> - **NOT_ADMITTED.** If the minimal route does not fit, DDNN-2 is NOT_ADMITTED with its cause,
>   never a smaller experiment.
>
> **The frozen protocol of each scored attempt** is committed before its first warm-up or
> evaluation fit. It records:
>
> - the representation, the input groups and their encoding;
> - the search: space, priors, sampler, trial count, seeds, batch dates and ranking metric;
> - every fold's chosen ensemble, with its validation scores;
> - the gate's dates, its excluded training days and its results;
> - the training recipe, the guards and the emission;
> - the reference tolerances;
> - the arms and the weight;
> - the attempt number, the level and the rule's text;
> - the budget accounting.
>
> ### 23.8 Population, metrics and diagnostics
>
> **For every scored attempt,** §21.5's population, metrics and uncertainty apply:
>
> - 10,747 keys and 638 origins;
> - released errors at D−2 or earlier;
> - the emitted p50's S_MAE and S_WIS, equal-fold and B0-normalised;
> - the shared 2,000-replicate CP-20 index set, with seed 15042 and 7-day blocks within folds;
> - per-fold paired daily-loss intervals;
> - all six §8 diagnostics;
> - coverage with width;
> - the stress period and the peak.
>
> v5 and v3+D2 take their warm-up errors from DDNN-2 fits at the warm-up origins. Ratio intervals
> are reported at 97.5%, the decision level, and at 95% for comparison with CP-21 to CP-23.
>
> **Contrasts,** each read under §17.5:
>
> | Contrast | Role |
> |---|---|
> | v5 − v4 | The adoption decision (§23.9) |
> | v5 − v3 | Reference |
> | D2 − L, D2 − HG, D2 − v4 | DDNN-2 alone, against its same-information twin, LEAR and v4 |
> | D2 − D | DDNN-2 against CP-23's DDNN |
> | (v3+D2) − v4, beside (v3+D) − v4 | DDNN-2, then CP-23's DDNN, in LightGBM's place |
> | (v3+D2) − v3 | DDNN-2 as v3's third member |
> | v5 − (v3+D2) | Whether LightGBM still adds once DDNN-2 is present |
>
> **Diagnostics,** descriptive and choosing nothing, delivered per attempt to `reports/ddnn2/`:
>
> - D2's calibration: coverage by level and the PIT histogram;
> - error correlations among D2, D, HG, A1_w, B2_w and L, pooled and by fold;
> - MAE by local hour beside L and HG;
> - extrapolation on extreme days, beside CP-23's record;
> - the 2022 peak, fold 3 and fold 4;
> - every guard activation and crossing;
> - the search: each fold's ensemble, with its validation and gate scores beside its fold scores;
> - member stability;
> - a shape blend, descriptive only and never eligible: v4's p50 plus the average of the H layer's
>   and D2's quantile offsets from their own medians;
> - fit cost, and a cold daily cycle at 20 or more origins across the folds.
>
> ### 23.9 Pre-registered rule `cp24-adoption`, set 2026-10-05
>
> v5 of scored attempt k (k ≤ 2) is adopted in research as v5 if, and only if, all five of these
> hold against v4 on identical rows:
>
> 1. **Joint improvement over v4, at the attempts-adjusted level.** The paired v5 − v4 differences
>    use two-sided 97.5% intervals: the 1.25% and 98.75% percentiles of the shared replicates.
>    - The upper endpoint of ΔS_WIS is < 0.
>    - The upper endpoint of ΔS_MAE is ≤ 0.
> 2. **No regression.** v5 meets all six original §8 diagnostics.
> 3. **A complete, valid evaluation.**
>    - Engineering PASS with a fresh binding Integration verdict.
>    - All 10,747 keys issued with finite, ordered quantiles.
>    - Every guard activation reported.
> 4. **No resolved per-fold degradation.** No fold has a 95% paired daily-loss interval (v5 − v4)
>    lying entirely above zero, in MAE or in WIS.
> 5. **A practical size.** Both point estimates improve v4's score by at least 0.5%:
>    - ΔS_MAE ≤ −0.005·S_MAE(v4);
>    - ΔS_WIS ≤ −0.005·S_WIS(v4).
>
> **Why 97.5%.** The level in condition 1 splits 5% across the cap of two attempts. It is fixed in
> advance, whatever number of attempts runs. Condition 4 stays at 95%, its stricter side.
>
> **What the split does not cover.** The split controls the number of looks, not the adaptation of
> attempt 2 to attempt 1's fold results. 4.7T carries that protection. Attempt 2 is the
> Owner-delegated route of §23.6, never the Lead's discretion.
>
> **Otherwise,** attempt k's v5 is not adopted, with its first unmet condition and its values.
>
> **How the rule is applied:**
>
> - mechanically, never re-weighted, re-thresholded or overridden after results;
> - D2, v3+D2 and D are never eligible;
> - a mixed result is no demonstrated joint preference, never equivalence;
> - an INCOMPLETE or BLOCKED return yields no decision and nothing to publish.
>
> **CP-24's outcome** is one of four:
>
> - adopted in attempt k;
> - the branch "DDNN-2 member on v4", with each scored attempt's first unmet condition;
> - stopped at the pre-fold gate;
> - DDNN-2 NOT_ADMITTED.
>
> In every outcome, whatever DDNN-2 vectors exist are stored for 4.8.
>
> **What adoption means:**
>
> - **A research status, and provisional.** v1 remains the released product and the demo, and no
>   designation, freeze or Live follows (§16).
> - **The opponent.** At CP-24's landing, "same information, same opponent" comes to name v5.
> - **4.7T** is the confirmation. Its frozen manifest carries v3, v4 and v5, with the number of
>   DDNN looks disclosed, and nothing is re-tuned for it.
> - **Naming, proposed:**
>   - adopted: "v5 · DDNN-2 member added", with predecessor v4. The A3 transition is titled "From
>     v4 to v5: adding a distributional neural network";
>   - not adopted: the branch "DDNN-2 member on v4".
>
> ### 23.10 Causal and integrity controls
>
> §21.7's controls and §20.7's applicable ones apply to DDNN-2, v5 and v3+D2. Each negative
> assertion is paired with a positive control. In addition:
>
> - **The search and the gate, fold by fold.**
>   - **Negative controls.** Mutating any outcome on or after D0_f − 56 changes none of fold f's
>     search results or its ensemble. Mutating any outcome on or after D0_f changes none of fold
>     f's gate results.
>   - **Positive controls.** Each of these can change the results:
>     - mutating a validation-batch outcome can change fold f's search;
>     - mutating a fold-f gate-day outcome can change fold f's gate;
>     - mutating an earlier fold's evaluation day inside a later fold's training window can change
>       that later fold's fits.
> - **Statistics and transforms:**
>   - every scaler, winsorisation quantile, imputation and transform statistic is fitted on the
>     fit's own training rows, never on its held-out weeks or forecast rows;
>   - the origin's level and scale use prices up to D−1 only;
>   - inversion is exact at every quantile.
> - **Recency.** Every member trains on days up to D−1 outside its own held-out weeks. As the
>   positive control, mutating such a day moves the fit.
> - **Weather coverage.** No pre-fold fit trains on an uncovered day, and the wrapper for v4's
>   members changes nothing at covered origins. The paired positive controls:
>   - v4's unwrapped member code refuses a fold-4 gate day;
>   - removing the exclusion from a fold-4 search fit changes its training rows.
> - **DST.** Fixtures cover the inputs, the loss mask and the emitted keys:
>   - on real data, every transition day from 2019-03-31 to 2026-03-29. 2022-10-30 has no weather
>     record, so its fixture covers prices, load, the loss mask and the keys;
>   - a synthetic calendar fixture for 2026-10-25.
> - **Pre-registration.** Each attempt's frozen-protocol commit is an ancestor of the first commit
>   or ledger entry that contains any of its warm-up or evaluation forecasts, and precedes it in the
>   ledger. The fitting and scoring entry points refuse otherwise.
> - **v4's members on the gate days.** They reproduce committed fold vectors by the same code path,
>   bit for bit or within a measured and recorded tolerance.
> - **Composites:**
>   - `c_v5 − c_v4 = (1/6)·(D2 − L)` within tolerance;
>   - v5 and v3+D2 run on HG's H-layer code path.
> - **Determinism.** One BLAS thread per worker, fixed seeds, a fixed batch order and restart
>   replay.
>
> ### 23.11 Ceilings and calendar
>
> These are maxima, not targets. 4.6R′ projects against them, and §23.6 allows a stated raise.
>
> | Dimension | Maximum |
> |---|---|
> | New models | 1 (DDNN-2). 0 other families, information or learned weights |
> | Scored attempts | 2 |
> | Pre-fold rounds | 3 before attempt 1; 1 before attempt 2 |
> | Policies per attempt | 1 eligible (v5); 2 study and attribution arms (D2, v3+D2); saved references v4, v3, A1, B2 and D |
> | DDNN-2 member fits | 40,000 in total, including 4.6R′, rounds, gates, attempts, controls, reproduction, failures and review |
> | v4-member fits on gate days | One pass at the 280 gate origins, reused across rounds, plus its parity checks |
> | Replay | 12,000 new policy-days, gate days included |
> | References and uncertainty | 3 reference passes. 6 bootstrap passes of 2,000 replicates, where a pass is one run over all of a scored attempt's contrasts: per scored attempt, two by the Lead and one for review |
> | Compute | 150 aggregate machine-hours; at most 4 concurrent workers; BLAS 1; CPU only; no GPU, MPS or cloud |
> | Memory and disk | 10 GiB RSS; 10 GiB added peak disk |
> | Data, network and cost | 0 data bytes. If the local cache lacks CP-23's pinned PyTorch CPU wheels, the one permitted download is that same pinned set, from PyPI. 0 remote writes; $0 |
> | Effort | About 35 active hours; hard ceiling of 50 |
>
> **Before dependent work,** the Lead completes §14.6 E1–E4 for CP-24, with the Lead and Critic
> sessions named by the Lead.
>
> ### 23.12 Publication packet and MLflow
>
> §21.9 applies, with these changes:
>
> - **Pinned rules, which the issued brief also records:**
>   - PUBLISH_RULES 1.3, SHA-256
>     `5a660864f8b82943174741320c71087a3d0508f707edeb997cb2c1395c1c73b4`;
>   - the packet template `docs/track-b/publication-packet-template.md`, SHA-256
>     `4efb01855ae2d9a6f54b5624607a93046b1fffa881e34af0c6798c513c7829cf`.
> - **The packet:** `docs/track-b/evidence/cp-24/publication-packet.md`, in every outcome, with the
>   claim map `docs/track-b/research-content/cp24-claims.md`. A stop is recorded as such. It
>   carries:
>   - draft registry entries for each scored attempt;
>   - the derived quantities: the gate results, the number of rounds and scored attempts, and the
>     adjusted level.
> - **MLflow:**
>   - the experiment is `delu-generations`;
>   - local tracking only, in `.local/mlruns/cp24`;
>   - a draft export, `reports/ddnn2/mlflow-export-draft/cp24.json`. A CP-24 module builds it by
>     importing `scripts/mlflow_export.py`'s functions unchanged;
>   - no public write.
> - **Public surfaces are unchanged.** Publication follows the Owner's LAND and three Owner
>   decisions:
>   - v5's encoding, if v5 is adopted;
>   - whether the not-adopted branches are published;
>   - automation items 6 and 7 (§22).
>
> ### 23.13 Complete CP-24 acceptance checklist
>
> All eighteen items are mandatory. Engineering PASS requires neither admission nor adoption: a
> complete, valid NOT_ADMITTED, gate-stopped or not-adopted result can pass.
>
> **After a stop:**
>
> - a NOT_ADMITTED stop under item 3 makes items 4–14 not applicable;
> - a NOT_ADMITTED stop under item 5 makes items 6–14 not applicable;
> - a stop under item 7 before attempt 1 makes items 8–14 not applicable.
>
> Each not-applicable item is recorded with the stop's evidence, and items 15–18 apply in full.
>
> 1. **Verify the starting state** and preserve prior evidence and other sessions' work.
>    - Verify the ratified anchor's SHA-256 against the brief.
>    - Record the baseline with `scripts/gauntlet.py start cp-24`.
>    - Work only in the worktree `.local/worktrees/cp-24/lead`, on `gauntlet/cp-24`.
>    - Package the issued brief byte for byte as `docs/track-b/evidence/cp-24/issued-brief.md`.
> 2. **Verify the inputs:**
>    - population, manifest and frozen weather, including the coverage gap of §23.6;
>    - saved-vector identities, including CP-23's D, reproduced from the objects preserved at the
>      evidence tags where a live identity check no longer applies;
>    - an independent representative HG and v4 slice;
>    - no retrieval, and nothing after 2026-04-07.
> 3. **Complete 4.6L′.**
> 4. **Prove the code's correctness** under §23.7: the import audit, the finite-difference checks,
>    and the PyTorch reference checks, installed so that they cannot be skipped silently.
> 5. **Complete 4.6R′** on pre-fold data, with PASS or NOT_ADMITTED and its cause. On
>    NOT_ADMITTED, stop, with no gate and no comparison.
> 6. **Run every pre-fold round** (§23.4, §23.6), with no DDNN-2 or new-policy fit at a warm-up
>    or evaluation origin:
>    - each fold's search, recorded in a ledger;
>    - the gate, with v4's members proven on the same code path and the weather-coverage rule
>      applied;
>    - the pre-fold report.
> 7. **Commit every S1 exchange** and, for each attempt that runs, its frozen protocol, before any
>    of its warm-up or evaluation fits. Stop when §23.6 says the route ends.
> 8. **Implement exactly DDNN-2, v5 and the arms,** and prove composite parity.
> 9. **Prove every control** of §23.10 and the inherited ones, each negative paired with a
>    positive.
> 10. **Produce all 10,747 keys for every new policy** in every scored attempt, with finite,
>     ordered quantiles. Keep the emitted p50 separate from the central forecast.
> 11. **Score every policy of every attempt,** and independently verify:
>     - the scores and the diagnostics;
>     - coverage with width;
>     - all six §8 diagnostics for each new policy.
> 12. **Apply `cp24-adoption` mechanically** to every scored attempt. State each decision with its
>     first unmet condition, and every §23.8 contrast with its reading. Keep the Engineering,
>     research and product statuses distinct.
> 13. **Respect the attempt bounds.** Commit the S2 exchange and any attempt 2 under §23.6's
>     bounds. Run at most two scored attempts, and none after an adoption.
> 14. **Deliver §23.8's diagnostics** to `reports/ddnn2/`.
> 15. **Store whatever DDNN-2 vectors exist** for 4.8. **Enforce and report every §23.11 cap,**
>     with any committed raise, and respect the calendar.
> 16. **Supply the durable evidence,** with executable reproduction commands and byte-exact
>     storage.
>     - Deliver §23.12's packet, which records any stop, and the draft export.
>     - These stay unchanged: the public surfaces, the published export set,
>       `scripts/mlflow_export.py`, and the root `pyproject.toml` and `uv.lock`.
>     - CI is green, and there is no public write.
> 17. **Obtain one fresh, independent Integration-Critic PASS** on a clean detached checkout of
>     the final candidate. Launch it with `scripts/gauntlet.py critic-open`, `critic-brief` and
>     `critic-close`. The review independently:
>     - recomputes every scored attempt's metrics, intervals and verdict;
>     - checks the gate's results and the steering record against §23.6;
>     - checks pre-registration by Git ancestry and the ledgers;
>     - reruns the reference checks;
>     - reproduces a representative search trial, a representative DDNN-2 ensemble fit and its
>       emission;
>     - re-derives the packet.
> 18. **Return the canonical packet** (templates §3), checked with `scripts/gauntlet.py return`.
>     It carries:
>     - both terminal SHAs and the verdict-only delta;
>     - resource totals, the number of rounds and scored attempts;
>     - branch, worktree and stash accounting.
>
>     Stop at CP-24's local result.
>
> ### 23.14 Paths and entry authority
>
> **Write paths:**
>
> - `src/cp24/`, `tests/cp24/`, `scripts/cp24_*.py`;
> - `reports/ddnn2/`, `docs/track-b/evidence/cp-24/`;
> - `docs/track-b/research-content/cp24-claims.md`.
>
> **Never written:**
>
> - the root `pyproject.toml` and `uv.lock`;
> - `scripts/mlflow_export.py`, and every file that CP-21's to CP-23's artifact manifests bind;
> - `src/cp23/` and every earlier checkpoint's code and reports, which are reused by import.
>
> **Ignored material:** `.local/{worktrees,artifacts,tmp}/cp-24/` and `.local/mlruns/cp24`.
>
> **Read-only:**
>
> - CP-15 to CP-23 code and reports;
> - `evidence/cp-20`, `evidence/cp-21`, `evidence/cp-22` and `evidence/cp-23`;
> - `.local/artifacts/cp-20/` to `cp-23/`.
>
> **Preserve:** v1; all earlier evidence; the public surfaces; Q&A; `progress.md`; every locked
> document.
>
> **Roles:**
>
> - **The executor.** The accountable executor is the CP-24 Engineering Lead, in its own worktree.
> - **The reviewer.** Its fresh, independent Integration Critic.
> - **Steering.** The Orchestrator steers only under §23.6.
>
> **Ratification and CP-24's execution: GRANTED by the Owner's delegation of 2026-10-04** (the
> header's authority). The grant covers:
>
> - CP-24's execution under this section and the issued brief;
> - local `gauntlet/cp-24` candidate and evidence commits, and exact packaging of the issued brief;
> - the steering of §23.6, and the launches it names;
> - the Orchestrator's commit and push of five things:
>   - this revision;
>   - its amendment record;
>   - the research report;
>   - the brief's record in `progress.md`;
>   - the programme handoff's consistency edits.
>
> **Never authorized here:**
>
> - the LAND, which stays the Owner's by hand (`AGENTS.md`);
> - any push or tag by the Lead or the Critic;
> - publication and remote writes;
> - data retrieval;
> - any governance edit beyond this revision and its record;
> - later checkpoints.
>
> ### 23.15 Decisions recorded, 2026-10-04 and 2026-10-05
>
> | # | Decision | Set by | Ratified outcome |
> |---|---|---|---|
> | D1 | The route | Owner | DDNN-2, delegated to the Orchestrator: research agent, plan, independent critic, execution agent, without the Owner until the report and the LAND request |
> | D2 | This anchor | Owner | v21-r11, under a suspension that includes commit, push and every need |
> | D3 | Discretion | Owner | The representation, the search, the ensemble, the weight in v5 and the ceilings are the Orchestrator's, and may change during the work |
> | D4 | Representation and training | Orchestrator, under the delegation | Day-level rows with 96 outputs. Every member trains on data up to D−1, with random whole-week early stopping on the scored pinball loss (§23.3) |
> | D5 | Search and ensemble | Orchestrator, under the delegation | Per-fold random search on batch-rolling validation that avoids every fold's days. The top four configurations with two seeds each, combined by the per-level median (§23.4) |
> | D6 | The candidate and its weight | Orchestrator, under the delegation | v5 = (2/3)·c_HG + (1/6)·L + (1/6)·D2: DDNN-2 shares LightGBM's third. Fixed, never estimated (§23.5) |
> | D7 | Steering and attempts | Orchestrator, under the delegation | A pre-fold gate; at most three rounds before attempt 1 and one before attempt 2; at most two scored attempts; steering at S1 and S2 only (§23.6) |
> | D8 | The rule | Orchestrator, under the delegation | `cp24-adoption`: CP-23's four conditions with condition 1 at 97.5%, plus a 0.5% practical size (§23.9) |
> | D9 | Ceilings | Orchestrator, under the delegation | §23.11, raisable at S1 or S2 to stated maxima (§23.6) |
> | D10 | The reference tests | Orchestrator, under the delegation | CP-23's test-only lock, or a new one under `tests/cp24/` with the same pins; never the root lock |
> | D11 | Weather coverage | Orchestrator, under the delegation | Pre-fold fits leave out the days without a frozen weather record (2022-09-29..2023-03-24); no retrieval (§23.6) |
> | D12 | Publication | Orchestrator, under the delegation | None in CP-24; the Owner decides after the LAND |


## Supporting section 24.2

> ### 24.2 The short path, the development boundary and the red line
>
> **The short path (Owner, 2026-10-12).** No new data source is collected, tested or admitted in this
> programme. Stage 3's shortlist (`docs/track-b/data-source-research-2026-10-11.md`) stays a
> documented finding: a possible extension after the final product. No enquiry, registration or
> purchase follows from it.
>
> **Development data:** delivery days 2019-01-01 to 2026-09-06, the existing snapshot's span.
>
> - **The period 2026-04-08 to 2026-09-06 joins development by this revision** (Owner, 2026-10-12).
>   - The research never used it: the earlier boundary was `data/partitions.json`'s `eda_cutoff`,
>     2026-04-07.
>   - v1 used it for its CQR calibration (2026-04-09 to 2026-06-07) and its one-shot holdout
>     (2026-06-09 to 2026-09-06), whose results are published (`docs/cp2-model-report.md` §4).
>   - It therefore cannot serve as a fresh test, and serves as development data instead.
> - **v1's historical records stay unchanged,** and so do `data/partitions.json` and
>   `data/snapshot.parquet` (§1). CP-25 writes a new partition specification beside them. v1's
>   holdout results stay v1's record, while the days themselves are development data.
> - **Displays and publication.** Before the final test, no research number, chart or choice uses
>   data after 2026-09-06. That replaces §19.8's 2026-04-07, and PUBLISH_RULES invariant 10 moves
>   with it (PUBLISH_RULES 1.5).
>
> **The red line.** Delivery days from 2026-09-07 stay closed until 4.7T opens (§24.9).
>
> - **Data on disk.** Every downloader refuses any row whose Europe/Berlin delivery day is after
>   2026-09-06, in code.
>   - **For GFS, the guard tests the run's initialization, not its valid time.** A run serves the
>     delivery day after its run date. The guard refuses any run initialized at or after 2026-09-06
>     00 UTC, and any lead outside §15.2's f021–f048. A forecast's valid time after the boundary is
>     not an outcome.
>   - **Tests:**
>     - the instants 2026-09-06 21:00 and 22:00 UTC, for rows;
>     - the 2026-09-06 00 UTC run, which is refused;
>     - the 2026-09-05 00 UTC run's f048 message, which serves delivery day 2026-09-06 and is
>       admitted.
> - **The boundary moves only twice.** The 4.7T gate moves it to 2026-12-05. After 4.7T, CP-18's
>   brief retires the guard for the live pipeline only.
> - **Reading.** No agent reads reports, news, analyses or prices about market events after
>   2026-09-06.
> - **The window.** 4.7T's window is fixed now (§24.3) and is never extended after a result.
>
> **The exposure ledger** lives in `docs/track-b/exposure-ledger.md`. The Orchestrator keeps it,
> seeds it with the entries below at ratification, and adds every later exposure. Known entries:
>
> 1. **2026-09-08, the snapshot pull** (`data/source_manifest.json`). The first review found no
>    committed row after 2026-09-06; the audit verifies the pull's request bounds.
> 2. **2026-09-15, CP-15's retrieval of smard.de pages**
>    (`reports/cp15/feasibility/source_retrieval_manifest.json`).
> 3. **2026-10-11, stage 3's retrieval of provider pages:** documentation and metadata only, by its
>    report. Its only data query was Elia's record counts, bounded at 2026-04-07 Brussels.
> 4. **2026-10-12, the stage 4 research agent** reported that a search showed it an excerpt from
>    after 2026-04-07, which it discarded. It left no raw material, and the Orchestrator did not look
>    for the excerpt.
>
> **Their impact assessment** is recorded in the ledger before CP-26's first score, and CP-26's
> Integration Critic reviews it. For entry 4, the assessment considers whether any value adopted
> from the stage 4 memo could carry a market outcome.
>
> **The audit standard (for §24.9):**
>
> - **The test:** no outcome after 2026-09-06 entered any fit, tuning, selection, registration or
>   recorded Owner decision.
> - **Incidental exposures** are listed, each with an impact assessment. They block 4.7T only if they
>   could have informed a registered choice.
> - **The Owner declares in the audit** that his decisions used no information after 2026-09-06:
>   the tier ruling (§24.5), the CP-28 decision, the margin rulings, and CP-17.
> - **The CP-28 decision:** the Owner's confirmation of CP-28 may rest only on CP-26's report, its
>   resources and this section.
>
> **The boundary governs development only.** The live product, once running, trains on all the data
> available to it.


## Supporting section 24.4

> ### 24.4 The forecast issue time
>
> **From CP-25 on, the issue time is D−1 11:00 Europe/Berlin,** one hour before the 12:00 day-ahead
> gate, every day:
>
> - 10:00 UTC when D−1 is on CET, and 09:00 UTC when it is on CEST;
> - the UTC instant follows D−1's own local offset at 11:00, including on transition days.
>
> **Rules:**
>
> - **Strictly before.** An input is usable only if it was published strictly before the issue time.
>   A publication at exactly the issue time is not.
> - **The target-day embargo.** No price of delivery day D in any zone, and no transformation or
>   same-auction output that reveals it, enters, whatever its timestamp says.
> - **Calendar features.** Deterministic calendar features known in advance, such as day of week,
>   month, statutory holidays and day length, are admissible. Hindsight labels are not (§24.5).
> - **§2's released-error rule is unchanged:** errors come from complete delivery days ≤ D−2,
>   consumed once.
>
> **Why.** §14's origin, D−1 11:00 UTC with a fixed UTC+01:00, is 13:00 CEST in summer: after the
> gate, and after the auction's results are published. No generation ever used a day-D price, but a
> live forecast at that hour is not a forecast.
>
> **Records before this revision keep 11:00 UTC** and are not relabelled. CP-26's results are under
> the new issue time.
>
> **The live product** publishes its forecast before 12:00 local. CP-18 fixes the schedule, its
> deadline and its failure rule; a late forecast is recorded as late.


## Supporting section 24.5

> ### 24.5 The vintage tiers (Owner, 2026-10-12)
>
> **For every published input of every policy:**
>
> 1. **Tier 1:** original vintages with publication timestamps enter the main evaluation.
> 2. **Tier 2:** preserved original values, with availability reconstructed from documented
>    schedules, may enter, with disclosure and delay-sensitivity checks.
> 3. **Tier 3:** revised historical values without original vintages are excluded from the main
>    evaluation and tested separately.
>
> Reconstructing the availability time is acceptable; substituting retrospectively corrected values
> is not. Each input is verified individually, and licensing remains mandatory.
>
> **The tier register,** which CP-25 writes, has three categories:
>
> - **published inputs,** each with its tier and its evidence;
> - **deterministic calendar features known in advance,** which are admissible;
> - **hindsight labels,** which are inadmissible. For example, v1's `crisis_period`
>   (2021-09-01 to 2022-12-31) and `post_crisis` (from 2023-01-01), in
>   `src/delu_forecast/features.py`, encode regime boundaries known only later.
>
> **The target price** is tier 2 only if CP-25 documents SDAC result finality. Otherwise the Owner
> rules before CP-26.
>
> **An input whose originality cannot be established** is treated as tier 3 for the ruling below.
>
> **Tier 3 among the inputs of B0 or v1–v5.** The day-ahead load forecast is the known risk, because
> `data/snapshot.parquet` holds SMARD's current values.
>
> - **CP-25 returns the tier register to the Owner** before CP-26's brief is issued.
> - **If any of those inputs is tier 3,** CP-26 does not start until the Owner rules, before any
>   score.
> - **The default, under his standard:**
>   - the main evaluation runs each affected policy without that input, or with a substitute that
>     CP-25 registers and that is itself tier 1 or tier 2. The variant is named, for example
>     "v5 (no revised load)";
>   - the as-landed policy runs beside it, labelled revision-contaminated, and is never used for
>     selection, combination or freezing.
> - **The Owner may instead grant a recorded exception** for that input.
> - **The ruling specifies the variant's construction,** for each affected member, as a declared
>   method change:
>   - the columns removed or substituted (for example LEAR's load lags, and v1-R's two load
>     features);
>   - DDNN-2's always-included inputs, with the search space adjusted to match;
>   - a fresh run of the 14 searches (§24.7).
>
>   The harness may apply exactly those changes and no others.
> - **A parity check for the variant.** With the removed inputs restored, the variant's code
>   reproduces the as-landed parity vectors (§24.7).
> - **The control.** In this section and in §§24.7–24.9, "the control" is v5, unless the ruling names
>   a variant. The ruling then names it.
>
> **Tier 2: delay sensitivity, from a margin table.** Availability is reconstructed from documented
> schedules, so a uniform shift either changes nothing on a day or removes the input that day.
>
> - **The margin table.** For each tier-2 input group and each shift (+1, +6 and +24 hours), CP-25
>   computes the days on which the shifted availability is no longer strictly before the issue time.
> - **What follows from it:**
>   - **a shift that affects no day** is recorded as passed, without a run;
>   - **a shift that affects every day** is recorded as structural, with the result of the input's
>     registered missing-input rule. For weather that is §15.3; for the load forecast and prices it is
>     a failure, so the day falls back (§24.7);
>   - **a run is made only when the affected days are a non-empty proper subset.** It runs the
>     control with the shift applied, including its 14 searches, and is reported beside the nominal
>     run.
> - **Fragile.** A shift that is run is fragile if the control's shifted run worsens either primary
>   score by more than 2% relative to the nominal run.
> - **When the Owner rules:**
>   - on structural shifts, with the tier register, before CP-26;
>   - on a fragile result from a delay run, with CP-26's report, before CP-28.
>
>   For
>   example, the load forecast's deadline is two hours before the gate, about 10:00 local, so a
>   one-hour delay reaches the issue time on every day. He may accept that margin as a disclosed
>   operational risk, measured in CP-18's live trial. CP-17 records the rulings; it does not discover
>   them.
> - **No previous-run or previous-day fallback** is introduced.
> - **The missing-input rules:**
>   - for weather, §15.3: the three derived columns go missing and their indicators are set;
>   - for the load forecast and prices, the inherited rule in the landed code, which CP-25 states with
>     its file and line.
>
> **Licences:** every input has a recorded licence. `DATA-LICENSE.md` is unchanged.


## Supporting section 24.8

> ### 24.8 CP-28: 4.8 on stored forecasts (stage 8)
>
> **Status:** it runs only if the Owner confirms it after CP-26 lands. Every arm is specified here,
> and in CP-28's frozen protocol (§24.7).
>
> **The members** are the control's three, from CP-26's ledger:
>
> - c_HG: v3's central forecast;
> - L: the mean of L-N and L-R;
> - D2: DDNN-2's median.
>
> **The control** is the control named under §24.5: v5, unless a tier ruling names a variant. It
> keeps the weights (2/3, 1/6, 1/6) and its interval layer. **Wherever §§24.8–24.9 say v5, they mean
> the control** (§24.5): in its weights, its forecast, the gates' L_v5, and the disclosures.
>
> **The construction, as v5's own:**
>
> - Weights apply to the members' central forecasts.
> - Each combined arm's quantiles come from HG's H layer, re-estimated on that arm's own issued
>   central errors.
> - Each combined arm stores its pre-outcome native central with that issuance's causal weights
>   and scale. Insufficient H history permits central warm-up and D−2 own-error release even on
>   a scored fallback date. Missing members or solver failures create no native arm central.
>   Copied fallback errors never populate the arm's H buffer, and emitted fallback scores stay fixed.
> - The learned arms minimize mean daily central MAE.
> - A1 keeps DDNN-2's own Johnson SU quantiles.
>
> **The ledger rule:**
>
> - A member forecast for day s enters any arm's learning only if s ≤ D−2: a complete delivery day
>   released under §2. Its forecast was made without its outcome.
> - D's combined forecast is produced before D's outcome enters the ledger.
> - CP-26's warm-up supplies the first ledger days.
> - The latest 728 complete released learning days (minimum 364/728) are separate from H's latest
>   28 own-error days. A complete day with all three native members can be a learning row even
>   when v5's measured output was fallback solely for H warm-up. Partial keys never create a
>   complete learning row. Actual support, not a promised date, determines learning startup.
>
> **The arms (Owner, 2026-10-12):**
>
> | Arm | Rule |
> |---|---|
> | A1 | DDNN-2 alone, with its own quantiles |
> | A2 | Equal weights, (1/3, 1/3, 1/3) |
> | A3 | One global weight vector, chosen on the simplex grid with step 0.01 (5,151 points). It minimizes mean daily central MAE over the latest 728 ledger days on which all three members are valid, and needs at least 364 such days. Ties go to the point nearest v5's weights (Euclidean), then to the lowest grid index. Deployed weights = 0.5 × fitted + 0.5 × v5's, updated daily. Before 364 days: v5's weights |
> | A4 | One weight vector for each of CP-21's blocks (night 22–05, solar 10–16, shoulder/peak 06–09 and 17–21), on the same grid, minimizing central MAE over the block's hours across the latest 728 ledger days, and needing 728. Deployed = 0.25 × the block's fitted vector + 0.75 × A3's deployed weights. Before 728 days: A3's deployed weights |
> | A5 | The NumPy meta-learner (below) |
> | A6 | A3 without shrinkage: the same grid, objective, window, minimum history and tie rule, with deployed weights = the fitted weights. It can reach any weighting, including 100% on one member. Before 364 days: v5's weights |
> | A7 | A5 without shrinkage: the same network and training, with deployed weights = the network's output as it is. Before 364 days: v5's weights |
>
> **A5, the NumPy meta-learner:**
>
> - **Sixteen inputs, all known at the issue time:**
>   - for each member, its mean absolute central error over the last 7 and the last 28 ledger days;
>   - the high-volatility and negative-price-risk states (§24.7), and the "volatility unknown" flag
>     below;
>   - season, as four one-hot values;
>   - hour block, as three one-hot values.
> - **Output:** for each day and block, a softmax over the three members.
> - **The network:** one hidden layer of 8 tanh units.
> - **The loss:** the mean absolute error of the weighted central forecast over the block's hours.
> - **Training:**
>   - full-batch Adam, learning rate 0.01, 300 epochs, L2 penalty 1e-3 on the weights;
>   - initialization seeded with `SeedSequence([28, D.toordinal(), 0x4D4C])`;
>   - refit daily, from scratch, on the latest 728 ledger days, needing at least 364.
> - **Deployed weights** = 0.5 × the network's output + 0.5 × v5's weights. Before 364 days: v5's
>   weights.
>
> **Further fixed details:**
>
> - Training rows for every learned arm, A3 to A7, require all three members to be valid.
> - The grid points are ordered lexicographically by (w_HG, w_L), ascending. A4's ties follow A3's
>   rule.
> - A5's and A7's inputs are standardized on the training window only. A6 and A7 share A3's and
>   A5's fits: only the shrinkage differs.
> - An unknown volatility state is encoded as "not high", with a separate 0/1 flag for "unknown".
> - Adam's β1 = 0.9, β2 = 0.999 and ε = 1e-8; weights are initialized from a normal distribution with
>   standard deviation 0.1, and biases at zero.
> - **Any implementation detail this section still leaves open** is fixed in CP-28's frozen protocol
>   before CP-26's first score. CP-26's Integration Critic checks that none depends on an outcome.
>
> **Failures:**
>
> - A missing member makes the arm use v5's forecast that day.
> - If v5's forecast is missing too, B0's forecast is used.
> - A solver failure, with every member valid, makes the arm use A2's.
> - No arm renormalizes over a subset of members, and every fallback day is counted.
>
> **The gates, against the control (written v5 below), on CP-26's scored calendar:**
>
> 1. **Improvement:** `H0: E[L_arm − 0.995·L_v5] ≥ 0` is rejected for both MAE and WIS; that is, by
>    more than 0.5%.
> 2. **Non-inferiority:** `E[L_arm − 1.02·L_v5 | g] ≥ 0` is rejected for both MAE and WIS in each
>    complete year, 2021 to 2025, and in each pooled season. A required cell with fewer than 90 days
>    makes the arm inconclusive.
> 3. **The compound test:** the arm's p-value is the largest over its required endpoints. Holm runs
>    across the seven arms at α = 0.05; CP-27's family no longer exists.
> 4. **Sensitivity.** Every arm's compound p-value and Holm are recomputed under each variant: 7-day
>    blocks, 28-day blocks, and unstratified. An arm that passes under the primary analysis but fails
>    under any variant is inconclusive, and is not adopted.
>
> **Disclosed in advance:**
>
> - A4 equals A3 until 728 complete released ledger days exist. All learned arms start according
>   to actual support; member/search failures and incomplete days may delay it. Report the observed
>   startup and calendar span, with no guarantee of a fixed activation date. A4's early cells test
>   A3's weights to that extent.
> - The learned arms equal v5 until their minimum history exists.
> - **A6 and A7 are unshrunk** (Owner, 2026-10-12). They can place any weight on DDNN-2, up to 100%,
>   and are the arms most exposed to overfitting and to lag at regime changes. The gates, the
>   simplicity order and 4.7T are their protection.
> - **CP-28's Holm control is conditional on the Owner's decision to run it.** That decision follows
>   CP-26's report, which includes DDNN-2 alone (A1's forecasts) on the same calendar. 4.7T still
>   carries the protection.
>
> **Selection:**
>
> - Among the arms that pass, the one with the lowest WIS wins.
> - Arms whose WIS is less than 0.5% above the best are tied, and the simpler arm wins, in the order
>   A1, A2, A3, A6, A4, A5, A7.
> - If no arm passes, the control is the candidate for the freeze.
>
> **Further rules:**
>
> - There is one look, and no arm is added. A failed or unexecuted arm counts with p = 1.
> - **Ceiling, proposed:** 40 machine-hours.
> - **Evidence class:** `development_post_selection`; 4.7T carries the protection.
> - **Gates:** CP-26's LAND, the Owner's confirmation, the issued brief, and the LAND.


## Supporting section 24.9

> ### 24.9 CP-17 and 4.7T
>
> **CP-17 freezes one candidate,** CP-28's selection or the control (§24.5), together with:
>
> - its daily retraining rule (§16.2), the issue time, and its inputs and their tiers;
> - its DDNN-2 search state and its combiner state at the freeze;
> - **DDNN-2's search schedule in operation:** the 182-day searches continue, the next being
>   S_14 = 2027-01-06, after S_13 = 2026-07-08, under the same phase and rules, as part of the
>   frozen refit schedule. These are protocol dates only, never permission to read future data;
> - the tier and margin rulings (§24.5);
> - its fallback and failure rules;
> - §19.5's definitions;
> - the lock-price policy, if the final product adopts it
>   (`docs/track-b/final-product-lock-price-notes-2026-10-11.md`).
>
> **§16.4's "before fresh-data test" row** is met by CP-26's daily refits of the control and CP-28's
> of the arms.
>
> **Registered before 4.7T opens:**
>
> - **the comparators:**
>   - the candidate against the control, when they differ;
>   - the candidate against B0, in every case;
>   - v3, v4 and v1's released artifact, as descriptive references;
> - the primary scores and their aggregation, from §24.7;
> - the pass conditions and margins;
> - a dependence treatment suited to 90 days;
> - the failure rules;
> - PUBLISH_RULES §14's "before final-candidate test" trigger.
>
> **The audit (§24.2's standard).** Before opening, the Lead and an independent reviewer check the
> download logs, the boundary guard's tests, the exposure ledger and the Owner's declaration. If the
> standard is not met, 4.7T returns BLOCKED.
>
> **Then:** CP-18, with security hardening (§22's reminder), a controlled live trial whose length the
> Owner sets, and site activation; then CP-19.
>
> **On the timeline.** §16.4 requires CP-19 to cover at least 90 consecutive delivery days after the
> final freeze. With 4.7T opening no earlier than 2026-12-04, CP-19 cannot finish before about March
> 2027. CP-18 may still publish live observations labelled "prospective evaluation in progress".

