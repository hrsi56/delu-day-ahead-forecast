# Verdict — PRES-2 — Integration — PASS

- Candidate SHA: `d7d57e316a0afa198a2196bf4a2f1a3ac4a7c987`
- Plan / version / bar: `docs/track-b/publish-rules-migration-plan-2026-09-29.md`, revision 1 (SHA-256
  `24913b2b947aeef585e5994d61c91fed3c9eb0da830d6366c7f749e689b724c8`); bar cited in
  `docs/track-b/pres-2-execution-brief-2026-09-29.md`, "Complete authoritative checkpoint bar": `docs/PUBLISH_RULES.md`
  revision 1.0 in full (SHA-256 `03f106060d9a646ce0c0c986d2f5fb6549929f2ed7270f0c8678fbfd2293b3a3`) with its
  incorporated baseline, and the plan's §§1, 3–9 (especially §4, §5, §6, §8.3, §9).
- Verbatim bar excerpt (each confirmed present, byte for byte, in its file at this SHA):
  > ## Complete authoritative checkpoint bar
  > - Read PUBLISH_RULES in full. Every applicable clause is controlling, including
  >   all incorporated surviving baseline requirements and the A1–A6 amendments.
  > - Read the migration plan in full. Its complete outcome and acceptance contract
  >   is §§1, 3–9, especially the twelve-subject product map (§4), transitions (§5),
  >   phase exits (§6), complete acceptance matrix (§8.3) and definition of done (§9).
  >   §7's current touchpoints and implementation suggestions are aids; you own how
  >   to achieve the outcome. They are not a required module decomposition.
  > - A7/Live is deferred under its actual trigger, not marked implemented.
  > - Use docs/track-b/gauntlet-templates.md §§2–3 for Critic/return contracts.
  > - The checklist is not capstone_v21.md §12 (CP-15). That historical research
  >   checklist is not PRES-2's presentation acceptance and does not authorize fits.
  > - Map every applicable item to evidence. No convenience summary below reduces it.

  > **Local-ready milestone:** complete P1–P6/P7 artifact set, no local violation, appropriate tests
  > and independent final-candidate PASS, reviewed export/bundle and a concrete Owner publication packet.

  (brief, "Complete authoritative checkpoint bar" and "Observable outcome"; plan §9. The excerpt is the citation.)
- Worktree clean before and after: **yes** — `git status --porcelain` empty at start (05:58 UTC), after the rebuilds,
  after `make wasm`, after every check, at the end of the checks (06:29 UTC) and at the final pre-removal check
  (10:15 UTC); `HEAD` stayed `d7d57e316a0afa198a2196bf4a2f1a3ac4a7c987`.

**Scope of this PASS.** It is the independent final-candidate PASS of the **local-ready milestone** (plan §9) on the
exact candidate. It is not a deployed-migration PASS: the public surfaces still serve PRES-1 (Pages
`d1227c0f…`, Space revision `59d941825755bf73eabb7ff20e31124fee305755`), and P8's public acceptance, including the
public closure of F01–F04, can only follow the Owner's publication. Those rows are marked *pending P8*, not passed.

**Reviewer.** A fresh Integration Critic that authored none of the PRES-2 changes, working only in the clean
detached worktree `.local/worktrees/critic-pres-2` at the candidate SHA, with outputs under
`.local/tmp/pres-2-critic/`. No commit, push, upload, MLflow or Hugging Face write; `deploy_space.py` ran without
`--upload`; no credential value was printed, read or logged by me. `progress.md`, `orchestrator-role.md`, the syllabus
and Track A/C material were not read.

## Commands actually run

Environment for every `uv`/Playwright command: `UV_CACHE_DIR=.local/cache/uv UV_FROZEN=1 UV_OFFLINE=1
MLFLOW_DISABLE_AGENT_HINT=1 PLAYWRIGHT_BROWSERS_PATH=.local/tools/playwright/browsers`; `O=.local/tmp/pres-2-critic`.

