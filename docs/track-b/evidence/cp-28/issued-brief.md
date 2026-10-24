# Track B Checkpoint Brief — CP-28 (4.8 on stored forecasts: seven arms against the control, after r17's no-training GFS note)

*Issued by the Orchestrator on 2026-10-24, Asia/Jerusalem.*

## Target
- Repository: DE-LU day-ahead forecasting, `/Users/djourno/Downloads/PJM` (origin
  `hrsi56/delu-day-ahead-forecast`). The checkpoint runs locally, in the Lead's own worktree.
- Authorized checkpoint: CP-28, exactly one.
- Ratified plan anchor: `capstone_v21.md`, revision v21-r17, §24.8, SHA-256
  `3124451da84c3cd99fae728c371207aace6ae537474f7769d0ff6333ee53e4fc`. On `main` the section is
  135 lines and 8,224 bytes, with section SHA-256
  `5eaaa7c8ee418e1b4dc0029ccb66c862f3b6bc7fca1bbc451c4850bd39d84d26`.
  - **§24.8 is governed by:**
    - §24.2: the boundary, the guard, the exposure ledger and the audit standard;
    - §24.4: the issue time;
    - §24.5: the control and the Owner's rulings;
    - §24.7: CP-26's stored ledger and its frozen protocol;
    - §24.9: CP-17 follows.

    It inherits §2's released-error rule and target-day embargo.
  - **CP-28's frozen protocol,** registered outcome-blind in CP-26:
    `docs/track-b/evidence/cp-26/cp28-frozen-protocol-v21-r14.md`, SHA-256
    `2b9286b0e948f59f97de33315a8b4fb3ef121003fc4ba82355b1ccf6585497a8`. It governs every detail
    §24.8 leaves open. `cp28-frozen-protocol.md` stays historical.
  - **The post-results supplement (v21-r17)** runs before the experiment:
    `docs/track-b/evidence/cp-26/cp28-gfs-postresults-addendum-v21-r17.md`, SHA-256
    `39f322afa9717c5cfb0b626a1a8430fa9f5fcc0dfdd159123b9d4b48e7db03b4`. Its authority is the
    Owner's GFS ruling, `docs/track-b/cp-26-gfs-ruling-2026-10-19.md`, SHA-256
    `3b97ff6abdf9a30ddd8c950cf3c459301d757aa1af08f6d8121bc73f92ba2373`.
  - **The Owner's tier and margin rulings:** `docs/track-b/cp-25-rulings-2026-10-12.md`, SHA-256
    `c7af67f88157277aafd8dd2b1b49e12a1d9ff4b747ca5bdf178fac664fba53c1`.
  - **The publication anchor** is PUBLISH_RULES 1.5, SHA-256
    `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`, for the draft packet only.
    CP-28 publishes nothing.
- **The Owner's confirmation that CP-28 runs** (§24.2's audit standard: it rests only on CP-26's
  report, its resources and §24.8). Given on 2026-10-19, after CP-26's report: "בסדר גמור אני מאשר
  לך לעשות הכל. תן לי פקודות לland ונתקדם לCP-28". It is recorded in
  `docs/track-b/cp-26-landing-2026-10-21.md` (SHA-256
  `402e0a3f2ab90590ae0eebf908b0408c074f4305837103db55758916c095c03c`).

## Orchestrator-reported expected state
- **Branch / commit:** `main` = `origin/main` at the commit that records CP-28's issue.
  - It is a direct child of `a9be03a0f5036db4cc828e359f0f05f323875eed`, CP-26-CI's closure, and
    changes only `progress.md`.
  - **Tags:** `land/cp-26` = `61658c7`, and `evidence/cp-26` = `ca20331`, which is **local-only and
    never pushed**. Also `land/cp-26-ci` = `e4a02df` and `evidence/cp-26-ci` = `644ac1a`.
  - **Branches and worktrees:** none besides `main` and the primary checkout.
- **Working tree:** the primary checkout `/Users/djourno/Downloads/PJM` is on `main` and clean
  apart from ignored material.
  - **The Orchestrator uses it during CP-28.** Never switch its branch, and never write a tracked
    file in it. Your only writes there are under:
    - `.local/artifacts/cp-28/`: the tools' state, ledgers, logs, caches and extracted inputs;
    - `.local/tmp/cp-28/`;
    - the worktrees under `.local/worktrees/cp-28/`.
  - **The canonical brief** is `.local/artifacts/cp-28/issued-brief.md`. Package that file byte for
    byte, not the pasted text.
