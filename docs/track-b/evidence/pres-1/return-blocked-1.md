# Track B Checkpoint Return — PRES-1

## Status

**BLOCKED.** The authenticated read-only DagsHub prerequisite returned HTTP 403. No F1 upload was attempted. This is not a publication-ready candidate and is not authorized for landing or push. The independent review result below is preserved separately from this external blocker.

## Identity

- Repository: `/Users/djourno/Downloads/PJM`; checkpoint: PRES-1.
- Lead checkout: `.local/worktrees/pres-1/lead`; branch: `gauntlet/pres-1`.
- Controlling standard: `docs/track-b/evidence/pres-1/publication-standard-v1.md`, version 1, SHA-256 `01d721c2ba6316ca9a2f707e79da229bef732e91bad22f6ce457fb01e69478cc`.
- Supporting plan: `docs/track-b/presentation-and-tracking-plan-2026-09-24.md`, revision 3, SHA-256 `281193740a256a99a1676d53ef61c9babb5f744a7d0fb038927e305d1149812c`, as amended by standard §15.
- Active brief: `pres-1-conformance-brief-2026-09-28.md` in this evidence directory, SHA-256 `51dd9b8685ea9feb774bd27a7d1241d7e678182dd93b1820cead686686d1f502`.
- Starting `main` at this resumption: `a8bee0ce5b3d1f25d0b477c88c53c21f50bd163f`, clean and equal to local `origin/main`. No fetch was performed, so this is not a new remote-freshness claim.
- Historical PRES-1 branch base: `e8025cc`; conformance starting candidate: `af0abb090ad3eba2888c3791ebe3cdcf28409a7f`.
- The Owner's resumption instruction superseded the brief's old expected candidate and named `49cc9ac`; inspection confirmed it with no mismatch.
- `final_candidate_sha`: **49cc9ac3e97b090a65a711f0b853b06e11aa1cc9**. This names the reviewed stopped candidate, not a passing publication candidate.
- `evidence_tip_sha`: the commit containing this return, resolved exactly by `git log -1 --format=%H -- docs/track-b/evidence/pres-1/return.md`; its full 40-hex SHA is supplied in the terminal handoff. A commit cannot contain its own SHA as file content.
- Candidate-to-evidence delta: only the following evidence paths (verified after commit):

```text
docs/track-b/evidence/pres-1/changed-files.md
docs/track-b/evidence/pres-1/independent-check-3.md
docs/track-b/evidence/pres-1/resumption-preflight-2026-09-28.json
docs/track-b/evidence/pres-1/return.md
```.

## Repository state and preservation

`git status --porcelain=v1` is empty after the evidence/return commit. `git diff --stat` and `git diff` are empty for the working tree. The full checkpoint delta is accounted below. The final branch is 49 commits ahead / 3 behind `main`, including this single evidence-only resumption commit.

Only return/evidence files were added during this resumption. No source, generator, generated surface, research record, test, anchor, standard, configuration, `progress.md`, model, data or dependency file was changed. The current page/README/cards retain the candidate's bytes. `main` was neither edited nor staged; no merge, push, tag, public upload or redeploy was performed.

The root has only `main` and the accounted-for `gauntlet/pres-1` branch. At entry the latter was 48 ahead / 3 behind `main`; the three main-only commits are not silently imported. Final topology and all remaining worktrees are recorded below. Full checkpoint file reasons are in `changed-files.md` (91 inherited files, plus resumption evidence). The full inherited diff is retained in `.local/tmp/pres-1/resumption-full.diff`; exact reconstruction: `git diff --binary main...49cc9ac3e97b090a65a711f0b853b06e11aa1cc9`.

## Complete checklist with direct evidence

This covers the whole checkpoint, including phases 0–E, conformance W1–W16 and the remaining publication sequence. “Prior evidence” identifies existing records; it does not claim a new Lead rerun or override the independent verdict.

### Plan revision 3 §12, as amended

