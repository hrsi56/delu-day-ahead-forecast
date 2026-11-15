# Verdict — CP-29 — Integration — PASS

- Candidate SHA: a04f34078b2d11b658cb975293b2f5f12d074caa
- Plan / version / bar: `capstone_v21.md`, v21-r20 (SHA-256 `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`), §16.4 "Delivery and acceptance obligations for future briefs" (section 19 lines, 1777 bytes, SHA-256 `502c1a588c9fe88e557084cff3fe1c44871c8e0c8fbe42a2284650d3a98a73ab`); with the issued brief `docs/track-b/evidence/cp-29/issued-brief.md` (SHA-256 `c3a5a8919631293916a0a457ca93542e0544a400a8bc9019596fb00313e3a1b0`), its "Observable outcome" and "Complete authoritative checkpoint bar", which quotes the approved contract `docs/track-b/economic-policy-contract-2026-11-15.md` (SHA-256 `21a9208573668becd2af3d9e476855e3f8c0e66c85fc9097194bd6deae580889`, decision 32) §§1–11, §16.3, programme §4.E, PUBLISH_RULES 1.5 §5.1a and §24.14's "What stays exactly as registered".
- Verbatim bar excerpt:

> ### 16.4 Delivery and acceptance obligations for future briefs
>
> | Stage | Required addition to the full future checkpoint bar |
> |---|---|
> | Before fresh-data test | Replay the intended daily refit/update and issuance contract; freeze scoring and any evaluated economic policy before outcome access; retain the protected test boundary |
> | CP-17 | Owner's final-version designation, prerequisites/disposition, policy/initialization and registry identities, daily fit and failure rules, metric formulas, resource and calendar plan |
> | CP-18 | Actual scheduled training/issuance and outcome reconciliation, one product/demo identity, complete documentation/results/business sections, daily public panel and independent public acceptance |
> | CP-19 | At least 90 consecutive delivery days after final freeze under §9; count real timely forecasts and failures, verify registry lineage, evaluate without tuning or excluding bad days |
>
> Live observations and the matching demo may be published at authorized CP-18 with the label
> “prospective evaluation in progress”; do not wait for CP-19 to show operation, and do not claim
> completed validation before it. Public acceptance checks actual hosted output and daily records;
> local fixtures do not establish daily operation. Include positive controls for altered identities,
> future-label leakage, stale/failed fits, missing/zero/negative prices and partial/DST days, plus
> reproducible percentage, interval and authorized business-series derivations. The full existing
> independent, browser, accessibility and publication contract still applies.
>
> No checkpoint starts here. The numeric future briefs and approved budgets remain necessary;
> this amendment resolves the required product outcome, not experimental results or implementation.

  (The excerpt is the citation. Any line number is a courtesy and is non-binding.)
- Worktree clean before and after: yes. `/Users/djourno/Downloads/PJM/.local/worktrees/cp-29/critic-1`, detached at
  `a04f34078b2d11b658cb975293b2f5f12d074caa`; `git status --porcelain` empty before the review, after the full
  re-derivation, and again before this verdict was written; `HEAD` unchanged. The only byproduct is the gitignored
  `.venv/` that `uv run` created inside the worktree.
- Isolation: cooperative and procedural, not enforced by a sandbox. I worked from the critic worktree and my own
  scratchpad. I did not open the Lead's or a Builder's checkout, uncommitted diffs, the Lead's ledger, or any
  conversation history. The one command run from the Lead's worktree as working directory was the instructed
  `git show main:scripts/gauntlet.py | python3 -I - critic-brief cp-29`, which reads `main` through Git. I did not open
  the Claude memory directory. I made no Git write.

## Commands actually run

All commands below ran in `/Users/djourno/Downloads/PJM/.local/worktrees/cp-29/critic-1` with
`MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1` exported, unless another location is stated.

