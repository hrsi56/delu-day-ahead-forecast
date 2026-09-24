# Verdict — CP-20 — Integration — PASS

- Candidate SHA: `3e9ff8b500c2c655fea810ae11886503927f176c`
- Plan / version / bar: `capstone_v21.md`, v21-r4 (ratified), SHA256 `150bd53fa15067b1d138c95d0912f86a1e92ce74092059be09034758c1926167`, §15.6. The bar inherits the §14.8 verification standard, §§15.1–15.5 and §§14.1–14.4. It is read with `docs/track-b/capstone_v21-r3-to-v21-r4-amendments.md` (SHA256 `3e0bdf6a343d5336f406f0eeb726b1b65c0f767ec8d9418a7d8118902e1ace55`) and `docs/track-b/cp-20-direct-weather-brief.md` (SHA256 `28a4e195fa7f66ff3270d5d54e477478e90aa42124bceb1ee529f95f5761883e`). All three hashes match the bytes at the candidate.
- Assignment: `.local/artifacts/cp-20/critic-2/assignment.md`, SHA256 `615f5b2a2bfe1f3b06d53a20864b99b7850819e2da6808c2abcea36cb7cc6cb4` (verified). Decode list: `.local/artifacts/cp-20/critic-2/eligible-decodes.txt`, SHA256 `d35faaa4b4114edce9207823b2bf6f373f75e8bd64d6908bb6e3ca49a86e88f8` (verified; 1,035 paths).
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

  (The excerpt is the citation. My own script found all 35 lines verbatim in the checkout and in `git show HEAD:capstone_v21.md`. As a courtesy, it starts at line 901.)
- Worktree clean before and after: **yes**. `/Users/djourno/Downloads/PJM/.local/worktrees/cp-20/critic-2` is detached at `3e9ff8b…`. `git status --porcelain` was empty at the start, after every job and just before this file was written. `--ignored` also showed nothing. HEAD never changed. I made no Git writes and edited no tracked file. As the assignment instructs, the worktree stays in place for the Lead to remove.

## Commands actually run

Every compute job ran from the Critic worktree through the monitor with `PYTHONDONTWRITEBYTECODE=1`:

`$PY scripts/cp20_weather.py --monitor --name critic2-<x> --workers 1 --log /Users/djourno/Downloads/PJM/.local/artifacts/cp-20/critic-2/logs/critic2-<x>.log -- <cmd>`

- `PY=/Users/djourno/Downloads/PJM/.venv/bin/python`.
- `WX=/Users/djourno/Downloads/PJM/.local/artifacts/cp-20/wx-venv/bin/python` (ecCodes 2.49.0, numpy 2.5.3).
- Scripts: `.local/artifacts/cp-20/critic-2/scripts/`. Outputs: `.local/artifacts/cp-20/critic-2/out/`.

The scripts are my own. They import nothing from the candidate's scoring or H-layer code. Where the candidate's code is used, it is named below.

