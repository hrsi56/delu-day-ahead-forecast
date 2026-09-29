# PRES-2 — local acceptance matrix

The plan's §8.3 matrix, with the record that evidences each row. Every record named here is committed
under `reports/presentation/release-checks/`; screenshots stay in `.local/artifacts/pres-2/` (local
evidence, not public proof). **Local** means the candidate served from this machine; **public** means
an anonymous read of a live service. Nothing here claims public behaviour of the new candidate: that is
P8, after the Owner publishes (`publication-packet.md`). Each JSON record's verdict fields were read,
not only the exit code (plan P5.8).

## Identities checked

| Output | Identity |
|---|---|
| `docs/index.html` | 1,684,252 bytes, SHA-256 `f36314e28811ed4b7ec41bc73dfd481ddb112815effabfc4e7b3ae74d8edab1d`, built at `f788f63` (the route-label repair); `rebuild_presentation.py` and `build_pages.py --final` reproduce it byte for byte. The page before that repair, `47c74c45…` (1,684,174 bytes), is the one the fresh reader saw and attempt 6 checked |
| Static Space bundle `dist/space-wasm` | 805 files, 44,164,910 bytes, `bundle_sha256` `8007f0d2a9c09a8c2c3182745dac6b38956a9a0ad8f58541f32472b674d5bb4e`; rebuilt from source by `make wasm` with the same hash; exact copy kept at `.local/artifacts/pres-2/space-wasm-8007f0d2/` |
| MLflow export `reports/presentation/mlflow-export/` | byte-identical to the published export (`mlflow_export.py --check`: "the committed export is current"); no upload needed |
| `reports/presentation/mlflow_index.json` | rewritten by `verify_mlflow_mirror.py index` from `pres-2-public-mirror.json` and `pres-2-public-mlflow-routes.json`; only its two verification timestamps changed |

## The matrix

The page-level rows cite the records made on the final page `f36314e2…` at `f788f63`. Attempt 6 and the
attempt-2 records, on the page before the route-label repair, give the same placements, chart sizes,
accessibility and discovery results.

