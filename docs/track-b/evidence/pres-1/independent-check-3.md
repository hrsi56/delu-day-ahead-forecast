# Verdict — PRES-1 — Integration — FAIL

- Candidate SHA: `49cc9ac3e97b090a65a711f0b853b06e11aa1cc9`
- Plan / version / bar: `docs/track-b/evidence/pres-1/publication-standard-v1.md`, version 1, §16; conformance brief §4 W1–W15, §10–11; plan revision 3 §§6–12/16 as amended by standard §15.
- Standard SHA-256 verified: `01d721c2ba6316ca9a2f707e79da229bef732e91bad22f6ce457fb01e69478cc`.
- Plan SHA-256 verified: `281193740a256a99a1676d53ef61c9babb5f744a7d0fb038927e305d1149812c`.
- Brief SHA-256 verified: `51dd9b8685ea9feb774bd27a7d1241d7e678182dd93b1820cead686686d1f502`.
- Worktree clean before and after: **yes**; detached HEAD remained the candidate above. Checkout: `.local/worktrees/pres-1/check-4`, created by the Lead; no candidate-file edits, Git mutations, branch, tag, or worktree creation by this Critic. Reproduction rewrote generated files to identical bytes and produced ignored runtime byproducts.
- Isolation: procedural, not a read-only filesystem. No Builder checkout or Builder narrative was used. No `progress.md`, `orchestrator-role.md`, syllabus, or Track A/C material was read. The first template read accidentally included the surrounding canonical forms as well as §2; only §2's review contract informed this verdict.
- Scope: **the independent pre-F1 review**. F1–F4, W16, final visual approval, publication and post-deploy checks are subsequent ordered deliverables, not certified here. The Lead separately reported an authenticated read-only HTTP 403; this Critic made no authenticated call or credential workaround. That external blocker does not excuse the two artifact violations below.

## Verbatim bar excerpt

> **In force from ratification: every clause of §1–§15.** On 2026-09-28 the Owner instructed that the
> current state be brought to this standard "including everything". The PRES-1 conformance task
> therefore implements all of the following:
>
> - the registry, with derived names, statuses, comparators and comparability IDs, and MLflow names
>   taken from it;
> - the typed derived records and the headline block;
> - the §1 placements;
> - the chapter grammar and generic renderer, with v2 and v3 migrated and v1's archive untouched;
> - the branch card;
> - the §4 lint and the status lint;
> - the evidence tiers;
> - the README structure and cross-surface parity;
> - the completeness guard;
> - the §10 checks;
> - contract tests in place of tests pinned to content;
> - the runbook and the publication-packet template.

The excerpt was confirmed verbatim at the candidate SHA. It is the citation; line numbers below are only navigation aids.

## Findings

### F1 — W3 / standard §3.3(a): N is row-order dependent, and count records bypass re-derivation

`src/delu_forecast/derived.py:182–219` increments `tested` as it walks criteria-file rows. It therefore publishes A1–A5 counts of 1, 2, 3, 4, 5 and a v2 count of 6. The registry dates all five CP-15 decisions 2026-09-16 and both CP-16 decisions 2026-09-23; those were bounded multi-policy comparisons, not separate adoption decisions after each CSV row. The standard defines N as the policies tested against the same rule up to the decision, frozen at that date. On the recorded decision dates the counts are five for each CP-15 arm, seven for each CP-16 arm, and eight for v3. No inspected provenance establishes the sequential within-checkpoint decisions the implementation assumes. The erroneous earlier counts are also stated in claim P16 of `docs/track-b/research-content/publication-claims.md`.

The independent control reverses only the policy iteration order, leaving evidence and dates unchanged. A1's N changes from 1 to 5 and v2's from 6 to 7. This demonstrates that the derived record is not invariant to an irrelevant CSV ordering choice. The currently displayed **v3 N=8 is correct**; this finding does not dispute the headline's arithmetic.

There is also an unconditional validation hole: `derived.py:334–335` explicitly skips both `tested` and `first_to_meet` in `validate_all()`. Replacing the cached v3 count with `999` in memory returns an empty findings list. The required independent re-derivation of every typed headline quantity is therefore absent for these kinds. The fixture assertion that today's v3 count equals eight does not establish the contract for every policy or catch a corrupted count through the validator.

