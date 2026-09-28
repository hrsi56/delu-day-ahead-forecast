# Verdict — PRES-1 — Integration — PASS

- Candidate SHA: `217f4f8bd84a14cbbebb35a26b232678d1197998`.
- Scope: **pre-F1 independent review**, the ordered gate in conformance brief §5.2. This PASS certifies the implemented W1–W15 pre-F1 artifact. It does **not** certify the completed PRES-1 checkpoint, F1–F4, W16, public mirror/routes, final visual approval, landing or deployment. Those remain pending and require the specified final focused recheck.
- Plan / version / bar: `docs/track-b/evidence/pres-1/publication-standard-v1.md`, version 1, §16, all §§1–15; SHA-256 `01d721c2ba6316ca9a2f707e79da229bef732e91bad22f6ce457fb01e69478cc` verified from candidate bytes. Supporting brief `docs/track-b/evidence/pres-1/pres-1-conformance-brief-2026-09-28.md` §§4,5,10,11, SHA-256 `51dd9b8685ea9feb774bd27a7d1241d7e678182dd93b1820cead686686d1f502` verified; presentation plan revision 3 §§6–12,16 as amended by standard §15; referenced capstone v21 §§6–8,14–15.
- Worktree: `/Users/djourno/Downloads/PJM/.local/worktrees/pres-1/check-5`, fresh clean detached candidate supplied by Lead. `git status --porcelain=v1` empty before and after; `git rev-parse HEAD` unchanged. Isolation is cooperative, not a read-only filesystem claim. No source or Git mutations. Reproduction regenerated identical tracked bytes. No Builder checkout, conversation, program state or Orchestrator role document was read.
- Verbatim bar excerpt, confirmed against the candidate (the excerpt is the citation):

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

All repository commands ran in the detached worktree above. Test/reproduction wrappers removed environment names containing TOKEN/PASSWORD/SECRET/KEY/CREDENTIAL and `MLFLOW_TRACKING_USERNAME` without printing values. They set `UV_CACHE_DIR=/Users/djourno/Downloads/PJM/.local/cache/uv`, `UV_PYTHON_INSTALL_DIR=/Users/djourno/Downloads/PJM/.local/tools/python`, `UV_PYTHON=3.12`, and `TMPDIR=/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-5`. Scratch below abbreviates that last path. No authenticated network request or public write was made by this Critic.

