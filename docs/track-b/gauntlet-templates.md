# Track B Gauntlet — Canonical Templates

Boundary-contract forms, not a second capstone plan. The ratified plan named in `progress.md` is
normative; `engineering-role.md` owns the execution process. Replace every bracketed field; never
infer an anchor from the highest version on disk.

Isolation is a plain `git worktree` at the candidate SHA. Verdicts are markdown files committed
under `docs/track-b/evidence/<checkpoint>/`. There is no protocol tool, schema, or evidence-ref
namespace.

---

## 1. Orchestrator checkpoint brief

```markdown
# Track B Checkpoint Brief — [M#/CP-# or FM#/FCP-#]

Target repository: [absolute path or unambiguous repo name]
Authorized checkpoint: [exactly one checkpoint]
Ratified plan anchor: [exact filename and version from progress.md]
Complete checkpoint checklist: [exact citation to the full named CP/FCP checklist]
Supporting sections: [exact citations needed for this checkpoint]
Total checkpoint active-elapsed ceiling: [numeric hours, orientation through terminal return]

## Orchestrator-reported expected state
- branch / commit / working-tree expectation
- completed predecessor and artifacts expected to exist
- data snapshot/cutoff expected

Engineering-Lead must verify this against the repository before relying on it. A material
mismatch is returned, not silently reconciled.

## Observable outcome
[The state that must exist when this checkpoint closes.]

## Complete authoritative checkpoint bar
- [every item in the named CP/FCP checklist, with citation]

## Task-specific supporting extract
- [supporting-plan citation]: [faithful outcome-level statement]

The complete named CP/FCP checklist remains controlling even if an extract omits an item. An
extract may not weaken, strengthen, or replace it.

## Applicable constraints
- [ratified architecture/data/method constraints]
- $0 expected run rate; $65/month policy ceiling
- M3 / 16 GB / CPU-only, unless the named plan says otherwise

## CP-2 label-blind four-catalog outcome (include only for CP-2)
- Scientific bar — Blind Critic never adjudicates; fresh Integration must match the committed
  selection declaration: [`capstone_V6_5.md` §12 CP-2 citation + verbatim excerpt]
- Metric / eligibility / tie-break authority: [`capstone_V6_5.md` §4.1 citation + verbatim excerpt]
- Blinding is procedural: the Lead withholds the mapping and reveals only after the Blind verdict
  is written. The packet must label it `COOPERATIVE_PROCEDURAL`.

## Owner-only actions already authorized
- none / [credential, signup, browser-bound action, payment, publication]

## Executor preconditions
- Minimum executor tier and reasoning effort: [named tier · named effort]
- This must be a **new session** that has not read `orchestrator-role.md`, `progress.md`, the
  syllabus, or Track A/C material. Affirm this in the packet's provenance block.

## Stop and return
Emit `started_at_utc` and your verified repository state as your first observable output. Then run
the bounded Gauntlet autonomously under `engineering-role.md`. Return exactly one Return Packet
with PASS, BLOCKED, PLATEAU, or BUDGET_EXHAUSTED — or, if this brief is invalid, return
BRIEF_INVALID on the §10 form before editing anything. Stop all Track B work before any later
checkpoint. Do not plan or begin it.
```

Clock accounting is `engineering-role.md` § *Active-elapsed wall-clock ceiling*; brief validity and
required fields are § *Required brief fields*; the bar a brief may not reduce is the plan's §12.

---

## 2. Active `workbench.md`

Create only after a valid brief arrives. Git-ignored; never committed, never carried upward.

