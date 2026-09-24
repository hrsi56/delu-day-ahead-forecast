# Verdict — CP-20 — Integration — FAIL

- Candidate SHA: `a7943fb6262c1a50b729bd92fe701c8be9428038`
- Plan / version / bar: `capstone_v21.md`, v21-r4 (ratified), SHA256 `150bd53fa15067b1d138c95d0912f86a1e92ce74092059be09034758c1926167`, §15.6 (inheriting the §14.8 verification standard, §§15.1–15.5 and §§14.1–14.4). Read with `docs/track-b/capstone_v21-r3-to-v21-r4-amendments.md` (SHA256 `3e0bdf6a…1ace55`) and `docs/track-b/cp-20-direct-weather-brief.md` (SHA256 `28a4e195…761883e`). All three hashes were verified at the candidate.
- Assignment: `.local/artifacts/cp-20/critic/assignment.md`, SHA256 `e4fb85dc2a31005dbbe6edeb24d87cb9389cb3140c1cb149420dc1b8bd700730` (verified).
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

  (The excerpt is the citation. It appears verbatim at the candidate, in both the checkout and `git show a7943fb:capstone_v21.md`. The courtesy line number is 901.)
- Worktree clean before and after: yes. `/Users/djourno/Downloads/PJM/.local/worktrees/cp-20/critic` was detached at `a7943fb…`, and `git status --porcelain` was empty at the start, after every job and before this file was written. Pytest ran with `-p no:cacheprovider`, `PYTHONDONTWRITEBYTECODE=1` and `--basetemp` under `.local/tmp/cp-20/critic/`. As the assignment instructs, the worktree is left in place for the Lead to remove.

## Commands actually run

All compute ran from the Critic worktree through the monitor, in this form: `$PY scripts/cp20_weather.py --monitor --name critic-<x> --workers 1 --log /Users/djourno/Downloads/PJM/.local/artifacts/cp-20/critic/logs/critic-<x>.log -- <cmd>`. Here `PY=/Users/djourno/Downloads/PJM/.venv/bin/python` and `WX=…/.local/artifacts/cp-20/wx-venv/bin/python`, which has ecCodes 2.49.0 and matches `reports/weather-admission/scripts/requirements.freeze.txt`. The scripts are under `.local/artifacts/cp-20/critic/scripts/` and their outputs under `…/critic/out/`.

