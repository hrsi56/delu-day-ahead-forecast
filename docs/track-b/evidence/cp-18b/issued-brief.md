# Track B Checkpoint Brief — CP-18b (CP-18's preparation, part 2: the outcomes, the daily bundle and the final-product Space)

*Issued by the Orchestrator on 2026-11-04, Asia/Jerusalem, under the Owner's decisions 7, 25, 26 and 27.*

## Target
- Repository: DE-LU day-ahead forecasting, `/Users/djourno/Downloads/PJM` (origin
  `hrsi56/delu-day-ahead-forecast`). The checkpoint runs locally, in the Lead's own worktree. It may also run in
  CP-18a's public scratch repository (below).
- Authorized checkpoint: CP-18b, exactly one.
- **What follows it:** 4.7T, no earlier than 2026-12-04, then CP-18's activation and the complete publication, each
  under its own brief.
- **What it does.** On development data only, it builds everything between an issued day and the visitor's
  browser that CP-18a left out:
  - the outcomes' reconciliation and the evaluation records;
  - the dated bundle, built and verified;
  - the final-product Space that computes only from that bundle;
  - the publication step, prepared and exercised against a local server only;
  - the Space plan §7 step 6's tests and negative controls.

  Nothing in this round retrieves, reads, issues or displays anything for a delivery day after 2026-09-06.
  Nothing is uploaded to Hugging Face or published.
- Ratified plan anchor: `capstone_v21.md`, revision v21-r19, SHA-256 `acdeeab18a17ecdb83ade83d369a5031f3180f8fdb618a23af5b37836663996e`.
  - **The bar** is quoted below:
    - §19.1–19.8;
    - §16.3, and §16.4's CP-18 row with its paragraphs;
    - §24.12's "Open, for the Owner and for later checkpoints", for its "For CP-18" items and R7;
    - §24.13's "The publication time (decision 22)", for what the Space may say;
    - PUBLISH_RULES 1.5 §7.3 (A9);
    - the Space plan's §4.12 and §7, whose steps 4–6 bind this round.
  - **PUBLISH_RULES** `docs/PUBLISH_RULES.md`, revision 1.5, SHA-256
    `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`.
  - **The Space plan** `docs/track-b/final-product-space-plan-2026-09-30.md`, SHA-256
    `ad3568c8997a08aa291bd3a7f29046c24ce61f0c1fd992622f921b5d23f9174c`. Its §4 (the views) is the design this round
    implements, under A9.
  - **Decision 7** (`docs/track-b/pre-cp-17-rulings-2026-10-25.md`): CP-18's preparation runs "with dry runs on data to
    2026-09-06 only".
- **The frozen policy, which this round runs and never changes:** CP-17c's freeze.
  - its landing record `docs/track-b/cp-17c-landing-2026-10-30.md`;
  - its freeze record and manifest under `docs/track-b/evidence/cp-17c/`, policy identity `720fc581be6206eba8ed303e689e63c09272a189564090a547d93fc9e7db62dc`;
  - **what CP-17 froze for the Space and this round implements, never redefines:**
    - the bundle's seven kinds and its rules (`docs/track-b/evidence/cp-17/payload-schema.md`, `cp17.schema`);
    - §19.5's definitions (`docs/track-b/evidence/cp-17/definitions.md`, `cp17.scoring`);
    - §19.3's τ_eq = 0.01 EUR/MWh and its three statuses (`cp17.retrain`);
    - §19.7's methods (`cp17.attribution`);
    - the browser runners `src/cp17/browser/`;
    - the freeze record's §14, including its F1.
- **CP-18a,** landed: its landing record `docs/track-b/cp-18a-landing-2026-11-04.md` (`09d23bf42ab5494d137675334c6a6d6c56a9e07eca7c3c261c3f15f0a66e2c51`), `land/cp-18a` =
  `65852abd48709785361b19b1bef71a5b44a6e3e8`, `evidence/cp-18a` = `40f481847d372a2211940a18ddbd46b9d98f2377`. Its pipeline `src/cp18/`, its live store and its dry
  runs' issued development days are this round's inputs.
- **The Owner's decisions:**
  - 1–19, bound by CP-17b's and CP-17c's frozen copies;
  - 20–21 in `docs/track-b/owner-decisions-2026-10-29.md`;
  - 22–25 in `docs/track-b/owner-decisions-2026-10-30.md`
    (`1286548362b5618e3fb01c616d673c0af83dd79effeaf102bb9727ac219aabab`);
  - 26–27 in `progress.md` (2026-10-30). Under decision 27, the Orchestrator decides every matter that costs the Owner
    nothing, and logs it for his ratification.
- **The Orchestrator's rulings for this round,** under decision 27:
  - **O13 — the "before final-candidate test" items** (PUBLISH_RULES §14), which §24.12 left for the Owner. They take
    CP-17's proposals as written in `docs/track-b/evidence/cp-17/4-7t-frozen-protocol.md` §12:
    - the badge;
    - the wording;
    - the fresh headline window;
    - the hero-switch rule. A1 is "final candidate · pending 4.7T" until 4.7T is scored. It becomes "live" only at
      CP-18's activation, which requires a passed 4.7T. On a fail, v1 stays the released product.

    This also answers §24.12's question of when A1 replaces v1 as the product: at CP-18's activation, after a
    passed 4.7T.
  - **O14 — §19.3's visitor wording:**
    - CP-17's proposal in `reports/cp17/report.md` ("The reference runtime, and the visitor wording proposed for the
      Owner");
    - plus one sentence that states F1, as §24.12 requires. The issued values were computed in the same WebAssembly
      runtime the visitor runs. At one DST origin of the development period, that runtime's result differed from
      native arithmetic by up to 0.028 EUR/MWh.

    The Lead writes the final sentence, and the return quotes it.

## Orchestrator-reported expected state
- **Branch / commit:** `main` = `origin/main` at the commit that records this brief's issue.
  - It is a direct child of `8bec8b35d3f42b88a9be0e5825471882c8358154`, CP-18a's closure, and changes only `progress.md`.
  - **Between them and CP-18a's landing,** `a1625b1a` is a test-only CI repair (CP-18a's landing record,
    Disclosures).
  - **Tags:**
    - `land/cp-18a` = `65852abd` and `evidence/cp-18a` = `40f48184`, pushed, with every earlier checkpoint's;
    - `evidence/cp-26` = `ca20331`, which is **local-only and never pushed**.
  - **Branches and worktrees:** none besides `main` and the primary checkout.
