# Capstone v6.4 → v6.5 — capture-schedule feasibility amendment

**Status:** owner-ratified 2026-08-04. Scope-preserving. No scientific criterion is weakened,
removed, or relabelled.

## The defect this closes

The v6.4 §3 point-in-time capture contract requires A65/A01 captures on **at least three
non-consecutive delivery days**, at 10:30 and 11:45 Europe/Berlin on D-1. Non-consecutive puts a
floor of five calendar days on the work, and a failed, partial, or rate-limited request does not
count — so the real span is longer whenever an attempt misses.

v6.4 placed that requirement inside the **CP-1 checklist**, and CP-1 runs under a single
active-elapsed wall-clock ceiling — the milestone's own allocation plus CP-1's 6 h Gauntlet
planning reserve, combined by the Orchestrator at issue time. The two are not co-schedulable at
any plausible value of that ceiling, and `engineering-role.md` offers no reading that survives:

- Treat the wait as an **eligible pause**: eligibility requires *all* Lead/Builder/Critic/
  Integration/test/tool activity to be stopped. CP-1 would have to freeze completely for five or
  more days to satisfy a bookkeeping rule.
- Treat it as **not** a pause: the clock runs continuously across those calendar days — roughly
  120 hours of wall clock, exceeding any plausible CP-1 ceiling — and CP-1 returns
  `BUDGET_EXHAUSTED` on day one, always.

This is a collision between the AMD-2 capture contract and the single-active-clock ceiling model.
Both predate the Gauntlet tooling work; neither is wrong on its own.

## Why the ceiling was not simply raised

The ceiling measures *work consumed*, not *calendar span*. Inflating it to ~130 h to absorb waiting
would give a genuinely stuck or looping Lead that much runway before `BUDGET_EXHAUSTED` fires,
trading a real control for a bookkeeping convenience. It would also corrupt the program schedule:
CP-1's 6 h is part of the 22 h Gauntlet planning reserve that feeds the whole-program envelope, and
`progress.md` labels that reserve "planning-load capacity … not a stand-alone runtime ceiling."

## The split

| Stage | Who | Clock | Scope |
|---|---|---|---|
| **M0.5 / CP-0** | Engineering Lead, bounded Gauntlet | short active-elapsed ceiling | Author and independently review the capture instrument. |
| **B-Man-PIT** | Yarden, manual | none | Run the reviewed instrument on the qualifying days. |
| **CP-1** | Engineering Lead, existing ceiling | milestone allocation + 6 h reserve, unchanged | A fresh Critic independently **verifies** the resulting ledger. |

The division follows the existing block-type boundary in `orchestrator-role.md`: waiting for a
scheduled external publication requires no engineering judgement, only that the date arrive, so it
belongs in a manual block. Authoring the instrument and verifying its output both require judgement,
so both stay inside the Gauntlet.

## Why CP-0 exists rather than writing the instrument unreviewed

The capture ledger is CP-1 checklist evidence. If the instrument that produces it were authored
outside any review regime, CP-1's `PASS` would rest on an uninspected instrument — the exact hole the
architecture exists to close, displaced one step earlier. CP-0 keeps the instrument inside the
Gauntlet while staying free of any calendar dependency.

CP-0 is also the first checkpoint executed under the `engineering-role.md` contract. Its Return
Packet is that contract's operational validation, on a small and genuinely needed artifact rather
than a synthetic rehearsal.

## Changes

1. **§3** — capture contract notes where each phase runs. The evidence contract itself is unchanged.
2. **§12** — new `### M0.5 — Point-in-time capture instrument` with the CP-0 checklist and the
   B-Man-PIT block definition.
3. **§12 / CP-1** — the point-in-time item becomes a verification item. CP-1 verifies the ledger,
   does not produce it, and does not wait for capture days. An incomplete ledger returns `BLOCKED`
   naming the missing qualifying days — never a weakened bar.
4. **Version markers** — M0 header and changelog record v6.5.
5. **DEC-AWS numbering** — the parked AWS cascade targeted v6.4 → v6.5; v6.5 is now taken, so that
   cascade would produce v6.6. Noted in `capstone_V6_5.md` and `aws-extension-spec_v1_1.md`.

