# Track B Checkpoint Brief — CP-17c-probe (can a GitHub-hosted runner be the issuing host?)

*Issued by the Orchestrator on 2026-10-30, Asia/Jerusalem.*

## Target
- Repository: DE-LU day-ahead forecasting, `/Users/djourno/Downloads/PJM` (origin
  `hrsi56/delu-day-ahead-forecast`). The checkpoint runs locally, in the Lead's own worktree, plus
  runs on GitHub-hosted runners in one new private scratch repository (below).
- Authorized checkpoint: CP-17c-probe, exactly one. It is the probe of the Owner's decision 24.
- **Why.** A1's frozen issuing host is the pinned Pyodide in the pinned Node.js binary on the Owner's
  Mac. The Owner wants the daily pipeline to run on GitHub Actions instead. The anchor makes any other
  binary or machine a runtime change, so a re-freeze (CP-17c) and an anchor amendment (r19) must pin
  the new host before 4.7T opens. This probe measures whether a hosted runner reproduces the frozen
  host, so the Orchestrator can choose the host.
- Ratified plan anchor: `capstone_v21.md`, revision v21-r18, SHA-256
  `9caf83393a08df6851f7e829722583a142ebc2354ee99a3bbaa015d929f3d401`. §24.12 defines the frozen policy
  and its issuing host.
- The Owner's decisions 22–25 are in `docs/track-b/owner-decisions-2026-10-30.md` (SHA-256
  `1286548362b5618e3fb01c616d673c0af83dd79effeaf102bb9727ac219aabab`). Decision 24 is this probe's mandate.

## Orchestrator-reported expected state
- **Branch / commit:** `main` = `origin/main` at the commit that records this probe's issue.
  - It is a direct child of `782a1979f0914facd5954dd03e569ce86a55ac32`. It adds
    `docs/track-b/owner-decisions-2026-10-30.md` and changes `progress.md`.
  - **Tags:** `evidence/cp-26` is local-only and never pushed. `land/cp-17b` = `095578cb…` and
    `evidence/cp-17b` are pushed, with CP-17's and CP-17-probe's.
  - **Branches and worktrees:** none besides `main` and the primary checkout.
- **Working tree:** the primary checkout is on `main` and clean apart from ignored material.
  - **The Orchestrator uses it.** Never switch its branch, and never write a tracked file in it.
    Your only writes there are under `.local/artifacts/cp-17c-probe/`, `.local/tmp/cp-17c-probe/`,
    `.local/tools/` (the pinned binaries below) and the worktrees under
    `.local/worktrees/cp-17c-probe/`.
  - **The canonical brief** is `.local/artifacts/cp-17c-probe/issued-brief.md`. Package that file
    byte for byte.
- **What already exists:**
  - **The frozen package** `src/cp17/` and CP-17b's freeze manifest
    `docs/track-b/evidence/cp-17b/freeze-manifest.json` (policy identity `439115fb…`), with
    `python -m cp17.tools.refreeze verify` as its check.
  - **The frozen host on this machine:** Node.js v26.7.0 at
    `/opt/homebrew/Cellar/node/26.7.0/bin/node`, pinned in Homebrew since 2026-10-30; Pyodide 0.28.0
    in `.local/tools/pyodide-0.28.0/`.
  - **The references the runners are compared against,** all produced under the frozen host:
    - `reports/cp17b/shadow-run.json`: 14 consecutive delivery days, 2026-08-24 to 2026-09-06, A1
      with the three shadows (v4, v2, B0) and their buffers;
    - `reports/cp17b/host-parity.json`: the issuing host's parity origins, including the DST day
      2025-10-26 and 2026-03-29;
    - `reports/cp17b/f1-2026-03-30.json`: the day where the host differs most from native arithmetic.
  - **Development data** to 2026-09-06, as CP-17b used it to build payloads.
  - **GitHub:** `gh` is authenticated as `hrsi56`, with the `repo` and `workflow` scopes. The scratch
    repository does not exist yet.
- Verify this yourself before relying on it, and report any material mismatch.

## Observable outcome
A final candidate on `gauntlet/cp-17c-probe`, bound by one fresh focused Integration-Critic PASS,
with the following.

