# Gauntlet contract amendment + CP-0 re-run — execution plan

**Status: RATIFIED 2026-08-05 — awaiting owner commit, then Phase 1.** All three gates decided
below. Charged to the Gauntlet reserve (≈44 h remain). No phase executes ahead of its order.

**Goal.** Close every defect in `docs/track-b/cp-0-defects.md`, then re-run CP-0 clean-room under the
amended contract and use that run as the acceptance test for the amendment itself. End state: `main`
carries the amended contract and one landed CP-0, the ledger is closed, and **the repository holds
exactly one local branch.**

---

## Ratified decisions

| Gate | Decision | Consequence |
|---|---|---|
| **DEC-1** | **This amendment requisitions `v6.6`.** DEC-AWS cascades to **capstone v6.7 + map v9**. | `progress.md:41`, `:72`, `:142` updated in Phase 0. No map rebuild for this amendment — nothing here changes the stage sequence. |
| **DEC-2** | **All 14 amendments bundle into one `v6.6` package**, ratified together before the re-run. | One ratification, one acceptance run. G1–G14 land as a unit or not at all. |
| **DEC-3** | **The CP-0 re-run is a 100% fresh clean-room build.** No seeding from the archive. | Attempt 2 must prove the amended contract stands on its own. Enables the Phase 5.4 replication check. |

**Execution order, as ratified.** The owner performs Phase 0 and Phase 1 manually and immediately
after committing this plan; Phase 2 onward follows. Phase 1 is therefore executed **under the owner's
own standing authority, before AMD-G13 exists** — G13 then codifies the procedure so it stops
depending on anyone remembering it.

---

## What is being fixed

Thirteen defects. Twelve are in the ledger; **D-CP0-13 is new and is appended in Phase 2.0**, because
it comes from the owner's standing requirement rather than from the CP-0 run.

### D-CP0-13 — No branch or ref reclamation rule *(to be appended to the ledger)*

**Statement.** Nothing in the contract says what happens to `gauntlet/<checkpoint>`, or to any
worktree, after a checkpoint closes. Refs accumulate silently across sessions, and there is no rule
preventing the deletion of a branch that live documents still depend on.

**Evidence.** The 2026-08-05 cleanup found **six worktrees and eight local branches** against one
repository, including an orphan from a third session, none of which any rule required anyone to
reclaim. Simultaneously, `cp-0-defects.md` cites `7526310`, `63ebfab`, and `8f371e5` — all reachable
**only** from `gauntlet/cp-0`. Deleting that branch as "cleanup" would leave the ledger citing SHAs
that garbage collection is free to destroy.

**Impact.** Two failure modes pulling in opposite directions: refs accumulate until nobody knows
which are live, and the obvious remedy — delete them — silently breaks the evidence chain the whole
architecture rests on. The contract has no position on either.

**Ownership.** `AGENTS.md`, `orchestrator-role.md`, `gauntlet-templates.md` §9.

**Remedy.** AMD-G13, below.

### Amendment map

