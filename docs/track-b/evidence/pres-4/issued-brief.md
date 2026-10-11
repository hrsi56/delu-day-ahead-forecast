# Track B Checkpoint Brief — PRES-4 (publication of v5, with CP-22 and CP-23 as branch cards)

*Issued by the Orchestrator on 2026-10-11 (Sunday), Asia/Jerusalem.*

## Target
- Repository: DE-LU day-ahead forecasting, `/Users/djourno/Downloads/PJM` (origin
  `hrsi56/delu-day-ahead-forecast`).
- Authorized checkpoint: PRES-4, exactly one. It does four things:
  - publishes CP-24's adopted generation, v5, on the research surfaces: the report (Pages), the
    README and MLflow;
  - publishes CP-22 and CP-23 as branch cards, "tested, not adopted";
  - corrects the public planned-work list;
  - leaves the Space unchanged. By the Owner's decision of 2026-10-11 it keeps serving the released
    v1 demo until the final product's freeze.

  This is presentation work only. It reopens no checkpoint or publication, and starts no research
  checkpoint, final-product designation or Live.
- **The name.** "PRES-4" was earlier reserved for CP-22's replacement plan
  (`docs/track-b/cp-22-publication-plan-2026-10-01.md`), which never ran. That plan is not an input.
- Ratified plan anchor: the publication anchor `docs/PUBLISH_RULES.md`, revision 1.4, SHA-256
  `ccfe6199535dc104250ee1ed1d8ff57bf0b12fbfb4945a3521e2e29fad479a80`.
  - It incorporates Publication Standard v1
    (`7bb90c4cbd15bde42121d615bd850854610a1aa0b3a776190a58ef481abeb68c`) and the presentation plan
    (`b04a0bb1af171545ad74b5a91cf96d67b53e5322a0b5394c58cbbb0ca6ace19c`).
  - Apply its precedence and amendments A1–A6 and A11.
  - Record as not applicable, with the reason:
    - A7, A8 and A9: there is no final-product designation, rollout or live panel;
    - A10: no adopted generation is revised in place; v5 is a new generation.
- **Research constraint anchor, read-only:** `capstone_v21.md` v21-r12, SHA-256
  `caf03d705a785369972b6e9ef3d043815a4a7ba77830cabb51e939c486477ce4`.
  - **§23.12** governs CP-24's packet and MLflow.
    - CP-24 ran under v21-r11, whose exact bytes are at `evidence/cp-24:capstone_v21.md`
      (`11068e3f57bd9277be50db62d109f3e7d8ea7b8fdfa042886ccc4ae5ab1ed2d2`).
    - §23.12 pins PUBLISH_RULES 1.3 for CP-24's own packet. This block publishes under 1.4, which
      adds only A11, work availability.
  - **§23.12's three Owner decisions,** made on 2026-10-11:
    - v5's encoding (Task-specific extract, step 5);
    - the not-adopted branches are published;
    - automation items 6 and 7 are built, at `bfadb39`.
  - **§20.13 and §21.9:** the Owner decided on 2026-10-11 to publish CP-22's and CP-23's branches.
  - **§16 and §19,** the final product and its Space, are not triggered.

  This brief activates no research checkpoint.
