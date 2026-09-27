# Verdict — PRES-1 — Independent check — FAIL

- Candidate SHA: 28b3c2c8f4012b1b623be24fc639e6d63bc24e59
- Plan / version / bar: `docs/track-b/presentation-and-tracking-plan-2026-09-24.md`, revision 3 (SHA-256 `281193740a256a99a1676d53ef61c9babb5f744a7d0fb038927e305d1149812c`, confirmed at the candidate), §12 "Phases, order and acceptance", the Acceptance column for phases 0 to D2, with the §6 invariants and the §9.5 test table (brief §8). Brief / section: `docs/track-b/pres-1-brief-2026-09-24.md` (SHA-256 `7cb672f2ffa960908723e55e114442be4f8286e718892935acad3e6e0965ebb4`, confirmed), §9 "Independent check", "What its assignment covers".
- Verbatim bar excerpt:
  > **0: Demo diagnosis** … Diagnosis recorded. The demo states (§7.11) go ahead in any case.
  > **A: Content** … Every statement has a claim ID and a file/row source. No withheld phrasing. No v2+ content after 2026-04-07.
  > **B: Evidence layer** … Tests green, negative controls included. No typed research number in any generator.
  > **C: MLflow preparation, local only** … The rehearsal's verifier passes. An interrupted upload resumes without duplicates. The deliberate faults are caught. No public write.
  > **D1: Visual specimen** … **Ready to extend when:** the Owner approves both the desktop and the phone composition; the hierarchy of result, limitation and evidence is clear; no scientific meaning depends on colour or hover; real content fits; and the reader tasks show no confusion between research progress and the released product.
  > **D2: Full page and surfaces** … Tests 17–34 green. `make verify`. No fetches. The size budget holds. The §11.3 report checks pass locally.

  > - **The data:** every rendered research number is re-derived from its source record.
  > - **The claims:** the claim maps; the withheld phrases; the labels; the exact H−P endpoint; v1's label.
  > - **The charts:** units, direction and intervals; scales; mobile variants; the meaning survives without colour or hover.
  > - **The links:** internal anchors, the repaired link checker and the MLflow routes.
  > - **The reading experience:** the six reader tasks in plan §11.4.

  (The excerpt is the citation. Any line number is a courtesy and is non-binding.) Every excerpt was found verbatim at the candidate SHA: each §12 acceptance cell with `grep -cF` = 1 in the plan (plan lines 1345–1350), and each brief §9 bullet with `grep -cF` = 1 (brief lines 219–232). I read the Tasks and Outputs cells of the same rows, and plan §§6, 7, 8, 9, 10, 11 and 16 in full.
- Worktree clean before and after: yes. `git status --porcelain` was empty and `rev-parse HEAD` = the SHA before starting and again before writing this verdict. `check_links.py` rewrote `reports/cp3/link_check.json`; I copied it out and restored it with `git checkout --`. Only gitignored byproducts remain (`.venv`, `app/public`, caches).

## Commands actually run

All in `.local/worktrees/pres-1/check-2`. Outputs are under `.local/tmp/pres-1/check-2-out/`.

