# Capstone v21-r10 → v21-r11 — CP-24: DDNN-2, and CP-23's outcome (ratified)

**Ratified on 2026-10-05 under the Owner's delegation of 2026-10-04.** The Orchestrator drafted the
text under the Owner's task-scoped suspension. That grant also covers:

- the commit and push of this revision;
- CP-24's execution, with the steering of §23.6.

The LAND stays the Owner's, by hand.

## Decision and authority

After CP-23's closure on 2026-10-04, the Orchestrator recommended running DDNN-2 before the
data-admission research. It asked for a suspension and proposed to bring the design decisions
back for approval. The Owner wrote, in order (verbatim, times in UTC):

18:45:

> תכין תוכנית עבודה לDDNN-2 , תעביר אותה אצל סוכנים באופן עצמאי תחתיך. סוכן מחקר עצמאי ובלתי תלוי יכין לך כיוונים אפשריים, אתה תכין תכנית, תשלח אותה למבקר עצמאי שיבחן ויבדוק אותה אחר כך תשלח בעצמך לסוכן ביצוע את DDNN-2 בלי לערב אותי
>
> המטרה היא לתת לך שליטה מלאה על הביצוע תוך הבטחה למאמץ ממוקד ומקסימלי ובקרה בכל שלב ככה שתוכל לכוון ולנסות למצוא דרך בה DDNN כן תוכל לשמש אותנו.
>
> מה דעתך?
>
> לצורך זה כמובן יש לך השעיית Lockdown לסעיף עוגן חדש,  הסעיף יגדיר את DDNN-2 ואת האישור לכל הצרכים לו, וכלול בו אישור כמובן ל-commit ו-push ולכל מה שצריך.

18:47:

> הייצוג, היקף חיפוש ההיפר-פרמטרים, האנסמבל, המשקל בתוך v5 והתקרות כולם לשיקולך וניתנים לשינוי גם תוך כדי העבודה אם תצטרך

18:48:

> תמשיך באופן חופשי ומלא עד דוח ובקשת LAND

In English:

- **The route.** Prepare a work plan for DDNN-2 and pass it through agents working independently
  under the Orchestrator. An independent research agent prepares possible directions; the
  Orchestrator writes the plan; an independent critic examines it; then the Orchestrator itself
  sends DDNN-2 to an execution agent, without involving the Owner.
- **The goal.** Give the Orchestrator full control of the execution, while ensuring a focused,
  maximal effort and control at every stage. The Orchestrator can then steer and try to find a
  way in which DDNN can serve the programme.
- **The authority.** A Lockdown suspension for a new anchor section that defines DDNN-2 and the
  approval for all its needs, including commit, push and everything required.
- **The discretion.** The representation, the hyperparameter search scope, the ensemble, the
  weight in v5 and the ceilings are at the Orchestrator's discretion, and may change during the
  work if needed.
- **The instruction.** Continue freely and fully, up to the report and the LAND request.

**The Orchestrator's guardrails.** Answering "מה דעתך?", the Orchestrator committed to these
guardrails, which §23 implements:

- all search and steering on training data before the folds;
- each pre-registered attempt scored on the folds once, within a cap on attempts fixed in
  advance;
- design free until the protocol freeze;
- a plan critic that sees only the plan;
- an execution agent that sees only the brief and works in its own worktree;
- an independent Integration Critic;
- the LAND by the Owner, by hand, and no publication.

When the session was compacted and the first research run was lost, the Owner repeated the
instruction on 2026-10-04: "כנראה בגלל הקומפקט. תתחיל מחדש. תמשיך באופן חופשי ומלא עד דוח ובקשת
LAND".

**How the delegation is read:**

- **The Owner's decisions** are D1–D3 in §23.15.
- **Delegated decisions.** Every design choice the Owner did not state is D4–D12. Each is marked
  "Orchestrator, under the delegation", so that the Owner can see it and reverse it at the LAND.
- **Steering.** The words "control at every stage … so that you can steer" authorize §23.6's
  steering points. They are a CP-24-specific exception to the one-brief, one-return pattern of
  `orchestrator-role.md`, which is unchanged.

## How the plan was made

1. **Independent research.** A research agent received CP-23's facts and files, but not the
   Orchestrator's own proposal. It did not read `progress.md` or the Orchestrator's files. Its
   report is committed as
   [cp-24-research-directions-2026-10-05.md](cp-24-research-directions-2026-10-05.md). Its three
   top diagnoses:
   - stale, early-stopped training: the kept networks stopped at epochs 3–8 and never trained
     on the last 28 days;
   - per-hour rows that duplicated LightGBM's information;
   - a role that over-weighted the weakest member, with a non-robust ensemble mean.
2. **What the Orchestrator took from it:**
   - the training recipe;
   - the day-level representation;
   - the per-fold batch-rolling search and the top-four ensemble with a per-level median;
   - the guards;
   - the weight by v4's own rule;
   - the pre-fold gate;
   - a stricter level and a practical size in the rule.