- **Execution inputs.** Verify each hash before relying on it:

  | Input | Path | SHA-256 |
  |---|---|---|
  | CP-24's publication packet | `docs/track-b/evidence/cp-24/publication-packet.md` | `627291073d99363ad09baa413307e7b62db64ef1f7223974b4da5ab658c7b6be` |
  | CP-24's draft registry | `reports/ddnn2/draft-registry.json` | `7d25bdcaa7b19c387830e0d4df87d1e0c6101be0a48ad0be634b0ab92b8970ee` |
  | CP-24's claim map | `docs/track-b/research-content/cp24-claims.md` | `918a71f269b4d2e24a7bdb107825aa1476cf32e2adaa04e80e5d506dd5f3f774` |
  | CP-24's draft export | `reports/ddnn2/mlflow-export-draft/cp24.json` | `ead221fbdccfdd1ce589c0844493e46d981fc96249d347fdf823afa6fd62ce21` |
  | The CP-24 landing record, v5's adoption source | `docs/track-b/cp-24-landing-2026-10-11.md` | `4b37b337bd27336209623fbcae88bbefd60f1c8a5d6fa939c34437c4bd7f6ca4` |
  | CP-24's return | `docs/track-b/evidence/cp-24/checkpoint-return.md` | `b1dd661553f4bdbe0fdef29e26ebdf12f0001924bb12c32ad48b987c3e64212a` |
  | CP-24's verdict | `docs/track-b/evidence/cp-24/integration.md` | `b112a2ca8bf00ee0316f7036110e29e534f812ed435cd8fde7b02be8e541304a` |
  | CP-22's publication packet | `docs/track-b/evidence/cp-22/publication-packet.md` | `f05dfb8684abeca76f21e77876fe1a78a8c64fa6f96125ee953336a51e4c3219` |
  | CP-22's claim map | `docs/track-b/research-content/cp22-claims.md` | `a9deb40982550d19535cad0d11e91b77eabe96d8a8f48d3c81fa11347e3c0a62` |
  | The CP-22 landing record | `docs/track-b/cp-22-landing-2026-10-04.md` | `a999acb7586d44886dbabd63ea246d7e5c8068ead91880c20a124a6217a2b600` |
  | CP-23's publication packet | `docs/track-b/evidence/cp-23/publication-packet.md` | `e0eba4419d9b60f8ddfdf1523a48798db3edb77b657f31b5307e236500a5ce49` |
  | CP-23's claim map | `docs/track-b/research-content/cp23-claims.md` | `5c12f47b7de9b279df9f5bb31344156a1461c37d873a2425034c9d2ea040a172` |
  | The CP-23 landing record | `docs/track-b/cp-23-landing-2026-10-04.md` | `a860780a872f9dfb4a54a5ee542ad0f86f22ac92a412d6adffaa34617d3a227d` |
  | The publication runbook | `docs/track-b/publication-runbook.md` | `0f92b92b69572b142a2f5091a7d8737ed6c1f90a7f8beed35a292d297f0af3e9` |
  | The packet template | `docs/track-b/publication-packet-template.md` | `4049c3e1f695034ec45fa185d465fce05ab1183cbded72188306579d7287d01a` |
  | The publication advisory log | `docs/track-b/publication-advisory-log.md` | `e6b23215d14dcf09ef0f9de6104027d7e4591a44f02bf37f834b96bf654098ca` |
  | The Owner's programme plan, stage 2 as scope | `docs/track-b/programme-plan-2026-10-11.md` | `3063697d1b266e037bea7464e99bf72be8530c5bd5c8e5748db1c73ac1dcc830` |

  - CP-22's and CP-23's draft registries and draft exports are
    `reports/v4-revision/draft-registry.json` with `mlflow-export-draft/cp22.json`, and
    `reports/distribution-challenger/draft-registry.json` with `mlflow-export-draft/cp23.json`.
    Their landed bytes are bound by `evidence/cp-22` and `evidence/cp-23`.
  - The programme plan is scope, not authority, and its other stages are not this block's.

## Orchestrator-reported expected state
- **Branch / commit:**
  - `main` = `origin/main` = `bfadb39e1e974b951fd9eade2ac0363be0d7c795`. Its last commits are:
    - `bfadb39`, the publication tools;
    - `633afae`, the programme plan;
    - `ec33d07`, the lock-price notes;
    - `a264ef1`, CP-24's closure;
    - `05e6015` = `land/cp-24`.
  - `main` may instead be one direct child of `bfadb39` that changes only `progress.md`: the
    Orchestrator's record of this issue.
  - **The evidence tags:**
    - `evidence/cp-24` = `05b7e618de8de2f3f59c3e62aaf1664807bf397e`, committed
      2026-10-10 23:21 +0300;
    - `evidence/cp-23` = `928bc1389627499fba14222e552feb62492f6e2d`;
    - `evidence/cp-22` = `8daf7d0775404611e9f7ef4844fc602f1aa67b26`.
  - **Topology:**
    - locally, `main` only, with no `gauntlet/*` branch, no worktree besides the primary checkout
      and no stash;
    - on `origin`, the branch `main` and every `land/*`, `evidence/*` and `archive/*` tag.
  - **The secret guard:** `core.hooksPath` is `/Users/djourno/Downloads/PJM/.githooks`.
