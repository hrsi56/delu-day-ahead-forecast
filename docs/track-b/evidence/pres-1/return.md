# Track B Checkpoint Return — PRES-1

## Status

PASS — Lead implementation and F1–F4 acceptance. This is a handoff for Orchestrator verification and delegated F5 visual approval; it is not a claim that the branch has landed, Pages/Space have been redeployed, or checkpoint reclamation is complete.

## Identity

- Repository: `/Users/djourno/Downloads/PJM`; checkpoint PRES-1; Engineering Lead checkout `.local/worktrees/pres-1/lead`, branch `gauntlet/pres-1`.
- Standard: `docs/track-b/evidence/pres-1/publication-standard-v1.md`, v1, SHA-256 `01d721c2ba6316ca9a2f707e79da229bef732e91bad22f6ce457fb01e69478cc`.
- Supporting plan: `docs/track-b/presentation-and-tracking-plan-2026-09-24.md`, revision 3, SHA-256 `281193740a256a99a1676d53ef61c9babb5f744a7d0fb038927e305d1149812c`, as amended by standard §15. Ratified research anchor: `capstone_v21.md`.
- Brief: `docs/track-b/evidence/pres-1/pres-1-conformance-brief-2026-09-28.md`, SHA-256 `51dd9b8685ea9feb774bd27a7d1241d7e678182dd93b1820cead686686d1f502`.
- Starting main at resumption: `a8bee0ce5b3d1f25d0b477c88c53c21f50bd163f`, clean and equal to local `origin/main`. No fetch/remote-freshness claim. Historical branch base `e8025cc`; conformance starting candidate `af0abb090ad3eba2888c3791ebe3cdcf28409a7f`.
- Owner-requested interrupted candidate: `49cc9ac3e97b090a65a711f0b853b06e11aa1cc9`, verified before change. The previous coherent stopped return at `df470fb915271541e60b3b3a727f2bf6e1d37364` is preserved byte-for-byte in `return-blocked-1.md`. This return supersedes it.
- `final_candidate_sha`: **a0302dd6c5ff6714709b4f3a3b742f71a4b596a7** — the exact SHA of the fresh final Integration review. Every final bar binds here.
- `evidence_tip_sha`: the single final evidence/return commit, resolved by `git log -1 --format=%H -- docs/track-b/evidence/pres-1/return.md`; the full 40-hex value is supplied in the terminal handoff. A commit cannot contain its own SHA as file content.
- Candidate-to-evidence delta (verified after the evidence commit):

```text
docs/track-b/evidence/pres-1/changed-files.md
docs/track-b/evidence/pres-1/f1-f4-execution.md
docs/track-b/evidence/pres-1/independent-check-5.md
docs/track-b/evidence/pres-1/return.md
```

The command is `git diff --name-only <final_candidate_sha>..<evidence_tip_sha>`; every path must be within `docs/track-b/evidence/pres-1/`.

## Repository state

`git status --porcelain=v1`, `git diff --stat` and `git diff` are empty at return. `main` remains clean at the starting SHA, with nothing staged; no main commit, merge, push, tag or redeploy was performed. The only public write was the explicitly authorized F1 invocation described below. The final branch is **59 ahead / 3 behind main**, clean. Main's three documentation/state commits were not silently imported.

The checkpoint's full file-by-file reasons are in `changed-files.md`. The full binary-capable diff and stat are retained at `.local/tmp/pres-1/final-full.diff` and `final-diff-stat.txt`; exact reconstruction is `git diff --binary main...<evidence_tip_sha>`. No dependency, model, data snapshot, research protocol, ratified anchor, rulebook, agent configuration or program-state file was changed by this resumption.

## Complete checklist with direct evidence

### Presentation plan revision 3 §12, as amended

