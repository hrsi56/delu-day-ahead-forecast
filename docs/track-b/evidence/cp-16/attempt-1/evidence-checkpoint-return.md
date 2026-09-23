# Track B Checkpoint Return — CP-16

## Status

**BLOCKED** — completing the authorized evaluation needs an Owner-ratified replay allowance. This is not a completed negative research result. The Lead's initial accounting omitted synthetic warm-up, and the original resource supervisor had a fail-open defect; both are disclosed below and preserved in evidence.

## Identity

- Repository: PJM, /Users/djourno/Downloads/PJM.
- Checkpoint: CP-16 only; ratified capstone_v21.md v21-r2, complete §14.8.
- final_candidate_sha: **3a160fd33ed92bb0061144cfbce2323d8b3a7db9**.
- evidence_tip_sha: **SELF_COMMIT**. Resolve with `git log -1 --format=%H -- docs/track-b/evidence/cp-16/checkpoint-return.md` at this retained branch; the exact resolved full SHA is supplied in the terminal receipt/rendered return. A committed file cannot literally contain its own content-derived Git SHA.
- `git diff --name-only 3a160fd33ed92bb0061144cfbce2323d8b3a7db9 SELF_COMMIT`: **EVIDENCE_DELTA**. Every path must be under docs/track-b/evidence/cp-16/. The exact command output is retained in the rendered terminal packet after commit.

## Repository state

- Branch: **gauntlet/cp-16**, opened solely for this authorized local candidate/evidence chain. Clean after evidence commit; 3 commits ahead of main, 0 behind. Tip is evidence_tip_sha above.
- Main remains 6621402b2be9aed85be433432bcffffb56adf3e4. Nothing was staged or committed on main; nothing pushed. Pre-existing Owner/other-session status is preserved in main-state.txt. No unknown branch was encountered.
- Lead worktree: .local/worktrees/cp-16/lead, seeded at 6621402b2be9aed85be433432bcffffb56adf3e4, retained for Owner review.
- Builder worktrees .local/worktrees/cp-16/builder-residual and builder-scoring: same seed, bounded owned source/tests imported, then both removed under this checkpoint's lifecycle.
- Fresh Critic worktree .local/worktrees/cp-16/critic: detached at final_candidate_sha, clean before/after; removed after verdict import. Review isolation was cooperative read-only, not sandbox-enforced.
- Tags created: **none**. Branch disposition is unassigned; Owner decision required before reclamation.
- All checkpoint scratch/worktrees/cache remain project-local. Retained .local/artifacts/cp-16 contains ledger/log recovery, full diff and rendered packet; .local/tmp/cp-16 contains exact review scripts/assignment and test fixtures. Required decisions, logs, raw interrupted evidence, scripts and verdict are committed in normal paths; none exist only in scratch.

## Complete checklist with direct evidence

| # | Checklist item | Status | Direct evidence |
|---|---|---|---|
| 1 | Verify repository/input state; preserve prior work; commit immutable inputs and complete pre-run identities/keys | PARTIAL | Matching supplied hashes; e625967 pre-run commit; input-manifest. Resource preflight missed synthetic warm-up usage. |
| 2 | Implement only fixed A1/B2 central blend and H/P; freeze on permitted training data | PARTIAL | src/cp16/residuals.py; pre-run protocol; first fold seven admission dates only. Four folds not admitted. |
| 3 | Prove availability, transforms, D-2/once, warm-up/DST, fallback, cache and restart with controls | PARTIAL | 19 residual synthetic tests and inherited controls passed before stop; one saved training reproduction recorded. Required production causal fits and all-fold proof incomplete. |
| 4 | Forecast every original key with shared counts, failures, finite ordered emitted quantiles | UNMET | Expected keys retained: 2160/2159/2112/2160/2156. No outer predictions; required 75229 rows absent. |
| 5 | Independently verify scores/normalization and all diagnostics; re-score five saved references | UNMET | Scoring implementation/synthetic fixtures exist; production metrics, diagnostics and reference re-scoring not executed. |
| 6 | Apply ranking, paired uncertainty, joint-preference rule and six original diagnostics | UNASSESSED | No comparison or bootstrap executed. Historical CP-15 NOT_DEMONSTRATED unchanged; no delivery eligibility. |
| 7 | Enforce/report all resource caps including warm-up, failed attempts, controls and review | FAIL | Corrected 3730/4500 policy-days; 1200 needed versus 770 remaining. Supervisor gap and early Builder thread/concurrency evidence limitations disclosed. |
| 8 | Durable protocol, lineage, outputs, failures/resources, reproducibility; controls/regressions | PARTIAL | Protocol, complete key manifest, partial lineage, failure/resource logs and bounded reproduction supplied. Required scientific output files absent. |
| 9 | Fresh independent Integration PASS on exact clean detached final candidate | FAIL | Fresh Critic reviewed exact candidate; missing full evaluation prevents PASS. See integration.md. |
| 10 | Canonical packet, terminal SHAs/evidence delta/reachability/ref accounting; stop at CP-16 | HANDOVER ONLY | This packet and terminal receipt; evidence-only final delta. Branch awaits Owner disposition. No later checkpoint work. |

