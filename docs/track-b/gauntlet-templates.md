# Track B Gauntlet — Canonical Templates

These are boundary-contract templates, not a second capstone plan. The ratified plan named in `progress.md` remains normative. Replace every bracketed field; never infer an anchor from the highest version on disk.

## 1. Orchestrator checkpoint brief

```markdown
# Track B Checkpoint Brief — [M#/CP-# or FM#/FCP-#]

Target repository: [absolute path or unambiguous repo name]
Authorized checkpoint: [exactly one checkpoint]
Ratified plan anchor: [exact filename and version from progress.md]
Complete checkpoint checklist: [exact citation to the full named CP/FCP checklist]
Supporting sections: [exact citations needed for this checkpoint]
Total checkpoint active-elapsed ceiling: [numeric hours covering orientation through terminal return]

## Orchestrator-reported expected state
- branch / commit / working-tree expectation
- completed predecessor and artifacts expected to exist
- data snapshot/cutoff expected

Engineering-Lead must verify this state against the repository before relying on it. A material mismatch is returned, not silently reconciled.

## Observable outcome
[The state that must exist when this checkpoint closes.]

## Complete authoritative checkpoint bar
- [every item in the named CP/FCP checklist, with citation]
- [...]

## Task-specific supporting extract
- [supporting-plan citation]: [faithful outcome-level statement]
- [...]

The complete named CP/FCP checklist remains controlling even if either extract accidentally omits an item. A supporting extract may not weaken, strengthen, or replace it.

## Applicable constraints
- [ratified architecture/data/method constraints]
- $0 expected run rate; $65/month policy ceiling
- M3 / 16 GB / CPU-only, unless the named plan says otherwise

## Owner-only actions already authorized
- none / [credential, signup, browser-bound action, payment, publication]

## Stop and return
Run the bounded Gauntlet autonomously under `engineering-role.md`. Return exactly one consolidated Return Packet with PASS, BLOCKED, PLATEAU, or BUDGET_EXHAUSTED. Stop all Track B work before any later checkpoint. Do not plan or begin it.
```

Measure one active elapsed wall clock in UTC. Record raw seconds from `started_at_utc` to terminal return minus only logged, eligible all-context pauses. Parallel contexts overlap and never sum. New owner/credential/authority requirements return `BLOCKED`; they are not open-ended pauses.

Invalid briefs are returned before work begins if they omit the exact anchor or full-checklist citation, authorize more than one repo/checkpoint, or lack a numeric active-elapsed wall-clock ceiling. A brief cannot reduce the checkpoint bar: that requires an owner-ratified capstone/checkpoint amendment, a new exact anchor, and then a replacement brief.

## 2. Active `workbench.md`

Create this file only after a valid checkpoint brief arrives.

```markdown
# Active Track B Workbench — [checkpoint]

Plan anchor:
Candidate branch/full commit SHA:
Checkpoint active-elapsed ceiling:
started_at_utc:
last_updated_at_utc:
Consumed active elapsed: [raw seconds / decimal hours]

## Eligible pause ledger
| paused_at_utc | resumed_at_utc | duration seconds | reason/evidence | all contexts stopped? |
|---|---|---:|---|---|

## Authorized goal and bar
- criterion → evidence required

## Lead-chosen pieces
| Piece | Owned paths/artifact | Builder state | Fresh critic state | Largest open gap |
|---|---|---|---|---|

## Mandatory independent surfaces in scope
| Surface | Applicable? | Critic evidence/verdict |
|---|---|---|
| Temporal normalization | | |
| Champion/benchmark schema firewall | | |
| A75 climatology fit lineage | | |
| Four-catalog metric recomputation from frozen predictions | | |
| M3 hand-checkable CQR threshold recomputation | | |

## Mandatory M1 acceptance-oracle pack (when CP-1 is active)
| Oracle | Independent fixture SHA-256 | Independent expected result | Critic commands/evidence/verdict |
|---|---|---|---|
| M1-O1 — misaligned PT15M chunk stitch | | exactly one four-quarter mean; no three-quarter mean | |
| M1-O2 — missing quarter | | no hourly value; explicit incomplete/recovery | |
| M1-O3 — Berlin fall-back hour | | both 02:00 offsets survive as distinct UTC; 25 rows; true duplicate rejected | |
| M1-O4 — A75 fit-lineage poison | | calibration/eval poison is inert; proper-training poison changes fit | |
| M1-O5 — champion/benchmark schema poison | | valid champion passes; A69/A69-derived/actual injection fails closed; benchmark adds only approved A69 fields and rejects actuals | |

## Integration
- full candidate commit SHA:
- reproduction commands:
- isolated Critic manifest path/hash:
- fresh Integration-Critic verdict:

## Exact blocker, if terminal
- none / exact owner or authority request
```

