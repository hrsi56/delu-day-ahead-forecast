# Capstone v21-r17 → v21-r18 — A1's freeze and 4.7T's terms ratified

**Owner authority, 2026-10-28.** On CP-17's return the Owner wrote: "אני מאשר את כל ההמלצות שלך"
("I approve all your recommendations"). With it: "יש לך אישור מלא עם כל ההשעיות וכל מה שאתה צריך"
("you have full approval, with every suspension and everything you need"). His decisions 13–19 are
recorded in `docs/track-b/cp-17-owner-decisions-2026-10-28.md`, SHA-256
`4d049770e51a37a806c52a4ae681f70aae62ac1847a67c7c0c3109385da3ac37`. Decision 19 reads, in part:
"r18 then ratifies the terms with CP-17b's freeze identity. It is done under the Owner's suspension,
granted with these decisions, and with an independent plan review, before 2026-12-04."

**The start, 2026-10-29.** After CP-17b's LAND the Orchestrator asked whether to start r18, and the
Owner answered in the session: "Yes, start r18". `progress.md`'s session log records it.

**The scope of the suspension.** It covers four things:
- `capstone_v21.md`;
- this amendment record;
- the directly necessary consistency edits to `progress.md`;
- the commit and push of these files to `main`.

It ends at this task's terminal return. It does not authorize:
- any other governance file, `docs/PUBLISH_RULES.md` included;
- a change to any code, test, frozen record, verdict or freeze;
- publication;
- opening 4.7T or any other checkpoint.

**The base:** r17 at `61658c7:capstone_v21.md`, SHA-256
`3124451da84c3cd99fae728c371207aace6ae537474f7769d0ff6333ee53e4fc`. `main` was `f28955f5` when this
revision was drafted.

| Scope | r17 | r18 |
|---|---|---|
| The candidate | §24.9: CP-17 freezes CP-28's selection or the control | A1, frozen by CP-17 and re-frozen by CP-17b, policy identity `439115fb…` (§24.12) |
| The daily policy | §16.2's freeze list; the failure policy left to CP-17 | the success definition, the two chains, partial days, the shadows (B0's included) and the driver, as frozen (§24.12) |
| §19.3 and §19.5 | τ_eq and the reference runtime from the probe; the tolerance τ left to the Owner | τ = 10 EUR/MWh; τ_eq = 0.01 EUR/MWh, with the training window bound first and three statuses; the reference runtime as frozen (§24.12) |
| F1 | not yet observed | recorded at its largest observed figure, 0.082 EUR/MWh, as an observation and not a bound. Its public wording stays the Owner's (§24.12) |
| 4.7T's terms | §24.9's list, to be registered before 4.7T opens | CP-17's protocol `337a102d…` as revised by CP-17b's `04aac76a…`, plus the 20-machine-hour ceiling and the full scope of the Owner's declaration (§24.12) |
| PUBLISH_RULES §14's trigger | in §24.9's list | open for the Owner, before 4.7T opens (§24.12) |
| When A1 replaces v1 | §16.1 | open for the Owner, before CP-18's activation (§24.12) |
| The `schema.py` defect | — | fail-safe; accepted for the frozen policy's life (R7, §24.12) |
| 4.7T's calendar | opens no earlier than 2026-12-04 | unchanged |

**What changes in the file:**
- **A new authority notice** at the top. r17's title gains "Historical", and a separating rule is
  inserted.
- **A new §24.12** at the end.

**What does not change:**
- **Everything else below the new notice** stays byte for byte: the historical headers, §§1–23 and
  §§24.1–24.11. So CP-26's test of §§1–23 against r13 (`tests/test_cp26_repair_contract.py`) still
  holds.
- **No frozen record.** CP-17's and CP-17b's freezes, protocols, verdicts and landing records stay as
  committed. The freeze manifest's F1 text keeps CP-17's 0.028 figure, and §24.12 records the
  disclosure.