- **What already exists:**
  - **CP-26's landed outputs on `main`,** in `reports/rebaseline/cold-rerun-2026-10-15/`:
    - the report;
    - `presentation-v21-r16/`;
    - the publication packet draft;
    - `execution-manifest.json`, `diagnostics-manifest.json` and `scores-manifest.json`
      (`b9f10917…f84d`). The last one's `forecast_ledger` binds the stored ledger.
  - **CP-26's stored member forecasts are not on `main`.** That is the curated landing, recorded in
    `docs/track-b/cp-26-landing-2026-10-21.md` and `docs/track-b/evidence/cp-26/landing-omitted-files.tsv`.
    - **Where they are:** `reports/rebaseline/cold-rerun-2026-10-15/forecast-ledger/` (2,441 files,
      1.09 GB) and the learning ledger exist only in the local tag `evidence/cp-26`.
    - **How to read them, read-only, into `.local/artifacts/cp-28/inputs/`:**
      `git -C /Users/djourno/Downloads/PJM archive evidence/cp-26 <path> | tar -x -C <dir>`.
    - **Bind them before any use:** check every file against `git ls-tree -r evidence/cp-26` and
      `scores-manifest.json`, and record the identity at entry (protocol §1).
    - **Never commit them** to `gauntlet/cp-28`.
  - **CP-26's local stored analysis outputs,** which are not in Git, are in
    `.local/artifacts/cp-26/cold-rerun-2026-10-15/r16/final-analysis-inputs/reports/rebaseline/cold-rerun-2026-10-15/`:
    - `report.json` (`1b1aa805…56d8`), with `inference_endpoints` and `diagnostic_tables`;
    - `scores/hourly.parquet` (`f465d5e7…e709`);
    - the inference and diagnostics manifests.

    They are read-only. Bind them by these hashes and by `scores-manifest.json`.
  - **The bootstrap and diagnostics replicate folders exist only on the Owner's backup drive**
    (`docs/track-b/backup-register.md`). The supplement uses the summaries in `report.json`. If any
    task needs the replicates, return BLOCKED; never recompute them.
  - **CP-25's frozen inputs** are in `reports/development-inputs/`: the calendar, the masks, the tier
    register and the GFS +6 h affected-date classification.
  - **The code:**
    - **`src/cp26/` is landed code.** Its live identity guards refuse under r17 by design (CP-26's
      landing record). Never call them, and never edit `src/cp26/`.
    - **Write CP-28 in `src/cp28/`,** with its own read-only reader of CP-26's stored outputs that
      verifies hashes against the committed manifests.
  - **The exposure ledger** is `docs/track-b/exposure-ledger.md`. The Orchestrator keeps it; report
    any exposure in your return. CP-26's rows are frozen in
    `docs/track-b/evidence/cp-26/exposure-ledger-frozen.md`.
  - **The backup register,** `docs/track-b/backup-register.md`, is locked. Never edit it.
  - **The tools:** `scripts/gauntlet.py` and `scripts/bar.py`. CP-26's supervision stress tests carry
    the `stress` marker and skip only when `CI=true`.
- Verify this yourself before relying on it, and report any material mismatch.

## Observable outcome
CP-28 closes with the following, bound by one fresh Integration-Critic PASS:

1. **First, the r17 GFS note,** exactly as the supplement specifies.
   - It is descriptive: no fit, search, replay, recalibration or new bootstrap.
   - It goes in its own evidence directory, `docs/track-b/evidence/cp-28/gfs-postresults/`, with a
     short note and a small machine-readable table.
   - It is committed before any CP-28 arm is fit or any CP-28 score is computed.
2. **The seven-arm experiment,** under §24.8 and the frozen protocol:
   - the causal controls of protocol §10, proven before any scored run;
   - then one look: every arm's daily causal forecasts on CP-26's nominal ledger;
   - the twenty endpoints per arm, the compound p-values, and Holm across seven arms at α = 0.05;
   - the three sensitivity variants;
   - the selection: the winner, or the control.
3. **The retention record** of protocol §10.
4. **The report,** and a draft publication packet under PUBLISH_RULES 1.5. It is a draft only.

A complete result in which no arm passes, so that the control becomes the freeze candidate, is a
valid PASS. **The return carries the Owner's CP-17 summary:**
- the selected candidate or the retained control;
- its scores against the control and B0;
- the Holm and sensitivity decisions;
- the startup and fallback counts;
- the GFS note's headline.

## Complete authoritative checkpoint bar
`capstone_v21.md` v21-r17 §24.8, "CP-28: 4.8 on stored forecasts (stage 8)": every item. It is
governed by the sections named in Target, the frozen protocol and the supplement (both bound by
hash above).

Verbatim, extracted with `scripts/bar.py bar` from the anchor at `a9be03a`:

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

**Landing-readiness items,** which bind this candidate as well. Each is a lesson from CP-26:

1. **GitHub-landable as is.**
   - No committed file is over 50 MB, so that the evidence tip itself can be pushed with no curated
     landing.
   - Bulk retention, such as stored bootstrap draws, stays in `.local/artifacts/cp-28/`. A committed
     manifest lists each file's size and SHA-256.
2. **CI-ready.** The workflow's seven steps (`.github/workflows/tests.yml`) are green on a
   history-free single-commit copy of the candidate, with `CI=true` and Python 3.12, and
   `pytest -m stress` passes locally.
   - **No test depends on** branch history, tags, or the local-only inputs above.
   - **Tests over the real stored inputs** skip with a stated reason when those inputs are absent.
   - **Unit tests use synthetic fixtures.**
