# CP-18b: the outcomes, the daily bundle and the final-product Space, on development data

CP-18's preparation, part 2. Everything between an issued day and the visitor's browser that CP-18a left out: the
outcomes' reconciliation and the evaluation records, the dated bundle (built, verified and gated), the final-product
Space that computes only from that bundle, the publication step (prepared, exercised against a local static server
only), and the Space plan §7 step 6's tests and controls. Development data through 2026-09-06 only. Nothing was
uploaded to Hugging Face or published, and nothing under `src/cp17/` or `src/cp17c/` changed: `refreeze verify` on
CP-17c's manifest prints `verified` at the candidate.

## 1. The outcomes' reconciliation (`src/cp18/outcomes.py`)

- **Per UTC key, with source, publication time and revision.** Every issued day's canonical keys (23, 24 or 25) get the
  published price, or `null`. The source is SMARD `chart_data` filter 4169 (DE-LU), the route the snapshot used: the
  hourly product before 2025-10-01, the mean of the four quarter-hour prices from then on (CP-18a's client and its
  aggregation rules, imported).
- **Published or pending.** A price is reconciled once its publication time is at or before the run's wall clock: the
  source document's own time when the response carries one, else the tier register's documented schedule (P's prices
  by 13:00 Europe/Berlin on P−1, ruling 2). Until then the day is pending: every price `null`, nothing scored. A key
  without a value stays `null` and its day is partial.
- **Where the prices come from.** First CP-18a's input archive (`live/inputs/days/<x>/`, where each later day's build
  archived the prices of D−3 to D−1), then the reconciler's own retrieval through the same client, archived in the same
  format under `live/outcomes/archive/`. A failed retrieval archives nothing, so a later run retries it.
- **Revisions.** A later archived record of the same day with other values is reconciled as a revision, with its own
  time as `revised_utc`; the earlier observation stays in the log. A published price is never withdrawn.
- **As the live pipeline runs it.** Each run appends one entry to `live/outcomes/` holding only the days whose
  observation changed. The rehearsal (§6) shows a later run reconciling the day published since.
- **Development days only.** This round reads CP-18a's committed recorded responses (`reports/cp18a/dryrun/recorded/`:
  SMARD values pulled 2026-09-08, rendered in the source's documented response shape and labelled `rendered`). Nothing
  was downloaded. A rendered response carries no document time, so each price's publication time is the documented
  schedule's, and its retrieval time is the snapshot pull's, which in a dry run is later than the simulated wall clock.

## 2. The evaluation records (`src/cp18/evaluation.py`)

`cp17.scoring.evaluate`, per window, per evidence class and per policy (the product, and B0 as context). The three
windows never pool (§19.6):

| Window | Evidence class | Records | In the Space |
|---|---|---|---|
| development | development · post-selection, CP-26's stored nominal forecasts, autumn-2025 (2025-10-01 to 2025-11-30) and spring-summer-2026 (2026-03-01 to 2026-09-06) | A1 and B0 each; static, committed at `reports/cp18b/evaluation/development.json`, every summary equal to CP-17's scoring check (`reports/cp17/scoring-check.json`) | static, from evidence |
| development | development rehearsal · CP-18 dry runs on development days · not prospective and not 4.7T | A1's issued days 2026-08-31 to 2026-09-03 and 2026-09-05; B0 from its served training windows, each equal to the issuing host's shadow by hash | recomputed in the browser |
| 4.7T | one-shot fresh-data test (4.7T) · not yet scored | empty | recomputed (empty) |
| prospective | prospective · evaluation in progress until CP-19 | empty: no prospective day exists | recomputed (empty) |

- **The dry runs' days are a development rehearsal** everywhere: their evidence class, the manifest's evidence label,
  the live claims and the Space. `cp18.spaceglue.window_days` places no development date in 4.7T or the prospective
  record, by rule (a test).
