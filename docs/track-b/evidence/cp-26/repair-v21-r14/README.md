# CP-26 v21-r14 repair package — validation evidence

This package repairs the existing CP-26. **CP-26 remains INCOMPLETE.** r14 is an Owner-review
candidate, not a ratified plan. The independent repair-readiness review is recorded separately;
it is not CP-26 Integration and cannot close that checkpoint. No new search, pilot, experimental
calendar replay, CP-26 score, CP-28 arm, publication, main write or history rewrite occurred.

## Identity and custody

| Artifact | Identity |
|---|---|
| Initial Lead HEAD | `5cc3cc083c4340fd8d792eeaf6551a007987a877` |
| Immutable landed-code base/main | `647d6eb81b2cf6e0cfaf4152f659d689ff973578` |
| r13 anchor | `173799d818387b9d82db16b9ccd7195afaebbea8e11259809e4a8b704bd525a8` |
| r14 anchor-only commit | `332baeb861cec5a58516c58a29a1a3afe1eec909` |
| r14 candidate anchor SHA-256 | `3be866bd10af02cc2b0b956ed91be660dca29a62c0b23b00997bf0b415d100c5` |
| Amendment sheet SHA-256 | `554a3aa4bf81f3fc1cc2319e624295570f919ff1fd4a6d9e2c9f56f8dcf6b79a` |
| Active repair brief SHA-256 | `5b6a0cdfad870da6b59a03ff29576ff6ec98891e941d56986516e6f3f743ff84` |
| CP-28 r14 registration SHA-256 | `2b9286b0e948f59f97de33315a8b4fb3ef121003fc4ba82355b1ccf6585497a8` |
| Active-document manifest SHA-256 | `aa29af82181769afefdb0a4446057dd08f7ebafaac27a398aa2679397a3cadfe` |
| Source/protocol freeze commit before parity | `563be855d918cb7ec3a2b53497414a863dc43431` |

The first anchor commit was `c0ed61728bf532b9ce2efc4339bd0749645c0b1f`; the next anchor-only
commit made protocol freezing precede searches/pilot. Dependent pins then name332baeb in full.
No self-referential hash/commit exists. `active-documents.json` records versions, supersession
and reasons. Original `issued-brief.md`, its primary canonical copy and `cp28-frozen-protocol.md`
are unchanged. r13 code/output bytes and inherited uncommitted work were preserved before use;
`initial-inventory.json`, `preserved-r13/`, `inherited-uncommitted.patch` and the reachable initial
commit establish custody. The active harness log's original hash was
`6835e0bcbc6a211cfb8e4bb04cf0b8bcd49c6207e06de5eea7e99fa180cda48d` and is preserved too.

## Repair checklist and observed evidence

| Required contract | Evidence |
|---|---|
| All14 search dates×three routes; exact landed support/week extrema | `reports/rebaseline/repair-v21-r14/search-support.json`/`.md`, support-only monitored runs; B=[1,7,11,…,11] on nominal,noload,gfs6. First batch2019-12-18..2020-01-14: N321,pool48,m10,min train251,min hold46. Support algorithm, not these expected numbers, is authoritative |
| Fixed sampler128, permitted space, halving/ranking/ties, effective no-load identity and eight members | `test_cp26_search.py`: exact128 draws, disjoint seed domains,43 survivors when B>4, duplicates consume trials, failed batch/search/refused subset, verified source/plan/cache lineage |
| Warm-up/recovery after D−2; no central failure intake; immutable fallback | `test_cp26_state.py`, `test_cp26_replay.py`: own native errors enter once under H-history shortage; member/solver/identity/scale/numerical-H failures refuse; stored fallback vector remains unchanged |
| B0 raw recipe/no self fallback; v1-R nine heads,CQR,embargoes | Synthetic raw-error readiness and missing-output test; stubbed real adapter verifies9→CQR→isotonic→7; bounded728-day head window and both embargoes |
| Partial issuance remains scored, no full-error intake; fullDST23/25 days enter | State tests preserve frozen scoring keys and actual canonical keys. A full native issuance and a partial scoring subset are distinct predicates; no missing issuance key is invented |
| Historical scale; consume once; no D/D−1 feedback | State/replay tests mutate truth only behind release callback; D/D−1 are never requested, D−2 is; saved original scale and restored provenance are checked |
| Continuous vs resumed equivalence; no reset at scoring/search/failure | Multi-route serialized replay across search/measurement boundaries, including D2 failure/recovery; immutable prior outputs and original pending/consumed state compared |
| Learning ledger independent of28-day H; route separation | Complete three-native-member rows retained despite H-only fallback;364/728 learning support is separate; late historical issuance and late-release look-ahead refused; route buffers isolated |
| Death,PID reuse,orphan,unreconciled reserve | `test_cp26_monitor.py`: independent supervisor completion; real outer/SIGKILL supervisor death, live orphan, reused PID, registered detached worker, omitted worker receipt, failed-job accounting, no idle charge, idempotent reserve/reconciliation |
| Current old-settings parity |96 exact checks PASS, sampled oldfold2–5 ×nominal/restored no-load; every member fitted fresh with old identity/time/boundary. CP24 ensembles are fixtures only and never serve CP26 |
| Original history/decision rules remain intact | `test_cp26_repair_contract.py`: original brief/protocol hash equality; §§1–23 unchanged; CP28 sections3–5/8–9 byte-identical; new documents pinned and r14 explicitly pending ratification |

