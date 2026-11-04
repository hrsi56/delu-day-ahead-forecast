# Track B Checkpoint Brief — CP-18a (CP-18's preparation, part 1: the daily pipeline, its states, the runner and security hardening)

*Issued by the Orchestrator on 2026-10-30, Asia/Jerusalem, under the Owner's decisions 7, 25, 26 and 27.*

## Target
- Repository: DE-LU day-ahead forecasting, `/Users/djourno/Downloads/PJM` (origin
  `hrsi56/delu-day-ahead-forecast`). The checkpoint runs locally, in the Lead's own worktree, plus runs on
  GitHub-hosted `macos-26` runners in one new **public** scratch repository (below).
- Authorized checkpoint: CP-18a, exactly one.
- **What follows it:** the daily bundle and the Space, under their own brief.
- **What it does.** It builds, on development data only, everything CP-18's activation needs to run A1
  unattended every delivery day, except the Space and the bundle:
  - the daily pipeline around the frozen package;
  - the states it carries;
  - the `macos-26` workflow and the local fallback;
  - the live-input payload builder;
  - the security hardening §22 reminds of.

  Nothing in this round retrieves, reads or issues for a delivery day after 2026-09-06.
- Ratified plan anchor: `capstone_v21.md`, revision v21-r19, SHA-256 `acdeeab18a17ecdb83ade83d369a5031f3180f8fdb618a23af5b37836663996e`.
  - **The bar** is quoted below:
    - §24.13's "For CP-18", with its publication time, catch-up and S_14 sections;
    - §24.12's "For CP-18" and its R7 paragraph;
    - §19.4;
    - §22's binding reminder on CP-18's security items;
    - the Space plan's §7 step 4 and step 6, as far as the pipeline is concerned.
  - **Decision 7** (`docs/track-b/pre-cp-17-rulings-2026-10-25.md`): CP-18's preparation runs "with dry runs
    on data to 2026-09-06 only".
- **The frozen policy this round runs, and never changes:** CP-17c's freeze.
  - its landing record `docs/track-b/cp-17c-landing-2026-10-30.md` (`89b65c841950cbb389a7e0f849f149f487669819491a71bb434e9d91f96b4759`);
  - its freeze record and manifest under `docs/track-b/evidence/cp-17c/`, policy identity `720fc581be6206eba8ed303e689e63c09272a189564090a547d93fc9e7db62dc`;
  - `land/cp-17c` = `1622e1873de241c9d49c44bdcf97398ba21696c3` and `evidence/cp-17c` = `26288046cd76e17e7fd6ee9d28297a3a93c8056b`.
- **The Owner's decisions:**
  - 1–19, bound by CP-17b's and CP-17c's frozen copies;
  - 20–21 in `docs/track-b/owner-decisions-2026-10-29.md`;
  - 22–25 in `docs/track-b/owner-decisions-2026-10-30.md`
    (`1286548362b5618e3fb01c616d673c0af83dd79effeaf102bb9727ac219aabab`);
  - 26–27 in `progress.md` (2026-10-30): scratch repositories may be public, and the Orchestrator decides
    every matter that costs the Owner nothing.

## Orchestrator-reported expected state
- **Branch / commit:** `main` = `origin/main` at the commit that records this brief's issue.
  - It is a direct child of `c350203b04f19989b9ef1a15e075325b329f16de`, CP-17c's closure, and changes only `progress.md`.
  - **Tags:**
    - `land/cp-17c` = `1622e187` and `evidence/cp-17c` = `26288046`, pushed, with every earlier
      checkpoint's;
    - `evidence/cp-26` = `ca20331`, which is **local-only and never pushed**.
  - **Branches and worktrees:** none besides `main` and the primary checkout.
- **Working tree:** the primary checkout is on `main` and clean apart from ignored material.
  - **The Orchestrator uses it.** Never switch its branch, and never write a tracked file in it.
    Your only writes there are under `.local/artifacts/cp-18a/`, `.local/tmp/cp-18a/`, `.local/tools/`
    and the worktrees under `.local/worktrees/cp-18a/`.
  - **The canonical brief** is `.local/artifacts/cp-18a/issued-brief.md`. Package that file byte for
    byte.
