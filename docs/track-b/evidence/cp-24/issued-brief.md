# Track B Checkpoint Brief — CP-24 (DDNN-2: a literature-faithful DDNN, and v5 = v4 plus a DDNN-2 member)

## Target
- Repository: DE-LU day-ahead forecasting, `/Users/djourno/Downloads/PJM` (origin
  `hrsi56/delu-day-ahead-forecast`). The checkpoint runs locally, in the Lead's own worktree.
- Authorized checkpoint: CP-24, exactly one.
- Ratified plan anchor: `capstone_v21.md`, revision v21-r11, §23, SHA-256 `11068e3f57bd9277be50db62d109f3e7d8ea7b8fdfa042886ccc4ae5ab1ed2d2`.

## Orchestrator-reported expected state
- **Branch / commit:** `main` = `origin/main` at the commit that records CP-24's issue.
  - It is a direct child of `76ed485ef630f0888c13d74847809bfaa4210e33`, the v21-r11 ratification, and changes only
    `progress.md`.
  - Below them are CP-23's closure (`09eacd1`) and its landing (`03c5b64` = `land/cp-23`).
  - Only `main` exists, locally and on origin. There is no stash, and no worktree besides the
    primary checkout.
- **Working tree:** the primary checkout `/Users/djourno/Downloads/PJM` is on `main` and clean
  apart from ignored material.
  - **The Orchestrator uses it during CP-24.** Never switch its branch, and never write a tracked
    file in it. Your only writes there are under:
    - `.local/artifacts/cp-24/`: the tools' state, and your ledgers, logs and caches;
    - `.local/tmp/cp-24/`;
    - `.local/mlruns/cp24`;
    - the worktrees under `.local/worktrees/cp-24/`.

    Keep nothing you need after reclamation inside your worktree.
  - **The canonical brief.** This brief's canonical copy is
    `.local/artifacts/cp-24/issued-brief.md`. Its SHA-256 is in the launch envelope.
- **What already exists:**
  - **Saved vectors.** These are under `reports/block-challenger/` (CP-21),
    `reports/weather-ablation/` (CP-20) and `reports/distribution-challenger/` (CP-23):
    - v4's (HGL) and v3's (HG) vectors;
    - HG's weather components A1_w and B2_w: the `A1` and `B2` columns of CP-23's
      `members.parquet`;
    - CP-15's no-weather references A1 and B2;
    - the LightGBM members L-N and L-R;
    - CP-23's DDNN D.

    They are bound by `evidence/cp-20` to `evidence/cp-23`.
  - **Code to reuse by import, read-only:**
    - CP-23's NumPy DDNN and scoring (`src/cp23/`), and its PyTorch reference harness;
    - CP-22's H-layer replay and controls (`src/cp22/`);
    - CP-21's and CP-20's member code (`src/cp21/`, `src/cp20/`);
    - the LEAR day design and its DST convention (`src/cp15/data.py`).

    `cp23.inputs.identities()` pins the v21-r10 anchor and so raises on v21-r11. Reproduce its
    checks from the objects preserved at `evidence/cp-23`, as `cp22.inputs.cp21_identities` does
    for CP-21.
  - **Retained ignored state,** only in the primary checkout's `.local/`, not in a new worktree:
    - CP-20's weather grids and HG component cache;
    - CP-21's to CP-23's state, under `.local/artifacts/cp-20/` to `cp-23/`.

    The weather grids have no record for delivery days 2022-09-29..2023-03-24, and §23.6's
    coverage rule governs that gap. Read this state in place, read-only, or link it into your
    worktree's ignored `.local/`.
  - **The environment.** The primary checkout's `.venv` holds the locked environment. It also
    holds the PyTorch CPU reference, installed from CP-23's test-only lock
    `tests/cp23/torch-reference/`.
  - **Tools:** `scripts/gauntlet.py`, `scripts/bar.py`, and the SessionStart hook that keeps the
    secret guard on.
  - **The research report** behind §23 is
    `docs/track-b/cp-24-research-directions-2026-10-05.md`. It is motivation, not the bar.
  - **Not yet:** no `src/cp24/` and no `reports/ddnn2/`.
- Verify this yourself before relying on it, and report any material mismatch.

