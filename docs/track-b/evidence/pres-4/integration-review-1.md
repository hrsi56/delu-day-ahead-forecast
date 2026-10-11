# Verdict — PRES-4 — Integration — FAIL

- Candidate SHA: `a852c0a898e6290e37c4674fe0b088c04a31d5bd` (local branch `gauntlet/pres-4`, eight commits above `main` = `origin/main` = `e398a30bb53ecd4c397aad0f34fd122d42e74553`)
- Plan / version / bar: `docs/PUBLISH_RULES.md`, revision 1.4 (SHA-256 `ccfe6199535dc104250ee1ed1d8ff57bf0b12fbfb4945a3521e2e29fad479a80` at the candidate), "## 13. Acceptance record for a future publication" (28 lines, 2,915 bytes, SHA-256 `c80c10e311ec6523e8989e9fa278e41067dbc8bb312155d967bd356c08426383`), applied as the issued brief's complete authoritative bar: PUBLISH_RULES 1.4 in full, the runbook's named sections, the packet template, the programme plan's stage 2 and the brief's outcome and extract.
- Verbatim bar excerpt:

> ## 13. Acceptance record for a future publication
>
> One review record can carry this matrix; duplicate certificates are unnecessary:
>
> | Area | Required record |
> |---|---|
> | Authority | Effective rules/hash; research anchor; brief; applicable clauses and justified N/A triggers |
> | Identity | Local branch/SHA/tree state; final candidate; landing/service revisions; served hashes |
> | Claims | Source rows/hashes, derivations, classes, comparator/population, count census, limitations |
> | Reader | Default path/screens, placements, definitions, unchanged six-question fresh-agent record |
> | Journey | Adopted transitions, rejected branches, plans; no implied unperformed experiment |
> | Content | Twelve active-product subjects, applicability, product-replacement migration, concise research histories, protected archive and approved contribution |
> | Charts | Rendering, semantics, mobile variants, values and discoverable routes under A5 |
> | Product | Actual demo identity, startup metadata, cold start, controls, failure/retry, applicable limitations |
> | Accessibility | Engine/width matrix, keyboard, AX controls, focus, targets, contrast, zoom/reflow, tool gaps |
> | Tracking | Mirror, histories/artifacts, anonymous routes and settled charts; no substituted local proof |
> | Release | Final build, guard/test results, exact-candidate independent check, authorized action record |
> | Public check | Per-surface identity/behaviour, first failures/retries, limitations and verdict |
> | Follow-up | Violations versus recommendations versus rule proposals; comparison with earlier findings |
> | Final product (A8, conditional) | Owner designation; one product/demo/daily-policy identity; frozen update contract; daily fit/issuance lineage; ordered method/results/business/comparison sections; actual rollout status |
> | Daily panel (A7/A8, conditional) | Today issued-versus-published prices; percentage and MAE derivations including zero/negative/missing outcomes; tomorrow intervals; coverage/width; separate training/issuance timestamps and stale/failure states |
> | Business (A8, conditional) | Reproducible cumulative net value and benchmark when evaluated; explicit unevaluated state otherwise; costs, denominators, risk and simulation/realization labels |
> | Final-product Space (A9, conditional) | Every §7.3 view against its records; recomputation rows on the served bundle; served identity equal to the intended daily artifact; the retrain's measured status; the §9 matrix on views and controls; the listed negative controls |
>
> Preserve screenshots and necessary machine-readable evidence with the review's declared scope.
> Release evidence uses the normal committed evidence locations; task scratch stays in `.local/`.
> For an expressly local-only review, identify retained local evidence honestly and do not claim
> its machine-specific paths are publicly available. Do not overwrite a prior report to claim closure.

  (The excerpt is the citation. Any line number is a courtesy and is non-binding.)

