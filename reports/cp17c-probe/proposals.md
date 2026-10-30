## The result

**Both runners reproduce the frozen issuing host bit for bit, on every fit measured, within the frozen ceilings.**

- **What ran.** CP-17b's own reference fits:
  - A1 at the nine issuing-host parity origins, and v4, v2 and B0 at two of them;
  - all four policies on F1's day, 2026-03-30;
  - the 14 consecutive shadow days, with the shadow states carried by each runner.

  Each fit ran in a fresh process of `cp17.daily`, with the frozen package's zip, Pyodide 0.28.0's 23 pinned files,
  and the official Node.js v26.7.0 binary for the platform in place of Homebrew's. Every payload's identity equals
  the one the reference used.
- **`ubuntu-24.04` (Linux x64, AMD EPYC 7763, 2 vCPU):**
  - 75 of 75 fits bit-identical;
  - the buffers equal the reference's at all 14 origins, and the final state equals it;
  - the slowest attempt took 284.6 s, and the largest peak was 844 MiB.
- **`macos-26` (Apple M2 Pro, virtual, 5 cores):**
  - 75 of 75 fits bit-identical;
  - the same buffers and final state;
  - the slowest attempt took 228.9 s, and the largest peak was 917 MiB.
- **The local control.** The official darwin-arm64 binary on this M3 reproduced all 19 parity and F1 fits bit for
  bit, twice. Its SHA-256 is `a9bd0630…`, where Homebrew's is `1ef99ea2…`.
  - This is the same binary the `macos-26` jobs ran. Neither the binary nor the machine moved a single bit.
- **The supplementary records.** Run 1's harness failed after each fit, but the 14 records it left are the frozen
  runner's own. All 14 are bit-identical too, including 10 on a different Linux CPU (AMD EPYC 9V45).
- **What it means.** No selection differed and no quantile moved, so τ_eq and F1 are untouched: every retrain
  status reads "identical bit for bit".
- **Cost of the probe.** It used **863 GitHub minutes** as a private repository counts them (macOS at ten times),
  of the 1,500 allowed.
- **The scratch repository, `hrsi56/delu-host-probe`,** is left in place, and deleting it is the Owner's decision.
  As `scratch-repository.json` records, it is private, holds no secret or variable, and gives workflow tokens read
  access by default (its workflow asks for `contents: read` only). Its two commits are the inputs the runs used.

## Proposal 1 — the runner: `ubuntu-24.04` (Linux x64)

Both pass cleanly, so the choice is the Orchestrator's (decision 24). I propose Linux:

- **Reproduction is equal.** Both runners reproduce every fit. Linux did so on two CPU generations (EPYC 7763 and
  EPYC 9V45), the more demanding evidence that its result does not depend on the machine it lands on.
- **Time.** Linux is slower but far inside the ceiling:
  - One issuance (A1 and the three shadows, one after another) took 349–366 s on Linux, against 270–284 s on macOS
    and 197–212 s on this M3.
  - The slowest single attempt, 284.6 s, is 32% of the 900 s ceiling.
  - Linux's speed depends on the CPU it lands on. A1 at 2025-10-26 took 146.8 s on an EPYC 9V45 and 284.6 s on an
    EPYC 7763.
- **Memory.** It is no constraint on either runner: the largest peak was under 0.92 GiB, against 4 GiB.
- **Cost and capacity.**
  - A private repository counts macOS minutes at ten times.
  - Linux's standard fleet is GitHub's largest.
  - In a public repository, standard runners cost nothing on either OS.
- **What I do not know.**
  - The probe measured the runner classes of a private repository (2 vCPU and 7.7 GiB on Linux).
  - A public repository's standard Linux runner is a different class. Its timing, not its arithmetic, would need
    the re-freeze's own measurement.
  - One image version per OS was observed: `ubuntu24 20261026.354.1` and `macos26 20261013.0424.1`.

**If the Orchestrator chooses macOS instead,** everything below holds with the darwin-arm64 binary. It is the
local control's binary, and the one the `macos-26` jobs ran.

## Proposal 2 — what CP-17c must re-freeze for that runner

- **The pinned binary.**
  - Source: `node-v26.7.0-linux-x64.tar.gz` from `https://nodejs.org/dist/v26.7.0/`, 62,014,253 bytes, SHA-256
    `bd6b6c31e377bad9ad579bed72e5bc11f4c879ac9452ad51d30e646ea3d828df`.
  - Verified against the release's `SHASUMS256.txt` (2,943 bytes, SHA-256
    `4533f0a43b9ba7f78a48230a0511b9dd5c931f20c3b3cac281ff9b7a2080fb2e`).
  - Its `bin/node` is 147,870,928 bytes, SHA-256 `ad19784f7e90ba789a099eccba77ede8dc90a778c424f1c10a70fed3ff903fdc`.
  - The macOS alternative is `node-v26.7.0-darwin-arm64.tar.gz` (57,622,243 bytes, `7ee659a7…`), with `bin/node`
    `a9bd0630891c2dcdee70de88270fee2cc0c4a9e76495039dd3b4f91c5e6b71df`.
- **How the binary is retrieved.**
  - The tarball is over the 50 MB limit for a committed file, so each run retrieves it. Retrieval took 0.5 s here.
    A cache keyed by the tarball's hash would also work.
  - The run verifies the tarball and the binary by those hashes before any fit. The hashes are the pin, not the URL.
  - If retrieval or a hash fails, nothing is fitted and the day is not issued.
- **Pyodide 0.28.0's 23 files** keep their frozen hashes. They total 43 MB, and the largest file is 13 MB, so they
  can live in the repository, as they did in the scratch repository.
