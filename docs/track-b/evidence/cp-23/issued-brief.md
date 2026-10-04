# Track B Checkpoint Brief — CP-23 (the DDNN route: v5 = v4 plus a DDNN member)

## Target
- Repository: DE-LU day-ahead forecasting, `/Users/djourno/Downloads/PJM` (origin
  `hrsi56/delu-day-ahead-forecast`). The checkpoint runs locally.
- Authorized checkpoint: CP-23, exactly one.
- Ratified plan anchor: `capstone_v21.md`, revision v21-r10, §21, SHA-256 `6873c2501067c63692ec7cb79dfd4073164a8a014edbd6ebc23169e7e8ff6709`.

## Orchestrator-reported expected state
- **Branch / commit:** `main` = `origin/main` at the commit that records CP-23's execution
  grant. It is a direct child of `3f7aaf24bf8f5793dd9aba2d88ae8128fef80045`, the v21-r10
  ratification, and changes only `progress.md`. Below them are the checkpoint tools (`42e4ceb`)
  and CP-22's closure (`6483324`, on `land/cp-22` = `ebb7d42`). Only `main` exists, locally and on
  origin. There is no stash and no worktree besides the primary checkout.
- **Working tree:** clean apart from ignored material. This brief's canonical copy is
  `.local/artifacts/cp-23/issued-brief.md`; its SHA-256 is in the launch envelope.
- **What already exists:**
  - **Saved vectors.** v4's (HGL), v3's (HG), A1's and B2's committed vectors are under
    `reports/block-challenger/` (CP-21) and `reports/weather-ablation/` (CP-20), with
    `evidence/cp-21` and `evidence/cp-22`.
  - **Code to reuse by import, read-only:** CP-22's H-layer replay, scoring and controls under
    `src/cp22/`, and CP-21's and CP-20's code.
  - **Retained state:** CP-20's weather grids and HG component cache, and CP-21's and CP-22's
    state, under `.local/artifacts/cp-20/`, `cp-21/` and `cp-22/`.
  - **Tools:** `scripts/gauntlet.py` and `scripts/bar.py`, and the SessionStart hook that keeps
    the secret guard on.
  - **Not yet:** no DDNN code and no `reports/distribution-challenger/`.
- Verify this yourself before relying on it, and report any material mismatch.

## Observable outcome
CP-23 closes with one of two results:

- **DDNN NOT_ADMITTED** at 4.6L or 4.6R, with its cause and no comparison; or
- **4.6C complete,** with `cp23-adoption` applied mechanically. v5 is either adopted in research
  or becomes the branch "DDNN member on v4", with its first unmet condition.

The second result also carries:

- the descriptive readings for DDNN alone and for v3+D;
- §21.5's diagnostics;
- the publication packet and a draft MLflow export.

Either result is bound by one fresh Integration-Critic PASS.

## Complete authoritative checkpoint bar
`capstone_v21.md` v21-r10 §21.10, "Complete CP-23 acceptance checklist", all sixteen items. They
are governed by:

- §21.1–§21.9 and §21.11;
- the inheritances those sections name: §17.3–§17.9, §20.4–§20.7, §14.6, §8 and §18.

Verbatim, checked with `scripts/bar.py check` against the anchor at `3f7aaf2`:

> ### 21.10 Complete CP-23 acceptance checklist
>
> All sixteen items are mandatory. Engineering PASS does not require admission or adoption: a
> complete, valid NOT_ADMITTED or not-adopted result can pass.
>
> 1. **Verify the starting state** and preserve prior evidence and other sessions' work.
>    - Verify the ratified anchor's SHA-256 against the brief.
>    - Record the baseline with `scripts/gauntlet.py start cp-23`.
>    - On `gauntlet/cp-23`, package the issued brief byte for byte as
>      `docs/track-b/evidence/cp-23/issued-brief.md`.
> 2. **Complete 4.6L,** with every use dispositioned. Stop at its cap, or if research use is not
>    permitted.
> 3. **Prove the code's correctness under §21.3:**
>    - the NumPy-only import audit;
>    - finite-difference gradient checks;
>    - the PyTorch reference checks, passing at the frozen tolerances and installed so that they
>      cannot be skipped silently.
> 4. **Complete 4.6R** on training data only, with the measured values, the projection against
>    §21.8, and PASS or NOT_ADMITTED with its cause. On NOT_ADMITTED, stop, with no comparison,
>    and report to 4.7.
> 5. **Commit the frozen pre-run protocol** (§21.4) before any evaluation fit.
> 6. **Verify the inputs:**
>    - population, manifest and frozen weather;
>    - saved-vector identities;
>    - an independent representative HG and v4 slice;
>    - no retrieval, and nothing after 2026-04-07.
> 7. **Implement exactly DDNN, v5 and the arms,** with training-only selection and early stopping,
>    and prove composite parity.
> 8. **Prove every control** of §21.7 and the inherited ones, each negative paired with a positive.
> 9. **Produce all 10,747 keys** for every new policy, with finite, ordered quantiles and the
>    emitted p50 kept separate from the central forecast.
> 10. **Score every policy,** and independently verify the scores, the diagnostics, coverage with
>     width, and all six §8 diagnostics for each new policy.
> 11. **Apply `cp23-adoption` mechanically.** State the decision with its first unmet condition,
>     and every §21.5 contrast with its reading. Keep the Engineering, research and product
>     statuses distinct.
> 12. **Deliver §21.5's diagnostics** to `reports/distribution-challenger/`.
> 13. **Enforce and report every §21.8 cap,** and respect the calendar.
> 14. **Supply the durable evidence,** executable reproduction commands and byte-exact storage.
>     Deliver §21.9's packet and draft export. Public surfaces and the published export set stay
>     unchanged, CI is green, and there is no public write.
> 15. **Obtain one fresh, independent Integration-Critic PASS** on a clean detached checkout of
>     the final candidate. Launch it with `scripts/gauntlet.py critic-open`, `critic-brief` and
>     `critic-close`. The review independently:
>     - recomputes the metrics, intervals and the verdict;
>     - reruns the reference checks;
>     - reproduces a representative DDNN fit, its ensemble and its quantile emission;
>     - re-derives the packet.
> 16. **Return the canonical packet** (templates §3), checked with `scripts/gauntlet.py return`.
>     It carries:
>     - both terminal SHAs and the verdict-only delta;
>     - resource totals;
>     - branch, worktree and stash accounting.
>
>     Stop at CP-23's local result.

