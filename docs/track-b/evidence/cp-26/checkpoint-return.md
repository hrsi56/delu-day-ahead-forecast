# Track B Checkpoint Return — CP-26

## Status
BLOCKED — the measured recovery3 restart projection exceeds the unchanged 388-hour gate. Scientific work is stopped. CP-26 is incomplete; there is no Integration PASS.

## Identity
- Repository: `/Users/djourno/Downloads/PJM`; checkpoint CP-26; `capstone_v21.md` v21-r14, complete §24.7 and all cited supporting clauses.
- Anchor SHA-256: `3be866bd10af02cc2b0b956ed91be660dca29a62c0b23b00997bf0b415d100c5`; Owner continuation authority: `6d00862075102c9c9ea40dc024650a07c0c199d7c78e9c10c38cbdfa68d591db`.
- final_candidate_sha: `8ecaae11790e7b61ba6639760c5ceaf7d819b345` — the **unreviewed terminal candidate**, not an accepted or Critic-reviewed artifact.
- evidence_tip_sha: the full descendant SHA is given in the terminal message; a committed file cannot contain its own commit SHA.
- `git diff --name-only 8ecaae11790e7b61ba6639760c5ceaf7d819b345..<evidence_tip_sha>` is saved in the final local Git packet and reported in the terminal message. The delta is restricted to `docs/track-b/evidence/cp-26/`; it records this return and closing custody only.
- Frozen scientific Source candidate: `e0181812a6da3487efd3faee7da8e53dccd3ec92`. All current Source identity files remain unchanged from that scientific freeze.

## Repository state
- Branch: `gauntlet/cp-26`; existing Lead worktree retained. No new branch or tag was created by this continuation, no ref deleted, no push or remote mutation.
- Primary `main` remains `647d6eb81b2cf6e0cfaf4152f659d689ff973578`; no tracked write, staging, commit or branch switch on main. Owner-ratified anchor/amendment differences visible against main predate this continuation; their bytes are unchanged from the delivered handover.
- Tracked tree is coherent. Two mutable575-prefix exports remain deliberately unstaged/untracked: `reports/rebaseline/continuation-v21-r14-accounting-3/replay-state.json` and `learning-ledger.json`. Their exact hashes and durable byte custody are in `continuation-v21-r14/terminal-custody.json`; the state is79,201,605 bytes and ends 2021-07-28.
- Required decision evidence is committed in normal project paths; retained local caches/backups are recovery material with recorded paths, identities and purposes.

Worktrees declared by the continuation's normal evidence (including the pre-existing Lead, and the twice-created review fixture path):