3. **No pinned file changes.** Before editing any tracked file outside `src/cp28/`, `tests/` (new
   CP-28 files) and `docs/track-b/evidence/cp-28/`, check that no earlier evidence binds its bytes.
   That includes `src/cp26/harness.py`'s `PINS`.
4. **The Integration Critic runs the whole suite,** not a subset: the history-free `CI=true`
   Python 3.12 sequence, plus `pytest -m stress`.

## Task-specific supporting extract
- **The ceiling is 40 machine-hours** (§24.8's proposal, granted by the Owner's delivery of this
  brief), summed over workers' wall time.
  - At most 4 concurrent workers, BLAS 1, CPU only, peak memory 12 GB, no cloud and no GPU.
  - The supplement uses one worker, about one hour, and is charged to the same ledger.
- **"The first score"** means the first computation of any evaluation metric of a CP-28 arm on a
  scored-calendar day: a loss, coverage, a ratio or a test. Reading CP-26's stored scores for the
  supplement is not a CP-28 score.
- **There is one look.** After the first CP-28 score, no arm is rerun, re-specified or added. An
  operational resume from committed state is not a rerun. An arm that fails or cannot run counts
  with p = 1.
- **A deficiency in the protocol** is returned as BLOCKED before scoring, never repaired from
  CP-26's outcomes (protocol §10).

## Applicable constraints
- **No retrieval of any kind:** 0 data bytes and 0 remote writes. Every input is local. Any MLflow
  export is a local draft, never uploaded.
- **The red line (§24.2).** No delivery day after 2026-09-06 is read. Do not read, record or mention
  any market value or event after 2026-09-06.
- **Files that never change:**
  - `data/` and `reports/development-inputs/`;
  - CP-26's `reports/rebaseline/` outputs, and every other file that earlier evidence binds;
  - the landed code in `src/delu_forecast/`, `src/cp15/` to `src/cp26/`;
  - the root `pyproject.toml` (`aa35326a…4e4a`) and `uv.lock` (`5d2aecc3…a94`). CP-28 is NumPy-only,
    per §24.8;
  - the anchors and amendment records, `AGENTS.md`, the role files, the exposure ledger and the
    backup register.
- **Long computation** may run unattended in the background, within the ceiling, under your
  ledger. Commit work in progress on `gauntlet/cp-28` at every stage boundary. A usage limit can stop
  you at any moment, and you resume from your last commit and ledgers.
- **Credentials** follow `AGENTS.md` § Credentials; none is needed. Export
  `MLFLOW_DISABLE_TELEMETRY=true` and `DO_NOT_TRACK=1` for any MLflow job.
- **Pinned identities:** every hash above, and the packet template
  `docs/track-b/publication-packet-template.md`
  (`4049c3e1f695034ec45fa185d465fce05ab1183cbded72188306579d7287d01a`).
- **Tools:**
  1. run `scripts/gauntlet.py start cp-28` first, from the primary checkout;
  2. create your worktree with
     `git -C /Users/djourno/Downloads/PJM worktree add -b gauntlet/cp-28 .local/worktrees/cp-28/lead main`;
  3. launch the one Critic with `critic-open`, `critic-brief` and `critic-close`. If you cannot
     start a subagent, end your turn with `critic-open`'s output and ask the Orchestrator to launch
     the Critic with exactly the printed prompt;
  4. check the return with `scripts/gauntlet.py return`.
- **Memory:** do not open or edit the files in the Claude memory directory
  (`~/.claude/projects/-Users-djourno-Downloads-PJM/memory/`). Its auto-loaded index informs no
  decision.
- **Owner-facing Git commands** must be non-interactive: `git --no-pager …` and
  `git commit -F <file>`.

## Timebox
About 25 active hours from orientation to the terminal return. Unattended computation within the
40-machine-hour ceiling runs alongside and is not counted as active hours.

## Owner-only actions already authorized
- **CP-28's execution** under v21-r17 §24.8, the frozen protocol, the supplement and this brief. The
  Owner's delivery of this brief is his grant (§24.10), including the 40-machine-hour ceiling. It
  covers local `gauntlet/cp-28` candidate and evidence commits in your worktree, and the exact
  packaging of this brief.
- **Nothing else:** no retrieval, mainline operation, push, tag, publication, remote write, MLflow
  upload or governance edit.

## Stop and return
- **First commit.** The first commit on `gauntlet/cp-28` copies the canonical brief byte for byte to
  `docs/track-b/evidence/cp-28/issued-brief.md`.
- **The return.** Return exactly one of PASS / BLOCKED / INCOMPLETE, using templates §3. It
  carries both terminal SHAs and the verdict-only delta, checked with `scripts/gauntlet.py return`.
  - Its "Open risk or exact owner action" section gives the Owner's CP-17 summary from Observable
    outcome.
  - Name any exposure (§24.2), and any interview-answer trigger, in one line each.
- **Do not** begin CP-17 or 4.7T. Do not commit to `main`, publish or push. Leave your worktree and
  branch for the Owner's LAND and the Orchestrator's reclamation.