| Command | Exit | Observed |
|---|---|---|
| `git status --porcelain`; `git rev-parse HEAD` | 0 | empty; `28b3c2c8f4012b1b623be24fc639e6d63bc24e59` |
| `shasum -a 256` on the plan and the brief | 0 | `2811937…9812c` and `7cb672f…65ebb4`: both match |
| `uv sync --frozen` | 0 | "Checked 117 packages" |
| `uv run --frozen python scripts/build_wasm_payload.py` | 0 | "payload: 15,363,807 bytes across 14 files … wrote reports/cp3b/payload.json"; the tree stayed clean |
| `uv run --frozen pytest -q` | 0 | **735 passed, 7 skipped** in 161 s. A rerun with `-rs` gave the same result; the skips are `tests/cp20/test_gfs_eccodes.py` (no eccodes), one CP-16 anchor-bound test and five CP-16 production-verification tests. None is in tests 17–34. |
| `uv run --frozen python scripts/verify_release.py` (the `make verify` target, Makefile:81–82) | 0 | Every bound claim agrees on all five surfaces; "fetching references to an external origin: 0"; "gated DagsHub UI links on any surface: none"; it ends with "PASS — every bound claim agrees on every surface; the static page fetches nothing" |
| `uv run --frozen python scripts/rebuild_presentation.py`, then `git status --porcelain` | 0 / 0 | README research block, README CP-3 section, MLflow export, static page and cross-surface checks all "ok" ("rebuilt every presentation surface in 11.8 s"). `git status` was **empty**: every surface, including `reports/cp3/pages_build.json`, reproduces byte for byte. |
| `uv run --frozen python scripts/mlflow_export.py --check` | 0 | "the committed export is current" |
| `uv run --frozen python scripts/mlflow_publish.py --dry-run` | 0 | "dry run: 23 runs, 6928 metric points, 55 artifacts; outbound scan clean; export current at 28b3c2c8f401". It returns before any client is built, so there was no network write. |
| `uv run --frozen python scripts/check_links.py` (read-only GETs) | 0 | 18 destinations, all 200, including three GitHub blob URLs on `evidence/cp-20` and two on `evidence/cp-16`; 4 gated DagsHub UI paths return 302 to /user/login; "failed destinations: none". `link_check.json` was copied out and restored. |
| Mocked gate, run in-process on the real surfaces: `check_links.main(probe=…, record=None, gated=False)` | — | one destination forced to 404 gave **exit 1** ("failed destinations: […/weather-ablation/report.md]"); all 200 gave exit 0; every probe erroring gave exit 1. `classify()` returned local, example and example for a loopback URL, a `<you>` placeholder and example.com. |
| `…/playwright/bin/python scripts/check_reader_paths.py screens docs/index.html --width 1440 --width 390 --out …/screens --record …` | 0 | 1440: scrollWidth 1440 = clientWidth, overflow False; 390: 390 = 390, overflow False; smallest chart text 12 px (v1 replay) |
| `… charts docs/index.html --out …/charts --record …` | 0 | 66 chart captures at 1440, 390, 360 and 320, closed and open: no overlap, no clipping, minimum 12 px, overflow 0 px at every width |
| `… route docs/index.html --out …/route --record …` | 0 | At 390, 360 and 320 the preview route opens the archive at `#forecast`; the replay draws at 358, 328 and 296 px with 12 px text; 95% shows **0.9398**; the ×1.02 scenario caveat is shown; the archive's Results link stays in v1 |
| `… a11y docs/index.html --engine chrome --engine webkit --record …` | 0 | Chrome 153.0.8010.54 and WebKit 26.6 each: text contrast 0 below threshold (2,172 checked at 1440, 2,164 at 390); non-text 0 below 3:1 (549 and 527); 85 touch targets at 390 with 0 under 44 px; keyboard 54 stops in document order, 0 without visible focus, summary toggles on Enter, an anchor into a closed disclosure opens it; overflow 0 px at 1280 and 1440 zoomed to 200% and at a 320 px reflow, closed and open |
| My own Playwright scripts, run with the same tool Python: `reader.py` (viewport screens and innerText at 1440×900 and 390×844), `tasks.py` (where each reader-task answer sits on the page), `mlflow_route.py` (anonymous visits to the two advertised `delu-cp2` routes) | 0 | results below |
| Read-only `curl` to DagsHub REST: `experiments/get-by-name?experiment_name=delu-generations`, `experiments/get?experiment_id=0` and `registered-models/get` | 0 | **404 RESOURCE_DOES_NOT_EXIST** for `delu-generations`; experiment 0 = `delu-cp2`; `delu-day-ahead-champion` has the `champion` alias on v1 |
| Read-only `curl` of raw GitHub rows the page links to (`evidence/cp-20` `uncertainty.csv` L12–13, `metrics.csv` L44–50; `evidence/cp-16` `uncertainty.csv` L32; `main` `docs/track-b/evidence/cp-20/integration.md`) | 0 | Each is byte-identical to the committed row, e.g. `equal_fold,HG,H0,MAE,-0.07831150099532369,-0.10059575155295458,-0.05703087928591252,…`; the review file begins "Verdict — CP-20 — Integration — PASS" |
| My own offline re-derivation scripts (`scripts/extract.py`, `recompute.py`, `chartpos*.py`, `bare.py`), which read sources with `git show <evidence tag>:<path>` and never import project code | 0 | results below |

## Evidence actually inspected

**Governance and records read.** `AGENTS.md`; the plan (in full) and the brief (in full); both claim maps; `research_claims.py` (templates, `WITHHELD_PATTERNS`, `STALE_PHRASES`); the relevant parts of `research.py` (`SOURCES`); `build_pages.py` (scale code, C3, C5, the token sheet, a numeric-literal grep over the whole file); `mlflow_export.py`, `mlflow_publish.py`, `readme_research.py`, the `cp3_readme.py` diff and `rebuild_presentation.py`; the `claims.py`, space card and `build_wasm_space.py` diffs; tests 23 and 29–34 (names and the relevant bodies); `reports/presentation/**`; `reports/cp3b/space_wasm_bundle.json`; `docs/track-b/evidence/pres-1/{reader-tasks-d1,owner-hand-checks,independent-check-1}.md`. The D1 review in the main checkout hashes to `2193d2e5…77b5f5`, as `specimen.md` records. `pyproject.toml`, `uv.lock`, the locked set, `DATA-LICENSE.md`, `models/`, `data/` and the CP-2/10/15/16/20 reports: **no diff** from e8025cc to HEAD.

