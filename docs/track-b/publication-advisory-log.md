# Publication advisory log

**Publication Standard v1 §11.** Only a violation of a clause in force, or of a brief's acceptance
criteria, blocks a publication. Every other finding is recorded here. After each publication the
Orchestrator reviews the log and may propose amendments to the Owner (§13); the Owner ratifies each
new version. Entries are appended, never edited; a later entry may close an earlier one.

| Field | Meaning |
|---|---|
| ID | `A-<publication>-<n>` |
| Source | Who found it: the Lead, an independent checker, a cold reader, the Orchestrator |
| Finding | What was observed, with where |
| Why advisory | Why it does not violate a clause in force or the brief's acceptance |
| Proposal | What might change, and who decides |

---

## PRES-1 (the conformance task, 2026-09-28)

| ID | Source | Finding | Why advisory | Proposal |
|---|---|---|---|---|
| A-PRES1-1 | Lead | W2's acceptance asks for an unchanged digest on every export artifact and for changed names, descriptions and tags. `summary.json` and `README.md` carry the run's name (and tags), so their bytes must change when the name does. | Met as the Owner resolved on 2026-09-28: byte identity for every artifact without identity; for the 46 identity-bearing artifacts, restoring the old name and tags reproduces the old SHA-256 exactly (`registry-zero-diff.md`) | Word the next registry-change acceptance as "every artifact digest unchanged, or reproduced exactly by restoring the old identity fields". Orchestrator |
| A-PRES1-2 | Lead | Playwright 1.63's public API exposes no WebKit accessibility tree. The §10 check reads WebKit's own accessibility properties through its inspector protocol (`DOM.getAccessibilityPropertiesForNode`), reached through a private playwright-core API. | The evidence is WebKit's; only the access path is private. A Playwright upgrade may break it, and the check then fails loudly rather than passing | Pin the Playwright tool version in the runbook, or adopt a supported API if one appears. Orchestrator (tooling) |
| A-PRES1-3 | Lead | marimo copies each linked stylesheet into its widgets' shadow roots, where relative font URLs resolve against the page; WebKit asked the Space's root for three fonts. The build now ships all 67 stylesheet targets at the root too (2.0 MB, 67 files). | W12 is met: zero failed requests in both engines. The extra files are copies, not a calculation | Re-check after a marimo upgrade; drop the copies if marimo fixes the resolution. Orchestrator (tooling) |
| A-PRES1-4 | Lead | The comparison's finding sentence ends at about 2,490 px on a 390 × 844 phone, 42 px inside the 2,532 px floor (§1), and at about 1,767 px on desktop, 33 px inside 1,800. The desktop margin is thin because the opening's right-hand column must stay about 460 px wide for the preview's chart text to reach 12 px. | Within the placement | Any copy added to the opening or above the comparison needs a measurement in both engines first (runbook §2, "Limits to watch"); a compaction of the opening is the Owner's design decision. Orchestrator |
| A-PRES1-5 | Lead | The status lint's synonym family flagged "this bundle remains runnable locally" on the container Space card, a statement about the bundle, not a model's status. The word was changed to "runs" under the Owner's focused extension of `build_space.py`. | Satisfied by the change | Keep the lint subject-blind (cheap, and the checker's rubric catches intent); note the pattern in the checker's rubric. Orchestrator |
| A-PRES1-6 | Lead | The container Space card (`space/README.md`) was outside the brief's write allowlist, although the standard's §8 "Space card" rule reaches it. The Owner extended the allowlist on 2026-09-28. | Resolved by the Owner's extension | Future publication briefs name `scripts/build_space.py` with the other surface generators. Orchestrator |
| A-PRES1-7 | Lead | MLflow run names carry the experiment code in parentheses, for example "v3 · weather features (HG)". MLflow views are reader-grade links (§7), and a reader following one meets the codes. | The reading path (§1) is the page and the README's top block; MLflow pages are the deep layer, where codes may appear (§4) | Consider code-free run names with the code as a tag only, before the next upload, since run names become public at upload. Owner (names are fixed before upload) |
| A-PRES1-8 | Lead | Both Space cards' shared body still uses CP-3's word "champion" for v1 (for example the holdout table's "Champion" column). | The standard's §8 card rule covers the model line and links, which come from the registry; "champion" is v1's frozen CP-3 vocabulary and names no status | Align the body with the registry's name in a later card pass. Orchestrator |
| A-PRES1-9 | Cold readers (both) | The headline's "14% and 17%" is not matched to the point-error and interval scores on the first screen; readers matched them only at the comparison. | The headline reads exactly as the standard's §3.4, which the locked core (§13) fixes | "(v3: 14% on the point-error score and 17% on the interval score; …)" in a later version of §3.4. Owner |
| A-PRES1-10 | Cold readers (both) | The comparison chart shows seven policies while the headline counts 8 tested against the targets; five of the eight are never named on the reading path. | N is the §3.3 derived record; the chart shows the comparison population, not the policies tested against the rule | Name the eight in the targets' definition, or add a one-line note under the chart. Orchestrator (copy) |
| A-PRES1-11 | Cold readers (both) | v1's 1.052 score ratio, "28.58% worse than the naive's" and its holdout win read as a clash; the reconciliation is in a closed disclosure. | Invariant 4 protects v1's statements; the reading path is correct | A one-line reconciliation beside v1's score in its chapter. Orchestrator (copy) |
| A-PRES1-12 | Cold readers | v1 is "one LightGBM quantile model" in v2's change and "A LightGBM ensemble" in v1's chapter; daily LEAR is "refitted daily" in the terms and "fitted for each hour" in v2's chapter. | Both pairs are true descriptions (nine quantile heads in one model; one linear model per hour, refitted daily) | Use one phrase for each across the page. Orchestrator (copy) |
| A-PRES1-13 | Cold readers (both) | v2's pooled-interval control is "the same blend with pooled intervals", yet its point-error score differs from v2's (−0.0017). | Research content, reported as committed | One sentence on why the interval method moves the point forecast (the median of the predictive distribution). Orchestrator, from the CP-16 record |
| A-PRES1-14 | Cold readers (both) | "+0.0000039", "+0.037" and "28.58%" read as over-precise. | Required: §4 keeps a near-zero value's sign and two significant figures; invariant 4 protects "28.58%" | None; noted for the amendment review. Orchestrator |
| A-PRES1-15 | Cold reader (desktop) | "Trained champion" is never defined. | v1's frozen archive vocabulary (invariant 24) | Consider a glossary line in v1's chapter, outside the archive. Orchestrator |
| A-PRES1-16 | Cold reader (desktop) | The preview beside v3's headline shows v1, which is easy to misread on a skim. | By design: the preview is the demo's model and carries a "Historical forecast · v1" badge | Watch in the next human read. Orchestrator |
| A-PRES1-17 | Cold reader (desktop) | The footer's "no additional runtime requests" sits beside a demo that downloads 57 MB. | The statement is about the report page, and is true | Say "this page makes no additional runtime requests". Orchestrator (copy) |
| A-PRES1-18 | Cold reader (phone) | Which interval level the interval score uses is not shown on the reading path; "released" reads as "the model in the demo". | Definitions in the terms follow §3.1; "released" is the registry's status | Add the level to the interval score's definition; define "released" beside the release rule. Orchestrator (copy) |

## PRES-3 (the publication of v4, 2026-09-30)

### PRES-2's recommendations R1–R7 (`docs/track-b/evidence/pres-2/integration.md`), one disposition each

| Recommendation | Disposition |
|---|---|
| R1 — A3 cards could state the question | Deferred. A question row would change the two published transition cards, which PRES-3 keeps byte-identical; each chapter states its question directly below. The v3 → v4 card has the same form, so a later presentation block can add the row to all three at once. |
| R2 — the startup line measures an earlier bundle | Carried to the Owner's post-deployment step. The page cites the public demo measured on 2026-09-29. The PRES-3 bundle differs from it only in nine gzip header bytes (A-PRES3-2), and the Owner's A6 checks re-measure the cold start after the Space commit (packet §8). A materially different start updates the record in the next build. |
| R3 — no audit-grade evidence row for the product topics | Deferred. PRES-3 may not change the product documentation (brief; A4). |
| R4 — data topic precision | Deferred, for the same reason as R3. |
| R5 — carried advisories A04, A05 and A07 | Deferred. This block does not change the MLflow UI's default view (A04) or v1's reconciliation (A05). v4's chapter states its evidence-class caveat once, in "What this result does not establish" (A07). |
| R6 — the build message prints a character count as "bytes" | Taken up. `scripts/build_pages.py` prints the UTF-8 byte count. |
| R7 — the Critic's reproduction order | Taken up. PRES-3's Integration Critic assignment builds the browser payload (`make wasm`) before pytest, as CI does. |

### New advisories

| ID | Source | Finding | Why advisory | Proposal |
|---|---|---|---|---|
| A-PRES3-1 | Lead | The `delu-generations` experiment description names the four parents published on 2026-09-28. It does not name CP-21, whose runs the upload adds. | Rewriting it is an experiment-level write, and the brief authorizes writes to CP-21's five runs only. The export pins the published text (`scripts/mlflow_export.py::EXPERIMENT_NOTE_CHECKPOINTS`), and the publisher refuses any other write. | Authorize one `set_experiment_tag` write for `mlflow.note.content` naming all five parents, then extend the pin. Owner |
| A-PRES3-2 | Lead | `make wasm` on 2026-09-30 produced bundle `9028a118…`, not PRES-2's `8007f0d2…`. The only difference is byte 9 (the OS field) of the gzip header of each of the nine booster files. This interpreter's `gzip.compress` writes 255 there; PRES-2's build wrote 19. The decoded boosters are bitwise identical, and the equivalence gate passes. | The model, card and every other file are unchanged; the served bytes differ only in a compression header. | Write the gzip header in `scripts/build_wasm_payload.py` explicitly, so the bundle is byte-identical across Python versions. Orchestrator (tooling) |
| A-PRES3-3 | Lead | CP-21's artifact manifest binds `scripts/mlflow_export.py` and two CP-21 test files by hash. Publication must extend all three, so PRES-3 exempts exactly those files from CP-21's byte-for-byte test. A companion test checks their reviewed bytes at `evidence/cp-21`. | The manifest stays a true record of the reviewed candidate, and every other bound file is still checked byte for byte. | A research checkpoint's manifest could leave out shared presentation code that its publication block is required to extend. Orchestrator |
| A-PRES3-4 | Lead | Playwright's WebKit build had been removed from its default cache after PRES-2. With the Owner's approval on 2026-09-30, PRES-3 reinstalled it inside the project, at `.local/tools/ms-playwright` (`PLAYWRIGHT_BROWSERS_PATH`). | Environment, not product. | Point the runbook's browser commands at the project-local browser path. Orchestrator (tooling) |
| A-PRES3-5 | Editorial review, PA1 | Standard §15 asks for the target line "with a met / not-met column and N" and does not say where the column sits. By the Owner's direction of 2026-10-01 the comparison chart labels each generation v1–v4 and draws no targets column; the column is the value table's "Both targets", which the chart's description names, and the target in words, its date and N stay on the reading path. | The page meets the clause as written; only its location is unstated, so a later checker could read it either way. | Note on the incorporated standard §15: "The met / not-met column may sit in the comparison's value table beside the canonical names, provided the chart's description points to it; the target in words, its date and N stay on the reading path." Owner |
| A-PRES3-6 | Lead | The v4 ladder's first label ran under its own interval mark on desktop: an interval chart drew each label on one line, wider than its column. The release check measures text against text, not text against marks, so it passed. | Repaired: the ladder wraps its labels inside their column (`build_pages.py::single_rows`, `wrap_labels`). | Extend the release check's overlap test to chart marks. Orchestrator (tooling) |
| A-PRES3-7 | Editorial review, recommendation 11 | The GFS attribution line names "the v3 research model's weather data"; v4 uses the same weather columns. | The text is the Owner's `DATA-LICENSE.md` wording, and it also feeds both Space cards and the v1 demo's `claims.json`: changing it here would change the reviewed bundle. The attribution itself (source, licence, modification) is present on every surface. | Extend the wording to "the research models' weather data, from v3 on" in `DATA-LICENSE.md`, then regenerate at the next Space deployment. Owner |

### The editorial review's recommendations (`docs/track-b/evidence/pres-3/editorial.md`), one disposition each

Its five violations, V1–V5, are repaired, each with a test in `tests/test_45_pres3_v4_publication.py`.

| Recommendation | Disposition |
|---|---|
| 1 — the ladder's "-0.00" tick | Taken up: `Scale.ticks` turns a signed zero into zero; a test refuses a signed-zero tick on the page. |
| 2 — the ladder's labels omit the missing-input rule | Taken up: the label and the chart's description carry C106's whole bundle; the labels wrap (A-PRES3-6). |
| 3 — "attribute" | Taken up: "Three study arms separate the change into steps, one at a time." |
| 4 — the change of interval method | Taken up: the transition card says the interval is the ratio's, and the bootstrap settings state both methods (P08, P18). |
| 5 — "three-block" undefined before the chapter | Taken up in the transition card. No headline term: the headline block must stay within the first screen. |
| 6 — the headline's rule in words | Deferred: the wording is P51's, the rule's four conditions are one route away ("Read them"), and a longer headline risks the first-screen placement. |
| 7 — the transition card's "Not established" | Taken up: "A gain over the August 2022 peak is not shown either: over those 17 days, v4's point error is higher than v3's." |
| 8 — "inputs" for "information" | Taken up in the change sentence and the change diagram; the card's "kept v3's inputs" stays, as the review notes. |
| 9 — coverage at one level only | Taken up: pooled coverage at the 50%, 80% and 95% levels, for v4 and v3. |
| 10 — 4.6's evidence line | Taken up: "A provenance and licence record and resource measurements, then one predefined comparison on identical hours" (research anchor §18.4). |
| 11 — the GFS attribution | Deferred to the Owner (A-PRES3-7). |
| 12 — a stale MLflow route | Taken up: a verified route is linked only while its runs are the registry's, and the final build refuses until the index covers them; the comparison's link returns with the index written after CP-21's upload. |
| 13 — the met / not-met column on the reading path | P25 updated; A-PRES3-5. Naming the tested rows that did not meet the targets in the sentence is deferred: the value table names every verdict. |
| 14 — "8 policies" counts references | Deferred: it predates PRES-3, and the census sentence says the chart's rows are not the census. |
