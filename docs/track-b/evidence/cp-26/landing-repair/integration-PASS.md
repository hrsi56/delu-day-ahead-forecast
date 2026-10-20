# Verdict — CP-26 — Integration — PASS

- Candidate SHA: `04f00eac5506c550ed4c775b84dc65a41f86c007` (`gauntlet/cp-26`; prior evidence tip `d8f912ad9be0867f11e4b634c2f482792ea5e951`; `main` `647d6eb81b2cf6e0cfaf4152f659d689ff973578`).
- Plan / version / bar: `capstone_v21.md`, **v21-r17** (SHA-256 `3124451da84c3cd99fae728c371207aace6ae537474f7769d0ff6333ee53e4fc` at the candidate), `### 24.7 CP-26: the re-baseline on every development day (stage 6)` (250 lines, 15,129 bytes, section SHA-256 `423527d92156e47742c0aba593f04b08334e7a9b526f0dbc6208a3c38dcf5b1e`). The bar judged for this candidate is the issued landing-repair brief's five items (`docs/track-b/evidence/cp-26/landing-repair-brief.md`, SHA-256 `27d3e1afbdcc5f02b88b27f59ed4935ac8bc99918ea8c58124e0cdbb3bd89e3d`) and its observable outcome on history, exclusions and untracked outputs. This is a focused landing-repair review; §24.7's science was not re-reviewed, only confirmed unchanged.
- Verbatim bar excerpt: the two quoted blocks below (§24.7 at the candidate, then the brief's bar and outcome clause at the candidate).
  (The excerpt is the citation. Any line number is a courtesy and is non-binding.)
- Worktree clean before and after: **yes**. `/Users/djourno/Downloads/PJM/.local/worktrees/cp-26/critic-2`, `git status --porcelain` empty and `HEAD` = `04f00eac5506c550ed4c775b84dc65a41f86c007` at the start, after the full-tree suite run, immediately before writing this verdict, and again after writing it (with `bar.py check` of this file against both sources: 3 of 3 quoted blocks ok). Only Finder `.DS_Store` files appear as ignored entries. Isolation is cooperative and procedural: no read-only mount was available. No Git write was made.

**§24.7 at the candidate** (confirmed with `bar.py bar … --at 04f00ea… --quote`, and byte-equal to the excerpt in the generated brief):

> ### 24.7 CP-26: the re-baseline on every development day (stage 6)
>
> **Purpose:** run B0, v1-R and v2–v5 daily on every eligible development day under one protocol.
> The result is the new all-season baseline, and a stored ledger of every member's out-of-sample
> forecasts for CP-28 and 4.7T.
>
> #### Days
>
> - **The scored calendar:** delivery days 2020-12-29 to 2026-09-06, 2,078 calendar days, less
>   CP-25's frozen exclusions.
> - **The warm-up:** delivery days 2020-01-01 to 2020-12-28, forecast the same way and never scored.
>   It only fills interval buffers and CP-28's first ledger.
> - **Four masks are reported separately:**
>   - every eligible day;
>   - the days never scored before (CP-25's mask);
>   - the old-fold days, folds 2–5, re-run under this protocol;
>   - 2026-04-08 to 2026-09-06, newly opened and used earlier by v1.
>
>   The old five-fold results, their S_MAE and S_WIS and their uncertainty stay as the historical
>   record, never overwritten.
>
> #### Policies
>
> - **B0,** the similar-day naive, unchanged.
> - **v1-R (728-day window, no hindsight regime flags):** the released v1 recipe, refit daily, with
>   two declared method changes:
>   - `crisis_period` and `post_crisis` are removed (§24.5);
>   - the training window is 728 days, where v1 expanded from 2019-01-01.
>
>   The rest of the recipe is the `base` catalog, the nine LightGBM quantile heads, CQR, and isotonic
>   ordering, laid out for each origin D as follows:
>   - the heads train on `[max(2019-01-01, D−728), D−62)`;
>   - day D−62 is an embargo;
>   - CQR calibrates on D−61 to D−2;
>   - day D−1 is an embargo.
>   - The thread count follows the worker's allotment; that is not a method change.
>   - **The released artifact** is reported descriptively, on its holdout days only: 2026-06-09 to
>     2026-09-06.
>   - If v1-R cannot be built without a further method change, CP-26 reports v1 through the released
>     artifact and B1's preserved vectors on the old folds, and says so.
> - **v2, v3, v4 and v5,** through the harness below: their landed member code, fixed blend weights,
>   interval layers, seeds and inner tuning rules, unchanged. Only the data identity, the boundary,
>   the weather source, the issue time and the calendar follow this section.
>   - **A tier-3 ruling** may name a variant, built only by the ruling's declared changes (§24.5).
> - **DDNN-2 alone** is descriptive in CP-26. It is a CP-28 arm (§24.8).
>
> #### The harness and the parity gate
>
> - **The harness.** The landed code refuses any snapshot, boundary or anchor other than its own
>   (`src/cp15/data.py`, `src/cp20/inputs.py`, `src/cp24/inputs.py`). CP-26 therefore builds a
>   harness that imports the landed member code unchanged and replaces only:
>   - the data identity: the new partition specification and CP-25's manifest;
>   - the boundary;
>   - the weather source: CP-20's grids plus CP-25's;
>   - the issue-time label;
>   - the identity pins: the protocol revision, the anchor and issued-document hashes, and the lineage
>     checks. Each replaced pin is listed in the harness log.
> - **The parity gate, before the full run.** Under the old settings (11:00 UTC, the old identity and
>   boundary), the harness reproduces the committed central vectors bitwise at sampled old-fold
>   origins:
>   - for A1, B2, A1_w, B2_w, L-N and L-R;
>   - for D2, on CP-24's committed ensembles. Those ensembles check parity only, and never serve a
>     CP-26 forecast;
>   - for B0, and for the assembled v2–v5 central vectors.
>
>   If parity fails, the Lead stops and reports.
>
> #### DDNN-2's training-only search, for CP-26
>
> - **Search dates:** S_k = 2020-01-15 + 182k days, for k = 0 to 13. Search k serves only the origins
>   from S_k up to the day before S_(k+1). Before S_0 there is no native D2 forecast.
> - **The batches:** consecutive 28-day blocks, tiling backward from S_k − 1.
>   - Among blocks starting on or after 2019-07-01, keep up to the 11 newest eligible blocks.
>   - Use exactly the landed DDNN-2 support mask, complete-calendar-week pool and 20% holdout-week
>     count, retaining its exclusion of the most recent seven days. Let N be the supported window
>     days and m the fixed held-out week count. Minimum training support is N minus the sum of the
>     m largest week supports; minimum holdout support is the sum of the m smallest. Accept only
>     minima at least 250 and 14 respectively. Eligibility must hold for every possible split.
>   - Lists depend only on support, are shared by every configuration in a search and are signed
>     before fitting. No seed, loss or convergence filters them. B is computed, never hard-coded:
>     the expected reproduction is [1,7,11,…,11], with first block 2019-12-18..2020-01-14 and minima
>     251/46. The algorithm and frozen inputs govern if a reported count disagrees.
>   - There is no fold skip rule: every block lies before the search's first origin.
> - **One fit per trial and batch,** on `[max(2019-01-01, b − 728), b)`.
> - **The sampler:** seeded with `SeedSequence([26, k, 0x5A3])`, with 128 trials. Successive halving,
>   the ranking metric and the tie rule follow §23.4.
> - **Frozen fit seeds:** trial/batch seed = `26_000_000 + k*100_000 + trial*100 + batch`,
>   trial=0..127 and retained batch=0..10, newest first. Ensemble member seed =
>   `26_000_000 + k*100_000 + 90_000 + 10*rank + repeat`, rank=1..4 and repeat=1..2.
>   These disjoint domains are fixed before fitting and shared across the three routes; no retries
>   with replacement seeds. Sampling space/priors remain the landed permitted space.
> - **The ensemble:** four best distinct effective configurations, two seeds each, exactly eight
>   members. Effective identity excludes trial id; in the no-load variant it also excludes removed
>   load flags. Duplicates consume trials; no extra sampling compensates for them. A configuration
>   failing a required batch cannot rank over all batches.
> - **Search failure:** zero eligible blocks or fewer than four valid effective configurations is
>   recorded. D2 is unavailable throughout that search's service period; the next search remains
>   on schedule. Never extend an earlier ensemble or relax a threshold. One failed daily member
>   invalidates D2 for that date: no median of a successful subset.
> - **CP-24's ensembles are never reused** for a CP-26 forecast.
>
> #### Training and information
>
> - **A daily refit** at every origin, for every member, on `[max(2019-01-01, D−728), D)`, filtered
>   by availability at the issue time. For every scored day the window is exactly 728 days.
> - **A training target enters only once its price was published** before the issue time.
> - **No expanding-window sensitivity** is run under the short path.
>
> #### Scores
>
> - **Primary:**
>   - p50 MAE, and the seven-quantile WIS (50/80/95% intervals, weights α/2, median weight 1/2,
>     divided by 3.5);
>   - each day's loss is the mean over its actual hours, and days weigh equally;
>   - the B0 ratio is the policy's mean daily loss over B0's, reported beside the raw losses.
> - **Secondary:**
>   - the mean of the four pooled-season ratios;
>   - the mean of the five complete-year ratios, 2021 to 2025;
>   - 2020 and 2026, both partial, reported separately; quarters descriptive.
> - **Calibration, descriptive:**
>   - 50/80/95% coverage, the lower and upper exceedance rates and the widths;
>   - quantile hits, and the eight-bin quantile histogram;
>   - Christoffersen's tests;
>   - the memo's moment-test family (HAC lag 14, 100,000 replicates, seed 20261013, Holm at 5%), as
>     a diagnostic only.
> - **Registered breakdowns:**
>   - season (DJF, MAM, JJA, SON);
>   - year and quarter;
>   - local hour;
>   - day type: weekday or weekend, the nationwide holiday flag, and 23-, 24- and 25-hour days;
>   - the 2021–2022 stress label, descriptive;
>   - two states known at the issue time:
>     - negative-price risk: any negative hour in the last 7 fully known delivery days;
>     - high volatility: the standard deviation of the last 28 fully known daily mean prices is above
>       the 90th percentile of the previous 365 such values, using linear percentiles and a strict
>       comparison;
>   - realized-outcome slices, descriptive only.
>
> #### Inference
>
> - **The bootstrap:**
>   - paired, non-circular moving blocks of 14 calendar days, 10,000 replicates, seed 20261012;
>   - drawn within calendar-year strata (the three 2020 days join 2021; 2026 is a partial stratum),
>     never across a real gap;
>   - studentized, with Bartlett HAC at lag 14.
> - **Sensitivity:** 7- and 28-day blocks, and an unstratified 14-day variant.
> - **Secondary tests:**
>   - Diebold–Mariano on daily losses;
>   - Giacomini–White, with these instruments: a constant, the lag-1 differential, a weekend flag,
>     and the two states above;
>   - the 90% Model Confidence Set, descriptive.
>
> #### Failures
>
> - **A failed fit or forecast** is scored, on that day, with B0's forecast as the policy's fallback.
>   Fallback days are counted and reported by policy.
> - **If B0's own inputs are also unavailable,** the policy fails that day. The failure is counted,
>   and the day is scored as missing in every paired comparison involving that policy.
> - **Separate four statuses on every date:** native-central validity, interval readiness, source
>   of the emitted/scored output, and eligibility of the issuance for a complete-day own error.
>   A valid native central and required issuance scale may be stored before its outcome even
>   when fewer than 28 complete released own-error dates force a scored fallback. Its own error
>   may enter once, after complete D−2 release. This applies in warm-up and recovery in measurement.
>   The emitted fallback remains scored and counted as fallback; never revise it retrospectively.
> - **This exception is only for insufficient interval history.** Member, solver, identity, required
>   scale or numerical H-construction failure admits no own error. Copied fallback errors, another
>   policy's errors and forecasts constructed after the outcome never enter. v2–v5 and variants
>   retain their landed H recipe and blend weights; gaps lengthen the represented calendar span.
> - **B0 retains raw own errors**, with no A1-scale requirement. Warm-up may issue central only.
>   In measurement, if its own valid quantiles are unavailable, B0 has no fallback to itself:
>   retain a missing output under paired-comparison rules while a valid pre-outcome native central
>   continues warming its own raw-error buffer. v1-R retains nine heads, embargoes and CQR;
>   it never substitutes an issued-error H buffer for CQR.
> - **If a main policy's fallback days exceed 1% of the calendar,** the Lead reports before CP-28.
>   Every main policy counts, including a tier-3 variant. Delay runs and the revision-contaminated
>   as-landed policies are reported separately.
> - **No day leaves the calendar** after scoring.
>
> #### What CP-26 claims
>
> - **It is a control audit.** For each adopted transition (v2 → v3, v3 → v4, v4 → v5) it reports
>   the paired differences, the ratio intervals and the year and season breakdowns, all
>   descriptive.
> - **No adoption, replacement or demotion follows from it.** If v5 does not improve on v4 over the
>   full calendar, the record says so, and the control (§24.5) stays CP-28's control.
>
> #### CP-28's frozen protocol
>
> - **Author and timing:** the CP-26 Lead writes it from §24.8, without inspecting any outcome, and
>   commits it on `gauntlet/cp-26` before CP-26 computes its first score.
>   The versioned r14 repair protocol is committed before any new search or training pilot;
>   the prior protocol remains historical, with hash-bound supersession recorded.
> - **Review:** CP-26's Integration Critic reviews it.
> - **Custody:** it lands with CP-26. If CP-26 is discarded, the protocol goes with it.
> - **The Owner's later confirmation** decides only whether CP-28 runs, never what it tests.
>
> #### The ledger
>
> Every forecast is stored with its issue instant, training-target cutoff, input vintages, seeds and
> code identity.
>
> Scoring keys permitted by CP-25, a complete canonical day eligible for an own-error buffer,
> and a complete three-native-member day eligible for CP-28 learning are separate predicates.
> A partially eligible day stays measured on its frozen keys, without an invented hour, but a
> partial issuance cannot supply a complete-day error. Full 23/24/25-hour DST dates can.
> Keep pending issuances, once-only consumption, latest released errors and original issuance
> scales continuously across warm-up/measurement, search boundaries, failures and restart.
> Each policy and route owns separate buffers and identity-bound caches. Report buffer counts,
> oldest/latest dates, span and age. No search transition resets this state.
>
> #### Ceilings, proposed
>
> - **400 machine-hours,** summed over workers' wall time, as CP-24's ledger defines it. This
>   includes the warm-up, the parity gate, the searches, the delay runs, the bootstrap, diagnostics,
>   tests and failed jobs.
> - At most 4 concurrent workers; BLAS 1; CPU only; peak memory 12 GB; no cloud and no GPU.
> - **The basis.** The first review projects about 150–165 machine-hours from measured costs per
>   origin.
>   - A run of the control costs about 29 hours of fits, and about 34 with its 14 searches (the second
>     review's reconstruction from CP-24's measured costs).
>   - Under §24.5's margin table, delay runs are expected to be few or none.
>   - **A tier ruling that adds a variant also sets the ceiling it needs:** each variant costs about
>     70–85 machine-hours, and the ruling records the new ceiling.
> - **A timing pilot comes first:** 14 origins, training only, with scores sealed. The general
>   cumulative admission line is an absolute 436.5 machine-hours. For the existing run
>   `cp26-cold-rerun-2026-10-15-01` only, the Owner-approved exception is **440 machine-hours**.
>   The actual cumulative hard ceiling is **500 machine-hours**. Admission is not recalculated
>   as a fraction of that ceiling. Above the applicable admission line, the Lead stops and reports
>   before the full run. A continuation pilot must price
>   all 42 searches across nominal/no-load/GFS+6, as well as daily fits, parity, tests, failed jobs,
>   bootstrap and diagnostics. Compare total projected expense including historical measured
>   time, reported time and retained reserves with the applicable absolute admission line;
>   14 daily origins alone do not price searches.
>   Do not reset the ledger. Unreconciled worker duration or surviving orphan blocks new compute;
>   restart idle time is not measured worker time. The earlier repair-only scope (10 new
>   machine-hours within its then-485-hour ceiling, excluding real search/pilot/replay/scores)
>   remains closed; it is not reopened or extended by this continuation.
>
> #### Outputs, gates and publication
>
> - **Outputs:** the ledger; the scores, and the uncertainty with its stored replicates; the
>   diagnostics; the report; CP-28's frozen protocol; and a draft publication packet under
>   PUBLISH_RULES §11.
> - **Gates:**
>   - CP-25's LAND;
>   - the Owner's tier and margin rulings (§24.5);
>   - the issued brief;
>   - the LAND.
> - **Publication:** CP-26's results may be published before 4.7T, under PUBLISH_RULES 1.5's
>   invariant 10. Publishing is a separate decision.

**The repair bar and outcome clause** (`docs/track-b/evidence/cp-26/landing-repair-brief.md` at the candidate):

> 1. **The five tests above pass** for a correct reason, not by being skipped, deleted or loosened.
>    Each repair is stated:
>    - a stale expectation is updated to the authorized value, citing its authority (r15's
>      calibration, the r16 commits, r17);
>    - a history-dependent check reads recorded identities instead of the branch's Git history;
>    - a fixture includes what it needs.
> 2. **A repair outside `tests/` is allowed only if a guard is wrong under r17.** It is limited to
>    `src/cp26/` identity and guard code, never to a forecast, search, scoring, inference or
>    reporting path, and it is justified in the return.
> 3. **The full suite is green on the curated landing tree,** and also on the full candidate tree.
> 4. **Every scientific output is unchanged:** `git diff --stat 6f57feb <new candidate> -- reports/`
>    is empty.
> 5. **One fresh focused Integration Critic,** from a clean detached checkout of the new candidate,
>    checks items 1–4 and reruns the suite on the curated tree.

> - **no test depends** on the `gauntlet/cp-26` commit history, on an excluded file, or on the
>   untracked output folders;

## Commands actually run

Every Git command ran against the critic worktree or the named environment, read-only. Exit codes are 0 unless stated.

**Orientation and identity**

```text
git -C <critic-2> status --porcelain                      -> empty (exit 0)
git -C <critic-2> rev-parse HEAD                          -> 04f00eac5506c550ed4c775b84dc65a41f86c007
git show <rev>:capstone_v21.md | shasum -a 256            -> 4766a61: 27bdc604…0fd1 (r16, = H.PINS)
                                                              332baeb: 3be866bd…00c5 (= SCIENTIFIC_ANCHOR_SHA256)
                                                              5cc3cc0 and 647d6eb (main): 173799d8…a8a5 (r13)
                                                              6f57feb: 27bdc604…  f014e5b, d8f912a, 04f00ea: 3124451d…e4fc
git show main:scripts/bar.py | python3 -I - bar capstone_v21.md "### 24.7 …" --at <rev>
                                                          -> at 6f57feb, f014e5b, d8f912a and 04f00ea: section 250 lines,
                                                             15129 bytes, sha256 423527d9…5b1e (identical at all four)
git show 04f00ea:docs/track-b/evidence/cp-26/landing-repair-brief.md | shasum -a 256
                                                          -> 27d3e1afbdcc5f02b88b27f59ed4935ac8bc99918ea8c58124e0cdbb3bd89e3d
shasum -a 256 .local/artifacts/cp-26-landing/exclusion-rule.txt
                                                          -> 7cbd68734f864d78a076800ecb1db273a8b8e50ba00f0bf79b76d24ac72af565
```

**The repair diff (bar items 1, 2, 4)**

```text
git log d8f912a..04f00ea                                  -> 1c59c24 (brief), 7fbbff7 (r17 PASS copy), 04f00ea (tests)
git diff --name-status d8f912a 04f00ea                    -> 7 A under docs/track-b/evidence/cp-26/, 5 M under tests/
git diff --name-only d8f912a 04f00ea | grep -v -e '^tests/' -e '^docs/track-b/evidence/cp-26/'
                                                          -> nothing (grep exit 1)
git diff --stat 6f57febe3659b1f902c17f3db31ba41e41136178 04f00ea -- reports/
                                                          -> empty (exit 0)
git diff --stat d8f912a 04f00ea -- reports/ data/ src/ pyproject.toml uv.lock 'capstone_*' 'syllabus_*'
    '*-amendments.md' AGENTS.md CLAUDE.md engineering-role.md orchestrator-role.md notebooklm-role.md
    docs/track-b/gauntlet-templates.md docs/track-b/exposure-ledger.md docs/PUBLISH_RULES.md
    docs/track-b/rule-inventory.md docs/track-b/cp-0-defects.md program-stage-sequence.md .claude
                                                          -> empty (exit 0)
git diff --name-status 6f57feb d8f912a                    -> 31 A, 1 M (capstone_v21.md, the r17 ratification)
git rev-parse 04f00ea:docs/track-b/evidence/cp-26/gfs-v21-r17/integration-r17-PASS.md \
              04f00ea:docs/track-b/evidence/cp-26/integration.md d8f912a:docs/track-b/evidence/cp-26/integration.md
                                                          -> 74eb6d6065e7b8584c422f99ad65dd5b70ac3325 (all three)
per-file test-function names, d8f912a vs 04f00ea         -> identical in all five files (66, 9, 4, 3, 15)
grep skip/skipif/importorskip/xfail in tests/test_cp26_*.py
                                                          -> none
```

**Records behind each repair (bar item 1)**

```text
PINS recomputed at the candidate (regex over src/cp26/harness.py, sha256 of each file)
                                                          -> 25 of 26 OK; capstone_v21.md 3124451d… vs pin 27bdc604…
                                                             (r17 supersedes r16, expected)
calibration-v21-r15.json policy_tested                    -> startup 14.0, heartbeat 8.0, poll 0.2, ledger 3.0
authority-v21-r16.json limits_preserved                   -> startup 14, heartbeat 8, poll 0.2, ledger 3
src/cp26/limits.py (from a57aba5, r15)                    -> LEDGER 3.0, HEARTBEAT 8.0, STARTUP 14.0, POLL 0.2
capstone_v21-r14-to-v21-r15-amendments.md                 -> Owner approval 2026-10-16 to replace the 0.5 s / 2 s
                                                             restrictions with measured finite limits
git show 8070238 -- src/cp26/harness.py                   -> ANCHOR_COMMIT c9d5ab9… -> 4766a61…; capstone pin -> 27bdc604…;
                                                             the two stress tests' policy asserts left at 10/2/0.2/0.5
authority-v21-r16.json                                    -> anchor_commit 4766a61…, original_scientific_anchor_commit
                                                             332baeb…, sha 3be866bd…, cumulative_before
                                                             .continuation_authority_sha256 6d008620… (= PIN),
                                                             ratified_documents capstone 27bdc604…
grep 27bdc604… docs/track-b/capstone_v21-r16-to-v21-r17-amendments.md
                                                          -> line 15 (the r17 "Base" clause)
active-documents.json                                     -> capstone_v21.md at 332baeb, 3be866bd…, supersedes
                                                             {5cc3cc0, v21-r13, 173799d8…}; landed_code_base 647d6eb…;
                                                             historical_documents_unchanged = issued-brief.md,
                                                             cp28-frozen-protocol.md
git show 5cc3cc0:<each historical document> | shasum -a 256 vs working file
                                                          -> issued-brief.md 5e16a134… = 5e16a134…;
                                                             cp28-frozen-protocol.md f2ebee6e… = f2ebee6e…
§§1–23 ('## 1. ' up to '## 24. ') sha256 at 5cc3cc0, 647d6eb and 04f00ea
                                                          -> 1d5406a3df529929ce6a662af97d7fcfeecc40726906b5a994548140d6f1a872
                                                             at all three (= R13_SECTIONS_1_TO_23_SHA256)
harness-log.json landed_code vs git show 647d6eb:<every .py under the eight LANDED_CODE roots>
                                                          -> 146 entries, equal; worktree equal; git diff 647d6eb 04f00ea
                                                             -- <landed roots> lists 0 files
cmp each scientific-base-1e7eb02/<n>.py with git show 1e7eb029f1cb…:src/cp26/<n>.py
                                                          -> execution, harness, parity, search: byte-identical
git rev-parse 1e7eb02:src/cp26/<n>.py, sha256, byte count -> 83959c0c…/3b8de55d…/32280, 98f9a8bc…/7c5e3c30…/24187,
                                                             d34d244f…/8a73ff52…/19207, 29982217…/a8bda41a…/27300;
                                                             all equal manifest.json
runtime-code-v21-r16.json original_recipe_code_sha256     -> harness 7c5e3c30…, parity 8a73ff52…, search a8bda41a…
                                                             (= snapshot hashes); scientific_base_commit 1e7eb02…
parity.json reference_custody vs git show <evidence_commit>:<file> and the working file
                                                          -> 14 of 14 blobs OK (cp15, cp16, cp20, cp21, cp23, cp24);
                                                             96 checks, status PASS
git merge-base --is-ancestor <c> 647d6eb; git tag --contains <c>
                                                          -> the six parity evidence commits are reachable only from
                                                             evidence/cp-15…cp-24 tags; 1e7eb02, 5cc3cc0, 4766a61,
                                                             332baeb, b06114f are not on main and in no tag
execution-manifest.json protocol_identity vs admission-v21-r15.json and checks-v21-r16.json
                                                          -> equal; document_sha256 matches the (excluded)
                                                             continuation-v21-r14/execution-protocol.json; registration
                                                             sha matches
search-plans/<route>/k<k>.json identity vs execution-manifest.json searches[]
                                                          -> 42 of 42 equal (nominal k13 included)
python (sys.path src) H.continuation_authority(.), H.identities(.) at the candidate
                                                          -> HarnessError "ratified continuation document identity
                                                             changed"; HarnessError "pinned identity mismatch:
                                                             capstone_v21.md 3124451d… != 27bdc604…"
```

**Curated tree and history-free repository (environments the Lead prepared)**

```text
git diff --name-only main 04f00ea                         -> 10,265 paths (10,264 A, 1 M)
minus the 15 exclusion lines                              -> 846 curated, 9,419 excluded
git -C <critic-curated> rev-parse HEAD / main             -> 647d6eb… / 647d6eb…
git -C <critic-curated> diff --cached --name-only main    -> 846 paths, identical to the computed list
git -C <critic-curated> diff --name-only                  -> empty
xargs -n 200 git diff --cached --name-only 04f00ea -- < <curated list>
                                                          -> empty; and a -z (space-safe) Python comparison of
                                                             every curated index entry with ls-tree 04f00ea -> equal
ls-files -s -z (critic-curated) vs ls-tree -r -z c4e3b0ba914bba33b4d2f27e635705df55a3ad42
                                                          -> equal: 2,397 entries, all stage 0; curated entries equal the
                                                             candidate's, the other 1,551 equal main's
sum of curated file sizes                                 -> 846 files, 44,801,005 bytes
git -C <critic-ci-sim> rev-parse --show-toplevel HEAD HEAD^{tree}
                                                          -> its own top level; e5624978…; c4e3b0ba914bba33b4d2f27e635705df55a3ad42
git -C <critic-ci-sim> rev-list --all --count; tag; for-each-ref
                                                          -> 1; empty; refs/heads/ci-sim only; no alternates file
ls-tree -r -z HEAD (ci-sim) vs ls-files -s -z (critic-curated)
                                                          -> equal, 2,397 entries
git -C <critic-ci-sim> cat-file -e <c>^{commit} for 04f00ea, d8f912a, 647d6eb, 1e7eb02, 5cc3cc0, 4766a61, 1bdc75b
                                                          -> none resolves
```

**Suites (bar item 3), one at a time, under the CP-26 monitor, with the brief's template**

```text
/Users/djourno/Downloads/PJM/.venv/bin/python -B <critic-2>/scripts/cp26_rebaseline.py monitor \
  --name NAME --workers 4 --log /Users/djourno/Downloads/PJM/.local/artifacts/cp-26/landing-repair/logs/NAME.log -- \
  /usr/bin/env -u CP26_LEDGER -u CP26_MONITORED_JOB -u CP26_JOB_ID -u CP26_JOB_INDEX -u CP26_WORKERS \
  -u PYTHONPATH -u VIRTUAL_ENV -u PYTHONDONTWRITEBYTECODE UV_PROJECT_ENVIRONMENT=ENV/venv UV_PYTHON=3.12 UV_OFFLINE=1 \
  MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1 CP26_PROJECT_ROOT=ENV/absent-project-root \
  /bin/sh -c 'cd TREE && uv sync --locked --dev && uv run python scripts/build_wasm_payload.py && uv run pytest -q -p no:cacheprovider -rfEs'
ENV = /Users/djourno/Downloads/PJM/.local/tmp/cp-26-landing-repair/critic-envs/NAME (fresh, empty before the run)
```

| NAME | TREE | Monitor line | pytest's final line |
|---|---|---|---|
| `critic-2-curated` | `.local/worktrees/cp-26/critic-curated` | job `f8aa2674…`, exit_code 0, abort_reason null, wall 616.84 s | `2213 passed, 8 skipped in 531.35s (0:08:51)` |
| `critic-2-ci-sim` | `.local/tmp/cp-26-landing-repair/critic-ci-sim` | job `3036a6b6…`, exit_code 0, abort_reason null, wall 616.62 s | `2205 passed, 16 skipped in 530.34s (0:08:50)` |
| `critic-2-full` | `.local/worktrees/cp-26/critic-2` | job `ec5c5add…`, exit_code 0, abort_reason null, wall 659.34 s | `2213 passed, 8 skipped in 534.36s (0:08:54)` |

Each log shows `Using CPython 3.12.14`, a new virtual environment at ENV/venv, `Resolved 129 packages`, `Installed 117 packages`, and the payload step's Python 3.13 model warning. Skips (`-rfEs`):

- **Curated and full (8):** `tests/cp20/test_gfs_eccodes.py:11` (no eccodes); `tests/cp16/conftest.py:66` (CP-16 bound to the v21-r3 anchor) ×1 and `:61` (production verification) ×5; `tests/cp24/test_draft_export.py:38`.
- **History-free (16):** the same 8, plus `tests/cp21`, `cp22` and `cp23` `test_saved_evidence.py` (evidence/cp-2x not in this checkout), `tests/test_29_research_evidence.py:49` (no evidence tags), `tests/test_36_derived_records.py:88` and `tests/test_38_page_architecture.py:249` (no Git history), and `tests/test_49_pres4_v5_publication.py:138` and `:693` (published export's commit absent).
- **No CP-26 test is skipped** in any run. No FAILED or ERROR line appears in any run.
- **Tree state after each run:**
  - The curated worktree is still 845 `A ` + 1 `M ` staged, with nothing unstaged.
  - The ci-sim status is empty, still 1 commit, no tag.
  - The critic worktree is clean at the candidate. The payload step rewrote the tracked `reports/cp3b/payload.json` with identical bytes.
- `supervisor_identity_lost` did not recur.

**The rich-admin behaviour (assignment's "behavior to judge")**, TEST = `tests/test_cp26_ledger_liveness.py::test_rich_closed_jobs_three_busy_owners_accept_fourth_admin_with_full_future_history`, TREE = ci-sim, template without the payload step, `uv run pytest -q -p no:cacheprovider -rfEs --basetemp=ENV/basetemp "$TEST"`, each in a fresh ENV:

| NAME | Extra variable | Monitor line | pytest | Inner ledger, last four jobs |
|---|---|---|---|---|
| `critic-2-rich-admin-nobytecode` | `PYTHONDONTWRITEBYTECODE=1` after `-u PYTHONDONTWRITEBYTECODE` | job `99588430…`, exit_code 1, wall 86.53 s | `1 failed in 59.60s`: `subprocess.TimeoutExpired` at `process.communicate(timeout=15)`, `tests/test_cp26_ledger_liveness.py:2169` | three owners and `ledger-rich-admin` all still `running` when the test's cleanup killed them; admin supervisor sequence 30, watchdog 17 |
| `critic-2-rich-admin-bytecode` | none | job `4b65312a…`, exit_code 0, wall 68.12 s | `1 passed in 45.22s` | owners exit 0 at 15.46–15.87 s; `ledger-rich-admin` exit 0, abort null, **9.03 s** |

After both: `pgrep -fl critic-2-rich-admin` and `pgrep -fl critic-ci-sim` -> none (exit 1); no orphan.

**Ledger accounting:** `scripts/cp26_rebaseline.py status` -> 243.4407 machine-hours before the first run, 245.7157 after the fifth (5 jobs × 4 declared workers, 2,047.45 s wall in all), `running: []`, `unreconciled_reserves: []`. It was never reset.

## Evidence actually inspected

- **The generated brief:** `critic-brief cp-26` from `main`'s `scripts/gauntlet.py`.
- **The issued repair brief:** the whole file at the candidate.
- **The three repair commits:** their messages, the full test diffs of `tests/test_cp26_{ledger_liveness,parity,r15,repair_contract,search}.py`, and the new test bodies in context.
- **Harness code:**
  - `src/cp26/harness.py`, lines 55–320: PINS, `identities`, `landed_code`, `continuation_authority`, `input_fingerprint`, `_runtime_record`, `recipe_code_sha256` and `runtime_lineage`.
  - `src/cp26/parity.py`: `SOURCES`, `verify_sources` and `load_references`.
  - `src/cp26/search.py` `search_identity`, `src/cp26/gates.py` `protocol_identity`, and `src/cp26/limits.py`.
  - `src/cp26/supervisor.py`, the policy lines.
- **History:** the r15 commit `a57aba5` (limits) and the r16 commit `8070238`, for harness and test changes.
- **Records:**
  - `calibration-v21-r15.json`, `authority-v21-r16.json`, `runtime-code-v21-r16.json`, `admission-v21-r15.json` and `checks-v21-r16.json` (`docs/track-b/evidence/cp-26/cold-rerun-2026-10-15/`).
  - `docs/track-b/evidence/cp-26/repair-v21-r14/active-documents.json`.
  - `reports/rebaseline/harness-log.json`, plus `reports/rebaseline/cold-rerun-2026-10-15/execution-manifest.json`, `parity.json`, and all 42 `search-plans/*/k*.json`.
  - `docs/track-b/capstone_v21-r14-to-v21-r15-amendments.md` (authority passage) and `docs/track-b/capstone_v21-r16-to-v21-r17-amendments.md` (head, including the r16 base clause and "§24.7 remains byte-identical").
- **The new evidence directory:** `docs/track-b/evidence/cp-26/landing-repair/scientific-base-1e7eb02/`, all five files.
- **Exclusion rule and tests:** `.local/artifacts/cp-26-landing/exclusion-rule.txt`, and `.github/workflows/tests.yml`.
- **Payload build:** `scripts/build_wasm_payload.py`, its output paths.
- **Static audit:**
  - every `git` call in `src/cp26/*.py` and `scripts/cp26_*.py`, and every call site of the Git-reaching functions;
  - every `git`, `check_output`, `git_blob_sha256` and `hooksPath` use in `tests/`;
  - every test reference to an excluded path or to the three untracked output folders;
  - `CP26_PROJECT_ROOT` use in tests.
- **Logs:** the five monitor logs named above, plus the inner ledgers under the two rich-admin basetemps.
- **Not read:**
  - the Lead's or the earlier critic attempt's logs, notes or scratch;
  - `progress.md`, the syllabus, Track A/C material and `orchestrator-role.md`;
  - any data dated after 2026-09-06.

  No network access, search, fit, forecast, replay, scoring, bootstrap or report regeneration.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 0a | §24.7 unchanged | PASS | Section hash `423527d9…` identical at 6f57feb, f014e5b, d8f912a and the candidate; equal to the generated brief's excerpt. |
| 0b | Anchor unchanged by the repair | PASS | `capstone_v21.md` is `3124451d…` at f014e5b, d8f912a and 04f00ea; the frozen-path diff d8f912a..04f00ea is empty. |
| 1.1 | Repair: `test_three_jobs_keep_fresh_supervision_with_full_future_history` | PASS | **Stale expectation.** The policy assert now equals both a literal 14/8/0.2/3 s and the values read from `calibration-v21-r15.json` `policy_tested` and `authority-v21-r16.json` `limits_preserved`. I confirmed those match `src/cp26/limits.py` (r15, a57aba5) and the r15 Owner authority to replace 0.5 s/2 s with measured finite limits. Every other assertion is untouched, including freshness, sample-sequence growth and the 500 h `CAPS`. Not loosened. |
| 1.2 | Repair: `test_rich_closed_jobs_three_busy_owners_accept_fourth_admin_with_full_future_history` | PASS | Same repair, same authority. The 15 s controller wait, the admin's own assertions (<0.5 s lock telemetry, 4 workers) and the post-checks are unchanged. Passed in all three suites and alone with bytecode allowed. See item 7. |
| 1.3 | Repair: `test_anchor_commit_and_landed_base_are_distinct_and_explicit` | PASS | **Stale expectation and history.** `ANCHOR_COMMIT` 332baeb→4766a61 follows r16 (8070238 set it), and 332baeb is kept as `SCIENTIFIC_ANCHOR_COMMIT`. The history reads were replaced: (a) the r16 authority record, pinned by bytes; (b) the r17 amendment naming 27bdc604…; (c) active-documents.json; (d) the harness-log landed-code map. I verified each against Git independently: 4766a61:capstone = 27bdc604; 332baeb = 3be866bd; the harness-log map equals all 146 landed `.py` at 647d6eb. The per-pin byte loop exempts only capstone (superseded by r17) and the continuation authority, which lies in the excluded `continuation-v21-r14/` folder and is bound through the pinned r16 authority's `cumulative_before` record. The CP-25 and CP-15 manifest checks from `identities()` are kept. |
| 1.4 | Repair: `test_original_documents_and_sections_1_through_23_stay_historical` | PASS | **History.** The `git show 5cc3cc0:` reads were replaced by active-documents.json's `supersedes` hashes and a recorded §§1–23 SHA-256. I recomputed the constant at 5cc3cc0, main and the candidate (`1d5406a3…`, equal). Both historical documents equal 5cc3cc0's bytes. The r13 identity (173799d8…, v21-r13, 5cc3cc0) is asserted exactly. Not loosened. |
| 1.5 | Repair: `test_search_lineage_changes_when_context_adapter_changes` | PASS | **Fixture.** Since r16, `recipe_code_sha256` reads `RUNTIME_LINEAGE` from `git show HEAD:` in the root. The fixture now writes and commits a synthetic lineage in its own tmp repository, and adds an assertion that the recipe identities are reported. The original assertion (changing `members.py` changes the identity) is unchanged. `core.hooksPath=/dev/null` applies only to that throwaway tmp repository, as `tests/cp24/test_base_tree.py` already does. |
| 1.6 | Repair: `test_r15_authority_does_not_relabel_scientific_plan_or_parity` | PASS | **r17 and history.** I confirmed the live guards refuse at the candidate: `continuation_authority` raises "ratified continuation document identity changed" and `identities` raises a capstone pin mismatch. That is correct fail-closed behaviour for execution guards bound to the r16 anchor after r17 forbade new computation, so no guard is wrong. The test now binds the same identities through committed records. I checked its replicated fingerprint and plan-identity formulas against `input_fingerprint`/`search_identity`/`recipe_code_sha256` (same keys, same `json.dumps(sort_keys=True)`). Independent checks: protocol = r15 admission = r16 checks; protocol document hash matches the excluded file; all 42 plan identities equal the manifest's; parity custody 14/14 equals Git blobs. The relabel check (r14 schema, research sha, search protocol, 96 parity checks) is retained. |
| 1.7 | Repair: `test_original_numeric_functions_are_unchanged_by_r15` | PASS | **History.** The AST comparison now reads `scientific-base-1e7eb02/`. All four snapshots are byte-identical to `git show 1e7eb029f1cb…:src/cp26/<n>.py`, and blob ids, SHA-256 and sizes equal the manifest. Harness, parity and search equal the r16 lineage's recipe hashes. The comparison logic is unchanged. |
| 1.8 | Repair: `test_real_references_are_committed_and_internally_bitwise_consistent` | PASS | **History (local evidence tags).** `git_blob_sha256` is monkeypatched to parity.json's recorded custody; a missing key raises. Every real vector check in `load_references` still runs, and the test now also asserts `custody == recorded`. I verified the recorded blobs equal `git show <evidence_commit>:<file>` and the working files (14/14). Those commits are reachable only from `evidence/cp-*` tags. |
| 1.9 | No test skipped, deleted or loosened | PASS | Same test names in all five files. No skip/xfail in any CP-26 test. No CP-26 test appears among the skips of any run. 57 added lines containing `assert` against 12 removed, each removed one replaced as described above. |
| 2 | Nothing outside `tests/` (src only if a guard is wrong under r17) | PASS | d8f912a..04f00ea touches only `tests/` (5 M) and `docs/track-b/evidence/cp-26/` (7 A, all new files; the r17 PASS copy is blob-identical to `integration.md`). No `src/` change, so no guard justification is required. Frozen paths are unchanged. |
| 3a | Suite green on the curated landing tree | PASS | `2213 passed, 8 skipped`, monitor exit 0. |
| 3b | Suite green on the full candidate tree | PASS | `2213 passed, 8 skipped`, monitor exit 0. |
| 4 | `git diff --stat 6f57feb <candidate> -- reports/` empty | PASS | Empty. Since 6f57feb, the only non-additive change anywhere is the r17 anchor. |
| 5 | Fresh focused Integration Critic from a clean detached checkout reruns the suite on the curated tree | PASS | This review: detached clean worktree at the candidate, no Git write, curated suite rerun. |
| 6a | No test depends on `gauntlet/cp-26` history | PASS | The history-free repository (1 commit, no tag, candidate commits unresolvable) gave `2205 passed, 16 skipped`, with no CP-26 skip. Static audit: every remaining Git call in CP-26 tests is against a tmp fixture repo or monkeypatched; real-root reads are of committed files only. |
| 6b | No test depends on an excluded file | PASS | The curated tree and ci-sim hold none of the 9,419 excluded paths, and both suites are green. Static grep finds excluded-path names only under `tmp_path` fixtures. The r15 test compares `PROTOCOL` only as a string. |
| 6c | No test depends on the untracked output folders | PASS | Those folders exist only in the Lead worktree; none is present in the three trees run here. No test names them. |
| 7 | Curated tree identity and environments verified | PASS | Curated: HEAD = main; the staged list equals my computed 846-path list; staged content equals the candidate; nothing unstaged; index = tree `c4e3b0ba…` (2,397 files; 846 curated, 44,801,005 bytes). Ci-sim: HEAD^{tree} `c4e3b0ba…`, 1 commit, no tag, entries equal the curated index. |
| 8 | Rich-admin timeout: defect or environment | PASS (environment) | Reproduced both ways in fresh venvs: with `PYTHONDONTWRITEBYTECODE=1` it times out at the 15 s wait, with all four inner jobs still running. Allowed bytecode, as in CI's workflow (which sets no such variable), it passes, the admin job taking 9.03 s. With no `.pyc` anywhere, every `python -B` inner process recompiles numpy/pandas imports. The repair did not touch the 15 s wait. Residual risk, non-blocking: about 6 s of margin on this machine, and a slower runner could flake. |

## On FAIL only
- Single largest meaningful gap: not applicable (PASS).
- Exact next acceptance test: not applicable (PASS).

## Notes (non-blocking)

- **Reduced guard coverage.** After the repair, no test runs the live `continuation_authority`, `identities`, `input_fingerprint`, `landed_code` or `protocol_identity` against the real tree. Elsewhere they are monkeypatched, and under r17 they refuse by design. The repaired tests reproduce their identity computations from committed records. That is the right repair under the brief, but a future change to those functions' formulas would not be caught by the record-based tests.
- **Self-bound snapshot.** `execution.py` in `scientific-base-1e7eb02/` is bound only by the snapshot's own `manifest.json`, since the r16 lineage records no recipe hash for it. I verified its bytes against 1e7eb02 directly; CI cannot.
- **Retained environments.** The five fresh environments under `.local/tmp/cp-26-landing-repair/critic-envs/critic-2-*` (about 4.3 GB, including the two rich-admin basetemps) are left for the Lead's cleanup with the worktree. They are named in the return.
