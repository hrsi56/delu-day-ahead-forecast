# PRES-1 release review — one focused round before landing

> **Superseded before handover, 2026-09-28. Do not hand this document to the Lead.**
>
> - On the Owner's challenge, this review's R1–R8 were judged to be mostly patches on top of the
>   plan's own root causes.
> - It is replaced by `docs/track-b/publication-standard-v1.md`, ratified by the Owner on
>   2026-09-28, and by `docs/track-b/pres-1-conformance-brief-2026-09-28.md`, the brief for a new
>   Lead session.
> - This file is kept as the record of the release review. Its findings are carried into the
>   standard, and its §1 verifications still describe `af0abb0`.

**Orchestrator release review, 2026-09-28.**

- **Candidate:** `gauntlet/pres-1` at `af0abb090ad3eba2888c3791ebe3cdcf28409a7f`, 26 commits ahead of
  `main` at `e8025cc`.
- **Reviewed as:** a Lead Data Scientist and a VP Engineering would read it when interviewing for a
  team role.

**Verdict: not ready to land.** The work is accurate and well built, and I found no factual error.
Four things stand between the candidate and a landing:

- it hides its strongest result;
- the README and the next-generation path are not ready;
- the release is not closed: there is no independent PASS on this candidate, the MLflow links are
  unpublished, the device checks are open, and there is no return.

Close them in one round, as specified below. Nothing here reopens the approved design, the plan's
invariants or the science.

---

## 0. Owner instructions that govern this round (2026-09-28)

The Owner instructed: "Don't ask me to run tests or look myself. Everything is in your hands."

**Consequences for PRES-1:**

1. **Final audit F11 is re-scoped.** It asked the Owner to run the Safari, iPhone and VoiceOver
   checks himself; the Owner will not run them.
   - The agent runs the automated checks in §4.2 instead.
   - The return states plainly that nothing was verified on a real Safari, a real iPhone or with
     VoiceOver.
2. **The Owner's final visual approval (plan §12, F5) is delegated** to this Orchestrator review. I
   repeat it on the final candidate before landing.
3. **Landing belongs to the Orchestrator this time.** The Owner instructed the Orchestrator to
   merge, commit and push once the release review passes. The Lead does not land, push or create
   tags.

**Actions the Owner authorizes by handing this document to the Lead:**

- **F1, the public MLflow upload.** Upload the committed export to the `delu-generations`
  experiment on DagsHub. This is allowed only after the gate in §5, step 5, holds.
- **F7, the Hugging Face Space redeploy.** The Orchestrator performs it after landing and pushing.
  F8, the post-deploy checks, follows it.

No other public action is authorized:

- no push by the Lead, and no registry change;
- no write to `delu-cp2`;
- no CP-21 work.

---

## 1. What I verified myself

I worked in my own clean detached worktree at `af0abb0`, independently of the Lead and of the
independent checker.

| Check | Result |
|---|---|
| `uv sync --frozen`, then the full suite (credentials removed from the environment) | **751 passed, 7 skipped.** The skips are the known ones: no eccodes; one CP-16 anchor-bound test; five CP-16 ledger tests. |
| `scripts/verify_release.py` | PASS: every bound claim agrees on every surface, and the page makes no fetches |
| `scripts/mlflow_export.py --check`; `mlflow_publish.py --dry-run` | Export current. 23 runs, 6,928 metric points, 55 artifacts. The outbound scan is clean. |
| `scripts/rebuild_presentation.py`, then `git status` | Deterministic: no diff |
| `scripts/check_links.py` | Failed destinations: none. The gated DagsHub UI paths return 302, as the control expects. |
| DagsHub, read-only | No `delu-generations` experiment exists, so no public write happened early |
| Chrome at 1,440 and 390 px, closed disclosures | No horizontal overflow; the page is 1.52 MB |
| Accuracy spot checks against committed sources | Correct: the scoreboard, the v3−v2 and fold-3 intervals, and the crisis window. "Narrower in every period" holds at 50%, 80% and 95%. Pooled coverage is 0.9377 against 0.9389. |
| Reading | Every visible sentence of the page, and the README research block |

Independent check 2 already re-derived all 734 displayed numerals, and I did not repeat that.

---

## 2. Assessment for the audience

**Keep:**

