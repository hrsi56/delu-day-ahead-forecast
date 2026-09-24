# Integration Critic — CP-20

## Candidate
- Full SHA: 3e9ff8b500c2c655fea810ae11886503927f176c
- Clean detached worktree (created by the Lead with
  `git -C /Users/djourno/Downloads/PJM worktree add --detach /Users/djourno/Downloads/PJM/.local/worktrees/cp-20/critic-2 3e9ff8b500c2c655fea810ae11886503927f176c`):
  `/Users/djourno/Downloads/PJM/.local/worktrees/cp-20/critic-2`
- Confirm `git status --porcelain` is empty and `HEAD` equals the SHA before and after your review.
  Work only from that worktree. Perform no Git write of any kind (no commit, checkout, reset, stash,
  worktree add/remove, push) and edit no tracked file.

## Controlling plan
- File: `capstone_v21.md`   Version: v21-r4 (ratified), SHA256 150bd53fa15067b1d138c95d0912f86a1e92ce74092059be09034758c1926167,
  read with `docs/track-b/capstone_v21-r3-to-v21-r4-amendments.md` (SHA256 3e0bdf6a343d5336f406f0eeb726b1b65c0f767ec8d9418a7d8118902e1ace55)
  and the execution brief `docs/track-b/cp-20-direct-weather-brief.md` (SHA256 28a4e195fa7f66ff3270d5d54e477478e90aa42124bceb1ee529f95f5761883e).
- Bar citation: §15.6, inheriting the §14.8 verification standard, §§15.1–15.5 and §§14.1–14.4.
- Verbatim bar excerpt:
  > ### 15.6 Complete CP-20 acceptance checklist
  >
  > All ten items are mandatory. They inherit the verification standard of §14.8; the weather
  > additions and H0/HG scope replace CP-16-specific H/P wording, not its scientific safeguards.
  >
  > 1. Verify repository/input state, retain prior evidence and other-session work; after Owner
  >    ratification/execution grant only, package exact supplied anchor/amendment/brief and commit
  >    the frozen protocol/input/conversion/missingness/budget manifests before comparison.
  > 2. Close the eight-run admission extension; validate all extracted field/lead/version metadata,
  >    source/endpoint identity and historical availability basis. Preserve inferred versus decoded
  >    evidence, 2019 structural missingness and all dossier exceptions; record every extraction gap.
  > 3. Implement exactly H0/HG and the frozen conversion/fallback; show only the predefined weather
  >    treatment differs. Verify H0 against accepted CP-16 vectors and reproduce representative
  >    weather-component fits. Training-only admission must precede outer scoring; no tuning to gain.
  > 4. Prove §14.8 item 3's causal/state/DST/cache controls, plus positive/negative weather-origin,
  >    accumulation, units, packing/clipping, aggregation and missingness controls. Verify pre-2019
  >    refusal and independent reconstruction from retained raw samples without rerunning admission.
  > 5. Produce all original eligible keys for both arms and the required reference metrics; no
  >    denominator changes. Independently verify emitted p50/ordered vectors, all §14.3 diagnostics
  >    and support counts, including fallback incidence; inherited failures still preclude PASS.
  > 6. Apply HG−H0 paired endpoint rule and all six original §8 diagnostics; keep point/interval
  >    effects, uncertainty, negative/mixed findings, post-selection labels and research/product
  >    distinctions. No promotion, economic threshold or claim of guaranteed availability/coverage.
  > 7. Enforce/report every §15.5 cap from the first job, all attempts and independent review;
  >    preserve historical debits/monitoring limitations. Exhaustion yields BLOCKED/INCOMPLETE,
  >    never implicit permission to impute unfinished extraction or shrink evaluation.
  > 8. Supply protocol, lineage, decoded weather/features, predictions, metrics/diagnostics,
  >    uncertainty, criteria, failure/resource logs, rights notices and executable reproduction
  >    commands; preserve invalid outputs/repairs and run relevant inherited regression guards.
  > 9. Obtain **one fresh independent Integration-Critic PASS** binding the exact final candidate
  >    in a clean detached checkout and this entire checklist, with independent saved-vector
  >    metrics/paired uncertainty and representative conversion/component/causal/state reproduction.
  > 10. Return canonical packet, final candidate and evidence-tip SHAs, evidence-only terminal
  >     delta, reachable history, all resources and branch/worktree accounting; stop at CP-20's
  >     local result. No mainline action, publication, later checkpoint or executor self-ratification.

  Confirm it appears verbatim in `capstone_v21.md` at this SHA.

## What to verify
The complete §15.6 checklist, items 1–10, item by item: contract consistency, hard invariants,
reported metrics, reproduction, documentation. Recompute independently with your own code. Do not
redesign. Item 9 is this review. Item 10 is completed by the Lead after your verdict (return packet,
evidence-tip SHA, evidence-only delta). Verify what is checkable for it at the candidate and state
what remains.

Artifact paths (at the candidate):
- `reports/weather-ablation/`, `src/cp20/`, `scripts/cp20_weather.py`,
  `tests/cp20/`, `docs/track-b/evidence/cp-20/`.