| AMD | Closes | Owner documents | Substance |
|---|---|---|---|
| **G1** | D-CP0-6 | §12 · `engineering-role.md` 8–9 · TMPL §7/§8 | Split `final_candidate_sha` from `evidence_tip_sha`; delta must be verdict-only; gate runs the check |
| **G2** | D-CP0-8, D-CP0-1 (part) | `engineering-role.md:9` · TMPL §7/§8 | Forbid the *influence*, not the *reading*; declared post-Integration read; provenance block; `ASSERTED_ROLE_BOUNDARY` |
| **G3** | D-CP0-12 | `AGENTS.md` · TMPL §7 · new TMPL §9 | Landing Report, gate inspection, owner-only squash merge |
| **G4** | D-CP0-1 (part), D-CP0-5 (floor) | `orchestrator-role.md` launch envelope | Named minimum executor tier and reasoning effort; session-freshness declaration |
| **G5** | D-CP0-2, D-CP0-3 | §12 status vocabulary · `engineering-role.md` ceiling § · new TMPL §10 | `BRIEF_INVALID` as a fifth pre-work status with its own minimal form; brief validation precedes the clock and consumes no ceiling |
| **G6** | D-CP0-4 | TMPL §7/§8 | Packet reproduces the ten required brief fields verbatim; gate validates them against the plan it holds |
| **G7** | D-CP0-5 (abandonment) | `orchestrator-role.md` · §12 | `started_at_utc` + verified state as first observable output; owner-side abandonment convention, distinct from `BUDGET_EXHAUSTED` |
| **G8** | D-CP0-7 | `engineering-role.md` step 4 · TMPL §7/§8 | Each Builder worktree's seed declared; seeding permitted but forces whole-artifact review |
| **G9** | D-CP0-9 | `engineering-role.md:56` | Demote cache routing to a recommendation; `git status --porcelain` stays the only cleanliness test |
| **G10** | D-CP0-10 | `AGENTS.md` · `engineering-role.md` step 1 · TMPL §7 | Topology recorded at start and terminal return; no other session writes to `main` or owned paths while a checkpoint is open |
| **G11** | D-CP0-11 | TMPL §5 | Line citations optional and explicitly non-binding; only the verbatim excerpt is load-bearing |
| **G12** | mandatory-surface scope | §12 · TMPL §7/§8 | Packet declares in-scope/out-of-scope **with a reason** for each of the five surfaces, so gate item 3 has something to check |
| **G13** | **D-CP0-13** | `AGENTS.md` · `orchestrator-role.md` · TMPL §9 | Branch and ref lifecycle; tag-before-delete; the one-branch invariant |
| **G14** | method | `rule-inventory.md` | Re-run the project's own rule-inventory method across the amendment |

**Authoring order: G2 → G1 → G3 → G13 → G5 → G4/G7 → G6/G8/G12 → G9/G10/G11 → G14.**
G2 first because D-CP0-1's remedy is unwritable before it. G1 before G3 because G3's landing rule
needs the two-SHA vocabulary. G13 immediately after G3 because it completes the same boundary.

---

## AMD-G13 in full — branch and ref lifecycle

### The invariant

> **At rest the repository has exactly one local branch: `main`.** While a checkpoint is open it has
> exactly one more: `gauntlet/<checkpoint>`. There is never a third. A branch that is neither `main`
> nor the single open checkpoint branch is a defect to be reclaimed, not a state to be tolerated.

### Disposition at checkpoint close — exactly one, and both end in deletion

| | LAND | DISCARD |
|---|---|---|
| When | The owner accepts the artifact | The attempt is superseded, abandoned, or refused |
| Step 1 | `git merge --squash gauntlet/<cp>` → review staged tree → `git commit` **by hand** | — |
| Step 2 | `git tag land/<cp> <evidence_tip_sha>` | `git tag archive/<cp>-attempt-<k> <evidence_tip_sha>` |
| Step 3 | `git branch -D gauntlet/<cp>` | `git branch -D gauntlet/<cp>` |
| Result | One owner-authored commit on `main`; branch gone; every cited SHA still reachable via tag | Nothing on `main`; branch gone; every cited SHA still reachable via tag |

### The hard rule

> **Tag before delete, always.** A branch may never be deleted while any live document cites a SHA
> reachable only from it. Tags are not branches: they satisfy the one-branch invariant while keeping
> every cited SHA reachable and safe from garbage collection. A cleanup that breaks a citation in
> `cp-0-defects.md`, a verdict, or a Return Packet is not cleanup — it is evidence destruction.
>
> **The citation follows the ref.** When a branch is retired, every live document that named it is
> repointed to the tag in the same operation. A tag that preserves the SHA while the prose still
> points at a deleted branch satisfies the letter of this rule and fails its purpose.

### Who executes what — owner instruction, 2026-08-05

