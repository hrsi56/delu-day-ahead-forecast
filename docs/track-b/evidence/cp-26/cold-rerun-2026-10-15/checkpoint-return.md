# Track B Checkpoint Return — CP-26

## Status

BLOCKED — the priced cold-run completion components already exceed the 388-hour cumulative admission gate. The sole-writer pilot also stopped at the unchanged ledger deadline. All work has stopped; CP-26 is incomplete and has no Integration PASS.

## Identity

- Repository: `/Users/djourno/Downloads/PJM`; existing CP-26; `capstone_v21.md` v21-r14, complete §24.7 and all cited supporting sections.
- Anchor SHA-256: `3be866bd10af02cc2b0b956ed91be660dca29a62c0b23b00997bf0b415d100c5`; anchor commit `332baeb861cec5a58516c58a29a1a3afe1eec909`.
- final_candidate_sha: `aff3e274f5670649aaeb359f49aad18d53f9e274` — unreviewed terminal preservation candidate, not a complete or accepted scientific artifact.
- evidence_tip_sha: full descendant SHA in the terminal message; a committed file cannot contain its own SHA.
- `git diff --name-only aff3e274f5670649aaeb359f49aad18d53f9e274..<evidence_tip_sha>`: the closing delta is restricted to `docs/track-b/evidence/cp-26/` and is reported in the terminal validation.
- Scientific run: `cp26-cold-rerun-2026-10-15-01`. Exact delivered brief is preserved by authority commit `63c4684c9e6b2686fa010d540b732e1d1dbabccf`; initial run counter0.000 h; verified historical baseline 65.16212464012295 h.
- Complete verbatim bar: `complete-bar.md`, extracted by main's `scripts/bar.py`;245 lines, section SHA-256 `26d2d73945c1afdfd0e4cd20531a86ea11b8c07f1b47f9b23ea19b6655ec7e90`.

## Repository state

- Existing `gauntlet/cp-26` and Lead checkout retained. No branch, worktree or tag created by this execution; no deletion, publication, push or main operation.
- Material opening mismatch: Lead was at 63c4684 with pending run-accounting changes and tests, rather than expected7b11c8c. Registration already existed; it was verified and reused. No duplicate run/counter was created.
- Primary main is clean at 647d6eb81b2cf6e0cfaf4152f659d689ff973578. All governance and anchors remain unchanged by this execution.
- Deliberately untracked historical exports: `reports/rebaseline/continuation-v21-r14-accounting-3/learning-ledger.json` and `replay-state.json`. Their bytes and all 47 preserved scientific hashes verified unchanged.
- Retained recovery material: primary `.local/artifacts/cp-26/cold-rerun-2026-10-15/` contains Owner brief variants, original job logs, test fixtures and cold metadata; Owned commit-message scratch files are removed during final closing. No replacement worktree or old-run repack was created.

## Complete checklist with direct evidence

All 35 rows of the existing complete-requirements map are carried individually. The full 245-line bar and inheritances govern; EVIDENCED means preserved engineering evidence, never independent acceptance. Evidence paths below are relative to this cold evidence directory unless a repository prefix is shown.

