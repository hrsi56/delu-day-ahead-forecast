# v21-r12 → v21-r13 and PUBLISH_RULES 1.4 → 1.5 — the programme after CP-24

Owner-authorized and ratified on 2026-10-12.

## Authority and scope

On 2026-10-12, after reading the final draft, the Owner wrote:

> תוסיף A6 A3 בלי כיווץ: משקל גלובלי נלמד, שיכול להגיע לכל ערך; A7 A5 בלי כיווץ: המטא־לומד, עם
> הפלט שלו כפי שהוא

> מאשר השעיית Lockdown ל־v21-r13 ול־PUBLISH_RULES 1.5, מאשר את הטקסט של plan-for-critic-r4.md עם
> התוספת של a6 a7 מראש, ומאשר commit ו־push לכל מה שצריך.

**In English:** "Add A6, A3 without shrinkage: a learned global weight that can reach any value; and
A7, A5 without shrinkage: the meta-learner, with its output as it is." Then: "I approve a Lockdown
suspension for v21-r13 and PUBLISH_RULES 1.5, approve the text of plan-for-critic-r4.md with the
addition of A6 and A7 up front, and approve commit and push for everything needed."

**What the grant covers.** It is a task-scoped Lockdown suspension for:

- research v21-r13 and PUBLISH_RULES 1.5;
- this record;
- the exposure ledger, `docs/track-b/exposure-ledger.md`, which v21-r13 §24.2 creates;
- directly necessary consistency edits to the programme plan and `progress.md`.

It includes their commit and push, and it ends at this task's terminal return. It authorizes no
checkpoint: CP-25, CP-26 and CP-28 each need their own brief and grant (§24.10).

## Result

**Research v21-r13** (`capstone_v21.md`), as additions only:

- a header, prepended;
- three rows in §10: CP-25, CP-26 and CP-28;
- §24, appended: the programme after CP-24.

§§1–23 and every earlier header keep their bytes. §24.1 lists each earlier rule that §24 replaces
for future work.

**PUBLISH_RULES 1.5:**

- the first line and a revision-authority paragraph;
- §1.3's "Revision 1.5 / A12" bullet;
- **§10.5:** the independent post-deployment check, required only when a served surface differs from
  what the binding independent review covered, or a public check fails without a passing retry;
- **§12, invariant 10:** the date boundary moves from 2026-04-07 to 2026-09-06;
- §13's "Public check" row;
- §15's lead-in, and A12;
- §16.5;
- §17's change-record entries for 1.4, which was missing, and for 1.5.

## The decisions

| # | Decision | Date and source |
|---|---|---|
| D1 | The short path: no new data sources; CP-27 dropped; CP-28 on stored forecasts, confirmed after CP-26 | 2026-10-12; programme plan, top |
| D2 | The issue time, D−1 11:00 Europe/Berlin, strictly before | 2026-10-12; programme plan, stage 4 |
| D3 | The vintage standard: three tiers | 2026-10-12; programme plan, stage 4 |
| D4 | 4.7T on 2026-09-07 to 2026-12-05; 2026-04-08 to 2026-09-06 joins development; the replay withdrawn | 2026-10-12; programme plan, top |
| D5 | CP-28's arms A1–A5, with A6 and A7 added at ratification | 2026-10-12; programme plan, stage 4; the words above |
| D6 | Several sources admissible with a union arm: moot under D1 | 2026-10-12 |
| D7 | The conditional independent post-deployment check | 2026-10-11, at PRES-4's closure |

§24.11 marks every other design choice and who made it.

## The finding behind D4

While drafting, the Orchestrator found three facts:

- `data/snapshot.parquet` holds 3,648 hourly rows after 2026-04-07, to 2026-09-06;
- `data/partitions.json` marks v1's final calibration (2026-04-09 to 2026-06-07) and its holdout
  (2026-06-09 to 2026-09-06);
- `docs/cp2-model-report.md` §4 publishes the holdout's result.

The fixed 4.7T window (2026-04-08 to 2026-07-06) and most of the replay window therefore fell on
exposed data. The first plan critic confirmed that no committed file holds a row after 2026-09-06.

## How the text was reviewed