**Blob identity.** Every CP-20, CP-16, CP-15, CP-10 and CP-2 source I used has the same blob at HEAD as at its evidence tag (`git rev-parse HEAD:<p>` = `evidence/cp-20:<p>`). CP-10 has no tag of its own; its files are read at `evidence/cp-15`, as `research.py` declares.

**Data: every claim-bound value re-derived.** I parsed all 1,444 `data-claim` elements on the page. For each `data-record` I located the source row myself: `metrics.csv` by policy and scope (or policy, `per_fold` and fold); `uncertainty.csv` by candidate, baseline, scope and metric; `criteria.csv`; `diagnostics.csv` hour and peak rows; `peak.csv`; `relative_scores.csv`; `peak_windows.csv`; the CP-2 JSON and CSV; `protocol.json`; `extraction-summary.json`; `resource-final.json`. I then rounded to the displayed number of decimals.

- **734 of 734** displayed numerals match their sources, and **447 of 447** `value=` attributes are exact.
- The only "mismatches" were benign: "28.58% worse" is the absolute value of −28.580190…, and a "2" came from the label "v2".
- The 11 elements without a record are v1 claims from `claims.py`. I re-derived them from `reports/cp2/holdout_report.json` and `dm_development.json`.
- A scan for unbound numerals outside the v1 archive found only licence and version strings (CC BY 4.0, GFS 0.25°, a DOI, Python 3.13.15).

Numbers recomputed, with sources:

| # | Where on the page | Shown | Source (evidence tag) | Source value |
|---|---|---|---|---|
| 1 | Opening / overview / fairness | 10,747 hours | M20 B0 pooled `n_hours` (cp-20) | 10747.0 |
| 2 | Overview, v3 S_MAE / S_WIS | 0.5658 / 0.5322 | M20 L50 HG equal_fold | 0.5657606376 / 0.5322186902 |
| 3 | Overview, v2 S_MAE / S_WIS | 0.6441 / 0.6160 | M20 L49 H0 | 0.6440721386 / 0.6160299895 |
| 4 | Overview, v1 S_MAE / S_WIS | 1.0518 / 0.9856 | M20 L45 B1 | 1.0518451348 / 0.9856366964 |
| 5 | Overview reference lines | limit 0.59203 / 0.57509 | C20 L2–3 `upper_limit` | 0.5920298211 / 0.5750919367 |
| 6 | F07 note | 28.58% worse; 448 days | DM2 point vs similar-day naive | −28.580190297; `n_days` 448 |
| 7 | F07 note | MAE 32.45 / 32.81 / 41.74 | PM2 similar_day_naive; M20 B0 pooled; M20 B1 pooled | 32.4522992 / 32.8101017 / 41.7434816 |
| 8 | v3 C2a (a confidence interval) | −0.0783 [−0.1006, −0.0570] | U20 L12 | −0.0783115010 [−0.1005957516, −0.0570308793] |
| 9 | v3 C2a | −0.0838 [−0.1044, −0.0655] | U20 L13 | −0.0838112993 [−0.1043826811, −0.0655398413] |
| 10 | v3 fold-3 caveat | −3.18 [−6.09, +0.037] EUR/MWh | U20 L6 | −3.1782372 [−6.0898293, 0.0368770] |
| 11 | v3 crisis peak | MAE 52.51 → 47.52; hits 377 → 383 of 408 | C20 criterion 4 peak `actual`; D20 L837/L977 `hit_count95`, `n_hours` | 52.5098015 / 47.5214373; 377.0 / 383.0; 408 |
| 12 | v3 "what else changes" | 0.9377 against 0.9389 | M20 HG / H0 pooled `coverage95` | 0.9376570 / 0.9388667 |
| 13 | v2 chart 2, H−B2 | −0.0137 [−0.0236, −0.0053]; −0.0230 [−0.0337, −0.0118] | U16 L34–35 (cp-16) | −0.0137388 [−0.0235719, −0.0053442]; −0.0229611 [−0.0336965, −0.0118099] |
| 14 | **Exact H−P endpoint** | +0.000003857628092332211 | U16 L32 `ci_upper` | 3.857628092332211e-06 (identical decimal expansion). It appears 4 times: desktop SVG, phone SVG (on its own line), the interpretation text and the values table. There is no rounded or `≈0` form anywhere. |
| 15 | v2, control − daily LEAR, WIS | −0.0103 [−0.0201, +0.00067] | U16 L37 | −0.0102693 [−0.0200602, +0.0006704] |
| 16 | CP-10 branch | 19.36% → 32.11% | PW10 `coverage_95` v1_reference / c1_price_volatility (cp-15) | 0.1936275 / 0.3210784 |
| 17 | CP-15 branch | A1 crisis MAE 49.88; B2 0.6578 / 0.6390 against A1 0.6723 / 0.6460 | PK15 A1 `MAE`; RS15 | 49.8766991; 0.6578109 / 0.6389910; 0.6722908 / 0.6460151 |
| 18 | v1 chapter | bias −269.45; level 269.45; shape 66.88; 0.194 coverage | PK15 B1 | −269.4488149; 269.4488149; 66.8793216; 0.1936275 |
| 19 | v1 holdout (v1 claim) | 25.9078 / 27.7578; 6.7083 / 13.8789; p = 1.98e-18; +1.6228, p = 0.948 | `reports/cp2/holdout_report.json`; DM2 | 25.9077804 / 27.7577674; 6.7082949 / 13.8788837; 1.98148e-18; 1.6228252, 0.9476866 |
| 20 | v3 C3, v1 fold-3 MAE | 140.99 | M20 B1 per_fold fold_3 `MAE` | 140.9928522 |
| 21 | v3 protocol | 2,476 runs; 123,800 messages; 136.0 GiB; 40.09 h; $0; seed 15042, 2,000 replicates, 7-day blocks | `extraction-summary.json`; `resource-final.json`; `protocol.json` | 2476; 123800; 136.0; 40.09; 0; 15042 / 2000 / 7 |

