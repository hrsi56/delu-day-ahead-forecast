# Publication Standard, version 1

> **Work-availability amendment, Owner-authorized 2026-10-10.** Scheduling restrictions
> have been removed under `AGENTS.md` § Work availability. Historical hashes and reviews
> bind the prior text at `522d7ea:docs/track-b/publication-standard-v1.md`; they do not bind this amended copy.

**Ratified by the Owner, 2026-09-28,** with the decisions recorded in §17. The record of how the
standard was derived and challenged is `docs/track-b/publication-standard-derivation-2026-09-28.md`.

**What it governs.** Every public surface of the DE-LU forecasting project:

- the report site on GitHub Pages (`docs/index.html`);
- the repository's README;
- the Hugging Face Space and its cards;
- the public MLflow experiment `delu-generations`;
- any future live panel.

**Precedence.**

- **Research anchors govern the research.** The ratified research anchors and the Owner's
  standing decisions govern what is evaluated, against what, and on which data. This standard
  governs only how results are published, and never overrides them.
- **It governs presentation from now on.** Plan revision 3 (`presentation-and-tracking-plan-2026-09-24.md`)
  specified PRES-1: one page, at one moment. This standard governs every publication from now on,
  including the completion of PRES-1. The plan clauses listed in §15 are amended at ratification.
  Everything else in the plan stays in force (§14).
- **Nothing downstream may relax it.** A later plan or brief may add requirements. It may never
  relax a clause of this standard.
- **Authority is unchanged.** `AGENTS.md` stays the authority on publication, `main` and
  credentials. Nothing here grants an agent the right to publish.

---

## 0. Why it exists

The PRES-1 review history showed three failures.

- **No floors.** The plan said at length what must not be said, and never what must be said, or
  where.
  - In the first D1 specimen, a number was on the first screen.
  - After D1, the headline sat on screen 2 as a sentence without numbers, and the numbers only on
    screen 5.
  - The reader gate passed every round, because its tasks asked only whether a reader could
    locate an answer.
- **No single source for the story's state.** The numbers have one source, and it is excellent.
  Names, statuses and "current" are typed in many places.
  - v3's chapter says "We retained v3 as the current research model", which becomes false the day
    v4 is adopted.
  - Publishing v4 on today's system touches about 45 places in 9 files.
- **A review ratchet.** Each round reviewed against the previous bar and could only add
  constraints. The plan's own reader-hostile clauses stayed frozen, because no reviewer had a way
  to change them.

This standard adds four things:

- floors;
- names and statuses derived from one registry;
- complete-or-nothing publication;
- a blocking rule with an amendment channel.

---

## 1. Audience and the reading contract

**The readers.** A Lead Data Scientist and a VP R&D or engineering lead, evaluating the Owner for a
team role. They are busy, sceptical and competent. They know MAE, confidence intervals and
benchmarks, but not this project's codes.

**The reading path** is the rendered page minus the bodies of closed disclosures and the value
tables, counting only the desktop variant of each chart. It also covers the README's generated top
block. All measurements below are made with every disclosure closed, in Chrome and in WebKit.

| Layer | Must answer | Placement |
|---|---|---|
| **Headline** (about 10 s) | What is forecast; the headline result with its numbers (§3); its evidence class; what the demo runs | The headline block is fully visible without scrolling at 1,440 × 900 and at 390 × 844 |
| **Orientation** (about 60 s) | (i) The change against the comparator with its interval, and the main caveat. (ii) The terms first used in the headline, defined. (iii) Why the demo runs the model it runs (§5, the release rule). (iv) A route to who did what. | (i) is in the comparison panel, above its chart. (ii) is directly below the headline block. (iii) is beside the demo action, outside any disclosure. (iv) is the byline link. The comparison's finding sentence is fully visible within 2 screens at 1,440 × 900 (1,800 px) and within 3 screens at 390 × 844 (2,532 px). |
| **Journey** (about 5 min) | Each generation's question, change, result, limits and decision; what was tried and dropped; how the system works, with a stack line; how to check it | The fixed order of §6 |
| **Deep** | The evidence records, reviews, MLflow runs and code | One click from each evidence row |

