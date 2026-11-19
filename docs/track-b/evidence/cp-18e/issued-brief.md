# Track B Checkpoint Brief — CP-18e (decision 33: the live product keeps S_13's search; no S_14)

*Issued by the Orchestrator on 2026-11-19, Asia/Jerusalem, under the Owner's decisions 27, 28, 33 and 34.*

## Target
- Repository: DE-LU day-ahead forecasting, `/Users/djourno/Downloads/PJM` (origin
  `hrsi56/delu-day-ahead-forecast`, public). The checkpoint runs locally, in the Lead's own worktree. It may also run
  dry runs in CP-18a's public scratch repository `hrsi56/delu-pipeline-dryrun`, with fake credentials only.
- Authorized checkpoint: CP-18e, exactly one. No other checkpoint runs beside it.
- **Why.** The live pipeline serves each delivery day from the search that `cp26.search.serving_search(day)` names.
  From delivery day 2027-01-06 that is S_14, whose state `k14.json` §24.13's H4 would have computed on the Owner's
  Mac. Without it, the pipeline leaves every such day open with "S_14's state not in place", so the product would
  stop issuing. The Owner cancelled S_14 and every later search (decision 33): v6 keeps S_13's state.
- **What it does:**
  1. **The live serving rule.** Every live delivery day is served by S_13's state, the one A1's freeze pins
     (`cp17.runtime.K13`), including the days S_14 and later searches would have served.
  2. **Nothing before 2027-01-06 changes,** byte for byte.
  3. **The record and the Space say it:** the issued record names the serving search, and the Space states decision
     33's rule where it describes how v6's networks are chosen.
- **What follows it:** the Orchestrator's LAND; then only 4.7T, when the Owner asks, no earlier than 2026-12-04,
  exactly as registered (decision 34). This is the programme's last round before 4.7T: keep it small.
- Ratified plan anchor: `capstone_v21.md`, revision v21-r20, SHA-256 `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`.
  - **The bar** is quoted below: §24.9 (the search schedule), §24.13's "Where S_14 runs (H4)" and "For CP-18",
    §24.14's "What stays exactly as registered", PUBLISH_RULES 1.5 A9.
  - **Decision 33 supersedes, for the live product only,** §24.9's "the 182-day searches continue, the next being
    S_14 = 2027-01-06", §16.2's frozen refit schedule as far as the searches go, §24.13's H4, and the cause "S_14's
    state not in place". The anchor records it at its next revision. Every other sentence stands.
  - **PUBLISH_RULES** `docs/PUBLISH_RULES.md`, revision 1.5, SHA-256
    `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`.
- **The frozen policy, which this round runs and never changes:** CP-17c's freeze, policy identity
  `720fc581be6206eba8ed303e689e63c09272a189564090a547d93fc9e7db62dc`. `refreeze verify` on its manifest prints
  `verified` at the final candidate.
- **The landed live product, this round's input:** CP-18d, `docs/track-b/cp-18d-landing-2026-11-18.md`
  (`c4da58c0cd6119f1690a6129e80bc127c858e81c730be58224e50cea96bb9d6a`, with its addendum on the first day issued by
  the chain alone), `land/cp-18d` = `c61757d8`.
- **The Owner's decisions:** 1–19 bound by the frozen copies; 20–21 (`owner-decisions-2026-10-29.md`); 22–25
  (`owner-decisions-2026-10-30.md`); 26–27 (`progress.md`); 28 (`docs/track-b/owner-decisions-2026-11-05.md`,
  `4daa5617e51208b0994eac925d51078ea43481e6fb1017aec3576c0936490215`); 29–31 (`docs/track-b/owner-decisions-2026-11-15.md`,
  `ad1beb9f9e7ee235195db96d63d8c3684a5d664f29d51622c866538620c7a323`); 33–34 (`docs/track-b/owner-decisions-2026-11-19.md`,
  `73d64e47ab10b9ba1d6a08765a99cf676c3f40d22d3df6c8e674a9187581921f`).
- **The Orchestrator's rulings that bind this round** (decision 27, logged for the Owner): O13 (the status wording),
  O16 (visual choices are the Owner's), O18 (the issue-time labels), O67 (CP-18d's open items; its alert items are
  not part of this round, decision 34).
