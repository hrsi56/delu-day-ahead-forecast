# Integration Critic — CP-16

## Candidate
- Full SHA: bf3ca602e32e99e45c7835e3f95148f62b608099
- Clean detached worktree: /Users/djourno/Downloads/PJM/.local/worktrees/cp-16/critic-r3
- Confirm git status --porcelain is empty and HEAD unchanged before and after review.
- Cooperative read-only isolation. Do not modify tracked files or Git state. Lead removes worktree after verdict import.

## Controlling plan
- File capstone_v21.md, version v21-r3, bar §14.8; verify supplied SHA256 67d2176865fea4d6ada0b13bafb128016970d78337d5a936890ddbff7c3ad6ed.
- Read engineering-role.md and only relevant capstone §§2–9 and complete §14. Do not read progress.md, orchestrator-role.md, syllabus or Track A/C.
- Verbatim bar excerpt (confirm exact text at candidate):

### 14.8 Complete CP-16 acceptance checklist

Every item is mandatory. Engineering PASS does not require a positive research finding; it
does require a complete valid evaluation and fresh binding Integration PASS.

1. Verify actual repository/input state and preserve other sessions' work and all v1/CP-15
   evidence. Commit the exact ratified amendment, execution brief and complete pre-run protocol
   on the authorized CP-16 candidate branch before new model comparison; document input,
   code, dependency, budget and protocol identities and all permitted origin/target keys.
2. Implement only the fixed A1/B2 central blend, the frozen causal hour-aware residual policy
   and the otherwise identical pooled control. Freeze the two constructions on permitted
   training data before outer scoring; prove that their only difference is hour-aware pooling.
3. Prove origin availability, training-only and origin-specific transforms, D−2 release,
   consume-once, genuine warm-up, complete-day/DST identity, sparse-hour fallback, cache
   identity and restart replay, with negative assertions accompanied by positive controls.
   Preserve relevant inherited namespace guards and all prohibited-partition boundaries.
4. Produce forecasts for every original eligible target in all five folds; report exact
   shared key counts, failed issuance and original exclusions, all finite ordered quantiles
   and emitted p50 separately from central. No missing eligible forecasts, altered targets
   or silently reduced denominators can support completed-evaluation PASS.
5. Independently verify emitted-vector scores, original seven-quantile WIS and equal-fold B0
   normalization, all required per-fold/hour/block/peak diagnostics and their denominators.
   Re-score saved B0/B1/B2/A1 references and B3's diagnostic comparisons without new fits or
   overwriting historical evidence. Keep native v1 pinball separate.
6. Apply the frozen research ranking/paired uncertainty/no-preference rule mechanically,
   report both point and interval effects including negative or mixed findings, and report
   all six unchanged original §8 diagnostics. Distinguish Engineering status, historical
   CP-15 product status, new research findings and product/delivery eligibility. No demonstrated
   joint preference is not equivalence or absence of benefit; disclose mixed effects. No post-hoc
   economic threshold or research-to-product promotion is permitted.
7. Enforce and report every adopted numeric resource/candidate cap, counting warm-up, inner
   selection, failed attempts, controls, corrections and independent reproduction. At the
   first exhausted cap retain partial evidence and return the appropriate non-PASS status;
   no unauthorized scope reduction or resource extension can cure an incomplete checklist.
8. Supply durable protocol, lineage, predictions, metrics, diagnostics, uncertainty, failure/
   resource logs, notices, reproducibility manifest and executable reproduction commands.
   Run relevant controls and regression checks; disclose defects/repairs and invalidated
   outputs. All development results retain their post-selection label and inherited limits.
9. Obtain one fresh independent Integration-Critic PASS on a clean detached checkout of
   the exact final candidate, covering this entire checklist, independently recomputed
   saved-prediction metrics and representative causal/component/state reproduction. Preserve
   commands, exit codes and limits; no self-certification or unsupported PASS.
10. Return the complete canonical checkpoint packet, both terminal SHAs and a verdict-only
    candidate-to-evidence delta, reachable evidence, branch/worktree/tag accounting, elapsed
    effort and all resource totals. End at CP-16's local result, including an honest negative
    result; no next checkpoint, final live-policy selection, publication or mainline operation.