| Phase | Acceptance / status | Direct evidence |
|---|---|---|
| 0 | Prior diagnosis and required startup states recorded | `reports/presentation/release-checks/2026-09-24-demo.json`; later demo/state records; Owner device observation retained without inventing device/browser |
| A | Prior content/claim mapping; preserved research boundary | `docs/track-b/research-content/{cp20-update,cp20-claims,cp15-cp16-claims,publication-claims}.md`; independent verdicts |
| B | Evidence/claim modules and negative controls implemented; new review governs remaining defects | `src/delu_forecast/{research,research_claims,derived}.py`; tests 29–32/36; `conformance-checks.md` |
| C | Local rehearsal, interrupt/resume and deliberate-fault detection recorded; public capability unproven | `reports/presentation/mlflow-capabilities.json`; `mlflow-export/`; checks 1–2; no public F1 in this resumption |
| D1 | Owner approved 2026-09-25 | `owner-decisions.md`; `reader-tasks-d1.md`; `reports/presentation/d1/specimen.md` |
| D2 | Full page, README, demo/card implementation present; subject to fresh review findings | `docs/index.html`; release records; `conformance-checks.md`; `independent-check-3.md` |
| E | NOT COMPLETE: no terminal acceptance claimed | Historical checks 1–2 FAIL; fresh check 3 below; cold-reader record and 3.12/3.13 results preserved |
| F | BLOCKED before F1; F2–F4 not performed; F5–F8 remain outside this Lead's execution | `resumption-preflight-2026-09-28.json`; no verified index; build `final: false` |

### Conformance brief §4, W1–W16

| # | Acceptance / current disposition | Direct evidence |
|---|---|---|
| W1 | Copies and decisions present; hashes independently checked at entry | Standard/brief hashes above; `owner-decisions.md` |
| W2 | Registry and introduction proof present; final identity fixed before any F1 | `registry-zero-diff.md`; export-diff records; `registry.py`; tests 35/41 |
| W3 | **FAIL:** tested-count provenance and re-validation defects; repair required | `derived.py`; `publication-claims.md`; tests 36; `independent-check-3.md` |
| W4 | Headline and placements previously measured within the standard's floors | `2026-09-28-standard-s10.json`; desktop headline ~775 px/finding ~1767 px; phone ~605 px/~2490 px; `conformance-checks.md` |
| W5 | **FAIL:** evidence slot precedes limitations/decision; archive and size checks otherwise implemented | `build_pages.py`; tests 38; page 1,558,019 bytes; fresh verdict |
| W6 | Reading-path rules and lint negative controls implemented | `publication_lint.py`; tests 37; `conformance-checks.md`; fresh verdict |
| W7 | Registry-token statuses and source lint implemented | Registry/status templates; tests 35/37; fresh verdict |
| W8 | Evidence-tier classifier, dated labels and tests implemented | tests 38; `registry.EVIDENCE_TAGS`; fresh rubric review |
| W9 | Generated README structure and registry-based card parity implemented | `readme_research.py`, `build_space.py`, `verify_release.py`; tests 32/39; Owner's focused allowlist extension |
| W10 | Completeness guard implemented; its actual publication acceptance remains OPEN | Build record `final: false`; six routes omitted; hook after secret guard and CI backstop; tests 40 |
| W11 | Local export/publisher/verifier and route checks implemented; F1–F3 BLOCKED | `mlflow-tracking-spec.md`; `mlflow-capabilities.json`; dry-run evidence; failed authenticated prerequisite |
| W12 | Referenced fonts/assets packaged; prior four cold starts had zero failed requests | `2026-09-28-demo-w12.json`; bundle record; tests 23; fresh verdict |
| W13 | System-view stack rendered | `build_pages.py::system_view`; tests 38 |
| W14 | Run/README/marker content pins replaced by contract tests | tests 31/32/34 and their negative controls |
| W15 | Runbook, packet and advisory log present | `publication-runbook.md`, `publication-packet-template.md`, `publication-advisory-log.md`; tests 42 |
| W16 | Exact template and fourth-generation encoding proposals supplied below, without editing locked templates | W16 section of this return; drafts used only as input, ordering corrected against standard §12 |

### Standard clauses in force (§16)

| Clause | Coverage / disposition |
|---|---|
| §1 | Headline/orientation placements and reading contract: release record and fresh review; placement margins remain narrow |
| §2 | Evidence classes and claim limits: registry/claims and fresh review |
| §3 | **FAIL:** policy counts depend on row order and tested/first-to-meet records evade re-validation; headline N=8 itself re-derives |
| §4 | Numeric/plain-language lint and protected v1 wording: W6, tests and fresh review |
| §5 | Registry identities/status/comparability: W2/W7/W9/W11 and fresh review |
| §6 | **FAIL:** the chapter evidence slot is in the wrong order; other architecture checks are separately recorded |
| §7 | Frozen evidence labels/link tiers: W8 and rubric review |
| §8 | README/card/MLflow source and parity: W9/W11; public mirror pending |
| §9 | Publication must remain blocked: non-final build and missing verified routes |
| §10 | Existing release record and fresh review; no real Safari, real iPhone or screen reader used |
| §11 | Independent review preserved; no binding PASS asserted; publication checks incomplete |
| §12 | Packet/runbook present; sequence stops before upload |
| §13 | Ratified hashes checked; no core or token changes |
| §14 | Carryover invariants individually accounted below |
| §15 | Amendments applied as controlling rules, not old contradictory acceptance wording |