- the restrained, consistent design;
- the aligned dot-plot comparison, and the paired-difference charts;
- limitations placed next to results;
- the clear split between the released v1 demo and v3 research;
- phone layouts with dedicated chart variants;
- the exact H−P endpoint;
- the rebuild command;
- the contribution statement;
- deterministic builds.

This reads as professional work.

**Where the target reader still stumbles:**

| # | Priority | Finding | Why it matters to the reader |
|---|---|---|---|
| R1 | P1 | **No result in the first screen.** The opening says what the product is but not how well it does. The "Latest research" line has no number. On a phone, the first number appears about three screens down (the comparison, at y ≈ 2,611 px), and v3's result about seven screens down (y ≈ 5,843 px). | Hiring readers decide in the first screen whether to keep reading |
| R2 | P1 | **The strongest honest result is buried.** v3 is the only policy of the seven, and the first in the programme, that clears both pre-specified improvement targets: 10% better than the best reference, daily LEAR, on each score. The comparison labels those lines "limit 0.59203" and "the plan's diagnostic limits … screening thresholds, not a certification". The finding that v3 is the first to meet all six criteria sits inside a closed disclosure. | Pre-specifying a bar and then clearing it is the single most convincing point for a data-science lead, and it is currently invisible |
| R3 | P2 | **No absolute anchor.** Everything is a ratio or a normalized difference, and a reader cannot tell what the error is in EUR/MWh. The committed pooled MAE is 41.74 (v1), 20.23 (v2) and 18.26 (v3) EUR/MWh over the 10,747 hours. | Plain units make the ratios believable. Keep them as context, not a headline (W11). |
| R4 | P2 | **The README opens with the old story.** Its "What it is (30-second read)" describes v1 only. The research block comes after it. | Engineering leads usually read the README before the site |
| R5 | P2 | **The next generation is not a template yet.** Chapters and charts are bespoke functions (`v3_chapter`, `v2_chapter`, `c2a_chart`, …). The rail, overview rows and lineage are separate literals. There is no runbook and no consistency test for adding v4. | The Owner's next generations will be published on this framework |
| R6 | P3 | **Wording and precision.** "Negative favours the first policy"; the "limit 0.59203" labels; charts mix 4 and 5 decimals (0.59203 and +0.00067 among 4-decimal values). | Small friction for a careful reader |
| R7 | P3 | **Demo fonts.** In the local Space build, WebKit requests three marimo fonts (PT Sans Regular and Bold, Lora) that return 404 (`release-checks/2026-09-28-demo-local.json`). | A Safari visitor gets fallback fonts and console errors |
| R8 | P3 | **No stack line.** "How the system works" never names the tools. | An engineering lead scans for the stack |

**Release blockers (process):**

| # | Blocker |
|---|---|
| B1 | No independent PASS binds the current candidate. Rounds 1 and 2 FAILED, and changes landed after both. |
| B2 | Four `data-unpublished` markers remain; F1–F4 are not done. |
| B3 | F11 is open. It is resolved by §0 and §4.2. |
| B4 | There is no `return.md` (brief §10). |

---

## 3. Required changes and acceptance

Keep every approved element: the D1 design, invariants 1–26, the contribution statement, the exact
H−P endpoint, the evidence labels. Every new number comes from the evidence layer and has a
claim-map entry (invariant 17).

**R1. One result in the opening.**

- Add one evidence-bound line to the opening, either in the research status card or directly under
  it. Suggested wording, with each number bound to its record:

  > v3 is the only model below both pre-specified improvement targets: point-error score 0.566 and
  > interval score 0.532, where a naive forecast scores 1.00 (v2: 0.644 and 0.616). Development
  > evidence after selection; performance on future data is untested.

- **Acceptance:**
  - fully visible without scrolling at 1,440 × 900;
  - within the first 1.5 screens at 390 × 844;
  - the development label sits next to the numbers;
  - the claim-map entry exists;
  - test_30 binds every number.

**R2. Say what the dashed lines are.**

- In the comparison, label the lines **"target: 10% better than the best reference"**.
  Explain in one sentence that the rule was fixed in the plan before the experiments, and keep
  "not a product qualification".
