# Verdict — PRES-6 — Integration (focused recheck at the final SHA) — PASS

- Candidate SHA: 6dfca90facd1d970019d7d1e0bdd9022b9a84957
- Plan / version / bar: `capstone_v21.md`, v21-r20, §24.14 "Publishing and going live before 4.7T (v21-r20)", items 5
  and 6, with the checkpoint's brief `docs/track-b/evidence/pres-6/issued-brief.md` (SHA-256
  `bdb78f02894896d2ee1f249355d23351f972cdb217d4d906d22561172f40e5f6`, recomputed at the candidate), its "Observable
  outcome" and "Complete authoritative checkpoint bar".
- Plan identity, recomputed with `main`'s `scripts/bar.py` at the candidate: plan SHA-256
  `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6` (revision line "# Capstone v21-r20 — publishing
  and going live before 4.7T"); section 115 lines, 7426 bytes, SHA-256
  `5d38de24b3c68ec01e2f5c4e6eaf368c253485107549fc2d85c3c71ccf2f5349`, equal to the generated brief's.
- Verbatim bar excerpt: the whole section, extracted at the candidate by `bar.py bar … --quote`. The assignment's three
  cited lines are in it: "**The development-period displays** stay on days through 2026-09-06." (item 5) and "**Its
  research numbers use development data only.**" / "**It runs under PUBLISH_RULES 1.5.**" (item 6).
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

- Worktree clean before and after: yes. `git -C /Users/djourno/Downloads/PJM/.local/worktrees/pres-6/critic-2 status
  --porcelain` printed nothing before the review, after the product check, the test run, the page rebuild, the lint and
  the release check, and before this verdict was written; `HEAD` stayed `6dfca90facd1d970019d7d1e0bdd9022b9a84957`.
  The only byproduct inside the worktree is the Git-ignored `.venv` that `uv run` created (and Git-ignored
  `__pycache__`). No Git write of any kind was made; no network call beyond `127.0.0.1`.

## Commands actually run

All from `/Users/djourno/Downloads/PJM/.local/worktrees/pres-6/critic-2`, with `MLFLOW_DISABLE_TELEMETRY=true
DO_NOT_TRACK=1` exported for every `uv run`. My scratch folder, outside the worktree, is
`/private/tmp/claude-501/-Users-djourno-Downloads-PJM/42e9ff0c-59d6-4c47-9c7c-d02f4609ac41/scratchpad/critic-2`
(below: `$S`); my scripts there import nothing from `delu_forecast.final_candidate`.

| # | Command | Exit | Observed |
|---|---|---|---|
| 1 | `git status --porcelain`; `git rev-parse HEAD`; `date` | 0 | empty; `6dfca90facd1d970019d7d1e0bdd9022b9a84957`; Sat 2026-11-14 23:35 IST at the start |
| 2 | `shasum -a 256 capstone_v21.md`; `git show main:scripts/bar.py \| python3 -I - identity capstone_v21.md` | 0 | `80341681…30e6`; revision line "# Capstone v21-r20 — publishing and going live before 4.7T" |
| 3 | `git show main:scripts/bar.py \| python3 -I - bar capstone_v21.md "### 24.14 Publishing and going live before 4.7T (v21-r20)" --at 6dfca90f… --quote` | 0 | section 115 lines, 7426 bytes, `5d38de24…5349`; the assignment's three lines at its lines 76, 86, 87 |
| 4 | `shasum -a 256` of the issued brief, `docs/PUBLISH_RULES.md`, `owner-decisions-2026-11-05.md`, `publication-runbook.md` | 0 | `bdb78f02…40e5f6`, `1bc0c523…f94e`, `4daa5617…0215`, `0f92b92b…f3e9`: the pins |
| 5 | `git diff --stat=200 f8fcd723… 6dfca90f…`; `git log --format='%H %ci %an %s' f8fcd723..6dfca90f`; `git show --stat 1cb0608d` | 0 | 12 files, 13,497+/55−; two commits, `1cb0608d` (23:24:29 +0200, 8 files: the fix and review 1) and `6dfca90f` (23:34:33 +0200: the final build and records) |
| 6 | `git diff f8fcd723… 6dfca90f… -- src tests docs/index.html …/fresh-reader.md reports/cp3/pages_build.json`, `-- …/publication-packet.md`, `-- …/pres-6-local-release.json` | 0 | item 2 below |
| 7 | `git rev-parse f8fcd723:…/pres-6-local-release.json HEAD:…/pres-6-local-release-attempt-5.json`; `cmp docs/track-b/evidence/pres-6/integration-review-1.md /Users/djourno/Downloads/PJM/.local/artifacts/pres-6/critic-1/integration.md` | 0, 0 | both `b303c70b3fbb…`; the committed review 1 is byte-identical to its Critic's file |
| 8 | packet §0 extracted at `e049bdf0`, `72e688e2`, `f8fcd723`, `HEAD` and diffed; `git log -1 --format='%h %ci'` of `e049bdf0`, `df08d772`; `git show --stat df08d772` | 0 | §0 at `72e688e2` equals §0 at `f8fcd723`; `f8fcd723`→`HEAD` is two insertions only (6 and 4 lines), no line removed or changed; §0 13:31:25, the first rows (`bins.csv` among them) 13:33:20 |
| 9 | `git grep -n -i -E` over the tree for the clause's variants (`committed hour`, `committed hourly`, `prices are committed`, `with committed observed`, `not committed`, `prices on P-all`, `only … test periods`), and `observed price \| hourly price \| … committed` over PRES-6's surfaces and evidence | 0 | at the candidate the clause stands only in packet §0's two original sentences, each followed by its dated disclosure, in those disclosures and §10.2's, `fresh-reader.md`'s disposition (quoted as the withdrawn reason), `integration-review-1.md` and `test_51`'s regex; `pres6-claims.md`'s C1006 row does not carry it |
| 10 | `uv run python -m delu_forecast.final_candidate --product --check` | 0 | `{"identical_to_committed": {"bins.csv": true, "coverage.csv": true, "days.csv": true, "explanation.csv": true, "monthly.csv": true, "regimes.csv": true, "summary.json": true}}` |
| 11 | `uv run pytest -q -rs tests/test_51_pres6_product_results.py tests/test_33_check_links_gate.py tests/test_48_publication_tools.py tests/test_43_publish_rules_migration.py tests/test_30_research_claims_rendered.py` | 0 | `656 passed, 1 skipped in 43.03s` (review 1: 654 + the two new `test_51` cases); the skip is `tests/test_30_research_claims_rendered.py:348: app/public/ is built by make wasm-payload`, not PRES-6's |
| 12 | `git tag -l evidence/pres-6 land/pres-6` | 0 | nothing: neither tag exists yet |
| 13 | `uv run python scripts/build_pages.py --final`, then `git status --porcelain`; `shasum -a 256 docs/index.html README.md`; `wc -c docs/index.html` | 0, 0 | `wrote …/docs/index.html (1,997,873 bytes)` and `reports/cp3/pages_build.json`; status empty; page `5e294d40790f3415c14cf932e94f1351e2e99a0b84d6efd3d2321046d7eccdaa`, README `da9ae187…77e1a` (review 1's, unchanged) |
| 14 | `make lint-publication`, then `git status --porcelain` | 0, 0 | `page: 0 finding(s)`, `readme: 0`, `templates: 0`, `PASS`; status empty |
| 15 | `python3 -m http.server --bind 127.0.0.1 8797 --directory docs`; `curl -s -o /dev/null -w '%{http_code}' …/index.html`; `curl -s …/index.html \| shasum -a 256`; `\| wc -c` | — / 0 | 200; served `5e294d40…ccdaa`, 1,997,873 bytes (server stopped afterwards) |
| 16 | `PLAYWRIGHT_BROWSERS_PATH=/Users/djourno/Downloads/PJM/.local/tools/ms-playwright /Users/djourno/Downloads/PJM/.local/tools/playwright/bin/python scripts/check_reader_paths.py release http://127.0.0.1:8797/index.html --shots $S/shots --out $S/release.json` | 0 | `passed=True`, checked 2026-11-14T21:46:55Z; Chrome 157.0.8103.51 and WebKit 26.6 at 1440, 768, 390, 360 and 320, plus WebKit iPhone 15; item 3.8 |
| 17 | `.venv/bin/python -I $S/scripts/periods.py <worktree>`: CP-24's `predictions.parquet` folds against `daily-losses.parquet`'s A1 days, and `data/snapshot.parquet`'s priced days | 0 | fold_1 2020-07-01..09-28, 0 days in P-all; fold_2 2021-04-01..06-29 (90), fold_3 2022-07-01..09-28 (88), fold_4 2025-05-01..07-29 (90), fold_5 2026-01-08..04-07 (90); P-v5 358 days, 2021-04-01 to 2026-04-07 (`summary.json`: 358 days, 8,587 hours, folds 2–5); the snapshot prices 2,068 of 2,068 P-all days |
| 18 | `.venv/bin/python -I $S/scripts/surfaces.py <worktree>`: `test_51`'s `FALSE_PRICE_CLAUSES` (read from the test file) and my own broader pattern over the page text, README, `research.py` and the `PRES6_BLOCKS` source at `f8fcd723` and at the candidate; `RC.withheld_findings` over README and page text; every `<data value data-claim data-record>` element of both pages | 0 | at `f8fcd723` the test's regex fires on the page, `research.py` and `PRES6_BLOCKS` (README clean); at the candidate it fires on none, nor does mine; withheld: README `[]`, page `W15: 'coverage guarantee'` only (the protected v1 archive, as in review 1); 836 `<data>` elements on each page, identical in value, claim, record and text |
| 19 | `.venv/bin/python -I $S/scripts/recompute.py <worktree>`: my own recomputation from the pinned inputs of `regimes.csv` (days, hours, spans, both scores, the ratios), `coverage.csv`, `monthly.csv`, `bins.csv` (P-v5 joined to A1's stored quantiles, ten equal bins by median) and the three chosen days | 0 | `PROBLEMS none`; P-v5 358 days, 8,587 hours; chosen 2021-06-16 (of 90), 2022-07-26 (of 88), 2025-05-02 (of 180), equal to `days.csv` |
| 20 | `.venv/bin/python -I $S/scripts/datetest.py <worktree>`: `test_51::test_the_evidence_tags_date_is_the_tips` with `git` answers simulated as GitHub's CI would give them after the LAND (no tag; full history; the rows last touched by the squash commit) | 0 | landing dated 2026-11-15: PASS; dated 2026-11-16: `AssertionError` (advisory N1) |
| 21 | for each file the delta modifies: its `f8fcd723` SHA-256 and blob prefix searched with `git grep` over `HEAD` | 0 | only `docs/index.html`'s `48fef1a0…` is cited, by `integration-review-1.md` and packet §7, as the history of review 1's page; no other pre-delta bytes are bound |
| 22 | `sed -n 1,9p .github/workflows/tests.yml` and its steps; `grep` of `daily.yml` for its pushes; `sed -n 396,420p scripts/leak_scan.py` | 0 | `on: push`; `actions/checkout@v4` (no tags); Python 3.12; `ci_range` runs `git fetch --no-tags --quiet origin --unshallow <after>`; the runner pushes with `github.token` |
| 23 | `git show main:scripts/bar.py \| python3 -I - check /Users/djourno/Downloads/PJM/.local/artifacts/pres-6/critic-2/integration.md --source capstone_v21.md@6dfca90facd1d970019d7d1e0bdd9022b9a84957` (on this verdict) | 0 | `ok: lines 17–131 (7425 bytes) appear in capstone_v21.md@6dfca90facd1` |

## Evidence actually inspected

- The generated Critic brief (`critic-brief pres-6`) and the Lead's assignment in it; `AGENTS.md` (role router).
- `docs/track-b/evidence/pres-6/integration-review-1.md` in full (the earlier verdict, FAIL at `f8fcd723`).
- The full delta `f8fcd723..6dfca90f`: the diffs of `docs/index.html`, `src/delu_forecast/registry.py`,
  `src/delu_forecast/research.py`, `src/delu_forecast/research_claims.py`, `tests/test_51_pres6_product_results.py`,
  `docs/track-b/evidence/pres-6/fresh-reader.md`, `docs/track-b/evidence/pres-6/publication-packet.md` (all 32+/12−
  lines), `reports/cp3/pages_build.json`, `reports/presentation/release-checks/pres-6-local-release.json`; the new
  `pres-6-final-prerelease.json` (every check row); `pres-6-local-release-attempt-5.json` by blob identity only.
- Packet §0 at `e049bdf0`, `72e688e2`, `f8fcd723` and the candidate; packet §7, §8.1–§8.3, §9, §10.2–§10.4.
- The issued brief's allowed paths (its "Allowed paths" list) and its review outcome 9; the runbook's §9
  (`publication-runbook.md`, `0f92b92b…f3e9`, equal to the brief's pin).
- `docs/track-b/research-content/pres6-claims.md`'s C1006 row; `research.py`'s `POPULATIONS`; `PRES6_BLOCKS`'s
  `outcomes.bins` template.
- The committed product rows `reports/pres6/product-results/*.csv` and `summary.json`; the four pinned inputs
  (`daily-losses.parquet`, `hourly.parquet`, CP-24's `predictions.parquet`) and `data/snapshot.parquet`, read by my own
  scripts.
- `.github/workflows/tests.yml` (trigger, checkout, Python 3.12), `.github/workflows/daily.yml` (its pushes use
  `github.token`), `scripts/leak_scan.py::ci_range` (`git fetch --no-tags … --unshallow`).
- My own release record (`release.json` in my scratch folder) and the committed `pres-6-local-release.json`.
- I did not read the Builder's or the Lead's ledger, notes or any other file under `.local/artifacts/pres-6/`; I only
  compared the committed `integration-review-1.md` byte for byte with `.local/artifacts/pres-6/critic-1/integration.md`
  (`cmp`), without reading the latter otherwise.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1.1 | Review 1's acceptance test: no public surface, claim template or population label says hourly prices are committed only for v5's test periods | PASS | The bins' text now reads "…that falls on an eligible development day (four periods between 2021-04-01 and 2026-04-07), the population fixed before any bin was drawn, 8,587 hours on 358 days…"; `research.py`'s `pres6-p-v5` label is "the 358 days of v5's test periods 2 to 5 inside CP-26's days". No hit at the candidate on the page, README, `PRES6_BLOCKS`, `research.py`'s `POPULATIONS` (commands 9, 18); `registry.py` has none; `pres6-claims.md`'s C1006 never carried it. MLflow and the Space are untouched by the delta. The packet keeps the original sentences only under their dated disclosures, as item 1.4 requires. |
| 1.2 | A `test_51` case rejects the clause | PASS | `test_no_surface_says_hourly_prices_are_committed_only_for_v5s_periods`: proves the premise false from `data/snapshot.parquet` (priced days include 2020-12-29, 2022-07-26, 2026-09-06), then refuses four phrasings on the page text, README, the `PRES6_BLOCKS` templates and `POPULATIONS`, with a negative control. Its regex fires on `f8fcd723`'s page, template and label and on none at the candidate (command 18); it passes in command 11. |
| 1.3 | The bins view keeps §0's population with a true reason (or covers every day under a recorded ruling) | PASS, advisory N5 | P-v5 kept; no ruling needed or made. "The population fixed before any bin was drawn" is true: §0 named "every scored hour of P-v5" at `e049bdf0` (13:31:25), before `bins.csv` first appeared at `df08d772` (13:33:20) (command 8). The added dates are right: folds 2–5 inside P-all are four periods, 2021-04-01 to 2026-04-07, 358 days (command 17), which also answers review 1's advisory A2. `bins.csv` and the 836 data values are unchanged (commands 10, 18, 19). |
| 1.4 | §0's premise corrected by a dated disclosure, not rewritten | PASS | §0 from `f8fcd723` to the candidate gains two sub-bullets and loses or changes nothing (command 8): "*Disclosure, 2026-11-14, after Integration review 1 (FAIL at `f8fcd723`), not a rewrite:* 'where committed hourly observed prices exist' is false…", and the matching one under the coverage correction ("half false … the conclusion stands"). Both are true: the snapshot prices all 2,068 P-all days (command 17); CP-28's `hourly.parquet` holds arms A1–A7 only, and `daily-losses.parquet`'s B0 rows have no coverage (0 non-null), so the naive's coverage stays uncomputed. The date matches `1cb0608d` (2026-11-14 23:24 +0200). §10.2 adds the disclosure. |
| 1.5 | All the reproduction checks pass again at this SHA, including the HTTP release check; page ≤ 2,000,000 bytes | PASS | `--product --check` all `true` (10); 656 passed, 1 unrelated skip (11); `build_pages.py --final` then status empty, page `5e294d40…`, 1,997,873 bytes (13); lint 0/0/0 PASS (14); served page 200, same hash and size (15); the HTTP release check `passed` true (16), the product finding at 1,667.6 / 1,668.3 px ≤ 1,744 (1440×900) and 2,369.5 / 2,369.3 px ≤ 2,420 (390×844). |
| 2.1 | The delta, file by file: each change is the fix, a review-1 advisory, the final build or a record | PASS, advisories N1, N3 | **Fix** (`1cb0608d`): `docs/index.html` (the bins paragraph), `research_claims.py` (its template), `research.py` (the label), `test_51` (the clause test), packet §0 and §10.2 (the two disclosures), `fresh-reader.md` (D07's disposition: "Repaired, then corrected", quoting the withdrawn reason). **Review 1's advisories**: A1 (§10.3 item 1 now 50.5 px, 2,369.5 against 2,420), A2 (the periods' dates on the page), A5 (§0's coverage disclosure), A6 (§8.2's last check now `--name-only … \| grep -v '^live/' ; echo landed-tree-checked`); A3 and A4 stay as disclosed (§10.4). **Final build** (`6dfca90f`): `registry.EVIDENCE_TAGS["evidence/pres-6"]` `("", "2026-11-14")` → `("", "2026-11-15")`, which moves the page's five "frozen" labels of `evidence/pres-6` links to 2026-11-15 (the `evidence/cp-17` link keeps 2026-10-28); `pages_build.json` bytes 1,997,761 → 1,997,873; `test_the_evidence_tags_date_is_the_tips` (see N1). **Records**: `integration-review-1.md` (byte-identical to its Critic's file, command 7); `pres-6-final-prerelease.json` (at `f8fcd723`, see N3); `pres-6-local-release-attempt-5.json` (the old record, same blob `b303c70b`); `pres-6-local-release.json` (the final page: `checked_at` 21:34:14 UTC, page heights +26 px from the longer bins text, contrast `checked` +2 for the two date spans, `release-http-7` paths; nothing else); packet §7, §9, §10.3, §10.4 numbers and rows. |
| 2.2 | No number moves | PASS | `reports/pres6/` is not in the delta; `--check` identical (10); my recomputation `PROBLEMS none` (19); the 836 `<data>` elements of the two pages are identical (18); README unchanged (`da9ae187…`). The only changed figures are the page's own size (1,997,873) and the release record's measurements, both re-measured here. |
| 2.3 | Nothing leaves the allowed paths | PASS | All 12 files are under the brief's list (`docs/index.html`, `reports/cp3/pages_build.json`, `src/delu_forecast/`, `tests/` outside `tests/cp18c/`, `reports/presentation/` release checks `pres-6-*`, `docs/track-b/evidence/pres-6/`). No anchor, governance file, PUBLISH_RULES, template, frozen record or live-product path; no pre-delta bytes bound by evidence (21). |
| 2.4 | No new claim lacks a record | PASS | New page text: the two dates (structural spans; packet §0 and CP-24's rows, command 17) and "the population fixed before any bin was drawn" (packet §0's commit order, command 8); new labels "frozen 2026-11-15" (the registry, guarded by packet §8.2's date check; N2). New packet claims: the prerelease (its record), the HTTP release (my rerun, 1.5), the budget (13). |
| 3.1 | Review 1's outcomes 1–10 still hold | PASS | The page differs from `f8fcd723`'s in two lines only (the bins paragraph and the evidence row), so the A8 order, the opening, Product results' five items, Business insights, the README glance, R1–R7 and the withheld guard stand as review 1 found them; my release record has `order: A8` and `finding_id: product-finding` in all 11 views, and A5's 54 routes pass in both engines at both placement sizes. Outcomes 5–6: `test_33`, `test_48` pass (11). Outcome 8: 1,997,873 ≤ 2,000,000. Outcome 9: editorial, fresh reader, review 1 (FAIL) committed; this recheck. Outcome 10: §8 (3.9). |
| 3.2 | The rules fixed first | PASS | §0's order unchanged (`e049bdf0` → `beac7da6` → `df08d772` → `72e688e2` → `cb48bd92`); the delta only appends dated disclosures (8). |
| 3.3 | Every number re-derives | PASS | Commands 10 and 19; `test_51`'s re-derivation cases pass (11). |
| 3.4 | No fit or recomputation of another policy | PASS | `final_candidate.py` is not in the delta; the disclosure keeps the naive's coverage uncomputed and P-v5 as fixed. |
| 3.5 | Nothing after 2026-09-06 | PASS | No new data or row; the new dates are 2021-04-01, 2026-04-07 (data) and 2026-11-14/15 (process dates). `daily-losses.parquet` ends 2026-09-06 (19). |
| 3.6 | The allowed paths | PASS | Item 2.3. |
| 3.7 | The withheld claims | PASS | W54/W55 cases pass (11); README `[]`, page only W15 in the protected v1 archive (18). |
| 3.8 | The browser matrix over HTTP, A2 on the product finding (O48) | PASS | My record (command 16), over HTTP from `127.0.0.1`: Chrome 157.0.8103.51 and WebKit 26.6 at 1440, 768, 390, 360 and 320, plus WebKit iPhone 15; `finding_id: product-finding`, header 56 px in every view. A2: 1440×900 (N = 2): 1,667.6 / 1,668.3 ≤ 2 × 900 − 56 = 1,744, the finding on screen 2; 390×844 (N = 3): 2,369.5 / 2,369.3 ≤ 3 × 844 − 2 × 56 = 2,420, on screen 3; equal to the committed record's values. Every view: 0 problems, 0 console errors, 0 failed requests, 0 HTTP errors, 0 resources after the document, 0 px overflow with disclosures open, scroll width equal to client width. Smallest chart text 12.21 px (320) in both engines. Keyboard: 177 stops in document order, 0 without visible focus, both engines; touch targets at 390: 0 under 44 px of 252; contrast: 0 below at 1440 and 390; zoom 200 % and 320 reflow: 0 px overflow; accessibility trees: no unnamed, unexposed or wrong-state element in the four views; discovery: 54 routes, `passed` true, in all four. The record states no real Safari, iPhone or screen reader was used. |
| 3.9 | Packet §8's commands | PASS, advisories N1, N2 | §8.2's changed last check is sound: after the squash commit, `git diff --name-only HEAD <evidence_tip_sha>` lists exactly `main`'s own movement since `87811abc`, and the `; echo` ends it whatever `grep` returns; every command stays non-interactive. The date check (`git log -1 --format=%cs <tip>` against the registry line) guards N2. Nothing else in §8 changed. |

### Advisories (not grounds for FAIL; for the return and the Orchestrator's landing)

- **N1 — the new date test fails on GitHub's CI unless the LAND is dated 2026-11-15.**
  `test_51::test_the_evidence_tags_date_is_the_tips` falls back, when the tag `evidence/pres-6` is absent, to
  `assert date >= <date of the last commit touching reports/pres6/product-results>`. That holds on `gauntlet/pres-6`
  (the rows' last commit is `cb48bd92`, 2026-11-14), but on `main` the rows' last commit becomes the LAND's squash
  commit. GitHub's `invariant-tests` (`on: push`, `actions/checkout@v4` without tags) runs `leak_scan.py ci`, whose
  `ci_range` runs `git fetch --no-tags … --unshallow`: full history, no tags, so the fallback is taken and the
  `rev-list --count` skip does not apply. Simulated (command 20): a landing dated 2026-11-15 passes, 2026-11-16
  fails. A later landing would leave `main`'s GitHub CI red on that push and on every later human push, and only a
  code change through a checkpoint could repair it (the daily runner pushes with `github.token`, which triggers no
  run). Packet §8.2 checks that the evidence tip's date equals the registry's, but does not require the LAND on the
  same day. Either land on 2026-11-15 (the date `%cs` prints in the commit's own offset, +0200 on this Mac), or,
  before landing on a later day, make the fallback skip when the tag is absent and history exists (a new candidate
  and recheck).
- **N2 — the evidence tip must carry 2026-11-15.** The page labels PRES-6's rows "frozen 2026-11-15" and the
  registry says so; the candidate itself is dated 2026-11-14 23:34 +0200. The commit that adds this verdict (the
  evidence tip) must be dated 2026-11-15 in its own offset. This verdict was finished at 2026-11-14 23:47 IST, so
  it must not be committed before 00:00 IST. Packet §8.2's date check stops the LAND otherwise.
- **N3 — the final-stage prerelease record is at `f8fcd723`, not at this SHA.** It is labelled so in packet §7 and
  the record's `head`, and the runbook places the prerelease before the independent check. It records two
  `UNEXPECTED` steps, both disclosed: the Python 3.12 run's one failure (`test_refreeze17c`'s 3.13 pin, also in
  PRES-5's and PRES-6's pre-final records) and five `blob/evidence/pres-6/…` links that answer 404 until the tag is
  pushed. The delta `f8fcd723..6dfca90f` changes two page lines, three source lines, one test file and records;
  this recheck's own reruns at the final SHA cover the named checks, not the full 3.13/3.12 suites.
- **N4 — the committed HTTP release record does not itself hold the served page's SHA-256** (neither did
  attempt 5's); packet §7 binds `5e294d40…` beside it (R4 as applied in review 1). My served page has that hash.
- **N5 — the bins' reason is procedural.** "The population fixed before any bin was drawn" is true (§0 at
  `e049bdf0` precedes `bins.csv` at `df08d772`) but does not say why v5's periods were chosen; the reason first given
  is withdrawn by §0's dated disclosure, which the page's evidence row ("The rules, fixed before the computation")
  links. Acceptable as is.

## On FAIL only

Not applicable: PASS. (Advisory N1 is the one item that needs an action before or at the LAND: land on 2026-11-15, or
change the date test's fallback first.)
