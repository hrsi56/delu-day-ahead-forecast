# Verdict — PRES-3 — Integration — PASS

- **final_candidate_sha:** `4ad7d09f5b9405f09b633326979890e9fa9180ca`. This verdict binds here.
  - It is one commit on `gauntlet/pres-3` after the independently checked candidate: "PRES-3: cp21
    uploaded, verified and indexed; the final build".
  - Its PASS rests on the focused recheck in the section "Focused recheck at the final SHA" below.
- **Independently checked candidate:** `747d2bbc9336758ce4a26d12a5d9ddb35d46e72a` (local branch
  `gauntlet/pres-3`; off `main` `17f354e42c0d6f3199227fe9d29df9f4dc8211e0`; seven commits
  `f694510` … `747d2bb`).
  - The full independent review below binds that SHA. It passed.
  - The delta `747d2bb..4ad7d09` holds only the MLflow index, the final-build outputs and the
    upload, mirror and route records. Every check those files affect passes again at
    `4ad7d09`.
- **Candidate SHA (full review):** `747d2bbc9336758ce4a26d12a5d9ddb35d46e72a`.
- **Plan / version / bar:** `docs/track-b/evidence/pres-3/issued-brief.md`, the Orchestrator's
  PRES-3 brief issued 2026-09-30. Its SHA-256 at this SHA is
  `57a8c7fbc1b9b0d3c268e4af95a02a4a75276dda8224a24a6b1119ac03b773d7`, equal to the assignment.
  The bar is the section "Complete authoritative checkpoint bar". The rules are PUBLISH_RULES 1.2,
  `a43ac02021b7de468e02db30b61ec73f86cdafa69df845cf084ab196528bb15b`. Both hashes were recomputed
  before any test ran.
- **Verbatim bar excerpt.** It is present at lines 164–180 of that file at this SHA. The line
  numbers are a courtesy.
  > - **PUBLISH_RULES 1.2 in full.** Every applicable clause, including the incorporated baseline,
  >   A1–A6 and §13's acceptance record. Record A7, A8 and A9 as not applicable, with the reason.
  > - **The runbook:**
  >   - §2, all touchpoints 1–18, 12a included, with "What follows without an edit" and "Limits to
  >     watch";
  >   - §1, §1a, §8 and §9.
  > - **The packet template, every section.** Complete CP-21's packet into PRES-3's, with §8 filled
  >   for every surface.
  > - **The publication plan, as scope:**
  >   - §4's table and its "in both outcomes" statements;
  >   - §6's surface table and its `style.css` paragraph;
  >   - §7's sequence.
  > - **v21-r8 §18.5's planned-item correction,** as the Observable outcome states it.
  > - **Critic and return:** `docs/track-b/gauntlet-templates.md` §§2–3. This is not a research
  >   checklist, and it authorizes no fit.
  >
  > Map every applicable item to evidence. The extract below does not narrow this bar.
- **Worktree clean before and after: yes.**
  - Worktree: `/Users/djourno/Downloads/PJM/.local/worktrees/critic-pres-3`, detached at the
    candidate.
  - `git status --porcelain` was empty at 02:17 IDT, after every command, at 06:12 IDT when the
    review resumed, and at 06:28 IDT at the end.
  - One command rewrites a tracked record (`check_links.py`). It is noted below.
- **Reviewer:** a fresh Integration Critic. I authored none of the changes.
  - **Inputs:** only the assignment, the candidate tree and the local artifacts it names.
  - **Not read:** `progress.md`, `orchestrator-role.md`, the syllabus and Track A/C material.
  - **Timing:** the review paused from about 02:31 to 06:12 IDT on a usage limit. Thursday
    2026-10-01, outside the Friday–Saturday window.
  - **Order of reading:** I formed my findings before I read `editorial.md`, `fresh-reader.md` or
    the advisory dispositions. I compared them only afterwards; see the last section.

## Commands actually run

All commands ran in the clean worktree. `MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=true
MLFLOW_DISABLE_AGENT_HINT=1` was exported before anything imported MLflow. One later
`build_pages.py --final` run omitted the agent-hint variable and printed MLflow's hint line;
telemetry stayed disabled. Scratch output is in `/Users/djourno/Downloads/PJM/.local/tmp/pres-3-critic/`.

