# Transfer prompt — bounded v2/v3 plan rewrite

**READY FOR TRANSFER — document rewriting only.** The independent review passed its numerical verification gate and returned **TARGETED REVISION REQUIRED**. This prompt authorizes a proposed-plan rewrite, not programme execution, model promotion, governance amendment or publication.

Copy the prompt below into a fresh session. Do not launch an agent from the review session.

---

You are an Owner-directed **bounded document rewriter** in:

`/Users/djourno/Downloads/PJM`

Your task is to revise the proposed programme plan so that its delivery routes, dependencies, evidence claims and execution prerequisites are clear. You are not an Engineering Lead running a checkpoint and not an Orchestrator changing programme state. You must finish the document work and its handoff, then stop.

## Authority and containment

Read `AGENTS.md` in full and establish this role before mutation. The Owner authorizes rewriting **only this durable file**:

`docs/track-b/v3-plan-handoff-2026-09-22.md`

It is a proposed handoff plan, not a ratified anchor. No Lockdown suspension is assumed or granted for anything else. If a locked-file change is necessary, identify the exact file/text and why in your return; do not make it. You can complete the proposed-plan revision while leaving the corresponding programme action blocked.

Read relevant evidence and primary sources without external cost. Preserve all existing dirty work outside the authorized target. Preserve a byte-for-byte before copy of the target and any scratch/full-diff files inside project-local `.local/`; do not use sibling directories or system temporary locations. If the current plan differs from the independent review's input hash, inspect and report the changes and retain compatible Owner work; do not overwrite it with a historical copy. If scope conflicts cannot be resolved from the current instructions, surface the conflict instead of silently reverting work.

Do not modify the review, this transfer prompt, the earlier review, `progress.md`, Q&A, source, tests, evidence, datasets, forecasts, models, anchors, governance or agent configuration. Do not execute work items, fit candidates, run controller/combiner searches, consume reserved outcome partitions, download bulk archives, create branches/worktrees/tags, launch other agents, stage, commit or publish. No messages to other people or external paid services. Presentation content only: no rendering, layout work or visual QA. No Q&A edits; name any capture trigger in the terminal return.

## Required reading

All paths are relative to the project root unless an absolute path is given.

1. `AGENTS.md` — complete role, containment, governance and Git authority.
2. `docs/track-b/v3-plan-handoff-2026-09-22.md` — the current target, in full.
3. `docs/track-b/v3-plan-independent-review-2026-09-22.md` — the independent critique, in full; address **IR-01 through IR-08**.
4. `docs/track-b/plan-review-2026-09-22.md` — earlier review, as historical evidence/claims, not authority.
5. `capstone_v21.md` — §§2–3 and §§6–10, especially the unchanged §8 failed bar, registry/freeze requirements and stage authority. Read-only.
6. `reports/cp15/protocol.json`, `reports/cp15/scoring_metadata.json`, `reports/cp15/selection.json` — definitions, status and population contract.
7. `data/partitions.json` — date/partition metadata only; do not open reserved outcomes.
8. `reports/cp2/a69_benchmark.json` — A69 arm/feature/grid and post-gate limitations.
9. `docs/track-b/cp-15-landing.md` — current retrieval and preserved status; historical publication authorization there does not authorize this task.

If a factual contradiction requires source inspection, use the exact primary-source links in the independent review. For architecture details, permitted targeted reads are `src/cp15/models.py` and `src/cp15/data.py`; do not edit them or train anything. The review's `.local/independent-review-2026-09-22/` recovery packet is optional, not required evidence: essential methods/results are in the durable critique. Do not make missing scratch a blocker to document work.

Reviewed target SHA256 was `290107db5abdd0623c519bfe1c745bec75a51980cd3f3b8b707d0e69458fee72`. Verify actual current bytes before relying on that identity.

## Intended outcome and structure

Keep one programme plan, not a competing plan derived from the critique. Retain useful existing text and choose concise wording; cosmetic edits are not an objective. The reader should be able to determine the next deliverable, its authority, what blocks it, and how it can finish even if no model qualifies.

Use a structure with these functions; headings and presentation are your choice:

- Present status, scope and three distinct outcomes: existing-evidence research package, evaluated causal candidate, qualified live product.
- Next recommended bounded packet, with unresolved Owner choice clearly separate from the recommendation. A local existing-evidence package and a decision/brief packet for one existing-input v2 test need not await weather admission. This is a recommended sequence, not an Owner decision to execute it.
- An Owner decision register that identifies which work each unresolved decision blocks.
- A dependency/work register that distinguishes a ready-to-authorize bounded packet from conditional future engineering. Preserve existing work IDs or provide an explicit mapping so no scheduled work disappears accidentally.
- Minimal causal, resource, archive and release contracts needed to write future briefs. Do not pretend that required fields already have chosen values.
- A compact evidence ledger with metric/population/variant/status and links to methods. Preserve consequential facts and historical failure disclosures; move detailed reasoning behind references rather than silently deleting it.
- Local artifact and Owner publication handoff boundaries, including negative-result closure and explicit deferred-work disposition.

