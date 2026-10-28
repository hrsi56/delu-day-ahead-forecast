# CP-17's freeze record: A1 as a complete daily policy on one code path

**The machine-readable freeze** is [`freeze-manifest.json`](freeze-manifest.json). It holds:
- **the policy identity:** SHA-256 `a4624978b60a8227475a8502d1309c913f4f840daba980a0bbd0b8ddf1356a94`. Every issued artifact cites it.
- **the initial artifact and state** at the freeze origin.
- **the reference bundle's manifest.**

Its content digest is `c48d82a51575cd9c5a15088a966977a2a9e3471405c9c821d9f1d2411519bceb`.

**Verifying it.** `python -m cp17.tools.freeze verify docs/track-b/evidence/cp-17/freeze-manifest.json`
recomputes every recorded file hash from the files themselves. It refuses an altered or missing file, a wrong
registry version, or a broken digest; the positive controls are in `tests/cp17/test_records.py`.

**Authority:**
- `capstone_v21.md` v21-r17: §24.9, §16.2, §16.4's CP-17 row, §19.2, §19.3, §19.5, §19.7, and §9's freeze
  identities;
- the Owner's decisions 1–12 (`docs/track-b/pre-cp-17-rulings-2026-10-25.md`, `d29b0abc…`);
- the brief `9f235cf8…`.

**"Frozen"** means this. After CP-17 lands, any change to the policy, its code, its runtime or its state
needs a new freeze and a new evaluation (§16.2). Daily fitting changes weights and state within the frozen
policy, and is not a change to it.

## 1. The designation and its prerequisites (§16.1, §16.4)

- **The designation.** A1 is designated the final version, pending 4.7T: DDNN-2 alone, CP-26's nominal D2
  with its own Johnson SU quantiles, which CP-28 selected (decision 1).
- **v1 remains the product until CP-19.** It also remains while 4.7T, CP-18 and the live trial are pending.
- **The prerequisites, all landed:**
  - CP-25 (the development inputs; `land/cp-25`);
  - CP-26 (the re-baseline; `land/cp-26`);
  - CP-28 (the selection; `land/cp-28`, `selection.json` `22a3dacf…`);
  - CP-17-probe (`land/cp-17-probe`).
- **What follows:** 4.7T, under the frozen protocol; then CP-18; then CP-19.

## 2. Code and dependencies (§16.2)

- **The one code path is `src/cp17/`** (§19.2). The issuing host, the native reference and the browser run
  the same files:
  - the product modules `dailyfit`, `issue`, `scoring`, `retrain`, `attribution` and `schema`;
  - the host driver;
  - the landed model code they import;
  - two import-only stand-ins (`holidays`, `resource`).
- **The package:** 33 files, SHA-256 of the file list `54212d2cb0862453bee72ff56f0c0821cb6ba0e3751aa05f478ad6547d233e6c`.
  - Its deterministic zip is 86,816 bytes, `1d4e3c7e…`.
  - The import closure is measured, not declared (`cp17.tools.bundle`). The native-only drivers in
    `cp17.tools` never ship.
- **Dependencies:**
  - the root `uv.lock` `5d2aecc3…` and `pyproject.toml` `aa35326a…`, both unchanged;
  - the pinned runtime's packages: numpy 2.2.5, pandas 2.3.0, scikit-learn 1.7.0, LightGBM 4.6.0 and their lock
    dependencies.
- **The issuing host** (decision 10): Pyodide 0.28.0 in Node.js v26.7.0, one worker.
  - **Pyodide** is identified by its 23 file hashes, which equal CP-17-probe's retrieval manifest. Its lock
    file reports `0.28.0.dev0`.
  - **Node.js** is `/opt/homebrew/Cellar/node/26.7.0/bin/node`, SHA-256 `1ef99ea2…d040`.
  - **No component needs §19.3's exception route.** A1, v4, v2 and B0 all run there and in both browsers.
  - **v5,** the 4.7T control, runs natively. It is not in the product's chain.

## 3. Features and source availability (§24.4, §24.5)

