# Programme state — DE-LU day-ahead forecasting

*Orchestrator-owned. **Regenerated 2026-09-15 for handover**, replacing a file that had accreted
through a three-track programme that no longer exists. Written for the Orchestrator who picks this
up next.*

**The one active plan: [`capstone_v20.md`](capstone_v20.md) — *From frozen artifact to running
system*, ratified 2026-09-15.** Everything else named in this file is history, reference, or
environment.

`main` = `origin/main` = **`8d56942`** · tree clean · one branch · 191 tests pass.

---

## 1. Where the programme stands

**v1 is complete, live, and closed. v2 has not started.**

| | | |
|---|---|---|
| **M1 / CP-1** | Data layer, fixed features | `land/cp-1` · `evidence/cp-1` |
| **M2 / CP-2** | Model, calibration, analysis | `land/cp-2` · `evidence/cp-2` |
| **M3 / CP-3** | Showcase and release | `land/cp-3` · `evidence/cp-3` |
| **M3.5 / CP-3B** | WASM showcase on a Static Space | `land/cp-3b` · `evidence/cp-3b` |
| **REL-1** | Publish | **complete** — all four conditions met |
| **CP-10 → CP-14** | `capstone_v20.md` §9 | **not started** |

### The three live surfaces

| | |
|---|---|
| **[Static report](https://hrsi56.github.io/delu-day-ahead-forecast/)** | The primary link. The full §10 reading order in one self-contained file that makes **zero network calls** — it cannot sleep and cannot break when a CDN does. |
| **[Interactive Space](https://huggingface.co/spaces/Yarden-Viktor/delu-day-ahead-forecast)** · [app direct](https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/) | The champion's own boosters running in the browser under Pyodide, proved **bitwise equal** to the frozen artifact. A Static Space executes nothing, so it never sleeps. ~57 MB first visit, ~1 MB after. |
| **[MLflow on DagsHub](https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow)** | Every decision-bearing run, anonymously readable. |

### What v1 actually claims

The champion beats the similar-day naive on the one-shot holdout on **both** metrics — MAE
25.9078 vs 27.7578 (−6.66 %), mean pinball 6.7083 vs 13.8789 (−51.67 %), DM p 1.98e−18 — and that is
the only confirmatory evidence in the project. Everything else is `development_post_selection`.

**Two results are deliberately unflattering and must stay that way.** The point-MAE DM in
development is `p = 0.948` with statistic **+1.6228** — the median is 28.58 % *worse* than the
naive, dominated by fold_3, the August-2022 crisis peak. And the 95 % interval covered **0.194** of
outcomes over the August-2022 peak weeks. **That collapse is the defect `capstone_v20.md` exists to
fix**, and it is documented on every public surface. It is not a bug to quietly repair.

---

## 2. What happens next

`capstone_v20.md` §9. Five checkpoints, dependencies stated per row.

| | | Depends on |
|---|---|---|
| **before CP-10** | the §2.4 run-count reconciliation — **already done 2026-09-15**, not a checkpoint | — |
| **CP-10** | M4 calibration: C-1 scaled conformal and C-2 ACI, selection on folds {1,2,4,5} only | — |
| **CP-11** | Freeze `v2-calibration-only` and `v2-full`; the 90-day clock starts | CP-10 |
| **CP-12** | The daily service + MLflow on the critical path | CP-11 |
| **CP-13** | The live scorecard | CP-12 |
| **CP-14** | The one-shot evaluation | CP-11 + 90 delivery days |

**Read §13 of the plan before writing the first brief.** It is written for the Engineering Lead and
states what to read, what not to touch, and the standards that are not negotiable.

---

## 3. Open items

- **⚠ CP-3B item 6 was never completed.** No Integration Critic verdict binds its final candidate
  `55a70e7`: round 1 FAIL, round 2 FAIL then repaired, round 3 cut off twice by usage limits. The
  Lead returned `INCOMPLETE`; the owner directed release. Recorded at
  [`docs/track-b/evidence/cp-3b/item-6-NOT-COMPLETED.md`](docs/track-b/evidence/cp-3b/item-6-NOT-COMPLETED.md)
  with the Orchestrator's substitute verification described for exactly what it is and is not.
  **This is not a precedent** — `capstone_v20.md` §9 forbids landing without a binding verdict, and
  every brief must say so.
- **A cold first visit to the Space can meet a `429`.** Immediately after an upload, Hugging Face's
  own edge rate-limited a burst of ~176 parallel asset requests and the page rendered blank; a
  reload cleared it. Transient, but a first-time visitor can hit it.
- **`reports/cp3/pages_build.json` stamps `built_on` with the build date**, so regenerating on a
  later day dirties that record. No published surface moves. Fold it into the next regeneration.

**Closed and not to be re-opened:** the CP-0 defect ledger (20 defects, closed 2026-09-14); the
ENTSO-E outage (resolved, and the v2 daily path uses SMARD anyway); PRE-2 / DagsHub MLflow; the
`hrsi56` vs `Yarden-Viktor` Hugging Face account; the missing LICENSE.

---

## 4. Lessons that cost something

Each of these was paid for once. None should be re-learned.

- **A green test run is not evidence.** CP-1's first attempt returned `PASS` from its own Integration
  Critic while **95.83 % of its rows leaked**, because every test inherited the same wrong premise.
  An independent pre-landing audit caught it and paid for itself on first use.
- **Where a test asserts something does *not* happen, it needs a positive control that proves it can
  fail.** An assertion satisfiable by an inert implementation is not an assertion.
- **Fix the generator, not the output.** A value corrected in a file while the script that writes
  that file still emits the old one is silently reverted by the next build. This happened here: a
  MiB/MB label was fixed in a report while `scripts/cp2_report.py` still divided by 1,048,576 and
  wrote `MB`.
- **A brief that asserts a platform fact must re-verify it.** The CP-3 brief told a Lead that
  Hugging Face's free tier served Docker Spaces. It had stopped two months earlier. The Lead built
  the whole container path against a constraint that no longer existed.
- **Tell a Lead to verify the state it is told it is starting from.** Two separate Leads caught
  factual errors in Orchestrator-issued briefs — wrong SMARD filter IDs, and crossing counts that
  were the two arms stacked rather than the champion's. Both were right.
- **Read a return for protocol defects as well as for its verdict**, and verify the hard gate
  independently rather than re-running the Lead's own suite.
- **Grep for conflict markers when opening a session** — `^<<<<<<<`, `^=======$`, `^>>>>>>>`,
  `Updated upstream`, `Stashed changes`. Commit `30b1b9f` published six of them to a public repo.
- **The holdout is opened once.** v1's is spent permanently. v2 gets its own, and the model that
  ships is the model that was evaluated.

---

## 5. Environment and access

- **Role routing.** `AGENTS.md` is the canonical router and carries the Governance Lockdown;
  `CLAUDE.md` points at it only; `orchestrator-role.md` governs programme management;
  `engineering-role.md` governs execution. `docs/track-b/gauntlet-templates.md` has the four forms.
  > Both `orchestrator-role.md` and `program-stage-sequence.md` carry a **scope-narrowed header**:
  > everything in them about Track A or Track C is historical. Their Track B governance is unchanged.
- **Credentials — never printed, logged or committed.**
  - `MLFLOW_TRACKING_URI`, `MLFLOW_TRACKING_USERNAME`, `MLFLOW_TRACKING_PASSWORD` in `~/.zshrc`.
    **Auth is HTTP basic, not Bearer** — Bearer returns `401`.
  - `HF_TOKEN` via `launchctl setenv`, reaching a session by **process inheritance**. It authenticates
    as `Yarden-Viktor`.
  - `ENTSOE_API_TOKEN` present. **`entsoe-py` 0.8.0 passes it as a query parameter**, so it appears
    in request URLs *and in raised exception text* — redact before logging, and prefer SMARD in any
    unattended job.
  - **Verify anything set in `~/.zshrc` with `zsh -ic`, not `zsh -lc`.** A login but non-interactive
    shell does not source it; an earlier probe reported variables absent and was wrong.
- **Link discipline.** The DagsHub *repository* UI answers `302 → /user/login` anonymously despite
  `private=False`. **Every public link uses the `.mlflow` host**; `scripts/check_links.py` carries the
  four gated URLs as a control.
- **Hugging Face.** Account `Yarden-Viktor`. Docker and Gradio Spaces moved behind paid PRO on
  2026-07-08; **only Static Spaces are free**, and a Static Space never sleeps.
  `hf upload` returns `402` because the CLI calls repo-create even when the repo exists — use
  `HfApi.upload_folder` against the existing Space.
- **Compute.** DagsHub gives tracking, registry and storage and **no compute**. GitHub Actions is
  **free and unmetered for public repositories**. Local: Apple M3, 16 GB, CPU-only, **$0 run rate**.
- **Which check covers what.** `make verify` binds the item-5 *claim* set across surfaces — cutoffs,
  catalog, metrics, evidence class, benchmark. It does **not** check URLs; the test suite and
  `scripts/check_links.py` do. Naming the wrong one in a bar was a real defect found at handover.

---

## 6. Standing scope decisions

**Out, with the reasoning recorded so it is not re-litigated:**

- **Track C — cancelled 2026-09-15.** Outreach, CV surfaces, LinkedIn, target research and interview
  rehearsal left this repository. `TRIG-C` and `C-1` are struck. `שאלות תשובות.docx` is closed at
  **25 entries** and receives no further entries; `AGENTS.md` § *Interview-answer capture* is
  suspended accordingly and retained rather than deleted, so reinstating it is one owner line.
- **Track A — out**, as it already was in practice. `syllabus_v3_2.md` gated nothing.
- **No fuel-price layer.** Re-closed on evidence 2026-09-15: every TTF/THE source found is
  commercial with redistribution-prohibiting terms; ACER publishes a daily *LNG* assessment, not a
  hub price. A reproducible open repository that cannot legally ship its own inputs is not
  reproducible — see [`DATA-LICENSE.md`](DATA-LICENSE.md).
- **Gate-legal weather forecasts begin in 2024.** Open-Meteo's archive reaches 2017 but stitches
  short-lead-time runs, which is look-ahead. **Folds 1–3 are unreachable**, so the data track cannot
  touch the crisis regime and no surface may imply it can.
- **The §5.2 delivery-day availability invariant is law.** Masking delivery-day prices must change
  the output by exactly `0.0`; a D−1 mutation must move it. Currently `220.9433` EUR/MWh.
- **Amendments granted and spent:** WASM for CP-3B only (§9.2's "server mode, not WASM"), and
  sequential conformal for C-2 only (§13's EnbPI/SPCI exclusion).
- **Optional, unscheduled, neither starts on its own:** `Binary Classification Mini-Capstone.md` and
  `aws-extension-spec_v1_1.md` (stale).

---

## 7. Where the history lives

This file no longer narrates it. It is preserved and addressable:

- **The reviewed chains** — `evidence/cp-0`, `evidence/cp-1`, `evidence/cp-2`, `evidence/cp-3`,
  `evidence/cp-3b`. Each landing was a squash with one parent, so the candidate SHAs are **not** on
  `main` and the tag is the only thing preserving them. Verdicts are at
  `docs/track-b/evidence/<cp>/`.
- **v1's ratified plan** — `capstone_V6_8.md`, with its amendment sheets. History, not instruction.
- **M4's reasoning** — `capstone_M4_v2-plan.md`, including the one Orchestrator recommendation the
  owner overruled and why. Superseded by `capstone_v20.md` §4–§5.
- **The defect ledger** — `docs/track-b/cp-0-defects.md`, closed 2026-09-14 after 40 days.
- **v1's results** — `docs/cp2-model-report.md` and `reports/cp2/`. Evidence; not to be changed.
- **Everything else** — `git log`. Commit messages in this repository carry the reasoning, not just
  the change.