The workbench is temporary engineering state, ignored by Git, and never included in a candidate commit or Critic checkout/context. The Orchestrator never reads it and `progress.md` never imports it. At terminal return, archive a renamed final snapshot beside checkpoint evidence only if it contains unique evidence; otherwise delete it. Never carry an active root workbench into the next checkpoint.

At M1, the oracle table is mandatory rather than illustrative. A fresh Critic—not the Builder—materializes and hashes every fixture outside the candidate checkout, computes the expected outcome independently, and records exact commands and results. Repository property tests do not substitute for these five verdicts.

## 3. Builder assignment

```markdown
# Builder assignment — [piece]

Authorized checkpoint:
Owned paths/artifact:
Observable goal:
Concrete acceptance bar:
Relevant ratified rules/citations:
Required tests/reproduction/evidence:
Forbidden scope:
Target wall-clock window within the checkpoint ceiling (Lead-set, non-authoritative):

Implement only this bounded piece. Commit the candidate and return its full SHA, artifact hashes, exact reproduction commands, evidence, known gaps, and active-elapsed timing. Do not self-certify the checkpoint or ask a Critic to review an uncommitted diff.
```

## 4. Independent Critic assignment

Use a fresh read-only context and the mandatory isolated protocol in `engineering-role.md`. Create a clean detached checkout at the full candidate SHA outside the Builder tree. `workbench.md`, Builder history, summaries, and uncommitted files must be absent. Route caches, generated output, and verdict evidence outside the Critic checkout.

```markdown
# Independent Critic — [piece or mandatory surface]

Authorized checkpoint:
Full candidate commit SHA:
Candidate artifact path/SHA-256:
Exact ratified plan filename/version:
Observable goal and exact bar citation/version:
Decision-bearing input/data SHA-256 (or explicit N/A):
Exact reproduction commands:
Expected output/tolerance:
Critic context/run ID: [if exposed by the harness]

## Before-review integrity
- `git rev-parse --verify HEAD`:
- `git rev-parse --verify 'HEAD^{tree}'`:
- `git diff --quiet`: PASS
- `git diff --cached --quiet`: PASS
- `git status --porcelain=v1 --untracked-files=all --ignored=matching`: EMPTY
- `test ! -e workbench.md`: PASS

Inspect and rerun independently. Return:
- Verdict: PASS | FAIL
- Bound candidate SHA/artifact hash, bar citation/version, and input hashes
- Exact commands actually executed
- Before/after integrity evidence from `scripts/gauntlet_critic_snapshot.sh` or equivalent
- Evidence actually inspected/recomputed
- The single largest meaningful gap
- The exact next acceptance test
- Any scope or methodology conflict

Do not edit the checkout or inspect the Builder workspace. Repeat every integrity check after review without cleaning/resetting first. Any changed SHA/tree, nonempty status, workbench presence, or missing provenance field invalidates the verdict. Do not redesign the project and do not accept claims that are not reproducible from the artifact.
```

For comparison artifacts, use blind A/B review where practical. On `FAIL`, Engineering-Lead routes the evidence directly back to a Builder and later launches a fresh critic; Yarden does not relay messages.

## 5. Fresh Integration Critic