- **The issue time** is D−1 11:00 Europe/Berlin: 09:00 UTC when D−1 is on CEST, 10:00 UTC on CET, by D−1's
  own offset (`cp25.guard.issue_time`).
  - An input is usable only if published strictly before that instant.
  - No price of D, and no transformation that reveals it, enters (the target-day embargo).
- **Tiers.** The tier register `reports/development-inputs/tier-register.json` applies with the Owner's
  rulings:
  - the CP-25 rulings (`docs/track-b/cp-25-rulings-2026-10-12.md`);
  - the margin ruling;
  - the GFS ruling of 2026-10-19.

  CP-17 records these rulings; it does not change them. Their hashes are in the policy identity.
- **The payload contract** is `payload-schema.md`: the training window never carries its target day's
  outcome.

## 4. Hyperparameters and search state (§24.9)

- **A1's search state:** CP-26's nominal search S_13 = 2026-07-08 (`k13.json`), with the four best effective
  configurations, two seeds each.
  - Recorded by its file hash and its content digest `6090f4ab…`, and its eight members by rank, repeat,
    seed and configuration.
- **The landed recipes:**
  - CP-15's protocol, by digest;
  - LEAR's relative-alpha grid and chronological validation;
  - LightGBM's four-configuration capacity grid (`cp21.lgbm.GRID`);
  - the fixed blends: v4 = A1_w/3 + B2_w/3 + L-N/6 + L-R/6; v2 = A1/2 + B2/2; v5 = A1_w/3 + B2_w/3 + L-N/12
    + L-R/12 + D2/6.
- **The combiner state.** A1 has none: DDNN-2 alone. The fallbacks' and the control's blend weights are fixed.

## 5. Training windows and label rules (§2, §16.2)

**The windows:**
- **A1:** [max(2019-01-01, D−728), D), with lags reaching D−735, and seeded held-out weeks and early
  stopping per member.
- **LEAR:** CP-15's history start, with a 28-day chronological validation.
- **LightGBM:** [max(2019-01-01, D−728), D), with capacity chosen on the window less its last 28 days.

**Training targets** are delivery days before D, published strictly before the issue time. D−1's prices are
published on D−2, so D−1 is a training target. This is the landed rule, which CP-26's parity reproduces.

**Released errors** in every interval buffer come from complete delivery days ≤ D−2, consumed once (§2).

See conflict C1 in §11.

## 6. The initial artifact and state at the freeze origin

**The freeze origin** is the issuance for delivery 2026-09-06 at 2026-09-05 09:00 UTC.

**The initial artifact** is the issuing host's A1 artifact:
- ``8b881354e1b47b36f600f9d1a540e1da784749bca479a188051bd2091c76f8db``, kept in [`artifact-2026-09-06.json`](artifact-2026-09-06.json), with its arrays in the
  reference bundle;
- displayed as "successful daily fit";
- issued in 67.7 s of wall time and 831 MiB of peak memory,
  within the 15-minute and 4 GB ceilings.

**The initial state** is the fallbacks' and the control's interval states at the freeze origin: v4's, v2's
and v5's H buffers and B0's raw-error buffer, each 28 released days, 2026-08-08 to 2026-09-04.
- They are rebuilt from CP-26's ledger.
- Every rebuilt day's errors equal the hash CP-26's final replay state consumed.
- They are recorded by digest in the manifest's `initial_state`.

4.7T's first forecast, delivery 2026-09-07, is issued at 2026-09-06 09:00 UTC from data available then.
CP-17 prepares it; it does not produce it.

## 7. Randomness and seeds

- **A1:** the eight member seeds of S_13, which also seed the held-out weeks. They are fixed.
- **The search seeds** follow §24.7's formulas, for S_14 on.
- **LightGBM's `random_state`** is 42, CP-15's protocol seed. LightGBM is deterministic and row-wise.
- **LEAR** has no seed: cyclic coordinate descent, so the protocol's recorded seed 42 never enters.
- **The 4.7T analysis seed** is 20261204.
- **No retry with a replacement seed,** ever.

## 8. The refit schedule (§24.9)