- **Working tree:**
  - The primary checkout may carry one uncommitted Orchestrator change, `progress.md`. It is not
    PRES-4's: leave it untouched, and do not read it (`AGENTS.md` role router).
  - Your ignored folder `.local/artifacts/pres-4/` holds this brief's canonical copy,
    `issued-brief.md`.
- **What already exists:**
  - **CP-24's committed evidence,** under `reports/ddnn2/` and `docs/track-b/evidence/cp-24/`.
    - It includes `attempt-1/ratio-intervals.csv`: the ratio intervals at the 97.5% decision level
      as well as at 95%.
    - It includes the full-coverage leakage controls, `attempt-1/leakage-controls.json`.
  - **CP-22's and CP-23's committed evidence,** under `reports/v4-revision/` and
    `reports/distribution-challenger/`.
  - **The local MLflow stores** `.local/mlruns/cp22`, `cp23` and `cp24`.
  - **The published export set** `reports/presentation/mlflow-export/`: 28 runs in
    `delu-generations`, under parents `cp10`, `cp15`, `cp16`, `cp20` and `cp21`.
  - **The reviewed Space bundle the Space serves,** copied at
    `.local/artifacts/pres-3/space-wasm-9028a118/`
    (`9028a11869a378ea5c3401a00ad46368e1c9e2f2f9f8732330d32b71af081585`).
  - **The publication tools,** new at `bfadb39`:
    - `scripts/prerelease.py` (`make prerelease`), the runbook §9 offline checks;
    - `scripts/publication_receipt.py`, the post-deploy receipt.
- **Public state.** The Orchestrator read it anonymously with `scripts/publication_receipt.py` on
  2026-10-10 at 23:17 UTC:
  - **GitHub Pages:** HTTP 200, 1,907,718 bytes, SHA-256
    `8a1fedd8bc6bf89d1db170b3fb83df34255e4c350c22113d1df52088c25c8c39`, equal to
    `docs/index.html` at `main`.
    - It shows v4 as the research headline.
    - Its planned list still carries "4.6 · DDNN".
  - **The Space** `Yarden-Viktor/delu-day-ahead-forecast`: public, static, at revision
    `0331088725fedab2f5a1ec804ae03bf960cf126f`.
    - Its file tree equals the `9028a118…` bundle, file by file.
    - Its served page equals the bundle's `index.html` once Hugging Face's injected
      `window.huggingface` script is removed.
  - **MLflow on DagsHub** (`delu-generations`): 28 of 28 runs found. No `cp22`, `cp23` or `cp24`
    run is public.
  - **The link check failed** on about 20 GitHub `blob` pages. GitHub was returning 503 to
    anonymous requests from this machine after two link runs within the hour, while its status page
    read operational.
- Verify all of this yourself before relying on it, and report any material mismatch.

## Observable outcome
v5 is published on the research surfaces, completely or not at all. When this checkpoint closes,
after the Owner's post-return steps:

- **The registry.**
  - It names v5 **"v5 · DDNN-2 added"**. The Owner chose this name on 2026-10-11; it replaces the
    draft's "v5 · DDNN-2 member added" everywhere.
  - v5 is adopted in research on 2026-10-11, with the CP-24 landing record as its source.
  - v4 is both v5's predecessor and its comparator.
  - DDNN-2 alone and v3 + DDNN-2 are study arms, never eligible and not adopted.
- **The headline and opening.** The research headline moves to v5 through the registry. It names
  its metrics (A1) and leads with the pre-specified verdict. The opening pairs research v5 with
  released v1.