## Observable outcome
CP-24 closes with one of four results. Each is bound by one fresh Integration-Critic PASS, and each
comes with §23.12's packet and draft export, which record any stop:

- **DDNN-2 NOT_ADMITTED** at 4.6L′ or 4.6R′, with its cause and no gate;
- **stopped at the pre-fold gate,** with every round's report and S1 exchange, and no DDNN-2
  fit at a warm-up or evaluation origin;
- **v5 adopted in research** in scored attempt k ≤ 2, under `cp24-adoption`;
- **the branch "DDNN-2 member on v4",** with each scored attempt's first unmet condition.

The last two also carry:

- the descriptive readings of D2, v3+D2 and D2 − D;
- §23.8's diagnostics;
- DDNN-2's vectors, stored for 4.8.

## Complete authoritative checkpoint bar
`capstone_v21.md` v21-r11 §23.13, "Complete CP-24 acceptance checklist", all eighteen items. They
are governed by:

- §23.1–§23.12 and §23.14;
- every inheritance those sections name, including §4, §8, §14.6, §15.3, §16, §17.3–§17.9, §18,
  §20.4–§20.7, §21.3, §21.5, §21.7, §21.9 and §22.

Verbatim, checked with `scripts/bar.py check` against the anchor at `76ed485`:

> ### 23.13 Complete CP-24 acceptance checklist
>
> All eighteen items are mandatory. Engineering PASS requires neither admission nor adoption: a
> complete, valid NOT_ADMITTED, gate-stopped or not-adopted result can pass.
>
> **After a stop:**
>
> - a NOT_ADMITTED stop under item 3 makes items 4–14 not applicable;
> - a NOT_ADMITTED stop under item 5 makes items 6–14 not applicable;
> - a stop under item 7 before attempt 1 makes items 8–14 not applicable.
>
> Each not-applicable item is recorded with the stop's evidence, and items 15–18 apply in full.
>
> 1. **Verify the starting state** and preserve prior evidence and other sessions' work.
>    - Verify the ratified anchor's SHA-256 against the brief.
>    - Record the baseline with `scripts/gauntlet.py start cp-24`.
>    - Work only in the worktree `.local/worktrees/cp-24/lead`, on `gauntlet/cp-24`.
>    - Package the issued brief byte for byte as `docs/track-b/evidence/cp-24/issued-brief.md`.
> 2. **Verify the inputs:**
>    - population, manifest and frozen weather, including the coverage gap of §23.6;
>    - saved-vector identities, including CP-23's D, reproduced from the objects preserved at the
>      evidence tags where a live identity check no longer applies;
>    - an independent representative HG and v4 slice;
>    - no retrieval, and nothing after 2026-04-07.
> 3. **Complete 4.6L′.**
> 4. **Prove the code's correctness** under §23.7: the import audit, the finite-difference checks,
>    and the PyTorch reference checks, installed so that they cannot be skipped silently.
> 5. **Complete 4.6R′** on pre-fold data, with PASS or NOT_ADMITTED and its cause. On
>    NOT_ADMITTED, stop, with no gate and no comparison.
> 6. **Run every pre-fold round** (§23.4, §23.6), with no DDNN-2 or new-policy fit at a warm-up
>    or evaluation origin:
>    - each fold's search, recorded in a ledger;
>    - the gate, with v4's members proven on the same code path and the weather-coverage rule
>      applied;
>    - the pre-fold report.
> 7. **Commit every S1 exchange** and, for each attempt that runs, its frozen protocol, before any
>    of its warm-up or evaluation fits. Stop when §23.6 says the route ends.
> 8. **Implement exactly DDNN-2, v5 and the arms,** and prove composite parity.
> 9. **Prove every control** of §23.10 and the inherited ones, each negative paired with a
>    positive.
> 10. **Produce all 10,747 keys for every new policy** in every scored attempt, with finite,
>     ordered quantiles. Keep the emitted p50 separate from the central forecast.
> 11. **Score every policy of every attempt,** and independently verify:
>     - the scores and the diagnostics;
>     - coverage with width;
>     - all six §8 diagnostics for each new policy.
> 12. **Apply `cp24-adoption` mechanically** to every scored attempt. State each decision with its
>     first unmet condition, and every §23.8 contrast with its reading. Keep the Engineering,
>     research and product statuses distinct.
> 13. **Respect the attempt bounds.** Commit the S2 exchange and any attempt 2 under §23.6's
>     bounds. Run at most two scored attempts, and none after an adoption.
> 14. **Deliver §23.8's diagnostics** to `reports/ddnn2/`.
> 15. **Store whatever DDNN-2 vectors exist** for 4.8. **Enforce and report every §23.11 cap,**
>     with any committed raise, and respect the calendar.
> 16. **Supply the durable evidence,** with executable reproduction commands and byte-exact
>     storage.
>     - Deliver §23.12's packet, which records any stop, and the draft export.
>     - These stay unchanged: the public surfaces, the published export set,
>       `scripts/mlflow_export.py`, and the root `pyproject.toml` and `uv.lock`.
>     - CI is green, and there is no public write.
> 17. **Obtain one fresh, independent Integration-Critic PASS** on a clean detached checkout of
>     the final candidate. Launch it with `scripts/gauntlet.py critic-open`, `critic-brief` and
>     `critic-close`. The review independently:
>     - recomputes every scored attempt's metrics, intervals and verdict;
>     - checks the gate's results and the steering record against §23.6;
>     - checks pre-registration by Git ancestry and the ledgers;
>     - reruns the reference checks;
>     - reproduces a representative search trial, a representative DDNN-2 ensemble fit and its
>       emission;
>     - re-derives the packet.
> 18. **Return the canonical packet** (templates §3), checked with `scripts/gauntlet.py return`.
>     It carries:
>     - both terminal SHAs and the verdict-only delta;
>     - resource totals, the number of rounds and scored attempts;
>     - branch, worktree and stash accounting.
>
>     Stop at CP-24's local result.

