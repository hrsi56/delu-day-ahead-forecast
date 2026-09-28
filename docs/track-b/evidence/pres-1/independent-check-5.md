# Verdict — PRES-1 — Integration — PASS

- Candidate SHA: `a0302dd6c5ff6714709b4f3a3b742f71a4b596a7`.
- Scope: **full final Integration review, including F1–F4**, under conformance brief §§4,5,10,11. This is not a links-only recheck and does not reuse the pre-F1 PASS as the final verdict.
- Plan / version / bar: `docs/track-b/evidence/pres-1/publication-standard-v1.md`, version 1, §16, all §§1–15 in force. SHA-256 `01d721c2ba6316ca9a2f707e79da229bef732e91bad22f6ce457fb01e69478cc`; supporting plan revision 3 SHA-256 `281193740a256a99a1676d53ef61c9babb5f744a7d0fb038927e305d1149812c`; conformance brief SHA-256 `51dd9b8685ea9feb774bd27a7d1241d7e678182dd93b1820cead686686d1f502`. All three hashes independently checked from candidate bytes. Plan §§6–12,16 are read as amended by standard §15; capstone v21 §§6–8 and referenced portions of §§14–15 govern score/contrast semantics.
- Worktree clean before and after: **yes**, fresh detached `/Users/djourno/Downloads/PJM/.local/worktrees/pres-1/check-6`, unchanged exact HEAD. Isolation was cooperative, not an operating-system read-only mount. No source, governance or Git mutation; allowed reproduction regenerated identical tracked bytes. No Builder checkout, Builder conversation, program state, Orchestrator role document or later-checkpoint material was read.
- Terminal Lead return is an evidence-only follow-on under engineering-role step 7. The candidate's obsolete BLOCKED return is not certified as current; its W16 proposals were inspected. F5 delegated visual approval and F6–F8 publication/deployment/post-deploy actions remain the Orchestrator/Owner handoff, outside this Critic's execution.
- Verbatim bar excerpt confirmed at candidate (the excerpt is the citation):

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

## Commands actually run

All repository work used the detached checkout above. `S` below means `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6`; `A` means `/Users/djourno/Downloads/PJM/.local/artifacts/presentation/check-6`. The retained `S/run.py` strips environment names containing TOKEN/PASSWORD/SECRET/KEY/CREDENTIAL and `MLFLOW_TRACKING_USERNAME` without printing values; sets `UV_CACHE_DIR=/Users/djourno/Downloads/PJM/.local/cache/uv`, `UV_PYTHON_INSTALL_DIR=/Users/djourno/Downloads/PJM/.local/tools/python`, `UV_PYTHON=3.12`, `TMPDIR=S`, `PYTHONDONTWRITEBYTECODE=1`, and the supplied Playwright browser path. `S/wasm.py` uses the existing read-only root Python 3.13.15 environment, `PYTHONPATH=src`, its bin directory first in PATH, and the same credential stripping/temp containment. No authentication or public write was performed.