- Worktree clean before and after: yes. `git -C /Users/djourno/Downloads/PJM/.local/worktrees/pres-4/critic-1 status --porcelain` was empty at the start, after `make wasm`, after each `pytest` run, after the rebuild and the export checks, after the link check, and before this verdict was written; `HEAD` stayed `a852c0a898e6290e37c4674fe0b088c04a31d5bd` throughout. Ignored byproducts only (`.venv/`, `app/public/`, `dist/`).
- Reviewer: one fresh Integration Critic. It authored none of PRES-4's changes, worked only in the clean detached worktree above with the brief's prescribed inputs, made no Git write of any kind, and used the network for anonymous reads only (the link check, the served Pages page, the Space card and `origin/main`'s commit). No credential value was printed or typed: values were read only inside one process running `scripts/secret_guard.py`'s own functions, which printed a count and variable names. It formed the findings below before reading `docs/track-b/evidence/pres-4/editorial.md`, `fresh-reader.md` and the advisory log's PRES-4 section; the comparison with them follows the findings. No real Safari, real iPhone or screen reader was used, and this review did not rerun the Playwright browser checks: those rows rest on the committed records, whose page bytes were confirmed equal to the candidate's.
- Local-only evidence (machine-specific, not public): logs, records and helper scripts under `/Users/djourno/Downloads/PJM/.local/tmp/pres-4-critic-1/`.

## Commands actually run

All from `/Users/djourno/Downloads/PJM/.local/worktrees/pres-4/critic-1`, with `MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=true MLFLOW_DISABLE_AGENT_HINT=1` exported in every shell that imported MLflow.

| # | Command | Exit | Observed |
|---|---|---|---|
| 1 | `git show main:scripts/gauntlet.py \| python3 -I - critic-brief pres-4` | 0 | The brief: candidate `a852c0a8…`, this worktree, bar PUBLISH_RULES §13, verdict path |
| 2 | `git status --porcelain`; `git rev-parse HEAD main origin/main gauntlet/pres-4` | 0 | empty; `a852c0a8…`; `e398a30b…` twice; `a852c0a8…` |
| 3 | `git show main:scripts/bar.py \| python3 -I - bar docs/PUBLISH_RULES.md "## 13. Acceptance record for a future publication" --at a852c0a8…` and `… identity docs/PUBLISH_RULES.md --at a852c0a8…` | 0, 0 | Revision 1.4, file `ccfe6199…a80`; section 28 lines, 2,915 bytes, `c80c10e311ec6523e8989e9fa278e41067dbc8bb312155d967bd356c08426383`: equal to the brief's identity line |
| 4 | `shasum -a 256` and `cmp` of `docs/track-b/evidence/pres-4/issued-brief.md` against `.local/artifacts/pres-4/issued-brief.md`; `git show c5c931b --stat` | 0 | both `54169c7c998958e850d451bf5c766dddbd559721f1920370020035e3bae57bdd`, byte-identical; the branch's first commit adds only that file |
| 5 | SHA-256 at `a852c0a` and at `e398a30` of every input in the brief's "Execution inputs" table, the standard and the presentation plan | 0 | 20 of 20 equal their pinned hashes and are unchanged from `e398a30`; the advisory log is `983708c7…` at the candidate, its first 16,021 bytes are `e6b23215…98ca` (append-only); `presentation-and-tracking-plan-2026-09-24.md` is `b04a0bb1…19c` |
| 6 | `git diff --name-only e398a30 a852c0a`, filtered for the Governance Lockdown set, `progress.md`, the runbook, the template, artifact manifests and earlier evidence | 0 | none touched (the one `manifest.json` changed is the MLflow export's own) |
| 7 | `uv sync --frozen` | 0 | environment installed |
| 8 | `make wasm` | 0 | payload 15,363,807 bytes; gate max deviation 0.0, null mismatches 0; the three controls each break the gate; bundle 805 files, 44,164,910 bytes, `bundle_sha256` `9028a11869a378ea5c3401a00ad46368e1c9e2f2f9f8732330d32b71af081585`; `git status --porcelain` empty |
| 9 | Independent bundle hash: `find dist/space-wasm -type f` sorted, `shasum -a 256` per file, the lines hashed; `diff -rq dist/space-wasm .local/artifacts/pres-3/space-wasm-9028a118` | 0 | `9028a118…1585`; the two trees identical file for file |
| 10 | SHA-256 of `space/README.md`, `space-wasm/README.md` at the worktree, `e398a30` and `a852c0a` | 0 | `745bbb93…d553` and `c92a2666…9a67` everywhere |
| 11 | `uv run pytest -q -p no:cacheprovider` | 0 | 1,652 passed, 8 skipped in 240 s; `git status --porcelain` empty |
| 12 | `uv run pytest -q -rs -p no:cacheprovider` | 0 | 1,652 passed, 8 skipped in 226 s. Skips: `eccodes` not installed (1); CP-16 identity bound to the v21-r3 anchor (1); CP-16 production verification (5); `tests/cp24/test_draft_export.py:38`, "scripts/mlflow_export.py changed after CP-24" (1), the by-design skip |
| 13 | `uv run python scripts/rebuild_presentation.py`, then `git status --porcelain` | 0 | README blocks, CP-3 section, MLflow export, static page and the agreement checks ok; status empty: every generated surface, both Space cards included, equals its committed bytes |
| 14 | `make verify` | 0 | PASS: every bound claim agrees on every surface; zero fetching references in `docs/index.html` (1,993,644 bytes); cross-surface parity of headline, names and statuses |
| 15 | `make lint-publication` | 0 | PASS: page, README and templates 0 findings |
| 16 | `uv run python scripts/mlflow_export.py --check` | 0 | "the committed export is current" |
| 17 | `uv run python scripts/mlflow_export.py --diff-against e398a30bb53ecd4c397aad0f34fd122d42e74553` | 0 | runs 28 → 44, the 16 of `cp22`, `cp23`, `cp24` added; 206 params, 9,178 metric points, 51 datasets, 73 artifacts checked (73 digests unchanged); identity changes on 0 runs; substantive changes none; `only_identity=True` |
| 18 | The same with `--out .local/tmp/pres-4-critic-1/export-diff.json` | 0 | `experiment_tag_changes: ["mlflow.note.content"]`; JSON equal to the committed `pres-4-export-diff.json` |
| 19 | `uv run python scripts/mlflow_export.py --draft cp22 --check`; `… --draft cp23 --check` | 0, 0 | both "the committed draft export is current" |
| 20 | `uv run python -c "…E.later_final_vs_draft(k)['equal_apart_from_pending'] for k in ('cp22','cp23','cp24')"` | 0 | `cp22 True`, `cp23 True`, `cp24 True` |
| 21 | SHA-256 of every file in `reports/presentation/mlflow-export/`, against `e398a30` | 0 | `cp10`–`cp21` unchanged; `cp22.json` `4be85b84…59359`, `cp23.json` `413ebf56…7eac0`, `cp24.json` `d55cf3de…2911`, `manifest.json` `af680390…ae1d` |
| 22 | Draft-versus-final tag and description comparison of every run in the three exports (Python, stdlib) | 0 | only pending fields and the Owner's rename differ, except `cp23/D`'s description, whose subtitle is the shortened one (recorded departure, observation O1) |
| 23 | `wc -c docs/index.html`; `shasum -a 256 docs/index.html README.md`; `cat reports/cp3/pages_build.json`; page and README hash at `719ddeb`, `db65a46`, `b0ed155`, `a852c0a` | 0 | 1,993,644 bytes, `e22525a9…a366`; README `142c27a2…7d25`; `final: false`, four routes omitted; page and README identical from `db65a46` to the candidate; code unchanged after `db65a46` |
| 24 | `uv run python .local/tmp/pres-4-critic-1/scripts/simulate_final.py`: the `--final` build in memory, every expected route indexed with URLs from `verify_mlflow_mirror.route_url` and 32-hex run IDs | 0 | all 10 routes published, 0 missing; 1,995,526 bytes (4,474 under 2,000,000); nothing written |
| 25 | Element-level byte comparison of `docs/index.html` against `e398a30`'s, by `id` | 0 | identical: `product`, `v4`, `v3`, `v2`, `v1`, `v1-archive`, `transition-v3-v4`, `transition-v2-v3`, `transition-v1-v2`, `branches-v1`, both v1–v2 branch cards, `contribution`, `attribution`; changed: `top`, `journey`, `planned`, `evidence` (the system view adds v5) |
| 26 | `python3 -I .local/tmp/pres-4-critic-1/scripts/recompute.py` and ad hoc stdlib reads of the committed rows | 0 | every reading-path value checked re-derives (see Claims below) |
| 27 | Parity of shared identities across `reports/block-challenger`, `v4-revision`, `distribution-challenger` and `ddnn2/attempt-1` `metrics.csv` (equal-fold, pooled and per-fold rows) | 0 | `HGL`, `HG`, `B0`–`B3`, `A1` identical in all four; `H0` identical in CP-21 and CP-22 |
| 28 | `RC.render_template('P55', '{r:derived.change.v5.S_MAE\|ciexact}')` and the same with `\|ci`, and for `derived.change_decision.v5.*` | 0 | `ciexact` renders the point value `−2%` with no `data-field`; `ci` renders `[−3%, −2%]` from `ci_low` / `ci_high`: violation V1 reproduced |
| 29 | `check_links.main([], record=.local/tmp/pres-4-critic-1/links-attempt-1.json)` (anonymous; the committed record untouched) | 0 | 46 links; failed destinations none; the gated DagsHub paths answer 302 to login, as controls; `git status --porcelain` empty |
| 30 | `curl` (anonymous) of the Pages URL, the Space's raw `README.md` and GitHub's `commits/main` API | 0 | Pages HTTP 200, 1,907,718 bytes, `8a1fedd8…8c39`; Space card `c92a2666…9a67`; `origin/main` `e398a30bb53ecd4c397aad0f34fd122d42e74553` (2026-10-11T11:17Z) |
| 31 | `scripts/secret_guard.py`'s own `credentials()` and `_outgoing('origin', …gauntlet/pres-4 a852c0a8…)`, in one process that printed only counts and names | 0 | 5 distinct credential values loaded; commits `e398a30..a852c0a` scanned; 0 findings |
| 32 | `shasum -a 256 -c` of the 62 screen hashes listed in `fresh-reader.md`, in `.local/tmp/pres-4/fresh-reader/` | 0 | 62 of 62 OK |
| 33 | `git show main:scripts/bar.py \| python3 -I - check <this verdict> --source docs/PUBLISH_RULES.md@a852c0a898e6290e37c4674fe0b088c04a31d5bd` | 0 | "ok: lines 7–34 (2914 bytes) appear in docs/PUBLISH_RULES.md@a852c0a898e6" |

## Evidence actually inspected

- **Governing text:** `AGENTS.md`; the issued brief in full; `docs/PUBLISH_RULES.md` 1.4 in full; Publication Standard v1 §§3–6; `docs/track-b/publication-runbook.md` in full; `docs/track-b/publication-packet-template.md` in full; `docs/track-b/programme-plan-2026-10-11.md` §§1–12; `docs/track-b/gauntlet-templates.md` §2 as the brief carries it.
- **The committed rows:** `reports/ddnn2/attempt-1/` `metrics.csv`, `uncertainty.csv`, `ratio-intervals.csv`, `criteria.csv`, `decisions.json`, `diagnostics.csv` (peak rows), `protocol.json` (`rule_verbatim`), `controls.json`, `leakage-controls.json`; `reports/v4-revision/` and `reports/distribution-challenger/` `metrics.csv`, `uncertainty.csv`, `criteria.csv`; `reports/block-challenger/metrics.csv` and `criteria.csv`; `reports/cp15/criteria.csv`; `data/source_manifest.json`, `data/partitions.json`.
- **Drafts and records:** the three draft registries; the three draft exports and the three final exports; `docs/track-b/research-content/cp24-claims.md`; `publication-claims.md` P21 and P53–P59; the CP-22, CP-23 and CP-24 landing records (status sources); the three checkpoint verdicts' candidate lines; the evidence tags' commits and dates.
- **Code and tests:** the diffs of `src/delu_forecast/registry.py`, `research_claims.py` (definitions, headline terms, `_render_derived`, `_render_record`), `scripts/build_pages.py` (`PLANNED_WORK`, `planned_work`, `ratio_change_table`, `v5_slots`, `route_coverage`, `main`, the tokens and `marker_problems`), `scripts/mlflow_export.py` (`EXPERIMENT_NOTE_CHECKPOINTS`, `final_vs_draft`, `renamed_draft`, `later_final_vs_draft`), `scripts/verify_mlflow_mirror.py` (`route_url`, `write_index`); `tests/test_45` and `tests/test_49` (diffs and the planned-list, registry and chapter tests); `tests/cp22`, `tests/cp23` amendments and `tests/cp24/test_draft_export.py`'s skip; `tests/cp21/test_saved_evidence.py` (the precedent).
- **Surfaces:** `docs/index.html` (text extraction and raw HTML of the opening, the comparison and its value table, the journey, the transition, both new branch cards, the v5 chapter including `#v5-ratio-values`, the planned list, the system view), against `e398a30`'s page; `README.md` diff against `e398a30`; both Space cards.
- **Check records:** `reports/cp3/pages_build.json`; `reports/presentation/release-checks/pres-4-local-release.json` (views, placements, chart text, discovery, keyboard/contrast summary), `pres-4-local-demo.json`, `pres-4-local-demo-a11y.json`, `pres-4-local-states.json`, `pres-4-space-check.json`, `pres-4-space-unchanged.json`, `pres-4-pre-final-prerelease.json`, `pres-4-links.json`, `pres-4-export-diff.json`; fresh-reader screens D01 and D10 viewed.
- **The packet:** `docs/track-b/evidence/pres-4/publication-packet.md` §§1–10 in full.
- **After forming the findings:** `editorial.md`, `fresh-reader.md`, the advisory log's PRES-4 section.

## Existing-rule violations (PUBLISH_RULES §10.1, category 1)

### V1 · The v5 ratio value table shows the point estimate in both interval columns (Medium)

- **Clause.** PUBLISH_RULES §3.4: "Research numbers originate in committed source rows … claim maps bind the interpretation; generators render them" and "Full precision in tables"; Publication Standard v1 §4: "Exact values live in the value tables"; PUBLISH_RULES §3.2: the change as a share of the comparator's score "with its 95% interval"; the publication's claim P55, which binds this table: "exact values in the chapter's value table: −2.49% [−2.96%, −1.79%] and [−3.04%, −1.68%]; −2.36% [−2.78%, −1.71%] and [−2.86%, −1.62%]".
- **Observation.** In `docs/index.html`, disclosure `#v5-ratio-values` ("View the change as a share of v4's score"), the columns headed "95% interval" and "97.5% interval, the decision level" each hold `−2%` for both scores. Every one of those four cells is `<data value="-2.48990…"` (or `-2.35614…`) with no `data-field`: the rounded point estimate, not an interval. The true values are, for the point-error score, 95% [−2.9585%, −1.7939%] and 97.5% [−3.0368%, −1.6823%]; for the interval score, 95% [−2.7787%, −1.7145%] and 97.5% [−2.8593%, −1.6208%] (`ratio-intervals.csv` L2–L3; `derived.change.v5.*`, `derived.change_decision.v5.*`).
- **Cause, reproduced.** `scripts/build_pages.py::ratio_change_table` calls `interval(…, exact=True)`, which emits `{r:<derived record>|ciexact}`; `src/delu_forecast/research_claims.py::_render_derived` handles `ci`, `lo`, `hi`, `abs` and `exact` but not `ciexact`, so it falls through to `one("value", None)`. Command 28 shows `|ciexact` rendering `−2%` and `|ci` rendering `[−3%, −2%]` from the same record. `tests/test_49` only asserts that the disclosure exists.
- **Impact.** The one table the page offers for the exact ratios misstates both intervals at both levels, as a single number, on a public surface. It is the table that P55, the packet's slot record, editorial V10's recorded repair, advisory A-PRES4-1 ("the value tables carry the exact ratios") and the fresh reader's disposition 3 ("the exact ratios are in the value table") rely on, so each of those closures is unsupported by the candidate.
- **Priority.** Medium: wrong values in a value table; the reading path's whole-percent figures are correct.
- **Repair.** Render `ciexact` for derived records in `_render_derived` (both endpoints at full precision, each a `<data>` with `data-field="ci_low"` / `"ci_high"`), regenerate with `scripts/rebuild_presentation.py`, and bind it with a test and a negative control.
- **Acceptance check.** In the regenerated `#v5-ratio-values`, each interval cell holds two `<data>` elements whose `value` attributes equal the derived records' `ci_low` and `ci_high` above; a doctored table showing the point value fails the new test.

### V2 · Two headline terms no longer match the text their claims bind (Low)

- **Clause.** Publication Standard v1 §3.1, incorporated by PUBLISH_RULES §1.1: "Definition, at first use: 'error relative to a simple naive forecast, averaged over the test periods; lower is better'"; PUBLISH_RULES §3.4 (claim maps bind the interpretation); claims P21 ("error scores (the standard §3.1 definition)") and P53 (the paired difference "defined beneath it at that level ('with its 97.5% confidence interval, the rule's level')").
- **Observation.** The shared block `terms.error_scores` now renders "error relative to a naive forecast, averaged by test period; lower is better" on the page and in the README's glance, where `e398a30` rendered the standard's definition. The headline's paired-difference term renders "v5's score minus v4's, with the rule's 97.5% interval; below zero favours v5", not P53's quoted "confidence interval" wording. The advisory log records that both terms "were shortened" to keep A2's phone placement; neither P21 nor P53 was updated, and no Owner decision or rule proposal covers the change to the standard's definition.
- **Impact.** Low. "averaged by test period" is looser than "averaged over the test periods" (the score is a mean over periods of per-period ratios), and the first screen's 97.5% interval loses the word that distinguishes it from the demo's "80% prediction interval" beside it (PUBLISH_RULES §3.2's distinct-label rule is still met, narrowly, by "the rule's"). The claim layer misdescribes the surface.
- **Repair.** Restore the standard's definition, or record an Owner decision changing it and rebind P21; make P53 quote the rendered term, or render "confidence interval". Re-measure A2 in both engines afterwards: the phone finding has 17.5 px to spare.
- **Acceptance check.** The rendered `terms.error_scores` equals the definition P21 binds; P53's quoted wording equals the rendered term; A2 still passes in Chrome and WebKit.

No other existing-rule violation was found.

## Observations and recommendations (not violations)

- **O1 — the draft-equality check cannot see a description change.** `final_vs_draft` treats any change to `mlflow.note.content` as a filled pending field whenever the draft's value contains `pending-at-landing`. The one non-pending change in the three exports, `cp23/D`'s shortened subtitle (Standard v1 §5's eight-word limit, recorded in packet §2 and A-PRES4-4), therefore passes silently. Recommend comparing the description apart from its pending sentence and the declared renames and departures.
- **O2 — a typed value in a review record.** `fresh-reader.md` disposition 3 cites "−2.48% [−3.11%, −1.70%]", which matches no record (exact: −2.49% [−2.96%, −1.79%] at 95%, [−3.04%, −1.68%] at 97.5%). Append a correction; do not rewrite the record.
- **O3 — the land commit message.** Packet §8.2 runs `git commit -F .local/artifacts/pres-4/land-commit-message.txt`; the file does not exist yet. The return must write it, as the brief requires.
- **O4 — the page budget.** 1,993,644 bytes at the candidate. A simulated `--final` build with all ten routes indexed measured 1,995,526 bytes (4,474 to spare); V1's repair adds a few hundred bytes. Re-measure at the next candidate and at the final SHA. A sixth chapter will not fit (A-PRES4-5).
- **O5 — wording.** Registry-generated status sentences such as "In October 2026, the DDNN-2 alone was not adopted" (the `cp24/D2` description) read awkwardly.

## Checklist verdict

### Identities and constraints

| # | Item | Verdict | Evidence |
|---|---|---|---|
| I1 | Candidate, clean detached worktree, bar excerpt present at the candidate | PASS | Commands 2–3 |
| I2 | Issued brief byte-identical to the canonical copy, `54169c7c…`; first branch commit copies it | PASS | Command 4 |
| I3 | Every pinned input hash, the standard and the presentation plan; the advisory log append-only | PASS | Command 5 |
| I4 | Base `main` = `origin/main` = `e398a30`; Pages serves `8a1fedd8…`, 1,907,718 bytes; the Space card `c92a2666…`; the published export 28 runs at `e398a30` | PASS | Commands 2, 17, 30 |
| I5 | No locked file, runbook, template, `progress.md`, artifact manifest or earlier evidence changed | PASS | Command 6 |
| I6 | The candidate's surfaces as the Lead measured them: page `e22525a9…`, 1,993,644 bytes; README `142c27a2…`; the four export hashes; the cards | PASS | Commands 10, 21, 23 |
| I7 | No credential value in any outgoing commit | PASS | Command 31 |

### PUBLISH_RULES 1.4, clause by clause, and the incorporated baseline

| # | Clause | Verdict | Evidence |
|---|---|---|---|
| P1 | §1.1–§1.3 authority, the four identities, categories | PASS | The brief pins 1.4, the standard and the plan; publication rule, research generation v5, product status (v1 released) and artifact identities kept apart on the page and in the packet |
| P2 | §2 reader contract; A1 | PASS | The headline names each metric beside its value and leads with the verdict; the terms sit beneath it |
| P3 | §2 placements; A2 | PASS (committed record) | `pres-4-local-release.json`, page bytes equal to the candidate's: headline ends 800.6 / 801.3 px at 1440×900 and 628.6 / 628.7 px at 390×844; the finding 1,727.6 / 1,728.3 px (limit 1,744) and 2,402.5 px (limit 2,420); the `--final` additions all fall below the finding (`build_pages.py` lines 1711, 1935, 2631) |
| P4 | §2 definitions at first use; v1 §3.1 | FAIL | V2 |
| P5 | §3.1 evidence classes; W1–W48 | PASS | "Development · post-selection" on the headline, the transition, the chapter and both cards; W47 respected (the headline quotes 97.5% only); lint 0 findings |
| P6 | §3.2 verdict, rule date, distance, N, ratio intervals from own draws, absolute MAE, one population | PASS | Recomputed: v5 − v4 ΔS_MAE −0.0133 [95% −0.0161, −0.0096; 97.5% −0.0166, −0.0091], ΔS_WIS −0.0119 [−0.0143, −0.0087; −0.0147, −0.0084]; ratios −2.49% / −2.36% → −2% [−3%, −2%] at both levels; N = 1; rule set 2026-10-05 (`rule_verbatim`); v5 MAE 4.8–14.4 and 45.5 EUR/MWh, v4 47.0, naive 8.6–30.5 and 86.9; one population (command 27) |
| P7 | §3.3 counting | PASS | 25 identities by decision date (5+2+1+4+10+3); v3 first; 16 later met both (v4, L-P, L-R, L-N; CP-22's seven; CP-23's v5 and v3+D, D not; CP-24's three); 12 rows = 8 tested + 4 references |
| P8 | §3.4 provenance and formatting | FAIL | V1 (and V2's claim drift); the reading path otherwise derived, whole percent, ≤ 4 significant figures, one decimal for EUR/MWh |
| P9 | §4 registry, A3 transition, branch cards | PASS | v5 entry and arms as drafted with the two named changes; CP-22 and CP-23 as `branch` with their arms; transition "From v4 to v5: adding a distributional neural network" with predecessor, change, comparator = predecessor, result at 95% and 97.5%, limits, dated decision and route; both cards carry question, comparator, deciding result with interval, "Not adopted", month, reason, evidence class and evidence |
| P10 | §4 A10 | N/A, confirmed | v5 is a new generation; no entry gains a revision |
| P11 | §5 architecture, A4, §5.1 product documentation | PASS | Order unchanged; `#product` byte-identical to `e398a30` |
| P12 | §5.2 chapter grammar; one page; 2.0 MB | PASS | `slot_problems` empty (`tests/test_49`); 1,993,644 bytes; simulated final 1,995,526; no compaction, v2 and v3 byte-identical (the Owner's D1) |
| P13 | §6 charts, discovery, A5; encoding | PASS (committed record) | v5's main chart with direct labels and the rose filled pentagon (`TOKENS["v5"]` `#BE123C`, `marker_problems` refuses a shared shape); study points as open circles with labels; 40 routes per engine at both placement sizes, none failed, `#v5-*` routes landing below the header with no closed ancestor; chart text ≥ 12.21 px at every width, closed and open |
| P14 | §7.1 product contract | PASS | Opening names v1 as the demo's model and v5 as research; release rule and startup line unchanged |
| P15 | §7.2 / A7, §7.3 / A9, A8 | N/A, confirmed | No final-product designation, rollout or live panel |
| P16 | §8 surfaces and links | PASS | README generated from the registry; parity PASS; both Space cards unchanged; 46 links resolve anonymously; audit labels' dates match the tags |
| P17 | §9 browser and accessibility matrix | PASS (committed records) | Chrome 154.0.8037.98 and WebKit 26.6 at 1440×900, 768×1024, 390×844, 360×780, 320×640 and the emulated iPhone 393×659; no console error, failed request, HTTP error or post-document resource; AX trees, keyboard, touch, contrast, zoom and reflow passed; the demo's controls and states (`pres-4-local-demo*.json`, `pres-4-local-states.json`); no real Safari, iPhone or screen reader |
| P18 | §10.1 independence; §10.2 fresh reader | PASS | Editorial reviewer and fresh reader authored nothing; the six questions verbatim; 62 closed-state screens, hashes verified; answers 1–5 agree with the records (see O2) |
| P19 | §10.3 / A6 public checks | Not yet applicable | After the Owner's steps; packet §8.5 supplies them |
| P20 | §11 packet and order | PASS so far | Build → editorial → fresh reader → this check; the upload, index, `--final` build and focused recheck follow |
| P21 | §12 baseline coverage | PASS, except V2 | Applied through the rows above |
| P22 | §14 pending triggers | PASS | v5's encoding and the no-compaction decision taken by the Owner on 2026-10-11 |
| P23 | A11 work availability | PASS | No calendar gate used |

### §13's acceptance record (the bar)

| # | Area | Verdict | Evidence |
|---|---|---|---|
| A1 | Authority | PASS | Packet §1 and §9.1; hashes verified (I3); A7–A10 not applicable with reasons |
| A2 | Identity | PASS at the candidate | `gauntlet/pres-4` at `a852c0a8…`, clean, off `e398a30`; the final candidate, landing and served identities are later |
| A3 | Claims | FAIL | V1, V2; every reading-path value otherwise re-derived (P6, P7) and the census verified |
| A4 | Reader | PASS | Default path and placements (P3); definitions beneath the headline (V2 aside); the fresh-reader record |
| A5 | Journey | PASS | One new adopted transition; two branch cards between v4 and v5; the planned list per the programme plan; no unperformed experiment implied |
| A6 | Content | PASS | Twelve product subjects unchanged for v1 (byte-identical); v5's concise chapter; v1 archive byte-identical; contribution unchanged |
| A7 | Charts | PASS | P13 |
| A8 | Product | PASS | Demo v1, bundle `9028a118…` rebuilt identically; startup metadata, controls, failure and retry records |
| A9 | Accessibility | PASS (committed records) | P17 |
| A10 | Tracking | PASS at the candidate | Export current; 28 → 44 runs, only identity, one experiment-tag change; the mirror, routes and index follow the authorized upload |
| A11 | Release | PASS at the candidate | Tests, verify, lint, determinism, links and guard (by design non-final) pass; this exact-candidate check is FAIL |
| A12 | Public check | Not yet applicable | Packet §8.5 |
| A13 | Follow-up | PASS with exceptions | Violations, recommendations and amendments kept apart in the reviews; the advisory log's closures of editorial V10 and A-PRES4-1 are not supported (V1) |
| A14–A17 | Final product, daily panel, business, final-product Space | N/A, confirmed | No A8 trigger |

### The runbook

| # | Section | Verdict | Evidence |
|---|---|---|---|
| R1 | §2 steps 1–5 (`_ENTRIES`, `CHECKPOINTS`, `EVIDENCE_TAGS`, `RULES`, `COMPARISON_ORDER`) | PASS | Registry diff; tags' commits and dates (author time zone); CP-22's three rules (2026-10-01), `cp23-adoption` (2026-10-04), `cp24-adoption` (2026-10-05); v5 first |
| R2 | §2 step 6 `CRISIS_ORDER` | PASS (not needed) | v5 states its peak in text |
| R3 | §2 steps 7–10 (`SOURCES`, `CRITERIA_FILES`, `CHANGES`, `PERIOD_SUBJECTS`) | PASS | Rows blob-pinned; verdict, ratios at both levels, periods and coverage re-derive (P6) |
| R4 | §2 steps 11–12a (claim maps, `v5.*`, `transition.v4-v5.*`) | PASS, except V2 | Claim maps registered; blocks bound |
| R5 | §2 steps 13–15 (`v5_slots`, `chapter_sequence`, `CHARTS_BY_RUN`) | FAIL | V1 sits in `v5_slots`' value table; registration and charts otherwise correct |
| R6 | §2 step 16 tokens | PASS | P13 |
| R7 | §2 steps 17–18 (export specification, tests) | PASS | Commands 16–22; `tests/test_49`, `tests/test_43` |
| R8 | §2 "What follows without an edit" | PASS | Opening, rail, jump row, lineage, comparison rows, chapter order, README glance and list, Space cards' model line (unchanged), run set and routes |
| R9 | §2 "Limits to watch" | PASS | Placements (P3), chart text (P13), budget (P12, O4) |
| R10 | §3 touchpoints 1–5 for CP-22 | PASS | Branch entry and seven arms; checkpoint; tag; `branch.pooled-lightgbm-member-for-v4.*`; export specification |
| R11 | §3 touchpoints 1–5 for CP-23 | PASS | Branch entry and two arms; checkpoint; tag; `branch.ddnn-member-on-v4.*`; export specification |
| R12 | §1 order; §1a receipt; §8 routes; §9 checks | PASS | Order kept so far; packet §8 intended identities; expected routes omitted until verified and the `--final` build refuses without them; prerelease record PASS at `b0ed155` (differs from the candidate only in the packet, a one-line link-record timestamp and the prerelease record) and this rerun |

### The packet template, section by section

| # | Section | Verdict | Evidence |
|---|---|---|---|
| T1 | §1 Identity | PASS | Brief, anchors, tags, model-code SHAs equal to each verdict's candidate line |
| T2 | §2 Registry entries | PASS | As drafted with the named departures (name, dates, sources, CP-22's resolved reason, CP-23's subtitle) |
| T3 | §3 Claim maps | PASS, except V2 | P53–P59 added |
| T4 | §4 Derived quantities | PASS | Re-derived (P6) |
| T5 | §5, §5a Slot texts and transition | FAIL | V1 (the slot record names the value table that misreports) |
| T6 | §5b, §5d | N/A, confirmed | Product unchanged; no final-product trigger |
| T7 | §5c Chart routes | PASS | P13 |
| T8 | §6 MLflow export | PASS | Commands 16–22; O1 |
| T9 | §7 Checks run | PASS | Records exist and agree with this rerun |
| T10 | §8 Receipt and the Owner's packet | PASS at the candidate | Every surface named; the Space recorded verified unchanged; non-interactive commands with expected outputs; O3 |

### The Owner's programme plan, stage 2

| # | Item | Verdict | Evidence |
|---|---|---|---|
| S1 | D1 no compaction | PASS | v2 and v3 byte-identical; within budget |
| S2 | D2 CP-22 and CP-23 published, and in the comparison where possible | PASS | Two cards; R, M and CP-23's candidate as study points on the shared population |
| S3 | D3 automation items 6 and 7 | PASS | `prerelease.py` used; `publication_receipt.py` in the Owner's packet |
| S4 | D4 advisories | PASS | A-PRES3-1 taken up; A-PRES3-7 and A-PRES3-5 deferred with reasons |
| S5 | The Space stays on v1 | PASS | Commands 8–10, 30 |
| S6 | Risk: the page budget | PASS | P12, O4 |
| S7 | Risk: `scripts/mlflow_export.py` bound by CP-22's and CP-23's tests | PASS | `AMENDED_BY_PUBLICATION` in both, as for CP-21, with tag-byte checks; no manifest edited; CP-24's draft-export test skips by design |
| S8 | "Say plainly" | PASS | 448 of 2,654 days (16.9%), none in October–December, one winter; DDNN-2 alone descriptive; post-selection development evidence and v1 the product; the re-evaluation in the planned list |

### The brief's observable outcome and extract, items 1–10

| # | Item | Verdict | Evidence |
|---|---|---|---|
| B1 | Registry | PASS | "v5 · DDNN-2 added"; adopted 2026-10-11 from the CP-24 landing record; v4 predecessor and comparator; arms never eligible |
| B2 | Evidence | PASS | P6; coverage 448 / 2,654 from `represented_dates`, the source manifest's first hour and `eda_cutoff` |
| B3 | Claims and slots | PASS, except V2 | Claim maps, `v5.*`, `transition.v4-v5.*`, the coverage slot, `branch.<id>.*`; withheld claims guarded |
| B4 | Chapter and charts | FAIL | V1 |
| B5 | Encoding | PASS | P13 |
| B6 | Planned work | PASS | 4.6 gone; re-evaluation and new input data added, unnumbered; 4.4V source-neutral; 4.8 and 4.7T unchanged; comparator v5; test and five negative controls over the page, README blocks and both cards |
| B7 | Export and tests | PASS | Commands 16–22; A-PRES3-1; frozen-file treatment |
| B8 | Space | PASS | Bundle, cards and gate (commands 8–10) |
| B9 | Limits | PASS | Placements, budget, chart text |
| B10 | Advisories | PASS | One-line dispositions for A-PRES3-1, -7, -5; A-PRES4-1's text is inaccurate (V1) |
| B11 | Upload, index and `--final` build | Not yet applicable | After this verdict, rechecked at the final SHA |

## Comparison with the earlier reviews (read after the findings above)

- Editorial V10 asked for the exact ratios in a value table. The advisory log records it repaired ("the exact ratios are in a value table (V10)"), and A-PRES4-1 says "the value tables carry the exact ratios". The table exists but its interval columns are wrong (V1), so the closure is not supported. The editorial review ran on `87cdcea`, before the table existed, and could not see it; the fresh reader's disposition 3 relies on it.
- The advisory log's note that the error-score and paired-difference terms "were shortened" to keep A2's phone placement is the change V2 records; it was disclosed, but not treated as a departure from the standard's definition or carried into P21 and P53.
- The other editorial findings V1–V9 are repaired at the candidate as far as this review checked them (the DDNN-2 and not-adopted terms, the legend, DDNN-2 alone's intervals, the winter wording, the cards' evidence class, the acronym case, the caveat wording, the leakage route).

## On FAIL only

- **Single largest meaningful gap:** the v5 chapter's exact-value table "View the change as a share of v4's score" (`#v5-ratio-values`) shows the rounded point estimate, `−2%`, in both its "95% interval" and its "97.5% interval, the decision level" columns, for both scores, because `research_claims._render_derived` ignores the `ciexact` option that `build_pages.ratio_change_table` passes; the public table misstates both intervals, and P55, editorial V10's recorded repair, A-PRES4-1 and the fresh reader's disposition 3 rely on it.
- **Exact next acceptance test:** on a new candidate regenerated from source, (1) each interval cell of `#v5-ratio-values` holds two `<data>` elements, `data-field="ci_low"` and `"ci_high"`, whose values equal the derived records' endpoints at full precision (point-error score: 95% −2.9584699118793495 and −1.793927483038195, 97.5% −3.0367905356064449 and −1.6822708947669157; interval score: 95% −2.7786808736341522 and −1.714496476404881, 97.5% −2.8593332937828102 and −1.6208499381219484), bound by a test whose negative control fails on today's rendering; (2) V2 repaired: the rendered error-score term is the definition P21 binds (the standard's, or an Owner-approved one with P21 rebound), and P53 quotes the rendered paired-difference term; (3) `rebuild_presentation.py` with an empty `git status`, `make lint-publication`, `make verify`, `uv run pytest -q`, the page budget (≤ 2,000,000 bytes at the candidate and for the `--final` build) and the A2 placements in Chrome and WebKit pass again; (4) a fresh exact-candidate Integration review of that candidate passes before the MLflow upload.