- **Every delivery day, including DST days,** every policy that issues is refitted from its own shipped
  training window.
- **DDNN-2's 182-day searches continue:** S_k = 2020-01-15 + 182k, the next being S_14 = 2027-01-06, under the
  same phase, rules and seeds. These are protocol dates only, never permission to read future data.
- **No search falls in 4.7T's window.**

## 9. The uncertainty layers

- **A1:** DDNN-2's own Johnson SU quantiles, the per-level median of the eight members, with the landed
  crossing restoration.
- **v4 and v2 (fallbacks):** the H layer, hour-aware quantiles of the last 28 released standardized own errors:
  - shrinkage n/(n + 56), from 14 distinct days at the hour;
  - scaled by the issued scale.
- **B0:** the pooled linear quantiles of its last 28 released raw errors.
- **v5 (the control):** its own H layer.
- **The lock-price policy** is not adopted (decision 3).

## 10. The failure policy and the success definition (decisions 11 and 12; §16.2)

**The chains** (`cp17.issue`):

| Cause | Chain |
|---|---|
| GFS late or missing at the issue time | A1 recorded as skipped for an unavailable input → **v2** → **B0** → failed issuance |
| A1's own fit fails while the weather is available | **v4** → **v2** → **B0** → failed issuance |
| a fallback's own fit fails | the next one in its chain |

**The rules of the chain:**
- **A1 issues whenever its own fit succeeds.** The validity of other policies' members never triggers a
  fallback. CP-28's common-member check was a comparison device, and v5 is not in the product's chain.
- **Every fallback is complete:** no subset is renormalized, and no quantile is manufactured.
- **Display:** a failed or skipped fit is displayed as such, even when a fallback issues. A fallback forecast
  never counts as a successful A1 fit.
- **Disclosure:** for the GFS-late route, item 1's measured excess (`reports/cp17/gfs-check.md`) is disclosed:
  v2 is +2.27% MAE and +6.68% WIS against A1's GFS +6 h route on the 1,354 paired affected development
  dates.

