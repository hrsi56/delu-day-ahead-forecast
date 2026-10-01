# Track B Checkpoint Brief — PRES-3 (publication of v4, CP-21's adopted generation)

*Issued by the Orchestrator on 2026-09-30 (Wednesday), about 22:15 Asia/Jerusalem. It supersedes
an earlier draft of the same day that was never issued.*

## Target
- **Repository:** DE-LU day-ahead forecasting, `/Users/djourno/Downloads/PJM` (origin
  `hrsi56/delu-day-ahead-forecast`).
- **Authorized checkpoint:** PRES-3, exactly one.
  - It publishes CP-21's adopted generation, v4, on every public surface.
  - It corrects the public planned-work list after the Owner's withdrawal of TabPFN.
  - This is presentation work only. It reopens neither CP-21 nor PRES-1 or PRES-2. It starts no
    research checkpoint, final-product designation or Live.
- **Ratified publication anchor:** `docs/PUBLISH_RULES.md`, revision 1.2, SHA-256
  `a43ac02021b7de468e02db30b61ec73f86cdafa69df845cf084ab196528bb15b`.
  - It incorporates Publication Standard v1
    (`01d721c2ba6316ca9a2f707e79da229bef732e91bad22f6ce457fb01e69478cc`) and presentation plan
    revision 3 (`281193740a256a99a1676d53ef61c9babb5f744a7d0fb038927e305d1149812c`).
  - Apply its precedence and amendments A1–A6.
  - A7, A8 and A9 are not triggered: there is no final-product designation, rollout or live
    panel. By its §17, the 1.2 entry, PRES-3's obligations under 1.2 equal those under 1.1.
- **Research constraint anchor, read-only:** `capstone_v21.md` v21-r8, SHA-256
  `81d6127197cabf344f56c2cf25ef5fc8f9fdb2860e249c294177471d3130c182`. Its historical §§1–18 are
  byte-identical to the revisions that introduced them.
  - **§17.6** (what adoption means; naming) and **§17.9** (the publication packet and MLflow)
    govern CP-21's content.
    - CP-21 ran under v21-r6, whose exact bytes are at `evidence/cp-21:capstone_v21.md`
      (`ee402c4703d176f8181ed82966c978ad84c3c73a0cdb1d3567871f58bc867344`).
    - §17.9 pins PUBLISH_RULES 1.1 for CP-21's own packet. This block publishes under 1.2, as
      stated above.
  - **§18.1 and §18.5.** TabPFN is withdrawn. §18.5 assigns the correction of the public planned
    item "4.6 · DDNN / TabPFN" to "the next authorized publication block"; PRES-3 is that block.
  - **§16 and §19** (the final product and its Space) are not triggered.

  This brief activates no research checkpoint.
- **Execution inputs.** Verify each hash before relying on it:
  - CP-21's publication packet `docs/track-b/evidence/cp-21/publication-packet.md`,
    `b5ffceee4df9d09f7d12c106d3fa34ba5e84629fb7856b31998a69660a3b075c`;
  - the publication runbook `docs/track-b/publication-runbook.md`,
    `b5d0000824cb61cc9eae92729a2ad8c24e3f5dd4798e09ff38d76731fba8c931`;
  - the packet template `docs/track-b/publication-packet-template.md`,
    `4efb01855ae2d9a6f54b5624607a93046b1fffa881e34af0c6798c513c7829cf`;
  - the CP-21 publication plan `docs/track-b/cp-21-publication-plan-2026-09-29.md`,
    `c0ac0d2640c9375046bf235f5839e078b2504d7655d4b89cd97d9ea3d9c47198`.
    - This brief adopts its §4 (outcome A), §6 (every surface) and §7 (sequence) as scope. It is
      not otherwise an authority.
    - Where it names PUBLISH_RULES 1.1 or v21-r6, read the identities above.
  - the CP-21 landing record `docs/track-b/cp-21-landing-2026-09-30.md`,
    `569b471b926eace935b3b76290666f69d8650a6092ec58d755195a69260f9aed`. It is the source of v4's
    adoption date, 2026-09-30.
  - CP-21's return `docs/track-b/evidence/cp-21/checkpoint-return.md`
    (`566841e6dc22e26e1fd92a803da4741c90a128cfbed38c601987d673b9fde7f3`) and verdict
    `docs/track-b/evidence/cp-21/integration.md`
    (`7461548f51c82e62d08516e0fba12a9e8388b013a78c5cda8f60b7fc33b1a5c1`);
  - the publication advisory log `docs/track-b/publication-advisory-log.md`
    (`d1cb5309e43e3801bf1409016ddbd216279d92c2ed9ec9d48904439a9f59702f`), and PRES-2's
    recommendations R1–R7, listed after the table in `docs/track-b/evidence/pres-2/integration.md`
    (`7109f78453c9286b5f1ada5726ba75b277d53c008fb65079e0a759edc902c78e`).

