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
| 3 | Presentation around v2 (4.3R), with CP-20 alongside | ✅ PRES-1 published and closed; [landing and F8](docs/track-b/pres-1-landing-2026-09-29.md), evidence preserved at `evidence/pres-1` |
| 4 | v3 weather pipeline (CP-20, 4.4D) | ✅ Done and landed |
| 5 | Three-block LightGBM (4.5) | ⬜ Not started |
| 6 | DDNN / TabPFN (4.6L → 4.6R → 4.6C) | ⬜ Not started |
| 7 | VRE generation and residual-load model (4.4V, optional) | ⬜ Not started |
| 8 | Recombination (4.8, optional, after 5–7) | ⬜ Not started |
| End | Fresh-data test (4.7T), then live run of the final model (CP-17 → CP-19), then public presentation and CV (4.3C/4.10R) | Reserved for the end |

**PRES-1 CLOSED — LAND and F6–F8 complete, 2026-09-29.**
[Landing/publication record](docs/track-b/pres-1-landing-2026-09-29.md); [receipt/F5](docs/track-b/pres-1-receipt-2026-09-29.md).
The Owner expressly reaffirmed D5 as a checkpoint-only exception. Reviewed candidate
`a0302dd6c5ff6714709b4f3a3b742f71a4b596a7` and evidence tip
`0df6dda203ea31ab35b34e7ad69d2a2e3e871ebf` are preserved by `evidence/pres-1`.
Squash landing `265661da4d8ae2565003c8ab6e8525f9ffec45d3` is tagged `land/pres-1`;
both tags and main were pushed. The Lead branch/worktree are reclaimed; only main remains.

- Engineering full independent PASS and delegated F5 were accepted. F1 was **not repeated**.
- Report/README published; exact 805-file Space bundle deployed at Hub commit
  `59d941825755bf73eabb7ff20e31124fee305755`. Demo remains v1, research presentation covers v1–v3.
- F8 passed: Pages exact bytes, bundle identity, four fresh engine/viewport demo checks with
  controls, complete 23-run mirror, six routes in both engines, ten settled charts and link gate.
  Initial HF/DagsHub 429 failures are retained; targeted fresh retries passed. No uninterrupted
  availability guarantee. Public landing/tag CI and Pages deployment passed.
- Historical FAILs, effort/disk accounting limitations and cold-reader/device limits remain.
  No governance edit, guard bypass, new research or later-checkpoint authority.

**Next pending Track B checkpoint: CP-21, the first v3 extension.** It is not authorized yet:
the Owner has not chosen the extension (see Blockers). Opening it needs a v21-r5 amendment and a
CP-21 brief that apply the standing decisions below. CP-17–CP-19 stay reserved for the final
model's freeze, live operation and prospective evaluation.

**Repository:**

- Only `main` and the primary checkout remain. PRES-1 landing/evidence refs are the two tags above.
- Public PRES-1 landing/tag CI (`invariant-tests`) and Pages deployment passed; exact runs in the landing record.
- Decoded GFS grids and CP-20 working material are retained under `.local/`
  ([artifact map](docs/track-b/local-artifacts.md)).

**Public surfaces (PRES-1; demo v1 / research v1–v3):**

| Surface | What it is |
|---|---|
| [Static report](https://hrsi56.github.io/delu-day-ahead-forecast/) | The primary link; makes zero network calls |
| [Static Space](https://huggingface.co/spaces/Yarden-Viktor/delu-day-ahead-forecast) ([app direct](https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/)) | The champion's boosters in the browser, bitwise equal to the frozen artifact |
| [MLflow on DagsHub](https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow) | Every decision-bearing run, anonymously readable |

README/report/Space research cards now present v1–v3. The released browser model remains v1;
the 23-run `delu-generations` mirror is public and verified. No research generation is promoted
to the demo by this presentation release.
- **Earlier:** v1 complete and closed (CP-0 … CP-3B, REL-1).

---

## 6. Blockers / Open Questions

- **PRES-1 closed; no remaining release blocker.** F6–F8 passed under the explicit Owner
  exception. Initial HF/DagsHub rate-limit failures and successful retries are recorded.
  Historical active-hour total and added-disk baseline remain unavailable, not retroactively
  certified compliant. Required tags preserve all evidence; no implementation or review reopens.
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
- **Public-surface defects F01–F04 resolved by PRES-1.** Responsive report, explicit demo startup
  states, current verified tracking links and generated README shipped; post-deploy checks pass.
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

- **[2026-10, from the 19th]** `ubuntu-latest` moves to Ubuntu 26. CI is pinned to Python 3.12;
  check the first run after the move.
- **[Next extension brief]** Apply the 2026-09-24 standing decisions:
  - HG's information set, with HG itself as a reference on identical rows;
  - no data after 2026-04-07;
  - a TabPFN run needs 4.6L's licence-use table first;
  - positive controls must survive the model's own transforms (see Lessons).
- **[Next]** PRES-1 is closed. W16/template/publication-packet proposals remain in the preserved
  return for a separate appropriately authorized governance task; none was applied at closure.
  Then the unresolved CP-21 extension choice. Do not repeat F1 or reopen PRES-1.
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