> "One of the CP-0 insights is that I don't want to deal with unnecessary branch management."

Ref hygiene is tedium, not judgement, and delegating it costs nothing that matters. The protection
that matters is **what enters `main`**, and that is untouched.

| Operation | Executor | Why |
|---|---|---|
| INSPECT — topology, diffs, reconciliation | **Agent** | Read-only |
| DISPOSE · **LAND** — the squash and the commit on `main` | **Owner, by hand** | Unchanged. `git merge --squash` stages without committing precisely so the owner authors what lands |
| DISPOSE · **DISCARD** — tag the attempt | **Agent** | Creates a ref, destroys nothing |
| REPOINT — update documents citing the retired branch | **Agent** | Mechanical, and the agent is what breaks it if skipped |
| RECLAIM — delete the branch, remove worktrees, prune | **Agent** | Tedium. Permitted **only** after the disposition is recorded and the tag verified to resolve |

**The one guard that survives delegation:** an agent may never delete a ref whose SHAs are not
already reachable from a verified tag, and may never delete a branch the owner has not dispositioned
as LAND or DISCARD. Deletion is permitted; deciding what the work was worth is not.

### Orchestrator runbook — the automatic part

Added verbatim to `orchestrator-role.md` so reclamation is a step the Orchestrator performs at every
checkpoint close rather than a thing someone remembers:

```text
# 1. INSPECT — read-only, reconcile against the packet's Landing Report
git worktree list
git branch -vv
git tag --list 'land/*' 'archive/*'
git log --oneline --graph main..<evidence_tip_sha>
git diff --stat main...<evidence_tip_sha>
git diff --name-only <final_candidate_sha>..<evidence_tip_sha>   # AMD-G1: evidence paths only

# 2. DISPOSE — owner runs exactly one of:
#    LAND
git checkout main && git merge --squash gauntlet/<cp>
git status && git diff --cached          # review; nothing is committed yet
git commit                               # authored by hand
git tag land/<cp> <evidence_tip_sha>
#    DISCARD
git tag archive/<cp>-attempt-<k> <evidence_tip_sha>

# 3. REPOINT — update every live document that cites the retired branch to cite the tag

# 4. RECLAIM — always, after either disposition
git branch -D gauntlet/<cp>
git worktree remove <each path in the Landing Report>
git worktree prune
git branch -vv                           # MUST show main only
```

**Step 4's final line is the gate.** A checkpoint is not closed until `git branch -vv` shows `main`
alone. `AGENTS.md` gains the matching prohibition: agents never merge, squash, rebase, fast-forward,
or cherry-pick into `main`, never delete a branch the owner has not dispositioned, and never offer to.

---

## Execution phases

### Phase 0 — Preconditions *(owner, ~0.5 h)*

1. Commit this plan on `main`, by hand.
2. Apply DEC-1's renumbering: `progress.md:41`, `:72`, `:142` — DEC-AWS becomes **capstone v6.7 +
   map v9**.
3. Confirm `main` clean; confirm `gauntlet/cp-0` @ `8f371e5` intact with `7526310`, `63ebfab`,
   `8f371e5` all reachable.

### Phase 1 — Archive and discard CP-0 attempt 1 *(owner, ~0.5 h)*

Performed manually under the owner's standing authority, before AMD-G13 exists. G13 later codifies
exactly this sequence.

```text
git tag archive/cp-0-attempt-1 8f371e5
```

**Then repoint the citations — this step is not optional.** `cp-0-defects.md` currently states that
attempt 1's SHAs are "reachable on that branch" and names `gauntlet/cp-0` in its header, its
receipt-gate verification section, and several defect entries. The moment the branch is deleted those
sentences are false. Update each to name `archive/cp-0-attempt-1`. **A ledger left pointing at a
deleted branch is the same citation-breakage D-CP0-13 exists to prevent, committed in prose instead
of in git.**

```text
git branch -D gauntlet/cp-0
git branch -vv                           # expect: main, plus the article worktree branch below
```

