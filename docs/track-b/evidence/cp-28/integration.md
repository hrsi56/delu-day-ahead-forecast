# Verdict — CP-28 — Integration — PASS

- Candidate SHA: 36ed7249db274cb99a906b5485e06ec2380d4922
- Plan / version / bar: `capstone_v21.md`, v21-r17 (anchor SHA-256 `3124451da84c3cd99fae728c371207aace6ae537474f7769d0ff6333ee53e4fc`), §24.8 "CP-28: 4.8 on stored forecasts (stage 8)". The section is 135 lines and 8,224 bytes, with section SHA-256 `5eaaa7c8ee418e1b4dc0029ccb66c862f3b6bc7fca1bbc451c4850bd39d84d26`. It is governed by §§24.2, 24.4, 24.5, 24.7 and 24.9 and by §2's released-error rule and target-day embargo. The frozen protocol `cp28-frozen-protocol-v21-r14.md` (`2b9286b0…7a8`) fixes every detail the section leaves open, the r17 supplement (`39f322af…3b4`) is bound beside it, and the issued brief is `57cb6d53…6ba3`.
- Verbatim bar excerpt:

  > ### 24.8 CP-28: 4.8 on stored forecasts (stage 8)
  >
  > **Status:** it runs only if the Owner confirms it after CP-26 lands. Every arm is specified here,
  > and in CP-28's frozen protocol (§24.7).
  >
  > **The members** are the control's three, from CP-26's ledger:
  >
  > - c_HG: v3's central forecast;
  > - L: the mean of L-N and L-R;
  > - D2: DDNN-2's median.
  >
  > **The control** is the control named under §24.5: v5, unless a tier ruling names a variant. It
  > keeps the weights (2/3, 1/6, 1/6) and its interval layer. **Wherever §§24.8–24.9 say v5, they mean
  > the control** (§24.5): in its weights, its forecast, the gates' L_v5, and the disclosures.
  >
  > **The construction, as v5's own:**
  >
  > - Weights apply to the members' central forecasts.
  > - Each combined arm's quantiles come from HG's H layer, re-estimated on that arm's own issued
  >   central errors.
  > - Each combined arm stores its pre-outcome native central with that issuance's causal weights
  >   and scale. Insufficient H history permits central warm-up and D−2 own-error release even on
  >   a scored fallback date. Missing members or solver failures create no native arm central.
  >   Copied fallback errors never populate the arm's H buffer, and emitted fallback scores stay fixed.
  > - The learned arms minimize mean daily central MAE.
  > - A1 keeps DDNN-2's own Johnson SU quantiles.
  >
  > **The ledger rule:**
  >
  > - A member forecast for day s enters any arm's learning only if s ≤ D−2: a complete delivery day
  >   released under §2. Its forecast was made without its outcome.
  > - D's combined forecast is produced before D's outcome enters the ledger.
  > - CP-26's warm-up supplies the first ledger days.
  > - The latest 728 complete released learning days (minimum 364/728) are separate from H's latest
  >   28 own-error days. A complete day with all three native members can be a learning row even
  >   when v5's measured output was fallback solely for H warm-up. Partial keys never create a
  >   complete learning row. Actual support, not a promised date, determines learning startup.
  >
  > **The arms (Owner, 2026-10-12):**
  >
  > | Arm | Rule |
  > |---|---|
  > | A1 | DDNN-2 alone, with its own quantiles |
  > | A2 | Equal weights, (1/3, 1/3, 1/3) |
  > | A3 | One global weight vector, chosen on the simplex grid with step 0.01 (5,151 points). It minimizes mean daily central MAE over the latest 728 ledger days on which all three members are valid, and needs at least 364 such days. Ties go to the point nearest v5's weights (Euclidean), then to the lowest grid index. Deployed weights = 0.5 × fitted + 0.5 × v5's, updated daily. Before 364 days: v5's weights |
  > | A4 | One weight vector for each of CP-21's blocks (night 22–05, solar 10–16, shoulder/peak 06–09 and 17–21), on the same grid, minimizing central MAE over the block's hours across the latest 728 ledger days, and needing 728. Deployed = 0.25 × the block's fitted vector + 0.75 × A3's deployed weights. Before 728 days: A3's deployed weights |
  > | A5 | The NumPy meta-learner (below) |
  > | A6 | A3 without shrinkage: the same grid, objective, window, minimum history and tie rule, with deployed weights = the fitted weights. It can reach any weighting, including 100% on one member. Before 364 days: v5's weights |
  > | A7 | A5 without shrinkage: the same network and training, with deployed weights = the network's output as it is. Before 364 days: v5's weights |
  >
  > **A5, the NumPy meta-learner:**
  >
  > - **Sixteen inputs, all known at the issue time:**
  >   - for each member, its mean absolute central error over the last 7 and the last 28 ledger days;
  >   - the high-volatility and negative-price-risk states (§24.7), and the "volatility unknown" flag
  >     below;
  >   - season, as four one-hot values;
  >   - hour block, as three one-hot values.
  > - **Output:** for each day and block, a softmax over the three members.
  > - **The network:** one hidden layer of 8 tanh units.
  > - **The loss:** the mean absolute error of the weighted central forecast over the block's hours.
  > - **Training:**
  >   - full-batch Adam, learning rate 0.01, 300 epochs, L2 penalty 1e-3 on the weights;
  >   - initialization seeded with `SeedSequence([28, D.toordinal(), 0x4D4C])`;
  >   - refit daily, from scratch, on the latest 728 ledger days, needing at least 364.
  > - **Deployed weights** = 0.5 × the network's output + 0.5 × v5's weights. Before 364 days: v5's
  >   weights.
  >
  > **Further fixed details:**
  >
  > - Training rows for every learned arm, A3 to A7, require all three members to be valid.
  > - The grid points are ordered lexicographically by (w_HG, w_L), ascending. A4's ties follow A3's
  >   rule.
  > - A5's and A7's inputs are standardized on the training window only. A6 and A7 share A3's and
  >   A5's fits: only the shrinkage differs.
  > - An unknown volatility state is encoded as "not high", with a separate 0/1 flag for "unknown".
  > - Adam's β1 = 0.9, β2 = 0.999 and ε = 1e-8; weights are initialized from a normal distribution with
  >   standard deviation 0.1, and biases at zero.
  > - **Any implementation detail this section still leaves open** is fixed in CP-28's frozen protocol
  >   before CP-26's first score. CP-26's Integration Critic checks that none depends on an outcome.
  >
  > **Failures:**
  >
  > - A missing member makes the arm use v5's forecast that day.
  > - If v5's forecast is missing too, B0's forecast is used.
  > - A solver failure, with every member valid, makes the arm use A2's.
  > - No arm renormalizes over a subset of members, and every fallback day is counted.
  >
  > **The gates, against the control (written v5 below), on CP-26's scored calendar:**
  >
  > 1. **Improvement:** `H0: E[L_arm − 0.995·L_v5] ≥ 0` is rejected for both MAE and WIS; that is, by
  >    more than 0.5%.
  > 2. **Non-inferiority:** `E[L_arm − 1.02·L_v5 | g] ≥ 0` is rejected for both MAE and WIS in each
  >    complete year, 2021 to 2025, and in each pooled season. A required cell with fewer than 90 days
  >    makes the arm inconclusive.
  > 3. **The compound test:** the arm's p-value is the largest over its required endpoints. Holm runs
  >    across the seven arms at α = 0.05; CP-27's family no longer exists.
  > 4. **Sensitivity.** Every arm's compound p-value and Holm are recomputed under each variant: 7-day
  >    blocks, 28-day blocks, and unstratified. An arm that passes under the primary analysis but fails
  >    under any variant is inconclusive, and is not adopted.
  >
  > **Disclosed in advance:**
  >
  > - A4 equals A3 until 728 complete released ledger days exist. All learned arms start according
  >   to actual support; member/search failures and incomplete days may delay it. Report the observed
  >   startup and calendar span, with no guarantee of a fixed activation date. A4's early cells test
  >   A3's weights to that extent.
  > - The learned arms equal v5 until their minimum history exists.
  > - **A6 and A7 are unshrunk** (Owner, 2026-10-12). They can place any weight on DDNN-2, up to 100%,
  >   and are the arms most exposed to overfitting and to lag at regime changes. The gates, the
  >   simplicity order and 4.7T are their protection.
  > - **CP-28's Holm control is conditional on the Owner's decision to run it.** That decision follows
  >   CP-26's report, which includes DDNN-2 alone (A1's forecasts) on the same calendar. 4.7T still
  >   carries the protection.
  >
  > **Selection:**
  >
  > - Among the arms that pass, the one with the lowest WIS wins.
  > - Arms whose WIS is less than 0.5% above the best are tied, and the simpler arm wins, in the order
  >   A1, A2, A3, A6, A4, A5, A7.
  > - If no arm passes, the control is the candidate for the freeze.
  >
  > **Further rules:**
  >
  > - There is one look, and no arm is added. A failed or unexecuted arm counts with p = 1.
  > - **Ceiling, proposed:** 40 machine-hours.
  > - **Evidence class:** `development_post_selection`; 4.7T carries the protection.
  > - **Gates:** CP-26's LAND, the Owner's confirmation, the issued brief, and the LAND.
  >
  > **Separate post-results supplement (v21-r17).** Before execution, report the approved
  > existing-output GFS differential and planning-scenario analysis under
  > `docs/track-b/evidence/cp-26/cp28-gfs-postresults-addendum-v21-r17.md`. It is outside the seven-arm
  > experiment and its multiplicity/selection family; it changes none of the frozen rules above.
  > An unfavorable or unsupported descriptive result is reported without tuning an arm, changing
  > the control or inventing an additional statistical or operational acceptance gate.

  (The excerpt is the citation. Any line number is a courtesy and is non-binding.)