### All 26 carried invariants (plan §6, standard §15 amendments)

| # | Required invariant | Evidence / disposition |
|---|---|---|
| 1 | Zero runtime fetches on report | test 19, `make verify` prior record and fresh review |
| 2 | One v1 claim source | `claims.py`, payload/equivalence and surface agreement checks |
| 3 | Generator owns output | All inherited surface changes through generators; no surface edit in resumption |
| 4 | Exact protected v1 honesty statements | claims and archive tests; independent rubric review |
| 5 | Limitations per presented model (amended) | tests 21/39; surface parity |
| 6 | Tracking links use `.mlflow` host | verifier, route generation, link checks |
| 7 | `live_` wall | test 24; no live action |
| 8 | Attribution and licensing on surfaces | claims/cards/page; binding and surface tests |
| 9 | Near-zero sign/two significant figures, full table value (amended) | +0.0000039 reading path and full endpoint table; tests 29/30/37 |
| 10 | v2+ date cutoff 2026-04-07 | typed windows/date guards; immutable research inputs |
| 11 | Research labels, no-preference distinction, descriptive economics | claims/withheld tests; independent review |
| 12 | English surfaces and authorized visual approval | Owner D1; final visual approval delegated to Orchestrator and pending |
| 13 | Dependency files unchanged | prior check record; no diff during resumption |
| 14 | No public retired-governance text | phrase guards and independent review |
| 15 | Typed units/comparator/aggregation/evidence class | record/chart guards and independent review |
| 16 | No placeholder ships | guard must block this non-final tree; no publication performed |
| 17 | Source-bound research numbers | binding/re-derivation tests and independent review; findings remain open where stated |
| 18 | README ownership | tests 32; generated glance and generation sections |
| 19 | Only verified advertised reader routes | six new MLflow routes omitted; F2/F3 pending |
| 20 | Public-action authority | D5 authorizes F1 only after its gate; no upload attempted; final visual delegation retained |
| 21 | No new research budget | No fits, new scoring or data retrieval by resumed Lead |
| 22 | Meaning survives colour/hover removal | direct labels/shapes/table routes; chart and accessibility review |
| 23 | Phone chart variants/readable text | standard §10 release record and fresh review |
| 24 | Preserved v1 archive | archive byte-identity contract against af0abb0; fresh review |
| 25 | Demo loading/failure/retry states | recorded startup-state tests, static markup and tests 23 |
| 26 | Planned work unscored/unnumbered | page structure/claims checks and independent review |

## Integration verdict and findings

`docs/track-b/evidence/pres-1/independent-check-3.md`: **FAIL**, binding `49cc9ac3e97b090a65a711f0b853b06e11aa1cc9`. Reviewer: fresh independent agent `/root/integration_pres1`, which authored none of PRES-1. It reviewed a new clean detached `check-4` checkout; its final HEAD/status remained unchanged/empty. The verdict was copied byte-for-byte and the checkout removed.

- **W3 / standard §3.3(a):** CSV order changes historical policies-tested counts; CP-15 policies need decision-boundary N=5, CP-16 arms N=7, and v3 N=8. The validator skips `tested` and `first_to_meet`; a corrupted count of 999 passes. Required next tests: row permutation invariance, independently corrupted count and first-to-meet rejection, and source-backed decision counts. The claim map must be corrected too.
- **W5 / standard §6:** both chapters render the evidence row before limitations and the dated decision. Required next test: DOM order reading → limitations → dated decision → evidence → details, with a negative control moving evidence before limitations or decision.

These findings were not repaired after the mandatory credential-failure stop. They remain explicit work for resumption. The full pre-F1 check must pass before upload; a post-F4 focused check has not occurred. The Critic reran the full 3.12 suite (927 passed, 7 skipped), release checks, anonymous destination checks, lint, export, dry run and deterministic rebuild. It independently checked 9,025 source records and 470 raw numeric DOM bindings. It disclosed reliance on the existing unchanged-input demo cold-start records rather than claiming a new full Space rebuild/cold start.

Earlier verdicts remain unmodified:

