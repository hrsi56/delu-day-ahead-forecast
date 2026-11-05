# Track B Checkpoint Brief — CP-18c (CP-18's activation: the live product, now, before 4.7T)

*Issued by the Orchestrator on 2026-11-05, Asia/Jerusalem, under the Owner's decisions 25, 27 and 28.*

## Target
- Repository: DE-LU day-ahead forecasting, `/Users/djourno/Downloads/PJM` (origin
  `hrsi56/delu-day-ahead-forecast`, public). The checkpoint runs locally, in the Lead's own worktree. It may also run
  dry runs in CP-18a's public scratch repository `hrsi56/delu-pipeline-dryrun`.
- Authorized checkpoint: CP-18c, exactly one.
- **Beside it** runs the publication of the research, in another Lead's own worktree. The two share no path (below).
- **What it does.** It turns CP-18a's pipeline and CP-18b's bundle and Space into the working live product, now, under
  decision 28 and r20 §24.14:
  - it retires the boundary guard for the live pipeline only;
  - it downloads all the data the live pipeline needs, from 2026-09-07 through the present;
  - it seeds the live store at the freeze origin and carries it to the first live day;
  - it issues the first live delivery days with the frozen A1 on the issuing host;
  - it builds the dated bundle and the final-product Space from the live record, and publishes the Space to Hugging
    Face, replacing v1's frozen demo, with v1 kept at `/history/`;
  - it completes what the activation still needs, and makes the daily operation ready to run unattended.
- **What follows it:** the Orchestrator's LAND, then the daily operation; 4.7T, no earlier than 2026-12-04, exactly as
  registered; and the publication of 4.7T's result.
- Ratified plan anchor: `capstone_v21.md`, revision v21-r20, SHA-256 `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`.
  - **The bar** is quoted below:
    - §24.14, in full;
    - §24.13's "The issuing host (decision 24; H1)", "The publication time (decision 22)", "The catch-up (decision
      23)" and "For CP-18";
    - §24.12's "Open, for the Owner and for later checkpoints";
    - §19.4;
    - PUBLISH_RULES 1.5 §7.2, §7.3 (A9) and A6.
  - **PUBLISH_RULES** `docs/PUBLISH_RULES.md`, revision 1.5, SHA-256
    `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`.
  - **The Space plan** `docs/track-b/final-product-space-plan-2026-09-30.md`, SHA-256
    `ad3568c8997a08aa291bd3a7f29046c24ce61f0c1fd992622f921b5d23f9174c`.
- **The frozen policy, which this round runs and never changes:** CP-17c's freeze, policy identity
  `720fc581be6206eba8ed303e689e63c09272a189564090a547d93fc9e7db62dc` (`docs/track-b/cp-17c-landing-2026-10-30.md`,
  `docs/track-b/evidence/cp-17c/`). `refreeze verify` on its manifest prints `verified` at the final candidate.
- **The landed preparation, this round's inputs:**
  - CP-18a: `docs/track-b/cp-18a-landing-2026-11-04.md` (`09d23bf4…`), `land/cp-18a` = `65852abd`. Its
    `reports/cp18a/report.md` §8 and its landing record's "What the activation still needs";
  - CP-18b: `docs/track-b/cp-18b-landing-2026-11-05.md` (`fe191d89b808ddb8fa4ad8761fa1a1660c17a47fa118b87bcadde064f890efe2`), `land/cp-18b` = `ff382b2b`. Its
    "What the activation and the publication still need".
- **The Owner's decisions:** 1–19 bound by the frozen copies; 20–21 (`owner-decisions-2026-10-29.md`); 22–25
  (`owner-decisions-2026-10-30.md`); 26–27 (`progress.md`); 28 (`docs/track-b/owner-decisions-2026-11-05.md`,
  `4daa5617e51208b0994eac925d51078ea43481e6fb1017aec3576c0936490215`).
- **The Orchestrator's rulings that bind this round** (decision 27, logged for the Owner): O13 (the status wording),
  O14 (the visitor F1 sentence, with 0.082 EUR/MWh), O16 (the visual approval, provisional), O17 (the Space to
  replace, v1 at `/history/`, the first visit accepted), O18 (N7's issue times and N1's source label), and r20's P1–P4.

## Orchestrator-reported expected state
- **Branch / commit:** `main` = `origin/main` at the commit that records this brief's issue.
  - It is a direct child of `1e3981a9`, v21-r20's ratification, which follows CP-18b's closure `5954d8c3` and its
    landing `ff382b2b`. The issue commit changes only `progress.md`.
  - **Tags:** `land/cp-18b` = `ff382b2b` and `evidence/cp-18b` = `1348c970`, pushed, with every earlier checkpoint's.
    `evidence/cp-26` = `ca20331` is **local-only and never pushed**.
  - **Branches and worktrees:** `main`, and PRES-5's `gauntlet/pres-5` with its worktree `.local/worktrees/pres-5/lead`,
    which runs beside this round. Never touch them.
- **Working tree:** the primary checkout is on `main` and clean apart from ignored material.
  - **The Orchestrator uses it.** Never switch its branch, and never write a tracked file in it. Your only writes
    there are under `.local/artifacts/cp-18c/`, `.local/tmp/cp-18c/`, `.local/tools/` and the worktrees under
    `.local/worktrees/cp-18c/`.
  - **The canonical brief** is `.local/artifacts/cp-18c/issued-brief.md`. Package that file byte for byte.
- **What already exists:**
  - **CP-17c's frozen package** `src/cp17/`, checked by
    `python -m cp17.tools.refreeze verify docs/track-b/evidence/cp-17c/freeze-manifest.json` (`verified` here);
  - **CP-18a's pipeline** `src/cp18/` and `src/cp18/live/`: the live store with its genesis and `carry` commands, the
    live transport and builder, `daily.yml` (dispatch-only, dry run), the local fallback's `launchd` file (not
    installed), the leak scan, the environment lint and the rulesets (written, not applied);
  - **CP-18b's** outcomes, evaluation records, bundle and gate, controls, publication step `cp18.publish`, the Space
    `space-product/` and `scripts/build_product_space.py`, and the browser acceptance `tests/cp18b/space_acceptance.py`;
  - **the boundary guard** `src/cp25/guard.py`, at 2026-09-06 for every path;
  - **the tools:** Pyodide 0.28.0, Playwright 1.63.0 and its browsers, and the official Node.js binary, under
    `.local/tools/`; the Homebrew binary `/opt/homebrew/Cellar/node/26.7.0/bin/node`, pinned;
  - **the guards:** `scripts/secret_guard.py` and `scripts/leak_scan.py`, via `.githooks/`; CP-18b's reproduction
    script `.local/artifacts/cp-18b/ci-runner.py`;
  - **the published surfaces:** the report `docs/index.html` (`54708134…`, v5) and the README (`c816972a…`), which are
    PRES-5's; the Space `Yarden-Viktor/delu-day-ahead-forecast` at revision `0331088725fedab2f5a1ec804ae03bf960cf126f`,
    serving v1's frozen demo;
  - **GitHub:** `gh` is authenticated as `hrsi56`. At issue the product repository had **no repository secret**. The
    Owner is entering `ENTSOE_API_TOKEN`, `HF_TOKEN` and `DAGSHUB_USER_TOKEN`. The public `hrsi56/delu-pipeline-dryrun`
    is CP-18a's scratch repository, which this round may reuse.
  - **No live data exists yet:** no `live/` record on `main`, no live archive, and no
    `docs/track-b/exposure-ledger-continued.md`.