**Required acceptance:** derive counts from the evidenced decision boundary, independently recompute count and first-to-meet records, and add controls proving that (1) reordering source policy rows leaves every count unchanged, (2) a corrupted count and first-to-meet record each fail, and (3) the contemporaneous CP-15/CP-16 decisions have counts 5/7 while v3 remains 8. Rebuild the affected claim map and surfaces and obtain a fresh review.

### F2 — W5 / standard §6: chapter evidence is out of the fixed slot order

The standard's chapter grammar orders reading, limitations, dated decision, evidence row, then details. `scripts/build_pages.py:1645–1653` instead emits `slots.evidence` inside the main-chart figure, before both `not-established` and `decision`. Both v2 and v3's committed DOMs follow that order. `test_38` checks only the coarse `data-slot` sequence and does not include evidence's position, so the suite passes the wrong grammar.

**Required acceptance:** both generated chapters must have their evidence row after the dated decision and before details, with a DOM-order contract test that fails if the evidence row is moved before either limitations or decision. This is an explicit fixed-slot requirement, not a proposed redesign.

## Commands actually run

Commands ran in the detached candidate unless otherwise stated. Test/reproduction and browser processes received an environment with credential-like variables removed (matching TOKEN, PASSWORD, SECRET, CREDENTIAL, API_KEY, ACCESS_KEY, and MLFLOW_TRACKING_USERNAME); no values were printed. Scratch and pytest basetemp were under `.local/tmp/pres-1/check-4`. Shared uv cache and managed Python paths were the Lead-supplied `.local/cache/uv` and `.local/tools/python`.

| Command or exact executed operation | Exit | Observed |
|---|---:|---|
| `git status --porcelain=v1`; `git rev-parse HEAD`, before review | 0 | Empty status; exact candidate SHA |
| Python `hashlib.sha256(Path(path).read_bytes())` for the three controlling files | 0 | All hashes above match |
| `uv sync --locked --dev` | 0 | Locked environment installed; the resolved interpreter was Python 3.12.14 |
| `uv run python scripts/build_wasm_payload.py` | 0 | 15,363,807-byte payload; 14 files; 54-day fixture. Expected warning: champion saved under Python 3.13.15, running under 3.12.14 |
| `uv run pytest -q` | 0 | **927 passed, 7 skipped in 128.99 s** |
| `make verify` | 0 | Every bound claim agrees; zero runtime external fetches; headline, names and statuses agree across surfaces |
| `make lint-publication` | 0 | Page 0, README 0, template-source 0 findings |
| `uv run python scripts/mlflow_export.py --check` | 0 | Committed export is current |
| `uv run python scripts/mlflow_publish.py --dry-run` | 0 | 23 runs, 6,928 metric points, 55 artifacts; outbound scan clean; export current at the candidate SHA; no network write |
| `uv run python scripts/rebuild_presentation.py` | 0 | All surfaces rebuilt in 10.2 s |
| `git status --porcelain=v1`, immediately after rebuild | 0 | Empty: deterministic tree |
| `python3 scripts/publication_guard.py tree` | 1, expected | Rejects `reports/cp3/pages_build.json` with `final: false`. This is the required pre-F1 rejection, not an additional defect |
| `.venv/bin/python /Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-4/independent_numeric.py` | 0 | Independent direct CSV/JSON read of **9,025** evidence records, all source blob hashes and **470** DOM raw numeric bindings agree; primary arithmetic below; F1 counterexamples reproduced |
| `/Users/djourno/Downloads/PJM/.local/tools/playwright/bin/python scripts/check_reader_paths.py release docs/index.html --shots /Users/djourno/Downloads/PJM/.local/artifacts/presentation/check-4 --out /Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-4/release.json` with the supplied `PLAYWRIGHT_BROWSERS_PATH` | 0 | `passed: true`; all eleven views, four engine accessibility-tree checks, keyboard/touch/contrast/zoom checks pass |
| Anonymous link checker: import `scripts/check_links.py`; collect its destination URLs; `ThreadPoolExecutor(max_workers=8).map(C.probe, urls)`; then `C.main(record=Path('/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-4/links.json'), probe=lambda u: results[u])` | 0 | All destinations among 26 classified URLs resolve. Four repository-UI controls redirect 302 to login; no candidate report overwritten |
| Independent Python DOM extraction of v2/v3 `[data-slot]` and `.ev` positions | 0 | Both evidence rows occur before limitations and decision: F2 |
| `git show af0abb0:<path>` compared byte-for-byte to `git show 6f08b95:<path>`, for page, README and both Space cards | 0 | All four W2 introduction surfaces byte-identical |
| Independent extraction of the complete archive `<details>` from `af0abb0:docs/index.html` and candidate page | 0 | Byte-identical; archive SHA-256 `d4d19223559b89747d981bfea86f1bc64661149e842dfee96898ba2b60196021` |
| `git diff --quiet af0abb0 HEAD -- <path>` for `pyproject.toml`, `uv.lock`, `AGENTS.md`, `engineering-role.md`, templates, `capstone_v21.md` | 0 each | All unchanged |
| `git diff --name-only 4dbdfbb HEAD -- scripts/build_wasm_space.py app/wasm_showcase.py app/browser_champion.py space-wasm/README.md src/delu_forecast/claims.py` | 0 | Empty: inspected W12 source/card inputs unchanged since measured bundle |
| `git diff --name-only 5d8ce9b HEAD` | 0 | Only `docs/track-b/evidence/pres-1/conformance-checks.md` and `reports/cp3/link_check.json`; precheck code is candidate-identical |
| Final `git status --porcelain=v1`; `git rev-parse HEAD` | 0 | Empty; exact candidate unchanged |