- **What already exists:**
  - **CP-17c's frozen package** `src/cp17/`. Its check is
    `python -m cp17.tools.refreeze verify docs/track-b/evidence/cp-17c/freeze-manifest.json`, which prints
    `verified` on this machine. It includes the H2 checks `cp17.hostcheck` and the host pins
    `cp17.runtime`;
  - **CP-17c's harness** `src/cp17c/`, usable as a pattern:
    - the scratch workflow `refreeze.yml`, which retrieves the binary by hash;
    - the state store `store.py`, with its head bound to its ledger;
    - the states' route `state.py`;
    - the scratch tree builder `inputs.py`;
  - **the official binary** in `.local/tools/node-v26.7.0-official/`, and **Pyodide 0.28.0** in
    `.local/tools/pyodide-0.28.0/`;
  - **the states:**
    - the freeze-origin state and the canary payload in `.local/artifacts/cp-17c/state/`;
    - A1's `k13.json` in CP-17's verified `evidence/cp-26` extract,
      `.local/artifacts/cp-17/inputs/reports/rebaseline/cold-rerun-2026-10-15/search-results/nominal/`;
  - **the development payload builder** `cp17.tools.payloads`, which refuses days after 2026-09-06;
  - **CP-25's recorded data** in `.local/artifacts/cp-25/` and the `evidence/cp-26` extract, read-only;
  - **the boundary guard** `src/cp25/guard.py`. Its boundary stays at 2026-09-06;
  - **the secret guard** `scripts/secret_guard.py`, called from `.githooks/` (`pre-commit`, `pre-push`,
    `commit-msg`), and the CI workflow `.github/workflows/tests.yml`;
  - **the Homebrew binary** at `/opt/homebrew/Cellar/node/26.7.0/bin/node`, pinned. It is CP-17b's
    frozen host and stays installed;
  - **GitHub:** `gh` is authenticated as `hrsi56`, with the `repo` and `workflow` scopes. The public
    repository `hrsi56/delu-host-refreeze` is CP-17c's, and the private `hrsi56/delu-host-probe` is
    CP-17c-probe's. Leave both untouched.
- Verify this yourself before relying on it, and report any material mismatch.

## Observable outcome
CP-18a closes with the following, bound by one fresh Integration-Critic PASS. Nothing under `src/cp17/`
changes: the frozen package is called, never edited. Any change there is a re-freeze, which this round
does not do.