1. **The runner measurement.** On a standard GitHub-hosted **Linux x64** runner and a standard
   GitHub-hosted **macOS Apple-silicon** runner, each named by its image label, with its image
   version, CPU, cores and memory recorded.
   - **What runs:** the frozen daily chain, `cp17.daily`, with the frozen package, the pinned Pyodide
     files, and the official Node.js v26.7.0 binary for that platform in place of Homebrew's. The
     CPython side runs in the environment `uv.lock` pins.
   - **The days,** in this priority if the minute cap below forces a subset on macOS:
     1. the issuing-host parity origins of `host-parity.json`, for every policy it records;
     2. F1's day, 2026-03-30;
     3. the 14 days of `shadow-run.json`, with the shadows and their buffers, latest days first.
   - **Recorded, per runner, day and policy:**
     - whether the issued quantiles are bit-identical to the reference, by their SHA-256;
     - if they are not, the largest absolute difference per emitted quantile, in EUR/MWh, and whether
       every data-driven selection matched;
     - the buffers' SHA-256 against the reference;
     - wall time and peak memory, measured as the success definition measures them, against its
       15 minutes and 4 GB;
     - that each payload's identity equals the one the reference used.
2. **A local control on this machine.** The official darwin-arm64 Node.js v26.7.0 binary in place of
   Homebrew's, on the parity origins and F1's day. It separates the effect of the binary from the
   effect of the machine.
3. **Proposals for the Orchestrator,** each with its reasoning:
   - **which runner passes cleanly,** if any: bit-identical on every day and policy, within the
     ceilings. If both do, compare them on time, memory and stability;
   - **what CP-17c must re-freeze** for that runner: the pinned binary and how it is retrieved, the
     host's identity, where `refreeze verify` runs, and how a daily run checks its runtime before it
     issues;
   - **the daily cost** on that runner per issuance, and for decision 23's bound of four issuances per
     run;
   - **an estimate, not a run,** of whether DDNN-2's next search, S_14 on 2027-01-06, fits a hosted
     runner's job limits.
4. **If no runner reproduces the frozen host,** the probe still returns PASS with the numbers. The
   result is a finding, not a failure. Return BLOCKED only if the measurement itself cannot be made,
   for example a GitHub quota or access refusal, with what was measured.

## Complete authoritative checkpoint bar
`capstone_v21.md` v21-r18 §24.12, the frozen policy's host, its resources and its runtime rule, as the
measurement standard. Verbatim, from the anchor at `782a1979`:

> | The issuing host | Pyodide 0.28.0, by its 23 pinned file hashes, in the pinned Node.js v26.7.0 binary (`1ef99ea25fe70c9b67e7efe768ef8ee22148d3cabc703db6131b57aeb617d040`), one worker (decision 10). The chain's judgement and the shadow states run in CPython inside `cp17.daily`, from the package's own files, in the environment `uv.lock` pins |
> | The reference runtime (§19.3) | the issuing host, plus Chromium 153.0.8010.12 and WebKit 26.6 through Playwright 1.63.0, on the Apple M3 machine class (8 cores, 16 GB, macOS 26.5.2) |
> 
> **"Frozen"** keeps §16.2's meaning. Any change to the policy, its code, its runtime or its state needs
> a new freeze and a new evaluation. Daily fitting changes weights and state within the frozen policy,
> and is not a change to it.
> 
> 5. **Resources.** One worker under the issuing host, at most 15 minutes of wall time and 4 GB of peak
>    memory, measured in the attempt's own process. An issued artifact always carries its measurement
>    (N2).
> 
>   - **where the pipeline runs.** The issuing host is the pinned files above. Any other binary or
>     machine is a runtime change, which needs a new freeze and a new evaluation (§16.2);

**The Owner's mandate,** decision 24 of `docs/track-b/owner-decisions-2026-10-30.md`, quoted:

> 24. **The issuing host may move to a GitHub-hosted runner.**
>     - **A probe first, CP-17c-probe,** on development data only: on a Linux x64 runner and on a macOS
>       Apple-silicon runner, it checks whether the daily fit reproduces the frozen issuing host bit for
>       bit, for A1 and the three shadows, within the frozen time and memory ceilings.
>     - **If a runner passes cleanly,** the Orchestrator chooses between Linux and macOS. r19 and a short
>       re-freeze, CP-17c, then pin that host before 4.7T opens.
>     - **If neither passes cleanly,** the Owner's Mac stays the issuing host. Any other outcome is a new
>       decision, brought to the Owner.
>     - **Until then** the frozen host is unchanged. Homebrew's `node` is pinned on the Owner's machine
>       (2026-10-30), so an upgrade cannot replace the pinned binary.

**Further items,** which bind this candidate as well:

1. **Development data only.** No delivery day after 2026-09-06 is read, on this machine or on a
   runner.
2. **Retrieval is software only,** as listed below. No data is retrieved from any source.
3. **GitHub-landable and CI-ready.**
   - No committed file is over 50 MB.
   - The workflow's seven steps are green on a history-free single-commit copy, with `CI=true` and
     Python 3.12.
   - **Tests that need the runtimes or GitHub** skip with a stated reason when those are absent, as
     they are on CI. **Timing-sensitive tests** carry the `stress` marker.