The existing suite contains intentional production-replay/anchor exclusions, including CP-16 tests requiring a charged research ledger and its historical v21-r3 identity. Those are not secretly enabled here: the review has no research-replay budget. Seven skips remain explicit; they are not seven newly verified tests. The local Python 3.13 run and separate complete Python 3.12 CI-step run are evidenced in committed `conformance-checks.md`; this Critic reran the full suite on 3.12, not a second full 3.13 run.

### Independent numeric results

These were calculated with Decimal directly from committed CSV cells, without calling the headline formula functions. Sources: weather-ablation metrics/uncertainty; the policy-count comparison additionally uses criteria identities and their recorded registry decision dates.

| Quantity | Independent result | Published rounding |
|---|---|---|
| v3 point / interval distance from daily LEAR | −13.9934247076% / −16.7095223164% | −14% / −17% |
| v2 point / interval distance from daily LEAR | −2.0885597195% / −3.5933291357% | −2% / −4% |
| v3−v2, share of v2 point score | −12.1588089747%; CI [−15.6187087625%, −8.8547347208%] | −12% [−16%, −9%] |
| v3−v2, share of v2 interval score | −13.6050680550%; CI [−16.9444155170%, −10.6390666751%] | −14% [−17%, −11%] |
| v3 ordinary/stress MAE | 5.2539246025–15.6403099996; 48.0353856912 EUR/MWh | 5.3–15.6; 48.0 |
| v2 ordinary/stress MAE | 6.3108021102–18.7301457164; 51.2136229218 EUR/MWh | 6.3–18.7; 51.2 |
| Naive ordinary/stress MAE | 8.6331388889–30.5034148887; 86.9488731061 EUR/MWh | 8.6–30.5; 86.9 |
| Daily LEAR ordinary/stress MAE | 6.2192690831–19.2025018438; 54.0078246502 EUR/MWh | 6.2–19.2; 54.0 |

The direct record audit checked selectors and interval cells independently of `R.rederive`, using Python CSV/JSON readers and Git blob hashing. It checked source values, not new forecasts or new bootstrap draws; no new scoring or fitting was performed. Existing tests additionally check record units, populations, boundaries, claim-map membership, display precision and source/claim negative controls. F1 demonstrates the portion those tests miss.

## Evidence actually inspected

- Governing standard and conformance brief; owner decisions; applicable plan and capstone sections; engineering role and root rules.
- Registry entries, evidence classes, dated statuses, comparators and route/run derivation; `derived.py`, `research.py`, publication lint and claim maps, including W1–W21.
- Page generator's chart/scale/interval and chapter code, generated page, complete README generated blocks, both cards, and model-line parity code through the checks.
- All registered source cells and hashes from CP-10/15/16/20, CP-2 holdout/development evidence and resource/protocol JSON through the independent record read; the corresponding report headings and decision statuses. The stress period and peak-window distinction remain intact. The H−P positive endpoint remains positive and exact in the value table; the reading path shows +0.0000039.
- Publication guard, hook ordering and CI backstop; registry/lint/grammar/export/guard/runbook tests and their negative controls, executed as part of the suite.
- W2 zero-diff record and its record-level diff test; current deterministic MLflow export and dry run. No public mirror/index exists for F1–F4 at this stage.
- `conformance-checks.md`, `cold-reader-check.md`, committed §10 release JSON, W12 demo JSON, Space-state records and `reports/cp3b/space_wasm_bundle.json`; runbook, packet and advisory log.
- Fresh generated screenshots: Chrome desktop screen 1 and screen 3, WebKit phone screen 1 inspected visually. The release tool measured all chart variants with disclosures both closed and open at every required width, including no overlap/clipping and minimum text size. Current reading, record bindings and scripts were also inspected; this is not a claim of manual visual inspection of every pixel of every screenshot.

