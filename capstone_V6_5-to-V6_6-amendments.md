# capstone v6.5 → v6.6 — amendment sheet

**Ratified 2026-08-05.** Owner-approved. **Execution-contract only.**

**Nothing scientific moved.** No bar, invariant, acceptance criterion, feed identifier, fold scheme,
metric definition, coverage requirement, or scope boundary changed. **§§2–3, §§5–11 and §13 are
byte-identical to v6.5.**

**One checklist change, and it adds rather than relaxes.** CP-1 through CP-5 each gain an explicit
Integration-verdict line. It creates no new obligation — §12's `PASS` definition already required a
fresh Integration `PASS` at every checkpoint — but the requirement previously appeared in a
checklist only at CP-0, so five checklists could be read end to end without it in view. Nothing was
removed from any checklist, and no threshold moved.

Two sections outside §12 did change, and a reader must not be told otherwise. **§1** carries the
version-delta block. **§4.1's canonicalization pointer was corrected**: it cited three `blind-*`
commands retired with the protocol tooling, and templates §4–§6 for a "schema and canonicalization
contract" those sections do not contain. The paragraph now states that it is itself the contract,
applied by hand. **A CP-2 Lead must re-read §4.1** — templates §1 routes them there for the metric,
eligibility and tie-break authority.

That correction is also the cautionary tale of this amendment: the defect survived four independent
review rounds because every one of them was told §§1–11 were unchanged. A scope claim is an
instruction not to look.

Every other edit is in §12 or in the four contract documents §12 points at.

**Why a version bump at all.** Three of the changes alter what `PASS` *means* — the SHA a bar binds
to, the statuses a checkpoint may return, and the conditions that invalidate a `PASS`. Under the
version-precedence rule those are anchor-class and cannot ship as a corrective pass, so v6.6 exists
and no brief may cite it until `progress.md` names it.

**Numbering.** DEC-1 requisitioned v6.6 for this package. DEC-AWS, parked until G5, cascades to
**capstone v6.7 + map v9**; map v8 is deliberately left unused so plan and map numbering stay
aligned. No map rebuild — nothing here changes the stage sequence.

## Provenance

Every amendment closes a defect in `docs/track-b/cp-0-defects.md`, opened when the first CP-0 handoff
was refused at the front gate and extended by CP-0's `PASS`, its receipt gate, and the Phase 2.1 rule
inventory. Seventeen defects. The amendment closes all of them, including D-CP0-10 in full — its concurrent-session half was specified in the plan, omitted from the first authoring pass, and authored as `R7` after the fifth review. The full plan is
`docs/track-b/gauntlet-amendment-plan.md`; the rule accounting is `docs/track-b/rule-inventory.md`
§ *v6.6 amendment inventory*.

## §12 changes

| Change | Was | Is |
|---|---|---|
| Terminal statuses | Four: `PASS` · `BLOCKED` · `PLATEAU` · `BUDGET_EXHAUSTED` | Five, adding **`BRIEF_INVALID`** — a pre-work status: the authorization was malformed, so no work started, no clock consumed, no file edited. The only status returning no Return Packet |
| Abandonment | Undefined. A stalled executor returned nothing and had no vocabulary | Named explicitly as **owner-side and not a Lead status**, and explicitly **not** `BUDGET_EXHAUSTED` — that status asserts the ceiling was consumed by work, which an abandoned run cannot evidence |
| `PASS` definition | Integration `PASS` + computed-current component bindings | Adds: Integration bound to **`final_candidate_sha`**, and a **verdict-only delta** between it and `evidence_tip_sha` |
| Checklist item 7 — CP-0 originally, now **every CP** | Present only at CP-0; CP-1–CP-5 relied on the §12 `PASS` definition alone | Binds `final_candidate_sha`, evidence tip verdict-only, and now stated explicitly in all six checklists so none is closable without it in view. No bar weakened — it restates an existing §12 requirement |
| Mandatory surfaces | "when their subject matter is in scope" | Scope is **declared, never inferred**: the packet states each of the five as in or out of scope **with a reason**. An unstated judgement is indistinguishable from an unmade one |

## The circularity, and why it needed naming

v6.5 required Integration `PASS` "at the exact final candidate SHA/tree" while
`engineering-role.md` required every verdict to be committed *after* its review. For the Integration
verdict — the last one, with nothing above it — recording it always creates a commit no Integration
Critic reviewed. **No ordering satisfied both.** CP-0 satisfied item 7 only because the delta happened
to be a single evidence file, which nothing required.

v6.6 names two SHAs instead: `final_candidate_sha` is what the Integration Critic reviewed and what
every bar binds to; `evidence_tip_sha` is the branch tip afterwards; the delta between them must
contain nothing outside `docs/track-b/evidence/<checkpoint>/`, and the Orchestrator runs that command
itself rather than accepting the claim. **CP-0 attempt 1 satisfies the new wording retroactively** —
what it achieved by accident is now a required property.