**Chart geometry.** For all 20 chart SVGs (10 desktop/phone pairs) I fitted each axis from its own tick labels and checked every bound mark (circle, rect, polygon or interval line) against its source value.

- **760 of 772** marks sit where their value says.
- The other **12** are v3 C3's fold-1 MAE and fold-1 WIS rows, desktop and phone. Their marks are placed correctly on the true domains, 0–7.5 and 0–4.5, but the right-end tick labels read **"8"** and **"4"**. The cause: `build_pages.py` `c3_panels` sets `hi` = `ceil(top·1.08/mag·2)·mag/2`, which gives 7.5 and 4.5, and `multi_rows` prints `tick_text(hi, 1)`, which is `f"{hi:.0f}"`; that rounds half to even, so 7.5 → "8" and 4.5 → "4". Visible effect: v1's WIS triangle, printed "4.00", sits left of the "4" end tick.
- The other 8 C3 rows show domain ends that match their labels (25, 200, 25, 30, 15, 95, 15, 15).
- Desktop and phone variants carry the same bound marks and the same values in every chart (v2 chart 2 differs only in line-wrapping of the endpoint).

**MLflow export.**

- **Structure.** 23 runs, 23 unique `run_key`s. Parents: cp10, cp15, cp16, cp20. Children 7 / 9 / 2 / 1, exactly plan §10.3. `manifest.counts` = {parents 4, children 19, total 23}. Deterministic (`--check`, and rebuild with no diff).
- **Values.** Run-description numbers come from records at build time (`_n()` / `_ratio()`): "79/408 to 131/408" = PW10 `covered_95` 79 / 131 over `n_obs` 408.0; "10,747" = CP-15 B0 `n_hours`; "448 represented development days" = `n_days`. Sampled metric values equal their sources to full precision: `cp20/HG` `s_mae` 0.5657606376333641; `delta_s_mae_vs_v2_h` −0.07831150099532369 with `ci_high` −0.05703087928591252; `fold_mae_eur` at steps 1–5 equals M20 per fold; `cp16/V2-H` `delta_s_mae_vs_v2_p_ci_high` 3.857628092332211e-06; `peak_hits95` 383.
- **Timestamps.** Fold points carry each fold's last delivery date. The latest timestamp across all 6,928 points is 2026-04-07.
- **Tags.** `cp15/B1` carries `delu.v1_record_run=83e475627b6646c885c70f9010c8cf2e`. Two comparability IDs: 15 runs (CP-15/16/20) and 8 runs (CP-10). Provenance tags are separate.
- **Capability record.** `reports/presentation/mlflow-capabilities.json` records a local 3.5.1 rehearsal with `passed: true`: an interruption after 115 writes (exit 3); verification failing as expected (34 problems); resume "13 created, 2 resumed, 8 already complete"; verification after resume passed (23 runs, 6,928 points); idempotent re-run passed; both deliberate faults caught ("1 missing" history point; altered `summary.json` digest). The public server was probed read-only: `/version` 3.5.1, and "delu-generations exists: false".
- **No public write.** There is no `mlflow_index.json`, and no record has `"target": "public"`. My own read-only REST call returns 404 for `delu-generations`.

