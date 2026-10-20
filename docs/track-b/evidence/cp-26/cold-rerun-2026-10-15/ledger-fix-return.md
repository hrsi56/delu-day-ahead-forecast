# Track B Checkpoint Return — CP-26

## Status

BLOCKED — the fixed retry-count defect no longer terminates valid refreshes early, but the same pilot still hits the actual0.5s ledger deadline at one worker.51probes remain. The cost gate has not passed.

## Identity

- Repository: `/Users/djourno/Downloads/PJM`; Lead: `.local/worktrees/cp-26/lead`; existing run `cp26-cold-rerun-2026-10-15-01`.
- Anchor: capstone_v21.md, v21-r14, complete§24.7 and inherited requirements; SHA256 `3be866bd10af02cc2b0b956ed91be660dca29a62c0b23b00997bf0b415d100c5`, anchor commit `332baeb861cec5a58516c58a29a1a3afe1eec909`.
- final_candidate_sha: `80f12d09690aa34813c9b715b5cf5edc3a351037` — terminal candidate, unreviewed.
- evidence_tip_sha: the descendant full SHA supplied in the terminal response. This file and the checklist/validation metadata bind the candidate; they are preserved in evidence-only commits above it.
- Run `git diff --name-only 80f12d09690aa34813c9b715b5cf5edc3a351037..<evidence_tip_sha>`; every resulting path must stay inside docs/track-b/evidence/cp-26/. Actual verified output is preserved in the terminal validation record.
- Exact full bar: complete-bar.md; scripts/bar.py check exited0 against the pinned anchor commit.

## Repository state

- Branch: gauntlet/cp-26, retained for Owner review; candidate83ahead/0behind main. No branch, worktree or tag created by this addendum task.
- Tracked tree clean at candidate. Deliberately untracked historical exports remain:
  - reports/rebaseline/continuation-v21-r14-accounting-3/learning-ledger.json
  - reports/rebaseline/continuation-v21-r14-accounting-3/replay-state.json
- main remains clean at647d6eb81b2cf6e0cfaf4152f659d689ff973578; nothing staged on main, no push, remote write, tag, governance edit or CP-28 execution.
- Both runs, prior authority/admission/return records, all47historical scientific hashes and all946initial cold-probe bytes are preserved. No new scientific run or ledger was created.

## Complete checklist with direct evidence