## Integration verdict

- Path: docs/track-b/evidence/cp-16/integration.md. Result: **FAIL**.
- Candidate bound: 3a160fd33ed92bb0061144cfbce2323d8b3a7db9.
- Actual Critic:/root/integration_critic; Lead:/root, thread 01a0cb93-625c-7213-aa6b-825ac1c4f5a3. Fresh no-history review; exact bar, commands/exits and ten separate judgments preserved. The verdict was imported byte-for-byte.
- 59 bounded tests passed in independent review; original keys and artifact hashes matched. No scientific comparison, model refit or residual replay was performed in review. Missing deliverables and incomplete resource evidence prevent PASS.

## Research and product state

- Historical CP-15 product feasibility: **NOT_DEMONSTRATED**, unchanged.
- New original-§8 diagnostics: **unassessed**; complete-forecast acceptance itself is unmet.
- Descriptive H/P ranking and joint preference: **unassessed**, since no outer comparison exists.
- Product/delivery eligibility: **not authorized**. No economics, promotion, registry action or live clock.
- All new development artifacts remain development_post_selection. No preference or equivalence conclusion is inferred from interruption. Inherited A65 vintage/data-revision limitations remain.

## Reproduction

- Exact bounded commands and prerequisites: reports/v2-causal/reproduce.md; actual command/exit/output details: integration.md and committed logs.
- Before fits: 49 tests passed, and the exact pre-run protocol was committed at e625967e20f3f79f2c4d07c9b414065ff0717d02.
- Repair verification: 7 monitor/input tests passed; the added blocked-execution guard passed separately; 25 inherited boundary/live-namespace checks passed. Independent review reran 34 monitor/input/scoring tests plus 25 inherited guards successfully.
- Preflight enumerated 638 date-fold keys and all 10747 target keys per policy. Admission retained 37 fold-1 origins, 7 admission dates and 8 new component-date pairs. The recorded cache reproduction matched both components and fingerprints; independent production reproduction remains incomplete.
- Required predictions.parquet, metrics.csv, diagnostics.csv, uncertainty.csv and criteria.csv are absent. No partial summary is passed off as a full score.

## Resources and defects

- **Policy-days: 3730/4500** (3654 conservative synthetic controls including warm-up/failed attempts/restored pending state; 76 production reservations). Remaining 770 versus 1200 needed to finish the planned production pass; shortfall 430 before outstanding controls and review.
- Component attempts: 21/2000 total, 17/1500 main. Primitive Lasso calls: 2494/240000; inner: 1996/192000; final: 498/48000. Interrupted attempts remain counted.
- Aggregate charged machine time: 624.085567 seconds (0.1734 hours)/24 machine-hours, including conservative pre-instrumentation/tail charges and the Critic's failed audit attempt.
- Monitored peak process-tree RSS: 1256341504 bytes. Historical unmonitored peak RSS, aggregate worker count and early Builder BLAS pinning are **unknown**, not retrospectively certified. resource-final.json and Integration findings qualify the unsupported global summary claims in the older candidate resources.json.
- Peak monitored disk accounting, conservatively including the whole Git store: 567967852 bytes/20 GiB. Existing environment reused; 0 new dataset/model download bytes; external cost $0.
- Implemented output policies 2, saved references planned 5, scored policies 0, new residual recipes 1 plus pooled control 1, feature recipes 1, central configurations 2, model seed 42 and bootstrap seed 15042, ensemble members 2. No new recipe/outer search, neural/VRE/weather/economic run, GPU/cloud job, operational day, schedule or remote mutation. Production bootstrap/reference score passes 0/3 each.
- Initial synthetic accounting reported successful predictions only; corrected using preserved actual test history. No overlap discounts were used. Earlier raw test outputs and the first fixture failure are retained in residual-builder-audit.md.
- The original disk monitor lost a temporary JSON path during atomic rename and exited while its child remained running. The Lead interrupted the child, preserved the raw prefix and traceback, and charged a conservative elapsed upper bound. The repaired monitor tolerates disappearing paths, kills its process group on monitor failure, and refuses scientific execution while the protocol is BLOCKED.
- A Critic audit initially compared timestamp storage resolutions directly and failed; the corrected audit normalized both to nanoseconds and confirmed every UTC key. Both scripts, outputs and charged jobs are retained.