| # | Command | Exit | Observed output |
|---|---|---|---|
| 0 | `git status --porcelain`, `git rev-parse HEAD`, `shasum -a 256` on the assignment and on the three issued documents, and a Python verbatim-excerpt search in the checkout and in `git show a7943fb:capstone_v21.md` | 0 | Clean; HEAD `a7943fb…`; all four hashes match; the 35-line excerpt is found verbatim in both. |
| 0b | `git diff --name-status main..HEAD`, `git log`, `git branch -vv`, `git tag --list`, `git merge-base --is-ancestor a7943fb gauntlet/cp-20` | 0 | 168 files, all additions (`A`), none modified or deleted. The only path outside the §15.7 envelope is `scripts/cp20_finalise.py`. The candidate is the tip of `gauntlet/cp-20`, 20 commits ahead of `main` `88c68cf` and 0 behind. |
| 0c | Byte comparison of the live ledger with `docs/track-b/evidence/cp-20/ledger-snapshot-before-review.json` | 0 | Identical (SHA256 `cabf6b6b…a5bcc0`), so there was no unrecorded activity between the candidate and this review. |
| 59 | `critic-static`: `$PY -u critic_static.py` | 0 | 71 checks. Two genuine FAILs: `protocol_frozen_hashes_match_candidate_bytes` and `artifact_manifest_hashes_match_candidate_bytes` (details under item 1). A third, `messages_metadata_all_valid`, was only my own wrong shortName expectation: it flagged `shortName` 74,280 times. ecCodes names these fields `sdswrf`/`10u`/`10v`/`u`/`v` consistently per field, and every other key had 0 problems. All other checks passed (counts, identities, metadata, raw bytes, features, cache, ledger, timeline). |
| 60 | `critic-scoring`: `$PY -u critic_scoring.py`, which reserves 1 analysis pass and 1 reference pass | 0 | 42 metric rows, 980 hour/block/peak/recovery rows, 3,150 daily rows, 42 criteria rows and 12 uncertainty rows are index-equal. Numeric differences are ≤5.7e-14, apart from one column where my own definition was wrong (see 61). The bootstrap index SHA256 `e1df9a68…f99b` equals the lineage value, and the joint rule gives "observed joint improvement". |
| 61 | `critic-levelmae`: `$PY -u critic_levelmae.py`, a follow-up in the same pass (no bootstrap, no new pass) | 0 | I used the day-weighted `daily_mean_level_MAE`, which is the inherited CP-15 definition, in place of my hour-weighted first attempt. 1,022 rows, max diff 7.1e-15. |
| 62 | `critic-replay`: `$PY -u critic_replay.py`, which reserved 1,276 policy-days | 0 | 21,494 evaluation rows are bitwise equal (all 7 quantiles and central). All 70 admission `vector_sha256` values match, as do all 483 predicted origins' hour support and buffer metadata and the final per-fold states. Fallback cells: 0. |
| 63 | `critic-components`: `$PY -u critic_components.py`, which ran 36 non-main attempts, 4,240 primitive fits and 18 policy-days | 0 | The identity fingerprint recomputed from the candidate equals the lineage value. All 8 origins are bitwise equal, with fit logs equal apart from timing. Every control passed (see item 4). |
| 64 | `critic-decode`: `$WX -u critic_decode.py`, with 1,150 × `reserve(message_attempts=1)` | 0 | 1,150/1,150 retained raw messages were decoded once each. The box was located from the decoded geometry (55.25→47.0 °N ×34, 5.5→15.5 °E ×41), and all 1,150 boxes are bitwise equal to the stored boxes. |
| 65 | `critic-convert`: `$PY -u critic_convert.py` | 0 | My own §15.2 conversion over 23 runs and 550 canonical hours differs from `weather-features.parquet` by at most 8.9e-16 (wind10), 1.8e-15 (wind100) and 0.0 (DSWRF). Clipping logs are equal, and there are 0 metadata problems. |
| 66 | `critic-tests`: `$PY -m pytest tests/cp20 -q -p no:cacheprovider --basetemp=…/critic/pytest` | 0 | 86 passed, 1 skipped |
| 67 | `critic-tests-wx`: `$WX -m pytest --noconftest tests/cp20/test_gfs_eccodes.py …test_gfs_locator.py …test_fetcher_watchdog.py …test_attempts.py …test_retry_routing.py …test_concurrent_leads.py -q …` | 0 | 75 passed |
| 68 | `critic-guards`: the listed guards plus the whole `tests/cp16` directory, which I added | 1 | 3 failed and 3 errors, all in unlisted CP-16 production tests. They require `CP16_LEDGER` and the v21-r3 anchor, and that anchor was replaced on the base `main` `88c68cf`, not by CP-20. |
| 69 | `critic-guards-listed`: `$PY -m pytest tests/test_02_rolling_closed_left.py tests/test_05_schema_firewall.py tests/test_08_partition_integrity.py tests/test_12_partition_exclusion.py tests/test_24_live_namespace_is_walled_off.py tests/cp16/test_residuals.py tests/cp16/test_scoring.py -q …` | 0 | 70 passed |
| 70 | `critic-refusals`: `$PY -u critic_refusals.py` (synthetic data only) | 0 | `prepare` on a 2018-12-31 frame gives "pre-2019 input refused". `history_start` floors at 2019-01-01, and A4 gives "pre-2019 history forbidden". A non-imputable missing class is refused. **`check_protocol(Path('.'))` at the clean candidate raises `ValueError: frozen input changed since pre-fit freeze: reports/weather-ablation/prerun-attempts.csv`.** |
| 71–73 | `critic-misc`, `critic-requests`, `critic-requests2` (log reads) | 0 | No message was tried on two endpoints or on an unlisted endpoint. H0 and HG have identical buffer dates and hour support at all 483 predicted origins. The 216,614 requests went to 2 hosts only. The largest ranged body was 4.73 MB. The 17,522 unranged requests are all `.idx` (≤41 KB) or listings (≤135 KB), so no global run file was downloaded. |
| — | `stat`/`git show -s --format=%ct` on the HG cache and commits | 0 | 638 cache files, written 05:02:13Z–05:39:17Z: after the protocol commit (05:01:41Z) and before comparison (05:39:21Z). The 188 warm-up fits finished by 05:12:43Z. The 450 evaluation fits all postdate the admission-freeze commit (05:13:53Z). |

