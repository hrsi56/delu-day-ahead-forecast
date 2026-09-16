# Recovery of omitted programme context — 2026-09-15

## Finding

The owner’s concern is confirmed. A standing decision explicitly limiting the data to
2019-01-01 onward was removed from `progress.md` by commit `8d56942`. Its explanation
remained in Q&A entry 2 and in the historical project material. The Orchestrator’s CP-15
receipt missed that explanation and wrongly recommended investigating earlier inputs.
That recommendation is withdrawn.

This report restores operational context. It is not a capstone amendment, new brief,
engineering audit, or authority to change the target, inputs, windows or evaluation folds.

## Exact history

| Record | What it establishes |
|---|---|
| `7aaa02bfd3129e4a3517b8e6947b67ecd62bc0e9` — 2026-09-08 | First committed Q&A document already includes entry 2 explaining the deliberate 2019 start and the DE-LU/DE-AT-LU market distinction. Its nonempty paragraph text is identical in the current document. |
| `4ec9fab6de794418de4edf673661e472242a72a4` — 2026-09-08 | Adds the explicit 2019 boundary to Standing Scope Decisions in `progress.md`. |
| `2517e55a9f58a87559878034e87467ca4d62fecd` — 2026-09-15 | Last progress version immediately before the handover rewrite still carries the boundary at line 106. |
| `8d569428fc905226f1944f9e8a9a44dd89324535` — 2026-09-15 | Rewrites progress and deletes the boundary, both vintage-assumption bullets, and other context. Its commit message says “Kept every load-bearing fact”; the deletion contradicts that claim. |
| `24da4bd`, `3618658` and the later local progress edits | Subsequent pointer/CP-10 handoff changes did not restore the boundary before CP-15. |
| CP-15 candidate `f8d0ed2a5f0737f0d088c3474b5a9fe77a406f37` and evidence tip `193d9cf48c586b9c4b1f43d7a5677b2d5f400832` | The received packet exposes the incompatibility between the fixed long window and the preserved archive start. Its Integration FAIL and all unassessed product criteria remain unchanged. |

Exact deleted text, still present at `2517e55:progress.md:106`:

> **The data window starts 2019-01-01 and not earlier.** DE-LU split from DE-AT-LU on **2018-10-01**; pre-split prices are a different market product, not more of the same series.

The Git author metadata does not establish which agent composed every sentence. Attribution
here is to the verified commit and its text. The current Orchestrator separately owns its
failure to consult the surviving explanation before recommending a remedy.

## Consequence for CP-15

The preserved archive start is a design decision, not an accidental short pull. The received
preflight says fold 1’s first 728-day window starts 2018-07-04, before the market split.
Even adding only post-split 2018 observations would not supply that entire window. Genuine
warm-up requires earlier support still.

Thus the task is to reconcile the plan with the established data/target contract. It is not
to assume older values can be fetched as the same target. No shorter window, fold omission,
different market, amended warm-up or replacement candidate set is selected by this recovery.
The Engineer correctly reported the unmet prerequisite rather than silently changing it.
The unperformed Chronos-2 and structural-input deliverables remain separately incomplete.

`capstone_v21.md` §5 still says:

> Use precisely 728 or 84 preceding calendar days; filter by inherited admissibility.

It also requires reporting insufficient prehistory rather than silently shortening windows
or dropping a fold. The locked plan is unchanged. Any actual amendment requires the Owner’s
specific task-scoped Lockdown suspension; the instruction to restore progress does not grant it.
CP-15 and CP-10 disposition decisions remain open; no branch was tagged or reclaimed.

## All 25 pre-rewrite standing decisions: disposition

Source for every row: `2517e55:progress.md`, Standing Scope Decisions. “Restored” means
operational context was returned to current progress; it does not create fresh governance.

