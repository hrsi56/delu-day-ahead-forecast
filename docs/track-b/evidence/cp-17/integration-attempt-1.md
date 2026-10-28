# Verdict — CP-17 — Integration — FAIL

- Candidate SHA: dc78e209b05ebab39e5000d5ac812f9eee035316
- Plan / version / bar: `capstone_v21.md`, revision v21-r17, SHA-256
  `3124451da84c3cd99fae728c371207aace6ae537474f7769d0ff6333ee53e4fc`; bar `### 24.9 CP-17 and 4.7T` (40 lines,
  2,007 bytes, section SHA-256 `6675e907ccad916e02059b12479daec712f0e720efd4c4056e656b863027a0f1`), together with
  §16.2, §19.2, §19.3, §19.5, §19.7 and §16.4's CP-17 row, under the issued brief
  `docs/track-b/evidence/cp-17/issued-brief.md` (`9f235cf8…1b1a73`) and the Owner's decisions record
  `docs/track-b/pre-cp-17-rulings-2026-10-25.md` (`d29b0abc…a8f6b0`).
- Verbatim bar excerpt:

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

  (The excerpt is the citation. Any line number is a courtesy and is non-binding.)
- Worktree clean before and after: yes. `git -C /Users/djourno/Downloads/PJM/.local/worktrees/cp-17/critic-1
  status --porcelain` was empty, and `HEAD` was `dc78e209b05ebab39e5000d5ac812f9eee035316`, before the review,
  after every reproduction step, and before this verdict was written.

## Commands actually run

Each command ran from the worktree, unless another directory is named. My outputs are under
`/Users/djourno/Downloads/PJM/.local/artifacts/cp-17/critic-1/` (`repro/`, `*.console.log`). Every
Python command had `MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1` and `PYTHONPATH=src`. Every native fit
also had the five BLAS variables at 1. No network contact was made.

0. **The brief and the bar.**
   - `git show main:scripts/gauntlet.py | python3 -I - critic-brief cp-17`: exit 0.
   - `git show main:scripts/bar.py | python3 -I - bar capstone_v21.md '### <heading>' --at dc78e209…`, for
     each of the six headings: exit 0. All six section identities equal the brief's table:
     - §24.9: 40 lines, 2,007 bytes, `6675e907…`;
     - §16.2: 32 lines, 2,408 bytes, `c54723ef…`;
     - §19.2: 6 lines, 335 bytes, `53834210…`;
     - §19.3: 25 lines, 1,354 bytes, `5d1f869e…`;
     - §19.5: 19 lines, 1,170 bytes, `1d47a505…`;
     - §19.7: 12 lines, 494 bytes, `10060bd2…`.
   - The plan's SHA-256 is `3124451d…`.
   - `shasum -a 256` on the brief, the rulings, the plan, the tracking spec, the Space plan and
     PUBLISH_RULES gave `9f235cf8…`, `d29b0abc…`, `3124451d…`, `8912e228…`, `ad3568c8…` and `1bc0c523…`.
     Each equals the brief's citation.
   - `grep` found §16.4's CP-17 row verbatim at `capstone_v21.md`.
   - After this verdict was written:
     `git show main:scripts/bar.py | python3 -I - check <this verdict> --source capstone_v21.md@dc78e209…`
     exited 0: "ok: lines 12–51 (2006 bytes) appear in capstone_v21.md@dc78e209b05e".
1. **The whole suite in CI mode.** I read the runner first, then ran
   `python3 /Users/djourno/Downloads/PJM/.local/artifacts/cp-17/ci-runner.py critic dc78e209… ci312`.
   - Exit 0. `results.json` shows `complete: true` and `scratch_removed: true`, with tree `744994cf…`,
     the candidate's tree.
   - Python was 3.12.14, `CI=true`, offline, with the local-only inputs hidden.
   - The workflow's seven steps (`.github/workflows/tests.yml`), with exit code and seconds:
     - `uv sync --locked --dev`: 0 (1.5 s);
     - `build_wasm_payload.py`: 0 (75.0 s);
     - `pytest -q`: 0, "2303 passed, 41 skipped in 479.41s";
     - `test_10_cqr_order_statistic.py`: 0, "8 passed";
     - `verify_release.py`: 0, "PASS — every bound claim agrees…";
     - `test_22_wasm_equivalence.py`: 0, "15 passed";
     - `publication_guard.py tree`: 0.
   - The stress collection exited 0: "19/2343 tests collected".
   - Every CP-17 skip states its reason, for example "CP-26's local-only stored state (the evidence/cp-26
     extract) is absent".
   - The logs are in `.local/artifacts/cp-17/critic-validation/ci312/`.
   - The runner's one commit was made inside its own throwaway `git init` copy, which it then removed. No Git
     write touched this repository.