| Phase | Acceptance / status | Direct evidence |
|---|---|---|
| 0 | Complete: startup diagnosis and failure states recorded | `2026-09-24-demo.json`; later local demo/state records; final four cold starts and both-engine failure/retry record |
| A | Complete: claim maps, withheld phrases and frozen research boundary | `docs/track-b/research-content/{cp20-update,cp20-claims,cp15-cp16-claims,publication-claims}.md`; final independent review |
| B | Complete: source-bound record/claim/derived layers and negative controls | `research.py`, `research_claims.py`, `derived.py`; tests 29–32/36; independent numeric recomputation |
| C | Complete: local probe/rehearsal, interrupt/resume/idempotence and fault detection; actual public support now measured | `mlflow-capabilities.json`, committed export, F1/F3 records; historical local and fresh public results kept distinct |
| D1 | Owner approved 2026-09-25 | `owner-decisions.md`; `reader-tasks-d1.md`; `reports/presentation/d1/specimen.md`; preserved editorial review |
| D2 | Complete: full report, README, demo/cards, archive, charts and accessibility | Generated surfaces, contract tests, final §10/demo/state records |
| E | Complete on final independent verdict | `independent-check-5.md`, `final-checks.md`, cold-reader applicability, both Python suites; earlier FAILs preserved |
| F | F1–F4 complete; F5–F8 handed over | Actual upload, verifier index, mirror/routes/capabilities, final build and full final recheck. Orchestrator visual approval/publication/post-deploy checks remain subsequent actions |

### Conformance brief §4 — W1–W16

| # | Acceptance | Direct evidence |
|---|---|---|
| W1 | Standard/brief copies and Owner decisions preserved exactly | Hashes above; `owner-decisions.md` |
| W2 | Registry is canonical; introduction identity proof and contracts pass; names fixed before upload | `registry-zero-diff.md`; record-level export diff; tests 35/41; independent reproduction |
| W3 | Decision counts 5/7/8 tied to recorded dates, not CSV order; counts and first-to-meet freshly re-derived | `derived.py`; claim P16; tests 36 with permutation/corruption/source/tie controls; independent 60-record arithmetic |
| W4 | Exact headline, adjacent definitions and all placements pass | Final §10 record: desktop headline ≤775.3 px / finding ≤1767 px; phone ≤604.7 / ≤2490.1 |
| W5 | Generic chapter grammar with actual evidence after decision; branches and immutable archive; size <2 MB | tests 38; final DOM; page 1,560,646 bytes; archive hash `d4d19223559b89747d981bfea86f1bc64661149e842dfee96898ba2b60196021` |
| W6 | Numeric/plain-language rules, sign-preserving endpoint, p floor, definitions and lint pass | `publication_lint.py`; tests 37; independent display audit; zero page/README/source findings |
| W7 | Dated past-tense registry statuses; negative stale-status controls | Registry/templates; tests 35/37; final review |
| W8 | Typed frozen evidence labels, correct dates and reader/audit-tier links | tests 38; URL classifier and actual link checks; final review |
| W9 | Generated README ownership, per-model limitations, registry card lines and parity | tests 21/32/39; `verify_release.py`; final README/cards |
| W10 | Complete verified index; final build; no placeholder; fail-closed publication/secret guards | Six expected/published routes, zero omissions, `final: true`; tests 40; publication guard exit 0; hook ordering unchanged |
| W11 | Current registry-matched export uploaded only after PASS; complete public mirror and actual routes verified | `f1-f4-execution.md`; 23 runs / 6,928 points / 55 artifacts; six REST/browser routes; ten settled comparison charts |
| W12 | All referenced assets packaged; fresh cold starts/controls pass | Final bundle record, tests 23; four fresh Chrome/WebKit starts with zero failures/errors |
| W13 | Stack line comes from system-view data | `build_pages.py::system_view`; tests 38 |
| W14 | Run/README/marker assertions test contracts with negative controls | tests 31/32/34, registry-based expectations |
| W15 | Complete runbook, publication-packet template and advisory log | `publication-runbook.md`, `publication-packet-template.md`, `publication-advisory-log.md`; tests 42 and independent review |
| W16 | Exact template and v4 encoding proposals, below; no locked file edited | This return's W16 section, preserved from the reviewed durable proposal, not accepted merely from a scratch draft |