| Command | Exit | Observed |
|---|---:|---|
| `git status --porcelain=v1`; `git rev-parse HEAD` | 0 each | Empty status; exact assigned SHA, before and after |
| `uv sync --locked --dev` | 0 | Fresh locked environment, CPython 3.12.14 |
| `uv run python --version` | 0 | Python 3.12.14 |
| `uv run python scripts/build_wasm_payload.py` | 0 | 15,363,807 bytes / 14 files; 54-day, 1,296-row fixture; expected saved-model Python 3.13.15 / runtime 3.12.14 warning |
| `uv run pytest -q` | 0 | **944 passed, 7 skipped in 135.65 s** |
| `make verify` | 0 | All bound claims and four cutoffs agree; zero fetching references; headline/name/status parity passes |
| `make lint-publication` | 0 | Page 0 findings; README 0; template sources 0 |
| `uv run python scripts/mlflow_export.py --check` | 0 | Committed export current |
| `uv run python scripts/mlflow_publish.py --dry-run` | 0 | 23 registry-matched runs, 6,928 metric points, 55 artifacts; outbound scan clean; export current at candidate |
| `uv run python scripts/rebuild_presentation.py` | 0 | All surfaces rebuilt in 11.3 s; subsequent status empty |
| `python3 scripts/publication_guard.py tree` | 1, expected | Refuses `final: false`; required pre-F4 safety, not a completed-publication PASS |
| `.venv/bin/python <scratch>/independent.py` | 0 | Independent direct CSV/JSON recomputation: 32 source blobs match frozen tags; 9,025 evidence records, 60 derived records, 413 rendered identities, 470 raw DOM bindings and 737 rounded visible numeric bindings agree; actual chapter order and archive bytes pass |
| `.venv/bin/python -c "import sys; from pathlib import Path; sys.path.insert(0,'scripts'); import check_links; sys.exit(check_links.main(record=Path('/Users/djourno/Downloads/PJM/.local/tmp/pres-1/check-5/links.json')))"` | 0 | Anonymous destinations pass; repository UI controls redirect to login as expected |
| `PLAYWRIGHT_BROWSERS_PATH=/Users/djourno/Downloads/PJM/.local/tools/playwright/browsers /Users/djourno/Downloads/PJM/.local/tools/playwright/bin/python scripts/check_reader_paths.py release docs/index.html --shots /Users/djourno/Downloads/PJM/.local/artifacts/presentation/check-5 --out <scratch>/release.json` | 0 | `passed: true`; all 11 views, four engine accessibility-tree checks, keyboard/touch/contrast/zoom checks pass |
| `uv run pytest tests/test_10_cqr_order_statistic.py tests/test_22_wasm_equivalence.py tests/cp16/test_budget_inputs.py tests/cp16/test_saved_results.py tests/cp16/test_state_results.py -q -rs` | 0 | 36 passed, 6 skipped; independently identifies CP-16 skip reasons; CQR and WASM identity gates pass |
| `uv run python scripts/mlflow_export.py --diff-against af0abb0 --to 0f93205 --out <scratch>/registry-diff.json` | 0 | 155 params, 6,928 metric points, 39 datasets, 55 artifacts checked; 9 unchanged artifact digests and 46 reproduced by restoring identity; no substantive change |
| `git diff --stat af0abb0 6f08b95 -- docs/index.html README.md` | 0 | Empty: registry introduction preserves page/README bytes |
| `git diff --stat af0abb0 HEAD -- pyproject.toml uv.lock` | 0 | Empty |
| `git diff --name-only 1d80bbd HEAD` | 0 | Only `docs/track-b/evidence/pres-1/w3-w5-pre-review-checks.md`; recorded pre-review Python 3.13/3.12 checks cover identical artifact code |
| `git diff --name-only 4dbdfbb HEAD -- app space space-wasm scripts/build_wasm_space.py scripts/build_space.py src/delu_forecast/claims.py src/delu_forecast/registry.py` | 0 | Empty: recorded W12 Space inputs unchanged |

Read-only inspections also used `cat`, `sed`, `rg`, `git show`, `git log`, `git diff` and BeautifulSoup scripts for contracts, modules, tests, provenance and DOM. During scratch-script creation an accidental trailing `.local-not-a-command` returned 127 after the file had been written; no candidate file changed. The completed script was then executed successfully and its final run is retained. A preliminary display check identified v1's negative relative-improvement record displayed as positive **28.58% worse**; the final independent checker explicitly verifies that semantic sign conversion and its “worse” label.

The seven suite skips are explicit: five CP-16 charged production-verification tests without `CP16_LEDGER`, one CP-16 supplied-input identity test bound to the superseded v21-r3 anchor, and the optional ecCodes test module (`eccodes` is absent from the locked environment). No charged research replay was enabled. They are not seven newly certified tests. This Critic reran Python 3.12; the full Python 3.13 result (944/7) is the committed `w3-w5-pre-review-checks.md` record on artifact-identical `1d80bbd`, not a second independent 3.13 run. This is macOS execution, not a claim of Ubuntu CI execution.

## Evidence actually inspected

- Contracts and hashes listed above; `AGENTS.md`, `engineering-role.md`, templates §2 and `owner-decisions.md`, including delegated automated device checks and the separate F1 gate.
- `research.py`, `derived.py`, `registry.py`, `research_claims.py`, `publication_lint.py`, claim sources, chapter/generator and export/publisher/guard paths, verifier behavior, CI workflow and pre-push ordering; tests 29–42 and applicable release/identity tests.
- All 32 record-cited source blobs (direct file reads and Git tag identity), including CP-10/15/16/20 metrics, uncertainty, criteria, diagnostics and protocols. The independent scratch checker reads CSV selectors/JSON paths directly rather than treating `validate_all()` or test success as proof. It recomputes every derived formula using Decimal arithmetic, decision dates and original criteria rows. The CP-15 preregistration/date tests and history check passed.
- Claim maps `cp15-cp16-claims.md`, `cp20-claims.md`, `publication-claims.md`; rendered README and Space model lines, bound research HTML, actual chapter DOM, source-tied figure labels and the preserved v1 archive.
- `registry-zero-diff.md`, `w3-w5-pre-review-checks.md`, `conformance-checks.md`, `ci-py312.md`, `cold-reader-check.md`, capability/release/Space records, authentication correction and corrected precheck JSON, publication runbook, packet template and advisory log.
- Fresh browser measurements in `release.json` and screenshots: desktop Chrome screens 1 and 3; WebKit phone screens 7–9 and 11–13. They show labeled units, zero reference, paired 95% confidence intervals, distinct generation marks, explicit policy directions, readable phone variants and result/limitations/decision order. The automated run additionally measures every chart closed/open at all required widths.