- Verify this yourself before relying on it, and report any material mismatch.

## Observable outcome
CP-18c closes with the following, bound by one fresh Integration-Critic PASS before any upload. Nothing under
`src/cp17/` or `src/cp17c/` changes.

1. **The guard, retired for the live pipeline only** (§24.14 item 2).
   - The live pipeline's boundary is each delivery day's own cutoff, through the present.
   - Every research path still refuses any row after 2026-09-06: CP-25's development downloaders, CP-17c's
     development builder, and every development report. Tests show both sides.
   - If a file that the live pipeline uses for its guard is bound by a freeze manifest or `src/cp26/harness.py`'s
     `PINS`, do not edit it. Route around it in `src/cp18/`, and name the route in the return.
2. **All the data, through the present.**
   - Retrieve every input the live pipeline and its daily refit need: SMARD's prices and load, ENTSO-E's series, the
     load forecast, and GFS from the AWS listing, from 2026-09-07 through the present. Use CP-18a's live transport and
     builder.
   - Archive each response under the live archive's data-only paths, with its URL, retrieval time, size, SHA-256 and
     vintage label.
   - Judge each input's availability for an issuance by publication time against that day's cutoff (§24.13). A day
     whose inputs cannot be shown to precede its cutoff is not issued, with its cause.
   - Decode live GFS with a pinned ecCodes, on the Mac and in the runner's environment.
   - The live-input builder runs only on darwin-arm64, the issuing host's platform (CP-18a's disclosure).
   - Credentials are read from the environment inside the consuming process only.
3. **The live store** (§24.14 item 4). Seed it at the freeze origin, 2026-09-06, with CP-18a's genesis command. Carry
   it to the first live day with CP-18a's `carry`, giving decision 28 as the reason. The days between are outside the
   live record and are never issued.
4. **The first live issuances.**
   - Run on the Owner's Mac, the issuing host's local fallback, after the H2 checks: the pins, the binary, the machine
     and the canary.
   - Issue the current target day and decision 23's catch-up within its lookback, each by the frozen chain, with its
     actual run time in its lineage.
   - Record every day not issued, with its cause.
5. **The outcomes and the evaluation records,** live.
   - Reconcile each issued day's published prices through `cp18.outcomes` with the live transport.
   - Each price names the archive that served it (O18, N1).
   - The live window is prospective, "prospective evaluation in progress". It never pools with development or with
     4.7T, and nothing in it is labelled 4.7T.
6. **The dated bundle and the Space, from the live record.**
   - Build the bundle with `cp18.bundle`. The gate (R7, the frozen identity, the native recompute) passes. The red-line
     check now applies to the research windows only.
   - Build the Space with `scripts/build_product_space.py`, with v1's deployed files from the current Space revision at
     `/history/`, unchanged (O17).
   - **What it says:**
     - A1 is "final candidate · pending 4.7T" (O13);
     - the live scores are "prospective evaluation in progress";
     - no live score is presented as 4.7T's or as a test result;
     - the issue times show the cutoff-based issue time and each issuance's actual run time (O18, N7);
     - O14's sentence;
     - the development-period displays stay on days through 2026-09-06.
   - The browser acceptance passes in Chromium and WebKit, as CP-18b's did, against the live bundle.
7. **The publication to Hugging Face, after the Integration PASS.**
   - Publish the bundle and the Space to `Yarden-Viktor/delu-day-ahead-forecast` with `cp18.publish`'s `HubTarget`,
     with `HF_TOKEN` read inside the uploading process.
   - Then run the served-identity check over HTTPS, and A6's public checks.
   - If the upload or a check cannot complete, return BLOCKED with the exact remaining operation. Report a partial
     upload as partial.
8. **The daily operation, ready to run.**
   - `daily.yml` gains a `schedule:` after the cutoff, the live mode, the claim pointed at `origin`, the bundle step
     (its `--arrays` from `$RESULTS/run/runs/A1-<day>-*/run-arrays.npz` before the results step deletes them), the
     Space build and the publication step.
     - The secrets are read inside the steps that use them.
     - The job holds `contents: write` only where it writes (N6).
     - GitHub's rule that disables a scheduled workflow after a period without activity is handled.
   - **Rehearse it in the public scratch repository** with fake credentials only, dry-run, as CP-18a did. No real secret
     goes to any runner in this round.
   - **The local fallback.** Its `launchd` file is written and tested, not installed. The Orchestrator installs it
     after the LAND if the runner cannot run.
9. **What the activation still needs, done:**
   - N5: an exception in a day's acquisition or build becomes a recorded cause, never an escaped run;
   - O18's N1 and N7;
   - the 31-December Monday bridge-day edge (2029, 2035): it fails closed, as not issued with its cause, until a later
     brief decides it;
   - the rulesets (P0-7): written, applied by the Orchestrator after the LAND.
10. **The exposure ledger's continuation** (§24.14 item 2). Create `docs/track-b/exposure-ledger-continued.md`.
    - Seed it with decision 28's entry, dated by the live pipeline's first retrieval, and its impact assessment as
      §24.14 states it.
    - It records no market value.
11. **The tests and the controls.**
    - The guard's two sides, the carry, N5's causes, the bridge-day edge, the source labels and the issue-time labels.
    - CP-18b's negative controls still refused on the live bundle.
12. **The return's table for the Orchestrator's steps after the LAND, in order:**
    - the push, and GitHub's CI;
    - the first runner dispatch, once the Owner has entered the three secrets;
    - enabling the schedule;
    - the fallback install if needed;
    - the rulesets.

    Each step has its exact command and its check.