The fresh §1 placement results reproduce the committed measurements: desktop headline ends at 774.6/775.3 px and comparison finding at 1765.6/1767.0 px (Chrome/WebKit); phone headline 604.6/604.7 px and finding 2488.5/2490.1 px. Both satisfy the standard. No real Safari, real iPhone or screen reader was used; WebKit and the iPhone device are Playwright builds/emulation.

The existing cold-reader record names fresh screen-only readers and records all six questions, grading 1–5 against the registry and derived records. It predates three documented copy/spacing fixes; the binding headline and scientific quantities are unchanged, and the candidate measurements still pass. I did not misrepresent my now-informed reading as a new cold read.

W12's four cold starts record zero failed requests, level/scenario changes and ready states; the associated candidate inputs remain byte-identical. The committed bundle hash is `eb122883896d755fd3314b6b5d361c1f6d23e0251412edfeeeef5c6201b8aacb`. I inspected those records and source/asset contracts but **did not independently rebuild the full Space bundle or rerun its four cold starts**. Likewise I did not repeat the old local MLflow server rehearsal or any post-F1 mirror/browser route test. These limits are explicit, not fabricated fresh successes.

Audit links on the page use frozen/type/date labels and evidence rows. The old reports' “pending fresh exact-candidate Integration review” wording is frozen historical report state; current verdict links accompany it, and no active page claims the frozen report itself was edited to become current. The target/date and endpoint rules are enforced by the executed checks.

## Checklist verdict — conformance work packages

“PASS, recorded” means acceptance evidence was inspected and candidate identity checked, not that an unperformed check was rerun. “DEFERRED” identifies the ordered post-review deliverables; it is not a final-checkpoint PASS.

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| W1 | Immutable standard/brief copies and Owner decisions | PASS | Three matching hashes; owner-decisions records ratification, visual delegation, F1 scope |
| W2 | Complete registry, identity aliases, derived surfaces, final names and zero-diff proof | PASS | test_35/41; direct four-surface historical equality; export records preserve metrics/history/params and identity-restored artifact bytes; H0=V2-H |
| W3 | Typed derived verdict, distance, N/date, relative-score intervals, ordinary/stress ranges | **FAIL** | F1; all primary arithmetic matches, but prior N values depend on CSV order and count/first-to-meet validation is skipped |
| W4 | Exact headline, definitions, opening/orientation placements | PASS | Fresh two-engine release measurements; headline parity and exact §3.4 text |
| W5 | Section order, generic fixed-slot grammar, branches, archive and chart identities | **FAIL** | F2: evidence is before limitations/decision. Other components pass: generic renderer, branches, archive byte equality, 1,558,019-byte size, distinct markers |
| W6 | Numeric/word rules and four-family lint | PASS | Executed lint and negative controls; endpoint/p-value precision, unit/display bindings; no unbound reading-path numeral found |
| W7 | Registry-derived dated status and non-expiring template copy | PASS | Template-source lint and negative controls; registry status tests |
| W8 | Evidence tiers, frozen labels and no misleading active status link | PASS | Link classification/date tests, report-state inspection and fresh anonymous destinations |
| W9 | README ownership, per-model limitations, Space registry lines and parity | PASS | Generated top/list structure; test_21/32/39 and verify_release; Space required-line negative controls |
| W10 | Omit unverified routes, final-build completeness and publication guard | PASS pre-F1 | Missing routes omitted, no placeholder; final false correctly rejected; test_40 exercises real hook ordering and bad/missing inputs |
| W11 | Registry MLflow identity, source-of-truth description, verifier-written index and export contract | PASS local portion; F1–F4 DEFERRED | Current export and clean dry run; test_34 contract/controls. Public routes and index not certified |
| W12 | Ship/remove broken assets, extend asset contract, cold starts and bundle hash | PASS, recorded | test_23; asset scanner code; four committed cold starts zero failures; unchanged input proof and bundle hash; fresh bundle/cold-start rerun not performed |
| W13 | Data-derived stack line | PASS | SYSTEM_VIEW/stack_tools and page; test_38 |
| W14 | Contract tests replace run count, README difference phrase and marker-shape constants | PASS | test_34, test_30 difference-label checks, marker_problems contract and negative controls |
| W15 | Runbook, packet and advisory log | PASS | Files inspected; test_42 resolves touchpoints and registry/slot/menu/route vocabularies; negative controls |
| W16 | Landing-template/packet and v4 encoding proposals in return | DEFERRED | Return-only deliverable after this pre-F1 review; no locked template edited |

