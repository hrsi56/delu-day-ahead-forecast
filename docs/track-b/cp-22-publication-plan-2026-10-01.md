# CP-22 publication plan — revising v4 in place (PRES-4)

**Orchestrator planning document, 2026-10-01. It is not a brief and not an authority.** It plans
the block that follows CP-22's landing, under decision D5 of
[v21-r9 §20](../../capstone_v21.md) and PUBLISH_RULES 1.3 A10. The PRES-4 brief is issued only
after CP-22's terminal return and the Owner's LAND. That brief names its ceilings and every
external action the Owner authorizes.

## 1. Entry conditions

1. CP-22 returned PASS with a fresh Integration PASS, its publication packet and its draft export.
2. The Owner squash-landed it and tagged `land/cp-22` and `evidence/cp-22`, and its branch was
   reclaimed.
3. **There is a replacement under `cp22-replacement`.** If not, nothing is published until the
   Owner decides, because CP-22 stops at its return (Owner decision, 2026-10-01).

An INCOMPLETE or BLOCKED CP-22 has no result to publish.

## 2. Pinned rules

- **PUBLISH_RULES 1.3,** at the hash the PRES-4 brief records, with its incorporated sources.
- **The runbook and packet template** at their hashes on the day of issue.
- **A7, A8 and A9 are not triggered:** no live panel, no final-product designation and no Space
  product.
- **The independent check is mandatory.**

## 3. The work: a v4 revision (A10)

The packet supplies every value; no number is typed.

| Area | Work |
|---|---|
| Registry | v4's entry gains a dated revision under A10, sourced from CP-22's landing record. Its current construction is W or W+DL. The superseded revision records CP-21's HGL with its codes, runs and evidence. A revision event joins the status vocabulary, and the runbook's lists and the registry tests are updated with it. |
| Name | "v4 · LightGBM member added" (proposed in §20.6) |
| Checkpoint and evidence | CP-22's entry, MLflow children and `evidence/cp-22` with its freeze date |
| Rules | `cp22-replacement` and `cp22-dynamic-layer`, set 2026-10-01 |
| Chapter | v4's chapter shows the current revision. It keeps the superseded three-block construction visible as a dated earlier revision, with its comparator, result and limitations. |
| A3 | The v3 → v4 transition describes the current revision and states the revision. The revision step is a dated note with its difference and interval against the three-block v4. |
| Headline | It stays on v4 (the current revision), with metric names (A1). The released product stays v1. |
| MLflow | Upload `cp22`, equal to the draft apart from the landing-time fields. CP-21's published runs are unchanged. The `compare:v4` route covers the current revision. |
| Encoding | v4 keeps D6's encoding: amber `#B45309`, a filled diamond and "v4" |

**In every outcome with a replacement,** the chapter's method detail states:

- the ladder v4 → M → A-PN-sel → R, and DL's two parts;
- the replacement finding, with its rule;
- whether the replacement shows a joint improvement over v4;
- the DL finding;
- the peak finding.

None is hidden, whichever way it falls.

## 4. Every surface (runbook §1a; packet §8)

| Surface | Work | Evidence before completion |
|---|---|---|
| GitHub source / README | The landing and publication commits, pushed on the Owner's instruction. The README's generation list shows v4's revision. | The landing SHA, the pushed revision and the served README bytes |
| GitHub Pages | Rebuilt and deployed, with the revised v4 chapter | The served hash equals the reviewed `docs/index.html`, plus the A6 public browser checks |
| Public MLflow | An authorized upload of `cp22`, then the mirror verification, the routes and the index, before the final build | The export identity and its record-level diff, the run IDs, and anonymous REST and browser checks |
| HF Space card and demo | The card's model line may change; the demo stays v1. Deploy only if the bundle changes, deleting files the bundle does not carry. | The Hub revision, the card bytes and the demo checks, or a verified-unchanged identity |

## 5. Sequence and authority

Follow PUBLISH_RULES §11:

1. build from the packet;
2. editorial review;
3. fresh reader;
4. independent check;
5. authorized MLflow upload;
6. final build;
7. focused recheck;
8. LAND, push and Space, each on the Owner's named instruction;
9. A6 public checks;
10. the packet §8 receipt and a closure record.

Give the Owner only non-interactive Git commands.

## 6. Rough effort (an estimate, not a ceiling)

About 12–20 active hours. Most of the work is the revision mechanism, which is new (A10): the
registry, the status vocabulary, the chapter's revision view and the tests. The PRES-4 brief sets
the actual timebox.

## 7. Out of scope

- research reruns or new scores;
- any change to the released product or the demo's model;
- A7, A8 or A9 work;
- regrading PRES-1, PRES-2 or PRES-3;
- template or anchor edits.