- **Consistency with the static record.** On the five rehearsal days, which also lie in CP-17's spring-summer window, the
  rehearsal's per-day MAE equals the static record's to about 1e-10 EUR/MWh: the issuing host against native
  arithmetic, as F1 records at these origins.
- **The daily record** (`live/evaluation/<as-of day>.json`) holds the recomputed windows and names the static file by
  hash, so a day's commit stays small. The bundle's `evaluation.json` is the static records followed by the day's.

## 3. The dated bundle (`src/cp18/bundle.py`)

Built from the live store, the seven kinds exactly as `docs/track-b/evidence/cp-17/payload-schema.md` defines them.
The committed bundle `reports/cp18b/bundle/` was built from the dry runs' store (`reports/cp18b/dryrun/store/`, CP-18a's
runner run 41204328732, every file equal to the run's own `results-sha256.txt`) as of 2026-09-05 10:00 Europe/Berlin.

| Kind | File(s) | Bytes | From |
|---|---|---:|---|
| manifest | `manifest.json` | 3,661 | the served identity: product, the frozen policy identity `720fc581…` and package `9a2d961a…`, the issuing host, the daily artifact `c18db6d5…` (2026-09-05, A1), its three times, freshness `fresh` as of 2026-09-05 (latest issued 2026-09-05) |
| issued_forecasts | `issued-forecasts.json` | 20,605 | the five issued days, each from its own artifact |
| outcomes | `outcomes.json` | 28,888 | 120 keys reconciled at the run's wall clock |
| evaluation | `evaluation.json` | 345,404 | §2's records |
| fitted_artifact | `artifact.json`, `artifact-arrays.npz` | 8,061 + 2,133,942 | the store's artifact; the issued fit's exported arrays |
| training_window | `A1-2026-09-05.{json,npz}`; `B0-<day>.{json,npz}` × 5 | 538,964; 79,570 | the payloads each day's record names by hash |
| series | `series.json` | 2,324,026 | hourly prices 2019-01-01 to 2026-09-05 (the last day published at the wall clock) |

- **The size budget.** First visit: the manifest and the four records the Space loads at start, **406,619 bytes**,
  of which the static development records are 85%. The training window: **538,964 bytes**, loaded only on "Train it
  yourself" after its size is shown. On request: **4,537,538 bytes** (the fitted arrays, B0's windows, the series).
- **Every served payload is the issued one.** Each training window is taken by the payload hash its day's record holds,
  from the dry runs' payload folders, or rebuilt with no cache by CP-18a's live-input builder from the store's states
  and the recorded responses. The rebuild of all six payloads took 96.5 s and gave the same bundle, file by file
  (`reports/cp18b/sources.json`).
- **The fitted arrays.** The dry run deleted each attempt's `run-arrays.npz` before its upload (`daily.yml`). 2026-09-05's
  issued fit was therefore rerun under the issuing host (Pyodide 0.28.0 in Node.js v26.7.0, with the export on) on the
  issued payload. It reproduced the artifact's quantiles and all eight members' weight hashes in 82 s, and
  `cp18.spaceglue.rebuild_a1` binds the arrays to the artifact again in every build. `python -m cp18.bundle --refit` does
  the same for a run that issued nothing.
- **Freshness** from the store and the wall clock: `fresh` when the target day (the latest delivery day whose cutoff has
  passed) is issued, `failed` when it is decided as not issued, `stale` when it is not decided yet, with the as-of day
  and the latest issued day. Nothing is labelled late or timely.
- **A day not issued is shown with its cause.** The frozen manifest has one free-text field, the product's evidence
  label; the bundle writes each day not issued there, with its cause (`...; not issued: 2026-09-04, outside the issued
  record (rehearsal: ...)`). A failed chain issuance also names its failed artifact, whose attempts carry the causes.