### Publication Standard §§1–15 in force

| Clause | Acceptance / evidence |
|---|---|
| §1 | Reading contract and placements: final §10 and unchanged cold-reader claim blocks |
| §2 | Evidence classes and limitations: registry, maps and independent review |
| §3 | Typed quantities and exact headline: every derived record independently re-derived, count defects repaired |
| §4 | Precision/plain terms: independent numeric/display checks and lint negative controls |
| §5 | Registry, status, comparator and population contracts: tests and all surface/export consumers |
| §6 | Architecture and actual chapter slot order: DOM checks, fixed archive and size bound |
| §7 | Frozen audit labels and verified reader links: classifier and actual destination/browser checks |
| §8 | README/card/MLflow parity: generator ownership, final mirror and surface checks |
| §9 | Complete final build: guard passes, no omitted route or placeholder |
| §10 | Fresh final device/accessibility checks: Chrome and Playwright WebKit; no real Safari/iPhone/screen reader claimed |
| §11 | Two-version suites, negative controls, applicable two-reader record and fresh full final Integration verdict |
| §12 | Packet/runbook and actual ordered F1–F4; remaining visual/publication actions handed over |
| §13 | Ratified hashes unchanged; no governance edits or visual token changes |
| §14 | All 26 carryover invariants individually mapped below |
| §15 | Approved amendments govern headline/target/order/precision/limitations/devices/contracts/grammar |

### All 26 carried invariants, as amended

| # | Invariant | Direct evidence |
|---|---|---|
| 1 | Zero runtime fetches on report | test 19, `make verify`, final browser report |
| 2 | One v1 claim source | `claims.py`, payload/equivalence and cross-surface checks |
| 3 | Generator owns output | Clean deterministic rebuild; no hand-edited generated surface |
| 4 | Exact v1 honesty statements | Byte-identical archive and release/claim tests |
| 5 | Limitations per presented model | tests 21/39 and final surface parity |
| 6 | Tracking uses `.mlflow` host | Verifier routes, link gate and anonymous browser checks |
| 7 | `live_` wall | test 24; no live action |
| 8 | Attribution/licensing | Page, README and cards; binding checks |
| 9 | Near-zero sign/precision and full table value | +0.0000039 reading path, exact table endpoint; tests 29/30/37 |
| 10 | Research cutoff 2026-04-07 | Record windows/date guards and unchanged research inputs; v1 published replay remains the explicit exception |
| 11 | Research labels/no-equivalence/descriptive economics | Maps, withheld-phrase tests and independent review |
| 12 | English surfaces and presentation authority | Owner D1 approval; F5 delegated to Orchestrator, still to be exercised |
| 13 | Dependency files unchanged | `git diff` confirms pyproject.toml/uv.lock unchanged |
| 14 | No retired-governance claims in public copy | Phrase guards and independent rendered review |
| 15 | Typed units/comparator/aggregation/evidence class | Record/chart guards and independent re-derivation |
| 16 | No placeholder ships | Final guard, missing-index/placeholder negative controls; no Pages/Space publication by Lead |
| 17 | Source-bound research numbers | Independent source/raw/visible/derived record audits; all F1 export hashes preserved |
| 18 | README ownership | tests 32, generated glance and generation sections |
| 19 | Only verified advertised routes | Six of six REST + both-browser routes; actual settled charts; verifier-generated index |
| 20 | Public-action authority | Only F1 under D5 after PASS, recorded in upload log; no additional publication authority inferred |
| 21 | No new research budget | No new fit/scoring/data retrieval; tests and frozen-cell re-derivation only |
| 22 | Meaning survives color/hover removal | Direct labels/shapes/table routes and final chart/accessibility checks |
| 23 | Phone variants/readable text | Final §10 measurements, including narrow widths |
| 24 | v1 archive preserved | Independent byte identity against af0abb0 |
| 25 | Demo loading/failure/retry | Final forced failure/hang/retry record and successful cold starts |
| 26 | Planned work unscored/unnumbered | Separate post-chapter planned section, source/claim tests |