2. **`pytest -m stress`, CI unset.** I ran the same runner with mode `stress`.
   - Exit 0: "19 passed, 1 skipped, 2324 deselected in 387.72s".
   - All 19 stress-marked tests that collection lists passed, including
     `tests/cp17/test_hosts.py::test_issuing_host_reproduces_its_record` and
     `::test_browser_reproduces_the_issuing_host`. The one skip is a collection-level skip, not one of them.
3. **The GFS check.** `.venv/bin/python -m cp17.tools.gfs_check --out repro/gfs/gfs-check.json`
   - Exit 0, 35.8 s. It printed `BLOCKED {"MAE": 0.02270720735470033, "WIS": 0.06683811993513378}`.
   - `cmp` against `reports/cp17/gfs-check.json` and `reports/cp17/gfs-check-daily.csv`: both
     byte-identical.
   - I recomputed the table from `gfs-check-daily.csv` independently, with the paired population, means
     over dates, and every count and mean asserted against the record:

     | Mask | Paired dates | Paired hours | MAE excess | WIS excess |
     |---|---:|---:|---:|---:|
     | affected | 1,354 | 32,478 | +2.2707% | +6.6838% |
     | unaffected | 696 | 16,686 | +34.6081% | +40.0942% |
     | every eligible date | 2,050 | 49,164 | +11.6432% | +16.1813% |

4. **One native parity origin.**
   `.venv/bin/python -m cp17.tools.parity --out repro/native --origins 2026-03-29 --attribution 2026-03-29`
   - Exit 0, 84 s: `2026-03-29 PASS {'A1': True, 'v2': True, 'v4': True, 'v5': True, 'B0': True}`.
   - Every check is identical to `reports/cp17/native-parity.json` for that origin, apart from timings.
   - All five payload digests equal the record's, for example A1 `89e502a4…`.
   - All five quantile hashes equal the record's, for example A1 `67ef0f36…`.
   - **An independent check.** The ledger file `forecast-ledger/2026-03-29.json` hashes to git blob
     `33a6161c…`, which equals `git ls-tree evidence/cp-26`. My A1 quantiles are IEEE-754 identical to its
     `members.nominal.D2.quantiles`, and v5, v4, v2 and B0 are identical to its `nominal/<p>.native_quantiles`.
   - **Also:** `--origins 2026-09-06` (exit 0, 108 s, PASS). All nine of my payload files (A1, v4, v2 and B0
     `.json`/`.npz`, v5 `.json`) are byte-identical (`cmp`) to the Lead's
     `.local/artifacts/cp-17/final/native/payloads/`, which step 6 uses.
5. **One issuing-host parity origin.**
   - `python -m cp17.tools.bundle --out repro/bundle/src.zip`: exit 0, "33 files 86816 bytes 1d4e3c7ee6f38db9".
     - `files_sha256` equals `reports/cp17/bundle-manifest.json`'s.
     - `package_sha256` is `54212d2c…`, and the zip is byte-identical (`1d4e3c7e…`).
     - No `cp17/tools/` file is in the package.
   - `python -m cp17.tools.hosts node --bundle repro/bundle/src.zip --payloads repro/native/payloads --out repro/nodes --runs A1-2026-03-29 --attribution A1-2026-03-29`
     - Exit 0, 80 s, "A1-2026-03-29 ok". There were no errors and no blocked requests, under Pyodide 0.28.0
       and Node v26.7.0.
     - The quantiles' SHA-256 is `b5ca894f…cc05`, which equals the committed `issued_quantiles_sha256` bit for
       bit.
     - The 18 executed files equal the package's hashes.
   - `cp17.retrain.compare('A1', <my native fit>, <my host fit>)`:
     - status "within ±0.01 EUR/MWh", the committed status;
     - payload identity equal; selections all matched;
     - max 6.27698966582102e-07 EUR/MWh, at the p90.
     The per-level maxima equal the record's.
