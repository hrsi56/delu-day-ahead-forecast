# Verdict — PRES-6 — Integration — PASS

- Candidate SHA: 4ecfcd094f4b103b57a5f16013a8089ccbd3e9f2
- Plan / version / bar: `capstone_v21.md`, v21-r20, §24.14 "Publishing and going live before 4.7T (v21-r20)", items 5
  and 6, with the checkpoint's brief `docs/track-b/evidence/pres-6/issued-brief.md` (SHA-256
  `bdb78f02894896d2ee1f249355d23351f972cdb217d4d906d22561172f40e5f6`, recomputed at the candidate), its "Observable
  outcome" and "Complete authoritative checkpoint bar".
- Review focus: the focused recheck at the final SHA. The delta `6dfca90f..4ecfcd09` (one commit, three files), the
  resolution of review 2's advisory N1, and review 2's passing items by the delta's reach.
- Plan identity, recomputed with `main`'s `scripts/bar.py` at the candidate: plan SHA-256
  `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`; section 115 lines, 7426 bytes, SHA-256
  `5d38de24b3c68ec01e2f5c4e6eaf368c253485107549fc2d85c3c71ccf2f5349`, equal to the generated brief's.
- Verbatim bar excerpt: the whole section, extracted at the candidate by `bar.py bar … --quote`. The assignment's three
  cited lines are in it: "**The development-period displays** stay on days through 2026-09-06." (item 5) and "**Its
  research numbers use development data only.**" / "**It runs under PUBLISH_RULES 1.5.**" (item 6). They are not
  adjacent in the plan (advisory A4).
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

- Worktree clean before and after: yes. `git -C /Users/djourno/Downloads/PJM/.local/worktrees/pres-6/critic-3 status
  --porcelain` printed nothing at the start, after the product check, the test run, the page rebuild and the lint, and
  before this verdict was written; `HEAD` stayed `4ecfcd094f4b103b57a5f16013a8089ccbd3e9f2`. Git-ignored byproducts
  inside the worktree: `.venv` and `.pytest_cache` (mine, from `uv run`), and a `.DS_Store` that Finder wrote at
  23:51:20 during the review (not mine; the rebuild after it was byte-identical, so it touched no build). No Git write
  of any kind in the repository under review: no commit, branch, tag, stash, push or worktree command. The N1 checks
  ran in a throwaway clone (`git clone --shared --no-tags`) in my scratch folder, which held the scratch commits and
  tags; all scratch tags were deleted and the clone was removed afterwards. The memory directory was not opened.

## Commands actually run

All from `/Users/djourno/Downloads/PJM/.local/worktrees/pres-6/critic-3` unless stated, with
`MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1` exported for every `uv run` and every Python run. `$S` is my scratch
folder `/private/tmp/claude-501/-Users-djourno-Downloads-PJM/42e9ff0c-59d6-4c47-9c7c-d02f4609ac41/scratchpad/critic-3`;
`$C` is the throwaway clone `$S/clone`; `$PY` is the critic worktree's `.venv/bin/python`, run in `$C` with
`PYTHONPATH=$C/src` (confirmed: `registry` loads from `$C/src`, `EVIDENCE_TAGS["evidence/pres-6"] == ('', '2026-11-15')`).