## Integration verdicts and repaired findings

Final: `independent-check-5.md`, **PASS**, binding **a0302dd6c5ff6714709b4f3a3b742f71a4b596a7**, fresh agent `/root/integration_pres1_final` in detached `check-6`. The Critic independently passed 944 tests (7 documented skips), recomputed 9,025 raw and 60 derived records and 1,522 DOM bindings, verified all 23 public runs, 560 histories / 6,928 points and 55 artifact hashes, reproduced the exact bundle, and passed all required views, anonymous routes, ten settled charts and four demo cold starts. Verdict SHA-256: `3343ecf10222531cc4ecdf9085d52b06abad7dae68164532db43f603867e37a8`. The full review was chosen because F4 changes the generated tracking sentence from future to present tense as well as adding verified links. The checkout stayed clean at that SHA; the verdict was imported byte-for-byte and its worktree removed. Isolation was procedural, not a claimed read-only mount.

Pre-F1: `independent-check-4.md`, **PASS**, binding `217f4f8bd84a14cbbebb35a26b232678d1197998`, fresh agent `/root/integration_pres1_recheck` in `check-5`. It recomputed 9,025 evidence records, 60 derived records, 470 raw and 737 displayed numeric bindings; all 32 source blobs matched frozen refs. F1 used the subsequent evidence-only commit `c8e8f1096471dff0ed8841cdf5a45ce571c89619`.

Preserved historical FAILs: check 1 at `9ae76f468cc9c3f6c6654261460fe5453186d1f8`; check 2 at `28b3c2c8f4012b1b623be24fc639e6d63bc24e59`; check 3 at `49cc9ac3e97b090a65a711f0b853b06e11aa1cc9`. The originally interrupted check-3 produced no verdict; its logs never established PASS.

Check 3's W3 defect is repaired with date-based counts and independent validation of count/first-to-meet records; reordering source rows and corrupting count/first flags now fail the appropriate controls. Its W5 defect is repaired in the generic renderer and actual DOM-order controls: reading → limitations → dated decision → evidence → details. Prior source/axis/contrast findings and repairs remain in `final-audit-matrix.md`. No historical FAIL was relabelled.

The initial account-API Basic 403 was a wrong credential diagnostic, not proof that the stored token needed replacement. The actual MLflow read endpoint returns 200 with the same variables; redirect/error/leakage controls are tested. `authentication-correction.md`, the corrected read record and `f1-precheck.json` preserve this correction. Stored credentials were never changed or exposed.

## Reproduction and observed results

`final-checks.md` records the exact commands, exits, logs and hashes. Lead full suite: **944 passed / 7 skipped** on Python 3.13.15 and clean Python 3.12.14; named CQR/model-identity checks, `make verify`, lint, export-current/dry-run and final guard all pass. Both clean rebuilds leave empty Git status. This is local macOS CI-equivalent execution, not an Ubuntu CI claim. The seven deliberate/optional exclusions remain explicit; no charged replay was enabled.

`f1-f4-execution.md` records actual public activity and F4's bundle. Mirror: **23 unique runs, 6,928 metric points, 55 artifact hashes**, all params/tags/parent links equal. Six routes pass REST and anonymous Chromium/WebKit; all five comparison charts render in both engines. Fresh extra reads match **39 dataset names/digests/contexts**, **23 notes**, **19 parent links** and the v3 tag filter. Protected `delu-cp2` experiment and champion-registry metadata match the pre-F1 baseline. Dataset UI pages and a separate nesting-control interaction are not advertised as verified.