- `/Users/djourno/Downloads/PJM/.local/worktrees/cp-26/builder-accounting-3`: removed; exact declaration/seed/import/backup records are indexed in terminal-lifecycle.json.
- `/Users/djourno/Downloads/PJM/.local/worktrees/cp-26/builder-numeric-reproduction`: removed; exact declaration/seed/import/backup records are indexed in terminal-lifecycle.json.
- `/Users/djourno/Downloads/PJM/.local/worktrees/cp-26/builder-numeric-review`: removed; exact declaration/seed/import/backup records are indexed in terminal-lifecycle.json.
- `/Users/djourno/Downloads/PJM/.local/worktrees/cp-26/continuation-accounting`: removed; exact declaration/seed/import/backup records are indexed in terminal-lifecycle.json.
- `/Users/djourno/Downloads/PJM/.local/worktrees/cp-26/continuation-analysis-inventory`: removed; exact declaration/seed/import/backup records are indexed in terminal-lifecycle.json.
- `/Users/djourno/Downloads/PJM/.local/worktrees/cp-26/continuation-daily`: removed; exact declaration/seed/import/backup records are indexed in terminal-lifecycle.json.
- `/Users/djourno/Downloads/PJM/.local/worktrees/cp-26/continuation-diagnostic-cells`: removed; exact declaration/seed/import/backup records are indexed in terminal-lifecycle.json.
- `/Users/djourno/Downloads/PJM/.local/worktrees/cp-26/continuation-execution`: removed; exact declaration/seed/import/backup records are indexed in terminal-lifecycle.json.
- `/Users/djourno/Downloads/PJM/.local/worktrees/cp-26/continuation-scoring`: removed; exact declaration/seed/import/backup records are indexed in terminal-lifecycle.json.
- `/Users/djourno/Downloads/PJM/.local/worktrees/cp-26/continuation-supervision`: removed; exact declaration/seed/import/backup records are indexed in terminal-lifecycle.json.
- `/Users/djourno/Downloads/PJM/.local/worktrees/cp-26/lead`: retained existing Lead checkout for Owner review.
- `/Users/djourno/Downloads/PJM/.local/worktrees/cp-26/replay-resource-fixture-builder`: removed; exact declaration/seed/import/backup records are indexed in terminal-lifecycle.json.
- `/Users/djourno/Downloads/PJM/.local/worktrees/cp-26/replay-segments-builder`: removed; exact declaration/seed/import/backup records are indexed in terminal-lifecycle.json.
- `/Users/djourno/Downloads/PJM/.local/worktrees/cp-26/review-context-fixture`: removed; exact declaration/seed/import/backup records are indexed in terminal-lifecycle.json.
- `/Users/djourno/Downloads/PJM/.local/worktrees/cp-26/review-monitor-builder`: removed; exact declaration/seed/import/backup records are indexed in terminal-lifecycle.json.
- `/Users/djourno/Downloads/PJM/.local/worktrees/cp-26/serial-recovery-builder`: removed; exact declaration/seed/import/backup records are indexed in terminal-lifecycle.json.
- `/Users/djourno/Downloads/PJM/.local/worktrees/cp-26/startup-recovery-builder`: removed; exact declaration/seed/import/backup records are indexed in terminal-lifecycle.json.

All created writable Builder and detached fixture worktrees have been removed after exact import/preservation. Earlier five repair worktrees were already removed at delivery; their historical record remains `repair-v21-r14/local-lifecycle.json`. `terminal-lifecycle.json` lists current registered trees, exact declaration records, retained backups/fixtures and disposed test scratch. No unrelated worktree was removed.

## Complete checklist with direct evidence
All 35 rows of the committed complete-requirements map are shown individually. Every row inherits the full named bar and supporting clauses; EVIDENCED means preserved engineering evidence, not independent acceptance. Fixtures do not satisfy an actual experiment item. Paths abbreviated below are relative to `docs/track-b/evidence/cp-26/continuation-v21-r14/` unless their repository prefix is shown.