| # | Command | Exit | Observed |
|---|---|---|---|
| 1 | `git status --porcelain`; `git rev-parse HEAD`; `git log --oneline -6`; `date` | 0 | empty; `4ecfcd09…`; parent `6dfca90f`; Sat 2026-11-14 23:50 IST at the start |
| 2 | `git show <sha>:capstone_v21.md \| shasum -a 256`; `git show main:scripts/bar.py \| python3 -I - bar capstone_v21.md "### 24.14 …" --at 4ecfcd09…` (and with `--quote`) | 0 | `80341681…30e6`; section 115 lines, 7426 bytes, `5d38de24…5349`; the three cited lines at plan lines 5603, 5613, 5614 |
| 3 | `shasum -a 256 docs/track-b/evidence/pres-6/issued-brief.md` | 0 | `bdb78f02…40e5f6`, the pin |
| 4 | `git diff --stat` and `--name-status 6dfca90f..4ecfcd09`; `git rev-list --count` | 0 | 1 commit; `A integration-review-2.md` (254+), `M publication-packet.md` (8+), `M tests/test_51_pres6_product_results.py` (8+/11−) |
| 5 | `shasum -a 256 docs/track-b/evidence/pres-6/integration-review-2.md /Users/djourno/Downloads/PJM/.local/artifacts/pres-6/critic-2/integration.md`; `cmp` of the two | 0, 0 | both `12a0cfdac3eada7d3ece153b12b52a61cd7fedcfb04e2376994e65faf7421796`, the expected value; identical |
| 6 | `git diff 6dfca90f..4ecfcd09 -- publication-packet.md tests/test_51_pres6_product_results.py` | 0 | item 1.2 and 1.3 below |
| 7 | `git rev-parse 6dfca90f:<p>` vs `HEAD:<p>` for `docs/index.html`, `README.md`, `reports`, `reports/pres6`, `reports/pres6/product-results`, `reports/cp3/pages_build.json`, `src`, `scripts` | 0 | every object identical (`docs/index.html` `56f3a3ce…`, `README.md` `1254b360…`, `reports` `99c53387…`, `product-results` `c2316e8e…`, `src` `e7f3ed3a…`); only `docs/track-b/evidence/pres-6` differs |
| 8 | `grep -n -A25 "Allowed paths"` and the brief's section list | 0 | `tests/` (apart from `tests/cp18c/`) and `docs/track-b/evidence/pres-6/` are allowed |
| 9 | the `6dfca90f` blob and SHA-256 prefixes of the two modified files, `git grep` over `HEAD`; `git grep test_51 HEAD -- tests/pres5_landed_code.py src/cp26/harness.py '*.json'` (each piped through `head`) | 0 | no output, so no hit: no evidence binds the modified files' earlier bytes |
| 10 | `sed -n 1,40p` and `425,450p tests/test_51…py`; `grep EVIDENCE_TAGS src/delu_forecast/registry.py` | 0 | the new test (item 1.3); registry `"evidence/pres-6": ("", "2026-11-15")` |
| 11 | `cat .github/workflows/tests.yml`; `grep -n "no-tags\|unshallow\|fetch" scripts/leak_scan.py` | 0 | `on: push`; `actions/checkout@v4` with no `fetch-depth`/`fetch-tags`; `uv run pytest -q`; `_fetch` runs `git fetch --no-tags --quiet origin …`, `--unshallow <after>` |
| 12 | `git tag -l evidence/pres-6 land/pres-6` (in the worktree and in the primary checkout) | 0 | nothing: neither tag exists |
| 13 | `uv run python -m delu_forecast.final_candidate --product --check` | 0 | `{"identical_to_committed": {"bins.csv": true, "coverage.csv": true, "days.csv": true, "explanation.csv": true, "monthly.csv": true, "regimes.csv": true, "summary.json": true}}`; status empty after |
| 14 | `uv run pytest -q -rs tests/test_51_pres6_product_results.py tests/test_33_check_links_gate.py tests/test_48_publication_tools.py tests/test_43_publish_rules_migration.py tests/test_30_research_claims_rendered.py` | 0 | `655 passed, 2 skipped in 41.95s`. Skips: `test_51…py:443: the evidence/pres-6 tag is not in this checkout (packet §8.2 checks the date before tagging)` (the changed test, no tag here) and `test_30…py:348: app/public/ is built by make wasm-payload` (not PRES-6's). Review 2 had 656 passed, 1 skipped: the difference is exactly the date test, which now skips where the old fallback passed |
| 15 | `uv run python scripts/build_pages.py --final`; `git status --porcelain`; `shasum -a 256 docs/index.html README.md`; `wc -c docs/index.html`; `git show 6dfca90f:docs/index.html \| shasum -a 256`; same for `README.md` | 0, 0 | `wrote …/docs/index.html (1,997,873 bytes)` and `reports/cp3/pages_build.json`; status empty; page `5e294d40790f3415c14cf932e94f1351e2e99a0b84d6efd3d2321046d7eccdaa`, 1,997,873 bytes, equal to `6dfca90f`'s; README `da9ae187766c895d102676b16a5870540029d471b26687fe78cc3319edc77e1a`, equal to `6dfca90f`'s |
| 16 | `make lint-publication`; `git status --porcelain`; `git rev-parse HEAD` | 0, 0 | `page: 0 finding(s)`, `readme: 0`, `templates: 0`, `PASS`; status empty; `4ecfcd09…` |
| 17 | `git clone --shared --no-tags --no-checkout -q /Users/djourno/Downloads/PJM $C`; `git -C $C tag -l \| wc -l` | 0 | clone made; 0 tags; `origin/main` `29b6431e…` |
| 18 | in `$C`: `git commit-tree <4ecfcd09's tree> -p origin/main` with author and committer date `2026-11-16T10:00:00+0200` (scratch identity via `-c`); `git checkout --detach` it; `git log -1 --format=%cs -- reports/pres6/product-results`; `git rev-list --count HEAD` | 0 | a simulated squash LAND `3dec5de0`, dated 2026-11-16 and the rows' last commit; 272 commits; 0 tags; status clean |
| 19 | in `$C` at the LAND: `$PY -m pytest -q -rs -p no:cacheprovider tests/test_51…py::test_the_evidence_tags_date_is_the_tips` | 0 | `1 skipped`: `the evidence/pres-6 tag is not in this checkout …` |
| 20 | negative control, same place: `6dfca90f`'s version of the test written as `tests/test_51_old_6dfca90f.py` in `$C`, then the same node | 1 | `AssertionError: assert '2026-11-15' >= '2026-11-16'` at the old fallback: the scenario reproduces review 2's N1 |
| 21 | `git init --bare $S/ci.git`; `git fetch --no-tags --depth=1 file://$C 3dec5de0`; `git fetch --no-tags --unshallow file://$C 3dec5de0` (CI's checkout and `leak_scan`'s fetch); `git log -1 --format=%cs evidence/pres-6` | 0, 0, 128 | 0 tags; `fatal: ambiguous argument 'evidence/pres-6': unknown revision …` (exit 128, the test's skip branch); 272 commits |
| 22 | in `$C`, HEAD at the LAND (2026-11-16): `git tag evidence/pres-6 <tip>` for each tip below, the date test, `git tag -d` | — | tip = scratch commit on `4ecfcd09` dated `2026-11-15T00:10:00+0200`: `1 passed` (exit 0); the same as an annotated tag (`cat-file -t` = `tag`): `1 passed` (0); tip = `4ecfcd09` itself (2026-11-14): `1 failed`, the assertion diff `- 2026-11-14 / + 2026-11-15` (1); tip = scratch commit dated `2026-11-16T09:00:00+0200`: `1 failed`, `- 2026-11-16 / + 2026-11-15` (1); afterwards 0 tags |
| 23 | in `$C` at the LAND, old file removed, 0 tags: `$PY -m pytest -q -rs -p no:cacheprovider tests/test_51_pres6_product_results.py` | 0 | `27 passed, 1 skipped`: nothing else in `test_51` depends on the landing's date |
| 24 | `git diff --stat f8fcd723..4ecfcd09 -- src tests scripts Makefile pyproject.toml uv.lock .github`; the registry line diff | 0 | `registry.py` (the date, `2026-11-14` → `2026-11-15`), `research.py`, `research_claims.py` (the fix), `test_51` (one test file): the packet note's N3 sentence |
| 25 | `grep -n` over the packet for `5e294d40`, the date check and the registry; `sed -n 370,385p`, `590,600p`, `700,730p` | 0 | §7 binds `5e294d40…` (served, R4); §8.2's date check; §9.3; §10.4's notes |
| 26 | `rm -rf $C $S/ci.git`; `git status --porcelain --ignored`; `stat` of the ignored entries | 0 | scratch removed; ignored `.DS_Store` (23:51:20), `.pytest_cache/`, `.venv/` only |
| 27 | `git show main:scripts/bar.py \| python3 -I - check /Users/djourno/Downloads/PJM/.local/artifacts/pres-6/critic-3/integration.md --source capstone_v21.md@4ecfcd094f4b103b57a5f16013a8089ccbd3e9f2` (on this verdict) | 0 | see the line after this table |
| 28 | the assignment's excerpt as written (its four `>` lines as one block) through the same `bar.py check` | 1 | `MISMATCH: …:3 is not in any source after the quote's first 2 line(s)` (advisory A4) |

Command 27's observed output: `ok: lines 19–133 (7425 bytes) appear in capstone_v21.md@4ecfcd094f4b` (exit 0): the one quoted block in this verdict is the plan's §24.14, byte for byte.

## Evidence actually inspected

- The generated Critic brief (`critic-brief pres-6`) and the Lead's assignment in it; `AGENTS.md` (role router and
  working-file rules).
- `docs/track-b/evidence/pres-6/integration-review-2.md` in full (the earlier verdict, PASS at `6dfca90f`, advisories
  N1–N5), and its byte identity with `.local/artifacts/pres-6/critic-2/integration.md` (`cmp` and SHA-256 only).
- The whole delta `6dfca90f..4ecfcd09`: the packet's added §10.4 paragraph on review 2 (8 lines), and `test_51`'s
  `test_the_evidence_tags_date_is_the_tips` before and after; the test file's header and imports.
- `src/delu_forecast/registry.py::EVIDENCE_TAGS["evidence/pres-6"]`.
- The issued brief's "Allowed paths" and its rule on bytes bound by earlier evidence.
- `.github/workflows/tests.yml` in full; `scripts/leak_scan.py`'s `_fetch` and its `--unshallow` call.
- Packet §7's release row, §8.2's date check, §9.3's touchpoints table, §10.4's review notes.
- The object identity at `6dfca90f` and the candidate of the page, the README, `reports/` (all committed rows),
  `reports/cp3/pages_build.json`, `src/` and `scripts/`.
- I did not read the Builder's or the Lead's ledger, notes or any other file under `.local/artifacts/pres-6/`; I only
  hashed and compared `.local/artifacts/pres-6/critic-2/integration.md` with the committed review 2.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1.1 | The delta: review 2's verdict committed verbatim | PASS | `integration-review-2.md` SHA-256 `12a0cfda…1796`, equal to the expected value and to the Critic's file, which `cmp` finds byte-identical (command 5). |
| 1.2 | The delta: the packet's note on review 2 | PASS, advisories A1, A3 | Eight added lines in §10.4, nothing else in the packet changed (command 6). Each sentence checks: review 2's PASS at `6dfca90f` and its "no number moves" (review 2 items 1.1, 2.2); N1's account is what commands 19–21 reproduce (the old fallback fails a late landing; GitHub's CI has no tag); "the check now runs only where the tag is present" is the test (item 1.3); N3's "the code delta since is the fix, one test and the date" matches command 24; N4: §7 binds `5e294d40…` as the served page's hash (command 25); N5 as review 2 judged. N2's sentence states a commitment the evidence tip has yet to meet (A1). |
| 1.3 | The delta: `test_51`'s date check | PASS | The fallback through the rows' last commit and the `rev-list --count` skip are removed. The test now asserts the registry date's form unconditionally (`re.fullmatch(r"2026-11-1[4-9]", date)`), skips with a reason when `git log -1 --format=%cs evidence/pres-6` fails or prints nothing, and otherwise asserts equality. Only this function changed; `re` and `pytest` are imported at module level; the docstring's account of GitHub's CI (no tags) matches the workflow and `leak_scan` (command 11). No top-level `evidence/` path exists that `git log` could read as a path instead of the tag. |
| 1.4 | The page, the README and every committed row byte-identical to `6dfca90f`'s | PASS | Git objects identical for `docs/index.html`, `README.md`, `reports/` (all rows, including `reports/pres6/product-results/`), `reports/cp3/pages_build.json`, `src/`, `scripts/` (command 7); the rebuilt page is `5e294d40…`, 1,997,873 bytes, equal to `6dfca90f`'s, and the README `da9ae187…` (command 15). |
| 1.5 | Nothing leaves the allowed paths | PASS | Three files: two under `docs/track-b/evidence/pres-6/`, one under `tests/` outside `tests/cp18c/`, all on the brief's list (command 8). No anchor, governance file, PUBLISH_RULES, template, frozen record or live-product path. No earlier evidence binds the modified files' previous bytes (command 9). |
| 2.1 | N1 resolved: without the tag, as GitHub's CI checks out, the landing's date cannot fail the test | PASS | On a simulated squash LAND dated 2026-11-16 with full history and no tag, the candidate's test skips (command 19); `6dfca90f`'s version fails there (command 20), so the scenario is the one N1 named. CI's fetch shape (`--depth=1`, then `--unshallow`, both `--no-tags`) leaves `git log … evidence/pres-6` at exit 128, the skip branch (command 21). The rest of `test_51` passes on that LAND (command 23). The landing's date no longer enters the test at all: the only unconditional assertion reads the registry. |
| 2.2 | Where the tag is present, the test still requires the registry date to equal the tag's commit date | PASS | Tag at a tip dated 2026-11-15: passes, lightweight and annotated. Tag at `4ecfcd09` (2026-11-14): fails. Tag at a tip dated 2026-11-16: fails. HEAD was the 2026-11-16 LAND throughout, so the outcome follows the tag, not the checkout (command 22). |
| 3.1 | Review 2's passing items still hold, by the delta's reach: the product check | PASS | `--product --check` all seven files `true` (command 13). |
| 3.2 | The named test files | PASS | `655 passed, 2 skipped`, exit 0 (command 14); the second skip is the changed date test, which has no tag to check here. |
| 3.3 | The final build is reproducible and committed | PASS | `build_pages.py --final` leaves `git status --porcelain` empty; page `5e294d40…`, 1,997,873 ≤ 2,000,000 bytes (command 15). |
| 3.4 | `make lint-publication` | PASS | 0 / 0 / 0 findings, `PASS`, status empty (command 16). |
| 3.5 | Review 2's other items (1.1–1.5, 2.1–2.4, 3.1–3.9) | PASS | The delta touches no source, script, page, README, row, release record or packet section other than §10.4's added paragraph (commands 4, 7). So review 2's findings on the fix, the claims, the populations, the release matrix over HTTP (same page bytes, so its served hash and measurements stand) and packet §8 reach this SHA unchanged. Its N1 is resolved (2.1–2.2), N3–N5 are restated accurately, and N2 stays open as A1. |

### Advisories (not grounds for FAIL; for the return and the Orchestrator's landing)

- **A1 — the evidence tip must carry 2026-11-15 (review 2's N2, still open).** The registry dates `evidence/pres-6`
  2026-11-15, and the page labels the product rows "frozen 2026-11-15". The candidate is dated
  2026-11-14 23:48:58 +0200, and this verdict was finished before midnight IST on 2026-11-14. So the commit that adds
  this verdict (the evidence tip) must be committed on or after 00:00 IST, 2026-11-15, in its own +0200 offset. The
  packet's sentence "N2: the evidence tip is committed on 2026-11-15 (local time)" is true only once that happens.
  Packet §8.2's date check (`git log -1 --format=%cs <evidence_tip_sha>` against the registry line, "A different
  date: stop") is the gate. With the fallback gone, GitHub's CI on `main` no longer checks this date. That is
  acceptable: §8.2 is the remedy review 2 named, and any checkout that has the tag still enforces it (2.2).
- **A2 — where the strict branch runs.** After the LAND, the strict comparison runs in any checkout that has the tag
  (the Owner's primary checkout once he tags). I expect it also runs in a GitHub run triggered by pushing the tag
  itself, because `actions/checkout` fetches the pushed tag ref. I did not test that case.
- **A3 — packet §9.3's registry row is stale (outside the delta).** It reads "added; its date set in the final-build
  commit to that commit's date". The final-build commit `6dfca90f` is dated 2026-11-14, but the registry carries
  2026-11-15, the evidence tip's day, as that commit's message, packet §1 and §8.2 say. This is records-only
  wording, unchanged since `6dfca90f`, on no public surface. Worth one word at the next packet edit; not a
  candidate change.
- **A4 — the assignment's excerpt form.** The assignment quotes item 5's last line and item 6's last two lines as one
  `>` block joined by a blank `>` line. They are not adjacent in §24.14, so `bar.py check` rejects that block
  (command 28). Each line is verbatim in the plan at the candidate (command 2), and the generated brief's
  whole-section excerpt, quoted above, passes. This is a form point about the assignment, not the candidate.
- **A5 — byproducts.** A Finder `.DS_Store` appeared in the worktree during the review (Git-ignored). The page was
  rebuilt after it and stayed byte-identical. My scratch clone was in the session scratch folder, outside the
  project's `.local/`, and was removed afterwards (command 26).

## On FAIL only

Not applicable: PASS. (Advisory A1 is the one item that needs an action at the LAND: commit the evidence tip on
2026-11-15 and let packet §8.2's date check confirm it before tagging.)