- **The chapter.** A v5 chapter, and the A3 transition "From v4 to v5: adding a distributional
  neural network". Visible in them, every value derived from committed rows and none typed:
  - the verdict, with both ratio intervals: at 95%, and at 97.5%, the decision level of §23.8;
  - **the coverage limits, stated plainly:**
    - the number of scored days, and their share of the days in the data, naming the denominator;
    - that no scored day falls in October to December;
    - that the scored days hold one winter;
  - **DDNN-2 alone,** descriptive and never eligible, exactly as the claim map reads it;
  - **the full-coverage leakage controls,** as the claim map reads them;
  - **the evidence class:** the second DDNN decision on the same five folds, post-selection
    development evidence, with 4.7T carrying the protection.
- **The branch cards** (runbook §3), brief and point by point:
  - CP-22, "Pooled LightGBM member for v4", and CP-23, "DDNN member on v4", each with:
    - its question and comparator;
    - its deciding result;
    - a dated "not adopted" status with a one-line reason, from its draft registry entry and
      claim map.
  - Their study arms are study-arm entries.
  - Where the comparison chart can show a branch's candidate on the same population as v5 and v4,
    it is added as a study point, derived and not typed. Where it cannot, the reason is recorded.
- **The planned-work list follows the Owner's programme plan of 2026-10-11, at item level:**
  - **4.6 leaves the list.** It is now the v5 chapter and CP-23's card.
  - **Add a re-evaluation on every eligible day.**
  - **Add new input data:** fuel and carbon prices, neighbouring markets, and earlier forecasts
    that already cover the delivery day.
  - **Make the wind and solar item source-neutral.** It drops "in-house", since an external
    forecast may replace building one.
  - **4.8 and "4.7T and live" keep their content.**
  - The items stay unscored and unnumbered, and commit to no design that no anchor fixes. The
    section's comparator follows the registry.
- **Derived surfaces.** The README follows from the registry.
- **The Space is unchanged.**
  - Its bundle stays `9028a118…`, both generated Space cards stay byte-identical, and the demo
    still runs the released v1. The bitwise-equivalence gate passes.
  - If the registry change would alter a card or the bundle, return BLOCKED with the diff. The
    Space is not redeployed in PRES-4.
- **MLflow.**
  - `cp24`, `cp22` and `cp23`, each with its children, are uploaded under the authority below,
    then verified, routed and indexed, all before the final build. The routes are `experiment`,
    `compare:v5` and each branch's `compare:<id>`.
  - The experiment description names every parent (A-PRES3-1).
- **Review.** The independent check passes at the candidate, and a focused recheck passes at the
  final SHA.
- **The owner packet.** Packet §8 names the exact payloads and ready-to-run commands for the
  remaining steps: the landing, the push, and the public post-deployment checks, including
  `scripts/publication_receipt.py`.

The publication is complete only after those steps and their public evidence. A local PASS is not
a deployed publication.

## Complete authoritative checkpoint bar
- **PUBLISH_RULES 1.4 in full.** Every applicable clause, including the incorporated baseline,
  A1–A6, A11 and §13's acceptance record. Record A7–A10 as not applicable, with the reason.
- **The runbook:**
  - §2, all touchpoints, with "What follows without an edit" and "Limits to watch";
  - §3, touchpoints 1–5, for each of CP-22 and CP-23;
  - §1, §1a, §8 and §9.
- **The packet template, every section.**
  - Complete CP-24's packet into PRES-4's, with CP-22's and CP-23's branch entries.
  - Fill §8 for every surface, with the Space recorded as verified unchanged.
- **The programme plan's stage 2, as scope:** the Owner's decisions and the two risks.
- **Critic and return:** `docs/track-b/gauntlet-templates.md` §§2–3. This is not a research
  checklist, and it authorizes no fit.

Map every applicable item to evidence. The extract below does not narrow this bar.

## Task-specific supporting extract
1. **Registry** (runbook §2 steps 1–6, and §3).
   - **v5's entries.** Enter packet §2's draft entries for v5 and its study arms as drafted, with
     two changes:
     - v5's name is the Owner's;
     - the statuses are dated 2026-10-11 and sourced from the CP-24 landing record.
   - **The draft's code additions to existing entries.** Add them unless an addition would change
     a previously published MLflow record. In that case leave it out, and record it in the packet
     and the return.
   - **CP-22 and CP-23** enter as kind `branch`, from their draft registries, each with its study
     arms.
   - **The lists:**
     - `CHECKPOINTS` gains CP-24, CP-22 and CP-23, each with its run key, evidence tag and SHA,
       report, verdict, landing record and children;
     - `EVIDENCE_TAGS` gains `evidence/cp-22`, `evidence/cp-23` and `evidence/cp-24`, with each
       tip's commit date;
     - `RULES` gains CP-22's rules (set 2026-10-01), `cp23-adoption` (set 2026-10-04) and
       `cp24-adoption` (set 2026-10-05);
     - `COMPARISON_ORDER` puts v5 first.