| Area (§8.3) | Acceptance | Evidence | Result |
|---|---|---|---|
| Rules / candidate | Exact hashes; full effective clause list; final candidate and output identities | `baseline.md`; `content-packet.md` §1 and §6; the table above | met |
| Product | Released registry identity on all surfaces; twelve topics supported or qualified; no transplanted model evidence | `content-packet.md` §2; `test_43` (A4 tests with negative controls: undocumented released model, missing subject, another generation's record, frozen versus fold-5 SHAP); `verify_release.py` names and statuses on page, README, both cards and the export | met |
| Opening / placement | Headline in the first screen in both engines; each score named; terms, release rule and startup metadata; A2 with measured header | `pres-2-local-release-attempt-7.json`: headline bottom 800.6 / 801.3 px at 1440×900 and 628.6 / 628.7 px at 390×844; finding bottom 1702.6 / 1703.3 px against the A2 limit 1744 (N = 2, H = 900, h = 56) and 2381.5 / 2381.5 px against 2420 (N = 3, H = 844, h = 56); release rule and byline outside disclosures; consecutive screens in `.local/artifacts/pres-2/local-release-attempt-7/placement` and `cold-reader` | met |
| Transitions | v1→v2 comparator distinction and gap; v2→v3 direct evidence; rejected branches kept; nothing invented | `content-packet.md` §3–§4; `test_43` A3 tests (registry predecessors; negative controls for a missing start, a cycle, a non-generation predecessor, a double successor and date order) | met |
| Fair comparison | Bound hours and days, equal-fold method, metric, comparator, class | "7 policies · the same 10,747 historical hours over 448 days · error scores averaged with equal weight over five test periods · lower is better" (P07, bound to `cp20.metrics.B0.pooled.n_hours` / `n_days`); `test_43` F04 tests | met |
| Charts | Values, scales, units, interval kind, labels; phone variants; discoverable routes | `pres-2-local-charts-attempt-3.json`: 90 chart views at 1440, 390, 360 and 320 px, closed and open, no overlap or clipping, smallest text 12 px (each text's own screen transform); `discovery` in `pres-2-local-release-attempt-7.json`: 26 routes by mouse, keyboard and deep link, both engines, 1440×900 and 390×844; the rendered charts inspected by eye (`editorial.md`) | met |
| Browsers | Chrome and Playwright WebKit at 1440×900, 768, 390×844, 360, 320; emulated iPhone; versions | `pres-2-local-release-attempt-7.json`: Google Chrome 154.0.8037.58 through Playwright's `channel="chrome"`, Playwright WebKit 26.6; 768×1024, 360×780, 320×640 heights recorded; WebKit "iPhone 15" device emulation (393×659) | met |
| Accessibility | Named charts and controls; disclosure state; keyboard and focus; ~44 px targets; contrast; the demo's own widgets | report: `accessibility_trees` (Chrome's tree through CDP, WebKit's through its inspector protocol) and `keyboard_touch_contrast_zoom` in attempt 7: document order, visible focus everywhere, 0 targets under 44 px, 0 contrast failures at 1440 and 390; demo: `pres-2-local-demo-a11y-attempt-4.json`, both engines at 1440×900 and 390×844: no unnamed control in either engine's native tree (inside the widgets' shadow roots), no target under 44 px, slider, radio and menu operated by keyboard with visible focus | met, with the limits below |
| Zoom / reflow | 200% and 320 CSS px; emulation labelled | attempt 7 `zoom_and_reflow`: 1280 and 1440 at 200% and 320 px reflow, no overflow, disclosures closed and open, both engines; emulated, not a physical device | met |
| Offline / size | No runtime request, favicon 404 or console failure; one page ≤ 2.0 MB | attempt 7: `http_errors`, `failed_requests`, `console_errors` and `resources_after_document` empty in every view, served over HTTP; no words run together in any flex or grid container, closed or open (`collapsed_spaces`); `pres-2-local-f02-negative-control.json`: the published PRES-1 page's `/favicon.ico` request (404 in the server log) is caught through Resource Timing in Chrome; the candidate makes none; `verify_release.py` zero-fetch check; page 1,684,252 bytes | met |
| Demo | Cold starts in both engines on desktop and phone; level and scenario response; ready / loading / failure / retry; unchanged model equivalence | local: `pres-2-local-demo.json` (fresh contexts, ready in 9.6–11.2 s, level and scenario each changed the view, no console error or failed request); `pres-2-local-states.json` (asset failure, runtime failure and hang reach the failure state with the report link; retry reaches ready), both engines; `make wasm`: gate max deviation 0.0 on the 54-day fixture, three negative controls break it; public (the deployed PRES-1 bundle, read-only): `pres-2-public-demo-baseline.json`, four cold starts 18.3–20.0 s | met locally; public at P8 |
| Archive | Protected text and behaviour; old anchors; current documentation outside it | `test_38` (the `v1-archive` block byte-identical to `af0abb0`, 961,360 characters); old anchors resolve (`#data`, `#results`, `#forecast`, `#repro`, `#regimes`, `#spectral`, `#shap`); the archive replay keeps its colours and controls (`charts` `v1-replay`); product documentation sits in `#product` | met |
| Parity | Same headline, names, statuses, product limitations and valid links across surfaces | `verify_release.py` PASS; `pres-2-links-attempt-3.json`: every destination on the page, README and both cards resolves, the four gated DagsHub controls redirect to sign-in and are not advertised | met |
| Tracking | Exact mirror, histories, parents, artifacts, advertised routes, settled plots, anonymous | public, read-only: `pres-2-public-mirror.json` (23 runs, 6 REST routes, 0 problems); `pres-2-public-mlflow-routes.json` (6 routes × Chromium and WebKit, fresh anonymous contexts, expected run names present, comparison plots settled) | met (public, existing mirror) |
| Fresh reader | Separate agent, screenshots only, six fixed questions; answers 1–5 and placements checked; answer 6 advisory | `fresh-reader.md`: one context-free agent read only the 39 closed-state screens (Chrome 1440×900, then WebKit 390×844); answers 1–5 agree with the registry and derived records from the required placements, the metric of each headline value named correctly (A1); its one rendering defect is repaired and now checked | met |
| Independent review | Checker authored nothing; final candidate bound | `integration.md` | see that record |
| Public acceptance | Served identities and behaviour; F01–F04 closed by public evidence | not yet possible: P8, after the Owner's publication (`publication-packet.md`) | pending, Owner gate |

## Attempts, first failures and retries

| Record | Candidate | Outcome |
|---|---|---|
| release attempt 1 | working tree before `621d135` | The checker crashed in its discovery step before writing a record: it clicked an archive link inside the closed product manual. The screens it had taken are in `.local/artifacts/pres-2/local-release-attempt-1/`. Repair to the checker: a route that starts inside a topic is followed in two steps, the topic's route first |
| `pres-2-local-release-attempt-2.json` | working tree before `621d135` | **FAIL**: the new reliability chart's axis label "0.2" was clipped with disclosures open (every view); two standalone links under 24 px high; the `#product` route's landing test, which took a table inside the closed manual for the route's first result. Repaired in the page source (the chart's left padding; full-height `.quiet` links) and in the checker (the landing test scoped to the route's own heading level) |
| `pres-2-local-release-attempt-3.json` | after `926ac28`, before `d7338c0` | **FAIL**: the same two links under 24 px |
| `pres-2-local-release-attempt-4.json` | `d7338c0` | pass |
| `pres-2-local-release-attempt-5.json` | `66b29b1` | pass |
| `pres-2-local-charts.json` | `66b29b1` | **FAIL**: the product replay's text at 11.91 px at 320 px wide: the renderer drew into a width 2 px wider than the area inside the chart's border. Repaired at `a5bca2f` (drawing width = `clientWidth`); the checker now measures each text's screen transform, which includes the border |
| `pres-2-links.json` | `66b29b1` | **FAIL**: the link gate read `http://www.w3.org/2000/svg&#x27` from the inline icon as an address. Repaired at `a5bca2f` (the icon is base64), with a test and a negative control |
| `pres-2-local-release-attempt-6.json`, `pres-2-local-charts-attempt-2.json`, `pres-2-local-route-attempt-2.json`, `pres-2-links-attempt-2.json` | `a5bca2f`, page `47c74c45…` | pass |
| fresh reader (`fresh-reader.md`) | page `47c74c45…` | **Found a defect every check had passed**: three route labels in the v3 chapter drew their words together. Repaired in the generator (the label is one span) and made a release-check finding; `pres-2-local-collapsed-space-control.json` catches the three labels on that page in both engines and viewports and none on the repaired page |
| `pres-2-local-collapsed-space-control.json` | pages `47c74c45…` and `f36314e2…` | pass: the new finding catches the three labels on the earlier page in both engines and viewports, and none on the repaired page |
| `pres-2-local-release-attempt-7.json`, `pres-2-local-charts-attempt-3.json`, `pres-2-local-route-attempt-3.json`, `pres-2-links-attempt-3.json` | `f788f63`, page `f36314e2…` | pass, with the collapsed-space finding empty in every view |
| `pres-2-local-demo-a11y-attempt-1.json` | working tree before `621d135` | **FAIL**: in Chrome, ArrowRight left the interval level at 80%, and WebKit's run did not complete its keyboard step. The keys do operate the group (in attempt 4, Chrome: ArrowRight 80%, ArrowLeft 95%; WebKit: 95%, then 50%): the framework's roving focus does not start from the checked radio, and the published PRES-1 bundle behaves the same way. The check was corrected to record both arrow directions and to require that the level changes |
| `pres-2-local-demo-a11y-attempt-2.json`, `-attempt-3.json` | working-tree bundle before `621d135` | pass (attempt 3 added the visible-focus assertion) |
| `pres-2-local-demo-a11y-attempt-4.json` | bundle `8007f0d2…`, the one `621d135` first recorded | pass: every assertion on the final bundle |

Runs marked "working tree" were made on uncommitted states of the same branch before the commit
named; the timestamps in each record and its screenshots fix the order.

## Limits, stated as they are

- **No real Safari, no physical iPhone and no screen reader** were used. Playwright WebKit is the
  Safari engine, not Safari; the phone widths and the iPhone are emulated.
- **WebKit's accessibility tree** is read through WebKit's inspector protocol
  (`DOM.getAccessibilityPropertiesForNode`) over playwright-core's in-process connection, a private
  API of Playwright 1.63. It inspects the demo widgets inside their open shadow roots; it is not an
  assistive-technology test.
- **Chrome updated itself** from 153.0.8010.54 to 154.0.8037.58 during release attempt 3 (both versions
  appear in that record); every later record uses 154, and each record names its version.
- **The startup measurement on the page** (P34) is the public PRES-1 bundle's cold start, measured
  on 2026-09-29 and labelled as such. The new bundle differs by the control-name and target-size
  repair, the scenario slider's plain label and one card line, not in its model or payload; its public
  cold start is measured at P8.
- **Demo timings are local**: `pres-2-local-demo.json` is served from this machine, not Hugging Face.
- **Python**: every suite and build ran on CPython 3.12.14, the interpreter CI uses
  (`.github/workflows/tests.yml`). No Python 3.13 cross-run was made in PRES-2. MLflow warns that the
  champion was saved under Python 3.13.15, as it does in CI; the bitwise gate is unaffected.
- **Public behaviour of the candidate** is unverified until P8. The public observations above
  describe the services as they are now (PRES-1's deployment and the unchanged MLflow mirror).