| # | Command | Exit | Observed output |
|---|---|---|---|
| 1 | `git show main:scripts/gauntlet.py \| python3 -I - critic-brief cp-29` (from the Lead's worktree, read-only) | 0 | the generated Critic brief: candidate `a04f3407…`, worktree `critic-1`, plan identity and the §16.4 excerpt above |
| 2 | `git -C …/critic-1 status --porcelain`; `git rev-parse HEAD` | 0 | empty; `a04f34078b2d11b658cb975293b2f5f12d074caa` |
| 3 | `shasum -a 256` of the issued brief, the contract and `capstone_v21.md` | 0 | `c3a5a891…b0`, `21a92085…889`, `80341681…6e6`, each equal to the brief's pins |
| 4 | `shasum -a 256` of every execution input (the brief's table) and `parity.json` | 0 | every value equal to the brief's pins: `f5cb02a1…f638`, `f092140e…3ce8`, `7e9c972f…b85d`, `9d3f539f…5cf9`, `7dd2dc73…7f00`, `4e234cda…ea52`, `83468823…16cb6`, `415e2e7c…c198b`, `5d2aecc3…5a94`; `parity.json` `090c3cb4…dbc5` |
| 5 | `uv run python -m cp29.evaluate --check` | 0 | `{"identical_to_committed": {"paired.csv": true, "summary.csv": true}}` (uv created `.venv`, CPython 3.13.15, 117 packages; scipy 1.18.1) |
| 6 | `uv run python -m cp29.report --check` | 0 | `{"identical_to_committed": true}` |
| 7 | `uv run pytest -q tests/cp29 tests/test_29_research_evidence.py tests/test_30_research_claims_rendered.py tests/test_34_mlflow_export.py` | 0 | `659 passed, 1 skipped in 59.93s` (HiGHS printed `HighsMipSolverData::transformNewIntegerFeasibleSolution tmpSolver.run();` lines; no failure) |
| 8 | `make lint-publication` | 0 | `page: 0 finding(s)`, `readme: 0 finding(s)`, `templates: 0 finding(s)`, `PASS` |
| 9 | `uv run python -m cp29.evaluate` (the full re-derivation, one process), then `git status --porcelain` | 0; 0 | 2026-11-15T21:45:51Z to 21:54:47Z (8 min 56 s): `{"wrote": ["checks.json", "daily.csv", "paired.csv", "report.md", "summary.csv"], "rows": 26964}`; status empty, so every committed record reproduced byte for byte |
| 10 | `git log`/`git show --stat` of `eab32284..HEAD`, `git diff --name-status eab32284 HEAD`, and the diffs of every modified file | 0 | listed under "Evidence actually inspected" |
| 11 | pyarrow metadata reads (no rows) of the snapshot, CP-28's forecasts and CP-24's predictions | 0 | snapshot: 67,343 rows, delivery dates 2019-01-01 to 2026-09-06; hourly.parquet days to 2026-09-06; predictions to 2026-04-07 |
| 12 | Critic's independent script `scratchpad/indep/summaries.py` (no project import): re-derives `summary.csv` and `paired.csv` from the committed `daily.csv`, with my own bootstrap | 0 | 120 of 120 summary rows match, largest relative difference 2.2e-16; 12 of 12 paired rows, largest absolute difference 9.1e-13 EUR |
| 13 | Critic's independent script `scratchpad/indep/recompute.py` (no project import; the snapshot read with a row filter at 2026-09-06; my own joins, my own naive, my own MIP in a different formulation; 4 workers, 96 s) | 0 | populations, joins, parity and optimum values reproduced (details below) |
| 14 | `scratchpad/indep/recompute2.py`: the same plus a linear polish stage with the hours' directions fixed (4 workers, 111 s) | 0 | 26,963 of 26,964 rows reproduce the committed realized profit within €0.001 and every row's energies within 1e-7 MWh |
| 15 | Critic's probes, in memory, through `cp29.evaluate.daily_rows` and `cp29.battery` | 0 | a NaN cleared price marks every source missing, not traded, profit 0; settlement at zero and negative prices equals the hand formula; a 24-hour day with one snapshot row absent is solved over 23 hours and traded (Observation 1) |
| 16 | `git grep` for the earlier blob and SHA-256 (full and 8-character forms) of each modified tracked file | 0 | no committed file cites any of them except the CP-29 packet itself |
| 17 | `.venv/bin/python -I -c` counting `delu_forecast.research.records()` keys starting `cp29.` and running `validate_all` on them | 0 | `2076 0`: 2,076 records, no validation problem |
| 18 | `git show main:scripts/bar.py \| python3 -I - check /Users/djourno/Downloads/PJM/.local/artifacts/cp-29/critic-1/integration.md --source capstone_v21.md@a04f34078b2d11b658cb975293b2f5f12d074caa` | 0 | `ok: lines 7–25 (1776 bytes) appear in capstone_v21.md@a04f34078b2d` |
| 19 | `git status --porcelain`; `git rev-parse HEAD`, before writing this verdict | 0 | empty; `a04f34078b2d11b658cb975293b2f5f12d074caa` |

## Evidence actually inspected

- **The governing texts:** `AGENTS.md`; the issued brief, in full; the contract's sections as the brief quotes them;
  PRES-6's packet §0 (populations, regimes, bootstrap settings).
- **The packet** `docs/track-b/evidence/cp-29/publication-packet.md`, in full, and its history: §0 as committed in
  `212a39cc` (2026-11-15 16:30:15 UTC), the correction in `774238d2` (16:33:24 UTC, nine added lines, §0 otherwise
  unchanged), and the post-result sections added in `7b7727ef` and `a04f3407`. §0 is unchanged after `774238d2`.
- **The commit order:** `7a457726` brief; `212a39cc` §0 and the code, no `reports/cp29`; `774238d2` correction, no
  records; `2e9242c9` (16:43:31 UTC) the first commit holding any profit (`reports/cp29/*`), plus `report.py`,
  `test_evaluation.py` and the v5-on-P-all summary exclusion; `7b7727ef` the claim layer and manifest; `d36cbc90` the
  report's wording; `a20b2bb7` two positive-control tests; `a04f3407` packet §3. `battery.py` and `inputs.py` are
  unchanged after `774238d2`; `evaluate.py` gained only the v5 exclusion and the `--summaries` option.
- **The code:** `src/cp29/battery.py`, `inputs.py`, `evaluate.py`, `report.py` (read in full);
  `delu_forecast.baselines.similar_day_naive`, `features._calendar_day_lag`, `final_candidate._block_means`,
  `cp25.guard`, `cp17.dailyfit.array_hash`; `src/cp26/harness.py` (`LANDED_CODE`, `PINS`); `tests/pres5_landed_code.py`.
- **The tests:** `tests/cp29/test_battery.py`, `test_evaluation.py`, `test_claims.py` (read in full); the diff of
  `tests/test_29_research_evidence.py`; `tests/test_30`'s claim-map coverage.
- **The records:** `reports/cp29/report.md` (read in full), `paired.csv` (all rows), `summary.csv`, `checks.json`
  (all keys; the brute-force rows), `daily.csv` (all 26,964 rows, by script).
- **The claim layer:** the diffs of `research.py`, `research_claims.py`, `registry.py`, `manifest.json`;
  `docs/track-b/research-content/cp29-claims.md` in full.
- **Inputs:** `parity.json` (the B0 checks) and the five `reports/cp18b/dryrun/store/issued/*/record.json` B0 shadows
  (days 2026-08-31 to 2026-09-05).

## Independent recomputation (the critic's own code)

- **Populations:** P-all, from CP-28's A1 days 2020-12-29 to 2026-09-06: 2,068. P-v5, v5's folds 2–5 ∩ P-all: 358.
  The fold ranges are exactly the contract's (2021-04-01–2021-06-29, 2022-07-01–2022-09-28 with 88 days,
  2025-05-01–2025-07-29, 2026-01-08–2026-04-07); no fold 2–5 day lies outside P-all. The 10 calendar days outside
  P-all include the autumn change days 2023-10-29 and 2024-10-27.
- **The day's hours:** 2,059 days × 24, six × 23 (exactly the six spring change days), three × 25 (exactly the autumn
  change days in P-all); no NaN price on P-all; every snapshot `delivery_date` equals the Berlin date of its hour.