2. **Evidence** (steps 7–10). Pin the committed rows by blob, and derive every value, typing none:
   - the verdict, the distance from v4, and N = 1;
   - the ratio intervals at 95% and at 97.5%, from CP-24's own draws (`ratio-intervals.csv`,
     `uncertainty.csv`);
   - per-period MAE, with fold 3 as the stress period;
   - the coverage counts, from the committed population and fold dates.
3. **Claims and slots** (steps 11–12a).
   - Register the claim maps, and the `v5.*` and `transition.v4-v5.*` blocks from packet §5 and
     §5a.
   - Add a slot for the coverage limits.
   - Register the `branch.<id>.question`, `.result` and `.reason` blocks for CP-22 and CP-23.
   - Withheld claims stay withheld.
4. **Chapter and charts** (steps 13–15).
   - Write a `v5_slots` builder, modelled on `v4_slots`, and register it in `chapter_sequence`.
     Its detail headings feed A5's routes.
   - The branch cards come from `branch_card` and `lineage`.
   - Add the charts the MLflow runs carry.
5. **Encoding** (step 16). The Owner decided it on 2026-10-11: **rose `#BE123C`, a filled
   pentagon, and the direct label "v5".**
   - Add the pentagon to `marker()`.
   - `marker_problems` must still prove that every generation's shape is its own.
   - No further Owner input is needed.
6. **Planned work.** Correct `scripts/build_pages.py::PLANNED_WORK` to the Observable outcome and
   regenerate. Bind the correction with a regression test and a negative control over every
   generated surface that carries it.
7. **Export and tests** (steps 17–18).
   - **The export specifications:** add CP-24's, CP-22's and CP-23's to
     `scripts/mlflow_export.py::CHECKPOINTS`.
   - **`cp24.json`** must equal its draft except for packet §6's pending fields and the name
     fields the Owner's name changes.
   - **`cp22.json` and `cp23.json`** must equal their drafts except for their pending fields.
   - **No previously published record may change:** run `--diff-against` the published set, and
     `--check`.
   - **A-PRES3-1:** `EXPERIMENT_NOTE_CHECKPOINTS` names every parent.
   - **The frozen-file treatment.** `scripts/mlflow_export.py` is bound by CP-22's and CP-23's
     saved-evidence and draft-export tests.
     - Record each change in those tests exactly as PRES-3 recorded it for CP-21
       (`tests/cp21/test_saved_evidence.py::AMENDED_BY_PUBLICATION`).
     - CP-24's draft-export test skips by design once the file changes.
     - No artifact manifest is edited.
   - **Tests:** add re-derivation tests with negative controls, and extend
     `tests/test_43_publish_rules_migration.py` with the v5 transition.
8. **Space.** Unchanged, as the Observable outcome states. Prove it:
   - the regenerated cards are byte-identical;
   - the bundle hash is unchanged;
   - the bitwise-equivalence gate passes.
9. **Limits.**
   - **A2's placement bounds,** measured in Chrome and WebKit.
   - **The 2.0 MB page budget.** The page is 1,907,718 bytes now. The Owner decided on 2026-10-11
     that there is no compaction: the v2 and v3 sections are not edited. If v5 and the two branch
     cards would breach the budget, return BLOCKED with the measured size.
   - **Chart text** of at least 12 px at every width.
10. **Advisories.** Give each a one-line disposition in the advisory log:
    - A-PRES3-1 is taken up here;
    - A-PRES3-7 is deferred to the final product's Space deployment, since the Space is unchanged;
    - A-PRES3-5 is deferred, since it needs a Lockdown suspension.