| Exact command (absolute scratch prefixes abbreviated S/A) | Exit | Observed |
|---|---:|---|
| `uv sync --locked --dev` | 0 | CPython 3.12.14; locked dependencies installed in isolated checkout. |
| `uv run python scripts/build_wasm_payload.py` | 0 | 15,363,807 bytes / 14 files; 54-day, 1,296-row fixture. Expected 3.13-saved-model/3.12-runtime warning. |
| `uv run pytest -q -rs` | 0 | 944 passed, 7 skipped in 167.49 s; all active tests pass. |
| `uv run pytest tests/test_10_cqr_order_statistic.py tests/test_22_wasm_equivalence.py -q` | 0 | 23 passed: named CQR order-statistic and WASM identity workflow checks. |
| `make verify` | 0 | Every bound claim and cutoff agrees; zero fetching references; headline/name/status parity passes. |
| `make lint-publication` | 0 | Page, README and template sources: zero findings. |
| `uv run python scripts/mlflow_export.py --check` | 0 | Committed export current. |
| `uv run python scripts/mlflow_publish.py --dry-run` | 0 | 23 registry-matched runs, 6,928 metric points, 55 artifacts; outbound scan clean; no writes. |
| `uv run python scripts/rebuild_presentation.py` | 0 | All five presentation steps and parity pass; subsequent tracked status empty. |
| `python3 scripts/publication_guard.py tree` | 0 | Final record; no placeholder; exit 0. |
| `git status --porcelain=v1` | 0 | Empty stdout. |
| `uv run python S/check_numeric.py` | 0 | Independent direct CSV/JSON and Decimal computation: 9,025 raw records, 60 derived records, 32 frozen tag blobs, 1,522 DOM bindings / 413 unique identities; all agree. |
| `uv run python S/display.py` | 0 | Independent decimal rounding of numeric DOM text agrees with source/derived values; see display.json. |
| `uv run python scripts/mlflow_export.py --diff-against af0abb0 --to 0f93205 --out S/registry-diff.json` | 0 | 155 params, 6,928 metric points, 39 datasets and 55 artifacts; 9 unchanged hashes, 46 exact old hashes after restoring identity; no substantive change. |
| `uv run python -c 'import sys; from pathlib import Path; sys.path.insert(0,"scripts"); import check_links; raise SystemExit(check_links.main(record=Path("S/links.json")))'` | 0 | All required destinations passed; gated repository UI controls redirect to login as expected. |
| `/Users/djourno/Downloads/PJM/.local/tools/playwright/bin/python scripts/check_reader_paths.py release docs/index.html --shots A --out S/release.json` | 0 | All 11 views, four native-engine accessibility-tree checks, keyboard/touch/contrast/zoom checks pass. |
| `uv run python scripts/verify_mlflow_mirror.py verify --target public --out S/mirror.json` | 0 | Anonymous verification: 23 expected/found, 560 histories / 6,928 points, 55 artifact hashes; params/tags/parents and six REST routes pass. |
| `uv run python scripts/verify_mlflow_mirror.py index --mirror-record reports/presentation/release-checks/2026-09-28-mlflow-index-prereq-mirror.json --browser-record reports/presentation/release-checks/2026-09-28-mlflow-routes.json --out S/index-reproduced.json` | 0 | Generated six routes, zero withheld; cmp against committed index exits 0, byte-identical. |
| `/Users/djourno/Downloads/PJM/.venv/bin/python scripts/build_wasm_payload.py` | 0 | Python 3.13 payload regenerated successfully. |
| `/Users/djourno/Downloads/PJM/.venv/bin/python scripts/verify_wasm_equivalence.py` | 0 | 11,628 values: max deviation 0.0, zero null mismatches; all three perturbations break the gate; causal masking holds. |
| `/Users/djourno/Downloads/PJM/.venv/bin/python scripts/build_wasm_space.py` | 0 | 805 files / 44,162,180 bytes; bundle b046c69b899bb9d5a2b2f9aeb3e5b3eebfdda820a419137ef5cdf8b8ac8f7c3d, exact match. |
| `/Users/djourno/Downloads/PJM/.local/tools/playwright/bin/python scripts/check_reader_paths.py demo --engine chrome --engine webkit --viewport 1440x900 --viewport 390x844 --url http://127.0.0.1:8821/ --out S/demo.json` | 0 | Four fresh cold starts, Chrome/WebKit at both viewports: ready in 10.2–11.8 s; controls respond; zero failed requests and console errors. |
| `/Users/djourno/Downloads/PJM/.local/tools/playwright/bin/python scripts/check_reader_paths.py states --engine chrome --engine webkit --url http://127.0.0.1:8821/ --out S/states.json` | 0 | Both engines: forced asset failure, runtime failure, hang/deadline and successful retry verified. Playwright route-cancellation cleanup warnings noted below. |
| `/Users/djourno/Downloads/PJM/.local/tools/playwright/bin/python scripts/check_reader_paths.py mlflow-routes --mirror-record S/mirror.json --shots A/mlflow --out S/routes.json` | 0 | Six routes in both Chromium and WebKit: intended names/IDs present anonymously; all pass. |
| `/Users/djourno/Downloads/PJM/.local/tools/playwright/bin/python S/settled.py` | 0 | Five comparison routes × two engines: three Plotly SVGs each, zero skeletons, missing expected content or HTTP errors. |
| `uv run python S/capabilities.py` | 0 | 39 dataset name/digest/context matches, 23 notes; v3 filter exactly cp20/HG; server 3.5.1. |
| `git rev-parse HEAD`; `git status --porcelain=v1`; `git diff --check` | 0 each | Assigned SHA, empty status/diff-check at final inspection. |
| `git diff --quiet af0abb0 6f08b95 -- docs/index.html README.md space/README.md space-wasm/README.md reports/cp3/pages_build.json` | 0 | Registry-introduction surface proof independently reproduced. |
| `git diff --stat 217f4f8bd84a14cbbebb35a26b232678d1197998..c8e8f1096471dff0ed8841cdf5a45ce571c89619` | 0 | Only the pre-F1 verdict, proving F1's export commit differs from its gate candidate by evidence only. |
| `cmp reports/presentation/mlflow_index.json S/index-reproduced.json` | 0 | Verifier-generated index is byte-identical. |
| `python3 -m http.server 8821 --bind 127.0.0.1 --directory dist/space-wasm` | Started; intentionally terminated | Served only the local final bundle; stopped after demo/state checks. |