## Evidence actually inspected

- **Governance and contract:** `AGENTS.md`, `engineering-role.md` (Integration Critic protocol), `docs/track-b/gauntlet-templates.md` §2, `capstone_v21.md` §§7–8, 14–15, the amendment, the brief and `docs/track-b/weather-content-intake-2026-09-23.md` (whether it is present).
- **Candidate sources:** `src/cp20/{weather,components,execution,inputs,scoring,controls,controls_supplement,assemble,plan,gfs,budget}.py`, `scripts/cp20_weather.py`, `src/cp15/{models,data,scoring}.py`, `src/cp16/{residuals,inputs}.py` and the test inventory under `tests/cp20/`.
- **CP-20 decision-bearing inputs and outputs:** every file in `reports/weather-ablation/`. That covers `protocol.json`, `lineage.json` (plus the versions at `255ecfb` and `30a958a`), `run-manifest.json`, `messages.parquet` (123,800 rows), `weather-features.parquet` (59,446 rows), `predictions.parquet` (75,229 rows), `metrics.csv`, `diagnostics.csv`, `uncertainty.csv`, `criteria.csv`, `fallback.csv`, `failures.csv`, `missingness.csv`, `radiation-clipping.csv`, `extended-inventory.csv`, `sample-hash-comparison.csv`, `extraction-summary.json`, `extraction-repairs.json`, `post-freeze-repairs.json`, `chain-code-versions.json`, `locator-fix-verification.json`, `causal-controls*.json`, `h0-dryrun.json`, `artifact-manifest.json`, `resources.json`, `rights-notice.md`, `report.md` and `reproduce.md`.
- **Pre-review evidence:** `docs/track-b/evidence/cp-20/` (README, ledger snapshot, `job-code-versions.jsonl`).
- **Inherited inputs:** `reports/v2-causal/{predictions.parquet,input-manifest.json,lineage.json}`, `reports/cp15/predictions.parquet` and the `reports/weather-admission/hashes/*.sha256` lists (853 present files re-hashed).
- **Local evidence (read-only):**
  - `.local/artifacts/cp-20/ledger/budget.json`.
  - All 2,476 `weather/runs/*.json` records, with every `*.npz` re-hashed.
  - 1,150 retained raw messages in `weather/raw/`, all re-hashed and decoded.
  - `weather/attempt-outcomes.jsonl`, `o2-a1-restored-attempts.jsonl` and `requests.jsonl`.
  - All 638 `hg-components/*/*.json`, each digest recomputed.
  - 600 admission samples in `.local/weather-admission/cache/gfs/`, re-hashed.
- **Critic outputs (local; sha256):**
  - `out/static.json` `f36d6f16…7945f`
  - `out/scoring.json` `6697b741…b8b88`
  - `out/levelmae.json` `ed123942…f48`
  - `out/replay.json` `af864423…cefa`
  - `out/components.json` `8f694870…2d3c`
  - `out/decode-summary.json` `40384126…08128`
  - `out/convert.json` `a1822266…37200`
  - `out/refusals.json` `51d5e166…1ace`
  - `out/misc.json` `20845dd1…cfd5`
  - The decoded boxes in `out/decoded/` stay local under the rights notice.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1 | Repository and input state; packaging; frozen manifests before comparison | **FAIL** (identity binding) | **What passes:**<br>• The issued anchor, amendment and brief match their SHA256s.<br>• The admission bundle and intake receipt are present, and the admission bundle's hash lists re-verify (853 files).<br>• The branch only adds files, so prior evidence and other work are untouched.<br>• `protocol.json` was committed at `255ecfb` before any HG fit and is unchanged since. The admission freeze at `30a958a` precedes comparison and scoring.<br><br>**Defect:** `protocol.json` `frozen_inputs_sha256` and `artifact-manifest.json` bind `reports/weather-ablation/prerun-attempts.csv` to `859ba632…d5fb06`. That is the sha256 of the committed text with LF→CRLF. The committed bytes hash to `bef7f523…2c2457` and have not changed since `d4b72d3`. The recorded input identity is therefore not the identity of any committed input. Same root cause as item 8. |