| Ledger job | Command | Exit | Observed output |
|---|---|---|---|
| — | `git status --porcelain`; `git rev-parse HEAD`; `shasum -a 256` on the assignment, decode list and 3 issued documents; `git branch -avv`, `git worktree list`, `git log main..HEAD`, `git diff --name-status main..HEAD` | 0 | The worktree is clean and HEAD is `3e9ff8b…`. All 5 hashes match. `gauntlet/cp-20` is at `3e9ff8b` and `main` at `88c68cf`. The candidate is 22 commits ahead of `main` and 0 behind. The diff has 229 paths, all additions, all inside §15.7. |
| 83 | `critic2-static`: `$PY -u critic2_static.py` | 0 | 69 checks, with 67 genuine passes. The other 2 failed only because my own expectations were wrong. **(a)** `dswrf_param`: 24,760 DSWRF messages have discipline 0 / category 4 / **parameter 192**, the NCEP local DSWRF code, with shortName `sdswrf` in every version. I had expected WMO 7. The code is consistent everywhere and my own decode (job 87) agrees. **(b)** The admission raw-sample hash list has **800** entries (600 GFS + 200 ICON), not the 600 I expected. All 800 re-hash equal. Details under the items below. |
| 84 | `critic2-scoring`: `$PY -u critic2_scoring.py`. Reserves `analysis_passes=1, reference_passes=1` first. | 0 | The pass was reserved (counts now 3/3 each). I re-scored all 75,229 rows with my own code. There are 1,022 summary cells (pooled, per fold, 24 hours, 3 blocks, peak, recovery), all present. Max abs diff ≤ 5.7e-14. The 3,150 daily rows match to ≤ 5.7e-14, with identical n_hours and NaN pattern. S scores match to ≤ 2.2e-16. The 42 §8 criteria rows have the same pass/fail and values within 7.1e-15. The bootstrap index SHA256 `e1df9a68…f99b` equals lineage. The 12 uncertainty rows match to ≤ 7.1e-15. The joint rule gives **observed joint improvement**. |
| 85 | `critic2-replay`: `$PY -u critic2_replay.py`. Reserves `policy_days=1276` first. | 0 | My own §14.2 H layer, run as one continuous replay per fold and arm. **Vectors:** all 21,494 evaluation rows (7 quantiles, central, scale) are **bitwise equal**. All 70/70 admission `vector_sha256` values match, as do all 896/896 evaluation-origin buffer_sha256 / buffer dates / hour_support records and all 10/10 final per-fold states. **Scale:** my scale, computed from the snapshot, equals the CP-15 issued scale on all 598 CP-15-sourced days and the HG cache scale hash on all 636 days with eligible hours. **Other:** 0 failures and 0 fallback cells (of 23,184). Buffers are identical between arms. Incomplete issued days (for example 2021-03-29/30 and 04-04) are never buffered. |
| 86 | `critic2-components`: `$PY -u critic2_components.py`, using the candidate's `check_protocol`, `weather_design`, `hg_identity`, `augment` and `counted_fits(b, main=False)` around inherited `cp15.models.fit_day` | 0 | The identity fingerprint recomputed at the candidate equals the lineage value `132369…a591`. There are 6 origins (4 reproduction + 2 control), none used by the Lead or by attempt 1. All 6 are **bitwise equal** to the HG cache, with fit logs equal apart from timing. My own local-hour weather lookup equals the appended columns on 11,918–17,484 training and forecast rows per origin, and the other columns are unchanged. The controls and refusals are under item 4. Charged: 36 component attempts, 4,310 primitive fits (3,448 inner, 862 final) and 18 policy-days. |
| 87 | `critic2-decode`: `$WX -u critic2_decode.py`, with 1 × `reserve(message_attempts=1)` before each decode | 0 | 1,035/1,035 listed messages. Each was sha256-checked, decoded once (journal-guarded) and had its box selected by decoded coordinates: 55.25→47.0 °N × 34, 5.5→15.5 °E × 41. **All 1,035 boxes are bitwise equal to the stored run boxes.** Metadata problems: 0. The split is v14 90, v15.1 195, v16 750, across 23 runs. |
| 88 | `critic2-convert`: `$PY -u critic2_convert.py` | 0 | My own §15.2 conversion from my own decode. 495 canonical hours were reconstructable from the decoded leads, over 23 runs, 8 DST days, and versions v14, v15.1 and v16. Differences from `weather-features.parquet`: **0.0** for wind10, wind100 and DSWRF. Clip counts are equal. Units and levels: m s⁻¹ at heightAboveGround 10/100, and W m⁻² at surface. |
| 89 | `critic2-attempts` (first try) | 1 | My own JSON-serialisation bug (tuple keys). It only reads logs and charged no counter except 1.1 machine-seconds. |
| 90 | `critic2-attempts`: `$PY -u critic2_attempts.py` (log reads only) | 0 | **Successes:** 123,800/123,800 messages succeeded, with at most 2 successes per message. **Tries:** under the O2/O2-A1 counting rule, at most 1 counted failure per message (20 messages). Tries that received a response number at most **3** per message. Counting every try of any outcome, 25 messages had 4, each of them 3 responses + 1 network failure with no response. **Retained raw:** tries + attempt-1 review + this review ≤ 3 for all 1,150 retained messages, even on the all-tries basis. **Requests:** 216,614 requests went to 2 hosts only. The largest body was 4.73 MB. Unranged requests are only `.idx` (17,490) and listings (32), each ≤ 135 KB. |
| 91 | `critic2-tests`: `$PY -m pytest tests/cp20 -q -p no:cacheprovider --basetemp=.local/tmp/cp-20/critic-2/pytest` | 0 | 86 passed, 1 skipped. The skipped test is `test_gfs_eccodes`, an ecCodes import-skip that runs in job 92. |
| 92 | `critic2-tests-wx`: `$WX -m pytest --noconftest` on the six WX test files listed in `reproduce.md` §5 (`-q -p no:cacheprovider --basetemp=…/pytest-wx`) | 0 | 75 passed |
| 93 | `critic2-guards`: `$PY -m pytest tests/test_02_rolling_closed_left.py tests/test_05_schema_firewall.py tests/test_08_partition_integrity.py tests/test_12_partition_exclusion.py tests/test_24_live_namespace_is_walled_off.py tests/cp16/test_residuals.py tests/cp16/test_scoring.py -q -p no:cacheprovider --basetemp=…/guards` | 0 | 70 passed |
| — | Read-only inspection with system `python3` and `git`: ledger versus snapshot, `git log` of frozen files, first request versus freeze commit, dossier and admission exceptions, the report | 0 | Evidence cited under the items below |

