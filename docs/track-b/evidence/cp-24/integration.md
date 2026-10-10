# Verdict — CP-24 — Integration — PASS

- **Candidate SHA:** `7949a98f80c81c5a789dd69c213da16c811d345c` (local branch `gauntlet/cp-24`; base `522d7ea722b5d215d827d7aed9c56b7a9dec066e`; `main` = `origin/main` = `7ff6a50cb54ad34a7f0e52981e18f990fa0323bb`, moved by the Owner, not by CP-24).
- **Plan / version / bar:** `capstone_v21.md`, revision **v21-r11**, SHA-256 `11068e3f57bd9277be50db62d109f3e7d8ea7b8fdfa042886ccc4ae5ab1ed2d2` at the candidate. Bar: **§23.13 "Complete CP-24 acceptance checklist", all eighteen items**, governed by §23.1–§23.12 and §23.14 with their inheritances. Also checked: the continuation brief's three conditions (`docs/track-b/evidence/cp-24/continuation-brief.md`, SHA-256 `5960b90855910c8deb433b83ffedd93add7c494fcc10833a5f25f2b16686e4ec`), the repair after the third review's FAIL, and the work-availability supersession. Section identity from the generated brief: 77 lines, 4,591 bytes, SHA-256 `5ffb90a3bd275ad59cc8fd8d60103a683ba590b946bda1a54e50211e1b164abe`.
- **Reviewer:** one fresh Integration Critic session (record `critic-4`, opened 2026-10-10T19:53:52Z, assignment SHA-256 `b0ee87f9…48b3`, re-checked unchanged by `critic-brief`). It was launched with the prompt `git show main:scripts/gauntlet.py | python3 -I - critic-brief cp-24` and worked from that generated brief.
  - **What it read beyond the brief:** `AGENTS.md` on `main`, as `CLAUDE.md` requires before acting, and the third review's committed verdict, which the assignment permits.
  - **What it did not open:** `.local/artifacts/cp-24/critic-1/`, `critic-2/` or `critic-3/`, the Lead's worktree, the Lead's notes, `progress.md` and `orchestrator-role.md`.
  - **Disclosure:** the session's harness context carried the Owner's auto-memory index, and one memory note was read at orientation. Nothing in this review relied on either.
  - **Isolation is cooperative:** a clean detached `git worktree` at `.local/worktrees/cp-24/critic-4`, with no read-only mount.
- **Worktree clean before and after:** yes. `git -C /Users/djourno/Downloads/PJM/.local/worktrees/cp-24/critic-4 status --porcelain` was empty, with `HEAD` = `7949a98f80c81c5a789dd69c213da16c811d345c`, at the start, after every job and immediately before this verdict was written. Two kinds of ignored byproduct appeared inside the worktree, which the protocol allows:
  - the browser payload `app/public/`, which CI also builds; it rewrote the tracked `reports/cp3b/payload.json` byte-identically;
  - `__pycache__/` directories.
- **Verbatim bar excerpt** (from the generated brief; checked against the file at the candidate with `bar.py check`, command 22). The excerpt is the citation. Any line number is a courtesy and is non-binding.

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

## Summary

PASS. All eighteen items verify at the candidate, or are not yet due by construction: item 18 is the Lead's return, which follows this verdict. The continuation's three conditions hold. The repair that the third review's FAIL asked for is complete and exact.

**The result reproduces under independent recomputation.** This review's own code (it imports no CP-24 scoring code) recomputes the following from the committed rows:

- every new-policy metric;
- S_MAE and S_WIS;
- every 95% and 97.5% interval, both differences and ratios;
- the six §8 criteria for v5, v3+D2 and D2;
- `cp24-adoption`, from scratch.

All agree with the committed tables to within 1e-13. v5 is adopted in attempt 1:

- ΔS_MAE −0.01334, with 97.5% interval [−0.01659, −0.00914], which is −2.49% of v4's score, 97.5% [−3.04%, −1.68%];
- ΔS_WIS −0.01191, with 97.5% interval [−0.01469, −0.00838], which is −2.36%, 97.5% [−2.86%, −1.62%].

**The stored bootstrap draws are genuine.** For one contrast, v5 − v4, 200 of the 2,000 replicates were regenerated from the CP-20 index set, re-implemented here (its fingerprint `e1df9a68…` is equal). They match the stored draws in every fold and equal-fold to within 6.4e-14.

**Representative reproduction, all bitwise:**

- the gate;
- a fold-4 search trial whose window excludes 174 uncovered weather days;
- two eight-member ensembles with their emission, including the 23-hour DST day 2026-03-29;
- two H-layer replays.

**This review's own harsher leakage test** was run at an origin not used by the committed controls (fold 3, 2022-08-25). It reproduces the committed D2 bit for bit with every outcome on or after D replaced by random values, and again with every row after D truncated. Moving D−1's prices moves the forecast.

**Non-blocking observations** are below. O1 is a factual error in `defects-and-repairs.md` item 11, and the return must correct it.

## Commands actually run