## Prioritized changes and finding dispositions

Address every material finding, including low-severity IR-08. These are required outcomes, not instructions to accept unsupported claims.

**IR-01 — Repair delivery dependencies.** Remove universal weather-admission gating from the existing-input v2 amendment/brief path. Make it apply only to weather scope in prose and tables. Make an Owner-approved existing-evidence research route finish without new v2 results or prospective qualification. Candidate evaluation finishes on validated positive/negative/blocked results; qualification and public release remain separate. Local handoff can finish while Owner publication waits. Do not imply a research route is already ratified or change the anchor to create one.

**IR-02 — Expose finite budgets and missing prerequisites.** Give the first packet a concrete deliverable, accountable role, dependencies, finish/stop condition, effort range and local output destination. For future conditional items, identify which numeric candidate/configuration/seed/ensemble/feature-search/refit/compute caps and artifact paths their authorized brief must supply. Count controls, warm-up and failed admissions. An effort estimate is not a hard cap. Do not invent Owner resource limits: label any undetermined limit as a blocker to that item, and require its resolution before fitting. Show Owner latency, archive transfer and prospective operational effort separately. Correct total-path accounting if dependencies change.

**IR-03 — Sequence cheap informative controls.** Specify that the v2 protocol includes an otherwise identical pooled-residual control to identify the effect of hour-aware uncertainty; it is a declared control, not an unlimited sweep. For weather, direct-weather paired ablation precedes optional intermediate generation/residual-load modelling. Resolve the current conflict between “optional VRE” and a mandatory direct-versus-VRE deliverable. Define the point at which an authorized protocol stops or justifies the extension. A negative direct-weather result is not proof that every VRE representation fails. Keep architecture challengers optional; no automatic new-family replacement search on an admission failure.

**IR-04 — Make economics a specific policy.** Carry forward the Owner's unresolved economic specification and the option to keep economics descriptive. Add required future fields for forecast functional/objective, cashflow and settlement resolution, deterministic optimization tie-breaking and solver settings, missing-input execution, cost/physical constraints, aggregation/denominator treatment and uncertainty. Do not silently treat hourly complete-day diagnostics as quarter-hour outage-inclusive product economics or marginal quantiles as joint scenarios. Clarify the fixed-strike illustration: buy at the hourly price, resell/offset exposure at €50; payoff `(50-y)*I(p50<50)`. No new trading implementation is requested.

**IR-05 — Strengthen archive admission without executing it.** Preserve plausible NCAR/OCF historical depth and the 16-active-hour gap-list stop. Add explicit required-lead/field endpoints, historical model/schema changes, supported current access, historical-to-live equivalence, source retrieval/fingerprint and publication-versus-retrieval evidence. Mention NCAR's update-stop warning and Dynamical's phased migration planning date of September 30, 2026, with a current primary-source link. Do not call it universal data deletion or infer OCF history from a replacement service. No provider/fold is admitted by the rewrite.

**IR-06 — Attach verification labels to exact claims.** Separate the original claim from the revised specified experiment. Unknown original recipes are NOT TESTED as exact experiments; matching revised figures are REPRODUCED; related variants with differences are REPRODUCED WITH DEVIATION. Use NOT REPRODUCED only for an adequately specified tested claim or unsupported source assertion, explaining the object. Carry the fixed-p50, bootstrap, B0 solver-tie and calendar-adjacency caveats from the independent review. Record the six-arm population and distinguish metric grids/weighting. Do not present the earlier review's code appendix as covering calculations it omits. Link the independent durable methods.

**IR-07 — Complete the disposition/freeze/run/evaluation chain.** If 4.8 recombination is admitted it precedes final 4.7 disposition; otherwise record its deferral. A qualified path requires feasibility, exact policy/initial-state registration, separately authorized prospective issuance/scorecard, ≥90 consecutive post-freeze delivery days, registry/fingerprint verification before outcome access, and a final ratified evaluation. Preserve failures/staleness and the rule that a policy change starts a new evaluation. Keep future monitoring/operational metrics and publication authority explicit; elapsed time alone is not evidence. Do not amend §§8–10 or authorize any stage yourself.

**IR-08 — Correct narrow numerical descriptions.** The nominal full-history blocks have 5,824 night / 5,096 solar / 6,552 shoulder rows before eligibility/DST, or clearly state that ~5,800 was an average approximation. Median pinball is MAE/2, with the same minimizer as MAE, not numerically MAE. Correct only the proposed plan; do not repair Q&A or unrelated files. Runtime/gap-closure estimates remain unmeasured.

## Facts, numbers and caveats that must survive

