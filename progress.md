# Programme state — DE-LU day-ahead forecasting

*Orchestrator-owned. Regenerated in full on 2026-09-29 at the Owner's explicit request, under
`orchestrator-role.md` § The regeneration contract. The incoming file is the committed
`progress.md` at `05587acdcf0536196678b444a4806c7f05c47cb5` (`main` = `origin/main`, PRES-2
closure). The omission diff against it is summarized in the Session Log. The file was updated
in place the same day for the Owner's ratification of v21-r6 and the CP-21 execution grant.
The task performed no engineering test, fit, data retrieval, deployment or MLflow write. Its
commit and push were made on the Owner's explicit, task-scoped instruction.*

---

## 1. Current Position

### Track B — capstone (the critical path)

**Foundation established.** The v1 product is released. CP-10, CP-15, CP-16 and CP-20 are
landed, GFS is admitted, and PRES-1 and PRES-2 are closed. Their detailed results and accepted
limitations remain in the [landing and closure records and evidence tags](#where-the-history-lives).

**Released product: frozen v1. Best research policy: HG (v3).** HG adds the admitted GFS
wind/radiation features to CP-16's V2-H central-blend/hour-aware policy. CP-20 found joint
point/interval improvement over H0 on the common development population. These are
`development_post_selection` findings, not promotion, product qualification or Live eligibility.
Use the [CP-20 landing record](docs/track-b/cp-20-landing-2026-09-24.md) for exact scores,
intervals and fold qualifications; CP-15's product result remains `NOT_DEMONSTRATED`.

**Programme stages** (Owner's sequence, current state 2026-09-29):

| # | Stage | Status |
|---|---|---|
| 1 | NWP archive-depth gate (4.1) | ✅ Done: GFS admitted |
| 2 | v2 build and causal fix (CP-16, 4.2) | ✅ Done and landed |
| 3 | Presentation around v2 (4.3R), with CP-20 alongside | ✅ PRES-1 and PRES-2 closed |
| 4 | v3 weather pipeline (CP-20, 4.4D) | ✅ Done and landed |
| 5 | Three-block LightGBM (4.5) | ▶ CP-21 on top of v3: v21-r6 §17 ratified and execution authorized 2026-09-29; brief issued; awaiting the Lead's return |
| 6 | DDNN / TabPFN (4.6L → 4.6R → 4.6C) | ⬜ Not started |
| 7 | VRE generation and residual-load model (4.4V, optional) | ⬜ Not started |
| 8 | Recombination (4.8, optional, after 5–7) | ⬜ Not started |
| End | Fresh-data test (4.7T), then live run of the final model (CP-17 → CP-19), then public presentation and CV (4.3C/4.10R) | Reserved for the end |

**Next pending Track B checkpoint: CP-21 — work item 4.5, three-block LightGBM on top of v3.
Ratified, execution authorized and brief issued, all on 2026-09-29.**

- **The choice.** The Owner chose it on 2026-09-29. That answers the 2026-09-24 open question
  and supersedes the earlier recommendation: 4.6 first, then 4.4V and 4.8, with 4.5 only as an
  extra arm of 4.8.
- **Ratified.** [v21-r6 §17](capstone_v21.md) and its
  [amendment record](docs/track-b/capstone_v21-r5-to-v21-r6-amendments.md) were ratified with
  two Owner changes: the pooled attribution arm L-P, and a fourth adoption condition (a per-fold
  veto). Both documents are committed and pushed.
- **Next:** a new Engineering Lead runs CP-21 from the issued brief, which the Owner pastes
  inside the fixed launch envelope. The Orchestrator then runs the templates §4 receipt,
  proposes LAND for any Engineering-PASS outcome, and issues the publication block.
- **Design.**
  - HGL is the sole adoption candidate: HG's blend plus a fixed one-third three-block LightGBM
    member (the mean of raw and normalized blocks), with HG's interval layer re-estimated on
    HGL's own errors. HG is the comparator on identical rows.
  - Attribution arms: L-P (pooled 24-hour, raw), L-R (blocks, raw) and L-N (blocks,
    normalized). The ladder is B3 → L-P → L-R → HGL. L-R − L-P tests the block split, and that
    finding is reported whichever way it falls.
  - The population is CP-20's: 10,747 hours over 448 days in five folds.
- **The rule for v4.** All four conditions:
  1. joint improvement over HG (upper S_WIS endpoint < 0, upper S_MAE endpoint ≤ 0);
  2. all six §8 diagnostics met;
  3. a complete, valid evaluation;
  4. no fold with a resolved degradation in MAE or WIS.
- **Ceilings:** about 32 active hours (hard 40), 60 machine-hours, 24,000 main and 35,000 total
  LightGBM fits, 10,500 policy-days, 20 GiB of disk. No network, and no work from Friday 00:00
  to Sunday 00:00.
- **Outcome.**
  - If the rule is met: `v4 · <adopted change>`, which becomes the base for the next
    extensions.
  - Otherwise: the branch "Three-block LightGBM on v3", marked "Not adopted".
  - Published either way, through a separate publication block after LAND
    ([plan](docs/track-b/cp-21-publication-plan-2026-09-29.md)).
- **Reserved.** CP-17–CP-19 remain reserved for the final model's freeze, live operation and
  prospective evaluation. §16 defines the final product, not CP-21.

**PRES-2 — final state: CLOSED on 2026-09-29, by the Owner's decision after his own manual
public check.** The source is the [closure record](docs/track-b/pres-2-closure-2026-09-29.md).
Its contract remains PUBLISH_RULES 1.0.

- **Shipped:** twelve product subjects below the opening, the v1→v2 and v2→v3 transitions,
  chart routes, the F01–F04 repairs and companion documentation.
- **Integration PASS** at `d7d57e3`, covering the local-ready milestone.
- **Landed and pushed:** `land/pres-2` = `a543616`; `evidence/pres-2` = `871c0e2`.
- **Space deployed:** revision `0c550e8`, bundle `8007f0d2…`.
  ([Deployment receipt](docs/track-b/pres-2-space-deployment-2026-09-29.md).)
- **Targeted public checks passed.** Four demo configurations, after one retained HTTP 429
  failure and a successful retry.
- **The rest of P8** was covered by the Owner's manual check, recorded as his check, not as
  automated evidence.
- **The new independent postdeploy review was waived for PRES-2 only.** This one-time exception
  is not a PASS; the standing rule is unchanged.
- **F01–F04** of the later independent review were closed publicly.
- **`style.css`** was accepted as an unused leftover, to be removed at the next Space upload.
- **Reclaimed:** the branch and worktree. The stale stash was dropped on the Owner's
  instruction.

**Repository:**

- `main` = `origin/main` at the CP-21 ratification commit, a direct child of `05587ac`. It adds
  five documents:
  - the ratified anchor;
  - the amendment record;
  - the publication plan;
  - the programme handoff's consistency notes;
  - this file.

  No branch other than `main`, no worktree besides the primary checkout, and no stash.
- **Left uncommitted:** `שאלות תשובות.docx`, carrying Q&A entry 37. It was not in the Owner's
  commit list. It is not CP-21's; the Lead leaves it untouched.
- **The issued brief's canonical copy** is `.local/artifacts/cp-21/issued-brief.md`, which is
  ignored by Git. The Lead packages it byte for byte in CP-21's evidence.
- **Local material.** Decoded GFS grids, the HG component cache and other CP-20 material stay
  under `.local/` ([artifact map](docs/track-b/local-artifacts.md)); CP-21 reuses them
  read-only. The PRES-2 bundle and records stay in `.local/artifacts/pres-2/` as recovery
  material.

**Public surfaces — distinguish a Git push from a verified deployment:**

| Surface | Last evidenced state / pending action |
|---|---|
| [GitHub repository](https://github.com/hrsi56/delu-day-ahead-forecast) | `main` at `05587ac`, both PRES-2 tags pushed |
| [Static report](https://hrsi56.github.io/delu-day-ahead-forecast/) | PRES-2 page: HTTP 200, SHA-256 `f36314e28811ed4b7ec41bc73dfd481ddb112815effabfc4e7b3ae74d8edab1d`, re-read anonymously 2026-09-29. Behaviour accepted by the Owner's manual check at closure. |
| [Static Space](https://huggingface.co/spaces/Yarden-Viktor/delu-day-ahead-forecast) ([direct app](https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/)) | Revision `0c550e863711e19abbb35219cf64d45dfb39c888`, public/static/RUNNING (re-read anonymously 2026-09-29). Bundle `8007f0d2a9c09a8c2c3182745dac6b38956a9a0ad8f58541f32472b674d5bb4e`: 805 files, 44,164,910 bytes, preserved at `.local/artifacts/pres-2/space-wasm-8007f0d2/`. Plus the unused `style.css`, making 806 files; the next upload removes it. |
| [MLflow on DagsHub](https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow) | Unchanged 23-run, six-route export verified during PRES-2; no post-push recheck claimed. CP-21 adds `cp21` runs only through the publication block. |

**Scope outside Track B:** Track C was cancelled and moved out of this repository; no marketing
state is tracked here. Track A is inactive and has no position. The Owner's end-stage CV-use
decision remains a boundary, not an active workstream.

---

## 2. Setup State

- **No pending one-time actions.** The DagsHub restart item, pending since 2026-09-24, was closed
  on 2026-09-29 on the Owner's confirmation. See the Session Log.

---

## 3. Strategic Anchors

- **Publication anchor:** [PUBLISH_RULES](docs/PUBLISH_RULES.md) **1.1**, Owner-ratified
  2026-09-29; SHA-256 `91eea445434718a163f03bcfd82e1db275a9d98311e76eb6cd1365f3707584f3`.
  A1–A6 continue; strengthened A7 and A8 govern future final-product rollout/daily operation.
  Historical PRES-2 remains governed by 1.0 (`03f106060d9a646ce0c0c986d2f5fb6549929f2ed7270f0c8678fbfd2293b3a3`),
  preserved at `evidence/pres-2:docs/PUBLISH_RULES.md`; PRES-1 retains Publication Standard v1.
  Incorporated baseline: Publication Standard v1 `01d721c2…`; presentation plan revision 3
  `28119374…`.
- **Ratified research authority:** `capstone_v21.md` **v21-r6**, Owner-ratified 2026-09-29,
  SHA-256 `ee402c4703d176f8181ed82966c978ad84c3c73a0cdb1d3567871f58bc867344`.
  - §17 governs CP-21; it was ratified with two Owner changes, and its execution was authorized.
  - §16, unchanged from r5, remains the final-product authority.
  - Historical §§1–16 are byte-for-byte intact; r6 adds only a header, a §10 row and §17.
  - CP-20 is closed under r4, and its §15.7 authority stays spent.
  - [Amendment record](docs/track-b/capstone_v21-r5-to-v21-r6-amendments.md), SHA-256
    `a9086fa1d70ea9cfd9c7fde3733f631bff7b8e372a8990e6cc7a52be3650bedd`.
- **CP-21 issued brief:** canonical copy `.local/artifacts/cp-21/issued-brief.md` (ignored),
  SHA-256 `813fb8a476a7b6d10ecf0a5519e97ec8efc4ff36e0f13868676ad34534fc020f`. The Lead packages
  it as `docs/track-b/evidence/cp-21/issued-brief.md`. It pins PUBLISH_RULES 1.1 and the anchor
  and amendment hashes above.
- **Historical authorities:**

  | Authority | Governed | Where the exact bytes are |
  |---|---|---|
  | v21-r5 | Defined §16; governed no checkpoint | `81ab3be:capstone_v21.md` (`a4e178c3…`) |
  | v21-r4 | CP-20 | `evidence/pres-2:capstone_v21.md` (`150bd53f…`) |
  | v21-r3 | CP-16 | `evidence/cp-16:capstone_v21.md` (`67d21768…`) |
  | v21-r1 | CP-15 | `evidence/cp-15:capstone_v21.md` (`44ea4e54…`) |
  | Original `capstone_v20.md` | CP-10 | `docs/track-b/anchors/cp-10-capstone_v20.md` |
  | `capstone_V6_8.md` | v1 | the file itself |

  Once the live anchor advances, closed checkpoints are reproduced from their `evidence/` tags.
- **Programme plan:** the [v3 plan handoff](docs/track-b/v3-plan-handoff-2026-09-22.md), with
  work items 4.0–4.10 and the decision register D1–D6. Current identity after the CP-21
  consistency notes: `ddc6bd3a…`. It was `0fe3a69e…` after v21-r5's consistency edit
  (`81ab3be`); the `7fdd8205…` recorded here until 2026-09-29 predated `81ab3be`. The
  [CP-21 publication plan](docs/track-b/cp-21-publication-plan-2026-09-29.md) (`c0ac0d26…`)
  plans the publication block that follows CP-21.
- **Target:** hourly day-ahead prices in the DE-LU (Germany–Luxembourg) bidding zone, under the
  inherited forecast-origin and eligibility contract. The aim is better point forecasts and
  honest, useful uncertainty.
- **Budget:**
  - $0 external run rate: no paid licence, purchase or paid tier. A free API registration is
    acceptable when needed.
  - The inherited $65/month ceiling is not spending authorization.
  - Use is non-commercial: CV and open source.
- **Hardware:** Apple M3 with 16 GB, CPU only. v21 permits a bounded local MPS probe. No GPU or
  cloud.
- **Language:** English for documents and briefs. The Owner may write in Hebrew.
- **Governance:**
  - `AGENTS.md` is canonical: lockdown, credentials, Git and publication authority, branch
    lifecycle.
  - `orchestrator-role.md` and `engineering-role.md` govern their roles.
  - `docs/track-b/gauntlet-templates.md` holds the four forms.
  - `orchestrator-role.md` and `program-stage-sequence.md` carry scope-narrowed headers: their
    Track A and Track C content is historical.
  - Publication and mainline history belong to the Owner. Task-scoped delegations are recorded in
    the Session Log.
- **Platforms, access and tooling:**
  - **Credentials:** `DAGSHUB_USER_TOKEN` (also supplied as `MLFLOW_TRACKING_USERNAME` and
    `MLFLOW_TRACKING_PASSWORD`), `ENTSOE_API_TOKEN` and `HF_TOKEN`, stored in `~/.zshrc` and
    `launchctl`. The rules are in `AGENTS.md` § Credentials. Verify `.zshrc` variables with
    `zsh -ic`, not `zsh -lc`.
  - **DagsHub MLflow:**
    - It uses HTTP basic auth; Bearer returns 401.
    - Public links use the `.mlflow` host, and `scripts/check_links.py` keeps the gated URLs as a
      control.
    - DagsHub provides tracking, registry and storage, but no compute.
  - **Hugging Face (`Yarden-Viktor`):** only Static Spaces have been free since 2026-07-08.
    Upload with `HfApi.upload_folder`, because `hf upload` returns 402.
  - **ENTSO-E:** `entsoe-py` 0.8.0 puts the token in request URLs and exception text. Redact both,
    and prefer SMARD for unattended jobs.
  - **CI:** GitHub Actions is free for this public repository. `invariant-tests` runs on every
    push, pinned to Python 3.12.
  - **Checks:** `make verify` binds the cross-surface claim set. PRES-1 repaired F05:
    `scripts/check_links.py` now fails on broken required links; its post-deploy gate passed.
  - **Secret guard:** `.githooks/` together with `scripts/secret_guard.py`. It is enabled locally
    with `git config core.hooksPath /Users/djourno/Downloads/PJM/.githooks`, and a fresh clone
    must enable it again.

---

## 4. Standing Scope Decisions

These carry forward indefinitely. Each changes only by explicit Owner ratification, named in the
Session Log.

**Added 2026-09-29 (Owner — CP-21 ratification):**

- **v4's chart encoding, used only if a v4 is adopted:** amber `#B45309`, a filled diamond
  marker and the direct label "v4" (PRES-1 W16(b)). This resolves the Publication Standard's
  "At v4" trigger in advance.

**Added 2026-09-29 (Owner — final-product lifecycle):**

- The exact version the Owner designates final becomes the selected product. Completed rollout
  aligns final version, product, primary demo and daily forecasting policy; selection alone
  does not certify deployment or predictive quality. Until rollout, show pending status honestly.
- Freeze the policy, initialization and update/evaluation rules; require daily retraining,
  eligible data refresh and issuance with dated artifacts and lineage. Context/input refresh
  alone is not training. Any incompatible model/cadence needs an explicit Owner exception.
- Final-product order: daily product panel → **How the product works** → scientific
  **Product results** → **Business insights** → **How the models compare**, followed by all
  previously planned sections unchanged. The twelve-subject documentation follows that product.
  Under A8, the early A2 placement bound applies to the product finding, not the later comparison.
- Today: originally issued hourly forecasts against eligible published prices, defined percentage
  performance alongside MAE. Tomorrow: issued hourly predictions and intervals; past coverage and
  width qualify reliability. Freeze formulas/windows/denominators and zero/negative-price handling;
  show pending, incomplete, stale and failed states and separate fit/refresh/issuance times.
- Business profit/value curves require a defined, evaluated decision policy, costs, benchmark,
  full time series and risk/loss context; label simulation versus realization. Otherwise show
  the evidence gap. Forecast accuracy is not profit; no economic experiment is opened here.
- Every delivery day is in scope, including DST and Friday/Shabbat, without scheduled manual
  Owner work on those days. Future operating authorization must supply unattended coverage,
  monitoring and failure rules. No scheduler or standing public-write permission is created now.
- Research v21-r5 §16 and publication 1.1 A7/A8 are prospective; PRES-1/PRES-2 evidence and
  immutable v1 remain unchanged. CP-17–19 and CP-21 require their own bars/briefs. Live may be
  displayed during CP-18 as evaluation in progress; CP-19 still needs at least 90 delivery days.

**Added 2026-09-24 (Owner):**

- **Same information, same opponent.** Every new model receives exactly the information HG
  receives, including the three frozen GFS weather features and their missing indicators. It is
  evaluated against HG on identical rows. Beating a weaker reference means beating the wrong
  model.
- **No data after the development window until the final test.** Nothing dated after
  2026-04-07, the last fold-5 delivery day, may be read, scored, plotted or used for any choice
  before the single final fresh-data test (4.7T). This covers prices, weather and every other
  input or outcome. Each additional model selected on the same development periods makes that
  test more important.
- **Final sequence.** The fresh-data test (4.7T) is reserved for the end. Only the final model
  built goes live (CP-17 freeze, then at least 90 consecutive days, then CP-19); the current HG
  is not frozen. CV use comes last, after the holidays. *Amended 2026-09-24:* the public site is
  updated as each generation lands, starting with v1–v3 now.
- **One scrolling history page.** The public report is a single page that stays single however
  many generations exist. Chapters run newest first, with the live model eventually at the top.
  Each generation is shown with its results, statistics, and pros and cons, including
  generations that were not adopted.
- **MLflow is the visible cross-version tool.** v2/v3 runs are backfilled, and future checkpoints
  are tracked in MLflow. `delu-cp2` (v1's record) stays untouched. The design is in the
  [presentation and tracking plan](docs/track-b/presentation-and-tracking-plan-2026-09-24.md).
- **Publication anchor (updated by Owner authority, 2026-09-29).** New publication briefs follow
  [PUBLISH_RULES 1.1](docs/PUBLISH_RULES.md), including its explicit amendments and triggers;
  the already-issued PRES-2 task retains 1.0 and its original evidence contract.
  [Publication Standard v1](docs/track-b/publication-standard-v1.md), ratified 2026-09-28, remains
  the incorporated baseline and the historical PRES-1 acceptance contract.
  - The headline is defined before results, and every percentage is a derived record.
  - One registry supplies names and statuses.
  - Publication is complete or not at all.
  - A blocking rule sits beside an advisory log.
  - Its core changes only by the Owner. Every brief cites its SHA-256.
  - From CP-21 on, each checkpoint's return carries a publication packet.
  - Every adopted generation explains its predecessor transition without replacing the protocol
    comparator or inventing experiments. The full twelve-subject product documentation follows
    the active released/frozen product opening and moves with the product when it changes;
    research generations retain concise decision histories. Explanatory charts have descriptive routes.
  - Headline values name their metrics; usable-screen placement accounts for the header.
  - Postdeploy evidence verifies public identities and behaviour. Future live panels distinguish
    frozen policy, fitted artifact, daily inference, retraining and measured uncertainty.
  - The new anchor changes publication requirements, not research scope, model status or release authority.
- **Presentation and tracking rules (plan R1–R6, approved 2026-09-24):**
  - v1's holdout moves into the v1 chapter and is not deleted;
  - agents build the page and charts from data, and the Owner reviews visually before any push;
  - version numbers go only to adopted models;
  - the repository is the source of truth: MLflow mirrors it, and the page never reads MLflow;
  - checkpoints track locally and publish to MLflow at landing;
  - the Model Registry holds only runnable, frozen policies.
- **Presentation decisions (plan §16, 2026-09-24):**
  - **Generation naming:** `vN · <adopted change>`.
    - A number is given only after adoption, and none is reserved in advance (for example, for
      DDNN or VRE).
    - A rejected experiment stays a branch with a descriptive name.
    - "Final candidate" and "Live" are statuses of a version, not names.
  - **Independent check:** mandatory for presentation releases. It is done by a checker that did
    not write the changes, and it covers the data, the claims, the charts, the links and the
    reading experience. The Owner's visual approvals at D1 and at the end come in addition to it.
  - **The MLflow step** is carried in briefs until its route has completed and been verified
    once. Then it goes into the landing templates. The Owner granted the Lockdown suspension for
    that edit, and it is applied in a separate task.
  - **The capability probe** is local plus read-only against DagsHub, with no public write probe.
    Capabilities are verified against the service after the authorized upload.
  - **The experiment is `delu-generations`,** on every surface; `delu-cp2` stays untouched.
  - **The contribution statement is required,** in the Owner's wording (plan §8.9).
  - **The visual tokens in plan §7.3** are the D1 starting point.
- **Credentials.** They are stored as `~/.zshrc` exports mirrored in `launchctl`, on a
  single-user, biometric-locked machine. Agents never view or hand-type a value and use
  credentials only as stored variables. The secret guard is mandatory (`AGENTS.md` §
  Credentials).
- **CP-20 local weather material is retained.** `.local/artifacts/cp-20/weather/` holds the only
  copy of the decoded GFS box grids ([artifact map](docs/track-b/local-artifacts.md)).

**Data and target:**

- **Data begins 2019-01-01 by design.** DE-LU split from DE-AT-LU on 2018-10-01, so earlier
  prices belong to a different product. The start covers the pre-crisis, crisis and
  normalization regimes; it is neither an outage nor a truncation. Sources: `4ec9fab`,
  `2517e55:progress.md:106`, Q&A entry 2.
- **Two inherited data-vintage assumptions stay disclosed.**
  - Pre-gate availability of the A65/A01 load forecast was assumed, not proven.
  - The historical 42-day, D−2-bounded A75 generation proxy uses current archive values, and
    their revision status is unproven.

  Both accompany any historical availability claim and neither relaxes v21's causal-input
  rules.
- **SMARD is the planned fallback-primary source.** CP-1 used it during the ENTSO-E outage under
  the existing clause. This is not blanket authority for new sources or targets.
- **The target stays hourly means over canonical delivery hours** across the 2025-10-01
  quarter-hour transition.
  - Quarter-hour inputs aggregate to hours, with complete-bin and chunk-boundary handling.
  - 23-, 24- and 25-hour days keep their identity.
  - The snapshot's 576 negative hourly means and the regulator's 573 are different quantities.
- **The delivery-day availability invariant (v21 §2) holds.** Masking delivery-day prices changes
  the output by exactly `0.0`, and a D−1 mutation must move it (currently `220.9433` EUR/MWh).
- **Weather source.** Direct weather comes from the admitted GFS 0.25° D−1 00 UTC archive: NCAR
  d084001 through 2020 and NOAA AWS from 2021. It covers all five folds (v21-r4 §15).
  Open-Meteo's archive is not gate-legal, because it stitches short-lead runs. ICON-EU is not
  admitted. *Amended 2026-09-24:* this replaces the decision that gate-legal weather began in
  2024 and folds 1–3 were unreachable, which the ratified GFS admission superseded.
- **No fuel-price layer.** No free, daily and redistributable TTF/THE series exists. A read-only
  structural feasibility sheet is the most v21 permits. See [`DATA-LICENSE.md`](DATA-LICENSE.md).

**Claims and evidence:**

- **v1's only confirmatory claim is the one-shot holdout.** The champion beats the similar-day
  naive on both metrics:
  - MAE 25.9078 vs 27.7578 (−6.66%);
  - mean pinball 6.7083 vs 13.8789 (−51.67%);
  - DM p = 1.98e−18.

  Everything else is `development_post_selection`.
- **Two unflattering v1 results stay on every public surface:**
  - the development point-MAE DM has p = 0.948 and statistic +1.6228. The median is 28.58% worse
    than the naive, driven by August 2022 (fold 3);
  - interval coverage over the August-2022 peak weeks is 0.194.
- **Recovered v1 facts are preserved:**
  - fold 3 trained through 2022-04-29, including 5,784 crisis hours. The diagnosis was shrinkage
    toward the training level;
  - the residual-load proxy lost (13.0158 vs 13.0642 mean pinball);
  - the measured 19.49% post-gate A69 information cost did not authorize using A69;
  - the four cutoffs (snapshot, raw fit, final calibration, holdout), the no-retrain identity and
    the semantic fingerprint are kept.
- **Research status labels persist:**
  - CP-15 product feasibility stays `NOT_DEMONSTRATED`;
  - CP-16 and CP-20 results are `development_post_selection`;
  - economics stay descriptive, and no product threshold is invented.

**Process:**

- **Owner observance (clarified 2026-09-29): no scheduled manual Owner work on Friday or
  Shabbat.** The ratified daily-product obligation still covers those delivery days; its future
  brief must explicitly authorize unattended coverage and failure handling before launch.
- **Reasoning capture is active** (`AGENTS.md` § Interview-answer capture).
  - Only the Orchestrator files entries, through `scripts/qa_append.py`; the Lead names triggers
    in its return.
  - `שאלות תשובות.docx` has 37 entries. Entry 37 covers why CP-21 adds the block LightGBM on
    top of v3, with a pooled control and a pre-registered rule; it is uncommitted, pending the
    Owner. Entry 36 covers frozen policy versus daily training and product presentation.
  - Presentation is the Owner's.
- **Retired controls stay retired.** These are AMD-G5's waived negative control, the old
  point-in-time capture ledger, publication-metadata substitution and the four-catalog selection
  machinery.
- **Amendments granted and spent:** WASM for CP-3B only, and sequential conformal for C-2 only.
  v21 opens its stated comparisons, not an unlimited method set.
- **Track A is out, and Track C was cancelled on 2026-09-15.** `TRIG-C` and `C-1` are struck.
- **Optional and unscheduled:** `Binary Classification Mini-Capstone.md` and
  `aws-extension-spec_v1_1.md` (stale).

---

## 5. Session Log — newest first

- **CP-21 ratified, authorized and issued, 2026-09-29.** The Owner: "מאשר את v21-r6 עם שני
  שינויים, ומאשר ביצוע CP-21".
  - **D1:** HGL confirmed as the sole candidate. The pooled attribution arm L-P was added: one
    24-hour LightGBM, raw target, HG's exact information with weather, and the H layer on its
    own errors. It is not adoption-eligible.
    - It tests the block hypothesis through the ladder B3 → L-P → L-R → HGL.
    - L-R − L-P is a descriptive secondary contrast, and the split claim is reported by result.
  - **D2:** three conditions, plus a fourth: no fold with a resolved HGL − HG degradation in MAE
    or WIS.
  - **D3, D5 and D6 as recommended.** D6: amber `#B45309` with a filled diamond marker.
  - **D4, recomputed for L-P:** 11 policies, 22,330 nominal fits (24,000 main, 35,000 total),
    10,500 policy-days, 60 machine-hours, about 32 hours (hard 40).
  - **Setup item closed on the Owner's confirmation.**
    - The Claude app started 2026-09-24 at 22:56, after the rotation; the exposure/rotation
      record was committed at 15:49 that day.
    - PyCharm and Terminal were not running.
    - Verified uploads have since succeeded: PRES-1 F1 and PRES-2's Space.
  - **Actions:**
    - §17 was finalized and v21-r6 marked ratified; the amendment record, handoff notes,
      publication plan and this file were updated.
    - Q&A entry 37 was filed with the prescribed appender, and left uncommitted because it was
      outside the commit list.
    - The five named documents were committed and pushed on the Owner's explicit, task-scoped
      instruction, with the secret guard enabled.
    - The brief was issued in the fixed envelope for a new Engineering Lead.
    - The Lockdown suspension ended at this return.
  - **Omission review:** within this in-place update, the removed items are:
    - the draft status;
    - the answered D1–D6 question (resolved above);
    - the closed Setup item (resolved above);
    - the done "[On CP-21 ratification]" notes.

    The pre-update copy is in `.local/artifacts/cp21-orchestration-2026-09-29/`.
- **CP-21 drafted; programme state regenerated, 2026-09-29.**
  - **The Owner's choice, in his words:** "לצורך שימוש בv3 והוספה עליו של פיצול LightGBM
    לשלושה בלוקים ואימון מחדש, נוסיף את התוצאות לאתר להשוואה בכל מקרה …". In short: 4.5 on top
    of v3, published in either outcome; v4 if it improves under a rule fixed in advance,
    otherwise a not-adopted experiment.
    - It answers the 2026-09-24 CP-21 question.
    - It supersedes the recommendation to use 4.5 only as an arm of 4.8.
  - **Authority:** a task-scoped Lockdown suspension for v21-r6 §17, its amendment record and
    consistency edits to the programme handoff. It is spent at this task's return.
  - **State checks.**
    - The first check found PRES-2's closure incomplete: deployment committed at `5a6b585`,
      review and reclamation open. The Orchestrator stopped and reported.
    - The Owner then confirmed the closure finished. `05587ac` (closure and reclamation) was
      verified on `main` and `origin`.
    - Verified anonymously and read-only: the anchor, PUBLISH_RULES and tag identities, the Space
      revision and the Pages hash.
  - **Produced, uncommitted:**
    - `capstone_v21.md` draft v21-r6: header, a CP-21 row in §10, §17; additions only.
    - The [amendment record](docs/track-b/capstone_v21-r5-to-v21-r6-amendments.md), with six
      decisions and recommendations.
    - The [publication plan](docs/track-b/cp-21-publication-plan-2026-09-29.md) for both
      outcomes, recommending a separate publication block after LAND.
    - Dated 4.5 consistency notes in the programme handoff.
    - This regeneration.
  - **PRES-2's final state** was recorded from its closure record, without rerunning its checks.
  - **A stale pointer was corrected:** the programme-plan identity had been left at `7fdd8205…`
    since `81ab3be`.
  - No fit, data retrieval, MLflow write, deployment, commit or push was performed.
  - **Omission review** against `05587ac:progress.md`. Nothing was dropped silently; every other
    item was retained.
    - Now in "Where the history lives," as resolved items or history:
      - PRES-2's identity/step table;
      - the resolved "later independent public review" blocker;
      - the stale "PRES-2 still awaits deployment acceptance" pointer.
    - Compressed to one line each, with decisions, reasons and links kept: the older multi-line
      Session Log entries.
    - Renamed: "[After PRES-2 / next research brief]" is now "[Every research brief]"; its
      content is unchanged.
    - The incoming copy and the diff are in `.local/artifacts/cp21-orchestration-2026-09-29/`.
- **PRES-2 closed, 2026-09-29.** Closed by the Owner's decision after his manual public check
  ("בדקתי ידנית בעצמי. אפשר לסגור הכל"; "בצע בעצמך מה שצריך"). The independent postdeploy review
  was waived for PRES-2 only, not a PASS. F01–F04 were closed publicly and `style.css` accepted.
  The branch was reclaimed after verifying that `evidence/pres-2` reaches all 12 commits, and the
  stale stash was dropped. The CP-21 choice was recorded.
  [Closure record](docs/track-b/pres-2-closure-2026-09-29.md).
- **PRES-2 Space deployed, 2026-09-29.** The Owner authorized the upload. The exact bundle
  `8007f0d2…` went up as Hub revision `0c550e8`, with all 805 files verified and the card and
  normalized HTML matching. Four public demo configurations passed after one retained 429
  failure and retry. No research, MLflow or Git change.
  [Receipt](docs/track-b/pres-2-space-deployment-2026-09-29.md).
- **Publication surface completion check, 2026-09-29.** After the Owner flagged the stale Space,
  runbook §1a and packet §8 were added so that every release accounts for Pages, the Space,
  MLflow and the README. An unchanged MLflow export is verified, not duplicated. Final daily
  training must reach the hosted demo. No locked anchor or service changed.
- **Final-product rules ratified, 2026-09-29.** The Owner approved the suspension ("מאשר באופן
  מלא") for PUBLISH_RULES 1.1 (A8, strengthened A7) and research v21-r5 §16: one
  product/demo/daily-policy identity, product-first page order, daily retraining with an
  exception route, defined percentage and uncertainty display, evidence-based business
  insights. Q&A entry 36 was filed. No model was selected.
- **Progress regeneration, 2026-09-29 (after the PRES-2 return).** A full regeneration at the
  Owner's request. It corrected stale landing and branch state, and closed history was
  compressed without dropping decisions. The recovery copy is in
  `.local/artifacts/progress-regeneration-2026-09-29/`.
- **PRES-2 landing, 2026-09-29.** On the Owner's explicit instruction, evidence tree `871c0e2` was
  squash-landed as `a543616`, and `main` and both tags were pushed. No tests were repeated. This
  was a task-scoped instruction, not a standing governance exception.
- **PRES-2 return, 2026-09-29.** BLOCKED only at publication authority. Integration PASS at
  `d7d57e3`, with evidence at `871c0e2`; R1–R7 are advisories.
- **PRES-2 brief issued, 2026-09-29.** Pinned PUBLISH_RULES 1.0 and migration revision 1, with an
  approximately 32-hour timebox. [Brief](docs/track-b/pres-2-execution-brief-2026-09-29.md).
- **Migration plan, 2026-09-29.** [Revision 1](docs/track-b/publish-rules-migration-plan-2026-09-29.md) mapped the product subjects, predecessor comparisons, F01–F04 and A1–A6. It kept two limits explicit: the frozen-versus-fold-5 SHAP, and the absent paired v2−v1 uncertainty. A7 was deferred.
- **PUBLISH_RULES 1.0 established, 2026-09-29.** Established under the Owner's task-scoped
  suspension; subjects 1–12 belong to the active product. The suspension ended at return.
- **Preservation correction, 2026-09-29.** Recovered state omitted in `3cd7592` from `a067d2f`.
  This is why an omission review must use the full incoming working copy.
- **PRES-1 closure, 2026-09-29.** Owner-delegated landing, push, Space redeploy and F6–F8 succeeded;
  the initial 429 failures were retained and the branch reclaimed.
  [Landing record](docs/track-b/pres-1-landing-2026-09-29.md).
- **PRES-1 D5 reaffirmation, 2026-09-29.** The Owner's exception covered PRES-1's landing,
  deployment, postdeploy checks and closure only.
- **PRES-1 receipt/F5, 2026-09-29.** Final independent PASS; entry 35 filed.
  [Receipt](docs/track-b/pres-1-receipt-2026-09-29.md).
- **Publication Standard v1 ratified, 2026-09-28.** D1–D3, D5 and D6 approved, D4 withdrawn, D7
  optional; the exact scope is in standard §§16–17.
- **Standard derivation, 2026-09-28.** [Derivation record](docs/track-b/publication-standard-derivation-2026-09-28.md); the earlier release review was superseded, not used as a gate.
- **Earlier PRES-1 release review, 2026-09-28.** Candidate `af0abb0` was not ready to land
  ([superseded review](docs/track-b/presentation-release-review-2026-09-28.md)).
- **Presentation plan R3 approved/brief issued, 2026-09-24.** All nine §16 answers recorded; MLflow template integration remains a separate task.
- **Design review/R3, 2026-09-24.** [Review](docs/track-b/presentation-design-review-v2-2026-09-24.md) resolved states, SVG markup and visual grammar.
- **External review/R2, 2026-09-24.** [Review](docs/track-b/presentation-review-and-corrections-2026-09-24.md) corrected units, gate order, evidence layers and MLflow claims.
- **Presentation plan R1, 2026-09-24.** One growing history page, v1–v3 now, MLflow backfill, publication as generations land.
- **Progress/credential rules, 2026-09-24.** Four standing decisions ratified; the value-based credential guard added.
- **CI restored, 2026-09-24.** Collection repairs and a Python 3.12 pin landed.
- **Credential exposure/rotation, 2026-09-24.** The Owner rotated the exposed DagsHub token, with no history rewrite. [Record](docs/track-b/credential-exposure-2026-09-24.md); the old-application restart item was closed on 2026-09-29.
- **CP-20 LAND, 2026-09-24.** `land/cp-20` and `evidence/cp-20` preserve the accepted research; no promotion.
- **2026-09-23.** CP-20/v21-r4 ratified and issued; weather/content admission and CP-16 PASS/landing accepted.
- **2026-09-15/16.** v21 adopted; CP-15 resumed and landed with CP-10; the 2019 boundary recovered.
- **Earlier.** v1 foundation released and closed; see Current Position and the evidence tags.

---

## 6. Blockers / Open Questions

- **Final-product operating specification remains pending:** no final version designated and no
  daily system running. Future authorized work must fix numeric fit/issuance schedules, training
  windows, resources, percent-score formula/tolerance, source/outcome timing, business-use-case
  evaluation (if any), deployment/daily-demo design and Friday/Shabbat failure coverage. These
  implementation fields do not reopen the now-ratified product identity/order/daily-fit decision.

- **PRES-2 advisories:** R1–R7 in the [Integration verdict](docs/track-b/evidence/pres-2/integration.md)
  and the [advisory log](docs/track-b/publication-advisory-log.md) remain recommendations for the
  next publication, not release failures. They include transition question wording, startup
  timing for the new public bundle, product evidence links, data wording, carried editorial points,
  byte-count logging and clean-checkout reproduction order. The targeted public runs recorded
  19.2–21.4 s to a visible forecast; these are observations, not a benchmark.

- **PRES-1 remains closed under its landing record.** F6–F8 passed under the explicit Owner
  exception. Initial HF/DagsHub rate-limit failures and successful retries are recorded.
  Historical active-hour total and added-disk baseline remain unavailable, not retroactively
  certified compliant. Required tags preserve all evidence. New rules do not retroactively turn
  PRES-1 advisories into violations.
- **CP-20's analysis and reference passes are exhausted.** Further CP-20 scoring would need a cap
  decision. CP-21 reuses CP-20's saved vectors metric-only, under its own ratified caps.
- **The weather admission is conditional** on inferred NCAR field presence and reconstructed
  availability. 2019-01-01 is structurally missing.
- **Product feasibility remains `NOT_DEMONSTRATED`** (CP-15). No policy is qualified.
  Chronos-2 was only an unscored probe.
- **The registry-loading requirement (v21 §9) is not implemented yet.** It needs exact
  initialization versions and fingerprints, refusal before any outcome access, and state lineage
  for prescribed updates.
- **Independent plan-review limits:** v21 has had Orchestrator consistency checks, not an
  independent engineering audit. Every checkpoint needs a fresh independent Integration review.
- **CP-3B item 6 was never completed.** No verdict binds `55a70e7`
  ([record](docs/track-b/evidence/cp-3b/item-6-NOT-COMPLETED.md)). This is not a precedent:
  every brief must require a binding verdict.
- **Earlier review's public-surface defects F01–F04 were recorded as resolved by PRES-1.**
  Responsive report, explicit demo startup states, current verified tracking links and generated
  README shipped; the landing post-deploy checks passed. This historical disposition is distinct
  from the later review's F01–F04, which PRES-2 closed.
  Transient hosting 429s remain an availability limitation, with initial failures retained.
- **Known issues, no action scheduled:**
  - a cold first visit to the Space can hit a Hugging Face `429`;
  - `reports/cp3/pages_build.json` stamps its build date;
  - `actions/checkout@v4` and `setup-uv@v6` target the deprecated Node 20, though they run on
    Node 24;
  - `AGENTS.md` § Interview-answer capture has the typo "agents Never hand-edit". Fixing it
    requires a suspension.
- **Closed and not to be reopened:**
  - the CP-0 defect ledger (20 defects, closed 2026-09-14);
  - the ENTSO-E outage;
  - PRE-2 / DagsHub MLflow;
  - the `hrsi56` vs `Yarden-Viktor` Hugging Face account question;
  - the missing LICENSE.

---

## 7. Notes for Future Sessions

- **[CP-21 launch]** The Owner pastes the issued envelope into a new Code-tab session.
  - Launch on Sunday–Wednesday, so that the expected compute ends before Friday 00:00.
  - The Lead stops at a checkpoint for Friday–Saturday and resumes on the Owner's message.
  - Commit Q&A entry 37 whenever convenient; it is outside CP-21.
- **[After CP-21's return]** Run the templates §4 receipt checks. Propose LAND for any
  Engineering-PASS outcome, then issue the publication block (PRES-3) from the
  [publication plan](docs/track-b/cp-21-publication-plan-2026-09-29.md), pinned to
  PUBLISH_RULES 1.1. It covers every surface: Pages, the Space, MLflow and the README.
- **[4.7T]** If v4 is adopted, its frozen manifest carries both v3 and v4.
- **[If v4 is adopted, at CP-21's landing]** Ask the Owner to update the standing decision
  "same information, same opponent", which names HG, so that later extensions face v4 on v4's
  information.
- **[Next Space deployment]** Delete remote files that are not in the reviewed bundle; the
  unused `style.css` has survived PRES-1 and PRES-2. Then verify that the served file set equals
  the bundle. Account for every surface: Pages, the Space, MLflow and the README (runbook §1a,
  packet §8). A Git push is not a verified deployment.
- **[Every new publication brief]** Pin PUBLISH_RULES 1.1 and incorporated source hashes;
  retain A1–A6 and apply A7/A8 at their final-product/live triggers. PRES-2 was closed under
  its original 1.0 contract. Predecessor comparisons and descriptive chart routes remain;
  v2→v3 reuses existing weather evidence, and v1's archive stays historical.
- **[Final-product designation / CP-17–19]** Carry research v21-r5 §16, publication 1.1 §§5/7.2,
  runbook §7b and packet §5d. Complete the numeric operating/scoring manifest, publish one
  product/demo policy at authorized rollout, and distinguish daily live evidence from completed
  prospective evaluation. No current research generation is promoted by this documentation task.
- **[2026-10, from the 19th]** `ubuntu-latest` moves to Ubuntu 26. CI is pinned to Python 3.12;
  check the first run after the move.
- **[Every research brief]** Apply the 2026-09-24 standing decisions:
  - HG's information set, with HG itself as a reference on identical rows;
  - no data after 2026-04-07;
  - a TabPFN run needs 4.6L's licence-use table first;
  - positive controls must survive the model's own transforms (see Lessons).
- **[After publication / governance follow-up]** PRES-1 W16/template proposals remain in its
  preserved return for a separate appropriately authorized governance task; no locked-template
  amendment is certified here. PRES-2's runbook/packet updates do not establish that every W16
  proposal was adopted. Until that task runs (D6 of 2026-09-28), every research brief carries
  the MLflow step and the packet explicitly, as CP-21's brief does. Do not repeat F1 or reopen
  PRES-1.
- **[End of programme, after the holidays]**
  1. The 4.7T fresh-data test on the unused period. Report the never-published sub-period from
     2026-09-07 separately.
  2. The CP-17 freeze and a live run of at least 90 days for the final model only. The live panel
     goes at the top of the page.
  3. CV use. Presentation is the Owner's.
- **[Any future adaptive-conformal method]** Define the alpha convention explicitly
  ([Gibbs–Candès miscoverage](https://arxiv.org/html/2106.00170v3#S2.E2)), with hit/miss
  direction fixtures.
- **[Standing carry]** No executor for CP-17–CP-19 starts without its complete bar and brief. No
  prospective clock starts before an eligible policy and its update and evaluation rules are
  frozen. The weather-vintage, fuel-rights, delayed-feedback and registry-loading limits carry
  forward; no token, library or green local test solves any of them.
- **[Standing carry]** No Track A or Track C follow-up and no optional project is scheduled.
  Reasoning capture stays active.

---

## Lessons that cost something

Each was paid for once. None should be relearned.

- **Scan for secret values, not shapes.** A pattern scan passed the DagsHub token on 2026-09-24.
  Tests must not dump the environment.
- **A positive control must survive the model's own transforms.** CP-20's frozen ×3 weather
  control passed on rounding noise, because standardization cancels a uniform rescaling.
- **Store hash-bound files byte for byte.** CP-20 Integration attempt 1 failed because Git
  normalized the line endings of a CSV that the frozen protocol had hashed.
- **Compression must preserve decision reasons.** `8d56942` dropped the 2019 boundary. Recover a
  decision with its provenance; never treat silence as a reset.
- **Check the forecasting task before the implementation.** Reason from one whole-day issuance and
  admissible information. Constrain semantics, not syntax.
- **Plan for source and scheduler failure.** Remember the ENTSO-E outage. Do not rely on a free
  Actions schedule for a hard deadline.
- **A clarification can expose an unverified assumption.** Verify against the artifact or a
  current primary source.
- **A green test run is not evidence.** CP-1's first PASS hid 95.83% leaked rows, and an
  independent audit caught it.
- **A negative assertion needs a positive control** that proves it can fail.
- **Fix the generator, not the output.** `scripts/cp2_report.py` once re-emitted a corrected
  MiB/MB label.
- **A brief that asserts a platform fact must re-verify it.** Hugging Face Docker Spaces had
  already left the free tier.
- **Tell a Lead to verify its starting state.** Leads caught wrong SMARD IDs and stacked
  crossing counts.
- **Read a return for protocol defects as well as for its verdict.** Verify the hard gate
  independently.
- **Grep for conflict markers when opening a session.** `30b1b9f` published six.
- **The holdout is opened once.** v1's is spent, and the model that ships is the model that was
  evaluated.

---

## Where the history lives

- **Reviewed chains:**
  - `evidence/cp-0`, `evidence/cp-1`, `evidence/cp-2`, `evidence/cp-3`, `evidence/cp-3b`,
    `evidence/cp-15` (including CP-10), `evidence/cp-16` and `evidence/cp-20`, with landings at
    the matching `land/` tags;
  - `evidence/pres-1` / `land/pres-1` and `evidence/pres-2` / `land/pres-2` preserve the
    publication chains; both publications are closed and their branches reclaimed;
  - `archive/cp-0-attempt-1`, `archive/weather-admission-20260923` and
    `archive/cp15-cp16-content-20260923`.

  Squash landings do not contain the candidate SHAs; only the tags preserve them. Verdicts are in
  `docs/track-b/evidence/<cp>/`.
- **Publication evidence:**
  - PRES-1: [landing](docs/track-b/pres-1-landing-2026-09-29.md);
  - the [later independent public review](docs/track-b/publication-postdeploy-independent-review-2026-09-29.md):
    F01 unnamed demo controls, F02 favicon 404, F03 hidden startup metadata, F04 fairness note
    without the day count. They were fixed in PRES-2 and closed publicly on the Owner's check;
    these IDs are distinct from the earlier review's F01–F04;
  - PRES-2: [Integration](docs/track-b/evidence/pres-2/integration.md),
    [acceptance](docs/track-b/evidence/pres-2/acceptance.md),
    [publication packet](docs/track-b/evidence/pres-2/publication-packet.md),
    [Space deployment receipt](docs/track-b/pres-2-space-deployment-2026-09-29.md) and
    [closure record](docs/track-b/pres-2-closure-2026-09-29.md). PRES-2's identities: candidate
    `d7d57e3`, evidence tip `871c0e2`, landing `a543616`, Space revision `0c550e8`, bundle
    `8007f0d2…`.
- **Landing and receipt records:**
  - [CP-15 landing](docs/track-b/cp-15-landing.md);
  - [CP-16 landing](docs/track-b/cp-16-landing-2026-09-23.md);
  - the CP-16 [blocked](docs/track-b/cp-16-blocked-receipt-2026-09-23.md) and
    [PASS](docs/track-b/cp-16-pass-receipt-2026-09-23.md) receipts;
  - the [weather/content intake](docs/track-b/weather-content-intake-2026-09-23.md);
  - [CP-20 landing](docs/track-b/cp-20-landing-2026-09-24.md);
  - the [credential exposure record](docs/track-b/credential-exposure-2026-09-24.md).
- **Earlier state narrative:**
  - `f704ac4:progress.md`;
  - [context recovery](docs/track-b/progress-context-recovery-2026-09-15.md);
  - the [2026-09-15 handover](docs/track-b/orchestrator-handover-2026-09-15.md);
  - [decision packet 4.0a](docs/track-b/v2-decision-brief-packet.md).

  The issued checkpoint briefs and handoffs are in `docs/track-b/`.
- **Plans:**
  - `capstone_V6_8.md` (v1);
  - `capstone_M4_v2-plan.md`;
  - `capstone_v20.md` and its archived CP-10 copy;
  - `capstone_v21.md` with its amendment sheets;
  - the programme plan and its reviews in `docs/track-b/`;
  - the [CP-21 publication plan](docs/track-b/cp-21-publication-plan-2026-09-29.md).
- **Defect ledger:** `docs/track-b/cp-0-defects.md`, closed 2026-09-14.
- **v1 results:** `docs/cp2-model-report.md` and `reports/cp2/`.
- **Local recovery material:** `.local/`, per the [artifact map](docs/track-b/local-artifacts.md).
  It is not an off-device backup.
- **Everything else:** `git log`.