## Files changed

`git diff --stat main...SELF_COMMIT` and the full diff are retained in .local/artifacts/cp-16/final-stat.txt and final-full.diff and embedded/referenced by the rendered terminal packet. The baseline delta contains only the three expressly supplied immutable packaging files and the authorized CP-16 envelope.

| File | Reason |
|---|---|
| capstone_v21.md | Exact Owner-supplied ratified anchor bytes; packaged without authoring governance. |
| docs/track-b/capstone_v21-r1-to-v21-r2-amendments.md | Exact supplied ratified amendment bytes. |
| docs/track-b/cp-16-v2-brief.md | Exact supplied execution brief bytes. |
| docs/track-b/evidence/cp-16/admission.log | Preserve actual partial-run, test or resource-defect evidence: admission.log. |
| docs/track-b/evidence/cp-16/blocked-execution-test.log | Preserve actual partial-run, test or resource-defect evidence: blocked-execution-test.log. |
| docs/track-b/evidence/cp-16/checkpoint-return.md | Canonical non-PASS checkpoint return; its own commit identity resolves in the terminal receipt. |
| docs/track-b/evidence/cp-16/critic-audit.log | Independent review, terminal resource accounting, or handover evidence: critic-audit.log. |
| docs/track-b/evidence/cp-16/critic-audit.py | Independent review, terminal resource accounting, or handover evidence: critic-audit.py. |
| docs/track-b/evidence/cp-16/critic-final-audit-normalized.log | Independent review, terminal resource accounting, or handover evidence: critic-final-audit-normalized.log. |
| docs/track-b/evidence/cp-16/critic-final-audit.log | Independent review, terminal resource accounting, or handover evidence: critic-final-audit.log. |
| docs/track-b/evidence/cp-16/critic-final_audit.py | Independent review, terminal resource accounting, or handover evidence: critic-final_audit.py. |
| docs/track-b/evidence/cp-16/critic-final_audit_normalized.py | Independent review, terminal resource accounting, or handover evidence: critic-final_audit_normalized.py. |
| docs/track-b/evidence/cp-16/critic-guards.log | Independent review, terminal resource accounting, or handover evidence: critic-guards.log. |
| docs/track-b/evidence/cp-16/critic-tests.log | Independent review, terminal resource accounting, or handover evidence: critic-tests.log. |
| docs/track-b/evidence/cp-16/inherited-guards.log | Preserve actual partial-run, test or resource-defect evidence: inherited-guards.log. |
| docs/track-b/evidence/cp-16/integration-assignment.md | Independent review, terminal resource accounting, or handover evidence: integration-assignment.md. |
| docs/track-b/evidence/cp-16/integration.md | Independent review, terminal resource accounting, or handover evidence: integration.md. |
| docs/track-b/evidence/cp-16/interrupted-admission-lineage.json | Preserve actual partial-run, test or resource-defect evidence: interrupted-admission-lineage.json. |
| docs/track-b/evidence/cp-16/main-state.txt | Independent review, terminal resource accounting, or handover evidence: main-state.txt. |
| docs/track-b/evidence/cp-16/monitor-regression.log | Preserve actual partial-run, test or resource-defect evidence: monitor-regression.log. |
| docs/track-b/evidence/cp-16/pre-run-tests.log | Preserve actual partial-run, test or resource-defect evidence: pre-run-tests.log. |
| docs/track-b/evidence/cp-16/preflight.log | Preserve actual partial-run, test or resource-defect evidence: preflight.log. |
| docs/track-b/evidence/cp-16/residual-builder-audit.md | Preserve actual partial-run, test or resource-defect evidence: residual-builder-audit.md. |
| docs/track-b/evidence/cp-16/resource-accounting-audit.md | Preserve actual partial-run, test or resource-defect evidence: resource-accounting-audit.md. |
| docs/track-b/evidence/cp-16/resource-final.json | Independent review, terminal resource accounting, or handover evidence: resource-final.json. |
| docs/track-b/evidence/cp-16/review-identity.json | Independent review, terminal resource accounting, or handover evidence: review-identity.json. |
| docs/track-b/evidence/cp-16/supervisor-failure-record.json | Preserve actual partial-run, test or resource-defect evidence: supervisor-failure-record.json. |
| reports/v2-causal/artifact-manifest.json | Hashes of the partial candidate source, tests and artifacts. |
| reports/v2-causal/failures.csv | Accounting/supervision interruption records; no invented successful forecasts. |
| reports/v2-causal/input-manifest.json | All permitted origin/target keys, input identities and training-only feasibility. |
| reports/v2-causal/lineage.json | Preserved partial training-only component lineage and explicit blocked stage. |
| reports/v2-causal/protocol.json | Frozen scientific recipe, ceilings, numerical fixtures and disclosed repair identity. |
| reports/v2-causal/report.md | Honest incomplete research result and exact authority needed. |
| reports/v2-causal/reproduce.md | Bounded executable checks and restrictions on unfinished scientific jobs. |
| reports/v2-causal/resources.json | Counter correction, monitored jobs and unknown memory gap. |
| scripts/cp16_v2.py | Local phase driver and repaired fail-closed resource monitor. |
| src/cp16/__init__.py | CP-16 namespace. |
| src/cp16/budget.py | Atomic persistent resource ceilings and per-Lasso-call accounting. |
| src/cp16/execution.py | Ordered admission/replay/scoring and blocked-authority refusal. |
| src/cp16/inputs.py | Partition filtering, immutable inherited inputs and cache identity checks. |
| src/cp16/preflight.py | Training-only E 1 support audit and complete permitted key manifest. |
| src/cp16/residuals.py | Fixed shared causal H/P residual state and persistence. |
| src/cp16/scoring.py | Fixed seven-policy scores, diagnostics, criteria and paired calendar bootstrap. |
| tests/cp16/test_budget_inputs.py | Synthetic regression/control coverage for budget inputs. |
| tests/cp16/test_monitor.py | Synthetic regression/control coverage for monitor. |
| tests/cp16/test_residuals.py | Synthetic regression/control coverage for residuals. |
| tests/cp16/test_scoring.py | Synthetic regression/control coverage for scoring. |