## Complete authoritative checkpoint bar
Verbatim, extracted by `scripts/bar.py bar … --at 1e3981a9 --quote` from `main` at r20's ratification.
(The excerpt is the citation. Any line number is a courtesy and is non-binding.)

**`capstone_v21.md` v21-r20 §24.14** (the file `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`; the section 115 lines, 7426 bytes, SHA-256 `5d38de24b3c68ec01e2f5c4e6eaf368c253485107549fc2d85c3c71ccf2f5349`):

> ### 24.14 Publishing and going live before 4.7T (v21-r20)
>
> **What this section does.** It applies the Owner's decision 28 of 2026-11-05
> (`docs/track-b/owner-decisions-2026-11-05.md`, SHA-256 `4daa5617e51208b0994eac925d51078ea43481e6fb1017aec3576c0936490215`).
> - It governs where it differs from §24.2, §24.9, §24.10, §24.12's list "For CP-18", §24.13's list "For CP-18" and
>   decision 25's order.
> - Every term below was set without any 4.7T outcome, since none exists.
>
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
>
> #### What changes
>
> **1. The order (decision 25).** CP-18's activation and a publication now come before 4.7T:
> - **CP-18c**, the activation: the live product starts and runs daily;
> - **PRES-5**, the publication: the research since v5, A1 in the comparison, and the live product;
> - **then 4.7T** at its date, and the publication of its result.
>
> Decision 25's "one complete publication" becomes these two publications.
>
> **2. The red line, for the live pipeline only.** §24.2's guard retires for the live pipeline at CP-18c, not
> after 4.7T.
> - **The live pipeline downloads all the data through the present** and trains on it, as §24.2's last
>   paragraph allows ("The live product, once running, trains on all the data available to it").
> - **Every research path keeps the guard.** The development downloaders and builders still refuse any row after
>   2026-09-06, and CP-17c's development builder stays as frozen.
> - **Reading.** The live data is handled by code.
>   - An agent that operates the live pipeline may read its logs and records, only to operate it.
>   - No agent uses data after 2026-09-06 for any research number, chart, choice or registration before 4.7T is
>     scored.
>   - §24.2's rule on reports, news and analyses about market events after 2026-09-06 is unchanged.
> - **The exposure ledger.** Its pinned file `docs/track-b/exposure-ledger.md` stays byte for byte. Later entries
>   go in its continuation, `docs/track-b/exposure-ledger-continued.md`, which the audit reads with it.
>   - CP-18c seeds the continuation with decision 28's entry, dated by the live pipeline's first
>     retrieval.
>   - **Its impact assessment:** nothing 4.7T tests can change after it. Everything 4.7T tests was frozen,
>     registered and pushed to the public repository before decision 28: `land/cp-17c`, 2026-10-30, and the
>     protocol at its freeze. `refreeze verify` checks the freeze on every run.
>
> **3. The audit (§24.2's standard) reads with this.**
> - **The live product's daily fits** are the frozen policy's own operation, not research fits. They sit
>   outside the standard's "fit" and are recorded in the continuation.
> - **The standard's test applies unchanged** to everything 4.7T tests.
> - **The Owner's declaration** covers his decisions before 4.7T opens. Decision 28 used no information after
>   2026-09-06.
>
> **4. The live product's start.**
> - **The live store** is seeded at the freeze origin, 2026-09-06, with CP-18a's genesis command. It is carried
>   to the first live day with CP-18a's `carry`.
> - **The days between** are outside the live record and are never issued by the live product.
> - **The live product's forecasts for window days,** from its first live day to 2026-12-05, are its own. Each
>   carries its actual run time, and none is 4.7T's.
> - **After 4.7T** the live store continues. §24.12's carry "from 4.7T's last window day to the first live day"
>   becomes this carry from the freeze origin.
>
> **5. What the live product shows.**
> - **It shows the live record** under PUBLISH_RULES A7 and A9: the issued forecasts, the outcomes as published,
>   and the issued forecasts' prospective scores.
> - **A1's status** reads "final candidate · pending 4.7T" (O13).
> - **The prospective scores** are labelled "prospective evaluation in progress" (§24.9).
> - **No display presents a live score** as 4.7T's, or as a test result.
> - **The development-period displays** stay on days through 2026-09-06.
>
> **6. The publication (PRES-5).** Decision 28 is the separate decision that §24.10 requires for publishing
> CP-26's and CP-28's results.
> - **It covers:**
>   - A1 in the published comparison, on the same data as v5's comparison;
>   - CP-26's re-baseline on every development day;
>   - CP-28's selection;
>   - the freeze, with 4.7T's registered terms;
>   - the live product.
> - **Its research numbers use development data only.**
> - **It runs under PUBLISH_RULES 1.5.**
>
> **7. The runner and the secrets.**
> - **Until the Owner enters the three repository secrets** (decision 25), the daily runs use the local fallback
>   on the Owner's Mac (§24.13), with the credentials used only inside the consuming process.
> - **The `macos-26` schedule is enabled** once the secrets exist.
> - **The issuing host and the H2 checks are unchanged** on either machine.
>
> **8. What this supersedes:**
> - **§24.2:** "After 4.7T, CP-18's brief retires the guard for the live pipeline only" (item 2);
> - **§24.9:** the order of "Then: CP-18 … and site activation" (item 1);
> - **§24.10:** "No publication" (item 6);
> - **§24.12's list "For CP-18":** the carry from 4.7T's last window day (item 4);
> - **§24.13's list "For CP-18":** the item on the red line on the runner (item 2).
>
> S_14 (§24.13, H4) is unchanged.
>
> #### Decisions recorded (v21-r20)
>
> | # | Decision | Who |
> |---|---|---|
> | 28 | Publish and go live now; A1 frozen and untouched; 4.7T exactly as registered | Owner, 2026-11-05 (`docs/track-b/owner-decisions-2026-11-05.md`, SHA-256 `4daa5617e51208b0994eac925d51078ea43481e6fb1017aec3576c0936490215`) |
> | P1 | "All the data" for the published research means every development day. Research numbers on window days wait for 4.7T, so that it stays the one test | Orchestrator, under decision 27 |
> | P2 | The live start: genesis at the freeze origin, carried to the first live day. The live product's window-day forecasts are its own, never 4.7T's | Orchestrator, under decision 27 |
> | P3 | The guard retires for the live pipeline only. The exposure ledger continues in a new file, because its own file is pinned | Orchestrator, applying decision 28 |
> | P4 | The local fallback runs until the repository secrets exist | Orchestrator, under decision 27 |
>
> **The Owner's declaration (§24.2)** covers decision 28. P1–P4 are registrations under §24.2's test, which the
> audit checks, as R1–R7 and H1–H4 are.

**`capstone_v21.md` v21-r20 §24.13, "The issuing host (decision 24; H1)"** (the file `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`; the section 73 lines, 5646 bytes, SHA-256 `6eacad578ebbded76cc978cb1ef839e024089b28e532e17eb0cd88da50f24d1e`):

> #### The issuing host (decision 24; H1)
>
> **From CP-17c's landing on,** the issuing host is the following.
>
> | Item | Value |
> |---|---|
> | The runtime | Pyodide 0.28.0, by its 23 pinned file hashes, in the official Node.js v26.7.0 darwin-arm64 binary, one worker. The tarball is `node-v26.7.0-darwin-arm64.tar.gz` from `https://nodejs.org/dist/v26.7.0/`, 57,622,243 bytes, SHA-256 `7ee659a7768e641bbfd5360940660b8e8fd0052f77488f365562bac522fc15d4`. Its `bin/node` is 145,238,560 bytes, SHA-256 `a9bd0630891c2dcdee70de88270fee2cc0c4a9e76495039dd3b4f91c5e6b71df`. The chain's judgement and the shadow states run in CPython inside `cp17.daily`, in the environment `uv.lock` pins, under one CPython patch version that CP-17c pins |
> | The machines | **The daily product:** a GitHub-hosted standard runner, label `macos-26` (Apple silicon), in the product's repository, `hrsi56/delu-day-ahead-forecast`, which is public. **4.7T and any local run:** the Owner's Apple-silicon Mac. The runner's image version and CPU model are recorded, and are not pinned |
> | The reference runtime (§19.3) | the issuing host above, plus Chromium 153.0.8010.12 and WebKit 26.6 through Playwright 1.63.0, on the Apple M3 machine class, as §24.12 records |
> | Resources | unchanged: criterion 5's one worker, 15 minutes of wall time and 4 GB of peak memory |
>
> **What this supersedes in §24.12, from CP-17c's landing:**
> - **its "The issuing host" row,** and the issuing-host part of its "reference runtime" row;
> - **in its list "For CP-18":**
>   - the first item's "deadline and late-forecast rule (§24.4)". The publication time below governs;
>   - the item "where the pipeline runs". The issuing host is the binary and runtime pinned above.
>     - **A machine that passes the checks below (H2) is not a runtime change.** That covers any
>       `macos-26` runner VM, image version or CPU model, and the Owner's Apple-silicon Mac.
>     - **Any other binary, runtime file, operating system or architecture is a runtime change** (§16.2).
>
> **Until CP-17c lands,** §24.12's issuing host stays the frozen host. That is the Homebrew binary
> `1ef99ea25fe70c9b67e7efe768ef8ee22148d3cabc703db6131b57aeb617d040`, and Homebrew's `node` stays pinned
> on the Owner's Mac.
>
> **Why macOS and not Linux (H1).** Both runners passed cleanly, and decision 24 leaves the choice to the
> Orchestrator. CP-17c-probe proposed Linux.
> - **One binary for the whole product.**
>   - 4.7T runs on the Owner's Mac with no cloud (§24.12).
>   - With the macOS runner, the daily product, 4.7T and any local run all use the same binary,
>     `a9bd0630…`, on the same architecture. So 4.7T tests the binary and runtime the product issues
>     with. The probe found the arithmetic identical on every machine it measured, and the canary checks
>     it on every run.
>   - Linux's binary, `ad19784f…`, cannot run on the Owner's Mac. 4.7T would then have tested another
>     binary, or moved to the cloud against its registered terms.
> - **The machine moved no bit.** The same binary reproduced every fit on the runners' M2 Pro, across two
>   runner images, and the parity and F1 fits on the M3.
> - **The cost is the same.** The product's repository is public, where standard runners cost nothing on
>   either OS, by GitHub's published terms. The probe's ten-times macOS rate is a private repository's.
> - **What Linux would have given:**
>   - reproduction on two runner CPU generations, one of them from the cancelled run's records. macOS
>     showed two Apple generations, the M2 Pro and the M3;
>   - more plentiful runners. Decisions 22 and 23 already absorb a delayed or dropped run.
>
> **The runner class.** The probe measured a private repository's `macos-26` class, and the public
> repository's class may differ.
> - **The arithmetic** did not change across machines. The canary checks it on every run.
> - **The timing** did change. Each fit's ceiling is enforced in its own process, so a slower class fails
>   closed, never silently.
> - **So CP-17c measures on a private repository's `macos-26`.** CP-18 measures the public class's timing
>   in the product's repository, on development days, before the first live issuance.
> - **Why not a public scratch repository.** Its runs would need A1's search state and CP-17c's material.
>   That would publish them before decision 25's one complete publication.
>
> **The checks before each run's first issuance (H2).**
> - They run once per run, on either machine, in the order below. They run again whenever the machine or
>   the runtime changes within a run.
> - **Any failure means nothing in that run is issued,** and each of its days is not issued.
> - **For 4.7T,** they run once before the window's first issuance, as part of §24.12's runtime
>   precondition. A failure there is not a day's outcome: no window issuance runs, nothing is counted, and
>   4.7T's brief returns it as a blocker.
>
> The checks:
> 1. **The pins.** `refreeze verify` against CP-17c's manifest must report no problem and no unchecked
>    item. It exits 0 in both cases, so the run reads its output, as §24.12 requires for 4.7T.
> 2. **The binary.** The tarball and `bin/node` must match the hashes above.
> 3. **The machine.** It must be macOS on ARM64. On the runner, `ImageOS` must be `macos26`, and the image
>    version is recorded.
> 4. **A canary fit.** A1 at the freeze origin, 2026-09-06, is reissued under the host. Its quantiles must
>    reproduce the frozen SHA-256 that CP-17c records for the freeze origin.
>    - The probe found CP-17b's value,
>      `4e6abb02fbb02aa8ef202207f21b76bc33b34c37d025a0a93a491135ea43cea5` (`reports/cp17b/host-parity.json`),
>      and CP-17c shows it unchanged.
>    - It took 98.8 s on `macos-26`.

**`capstone_v21.md` v21-r20 §24.13, "The publication time (decision 22)"** (the file `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`; the section 39 lines, 2762 bytes, SHA-256 `8b656f9ae608f63ef630fa12f02416f894d99ebd82aa4222d37193af61311f47`):

> #### The publication time (decision 22)
>
> - **The information cutoff is unchanged:** D−1 11:00 Europe/Berlin, strictly before (§24.4).
>   - A run may happen at any time after the cutoff.
>   - Its payload holds only inputs published before the cutoff. So a later run issues the same forecast,
>     under the condition below.
> - **"Before the outcome"** in the frozen rules means without access to D's outcome, under the target-day
>   embargo (§24.4). It does not mean wall-clock time.
> - **Availability is judged by publication time against D's own cutoff, never by the run time.** The
>   tier register and the Owner's tier, margin and GFS rulings (§24.5) apply unchanged. This covers each
>   input and the GFS-availability flag (§24.12, decision 11).
>   - **For the live pipeline, CP-18 makes this verifiable** in one of three ways:
>     - each day's inputs are retrieved and archived by the cutoff;
>     - each input is taken from a source that preserves its vintage;
>     - for an input the tier register admits with reconstructed availability (tier 2), its documented
>       schedule.
>   - **A live day whose inputs cannot be shown this way is not issued,** and its cause is recorded.
>   - **4.7T's window keeps its registered vintage terms** (the protocol's §3, "Vintages").
> - **A delivery day is issued or not issued.** There is no "late" status and no "late" label.
> - **What stays recorded:**
>   - each issuance's actual run time, in its lineage (§16.2);
>   - the date of the last training, which the product's panel states.
> - **No public wording claims** that a forecast was published before the auction, or before its outcome.
> - **What this supersedes:**
>   - **§24.4's sentence** "The live product publishes its forecast before 12:00 local. CP-18 fixes the
>     schedule, its deadline and its failure rule; a late forecast is recorded as late." CP-18 fixes the
>     schedule and the failure rule. There is no deadline.
>   - **§16.2's "numeric origin/deadlines".** CP-18's brief fixes the origin and the cutoff, and no
>     deadline.
>   - **§16.4's CP-19 row,** where "count real timely forecasts and failures" becomes "count issued and
>     not-issued delivery days". CP-19's at least 90 consecutive delivery days count every day, issued or
>     not issued.
> - **§16.2's rule stands:** "Do not ... backfill a late forecast as timely". No forecast is labelled timely.
>   A catch-up issuance carries its own run time and relabels nothing.
> - **`AGENTS.md`'s daily-update exception needs no change.** It reads: "A failed or late day is published
>   as failed or stale, never skipped silently or backfilled as timely." Under this section:
>   - a day that is not issued is shown as not issued;
>   - the panel shows the date of its last training;
>   - nothing is labelled timely.