Additional read-only inspection used cat/sed/rg, git show/log/diff, BeautifulSoup and hashes for contracts, source, tests, source records, DOM and evidence. An initial screenshot filename lookup failed (the files are named `screen-01.png`); a guessed `test_37_chapter_grammar.py` read failed (actual grammar tests are in test 38); a scratch inspection used the nonexistent export key `datasets` (actual key `inputs`) and was corrected. These inspection errors did not change candidate files or affect completed checks. The states driver exits 0 and records every expected state; it also emits asyncio CancelledError warnings as deliberately intercepted requests are cancelled during context cleanup. No such errors occurred in the ordinary four cold starts.

The seven skips are deliberate existing boundaries: optional ecCodes unavailable (one); CP-16 input identity tied to the prior v21-r3 anchor (one); charged production verification without CP16_LEDGER/CP16_REQUIRE_SAVED_EVIDENCE (five). No research fit, scoring pass or GFS download was enabled. Python 3.12 tests ran independently here; the full Python 3.13 suite is retained evidence in `final-checks.md` (944/7), not claimed as a second fresh full suite. The fresh 3.13 payload/equivalence/bundle and browsers were rerun here. This is macOS CI-equivalent execution, not Ubuntu CI.

## Evidence actually inspected

- Contracts, hashes and bounded governance listed above; Owner decisions, including D5 authority and automated device delegation.
- Evidence/derived/registry/claim/lint modules; chapter/generator, README/card generation, publisher/precheck, mirror/index, release driver and publication guard paths; corresponding tests 29–42, existing release tests and CI workflow. Full suite includes every negative-control family: wrong source/row/revision/unit/population/window; unmapped or undeclared numeral; missing registry surface; missing chapter slot; status/code/precision/percentage lint; unverified routes/placeholders; credential canary; export identity; and guard fail-closed conditions.
- All 32 record-cited source files and frozen blobs, including CP-10/15/v2-causal/weather-ablation CSV/JSON/protocol/resource files. `S/check_numeric.py` independently reads selectors/JSON paths and recomputes each formula without calling the production validators. Original criteria and landing dates establish the 5/7/8 counts; v2/H0 is counted once. Preregistration history tests pass. `S/display.py` separately checks displayed decimal rounding.
- Claim maps `cp15-cp16-claims.md`, `cp20-claims.md`, `publication-claims.md`, source reports, research updates, README and both Space cards; final HTML/DOM and screenshots. The near-zero H−P endpoint keeps its positive sign (+0.0000039; exact full value in table); v1's holdout p-value is floored on the reading path and exact in its table. No prohibited attribution, equivalence, qualification or significance claim was found on the research reading path.
- Publication runbook, packet template and advisory log; registry zero-diff proof; pre-F1 verdict; upload log, generated index, full mirror/routes/charts/capabilities records, final-s10/demo/states JSON, final-checks and cold-reader record. Historical local interruption/resume/corruption rehearsal and protected-namespace before/after metadata claims rely on retained records; no destructive public probe or redundant upload was performed.
- Final browser observations: headline bottoms Chrome/WebKit 774.6/775.3 desktop and 604.6/604.7 phone; comparison finding bottoms 1765.6/1767.0 desktop and 2488.5/2490.1 phone. These meet 900/844 and 1800/2532 floors. All measured charts have readable text and no clipping/overlap; no runtime report requests; native engine accessibility states/names, keyboard/focus, touch, contrast and reflow pass. No real Safari, iPhone or screen reader was used.
- Screenshots inspected directly: Chrome desktop cold-reader screens 1 and 3; WebKit phone screens 1,7,8,11,12; settled MLflow overview in WebKit and v3 in Chrome. Other required widths/routes are covered by the full measured records. All ten settled comparisons have actual plots, not loading skeletons, with intended run identities.
- The exact full v1 archive matches `af0abb0`, SHA-256 `d4d19223559b89747d981bfea86f1bc64661149e842dfee96898ba2b60196021`. All 58 claim-block texts match the cold-reader source at `c6dda1f`; placement is freshly measured. This supports continued applicability of the retained two-reader check; no fabricated new cold read is claimed.