- `independent-check-1.md`: FAIL at `9ae76f468cc9c3f6c6654261460fe5453186d1f8`.
- `independent-check-2.md`: FAIL at `28b3c2c8f4012b1b623be24fc639e6d63bc24e59`.
- The interrupted original check-3 produced no verdict. Its scratch output never establishes PASS.

Historical source/axis/contrast findings have recorded repairs in `final-audit-matrix.md`. Its old F10/F11 disposition is historical: F1 authority now exists but its gate fails; actual Safari/iPhone/VoiceOver requirements were replaced by standard §10 and the Owner's 2026-09-28 decision. No old FAIL is rewritten or retrospectively relabelled PASS.

## Reproduction and checks actually observed

The resumed Lead verified clean HEAD/branch/root topology, all three controlling document hashes, matching main/origin refs and unchanged page/card bytes. The only remote request made by the resumed Lead was authenticated read-only `GET https://dagshub.com/api/v1/user`, with redirects disabled and no response body read: HTTP **403**, precheck exit **1**. Both MLflow variables were reported **set**, never displayed. This result does not distinguish a stale credential from a DagsHub/service access restriction. See `resumption-preflight-2026-09-28.json`.

Existing pre-review execution is fully recorded in `conformance-checks.md`: Python 3.13.15 and clean Python 3.12.14 both **927 passed / 7 skipped**, `make verify` PASS, deterministic rebuild, current export, clean publisher dry run and link gate. Python 3.12 was a macOS CI-equivalent run, not an actual Ubuntu CI run. The guard correctly refused the non-final build. The fresh Critic's commands/results are in its own verdict; neither set of prior logs is treated as a substitute for that review.

To reproduce the local acceptance checks, use project-local caches/runtime and remove credential-like variables from the test process (the existing `.local/tmp/pres-1/nocreds.py` wrapper does that without printing them):

```sh
uv sync --locked --dev
uv run python scripts/build_wasm_payload.py
uv run pytest -q
make verify
make lint-publication
uv run python scripts/mlflow_export.py --check
uv run python scripts/mlflow_publish.py --dry-run
uv run python scripts/rebuild_presentation.py
git status --porcelain=v1
python3 scripts/publication_guard.py tree
```

The last command is expected to fail until F4. Do not report that expected refusal as successful publication readiness. Existing Python 3.12 workflow coverage includes the CQR fixture and test 22 model-identity gate. No new or modified repository test was authored in this resumption; the Critic authored an independent scratch verification script, preserved by path/hash in its verdict; `changed-files.md` explains the purpose of every inherited added/changed test file.

## Files changed and full diff

Resumption adds only `docs/track-b/evidence/pres-1/changed-files.md` (whole-checkpoint file reasons), `resumption-preflight-2026-09-28.json` (the authenticated HTTP 403), `independent-check-3.md` (fresh independent FAIL), and `return.md` (this handover). No test changes.

`git diff --stat main...49cc9ac`:

```text
 .githooks/pre-push                                 |    29 +-
 .github/workflows/tests.yml                        |     6 +
 Makefile                                           |    36 +-
 README.md                                          |   232 +-
 app/wasm_showcase.py                               |   182 +-
 docs/index.html                                    |   766 +-
 docs/track-b/evidence/pres-1/ci-py312.md           |    30 +
 docs/track-b/evidence/pres-1/cold-reader-check.md  |   115 +
 docs/track-b/evidence/pres-1/conformance-checks.md |   138 +
 docs/track-b/evidence/pres-1/final-audit-matrix.md |    47 +
 .../track-b/evidence/pres-1/independent-check-1.md |   217 +
 .../track-b/evidence/pres-1/independent-check-2.md |   195 +
 docs/track-b/evidence/pres-1/owner-decisions.md    |    71 +
 docs/track-b/evidence/pres-1/owner-hand-checks.md  |    44 +
 .../pres-1/pres-1-conformance-brief-2026-09-28.md  |   366 +
 .../presentation-d1-editorial-review-2026-09-25.md |   269 +
 ...resentation-final-editorial-audit-2026-09-28.md |   228 +
 .../evidence/pres-1/publication-standard-v1.md     |   741 +
 docs/track-b/evidence/pres-1/reader-tasks-d1.md    |   129 +
 docs/track-b/evidence/pres-1/reader-tasks-final.md |    59 +
 docs/track-b/evidence/pres-1/registry-zero-diff.md |   135 +
 docs/track-b/mlflow-tracking-spec.md               |   199 +
 docs/track-b/publication-advisory-log.md           |    39 +
 docs/track-b/publication-packet-template.md        |   100 +
 docs/track-b/publication-runbook.md                |   196 +
 docs/track-b/research-content/cp15-cp16-claims.md  |    22 +-
 docs/track-b/research-content/cp15-cp16-update.md  |    14 +-
 docs/track-b/research-content/cp20-claims.md       |   181 +
 docs/track-b/research-content/cp20-update.md       |   225 +
 .../track-b/research-content/publication-claims.md |    60 +
 reports/cp3/link_check.json                        |   197 +-
 reports/cp3/pages_build.json                       |    24 +-
 reports/cp3b/space_wasm_bundle.json                |    92 +-
 reports/presentation/d1/layout-measurements.json   |   735 +
 reports/presentation/d1/specimen.md                |   140 +
 reports/presentation/mlflow-capabilities.json      |   242 +
 reports/presentation/mlflow-export/cp10.json       |  2042 ++
 reports/presentation/mlflow-export/cp15.json       | 29474 +++++++++++++++++++
 reports/presentation/mlflow-export/cp16.json       |  6223 ++++
 reports/presentation/mlflow-export/cp20.json       |  3056 ++
 reports/presentation/mlflow-export/manifest.json   |  1215 +
 .../release-checks/2026-09-24-demo.json            |   212 +
 .../release-checks/2026-09-25-demo-local.json      |   132 +
 .../release-checks/2026-09-25-rebuild.json         |    15 +
 .../2026-09-25-space-states-local.json             |    91 +
 .../presentation/release-checks/2026-09-27.json    |   539 +
 .../release-checks/2026-09-28-demo-local.json      |   128 +
 .../release-checks/2026-09-28-demo-w12.json        |   112 +
 .../2026-09-28-export-diff-f1-candidate.json       |   807 +
 .../2026-09-28-registry-export-diff.json           |   798 +
 .../2026-09-28-space-states-local.json             |    91 +
 .../release-checks/2026-09-28-standard-s10.json    |   946 +
 .../presentation/release-checks/2026-09-28.json    |   536 +
 scripts/build_pages.py                             |  2748 +-
 scripts/build_space.py                             |    43 +-
 scripts/build_wasm_space.py                        |   270 +-
 scripts/check_links.py                             |   103 +-
 scripts/check_reader_paths.py                      |  1105 +
 scripts/cp3_readme.py                              |    42 +-
 scripts/lint_publication.py                        |    57 +
 scripts/mlflow_export.py                           |   882 +
 scripts/mlflow_publish.py                          |   323 +
 scripts/publication_guard.py                       |   114 +
 scripts/readme_research.py                         |   328 +
 scripts/rebuild_presentation.py                    |    97 +
 scripts/verify_mlflow_mirror.py                    |   508 +
 scripts/verify_release.py                          |    32 +-
 space-wasm/README.md                               |    18 +-
 space/README.md                                    |     9 +-
 src/delu_forecast/claims.py                        |    50 +-
 src/delu_forecast/derived.py                       |   389 +
 src/delu_forecast/publication_lint.py              |   515 +
 src/delu_forecast/registry.py                      |   685 +
 src/delu_forecast/research.py                      |  1027 +
 src/delu_forecast/research_claims.py               |   750 +
 tests/test_21_limitations_are_complete.py          |    81 +-
 tests/test_23_static_space.py                      |   105 +
 tests/test_29_research_evidence.py                 |   198 +
 tests/test_30_research_claims_rendered.py          |   504 +
 tests/test_31_page_structure.py                    |   239 +
 tests/test_32_readme_ownership.py                  |   154 +
 tests/test_33_check_links_gate.py                  |    76 +
 tests/test_34_mlflow_export.py                     |   199 +
 tests/test_35_registry.py                          |   179 +
 tests/test_36_derived_records.py                   |   180 +
 tests/test_37_publication_lint.py                  |   147 +
 tests/test_38_page_architecture.py                 |   318 +
 tests/test_39_cross_surface_parity.py              |   107 +
 tests/test_40_publication_guard.py                 |   160 +
 tests/test_41_export_zero_diff.py                  |   104 +
 tests/test_42_publication_runbook.py               |   126 +
 91 files changed, 65318 insertions(+), 572 deletions(-)
```

Whole-checkpoint one-line reasons: `changed-files.md`. Full machine-readable diff and stat are retained under `.local/tmp/pres-1/`; they are review conveniences, while the candidate and committed evidence are the durable source. No locked rulebook/template/anchor is modified.

## Elapsed, disk and network

Resumption wall-clock effort, including concurrent review and terminal preparation: approximately **0.5 hour**, rounded to the nearest half hour; the Critic also reports 0.5 hour rounded, overlapping rather than additional wall time.

