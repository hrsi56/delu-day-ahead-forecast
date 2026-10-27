# Track B Checkpoint Brief — CP-17-probe (the in-browser feasibility probe for A1, before the freeze)

*Issued by the Orchestrator on 2026-10-27, Asia/Jerusalem.*

## Target
- Repository: DE-LU day-ahead forecasting, `/Users/djourno/Downloads/PJM` (origin
  `hrsi56/delu-day-ahead-forecast`). The checkpoint runs locally, in the Lead's own worktree.
- Authorized checkpoint: CP-17-probe, exactly one. It is the bounded feasibility probe that the
  Space plan allows to run before CP-17 with its own brief
  (`docs/track-b/final-product-space-plan-2026-09-30.md` §7, step 2; SHA-256
  `ad3568c8997a08aa291bd3a7f29046c24ce61f0c1fd992622f921b5d23f9174c`).
- **Why it comes first.** CP-17's first brief (`64758101…`) left out §19's freeze fields. The Lead
  validated it and stopped before any repository work. This probe supplies the measurement that
  §19.3 item 4 requires before the freeze. CP-17 is then reissued with τ_eq, the reference runtime
  and the §19.7 method fixed.
- Ratified plan anchor: `capstone_v21.md`, revision v21-r17, SHA-256
  `3124451da84c3cd99fae728c371207aace6ae537474f7769d0ff6333ee53e4fc`.
  - §19 binds the CP-17 and CP-18 briefs. §24.1 keeps it in force, and §24 does not touch it.
  - The bar is §19.3 item 4 (with items 1, 2 and 5) and §19.2, quoted below.
  - The Owner's decisions before CP-17 are in `docs/track-b/pre-cp-17-rulings-2026-10-25.md`
    (`22341d752dcd903f05f3c6dcfde7ceec2c6c8940e053650018a7a4c5d36800b7`). The designated policy is A1,
    DDNN-2 alone, and the fallback is v2.

## Orchestrator-reported expected state
- **Branch / commit:** `main` = `origin/main` at the commit that records this probe's issue.
  - It is a direct child of `c81f685a6cee86f24cb03b6dd52a2ad2c0c21751`, and changes only
    `progress.md`.
  - **Tags:** `evidence/cp-26` = `ca20331` is local-only and never pushed. `land/cp-28` and
    `evidence/cp-28` are pushed.
  - **Branches and worktrees:** none besides `main` and the primary checkout.
- **Working tree:** the primary checkout is on `main` and clean apart from ignored material.
  - **The Orchestrator uses it.** Never switch its branch, and never write a tracked file in it.
    Your only writes there are under `.local/artifacts/cp-17-probe/`, `.local/tmp/cp-17-probe/`,
    `.local/tools/` (the pinned runtimes below) and the worktrees under
    `.local/worktrees/cp-17-probe/`.
  - **The canonical brief** is `.local/artifacts/cp-17-probe/issued-brief.md`. Package that file byte
    for byte.
- **What already exists:**
  - **A1's code and state:**
    - the landed DDNN-2 code, `src/cp24/`;
    - CP-26's harness, `src/cp26/`, whose live guards refuse under r17, so never call them;
    - CP-26's stored fits, searches and state in `.local/artifacts/cp-26/cold-rerun-2026-10-15/`;
    - search results and plans, and the forecast ledger, in the local-only tag `evidence/cp-26`.
      Extract what you need read-only with `git archive`, into `.local/artifacts/cp-17-probe/inputs/`.
  - **v2's code:** `src/cp16/`, which rests on `src/cp15/`.
  - **Development data** to 2026-09-06: `data/snapshot.parquet`, CP-25's
    `reports/development-inputs/`, and CP-20's committed weather features.
  - **The browser runtimes on this machine:**
    - Playwright, with its WebKit build (`webkit-2359`), in `.local/tools/playwright/` and
      `.local/tools/ms-playwright/`;
    - **no** Chromium build;
    - **no** Pyodide.