6. **One browser identity run, and v4's browser run.** I ran
   `PLAYWRIGHT_BROWSERS_PATH=… .local/tools/playwright/bin/python src/cp17/tools/measure.py --pyodide … --bundle repro/bundle --payloads .local/artifacts/cp-17/final/native/payloads --out repro/browser.json --runs A1-2026-09-06,v4-2026-09-06 --browsers webkit --attribution 1`.
   - Exit 0: "webkit A1-2026-09-06 ok 67.4s", "webkit v4-2026-09-06 ok 78.3s". WebKit was 26.6.
   - There were no errors, no blocked requests and no 404s, and the executed files equal the package.
   - **A1:** quantiles `4e6abb02…a5`. This equals the committed issuing-host record for A1-2026-09-06 and the
     freeze artifact's `quantiles_sha256`.
   - **v4:** quantiles `76599de7…c9`. This equals the committed issuing-host v4-2026-09-06, so the status
     against the issuing host is "identical bit for bit".
   - **Against my native 2026-09-06 fits:** A1 is "within ±0.01 EUR/MWh" (9.38e-13) and v4 is "within ±0.01
     EUR/MWh" (4.26e-13). Selections all matched for both.
7. **The freeze manifest and the CP-17 tests.**
   - `python -m cp17.tools.freeze verify docs/track-b/evidence/cp-17/freeze-manifest.json`: exit 0,
     `verified`.
   - `pytest -p no:cacheprovider tests/cp17 -q -rs --basetemp=repro/pytest-tmp`, with BLAS at 1 and CI unset:
     exit 0, "50 passed in 216.75s". There were no skips: the real-input, record and host tests all ran.
8. **My own checks** (read-only).
   - `git diff --name-only/--name-status be504ab..dc78e209` and `dd5e57f..dc78e209`:
     - The candidate adds 67 files and modifies, deletes or renames none since `dd5e57f`.
     - Every path is under `src/cp17/`, `tests/cp17/`, `reports/cp17/` or `docs/track-b/evidence/cp-17/`.
     - `be504ab..dd5e57f` touches only `progress.md` and the decisions record.
     - `git diff --quiet dd5e57f dc78e209 -- <the protected paths>` exited 0. That covers `src/cp17probe`,
       `src/cp15`–`src/cp28`, `src/delu_forecast`, `data`, `reports/development-inputs`, `pyproject.toml`,
       `uv.lock`, the anchors, the role and governance files, the exposure ledger, the backup register and
       `.claude`.
     - The root `pyproject.toml` hashes to `aa35326a…` and `uv.lock` to `5d2aecc3…`.
   - `git ls-tree -r -l dc78e209`: no blob is over 50 MB (the largest is 30.8 MB, pre-existing). The largest
     CP-17 file is 308,888 bytes.
   - A date scan of every file the checkpoint added found nothing after 2026-09-06 that is a delivery day,
     key or value. What it found is protocol, run-name or ruling dates: the 4.7T window, S_14, the
     cold-rerun's name, the ruling and issue dates, and the compute-ledger timestamps. No UTC key of a later
     delivery day occurs; the last key of 2026-09-06 is `2026-09-06T21:00:00+00:00`.
   - **The boundary:**
     - `data/snapshot.parquet` ends at delivery 2026-09-06, 21:00 UTC;
     - the ledger extract's last file is `2026-09-06.json`;
     - `cp25/guard.py` has `BOUNDARY = date(2026, 9, 6)`, unchanged.
   - **Runtime identities:**
     - the Node binary hashes to `1ef99ea2…d040`;
     - all 23 Pyodide files equal the freeze manifest's hashes and the CP-17-probe retrieval manifest
       (`37bf451f…`).
   - **The reference bundle:**
     - `schema.verify_bundle` on `.local/artifacts/cp-17/final/reference-bundle/` returned `[]`;
     - its manifest hashes to `7d4ed1b9…`, the committed one;
     - two extra tamperings were refused: one digit of `artifact.json`, and a truncated `series.json`.
   - **C2's count:** CP-26's ledger has 2,078 scored days from 2020-12-29 to 2026-09-06. On 43 of them
     `nominal/v5.full_canonical_issuance` is false, as freeze record C2 states. They are mostly the two days
     after a DST change and the Sunday after it.
   - **The freeze record's file:line citations** match the code at the candidate:
     - `src/cp26/members.py:199`, `:213`;
     - `src/cp24/design.py:306-307`;
     - `src/cp15/models.py:45`;
     - `src/cp21/lgbm.py:123-126`;
     - `src/cp15/data.py:79-80`;
     - `src/cp24/member.py:43-45`.
   - **The issuance code exercised directly** (a synthetic check in a scratch interpreter, no file
     written). `cp17.issue.decide(2026-09-06, gfs=True)` with an A1 attempt that succeeds, then
     `issue.artifact(…, wall_seconds=1000.0, peak_bytes=5 GiB)`:
     - fitted `['A1']` only;
     - `issued_policy: A1`, `display: failed fit (resources)`, `route: designated`;
     - A1's quantiles issued, `resource_check` listing both ceilings, and `verify_artifact` `[]`.

     With A1 failed in training and v4 over both ceilings: fitted `['A1', 'v4']`, `issued_policy: v4`,
     `display: failed fit; fallback v4 issued`. v2 is never tried. See the gap below.

