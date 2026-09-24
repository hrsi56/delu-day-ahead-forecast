# Programme state — DE-LU day-ahead forecasting

*Orchestrator-owned. **Regenerated 2026-09-24 at the Owner's explicit request** under the
`orchestrator-role.md` regeneration contract: mandatory skeleton, closed history compressed,
omission review in the Session Log. The previous full text is `f704ac4:progress.md`.*

---

## 1. Current Position

### Track B — capstone (the critical path)

**Foundation established.** v1 is released and closed. Four checkpoints have landed since
(CP-10, CP-15, CP-16, CP-20), and the weather archive is admitted. Tags preserve every reviewed
chain (see *Where the history lives*).

| Stage | Result | Tags |
|---|---|---|
| v1: M1–M3.5 / CP-1 … CP-3B, REL-1 | Released; public surfaces below | `land/cp-0` … `land/cp-3b` with matching `evidence/` tags |
| CP-10 (v20 M4 calibration) | Engineering PASS; landed with CP-15; no promotion | via `evidence/cp-15` |
| CP-15 (v21-r1 adaptive feasibility) | Engineering PASS. Product `NOT_DEMONSTRATED`: A1 is the best challenger, B2 has better primary scores, none qualified | `land/cp-15`, `evidence/cp-15` |
| CP-16 (v21-r3 existing-input v2) | Research PASS. H−B2 exploratory joint improvement; H−P no demonstrated joint preference; H and P miss §8 criteria 1–2 | `land/cp-16`, `evidence/cp-16` |
| Weather admission (4.1) | GFS ADMIT for all five folds; ICON NOT_ADMITTED | `reports/weather-admission/` |
| CP-20 (v21-r4 direct-GFS ablation, 4.4D) | Research PASS; HG−H0 observed joint improvement | `land/cp-20`, `evidence/cp-20` |

**Current best research policy: HG.** HG is the CP-16 V2-H policy (the fixed B2/A1 LEAR blend
with hour-aware intervals) plus three frozen GFS features: mean 10 m wind speed, mean 100 m wind
speed and mean DSWRF over 47–55.25°N, 5.5–15.5°E, each with a missing indicator.

**HG − H0** (H0 is the same policy without weather):

| Measure | Difference | 95% interval |
|---|---|---|
| ΔS_WIS | −0.0838 | [−0.1044, −0.0655] |
| ΔS_MAE | −0.0783 | [−0.1006, −0.0570] |

- All five folds favour HG. The fold-3 MAE interval crosses zero.
- **Scores normalized to the similar-day naive** (equal-fold, B0 = 1.00; lower is better):

  | Policy | S_MAE | S_WIS |
  |---|---|---|
  | HG | 0.566 | 0.532 |
  | H0 | 0.644 | 0.616 |
  | B2 | 0.658 | 0.639 |
  | v1 (B1) | 1.052 | 0.986 |

- As diagnostics, HG meets all six original §8 criteria, the first evaluated policy to do so.
  H0 misses criteria 1–2.
- Every result is `development_post_selection`. No promotion, product qualification or live
  eligibility follows. The full record is the [CP-20 landing record](docs/track-b/cp-20-landing-2026-09-24.md).

