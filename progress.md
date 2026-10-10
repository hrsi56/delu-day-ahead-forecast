# Programme state — DE-LU day-ahead forecasting

*Orchestrator-owned. Regenerated in full on 2026-09-30 at the Owner's explicit request ("תוציא
progress חדש ומעודכן"), under `orchestrator-role.md` § The regeneration contract. The work ran in
a Claude Code cloud session: a fresh GitHub clone, without the Owner's `.local/` material,
credentials or local branches. The incoming file is `4892d57:progress.md`, the head of
[hrsi56/delu-day-ahead-forecast#1](https://github.com/hrsi56/delu-day-ahead-forecast/pull/1). The
omission diff against it is summarized in the Session Log. The task ran CP-21's read-only receipt
checks and filed Q&A entries 39–42. It ran no fit, data retrieval, deployment or MLflow write.
Its commit, push and the squash merge of PR #1 follow the Owner's explicit, task-scoped
instructions of 2026-09-30. The file was updated in place the same day, through PR #2, for the
Owner's amendment of "same information, same opponent" and the retirement of the session
branch. It was updated in place again the same day, through a third pull request, for the
final-product Space plan (v21-r8 §19, PUBLISH_RULES 1.2) and the Owner's completion of CP-21's
reclamation and the session-branch retirement. It was updated in place once more that evening,
in a local Orchestrator session on the Owner's machine, for the issue of the PRES-3 brief, and
on 2026-10-01 for PRES-3's return, landing, deployment and closure. It was updated in place again
on 2026-10-01 for the Owner's CP-22 decisions, the ratification of v21-r9 and PUBLISH_RULES 1.3,
and the issue of the CP-22 brief. Its commit and push follow the Owner's explicit, task-scoped
instruction of 2026-10-01. It was updated in place again on 2026-10-04 for CP-22's receipt, the
Owner's decision that v4 stays as it is, the landing and reclamation, the 4.8 note and the v4
wording fix. That commit and push follow the Owner's explicit instruction of 2026-10-04. Later
that day it was updated again for the automation tools, the branch cleanup, the ratification of
v21-r10 (CP-23, DDNN) and the programme order. That commit and push follow the Owner's
instructions of the same day. That evening it was updated for CP-23's grant and brief, and then
for CP-23's receipt, the Owner's landing and its closure. On 2026-10-05 it was updated for the
ratification of v21-r11 (CP-24, DDNN-2) and CP-24's issue, under the Owner's delegation of
2026-10-04 ("תמשיך באופן חופשי ומלא עד דוח ובקשת LAND"). Those commits and pushes follow
that delegation. On 2026-10-11 it was updated in place for CP-24's pause, the Owner's handover
to a new Orchestrator session, the continuation, the receipt, the Owner's landing and CP-24's
closure. That commit and push follow the Owner's instruction.*

---

## 1. Current Position

### Track B — capstone (the critical path)

**Foundation established.** The v1 product is released. CP-10, CP-15, CP-16, CP-20, CP-21, CP-22,
CP-23 and CP-24 are landed, GFS is admitted, and PRES-1, PRES-2 and PRES-3 are closed. PRES-3
published v4 on every surface on 2026-10-01. Since then three checkpoints closed:

- CP-22 re-examined v4 and made no replacement (2026-10-04);
- CP-23 tested a DDNN member and did not adopt v5 (2026-10-04);
- CP-24 tested DDNN-2 and **adopted v5 in research** (landed 2026-10-11).

Their detailed results and accepted limitations remain in the
[landing and closure records and evidence tags](#where-the-history-lives).

**Released product: frozen v1. Research base: v5, adopted in research by CP-24 (landed
2026-10-11).** No public surface shows v5 yet; the published research headline is still v4.

- **What v5 is.** v5 = (2/3)·HG + (1/6)·L + (1/6)·DDNN-2: v4 with half of LightGBM's third given
  to DDNN-2, a NumPy DDNN with day-level rows and 24 × 4 Johnson SU outputs. HG's hour-aware
  interval layer is re-estimated on v5's own errors. The weight is fixed, never estimated.
- **Why it was adopted.** On the same 10,747 development hours it met all five conditions of the
  pre-registered rule `cp24-adoption` against v4: S_MAE −2.49% and S_WIS −2.36%, with 97.5%
  intervals [−3.04%, −1.68%] and [−2.86%, −1.62%], all six §8 diagnostics, a complete valid
  evaluation, no fold decisively worse, and the 0.5% practical size.
- **What it does not show.** DDNN-2 alone was −10.67% S_MAE and −15.53% S_WIS against v4, but it
  was never eligible, so that is descriptive. Leakage was ruled out at all 636 origins (below).
- **Evidence class.** `development_post_selection`, and the second DDNN decision on these five
  folds. No promotion, product qualification or Live eligibility; 4.7T carries the protection.
  Exact values: the CP-24 [return](docs/track-b/evidence/cp-24/checkpoint-return.md) and
  [verdict](docs/track-b/evidence/cp-24/integration.md).

**v4 (HGL) is now the retained comparator.** It was adopted in research on 2026-09-30 and kept as
it is after CP-22 (Owner, 2026-10-04).

- **What v4 is.** v3's two LEAR components plus a three-block LightGBM member at one-third
  weight (the mean of raw and normalized block models), with v3's hour-aware interval layer
  re-estimated on v4's own errors.
- **Why it was adopted.** On CP-20's 10,747 development hours it met all four conditions of the
  pre-registered rule `cp21-adoption`: S_MAE −5.3% [−6.4%, −4.0%] and S_WIS −5.0% [−6.0%, −3.8%]
  against v3, all six §8 diagnostics, a complete valid evaluation, and no fold decisively worse.
- **What it does not show.** The block split itself, three blocks against one pooled LightGBM,
  showed no demonstrated joint preference: the gain came from the blend. HGL's MAE on the
  17-day peak was 50.1 against v3's 47.5 EUR/MWh (descriptive).
- **What CP-22 added.** Removing the split showed no demonstrated difference overall. It was
  decisively worse in fold 4 (summer 2025), though, so the rule kept v4. Since 2026-10-04 the
  report and README name v4's addition "a LightGBM forecaster", and say that the gain comes from
  the combination, not from the split. The registry name is unchanged
  ([CP-22 landing record](docs/track-b/cp-22-landing-2026-10-04.md)).
- **Evidence class.** `development_post_selection`: no promotion, product qualification or Live
  eligibility. CP-15's product result remains `NOT_DEMONSTRATED`. Exact values: the CP-21
  [return](docs/track-b/evidence/cp-21/checkpoint-return.md) and
  [verdict](docs/track-b/evidence/cp-21/integration.md).
- **v3 (HG) stays a retained reference.** It is CP-16's V2-H central-blend/hour-aware policy
  plus the admitted GFS wind and radiation features; its scores and fold qualifications are in
  the [CP-20 landing record](docs/track-b/cp-20-landing-2026-09-24.md).

**Programme stages** (Owner's sequence, current state 2026-10-11):

| # | Stage | Status |
|---|---|---|
| 1 | NWP archive-depth gate (4.1) | ✅ Done: GFS admitted |
| 2 | v2 build and causal fix (CP-16, 4.2) | ✅ Done and landed |
| 3 | Presentation around v2 (4.3R), with CP-20 alongside | ✅ PRES-1 and PRES-2 closed |
| 4 | v3 weather pipeline (CP-20, 4.4D) | ✅ Done and landed |
| 5 | Three-block LightGBM (4.5) | ✅ CP-21 landed 2026-09-30: v4 adopted in research. Published by PRES-3, closed 2026-10-01 |
| 5a | v4 re-examined (CP-22; [v21-r9 §20](capstone_v21.md)) | ✅ Closed 2026-10-04: PASS, no replacement (R and M failed condition 4 on fold 4); the Owner kept v4 as it is; landed as `land/cp-22` ([landing record](docs/track-b/cp-22-landing-2026-10-04.md)). The v4 wording on the report and README was corrected the same day |
| 5b | Checkpoint automation ([plan](docs/automation-plan.md) items 2, 1, 5, 3, 4, 8) | ✅ Done 2026-10-04 (`42e4ceb`). Items 6 and 7 deferred to the next publication, with a binding reminder |
| 6 | DDNN, written in NumPy only: CP-23, 4.6L → 4.6R → 4.6C ([v21-r10 §21](capstone_v21.md)) | ✅ CP-23 closed 2026-10-04: PASS; DDNN passed 4.6L, the correctness checks and 4.6R; v5 not adopted (`cp23-adoption` condition 1); landed as `land/cp-23` ([landing record](docs/track-b/cp-23-landing-2026-10-04.md)). DDNN-2 follows as CP-24 (row 6a) |
| 6a | DDNN-2: CP-24, a literature-faithful DDNN behind a pre-fold gate ([v21-r11 §23](capstone_v21.md)) | ✅ CP-24 closed 2026-10-11: PASS; DDNN-2 passed 4.6L′, the correctness checks, 4.6R′ and the pre-fold gate in one round; **v5 adopted in research** in scored attempt 1 (`cp24-adoption`, all five conditions); leakage ruled out at all 636 origins; landed as `land/cp-24` ([landing record](docs/track-b/cp-24-landing-2026-10-11.md)) |
| 7 | Comprehensive data-admission research, immediately after DDNN, with 4.4V (VRE generation and residual load) ([v21-r10 §22](capstone_v21.md)) | ⬜ Not started. Scope filed 2026-10-04 (Notes, [Data admission research]) |
| 8 | Recombination (4.8), with a NumPy meta-learner and per-block weights among its arms | ⬜ Not started. Filed 2026-10-04 (Notes, [4.8]) |
| End | Fresh-data test (4.7T), then live run of the final model (CP-17 → CP-19), then public presentation and CV (4.3C/4.10R) | Reserved for the end |

**No Track B checkpoint is active.** Under v21-r10 §22 the next stage is 7, the data-admission
research with 4.4V. The Owner has not yet chosen what opens next. Any publication of v5 first
needs the Owner's §23.12 decisions (Blockers).

**CP-24 is closed** ([landing record](docs/track-b/cp-24-landing-2026-10-11.md)). It ran under
[v21-r11 §23](capstone_v21.md), from the issued brief `a3f11470…` and the continuation brief
`5960b908…`.

- **Status.** PASS, with an Integration PASS at `7949a98`. The evidence tip is `05b7e61`
  (`evidence/cp-24`), and the landing is `05e6015` (`land/cp-24`).
- **Entry and gate.** DDNN-2 passed 4.6L′, the §23.7 correctness checks and 4.6R′. The pre-fold
  gate (G0–G3) passed in round 1, and S1 froze that design.
- **`cp24-adoption`: v5 is adopted** in scored attempt 1, against v4:

  | Score | v5 − v4 | Share of v4, 97.5% |
  |---|---|---|
  | ΔS_MAE | −0.0133 [−0.0166, −0.0091] | −2.49% [−3.04%, −1.68%] |
  | ΔS_WIS | −0.0119 [−0.0147, −0.0084] | −2.36% [−2.86%, −1.62%] |

  No fold is decisively worse. No attempt 2 ran, because an adoption ends the attempts.
- **Leakage, ruled out at full coverage.** The committed controls proved the masks at only two
  origins, too few for a member this strong. The continuation refitted the frozen ensemble at all
  636 warm-up and evaluation origins with every outcome on or after the delivery day destroyed.
  All 636 were bit-identical, a planted one-day leak was caught in 5 of 5 folds, and a D−1 price
  change moved the forecast at 22 of 22 origins.
- **The run.** The usage limit stopped the first Lead three times on 2026-10-05, the last time
  with its nested Critic mid-review. The Owner handed the work to a new Orchestrator session,
  which issued a continuation. The continuation Lead (about 3.5 active hours, about 8 in all):
  - repaired a base-tree test that would have turned `main` red after the LAND;
  - extended the leakage controls;
  - closed the two unfinished reviews.

  Critic 3 failed the candidate for reporting ratio intervals at 95% only. The repair derived the
  97.5% intervals from the stored draws, and Critic 4 passed.
- **Resources.** All within §23.11, with no raise. 16,436 of 40,000 DDNN-2 fits and 18.9 of 150
  machine-hours. The reference passes are spent (3 of 3).

**CP-23 is closed** ([landing record](docs/track-b/cp-23-landing-2026-10-04.md)). It ran under
[v21-r10 §21](capstone_v21.md), from the brief `33f6b412…`.

- **Status.** PASS, with an Integration PASS at `f9a737e`. The evidence tip is `928bc13`
  (`evidence/cp-23`), and the landing is `03c5b64` (`land/cp-23`).
- **Entry.** DDNN passed every gate:
  - 4.6L permitted research use;
  - the NumPy-only audit, the gradient checks and 26 of 26 PyTorch reference checks passed;
  - 4.6R passed.
- **`cp23-adoption`: v5 is not adopted,** at condition 1, against v4:

  | Score | v5 − v4 | Share of v4 |
  |---|---|---|
  | ΔS_MAE | +0.0064 [−0.0016, +0.0149] | +1.2% |
  | ΔS_WIS | +0.0071 [−0.0009, +0.0138] | +1.4% |

  Fold 3 is also decisively worse in MAE.
- **Descriptive results:**
  - DDNN alone is jointly worse than v3 and v4.
  - As v3's third member it gives −2.5% / −2.1%, against LightGBM's −5.3% / −5.0%.
  - LightGBM still adds once DDNN is present.
- **Two defects in the Orchestrator's anchor and brief:** the PUBLISH_RULES pin, and PyTorch in the
  root `uv.lock`. The Owner ruled on both during the run.

**CP-22 is closed** ([landing record](docs/track-b/cp-22-landing-2026-10-04.md)). It ran under
[v21-r9 §20](capstone_v21.md), from the brief `563f64f3…`.

- **Status.** PASS, with an Integration PASS at `29d8d38`. The evidence tip is `8daf7d0`
  (`evidence/cp-22`), and the landing is `ebb7d42` (`land/cp-22`).
- **`cp22-replacement`: no replacement.**
  - R (one pooled normalized LightGBM averaged over four capacities) and M (the split removed)
    were both non-inferior to v4 overall:

    | Policy | ΔS_MAE | ΔS_WIS |
    |---|---|---|
    | R | +0.0011 | +0.0010 |
    | M | −0.0013 | −0.0008 |

    All four intervals span zero. Both met all six §8 diagnostics.
  - Both failed condition 4. Fold 4 (2025-05-01..07-29) is decisively worse than v4:

    | Policy | Fold-4 MAE (EUR/MWh) | Fold-4 WIS (EUR/MWh) |
    |---|---|---|
    | R | +0.31 [0.15, 0.42] | +0.18 [0.10, 0.23] |
    | M | +0.20 [0.05, 0.33] | +0.11 [0.02, 0.20] |

  - The two layer rules did not apply, because there was no winner W.
- **Descriptively:**
  - No ladder step shows a demonstrated preference; v4's gain comes from adding the member.
  - The dynamic interval layer reacted to the 2022 peak in 4 days rather than 12. It widened the
    intervals by about 15%, though, and worsened S_WIS by about 4.4% on v4 and on v3.
  - PN's capacity selection is mostly noise, with a flip rate of 0.54.
- **The Owner's decision, 2026-10-04:** "v4 נשאר כפי שהוא". PRES-4's replacement plan does not
  start, because its entry condition 3 is unmet.
- **Records:**
  - the [amendment record](docs/track-b/capstone_v21-r8-to-v21-r9-amendments.md);
  - the unexecuted [PRES-4 plan](docs/track-b/cp-22-publication-plan-2026-10-01.md);
  - the [landing record](docs/track-b/cp-22-landing-2026-10-04.md), which also records the v4
    wording fix.

- **PRES-3 is closed** ([closure record](docs/track-b/pres-3-closure-2026-10-01.md)).
  - v4 is the research headline on the report and the README. Its chapter and the v3 → v4
    transition are published, and the planned list carries 4.6 as DDNN alone, against v4.
  - MLflow carries `cp21` and its four children. The Space serves the reviewed bundle at
    revision `0331088`, still v1, without `style.css`.
  - The independent post-deployment review was waived by the Owner for PRES-3 only. The
    receipt rests on byte identity and the automated public records.
- **Under the standing rule,** amended 2026-09-30, DDNN gets v4's information and faces v4 on
  identical rows, with v3 as a reference. Since CP-22 made no replacement, v4 here means the
  three-block construction.
- **The final product.** CP-17–CP-19 stay reserved for the final model. §16 defines the final
  product, and §19 with PUBLISH_RULES A9 defines its Space; the
  [final-product Space plan](docs/track-b/final-product-space-plan-2026-09-30.md) carries their
  checklist into the CP-17 and CP-18 briefs.

**Repository**, as verified on the Owner's machine on 2026-10-11:

- **`main` = `origin/main`** at the commit that carries this update. Below it:
  - `05e6015` = `land/cp-24`, CP-24's squash landing by the Owner;
  - `7ff6a50`, the Owner's work-availability amendment (v21-r12, PUBLISH_RULES 1.4);
  - `522d7ea`, the record of CP-24's issue;
  - `76ed485`, the v21-r11 ratification;
  - `09eacd1`, CP-23's closure records;
  - `03c5b64` = `land/cp-23`, CP-23's squash landing by the Owner;
  - `a4acd79`, the record of CP-23's grant;
  - `3f7aaf2`, the v21-r10 ratification;
  - `42e4ceb`, the automation tools;
  - `6483324`, CP-22's closure records;
  - `b194c72`, the v4 wording fix;
  - `ebb7d42` = `land/cp-22`, CP-22's squash landing by the Owner;
  - `32bdf9b`, the last of four automation-plan commits from another session;
  - `940eb98`, the v21-r9 ratification.
- **Tags on origin.** `evidence/cp-24` = `05b7e61`, `evidence/cp-23` = `928bc13` and
  `evidence/cp-22` = `8daf7d0`, together
  with every earlier `land/*`, `evidence/*` and `archive/*` tag listed in
  [Where the history lives](#where-the-history-lives). Two archive tags were added on 2026-10-04
  (below).
- **Branches.** Only `main` is on origin. Locally there is also
  `codex/final-product-price-lock-plan`, at `7ff6a50`, with its worktree
  `.local/worktrees/final-product-price-lock-plan`. It holds another Orchestrator session's
  Owner-authorized, deliberately uncommitted v21-r13 planning work: the final product's lock-price
  extension. Its disposition is the Owner's.
  - `gauntlet/cp-24` was reclaimed on 2026-10-11 with `scripts/gauntlet.py reclaim`, with a
    verified bundle in `.local/artifacts/cp-24-reclaim-20261010/`. Its worktrees are removed.
  - `gauntlet/cp-23` was reclaimed on 2026-10-04 with `scripts/gauntlet.py reclaim`, with a verified
    bundle in `.local/artifacts/cp-23-reclaim-20261004/`.
  - `gauntlet/cp-22` was deleted on 2026-10-04, after the tag checks. A verified Git bundle is in
    `.local/artifacts/cp22-landing-2026-10-04/`.
  - The automation plan's branches were removed on the Owner's instruction ("אמור להשאר לנו רק
    main"):
    - `claude/kind-edison-77jsmw` was fully in `main`;
    - `claude/automation-plan-corrections-t45wdc` was a superseded draft, kept as
      `archive/automation-plan-corrections-20261001` = `1615866`.
  - The sibling proposal `claude/deterministic-migration-plan-js1sd0` was kept as
    `archive/deterministic-migration-plan-20261001` = `110e361` and deleted.
  - The GitHub Desktop stash was dropped by the Owner.
- **The retired cloud session branch.** `archive/v21-r7-session-20260930` = `e84d467` keeps the
  commits this file cites reachable.
- **Retained local recovery material:**
  - `.local/artifacts/cp-24/` (102 MB), `.local/mlruns/cp24/`,
    `.local/artifacts/cp-24-reclaim-20261010/` and `.local/artifacts/cp-24-orchestrator/`.
    `.local/artifacts/cp-24/` holds the only copy of DDNN-2's warm-up and gate-day vectors, which
    4.8 may need (Critic observation O2). Keep it;
  - `.local/artifacts/cp-23/` (32 MB), `.local/mlruns/cp23/` and
    `.local/artifacts/cp-23-reclaim-20261004/`. The PyTorch reference is installed in `.venv` from
    `tests/cp23/torch-reference/`, and a plain `uv sync --locked` removes it;
  - `.local/artifacts/cp-22/` (25 MB), `.local/mlruns/cp22/` and
    `.local/artifacts/cp22-landing-2026-10-04/`;
  - `.local/artifacts/cp-21/` (62 MB) and `.local/mlruns/cp21/`;
  - `.local/artifacts/pres-3/` (327 MB), which includes the reviewed Space bundle copy
    `space-wasm-9028a118/`;
  - the CP-20 material under `.local/`
    ([artifact map](docs/track-b/local-artifacts.md); the closure records list their own).

**Public surfaces — distinguish a Git push from a verified deployment:**

| Surface | Last evidenced state / pending action |
|---|---|
| [GitHub repository](https://github.com/hrsi56/delu-day-ahead-forecast) | `land/cp-24` = `05e6015`, pushed by the Owner on 2026-10-11 with `evidence/cp-24` = `05b7e61`, on top of the Owner's work-availability commit `7ff6a50`. Before them, `land/cp-23` = `03c5b64` with `evidence/cp-23` = `928bc13`; `land/cp-22` = `ebb7d42` with `evidence/cp-22` = `8daf7d0`; and the Orchestrator's pushes on the Owner's instruction: the v4 wording fix `b194c72`, the tools, v21-r10 and the records. The README carries the corrected v3 → v4 transition. |
| [Static report](https://hrsi56.github.io/delu-day-ahead-forecast/) | v4 wording fix, served after the push of `b194c72`: HTTP 200, 1,907,718 bytes, SHA-256 `8a1fedd8bc6bf89d1db170b3fb83df34255e4c350c22113d1df52088c25c8c39`, equal to `docs/index.html`, read anonymously 2026-10-04. Wording only: no number, name or status changed. Browser checks were not rerun for a wording-only change; the reviews were waived by the Owner. The PRES-3 page before it was `97e1d862…`. |
| [Static Space](https://huggingface.co/spaces/Yarden-Viktor/delu-day-ahead-forecast) ([direct app](https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/)) | PRES-3 deployment 2026-10-01 10:45 UTC: revision `0331088725fedab2f5a1ec804ae03bf960cf126f`, public/static/RUNNING, 805 files, verified file by file against the reviewed bundle `9028a11869a378ea5c3401a00ad46368e1c9e2f2f9f8732330d32b71af081585` (44,164,910 bytes; copy at `.local/artifacts/pres-3/space-wasm-9028a118/`). `style.css` deleted. It runs v1. The card is unchanged. Public demo checks passed on 2026-10-01; the first cold run's HF 429 is retained beside its passing retry. |
| [MLflow on DagsHub](https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow) | PRES-3's authorized upload, 2026-10-01 03:32–03:43 UTC: `cp21` and its four children created; the 23 published runs found complete and untouched; no experiment tag written. Public mirror 28/28 and 7/7 routes, including `compare:v4`, in Chromium and WebKit, before the final build. The experiment description still names only the four earlier parents (A-PRES3-1). Post-deploy recheck 2026-10-01: 28/28 runs, and the routes pass in Chromium and WebKit. |

**Scope outside Track B:** Track C was cancelled and moved out of this repository; no marketing
state is tracked here. Track A is inactive and has no position. The Owner's end-stage CV-use
decision remains a boundary, not an active workstream.

---

## 2. Setup State

- **No pending setup action.** PRES-3's closure set was committed and pushed as `ddb9379` on
  2026-10-01. CP-24's closure records are in the commit that carries this update.

---

## 3. Strategic Anchors

- **Current work-availability amendment (Owner, 2026-10-10):** research **v21-r12**,
  `capstone_v21.md` SHA-256 `caf03d705a785369972b6e9ef3d043815a4a7ba77830cabb51e939c486477ce4`; publication
  **PUBLISH_RULES 1.4**, SHA-256 `ccfe6199535dc104250ee1ed1d8ff57bf0b12fbfb4945a3521e2e29fad479a80`.
  Incorporated amended baseline: Publication Standard v1 SHA-256 `7bb90c4cbd15bde42121d615bd850854610a1aa0b3a776190a58ef481abeb68c`;
  presentation plan SHA-256 `b04a0bb1af171545ad74b5a91cf96d67b53e5322a0b5394c58cbbb0ca6ace19c`.
  The [amendment record](docs/track-b/capstone_v21-r11-to-v21-r12-amendments.md) records authority and scope.
  Older scheduling instructions are superseded even in a hash-pinned brief. All research
  bars and resource ceilings remain in force; no checkpoint is opened, resumed or closed here.
  Earlier identities below record ratification history. Where a copy was amended for work
  availability, its historical hash binds the original at `522d7ea:<path>`, not the amended copy.

- **Historical publication anchor:** [PUBLISH_RULES](docs/PUBLISH_RULES.md) **1.2**, Owner-authorized
  2026-09-30; SHA-256 `a43ac02021b7de468e02db30b61ec73f86cdafa69df845cf084ab196528bb15b`.
  A1–A6 continue; strengthened A7 and A8 govern future final-product rollout/daily operation,
  and 1.2's conditional A9 (§7.3) governs the final product's Space. Revision 1.1
  (`91eea445…`) is preserved at `6f4575b:docs/PUBLISH_RULES.md`; its obligations equal 1.2's
  wherever A9 is not triggered.
  Historical PRES-2 remains governed by 1.0 (`03f106060d9a646ce0c0c986d2f5fb6549929f2ed7270f0c8678fbfd2293b3a3`),
  preserved at `evidence/pres-2:docs/PUBLISH_RULES.md`; PRES-1 retains Publication Standard v1.
  Incorporated baseline: Publication Standard v1 `01d721c2…`; presentation plan revision 3
  `28119374…`.
- **Previous research anchor, ratified on 2026-10-05** under the Owner's delegation of 2026-10-04.
  The anchor's header quotes the suspension and the grant: `capstone_v21.md` **v21-r11**,
  SHA-256 `11068e3f57bd9277be50db62d109f3e7d8ea7b8fdfa042886ccc4ae5ab1ed2d2`.
  - **What it adds,** as additions only:
    - §21.13: CP-23's outcome.
    - §23: CP-24, DDNN-2.
    - A CP-24 row in §10.
  - **Its amendment record:**
    [r10 → r11](docs/track-b/capstone_v21-r10-to-v21-r11-amendments.md), SHA-256
    `474017e1c8e8584e9c2956f40a872aa8917a6e110cbc58dc7a4110c9c802d782`.
  - **v21-r10** is preserved at `3f7aaf2:capstone_v21.md` (`6873c250…`).
- **Research anchor ratified on 2026-10-04,** superseded by v21-r11, under the Owner's task-scoped suspension
  ("מאושר באופן מלא, כולל השעיה וכולל קומיט פוש מה שאתה צריך"): `capstone_v21.md` **v21-r10**,
  SHA-256 `6873c2501067c63692ec7cb79dfd4073164a8a014edbd6ebc23169e7e8ff6709`.
  - **What it adds,** as additions only:
    - §20.13: CP-22's outcome, and the Owner's decision that v4 stays as it is. §20.1's
      "the block split is removed in every outcome" yields to it.
    - §21: CP-23, the DDNN route.
    - §22: the programme order after CP-22.
    - A CP-23 row in §10.
  - **Its amendment record:**
    [r9 → r10](docs/track-b/capstone_v21-r9-to-v21-r10-amendments.md), SHA-256
    `453a66a107e6b597cecc80c02e04995b4de4a0935960638df220c5722afa5199`.
  - **v21-r9** is preserved at `940eb98:capstone_v21.md` (`5fc9c686…`).
- **Anchors ratified on 2026-10-01** under the Owner's task-scoped suspension ("ההשעיה
  תכסה כל מה שצריך"):
  - **Research:** `capstone_v21.md` **v21-r9**, SHA-256
    `5fc9c6862aa9f623af29db295e79456ecd94c60e213f8f286cdca97153e09175`. Superseded by v21-r10
    above, which keeps its bytes.
    - §20 governs CP-22. It adds a header, a CP-22 row in §10 and §20; additions only.
    - v21-r8 is preserved at `c352436:capstone_v21.md` (`81d61271…`).
  - **Publication:** PUBLISH_RULES **1.3**, SHA-256
    `5a660864f8b82943174741320c71087a3d0508f707edeb997cb2c1395c1c73b4`.
    - It adds A10, revising an adopted generation in place.
    - 1.2 is preserved at `c352436:docs/PUBLISH_RULES.md` (`a43ac020…`).
  - **The amendment record,**
    [r8 → r9](docs/track-b/capstone_v21-r8-to-v21-r9-amendments.md), SHA-256
    `912eb98ffceb1b7b31e0e14da6cffc8725c3af7b227cbbcef4cea62841f5d52a`.
  - **The CP-22 issued brief,** `563f64f3…`, pins all three.

  The two entries below describe the anchors as they stood before 2026-10-01. Where they
  differ, these identities govern.
- **Ratified research authority (until 2026-10-01):** `capstone_v21.md` **v21-r8**,
  Owner-authorized 2026-09-30, SHA-256
  `81d6127197cabf344f56c2cf25ef5fc8f9fdb2860e249c294177471d3130c182`.
  - §19 (r8) governs the final product's Space: what it computes and claims, and the required
    in-browser "Train it yourself" action. It binds CP-17 and CP-18 and opens no checkpoint.
  - §18 (r7) governs programme item 4.6: TabPFN is withdrawn, and DDNN is written from the
    start in NumPy only, with PyTorch only as a correctness reference in tests on the
    development machine. It opens no checkpoint.
  - §17 governed CP-21, which is landed; its evidence binds the v21-r6 bytes.
  - §16, unchanged from r5, remains the final-product authority.
  - Historical §§1–18 are byte-for-byte intact; r8 adds only a header and §19.
  - CP-20 is closed under r4, and its §15.7 authority stays spent.
  - [Amendment record r7 → r8](docs/track-b/capstone_v21-r7-to-v21-r8-amendments.md), also
    recording PUBLISH_RULES 1.1 → 1.2, SHA-256 `2a2d12d3a9845d63f1e41eefdb0fa86e6e9be05db18c1c2877be8212e20854e5`.
  - [Amendment record r6 → r7](docs/track-b/capstone_v21-r6-to-v21-r7-amendments.md), SHA-256
    `86edc1d8f4e93d62abc513b5f14e5c11bd985643bb60a79d5538f4235c075112`.
  - [Amendment record r5 → r6](docs/track-b/capstone_v21-r5-to-v21-r6-amendments.md), SHA-256
    `a9086fa1d70ea9cfd9c7fde3733f631bff7b8e372a8990e6cc7a52be3650bedd`.
- **Historical authorities:**

  | Authority | Governed | Where the exact bytes are |
  |---|---|---|
  | v21-r11 | CP-24 | `evidence/cp-24:capstone_v21.md` (`11068e3f…`, verified 2026-10-11), also `76ed485` |
  | v21-r7 | Defined §18; governed no checkpoint | `c9dc364:capstone_v21.md` (`e6a4e301…`) |
  | v21-r6 | CP-21 | `evidence/cp-21:capstone_v21.md` (`ee402c47…`, verified 2026-09-30), also `270a0a0` |
  | v21-r5 | Defined §16; governed no checkpoint | `81ab3be:capstone_v21.md` (`a4e178c3…`) |
  | v21-r4 | CP-20 | `evidence/pres-2:capstone_v21.md` (`150bd53f…`) |
  | v21-r3 | CP-16 | `evidence/cp-16:capstone_v21.md` (`67d21768…`) |
  | v21-r1 | CP-15 | `evidence/cp-15:capstone_v21.md` (`44ea4e54…`) |
  | Original `capstone_v20.md` | CP-10 | `docs/track-b/anchors/cp-10-capstone_v20.md` |
  | `capstone_V6_8.md` | v1 | the file itself |

  Once the live anchor advances, closed checkpoints are reproduced from their `evidence/` tags.
- **Programme plan:** the [v3 plan handoff](docs/track-b/v3-plan-handoff-2026-09-22.md), with
  work items 4.0–4.10 and the decision register D1–D6.
  - Current identity, after v21-r8's Space notes: `b250121b…`.
  - Earlier identities: `cf498c44…` after v21-r7's 4.6 consistency edits, `ddc6bd3a…` after
    the CP-21 consistency notes, and `0fe3a69e…` after v21-r5's consistency edit (`81ab3be`).
    The `7fdd8205…` recorded here until 2026-09-29 predated `81ab3be`.
  - The [CP-21 publication plan](docs/track-b/cp-21-publication-plan-2026-09-29.md)
    (`c0ac0d26…`) plans PRES-3.
  - The [final-product Space plan](docs/track-b/final-product-space-plan-2026-09-30.md)
    (`e2160b82…`) plans the Space for CP-17 and CP-18, split by authority.
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
  - **One standing exception**, approved 2026-09-30 in `AGENTS.md` § Git and publication
    authority: the final product's daily pipeline, once an authorized CP-18 brief launches it,
    may publish each day's data-only update unattended. That covers the Space bundle, the
    data-only records and regenerated report on `main`, and `delu-live` in MLflow. It is never a
    code, policy, model, rule or anchor change, and every day is validated and fails closed.
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
    with `git config core.hooksPath /Users/djourno/Downloads/PJM/.githooks`.
    - Since 2026-10-04, the SessionStart hook `.claude/hooks/session_start.py` (wired in
      `.claude/settings.json`) restores it at every session start, when it is unset or points at
      a missing directory.
    - That covers fresh clones and cloud sessions. The Owner's suspension expressly authorized
      that write.
  - **Checkpoint tools (2026-10-04,
    [automation plan](docs/automation-plan.md) items 1, 2, 4, 5 and 8).** A party checking
    someone else's work runs `main`'s copy: `git show main:scripts/<tool> | python3 -I - …`.
    - **`scripts/bar.py`**: verbatim plan sections with their SHA-256 (`bar`), byte checks of
      quoted bars (`check`), the brief's templates §1 form (`brief`), and file identities
      (`identity`).
    - **`scripts/gauntlet.py`**, for the Lead:
      - `start` and `return`;
      - `critic-open`, `critic-brief` and `critic-close`.
    - **`scripts/gauntlet.py`**, for the Orchestrator:
      - `receipt`, which prints templates §4's list verbatim (the Owner's ruling of 2026-10-04:
        that list governs);
      - `inspect`, `citations` and `discard`;
      - `reclaim --disposition`, which enforces the tag guard and keeps a verified bundle;
      - `land-commands`, which only prints the Owner's non-interactive LAND sequence.
    - **`scripts/progress_diff.py`**: this file's omission diff. Only the Orchestrator uses it,
      and never from a hook.
  - **Claude Code cloud sessions (first used 2026-09-30):**
    - Each session is a fresh, shallow GitHub clone, without `.local/`, credentials or the
      Owner's local branches. State on the Owner's machine is confirmed by the Owner, never
      inferred.
    - Enable the secret guard in each clone with `git config core.hooksPath <clone>/.githooks`.
    - Seven `test_40_publication_guard.py` tests error there. The container sets
      `GIT_CONFIG_COUNT`, and the fixture strips `GIT_CONFIG_KEY_*`. With the count unset they
      pass, and GitHub CI is unaffected.

---

## 4. Standing Scope Decisions

These carry forward indefinitely. Each changes only by explicit Owner ratification, named in the
Session Log.

**Added 2026-09-30 (Owner — unattended daily publication; `AGENTS.md`):**

- **Daily data-only publication of the final product needs no per-day instruction.** Once an
  authorized CP-18 brief launches the pipeline, it covers every delivery day.
- **Its limits** are in `AGENTS.md` § Git and publication authority, under the standing
  publication exception.
- **This supersedes plan §5.1's row that reads "Open".** The plan’s r7→r8
  hash binds its prior bytes; the 2026-10-10 work-availability amendment removes its scheduling restrictions.
- **The Owner's other final-product decisions** (τ, τ_eq, where the job runs, visual approval,
  the Headline Arena reply) are surfaced only at the end of the programme.

**Added 2026-09-30 (Owner — final-product Space; v21-r8 §19, PUBLISH_RULES 1.2 A9):**

- **The Space becomes the final product's daily tool.**
  - It serves the designated final product only, from a dated daily bundle.
  - It shows today's issued forecast against published prices, tomorrow's forecast with its
    intervals, and measured coverage with width.
  - It offers views for the forecast, validation, reliability, explainability, features, data
    and limitations, and keeps v1 as a labelled history route.
- **"Train it yourself" is required.** It retrains one issued day's fit in the browser and
  reports only a measured equality with the issued artifact. If the designated model cannot
  meet it, CP-17 returns a blocker, and only an explicit Owner exception with public wording
  waives it.
- **Honest confidence.** The nominal level is always shown against measured coverage and width.
  The percentage measure is "within ±τ EUR/MWh", with τ set by the Owner at CP-17 before 4.7T.
  No "X% correct" and no confidence percentage.
- **Attribution, not causality,** in the feature and explainability views.

**Added 2026-09-30 (Owner — v21-r7):**

- **TabPFN is withdrawn**, in every version. It is no candidate, comparator, recombination
  member or product. The planned TabPFN–DDNN comparison is withdrawn by decision, not reported
  as failed. Bringing it back needs a new Owner amendment.
- **DDNN is written from the start in NumPy only.** One implementation, NumPy and the Python
  standard library, produces every DDNN result, daily fit and displayed forecast; no second
  implementation is written for another runtime.
- **PyTorch is only a correctness check on the development machine.** It serves in tests as a
  reference for the forward pass, the Johnson SU likelihood, gradients and short training
  trajectories. It never trains a scored model or emits anything that enters evidence, and it
  is not a runtime dependency.

**Added 2026-09-29 (Owner — CP-21 ratification):**

- **v4's chart encoding:** amber `#B45309`, a filled diamond marker and the direct label "v4"
  (PRES-1 W16(b)). This resolves the Publication Standard's "At v4" trigger. v4 was adopted on
  2026-09-30, so PRES-3 applies it.

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
- Every delivery day is in scope, including DST. Future operating authorization must supply unattended coverage,
  monitoring and failure rules. No scheduler or standing public-write permission is created now.
- Research v21-r5 §16 and publication 1.1 A7/A8 are prospective; PRES-1/PRES-2 evidence and
  immutable v1 remain unchanged. CP-17–19 and CP-21 require their own bars/briefs. Live may be
  displayed during CP-18 as evaluation in progress; CP-19 still needs at least 90 delivery days.

**Added 2026-09-24 (Owner):**

- **Same information, same opponent.** Every new model receives exactly the information v4
  receives, including the three frozen GFS weather features and their missing indicators. It is
  evaluated against v4 on identical rows, with v3 (HG) kept as a reference. Beating a weaker
  reference means beating the wrong model. *Amended 2026-09-30 by the Owner* ("מאשר להעביר את
  הכלל "אותו מידע, אותו יריב" מ-HG ל-v4"), as v21-r6 §17.6 foresaw at CP-21's landing. v4 was
  built with exactly HG's information, so the information set is unchanged; the opponent moves
  from HG to v4.
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
- **Publication anchor (updated by Owner authority, 2026-09-29 and 2026-09-30).** New publication
  briefs follow [PUBLISH_RULES 1.2](docs/PUBLISH_RULES.md), including its explicit amendments and
  triggers. 1.2 adds only the conditional A9 for the final-product Space. The already-issued
  PRES-2 task retains 1.0 and its original evidence contract.
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
  - CP-16, CP-20 and CP-21 results are `development_post_selection`;
  - economics stay descriptive, and no product threshold is invented.

**Process:**

- **Work availability (Owner, 2026-10-10):** authorized work may run at any time on every day.
  No weekday/time check, approaching-weekend stop, calendar pause or resumption exception is
  required. This replaces all earlier scheduling restrictions; see `AGENTS.md` § Work availability.
- **Reasoning capture is active** (`AGENTS.md` § Interview-answer capture).
  - Only the Orchestrator files entries, through `scripts/qa_append.py`; the Lead names triggers
    in its return.
  - `שאלות תשובות.docx` has 46 entries.
    - Entries 44–46 (2026-10-01) file three of PRES-3's six named triggers:
      - the bundle hash, from the gzip OS byte to the hidden marimo sandbox prompt, and why the
        reviewed bytes were deployed;
      - the fresh reader catching an undefined headline term that the editorial review missed;
      - the write-plan guard that left the MLflow description stale rather than make an
        unauthorized write.
    - Entry 43 (2026-09-30) covers how the final product shows "how sure" honestly: nominal level
      against measured coverage and width, a percentage measure defined in advance, in-browser
      recomputation and "Train it yourself".
    - Entries 39–42 (2026-09-30) file CP-21's four named triggers: thread determinism, the blend
      rather than the block split, the single interval-layer path, and the interrupted review.
    - Entry 38 covers why DDNN is written from scratch in NumPy rather than PyTorch, and why
      TabPFN was dropped.
    - Entry 37 covers why CP-21 adds the block LightGBM on top of v3.
    - Entry 36 covers frozen policy versus daily training and product presentation.
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

- **CP-24 paused, continued, received, landed and closed, 2026-10-05 to 2026-10-11.**
  - **The pause, 2026-10-05.** The account's usage limit stopped the first Lead at 17:28 IDT, with
    attempt 1 scored and v5 adopted, and its nested Critic 2 mid-review. The previous Orchestrator
    session wrote a pause packet.
  - **The Owner's handover, the same evening.** The Owner handed CP-24 to a new Orchestrator
    session himself ("אני מוסר לך את העבודה בעצמי").
    - He called `ORCHESTRATOR-HANDOFF.md` not relevant.
    - He said `RESUME.md` might contain errors, and should be read only for CP-24's state.
    - He had both deleted; they went to the Trash.
  - **The new session's findings.**
    - It verified the state against the branch, the ledgers and origin.
    - It set aside the old notes' re-derived metrics, which the Orchestrator may not compute.
    - It also set aside their plan to order extra leakage controls by "steering": §23.6 has no
      such channel after an adoption.
    - It confirmed the base-tree defect in the code.
  - **The continuation brief.** It was issued as `11063a11…`, without a `progress.md` update, to
    keep `main` clean during the run. The Owner's maintenance of 2026-10-10 re-issued it as
    `5960b908…`, with the calendar clauses removed.
    - It asks for a landing-safe base-tree proof.
    - It asks for item 9 evidence matched to D2's strength, with any extension verification only.
    - It asks for a fresh Critic that receives nothing from Critics 1 and 2.
  - **The return, 2026-10-10.** PASS, with candidate `7949a98` and evidence tip `05b7e61`. Critic 3
    failed `7ea9bdd` on the missing 97.5% ratio intervals. They were derived without rescoring,
    and Critic 4 passed.
  - **The receipt.** It was run with `main`'s `gauntlet.py receipt`, and every check passed:
    - the delta is evidence-only: four files;
    - the verdict is PASS at the candidate;
    - all 18 checklist rows carry evidence;
    - nothing of CP-24 was on origin.

    The staged squash was 122 added files inside §23.14's paths, byte-identical to the evidence
    tip.
  - **The LAND, 2026-10-11 01:00 IDT.** The Owner landed it by hand as `05e6015` and pushed
    `land/cp-24` and `evidence/cp-24`. The Orchestrator reclaimed the branch and its worktree, kept
    `.local/artifacts/cp-24/`, and wrote the
    [landing record](docs/track-b/cp-24-landing-2026-10-11.md). It filed Q&A entries 55–57: the
    leakage proof, the 97.5% review FAIL and the landing-safe test.
  - **Not carried forward.** The Owner said that the rest of the old pause notes would be dealt
    with later. Their programme-order and coverage proposals are therefore not recorded here as
    decisions.
  - **The omission diff.** Three items were removed:
    - the active-checkpoint block, which became the CP-24 closure;
    - "Only `main` exists", superseded by the codex branch;
    - "No worktree exists besides the primary checkout".

    The blocker on publishing the not-adopted CP-22 and CP-23 branches is still open: it is folded
    unchanged into the new "Publishing v5" blocker, with its recommendation. Nothing else was
    dropped.

- **Work availability, Owner decision, 2026-10-10.** A dedicated maintenance editor removed
  calendar restrictions from rules, plans and runtime monitors under the Owner’s explicit
  task-scoped edit/commit/push authority, including main. Research v21-r12 and publication
  1.4 record the amendment; existing evidence and historical commits remain preserved.
  The omission diff removes only the superseded scheduling conditions and updates affected
  anchor identities; checkpoint state, research requirements and other pending actions are unchanged.

- **v21-r11 ratified and CP-24 (DDNN-2) issued under the Owner's delegation, 2026-10-05.**
  - **The delegation, 2026-10-04.** The Owner handed DDNN-2 to the Orchestrator, to run through
    independent agents without the Owner until the report and the LAND request. It came with a
    Lockdown suspension, commit and push, and discretion over the design and the ceilings. The
    words are quoted in the [r10 → r11 record](docs/track-b/capstone_v21-r10-to-v21-r11-amendments.md).
    This answered the open question of DDNN-2's timing: DDNN-2 runs now, before stage 7. The
    [DDNN-2] note became CP-24.
  - **Research.** An independent research agent diagnosed CP-23 and proposed directions
    ([report](docs/track-b/cp-24-research-directions-2026-10-05.md)). Its first run was lost at a
    compaction. A usage limit interrupted the second, which was resumed and completed.
  - **Plan review.** An independent plan critic reviewed the plan twice:
    - first READY WITH FIXES, with 2 BLOCKING, 10 MAJOR and 23 MINOR findings;
    - then READY WITH FIXES, with every first-review finding resolved and three new MAJOR findings applied as given.

    The main catch: CP-20's weather grids have no record for 2022-09-29..2023-03-24, and
    pre-fold fits now leave those days out.
  - **Ratified and issued.** v21-r11 was ratified at `76ed485`, and the brief was issued as
    `a3f11470…`. The Lead was launched in the background, in `.local/worktrees/cp-24/lead`.
- **CP-23 received, landed and closed; DDNN-2 proposed, 2026-10-04.**
  - **Return.** PASS, with candidate `f9a737e` and evidence tip `928bc13`. DDNN was admitted, and
    v5 was not adopted (`cp23-adoption` condition 1, also condition 4 on fold 3). The run took
    about 4 active hours, all on Sunday.
  - **Receipt.** It was run with `main`'s copy of `gauntlet.py receipt` and `return`, and every
    check passed:
    - the delta is evidence-only and the verdict PASS;
    - `return` found 0 problems;
    - all 97 paths are inside §21.11, and the root `uv.lock` is unchanged;
    - nothing was pushed, and the published export is unchanged.
  - **Two defects of the Orchestrator's,** which the Lead escalated and the Owner ruled on during
    the run. The rulings were verified in the Lead's transcript:
    - the brief omitted the PUBLISH_RULES 1.3 hash, and the ruling was to pin `5a660864…`;
    - §21.3 put PyTorch in the evidence-bound root `uv.lock`, and the ruling was a separate lock
      in `tests/cp23/torch-reference/`.

    Both lessons were saved for future anchors and briefs.
  - **The Owner's question,** "יש לך רעיון לאיזשהו מחקר כלשהו לגבי DDNN לפני שאנחנו ככה פוסלים
    אותו?". The Orchestrator answered with a read-only diagnosis of CP-23's vectors and a proposal:
    - DDNN alone is the weakest member, at a central MAE of 21.2;
    - its errors correlate 0.83 with LightGBM's, because it was fed LightGBM's per-hour rows;
    - its hindsight best weight in v4 is 0.05–0.10, worth under 0.5%;
    - the proposal is DDNN-2: a daily representation, a real training-only search and an ensemble
      of configurations. The Orchestrator recommended running it before stage 7.
  - **The landing.** The Owner landed by hand at 21:23 IDT with the `land-commands` sequence:
    `land/cp-23` = `03c5b64`, `evidence/cp-23` = `928bc13`, pushed. The tree equals the evidence
    tip, and the message equals the prepared file.
  - **Closure.**
    - `gauntlet.py reclaim cp-23 --disposition land` bundled the branch and deleted it. `citations`
      found no live document to repoint.
    - The landing record, this update and Q&A entries 52–54 were written, committed and pushed
      under "אישור commit ו-push להכל".
  - **Open with the Owner:**
    - DDNN-2's timing;
    - whether the not-adopted branches of CP-22 and CP-23 are published. The recommendation is
      the next publication.
- **CP-23 authorized and its brief issued, 2026-10-04.**
  - **The grant.** The Owner wrote "מאשר ביצוע CP-23, ההחלטות כפי שקבעת", so v21-r10 §21.12's
    delegated decisions D4–D10 stand as set.
  - **The brief.** It was issued as `33f6b412…`, with the grant quoted under "Owner-only actions
    already authorized", and checked with `scripts/bar.py`: the bar quote is byte-exact at
    `3f7aaf2`, and the form is complete. Its envelope is in `.local/artifacts/cp-23/`.
  - **This commit** changes only this file, so the brief's expected state (a direct child of
    `3f7aaf2`) holds.
- **Automation implemented, branches cleaned, v21-r10 ratified, 2026-10-04.**
  - **The Owner's questions, answered:**
    - **A meta-learner that predicts each member's weight.** It is legal only walk-forward.
      Filed in 4.8 as a NumPy network, with baselines.
    - **More data (energy prices, rates, a fear index).** CP-15's feasibility sheet already found
      the blocker is legal, origin-correct data, not the idea. A comprehensive research was filed
      for immediately after DDNN, including the Owner's "+2" vintage idea.
  - **The Owner's instructions,** quoted in the r9 → r10 amendment record:
    - the approved order;
    - "השעיית Lockdown";
    - the receipt ruling, that templates §4's list governs;
    - "אישור commit ו-push להכל";
    - "בצע".
  - **Done.**
    - **Branches.** The automation plan's branches were removed: `kind-edison` was fully merged,
      and `t45wdc` was archived and deleted. The sibling proposal `js1sd0` was archived and
      deleted. Only `main` remains.
    - **Tools.** Items 2, 1, 5, 3, 4 and 8 were implemented, with 16 tests. The full suite passed
      on a clean worktree (1,323 passed, 7 skipped), and they were pushed as `42e4ceb`.
    - **The anchor.** v21-r10 was written as additions only (§20.13, §21 CP-23, §22 the order).
      Its amendment record and this update were committed and pushed.
  - **Resolved,** per the omission diff (`scripts/progress_diff.py`):
    - the open question on the 4.6 candidate and v5 rule, by v21-r10 §21;
    - the items left from CP-22's period: the stash, dropped by the Owner; the branches, removed;
      the automation plan, implemented;
    - the old next-pending text, replaced by CP-23;
    - "[First 4.6 brief]", replaced by "[CP-23 brief]".
  - **Not done.** No fit, model run, data retrieval, MLflow write or deployment. CP-23's
    execution is not granted yet.
- **CP-22 received, decided, landed and closed; the v4 wording fixed, 2026-10-04.**
  - **Return.**
    - The Lead's terminal return was PASS, with candidate `29d8d38` and evidence tip `8daf7d0`,
      and research result no replacement.
    - The run resumed on Saturday 2026-10-03 at 20:33 IDT, under the Owner's written calendar
      exception, and finished on Sunday.
  - **Receipt.** The templates §4 receipt was run read-only, and every check passed:
    - the delta to the evidence tip is verdict and evidence files only;
    - the verdict is PASS at the candidate;
    - all 13 items carry evidence;
    - all paths are inside §20.11;
    - nothing was pushed;
    - the anchors are unchanged;
    - the calendar exception was verified in the Lead's transcript.

    Disclosed and not CP-22's: GitHub Desktop moved `main` by ref and stashed and switched the
    tree for 21 seconds on 2026-10-01. The protocol's identity record mislabels one hash, and the
    live check against the anchor passed.
  - **Explanations given to the Owner,** which became Q&A entries 47–51:
    - why LightGBM helps with the same information: its errors correlate with v3's at only 0.79,
      and the blend beats both parts;
    - why the split can matter without information, through bias and variance;
    - a hindsight bound for per-block weights;
    - why such weights are legal only when they are causal.
  - **The Owner's decisions:**
    - "v4 נשאר כפי שהוא";
    - "תתייק ב4.8 לבחון משקל לכל בלוק", with a note on a per-fold weight or a model that predicts
      the weight, and the Owner's own question whether that is legal, "זה אומר שאנחנו לומדים
      לקראת העתיד לא?";
    - a wording fix on the site, removing the prominent mention of the split, "לא צריך לשרוף על
      זה מלא עבודה".
  - **The landing.** The Owner landed by hand at 14:31 IDT, with the non-interactive sequence:
    `land/cp-22` = `ebb7d42` and `evidence/cp-22` = `8daf7d0`, pushed. Then: "LAND. מאשר את הנוסח
    ואת הוויתור על הביקורות. אחרי ה-LAND תבצע הכול כולל commit ו-push".
  - **Done on that instruction:**
    - the landing was verified;
    - the branch was bundled and reclaimed;
    - the wording fix `b194c72` was built from source and checked: full suite 1,307 passed on a
      clean worktree, lint 0, `verify_release` PASS;
    - it was pushed, and the served page was verified equal;
    - the landing record, this update and Q&A entries 47–51 were written.

    A Finder `.DS_Store` that inflated a published directory size was kept out of the build.
  - **Not done.** No fit, model run, data retrieval, MLflow write or Space deployment.
- **CP-22 drafted under the Owner's decisions, 2026-10-01.**
  - **The request.** The Owner asked to re-examine v4 before DDNN: "תפרק את ההבדלים בין V4 ו
    V3 לגורמים … תרכיב מחדש בצורה מיטבית".
  - **The Orchestrator's findings,** read-only from committed CP-21 evidence:
    - the gain comes from the member, not the split, since the pooled model has `local_hour`;
    - the raw half drives the peak degradation;
    - the daily capacity selection is mostly noise: the median winner margin is 1.5%, and G1 was
      chosen on 24–44% of origins;
    - v3 and v4 under-cover in folds 1–4.
  - **The method.** Tuning on the folds was advised against, in favour of pre-registered
    policies.
  - **The Owner's decisions:**
    - "לא. בוא נגדיר שהגרסא החדשה שתצא תדרוס את V4. הפיצול יימחק בכל מקרה";
    - D1–D8 "מאשר כפי שהמלצת";
    - if both fail, "עוצרים וחוזרים אליך";
    - "ההשעיה תכסה כל מה שצריך";
    - "28 יום זה הרבה וזה רדג׳ידי … צריך איזשהי למידה דינאמית יותר";
    - after the single-day weighting was explained: "תוסיף", then "אני לא רוצה שהזרוע תבחר
      ותחליף את ה7 ימים. אני רוצה לבדוק האם נכון להוסיף משקל מהיר יותר בנוסף, לזיהוי שינויים
      חדים". The 3-day arm became the add-on W+DLF.
  - **Recomputed for W+DLF:** replay is now 16,000 policy-days.
  - **Drafted, uncommitted:**
    - v21-r9 §20 (CP-22), with a §10 row; additions only;
    - PUBLISH_RULES 1.3 A10; only the revision line is replaced;
    - the [amendment record](docs/track-b/capstone_v21-r8-to-v21-r9-amendments.md);
    - the [PRES-4 plan](docs/track-b/cp-22-publication-plan-2026-10-01.md);
    - a dated note in the programme handoff;
    - this update.
  - **Also delivered:** the Owner's planning prompt, `.local/artifacts/v4-investigation/orchestrator-prompt.md`.
  - **Not done in drafting.** No fit, model run, data retrieval, MLflow write or deployment.
  - **Ratified and authorized.** The Owner wrote: "נותן לך את: 1. אישור הטקסט. 2. אישור ביצוע
    CP-22. 3. הוראה ואישור לעשות commit ו-push לכל המסמכים בעצמך. נעשה הכל מקומית".
  - **Then:**
    - the anchor, the record and 1.3 were marked ratified, and §20.11's grant was recorded;
    - the brief was filled with the ratified hashes and issued, with its envelope;
    - the six documents were committed and pushed on that explicit, task-scoped instruction,
      with the secret guard enabled.
  - **The suspension** ends at this task's terminal return.

- **PRES-3 issued, returned, landed, deployed and closed, 2026-09-30 to 2026-10-01.**
  - **Issue.** The Owner decided that the brief authorizes only the MLflow upload, and confirmed
    the name "v4 · three-block LightGBM added". The brief is `57a8c7fb…`. The superseded 16:11
    draft (`ccbad5c5…`) was kept, not deleted.
  - **Return.** BLOCKED at the external gate after about 9 of 24 hours. The Integration PASS
    binds `4ad7d09`, with evidence tip `42a4bb4`. The receipt was accepted, and the upload's
    write plan was confirmed to cover `cp21` and its four children only.
  - **The Owner's steps:**
    - LAND `f6dabfa`, with `land/pres-3` and `evidence/pres-3`;
    - the push;
    - the Space deployment of the reviewed bundle copy, revision `0331088`, with `style.css`
      deleted and every file verified.
  - **A hand rebuild did not reproduce the bundle.** `make wasm` in an interactive terminal
    produced a different bundle, because marimo's invisible sandbox prompt pulled marimo 0.25.0.
    The reviewed copy was deployed instead, and the fix is on the tooling list.
  - **A6.** The Orchestrator ran the public checks, and all passed. One HF 429 first failure is
    retained beside its passing retry.
  - **The waiver.** The independent post-deployment review was waived by the Owner for PRES-3
    only ("Confirmed, proceed with closing PRES-3"), on the basis of byte identity and the
    automated public records.
  - **Reclamation and Q&A.** The branch and worktree were reclaimed. Q&A entries 44–46 were
    filed.
  - **Details:** the [closure record](docs/track-b/pres-3-closure-2026-10-01.md).
  - **Omission review** against `.local/artifacts/pres-3-landing-2026-10-01/progress-before-closure.md`:
    - the PRES-3 Current-Position block and the three PRES-3 Session Log entries are compressed
      into this line and the closure record;
    - the Note "[PRES-3 closure]" is resolved;
    - nothing else was dropped.
- **Unattended daily publication approved; Space decisions deferred to the end, 2026-09-30.**
  The Owner: "וההחלטות הללו אני רוצה שיצופו בעתיד. בסוף. אישור לפרסום יומי אוטומטי (תיקון
  ב-AGENTS.md) אפשר לאשר כבר עכשיו. יש לך אישור מפורש לעריכה הזו. אל תריץ מחדש CI".
  - **`AGENTS.md`.** A standing publication exception was added to § Git and publication
    authority. It is scoped to the final product's daily, data-only updates, active once an
    authorized CP-18 brief launches the pipeline, and validated and fail-closed every day, with
    no code, policy, rule or anchor change. This is the Owner-only amendment that Standard v1 §16
    and PUBLISH_RULES §7.2 required before Live.
  - **Deferred.** τ, τ_eq, where the job runs, visual approval and the Headline Arena reply moved
    from Open Questions to "[End of programme]".
  - **Names.** The Owner asked whether CP-17 and CP-18 were already used. They are not: no tag,
    commit or checkpoint has used CP-17–CP-19. They have been reserved in v21 §10 since
    2026-09-15 for the final freeze, daily operation and prospective evaluation, which is why the
    weather and block experiments were numbered CP-20 and CP-21.
  - **CI.** At the Owner's instruction, CI was not rerun: the commit and the squash merge carry
    `[skip ci]`. `AGENTS.md` and `progress.md` are documentation that no test pins.
- **Final-product Space plan anchored, 2026-09-30.** The Owner asked for a plan, anchored "split
  by authority", that makes the Space the final product's useful, informative tool. The Owner
  granted task-wide authority ("לצורך המשימה הזו במלואה יש לך אישור לבצע כל מה שאתה צריך קומיט
  מרג׳ פוש הוספת קבצים ועריכה") and instructed that only contracts, rules and anchors be used,
  not the current Space or site.
  - **Produced:**
    - the [final-product Space plan](docs/track-b/final-product-space-plan-2026-09-30.md);
    - research v21-r8 §19, on what the Space computes and claims;
    - PUBLISH_RULES 1.2 §7.3 (A9), on presentation and acceptance;
    - the [amendment record](docs/track-b/capstone_v21-r7-to-v21-r8-amendments.md);
    - handoff notes in 4.9O;
    - Q&A entry 43;
    - this update.
  - **Left to the Owner:**
    - the percentage tolerance τ and the equality tolerance τ_eq, at CP-17;
    - unattended daily publication, an `AGENTS.md` decision at CP-18;
    - where the daily job runs;
    - visual approval;
    - the Headline Arena reply.
  - **Headline Arena.** The Owner forwarded a message from Headline Arena inviting daily
    forecast submissions. The plan recommends declining for now: no DE-LU power target, an
    external automated publication, and no substitute for CP-19. A suggested reply is in plan
    §9.
  - **Also recorded:**
    - the Owner's CP-21 landing record (`6f4575b`) closes the reclamation item;
    - `archive/v21-r7-session-20260930` = `e84d467` was verified on origin, and the first
      session branch was deleted by the Owner;
    - the session branch name was recreated from `main` for this task.
  - **Omission review:** removed are the two resolved Setup items (CP-21 reclamation; tag and
    delete) and the in-browser retraining open question, now decided; nothing else was dropped.
- **Standing rule moved to v4; session branch retired, 2026-09-30.** The Owner: "בצע. בנוסף,
  מאשר להעביר את הכלל "אותו מידע, אותו יריב" מ-HG ל-v4."
  - **Rule.** "Same information, same opponent" now names v4, as v21-r6 §17.6 foresaw at
    CP-21's landing. The information set is unchanged, since v4 was built with exactly HG's.
    The open question was resolved, and the notes for the 4.6 brief and every research brief
    were updated.
  - **Branch.** The Owner approved tagging and deleting the session branch.
    - The cloud session created `archive/v21-r7-session-20260930` = `e84d467` locally, but its
      push was refused (HTTP 403: Git access is limited to the session's own branch). The
      session did not retry or route around the refusal.
    - Tagging and deletion therefore move to Setup State as Owner actions, in that order.
    - This file's citations now point at the tag. The v21-r7 amendment record also names the
      branch; it is a hash-bound historical record and is not repointed.
  - **Landing.** `main` was merged into the session branch rather than the branch being reset,
    so the cited commits stay reachable until the tag exists. The update landed as PR #2, with
    the same task-scoped delegation as PR #1.
  - **Omission review:** removed are the answered open question and the pending note on the
    rule, both resolved above; nothing else was dropped.
- **Programme state regenerated; CP-21 receipt recorded, 2026-09-30.** A full regeneration at
  the Owner's request, in a Claude Code cloud session.
  - **CP-21 receipt.** The templates §4 read-only checks against `evidence/cp-21` matched the
    return:
    - the six candidate commits are reachable only from the tag;
    - `git diff --stat main...evidence/cp-21` shows 70 files;
    - the delta from `260dcf9` to the evidence tip is the three verdict files;
    - every cited SHA is reachable;
    - the tag carries the v21-r6 anchor bytes, `ee402c47…`.

    Local branch and worktree reclamation cannot be checked from the cloud; it is in Setup State.
  - **Q&A.** Entries 39–42 were filed for the Lead's four named triggers.
  - **CI on PR #1.** Run 71 on `f686c51` (v21-r7) passed in full on GitHub. Run 72 on
    `4892d57` was running at regeneration.
  - **Omission review** against `4892d57:progress.md`. Nothing was dropped silently.
    - Resolved this session:
      - the open question "CP-21's receipt is not recorded" (receipt above);
      - the "[CP-21 launch]" and "[After CP-21's return]" notes (CP-21 ran, returned PASS and was
        landed; PRES-3 carries on as the next checkpoint);
      - the note "[If v4 is adopted, at CP-21's landing]", now an open question to the Owner;
      - the "[Next publication block]" note, merged into the PRES-3 note.
    - Pruned as closed history, with identities kept in Where the history lives:
      - the CP-21 design block and the PRES-2 closure block in Current Position;
      - the CP-21 issued-brief anchor line (the brief is packaged at
        `docs/track-b/evidence/cp-21/issued-brief.md`, `813fb8a4…`);
      - the stale repository lines (`main` at the ratification commit; uncommitted entry 37).
    - Compressed to one line each: the multi-line 2026-09-29 Session Log entries.

    The incoming copy is `4892d57:progress.md`, also at
    `.local/artifacts/progress-regeneration-2026-09-30/` in the cloud container.
- **Owner-delegated landing of PR #1, 2026-09-30.** The Owner: "בצע. יש לך הרשאה", after
  "יש לך אישור ועקיפה מוחלטת לבצע גם push". The agent squash-merges
  [hrsi56/delu-day-ahead-forecast#1](https://github.com/hrsi56/delu-day-ahead-forecast/pull/1)
  once CI is green. AGENTS.md otherwise reserves landing to the Owner, by hand. This is a
  task-scoped delegation, not a standing one, and the session branch is left for the Owner's
  disposition.
- **v21-r7: TabPFN withdrawn, DDNN in NumPy only, 2026-09-30.** The Owner: "יש לך הרשאה מלאה.
  תערוך בעוגנים את ההתייחסות ל DDNN ו TabPFN. אנחנו נוותר על TabPFN. קבע ש-DDNN נכתב מההתחלה
  ב-numpy בלבד. PyTorch ישמש רק כבדיקת נכונות על המחשב."
  - It followed a consultation on the Owner's request for a one-click option to retrain the final
    product in the browser. That requirement itself is still open (see Open Questions).
  - `capstone_v21.md` became v21-r7, with a header and §18 added and nothing else changed. An
    [amendment record](docs/track-b/capstone_v21-r6-to-v21-r7-amendments.md) was written, the
    handoff's 4.6 passages were edited (each marked *2026-09-30*) and Q&A entry 38 was filed.
  - Committed, pushed and opened as PR #1 under the Owner's full task-scoped authority, with the
    secret guard enabled in the cloud clone.
  - Left unchanged, with reasons in the record: PUBLISH_RULES 1.1, historical records, the public
    report and its generator, and claim guard W14.
  - The Lockdown suspension ended at that return.
- **CP-21 returned PASS and was landed, 2026-09-30.**
  - **Verdict and landing.** Integration PASS at `260dcf9`; evidence tip `1d13f99`. The Owner
    squash-landed it as `4e37cf7` and pushed `land/cp-21` and `evidence/cp-21`.
  - **Result.** The research verdict under `cp21-adoption` is v4. The block-split finding shows
    no demonstrated joint preference.
  - **Cost.** About 3.5 active hours and 6.1 machine-hours. 22,260 main LightGBM fits, with no
    cap exceeded; the reference and bootstrap passes are exhausted at 3/3.
  - **The Lead's open points** are now in Open Questions: the standing-rule update and PRES-3.
- **CP-21 ratified, authorized and issued, 2026-09-29.** The Owner: "מאשר את v21-r6 עם שני
  שינויים, ומאשר ביצוע CP-21". D1 added the pooled attribution arm L-P; D2 added the per-fold
  veto; D3, D5 and D6 as recommended (D6: amber `#B45309`, filled diamond); D4 recomputed (11
  policies, 24,000/35,000 fits, 10,500 policy-days, 60 machine-hours, about 32 hours, hard 40).
  The DagsHub restart item was closed on the Owner's confirmation. Q&A entry 37 was filed; five
  documents were committed and pushed on the Owner's instruction; the brief was issued.
- **CP-21 drafted; programme state regenerated, 2026-09-29.** The Owner chose 4.5 on top of v3,
  published in either outcome ("לצורך שימוש בv3 והוספה עליו של פיצול LightGBM לשלושה בלוקים …").
  That answered the 2026-09-24 question and superseded the recommendation to run 4.6 first, then
  4.4V and 4.8, with 4.5 only as an arm of 4.8. v21-r6 §17, its amendment record, the publication plan and the handoff notes were drafted under
  a task-scoped suspension. PRES-2's closure was verified at `05587ac`; the programme-plan pointer
  was corrected from `7fdd8205…`. Omission review against `05587ac:progress.md`.
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

- **Publishing v5 (open, Owner; v21-r11 §23.12).** v5 is adopted in research, but no public
  surface shows it. Before any publication brief the Owner decides:
  - v5's encoding (PUBLISH_RULES §14);
  - whether the not-adopted CP-22 and CP-23 branches are published. The Orchestrator recommends
    bundling them, as "tested, not adopted", into the same publication;
  - automation items 6 and 7 (Notes).

  The public planned list still shows 4.6 as DDNN against v4 until then.

- **PRES-3's three advisories for the Owner (open; none blocks closure).** Details are in the
  advisory log at the evidence tip. Recommended: defer all three, as below.
  - **A-PRES3-7, GFS attribution.** Extend `DATA-LICENSE.md`'s line to "the research models'
    weather data, from v3 on".
    - The wording also feeds both Space cards and the v1 demo's `claims.json`, so changing it now
      would invalidate the reviewed bundle.
    - Recommended: approve the wording and apply it in the next publication that deploys the
      Space.
  - **A-PRES3-1, the MLflow experiment description.** It still names only the four earlier
    parents.
    - The fix is a code change, extending the pin in
      `scripts/mlflow_export.py::EXPERIMENT_NOTE_CHECKPOINTS`, plus one authorized experiment-tag
      write.
    - Recommended: carry both in the next publication brief.
  - **A-PRES3-5, a note on standard §15** on where the met / not-met column may sit.
    - It edits a locked publication anchor, so it needs a task-scoped Lockdown suspension.
    - Recommended: fold it into the pending governance follow-up (PRES-1 W16, D6 of 2026-09-28).
- **Final-product Space decisions are deferred to the end, by the Owner's instruction (2026-09-30).**
  They are listed under "[End of programme]" in the Notes, and are not raised before then.
  Unattended daily publication was approved on 2026-09-30 and written into `AGENTS.md`.
- **Final-product operating specification remains pending:** no final version designated and no
  daily system running. Future authorized work must fix numeric fit/issuance schedules, training
  windows, resources, percent-score formula/tolerance, source/outcome timing, business-use-case
  evaluation (if any), deployment/daily-demo design and daily failure coverage. These
  implementation fields do not reopen the now-ratified product identity/order/daily-fit decision.
- **PRES-2 advisories R1–R7 were dispositioned in PRES-3** (the
  [advisory log](docs/track-b/publication-advisory-log.md)):
  - R6 and R7 were taken up;
  - R2's cold-start re-measurement was carried to PRES-3's public checks, where the four runs
    recorded 18.9–21.5 s;
  - R1, R3, R4 and R5 were deferred with reasons, for a later presentation block. R3 and R4
    wait for a change to the product documentation.
- **PRES-1 remains closed under its landing record.** F6–F8 passed under the explicit Owner
  exception. Initial HF/DagsHub rate-limit failures and successful retries are recorded.
  Historical active-hour total and added-disk baseline remain unavailable, not retroactively
  certified compliant. Required tags preserve all evidence. New rules do not retroactively turn
  PRES-1 advisories into violations.
- **Scoring passes are exhausted for CP-20, CP-21 and CP-24.** Further CP-20 scoring would need a
  cap decision; CP-21's reference and bootstrap passes stand at 3/3, and CP-24's reference passes
  at 3/3, so any rescoring of CP-21 or CP-24 needs a new Owner-approved allowance.
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
  - a later change to CP-23's test-only lock `tests/cp23/torch-reference/uv.lock` turns CI red
    unless CP-23's tests and CP-24's frozen `test_reference_record.py` get the Owner's
    `AMENDED_BY_…` treatment. A later change to `scripts/mlflow_export.py` needs the same in
    CP-23's tests. Both files are frozen today
    ([CP-24 land simulation](docs/track-b/evidence/cp-24/land-simulation.md));
  - a cold first visit to the Space can hit a Hugging Face `429`;
  - `reports/cp3/pages_build.json` stamps its build date;
  - `actions/checkout@v4` and `setup-uv@v6` target the deprecated Node 20, though they run on
    Node 24;
  - `AGENTS.md` § Interview-answer capture has the typo "agents Never hand-edit". Fixing it
    requires a suspension;
  - `test_40_publication_guard.py` errors in Claude Code cloud containers (see Platforms). The
    fixture could also strip `GIT_CONFIG_COUNT`.
- **Closed and not to be reopened:**
  - the CP-0 defect ledger (20 defects, closed 2026-09-14);
  - the ENTSO-E outage;
  - PRE-2 / DagsHub MLflow;
  - the `hrsi56` vs `Yarden-Viktor` Hugging Face account question;
  - the missing LICENSE.

---

## 7. Notes for Future Sessions

- **[Tooling follow-up]** PRES-3's tooling advisories, for a later, separately authorized task:
  - A-PRES3-2: write the gzip header explicitly, so the bundle is byte-identical across Python
    versions;
  - A-PRES3-3: keep shared presentation code out of research checkpoints' byte-bound manifests;
  - A-PRES3-4: point the runbook's browser commands at `.local/tools/ms-playwright`;
  - A-PRES3-6: extend the release check's overlap test to chart marks.
  - **New, 2026-10-01:** make `scripts/build_wasm_space.py::run_export` pass `--no-sandbox` and
    `stdin=DEVNULL`, or pin marimo in the notebook header. A rebuild must then reproduce the
    reviewed bundle from any terminal. Until that lands, deploy reviewed bundle copies, never a
    hand rebuild.
  - **New, 2026-10-01:** rename `deploy_space.py`'s plan field `served_equals_bundle`, for example
    to `before_served_equals_bundle`, so that a deploy record cannot read as a failed
    verification.
  - **New, 2026-10-04: a local build can be contaminated.**
    - `src/delu_forecast/claims.py` sums `models/champion/` for the published "whole directory"
      size, excluding only `__pycache__` and `.pyc`. A Finder `.DS_Store` there moved the
      number from 31,623,247 to 31,629,395 bytes in a local build.
    - The fix: count only tracked files, or exclude dotfiles.
    - Until then, before building the page locally, check `git status --ignored models/champion`.
- **[4.8 Recombination] The Owner's idea, 2026-10-04: "תתייק ב4.8 לבחון משקל לכל בלוק".**
  Bound by v21-r10 §22.
  - **To test:** a LightGBM weight for each hour block, in place of the fixed 1/3.
  - **Filed on the Owner's question, 2026-10-04:** "לבחון רשת ב-NumPy לצורך meta-learner".
    - **The candidate:** a small NumPy network, on DDNN's code, that predicts each member's
      weight for tomorrow from regime features. Examples are recent volatility, each member's
      recent errors, season and hour block.
    - **Its baselines:** fixed weights, per-block weights, and weights from recent errors.
    - **Its rule:** set in advance. Simple baselines often match a meta-learner, which can lag
      exactly at a regime change.
  - **Also noted as an idea:** a weight that varies over time or by period.
  - **Admissibility.** Only causal forms are legal:
    - estimated at each origin from released errors only (≤ D−2), walk-forward;
    - designed and frozen before any scoring.

    A weight chosen per fold from that fold's own outcomes is an oracle, and so is a model fitted
    on later folds and applied to earlier ones. Both are excluded.
  - **Disclosed hindsight bound.** The Orchestrator computed it on 2026-10-04 from CP-22's
    committed `members.parquet` and `predictions.parquet`. Script and output are in
    `.local/artifacts/cp-22/oracle_block_weights.py` and `oracle-block-weights.txt`. It uses the
    central forecast and selects nothing. Against the fixed 1/3:

    | Weighting | Pooled central MAE |
    |---|---|
    | One global weight (0.40) | −0.1% |
    | Per block (night 0.20, shoulder/peak 0.55, solar 0.50) | −0.8% |
    | Per fold and block | −1.6% |

  - **What the bound shows.**
    - The night wants less LightGBM than the day in all five folds.
    - The 2022 crisis wants much less in every block (0.10–0.40).
    - A causal weight would realize only part of the bound. CP-22's intervals were about ±0.5%
      of S, so the gain may not be demonstrable.
  - **Timing.** Best done after DDNN, so that all members' weights are learned together once. Any
    result stays development evidence; 4.7T is the test.
- **[CP-24]** Closed on 2026-10-11. v5 is adopted in research
  ([landing record](docs/track-b/cp-24-landing-2026-10-11.md)).
  - **DDNN-2's vectors for 4.8.** The scored vectors are in `reports/ddnn2/attempt-1/members.parquet`
    and `predictions.parquet`. The warm-up and gate-day vectors exist only in
    `.local/artifacts/cp-24/` (Critic observation O2), so do not clean that folder before 4.8.
  - **DDNN-2 alone was −10.67% S_MAE against v4,** descriptively. That invites a 4.8 arm, with
    its weight set by a pre-registered rule before any scoring and an honest post-selection label.
    It cannot be a further CP-24 attempt.
- **[CP-23]** Closed on 2026-10-04. DDNN was admitted and v5 was not adopted
  ([landing record](docs/track-b/cp-23-landing-2026-10-04.md)). Its DDNN vectors are saved in
  `reports/distribution-challenger/members.parquet` and are available to 4.8 at no fit cost. The
  hindsight best weight inside v4 is 0.05–0.10, worth under 0.5%.
- **[CP-22]** Closed on 2026-10-04 with no replacement; v4 is unchanged
  ([landing record](docs/track-b/cp-22-landing-2026-10-04.md)). PRES-4's replacement plan was not
  entered. v21-r10 §20.13 records the outcome against §20.1.
- **[Data admission research] Immediately after DDNN** (v21-r10 §22, stage 7), with 4.4V. The
  Owner's scope, 2026-10-04: "מחירי אנרגיה, ריביות, מדד פחד בבורסה המקומית כל מה שאפשר וחוקי
  לשלוף וללמוד ממנו".
  - **Candidates:**
    - gas (TTF and alternatives), oil, coal and EUA;
    - central-bank rates;
    - a German volatility index (VDAX-NEW or V2X);
    - neighbouring zones and cross-border capacity;
    - outages;
    - wind, solar and load forecasts.
  - **Inputs published after the 11:00 UTC origin.** For example, the TSO wind and solar
    forecasts are published at 18:00. Test two routes:
    - an earlier vintage that already covers delivery day D, such as a forecast for D published
      at 18:00 on D−2. This is the Owner's "+2" idea;
    - another provider, or an API, that publishes before the origin.
  - **Wind and solar.** Compare an external, reliable forecast API with building 4.4V's own
    model.
  - **Admission.** Every input must pass CP-15's five admission checks
    (`reports/cp15/feasibility/structural_inputs.md`). They require a licence for research and
    for the final product's daily operation, an `available_at` vintage, missingness, an
    imputation rule, and coverage from 2019 with redistribution rights.
  - **Starting point.** CP-15 found no free, redistributable, origin-correct TTF series from 2019;
    EEX's terms restrict use, including AI use. EUA has only an auction archive.
  - **Order.** Desk research first. Any retrieval, subscription or purchase is the Owner's
    decision. Admitted inputs go to a pre-registered ablation checkpoint, and DDNN's comparison
    stays on v4's information.
- **[Security hardening before CP-18]** CP-18's daily pipeline handles credentials every day.
  Before it, bring back the security items of the archived proposal
  `archive/deterministic-migration-plan-20261001` (v21-r10 §22):
  - a value-free leak scan with salted fingerprints;
  - an AST lint for bare `os.environ[...]` reads;
  - GitHub rulesets;
  - a language rule for role files, which today say "Reply in English" while the Owner wants
    Hebrew.
- **[Formerly unscheduled hypothesis]** v3 plus a single pooled LightGBM member was tested inside
  CP-22's design (§20.2), as A-LP and the pooled members. None was adopted, and no replacement was
  made.
- **[4.7T]** v4 is adopted, so its frozen manifest carries both v3 and v4. CP-22 made no
  replacement, so v4 there is the three-block construction. CP-23 adopted no v5. CP-24 adopted
  v5 = (2/3)·HG + (1/6)·L + (1/6)·DDNN-2 in research, so v5 joins too, unless 4.8 replaces it.
  Whether DDNN-2 alone should face 4.7T is a decision for before 4.7T, under a pre-registered rule.
- **[Before the next publication's brief — binding, v21-r10 §22]** Bring automation items 6
  (post-deploy publication receipt) and 7 (pre-review check runner) to the Owner for a decision.
  The brief is not issued before it. Also carry:
  - A-PRES3-1, -5 and -7 (Blockers);
  - the Owner's choice of v5's encoding (PUBLISH_RULES §14). v5 was adopted by CP-24.
- **[Every new publication brief]** Pin PUBLISH_RULES 1.4 (from 2026-10-10) and
  incorporated source hashes;
  retain A1–A6 and apply A7/A8/A9 at their final-product/live triggers. PRES-2 was closed under
  its original 1.0 contract. Predecessor comparisons and descriptive chart routes remain;
  v2→v3 reuses existing weather evidence, and v1's archive stays historical.
- **[Final-product designation / CP-17–19]** Carry research v21-r5 §16, publication 1.1 §§5/7.2,
  runbook §7b and packet §5d. Complete the numeric operating/scoring manifest, publish one
  product/demo policy at authorized rollout, and distinguish daily live evidence from completed
  prospective evaluation. No current research generation is promoted by this documentation task.
  *Added 2026-09-30:* also carry research v21-r8 §19 and PUBLISH_RULES 1.2 §7.3 (A9), with the
  [final-product Space plan](docs/track-b/final-product-space-plan-2026-09-30.md) §7 as the
  checklist.
  - **The CP-17 brief** runs §19.3's browser feasibility probe for the designated policy, then
    freezes:
    - the percentage measure with the Owner's τ;
    - the rolling windows, the reliability and PIT definitions, and the recomputation tolerance;
    - τ_eq and the reference runtime;
    - any neural attribution method;
    - the Space payload schema.
  - **The CP-18 brief** builds the daily bundle and the A9 views, with their tests and negative
    controls. Unattended daily publication is already authorized by `AGENTS.md`'s standing
    publication exception (2026-09-30). The brief names the pipeline's paths, credential use
    and monitoring within that exception.
- **[2026-10, from the 19th]** `ubuntu-latest` moves to Ubuntu 26. CI is pinned to Python 3.12;
  check the first run after the move.
- **[Every research brief]** Apply the 2026-09-24 standing decisions:
  - v4's information set (HG's, including the GFS features), with v4 as the opponent on
    identical rows and v3 as a reference (amended 2026-09-30);
  - no data after 2026-04-07;
  - DDNN is written in NumPy only, with PyTorch only as a correctness reference in tests on the
    development machine; TabPFN is withdrawn (v21-r7 §18);
  - positive controls must survive the model's own transforms (see Lessons).
- **[After publication / governance follow-up]** PRES-1 W16/template proposals remain in its
  preserved return for a separate appropriately authorized governance task; no locked-template
  amendment is certified here. PRES-2's runbook/packet updates do not establish that every W16
  proposal was adopted. Until that task runs (D6 of 2026-09-28), every research brief carries
  the MLflow step and the packet explicitly, as CP-21's brief does. Do not repeat F1 or reopen
  PRES-1.
  - *Added 2026-10-01*, for the same task:
    - A-PRES3-5's note on standard §15;
    - the proposal to require the independent post-deployment review only when the served
      bytes differ from the independently reviewed bytes, or a public check fails. PRES-2 and
      PRES-3 were both waived on byte identity.

    Both edit locked publication anchors and need the Owner's task-scoped suspension.
- **[End of programme, after the holidays]**
  1. The 4.7T fresh-data test on the unused period. Report the never-published sub-period from
     2026-09-07 separately.
  2. The CP-17 freeze and a live run of at least 90 days for the final model only. The live panel
     goes at the top of the page.
  3. CV use. Presentation is the Owner's.
- **[End of programme — surface these Owner decisions then, not before]** (Owner instruction,
  2026-09-30; [plan](docs/track-b/final-product-space-plan-2026-09-30.md) §5.1):
  - **At CP-17, before 4.7T:**
    - the percentage tolerance τ, for the measure "within ±τ EUR/MWh";
    - the equality tolerance τ_eq of "Train it yourself", after the browser feasibility probe
      measures time, memory, payload sizes, deviation from the native fit and selection
      agreement. CP-21 measured v4's cold daily cycle at a median of 24.7 s and a maximum of
      69.4 s on the M3 with four processes; browser timings are unmeasured.
  - **At CP-18:**
    - where the daily job runs;
    - visual approval of the new Space.
  - **Headline Arena:** the reply to the invitation received on the Space. The recommendation is
    to decline, and revisit only after CP-19 and only if the arena adds a DE-LU day-ahead
    target. The suggested reply is in plan §9. Posting it is the Owner's external action.
  - **Optional, earlier if the Owner wants it:** a bounded probe brief to de-risk the button
    (plan §7, step 2).
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
- **Deploy the bytes that were reviewed, not a rebuild.** A hand `make wasm` in an interactive
  terminal pulled marimo 0.25.0 through a hidden sandbox prompt and produced a different bundle.
  The hash binding refused it.
- **Owner-run Git must be non-interactive.** The CP-21 LAND stalled in the pager and then in vim.
  Every owner packet uses `git --no-pager` and `git commit -F <message file>`.
- **A result far from the prior widens the controls before the review.** CP-24's DDNN-2 jumped
  from CP-23's weakest member to −10.7% against v4, while its leakage masks were proven at only
  two origins. The full-coverage refit settled it. A test that pins living files is a landing
  hazard too, and the CP-24 base-tree test would have turned `main` red.
- **The holdout is opened once.** v1's is spent, and the model that ships is the model that was
  evaluated.

---

## Where the history lives

- **Reviewed chains:**
  - `evidence/cp-0`, `evidence/cp-1`, `evidence/cp-2`, `evidence/cp-3`, `evidence/cp-3b`,
    `evidence/cp-15` (including CP-10), `evidence/cp-16`, `evidence/cp-20`, `evidence/cp-21`,
    `evidence/cp-22`, `evidence/cp-23` and `evidence/cp-24`, with landings at the matching
    `land/` tags;
  - `evidence/pres-1` / `land/pres-1`, `evidence/pres-2` / `land/pres-2` and
    `evidence/pres-3` / `land/pres-3` preserve the publication chains; all three publications
    are closed and their branches reclaimed;
  - `archive/cp-0-attempt-1`, `archive/weather-admission-20260923` and
    `archive/cp15-cp16-content-20260923`;
  - `archive/v21-r7-session-20260930` = `e84d467`, the retired cloud session branch behind
    PR #1, pushed by the Owner on 2026-09-30;
  - `archive/automation-plan-corrections-20261001` = `1615866`, a superseded draft of the
    automation plan, and `archive/deterministic-migration-plan-20261001` = `110e361`, the sibling
    security proposal. Both branches were deleted on 2026-10-04, on the Owner's instruction.

  Squash landings do not contain the candidate SHAs; only the tags preserve them. Verdicts are in
  `docs/track-b/evidence/<cp>/`.
- **CP-21 evidence:** the [return](docs/track-b/evidence/cp-21/checkpoint-return.md),
  [Integration verdict](docs/track-b/evidence/cp-21/integration.md),
  [publication packet](docs/track-b/evidence/cp-21/publication-packet.md) and
  [issued brief](docs/track-b/evidence/cp-21/issued-brief.md) (`813fb8a4…`), with the results
  under `reports/block-challenger/`. Its identities: candidate `260dcf9`, evidence tip `1d13f99`,
  landing `4e37cf7`.
- **CP-22 evidence:**
  - the [return](docs/track-b/evidence/cp-22/checkpoint-return.md);
  - the [Integration verdict](docs/track-b/evidence/cp-22/integration.md);
  - the [publication packet](docs/track-b/evidence/cp-22/publication-packet.md);
  - the [issued brief](docs/track-b/evidence/cp-22/issued-brief.md) (`563f64f3…`);
  - the results under `reports/v4-revision/`, with the
    [report](reports/v4-revision/report.md).

  Its identities: candidate `29d8d38`, evidence tip `8daf7d0`, landing `ebb7d42`.
- **CP-23 evidence:**
  - the [return](docs/track-b/evidence/cp-23/checkpoint-return.md);
  - the [Integration verdict](docs/track-b/evidence/cp-23/integration.md), with the Critic's
    independent scorer under `review/`;
  - the [publication packet](docs/track-b/evidence/cp-23/publication-packet.md);
  - the [issued brief](docs/track-b/evidence/cp-23/issued-brief.md) (`33f6b412…`);
  - the entry records and results under `reports/distribution-challenger/`, with the
    [report](reports/distribution-challenger/report.md).

  Its identities: candidate `f9a737e`, evidence tip `928bc13`, landing `03c5b64`.
- **CP-24 evidence:**
  - the [return](docs/track-b/evidence/cp-24/checkpoint-return.md);
  - the [Integration verdict](docs/track-b/evidence/cp-24/integration.md), with Critic 3's
    [FAIL](docs/track-b/evidence/cp-24/review/critic-3-integration-FAIL.md);
  - the [land simulation](docs/track-b/evidence/cp-24/land-simulation.md);
  - the [publication packet](docs/track-b/evidence/cp-24/publication-packet.md);
  - the [issued brief](docs/track-b/evidence/cp-24/issued-brief.md) (`a3f11470…`) and the
    [continuation brief](docs/track-b/evidence/cp-24/continuation-brief.md) (`5960b908…`), with
    the S1 exchange under `steering/`;
  - the entry records, round 1, attempt 1 and the leakage controls under `reports/ddnn2/`, with
    the [report](reports/ddnn2/report.md).

  Its identities: candidate `7949a98`, evidence tip `05b7e61`, landing `05e6015`.
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
    `8007f0d2…`. Twelve product subjects, the v1→v2 and v2→v3 transitions and the F01–F04
    repairs shipped; the new independent postdeploy review was waived for PRES-2 only.
  - PRES-3: [closure record](docs/track-b/pres-3-closure-2026-10-01.md), which carries the
    packet §8.1 receipt;
    [Integration](docs/track-b/evidence/pres-3/integration.md),
    [publication packet](docs/track-b/evidence/pres-3/publication-packet.md),
    [editorial review](docs/track-b/evidence/pres-3/editorial.md),
    [fresh reader](docs/track-b/evidence/pres-3/fresh-reader.md) and
    [issued brief](docs/track-b/evidence/pres-3/issued-brief.md) (`57a8c7fb…`).
    - Identities: candidate `4ad7d09` (independently checked at `747d2bb`), evidence tip
      `42a4bb4`, landing `f6dabfa`, Space revision `0331088`, bundle `9028a118…`, page
      `97e1d862…`.
    - The independent postdeploy review was waived for PRES-3 only.
- **Landing and receipt records:**
  - [CP-15 landing](docs/track-b/cp-15-landing.md);
  - [CP-16 landing](docs/track-b/cp-16-landing-2026-09-23.md);
  - the CP-16 [blocked](docs/track-b/cp-16-blocked-receipt-2026-09-23.md) and
    [PASS](docs/track-b/cp-16-pass-receipt-2026-09-23.md) receipts;
  - the [weather/content intake](docs/track-b/weather-content-intake-2026-09-23.md);
  - [CP-20 landing](docs/track-b/cp-20-landing-2026-09-24.md);
  - the CP-21 receipt, recorded in this file's Session Log on 2026-09-30, and the Owner's
    [CP-21 landing and closure record](docs/track-b/cp-21-landing-2026-09-30.md);
  - the [CP-22 landing and closure record](docs/track-b/cp-22-landing-2026-10-04.md). It includes
    the receipt, the Owner's decision and the v4 wording fix's public receipt;
  - the [CP-23 landing and closure record](docs/track-b/cp-23-landing-2026-10-04.md). It includes
    the receipt, the Owner's two rulings during the run, and the Orchestrator's diagnosis behind
    DDNN-2;
  - the [CP-24 landing and closure record](docs/track-b/cp-24-landing-2026-10-11.md). It includes
    the pause, the Owner's handover, the continuation, the receipt and the LAND;
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
  - `capstone_v21.md` with its amendment sheets, the latest being
    [r9 → r10](docs/track-b/capstone_v21-r9-to-v21-r10-amendments.md);
  - the [automation plan](docs/automation-plan.md), with its implementation status;
  - the programme plan and its reviews in `docs/track-b/`;
  - the [CP-21 publication plan](docs/track-b/cp-21-publication-plan-2026-09-29.md) and the
    unexecuted [CP-22 publication plan](docs/track-b/cp-22-publication-plan-2026-10-01.md);
  - the [final-product Space plan](docs/track-b/final-product-space-plan-2026-09-30.md).
- **Defect ledger:** `docs/track-b/cp-0-defects.md`, closed 2026-09-14.
- **v1 results:** `docs/cp2-model-report.md` and `reports/cp2/`.
- **Local recovery material:** `.local/`, per the [artifact map](docs/track-b/local-artifacts.md).
  It is not an off-device backup.
- **Everything else:** `git log`.