The index necessarily consumes the successful mirror/browser records before it can be written. Those F2 prerequisites supply F3's acceptance evidence, as runbook §1.5 orders; after the index commit, F3 records capabilities. The parallel browser route seed exactly matched the complete verifier's route map and run IDs. Timestamps were not relabelled as a later rerun. Index commit `2665381157f1886b51f02696db49e2f9e7db5f1b`; capability commit `a5b2a7d5b9721af900bc662e1be995822f4861aa`; F4 build `a05cbc3348cb5a7860a2284cb11f8dbedcf34735`.

Final §10 release record passes all eleven views and four engine accessibility-tree checks. All four final local demo cold starts and both controls pass with zero failed requests/errors; forced failures and retry also pass. No real Safari, iPhone or screen reader was used. The two earlier cold readers remain applicable: all 58 final claim-block texts are unchanged, and final placements independently pass. This is not a fabricated new cold read. Human cold read remains optional under D7.

Typical reproduction (project-local tool/cache paths and credential-stripped test process):

```sh
uv sync --locked --dev
uv run python scripts/build_wasm_payload.py
uv run pytest -q
uv run pytest tests/test_10_cqr_order_statistic.py tests/test_22_wasm_equivalence.py -q
make verify
make lint-publication
uv run python scripts/mlflow_export.py --check
uv run python scripts/mlflow_publish.py --dry-run
uv run python scripts/rebuild_presentation.py
git status --porcelain=v1
python3 scripts/publication_guard.py tree
uv run python scripts/verify_mlflow_mirror.py verify --target public --out .local/tmp/pres-1/mirror-recheck.json
```

Do not repeat F1 as an incidental verification command. Its one successful invocation is already preserved.

## Approvals, effort, disk and network

Owner D1 approval: **2026-09-25**, following the named editorial corrections, byline approval and the Owner's unnamed-device observation. Standard ratification and D1–D7 outcomes: **2026-09-28**, including full conformance scope, F1 after independent PASS, final visual delegation to Orchestrator, automated Chrome/WebKit checks in place of real devices/VoiceOver, and optional human cold read. The notebook/claims/card-builder allowlist extensions and latest authentication correction/resumption are recorded in `owner-decisions.md`. No approval is inferred from a green test.

Current credential-correction/F1–F4 continuation: approximately **1.5 hours**, rounded to half an hour, including overlapping independent review. The previous stopped resumption was approximately 0.5 hour. The earlier sessions' cumulative active-hour ledger is unavailable in durable supplied material; commit timestamps do not distinguish active work from Owner waiting. No invented total or certified historical 80-hour-ceiling claim is made. This retained accounting limitation does not change the 60-hour estimate / 80-active-hour ceiling, and no later checkpoint was begun.

Disk at return: **approximately 3.77 GiB across the measured retained directories: PRES-1 worktrees 1,162,320 KiB; PRES-1 scratch 453,092 KiB; presentation screenshots 441,264 KiB; shared uv cache 864,972 KiB; shared local tools 1,029,348 KiB (measured after removing check-6; final return/diff files add a small amount)**. Totals include inherited material; no initial shared-cache baseline exists, so this is measured occupancy rather than a certified cumulative added-disk debit. New CI/review worktrees are removed after evidence preservation; all known task-created scratch/screenshots/caches are within project `.local/`. Retained logs/scripts/screenshots and recovery material are declared below. No paid service, new dependency or research execution was introduced; expected external cost **$0**.

