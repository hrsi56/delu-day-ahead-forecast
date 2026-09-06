# Yarden's Triple-Track Progress Log

*Living document, maintained under `orchestrator-role.md`. **Regenerated 2026-09-06 after a structural change on owner instruction:** the point-in-time capture requirement is dropped, Track A becomes an optional parallel track, and a scope-reduction amendment to `capstone_V6_6.md` is pending owner authorization. Anchors: `capstone_V6_6.md` v6.6 (amendment pending), `syllabus_v3_2.md` v3.2 (**demoted to optional — no longer gating**). `main` = `origin/main` = `d5b0b12`, clean.*

---

## Current Position

### Track A — Learning: OPTIONAL PARALLEL TRACK (owner decision, 2026-09-06)

- **Status change.** Track A is no longer a separate mandatory track with gating checkpoints. The syllabus runs as an **optional parallel resource**: blocks are pulled when a capstone task needs the theory, not on a schedule. **No Track A checkpoint gates any Track B work.**
- **G0 no longer blocks anything.** L5 and the Month-0 deliverables remain available and worth finishing for their own sake — deliverable #2 is genuine interview surface — but they gate nothing and no session opens by asking for a status line.
- **Anchor demoted.** `syllabus_v3_2.md` v3.2 stays a valid reference and is not rewritten or retired. It simply stops being law: nothing in Track B waits on it.
- **What this costs, stated once so it is not rediscovered:** the program loses its forcing function for the math foundations. The capstone will now teach by necessity rather than by curriculum, which is faster and less complete. That is the owner's trade.
- **Month-0 pace is no longer a blocker.** The ~6.5-week overrun is dissolved by this decision rather than absorbed: with Track A optional there is no schedule to overrun.

### Track B — Capstone Builds: the critical path, and now the only one

- **Anchor:** **`capstone_V6_6.md` v6.6**, owner-ratified 2026-08-05. **A scope-reduction amendment is drafted and awaiting owner authorization** — see Blockers.
- **Position: M0 DONE. M0.5/CP-0 CLOSED `PASS`, LANDED (`a911191`), RECLAIMED.** Tags `land/cp-0`, `evidence/cp-0`; earlier attempt archived at `archive/cp-0-attempt-1`. Verdicts at `docs/track-b/evidence/cp-0/`.
- **B-Man-PIT is CANCELLED (owner decision, 2026-09-06).** The point-in-time capture ledger is dropped. **A65/A01 is treated as known-at-forecast-time on the strength of Regulation 543/2013 Art. 6(2)(b)** — publication mandated no later than two hours before gate closure — **corroborated by the 2026-06-12 spike**, which observed A65 present at 15:35 CEST D-1 while A69 was still absent, exactly as the two different regulatory deadlines predict. This is the standard basis used throughout the EPF literature. It is an **assumption, recorded as an assumption**, and must appear as such in §5.2 and in the public limitations section — never as an empirical demonstration.
- **All capture automation deleted, 2026-09-06.** GitHub: workflow, artifacts and repository secret removed. Local machine: `launchd` agent unloaded and deleted, wrapper and token directory removed, logs removed, `caffeinate` holds killed, `data/pit_capture/` removed. No `pmset` setting was ever changed. Nothing remains on either surface.
- **Next Track B action: the scope amendment, then one M1/CP-1 brief.** CP-1's only remaining prerequisite was the capture ledger; with that gone, **M1 is schedulable as soon as the amendment is ratified.**
- **Defect ledger.** `docs/track-b/cp-0-defects.md`: 17 ACCEPTED · D-CP0-18 and D-CP0-19 REMEDIED but not re-tested · D-CP0-20 REMEDIED · AMD-G5 WAIVED. Both open re-tests happen *inside* CP-1 and its landing; neither gates it.
- **Governance Lockdown in force** since 2026-08-08 (`f45e577`), owner-clarified at `3dab960`. Suspensions are task-scoped and spent at terminal return.
- **v6.4 statistical corrections that survive the amendment:** five pinned folds are development/selection evidence with descriptive post-selection DM p-values; complete experiment lineage replaces run counts; M3/CP-3 independently recomputes the CQR fixture and one real calibration fold.

### Track C — Marketing: FROZEN by default

- No Track C block active. Phase-trigger fires after flagship M2. Active applications open after G3 and no later than Month 5 — **both now measured against Track B alone**, since Track A no longer gates.
- **Last published artifact:** `hrsi56/Zero-Trust-Hierarchy`, public, carrying the method article, rulebook, forms and a Pages rendering, plus three Code-Graph-RAG documents at `3ab7e1f`. Separate history and remote; portfolio surface, not a Track B artifact.
- CV iteration budget: three slots across the year.
- **A live job posting was assessed 2026-09-06** (Kamada QA Specialist, Beer-Sheva). Recommendation recorded: not a DS role and not a route to one; eligible but a parallel career ladder. **Open question below — the owner's income runway is unknown and it is the fact that decides it.**