| # | Checklist item | Status | Direct evidence |
|---|---|---|---|
| 1 | Authority and checkpoint continuity (24.7 Outputs/gates; continuation Target/Owner grant) | EVIDENCED | issued-brief.md and registration.json; existing CP-26 branch reused. |
| 2 | Prospective registration and exposure assessment (24.2;24.7 CP28 protocol; continuation preparation) | EVIDENCED | Existing frozen CP-28 protocol retained; exposure assessments in the unchanged exposure ledger; no new exposure. |
| 3 | Boundary, immutable inputs and local-only scope (24.2;24.4;24.5; continuation constraints) | EVIDENCED | namespace-and-population.json and terminal-custody.json; named anchor/inputs/landed model bytes unchanged; zero retrieval/remote writes. |
| 4 | Fresh supervision and owned-process enforcement (continuation preparation finding1) | PARTIAL / STOPPED | 17 bound job endings preserved; guards stopped workers. Concurrent writers and a sole writer failed liveness; no reliable full-run path demonstrated. |
| 5 | Closed repair accounting and cumulative charges (continuation preparation finding2/constraints) | EVIDENCED | resources.json; separate zero-origin run view, all historical charges and2826-second reserve retained; closed repair remains1255.047680753924 seconds. |
| 6 | Production pipeline and restart fixtures (continuation preparation) | PARTIAL | Minimal namespace/attribution/cache-preparation changes and targeted checks; no full scientific production execution. |
| 7 | Harness scope and current bitwise parity (24.7 Harness/parity;24.5 variant parity) | EVIDENCED | Byte-identical reused parity.json:96 checks; harness/member/parity code and input identities unchanged. |
| 8 | Causal controls and DST identity (2;24.4;14.3;23.10 inherited controls) | PARTIAL / REUSED | Unchanged numerical/state algorithms and applicable prior evidence;35 + 2 + 6 + 22 affected checks pass. Initial broad liveness attempt invalid and not reused. |
| 9 | Exact calendar and four frozen masks (24.7 Days; continuation preparation) | EVIDENCED | 2068 eligible measurement days,2078 calendar days,49596 frozen keys;363 warm-up dates;2441 total origins; masks755/358/152 separately registered. |
| 10 | Tier rulings, routes and missing inputs (24.5;15.3; Owner tier rulings) | PARTIAL | Nominal/no-load/GFS +6 routes and CP-25 rulings retained; no new route results. |
| 11 | Sealed fourteen-origin training-only timing pilot (24.7 Ceilings; continuation constraints) | PARTIAL | 946/1064 sealed fresh probes;37/42 complete route/search pairs.118 probes missing after the sole-writer watchdog stop. |
| 12 | Projection and enforced cumulative resource gates (24.7 Ceilings; continuation constraints) | BLOCKED | admission.json:396.30118949385724 h priced subtotal exceeds388 h by 8.30118949385724 h; unresolved reliability cost additionally unpriced. |
| 13 | Forty-two signed support-only search plans (24.7 DDNN2 dates/batches) | EVIDENCED | All 42 fresh signed plans and execution-manifest.json committed at 42083d9 before any timing fit. |
| 14 | Registered sampler, seeds, halving and ranking (24.7 search;23.4) | EVIDENCED | 128 trials, fixed support, seeds and halving unchanged; run-ID metadata only. |
| 15 | All forty-two searches reach terminal outcomes (24.7 search fit/service rules) | NOT RUN | Zero new terminal serving searches; old 42 results retained unused as scientific state. |
| 16 | Exact eight-member ensembles and search failures (24.7 search ensemble/failure rules) | NOT RUN | No new serving ensembles; pilot first-four-configuration fits are timing only. |
| 17 | Fresh daily fits and strict target availability (24.7 Training/information;2;16.2;24.4) | NOT RUN | Zero cold forecast origins;2441 remain. Pilot member fits do not satisfy daily production. |
| 18 | B0, v1-R and released-v1 reference fidelity (24.7 Policies/Failures) | PARTIAL | B0/v1-R implementation and relevant parity retained; no new full-calendar or released-v1 descriptive score rows. |
| 19 | Landed v2-v5 composition and member recipes (24.7 Policies;14.1-2;15.1-3;17.2-3;23.5) | PARTIAL | Fixed landed model/blend recipes unchanged; no new complete forecast vectors. |
| 20 | DDNN2 landed training and emission (23.3-4;23.10;24.7 Policies) | PARTIAL | Training-only DDNN-2 probes retained, including numerical failures; no production D2 ensemble/issuance. |
| 21 | Complete durable forecast provenance (24.7 Ledger;16.2) | NOT PRODUCED | No new forecast ledger. |
| 22 | Landed H construction and original issuance scales (14.2;17.2;23.5;24.7 Failures/Ledger) | NOT RUN | No new H state; old state not imported. |
| 23 | Own-error admission and B0/CQR special rules (24.7 Failures;2) | NOT RUN | No new issued own errors or CQR-scored calendar. |
| 24 | Three predicates, persistent buffers and learning ledger (24.7 Ledger;24.8 ledger rule) | NOT PRODUCED | No new replay/learning ledger; old 575-origin exports remain untracked and hash-preserved. |
| 25 | Failure scoring, calendar retention and threshold disclosure (24.7 Failures) | NOT PRODUCED | No new scored fallbacks or full-calendar1percent report. |
| 26 | Primary scores on all four masks (24.7 Scores primary) | NOT PRODUCED | No new primary score tables on any mask. |
| 27 | Secondary estimands and registered breakdowns (24.7 Scores secondary/breakdowns) | NOT PRODUCED | No new secondary/year/season/hour/day-type/state or realized-outcome score breakdowns. |
| 28 | Bootstrap uncertainty and stored replicates (24.7 Inference bootstrap/sensitivities;Outputs) | NOT PRODUCED | No experimental bootstrap results/replicates; full registered algorithm timing reused only. |
| 29 | Secondary DM/GW/MCS inference (24.7 Inference secondary tests) | NOT PRODUCED | No experimental DM/GW/MCS output. |
| 30 | Calibration and complete moment diagnostics (24.7 Scores calibration) | NOT PRODUCED | No experimental calibration/Christoffersen/moment family output. |
| 31 | Control audit, load bound and GFS fragility (24.7 Claims;24.5; continuation outcome) | NOT PRODUCED | No v2→v3→v4→v5, no-load bound or GFS fragility result; no adoption/demotion decision. |
| 32 | Complete frozen CP28 protocol and state readiness (24.7 CP28 protocol;24.8-9; continuation extract) | PARTIAL | Frozen CP-28 protocol retained unchanged; no arm executed and no new learning state. |
| 33 | Final artifact integrity and truthful report (24.7 Outputs/Ledger; continuation outcome) | PARTIAL | Cold artifacts/receipts/hashes preserved; full scientific report absent. |
| 34 | Local draft publication packet and MLflow export (24.7 Outputs; PUBLISH_RULES1.5 section11) | NOT PRODUCED | No result publication packet or MLflow export generated; public surfaces unchanged. |
| 35 | Fresh binding Integration review and complete terminal return (engineering role; continuation Stop/return/Timebox) | NOT RUN | No Integration Critic launched because the complete artifact is absent. This is a BLOCKED return, not PASS. |

