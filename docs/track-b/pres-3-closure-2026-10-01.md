# PRES-3 closure — 2026-10-01

**PRES-3 is closed. v4, "v4 · three-block LightGBM added", is published on every surface: the
report, the README, MLflow and the Space. v1 remains the released product and the demo.** The
independent post-deployment review was waived by the Owner for PRES-3 only. It did not pass, and
it is not certified.

## Identities

| Item | Value |
|---|---|
| Brief | `docs/track-b/evidence/pres-3/issued-brief.md`, SHA-256 `57a8c7fbc1b9b0d3c268e4af95a02a4a75276dda8224a24a6b1119ac03b773d7`, issued 2026-09-30 |
| Pinned rules | PUBLISH_RULES 1.2 `a43ac02021b7de468e02db30b61ec73f86cdafa69df845cf084ab196528bb15b`; research constraint anchor `capstone_v21.md` v21-r8 `81d6127197cabf344f56c2cf25ef5fc8f9fdb2860e249c294177471d3130c182` |
| Starting `main` | `17f354e42c0d6f3199227fe9d29df9f4dc8211e0` |
| Independently checked candidate | `747d2bbc9336758ce4a26d12a5d9ddb35d46e72a` |
| Final candidate (the Integration PASS binds here) | `4ad7d09f5b9405f09b633326979890e9fa9180ca` |
| Evidence tip / `evidence/pres-3` | `42a4bb4589157fa0241ea03c693d07b527bf040c` |
| Squash landing / `land/pres-3` | `f6dabfa69936d0b4071820e5b6a10ac055477fd4`, with the single parent `17f354e` |
| Page | `docs/index.html`, SHA-256 `97e1d86203a766534045a57a6616269982a7730756f6a0a96965497be92b9530`, 1,907,451 bytes |
| README | SHA-256 `09e7dc664a96444d14fc137f25b1c2cb67160052278bfcefdb985ff853c10c91` |
| Space bundle | `9028a11869a378ea5c3401a00ad46368e1c9e2f2f9f8732330d32b71af081585`: 805 files, 44,164,910 bytes |
| Space revision | `0331088725fedab2f5a1ec804ae03bf960cf126f` (before: `0c550e863711e19abbb35219cf64d45dfb39c888`) |
| MLflow runs | `cp21` `bc152519f4cc4c3abada756a67e9ad89`, `cp21/HGL` `d7c53e9d7db94ed48d91da14be2d343b`, `cp21/L-P` `c9b0216014dd48ed8d02939f9f88b458`, `cp21/L-R` `cbdb4a2a7b8e47a78c7bc1feeb9aa8eb`, `cp21/L-N` `2990b1081ea943c584548dc4a5190ad7` |

## The return and its receipt

- **The Lead returned BLOCKED at the external gate on 2026-10-01**, about 9 hours after the
  brief, against a 24-hour timebox.
- **The Integration verdict is PASS.**
  - The full independent check ran at `747d2bb`; the focused recheck ran at `4ad7d09`.
  - The verdict is `docs/track-b/evidence/pres-3/integration.md`.
  - The editorial review's five violations and the fresh reader's one finding were repaired
    before the check.
- **The Orchestrator's receipt** (templates §4 and the role's enumerated checks):
  - `main..42a4bb4` is nine commits, and `main` was untouched;
  - `4ad7d09..42a4bb4` is the verdict file only;
  - `747d2bb..4ad7d09` holds the page, the build record, the MLflow index and three upload and
    verification records;
  - every cited SHA is reachable;
  - the packaged brief is byte-identical to the issued one;
  - none of the 56 changed paths is a locked or pinned governance file.
- **The one external action the brief authorized, the MLflow upload, stayed in scope.** The
  upload ran 2026-10-01 03:32–03:43 UTC. Its write plan named `cp21` and its four children only:
  5 runs were created, 23 published runs were skipped as complete, and no experiment tag was
  written.
- **A recorded difference from the brief's wording.** The final `cp21.json` carries eight chart
  artifacts on `cp21/HGL` beyond the draft's pending fields. This follows runbook §2 step 15, and
  the Critic judged it explicitly. The export changes no published record.
- **Disclosures accepted:**
  - the Owner's direction of 2026-10-01 on the comparison chart;
  - the Owner-approved reinstall of WebKit under `.local/tools/`;
  - packet §9.1's stale placement figures (R-1), corrected in the return: 1,702.6 / 1,703.3 px
    on desktop and 2,400.5 px on phone;
  - one MLflow import before the telemetry variables were set, which made no tracking call.

## The Owner's steps, as they happened