## Checklist verdict

### Conformance brief W1–W16

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| W1 | Evidence copies and Owner decisions | PASS | Three required hashes match; delegated devices/visual approval and F1 authority recorded. |
| W2 | Complete registry, one identity, derived surfaces, introduction proof | PASS | Registry/tests35; independent original surface byte comparison and identity-restored artifact diff; F1 export identical. |
| W3 | Typed derived quantities, date/N/provenance, negative controls | PASS | All 60 recomputed from original rows; N=5/7/8; only v3 meets both; date/protocol/earlier-pass/reorder controls pass. |
| W4 | Exact headline, definitions and orientation placements | PASS | Same headline in README/page; direct definitions/release rule/byline; fresh placements satisfy floors. |
| W5 | Generic chapter grammar, lineage cards, preserved archive, tokens/size | PASS | Actual DOM order checked independently; limitations/decision precede evidence; archive exact; 1,560,646 bytes. |
| W6 | Precision/plain wording/unit rules and lint | PASS | Independent raw/derived/display checks, exact endpoint preservation, test37 family negative controls; zero lint findings. |
| W7 | Derived status and dated past tense | PASS | Registry tokens and template-source lint with synonyms/negative controls; no expiring current-state prose found. |
| W8 | Evidence tiers and frozen labels | PASS | Target-based classifier/test38; dated evidence rows; frozen report status caveats neutralised by explicit labels. |
| W9 | README ownership, per-model limits, Space parity | PASS | Generated glance/generations; v1 section; model limitations and verify_release/tests32/39. |
| W10 | Complete final build and fail-closed guard | PASS | Final:true; six expected/published routes, none omitted; guard exit0 and negative controls; secret guard remains first. |
| W11 | Registry-based MLflow, real mirror/routes and F1–F4 | PASS | Fresh 23-run mirror, metrics/artifacts/parents, generated index bytes, 12 route-engine checks, 10 settled charts. |
| W12 | Space assets, cold starts and exact bundle | PASS | 315 referenced assets present; exact 3.13 bundle hash; 4 cold starts and control responses with zero ordinary errors. |
| W13 | Stack line from system-view data | PASS | Renderer/test38 derives implemented tools; present in final page. |
| W14 | Contract tests replacing fixed content pins | PASS | Run set derives from registry, README contrast contract and marker-role contract; negative controls pass. |
| W15 | Runbook, packet, advisory log | PASS | Touchpoints match actual functions/registry/grammar; test42; status/population/branch and publication order covered. |
| W16 | Return-only template and v4 encoding proposals | PASS | Existing return's exact MLflow/packet blocks and amber diamond proposal inspected; locked templates untouched. |

### Publication Standard clauses in force

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| §1 | Reading contract, placement, tone | PASS | Fresh two-engine placements; headline/orientation/journey/deep routes; property-based development caveats. |
| §2 | Evidence classes, badge, status precedence | PASS | Registry/demo v1 and research v3 correctly separated; development vs one-shot evidence distinct. |
| §3 | Predefined primary scores, comparator, derived headline, context | PASS | Arithmetic matches Appendix: −14/−17%, −2/−4%, −12% [−16,−9], −14% [−17,−11]; ranges 5.3–15.6/48.0 and 8.6–30.5/86.9; N8. Future ratio/bootstrap/live triggers remain deferred. |
| §4 | Numeric/wording precision, signs, units, plain names, lint | PASS | Display checks and lint/negative controls; exact values retained in tables; archive exemption preserved. |
| §5 | Single registry, dated status, comparability, release rule | PASS | Registry identities and one-population chart guard; derived page/README/cards/export. |
| §6 | Section order, chapter grammar, branch card, size | PASS | DOM/renderer checks; newest-first; planned after chapters; archive preserved; under 2 MB. |
| §7 | Reader/audit evidence tiers and frozen destinations | PASS | Explicit dated labels and evidence-row placement; actual linked frozen reports inspected. |
| §8 | Surfaces, limitations, MLflow naming/index, parity | PASS | verify_release, cards/README inspected; experiment source-of-truth note; verifier index exact. |
| §9 | Complete-or-nothing publication | PASS | Real verified routes, final build, no marker; hook and CI fail closed. |
| §10 | Devices/accessibility | PASS | All 11 views, native AX properties both engines, keyboard/focus/touch/contrast/zoom and request checks. |
| §11 | Offline contracts, release gates, cold reader, independent gate | PASS | Fresh suite/release/link/mirror checks; 58-block equivalence establishes retained cold-reader applicability; this fresh final full review binds candidate. |
| §12 | Packet/runbook and ordered publication | PASS | Packet/runbook; pre-F1 gate → upload → verified index → capability acceptance → final build → this review; F5–F8 handoff explicitly unexecuted. |
| §13 | Ratified hashes/core/authority | PASS | Exact hashes verified; no governance edit or agent publication here. |
| §14 | Carried invariants and prior artifacts | PASS | All 26 rows below; source identity, no date-boundary expansion or new research. |
| §15 | Ratified plan amendments applied | PASS | Required headline/targets, planned location, precision/p-value and per-model limitation rules supersede prior formulations. |

