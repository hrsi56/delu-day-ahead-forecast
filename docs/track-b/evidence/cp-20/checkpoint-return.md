# Track B Checkpoint Return — CP-20

## Status
PASS

## Identity
- Repository / checkpoint / ratified anchor and version: local `/Users/djourno/Downloads/PJM`; CP-20 (direct-GFS paired research ablation, HG − H0); `capstone_v21.md` v21-r4 (ratified), §15 with §14 inheritance, SHA256 150bd53fa15067b1d138c95d0912f86a1e92ce74092059be09034758c1926167; amendments `docs/track-b/capstone_v21-r3-to-v21-r4-amendments.md` SHA256 3e0bdf6a343d5336f406f0eeb726b1b65c0f767ec8d9418a7d8118902e1ace55; brief `docs/track-b/cp-20-direct-weather-brief.md` SHA256 28a4e195fa7f66ff3270d5d54e477478e90aa42124bceb1ee529f95f5761883e (all three verified at the candidate).
- final_candidate_sha: **3e9ff8b500c2c655fea810ae11886503927f176c** (every bar binds here).
- evidence_tip_sha: **SELF_COMMIT**. Resolve as the commit containing this return: `git log -1 --format=%H -- docs/track-b/evidence/cp-20/checkpoint-return.md`. The canonical packet gives the resolved SHA; a file cannot contain its own commit SHA.
- `git diff --name-only 3e9ff8b500c2c655fea810ae11886503927f176c..<evidence_tip_sha>` (57 paths, all under `docs/track-b/evidence/cp-20/`):
  docs/track-b/evidence/cp-20/checkpoint-return.md
  docs/track-b/evidence/cp-20/integration-2/eligible-decodes.txt
  docs/track-b/evidence/cp-20/integration-2/logs/critic2-attempts.log
  docs/track-b/evidence/cp-20/integration-2/logs/critic2-components.log
  docs/track-b/evidence/cp-20/integration-2/logs/critic2-convert.log
  docs/track-b/evidence/cp-20/integration-2/logs/critic2-decode.log
  docs/track-b/evidence/cp-20/integration-2/logs/critic2-guards.log
  docs/track-b/evidence/cp-20/integration-2/logs/critic2-replay.log
  docs/track-b/evidence/cp-20/integration-2/logs/critic2-scoring.log
  docs/track-b/evidence/cp-20/integration-2/logs/critic2-static.log
  docs/track-b/evidence/cp-20/integration-2/logs/critic2-tests-wx.log
  docs/track-b/evidence/cp-20/integration-2/logs/critic2-tests.log
  docs/track-b/evidence/cp-20/integration-2/out/attempts.json
  docs/track-b/evidence/cp-20/integration-2/out/components.json
  docs/track-b/evidence/cp-20/integration-2/out/convert.json
  docs/track-b/evidence/cp-20/integration-2/out/decode-journal.jsonl
  docs/track-b/evidence/cp-20/integration-2/out/decode-summary.json
  docs/track-b/evidence/cp-20/integration-2/out/decoded-local-sha256.txt
  docs/track-b/evidence/cp-20/integration-2/out/decoded-meta.json
  docs/track-b/evidence/cp-20/integration-2/out/replay.json
  docs/track-b/evidence/cp-20/integration-2/out/scoring-pass-reserved.json
  docs/track-b/evidence/cp-20/integration-2/out/scoring.json
  docs/track-b/evidence/cp-20/integration-2/out/static.json
  docs/track-b/evidence/cp-20/integration-2/scripts/critic2_attempts.py
  docs/track-b/evidence/cp-20/integration-2/scripts/critic2_components.py
  docs/track-b/evidence/cp-20/integration-2/scripts/critic2_convert.py
  docs/track-b/evidence/cp-20/integration-2/scripts/critic2_decode.py
  docs/track-b/evidence/cp-20/integration-2/scripts/critic2_replay.py
  docs/track-b/evidence/cp-20/integration-2/scripts/critic2_scoring.py
  docs/track-b/evidence/cp-20/integration-2/scripts/critic2_static.py
  docs/track-b/evidence/cp-20/integration-assignment.md
  docs/track-b/evidence/cp-20/integration.md
  docs/track-b/evidence/cp-20/lead-scripts/build-wx-venv.sh
  docs/track-b/evidence/cp-20/lead-scripts/build_manifest.py
  docs/track-b/evidence/cp-20/lead-scripts/diag_concurrent.py
  docs/track-b/evidence/cp-20/lead-scripts/diag_probe.py
  docs/track-b/evidence/cp-20/lead-scripts/extraction_protocol.py
  docs/track-b/evidence/cp-20/lead-scripts/h0_dryrun.py
  docs/track-b/evidence/cp-20/lead-scripts/precheck-tests.log
  docs/track-b/evidence/cp-20/lead-scripts/precheck.log
  docs/track-b/evidence/cp-20/lead-scripts/precheck.py
  docs/track-b/evidence/cp-20/lead-scripts/restart_trigger.py
  docs/track-b/evidence/cp-20/lead-scripts/subset_sanity.py
  docs/track-b/evidence/cp-20/markers/critic2-attempts.DONE.json
  docs/track-b/evidence/cp-20/markers/critic2-attempts.FAILED.superseded-90.json
  docs/track-b/evidence/cp-20/markers/critic2-components.DONE.json
  docs/track-b/evidence/cp-20/markers/critic2-convert.DONE.json
  docs/track-b/evidence/cp-20/markers/critic2-decode.DONE.json
  docs/track-b/evidence/cp-20/markers/critic2-guards.DONE.json
  docs/track-b/evidence/cp-20/markers/critic2-replay.DONE.json
  docs/track-b/evidence/cp-20/markers/critic2-scoring.DONE.json
  docs/track-b/evidence/cp-20/markers/critic2-static.DONE.json
  docs/track-b/evidence/cp-20/markers/critic2-tests-wx.DONE.json
  docs/track-b/evidence/cp-20/markers/critic2-tests.DONE.json
  docs/track-b/evidence/cp-20/markers/precheck-tests.DONE.json
  docs/track-b/evidence/cp-20/markers/precheck.DONE.json
  docs/track-b/evidence/cp-20/resource-final.json