**Demo states (§7.11).**

- `build_wasm_space.py` injects static loading, failure, retrying and ready markup, opening the `<body>`, with a Retry button, a link back to the report, no percentage, and a timer used only as a deadline.
- `startup_findings` guards it. The extended `test_23` (4 tests, not skipped) asserts the markup and has a negative control.
- `space_wasm_bundle.json` records `startup_states.injected: true`, `problems: []`.
- `release-checks/2026-09-25-space-states-local.json` records the states in Chrome 153 and WebKit 26.6 at 390×844: asset failure → failure; retry → ready; runtime-reported failure in 1.1–1.2 s; a hung runtime still loading at 1 minute and in failure after the deadline.

**D1.** `reports/presentation/d1/specimen.md`, "The Owner's Stop 1 decisions (2026-09-25)", records: "D1 approved with the correction above; D2 proceeds"; the heading correction; contribution wording approved; public name "Yarden Viktor Dejorno"; the device-test outcome. The page matches:

- "Performance during the 2022 price peak" is present.
- The contribution text is identical to D1 review line 254.
- The byline "Led by Yarden Viktor Dejorno · Contribution" is present.
- The CSS tokens equal the token table (all 17 values).
- The reader-task record (`reader-tasks-d1.md`, round 2) reports no confusion between research and product.

**§11.3 report checks, row by row.** The engines were Google Chrome 153.0.8010.54 and Playwright WebKit 26.6 on this Mac (arm64, Darwin 25.5.0), with phone widths emulated. The committed record `release-checks/2026-09-27.json` (page generator commit 67570c8; `docs/index.html` and `build_pages.py` unchanged since) and my reruns agree.

| §11.3 Report check | Demonstrated where | Not demonstrated |
|---|---|---|
| Screenshots at 1,440, 768, 390 and 360 px | Chrome: all widths plus 320 in the record; I reran 1440 and 390, and charts at 1440, 390, 360 and 320 | Desktop Safari, iPhone Safari |
| `scrollWidth ≤ clientWidth` on phones; 200% zoom; reflow at 320 | Chrome and WebKit: 0 px overflow, closed and open | Desktop Safari, iPhone Safari |
| Contrast: text 4.5:1 and 3:1; non-text 3:1 | Chrome and WebKit: 0 failures (text and chart shapes); the preview band now has a #71717A (4.83:1) outline | Desktop Safari, iPhone Safari |
| Keyboard: order, visible focus, anchor links into closed disclosures | Chrome (Tab) and WebKit (Alt+Tab): pass | Real desktop Safari |
| **Disclosures that are announced** | none | **Not demonstrated on any device.** VoiceOver is in `owner-hand-checks.md` row 6, unticked; the record says status "pending" |
| Touch targets of about 44 px | Chrome and WebKit at 390 emulated: 0 under 44 | iPhone Safari (hand-check row 5, unticked) |
| Charts readable; meaning without colour; fan chart ×1.02 and 95% behaviour | Chrome: no overlap or clipping, 12 px floor, 0.9398 and the caveat after the route | Desktop Safari, iPhone Safari (hand-check rows 2, 3 and 7, unticked) |

Plan §11.3 names "Desktop Chrome and Safari; iPhone Safari" for this row. `owner-hand-checks.md` is an empty checklist. The committed record gives `owner_hand_checks.status`: "pending: needs a person, a real Safari, a real iPhone and VoiceOver". I could not close this myself: no iOS runtime is available, and Safari automation would change a system setting.

The other §11.3 rows:

- **Demo row:** local build only, cold start 10.6–11.7 s in Chrome and WebKit, with level and scenario changes working. The deployed Space gets the states only at F7.
- **MLflow row:** only the `delu-cp2` routes are advertised. I opened `#/experiments/0` and `#/models` anonymously in Chrome: `delu-cp2` lists its runs, and `delu-day-ahead-champion` shows `@ champion`.

## Reader tasks (plan §11.4)

