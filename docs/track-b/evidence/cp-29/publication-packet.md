# CP-29 publication packet

**The brief `docs/track-b/evidence/cp-29/issued-brief.md` (SHA-256
`c3a5a8919631293916a0a457ca93542e0544a400a8bc9019596fb00313e3a1b0`); the Owner's approved economic-policy contract
`docs/track-b/economic-policy-contract-2026-11-15.md` (SHA-256
`21a9208573668becd2af3d9e476855e3f8c0e66c85fc9097194bd6deae580889`, decision 32); research v21-r20.** This section,
§0, was committed before any profit was computed. The contract is the authority: §0 fixes only what it leaves to the
research round (its §3, "Fixed by the research round before any number", and programme §4.E's engineering items), and
the Orchestrator's rulings on two points it does not settle.

## §0. Rules fixed before any number

### The Orchestrator's rulings in this round (decision 27), beside the brief

- **O57 (the claim layer's paths):** the allowed paths gain `src/delu_forecast/research.py`, for CP-29's sources,
  populations and record builders only, and `docs/track-b/research-content/cp29-claims.md`, with its `CLAIM_MAPS`
  entry and `tests/test_30`'s coverage of it. Existing entries stay byte-identical in meaning; no page or README change
  in this round (PRES-7 renders).
  - **The binding check, before any edit:** no committed file cites the bytes (git blob or SHA-256 at `eab32284`) of
    `research.py` (`2f6953ac…`), `research_claims.py` (`239b3d1f…`), `registry.py` (`23efe505…`) or
    `tests/test_30` (`6763b3bf…`), apart from CP-24's historical base-tree record, which its own docstring says binds
    no later work. `tests/pres5_landed_code.py` (O34) compares those three modules with PRES-5's recorded copies, not
    the working tree, so editing them is safe. CP-29's own code lives in `src/cp29/`, outside CP-26's landed-code paths
    (`src/cp26/harness.py`'s `LANDED_CODE`). `PINS` holds governance files only. No freeze manifest pins them.
- **O58 (two clarifications of the contract, before §0; no parameter changes):**
  1. **One direction per hour.** A mixed-integer programme with one binary per hour, so the battery charges or
     discharges in an hour, never both. HiGHS's MIP, through the locked scipy, with the same limits for every source,
     perfect foresight included: a single-inverter battery cannot do both at once.
     - **Rejected, and why:** the pure LP, which can buy and sell in the same hour and so earn at negative prices by
       burning energy through the losses (an artefact, not a strategy the contract describes); and the LP with charge
       plus discharge at most 1 MW in an hour, which still allows part of it. **No profit was computed under either.**
  2. **The wear cost's base:** €25 per MWh of energy leaving the battery at its terminals, the energy sold at the grid
     divided by √0.85, as the contract's derivation states. The daily cycle limit uses the same base (at most 2 MWh
     leaving the terminals). The exchange fee stays on the energy bought and sold at the grid.

### The programme (`src/cp29/battery.py`)

For each delivery day D, each source and each rule, one programme over D's hours t = 0 … T−1 (T = 23, 24 or 25):

- **Variables:** `c[t]`, the energy bought at the grid (MWh, charging); `d[t]`, the energy sold at the grid (MWh,
  discharging); `s[t]`, the energy stored at the end of hour t (MWh, at the battery's terminals); and a binary `z[t]` per hour (1: the hour may charge; 0: it may discharge).
- **§2's limits:**
  - power, 1 MW at the grid each way: 0 ≤ c[t] ≤ 1 and 0 ≤ d[t] ≤ 1 (MWh in an hour);
  - efficiency √0.85 on charge and on discharge: s[t] = s[t−1] + √0.85·c[t] − d[t]/√0.85;
  - usable energy 0 ≤ s[t] ≤ 2 MWh; empty at the start and at the end of each day: s[−1] = 0, s[T−1] = 0;
  - one cycle a day: the energy leaving the battery at its terminals, Σ d[t]/√0.85, is at most 2 MWh (O58);
  - one direction per hour (O58): c[t] ≤ z[t] and d[t] ≤ 1 − z[t].
- **The objective,** maximized: the forecast's net value Σ sell[t]·d[t] − Σ buy[t]·c[t] − wear·W − 0.10·Σ (c[t] +
  d[t]), where W = Σ d[t]/√0.85, the energy leaving the battery at its terminals (O58). Under the median rule `buy = sell = q50` (`p50`); under the risk-aware variant
  `buy = q75` and `sell = q25`; perfect foresight uses the cleared prices for both.
- **Step 3:** if the best value is not above €1e-6, the battery does nothing on D.
- **Settlement:** the chosen schedule at D's cleared prices, with the same wear and fee: Σ price[t]·(d[t] − c[t]) −
  wear·W − 0.10·Σ (c[t] + d[t]).
- **Wear:** €25 per MWh (main), then €0 and €50 (sensitivity), each run separately, never chosen afterwards.

### The solver, its tolerances and the tie-break

- **The solver:** HiGHS through scipy 1.18.1 from the locked environment (`uv.lock` `5d2aecc3…a94`):
  1. the integer stage, `scipy.optimize.milp`, presolve on, relative MIP gap **0**. HiGHS's absolute MIP gap and its
     MIP feasibility tolerance stay at their defaults, about 1e-6, which scipy cannot change;
  2. then the linear stage. With each hour's direction fixed from the integer stage (`c[t] ≤ z[t]`,
     `d[t] ≤ 1 − z[t]`), the same three solves run again as linear programmes, through
     `scipy.optimize.linprog(method="highs")`, presolve on, primal and dual feasibility tolerances 1e-9.

     The schedule comes from this stage. The integer stage's optimum is feasible here, so nothing is lost.
- **The tie-break** (contract §3: "among equal optima, the schedule that trades earliest and least"): three solves.
  1. The best value V*.
  2. Among schedules worth at least V* − ε_v, the least energy traded, E* = min Σ (c[t] + d[t]).
  3. Among those also trading at most E* + ε_e, the earliest: min Σ (t + 1)·(c[t] + d[t]).

  Least comes before earliest; equal optima are values within ε_v of V*. The three solves run in the integer stage
  and again in the linear stage, each lexicographically at the optimum within the tolerance (O58).
- **Tolerances:** ε_v = €1e-6; ε_e = 1e-7 MWh; an energy below 1e-9 MWh is set to zero; the limit check allows 1e-7
  MWh. The schedule is a function of the inputs alone; `tests/cp29` checks that the same inputs give the same schedule.
- **The limits are checked on every schedule** (`battery.violations`); any breach stops the run, writing nothing.
- *Correction, 2026-11-15 16:33 UTC, before any profit was kept or seen:* the first run (16:30–16:32 UTC) stopped in
  the integer stage's third solve, which HiGHS found infeasible. The cause: ε_e = 1e-7 MWh (and ε_v = €1e-6) are below
  HiGHS's MIP feasibility tolerance, about 1e-6, which scipy's `milp` cannot tighten. That run had passed the checks
  before the results and wrote nothing; no profit from it was written, printed or read.
  - **The integer stage's tie-break slacks** are now ε_v = €1e-4 and ε_e = 1e-5 MWh. That stage only chooses each
    hour's direction.
  - **The linear stage keeps ε_v = €1e-6 and ε_e = 1e-7 MWh** and sets the schedule.
  - **A tie-break solve** (the second or third) that HiGHS still finds infeasible keeps the previous stage's
    solution, deterministically. Each one is counted in `daily.csv` (`tie_break_fallbacks`) and in `checks.json`.

### The day, a missing hour, and the joins (`src/cp29/inputs.py`)

- **A delivery day's hours** are the committed snapshot's hours for that Europe/Berlin day: 23 on the spring change,
  25 on the autumn change, 24 otherwise. P-all holds six 23-hour days and three 25-hour days.
- **A missing hour** (contract §5): if the source lacks any of D's hours, or a price is missing, D is not traded:
  profit zero, kept and counted, never dropped. Known from the joins before any profit, the source's own gaps are:
  - v6, 33 days: CP-26's lag rule fails closed at local hour 2 on the days whose D−1 or D−7 source day is a
    clock-change day, so CP-28's stored A1 forecasts have no row there;
  - the naive, 11 days: its frozen rule fails the same way on the Sundays a week after a clock change;
  - v5, 4 of its 358 days; perfect foresight, none (the snapshot has no missing price on P-all).
- **The joins,** every one by UTC delivery hour (the snapshot's `timestamp_utc`):
  - **the cleared prices:** `data/snapshot.parquet`, `price_eur_mwh` (`7dd2dc73…7f00`), cut at 2026-09-06 before
    anything reads it, every row through `cp25.guard`;
  - **v6:** `reports/cp28/forecast/hourly.parquet` (`f5cb02a1…f638`), arm `A1`, `q25`, `q50`, `q75`;
  - **v5:** `reports/ddnn2/attempt-1/predictions.parquet` (`9d3f539f…5cf9`), policy `v5`, folds 2–5, `p25`, `p50`,
    `p75`;
  - **the naive:** `delu_forecast.baselines.similar_day_naive` (`baselines.py` `4e234cda…ea52`) on the cut snapshot.

### The checks before the results (`src/cp29/evaluate.py`, `checks`)

Run first; if any fails, nothing is written.

- **The naive's parity with CP-26's B0 central vector,** wherever a committed record holds it. CP-26's parity record
  `reports/rebaseline/cold-rerun-2026-10-15/parity.json` (`090c3cb4…dbc5`) holds B0's central vector as IEEE-754 bits
  for four development days (2021-04-01, 2022-07-01, 2025-05-01, 2026-01-08), on two paths; the naive must equal
  every one bit for bit. Verified before this section was committed: 8 of 8 equal.
  - CP-28's daily losses do not hold B0's central vector: B0's daily MAE there scores its interval layer's median,
    not the similar-day price, so it is not a parity record.
  - **Supplementary:** the frozen package's B0 (CP-17's, the same rule) records its issued central vector's SHA-256
    for five development days in CP-18b's committed dry run (`reports/cp18b/dryrun/store/issued/*/record.json`); the
    naive must equal all five. Verified: 5 of 5.
- **The populations equal PRES-6's:** P-all 2,068 days, P-v5 358 days (verified).
- **The brute force:** every 50th day of P-all in calendar order from the first (42 days), each source and rule, wear
  €25. A dynamic programme over every schedule on a grid of stored energy (0.05 MWh steps) and energy discharged so
  far finds the best forecast value on the grid. It must never beat the solver's by more than ε_v. Each grid step is
  one battery flow in one direction, so it covers the integer programme (O58).
- **After the rows:** perfect foresight is never negative on a day; every schedule meets every limit.

### The measures (contract §6), from the daily rows alone

Per population (P-all, P-v5), scope (all days; each regime, with its count), source, rule and wear:

- cumulative net profit (EUR), the sum of the daily profits;
- the share of perfect foresight captured: the sum of the source's daily profits over the sum of perfect foresight's
  under the same wear, on the same days; "undefined" when that sum is zero;
- the daily distribution: mean, median, 5th and 95th percentiles (`numpy.percentile`, linear interpolation);
- losing days (profit below zero): their number, their share of all the population's days, and the largest single-day
  loss;
- the maximum drawdown: the largest fall of the cumulative profit curve, which starts at zero, from an earlier peak;
- trading days, and the energy cycled: MWh bought and sold at the grid, MWh discharged from the battery, and full
  cycles (that last over 2 MWh).

The regimes are PRES-6's: before the crisis (2020-12-29 to 2021-08-31), the crisis (2021-09-01 to 2022-12-31), and
from 2023-01-01. The cumulative series is the daily rows themselves.

### The paired differences and the bootstrap

- **The pairs,** under each wear (€25, €0, €50, in that order) and, within each wear, in this order:
  1. P-all, median rule: v6 − the naive;
  2. P-v5, median rule: v6 − the naive;
  3. P-v5, median rule: v6 − v5;
  4. P-v5, risk-aware variant: v6 − v5.
- **Day by day,** on the same days; the mean daily difference and the total, n times the mean.
- **The interval:** 95%, percentile (2.5% and 97.5%), from a paired non-circular moving-block bootstrap over the days
  in calendar order: 14-day blocks, 2,000 replicates, PRES-6's own function (`final_candidate._block_means`), one
  generator seeded **20261115**, drawn in the order above.

### The records (`reports/cp29/`)

- `daily.csv`: one row per day, source, rule and wear, with the regime, P-v5 membership, the day's hours, the missing
  flag, the trading flag, MWh bought, sold and discharged from the battery, the forecast's expected profit, the
  realized profit and the evidence class, **simulated, development, post-selection**.
- `summary.csv`, `paired.csv`: derived from `daily.csv` alone; `python -m cp29.evaluate --check` re-derives both, byte
  for byte.
- `checks.json`: the checks above, the programme's form, the tolerances and every input's SHA-256.
- `report.md`: the method, the results with their uncertainty, the disclosures and "what it does not claim", in plain
  words.

**Nothing else is computed:** no other battery, rule, threshold or variant.

---

The sections below were written after the results existed.

## §1. What the round produced

| Item (the brief's outcome) | Where | Evidence |
|---|---|---|
| 1 The rules fixed before any number | §0, committed in `212a39cc`, corrected in `774238d2`, both before any profit was kept | `git log` |
| 2 The checks before the results | `reports/cp29/checks.json` | the naive's parity 8/8 with CP-26's B0, 5/5 with the frozen package's; P-all 2,068, P-v5 358; the brute force never beat the solver in 184 programmes; every schedule within the limits; perfect foresight never negative; no tie-break fallback |
| 3 The results, exactly the contract's | `reports/cp29/daily.csv` (26,964 rows), `summary.csv`, `paired.csv` | `python -m cp29.evaluate --check`; `tests/cp29/test_evaluation.py` (a fresh re-solve of sampled days reproduces the committed rows) |
| 4 The records | `reports/cp29/`: the daily rows, each labelled simulated, development, post-selection; the summaries and pairs derived from them alone | the same |
| 5 The report | `reports/cp29/report.md`, written from the records (`python -m cp29.report --check`) | `tests/cp29/test_evaluation.py` |
| 6 The registry entries for PRES-7 | `research.py`: three sources and 2,076 `cp29.*` records; `research_claims.py`: eight claim blocks (C1101–C1108) on the `PRES7` surface, rendered nowhere in this round, and W56, W57; `registry.py`: `evidence/cp-29`; the claim map `docs/track-b/research-content/cp29-claims.md` | `tests/cp29/test_claims.py`; `tests/test_29`, `tests/test_30` |

**One defect found and fixed before commit:** the first summaries listed v5 under P-all, whose share of perfect
foresight then compared v5's 358 days with perfect foresight's 2,068. The contract runs v5 on P-v5 only; P-all's
summaries now omit it, and a test refuses the mixing.

## §2. The export manifest (ruling O59)

`scripts/mlflow_export.py` regenerated `reports/presentation/mlflow-export/manifest.json`. **Every changed line is a
CP-29 source entry** (`git diff`, 23 lines, all additions):

```text
+  "reports/cp29/daily.csv": {
+   "blob": "c0a8794b8139633cf945922e460db699ca4facab",
+   "tag": "evidence/cp-29"
+  },
+  "reports/cp29/paired.csv": {
+   "blob": "64d305bd70e844ca19b6701872f2f4aff248141a",
+   "tag": "evidence/cp-29"
+  },
+  "reports/cp29/summary.csv": {
+   "blob": "6e969b79ce891a7ea861d412a44ce20e25e97b92",
+   "tag": "evidence/cp-29"
+  },
```

No run, experiment tag, description or other field changed; no other export file changed; nothing was uploaded or
written to MLflow. The pin check before the edit: no committed file cites the manifest's earlier bytes (blob
`17ea2a73…`, SHA-256 `c9eaac33…`). `tests/test_34`: see §3.

## §3. Checks run

(Filled at the candidate.)