All compute ran under the CP-24 monitor (`$MON` = `$PY scripts/cp24_ddnn2.py monitor --workers 1 --name critic4-… --log …`) from the worktree, with `MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1 CP24_PROJECT_ROOT=/Users/djourno/Downloads/PJM`. Logs and outputs are under `/Users/djourno/Downloads/PJM/.local/artifacts/cp-24/critic-4/`. This review's own scripts are under `critic-4/scripts/`.

1. **Starting state.** `git -C <wt> status --porcelain`, then `git rev-parse HEAD`. Exit 0: empty, and `7949a98f80c81c5a789dd69c213da16c811d345c`.
2. **Identities.** `shasum -a 256` of the following, each equal to its expected value:
   - `capstone_v21.md`: `11068e3f…`;
   - `docs/track-b/evidence/cp-24/issued-brief.md` and `.local/artifacts/cp-24/issued-brief.md`: both `a3f11470…`, `cmp` identical;
   - `continuation-brief.md` and its canonical file: both `5960b908…`, `cmp` identical;
   - `docs/PUBLISH_RULES.md`: `5a660864…`;
   - `docs/track-b/publication-packet-template.md`: `4efb0185…`;
   - `docs/track-b/capstone_v21-r10-to-v21-r11-amendments.md`: `474017e1…`;
   - `tests/cp23/torch-reference/uv.lock`: `b3164a37…`.

   `git rev-parse main origin/main` gives `7ff6a50c…` for both. `522d7ea` is an ancestor of the candidate, which is 32 commits above it.
3. **Diffs.**
   - `git diff --stat 7ea9bdd73fb7df50991083e674c4dad24335aaf0 HEAD`: 13 files, +861/−76. They are the claim map, packet, report, `reproduce.md`, `resources.json`, `defects-and-repairs.md`, `artifact-manifest.json`, `src/cp24/{claims,ratios,report}.py`, `tests/cp24/test_ratio_intervals.py`, the new `attempt-1/ratio-intervals.csv` and the committed critic-3 verdict.
   - `git diff --name-status 522d7ea HEAD`: 118 entries, all `A`, all under §23.14's write paths.
4. **Generators and export,** each `PYTHONPATH=src $PY -m …`. All exit 0:
   - `cp24.packet --check`: `{"draft_registry_identical_to_committed": true}`;
   - `cp24.claims --check`: identical, and `lint_findings: []`;
   - `cp24.report --check`: identical;
   - `cp24.basetree --check`: `unchanged: true`;
   - `cp24.basetree --check-rev 7949a98f…`: 1,322 recorded files unchanged, 118 added under CP-24 paths, `problems: []`;
   - `cp24.export --attempt 1 --check`: "the committed draft export is current";
   - `cp24.ratios --attempt 1 --check`: identical;
   - `$PY scripts/mlflow_export.py --check`: "the committed export is current".

   As the positive control, `cp24.basetree --check-rev 7ff6a50` exits 1 and lists the 20 base files `main` changed, among them `AGENTS.md`, `capstone_v21.md`, `docs/PUBLISH_RULES.md` and `progress.md`.