| # | Command | Exit | Observed |
|---|---|---|---|
| 1 | `git worktree add --detach …/critic-pres-3 747d2bb…`; `git status --porcelain` | 0 | HEAD `747d2bb…`; porcelain empty |
| 2 | `shasum -a 256` of the brief, PUBLISH_RULES, the runbook, the packet template, the CP-21 plan, landing record, packet, return and verdict, PRES-2's verdict, `cp21-claims.md`, the draft export, `capstone_v21.md`, standard v1 and plan revision 3 | 0 | Every hash equals the brief's. The exception is the advisory log (`e6b23215…`, against the brief's `d1cb5309…`), which PRES-3 legitimately appends to |
| 3 | `uv sync --locked --dev --offline` | 0 | 129 packages resolved, 117 checked; Python 3.13.15 |
| 4 | `make wasm` | 0 | Payload: 15,363,807 bytes across 14 files. The gate's maximum deviation is 0.0; three controls broke it (0.01, 0.427, 50.2). Assembled 805 files, 44,164,910 bytes. `bundle_sha256` `9028a11869a378ea5c3401a00ad46368e1c9e2f2f9f8732330d32b71af081585` |
| 5 | Independent shell recompute of the bundle hash (sorted `sha256  path` lines) | 0 | `9028a118…1585` |
| 6 | Bundle comparison with PRES-2's reviewed copy (`.local/artifacts/pres-2/space-wasm-8007f0d2/`), file by file, plus a decompression of the nine boosters | 0 | 796 of 805 files are identical. The nine `public/boosters/*.txt.gz.b64` differ only in gzip header byte 9 (OS field): `0x13` in PRES-2's copy, `0xff` here. The decompressed booster text is identical for all nine |
| 7 | `uv run pytest -q -p no:cacheprovider` (after `make wasm`) | 0 | **1280 passed, 7 skipped** in 177.45 s |
| 8 | the same with `-rs` | 0 | 1280 passed, 7 skipped. Skip reasons: `eccodes` absent (1); CP-16 identity bound to v21-r3 (1); CP-16 production verification needs its ledger (5) |
| 9 | `uv run python scripts/mlflow_export.py --check` | 0 | "the committed export is current" |
| 10 | `uv run python scripts/mlflow_export.py --diff-against 17f354e --out <scratch>` | 0 | Runs 23 → 28; the additions are exactly `cp21`, `cp21/HGL`, `cp21/L-N`, `cp21/L-P` and `cp21/L-R`. Checked: 155 params, 6,928 metric points, 39 datasets and 55 artifacts, **55/55 artifact digests unchanged**. **0 identity changes**, no substantive change, `experiment_tag_changes` [], `only_identity` True |
| 11 | Independent JSON diff of the final `cp21.json` against the CP-21 draft | 0 | params, metrics, `metric_units`, inputs, parents and run names are identical on all five runs. Differences: the pending tags (`delu.status`, `delu.evidence_ref`, `delu.model_code_sha`, `delu.original_completed_utc`, `mlflow.note.content`); the README lines naming the tag commit and the landing record; the draft-only keys `status`, `pending_fields` and `draft_registry`; and **eight chart artifacts added to `cp21/HGL`** (overview, v4-c2a, ladder, arms, c2b, c3, c4, c6). Filled identities: `260dcf9…`, CP-21's `final_candidate_sha`; `evidence/cp-21@1d13f99`; `2026-09-30T00:57:44Z`, the tag commit time 03:57:44 +0300 |
| 12 | Recompute of the ratio intervals from `replicates.parquet` and from `replicate-scores.parquet` (HGL/HG − 1, 2.5th/97.5th percentiles) | 0 | MAE [−0.063665, −0.039665] and WIS [−0.059542, −0.037981]; equal to `uncertainty.csv` L72–L73 and to the page's −5% [−6%, −4%] on both |
| 13 | Cell-by-cell comparison of CP-21's `metrics.csv` with CP-20's on the seven shared policies | 0 | Same index; **0 differing cells**; CP-21 adds only the `stress_period` column |
| 14 | `criteria.csv` summary | 0 | HG, HGL and L-N meet every criterion; L-P misses 4; L-R misses 4 and 5; all five meet 1–2 |
| 15 | `make verify` | 0 | PASS: every bound claim agrees on every surface; `docs/index.html` (1,906,528 bytes) has 0 external fetch references; cross-surface parity agrees |
| 16 | `make lint-publication` | 0 | page, README and templates: 0 findings each |
| 17 | `make publication-guard` | 2 | BLOCKED: "reports/cp3/pages_build.json is a non-final build record (final: false)", by design |
| 18 | `uv run python scripts/rebuild_presentation.py`; `git status --porcelain` | 0 | Rebuilt in 11.1 s; **porcelain empty** |
| 19 | `uv run python scripts/check_links.py` | 0 | 37 links, "failed destinations: none". The five `blob/evidence/cp-21/…` links answer 200. It rewrote `reports/cp3/link_check.json` (timestamp and one dropped stale URL). That output is copied to scratch (`link_check-critic.json`) and the tracked file restored with `git checkout --`. The fresh link set equals the committed `pres-3-links.json` |
| 20 | `uv run pytest -q tests/test_44_deploy_space.py tests/test_45_pres3_v4_publication.py tests/test_43_publish_rules_migration.py` | 0 | **122 passed** |
| 21 | `uv run python scripts/deploy_space.py --bundle dist/space-wasm --expect 9028a118… --delete style.css`, check mode, anonymous, 2026-09-30T23:29:02Z | 0 | Space `static`, public, RUNNING, revision `0c550e863711e19abbb35219cf64d45dfb39c888`. `planned_adds` []; `planned_changes`: the nine boosters; `planned_deletes` `["style.css"]`; `declared_matches` true; `credential_guard` passed; "check only: nothing was written" |
| 22 | `curl -s https://hrsi56.github.io/delu-day-ahead-forecast/ \| shasum -a 256` at 23:29:07Z | 0 | `f36314e2…dab1d`, equal to `17f354e:docs/index.html` (PRES-2) |
| 23 | `python3 -m http.server 8741 --bind 127.0.0.1 --directory docs`, then `check_reader_paths.py release http://127.0.0.1:8741/index.html --shots <scratch>/release --out <scratch>/release.json` | 0 | The first attempt was killed by the pause (Playwright EPIPE); it is kept as `release-attempt-1-interrupted*`. The second run is **passed=True**, 2026-10-01T03:18:17Z; details below |
| 24 | `chart_shots.py` and `zoom_shot.py` (my scratch scripts) | 0 | Element screenshots of the overview chart, the eight v4 charts, the preview and v3's coverage chart. Chrome and WebKit at 1440/390/320, every disclosure open; plus 4× crops |
| 25 | `python3 -m http.server 8742 … --directory dist/space-wasm`; `check_reader_paths.py demo`, `demo-a11y` and `states` with `--url http://127.0.0.1:8742/` | 0/0/0 | Demo: ready in 10.2 s (Chrome, both sizes), 12.2 s and 11.7 s (WebKit); 0 console errors, 0 failed requests. `demo-a11y` passed=True: no unnamed control, no target under 44 px, slider, radio and menu operated by keyboard. States: failure in 1.1/1.2 s when the runtime reports one; loading at 1 min, then failure after the deadline; asset failure with the report link; retry reaches ready |
| 26 | `uv run python scripts/build_pages.py --final` | 1 | "final build refused: the verified MLflow index lacks ['compare:overview', 'compare:v4']". Nothing written; porcelain empty. This is the intended gate before the upload |
| 27 | Bundle record check: `pres-3-space-bundle.json` `per_file` against my rebuild; the hash of `.local/artifacts/pres-3/space-wasm-9028a118/` | 0 | 805 paths, 0 SHA-256 mismatches; the retained copy hashes to `9028a118…` |
| 28 | Fresh-reader screens: `shasum -a 256` of `.local/tmp/pres-3/fresh-reader/*.png` against the 48 hashes in `fresh-reader.md` | 0 | 48 files; the aggregate hash `5e373567…` is equal on both sides |
| 29 | Pattern scan of `git diff 17f354e..HEAD` for token shapes (`hf_…`, `ghp_…`, AKIA, key=value secrets) | 0 | 0 matches. No credential variable was read. The value-based guard is the Owner's pre-push step |
| 30 | `pkill` of both local servers; final `git status --porcelain` | 0 | Both servers stopped; porcelain empty |

**My release record, both engines at every width** (`release.json`):

- **Engines.** Chrome 154.0.8037.58 and WebKit 26.6.
- **Headline block.** It ends at:
  - 800.6 px (Chrome) and 801.3 px (WebKit) at 1440 × 900;
  - 628.6 px and 628.7 px at 390 × 844.
- **Finding sentence.** It ends at:
  - 1,702.6 px and 1,703.3 px at 1440 × 900, against the A2 limit of 1,744 (h = 56);
  - 2,400.5 px at 390 × 844, against the limit of 2,420.
- **Smallest chart text.** 12.21 px at 320, 14.58 px at 390 and 12.38 px at 1440.
- **Accessibility.**
  - Text overlaps and clips, console errors, failed requests, HTTP errors and post-document
    resources: 0 everywhere.
  - Accessibility trees pass in both engines.
  - Keyboard order is logical and focus is visible; summaries toggle on Enter; an anchor into a
    closed disclosure opens it.
  - Touch targets under 44 px: 0. Contrast failures: 0. Overflow at 200% zoom and at 320 px reflow:
    0.
- **A5 discovery.** 33 routes per engine at both placement sizes, all passed.
- **Agreement with the Lead.** These numbers equal the Lead's attempt-4 record
  (`pres-3-local-release.json`).
- **Not used.** No real Safari, no real iPhone and no screen reader.

## Evidence actually inspected

- **Governing text.**
  - The whole brief.
  - `AGENTS.md`.
  - `gauntlet-templates.md` §§2–4.
  - `docs/PUBLISH_RULES.md`, all 1,098 lines.
  - Publication Standard v1 §§1–4 and §15.
  - Plan revision 3 §8.2 and §10.6.
  - The whole runbook, the whole packet template and the whole CP-21 publication plan.
  - `capstone_v21.md` §17.6, §17.9 and §18 (all of it).
  - The CP-21 landing record's Owner decisions.
- **CP-21 evidence.**
  - The whole CP-21 packet.
  - The whole `cp21-claims.md`.
  - `draft-registry.json`.
  - `uncertainty.csv` L72–L85.
  - `metrics.csv`: equal-fold and per-fold rows, and the date range, which ends at 2026-04-07.
  - `criteria.csv`.
  - `diagnostics.csv` peak rows L855, L998 and L1141.
  - `adoption.json`.
  - `replicates.parquet` and `replicate-scores.parquet`.
- **PRES-3 code diff from `17f354e`.**
  - `registry.py` in full.
  - `mlflow_export.py` in full.
  - `mlflow_publish.py` in full.
  - `deploy_space.py`, the whole file.
  - `tests/test_44_deploy_space.py`, the whole file.
  - `derived.py`: the additions for CP-21, `RATIO_CHANGES`, `PERIOD_SUBJECTS` and
    `ADOPTION_RULES`.
  - `publication_lint.py`.
  - The `research_claims.py` withheld patterns (W14 unchanged; W22–W26 added).
  - `build_pages.py`: `PLANNED_WORK`, `planned_items`, `planned_work`, `CHARTS_BY_RUN`, `_indexed`,
    `route_coverage` and `main`.
  - `tests/cp21/*` (the A-PRES3-3 exemption and its companion check).
  - `tests/test_43` (the v4 transition).
  - `tests/test_45`: the planned-list, history-byte-identity, withheld and export tests.
- **Rendered surfaces.**
  - `docs/index.html`: the full visible-text diff against `17f354e` (in `page-textdiff.txt`) and
    against `d9c4438`.
  - Every `v4.*`, `transition.v3-v4.*`, `comparison.*` and `terms.*` block.
  - The SVG title, description and labels of all eight v4 charts and of the overview chart.
  - The v4 and v3 evidence rows.
  - The route anchors.
  - The six historical sections and the v1 archive, by SHA-256 against `17f354e`: all
    byte-identical.
  - The README diff.
  - Both Space cards.
  - `docs/deploy.md`.
- **Chart images.** I looked at them myself:
  - the overview, v4-c2a, ladder, arms, c2b, c3, c4 and c6 at 1440 (Chrome);
  - the ladder, arms and c3 at 320, and the overview and c6 at 390 (WebKit or Chrome);
  - 4× crops of c6's nominal labels and c4's right edge;
  - v3's published coverage chart, for comparison;
  - my release screens D01–D02 at 1440.
- **Lead records.** I judged them against my own runs:
  - the publication packet, in full;
  - the advisory-log PRES-3 section;
  - `pres-3-local-release*.json`, attempts 1–4;
  - `pres-3-space-check.json` and `pres-3-space-bundle.json`;
  - `pres-3-determinism.txt`, `pres-3-pytest-3.13.txt` and `pres-3-ci312.txt`;
  - the local demo records;
  - the `publication-claims.md` and `cp20-claims.md` diffs (P07, P08, P10, P16, P18–P26, P33,
    P51 and P52).
- **Reviews.** Read after my findings were formed: `editorial.md` and `fresh-reader.md`, in full.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| **1** | **PUBLISH_RULES 1.2 in full** | | |
| 1.1 | §1.1–1.3: authority, the four identities, applicability; hashes pinned before testing | PASS | Run 2: the brief pins 1.2 `a43ac020…`, v1 `01d721c2…`, plan revision 3 `28119374…` and v21-r8 `81d61271…`, all recomputed equal. The packet's §1 keeps the rule revision, generation (v4), product status (v1 released) and artifact identities apart |
| 1.2 | §2, the reader contract, and **A1** (metric beside each headline number) | PASS | The headline reads "both error scores improved on v3's (v4 − v3: −0.0301 [−0.0368, −0.0228] on the point-error score, −0.0266 [−0.0327, −0.0204] on the interval score; 1 policy tested against the rule)". Each value carries its metric. The terms beneath define error scores, the adoption rule, the paired difference, policies and the class. The release rule sits beside the demo action. The byline links to the contribution statement |
| 1.3 | §2, **A2** placements (measured header) | PASS | Run 23: 1,702.6/1,703.3 ≤ 1,744 and 2,400.5 ≤ 2,420. The headline block is within the first screen in both engines and at both sizes. Phone margin: 19.5 px |
| 1.4 | §3.1 evidence classes; W1–W21 in force | PASS | The badge "Development · post-selection" is on the headline and the chapter. `v4.caveat.class`. No significance, validation or confirmatory wording in the v4 additions. `test_45::test_no_surface_carries_a_withheld_claim` passes |
| 1.5 | §3.2 scores, comparator, uncertainty (the ratio interval from CP-21's own draws; labelled confidence intervals; null ≠ equivalence) | PASS | Run 12 recomputes −5% [−6%, −4%] on both scores from the draws. Every difference or ratio interval in the v4 chapter and README is a "confidence interval"; "95% interval" is used only for forecast intervals. The block split is "no demonstrated joint preference". The bootstrap note states both interval methods (v4's ratio; v2/v3's fixed denominator) |
| 1.6 | §3.3 counting identities | PASS | N = 1 for `cp21-adoption`; the study arms are never eligible (§17.6). The target census is 12 (5 + 2 + 1 + 4, one identity once), listed by decision date, and stated apart from the chart's 8 rows |
| 1.7 | §3.4 provenance and formatting; negative controls | PASS | `make verify` passes; lint 0 findings; every number in the v4 blocks carries a `data-record`. Re-derivation checks: runs 12–14 and `test_45`. Negative controls: a perturbed row, an unmet condition, an unstated rule date, a stale planned list and the withheld phrases |
| 1.8 | §4 registry identity, and **A3** transition | PASS | `registry.py` holds v4 "v4 · three-block LightGBM added": adopted in research 2026-09-30, source `cp-21-landing-2026-09-30.md`, predecessor and comparator v3. The three study arms are not adopted, 2026-09-30. The transition card "From v3 to v4: adding a three-block LightGBM" has predecessor and date, change, comparator = predecessor, result with its confidence interval and class, limits (C111, C120), dated decision and route `#v4-chart-title`. `test_43` covers the v1→v2→v3→v4 chain |
| 1.9 | §5, **A4** order and product documentation unchanged | PASS | The section order is PRES-2's. The product section is byte-identical to `17f354e` (SHA-256 `7b8078e5…`). v1 remains released; the release rule is unchanged |
| 1.10 | §5.1, the twelve subjects | N/A, with reason | The released product is unchanged (packet §5b). The documentation is byte-identical |
| 1.11 | §5.1a and **A8** | N/A, with reason | No final-product designation (brief; §1.3) |
| 1.12 | §5.2 chapter grammar; the 2.0 MB budget | PASS | The v4 chapter carries every slot: question, change, chart, headline, reading, not established (3), decision, evidence and the five details. The page is 1,906,528 bytes, under 2.0 MB; compaction waits for v5 |
| 1.13 | §6 charts, and **A5** discovery | PASS | Every v4 chart has a title, a description, metric and unit, a "no difference" or nominal reference, direct labels and shape (diamond, D6) besides colour. Comparable panels share scales, except c3's per-fold scales, which follow published v3's convention and are stated under the chart. 33 routes pass by mouse, keyboard and deep link in both engines at both sizes. Recommendations R-5 and R-6 are below |
| 1.14 | §7.1 product contract (demo, startup, states) | PASS | Run 25: cold start, controls, keyboard, 44 px targets, loading/failure/retry. The startup line is beside the action. The demo still computes v1: the equivalence gate holds at 0.0 deviation and the decoded boosters are identical (run 6) |
| 1.15 | §7.2, **A7** | N/A, with reason | No live panel authorized |
| 1.16 | §7.3, **A9** | N/A, with reason | Conditional on A8's trigger, which has not occurred (§17's 1.2 entry: PRES-3's obligations equal 1.1's) |
| 1.17 | §8 public surfaces agree; zero runtime network; GFS attribution | PASS | `make verify` parity covers the page, README, both cards and the export; 0 external fetches; 0 post-document resources in both engines. The README glance equals the page headline. The cards are unchanged and name v1. The GFS line is present on every surface; recommendation R-3 is below |
| 1.18 | §9 browser and accessibility matrix | PASS (local) | Run 23 covers every width and the iPhone emulation, accessibility trees, keyboard, touch, contrast, zoom/reflow and requests. The public matrix is the Owner's step (A6) |
| 1.19 | §10.1 independence; three outputs separate | PASS | This record; the three outputs are below |
| 1.20 | §10.2 fresh reader | PASS | `fresh-reader.md` records the six unchanged questions, the closed-state screens (48, hashes verified in run 28) and the answers preserved verbatim. Answers 1–5 match the registry and the derived records, which I checked independently (runs 11–14). The one violation it found ("policy" undefined in the headline) is repaired at the candidate |
| 1.21 | §10.3, **A6** post-deployment evidence | N/A at the candidate, with reason | It follows the Owner's landing, push and Space upload (brief §"Stop and return" step 4). The packet's §8.5 gives the per-surface commands and records; recommendation R-4 is below |
| 1.22 | §10.4 verdict semantics | PASS | This verdict |
| 1.23 | §11 packet and sequence; no placeholder or non-final build reaches `main` | PASS | The packet is complete. The order so far is build → editorial (`7dd234b`) → fresh reader (`d9c4438`) → independent check (this, at `747d2bb`). The final build refuses at the candidate (run 26) and the guard blocks the non-final record (run 17) |
| 1.24 | §12, the incorporated baseline and plan invariants (1, 3, 8, 10, 13, 14, 16–19, 21, 26) | PASS | Zero fetch (run 15). Regenerated, not hand-edited: determinism (run 18). Nothing after 2026-04-07: CP-21 rows end on 2026-04-07. `pyproject.toml` and `uv.lock` unchanged. No retired-tooling text on any surface. Only verified routes are linked (`_indexed`). Planned work is unscored and unnumbered |
| 1.25 | §13 acceptance record | PASS, with an erratum | Packet §9.2 covers every area. Its §9.1 "§2" row cites the superseded attempt-3 placements; the candidate's values are those in run 23 and packet §7 (R-1) |
| 1.26 | §14 pending triggers (the v4 encoding; v5 compaction) | PASS | D6 is applied: `--v4:#B45309`, a filled diamond, the direct label "v4". Contrast ≥ 4.5 is tested. No compaction is needed |
| 1.27 | A7, A8 and A9 recorded as not applicable, with the reason | PASS | Packet §5d and §9.1: no final-product designation, rollout, live panel or final-product Space |
| **2** | **The runbook** | | |
| 2.1 | §2 step 1, `_ENTRIES` | PASS | The four entries equal `draft-registry.json` field for field (the registry diff, `test_45`). Statuses are dated 2026-09-30 from the landing record |
| 2.2 | §2 step 2, `CHECKPOINTS` | PASS | `CP-21`: `cp21`, owner v4, `evidence/cp-21`, `1d13f99`, 2026-09-30, the report, verdict and landing record, children HGL, L-P, L-R and L-N. The tag resolves to `1d13f99b…`, committed 2026-09-30 03:57:44 +0300 |
| 2.3 | §2 step 3, `EVIDENCE_TAGS` | PASS | `("1d13f99", "2026-09-30")`. The audit labels read "frozen 2026-09-30" |
| 2.4 | §2 step 4, `RULES` | PASS | `cp21-adoption`, set 2026-09-29, with v21-r6 §17.6 and `protocol.json` as provenance. `_adoption_date` checks both quotes |
| 2.5 | §2 step 5, `COMPARISON_ORDER` | PASS | v4 comes first. `COMPARISON_EXPERIMENT` moved to CP-21 on the same population: 0 differing cells against CP-20 (run 13). v3's pinned comparison keeps CP-20's seven rows |
| 2.6 | §2 step 6, `CRISIS_ORDER` | PASS | v4's chapter shows the August 2022 peak, so the order is `(v2, v3, v4)`. v3's chapter is pinned to `V3_CRISIS_ORDER`, and a negative control refuses a silent v3 redraw |
| 2.7 | §2 step 7, `SOURCES` | PASS | The CP-21 rows are pinned by blob. `records()` holds 14,948 records, matching the packet |
| 2.8 | §2 step 8, `CRITERIA_FILES` | PASS | Includes `CP-21`. `ADOPTION_RULES` derives the verdict as met only when all four committed conditions are met |
| 2.9 | §2 step 9, the change with CP-21's interval | PASS | `RATIO_CHANGES`, recomputed in run 12 |
| 2.10 | §2 step 10, per-period MAE with fold 3 as stress | PASS | v4: 4.9–15.0 EUR/MWh in ordinary periods, 47.0 in the stress period. v3 for comparison: 5.3–15.6 and 48.0. Read from the `metrics.csv` per-fold rows |
| 2.11 | §2 step 11, the claim map registered | PASS | `cp21-claims.md`, unchanged (`8df2e9a5…`), is in `CLAIM_MAPS` |
| 2.12 | §2 step 12, `v4.*` blocks; headline through `headline_template` | PASS | Question, change, chart headline, reading, three not-established items, decision, method (blend, inputs, ladder with C106's bundle, split exactly as C111, arms), folds, absolute values, peak (C120), coverage, rule, criteria, parity, controls and cost. Each was checked against its claim (C101–C127) and its committed row |
| 2.13 | §2 step 12a, `transition.v3-v4.*` | PASS | Title, change, comparator, result and limits. No `predecessor` block, because the comparator is the predecessor |
| 2.14 | §2 step 13, `v4_slots` with `MainChart` and `detail_head` | PASS | `slot_problems` passes (build). Six detail headings feed "Explore these results" |
| 2.15 | §2 step 14, `chapter_sequence` | PASS | The v4 chapter renders first; the jump row reads v4 v3 v2 v1 |
| 2.16 | §2 step 15, `CHARTS_BY_RUN` | PASS | `cp21/HGL` gets eight charts (plan rev. 3 §10.6). `cp20/HG`'s overview is drawn pinned, and all 55 published artifact digests are unchanged (run 10) |
| 2.17 | §2 step 16, `TOKENS` (Owner D6) | PASS | `#B45309`, a filled diamond, the label "v4". Seen in the charts |
| 2.18 | §2 step 17, export specification | PASS | `CHECKPOINTS["cp21"]`. The final export equals the draft apart from the pending fields plus the plan-§10.6 charts (run 11). It changes no published record (run 10) |
| 2.19 | §2 step 18, tests with negative controls | PASS | `test_45` (612 lines), the `test_43` extension and the `tests/cp21` updates; 122 pass (run 20) |
| 2.20 | §2 "What follows without an edit" | PASS | Opening status pair, rail, jump row, lineage (v4 node), comparison rows, chapter order, README glance and generation list, both cards' model line (v1), run set (28) and routes (`compare:v4`). The runbook's lists are resolved by `test_42` (in the full run) |
| 2.21 | §2 "Limits to watch" | PASS | Placements as in 1.3; 12.21 px minimum chart text; 1.91 MB |
| 2.22 | §1, the order of a publication | PASS so far | Steps 1–4 are done in order. Steps 5–9 follow this PASS (the MLflow upload, verification, browser routes and index; `--final`; the focused recheck; the Owner's steps; A6) |
| 2.23 | §1a completion receipt, every surface | PASS | Packet §8.1 has rows for GitHub/README, Pages, MLflow, the card and the direct demo. Intended identities are filled; observed identities await the publisher, as the template requires |
| 2.24 | §8 MLflow routes | PASS (gate) | `expected_routes()` gives `experiment`, `compare:overview` (8 runs) and `compare:v4` (cp21 ×4 + cp20/HG). Routes are linked only when verified for exactly those runs (`_indexed`). The final build refuses until then (run 26) |
| 2.25 | §9, checks before the independent check | PASS | Every item reproduced here (runs 7, 15–19, 23, 25), except the Python 3.12 CI run. That one I inspected in the Lead's `pres-3-ci312.txt` (Python 3.12.14 at `4b64fd2`, every step exit 0, 1,280 passed) but did not repeat, because it needs a second worktree |
| **3** | **The packet template, every section** | | |
| 3.1 | §1 Identity | PASS | Packet §1 |
| 3.2 | §2 Registry entries | PASS | Packet §2; all seven code additions entered. None changes a published record: 0 identity changes, 55/55 digests unchanged, historical sections byte-identical |
| 3.3 | §3 Claim map | PASS | Packet §3. I checked C100–C127 and W22–W27 against the committed rows. P51 and P52 bind the headline and transition. The PRES-3 notes on P07, P08, P10, P16, P18–P26 and P33 append; nothing is rewritten |
| 3.4 | §4 Derived headline quantities | PASS | Packet §4 equals my recomputation: verdict met; rule date 2026-09-29; distances; N = 1; ratio change and interval; per-period MAE |
| 3.5 | §5 Slot texts | PASS | Packet §5 lists the editorial differences from the draft. None changes a claim |
| 3.6 | §5a Transition | PASS | Packet §5a equals the rendered card |
| 3.7 | §5b Product documentation | N/A, with reason | The released model is unchanged |
| 3.8 | §5c Chart routes | PASS | Seven routes listed. Every heading anchor exists, and discovery passes (run 23) |
| 3.9 | §5d Final product | N/A, with reason | Trigger unmet |
| 3.10 | §6 MLflow export | PASS | Packet §6 equals runs 9–11. The upload command needs `--owner-instruction` (R-2) |
| 3.11 | §7 Checks run | PASS | Packet §7; I reproduced each figure except the one noted in R-1 |
| 3.12 | §8 Receipt and the Owner's packet, every surface, non-interactive commands with expected outputs | PASS | §8.0–8.7 give the payload identities (page, README, bundle 805 files with a per-file list, card hashes, export) and the deletion set `style.css`. The commands use `git --no-pager` and `git commit -F` and state expected outputs. Steps: LAND (twin check, squash, `write-tree` equality, both tags), push (value-based scan, then the guard), Space (check mode, then `--upload --delete style.css --record`), A6 checks per surface plus the independent public review, receipt, failure path. Conditions for the return are in R-2b and R-4 |
| **4** | **The CP-21 publication plan, as scope** | | |
| 4.1 | §4 table, outcome A, steps 1–18 | PASS | As in items 2.1–2.19 |
| 4.2 | §4 "Headline", "Released product", "Limits to check" | PASS | The headline moves to v4 with metric names and leads with the verdict. The orientation gives the share of v3's score with CP-21's interval. The opening pairs research v4 with released v1. The demo and product docs are unchanged. Limits as in 2.21 |
| 4.3 | §4 "in both outcomes" statements | PASS | The ladder B3 → L-P → L-R → HGL discloses that B3 → L-P bundles weather with size selection and the missing-input rule (`v4.method.ladder`, chart label and description; C106, W23). The block split L-R − L-P reads "no demonstrated joint preference" with its values, on the reading path in "not established" and in the transition card (C111, W22) |
| 4.4 | §6 surface table | PASS | GitHub/README, Pages, MLflow, card and demo all have actions and evidence in packet §8. The bundle changed, so `make wasm` was run and the Space upload is planned. The demo still runs v1 |
| 4.5 | §6 `style.css` paragraph | PASS | The deployment deletes exactly `style.css` in the same Hub commit, then verifies the served set equals the bundle. Check mode confirms the set today (run 21) |
| 4.6 | §7 sequence | PASS so far | As in 2.22 |
| **5** | **v21-r8 §18.5: the planned-item correction** | | |
| 5.1 | 4.6 is DDNN alone; no TabPFN or "tabular foundation model" on any surface | PASS | The page shows "A distributional neural network … Work item 4.6 · DDNN". Zero matches for TabPFN or "tabular foundation" in the page, README, both cards, the whole `dist/space-wasm` and the export |
| 5.2 | Its question names v4 as the comparator ("same information, same opponent") and fixes no design | PASS | "Does a distributional neural network improve on v4, with the same information and on identical hours?" v4 is filled from the registry. It is neither standalone nor a blend member. The evidence line follows §18.4 (4.6L, 4.6R, 4.6C) |
| 5.3 | 4.5 leaves the list | PASS | "Models for different parts of the day … 4.5 · Three-block LightGBM" is removed; it is now v4's chapter |
| 5.4 | Other items keep their content; the comparator follows the registry; W14 unchanged | PASS | 4.4V, 4.8 and 4.7T are byte-identical in content. "would be compared with v4". The W14 regex is unchanged (`test_45`). Historical records naming TabPFN are untouched |
| 5.5 | Regression test and negative control over every generated surface | PASS | `planned_problems` covers the page, README blocks and both cards. Four doctored-page controls plus a card/README control |
| **6** | **Critic and return** | | |
| 6.1 | `gauntlet-templates.md` §2: the verdict form | PASS | This file |
| 6.2 | `gauntlet-templates.md` §3: the return | N/A at the candidate, with reason | The return follows the MLflow upload, the final build and the focused recheck (brief, "Reviews and evidence"; "Stop and return"). Conditions for it are listed below |
| **A** | **Further assignment items** | | |
| A.1 | Claims against `cp21-claims.md` (C100–C127, W22–W27; W1–W21 earlier) and `publication-claims.md` (P51, P52, PRES-3 notes) | PASS | Every v4 number on the page matches its committed row (runs 11–14, the peak rows). W22–W26 have guards with negative controls. W27 holds: every v4 number sits under its class badge |
| A.2 | Editorial review and its dispositions | PASS | `editorial.md` was written at `7dd234b` by an agent that authored no changes. Its V1–V5 are repaired at the candidate, each verified in the rendered text. Its fourteen recommendations each have a disposition in the advisory log. PRES-2's R1–R7 each have a one-line disposition |
| A.3 | Fresh reader | PASS | As in 1.20 |
| A.4 | No previously published record changed | PASS | v3, v2 and v1 chapters, the product section, both earlier transitions and the v1 archive are byte-identical to `17f354e`. The 23 published MLflow runs, the 55 artifacts and the experiment tags are unchanged. No historical evidence file, anchor, locked file, `pyproject.toml` or `uv.lock` is in the diff |
| A.5 | `scripts/deploy_space.py` and its offline tests | PASS | One `create_commit`, with adds and deletes, against the revision just read. Check mode lists the deletion set and writes nothing. Upload refuses unless the declared set equals the computed one (`--delete`/`--delete-none`). A deletion-only commit is possible; an identical Space gets no commit. After the commit it verifies the tree by path and per-file hash (blob SHA-1 or LFS SHA-256) and writes the record. Failures are recorded as type and status only. `HF_TOKEN` is read only inside the commit. 21 offline tests, including the extra, missing, changed, too-few, too-many and delete-none negative controls; a fake Hub records every call |
| A.6 | Reproduction: determinism and bundle hash | PASS | Runs 4, 5 and 18 |

## On FAIL only

Not applicable: the verdict is PASS.

---

## §10.1 output 1 — Existing-rule violations

**None.** I found no violation of an effective clause at the candidate. Two observations were
weighed and not classified as violations:

- **The packet §9.1 stale placements (R-1).** The required §13 record of the candidate's placements
  exists correctly in packet §7 and in the committed `pres-3-local-release.json`. The §9.1 row
  mis-transcribes it, and no compliance conclusion changes.
- **The targets' met / not-met column.** Standard v1 §15 states no location for the column. It is
  in the value table, N and the target in words with its date stay on the reading path, and the
  reading path names every policy that met both targets. PA1 is the right remedy.

## §10.1 output 2 — Product recommendations (not violations)

- **R-1 (documentation erratum; record it in the return, not by editing the packet).** Packet
  §9.1, row "§2 reader contract and placements; A1, A2", gives the finding at
  "1,677.6 / 1,678.3 px … and 2,379.5 px".
  - Those are attempt 3's values for the page at `d9c4438`.
  - The candidate's values are 1,702.6 / 1,703.3 px and 2,400.5 px. My run 23, packet §7 and the
    attempt-4 record all give them.
  - The brief limits the focused recheck's delta to the index and the final-build outputs, so the
    packet cannot be corrected in place. The return should state the erratum. This verdict records
    the correct values.
- **R-2 (Lead step after this PASS).** Packet §6's upload command omits `--owner-instruction`.
  - `scripts/mlflow_publish.py` refuses a public upload without it, before any write (L380). The
    failure is closed, but the command as written will not run.
  - Add the brief's authorization text, verbatim.
- **R-2b (the return).** `.local/artifacts/pres-3/msgs/land.txt`, which packet §8.2 uses for
  `git commit -F`, does not exist yet (only `c01.txt` does). Write it before the return.
- **R-3 (Owner).** Two Owner-scoped gaps should be listed as outstanding actions in the return's
  receipt (packet §8.1), not only in the advisory log:
  - **A-PRES3-7, the GFS attribution.** The line says "the v3 research model's weather data" while
    v4 uses the same columns.
  - **A-PRES3-1, the MLflow experiment description.** After the upload it will name four parents
    while five exist. Updating it is an experiment-level write outside the brief's five-run
    authority, so pinning it was correct.
- **R-4 (Owner packet).** The §8.5 Playwright commands need
  `PLAYWRIGHT_BROWSERS_PATH=/Users/djourno/Downloads/PJM/.local/tools/ms-playwright`. The packet
  states this in prose, but the commands are not ready to run as written; put the variable inline.
  - "Each passes with `passed` true" does not fit `demo` and `states`, whose records carry per-run
    fields, not a top-level `passed`. Give their expected fields: ready, 0 console errors and 0
    failed requests for `demo`; failure, failure, retry → ready for `states`.
- **R-5 (charts, tooling; A-PRES3-6).**
  - v4-c6 at 1440: the v4 diamond touches the "nominal 80%" and "nominal 95%" labels and hides the
    nominal tick and v3's circle.
  - v4-c3, fold 3: the v3 circle covers most of the v4 diamond.
  - v4-c4: the right-edge "40" tick ends within a pixel of the viewBox.
  - Meaning survives in each case: the values are printed beside the marks, and v3's published c6
    has the same pattern.
  - Extend the overlap check to text against marks, as A-PRES3-6 proposes.
- **R-6 (copy).**
  - The headline's rule in words stays abbreviated (editorial recommendation 6, deferred).
  - The headline term's link text "Read them" is generic; "Read the four conditions" would be more
    descriptive.
  - Optionally name v2 and normalized LEAR as tested and not met in the target sentence (editorial
    recommendation 13).
- **R-7 (determinism; A-PRES3-2).**
  - The bundle hash depends on the interpreter's gzip OS byte. Here it is 0xff (Python 3.13.15);
    PRES-2's copy has 0x13. CI's Python 3.12 build would reproduce neither hash.
  - The primary checkout's `.venv` is Python 3.13.15, so packet §8.4's `make wasm` → `9028a118…`
    expectation holds today.
  - Write the gzip header explicitly. The page's cold-start line still measures PRES-2's bundle
    (R2 in PRES-2's list); the Owner's A6 re-measurement settles it.
- **R-8 (code).** `derived._adoption_eligible` returns `len([candidate])`, which is 1 by
  construction, so its negative control cannot change N. Derive N from the protocol's eligible
  list, and add a control with two eligible candidates.

## §10.1 output 3 — Proposed rule amendments

- **None of my own.**
- **I endorse PA1 / A-PRES3-5** (the editorial review's): add a note on standard v1 §15 that the
  met / not-met column may sit in the comparison's value table, provided the chart's description
  points to it and the target in words, its date and N stay on the reading path.
  - **Observed problem:** the clause states no location.
  - **Cost:** none beyond P25.
- **Verification limit.** The Owner's direction of 2026-10-01, which moved the column, is recorded
  only in the Lead's and editor's records. I could not verify it, and my finding does not depend on
  it.

## Comparison with earlier reviews (after my findings were formed)

- **The editorial review.**
  - Its V1–V5 are repaired at the candidate, and I confirmed each in the rendered text:
    - V1: the comparison terms are visible directly under the caveat.
    - V2: the README states the threshold, N = 12 and who met.
    - V3: the reading lists the four conditions, and the README carries the rule.
    - V4: the arms read "no demonstrated joint preference".
    - V5: the labels say "confidence interval".
  - Its recommendations 6, 11, 13 and 14 match my R-3 and R-6. Its recommendation 12 (stale MLflow
    route) is closed by the `_indexed` guard: run 26 shows the final build refusing until the index
    covers the eight-row comparison and `compare:v4`.
- **The fresh reader.**
  - Its one violation ("policy" undefined beneath the headline) is repaired at the candidate.
  - The repair moved the finding 25 px down. That is why packet §9.1 (R-1) now lags packet §7.
- **No claim of closure is contradicted by my evidence**, except the stale §9.1 figures.
- **New relative to both reviews:** R-1 (erratum), R-2 (`--owner-instruction`), R-2b
  (`land.txt`), R-4
  (the inline environment variable and the expected fields) and R-8 (N's derivation).

## Conditions for the focused recheck at the final SHA

The brief limits the final delta to the index and the final-build outputs. The recheck should
confirm the following:

- `git diff --name-only 747d2bb..<final_candidate_sha>` lists only:
  - `reports/presentation/mlflow_index.json`;
  - `docs/index.html`;
  - `reports/cp3/pages_build.json`, now with `final: true`;
  - `.nojekyll`, if touched;
  - the upload, mirror and route records under `reports/presentation/release-checks/pres-3-*`.
- `make publication-guard` passes.
- `build_pages.py --final` succeeds, and the index has `compare:overview` with its eight run keys
  and `compare:v4` with its five.
- The release check reruns in both engines. The added MLflow links sit below the finding, but the
  phone margin is only 19.5 px.
- `mlflow_export.py --check` is current, and the uploaded runs equal `cp21.json`
  `68d165142e720e2bc0485e511fe85fe1bff40efddb6bce50290f53ddc904ff7f`.
- The bundle stays `9028a118…`.

## Worktree accounting

- **Created:** `/Users/djourno/Downloads/PJM/.local/worktrees/critic-pres-3`, detached at
  `747d2bb`. It was clean at the end, and it is removed after this record is written.
- **Not created:** no branch, tag or ref.
- **Servers:** the local HTTP servers on 127.0.0.1:8741 and 8742 are stopped.
- **Scratch:** all output is under `/Users/djourno/Downloads/PJM/.local/tmp/pres-3-critic/`.
- **Writes:** none to any remote. No MLflow, Hugging Face or Git write.
- **Removal confirmed.** At 06:31 IDT, `git worktree remove …/critic-pres-3` exited 0 after an empty `git status --porcelain`. `git worktree list` now shows only the primary checkout and the Lead's `pres-3/lead`.

## Focused recheck at the final SHA

**Result: PASS at `4ad7d09f5b9405f09b633326979890e9fa9180ca`.** The final delta holds only what the
brief allows. Every check those files affect passes again. The public MLflow holds the five cp21 runs
equal to the committed export, and the 23 earlier runs are unchanged.

- **Worktree:** `/Users/djourno/Downloads/PJM/.local/worktrees/critic-pres-3-final`, detached at
  `4ad7d09…`, created at 06:59 IDT (Thursday 2026-10-01).
- **Cleanliness:** `git status --porcelain` was empty after creation, after every step below and at
  the end (07:18 IDT).
- **Environment:** `MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=true MLFLOW_DISABLE_AGENT_HINT=1` was
  exported throughout.
- **Scratch:** `/Users/djourno/Downloads/PJM/.local/tmp/pres-3-critic/final/`.

### Commands actually run

| # | Command | Exit | Observed |
|---|---|---|---|
| F1 | `git merge-base --is-ancestor 747d2bb… 4ad7d09…`; `git log --oneline 747d2bb..4ad7d09` | 0 | Ancestor; one commit, `4ad7d09 PRES-3: cp21 uploaded, verified and indexed; the final build` |
| F2 | `git diff --name-only 747d2bbc9336758ce4a26d12a5d9ddb35d46e72a..4ad7d09f5b9405f09b633326979890e9fa9180ca` | 0 | Six files, all allowed (details below the table) |
| F3 | Line-level diff of `docs/index.html`, `747d2bb` → `4ad7d09` | 0 | Exactly two insertions, both inside existing evidence rows (details below the table) |
| F4 | Index diff, `747d2bb` → `4ad7d09` | 0 | `compare:overview` run keys go from 7 to 8. `compare:v4` is added with REST passed and browser passed (Chromium, WebKit). The other five routes are unchanged. `runs`: 23 → 28, added exactly the five cp21 keys, 0 removed, **0 changed run IDs**. `verified_at_utc` `2026-10-01T03:43:47Z`, `browser_checked_at_utc` `03:52:06Z`. The run IDs parsed from each URL map back, in order, to the expected run keys |
| F5 | `uv sync --locked --dev --offline`; `make wasm` | 0; 0 | Gate max deviation 0.0. 805 files, 44,164,910 bytes. `bundle_sha256` `9028a11869a378ea5c3401a00ad46368e1c9e2f2f9f8732330d32b71af081585`, unchanged |
| F6 | `make publication-guard` | **0** | "publication-guard: the tree carries no placeholder and a final build record" |
| F7 | `uv run python scripts/build_pages.py --final` | **0** | Wrote `docs/index.html` (1,907,451 bytes) and `pages_build.json`; porcelain empty |
| F8 | `uv run python scripts/rebuild_presentation.py`; `git status --porcelain` | 0 | Rebuilt in 11.2 s; **porcelain empty** |
| F9 | `make verify` | 0 | PASS. `docs/index.html` is 1,907,451 bytes, with 0 external fetch references and no gated DagsHub UI links. Parity across the page, README, both cards and the export |
| F10 | `make lint-publication` | 0 | page, README and templates: 0 findings |
| F11 | `uv run python scripts/mlflow_export.py --check` | 0 | "the committed export is current". `cp21.json` is `68d165142e720e2bc0485e511fe85fe1bff40efddb6bce50290f53ddc904ff7f`, unchanged |
| F12 | `uv run pytest -q -p no:cacheprovider tests/test_34_*.py tests/test_38_*.py tests/test_39_*.py tests/test_40_*.py tests/test_41_*.py tests/test_43_*.py tests/test_45_*.py` | 0 | **184 passed** |
| F13 | `uv run pytest -q -p no:cacheprovider -rs` (full suite) | 0 | **1280 passed, 7 skipped**; the same three skip reasons as at the candidate |
| F14 | `uv run python scripts/verify_mlflow_mirror.py verify --target public --out <scratch>/public-mirror-critic.json` (anonymous REST, no credential, no write), 04:02:53Z | 0 | **passed=True**, problems []; expected 28, found 28, 9,178 metric points (details below the table) |
| F15 | `check_reader_paths.py mlflow-routes --mirror-record <scratch>/public-mirror-critic.json --shots <scratch>/mlflow-routes --out <scratch>/mlflow-routes.json` (anonymous browser) | 0 | All seven routes pass in Chromium and WebKit, including `compare:overview` and `compare:v4`. I looked at the screenshots myself (details below the table) |
| F16 | `python3 -m http.server 8743 --bind 127.0.0.1 --directory docs`; `check_reader_paths.py release http://127.0.0.1:8743/index.html --shots <scratch>/release --out <scratch>/release.json` (served bytes `97e1d862…`), 04:17:32Z | 0 | **passed=True**, with placements identical to the candidate (details below the table). Server stopped afterwards |
| F17 | `check_links.main(record=<scratch>/links.json)` (scratch record; the tracked file is untouched) | 0 | "failed destinations: none"; both new compare-runs URLs answer 200 |
| F18 | Pattern scan of `git diff 747d2bb..4ad7d09` for token shapes, `Authorization`/`Bearer` and home-directory paths | 0 | 0 matches |

**F2, the delta.** The six files are:

- `docs/index.html`;
- `reports/cp3/pages_build.json`;
- `reports/presentation/mlflow_index.json`;
- `reports/presentation/release-checks/pres-3-mlflow-upload.json`;
- `reports/presentation/release-checks/pres-3-public-mirror.json`;
- `reports/presentation/release-checks/pres-3-public-mlflow-routes.json`.

These are the index, the final-build outputs, and the upload, mirror and route records, nothing
else. The README, both cards, the export and the bundle are unchanged.

**F3, the page change.**

- **Line 509** (the comparison's evidence row) gains `<a class="ev external reader" …
  data-route="compare:overview">Compare the runs in MLflow</a>`. Its eight run IDs are cp21/HGL,
  cp20/HG, cp16/V2-H, cp15/B2, cp15/A1, cp15/B3, cp15/B1 and cp15/B0.
- **Line 546** (the v4 chapter's evidence row) gains the same link with `data-route="compare:v4"`.
  Its five run IDs are cp21/HGL, cp21/L-P, cp21/L-R, cp21/L-N and cp20/HG.
- **Size:** +923 bytes. The page is now 1,907,451 bytes, SHA-256
  `97e1d86203a766534045a57a6616269982a7730756f6a0a96965497be92b9530`.
- `pages_build.json`: `final` false → true; `links_omitted_until_verified` → []; `routes_published`
  gains `compare:overview` and `compare:v4`.

**F14, the public mirror.**

- Every run's run name, parent link, params (no extras), tags, metric histories (no extra metrics),
  artifact SHA-256 values and upload-completion tags equal the committed export, including
  `cp21.json` `68d16514…`.
- cp21 run IDs:

  | Run key | Run ID | Points | Artifacts |
  |---|---|---|---|
  | `cp21` | `bc152519…` | — | 2 |
  | `cp21/HGL` | `d7c53e9d…` | 531 | 10 |
  | `cp21/L-P` | `c9b02160…` | 573 | — |
  | `cp21/L-R` | `cbdb4a2a…` | 573 | — |
  | `cp21/L-N` | `2990b108…` | 573 | — |

- The experiment tags equal the export; no unexpected run key exists.
- The 23 earlier runs keep their PRES-2 run IDs and equal the export. That export is unchanged since
  `17f354e`: candidate run 10 found 55/55 digests unchanged.
- All seven routes pass their REST check.

**F15, what the route screenshots show.** "Comparing 8 Runs from 1 Experiment" and "Comparing 5
Runs", with the parallel-coordinates plot and run details. The names read "v4 · three-block LightGBM
added (HGL)", "Pooled LightGBM with weather (L-P)" and so on. Anonymous: no sign-in redirect.

**F16, the release check on the final page.**

- **Placements, identical to the candidate's:**
  - headline block 800.6/801.3 px at 1440 and 628.6/628.7 px at 390;
  - finding 1,702.6/1,703.3 px (limit 1,744) and 2,400.5 px (limit 2,420).
  - The new links sit in evidence rows below the finding.
- **Charts:** smallest text 12.21 px; 0 overlaps.
- **Requests:** 0 failed requests, console errors, HTTP errors or post-document resources at every
  width in both engines.
- **Accessibility:** trees, keyboard, touch, contrast and zoom/reflow pass in both engines.
- **A5 discovery:** 33 routes per engine at both sizes, all passed.

### Judging the Lead's records

I judged these against my own runs rather than trusting them.

- **`pres-3-mlflow-upload.json`.** Target public; `export_commit` `747d2bb…`; 03:32:41–03:43:30Z,
  after this review's candidate PASS.
  - `owner_instruction` quotes the brief's authorization verbatim and cites the PASS at `747d2bb`.
    This closes R-2 for the run itself.
  - `write_plan`:
    - authorized = the five cp21 keys;
    - `experiment_exists` true;
    - `experiment_tags_to_write` [];
    - every other run `complete`;
    - `to_write` = the five cp21 keys.
  - The 23 earlier runs are "skipped (complete)". The five cp21 runs are "created", with points
    logged 0, 531, 573, 573 and 573. These equal the export's per-run counts and my F14.
  - 236 write operations, all inside the authorized runs.
  - No experiment tag was written, so the experiment description stays the published one
    (A-PRES3-1).
- **`pres-3-public-mirror.json`.** It matches my F14 exactly: the same 28 run IDs, the same
  per-run point counts, passed, problems [].
- **`pres-3-public-mlflow-routes.json`.** It matches my F15: all seven routes pass in both
  engines, with no failed requests, console or API errors, or sign-in redirect.
- **Conclusion.** Nothing in these records is contradicted by my evidence. MLflow was written only
  within the brief's one authorized action. No other external write is evidenced or needed for this
  commit.

### Disposition of the conditions set at the candidate

Every condition in "Conditions for the focused recheck at the final SHA" (above) is met.

- **The delta.** `.nojekyll` and the export are untouched. The record names differ from my
  anticipated list only in naming; they are the upload, mirror and route records.
- **The final gates.** `publication-guard` passes, and `--final` succeeds.
- **The index.** It holds `compare:overview` with its eight run keys and `compare:v4` with its five.
- **The release check.** It reruns in both engines with unchanged placements; the phone margin is
  still 19.5 px.
- **The export.** `--check` is current, and the uploaded runs equal `cp21.json` `68d16514…`.
- **The bundle.** It stays `9028a118…`.

### Still open, carried to the return (unchanged recommendations, none a violation)

- **R-1.** The packet §9.1 placement erratum is to be stated in the return.
- **R-2b.** `land.txt` is to be written before the return.
- **R-3.** The GFS attribution (A-PRES3-7) and the experiment description (A-PRES3-1) are Owner
  actions in the receipt.
- **R-4.** The §8.5 commands need `PLAYWRIGHT_BROWSERS_PATH` inline, and expected fields for `demo`
  and `states`.
- **R-5 to R-8.** As stated above.
- **The public A6 checks.** The landing, the push, the Space upload deleting exactly `style.css`,
  and the A6 public checks remain the Owner's (packet §8). A local PASS is not a deployed
  publication.

### Worktree accounting for the recheck

- **Created:** `/Users/djourno/Downloads/PJM/.local/worktrees/critic-pres-3-final`, detached at
  `4ad7d09…`. It was clean at the end, and it is removed after this record is written.
- **Not created:** no branch, tag or ref.
- **Servers:** the local server on 127.0.0.1:8743 is stopped.
- **Writes:** no commit, push, upload, or MLflow or Hugging Face write; no credential was read or
  printed.
- **Removal confirmed.** At 07:19 IDT, `git worktree remove …/critic-pres-3-final` exited 0 after an empty `git status --porcelain`. `git worktree list` shows only the primary checkout and the Lead's `pres-3/lead`.