## Checklist verdict — standard clauses in force

| # | Clause | Verdict | Evidence |
|---|---|---|---|
| §1 | Reading contract, placements and tone | PASS | Fresh release report and cold-reader record; figures above |
| §2 | Evidence classes, badge and released/research distinction | PASS | Registry and page/README; v1 preview and demo distinguished from development headline |
| §3 | Pre-specified headline quantities and arithmetic | **FAIL** | F1; score shares/ranges/headline correct, per-decision N and independent count validation not correct |
| §4 | Precision, names, units, definitions and lint | PASS | Full lint/tests and direct bindings; exact values retained in detail |
| §5 | Identity/status/comparability registry | PASS | Entries, aliases, status history, comparability refusal and required-surface negative controls |
| §6 | Architecture and fixed chapter/branch grammar | **FAIL** | F2; otherwise fixed section order, branches, size and archive pass |
| §7 | Evidence tiers and frozen records | PASS | Type/date labels, target classifier and inspected frozen report states |
| §8 | README, limitations, cards, MLflow local identity and parity | PASS pre-F1 | Ownership, per-model limits and cross-surface agreement; verifier index awaits upload |
| §9 | Completeness | PASS pre-F1 | Omission and guard behavior verified; this is deliberately not a main-ready tree |
| §10 | Engine/device/accessibility release checks | PASS | Fresh full release JSON; no real-device/screen-reader claim |
| §11 | Offline gates, cold read, blocking rule and independent review | **FAIL** | F1 exposes an incomplete re-derivation gate despite green suite; this verdict does not permit F1 |
| §12 | Publication packet/runbook and order | PASS for current stage | W15; no upload/publication; subsequent ordered steps not claimed complete |
| §13 | Ratification and locked-core detection | PASS | Hashes and unchanged protected files |
| §14 | Carried-over invariants and evidence architecture | **FAIL in derived-record coverage** | F1; individual invariants assessed below |
| §15 | Ratified amendments applied | PASS except §6 implementation F2 | Headline, targets, planned order, endpoint/p-value changes and per-model limitation scope implemented |

## Checklist verdict — plan revision 3 invariants, as amended

| # | Invariant | Verdict | Evidence |
|---|---|---|---|
| 1 | Zero runtime network calls from report | PASS | test_19, verify_release and fresh browser request observations |
| 2 | Single v1 claim source; research evidence source | PASS | Claims payload rebuild and agreement tests |
| 3 | Generator ownership | PASS | Full deterministic rebuild, empty status |
| 4 | Exact v1 honesty statements | PASS | Claims/tests/archive equality; protected deficit/coverage/crossings/cutoffs/holdout statement preserved |
| 5 | Per-model limitations across applicable surfaces | PASS | test_21 and per-generation README/page/card inspection |
| 6 | Tracking uses `.mlflow` host | PASS | verify_release and fresh link gate; UI paths remain gated controls |
| 7 | Live namespace wall | PASS | test_24 |
| 8 | Attribution/licensing, including GFS | PASS | Surface agreement and page/card text |
| 9 | v2 language / positive endpoint / no significance, as amended | PASS | +0.0000039 reading path, full +0.000003857628092332211 in values; tests/maps |
| 10 | Research date boundary | PASS | Every applicable record-window test, direct committed sources; no new later-data research |
| 11 | Development labels, NOT_DEMONSTRATED, non-equivalence, descriptive economics | PASS | Maps and chapter/report wording |
| 12 | English and Owner presentation authority | PASS pre-F1 | English surfaces and recorded delegation; no publication performed |
| 13 | Dependency files unchanged | PASS | Direct Git comparisons |
| 14 | No retired-governance copy | PASS | Phrase tests and inspected surface text |
| 15 | Metric/unit/aggregation/comparator/class; one unit per axis | PASS | Typed records/series and mixed-unit negative controls; chart labels |
| 16 | No placeholder ships | PASS pre-F1 | No marker, omitted routes and rejecting guard; not ready for main |
| 17 | Evidence-only rendered research numbers | **FAIL in required derived verification** | Values are bound and match sources, but F1's counts lack the mandated independent derivation contract |
| 18 | Generated README ownership | PASS | test_32; idempotent rebuild |
| 19 | Routes advertised only after checks | PASS pre-F1 | New MLflow routes omitted; existing destinations checked; F3 not claimed |
| 20 | Owner review/instruction before public action | PASS for review | No public write; recorded prior approvals and delegated final review; this FAIL prohibits F1 gate |
| 21 | No new research budget | PASS | Arithmetic over committed records and prescribed tests only; no fits/scoring/retrieval commissioned |
| 22 | Meaning independent of colour/hover | PASS | Direct labels, distinguishable shapes, visible interval/values and table alternatives |
| 23 | Mobile variants and readable text | PASS | Fresh all-width chart measurement, including open disclosures, at least 12 px |
| 24 | v1 archive preserved | PASS | Independent byte equality and archive digest |
| 25 | Demo ready/loading/failure/retry states | PASS, recorded | test_23/state code, preserved recorded startup-state checks; not rerun against deployment |
| 26 | Planned work unscored/unversioned | PASS | Separate after-chapter planned section and tests |