**Also reclaim the last article branch.** `claude/gauntlet-loop-article-19d7ae` @ `ca7bf11` is
identical to `main` and its worktree is no longer needed:

```text
git worktree remove /Users/djourno/Downloads/PJM/.claude/worktrees/gauntlet-loop-article-19d7ae
git branch -d claude/gauntlet-loop-article-19d7ae
git worktree prune
git branch -vv                           # MUST show main only
```

Phase 1 ends with the one-branch invariant already true, before the amendment that requires it is
written.

### Phase 2 — Author the amendment *(~6 h)*

**2.0** Append **D-CP0-13** to the ledger with its provenance row and index entry.

**2.1 Rule inventory, before.** Re-run the method that caught two near-drops during the prune:
enumerate every normative rule touched by G1–G13 across `capstone_V6_5.md` §12,
`engineering-role.md`, `gauntlet-templates.md`, `AGENTS.md`, and `orchestrator-role.md`, with its
current location and its post-amendment owner. **This is not optional** — the amendment touches five
documents and the project has already proved twice that targeted greps lose rules.

**2.2 Author G1 … G13** in the order above, one owner per rule, cross-references never restatements.
`capstone_V6_5.md` → `capstone_V6_6.md`; every reference repointed; an amendment sheet
`capstone_V6_5-to-V6_6-amendments.md` in the existing style.

**2.3 Independent review before ratification.** The amendment is judged by a fresh context that did
not author it, against the 2.1 inventory: every enumerated rule present in its assigned owner, no
rule stated normatively in two places, no bar weakened. **Builder ≠ Critic applies to the contract
itself** — the alternative is the contract's authors certifying their own work, which is the exact
thing the contract forbids everywhere else.

**2.4** Ratify. `progress.md` regenerated with the new anchor.

### Phase 3 — Ledger and blocker state *(~0.5 h)*

Mark every defect `REMEDIED BY AMD-Gn — pending acceptance in the CP-0 re-run`. The ledger stays
**OPEN**: an amendment authored is not an amendment proven.

### Phase 4 — Re-run CP-0 under the amended contract *(2 h ceiling)*

**4.1 Negative control first — deliberately issue one deficient brief.** Omit the numeric ceiling.
Expected: a `BRIEF_INVALID` return in AMD-G5's new form, naming the missing field, with **zero clock
consumed and no repository edit**. This is a positive control for the front gate, in the same spirit
as CP-0's own item-2 control. If it returns anything else, G5 has failed and Phase 4 stops.

**4.2 Issue the valid brief** — fresh session, launch envelope carrying AMD-G4's executor floor and
session-freshness declaration, anchored at `capstone_V6_6.md`, same 7-item CP-0 checklist, same 2 h
ceiling.

**4.3 Run** clean-room per DEC-3, to a terminal Return Packet. The Lead is not told that a prior
attempt exists and is given no path to it; `archive/cp-0-attempt-1` is outside its brief.

### Phase 5 — Acceptance: did each amendment actually fix its defect *(~2 h)*

Every amendment gets an observable test in the re-run. **An amendment with no test is not accepted.**

