# Verdict — CP-17 — Integration — PASS

- Candidate SHA: ca874204e768fdb2539f9c1e07d87b524c95c7db
- Plan / version / bar: `capstone_v21.md`, revision v21-r17, SHA-256
  `3124451da84c3cd99fae728c371207aace6ae537474f7769d0ff6333ee53e4fc`; bar `### 24.9 CP-17 and 4.7T` (40 lines,
  2,007 bytes, section SHA-256 `6675e907ccad916e02059b12479daec712f0e720efd4c4056e656b863027a0f1`), together with
  §16.2, §19.2, §19.3, §19.5, §19.7 and §16.4's CP-17 row, under the issued brief
  `docs/track-b/evidence/cp-17/issued-brief.md` (`9f235cf8…1b1a73`) and the Owner's decisions record
  `docs/track-b/pre-cp-17-rulings-2026-10-25.md` (`d29b0abc…a8f6b0`). This is the second Integration review; the
  first (FAIL, `dc78e209…`) is `docs/track-b/evidence/cp-17/integration-attempt-1.md` at the candidate.
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
- Worktree clean before and after: yes. `git -C /Users/djourno/Downloads/PJM/.local/worktrees/cp-17/critic-2
  status --porcelain` was empty, and `HEAD` was `ca874204e768fdb2539f9c1e07d87b524c95c7db`, before the review,
  after the reproduction steps, and before this verdict was written. The only byproduct inside the worktree is
  gitignored bytecode (`src/*/__pycache__/`, created by the package build of step 5), which invalidates nothing.

## Commands actually run

Each command ran from the worktree unless another directory is named. My outputs are under
`/Users/djourno/Downloads/PJM/.local/artifacts/cp-17/critic-2/` (`repro/`, `scripts/`, `*.console.log`,
`critic-brief.md`, `bar-sections.txt`). Every Python command had `MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1`,
`PYTHONPATH=src` and `PYTHONDONTWRITEBYTECODE=1`; every native fit also had the five BLAS variables at 1. No
network contact was made, and I performed no Git write in this repository.

0. **The brief and the bar.**
   - `git show main:scripts/gauntlet.py | python3 -I - critic-brief cp-17`: exit 0, 295 lines (kept as
     `critic-2/critic-brief.md`, SHA-256 `ff3c5967…`).
   - `git show main:scripts/bar.py | python3 -I - bar capstone_v21.md '<heading>' --at ca874204…`, for the six
     headings: exit 0 each. The identities equal the brief's table: §24.9 40 lines, 2,007 bytes, `6675e907…`;
     §16.2 32, 2,408, `c54723ef…`; §19.2 6, 335, `53834210…`; §19.3 25, 1,354, `5d1f869e…`; §19.5 19, 1,170,
     `1d47a505…`; §19.7 12, 494, `10060bd2…`; the plan `3124451d…`.
   - `shasum -a 256`: `issued-brief.md` `9f235cf8…`, `issued-brief-v1-9e522b9a.md` `9e522b9a…`, the rulings
     `d29b0abc…`, `capstone_v21.md` `3124451d…`; each equals its citation.
   - After this verdict was written: `git show main:scripts/bar.py | python3 -I - check <this verdict> --source
     capstone_v21.md@ca874204…`: exit 0, "ok: lines 13–52 (2006 bytes) appear in capstone_v21.md@ca874204e768".