- **The joins:** v6, 49,596 A1 rows on P-all, none with `scoring_key` false, every `day` equal to its Berlin date. The
  sources' missing days: v6 33, naive 11, v5 4, perfect foresight 0, equal to the committed flags row for row.
- **The naive, my own implementation** (same Berlin wall-clock hour on D−1 for Tuesday to Friday, D−7 otherwise; a
  wall-clock time that occurs twice or never gives no value): bit for bit equal to CP-26's B0 central vector on all
  8 parity records (4 days, 2 paths), and its SHA-256 equal to the frozen package's B0 shadow on all 5 dry-run days.
- **The optimum:** a mixed-integer programme in a different formulation (cumulative state-of-charge rows, no SOC
  variables), solved for every one of the 26,964 rows. The committed schedule's forecast value lies between my
  optimum − €6.02e-5 and my optimum, on every row. Perfect foresight's committed profit equals my optimum within
  €1.0e-6 on every row, so every denominator of "share of perfect foresight" is reproduced.
- **The realized profit:** with a linear polish stage like §0's, my schedules reproduce the committed realized profit
  within €0.001 on 26,963 of 26,964 rows, and the energies within 1e-7 MWh on all rows. Every source's total at every
  wear agrees within €0.0004, except v6's risk-aware variant at €0 (€3.23, one near-tie row; Observation 2).
