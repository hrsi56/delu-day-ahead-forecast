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