## Orchestrator-reported expected state
- **Branch / commit:**
  - `main` = `origin/main` = `17f354e42c0d6f3199227fe9d29df9f4dc8211e0`, whose last five commits
    are `17f354e`, `c352436`, `6f4575b`, `632d0e6` and `c9dc364`.
    - `main` may instead be one direct child of `17f354e` that changes only `progress.md`: the
      Owner may commit the Orchestrator's record of this issue before launching you.
    - CP-21's squash landing is `4e37cf7926c87744188b679cef5a7d29e9ef6499` (`land/cp-21`).
    - `evidence/cp-21` = `1d13f99b1ab12f64719b439d0a9d4703bc7e1bdb`, committed
      2026-09-30 03:57 +0300.
  - Local branches: `main` only. There is no `gauntlet/*` branch, no worktree besides the primary
    checkout and no stash.
  - On `origin`: the branch `main` only, with every `land/*`, `evidence/*` and `archive/*` tag
    (read with `git ls-remote` on 2026-09-30).
  - `core.hooksPath` is `/Users/djourno/Downloads/PJM/.githooks`, so the secret guard is enabled.
- **Working tree:**
  - The primary checkout may carry one uncommitted Orchestrator change, `progress.md`, recording
    this brief's issue. It is not PRES-3's: leave it untouched, and do not read it (`AGENTS.md`
    role router).
  - Your ignored folder `.local/artifacts/pres-3/` holds this brief's canonical copy,
    `issued-brief.md`, and its launch envelope.
  - Its subfolder `superseded-draft-2026-09-30/` holds an earlier, never-issued draft pinned to
    superseded anchors. It is not an input; do not use it.
- **What already exists:**
  - CP-21's committed evidence, under `reports/block-challenger/` and
    `docs/track-b/evidence/cp-21/`. It includes:
    - `reports/block-challenger/draft-registry.json`;
    - the claim map `docs/track-b/research-content/cp21-claims.md`
      (`8df2e9a5c0edd160c4c0d6536c40eb1b0fee248db890a65da58abe4c3ec37c43`);
    - the draft export `reports/block-challenger/mlflow-export-draft/cp21.json`
      (`0f23d52dec3c3d4a413cfe15d959f8dd134d706d240d24f4d5889e0847ef5603`), with its pending
      fields listed in packet §6.
  - The local MLflow store `.local/mlruns/cp21`, which reads back equal to the draft.
  - CP-21's retained local material in `.local/artifacts/cp-21/`.
  - The registry, page, README and Space generators as PRES-2 left them.
  - The published export set `reports/presentation/mlflow-export/`: 23 runs in
    `delu-generations`, six routes.
  - A copy of PRES-2's reviewed Space bundle at `.local/artifacts/pres-2/space-wasm-8007f0d2/`.