1. **The daily pipeline, as code** in a new package `src/cp18/`, with tests under `tests/cp18a/`.
   - **One run:**
     1. the H2 gate (`cp17.hostcheck`), once, before the first issuance. Any failure issues nothing in
        that run;
     2. decision 23's catch-up: a three-day lookback, at most four issuances per run, oldest first;
     3. each issuance through `cp17.daily`, once per delivery day.
   - **No deadline and no "late" label (decision 22).**
     - The cutoff stays D−1 11:00 Berlin.
     - The run time stays in the artifact.
     - A live day's input availability is judged by publication time against its cutoff, never by the
       run time. Make that judgement verifiable from the record: each input's source publication time,
       retrieval time and hash.
   - **The issued record is the single source.**
     - One issuance per delivery day, across the runner and the local fallback.
     - No issued forecast is ever replaced, rescored or relabelled.
     - Design the claim, for example: the day's issued record on `origin/main` is the claim, the pipeline
       fetches before issuing, and the loser of a push race discards its own issuance. Test the race.
   - **The cause of each day not issued,** recorded in the record. The causes are r19's five:
     - a failed issuance by the chain;
     - a failed H2 check;
     - a live day's inputs that cannot be shown to precede its cutoff;
     - no run within the lookback;
     - S_14's state not in place.
   - **R7's rule stays** wherever the pipeline calls `verify_bundle`: a raised error is a refused record.
   - **The red line in code.** Until CP-18's activation brief retires the boundary guard after 4.7T,
     the pipeline refuses any delivery day after 2026-09-06 (`src/cp25/guard.py`). The retirement is a
     one-line, reviewed change that a later brief makes, not a flag.
   - **A red-line test over every file this round adds,** with no file skipped whole. CP-17c's test
     skipped two of its reports whole (its second review's N4).
2. **The live-input payload builder.**
   - It is the code that turns retrieved source data into the frozen payload kinds `cp17.daily` takes,
     with each day's GFS flag set under the tier register and the Owner's tier, margin and GFS rulings.
   - **Shown equal to the development builder** (`cp17.tools.payloads`): byte-identical payloads at the
     nine parity origins and on the 14 shadow days. The source is CP-25's recorded vintage data, never a
     fresh download.
   - **The retrieval clients** (ENTSO-E, and every other source A1's payloads need) are exercised only
     against recorded responses.
   - **No network data retrieval in this round.** 4.7T's brief and CP-18's activation brief cite this
     builder.
3. **The state store,** from CP-17c's proposal (`reports/cp17c/state-route-proposal.md`).
   - **Keep CP-17c's fix for its first Critic's F1.** `head.json`'s `state_file`, `state_sha256`,
     `last_day` and `last_artifact_sha256` equal the ledger's last entry, and a repointed head fails
     `Store.verify()` (`src/cp17c/store.py`). The pipeline's store imports it or carries it into
     `src/cp18/` with its test. It never weakens it.
   - **Where the states live.**
     - CP-17c's landing record rules this under decisions 26 and 27. A1's `k13.json`, the freeze-origin
       states, the canary payload and the carried states may sit in the public product repository's Git
       history. Its Pages site never serves them.
     - Name the exact data-only paths that CP-18's daily commits to `main` will use (`AGENTS.md`'s
       standing publication exception requires the brief to name them).
   - **The carry from 4.7T's last window day to the first live day.** Design it, and rehearse it on
     development days: a store carried across a gap, and resumed bit for bit.
   - **S_14 (H4):** where its state enters the store, and what the pipeline records while it is absent.
4. **The runner workflow,** `.github/workflows/daily.yml` (new).
   - **It runs on `workflow_dispatch` only in this round.** It has no `schedule:` trigger; CP-18's
     activation adds one.
   - Retrieve the official binary by hash, run the H2 gate, then the pipeline in dry-run mode on
     development days.
   - **The binary and Pyodide's 23 files reach the runner by hash,** from their official release URLs, as
     CP-17c's harness did.
   - **The secret guard and the pre-push guards run on the runner's own commits and pushes.** Show it,
     with a fake credential that the guard blocks by value.
   - **Credentials** are read only as stored variables inside the consuming process. Show with fake
     values that no log line and no artifact contains one.
     - **The Orchestrator has fixed the names,** as repository secrets in
       `hrsi56/delu-day-ahead-forecast` that the Owner enters himself: `ENTSOE_API_TOKEN`, `HF_TOKEN` and
       `DAGSHUB_USER_TOKEN`. The MLflow URI is public configuration, not a secret.
     - **If the live pipeline needs any other credential,** name it in the return. This round creates
       none.
   - **GitHub's rule that disables a scheduled workflow** after a period without repository activity:
     show how the pipeline stays enabled.
   - **Permissions:** `contents: write` only where the day's data-only commit needs it; everything else
     read.
5. **The local fallback on the Owner's Mac:**
   - the same binary (`.local/tools/node-v26.7.0-official/`), the same checks and the same claim rule;
   - one command;
   - a proposed `launchd` agent file, written but not installed. Installing it is CP-18's activation.
6. **The public runner class's timing (§24.13).**
   - Measure it on development days in the public scratch repository: one issuance, and four with the
     canary, against criterion 5's ceilings.
   - It is the same class as the product repository's. The Orchestrator repeats one dispatch in the
     product repository after this round lands, and records it in the landing record.
   - **CP-17c's one data point:** two resumed days on that class, 382.7 s per issuance alone, on a 3-core
     M1 virtual machine. Its private class gave 431.8 s with two blocks side by side.
7. **Security hardening (§22; the archived proposal `archive/deterministic-migration-plan-20261001`):**
   - **P0-2, the value-free leak scan:** `scripts/leak_scan.py`, with:
     - F2 environment-dump shapes and F3 known prefixes;
     - F1 salted fingerprints, supported with the generator `scripts/credential_fingerprints.py`. The
       fingerprint file itself is generated by the Owner on his Mac, never by an agent;
     - wiring into `.githooks/` after `secret_guard.py`, and as the first CI step in `tests.yml`;
     - the proposal's acceptance on fake fixtures only.
   - **P0-3, environment-dump prevention:**
     - the AST lint for bare `os.environ` subscript reads, as a test with a reasoned allowlist;
     - the pytest redaction plugin registered with `-p`, if `pytest.ini` is not bound by any earlier
       evidence (check `PINS` and every freeze manifest first). Otherwise, the least intrusive
       registration, stated.
     - `src/cp17/` is frozen, so any read there is allowlisted with that reason.
   - **P0-7, the server-side rulesets:**
     - their exact configuration as JSON files under `reports/cp18a/rulesets/`, ready to apply;
     - the acceptance steps.

     Applying them is outside this round.
8. **What CP-18's activation brief and 4.7T's brief cite,** in the return, in one table: paths,
   commands, secret names, the claim rule, the state paths and the timing.

## Complete authoritative checkpoint bar
Verbatim, extracted by `scripts/bar.py bar … --at 1622e187 --quote` from `main` at CP-17c's landing.
(The excerpt is the citation. Any line number is a courtesy and is non-binding.)

**`capstone_v21.md` v21-r19 §24.13, "For CP-18"** (the file `acdeeab18a17ecdb83ade83d369a5031f3180f8fdb618a23af5b37836663996e`; the section 30 lines, 1991 bytes, SHA-256 `9121e5576a19b96fb40e5062af8fd7329e243a6fdd97bbf8f22bdca3e709750a`):

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

**`capstone_v21.md` v21-r19 §24.13, "The publication time (decision 22)"** (the file `acdeeab18a17ecdb83ade83d369a5031f3180f8fdb618a23af5b37836663996e`; the section 39 lines, 2762 bytes, SHA-256 `8b656f9ae608f63ef630fa12f02416f894d99ebd82aa4222d37193af61311f47`):

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

**`capstone_v21.md` v21-r19 §24.13, "The catch-up (decision 23)"** (the file `acdeeab18a17ecdb83ade83d369a5031f3180f8fdb618a23af5b37836663996e`; the section 17 lines, 1101 bytes, SHA-256 `3403ca7bb739f7a816bf0cac277df14fdcab15570a2748e77c71515cd7edc4e0`):

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

**`capstone_v21.md` v21-r19 §24.13, "Where S_14 runs (H4)"** (the file `acdeeab18a17ecdb83ade83d369a5031f3180f8fdb618a23af5b37836663996e`; the section 14 lines, 885 bytes, SHA-256 `ad374e1dbe1a68ee197a1bfbd2a6f904cc70f45b991d5f8f90898aca4f71fb68`):

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

**`capstone_v21.md` v21-r19 §24.12, "Open, for the Owner and for later checkpoints" (its "For CP-18" list and R7)** (the file `acdeeab18a17ecdb83ade83d369a5031f3180f8fdb618a23af5b37836663996e`; the section 53 lines, 3662 bytes, SHA-256 `9a0d7be68830d512c09ed129fc47590094855e5fdbab2b3c11995f77bbb2702a`):

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

**`capstone_v21.md` v21-r19 §19.4** (the file `acdeeab18a17ecdb83ade83d369a5031f3180f8fdb618a23af5b37836663996e`; the section 8 lines, 532 bytes, SHA-256 `cf619098a5aaba12728f3e6f912debd4f59c7db0320b11d6db5afd86ce7256a6`):

> ### 19.4 Daily delivery
>
> Each delivery day, the authorized pipeline publishes a dated bundle to the Space: the issued
> forecasts, the issuing artifact and its lineage, the reconciled outcomes and the evaluation
> records. The bundle's manifest lists every served file with its SHA-256. The Space shows the
> served identity and its freshness. A forecast recomputed by a newer fit is never shown or scored
> as issued. Delivery needs the separate operational and publication authority of §16.2 and
> programme 4.9; this section grants none.

**`capstone_v21.md` v21-r19 §22 (its binding reminder on CP-18's security items)** (the file `acdeeab18a17ecdb83ade83d369a5031f3180f8fdb618a23af5b37836663996e`; the section 59 lines, 3312 bytes, SHA-256 `43bde77b40435fefd23e30a847dc2da7ef6dcc61518cfc2f81d1bcf77487e8f9`):

> ## 22. Programme order after CP-22 (Owner, 2026-10-04)
>
> The Owner approved this order on 2026-10-04 ("הסדר המאושר", then "בצע"). It amends the
> handoff's sequence only as stated here.
>
> 1. **Automation, done 2026-10-04.**
>    - Items 2, 1, 5, 3, 4 and 8 of `docs/automation-plan.md` were implemented in commit
>      `42e4ceb`.
>    - Item 3 was created under the Owner's task-scoped suspension of the same day.
>    - Templates §4's receipt list governs (the Owner's ruling).
> 2. **CP-23, DDNN (§21).**
> 3. **Immediately after DDNN: a comprehensive data-admission research, together with 4.4V.**
>    - **Scope, in the Owner's words:** energy prices, interest rates, the local stock market's fear
>      index, and "כל מה שאפשר וחוקי לשלוף וללמוד ממנו". The research covers at least:
>      - gas (TTF and alternatives), oil, coal and carbon (EUA);
>      - central-bank rates;
>      - a German volatility index;
>      - neighbouring-zone and cross-border inputs;
>      - outages;
>      - wind, solar and load forecasts.
>    - **Late publication.** For an input published after the 11:00 UTC origin, the research tests
>      two routes. One is an earlier vintage that already covers the delivery day, for example a
>      forecast for day D published at 18:00 on D−2. The other is a provider that publishes before
>      the origin. It also assesses an external wind and solar forecast API, available and
>      reliable, as an alternative to building 4.4V's own model.
>    - **Admission checks.** Every input must pass CP-15's five admission checks
>      (`reports/cp15/feasibility/structural_inputs.md`). They require, for both research and the
>      final product's daily operation:
>      - a licence;
>      - an `available_at` vintage;
>      - missingness;
>      - an imputation rule;
>      - coverage from 2019 with redistribution rights.
>    - **Desk research first.** Any retrieval or purchase is the Owner's decision. Admitted inputs
>      then go to a pre-registered ablation checkpoint.
> 4. **4.8, recombination with a meta-learner.**
>    - **The candidate.** A small NumPy network, on DDNN's infrastructure, that predicts each
>      member's weight from regime features.
>    - **How it learns.** Walk-forward only: at each origin it learns from released errors and
>      features available then, and its design is frozen before scoring.
>    - **What it faces,** under a pre-registered rule:
>      - the fixed weights;
>      - per-block weights, which the Owner filed on 2026-10-04;
>      - weights from recent errors.
>    - **Disclosed in advance.** The Orchestrator's hindsight bound for the LightGBM weight is
>      known: per block −0.8% and per fold and block −1.6% pooled central MAE. It is an oracle, not
>      selectable.
> 5. **4.7T,** then CP-17–CP-19.
>
> **Binding reminders:**
>
> - **Before the next publication's brief is issued,** the Orchestrator brings automation items 6
>   (post-deploy publication receipt) and 7 (pre-review check runner) to the Owner for a decision.
>   The brief waits for that decision.
> - **Before CP-18's daily pipeline,** which handles credentials every day, the Orchestrator brings
>   back the security items of the archived proposal `archive/deterministic-migration-plan-20261001`:
>   - a value-free leak scan;
>   - a lint for bare environment reads;
>   - GitHub rulesets.

**The final-product Space plan `docs/track-b/final-product-space-plan-2026-09-30.md` §7 (steps 4 and 6 bind the pipeline here; step 5 is CP-18b's)** (the file `ad3568c8997a08aa291bd3a7f29046c24ce61f0c1fd992622f921b5d23f9174c`; the section 50 lines, 2648 bytes, SHA-256 `e753f5d23807d7d6ba33669471957f4fa8811f0dfe6eb529c9fc02f83e6a8f0b`):

> ## 7. Automatic execution at the final-product rollout
>
> Nothing here needs a new decision later, beyond §5.1's open items. The anchors make the Space a
> required part of the final product's rollout: research §16 and §19 bind CP-17 and CP-18, and
> publication A8 and A9 bind the release. Every future brief pins both.
>
> **The checklist the CP-17 and CP-18 briefs carry:**
>
> 1. **Designation (Owner).** Record the final version. Its evidence class and product identity
>    drive every Space label.
> 2. **Feasibility probe (CP-17, before the freeze).** Train one delivery day of the designated
>    policy under Pyodide in Chromium and WebKit, on development data only. Measure:
>    - time and peak memory;
>    - the first-visit and training-payload sizes;
>    - the deviation from the native fit, bitwise or not;
>    - whether the selections match.
>
>    If this is infeasible, return a blocker for the Owner's §19.3 decision. This can also run
>    earlier, as a bounded probe with its own brief, to de-risk the button.
> 3. **Freeze (CP-17):**
>    - τ (Owner), the percentage formula, denominator and partial-day rule, and zero or negative
>      handling;
>    - the rolling window lengths, the PIT and diagram definitions, and the recomputation
>      tolerance;
>    - τ_eq (Owner) and the reference browser and runtime;
>    - the attribution method for any neural component;
>    - the payload schema and manifest.
> 4. **Daily pipeline (CP-18):**
>    - acquire, validate, fit and issue before the gate;
>    - build the dated bundle and verify it (hashes, schema, recomputation rows);
>    - publish it to the Space and verify the served identity;
>    - reconcile outcomes later and update the records.
>
>    Failures and staleness stay visible, and every delivery day is covered, including DST days. This needs the Owner's `AGENTS.md` authority first.
> 5. **Space build (CP-18):** §4's views under A9, from the payload only, with the History route
>    for v1.
> 6. **Tests (CP-18):**
>    - an extended `test_24` (the live namespace);
>    - a live claim builder;
>    - payload contract tests;
>    - negative controls: a tampered file is detected; a pending outcome stays unscored; a stale
>      artifact is shown as stale; a mismatched recomputation shows ✗ and blocks publication; a
>      retrain with a changed seed is reported as different; a counterfactual is never labelled
>      issued.
> 7. **Review and release:** the independent exact-candidate review; the packet with §5d and A9
>    rows; the Owner-authorized launch; public A6 checks of every view.
> 8. **Operation:** "prospective evaluation in progress" until CP-19 closes after at least 90
>    consecutive delivery days.
>
> ---

**Further items,** which bind this candidate as well:

1. **Blind.** The boundary stays at 2026-09-06. No byte dated after it is downloaded, read or inferred,
   on this machine or on a runner. No 4.7T forecast and no live forecast is produced.
2. **GitHub-landable as is.** No committed file is over 50 MB.
3. **CI-ready.** The workflow's seven steps are green on a history-free single-commit copy, with
   `CI=true` and Python 3.12, and `pytest -m stress` passes locally. If item 7 adds the leak scan as the
   first CI step, it is green there too.
   - No test depends on branch history, tags or local-only inputs.
   - Tests over real stored inputs, runtimes or GitHub skip with a stated reason when those are absent.
4. **What never changes:**
   - `src/cp17/` and `src/cp17c/`, and every checkpoint's reports and evidence;
   - the landed code in `src/delu_forecast/`, `src/cp15/` to `src/cp28/`, `src/cp17probe/` and
     `src/cp17cprobe/`;
   - `data/`, `reports/development-inputs/`, the root `pyproject.toml` and `uv.lock`;
   - the anchors and amendment records, the decisions records, `AGENTS.md`, the role files, the exposure
     ledger and the backup register.

   Before editing any tracked file, check that no earlier evidence binds its bytes. That includes
   `src/cp26/harness.py`'s `PINS`, and every freeze manifest's governance pins. `refreeze verify` on
   CP-17c's manifest prints `verified` at the final candidate.
5. **The Integration Critic** reruns, locally:
   - the suite in the history-free `CI=true` Python 3.12 sequence, and `pytest -m stress`;
   - one dry run of the pipeline on a development day, through the H2 gate;
   - the claim's race test, and one forced cause of each not-issued kind;
   - the live builder's byte equality at one parity origin;
   - the leak scan and the environment lint against their fake fixtures.

   It recomputes every runner comparison from the downloaded results, verified by their hashes. It runs
   nothing on GitHub.

## Task-specific supporting extract
- **The public scratch repository:** one new public repository, `hrsi56/delu-pipeline-dryrun`, created
  for this round.
  - **Why public.** Under decision 26, a scratch repository's Git is not a publication, and standard
    runners on public repositories are free. It has no Pages site.
  - **Before its first push, and before every later one,** run the value-based secret scan over
    everything outgoing (`scripts/secret_guard.py` via the hooks).
  - **It holds only what the runs need:**
    - the package's files, the pipeline and the workflow;
    - A1's `k13.json`, the freeze-origin states and the canary payload;
    - development payloads or their inputs.

    No data dated after 2026-09-06.
  - **It creates no secret and no variable.** Fake credentials are test fixtures in code, never secrets.
  - **It is left in place after the return.** The return names it.
- **Retrieval, authorized for software only:**
  - Node.js v26.7.0's official darwin-arm64 tarball and `SHASUMS256.txt`, and Pyodide 0.28.0's files,
    verified against CP-17c's hashes;
  - **on the runners:** `uv` and the Python packages `uv.lock` pins; the pinned CPython; GitHub's own
    actions, pinned by commit SHA.

  Record each URL, the version, the bytes and the SHA-256. Make no other network contact, and no data
  retrieval.
- **The ceilings:**
  - **Local:** 10 machine-hours, summed over workers' wall time. At most 4 concurrent workers, BLAS 1 for
    native fits, CPU only, peak memory 12 GB, no GPU.
  - **GitHub:** standard hosted `macos-26` runners in the public scratch repository only, no larger
    runners and no private repository. At most 15 job-hours in all, and each job's `timeout-minutes` set.
  - Keep a ledger, and stop before a ceiling.
- **"Frozen"** keeps §16.2's meaning. The pipeline is new code around the frozen package. It is reviewed
  here, and changes later only through a checkpoint.

## Applicable constraints
- **The red line (§24.2).** No delivery day after 2026-09-06 is read, recorded or mentioned, except as
  a protocol or calendar date.
- **Homebrew's `node` stays pinned and installed.** Never upgrade, unpin or remove it.
- **Credentials** follow `AGENTS.md` § Credentials.
  - No real credential is needed in this round, and no secret is created anywhere.
  - Never print, log or echo an environment variable's value.
  - Export `MLFLOW_DISABLE_TELEMETRY=true` and `DO_NOT_TRACK=1`. Any MLflow use in this round is a local
    file store.
- **Allowed paths:**
  - `src/cp18/`, `tests/cp18a/`, `reports/cp18a/` and `docs/track-b/evidence/cp-18a/`;
  - `scripts/leak_scan.py` and `scripts/credential_fingerprints.py`;
  - `.githooks/` (the leak-scan calls only);
  - `.github/workflows/daily.yml` (new);
  - `.github/workflows/tests.yml` (the leak-scan step only);
  - `pytest.ini` (the plugin registration only, as item 7 says);
  - `tests/environ_redact.py` and the environment-access lint test.

  Nothing under `src/cp17/` or `src/cp17c/`, and no anchor or governance file.
- **Long computation** may run unattended in the background, within the ceilings, under your ledger.
  Commit work in progress on `gauntlet/cp-18a` at every stage boundary.
- **Tools:**
  1. run `scripts/gauntlet.py start cp-18a` first, from the primary checkout;
  2. create the worktree with
     `git -C /Users/djourno/Downloads/PJM worktree add -b gauntlet/cp-18a .local/worktrees/cp-18a/lead main`;
  3. run one Critic, through `critic-open`, `critic-brief` and `critic-close`. **The first line of the
     Critic's launch assignment** forbids opening the Claude memory directory;
  4. check the return with `scripts/gauntlet.py return`.
- **Memory:** do not open or edit the files in the Claude memory directory
  (`~/.claude/projects/-Users-djourno-Downloads-PJM/memory/`).
- **Owner-facing Git commands** must be non-interactive.

## Timebox
About 16 active hours from orientation to the terminal return.

## Owner-only actions already authorized
- **CP-18a's execution** under decisions 7, 25, 26 and 27 and this brief. The Orchestrator delivers this
  brief under the Owner's grant, and that delivery is the grant. It covers:
  - creating the public scratch repository `hrsi56/delu-pipeline-dryrun`, pushing to it, and running its
    workflows within the GitHub ceiling;
  - the software retrievals above, and the local ceiling;
  - local `gauntlet/cp-18a` commits and the brief's packaging.
- **Nothing else:**
  - no push, branch or tag on `origin`;
  - no secret;
  - no data retrieval;
  - no 4.7T run;
  - no boundary move;
  - no anchor or governance edit;
  - no publication;
  - no mainline operation;
  - no `launchd` installation;
  - no ruleset applied.

## Stop and return
- **First commit.** The first commit copies the canonical brief byte for byte to
  `docs/track-b/evidence/cp-18a/issued-brief.md`.
- **Questions.** If the brief is unclear or wrong, ask the Orchestrator before repository work, or stop
  at the conflict. The anchor and the Owner's decisions prevail over this brief.
- **The return.** Return exactly one of PASS / BLOCKED / INCOMPLETE, using templates §3, with both
  terminal SHAs and the verdict-only delta, checked with `scripts/gauntlet.py return`.
  - **Its "Open risk or exact owner action" section** gives item 8's table and the secret names.
  - Name the scratch repository and the job-hours used.
  - Name any exposure (§24.2), and any interview-answer trigger, in one line each.
- **Do not** open 4.7T, build the Space, or activate anything. Leave your worktree and branch for the
  LAND.