- **Row identities:** for every traded row, MWh discharged from the battery = MWh sold / √0.85 (6.7e-16) and MWh bought
  × √0.85 = MWh sold / √0.85 (empty at the end, 1.7e-14); at most 2.0000000000000004 MWh discharged from the battery,
  2/√0.85 bought and 2·√0.85 sold a day; "traded" iff energy > 0; untraded rows have expected and realized profit 0;
  traded rows have expected profit > €1e-6 (minimum €0.073). No source beats perfect foresight on a day by more than
  €1.0e-6.
- **The summaries and pairs:** re-derived from the committed `daily.csv` with my own code: all 120 summary rows and
  17 measures, and all 12 paired rows with my own non-circular moving-block bootstrap (14-day blocks, 2,000
  replicates, seed 20261115, drawn in the order wear €25, €0, €50, then the four pairs) reproduce the committed
  values to floating-point precision.
- **Brute force** (`checks.json`): 184 programmes = 42 sampled days × 4 (v6 two rules, the naive, perfect foresight)
  + 8 P-v5 days × 2 (v5); the solver is never beaten; the largest solver margin is €4.31.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1.1 | Outcome 1, the rules fixed before any number: §0 committed before the first profit | PASS | `212a39cc` holds §0 and the code and no record; the first profit is committed in `2e9242c9`, 13 minutes later. §0 fixes the solver (milp + linprog, HiGHS, scipy 1.18.1), tolerances, the deterministic tie-break, the programme, the 23/25-hour days, the missing-hour rule, the seed 20261115 and the joins. The one change to §0 (`774238d2`) answered a solver infeasibility, not a result, and is dated before any record. `tests/cp29` tests the tie-break and determinism |