**Tone.** Seriousness shows in the quality of the comparison and in how easy it is to check. It
does not show in how often the page says it was checked. Each caveat appears once, where it applies,
and is phrased as a property of its evidence class ("development evidence, not a test on new data").
Caveats never use wording that expires, such as "still to be evaluated".

---

## 2. Evidence classes

Every result belongs to exactly one class. The class decides its badge and its wording.

| Class | Badge | May say | May not say |
|---|---|---|---|
| **Development** (post-selection, historical data) | "Development · post-selection" | "improved in development tests"; "met the targets set before the experiments (first of N policies tested)"; "adopted in research" | Significance wording; an unqualified "outperforms" or "beats"; "validated", "confirmed", "proven"; product readiness, qualification, promotion or live selection |
| **One-shot test** (pre-specified, run once on data never used for development or selection) | Set by the 4.7T protocol. v1's holdout keeps "Confirmatory-style, not power-qualified". | "evaluated once, as specified in advance, on N days never used for development or selection" | "Confirmatory" without its qualifier; pooling with development numbers |
| **Live, prospective** | "Prospective · N days" | "over N live days: forecasts issued before the auction, scored afterwards" | Extrapolation beyond the period; economic value |

**Rules.**

- The headline carries its class badge.
- Numbers from different classes never share a chart or a sentence as if they were comparable.
- The hero shows the model with the highest status reached: live, then final candidate, then
  released, then research. The registry decides which (§5).
- The withheld claims W1–W21 continue.

---

## 3. The headline, defined before any result exists

These rules hold for every generation. No publication chooses its headline after seeing its result.

### 3.1 Primary scores

The primary scores are the ones the governing research plan names. Today they are S_MAE and S_WIS:
a policy's error relative to the similar-day naive forecast in each test period, averaged over the
periods with equal weight.

- **Plain names:** "point-error score" and "interval score".
- **Collective name:** "error scores".
- **Definition, at first use:** "error relative to a simple naive forecast, averaged over the test
  periods; lower is better".

### 3.2 The comparator

- **Who names it.** The governing research plan and the Owner's standing decisions name the
  comparator. Since 2026-09-24 it is HG, with HG's information, on identical rows.
- **When it is recorded.** The registry records it before results exist.
- **Past comparisons stand.** v2 was compared with daily LEAR, and v3 with v2.

### 3.3 The headline quantities

Every quantity below is a **typed derived record.** Each one is:

- computed by a formula in the evidence layer from committed rows;
- re-derived by the tests, as `test_29` does today;
- mapped in the claim map.

**(a) The pre-specified verdict.** It applies when the governing research plan set a target or a
decision rule before the experiment, for example criteria 1–2, or a joint-improvement rule
against HG. It states:

- met or not met;
- the rule in words;
- the date the rule was set, citing the record that establishes that date;
- the distance from the rule's comparator, in the rule's own unit;
- **N:** the number of policies tested against the same rule up to this decision, frozen at that
  date;
- the label "point comparison" whenever no confidence interval exists.

**(b) The change against the comparator.** The difference in each primary score, given as a share
of the comparator's score in whole percent.

- **Its 95% interval** is the committed interval of the difference, divided by the same fixed
  denominator.
- **Its label** reads "as a share of <comparator>'s score".
- **From CP-21 on,** each checkpoint computes the interval of the ratio from its own bootstrap
  draws, and the headline uses that interval.
- **Never write "N% lower error".** Absolute error changes by a different amount in each period.

**(c) Absolute context.** Mean absolute error in EUR/MWh, shown as a range over the ordinary test
periods, with the stress period stated separately.

- The research protocol names the stress period; it is not assumed to be fold 3.
- This is context only: it never ranks and never leads (W11).

**What may not appear on the reading path:**

- **Other relative-change percentages.** None may appear.
- **Exceptions.** Nominal levels (80%, 95%) are structural numerals. v1's statements protected by
  invariant 4 keep their exact form.

### 3.4 The headline block

**Its form.** One sentence plus the class badge.

- It is generated from the registry's current generation and its derived records.
- It renders identically in the research status card of the page's opening and at the top of the
  README.
- It leads with (a) when a pre-specified rule existed, and with (b) otherwise.
- The change with its interval, and the qualifier that the result is "a development diagnostic,
  not a product qualification", belong to the orientation layer.

**For v3:**