- **Working tree:** the primary checkout is on `main` and clean apart from ignored material.
  - **The Orchestrator uses it.** Never switch its branch, and never write a tracked file in it. Your only writes
    there are under `.local/artifacts/cp-18b/`, `.local/tmp/cp-18b/`, `.local/tools/` and the worktrees under
    `.local/worktrees/cp-18b/`.
  - **The canonical brief** is `.local/artifacts/cp-18b/issued-brief.md`. Package that file byte for byte.
- **What already exists:**
  - **CP-17c's frozen package** `src/cp17/`. Its check is
    `python -m cp17.tools.refreeze verify docs/track-b/evidence/cp-17c/freeze-manifest.json`, which prints `verified`
    on this machine. Its zip is built by `python -m cp17.tools.bundle`, and its browser runners are
    `src/cp17/browser/`;
  - **CP-18a's pipeline** `src/cp18/`:
    - the live store and its data-only paths;
    - the dry run's material `reports/cp18a/dryrun/`;
    - the table of what later briefs cite, in `reports/cp18a/report.md` §8;
  - **CP-18a's dry runs' issued development days**, 2026-08-31 to 09-05:
    - the downloaded results in `.local/artifacts/cp-18a/downloads/`, including the product repository's run
      41785682146;
    - the stores carried out of them;
  - **the reference bundle** for the freeze origin, delivery 2026-09-06 (`payload-schema.md`, "The reference bundle");
  - **CP-25's recorded data** in `.local/artifacts/cp-25/` and the `evidence/cp-26` extract, read-only;
  - **the boundary guard** `src/cp25/guard.py`. Its boundary stays at 2026-09-06;
  - **the claim layer** `src/delu_forecast/claims.py` and `surfaces.py`, and `tests/test_24_live_namespace_is_walled_off.py`;
  - **v1's Space:** `space-wasm/`, `space/`, `scripts/build_wasm_space.py`, `scripts/build_space.py` and
    `scripts/deploy_space.py`, the History route's source;
  - **the tools:** Pyodide 0.28.0 in `.local/tools/pyodide-0.28.0/`; Playwright 1.63.0 in `.local/tools/playwright/`
    with its browsers in `.local/tools/ms-playwright/`; the official Node.js binary in
    `.local/tools/node-v26.7.0-official/`;
  - **the guards:** the secret guard `scripts/secret_guard.py` and the leak scan `scripts/leak_scan.py`, called from
    `.githooks/`, and the CI workflow `.github/workflows/tests.yml`. Its leak-scan step comes first;
  - **CP-18a's reproduction script** `.local/artifacts/cp-18a/ci-runner.py`, with Git's global configuration hidden;
  - **the Homebrew binary** at `/opt/homebrew/Cellar/node/26.7.0/bin/node`, pinned. It is CP-17b's frozen host and
    stays installed;
  - **GitHub:** `gh` is authenticated as `hrsi56`, with the `repo` and `workflow` scopes.
    - The public `hrsi56/delu-pipeline-dryrun` is CP-18a's scratch repository, which this round may reuse.
    - The public `hrsi56/delu-host-refreeze` and the private `hrsi56/delu-host-probe` stay untouched.
- Verify this yourself before relying on it, and report any material mismatch.

## Observable outcome
CP-18b closes with the following, bound by one fresh Integration-Critic PASS. Nothing under `src/cp17/` or
`src/cp17c/` changes: the frozen package is called, never edited.

1. **The outcomes and the evaluation records.**
   - **Reconcile** each issued day's published prices:
     - per UTC key, with the source, the publication time and any revision;
     - a missing or not-yet-published price is `null`, and its day is pending;
     - development days only, from CP-25's recorded data, never a fresh download.

     Design it as the live pipeline will run it: a later run reconciles the days whose outcomes have since been
     published.
   - **The committed evaluation records** come from `cp17.scoring.evaluate`, per window and per policy: the
     product, and B0 as context.
   - **The three windows never pool (§19.6):**
     - development, static from evidence;
     - 4.7T, empty until it is scored;
     - prospective, empty and "in progress" until CP-19.
   - **The dry runs' issued days, 2026-08-31 to 09-05, are a development rehearsal.** They are labelled so
     everywhere, and are never shown or scored as prospective or as 4.7T.
   - **Name the data-only paths** these records use on `main` (`live/…`), beside CP-18a's.
2. **The dated bundle.**
   - **Build it from the live store:** the seven kinds, exactly as `docs/track-b/evidence/cp-17/payload-schema.md`
     defines them.
     - The manifest names the served identity.
     - Its freshness is `fresh`, `stale` or `failed`, with the as-of day and the latest issued day.
     - A day not issued is shown as not issued, with its cause. Nothing is labelled late or timely (decision 22).
   - **Verify it with `cp17.schema.verify_bundle`,** under R7: a raised error is a refused bundle.
     - Verify it before any publication.
     - Show every rule with a negative control.
   - **The recomputation check gates publication.** Run `scoring.recompute_check` natively before publication. Any
     mismatch blocks that day's publication as a product failure (definitions, "The recomputation check").
   - **The size budget:** the first-visit bytes against the training-window bytes, each measured and disclosed.
     Only the manifest and the day's records load at start (A9, "Loading and network").