1. **LAND.** The Owner squash-landed `gauntlet/pres-3` by hand with the packet's non-interactive
   commands.
   - The commit is `f6dabfa`.
   - Its tree equals the evidence-tip tree.
   - The tags are lightweight: `land/pres-3` = `f6dabfa` and `evidence/pres-3` = `42a4bb4`.
2. **Push.**
   - The publication guard passed: "the tree carries no placeholder and a final build record".
   - The Owner pushed `main` and both tags.
   - `git ls-remote` reads `main` = `land/pres-3` = `f6dabfa` and `evidence/pres-3` = `42a4bb4`
     on origin.
3. **The Space.**
   - **A hand rebuild did not reproduce the reviewed bundle.** The packet's `make wasm`, run in
     the Owner's terminal, assembled 566 files with hash `247dbe94…`.
   - **The cause.**
     - `app/wasm_showcase.py` carries PEP 723 inline dependencies with `marimo` unpinned.
     - In an interactive terminal, `marimo export` asks whether to run in a sandbox. Its prompt
       goes to stderr, which `scripts/build_wasm_space.py::run_export` captures, so it is
       invisible, and the default is yes.
     - The export therefore ran with marimo 0.25.0 from a fresh isolated uv environment, created
       13:41:49 local time, instead of the locked 0.24.2.
     - The Lead's builds had no TTY, so marimo defaulted to no sandbox.
   - **The guard held.** The deploy script binds the reviewed hash with `--expect`, so it would
     have refused that bundle. The modified `reports/cp3b/space_wasm_bundle.json` was restored,
     and the diff is kept at `.local/artifacts/pres-3/owner-make-wasm-diff.txt`.
   - **The route taken.** The Owner deployed the exact reviewed copy,
     `.local/artifacts/pres-3/space-wasm-9028a118/`, at 10:45:49–10:45:57 UTC.
     - The Orchestrator's check mode first confirmed the plan: 9 changed booster files, no
       additions, and the deletion set `{style.css}` matching the declared one.
     - The deployment made one commit, `0331088`.
     - The result was `status` `deployed` and `verified` true, with no missing, extra or
       mismatched path. The record is `reports/presentation/release-checks/pres-3-space-deployment.json`.
   - **A misleading field.** The record's `served_equals_bundle: false` comes from the pre-commit
     plan on the old revision, not from the post-deployment verification.
4. **The A6 public checks.** The Orchestrator ran the packet's commands, read-only and anonymous,
   2026-10-01 10:46–11:09 UTC. Logs are in `.local/artifacts/pres-3/a6-logs/`.
5. **The independent public review was waived by the Owner,** for PRES-3 only: "Confirmed,
   proceed with closing PRES-3", after the Orchestrator's recommendation.
   - **The basis.** The served page, README and Space files are byte-identical to the reviewed
     final candidate. PUBLISH_RULES §10.1 checks unchanged material by byte identity. The
     content had an editorial review, a fresh reader, an independent Integration review and a
     focused recheck before deployment. The public behaviour was tested on the live services.
   - **What is given up.** No independent reader of the live surfaces checked hosting-only
     effects.
   - **It is the second consecutive waiver,** after PRES-2. A rule change, rather than another
     exception, is carried to the pending governance follow-up.

## Publication completion receipt (packet §8.1)

| Surface | Intended identity | Observed public identity and UTC time | Verification record and result | Outstanding |
|---|---|---|---|---|
| GitHub source / README | `f6dabfa`; README `09e7dc66…` | `origin/main` = `f6dabfa`, read 2026-10-01; the raw README's SHA-256 equals `09e7dc66…`, about 10:46 | `git ls-remote`; anonymous fetch | none |
| GitHub Pages | page `97e1d862…`, 1,907,451 bytes | HTTP 200, 1,907,451 bytes, SHA-256 `97e1d862…`, about 10:46 | `pres-3-public-report.json` (`ed4ecf15…`): passed in Chrome and WebKit at every width | none |
| Public MLflow | 28 runs including `cp21` and its four children; routes `experiment`, `compare:overview`, `compare:v4` and the earlier ones | 28/28 runs, 9,178 metric points, 7/7 routes by REST, 11:00–11:07 | `pres-3-public-mirror-postdeploy.json` (`62392f65…`) passed; `pres-3-public-mlflow-routes-postdeploy.json` (`16a8ec8c…`) passed in Chromium and WebKit | The experiment description still names four parents (A-PRES3-1) |
| Hugging Face Space card | `space-wasm/README.md` unchanged, `c92a2666…` | The served card's SHA-256 equals `c92a2666…`; the Space is static, public, RUNNING, at `0331088`, with 805 files and no `style.css` | Anonymous API and raw fetch | none |
| Hugging Face direct demo | bundle `9028a118…`, running v1 | Every served file equals the bundle by path and hash, verified at 10:45:57 | `pres-3-space-deployment.json` (`85be9772…`): verified. `pres-3-public-demo.json` (`7c243ded…`): a **first failure**, Chrome 1,440 × 900, timed out at 180 s on 20 HTTP 429 responses from Hugging Face; the other three runs were ready in 19.7–21.5 s. `pres-3-public-demo-retry-1.json` (`09912da2…`): the targeted retry at about 11:02 was ready in 18.9 s with no error. `pres-3-public-demo-a11y.json` (`692e0f96…`) passed. `pres-3-public-states.json` (`0ae9d85b…`): the failure, hang and asset-failure states and the recovery behaved as specified | none; the cold-visit 429 is a known service limitation |

