# Track B Checkpoint Brief — CP-22 (v4 revised: one pooled member and a dynamic interval layer)

## Target
- Repository: DE-LU day-ahead forecasting, `/Users/djourno/Downloads/PJM` (origin
  `hrsi56/delu-day-ahead-forecast`).
- Authorized checkpoint: CP-22, exactly one.
- Ratified plan anchor: `capstone_v21.md`, revision v21-r9, §20, SHA-256 `5fc9c6862aa9f623af29db295e79456ecd94c60e213f8f286cdca97153e09175`.
- The amendment record is `docs/track-b/capstone_v21-r8-to-v21-r9-amendments.md`, SHA-256
  `912eb98ffceb1b7b31e0e14da6cffc8725c3af7b227cbbcef4cea62841f5d52a`.
- The publication anchor is `docs/PUBLISH_RULES.md` 1.3, SHA-256 `5a660864f8b82943174741320c71087a3d0508f707edeb997cb2c1395c1c73b4`.
- Verify all three hashes.

## Orchestrator-reported expected state
- **Branch / commit:** `main` = `origin/main` at the v21-r9 ratification commit. It is a direct
  child of `ddb9379` (PRES-3 closed) and adds or changes six documents:
  - `capstone_v21.md`;
  - `docs/PUBLISH_RULES.md`;
  - `docs/track-b/capstone_v21-r8-to-v21-r9-amendments.md`;
  - `docs/track-b/cp-22-publication-plan-2026-10-01.md`;
  - `docs/track-b/v3-plan-handoff-2026-09-22.md`;
  - `progress.md`.

  No `gauntlet/*` branch, no worktree besides the primary checkout, no stash.
- **Working tree:** clean apart from ignored material. This brief's canonical copy is
  `.local/artifacts/cp-22/issued-brief.md`.
- **What already exists:**
  - **CP-21's evidence:** `land/cp-21` = `4e37cf7`, `evidence/cp-21` = `1d13f99`.
    - `reports/block-challenger/`, including `predictions.parquet` (HGL, L-N, L-P and L-R for
      all 10,747 keys), `fits.parquet`, `protocol.json` (the capacity grid G1–G4) and
      `uncertainty.csv`.
  - **CP-20's evidence:** `reports/weather-ablation/`, with HG and its components.
  - **Retained local state:** `.local/artifacts/cp-21/` holds the fit cache, the HGL state
    snapshots and the ledger, and may hold warm-up forecasts. `.local/artifacts/cp-20/` holds
    the weather grids and the HG component cache.
  - **Tooling:** LightGBM is pinned. The exporter is `scripts/mlflow_export.py`.
- Verify all of this yourself before relying on it, and report any material mismatch.

## Observable outcome
A local, independently reviewed CP-22 evaluation on `gauntlet/cp-22`. When it closes:

- PN (PN-avg and PN-sel) and every §20.2 composite are issued for all 10,747 keys;
- every policy is scored with §20.5's paired, per-fold and ratio uncertainty;
- `cp22-replacement` has been applied mechanically. The result is R, M or no replacement, with
  the first unmet condition.
- if there is a winner, `cp22-dynamic-layer` has been applied to it, and then, if DL was
  adopted, `cp22-fast-component`;
- every §20.5 contrast is reported with its reading, including the Owner's investigation
  diagnostics;
- the fit-cost and daily-cycle diagnostic is delivered;
- the publication packet and the draft export are complete;
- one fresh Integration-Critic PASS binds the exact final candidate;
- nothing is on `main`, nothing is pushed and nothing is written publicly.

A complete, valid "no replacement" result is a successful checkpoint. It stops there for the
Owner's decision.

## Complete authoritative checkpoint bar
`capstone_v21.md` v21-r9, **§20.10: all thirteen items.**

- The governing specification is §20.1–§20.9 and §20.11.
- §20 incorporates §17.3–§17.9 where it says so, together with their inherited §§2–4, §8's six
  diagnostics and §§14–15.
- Every item is mandatory. This brief's extract never narrows it.

## Task-specific supporting extract
- **Eligible policies, in a fixed sequence:**
  - R = `(2/3)·c_HG + (1/3)·PN-avg`;
  - then M = `(2/3)·c_HG + (1/3)·mean(PN-sel, L-P)`.

  Both are judged by `cp22-replacement`'s non-inferiority against v4, on both scores and per
  fold, with all six §8 diagnostics.
- **The dynamic layer.** DL on the winner is a separate decision. Its fixed parameters are a
  7-day half-life for recency weights inside the 28-day buffer, ACI with γ = 0.10 per day, and
  `α_t` clipped to `[α/5, min(2α, 0.9)]`. Freeze them, with direction fixtures, in the pre-run
  protocol.
- **W+DLF** is DL plus a fast kernel: a one-day half-life carrying one third of the weight. It is
  decided only as an add-on to an adopted W+DL (`cp22-fast-component`), never as a replacement
  for the 7-day memory. Report the shock-day diagnostics of §20.5.
- **Fixed:** the 1/3 member weight. **Excluded:** learned weights, new features, blocks, seed
  ensembles and LEAR changes.
- **Reuse.** L-P, L-N, HGL and HG vectors are reused only with verified identity. Warm-up errors
  come from retained state, or from bit-identical regeneration within the caps.

## Applicable constraints
- **The §20.8 ceilings, enforced from the first job:**
  - LightGBM: 6,000 main and 9,000 total fits;
  - replay: 16,000 new policy-days;
  - 30 machine-hours, at most 4 concurrent threads, BLAS 1;
  - 10 GiB RSS and 10 GiB added disk;
  - 0 bytes downloaded and 0 remote writes; $0.
- **The calendar:** no work from Friday 00:00 to Sunday 00:00, Asia/Jerusalem.
- **Data:** nothing dated after 2026-04-07, and no weather retrieval.
- **Credentials** follow `AGENTS.md` § Credentials. Export `MLFLOW_DISABLE_TELEMETRY=true` and
  `DO_NOT_TRACK=1` for any MLflow job. The secret guard is mandatory; never use `--no-verify`.
- **Working files** go under `.local/`.
- **Owner-facing Git commands** must be non-interactive: `git --no-pager …` and
  `git commit -F <message file>`.

## Timebox
About 24 active hours; hard ceiling of 32, from orientation through terminal return. Report
elapsed hours to the nearest half hour.

## Owner-only actions already authorized
CP-22's execution under §20.11's grant:

- local `gauntlet/cp-22` candidate and evidence commits;
- exact packaging of this brief.

Nothing else: no mainline operation, push, tag, publication, remote write, data retrieval or
governance edit.

## Stop and return
- **First commit.** The first commit on `gauntlet/cp-22` copies this brief byte for byte to
  `docs/track-b/evidence/cp-22/issued-brief.md`.
- **The return.** Return exactly one of PASS / BLOCKED / INCOMPLETE, using
  `docs/track-b/gauntlet-templates.md` §3, with the publication packet attached. Include:
  - both terminal SHAs and the verdict-only delta;
  - every §20.8 total;
  - all three verdicts, each with its first unmet condition;
  - every §20.5 contrast reading;
  - branch and worktree accounting.
- **Do not** begin, scaffold or plan PRES-4 or 4.6. Do not commit to `main`, publish or push.