| AMD | Acceptance test | Fails if |
|---|---|---|
| G1 | Packet carries both SHAs; gate runs `git diff --name-only <final>..<tip>` | Anything outside `docs/track-b/evidence/cp-0/` appears |
| G2 | Packet has the provenance block, `ASSERTED_ROLE_BOUNDARY`, and declares any late read with timing | Block absent, or a read is discoverable that the packet did not declare |
| G3 | Packet has a Landing Report; gate's inspection reconciles against the live repo | Any discrepancy between report and repository |
| G4 | Envelope names the executor floor; Lead affirms session freshness | Either absent |
| G5 | 4.1 returns `BRIEF_INVALID` in the new form, zero clock, no edit | Any other status, any clock consumed, or any edit |
| G6 | Packet reproduces the ten brief fields; gate validates them against the plan | A field is missing or does not match |
| G7 | `started_at_utc` + verified state emitted as first observable output | Not observable before the first Builder dispatch |
| G8 | Packet declares each Builder worktree's seed | Any seed undeclared |
| G9 | Text check only — routing is a recommendation, `--porcelain` is the test | Contradiction survives |
| G10 | Packet records topology at start and terminal return | Either missing, or a change goes unreported |
| G11 | Verdicts omit line citations or mark them non-binding | A line citation is presented as binding |
| G12 | Packet declares in/out of scope **with a reason** for all five surfaces | Any surface undeclared |
| G13 | After Phase 6, `git branch -vv` shows `main` only; `archive/cp-0-attempt-1` and `land/cp-0` both resolve; no live document cites a deleted branch | Any extra branch, any unreachable cited SHA, or any stale branch citation in prose |

**5.4 Replication check *(analysis, not a gate)*.** Diff the attempt-2 instrument against
`archive/cp-0-attempt-1`. Two independent clean-room implementations of the same 7-item bar are a
free reading of that bar's clarity: **material divergence on a bar item means the bar is ambiguous,
not that the code is wrong.** Anything found here goes to the ledger as a capstone finding, not a
contract one. DEC-3 is what makes this check meaningful — a seeded attempt 2 would have proved
nothing.

### Phase 6 — Land, reclaim, close *(~1.5 h)*

1. Receipt gate on the attempt-2 packet, including every Phase 5 row.
2. **LAND** per AMD-G13: `git merge --squash gauntlet/cp-0` → review staged tree → commit by hand →
   `git tag land/cp-0 <evidence_tip_sha>`.
3. **REPOINT then RECLAIM**: update any document citing `gauntlet/cp-0`, delete the branch, remove
   every worktree in the Landing Report, prune, confirm `git branch -vv` shows `main` alone.
4. Close the ledger — status `CLOSED`, each defect marked `REMEDIED AND ACCEPTED` with its Phase 5
   evidence. Anything that failed acceptance stays open and blocks CP-1.
5. Discharge the `progress.md` blocker; next pending checkpoint becomes CP-1 behind B-Man-PIT only.

---

## Budget

| Phase | Estimate |
|---|---|
| 0 — preconditions *(owner)* | 0.5 h |
| 1 — archive, repoint, discard, reclaim *(owner)* | 0.5 h |
| 2 — author + inventory + independent review | 6 h |
| 3 — ledger state | 0.5 h |
| 4 — CP-0 re-run | 2 h (attempt 1 used 0.76 h) |
| 5 — acceptance | 2 h |
| 6 — land, reclaim, close | 1.5 h |
| **Total** | **≈13 h against ≈44 h reserve** |

The 24 h of headroom raised on 2026-08-05 currently has no named consumer. This is that consumer —
Phase 6.5 should close the open question in `progress.md` Blockers.

## Risks

- **The re-run finds new defects.** Likely, and it is the point. New IDs continue from D-CP0-14; they
  do not automatically re-block CP-1 unless they are blocking-class, which is an owner call at
  Phase 6.
- **The amendment over-corrects.** The ledger's *What the run confirmed* section is the guard:
  Builder ≠ Critic, computed staleness, worktree isolation, and the expected-state mismatch rule all
  worked and must survive Phase 2 unchanged. Phase 2.3's independent review checks this explicitly.
- **Clean-room costs a known instrument.** DEC-3 means attempt 2 may rediscover the three
  crash-without-ledger-entry bugs attempt 1 already fixed, or miss them. That is the price of the
  test, and it is the right price: if attempt 2's independent Critic does not catch them, that is a
  finding about the bar, not a loss.
- **Phase 2 is authoring, not a checkpoint.** It consumes reserve but has no Gauntlet ceiling and no
  terminal status. If that turns out to matter, it is itself a finding — the contract governs
  checkpoints and says nothing about governance work.