## Task-specific supporting extract
- **The candidate:** v5 = `(2/3)·c_v4 + (1/3)·D`, with HG's H layer re-estimated on v5's own
  errors.
- **The arms:** D, DDNN alone with its own Johnson SU quantiles, and v3+D, both never eligible.
  The references are v4 (the comparator), v3, A1 and B2.
- **DDNN:**
  - NumPy only, with a Johnson SU head;
  - exactly v4's information, on §4's normalized target;
  - history `[max(2019-01-01, D−728), D)`, refitted at every origin;
  - early stopping on the window's last 28 days;
  - at most four configurations, chosen once per fold before its first origin, on training data
    only;
  - at most four seeds, combined by quantile averaging unless the protocol fixes otherwise;
  - p50 and the central forecast D are the ensemble's median.
- **The gates:** 4.6L (at most 4 active hours), then the §21.3 checks, then 4.6R (training only,
  projected against §21.8), then the frozen protocol, then 4.6C.
- **The rule:** `cp23-adoption` (§21.6), four conditions against v4.

## Applicable constraints
- **The §21.8 ceilings,** enforced from the first job:
  - DDNN fits: 4,000 main and 6,000 in total;
  - 8,000 policy-days;
  - 3 reference passes and 3 bootstrap passes;
  - 60 machine-hours, at most 4 workers, BLAS 1, CPU only;
  - 10 GiB RSS and 10 GiB added disk;
  - 0 data bytes, 0 remote writes, $0.

  The one permitted download is the pinned PyTorch CPU test dependency, from PyPI.
- **The calendar:** no scheduled work from Friday 00:00 to Sunday 00:00, Asia/Jerusalem.
- **Data:** nothing dated after 2026-04-07, and no weather retrieval.
- **Credentials** follow `AGENTS.md` § Credentials. Export `MLFLOW_DISABLE_TELEMETRY=true` and
  `DO_NOT_TRACK=1` for any MLflow job.
- **Working files** go under `.local/`. Commit work in progress on `gauntlet/cp-23` before any
  pause: GitHub Desktop stashes untracked files when the Owner switches branches.
- **Tools:**
  - run `scripts/gauntlet.py start cp-23` first;
  - launch the one Critic with `critic-open`, `critic-brief` and `critic-close`;
  - check the return with `scripts/gauntlet.py return`.
- **Owner-facing Git commands** must be non-interactive: `git --no-pager …` and
  `git commit -F <file>`.

## Timebox
About 30 active hours from orientation to the terminal return, with a hard ceiling of 40 (§21.8).

## Owner-only actions already authorized
- **CP-23's execution** under v21-r10 §21 and this brief:
  - local `gauntlet/cp-23` candidate and evidence commits;
  - exact packaging of this brief.

  Granted by the Owner on 2026-10-04: "מאשר ביצוע CP-23, ההחלטות כפי שקבעת".
- **The one download:** the pinned PyTorch CPU wheel set from PyPI, as a test-only dependency,
  with its licence recorded in 4.6L.
- **Nothing else:** no mainline operation, push, tag, publication, remote write, data retrieval
  or governance edit.

## Stop and return
- **First commit.** The first commit on `gauntlet/cp-23` copies this brief byte for byte to
  `docs/track-b/evidence/cp-23/issued-brief.md`.
- **The return.** Return exactly one of PASS / BLOCKED / INCOMPLETE, using templates §3. It
  carries both terminal SHAs and the verdict-only delta, checked with `scripts/gauntlet.py
  return`.
- **Do not** begin, scaffold or plan the data-admission research, 4.4V, 4.8 or any publication.
  Do not commit to `main`, publish or push.
