# Verdict — CP-21 — Integration — PASS

- **Candidate SHA:** `260dcf9fb3f5706cb896991ba7b6edf4cd9494b6` (local branch `gauntlet/cp-21`; pre-run base `ffcf9f3d10ad21db5db65f42e0c40653dbc05904` = `main` = `origin/main`)
- **Plan / version / bar:** `capstone_v21.md`, revision **v21-r6** (ratified 2026-09-29), SHA-256 `ee402c4703d176f8181ed82966c978ad84c3c73a0cdb1d3567871f58bc867344` (verified at the candidate and at the ratification commit `270a0a0`); bar **§17.10 "Complete CP-21 acceptance checklist", all thirteen items**, governed by §17.1–§17.9 and §17.11 with the inheritances §17.1 names.
- **Reviewer:** a fresh, independent Integration Critic session (the second for this candidate). The first, interrupted session's scratch (`.local/artifacts/cp-21/critic/`) was not opened or relied on. Isolation is cooperative (a clean detached `git worktree`; no read-only mount).
- **Worktree clean before and after: yes.** `/Users/djourno/Downloads/PJM/.local/worktrees/cp-21/critic-2`: `git status --porcelain` empty and `git rev-parse HEAD` = `260dcf9fb3f5706cb896991ba7b6edf4cd9494b6` at the start, after every write-capable step (payload build, suite, checks) and immediately before writing this verdict. Only ignored byproducts appeared (`app/public/`, `__pycache__/`, `.DS_Store`).
- **Verbatim bar excerpt** (extracted with `awk '/^### 17.10 /{f=1} /^### 17.11 /{f=0} f' capstone_v21.md` and compared byte for byte with the brief's excerpt: identical, 4,472 bytes, SHA-256 `3b78d0f86248308f4010b9794174e8d553b13bb3342570b47b8828a670ea9c04`; the extraction carries only the one blank separator line before `### 17.11` in addition). The excerpt is the citation; line numbers (1554–1623) are a courtesy.

> ### 17.10 Complete CP-21 acceptance checklist
>
> All thirteen items are mandatory. Engineering PASS does not require adoption: a complete,
> valid "Not adopted" result can pass.
>
> 1. Verify the repository and input state, and preserve prior evidence and other sessions'
>    work.
>    - The ratified anchor and the amendment record are on `main` at the ratification commit;
>      verify their SHA-256 against the brief.
>    - On `gauntlet/cp-21`, package the issued brief byte for byte as
>      `docs/track-b/evidence/cp-21/issued-brief.md`, from its canonical copy
>      `.local/artifacts/cp-21/issued-brief.md`, and record its SHA-256.
>    - Before any outer scoring, commit the frozen pre-run protocol:
>      - the arms, blend weights, block map, feature list and missing rule;
>      - the capacity grid, inner split and tie rule;
>      - fixtures, seeds, the key/origin manifest and cache identities;
>      - budget accounting and the §17.6 rule text.
> 2. Verify the CP-20 population and manifest identities, and the frozen weather features from
>    the retained grids. Reuse HG components only with verified identity, and obtain an
>    independent representative HG reproduction that matches the accepted CP-20 vectors. No
>    retrieval, and no data after 2026-04-07.
> 3. Implement exactly L-P, L-R, L-N and HGL, with training-only capacity selection for every
>    LightGBM model. Prove three things:
>    - HGL differs from HG only by the added member and uses HG's H recipe on its own errors;
>    - L-R and L-N differ only in target representation;
>    - L-P and L-R differ only in pooled versus per-block fitting.
> 4. Prove every §17.7 control, pairing each negative assertion with a positive control that
>    survives the model's transforms. Rerun the applicable inherited regression and namespace
>    guards without a live mutation.
> 5. Produce all 10,747 keys for each new arm, with finite, ordered quantiles and the emitted p50
>    kept separate from the central forecast. Account for failures, exclusions and fallback
>    incidence without changing denominators.
> 6. Score all eleven policies. Independently verify:
>    - the emitted-vector scores and the equal-fold normalization;
>    - every per-fold, hour, block, stress and peak diagnostic, with its denominators and support
>      labels;
>    - coverage together with width;
>    - all six §8 diagnostics for each new arm.
> 7. Apply §17.6's four conditions mechanically.
>    - Report the primary and secondary contrasts with paired intervals, per-fold intervals, and
>      the ratio intervals from the checkpoint's own stored draws.
>    - State the block-split finding from L-R − L-P, with §17.5's reading.
>    - State the verdict, v4 or not adopted, with the first unmet condition; state mixed and
>      negative findings.
>    - Keep the Engineering status, the research finding and the product status (v1 released)
>      distinct. No promotion, freeze or economic claim.
> 8. Deliver §17.5's fit-cost and daily-retrain diagnostic in `reports/block-challenger/`.
> 9. Enforce and report every §17.8 cap from the first job, including controls, failures and
>    independent review, and respect the Friday/Shabbat calendar. At an exhausted cap, retain the
>    partial evidence and return the applicable non-PASS status.
> 10. Supply the durable evidence and executable reproduction commands: the protocol, lineage,
>     predictions, metrics, diagnostics, uncertainty with stored replicates, criteria, failures,
>     resources and the fit-cost report. Store hash-bound files byte for byte, and disclose
>     defects, repairs and invalidated outputs.
> 11. Deliver §17.9's publication packet and draft MLflow export, with public surfaces and the
>     published export set unchanged, CI green and no public write.
> 12. Obtain one fresh, independent Integration-Critic PASS on a clean detached checkout of the
>     exact final candidate. The review covers this entire checklist and:
>     - independently recomputes the saved-vector metrics, the paired, per-fold and ratio
>       intervals and the §17.6 verdict;
>     - representatively reproduces HG, a block and a pooled LightGBM selection and fit, and the
>       causal and state controls;
>     - re-derives the packet and the export.
> 13. Return the canonical packet (templates §3), together with the publication packet:
>     - both terminal SHAs and a verdict-only delta;
>     - reachable evidence;
>     - all resource totals and elapsed hours;
>     - branch and worktree accounting.
>
>     Stop at CP-21's local result.

**Mechanical consequence for the rule.** With this Engineering PASS, condition 3 of rule
`cp21-adoption` (§17.6) holds; conditions 1, 2 and 4 hold on this review's own recomputed rows.
The mechanical verdict is therefore **v4** (no unmet condition). The block-split finding
(L-R − L-P) is **no demonstrated joint preference**. This is a research status only: v1 remains the
released product and demo; nothing here promotes, freezes or makes an economic claim.

## Commands actually run

Environment: `P=/Users/djourno/Downloads/PJM; PY=$P/.venv/bin/python` (Python 3.13.15, LightGBM
4.7.0), `OUT=$P/.local/artifacts/cp-21/critic-2`, working directory the critic worktree,
`MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=true`. Every computing step ran through
`$PY scripts/cp21_blocks.py monitor --name <name> --workers <n> --log $OUT/<log> -- <command>`
against the shared cumulative ledger. Ledger job indices 75–98 are this review's.

**Identity and history (read-only, not monitored)**

| Command | Exit | Observed |
|---|---|---|
| `git -C <wt> status --porcelain`; `git -C <wt> rev-parse HEAD` (start, mid-review, end) | 0 | empty; `260dcf9fb3f5706cb896991ba7b6edf4cd9494b6` each time |
| `shasum -a 256 capstone_v21.md docs/track-b/capstone_v21-r5-to-v21-r6-amendments.md`; same via `git show 270a0a0:<file>` | 0 | `ee402c47…c867344`, `a9086fa1…50bedd` at both the candidate and the ratification commit `270a0a0` (on `main`) |
| `awk '/^### 17.10 /{f=1} /^### 17.11 /{f=0} f' capstone_v21.md` vs the brief's excerpt | 0 / diff 1 | byte-identical; the only difference is the trailing blank separator line |
| `shasum -a 256 docs/track-b/evidence/cp-21/issued-brief.md .local/artifacts/cp-21/issued-brief.md` | 0 | both `813fb8a476a7b6d10ecf0a5519e97ec8efc4ff36e0f13868676ad34534fc020f` |
| `shasum -a 256 docs/PUBLISH_RULES.md docs/track-b/publication-standard-v1.md docs/track-b/presentation-and-tracking-plan-2026-09-24.md docs/track-b/publication-packet-template.md` | 0 | `91eea445…`, `01d721c2…`, `28119374…`, `4efb0185…` — all as pinned |
| `git log --stat ffcf9f3..260dcf9`; `git log --format='%H %ad %cd %s'` | 0 | 5 commits: `b9d6310` brief (19:00), `49bcdfc` protocol (22:13:46), `bcf33dd` admission freeze (22:28:23), `cf1ed71` vectors before scoring (22:58:36), `260dcf9` candidate (23:42:49), all 2026-09-29 +03:00 |
| `git diff --name-only ffcf9f3..260dcf9` filtered by the §17.11 write paths | 1 (no match) | every changed path is inside §17.11; only `scripts/mlflow_export.py` is modified, the rest are additions |
| `git diff --stat ffcf9f3..260dcf9 -- reports/presentation README.md app docs/index.html pyproject.toml uv.lock` | 0 | empty: no public surface, published export, dependency pin or lock change |
| python: every `implementation_sha256` (22), `frozen_inputs_sha256` (10) and `preflight_sha256` (5) entry of `protocol.json` against the candidate files; `git show 49bcdfc:reports/block-challenger/protocol.json` vs the candidate | 0 | 0 mismatches; `protocol.json` byte-identical to the pre-run commit (SHA-256 `a51cfbbe…`); `git diff --stat 49bcdfc 260dcf9` over the 22 forecast-path files: empty |
| python: `protocol.json` `adoption_rule_verbatim` / `block_models_verbatim` vs the plan's §17.6 / §17.3 | 0 | both verbatim-equal |
| `git show cf1ed71:reports/block-challenger/predictions.parquet \| shasum -a 256` | 0 | `d8ba42e9…` = candidate file = `adoption.json` input hash; lineage origins/states/admission unchanged after scoring (only `research_summary` and the stage label added) |
| python over `artifact-manifest.json` | 0 | 66 files: every SHA-256 equals both the committed blob and the checkout; every tracked CP-21 file is manifested; `git check-attr` shows `text: unset` (`* -text`) |
| `git worktree list`; `git branch -vv`; `git for-each-ref refs/remotes`; `git tag --list` | 0 | `main` = `origin/main` = `ffcf9f3`; `gauntlet/cp-21` = `260dcf9` (Lead worktree `.local/worktrees/cp-21/lead`); no remote-tracking ref or tag for CP-21 |
| `$PY scripts/cp21_blocks.py status` (start / end) | 0 | start: `reference_passes` 2, `analysis_passes` 2, `lgbm_fits` 24,057, `machine_seconds` 20,743; end: see "Resources charged by this review" |

**Monitored jobs**

| # | Job and command | Exit | Observed |
|---|---|---|---|
| 75 | `critic2-tests-cp21`: `$PY -m pytest tests/cp21 -q -p no:cacheprovider` | 0 | 44 passed |
| 76 | `critic2-inspect`: `$PY $OUT/c2_inspect.py` (integrity only, no metrics) | 0 | 11 policies × 10,747 keys, each equal to CP-15's independent expected keys (fold counts 2,160/2,159/2,112/2,160/2,156; 448 represented days; fold 3 2,112 h/88 d; peak 408 h/17 d); all finite and ordered; new arms: 0 rows with p50 = central; truth/scale/level bitwise equal to HG for every policy; `origin_utc` = D−1 11:00 UTC; max date 2026-04-07; HGL blend gap max 1.99e-13 |
| 77, 78 | `critic2-reference-synthetic`: `$PY $OUT/c2_reference.py --synthetic` | 1, 1 | defects in my own script (a column named `shape`; tuple JSON keys), fixed; synthetic mode charges no pass |
| 79 | same | 0 | end-to-end code path on random vectors (77/1,573/4,950/105 rows aligned by key; loss values mismatch, as expected) |
| 80 | `critic2-bootstrap-synthetic`: `$PY $OUT/c2_bootstrap.py --synthetic` | 0 | code path OK; re-implemented CP-20 index generator SHA-256 `e1df9a68…f99b` = CP-20's |
| 81 | `critic2-reference-pass`: `$PY $OUT/c2_reference.py` — **charged `reference_passes` 2 → 3** before reading outcomes | 0 | 77/77 metric rows, 1,573/1,573 diagnostic rows, 4,950/4,950 daily rows, 105/105 criteria rows reproduced: worst relative difference 3.4e-16, criteria actual max 7.1e-15, statuses identical, support labels identical (all 1,485 hour/block rows `eligible`, i.e. ≥ 56 represented dates; new arms' minimum 86) |
| 82 | `critic2-bootstrap-pass`: `$PY $OUT/c2_bootstrap.py` — **charged `analysis_passes` 2 → 3** | 0 | index SHA-256 = CP-20's; 84/84 interval rows (max abs diff 3.5e-15; ratios 4.9e-16); 168,000 stored draws (1.4e-14) and 44,000 replicate scores (4.4e-16) reproduced; committed intervals = percentiles of committed draws (1.8e-15) |
| 83 | `critic2-lgbm-independent`: `$PY $OUT/c2_lgbm.py` (35 review fits, charged) | 0 | independent re-implementation of windows, blocks, 28-day split, §15.3 rule, grid, selection/tie and refit: L-P pooled fold_2 2021-06-10, L-R blocks fold_5 2026-02-12, L-N blocks at the warm-up origin fold_4 2025-04-12 — selected configurations, exact validation MAEs, row counts, window-row hashes, all 35 tree hashes and the central vectors equal the committed rows bit for bit (lineage central SHA for the warm-up origin, whose committed fit used data materialised before fold 4) |
| 84 | `critic2-review`: `$PY -m cp21.review --out $OUT/review.json --component fold_3:2022-08-24 --component fold_5:2026-03-02 --lgbm fold_1:2020-09-12:L-P --lgbm fold_3:2022-09-08:L-R --replay fold_3:2022-07-01:2022-07-24 --mask fold_4:2025-07-15:L-N` | 0 | both HG refits: A1/2+B2/2 bitwise = accepted CP-20 HG central, A1 and B2 bitwise = CP-20 cache; L-P and L-R: central bitwise, selection, validation MAE and tree hashes equal; replay from the admission-freeze commit `bcf33dd`: 2,112 rows bitwise equal to committed vectors; mask: delivery-day and future mask max abs 0.0, non-uniform D−1 mutation 65.14 EUR/MWh |
| 85 | `critic2-hlayer`: `$PY $OUT/c2_hlayer.py` (25 policy-days) | 0 | independent §14.2 reconstruction from each arm's own committed errors: HGL, L-P, L-R, L-N and HG at one mid-fold origin per fold, all 25 vectors bitwise equal; substituting HG's errors misses HGL's vector by 1.03–13.31 EUR/MWh |
| 86 | `critic2-state`: `$PY $OUT/c2_state.py` (22 policy-days) | 0 | on the committed admission-freeze L-N fold_5 state: continuous replay bitwise = committed; save/reload restart identical; D−1 refused, D−2 accepted once; repeat release consumes nothing; partial day never buffered; unavailable truth stays pending; backward origin refused |
| 87 | `critic2-wasm-payload`: `$PY scripts/build_wasm_payload.py` | 0 | payload 15,363,807 bytes; `reports/cp3b/payload.json` rewritten byte-identically (`git status --porcelain` empty) |
| 88 | `critic2-suite` (4 workers): `$PY -m pytest -q -p no:cacheprovider` | 0 | **1,131 passed, 8 skipped** |
| 97 | `critic2-skip-reasons` (4 workers): `$PY -m pytest -q -rs -p no:cacheprovider` over the skip-capable files and `tests/test_24_live_namespace_is_walled_off.py` | 0 | 535 passed; the 8 skips: `eccodes` absent (1), `marimo` absent (1), CP-16 identity bound to the v21-r3 anchor (1), CP-16 production verification needs its own ledger (5); the live-namespace wall ran and passed |
| 89 | `critic2-verify`: `$PY scripts/verify_release.py` (`make verify`) | 0 | "PASS — every bound claim agrees on every surface; the static page fetches nothing" |
| 90 | `critic2-guard`: `python3 scripts/publication_guard.py tree` | 0 | "the tree carries no placeholder and a final build record" |
| 91 | `critic2-export-check`: `$PY scripts/mlflow_export.py --check` | 0 | "the committed export is current" |
| 92 | `critic2-draft-check`: `$PY scripts/mlflow_export.py --draft cp21 --check` | 0 | "the committed draft export is current" |
| 93 | `critic2-packet-check`: `$PY -m cp21.packet --check` | 0 | `draft_registry_identical_to_committed: true` |
| 94 | `critic2-claims-check`: `$PY -m cp21.claims --check` | 0 | claim map and publication packet identical to committed; 0 lint findings |
| 95 | `critic2-report-check`: `$PY -m cp21.report --check` | 0 | `report.md` and `fit-cost.md` identical to committed |
| 96 | `critic2-weather`: `$PY $OUT/c2_weather.py` | 0 | 2,476 retained runs regenerated through CP-20's frozen conversion: 59,446 rows, keys, values and statuses bitwise equal; design SHA-256 `f5a9c6ed…274c0`; only missing values are the 24 structural 2019-01-01 hours; max date 2026-04-07 |
| 98 | `critic2-e1check`: `$PY $OUT/c2_e1check.py` (no fit) | 0 | missing weather exists only on 2019-01-01 (structural, never an eligible row: the first eligible row is 2019-01-31) and 2022-09-29..2023-03-24 (no frozen record, outside every window: fold 3's windows end by 2022-09-27 and fold 4's first window starts 2023-03-25); consistent with E1's statement and with 0 failures |

Also run (read-only python over committed files, not monitored): fit-cost and daily-cycle
re-derivation from `fits.parquet` (totals, capacity counts, 1.749× ratio, median 24.72 s / max
69.44 s at 25 origins, five per fold; all 4,452 final configurations equal the argmin of their
inner validation MAE with ties to the smaller); admission-freeze lineage at `bcf33dd` (140
admission vectors on D0−8..D0−2, 28-day buffers ending ≤ D−2, latest day 2026-01-07); every one of
the 1,932 predicted origins in the candidate lineage has a 28-day buffer ending ≤ D−2; each arm
covers exactly the 638 manifest origins; the 7 re-scored saved references equal CP-20's committed
`metrics.csv` rows exactly (0.0); the draft export's run names, tags, statuses and sampled values
against `metrics.csv`/`uncertainty.csv`; every claim-map line reference (U21 L2–L85, M21 L3–L78,
D21 L998/L1141) points to the named row and its rounding is correct; the local MLflow store opened
read-only (`sqlite …?mode=ro`): experiment `delu-generations`, runs `cp21`, `cp21/HGL`, `cp21/L-P`,
`cp21/L-R`, `cp21/L-N`, names as in the draft; ledger calendar and concurrency (no job in the
Friday/Shabbat window; peak declared concurrent workers 4).

## Evidence actually inspected

- **Governance and bar:** `AGENTS.md`, `engineering-role.md` (§ Integration Critic protocol), `docs/track-b/gauntlet-templates.md` §2; `capstone_v21.md` §§1–4, 8–9, 14.1–14.6, 15.1–15.3, 16 and 17.1–17.11; `docs/track-b/evidence/cp-21/issued-brief.md`.
- **Code:** `src/cp21/{protocol,lgbm,inputs,execution,scoring,evaluate,controls,daily,review,components,finalise,packet,tracking,jobs,budget}.py`, `scripts/cp21_blocks.py`, the draft path of `scripts/mlflow_export.py` (diff from base), `src/cp16/residuals.py`, the relevant parts of `src/cp15/data.py`, `src/cp15/models.py`, `src/cp15/scoring.py`, `src/cp20/scoring.py`, `src/cp20/weather.py`; `tests/cp21/test_guards.py`, `test_blocks_and_blend.py` (partly).
- **Evidence files:** `protocol.json`, `preflight/{input-verification,weather-regeneration,benchmark,thread-determinism}.json`, `lineage.json` (candidate and `bcf33dd`/`cf1ed71` versions), `predictions.parquet`, `metrics.csv`, `diagnostics.csv`, `uncertainty.csv`, `replicates.parquet`, `replicate-scores.parquet`, `criteria.csv`, `adoption.json`, `fallback.csv`, `failures.csv` (header only: 0 failures), `controls.json` (49 checks, all passed), `hg-parity.json` (10,747 rows bitwise), `daily-cycle.json`, `fit-cost.{md,csv,json}`, `fit-cost-by-origin.csv`, `fits.parquet`, `resources.json`, `draft-registry.json`, `mlflow-export-draft/cp21.json`, `mlflow-local.json`, `published-export-diff.json` (23 runs, only identity, 0 substantive changes), `defects-and-repairs.md` (D1–D7), `artifact-manifest.json`, `report.md`, `reproduce.md`; `docs/track-b/research-content/cp21-claims.md`; `docs/track-b/evidence/cp-21/publication-packet.md` (every template section present; §5b and §5d not applicable with reasons); the shared ledger `.local/artifacts/cp-21/ledger/budget.json` (jobs, events, pauses, peaks).
- **Saved inputs:** `reports/weather-ablation/{predictions.parquet,metrics.csv,uncertainty.csv,weather-features.parquet,run-manifest.json}`, `reports/cp15/{predictions.parquet,protocol.json}`, `reports/v2-causal/input-manifest.json`, `data/snapshot.parquet` (filtered to 2019-01-01..2026-04-07 before materialisation), `.local/artifacts/cp-20/weather` (read through CP-20's conversion) and `.local/artifacts/cp-20/hg-components` (through `cp21.review`).
- **This review's outputs** (outside the checkout, in `/Users/djourno/Downloads/PJM/.local/artifacts/cp-21/critic-2/`), as `shasum -a 256` lines:

```text
ba6af3bf70bd30f0417ce45d6c8a6c568c434be38ce95b6af8bcd55c1308f674  reference-real.json
1bffe5eeb9b942d8e355568a6760f83cf8baf1cf19c293fe784e97089c166520  critic-criteria-real.csv
6442857eda99d38275bf1e761f6bb45a042618ff020a7e14e588fe79a8326023  critic-daily-real.parquet
3c8008ee440b98519e367cff75658170713b128818e9c16cd214ce5751e4403d  bootstrap-real.json
f2ece32281dcfc963ba4f94303954620b182f5b401c88f15b9737f56f16f2533  critic-uncertainty-real.csv
84bf2bba69a070336ab20cf6055d25e354e3d700e91c83582e0500a8567ad4b0  lgbm-independent.json
eda46893a7a225495ca40b6da9d982b1dcf64c8e9a02303a4f2ed633def35f80  review.json
05efb5e6f57eaa33c5cf7cf9a6db8f963e00c30bb37eece4c3b97d986d86a709  hlayer-independent.json
8b8d2d6356e7a478f9d530965354977293bbac7b2ee58cc91fd026f8cdc04235  state-controls.json
82b675d9f847d12280a59deef147a39016f99785e08e2e2befc425985666b5d5  weather-regeneration.json
89091bb74c7e568be6a6a51b0fd0a6e8fe5296859427ed4fe45e4f2b7c47dbd9  inspect.json
9ee96e2fa7240b209d787fbfcaccbafd581312744741c9fc856ed599b4d17715  c2_inspect.py
ad898aff28b6b5495bbeafbfc4c1da33beea127c309e42b9376931b6cd901fdf  c2_reference.py
f41db82de75603fdf4fb68de5d787b3a030e8dc3bbef1cf0a94b56035181d357  c2_bootstrap.py
b3a8b7b76cd4246b365046db8c3ca76b8e19b08e21a111a025deb6719f4c95ed  c2_lgbm.py
8a304963cea6b6968661373f46fd87b1b21ce1c9d57d6eb59b3c292caa109f1b  c2_hlayer.py
12d9a8735384dbdad43df99f463cd9fb4517a70171f5a8d73c759ed7d67bf2de  c2_state.py
e8836d80ab26c6b0968789d5c131572c881e7e1b55b74f34c8c4e0ec16d2a73a  c2_weather.py
811d64eb142f0d20d13a177aa05fa0d6908d8e277abab8d727cfb853eedc9aa0  c2_e1check.py
```

## Recomputed headline values (this review's own rows)

| Quantity | Value |
|---|---|
| S_MAE / S_WIS | HGL 0.5357 / 0.5056; HG 0.5658 / 0.5322; L-P 0.5785 / 0.5477; L-R 0.5835 / 0.5540; L-N 0.5769 / 0.5402; B3 0.7841 / 0.7399; B2 0.6578 / 0.6390; B1 1.0518 / 0.9856; B0 1 / 1 |
| HGL − HG (condition 1) | ΔS_MAE −0.0301 [−0.0368, −0.0228]; ΔS_WIS −0.0266 [−0.0327, −0.0204]; ratios −5.32% [−6.37%, −3.97%] and −5.01% [−5.95%, −3.80%] |
| HGL − HG per fold, MAE / WIS (condition 4) | f1 −0.323 [−0.491, −0.179] / −0.190 [−0.280, −0.100]; f2 −0.668 [−1.029, −0.360] / −0.348 [−0.526, −0.194]; f3 −1.008 [−2.556, 0.586] / −0.781 [−1.698, 0.088]; f4 −0.864 [−1.111, −0.629] / −0.471 [−0.629, −0.322]; f5 −0.688 [−0.970, −0.220] / −0.365 [−0.505, −0.137] — no lower endpoint > 0 |
| §8 (condition 2) | HGL met (21/21 rows); HG met; L-N met; L-P not met (criterion 4); L-R not met (criteria 4, 5) |
| Block split L-R − L-P | ΔS_MAE +0.0050 [−0.0084, 0.0142], ΔS_WIS +0.0063 [−0.0050, 0.0135]: no demonstrated joint preference (both higher, both intervals span zero) |
| Other secondary contrasts | L-P − B3 observed joint improvement (−0.2056 / −0.1922, both intervals below zero); L-N − L-R, L-P − HG, L-N − HG no demonstrated joint preference (both span zero); L-R − HG no demonstrated joint preference with the S_WIS interval wholly above zero (+0.0218 [0.0004, 0.0450]) |
| Peak 2022-08-15..31 (descriptive) | HGL MAE 50.09, WIS 28.02, 382/408 hits; HG 47.52, 27.31, 383/408 — HGL's peak MAE is higher, as the report states |
| §17.6 | condition 1 met; 2 met; 3 met with this Engineering PASS (all 10,747 keys finite and ordered for every arm); 4 met → **v4**, no first unmet condition |

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1 | Repository/input state; prior evidence and other sessions' work preserved; anchor and amendment on `main`; issued brief packaged byte for byte with SHA-256; frozen pre-run protocol committed before any outer scoring | **PASS** | Anchor `ee402c47…` and amendment `a9086fa1…` on `main` at `270a0a0` and unchanged at the candidate; brief `813fb8a4…` = canonical copy, recorded in `protocol.json` and `inputs.ISSUED`, stored `-text`; base `ffcf9f3` = `main` = `origin/main`, nothing outside §17.11 changed and no existing file deleted; `protocol.json` committed at `49bcdfc` (22:13:46) before the first main fit job (22:13:54) and the scoring job (23:01:27) and byte-identical since; it holds arms, blend weights, block map, 29-column feature list and §15.3 rule, grid G1–G4, 28-day inner split, tie rule, E2 fixtures, seeds 42/15042, the 638-origin table and key SHA-256 (verified against the manifest), cache identities, caps/E1/E3 accounting and §17.6/§17.3 verbatim; only accuracy-blind training-only benchmark/determinism fits preceded it |
| 2 | CP-20 population/manifest identities; frozen weather from retained grids; HG components only with verified identity; independent representative HG reproduction; no retrieval; nothing after 2026-04-07 | **PASS** | Keys equal CP-15's independent expected keys; manifest 638 origins/35 admission dates/warm-up starts verified; my regeneration of all 2,476 retained runs is bitwise equal (design `f5a9c6ed…`); Lead's preflight verified all 638 HG cache entries; my HG refits at fold_3 2022-08-24 and fold_5 2026-03-02 are bitwise equal to the accepted CP-20 HG central and to the cache; `download_bytes` 0; every loader filters to ≤ 2026-04-07 before materialisation and every vector's max date is 2026-04-07 |
| 3 | Exactly L-P, L-R, L-N, HGL with training-only capacity selection for every LightGBM model; the three parity proofs | **PASS** | Only four new arms in predictions/fits (7 models × 3,180 fits); all 4,452 final configurations equal the inner-validation argmin (ties to the smaller), validation inside each window's last 28 days; my independent re-implementation reproduces pooled and block selections, trees and centrals bit for bit. HGL: components bitwise equal to HG's (refits and cache), blend gap ≤ 1.99e-13, and my own §14.2 reconstruction from HGL's own errors is bitwise equal (HG's errors would differ by up to 13.3 EUR/MWh). L-R vs L-N: one code path differing only in target/feature representation; both reproduced independently. L-P vs L-R: identical rows (control `pooled_block_rows_equal`), features, target, grid, rule and H path; both reproduced independently |
| 4 | Every §17.7 control with transform-surviving positive controls; inherited regression and namespace guards rerun without live mutation | **PASS** | `controls.json`: 49 checks all passed (delivery-day mask 0.0 with non-uniform D−1 mutation moving every arm incl. L-N and HGL; future weather 0.0; cross-date permutation and within-day rearrangement of weather move every LightGBM arm; ×3 scaling invariance shown as diagnostic only; training-only selection both directions; pooled–block parity; DST blocks; state/cache refusals; boundary guard with positive control; n_jobs 4 = main run); schema refusal of post-gate/actual columns tested with positive control (`tests/cp21/test_guards.py`); my reproductions: mask 0.0 / D−1 mutation 65.14 (L-N fold_4), replay from `bcf33dd` bitwise (fold_3, 22 days × 4 arms), 8/8 state controls on a different arm and fold; full suite 1,131 passed incl. `test_24_live_namespace_is_walled_off.py`, no live mutation |
| 5 | All 10,747 keys per new arm, finite ordered quantiles, emitted p50 separate from central; failures, exclusions and fallback accounted without changing denominators | **PASS** | 4 × 10,747 = 42,988 rows, keys equal the expected keys, all finite and ordered, `central` and `p50` separate columns with no row equal; `failures.csv` empty (0 fit failures; no failure JSON); fallback 0 of 11,592 hour cells per arm (`fallback.csv`); exclusions are only CP-20's original ones (fold 3's 2022-07-20/21 without eligible hours; one excluded hour on each of 2021-04-04, 2026-03-30, 2026-03-31 and 2026-04-05; 2026-03-29 is a canonical 23-hour DST day), denominators identical for all eleven policies |
| 6 | Score all eleven policies; independently verify scores and equal-fold normalization, every per-fold/hour/block/stress/peak diagnostic with denominators and support labels, coverage with width, all six §8 diagnostics per new arm | **PASS** | My charged reference pass reproduces every row of `metrics.csv` (77), `diagnostics.csv` (1,573 + 4,950 daily), `criteria.csv` (105) to ≤ 3.4e-16 relative, including represented-date lists and support labels; saved references equal CP-20's committed rows exactly; coverage 50/80/95 reported with mean/median/p95 width and tail misses per fold, hour, block and peak |
| 7 | §17.6 applied mechanically; contrasts with paired, per-fold and ratio intervals from the checkpoint's stored draws; block-split finding; verdict with first unmet condition; mixed/negative findings; statuses kept distinct | **PASS** | My charged bootstrap pass reproduces all 84 interval rows, the 168,000 stored draws and 44,000 replicate scores with CP-20's index set; §17.6 on my rows: 1, 2, 4 met, 3 met with this PASS → v4 (matches `adoption.json`); block split "no demonstrated joint preference" with both directions shown; mixed/negative findings stated (L-R − HG S_WIS worse, L-P/L-R fail §8, HGL's higher peak MAE, fold-3 intervals spanning zero); `report.md` separates research verdict, Engineering status (bound to this verdict), product status (v1 released) and states no promotion, freeze, Live or economic claim |
| 8 | §17.5 fit-cost and daily-retrain diagnostic in `reports/block-challenger/` | **PASS** | `fit-cost.{md,csv,json}`, `fit-cost-by-origin.csv`, `fits.parquet`: rows, selected capacity, inner/final wall and CPU seconds and worker memory by arm, model and origin, block vs pooled 1.749× (re-derived); HG regeneration disclosed (none in the main run; 12 control + 50 daily-cycle check refits); `daily-cycle.json`: 25 cold origins, five per fold, 4 workers, median 24.72 s, max 69.44 s (re-derived), refitted A1_w/B2_w bitwise = CP-20 and blocks/HGL vector bitwise = main run; labelled diagnostic only (D3) |
| 9 | Every §17.8 cap enforced and reported from the first job, including controls, failures and review; Friday/Shabbat respected; non-PASS at an exhausted cap | **PASS** | Ledger initialised before the first job (pre-ledger orientation conservatively charged); monitor charges wall × workers, refuses a fifth worker and the calendar window; every counter reserved before use; no cap exceeded (end of review: LightGBM 24,157/35,000, main 22,260/24,000, component-days 72/1,600, Lasso 8,630/192,000, policy-days 4,190/10,500, machine-hours 6.13/60, peak RSS 3.95 GB/10 GiB, added disk 0.53 GB/20 GiB, 0 downloads, 0 remote writes); all jobs on Tue 29 / Wed 30 Sep, none in the window; peak declared concurrency 4; failed/stopped jobs charged and disclosed; `resources.json` reports every cap at the candidate. Reference and bootstrap passes now stand at **3/3 — reached, not exceeded**, by this review's allotted passes; no non-PASS trigger arises because the work is complete |
| 10 | Durable evidence and executable reproduction commands; byte-exact hash-bound files; defects, repairs and invalidated outputs disclosed | **PASS** | All listed artifacts present; `reproduce.md` gives the monitored commands (the check commands in its §5 ran green here); `artifact-manifest.json` binds 66 files, all hashes equal blob and checkout, `.gitattributes` `* -text` / `-text` effective; `defects-and-repairs.md` D1–D7 match the ledger's failed/stopped jobs (verify-weather, benchmark, fit-cost) and state no invalidated committed output; comparison vectors byte-identical to the pre-scoring commit |
| 11 | §17.9 publication packet and draft MLflow export; public surfaces and published export unchanged; CI green; no public write | **PASS** | Packet fills every template section, claim map SHA `8df2e9a5…` and draft SHA `0f23d52d…` as stated; `cp21.packet/claims/report --check` and `mlflow_export.py --draft cp21 --check` regenerate identical files; names/statuses follow the draft entries and the mechanical verdict (parent `v4 · three-block LightGBM added (CP-21)`, HGL `generation v4`, study arms `not adopted`, statuses pending at landing); sampled exported values equal committed rows; published export `--check` current and record-level diff only-identity (23 runs, 0 changes); no public-surface diff; CI-equivalent steps green locally (payload, 1,131-test suite, `verify_release.py`, `publication_guard.py tree`); local MLflow store only (`remote_writes` 0; no remote ref for CP-21). GitHub CI itself was not run (no push is authorized) |
| 12 | One fresh, independent Integration-Critic PASS on a clean detached checkout of the exact final candidate, covering the whole checklist, with the named recomputations, reproductions and re-derivations | **PASS** (this verdict) | Clean detached worktree at `260dcf9…`; saved-vector metrics, paired/per-fold/ratio intervals and the §17.6 verdict recomputed with my own code (jobs 81, 82); HG, one pooled and three block selections-and-fits reproduced independently (job 83) and through `cp21.review` (job 84); causal controls (job 84 mask) and state controls (jobs 84 replay, 86); H layer reconstructed (job 85); packet and export re-derived (jobs 91–95 plus manual row checks) |
| 13 | Canonical packet (templates §3) with the publication packet: both terminal SHAs and verdict-only delta; reachable evidence; all resource totals and elapsed hours; branch and worktree accounting | **Not yet due — the Lead's post-verdict obligation** | What can exist at the candidate does: `resources.json` (candidate-time totals), the publication packet, reachable candidate history on `gauntlet/cp-21`. The return, `evidence_tip_sha`, the verdict-only delta (`git diff --name-only 260dcf9..<evidence_tip>` must stay inside `docs/track-b/evidence/cp-21/`), final resource totals including this review (`src/cp21/finalise.py` names `docs/track-b/evidence/cp-21/resource-final.json`; the report says the final totals will be in the evidence directory) and branch/worktree accounting (`gauntlet/cp-21`, `.local/worktrees/cp-21/lead`, `.local/worktrees/cp-21/critic-2`) are written after this verdict |

## Resources charged by this review

Ledger jobs 75–98: machine time ≈ 0.37 h (1,336 s, wall × declared workers);
LightGBM fits +100 (35 independent + 65 `cp21.review`, all `lgbm_fits_review`); HG component-days
+4 (+480 Lasso attempts, charged by `counted_lear`); policy-days +143 (96 replay, 25 H-layer, 22 state);
`reference_passes` +1 (→ 3/3); `analysis_passes` +1 (→ 3/3). Ledger totals at the end of the review:
`lgbm_fits` 24,157, `main_lgbm_fits` 22,260, `lgbm_fits_review` 365, `component_attempts` 72,
`primitive_fits` 8,630, `policy_days` 4,190 (review 891), `machine_seconds` 22,079 (6.13 h), peak
aggregate RSS 3,952,017,408 B, peak added disk 530,694,395 B, active-hours upper bound 3.42.

## Non-blocking observations

1. `src/cp21/daily.py` says each cold cycle loads "everything a live system has on the morning of
   D−1", but `load(root, before=day + 1)` materialises delivery day D's rows including its prices.
   The forecast is unaffected (the delivery-day mask control gives exactly 0.0 and the cycle's
   vectors equal the main run bit for bit); it is a wording inaccuracy in a diagnostic's docstring,
   not in any evidence claim.
2. With this review the metric-only reference and bootstrap pass caps are fully used (3/3). No
   further scoring or bootstrap pass is available under §17.8; the Lead's final resource totals
   should say so.
3. The 8 skipped tests are environment-gated (no `eccodes`, no `marimo`, CP-16's production checks
   need their own ledger or the v21-r3 anchor); none is a CP-21 test and none is caused by a CP-21
   change (CP-21 touches neither those tests nor the anchor).
4. The worktree was created by the Lead and is left in place for the Lead to remove under its
   lifecycle; this review wrote only under `.local/artifacts/cp-21/critic-2/`.

## On FAIL only

Not applicable: the verdict is PASS.
