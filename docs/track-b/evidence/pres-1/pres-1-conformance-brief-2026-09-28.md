# PRES-1 conformance to Publication Standard v1: Engineering Lead brief

**Engineering Lead · PRES-1 · issued 2026-09-28 at the Owner's instruction.** The Owner carries this
brief to a **new** Engineering Lead session. It authorizes bounded execution under it.

- **Repository:** `/Users/djourno/Downloads/PJM`.
- **The session it replaces.** It supersedes the retired PRES-1 Lead session, which receives nothing
  further.
- **The release review of 2026-09-28** was never handed over. It is context only.

---

## 1. Target

- **The authorized checkpoint:** PRES-1, the presentation release of generations v1–v3. Its branch
  is `gauntlet/pres-1`.
- **The controlling specification:** the ratified
  [Publication Standard v1](publication-standard-v1.md) ("the standard").
  - [Plan revision 3](presentation-and-tracking-plan-2026-09-24.md) stays in force as the standard's
    §14 and §15 carry and amend it.
  - This brief adds authority, ceilings, the checks and the return.
- **Precedence.**
  - The standard governs presentation. The research anchors and the Owner's standing decisions
    govern research.
  - If the documents still disagree, stop and return BLOCKED, naming the clause. Do not
    reinterpret.

**The observable outcome.** The PRES-1 candidate is brought to **full conformance with every clause
of the standard in force** (its §16), "including everything", in the Owner's words. It is then taken
to a publication-ready state:

- the public MLflow mirror is uploaded and verified;
- the final page builds with real links and no placeholder;
- one independent PASS binds the final candidate;
- the return is written.

After your return, the only steps left are the Orchestrator's verification, its landing and push,
and its redeploy of the Space.

**Before any other work, verify:**

- **The standard's SHA-256:**
  `01d721c2ba6316ca9a2f707e79da229bef732e91bad22f6ce457fb01e69478cc`
- **The plan's SHA-256:**
  `281193740a256a99a1676d53ef61c9babb5f744a7d0fb038927e305d1149812c`
- **This brief's SHA-256:** given in the Owner's prompt.
- **The starting `main`:** record its SHA. It must contain this brief and the standard at the
  hashes above, be clean, and equal `origin/main`.
- **The candidate:** `gauntlet/pres-1` at `af0abb090ad3eba2888c3791ebe3cdcf28409a7f`, checked out and
  clean in `.local/worktrees/pres-1/lead`. If the branch, the worktree or the tree differs, stop and
  report it. Another session may have written there.

## 2. Read first

1. **Governance:**
   - `AGENTS.md` in full, including § Credentials, § Git and publication authority, and § Branch
     and ref lifecycle;
   - `engineering-role.md` in full;
   - `docs/track-b/gauntlet-templates.md` §2 (assignment and verdict) and §3 (return).
2. **The standard, in full.** For context only, its
   [derivation record](publication-standard-derivation-2026-09-28.md).