3. **What the Orchestrator changed:**
   - **Representation.** One representation, day-level, instead of two families: a per-hour
     family would double the compute in a four-day window.
   - **Validation batches.** They avoid every fold's warm-up and evaluation days, so no steering
     decision can see a fold outcome. That gives B = 3, 7, 11, 11, 11 instead of eleven
     everywhere.
   - **Attempts.** At most two scored attempts instead of one, with a second only for a recorded
     design diagnosis, through the same gate. The 97.5% level splits 5% across that cap.
   - **The candidate's name.** v5, because CP-23 adopted no v5, so the name is free.
4. **Independent plan review.** A plan critic received only the plan packets and the
   repository: `3eb7bff8b96060dc4c023d52d5b21abfdcd410233c2e1025dc67df22adb85cf0`, then
   revision 2, `f1ddfb90fce0451a09f6c63197345d55a9d1ddd9d7815d2001a3dde56f3e1d22`. Its findings
   and their dispositions are in the next section.

## Plan review and dispositions

**The first review** covered the packet `3eb7bff8…` and returned READY WITH FIXES, with 2
BLOCKING, 10 MAJOR and 23 MINOR findings:

| Finding | Disposition |
|---|---|
| B1: CP-20's weather grids have no record for 2022-09-29..2023-03-24. Fold 4's gate and the fold-4 and fold-5 searches need it | Fixed: §23.6's weather-coverage rule. Pre-fold fits leave the uncovered days out, and v4's members run on fold 4's gate days through a scoped, logged wrapper. No retrieval (D11) |
| B2: "The search never reads an evaluation or warm-up outcome" was false, since later folds train on earlier folds | Fixed: the fold-by-fold invariant in §23.4, and its controls in §23.10 |
| M1: the header said three attempts | Fixed: two |
| M2: the ceilings could not cover the permitted route | Fixed differently. At most three rounds before attempt 1 and one before attempt 2; 40,000 fits and 150 machine-hours; route projections in 4.6R′; a budget check at each step |
| M3: editing `scripts/mlflow_export.py` would fail CP-23's byte-exact test | Fixed: the file is never written, and a CP-24 module imports its functions |
| M4: "A1, B2" meant two different things | Fixed: A1_w and B2_w for HG's weather components |
| M5: warm-up fits could precede the freeze | Fixed: the freeze comes before any warm-up or evaluation fit |
| M6: attempt 2 could change "the search" | Fixed: it may only widen the space, and its search reruns from scratch |
| M7: the steering states were incomplete | Fixed: rounds, freezes, stops, S2's trigger and the checklist after a stop |
| M8: a mid-run revision of §23 had no mechanics | Fixed: no revision. A ceiling may be raised only by a committed steering answer, up to stated maxima |
| M9: "exactly v4's (§17.3)" imported per-hour bans | Fixed: v4's sources in day-level form, as §21.2 permits |
| M10: the locked `orchestrator-role.md` rules set aside were not named | Fixed: named in the header and §23.6 |
| m1–m23 | Applied. m18 was met by moving the Orchestrator's files to `.local/artifacts/cp-24-orchestrator/`. The search space was also narrowed for cost, to one or two layers of 16–512 units |

**The second review** covered revision 2, `f1ddfb90…`, and returned READY WITH FIXES. Every
finding of the first review was resolved. It added three MAJOR and eleven MINOR findings, each
with exact text, and said that no further round was needed once that text was applied:

| Finding | Disposition |
|---|---|
| N1: "no warm-up or evaluation fit" contradicted the required reproductions of v4's and HG's committed vectors | Fixed: the rule binds DDNN-2 and the new policies, and reproducing committed vectors is not such a fit |
| N2: "tuned before D0_f − 56" contradicted S1's gate-informed choices | Fixed: the search uses data before D0_f − 56, and S1 uses data before D0_f |
| N3: two attempts need six bootstrap passes | Fixed: six, defined per scored attempt |
| n1–n11 | Applied: the three raisable ceilings named, the not-applicable rule completed, 4.6R′'s record and a floor of 32 trials, CP-15's statistics corrected, paired positive controls, the Lead's retained paths, the export in every outcome, the timebox raise, one list of committed documents, the third set-aside rule, and the ensemble drawn from full-batch trials |

The text was applied as given, and no third round was run.

## Identities