> Met both accuracy targets set before the experiments: error scores at least 10% below the
> strongest benchmark, daily LEAR (v3: 14% and 17% below; the first of 8 policies tested to meet
> them). [Development · post-selection]

### 3.5 Branches, secondary outcomes and changed populations

- **A branch-only checkpoint.** When a checkpoint yields only a rejected branch, the headline
  stays with the current adopted generation, and the branch appears as a dated card in the lineage.
- **A secondary outcome.** A generation's brief may declare one secondary outcome before any
  results exist.
- **A changed population.** If the evaluated population changes, the page says so. No metric is
  switched because of it.

### 3.6 The one-shot test and live

**The one-shot test.**

- The headline uses the protocol's own metric and window.
- It states the dates of the fresh window, which never overlaps a period already published.
- The badge and wording are fixed before the test (§16).

**Live.** The headline states the number of live days and nothing beyond them.

---

## 4. Numbers and words

These rules apply on the reading path (§1).

**Precision.**

- Scores and differences: at most four significant figures.
- Percentages: whole numbers.
- EUR/MWh: one decimal place.
- Each chart uses one precision.
- Exact values live in the value tables.
- Exempt: structural numerals (versions, dates, levels, counts), axis ticks and the
  invariant-4 statements.

**Never round toward zero across a sign.** A value near zero keeps its sign and at least two
significant figures, for example +0.0000039. Its full value appears in the value table. This amends
invariant 9 and keeps its purpose, W3.

**p-values.** They are floored at 10⁻⁶ ("p < 10⁻⁶"). The exact value is kept in the value table.

**Units and comparators.** Every number states its unit and its comparator. One axis carries one
unit (invariant 15).

**Plain names first.** These never appear on the reading path:

- checkpoint codes and policy codes;
- S_MAE or S_WIS without its plain name;
- claim IDs and §-references;
- identifiers such as NOT_DEMONSTRATED.

They may appear in the detail layer and in value tables.

**Definitions.**

- Each term is defined where it is first used.
- Terms first used in the headline block are defined directly below it.
- There is no separate glossary.

**Thresholds.** A threshold is stated in words, with its date. For example, "target: at least 10%
below the strongest benchmark (set 2026-09-15)". A bare "limit 0.59203" does not meet this rule.

**v1.**

- v1's chapter follows these rules, except for the statements invariant 4 protects.
- v1's archive stays as published (invariant 24).

### Enforcement

One lint with rule families. Each family has a negative control.

- **Codes.** A denylist generated from the registry's code fields, plus these patterns:
  - checkpoint codes, `CP-\d+`;
  - claim IDs, `[CPW]\d{1,3}`;
  - section references, `§\d`;
  - underscore identifiers, `[A-Z]+_[A-Z_]+`.

  There is no hand-kept list.
- **Precision.** Each bound value is checked against the unit of its record. Any numeral that is
  not bound to a record fails.
- **Percentages.** A `%` passes only as one of:
  - a derived relative-change record;
  - a structural level;
  - an exempt v1 statement.
- **Status words.** This family runs over the template sources, not the rendered page (§5).

The PRES-1 conformance task builds the lint (§16). From then on it runs in CI.

---

## 5. The registry: one source for identity, status and comparability

There is one entry per generation, branch, reference, study arm and control:

| Field | Content |
|---|---|
| Identity | `id`; a canonical name (`vN · <adopted change>` for generations, a descriptive name for everything else); a subtitle of at most eight words |
| Kind | One of: generation, branch, reference, study arm, control |
| Codes | Its experiment codes. v2 is `V2-H` in CP-16 and `H0` in CP-20: one identity with two codes. |
| Status history, dated | adopted in research, not adopted, released, final candidate, live, retired |
| Comparison | Its comparator (§3.2) and the comparability ID of its evaluated population |
| Evidence | Evidence class; governing plan and pre-specified rule, if any; evidence sources; claim map; MLflow run keys |

**Rules.**

- **Every surface derives its names, statuses and order from the registry.** On the page this
  covers:
  - the opening's status pair;
  - the rail, jump row and lineage;
  - the comparison rows;
  - chapter order and headers.

  Elsewhere it covers the README headings, the Space card's model line, and MLflow run names,
  descriptions and tags.