After removing check-3/check-4, `du -sk` measured: PRES-1 worktrees **1,161,772 KiB** (lead only), PRES-1 scratch **280,356 KiB**, presentation screenshots **340,460 KiB**, shared uv cache **864,820 KiB**. These four measured roots total about **2.52 GiB**; they include inherited material and are not a new-disk debit. Shared pre-existing tool environments are outside that subtotal. No initial shared-cache baseline or historical peak is available, so a precise cumulative “added under .local” figure cannot be certified from this session. The new check-4 checkout/environment has been removed. All new scratch stayed inside the project; retained review script/logs/screenshots are hash-accounted in the verdict. The original check-3 scratch and check-3-stopped recovery material remain available; their logs confer no PASS.

The earlier sessions' cumulative active-hour total is not present in the durable return material supplied to this session. Commit timestamps do not establish active effort or separate Owner waiting. No fabricated cumulative total or verified 80-hour-ceiling claim is made. The Orchestrator must retain this accounting gap on resumption. The brief's approximate 60-hour timebox and hard 80-active-hour ceiling remain unchanged.

No public network write was made by this resumption: F1 was not invoked; no push, registry write, `delu-cp2` write, Space upload or redeploy. Historical local MLflow rehearsal writes are recorded in `mlflow-capabilities.json` and the earlier verdicts; these are loopback writes, not public publication. Historical records report no earlier public F1. External cost for this resumption: $0; new research fits/scores/dataset retrieval: zero.

## Open blocker and next acceptance

1. **Authentication/access:** a consuming process must be able to make the authenticated read-only DagsHub call successfully with the stored credentials. The smallest external action is for the Owner to restore that access; if the token was rotated, restarting Codex may be necessary to inherit it. Do not paste credentials into the task, change stored credentials without instruction, or infer that variable presence proves validity.
2. **Independent findings:** repair every blocking finding listed in `independent-check-3.md`, rerun affected checks and the required full gates, designate a new candidate and obtain a fresh independent PASS. No self-certification.
3. **F1–F4:** after that PASS, a current committed export, clean dry run and successful credential precheck, use the existing D5 authority for F1; verify the mirror/routes, generate and commit the index, record capabilities, make the final build and get an independent focused recheck (full if the rendered change exceeds index/link targets).
4. **Effort record:** preserve the disclosed historical accounting gap; recover prior active-hour evidence if available before claiming full compliance.

This return ends the Lead's work at a coherent blocked boundary. No later checkpoint is opened or planned.

## Landing report — deferred until acceptance

- Proposed disposition: **LAND after all open gates pass**; do not land this stopped candidate. Keep `gauntlet/pres-1` open for repair and completion, not DISCARD.
- Evidence tip to preserve: the return commit identified above and by its full SHA in the terminal handoff. Cited candidate commits are checked reachable; no branch/ref deletion or disposition tag was created.
- Branch/worktree/tag accounting: `gauntlet/pres-1` was inherited, not created anew; its purpose remains PRES-1, final tip is the evidence/return commit identified above, 49 ahead / 3 behind main, clean. The inherited lead checkout remains at `.local/worktrees/pres-1/lead`. Fresh detached `.local/worktrees/pres-1/check-4` was created at the reviewed SHA for this independent check and removed after verdict preservation. Interrupted `.local/worktrees/pres-1/check-3` was verified clean at that SHA and removed under this checkpoint's lifecycle; its external scratch is retained. Earlier recorded check-1/check-2 and ci-1 through ci-6 checkouts were already absent. No branch or tag created in this resumption; only main and the lead checkout remain registered..
- Live branch references in permitted read scope: this return; `docs/track-b/evidence/pres-1/pres-1-conformance-brief-2026-09-28.md`; `docs/track-b/pres-1-brief-2026-09-24.md`. The two preserved editorial reviews also contain historical references, which must remain historical evidence. Program-state references were not inspected; the Orchestrator owns their inventory and repointing. Locked documents are never edited under a generic reclamation instruction.
- Proposed eventual squash message: `Publish the v1–v3 research presentation with registry-driven claims and verified MLflow routes` — use only after the stated publication gates are met.
- Space bundle currently recorded: `eb122883896d755fd3314b6b5d361c1f6d23e0251412edfeeeef5c6201b8aacb` (805 files, 44,162,066 bytes). This is the **pre-F4** bundle; the final card gains verified links and requires a new bundle/hash.
- Exact redeploy command from `docs/deploy.md`, for the authorized publisher after final approval, **not executed**: `hf upload Yarden-Viktor/delu-day-ahead-forecast dist/space-wasm . --repo-type space`. Build with `make wasm` first; use the stored credential through the consuming tool, never type it.

