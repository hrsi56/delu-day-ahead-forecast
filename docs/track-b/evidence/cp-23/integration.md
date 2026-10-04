# Verdict — CP-23 — Integration — PASS

- **Candidate SHA:** `f9a737eb2bb8ccdb93c0de5cf1449630ee246e90` (local branch `gauntlet/cp-23`; branch base `a4acd792954c577e60235c427380c82031c4372a` = `main` = `origin/main`, a direct child of the v21-r10 ratification `3f7aaf24bf8f5793dd9aba2d88ae8128fef80045` that changes only `progress.md`)
- **Plan / version / bar:** `capstone_v21.md`, revision **v21-r10**, SHA-256 `6873c2501067c63692ec7cb79dfd4073164a8a014edbd6ebc23169e7e8ff6709` (equal at the candidate, on `main` and in the issued brief); bar **§21.10 "Complete CP-23 acceptance checklist", all sixteen items**, governed by §21.1–§21.9 and §21.11 with the §17.3–§17.9, §20.4–§20.7, §14.6, §8 and §18 inheritances.
- **Reviewer:** one fresh, independent Integration Critic session, launched with `scripts/gauntlet.py critic-open` and `critic-brief cp-23` (record `critic-1`, opened 2026-10-04T17:16:27Z; assignment SHA-256 `4083b6421e8336f126397d5ffe2dbf6e5f0680013cfc2c123a5acea1891bbf63`, unchanged). It received only the generated brief: no Builder checkout, diff, reasoning, summary or conversation history. The Lead's `.local/artifacts/cp-23/` working notes (`launch-envelope.md`, `draft-brief.md`, `progress-commit-message.txt`) were not opened. Isolation is cooperative: a clean detached `git worktree`, no read-only mount.
- **Worktree clean before and after:** yes. `git -C /Users/djourno/Downloads/PJM/.local/worktrees/cp-23/critic-1 status --porcelain` was empty, and `HEAD` was `f9a737eb2bb8ccdb93c0de5cf1449630ee246e90`, at the start, after every job and before this verdict was written. The CI payload build wrote only the ignored `reports/cp3b/payload.json`.
- **Verbatim bar excerpt** (the brief's excerpt, checked against the file at the candidate with `bar.py check`; see the commands below). The excerpt is the citation. Any line number is a courtesy and is non-binding.

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

## Commands actually run

`WT` = `/Users/djourno/Downloads/PJM/.local/worktrees/cp-23/critic-1`; `PY` = `/Users/djourno/Downloads/PJM/.venv/bin/python`; `MON` = `$PY scripts/cp23_ddnn.py monitor --workers 1 --log /Users/djourno/Downloads/PJM/.local/artifacts/cp-23/critic-logs/<name>.log --name <name> --`, run from `WT` with `MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1 MLFLOW_DISABLE_AGENT_HINT=1`. Results were written to `/Users/djourno/Downloads/PJM/.local/artifacts/cp-23/critic-1/out/`, outside the worktree. No command made a network call.

**Required check 1: recompute the metrics, intervals, readings and verdict**

- `MON(critic1-score) $PY -m cp23.review --out …/out/score.json --score` → monitor exit 0, 4.2 s.
- Observed: metrics 70/70 rows, uncertainty 84/84, criteria 105/105.
  - `unmatched` 0 and `nan_pattern_mismatches` 0 for all three.
  - `max_abs_numeric_difference`: metrics 5.68e-14, uncertainty 4.44e-16, criteria 3.55e-15 (all ≤ 1e-12).
  - `verdict_equal`, `first_unmet_equal`, `unmet_equal` and `readings_equal` are all true.
- This command reuses the Lead's `cp23.scoring`, so it shows reproduction, not independence. The independent recomputation is check 1b.

**Check 1b: independent recomputation (the Critic's own code)**

- `MON(critic1-independent-score) $PY …/out/critic_score.py …/out/independent-score.json` → monitor exit 0. The script was run from the session scratchpad and then moved, unchanged, to `/Users/djourno/Downloads/PJM/.local/artifacts/cp-23/critic-1/out/critic_score.py` (SHA-256 `96ce693c73601ff5261c4c09c7c3490f3cf75306fd4ee58895884075e8fbe120`).
  - The script is written from the text of §14.3, §14.4, §17.5, §8, §21.2 and §21.6. It imports no project scoring code; its only project import is the ledger, to reserve one reference pass and one bootstrap pass.
  - It computes:
    - emitted-p50 AE and WIS with weights α/2 and ½ and divisor 3.5;
    - equal-fold B0 ratios;
    - its own seed-15042 index set: 13 noncircular 7-day blocks per replicate, starts 0–83, truncated to 90;
    - the 7 contrasts, ratio intervals and per-fold paired daily-loss intervals;
    - §8 for v5, v3+D, D, v3 and v4, and the rule.
- Observed:
  - The index-set fingerprint is `e1df9a68dc6715aa2ecd9705ef61f504a3fe109ed917d1151ccbc46ea9e0f99b`, equal to CP-20's.
  - Against the committed tables, the maximum absolute differences are:
    - equal-fold S for all 10 policies: 2.2e-16;
    - per-fold MAE, WIS and cov95: 7.1e-15;
    - pooled MAE, WIS, cov50/80/95 and mean width95: 2.8e-14;
    - all 84 contrast rows (difference, CI, ratio and ratio CI, equal-fold and per fold): 4.3e-14.
  - All 7 readings are equal.
  - §8: v5, v3+D, v3 and v4 meet all six. D fails 1 (S_MAE 0.6319 > 0.5920) and 5 (fold_3 MAE 58.84 > 56.71). Both match `criteria.csv`.
  - Rule: unmet [1, 4], first unmet 1. Only fold_3 MAE is decisively worse. Both match `decisions.json`.

**Required check 2: rerun the PyTorch reference checks**

- `CP23_REFERENCE_ERRORS=…/out/torch-max-errors.json MON(critic1-torch) $PY -m pytest -q -p no:cacheprovider -rA tests/cp23/torch_reference_checks.py` → monitor exit 0.
  - Output: "26 passed, 1 warning in 4.42s", with 0 failed, skipped or errored.
  - The warning is PyTorch's own `requires_grad` scalar-conversion notice in the test's helper.
- torch 2.14.1 and numpy 2.4.6.
- 142 check groups. The worst observed error is 3.3e-4 of its frozen bound (`cdf_at_quantiles`). The other kinds are ≤ 2.9e-4 of their bounds, and the trajectories ≤ 7.3e-8.
- Run as plain pytest, as the brief says, rather than through the `reference-checks` job. That job rewrites the tracked `reference-checks.json`, and the ledger's uncapped `reference_check_runs` counter therefore stays at 1.

**Check 2b: a missing PyTorch fails rather than skips**

- `$PY -c "sys.modules['torch']=None; pytest.main([... torch_reference_checks.py])"` → "ERROR tests/cp23/torch_reference_checks.py … 1 error during collection", pytest exit code 2, 0 skipped.

**Required check 3: reproduce a representative DDNN fit, its ensemble and its quantile emission**

- `MON(critic1-ddnn) $PY -m cp23.review --out …/out/ddnn.json --ddnn fold_3:2022-08-20 --ddnn fold_4:2025-06-26 --ddnn fold_5:2026-04-07` → monitor exit 0, 75.1 s, 12 member fits charged as review.
  - fold_3 is the brief's origin. fold_4 and fold_5 are the Critic's own choice: the 2025 fold where CP-22's candidates failed, and the last date permitted.
- Observed at all three origins (configurations C2, C3 and C4), every boolean is true:
  - D's central and quantiles are bitwise equal to the committed `predictions.parquet`;
  - D equals the `members.parquet` D column;
  - each member's `params_sha256`, `best_epoch` and `epochs_run` equal `fits.parquet`;
  - the quantiles are finite and strictly ordered;
  - the p50 is the central forecast, and the ensemble is the mean of the member z-quantiles.
- `crossed_rows` is 0 everywhere, and n_hours is 24 at each origin.

**Required check 4: re-derive the packet** (`PYTHONPATH=src`, telemetry disabled; each exit 0)

- `$PY -m cp23.packet --check` → `{"draft_registry_identical_to_committed": true}`.
- `$PY -m cp23.claims --check` → `identical_to_committed`: true for both `cp23-claims.md` and `publication-packet.md`; `lint_findings` [].
- `$PY scripts/mlflow_export.py --draft cp23 --check` → "the committed draft export is current".
- `$PY scripts/mlflow_export.py --check` → "the committed export is current".
- `cp23.report.build(Path('.'))` was evaluated in memory, writing nothing. It equals the committed `report.md` byte for byte (14,819 characters).

**Check 5: replay v5 through the H layer**

- `MON(critic1-replay) $PY -m cp23.review --out …/out/replay.json --replay v5:fold_4:2025-05-01:2025-05-14` → monitor exit 0, 14 policy-days charged as review.
- Observed: `bitwise_equal` true, 336 rows, admission-freeze commit `ded8fc1c70b0ad7b1d7091b467631aa7f65a197d`.

**Other checks (no fit, no pass)**

- `$PY -m pytest -q -p no:cacheprovider tests/cp23` → "41 passed in 7.42s", exit 0.
- `PYTHONPATH=src $PY -c "…check_protocol(Path('.'))"` → returned the protocol, raising nothing; exit 0.
  - `protocol.json` has blob `a7018661bc3d…` at both the freeze commit `a008c47` and the candidate.
- The CI sequence, run in the worktree:
  - `$PY scripts/build_wasm_payload.py` → exit 0 (writes ignored files only);
  - `$PY -m pytest -q -p no:cacheprovider` → "1363 passed, 8 skipped in 205.17s", exit 0;
  - `$PY scripts/verify_release.py` → "PASS — every bound claim agrees on every surface", exit 0;
  - `python3 scripts/publication_guard.py tree` → "the tree carries no placeholder and a final build record", exit 0.
- `$PY -m pytest -rs tests/test_10_cqr_order_statistic.py tests/test_22_wasm_equivalence.py` → 23 passed.
- The 8 suite skips, listed with `-rs`, are all in pre-CP-23 files: eccodes not installed; marimo not installed; CP-16's identity bound to the v21-r3 anchor; and five CP-16 production checks gated on `CP16_LEDGER`.
- Git inspection, read-only:
  - `git log --format='%H %cI %s' main..f9a737e`;
  - `git diff --stat` and `--name-only main...f9a737e`;
  - per-commit `git diff --stat <c>^ <c> -- src scripts tests pyproject.toml uv.lock`;
  - `git rev-parse <tag>:<path>` for the saved vectors at `land/cp-20`, `land/cp-21`, `land/cp-22`, `main` and the candidate;
  - `git check-attr text`;
  - `git branch -a -vv`, `git stash list`, `git worktree list`.
- `shasum -a 256` of the anchor, the brief (worktree, `.local` canonical copy and blob at `cb9ba29`), PUBLISH_RULES at `main` and at the candidate, the claim map, the draft export and the packet template.
- Ledger reads: `scripts/cp23_ddnn.py status`, and the job list from `.local/artifacts/cp-23/ledger/budget.json`.
- `git show main:scripts/bar.py | python3 -I - check <this verdict> --source capstone_v21.md@f9a737eb2bb8ccdb93c0de5cf1449630ee246e90` → "ok: lines 9–63 (3227 bytes) appear in capstone_v21.md@f9a737eb2bb8", exit 0. The section's identity from `critic-brief` is 55 lines, 3,228 bytes, SHA-256 `39ed41f4…65f5cc`; the one-byte difference is the trailing newline. After that check only text outside the excerpt was edited.
- Final state: `git -C $WT status --porcelain` empty (exit 0); `git -C $WT rev-parse HEAD` → `f9a737eb2bb8ccdb93c0de5cf1449630ee246e90`.

## Evidence actually inspected

- **The plan:** `capstone_v21.md` §21 (all subsections), §20.4–§20.5, §17.3, §17.5–§17.6, §14.3–§14.4, §14.6, §15.4 and §8. Also the handoff's 4.6L use table in `docs/track-b/v3-plan-handoff-2026-09-22.md`.
- **The evidence:** `docs/track-b/evidence/cp-23/issued-brief.md`, `publication-packet.md` and `.gitattributes`; `docs/track-b/research-content/cp23-claims.md` (its sections, and the withheld claims W35–W41).
- **Reports:** `reports/distribution-challenger/`:
  - `report.md`, `licence-admission.md`, `resource-admission.md`, `protocol.json` (pins, rules, `owner_rulings`, tolerances, DDNN block) and `selection.json`;
  - `controls.json` (all 61 checks, field by field), `parity.json`, `reproduction.json` and `preflight/input-verification.json`;
  - `preflight/weather-regeneration.json`, `daily-cycle.json`, `resources.json`, `defects-and-repairs.md`, `failures.csv` (header only) and `reproduce.md`;
  - `published-export-diff.json`, `artifact-manifest.json` (all 86 hashes checked against the files and the committed blobs: 0 mismatches) and `.gitattributes`;
  - `diagnostics/*.csv`, `metrics.csv`, `uncertainty.csv`, `criteria.csv`, `decisions.json`, `predictions.parquet`, `members.parquet` and `fits.parquet`.
- **Code:**
  - `src/cp23/ddnn.py` (imports, JSU head, quantiles, Adam, ensemble, emission, selection), `member.py`, `features.py` (docstring and windows), `audit.py`, `reference.py`, `review.py`, `scoring.py`, `evaluate.py`, `budget.py`, `admission.py` (the evaluation cutoff guard) and the `daily.py` diff;
  - `scripts/cp23_ddnn.py`, `tests/cp23/test_numpy_only.py`, the `test_ddnn_gradients.py` header and test list, and `tests/cp23/torch_reference_checks.py`;
  - `src/cp20/scoring.py` (`_indices`, `_bootstrap`) and `.github/workflows/tests.yml`.
- **Local state:** `.local/artifacts/cp-23/start.json`, `critic-open.json`, the ledger and `reference/runs.jsonl`.
- **For precedent:** `main:docs/track-b/evidence/cp-22/integration.md`.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1 | Starting state; anchor SHA-256; baseline; brief packaged byte for byte | **PASS** | Anchor `6873c250…f6709` in the brief = the file at the candidate = `main`. `start.json` recorded at 2026-10-04T14:22:50Z: HEAD = main = origin/main = `a4acd79`, one worktree, no stash, clean. The first branch commit `cb9ba29` (5 s later) adds only `issued-brief.md`. Its blob, the worktree file and the `.local` canonical copy all hash `33f6b412…502d0c`. Every ref in `start.json` is still present and unmoved; the only new ref is `refs/heads/gauntlet/cp-23`. |
| 2 | 4.6L complete, every use dispositioned | **PASS** | `licence-admission.md`: original MIT code; method sources cited; no third-party code or weights. Each of the seven test-only packages is listed with version, wheel source, licence and the 2026-10-04 check date. All seven handoff uses carry a disposition with conditions: research and retention are permitted; publishing, local operation and demo are licence-permitted but not authorized by CP-23; hosted service and product are unresolved and carried to 4.7 and 4.10. The record states under one active hour (cap 4). |
| 3 | §21.3: import audit, finite-difference gradients, PyTorch reference passing at frozen tolerances and not silently skippable | **PASS** | Audit: AST-based, NumPy and stdlib only; its 7 framework or relative-import fixtures fail it. Gradient tests cover the JSU partials and every layer of every configuration, with wrong-gradient positive controls. Within the 41 passed. The reference was rerun at 26/26 with worst error 3.3e-4 of bound. The tolerances, `ddnn.py` and the check file were committed in `cd56434` before the only recorded run (14:55:17Z) and are unchanged since. With torch hidden, collection errors (exit 2), and the job requires exactly 26 passed with 0 skipped. The pin sits in the separate test-only lock `tests/cp23/torch-reference/` under the Owner's recorded ruling (`protocol.json` `owner_rulings`); the root `uv.lock` and `pyproject.toml` are unchanged. |
| 4 | 4.6R on training data only, measured values, projection, PASS/NOT_ADMITTED | **PASS** | `resource-admission.md` and `.json`: PASS. Two warm-up-start origins (fold 1 and fold 5), with data loaded `before=` each fold's evaluation start and a guard refusing any evaluation date (`admission.py`). Accuracy-blind. Peak 0.72 GiB; fit and prediction times; finite, ordered emission. The projection is inside every §21.8 cap (2,624/4,000 main fits; 4,560/6,000 total; 15.2/60 machine-hours; 4,902/8,000 policy-days; 3.87/10 GiB). |
| 5 | Frozen pre-run protocol committed before any evaluation fit | **PASS** | Protocol commit `a008c47` at 15:10:03Z. The ledger's first post-freeze fit jobs are `select` 15:10:12Z, `fits-warmup` 15:11:24Z and `fits-evaluation` 15:18:59Z. The only earlier DDNN fits are 4.6R's 32 training-only fits, which §21.4 orders first. The blob is unchanged since the freeze, and `check_protocol` passes (every pinned implementation and input hash is current). No decision-bearing module changed after the freeze. Post-freeze code commits only add modules (controls, daily, diagnostics, packet, report, claims, finalise, review, tracking), plus one recorded `daily.py` repair to a descriptive side field. The rule text equals §21.6's four conditions. |
| 6 | Inputs: population, manifest, frozen weather; saved-vector identities; independent HG and v4 slice; no retrieval; nothing after 2026-04-07 | **PASS** | Manifest: 638 origins (127+127+127+130+127) and 10,747 keys. Weather rebuilt from CP-20's retained grids: retrieval none, values bitwise equal, max date 2026-04-07. The saved vectors (weather-ablation, block-challenger and cp15 predictions), weather features, snapshot and partitions are blob-identical to `land/cp-20`, `land/cp-21`, `land/cp-22` and `main`. `reproduction.json`: HG's central, v4's central, L-N and L-R are bitwise equal at 2021-04-01 (fold_2) and 2026-01-08 (fold_5). The maximum delivery date of every policy is 2026-04-07 (Critic's check). |
| 7 | Exactly DDNN, v5 and the arms; training-only selection and early stopping; composite parity | **PASS** | DDNN: NumPy-only, ELU network with a JSU head; information exactly §17.3's (CP-15's 23 features, 3 GFS columns, 3 indicators under §15.3); §4 target. History is `[max(2019-01-01, D−728), D)`, early stopping on `[D−28, D)`, four seeds, z-space quantile averaging, sort-rearrangement counted. Critic's check of `selection.json` and `fits.parquet`: each fold's train/stop/holdout windows sit exactly before D0, the chosen configuration is the holdout-MAE argmin, and every origin fit in a fold uses only that configuration with seeds 42–45. Parity (Critic): max \|c_v5 − (2/3)c_v4 − (1/3)D\| = 1.7e-13 and max \|c_v3+D − (2/3)c_HG − (1/3)D\| = 1.7e-13, both ≤ 1e-9. v5 and v3+D run on the H path (`controls.json`), and D uses its own JSU quantiles. |
| 8 | Every §21.7 and inherited control, each negative paired with a positive | **PASS** | `controls.json`: 61 checks, `all_passed` true. Delivery-day and future masking give exactly 0.0, paired with the non-uniform D−1 mutation, which moves D, v5 and v3+D. Future weather gives 0.0, paired with target-day weather rearrangement and cross-date permutation, which move. Validation-outcome mutation changes early stopping (best epochs [19,4,7,5] → [1,1,1,1]). Evaluation outcomes leave selection identical, while holdout outcomes change the selection losses. Also: determinism bitwise against the main run; restart replay; release rules (consume once, D−1 refused, D−2 accepted, partial day, duplicate); tampered or wrong-identity cache refusals; boundary guard (accepts 2026-04-07, refuses 2026-04-08); DST 23/25 hours; composite parity; import audit, gradient and reference records. |
| 9 | All 10,747 keys per new policy; finite, ordered quantiles; p50 separate from central | **PASS** | Critic's check: v5, v3+D and D each have exactly the 10,747 CP-15 B0 keys with no duplicates, finite central and quantiles, strictly increasing quantiles, and y_true equal to B0's. For v5 and v3+D, the p50 equals the central forecast on 0 rows (H-layer median residual). For D, p50 = central on all rows, as §21.2 defines. 0 rows rearranged. |
| 10 | Score every policy; independently verify scores, diagnostics, coverage with width, all six §8 diagnostics per new policy | **PASS** | Check 1 reproduces the tables. Check 1b recomputes all 10 policies' scores, coverage and widths, every interval, and §8 for every new policy with independent code (max difference 4.3e-14). D's calibration by level was recomputed from `predictions.parquet` and equals `diagnostics/calibration-by-level.csv`. |
| 11 | Apply `cp23-adoption` mechanically; decision, first unmet condition, every §21.5 contrast reading; statuses distinct | **PASS** | v5 is not adopted and CP-23 becomes the branch "DDNN member on v4". First unmet is 1: ΔS_MAE 0.0064 [−0.0016, 0.0149] and ΔS_WIS 0.0071 [−0.0009, 0.0138]. Condition 4 is also unmet (fold_3 MAE 1.915 [0.301, 4.395]). Conditions 2 and 3 (keys) are met. All seven contrasts are read (v5−v4 no demonstrated joint preference; D−v4 and D−v3 observed joint worsening; the others observed joint improvement), and each equals the Critic's recomputation. Engineering (bound to this verdict), research (development_post_selection) and product (v1 unchanged) are stated separately in `report.md` and `decisions.json`. |
| 12 | §21.5 diagnostics delivered to `reports/distribution-challenger/` | **PASS** | Present: calibration by level and PIT; extrapolation (26 extreme days, beside CP-22's tree record); peak and fold 4; seed stability and epochs; the configuration per fold; fit cost (`fit-cost.json`, by origin, `fits.parquet`). The cold daily cycle has 25 origins, 5 per fold, four workers, and every bitwise check true. v4's component cycle is CP-21's committed figure, a disclosed design note. |
| 13 | Every §21.8 cap enforced and reported; calendar respected | **PASS** | `budget.py` `CAPS` equal §21.8 and are reserved before use. The monitor enforces workers, RSS, disk, machine-hours, active hours and the calendar. `resources.json` reports each cap against use. Live ledger after this review: main fits 2,624/4,000; total 2,856/6,000; policy-days 3,293/8,000; reference passes 3/3; bootstrap passes 3/3; machine time 2.25/60 h; peak RSS 3.19/10 GiB; peak added disk 0.30/10 GiB (322,106,383 bytes, which counts the Critic worktree's checkout by the monitor's rule); data 0 B and remote writes 0. The test dependency's 137,444,189 bytes are recorded separately. Every ledger job started and ended on Sunday 2026-10-04, Asia/Jerusalem. |
| 14 | Durable evidence, executable reproduction, byte-exact storage; packet and draft export; public surfaces and published export unchanged; CI green; no public write | **PASS** | `reproduce.md` gives the job sequence the ledger shows, with commit points. Byte-exact storage: `* -text` on `evidence/cp-23/` and `reports/distribution-challenger/`, and 86/86 manifest hashes equal the files and the committed blobs. The packet completes every template section (1–8, 5a–5d), with §5b and §5d not applicable. Its §4 values equal `uncertainty.csv` L72–L75 and the per-fold `metrics.csv` rows, and its claim-map and draft-export hashes match. All four re-derivation checks pass. The published-export diff is 28→28 runs, identity only, no substantive change. The changed paths lie inside §21.11, with no public surface. CI sequence green (above). No remote-tracking ref for CP-23, and origin/main = main. |
| 15 | One fresh, independent Integration-Critic PASS on a clean detached checkout; launched with critic-open, critic-brief, critic-close; independent recomputation, reference rerun, DDNN reproduction, packet re-derivation | **PASS (this verdict)** | Launched with `critic-open` (record critic-1) and `critic-brief cp-23`, on the clean detached worktree at the full candidate SHA. All four required independent checks were performed and passed (checks 1/1b, 2, 3 and 4 above). `critic-close` is the Lead's next step. |
| 16 | Return the canonical packet (templates §3), checked with `scripts/gauntlet.py return` | **Not yet due — the Lead's post-verdict obligation** | It cannot exist at the candidate. The return must add: `evidence_tip_sha`; the verdict-only delta (`git diff --name-only f9a737eb2bb8ccdb93c0de5cf1449630ee246e90..<evidence_tip>` must stay inside `docs/track-b/evidence/cp-23/`); final resource totals including this review (2 reference passes, 2 bootstrap passes, 12 DDNN review fits and 14 review policy-days, all charged to the ledger); and branch, worktree and stash accounting (`gauntlet/cp-23`, `.local/worktrees/cp-23/critic-1`, no stash). |

## Observations (non-blocking)

1. **The review exhausted the scoring allowance.** It spent both permitted metric-only reference passes and both bootstrap passes. One went to the brief's `cp23.review --score`, the other to the Critic's independent recomputation. The ledger now stands at 3/3 for each, so any re-scoring of a changed candidate would exceed §21.8.
2. **PyTorch is installed in the project `.venv`.** It came from the separate test lock's hashed requirements. A plain `uv sync --locked` would remove it, and the reference step would then fail loudly at collection, as shown, rather than skip.
3. **The selection positive control changes the losses, not the choice.** Under holdout-outcome mutation the configuration losses change (fold_1: 4.18 → 82.8 for C2) but the choice stays C2. This is an adequate pairing, because the negative assertion compares the same loss vector, which stays bit-identical under evaluation-outcome mutation.
4. **Two pre-run timestamps share a second.** The tolerance commit `cd56434` and the `reference-checks` job start fall in the same second (14:55:11Z); `runs.jsonl` holds the single recorded run, made after the commit.