```markdown
# Active Track B Workbench — [checkpoint]

Plan anchor:
Candidate branch / full commit SHA:
Checkpoint active-elapsed ceiling:
started_at_utc / last_updated_at_utc:
Consumed active elapsed: [raw seconds / decimal hours]

## Eligible pause ledger
| paused_at_utc | resumed_at_utc | seconds | reason/evidence | all contexts stopped? |
|---|---|---:|---|---|

## Authorized goal and bar
- criterion → evidence required

## Lead-chosen pieces
| Piece | Owned paths | Builder worktree | Integration SHA | Critic verdict | Largest open gap |
|---|---|---|---|---|---|

## Mandatory independent surfaces in scope
| Surface | Applicable? | Verdict file |
|---|---|---|
| Temporal normalization | | |
| Champion/benchmark schema firewall | | |
| A75 climatology fit lineage | | |
| CP-2 label-blind four-catalog metric recomputation | | |
| M3 hand-checkable CQR threshold recomputation | | |

## Mandatory M1 acceptance-oracle pack (when CP-1 is active)
| Oracle | Independent fixture | Independent expected result | Critic commands / verdict |
|---|---|---|---|
| M1-O1 — misaligned PT15M chunk stitch | | exactly one four-quarter mean; no three-quarter mean | |
| M1-O2 — missing quarter | | no hourly value; explicit incomplete/recovery | |
| M1-O3 — Berlin fall-back hour | | both 02:00 offsets distinct in UTC; 25 rows; true duplicate rejected | |
| M1-O4 — A75 fit-lineage poison | | calibration/eval poison inert; proper-training poison changes fit | |
| M1-O5 — champion/benchmark schema poison | | champion passes; A69/actual injection fails closed | |

## Integration
- final candidate SHA:
- reproduction commands:
- Integration verdict file:

## Exact blocker, if terminal
- none / exact owner or authority request
```

The M1 oracle table is mandatory, not illustrative — the bar and the independent-fixture
requirement are the plan's §12.

---

## 3. Builder assignment

```markdown
# Builder assignment — [piece]

Authorized checkpoint:
Your worktree (Lead-created, writable):
Owned paths (exact allowlist):
Observable goal:
Concrete acceptance bar:
Relevant ratified rules/citations:
Required tests/reproduction/evidence:
Forbidden scope:
Target window within the checkpoint ceiling (Lead-set, non-authoritative):

Implement only this piece and edit only the allowlisted paths. Do not stage, commit, merge,
switch branches, update refs, or manage worktrees. Return the changed-path list, exact
reproduction commands, evidence, and known gaps to the Engineering Lead. The Lead alone imports
those paths and commits serially on `gauntlet/<checkpoint>`. Do not grade your own work, write a
verdict, or mark any CP item complete.
```

---

## 4. Independent Critic assignment

The Lead first commits the candidate, then creates a clean detached worktree at that SHA:

```text
git worktree add --detach ../critic-<piece> <full-candidate-sha>
git -C ../critic-<piece> status --porcelain     # must be empty
```

```markdown
# Independent Critic — [piece or mandatory surface]

Authorized checkpoint:
Piece:
Full candidate commit SHA:
Your worktree (clean, detached, read-only to you):
Artifact path:
Controlling plan: [repo-relative .md] · version [v] · bar citation [§x.y]
Verbatim bar excerpt:
> [exact text from that file at this SHA]
Decision-bearing inputs:
Exact reproduction commands:
Expected output / tolerance:

Inspect and rerun the real artifact. You do not receive the Builder's checkout, diff, reasoning,
summary, or history, and you may not edit anything or inspect a Builder workspace. Confirm the
bar excerpt above appears verbatim in the cited plan at this SHA. Before writing your verdict,
confirm the worktree is still clean and HEAD unchanged.

Return the verdict in §5. Do not redesign the project, and do not accept a claim you cannot
reproduce from the artifact.
```

On any `FAIL` the Lead routes the gap directly back to a Builder and later launches a fresh
Critic; Yarden never relays messages. No comparison is called blind merely because labels were
renamed.

---

## 5. Critic verdict

One markdown file, committed at `docs/track-b/evidence/<checkpoint>/<piece>-<round>.md`.