## Applicable constraints
- **No research.** $0 external spend. No research rerun, fit, new score, bootstrap, data
  retrieval or typed number.
  - Nothing dated after 2026-04-07 is read, scored or shown.
  - CP-24's reference passes are exhausted at 3/3, as are CP-21's.
- **The product is unchanged.**
  - No change to the released product, the demo, the product documentation (A4) or the release
    rule; v1 stays released.
  - No promotion, final-product designation, CP-17 freeze, Live or daily operation.
- **History is preserved.**
  - Keep every historical chapter, archive, adverse fact, prior review and published MLflow
    record. The v2 and v3 sections are untouched.
  - PRES-1 to PRES-3 are not regraded.
- **Generated files are regenerated from their sources** (`scripts/rebuild_presentation.py`),
  never hand-edited.
- **Not edit targets:**
  - `main` and `progress.md`;
  - the whole locked set of `AGENTS.md`'s Governance Lockdown: the rulebook, every ratified anchor
    including `capstone_v21.md` and `docs/PUBLISH_RULES.md`, the amendment records and
    `.claude/**`;
  - the runbook and the packet template, which are pinned inputs;
  - every checkpoint's artifact manifest and evidence.

  Earlier checkpoints' code changes only at the publication touchpoints named above and in the
  runbook. No Lockdown suspension is active. If a change to a locked file is genuinely necessary,
  halt and return BLOCKED, naming the file and the exact text.
- **Paths.**
  - Temporary worktrees, tools, caches and screenshots go under `.local/`.
  - Durable evidence goes under `docs/track-b/evidence/pres-4/` and
    `reports/presentation/release-checks/pres-4-*`.
  - Code and tests go in their normal paths.
- **Credentials** follow `AGENTS.md` § Credentials.
  - Consume stored variables only inside the process that needs them. Never print, type or log a
    value. Anonymous reads stay anonymous.
  - Before anything imports MLflow, including the test suite, export
    `MLFLOW_DISABLE_TELEMETRY=true` and `DO_NOT_TRACK=true`.
  - The secret guard is mandatory; never use `--no-verify`.
  - Before any commit that carries logs or evidence, scan the outgoing content for the actual
    values of the stored credentials, in a script that never prints them.
- **Work availability:** `AGENTS.md` § Work availability applies; there is no calendar pause.

## Reviews and evidence
- **Before the independent check, run the runbook §9 checks:**
  - **The offline checks:** `make prerelease`, which is `scripts/prerelease.py` at
    `--stage pre-final`, from a clean tree. It covers the tests on Python 3.13 and a clean 3.12 run
    of every CI step, `make verify`, `make lint-publication`, determinism, links and the guard.
  - **The browser checks** with `scripts/check_reader_paths.py`:
    - Chrome and WebKit at every width, with accessibility, keyboard, touch, contrast, requests and
      the placements;
    - A5 discovery, and the demo's controls.
  - **GitHub's 503s.** GitHub may return 503 to anonymous link checks after a burst. Keep the first
    failure and retry after a pause; a 503 is never a pass.
- **One editorial review** against the standard.
- **A fresh reader.** A separate, context-free agent receives only closed-state screenshots and
  the six unchanged questions of PUBLISH_RULES §10.2. Save its original answers.
- **The independent check is mandatory.**
  - One fresh Integration Critic, which authored none of the changes, reviews the work.
  - It works in a clean detached checkout at the candidate SHA, with only the prescribed inputs.
- **After the MLflow upload, the index and the `--final` build,** obtain an exact-SHA focused
  recheck on the final SHA.
  - It confirms that the delta from the independently checked candidate holds only the index and
    the final-build outputs, and that the checks those files affect pass again.
  - The binding verdict, `docs/track-b/evidence/pres-4/integration.md`, cites that final SHA as
    `final_candidate_sha`.
  - The delta to the evidence tip is verdict-only.
- **Retain first failures and retries.** A local result never stands in for public evidence.

## Timebox
Approximately 24 hours, orientation through terminal return. Report elapsed time to the nearest
half hour. Crossing it is a scope check, not an automatic stop.

