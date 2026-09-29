# Capstone v21-r5 → v21-r6 — CP-21: three-block LightGBM on top of v3 (ratified)

**Ratified by the Owner on 2026-09-29, with two changes. CP-21 execution was authorized the same
day.**

## Decision and authority

On 2026-09-29 the Owner chose CP-21:

> לצורך שימוש בv3 והוספה עליו של פיצול LightGBM לשלושה בלוקים ואימון מחדש, נוסיף את התוצאות
> לאתר להשוואה בכל מקרה, אם היא תצליח ותשפר זה יהיה המודל איתו נמשיך לעבר ההרחבות הבאות,
> נקרא לו V4. אם לא אז נתעד ונפרסם את הממצאים ואולי נקרא לזה רק ניסוי ו״גרסא שלא התקבלה״.

In English: take v3, add a LightGBM split into three hour blocks on top of it, and retrain.
Publish the results on the site for comparison in either outcome. If it improves on v3 under a
rule fixed in advance, it becomes v4 and the base for the next extensions. If not, it is
documented and published as a not-adopted experiment.

**What the choice resolves.** It answers the open question of 2026-09-24 (which extension opens
CP-21). It supersedes that date's recommended order: 4.6 first, then 4.4V, then 4.8, with 4.5
only as an extra arm of 4.8.

**Ratification.** The Owner reviewed the Orchestrator's draft and replied: "מאשר את v21-r6 עם
שני שינויים, ומאשר ביצוע CP-21" (I ratify v21-r6 with two changes, and I authorize CP-21's
execution). The two changes:

- **D1:** add the pooled attribution arm L-P, to test whether the block split itself helps.
- **D2:** add a fourth adoption condition, a per-fold veto.

The Owner accepted D3–D6 as recommended, with D4's ceilings recomputed for L-P.

**Authority.** The Owner granted a task-scoped Lockdown suspension covering three things:

- `capstone_v21.md` revision v21-r6, §17;
- this record;
- directly necessary consistency edits to `docs/track-b/v3-plan-handoff-2026-09-22.md`.

The Owner also instructed this task to commit and push five documents: the anchor, this record,
the publication plan, the programme handoff and `progress.md`. That was a task-scoped
instruction, not a standing exception. The suspension ends at this task's terminal return.

**The Lead's authority** is only §17.11's grant: CP-21 execution, local `gauntlet/cp-21` commits
and packaging of the issued brief.

## Identities

| Item | Identity |
|---|---|
| Incoming `main` = `origin/main` | `05587acdcf0536196678b444a4806c7f05c47cb5` (PRES-2 closure) |
| Previous research authority | v21-r5 at `81ab3be:capstone_v21.md`, SHA-256 `a4e178c30c555cc91dfbe338bbcf3e8776d67709d6dc4a72bc4f5892971003c9` |
| Ratified anchor | `capstone_v21.md` v21-r6, SHA-256 `ee402c4703d176f8181ed82966c978ad84c3c73a0cdb1d3567871f58bc867344` |
| Publication anchor for CP-21's packet | PUBLISH_RULES 1.1, SHA-256 `91eea445434718a163f03bcfd82e1db275a9d98311e76eb6cd1365f3707584f3` |
| Issued brief | Canonical copy `.local/artifacts/cp-21/issued-brief.md`, packaged by the Lead as `docs/track-b/evidence/cp-21/issued-brief.md`. Its SHA-256 is recorded in `progress.md`, because the brief cites this record's hash. |
| Earlier revisions | v21-r4 at `evidence/pres-2:capstone_v21.md`, v21-r3 at `evidence/cp-16`, v21-r1 at `evidence/cp-15` |

**What v21-r6 adds:** a revision header, one CP-21 row in §10's table and a new §17. It deletes
and alters no existing line; `git diff` against v21-r5 shows only additions.

**What stays as it was.** CP-20 stays judged under r4, and PRES-2 under PUBLISH_RULES 1.0. §16
remains the final-product authority. CP-17–CP-19 stay reserved.

## Ratified decisions

| # | Question | Ratified outcome |
|---|---|---|
| D1 | The adoption candidate | HGL is the sole candidate: `(1/3)·A1_w + (1/3)·B2_w + (1/6)·L-N + (1/6)·L-R`, with HG's H layer re-estimated on its own errors. L-R and L-N (block, raw and normalized) are attribution arms. **Owner change:** a pooled attribution arm, L-P, is added: one LightGBM for all 24 hours, raw target, HG's exact information with weather, and the H layer on its own errors. It is not adoption-eligible. |
| D2 | The adoption rule | Joint improvement over HG, all six §8 diagnostics, and a complete, valid evaluation. **Owner change:** a fourth condition, no resolved per-fold degradation. |
| D3 | Daily-retrain cost | A mandatory diagnostic, not a selection criterion |
| D4 | Ceilings | As recommended, recomputed for L-P (below) |
| D5 | Publication routing | A separate publication block (PRES-3) after the Owner's LAND, in either outcome, pinned to PUBLISH_RULES 1.1 |
| D6 | v4's encoding, used only if v4 is adopted | Amber `#B45309`, a filled diamond marker and the direct label "v4" (PRES-1 W16(b)) |