| # | Checklist item | Status | Direct evidence |
|---|---|---|---|
| 1 | Authority and checkpoint continuity (24.7 Outputs/gates; continuation Target/Owner grant) | EVIDENCED | authority.json; issued-continuation-brief-v21-r14.md; original branch reused. |
| 2 | Prospective registration and exposure assessment (24.2;24.7 CP28 protocol; continuation preparation) | EVIDENCED | execution-protocol.json; cp28-frozen-protocol-v21-r14.md and existing exposure-impact records retained before new training. |
| 3 | Boundary, immutable inputs and local-only scope (24.2;24.4;24.5; continuation constraints) | EVIDENCED | execution-protocol.json; accounting-3-resumption.json; terminal-custody.json ratified pins and unchanged locked documents. |
| 4 | Fresh supervision and owned-process enforcement (continuation preparation finding1) | EVIDENCED | recovery3-resource-fixtures/verification.json; four real isolated cases; original2 s / 0.5 s limits unchanged; production-2 genuine stale-heartbeat stop retained. |
| 5 | Closed repair accounting and cumulative charges (continuation preparation finding2/constraints) | EVIDENCED | terminal-custody.json and original cumulative ledger; repair closed1255.047680753924 s;2826 s reserve retained; failed charges not reset. |
| 6 | Production pipeline and restart fixtures (continuation preparation) | PARTIAL | 74 guarded recovery tests passed; original Source state equivalence/export-recovery fixtures. Unadmitted R3 production continuation remains unrun. |
| 7 | Harness scope and current bitwise parity (24.7 Harness/parity;24.5 variant parity) | EVIDENCED | reports/rebaseline/continuation-v21-r14-accounting-3/parity.json and preserved-preparation-validation.json; no parity rerun or change in this stop phase. |
| 8 | Causal controls and DST identity (2;24.4;14.3;23.10 inherited controls) | EVIDENCED | Source tests/test_cp26_replay.py, state/execution tests and registered frozen protocol; complete calendar execution remains partial. |
| 9 | Exact calendar and four frozen masks (24.7 Days; continuation preparation) | PARTIAL | Frozen2441-origin/2078-measurement calendar,49596 keys/four masks registered;575 origins actually issued. |
| 10 | Tier rulings, routes and missing inputs (24.5;15.3; Owner tier rulings) | PARTIAL | execution-protocol.json; Owner CP-25 rulings and three routes retained; full-calendar variant results pending. |
| 11 | Sealed fourteen-origin training-only timing pilot (24.7 Ceilings; continuation constraints) | EVIDENCED | sealed-pilot-validation.json; active timing-pilot.json and cost-projection.json preserve the14-origin training-only basis and all 42-search pricing. |
| 12 | Projection and enforced cumulative resource gates (24.7 Ceilings; continuation constraints) | BLOCKED | recovery3-preparation/projection-stop.json:382.095264247181+468*172.1430314158788/3600=404.4738583312452 h, above388 h before further overhead. |
| 13 | Forty-two signed support-only search plans (24.7 DDNN2 dates/batches) | EVIDENCED | All 42 signed active search-plans/ and execution-manifest.json retained. |
| 14 | Registered sampler, seeds, halving and ranking (24.7 search;23.4) | EVIDENCED | Frozen src/cp26/search.py;42 actual search-results/; fixed128trials, registered halving/seeds/support rules retained. |
| 15 | All forty-two searches reach terminal outcomes (24.7 search fit/service rules) | EVIDENCED | All 42 active search-results/ and route-search-completion/ terminal records retained; no search rerun. |
| 16 | Exact eight-member ensembles and search failures (24.7 search ensemble/failure rules) | EVIDENCED | stage-checkpoints/ searches evidence and42 terminal search results retain exact four distinct configurations times two seeds. |
| 17 | Fresh daily fits and strict target availability (24.7 Training/information;2;16.2;24.4) | PARTIAL | 83 canonical phase receipts and575 immutable daily issuances; remaining1866 origins and pending physical phases unrun. |
| 18 | B0, v1-R and released-v1 reference fidelity (24.7 Policies/Failures) | PARTIAL | Frozen B0/v1-R Source and575 issued ledgers preserved; released-v1 final descriptive score rows pending. |
| 19 | Landed v2-v5 composition and member recipes (24.7 Policies;14.1-2;15.1-3;17.2-3;23.5) | PARTIAL | Frozen landed member composition and575 policy ledgers preserved; no complete-calendar evaluation. |
| 20 | DDNN2 landed training and emission (23.3-4;23.10;24.7 Policies) | PARTIAL | 42 actual registered search outcomes and daily native caches preserved; complete DDNN2 calendar emission pending. |
| 21 | Complete durable forecast provenance (24.7 Ledger;16.2) | PARTIAL | incidents/production-2/partial-replay-custody.json binds all575 immutable files,19 native members/13 policies and original lineage;2441 required. |
| 22 | Landed H construction and original issuance scales (14.2;17.2;23.5;24.7 Failures/Ledger) | PARTIAL | Preserved575 ReplayState and r14 Source; initialization proves no state/native-cache change; full-calendar H evidence pending. |
| 23 | Own-error admission and B0/CQR special rules (24.7 Failures;2) | PARTIAL | Source own-error/CQR/B0 rules and47-day restart fixture;575 original issued records retained; remaining calendar pending. |
| 24 | Three predicates, persistent buffers and learning ledger (24.7 Ledger;24.8 ledger rule) | PARTIAL | 79,201,605-byte state snapshot, exact575 mutable exports, pending/consumed feedback and learning preserved; full2441 not reached. |
| 25 | Failure scoring, calendar retention and threshold disclosure (24.7 Failures) | NOT COMPLETE | Failed physical jobs retain actual dispositions/charges. Full-calendar policy fallback rates and1% disclosures have not been computed. |
| 26 | Primary scores on all four masks (24.7 Scores primary) | NOT PRODUCED | No CP-26 aggregate score tables computed; four masks remain registered. |
| 27 | Secondary estimands and registered breakdowns (24.7 Scores secondary/breakdowns) | NOT PRODUCED | No full-calendar secondary estimands or registered score breakdown tables. |
| 28 | Bootstrap uncertainty and stored replicates (24.7 Inference bootstrap/sensitivities;Outputs) | NOT PRODUCED | No experimental bootstrap replicates or completed bootstrap manifest; tested/review callers are preparation only. |
| 29 | Secondary DM/GW/MCS inference (24.7 Inference secondary tests) | NOT PRODUCED | No experimental DM/GW/MCS results. |
| 30 | Calibration and complete moment diagnostics (24.7 Scores calibration) | NOT PRODUCED | No complete calibration/Christoffersen/moment family or Holm report. |
| 31 | Control audit, load bound and GFS fragility (24.7 Claims;24.5; continuation outcome) | NOT PRODUCED | No generation-transition conclusion, load-forecast bound or GFS fragility result; complete evaluation is unavailable. |
| 32 | Complete frozen CP28 protocol and state readiness (24.7 CP28 protocol;24.8-9; continuation extract) | PARTIAL | Exact frozen CP28 protocol retained before training; final state readiness and fresh CP26 review absent. CP28 not executed. |
| 33 | Final artifact integrity and truthful report (24.7 Outputs/Ledger; continuation outcome) | NOT PRODUCED | Partial forecasts and complete custody preserved; final report/integrity of whole experimental artifact pending. |
| 34 | Local draft publication packet and MLflow export (24.7 Outputs; PUBLISH_RULES1.5 section11) | NOT PRODUCED | No final local draft publication packet or MLflow result export; no external write. |
| 35 | Fresh binding Integration review and complete terminal return (engineering role; continuation Stop/return/Timebox) | NOT MET | No fresh Integration Critic or verdict. This complete BLOCKED return is not an Integration PASS. |