## Evidence actually inspected

- **Governance:**
  - `AGENTS.md`, `engineering-role.md` (Integration Critic protocol), `docs/track-b/gauntlet-templates.md` §2.
  - `capstone_v21.md` §§7–8 and §§14–15, the v21-r3→v21-r4 amendment, the CP-20 brief.
  - The presence and hashes of `docs/track-b/weather-content-intake-2026-09-23.md` and `reports/weather-admission/`.
- **Candidate code (read):** `src/cp20/{execution,components,weather,inputs,scoring,controls,controls_supplement,budget,finalise}.py`, `scripts/cp20_weather.py`, `src/cp16/residuals.py`, `src/cp15/{data,models,scoring}.py` (definitions), `src/delu_forecast/features.py` (168-hour scale window), and the test inventories of `tests/cp20` and `tests/cp16/test_residuals.py`.
- **CP-20 artifacts:**
  - `protocol.json`: all 84 bound hashes recomputed.
  - `artifact-manifest.json`: all 41 entries recomputed; it covers all 42 tracked outputs.
  - `run-manifest.json`, `messages.parquet` (123,800), `weather-features.parquet` (59,446), `predictions.parquet` (75,229), `lineage.json`, including the versions committed at `30a958a`.
  - `metrics.csv`, `diagnostics.csv`, `uncertainty.csv`, `criteria.csv`, `fallback.csv`, `failures.csv`, `missingness.csv`, `radiation-clipping.csv`, `extended-inventory.csv`, `sample-hash-comparison.csv`, `extraction-summary.json`, `extraction-repairs.json` (r1–r12, O1, O2, O2-A1, S1, O3, O4, run plan), `post-freeze-repairs.json` (r13, finaliser, rights notice, r14), `.gitattributes`, `causal-controls*.json`, `resources.json`, `rights-notice.md`, `report.md`, `reproduce.md`.
  - `docs/track-b/evidence/cp-20/`: the README, the ledger snapshot, and attempt 1's verdict, used only to confirm what r14 repaired.