**`capstone_v21.md` v21-r20 §24.13, "The catch-up (decision 23)"** (the file `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`; the section 17 lines, 1101 bytes, SHA-256 `3403ca7bb739f7a816bf0cac277df14fdcab15570a2748e77c71515cd7edc4e0`):

> #### The catch-up (decision 23)
>
> - **Each run** issues, in chronological order:
>   - the missed delivery days within a lookback of three days before the current target day;
>   - then the current target day.
> - **At most four issuances run in one run.**
> - **A day older than the lookback is never issued.** It stays not issued, so the backlog never exceeds
>   three days and every run reaches the current day.
> - **Each catch-up** uses only inputs published before that day's own cutoff, as judged above, and never
>   replaces an issued forecast.
> - **The bound in time.**
>   - Each fit keeps its 15-minute ceiling.
>   - Decision 23's record says "a run takes at most about an hour". That counts one fit per issuance.
>   - With A1 and three shadows per issuance, the ceilings bound a four-issuance run, with its canary, at
>     about 4¼ hours. That is inside GitHub's 6-hour job limit, by GitHub's published terms.
>   - Measured on `macos-26`, one issuance took 270–284 s, and four with the canary about 21 minutes.
> - **CP-18 may shorten the lookback** after measuring the runtime. It may not remove the bound.