- **Status is derived, never typed.**
  - Templates are dated and in the past tense, for example "In September 2026, v3 was adopted in
    research".
  - Status words ("current", "latest", "still", "now", "the demo runs") come only through registry
    tokens.
  - A lint over the template sources catches common synonyms. The checker's rubric backs it up.
- **One comparability ID per comparison chart.**
  - The build refuses to draw a mix.
  - A generation evaluated on a new population gets a new comparison, and the earlier one stays in
    its chapter.
- **The release rule is stated once, from the registry.** The demo runs the released model.
  Research generations are not released one by one; only the final model, after its one-shot test
  and live run, replaces the released one.

---

## 6. Page architecture

**Section order.**

1. The header.
2. The opening: title, description, the status pair carrying the headline block, actions, the
   release rule and the preview.
3. The lineage.
4. The comparison.
5. The chapters, newest first.
6. Planned work.
7. How the system works, with a stack line rendered from the system-view data.
8. Reproduction.
9. The contribution statement.
10. Terms and attribution.

Moving planned work after the chapters amends plan §7.2 (§15).

**The chapter grammar.** A generic renderer fills these fixed slots:

1. the question and the change, as one diagram;
2. the main chart: paired differences against the comparator on both primary scores, with 95%
   intervals;
3. the reading, in one sentence;
4. at most three things the result does not establish;
5. the decision, dated;
6. the evidence row;
7. details from a fixed menu:
   - method;
   - per-period consistency, including absolute per-period errors;
   - the stress period;
   - coverage and width;
   - protocol and review.

Chart headlines are claim-bound blocks.

**The branch card.** It carries the question, the comparator, and the difference with its interval
(or the diagnostic that decided it). It then states "Not adopted", with a one-line reason and the
evidence. Branches attach to the lineage where they belong in time, including after the latest
generation.

**v1.** v1's chapter follows §4. Its archive is not migrated to the grammar.

**Scale.** The 2.0 MB size budget holds. When a new chapter would breach it, or at v5, whichever
comes first, the Orchestrator proposes a compaction rule to the Owner. Any option that moves full
chapters out of the page needs the Owner to amend the one-page decision (§16).

---

## 7. Evidence tiers and links

- **Reader grade.** These may be linked from the reading path:
  - MLflow runs and comparison views;
  - the page's own value tables.
- **Audit grade.** These appear only in the evidence row:
  - engineering reports;
  - review verdicts;
  - claim maps;
  - raw CSV rows.

  Each one's label says its type and date, in the form "<type>, frozen <date>". For example:
  "Engineering report, frozen 2026-09-24".
- **Classifying a link.** A link is audit grade when its target is under `reports/` or
  `docs/track-b/evidence/`, is a claim map, or is a `.csv` file. The date in its label must match
  the date of the evidence tag.
- **Frozen records are never edited.** A stale line inside one is neutralised by its label.
- **No link lands on a record whose status contradicts the registry,** unless its label says the
  record was frozen before that status. This is a rubric item. Today's "Full report" link fails it:
  it lands on "pending fresh exact-candidate Integration review".

---

## 8. Surfaces

**The README.**

- **Top:** a generated "At a glance" block holding:
  - what the project is;
  - the headline block;
  - the demo, the report, the evidence and MLflow.
- **Next:** a generated list of generations from the registry.
- **Then:** stable hand-written sections only, such as how to run the project and the licence.
- **Anywhere:** no hand-written "current" state. v1's "30-second read" moves under a v1 heading.

**Limitations (invariant 5, re-scoped).** A model's limitations appear on every surface that
presents that model:

- the demo;
- the Space card;
- its chapter;
- its README section.

A retired model's limitations stay in its archive.

**The Space card.** Its model line and links derive from the registry.

**MLflow.**

- Run names, parent names, descriptions and tags derive from the registry.
- The experiment description says the repository is the source of truth.
- The mirror verifier, not a person, writes `mlflow_index.json`.

**The repository root.** What sits in the root is the Owner's personal decision. It is outside this
standard.

**Parity.** A cross-surface test, extending `verify_release.py`, checks that the headline block,
names and statuses agree on every surface.

---

## 9. Completeness: publish everything or nothing

**No placeholder reaches `main`.** A `data-unpublished` marker, or a build record with
`final: false`, never reaches `main`.