---

## Setup State

- **Project Knowledge swap — owner action pending:** `capstone_V6_6.md` (or its successor once amended), `program-stage-sequence.md` v7, this file, and the current role/router docs. `syllabus_v3_2.md` is now optional reference, not an anchor.
- **NotebookLM:** no longer required. Load the syllabus only if an optional Track A block is actually run.
- **Companion:** stage-gated; must not enter NotebookLM, an engineering repo, or a brief before FM0.
- **Role routing:** `AGENTS.md` is the canonical router and carries the Governance Lockdown; `CLAUDE.md` points to it only; `orchestrator-role.md` governs program management; repo-root `engineering-role.md` governs Track B execution.
- **Canonical templates:** `docs/track-b/gauntlet-templates.md` — ten forms.
- **`ENTSOE_API_TOKEN` has no persistent home on this machine** — it is not in any dotfile, `launchctl setenv`, `.env`, or Keychain. M1 needs it. Store it in a password manager and export it before the M1 brief. **The token was pasted into a chat transcript on 2026-09-06 and should be regenerated at ENTSO-E.**

---

## Strategic Anchors

- **Target:** industry Data Scientist at NIS 35K. Audience: DS hiring manager, not MLE.
- **Authoritative document:** `capstone_V6_6.md` **v6.6** (amendment pending). **This file decides what is law.**
- **Optional reference:** `syllabus_v3_2.md` v3.2 — demoted 2026-09-06, no longer an anchor, not retired.
- **Stage-gated:** `Binary Classification Mini-Capstone.md` v1.0, after CP-5.
- **Planning aid:** `program-stage-sequence.md` v7, static/non-anchor. Its Track A rows are now optional.
- **Parked proposal:** `aws-extension-spec_v1_1.md` — DEC-AWS, adjudicated at G5; would produce capstone v6.7 + map v9.
- **Governance record:** `docs/track-b/rule-inventory.md` (168 live rules) and `docs/track-b/cp-0-defects.md`. Both locked.
- **Repos:** flagship `hrsi56/delu-day-ahead-forecast` (local `/Users/djourno/Downloads/PJM`); public method repo `hrsi56/Zero-Trust-Hierarchy`; companion fraud repo at FM0; standalone CNN repo at DL; ALG solutions repo at ALG-1.
- **Budget/hardware:** $0 expected run rate, $65/month ceiling; M3, 16 GB, CPU-only.
- **Language:** replies and briefs in English; Hebrew input fine.

---

## Standing Scope Decisions