- **Links:** `pres-3-public-links.json` (`7ba89d0d…`) records no failed destination. The 302s to
  DagsHub's login are the gated-path controls.
- **The 429** is a service-availability observation, not a product defect. It neither proves
  uninterrupted availability nor is erased by the retry.
- **Completion disposition:** complete on every surface, with one Owner waiver: the independent
  post-deployment review.

## Reclamation (templates §4)

- **Before deletion:**
  - `evidence/pres-3` reaches every cited commit (`f694510`, `4b64fd2`, `747d2bb`, `4ad7d09`,
    `42a4bb4`);
  - the branch had no commit outside the tag;
  - both tags were verified on origin.
- **Pre-reclamation copies** in `.local/artifacts/pres-3-landing-2026-10-01/`: a verified Git
  bundle of `17f354e..gauntlet/pres-3`, and worktree, branch and ref snapshots.
- **Removed:**
  - the worktree `.local/worktrees/pres-3/lead`, which was clean. Its 1.1 GB of ignored content
    was regenerable: `.venv`, `app/public`, `dist` and caches;
  - the branch `gauntlet/pres-3` (it was `42a4bb4`); the worktree records were pruned.
- **Already removed by the Lead:** the Builder, editorial, CI and Critic worktrees. The branch
  was never pushed.
- **Live citations.** `progress.md` is repointed in the same operation. The issued brief, the
  packet, the verdict and the return are hash-bound records of the run and keep their bytes.

| Historical reference | Current retrieval |
|---|---|
| `gauntlet/pres-3`, the reviewed chain | `evidence/pres-3` |
| Any branch commit | Unchanged SHA, reachable through `evidence/pres-3` |
| The squashed publication | `land/pres-3` |
| `.local/worktrees/pres-3/lead/<path>` | The same path in the primary checkout; exact bytes through `git show evidence/pres-3:<path>` |

## Retained local material

`.local/` is ignored by Git and is not an off-device backup.

| Path | Content |
|---|---|
| `.local/artifacts/pres-3/` (327 MB) | The issued brief and its envelope, the superseded draft, the return and the Owner's commands, the reviewed bundle copy `space-wasm-9028a118/`, release attempts, the fresh-reader material, the CI 3.12 runner, the A6 logs and screenshots, and the unused public-review brief |
| `.local/artifacts/pres-3-landing-2026-10-01/` | The branch bundle and ref snapshots |
| `.local/tools/ms-playwright/` (299 MB) | The project-local Playwright browsers (A-PRES3-4) |

## Carried forward

- **For the Owner (none blocks closure):**
  - A-PRES3-7: the GFS attribution wording, to apply at the next Space deployment;
  - A-PRES3-1: the MLflow experiment description, through a code pin and one authorized tag write
    in the next publication brief;
  - A-PRES3-5: the standard §15 note, in the governance follow-up.
- **Tooling** (A-PRES3-2, -3, -4 and -6), plus two found at closure:
  - the marimo sandbox: `run_export` must pass `--no-sandbox` and `stdin=DEVNULL`, or the notebook
    must pin marimo;
  - the `served_equals_bundle` field name.

  Until the first is fixed, a Space deployment uploads a reviewed bundle copy, never a hand
  rebuild.
- **Governance proposal:** require the independent post-deployment review only when the served
  bytes differ from the independently reviewed bytes or a public check fails. It needs the
  Owner's task-scoped Lockdown suspension.
- **Q&A:** three of the Lead's six named triggers are filed. The Orchestrator proposed filing three to save tokens, and the Owner accepted that with the closure.
  They cover the bundle hash and the marimo sandbox, the fresh reader against the editorial
  review, and the write-plan guard that left the MLflow description stale.

Record-level scientific claims are taken as the return and the binding verdict report them. No
experiment, fit or test was rerun for this closure.