- Worktree clean before and after: yes. `git status --porcelain` was empty at the start (2026-10-24T20:00Z) and at the end (2026-10-24T22:05Z), and HEAD stayed at `36ed7249db274cb99a906b5485e06ec2380d4922` throughout. The only ignored entries are three Finder `.DS_Store` files (`.DS_Store`, `docs/.DS_Store`, `docs/track-b/.DS_Store`). They were already present at the first ignored-file listing, and nothing in this review wrote them.

**Isolation.** The isolation was cooperative and procedural. The Critic made no Git write to the project repository: no commit, branch, tag, stash, push or worktree command. Every write went under `/Users/djourno/Downloads/PJM/.local/tmp/cp-28/critic/`, except this verdict. The Lead's `.local/artifacts/cp-28/` (inputs, bulk) was only read and hashed. The history-free copies are fresh, separate scratch repositories. Each has one commit, and each commit's tree equals the candidate's, as the step 4 reproduction required. The Critic read nothing dated after 2026-09-06 and saw no exposure.

## Commands actually run

Environment for every Python run: `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1`. Real-input runs used `/Users/djourno/Downloads/PJM/.venv/bin/python` (Python 3.13.15, the lock's packages). Below, `S` stands for `/Users/djourno/Downloads/PJM/.local/tmp/cp-28/critic`, and `W` is the worktree.

**Brief and bar**

1. `git show main:scripts/gauntlet.py | python3 -I - critic-brief cp-28` → exit 0. The brief was saved to `S/brief.md`.
2. `git show main:scripts/bar.py | python3 -I - check S/brief.md --source capstone_v21.md@36ed7249…` → exit 1, with two messages.
   - "ok: lines 13–147 (8223 bytes) appear in capstone_v21.md@36ed7249db27": the bar excerpt matches.
   - "MISMATCH … brief.md:310 … '[paste the exact text; confirm it appears in that file at this SHA]'": this second block is the templates' placeholder text, which the generated brief reproduces. It is not a bar quote.
3. `git show main:scripts/bar.py | python3 -I - bar capstone_v21.md "### 24.8 CP-28: 4.8 on stored forecasts (stage 8)" --at 36ed7249…` → exit 0. It printed "section 135 lines, 8224 bytes, sha256 5eaaa7c8…6d84d26", and `shasum` of the extracted section gives the same hash.
3a. After this verdict was written: `git show main:scripts/bar.py | python3 -I - check /Users/djourno/Downloads/PJM/.local/artifacts/cp-28/critic-1/integration.md --source capstone_v21.md@36ed7249db274cb99a906b5485e06ec2380d4922` → exit 0, "ok: lines 7–141 (8223 bytes) appear in capstone_v21.md@36ed7249db27".

**Identity**

4. `git status --porcelain` empty; `git rev-parse HEAD` = `36ed7249…4922`. `main` = merge-base = `315ad86cd35ea3c86fd685b13cdf60106df9fb73`.
5. `shasum -a 256` on the anchor, the protocol, the supplement, the GFS ruling, the tier rulings, PUBLISH_RULES, the packet template, CP-26's `scores-manifest.json`, the issued brief, `pyproject.toml` and `uv.lock` → every hash equals the brief's value.
   - `pyproject.toml` = `aa35326a…4e4a`; `uv.lock` = `5d2aecc3…a94`.
   - `git rev-parse evidence/cp-26` = `ca2033120288c6a396fec8c01404f0220523d695`.
6. `shasum -a 256` on CP-26's local `report.json` and `scores/hourly.parquet` → `1b1aa805…56d8` and `f465d5e7…e709`, as the brief states.
7. `git ls-tree -r evidence/cp-26` over the four input paths, compared with `git hash-object --stdin-paths` over the extracted `.local/artifacts/cp-28/inputs/reports/**` (`.DS_Store` excluded) → identical, 2,444 blobs. That is 2,441 forecast-ledger files, `learning-ledger.json`, `inference-manifest.json` and `replay-state.json`.

**Scope of the diff**

8. `git diff --stat main...HEAD` → exit 0, "53 files changed, 11005 insertions(+)".
   - `git diff --name-only main...HEAD` → 53 paths, all status `A`. None exists on `main`, and every one is under `src/cp28/`, `tests/cp28/`, `tests/cp28_synthetic.py`, `docs/track-b/evidence/cp-28/` or `reports/cp28/`.
   - `git diff --quiet main HEAD -- src/cp15…src/cp26 src/delu_forecast data reports/development-inputs reports/rebaseline pyproject.toml uv.lock AGENTS.md CLAUDE.md role files exposure-ledger backup-register gauntlet-templates PUBLISH_RULES rule-inventory capstone_* program-stage-sequence.md .claude .github .githooks scripts` → exit 0, so none of these paths changed.
   - `git ls-tree -r -l HEAD` → no file at or over 50 MB. The largest CP-28 file is `reports/cp28/forecast/hourly.parquet` at 23,721,382 bytes.
9. Per-commit file lists (`git rev-list --reverse main..HEAD`, `git diff-tree`), in this order:
   - `c846fe6`: the brief;
   - `fd95497`: the entry binding and the reader;
   - `9165c77`: the GFS note (18:52:18Z);
   - `22233e4`: the arms, the causal-control tests, their log and the scorer validation (19:14:40Z);
   - `b5bfd8e`: the forecasts (19:20:48Z);
   - `b627c86`: the scores;
   - `67e3449`, `91c8aab`, `36ed724`: report rendering and records only.
   - `git diff --stat b5bfd8e 36ed724 -- src tests` → only `src/cp28/report.py` and `tests/cp28/test_cp28_results.py` changed after the forecasts. `engine`, `grid`, `meta`, `states`, `inference`, `scoring`, `pipeline` and `reader` are unchanged since `22233e4`.
10. Manifest audit (`python3 -I`, hashing every file listed in `reports/cp28/forecast/manifest.json` and `results/manifest.json`, plus their `code_sha256`) → 0 code mismatches, 0 file mismatches. The results manifest's `forecast_manifest_sha256` equals the committed forecast manifest.
    - Forecast stage: `started_utc` 19:14:47Z, finished 19:20:25Z, `scores_computed: false`, `latest_truth_requested_at_last_origin: 2026-09-04`.
    - Score stage: started 19:20:54Z, after the forecasts commit at 19:20:48Z.

**Reproduction step 1: the CP-28 suite**

11. `cd W && PYTHONDONTWRITEBYTECODE=1 TMPDIR=S/tmp PYTHONPATH=src …/.venv/bin/python -m pytest -q -p no:cacheprovider -rs tests/cp28` → exit 0, "45 passed in 75.93s". No test was skipped, so the real-input tests ran. The worktree was still clean afterwards.

**Reproduction step 2: the full rerun**

12. `git -C W archive 36ed7249… | tar -x -C S/rerun/copy`, then `rm -rf` of the copy's `reports/cp28/forecast` and `reports/cp28/results`.
    - `S/rerun/local/artifacts/cp-28/inputs` → symlink to `/Users/djourno/Downloads/PJM/.local/artifacts/cp-28/inputs`.
    - `S/rerun/local/artifacts/cp-26` → symlink to `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26`.
    - Run from the copy with `CP28_LOCAL_ROOT=S/rerun/local PYTHONPATH=src`:

    | Stage | Exit | Time | Observed |
    |---|---|---|---|
    | `python -m cp28.pipeline validate-scoring .` | 0 | 8.46 s | v5 and B0 each have 2,068 dates, 0 missing, 0 extra; maximum relative difference 3.43e-16 and 3.21e-16 |
    | `forecast .` | 0 | 357.69 s | 2,441 origins, 17,087 issues; latest truth requested 2026-09-04 |
    | `score .` | 0 | 151.21 s | All seven pass in all four analyses; A1 selected |
    | `python -m cp28.report .` | 0 | 1.41 s | "wrote report, packet, export draft and owner summary" |

    The bulk retention was written to `S/rerun/local/artifacts/cp-28/bulk/bootstrap` (29 files).
13. `python -I S/compare_rerun.py W S/rerun/copy S/rerun/local/…/bootstrap /Users/djourno/Downloads/PJM/.local/artifacts/cp-28/bulk/bootstrap` → exit 0, "OVERALL MATCH".
    - The same 23 files exist under `reports/cp28/` in both trees, and 20 of them are byte-identical. That includes every parquet, csv and json apart from the two manifests, and `networks.npz` is byte-identical as well as array-identical.
    - `forecast/manifest.json` differs only in `started_utc`, `finished_utc` and `wall_seconds`.
    - `results/manifest.json` differs only in those three fields and in `forecast_manifest_sha256`.
    - `report.md` differs only in its two wall-time lines: 338.1 s committed against 356.5 s here, and 133.3 s against 149.8 s.
    - All 560 endpoint p-values are identical, and every status is "computable". `holm.csv` is identical, and `selection.json` is identical (A1).
    - The Lead's 29 bulk files match `bulk-manifest.json` in size and SHA-256. Array by array, the Critic's rerun bulk is identical to the Lead's.

**Reproduction step 3: the r17 note**

14. `cd W && PYTHONPATH=src …/python -m cp28.gfs_note . S/gfs` → exit 0, "wrote 172 rows". `cmp` against `docs/track-b/evidence/cp-28/gfs-postresults/{note.md,table.csv,provenance.json}` → all three are byte-identical (`8373dbd0…`, `1bfe1366…`, `a48ea631…`).

**Reproduction step 4: the history-free CI sequence**

15. `S/run-ci.sh ci312`. The script:
    - extracts `git archive` of the candidate into `S/ci312/copy`;
    - runs `git init -b main`, sets `core.hooksPath .githooks`, then `git add -A -f` and one commit (the pre-commit and commit-msg secret guards ran);
    - checks that the copy's tree equals the candidate tree `f9d64bc6bb9cfd8047db23415126e52895415eb1`, with a commit count of 1;
    - writes an invalid `.git` sentinel file at `<copy>/.local/tmp/.git`;
    - runs each step under `env -i` (credentials absent) with `HOME`, `PATH=<copy>/.venv/bin:/opt/homebrew/bin:/usr/bin:/bin:…`, `CI=true`, `UV_PYTHON=3.12`, `UV_PYTHON_DOWNLOADS=never`, `UV_CACHE_DIR=/Users/djourno/Downloads/PJM/.local/cache/uv` and `UV_OFFLINE=1` (also during the sync, which succeeded from the shared cache), `TMPDIR=<copy>/.local/tmp`, and the BLAS and telemetry variables above.

    | Step | Command | Exit | Time | Last line |
    |---|---|---|---|---|
    | 01 | `uv sync --locked --dev` | 0 | 1.4 s | " + zipp==4.1.0" |
    | 02 | `python3 --version` | 0 | | "Python 3.12.14" |
    | 03 | `uv run python --version` | 0 | | "Python 3.12.14" |
    | 04 | `uv run python scripts/build_wasm_payload.py` | 0 | 77.8 s | "wrote …/copy/reports/cp3b/payload.json" |
    | 05 | `uv run pytest -q -rs` | 0 | 451.6 s | "2234 passed, 33 skipped in 449.87s" |
    | 06 | `uv run pytest tests/test_10_cqr_order_statistic.py -q` | 0 | | "8 passed in 0.02s" |
    | 07 | `uv run python scripts/verify_release.py` | 0 | | "PASS — every bound claim agrees on every surface; the static page fetches nothing; …" |
    | 08 | `uv run pytest tests/test_22_wasm_equivalence.py -q` | 0 | | "15 passed in 1.94s" |
    | 09 | `python3 scripts/publication_guard.py tree` | 0 | | "publication-guard: the tree carries no placeholder and a final build record" |

    - The copy was still clean in tracked files afterwards.
    - Of the 33 skips, 16 are the CP-26 supervision stress tests, each skipped with the reason "CP-26 supervision stress test, run locally because a 4-vCPU CI runner cannot host it reliably, RUN_STRESS=1 forces it." They are 7 in `test_cp26_ledger_liveness.py`, 3 in `test_cp26_monitor.py` and 6 in `test_cp26_supervision.py`.
    - CP-28's one real-input test skipped with the reason "CP-26 local analysis outputs (.local/artifacts/cp-26/...) are absent; the note cannot be regenerated here" (`tests/cp28/test_cp28_gfs_note.py:50`).
    - CP-28's committed-result re-derivation tests (`tests/cp28/test_cp28_results.py`) ran and passed.
    - Log SHA-256 for step 05: `b606bedf08a67732231fd80b02f97cc4c689acc4ce07f56d3e840b5dd567481c`.

    **First attempt (harness error).** The Critic's first attempt (`S/ci312-attempt1/`, preserved) set `TMPDIR` to `S/ci312/tmp`. That directory is inside the primary repository's tree and outside the copy's `.git` sentinel. Step 05 then exited 1 with "1 failed, 2233 passed, 33 skipped": `tests/test_47_session_start_hook.py::test_the_hook_never_fails_outside_a_repository`. Its "outside a repository" `tmp_path` walked up into the primary PJM repository, so the hook printed that repository's state. Moving `TMPDIR` inside the sentinel, as the brief intends and as the Lead's runner does, fixed it. This was the Critic's misconfiguration, not a candidate defect.

**Reproduction step 5: the stress tests**

16. `S/run-ci.sh stress` runs on a fresh single-commit copy with the same tree. Its environment is the same as step 15's, with `CI` unset.
    - `uv sync --locked --dev` → exit 0; Python 3.12.14.
    - `uv run pytest -m stress -q -rs` → exit 0, "16 passed, 1 skipped, 2250 deselected in 189.35s". The one skip is the module-level import guard `tests/cp20/test_gfs_eccodes.py:11: could not import 'eccodes'`, which is not a stress test.

**Reproduction step 6: the diff**

17. `git -C W diff --stat main...HEAD` and `--name-only` (item 8 above) → only new CP-28 paths.

**The Critic's independent recomputation** (not in the brief's list; written from the protocol text, without importing `src/cp28`)