## Repository state
- Branch: `gauntlet/cp-20` (local only). Working tree: clean after the terminal evidence commit.
- Branches, worktrees or tags this checkpoint created:
  - `gauntlet/cp-20`: candidate and evidence branch from `main` 88c68cf. It holds the reviewed chain: the failed candidate a7943fb, the passed candidate 3e9ff8b and the evidence tip. Local, never pushed.
  - Worktrees `.local/worktrees/cp-20/critic` (a7943fb, Integration attempt 1), `.local/worktrees/cp-20/precheck` (3e9ff8b, the Lead's clean-checkout check) and `.local/worktrees/cp-20/critic-2` (3e9ff8b, Integration attempt 2): created, confirmed clean and removed by this checkpoint; `git worktree prune` run.
  - Created by the desktop app at session start, not by a checkpoint command:
    - Branch `claude/cp-20-weather-augmentation-7c081b` at 88c68cf: never used, no commits. Left in place for the Owner.
    - Worktree `.claude/worktrees/cp-20-weather-augmentation-7c081b`: the session worktree, switched to `gauntlet/cp-20`. It hosts the branch.
  - Tags: none.
- Other-session work present and untouched: branch `claude/word-rtl-issues-3286df` and worktree `.claude/worktrees/word-rtl-issues-3286df` (detached at 88c68cf); `stash@{0}` (`claude/modest-bardeen-96zee0`).
- `main` untouched at 88c68cf (= `origin/main`), nothing staged on `main`, nothing pushed: confirmed.

## Complete checklist with direct evidence (capstone_v21.md v21-r4 §15.6)
| # | Checklist item | Status | Direct evidence (path, command, or metric) |
|---|---|---|---|
| 1 | Repository/input state; prior evidence and other-session work retained; exact anchor/amendment/brief packaging; frozen manifests committed before comparison | PASS | Base `main` 88c68cf already carries the three controlling documents and `reports/weather-admission/`; their hashes were verified at the candidate and none was revised. `run-manifest.json` and `extraction-protocol.json` were frozen (86d8e1f) before any target request. The pre-fit `protocol.json` (E1–E4; implementation, input, conversion, missingness and budget hashes) was frozen (255ecfb) before any HG fit. The training-only admission `lineage.json` was frozen (30a958a) before the comparison (2dac186). In a clean checkout, `check_protocol` passes and all 84 protocol and 41 manifest hashes match the committed bytes (`integration.md`; `lead-scripts/precheck.log`). CP-15/16 files are identical to `main`. |
| 2 | Eight-run admission extension; field/lead/version metadata, source/endpoint identity and availability basis validated; inferred vs decoded, 2019 structural missingness and dossier exceptions preserved; every extraction gap recorded | PASS | `extended-inventory.csv`: 8/8 runs (2023-03-24..31) pass. `messages.parquet` and `runs.csv`: 2,476/2,476 runs and 123,800 target messages decoded and validated (AWS 87,200; NCAR 36,600), with 0 nonfinite values. `missingness.csv`: only the structural 2019-01-01 day (24 h); no run classified missing and nothing imputed. `sample-hash-comparison.csv`: 600/600 identical. `failures.jsonl`: 482 failure records, every affected run later completed. The dossier exceptions (AWS lacks 2021-02-02; NCAR 2024-09-15 f039 truncated) and the inferred-presence and reconstructed-availability disclosures are in `protocol.json` and `report.md`. |
| 3 | Exactly H0/HG and the frozen conversion/fallback; only the weather treatment differs; H0 vs accepted CP-16; representative weather-component fits; training-only admission before outer scoring; no tuning | PASS | `src/cp20/components.py` appends only the three frozen columns to the unchanged CP-15 A1/B2 recipe. H0 is bitwise equal to the CP-16 V2-H vectors (10,747 rows; `lineage.json` `h0_verification`, `h0-dryrun.json`), and its 35 admission vectors match the CP-16 V2-H hashes. HG refits are bitwise equal to the cache: 2 in the controls, 8 in Integration 1 and 6 in Integration 2. Neutralised weather reproduces H0 to ≤1.4e-14. The admission freeze commit precedes the comparison, and no parameter was changed after results. |
| 4 | §14.8 item 3 causal/state/DST/cache controls; positive/negative weather-origin, accumulation, units, packing/clipping, aggregation and missingness controls; pre-2019 refusal; independent reconstruction from retained raw samples | PASS | `causal-controls.json`: delivery-day/future mask 0.0; future-weather mutation 0.0; D−1 price mutation moves the forecast. `causal-controls-supplement.json` (r13): target-day D−1 weather shift and training-weather permutation both move it >1e-6. The frozen ×3 control is scale-invariant under standardisation and is disclosed. DST: 59,446 hours match the Berlin calendar (8 spring-forward and 6 fall-back days; repeated hours averaged). `radiation-clipping.csv`: clipping ≥−3q; no invalid support. `tests/cp20` (86 passed + 1 skipped) and extraction-environment tests (75 passed). Integration 2 decoded 1,035 retained raw messages (boxes bitwise equal; 495 hours reconstructed exactly) and checked the pre-2019 refusal and the state replay (all 70 admission vectors, 896 buffer records, 10 final states). |
| 5 | All original eligible keys for both arms and reference metrics; no denominator change; p50/ordered vectors, §14.3 diagnostics, support counts and fallback independently verified | PASS | `predictions.parquet`: 21,494 contrast rows; 75,229 scored rows; fold counts 2,160/2,159/2,112/2,160/2,156; fold 3 has 88 dates; the peak has 408 hours on 17 dates. `diagnostics.csv` and `metrics.csv` (all §14.3 slices and support counts); `fallback.csv`: 0 fallback cells for both arms. Integration 2 re-scored every row: metrics, diagnostics and criteria match to ≤5.7e-14. The CP-15 product status stays NOT_DEMONSTRATED. |
| 6 | HG − H0 paired endpoint rule and all six original §8 diagnostics; effects, uncertainty, mixed findings, post-selection labels and research/product distinctions kept; no promotion, economic threshold or availability claim | PASS | `uncertainty.csv`: ΔS_WIS −0.0838 [−0.1044, −0.0655] and ΔS_MAE −0.0783 [−0.1006, −0.0570], so the result is an observed joint improvement (seed 15042, 2,000 replicates, 7-day blocks, one index set; independently reproduced in both Integration reviews, ≤5.7e-14 in Integration 2). Mixed finding: the fold-3 per-fold MAE interval crosses 0 (upper +0.037). `criteria.csv`: HG met all six §8 criteria; H0 not met on 1 and 2 (diagnostics only). `report.md`: `development_post_selection`, no promotion, no new economics, no availability guarantee. |
| 7 | Every §15.5 cap enforced and reported from the first job, all attempts and the independent review; historical debits and monitoring limitations preserved | PASS | `resource-final.json` (the ledger was never reset). CP-20 increments against caps: machine 40.09 h / 120; transfer 136.0 GiB / 160; policy-days 4,525 / 9,000; component-day attempts 1,384 / 4,000 (main 1,272 / 3,000); primitive fits 165,870 / 480,000 (inner 132,696 / 384,000, final 33,174 / 96,000); analysis passes 3 / 3 and reference passes 3 / 3, now exhausted; message attempts 8,870 / 371,400; peak RSS 3.72 GiB / 10; peak added disk 2.35 GiB / 40; 4 workers; BLAS 1; 0 GPU/cloud; $0. Active hours ≤4.92 of the 64 h timebox and 80 h hard stop. CP-16 prior totals are reported separately and unchanged: 6,458 policy-days; 121 component attempts (93 main); 14,484 primitive fits; 0.55 machine-hours; 2 analysis passes; 2 reference passes. Disclosed limitations: 1,885 pre-O2 message charges retained; job-3 validation failures (r1 validator defect) counted conservatively; a few development test runs outside the monitor, each charged 60 s; the job-33 code version was reconstructed (the pre-r10 extractor did not self-record); 25 target messages reach 4 tries if network failures without a response are counted (excluded under Owner decision O2). |
| 8 | Protocol, lineage, decoded weather/features, predictions, metrics/diagnostics, uncertainty, criteria, failure/resource logs, rights notices and executable reproduction commands; invalid outputs and repairs preserved; inherited regression guards run | PASS | `reports/weather-ablation/`: protocol, lineage, weather-features, messages, predictions, metrics, diagnostics, uncertainty, criteria, fallback, failures, resources, report and artifact-manifest. `rights-notice.md` covers NOAA/NCEP, the NCAR DOI and the NODD terms. `reproduce.md` runs from a clean checkout (`check_protocol` passes). Repairs are preserved: r1–r12 (`extraction-repairs.json`, `defects/`), r13–r14 (`post-freeze-repairs.json`) and Integration attempt 1 (`integration-attempt-1/`). The listed inherited guards pass (70). The full `tests/cp16` directory has 3 failures and 3 errors that occur identically on `main` 88c68cf (CP16_LEDGER unset; v21-r3 anchor identity); they are not CP-20 regressions. |
| 9 | One fresh independent Integration-Critic PASS on the exact final candidate in a clean detached checkout covering the entire checklist, with independent metrics/uncertainty and conversion/component/causal/state reproduction | PASS | `docs/track-b/evidence/cp-20/integration.md` (SHA256 395d4f01391cb9b39d03873f5606d4098ea9fa06b0165cd2c5a837ece030d2a3): PASS at 3e9ff8b500c2c655fea810ae11886503927f176c. The worktree was clean before and after; assignment `integration-assignment.md` (SHA256 615f5b2a…); scripts, logs and outputs in `integration-2/`. The earlier FAIL at a7943fb is preserved in `integration-attempt-1/`. |
| 10 | Canonical packet, final candidate and evidence-tip SHAs, evidence-only terminal delta, reachable history, all resources and branch/worktree accounting; stop at CP-20's local result | PASS | This return. The delta between the two SHAs touches only `docs/track-b/evidence/cp-20/` (57 paths above). a7943fb, 3e9ff8b and the evidence tip are reachable on `gauntlet/cp-20`. Resources: `resource-final.json`. Branch and worktree accounting: above. No mainline action, publication, VRE experiment, later checkpoint or self-ratification. |

## Integration verdict
- Path: `docs/track-b/evidence/cp-20/integration.md`   Result: **PASS**
- Candidate SHA it binds: 3e9ff8b500c2c655fea810ae11886503927f176c
- Preceding review: `docs/track-b/evidence/cp-20/integration-attempt-1/integration.md`, FAIL at a7943fb6262c1a50b729bd92fe701c8be9428038. Two findings: a line-ending hash mismatch for `prerun-attempts.csv`, and the finaliser outside the §15.7 paths. Both were repaired as r14 and the finaliser move, and no result changed.

## Reproduction
Commands: `reports/weather-ablation/reproduce.md`, run through `scripts/cp20_weather.py --monitor` against the shared ledger. Results observed:
- Extraction chain: 2,476/2,476 runs; r10 locator-fix verification passed on 5 previously failing days before the NCAR re-run.
- Assembly: 123,800 messages; 59,446 feature hours; weather design SHA256 f5a9c6ed7dae18e711017e9f2887e3c72f64c286137bd7cabfb3469cd10274c0.
- Research jobs:
  - HG warm-up: 188 components.
  - Admission: 35 dates × 2 arms.
  - HG evaluation: 450 components.
  - Comparison: 5 folds × 90 dates.
  - Controls and r13 supplement: all pass.
  - Score: HG−H0 observed joint improvement; H0 bitwise equal to CP-16 V2-H.
- Tests: `tests/cp20` 86 passed + 1 skipped; extraction environment 75 passed; inherited guards 70 passed. In the Lead's clean checkout of 3e9ff8b, `check_protocol` and every recorded hash passed and `tests/cp20` passed (`lead-scripts/precheck*.log`); Integration 2 reran all three suites with the same results.

## Files changed
`git diff --stat 88c68cf 3e9ff8b`: 229 files, +406,449 lines, all within the §15.7 paths.
- `src/cp20/` (20 files): extraction (budget, net, gfs, extract, chain, plan, probe, feasibility), conversion (weather, assemble), modelling (inputs, components, execution, scoring, controls, controls_supplement), protocol, report and finalise.
- `tests/cp20/` (8 files): locator, ecCodes, conversion, arms/scoring, attempts, retry routing, fetcher watchdog and concurrent leads.
- `scripts/cp20_weather.py`: the driver and resource monitor.
- `reports/weather-ablation/` (42 files): frozen manifests and protocol, extraction evidence, features, predictions, metrics, uncertainty, criteria, controls, report, resources, rights notice, repair records and reproduction commands. Large tables are committed as parquet: `messages.parquet` 14.5 MB, `weather-features.parquet` 2.0 MB.
- `docs/track-b/evidence/cp-20/` (158 files at the candidate, +57 in the evidence delta): job logs, markers, ledger snapshots, chain status, code versions, both Integration reviews, the Lead's scripts, the final resources and this return.

## Elapsed
- Wall clock: about 15 h (2026-09-23 15:50Z to 2026-09-24 ~07:05Z), much of it unattended extraction.
- Active effort by the ledger: ≈4.5 h, and ≤4.92 h with the closing allowance, against the 64 h approximate timebox and 80 h hard stop. This counts the usage-limit idle gap and Owner decision O3 unattended waits as paused, and the waits on the Integration reviews as active.

## Open risk or exact owner action
1. **Disposition:** LAND or DISCARD `gauntlet/cp-20` (Owner only).
2. **Owner decisions from pasted blocks:** O1, O2, O2 amendment A1, S1, O3 and O4 are recorded in `reports/weather-ablation/extraction-repairs.json`. Apart from O2, which the Owner confirmed in chat, they reached this session as pasted text, and neither Critic could verify them independently. The per-message attempt cap relies on O2's counting rule: counting network failures without a response, 25 target messages reach 4 tries. Owner confirmation of these records is the smallest open action.
3. **Weather attribution in `DATA-LICENSE.md`:** an Owner decision per the admission record; not edited. `reports/weather-ablation/rights-notice.md` covers the committed weather-derived artifacts in the meantime.
4. **Scoring passes exhausted:** analysis and reference passes are both 3/3, so any further scoring needs an Owner cap decision.
5. **Unused app-created branch:** `claude/cp-20-weather-augmentation-7c081b` (at 88c68cf) can be deleted at the Owner's discretion.

## Landing report
- Proposed disposition: **LAND**. It is a PASS research result labelled `development_post_selection`, with no product, public-surface or CP-15/16 change, and it preserves the complete reviewed evidence. As with land/cp-15 and land/cp-16, tag both `land/cp-20` and `evidence/cp-20`.
- Evidence tip to preserve: **SELF_COMMIT** (resolved in the packet). The reviewed chain includes a7943fb (FAIL) and 3e9ff8b (PASS).
- Live documents citing this branch, to repoint on reclamation: `capstone_v21.md`, `docs/track-b/capstone_v21-r3-to-v21-r4-amendments.md` and `docs/track-b/cp-20-direct-weather-brief.md` (all name `gauntlet/cp-20` as the authorized branch); `docs/track-b/evidence/cp-20/integration.md`.
- Proposed commit message: `cp-20: direct-GFS paired ablation HG−H0 (development_post_selection research evidence; observed joint improvement; no promotion)`

## Post-return reads
none