- Add the reading as the interpretation sentence: **only v3 is below both targets; v2 is not.**
- Bring the visible v3 chapter text into line: v3 is the first evaluated policy to meet all six
  original criteria, as a development diagnostic. Today this appears only inside "Criteria,
  controls and review".
- **Acceptance:**
  - no visible occurrence of "the plan's diagnostic limits" or a bare "limit 0.59203" label;
  - the statement is bound to the S records and the two limit records;
  - withheld claims W6 and W7 stay respected (no qualification wording, no significance wording).

**R3. An absolute anchor, as context.**

- In the comparison's "View values", add pooled MAE and WIS in EUR/MWh for all seven policies.
  Label them "pooled over all hours, dominated by the 2022 crisis; context, not the ranking
  metric".
- Optionally add one sentence in the v3 chapter: "average absolute error over all 10,747 hours:
  20.23 → 18.26 EUR/MWh (pooled)".
- **Acceptance:**
  - the values come from `reports/weather-ablation/metrics.csv` pooled rows;
  - W11 holds: pooled figures are never the headline or the ranking;
  - test_30 binds them.

**R4. The README leads with the current state.**

- Add a generator-owned "At a glance" block directly under the title, with four lines:
  1. what the project is;
  2. the released v1 demo, with its link;
  3. the R1 result line;
  4. links to the report, the evidence and, after F1, MLflow.
- The v1 "30-second read" stays below it, unchanged.
- **Acceptance:**
  - `test_32` covers the new markers: exactly once, idempotent, bytes outside unchanged;
  - `make verify` passes.

**R5. Make the next generation a template, not a rewrite.**

- **A single `GENERATIONS` registry** (ordered: version, name, adoption status, chapter anchor,
  MLflow `run_key`, overview row). It drives the rail, jump row, lineage main line, highlighted
  overview rows and README headings. Chapter bodies stay bespoke, because each story differs, but
  they are built only from the shared helpers (`chapter_header`, `story`, `evidence_row`,
  `disclosure`, the panel builders).
- **A new `tests/test_35_generation_registry.py`.** It fails when a registered generation lacks
  any of: a chapter anchor, a rail entry, an overview row, a README heading or an export
  `run_key`. It includes a negative control.
- **A new runbook, `docs/track-b/presentation-add-a-generation.md`.** It lists every touchpoint for
  adding `v4 · <adopted change>`, and the rejected-branch path, following the naming rule in plan
  §16: sources, records, claims and claim map, the chapter, charts, the overview row, lineage,
  README, the MLflow export parent and child, and tests.
- **Acceptance:**
  - a byte diff of `docs/index.html` shows only the changes from R1–R4, R6 and R8;
  - the full suite is green.

**R6. Wording and precision.**

- Replace "negative favours the first policy" with the explicit policy for each row.
- Use one display precision per chart. Exact values live in the values tables.

**R7. Demo fonts.**

- Either ship the three font files in the bundle, or remove their `@font-face` references in
  `build_wasm_space.py`. Change no calculation.
- Extend `test_23`: every asset the bundle's CSS and HTML reference must exist in the bundle.
- Re-run the local demo check in Chrome and WebKit, with zero failed requests.

**R8. A stack line.**

- Add one compact "Built with" line to "How the system works": Python; pandas and NumPy; LightGBM;
  scikit-learn (Lasso); marimo and Pyodide; MLflow on DagsHub; GitHub Actions; GitHub Pages; the
  Hugging Face Static Space.
- Structural text only; no claims.

---

## 4. Checks for this round

### 4.1 Standard checks, on the final pre-F1 candidate

- The full suite in the local Python 3.13 environment, and a clean Python 3.12 CI-equivalent run
  (every step in `.github/workflows/tests.yml`).
- `make verify`; `mlflow_export.py --check`; `mlflow_publish.py --dry-run`; a determinism check
  (rebuild, then an empty `git status`); `check_links.py`.
- Chart checks at 1,440, 768, 390, 360 and 320 px, with disclosures both closed and open: no
  overflow, no overlap, text at least 12 px.

### 4.2 Device and accessibility checks, replacing owner-run F11

Run in Playwright under `.local/tools/playwright`, and record the results in
`reports/presentation/release-checks/<date>.json`.