## Evidence actually inspected

- **The packaged brief** `docs/track-b/evidence/cp-17/issued-brief.md`, in full, and the decisions record
  (decisions 1–12).
- **The frozen documents**, read in full: `freeze-record.md`, `4-7t-frozen-protocol.md`, `definitions.md` and
  `payload-schema.md`. I also inspected `freeze-manifest.json` (every section) and `artifact-2026-09-06.json`,
  and listed `schemas/`.
- **The records:** `reports/cp17/report.md`, read in full, and `gfs-check.md`/`.json`/`-daily.csv`,
  `native-parity.json`, `host-parity.json` (all 15 issuing-host rows, the four browser rows and the F1
  member deviations), `issuance.json`, `controls.json`, `reference-bundle.json`, `bundle-manifest.json`,
  `compute-ledger.jsonl` and `retrieval-manifest.json`.
- **The code:**
  - read in full: `src/cp17/retrain.py`, `issue.py`, `dailyfit.py`, `scoring.py`, `host/driver.py`,
    `host/node_run.mjs`, `tools/bundle.py`, `tools/issuance.py`, `tools/controls.py` and
    `tools/fresh_test.py`;
  - read in part: `schema.py` (the validator and `verify_bundle`), `attribution.py` (group Shapley and the
    LEAR part), `tools/parity.py`, `tools/ledger.py`, `tools/freeze.py` (identity and `verify`),
    `tools/gfs_check.py`, `tools/hosts.py`, `tools/measure.py` and `tools/reproduce.sh`;
  - from the landed code: `cp28.inference.test_endpoint`.
- **The tests:** `tests/cp17/test_units.py` (the issuance, resources and bundle parts), `test_records.py` and
  `test_hosts.py`.
- **The commit log** `be504ab..dc78e209` on `gauntlet/cp-17`:
  - `05bb6c51` records that the first official run's training-window control read "within +/-0.01 EUR/MWh"
    (0.0091 EUR/MWh, every selection matched), and that binding the payload identity first was added;
  - `af4c20c8..dc78e209` changes only records and documents, no code.
- **The Lead's local material that the brief names:** `ci-runner.py`, `critic-open.json`, `final/native/payloads/`
  and `final/reference-bundle/`. I did not open the Lead's return drafts, CI notes or other narrative files in
  `.local/artifacts/cp-17/`.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1 | **Brief item 1: the A1 GFS check** (done at `2d570e0`; rulings 11 and 12 followed) | PASS | Rerun byte-identical (JSON and daily CSV). My independent recomputation gives the same paired counts and means, +2.2707% MAE and +6.6838% WIS on 1,354 affected dates. The rule is met (BLOCKED), and the record stays as committed. Decisions 11 and 12 are carried into `cp17.issue.CHAINS` and freeze record §10. |