- **The checks.**
  - CP-17b's `refreeze verify` reads its governance pins from frozen copies, so this revision leaves it
    green.
  - CP-17's own `freeze verify`, run by hand on the raw tree, reports the anchor as altered, beside the
    two package files CP-17b re-froze. That is by design, and the suite runs CP-17's check on CP-17b's
    view (`tests/cp17/test_records.py`).

## How it was checked

The records are in `.local/artifacts/r18/`, which Git ignores (`/.local/`), so they are cited by hash.

| Record | SHA-256 | Result |
|---|---|---|
| The plan critic's brief, `plan-critic-brief.md` | `c63ce6cee940ec330a496dc1655cab8f50768d33e1e57aae2dcde110abc7d1d5` | — |
| The reviewed candidate, `candidate/capstone_v21.md` (first version), with its record `8d4f46c8…` | `cafe182875a1a989ebafd6e897c3959b0b842cbd91996a370d453703cbc1f9ca` | — |
| The review, `plan-critic-review.md` | `cb983c7774fe37a9fdd6db11e069ad68815fa28b47c88e4895badf8bdde068ef` | READY WITH FIXES: 0 blocking, 6 major, 12 minor. No hash, identity or figure is wrong, nothing leaks, and no CI step is at risk |
| History-free CI on the first candidate's tree (`ci-cand1.log`; `cand1-validation/ci312/results.json`) | `9c69ede5…`; `844e8cd2…` | the seven steps exit 0, with 2,427 passed and 42 skipped, the same as unamended |

The critic's check of the fixes (`plan-critic-check.md`, SHA-256
`2b04cd92a84177ce02a4346991e93b149639723415a5dd040def297fbacb57b1`) found all 18 findings
resolved, with three new MINOR wording points, N1–N3, and a verdict of READY WITH FIXES. N1–N3 were
applied as given:
- the open list names R7's exception;
- the protocol's §8 and §12 are quoted exactly;
- R7's handling rule covers the Space's `verify_bundle` too.

The CI run on the final tree is recorded in `progress.md`'s session log.

**The dispositions.** Every finding was applied, as the critic gave it, unless the row says otherwise.

| Finding | Disposition |
|---|---|
| M1, when A1 replaces v1 is ratified two ways | applied: the candidate row says "until A1 replaces it", and the question is open for the Owner before CP-18's activation (R6) |
| M2, the decisions table doesn't attribute every term | applied: rows P and F, and the notice's sentence reworded |
| M3, τ_eq loses its training-window binding | applied |
| M4, the runtime check isn't a precondition | applied: the issuing host's pinned files, the precondition for 4.7T's brief, and where CP-18's pipeline runs |
| M5, the window's payloads | applied, for 4.7T's brief |
| M6, the `schema.py` defect has no owner | applied as a decision: accepted for the frozen policy's life (R7), and the Owner may order a re-freeze before 4.7T opens |
| m1, "byte for byte" vs the title line | applied, here too |
| m2, macOS 26.5.2 | applied |
| m3, the intake rule's words | applied |
| m4, F1's source and the browser evidence | applied, with one correction. The S_13 origins differ by at most 9.4e-9 EUR/MWh across 2026-08-31 to 2026-09-06. 9.4e-13 holds at the freeze origin alone |
| m5, the visitor wording and F1's public statement | applied: both are the Owner's publication decision |
| m6, "this ratification" as an Owner decision | applied |
| m7, the map of the freeze list, and A1's state | applied |
| m8, the PUBLISH_RULES §14 ruling as a prerequisite | applied |
| m9, the checks unanchored | applied: this section |
| m10, the 4.7T table's "A1", and the comparators' failure rule | applied |
| m11, decision 6 in the table | applied |
| m12, what CP-17's raw `freeze verify` reports | applied, here too |

**What r18 did not need:**
- **No experiment, fit or download.** Every figure it states comes from CP-17's and CP-17b's committed
  records.
- **No 4.7T information.** No delivery day after 2026-09-06 exists on this machine, or was read or
  inferred. The critic counted 0 rows after 2026-09-06 in the committed data, reading dates only.