| # | Command (worktree root) | Exit | Observed output |
|---|---|---|---|
| 1 | `git rev-parse HEAD; git status --porcelain` | 0 | `d7d57e3…`; empty |
| 2 | `shasum -a 256` of PUBLISH_RULES, plan, brief, independent review, AGENTS.md, standard v1, plan R3, capstone_v21.md | 0 | `03f10606…`, `24913b2b…`, `fa118734…`, `74d33d52…`, `ce276061…`, `01d721c2…`, `28119374…`, `150bd53f…` — every hash the brief pins matches |
| 3 | `uv sync --frozen --offline --python 3.12` | 0 | environment created, CPython 3.12.14 |
| 4 | `uv run --frozen --offline pytest -q` (prescribed position, **before** `make wasm`) | 1 | `3 failed, 1072 passed, 8 skipped, 12 errors` — all 15 in `tests/test_22_wasm_equivalence.py`, each "app/public/ is absent … make wasm-payload". Ordering artifact of a fresh checkout: CI (`.github/workflows/tests.yml`) builds the payload before pytest. Resolved by #15 |
| 5 | `uv run … python scripts/lint_publication.py` | 0 | `page: 0 finding(s)`, `readme: 0`, `templates: 0`; `PASS` |
| 6 | `uv run … python scripts/verify_release.py` | 0 | every bound claim on README, both cards, Pages export and MLflow record: `yes`; four cutoffs separate; `fetching references to an external origin: 0` over 1,684,252 bytes; no gated DagsHub link; `.mlflow` tracking URI everywhere; cross-surface parity `agree`; `PASS` |
| 7 | `uv run … python scripts/mlflow_export.py --check` | 0 | `the committed export is current` |
| 8 | `uv run … python scripts/rebuild_presentation.py` | 0 | README block, CP-3 section, export, page, agreement/zero-fetch `ok`; `git status` empty |
| 9 | `uv run … python scripts/build_pages.py --final` | 0 | page rewritten; `docs/index.html` SHA-256 `f36314e28811ed4b7ec41bc73dfd481ddb112815effabfc4e7b3ae74d8edab1d`, 1,684,252 bytes (the log's "1,683,280 bytes" is a character count, see recommendation R6); `pages_build.json` `final: true`, `bytes: 1684252` |
| 10 | `python3 scripts/publication_guard.py tree` | 0 | `the tree carries no placeholder and a final build record` |
| 11 | `git status --porcelain` | 0 | empty — every generated output reproduced byte for byte |
| 12 | `make wasm` | 0 | payload 15,363,807 bytes / 14 files; fixture 54 days, 1,296 rows, 11,628 values; `gate: max \|deviation\| 0.0, null mismatches 0`; controls `cqr_threshold_plus_0.01` 0.01, `median_head_599_of_600_trees` 0.427034, `p25_p50_heads_swapped` 50.2047 — each `broke gate True`; masked diff 0.0, D−1 control 220.9433; bundle 805 files, 44,164,910 bytes |
| 13 | `git status --porcelain` | 0 | empty |
| 14 | independent bundle hash: `shasum -a 256` of every file in `dist/space-wasm` (sorted by path), then of those lines | 0 | `8007f0d2a9c09a8c2c3182745dac6b38956a9a0ad8f58541f32472b674d5bb4e` (805 files) |
| 15 | `uv run … pytest -q` (payload present) | 0 | `1088 passed, 7 skipped` |
| 16 | `uv run … python scripts/deploy_space.py --bundle dist/space-wasm --expect 8007f0d2…` | 0 | bundle hash matches, 805 files, 44,164,910 bytes; `credential_guard: passed`; Space `sdk: static`, `private: false`, revision `59d941825755bf73eabb7ff20e31124fee305755`, `RUNNING`; `check only: nothing was uploaded` |
| 17 | `http.server` 8840 (`docs/`) and 8841 (`dist/space-wasm/`) on 127.0.0.1 | — | served page `f36314e2…`; served demo index `fcb0ed13…` = manifest `index_html_sha256` |
| 18 | `$PW scripts/check_reader_paths.py release http://127.0.0.1:8840/ --shots $O/release --out $O/release.json` | 0 | `passed: true`; 11 views, `problems` empty in each; discovery 26 routes pass in Chrome and WebKit at 1440×900 and 390×844 |
| 19 | `… charts … --out $O/charts --record $O/charts.json` | 0 | 90 chart views: no overlap, clipping or horizontal overflow; smallest text 12 px |
| 20 | `… route … --out $O/route --record $O/route.json` | 0 | both replays: 0.9398 at 95%, scenario caveat shown; product replay hides the observed line; text ≥ 12 px at 390/360/320 |
| 21 | `… demo --engine chrome --engine webkit --viewport 1440x900 --viewport 390x844 --url http://127.0.0.1:8841/ --out $O/demo.json` | 0 | 4 fresh-context runs ready at 10.2 / 9.6 / 11.7 / 11.7 s; level to 95% and scenario to ×1.01 each changed the view; 0 console errors, 0 failed requests |
| 22 | `… states --engine chrome --engine webkit --url http://127.0.0.1:8841/ --out $O/states.json` | 0 | both engines: asset failure → `failure` with the report link; retry → ready; runtime failure → `failure` (1.1 / 1.2 s); hang → `loading` at 1 min, `failure` after the deadline |
| 23 | `… demo-a11y --engine chrome --engine webkit --viewport 1440x900 --viewport 390x844 --url http://127.0.0.1:8841/ --out $O/demo-a11y.json` | 0 | `passed: true`; 12 controls per run, none unnamed, none under 44 px |
| 24 | `uv run … python -c "…check_links.main(record=Path('$O/links.json'))"` | 0 | `failed destinations: none`; 4 gated DagsHub paths 302 → sign-in, not advertised |
| 25 | `uv run … python scripts/verify_mlflow_mirror.py verify --target public --out $O/mirror.json` | 0 | `passed: true`, 23/23 runs, 6,928 metric points, 6/6 routes pass REST, 0 problems (06:17–06:22 UTC) |
| 26 | *additional, read-only:* `$PW scripts/check_reader_paths.py mlflow-routes --mirror-record $O/mirror.json --shots $O/mlflow-shots --out $O/mlflow-routes.json` | 0 | `passed: true`; 6 routes × Chromium and WebKit, anonymous, no sign-in redirect; each comparison view 3 settled plots, 0 skeletons |
| 27 | *additional:* `uv run … pytest -q -rs -p no:cacheprovider` | 0 | `1088 passed, 7 skipped`; skips: `eccodes` not installed (CP-20 decoding), CP-16 identity bound to v21-r3, 5 CP-16 ledger-charged verifications — none presentation tests |
| 28 | *additional:* `uv run … python predict_next_day.py --level 80 --self-check` | 0 | 24-hour forecast for 2026-09-06; coverage line 0.7593; self-check `passed: True` (masked 0.0; D−1 control 220.9433) |
| 29 | *additional:* `python3 $O/indep_numbers.py <worktree>` (reads the CSV/JSON sources directly, no project code) | 0 | 246 HTML `<data>` values and 122 SVG labels over 153 distinct records compared: **0 problems** |
| 30 | *additional:* `$PW $O/archive_behaviour.py http://127.0.0.1:8840/` | 0 | archive replay in Chrome 154 and WebKit 26.6 at 1440×900 and 390×844: ×1.02 removes the observed line and shows the caveat; 95% shows 0.9398; ×1.00 restores; `ARCHIVE BEHAVIOUR OK` |
| 31 | *additional:* archive/CSS/Owner-copy/fresh-reader identity scripts (Python, read-only) | 0 | see "Evidence actually inspected" |
| 32 | servers stopped; `git rev-parse HEAD; git status --porcelain` | 0 | `d7d57e3…`; empty; `main` still `01e394d…` |

## Evidence actually inspected

- **Governing text, read in full:** AGENTS.md; the brief; PUBLISH_RULES 1.0; the plan; Publication Standard v1;
  presentation plan revision 3; the 2026-09-29 independent review (F01–F04); `gauntlet-templates.md` §§2–3; the
  capstone v21 clauses the brief names (§§1–3, 6–8, 14–15).
- **Candidate diff:** `git diff --stat 01e394d..d7d57e3` (63 files); full diffs of `registry.py`, `research.py`,
  `research_claims.py`, `build_pages.py`, `build_wasm_space.py`, `deploy_space.py`, `README.md`, both cards,
  `app/wasm_showcase.py`, `docs/deploy.md`, runbook, packet template, both claim maps, `tests/test_38`, and the
  assertions and negative controls of `tests/test_43`/`test_44`; removed lines of every changed test and of
  `check_reader_paths.py` (none weakens a check; the A2 limits 1,744/2,420 are stricter than 1,800/2,532, and the
  MLflow route check now also requires settled plots).
- **Evidence packet:** every file under `docs/track-b/evidence/pres-2/` (baseline, content packet, acceptance,
  editorial, fresh reader, publication packet) and every committed `pres-2-*.json` release check (release attempts
  2–7, charts 1–3, route 1–3, links 1–3, demo-a11y 1–4, demo, states, F02 and collapsed-space controls, public demo
  baseline, public mirror, public MLflow routes). First failures are retained (release 2–3, charts 1, links 1,
  demo-a11y 1). My placements equal attempt 7 to the pixel.
- **Rendered pages, read by eye:** all 15 desktop (Chrome 1440×900) and phone (WebKit 390×844) closed-state screens
  1–3; the A2 captures (WebKit 1440 screen 2, Chrome 390 screen 3); product charts (SHAP 1440, coverage 1440 and
  320, replay 320); archive replay controls at 320; the product-replay route at 390; an anonymous MLflow v3/v2
  comparison (WebKit).
- **Independent recomputation from committed rows** (`weather-ablation/metrics.csv`, `uncertainty.csv`,
  `v2-causal/uncertainty.csv`, `cp2/regime_table.csv`, `reliability_three_stage.csv`, `holdout_report.json`,
  `diagnostics.json`): headline distances −13.99% / −16.71% → "14% / 17% below"; limits 0.59203 / 0.57509;
  v3 vs v2 −12.16% [−15.62, −8.85], −13.61% [−16.94, −10.64]; v2 vs daily LEAR −2.09% [−3.58, −0.81],
  −3.59% [−5.27, −1.85]; ordinary MAE v3 5.25–15.64, crisis 48.04, naive 8.63–30.50 / 86.95; 10,747 hours over 448
  days; B1 widths 41.53 / 75.47 / 130.86 EUR/MWh; every regime, reliability, holdout-coverage, SHAP and permutation
  value on the page.
- **Identity checks:** product sources' blobs equal the `evidence/cp-2` tag and the pins in
  `research.py::PRODUCT_SOURCES`; `scripts/cp2_diagnostics.py` L98–L167 confirms the frozen artifact is explained on
  fold 5's evaluation rows (`x_eval`), in sample, beside fold 5's out-of-sample model; CP-20's B1 pooled coverage
  equals CP-2's final development coverage exactly (so the width sentence describes the same intervals).
- **Preservation:** the `v1-archive` block (961,360 characters) is identical to the published PRES-1 page
  (`d1227c0f…`); its 49 archive-scoped CSS rules are unchanged; contribution, attribution, title, description and byline
  are identical to base; `reports/cp2`, `cp10`, `cp15`, `v2-causal`, `weather-ablation`, `mlflow-export` (tree
  `3e86afaa…` = main), `models/`, `data/`, `pyproject.toml`, `uv.lock`, `progress.md`, `.claude`, locked templates,
  PRES-1 evidence, advisory log (`d1cb5309…`) and landing record (`410475d2…`) are untouched.
- **Fresh reader:** the 39 supplied screens hash to the record's list and equal attempt 6's closed-state captures;
  the saved answer (12,008 characters) hashes to `6ea1a1bd…` and equals the committed verbatim block. The page it
  saw (`47c74c45…`) differs from the final page only by wrapping each "Explore these results" label in one `<span>`
  (token diff: 9 segments, no text change).
- **Server logs:** the report server received 46 requests, all `GET /` — no favicon or other asset; no 4xx/5xx on
  either server (the demo bundle ships its own `favicon.ico`, 200).
- **Owner packet:** README `3a16a70a…`, Static Space card `c92a2666…` (= bundle `README.md`), Space card
  `745bbb93…`, page and bundle hashes all match the packet; landing/publication order and P8 commands read.

## Checklist verdict

Legend: **PASS** — requirement met with the evidence cited; **Pending P8** — applies only after the Owner's
publication, not assessable on a pre-publication candidate and not claimed; **N/A** — trigger not reached, with the
reason. Recommendations referenced as R1–R7 are listed after the table and are not violations.

### A. The brief's bar and constraints

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| A1 | Governing identities pinned and present at the candidate (PUBLISH_RULES, plan, brief, standard v1, plan R3, capstone v21-r4, AGENTS.md, review) | PASS | Command 2; `baseline.md` §3; baseline commit `3702340` adds only the five exact copies |
| A2 | Exact-copy baseline only; no governance edit, `progress.md` not copied or staged | PASS | AGENTS.md at candidate = pinned `ce276061…` (the brief's exact copy); no other locked file changed; `progress.md` unchanged from base |
| A3 | Observable outcome: report, README, cards, demo and routes brought to A1–A6, research and history preserved, local work reviewed through a publication-ready handoff | PASS (local) / Pending P8 (public) | Sections B–D below; `publication-packet.md` |
| A4 | A7/Live deferred under its actual trigger, not marked implemented | PASS | `content-packet.md` §6 rows §7.2/A7 "no — deferred"; page shows "Live operation · planned" (dashed) and no live panel |
| A5 | Critic/return contracts per `gauntlet-templates.md` §§2–3 | PASS | This file follows §2 |
| A6 | Not the CP-15 §12 checklist; no fits | PASS | No research script run; `make wasm` only rebuilds the payload and proves the gate |
| A7 | Every applicable item mapped to evidence | PASS | `content-packet.md` §6 applicability matrix; `acceptance.md`; this table |
| A8 | Priority 1: subjects 1–12 documented for the released product right after the opening; follows a future product | PASS | B-§5, C-§4 rows; `PRODUCT_DOCS[released.id]`, `ProductDocsError` with negative controls (`test_43`) |
| A9 | Priority 2: v1→v2, v2→v3 as adopted transitions; rejected experiments separate | PASS (R1) | C-§5 rows |
| A10 | Priority 3: no invented paired v2−v1 interval | PASS | Card states "No paired interval for v2 against v1 exists"; values without an interval |
| A11 | Priority 4: metric names, header-aware placement, descriptive routes from the closed state | PASS | B-A1, B-A2, B-A5 rows |
| A12 | Priority 5: F01–F04 repaired | PASS (local) / Pending P8 (public closure) | Section D |
| A13 | Priority 6: graph/model/population identity; fold-5 SHAP vs frozen in-sample SHAP kept apart | PASS | Identity checks above; `test_a4_fold5_and_frozen_shap…` |
| A14 | $0; no research, fit, holdout opening, data acquisition, bootstrap, promotion, retraining or scheduler | PASS | Diff touches no research code/data; no downloads (`UV_OFFLINE`); registry statuses unchanged |
| A15 | Preserve date boundary, model and research artifacts, adverse facts, v1 archive, prior reviews, pinned dependencies | PASS | Preservation list above |
| A16 | Generators/claim sources changed; outputs regenerated; inference and bitwise gate preserved | PASS | Commands 8–15; `browser_champion_sha256` unchanged `9efb73f6…`; gate 0.0 |
| A17 | Stale ignored payload distinguished from the public bundle | PASS | Payload rebuilt fresh here (command 12); claims-parity test passes (command 15) |
| A18 | MLflow metric/history/artifact preservation; no historical SVG rewritten | PASS | Command 7; export tree = main; `test_41` in the suite |
| A19 | Temporary material in `.local/`; durable evidence in normal paths, attempts not overwritten | PASS | Records under `reports/presentation/release-checks/pres-2-*`, attempts numbered |
| A20 | Credentials rules | PASS | Guard reads values in-process only; nothing printed; anonymous reads anonymous (`urllib`, no auth header) |
| A21 | Chrome/WebKit width, accessibility, keyboard, contrast, chart, discovery, zoom/reflow, demo-state and link checks, rendered output inspected, local vs public distinguished | PASS (local) | Commands 18–26; screens read |
| A22 | Separate context-free fresh reader with the six questions; original answers saved | PASS | B-§10.2 row |
| A23 | Fresh independent Integration Critic in a clean detached checkout | PASS | This review |
| A24 | Final build/index before the exact-SHA review; one binding PASS | PASS | `docs/index.html`, `pages_build.json` and `mlflow_index.json` were last written at `f788f63` (the later commit `d7d57e3` adds evidence documents only); this review binds `d7d57e3`, whose tree reproduces those outputs byte for byte (commands 8–13) |
| A25 | Read-only verification of the unchanged public MLflow, no reupload | PASS | Commands 7, 25, 26 |
| A26 | First failures and retries retained; tool coverage limits disclosed | PASS | `acceptance.md` attempts table and "Limits"; records |
| A27 | No mainline write, remote mutation, upload, push or release | PASS | `main` = `01e394d`; check mode only |

### B. PUBLISH_RULES 1.0

| # | Clause | Verdict | Evidence |
|---|---|---|---|
| §1.1 | Sources and precedence; brief cannot relax the standard | PASS | Hashes pinned; no governing file edited |
| §1.2 | Four identities kept apart (rule revision, generation, product status, artifact) | PASS | Registry `released()` v1 vs `hero()` v3; `baseline.md`, packet identities; page: "Demo v1 · released LightGBM" beside "Research v3" |
| §1.3 | Applicability categories | PASS | `content-packet.md` §6 |
| §2 | Reader contract; reading path excludes closed bodies/tables; plain writing; caveat once | PASS | Screens read; lint 0 findings |
| §2-Headline | Target, numbers, class, demo model; whole block visible at 1440×900 and 390×844 | PASS | Headline bottom 800.6 / 801.3 (≤ 900) and 628.6 / 628.7 (≤ 844), both engines |
| §2-Orientation | Comparator, change, uncertainty, caveat above the chart; A2 limit | PASS | Finding 1,702.6 / 1,703.3 ≤ 1,744 and 2,381.5 ≤ 2,420; above chart (chart top 1,848.6 / 2,629.5); caveat directly below |
| §2-Definitions | Terms directly beneath the headline | PASS | Terms top 810.6 after headline 800.6 (Chrome 1440); `placement_findings` term rule |
| §2-Product identity | Why the demo runs this model, beside the action, outside disclosures | PASS | `release_rule_in_disclosure: false`, beside the action in every view |
| §2-Contribution | Byline route | PASS | `byline_in_disclosure: false`; "Led by … · Contribution" |
| §2-Journey | Ordered chapters and supporting sections | PASS | Screens 4–13 |
| §2-Depth | Labelled routes to values, runs, records, code, review | PASS | Evidence rows "…, frozen <date>"; "View values"; MLflow routes |
| §3.1 | Evidence classes kept apart; W1–W21; no significance/causal claims from development | PASS | Badges; product topics label one-shot, development and in-sample evidence; lint |
| §3.2 | Scores, named comparator roles, change as share with 95% interval, absolute MAE with stress period separate, one population, visible 10,747 h / 448 d, distinct interval kinds | PASS | Independent recomputation; "7 policies · the same 10,747 historical hours over 448 days · …" |
| §3.3 | Counting by declared rule; census vs rows; no hard-coded eight | PASS | Census sentence and exact census (A1–A5 2026-09-16; v2 and control 2026-09-23; v3 2026-09-24); `test_the_census_distinction_is_derived` |
| §3.4 | Provenance chain; precision; sign; p-value floor | PASS | 0 problems over 368 rendered values (command 29); lint 0; `p < 10⁻⁶`; `+0.0000039` |
| §4 | One registry for names/status; hero priority; research vs released separate | PASS | `verify_release.py` parity; status tokens; lint template family 0 |
| §4-A3 | Transition summaries for v2 and v3 | PASS (R1) | Both cards: predecessor with dated status, change, comparator (and whether it is the predecessor), result with 95% interval and class, not-established, dated decision, route |
| §4-Branches | Rejected branch cards, "Not adopted", reason, date, evidence, placed in time; none invented | PASS | "Experiments not adopted between v1 and v2" (calibration experiment, model comparison study); no v2–v3 group |
| §5-A4 | Eight-item order; product documentation directly after the opening; comparison before lineage | PASS | Order opening → `#product` → `#research-results` → `#journey` → chapters → planned → system → reproduce → contribution → attribution; `test_38` order tests with two negative controls |
| §5-Heading | Product heading not "About v1"; model visible as provenance | PASS | "How the product works"; lede names v1 from the registry |
| §5.1 | Twelve subjects for the actual product; dispositions; identity; archive not the only route | PASS | C-§4 rows; `content-packet.md` §2 |
| §5.1-Replacement | Replacement contract | PASS | `ProductDocsError` when `released()` has no topics (negative control); runbook §7a; packet §2.2 |
| §5.2 | Chapter grammar kept; one page; 2.0 MB | PASS | Chapters unchanged in grammar plus "Explore these results"; 1,684,252 bytes |
| §6 | Chart grammar, shared scales, no colour/hover-only meaning, labelled reference vs target, phone variants ≥ 12 px | PASS (R3) | 90 chart views clean; product charts: values printed, stage shapes, nominal line "a reference, not a target", mobile drawings |
| §6-A5 | Descriptive routes from the closed default state; ancestors open; heading below the sticky header; mouse, keyboard, deep link | PASS | 26 routes × 2 engines × 2 sizes, all three methods |
| §6-Navigation | Results · Journey · Evidence; no stacked sticky bars; deep links; archive return route; external marked | PASS | Screens; `↗` markers; old anchors land |
| §7.1 | Runnable model and why; replay vs inference; startup metadata beside the action; states; named controls | PASS (R2) | "Runs in your browser: about 57 MB … 18.3 s in Chrome 153 on a Mac, public demo, 2026-09-29; last verified 2026-09-29" (from `pres-2-public-demo-baseline.json`); commands 21–23 |
| §7.2-A7 | Future live only | N/A — deferred | No live product authorized; trigger not reached |
| §8 | Surfaces agree; README/card structure; MLflow index by verifier; report self-contained; attribution | PASS (local) / Pending P8 (served bundle) | Command 6; `mlflow_index.json` changed only in its two verifier timestamps; served-bundle check is P8 |
| §8-Routes | `.mlflow` host; anonymous REST and rendered destination | PASS | Commands 25–26 |
| §9-Engines | Chrome and WebKit, versions | PASS | Chrome 154.0.8037.58 (`channel=chrome`), WebKit 26.6 |
| §9-Widths | 1440×900, 768, 390×844, 360, 320, emulated iPhone, heights | PASS | 768×1024, 360×780, 320×640, iPhone 15 393×659 recorded |
| §9-Layout | Default and expanded, no horizontal scroll | PASS | `scroll_width = client_width` in 11 views; `overflow_with_disclosures_open` 0 |
| §9-Zoom/reflow | 200% and 320 px, labelled as emulation | PASS | 640×400 and 720×450 CSS viewports, 320×640; 0 overflow closed/open, both engines |
| §9-AX tree | Named charts and controls; disclosure state, both engines | PASS | Charts 4/14, controls 83/165 (1440), 80/162 (390), disclosures 18/25; 0 unnamed, 0 wrong state |
| §9-Keyboard | Order, visible focus, operation, unobscured targets | PASS | 83 stops in document order, none without visible focus; Enter toggles; anchors open closed disclosures |
| §9-Touch | ~44 px, framework widgets included | PASS | Report: 135 targets at 390, 0 under 44; demo: 12 controls per run, 0 under 44 |
| §9-Contrast | Text 4.5:1 / 3:1; non-text 3:1 | PASS | 3,147 / 3,135 text and 610 / 587 non-text items at 1440 / 390, 0 below, both engines |
| §9-Chart meaning | Units, direction, reference/target, interval kind, tables | PASS | Charts inspected; value tables present |
| §9-Demo | Cold start, controls, loading/failure/retry, return route | PASS (local) / Pending P8 (public) | Commands 21–22 |
| §9-Requests/links | No failed requests; no runtime network; valid destinations | PASS | 0 HTTP errors, failed requests, console errors, post-document resources in 11 views; server log 46 × `GET /`; command 24 |
| §9-MLflow | Mirror and settled charts, anonymous, both engines | PASS | Commands 25–26 |
| §9-Tools | Screenshots with context; real Safari/iPhone/screen reader not used and said | PASS | `release.json` `not_used`; WebKit AX via inspector API disclosed |
| §10.1 | Independent checker; three output kinds kept apart | PASS | This review; findings section below |
| §10.2 | Fresh reader: separate agent, closed screens only, six unchanged questions, answers preserved, answers 1–5 checked | PASS | Integrity checks above; answers agree with my recomputation; A1 mapping correct. The page it read (`47c74c45…`) differs from the final page only by one `<span>` around each of the "Explore these results" labels, the repair of its own observation 1 (no text change; answers 1–5 do not depend on it); the editorial re-read of the changed labels is recorded (`editorial.md`) |
| §10.3-A6 | Public identity and behaviour per surface | Pending P8 (local part PASS) | Public identities recorded pre-publication (`baseline.md` §4, packet §1; command 16) |
| §10.4 | Verdict discipline | PASS | Scope stated above |
| §11 | Packet contents (A3–A5 fields) and sequence | PASS | Content packet; publication packet; export unchanged so no upload; final build before this exact-SHA review |
| §12 | Baseline coverage map and invariants | PASS | Rows INV1–INV26 and the R3 clause rows below |
| §13 | Acceptance record | PASS | `acceptance.md` + this verdict; public row pending P8 |
| §14 | Maintenance and pending triggers | N/A — no trigger reached | No v4, v5 or size breach, final-candidate test or Live |
| §15-A1 | Each headline value names its metric | PASS | "14% below on the point-error score and 17% below on the interval score"; README identical; negative control on the PRES-1 wording |
| §15-A2 | N×H − (N−1)×h with the largest header; consecutive captures | PASS | h = 56; captures read (finding on desktop screen 2, phone screen 3, not under the header); negative controls in `test_43` |
| §15-A3 | Transition summaries | PASS (R1) | as §4-A3 |
| §15-A4 | Product documentation after the opening | PASS | as §5-A4, §5.1 |
| §15-A5 | Discoverable charts | PASS | as §6-A5 |
| §15-A6 | Public post-deployment evidence | Pending P8 | Packet §4 lists the per-surface commands and records |
| §15-A7 | Future live panel | N/A — deferred | as §7.2 |
| §16 | Authority record | PASS | No governance edit |
| §17 | Source identities | PASS | Pinned hashes match; runbook and template changed under plan P4.8 (not locked) |

**Invariants 1–26 (plan R3 §6 as amended; PUBLISH_RULES §12):**

| # | Invariant | Verdict | Evidence |
|---|---|---|---|
| INV1 | Zero runtime network | PASS | Inline `data:` icon; 0 post-document resources; server log |
| INV2 | One v1 claim source | PASS | `verify_release.py`; claim-parity test with fresh payload |
| INV3 | Generator, not output | PASS | Byte-for-byte rebuild (commands 8–13) |
| INV4 | v1 honesty statements exact | PASS | p = 0.948, 28.58% worse, 0.194, crossings 10,158 → 4,412 → 0, shipped = evaluated, four cutoffs and 152 days, "confirmatory-style, not power-qualified"; archive identical |
| INV5 | Limitations per model | PASS | Product topic "Limitations" with v1's full set; README v1 section; cards (parity) |
| INV6 | `.mlflow` host | PASS | `verify_release.py` |
| INV7 | `live_` wall | PASS | `test_24` in the suite |
| INV8 | Attribution/licensing incl. GFS | PASS | "Terms and attribution" unchanged from base |
| INV9 | v2 wording, near-zero endpoint | PASS | `+0.0000039` on the path, full value in the table |
| INV10 | Date boundary | PASS | No new v2+ number; product uses v1's published holdout (the D3 exception) |
| INV11 | Labels | PASS | Development / in-sample / one-shot labels; "not equivalence" |
| INV12 | English; Owner review | PASS | English copy; Owner approval is in the packet |
| INV13 | `pyproject.toml`, `uv.lock` unchanged | PASS | Not in the diff |
| INV14 | No retired-tooling narrative | PASS | No new mention; the one "Integration Critic" phrase is pre-existing v1 claim text |
| INV15 | Units | PASS | Axes and values carry units |
| INV16 | No placeholder | PASS | Command 10 |
| INV17 | Evidence-only numbers | PASS | Command 29; lint |
| INV18 | Generated README research | PASS | Markers; `test_32` |
| INV19 | Verified reader routes | PASS | Index from the verifier; 6 routes |
| INV20 | Owner review before public | PASS | Nothing published |
| INV21 | No research budget | PASS | — |
| INV22 | No colour/hover-only meaning | PASS | Shapes, direct labels, values |
| INV23 | Phone variants, text ≥ 12 px | PASS | Smallest 12.0 px across 90 views |
| INV24 | v1 archive text and behaviour | PASS | Identical block and CSS; behaviour (command 30); renderer change is the drawing width inside the border |
| INV25 | Demo states | PASS | Command 22 |
| INV26 | Planned work unscored/unnumbered | PASS | Planned block unchanged |

**Surviving plan R3 clauses (PUBLISH_RULES §12):**

| # | Clause | Verdict | Evidence |
|---|---|---|---|
| R3-7.5 | Analytical-panel grammar | PASS | Product panels: title/finding, subtitle (metric, population, class), labels with units, reference line, finding and qualification |
| R3-7.9 | Visible fairness population | PASS | 10,747 hours over 448 days, equal-fold, development |
| R3-7.10 | Anchors open disclosures; no stacked bars; archive return | PASS | Discovery and keyboard results |
| R3-7.11 | Startup metadata beside the action; states in the static HTML | PASS (R2) | Opening screen 1; first paint `loading`, static text "Starting the v1 demo…" |
| R3-7.12 | Contrast, zoom, reflow | PASS | §9 rows |
| R3-9 | Claim/evidence layer | PASS | Product sources blob-pinned (`PRODUCT_SOURCES`), claim map P33–P50, `test_29`/`test_30` |
| R3-10 | MLflow verification | PASS | Commands 25–26 |
| R3-16 | Owner decisions (names, contribution, visual tokens) | PASS | Owner copy identical to base; tokens unchanged |

### C. Migration plan §§1, 3–9

| # | Item | Verdict | Evidence |
|---|---|---|---|
| §1 | Outcome, authority, scope (1.1 identities, 1.2 inclusions, 1.3 deferrals) | PASS (local) / Pending P8 | Identities match; A7, promotion, retraining, v4/v5 deferred; demo remains v1 |
| §3.1 | Closed default page order and content | PASS | Screens: opening; product routes; comparison; evolution; planned; depth; contribution |
| §3.2 | Product and research legible as different things | PASS | "Demo v1 · released LightGBM" / "Research v3 · weather features"; product heading without "v1" |
| §3.3 | Placement and size feasibility | PASS | A2 met; 1.68 MB of 2.0 MB |
| §4-1 | Data | PASS | Target, sources, snapshot dates, cutoffs, windows, quarter-hour handling, no live feed; matches `data/README.md` (R4) |
| §4-2 | Regimes | PASS | 4,319 / 2,112 / 4,316 h; 465 h on 85 days — `regime_table.csv` |
| §4-3 | Features | PASS | 25 inputs grouped from `champion_card.json`; exclusions with the pre-registered comparison (+0.371516%) and benchmark (−19.4926%) |
| §4-3b | Seasonal rationale | PASS | 24 h, 168 h, 12-h harmonic — `spectral_peak_bins.csv` and archive §3b text |
| §4-4 | Validation | PASS | Five folds, one-day embargo, three baselines (`development_metrics.csv`), one-shot holdout, classes, leakage controls (0.0 / 220.9433) |
| §4-5 | Results | PASS | Holdout MAE, pinball, DM label, coverage 0.4407 / 0.7593 / 0.9398; development deficit; replay scores 1.052 / 0.986 |
| §4-6 | Attribution | PASS | Frozen artifact's in-sample SHAP on fold 5's rows, labelled; fold-5 OOS alongside; Spearman 0.98, 10/10 |
| §4-7 | Importance/sensitivity | PASS | Fold-5 development model's permutation importance (8.3 / 1.8 / 1.4), rank agreement 0.69, no causal claim; ceteris-paribus probe |
| §4-8 | Where it fails | PASS | Crisis 141.0 [123.1, 160.4], 0.555 of 2,112 h; peak 0.194 of 408; negative-price 0.710; fold models, not the frozen artifact, stated |
| §4-9 | Reliability | PASS | Stage coverage (holdout 0.8394 / 0.9398 / 0.9398; development 0.6705 / 0.8416 / 0.8452); widths 41.5 / 75.5 / 130.9; holdout width absent, said |
| §4-10 | Forecast | PASS | Product replay with level and scenario controls; historical replay label; demo bitwise on 54 days |
| §4-11 | Limitations | PASS | Summary plus v1's complete set and floor change |
| §4-12 | Reproduction | PASS | Documented command verified (command 28); identities; `make wasm`; container marked historical |
| §4-Identity | Frozen SHAP vs fold-5 distinction | PASS | Code-level confirmation; labels; `test_43` |
| §5.1-v1→v2 | Comparator ≠ predecessor, gap disclosed, no new ratio | PASS (R1) | Card fields; −2% [−4%, −1%], −4% [−5%, −2%] vs daily LEAR; descriptive 1.052 / 0.644 and 0.986 / 0.616 without interval |
| §5.1-v2→v3 | Direct predecessor comparison bound | PASS (R1) | "From v2 to v3: adding weather forecasts"; −12% [−16%, −9%], −14% [−17%, −11%] |
| §5.1-Records | Predecessor as validated metadata | PASS | `Entry.predecessor`, `transition_problems()` with five negative controls |
| §5.2 | Rejected paths preserved and headed apart; counts not conflated | PASS | Branch group heading; census sentence |
| §5.3-1 | Overall comparison | PASS | Overview visible by default |
| §5.3-2 | Weather across periods | PASS | "Did weather help in every test period?" → `#v3-per-period-differences` |
| §5.3-3 | Absolute errors | PASS | "Absolute errors per test period, for v1, v2 and v3" |
| §5.3-4 | By hour | PASS | "Errors by hour of the day, v2 against v3" |
| §5.3-5 | Crisis | PASS | "What happened in the 2022 crisis window" |
| §5.3-6 | Reliable or wider | PASS | "Did the intervals get more reliable, or only wider?" |
| §5.3-7 | v2's control | PASS | "What the pooled-interval control established, …" |
| §5.3-8 | Product works/fails | PASS | Twelve product routes; old anchors kept, `product-` prefix, no collision |
| §6-P0 | Baseline contains the controlling text; incoming work safe | PASS | `3702340`; main at `01e394d` with its incoming files |
| §6-P1 | Content packet; sourced sentences; correct graph identity | PASS | `content-packet.md`; claim map P33–P50; my source checks |
| §6-P2 | Structure fits floors, A2, size | PASS | Final measurements |
| §6-P3 | Report complete; F02–F04; generated only | PASS | No placeholder; byte-for-byte rebuild |
| §6-P4 | Demo and companion surfaces agree; F01; instructions current; export unchanged | PASS | Commands 6, 7, 16, 23; `docs/deploy.md` |
| §6-P5 | Local acceptance, tests not weakened, JSON verdicts read | PASS | Commands 15, 18–26; removed test lines are A1/A4 amendments only |
| §6-P6 | Editorial, fresh reader, independent review | PASS | `editorial.md`, `fresh-reader.md`, this verdict |
| §6-P7 | Mirror verified without reupload; final artifacts frozen; exact-SHA review; Owner packet | PASS | Commands 7, 25, 26; hashes; `publication-packet.md` |
| §6-P8 | Owner publication and public acceptance | Pending P8 | Owner gate |
| §6-P9 | Future replacement/Live interface only | N/A — future | Runbook §7a; no placeholder live panel |
| §7 | Change boundaries (immutable/out-of-scope files; legacy manifests) | PASS | Preservation list; `pages_build.json` and `space_wasm_bundle.json` are current build manifests, PRES-1 values kept in history |
| §8.1 | Rebuild and offline checks | PASS | Commands 5–15 |
| §8.2 | Browser and public-service checks (local substitutes now) | PASS (local) / Pending P8 (public) | Commands 18–26 |
| §8.3-Rules | Exact hashes, clause list, output identities | PASS | Commands 2, 9, 14 |
| §8.3-Product | Released identity on all surfaces; twelve topics; no transplanted evidence | PASS | Command 6; C-§4 rows |
| §8.3-Opening | First-screen headline, named scores, terms, rule, startup, A2 | PASS | B-§2 rows |
| §8.3-Transitions | Comparator distinction, direct v2→v3, branches, nothing invented | PASS | C-§5 rows |
| §8.3-Fair comparison | Bound hours/days, equal-fold, metric, comparator, class | PASS | Command 29; comparison subtitle |
| §8.3-Charts | Values, scales, units, labels, phone variants, routes | PASS | Commands 19, 29; discovery |
| §8.3-Browsers | Engines, widths, iPhone, versions | PASS | `release.json` |
| §8.3-Accessibility | Names, disclosure state, keyboard, 44 px, contrast, demo widgets | PASS | Commands 18, 23 |
| §8.3-Zoom/reflow | 200% and 320, emulation labelled | PASS | `release.json` |
| §8.3-Offline/size | No request, favicon 404 or console error; ≤ 2.0 MB | PASS | Command 18; server log; 1,684,252 bytes |
| §8.3-Demo | Cold starts, controls, states, equivalence | PASS (local) | Commands 12, 21, 22 |
| §8.3-Archive | Text and behaviour retained; old anchors; documentation outside | PASS | Command 30; identity checks; `#data`, `#results`, `#forecast`, `#repro`, `#regimes`, `#spectral`, `#shap` land |
| §8.3-Parity | Headline, names, statuses, limitations, links agree | PASS | Commands 6, 24 |
| §8.3-Tracking | Exact mirror, parents, artifacts, routes, settled plots, anonymous | PASS | Commands 25, 26 |
| §8.3-Fresh reader | Separate agent, screens only, six questions; 1–5 checked | PASS | B-§10.2 |
| §8.3-Independent review | Checker authored nothing; final candidate bound | PASS | This verdict |
| §8.3-Public acceptance | Served identities/behaviour; F01–F04 closed publicly | Pending P8 | Packet §4 |
| §9-Local-ready | P1–P7 artifacts, no local violation, tests, independent PASS, reviewed export/bundle, Owner packet | PASS | This table |
| §9-Migration complete | Publication, matched public identities, public checks, new postdeploy PASS | Pending P8 | Not claimed by the candidate (`acceptance.md`, packet) |
| §9-Failure handling | Recovery identities; no force-push, rewrite or MLflow deletion | PASS | Packet §5 |

### D. Findings F01–F04 of the 2026-09-29 independent review

| # | Finding | Verdict | Evidence |
|---|---|---|---|
| F01 | Demo slider and menu unnamed; small menu target | PASS locally / Pending P8 publicly | Chrome and WebKit native trees through the shadow roots: slider "Load-forecast scenario: × the day's load forecast, every other input fixed", radio group "Prediction-interval level", radios "50 %"/"80 %"/"95 %", menu "Notebook menu" 44×44; keyboard moves slider and radio, menu opens/closes; identity bitwise (gate 0.0) |
| F02 | Public favicon 404 | PASS locally / Pending P8 publicly | Inline base64 icon; no post-document resource in 11 views; server log shows no `/favicon.ico`; negative control catches the PRES-1 page's request |
| F03 | Startup metadata hidden | PASS locally / Pending P8 publicly | Size, time, browser, machine, date and last-verified date beside the action outside any disclosure, read from the record (R2) |
| F04 | 448 days missing from the visible population | PASS locally / Pending P8 publicly | "10,747 historical hours over 448 days", both bound to `cp20.metrics.B0.pooled.*` |

## On FAIL only

- Single largest meaningful gap: not applicable — the verdict is PASS; no applicable effective rule is violated.
- Exact next acceptance test: not applicable to this verdict. The migration's next gate is P8 after the Owner's
  publication: the public checks listed in `publication-packet.md` §4, which must close F01–F04 on the served
  surfaces and measure the new bundle's cold start.

## Findings, kept separate (PUBLISH_RULES §10.1)

**1. Existing-rule violations: none found.**

**2. Product recommendations (not violations):**

- **R1 — A3 cards could state the question.** Neither transition card has an explicit question line; the question
  is carried by the heading and "What changed", and stated in each chapter's "The question" directly below. The
  anchor's own copy specification for this transition has the same form, and plan §5.1's record fields do not list a
  question, so this is not a violation. Adding the chapter's question (and "on identical hours" in the v1→v2
  comparator row) would make each card self-contained.
- **R2 — The startup line measures the PRES-1 bundle.** It is correctly labelled "public demo, 2026-09-29" and plan
  P3.6 allows an earlier labelled measurement, but after publication it will describe the previous bundle. P8 must
  measure the new bundle's cold start (the packet already schedules this and an update if it differs materially).
- **R3 — Product topics have no audit-grade evidence row.** Their numbers are record-bound, the SHAP, permutation
  and regime results carry value tables, and v1's runs are linked from the "Run this product" topic and from the
  archive (`delu-cp2`, model registry, repository), matching the convention of the chapters' detail charts; a row such as
  "Holdout report / diagnostics, frozen 2026-09-15" (CP-2 files at `evidence/cp-2`) would complete §8's evidence tiers
  for the product documentation.
- **R4 — Data topic precision.** "One committed hourly snapshot … of the day-ahead price and the day-ahead load
  forecast" omits the snapshot's VRE forecast/actual fields, which serve only the rejected candidate and the post-gate
  benchmark; "the model uses …" would be exact.
- **R5 — Carried advisories.** The fresh reader's observations 2–18, prior advisories A04 (the MLflow comparison opens
  on parallel coordinates with fold width, still true), A05 (1.052 vs "28.58% worse" reconciled only in a
  disclosure) and A07 (repeated development caveats) remain advisory.