3. **The final-product Space,** under A9, from the bundle only. Design it from the Space plan §4. Its source is in a
   new folder, `space-product/`, built by a new script.
   - **Views and order (A9's table):**
     1. the product panel, first, not a tab;
     2. Train it yourself;
     3. Forecast;
     4. Validation;
     5. Reliability;
     6. Explainability;
     7. Features;
     8. Data;
     9. Limitations;
     10. the labelled History route, which is v1's frozen demo as it is.

     Build them as an accessible tab list, with keyboard operation and deep links.
   - **Train it yourself:**
     - runs the frozen package's zip under Pyodide 0.28.0, in a Web Worker;
     - uses the frozen browser runners. If it needs a different runner, it shows that runner bit-identical to the
       frozen one on an issued day in Chromium and WebKit;
     - shows the download size and the reference time with its date before the action;
     - supports cancel, failure and retry;
     - reports `cp17.retrain`'s three statuses, each selection's agreement and the largest difference per quantile;
     - labels the result "your retrained model", never "the forecast";
     - uses O14's wording.
   - **Validation** recomputes the windows in the browser with `cp17.scoring`. Its final "Matches the stored value"
     row shows ✓ or ✗ and both values.
   - **Explainability** and **Features** read `cp17.attribution` from the served fitted artifact, worded as A9 and
     §19.7 require.
   - **Data** shows the shipped series, no later than 2026-09-06 before the final test (§24.2's replacement of
     §19.8's date). It is labelled with its last date.
   - **Limitations** are generated from the claim layer shared with the report and README, through a live claim
     builder that keeps `test_24`'s `live_` wall. There is no hand-written limitation copy.
   - **The states, and what the Space says:**
     - not yet scored, pending, partial, stale, failed, and not issued;
     - "prospective evaluation in progress" until CP-19;
     - O13's badge and hero states;
     - never "X% correct", a confidence percentage, "late" or "timely";
     - no claim that a forecast was published before the auction (§24.13).
   - **Network:** the Space loads its pinned runtime and its own served files only. It verifies the manifest's hashes
     and shows the served identity. A verification failure is a visible failure state.
4. **The publication step, prepared but not run.**
   - **Code that would publish a verified bundle and the Space,** then verify the served identity: the served
     manifest's hashes must equal the intended daily artifact's.
   - **Exercise it against a local static server only.** The Hugging Face upload is CP-18's activation, with the
     Owner's `HF_TOKEN`.
   - **If `daily.yml` gains the bundle step, it is dry-run only,** like CP-18a's, and pushes nothing to GitHub.
5. **The tests (the Space plan §7 step 6, and §16.4's controls):**
   - the extended `test_24`, for the live namespace;
   - the live claim builder;
   - the payload contract tests;
   - **negative controls:**
     - a tampered file is detected;
     - a pending outcome stays unscored;
     - a stale artifact is shown as stale;
     - a mismatched recomputation shows ✗ and blocks publication;
     - a retrain with a changed seed is reported as different;
     - a counterfactual is never labelled issued;
   - **positive controls (§16.4):**
     - altered identities;
     - future-label leakage;
     - stale and failed fits;
     - missing, zero and negative prices;
     - partial and DST days.
6. **The browser acceptance,** locally, in Chromium and WebKit through Playwright 1.63.0 (`.local/tools/`):
   - every view's content against its records;
   - the "Matches the stored value" rows passing on the served bundle;
   - the served identity equal to the intended daily artifact;
   - PUBLISH_RULES §9's matrix for every view and control, at desktop and mobile widths;
   - zero non-local requests, recorded and blocked.

   A6, the public checks, waits for the publication.
7. **What CP-18's activation brief and the publication brief cite,** in the return, in one table:
   - the commands;
   - the bundle's paths and sizes;
   - the Space's build and its first-visit bytes;
   - the publication step;
   - O13's and O14's texts;
   - every Owner-facing presentation item still open, with the Orchestrator's proposed ruling for each. The visual
     approval is one of them.

## Complete authoritative checkpoint bar
Verbatim, extracted by `scripts/bar.py bar … --at 65852abd --quote` from `main` at CP-18a's landing.
(The excerpt is the citation. Any line number is a courtesy and is non-binding.)

**`capstone_v21.md` v21-r19 §19.1** (the file `acdeeab18a17ecdb83ade83d369a5031f3180f8fdb618a23af5b37836663996e`; the section 7 lines, 415 bytes, SHA-256 `4c24cbda3b7899629489187e8b8d656d3d050dae17899add7b0a063afaac4214`):

> ### 19.1 Scope
>
> The Space is the product's interactive tool, under §16.1's single identity for final version,
> product, primary demo and daily policy. It serves only the designated final product; v1's frozen
> demo remains a labelled history route. The Space computes only from the records the daily
> pipeline publishes to it (§19.4). At runtime it fetches nothing from data sources, registries or
> tracking services.

**`capstone_v21.md` v21-r19 §19.2** (the file `acdeeab18a17ecdb83ade83d369a5031f3180f8fdb618a23af5b37836663996e`; the section 6 lines, 335 bytes, SHA-256 `538342106768fedad8201f44bd4aadc3de02415cebf321cd0c1584eca75f6f7c`):

> ### 19.2 One code path
>
> The code that performs the daily fit, issuance and scoring is the code the Space runs in the
> browser for §19.3 and §19.5. No second implementation stands in for the product. A component
> that cannot run in the browser runtime is reported at CP-17 under §19.3's exception route; it is
> never replaced silently.

**`capstone_v21.md` v21-r19 §19.3** (the file `acdeeab18a17ecdb83ade83d369a5031f3180f8fdb618a23af5b37836663996e`; the section 25 lines, 1354 bytes, SHA-256 `5d1f869e153bac43b8f049ee8395b317f48a28e65282109eb107821ef28e582e`):

> ### 19.3 "Train it yourself" is required
>
> The Owner requires an in-browser retraining action for the final product.
>
> 1. **What it does.** In the visitor's browser, it retrains the daily fit of one issued delivery
>    day from that fit's shipped training window, with the same code, seed and selection rules.
>    It then predicts that day's quantiles.
> 2. **What it reports.**
>    - whether every data-driven selection matched the issued artifact;
>    - the largest absolute difference per emitted quantile, in EUR/MWh;
>    - one status that states only what was measured: identical bit for bit, within the frozen
>      tolerance τ_eq, or different.
> 3. **What it never does.** It never replaces, rescores or relabels an issued forecast.
> 4. **The probe.** Before the CP-17 freeze, a feasibility probe on development data measures, for
>    the designated policy:
>    - browser time and memory;
>    - payload sizes;
>    - the deviation from the native fit;
>    - selection agreement.
>
>    CP-17 freezes τ_eq and the reference runtime from that measurement.
> 5. **If the policy cannot meet this requirement** within the measured limits, CP-17 returns a
>    blocker. Only an explicit Owner exception, with its public wording, lets the product ship
>    without the action. The requirement is never dropped silently, and never met by retraining a
>    different implementation.

**`capstone_v21.md` v21-r19 §19.4** (the file `acdeeab18a17ecdb83ade83d369a5031f3180f8fdb618a23af5b37836663996e`; the section 8 lines, 532 bytes, SHA-256 `cf619098a5aaba12728f3e6f912debd4f59c7db0320b11d6db5afd86ce7256a6`):

> ### 19.4 Daily delivery
>
> Each delivery day, the authorized pipeline publishes a dated bundle to the Space: the issued
> forecasts, the issuing artifact and its lineage, the reconciled outcomes and the evaluation
> records. The bundle's manifest lists every served file with its SHA-256. The Space shows the
> served identity and its freshness. A forecast recomputed by a newer fit is never shown or scored
> as issued. Delivery needs the separate operational and publication authority of §16.2 and
> programme 4.9; this section grants none.

**`capstone_v21.md` v21-r19 §19.5** (the file `acdeeab18a17ecdb83ade83d369a5031f3180f8fdb618a23af5b37836663996e`; the section 19 lines, 1170 bytes, SHA-256 `1d47a50558cc7b9a9df1a657b7552a50df728457af6dd3dea8835e3403d7b521`):

> ### 19.5 Definitions frozen at CP-17, before the fresh-data test
>
> CP-17's freeze fixes the following before 4.7T:
>
> - **The percentage measure beside MAE:** its formula; the tolerance, which the Owner sets; the
>   denominator; eligible and partial-day hours; and zero, negative and missing prices.
>   - The proposed form is the share of scored hours within ±τ EUR/MWh.
>   - A figure relative to a benchmark is improvement, not correctness.
> - **Coverage and width** per nominal band, and the rolling window over scored delivery days.
> - **The reliability diagram:** for each emitted quantile level, the observed share of outcomes
>   at or below it, with counts.
> - **The quantile-band PIT:** the share of outcomes between adjacent emitted quantiles, against
>   each band's nominal share.
> - **The recomputation check.** The Space recomputes its evaluation metrics from the shipped
>   issued forecasts and outcomes, and compares them with the committed records.
>   - Counts match exactly; real values match within a frozen tolerance.
>   - A mismatch is shown, and blocks that day's publication as a product failure.
>
> Nothing in this list is chosen after seeing evaluation outcomes.

**`capstone_v21.md` v21-r19 §19.6** (the file `acdeeab18a17ecdb83ade83d369a5031f3180f8fdb618a23af5b37836663996e`; the section 9 lines, 261 bytes, SHA-256 `381833d578424f1bf1b90aed78b832a73827d05baf33e565a86382fabc7995b5`):

> ### 19.6 Evaluation windows
>
> Three windows stay separate and are never pooled:
>
> - development, static, from evidence;
> - the one-shot fresh-data test (4.7T);
> - the prospective record from the run start, "in progress" until CP-19.
>
> v1's holdout stays v1 history.

**`capstone_v21.md` v21-r19 §19.7** (the file `acdeeab18a17ecdb83ade83d369a5031f3180f8fdb618a23af5b37836663996e`; the section 12 lines, 494 bytes, SHA-256 `10060bd2f7315143d9e0a3a6a5529df324b76b9d8a757c87605f17b79148821c`):

> ### 19.7 Attribution and importance
>
> Methods are fixed by component class:
>
> - **a blend:** each component's weight times its forecast, an exact decomposition;
> - **linear components:** coefficient times the centered, standardized input;
> - **tree components:** per-prediction contributions (TreeSHAP), and gain read from the fitted
>   model;
> - **a neural component:** a method frozen at CP-17.
>
> All are presented as attribution within one fitted artifact, never as causality or incremental
> value.

**`capstone_v21.md` v21-r19 §19.8 (its date is 2026-09-06 under §24.2; the supporting extract)** (the file `acdeeab18a17ecdb83ade83d369a5031f3180f8fdb618a23af5b37836663996e`; the section 5 lines, 274 bytes, SHA-256 `6534df682192257f83beeed2116870b6a3e1b8195a85faa5f76d4e1a51dd49fa`):

> ### 19.8 Data displays
>
> Data and feature views compute from the shipped series. Before the final test, no research
> display uses data after 2026-04-07 (standing decision of 2026-09-24). From CP-18, the views run
> through the latest published day, labelled with its last date.

**`capstone_v21.md` v21-r19 §16.3** (the file `acdeeab18a17ecdb83ade83d369a5031f3180f8fdb618a23af5b37836663996e`; the section 30 lines, 2368 bytes, SHA-256 `3bec66a22d7fc86f6dcde441c82328229f94e0d49efe28abf63965ada4568c0e`):

> ### 16.3 What the product and demo expose
>
> The product panel comes first, followed by How the product works, scientific Product results,
> Business insights, How the models compare and all remaining sections in their existing order.
> [PUBLISH_RULES 1.1](docs/PUBLISH_RULES.md) §§5, 5.1a, 7.2 and A8 define presentation acceptance.
> The twelve-subject product coverage follows the actual final policy and its dated artifacts;
> the outgoing product's evidence stays historical. The primary demo uses the same product policy,
> and identifies the artifact/issue date and whether an interaction is a counterfactual scenario.
> An old replay may remain as labelled history, not as a different primary product.
>
> Show today's issued hourly forecasts versus available published outcomes, a defined percentage
> performance measure alongside MAE in EUR/MWh, and tomorrow's issued hourly forecasts and prediction
> intervals. Freeze the percentage formula, denominator, eligible population, scoring window,
> zero/negative-price treatment and any success tolerance before evaluation. A benchmark-relative
> percentage is labelled improvement, not correctness. Missing/pending outcomes are unscored;
> partial-day scores show completeness. Scoring uses the artifact that issued the prediction,
> not a newer fit. Record the price source, publication/revision times and outcome eligibility.
>
> Distinguish nominal prediction-interval level from measured coverage and width on an explicitly
> named past window. Neither means a point price has that percentage probability of being correct.
> Display separate last-training, data-refresh and issuance times, delivery date/timezone,
> freshness and failure state. No data or no evidence means a labelled unavailable state.
>
> Scientific graphics separate development, unused-data and prospective results. Business
> interpretation must separate forecast performance from an evaluated economic decision policy.
> Cumulative net profit/value, returns or business success rates require a frozen use case,
> constraints, costs, benchmark, denominator, complete time series and loss/risk disclosure;
> label simulated versus realized results. Without authorized evaluation, show the specific gap
> and measured forecasting implications. This is no authorization for trading, a new economic
> experiment or a fabricated profitable result; programme §4.E governs such evaluation.

**`capstone_v21.md` v21-r19 §16.4 (its CP-18 row and its paragraphs bind here)** (the file `acdeeab18a17ecdb83ade83d369a5031f3180f8fdb618a23af5b37836663996e`; the section 19 lines, 1777 bytes, SHA-256 `502c1a588c9fe88e557084cff3fe1c44871c8e0c8fbe42a2284650d3a98a73ab`):

> ### 16.4 Delivery and acceptance obligations for future briefs
>
> | Stage | Required addition to the full future checkpoint bar |
> |---|---|
> | Before fresh-data test | Replay the intended daily refit/update and issuance contract; freeze scoring and any evaluated economic policy before outcome access; retain the protected test boundary |
> | CP-17 | Owner's final-version designation, prerequisites/disposition, policy/initialization and registry identities, daily fit and failure rules, metric formulas, resource and calendar plan |
> | CP-18 | Actual scheduled training/issuance and outcome reconciliation, one product/demo identity, complete documentation/results/business sections, daily public panel and independent public acceptance |
> | CP-19 | At least 90 consecutive delivery days after final freeze under §9; count real timely forecasts and failures, verify registry lineage, evaluate without tuning or excluding bad days |
>
> Live observations and the matching demo may be published at authorized CP-18 with the label
> “prospective evaluation in progress”; do not wait for CP-19 to show operation, and do not claim
> completed validation before it. Public acceptance checks actual hosted output and daily records;
> local fixtures do not establish daily operation. Include positive controls for altered identities,
> future-label leakage, stale/failed fits, missing/zero/negative prices and partial/DST days, plus
> reproducible percentage, interval and authorized business-series derivations. The full existing
> independent, browser, accessibility and publication contract still applies.
>
> No checkpoint starts here. The numeric future briefs and approved budgets remain necessary;
> this amendment resolves the required product outcome, not experimental results or implementation.

**`capstone_v21.md` v21-r19 §24.12, "Open, for the Owner and for later checkpoints" (its "For CP-18" items and R7)** (the file `acdeeab18a17ecdb83ade83d369a5031f3180f8fdb618a23af5b37836663996e`; the section 53 lines, 3662 bytes, SHA-256 `9a0d7be68830d512c09ed129fc47590094855e5fdbab2b3c11995f77bbb2702a`):

> #### Open, for the Owner and for later checkpoints
>
> None of these is decided here, except the `schema.py` defect, which R7 accepts:
> - **For the Owner, before 4.7T opens: PUBLISH_RULES §14's "before final-candidate test" items.** These
>   are the badge, the wording, the fresh headline window and the hero-switch rule, and CP-17's protocol
>   §12 proposes them.
>   - They are publication rules, which the Owner ratifies (PUBLISH_RULES §14).
>   - 4.7T's brief cites his ruling.
> - **For the Owner, before CP-18's activation: when A1 replaces v1 as the product.**
>   - Decision 1 reads "v1 stays the product until CP-19".
>   - CP-17's protocol §8 says the same, then adds: "It also stays if 4.7T passes, until CP-18's
>     activation (§16.1)." Its proposed hero-switch rule (§12) reads: "It switches to 'live' only at
>     CP-18's activation, which requires a passed 4.7T."
>   - §16.1 and §19.1 require one identity for the panel, the demo and the daily policy at completed
>     rollout.
>
>   Neither reading governs CP-18's activation until he rules. His ruling can go with the §14 items.
> - **For 4.7T's brief:**
>   - **the §24.2 audit, the Owner's declaration and the retrieval approval;**
>   - **the runtime check, as a precondition.** A window issuance runs only where `refreeze verify`
>     reports no problem and no unchecked file. The command exits 0 in both cases, so the brief reads its
>     output. On CI it reports the issuing host's local files as unchecked, never as passed.
>   - **the window's inputs and payloads.**
>     - `cp17.daily` takes each day's payloads and GFS-availability flag from its caller.
>     - The only payload builder, `cp17.tools.payloads`, is outside the policy identity and refuses days
>       after 2026-09-06.
>     - 4.7T's brief names the code that turns the retrieved data into the frozen payload kinds. That
>       code sets each day's GFS flag under the tier register and the Owner's tier, margin and GFS
>       rulings.
>     - The brief also names how that code is shown equal to the development builder, for example by
>       byte-identical payloads at the nine parity origins, and how the comparators' native runs read the
>       window.
>
>     None of this changes a frozen rule.
> - **For CP-18:**
>   - the unattended pipeline, which calls `cp17.daily` once per delivery day, with its schedule,
>     deadline and late-forecast rule (§24.4);
>   - **where the pipeline runs.** The issuing host is the pinned files above. Any other binary or
>     machine is a runtime change, which needs a new freeze and a new evaluation (§16.2);
>   - publication authority, the MLflow registration of the local names and versions, and the Space's
>     activation;
>   - §19.3's visitor wording, proposed in CP-17's report for the Owner's publication decision. It states
>     F1 as recorded above.
> - **A fail-safe defect in the frozen package, accepted (R7).**
>   - **The defect.** A structurally malformed day in an issued-forecasts record that was also re-hashed
>     in the manifest makes `src/cp17/schema.py` raise an error instead of listing the fault.
>   - **Why it is accepted.** The record is refused either way, so nothing is issued or served from it.
>     A fix changes the package, so it needs a new freeze and a new evaluation (§16.2). Made after 4.7T,
>     a fix would leave 4.7T's result covering a superseded identity.
>   - **What follows.** It is accepted for the frozen policy's life, and fixed at the next freeze. CP-18's
>     pipeline, and the Space wherever it runs `verify_bundle`, treat a raised error as a refused record.
>     The Owner may instead order a re-freeze before 4.7T opens. CP-17b's landing record had listed the
>     defect for CP-18.

**`capstone_v21.md` v21-r19 §24.13, "The publication time (decision 22)" (for what the Space may say)** (the file `acdeeab18a17ecdb83ade83d369a5031f3180f8fdb618a23af5b37836663996e`; the section 39 lines, 2762 bytes, SHA-256 `8b656f9ae608f63ef630fa12f02416f894d99ebd82aa4222d37193af61311f47`):

> #### The publication time (decision 22)
>
> - **The information cutoff is unchanged:** D−1 11:00 Europe/Berlin, strictly before (§24.4).
>   - A run may happen at any time after the cutoff.
>   - Its payload holds only inputs published before the cutoff. So a later run issues the same forecast,
>     under the condition below.
> - **"Before the outcome"** in the frozen rules means without access to D's outcome, under the target-day
>   embargo (§24.4). It does not mean wall-clock time.
> - **Availability is judged by publication time against D's own cutoff, never by the run time.** The
>   tier register and the Owner's tier, margin and GFS rulings (§24.5) apply unchanged. This covers each
>   input and the GFS-availability flag (§24.12, decision 11).
>   - **For the live pipeline, CP-18 makes this verifiable** in one of three ways:
>     - each day's inputs are retrieved and archived by the cutoff;
>     - each input is taken from a source that preserves its vintage;
>     - for an input the tier register admits with reconstructed availability (tier 2), its documented
>       schedule.
>   - **A live day whose inputs cannot be shown this way is not issued,** and its cause is recorded.
>   - **4.7T's window keeps its registered vintage terms** (the protocol's §3, "Vintages").
> - **A delivery day is issued or not issued.** There is no "late" status and no "late" label.
> - **What stays recorded:**
>   - each issuance's actual run time, in its lineage (§16.2);
>   - the date of the last training, which the product's panel states.
> - **No public wording claims** that a forecast was published before the auction, or before its outcome.
> - **What this supersedes:**
>   - **§24.4's sentence** "The live product publishes its forecast before 12:00 local. CP-18 fixes the
>     schedule, its deadline and its failure rule; a late forecast is recorded as late." CP-18 fixes the
>     schedule and the failure rule. There is no deadline.
>   - **§16.2's "numeric origin/deadlines".** CP-18's brief fixes the origin and the cutoff, and no
>     deadline.
>   - **§16.4's CP-19 row,** where "count real timely forecasts and failures" becomes "count issued and
>     not-issued delivery days". CP-19's at least 90 consecutive delivery days count every day, issued or
>     not issued.
> - **§16.2's rule stands:** "Do not ... backfill a late forecast as timely". No forecast is labelled timely.
>   A catch-up issuance carries its own run time and relabels nothing.
> - **`AGENTS.md`'s daily-update exception needs no change.** It reads: "A failed or late day is published
>   as failed or stale, never skipped silently or backfilled as timely." Under this section:
>   - a day that is not issued is shown as not issued;
>   - the panel shows the date of its last training;
>   - nothing is labelled timely.

**`docs/PUBLISH_RULES.md` revision 1.5 §7.3 (A9)** (the file `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`; the section 52 lines, 5064 bytes, SHA-256 `b5ebca7bb691a88615bf21467dec5b85ae29f1bd48dc99dbb292fe0cf3414f5b`):

> ### 7.3 The final-product Space (A9, conditional)
>
> **A9 applies at A8's trigger to the Hugging Face Space and its direct app,** the primary demo of
> the Owner-designated final product. Research anchor §19 fixes what the Space computes and may
> claim; this section fixes how it presents and how it is accepted. The implementation plan is the
> [final-product Space plan](track-b/final-product-space-plan-2026-09-30.md).
>
> The report remains the entry point: static, self-contained and without a runtime. The Space is
> the product's interactive tool. Both show one product identity and derive every number from the
> same records.
>
> **Required views,** in this order. Each is a real view (plan §7.5): an accessible tab list with
> keyboard operation and deep links, not decorative tabs.
>
> | View | Required content | Required wording and states |
> |---|---|---|
> | Product panel (first, not a tab) | §7.2's A7 fields: identity and status; the daily artifact; separate training, refresh and issuance times; cutoff, delivery dates and timezone; today's issued forecast against published prices, with the frozen percentage measure and MAE over named scored hours; tomorrow's issued forecast with nominal bands; measured coverage with width over the named window | "Not yet scored", pending, partial, stale and failed states; "prospective evaluation in progress" until CP-19; no "X% correct" and no confidence percentage |
> | Train it yourself | Research §19.3's action: the retrain of one issued day's fit, selection agreement, largest difference per quantile, the measured status and the visitor's runtime | Extra download size, reference time and its date before the action; only runtime-reported stages; cancel, failure and retry; the result labelled "your retrained model", never "the forecast" |
> | Forecast | Only issued days in the day picker; issued p50 and nominal bands; published outcomes where available | "Issued at … by artifact …"; any what-if control labelled "counterfactual scenario — not an issued forecast" |
> | Validation | Development folds, static from evidence; the one-shot test and the prospective record recomputed in the browser: MAE, pinball, interval score, coverage with width per band, and the similar-day naive labelled as a reference; counts, failures and late issuances | Evidence badges per window; classes never pooled; a final "Matches the stored value" row with ✓ or ✗ and both values |
> | Reliability | A reliability diagram for every emitted quantile level, with counts; rolling coverage with width per band; the quantile-band PIT | The nominal level drawn and named as a reference, not a target; "nominal …; measured coverage … over …"; never "confidence" |
> | Explainability | The selected forecast decomposed by blend component, then by input contribution, in EUR/MWh against a stated baseline | "Contributed … relative to the model's baseline"; never "caused", never incremental value |
> | Features | The selected day's inputs against their training-window distribution; importance read from the fitted artifact, per component | The named artifact and its date; "how much this fitted model relies on each input"; attribution, not causality |
> | Data | Price distribution, negative hours, hourly profile and regimes, from the shipped series | Definitions where used (quarter-hour averaging, the price floor); date range within research §19.8 |
> | Limitations | Generated from the claim layer shared with the report and README | No hand-written limitation copy |
> | History (a labelled route) | v1's frozen demo, replay and identity check | "Historical"; never presented as the product |
>
> **Presentation line.** Plan §7's tokens, typography, panel grammar, components and states apply
> as on the report. That includes direct labels and marker shapes for generation identity, mobile
> chart variants, one primary action per view and no hover-only meaning. Theme switching, animated
> counters, remote fonts and disabled controls for missing features stay out.
>
> **Loading and network.**
>
> - Startup metadata sits beside the primary action (§7.1).
> - Only the manifest and the day's records load at start. Heavier payloads, above all the
>   training window, load on request after their size is shown.
> - The Space loads its pinned runtime and its own served files only: no runtime call to a data
>   source, registry or tracking service.
> - The page verifies the manifest hashes and shows the served identity; a verification failure is
>   a visible failure state.
>
> **Acceptance.** The §9 matrix applies to every view and control, including framework widgets and
> the tab list. The candidate and public checks record:
>
> - every view's content against its records;
> - the "Matches the stored value" rows passing on the served bundle;
> - the served identity equal to the intended daily artifact;
> - negative controls: a tampered file, a pending outcome, a stale artifact, a mismatched
>   recomputation, a retrain reported as different, and a counterfactual never labelled issued.
>
> A6 applies to the public Space. Visual choices remain the Owner's.

**The final-product Space plan `docs/track-b/final-product-space-plan-2026-09-30.md` §4.12** (the file `ad3568c8997a08aa291bd3a7f29046c24ce61f0c1fd992622f921b5d23f9174c`; the section 22 lines, 1510 bytes, SHA-256 `0ed43eefa5d416c77965bb58ece40e4cd6afe01c7618687cedf83097ad00a0f9`):

> ### 4.12 What the daily pipeline delivers to the Space
>
> The Space computes nothing on a schedule and fetches nothing from data sources. Each day, the
> authorized pipeline (§5) publishes a dated bundle:
>
> | Payload | Content | Loaded |
> |---|---|---|
> | Manifest | Every served file with its SHA-256; product and policy identity; daily artifact identity; the three times; freshness state | At start; the page verifies the hashes and shows the served identity |
> | Issued forecasts | Every issued day's hourly quantiles with issue time and issuing artifact | At start |
> | Outcomes | Reconciled published prices with source, publication and revision times | At start |
> | Evaluation records | The committed metric records that the recomputation must match | At start |
> | Fitted artifact | The day's model files (for example LightGBM text, NumPy arrays and coefficients) | For Explainability, Features and Train it yourself |
> | Training window | Inputs and targets of the day's fit window, with the GFS aggregates | Only on "Train it yourself", with its size disclosed first |
> | Series | Hourly prices for the Data view | For Data |
>
> - **Runtime rule:** the Space loads its pinned runtime and its own served files only. There are
>   no runtime calls to ENTSO-E, SMARD, GFS, the registry or MLflow. The report's
>   no-runtime-network rule is unchanged.
> - **Licensing:** CC BY 4.0 data and GFS-derived aggregates may be redistributed with attribution
>   (`DATA-LICENSE.md`). No raw GRIB and no credentials are shipped.
>
> ---

**The final-product Space plan §7 (steps 4–6 bind this round)** (the file `ad3568c8997a08aa291bd3a7f29046c24ce61f0c1fd992622f921b5d23f9174c`; the section 50 lines, 2648 bytes, SHA-256 `e753f5d23807d7d6ba33669471957f4fa8811f0dfe6eb529c9fc02f83e6a8f0b`):

> ## 7. Automatic execution at the final-product rollout
>
> Nothing here needs a new decision later, beyond §5.1's open items. The anchors make the Space a
> required part of the final product's rollout: research §16 and §19 bind CP-17 and CP-18, and
> publication A8 and A9 bind the release. Every future brief pins both.
>
> **The checklist the CP-17 and CP-18 briefs carry:**
>
> 1. **Designation (Owner).** Record the final version. Its evidence class and product identity
>    drive every Space label.
> 2. **Feasibility probe (CP-17, before the freeze).** Train one delivery day of the designated
>    policy under Pyodide in Chromium and WebKit, on development data only. Measure:
>    - time and peak memory;
>    - the first-visit and training-payload sizes;
>    - the deviation from the native fit, bitwise or not;
>    - whether the selections match.
>
>    If this is infeasible, return a blocker for the Owner's §19.3 decision. This can also run
>    earlier, as a bounded probe with its own brief, to de-risk the button.
> 3. **Freeze (CP-17):**
>    - τ (Owner), the percentage formula, denominator and partial-day rule, and zero or negative
>      handling;
>    - the rolling window lengths, the PIT and diagram definitions, and the recomputation
>      tolerance;
>    - τ_eq (Owner) and the reference browser and runtime;
>    - the attribution method for any neural component;
>    - the payload schema and manifest.
> 4. **Daily pipeline (CP-18):**
>    - acquire, validate, fit and issue before the gate;
>    - build the dated bundle and verify it (hashes, schema, recomputation rows);
>    - publish it to the Space and verify the served identity;
>    - reconcile outcomes later and update the records.
>
>    Failures and staleness stay visible, and every delivery day is covered, including DST days. This needs the Owner's `AGENTS.md` authority first.
> 5. **Space build (CP-18):** §4's views under A9, from the payload only, with the History route
>    for v1.
> 6. **Tests (CP-18):**
>    - an extended `test_24` (the live namespace);
>    - a live claim builder;
>    - payload contract tests;
>    - negative controls: a tampered file is detected; a pending outcome stays unscored; a stale
>      artifact is shown as stale; a mismatched recomputation shows ✗ and blocks publication; a
>      retrain with a changed seed is reported as different; a counterfactual is never labelled
>      issued.
> 7. **Review and release:** the independent exact-candidate review; the packet with §5d and A9
>    rows; the Owner-authorized launch; public A6 checks of every view.
> 8. **Operation:** "prospective evaluation in progress" until CP-19 closes after at least 90
>    consecutive delivery days.
>
> ---

**Further items,** which bind this candidate as well:

1. **Blind.** The boundary stays at 2026-09-06. No byte dated after it is downloaded, read, displayed or inferred. No
   4.7T forecast and no live forecast is produced.
2. **GitHub-landable as is.** No committed file is over 50 MB. The Space's runtime files (Pyodide's 23 files, the
   package zip) are retrieved or rebuilt by hash at build time, not committed, unless the return shows why one must
   be.
3. **CI-ready.**
   - The workflow's steps are green on a history-free single-commit copy, with `CI=true` and Python 3.12, and with
     Git's global configuration hidden as on a GitHub runner. Copy CP-18a's `ci-runner.py`: its `GIT_CONFIG_GLOBAL`
     points at a file holding only `[user] useConfigOnly = true`.
   - `pytest -m stress` passes locally.
   - **Every test that commits sets its own Git identity.**
   - **A byte-equality test that depends on the issuing host's platform** (darwin-arm64) skips elsewhere, with the
     reason. GitHub's ubuntu CI found two such gaps in CP-18a, after its landing.
   - No test depends on branch history, tags or local-only inputs. Tests over local-only material skip with a stated
     reason when it is absent.
4. **What never changes:**
   - `src/cp17/` and `src/cp17c/`, and every checkpoint's reports and evidence;
   - CP-18a's modules in `src/cp18/`, except where this round's code hooks into a run. Each such change is named in
     the return;
   - the landed code in `src/delu_forecast/`, `src/cp15/` to `src/cp28/`, `src/cp17probe/` and `src/cp17cprobe/`.
     New modules may import it;
   - v1's Space source (`space-wasm/`, `space/`) and its build scripts. The History route serves v1's build as it is;
   - the report `docs/index.html`, the README and every published surface;
   - `data/`, `reports/development-inputs/`, the root `pyproject.toml` and `uv.lock`;
   - the anchors and amendment records, the decisions records, `AGENTS.md`, the role files, the exposure ledger and
     the backup register.

   Before editing any tracked file, check that no earlier evidence binds its bytes. That includes
   `src/cp26/harness.py`'s `PINS` and every freeze manifest's governance pins. `refreeze verify` on CP-17c's manifest
   prints `verified` at the final candidate.
5. **The Integration Critic** reruns, locally:
   - the suite in the history-free `CI=true` Python 3.12 sequence, with Git's global configuration hidden, and
     `pytest -m stress`;
   - one bundle built from the dry runs' store and verified;
   - every negative control;
   - the Space in Chromium and WebKit, served locally, with one "Train it yourself" run to its status;
   - the recomputation row on the served bundle.

## Task-specific supporting extract
- **§24.2 replaces §19.8's date:** "no research display uses data after 2026-04-07 before the final test" becomes
  2026-09-06 (`capstone_v21.md` §24.1's table and §24.2). PUBLISH_RULES 1.5's invariant 10 moved with it.
- **The public scratch repository** `hrsi56/delu-pipeline-dryrun` (CP-18a's) may take further dry runs of the
  pipeline with the bundle step.
  - Before every push, run the value-based secret scan over everything outgoing (`scripts/secret_guard.py` and
    `scripts/leak_scan.py`, via the hooks).
  - It holds no data dated after 2026-09-06, no secret and no variable, and no Pages.
- **Retrieval, authorized for software only:**
  - Pyodide 0.28.0's files, verified against CP-17c's hashes;
  - **on the runners:** what CP-18a's workflow retrieves.

  Playwright 1.63.0 and its browsers are already in `.local/tools/`. Record each URL, version, size and SHA-256. Make
  no other network contact, and no data retrieval.
- **The ceilings:**
  - **Local:** 12 machine-hours, summed over workers' wall time. At most 4 concurrent workers, BLAS 1 for native fits,
    CPU only, peak memory 12 GB, no GPU.
  - **GitHub:** standard hosted runners in the public scratch repository only. At most 5 job-hours in all, and each
    job's `timeout-minutes` set.
  - Keep a ledger, and stop before a ceiling.
- **Presentation.** Visual choices remain the Owner's (A9). Build to PUBLISH_RULES §7's tokens and components, and
  record what the Owner will see in the return. Do not hold the round for visual taste.

## Applicable constraints
- **The red line (§24.2).** No delivery day after 2026-09-06 is read, recorded, displayed or mentioned, except as a
  protocol or calendar date.
- **Homebrew's `node` stays pinned and installed.** Never upgrade, unpin or remove it.
- **Credentials** follow `AGENTS.md` § Credentials.
  - No real credential is needed in this round, and no secret is created anywhere.
  - Never print, log or echo an environment variable's value.
  - Export `MLFLOW_DISABLE_TELEMETRY=true` and `DO_NOT_TRACK=1`.
- **Allowed paths:**
  - `src/cp18/` (new modules, and the named hooks into CP-18a's), `tests/cp18b/`, `reports/cp18b/` and
    `docs/track-b/evidence/cp-18b/`;
  - `space-product/` (new) and its build script under `scripts/` (new);
  - `tests/test_24_live_namespace_is_walled_off.py` (its extension only);
  - `.github/workflows/daily.yml` (the bundle step, dry-run only).

  Nothing under `src/cp17/` or `src/cp17c/`, and no anchor, governance or published file.
- **Long computation** may run unattended in the background, within the ceilings, under your ledger. Commit work in
  progress on `gauntlet/cp-18b` at every stage boundary.
- **Tools:**
  1. run `scripts/gauntlet.py start cp-18b` first, from the primary checkout;
  2. create the worktree with
     `git -C /Users/djourno/Downloads/PJM worktree add -b gauntlet/cp-18b .local/worktrees/cp-18b/lead main`;
  3. run one Critic, through `critic-open`, `critic-brief` and `critic-close`. **The first line of the Critic's
     launch assignment** forbids opening the Claude memory directory;
  4. check the return with `scripts/gauntlet.py return`.
- **Memory:** do not open or edit the files in the Claude memory directory
  (`~/.claude/projects/-Users-djourno-Downloads-PJM/memory/`).
- **Owner-facing Git commands** must be non-interactive.

## Timebox
About 24 active hours from orientation to the terminal return.

## Owner-only actions already authorized
- **CP-18b's execution** under decisions 7, 25, 26 and 27 and this brief. The Orchestrator delivers this brief under
  the Owner's grant, and that delivery is the grant. It covers:
  - pushing to the public scratch repository `hrsi56/delu-pipeline-dryrun` and running its workflows, within the
    GitHub ceiling;
  - the software retrievals above, and the local ceiling;
  - local `gauntlet/cp-18b` commits and the brief's packaging.
- **Nothing else:**
  - no push, branch or tag on `origin`;
  - no Hugging Face upload and no Space deployment;
  - no secret;
  - no data retrieval;
  - no 4.7T run;
  - no boundary move;
  - no anchor, governance or published-surface edit;
  - no publication;
  - no mainline operation.

## Stop and return
- **First commit.** The first commit copies the canonical brief byte for byte to
  `docs/track-b/evidence/cp-18b/issued-brief.md`.
- **Questions.** If the brief is unclear or wrong, ask the Orchestrator before repository work, or stop at the
  conflict. The anchor, PUBLISH_RULES and the Owner's decisions prevail over this brief.
- **The return.** Return exactly one of PASS / BLOCKED / INCOMPLETE, using templates §3, with both terminal SHAs and
  the verdict-only delta, checked with `scripts/gauntlet.py return`.
  - **Its "Open risk or exact owner action" section** gives item 7's table.
  - Name the job-hours used.
  - Name any exposure (§24.2), and any interview-answer trigger, in one line each.
- **Do not** open 4.7T, upload or deploy anything, or activate anything. Leave your worktree and branch for the LAND.