### F8 commands for the authorized publisher, after publication

These are future commands, not completed checks. Set output paths to the actual release date under the project `.local/` and committed release-record directory. The Pages-byte check compares the public bytes with the accepted local artifact:

```sh
curl --fail --silent --show-error https://hrsi56.github.io/delu-day-ahead-forecast/ -o .local/tmp/pres-1/pages-deployed.html
cmp docs/index.html .local/tmp/pres-1/pages-deployed.html
PLAYWRIGHT_BROWSERS_PATH=/Users/djourno/Downloads/PJM/.local/tools/playwright/browsers /Users/djourno/Downloads/PJM/.local/tools/playwright/bin/python scripts/check_reader_paths.py demo --engine chrome --engine webkit --viewport 1440x900 --viewport 390x844 --url https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/ --out reports/presentation/release-checks/postdeploy-demo.json
uv run python scripts/verify_mlflow_mirror.py verify --target public --out reports/presentation/release-checks/postdeploy-mlflow-mirror.json
PLAYWRIGHT_BROWSERS_PATH=/Users/djourno/Downloads/PJM/.local/tools/playwright/browsers /Users/djourno/Downloads/PJM/.local/tools/playwright/bin/python scripts/check_reader_paths.py mlflow-routes --mirror-record reports/presentation/release-checks/postdeploy-mlflow-mirror.json --shots /Users/djourno/Downloads/PJM/.local/artifacts/presentation/postdeploy-mlflow --out reports/presentation/release-checks/postdeploy-mlflow-routes.json
uv run python scripts/check_links.py
```

Read each record: demo readiness alone is not enough; startup, both controls/inference, failed requests, console errors and identity must be accounted for. Every advertised MLflow route must show its intended content in Chromium and WebKit anonymously.

## W16 proposals — return only

### W16 (a): proposed landing-template text: the MLflow step and the publication packet

The templates are locked; this is text for the Owner's separately authorized edit (the 2026-09-24
decision-4 suspension, extended to the packet by D6 on 2026-09-28). Nothing here edits them.

**1. `gauntlet-templates.md` §1, Orchestrator checkpoint brief — a new block after "Owner-only actions
already authorized":**

```text
## Publication (Publication Standard v1 §12)
- Standard: docs/track-b/publication-standard-v1.md, version [n], SHA-256 [hash]. The checker
  verifies the hash (§13).
- Packet (docs/track-b/publication-packet-template.md), filled in inside the checkpoint:
  the draft registry entry; the claim map; the derived headline quantities (the verdict and N,
  the ratio's interval from this checkpoint's own bootstrap draws, the per-period ranges); draft
  slot texts; the MLflow export.
- Tracking: experiment delu-generations. During the checkpoint, runs are tracked locally only
  (.local/mlruns/<cp>). The export reports/presentation/mlflow-export/<cp>.json is written by
  scripts/mlflow_export.py from committed evidence; `mlflow_export.py --check` exits 0; the
  export contract test (the export matches the registry) passes; no public write.
- Acceptance: the Integration Critic reviews the packet and the export like any other artifact:
  every metric re-derives from a committed record, every name, status, description and tag comes
  from the registry, and the record-level diff against the last published export changes nothing
  already published except names, descriptions and tags.
- No public action follows merely from checkpoint completion. When publication is explicitly
  authorized, follow docs/track-b/publication-runbook.md §1: independent PASS, upload and verification,
  final build and focused recheck, then authorized landing/push/redeploy. A non-final public surface
  never lands on main. Each public action needs its own recorded authority.
```

**2. `gauntlet-templates.md` §3, Checkpoint return — a new block after "Reproduction":**

```text
## Publication packet
- Registry entry (draft): [path or inline]
- Claim map: [path]
- Derived headline quantities: [verdict and N; the ratio and its interval, with the bootstrap
  settings; the per-period ranges; each with its committed source row]
- Draft slot texts: [path]
- MLflow export: [path]; `mlflow_export.py --check` [exit]; diff against the last published
  export: [only identity | list]
```

**3. `gauntlet-templates.md` §4, Orchestrator receipt and disposition — a publication gate before any LAND that includes changed public surfaces:**