Preserve these in the plan or its explicitly linked evidence ledger with clear labels. Do not convert estimates/unknowns into acceptance criteria. The independent review supplies full-precision values and methods.

- CP-15 Engineering PASS and `product_feasibility = NOT_DEMONSTRATED`; no successor is promoted/frozen and no prospective clock has started. Keep historical v1 failures, including p=.948 and 79/408 peak coverage, as existing reported evidence rather than newly verified facts.
- **Unchanged `capstone_v21.md` §8**, including failed aggregate limits **S_MAE .59203 / S_WIS .57509**, per-fold/peak constraints and its legitimate diagnostic best-reference comparator. Future criteria require the authorized additive amendment route, not a quiet relaxation or retrospective PASS.
- Independent gate on 10,747 original targets per policy, equal folds, emitted p50 and seven-quantile WIS: **B0 1/1; B2 .65781/.63899; A1 .67229/.64602; A2 .77371/.73167**. Keep B1/B0 fold-3 WIS **87.94/51.73** scoped to their different comparator constructions and native v1 pinball separate. CP-15's crisis MAE **140.99→51.21** is not an achievement of unbuilt v2.
- Six-arm mean **.67136**, restricted static/fold/hour optima **.63544/.62472/.62634**, fold×hour **.60407**, row discrete/convex **.33445/.27245**. Original .63744/.63015 versus pooled-objective explanation stays a qualified provenance issue, not proof of the old code's objective. No information ceiling or universal combination impossibility.
- Emitted A1+B2 blend **.64466/.62002**, central blend before new residuals **.64070 S_MAE**, four-component emitted mean **.64280**: different policies, none is measured performance of the proposed causal v2. Reduced-grid QRA/stacker/controller results remain explicitly unverified where recipes are absent.
- Day switching: **227/448**, crisis **53/88**, represented-adjacent lag **.07889**, calendar-adjacent sensitivity **.08134**, mean run **2.14354**; oracles **.65138/.59919/.53055**. No inference of conditional unpredictability from weak unconditional persistence. Classification accuracy does not measure weighted loss reduction.
- Hour-aware mismatch and alternative oracle WIS **.61048/.58936**, fixed emitted p50 and evaluation residuals. The causal .63793, .589–.638 range, ~2.4% opportunity and original criterion-5 oracle claim are not verified causal outcomes/bounds. A new residual median can change point performance. Twenty-eight per-hour errors do not support accurate 2.5% tails by themselves.
- Battery: distinguish the original underspecified table from the explicit 444-complete-day sensitivities; closure permits multiple cycles and simultaneous modes; costs/constraints and averaging change comparisons. A2 leads pooled EUR/day in tested settings while blend/B2 can lead equal-fold capture under cost. **A2−blend +1.806 EUR/day, exploratory 95% interval [−.486,4.292]**. B0's **221.86398 versus 221.90379** reflects equal-objective dispatch ties. No generalized economic winner, annualization, or confirmatory claim.
- **Keep the complete economic-threshold contamination block from §3.1 intact.** It discloses that the one-third-gap/≈90.9% threshold was selected after seeing 90.7–91.4% candidates and must not be adopted as written. Do not weaken it, quietly delete it or claim that new thresholds make old outcomes unseen. Outside the preserved block, clarify historical wording: the new exploratory CI does not rehabilitate the threshold, and any “v2 already achieves” phrase in the historical disclosure is not a result for the unbuilt causal v2.
- Raw-head A69 nine-quantile pinball **13.01584151→10.47871463 (19.49260734%)**, raw-p50 MAE **41.75983236→29.93830428**; post-gate v1 feature bundle, no CP-15 normalized/interval transfer or in-house VRE recovery fraction. Fold 2 worsened; pooled gain does not mean every-fold gain.
- SMARD and TenneT schedules support rejection of their named late publication routes, not all possible pre-gate VRE products. Deadline is not earliest publication; initialization is not publication.
- Archive documentary dates: NCAR GFS **2015-01-15**; OCF ICON-EU **2020-01-01** with early subset/March-2023 schema change and discontinued updating; OCF ICON-Global **March 2023**; Dynamical GFS/ICON-EU **2021-05-01/2026-02-10**. Open-Meteo historical stitched, Previous Runs fixed offsets and Single Runs are different products; early Single Runs IFS coverage is explicitly described as hindcasts. Documentary depth is not field/lead/vintage/publication admission.
- First-evaluation training starts **2019-01-01/2019-04-04/2020-07-03/2023-05-04/2024-01-11**, earlier warm-up subject to the 2019 floor. Preserve **11:00 UTC** origin separately from Europe/Berlin delivery calendar, complete-day D−2 error release/consume-once, units/scale, ordered quantiles, and origin-safe held-forward generated VRE features. Lead checks must cover approximately h22–h46 hour starts plus interval/interpolation endpoints, not only a single h24 forecast.
- April 8–September 6 is **152 dates**, not unseen confirmation; April 8–September 22 is 168 only including that date and exceeds the snapshot. Later dates are not automatically collected/authorized. Qualification uses **≥90 consecutive delivery days after policy freeze** under a ratified protocol. Keep all reused development results labelled `development_post_selection`.
- Zero external cost. Free registration/click-through acceptable as applicable; no paid or negotiated route. Preserve TabPFN eligibility/output/hosted-service caveats; Chronos pretraining overlap unknown; DDNN delivery/runtime unproven; NBEATSx deferral is a budget choice, not lack of exogenous inputs. No new architecture performance promises.
- Keep historical failures and material repair-scope disclosures visible. Q&A numbering/format work is outside scope; any owner-reported count remains attributed and unverified. Do not add a maintenance work queue.