- It is enforced before the push, by the repository's fail-closed pre-push hook.
- CI is a backstop, because Pages serves `main` as soon as it is pushed.

**MLflow comes first.** The runs are uploaded and verified before the final page build. Only routes
that pass their checks are advertised.

**What is not ready is left out.** A service or route that is not ready has its link omitted, never
replaced by a placeholder.

---

## 10. Devices and accessibility

**Required release checks,** recorded in `reports/presentation/release-checks/`:

- **Engines and widths:** Chrome and Playwright's WebKit, at 1,440 × 900, 768, 390 × 844, 360 and
  320 px, plus Playwright's emulated iPhone.
- **Accessibility trees,** in both engines:
  - disclosures expose an expanded state;
  - charts are named;
  - no control is unnamed.
- **Keyboard order and visible focus.**
- **Touch targets** of about 44 px.
- **Contrast** for text and for non-text elements.
- **No failed requests.**

**What is not required.** A real Safari, a real iPhone and a screen reader. Every record states
that they were not used. Both PRES-1 independent checks failed on that requirement, and no agent can
meet it. A person's check is always welcome, as an addition, never as a precondition.

---

## 11. Gates and review

**CI, offline, on every push.**

- Evidence re-derivation and claim binding (`test_29`, `test_30`).
- The §4 lint.
- Registry consistency, with a negative control.
- Cross-surface parity.
- Zero fetches.
- No placeholders on `main`.
- **Contract tests, never content counts.** A test says "the export matches the registry", never
  "exactly 23 runs".

**Release checks, local and recorded.**

- The §1 placements, in Chrome and WebKit.
- Chart rendering at every width.
- The demo's cold start.
- The link gate.
- The MLflow mirror verification.

**The cold-reader check.** A fresh agent with no project context gets only the rendered screens,
with disclosures closed. It answers six fixed questions:

1. What is the headline result, with its numbers?
2. Against what?
3. How sure are we, and on what class of evidence?
4. What does the demo run, and why not the best model?
5. What was tried and dropped?
6. What would you ask the candidate?

- **To pass,** answers 1–5 must match the registry and the derived records, within the §1
  placements.
- **Answer 6** is advisory input.

**The independent check.**

- **The checker** is an agent that wrote nothing in the publication.
- **Its bar** is the clauses of this standard in force for that publication (§16), plus the
  brief's acceptance criteria.
- **Its scope** follows the rendered diff. An unchanged part needs proof that it is unchanged:
  byte-identical output, or identical output record by record. Otherwise the check is full.

**The blocking rule.** Only a violation of a clause in force, or of the brief's acceptance
criteria, blocks a publication.

- **Everything else is advisory.** It goes to the advisory log,
  `docs/track-b/publication-advisory-log.md`.
- **After each publication,** the Orchestrator reviews the log and may propose amendments (§13).

**One binding PASS.** It is on the final candidate SHA. A change after the PASS needs a focused
recheck. The Owner's final approval follows, unless he has delegated it for a named publication.

---

## 12. Publication as a step of every checkpoint

**The publication packet.** Each research checkpoint's return includes it:

- the draft registry entry;
- the claim map;
- the derived headline quantities, computed inside the checkpoint:
  - the verdict and N;
  - the ratio's interval from the checkpoint's own bootstrap draws;
  - the per-period ranges;
- draft slot texts;
- the MLflow export.

**The publication runs in this order:**

1. Build from the packet.
2. One editorial review against this standard.
3. The cold-reader check.
4. The independent check.
5. The MLflow upload and verification.
6. The final build.
7. A focused recheck on the final SHA.
8. Landing, push and Space redeploy. These are done by the Owner, or on his explicit instruction
   naming the action (`AGENTS.md` § Git and publication authority).
9. The post-deploy checks.

**Where the packet is specified.**

- **Now:** CP-21's brief carries the packet as its own section.
- **Later:** it moves into the landing templates, which are locked. That needs the Owner's
  2026-09-24 decision-4 suspension, extended to cover the packet (§17, D6).

**The runbook.** `docs/track-b/publication-runbook.md` lists every touchpoint.

---

## 13. Governance

**Ratification.** The Owner ratifies this standard. Every publication brief cites its version and
SHA-256, and the checker verifies them.

