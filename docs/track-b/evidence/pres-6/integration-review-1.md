# Verdict — PRES-6 — Integration — FAIL

- Candidate SHA: f8fcd7239664f035496847eee06b1601d60f5790
- Plan / version / bar: `capstone_v21.md`, v21-r20, §24.14 "Publishing and going live before 4.7T (v21-r20)", items 5
  and 6, with the checkpoint's brief `docs/track-b/evidence/pres-6/issued-brief.md` (SHA-256
  `bdb78f02894896d2ee1f249355d23351f972cdb217d4d906d22561172f40e5f6`, recomputed), its "Observable outcome" and
  "Complete authoritative checkpoint bar" (PUBLISH_RULES 1.5, A8 triggered by O46).
- Plan identity, recomputed with `main`'s `scripts/bar.py`: plan `capstone_v21.md` at the candidate, SHA-256
  `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`; section 115 lines, 7426 bytes, SHA-256
  `5d38de24b3c68ec01e2f5c4e6eaf368c253485107549fc2d85c3c71ccf2f5349` (equal to the generated brief's).
- Verbatim bar excerpt (the whole section, extracted at the candidate by `bar.py bar … --quote`; items 5 and 6 carry
  the lines the assignment cites):
  (The excerpt is the citation. Any line number is a courtesy and is non-binding.)

> ### 24.14 Publishing and going live before 4.7T (v21-r20)
>
> **What this section does.** It applies the Owner's decision 28 of 2026-11-05
> (`docs/track-b/owner-decisions-2026-11-05.md`, SHA-256 `4daa5617e51208b0994eac925d51078ea43481e6fb1017aec3576c0936490215`).
> - It governs where it differs from §24.2, §24.9, §24.10, §24.12's list "For CP-18", §24.13's list "For CP-18" and
>   decision 25's order.
> - Every term below was set without any 4.7T outcome, since none exists.
>
> #### What stays exactly as registered
>
> - **A1's freeze.** CP-17c's policy identity `720fc581be6206eba8ed303e689e63c09272a189564090a547d93fc9e7db62dc`,
>   its manifest and the frozen package stay unchanged. `refreeze verify` guards them, and the live pipeline
>   calls the package without editing it.
> - **4.7T, in every registered term** (§24.12, §24.13):
>   - the window, delivery days 2026-09-07 to 2026-12-05;
>   - the candidate, the comparators, the scores, the pass conditions, the margins and the failure rules;
>   - the vintage terms (the protocol's §3);
>   - the machine (the Owner's Mac, no cloud) and the H2 checks before its first issuance;
>   - the calendar: it opens no earlier than 2026-12-04, after the price for 2026-12-05 is published;
>   - the audit, the Owner's declaration and his retrieval approval.
> - **4.7T issues its window itself.** Its issuance starts from the freeze-origin state, runs on the Owner's Mac
>   under its terms, and keeps its own store. Nothing the live product issues is 4.7T's issuance or score.
> - **No registered term changes from here until 4.7T is scored.** A proposal to change one returns 4.7T to the
>   Owner as BLOCKED.
>
> #### What changes
>
> **1. The order (decision 25).** CP-18's activation and a publication now come before 4.7T:
> - **CP-18c**, the activation: the live product starts and runs daily;
> - **PRES-5**, the publication: the research since v5, A1 in the comparison, and the live product;
> - **then 4.7T** at its date, and the publication of its result.
>
> Decision 25's "one complete publication" becomes these two publications.
>
> **2. The red line, for the live pipeline only.** §24.2's guard retires for the live pipeline at CP-18c, not
> after 4.7T.
> - **The live pipeline downloads all the data through the present** and trains on it, as §24.2's last
>   paragraph allows ("The live product, once running, trains on all the data available to it").
> - **Every research path keeps the guard.** The development downloaders and builders still refuse any row after
>   2026-09-06, and CP-17c's development builder stays as frozen.
> - **Reading.** The live data is handled by code.
>   - An agent that operates the live pipeline may read its logs and records, only to operate it.
>   - No agent uses data after 2026-09-06 for any research number, chart, choice or registration before 4.7T is
>     scored.
>   - §24.2's rule on reports, news and analyses about market events after 2026-09-06 is unchanged.
> - **The exposure ledger.** Its pinned file `docs/track-b/exposure-ledger.md` stays byte for byte. Later entries
>   go in its continuation, `docs/track-b/exposure-ledger-continued.md`, which the audit reads with it.
>   - CP-18c seeds the continuation with decision 28's entry, dated by the live pipeline's first
>     retrieval.
>   - **Its impact assessment:** nothing 4.7T tests can change after it. Everything 4.7T tests was frozen,
>     registered and pushed to the public repository before decision 28: `land/cp-17c`, 2026-10-30, and the
>     protocol at its freeze. `refreeze verify` checks the freeze on every run.
>
> **3. The audit (§24.2's standard) reads with this.**
> - **The live product's daily fits** are the frozen policy's own operation, not research fits. They sit
>   outside the standard's "fit" and are recorded in the continuation.
> - **The standard's test applies unchanged** to everything 4.7T tests.
> - **The Owner's declaration** covers his decisions before 4.7T opens. Decision 28 used no information after
>   2026-09-06.
>
> **4. The live product's start.**
> - **The live store** is seeded at the freeze origin, 2026-09-06, with CP-18a's genesis command. It is carried
>   to the first live day with CP-18a's `carry`.
> - **The days between** are outside the live record and are never issued by the live product.
> - **The live product's forecasts for window days,** from its first live day to 2026-12-05, are its own. Each
>   carries its actual run time, and none is 4.7T's.
> - **After 4.7T** the live store continues. §24.12's carry "from 4.7T's last window day to the first live day"
>   becomes this carry from the freeze origin.
>
> **5. What the live product shows.**
> - **It shows the live record** under PUBLISH_RULES A7 and A9: the issued forecasts, the outcomes as published,
>   and the issued forecasts' prospective scores.
> - **A1's status** reads "final candidate · pending 4.7T" (O13).
> - **The prospective scores** are labelled "prospective evaluation in progress" (§24.9).
> - **No display presents a live score** as 4.7T's, or as a test result.
> - **The development-period displays** stay on days through 2026-09-06.
>
> **6. The publication (PRES-5).** Decision 28 is the separate decision that §24.10 requires for publishing
> CP-26's and CP-28's results.
> - **It covers:**
>   - A1 in the published comparison, on the same data as v5's comparison;
>   - CP-26's re-baseline on every development day;
>   - CP-28's selection;
>   - the freeze, with 4.7T's registered terms;
>   - the live product.
> - **Its research numbers use development data only.**
> - **It runs under PUBLISH_RULES 1.5.**
>
> **7. The runner and the secrets.**
> - **Until the Owner enters the three repository secrets** (decision 25), the daily runs use the local fallback
>   on the Owner's Mac (§24.13), with the credentials used only inside the consuming process.
> - **The `macos-26` schedule is enabled** once the secrets exist.
> - **The issuing host and the H2 checks are unchanged** on either machine.
>
> **8. What this supersedes:**
> - **§24.2:** "After 4.7T, CP-18's brief retires the guard for the live pipeline only" (item 2);
> - **§24.9:** the order of "Then: CP-18 … and site activation" (item 1);
> - **§24.10:** "No publication" (item 6);
> - **§24.12's list "For CP-18":** the carry from 4.7T's last window day (item 4);
> - **§24.13's list "For CP-18":** the item on the red line on the runner (item 2).
>
> S_14 (§24.13, H4) is unchanged.
>
> #### Decisions recorded (v21-r20)
>
> | # | Decision | Who |
> |---|---|---|
> | 28 | Publish and go live now; A1 frozen and untouched; 4.7T exactly as registered | Owner, 2026-11-05 (`docs/track-b/owner-decisions-2026-11-05.md`, SHA-256 `4daa5617e51208b0994eac925d51078ea43481e6fb1017aec3576c0936490215`) |
> | P1 | "All the data" for the published research means every development day. Research numbers on window days wait for 4.7T, so that it stays the one test | Orchestrator, under decision 27 |
> | P2 | The live start: genesis at the freeze origin, carried to the first live day. The live product's window-day forecasts are its own, never 4.7T's | Orchestrator, under decision 27 |
> | P3 | The guard retires for the live pipeline only. The exposure ledger continues in a new file, because its own file is pinned | Orchestrator, applying decision 28 |
> | P4 | The local fallback runs until the repository secrets exist | Orchestrator, under decision 27 |
>
> **The Owner's declaration (§24.2)** covers decision 28. P1–P4 are registrations under §24.2's test, which the
> audit checks, as R1–R7 and H1–H4 are.

- Worktree clean before and after: yes. `git -C /Users/djourno/Downloads/PJM/.local/worktrees/pres-6/critic-1 status
  --porcelain` printed nothing before the review, after the page rebuild, after the lint, after the test runs and
  before this verdict was written; `HEAD` stayed `f8fcd7239664f035496847eee06b1601d60f5790`. The only byproduct inside
  the worktree is the Git-ignored `.venv` that `uv run` created. No Git write of any kind was made.

## Commands actually run

All from `/Users/djourno/Downloads/PJM/.local/worktrees/pres-6/critic-1`, with `MLFLOW_DISABLE_TELEMETRY=true
DO_NOT_TRACK=1` exported. My scratch folder (outside the worktree) is
`/private/tmp/claude-501/-Users-djourno-Downloads-PJM/42e9ff0c-59d6-4c47-9c7c-d02f4609ac41/scratchpad/critic` (below: `$S`).

| # | Command | Exit | Observed |
|---|---|---|---|
| 1 | `git status --porcelain`; `git rev-parse HEAD` | 0 | empty; `f8fcd7239664f035496847eee06b1601d60f5790` |
| 2 | `git show f8fcd723…:capstone_v21.md \| shasum -a 256` | 0 | `80341681…30e6` (the brief's) |
| 3 | `git show main:scripts/bar.py \| python3 -I - bar capstone_v21.md "### 24.14 Publishing and going live before 4.7T (v21-r20)" --at f8fcd723… --quote` | 0 | section 115 lines, 7426 bytes, `5d38de24…5349`; the excerpt above |
| 4 | `shasum -a 256` over the brief's 22 execution inputs, the four product inputs, `docs/PUBLISH_RULES.md`, the issued brief and `owner-decisions-2026-11-05.md` | 0 | every hash equals the brief's / packet §0's pin (PUBLISH_RULES `1bc0c523…f94e`; brief `bdb78f02…40e5f6`; decision 28 `4daa5617…0215`; `daily-losses.parquet` `7e9c972f…b85d`; `hourly.parquet` `f5cb02a1…f638`; `predictions.parquet` `9d3f539f…5cf9`; `native-reference.json` `f1decb80…96ab`) |
| 5 | `git log --reverse --format='%H %ci %s' 87811abc..HEAD`; `git show --stat` of `405e588c e049bdf0 beac7da6 df08d772 72e688e2 cb48bd92`; §0 extracted at `beac7da6`, `72e688e2` and `HEAD` and diffed | 0 | the order in item 3 below; §0 at `72e688e2` equals §0 at `HEAD` byte for byte |
| 6 | `git diff --stat=200 87811abc HEAD` | 0 | 40 files, all listed in item 6 below |
| 7 | `uv run python -m delu_forecast.final_candidate --product --check` | 0 | `{"identical_to_committed": {"bins.csv": true, "coverage.csv": true, "days.csv": true, "explanation.csv": true, "monthly.csv": true, "regimes.csv": true, "summary.json": true}}` |
| 8 | `uv run pytest -q tests/test_51_pres6_product_results.py tests/test_33_check_links_gate.py tests/test_48_publication_tools.py tests/test_43_publish_rules_migration.py tests/test_30_research_claims_rendered.py` | 0 | `654 passed, 1 skipped in 119.86s`; rerun with `-rs`: the skip is `tests/test_30_research_claims_rendered.py:348: app/public/ is built by make wasm-payload` (not PRES-6's) |
| 9 | `uv run python scripts/build_pages.py` then `git status --porcelain` | 0, 0 | `wrote …/docs/index.html (1,997,761 bytes)` and `reports/cp3/pages_build.json`; status empty; `docs/index.html` `48fef1a0e025cb79a7b53f833062e6e18c8c5ac3f04a7a8654fb5c2711b9c91c`, README `da9ae187766c895d102676b16a5870540029d471b26687fe78cc3319edc77e1a` |
| 10 | `make lint-publication` | 0 | `page: 0 finding(s)`, `readme: 0`, `templates: 0`, `PASS` |
| 11 | `python3 -m http.server --bind 127.0.0.1 8796 --directory docs`; `curl -s http://127.0.0.1:8796/index.html \| shasum -a 256` | — / 0 | served `48fef1a0…9c91c`, 200, 1,997,761 bytes (server stopped afterwards) |
| 12 | `PLAYWRIGHT_BROWSERS_PATH=/Users/djourno/Downloads/PJM/.local/tools/ms-playwright /Users/djourno/Downloads/PJM/.local/tools/playwright/bin/python scripts/check_reader_paths.py release http://127.0.0.1:8796/index.html --shots $S/shots --out $S/release.json` | 0 | `passed=True`, checked 2026-11-14T17:06:54Z; item 8 below |
| 13 | `.venv/bin/python -I $S/recompute.py <worktree>`: my own recomputation from the four pinned inputs, importing nothing from `delu_forecast.final_candidate` | 0 | `PROBLEMS none`: every value in the seven committed files equals mine (item 4) |
| 14 | probe quantiles against CP-28's arm A1 rows (`native-reference.json` `results["A1-<day>"]["quantiles"]` vs `hourly.parquet`) | 0 | 2026-03-29: 23×7, max abs difference 0.0; 2026-09-06: 24×7, 0.0; `central` = `native_central` = `q50` exactly |
| 15 | CP-26's `scores/summaries.parquet`, mask `all_eligible`, group `overall`, streams `nominal/D2` and `nominal/B0` | 0 | D2 MAE 17.186908, WIS 9.682533; B0 MAE 34.552721, WIS 21.141962; 2,068 dates each: equal to `regimes.csv`'s `all` rows |
| 16 | `RC.withheld_findings` over the page's text and the README | 0 | README `[]`; page one hit, `W15: 'coverage guarantee'`, in the protected v1 archive ("the assumption CQR's coverage guarantee rests on"), byte-identical on PRES-5's published page (`983a75c4…`) |
| 17 | for each modified file: its base (`87811abc`) SHA-256 and blob, searched with `git grep` over `HEAD`; the three freeze manifests' path sets; `tests/pres5_landed_code.py`; `src/cp26/harness.py` `PINS` | 0 | item 6 below |
| 18 | `data/snapshot.parquet` joined to `hourly.parquet` arm A1 on P-all, and to CP-24's `y_true` on P-v5 | 0 | P-v5: 8,587 hours, 0 missing, max abs `y_true` − snapshot price 0.0. P-all: all 2,068 days, hours equal `scoring_hours` on every day (49,596), max abs difference from `daily-losses.parquet`'s A1 MAE 5.7e-14 |
| 19 | read-only interface checks for packet §8: `publication_receipt.py`, `secret_guard.py`, `build_wasm_space.bundle_sha256`, `check_reader_paths.py` subcommands, `build_product_space.listing`; `git rev-parse origin/main main`; `git merge-base --is-ancestor 29b6431e origin/main`; `git log main..origin/main`; `git diff --name-only main origin/main` (paths only) | 0 | item 9 below |
| 20 | `git show main:scripts/bar.py \| python3 -I - check /Users/djourno/Downloads/PJM/.local/artifacts/pres-6/critic-1/integration.md --source capstone_v21.md@f8fcd7239664f035496847eee06b1601d60f5790` (on this verdict) | 0 | `ok: lines 15–129 (7425 bytes) appear in capstone_v21.md@f8fcd7239664` |

## Evidence actually inspected

- The issued brief in full; the generated Critic brief; `publication-packet.md` in full; the packet template's section
  list; `PUBLISH_RULES.md` §§2–3 (beside the brief's verbatim §5, §5.1, §5.1a, §6, A2, A5, A8).
- The full diff of `final_candidate.py`, `check_links.py` and `publication_receipt.py`; the diffs of `README.md`,
  `registry.py`, `research.py`'s PRES-6 sources and populations, `research_claims.py`'s W54/W55 and the bins template
  (line 1100), `mlflow-export/manifest.json`.
- `docs/index.html` at the candidate against PRES-5's published page (`git show 87811abc:docs/index.html`, SHA-256
  `983a75c4…9475`), section by section (the h2 order, the text of every section, the pre-`<main>` header and
  navigation), and the full rendered text of Product results and Business insights.
- The seven committed product-result files; `daily-losses.parquet`; `hourly.parquet`; CP-24's `predictions.parquet`;
  `native-reference.json`; `cp17/attribution.py` (`GROUPS`, `column_group`); `cp24/design.py`'s weather columns;
  `baselines.py::SIMILAR_DAY_LAG_BY_WEEKDAY`; `reports/development-inputs/eligibility-calendar.csv`;
  `data/snapshot.parquet` and `data/README.md`; CP-26's `summaries.parquet`.
- `integration-review-4.md`'s R1–R7; `tests/pres5_landed_code.py`; `src/cp26/harness.py`'s `PINS`;
  `reports/ddnn2/base-tree.json` and its users; the CP-17, CP-17b and CP-17c freeze manifests.
- My own release record `$S/release.json` (every view's placements, chart text, problems, console, failed requests,
  accessibility, discovery, keyboard, contrast and touch).
- I did not read the Builder's ledger or any other file under `.local/artifacts/pres-6/`, and formed every finding
  below before reading `editorial.md` and `fresh-reader.md`, which I then only searched for the clause in the gap.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1.1 | Outcome 1: the A8 order | PASS | Page h2 order: opening → How the product works (`product-h`) → Product results (`outcomes-h`) → Business insights (`business-h`) → How the models compare (`results-h`) → journey, chapters, v6…v1, planned, evidence, contribution, attribution, exactly PRES-5's relative order. The opening is byte-identical to PRES-5's; the main navigation's "Results" now leads to `#outcomes`. The release record has `order: A8` in all 11 views; discovery's descriptive routes pass from the closed default view (54 routes, both engines, 1440 and 390). |
| 1.2a | Outcome 2: forecast against observed | **FAIL** | The three days are the rule's (my lower medians: 2021-06-16 of 90, 2022-07-26 of 88, 2025-05-02 of 180; the upper medians 2021-05-20, 2022-08-27, 2025-05-20 differ, so the rule is not vacuous); `days.csv`'s 72 rows equal mine. The **whole-population view** covers 8,587 hours on 358 of the 2,068 days (v5's test periods 2–5), and the page gives the reason as "the only hours whose prices are committed hour by hour". That is false: `data/snapshot.parquet`, committed and pinned in CP-26's `PINS` (`7dd2dc73…`), holds the cleared price of every P-all hour; joined to CP-28's stored A1 rows it reproduces `daily-losses.parquet`'s v6 MAE on all 2,068 days (command 18). The README says the same snapshot holds "67,343 continuous hourly price rows", and the page's v1 archive says the champion "is rebuilt from the committed snapshot", so the published surfaces contradict each other. The same premise is packet §0's ("where committed hourly observed prices exist"), its first correction's ("the observed prices on P-all, which are not committed") and `research.py`'s population label `pres6-p-v5` ("with committed observed prices"). See the gap below. |
| 1.2b | Outcome 2: error over time | PASS | `monthly.csv` equals my calendar-month means (70 months, 2020-12 to 2026-09, each day once); v6 below the naive in every month on both scores; both peak in 2022 (v6 2022-12, the naive 2022-09), as the page says. |
| 1.2c | Outcome 2: error by regime | PASS | 246 / 481 / 1,341 days, 5,900 / 11,536 / 32,160 hours, summing to 2,068 and 49,596; means and ratios equal mine (0.4508, 0.4934, 0.5047; all-days 0.4974 and 0.4580). My own moving-block bootstrap (14 days, 2,000 replicates, another seed) gives intervals within a few hundredths of the committed ones (all-days MAE ratio [0.4724, 0.5215] vs [0.4734, 0.5230]); the committed draws re-derive exactly (command 7). Every regime has ≥ 60 days; the page says none is thin. |
| 1.2d | Outcome 2: explanation | PASS | The CP-17 probe's committed attribution (committed `42e27c70`, 2026-10-27), its fits v6's stored forecasts (command 14). `explanation.csv` equals my summary: delivered slots 23 of 24 on 2026-03-29 (slot 2 dropped), 24 on 2026-09-06; groups 9 and 10; the signed means bridge baseline to issued median (−21.1582, −32.5818); `price_d2` and `calendar` marked unused, never zero. The text's ranks hold (2026-03-29: weather 14.4, load 14.0; 2026-09-06: load 43.7, weather 30.8; `price_d2` 2.7). "Weather forecast: wind and sun" matches `gfs_h*_{wind10,wind100,dswrf}`. Wording: within one fitted model, not a cause, two days not the period. |
| 1.2e | Outcome 2: coverage with width | PASS | `coverage.csv` equals my hour-weighted coverage and width at 50/80/95 for all days and each regime (0.4779/0.7826/0.9437 at 25.5/51.7/88.8 EUR/MWh; the crisis lowest and widest). The nominal level is drawn as a reference line. The naive's coverage is omitted with a true reason on the page (its daily rows hold MAE and WIS only); computing it would need the naive's hourly intervals, a recomputation of another policy. |
| 1.2f | Outcome 2: each graphic's identity; populations; A2 | PASS, with advisory A2 | The identity line governs every graphic ("unless it names fewer days"): v6, A1, CP-28's stored forecasts, every eligible development day 2020-12-29 to 2026-09-06, EUR/MWh, development, post-selection; each chart's caption repeats units and class. Populations equal CP-26's D2 and B0 records (command 15) and CP-28's 2,068 days. A2 on the product finding: item 8. |
| 1.3 | Outcome 3: Business insights | PASS | Intended use, the measured implications (17.2 vs 34.6, 30.7 in the crisis, 51.7 wide, 0.7826) and their limits; "No decision policy, cost model or trading simulation has been authorized or run …"; no chart, no profit curve, no gain implied; "Lower forecast error and interval coverage are not profit, and not a success rate of any decision." |
| 1.4 | Outcome 4: the README | PASS | "Product results" and "Business insights" paragraphs carry the page's numbers and wording through the claim layer (17.2 [15.4, 19.1], 34.6, 51.7, 0.7826, 30.7); W54/W55 and every earlier guard find nothing (command 16). |
| 1.5 | Outcome 5: the link checker | PASS | `check_links.probe` follows redirects one hop at a time (`_NoRedirect`), records `{status, from, location, to}` per hop and fails when the final host differs from the link's (`cross_host_redirect`, `resolves` false); a loop and a missing `Location` fail; the receipt's link row reports `cross_host_redirects`. `test_33` covers the recorded `/history/` → `huggingface.co/history` fixture without the network (in command 8). |
| 1.6 | Outcome 6: the receipt's Space page | PASS | `publication_receipt.normalize_space_page` is `cp18.publish.normalized`, imported (the old local regex is deleted); removed bytes' size and hash recorded; `test_48` covers the recorded served page (in command 8). |
| 1.7 | Outcome 7: R1–R7 | PASS | The section-by-section text diff against PRES-5's page shows only R1 ("of the re-baseline's policies"), R2 ("The p-values come from"), R3 (`A1, PRES-5`, `v5, CP-24`, `A1, CP-24`), R5 (the question sentence) and R7 ("While v6 runs on the Space …") in the comparison and v6 chapter; no number changed. R4: the release records are over HTTP with the served SHA-256. R6 is the return's. |
| 1.8 | Outcome 8: the page budget | PASS | 1,997,761 bytes ≤ 2,000,000 (`pages_build.json`, my rebuild, the served page). |
| 1.9 | Outcome 9: review | PASS (for this stage) | `editorial.md` and `fresh-reader.md` are committed; this is the independent Integration check at the candidate (FAIL); the focused recheck at the final SHA is still to come. |
| 1.10 | Outcome 10: the packet's §8 | PASS | Item 9 below. |
| 2 | The complete checkpoint bar | **FAIL** (one finding) | PUBLISH_RULES 1.5: §5/A8 order PASS; §5.1 (subject 6 now supported on two days, others unchanged) PASS; §5.1a FAIL on the gap of 1.2a (the published interpretation of the population view is false); §3.1–§3.4 otherwise PASS (development, post-selection everywhere; regime intervals from the checkpoint's own draws; prediction vs confidence intervals labelled apart; one decimal EUR/MWh, four significant figures); §6/A5 PASS (54 routes); §9 PASS (item 8); A2 under A8 PASS. The runbook's touchpoints exist (`EVIDENCE_TAGS["evidence/pres-6"]`, seven `SOURCES` by blob and tag, the populations, `PRES6_BLOCKS`, `test_51`). Every packet-template section (1–8, 5a–5d) is present, with §0, §9 and §10 added and the `<final_…>` values left for the final build by design. r20 §24.14 items 5–6: development days through 2026-09-06 only, under PUBLISH_RULES 1.5. Templates §§2–3: the return is the Lead's. |
| 3 | The rules fixed first | PASS | `e049bdf0` (§0, 13:31:25 +0200) → `beac7da6` (first correction, 13:32:45) → `df08d772` (the first numbers, 13:33:20) → `72e688e2` (second correction, 14:07:38) → `cb48bd92` (`explanation.csv`, first added there, 14:09:04). §0 is byte-identical from `72e688e2` to the candidate. The order is the commits'; the 35 s between the first correction and the numbers shows the code was written beside §0, which Git cannot date further. |
| 4 | Every number re-derives from its committed row | PASS | Command 7 (byte-for-byte) and my independent recomputation (command 13, `PROBLEMS none`) over the four pinned inputs; `test_51`'s 453 records re-derive and a perturbed one fails; every value on the page's Product results and Business insights equals its rounded record: the regime table (8 rows), the coverage table (4 rows) and the bins table (10 rows) match their CSVs by script with 0 mismatches, and the headline, the text's numbers, the signed explanation table and the drawn values were checked against my output by hand. |
| 5 | No fit, no other policy recomputed; nothing after 2026-09-06; no live number | PASS | `product_build` reads parquet and JSON and computes means, quantiles and bootstrap resamples only; the naive's values are its committed `B0` rows. `daily-losses.parquet` has no day after 2026-09-06; every product row is within P-all. The report's build reads nothing under `live/`, `reports/cp18c/` or `space-product/`; every date after 2026-09-06 on the page is a process date (decisions, freezes, evidence tags, 4.7T's window), not data. |
| 6 | Allowed paths; never-touch paths; no governance; no earlier binding | PASS, with advisory A4 | The 40 changed files are all under the brief's allowed paths plus O48's `scripts/check_reader_paths.py` and its test (`test_43`). Nothing under `live/`, `src/cp18/`, `space-product/`, `tests/cp18c/`, `reports/cp18c/`, `docs/track-b/evidence/cp-18c/`, `scripts/build_product_space.py`, `.github/workflows/daily.yml` or `exposure-ledger-continued.md`; no anchor, governance, PUBLISH_RULES, template or frozen record. No modified file's base bytes are bound by live evidence: the only citations are historical records of PRES-5's published page and README and of PRES-5's export manifest, and CP-24's base-tree record (checked against its own base commit). `tests/pres5_landed_code.py` substitutes recorded bytes for `registry.py`, `research.py` and `research_claims.py` and excludes `final_candidate.py`, and PRES-6 adds no module under `src/delu_forecast/`; no freeze manifest names a changed file; `PINS` names none. |
| 7 | W54, W55 and every earlier guard | PASS | `WITHHELD_PATTERNS` holds 35 patterns, W54 and W55 the last two; none fires on the README or on the page's research text; the one page hit (W15) is the protected v1 archive, unchanged since PRES-5. `test_51`'s positive and negative cases pass. |
| 8 | The browser matrix over HTTP, both engines, A2 on the product finding (O48) | PASS | My record (command 12): Chrome 157 and WebKit at 1440, 768, 390, 360 and 320, plus WebKit iPhone 15; `finding_id: product-finding`, header 56 px in every view. 1440×900 (N=2): 1,667.6 / 1,668.3 ≤ 2×900−56 = 1,744. 390×844 (N=3): 2,369.5 / 2,369.3 ≤ 3×844−2×56 = 2,420; finding on screen 2 and 3 respectively. No problems, console errors, failed requests or horizontal overflow; smallest chart text 12.21 px (320); contrast 0 below; keyboard 177 stops in order; touch targets 0 under 44 px at 390; accessibility trees and 54-route discovery pass in both engines. |
| 9 | Packet §8's commands for landing on a moved `main` | PASS, with advisory A6 | Checked without running any external or write action: every command is non-interactive (`--no-pager`, `GH_PAGER=cat`, `commit -F`, `merge --no-edit`); the twin/overlap/staged-equality checks are sound (`xargs git diff --cached --quiet <tip> -- <paths>` and the complement test); the pre-push stdin lines match `secret_guard.py pre-push <remote> <url>`; `publication_receipt.py` takes `--landing --bundle --expect --date` and writes `<date>-publication-receipt.json`, `-postdeploy-links.json`, `-postdeploy-mlflow-mirror.json`; `bundle_sha256`, `check_reader_paths.py release` and `mlflow-routes --mirror-record` exist; `app/space-build.json`'s `files` is a list of `{path, sha256, bytes}`, as the §8.5 one-liner reads it. Repository state matches the packet's premise: `29b6431e` is on `origin/main`, and `main..origin/main` holds only two `delu-daily` commits touching only `live/` (paths listed, no record read). |

### Advisories (not the reason for FAIL)

- **A1.** Packet §10.3 item 1 says A2's phone margin is 25.5 px (2,394.5 against 2,420); the candidate measures 2,369.5
  (Chrome) and 2,369.3 (WebKit), a 50.5 px margin, as packet §7 itself records. Update the open item.
- **A2.** The bins table names its population ("v5's test periods", 358 days, 8,587 hours) but not those periods'
  dates; packet §0 has them. The brief asks each graphic to name its dates.
- **A3.** §0's display rule draws "each day's mean absolute contribution by group"; the chart draws the nine groups
  both days use and states `price_d2` (2.7) beside it, with every group in the values table. Disclosed in packet §10.2;
  acceptable as disclosed.
- **A4.** `reports/presentation/mlflow-export/manifest.json` changed (its `sources` list gains PRES-6's seven files;
  no run or tag changes). It is under `reports/presentation/` but outside the brief's parenthetical ("the release
  checks `pres-6-*` and the MLflow index if a route changes"); packet §6 discloses it, and no evidence binds its bytes.
  The Orchestrator should confirm it in the return.
- **A5.** The first correction's premise for omitting the naive's coverage ("the observed prices on P-all, which are
  not committed") is false for the same reason as the gap, though the omission itself stands on the true ground that
  the naive's hourly intervals are not committed and computing them would recompute another policy.
- **A6.** §8.2's last command, `git --no-pager diff --stat HEAD <evidence_tip_sha> | tail -1`, prints only the summary
  line, while its expectation names files; drop `| tail -1` or use `--name-only`.

## On FAIL only

- Single largest meaningful gap: Product results' whole-population view is restricted to v5's test periods on a false
  premise, and the page publishes that premise as fact — "the only hours whose prices are committed hour by hour" —
  while `data/snapshot.parquet` (committed, pinned by CP-26, `7dd2dc73…`) holds the cleared price of all 49,596 P-all
  hours and, with CP-28's stored A1 rows, reproduces v6's committed daily MAE on all 2,068 days; the README and the
  page's own archive state that the snapshot is committed, so the surfaces contradict each other (the same premise
  stands in packet §0, its first correction, and `research.py`'s `pres6-p-v5` label).
- Exact next acceptance test: at a new candidate, no public surface, claim template or population label says or
  implies that hourly observed prices are committed only for v5's test periods (a `test_51` case refuses the clause);
  the bins view either keeps §0's P-v5 population with a true reason or, under an Orchestrator ruling recorded in the
  packet before any new number, covers P-all from `data/snapshot.parquet` and CP-28's A1 rows; packet §0's premise is
  corrected by a dated disclosure, never rewritten; and `final_candidate --product --check`, the named pytest suites,
  the rebuild-then-clean-status check, `make lint-publication` and the HTTP release check (A2 ≤ 1,744 / 2,420 px, both
  engines) all pass again at that SHA, within 2,000,000 bytes.