### Independent results and applicability of retained records

All eight evaluated identities count once: each CP-15 arm has N=5 at 2026-09-16; each CP-16 arm has N=7 at 2026-09-23; v3 has N=8 at 2026-09-24. Only v3 meets both criteria. The validator now recomputes `tested` and `first_to_meet` from fresh rows; permutation, altered count/first flag, earlier passing source and simultaneous-decision negative controls pass. The claim map uses the same date-based semantics.

The standard's Appendix re-derives: v3 distances −14%/−17%, v2 −2%/−4%; v3 changes as shares of v2 −12% [−16%,−9%] and −14% [−17%,−11%]; ordinary/stress MAE v3 5.3–15.6/48.0, naive 8.6–30.5/86.9, v2 6.3–18.7/51.2, daily LEAR 6.2–19.2/54.0. These are equal-fold development quantities; no new fit or score was computed from predictions.

Actual v3/v2 DOM order is question/change → main chart/reading → limitations → dated decision → actual evidence links → details. The prior defective earlier evidence rows are absent. Archive bytes match `af0abb0`, SHA-256 `d4d19223559b89747d981bfea86f1bc64661149e842dfee96898ba2b60196021`. Page size is **1,558,081 bytes**, below 2 MB.

Fresh Chrome/WebKit headline bottoms are 774.6/775.3 px on 1440×900 and 604.6/604.7 on 390×844. Finding bottoms are 1765.6/1767.0 px (≤1800), and 2488.5/2490.1 (≤2532). Eleven views pass, with zero overflow/failed requests/console errors; smallest chart text is 12.21 px at 320, 14.58 px at 390, 12.38 px desktop. Both engines' own accessibility properties expose named controls/charts and disclosure expanded states. Keyboard focus, touch targets, text/non-text contrast and zoom/reflow pass. **No real Safari, real iPhone or screen reader was used.**

Cold-reader reliance is explicit: this Critic is not a fresh cold reader after reading the contracts. The prior two-reader record remains evidence for §11. I independently compared every `data-block` in its `c6dda1f` page with this candidate: all **58** claim blocks have identical text, and headline HTML is identical. Changed bytes are the already-recorded label/reproduction fixes and movement of chapter evidence rows after their decisions; the six questions' substantive answers remain supported. New browser measurements verify placements. This is continued applicability, not a fabricated new cold read.

W12 reliance is also explicit: the candidate's demo sources, payload source inputs, cards, registry and builders are byte-identical to the recorded `4dbdfbb` W12 inputs. I inspected the four fresh-context local demo runs in `2026-09-28-demo-w12.json`: Chrome/WebKit, desktop/phone, ready with controls changing the view, zero failed requests/errors, 10.1–11.7 s. The recorded bundle is `eb122883896d755fd3314b6b5d361c1f6d23e0251412edfeeeef5c6201b8aacb` (805 files; 315 asset references, none missing). I did not claim to rerun that complete browser demo or reproduce its Python 3.13 bundle in this review. The independent payload/equivalence and asset tests passed. F4 changes the card link inputs and therefore requires refreshed final bundle/check evidence.

Authentication: inspected code sends a no-redirect GET to the actual `.mlflow/api/2.0/mlflow/experiments/get?experiment_id=0` service, using only stored MLflow Basic variables. It emits state/status/identity booleans, not credentials, response data or exception text. Missing credentials, redirect, wrong experiment and error controls pass. The committed corrected authenticated record reports 200 and expected identity; that is retained evidence, not an authenticated request by this Critic, and proves read access rather than upload permission.