## Admission forecast and actual resources

The complete conservative total is unsupported because reliable ledger progress/recovery remains unpriced. The priced components alone already fail the gate. Historical costs are included once in the current balance; the old recovery-specific additive floor/queue is not used.

| Component | Machine-hours |
|---|---:|
| Cumulative charged balance at pricing | 66.318187 |
| all 2441 daily origins all 3 routes | 206.727953 |
| all 42 cold searches | 44.057609 |
| bootstrap | 5.054281 |
| chronological replay persistence exports | 8.221152 |
| diagnostics | 34.196586 |
| ordinary failure allowance | 29.998455 |
| parity | 0.293291 |
| scoring report draft packet review closure | 1.000000 |
| tests | 0.433676 |
| Priced cumulative subtotal | **396.301189** |
| Additional reliable-supervision/recovery cost | **Unpriced; material** |
| Admission limit | **388.000000** |

The priced new-run subtotal is331.139065 h, excluding historical baseline. Complete new-run/cumulative estimates and expected completion wall time are unavailable. At the last-tested one-worker configuration the priced remaining part alone is329.983003 wall-hours; it is not an admitted completion duration.

Basis: complete historical per-fit coverage for all 42 searches (16.939315 fit-hours), all retained search-attempt overhead (17.423356 allocated hours),2×cold margin and maximum whole12-probe fresh/old timing slowdown1.264326. Daily cost uses the maximum complete old/fresh origin per route×2441×1.25. Statistical algorithm/workload identities remain unchanged. A short79,201,605-byte resource-only serialization probe prices four growing encode/hash traversals and a write per date with 1.5byte-growth margin, fixed replay allowance and one startup/final export pair. No old H/learning object or serving cache was imported. Full basis and all 42 search rows are in admission.json/cost-forecast-blocked.json.

Actual snapshot before closing validation: new-run measured3702.309703 s + reported468.484414 s + reserved0.000000 s = 1.158553922 h; cumulative measured235358.595429 s + reported569.847393 s + retained reserve2826.000000 s = 66.320678562 h. Final closing snapshot is terminal-resources.json and the terminal message.
- Actual cumulative ceiling remains485 h. Historical 2826-second reserve belongs only to cumulative CP-26, not the cold counter. Closed repair usage remains1255.047680753924 seconds.
- Maximum tested registered production allocation was3 workers, one thread/fit; further4th worker was not admitted after swap growth and guard failures. The sole writer also failed after 1974.772537 seconds. The historical CP-26 aggregate RSS peak remains6,968,410,112 bytes; sole-pilot process-tree peak3,248,242,688 bytes, below 12GB. No GPU/cloud/retrieval/remote write.
- Initial broad test invocation inherited the scientific run ID into isolated fixture ledgers and did not honor its required fixture allocation. Its liveness results are invalid and not reused. Original receipt plus a conservative five-process outer-duration charge envelope are retained;65 applicable later checks pass. Early display omission of attributed maintenance receipts was fixed; authoritative cumulative charges were never removed.