**`capstone_v21.md` v21-r20 §24.13, "For CP-18" (its last item superseded by §24.14 item 2)** (the file `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`; the section 30 lines, 1991 bytes, SHA-256 `9121e5576a19b96fb40e5062af8fd7329e243a6fdd97bbf8f22bdca3e709750a`):

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

**`capstone_v21.md` v21-r20 §24.12, "Open, for the Owner and for later checkpoints"** (the file `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`; the section 53 lines, 3662 bytes, SHA-256 `9a0d7be68830d512c09ed129fc47590094855e5fdbab2b3c11995f77bbb2702a`):

> #### Open, for the Owner and for later checkpoints
>
> None of these is decided here, except the `schema.py` defect, which R7 accepts:
> - **For the Owner, before 4.7T opens: PUBLISH_RULES §14's "before final-candidate test" items.** These
>   are the badge, the wording, the fresh headline window and the hero-switch rule, and CP-17's protocol
>   §12 proposes them.
>   - They are publication rules, which the Owner ratifies (PUBLISH_RULES §14).
>   - 4.7T's brief cites his ruling.
> - **For the Owner, before CP-18's activation: when A1 replaces v1 as the product.**
>   - Decision 1 reads "v1 stays the product until CP-19".
>   - CP-17's protocol §8 says the same, then adds: "It also stays if 4.7T passes, until CP-18's
>     activation (§16.1)." Its proposed hero-switch rule (§12) reads: "It switches to 'live' only at
>     CP-18's activation, which requires a passed 4.7T."
>   - §16.1 and §19.1 require one identity for the panel, the demo and the daily policy at completed
>     rollout.
>
>   Neither reading governs CP-18's activation until he rules. His ruling can go with the §14 items.
> - **For 4.7T's brief:**
>   - **the §24.2 audit, the Owner's declaration and the retrieval approval;**
>   - **the runtime check, as a precondition.** A window issuance runs only where `refreeze verify`
>     reports no problem and no unchecked file. The command exits 0 in both cases, so the brief reads its
>     output. On CI it reports the issuing host's local files as unchecked, never as passed.
>   - **the window's inputs and payloads.**
>     - `cp17.daily` takes each day's payloads and GFS-availability flag from its caller.
>     - The only payload builder, `cp17.tools.payloads`, is outside the policy identity and refuses days
>       after 2026-09-06.
>     - 4.7T's brief names the code that turns the retrieved data into the frozen payload kinds. That
>       code sets each day's GFS flag under the tier register and the Owner's tier, margin and GFS
>       rulings.
>     - The brief also names how that code is shown equal to the development builder, for example by
>       byte-identical payloads at the nine parity origins, and how the comparators' native runs read the
>       window.
>
>     None of this changes a frozen rule.
> - **For CP-18:**
>   - the unattended pipeline, which calls `cp17.daily` once per delivery day, with its schedule,
>     deadline and late-forecast rule (§24.4);
>   - **where the pipeline runs.** The issuing host is the pinned files above. Any other binary or
>     machine is a runtime change, which needs a new freeze and a new evaluation (§16.2);
>   - publication authority, the MLflow registration of the local names and versions, and the Space's
>     activation;
>   - §19.3's visitor wording, proposed in CP-17's report for the Owner's publication decision. It states
>     F1 as recorded above.
> - **A fail-safe defect in the frozen package, accepted (R7).**
>   - **The defect.** A structurally malformed day in an issued-forecasts record that was also re-hashed
>     in the manifest makes `src/cp17/schema.py` raise an error instead of listing the fault.
>   - **Why it is accepted.** The record is refused either way, so nothing is issued or served from it.
>     A fix changes the package, so it needs a new freeze and a new evaluation (§16.2). Made after 4.7T,
>     a fix would leave 4.7T's result covering a superseded identity.
>   - **What follows.** It is accepted for the frozen policy's life, and fixed at the next freeze. CP-18's
>     pipeline, and the Space wherever it runs `verify_bundle`, treat a raised error as a refused record.
>     The Owner may instead order a re-freeze before 4.7T opens. CP-17b's landing record had listed the
>     defect for CP-18.