## Contract-document changes (§12 points at these; it does not restate them)

**`engineering-role.md`** — role boundary scoped to *influence* rather than *reading*, with a declared
post-Integration read permitted solely to author the packet and a mandatory provenance block labelled
`ASSERTED_ROLE_BOUNDARY`; `BRIEF_INVALID` replaces the unnamed "return the discrepancy"; brief
validation precedes the clock and consumes no ceiling; `started_at_utc` plus verified state as the
first observable output; Builder worktree seeds declared and seeded pieces reviewed whole; cache
routing demoted to a recommendation; topology recorded at start and terminal return; a terminal
handover section.

**`AGENTS.md`** — new § *Branch and ref lifecycle*: **branch accountability** — every branch an agent opens is declared
in its terminal return, and anything unaccounted is **escalated to the owner**, never auto-deleted and
never a block on a checkpoint — LAND/DISCARD dispositions, **tag before delete**, **the citation follows the ref**, and an execution split in which
agents inspect, tag, repoint and reclaim while **the landing commit stays owner-authored**; plus `R7`, which closes D-CP0-10's concurrent-session half by escalation rather than prohibition: concurrent writes are caught by the staleness rule, and the topology record makes them visible and attributable.

**`docs/track-b/gauntlet-templates.md`** — §1 gains executor-floor and session-freshness
preconditions; §5 gains **`Reviewed paths`** and marks line citations non-binding; §7 gains both
SHAs, the brief-field reproduction, the provenance block, Builder seeds, topology, surface scope and
the Landing Report; §8 gains five gate items the Orchestrator runs itself; **new §9** landing,
disposition and reclamation; **new §10** the `BRIEF_INVALID` form.

**`orchestrator-role.md`** — the launch envelope names a minimum executor tier and reasoning effort
and requires a session-freshness affirmation; the abandonment convention; landing and reclamation as
a gate step, closing when the checkpoint's own branch is dispositioned and reclaimed.

## The one that was hiding in plain sight

**D-CP0-16.** `E1` required every verdict to declare `reviewed_paths`, and `E2`–`E4` — all of
computed staleness — take that set as input. **The §5 verdict form had no such field.** Both CP-0
verdicts complied with the form and declared none; the Lead used the `Artifact:` line as an implicit
set and the Integration Critic computed the diff against paths never formally declared anywhere.

CP-0's staleness computation was sound because two competent agents independently chose compatible
implicit sets — not because the contract collected them. The rule's stated soundness condition is
"declare `reviewed_paths` honestly and broadly", and a field that does not exist cannot be declared
at all. v6.6 adds it to the form and to the packet's verdict table, with the soundness condition
printed where the Critic will read it.

## Rule accounting

**141 enumerated baseline → 168**, with **27 amended, 27 added, 0 retired**.

The baseline is 105 live executor-side rules after Option C, plus two domains enumerated for the
first time during this amendment: **Q** (23, `orchestrator-role.md` — D-CP0-14) and **S** (13,
`AGENTS.md` — D-CP0-17). Both had been amended for months without ever being inventoried; the second
was discovered only because this amendment made `AGENTS.md` an owner and recorded its baseline as
zero. New domain **R** (7 rules, `AGENTS.md`) carries the ref lifecycle and the one-writer rule,
taking over territory retired domains H and M vacated.

The Phase 1 domain tables in `rule-inventory.md` are now marked in place: 32 rules struck as
`RETIRED — Option C`, 8 restated with their current wording. That closes D-CP0-15, which had left
the ledger describing machinery deleted months earlier.

## Not yet proven

The amendment is authored, not validated. It is accepted only when the clean-room CP-0 re-run
exercises each amendment against its acceptance test in
`docs/track-b/gauntlet-amendment-plan.md` Phase 5 — including a deliberately deficient brief as a
negative control for `BRIEF_INVALID`. `docs/track-b/cp-0-defects.md` stays **OPEN** until then.

**Superseding note, 2026-09-04 — owner-authorized, task-scoped suspension of the Governance
Lockdown. The paragraph above is retained unedited as the record of what was required at
ratification; this note states what is true now.** The clean-room re-run executed on 2026-08-06 and
the Phase-5 matrix returned **11 of 13**: `AMD-G7` failed and **`AMD-G5`'s negative control was
never exercised**. On 2026-09-04 the owner **knowingly waived the AMD-G5 negative control**. It is a
closed decision, not a pending test, and it is **not** a condition on the defects ledger or on CP-1.
`BRIEF_INVALID` itself — the fifth terminal status, its clock-exclusion rule and the §10 form —
remains fully in force and unamended; only its deliberate negative-control exercise is waived. The
ledger stays OPEN on its remaining conditions alone: D-CP0-18 and D-CP0-19 re-tested.