| # | Checklist item | Status | Direct evidence |
|---|---|---|---|
| 1 | Authority and checkpoint continuity (24.7 Outputs/gates; continuation Target/Owner grant) | EVIDENCED | issued-ledger-fix-addendum.md and ledger-fix-authority.json preserve actual direct Owner authority at verifiedc1685ee; same run and branch, no reset. |
| 2 | Prospective registration and exposure assessment (24.2;24.7 CP28 protocol; continuation preparation) | EVIDENCED | Existing frozen CP-28 protocol retained; exposure assessments in the unchanged exposure ledger; no new exposure. |
| 3 | Boundary, immutable inputs and local-only scope (24.2;24.4;24.5; continuation constraints) | EVIDENCED | ledger-fix-terminal-custody.json verifies47unchanged historical hashes and946initial probe bytes; locked anchor hash unchanged; zero retrieval/remote writes. |
| 4 | Fresh supervision and owned-process enforcement (continuation preparation finding1) | PARTIAL / STOPPED | 23bound cold-run job endings retained, including6new jobs. The patched one-worker supervisor timed out after0.5312975411070511s with2conflicts; all workers stopped and ownership identities gone/reused. |
| 5 | Closed repair accounting and cumulative charges (continuation preparation finding2/constraints) | EVIDENCED | ledger-fix-resources.json and the live ledger retain both views, all prior charges,2826s historical reserve and the closed repair snapshot; no reset. |
| 6 | Production pipeline and restart fixtures (continuation preparation) | PARTIAL | Premature retry-count exhaustion removed.21targeted checks pass; actual refresh deadline remains a demonstrated blocker, without a general repair framework. |
| 7 | Harness scope and current bitwise parity (24.7 Harness/parity;24.5 variant parity) | EVIDENCED | Byte-identical reused parity.json:96 checks; harness/member/parity code and input identities unchanged. |
| 8 | Causal controls and DST identity (2;24.4;14.3;23.10 inherited controls) | PARTIAL / REUSED | Prior65applicable controls/namespace/gate checks reused;21new affected refresh/deadline/once-only/receipt/run-view checks pass. Scientific/model/state bytes unchanged. |
| 9 | Exact calendar and four frozen masks (24.7 Days; continuation preparation) | EVIDENCED | 2068 eligible measurement days,2078 calendar days,49596 frozen keys;363 warm-up dates;2441 total origins; masks755/358/152 separately registered. |
| 10 | Tier rulings, routes and missing inputs (24.5;15.3; Owner tier rulings) | PARTIAL | Nominal/no-load/GFS+6 routes and CP-25 rulings retained; no new route results. |
| 11 | Sealed fourteen-origin training-only timing pilot (24.7 Ceilings; continuation constraints) | PARTIAL | 1013/1064 sealed probes,40/42complete route/search pairs,67new terminal probes;51remain after the genuine single-worker elapsed timeout. All946prior bytes unchanged. |
| 12 | Projection and enforced cumulative resource gates (24.7 Ceilings; continuation constraints) | BLOCKED | ledger-fix-blocked-admission.json: priced subtotal396.461873518717h, minimum shortfall8.461873518717h; complete reliable refresh/recovery cost remains unsupported. No full workload admitted. |
| 13 | Forty-two signed support-only search plans (24.7 DDNN2 dates/batches) | EVIDENCED | All42 fresh signed plans and execution-manifest.json committed at42083d9 before any timing fit. |
| 14 | Registered sampler, seeds, halving and ranking (24.7 search;23.4) | EVIDENCED | 128 trials, fixed support, seeds and halving unchanged; run-ID metadata only. |
| 15 | All forty-two searches reach terminal outcomes (24.7 search fit/service rules) | NOT RUN | Zero new terminal serving searches; old42 results retained unused as scientific state. |
| 16 | Exact eight-member ensembles and search failures (24.7 search ensemble/failure rules) | NOT RUN | No new serving ensembles; pilot first-four-configuration fits are timing only. |
| 17 | Fresh daily fits and strict target availability (24.7 Training/information;2;16.2;24.4) | NOT RUN | Zero cold forecast origins;2441 remain. Pilot member fits do not satisfy daily production. |
| 18 | B0, v1-R and released-v1 reference fidelity (24.7 Policies/Failures) | PARTIAL | B0/v1-R implementation and relevant parity retained; no new full-calendar or released-v1 descriptive score rows. |
| 19 | Landed v2-v5 composition and member recipes (24.7 Policies;14.1-2;15.1-3;17.2-3;23.5) | PARTIAL | Fixed landed model/blend recipes unchanged; no new complete forecast vectors. |
| 20 | DDNN2 landed training and emission (23.3-4;23.10;24.7 Policies) | PARTIAL | Training-only DDNN-2 probes retained, including numerical failures; no production D2 ensemble/issuance. |
| 21 | Complete durable forecast provenance (24.7 Ledger;16.2) | NOT PRODUCED | No new forecast ledger. |
| 22 | Landed H construction and original issuance scales (14.2;17.2;23.5;24.7 Failures/Ledger) | NOT RUN | No new H state; old state not imported. |
| 23 | Own-error admission and B0/CQR special rules (24.7 Failures;2) | NOT RUN | No new issued own errors or CQR-scored calendar. |
| 24 | Three predicates, persistent buffers and learning ledger (24.7 Ledger;24.8 ledger rule) | NOT PRODUCED | No new replay/learning ledger; old575-origin exports remain untracked and hash-preserved. |
| 25 | Failure scoring, calendar retention and threshold disclosure (24.7 Failures) | NOT PRODUCED | No new scored fallbacks or full-calendar1percent report. |
| 26 | Primary scores on all four masks (24.7 Scores primary) | NOT PRODUCED | No new primary score tables on any mask. |
| 27 | Secondary estimands and registered breakdowns (24.7 Scores secondary/breakdowns) | NOT PRODUCED | No new secondary/year/season/hour/day-type/state or realized-outcome score breakdowns. |
| 28 | Bootstrap uncertainty and stored replicates (24.7 Inference bootstrap/sensitivities;Outputs) | NOT PRODUCED | No experimental bootstrap results/replicates; full registered algorithm timing reused only. |
| 29 | Secondary DM/GW/MCS inference (24.7 Inference secondary tests) | NOT PRODUCED | No experimental DM/GW/MCS output. |
| 30 | Calibration and complete moment diagnostics (24.7 Scores calibration) | NOT PRODUCED | No experimental calibration/Christoffersen/moment family output. |
| 31 | Control audit, load bound and GFS fragility (24.7 Claims;24.5; continuation outcome) | NOT PRODUCED | No v2→v3→v4→v5, no-load bound or GFS fragility result; no adoption/demotion decision. |
| 32 | Complete frozen CP28 protocol and state readiness (24.7 CP28 protocol;24.8-9; continuation extract) | PARTIAL | Frozen CP-28 protocol retained unchanged; no arm executed and no new learning state. |
| 33 | Final artifact integrity and truthful report (24.7 Outputs/Ledger; continuation outcome) | PARTIAL | ledger-fix-terminal-custody.json preserves both runs,23cold job endings,1013probes and47oldhashes; no full scientific report. |
| 34 | Local draft publication packet and MLflow export (24.7 Outputs; PUBLISH_RULES1.5 section11) | NOT PRODUCED | No result publication packet or MLflow export generated; public surfaces unchanged. |
| 35 | Fresh binding Integration review and complete terminal return (engineering role; continuation Stop/return/Timebox) | NOT RUN | Full35row checklist and exact bar retained. Artifact incomplete; no Integration review or checkpoint PASS claimed. |