| 2 | Eight-run extension; metadata; source and endpoint; availability; disclosures; gaps | PASS | **Added runs:** the 8 added runs (2023-03-24..31) are marked not-inventoried and use AWS first. Each has 50 validated messages and bracketed availability (`extended-inventory.csv` 8/8).<br>**Message metadata:** there are 123,800 unique messages (2,476 × 10 × 5). All 123,800 match on init and validity time, level and height, instant/avg step, DSWRF (L−3,L)/(L−6,L) bounds, units, parameter, surface, production status, processed type, centre, process 96 and quantum = 2^E/10^D. The regular_ll 1440×721 grid holds in all 2,476 run records.<br>**Sources and endpoints:** URLs follow the endpoint patterns, including v16 `atmos/`. DSWRF precision matches the model version. Messages split aws 87,200 / ncar 36,600, all on the primary endpoint.<br>**Dossier exceptions:** 2021-02-02 came from NCAR and 2024-09-15 from AWS.<br>**Disclosures:** structural 2019-01-01 missingness gives 24 NaN rows. The inferred-versus-decoded, reconstructed-availability and post-sample radiation disclosures appear in the protocol and the report.<br>**Gaps:** they are recorded in `failures.csv` (482 run-failure records, all later completed, none imputed; attempt outcomes) and in repairs r1–r12. |
| 3 | Exactly H0/HG; frozen conversion; only weather differs; H0 vs CP-16; component reproduction; ordering | PASS | **Only weather differs:** `augment` appends only 3 columns to the raw and normalised LEAR designs. My all-weather-missing refits equal the cached H0 components (≤1.14e-13) on 2 origins I chose: 2022-08-20 and 2026-03-29.<br>**H0:** it is bitwise equal to CP-16 V2-H on all 10,747 keys and every numeric column.<br>**Component reproduction:** 8 origins covering all folds, warm-up and evaluation, three spring-DST days and the crisis peak are bitwise equal to the cache. That meets atol 1e-8 / rtol 1e-10. Per-hour fit logs are identical (penalties, coefficient, imputer and scaler hashes), and the identity fingerprint equals `132369…a591`. Warm-up days were refitted on the full data, and that also matched, so later data does not leak.<br>**Ordering:** warm-up fits, then admission, then the freeze commit, then evaluation fits, then comparison.<br>**No tuning:** there is one recipe. The post-freeze change r13 adds controls only. |
| 4 | §14.8 item 3 controls; weather-origin, accumulation, units, packing, aggregation, missingness; pre-2019; raw reconstruction | PASS | **Own controls on 2 new origins (A1/B2):**<br>• A delivery-day and future mask (prices from D on, later loads, later weather) and a future-weather mutation both changed the components by exactly 0.0.<br>• A non-affine target-day (D−1 run) weather change moved them by 78.7/24.4 and 55.6/39.2 EUR/MWh.<br>• An available D−1 price change moved them by 100.8/107.2 and 100.8/98.9.<br>• All weather missing gave H0.<br><br>**Weather origin:** run = D−1 00 UTC and lead = 22–46 for every feature row.<br>**Causal state:** the independent continuous replay (≤D−2 release, consume-once, complete-day rule, 23/25-hour DST days) matches bitwise the committed run, which was restarted from saved state at the admission boundary.<br>**Cache:** identity and digests hold for all 638 entries.<br>**Conversion, from my own decode of the 1,150 retained raw messages (v14, v15.1 and v16; spring and autumn DST):**<br>• Features match to ≤1.8e-15.<br>• Accumulation: skipping de-averaging would move the result by up to 210 W/m², so an error of that kind would be detected.<br>• Aggregation: magnitude-of-mean differs by up to 9.4 m/s, and an unweighted mean differs as well.<br>• Clipping logs match. Units and bounds are correct on all messages.<br>• The admission's 600 retained samples are byte-identical by sha256.<br><br>**Pre-2019 refusal:** verified on synthetic data. |
| 5 | All keys for both arms; reference metrics; emitted vectors; §14.3 diagnostics; support and fallback | PASS | **Rows:** 75,229 rows, 7 policies × 10,747 keys with identical key sets. Fold counts are 2,160/2,159/2,112/2,160/2,156, fold 3 has 88 dates, and the peak is 408 h / 17 days. 21,494 contrast rows.<br>**Vectors:** all values are finite and ordered, and p50 differs from central in 100% of rows. The saved references are bitwise equal to CP-15.<br>**Recomputation:** my own metrics and diagnostics (per fold, pooled, 24 hours, 3 blocks, peak, recovery, daily) and the S scores match to ≤7.1e-14.<br>**Support and fallback:** support labels are equal (0 support-limited). Fallback incidence is 0, confirmed by my replay.<br>**Failures:** there were no failed issuances. |
| 6 | HG−H0 paired rule; six §8 diagnostics; labels and distinctions | PASS | **Bootstrap:** my own run (seed 15042, 2,000 replicates, 7-day noncircular blocks, one shared index set, same index SHA256) gives ΔS_MAE −0.0783115 [−0.1005958, −0.0570309] and ΔS_WIS −0.0838113 [−0.1043827, −0.0655398]. These equal `uncertainty.csv` to ≤7.1e-15, and the rule gives "observed joint improvement".<br>**§8:** H0 is not met on criteria 1 and 2. HG meets all six, and the values and limits match `criteria.csv`.<br>**Mixed findings:** the fold 3 MAE daily CI, whose upper bound is +0.037, is kept as a descriptive result.<br>**Labels:** the report is labelled `development_post_selection` and says no promotion, no product eligibility, no economics and reconstructed (not guaranteed) availability. |
| 7 | Every §15.5 cap from the first job; attempts; review; debits and monitoring limits | PASS (with Owner-dependent note) | **Ledger:** its caps equal §15.5, and every counter is within cap. After this review: machine 143,779.5 s (39.9 of 120 h); policy-days 3,231/9,000; component 1,348/4,000 (main 1,272/3,000); primitive 161,560/480,000; analysis and reference passes 2/3 each; message attempts 7,835/371,400; transfer 136.0/160 GiB. Peaks are 3.72 GiB RSS and 2.18 GiB disk. All jobs ran with BLAS 1 and ≤4 workers.<br>**Accounting:** the main solver calls in the cache logs (152,520) plus 40 control attempts (4,800) equal the ledger's 157,320 exactly. The pre-ledger orientation and unmonitored development tests are disclosed and charged.<br>**Owner note:** compliance with the 3-per-message cap rests on the recorded Owner decisions O1, O2 and O2-A1. Under them the maximum effective counted attempt per message is 1. Counting every try of any outcome, 25 messages had 4 tries. The Critic cannot independently verify the Owner instructions. The cap totals were not changed. |
| 8 | Protocol, lineage, weather, predictions, metrics, uncertainty, criteria, logs, rights, **executable reproduction**; repairs; guards | **FAIL** | **What passes:**<br>• Every listed artifact is present.<br>• `rights-notice.md` is present.<br>• Invalid outputs and repairs are preserved (`defects/`, the frozen ×3 control kept as an invariance check, r13, `post-freeze-repairs.json`).<br>• The listed guards pass (70), as do `tests/cp20` (86+1 skipped) and the WX tests (75).<br><br>**Defect:** `reproduce.md` §4 is not executable at the candidate. `hg-warmup`, `admission`, `hg-evaluation`, `comparison`, `controls` and `controls-supplement` all call `check_protocol`. In a clean checkout of `a7943fb` that raises `frozen input changed since pre-fit freeze: reports/weather-ablation/prerun-attempts.csv` (run 70).<br><br>**Also:**<br>• `scripts/cp20_finalise.py` is outside the §15.7 path envelope, which lists only `scripts/cp20_weather.py` (the brief says "Write only §15.7's paths"). It is disclosed as the finaliser but not as an exception to the path envelope.<br>• Minor: the WX test list in `reproduce.md` names 2 files, but the final run used 6. `resources.json` predates jobs 56–58, and the README says final resources follow in the evidence delta. |
| 9 | One fresh independent Integration-Critic PASS on the exact candidate | **FAIL** (this review is not a PASS) | The review used a clean detached checkout of `a7943fb`, independently recomputed saved-vector metrics and paired uncertainty, and reproduced conversion, components, causal behaviour and state. Every scientific recomputation matched. The verdict is FAIL because of items 1 and 8. |
| 10 | Canonical packet, both SHAs, evidence-only delta, reachable history, resources, accounting | OPEN (Lead, after verdict) | **Checkable now:** `a7943fb` is the `gauntlet/cp-20` tip, 20 commits ahead of `main` `88c68cf`, and `main` is untouched by this branch.<br>**Worktrees:** the main checkout, `.claude/worktrees/cp-20-weather-augmentation-7c081b` (on `gauntlet/cp-20`), `.claude/worktrees/word-rtl-issues-3286df` (detached at `88c68cf`, another session) and this Critic worktree.<br>**Other branches:** `claude/cp-20-weather-augmentation-7c081b` and `claude/word-rtl-issues-3286df`, both at `88c68cf`.<br>**Tags:** there is no `evidence/cp-20` tag yet.<br>**Remaining:** the return packet, the evidence-tip SHA and the evidence-only delta. |