## Owner decisions taken (2026-08-04)

- **Filename anchor — resolved.** The plan was renamed `capstone_V6_4.md` → `capstone_V6_5.md` and
  every reference updated across the repository, matching the existing convention that superseded
  plans are retrieved from Git (`97627a4:capstone_V6_4.md`).
- **CP-0 ceiling — resolved.** 2 h planning reserve. The Gauntlet reserve moves 22 h → 24 h and the
  program envelope ≈727 h → ≈729 h. The issued CP-0 brief states this as its numeric
  active-elapsed ceiling.
- **Stage map — rebuilt.** `program-stage-sequence.md` v6 → v7, adding the M0.5/CP-0 and B-Man-PIT
  rows in sequence. Every v6 stage is preserved in the same order.
- **DEC-AWS numbering.** The parked cascade now produces capstone v6.6 and map v8.

---

## Corrective addendum — verdict-staleness propagation (2026-08-04, same day)

The 2026-08-04 tooling pass replaced *rerun-everything-on-any-candidate-change* with **computed
staleness from declared `reviewed_paths`**. That change landed in `scripts/gauntlet_protocol.py`
(`_validate_reviewed_paths`, `_component_is_current`, `_validate_component_bindings`), in
`docs/track-b/schemas/critic-verdict.schema.json`, and in `engineering-role.md` §8 and the
Return-Packet criteria — but **was not propagated** to `capstone_V6_5.md` §12, to the two
`docs/track-b/gauntlet-templates.md` Integration passages, or recorded in this sheet. The plan
therefore forbade, under version precedence, the exact reuse the tool implements: at CP-1's 16
checklist items and three mandatory M1 critic surfaces, every integration commit would have forced
a full rerun of all of them. Propagated and recorded here.

**Normative rule (now stated identically in tool, schema, plan, role doc, and templates).** Every
component verdict declares a non-empty `reviewed_paths` set of safe repository-relative paths that
exist in the candidate tree at that verdict's own bound SHA. A component `PASS` taken at an earlier
candidate still binds at the final candidate **if and only if**:

1. its bound candidate is an **ancestor** of the final candidate (`merge-base` equals the bound
   SHA — a rebuilt or rebased branch fails this and is stale regardless of paths); **and**
2. `git diff --name-only <component-sha>..<final-sha> -- <reviewed_paths>` is **empty**; **and**
3. the binding's declared set exactly matches the referenced verdict record's own `reviewed_paths`.

A verdict failing any of the three is stale and exactly that component Critic reruns against the
final candidate with a new run ID/ref; a repair touching no reviewed path reruns nothing. A current
component `PASS` binds its own earlier SHA/tree — only the Integration Critic runs at the final
SHA/tree. **Soundness condition:** `reviewed_paths` must be declared honestly and broadly enough to
cover what the verdict actually depends on; understating them is the one way to make the rule
unsound, and the Integration Critic verifies each declared path exists in the candidate tree.

No scientific criterion, checklist item, invariant, or acceptance bar changes. This is an
execution-cost rule only.

## Corrective addendum — `st_nlink` (2026-08-04)

The `progress.md` session log for 2026-08-04 recorded that "same-UID hardening (`st_nlink`,
two-file run root)" was **removed**. That entry is wrong and is corrected in `progress.md`. Both
mechanisms are retained and enforced: `gauntlet_protocol.py:411` rejects hard-linked evidence reads
and `:3622` rejects hard-linked CP-2 custody files, `tests/test_cp2_blind_protocol.py:509` asserts
`st_nlink == 1`, and `capstone_V6_5.md` §12 and `capstone_V6_3-to-V6_4-amendments.md` both require
inode link count exactly one. What was actually withdrawn on 2026-08-04 was the *claim* that file
modes and hashes establish non-observation by a same-UID process: absent a real read sandbox or
allowlist, the honest isolation label is `COOPERATIVE_PROCEDURAL`, never `ENFORCED_READ_ISOLATION`.
The mechanisms stand; the over-claim about what they prove does not.
