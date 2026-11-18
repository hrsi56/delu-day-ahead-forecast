# Verdict — PRES-7 — Integration — PASS

Focused recheck at the final candidate.

- Candidate SHA: `e464b69e80902d029272628e6c35fa21fb9c1ed3`
- Plan / version / bar: `capstone_v21.md`, v21-r20 (file SHA-256 `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`, recomputed at the candidate), §16.3 "What the product and demo expose" and §24.14 "What stays exactly as registered"; the brief `docs/track-b/evidence/pres-7/issued-brief.md` (SHA-256 `b6a45b6002969c238547938661841e74f7b44f343fc60e3a56ced02879451175`, recomputed); PUBLISH_RULES 1.5 §10.1 (an exact-candidate PASS loses its coverage for subsequently changed content until a focused recheck). Scope: the delta from Integration review 1's candidate `364ac020e364dea0332ebf52c9ff0ca045d6b364`.
- Verbatim bar excerpt:

> Scientific graphics separate development, unused-data and prospective results. Business
> interpretation must separate forecast performance from an evaluated economic decision policy.
> Cumulative net profit/value, returns or business success rates require a frozen use case,
> constraints, costs, benchmark, denominator, complete time series and loss/risk disclosure;
> label simulated versus realized results. Without authorized evaluation, show the specific gap

  (The excerpt is the citation. Any line number is a courtesy and is non-binding.)
- Worktree clean before and after: yes (`git status --porcelain` empty before, after the rebuild, after the tests and before writing this verdict; `HEAD` `e464b69e…` throughout). The only byproduct is the gitignored `.venv/` that `uv run` created.

## Commands actually run

All from `/Users/djourno/Downloads/PJM/.local/worktrees/pres-7/critic-2`, with `MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1` exported for every `uv run`.

1. `git status --porcelain` → exit 0, empty. `git rev-parse HEAD` → `e464b69e80902d029272628e6c35fa21fb9c1ed3`.
2. `git diff --name-only 364ac020e364dea0332ebf52c9ff0ca045d6b364 e464b69e80902d029272628e6c35fa21fb9c1ed3` → exit 0:
   `docs/track-b/evidence/pres-7/integration-review-1.md`, `docs/track-b/evidence/pres-7/publication-packet.md`,
   `reports/presentation/release-checks/pres-7-candidate-prerelease.json`,
   `reports/presentation/release-checks/pres-7-local-release.json`. `git log 364ac020..e464b69e` → one commit, `e464b69e`.