## On FAIL only
- **Single largest meaningful gap:** The committed pre-fit `protocol.json` and `artifact-manifest.json` bind `reports/weather-ablation/prerun-attempts.csv` to the hash of an uncommitted CRLF variant (`859ba632…`, where the committed bytes are `bef7f523…`). As a result, `cp20.execution.check_protocol` refuses in a clean checkout of `a7943fb`, and every research job in `reproduce.md` §4 stops at its first step. The candidate's executable reproduction and its recorded input identity are therefore not valid as committed, even though every scientific result reproduced independently.
- **Exact next acceptance test:** Run this in a fresh clean detached checkout of the repaired candidate:

  `PYTHONPATH=src $PY -c "from pathlib import Path; from cp20.execution import check_protocol; check_protocol(Path('.'))"`

  It must exit 0, and the sha256 of every committed file named in `protocol.json` (implementation, frozen inputs, issued/inherited) and in `artifact-manifest.json` must equal its recorded value. `protocol.json`, `predictions.parquet`, `metrics.csv` and `uncertainty.csv` must stay byte-identical to `a7943fb`. No tracked path may remain outside the §15.7 envelope, so `scripts/cp20_finalise.py` must be moved inside it or expressly authorised.

## Limits and resources of this review
- **Isolation:** it is cooperative only. For diagnosis I looked at the git metadata, size and hash of `prerun-attempts.csv` in the Lead's checkout: it is CRLF, 22,335 bytes, and `core.autocrlf=input` masks it from `git status`. That was not decision-bearing. The finding stands on the candidate alone, because sha256 of the committed text with LF→CRLF equals the frozen hash.
- **Where the monitor writes:** the mandated monitor also wrote its `critic-*` markers and locks under `.local/artifacts/cp-20/{markers,locks}` and appended jobs 59–73 to the shared ledger. Job 68 left a `critic-guards.FAILED.json` marker; the cause is explained in row 68.
- **Charged to the shared §15.5 ledger:**

  | Resource | Used by this review |
  |---|---|
  | Monitor-charged machine time | 499.1 s (0.139 h), 1 worker |
  | Analysis passes | 1 |
  | Reference passes | 1 |
  | Policy-days | 1,294 |
  | Non-main component-day attempts | 36 |
  | Primitive fits | 4,240 (3,392 inner, 848 final) |
  | Message attempts | 1,150 (own decodes of retained raw messages, each once) |
  | Transfer | 0 bytes |

  No cap refused anything.