## Integration verdict

No Integration review was launched because the complete baseline artifact is absent. No integration.md or PASS is fabricated. The candidate is unreviewed.

## What changed and what stopped

The original `_resource_update` branch rejected a third cold-history conflict even before its deadline. Commit85733d256ad3dbba0a62ba267dd0ec9347e78a4d removes that separate retry-count limit. Refreshes and all preparation/acquisition/body/rename checks still use the original absolute deadline. Refresh-specific deadline expiry is labelled explicitly; there is no conflict-exhaustion error left. Flock, exact cold-byte proof, ownership/receipt checks and once-only mutation logic are unchanged.

The21targeted checks passed in2.46s under a four-slot outer monitor, allocated7.2415664159925655×4worker-seconds. They demonstrate five valid conflicts resolving inside0.5s for both resource mutation and evidence-task append, actual deadline expiry with no partial charge, duplicate-task idempotency and existing receipt/ownership/counter protections.65prior applicable checks and96bitwise parity checks remain applicable; no broad suite or separate repair Critic was run.

Three pilot jobs were attempted. A simultaneous reservation failed before registering a worker; its log and conservative reported cost are retained. The subsequent serialized reservation succeeded. One shard completed24missing probes; the other two stopped at real elapsed deadlines. Swap rose from5890.06MiB to7940.31MiB during startup, so no fourth worker was admitted. All of those jobs ended before the single-worker continuation.

The one-worker continuation advanced another43probes, then its supervisor stopped at187.57450433296617allocated wall-seconds. The failing ledger transaction read8617677bytes, had2conflicts/2attempts, body0s, maximum hold0.0020361669594421983s, wait0.03448404208756983s and total0.5312975411070511s. Its receipt records `outcome=timeout`, no write, workers_stopped=true and group_empty=true. This is actual elapsed timeout, not the removed retry-count cutoff. No further scientific retry followed.