**`capstone_v21.md` v21-r20 §19.4** (the file `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`; the section 8 lines, 532 bytes, SHA-256 `cf619098a5aaba12728f3e6f912debd4f59c7db0320b11d6db5afd86ce7256a6`):

> ### 19.4 Daily delivery
>
> Each delivery day, the authorized pipeline publishes a dated bundle to the Space: the issued
> forecasts, the issuing artifact and its lineage, the reconciled outcomes and the evaluation
> records. The bundle's manifest lists every served file with its SHA-256. The Space shows the
> served identity and its freshness. A forecast recomputed by a newer fit is never shown or scored
> as issued. Delivery needs the separate operational and publication authority of §16.2 and
> programme 4.9; this section grants none.

**`docs/PUBLISH_RULES.md` revision 1.5 §7.2** (the file `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`; the section 69 lines, 5102 bytes, SHA-256 `87a0fe6a68a90eb9565a5c8cc3918ee6b909f010ae3b0266ed91eba4bbfe7b68`):

> ### 7.2 Future live presentation — conditional, not activation
>
> The Owner's requested direction is a leading panel for today's forecast versus available actuals
> and tomorrow's forecast with uncertainty, followed by the product documentation. It requires the
> research/live protocol and the triggers in v1 §16 before implementation as a live product.
>
> Revision 1.1 makes this a required outcome for the Owner-designated final product, not an
> optional dashboard. The lifecycle and daily-training contract are in research anchor §16.
> Freeze the policy and reproducible initialization, not all future weights. Daily retraining,
> eligible input refresh and forecast issuance are mandatory for that selected product, subject
> to its declared failure policy. Input/context refresh alone is not training; a model that
> cannot meet daily training needs a documented Owner-approved exception before live admission.
> No such exception is granted here to TabPFN, immutable v1 or any other model.
>
> Distinguish:
>
> - **Frozen fitted artifact:** weights and calibration are unchanged.
> - **Frozen policy:** the algorithm, inputs, update rules and evaluation contract are fixed; fitting
>   can update only if that frozen protocol permits it.
> - **Daily inference/data refresh:** new forecasts from new eligible inputs; does not imply retraining.
> - **Daily retraining:** an explicit update operation requiring its own eligibility, reproducibility
>   and failure rules under the research protocol.
>
> **A7 requires the following display contract when a live panel is authorized:**
>
> | Field | Meaning and required qualification |
> |---|---|
> | Model and policy | Version, actual status and fitted-artifact/update identity |
> | Time | Forecast issue time, information cutoff, delivery date and explicit timezone |
> | Today's prices | Hourly values or an explicitly defined aggregate; distinguish forecast, published actual and not-yet-available outcome |
> | Observed error | A defined metric, units, scoring window, sample count and which issued forecasts it scores |
> | Tomorrow | Issued hourly forecast and prediction interval at the stated nominal level, or a clearly marked unavailable state |
> | Reliability | Observed interval coverage together with width over the named past window; no promise that a nominal level is verified future confidence |
> | Freshness | Last successful update and stale/missing/failed state; never silently present old forecasts as newly issued |
>
> The panel also shows the last successful **training** time separately from data refresh and
> forecast issuance, and identifies the daily artifact that produced each forecast. Today's
> score uses the predictions actually issued for today's delivery hours, not predictions
> recomputed by today's newer fit. Tomorrow's forecast is issued before its outcomes are known;
> before the issuance cutoff or on failure, show a dated pending/unavailable state.
>
> Show a **defined percentage performance measure alongside MAE in EUR/MWh**. Its formula,
> denominator, eligible hours, scoring window, partial-day completeness and handling of zero and
> negative prices must be fixed before evaluation. A possible contract is the percentage of
> scored hours within a predeclared absolute-error tolerance; the numeric tolerance must be
> justified and frozen by the protocol, not chosen after seeing results. A relative improvement
> against a benchmark must be labelled as improvement, not percentage correct. No clipping or
> silent exclusion may make a negative/undefined score look like high accuracy. If there are no
> eligible outcomes, show not yet scored, not 0% or 100%.
>
> Do not label performance merely “X% correct”. Hourly prices can be zero or negative, making common
> percentage errors misleading. Use the protocol's MAE in EUR/MWh and, if authorized and properly
> defined, its benchmark comparison. Do not equate a 95% forecast interval with a 95% probability that
> the point price is correct. A confidence interval for a historical score is a different object.
>
> The panel cannot determine when an outcome becomes scoreable: the protocol defines source,
> publication time, revisions and eligibility. Pending outcomes remain unscored. Keep the `live_`
> namespace boundary, final test protections and prospective publication timestamps.
>
> Before Live, resolve update/publication authority, `delu-live`,
> the runnable frozen-policy registry model, extended namespace tests, live claim builder and the
> demo approach for daily weather inputs. No unattended publishing authority is granted by this anchor.
>
> Daily means every delivery day, including 23/25-hour days. The future operating brief must
> supply an explicitly authorized unattended schedule and failure coverage; silently skipping
> delivery days is not daily operation. This document creates no scheduler or standing unattended-publication permission.
> The static report may be regenerated by that future authorized process; its no-runtime-network
> rule remains in force. Demo and panel use the same policy and identify any different dated
> artifacts; an older historical replay is labelled as such and is not the primary live demo.