**The ladder L-P creates.** Each step adds one thing:

| Step | What it adds |
|---|---|
| B3 → L-P | Weather, bundled with training-only capacity selection, because B3 is a saved fixed-hyperparameter reference |
| L-P → L-R | The block split, a controlled step |
| L-R → HGL | The blend into v3 |

The block-split claim is no longer withheld. It is reported from L-R − L-P according to its
result: observed joint improvement, observed joint worsening, or no demonstrated joint
preference.

**Final ceilings (§17.8):**

| Item | Ceiling |
|---|---|
| Policies | 4 new and 7 saved: 11 scored, 1 adoption candidate |
| LightGBM fits | 24,000 main (nominal 638 × 7 models × 5 = 22,330); 35,000 in total |
| HG components | 1,600 component-day attempts; 192,000 Lasso attempts |
| Replay | 10,500 new policy-days (4 passes of 2,552) |
| Passes | 3 reference passes; 3 bootstrap passes |
| Compute | 60 aggregate machine-hours; at most 4 concurrent threads; BLAS 1 |
| Memory and disk | 10 GiB RSS; 20 GiB added disk |
| Data, network and cost | 0 bytes downloaded; 0 remote writes; $0 |
| Timebox | About 32 active hours; hard ceiling 40 |
| Calendar | No work from Friday 00:00 to Sunday 00:00, Asia/Jerusalem |

**Alternatives considered in the draft:**

- **D1:** equal quarters; two candidates tested in fixed sequence; per-block weights chosen on
  pre-fold days.
- **Excluded throughout:** a per-block residual correction of HG. It would need a nested
  full-history HG replay, and in-sample residuals are forbidden by §3.
- **D2:** a looser point-only rule.
- **D3:** a 60-minute daily-cycle guardrail.
- **D5:** publication as a phase of CP-21.
- **D6:** orange `#C2410C`, or deferring the decision.

## The pre-registered adoption rule (final)

The rule is `cp21-adoption`, set on 2026-09-29. HGL becomes v4 if and only if all four
conditions hold:

1. **Joint improvement.** On the paired HGL − HG differences, the upper 95% endpoint of ΔS_WIS
   is < 0 and the upper 95% endpoint of ΔS_MAE is ≤ 0.
2. **No regression.** HGL meets all six original §8 diagnostics, as HG does.
3. **A complete, valid evaluation.** Engineering PASS with a binding Integration verdict, and all
   10,747 keys issued.
4. **No resolved per-fold degradation.** No fold may have a 95% interval for the paired
   daily-loss difference HGL − HG that lies entirely above zero, in either MAE or WIS.

**Otherwise,** CP-21 is the branch "Three-block LightGBM on v3", marked "Not adopted". Its reason
is the first unmet condition, with its values.

- **Attribution arms.** L-P, L-R and L-N are never adoption-eligible.
- **No valid evaluation.** An INCOMPLETE or BLOCKED return yields no adoption decision and no
  result to publish.
- **What adoption changes.** Adoption changes the research headline only. v1 stays the released
  product and demo.
- **If v4 is adopted:**
  - 4.7T carries both v3 and v4;
  - at landing the Owner updates the standing decision "same information, same opponent", which
    names HG, so that later extensions face v4.

## Disclosures

- **Seen results.** The Orchestrator and the Owner know CP-15's and CP-20's development results
  on these folds, including CP-15's combination diagnostics. For example, the static convex
  oracle scored 0.63544 against the A1+B2 blend's 0.64466; see programme §5.2. The one-third
  weight is fixed by family count, not fitted to those results.
- **Selection.** CP-21 is one more decision on the same five folds. Its results stay
  `development_post_selection`, and 4.7T carries the protection.
- **What CP-21 cannot establish:**
  - which individual weather feature helps;
  - the effect of weather alone, since B3 → L-P also changes capacity selection;
  - performance on unseen data;
  - economic value;
  - daily operation.

## Files touched by this task

| File | Change | Authority |
|---|---|---|
| `capstone_v21.md` | v21-r6: ratified header, a CP-21 row in §10 and new §17; additions only | Suspension; commit and push instructed |
| `docs/track-b/capstone_v21-r5-to-v21-r6-amendments.md` | This record, new | Suspension; commit and push instructed |
| `docs/track-b/v3-plan-handoff-2026-09-22.md` | Dated consistency notes on 4.5; no historical sentence removed | Suspension; commit and push instructed |
| `docs/track-b/cp-21-publication-plan-2026-09-29.md` | Publication plan for both outcomes, new; not locked | Orchestrator planning; commit and push instructed |
| `progress.md` | Full regeneration at the Owner's request, then the ratification update | Orchestrator regeneration contract; commit and push instructed |
| `.local/artifacts/cp-21/issued-brief.md` | Canonical copy of the issued brief; ignored by Git | Orchestrator brief issuance |

## Documentation validation

This task checked:

- that the anchor's diff against v21-r5 contains only additions;
- that no `[D#]` marker or draft status remains in §17;
- that every relative link added here resolves;
- the SHA-256 identities against the repository;
- that no locked file outside the named scope changed.

This is a documentation ratification, not an implementation PASS or a research result.