1. **WebKit, desktop 1,440 × 900, and an emulated iPhone** (Playwright's "iPhone 15" descriptor:
   touch, device pixel ratio 3), on both the report and the local Space build. Check:
   - no horizontal overflow;
   - readable charts;
   - the fan chart's behaviour at ×1.02 and at 95% (shows 0.9398);
   - tap targets of at least 44 px;
   - on desktop, keyboard order and a visible focus.
2. **Accessibility trees in Chromium and WebKit,** from Playwright's accessibility snapshot. Check
   that:
   - every `<summary>` exposes an expanded state that flips when toggled;
   - every chart exposes its title as its name and a description;
   - no interactive element is unnamed.
3. **The demo from a cold start in WebKit,** at both viewports:
   - the startup card appears first;
   - a forecast is visible;
   - the level and load controls change it;
   - the failure card links back to the report;
   - no failed requests (R7).
4. **The disclosure line,** in the record and in the return: "Real Safari, a real iPhone and
   VoiceOver were not used. Replaced by automated WebKit, emulation and accessibility-tree checks
   at the Owner's instruction of 2026-09-28."

### 4.3 Independent check, round 3

- **The checker:** a fresh agent that wrote nothing in PRES-1, working in a clean detached worktree
  at the exact pre-F1 candidate.
- **Scope:**
  - the brief's §9 in full;
  - this document's R1–R8, B1–B4 and §4.2;
  - a re-derivation of every newly displayed number.
- **It must PASS.** Rounds 1 and 2 stay preserved.

---

## 5. Order of work

1. **Copy this document** byte for byte into `docs/track-b/evidence/pres-1/`. Add the Owner's
   2026-09-28 handover to `owner-decisions.md`: the §0 consequences and the F1 and F7
   authorizations.
2. **Make R1–R8,** then rebuild every surface: the page, the README, the cards, the claims, the
   MLflow export and the Space bundle. Never hand-edit a generated file.
3. **Run §4.1 and §4.2.**
4. **Run the independent check, round 3,** until it passes.
5. **The F1 gate.** It holds only when all of these are true:
   - round 3 passed;
   - the export is current and the dry run is clean;
   - `MLFLOW_TRACKING_USERNAME` and `MLFLOW_TRACKING_PASSWORD` are set in the process (report only
     "set" or "unset").

   Then upload with `mlflow_publish.py --target public`.
6. **F2–F4:**
   - commit `mlflow_index.json`;
   - run `verify_mlflow_mirror.py --target public`, and the REST and browser route checks in
     Chromium and WebKit;
   - build with `build_pages.py --final` (no markers remain).

   Advertise only the routes that pass. Record any DagsHub feature that does not work, and do not
   promise it.
7. **Run a focused independent recheck** on the final candidate SHA (brief §9). If anything beyond
   the index and link targets changed, rerun the full check instead.
8. **Return** (`docs/track-b/evidence/pres-1/return.md`, brief §10), with:
   - `final_candidate_sha` and `evidence_tip_sha`;
   - the F3 records and the recheck verdict;
   - the Space bundle hash, and the exact redeploy command from `docs/deploy.md`;
   - an F8 command list for post-deploy checks.

   Then stop. Do not land, push, tag or redeploy.

**Ceilings for this round:**

- at most 16 active hours;
- $0;
- no fits, scoring passes or data retrieval;
- no changes to `pyproject.toml`, `uv.lock` or any locked file.

The allowlist is the brief's, plus the Owner's 2026-09-28 extension for `app/wasm_showcase.py`
(text and layout only). The new runbook, `test_35` and the README block are within it.

---

## 6. What I will check before landing

On the Lead's return, I verify:

- the final candidate and evidence-tip SHAs;
- round 3's PASS and the focused recheck, both bound to the final candidate;
- no `data-unpublished` marker remains, and the page and README carry real MLflow links that
  resolve anonymously to the intended runs and comparisons;
- R1–R8 are visible and correct at 1,440 and 390 px (my screenshots);
- the full suite, `make verify` and determinism, on a clean checkout;
- the delta from candidate to evidence tip touches evidence only.

**If all of these hold,** I land: a squash onto `main`, the tags `land/pres-1` and
`evidence/pres-1`, and a push. Then I run F7, the Space redeploy, and F8, the post-deploy checks
of the Pages bytes, demo startup and inference, and the MLflow routes.

**If any fails,** it comes back to the Lead with the failing item named.