## Checklist verdict

### Conformance deliverables

| # | Item | Verdict | Evidence |
|---|---|---|---|
| W1 | Ratified copies and Owner decisions | PASS | Both hashes exact; delegation/F1 decisions recorded |
| W2 | Registry and zero-diff introduction | PASS | All required identities/kinds; H0=V2-H; tested surface/unknown-entry controls; original page/README bytes and identity-only export diff reproduced |
| W3 | Derived verdict/distance/N/date/change/range records | PASS | Independent 60-record arithmetic and date-count census; fresh validation/negative controls; claim map |
| W4 | Headline and opening | PASS | Exact mandated headline, matching README, adjacent definitions and release rule; fresh Chrome/WebKit measurements |
| W5 | Architecture/grammar/branches/archive | PASS | Actual slot and evidence order, generic renderer, both branch cards, archive hash, page size and retained tokens |
| W6 | Numbers/words/lint | PASS | 737 visible values checked; sign-preserving endpoint and full table value; p floor; zero lint findings and negative controls |
| W7 | Status rules | PASS | Registry-derived past-tense dated statuses; template-source lint and injected stale-status failure |
| W8 | Evidence tiers | PASS | URL classification, frozen type/date labels and evidence rows; stale frozen report state is explicitly qualified by freeze date |
| W9 | README/Space/parity | PASS | Generated glance/generation ownership; v1-specific limitations; shared model-line generator; missing-line and parity controls |
| W10 | Completeness guard | PASS, pre-F1 | No placeholder mechanism; unavailable links omitted; missing-index final-build refusal; secret guard first; actual non-final tree rejection. Final build pending |
| W11 | MLflow identity/export and ordered publication | PASS, pre-F1 | Registry-matched run contract, current export, dry-run, artifacts/digests and precheck controls. F1–F4/public routes **pending**, not certified |
| W12 | Space assets and startup | PASS | Unchanged-input W12 record, bundle/asset evidence, payload and equivalence tests; explicit retained-record reliance above |
| W13 | System stack line | PASS | Rendered from system-view data; source and test agree |
| W14 | Contract tests | PASS | Registry-matched export, semantic README differences and registry-driven markers; negative controls |
| W15 | Runbook/packet/advisory log | PASS | All adoption/branch/population/status touchpoints, fields, slots and routes accounted; test_42 and inspected template |
| W16 | Return-only template/v4 proposals | PENDING | Outside pre-F1 artifact; must appear in terminal return |

### Publication Standard clauses

| # | Item | Verdict | Evidence |
|---|---|---|---|
| §1 | Audience/reading contract/placements | PASS | Fresh first-screen and orientation floors; reading-path/definitions/release/byline checks |
| §2 | Evidence classes | PASS | Development/post-selection badges, separate v1 holdout class, released-v1 demo and qualified claims |
| §3 | Headline quantities and form | PASS | All formulas/counts/date/intervals independently rederived; no unregistered promotional ratio |
| §4 | Precision/plain terms/numeric lint | PASS | Independent display audit, exact tables, lint and each family negative control |
| §5 | Registry/status/comparability | PASS | Required fields, single identities, canonical surface derivation, mixed-population refusal |
| §6 | Architecture/chapter grammar/branch card | PASS | Actual ordered DOM; immutable v1 archive; 1.558 MB |
| §7 | Evidence tiers/links | PASS | Frozen report labels, row placement, audited targets; anonymous gate |
| §8 | README/card/MLflow/parity | PASS pre-F1 | Generated names/model lines/headline; final mirror index remains pending |
| §9 | Completeness | PASS pre-F1 | Fail-closed guard and omitted unverified routes; non-final candidate correctly cannot reach main |
| §10 | Device/accessibility checks | PASS | Independent 11-view/two-engine release run and own engine trees |
| §11 | Gates/cold reader/independent check | PASS pre-F1 | Full suite, negative controls, retained cold read with proven unchanged claim blocks, this independent candidate verdict; final focused review pending |
| §12 | Publication process/packet/runbook | PASS pre-F1 | Implemented packet/runbook and order; public/final steps remain pending |
| §13 | Governance/ratification | PASS | Ratified hashes unchanged; no governance writes by Critic; named Owner decisions retained |
| §14 | Carryover | PASS pre-F1 | Individual invariant table below; typed source bindings and archive preserved |
| §15 | Ratified amendments | PASS | Headline/target/order/endpoint/p floor/per-model limits/status/devices/readers/contracts/grammar applied |