## What to verify
The entire checklist item by item: inputs, contracts, hard invariants, scores, controls, reproduction, resource accounting, documentation and terminal readiness. Independently recompute; do not redesign. Artifacts: reports/v2-causal/*, src/cp16/*, tests/cp16/*, scripts/cp16_v2.py; source inputs/hashes and all keys in input-manifest.json, implementation/output hashes in artifact-manifest.json. Preserved prior candidate and FAIL/evidence are under docs/track-b/evidence/cp-16/attempt-1 and in the cited Git history. Input governance identity: issued docs/track-b/cp-16-v2-brief.md and docs/track-b/capstone_v21-r2-to-v21-r3-amendments.md.

## Reproduction commands
Run only serialized compute commands through the shared monitor. In the detached worktree define:
CP16_PY=/Users/djourno/Downloads/PJM/.venv/bin/python
CP16_BUDGET=/Users/djourno/Downloads/PJM/.local/artifacts/cp-16/budget.json
CP16_PROJECT=/Users/djourno/Downloads/PJM
CP16_LOGS=/Users/djourno/Downloads/PJM/.local/artifacts/cp-16

1. "$CP16_PY" scripts/cp16_v2.py --monitor --ledger "$CP16_BUDGET" --project-root "$CP16_PROJECT" --log "$CP16_LOGS/r3-critic-tests.log" -- env CP16_REQUIRE_SAVED_EVIDENCE=1 "$CP16_PY" -m pytest tests/cp16 -q -s -p no:cacheprovider --basetemp="$CP16_PROJECT/.local/tmp/cp-16/r3-critic-tests"
2. "$CP16_PY" scripts/cp16_v2.py --monitor --ledger "$CP16_BUDGET" --project-root "$CP16_PROJECT" --log "$CP16_LOGS/r3-critic-components.log" -- "$CP16_PY" tests/cp16/reproduce_components.py --output "$CP16_LOGS/r3-critic-components.json"
3. "$CP16_PY" scripts/cp16_v2.py --monitor --ledger "$CP16_BUDGET" --project-root "$CP16_PROJECT" --log "$CP16_LOGS/r3-critic-guards.log" -- "$CP16_PY" -m pytest tests/cp15/test_pipeline.py tests/test_02_rolling_closed_left.py tests/test_05_schema_firewall.py tests/test_08_partition_integrity.py tests/test_12_partition_exclusion.py tests/test_24_live_namespace_is_walled_off.py -k 'not test_fit_delivery_mask_positive_d1_and_rolling_refit' -q -p no:cacheprovider --basetemp="$CP16_PROJECT/.local/tmp/cp-16/r3-critic-guards"

Expected: complete passing tests, exactly75,229 rows/10,747 keys per policy, fold counts2160/2159/2112/2160/2156. Independent metric/diagnostic/bootstrap tolerance2e-12 absolute/relative; H/P state vector tolerance1e-10 absolute/1e-12 relative; component tolerance1e-8 absolute/1e-10 relative with exact model/imputer/scaler/training fingerprints. Delivery-day mutation exactly0.0 and D−1 positive mutation strictly nonzero. All claims must follow complete §14; no favorable result is required.

Shared ledger pre-review counters:5022 policy-days,113 total component/93 main attempts,13524 primitive (10820 inner/2704 final), one reference and one analysis pass. Caps9000/2000/1500/240000/192000/48000, reference3/analysis3; historical3730 retained unchanged. Tests automatically reserve one reference+analysis pass and1276+152 real replay policy-days. Component reproduction reserves8 policy-days/8 attempts. Synthetic fixtures no real research data have no new policy-day debit; compute still monitored. Any additional real replay must reserve before execution in this SAME ledger; no repeated analysis beyond caps. Preserve failed-command charges; do not retry an entire expensive suite automatically. Resource caps/machine/effort/RSS/disk in ledger/protocol govern, including review. Do not run inherited saved-evidence suites or model-fit tests beyond named scope.

You may write read-only audit scripts only in .local/tmp/cp-16/critic-r3, run through the monitor, and return them as evidence. Any new script reading research outcomes must filter/project permitted data before materialization, never spent holdout/reserved tail.

## Verdict
Write one markdown verdict at /Users/djourno/Downloads/PJM/.local/artifacts/cp-16/r3-integration-verdict.md using gauntlet-templates.md §2: PASS/FAIL/BLOCKED, full candidate SHA, plan/version/bar and entire verbatim excerpt, clean checks, exact commands/exit codes/observations, inspected evidence, all ten checklist item verdicts. On FAIL name the largest meaningful gap and exact next acceptance test. No self-certification by executor. Item10 terminal evidence-only commit necessarily follows review: audit packet readiness and prescribed two-SHA procedure, identifying any unverified post-review steps. Do not change candidate or write verdict into the tracked worktree. Send Lead path and status. Stop when review is complete.