- **The host's identity, as the freeze records it.**
  - The runner: GitHub-hosted standard runner, label `ubuntu-24.04` (`ImageOS` `ubuntu24`, x64).
  - The runtime: the binary above, the 23 Pyodide files, the package zip, and CPython with the environment
    `uv.lock` pins.
  - **Pin CPython's patch version.** The probe's runners got 3.13.17 (Linux) and 3.13.16 (macOS), against the frozen
    host's 3.13.15, and the chain's CPython side matched all the same. The freeze should still name one version.
  - The image version and the CPU model are GitHub's to change weekly. Record them in each issuance's lineage; do
    not pin them.
- **Where `refreeze verify` runs: on the runner, in the issuing job, after the runtimes are in place and before the
  first fit.** Its local checks are written for the Mac, so CP-17c must change three things:
  - the Node.js path is Homebrew's (`/opt/homebrew/Cellar/node/26.7.0/bin/node`), so the new manifest must name the
    runner's binary by a fixed path in the job's workspace;
  - the Pyodide folder is `.local/tools/pyodide-0.28.0`;
  - A1's search state `k13.json` sits in the local-only `evidence/cp-26` extract, so it must reach the runner by a
    route CP-17c or CP-18 decides. The payload builder needs it too.
  - `cp17.daily.Host` takes the binary as an argument, which is how this probe ran it unchanged. The defaults
    `cp17.daily.NODE` and `cp17.tools.hosts.NODE` still name Homebrew's path.
- **How a daily run checks its runtime before it issues,** in order. Any failure stops the run: nothing is issued,
  and the day is "not issued".
  1. **The pins.** `refreeze verify` against the new manifest must report no problem and no unchecked file. It exits
     0 in both cases, so the run reads its output, as §24.12 already requires for 4.7T.
  2. **The runner.** `RUNNER_OS` must be Linux, `RUNNER_ARCH` X64, and `ImageOS` ubuntu24. The image version and the
     CPU model go into the lineage.
  3. **A canary fit.** One frozen reference fit reissued under the host, its quantiles' SHA-256 required to equal the
     frozen one.
     - A1 at the freeze origin, 2026-09-06 (`4e6abb02…`), took 137.3 s on Linux and 98.8 s on macOS here, and
       exercises the product's own arithmetic.
     - B0 at the same origin (`b12a9972…`) takes 7–12 s but exercises far less of it.

## Proposal 3 — the daily cost on that runner

These figures are measured, from the tables below. One issuance is A1 plus the three shadows, which decision 14 runs
every day. A job's setup before the chain took 19–30 s.

| | Linux (`ubuntu-24.04`) | macOS (`macos-26`) |
|---|---|---|
| One issuance, one process at a time | 349–366 s | 270–284 s |
| One run with one issuance, plus the A1 canary | about 9 job-minutes | about 7 job-minutes |
| As a private repository counts it | about 9 minutes | about 70 minutes |
| Decision 23's bound: four issuances in one run, one at a time, plus the canary | about 27 job-minutes | about 21 job-minutes |
| As a private repository counts it | about 27 minutes | about 210 minutes |
| Thirty ordinary days a month | about 270 minutes | about 2,100 minutes |

- **Running two issuances at once** is supported by the shadow jobs' evidence:
  - Linux's chain steps took 275–279 s of wall time per day (2 vCPU); macOS's took 151–155 s (5 cores). These are
    the shadow jobs' chain steps in `artifacts.json`, divided by their days.
  - Every attempt stayed inside the ceilings. On Linux the four processes' sum reached 567 s at most, so even the
    sum was within 900 s.
  - Two at once would bring decision 23's four issuances to about 21 job-minutes on Linux.
- **The run stays inside decision 23's own time bound** of about an hour.
- **In a public repository,** standard GitHub-hosted runners cost nothing. Where the pipeline runs is CP-18's
  decision.

## Proposal 4 — an estimate, not a run: DDNN-2's next search, S_14 on 2027-01-06

- **The basis** is committed records, nothing new:
  - S_13 trained 813 fits in 5,079 s of native fit time on this M3, one worker
    (`reports/rebaseline/cold-rerun-2026-10-15/cost-projection.json`, search 13). Searches 3–13 took 3,376–5,079 s.
  - CP-26 priced a cold search at twice the historical figure.
  - Under Pyodide, A1's fits took 3.3–5.6 times their native time, median 4.6 (`reports/cp17b/host-parity.json`).
- **Scaling.** The runners' measured speed against this M3 is the proxy for the search's own: the parity fits' median
  is 1.69 times on Linux and 1.20 times on macOS.
- **The job limit** is GitHub's documented 6 hours per job on hosted runners. It was not tested here.

| S_14 runs… | Linux, one worker | Linux, two workers, with the 2× margin | macOS, one worker | macOS, four workers, with the 2× margin |
|---|---|---|---|---|
| natively, as S_13 did | about 2.4 h | about 2.4 h | about 1.7 h | about 0.9 h |
| under the issuing host (Pyodide) | about 11 h | about 11 h | about 7.8 h | about 3.9 h |

- **Natively, S_14 fits one hosted job on either runner**, with the margin.
- **Under the issuing host, it does not fit one Linux job.** The search would have to be split across jobs: its
  halving rounds run in order, but the fits within a round are independent. It would fit one macOS job with four
  workers.
- **Memory is no constraint.** Pyodide's fits peaked under 0.92 GiB per process, against 7.7 GiB (Linux) and 14 GiB
  (macOS) per runner.
- **Open for the Orchestrator before S_14:** where S_14 runs is not frozen beyond "the same phase, rules and seeds".
  S_13 ran natively on this M3. A native search on another machine is not that machine's arithmetic, and this probe
  measured only the Pyodide path.