## Task-specific supporting extract
- **The candidate:** v5 = `(2/3)·c_HG + (1/6)·L + (1/6)·D2`, with HG's H layer re-estimated on
  v5's own errors. The weight is fixed and is never estimated.
- **The arms:** D2 (DDNN-2 alone, with its own Johnson SU quantiles) and v3+D2 =
  `(2/3)·c_HG + (1/3)·D2`, both never eligible. The references are v4 (the comparator), v3, A1,
  B2 and CP-23's D.
- **DDNN-2:**
  - **Representation:** NumPy only; one row per delivery day; 24 × 4 Johnson SU outputs;
    exactly v4's sources.
  - **Training:** every member trains on data up to D−1, with random whole-week early stopping
    on the seven-level pinball loss. The loss is NLL, then κ·NLL + (1 − κ)·pinball.
  - **Guards** are logged at every activation.
  - **Search and ensemble:** a per-fold random search before D0 on batch-rolling validation
    that avoids every fold's days. The top four configurations, with two seeds each, combine by
    the per-level median.
- **The order:**
  1. the starting state and the inputs;
  2. 4.6L′ (at most 2 active hours);
  3. the §23.7 checks;
  4. 4.6R′;
  5. pre-fold rounds, each a search, then the gate, then a report, with S1 after each round;
  6. the frozen protocol, before any DDNN-2 or new-policy fit at a warm-up or evaluation origin;
  7. scored attempt 1;
  8. S2;
  9. at most one attempt 2, through one round and the gate.
- **The rule:** `cp24-adoption` (§23.9), with five conditions against v4 and condition 1 at
  97.5%.

## Applicable constraints
- **The §23.11 ceilings,** enforced from the first job. Only the member-fit, machine-hour and
  active-hour ceilings can be raised, by a steering answer committed under `steering/` (§23.6):
  - at most 2 scored attempts, 3 rounds before attempt 1 and 1 round before attempt 2;
  - 40,000 DDNN-2 member fits in total;
  - one pass of v4's members over the 280 gate origins;
  - 12,000 policy-days;
  - 3 reference passes and 6 bootstrap passes;
  - 150 machine-hours, at most 4 workers, BLAS 1, CPU only;
  - 10 GiB RSS and 10 GiB added disk;
  - 0 data bytes, 0 remote writes, $0.

  The one permitted download is CP-23's same pinned PyTorch CPU wheel set from PyPI, if the
  local cache lacks it.