3. **Plan revision 3,** read together with the standard's §15:
   - §6 (invariants);
   - §7 (design specification; the visual tokens of §7.3 bind);
   - §8 (content);
   - §9 (the evidence layer);
   - §10 (MLflow);
   - §§11–12;
   - §16 (the Owner's decisions).
4. **The PRES-1 evidence on the branch, `docs/track-b/evidence/pres-1/`:**
   - the Owner's decisions;
   - both independent checks;
   - both reader-task records;
   - the Owner's two editorial reviews;
   - the audit matrix;
   - the hand checks;
   - the CI record.
5. **For context,** the superseded
   [release review](presentation-release-review-2026-09-28.md). Its findings are absorbed by the
   standard.
6. **`capstone_v21.md`, read-only:** §§6–8 (scores and criteria) and §§14–15.
7. **Evidence, read-only:**
   - `reports/{cp2,cp10,cp15,v2-causal,weather-ablation,weather-admission}/`;
   - `docs/track-b/research-content/`;
   - `docs/track-b/evidence/`;
   - `docs/deploy.md`.

**Engineering isolation.** Do not read `progress.md`, `orchestrator-role.md` or the syllabus.

**Rendering is authorized.** `AGENTS.md` reserves visual review for the Owner. For PRES-1,
plan §11.3 and the Owner's delegation of 2026-09-28 authorize rendering, screenshots and visual
checks by agents.

## 3. Owner decisions that bind

- **Plan revision 3 §16,** decisions 1–9. These include:
  - the naming rule: `vN · <adopted change>`, a number only after adoption, and "final candidate"
    and "live" as statuses;
  - the experiment `delu-generations`, with `delu-cp2` untouched;
  - the visual tokens.
- **The D1 approval of 2026-09-25.** The contribution statement and the public name "Yarden Viktor
  Dejorno" are displayed exactly as approved. Only the Owner changes them.
- **The standard's ratification, 2026-09-28** (its §17):
  - D2, the plan amendments of §15;
  - D3, the date boundary (below);
  - D5, execution and authority (§7 of this brief);
  - D7, a human cold read, which stays optional and never gates.
- **The Owner's instructions of 2026-09-28:**
  - he runs no tests and no visual checks himself;
  - his final visual approval of PRES-1 is delegated to the Orchestrator;
  - real Safari, a real iPhone and VoiceOver are replaced by the automated checks of the standard's
    §10.
- **The date boundary.**
  - Before the final test, no research generation's number, chart or choice may use data dated
    after 2026-04-07.
  - v1's published holdout replay (the opening preview and v1's archive) stays as published.
  - Add no new view of later data.

## 4. Deliverables and acceptance

**Cross-cutting rules.**

- **Implementation is yours.** You choose modules, file layout, decomposition and order, except
  for the ordering constraints in §5.
- **Generated files are never hand-edited.**
- **Every rendered research number comes from the evidence layer,** with a claim-map entry
  (invariant 17).
- **Each changed or new test** is reported with its reason.