- **R6 — Build message.** `build_pages.py` prints a character count labelled "bytes" (pre-existing); the build record
  is correct.
- **R7 — Reproduction order in this assignment.** In a clean checkout, pytest before `make wasm` yields 3 failed and
  12 errors, all "app/public/ is absent"; after `make wasm` the suite gives 1,088 passed, 7 skipped. Future Critic
  assignments should list `make wasm` (or `make wasm-payload`) before pytest, as CI does.

**3. Proposed rule amendments:** none.

**Comparison with earlier findings (made after the independent findings above).** F01–F04 are repaired in the
candidate and pass locally; their public closure remains P8's. The review's V2-01 and V2-02 proposals are now A1 and
A2 and are met (the fresh reader mapped 14% and 17% correctly; the full finding is readable by desktop screen 2 and
phone screen 3). Advisory A01's pacing concern is resolved by A2; A02's census confusion is addressed by the derived
census sentence; A04, A05 and A07 persist as advisories (R5). No earlier closure claim was found unsupported.

## Limits of this review

- No real Safari, physical iPhone or screen reader. Playwright WebKit is not Safari; phone sizes and the iPhone are
  emulated; 200% zoom is an equivalent CSS viewport. WebKit's tree is read through a private inspector API.
- Demo, report and state checks ran against local servers; timings (9.6–11.7 s) are local, not Hugging Face's.
  Public MLflow checks (commands 25–26) are fresh anonymous observations at 06:17–06:24 UTC and prove those runs,
  not continuous availability.
- Pages and the Space still serve PRES-1; nothing here certifies public behaviour of the candidate.
- Screenshots and machine records of this review are local evidence under `.local/tmp/pres-2-critic/`; they are
  not publicly available.