| 2 | **Brief item 2: one code path, `src/cp17/`** (§19.2) | PASS | **The package:** 33 files measured from the import closure, rebuilt byte-identical, with `cp17/tools/` absent and the stubs frozen in it. **Hosts:** native, Node, Chromium and WebKit ran it, and the executed-file hashes equal the package. **Inputs:** `dailyfit.run` reads only the payload, whose identity is checked. **Scope:** A1, v4, v2 and B0 are in the product scope, with v5 native as the control. No component needed the exception route. |
| 3 | **Brief item 3: the issuing host and its parity** | PASS | **Native parity:** the record is bitwise for five policies at nine origins (428 interval-state days per policy). I reran 2026-03-29 and 2026-09-06, both PASS, and 2026-03-29 is also bitwise against the tag's ledger directly. **Issuing host:** 15 runs, every selection matched, and every run within τ_eq except F1. I reproduced A1-2026-03-29 bit for bit. **Browser identity:** committed for Chromium and WebKit. I reproduced WebKit, and Chromium again in the stress test. **v4 in the browser:** measured (time, memory, payload, deviation, selections) and reproduced in WebKit. **Data check:** no data after 2026-09-06. |
| 4 | **Brief item 4: the freeze record and `freeze-manifest.json`** | FAIL (gap G) | **Present and verifying:** every §16.2, §16.4-row and §24.9 field is present, and `freeze verify` gives `verified`. The failure chains are stated exactly as decisions 11 and 12 rule them. The success definition's text is the brief's. The gaps G1, C1, C2, G2 and F1 are reported with file:line, and none changes landed code. **The failure:** §10 says the success definition is the brief's "as `cp17.issue` implements it", including "5. Resources … Anything else is a failed fit". The frozen code does not implement criterion 5 that way (gap G). |
| 5 | **Brief item 5: §19.5's definitions** | PASS | `definitions.md` matches the brief: τ = 10 inclusive, the denominator, partial days with completeness, zero, negative and missing prices, the label, the 28-scored-day rolling window, the eight-band PIT with closing-quantile ties, the reliability counts, and 1e-9·max(1,\|b\|). `scoring.py` implements it as written, which I checked by reading. The unit tests pass, and `scoring-check.json` is bit for bit native against the issuing host on 2,536 and 7,696 items. |
| 6 | **Brief item 6: §19.3's retrain comparison and §19.7's attributions** | PASS | **The status rule:** `retrain.compare` binds `payload_sha256` before the three-status rule, and a mismatch reports "different" while keeping `measured_status`. That follows §19.3 item 1 ("from that fit's shipped training window") and decision 9's three statuses. **The controls:** seed "different"; training window "different" (measured "within", 0.0091); target-day outcome leaves the A1, v2, v4 and B0 payloads byte-identical. The history is in commit `05bb6c51`. **Attributions:** by class as the brief fixes them (A1 group Shapley, at most 2,048 coalitions, efficiency 2.8e-14 in my run; LEAR linear; TreeSHAP and gain; blends). **The reference runtime** is frozen. |
| 7 | **Brief item 7: the payload schema and manifest** | PASS | The seven kinds have machine schemas equal to `schema.SCHEMAS` (tested), and the manifest carries the fields the brief lists. The embargo rule is checked per policy. The reference bundle verifies (`7d4ed1b9…`), and the four committed tamper controls plus my two extra are refused. See observation O1 on its recorded location. |
| 8 | **Brief item 8: 4.7T's frozen protocol, outcome-blind** | PASS | **Coverage:** every sub-item is present: comparators, scores and aggregation, the four endpoints with the 0.995 factor, the compound max-p at α = 0.05 with no Holm, 7-day blocks, 10,000 replicates and seed 20261204, how forecasts are generated, minimum support 60/90 with its reason, the failure rules, the §24.2 audit, the retrieval plan (prepared, not run) and PUBLISH_RULES §14's four items. **The code:** `fresh_test.py` matches the text and is tested on synthetic losses only. **Blind:** no 4.7T outcome is used, and no data after 2026-09-06 exists. |
| 9 | **The success definition** (brief, "A successful daily fit") | FAIL (gap G) | **Implemented:** criteria 1–3 in `issue.attempt`/`check_inputs`/`check_emission`, the A1 eight-member rule, and the GFS-late skip, all correct. **Not implemented:** criteria 5–6. An A1 fit over 15 min or 4 GB still issues A1's quantiles, with `issued_policy` 'A1' and only the display changed to "failed fit (resources)" (`src/cp17/issue.py:161-163`). It does not pass to v4. A fallback over the ceiling is not judged by criterion 5 at all, against "A v4 or v2 fallback fit is judged by the same five criteria". I demonstrated both directly. |
| 10 | **Further item 1: blind** | PASS | The boundary is 2026-09-06 in `cp25/guard.py`, unchanged. The snapshot and ledger end at 2026-09-06. No later delivery date, key or value is in any record. The retrieval manifest records 0/0/0, and every host and browser run recorded no non-local request. |
| 11 | **Further item 2: GitHub-landable** | PASS | No blob is over 50 MB. The extracts, payloads and bundle stay in `.local/artifacts/cp-17/`, listed in committed manifests. |
| 12 | **Further item 3: CI-ready** | PASS | The seven steps are green on a history-free single-commit copy with `CI=true` and Python 3.12. `pytest -m stress` passes locally, with the CP-17 host and browser tests run. The local-input tests skip with stated reasons, and the timing-sensitive tests carry `stress`. |
| 13 | **Further item 4: no pinned file changes** | PASS | The candidate adds files only, in the four allowed paths, and modifies no existing file since `dd5e57f`. The protected paths are unchanged, with the root `pyproject.toml` at `aa35326a…` and `uv.lock` at `5d2aecc3…`. |
| 14 | **Further item 5: the Critic's reruns** | PASS | Done, as listed under "Commands actually run" 1–7. |
| 15 | **§24.9 CP-17 and 4.7T** | FAIL (gap G) | **Frozen and correct:** the candidate (A1), the daily rule, the issue time, the inputs and tiers, the S_13 search state with no combiner, S_14 = 2027-01-06 as a protocol date, the tier and margin rulings by hash, §19.5's definitions, and the lock price (not adopted). **Registered:** the comparators, scores, margins, dependence treatment, failure rules, PUBLISH_RULES §14 and the audit. **The failure:** the bullet "its fallback and failure rules", because the frozen code issues a failed A1 fit instead of the fallback on a resource failure. |
| 16 | **§16.2 What freezes and what updates every day** | FAIL (gap G) | **Present:** the freeze list is complete (freeze record §§2–14), and each artifact carries its training window, seeds, timestamps and parent, input and state hashes. **The failure:** "For … resource exhaustion … apply the frozen fallback/staleness limits or record failed issuance". The code instead issues the over-ceiling fit's own forecast, labelled failed. |
| 17 | **§16.4's CP-17 row** | FAIL (gap G) | **Present:** the designation and prerequisites (§1), the policy, initialization and registry identities (§§2, 6, 12), the metric formulas (`definitions.md`), and the resource and calendar plan (§13, protocol §11). **The failure:** "daily fit and failure rules", gap G. |
| 18 | **§19.2 One code path** | PASS | As item 2. |
| 19 | **§19.3 "Train it yourself"** | PASS | τ_eq and the reference runtime are frozen from the probe. The status reports selections, per-level maxima and one of the three statuses, and never replaces or relabels an issued forecast (`compare` reads two results only). The visitor's retrain is bit-identical in Chromium and WebKit, which I reproduced in WebKit, and v4 was measured for the fallback. No exception is needed. |
| 20 | **§19.5 Definitions** | PASS | As item 5. Every value was fixed before any evaluation outcome: τ is the Owner's, and the 28 days and 1e-9 come from the brief and the Space plan. |
| 21 | **§19.7 Attribution and importance** | PASS | As item 6: the blend, linear, tree (TreeSHAP and gain) and neural (group Shapley) methods are frozen, with the "within one fitted artifact, never causality" wording in the code, the record and the report. |
| 22 | **Assignment check: the F1 issuing-host miss** | PASS | It is reported with its numbers and selections and not tuned. A1 at 2025-10-26 is "different": 0.0279 EUR/MWh at the p50, per-level maxima recorded, every selection matched. Member 5 (cp26-k11-t032, seed 27190032, 1,000 epochs) is at 0.77, member 4 at 3.6e-05, and the others at about 1e-13. Freeze record §11 F1 and the report state it for the Owner and r18. |
| 23 | **Assignment check: the report's tables and prose** | PASS | `test_report_tables_are_the_records` passed in my run. The prose figures I spot-checked agree with the records: 33 files and 86,816 bytes, 67.7 s and 831 MiB, 489 negative-price hours, 2,536/7,696 items, and 428 state days. |