- **Inherited inputs:**
  - `reports/v2-causal/{predictions.parquet,lineage.json,input-manifest.json,resources.json}`.
  - `reports/cp15/predictions.parquet` and `reports/cp15/folds/*-issued.parquet`.
  - `data/snapshot.parquet` and `data/partitions.json`.
  - `reports/weather-admission/hashes/*.sha256`: 53 report files and 800 raw samples re-hashed.
- **Local evidence (read-only):**
  - `.local/artifacts/cp-20/ledger/budget.json`.
  - All 2,476 `weather/runs/*.json`, with all 2,476 `*.npz` re-hashed.
  - The 1,150 files in `weather/raw/`, all re-hashed; 1,035 of them decoded.
  - `weather/attempt-outcomes.jsonl`, `o2-a1-restored-attempts.jsonl` and `requests.jsonl`.
  - All 638 `hg-components/*/*.json`, each digest recomputed. The cache-set digest (sha256 of the sorted per-file sha256 list) is `901d7f3ff674f237329640dda179ddce06a647b05e57f838edfc64f07d0c70fa`.
  - The 600 admission GFS samples in `.local/weather-admission/cache/gfs/`.
- **Critic outputs (local, sha256):**
  - `out/static.json` `ed72555a…0bec`
  - `out/scoring.json` `2dcf9a76…ce1f97`
  - `out/replay.json` `f73a593e…10bd`
  - `out/components.json` `3393fcaa…0bd`
  - `out/decode-summary.json` `7ceb11f6…d64d`
  - `out/decode-journal.jsonl` `c01a8355…5da3`
  - `out/decoded-meta.json` `70dd565a…59bb`
  - `out/convert.json` `4119e6cb…2727`
  - `out/attempts.json` `8b49e3e5…b460`
  - The 23 decoded boxes in `out/decoded/` stay local under the rights notice. Their set digest is `bfbe482a…5316`.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1 | Repository/input state; other work retained; exact anchor/amendment/brief packaging; frozen manifests before comparison | **PASS** | **Issued documents and admission bundle:** the anchor, amendment and brief are byte-exact to their issued SHA256s and came in from `main` `88c68cf`. The admission bundle and intake receipt are present. The admission hash lists re-verify: 53 report files and 800 raw samples.<br>**Other work untouched:** the branch adds 229 files within §15.7 and changes nothing else. `main` and the other-session branch (`claude/word-rtl-issues-3286df`) are untouched. Prior CP-15 and CP-16 evidence is unchanged; the references are bitwise equal to CP-15.<br>**Freeze order:** `run-manifest.json` and `extraction-protocol.json` were committed at `86d8e1f` (17:07:44Z). The first request followed at 17:07:58Z and the first ranged request at 17:09:42Z. The conversion (`weather.py`) was frozen at `fc4f1c8`. The pre-fit `protocol.json` (manifests, missingness, conversion and budget caps E3) was committed once, at `255ecfb`. The admission freeze `30a958a` precedes comparison.<br>**r14 repair verified:** every one of the 84 hashes bound in `protocol.json` equals the committed bytes, including `prerun-attempts.csv` = `859ba632…`, now stored `-text`, with content identical to the freeze commit apart from line endings. All 41 `artifact-manifest.json` entries match. The candidate's own `check_protocol` passes in this clean checkout. The implementation bytes are unchanged since `255ecfb`. |