- **Execution inputs.** Verify each hash before relying on it (all at `main` `5133b02c`, unless stated):

  | Input | Path | SHA-256 |
  |---|---|---|
  | Decisions 33–34 | `docs/track-b/owner-decisions-2026-11-19.md` | `73d64e47ab10b9ba1d6a08765a99cf676c3f40d22d3df6c8e674a9187581921f` |
  | CP-18d's landing record and addendum | `docs/track-b/cp-18d-landing-2026-11-18.md` | `c4da58c0cd6119f1690a6129e80bc127c858e81c730be58224e50cea96bb9d6a` |
  | CP-17c's freeze manifest (policy identity 720fc581…) | `docs/track-b/evidence/cp-17c/freeze-manifest.json` | `ceab430989d0050a2e8c0cf80f9fa22d0929a9dacfde69fc6c98127605752532` |
  | The live payloads (`load_ensemble`, `a1_payload`) | `src/cp18/live/payloads.py` | `9fbbda1150fbf561868e368833f34d8cc4e52cc3ec6d652cc9b5272d5de28d0e` |
  | The live build (`search_state_missing`) | `src/cp18/live/build.py` | `d0ef43c7f4a2afc4743b7c0253fe5de90057d85505e79c095d8ea32a8898ca2f` |
  | The pipeline (the S14 cause) | `src/cp18/pipeline.py` | `c69e9f4dabc72b8f51c72c1752ac835b140727daf526d7448f93c353769feda1` |
  | The causes | `src/cp18/causes.py` | `aa02af7f66484b0acf6cbb11b7f3d4cf1ff1b22c102fe75fe2011556b7b709c0` |
  | The bundle (the serving search file) | `src/cp18/bundle.py` | `2af6c07e6c819f84c7977e4112ad02fef97bf6f30e2f8fcbdedc8e4d068616af` |
  | The store (`search` entries) | `src/cp18/store.py` | `0f39aa094e10b097c67f86492bc69d8fa1863a8d70046d71298f51ba12b17f4c` |
  | The command line (`cp18 search --k 14`) | `src/cp18/__main__.py` | `4db7020a552136993ca7f5fda4e23f1651bebb8bb8b8b7286622dfc8b46c7599` |
  | The pinned inputs (`K13`) | `src/cp18/inputs.py` | `3dccc0c203b45bda637fb8abe55942f6e09472be23ad1adb01ebbf913c643c58` |
  | The Space's claims | `src/cp18/live_claims.py` | `66dc4fc0b61832234bcadc2bd90eada6f4cd1b7ceb00c586f4aebe51950285c0` |
  | The Space's build | `scripts/build_product_space.py` | `e09a104953b8d8bd26cfb4b0d1f0d54de4e1c31908fbafd7e2bb296941bd251b` |
  | CP-26's search rule (read only) | `src/cp26/search.py` | `941f9b3fb694c856689740a3675af4ea36e60250d6f39cfd1702e9eb9ae44d84` |
  | The frozen payload tools (read only) | `src/cp17/tools/payloads.py` | `d493da6fbe4c57acdd5d160991f65387f21e50b16c9839e32ea1587b0770fd76` |
  | The daily workflow (read only) | `.github/workflows/daily.yml` | `04d712ad6a73f7802866a0cabb09173b2735aad5cc39485f068067a6984e644e` |