- Decision-bearing inputs:
  - CP-20: `reports/weather-ablation/run-manifest.json`, `protocol.json`, `lineage.json`,
    `weather-features.parquet`, `messages.parquet`, `predictions.parquet`.
  - Inherited: `reports/cp15/`, `reports/v2-causal/predictions.parquet` and `lineage.json`,
    `data/snapshot.parquet`, `data/partitions.json`, `reports/weather-admission/`.
- Repair and decision records: `reports/weather-ablation/extraction-repairs.json`,
  `post-freeze-repairs.json`, `chain-code-versions.json`, `locator-fix-verification.json`.
- Local evidence (not committed):
  - `/Users/djourno/Downloads/PJM/.local/artifacts/cp-20/`: `ledger/budget.json`,
    `weather/runs/*.npz|json`, `weather/raw/` (retained raw target messages),
    `weather/attempt-outcomes.jsonl`, `weather/requests.jsonl`, `hg-components/`.
  - Admission retained raw samples: `/Users/djourno/Downloads/PJM/.local/weather-admission/cache/gfs/`.

## Reproduction
- Environments: modelling `PY=/Users/djourno/Downloads/PJM/.venv/bin/python`; decoding
  `WX=/Users/djourno/Downloads/PJM/.local/artifacts/cp-20/wx-venv/bin/python` (ecCodes).
- Commands: `reports/weather-ablation/reproduce.md` at the candidate.
- Run every compute command through the monitor from the Critic worktree:
  `cd /Users/djourno/Downloads/PJM/.local/worktrees/cp-20/critic-2 && $PY scripts/cp20_weather.py --monitor --name critic2-<x> --workers 1 --log /Users/djourno/Downloads/PJM/.local/artifacts/cp-20/critic-2/logs/critic2-<x>.log -- <command>`
  The monitor sets `PYTHONPATH` to the worktree's `src`, `CP20_LEDGER` to the shared cumulative
  ledger, and BLAS threads to 1.
- Expected output or tolerance:
  - H0 vectors bitwise equal to the accepted CP-16 V2-H vectors
    (`reports/v2-causal/predictions.parquet`, policy `V2-H`) on all 10,747 keys.
  - Component reproduction: atol 1e-8 and rtol 1e-10 against the cached HG/H0 components, with
    fingerprint equality.
  - Controls:
    - Exactly 0.0 change for the delivery-day/future masks and the future-weather mutation.
    - Change above 1e-6 EUR/MWh for the positive controls.
  - Recomputed metrics and the paired HG−H0 bootstrap (seed 15042, 2,000 replicates, 7-day
    blocks, one shared index set) match `metrics.csv` and `uncertainty.csv` to ≤1e-9 absolute.
  - Joint rule: upper CI(ΔS_WIS) < 0 AND upper CI(ΔS_MAE) ≤ 0, applied to the paired differences.
  - Conversion reconstructed from retained raw messages with your own decode matches the stored
    features to ≤1e-9 for the reconstructed hours; retained-sample byte identity by sha256.
  - Contract counts: 2,476 runs × 10 leads × 5 fields (123,800 target messages); 10,747 keys;
    21,494 contrast rows; 75,229 scored rows.

## Resources (shared cumulative §15.5 ledger; reserve before use)
- Allotment for this review:
  - ≤10 monitor-charged machine-hours with 1 worker.
  - ≤1 analysis pass and ≤1 reference pass (the last of each under the §15.5 caps).
  - ≤1,400 policy-days.
  - ≤40 component-day attempts (non-main) and ≤6,000 primitive fits.
  - No network access at all (0 transfer).
  - Decode only retained raw messages listed in
    `/Users/djourno/Downloads/PJM/.local/artifacts/cp-20/critic-2/eligible-decodes.txt`
    (sha256 d35faaa4b4114edce9207823b2bf6f373f75e8bd64d6908bb6e3ca49a86e88f8), each at most once. The
    list keeps every target message within 3 decode/extraction tries including reviews.
- Charging, with `from cp20.budget import Budget; b = Budget(os.environ['CP20_LEDGER'])`:
  - `b.reserve(policy_days=n)` before replaying n policy-days.
  - Component refits run inside `cp20.components.counted_fits(b, main=False)`.
  - `b.reserve(analysis_passes=1, reference_passes=1)` before your scoring pass.
  - `b.reserve(message_attempts=1)` before each raw decode.
  - A refusal (`CapExceeded`) means stop and report it. Never edit, reset or recreate the ledger.
- Write scripts, logs and outputs only under `/Users/djourno/Downloads/PJM/.local/artifacts/cp-20/critic-2/`
  (pytest `--basetemp` under `/Users/djourno/Downloads/PJM/.local/tmp/cp-20/critic-2/`; use
  `-p no:cacheprovider` and `PYTHONDONTWRITEBYTECODE=1`).

## Verdict
- Write one markdown verdict in the form of `docs/track-b/gauntlet-templates.md` §2 to
  `/Users/djourno/Downloads/PJM/.local/artifacts/cp-20/critic-2/integration.md`. The Lead commits it
  as `docs/track-b/evidence/cp-20/integration.md`.
- Confirm the worktree is clean before writing it. Leave the worktree in place; the Lead removes it.
