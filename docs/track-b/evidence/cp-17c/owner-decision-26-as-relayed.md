# The Owner's decision 26, as relayed to CP-17c's Lead

This is CP-17c's evidence of the ruling the Lead acted on: it is not a decisions record, which the Orchestrator keeps.

**Relayed by** the Orchestrator's session to the Lead on 2026-10-30, after CP-17c's first return (BLOCKED: GitHub had
refused the `resume` run for billing).

**The Owner's words, verbatim (2026-10-30):**

> לא אכפת לי שיהיה פאבליק על הגיט האב מה אכפת לי. תעשה פאבליק, תנסה לאמן ותמשיך עצמאית זה לא פרסום זה רק גיט בלי gh pages

**The Orchestrator's rendering.** He does not mind the scratch repository being public on GitHub: make it public, run
the training, and continue independently; it is not a publication, only a Git repository without GitHub Pages. To be
recorded as Owner decision 26.

**What the Orchestrator did before the switch** (as relayed):
- a value-based secret scan of the scratch repository's whole history (a fresh mirror clone, all five commits, through
  `scripts/secret_guard.py pre-push` with five credential values loaded): 0 findings;
- the same over the four runs' logs and all five artifacts: 0 findings;
- `gh repo edit … --visibility public` at 2026-10-30 14:21 UTC.

**What it changes for CP-17c:**
- **The scratch repository `hrsi56/delu-host-refreeze` is public** from 2026-10-30 14:21 UTC. The issued brief said it
  "is never made public"; the Owner's ruling supersedes that for this repository. It has no GitHub Pages, no secret and
  no variable, and its workflow token stays read-only.
- **The runner class.** Runs 1–4 ran on the private repository's `macos-26` class. Runs 5 and 6 (`resume`) ran on the
  public repository's class. That departs from r19 §24.13's reason for measuring on a private repository's `macos-26` ("Why
  not a public scratch repository. Its runs would need A1's search state and CP-17c's material."), by the Owner's
  ruling. The freeze record §8 and the return say which runs ran where, and what each machine was.
- **What became public** with the repository: the material §24.13 named, A1's search state `k13.json`, the
  freeze-origin states, the canary's payload, the carried state stores, the frozen package and the pinned Pyodide
  files, and development payloads through 2026-09-06. Nothing dated after 2026-09-06, and no credential value.
- **Minutes.** GitHub does not count a public repository's standard runners against the quota. CP-17c records runs 5
  and 6's job minutes and counts them as zero.
- **The first resume after the switch failed, transiently.** Run 5 (`41071149787`, 14:21:57 UTC) got a runner, but
  its checkout's fetch was answered three times with HTTP 403: "remote: Repository 'hrsi56/delu-host-refreeze' is
  disabled. remote: Please ask the owner to check their account." GitHub was still processing the visibility change.
  By 14:26 UTC anonymous reads worked again, as the Orchestrator and the Lead both checked. The run spent no
  compute: 33 seconds of job time, uncounted on a public repository. Run 6 (`41071696187`) is the same run, unchanged.
- **Run 6's machine** (its checks record): image `macos26 20261013.0424.1`, Apple M1 (Virtual), 3 cores, 7 GiB. That
  matches the private runs' machine class, and run 2's image version; run 3 ran on `20261021.0445.8`. Every run that
  reached its checks reproduced CP-17b's records bit for bit.
- **Run 6's timing** is a first measurement on the public repository's class. r19 §24.13 leaves that measurement to
  CP-18 ("CP-18 measures the public class's timing in the product's repository, on development days, before the first
  live issuance"); it is reported as what it is, and is not CP-18's measurement.

**The Owner's standing instruction, as relayed afterwards (2026-10-30):** run everything through to the complete
publication independently. CP-17c keeps to its brief's rules and finishes the round as planned.