## Orchestrator-reported expected state
- **Branch / commit:** `main` = `origin/main` at the commit that records this brief's issue: it adds
  `docs/track-b/owner-decisions-2026-11-19.md` and changes `progress.md`, on top of `5133b02c` (CP-18d's addendum).
  - **`main` moves during this round.** The live product's daily chain pushes data-only commits to `main`, by the
    author `delu-daily`, touching only `live/`. Never write under `live/`. The packet's LAND commands assume a moved
    `main`.
  - **Tags:** every landed checkpoint's `land/` and `evidence/` tags are pushed, except `evidence/cp-26` = `ca20331`,
    which is **local-only and never pushed**. The rulesets refuse moving or deleting a `land/`, `evidence/` or
    `archive/` tag, and refuse pushing a `gauntlet/*` branch.
  - **Branches and worktrees:** `main` only. No other checkpoint runs beside this one.
- **Working tree:** the primary checkout is on `main` and clean apart from ignored material.
  - **The Orchestrator uses it.** Never switch its branch, and never write a tracked file in it. Your only writes
    there are under `.local/artifacts/cp-18e/`, `.local/tmp/cp-18e/` and the worktrees under `.local/worktrees/cp-18e/`.
  - **The canonical brief** is `.local/artifacts/cp-18e/issued-brief.md`. Package that file byte for byte.
  - **A Finder `.DS_Store`** may sit in ignored folders such as `space-product/`. It is local-only and fails one CP-18c
    test in the primary checkout only. A clean worktree does not have it.
- **The live product:**
  - the daily workflow `.github/workflows/daily.yml` runs as CP-18d's self-dispatching chain on GitHub: a Linux tick,
    the `macos-26` acquisition from 5.5 h before D's cutoff, the run after the cutoff, the alert, the next link. On
    2026-11-19 it issued 2026-11-20 with no hand dispatch (the addendum);
  - the live store and the archive are on `main` under `live/`. Ten days are issued, 2026-11-06 to -20, all served by
    S_13;
  - `cp26.search.serving_search` gives 13 for delivery days 2026-07-08 to 2027-01-05 and 14 from 2027-01-06. No
    `k14.json` exists anywhere, and none will.
- **The searches of development:** S_0 to S_13, every 182 days, are CP-26's and stay as they are. CP-26's harness
  pins its files (`src/cp26/harness.py`'s `PINS`).
- **Credentials:** none are needed locally. The scratch repository holds fake ones only.
- Verify this yourself before relying on it, and report any material mismatch.

## Observable outcome
When this checkpoint closes, after the Orchestrator's LAND, the live product issues every delivery day from
2027-01-06 on as it issues 2026-11-20: v6 refitted that day, from S_13's network configurations. No day can be left
open for want of a search.

1. **The live serving rule (decision 33).**
   - **One rule, in `src/cp18/` only.** The live pipeline's serving search is S_13 for every delivery day from S_13's
     own service start, wherever the live code asks which search serves a day: the build, the payload, the pipeline's
     causes, the bundle and the store. `cp26.search` and the frozen package (`src/cp17*`) are not edited.
   - **The state is the pinned one:** `cp17.runtime.K13`, validated as now with `validate_ensemble(..., 13,
     'nominal')`, with its own member seeds. Nothing re-labels it as another search.
   - **No live day can carry "S_14's state not in place".** Where the code keeps that cause for earlier evidence
     (CP-18a's forced days), the Lead states why; the live path cannot reach it.
   - **Entering a later search into the store** (`cp18 search --k 14`, H4's route) is refused, naming decision 33.
   - **If the frozen package itself ties a day to `serving_search(day)`** on the live path, so that a day from
     2027-01-06 cannot be issued without editing `src/cp17*` or `src/cp26/`: stop and return BLOCKED with the exact
     place and the smallest change it would need. Do not edit either.
2. **Nothing before 2027-01-06 changes.**
   - For delivery days through 2027-01-05 the serving search, the payload and its hashes, the forecast and the record
     are those of the code at `5133b02c`, byte for byte. Show it on development days, and on the live record's issued
     days by recomputing what the store already holds where that is possible locally.
   - The ten issued days and every other record under `live/` are untouched.
3. **A day from 2027-01-06, rehearsed.** No such day has data. Show the rule end to end on development days through
   2026-09-06, by the pipeline's own injection point for the serving search (as CP-18a's forced days do): a day the
   old rule would serve by S_14 is built from S_13's state and issued; its record names S_13 and decision 33; and the
   same day under the old rule stays open with "S_14's state not in place" (the negative control).
4. **The record and the Space.**
   - **The issued record** names the serving search for every day (`search` k and its file hash, as now). For a day the
     old rule would have served by a later search, it also names decision 33. The Lead proposes the field; the
     Orchestrator rules.
   - **The Space** states, where it describes how v6's networks are chosen, in one or two sentences through the claim
     layer: the development evaluation re-ran the search every 182 days; the live product keeps the 2026-07-08 search's
     choice for every later day (the Owner's decision 33). If no Space surface describes it yet, the Lead adds those
     sentences where the Space describes v6's daily refit. No number changes. Visual choices are the Owner's (O16).
   - The report (`docs/index.html`) and `README.md` are not edited in this round.
5. **The tests and the controls.**
   - A negative control for each rule: a later search's state entered into the store is refused; a day served by
     another state than S_13's is refused by the live path; the old rule on a day from 2027-01-06 leaves it open.
   - CP-18a–d's tests stay green. Where decision 33 changes a behaviour they assert, the change is stated beside the
     test, as O36 did, and only that assertion changes.
   - `refreeze verify` prints `verified`; CP-26's `PINS` and every freeze manifest's governance pins still hold.
6. **The packet's table for the Orchestrator's steps after the LAND, in order:**
   - the LAND on a moved `main` (the runner's data-only commits) and the push, only while the chain's link is in its
     Linux tick and no `macos-26` job runs;
   - GitHub's CI;
   - the first runner day under the change, and how to check that its record and the Space carry the rule.

   Each step has its exact command and its check.

## Complete authoritative checkpoint bar
Verbatim, extracted by `scripts/bar.py bar … --at 5133b02c --quote` from `main` at `5133b02c`.
(The excerpt is the citation. Any line number is a courtesy and is non-binding.)

**`capstone_v21.md` v21-r20 §24.9, "CP-17 and 4.7T"** (the file `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`; the section 40 lines, 2,007 bytes, SHA-256 `6675e907ccad916e02059b12479daec712f0e720efd4c4056e656b863027a0f1`):

> ### 24.9 CP-17 and 4.7T
>
> **CP-17 freezes one candidate,** CP-28's selection or the control (§24.5), together with:
>
> - its daily retraining rule (§16.2), the issue time, and its inputs and their tiers;
> - its DDNN-2 search state and its combiner state at the freeze;
> - **DDNN-2's search schedule in operation:** the 182-day searches continue, the next being
>   S_14 = 2027-01-06, after S_13 = 2026-07-08, under the same phase and rules, as part of the
>   frozen refit schedule. These are protocol dates only, never permission to read future data;
> - the tier and margin rulings (§24.5);
> - its fallback and failure rules;
> - §19.5's definitions;
> - the lock-price policy, if the final product adopts it
>   (`docs/track-b/final-product-lock-price-notes-2026-10-11.md`).
>
> **§16.4's "before fresh-data test" row** is met by CP-26's daily refits of the control and CP-28's
> of the arms.
>
> **Registered before 4.7T opens:**
>
> - **the comparators:**
>   - the candidate against the control, when they differ;
>   - the candidate against B0, in every case;
>   - v3, v4 and v1's released artifact, as descriptive references;
> - the primary scores and their aggregation, from §24.7;
> - the pass conditions and margins;
> - a dependence treatment suited to 90 days;
> - the failure rules;
> - PUBLISH_RULES §14's "before final-candidate test" trigger.
>
> **The audit (§24.2's standard).** Before opening, the Lead and an independent reviewer check the
> download logs, the boundary guard's tests, the exposure ledger and the Owner's declaration. If the
> standard is not met, 4.7T returns BLOCKED.
>
> **Then:** CP-18, with security hardening (§22's reminder), a controlled live trial whose length the
> Owner sets, and site activation; then CP-19.
>
> **On the timeline.** §16.4 requires CP-19 to cover at least 90 consecutive delivery days after the
> final freeze. With 4.7T opening no earlier than 2026-12-04, CP-19 cannot finish before about March
> 2027. CP-18 may still publish live observations labelled "prospective evaluation in progress".

**`capstone_v21.md` v21-r20 §24.13, "Where S_14 runs (H4)"** (the file `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`; the section 14 lines, 885 bytes, SHA-256 `ad374e1dbe1a68ee197a1bfbd2a6f904cc70f45b991d5f8f90898aca4f71fb68`):

> #### Where S_14 runs (H4)
>
> - **S_14 = 2027-01-06 runs natively on the Owner's M3, the machine that ran S_13.**
>   - It runs in the environment `uv.lock` pins, under the same phase and rules (§24.9) and the freeze's
>     seeds.
>   - It counts as part of the live pipeline for §24.2's guard.
>   - S_13's fits took 5,079 s of native fit time there, on one worker. With CP-26's 2× margin, S_14 is
>     estimated at about 3 hours.
>   - Its state reaches the runner by the route CP-17c fixes for `k13.json`.
>   - A delivery day that S_14 serves is not issued until that state is in place. Decision 23's catch-up
>     then applies.
>   - If that machine is unavailable, where S_14 runs is a new decision for the Owner.
> - **Why.** A native search on another machine is not the same arithmetic, and none was measured.
> - **CP-18 schedules S_14.** It falls after 4.7T's window, so 4.7T is not affected.

**`capstone_v21.md` v21-r20 §24.13, "For CP-18"** (the file `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`; the section 30 lines, 1,991 bytes, SHA-256 `9121e5576a19b96fb40e5062af8fd7329e243a6fdd97bbf8f22bdca3e709750a`):

> #### For CP-18
>
> These add to §24.12's list "For CP-18", as amended above:
> - **the unattended pipeline on the `macos-26` runner.** It calls `cp17.daily` once per issuance, with the
>   checks above and decision 23's catch-up. It has a schedule and a failure rule, and no deadline;
> - **the public runner class's timing,** measured in the product's repository on development days before
>   the first live issuance, against criterion 5's ceilings;
> - **the cause of each day that is not issued,** in the record. The causes are:
>   - a failed issuance by the chain;
>   - a failed H2 check;
>   - a live day's inputs that cannot be shown to precede its cutoff;
>   - no run within the lookback;
>   - S_14's state not in place;
> - **one issuance per delivery day across the runner and the local fallback.** The issued record is the
>   single source, and no issued forecast is replaced;
> - **how the states are carried** from 4.7T's last window day to the first live day;
> - **a live day's input availability,** made verifiable as the publication time above requires;
> - **the credentials as GitHub secrets.** The Owner enters them himself (decision 25), and agents never
>   handle their values;
> - **`AGENTS.md`'s conditions on the runner:**
>   - the secret guard and the pre-push guards run on the runner's own commits and pushes;
>   - credentials are used only as stored variables inside the consuming process;
> - **public run logs.** The repository is public, so its run logs are public. Credentials, and any value
>   derived from them, are never printed;
> - **GitHub's rule that disables a scheduled workflow** after a period without repository activity. CP-18
>   shows how the pipeline stays enabled;
> - **a local fallback on the Owner's Mac,** with the same binary and the same checks;
> - **the red line on the runner.** Until CP-18's brief retires the boundary guard after 4.7T (§24.2), the
>   runner's pipeline runs only on development data through 2026-09-06 (decision 7). No scheduled run
>   retrieves later data.

**`capstone_v21.md` v21-r20 §24.14, "What stays exactly as registered"** (the file `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`; the section 16 lines, 1,161 bytes, SHA-256 `0e1f357969f5bad69b4e5dbc4682631196a77b4580381b6ef887cb96b7607c84`):

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

**`docs/PUBLISH_RULES.md` revision 1.5 A9** (the file `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`; the section 14 lines, 833 bytes, SHA-256 `c264126b70356802d2ca526386d9aa54a6219b2974a2aef0e517147ff18bf4bc`):

> ### A9 — The final-product Space
>
> **Observed need:** on 2026-09-30 the Owner found the Space uninformative for a daily product.
> The Owner asked for a daily-trained tool with a "Train it yourself" button, today and tomorrow
> panels, and views for data, features, validation, explainability, reliability, the forecast and
> limitations. The existing rules specified only the demo's states, its startup metadata and the
> panel's fields.
>
> **Addition, conditional on A8's trigger:** §7.3.
>
> **Check:** the §7.3 acceptance record, on the candidate and on the public Space.
> **Maintenance:** views render from the daily bundle and the shared claim layer, with no second
> claim source and no hand-typed numbers. The daily pipeline's cost is bounded by the CP-18 brief.
> This amendment adds no model, research, schedule or publication authority.

**Further items,** which bind this candidate as well:

1. **4.7T stays exactly as registered** (§24.14). Its window, 2026-09-07 to 2026-12-05, is served by S_13 under both
   rules. No 4.7T issuance, store, score or audit runs in this round. Nothing the live product issues is 4.7T's.
2. **A1 stays frozen.** No file of the frozen package, its manifest, `src/cp17*` or the freeze's evidence changes.
   `refreeze verify` prints `verified` at the final candidate.
3. **CP-26 stays as it is.** `src/cp26/` and its evidence are not edited; its searches S_0 to S_13 are the
   development record.
4. **The red line.** The live pipeline is exempt (r20 §24.14). No research number, chart or choice uses data after
   2026-09-06. The rehearsal uses development days only.
5. **§16.2's public wording** for a change to the frozen refit schedule: item 4 of the outcome.
6. **Critic and return:** `docs/track-b/gauntlet-templates.md` §§2–3.

Map every applicable item to evidence. The extract below does not narrow this bar.

## Task-specific supporting extract
- **The live product runs every day during this round,** from `main`, on the runner. Never push to the product
  repository, never write under `live/`, and never dispatch or cancel its workflows. The Orchestrator owns them.
- **Keep it small.** Decision 34 makes this the last round before 4.7T. Change only what decision 33 needs, with its
  tests and its two sentences on the Space. No other follow-up enters this round.
- **The ceilings:** 4 local machine-hours, summed over workers' wall time, at most 4 concurrent workers, CPU only;
  GitHub runner minutes in the scratch repository only if the rehearsal needs a runner. Keep a ledger, and stop
  before a ceiling.
- **Presentation.** Visual choices are the Owner's (O16). Build to the Space's existing tokens and components.

## Applicable constraints
- **Homebrew's `node` stays pinned and installed.**
- **Credentials:** none are needed locally. Never print, log or echo a credential value. The scratch repository uses
  fake credentials only. Export `MLFLOW_DISABLE_TELEMETRY=true` and `DO_NOT_TRACK=1`.
- **Allowed paths:**
  - `src/cp18/` and `tests/cp18e/`; `tests/cp18a/` to `tests/cp18d/` only as outcome item 5 allows;
  - `space-product/` and `scripts/build_product_space.py`;
  - `reports/cp18e/` and `docs/track-b/evidence/cp-18e/`.

  No anchor, governance file, `docs/PUBLISH_RULES.md`, `progress.md`, frozen record, `src/cp17*`, `src/cp26/`,
  `live/`, `.github/workflows/`, the report (`docs/index.html`, `README.md`) or the exposure ledger.
- **Before editing a tracked file,** check that no earlier evidence binds its bytes. That includes:
  - `src/cp26/harness.py`'s `PINS`;
  - `tests/pres5_landed_code.py`;
  - every freeze manifest's governance pins;
  - CP-18c's and CP-18d's evidence (`reports/cp18c/`, `reports/cp18d/`, `docs/track-b/evidence/cp-18c/`,
    `docs/track-b/evidence/cp-18d/`).
- **Tools:**
  1. run `scripts/gauntlet.py start cp-18e` first, from the primary checkout;
  2. create the worktree with
     `git -C /Users/djourno/Downloads/PJM worktree add -b gauntlet/cp-18e .local/worktrees/cp-18e/lead main`;
  3. run the independent check through `critic-open`, `critic-brief` and `critic-close`. **The first line of the
     Critic's launch assignment** forbids opening the Claude memory directory;
  4. check the return with `scripts/gauntlet.py return`.
- **Memory:** do not open or edit the files in the Claude memory directory
  (`~/.claude/projects/-Users-djourno-Downloads-PJM/memory/`).
- **Owner-facing Git commands** must be non-interactive.

## Timebox
About 5 active hours from orientation to the terminal return.

## Owner-only actions already authorized
- **CP-18e's execution** under decisions 27, 28, 33 and 34 and this brief, on `gauntlet/cp-18e`. The Owner said "תעשה
  את התיקון עכשיו" ("do the fix now"). The Orchestrator delivers this brief under his grant, and that delivery is the
  grant.
- **Dry runs in the scratch repository** `hrsi56/delu-pipeline-dryrun`, with fake credentials only, after the
  value-based secret scan of what is pushed there.
- **No action on the product.** No push, landing, merge or tag on the product repository, no Space upload, no write to
  the live store or `live/`, no workflow dispatch on the product repository, no governance edit. Those that apply
  are the Orchestrator's, after the return.

## Stop and return
- **First commit.** The first commit copies the canonical brief byte for byte to
  `docs/track-b/evidence/cp-18e/issued-brief.md`.
- **Questions.** If the brief is unclear or wrong, ask the Orchestrator, or stop at the conflict. The anchor, the
  Owner's decisions and PUBLISH_RULES prevail over this brief.
- **The return.** Return exactly one of PASS / BLOCKED / INCOMPLETE, using templates §3, with both terminal SHAs and
  the verdict-only delta, checked with `scripts/gauntlet.py return`.
  - Its "Open risk or exact owner action" section gives the packet's steps and every open item, with a proposed
    ruling for each.
  - Name the machine-hours used.
- Leave your worktree and branch for the LAND.