```markdown
# Verdict — [piece] — round [n]

Status: PASS | FAIL | BLOCKED
Checkpoint: [M#/CP-#]
Candidate SHA: [full sha]
Reviewed paths: [repo-relative paths this review actually covers — the staleness rule binds here]
Controlling plan: [file] · [version] · [bar citation]
Bar excerpt (verbatim, verified present at this SHA):
> [exact text]
Artifact: [path]
Worktree clean before and after review: yes/no

## What I inspected
- exact files, data, and pages

## Commands actually run
```text
[command]   → exit [n]
[observed output or sha256sum of the output file]
```

## Bar comparison
| Criterion | Evidence | Result |
|---|---|---|

## Largest remaining gap
[one, high-impact — omit only on PASS]

## Exact next acceptance test
[the observable condition that would close it]

## Non-blocking observations
- [optional]
```

`BLOCKED` means the check could not be performed (missing token, unavailable API). It is never a
substitute for `FAIL`.

**`Reviewed paths` is the soundness condition of computed staleness.** Declare them honestly and
broadly enough to cover what the verdict actually depends on; understating them is the one way to
make verdict reuse unsound. Integration checks that each declared path exists in the candidate tree.

**Line numbers are not part of the citation.** Only the verbatim bar excerpt and its presence in the
cited plan at the candidate SHA are load-bearing. A line range may be added as a courtesy and is
explicitly **non-binding** — line numbers move whenever the plan is edited while the quoted text does
not, which is precisely why the excerpt mechanism exists. A mismatched line range is never a defect
in the verdict.

---

## 6. Fresh Integration Critic

New clean worktree at the **final** candidate SHA, same contract as §4.

```markdown
# Fresh Integration Critic — [checkpoint]

Final candidate SHA / your worktree:
Controlling plan · version · complete checkpoint bar citation + verbatim excerpt:
Component verdict files relied on:
Clean reproduction commands / expected outputs:
Data snapshot / cutoff:

From this fresh context, verify:
1. every item in the complete named CP/FCP checklist against direct evidence;
2. every required component verdict exists, is PASS, and is computed-current — its candidate is an
   ancestor of the final candidate and `git diff --name-only <component-sha>..<final-sha> --
   <reviewed paths>` is empty;
3. cross-component contracts and hard invariants;
4. metrics recomputed from frozen predictions where applicable;
5. clean-environment reproducibility and documentation consistency;
6. absence of unauthorized later-checkpoint work.

For CP-2, additionally apply the §4.1 identities, eligibility comparisons and deterministic
tie-breaks after reveal, and confirm the adjudicated real winner equals the committed selection
declaration. A mismatch is FAIL.

Return a §5 verdict. Do not redesign.
```

---

## 7. Consolidated Return Packet

