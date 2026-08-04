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

## CP-2 mandatory label-blind four-catalog outcome (include only for CP-2)
- Scientific bar (Blind Critic never adjudicates; fresh Integration must match the committed winner): [`capstone_V6_5.md` §12 CP-2 exact citation + excerpt]
- Metric/eligibility/tie-break authority: [`capstone_V6_5.md` §4.1 exact citation + excerpt]
- Execution protocol authority: `docs/track-b/cp2-blind-protocol.md` — read only at CP-2.
- Machine contract/commands: `docs/track-b/schemas/cp2-blind-four-catalog.schema.json`; `blind-prepare`, `blind-recompute`, `blind-freeze`, `blind-reveal`, `blind-adjudicate` in `scripts/gauntlet_protocol.py`.

## Owner-only actions already authorized
- none / [credential, signup, browser-bound action, payment, publication]

## Stop and return
Run the bounded Gauntlet autonomously under `engineering-role.md`. Return exactly one consolidated Return Packet with PASS, BLOCKED, PLATEAU, or BUDGET_EXHAUSTED. Stop all Track B work before any later checkpoint. Do not plan or begin it.
```

Clock accounting is defined in `engineering-role.md` § *Active-elapsed wall-clock ceiling*; brief-validity and required fields in § *Required brief fields*; the bar a brief may not reduce is the named plan's §12. This form does not restate them.

## 2. Active `workbench.md`

Create this file only after a valid checkpoint brief arrives.

```markdown
# Active Track B Workbench — [checkpoint]

Plan anchor:
Checkpoint evidence root (`.gauntlet/evidence/<checkpoint>/`):
Current run support root (`.gauntlet/evidence/<checkpoint>/_support/<run-id>/`):
Candidate branch/full commit SHA/tree:
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
| Piece | Disjoint owned paths/artifact | Isolated Builder path/state | Lead serial-integration SHA | Fresh Critic state | Largest open gap |
|---|---|---|---|---|---|

## Mandatory independent surfaces in scope
| Surface | Applicable? | Critic evidence/verdict |
|---|---|---|
| Temporal normalization | | |
| Champion/benchmark schema firewall | | |
| A75 climatology fit lineage | | |
| CP-2 label-blind four-catalog metric recomputation and freeze-before-reveal chain | | |
| M3 hand-checkable CQR threshold recomputation | | |

## Mandatory M1 acceptance-oracle pack (when CP-1 is active)
| Oracle | Independent fixture SHA-256 | Independent expected result | Critic commands/evidence/verdict |
|---|---|---|---|
| M1-O1 — misaligned PT15M chunk stitch | | exactly one four-quarter mean; no three-quarter mean | |
| M1-O2 — missing quarter | | no hourly value; explicit incomplete/recovery | |
| M1-O3 — Berlin fall-back hour | | both 02:00 offsets survive as distinct UTC; 25 rows; true duplicate rejected | |
| M1-O4 — A75 fit-lineage poison | | calibration/eval poison is inert; proper-training poison changes fit | |
| M1-O5 — champion/benchmark schema poison | | valid champion passes; A69/A69-derived/actual injection fails closed; benchmark adds only approved A69 fields and rejects actuals | |

## CP-2 label-blind chain (when CP-2 is active)
Blindness strength: ENFORCED_READ_ISOLATION | COOPERATIVE_PROCEDURAL
Committed source manifest / selection declaration paths and blob hashes: `artifacts/cp2/blind/source-manifest.json` / ... ; `artifacts/cp2/blind/selection-declaration.json` / ...
Current blind-review ID / attempt:
Blind component run/piece/ref/support root:
Custody root (private; never expose contents here):
`blind-public-input.csv` / public manifest / commitment hashes:
Blind metrics / verdict / freeze state:
Integration run/piece/ref/support root:
Reveal / adjudication state:
Latest invalidation/reset reason:

## Integration
- exact final candidate commit SHA/tree:
- reproduction commands:
- tool-generated integrity manifest path/hash:
- schema-valid Critic verdict path/hash:
- fresh Integration-Critic verdict:

## Critic runs
| Unique immutable run ID / piece | Component/Integration | Pre-created candidate ref/SHA | Run root / owned support root | Integrity manifest path/hash | Committed schema hash | Schema-valid verdict path/hash/result |
|---|---|---|---|---|---|---|

## Preserved candidate refs
| Local `refs/gauntlet-evidence/...` ref | Exact SHA | Purpose | Verified? |
|---|---|---|---|

## Exact blocker, if terminal
- none / exact owner or authority request
```

Workbench lifecycle is `engineering-role.md` § *`workbench.md` lifecycle*. The M1 oracle table is mandatory, not illustrative — the bar and the independent-fixture requirement are the plan's §12.

For every component or Integration Critic, choose new ref-safe `<critic-run-id>` and `<piece>` values, initialize its run root, and create/verify its candidate ref at the exact current checkpoint `HEAD` **before** launching the review:

```text
python3 scripts/gauntlet_protocol.py init-evidence --repo-root <abs> --checkpoint <id> --run-id <critic-run-id>
python3 scripts/gauntlet_protocol.py create-ref --repo-root <abs> --checkpoint <id> --run-id <critic-run-id> --piece <piece> --candidate-sha <full-current-head-sha>
python3 scripts/gauntlet_protocol.py verify-ref --repo-root <abs> --checkpoint <id> --run-id <critic-run-id> --piece <piece> --candidate-sha <full-current-head-sha>
```

Evidence-root creation, containment, hashing, and reuse rules are `engineering-role.md` § *Live evidence and commit retention*.

## 3. Builder assignment

```markdown
# Builder assignment — [piece]

Authorized checkpoint:
Lead-created isolated writable detached worktree/snapshot:
Disjoint owned paths/artifact (exact allowlist):
Observable goal:
Concrete acceptance bar:
Relevant ratified rules/citations:
Required tests/reproduction/evidence:
Forbidden scope:
Target wall-clock window within the checkpoint ceiling (Lead-set, non-authoritative):

Implement only this bounded piece and edit only the allowlisted paths. Do not stage, commit, merge, switch branches, update refs, create/remove worktrees, or share a writable Git index with another Builder. Return the changed-path list, artifact/input hashes, exact reproduction commands, evidence, known gaps, and active-elapsed timing to the Engineering Lead. The Lead alone inspects and imports the allowlisted paths, verifies the staged path set, and commits serially on `gauntlet/<checkpoint>`. Do not self-certify the checkpoint or ask a Critic to review an uncommitted diff.
```

## 4. Independent Critic assignment

Use a fresh read-only context under `engineering-role.md` § *Mandatory isolated Critic protocol*, which defines the run/ref/support initialization order, the clean detached checkout, and what the Critic must never receive.

```text
scripts/gauntlet_critic_snapshot.sh create <full-sha> <outside-snapshot-path> <absolute-manifest-path> <critic-run-id>
scripts/gauntlet_critic_snapshot.sh verify <full-sha> <outside-snapshot-path> <absolute-manifest-path> <pre-review-manifest-sha256>
```

```markdown
# Independent Critic — [piece or mandatory surface]