18. `python -I S/indep_check.py W <inputs> <origin>` at the origins 2021-03-06, 2022-03-12, 2023-11-15 and 2026-09-06 → exit 0 at each. The script reads the stored ledger and the snapshot, with the red line applied at read.
    - **Learning dates.** The independent learning dates equal `learning-days.csv` at each cutoff: 364, 728, 1,303 and 2,313.
    - **A3 and A4 grid fits.** The grid indices match at every origin, for A3 and for each of A4's three blocks. At 2026-09-06, A3 = (0.08, 0.29, 0.63) and A4 = night (0.42, 0.13, 0.45), solar (0.04, 0.43, 0.53), shoulder/peak (0, 0.30, 0.70). No near-ties. A3's deployed weights are 0.5·fit + 0.5·w0, A6 = the fit, and A4 = 0.25·block + 0.75·A3's deployed weights.
    - **A5 inputs.** The six error features and the scaler mean and SD are exactly equal.
    - **A5 network.** A from-scratch NumPy reimplementation of §5 (seed, 300 Adam updates, L2, sign subgradient) reproduces the stored parameters to between 1e-6 and 1e-9 at three origins.
      - At 2023-11-15 the parameters differ by up to 1.7e-3 and the output weights by up to 2.3e-3. With the registered combination arithmetic order (`S/indep_check_order.py`), that falls to 3e-5 and 8e-5. This is the expected floating-order sensitivity of a sign-subgradient fit, not a specification difference.
      - A5's deployed weights are 0.5·output + 0.5·w0, and A7 = the output.
    - **A2's H layer.** An independent 28-date buffer with pooled and hourly quantiles and n_h/(n_h+56) shrinkage gives emitted quantiles and a native central exactly equal to the committed ones at all four origins.