```text
**PUBLISH — only on the Owner's explicit instruction naming each public action.**

F1  uv run python scripts/mlflow_publish.py --target public \
        --owner-instruction "<the instruction, verbatim>" \
        --log reports/presentation/release-checks/<date>-mlflow-upload.json
F2 prerequisites (also supply F3 evidence):
    uv run python scripts/verify_mlflow_mirror.py verify --target public \
        --out reports/presentation/release-checks/<date>-mlflow-mirror.json
    PLAYWRIGHT_BROWSERS_PATH=.local/tools/playwright/browsers .local/tools/playwright/bin/python \
        scripts/check_reader_paths.py mlflow-routes \
        --mirror-record reports/presentation/release-checks/<date>-mlflow-mirror.json \
        --shots .local/artifacts/presentation/mlflow-<date> \
        --out reports/presentation/release-checks/<date>-mlflow-routes.json
    uv run python scripts/verify_mlflow_mirror.py index \
        --mirror-record reports/presentation/release-checks/<date>-mlflow-mirror.json \
        --browser-record reports/presentation/release-checks/<date>-mlflow-routes.json
F2  Commit reports/presentation/mlflow_index.json: the verifier writes it, never a person.
F3  Record what the server supports in reports/presentation/mlflow-capabilities.json; a route or
    feature that fails is recorded and not advertised.
F4  uv run python scripts/build_pages.py --final     # refuses unless the index covers every route
    uv run python scripts/rebuild_presentation.py && git status --porcelain   # must stay empty
    make publication-guard                             # must pass: no placeholder, final record
    make wasm                                          # the Space card now carries the MLflow link
Then a focused recheck on the final SHA (a full one if anything beyond the index and link targets
changed), then landing, push and the Space redeploy, then the post-deploy checks.
```

### W16 (b): proposed chart encoding for v4 (plan §7.8; the tokens are the Owner's)

| Signal | v1 | v2 | v3 | **v4 (proposed)** |
|---|---|---|---|---|
| Colour | slate `#475569` | violet `#6D28D9` | teal `#0F766E` | **amber `#B45309`** (5.02:1 on white, 4.81:1 on the canvas) |
| Marker | triangle | square | circle | **diamond** (a square turned 45°, filled) |
| Direct label | "v1" | "v2" | "v3" | "v4" |

- **Why amber.** It is far in hue from the three generation colours and from the link accent
  (`#1D4ED8`), and it is neither red nor green, so it cannot read as "failed" or "passed" (plan
  §7.3: colour never means "passed"). Its luminance contrast with v1–v3 is 1.09–1.51, as low as
  theirs with each other (1.07–1.38), so, as today, the direct label and the marker carry the
  identity and no meaning depends on colour. Orange `#C2410C` (5.18:1 / 4.96:1) is the
  alternative.
- **Where it lands.** `scripts/build_pages.py::TOKENS` (`"v4": "#B45309"`), and the classes
  `.rail-v4`, `.node-v4` (the dot turned 45°), `.gen-v4` in `scripts/build_pages.py::css`;
  runbook §2, step 16. The existing contrast checks (text 4.5:1, non-text 3:1) and the token sheet
  cover it without change.
- **Decision:** the Owner's, before v4 is published (standard §16, "At v4").


## Advisory summary and interview-capture triggers

`docs/track-b/publication-advisory-log.md` contains A-PRES1-1 through A-PRES1-18: identity-bearing artifact digest semantics; private WebKit inspection API; font-copy workaround; narrow placement margins; registry/card tooling; MLflow code labels; and cold-reader questions about headline pairing, the eight-policy count, v1 comparison populations, model terminology, interval-induced median changes, protected precision, archive vocabulary, preview identity, runtime requests and interval-score levels. These remain advisory only where no active clause is violated; the new Critic's blocking findings are separately recorded.

Interview-capture triggers (Orchestrator only; no DOCX entry made here):

- How did we preserve research numbers while replacing scattered presentation identities with a registry?
- Why is a digest-restoration proof needed when artifact content contains names that intentionally change?
- How did we obtain WebKit accessibility evidence when the public automation API lacked a native-tree endpoint?
- Why did WebKit's font requests fail even though marimo's asset directory contained the fonts?
- What separates development improvement, a target verdict and permission to replace the released demo?
- Why do green tests and stored credentials not establish publication readiness?
- How should the policies-tested count be tied to actual decision provenance rather than incidental file order, if the independent finding is confirmed?

## Post-return reads

None. No `progress.md`, `orchestrator-role.md`, syllabus or Track A/C file was opened. Presentation editorial records were read as required by the brief; their incidental historical program-state remarks did not inform engineering decisions. No Q&A document was changed.