1. **The whole suite in CI mode.** I read the runner first, then ran
   `python3 /Users/djourno/Downloads/PJM/.local/artifacts/cp-17/ci-runner.py critic2 ca874204… ci312`.
   - **One deviation, procedural:** the label `critic2`, not `critic`, because `critic` would have written into
     `.local/artifacts/cp-17/critic-validation/`, which holds the first Critic's logs. Mine are in
     `.local/artifacts/cp-17/critic2-validation/ci312/`.
   - Exit 0. `results.json`: `complete: true`, `scratch_removed: true`, tree `cabbd2f9…`, which equals
     `git rev-parse ca874204…^{tree}`. Python 3.12.14, `CI=true`, offline, local-only inputs hidden.
   - The workflow's seven steps, exit code and seconds:
     - `uv sync --locked --dev`: 0 (1.2 s);
     - `build_wasm_payload.py`: 0 (164.0 s);
     - `pytest -q`: 0, "2310 passed, 41 skipped in 517.03s";
     - `test_10_cqr_order_statistic.py`: 0, "8 passed";
     - `verify_release.py`: 0, "PASS — every bound claim agrees on every surface; …";
     - `test_22_wasm_equivalence.py`: 0, "15 passed";
     - `publication_guard.py tree`: 0, "the tree carries no placeholder and a final build record".
   - The stress collection: exit 0, "19/2350 tests collected (2331 deselected)".
   - Every CP-17 skip states its reason, for example `tests/cp17/test_hosts.py: the pinned Pyodide, Node.js and
     the reproduction payloads are absent` and `test_real_inputs.py:41: CP-26's local-only stored state (the
     evidence/cp-26 extract) is absent`.
2. **`pytest -m stress`, CI unset:** the same runner, mode `stress`.
   - Exit 0: "19 passed, 1 skipped, 2331 deselected in 454.46s". `complete: true`, `scratch_removed: true`.
   - The one skip is collection-level and not CP-17's:
     `pytest -p no:cacheprovider -m stress --collect-only -q -rs` (worktree, exit 0) reports
     `tests/cp20/test_gfs_eccodes.py:11: could not import 'eccodes'`. The 19 collected stress tests include
     `tests/cp17/test_hosts.py::test_issuing_host_reproduces_its_record` and
     `::test_browser_reproduces_the_issuing_host`, so both ran and passed.
3. **The GFS check.** `.venv/bin/python -m cp17.tools.gfs_check --out repro/gfs/gfs-check.json`
   - Exit 0, 41.5 s, printed `BLOCKED {"MAE": 0.02270720735470033, "WIS": 0.06683811993513378}`.
   - `cmp` against `reports/cp17/gfs-check.json` and `reports/cp17/gfs-check-daily.csv`: both byte-identical.
   - An independent recomputation from the committed daily CSV (`scripts/gfs_recompute.py`, standard library
     only; every count and mean asserted against the record), exit 0:

     | Mask | Eligible | Paired dates | Paired hours | MAE excess | WIS excess |
     |---|---:|---:|---:|---:|---:|
     | affected | 1,358 | 1,354 | 32,478 | +2.2707% | +6.6838% |
     | unaffected | 710 | 696 | 16,686 | +34.6081% | +40.0942% |
     | every eligible date | 2,068 | 2,050 | 49,164 | +11.6432% | +16.1813% |

4. **One native parity origin.**
   `.venv/bin/python -m cp17.tools.parity --out repro/native --origins 2026-03-29 --attribution 2026-03-29`
   - Exit 0, 87 s: `2026-03-29 PASS {'A1': True, 'v2': True, 'v4': True, 'v5': True, 'B0': True}`.
   - My `checks` block is identical to `reports/cp17/native-parity.json`'s for that origin. All five payload
     digests (A1 `89e502a4…`) and quantile hashes (A1 `67ef0f36…`) equal the record's.
   - **Against the tag directly.** The ledger file `forecast-ledger/2026-03-29.json` (SHA-256 `38bf8232…`) is git
     blob `33a6161c…`, which `git ls-tree evidence/cp-26` (tag at `ca203312…`) lists. My A1, v5, v4, v2 and B0
     quantiles are IEEE-754 identical to its `members.nominal.D2.quantiles` and `policies.nominal/<p>.native_quantiles`
     on all 23 rows (`scripts/ledger_bitwise.py`).
   - My nine payload files are byte-identical (`cmp`) to the Lead's `final/native/payloads/` for that origin.
   - **Also `--origins 2026-09-06`:** exit 0, 90 s, PASS; quantile hashes equal the record's, and all nine
     payload files are byte-identical to the Lead's, which step 6 uses.