3. `git diff --quiet 364ac020… e464b69e… -- docs/index.html README.md reports/cp3/pages_build.json` → exit 0 (identical).
4. `shasum -a 256 capstone_v21.md docs/track-b/evidence/pres-7/issued-brief.md` → `80341681…30e6`, `b6a45b60…1175` (as briefed).
5. `uv run python scripts/build_pages.py --final` → exit 0; "wrote …/docs/index.html (2,082,672 bytes) and …/docs/.nojekyll", "wrote …/reports/cp3/pages_build.json".
6. `uv run python scripts/readme_research.py` → exit 0; "regenerated the glance and generations blocks of …/README.md".
7. `git status --porcelain` → exit 0, empty.
8. `make lint-publication` → exit 0; "page: 0 finding(s)", "readme: 0 finding(s)", "templates: 0 finding(s)", "PASS — the reading path and the template sources meet the standard's §4 and §5 rules".
9. `uv run pytest -q tests/test_52_pres7_business_insights.py tests/cp29` → exit 0; "51 passed in 16.49s" (no skips; HiGHS solver chatter on stderr only).
10. `git status --porcelain` → exit 0, empty. `shasum -a 256 docs/index.html README.md` → `7fd8dd2f462da049942dd438a14c8538bdc09536bdfa8760bfffbbd73abafc5e`, `efe8c08da7d03861e9b6075e6bc28f8fe321d749d44e56e965699b94547c07d1`.
11. A scratch script (outside the worktree) importing `delu_forecast.research_claims` and comparing every row of packet §5's table with `render(key, "md", surface=README)` for README blocks and `render(key, "md", surface=PAGE)` for page-only blocks → exit 0; 12 rows, every claim ID matches its block; 11 rows byte-equal; `economics.risk_aware` (C1203, page-only) differs only by the markdown emphasis on its lead phrase. A second check: that row equals the page's visible text (the block's HTML render with tags stripped) exactly, and appears verbatim in `docs/index.html`'s visible text → `page-text-equal: True`, `in page visible text: True`.
12. Rendered each README business block from the claim layer and located it in `README.md` → each found exactly once, in the order `business.use`, `business.measured`, `economics.setup` (C1101), `economics.finding` (C1102), `economics.caveat` (C1108), `economics.difference` (C1103), `economics.untraded` (C1202), `economics.v5` (C1104), `economics.risk` (C1105), `economics.sensitivity` (C1106), `economics.regimes` (C1107), `economics.limits` (C1108), `economics.assumptions` (C1204), `business.gap`, `business.limits`.
13. `git diff --name-only a5db292aa0aed68886ea0ab7237cf5fe9a672b65 e464b69e -- src/` → `src/delu_forecast/{publication_lint,registry,research,research_claims}.py` (four). `tests/pres5_landed_code.py` lines 32–34 record `derived.py`, `publication_lint.py`, `registry.py`, `research.py`, `research_claims.py`. `uv run python -c "…from cp26 import harness as H…"` → "25 pins; changed by PRES-7 and pinned: []".
14. `grep` of `docs/track-b/research-content/pres7-claims.md` → its rewording list names C1101, C1102, C1103, C1104 and C1108.
15. `grep '"evidence/pres-7"' src/delu_forecast/registry.py` → `"evidence/pres-7": ("", "2026-11-18"),`. `git log -1 --format='%cs %ci' e464b69e` → `2026-11-18 2026-11-18 18:26:36 +0200`.
16. Python reads of `pres-7-candidate-prerelease.json` and `pres-7-local-release.json` (fields, pass flags, per-view `problems`, 64-hex strings), and a leaf-by-leaf diff of `pres-7-local-release.json` against `pres-7-local-release-attempt-4.json` → 10,051 leaves each, 32 differ (results under item 3 below).
17. `git diff --word-diff=porcelain 5575920c 364ac020 -- docs/index.html` and `git show <c>:docs/index.html | shasum -a 256` for `5575920c`, `364ac020` → the only page changes after attempt 4's page: C1202 gains "by design (its input rules fail closed there)", C1104 gains "(the eligible days inside them)", the evidence date 2026-11-16 → 2026-11-18; hashes `d2358f0f…` and `7fd8dd2f…`.
18. Read-only `grep` of the prerelease's raw logs, `/Users/djourno/Downloads/PJM/.local/worktrees/pres-7/prerelease/.local/artifacts/prerelease/2026-11-18/07-…pytest-q.log` and `15-links.log` → "FAILED tests/cp17c/test_refreeze17c.py::test_the_committed_manifest_verifies_here" ("CPython 3.12.14 here, 3.13.15 pinned"), "1 failed, 3497 passed, 20 skipped"; links: one 404, `https://github.com/hrsi56/delu-day-ahead-forecast/blob/evidence/pres-7/docs/track-b/evidence/pres-7/publication-packet.md`, the only failed destination.
19. `awk` of `reports/cp29/paired.csv` (P-all, median, v6 − naive, wear 25) → total 37076.825…, interval 32322.648…, 42311.211…; 2,068 days; 14-day blocks, 2,000 replicates, seed 20261115.
20. `git merge-base --is-ancestor c61757d8 main` → on main; `git log -1 c61757d8` → 2026-11-18, "Land CP-18d: …"; its paths: `.github/workflows`, `docs/track-b`, `reports/cp18d`, `scripts/build_product_space.py`, `space-product/app`, `src/cp18`, `tests/cp18a`, `tests/cp18c`, `tests/cp18d`. `git show main:src/cp18/runner_artifact.py` → `verify` takes `--artifact` (required), `--record`, `--out`; the record is `space-artifact.json` with `deleted_arrays` rows carrying `path`.
21. Prior prerelease records `pres-5-*-prerelease.json`, `pres-6-*-prerelease.json` → each has the CI 3.12 pytest step at one failure; the PRES-5 and PRES-6 packets name `test_the_committed_manifest_verifies_here` under 3.12.
22. `git show main:scripts/bar.py | python3 -I - check /Users/djourno/Downloads/PJM/.local/artifacts/pres-7/critic-2/integration.md --source capstone_v21.md@e464b69e80902d029272628e6c35fa21fb9c1ed3`, run after writing. First run: exit 1, "MISMATCH: …integration.md:7 is not in any source …: 'Business interpretation must separate forecast performance from an evaluated economic decision policy.'". The excerpt had been copied from the Lead's assignment, which reflows the plan's lines (same words, different line breaks). The excerpt above now quotes the plan's whole lines verbatim. Rerun: exit 0, "ok: lines 9–13 (456 bytes) appear in capstone_v21.md@e464b69e8090". The worktree was still clean afterwards and `HEAD` was `e464b69e…`.

## Evidence actually inspected

- `docs/track-b/evidence/pres-7/integration-review-1.md` in full: its PASS at `364ac020`, its observations 1–5, command 11 (its own release check at `7fd8dd2f…`, A2 reproduced), the 44 `cp29.*` bindings, the 15 `tests/test_22` failures/errors in its own full run.
- `git diff 364ac020 e464b69e -- docs/track-b/evidence/pres-7/publication-packet.md` in full, and packet §§1, 3, 4, 5, 7, 8.0–8.2, 8.5, 10.3 item 5, 10.4 at the candidate.
- `reports/presentation/release-checks/pres-7-candidate-prerelease.json` (in full) and `pres-7-local-release.json` (fields, flags, views, discovery, keyboard block; diffed against attempt 4).
- The claim layer `src/delu_forecast/research_claims.py` (`render`, `render_template`, `BLOCKS`), `src/delu_forecast/registry.py::EVIDENCE_TAGS`, `tests/pres5_landed_code.py`, `src/cp26/harness.py::PINS`, `docs/track-b/research-content/pres7-claims.md`, `reports/cp29/paired.csv`, `README.md`, `docs/index.html`, `main:src/cp18/runner_artifact.py`.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1 | Every changed path since `364ac020` is under `docs/track-b/evidence/pres-7/` or `reports/presentation/release-checks/pres-7-*`; `docs/index.html`, `README.md`, `reports/cp3/pages_build.json` and all code and tests byte-identical | PASS | Commands 2–3: four paths, two in each allowed location; one commit in the range; `git diff --quiet` on the three named files exits 0; no `src/`, `scripts/`, `tests/` or other path appears in the name list |
| 2a | Note 1: §5's table equals what the claim layer renders now; the README list is complete | PASS | Command 11: all 12 rows carry their blocks' claim IDs; the 10 README rows are byte-equal to the README rendering; the page-only `economics.chart` is byte-equal; the page-only `economics.risk_aware` equals the page's visible text exactly (its markdown source bolds the lead phrase "A more cautious rule.", which the table renders as plain text, as the page shows it). The table now holds the post-review texts review 1 found stale ("Not evaluated.", "Paired over the same days", +37,080 [+32,320, +42,310], "by design (its input rules fail closed there)", the chart line with 85 %, empty start/end, €0.10 and `720fc581…`). Command 12: the README list in §5 (`business.use`, `business.measured`, C1101, C1102, the class caveat, C1103, C1202, C1104–C1108, C1204, `business.gap`, `business.limits`) is exactly the README's blocks in the README's order |
| 2b | Note 2: §3 names C1101–C1104 and C1108 | PASS | §3 reads "C1101, C1102, C1103, C1104 and C1108 are reworded on every surface, their claims and records unchanged (the claim map records each change …)"; command 14: `pres7-claims.md` lists the same five. §10.1's C1103 bullet carries the final wording, matching the rendered `economics.difference` |
| 2c | Note 3: §7's binding row names four modules | PASS | Command 13: exactly four `src/delu_forecast/` modules changed since `a5db292a` (`research.py`, `research_claims.py`, `registry.py`, `publication_lint.py`), all four among the five `tests/pres5_landed_code.py` records; `PINS` (25 entries) binds none of PRES-7's changed paths. The row's conclusion stands |
| 2d | Note 4: §7 records the prerelease at the candidate and the release check at the final page | PASS | §7's new prerelease row matches the record exactly (head `364ac020`, `stage` final, 10:02–10:57 UTC, 3.13: 3,501 passed / 17 skipped; 3.12: 3,497 / 20 / 1 failed; links 1 failed; verify, lint, rebuild with 0 changed paths, guard pass). The browser row cites `pres-7-local-release.json` at the final page, 16:26 UTC, with A2's four numbers; attempts 2–4 kept and attributed to their pages (`306c6096`, `5575920c`) |
| 2e | Each changed packet statement is true against the repository | PASS | §4(b): `paired.csv` gives 37,076.8 [32,322.6, 42,311.2], shown at four significant figures as 37,080 [32,320, 42,310] (command 19). §8.0/8.1/8.2: CP-18d landed on main as `c61757d8` on 2026-11-18 with the named paths (command 20); PRES-7's four changed paths since `364ac020`, and its paths since `a5db292a`, are outside them. §8.5: `cp18.runner_artifact verify --artifact … --out …` exists on main, reads `space-artifact.json`, and its `deleted_arrays` rows carry `path`, as the fetch loop assumes (command 20). §10.3 item 5 closed by that landing. §10.4's account of review 1 (re-derived series and six polylines, 44 bindings, the usage-limit pause, the 15 `test_22` failures/errors needing CI's payload) matches the review's text. §7's "PRES-5's and PRES-6's prereleases recorded the same one" holds (command 21) |
| 3a | `pres-7-candidate-prerelease.json`: the prerelease at the candidate; its two unexpected results the known 3.12 interpreter pin and the untagged `evidence/pres-7` link | PASS | The record: `head` `364ac020…`, `partial` false, `unexpected` exactly ["CI, Python 3.12: uv run pytest -q", "links"]; every other step "as expected". The record names the steps, not the causes; the raw logs (command 18, read only) show the single 3.12 failure is `test_the_committed_manifest_verifies_here` ("CPython 3.12.14 here, 3.13.15 pinned") and the single failed link is the `blob/evidence/pres-7/…/publication-packet.md` URL (404 until the tag is pushed). Not rerun, as briefed |
| 3b | `pres-7-local-release.json`: the release check, its page hash equal to the final `docs/index.html`, `passed` true | PASS, with observation 1 | `passed` true; every view's `problems` empty; accessibility trees 4/4, keyboard/touch/contrast/zoom 2/2 and discovery 4/4 passed; Chrome 157.0.8103.79 and WebKit 26.6, 11 views; `checked_at_utc` 2026-11-18T16:26:22Z, 14 s before the candidate's commit. The record holds no page-hash field (observation 1); the binding to `7fd8dd2f…` is established by: the page bytes are unchanged from `364ac020` to the candidate (item 1) and the rebuilt page hashes `7fd8dd2f…` (command 10); against attempt 4's record (page `d2358f0f…`) only the page heights and the last placement/cold-reader screen offsets change, by +26 px at the desktop widths and +52 px at the phone widths, which is what the two text additions after `5575920c` (command 17) produce, and nothing else differs but the timestamp and folder names; and review 1's own release check at `7fd8dd2f…` passed with the same A2 numbers |
| 4 | `registry.EVIDENCE_TAGS["evidence/pres-7"]` is `2026-11-18`, and the packet's §1 and §8.2 say so | PASS | Command 15: the registry entry is `("", "2026-11-18")`; §1's identity row says "frozen `2026-11-18`"; §8.2's check expects `2026-11-18` on both lines; the candidate's commit date is 2026-11-18, so §8.2's check would hold if this candidate were the evidence tip |
| 5 | Rebuild leaves the tree unchanged; lint PASS; the focused tests pass | PASS | Commands 5–10: `build_pages.py --final` and `readme_research.py` exit 0, `git status --porcelain` empty afterwards (page 2,082,672 bytes, `7fd8dd2f…`); `make lint-publication` PASS with 0 findings on page, README and templates; `pytest tests/test_52_pres7_business_insights.py tests/cp29` 51 passed |
| Bar | §16.3's business clause still holds at the final candidate | PASS | Item 1 shows no published byte, no code and no test changed since `364ac020`, where review 1 found the bar met (its item 2). The rebuild reproduces those bytes, and the focused tests that bind Business insights to CP-29's records pass |

## Observations (not blocking)

1. **The release-check record does not carry the page's hash.** `pres-7-local-release.json`, like attempts 2–4 and
   PRES-6's record, names the served URL (`http://127.0.0.1:8817/index.html`) but not the bytes served. The packet's
   "pass at the final page (`7fd8dd2f…`)" is therefore a statement the record alone cannot prove. It holds here
   by inference (item 3b) and by review 1's own run at those bytes. A `page_sha256` field in the release-check
   record would make the binding direct in future rounds. That is a tooling change outside PRES-7's evidence-only delta.
2. **§5's table follows a convention it does not state.** README blocks are shown in their README markdown and
   page-only blocks as the page's text. That is why `economics.risk_aware` shows its lead phrase without the `**…**`
   that its markdown source and the other bold-led rows carry. The words are exact. A clause in the table's lead-in
   ("README form where the block is in the README, else the page's text") would close the gap.

## On FAIL only

Not applicable (PASS).