## Acceptance and next boundary

The brief's §10 **overall PRES-1 acceptance is not met**: W3 and W5 fail here; W16 and F1–F4/final focused review remain later steps. The pre-F1 gate requires an independent PASS, so **this verdict does not authorize F1**, even if the separate credential blocker is resolved. A final checkpoint return cannot treat the green reproduction commands as a substitute for the two failed clauses.

- **Single largest meaningful gap:** N and first-to-meet are advertised as independently re-derived headline records, but the validator skips both; earlier counts are additionally tied to arbitrary CSV order. This is a claims-integrity gap, even though today's v3 headline happens to show the correct eight.
- **Exact next acceptance test:** in a repaired candidate, reversing every checkpoint's policy-row order must preserve all decision-date counts (CP-15=5, CP-16=7, v3=8), and independently corrupting either a `tested` or `first_to_meet` record must yield a validation failure. The same candidate must pass a DOM-order negative control for F2 and then the prescribed fresh review.

## Retained local material and time

No ref was created. Lead owns removal of `.local/worktrees/pres-1/check-4` after preserving this verdict. Ignored environment/payload/test byproducts in that checkout may be removed with that worktree. Review outputs retained:

- `.local/tmp/pres-1/check-4-verdict.md` (this file, for committing under `docs/track-b/evidence/pres-1/independent-check-3.md`).
- `.local/tmp/pres-1/check-4/`: command logs 0–9, commands JSON, independent numeric script/result, release/link logs and JSON, final-state JSON, pytest scratch.
- `.local/artifacts/presentation/check-4/`: the fresh release screenshots, including closed-disclosure cold-reader screen sets. These are local evidence, not the sole record of a required finding: findings and outcomes are written in this verdict.

Evidence SHA-256:

```text
7de7d16cea5d68ff10195b422ab5ff7ee9189a52682fd52d19f5e40ccc3eefbd  .local/tmp/pres-1/check-4/commands.json
24229fd838aae648c9bbccb579ed42b822bfe9f8f5fb0016e4266bdd7a1108c2  .local/tmp/pres-1/check-4/independent_numeric.py
33b777d6841e67db267ad9ebe551b64d783324cc2d5b9d16462db6cbb5dd1f32  .local/tmp/pres-1/check-4/independent-numeric.json
abb48fc244c60623f522c3f1d5afa7cbad4b7bd444ddb636401bd8cadad3c2b5  .local/tmp/pres-1/check-4/release.json
431827b6596daf92383b2f387d27910e09d68c5f8e88cdf39c053adb067ca220  .local/tmp/pres-1/check-4/links.json
b7cdf77004c61793931ee545a40491f849650bef9d1c98abdc77683e0f0b9cec  .local/tmp/pres-1/check-4/final-state.json
```

Approximate elapsed review: about 15 minutes (0.5 h rounded to the nearest half hour). No credential values displayed, public writes, new datasets, paid service or research runs. No post-return reads.

Interview-capture trigger: a green test suite did not protect a derived selection-count claim; an irrelevant row permutation and an intentionally corrupted record exposed the missing validation boundary.