- Verify this yourself before relying on it, and report any material mismatch.

## Observable outcome
A final candidate on `gauntlet/cp-17-probe`, bound by one fresh focused Integration-Critic PASS,
with the following.

1. **The measurement,** under Pyodide in Chromium and WebKit.
   - **What it does:** retrain the daily fit of A1 (CP-26's nominal D2, as CP-28 selected it) for two
     development delivery days. Each uses that fit's training window, code, seed and selection rules,
     then predicts the day's quantiles.
   - **The two days:** delivery 2026-09-06, and the DST delivery day 2026-03-29.
   - **What is recorded, per browser and day:**
     - wall time and peak memory;
     - the first-visit payload size and the training payload's size;
     - the largest absolute difference per emitted quantile against the native fit, in EUR/MWh, and
       whether the result is bitwise identical;
     - whether every data-driven selection matched.
   - **The same for v2,** the fallback that issues on GFS-late days, for one day.
2. **The native reference.** The same two A1 fits and one v2 fit run natively. They reproduce
   CP-26's stored forecasts for those days to CP-26's recorded parity standard. The browser fits are
   compared against these native fits.
3. **Proposals for the Owner and for CP-17,** each with its reasoning:
   - **τ_eq,** the equality tolerance (§19.3 item 2). It is the Owner's, set from this measurement. If
     the fits are bitwise identical, say so; the status is then "identical".
   - **the reference browser and runtime:** browser versions, the Pyodide version, the machine class,
     and the time and memory limits a visitor is told about;
   - **the attribution method for A1,** a neural component (§19.7), with its in-browser cost;
   - **the one-code-path design** (§19.2): how the daily-fit module is laid out, so that the native
     pipeline and the browser run the same code, and what CP-17 must freeze for that.
4. **The blocker route** (§19.3 item 5). If A1's browser retrain is infeasible within limits a
   visitor can meet, or its selections do not match, return BLOCKED with the numbers. Do not drop or
   replace the requirement.

## Complete authoritative checkpoint bar
`capstone_v21.md` v21-r17 §19.3, item 4, together with items 1, 2 and 5, and §19.2, for the
designated policy A1. Verbatim, extracted with `scripts/bar.py bar` from the anchor at `c81f685`:

> ### 19.2 One code path
>
> The code that performs the daily fit, issuance and scoring is the code the Space runs in the
> browser for §19.3 and §19.5. No second implementation stands in for the product. A component
> that cannot run in the browser runtime is reported at CP-17 under §19.3's exception route; it is
> never replaced silently.

> ### 19.3 "Train it yourself" is required
>
> The Owner requires an in-browser retraining action for the final product.
>
> 1. **What it does.** In the visitor's browser, it retrains the daily fit of one issued delivery
>    day from that fit's shipped training window, with the same code, seed and selection rules.
>    It then predicts that day's quantiles.
> 2. **What it reports.**
>    - whether every data-driven selection matched the issued artifact;
>    - the largest absolute difference per emitted quantile, in EUR/MWh;
>    - one status that states only what was measured: identical bit for bit, within the frozen
>      tolerance τ_eq, or different.
> 3. **What it never does.** It never replaces, rescores or relabels an issued forecast.
> 4. **The probe.** Before the CP-17 freeze, a feasibility probe on development data measures, for
>    the designated policy:
>    - browser time and memory;
>    - payload sizes;
>    - the deviation from the native fit;
>    - selection agreement.
>
>    CP-17 freezes τ_eq and the reference runtime from that measurement.
> 5. **If the policy cannot meet this requirement** within the measured limits, CP-17 returns a
>    blocker. Only an explicit Owner exception, with its public wording, lets the product ship
>    without the action. The requirement is never dropped silently, and never met by retraining a
>    different implementation.

**Further items,** which bind this candidate as well:

1. **Development data only.** No delivery day after 2026-09-06 is read.
2. **Software retrieval is limited to the two pinned runtimes below.** No data is retrieved.
3. **GitHub-landable and CI-ready.**
   - No committed file is over 50 MB.
   - The workflow's seven steps are green on a history-free single-commit copy, with `CI=true` and
     Python 3.12.
   - **Browser tests** skip with a stated reason when the runtimes are absent, as they are on CI.
   - **Timing-sensitive tests** carry the `stress` marker.
4. **No pinned file and no landed code changes.** New code lives under new paths only:
   `src/cp17probe/` or a `tools/` subfolder, `tests/` (new files), `reports/cp17-probe/` and
   `docs/track-b/evidence/cp-17-probe/`.
5. **The Integration Critic** reruns one browser measurement and the whole suite in that CI mode.

## Task-specific supporting extract
- **Retrieval, authorized for software only:**
  - **Pyodide,** one pinned release from its official distribution (the GitHub release or the
    official CDN), in a version whose NumPy build matches what A1 needs;
  - **Playwright's Chromium build,** matching the installed Playwright, installed with Playwright's
    own installer into `.local/tools/`.
  - Record each URL, the version, the bytes and the SHA-256. Install nothing else, and make no other
    network contact.
- **The ceiling:**
  - 5 machine-hours, at most 4 workers;
  - BLAS 1 for the native fits;
  - peak memory 12 GB;
  - no cloud and no GPU.

## Applicable constraints
- **The red line (§24.2):** no delivery day after 2026-09-06 is read, recorded or mentioned.
- **Files that never change:**
  - `data/`, `reports/` of earlier checkpoints, and every file that earlier evidence binds;
  - the landed code in `src/delu_forecast/` and `src/cp15/` to `src/cp28/`;
  - the root `pyproject.toml` and `uv.lock`. Runtimes live under `.local/tools/`, not in the lock;
  - the anchors and amendment records, `AGENTS.md`, the role files, the exposure ledger and the
    backup register.
- **Credentials** follow `AGENTS.md` § Credentials; none is needed. Export
  `MLFLOW_DISABLE_TELEMETRY=true` and `DO_NOT_TRACK=1`.
- **Tools:**
  1. run `scripts/gauntlet.py start cp-17-probe` first, from the primary checkout;
  2. create the worktree with
     `git -C /Users/djourno/Downloads/PJM worktree add -b gauntlet/cp-17-probe .local/worktrees/cp-17-probe/lead main`;
  3. run one focused Critic, through `critic-open`, `critic-brief` and `critic-close`;
  4. check the return with `scripts/gauntlet.py return`.
- **Memory:** do not open or edit the files in the Claude memory directory
  (`~/.claude/projects/-Users-djourno-Downloads-PJM/memory/`).
- **Owner-facing Git commands** must be non-interactive.

## Timebox
About 6 active hours from orientation to the terminal return.

## Owner-only actions already authorized
- **This probe,** including the two pinned software retrievals above, and the 5-machine-hour
  ceiling. The Owner's delivery of this brief is his grant. It covers local `gauntlet/cp-17-probe`
  commits and the brief's packaging.
- **Nothing else:** no data retrieval, no freeze, no 4.7T, no mainline operation, no push or tag,
  no publication, and no anchor edit.

## Stop and return
- **First commit.** The first commit copies the canonical brief byte for byte to
  `docs/track-b/evidence/cp-17-probe/issued-brief.md`.
- **The return.** Return exactly one of PASS / BLOCKED / INCOMPLETE, using templates §3, with both
  terminal SHAs and the verdict-only delta.
  - Its "Open risk or exact owner action" section gives the measurements and the four proposals for
    the Owner's τ_eq decision and for CP-17's reissue.
  - Name any interview-answer trigger in one line.
- **Do not** begin CP-17. Leave your worktree and branch for the LAND.