| Item | Identity |
|---|---|
| Incoming `main` = `origin/main` | `09eacd1` (CP-23's closure, on `land/cp-23` = `03c5b64`) |
| Previous research anchor | v21-r10 at `3f7aaf2:capstone_v21.md`, SHA-256 `6873c2501067c63692ec7cb79dfd4073164a8a014edbd6ebc23169e7e8ff6709` |
| CP-23's governing bytes | v21-r10 §21 at `evidence/cp-23`. v21-r11 neither reopens nor rescores CP-23 |
| Ratified identity | `capstone_v21.md` v21-r11, by SHA-256 in `progress.md` and in CP-24's issued brief |
| Publication anchor | PUBLISH_RULES 1.3, unchanged, SHA-256 `5a660864f8b82943174741320c71087a3d0508f707edeb997cb2c1395c1c73b4` |
| Research report | `docs/track-b/cp-24-research-directions-2026-10-05.md`, SHA-256 `224d80ebcb31a26ba5c8e307c72adec92e01dc66b48ee99af05f20000fdab714` |

**What v21-r11 adds:**

- a header;
- one CP-24 row in §10's table;
- §21.13, CP-23's outcome;
- §23, CP-24.

No existing line is deleted or altered, and `git diff` against v21-r10 shows only additions.

## Decisions

The table is §23.15's. The reasons for the delegated choices:

- **D4: train up to D−1, on day-level rows.**
  - On identical inputs CP-23's DDNN lost to LightGBM in every fold, and its fits never saw the
    last 28 days.
  - The day-level representation gives the network the previous evening's prices, which
    per-hour same-hour lags lack.
  - Both choices follow the two reference papers.
- **D5: search and ensemble.** CP-23's choice of one configuration out of four, on 28 days,
  was noise. Published practice tunes on long rolling validation and ensembles different tuned
  configurations. A per-level median stops one member's blow-up.
- **D6: one sixth, by v4's rule.** v4 weights its blocks two thirds LEAR and one third
  nonlinear, with equal weights inside each block. DDNN-2 joins the nonlinear block, so
  `c_v5 − c_v4 = (1/6)·(D2 − L)`.
  - The decision asks a clean question: does DDNN-2 improve v4's nonlinear member?
  - LEAR keeps the two thirds that carried fold 3.
  - CP-23's hindsight weight bound is disclosed, and it is not used.
- **D7: steering and attempts.** The pre-fold gate and up to three rounds before attempt 1 give
  the Orchestrator real steering on pre-fold evidence, without touching a fold. The cap of two
  scored attempts keeps one repair possible after a fold look, under a stricter level, through
  one more round and the same gate.
- **D8: the rule.** CP-23's four conditions stay, so that the decisions remain comparable. Two
  changes:
  - condition 1 moves to 97.5% for the cap;
  - a 0.5% practical size keeps a negligible gain from adopting a new model family.
- **D9: ceilings.**
  - **Estimated cost.** A pre-fold round is about 5,700 member fits at 128 trials, and a scored
    attempt about 5,100. CP-23's measured costs and the day-level row count give about 5–20
    seconds per fit. The narrowed space of one or two layers of 16–512 units keeps the slow
    tail down.
  - **The fit cap.** It is 40,000, and 150 machine-hours. The longest route allowed (three
    rounds and attempt 1, then one round and attempt 2) needs about 33,000 fits at 128 trials.
  - **The calendar** is the binding limit.

- **D11: weather coverage.** CP-20 extracted GFS only for the windows its 638 origins need, so
  delivery days 2022-09-29..2023-03-24 have no record. §15.3 forbids imputing unattempted weather,
  and CP-24 retrieves nothing, so pre-fold fits leave those days out. No warm-up or evaluation fit
  is affected: fold 4's first window starts on 2023-03-25, the first covered day.

## Disclosures

- **Known results.** The Owner and the agents know the results of CP-15 and CP-20 to CP-23 on
  these folds, CP-23's diagnosis and its hindsight bound.
- **Partly fold-motivated design.** The research agent's diagnosis read CP-23's fold-level
  tables: for example, the night-hour gap and the fold-3 examples. §23 keeps its choices at the
  level of literature-backed mechanisms and uses no fold-specific value. 4.7T carries the
  protection.
- **Selection.** CP-24 is the second DDNN decision on the same five folds. Its results stay
  `development_post_selection`, and the record carries the number of rounds and attempts.
- **What CP-24 cannot establish:**
  - performance on new data;
  - economic value;
  - daily operation;
  - in-browser retraining, which §16 and §19 decide.

## Files touched by this task

| File | Change | Authority |
|---|---|---|
| `capstone_v21.md` | v21-r11: header, a §10 row, §21.13 and §23; additions only | Suspension; commit and push delegated |
| `docs/track-b/capstone_v21-r10-to-v21-r11-amendments.md` | This record, new | Suspension; commit and push delegated |
| `docs/track-b/cp-24-research-directions-2026-10-05.md` | The research agent's report, new | The delegation |
| `docs/track-b/v3-plan-handoff-2026-09-22.md` | A dated v21-r11 note; no historical sentence removed | Suspension (consistency) |
| `progress.md` | The ratified state and CP-24's issue | Orchestrator regeneration contract |

## Documentation validation

This task checked:

- that the anchor's diff against v21-r10 contains only additions;
- that §23.13, the CP-24 bar, extracts cleanly with `scripts/bar.py` at the ratification
  commit;
- that the issued brief passes `scripts/bar.py brief`;
- that every relative link added here resolves.

This is a documentation ratification, not an implementation PASS or a research result.