```markdown
# Fresh Integration Critic — [checkpoint]

Authorized checkpoint:
Full final candidate commit SHA:
Final candidate artifact path/SHA-256:
Exact ratified plan filename/version:
Complete checkpoint bar citation/version:
Decision-bearing input/data SHA-256 (or explicit N/A):
Clean reproduction commands:
Expected output/tolerances:
Data snapshot/cutoff/hash:
Component and mandatory-surface verdict artifacts:
Component Critic provenance manifest paths/hashes:
Fresh detached checkout before-review integrity evidence:

From this fresh read-only context, verify:
1. every item in the complete named CP/FCP checklist against direct evidence;
2. all current independent verdicts and mandatory surfaces;
3. every component verdict still binds to unchanged reviewed paths and input hashes at the final candidate SHA; rerun stale verdicts;
4. cross-component contracts and hard invariants;
5. metrics recomputed from frozen predictions where applicable;
6. clean-environment reproducibility and documentation consistency;
7. absence of unauthorized later-checkpoint work.

Repeat the full integrity check after review without cleanup. Return PASS or FAIL with the same mandatory SHA/bar/input/command/integrity provenance, evidence inspected, the single largest gap, and the exact next acceptance test. Do not redesign.
```

## 6. Consolidated Return Packet

```markdown
# Track B Checkpoint Return — [M#/CP-#]

Status: PASS | BLOCKED | PLATEAU | BUDGET_EXHAUSTED
Target repository:
Ratified plan anchor:
Exact commit/branch:
Working-tree state:
Data snapshot/cutoff/hash:
Checkpoint active-elapsed ceiling:
started_at_utc / terminal_at_utc:
Eligible pause ledger (UTC, reason/evidence, all contexts stopped):
Consumed active elapsed: [raw seconds / decimal hours]
Integration verdict and evidence: PASS | FAIL | NOT_RUN — [evidence or exact reason]
Integration Critic provenance manifest (path/SHA-256):

## Complete named CP/FCP checklist
| Criterion citation | PASS/OPEN | Direct evidence/reproduction |
|---|---|---|

## Independent criticism
| Piece/surface | Critic/run ID | Candidate SHA / artifact hash | Bar citation/version | Input/data hashes | Exact commands | Before/after integrity evidence | Verdict/evidence | Largest gap and disposition |
|---|---|---|---|---|---|---|---|---|

## Engineering decisions
- decision and rationale
- rejected alternatives and why
- largest failure uncovered by the Gauntlet and how it was repaired

## Reproduction
- exact commands
- artifacts
- metrics/screenshots where applicable

## Open risks or exact owner action
- none / exact request

## Defense questions
1. [3–5 questions grounded in actual architecture, tradeoffs, and evidence]

Track B has stopped. No later-checkpoint work has begun.
```

## 7. Orchestrator receipt and gate

The Orchestrator checks that the packet names the authorized repo/checkpoint/anchor, maps **every item in the full named CP/FCP checklist** to direct evidence, includes all applicable independent surfaces and M1 oracles, and does not hide an open item behind `PASS`. Every required component, oracle, and Integration verdict must include the full candidate SHA/artifact hash, exact bar citation/version, input hashes, commands/tolerances, and clean-detached before/after integrity evidence. A missing field, dirty checkout, changed SHA/tree, stale component verdict, or review of uncommitted work invalidates that verdict and therefore invalidates `PASS`. A supported `PASS` requires a current fresh Integration-Critic `PASS`. For a non-`PASS` return, `NOT_RUN` is acceptable only with the exact terminal reason—`BLOCKED`, `PLATEAU`, or `BUDGET_EXHAUSTED`—that prevented integration; it never implies a pass.

- Supported `PASS`: close only that checkpoint in `progress.md`, summarize its evidence, then ask Yarden explicitly whether to authorize the next stage.
- `BLOCKED`: request only the exact owner action, authority, or plan/reality resolution named by the packet.
- `PLATEAU`: decide whether the remaining improvement is worth a new bounded brief; never relabel it `PASS`.
- `BUDGET_EXHAUSTED`: decide whether to issue a replacement brief with a numeric extension. A reduced bar first requires an owner-ratified capstone/checkpoint amendment and new exact anchor; the Lead cannot extend or reduce scope itself.

No terminal status automatically opens the next checkpoint.