**The locked core.** Only the Owner changes these clauses:

- §1's floors, and the existence of its placements;
- §2;
- §3;
- §5's rules;
- §7;
- §9;
- §11's blocking rule.

Until the standard is added to the locked set in `AGENTS.md`, the core is protected by detection
only: briefs cite the ratified hash, and the checker verifies it.

**The flexible part.** The Orchestrator may change these, with a changelog entry reported to the
Owner:

- copy, except the contribution statement and the Owner's public name, which only he changes;
- the chart vocabulary;
- tooling;
- tests;
- the numeric placements, which the Orchestrator may tighten but only the Owner may loosen.

Visual tokens stay the Owner's choice (plan §16, decision 9).

**The amendment channel.** After each publication, the Orchestrator reviews the advisory log and
proposes amendments. The Owner ratifies each new version.

---

## 14. What carries over

**Plan revision 3's invariants 1–26 stay in force** for every publication, as amended in §15.

- **The date boundary (invariant 10), as interpreted in §17, D3.** Before the final test, no
  research generation's number, chart or choice uses data dated after 2026-04-07. v1's published
  holdout replay is kept as published.
- **The other invariants carried over,** among them:
  - the wall around live data (7);
  - attribution (8);
  - Owner review before anything becomes public (20);
  - unscored planned work (26);
  - the `.mlflow` host (6).

**What PRES-1 built, kept:**

- **The evidence layer:**
  - typed records with hash-checked sources;
  - re-derivation tests with negative controls;
  - no generator types a research number;
  - a data binding on every rendered number.
- **Cross-surface agreement:**
  - one template per claim, for the page and the README;
  - v1's agreement check across surfaces, re-scoped.
- **The honesty devices:**
  - evidence badges;
  - "What this result does not establish";
  - v1's failure section and holdout label.
- **The page itself:**
  - one self-contained offline file;
  - phone chart variants with text of at least 12 px;
  - direct labels on chart marks;
  - accessibility checks;
  - v1's archive.
- **The MLflow pipeline:**
  - a deterministic export;
  - the outbound secret scan;
  - idempotent, verified publishing.
- **Independent checking** and the contribution statement.

---

## 15. Plan clauses amended at ratification

| Plan revision 3 | Amendment |
|---|---|
| §8.1 "At most one summary value … no new promotional percentage" | Replaced by §3. The headline block is required. Percentages are allowed only as pre-registered derived records. |
| §8.2's reference-line label, "the plan's diagnostic limits (criteria 1–2)" | "Target: at least 10% below the strongest benchmark (set 2026-09-15)", with a met / not-met column and N |
| §7.2, section order and "an information order, not a demand to fit everything above the fold" | Planned work moves after the chapters. The §1 placements apply. |
| Invariant 9, "printed in full" | §4: the sign and at least two significant figures on the reading path; the full value in the value table |
| §8.5, v1's holdout p = 1.98e−18 | "p < 10⁻⁶" on the reading path; exact in the value table |
| Invariant 5, "every limitation appears on every human surface" | Per model (§8) |
| §8.3, "adopted as the current research model" | Status is derived (§5) |
| §11.3, real Safari and iPhone | §10 |
| §11.4, locate-only reader tasks | §11's cold-reader check |
| §10.3's run count, used as a test constant | A contract test: the export matches the registry |
| §15, "using the same template" | §6's chapter grammar and branch card |

---

## 16. What is in force now, and what waits for a trigger

**In force from ratification: every clause of §1–§15.** On 2026-09-28 the Owner instructed that the
current state be brought to this standard "including everything". The PRES-1 conformance task
therefore implements all of the following:

- the registry, with derived names, statuses, comparators and comparability IDs, and MLflow names
  taken from it;
- the typed derived records and the headline block;
- the §1 placements;
- the chapter grammar and generic renderer, with v2 and v3 migrated and v1's archive untouched;
- the branch card;
- the §4 lint and the status lint;
- the evidence tiers;
- the README structure and cross-surface parity;
- the completeness guard;
- the §10 checks;
- contract tests in place of tests pinned to content;
- the runbook and the publication-packet template.

Its brief is `docs/track-b/pres-1-conformance-brief-2026-09-28.md`.

**Waits for its trigger:**