## Integration verdict
- Path: `docs/track-b/evidence/cp-26/integration.md` — **not produced**. No fresh Integration review was launched because the experiment is incomplete and the mandatory projection gate stopped this implementation.
- Candidate SHA it binds: none. Prior repair/internal reviews do not count as a CP-26 Integration verdict.
- `scripts/gauntlet.py return cp-26 8ecaae11790e7b61ba6639760c5ceaf7d819b345 <evidence_tip_sha>` is run against the final tip and its actual output retained. Its PASS-only check is expected to reject the absent Integration verdict; the validator and bar remain unchanged.

## Reproduction
The actual execution commands below were invoked from the Lead checkout through the original `recovery1_monitor.py monitor --name <recorded name> --workers <recorded allocation> -- <command>`. Original requests, clocks, progress, logs and summaries are preserved in the indicated folders. Tests were not run by Builders. Failed collection/helper jobs keep their actual receipts and charges.

`/Users/djourno/Downloads/PJM/.venv/bin/python -B -m pytest -q docs/track-b/evidence/cp-26/continuation-v21-r14/runners/test_recovery3_resource_liveness.py --basetemp=/Users/djourno/Downloads/PJM/.local/tmp/cp-26/recovery3-resource-guards-1 -o cache_dir=/Users/djourno/Downloads/PJM/.local/tmp/cp-26/recovery3-resource-pytest-cache-1`

Observed exit 0; workers 4; wall 4.472654875018634 s. Evidence: `docs/track-b/evidence/cp-26/continuation-v21-r14/runs/continuation-accounting-3-recovery3-resource-guards-1`.