**`docs/PUBLISH_RULES.md` revision 1.5 §7.3 (A9)** (the file `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`; the section 52 lines, 5064 bytes, SHA-256 `b5ebca7bb691a88615bf21467dec5b85ae29f1bd48dc99dbb292fe0cf3414f5b`):

> ### 7.3 The final-product Space (A9, conditional)
>
> **A9 applies at A8's trigger to the Hugging Face Space and its direct app,** the primary demo of
> the Owner-designated final product. Research anchor §19 fixes what the Space computes and may
> claim; this section fixes how it presents and how it is accepted. The implementation plan is the
> [final-product Space plan](track-b/final-product-space-plan-2026-09-30.md).
>
> The report remains the entry point: static, self-contained and without a runtime. The Space is
> the product's interactive tool. Both show one product identity and derive every number from the
> same records.
>
> **Required views,** in this order. Each is a real view (plan §7.5): an accessible tab list with
> keyboard operation and deep links, not decorative tabs.
>
> | View | Required content | Required wording and states |
> |---|---|---|
> | Product panel (first, not a tab) | §7.2's A7 fields: identity and status; the daily artifact; separate training, refresh and issuance times; cutoff, delivery dates and timezone; today's issued forecast against published prices, with the frozen percentage measure and MAE over named scored hours; tomorrow's issued forecast with nominal bands; measured coverage with width over the named window | "Not yet scored", pending, partial, stale and failed states; "prospective evaluation in progress" until CP-19; no "X% correct" and no confidence percentage |
> | Train it yourself | Research §19.3's action: the retrain of one issued day's fit, selection agreement, largest difference per quantile, the measured status and the visitor's runtime | Extra download size, reference time and its date before the action; only runtime-reported stages; cancel, failure and retry; the result labelled "your retrained model", never "the forecast" |
> | Forecast | Only issued days in the day picker; issued p50 and nominal bands; published outcomes where available | "Issued at … by artifact …"; any what-if control labelled "counterfactual scenario — not an issued forecast" |
> | Validation | Development folds, static from evidence; the one-shot test and the prospective record recomputed in the browser: MAE, pinball, interval score, coverage with width per band, and the similar-day naive labelled as a reference; counts, failures and late issuances | Evidence badges per window; classes never pooled; a final "Matches the stored value" row with ✓ or ✗ and both values |
> | Reliability | A reliability diagram for every emitted quantile level, with counts; rolling coverage with width per band; the quantile-band PIT | The nominal level drawn and named as a reference, not a target; "nominal …; measured coverage … over …"; never "confidence" |
> | Explainability | The selected forecast decomposed by blend component, then by input contribution, in EUR/MWh against a stated baseline | "Contributed … relative to the model's baseline"; never "caused", never incremental value |
> | Features | The selected day's inputs against their training-window distribution; importance read from the fitted artifact, per component | The named artifact and its date; "how much this fitted model relies on each input"; attribution, not causality |
> | Data | Price distribution, negative hours, hourly profile and regimes, from the shipped series | Definitions where used (quarter-hour averaging, the price floor); date range within research §19.8 |
> | Limitations | Generated from the claim layer shared with the report and README | No hand-written limitation copy |
> | History (a labelled route) | v1's frozen demo, replay and identity check | "Historical"; never presented as the product |
>
> **Presentation line.** Plan §7's tokens, typography, panel grammar, components and states apply
> as on the report. That includes direct labels and marker shapes for generation identity, mobile
> chart variants, one primary action per view and no hover-only meaning. Theme switching, animated
> counters, remote fonts and disabled controls for missing features stay out.
>
> **Loading and network.**
>
> - Startup metadata sits beside the primary action (§7.1).
> - Only the manifest and the day's records load at start. Heavier payloads, above all the
>   training window, load on request after their size is shown.
> - The Space loads its pinned runtime and its own served files only: no runtime call to a data
>   source, registry or tracking service.
> - The page verifies the manifest hashes and shows the served identity; a verification failure is
>   a visible failure state.
>
> **Acceptance.** The §9 matrix applies to every view and control, including framework widgets and
> the tab list. The candidate and public checks record:
>
> - every view's content against its records;
> - the "Matches the stored value" rows passing on the served bundle;
> - the served identity equal to the intended daily artifact;
> - negative controls: a tampered file, a pending outcome, a stale artifact, a mismatched
>   recomputation, a retrain reported as different, and a counterfactual never labelled issued.
>
> A6 applies to the public Space. Visual choices remain the Owner's.

**`docs/PUBLISH_RULES.md` revision 1.5 A6** (the file `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`; the section 15 lines, 1143 bytes, SHA-256 `df28e45b323f87ee4824c47e8d16b7c904793c3e7712da8e73edc50e1bd3cef7`):

> ### A6 — Specify public post-deployment evidence
>
> **Observed need:** postdeploy F01/F02 exposed unnamed demo controls and a public favicon request that
> report-only accessibility or local source checks had not settled. Earlier PASS records did not
> prove current public behaviour. The existing postdeploy step lacked this explicit evidence contract.
>
> **Addition to v1 §12 step 9:** “Verify the served identity and public behaviour of each advertised
> surface, using fresh observations against the applicable browser/interaction requirements. Record
> service revisions, raw/normalized hashes as applicable, first failures and retries, test limitations,
> and the difference between product defects and missing evidence. Local output and prior approvals
> cannot substitute for public checks. Compare previous findings only after forming independent findings.”
>
> **Check:** §10.3 identity records plus applicable §9 matrix and §10.4 verdict.
> **Maintenance:** reuse release checks against public URLs; retain existing probes and truthful scope.
> This clarifies evidence coverage, not a demand for real Safari/iPhone or a new research evaluation.

**Further items,** which bind this candidate as well:

1. **4.7T stays exactly as registered** (§24.14). No 4.7T issuance, store, score or audit runs in this round. Nothing
   the live product issues is labelled 4.7T's. No registered term is touched.
2. **The research boundary holds.** No research number, chart, choice or registration uses data after 2026-09-06. An
   agent reads the live data only to operate the pipeline. No agent reads reports, news or analyses about market
   events after 2026-09-06.
3. **GitHub-landable as is.** No committed file is over 50 MB. The live archive's committed paths are data only, and
   their size is measured and disclosed.