```markdown
# Track B Checkpoint Return — [M#/CP-#]

Status: PASS | BLOCKED | PLATEAU | BUDGET_EXHAUSTED
Target repository / ratified plan anchor:
Checkpoint branch: gauntlet/<checkpoint>
final_candidate_sha (Integration-reviewed; every bar binds here):
evidence_tip_sha (branch tip after the Integration verdict was committed):
Verdict-only delta: `git diff --name-only <final_candidate_sha>..<evidence_tip_sha>`
  → [paths, all of which must be under docs/track-b/evidence/<checkpoint>/]
Working-tree state:
Data snapshot / cutoff / hash:
Checkpoint active-elapsed ceiling:
started_at_utc / terminal_at_utc:
Eligible pause ledger (UTC, reason, all contexts stopped):
Consumed active elapsed: [raw seconds / decimal hours]
Integration verdict: PASS | FAIL | NOT_RUN — [verdict file or exact reason]

## Brief fields as issued
Reproduce the ten required fields verbatim from the brief, so the Orchestrator can validate the
authorization it wrote against the plan it holds.
| Required field | As issued in the brief |
|---|---|

## Provenance and read scope
Documents read during the decision-bearing phase: [exhaustive]
Reads after the final Integration verdict, solely to author this packet:
  [document] — [UTC] — [why necessary] — [what it did NOT influence]
Role-boundary guarantee: ASSERTED_ROLE_BOUNDARY — the Lead's own declaration. The harness does
  not enforce read isolation and this packet does not claim it does.

## Builder worktree seeds
| Piece | Worktree | Seed — brief-authored, or copied from [path] at [state] |
|---|---|---|

## Repository topology
| | At started_at_utc | At terminal return |
|---|---|---|
| Worktrees | | |
| Branches | | |
Changes during the run: [none / exact]

## Verdicts
| Piece / surface | Candidate SHA | Reviewed paths | Verdict file | Result | Largest gap and disposition |
|---|---|---|---|---|---|

## Mandatory surface scope
| Surface | In scope? | Why | Verdict file |
|---|---|---|---|
| Temporal normalization | | | |
| Champion/benchmark schema firewall | | | |
| A75 climatology fit lineage | | | |
| CP-2 label-blind four-catalog recomputation | | | |
| M3 CQR threshold recomputation | | | |

## CP-2 label-blind chain (only for CP-2)
Blindness: COOPERATIVE_PROCEDURAL — the Lead withheld the mapping; not cryptographically enforced.
| Attempt | Mapping file (withheld until) | Blind verdict | Reveal time | Adjudicated winner | Matches committed declaration? |
|---|---|---|---|---|---|

## Complete named CP/FCP checklist
| Criterion citation | PASS/OPEN | Direct evidence / reproduction |
|---|---|---|

## Engineering decisions
- decision and rationale
- rejected alternatives and why
- largest failure the Gauntlet uncovered, and how it was repaired

## Reproduction
- exact commands · artifacts · metrics/screenshots

## Open risks or exact owner action
- none / exact request

## Landing report
Diff against main: `git diff --stat main...<evidence_tip_sha>` → [summary]
Commits on the branch: `git log --oneline main..<evidence_tip_sha>` → [list]
Worktrees created by this checkpoint: [paths] — all removed / [exceptions with reason]
Worktrees NOT created by this checkpoint: [paths, SHA, clean/dirty] — left untouched
Other gauntlet/* branches present: [list, or none]
Proposed disposition: LAND | DISCARD — [one-line rationale]
Proposed commit message: [subject + body, for the owner to use, edit, or discard]

## Defense questions
1. [3–5, grounded in actual architecture, tradeoffs, and evidence]

Track B has stopped. No later-checkpoint work has begun.
```

The Landing Report is a report, never an action. The disposition is the owner's and the commit that
reaches `main` is authored by hand — see `AGENTS.md` § *Branch and ref lifecycle* and §9 below.

---

## 8. Orchestrator receipt and gate

A gate on the packet, not a re-derivation. Confirm that it:

1. names the authorized repository, the single checkpoint, and the exact ratified plan anchor;
2. maps **every item** in the full named CP/FCP checklist — not a convenience extract — to direct
   evidence, and hides no open item behind `PASS`;
3. includes every applicable mandatory independent surface and, at M1, all five acceptance oracles;
4. cites, for every required review, a committed verdict file naming its candidate SHA, its bar
   citation and verbatim excerpt, and the commands actually run;
5. shows a current fresh Integration-Critic `PASS` for any supported `PASS`, and uses `NOT_RUN`
   only in a non-`PASS` return that names the exact terminal reason;
6. carries **both** terminal SHAs — run `git diff --name-only <final_candidate_sha>..<evidence_tip_sha>`
   yourself and confirm it returns nothing outside `docs/track-b/evidence/<checkpoint>/`. Do not take
   the packet's word for it;
7. carries a **provenance block**. A packet without one is returned unread — an absent block is not
   an assertion that no late read occurred;
8. reproduces the **ten required brief fields**, and they match the brief you issued and the plan you
   hold;
9. declares **every Builder worktree's seed**, and **each of the five mandatory surfaces** as in or
   out of scope with a reason;