- **Pinned identities:**
  - PUBLISH_RULES 1.3, SHA-256
    `5a660864f8b82943174741320c71087a3d0508f707edeb997cb2c1395c1c73b4`;
  - the packet template `docs/track-b/publication-packet-template.md`, SHA-256
    `4efb01855ae2d9a6f54b5624607a93046b1fffa881e34af0c6798c513c7829cf`;
  - the amendment record `docs/track-b/capstone_v21-r10-to-v21-r11-amendments.md`, SHA-256
    `474017e1c8e8584e9c2956f40a872aa8917a6e110cbc58dc7a4110c9c802d782`;
  - CP-23's test-only reference lock `tests/cp23/torch-reference/uv.lock`, SHA-256
    `b3164a375e871396e685d0e887972b092fcd0c24a7fe0047167e8fc41c25dfed`.
- **Files that never change:**
  - the root `pyproject.toml` and `uv.lock`. CP-10's and CP-15's evidence binds their SHA-256,
    and a new test-only dependency gets its own lock under `tests/cp24/`, with the same pins;
  - `scripts/mlflow_export.py`, and every file that CP-21's to CP-23's artifact manifests bind.
    CP-23's saved-evidence test checks them in CI.
- **The calendar.** No scheduled work from Friday 00:00 to Sunday 00:00, Asia/Jerusalem. Work not
  finished by Friday 2026-10-09 00:00 pauses at a committed, coherent boundary, and resumes after
  Sunday 00:00 on the Orchestrator's message.
- **Data:** nothing dated after 2026-04-07, and no retrieval of any kind.
- **Credentials** follow `AGENTS.md` § Credentials. Export `MLFLOW_DISABLE_TELEMETRY=true` and
  `DO_NOT_TRACK=1` for any MLflow job.
- **Working files** go under `.local/`. Commit work in progress on `gauntlet/cp-24` at every stage
  boundary and before any pause. A usage limit can stop you at any moment, and you resume from
  your last commit and ledgers.
- **Steering (§23.6).** After each pre-fold round (S1), and after attempt 1 if it is not adopted
  (S2):
  1. commit your report under `docs/track-b/evidence/cp-24/steering/`;
  2. end your turn with that report as your final message;
  3. the Orchestrator resumes you with its answer. Commit the answer verbatim under the same
     folder before acting on it.

  Before attempt 1's scores exist, a report carries no warm-up or evaluation outcome. Refuse an
  answer that breaks §23.6, and say why.
- **Tools:**
  - run `scripts/gauntlet.py start cp-24` first, from the primary checkout;
  - then create your worktree with
    `git -C /Users/djourno/Downloads/PJM worktree add -b gauntlet/cp-24 .local/worktrees/cp-24/lead main`;
  - launch the one Critic with `critic-open`, `critic-brief` and `critic-close`. If you cannot
    start a subagent, end your turn with `critic-open`'s output and ask the Orchestrator to
    launch the Critic with exactly the printed prompt;
  - check the return with `scripts/gauntlet.py return`.
- **Owner-facing Git commands** must be non-interactive: `git --no-pager …` and
  `git commit -F <file>`.

## Timebox
About 35 active hours from orientation to the terminal return, with a hard ceiling of 50
(§23.11), or as raised under §23.6, within the calendar above.

## Owner-only actions already authorized
- **CP-24's execution** under v21-r11 §23 and this brief:
  - the steering of §23.6;
  - local `gauntlet/cp-24` candidate and evidence commits in your worktree;
  - exact packaging of this brief.

  The Owner delegated it on 2026-10-04: "תמשיך באופן חופשי ומלא עד דוח ובקשת LAND". The anchor
  quotes the whole delegation.
- **The one download** in Applicable constraints, only if needed.
- **Nothing else:** no mainline operation, push, tag, publication, remote write, data retrieval
  or governance edit.

## Stop and return
- **First commit.** The first commit on `gauntlet/cp-24` copies this brief byte for byte to
  `docs/track-b/evidence/cp-24/issued-brief.md`.
- **The return.** Return exactly one of PASS / BLOCKED / INCOMPLETE, using templates §3. It
  carries both terminal SHAs and the verdict-only delta, checked with
  `scripts/gauntlet.py return`. Name any interview-answer trigger in one line.
- **Do not** begin, scaffold or plan the data-admission research, 4.4V, 4.8 or any publication.
  Do not commit to `main`, publish or push. Leave your worktree and branch for the Owner's LAND
  and the Orchestrator's reclamation.