The final source test run after the first repair review observed **88 passed in37.45s**
(monitored job `repair-r14-pgid-fix-tests`, wall39.130454959s, two allocated workers).
The first repair review found unsafe ownership inference from a reused numeric
process group. Its verdict is preserved in `repair-review-attempt-1.md`. The corrected supervisor
binds PID/create-time identities, never signals a numeric group, refuses uncertain ending
evidence and enforces declared/global worker allocations before registered worker computation.
Seven additional regression tests cover group reuse, the discovery race, escaped workers and
worker registration limits. Every prior iteration/test cost remains in the ledger. This is
synthetic and support validation, not successful execution of the experiment.

The terminal `repair-review-attempt-2.md` is the fresh independent source/contract review;
the first attempt is historical defect evidence. Its disclosed exposure to Builder summaries
does not serve as terminal certification. The fresh review reports its ignored pytest-cache
byproduct and its first metadata script's out-of-snapshot attachment hash check openly.

## Exact compute commands

Run from `/Users/djourno/Downloads/PJM/.local/worktrees/cp-26/lead`, with the locked interpreter
`/Users/djourno/Downloads/PJM/.venv/bin/python -B`. The driver sets all five BLAS/thread limits
to1 before numerical imports. Receipts in `runs/` preserve actual argv, exit codes and durations.

```sh
/Users/djourno/Downloads/PJM/.venv/bin/python -B scripts/cp26_rebaseline.py monitor --name repair-r14-stable-tests --workers 2 -- /Users/djourno/Downloads/PJM/.venv/bin/python -B -m pytest tests/test_cp26_harness.py tests/test_cp26_parity.py tests/test_cp26_search.py tests/test_cp26_state.py tests/test_cp26_replay.py tests/test_cp26_monitor.py tests/test_cp26_repair_contract.py -q --basetemp=/Users/djourno/Downloads/PJM/.local/tmp/cp-26/repair-stable-tests
/Users/djourno/Downloads/PJM/.venv/bin/python -B scripts/cp26_rebaseline.py monitor --name repair-r14-pgid-fix-tests --workers 2 -- /Users/djourno/Downloads/PJM/.venv/bin/python -B -m pytest tests/test_cp26_harness.py tests/test_cp26_parity.py tests/test_cp26_search.py tests/test_cp26_state.py tests/test_cp26_replay.py tests/test_cp26_monitor.py tests/test_cp26_repair_contract.py -q --basetemp=/Users/djourno/Downloads/PJM/.local/tmp/cp-26/repair-pgid-fix-tests
/Users/djourno/Downloads/PJM/.venv/bin/python -B scripts/cp26_rebaseline.py monitor --name repair-r14-support-final --workers 1 -- /Users/djourno/Downloads/PJM/.venv/bin/python -B scripts/cp26_search_support.py --lead /Users/djourno/Downloads/PJM/.local/worktrees/cp-26/lead --output /Users/djourno/Downloads/PJM/.local/worktrees/cp-26/lead/reports/rebaseline/repair-v21-r14/search-support.json
/Users/djourno/Downloads/PJM/.venv/bin/python -B scripts/cp26_rebaseline.py monitor --name repair-r14-verify-inputs --workers 1 -- /Users/djourno/Downloads/PJM/.venv/bin/python -B scripts/cp26_rebaseline.py job verify-inputs
/Users/djourno/Downloads/PJM/.venv/bin/python -B scripts/cp26_rebaseline.py monitor --name repair-r14-parity --workers 1 -- /Users/djourno/Downloads/PJM/.venv/bin/python -B scripts/cp26_rebaseline.py job parity
```

