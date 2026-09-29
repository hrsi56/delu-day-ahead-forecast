# Programme state — DE-LU day-ahead forecasting

*Orchestrator-owned. Regenerated 2026-09-29 at the Owner's explicit request, under
`orchestrator-role.md` § Progress tracking. Based on the incoming, already-modified
`progress.md`, the PRES-2 return and committed verdict, and repository state at
`a5436162cd7a0c6bc1fdee3c60534928add756c7`. Mandatory sections, standing decisions and
pending actions are retained; closed history is compressed. This update performs no
engineering test, deployment, checkpoint closure, commit or push. Updated later the same day
for the Owner-ratified final-product lifecycle amendment; see active anchors and Session Log.*

---

## 1. Current Position

### Track B — capstone (the critical path)

**Foundation established.** The v1 product is released; CP-10, CP-15, CP-16 and CP-20
are landed, and GFS is admitted. PRES-1 is closed. Their detailed results and accepted
limitations remain in the [landing records and evidence tags](#where-the-history-lives).

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
| 3 | Presentation around v2 (4.3R), with CP-20 alongside | PRES-1 closed; PRES-2 landed and pushed, Space deployment and public acceptance pending |
| 4 | v3 weather pipeline (CP-20, 4.4D) | ✅ Done and landed |
| 5 | Three-block LightGBM (4.5) | ⬜ Not started |
| 6 | DDNN / TabPFN (4.6L → 4.6R → 4.6C) | ⬜ Not started |
| 7 | VRE generation and residual-load model (4.4V, optional) | ⬜ Not started |
| 8 | Recombination (4.8, optional, after 5–7) | ⬜ Not started |
| End | Fresh-data test (4.7T), then live run of the final model (CP-17 → CP-19), then public presentation and CV (4.3C/4.10R) | Reserved for the end |

**Active publication checkpoint: PRES-2 — LANDED / PUBLIC ACCEPTANCE INCOMPLETE.**
The [Integration verdict](docs/track-b/evidence/pres-2/integration.md) is PASS for the
local-ready milestone only. The Lead returned BLOCKED at the Owner publication gate;
the Owner subsequently explicitly instructed merge, commit and push, with no repeated tests.
That instruction was executed; it does not constitute a post-deployment PASS.

| Identity / step | Recorded state |
|---|---|
| Reviewed candidate | `d7d57e316a0afa198a2196bf4a2f1a3ac4a7c987` |
| Evidence tip | `871c0e27a3cba9f1b2d937a2482e5dfda7bbf9c7`, preserved by `evidence/pres-2` |
| Squash landing | `a5436162cd7a0c6bc1fdee3c60534928add756c7`, tagged `land/pres-2`; main and both tags pushed |
| Landing identity | Staged tree equalled the evidence-tip tree before commit; pre-existing `progress.md` changes preserved |
| Implemented | Twelve product subjects below the opening; v1→v2 and v2→v3 transitions; chart routes; F01–F04 repairs; companion documentation |
| Independent acceptance | Full local checklist mapped in the verdict and [acceptance matrix](docs/track-b/evidence/pres-2/acceptance.md); fresh-reader/editorial records present |
| Hugging Face | Reviewed PRES-2 bundle has **not been uploaded by this session** |
| Public acceptance P8 | Full public acceptance **not run**; a later anonymous HTML read matched the expected Pages hash, but no browser/demo acceptance or new CI-success claim follows |
| Reclamation | `gauntlet/pres-2` and its Lead worktree remain; checkpoint not closed |

**Next pending Track B checkpoint: finish PRES-2's publication/acceptance and reclamation.**
The [publication packet](docs/track-b/evidence/pres-2/publication-packet.md) is the continuation
source. No implementation restart or duplicate local test campaign is needed. The Owner's
no-repeat-tests instruction explains the unperformed P8 work; it is not a waiver of the
acceptance bar and does not turn an unobserved service into PASS.

**Next research checkpoint: CP-21, the first v3 extension — not authorized.** The extension
choice is still unanswered (see Blockers). Opening it requires a separately authorized
research amendment and complete brief. v21-r5 below defines the final product, not CP-21. CP-17–CP-19 remain reserved for the final model's freeze,
live operation and prospective evaluation. PRES-2 neither reopens PRES-1 nor promotes HG.

**Repository:**

- Main/last observed `origin/main`: `a5436162cd7a0c6bc1fdee3c60534928add756c7`.
- Retained Lead branch: `gauntlet/pres-2` at evidence tip `871c0e2`; worktree
  `.local/worktrees/pres-2`. Purpose: preserve the PRES-2 execution workspace pending closure.
  The squash leaves its 12 candidate/evidence commits outside main's ancestry; the evidence tag
  preserves them. No branch/worktree/ref was created or removed in this regeneration.
- Only `progress.md` was dirty on entry and is edited here; nothing is staged.
- Decoded GFS grids and CP-20 material stay under `.local/`
  ([artifact map](docs/track-b/local-artifacts.md)). Retain the reviewed PRES-2 bundle,
  screenshots and local records until public acceptance and disposition accounting finish.

**Public surfaces — distinguish a Git push from a verified deployment:**

| Surface | Last evidenced state / pending action |
|---|---|
| [GitHub repository](https://github.com/hrsi56/delu-day-ahead-forecast) | PRES-2 main and both preservation tags were pushed successfully |
| [Static report](https://hrsi56.github.io/delu-day-ahead-forecast/) | Anonymous HTML read during the subsequent Live-status discussion, 2026-09-29: HTTP 200 and SHA-256 `f36314e28811ed4b7ec41bc73dfd481ddb112815effabfc4e7b3ae74d8edab1d`, matching PRES-2. Byte identity only; public browser behaviour and full P8 still pending |
| [Static Space](https://huggingface.co/spaces/Yarden-Viktor/delu-day-ahead-forecast) ([direct app](https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/)) | Anonymous Hub API read 2026-09-29 11:01:53 UTC confirms PRES-1 revision `59d941825755bf73eabb7ff20e31124fee305755`, static/public/RUNNING. PRES-2 upload outstanding; metadata read is not bundle or browser verification |
| [MLflow on DagsHub](https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow) | Unchanged 23-run, six-route export verified during PRES-2; no upload needed; no post-push recheck claimed |

Expected PRES-2 Space bundle: `8007f0d2a9c09a8c2c3182745dac6b38956a9a0ad8f58541f32472b674d5bb4e`
(805 files, 44,164,910 bytes), preserved at `.local/artifacts/pres-2/space-wasm-8007f0d2/`
per the packet. Public closure of the later [independent review](docs/track-b/publication-postdeploy-independent-review-2026-09-29.md)'s
F01–F04 remains pending; local fixes are already reviewed and landed. Historical PRES-1
acceptance remains intact under its own effective rules.

**Scope outside Track B:** Track C was cancelled and moved out of this repository; no marketing
state is tracked here. Track A is inactive and has no position. The Owner's end-stage CV-use
decision remains a boundary, not an active workstream.

---

## 2. Setup State

- **ACTION-REQUIRED (Owner), pending since 2026-09-24:** restart the Claude desktop app, PyCharm
  and any terminal opened before the DagsHub token rotation. Until then those processes hold the
  revoked value. This item stays pending until the Owner confirms it. It matters before
  any old application is reused. PRES-1 F1 succeeded using the existing variables; that is
  evidence for the Lead process, not confirmation that every old application was restarted.

---

## 3. Strategic Anchors

- **Publication anchor:** [PUBLISH_RULES](docs/PUBLISH_RULES.md) **1.1**, Owner-ratified
  2026-09-29; SHA-256 `91eea445434718a163f03bcfd82e1db275a9d98311e76eb6cd1365f3707584f3`.
  A1–A6 continue; strengthened A7 and A8 govern future final-product rollout/daily operation.
  Historical PRES-2 remains governed by 1.0 (`03f106060d9a646ce0c0c986d2f5fb6549929f2ed7270f0c8678fbfd2293b3a3`),
  preserved at `evidence/pres-2:docs/PUBLISH_RULES.md`; PRES-1 retains Publication Standard v1.
- **Ratified research authority:** `capstone_v21.md` **v21-r5**, Owner-ratified 2026-09-29;
  SHA-256 `a4e178c30c555cc91dfbe338bbcf3e8776d67709d6dc4a72bc4f5892971003c9`. New §16 defines final-product identity,
  policy freeze, daily training and future-stage acceptance; it opens no checkpoint.
  Historical §§1–15 remain intact. CP-20 is closed under r4; its §15.7 authority stays spent.
  [Amendment record](docs/track-b/capstone_v21-r4-to-v21-r5-amendments.md).
- **Historical authorities:**

  | Authority | Governed | Where the exact bytes are |
  |---|---|---|
  | v21-r4 | CP-20 | `evidence/pres-2:capstone_v21.md` (`150bd53f…`) |
  | v21-r3 | CP-16 | `evidence/cp-16:capstone_v21.md` (`67d21768…`) |
  | v21-r1 | CP-15 | `evidence/cp-15:capstone_v21.md` (`44ea4e54…`) |
  | Original `capstone_v20.md` | CP-10 | `docs/track-b/anchors/cp-10-capstone_v20.md` |
  | `capstone_V6_8.md` | v1 | the file itself |

  Once the live anchor advances, closed checkpoints are reproduced from their `evidence/` tags.
- **Programme plan:** the [v3 plan handoff](docs/track-b/v3-plan-handoff-2026-09-22.md), with
  work items 4.0–4.10 and the decision register D1–D6. Navigation identity: `7fdd8205…`.
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
  - `שאלות תשובות.docx` has 36 entries (entry 36: frozen policy versus daily training and product presentation; entry 35: PRES-1 receipt).
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

- **Publication surface completion check, 2026-09-29.** Owner flagged stale Hugging Face and asked for MLflow coverage and guaranteed final-product delivery there. Anonymous Hub API confirmed PRES-1 revision `59d9418` at 11:01:53 UTC. Existing PUBLISH_RULES §§8/10.3/11 already require all-surface agreement and public verification; PRES-2's packet explicitly requires its Space upload and verifies an unchanged MLflow export. Added operational runbook §1a and packet §8 to make every release account for each surface: changed upload versus verified unchanged, publication-to-MLflow mapping, actual HF model/artifact/forecast identity and incomplete disposition until all required evidence exists. No duplicate MLflow experiment required for unchanged research; no promise of failure-free hosting. Final daily training must propagate to the hosted demo and be verified, not merely complete locally. No locked anchor, source, historical packet, credential, Git ref or external service changed; no deployment performed.
  - **Omission review:** all incoming state/decisions retained; only Space observation refreshed and continuation instructions strengthened under existing rules. API metadata evidence and incoming copies retained at `.local/artifacts/publication-surface-gate-2026-09-29/`. The task did not extend the spent Lockdown suspension.

- **Final-product rules ratified, 2026-09-29.** After specifying one final-model/product/demo/daily identity and product → methods → scientific results → business insights → comparison order, the Owner expressly approved the named task-scoped Lockdown suspension (“מאשר באופן מלא”). Established PUBLISH_RULES 1.1 A8/strengthened A7 and research v21-r5 §16, with the amendment record, programme/runbook/packet consistency and active hashes here. The daily-training default, explicit exception route, defined percentages, uncertainty and business evidence requirements are now binding for future final-product work. Historical research body and PRES-2 contract preserved. No model selected, code changed, tests rerun, service started, commit or publication performed.
  - **Omission review:** retained all incoming setup items, standing decisions, logs, blockers and future work. Updated active anchor identities and CP-21's no-longer-applicable “r5 next” wording; added the Owner's decision and future acceptance fields. Historical 1.0/r4 references remain dated. Clarified the Friday/Shabbat standing decision for manual work versus future authorized unattended daily coverage; recorded the preceding discussion's Pages byte-identity observation without claiming P8 acceptance. Required Q&A entry 36 added using the prescribed appender; no layout work. The task-scoped suspension expires at terminal return.

- **Progress regeneration, 2026-09-29 (this task).** Read the root router, Orchestrator regeneration/pruning contract, active-plan routing clauses, publication acceptance contract and PRES-2 evidence. Reconciled the return with the prescribed read-only Git packet checks; no engineering audit or product tests. Corrected stale “not started”, “only main”, “no repair implemented” and “CP-21 next” state. Preserved the incoming uncommitted decisions. Only `progress.md` changed; no stage, commit, push, deployment or reclamation.
  - **Omission review:** Setup State, Strategic Anchors, Standing Scope Decisions and Lessons retained verbatim. All unanswered questions, scheduled work and historical limitations retained. Closed foundation metrics/step-by-step PRES-1 history reduced to a Current Position summary and evidence links; prior Session Log entries compressed to one line each. Superseded PRES-2 launch routing replaced by the evidenced landing and outstanding P8/reclamation. The inactive Track A position and cancelled Track C status block reduced to a scope boundary under the scope-narrowed role header. No rule or acceptance criterion amended.
  - **Recovery:** incoming file, omission diff and review notes retained in `.local/artifacts/progress-regeneration-2026-09-29/`; this is local recovery material, not replacement evidence.
- **PRES-2 landing, 2026-09-29.** On the Owner's explicit merge/commit/push instruction, squash-landed reviewed evidence tree `871c0e2` as `a543616`; pushed main, `land/pres-2` and `evidence/pres-2` with required hooks enabled. Existing progress changes survived exactly. No product tests repeated, no Space upload or postdeploy acceptance; retained branch/worktree. This was a task-scoped mainline/publication instruction, not a standing governance exception.
- **PRES-2 return, 2026-09-29.** Lead returned BLOCKED solely at publication authority, with final-candidate Integration PASS at `d7d57e3` and evidence at `871c0e2`; the verdict maps local requirements and leaves P8 pending. Reported 1,088 passed / 7 skipped and reviewed exact bundle are prior evidence, not checks rerun by this Orchestrator. R1–R7 remain advisories; device/public-service limits remain in the verdict.
- **PRES-2 brief issued, 2026-09-29.** [Brief](docs/track-b/pres-2-execution-brief-2026-09-29.md) bound PUBLISH_RULES 1.0, migration revision 1, an approximately 32-hour timebox and complete local/public acceptance; supplied governance copies were immutable baseline inputs, and the original brief granted no public or mainline write.
- **Migration plan, 2026-09-29.** [Revision 1](docs/track-b/publish-rules-migration-plan-2026-09-29.md) mapped product subjects, predecessor comparisons, F01–F04 and A1–A6; kept frozen-versus-fold-5 SHAP, absent paired v2−v1 uncertainty and historical evidence preservation explicit; A7 deferred.
- **PUBLISH_RULES 1.0 established, 2026-09-29.** Owner's explicit task-scoped Lockdown suspension covered the publication anchor and its root registration/necessary state consistency; subjects 1–12 belong to the active product. Historical v1 rules/evidence and research authority preserved; the suspension ended at terminal return.
- **Preservation correction, 2026-09-29.** Recovered setup, anchors, decisions and logs omitted in `3cd7592` from `a067d2f`; corrected Q&A count to 35. This establishes why omission review must use the full incoming working copy.
- **PRES-1 closure, 2026-09-29.** Owner-delegated landing/push, Space redeploy and F6–F8 succeeded; initial 429 failures, effort/disk and device limits retained; tags verified and its branch/worktree reclaimed. [Landing record](docs/track-b/pres-1-landing-2026-09-29.md).
- **PRES-1 D5 reaffirmation, 2026-09-29.** Owner's exception covered that checkpoint's landing, exact Space deployment, postdeploy checks and closure only; no governance edits, guard bypass, repeated F1 or later-checkpoint authority.
- **PRES-1 receipt/F5, 2026-09-29.** Final independent PASS and delegated F5 accepted, entry 35 filed, unresolved publication-authority conflict carried until the separate D5 reaffirmation. [Receipt](docs/track-b/pres-1-receipt-2026-09-29.md).
- **Publication Standard v1 ratified, 2026-09-28.** D1–D3, D5 and D6 approved, D4 withdrawn, D7 optional; conformance brief issued and documents/state/Q&A 34 committed/pushed on Owner instruction. Exact in-force scope and decisions remain in standard §§16–17.
- **Standard derivation, 2026-09-28.** Independent advice and three-round review informed the [derivation record](docs/track-b/publication-standard-derivation-2026-09-28.md); the earlier release review was superseded, not used as an acceptance gate.
- **Earlier PRES-1 release review, 2026-09-28.** Candidate `af0abb0` was not ready to land; findings and the fix round remain in the [superseded review](docs/track-b/presentation-release-review-2026-09-28.md).
- **Presentation plan R3 approved/brief issued, 2026-09-24.** All nine §16 answers recorded, including naming, independent review, MLflow route and contribution text; MLflow template integration remains a separately authorized task, not an assumed completed edit.
- **Design review/R3, 2026-09-24.** [Review](docs/track-b/presentation-design-review-v2-2026-09-24.md) resolved conflicting states, SVG markup and visual grammar; subsequent ratification superseded the draft status.
- **External review/R2, 2026-09-24.** [Review](docs/track-b/presentation-review-and-corrections-2026-09-24.md) corrected units, gate order, evidence layers and MLflow claims; subsequent R3 superseded its pending approval.
- **Presentation plan R1, 2026-09-24.** Owner adopted one growing history page, v1–v3 now, MLflow backfill and publication as generations land; R1–R6 and end-stage CV boundary persist above.
- **Progress/credential rules, 2026-09-24.** Regenerated state under explicit instruction, ratified four standing decisions, added credential-value guard and synchronized stored variables without disclosure; closed research history compressed against `f704ac4:progress.md`, with open items retained.
- **CI restored, 2026-09-24.** Collection/precondition repairs and Python 3.12 pin landed; this historical success is not a PRES-2 public CI claim.
- **Credential exposure/rotation, 2026-09-24.** Owner rotated the exposed DagsHub token; no history rewrite by Owner decision. [Record](docs/track-b/credential-exposure-2026-09-24.md); old-application restart remains pending in Setup State.
- **CP-20 LAND, 2026-09-24.** `land/cp-20` / `evidence/cp-20` preserve the accepted research and weather attribution; no product promotion.
- **2026-09-23.** CP-20/v21-r4 ratified and issued; weather/content admission and CP-16 PASS/landing accepted; enduring limits are above and in tagged evidence.
- **2026-09-15/16.** v21 adopted; CP-15 resumed and landed with CP-10; repository/governance consolidated and the deliberate 2019 boundary recovered.
- **Earlier.** v1 foundation released and closed; see Current Position and preserved evidence tags.

---

## 6. Blockers / Open Questions

- **Final-product operating specification remains pending:** no final version designated and no
  daily system running. Future authorized work must fix numeric fit/issuance schedules, training
  windows, resources, percent-score formula/tolerance, source/outcome timing, business-use-case
  evaluation (if any), deployment/daily-demo design and Friday/Shabbat failure coverage. These
  implementation fields do not reopen the now-ratified product identity/order/daily-fit decision.

- **PRES-2 remains open:** exact Space bundle not uploaded, postdeploy checks and a new independent
  public verdict absent, Lead branch/worktree not reclaimed. The old Owner gate no longer blocks
  the Git steps already executed. Do not report the migration complete from local PASS or push.
- **PRES-2 advisories:** R1–R7 in the [Integration verdict](docs/track-b/evidence/pres-2/integration.md)
  remain recommendations, not release failures. They include transition question wording, startup
  timing for the new public bundle, product evidence links, data wording, carried editorial points,
  byte-count logging and clean-checkout reproduction order. P8 must measure the new cold start;
  no fresh public measurement is claimed here.

- **PRES-1 remains closed under its landing record.** F6–F8 passed under the explicit Owner
  exception. Initial HF/DagsHub rate-limit failures and successful retries are recorded.
  Historical active-hour total and added-disk baseline remain unavailable, not retroactively
  certified compliant. Required tags preserve all evidence.
- **Later independent public review: four open v1 conformance findings.** See the
  [2026-09-29 report](docs/track-b/publication-postdeploy-independent-review-2026-09-29.md):
  F01 unnamed demo controls; F02 favicon 404; F03 startup measurement metadata hidden; F04 visible
  fairness note omits the day count. These IDs belong to this new review, not the earlier F01–F04
  below. All four fixes are implemented, independently accepted locally and landed in PRES-2;
  public closure still requires the Space deployment and P8 evidence. New rules are not applied
  retrospectively to turn PRES-1 advisories into violations.
- **Open question, asked 2026-09-24: which extension opens CP-21?** It persists until answered.
  The recommended order:
  1. 4.6, starting with licence and resource entry for TabPFN, with DDNN as its direct
     comparator;
  2. then 4.4V, VRE modelling from the retained grids;
  3. then 4.8, recombination.

  4.5 is recommended only as an extra arm for 4.8.
- **CP-20's analysis and reference passes are exhausted.** Any further CP-20 scoring needs a cap
  decision.
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
  README shipped; the landing post-deploy checks passed. This historical disposition does not
  close the different F01–F04 in the later independent review above.
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

- **[2026-09 / next publication continuation]** Resume PRES-2 from the
  [publication packet](docs/track-b/evidence/pres-2/publication-packet.md), not its initial launch
  instructions. Git landing/push are done. Remaining work is exact Space upload, P8 service
  identity/behaviour evidence and a new independent postdeploy review, followed by documented
  closure/reclamation. Preserve historical review files, failed attempts, both tags and reviewed
  bundle. Use runbook §1a and packet §8 to account for every surface; PRES-2's existing packet
  already requires HF deployment despite its unchanged MLflow export. No release-complete claim
  follows from Git push. This tracking task performs no external write.
- **[Every new publication brief]** Pin PUBLISH_RULES 1.1 and incorporated source hashes;
  retain A1–A6 and apply A7/A8 at their final-product/live triggers. PRES-2 continuation keeps
  its original 1.0 contract. Predecessor comparisons and descriptive chart routes remain;
  v2→v3 reuses existing weather evidence, and v1's archive stays historical.
- **[Final-product designation / CP-17–19]** Carry research v21-r5 §16, publication 1.1 §§5/7.2,
  runbook §7b and packet §5d. Complete the numeric operating/scoring manifest, publish one
  product/demo policy at authorized rollout, and distinguish daily live evidence from completed
  prospective evaluation. No current research generation is promoted by this documentation task.
- **[2026-10, from the 19th]** `ubuntu-latest` moves to Ubuntu 26. CI is pinned to Python 3.12;
  check the first run after the move.
- **[After PRES-2 / next research brief]** Apply the 2026-09-24 standing decisions:
  - HG's information set, with HG itself as a reference on identical rows;
  - no data after 2026-04-07;
  - a TabPFN run needs 4.6L's licence-use table first;
  - positive controls must survive the model's own transforms (see Lessons).
- **[After publication / governance follow-up]** PRES-1 W16/template proposals remain in its
  preserved return for a separate appropriately authorized governance task; no locked-template
  amendment is certified here. PRES-2's runbook/packet updates do not establish that every W16
  proposal was adopted. Retain the unresolved CP-21 choice. Do not repeat F1 or reopen PRES-1.
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
    publication chains; PRES-2 still awaits deployment acceptance and reclamation;
  - `archive/cp-0-attempt-1`, `archive/weather-admission-20260923` and
    `archive/cp15-cp16-content-20260923`.

  Squash landings do not contain the candidate SHAs; only the tags preserve them. Verdicts are in
  `docs/track-b/evidence/<cp>/`.
- **Publication evidence:** [PRES-1 landing](docs/track-b/pres-1-landing-2026-09-29.md),
  [later independent public review](docs/track-b/publication-postdeploy-independent-review-2026-09-29.md),
  [PRES-2 Integration](docs/track-b/evidence/pres-2/integration.md),
  [acceptance](docs/track-b/evidence/pres-2/acceptance.md) and
  [publication packet](docs/track-b/evidence/pres-2/publication-packet.md).
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
  - the programme plan and its reviews in `docs/track-b/`.
- **Defect ledger:** `docs/track-b/cp-0-defects.md`, closed 2026-09-14.
- **v1 results:** `docs/cp2-model-report.md` and `reports/cp2/`.
- **Local recovery material:** `.local/`, per the [artifact map](docs/track-b/local-artifacts.md).
  It is not an off-device backup.
- **Everything else:** `git log`.