19. Inline Python on `results/daily-losses.parquet` and CP-26's `scores/daily.parquet`:
    - **A1 against CP-26's own DDNN-2 stream.** On the 2,050 native dates, A1's daily losses equal CP-26's `nominal/D2` (maximum relative difference 0 for MAE and 3.7e-16 for WIS). On the 18 fallback dates, A1's loss equals the copied v5 loss. CP-26's v5 and D2 were both B0 there.
    - **Startup arms against v5.** On the 67 startup scored dates, A3, A4, A5, A6 and A7 equal v5 to within 7.1e-15.
20. Inline Python recomputing HAC lag 14 and the one-sided p from the stored replicate statistics. The cases are A1 2025 MAE, A1 overall WIS, A7 2025 WIS, A1 DJF WIS (unstratified) and A6 2021 MAE (28-day).
    - T and p agree exactly. For example, A1 year 2025 MAE gives T = −2.4761806600 and p = 42/10001 = 0.0041996.
    - The smallest required-cell n is 359, and every overall n is 2,068.

## Evidence actually inspected

- **Specifications.** `capstone_v21.md` §24.8 at the candidate; the frozen protocol §§1–10 in full; the r17 supplement §§1–5 in full; the issued brief in full, including the Observable outcome, the landing-readiness items, the constraints, the Tools, and the Stop and return section; `docs/track-b/gauntlet-templates.md` §2; `publication-packet-template.md`.
- **Code read line by line:** `src/cp28/{reader,engine,grid,meta,states,scoring,inference,pipeline (validate, forecast, score, describe), gfs_note (inputs, differentials)}.py`; the landed `src/cp16/residuals.py` and the `src/cp25/guard.py` boundary.
- **Tests:** `tests/cp28/test_cp28_units.py` (the CP-26 draw and HAC reference test), `test_cp28_results.py`, and the skip guard in `test_cp28_gfs_note.py`.
- **Evidence records:** `docs/track-b/evidence/cp-28/{entry-identity.json, pre-score/causal-controls.md, causal-controls-tests.log (38 passed), scoring-validation.json, gfs-postresults/{note.md, provenance.json, resources.json, table.csv}, resources.json, lead-ci.md, lead-reproduction.json}`.
- **Forecast outputs:** `reports/cp28/forecast/*`, covering `arm-days` columns and counts, `fits` failures and ties, `h-traces` statuses, `features` and `issue-states` columns, and `cross-checks.json`.
- **Results and report:** `reports/cp28/results/{selection.json, compound.json, holm.csv, endpoints.parquet, bulk-manifest.json}`; `reports/cp28/report.md` in full; `owner-summary.json`; `publication-packet.md` and `.json`.
- **CP-26's tables:** `scores/daily.parquet`, its `nominal/D2` and `nominal/v5` streams.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1.1 | Members (c_HG = A1_w/2 + B2_w/2, L = mean(L-N, L-R), D2 median) and the control (nominal v5, w0 = (2/3, 1/6, 1/6), its interval layer) | PASS | `reader.parse_day`; c_HG is checked bit for bit against CP-26's v3 native central; independent member rebuild (cmds 18–19); the control's losses equal CP-26's to 3.4e-16 (cmd 12) |
| 1.2 | Construction: weights on centrals; each combined arm's quantiles come from HG's H layer re-estimated on its own issued central errors | PASS | `engine.run` uses one `cp16.SharedResidualState` per arm A2–A7, fed only that arm's central; A2's quantiles are independently exact (cmd 18); startup arms equal v5 to 7e-15 (cmd 19) |
| 1.3 | Native centrals stored before the outcome with that issuance's weights and scale; warm-up and D−2 own-error release on H-shortage fallback dates; missing members or solver failures create no central; copied fallback errors never enter H; emitted fallback scores stay fixed | PASS | `engine.run` issue/register order; `Truth` refuses dates after D−2; `state.issue` only for a valid native central on a complete day; 2,313 consumed errors per arm = 2,313 learning rows; 298 central-only errors per arm in warm-up; tests `test_copied_fallback_errors_never_enter…`, `test_valid_native_central_on_h_shortage…`, `test_hard_central_failures_never_enter` |
| 1.4 | Learned arms minimise mean daily central MAE | PASS | `grid.date_losses` and `window_objective` (equal date weights); `meta` loss with q = 1/(n·H_s); independent fits match (cmd 18) |
| 1.5 | A1 keeps DDNN-2's own Johnson SU quantiles | PASS | `d2_quantiles` require ordered, finite quantiles with q50 = D2's central; A1 equals CP-26's `nominal/D2` (cmd 19) |
| 1.6 | Ledger rule: s ≤ D−2, released once, forecast before outcome; D's forecast precedes D's outcome; CP-26's warm-up supplies the first days | PASS | `LearningLedger` pending/consumed; latest truth requested 2026-09-04 at origin 2026-09-06; first learning date 2020-02-29 from the 2020-01-01 warm-up; tests on target-day masking, D−1 and D−2, and duplicate release (38 passed before the forecasts) |
| 1.7 | Window: latest ≤ 728 complete released dates (minimum 364 or 728), separate from H's 28; partial keys never create a learning row; actual support decides startup | PASS | `ledger.window` vs `h[arm]._buffer`; `register` requires `complete` and all members valid; learning dates are identical to CP-26's stored learning ledger (2,313) and to the independent rebuild; 364 first reached at 2021-03-06 and 728 at 2022-03-12 |
| 1.8 | A1 rule | PASS | DDNN-2 alone, with its own quantiles; 2,050 native and 18 fallback |
| 1.9 | A2 rule | PASS | weights (1/3, 1/3, 1/3), with its own H; central exact (cmd 18) |
| 1.10 | A3 rule: 5,151-point grid, lexicographic order, minimum 364, latest 728, tie → integer distance to w0 then lowest index, deployed 0.5·fit + 0.5·w0, w0 before 364 | PASS | `grid.py`; unit tests on order and ties; 0 objective ties on the real run; independent indices at 4 origins; 67 scored `startup_w0` dates |
| 1.11 | A4 rule: per-block fits (night 22–05, solar 10–16, shoulder/peak 06–09 and 17–21), needing 728; 0.25·block + 0.75·A3 deployed; before 728, A3's deployed weights | PASS | `grid.BLOCK_HOURS`; `engine` A4 branch; independent block indices and deployment (cmd 18); rules on scored dates: `block_fitted_shrunk` 1,631, `a3_deployed` 370, `startup_w0` 67 |
| 1.12 | A5 specification: 16 issue-time inputs in order, softmax per day and block, 8 tanh units, block MAE loss, full-batch Adam (lr 0.01, 300 updates, L2 1e-3 on weights), seed `SeedSequence([28, D.toordinal(), 0x4D4C])`, daily refit from scratch on ≤ 728 dates (minimum 364), window-only weighted standardisation, unknown volatility = not high plus flag, β and ε values, N(0, 0.1) weights, zero biases; deployed 0.5·out + 0.5·w0 | PASS | `meta.py`, `engine.date_features`, `states.py`; issue-time states agree with CP-26's on all 2,078 dates (`cross-checks.json`); independent reimplementation matches (cmd 18); finite-difference gradient test |
| 1.13 | A6 rule: A3's fit, unshrunk, with the same window, minimum and ties; w0 before 364 | PASS | shares A3's fit (`deployed['A6'] = a3['weights']`); verified at 4 origins |
| 1.14 | A7 rule: A5's network output as it is; w0 before 364 | PASS | shares A5's fit and scaler; verified at 4 origins |
| 1.15 | Further fixed details: learned-arm training rows need all three members; A6 and A7 share fits; no outcome-dependent detail | PASS | `register` requires all members valid; protocol §§4–5 matched line by line |
| 1.16 | Failures hierarchy (missing member → v5's complete forecast → B0; solver failure → A2's complete forecast; no renormalising; every fallback counted) | PASS | `engine.fallback` and its branches; 18 `member_invalid` fallbacks per arm, scored as emitted and counted by source and reason in the report and owner summary; 0 solver or numeric failures; the 10 scored dates with no CP-25 eligible keys are recorded as `no_scoring_keys` |
| 1.17 | The twenty endpoints: improvement 0.995 overall on MAE and WIS; non-inferiority 1.02 in each year 2021–2025 and each season, MAE and WIS; cells under 90 inconclusive | PASS | `inference.endpoints` (20 per arm); 560 rows, all computable; minimum cell n 359; independent T and p (cmd 20) |
| 1.18 | Compound p = maximum of the twenty; Holm across seven at α = 0.05 | PASS | `run_variant` and `holm` (threshold 0.05/(8−j), monotone adjusted p); `holm.csv` checked by hand: every arm rejected in every variant |
| 1.19 | Three sensitivity variants (7-day, 28-day, unstratified 14-day); a primary pass that fails a variant is inconclusive | PASS | `VARIANTS`; fresh `default_rng(20261012)` per variant; draw plan and HAC equal CP-26's reference (unit test); all four analyses pass all seven arms; inconclusive = none |
| 1.20 | Disclosures in advance (A4 = A3 until 728, observed startup and span, learned arms equal v5 until their minimum, A6 and A7 unshrunk, Holm conditional on the Owner's decision) | PASS | `report.md` § Startup and § Disclosures |
| 1.21 | Selection: lowest WIS among passing arms; tie when WIS < 1.005·best; simplicity order A1, A2, A3, A6, A4, A5, A7; control if none passes | PASS | `inference.select`: A1 9.6825 against a bound of 9.7309; next lowest A6 10.1294; tie set {A1}; A1 selected |
| 1.22 | One look; no arm added; p = 1 for any failed or unexecuted arm | PASS | `forecast` refuses if scores exist and `score` refuses to overwrite; the ledger has exactly one forecast job and one score job before their commits; no forecast or score code changed after `22233e4`; the p = 1 paths are tested; no arm failed |
| 1.23 | Evidence class `development_post_selection` | PASS | `report.md`, packet, note |
| 2.1 | Frozen protocol §§1–9 where they fix a detail | PASS | §1 entry binding (`entry-identity.json` = tag blobs, cmd 7); §2 calendar, DST and issue time; §4 integer distance and equal date weights; §5 features (prefix rules, D−1 price as predictor), scaler, Adam; §6 H with the issuance scale and 14-date/56 shrinkage; §7 hierarchy; §8 WIS formula and tie rule; §9 runs, strata (2020-12-29..31 joined to 2021), non-circular blocks, HAC, centred null, (1+count)/(R+1) |
| 2.2 | Protocol §10 retention list | PASS | `forecast/` holds weights, fit identifiers, window positions and hash, scaler and parameters in `networks.npz`, feature support, state support, seeds and hashes, native centrals, emitted quantiles, statuses, H provenance and span; `results/` holds daily losses, paired masks (runs), 20×7×4 p-values, compound and Holm, selection calculation; draws and pivots in bulk |
| 2.3 | §10 causal controls proved before any scored run, with positive and negative controls | PASS | `pre-score/causal-controls.md` maps every §10 control to a test; the log (38 passed) was committed in `22233e4` at 19:14:40Z, before the forecast started at 19:14:47Z |
| 2.4 | Commit order: GFS note → pre-score controls → forecasts → scores | PASS | `9165c77` → `22233e4` → `b5bfd8e` → `b627c86` (cmd 9) |
| 3 | r17 GFS note: descriptive only (no fit, search, replay, recalibration or new bootstrap); own directory; short note and small table; committed before any arm was fit or scored | PASS | `gfs_note.py` has no RNG, fit or test, and reuses only CP-26's registered v5 intervals, guarded by equal pairs and difference; `gfs-postresults/` holds a 260-line note and a 172-row CSV; it reproduces byte for byte (cmd 14); committed 18:52Z, before `22233e4` |
| 4 | Observable outcome, including the Owner's CP-17 summary | PASS | report and draft packet (DRAFT_LOCAL, INCOMPLETE as a publication); `owner-summary.json` carries the selected A1, scores against the control and B0 with intervals, Holm and sensitivity, startup and fallback counts, and the GFS headline |
| 5.1 | GitHub-landable as is | PASS | 53 new files only; no LFS or curated landing needed |
| 5.2 | No committed file at or over 50 MB | PASS | maximum 23.7 MB (cmd 8); test enforces < 50 MB |
| 5.3 | Bulk retention manifest-listed with size and SHA-256 | PASS | `bulk-manifest.json` lists 29 files; the Lead's bulk matches on size and SHA-256; the Critic's rerun arrays are identical (cmd 13) |
| 5.4 | CI-ready on a history-free single-commit copy (`CI=true`, Python 3.12, all seven workflow steps) | PASS | cmd 15: all seven exit 0, plus the two version probes. The first attempt's single failure was the Critic's `TMPDIR` placement, as recorded under cmd 15 |
| 5.5 | `pytest -m stress` passes locally | PASS | cmd 16: 16 passed |
| 5.6 | No test depends on branch history, tags or the local-only inputs | PASS | CI copy has one commit, no tags and no `.local` inputs; 2,234 passed |
| 5.7 | Real-input tests skip with a stated reason when inputs are absent | PASS | `test_cp28_gfs_note.py:50` skip reason as quoted under cmd 15 |
| 5.8 | Unit tests use synthetic fixtures | PASS | `tests/cp28_synthetic.py`; units, causal controls and pipeline tests are synthetic |
| 5.9 | No pinned file changed: diff touches only new CP-28 paths; `src/cp26/harness.py` PINS and earlier evidence untouched | PASS | cmd 8: every path `A`, `src/cp26` unchanged, `reports/rebaseline` unchanged |
| 6.1 | No retrieval and no remote write | PASS | no network import in `src/cp28`; MLflow export is a local JSON draft; `UV_OFFLINE=1` throughout the Critic's runs; nothing pushed |
| 6.2 | Red line: nothing after 2026-09-06 is read | PASS | `reader.prices` filters at `guard.BOUNDARY` (2026-09-06) and calls `admit_rows`; ledger days pass `admit_delivery_day`; `Truth` stops at D−2; latest truth 2026-09-04 |
| 6.3 | Forbidden paths unchanged | PASS | cmd 8 `git diff --quiet` over the full list exited 0; `pyproject.toml` and `uv.lock` hashes as pinned |
| R1 | Reproduction 1 (`tests/cp28`, real inputs present) | PASS | 45 passed, 0 skipped |
| R2 | Reproduction 2 (full rerun: bytes, `networks.npz` arrays, p-values, Holm, selection) | PASS | cmd 13 "OVERALL MATCH"; differences only in the permitted timing fields |
| R3 | Reproduction 3 (r17 note byte for byte) | PASS | cmd 14 |
| R4 | Reproduction 4 (history-free CI) | PASS | cmd 15 (second, correctly isolated run) |
| R5 | Reproduction 5 (stress) | PASS | cmd 16 |
| R6 | Reproduction 6 (diff scope) | PASS | cmd 8 / 17 |

**Result:** A1 (DDNN-2 alone, with its own Johnson SU quantiles) is the selected CP-17 freeze candidate.

- **A1 against the control,** on the same 2,068 paired dates:
  - MAE 17.187 against 18.460 EUR/MWh, −6.9% (descriptive 95%: −9.1% to −5.1%);
  - WIS 9.683 against 10.871, −10.9% (−12.9% to −9.0%).
- **Holm and sensitivity:** all seven arms pass Holm in all four analyses. A1's compound p is 0.0042 in the primary analysis, 0.0069 with 7-day blocks, 0.0022 with 28-day blocks and 0.0053 unstratified.

**Non-blocking observations**

- **Draft packet.** The draft publication packet compresses the template's §§6–8. It has no surface-receipt table, and its checks list omits the export-contract and §4 lint items. It says it is DRAFT_LOCAL and INCOMPLETE, and CP-28 publishes nothing, so this is acceptable for a draft. Any later publication task must complete it.
- **Network reproduction.** A5 and A7's daily refits are reproducible bit for bit only under the committed arithmetic order. An independent reimplementation moves the output weights by up to about 1e-4 to 2e-3, as observed at one origin. This is inherent to the registered sign-subgradient fit and does not affect any decision recorded here.

## On FAIL only
- Single largest meaningful gap: not applicable (PASS).
- Exact next acceptance test: not applicable (PASS).