- **Public state,** read anonymously by the Orchestrator on 2026-09-30 at about 22:10
  Asia/Jerusalem:
  - **GitHub Pages** serves the PRES-2 page: HTTP 200, 1,684,252 bytes, SHA-256
    `f36314e28811ed4b7ec41bc73dfd481ddb112815effabfc4e7b3ae74d8edab1d`, equal to
    `docs/index.html` at `17f354e`.
    - It shows v3 as the research headline.
    - Its "Planned, not evaluated" list still carries "4.6 · DDNN / TabPFN" ("Does a
      distributional network, or a tabular foundation model, beat v3?") and "4.5 · Three-block
      LightGBM".
  - **The Space** `Yarden-Viktor/delu-day-ahead-forecast` is at revision
    `0c550e863711e19abbb35219cf64d45dfb39c888`: static, public, RUNNING, 806 files.
    - 805 of them are PRES-2's reviewed bundle,
      `8007f0d2a9c09a8c2c3182745dac6b38956a9a0ad8f58541f32472b674d5bb4e` (44,164,910 bytes).
    - The remote files absent from that bundle are exactly `{style.css}`, the unused leftover.
  - **MLflow on DagsHub** (`delu-generations`): the 23-run, six-route export was last verified
    during PRES-2 and was not re-read for this brief. No `cp21` run is public.
- Verify all of this yourself before relying on it, and report any material mismatch.

## Observable outcome
v4 is published on every surface, completely or not at all. When this checkpoint closes, after
the Owner's post-return steps:

- **The registry.**
  - It names v4 **"v4 · three-block LightGBM added"**. The Owner confirmed this name on
    2026-09-30.
  - v4 is adopted in research on 2026-09-30, with the CP-21 landing record as its source.
  - v3 is both v4's predecessor and its comparator.
  - L-P, L-R and L-N are study arms, not adopted.
- **The headline and opening.** The research headline moves to v4 through the registry. It names
  its metrics (A1) and leads with the pre-specified verdict. The opening pairs research v4 with
  released v1.
- **The chapter.** A v4 chapter, and the A3 transition "From v3 to v4: adding a three-block
  LightGBM". Visible in them:
  - the ladder, with the disclosure that its first step bundles weather with capacity selection
    (C106);
  - the block-split finding, exactly as C111 reads it;
  - the peak finding C120: on the 17-day August 2022 peak, v4's point error is higher than
    v3's. It is shown, not hidden or softened.
- **The planned-work list is corrected** for v21-r7 §18 and for CP-21's result.
  - **4.6 is DDNN alone.** No surface carries TabPFN or "tabular foundation model" in the item,
    its question or its code label.
    - Its question names v4 as the comparator ("same information, same opponent", amended by
      the Owner on 2026-09-30).
    - It does not commit to a candidate design that no anchor has fixed yet, such as a
      standalone DDNN or a blend member.
  - **4.5 leaves the planned list.** CP-21 evaluated it; it is now the v4 chapter.
  - The other planned items keep their content. The section's comparator follows the registry.
  - The claim guard W14 stays as it is; v21-r7 left it unchanged on purpose.
- **Derived surfaces.** The README, both Space cards and the MLflow export follow from the
  registry. The demo still runs the released v1 artifact, and the bitwise-equivalence gate
  passes.
- **MLflow.** `cp21` is uploaded under the authority below, then verified, routed (`experiment`,
  `compare:v4`) and indexed, all before the final build.
- **Space deployment tooling.** `scripts/deploy_space.py` can deploy the reviewed bundle and
  remove every remote file the bundle does not carry, today exactly `style.css`. It then verifies
  that the served file set equals the bundle, file by file. It is tested offline; only the Owner
  uses it, after the return.
- **Review.** The independent check passes at the candidate, and a focused recheck passes at the
  final SHA.
- **The owner packet.** Packet §8 names the exact payloads and ready-to-run commands for the
  remaining steps: the landing, the push, the Space deployment and the public post-deployment
  checks.

The publication is complete only after those steps and their public evidence. A local PASS is not
a deployed publication.

## Complete authoritative checkpoint bar
- **PUBLISH_RULES 1.2 in full.** Every applicable clause, including the incorporated baseline,
  A1–A6 and §13's acceptance record. Record A7, A8 and A9 as not applicable, with the reason.
- **The runbook:**
  - §2, all touchpoints 1–18, 12a included, with "What follows without an edit" and "Limits to
    watch";
  - §1, §1a, §8 and §9.
- **The packet template, every section.** Complete CP-21's packet into PRES-3's, with §8 filled
  for every surface.
- **The publication plan, as scope:**
  - §4's table and its "in both outcomes" statements;
  - §6's surface table and its `style.css` paragraph;
  - §7's sequence.
- **v21-r8 §18.5's planned-item correction,** as the Observable outcome states it.
- **Critic and return:** `docs/track-b/gauntlet-templates.md` §§2–3. This is not a research
  checklist, and it authorizes no fit.

Map every applicable item to evidence. The extract below does not narrow this bar.

## Task-specific supporting extract
1. **Registry** (runbook §2 steps 1–6).
   - Enter packet §2's draft entries exactly as drafted, with statuses dated 2026-09-30 and
     sourced from the landing record.
   - Add packet §2's proposed code additions to existing entries, unless an addition would
     change a previously published MLflow record. v21-r6 §17.9's "must change no previously
     published record" wins: leave such an addition out and record it in the packet and the
     return.
   - `CHECKPOINTS` gains CP-21: run key `cp21`, the evidence tag and SHA, the report, the
     verdict, the landing record and the children.
   - `EVIDENCE_TAGS` gains `evidence/cp-21` with the tip's commit date, as for earlier tags.
   - `RULES` gains `cp21-adoption`, set 2026-09-29.
   - `COMPARISON_ORDER` puts v4 first. `CRISIS_ORDER` changes only if v4's chapter shows the
     crisis window.
2. **Evidence** (steps 7–10). Pin CP-21's committed rows by blob. Derive every value, and type
   none:
   - the verdict, the distance from v3, and N = 1;
   - the ratio intervals, from CP-21's own draws (seed 15042, 2,000 replicates, 7-day blocks);
   - per-period MAE, with fold 3 as the stress period.
3. **Claims and slots** (steps 11–12a). Register the claim map and the `v4.*` and
   `transition.v3-v4.*` blocks from packet §5 and §5a.
   - The method detail states the ladder B3 → L-P → L-R → HGL. It discloses that B3 → L-P
     bundles weather with capacity selection and the missing-input rule (C106, W23).
   - The block-split finding appears exactly as C111 reads it (W22).
   - The peak finding C120 appears in the stress-period detail.
   - The withheld claims W1–W27 stay withheld.
4. **Chapter and charts** (steps 13–15). Write a `v4_slots` builder, modelled on `v3_slots`, and
   register it in `chapter_sequence`. Its detail headings feed A5's routes. Add the charts its
   MLflow run carries.
5. **Encoding** (step 16). The Owner decided it on 2026-09-29 (D6): amber `#B45309`, a filled
   diamond marker and the direct label "v4". No further Owner input is needed. The Owner's own
   visual review before the push is separate from the independent check.
6. **Planned work.** Correct `scripts/build_pages.py::PLANNED_WORK` to the Observable outcome and
   regenerate. Bind the correction with a regression test and a negative control over every
   generated public surface: the page, the README's generated blocks and both Space cards.
7. **Export and tests** (steps 17–18).
   - Add the CP-21 export specification.
   - The regenerated `cp21.json` must equal the draft except for packet §6's pending fields.
     The name is unchanged, so no name field may differ.
   - No previously published record may change: run `--diff-against` the published set, and
     `--check`.
   - Add re-derivation tests with negative controls. Extend
     `tests/test_43_publish_rules_migration.py` with the v4 transition.
8. **Space.**
   - Regenerate both cards. If the card or the bundle changes, rebuild with `make wasm`. The demo
     must serve the same v1 artifact, with the bitwise-equivalence gate passing.
   - Record the reviewed bundle's hash and its complete file list.
   - `scripts/deploy_space.py` now deletes no remote file. Extend it:
     - An upload commits the reviewed bundle and deletes every remote file the bundle does not
       carry, in one Hub commit, or fails closed.
     - Check mode lists that deletion set without changing anything.
     - Upload mode refuses unless the actual deletion set equals the set the Owner passes on the
       command line.
     - A deletion-only commit is possible when the reviewed bundle already equals the served
       files apart from the deletions.
     - After the commit, it verifies that the served file set equals the bundle, by path and
       per-file hash, and writes its record.
   - Test it offline with negative controls: an extra remote file, a missing file, a changed file
     and an unexpected deletion set. It makes no write to the Hub during this checkpoint.
9. **Limits.**
   - A2's placement bounds: 1,744 px at 1,440 × 900 and 2,420 px at 390 × 844, measured in Chrome
     and WebKit.
   - The 2.0 MB page budget; the page is 1.68 MB now. If v4 would breach it, return BLOCKED with
     the measured size. The compaction rule is the Owner's decision (runbook §2).
   - Chart text of at least 12 px at every width.
10. **Advisories.** Give each of PRES-2's R1–R7 a one-line disposition in the advisory log:
    taken up in PRES-3, or deferred with the reason. They are recommendations, not bars.

## Applicable constraints
- **No research.** $0 external spend. No research rerun, fit, new score, bootstrap, data
  retrieval or typed number. Nothing dated after 2026-04-07 is read, scored or shown. CP-21's
  reference and bootstrap passes are exhausted at 3/3.
- **The product is unchanged.**
  - No change to the released product, the demo's model, the product documentation (A4) or the
    release rule; v1 stays released.
  - No promotion, final-product designation, CP-17 freeze, Live or daily operation.
- **History is preserved.**
  - Keep every historical chapter, archive, adverse fact, prior review and published MLflow
    record.
  - PRES-1 and PRES-2 are not regraded.
  - Historical records that name TabPFN stay as written (v21-r8 §18.5).
- **Generated files are regenerated from their sources** (`scripts/rebuild_presentation.py`,
  `make wasm`), never hand-edited.
- **Not edit targets:** `main`, `progress.md`, and the whole locked set of `AGENTS.md`'s Governance
  Lockdown: the rulebook, every ratified anchor including `capstone_v21.md` and
  `docs/PUBLISH_RULES.md`, the amendment records and `.claude/**`. The runbook and the packet
  template are pinned inputs, not edit targets. No Lockdown suspension is active. If a change to
  any of these is genuinely necessary, halt and return BLOCKED, naming the file and the exact
  text.
- **Paths.**
  - Temporary worktrees, tools, caches and screenshots go under `.local/`.
  - Durable evidence goes under `docs/track-b/evidence/pres-3/` and
    `reports/presentation/release-checks/pres-3-*`.
  - Code and tests go in their normal paths.
- **Credentials** follow `AGENTS.md` § Credentials.
  - Consume stored variables only inside the process that needs them. Never print, type or log a
    value. Anonymous reads stay anonymous.
  - Before anything imports MLflow, including the test suite, export
    `MLFLOW_DISABLE_TELEMETRY=true` and `DO_NOT_TRACK=true`.
  - The secret guard is mandatory; never use `--no-verify`.
  - Before any commit that carries logs or evidence, scan the outgoing content for the actual
    values of the stored credentials, in a script that never prints them. A pytest traceback
    once published the DagsHub token.
- **Calendar.**
  - Nothing runs from Friday 00:00 to Sunday 00:00, Asia/Jerusalem: no background job and no
    MLflow upload.
  - If that window arrives mid-run, stop at a coherent boundary with no process running, and
    wait. The Owner resumes this session afterwards, and the pause does not count against the
    timebox.

## Reviews and evidence
- **Before the independent check,** run the runbook §9 checks:
  - the tests on Python 3.13, and a clean 3.12 run of every step of the CI workflow;
  - `make verify`, `make lint-publication` and `make publication-guard`;
  - determinism and links;
  - Chrome and WebKit at every width, with accessibility, keyboard, touch, contrast, requests and
    the placements;
  - A5 discovery, and the demo's controls.
- **One editorial review** against the standard.
- **A fresh reader.** A separate, context-free agent receives only closed-state screenshots and
  the six unchanged questions of PUBLISH_RULES §10.2. Save its original answers.
- **The independent check is mandatory.** PRES-2's waiver was a one-time exception.
  - One fresh Integration Critic, which authored none of the changes, reviews the work.
  - It works in a clean detached checkout at the candidate SHA, with only the prescribed inputs.
- **After the MLflow upload, the index and the `--final` build,** obtain an exact-SHA focused
  recheck on the final SHA.
  - It confirms that the delta from the independently checked candidate holds only the index and
    the final-build outputs, and that the checks those files affect pass again.
  - The binding verdict, `docs/track-b/evidence/pres-3/integration.md`, cites that final SHA as
    `final_candidate_sha`.
  - The delta to the evidence tip is verdict-only.
- **Retain first failures and retries.** A local result never stands in for public evidence.

## Timebox
Approximately 24 hours, orientation through terminal return, excluding any Friday–Saturday pause.
Report elapsed time to the nearest half hour. Crossing it is a scope check, not an automatic stop.

## Owner-only actions already authorized
The Owner's delivery of this brief authorizes the local checkpoint on `gauntlet/pres-3`. It also
authorizes exactly one external action, by the Owner's decision of 2026-09-30: **the MLflow upload
of runbook §1 step 5.**

- **When:** only after the independent check has passed at the candidate SHA, and outside the
  Friday–Saturday window.
- **What:** exactly the regenerated `cp21` export that the check reviewed: parent `cp21` and
  children `cp21/HGL`, `cp21/L-P`, `cp21/L-R` and `cp21/L-N`, into the experiment
  `delu-generations` on DagsHub.
- **How:** upload with `scripts/mlflow_publish.py`. Then run the mirror verification, the route
  checks (REST and browser) and the index.
- **Credentials:** the stored DagsHub variables, read inside the uploading process only.
- **Limits:**
  - No other MLflow write: no change to a published run, no registered model, no new experiment
    and no deletion.
  - If the tool would write anything else, stop before writing and return BLOCKED with the exact
    operation.
- **Failures:**
  - Retain a first failure, and retry within the service's limits.
  - If the upload cannot complete, return BLOCKED with the exact remaining operation.
  - Report a partial upload as partial, with the run IDs that exist.

Nothing else is authorized:

- no commit on `main`, landing, merge, push or tag push;
- no Pages deployment, Space upload or remote deletion (the deploy tooling is built and tested
  offline only);
- no governance edit.

Each of those is the Owner's, on a later explicit instruction.

## Stop and return
Return exactly one of PASS / BLOCKED / INCOMPLETE, using `docs/track-b/gauntlet-templates.md`
§3.

- **First commit.** The first commit on `gauntlet/pres-3` copies this brief byte for byte, from
  `.local/artifacts/pres-3/issued-brief.md` to `docs/track-b/evidence/pres-3/issued-brief.md`.
- **The return form.** Return with the complete §3 form, the completed publication packet and its
  applicability matrix.
- **BLOCKED at the external gate.** When all authorized work is complete and only the Owner's
  steps remain, return BLOCKED at that gate. State the local readiness, the MLflow upload's
  verified state and the binding Integration PASS. This is not a product FAIL.
- **Identities and accounting.**
  - Name `final_candidate_sha` and `evidence_tip_sha`, and show their verdict-only diff.
  - Identify the page, bundle and export hashes, the bundle's complete file list and the
    expected Space deletion set.
  - List every changed file and every check.
  - Account for every branch, worktree and ref.
- **The owner packet.** Supply a concrete packet for the remaining steps.
  - Every command must be non-interactive: `git --no-pager …`, and `git commit -F <message file>`
    with the message file written under `.local/artifacts/pres-3/`. No pager and no editor.
  - Give each command's expected output.

  The steps:
  1. **The LAND.**
     - First, check that `main`'s checkout holds no untracked copy of a file the branch adds.
     - Then `git merge --squash gauntlet/pres-3`, a check that the staged tree equals the
       evidence-tip tree, and `git commit -F`.
     - Then the tags: `land/pres-3` on the squash commit and `evidence/pres-3` on the evidence
       tip.
  2. **The push** of `main` and both tags, preceded by the value-based secret scan.
  3. **The Space upload** of the reviewed bundle hash with the extended `scripts/deploy_space.py`.
     - It deletes exactly the stated set (today `style.css`), then verifies that the served file
       set equals the bundle.
     - If the bundle is unchanged, the step is the deletion-only commit with the same
       verification.
  4. **The A6 post-deployment checks** for each surface: Pages, the README, MLflow, the Space card
     and the direct demo. They include an independent public review by a checker that wrote none
     of the changes, and keep first failures and retries.
  5. **The receipt.** The packet §8 fields each step fills, and the closure record's inputs.
- **Interview-answer triggers.** Name any in one line each (`AGENTS.md` § Interview-answer
  capture); file nothing.
- **Do not** land, merge, stage or commit on `main`, push, deploy, or begin another checkpoint.