4. **No pinned file and no landed code changes.** New code lives under new paths only:
   `src/cp17cprobe/` or a `tools/` subfolder, `tests/` (new files), `reports/cp17c-probe/` and
   `docs/track-b/evidence/cp-17c-probe/`. **Nothing is added under `.github/`** in this repository:
   the scratch repository's workflow file is kept under the new paths, so landing it never triggers a
   run here.
5. **The Integration Critic** reruns one local-control day and the whole suite in that CI mode, and
   recomputes every comparison from the runners' downloaded results, verified by their hashes. The
   Critic runs nothing on GitHub.

## Task-specific supporting extract
- **The scratch repository:** one new **private** repository, `hrsi56/delu-host-probe`, created for
  this probe.
  - **It holds only what the runs need:** the frozen package's files, the harness, the workflow, and
    payloads or their inputs, all for development days.
  - **It is never made public.** It creates no secret, and its workflow token is read-only apart from
    what uploading results needs.
  - **It is left in place after the return.** Deleting it is the Owner's, and the return names it.
- **Retrieval, authorized for software only:**
  - **Node.js v26.7.0,** the official `linux-x64` and `darwin-arm64` tarballs from
    `https://nodejs.org/dist/v26.7.0/`, each verified against that folder's `SHASUMS256.txt`;
  - **on the runners:** Pyodide 0.28.0's 23 files from its official CDN, or uploaded from
    `.local/tools/pyodide-0.28.0/`, either way verified against the freeze manifest's hashes; `uv`
    and the Python packages `uv.lock` pins; GitHub's own actions, pinned by commit SHA.
  - Record each URL, the version, the bytes and the SHA-256. Make no other network contact.
- **The ceilings:**
  - **Local:** 3 machine-hours, at most 4 workers, BLAS 1 for native work, peak memory 12 GB.
  - **GitHub:** standard hosted runners only, no larger runners. At most 1,500 minutes as GitHub's
    usage report counts them for a private repository, macOS minutes at GitHub's own rate. No paid
    usage: a quota or billing refusal stops the runs.

## Applicable constraints
- **The red line (§24.2):** no delivery day after 2026-09-06 is read, recorded or mentioned.
- **Files that never change:**
  - the frozen package `src/cp17/`, the freeze manifests and every file a freeze or earlier evidence
    binds;
  - `data/`, `reports/` of earlier checkpoints, and the landed code in `src/delu_forecast/` and
    `src/cp15/` to `src/cp28/`;
  - the root `pyproject.toml` and `uv.lock`. Runtimes live under `.local/tools/`, not in the lock;
  - `.github/`, the anchors and amendment records, `AGENTS.md`, the role files, the exposure ledger
    and the backup register.
- **Homebrew's `node` stays pinned and installed.** Never upgrade, unpin or remove it.
- **Credentials** follow `AGENTS.md` § Credentials; none is needed, and no secret is created anywhere.
  Export `MLFLOW_DISABLE_TELEMETRY=true` and `DO_NOT_TRACK=1`.
- **Tools:**
  1. run `scripts/gauntlet.py start cp-17c-probe` first, from the primary checkout;
  2. create the worktree with
     `git -C /Users/djourno/Downloads/PJM worktree add -b gauntlet/cp-17c-probe .local/worktrees/cp-17c-probe/lead main`;
  3. run one focused Critic, through `critic-open`, `critic-brief` and `critic-close`;
  4. check the return with `scripts/gauntlet.py return`.
- **Memory:** do not open or edit the files in the Claude memory directory
  (`~/.claude/projects/-Users-djourno-Downloads-PJM/memory/`).
- **Owner-facing Git commands** must be non-interactive.

## Timebox
About 6 active hours from orientation to the terminal return.

## Owner-only actions already authorized
- **This probe** (decisions 24 and 25), including:
  - creating the private scratch repository `hrsi56/delu-host-probe`, pushing to it, and running its
    workflows within the GitHub ceiling above;
  - the software retrievals above, and the local ceiling;
  - local `gauntlet/cp-17c-probe` commits and the brief's packaging.
- **Nothing else:** no push, branch or tag on `origin`; no secret; no data retrieval; no re-freeze;
  no anchor edit; no 4.7T; no publication; no mainline operation.

## Stop and return
- **First commit.** The first commit copies the canonical brief byte for byte to
  `docs/track-b/evidence/cp-17c-probe/issued-brief.md`.
- **The return.** Return exactly one of PASS / BLOCKED / INCOMPLETE, using templates §3, with both
  terminal SHAs and the verdict-only delta.
  - Its "Open risk or exact owner action" section gives the measurements per runner and the
    proposals for the host choice and CP-17c.
  - Name the scratch repository and the GitHub minutes used.
  - Name any interview-answer trigger in one line.
- **Do not** begin CP-17c. Leave your worktree and branch for the LAND.