### Presentation-plan invariants, as amended

| # | Invariant | Verdict | Evidence |
|---|---|---|---|
| 1 | Zero runtime calls | PASS | test_19; verify scan zero; fresh browser no failed requests |
| 2 | One v1 claim source | PASS | claims.py, payload, cross-surface verifier |
| 3 | Generator-owned output | PASS | Rebuild identical tracked bytes; generator/ownership tests |
| 4 | Exact v1 honesty statements | PASS | Preserved archive and release tests/claim agreement, including deficit/coverage/cutoffs/holdout qualifier |
| 5 | Per-model limitations | PASS | v1 demo/cards/README/chapter; v2/v3 limitations where presented; parity tests |
| 6 | `.mlflow` host | PASS | Link scan; publisher/verifier targets; repository UI only negative controls |
| 7 | Live namespace wall | PASS | test_24; no live action |
| 8 | Attribution/licensing | PASS | Site/README/cards include required source/license/GFS attribution |
| 9 | v2 wording and signed endpoint | PASS | +0.0000039 visible, +0.000003857628092332211 exact table, no significance claim |
| 10 | Research date boundary | PASS | Every applicable record window ≤2026-04-07; v1 published replay retained |
| 11 | Evidence labels and non-equivalence | PASS | Development label, historical NOT_DEMONSTRATED in detail, explicit no demonstrated joint preference/not equivalence |
| 12 | English/Owner presentation authority | PASS pre-F1 | English surfaces; final visual approval delegated and pending |
| 13 | Dependencies unchanged | PASS | pyproject.toml/uv.lock byte-identical to baseline |
| 14 | No retired governance tooling public copy | PASS | Rendered claim/stale-text scans and reading inspection |
| 15 | Units/comparators/aggregation/classes | PASS | Typed records/panels, mixed-unit rejection, chart labels and independent interval arithmetic |
| 16 | No placeholder ships | PASS pre-F1 | Final-build/guard negative controls; actual non-final tree blocked |
| 17 | Research numbers from evidence | PASS | 9,025 record audit, 470 raw/737 visible bindings; generator numeral guard |
| 18 | Generated README research span | PASS | Marker/ownership/idempotence tests and rebuild |
| 19 | Verified routes only | PASS pre-F1 | Unverified research MLflow links omitted; F3 verification pending before advertisement |
| 20 | Named public authority | PASS pre-F1 | No public action by Critic; F1 explicit Owner gate; later authority not inferred |
| 21 | No research budget | PASS | Committed-cell arithmetic only; charged production replay tests not enabled |
| 22 | No color/hover-only meaning | PASS | Direct labels, visible values, distinct shapes, zero references; screenshots and structure tests |
| 23 | Mobile variants/readable text | PASS | Fresh 390 and 320 measurements; stacked phone comparisons; minimum 12.21 px |
| 24 | v1 archive preserved | PASS | Independent byte comparison/hash to af0abb0 |
| 25 | Demo loading/failure/retry | PASS | Source/asset tests and applicable recorded startup/state checks; no fabricated progress |
| 26 | Planned work unscored | PASS | Separate post-chapter planned block; no version/scored/available-feature claim |

Withheld W1–W21 were inspected in the claim maps and checked against rendered blocks/README: H/P gains remain mixed, not equivalent; causal attribution is withheld; no product/economic/coverage guarantee or historical-oracle result is substituted; untested directions stay unscored; CP-20 weather claims follow its actually evaluated bundle, not an individual feature; the Integration review is not called peer review; demo identity remains v1; holdout always retains its qualifier. Tests exercise forbidden phrases and permit honest negations. No additional blocking claim was found.

## Remaining publication work and final state

F1 upload, F2 verifier-written index, F3 public mirror plus REST and Chromium/WebKit route checks, F4 final build, its refreshed bundle, and the focused final-candidate recheck are **pending**. The current build is intentionally non-final and must not be landed/pushed. W16 and the full return, Orchestrator's delegated visual decision, and authorized post-publication checks are not replaced by this verdict.