Read as a first-time visitor, every disclosure closed, screen by screen. Positions are the top of the first element that answers each task, measured in Chrome. "Screen n" = floor(top / viewport height) + 1. As an agent I cannot time myself meaningfully, so screens stand in for seconds.

| # | Task | My answer | 1,440 × 900 | 390 × 844 |
|---|---|---|---|---|
| 1 | Find the product | An hourly day-ahead price forecaster for the German–Luxembourg market, with prediction intervals. "Try the v1 demo" runs the released model in the browser (about 57 MB on a first visit); a static historical replay chart sits beside it. | Screen 1: preview label at 129 px, demo button at 760 px | Screen 1: button at 643 px; preview on screen 2 (892 px) |
| 2 | Released and research versions | Released: **v1** (LightGBM, "Released model", the demo). Research: **v3 · weather features**, badged "Development · post-selection" | Screen 1 (598 / 684 px) | Screen 1 (455 / 541 px) |
| 3 | The main improvement, in my words | v3 kept v2's blended-LEAR model and added forecast wind (10 m and 100 m) and solar radiation. On the same 10,747 historical hours, both its point error and its interval score fell against v2, by about 0.08 of the naive forecast's error each, with 95% intervals wholly below zero. It is not yet tested on new data, and the gain is weakest in the 2022 crisis fold. | Screen 2 (takeaway, 1,063 px); the chart with numbers on screen 5 (3,911 px) | Screen 2 (1,495 px); chart on screen 8 (6,363 px) |
| 4 | A rejected idea | CP-10's calibration experiment, "Not adopted · recalibrating v1 was not enough". The v2 chapter's closed disclosure gives 19.36% → 32.11% crisis coverage. | Screen 2 (1,563 px) | Screen 3 (2,201 px) |
| 5 | A remaining uncertainty | "Performance on future data is still to be evaluated". Also: the fold-3 interval crosses zero, and the gain is not attributable to any single feature. | Screen 2 (1,063 px); screens 5–6 (4,312 / 4,684 px) | Screen 2 (1,495 px); screens 9–10 |
| 6 | Open the evidence for one claim | Followed the v3 chart's "View source values" to `evidence/cp-20` `uncertainty.csv#L12`; the fetched row gives −0.0783115 [−0.1005958, −0.0570309], matching the chart. "Read the review" opens the CP-20 Integration verdict (PASS). | First evidence row on screen 4 (2,726 px) | Screen 6 (4,745 px) |

**Research progress against the released product: no confusion.** The status pair separates "Demo · v1 · Released model" from "Research · v3 · Development · post-selection". The lineage says "Adopted in research · not in the demo". v3's decision says "The demo continues to run v1". The preview is labelled "historical replay, not a live forecast".

Points of confusion or friction:

1. The overview shows the released v1 at 1.0518, worse than the naive, while its chapter says it beat the naive on its holdout. This is reconciled only by the pointer line and the closed "Definitions" disclosure.
2. The overview's "View source values" lands on B0's row (L44) of a 47-column CSV. S_MAE and S_WIS are the last two columns of L44–L50: findable, but raw.
3. **v3 C3 (in "Consistency across the five periods") mislabels two fold-1 axes as "8" and "4".** The v1 WIS triangle printed "4.00" sits visibly left of the "4" end tick.
4. C4's hit-count panel says "closer to nominal is better" but marks no nominal (about 388 of 408).
5. "Both v2 arms miss criteria 1–2 (0.6441 and 0.6458 against 0.59203)" shows only criterion 1's comparison.
6. Outside the page: the README research block says "The exact values and intervals are shown in the chart", but the README has no chart.
7. Outside the page: the overview figure's `aria-labelledby="overview-title"` points at an id that does not exist.