### Plan revision 3 invariants, as amended

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1 | Zero report runtime network calls | PASS | test19, verify_release, fresh browser requests. |
| 2 | One v1 claim source and rebuilt payload | PASS | claims.py, parity and fresh payload/equivalence. |
| 3 | Generator owns output | PASS | Rebuild gives identical tracked bytes. |
| 4 | Exact v1 honesty statements | PASS | claims/tests21; immutable archive; DM deficit, crisis mechanism, crossings, cutoffs/staleness and exact qualified holdout label retained. |
| 5 | Per-model limitations on every presenting surface | PASS | Amended scope; tests21/39 and card/chapter/README inspection. |
| 6 | Tracking links use .mlflow host | PASS | verify_release, link controls and anonymous routes. |
| 7 | live_ namespace wall | PASS | test24 passes; no live namespace change. |
| 8 | Attribution and licensing incl. GFS | PASS | claims/card/page/README and tests. |
| 9 | v2 wording and positive near-zero endpoint | PASS | W1–W21 checks; +0.0000039 reading path; +0.000003857628092332211 exact table. |
| 10 | No v2+ data after 2026-04-07 | PASS | All records' boundaries/tests30; v1 protected replay only. |
| 11 | Development/NOT_DEMONSTRATED/non-equivalence/economics labels | PASS | Source reports/maps and rendered research text. |
| 12 | English and Owner presentation authority | PASS | English surfaces; D1 approval and explicit delegated final visual handoff. |
| 13 | Dependency files byte-identical | PASS | Direct bytes against af0abb0; locked sync. |
| 14 | No public retired-governance tooling text | PASS | Phrase guards and surface inspection. |
| 15 | Typed units, aggregation, comparator and class | PASS | Record validation, mixed-unit negative controls, figure subtitles/scales. |
| 16 | No shipped placeholder | PASS | Final record, build refusal tests and fresh guard. |
| 17 | Research numbers only from evidence layer | PASS | 9,025 source records/60 formulas and 1,522 DOM bindings, tests29/30. |
| 18 | Generated README research span | PASS | tests32 and deterministic rebuild. |
| 19 | Only verified reader routes advertised | PASS | Index/REST/browser routes and settled charts independently pass. |
| 20 | Review and explicit public-action authority | PASS | D5 and pre-F1 independent PASS preserved; no additional publication performed. |
| 21 | No research budget spent | PASS | Arithmetic only plus presentation/model-equivalence reproduction; no fit/scoring/download experiment. |
| 22 | No colour/hover-only meaning | PASS | Direct labels, distinct marks, visible values/table alternatives; screenshots and checks. |
| 23 | Dedicated phone charts and ≥12px text | PASS | All widths measured closed/open; phone variants inspected. |
| 24 | Original v1 archive text/behaviour | PASS | Full archive byte-identical; replay 95% and scenario controls covered by tests/browser release. |
| 25 | Demo loading/failure/retry states | PASS | Static states/tests23 and fresh forced-state/retry records both engines. |
| 26 | Planned work unscored/unversioned | PASS | Planned section/registry/rendered checks; no available-feature promise. |