## On FAIL only

- **Single largest meaningful gap (G).**
  - **What the code does.** The frozen issuance code does not treat the success definition's resource
    ceiling as a failed fit that triggers the fallback. `cp17.issue.artifact` (`src/cp17/issue.py:161-163`)
    applies criterion 5 only after `decide` has chosen A1. When A1's fit exceeds 15 minutes or 4 GB, the
    artifact still issues A1's quantiles as the product forecast (route "designated"), and only relabels the
    display as "failed fit (resources)". An over-ceiling v4 or v2 fallback is issued without that check.
  - **What it contradicts:**
    - the brief's criteria 5–6: "Anything else is a failed fit. The frozen fallback then issues";
    - §16.2's resource-exhaustion rule;
    - freeze record §10's statement that `cp17.issue` implements the definition;
    - 4.7T §4's "A1 on a successful fit, the frozen fallback otherwise".
  - **Why it matters now.** The measured fits (≤ 146 s, ≤ 0.9 GB) are far inside the ceiling, so no
    committed number is affected. But this is the frozen product rule, and after landing it can change only
    with a new freeze.
- **Exact next acceptance test.**
  - **Unit tests in `tests/cp17`.** They must show three things:
    - an A1 attempt whose measured wall time exceeds 900 s, or whose peak exceeds 4 GiB, records A1 as
      failed for resources and goes on to v4, with display "failed fit; fallback v4 issued";
    - a v4 fallback over the ceiling passes to v2, and v2 to B0;
    - no path issues a forecast from an over-ceiling fit.
  - **The freeze record:** §10 states the same behaviour.
  - **The records:** regenerated from the changed package, so that the package, policy identity, freeze
    artifact and freeze manifest digests are re-recorded. `freeze verify`, `tests/cp17` and the
    issuing-host and browser identity checks pass again.
  - **The alternative:** if the Lead holds the current behaviour to be intended, it needs an explicit Owner
    ruling recorded as a conflict with the brief's success definition.