5. **This review's own rebuild of `reports/ddnn2/base-tree.json`** from the Git objects at `522d7ea` (`git ls-tree -r` and `git cat-file`, SHA-256 per blob): 1,322 files, equal to the record.
6. **The full suite in CI's environment.** `$MON /usr/bin/env -u CP16_LEDGER … -u CP24_WORKERS $PY -m pytest -q -p no:cacheprovider` (`critic4-pytest`) **exited 1**: 3 failed and 12 errors. All 15 are in `tests/test_22_wasm_equivalence.py`, which reports "app/public/ is absent", because this review had not yet built the browser payload that CI's workflow builds before the suite.
   - `$MON $PY scripts/build_wasm_payload.py` (`critic4-payload`): exit 0. The worktree was still clean.
   - The suite again (`critic4-pytest-2`, with `-rfEs`): **exit 0, 1,443 passed, 8 skipped** (eccodes, CP-16's v21-r3 binding and production-ledger skips, and marimo).
7. **The simulated LAND.** `$MON $PY -m cp24.landsim --main 7ff6a50cb54ad34a7f0e52981e18f990fa0323bb --candidate 7949a98f… --out critic-4/landsim` (`critic4-landsim`): **exit 0, `green: true`.**
   - Preconditions: the candidate only adds under CP-24 paths (118), `main` touches no CP-24 path (31 changes since the base), and the base is an ancestor of `main`.
   - Steps: payload 0; suite 0 (1,479 passed, 13 skipped); CQR 0 (8 passed); `verify_release` 0 (PASS); WASM 0 (15 passed); publication guard 0. No tracked change followed any step.
8. **The same with `--later-edits`** (`critic4-landsim-edits`, `--out critic-4/landsim-edits`): **exit 1, `green: false`.** The suite had 3 failed, 1,475 passed and 14 skipped; the other five steps exited 0.
   - `tests/cp23/test_reference_record.py::test_the_reference_passed_for_the_current_ddnn_code_with_nothing_skipped` failed on the CP-23 lock's hash.
   - `tests/cp23/test_saved_evidence.py::test_byte_exact_storage_of_every_manifested_file` failed on `scripts/mlflow_export.py`.
   - `tests/cp24/test_reference_record.py::test_the_reference_passed_for_the_current_model_code_with_nothing_skipped` failed on the CP-23 lock's hash.
   - `tests/cp24/test_draft_export.py` skipped as designed ("scripts/mlflow_export.py changed after CP-24").

   No CP-24 test reacted to the edited living documents.
9. **The PyTorch reference.** `$MON $PY -m pytest -q -p no:cacheprovider -rA tests/cp24/torch_reference_checks.py` (`critic4-torch-reference`): **exit 0, 32 passed**, 0 skipped, with torch 2.14.1.
10. **Recomputation by this review's own code.** `$MON $PY -I critic-4/scripts/recompute.py <wt> critic-4/recompute.json` (`critic4-recompute`): exit 0. It reads only committed files and imports no CP-24 code. MAE is |p50 − y|, and WIS is 2 × the mean seven-level pinball, which is algebraically CP-15's WIS.
    - **Keys:** v5, v3+D2 and D2 each have 10,747 rows, with keys equal to CP-15's B0 keys and unique. The quantiles are finite and ordered, the maximum delivery date is 2026-04-07, and `y_true` equals B0's.
    - **Composites from the saved vectors themselves:** CP-23's `members.parquet` A1/B2, and CP-21's L-N/L-R and HGL. Max |v5 − ((2/3)c_HG + L/6 + D2/6)| = 2.3e-13; v3+D2 1.1e-13; c_v5 − c_v4 − (D2 − L)/6 2.1e-13.
    - **New-policy per-fold MAE, WIS, coverage95 and hours:** max deviation 7.1e-15.
    - **Reference rows:** 45 of them (B0–B3 and A1 against `reports/cp15/per_fold.csv`, HG, HGL, D and v3+D against their own checkpoints' `metrics.csv`), with maximum deviation 0. S deviation 5.6e-17.
    - **Intervals:** all 132 `uncertainty.csv` rows' 95% and 97.5% intervals equal the percentiles of `replicates.parquet` to within 3.6e-15. The equal-fold draws equal the `replicate-scores.parquet` differences and ratios exactly. All 22 `ratio-intervals.csv` rows equal their point, 95% and 97.5% values to within 4.4e-16.
    - **One flag, which was this review's false positive:** D2 − L in WIS is marked undefined although its draws are finite. That is by design: L is point-only (`scoring.py`'s `POINT_ONLY`).
    - **The rule applied from scratch:**
      - Condition 1: 97.5% intervals ΔS_MAE [−0.016594, −0.009140] and ΔS_WIS [−0.014687, −0.008384]. **Met.**
      - Condition 2: §8's criteria 1–6. **Met.**
      - Condition 4: all ten fold intervals' upper endpoints are below zero. **Met.**
      - Condition 5: ΔS_MAE −0.013337 against 0.005 × 0.535659 = 0.002678, and ΔS_WIS −0.011912 against 0.002528. **Met.**
      - Verdict: adopted, equal to `decisions.json`.
11. **Stored draws regenerated.** `$MON $PY -I critic-4/scripts/redraw_subset.py <wt> critic-4/redraw.json` (`critic4-redraw`): exit 0. It reproduces the CP-20 index generator (seed 15042, 13 blocks of 7 days in 84 starts, truncated to 90) with fingerprint `e1df9a68dc6715aa2ecd9705ef61f504a3fe109ed917d1151ccbc46ea9e0f99b`, equal to CP-20's. It then computes v5, HGL and B0 daily losses with its own code. The first **200** of the 2,000 replicates of the **one** contrast v5 − v4 match the stored draws in all five folds and equal-fold, MAE and WIS, with maximum deviation 6.4e-14. **This is a 10% subset for one contrast, not a bootstrap pass** under §23.11's definition. It reserved no counter, and it read the saved v4 and B0 vectors only to form daily losses.
12. **Representative review.** `$MON $PY -m cp24.review --out critic-4/review.json --gate 1 --trial 1:fold_4:79:7 --ensemble 1:fold_5:2026-03-29 --ensemble 1:fold_3:2022-08-22 --replay 1:v5:fold_2:2021-04-01:2021-04-14 --replay 1:v3+D2:fold_4:2025-05-01:2025-05-07` (`critic4-review`): **exit 0.** `--score` was deliberately not run: the reference passes are spent.
    - `gate`: `conditions_and_folds_equal: true`, passed in both the recomputed and committed versions. G1 v5 12.5378 ≤ v4 12.8494; G2 D2/L = 0.8525; G3 331 of 375,984 = 0.088%.
    - `trial`: pinball 4.41791693672346 equals the ledger, MAE 15.3453301868917 equals it, and both have 158 epochs. Batch 7 starts 2024-06-15 and its window excludes 174 uncovered days.
    - `ensemble` fold_5 2026-03-29: 23 hours; D2's central and quantiles are bitwise, and all 8 members' weight hashes are bitwise.
    - `ensemble` fold_3 2022-08-22: 24 hours, all bitwise.
    - `replay` v5 fold_2 2021-04-01..14: 335 rows, bitwise.
    - `replay` v3+D2 fold_4 2025-05-01..07: 168 rows, bitwise.
13. **This review's own leakage spot-check.** `$MON $PY critic-4/scripts/leak_spot.py fold_3 2022-08-25 critic-4/leak-spot.json` (`critic4-leak-spot`): exit 0, `pass: true`. It refitted the fold's frozen eight-member ensemble three times.
    - **(A) Random overwrite:** every price on or after D (31,728 rows), every load after D (31,704) and all three weather columns after D (27,452 hour rows) were replaced by random values, not NaN. Central and quantiles are bitwise equal to `predictions.parquet`, and all 8 parameter hashes equal `fits.parquet`.
    - **(B) Truncation:** every row after D was dropped and D's prices were randomised. Bitwise equal, with hashes equal.
    - **(C) Positive:** D−1's 24 prices +50 EUR/MWh. The quantiles move by up to 113.84 EUR/MWh.
14. **Pre-registration.**
    - `git merge-base --is-ancestor 62b8e51f… dea66640…` exits 0, and so does `… cb52fe26…`.
    - The first commits, by `git log --diff-filter=A`: `protocol.json` 62b8e51 (2026-10-05 11:39:57 +0300); `lineage.json` dea6664 (11:57:07); `predictions.parquet` and `members.parquet` cb52fe2 (16:06:13); `metrics.csv` f7eb23e (16:07:28).
    - The ledger's `attempt_1_first_fit` (08:40:05Z) records `protocol_commit 62b8e51f…` and `protocol_sha256 2fd3c464…`. That hash equals the protocol at both HEAD and 62b8e51. The event precedes the first `fits_start` (warm-up, 53 s later).
15. **Steering.** The S1 report was committed at 031f826 (11:28:37 +0300) and the answer at 118089a (11:32:30). `protocol.json` `freezing_steering_answer.sha256` is `64811aa4…`, equal to the committed answer file. The answer is "freeze", given after a passing gate, with no raise.
16. **The frozen code.** `check_protocol(root, 1)` refuses with `ValueError: implementation changed since attempt 1's freeze: scripts/cp24_ddnn2.py`. `cp24.leakage.frozen_guard(root, 1)` passes. It covers 50 implementation files and 25 frozen inputs, with exactly two maintenance exceptions (`scripts/cp24_ddnn2.py` and `src/cp24/budget.py`, each frozen at the protocol commit and equal to its blob at `9667fb4`). This review's own hash comparison of `protocol.json`'s `implementation_sha256` agrees: only those two files differ at HEAD, none differs at 62b8e51, and no frozen input differs.
17. **The continuation changed nothing scored.** `git diff --stat d637590 HEAD -- reports/ddnn2/attempt-1/ reports/ddnn2/rounds/ docs/track-b/evidence/cp-24/steering/` shows only three added files: `leakage-by-origin.csv`, `leakage-controls.json` and `ratio-intervals.csv`.
18. **The maintenance commit.** `git show 9667fb4` and `git diff 9667fb4^ 9667fb4 -- src/cp24/budget.py scripts/cp24_ddnn2.py src/cp24/finalise.py src/cp24/report.py reports/ddnn2/report.md`. It removes `calendar_stop`, the monitor's admission and in-run calendar checks, and the calendar sentence in the report. It adds the continuation brief, the maintenance record and `finalise`'s two manifested paths, plus a regression test. It touches no forecast, fitting or scoring path.
19. **§8 criteria for each new policy,** an unmonitored inline read-only script over the committed predictions and CP-15's `per_fold.csv` and `peak.csv`:
    - v5, v3+D2 and D2 each meet criteria 1–6, equal to `criteria.csv`;
    - fold coverage95: v5 0.933–0.949, v3+D2 0.935–0.948, D2 0.927–0.977;
    - peak coverage95: v5 0.944, v3+D2 0.946, D2 0.953;
    - mean width95 equals `metrics.csv` to within 1.4e-14.
20. **Ledger.** `PYTHONPATH=src $PY scripts/cp24_ddnn2.py status`, after this review's jobs:

    | Counter | Used | Cap |
    |---|---|---|
    | DDNN-2 fits | 16,436 (review 98, control 5,325) | 40,000 |
    | Policy-days | 4,558 (gate 2,520, review 35) | 12,000 |
    | Reference passes | 3 | 3 |
    | Bootstrap passes | 3 | 6 |
    | Rounds before attempt 1 | 1 | 3 |
    | Scored attempts | 1 | 2 |
    | v4 gate origins | 280 | 280 |
    | Machine-hours | 18.94 | 150 |
    | Active hours (upper bound) | 7.70 | 50 |
    | Peak RSS | 4.89e9 B | 10 GiB |
    | Peak added disk | 5.76e9 B | 10 GiB |

    No raise is recorded, and nothing is running. `resources.json` records data download 0, remote writes 0 and cost $0.
21. **Topology.**
    - `git worktree list`: the primary checkout (`main` 7ff6a50), `cp-24/critic-4` (detached 7949a98), `cp-24/lead` (`gauntlet/cp-24` 7949a98) and `final-product-price-lock-plan` (`codex/final-product-price-lock-plan` 7ff6a50). No critic-1, critic-2 or critic-3 worktree remains.
    - `git stash list`: empty.
    - `.local/artifacts/cp-24/critic-open.json`: n = 1 and n = 2 are closed at 2026-10-10T17:13:27Z with `verdict_sha256: null` and their dispositions. n = 3 is closed at 19:45:05Z with `verdict_sha256 eaf3ada6…`, equal to the committed `review/critic-3-integration-FAIL.md`. n = 4 (this review) is open.
22. **Bar check.** `git show main:scripts/bar.py | python3 -I - check /Users/djourno/Downloads/PJM/.local/artifacts/cp-24/critic-4/integration.md --source capstone_v21.md@7949a98f80c81c5a789dd69c213da16c811d345c`, run from the worktree: **exit 0**, `ok: lines 15–91 (4590 bytes) appear in capstone_v21.md@7949a98f80c8`.

**Unmonitored, read-only checks, disclosed.** They made no fit and charged nothing:

- commands 2–5 and 14–21 (Git and hashing; the `--check` generators, which the brief lists without the monitor);
- the inline §8 script (command 19);
- `check_protocol` and `frozen_guard` (command 16);
- one look at the weather design table's columns.

## Evidence actually inspected

- **Briefs and records:**
  - `docs/track-b/evidence/cp-24/issued-brief.md`, `continuation-brief.md` and `work-availability-2026-10-10.md`;
  - `review/critic-3-integration-FAIL.md` (its gap, next acceptance test and observations);
  - `steering/s1-round-1-report.md` and `s1-round-1-answer.md`;
  - `publication-packet.md` (headline quantities and §4);
  - `docs/track-b/research-content/cp24-claims.md` (C420–C432, C441, W47).
- **The anchor:** `capstone_v21.md` §23.1–§23.15, §8, §17.5, §21.5 and §22 item 4.
- **Code:**
  - `src/cp24/{basetree,landsim,leakage,review,reference,ratios (via its check),claims,packet,report}.py`;
  - `src/cp24/ddnn2.py`'s constants and head;
  - `src/cp22/scoring.py`'s bootstrap and `src/cp20/scoring.py`'s `_indices`;
  - `src/cp15/scoring.py`'s `score_hourly` and `src/cp15/data.py`'s `prepare`;
  - `scripts/cp24_ddnn2.py`'s header and monitor;
  - every file under `tests/cp24/`, audited for what it binds (condition 1);
  - `.github/workflows/tests.yml`.
- **Records under `reports/ddnn2/`:**
  - `report.md` (verdicts, rule, contrast table, diagnostics, leakage);
  - `reproduce.md` (this run, and "At the final candidate: what runs where");
  - `defects-and-repairs.md` items 10–15;
  - `base-tree.json`, `artifact-manifest.json` (116 entries, all under CP-24 paths), `draft-registry.json`, `mlflow-local.json`, `mlflow-export-draft/cp24.json` (SHA-256 `ead221fb…`, equal to `mlflow-local.json`'s record), `resources.json` (job exit codes), `resource-admission.json`, `licence-admission.md`, `v4-parity.json` and `preflight/input-verification.json`;
  - `rounds/round-1/{gate,ensembles,search-ledger}.json`.
- **Attempt 1:**
  - `protocol.json` (`implementation_sha256`, `frozen_inputs_sha256`, `freezing_steering_answer`);
  - `predictions.parquet`, `members.parquet`, `fits.parquet`, `lineage.json`, `metrics.csv`, `uncertainty.csv`, `criteria.csv`, `ratio-intervals.csv`, `replicates.parquet`, `replicate-scores.parquet` and `decisions.json`;
  - `controls.json` (all sections), `leakage-controls.json`, `daily-cycle.json` (25 origins), `diagnostics.json` and the 13 files in `diagnostics/`.
- **Saved references:** `reports/cp15/{predictions.parquet,per_fold.csv,peak.csv}`, `reports/block-challenger/{predictions.parquet,metrics.csv}`, `reports/distribution-challenger/{members.parquet,metrics.csv}` and `reports/weather-ablation/metrics.csv`.
- **Ignored state, read only:** `.local/artifacts/cp-24/ledger/budget.json` (events, effort, jobs), `start.json`, `critic-open.json`, the canonical briefs, and a size listing of `attempt-1/`.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1 | Starting state; prior evidence preserved; baseline recorded; worked only in `lead` on `gauntlet/cp-24`; issued brief packaged byte for byte | **Met** | The anchor's SHA-256 equals the brief's (command 2). `start.json`, 2026-10-05T03:16:55Z: `main` = `origin/main` = `522d7ea`, clean, no stash, one worktree. The first branch commit, `1cead62`, adds only `issued-brief.md`, byte-identical to the canonical copy (`a3f11470…`). The `lead` worktree is on `gauntlet/cp-24` (command 21). Every one of the 1,322 base files is unchanged, and this review's own rebuild equals the record (commands 4–5). |
| 2 | Inputs: population, manifest, frozen weather with §23.6's gap; saved-vector identities including CP-23's D; independent HG and v4 slice; no retrieval; nothing after 2026-04-07 | **Met** | `input-verification.json`: `retrieval: none`, every saved-vector consistency flag true, and gate, warm-up, evaluation and batch days covered. `v4-parity.json`: bitwise at 11 covered origins, and the unwrapped code refuses a fold-4 gate day. This review's own checks: `members.parquet`'s A1, B2, L-N and L-R equal the saved vectors, v4's central rebuilds within 2.3e-13, truth equals B0's, and the maximum delivery date is 2026-04-07 (command 10). |
| 3 | 4.6L′ | **Met** | `licence-admission.md`: PASS. The code is original, NumPy-only, with CP-23's reference reused, inside the 2-hour cap. |
| 4 | Correctness under §23.7: import audit, finite-difference checks, PyTorch reference that cannot be skipped silently | **Met** | `test_numpy_only.py`, `test_ddnn2_gradients.py` and `test_reference_record.py` pass in the suite (command 6). The reference rerun gives 32 passed and 0 skipped, with torch 2.14.1 from the pinned lock `b3164a37…` (command 9). The check file has no skip logic, so a missing torch fails collection. |
| 5 | 4.6R′ on pre-fold data, PASS or NOT_ADMITTED | **Met** | `resource-admission.json`: PASS, 128 trials per fold per round, the maximal route fits, and the review reserve is recorded. |
| 6 | Every pre-fold round, with no DDNN-2 or new-policy fit at a warm-up or evaluation origin: search ledger, gate with v4's members proven and the coverage rule, pre-fold report | **Met** | There is one round. `search-ledger.json` has 128 trials per fold. The gate recomputes equal (command 12), and a fold-4 trial reproduces the ledger exactly with the uncovered days excluded. `leakage-controls.json`'s exhaustive structure covers 3,464 batches and 280 gate days. `controls.json` `weather_coverage` holds. In the ledger, every `fits_start` follows `attempt_1_first_fit` (command 14). `rounds/round-1/report.md` is present. |
| 7 | Every S1 exchange committed; each attempt's frozen protocol before its warm-up or evaluation fits; stop where §23.6 says | **Met** | The S1 report, then the verbatim answer (freeze after a passing gate), then the protocol, then the first fit, in that order. The protocol binds the answer's hash (commands 14–15). No stop was required. |
| 8 | Exactly DDNN-2, v5 and the arms; composite parity | **Met** | `ddnn2.py`'s constants match §23.3: λ and δ floors 1e-3 and 0.05, 20 warm epochs, patience 50, a maximum of 1,000 epochs, cap 1.25, a 19-level grid containing the seven scored levels, and the per-level median of eight members. The composites from the saved vectors hold within 2.3e-13, and c_v5 − c_v4 = (D2 − L)/6 within 2.1e-13. v5 and v3+D2 run on HG's H-layer path, and the replays are bitwise (commands 10, 12). |
| 9 | Every §23.10 and inherited control, each negative paired with a positive | **Met** | `controls.json` passes 80 of 80. It covers masks, held-out weeks, recency, preprocessor statistics, exact inversion, weather, DST canonical hours, pre-registration, composites, determinism and restart replay, plus search and gate by fold. `leakage-controls.json` passes 12 of 12: 636 of 636 origins bitwise with the future destroyed, 10,747 keys equal, D−1 positives 22 of 22, and the planted leak caught in 5 of 5. This review's own random-overwrite and truncation refits are bitwise, with a paired positive (command 13). `test_design_dst.py` passes, and the 23-hour DST ensemble is bitwise. |
| 10 | All 10,747 keys per new policy, finite and ordered; the emitted p50 kept separate from the central | **Met** | Command 10. The p50 differs from the central for v5 and v3+D2. For D2 the p50 is the central by §23.3's design. |
| 11 | Score every policy; independently verify scores, diagnostics, coverage with width, all six §8 diagnostics per new policy | **Met** | This review's own code reproduces the per-fold metrics, S, coverage and widths, and every reference row against its own checkpoint (commands 10, 19). §8 is met by v5, v3+D2 and D2, equal to `criteria.csv`. The diagnostics are present and consistent (item 14). |
| 12 | `cp24-adoption` applied mechanically; first unmet condition; every §23.8 contrast with its reading; statuses distinct | **Met** | Applied from scratch, it gives adopted, with no unmet condition, equal to the committed verdict (command 10). All 11 contrasts appear in `report.md` with §17.5's 95% endpoint readings and their 97.5% intervals, and D2 − L in WIS is "not defined". The Engineering, Research and Product rows are separate. |
| 13 | Attempt bounds | **Met** | One scored attempt, adopted. There is no S2 and no attempt 2 (§23.6 "After an adoption"), and the ledger records 1 of 2 scored attempts. |
| 14 | §23.8's diagnostics in `reports/ddnn2/` | **Met** | `attempt-1/diagnostics/` holds 13 files: calibration by level, PIT, error correlations, MAE by local hour, extrapolation, peak and folds 3–4, guards by fold and by member, the search beside validation, gate and fold, member stability, the shape blend and epochs. Alongside them are `fit-cost.json` and `fit-cost-by-origin.csv`, and `daily-cycle.json` with 25 cold origins across the five folds. |
| 15 | DDNN-2 vectors stored for 4.8; every §23.11 cap enforced and reported, with any raise; calendar | **Met** (calendar clause superseded) | D2 is committed on all 10,747 evaluation keys (`predictions.parquet`, `members.parquet`), with all 5,088 member fits recorded (`fits.parquet`). See O2 for the warm-up and gate-day vectors. Every cap holds at the post-review ledger, with no raise (command 20). The calendar sentence is superseded by `AGENTS.md` § Work availability (`main` `7ff6a50`, the Owner, 2026-10-10), as the assignment directs, and is not reinstated. |
| 16 | Durable evidence: executable reproduction, byte-exact storage, §23.12's packet and draft export, unchanged public surfaces, export set, `mlflow_export.py` and root lock; CI green; no public write | **Met** (see O1) | The `reproduce.md` verification commands all run (command 4). The manifest's byte-exact test and `-text` attributes pass in the suite. The packet and draft registry are re-derived (item 17). The draft export is current, and MLflow uses `delu-generations`, local tracking, `network: none` and a read-back equal. Unchanged files are proved candidate-scoped (`--check-rev`). CI is green on the simulated LAND (command 7) and the full suite passes (command 6). The only remote-tracking ref is `origin/main` at the Owner's `7ff6a50`, and the ledger shows remote writes 0. The network was not queried, as the brief forbids. |
| 17 | One fresh, independent Integration-Critic PASS on a clean detached checkout; recompute metrics, intervals and verdict; gate and steering; pre-registration; reference rerun; a representative trial, ensemble fit and emission; packet re-derived | **Met — this verdict** | Metrics, intervals and verdict were recomputed without `--score`, so no reference pass was spent, and 200 stored replicates were regenerated (commands 10–11). Gate and steering: commands 12 and 15. Pre-registration: command 14. Reference: command 9. Trial, two ensembles with emission, and two replays: command 12. The packet: `draft-registry.json` is re-derived from §23.12 and `decisions.json` (outcome `adopted`, rounds [1], scored attempts [1], gate passed). Its name, predecessor and A3 title follow §23.9. Its derived quantities (−0.0133 and −0.0119; 97.5% uppers −0.0091 and −0.0084; −2.5% and −2.4%, with 97.5% [−3.0%, −1.7%] and [−2.9%, −1.6%]) equal this review's values. |
| 18 | The canonical packet (templates §3), checked with `scripts/gauntlet.py return` | **Not yet due** | The Lead's act after this verdict. See "For the Lead's return". |

### The continuation brief's three conditions

| Condition | Verdict | Evidence |
|---|---|---|
| 1. CI stays green on `main` after the LAND; item 16's "unchanged" proof holds; no CP-24 test binds files later authorized work may change | **Met** (see O1) | The simulated squash onto `7ff6a50` runs all six CI steps green (command 7). `--check-rev` proves the candidate changed no base file. The repaired `test_base_tree.py` hashes no base file: it checks the record and both checkers on fixtures, with paired negatives. **Audit of every CP-24 test:** each binds only CP-24's own files or fixtures, except the two cases below. With `--later-edits`, no CP-24 test fails on a living document (command 8). The two exceptions: (a) `test_draft_export.py` binds `scripts/mlflow_export.py` and skips when it changes. (b) `test_reference_record.py` asserts the hash of CP-23's lock. That test is itself in attempt 1's frozen `implementation_sha256` (verified, command 16), so editing it would change a frozen element, which §23.6 forbids after an adoption. The lock is also bound by CP-23's own reference and byte-exact tests on `main`, which fail identically in the edited run. So a lock change already turns `main` red without CP-24, and CP-24 adds no new exposure. `defects-and-repairs.md` item 12 discloses this. I judge the handling sound. |
| 2. Item 9's control evidence matches the strength of the result; any extension verification only | **Met** | **Decision:** the committed `controls.json` alone (two origins) did not match a −10.67%/−15.53% member, and the extension was warranted. With `leakage-controls.json` (every one of the 636 origins, every member, every fold) and this review's harsher spot-check at a fresh origin, the evidence rules out the use of any outcome dated on or after the delivery day. The input vintages (A65 load forecasts, CP-20's GFS rule) are inherited and correctly scoped out in C441. **Verification only:** the extension changed nothing scored (command 17), `frozen_guard` passes, and the 5,325 control fits are inside §23.11 (16,436 of 40,000 fits in total). |
| 3. Every interruption accounted for | **Met** | `critic-open.json` n = 1 and n = 2 are closed with no-verdict dispositions, and their worktrees are gone (command 21). The third idle gap (2026-10-05 14:28Z → 2026-10-10 16:54Z) is in the effort ledger with the earlier two. This review received nothing from Critics 1–3 beyond the committed critic-3 verdict that the assignment names. |

### The repair after the third review's FAIL

**Met.** Each part of that verdict's "Exact next acceptance test" holds:

1. **The intervals are reported.** `ratio-intervals.csv` has 22 rows, each with the 95% and the 97.5% ratio interval, from the stored equal-fold `ratio` draws. All equal this review's percentiles to within 4.4e-16. For v5 − v4: MAE [−3.04%, −1.68%] and WIS [−2.86%, −1.62%], the values critic-3 expected. They appear in `report.md`'s contrast table, in the packet's §4 rows "(b)" and "Its 97.5% interval" and in claim C420. D2 − L in WIS stays undefined.
2. **They come only from the stored draws.** `git diff --stat 7ea9bdd… 7949a98…` shows 13 files. Under `attempt-1/` the only change is the added `ratio-intervals.csv`, so `protocol.json`, `predictions.parquet`, `members.parquet`, `fits.parquet`, `lineage.json`, `metrics.csv`, `uncertainty.csv`, `criteria.csv`, `decisions.json` and `replicates.parquet` are unchanged. `frozen_guard` passes. The ledger still shows 3 reference passes and 3 bootstrap passes.
3. **Every check passes:** packet, claims and report `--check`, `--check-rev` at the candidate, the default suite and `landsim` against `main` (commands 4, 6, 7). `test_ratio_intervals.py` passes in the suite.
4. **`reproduce.md`'s section "At the final candidate: what runs where"** states that the attempt-1 entry points refuse after `9667fb4`. It points to `d637590` for the original route, and names `cp24.review` (warning that `--score` spends a reference pass) and `cp24.leakage` as the path at the candidate. `defects-and-repairs.md` item 15 records the FAIL and the repair.

### Work availability, the maintenance commit and `check_protocol`

**The calendar.** The calendar sentence in item 15 and §23.11's calendar paragraph are treated as superseded by `AGENTS.md` § Work availability, on `main` at `7ff6a50` (the Owner, 2026-10-10). They are not reinstated.

**The maintenance commit.** The Owner's `9667fb4` was reviewed as part of the candidate. It removes only the calendar gate and its wording (command 18).

**The refusal is sound.** `check_protocol` fails closed on the two changed frozen files, as §23.6 intends, and no attempt-1 entry point runs at the candidate.

**So is the continuation's handling.** `frozen_guard` whitelists exactly those two paths. For each, it requires both the frozen blob at the protocol commit and the recorded maintenance blob, and it leaves every other implementation file and frozen input bound. The bit-for-bit refits confirm that the forecast path is the frozen one: 636 origins in the leakage job, plus this review's two ensembles, two replays and spot-check.

## Observations (not blocking on their own)

1. **O1 — `defects-and-repairs.md` item 11 overstates the edited LAND.** It says the simulation "is green on `main` as it stands, and again after simulated later edits to the living files". The second half is false. The `--later-edits` run is red: 3 failed, 1,475 passed, 14 skipped (command 8). The candidate's own `resources.json` records `landsim-main-edits` with exit code 1, so the document contradicts itself.
   - **Where the failures come from:** all three come from the two edited files that CP-23's evidence binds, `tests/cp23/torch-reference/uv.lock` and `scripts/mlflow_export.py`. None comes from a living document.
   - **What the return must do:** state the edited run's result exactly and correct this sentence in the landing record.
   - **Why it does not block:** item 12 of the same file discloses the binding correctly, and the plain LAND is green.
2. **O2 — The warm-up and gate-day D2 vectors are not committed.** The committed D2 vectors cover the 10,747 evaluation keys. The 188 warm-up origins' and the 280 gate days' D2 vectors exist only in the retained ignored caches (`.local/artifacts/cp-24/attempt-1/fits/`, about 58 MB, and the round caches). `lineage.json` binds the warm-up centrals by hash, and the leakage job reproduced all 188 warm-up origins bit for bit, so they are recoverable. 4.8 is walk-forward on released errors, so the return should say where these vectors live. They should be preserved, or committed by a later authorized step, before any reclamation of `.local/artifacts/cp-24/`.
3. **O3 — The gate sub-counter.** This review's `--gate` recomputation charged 840 more policy-days to `policy_days_gate`, which now reads 2,520: the Lead's gate plus two review recomputations. That is 4,558 of 12,000 in total. v4's gate origins stay at 280, because no v4 member was refitted.
4. **O4 — The reference passes stay at their cap.** They remain 3 of 3, and this review spent none: it ran no `--score`.
5. **O5 — The suite needs the browser payload first.** Run without the payload, the plain suite fails only `tests/test_22_wasm_equivalence.py` (command 6). CI builds the payload first, and `landsim` mirrors that. This is not a candidate defect.

## For the Lead's return (item 18)

The return must carry:

- **Both terminal SHAs and the verdict-only delta.**
- **This review's charges:**
  - 41 review fits: 1 trial, 2 × 8 ensemble members and 3 × 8 spot-check members;
  - 21 review policy-days, plus 840 charged to `policy_days_gate`;
  - 0 reference passes and 0 bootstrap passes;
  - about 0.39 charged machine-hours over the ten `critic4-*` jobs.

  Peak added disk is now 5.76e9 B (5.36 GiB), from this review's two landsim trees. Peak aggregate RSS is unchanged at 4.89e9 B.
- **The final cumulative totals** from the ledger after this review (command 20).
- **O1's correction and O2's statement.**
- **Branch, worktree and stash accounting:**
  - `gauntlet/cp-24` and its `lead` worktree;
  - the `critic-4` worktree, which `critic-close` removes;
  - no stash;
  - another session's branch `codex/final-product-price-lock-plan` at `7ff6a50`, with its worktree `.local/worktrees/final-product-price-lock-plan`. It is not CP-24's, and should be declared as such or escalated.
- **Disposable scratch:** this review's trees `.local/artifacts/cp-24/critic-4/landsim/tree` and `landsim-edits/tree`, about 1.3 GB each.