10. carries a **Landing Report** that reconciles against the live repository. Run the §9 inspection.
    A discrepancy between what the packet says the checkpoint left behind and what the repository
    actually holds is a gate failure, not a footnote.

What invalidates an individual verdict is `engineering-role.md`; the closing bar and the meaning of
each terminal status are the plan's §12. The receipt re-litigates neither.

- **Supported `PASS`:** close only that checkpoint in `progress.md`, summarize its evidence, then
  ask Yarden explicitly whether to authorize the next stage.
- **`BLOCKED`:** request only the exact owner action, authority, or resolution named.
- **`PLATEAU`:** decide whether the remaining improvement warrants a new bounded brief; never
  relabel it `PASS`.
- **`BUDGET_EXHAUSTED`:** decide whether to issue a replacement brief with a numeric extension. A
  reduced bar first requires an owner-ratified amendment and a new exact anchor.

No terminal status automatically opens the next checkpoint.

---

## 9. Landing inspection, disposition, and reclamation

Closing a checkpoint in program state and landing its code are **two decisions**. §8 gates the
packet; this section disposes of the tree. A checkpoint is not closed until `git branch -vv` shows
`main` alone.

**Step 1 — INSPECT (agent, read-only).** Reconcile against the packet's Landing Report:

```text
git worktree list
git branch -vv
git tag --list 'land/*' 'archive/*'
git log --oneline --graph main..<evidence_tip_sha>
git diff --stat main...<evidence_tip_sha>
git diff --name-only <final_candidate_sha>..<evidence_tip_sha>   # evidence paths only
```

**Step 2 — DISPOSE (exactly one).**

*LAND — owner, by hand. Never delegated, never agent-executed.*

```text
git checkout main && git merge --squash gauntlet/<cp>
git status && git diff --cached      # review the staged tree; nothing is committed yet
git commit                           # authored by hand, after the owner's own review
git tag land/<cp> <evidence_tip_sha>
```

`git merge --squash` stages the merged tree and deliberately stops short of a commit. That is the
point: the commit reaching `main` is authored, not generated. It also collapses candidate, component
verdicts and evidence tip into one commit, so the two-terminal-SHA ordering never propagates.

*DISCARD — agent-executed.*

```text
git tag archive/<cp>-attempt-<k> <evidence_tip_sha>
```

**Step 3 — REPOINT (agent).** Update every live document that cites the branch about to be deleted,
in the same operation. A tag that preserves the SHA while the prose still points at a deleted branch
satisfies the letter of the rule and fails its purpose.

**Step 4 — RECLAIM (agent).** Only after the disposition is recorded and the tag verified to resolve:

```text
git branch -D gauntlet/<cp>
git worktree remove <each path in the Landing Report>
git worktree prune
git branch -vv                       # MUST show main only
```

**Guards.** Never delete a ref whose SHAs are not already reachable from a verified tag. Never delete
a branch the owner has not dispositioned. Deletion is delegable; deciding what the work was worth is
not.

---

## 10. `BRIEF_INVALID` return

A **pre-work** return: the authorization was malformed, so no work started, no clock was consumed,
and no repository file was edited. It is the only terminal status that returns no Return Packet.

```markdown
# Brief Invalid — [checkpoint id as named, or "unnamed"]

Status: BRIEF_INVALID
Target repository as named:
validation_started_at_utc / returned_at_utc:
Clock consumed: none — brief validation precedes the ceiling
Repository edits made: none

## Missing or contradictory required fields
| Required field | State in the brief |
|---|---|

## Repository state verified before returning
- [whatever was checked, or "none — the brief was invalid on its face"]

## What would make this brief executable
- [the exact fields to supply; nothing else]
```

The Orchestrator's disposition is to reissue a complete brief. `BRIEF_INVALID` records that an
attempt was made and correctly refused — it does not open, close, or advance a checkpoint, and it
consumes no reserve.