Public writes: exactly one authorized F1 publisher invocation, **2026-09-28 20:27:28–20:54:18 UTC**, under D5. It created experiment `delu-generations` (ID 1) and 23 runs, with **710 counted logical operations plus 23 run-termination calls** omitted from the publisher's counter. The counter is not a complete transport-level HTTP count. Methods cover experiment tags, run data/params/tags/metric batches/datasets/artifacts, completion flags and status, all within that experiment. Upload record includes the exact authorization string and source commit. No public write probe, corruption/resume experiment, `delu-cp2` or registry write, Git publication, tag or redeploy. All subsequent remote calls were anonymous reads/POST searches. Historical loopback rehearsal writes remain separately recorded.

## Files changed, full diff and proposed commit

`changed-files.md` accounts for every file in the whole-checkpoint delta with a one-line reason, including every new/changed test. The continuation repairs `derived.py` (W3), the chapter renderer (W5), `mlflow_publish.py` (correct service precheck), their regression tests and generated outputs; then adds the actual public index/records and final verified surfaces. The earlier phases' source, claims, charts, demo, guards and runbook are part of the same checkpoint, not silently omitted from this return.

Full diff: `.local/tmp/pres-1/final-full.diff`; full stat: `.local/tmp/pres-1/final-diff-stat.txt`; reproducible with `git diff --binary main...<evidence_tip_sha>`. Working-tree status/stat/diff are empty. Proposed Owner-authored squash message: **`Publish the v1–v3 research presentation with registry-driven claims and verified MLflow routes`**.

## Open risk or exact owner action

No unresolved implementation or acceptance blocker. The remaining actions are the Orchestrator's verification and delegated F5 visual decision, followed by the Owner-controlled publication flow and F8. Device emulation, retained cold-reader applicability, historical effort/disk accounting and the forced-state tooling advisory are the limits explicitly recorded above. No credential change or new engineering authority is requested.

## Landing report and remaining authorized handoff

- Proposed disposition: **LAND**, after Orchestrator verification and delegated F5 visual approval. No LAND, merge, push, tag, branch deletion or redeploy was executed by this Lead.
- Evidence tip to preserve: full SHA in terminal handoff; every cited candidate SHA remains reachable on `gauntlet/pres-1`. The evidence tag is required before any later branch reclamation; a squash landing alone does not preserve the candidate chain.
- Branch: inherited `gauntlet/pres-1`, purpose PRES-1, clean final tip as above, 59 ahead / 3 behind main. No new branch or tag in this continuation. Main remains at the original SHA.
- Worktrees: inherited `lead` remains. Earlier interrupted `check-3` and fresh `check-4` were checked clean and removed in the previous resumption; scratch retained. This continuation created and removed `ci-7`, `check-5`, `ci-8`, and `check-6` under `.local/worktrees/pres-1/`, each detached at its recorded test/review SHA. Historical `check-1`, `check-2`, `ci-1` through `ci-6` were already absent. No unrelated worktree was removed. Only main and lead remain registered.
- Retained recovery: `.local/tmp/pres-1/` (prior drafts/rehearsal snapshots, interrupted-review recovery, current scripts/logs/diffs and independent audit files), `.local/artifacts/presentation/` (screenshots), shared `.local/cache/uv` and `.local/tools/`. These are recovery/reproduction material, not the sole copy of required verdicts/decisions/check results. Disposable active CI/review checkouts were removed; local test servers were stopped.
- Live branch references within permitted file scope: this return; the conformance brief evidence copy; `docs/track-b/pres-1-brief-2026-09-24.md`. Earlier preserved editorial/return records carry historical references and remain historical evidence. The Orchestrator owns program-state inventory/repointing; no locked document is changed by a generic cleanup instruction.
- Space bundle for redeploy: **b046c69b899bb9d5a2b2f9aeb3e5b3eebfdda820a419137ef5cdf8b8ac8f7c3d**, **805 files / 44,162,180 bytes**, Python 3.13.15 build; directory `.local/worktrees/pres-1/lead/dist/space-wasm` relative to project root. Exact command from `docs/deploy.md`, for the authorized publisher from the accepted checkout, **not executed here**: `hf upload Yarden-Viktor/delu-day-ahead-forecast dist/space-wasm . --repo-type space`.
- Remaining actions: Orchestrator independently verifies SHAs/evidence-only delta, clean two-version checks, its own final screenshots/placements, routes and bundle; gives the delegated F5 visual decision; follows the Owner-controlled Git/publication flow and runs F8. This return grants no new publication authority and does not close branch lifecycle/reclamation.