## Integration verdict

- Not obtained; no fresh Integration review was launched on an incomplete artifact. No critic verdict is invented. The unreviewed terminal candidate is not a PASS.
- `scripts/gauntlet.py return` is run once for structural diagnostics; missing Integration PASS is the expected non-PASS result. The old checkpoint-root return/brief remain historical bytes; this subdirectory is the fresh Owner-issued run return.

## Reproduction

- `python -B scripts/bar.py check docs/track-b/evidence/cp-26/cold-rerun-2026-10-15/complete-bar.md --source capstone_v21.md@332baeb861cec5a58516c58a29a1a3afe1eec909` — exact quoted bar check.
- `/Users/djourno/Downloads/PJM/.venv/bin/python -B scripts/cp26_rebaseline.py status` — live cumulative and attributed run counters; no running job.
- `find reports/rebaseline/cold-rerun-2026-10-15/timing-pilot -type f | wc -l` —946; required 1064.
- Observed checks:35 affected execution/cost/run-view checks;2 selected supervision checks with 2 declared slots;6gate checks;22analysis/report namespace checks. Commands, exit0 logs, identities and limits are preserved in targeted-validation.json and runs/. Initial invalid broad attempt remains initial-tests.json/log.
- Source/JSON `git diff --cached --check` passed. Unrestricted whitespace checking reports literal trailing spaces in preserved raw pytest logs and unified-diff context; those evidence bytes were intentionally preserved.
- Resource-only cost commands are preserved in runs/cold-persistence-resource-probe-1 and runs/cold-record-blocked-forecast-1. Do not redispatch scientific work against the live ledger while admission is BLOCKED.

## Files changed

- Full path/hash/one-line reason listing: files-touched.json. Small complete code-only diff from the observed opening commit: code-changes.patch. Large generated scientific-plan/probe diffs remain inspectable through Git; no giant full handover patch was generated.
- src/cp26/budget.py: two views over the same receipts, with hot/full-view maintenance charge consistency.
- src/cp26/gates.py, execution.py, search.py: committed cold authority and separate output/cache/state/search identity; numerical recipes unchanged.
- src/cp26/supervisor.py and scripts/cp26_rebaseline.py: existing-cache preparation and monitor run attribution; no guard or cap changed.
- src/cp26/analysis.py and reporting.py: cold output/recovery paths and actual run-authority provenance.
- scripts/cp26_cold_run.py and tests/test_cp26_run_accounting.py: bounded setup/check/pilot entry points and meaningful accounting checks.
- Cold report/evidence paths:42new support plans,946sealed timing probes, resource timings, admission blocker, exact bar, validation and17bound job endings. Historical outputs remain in place.

## Elapsed

Approximately 1.5 wall-clock hours from registration/delivery, about 1.0active hour against the approximate24-active-hour timebox. Unattended worker time is charged separately as machine-hours. The stop is admission/liveness, not timebox exhaustion.

## Open risk or exact owner action

Owner resource/continuation decision required: the priced subtotal exceeds388 h by 8.301189 h before unresolved reliability cost. A complete supported cumulative forecast≤388 h and reliable normal checkpoint progress under the unchanged 0.5 s/2 s guards are prerequisites to full execution. No further automatic retry or scientific workload is running. No locked edit is prepared or requested.
- CP-28 decision summary: unavailable; no fresh control-audit, load-bound, GFS +6 or fallback result exists. No CP-28 arm executed.
- Exposure: no new exposure to post2026-09-06 market data or events.
- Interview trigger: resolving2068eligible days versus the approximate1926description, separate-versus-cumulative spending, and stopping at a measured resource guard; Orchestrator capture only.

## Landing report

- Proposed disposition: retain the existing branch open for the Owner's review/decision, as explicitly requested; no LAND, tag or reclamation is authorized or proposed while CP-26 remains incomplete.
- Evidence tip to preserve: the descendant full SHA in the terminal message; candidateaff3e274f5670649aaeb359f49aad18d53f9e274 remains reachable on gauntlet/cp-26.
- Live documents citing this branch: this return, registration/issued brief, preserved prior checkpoint returns and evidence; no ref retired so no repointing performed.
- Proposed owner commit message: `CP-26: preserve cold-run accounting, timing evidence and blocked admission`.

## Post-return reads

None. No progress.md, orchestrator-role.md, syllabus or Track A/C material was read.