None of points 1–7 concerns the research/product distinction.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1 | **Phase 0**: diagnosis recorded; demo states go ahead in any case | PASS | `release-checks/2026-09-24-demo.json` holds the diagnosis (P0-1: blank static HTML before the runtime), a fix plan, fresh-context runs (Chrome 20.4 / 18.9 s; WebKit 21.1 / 22.0 s), and the Owner's device test ("passed … device and browser were not supplied"). The states are built (see item 5 and the demo-state evidence above). |
| 2 | **Phase A**: every statement has a claim ID and a file/row source; no withheld phrasing; no v2+ content after 2026-04-07 | PASS | The 23 `data-claim` IDs and the 34 block claim IDs are all defined in `cp20-claims.md` or `cp15-cp16-claims.md` (no W-ID used as a claim). Page copy is mapped P01–P15. My reading of the full research text found no W1–W21 phrasing (only honest denials: "This is not equivalence", "never confirmatory" in the protected v1 archive). Stale phrases are absent (test_30 and my reading). The latest v2+ date: the export's maximum timestamp and the fold 5 window both end on 2026-04-07. |
| 3 | **Phase B**: tests green with negative controls; no typed research number in any generator | PASS | Tests 29–32 are green, with negative controls for row, policy, aggregation, unit, revision, undeclared numeral, missing claim, withheld and stale phrasing, a table outside `.scroll`, an unlabelled series, and missing or duplicated markers. I read `build_pages.py`, `mlflow_export.py`, `readme_research.py`, `cp3_readme.py` and the claim templates: numbers come from `{r:record}`, `R.get()` or `_n()`. The round-1 typed notes and the "−0.0783 headline" are now record-bound. What remains typed is structural only: axis domains (e.g. C2a −0.12…0.02, C4 hits 0…420), window dates, and "17" days declared `data-structural="count"` for the 2022-08-15…31 window (agrees with D20 `n_days` 17). The v1 archive's pre-existing text is unchanged since e8025cc. |
| 4 | **Phase C**: rehearsal verifier passes; interrupted upload resumes without duplicates; faults caught; no public write | PASS | `mlflow-capabilities.json`: rehearsal `passed: true`; interruption at 115 writes then resume (13 created, 2 resumed, 8 complete); 23 runs after an idempotent re-run; deleted point and altered digest both caught. My runs: `--check` 0, dry run 0 (outbound scan clean). No index file, no public-target log, and the REST check returns 404 for `delu-generations`. The spec (`docs/track-b/mlflow-tracking-spec.md`) and test_34 are present and green. |
| 5 | **D1**: Owner approval of desktop and phone; clear result, limitation and evidence hierarchy; no meaning via colour or hover; real content fits; no research/product confusion | PASS | Approval is recorded in `specimen.md` ("D1 approved … D2 proceeds", 2026-09-25). The page matches the recorded decisions and the token sheet. There are no hover rules beyond link styling, no `title=` tooltips, and each generation has its own marker. At 320–1,440 there is no overflow. My own reader run and `reader-tasks-d1.md` round 2 found no confusion. |
| 6 | **D2**: tests 17–34 green; `make verify`; no fetches; size budget; **§11.3 report checks pass locally** | **FAIL** | Tests: 735 passed / 7 unrelated skips. `verify_release` PASS. 0 external fetch references (my grep as well). 1,520,886 ≤ 2,000,000 bytes. F02, F03 and F05 are fixed, the Space states are present, the README block is owned, the cards and claims are rebuilt identically. **But** §11.3 names Desktop Chrome **and Safari** and **iPhone Safari**. Only Chrome 153 and Playwright WebKit 26.6 were run. `owner-hand-checks.md` is unticked, the committed record says "pending", and "disclosures that are announced" was verified on no device. |
| 7 | **Data**: every rendered research number re-derived | PASS | 734 of 734 displayed numerals and 447 of 447 `value=` attributes match sources read at their evidence tags; 21 highlighted in the table above. No unbound research numeral outside the archive. Export notes and metrics sampled and exact. |
| 8 | **Claims: the claim maps** | PASS | Every rendered claim ID and block claim ID is present in a map. Source keys resolve to committed files with unchanged blobs. |
| 9 | **Claims: the withheld phrases** | PASS | No W1–W21 phrasing on the page (all disclosures), in the README research block or in the export notes. `WITHHELD_PATTERNS` and `STALE_PHRASES` checks green (test_30). My manual scan found no "peer review", "significant", "guarantee" (other than the negated "not a per-day delivery guarantee"), no economics, and no v3-in-demo. |
| 10 | **Claims: the labels** | PASS | "Development · post-selection" is beside each research result. `NOT_DEMONSTRATED` is present. "no demonstrated joint preference" appears with "This is not equivalence". "Adopted in research". No economics. |
| 11 | **Claims: the exact H−P endpoint** | PASS | `+0.000003857628092332211` ×4 on the page (full, wrapping on phones, never in a tooltip) and ×1 in the README, equal to U16 L32 `3.857628092332211e-06`. The chart row shows "see below", never a rounded value. |
| 12 | **Claims: v1's label** | PASS | Badge "Confirmatory-style, not power-qualified". The sentence "…— confirmatory-style, not power-qualified." is present. `HOLDOUT_DM_LABEL` agrees on all five surfaces (`verify_release`). |
| 13 | **Charts: units, direction and intervals** | PASS | One unit per axis (normalized C2a against EUR/MWh C2b; unit guard tested). Every comparative chart states direction ("lower is better", "negative favours v3 / the first policy", "closer to nominal", "narrower at equal coverage"); C5 now says "lower is better". Intervals are labelled "paired 95% confidence interval" and, in the fairness note, "not forecast intervals". Fold 3's crossing is not cropped. Minor: C4's hit panel has no nominal mark. |
| 14 | **Charts: scales** | **FAIL** | v3 C3 fold-1 MAE: domain 0–7.5, end label "8". Fold-1 WIS: domain 0–4.5, end label "4". This is in both desktop and phone variants: 12 of 772 marks are inconsistent with their own axis. Cause: `tick_text(hi, 1)` renders 7.5 and 4.5 with zero decimals, rounding half to even. The other 760 marks, and every other axis, agree with their source values. Per-fold scales are labelled as such (G12). |
| 15 | **Charts: mobile variants** | PASS | Each of the 10 charts has a dedicated phone SVG (296 units wide), with bound marks and values identical to desktop. Minimum rendered text is 12 px at 390, 360 and 320 (charts and route checks). |
| 16 | **Charts: meaning survives without colour or hover** | PASS | Distinct markers (v1 triangle, v2 square, v3 circle, reference diamond, study open circle), row labels and printed values on every mark or row (C5: dash style, markers, end labels and a values table). No hover-only content. Non-text contrast has 0 failures in both engines. |
| 17 | **Links: internal anchors** | PASS | 22 internal `href="#…"` all resolve; 111 ids, none duplicated. The archive has "Back to the model comparison", "Back to v1" and "Back to the top". Links into closed disclosures open them (a11y probe). Nit: a dangling `aria-labelledby="overview-title"` (not an anchor). |
| 18 | **Links: the repaired link checker** | PASS | The real run exits 0 with 18/18 destinations at 200. A mocked 404 or a network error gives exit 1, and all 200 gives exit 0. Local and example URLs are classified and not fetched. test_33 is green. |
| 19 | **Links: the MLflow routes** | PASS | The new experiment's links render as unavailable text, "(link added when the runs are published)" ×4, with `data-unpublished` markers and a `--final` refusal. Surfaces say `delu-generations` "will be tracked" (future tense until `mlflow_index.json` exists). `delu-cp2` `#/experiments/0` and `#/models` render anonymously; REST confirms id 0 = `delu-cp2`. |
| 20 | **Reading experience: the six reader tasks** | PASS | All six answered: tasks 1–2 on screen 1 at both widths, 3–5 by screen 2–3, and 6 by screen 4 (desktop) or 6 (phone). The evidence link was followed to the exact source row. No research/product confusion; the friction points are listed above. |
| 21 | **Plan §6 invariants** (brief §8) | PASS | Zero runtime calls; one v1 claim source (`make verify`); generated surfaces reproduce byte for byte; v1's honesty statements (10,158 → 4,412 → 0, 152-day staleness, shrinkage, 0.194, p = 0.948) unchanged in count since e8025cc; `.mlflow` host only; `live_` wall (test_24); GFS line on all four surfaces; endpoint; date guard; `pyproject.toml` and `uv.lock` byte-identical; no retired-tooling text; placeholder guard present; README markers once each; Space states; planned work unscored. |
| 22 | **Plan §9.5 test table** (brief §8) | PASS | test_29 through test_34 and the extended test_23 exist with the named checks and negative controls, and all pass. Existing tests 17–24 and 28 pass. |

## On FAIL only
- **Single largest meaningful gap:** D2's "The §11.3 report checks pass locally" is still not demonstrated for the browsers and devices §11.3 names: desktop Safari, iPhone Safari, and a screen reader announcing disclosures. `owner-hand-checks.md` is unticked and the committed record says "pending". A second, smaller defect: two axes in v3 C3 misstate their scale (fold-1 MAE labelled 0–8 on a 0–7.5 domain; fold-1 WIS labelled 0–4 on a 0–4.5 domain).
- **Exact next acceptance test:** Both must hold at one new candidate SHA.
  1. A committed `reports/presentation/release-checks/<date>.json`, or the completed `owner-hand-checks.md` that it references, records rows 1–7 of the hand checklist as passing on desktop Safari and on iPhone Safari, each with its device and browser version. The VoiceOver row must confirm disclosures announced as collapsed or expanded.
  2. In `docs/index.html`, every C3 axis end label equals its scale's domain end, in both variants. The chart-position check (marks against their own tick labels) finds 0 inconsistencies. `pytest` has a test that fails when a per-row axis end label differs from the `Scale.hi` it labels.