| 2 | Eight-run extension closed; metadata; source and endpoint identity; availability basis; disclosures; extraction gaps | **PASS** | **Run manifest:** the manifest's delivery-day set equals my independent union over the 638 CP-16 origins: 2,477 days, which is 2,476 runs plus the structural 2019-01-01. The run is always D−1 00 UTC, and there is no pre-2019 run. The v14/v15.1/v16 timeline holds.<br>**Added runs:** 2023-03-24..31 are not inventoried, use AWS as primary, have 50 validated messages each and bracketed availability. `extended-inventory.csv` shows 8/8.<br>**Messages:** all 123,800 messages are unique. Validity date and time, instant/avg steps, DSWRF bounds (L−3,L)/(L−6,L), levels 10/100, units, parameter codes (consistent per field), operational/forecast/centre kwbc/process 96, quantum = 2^E/10^D, URL patterns (including v16 `atmos/`) and the regular_ll 1440×721 grid all check out, with 0 problems. Endpoints split aws 87,200 / ncar 36,600, and every message is on its manifest primary endpoint.<br>**Dossier exceptions:** 2021-02-02 came from NCAR and 2024-09-15 from AWS.<br>**Disclosures:** the inferred-versus-decoded, reconstructed-availability, 2019 structural missingness, post-sample radiation and known-endpoint-defect disclosures are in `protocol.json` and `report.md`.<br>**Gaps:** they are recorded in `failures.csv`, the evidence `failures.jsonl` and repairs r1–r12. Every run completed and none was imputed. |
| 3 | Exactly H0/HG; frozen conversion and fallback; only weather differs; H0 vs CP-16; component reproduction; admission before outer scoring; no tuning | **PASS** | **Only weather differs:** `augment` appends only 3 columns, and my own local-hour lookup (repeated autumn hours averaged) equals them on 6 origins. With all weather missing, the refit reproduces the cached H0 components to ≤1.42e-14. Truth, scale and level are identical across arms, and so are buffer dates and support.<br>**H0:** `predictions.parquet` H0 is bitwise equal to CP-16 V2-H on all 10,747 keys and every numeric column, and my own replay reproduces it bitwise too.<br>**Component reproduction:** 6 new origins are bitwise equal to the cache (0.0 ≤ atol 1e-8 / rtol 1e-10): a warm-up day, a 23-hour incomplete day, the crisis peak, the last fold-5 day, a fold-2 evaluation day and a fold-4 admission day. Fingerprint equality holds.<br>**Ordering:** 188 warm-up fits, then the admission job, then the freeze commit `30a958a`, then 450 evaluation fits, then comparison. The admission records are unchanged after the freeze.<br>**No tuning:** there is one recipe. The post-freeze changes are controls or formatting only, and the scored files were committed once, at `2dac186`. |
| 4 | §14.8 item 3 causal/state/DST/cache controls plus weather-origin, accumulation, units, packing/clipping, aggregation, missingness; pre-2019 refusal; raw reconstruction | **PASS** | **Own controls on 2021-05-20 and 2025-04-25 (A1/B2):**<br>• A delivery-day and future mask (prices from D, loads after D, random weather after D) and a future-weather-only mutation each changed the components by **exactly 0.0**.<br>• An available D−1 price change moved them by 273.7/225.1 and 254.6/219.1 EUR/MWh.<br>• A non-affine change to target-day (D−1 run) weather moved them by 709.9/650.5 and 25,178/7,041.<br>• Permuting training-history weather moved them by 6.06/8.42 and 18.1/31.5. All three positive controls are above 1e-6.<br><br>**Weather origin:** every feature row comes from run D−1 00 UTC at lead 22–46.<br>**Causal state:** my continuous replay equals the candidate's restart-from-saved-state result bitwise. It confirms the D−2 release, consume-once and 28 complete days, that partial days are never buffered, 23/25-hour identity, and 0 fallback. The inherited cp16 residual tests (D−1 rejection versus D−2 acceptance, restart, sparse-hour, ties) pass.<br>**Cache refusal:** on a private copy, a wrong identity, tampered content and a miss are all refused.<br>**Conversion:**<br>• I decoded 1,035 retained raw messages with my own code, and they are bitwise equal to the stored boxes. My conversion of 495 hours equals the stored features exactly, with equal clip counts.<br>• The wrong recipes would be detected: magnitude of mean u/v is off by 9.40 m/s, no de-averaging by 209.8 W/m², an unweighted mean by 0.17 m/s, and a 3-hour lead shift by 1.72 m/s.<br>• Units and levels are correct. Clipping ≥−3q is clipped, anything below −3q is invalid, and an unknown quantum is invalid. Wrong averaging bounds and extrapolation beyond h46 are refused.<br>**Missingness:** delivery 2019-01-01 is structurally missing (24 NaN rows). A non-imputable class and unfinished extraction are both refused.<br>**Pre-2019:** `prepare` gives "pre-2019 input refused" and A4 `history_start` refuses.<br>**Admission samples:** all 600 are byte-identical to the CP-20 messages. Admission was not rerun. |
| 5 | All eligible keys for both arms; reference metrics; no denominator change; emitted p50 and ordered vectors; §14.3 diagnostics and support; fallback incidence | **PASS** | **Rows:** 75,229 = 7 × 10,747 with identical key sets, and 21,494 contrast rows. Fold counts are 2,160/2,159/2,112/2,160/2,156, fold 3 has 88 dates, and the peak is 408 h / 17 days.<br>**Vectors:** all finite and ordered, and p50 ≠ central in 100% of H0/HG rows.<br>**Recomputation:** all per-fold, pooled, hour, block, peak, recovery and daily metrics, support labels (all eligible, ≥56 dates) and S scores were recomputed independently (≤5.7e-14).<br>**Fallback:** incidence is 0 of 23,184 hour cells, equal to `fallback.csv`.<br>**Failures:** there are no failed issuances. |
| 6 | HG−H0 paired endpoint rule; six §8 diagnostics; effects, uncertainty, labels and distinctions; no promotion | **PASS** | **Bootstrap:** my own run (seed 15042, 2,000 replicates, noncircular 7-day blocks, one shared index set with the same SHA256) gives ΔS_MAE −0.0783115 [−0.1005958, −0.0570309] and ΔS_WIS −0.0838113 [−0.1043827, −0.0655398]. Upper(ΔWIS) < 0 and upper(ΔMAE) ≤ 0, so the rule gives **observed joint improvement**, which equals the candidate.<br>**§8:** H0 is not met on criteria 1 and 2; HG meets all six. Values and limits are equal.<br>**Mixed findings:** the fold-3 daily MAE CI (upper +0.037) is kept as descriptive.<br>**Labels:** the report carries `development_post_selection`, historical CP-15 NOT_DEMONSTRATED, "not authorized" product eligibility, no promotion, no economics, and reconstructed rather than guaranteed availability. |
| 7 | Every §15.5 cap from the first job; all attempts and review; historical debits and monitoring limits; exhaustion semantics | **PASS** (with notes) | **Ledger:** its caps equal §15.5 exactly and every counter is within cap. After this review: machine 144,324.8 s (40.1 of 120 h); policy-days 4,525/9,000; component 1,384/4,000 (main 1,272/3,000); primitive 165,870/480,000 (inner 132,696, final 33,174); analysis and reference passes **3/3 each**; message attempts 8,870/371,400; transfer 136.0/160 GiB. Peaks are 3.72 GiB RSS and 2.35 GiB disk. All 94 jobs ran at BLAS 1 with at most 4 concurrent workers.<br>**Attempts:** every failed job is listed in `failures.csv`. The pre-ledger orientation and unmonitored development tests are disclosed and charged.<br>**Per-message cap:** counting every try that received a response, the maximum is 3 per message. Only by counting network failures with no response do 25 messages reach 4. That exclusion rests on the recorded Owner decision O2, which I cannot verify independently.<br>**Note for item 10:** §15.5 asks for prior-task (CP-16) totals to be reported separately from the CP-20 increments. They are preserved unaltered in `reports/v2-causal/resources.json` and the CP-16 receipt, but the CP-20 packet does not restate them, so the return should carry them. |
| 8 | Protocol, lineage, weather and features, predictions, metrics, diagnostics, uncertainty, criteria, failure/resource logs, rights notices, executable reproduction; invalid outputs and repairs preserved; guards | **PASS** | **Artifacts:** all listed artifacts are present and hash-bound. `rights-notice.md` is present. The decoded grids stay local, bound by `runs.csv` npz SHA256s.<br>**Reproduction:** it is now executable at the clean candidate. `check_protocol` passes, and my component, replay, scoring and conversion reproductions pass through the candidate's identity and fingerprint path.<br>**Preserved:** invalid outputs and repairs (`defects/`, the frozen ×3 control kept as an invariance check, r13, r14, attempt-1 FAIL evidence, superseded markers).<br>**Tests and guards:** `tests/cp20` 86 passed (1 skipped), WX 75 passed, listed guards 70 passed. |
| 9 | One fresh independent Integration-Critic PASS on the exact candidate, clean detached checkout, whole checklist, independent saved-vector metrics/paired uncertainty and representative conversion/component/causal/state reproduction | **PASS** (this review) | I am a fresh reviewer, independent of the Lead and of attempt 1, working in a clean detached checkout of `3e9ff8b`. The whole checklist was mapped. My own scoring and bootstrap, H-layer replay, decode and conversion, component and causal controls reproduce everything within tolerance (mostly bitwise). |
| 10 | Canonical packet; candidate and evidence-tip SHAs; evidence-only delta; reachable history; resources; branch and worktree accounting; stop | **Checkable part PASS; rest OPEN (Lead)** | **Checkable now:** `3e9ff8b` is the tip of `gauntlet/cp-20`, 22 ahead of and 0 behind `main` `88c68cf`. `main` is untouched.<br>**Worktrees:** the main checkout; `.claude/worktrees/cp-20-weather-augmentation-7c081b` (on `gauntlet/cp-20`); `.claude/worktrees/word-rtl-issues-3286df` (detached at `88c68cf`, another session); and this Critic worktree.<br>**Other branches:** `claude/cp-20-weather-augmentation-7c081b` and `claude/word-rtl-issues-3286df`, both at `88c68cf`.<br>**Tags:** no `evidence/cp-20` tag yet.<br>**Open, for the Lead:** the return packet, the evidence-tip SHA, the evidence-only delta (this file plus final resources), the prior-task totals (see item 7) and removal of this worktree. |