`/Users/djourno/Downloads/PJM/.venv/bin/python -B docs/track-b/evidence/cp-26/continuation-v21-r14/runners/recovery3_liveness_fixture.py run --snapshot /Users/djourno/Downloads/PJM/.local/artifacts/cp-26/continuation-v21-r14/recovery3-liveness-input/closed-ledger.json --snapshot-sha256 5862c6f26e70290eec00a851f6b4d2fce6347720fd2a1c3f21eacb51f192b98b --output-root /Users/djourno/Downloads/PJM/.local/tmp/cp-26/recovery3-resource-fixture-1`

Observed exit 0; workers 4; wall 191.2452937080525 s. Evidence: `docs/track-b/evidence/cp-26/continuation-v21-r14/runs/continuation-accounting-3-recovery3-resource-fixture-1`.

`/Users/djourno/Downloads/PJM/.venv/bin/python -B -m pytest -q docs/track-b/evidence/cp-26/continuation-v21-r14/runners/test_recovery3_operations.py --basetemp=/Users/djourno/Downloads/PJM/.local/tmp/cp-26/recovery3-operations-tests-1 -o cache_dir=/Users/djourno/Downloads/PJM/.local/tmp/cp-26/recovery3-operations-cache-1`

Observed exit 2; workers 4; wall 3.5612522080773488 s. Evidence: `docs/track-b/evidence/cp-26/continuation-v21-r14/runs/continuation-accounting-3-recovery3-operations-tests-1`.

`/Users/djourno/Downloads/PJM/.venv/bin/python -B /Users/djourno/Downloads/PJM/.local/tmp/cp-26/import_recovery3_test_correction.py`

Observed exit 1; workers 1; wall 4.487945708096959 s. Evidence: `docs/track-b/evidence/cp-26/continuation-v21-r14/runs/continuation-accounting-3-recovery3-test-correction-1`.

`/Users/djourno/Downloads/PJM/.venv/bin/python -B -m pytest -q docs/track-b/evidence/cp-26/continuation-v21-r14/runners/test_recovery3_operations.py --basetemp=/Users/djourno/Downloads/PJM/.local/tmp/cp-26/recovery3-operations-tests-2 -o cache_dir=/Users/djourno/Downloads/PJM/.local/tmp/cp-26/recovery3-operations-cache-2`

Observed exit 0; workers 4; wall 15.241833458072506 s. Evidence: `docs/track-b/evidence/cp-26/continuation-v21-r14/runs/continuation-accounting-3-recovery3-operations-tests-2`.

`/Users/djourno/Downloads/PJM/.venv/bin/python -B docs/track-b/evidence/cp-26/continuation-v21-r14/runners/replay_segments_recovery3.py initialization`

Observed exit 0; workers 1; wall 184.19587008398958 s. Evidence: `docs/track-b/evidence/cp-26/continuation-v21-r14/runs/continuation-accounting-3-recovery3-initialization-1`.

Recorded job names are immutable historical evidence and cannot be redispatched; any newly authorized rerun needs a fresh name and existing guards. Projection arithmetic and custody can be checked read-only from the supplied JSONs and SHAs.

Observed: resource unit suite 56 passed; all 4 real isolated liveness cases completed; operations suite 74 passed, zero skips; initialization ZERO_NEW_ORIGIN_TIMING with zero native-cache writes and unchanged scientific counters/state. Original supervision limits remain2 s / 0.5 s, CPU/BLAS 1, at most4 workers and 12 GB. Short sleep/churn fixtures and synthetic64MiB padding are bounded operational observations, not guarantees for every future production job. Verbatim bar check exited0; full command/output in terminal custody.

## Resource account and decision
The recovery2 whole-run projection remains382.095264247181 h. The exact unadmitted derivative requires468 segment starts. The real chosen repeated initialization sequence took172.1430314158788 s; its two pilot-only cache scans,6.34329129208345 s, are excluded only from repeated-start pricing and retained in the actual pilot charge.

`382.095264247181 + 468 * 172.1430314158788 / 3600 = 404.4738583312452 hours`.