- **At v4.** The chart encoding for a fourth generation. Plan §7.8 encodes generation identity by
  colour, and visual tokens are the Owner's. The conformance task returns a proposal, and the
  Owner decides before v4 is published.
- **At v5, or when a chapter would breach the size budget.** A compaction rule, decided by the
  Owner (§6).
- **Before the final-candidate test.**
  - The one-shot badge and wording, under the 4.7T protocol.
  - Its headline window.
  - The rule for switching the hero.
- **Before Live.**
  - **Daily data-only updates.** They need an `AGENTS.md` amendment by the Owner, or an Owner-run
    push. "Pre-authorised" publishing does not exist under today's rules.
  - **The `delu-live` experiment and the `delu-day-ahead-policy` registry model** (plan §10.11).
  - **An extended `test_24`.**
  - **A live panel** with its own claim builder.
  - **The demo concept** for models that need a daily weather download.

---

## 17. The Owner's decisions at ratification, 2026-09-28

| # | Decision | Outcome |
|---|---|---|
| D1 | Ratify this standard, with the locked core of §13 | **Ratified.** The core is protected by detection (§13). Adding the standard to the Lockdown's locked set needs a future suspension that names that edit to `AGENTS.md`. |
| D2 | The §15 amendments: the headline and target line; planned work after the chapters; the endpoint and p-value display; the per-model scope of invariant 5 | **Approved** |
| D3 | The date boundary: v1's published holdout replay (the opening preview and v1's archive) stays as published. No research generation's number, chart or choice uses data after 2026-04-07 before the final test. | **Confirmed** |
| D4 | The repository root | **Withdrawn.** It is the Owner's personal decision and outside this standard (§8). |
| D5 | Execution and authority | **Approved. The Owner widened the scope to "including everything", in a new Lead session.** The brief sets the ceilings. It authorizes:<br>• the Lead's F1 public MLflow upload, after an independent PASS;<br>• after the Orchestrator's verification, landing, push and the Space redeploy by the Orchestrator.<br>The Owner's final visual approval is delegated to the Orchestrator for PRES-1. |
| D6 | Extend the 2026-09-24 decision-4 suspension (the MLflow step in the landing templates) to the publication packet | **Approved.** The Orchestrator applies it in a separate task after PRES-1 lands. |
| D7 | A human cold read before publication | **Left as an option.** It is an addition, never a gate. |

---

## Appendix. The v3 numbers used as examples

These come from committed rows: `evidence/cp-20:reports/weather-ablation/metrics.csv`,
`uncertainty.csv` and `criteria.csv`. They are illustrations only; the page takes every number from
derived records.

| Quantity | v3 | v2 | Daily LEAR |
|---|---|---|---|
| Point-error score (S_MAE) | 0.5658 | 0.6441 | 0.6578 |
| Interval score (S_WIS) | 0.5322 | 0.6160 | 0.6390 |
| Distance from daily LEAR, point / interval | −14% / −17% | −2% / −4% | — |
| Change against v2, share of v2's score, 95% interval | −12% [−16%, −9%] / −14% [−17%, −11%] | — | — |
| MAE per period, EUR/MWh: ordinary periods; 2022 crisis | 5.3–15.6; 48.0 | 6.3–18.7; 51.2 | 6.2–19.2; 54.0 |

**The target** is at most 0.9 × daily LEAR's score, which is 0.59203 and 0.57509 (capstone v21
§8, criteria 1–2).

**N = 8 policies were tested against it:**

- A1–A5 (CP-15);
- V2-H and its control V2-P (CP-16);
- HG (CP-20), in which H0 is V2-H.

Only HG met it.

**The date.** The anchor dates itself 2026-09-15, and was first committed with CP-15's results at
`0be8e56` on 2026-09-16. The Orchestrator verified on 2026-09-28 that the targets preceded those
results:

- the pre-registration commit `bb5e678` (2026-09-16 00:17) holds criteria 1–2;
- the commit is reachable from the tag `evidence/cp-15`;
- CP-15's results were committed at 03:15;
- the §8 text is identical to the anchor preserved from attempt 1.

The claim map cites these records.

**The naive forecast's MAE per period** is 8.6–30.5 EUR/MWh in the ordinary periods and 86.9 in the
crisis.