- **Point-in-time availability is ASSUMED, not measured (2026-09-06, owner decision).** A65/A01 is KFT by Regulation 543/2013 Art. 6(2)(b), corroborated by the 2026-06-12 spike. The capture ledger, the owner-run capture block and CP-1's ledger-verification item are dropped. **The assumption is disclosed as an assumption** in §5.2 and in the public limitations section; no document may describe it as empirically demonstrated. Reopening requires new evidence that the regulation is not honoured, not a preference.
- **Track A is optional (2026-09-06, owner decision).** The syllabus is a parallel resource, not a gated track. No learning checkpoint blocks any Track B work. Blocks are pulled on demand when a capstone task needs the theory.
- **Governance Lockdown (2026-08-08, prime directive, owned by `AGENTS.md`).** No agent may modify the rulebook, ratified anchors, governance record, or agent configuration. Halt and request a task-scoped suspension. `progress.md` is Orchestrator-owned state; status/evidence/disposition fields in the defects ledger may be updated without suspension, but acceptance criteria may not.
- **AMD-G5 negative control — WAIVED KNOWINGLY BY THE OWNER, 2026-09-04. Do not raise it again.** `BRIEF_INVALID` remains a valid terminal status; only its deliberate exercise is waived. The compensating control is the Orchestrator's mandatory pre-dispatch brief validation.
- **Owner observance constraint.** No scheduled work on Friday or Shabbat. Calendar-bound blocks schedule Sunday–Thursday.
- **A scheduler's advertised behaviour is not its behaviour (2026-09-06).** GitHub Actions' free scheduler delayed all four crons by 3.0–3.7 hours on its first real day. Never place a hard-deadline job on it. The first real run is the test, for schedulers as for contracts.
- **Reviews of the Gauntlet contract are unscoped by default.** A scope claim is an instruction not to look.
- **Authority limits are stated as scope, never as capability** (D-CP0-20).
- **v6.3 strict-gate architecture:** delivery-day A69 and derivatives forbidden from champion runtime; gate-feasible proxy arms share one pinned proper-training-only A75 climatology.
- **v6.6 Gauntlet contract:** two terminal SHAs with a verdict-only delta; five terminal statuses; role boundary scoped to influence; Landing Report and owner-only squash landing; branch accountability; executor floor and session-freshness preconditions; `reviewed_paths` on the verdict form.
- **Mandatory M1 acceptance oracles (retained):** PT15M chunk stitching; missing-quarter fail-closed; Berlin fall-back-hour identity; A75 proper-training-only fit poisoning with a positive control; champion/benchmark runtime-schema poisoning. A fresh Critic materializes and hashes every fixture outside the candidate checkout.
- **Static first touch:** GitHub Pages primary; marimo Space a labeled deep-dive; no keep-alive on any platform; Monday snapshot + static export; CP-5 carries a <3 s cold-cache gate.
- **Market/data:** DE-LU via ENTSO-E + SMARD, CC BY 4.0. No gas layer, no external weather. A75 is a proper-training-only fit target.
- **Model/scope:** single LightGBM quantile ensemble; CQR then isotonic; no neural challenger, trading layer, live session pulls, DVC, or enterprise monitoring — unless the pre-committed EnbPI reopen fires at M3.
- **Track B authority:** the Orchestrator decides what, when, which repo, which checkpoint, and the ceiling; the Engineering Lead decides how; the Return Packet closes a checkpoint.
- **Publication authority:** all agent work stays local. No push, no PR, no agent commit to `main` except under an explicit session-scoped owner lift. Landing is an owner-authored squash plus two tags.
- **Branch policy:** parallel work expected; every agent-opened branch declared in its terminal return; unaccounted branches escalated, never auto-deleted.

---

## Session Log — newest first

- **2026-09-06 — structural change: capture dropped, Track A demoted, capstone scope amendment drafted.** The owner ended the point-in-time capture effort after six days of accumulating operational friction — a failed GitHub Actions route, a mis-set secret, an empty token file, and a machine that sleeps after one minute — and directed that the data simply be assumed present on the strength of the regulation. All automation was deleted from both GitHub and the local machine, verified. Track A moved from a mandatory gated track to an optional parallel resource, dissolving the ~6.5-week Month-0 overrun and the G0 blocker along with it. The full capstone was then read for scope reduction; a seven-item amendment is drafted and awaiting authorization (Blockers). **The Orchestrator's contribution to the friction is recorded plainly: recommending GitHub Actions for a hard-deadline job, and directing a token-file command without first checking where the token lived.**
- **2026-09-06 — GitHub Actions capture failed its first real day.** All four scheduled runs fired 3.0–3.7 hours late; every one landed past the 12:00 Berlin gate and the guard skipped all four. Zero captures, one lost delivery day. The delay was uniform rather than jitter — the free-tier scheduler deprioritising. Fail-closed behaviour was the only reason this cost a day rather than a corrupted ledger.
- **2026-09-04 — AMD-G5 waived under a granted suspension; publication-metadata question closed on live evidence.** Live probes proved the platform's update-filter machinery works on A80 but is not wired to A65, `createdDateTime` is response-generation time, and SMARD's `created` is file-build time. Record at `docs/pit-metadata-investigation.md`. No contract changed, because the premise failed.
- **2026-09-03 — owner authority clarification; D-CP0-18 remedied at `6ea6a20`.** Lockdown suspensions became task-scoped; `progress.md` confirmed as Orchestrator-owned; the operational-record exception created for the defects ledger.
- **2026-08-10 — D-CP0-20 found and remedied.** `orchestrator-role.md` denied the Orchestrator a shell while the receipt gate required it to run checks. Third instance of one pattern: the rule was right and the thing making it executable was absent.
- **2026-08-08 — Governance Lockdown ratified; CP-0 landed and reclaimed; Phase-5 matrix returned 11 of 13.**
- **2026-08-05/06 — v6.6 ratified and hardened.** Rule inventory 141 → 168. Seven independent review rounds. The clean-room CP-0 re-run validated what text review could not.
- **2026-08-04 — v6.5 capture-schedule amendment** (now superseded by the 2026-09-06 cancellation).
- **2026-07-22 — v6.3 strict-gate amendment.** A69 excluded from champion; four-catalog selection; post-gate benchmark; DuckDB mart; health report.
- **2026-06-12 — Month-0 de-risking spike.** Eight probes; record at `docs/spike-feed-status.md`, evidence SHA `20fc1ff`. Findings that still bind: revision metadata is a dead end; the TP archive is not overwritten; feature feeds are natively PT15M; A69 initial publication is post-gate; ENTSO-E↔SMARD agree 96/96 within €0.01. **A65 present at 15:35 CEST D-1 — now the corroborating evidence the KFT assumption rests on.**
- **2026-06 — launch and conversion:** G0-mid and L1–L4; the M0 spike and v6.1; PJM→DE-LU conversion; program launch 2026-06-09.