Terminal pilot:1013/1064probes,67new,40/42complete route/search pairs,51missing. No successful probe was rerun or relabelled. No new terminal serving search, forecast, ensemble, native fit cache, H/learning state or score was created.

## Admission and compact cost table

The updated admission is BLOCKED. Current charges are added once; previous full-run estimates are not added to completed actuals. All previous rejected records remain unchanged.

| Remaining priced component | Machine-hours |
|---|---:|
| all2441 daily origins all3 routes | 206.727953 |
| all42 cold searches | 44.057609 |
| bootstrap | 5.054281 |
| chronological replay persistence exports | 8.221152 |
| diagnostics | 34.196586 |
| ordinary failure allowance | 29.998455 |
| parity | 0.293291 |
| scoring report draft packet review closure | 1.000000 |
| tests | 0.433676 |
| Remaining priced subtotal | 329.983003 |
| Cumulative balance used at pricing | 66.478871 |
| Priced cumulative subtotal | 396.461874 |
| Minimum shortfall above388 | 8.461874 |

Priced new-run subtotal: 331.299749h, excluding the65.16212464012295h original baseline. Complete supported cumulative/new-run completion estimates and expected completion wall time remain unavailable:51sealed probes and a reliable bounded refresh path are still missing. At one worker the priced remaining part alone is329.983003wall-hours; this is not an admitted completion duration. The complete forecast entry point was preserved but never executed because its full-pilot/successful-receipt prerequisites failed. No production cost-projection.json was generated.

Basis remains complete historical resource coverage for all42cold searches, including all retained attempts rather than resumed successful tails, a2×cold margin and maximum whole12-probe slowdown. Daily cost retains the maximum complete old/fresh route/origin×2441×1.25. Bootstrap/diagnostic algorithms and workload identities are unchanged. Growing persistence/export cost retains the measured79MB serialization sample, four traversals per date,1.5growth margin and chronological replay/start/final-export allowance. The10%future failure allowance is retained. A finite reliable refresh/recovery allowance remains unsupported; this is reported explicitly, never filled with zero. Thus the priced subtotal is a lower bound, already above388h.

## Resources

The authoritative account remains `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26/ledger/budget.json`; JSON evidence files are timestamped snapshots of that same account.

- Original historical baseline:65.16212464012295h; original run counter began0.000h and was not reset.
- At this return snapshot, new run: measured4223.598877619s, reported520.484414500s, reserved0.0s; total1.317800914h.
- At this return snapshot, cumulative CP-26: measured235879.884603506s, reported621.847393055s, retained reserve2826.0s; total66.479925555h. Final packaging charges are included in the terminal message's final live totals.
- Closed historical repair remains1255.047680753924s and inactive. Actual ceiling485h, admission388h, ledger0.5s, heartbeat2s, workers≤4, BLAS1, CPU-only and RSS12000000000bytes unchanged.
- Six new monitored jobs;23cold-run ending receipts total preserved. All jobs ended and all owned identities verified gone/reused. No unresolved reserve or orphan. Latest one-worker peak RSS3342909440bytes.
- Existing detached supervisors and caffeinate lifetime support used. No power, swap, priority, affinity, cron, LaunchAgent, heartbeat or watchdog-policy changes.

## Reproduction