### Ordered phases and final publication checks

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 0 | Demo diagnosis | PASS | Retained Owner device outcome/delegation; fresh desktop/phone-engine demo checks. |
| A | Content and claim maps | PASS | Three maps and frozen evidence; W1–W21 wording boundaries; no later data. |
| B | Evidence/binding layer and README ownership | PASS | Independent source/formula/display checks; tests29–32 negative controls. |
| C | Local tracking preparation | PASS | Current export/dry-run and inspected retained local 3.5.1 interruption/resume/idempotence/corruption evidence. |
| D1 | Specimen/tokens/reader approval | PASS | Owner decisions record D1 approval 2026-09-25; retained cold-reader record plus current applicability proof. |
| D2 | Full page/surfaces/states | PASS | Final page/cards/README, full suite, size/offline/AX/browser checks. |
| E | Review packet and clean CI-equivalent gates | PASS | Committed final 3.13 and clean 3.12 records; fresh independent 3.12 suite and final screenshots/export checks. |
| F1 | Authorized committed-export upload after independent gate | PASS | Independent-check-4 at 217f4f8; evidence-only c8e8f10; D5; upload log. All five current export files exactly equal F1's committed bytes. |
| F2 | Verifier-generated committed index | PASS | Index commit 2665381; regeneration from retained records byte-identical; fresh mirror maps equal; six routes, zero withheld, all IDs actual. |
| F3 | Anonymous public verification and capabilities | PASS | Fresh complete mirror; 39 inputs/23 notes/tag filter/server; intended route content in both engines and ten settled charts. Capability limitations stated honestly. |
| F4 | Final no-placeholder build and final review | PASS | Final deterministic build and exact bundle; guard passes; this full final verdict at a0302dd6. |
| F5 | Delegated final visual approval | HANDOFF | Reserved for the Orchestrator's own screenshot review after this return, per Owner decisions. Not claimed executed. |
| F6 | Landing/commit/push | HANDOFF | Owner/Orchestrator authority and review; not executed or authorized by this verdict. |
| F7 | Space redeploy | HANDOFF | Exact verified bundle handed over; no redeploy performed. |
| F8 | Post-deploy checks | HANDOFF | Requires F6/F7; local final-bundle checks are not labelled deployed-state proof. |

## Limits, findings and retained artifacts

No active-clause violation was found. Historical local rehearsal and original human/device outcomes are retained evidence, explicitly distinguished from fresh independent checks. The cold readers were agents, not humans. The F1 write counter's 710 excludes 23 set_terminated calls; the execution record correctly discloses that it is not a full HTTP-request count. No claim is made that protected namespaces received a complete historical-artifact census; retained before/after evidence covers metadata only.

One tooling observation is advisory: forced-route teardown emits Playwright cancellation warnings despite all expected state assertions passing; ordinary startup runs have zero errors. No source change is requested for that non-blocking observation. The existing editorial advisory log remains the place for non-bar improvements. Interview-capture trigger: final publication trust comes from independently matching the committed export to all public histories/artifact hashes and checking settled anonymous chart content, rather than treating an HTTP 200 or a loading skeleton as proof.

The Critic created no branch, tag or worktree. The Lead owns the assigned detached checkout and its removal. Scratch scripts/logs/JSON and screenshots remain under the assigned project-local S/A paths for preservation. The local HTTP server is stopped. Full HEAD/status were checked clean before this verdict was written outside the checkout.

### Scratch evidence digests

- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/build_wasm_payload-313.log` — SHA-256 `f98d5dd485726593943a907508068ba558a2230b5908692d4fc3cd28aeedcb03`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/build_wasm_payload-313.result.json` — SHA-256 `92a33e48a52af3742f6bdb7c20d9b448fc61b1c4540862d013f458c193176587`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/build_wasm_space-313.log` — SHA-256 `157e1f94553b13f3e14fe9ff0ec3ea8b9cccf210c42da978a651308c8431dbbe`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/build_wasm_space-313.result.json` — SHA-256 `58a1efdad14478ec0d7300e24852e8790d4a12566f9d5f6d2d490949549fa42a`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/capabilities.json` — SHA-256 `86adcd0a1695c56a7a5da3146388cdb37917cd3d3387d6c608f83a1cfb7f5452`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/capabilities.log` — SHA-256 `89d0da414212cb937d1724591df9353cee7d0f2133b0474351065be392344448`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/capabilities.py` — SHA-256 `b1f887ad8406abcf2e27d341c9544dd4f2f85d43de49b9591140272aa3e9571d`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/capabilities.result.json` — SHA-256 `7791f33dcd1cfbbe443892f8a531324b6519141d086474d9bd08632b696729e5`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/check_numeric.py` — SHA-256 `b4e89d4640d3b13289d7bf74f99b134059f70c6a878164c743cc42cab7160141`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/ci-specific.log` — SHA-256 `33080520bca22941903df3cd9bd553a8c66a7b4d68e5014b203cae7c8d51d086`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/ci-specific.result.json` — SHA-256 `d0bce6a3944fa25cb6e3482d56d2b83a117cee15666f0304e804d517ad30cd7f`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/demo.json` — SHA-256 `705b0563ac7ad8f1aa78e77ce80298b3fe6a45be2041844d8dcb6b47ddcc7904`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/demo.log` — SHA-256 `6d767cb416875b188d06aaefd087040bcf716e361233f12180d1613e332040e2`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/demo.result.json` — SHA-256 `4687f875e3465571ef0ac140de3eecab35b8fb56b87d7fead35f566e1da146c1`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/display.json` — SHA-256 `0be659f0a13eb6545b92b3c5967f93cb0efc7a8807ad740950a71766b11ea5e2`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/display.log` — SHA-256 `d99707a8ea9729a18073128630b54904a5d80581828b57203965463c1139ec1e`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/display.py` — SHA-256 `75c57a0a368bcc3b965b79824c98841a7a88de992c4e41c0ec6cd11af15a6109`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/display.result.json` — SHA-256 `419aa3fda99f325309aa026de494acc23061cbfcaae31ac6ba66dfb6e0855d11`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/dryrun.log` — SHA-256 `c0433534c6d20487671534b4ef15a0d4e1f533edb30ed37cfc5b628faf4b19c3`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/dryrun.result.json` — SHA-256 `3c8d0325739fad8667fc83ad178565cd64e2314f6abc13fbe058c561ee3d7be0`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/export.log` — SHA-256 `f4d98dee500c11d0b2451ae0a233c700d9e2c442bc67a1e3f4b7539037728bef`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/export.result.json` — SHA-256 `42ded8ba7c7d37cbb187a39f44585948301fb1cf4c01cab900e53bacd3dd714b`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/guard.log` — SHA-256 `e097b0ac2609bcbb3ca8d0c3dafe177e4dc56ac9e9ed9d4a1e679145e7510014`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/guard.result.json` — SHA-256 `bff9c89d04268fcff949f8577a0d22fcc26be041dd4fc586fe1ba3531182a86a`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/independent-numbers.json` — SHA-256 `5ff298e95e8273894be861fa52b3b4c5c90e6437c3d7fcf479f189fd1a8b59c9`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/index-reproduce.log` — SHA-256 `cb9b7c58b2fc11a9a32840df8e5e43d561bbd881aa80da13a92c418b4663cc19`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/index-reproduce.result.json` — SHA-256 `41ccd56855e86b4dfa37f2c9835d8df053b07143207e3a65dd910888a5c2c950`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/index-reproduced.json` — SHA-256 `1c5560442796108a92c0ee0319fe2cd7119cdf5d4f360b60151f8f99128ec173`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/links.json` — SHA-256 `f35f82078a5c802da7f1079611c752402d2da87c295a38f0d2e02316612d685e`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/links.log` — SHA-256 `f60ee4aae5e6ca2f99209b54fb48948e72f4849272e09f0d3326ddde3d385ce7`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/links.result.json` — SHA-256 `b991a925854d56be3d4442a4e617b7c38a73f41d04817d1b61ccfa9e21c37cc3`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/lint.log` — SHA-256 `869ba42374b692ea4e3df8ac31b7557c3b063d7612029d893545e30e5b7e59b7`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/lint.result.json` — SHA-256 `74eaf936dfdb68bdd775ed1d5ef9a2272e724703752032eaa19da9cf4a426e71`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/mirror.json` — SHA-256 `475dd57f08f3be469a772aaf1177d87d6896605194f6d5860087714bc6fe3408`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/mirror.log` — SHA-256 `23dd7a1840b421e645617684b9728626a208f2d7a16893af72eb1170637680c8`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/mirror.result.json` — SHA-256 `876432a4e9002e3e080493fc21a32bbdd62d19412f9327fabdcbc8a42782cef1`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/numbers.log` — SHA-256 `96420060833d02e75c47b6f38c81abff49d43de2cffb47f021cdf8f66167739d`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/numbers.result.json` — SHA-256 `e7ef354347a5da7bed3cf2c261574252483267d540a69ba31099cee992ba200b`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/payload.log` — SHA-256 `df13e0215b024c170e6b765e91181c790f72134057a05b5bc78da9ed58810144`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/payload.result.json` — SHA-256 `3a5aab7bb0991466f4295781320b7540d09f6eb4caebbbb269c48b09e1319f66`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/pytest.log` — SHA-256 `cd06ed82dc51882b62d24135a5a69a8da8d5a866c252b3a64b707c3325950c83`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/pytest.result.json` — SHA-256 `2be399a8a995f5d544dffcbb1d401bf61d619cdc17a374a9a960dff426b153ec`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/rebuild.log` — SHA-256 `c8f49a7c46f55165b3d9368c2847faf69d12766c38a454d2c8ef43d19ac515a8`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/rebuild.result.json` — SHA-256 `77ff4e978b87a5694a523ff00778d3970caf7d49724a015f4f94b3d9114c7594`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/registry-diff.json` — SHA-256 `997a96054c534a8ee56e1a081eddeb5ed4288b2caab74fb5471d059ac7b72d14`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/registry-diff.log` — SHA-256 `4106ba4f89dc0a49d969cca241098a55ac7817838856bbfcf60232fd2b255128`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/registry-diff.result.json` — SHA-256 `3866852ca23453098b5e396d5331a7af88863998462ace48fe55e421af1862c8`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/release.json` — SHA-256 `7303f83c4ae5861d711f81a0f5fad7d483f3255ceb74138bffe94cfcd6b3933f`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/release.log` — SHA-256 `cff503041aa0b11224a8fa345f0c1836ec2cc328152a442389b026a31245dc93`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/release.result.json` — SHA-256 `48a93ed4e39c7c16ee01793f61bf1fd9cab7d18784cb2152ea3324e6176ce0b9`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/routes.json` — SHA-256 `993adcbc586353b6071d0af9c51de28fb8794943a32453f6cb5a21d933f9c0e5`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/routes.log` — SHA-256 `9cff16b9bed19e8cee3e1b4000eb54b6417505ed5e701586be60cd8269737384`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/routes.result.json` — SHA-256 `b56f16210f14d11dff78a3f8b99fc49158b5d94293a1f3efb2074dccd63f6f4c`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/run.py` — SHA-256 `804721a894833ba91039237c25ac9782eb1309405bba048dd51c6b6185554e01`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/settled.json` — SHA-256 `4b7519a79383edbecca0eb06fc62a2e57f5d412632dc046defecad042adb8a05`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/settled.log` — SHA-256 `9c1210e7831bff0b9802f7a2d9089c7c259ce1f0cf7b9e51ec63cef444724aae`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/settled.py` — SHA-256 `2646356baca01765685e5f005b0d1ad616ec240eaf5e156ba8891a9df5acc58d`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/settled.result.json` — SHA-256 `9af4af8d7d2ec71922aaafd1e122c9c81b85bfc0ae25862c54337957b2eed879`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/states.json` — SHA-256 `fef538e242089d740df01f3c606fe235ada5e676c52eb121c31949cbb9786c32`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/states.log` — SHA-256 `29530bd8ccfad9236f684d80c82208836138aa25602befb85defca787fa5d77d`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/states.result.json` — SHA-256 `31a3587f1e47c236e2cfc0022af3b9d7f94580dba0c45d7d57c30aaea23c8f2c`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/status.log` — SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/status.result.json` — SHA-256 `5f32e44378739ab05611557066b40dd7ff9b48b0cf5d11f50be875876316fa24`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/sync.log` — SHA-256 `af611d8d870ae4ea984809c5999825393e2d7c8b96c81149907927643c631a7d`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/sync.result.json` — SHA-256 `b3a8b5792fde32267566c7bfd5bef546956748cca23def5fb5067887bd66c047`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/uv-d78c4024f0af21ba.lock` — SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/verify.log` — SHA-256 `8a59578a3c860053d36ad60a465b9ccf8356bf759e7194ea3ccdaf73400bdf71`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/verify.result.json` — SHA-256 `319ffddab0e37b8654c1becd8e4d069f97b3da505fc81cea6d965f2b99ad2b75`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/verify_wasm_equivalence-313.log` — SHA-256 `8dad56f5d607e287767239aaf273a9f31df4724c5e8cbb21e56493341b3b0003`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/verify_wasm_equivalence-313.result.json` — SHA-256 `4e6f887be0b84d445057e7043c6aa0ef0b681a549eeb4f72f5bcc4a21608b853`.
- `/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-6/wasm.py` — SHA-256 `f7d8c433de266976655b79440e95d2cc0f9a6e1c0ee296172e514fd8ee7b5898`.