Every draft, review and brief is kept in `.local/artifacts/v21-r13/`. That folder is ignored by Git
and is not an off-device backup.

| File | SHA-256 | What it is |
|---|---|---|
| `plan-for-critic.md` | `a8b340a07bd47c356a8e1319d5dd86da3d2cdd937545ce4a8fbffa548efde160` | Revision 1 |
| `plan-critic-brief.md` | `df2d147e82b7f6184fca89a9e50ee8d113ba771634020927bc627a73f08b4b6b` | The first critic brief |
| `plan-critic-review.md` | `86c537cc9d2618348f7bc489df2a112200dcb1001fbec983390576d3dda2732c` | First review: NOT READY, with 3 BLOCKING, 11 MAJOR and 13 MINOR findings |
| `plan-for-critic-r2.md` | `0fe0550b4d5b7b0018a43ef66d87815e6704e6624759e5b7f075e7b0ab41a9a7` | Revision 2 |
| `plan-critic-brief-r2.md` | `a4be1bbd41127703af3ce1cd90afcfa67cca9f377159faecdcc233aa7320eee6` | The re-review brief |
| `plan-critic-review-r2.md` | `dc24b9eeebd02d862151662d1d745c7f714d1802e7a60eef775f517f4cb9ebfc` | Second review: READY WITH FIXES, 24 resolved and 3 partly, new findings N1–N3 MAJOR and N4–N14 MINOR; with the appended check of revision 3: READY WITH FIXES, R1–R6 |
| `plan-for-critic-r3.md` | `48b44de9ab9c90fc72966f6a697845bdcf7becee186adad8af909c612b92bdf2` | Revision 3 |
| `plan-critic-check-r3.md` | `d7ee446a6d9fc3c4748c553905ff8249560b6c4ae3675e14f5615aff7d87e953` | The check brief |
| `plan-for-critic-r4.md` | `b93f4d2a5943c305f1a8782cc397843966af08450ed8e4e1b90b8c9a14a7e6cd` | Revision 4, the text put to the Owner |
| `plan-for-critic-r5.md` | `32e2d18951511e89809bbbfa8a0a1b341e5fc6b84a4e2ef6d697133f7c5b8f42` | Revision 5: revision 4 plus A6 and A7, the ratified text |

The critic's three blocking findings were:

- **B1:** the control's own inputs may be tier 3;
- **B2:** CP-28's arms averaged quantiles that one member lacks;
- **B3:** v1-R would carry hindsight regime flags.

They are resolved in §§24.5, 24.8 and 24.7. Each revision's Part G maps every finding to its
change.

**Disclosures:**

- In the first review, one `grep` included `progress.md` in its file list. Its output was discarded
  unseen.
- The stage 4 research agent's excerpt from after 2026-04-07 is entry 4 of the exposure ledger.

## Prior and new identities

| File | Prior | New |
|---|---|---|
| `capstone_v21.md` | v21-r12 at `7ff6a50`, `caf03d705a785369972b6e9ef3d043815a4a7ba77830cabb51e939c486477ce4` | v21-r13, `173799d818387b9d82db16b9ccd7195afaebbea8e11259809e4a8b704bd525a8` |
| `docs/PUBLISH_RULES.md` | 1.4 at `7ff6a50`, `ccfe6199535dc104250ee1ed1d8ff57bf0b12fbfb4945a3521e2e29fad479a80` | 1.5, `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e` |

Historical briefs, verdicts, packets and closure records keep their bytes and their pinned
hashes.

## Validation

- `git diff` of `capstone_v21.md` adds lines only.
- The full test suite, `scripts/publication_guard.py tree`, and the value-based secret scan run
  before the push. Their results are in the Session Log entry of this task in `progress.md`.

## Files changed

- `capstone_v21.md`: v21-r13.
- `docs/PUBLISH_RULES.md`: revision 1.5.
- `docs/track-b/capstone_v21-r12-to-v21-r13-amendments.md`: this record.
- `docs/track-b/exposure-ledger.md`: the exposure ledger, seeded with entries 1–4.
- `docs/track-b/programme-plan-2026-10-11.md`: consistency edits (stage 4 ratified; CP-28's seven
  arms).
- `progress.md`: the new anchor hashes, Current Position and the Session Log.