## Observations (not blocking)

- **O1. The reference bundle's location.** `reports/cp17/reference-bundle.json` (`location`) and
  `payload-schema.md` both name `.local/artifacts/cp-17/reference-bundle/`, which does not exist. The bundle is
  at `.local/artifacts/cp-17/final/reference-bundle/`, where its manifest hashes to the committed
  `7d4ed1b9…`.
- **O2. What `freeze verify` hashes.** Freeze record §12 says that `cp17.tools.freeze.verify` "refuses … an
  altered artifact". `verify` hashes the pinned files, the contracts and the package's code. It does not hash
  `artifact-2026-09-06.json` against `freeze_origin.artifact_file_sha256`, or the reference bundle. A changed
  artifact *digest inside the manifest* is refused, and the artifact's self-identity is checked by
  `verify_artifact` in `test_records.py`. But the CLI alone does not refuse an altered artifact file.
- **O3. The host shims are not in the frozen identity.** `src/cp17/host/node_run.mjs` and
  `src/cp17/browser/{index.html,worker.js}` load the package, set the driver's globals and block the network.
  They are committed at the candidate, but they are not in the package's file hashes or in the policy
  identity. The issuing host is identified only by the Pyodide files and the Node binary.
- **O4. `verify_bundle` and a missing `artifact.json`.** `schema.verify_bundle` checks rule 7 only when
  `artifact.json` is present. A bundle whose manifest omits the artifact file still verifies.
- **O5. Procedural notes.**
  - The CI runner commits inside its own throwaway copy, `.local/tmp/cp-17/critic-ci312` and
    `critic-stress`, and removes it. I made no Git write in this repository.
  - The browser run used the Lead's payloads, as step 6 prescribes, after I had shown them byte-identical to
    my own rebuilt payloads.