## Limits, deviations and resources of this review

- **Isolation** is cooperative (procedural) only. I read attempt 1's committed verdict, which is part of the candidate's evidence, only to confirm what r14 repaired. My findings rest on my own recomputation.
- **Where the scripts were written.** The harness's Write-tool hook refused paths outside my session worktree. I therefore authored the scripts and this verdict in my session scratchpad and copied them with `cp` into the assigned, git-ignored `.local/artifacts/cp-20/critic-2/`. Nothing tracked was touched.
- **Shared-state side effects.** The monitor wrote `critic2-*` markers and locks under `.local/artifacts/cp-20/` and appended jobs 83–93 to the shared ledger. Job 89 exited 1 because of my own bug and left `critic2-attempts.FAILED.superseded-90.json`. It was rerun as job 90.
- **The live ledger differs from the committed snapshot** only by the Lead's jobs 81–82 (`precheck`, `precheck-tests`: 11.4 machine-seconds, run after the candidate commit) and by my jobs. The snapshot is an exact prefix of the live ledger.
- **After this review the analysis and reference passes are exhausted (3/3).** Any further scoring pass would be refused by the §15.5 cap.
- **Charged to the shared §15.5 ledger by this review:**

  | Resource | Used by this review | Allotment |
  |---|---|---|
  | Monitor-charged machine time | 505.8 s (0.14 h), 1 worker | ≤10 h |
  | Analysis passes / reference passes | 1 / 1 | ≤1 / ≤1 |
  | Policy-days | 1,294 (1,276 replay + 18 controls) | ≤1,400 |
  | Non-main component-day attempts | 36 | ≤40 |
  | Primitive fits | 4,310 (3,448 inner, 862 final) | ≤6,000 |
  | Message attempts | 1,035 (listed messages only, each decoded once) | list only |
  | Network transfer | 0 bytes | 0 |

  No cap refused anything.
- **Elapsed:** about 0.5 hours of wall-clock time.