**The success definition** (the brief's, as `cp17.issue` implements it). For D, issued at D−1 11:00
Europe/Berlin:
1. **Inputs:**
   - the payload's identity verifies;
   - the target day's outcome is absent;
   - released errors are from complete days ≤ D−2;
   - training targets end before D.
2. **Training:** the members train under the frozen rules with no guard refusal and no non-finite value. One
   failed DDNN-2 member fails A1: there is no subset median (`src/cp26/members.py:199`, `:213`; landed rule
   and definition agree).
3. **Emission:** seven finite, ordered quantiles for every delivery hour of D (23, 24 or 25).
4. **The artifact:** written with its training window, labels, seeds, timestamps and parent, input and state
   hashes, and it verifies.
5. **Resources:** under the issuing host, one worker, ≤ 15 minutes of wall time and ≤ 4 GB peak memory.
   - **Each attempt is measured on its own.** It runs in its own fresh issuing-host process, and is judged on
     that process's wall time (runtime load included) and peak resident memory.
   - **This is judged inside `cp17.issue.attempt`, before the chain moves on,** for A1 and for every
     fallback alike.

Anything else is a failed fit:
- **its forecast is never issued, and the chain moves on.** A1 over the ceiling → v4; v4 over it → v2; v2
  over it → B0; B0 over it → a failed issuance;
- **v4 and v2 are judged by the same five criteria,** with their own frozen training rules;
- **natively** (the comparison path), criterion 5 is not judged, and the record says so;
- **the tests** are `tests/cp17/test_units.py::test_a_fit_over_the_resource_ceiling_fails_and_the_chain_moves_on`
  and its neighbours.

**Exercised under the issuing host on real development payloads,** one fresh process per attempt, each path
the same natively:

| Case | Path | Display | Issued forecast vs native |
|---|---|---|---|
| 2026-09-06, GFS available | A1 ok | successful daily fit | within ±0.01 EUR/MWh (largest 9.4e-13 EUR/MWh) |
| 2026-09-06, GFS declared unavailable | A1 skipped → v2 ok | skipped fit (GFS late or missing); fallback v2 issued | within ±0.01 EUR/MWh (largest 5.1e-13 EUR/MWh) |
| 2022-12-04 (a real A1 failure) | A1 failed (member 2, seed 26590021, `nonfinite_loss` at epoch 21, in both runtimes) → v4 ok | failed fit; fallback v4 issued | within ±0.01 EUR/MWh (largest 5.1e-13 EUR/MWh) |

Record: `reports/cp17/issuance.json`.

## 11. Gaps and conflicts, with proposed resolutions for r18

Each proposal was written without any 4.7T outcome. None changes landed code.

- **G1: the fallbacks' interval states need daily issuances.**
  - **The gap.** v4's and v2's H buffers, and B0's raw-error buffer, consist of each policy's own released
    errors. CP-26 issued every policy every day, but the product issues a fallback only when A1 fails. So a
    fallback's buffer would go stale, and a v4 fallback months later would carry an old error buffer.
  - **Proposed.** The daily pipeline fits the chain's policies (v4, v2, B0) every day under the issuing host,
    as **shadow issuances**: their central and scale are stored before the outcome, and they are never
    published as the product's forecast. This keeps their own buffers current, exactly as CP-26 did. The
    cost measured here is about 55 s (v4), about 45 s (v2) and under 1 s (B0) per day on the issuing host,
    within the 15-minute ceiling.
  - **The initial states** are CP-26's at the freeze origin (§6). Errors from native and from issuing-host
    issuances differ by rounding only (about 1e-12 here).
- **C1: "labels ≤ D−2" against the landed training targets.**
  - **The conflict.** The brief's criterion 1 says labels come only from complete delivery days ≤ D−2. But
    the landed training windows use D−1's published prices as targets: `src/cp24/design.py:306-307`
    (`[max(2019-01-01, D−728), D)`), `src/cp15/models.py:45` and `src/cp21/lgbm.py:123-126`. CP-26 ran
    them so, and its parity holds only so.
  - **Proposed.** "Labels" means the released forecast errors of the interval layers (§2's rule, ≤ D−2).
    Training targets are the delivery days before D published strictly before the issue time (§24.4,
    §24.7's "A training target enters only once its price was published before the issue time").
    `cp17.issue` checks both so.
- **C2: "every delivery hour of D" against the landed partial issuance.**
  - **The conflict.** The landed design issues only for hours whose inputs are valid:
    - `src/cp15/data.py:79-80`: rows are `feature_valid`;
    - `src/cp24/member.py:43-45`: the keys are those rows.

    CP-26 scored such days on CP-25's frozen keys. In CP-26's ledger, 43 of the 2,078 scored development days
    have incomplete issuance keys. Most are the days after a DST change, where a lag of the 23-hour day
    leaves one hour unforecastable. A few are input gaps with no keys at all.
  - **What happens now.** Under criterion 3 as written, every policy fails on such a day, so it is a failed
    issuance. 4.7T's window holds the 2026-10-25 DST change.
  - **Proposed.** A fit that emits for every hour the frozen design can forecast counts as successful on
    those hours, and is displayed as partial with the missing hours named. A day with no forecastable hour is
    a failed issuance. Until r18 rules, `cp17.issue` follows the brief as written.
- **G2: GFS missing in the training window, not at the issue time.**
  - **The case.** It is not the GFS-late route. A1's landed rule fails the fit
    (`uncovered_fails=True`), so the A1-failure chain applies. v4 checks its weather rows too and fails, so v2
    issues.
  - **Proposed.** Record this explicitly, as the implementation does.
- **F1: an issuing-host parity miss, reported and not tuned (brief item 3).**
  - **The miss.** At the 25-hour DST origin 2025-10-26, A1 under the issuing host differs from the native fit
    by up to 0.028 EUR/MWh (p50), above τ_eq = 0.01, with every data-driven selection identical.
  - **The cause** is one configuration, `cp26-k11-t032`, whose two members both train to the 1,000-epoch cap.
    Member 5 (seed 27190032), whose best epoch is the last, differs by 0.77 EUR/MWh in its own quantiles, and
    member 4 (seed 27190031) by 3.6e-05. The other six agree to about 1e-12.
  - **What it means.** τ_eq, set from CP-17-probe's two origins (largest 6.3e-7), is not a bound on rounding
    between native CPython and WebAssembly for long-trained DDNN-2 members. It remains the visitor's tolerance
    against the issued artifact, which the same WebAssembly runtime produces. That comparison is bit for bit
    in Chromium and WebKit.
  - **For r18:** record that the issued values can differ from native arithmetic by this much, and that the
    native parity with CP-26 stays the code-identity check. Nothing is changed.
- **None needs a §19.3 exception.** Every product component runs under Pyodide within the measured limits.

## 12. The registry identities (§9, the tracking spec)

- **Names and versions:** the registered model `delu-day-ahead-policy`, version 1; live metrics in the
  experiment `delu-live`, with the `live_` namespace wall.
- **These are local names and versions only.** Nothing is uploaded or registered at CP-17. The run names and
  tags follow `docs/track-b/mlflow-tracking-spec.md` (`8912e228…`), and CP-18 registers them under its
  authority.
- **The fingerprints the later evaluator must verify before opening outcome data** are the policy identity's
  and the freeze manifest's digests. `cp17.tools.freeze.verify` refuses a wrong or missing version, or an
  altered artifact.

## 13. The resource and calendar plan

For 4.7T: [`4-7t-frozen-protocol.md`](4-7t-frozen-protocol.md) §11.

For daily operation (CP-18):
- about 3 minutes on the issuing host per delivery day, including the proposed shadow issuances, issued at
  11:00 local;
- within the 15-minute and 4 GB ceilings of the success definition.

## 14. §19.5, §19.3 and §19.7, frozen

- **§19.5:** [`definitions.md`](definitions.md):
  - τ = 10 EUR/MWh;
  - the 28-scored-day rolling window;
  - the eight-band PIT and the reliability diagram with counts;
  - the recomputation tolerance 1e-9 · max(1, |b|).
- **§19.3:** τ_eq = 0.01 EUR/MWh and the three-status rule (decision 9; `cp17.retrain`).
  - **The training window is bound first.** A retrain is of the issued fit only if it ran on that fit's
    shipped training window (§19.3 item 1): its payload identity must equal the issued artifact's, or the
    status is "different". CP-17's first run of the training-window control showed why. A +1 EUR/MWh change to
    one training hour moved the quantiles by 0.0091 EUR/MWh with every selection matched, which the quantiles
    and selections alone would report as "within ±0.01 EUR/MWh".
  - **Negative controls:** a changed seed and a changed training-window value both report "different". A
    changed target-day outcome leaves all four payloads byte-identical (`reports/cp17/controls.json`).
  - **The reference runtime:**
    - Pyodide 0.28.0;
    - Chromium 153.0.8010.12 and WebKit 26.6, through Playwright 1.63.0;
    - Node.js v26.7.0;
    - the Apple M3 machine class, 8 cores, 16 GB, macOS 26.5.2.
  - The measured figures are in `reports/cp17/report.md`. The visitor wording is proposed there, for the
    Owner's later publication decision.
- **§19.7,** by component class (`cp17.attribution`):
  - **A1 (neural):** exact baseline Shapley over DDNN-2's input groups on the issued p50, with each member's
    training-row mean as the baseline, at most 2,048 coalitions, deterministic.
  - **v2:** the blend (A1/2 + B2/2), then each LEAR member's coefficient × centered, standardized input. The
    final Lasso is refitted from the landed calls and must reproduce its recorded coefficient hash.
  - **v4:** the blend (A1_w/3 + B2_w/3 + L-N/6 + L-R/6), the linear rule for the LEAR members, and TreeSHAP
    with split gain for the LightGBM members. The refitted booster must reproduce its recorded tree hash.
  - **Interval layers** are explained in words.
  - **All of it is attribution within one fitted artifact,** relative to its stated baseline, never
    causality or incremental value.