## Owner-only actions already authorized
The Owner's delivery of this brief authorizes the local checkpoint on `gauntlet/pres-4`. It also
authorizes exactly one external action, by the Owner's decision of 2026-10-11: **the MLflow upload
of runbook §1 step 5.**

- **When:** only after the independent check has passed at the candidate SHA.
- **What:**
  - exactly the regenerated `cp24`, `cp22` and `cp23` exports the check reviewed, each parent with
    its children, into the experiment `delu-generations` on DagsHub;
  - one write of the experiment description that `EXPERIMENT_NOTE_CHECKPOINTS` produces
    (A-PRES3-1).
- **How:** upload with `scripts/mlflow_publish.py`. Then run the mirror verification, the route
  checks (REST and browser) and the index.
- **Credentials:** the stored DagsHub variables, read inside the uploading process only.
- **Limits:**
  - No other MLflow write: no change to a published run, no registered model, no new experiment
    and no deletion.
  - If the tool would write anything else, stop before writing and return BLOCKED with the exact
    operation.
- **Failures:**
  - Retain a first failure, and retry within the service's limits.
  - If the upload cannot complete, return BLOCKED with the exact remaining operation.
  - Report a partial upload as partial, with the run IDs that exist.

Nothing else is authorized:

- no commit on `main`, landing, merge, push or tag push;
- no Pages deployment, Space upload or remote deletion;
- no governance edit.

Each of those is the Owner's, on a later explicit instruction.

## Stop and return
Return exactly one of PASS / BLOCKED / INCOMPLETE, using `docs/track-b/gauntlet-templates.md`
§3.

- **First commit.** The first commit on `gauntlet/pres-4` copies this brief byte for byte, from
  `.local/artifacts/pres-4/issued-brief.md` to `docs/track-b/evidence/pres-4/issued-brief.md`.
- **The return form.** Return with the complete §3 form, the completed publication packet and its
  applicability matrix.
- **BLOCKED at the external gate.** When all authorized work is complete and only the Owner's
  steps remain, return BLOCKED at that gate. State the local readiness, the MLflow upload's
  verified state and the binding Integration PASS. This is not a product FAIL.
- **Identities and accounting.**
  - Name `final_candidate_sha` and `evidence_tip_sha`, and show their verdict-only diff.
  - Identify the page's hash and size and the export hashes, and give the evidence that the Space's
    bundle and cards are unchanged.
  - List every changed file and every check.
  - Account for every branch, worktree and ref.
- **The owner packet.** Supply a concrete packet for the remaining steps.
  - Every command must be non-interactive: `git --no-pager …`, and `git commit -F <message file>`
    with the message file written under `.local/artifacts/pres-4/`. No pager and no editor.
  - Give each command's expected output.

  The steps:
  1. **The LAND.**
     - First, check that `main`'s checkout holds no untracked copy of a file the branch adds.
     - Then `git merge --squash gauntlet/pres-4`, a check that the staged tree equals the
       evidence-tip tree on the branch's paths, and `git commit -F`.
     - Then the tags: `land/pres-4` on the squash commit and `evidence/pres-4` on the evidence
       tip.
  2. **The push** of `main` and both tags, preceded by the value-based secret scan.
  3. **No Space upload:** the Space is unchanged by the Owner's decision.
  4. **The A6 post-deployment checks** for each surface: Pages, the README, MLflow, and the Space
     card and direct demo, verified unchanged.
     - Run
       `uv run python scripts/publication_receipt.py --landing <the squash commit> --bundle .local/artifacts/pres-3/space-wasm-9028a118 --expect 9028a11869a378ea5c3401a00ad46368e1c9e2f2f9f8732330d32b71af081585`.
     - Add the browser records of `scripts/check_reader_paths.py`.
     - Include an independent public review by a checker that wrote none of the changes.
     - Keep first failures and retries.
  5. **The receipt.** The packet §8 fields each step fills, and the closure record's inputs.
- **Interview-answer triggers.** Name any in one line each (`AGENTS.md` § Interview-answer
  capture); file nothing.
- **Do not** land, merge, stage or commit on `main`, push, deploy, or begin another checkpoint.