- `git show 85733d256ad3dbba0a62ba267dd0ec9347e78a4d -- src/cp26/budget.py tests/test_cp26_ledger_liveness.py` — exact narrow fix; ledger-fix.patch contains the complete zero-context source diff.
- ledger-fix-tests.json and runs/cold-ledger-fix-checks-1 bind the exact pytest.main command,21passes and successful supervised receipt. Do not run unmonitored test compute against the live account.
- `python -B scripts/bar.py check docs/track-b/evidence/cp-26/cold-rerun-2026-10-15/complete-bar.md --source capstone_v21.md@332baeb861cec5a58516c58a29a1a3afe1eec909` — exit0.
- `python -B scripts/cp26_rebaseline.py status` — live cumulative and run views; no running jobs.
- Count timing-pilot/*/*/*.json —1013; no timing-pilot.json or production cost-projection.json exists.
- ledger-fix-terminal-custody.json binds all original/current probe hashes,47historical hashes,23job receipts and all ending identities. The new admission is ledger-fix-blocked-admission.json; old admission.json remains unchanged.
- Source/JSON scoped whitespace checks passed; raw retained receipt logs remain verbatim.

## Files changed

130files changed,10389insertions(+),32deletions(-) between the opening tip and final candidate. Full per-path diff stat: ledger-fix-diff-stat.txt. Each of130candidate paths,its candidate hash and one-line reason: ledger-fix-changed-files.json; grouped source rationale: ledger-fix-file-reasons.json. The source diff is ledger-fix.patch; complete generated artifact diffs remain in Git without another giant handover patch.

- src/cp26/budget.py: remove premature retry exhaustion while keeping the absolute deadline.
- tests/test_cp26_ledger_liveness.py: five-conflict success, real timeout and once-only invariants.
- preparation-tests.json: truthful current operational-code identity,21newchecks and65applicable reused checks.
- New cold-run timing files:67registered terminal probes.
- New cold evidence: exact Owner addendum/authority, targeted test/provenance, six job endings, failed reservation, actual timeout blocker, updated partial forecast, hashes and terminal return/checklist.
- ledger-fixed-forecast.py is an unexecuted prospective full-pilot cost entry point, explicitly blocked on missing prerequisites. It grants no admission.

## Elapsed

Approximately0.5elapsed hour including orientation and terminal preservation, against the existing approximate24active-hour timebox. The stop is a real guard failure and unsupported admission, not timebox exhaustion. Unattended worker time is separately accounted above.

## Open risk or exact next prerequisite

The remaining technical blocker is an authoritative8.62MBcold-history refresh that exceeds0.5s even with one registered fit worker. The exact next acceptance test is recorded in ledger-fix-blocker.json: bounded real refresh/evidence append under live supervision without duplicate task/counter mutation, then the51remaining registered probes. No guard relaxation, broad recovery framework, repeated failed-fit retry or locked-file edit was made or prepared.

A complete supported forecast≤388h remains mandatory for full training. The existing priced subtotal is already8.461874h over that line before unresolved material operational cost. There is no admission PASS, no full training and no CP-28 arm. No favorable scientific result is assumed or sought.

Interview trigger for Orchestrator capture: distinguish premature retry exhaustion from actual elapsed-time expiry using once-only counters and measured receipts; the latter remained a genuine execution blocker. No interview document was edited.

## Landing report

- Proposed disposition: retain the existing gauntlet/cp-26 branch and Lead for Owner review as requested; no LAND, tag, reclamation or deletion proposed while incomplete.
- Evidence tip to preserve: the descendant full SHA in the terminal response; candidate80f12d09690aa34813c9b715b5cf5edc3a351037 remains reachable on gauntlet/cp-26.
- Live documents citing the branch: this return, previous returns, authority/registration and existing CP-26 evidence. No ref was retired; no repointing needed.
- Proposed Owner commit message: `CP-26: fix premature ledger retry exhaustion and preserve blocked pilot continuation`.
- Retained local materials: primary `.local/artifacts/cp-26/cold-rerun-2026-10-15/ledger-fix/` contains launcher originals and candidate identity. Disposable targeted pytest fixtures were removed after their successful evidence was committed. Committed evidence is the durable copy. This task's disposable commit-message scratch files are removed before terminal return.

## Post-return reads

None. No progress.md, orchestrator-role.md, syllabus or Track A/C material was read.