| 1.2 | Outcome 2, the checks before the results | PASS | `evaluate.main` runs `checks` first and writes nothing on failure. Parity 8/8 with CP-26's B0 and 5/5 with the frozen package (both reproduced independently); P-all 2,068 and P-v5 358 (reproduced); brute force on 184 programmes, never beaten; perfect foresight's minimum €0.00; every schedule checked by `battery.violations`; 0 tie-break fallbacks |
| 1.3 | Outcome 3, the results exactly the contract's (§§3, 4, 6) on P-all and P-v5, and nothing else computed | PASS | `daily.csv` holds exactly {v6 median/risk, naive median, v5 median/risk on P-v5 only, perfect foresight} × wear {25, 0, 50}: (2,068 × 4 + 358 × 2) × 3 = 26,964 rows. Summary: 120 rows (P-all, P-v5 × all and three regimes × three wears); paired: the four contract pairs × three wears. No other battery, rule, threshold or variant appears in the code or records. All reproduced independently |
| 1.4 | Outcome 4, the records and `--check` | PASS | `--check` exit 0, both files `true`; the full re-derivation reproduces `daily.csv`, `summary.csv`, `paired.csv` and `checks.json` byte for byte; every row is labelled "simulated, development, post-selection" |
| 1.5 | Outcome 5, the report | PASS | `report.md` is built from the records (`cp29.report --check` true). It states the method, the checks, the results with their intervals, the wear sensitivity, the regimes with counts, contract §8's disclosures and §9's "what it does not claim", and no annualized return, IRR, payback or success rate. Its numbers match my independent re-derivation |
| 1.6 | Outcome 6, the registry entries for PRES-7 with `evidence/cp-29`, and no page or README change | PASS | `research.py`: three CP-29 sources whose blobs equal the committed files, and `cp29.*` records; `research_claims.py`: C1101–C1108 on the `PRES7` surface only, W56/W57; `registry.py`: `evidence/cp-29`; `cp29-claims.md`; the manifest gains only the three CP-29 entries, with the right blobs. `docs/index.html` and `README.md` are unchanged; `tests/cp29/test_claims.py` passes, including the no-render test |
| 2.1 | Contract §2, the limits, and O58's one direction an hour | PASS | 1 MW at the grid each way (bounds on c, d); 2 MWh at the terminals (0 ≤ s ≤ 2); √0.85 each way; empty at the start and the end; Σ d/√0.85 ≤ 2; binary z with c ≤ z, d ≤ 1 − z. Verified in the code, in a different formulation, and on every committed row |
| 2.2 | Contract §2, the costs, and O58's wear base | PASS | wear €25/MWh (sensitivity €0, €50) on energy leaving the terminals (= sold / √0.85); fee €0.10 on MWh bought and sold at the grid; no grid fees. In the objective and in the settlement alike |
| 2.3 | Contract §3, the median rule | PASS | buy = sell = q50 (v5: p50); the value-maximizing schedule under §2's limits |
| 2.4 | Contract §3, the risk-aware variant | PASS | buy = q75, sell = q25 (v5: p75/p25), for v6 and v5 only; none for the naive or perfect foresight |
| 2.5 | Contract §3, step 3 (not above zero, do nothing) | PASS | best value ≤ €1e-6 → no trade (fixed in §0); every traded committed row has expected profit > €1e-6 and every untraded row 0 |
| 2.6 | Contract §3, the settlement | PASS | Σ price·(d − c) − wear·Σ d/√0.85 − 0.10·Σ(c + d) at the snapshot's cleared prices; perfect foresight's realized = expected within 4.5e-13; my probe's settlement at zero and negative prices equals the hand formula |
| 2.7 | Contract §3 and §0, the deterministic tie-break | PASS | value, then least energy, then earliest, as fixed in §0 and corrected before any record; same inputs give the same rows (the full re-derivation is byte-identical); 0 fallbacks. See Observation 2 on near-ties |
| 2.8 | Contract §4, the benchmarks | PASS | v6 = CP-28 arm A1 q25/q50/q75; the naive by its frozen rule from the committed snapshot, its central vector parity-checked; v5 = CP-24 policy v5 p25/p50/p75 on P-v5 only (the v5-on-P-all summaries are absent; a test refuses them); perfect foresight = the cleared prices, with the identical battery, costs and rule. "Doing nothing" is not shown as a reference row (Observation 4) |
| 2.9 | Contract §5, the populations and the regimes | PASS | P-all 2,068 and P-v5 358, reproduced; regimes 246 / 481 / 1,341 days, reproduced; development data only |
| 2.10 | Contract §5, the missing-hour rule | PASS | a day with any missing forecast or price hour is not traded, profit 0, kept and counted: v6 33, naive 11, v5 4 days, reproduced row for row; my NaN-price probe confirms the price branch. See Observation 1 on an absent snapshot row, which does not occur in the pinned inputs |
| 2.11 | Contract §6, the measures | PASS | cumulative net profit, the complete daily series (`daily.csv`) with units and the battery's size in the report; share of perfect foresight on sums over the same days ("undefined" on a zero denominator; none occurs); mean, median, 5th and 95th percentiles; losing days, their share, the largest loss; maximum drawdown; trading days and energy. All 120 × 17 values reproduced independently |
| 2.12 | Contract §6, the paired bootstrap | PASS | v6 − naive (P-all, P-v5) and v6 − v5 (P-v5, both rules), non-circular moving blocks of 14 days, 2,000 replicates, seed 20261115 fixed in §0 before computing, percentile 95% interval; reproduced exactly with my own implementation |
| 2.13 | Contract §6, "Not reported" | PASS | no annualized return, IRR, payback, business case or success rate in the report, the records or the claims; W56 and W57 guard them on every surface |
| 3.1 | §16.4: the economic policy frozen before outcome access | PASS | the contract is committed (`f118f2bb`) before the brief and before any number, pinned by SHA-256 in `cp29.inputs.PINNED` and checked before any input is read; it is not changed on the branch |
| 3.2 | §16.4: positive control, altered identities | PASS | `test_positive_control_an_altered_input_identity_is_refused`; `check_pins` runs first in `load_days` |
| 3.3 | §16.4: positive control, future-label leakage | PASS | `test_positive_control_a_row_after_the_development_boundary_is_refused` (a 2026-09-07 row is refused, the snapshot is cut at the boundary); `cp25.guard.admit_rows` runs on the prices, v6 and v5 |
| 3.4 | §16.4: positive controls, missing/zero/negative prices | PASS | missing forecast hour: `test_a_missing_hour_is_never_planned…`; missing price: the critic's probe (no committed test, Observation 1); zero prices: the hand-computed day (free energy); negative prices: `test_every_limit_holds_on_random_and_negative_price_days` |
| 3.5 | §16.4: positive controls, partial/DST days | PASS | 23-, 24- and 25-hour days: `test_daylight_saving_days_solve_over_their_own_hours`; the real P-all DST days verified independently. Partial days through a missing hour: covered; an absent snapshot row: not caught, but none exists in the pinned inputs (Observation 1) |
| 3.6 | §16.4: reproducible business-series derivations | PASS | `--check` (summaries and report), the byte-identical full re-derivation, and the critic's independent re-derivation of the rows, summaries and intervals |
| 4.1 | The red line: development data only, delivery days through 2026-09-06 | PASS | the pinned snapshot's metadata ends at 2026-09-06 (no later market row exists in any input); the code also cuts the snapshot at the boundary and guards every row; the latest day in every record is 2026-09-06; the code reads no 4.7T, live or later file |
| 4.2 | No fit: every forecast a committed, stored one | PASS | v6 from `reports/cp28/forecast/hourly.parquet` (committed `35e841b8`, 2026-10-25), v5 from `reports/ddnn2/attempt-1/predictions.parquet` (`05e60159`, 2026-10-11), both hash-pinned; the naive is a fixed rule on the committed snapshot; no estimator is called |
| 4.3 | Nothing frozen changed | PASS | `git diff eab32284 HEAD` touches no anchor, governance file, PUBLISH_RULES, the contract, `uv.lock`, `pyproject.toml`, `src/cp17`, `src/cp18`, frozen record or landed-code path (`src/cp29` is outside `LANDED_CODE`) |
| 4.4 | 4.7T untouched | PASS | no 4.7T path changed or read; the contract adds no term to 4.7T; nothing after 2026-09-06 is read |
| 5.1 | The allowed paths only | PASS | 21 files: `src/cp29/` (5), `tests/cp29/` (3), `reports/cp29/` (5), `docs/track-b/evidence/cp-29/` (2), `registry.py`, `research_claims.py`, `tests/test_29_research_evidence.py` (the claim layer's own test, a CP-29 branch only), O57's `research.py` and `cp29-claims.md`, O59's `manifest.json` |
| 5.2 | No earlier evidence binds a changed file | PASS | no committed file cites the earlier blob or SHA-256 of `research.py`, `research_claims.py`, `registry.py`, `tests/test_29` or `manifest.json` (full and 8-character searches; only the CP-29 packet names them). `tests/pres5_landed_code.py` compares PRES-5's recorded copies, not the working tree; `PINS` holds governance files only |
| 5.3 | Existing claim-layer entries unchanged in meaning | PASS | every change is additive: new sources, records, units ("EUR", "MWh", the CP-29 difference unit, used by CP-29 only), CP-29 branches in `_expected_unit`/`_expected_aggregation`, blocks on the new `PRES7` surface, W56/W57, one claim map. `tests/test_29`, `test_30`, `test_34` pass, and W56/W57 find nothing on the page or the README |
| 5.4 | Nothing under `src/cp18/`, `live/`, `space-product/`, `.github/` | PASS | `git diff --stat eab32284 HEAD` over those paths is empty |
| 6.1 | Packet honesty: the first run's stop | PASS | the correction is dated 16:33 UTC, matches `774238d2`'s time and comes before the first record (`2e9242c9`, 16:43 UTC). The described cause (tie-break slacks below HiGHS's MIP tolerance) matches the code change; the fallback is counted (0 used). That the first run printed or kept no profit is consistent with the code (rows are held in memory and nothing is printed) but cannot be verified after the fact |
| 6.2 | Packet honesty: the v5-under-P-all defect | PASS | the exclusion is in the same commit as the first committed summaries, so it precedes every committed number it governs. The fix is required by contract §4, changes no daily row and no other summary, and `test_v5_is_reported_on_p_v5_only…` refuses the mixing. The disclosure sits in the post-result section, as it should |
| 6.3 | Packet honesty: the other statements | PASS with observations | §1–§3's figures match the records and my runs (26,964 rows; 2,076 `cp29.*` records, all valid; parity 8/8 and 5/5; 184 brute-force programmes; 0 fallbacks; manifest +12 lines with the right blobs). I did not rerun the full default suite (3,469 passed) or the 676-test group that includes `tests/test_32`; my narrower run of the brief's command passed (659 passed, 1 skipped). Minor wording points are Observations 2, 3 and 6 |

## Observations (non-blocking; none changes a committed number beyond what is stated)

1. **An absent snapshot hour is not treated as missing.** `inputs.load_days` takes a day's hours from the snapshot's
   rows, and `daily_rows` flags only NaN values. The critic's probe: a 24-hour day with one row removed is solved
   over 23 hours and traded, where contract §5 says it should not be traded. **This cannot occur in this evaluation:**
   every P-all day holds exactly its calendar's hours, and the inputs are hash-pinned. No committed test covers a
   missing cleared price (the critic's probe shows that branch works). Worth closing before the contract is applied to
   live records (contract §7), where partial days happen.
2. **Near-ties and the integer stage's slack.** After the correction, the integer stage treats values within €1e-4 as
   equal optima and fixes every hour's direction, including idle hours, whose binaries are arbitrary. The final
   schedule's forecast value is therefore up to €6.02e-5 below the optimum (observed maximum). In one row
   (2025-07-29, v6 risk-aware, wear €0), it charges 0.169 MWh at hour 12 (forecast 66.8404) rather than hour 15
   (66.8400): €5.9e-5 less forecast value, €3.23 less realized profit, the "earliest" choice under §0's corrected rule.
   The only visible effect is one sensitivity cell (353,809 against 353,813 EUR; 91.4% either way). The result is
   deterministic and inside §0's disclosed tolerance. §0's sentence "The integer stage's optimum is feasible here, so
   nothing is lost" predates the correction and is no longer exact.
3. **v6's missing-day cause, as stated, is incomplete.** The packet says the 33 days are those "whose D−1 or D−7 source
   day is a clock-change day". v6 in fact lacks local hour 2 on D+1, D+2 and D+7 after each of the 11 changes (for
   example 2021-03-30 and 2021-11-02, two days after a change). The count and the treatment are correct.
4. **"Doing nothing"** (contract §4, profit zero, for reference) is not shown as a reference row in the report. The
   brief's outcome 3 does not list it, and its value is identically zero.
5. **The brief's expected state says the snapshot "also holds days after 2026-09-06".** The pinned file's metadata
   ends at delivery day 2026-09-06 (67,343 rows), so no later market value exists in any CP-29 input. The candidate
   also cuts and guards at the boundary, so either way the red line holds.
6. **The packet's O57 binding check** names `tests/test_30`'s earlier bytes, but the round changed `tests/test_29`,
   not `test_30`. The critic checked: no committed file cites `test_29`'s earlier blob (`6d2f2f02…`) or SHA-256
   (`9deb02de…`).
7. **Rulings O57, O58 and O59** are recorded only in the candidate's packet and named in this review's assignment. The
   critic took them as issued and checked the candidate against them; their issuance was not independently verified.

## On FAIL only
- Single largest meaningful gap: not applicable (PASS).
- Exact next acceptance test: not applicable (PASS).