| # | Deliverable (standard clauses) | Acceptance |
|---|---|---|
| **W1** | **Evidence and decisions.** Copy the standard and this brief, byte for byte, into `docs/track-b/evidence/pres-1/`. Add the Owner's 2026-09-28 decisions to `owner-decisions.md`: the standard's §17 outcomes, the delegation of visual approval, and the F1 authorization. | The copies' hashes match §1 |
| **W2** | **The registry (§5).** One entry for every generation, branch, reference, study arm and control, with every §5 field:<br>• the generations v1, v2 and v3;<br>• the branches: the calibration experiment (CP-10) and the model comparison study (CP-15);<br>• the references B0, B2 and B3;<br>• the study arms A1–A5;<br>• the control V2-P.<br>Each policy keeps one identity across experiment codes (V2-H = H0). Every surface takes its names, statuses and order from it: the page, the README, the Space cards, and MLflow run names, parents, descriptions and tags. The current hand-written maps are replaced by it. | **Zero-diff proof.** The registry's introduction is proven to change nothing:<br>• the rebuilt `docs/index.html` and README are byte-identical;<br>• the MLflow export differs only in names, descriptions and tags, shown by a record-level diff in which every metric, history point, parameter and artifact digest is unchanged.<br>**Final names.** They are fixed before F1.<br>**A consistency test with negative controls.** It fails when a registered generation lacks a derived surface, and when a surface names an unregistered entry. |
| **W3** | **Derived records (§3.3).** Each is a typed record computed from committed rows, re-derived by tests with negative controls, and mapped in the claim maps:<br>• the verdict on criteria 1–2 for each evaluated policy;<br>• its distance from daily LEAR in the rule's unit;<br>• N, the policies tested against the rule up to each decision;<br>• the date the rule was set, with its provenance records (`bb5e678` on `evidence/cp-15`; the anchor preserved from attempt 1);<br>• the share-of-score change of v3 against v2, with the fixed-denominator 95% interval;<br>• the per-period MAE ranges, with the stress period named by the protocol. | The standard's Appendix re-derives exactly: −14% / −17%; −2% / −4%; −12% [−16%, −9%] and −14% [−17%, −11%]; 5.3–15.6 and 48.0; 8.6–30.5 and 86.9; N = 8. A perturbed source row fails its test. |
| **W4** | **The headline and the opening (§1, §3.4).** The headline block appears in the research status card and at the top of the README. It reads exactly as the standard's §3.4, with its numbers bound to W3. The terms it introduces are defined directly below it. The "Latest research" summary is removed. The orientation items are placed as §1 requires, including the §8 qualifier "a development diagnostic, not a product qualification". Each generation has one canonical name and a subtitle of at most eight words. | Measured in Chrome and WebKit, with disclosures closed, and recorded under `reports/presentation/release-checks/`:<br>• the headline is fully visible at 1,440 × 900 and at 390 × 844;<br>• the comparison's finding sentence is fully visible within 1,800 px on desktop and 2,532 px on a phone. |
| **W5** | **Page architecture (§6).**<br>• Planned work moves after the chapters.<br>• One generic renderer builds the chapter grammar, with v3 and v2 migrated to its slots and chart headlines bound to claims.<br>• Branch cards for CP-10 and CP-15 attach to the lineage, with no content lost.<br>• v1's chapter follows §4.<br>• v1's archive stays byte-identical to `af0abb0`'s.<br>• The generation colours and markers of plan §7.3 and §7.8 stay for v1–v3. | A slot test with a negative control (a chapter missing a slot fails). The archive's byte-identity is tested. The page stays within 2.0 MB. |
| **W6** | **Numbers and words (§4), and the lint.** The precision rules; the endpoint shown as +0.0000039 on the reading path, with the full value in the table; v1's holdout p-value shown as "p < 10⁻⁶" on the reading path, with the exact value in its table; units and comparators; plain names; terms defined at first use; the target line in words with its date, plus a met / not-met column; explicit policies instead of "negative favours the first policy". One lint, with rule families for codes, precision, percentages and status words, and the reading path defined mechanically (§1). | The lint passes on the final page and the README. Each rule family has a negative control that fails. The lint runs in CI. |
| **W7** | **Status (§5, §1 tone).** Templates are dated and in the past tense. Status words come only through registry tokens. Caveats are phrased as properties of their evidence class, and nothing expires ("We retained v3 as the current research model" is removed). | The status family of the lint passes, and its negative control fails |
| **W8** | **Evidence tiers (§7).** Audit-grade links are labelled "&lt;type&gt;, frozen &lt;date&gt;", with the date matching the evidence tag. "Full report" is relabelled. Reader-grade links stay on the reading path. | A test classifies links by target URL. "No contradicting link" is checked by the independent checker. |
| **W9** | **Surfaces (§8).**<br>• **README:** the generated "At a glance" block, then the generated generation list, then stable hand-written sections only. v1's "30-second read" moves under a v1 heading. The stale surface table and the paraphrase at `README.md:209` are fixed, and no hand-written current state remains.<br>• **Invariant 5, per model.**<br>• **The Space cards** take their model line and links from the registry. | The README ownership test covers the new structure. A parity test (extending `verify_release.py`) shows the headline block, names and statuses agree on every surface. |
| **W10** | **Completeness (§9).**<br>• A route that is not verified has its link omitted; no placeholder mechanism remains.<br>• The final build refuses to run unless the verified index covers every route the registry expects.<br>• A publication guard blocks a push that would put a placeholder or a non-final build record on `main`. It runs from `.githooks/pre-push` after the secret guard, which still runs first and still fails closed. A CI step is its backstop. | The guard has a negative control. The secret guard's test stays green. |
| **W11** | **MLflow** (plan §10; standard §5, §8, §9). Names, descriptions and tags come from the registry. The experiment's description says the repository is the source of truth. The mirror verifier writes `mlflow_index.json`. F1–F4 run as §5 orders them. The run-count test becomes a contract test: the export matches the registry. | Every advertised route passes its REST check and its browser checks in Chromium and WebKit. Anything DagsHub does not support is recorded and not advertised. |
| **W12** | **The Space.** The three marimo fonts that return 404 are either shipped or their references removed; no calculation changes. `test_23` extends to every asset the bundle's CSS and HTML reference. | The demo cold start runs in Chrome and WebKit at both viewports with zero failed requests. The bundle hash is recorded. |
| **W13** | **The stack line** is rendered from the system-view data | Present in "How the system works" |
| **W14** | **Contract tests (§11)** replace tests pinned to content: the 23-run count, the README's "(v3 − v2)", and the three marker shapes | Each replacement asserts the rule, with a negative control |
| **W15** | **The runbook and the packet (§12).**<br>• `docs/track-b/publication-runbook.md` covers every touchpoint: an adopted generation, a branch card, a changed population, and the status transitions as far as they are defined.<br>• A publication-packet template.<br>• `docs/track-b/publication-advisory-log.md`, created with this publication's advisory findings. | The runbook's touchpoints match the registry and the renderer. It is tested, or checked by the checker. |
| **W16** | **Proposals, in the return only:**<br>• the exact landing-template text for the MLflow step and the publication packet (the templates are locked; do not edit them);<br>• a chart encoding for v4 (plan §7.8; the tokens are the Owner's). | Present in the return |

## 5. Ordering constraints

1. **The registry's names are final before F1,** because run names become public at F1.
2. **No F1 without its gate.** F1 runs only after:
   - one independent PASS on a candidate that contains W1–W15;
   - the export is current and its dry run is clean;
   - the §9 credential checks pass.
3. **The order after F1:**
   1. F2: the index is written by the verifier and committed.
   2. F3: the public mirror verification, and the REST and browser route checks, are recorded.
   3. F4: the final build.
   4. A focused recheck on the final candidate SHA; a full recheck if anything beyond the index and
      link targets changed.
4. **Checks before the independent check.** It runs after:
   - the full suite, in local Python 3.13 and in a clean Python 3.12 CI-equivalent run (every step
     in `.github/workflows/tests.yml`);
   - `make verify`;
   - determinism: a rebuild followed by an empty `git status`;
   - `check_links.py`;
   - the standard's §10 release checks;
   - the standard's §11 cold-reader check.

   All of them are recorded.

## 6. Git, worktrees and paths

- **Where to work.** Continue on `gauntlet/pres-1` in `.local/worktrees/pres-1/lead`, committing
  serially.
- **What not to do.** Never commit to `main`, merge, push or create tags.
- **Independent checks:** each in a clean, detached `.local/worktrees/pres-1/check-<n>` (n ≥ 3), at
  the exact candidate SHA. Remove each one afterwards.
- **Evidence:** `docs/track-b/evidence/pres-1/`. The earlier checks and records are preserved.
- **Tools** live under `.local/tools/`:
  - Playwright, with `PLAYWRIGHT_BROWSERS_PATH=.local/tools/playwright/browsers`;
  - the MLflow 3.5.1 rehearsal server.
- **Screenshots** go in `.local/artifacts/presentation/`, and scratch work in `.local/tmp/pres-1/`.
- **Declare every branch, worktree and tag you open.**

**Write allowlist, on the branch:**

- **Source:**
  - `src/delu_forecast/`: the evidence and claim modules, new registry, derived-record and lint
    modules;
  - `claims.py`, but only for the standard's display rules and the per-model limitation scope.
    Invariant 4's statements keep their exact form.
- **Scripts:**
  - `scripts/build_pages.py`, `readme_research.py`, `cp3_readme.py`, `build_wasm_space.py`,
    `check_links.py`, `check_reader_paths.py`, `mlflow_export.py`, `mlflow_publish.py`,
    `verify_mlflow_mirror.py`, `rebuild_presentation.py` and `verify_release.py`;
  - new scripts for the lint and the publication guard;
  - `Makefile` targets for these.
- **The demo app:** `app/wasm_showcase.py`, text and layout only.
- **Generated surfaces and records:**
  - `docs/index.html`;
  - `README.md`;
  - `space-wasm/README.md` and `space/README.md`;
  - the build records these generators rewrite;
  - `reports/presentation/**`.
- **Documents:**
  - `docs/track-b/mlflow-tracking-spec.md`;
  - `docs/track-b/research-content/**` (the claim maps);
  - the runbook, the packet template and the advisory log (W15).
- **Tests:** new tests, and changes to tests 17–34 where the standard changes what they assert.
- **The guard hookup:**
  - `.githooks/pre-push`, only to add the publication guard after the secret guard;
  - `.github/workflows/tests.yml`, only to add the guard's backstop step.
- **Evidence:** `docs/track-b/evidence/pres-1/**`.

**Never touch:**

- the locked set in `AGENTS.md`, including the templates and every capstone anchor and amendment;
- `progress.md`, `pyproject.toml` and `uv.lock`;
- the standard, the plan and this brief, apart from the W1 copies;
- `scripts/secret_guard.py` and the other hooks;
- `DATA-LICENSE.md`, `models/` and `data/`;
- any root file other than `README.md`;
- any committed report or evidence file from CP-2, CP-3, CP-3B, CP-10, CP-15, CP-16 or CP-20,
  except the build records the generators rewrite;
- the v1 registry's tags (`reports/cp3/mlflow_registration.json`, `tags_applied`);
- the `delu-cp2` experiment.

## 7. Authority and stops

- **No approval stops.** The Owner has delegated approvals.
- **Stop only to return BLOCKED or INCOMPLETE,** for one of these:
  - a clause that cannot be met;
  - a governance conflict;
  - a repository state that differs from §1;
  - a credential or network failure;
  - the §9 hard stop.
- **The one public action this brief authorizes (D5).** F1, the upload of the committed export to
  `delu-generations` on DagsHub, once §5's gate holds.
- **Nothing else public:**
  - no push, tag or Space redeploy;
  - no registry change;
  - no write to `delu-cp2`.
- **After your return,** the Orchestrator verifies (§8). Only then does it land, push, redeploy the
  Space and run the post-deploy checks (D5; `AGENTS.md` § Git and publication authority).

## 8. What the Orchestrator will verify; verify it yourself first

- **The SHAs.** The `final_candidate_sha` and the `evidence_tip_sha`. The delta between them touches
  evidence only.
- **The independent checks.** The binding PASS and the focused recheck, both bound to the final
  candidate.
- **A clean checkout.** The full suite (3.13, and a clean 3.12 run), `make verify`, determinism,
  `check_links.py`, the lint and the publication guard.
- **Screenshots.** The headline block, reading exactly as the standard's §3.4, and the standard's §1
  placements, in the Orchestrator's own screenshots at 1,440 × 900 and 390 × 844, in Chrome and WebKit.
- **Links.** No placeholder anywhere. Every advertised MLflow route resolves anonymously to its
  intended run or comparison.
- **The demo.** The Space bundle builds. The demo's cold start in WebKit shows zero failed requests.
- **The return.** It is complete.

A failed item comes back to the Lead, named.

## 9. Ceilings

- **Timebox:** about 60 active hours, from orientation to return. Crossing it is a scope check:
  report it and continue if the remaining work is bounded. **The hard stop is 80 active hours.**
  At that point, stop at a coherent state and return INCOMPLETE, saying what remains. Time spent
  waiting for the Owner does not count.
- **Cost:** $0.
  - No paid service and no new dependency.
  - `pyproject.toml` and `uv.lock` stay byte-identical.
- **Research budget:** none. No fits, no scoring passes and no data retrieval. The derived records
  are arithmetic on committed rows.
- **Network:** read-only HTTP for checks. The only public write is F1.
- **Disk:** at most 5 GiB added under `.local/`.
- **Credentials:** follow `AGENTS.md` § Credentials.
  - Never display a value.
  - Never bypass the secret guard, and keep `core.hooksPath` on `.githooks`.
  - **Before F1:**
    - inside the process, confirm that `MLFLOW_TRACKING_USERNAME` and
      `MLFLOW_TRACKING_PASSWORD` are set, reporting only "set" or "unset";
    - confirm that one authenticated, read-only DagsHub call succeeds, printing nothing derived
      from the credential.
  - **If authentication fails,** return BLOCKED. The Owner may need to restart the app so that the
    session inherits the rotated token.
  - **You do not need `HF_TOKEN`.** The Space redeploy is the Orchestrator's.

## 10. Acceptance

A PASS for PRES-1 requires all of the following:

- every clause of the standard in force (its §16), as the independent checker confirms;
- plan revision 3's invariants 1–26, as amended by the standard's §15;
- the acceptance of W1–W16;
- the §5 checks, all green and recorded;
- the standard's §10 release checks and its §11 cold-reader check, recorded and passing;
- MLflow F1–F3 passed, and the F4 final build with no placeholder;
- one binding independent PASS on the final candidate SHA, with the focused recheck after F2–F4.

If any item cannot be met, return INCOMPLETE or BLOCKED, naming it.

## 11. Independent check

- **Who.** A fresh agent that wrote nothing in PRES-1.
  - Spawn it as `engineering-role.md` describes, with the assignment form in templates §2.
  - It works in a clean, detached worktree at the exact candidate SHA.
- **Its bar:**
  - the standard's clauses in force;
  - plan revision 3, as amended;
  - this brief's §4 and §10.
- **Its scope is full.** It covers:
  - every rendered research number, re-derived, including W3's records;
  - the claim maps, the withheld phrases (W1–W21) and the labels;
  - the charts: units, direction, intervals, scales, the phone variants, and meaning that does not
    depend on colour;
  - the links and the evidence tiers;
  - the standard's §1 placements in Chrome and WebKit;
  - the negative controls of the lint, the status rules and the guard;
  - registry consistency;
  - the README and cross-surface parity;
  - the cold-reader record.
- **The blocking rule (the standard's §11).** Only a violation of a clause in force, or of this
  brief's acceptance, fails the check. Every other finding goes to the advisory log.
- **The verdict** goes to `docs/track-b/evidence/pres-1/independent-check-3.md`; a rerun gets the
  next number.

## 12. Return

Use templates §3, at `docs/track-b/evidence/pres-1/return.md`. The return covers the whole PRES-1
checkpoint: the earlier session's phases 0–E and this conformance work. It includes:

- **Status and identity:**
  - PASS, INCOMPLETE or BLOCKED;
  - the starting `main`;
  - the `final_candidate_sha` and the `evidence_tip_sha`.
- **Execution:**
  - W1–W16, each with its acceptance evidence;
  - every independent verdict;
  - the Owner's approvals and when each was given: D1 on 2026-09-25, and the ratification and D5
    on 2026-09-28.
- **Resources:**
  - active hours;
  - disk used;
  - every network write, each with the instruction that authorized it. For F1, that is D5 of
    2026-09-28, given through this brief.
- **Repository:**
  - the files changed, with one line of reason each;
  - an accounting of branches, worktrees and tags.
- **Landing report:**
  - the proposed disposition, LAND;
  - the evidence tip;
  - the live documents that cite `gauntlet/pres-1`;
  - a proposed squash commit message;
  - the Space bundle hash, and the exact redeploy command from `docs/deploy.md`;
  - the F8 command list: the Pages bytes, the demo's startup and inference in Chrome and WebKit,
    and the MLflow routes.
- **Follow-up:**
  - the W16 proposals;
  - a summary of the advisory log;
  - open issues;
  - interview-capture triggers, one line each; name them only and file nothing;
  - post-return reads.

Then stop.