## Elapsed

Approximately **0.5 hours** to the nearest half hour against 32-hour approximate timebox; conservative active-effort bound 1 hour against 40-hour hard ceiling. Resource infeasibility, not elapsed time, caused this return.

## Open risk or exact owner action

A new resource decision is required; the remaining 770 policy-days cannot cover 1200 unfinished production policy-days, even before further controls/review. The existing 3730 debit is retained. A conservative proposal is §14.5 residual replay only: replace “At most **3** full-equivalent H/P passes, **4, 500** policy-days total (750 × 2 × 3)” with “At most **5** full-equivalent H/P passes, **7, 500** policy-days total (750 × 2 × 5)”. All scientific rules and other caps remain unchanged. This would cover a fresh 1276-day production replay, 1276-day independent replay and 1002-day control suite with 216 remaining; it is not an authorization or a promised completion estimate.

Please manually and temporarily suspend the Governance Lockdown for this specific edit to capstone_v21.md §14.5 and the directly necessary amendment-record/issued-brief consistency changes, and have the Orchestrator issue the corrected ratified CP-16 brief. AGENTS.md requires: “When a change to any of these is genuinely necessary — HALT.” The Lead has made no such governance edit. Alternatively, the Owner can disposition this attempt DISCARD. Neither decision is inferred. All Track B work stops at this return.

## Landing report

- Proposed disposition: **DISCARD this incomplete attempt**, preserving its evidence chain; Owner may instead authorize a scoped resumption. No disposition has been executed.
- Evidence tip to preserve: SELF_COMMIT, resolved in the terminal receipt. No tag or branch deletion was made.
- Live branch citations: reports/v2-causal/report.md, this checkpoint-return.md and the terminal packet; the immutable execution brief/anchor also name its historical branch by contract. Operational citations must be repointed on Owner-directed reclamation; locked historical text is not edited without authority.
- Proposed commit message: `Preserve CP-16 interrupted admission, resource corrections and independent FAIL evidence`.
- No merge/squash/mainline action is proposed as an agent operation.

## Post-return reads

None. progress.md, orchestrator-role.md, syllabus and Track A/C material were not read.

## Interview capture trigger

Trigger: why synthetic warm-up and failed test attempts must count against the same replay budget, why an evidence monitor must fail closed, and why a resource gap must stop scoring rather than shrink the evaluation. No Q&A edit.