5. **One issuing-host parity origin.**
   - `python -m cp17.tools.bundle --out repro/bundle/src.zip`: exit 0, "33 files 86707 bytes 0aa2aed8ffbe7e82".
     `files_sha256`, `package_sha256` (`ac45f033…`), `zip_sha256` (`0aa2aed8…`, 86,707 bytes) and
     `runner_files_sha256` all equal `reports/cp17/bundle-manifest.json`. No `cp17/tools/` file, and no `.mjs`,
     `.js` or `.html`, is in the zip.
   - `python -m cp17.tools.hosts node --bundle repro/bundle/src.zip --payloads repro/native/payloads --out repro/nodes --runs A1-2026-03-29 --attribution A1-2026-03-29`:
     exit 0, 85 s, "A1-2026-03-29 ok 85s". No errors, no blocked request; Pyodide 0.28.0, Node v26.7.0; the 18
     executed files equal the package's hashes. Quantiles `b5ca894f…cc05`, which equals the committed
     `issued_quantiles_sha256` bit for bit.
   - `cp17.retrain.compare('A1', <my native fit>, <my host fit>)`: "within ±0.01 EUR/MWh", the committed status;
     payload identity equal; every selection matched; largest 6.27698966582102e-07 EUR/MWh; the per-level maxima
     equal the record's.
6. **One browser identity run and v4's browser run.**
   `PLAYWRIGHT_BROWSERS_PATH=… .local/tools/playwright/bin/python src/cp17/tools/measure.py --pyodide … --bundle repro/bundle --payloads .local/artifacts/cp-17/final/native/payloads --out repro/browser.json --runs A1-2026-09-06,v4-2026-09-06 --browsers webkit --attribution 1`
   - Exit 0: "webkit A1-2026-09-06 ok 70.4s", "webkit v4-2026-09-06 ok 80.3s". WebKit 26.6. No errors, no
     blocked request, no 404; the executed files (18 and 19) equal the package.
   - **A1:** quantiles `4e6abb02…a5`, equal to the committed issuing-host A1-2026-09-06 and to the freeze
     artifact's `quantiles_sha256`. Against the Lead's raw issuing-host output (`final/nodes/node-A1-2026-09-06.json`):
     "identical bit for bit".
   - **v4:** quantiles `76599de7…c9`, equal to the committed issuing-host v4-2026-09-06; against the raw output,
     "identical bit for bit", selections matched.
   - **Against my native 2026-09-06 fits:** A1 "within ±0.01 EUR/MWh" (9.38e-13), v4 "within ±0.01 EUR/MWh"
     (4.26e-13), selections matched and payload identity equal for both.
   - **Measured** (in-worker): A1 70.2 s, browser RSS peak 1.21 GB, WebAssembly memory 225 MB; v4 79.4 s,
     1.45 GB, 324 MB.
7. **The freeze manifest and the CP-17 tests.**
   - `python -m cp17.tools.freeze verify docs/track-b/evidence/cp-17/freeze-manifest.json`: exit 0, `verified`.
   - `pytest -p no:cacheprovider tests/cp17 -q -rs --basetemp=repro/pytest-tmp`, BLAS at 1, CI unset: exit 0,
     "57 passed in 221.46s", no skips.