No new advisory finding beyond the existing log's narrow placement margins, private WebKit accessibility API and cold-reader observations. Interview-capture trigger: why a policy census must use recorded decision dates rather than CSV order, and why a service-specific authenticated read distinguishes an irrelevant account-API rejection from an MLflow credential failure. The Critic files no interview document.

Final `git status --porcelain=v1`: empty. Final HEAD: `217f4f8bd84a14cbbebb35a26b232678d1197998`. No branch/tag/worktree created or removed by Critic; Lead remains sole Git writer and owns checkout removal. Scratch/scripts/logs/screenshots stay under the assigned project `.local/` paths, with hashes below for retention. Approximate review elapsed time: 0.5 hours (rounded).

## Retained artifact hashes

```text
099d8c6497be92b91a7c0b3770bd85a22477ca0f3ecc4d05715df8e48b09e063  .local/tmp/pres-1/check-5/browser.log
4e8f0679393fcad4a75a130a6e5d5a49cf036c2975b06d1347f999a07aa61882  .local/tmp/pres-1/check-5/command-0.log
243be218907860cef2fc08e5f7706f83c66ec3ee0149aaef9ee11f2e6e1e45c7  .local/tmp/pres-1/check-5/command-1.log
cc875a1418077004d4099884052076816ef9b4c5f779dd8fb9839536e2f96329  .local/tmp/pres-1/check-5/command-2.log
7b3414fbfa2424e47b19c3bd407fcbfe6efd87410e59258d05ac25aa34b1502b  .local/tmp/pres-1/check-5/command-3.log
869ba42374b692ea4e3df8ac31b7557c3b063d7612029d893545e30e5b7e59b7  .local/tmp/pres-1/check-5/command-4.log
c6441bf526668add95c360a310cf4308ac28f0e556c5fc5d12424ea77ac4cd7e  .local/tmp/pres-1/check-5/command-5.log
9b8d917e52e3e288ffc4fb8356f42b2dfc9aeb2fa624f014ac582e81d796e922  .local/tmp/pres-1/check-5/command-6.log
02033a87f4647edb5eb6b3e55dca1f15146138fdc445614998c8f5b9304fc897  .local/tmp/pres-1/check-5/command-7.log
5ecdd2cccfa4eeba12f0ca0c44bfef4c026b13ec143feeb7ce549f5ebf54d21b  .local/tmp/pres-1/check-5/command-8.log
4c3569f5da09975434dd9fd9a91fadbc4367a91d8f3c3fab59e9241ab9ee4bd8  .local/tmp/pres-1/check-5/extra-0.log
f88f64f59706e013161ace8fef9c00c91c22cc5728fa7bdc98b18b41b640d727  .local/tmp/pres-1/check-5/extra-1.log
e2b749510a694771874525e69d7086f135e6221c1a9c42ef8076cc979cd80c79  .local/tmp/pres-1/check-5/extra-2.log
3563c20e3e16c38c08a330659508cbae5054174d4510e24d6108679aba44c23c  .local/tmp/pres-1/check-5/independent.log
004502a8ddb6ddc12ba4dbfe9f16d54d40f7c34c24d2f5627776833bf531ed4f  .local/tmp/pres-1/check-5/links.log
025eb5fab2181a5218031822b7733c98d160528f794bf4f3f0e60ba821a7a507  .local/tmp/pres-1/check-5/commands.json
d39af9b55ad2fc1867b768ca150c27e050e51b40e1b8d1a6d2360ee6c11e964f  .local/tmp/pres-1/check-5/links.json
997a96054c534a8ee56e1a081eddeb5ed4288b2caab74fb5471d059ac7b72d14  .local/tmp/pres-1/check-5/registry-diff.json
53635bc7b45a2bd5e75be8effd02c6fd71045582b6ae597137775a5250d6cbe7  .local/tmp/pres-1/check-5/release.json
03f5a7fe3836497a0558b8246e2d003f362094a075d8318db3e3286446fe0089  .local/tmp/pres-1/check-5/independent.py
f21c5dbb35781a8dfdde352774ce7da33039acc0b89dcfccacc7f9c54cd53a2f  .local/tmp/pres-1/check-5/screenshots.sha256
```