Authorized checkpoint:
Piece ID: [mandatory ref-safe ID]
Pre-created candidate evidence ref: [`refs/gauntlet-evidence/<checkpoint>/<critic-run-id>/<piece>`]
Full candidate commit SHA:
Full candidate tree:
Candidate artifact path/SHA-256:
`plan.filename` (safe repository-relative committed `.md` path):
`plan.sha256` (exact SHA-256 of that blob's bytes at candidate SHA):
`plan.version` (human-readable version):
`plan.bar_citation` (exact human citation):
`plan.bar_excerpt` (non-empty verbatim text present in that same blob):
Observable goal:
Decision-bearing input/data SHA-256 (or explicit N/A):
Exact reproduction commands:
Expected output/tolerance:
Mandatory cache routing (export before any command; ignored byproducts inside the checkout invalidate the review):
- `PYTHONDONTWRITEBYTECODE=1`
- `PYTHONPYCACHEPREFIX=<support-root>/pycache`
- every other tool that writes beside its input directed under the support root
Command stdout/stderr destinations (absolute, outside run root):
Unique immutable Critic run ID: [mandatory ref-safe ID; never reused]
Critic ID: [ref-safe harness context ID when suitable; otherwise assigned]
Critic run root: [absolute `<repo>/.gauntlet/evidence/<checkpoint>/<critic-run-id>/`]
Critic-owned support root: [absolute `<repo>/.gauntlet/evidence/<checkpoint>/_support/<critic-run-id>/`]
Tool-generated integrity manifest path: [absolute `<run-root>/integrity-manifest.json`]
Critic verdict record path: [absolute `<run-root>/critic-verdict.json`]
Canonical verdict schema: [docs/track-b/schemas/critic-verdict.schema.json]
Committed verdict-schema SHA-256: [hash of the schema blob at candidate SHA]

## Before-review integrity
- `git rev-parse --verify HEAD`:
- `git rev-parse --verify 'HEAD^{tree}'`:
- `git diff --quiet`: PASS
- `git diff --cached --quiet`: PASS
- `git status --porcelain=v1 --untracked-files=all --ignored=matching`: EMPTY
- `test ! -e workbench.md`: PASS
- pre-review integrity-manifest SHA-256: [helper create output]

Inspect and rerun independently. Return:
- Verdict: PASS | FAIL
- Bound piece/evidence-ref/candidate SHA/tree, committed schema hash, artifact hash, complete `plan.filename`/`plan.version`/`plan.sha256`/`plan.bar_citation`/`plan.bar_excerpt` binding, and input hashes; prove that the verbatim excerpt occurs in the committed blob
- Exact commands actually executed with exit codes and stdout/stderr absolute paths/SHA-256
- Tool-generated create/verify integrity-manifest path and final SHA-256 from `scripts/gauntlet_critic_snapshot.sh` or equivalent; `verify` receives the recorded pre-review manifest SHA-256
- Separate Critic-verdict path and SHA-256, validated by `python3 scripts/gauntlet_protocol.py validate-verdict --verdict <absolute-path>` against `docs/track-b/schemas/critic-verdict.schema.json`
- Evidence actually inspected/recomputed
- Every file-backed artifact/input/command/evidence path under this run's exact owned support root, with SHA-256, inode link count exactly one, and UTC record time required by the canonical schema; no hard-linked/cross-run/external path or unhashed observation substitutes
- The single largest meaningful gap
- The exact next acceptance test
- Any scope or methodology conflict

Read-only conduct, the post-review re-verify, and the full invalidation list are `engineering-role.md` § *Mandatory isolated Critic protocol* steps 2–5. Do not redesign the project and do not accept claims that are not reproducible from the artifact.
```

On any `FAIL`, the Engineering Lead routes the evidence directly back to a Builder and later launches a fresh Critic; Yarden does not relay messages.

### 4.1 CP-2 label-blind four-catalog review

Applicable only when CP-2 is the authorized checkpoint. The Blind component Critic assignment and the freeze/reveal handoffs are in `docs/track-b/cp2-blind-protocol.md` §2–§3.

## 6. Fresh Integration Critic

```markdown
# Fresh Integration Critic — [checkpoint]

Authorized checkpoint:
Full final candidate commit SHA:
Full final candidate tree:
Final candidate artifact path/SHA-256:
`plan.filename` (safe repository-relative committed `.md` path):
`plan.sha256` (exact SHA-256 of that blob's bytes at final candidate SHA):
`plan.version` (human-readable version):
`plan.bar_citation` (complete checkpoint citation):
`plan.bar_excerpt` (non-empty verbatim text present in that same blob):
Decision-bearing input/data SHA-256 (or explicit N/A):
Clean reproduction commands:
Expected output/tolerances:
Data snapshot/cutoff/hash:
Component and mandatory-surface schema-valid verdict paths/hashes:
Component tool-generated integrity-manifest paths/hashes:
Canonical verdict schema: [docs/track-b/schemas/critic-verdict.schema.json]
Fresh detached checkout before-review integrity evidence:

## CP-2 revealed chain inputs (mandatory only for CP-2)
Blind review ID:
Blindness strength + enforced mechanism/candid limitation:
CP-2 blind schema path/blob SHA-256 and tool blob SHA-256:
Committed identity source-manifest repo path/blob SHA-256: `artifacts/cp2/blind/source-manifest.json` / ...
Committed selection-declaration repo path/blob SHA-256/declared winner: `artifacts/cp2/blind/selection-declaration.json` / ...
Blind component run/piece/ref and manifest/verdict paths/hashes:
Anonymous `blind-public-input.csv`/public-manifest/commitment/metrics paths/hashes:
Freeze path/hash/time:
Reveal path/hash/time:
Integration-owned copied mapping path/hash:
Integration-owned four real source CSV paths/hashes:
Integration-owned copied source manifest path/hash:
Integration-owned copied selection declaration path/hash:
Safe post-reveal preparation record path/hash:
Adjudication/chain-validation destination:

From this fresh read-only context, verify:
1. every item in the complete named CP/FCP checklist against direct evidence;
2. all current independent verdicts and mandatory surfaces;
3. every component `PASS` used for terminal `PASS` binds its declared piece, pre-created evidence ref, its own bound candidate SHA/tree, the same checkpoint and plan identity (`plan.filename`, `plan.version`, and `plan.sha256`) as Integration, the committed schema, and current input hashes; each component and Integration verdict retains its own piece-appropriate `plan.bar_citation` and `plan.bar_excerpt`, and each excerpt is independently proven verbatim in that same committed blob; staleness is computed, not assumed — a component `PASS` still binds **if and only if** its candidate is an ancestor of the final candidate and `git diff --name-only <component-sha>..<final-sha> -- <reviewed_paths>` is empty, and each stale verdict, and only a stale verdict, reruns with a new run ID/ref;
4. cross-component contracts and hard invariants;
5. metrics recomputed from frozen predictions where applicable;
6. clean-environment reproducibility and documentation consistency;
7. absence of unauthorized later-checkpoint work.

For CP-2, run `blind-adjudicate` and validate the full chain exactly as specified in
`docs/track-b/cp2-blind-protocol.md` §4–§5 (Integration-owned copies only, never custody). The
scientific bar it must satisfy — the Blind Critic never adjudicates, and the adjudicated real winner
must equal the committed selection declaration — is `capstone_V6_5.md` §12. `blind_adjudication`
binds `blind_review_id`, `freeze`, `reveal`, `adjudication`, `selected_role`, and
`selection_declaration`; terminal `PASS` requires its `match` to be `true`.

## 7. Consolidated Return Packet

Candidate refs were created before their reviews. Before returning, reverify every cited commit/ref with the associated immutable evidence run ID:

```text
python3 scripts/gauntlet_protocol.py verify-ref --repo-root <abs> --checkpoint <id> --run-id <id> --piece <id> --candidate-sha <full-sha>
```

```markdown
# Track B Checkpoint Return — [M#/CP-#]

Status: PASS | BLOCKED | PLATEAU | BUDGET_EXHAUSTED
Target repository:
Ratified plan anchor:
Checkpoint evidence root:
Frozen evidence root (committed copy):
Exact final candidate commit/tree/branch:
Working-tree state:
Data snapshot/cutoff/hash:
Checkpoint active-elapsed ceiling:
started_at_utc / terminal_at_utc:
Eligible pause ledger (UTC, reason/evidence, all contexts stopped):
Consumed active elapsed: [raw seconds / decimal hours]
Integration verdict and evidence: PASS | FAIL | NOT_RUN — [evidence or exact reason]
Integration integrity manifest (tool-generated path/SHA-256):
Integration Critic verdict record (schema-valid path/SHA-256):

## Critic run inventory
| Unique immutable run ID / piece | Component/Integration | Pre-created candidate ref/SHA | Run root / owned support root | Integrity manifest path/hash | Committed schema hash | Schema-valid verdict path/hash/result |
|---|---|---|---|---|---|---|

## CP-2 label-blind four-catalog chain (mandatory only for CP-2)
Blindness strength: ENFORCED_READ_ISOLATION | COOPERATIVE_PROCEDURAL
Enforced read mechanism or candid same-UID limitation:
Committed source manifest path/blob SHA-256: `artifacts/cp2/blind/source-manifest.json` / ...
Committed selection declaration path/blob SHA-256/declared winner: `artifacts/cp2/blind/selection-declaration.json` / ...
CP-2 blind schema path/blob SHA-256 and tool path/blob SHA-256:

| Attempt / blind-review ID | Final SHA/tree | Blind run/piece/ref/support | Custody-record path/SHA-256 + receipt-bound SHA/modes | `blind-public-input.csv` / manifest / commitment / receipt hashes | Metrics path/hash + Blind verdict | Integration run/piece/ref/support | Freeze path/hash/time | Reveal + Integration-owned copy paths/hashes/time | Adjudication path/hash/winner | Result/reset reason |
|---|---|---|---|---|---|---|---|---|---|---|---|

Chronology check: prepare < Blind metrics < Blind verify/verdict PASS < Integration init/ref < freeze < reveal < adjudication < Integration verify/verdict.
Mapping reuse check: PASS | FAIL
Blind Critic did not choose or assert any winner: PASS | FAIL

## Preserved candidate refs
| Local evidence ref (`scripts/gauntlet_protocol.py create-ref/verify-ref`) | Exact commit SHA | Purpose | Verified reachable? |
|---|---|---|---|

## Complete named CP/FCP checklist
| Criterion citation | PASS/OPEN | Direct evidence/reproduction |
|---|---|---|

## Independent criticism
| Piece/surface | Critic/run ID | Own bound candidate SHA/tree + computed-current vs final (ancestor + no reviewed_paths changed) | Artifact/input hashes | Plan filename/blob hash/version/citation + verbatim excerpt | Exact commands/tolerances | Integrity manifest path/hash | Schema-valid verdict path/hash/result | Largest gap and disposition |
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

## 8. Orchestrator receipt and gate

The Orchestrator's receipt is a **gate on the packet, not a re-derivation of hashes**. Confirm that
the packet:

1. names the authorized repository, the single checkpoint, and the exact ratified plan anchor;
2. maps **every item in the full named CP/FCP checklist** — not a convenience extract — to direct
   evidence, and hides no open item behind `PASS`;
3. includes every applicable mandatory independent surface and, at M1, all five acceptance oracles;
4. inventories, for every required component/oracle/Integration review, a unique immutable run root
   with its separate integrity manifest and schema-valid verdict record, its owned support root, its
   pre-created ref/SHA pair, and their hashes;
5. reports a successful `validate-verdict` for every verdict record and `verify-ref` for every cited
   ref — the Orchestrator checks the **reported exit codes**, and does not recompute hashes itself;
6. shows a current fresh Integration-Critic `PASS` for any supported `PASS`, and uses `NOT_RUN` only
   in a non-`PASS` return that names the exact terminal reason.

What invalidates an individual verdict is `engineering-role.md`; what the closing bar is, and what
each terminal status means, is the named plan's §12. The receipt re-litigates neither.

For CP-2, additionally require the §7 chain table to be complete and its blindness-strength label
honest. The chain's own validity conditions are `docs/track-b/cp2-blind-protocol.md`; the scientific
bar — Blind Critic never adjudicates, adjudicated winner equals the committed selection declaration —
is `capstone_V6_5.md` §12.

- Supported `PASS`: close only that checkpoint in `progress.md`, summarize its evidence, then ask Yarden explicitly whether to authorize the next stage.
- `BLOCKED`: request only the exact owner action, authority, or plan/reality resolution named by the packet.
- `PLATEAU`: decide whether the remaining improvement is worth a new bounded brief; never relabel it `PASS`.
- `BUDGET_EXHAUSTED`: decide whether to issue a replacement brief with a numeric extension. A reduced bar first requires an owner-ratified capstone/checkpoint amendment and new exact anchor; the Lead cannot extend or reduce scope itself.

No terminal status automatically opens the next checkpoint.