| # | Earlier decision | Recovery disposition |
|---|---|---|
| 1 | A65/A01 pre-gate availability is assumed, not measured | Restored explicitly, with its evidence limit. A post-gate observation is not pre-gate proof. |
| 2 | A75 archive revisions are a second disclosed assumption | Restored explicitly for the historical trailing proxy; not a waiver of v21 causality. |
| 3 | Track A optional | Superseded by the owner’s later cancellation/out-of-scope decision; not reinstated. |
| 4 | Results reported, never gated | Preserve honest negative engineering results; do not restore the blanket wording over v21 §8’s separate product criteria. |
| 5 | Shipped v1 model is the holdout-evaluated model | Preserved and made explicit with no retrain and four distinct cutoffs. Future update-policy architecture remains v21’s. |
| 6 | Whole-delivery-day availability boundary | Already present; restored the reason row-wise lag availability is insufficient. |
| 7 | A correct rule can describe the wrong forecast shape | Restored as a planning lesson, not permission to repeat the Engineer’s review. |
| 8 | Constrain semantics, not SQL syntax | Restored as the associated lesson; no new engineering prescription. |
| 9 | Data starts in 2019 because the prior market differs | Restored prominently; this is the immediate lost decision behind the CP-15 conflict. |
| 10 | SMARD fallback-primary is already authorized; reconciliation still costs a second source | Restored with the completed CP-1 reconciliation history. No new-source permission inferred. |
| 11 | Governance Lockdown | Retained in canonical AGENTS.md and current progress; not duplicated or amended. |
| 12 | Orchestrator-only interview capture; owner owns presentation | Already restored before this investigation. Q&A entry 2 was never lost. |
| 13 | AMD-G5 negative control knowingly waived | Restored as a closed historical decision, without waiving present CP-15 controls. |
| 14 | No scheduled work Friday or Shabbat | Restored as the owner’s standing preference. No later withdrawal was found in the reviewed record. |
| 15 | Do not use the free scheduler for a hard deadline | Restored as a historical operational lesson; no claim of a fresh provider verification. |
| 16 | External-source degradation is outside our control | Restored with the fallback lesson. The old outage remains closed. |
| 17 | Execution-contract reviews unscoped by default | Historical governance context retained here, not promoted over the current role’s closed packet-check boundary. Canonical contracts govern a future Owner-requested governance review. |
| 18 | Authority restrictions describe scope, not inability; D-CP0-20 | Preserved by the canonical governance/closed ledger references already in progress. No closed defect is reopened. |
| 19 | Fresh independent Critic, two SHAs, evidence delta and branch accountability | Already retained in current contracts and CP-15 receipt. |
| 20 | A69 excluded; lagged actuals through D-2 allowed | Already retained; restored the distinct A65/A75 assumption context around it. |
| 21 | DE-LU, ENTSO-E/SMARD, licensing; no gas/weather | Market and licensing remain; “no gas/weather” is not reinstated as a blanket rule over the bounded feasibility scope of v21. |
| 22 | Single LightGBM; no neural challenger or live system | Historical v1 scope, intentionally superseded by v21’s named model comparison and prospective direction. Not restored as current restrictions. |
| 23 | Orchestrator decides scope; Lead decides execution | Retained in canonical roles; owner carries one brief and one return. No executor was launched. |
| 24 | Owner-only publication and mainline history | Already retained and unchanged. |
| 25 | Declared parallel branches; unknown refs escalated | Already retained. No historical cleanup is inferred from this audit. |

## Additional recovered context

- **Hourly-target continuity.** The earlier “Hourly target end-to-end” progress bullet was
  removed at `888f7de7672e36d58ed0a32a7a3848699a3c9a1d` (2026-08-02), before the September
  rewrite. The historical v6.8 contract and spike memo retain quarter-hour-to-hour aggregation,
  complete bins, chunk boundaries and DST identity. Restored a concise pointer and meaning.
- **Crisis-fold interpretation.** `880e541` added the corrected explanation; `8d56942` removed
  the detailed progress record. `2517e55` records that training included 5,784 crisis hours
  through 2022-04-29, with 61.3% of evaluation above the training 99th percentile and 2.45%
  above its maximum. Restored as historical reported evidence, not a recomputation. “Only
  trained on pre-crisis data” must not return as an explanation.
- **Which features actually shipped.** The old CP-2 receipt records the losing residual-load
  proxy (base 13.0158 versus augmented 13.0642, +0.3715%), the 19.49% strict-gate information
  cost, no post-holdout retrain, and semantic fingerprinting because pickle bytes were unstable.
  Restored the key distinctions without imposing the old winner on CP-15.
- **Two negative-hour counts.** The old notes and Q&A entry 15 distinguish the snapshot’s
  576 hourly means from the regulator’s 573 figure in 2025. Restored the distinction without
  changing either historical number or making a new aggregation claim.
- **Retired machinery.** The old notes explicitly close the point-in-time ledger,
  publication-metadata substitution and four-catalog system. Restored their historical status;
  the old forward-confirmatory design does not override v21’s new prospective requirements.

## What was intentionally not restored as current state

Completed checkpoint narration remains at its evidence tags. Resolved outages, old token
diagnostics, the old account blocker, an obsolete v6.7 Project Knowledge swap, old draft
ratification questions and prior phase launches do not become new open tasks. Track A/C,
career/runway planning and superseded model restrictions remain outside the current scope.
Historical independent pre-landing-audit language does not override the current Orchestrator
rule against redoing engineering. No old task-scoped governance suspension is revived.

## Scope and reproducibility of this investigation

Inspected the latest 18 commit summaries and searched the 84 `progress.md` revisions listed
by `git log --all -- progress.md` for the market/date boundary. Traced relevant first-parent
additions/removals, reviewed the immediate pre/post-rewrite versions, and classified all 25
pre-rewrite Standing Scope Decisions. Also inspected relevant setup, notes and receipt text,
the surviving Q&A, and historical documentary cross-references. This is not a claim to have
audited every sentence in all 84 versions, nor an independent audit of engineering results.

Useful read-only reproduction commands:

```sh
git log --all --oneline -G 'data window starts|pre-split prices|2018-10-01' -- progress.md
git show 4ec9fab -- progress.md
git show 2517e55:progress.md
git show 8d56942 -- progress.md
git show 888f7de -- progress.md
```

No model fits, source/API research, credentials, tests of the engineering pipeline, ref
mutations or publication occurred. Original audit inputs and receipt-only review outputs
are preserved locally under `/tmp/pjm-context-recovery-review/`.