---

## Blockers / Open Questions

- **AWAITING OWNER AUTHORIZATION — the scope-reduction amendment to `capstone_V6_6.md`.** Drafted 2026-09-06, seven cuts, quantified at roughly 35–45 engineering hours plus a week of calendar, reducing CP-1 from 17 checklist items to about 12. `capstone_V6_6.md` is a ratified anchor inside the Governance Lockdown, so no agent may apply it: it needs one task-scoped suspension naming the file and the objective. **This is the only thing standing between the program and an M1/CP-1 brief.**
- **OPEN — the owner's income runway.** The Lab Engineer role ended July 2026. Whether income is the binding constraint decides both the Kamada question and whether this program's shape is right at all. Nothing downstream re-plans until this is answered.
- **Post-ratification edits to `capstone_V6_6.md`.** Four repair commits amended the plan after its ratification commit with no version bump. Fold a version marker into the same suspension as the amendment.
- **Locked anchor/map text drift.** `capstone_V6_6.md` §12's build-routing note still names the completed CP-0 re-run as the next brief; `program-stage-sequence.md` v7 carries stale v6/v6.5/v8 labels. Fold into the same suspension.
- **Public README status drift.** `README.md` still says the CP-0 re-run is pending. `README.md` is **not** locked — fix it in the next Track B documentation edit, before M1 goes public-facing.
- Optional/non-blocking: `.zshrc` line-137 dangling-source warning.

---

## Notes for Future Sessions

- **The next Track B action is the amendment, then exactly one M1/CP-1 brief** from `docs/track-b/gauntlet-templates.md` §1 with all eleven required fields and explicit executor preconditions. Do not create the workbench upstream.
- **Pre-dispatch brief validation is the operative front-gate control** now that AMD-G5 is waived. Check every required field before delivering.
- **Do not re-raise:** AMD-G5, the publication-metadata substitution, or the point-in-time capture ledger. All three are closed owner decisions with their reasoning recorded above.
- **The KFT assumption must be disclosed wherever the leakage audit is claimed** — §5.2, the README limitations, and the static page. An assumption stated plainly is defensible; an assumption presented as a measurement is not.
- **Read every Return Packet for protocol defects as well as its checkpoint verdict**, and route any contract fix as its own task under a suspension.
- CP-2 freezes champion lineage; a CP-2 Lead must re-read `capstone_V6_6.md` §4.1. CP-3 adds the CQR fixture recomputation. CP-4/CP-5 preserve lineage and cross-surface claim consistency.
- At each Track B `PASS`: close only that checkpoint, run the §9 landing inspection, take one disposition, take both tags, regenerate this file, and ask "Authorize the next stage?"
- At G5, adjudicate DEC-AWS. If approved, D8 itself authorizes capstone v6.7 + map v9.

---

*Regeneration diff, 2026-09-06. **Structural change, so a full regeneration rather than in-place edits.** **Removed as cancelled by owner decision, each named in the Session Log:** every B-Man-PIT item across Current Position, Blockers and Notes; the capture-automation teardown procedure; the `launchd`/token/`pmset` operational items; the capture-window and observance-scheduling detail tied to them. **Removed as dissolved rather than resolved:** the G0 blocker, the Month-0 overrun escalation, the "absorb the slip or re-plan?" question, and the C2+C8 post-G0 seam item — all were consequences of Track A being a gated track, which it no longer is. The syllabus itself is retained as optional reference and is not retired. **Retained deliberately although Track A is demoted:** L5 and Month-0 deliverable #2, because they are interview surface independent of any schedule. **Added:** the KFT assumption as a standing decision with its disclosure obligation; the Track A demotion; the scheduler lesson; the pending capstone amendment; the token's absence from any persistent store plus the rotation note; and the Kamada assessment with the income-runway question it exposed. **Nothing ratified was changed by this file** — the capstone amendment is drafted and unapplied, and `capstone_V6_6.md` v6.6 remains the anchor until the owner authorizes otherwise.*