This contractually required minimum pricing subtotal exceeds388 by16.4738583312452 h before future-prefix growth and extra finalizer/custody/admin costs. An additional intentionally double-counting subtotal retaining all subsequent measured work again is416.10460298541085 h at the stop snapshot. These are rejection subtotals, not a complete favorable upper projection. No Q3 JSON/admission or new controller was created, and no scientific origin was added after the575-origin stop.

At terminal packaging, measured=231627.722576554 s, reported=101.323288347 s, retained reserve=2826.0 s; total=65.154179407 machine-hours against485. The repair scope remains closed at1255.047680753924 s; unreconciled reserves=[]. Final packaging ending charges are included in the final authoritative resources stated in the terminal message/packet. `terminal-custody.json` records observed peak RSS/workers and original receipts. All pre-existing closed-job owned identities were independently retired; final packaging is reaped before terminal delivery.

## Files changed
The complete binary-capable main-to-candidate diff, continuation-only diff, both diff stats, status, branch/worktree records and one-line rationale for **each** main-to-candidate file are available at `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26/continuation-v21-r14/terminal-return-2`. `terminal-files-changed.json` commits the full per-file rationale census and `terminal-custody.json` binds packet hashes. The final packet adds the final evidence-only delta/full final diff and exact final status. All patch bytes are independently regenerable from the retained SHAs.

The new recovery callers implement bounded replay/state chains, exact prior-task reconciliation and zero-new finalization; their tests cover Source equivalence, recovery, counter tampering and exact command admission. Resource fixture files and records preserve real clone-only liveness measurements. Incident/prefix records retain original failures and575 scientific issuances. Terminal records preserve this stop and the handover; no locked governance edit was made.

## Elapsed
Approximately43 wall-clock hours since the recorded continuation orientation at2026-10-13T19:13:19Z, to the nearest half hour, including unattended computation. The Owner's timebox is60 active hours, excluding unattended runtime. Exact active time was not separately recorded; it is bounded above by elapsed wall time and has not reached60 h. The projection gate, not the timebox, requires this return.

## Open risk or exact owner action
The Owner must decide how CP-26 proceeds after the404.47 h minimum estimate. This return requests direction for a new recovery approach and fresh admission assessment; it does not authorize resumption, a method or ceiling change, or an anchor edit. The485 h cumulative cap and388 h projected-cost gate remain unchanged. All Track B execution stops at this return.

The preserved scientific record contains all 42 terminal searches and575 original forecast dates through 2021-07-28, with 83 of 352 canonical phases. Remaining 1866 origins, scores, stored uncertainty, diagnostics, full report, draft packet and fresh Integration review are incomplete. Generation transitions, the load-forecast bound, GFS fragility and full-calendar policy fallback rates are **unavailable**, not inferred from partial issuances. CP-28 and automatic publication remain unexecuted.

## Landing report
- Proposed disposition: retain the branch open pending Owner decision; no LAND/DISCARD is inferred or executed. The existing searches and partial causal state have value to preserve. Only the Owner may decide disposition and author any main landing.
- Evidence tip to preserve: the full `evidence_tip_sha` in the terminal message; no tag created or branch reclaimed.
- Live documents citing this branch: the original/repair/continuation briefs and returns, operational custody/admission records and this return. No citation is repointed because no branch is retired.
- Proposed commit message: `CP-26: preserve searches and partial replay; stop recovery at projection gate`.

## Exposure and interview-answer triggers
Exposure: no credential value seen/emitted and no new CP-26 aggregate score/inference viewed or computed; prior exposure-impact records remain unchanged. Partial forecast/state inspection served causal recovery and custody. No Orchestrator-only record was edited.

Interview-answer triggers for the Orchestrator: preserving scientific identity while changing operational boundaries; measuring real liveness through isolated ledgers; retaining failures and uncertainty about stale-heartbeat causation; distinguishing resource charges from scientific counters; stopping when measured restart costs invalidate a prospective budget. The Lead files no interview-answer document.

## Post-return reads
none. No `progress.md`, `orchestrator-role.md`, syllabus or TrackA/C material was read. No program-state update, CP-28 execution, publication or remote write.