- **The gate before publication** (`cp18.bundle.gate`), failing closed:
  1. `cp18.r7.verify` (R7: a raised error is a refused bundle);
  2. the frozen identity: the manifest's policy identity, package and issuing host, the served artifact's lineage, and
     the served A1 training window's payload identity against the artifact's;
  3. the red line: no served delivery day after 2026-09-06;
  4. `cp18.spaceglue.recompute` natively, the file the Space runs. Any mismatch blocks the day's publication as a
     product failure.

## 4. The negative and positive controls (`src/cp18/controls.py`, `reports/cp18b/controls.json`)

Every rule `verify_bundle` checks has a tampered copy that the gate refuses (20 controls, all refused, the served bundle
publishable):

| Rule | Control | Refused by |
|---|---|---|
| 1 | the freshness state "late" | the manifest schema |
| 2 | a listed file missing; one byte changed; unreadable JSON and NumPy (re-hashed) | the hash and size check; the readers |
| 3 | an unlisted file served | the listing check |
| 4 | a file listed as another kind; outcomes failing their schema | the kind and schema checks |
| 5 | a training window's bit flipped; its meta changed | its own identity |
| 6 | future-label leakage: the target day's price in A1's window, its identity re-made; a released error after D−2 | the embargo |
| 7 | the artifact's identity altered; the manifest naming another artifact; the issued forecast not the artifact's | `verify_artifact` and the cross-references |
| R7 | the verifier raising | `cp18.r7.verify` |
| §16.4 | the policy identity or package altered; a served day past the boundary | the identity and red-line checks |
| §19.5 | a committed record's MAE moved by 0.01 (re-hashed) | the recomputation: ✗ with both values, publication blocked |

The variants the Space is accepted on are built through the real build path where the state can arise (pending: no
outcome retrieval; stale: as of 2026-09-06; failed: 2026-09-06 recorded not issued by a failed H2 check), and by a
re-hashed edit where it cannot (tampered, mismatch, a changed seed, missing/zero/negative prices). §16.4's positive
controls are tests: altered identities, future-label leakage, stale and failed fits, missing, zero and negative prices,
and partial and DST days (a 25-hour, a 23-hour and a partial day through the recomputation).

## 5. The final-product Space (`space-product/`, `scripts/build_product_space.py`)

Built by `python scripts/build_product_space.py --bundle <dated bundle> --out <dist> [--history <v1 build>]` from the
bundle only, under A9. The build refuses a bundle the gate refuses, and any Pyodide file, the package zip or the frozen
browser worker that differs from CP-17c's freeze manifest; it writes the live claims (`app/claims.json`), a
deterministic build record (`app/space-build.json`: every served file with its SHA-256, the checks, the reference
measurements and the size budget) and the Hugging Face card (`README.md`, written, not published).