### F8 commands after the authorized publication

These are handoff commands, not completed deployment checks. Use the accepted checkout and actual release date for output names:

```sh
curl --fail --silent --show-error https://hrsi56.github.io/delu-day-ahead-forecast/ -o .local/tmp/pres-1/pages-deployed.html
cmp docs/index.html .local/tmp/pres-1/pages-deployed.html
PLAYWRIGHT_BROWSERS_PATH=/Users/djourno/Downloads/PJM/.local/tools/playwright/browsers /Users/djourno/Downloads/PJM/.local/tools/playwright/bin/python scripts/check_reader_paths.py demo --engine chrome --engine webkit --viewport 1440x900 --viewport 390x844 --url https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/ --out reports/presentation/release-checks/postdeploy-demo.json
uv run python scripts/verify_mlflow_mirror.py verify --target public --out reports/presentation/release-checks/postdeploy-mlflow-mirror.json
PLAYWRIGHT_BROWSERS_PATH=/Users/djourno/Downloads/PJM/.local/tools/playwright/browsers /Users/djourno/Downloads/PJM/.local/tools/playwright/bin/python scripts/check_reader_paths.py mlflow-routes --mirror-record reports/presentation/release-checks/postdeploy-mlflow-mirror.json --shots /Users/djourno/Downloads/PJM/.local/artifacts/presentation/postdeploy-mlflow --out reports/presentation/release-checks/postdeploy-mlflow-routes.json
uv run python scripts/check_links.py
```

Inspect each result: demo readiness alone is insufficient; both controls/inference, failures/errors and identity must agree. Every advertised MLflow route must show its intended content anonymously; comparison charts must settle. Compare deployed Pages bytes with the accepted artifact, not an unrelated fresh build.

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

The advisory log retains A-PRES1-1 through A-PRES1-18: identity-bearing artifact digests, private WebKit accessibility API, font packaging, narrow placement margins, registry/card tooling, MLflow code labels, and cold-reader questions about headline pairing, the eight-policy count, comparison populations, terminology, median/interval behavior, protected precision, archive vocabulary, preview identity, runtime requests and interval-score levels. These are advisory where no active clause is violated; all blocking review findings were repaired and freshly reviewed. The final Critic adds only an advisory about Playwright request-cancellation warnings during deliberately forced failure-state teardown; every state assertion passes and ordinary cold starts have zero errors. No blocking finding remains.

Interview-capture triggers (Orchestrator only; no DOCX entry filed here):

- Why does a date-based policy census survive row reordering while an incremental CSV count does not?
- Why did an account-API 403 reject a valid MLflow Basic pair, and how did a service-specific read resolve the diagnosis without changing credentials?
- How did we preserve all research values while centralizing identities, and why did name-bearing artifact hashes need a content-preservation proof?
- Why did green route names/IDs need an additional check that the actual comparison chart finished loading?
- How did the project obtain native WebKit accessibility evidence and fix fonts requested from shadow-root paths?
- What separates development improvement, a target verdict, a successful mirror upload and permission to replace the released demo?

## Post-return reads

After the written final Integration PASS, task-list/archive metadata and the recent metadata of the PJM review task were read solely to identify the Orchestrator handoff destination (`Set Orchestrator role`, task `01a0cb25-849b-73a0-afd0-850dba59cbcd`); no program-state, syllabus, Track A/C or Orchestrator-role file was read, and no engineering decision was informed by this lookup.

No later checkpoint was opened or planned. This terminal return ends the Engineering Lead's PRES-1 work.