## Decisions reserved to the Owner

Leave unresolved unless a new explicit Owner instruction in your session settles them:

- Intended user, decision/exposure and next delivery: research, point product, interval product, or both.
- New comparator and point/interval/coverage/support/uncertainty/economic gates, external economic rationale and required net surplus. “Descriptive economics” remains an option.
- Allowed market/settlement resolution, live operation expectations and quality-versus-delivery tradeoff.
- Exact resource/candidate allowances requiring a material scope decision; the admitted challenger family and whether optional VRE/recombination proceed.
- Archive fallback scope if admission fails: modern matched folds, amended dates under retained input boundary, causal proxy or prospective route. Do not choose one by default.
- Task-scoped Lockdown suspension, additive amendment, ratification, checkpoint/operational authorizations and release route.
- Owner landing, commit and publication. No agent chooses or carries these out.

Do not stop the document rewrite merely because these remain undecided. Make them explicit dependencies of the work they actually block.

## Acceptance checks for the revised document

1. Only the target durable file changed; its before bytes were preserved locally. All pre-existing unrelated dirty files are unchanged by this task.
2. Every material finding IR-01..IR-08 has a disposition: **addressed**, **retained with reason**, or **blocked**, with target section and evidence/reason. Include this matrix in the terminal return, not in a new durable file outside your allowlist.
3. Prose and work table agree on dependencies. Existing-input v2 and existing-evidence research content are not implicitly weather-gated. If admitted, recombination feeds final disposition before freeze. No research route claims to bypass Owner/anchor authority.
4. Every scheduled item has a deliverable/executor, dependency/authority, finish distinct from favorable performance, measurable criterion or named unresolved Owner decision, effort and elapsed dependencies, stop/budget or explicit pre-execution budget blocker, output destination and result-to-handoff path.
5. No numeric resource limit, candidate result, acceptance bar, admitted archive, forecast gain or Owner decision was fabricated to fill a cell. Future conditional work is not presented as fully execution-ready.
6. Point, interval and economic estimands are distinct. Quantile levels, equal-fold ratios, original rows, central/emitted differences, complete-day economics and oracle versus causal evidence are labelled consistently.
7. All historical failures, `development_post_selection` labels and the full economic contamination disclosure survive. Original §8 is unchanged; no new threshold retroactively changes CP-15's verdict.
8. Registry/fingerprint-before-outcomes, operational authorization, freeze, prospective clock, failure accounting and policy-change restart remain explicit. No historical confirmation window is called unseen.
9. Check links and current-source attribution for changed material external claims. A primary source or independent-review calculation that contradicts a proposed correction takes precedence over blind compliance; surface the contradiction and your evidence. Never silently implement an unsupported review correction.
10. Count lines/words and report them relative to the before copy. Aim for clarity, not an arbitrary reduction. Prefer a readable first packet plus conditional work over compressing unresolved decisions into dense cells. Do not render anything or execute experiments for document QA.

## Required terminal handoff

Finish one coherent document revision, then stop. Return:

- What changed and why; readiness of the bounded first packet separately from the entire programme.
- The complete IR-01..IR-08 disposition matrix and any contradictions found in the independent review.
- Remaining Owner decisions and exactly which work they block.
- Full **before/after task diff against your saved before copy**, not merely a diff against HEAD (the target may be untracked/dirty already). Make the full diff accessible and account for it.
- `git status --porcelain=v1`, `git diff --stat`, task-only diff statistics, and file accounting with one-line reasons. Separate pre-existing work from your edits. Do not stage to obtain a diff.
- Link to the revised plan and a proposed commit message; Owner alone decides committing/publication.
- Declaration of branches/worktrees/tags created: expected **none**; declaration of no checkpoint execution, fitting, reserved-outcome reads, governance edits, Q&A edits or publication.
- Any interview-answer capture trigger, in one line only; file no Q&A entry.

Then stop. Do not execute the revised plan or launch its executor.

---

End of transfer prompt.