- **The served layout** is fixed by the frozen "Train it yourself" worker (`src/cp17/browser/worker.js`, served byte for
  byte at `/app/worker.js`): `/index.html`, `/app/`, `/pyodide/` (the 23 pinned files), `/bundle/src.zip` (the frozen
  package), `/payloads/` (the dated bundle) and `/history/` (v1's demo).
- **Start-up.** Only the manifest and the day's records load at start: `issued-forecasts.json`, `outcomes.json`,
  `evaluation.json` and `artifact.json`, each checked against the manifest (SHA-256 and bytes) before it is used. A
  failed check is a visible failure state naming the file, and no view shows data from an unverified file. The served
  identity (the manifest's SHA-256, the policy identity, the package, the issuing host and the daily artifact) is shown
  near the top.
- **The views,** in A9's order: the product panel (first, not a tab), then an accessible tab list with keyboard
  operation and deep links (`#train`, `#forecast`, `#validation`, `#reliability`, `#explainability`, `#features`,
  `#data`, `#limitations`, `#history`).
  - **The product panel:** the status from O13 ("final candidate · pending 4.7T"; v1 stays the released product until
    CP-18's activation), "prospective evaluation in progress", the evidence label with each day not issued and its
    cause, the daily artifact, the three times, the cutoff, delivery dates and timezone, the freshness state; today's
    issued forecast against the published prices with the percentage measure and MAE over the named scored hours
    ("Not yet scored" when none); tomorrow's issued forecast with its nominal bands, or its dated pending or not-issued
    state; and "how sure", the measured coverage with width per band over the named rolling window.
  - **Train it yourself:** the frozen worker in a Web Worker, after the training window's two files are checked against
    the manifest. Before the action: the extra download (45.6 MB: runtime, packages, code and the 0.5 MB training
    window), the reference fit times with their date and runtime, and O14's wording. Cancel, failure and retry. After:
    `cp17.retrain`'s status, the per-member selections the artifact records, the largest difference per quantile level
    and the visitor's runtime, labelled "your retrained model".
  - **Validation:** the three windows apart, each with its badge; the development records static from evidence; the
    rehearsal, 4.7T and prospective records recomputed in the browser with `cp17.scoring` (the product worker runs
    `cp18.spaceglue.recompute`, the file the gate ran natively), ending in a "Matches the stored value" row with ✓ or ✗
    and both values.
  - **Reliability:** the reliability diagram per level with counts, rolling coverage with width per band, the
    quantile-band PIT, per record, never pooled.
  - **Explainability and Features:** `cp17.attribution`'s A1 method on the served fitted artifact (the members rebuilt
    from the served arrays and training window, reproducing the issued quantiles), worded as A9 and §19.7 require;
    one what-if control, labelled "counterfactual scenario — not an issued forecast", approximate and explained as
    such; the day's inputs against their training-window distribution in their source units.
  - **Data:** the shipped series (2019-01-01 to its last date, labelled), with the quarter-hour averaging and the price
    floor defined from the claim layer.
  - **Limitations:** generated from the live claim builder only (`cp18.live_claims`), which keeps `test_24`'s `live_` wall
    and reuses the record layer's own sentences verbatim where they apply.
  - **History:** labelled "Historical", v1's frozen demo at `/history/`, never presented as the product.
- **Network.** The product page and every view load the pinned runtime and the Space's own files only. v1's frozen demo
  at `/history/` loads its runtime from `cdn.jsdelivr.net` and `wasm.marimo.app` as v1 shipped it; that is outside the
  product's rule and is stated beside the route (§10).
- **Presentation.** Built to PUBLISH_RULES §7's tokens and components (canvas `#FAFAFA`, surfaces `#FFFFFF`, text
  `#18181B`, accent `#1D4ED8`, the system font stack, inline SVG charts with table alternatives and mobile variants). The
  visual approval is the Owner's (§8).
- **The size budget.** First visit **551,515 bytes**: the page, its scripts and records (144,896 bytes) and the bundle's
  start files (406,619 bytes, 85% of them the static development records). On request: the runtime and packages
  (44.9 MB, once per visit), the training window (0.54 MB), the fitted arrays with the training window (2.7 MB, for
  Explainability and Features), B0's windows (0.08 MB, for the recomputation), the series (2.3 MB).

## 6. The publication step (`src/cp18/publish.py`) and the rehearsal

- **One publication:** the gate; the Space build carrying exactly the bundle at `payloads/` and matching its own build
  record; one upload of the whole build; then the served identity read back as a visitor reads it (the served manifest
  byte for byte, every file it lists and every file of the Space's build record by hash, and the served artifact the
  intended one). Any difference fails the publication.
- **Exercised against a local static server only** (`LocalTarget`, `127.0.0.1`). `HubTarget` holds the Hugging Face path
  and refuses to write unless CP-18's activation passes its authority; it reads `HF_TOKEN` only inside its one commit.
- **The rehearsal** (`reports/cp18b/rehearsal/`): two runs in one data-only folder. Run 1 at 2026-09-04 12:00 Europe/Berlin
  reconciled 2026-08-31 to 09-03 and left 2026-09-05 pending (published 13:00); run 2 at 2026-09-05 10:00 reconciled it.
  Their records are what the daily pipeline commits to `main`, and run 2's bundle is the committed bundle byte for byte.

**The data-only paths on `main`**, beside CP-18a's `live/store/` and `live/inputs/days/<day>/`:

| Path | What | Written |
|---|---|---|
| `live/outcomes/` | `ledger.jsonl`, `entries/<n>-<day>.json` (each reconciliation's changed days), `archive/days/<day>/` (the reconciler's own retrievals) | each run |
| `live/evaluation/` | `ledger.jsonl`, `<as-of day>.json` (the recomputed windows; the static file named by hash) | once per as-of day |
| `live/bundles/` | `ledger.jsonl`, `<as-of day>/bundle.json` (the manifest and the gate's verdict), `<as-of day>/publication.json` (the served-identity check) | once per as-of day |
| `live/pinned/evaluation/development.json` | the static development records | once, at CP-18's activation |

Each is an append-only, hash-chained record log (`cp18.records`): a file is written once, and a replaced or dropped
line is refused.

## 7. The browser acceptance

Run locally on the integrated build of the committed bundle (`tests/cp18b/space_acceptance.py`; the record is
`reports/cp18b/acceptance.json`, the 181 screenshots stay local, each listed with its SHA-256, viewport, engine, URL,
time and disclosure state). Playwright 1.63.0, Chromium 153.0.8010.12 and WebKit 26.6, on the Apple M3 (macOS 26.5.2),
one browser process at a time, from 2026-11-05T03:14:33+00:00 to 2026-11-05T03:24:32+00:00.

**536 checks passed, 0 failed, 1 not run.**

| Check | Result |
|---|---|
| Every view's content against its records | the product panel's score, "how sure", the Forecast tables, the Validation rows, Reliability, Explainability, Features, Data and the Limitations, each equal to the served records and claims, in both engines |
| "Matches the stored value" on the served bundle | ✓ on every recomputed window (the rehearsal's 296 items per policy; 4.7T and the prospective record empty), both engines |
| The served identity | the manifest `9d35aaa2…` and the daily artifact `c18db6d5…` shown equal to the served and intended ones, both engines |
| Train it yourself | "identical bit for bit" in Chromium (86.5 s) and WebKit (83.2 s); every compared selection matched; largest difference 0 at every level. With member 0's seed changed: "different" (Chromium) |
| PUBLISH_RULES §9's matrix | 1440×900, 768×1024, 390×844, 360×800, 320×700 and an emulated iPhone, both engines: no horizontal page scroll; 200% zoom emulated as a 720-px viewport at device scale 2, and 320-px reflow; keyboard order, visible focus, arrow keys between tabs, anchored targets unobscured; touch targets ≥ 44 px; text and mark contrast from computed styles; charts and controls named; cold start, loading, failure, cancel, retry and the route back |
| Requests | zero non-local requests on the product page and every view, recorded and blocked, both engines. v1's demo at `/history/` requested `cdn.jsdelivr.net` (3) and `wasm.marimo.app` (1), blocked and recorded |
| The variants | tampered: the verification-failure state naming the file; pending: "Not yet scored"; stale and failed: their states, with the cause; prices: partial, zero and negative counted; mismatch: ✗ with both values, blocking publication; seed: "different"; the counterfactual control never labelled issued |
| Not run | WebKit's disclosure state in the accessibility tree: Playwright exposes WebKit's tree only as an ARIA snapshot, so it is recorded as a gap, not a pass (§9) |

A6, the public checks, waits for the publication. Real Safari, a real iPhone and a screen reader were not used.

## 8. What CP-18's activation brief and the publication brief cite

| Item | Value |
|---|---|
| The bundle step | `PYTHONPATH=src python -m cp18.bundle --root <checkout> --project <folder holding .local> --live <checkout>/live --now <ISO> --out <dir> (--arrays <the issuing attempt's run-arrays.npz> \| --refit) [--cache <the run's payload folder>] [--recorded <responses>] --record <file> --commit-records`; exit 0 publishable, 1 refused. In a live run it follows `python -m cp18 run`, in the same checkout, before the day's commit |
| The gate | `cp18.bundle.gate`: `cp18.r7.verify`, the frozen identity (policy, package, issuing host, the artifact's lineage, the A1 window's payload identity), the red line, then `cp18.spaceglue.recompute`; refused means nothing is published for that day |
| The outcomes | `cp18.outcomes.Outcomes.reconcile(archive, issued days, now, run_id, transport)`: the input archive first, then the SMARD client through `transport` (`cp18.live.transport.HttpTransport` at activation; `ReplayTransport` here); publication by the documented schedule or the document time |
| The controls | `PYTHONPATH=src python -m cp18.controls --bundle <dir> --record <file> [--variants <dir>]`: 20 negative controls, all refused (`reports/cp18b/controls.json`) |
| The Space build | `PYTHONPATH=src python scripts/build_product_space.py --bundle <dir> --out <dist> --history <v1's deployed files>`; first visit 551,515 bytes for this bundle; on request 45.1 MB of runtime, packages and code, once per visit |
| The publication step | `PYTHONPATH=src python -m cp18.publish --build <dist> --bundle <dir> --target <served folder> --record <file> --live <checkout>/live`: gate, the build carries exactly the bundle, one upload, the served identity read back (here 878 files, all equal). Activation replaces `LocalTarget` with `HubTarget(<repo>, authorized=True)` (one Hub commit, `HF_TOKEN` read inside it) and `http_fetch` with an HTTPS read of the Space's own origin |
| The browser acceptance | `PLAYWRIGHT_BROWSERS_PATH=.local/tools/ms-playwright .local/tools/playwright/bin/python tests/cp18b/space_acceptance.py --dist <dist> --scratch <dir> --variants <variants> --build-python <project python>`; A6's public checks follow the publication |
| The data-only paths | §6's table: `live/outcomes/`, `live/evaluation/`, `live/bundles/`, and `live/pinned/evaluation/development.json` placed once |
| The bundle's paths and sizes | `reports/cp18b/bundle/` (5,483,121 bytes, 18 files; manifest `9d35aaa2…`); first-visit bundle files 406,619 bytes; training window 538,964; on request 4,537,538 |
| `daily.yml` | unchanged; the activation adds, after the pipeline step: the bundle step above (its `--arrays` from `$RESULTS/run/runs/A1-<day>-*/run-arrays.npz`, before the results step deletes them), the Space build, and the publication step |
| O13 | A1 is "final candidate · pending 4.7T" until 4.7T is scored; "live" only at CP-18's activation, which requires a passed 4.7T; on a fail, v1 stays the released product (`cp18.live_claims`, `fresh_test=`) |
| O14 | CP-17's proposed wording, then: "The issued values were computed in the same WebAssembly runtime the visitor runs. On development days that runtime's results differed from native arithmetic by up to 0.082 EUR/MWh (A1's p2.5 on 2026-03-30), the largest difference observed, not a bound." |

## 9. The red line, the CI, and what stayed frozen

- **The red line.** Every planned and served day is a development day through 2026-09-06; the gate refuses a served day
  past it; `tests/cp18b/test_red_line.py` scans every file this round adds or changes (CP-18a's scanner, this round's
  paths). No market data after 2026-09-06 was downloaded, read, displayed or inferred.
- **Frozen.** Nothing under `src/cp17/`, `src/cp17c/`, `src/delu_forecast/`, `src/cp15/` to `src/cp28/`, `data/`,
  `reports/development-inputs/`, `pyproject.toml` or `uv.lock` changed, and no anchor, governance or published file.
  CP-18a's modules are unchanged: this round adds modules beside them and calls them.
- **`daily.yml` is unchanged.** The bundle step is optional in this round, and a step not exercised on the runner would
  be an untested workflow change; CP-18's activation adds it (§8).
- **CI-ready.** The workflow's steps, the leak scan first, run on a history-free single-commit copy with `CI=true`,
  Python 3.12 and Git's global configuration hidden (CP-18a's `ci-runner.py`); `pytest -m stress` runs locally (the
  return gives the logs). Byte-equality tests over native floating point run on the issuing host's platform only
  (darwin-arm64), with the reason; tests over local-only material skip when it is absent. No test commits.

## 10. Disclosures

- **A pause.** The account's usage limit stopped the round from about 01:40 to 05:10 Asia/Jerusalem on 2026-11-05. In
  flight: the Space Builder, which was cut off after its acceptance run and before its hand-over note. Its files were
  complete on disk; the Lead integrated them rather than restarting it. The Lead's CI rehearsal and stress run had
  finished. Nothing else changed.
- **A bounded Builder** built `space-product/`, `scripts/build_product_space.py`, `tests/cp18b/space_acceptance.py` and
  `tests/cp18b/test_space_build.py` in its own detached worktree (`.local/worktrees/cp-18b/builder-space`), to the
  Lead's assignment; the Lead imported the files, changed three references to claims it had removed (τ, the rolling
  length and τ_eq, now read from the served records), and reran the acceptance on the integrated build.
- **A brief defect, resolved in the anchor's favour.** O14's draft gave F1 as 0.028 EUR/MWh at one DST origin. §24.12
  (R3) records the largest observed figure, 0.082 EUR/MWh; the sentence states it, and the Orchestrator confirmed it
  (`docs/track-b/evidence/cp-18b/orchestrator-confirmation-as-relayed.md`).
- **Two gaps in the frozen schema, accepted by the Orchestrator, schema unchanged:**
  - the issued artifact records four of A1's per-member selections (the seed, the training and held-out day sets, the
    latest training day) and each member's weights' hash, so "Train it yourself" compares those; the other selections
    (early stopping's epochs, the winsorisation and cap activations, the crossing restorations) are not in the bundle,
    and the Space says so (`live_limitation_retrain_selections`);
  - the manifest has no field for a day's cause of not being issued, so the bundle writes each day not issued, with its
    cause, in the manifest's free-text evidence label.

  A dedicated field for each is a schema change, so it belongs to the next freeze.
- **The fitted arrays were recovered by a refit.** The dry runs deleted each attempt's arrays before upload. The issued
  fit of 2026-09-05 was rerun twice under the issuing host; both runs gave byte-identical arrays reproducing the
  artifact's quantiles and weights (`reports/cp18b/sources.json`).
- **Rendered development responses.** The outcomes on development days come from SMARD values pulled 2026-09-08,
  rendered in the source's response shape (CP-18a's recorded material), so their publication times are the documented
  schedule's and their retrieval time is the pull's, later than a dry run's simulated wall clock.
- **The manifest's times** are the issued artifact's own (frozen `cp17.issue.artifact`): last training and issuance at
  D−1 11:00 Europe/Berlin, and the data refresh, which the dry runs' prebuilt payloads left empty, shown as "not
  recorded". Each issuance's actual run time stays in the day's record in the store (§24.13).
- **v1's History route.** The local check used a rebuild of v1's export from v1's own build script, which is not
  byte-identical to v1's deployed bundle (its `index.html` differs); the published History route serves v1's deployed
  files as they are. v1's demo loads its runtime from `cdn.jsdelivr.net` and `wasm.marimo.app`, as v1 shipped it.
- **The accessibility tree in WebKit.** Playwright exposes WebKit's tree only as an ARIA snapshot; the acceptance records
  that as a gap, not a pass (PUBLISH_RULES §9).
- **The early CI rehearsal found two portability faults, both fixed:** two new modules named the frozen verifier outside
  `cp18.r7` (CP-18a's rule test), and the rehearsal compared gzip bytes, which follow the zlib version.
- **Compute:** about 2 machine-hours of the 12 before the final checks (`reports/cp18b/compute-ledger.json`), at most 4 concurrent workers.
  **GitHub:** no runner was used; 0 job-hours of 5.