Reproduction names and --basetemp directories should be fresh to keep receipts and recovery
material separate. Full experimental commands intentionally are not exposed by this repair driver.
The copied raw inherited patch has two whitespace context lines; exact byte custody is retained.
Source/plan diff-whitespace checks pass; those patch-data lines are not source edits.

## Resource reconciliation and limits

Initial547.5647564170067s already included4.13+1.995=6.125s. Historical measured jobs reconcile
to541.4397564170067s;6.125 is reclassified reported, never added twice. The independent audit's
four reported successful tests add90.127s exactly once. Reported total is96.252s.
Terminal resources separately add1s of tool-reported administrative batch elapsed;
the historic audit import remains90.127s. `terminal-resources.json` is the final total.
The failed audit's15.01s is only a lower bound and is not a separate charge. Authorized reserve
2826s remains **reserved**, never measured or reduced. `audit-time-bound.json` associates the
admitted failure with the sole audit turn1791907417..1791908415, between parity completion
1791905827.8090382 and attachment receipt1791908653.442842; the2826s ceiling bounds that window.
`resource-reconciliation.json` preserves the initial migration; terminal resources include every
subsequent measured worker job, report and reserve, with no reset. New repair scope is36000s,
inside485h; future pilot stop line388h. No worker-ending evidence means new compute refuses.

Supervisor process discovery is cooperative for detached workers: they must call
`cp26.supervisor.register_worker()` before detached work and complete the registration handshake
before their parent exits. Ancestry lost between OS samples cannot be recovered retrospectively.
Current model search/refits are serial; independent top-level monitored jobs may run concurrently
within4 workers. Any future detached parallel bootstrap must implement that handshake.

## Remaining experiment work and continuation brief

Owner review/ratification of the exact r14 bytes and a new continuation brief are required.
Real searches, the14-origin timing pilot, full chronological experimental replay, CP26 scoring,
replicates/bootstrap/inference/diagnostics, report/draft publication packet and full CP26
Integration remain unexecuted. The core search/refit/cache/issuance/replay/state primitives are
implemented; the end-to-end experiment CLI, orchestration/checkpoint-resume scheduling and
score/inference output assembly still require completion/validation under that continuation.
The frozen CP28 registration specifies arms but no arm is implemented here.

The continuation must bind the reviewed/ratified anchor hash/commit, active document manifest,
current source and parity identities, CP25 masks/cutoff, unchanged landed base, persistent state
and resource journal. It must conservatively price **all42 searches**; the support-derived
full-success bound is31575trial/batch fits before daily fits, failures and validation. Include
all historical measured/reported/reserved expense and remaining work against388h before a
full run. Structural support and bitwise old-setting parity do not guarantee four successful
configurations, eight daily fits, CQR success, cost or scientific generalization. Disclose the
first search's single winter block, calendar span/age of recovery buffers and existing vintage risk.

## Role and interview record

No `progress.md`, `orchestrator-role.md`, syllabus or TrackA/C material was read; no programme
state or `integration.md` changed. Post-return reads: none. No credential value or new market
exposure was observed. Interview triggers for the Orchestrator: support for every week split
versus merely one successful split; native-central recovery without retrospective fallback
replacement; separate H/learning/scoring eligibility; measured versus reported versus bounded
reserve accounting and refusal to present restart idle gaps as worker computation.