8. **My own checks.**
   - **The policy identity recomputed.** `python -m cp17.tools.freeze identity --bundle-manifest repro/bundle/src.json --protocol-from repro/native0906/payloads/v4-2026-09-06.json --out repro/policy-identity.json`:
     exit 0, "policy identity b304d6479a86…", and the whole object equals the manifest's `policy_identity`.
   - **The freeze-origin issuance reproduced.** `python -m cp17.tools.issuance --day 2026-09-06 --gfs 1 --payloads repro/native0906/payloads --bundle repro/bundle/src.zip --identity repro/policy-identity.json --out repro/issuance`:
     exit 0, 87 s, `[('A1', 'ok')] successful daily fit, within ±0.01 EUR/MWh`. My artifact equals the committed
     `artifact-2026-09-06.json` in every field except the measured resources and the attempt's timing (70.36 s
     and 846,217,216 bytes against 69.84 s and 840,499,200), which the artifact's identity includes. The
     quantiles (`4e6abb02…`) and the exported arrays (`15bf7731…`, the manifest's) are identical.
   - **The real A1 failure reproduced.** The same tool at `--day 2022-12-04 --gfs 1` with an empty
     `--payloads` folder, so the tool rebuilt the payloads: exit 0, 130 s. Natively and under the issuing host
     the path is `[A1 failed, v4 ok]`, "failed fit; fallback v4 issued"; A1's cause is member 2 (seed 26590021),
     `nonfinite_loss` at epoch 21. My rebuilt payloads are byte-identical to the Lead's `final/payloads-2022-12-04/`,
     and my v4 quantiles equal the Lead's artifact. The Lead's two artifact files hash to the committed
     `artifact_file_sha256` values.
   - **Criterion 5 on real payloads** (`scripts/ceiling_real.py`, the 2026-09-06 payloads, native fits, the
     measured resources replaced by stated values; exit 0). In every case `verify_artifact` returned `[]`, and
     the issued quantiles are the issued policy's own native fit:
     - A1 over 900 s: fitted A1, v4; v4 issued, "failed fit; fallback v4 issued";
     - A1 over 4 GiB, v4 over 900 s: fitted A1, v4, v2; v2 issued;
     - A1, v4, v2 over: B0 issued;
     - all four over: "failed issuance", no quantiles, resources `None`;
     - GFS late with v2 over 4 GiB: A1 skipped, v2 failed, B0 issued;
     - A1 at exactly 900 s and 4 GiB: A1 issued (the ceiling is inclusive).
   - **`freeze verify` on altered files.** On a `git archive ca874204…` copy outside the worktree (deleted
     afterwards), `freeze verify … --root <copy>`: unchanged, exit 0 `verified`; one character of the freeze
     artifact's display changed, exit 1 "the freeze-origin artifact is missing or altered"; a line appended to
     `src/cp17/browser/worker.js`, exit 1 "src/cp17/browser/worker.js: missing or altered".
   - **The reference bundle** (`.local/artifacts/cp-17/final/reference-bundle/`, the recorded location; it
     exists). Its manifest hashes to `45ecd6e4…`, equal to `reports/cp17/reference-bundle.json` and the freeze
     manifest. `schema.verify_bundle` returns `[]`. Refused: each of `artifact.json`, `outcomes.json`,
     `evaluation.json` and `issued-forecasts.json` removed from the manifest and the files; one quantile of
     `artifact.json` changed; `series.json` truncated. Its `artifact.json` equals the committed freeze artifact,
     and its arrays hash to the manifest's.
   - **Runtime identities.** All 23 Pyodide files hash to CP-17-probe's retrieval manifest (`37bf451f…`) and to
     the freeze manifest; the Node binary hashes to `1ef99ea2…d040`, the manifest's.
   - **Paths.** `git diff --name-status dd5e57f..ca874204…`: 67 files, all added, all under `src/cp17/`,
     `tests/cp17/`, `reports/cp17/` or `docs/track-b/evidence/cp-17/`; `be504ab..dd5e57f` touches only
     `progress.md` and the rulings. `git diff --quiet dd5e57f ca874204… -- src/cp17probe src/cp15 … src/cp28 src/delu_forecast data reports/development-inputs pyproject.toml uv.lock 'capstone_*' 'syllabus_*' program-stage-sequence.md AGENTS.md CLAUDE.md <role files> docs/track-b/gauntlet-templates.md docs/PUBLISH_RULES.md docs/track-b/publication-standard-v1.md docs/track-b/rule-inventory.md docs/track-b/cp-0-defects.md docs/track-b/exposure-ledger.md docs/track-b/backup-register.md .claude .github`:
     exit 0. `pyproject.toml` `aa35326a…`, `uv.lock` `5d2aecc3…`.
   - **Sizes.** `git ls-tree -r -l ca874204…`: no blob over 50 MB (largest 30.8 MB, pre-existing); the largest
     CP-17 file is 308,888 bytes.
   - **Dates** (`scripts/date_scan.py` over the 67 added files). Every date after 2026-09-06 is a protocol,
     ruling, issue, run-name or job-time date: the 4.7T window and gate, S_14, the analysis seed 20261204, the
     snapshot pull of 2026-09-08, `cold-rerun-2026-10-15`, the ruling dates and the compute-ledger times. No UTC
     key or value of a later delivery day occurs; the freeze artifact's last key is `2026-09-06T21:00:00+00:00`.
   - **The boundary.** `cp25/guard.py` has `BOUNDARY = date(2026, 9, 6)`; `data/snapshot.parquet` ends at
     2026-09-06 21:00 UTC; the ledger extract ends at `2026-09-06.json`; `reports/cp17/retrieval-manifest.json`
     records 0 data bytes, 0 software bytes and 0 remote writes.
   - **The freeze record's citations** hold at the candidate: `src/cp26/members.py:199`, `:213`;
     `src/cp24/design.py:306-307`; `src/cp15/models.py:45`; `src/cp21/lgbm.py:123-126`; `src/cp15/data.py:79-80`;
     `src/cp24/member.py:43-45`.
   - **A dead issuing-host process** (observation N1). With `cp17.tools.issuance.NODE` replaced by
     `/usr/bin/false` in a scratch interpreter, `host_issuance(…, 2026-09-06, gfs=True, …)` raised
     `FileNotFoundError` for `node-attempt-A1-2026-09-06.json` instead of recording a failed A1 fit.
   - **Compute.** `reports/cp17/compute-ledger.jsonl` sums to 4.23 worker-hours. This review added about one
     machine-hour, on at most three concurrent jobs.

## Evidence actually inspected

- **The packaged brief** in full, and the decisions record (decisions 1–12) in full.
- **The first verdict**, `integration-attempt-1.md`, in full: its gap G, its acceptance test and O1–O4.
- **The frozen documents**, in full: `freeze-record.md`, `4-7t-frozen-protocol.md`, `definitions.md`,
  `payload-schema.md`, `artifact-2026-09-06.json`, `schemas/fitted_artifact.schema.json`; `freeze-manifest.json`,
  every section.
- **The records:** `reports/cp17/report.md` in full; `gfs-check.md`, `.json`, `-daily.csv`;
  `native-parity.json`; `host-parity.json` (all 15 issuing-host rows, the four browser rows, F1's per-level and
  per-member deviations and selections); `issuance.json` (all three cases); `controls.json`;
  `scoring-check.json`; `reference-bundle.json`; `bundle-manifest.json`; `retrieval-manifest.json`;
  `compute-ledger.jsonl`.
- **The code:**
  - read in full: `src/cp17/issue.py`, `retrain.py`, `scoring.py`, `host/driver.py`, `host/node_run.mjs`,
    `tools/issuance.py`, `tools/hosts.py`, `tools/fresh_test.py`, and the diff `dc78e209..ca874204` of every
    changed code and test file (`issue.py`, `schema.py`, `host/`, `browser/worker.js`, `tools/bundle.py`,
    `tools/freeze.py`, `tools/records.py`, `tools/refbundle.py`, `tools/issuance.py`, `tests/cp17/test_units.py`,
    `test_records.py`);
  - read in part: `tools/freeze.py` (identity and `verify`), `tools/ledger.py`, `tools/gfs_check.py`,
    `tools/measure.py`, `schema.py`, `tests/cp17/test_hosts.py`, `test_records.py`;
  - from the landed code: `cp28.inference.test_endpoint`, `cp25/guard.py`'s boundary, and the cited lines above.
- **The commit log** `be504ab..ca874204` on `gauntlet/cp-17`, including `05bb6c51` (the training-window binding)
  and `e1e62f3a`/`ca874204` (the per-attempt rule and the regenerated records).
- **The Lead's local material the brief names:** `ci-runner.py`, `critic-open.json`, `final/native/payloads/`,
  `final/nodes/`, `final/issuance/`, `final/payloads-2022-12-04/` and `final/reference-bundle/`. I did not open
  the Lead's return drafts, CI notes, assignment drafts or other narrative files in `.local/artifacts/cp-17/`.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1 | **Brief item 1: the A1 GFS check** (done at `2d570e0`; rulings 11 and 12 followed) | PASS | Rerun byte-identical (JSON and daily CSV); my independent recomputation gives the same populations and means, +2.2707% MAE and +6.6838% WIS on 1,354 affected dates, so the rule is met. The record stays as committed. Decisions 11 and 12 are `cp17.issue.CHAINS`, the manifest's `failure_policy` and freeze record §10, with the excess disclosed. |
| 2 | **Brief item 2: one code path, `src/cp17/`** (§19.2) | PASS | 33 files, measured from the import closure and rebuilt byte-identical; no `cp17/tools/` file ships; the two stand-ins are in the package hashes. Native, Node, Chromium (stress test) and WebKit (my run) executed files equal to the package. A1, v4, v2 and B0 fit from their payloads; v5 natively. No exception route needed. |
| 3 | **Brief item 3: the issuing host and its parity** | PASS | **Native:** bitwise for five policies at nine origins (record); I reran 2026-03-29 and 2026-09-06 (PASS), and 2026-03-29 is IEEE-754 identical to the tag's ledger directly. **Issuing host:** 15 runs, every selection matched, all within τ_eq except F1, which is reported; I reproduced A1-2026-03-29 bit for bit. **Browser identity:** committed for both browsers; I reproduced WebKit, and the stress test reproduced Chromium. **v4 in the browser:** time, memory, payload, deviation and selections recorded for both browsers, and reproduced in WebKit. **Data:** nothing after 2026-09-06. |
| 4 | **Brief item 4: the freeze record and `freeze-manifest.json`** | PASS | Every field of §16.2's list, §16.4's row and the brief's list is present (record §§1–14, manifest sections). `freeze verify` gives `verified`, and refuses an altered artifact file and an altered runner (my tamper copy). The failure policy is stated exactly as decisions 11 and 12 rule it; §10 now states criterion 5 per attempt and the chain moving on. The gaps G1, C1, C2, G2 and F1 are reported with their files and lines, which hold, and no landed code changed. I recomputed the policy identity (`b304d647…`) and reproduced the freeze-origin artifact apart from its measured resources. |
| 5 | **Brief item 5: §19.5's definitions** | PASS | `definitions.md` matches the brief: τ = 10 inclusive; the denominator; partial days with completeness; zero, negative and missing prices; the label; the 28-scored-day rolling window; the eight-band PIT with closing-quantile ties; the reliability counts; 1e-9·max(1, \|b\|). `scoring.py` implements it as written (read). The unit tests pass, and `scoring-check.json` is native against the issuing host, bit for bit, on 2,536 and 7,696 items per policy. |
| 6 | **Brief item 6: §19.3's retrain comparison and §19.7's attributions** | PASS | **The status rule:** decision 9's three statuses in `retrain.status`; `compare` binds `payload_sha256` and reports "different" on a mismatch, keeping `measured_status`. **Controls:** seed "different"; training window "different" (measured "within", 0.0091); target-day outcome leaves all four payloads byte-identical. **Selections:** CP-17-probe's lists (`preprocessor` and weight hashes are diagnostics in both). **Attributions:** by class as the brief fixes them. **The reference runtime** is frozen in record §14 and the report. |
| 7 | **Brief item 7: the payload schema and manifest** | PASS | Seven kinds with machine schemas (tested equal to `schema.SCHEMAS`); the manifest fields; the per-policy embargo. The reference bundle verifies at its recorded location (`45ecd6e4…`), and the four committed controls plus my six refusals hold, including a missing `artifact.json`. |
| 8 | **Brief item 8: 4.7T's frozen protocol, outcome-blind** | PASS | Every sub-item is present: comparators; p50 MAE and WIS with equal date weights and CP-26's keys; the four endpoints with 0.995; the compound max-p at α = 0.05, no Holm; 7-day blocks, 10,000 replicates, seed 20261204; how forecasts are generated; minimum support 60 of 90 with its reason; the failure rules; the §24.2 audit; the retrieval plan, prepared and not run, with the guard moving only at the gate; PUBLISH_RULES §14's four items. `fresh_test.py` matches the text and is tested on synthetic losses. No 4.7T outcome is used. |
| 9 | **The success definition** (brief, "A successful daily fit") | PASS | Criteria 1–3 in `check_inputs`/`check_emission`, the eight-member rule (2022-12-04 reproduced), and criterion 5 now in `issue.attempt` on each attempt's own fresh-process measurement, before `decide` moves on. A1 over the ceiling goes to v4, v4 to v2, v2 to B0, B0 to a failed issuance; the GFS-late chain applies it too; fallbacks are judged by the same criteria; nothing over the ceiling is issued (unit tests, and my run on real payloads). The GFS-late skip and the display rules hold. Conflicts C1 and C2 are reported for r18, as the brief requires. See N2 and N3. |
| 10 | **Further item 1: blind** | PASS | Boundary 2026-09-06 in `cp25/guard.py`, unchanged; the snapshot and the ledger extract end at 2026-09-06; no later delivery key or value in any added file; 0/0/0 retrieved; no non-local request in any host or browser run, mine included. |
| 11 | **Further item 2: GitHub-landable** | PASS | No blob over 50 MB. Extracts, payloads and the reference bundle stay in `.local/artifacts/cp-17/`, listed in committed manifests. |
| 12 | **Further item 3: CI-ready** | PASS | The seven steps green on a history-free single-commit copy, `CI=true`, Python 3.12.14, offline. `pytest -m stress` passes locally (19 passed), with both CP-17 host and browser tests run. Local-input tests skip with stated reasons; the timing-sensitive tests carry `stress`. |
| 13 | **Further item 4: no pinned file changes** | PASS | Only added files, in the four allowed paths, since `dd5e57f`; every protected path unchanged; `pyproject.toml` and `uv.lock` at their pinned hashes. |
| 14 | **Further item 5: the Critic's reruns** | PASS | Done: steps 1–7 above, plus the issuances, the identity and the tamper checks. |
| 15 | **§24.9 CP-17 and 4.7T** | PASS | **Frozen:** the candidate A1; the daily rule, the issue time, the inputs and tiers; the S_13 search state with no combiner; S_14 = 2027-01-06 as a protocol date; the tier and margin rulings by hash; the fallback and failure rules, now including the resource ceiling per attempt; §19.5's definitions; the lock price, not adopted. **Registered:** comparators, scores, pass conditions and margins, a dependence treatment for 90 days, failure rules, PUBLISH_RULES §14, and the audit with its BLOCKED rule. |
| 16 | **§16.2 What freezes and what updates every day** | PASS | The freeze list is complete (record §§2–14, manifest). Each artifact carries its training window, seeds, timestamps and parent, input and state hashes. Resource exhaustion now fails the fit and applies the frozen fallback, or records a failed issuance; failed and skipped fits are displayed as such. |
| 17 | **§16.4's CP-17 row** | PASS | Designation and prerequisites (§1); policy, initialization and registry identities (§§2, 6, 12); daily fit and failure rules (§10); metric formulas (`definitions.md`); the resource and calendar plan (§13, protocol §11). |
| 18 | **§19.2 One code path** | PASS | As item 2. The fit, the chain's judgement (`cp17.issue`) and the scoring are package files; the runners that load the package are now frozen beside it. |
| 19 | **§19.3 "Train it yourself"** | PASS | τ_eq and the reference runtime are frozen from the probe. The comparison reports selections, per-level maxima and one of three statuses, and never replaces or relabels an issued forecast. The visitor's retrain is bit-identical to the issuing host in both browsers (I reproduced WebKit); v4 was measured. No exception is needed. |
| 20 | **§19.5 Definitions** | PASS | As item 5. Every value was fixed before any evaluation outcome: τ is the Owner's; 28 days and 1e-9 are the brief's. |
| 21 | **§19.7 Attribution and importance** | PASS | Blend, linear, tree (TreeSHAP and gain) and neural (group Shapley) methods frozen, with the "within one fitted artifact, never causality" wording in the code, the record and the report. |
| 22 | **The first review's acceptance test** | MET | **Unit tests:** `test_a_fit_over_the_resource_ceiling_fails_and_the_chain_moves_on` (five cases: A1→v4 by time and by memory, →v2, →B0, failed issuance), `test_the_gfs_late_chain_also_applies_the_ceiling`, `test_resources_at_the_limit_pass_and_unmeasured_resources_are_not_judged`; each asserts the issued quantiles are the issued policy's own. **Freeze record §10** states it. **Records regenerated:** package `ac45f033…`, identity `b304d647…`, artifact `a0bec858…`, manifest `a775e5ce…`; `freeze verify`, `tests/cp17` (57 passed), the stress host and browser tests, and my host and browser reruns all pass against them. |
| 23 | **The first review's smaller observations** | MET | **O1:** the record and `payload-schema.md` name `.local/artifacts/cp-17/final/reference-bundle/`, which exists and verifies. **O2:** `verify` hashes the freeze-origin artifact and checks it against the manifest (refused on my altered copy). **O3:** `runner_files_sha256` freezes `node_run.mjs`, `worker.js` and `index.html` in the identity and in `verify` (refused on my altered copy). **O4:** `verify_bundle` requires the four start-up kinds and `artifact.json` (refused when removed). |
| 24 | **The F1 issuing-host miss** | PASS | Reported and not tuned: A1 at 2025-10-26 is "different", 0.0279 EUR/MWh at the p50, per-level maxima recorded, every selection matched; member 5 (cp26-k11-t032, seed 27190032, 1,000 epochs) 0.77, member 4 3.6e-05, the rest about 1e-13. Freeze record §11 F1 and the report state it for the Owner and r18; τ_eq stays 0.01. |
| 25 | **`retrain.compare` binds the training window** | PASS | The payload identity is checked before the status is reported, and a mismatch is "different" (§19.3 item 1: "from that fit's shipped training window"); decision 9's three statuses are otherwise unchanged. Commit `05bb6c51` records the first run's control reading "within ±0.01" (0.0091) and the change. |
| 26 | **The report's tables and prose** | PASS | `test_report_tables_are_the_records` passed in CI mode and in my `tests/cp17` run. The prose figures I checked agree with the records: 33 files; +2.27%/+6.68% on 1,354 dates; F1's 0.028, 0.77 and 3.6e-05; the issuances' 69.8/61.0/62.0 s and 802/868/887 MiB; 2,536/7,696 items; 489 negative-price hours; 428 state days. |

## On FAIL only

Not applicable: the verdict is PASS.

## Observations (not blocking)

- **N1. The issuance driver is outside the frozen identity, and does not handle a dead process.**
  `cp17.tools.issuance.host_fit` runs each attempt's Node.js process with no timeout, ignores its exit code,
  and reads a fixed output path. A process that dies without writing its record raises out of `issue.decide`
  (demonstrated above), so the chain does not move on. A stale record left in the same `--out` folder would be
  read as the attempt's own (by reading the code). The frozen rule in `cp17.issue` is correct, and no committed
  record is affected. But criterion 5's measurement reaches `cp17.issue` only through this native-only driver,
  which the freeze manifest does not hash. CP-18's pipeline and the 4.7T runner should treat a missing or
  unreadable attempt record, or a timeout, as a failed fit, and r18 may want to name the driver that 4.7T uses.
- **N2. Criterion 5 depends on the caller supplying a measurement.** With `resources=None`, `issue.attempt`
  passes the fit and records "not judged". Neither the artifact schema nor `verify_artifact` refuses an issued
  artifact whose resources are not a measurement. The native comparison path needs this; a production artifact
  should not carry it.
- **N3. Criterion 4 is judged after the chain.** `issue.artifact` runs after `decide`, so an artifact failure
  could not move the chain. By construction it can fail only by raising, so this has no practical effect today.
- **N4. `freeze verify` recomputes less than the record says.** The freeze record's opening "Verifying it"
  paragraph says it "recomputes every recorded file hash from the files themselves". It does not recompute the 23 Pyodide hashes, the Node binary or
  `k13.json`'s hash. I checked those separately, and all equal the manifest.
- **N5. The report's r18 open-items list omits F1.** It lists G1, C1, C2 and G2. F1 is in the parity tables and
  in freeze record §11, marked "For r18".
- **N6. The machine-readable manifest does not carry the browser part of the reference runtime** (Chromium
  153.0.8010.12, WebKit 26.6, Playwright 1.63.0, the machine class). Freeze record §14 freezes them in prose.
- **N7. Cosmetic.** `resources_ok` formats wall time with `.0f`, so 900.001 s reads "wall time 900 s over the
  15-minute ceiling".
- **Procedural.** The CI runner commits only inside its own throwaway `git init` copies
  (`.local/tmp/cp-17/critic2-ci312`, `critic2-stress`) and removed both. My one tamper copy was outside the
  worktree and is deleted. I made no Git write in this repository.