4. **CI-ready.**
   - History-free, with `CI=true` and Python 3.12, and with Git's global configuration hidden. Copy CP-18b's
     `ci-runner.py`.
   - `pytest -m stress` passes.
   - Every committing test sets its own identity, and platform byte tests skip off darwin-arm64.
   - Tests over live data skip with a stated reason when it is absent, so GitHub's CI runs without it.
5. **What never changes:**
   - `src/cp17/`, `src/cp17c/` and every checkpoint's reports and evidence;
   - the landed code outside `src/cp18/`, `space-product/` and the named scripts. New modules may import it;
   - v1's Space source and build (`space-wasm/`, `space/`);
   - `docs/index.html`, the README and the research surfaces, which are PRES-5's;
   - `data/`, `reports/development-inputs/`, `pyproject.toml` and `uv.lock`;
   - the anchors, amendment records, decision records, `AGENTS.md`, `docs/PUBLISH_RULES.md`, the role files, the
     exposure ledger `docs/track-b/exposure-ledger.md` and the backup register.

   Before editing a tracked file, check that no earlier evidence binds its bytes.
6. **The Integration Critic** reruns, locally:
   - the history-free CI and `pytest -m stress`;
   - the guard's two sides;
   - one live bundle built and verified, with the recompute;
   - CP-18b's negative controls on it;
   - the Space in Chromium and WebKit, served locally, with one "Train it yourself" run to its status;
   - `refreeze verify`.

## Task-specific supporting extract
- **The paths PRES-5 owns, which this round never touches:** `docs/index.html`, `README.md`, `docs/track-b/research-
  content/`, the report's build scripts, `reports/pres5/` and `docs/track-b/evidence/pres-5/`.
- **Retrieval, authorized:**
  - the live sources above, from 2026-09-07 through the present, as the live pipeline needs them;
  - the current Space revision's deployed files, for `/history/`;
  - software: ecCodes and its Python binding, pinned, and the files CP-18a's and CP-18b's builds retrieve.

  Record each URL, version, size and SHA-256.
- **The ceilings:**
  - **Local:** 16 machine-hours, summed over workers' wall time. At most 4 concurrent workers, BLAS 1 for native fits,
    CPU only, peak memory 12 GB.
  - **GitHub:** standard hosted runners in the public scratch repository only, at most 6 job-hours, each job's
    `timeout-minutes` set.
  - **Hugging Face:** one publication of the Space, with retries within the service's limits.
  - Keep a ledger, and stop before a ceiling.
- **Presentation.** Build to PUBLISH_RULES §7's tokens and components. Visual choices are the Owner's (O16), so do not
  hold the round for visual taste.

## Applicable constraints
- **Homebrew's `node` stays pinned and installed.** Never upgrade, unpin or remove it.
- **Credentials** follow `AGENTS.md` § Credentials.
  - The live sources' credentials and `HF_TOKEN` are read from the environment inside the consuming process.
  - Never print, log or echo a value, or anything derived from one.
  - No secret is created anywhere. The Owner enters the repository secrets himself.
  - Export `MLFLOW_DISABLE_TELEMETRY=true` and `DO_NOT_TRACK=1`.
- **Before every push** to the scratch repository, and before the upload, run the value-based secret scan over
  everything outgoing (`scripts/secret_guard.py` and `scripts/leak_scan.py`).
- **Allowed paths:**
  - `src/cp18/`, `tests/cp18c/`, `reports/cp18c/`, `docs/track-b/evidence/cp-18c/`;
  - `space-product/`, `scripts/build_product_space.py`;
  - `.github/workflows/daily.yml`;
  - `live/` (the data-only paths);
  - `docs/track-b/exposure-ledger-continued.md` (new);
  - `tests/test_24_live_namespace_is_walled_off.py` (extension only).
- **Long computation** may run unattended in the background, within the ceilings. Commit work in progress on
  `gauntlet/cp-18c` at every stage boundary.
- **Tools:**
  1. run `scripts/gauntlet.py start cp-18c` first, from the primary checkout;
  2. create the worktree with
     `git -C /Users/djourno/Downloads/PJM worktree add -b gauntlet/cp-18c .local/worktrees/cp-18c/lead main`;
  3. run one Critic, through `critic-open`, `critic-brief` and `critic-close`. **The first line of the Critic's
     launch assignment** forbids opening the Claude memory directory;
  4. check the return with `scripts/gauntlet.py return`.
- **Memory:** do not open or edit the files in the Claude memory directory
  (`~/.claude/projects/-Users-djourno-Downloads-PJM/memory/`).
- **Owner-facing Git commands** must be non-interactive.

## Timebox
About 30 active hours from orientation to the terminal return.

## Owner-only actions already authorized
- **CP-18c's execution** under decisions 25, 27 and 28, r20 §24.14 and this brief. The Orchestrator delivers this
  brief under the Owner's grant, and that delivery is the grant. It covers:
  - the retrievals above;
  - the live issuances on the Owner's Mac;
  - pushing to the public scratch repository and running its workflows with fake credentials, within the ceiling;
  - **one Hugging Face publication** of the Space to `Yarden-Viktor/delu-day-ahead-forecast`, after the Integration
    PASS, with `HF_TOKEN` read inside the uploading process, and its public checks;
  - local `gauntlet/cp-18c` commits and the brief's packaging.
- **Nothing else:**
  - no push, branch or tag on `origin`, and no change to its settings, secrets or rulesets;
  - no real secret on any runner;
  - no 4.7T run, store or score;
  - no `launchd` install;
  - no anchor, governance or research-surface edit;
  - no MLflow write;
  - no mainline operation.

## Stop and return
- **First commit.** The first commit copies the canonical brief byte for byte to
  `docs/track-b/evidence/cp-18c/issued-brief.md`.
- **Questions.** If the brief is unclear or wrong, ask the Orchestrator, or stop at the conflict. The anchor,
  PUBLISH_RULES and the Owner's decisions prevail over this brief.
- **The return.** Return exactly one of PASS / BLOCKED / INCOMPLETE, using templates §3, with both terminal SHAs and
  the verdict-only delta, checked with `scripts/gauntlet.py return`.
  - **Its "Open risk or exact owner action" section** gives item 12's table.
  - Name the job-hours and machine-hours used, the live retrievals with their byte totals, and the Space revision
    published.
  - Name any interview-answer trigger in one line each.
- **Do not** open 4.7T, or touch `origin`. Leave your worktree and branch for the LAND.