**Programme stages** (the Owner's table, updated 2026-09-24):

| # | Stage | Status |
|---|---|---|
| 1 | NWP archive-depth gate (4.1) | ✅ Done: GFS admitted |
| 2 | v2 build and causal fix (CP-16, 4.2) | ✅ Done and landed |
| 3 | Presentation around v2 (4.3R), with CP-20 alongside | 🟡 [Local draft](docs/track-b/research-content/cp15-cp16-update.md). [Plan](docs/track-b/presentation-and-tracking-plan-2026-09-24.md) approved 2026-09-24; phases A–E not started |
| 4 | v3 weather pipeline (CP-20, 4.4D) | ✅ Done and landed |
| 5 | Three-block LightGBM (4.5) | ⬜ Not started |
| 6 | DDNN / TabPFN (4.6L → 4.6R → 4.6C) | ⬜ Not started |
| 7 | VRE generation and residual-load model (4.4V, optional) | ⬜ Not started |
| 8 | Recombination (4.8, optional, after 5–7) | ⬜ Not started |
| End | Fresh-data test (4.7T), then live run of the final model (CP-17 → CP-19), then public presentation and CV (4.3C/4.10R) | Reserved for the end |

**Next pending Track B checkpoint: CP-21, the first v3 extension.** It is not authorized yet:
the Owner has not chosen the extension (see Blockers). Opening it needs a v21-r5 amendment and a
CP-21 brief that apply the standing decisions below. CP-17–CP-19 stay reserved for the final
model's freeze, live operation and prospective evaluation.

**Repository:**

- `main` is the only branch and checkout.
- Public CI (`invariant-tests`) has been green since `566335d`.
- Decoded GFS grids and CP-20 working material are retained under `.local/`
  ([artifact map](docs/track-b/local-artifacts.md)).

**Public surfaces (v1):**

| Surface | What it is |
|---|---|
| [Static report](https://hrsi56.github.io/delu-day-ahead-forecast/) | The primary link; makes zero network calls |
| [Static Space](https://huggingface.co/spaces/Yarden-Viktor/delu-day-ahead-forecast) ([app direct](https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/)) | The champion's boosters in the browser, bitwise equal to the frozen artifact |
| [MLflow on DagsHub](https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow) | Every decision-bearing run, anonymously readable |

README and site describe v1 and CP-15. CP-16 and CP-20 are not yet on any public surface.

### Track C — marketing

Cancelled 2026-09-15; no outreach or CV surfaces live in this repository. The public site shows
v1–v3 now and grows with each generation. CV use comes at the end, after the holidays (Owner,
2026-09-24).

### Track A

No optional learning block is active.

---

## 2. Setup State

- **ACTION-REQUIRED (Owner), pending since 2026-09-24:** restart the Claude desktop app, PyCharm
  and any terminal opened before the DagsHub token rotation. Until then those processes hold the
  revoked value. This item stays pending until the Owner confirms it.

---

## 3. Strategic Anchors

- **Ratified authority:** `capstone_v21.md` **v21-r4** (§15, CP-20), ratified 2026-09-23, SHA256
  `150bd53fa15067b1d138c95d0912f86a1e92ce74092059be09034758c1926167`. CP-20 closed under it, and
  its §15.7 packaging authority ended at landing.
- **Historical authorities:**

  | Authority | Governed | Where the exact bytes are |
  |---|---|---|
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
  - **Checks:** `make verify` binds the cross-surface claim set. URLs are checked by the test
    suite and `scripts/check_links.py`.
  - **Secret guard:** `.githooks/` together with `scripts/secret_guard.py`. It is enabled locally
    with `git config core.hooksPath /Users/djourno/Downloads/PJM/.githooks`, and a fresh clone
    must enable it again.

---

## 4. Standing Scope Decisions

These carry forward indefinitely. Each changes only by explicit Owner ratification, named in the
Session Log.

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
- **Presentation and tracking rules (plan R1–R6, approved 2026-09-24):**
  - v1's holdout moves into the v1 chapter and is not deleted;
  - agents build the page and charts from data, and the Owner reviews visually before any push;
  - version numbers go only to adopted models;
  - the repository is the source of truth: MLflow mirrors it, and the page never reads MLflow;
  - checkpoints track locally and publish to MLflow at landing;
  - the Model Registry holds only runnable, frozen policies.
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

- **Owner observance: no scheduled work on Friday or Shabbat.** Any operational schedule must
  resolve this explicitly.
- **Reasoning capture is active** (`AGENTS.md` § Interview-answer capture).
  - Only the Orchestrator files entries, through `scripts/qa_append.py`; the Lead names triggers
    in its return.
  - `שאלות תשובות.docx` has 33 entries.
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

- **Presentation and tracking plan, 2026-09-24.** The Owner decided on one scrolling history page
  (newest first, live at the top at the end), showing v1–v3 on the site now, and MLflow as the
  visible cross-version tool, with v2/v3 backfilled and future work tracked.
  - Reviewed the live page, its generator, the site-shaping commits (155b0f8, 8341fba, 7f16f4e,
    99c9250, 5b94b8f) and the public MLflow state: only `delu-cp2`, with 55 runs, and the
    `champion` registry entry.
  - Drafted the [plan](docs/track-b/presentation-and-tracking-plan-2026-09-24.md): phases A–E,
    14 invariants and the MLflow tracking specification.
  - **Standing-decision amendment:** the public site is now updated as generations land; only CV
    use stays at the end.
  - The Owner approved the plan with R1–R6 as written, and they were recorded as standing rules.
    The plan and this state were committed and pushed at the Owner's instruction.
  - No site, README, MLflow or engineering change was made.

- **Progress regeneration, credentials rule and secret guard, 2026-09-24.** Done at the Owner's
  explicit request.
  - **This file:** regenerated under the contract. The Owner ratified four standing decisions:
    same information and opponent, no data after 2026-04-07, the final sequence and the
    credentials rule. The weather-source decision was amended to match the ratified GFS
    admission.
  - **`AGENTS.md`:** added § Credentials, under a task-scoped Lockdown suspension granted by the
    Owner's instruction.
  - **Secret guard:** added the value-based guard (`scripts/secret_guard.py`, `.githooks/`,
    `tests/test_28_secret_guard.py`) and enabled it locally.
  - **Tokens:** mirrored `ENTSOE_API_TOKEN` and `HF_TOKEN` from `launchctl` into `~/.zshrc`.
    No value was displayed.
  - **Omission review, pruned as closed history:** the CP-10, CP-15 and CP-16 receipts,
    handoffs and usage totals; the v21-r1, v21-r2 and v21-r3 issuance identity tables; the
    2026-09-15/16 consolidation, correction, validation and research narratives, including the
    live-namespace guard re-run and the v20-r1 draft; weather-intake and CP-20 issuance
    details; and superseded routing. The landings resolved all of these. They are preserved at
    `f704ac4:progress.md`, in the tags and in the landing records.
  - **Omission review, resolved:** the CP-16 test debt and CI, the ACI implementation concern,
    the CP-10 disposition and the token rotation.
  - **Carried:** every active item — anchors, standing decisions, open questions, the next
    checkpoint and the pending action.
- **CI restored, 2026-09-24.** `pytest.ini` (importlib mode) and `tests/cp16/conftest.py` fixed
  collection and test preconditions without touching any hash-bound file. CI is pinned to Python
  3.12, and public CI has been green since `566335d` (511 passed, 7 skipped).
- **DagsHub token exposure and rotation, 2026-09-24.** A Critic pytest log in the CP-20 evidence
  published the token. The Owner rotated it and local configuration was synchronized. No other
  secret appears in any ref. By Owner decision there is no history rewrite
  ([record](docs/track-b/credential-exposure-2026-09-24.md)).
- **CP-20 receipt, LAND, reclamation and push, 2026-09-24** (delegated by the Owner).
  `land/cp-20` = `f450bc1` and `evidence/cp-20` = `a7a9b2e`. The pasted Owner decisions O1–O4,
  A1 and S1 were confirmed, and the weather attribution was added to `DATA-LICENSE.md`.
- **2026-09-23:**
  - CP-20 ratified as v21-r4, revised (per-cell wind speed; 120 machine-hours) and issued.
  - Weather admission and the CP-15/16 content accepted.
  - CP-16 PASS receipt, then an Owner-delegated LAND with repository consolidation.
- **2026-09-15/16:**
  - v21 adopted.
  - CP-15 blocked, resumed, passed and landed with CP-10.
  - The repository consolidated to one checkout, with project-local containment.
  - Governance reconciled and the 2019 boundary recovered.
- **Earlier:** v1 complete and closed (CP-0 … CP-3B, REL-1).

---

## 6. Blockers / Open Questions

- **Presentation and tracking plan approved 2026-09-24; three §13 questions remain open.** They
  are in the [plan](docs/track-b/presentation-and-tracking-plan-2026-09-24.md):
  1. public names for future generations;
  2. the executor, and whether an independent claim check is required before the push;
  3. whether the MLflow landing step goes into the templates now (this needs a suspension) or is
     carried in briefs.

  Phase C (MLflow) must run from a process that holds the rotated token.
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

- **[2026-10, from the 19th]** `ubuntu-latest` moves to Ubuntu 26. CI is pinned to Python 3.12;
  check the first run after the move.
- **[Next extension brief]** Apply the 2026-09-24 standing decisions:
  - HG's information set, with HG itself as a reference on identical rows;
  - no data after 2026-04-07;
  - a TabPFN run needs 4.6L's licence-use table first;
  - positive controls must survive the model's own transforms (see Lessons).
- **[Next]** Run the approved presentation and tracking plan's phases A–E. Phase C runs after the
  Owner restarts the apps, so it uses the rotated token.
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
  - `archive/cp-0-attempt-1`, `archive/weather-admission-20260923` and
    `archive/cp15-cp16-content-20260923`.

  Squash landings do not contain the candidate SHAs; only the tags preserve them. Verdicts are in
  `docs/track-b/evidence/<cp>/`.
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
