# CP-16 fixed H/P research comparison — development, post-selection

Engineering status: **pending fresh exact-candidate Integration review**; the terminal verdict and both SHAs are recorded in the canonical checkpoint return. Historical CP-15 product status: **NOT_DEMONSTRATED**, unchanged. New original-§8 diagnostic status: {'V2-H': 'not_met', 'V2-P': 'not_met'}. Product/delivery eligibility: **not authorized by this research evaluation**.

Descriptive H/P ordering: V2-H then V2-P (S_WIS, then S_MAE, then P on exact ties). Ranking does not establish a supported winner or select a live policy. Primary conclusion: **no demonstrated joint preference**. All intervals are exploratory post-selection; no equivalence, absence-of-benefit or absence-of-harm claim follows.

## Point and interval scores

Each primary score equally averages five fold ratios to B0. MAE uses emitted p50; the central forecast remains separate. Seven-quantile WIS uses interval weights alpha/2, median weight 1/2 and divisor 3.5. Native v1 nine-quantile pinball remains in its original historical files and is not this WIS or mean_pinball_7.

| policy | S_MAE | S_WIS |
|---|---|---|
| B0 | 1.0 | 1.0 |
| B1 | 1.051845134839199 | 0.9856366964174134 |
| B2 | 0.6578109123747921 | 0.6389910407326591 |
| B3 | 0.7841363977682992 | 0.7399052224715813 |
| A1 | 0.6722908121370033 | 0.646015091607363 |
| V2-H | 0.6440721386286878 | 0.6160299894915677 |
| V2-P | 0.6457675850846845 | 0.6287217727210093 |

Primary H−P and secondary comparisons, with 95% paired percentile intervals:

| candidate | baseline | metric | difference | ci_lower | ci_upper | status |
|---|---|---|---|---|---|---|
| V2-H | V2-P | MAE | -0.0016954464559965077 | -0.003623724975937509 | 3.857628092332211e-06 | resolved |
| V2-H | V2-P | WIS | -0.012691783229441422 | -0.015571242603026905 | -0.010911902067713655 | resolved |
| V2-H | B2 | MAE | -0.013738773746104216 | -0.02357190366002046 | -0.005344156036269626 | resolved |
| V2-H | B2 | WIS | -0.022961051241091157 | -0.03369653727283832 | -0.011809928240258985 | resolved |
| V2-P | B2 | MAE | -0.012043327290107708 | -0.021286980583395003 | -0.003556325861059117 | resolved |
| V2-P | B2 | WIS | -0.010269268011649735 | -0.020060192236757847 | 0.000670395231647897 | resolved |

For H−P, WIS improves with an interval wholly below zero; MAE also has a negative point estimate, but its upper endpoint is +0.0000038576. It must not be rounded to zero to claim joint improvement. Joint improvement requires WIS upper endpoint <0 AND MAE upper endpoint <=0. Both metrics and their directions are retained without an invented tradeoff weight. Conclusions: {"V2-H-B2": "observed joint improvement", "V2-H-V2-P": "no demonstrated joint preference", "V2-P-B2": "no demonstrated joint preference"}.

## Population and causal construction

All seven policies cover 10,747 identical eligible keys: 2,160 / 2,159 / 2,112 / 2,160 / 2,156, totaling 75,229 policy-target rows. Full fold 3 has 2,112 hours across 88 represented dates; August 15–31 has 408 hours/17 dates. Original missing/excluded hours are preserved; no failed eligible issuance is removed. `failures.csv` records the current run, while historical invalidated failure logs remain in `attempt-1/`.

Both policies use exactly the A1/B2 central 50/50 blend, origin-specific A1 scale, and the same latest 28 complete released error days. H shrinks local-hour quantiles toward pooled values using n/(n+56), with pooled fallback below 14 distinct days; P uses pooled values. Both score their own shifted p50. No clipping, projection or p50 reset is used. All 35 training-only admission dates were completed and frozen before outer comparison. Fixed origins are D−1 11:00 UTC; delivery calendar is Europe/Berlin. D−1 errors cannot update the buffer, D−2 complete errors can; canonical 23/24/25-hour identities and consume-once hold.

## Diagnostics and unchanged quality conditions

`metrics.csv` reports all per-fold and pooled metrics, central/p50 error and centering, RMSE, signed bias, daily level/shape, 50/80/95% coverage and width summaries and tail misses. `diagnostics.csv` carries all 24 local hours, exhaustive night 22–05 / solar 10–16 / shoulder 06–09 and 17–21 blocks, represented dates/hits/widths, daily losses, peak and September recovery slices. At least 56 represented dates is required for supported hour/block comparison statements; fewer is explicitly support-limited. Peak and recovery slices remain descriptive.

`uncertainty.csv` retains all full-fold descriptive paired daily intervals and the primary equal-fold normalized intervals. Seed 15042 produces one shared set of 2,000 noncircular 7-calendar-day block draws per pass; missing dates remain missing. Undefined replicates would be unresolved, never dropped or redrawn. Index identity: e1df9a68dc6715aa2ecd9705ef61f504a3fe109ed917d1151ccbc46ea9e0f99b.

All six original §8 diagnostics, actuals, limits and comparator identities:

| policy | criterion | metric | scope | actual | lower_limit | upper_limit | comparator | status |
|---|---|---|---|---|---|---|---|---|
| V2-H | 1 | S_MAE | equal_fold | 0.6440721386286878 |  | 0.5920298211373128 | best B0-B3 | not_met |
| V2-H | 2 | S_WIS | equal_fold | 0.6160299894915677 |  | 0.5750919366593932 | best B0-B3 | not_met |
| V2-H | 3 | coverage95 | fold_1 | 0.9282407407407407 | 0.9 | 0.98 |  | met |
| V2-H | 3 | coverage95 | fold_2 | 0.936081519221862 | 0.9 | 0.98 |  | met |
| V2-H | 3 | coverage95 | fold_3 | 0.9389204545454546 | 0.9 | 0.98 |  | met |
| V2-H | 3 | coverage95 | fold_4 | 0.9384259259259259 | 0.9 | 0.98 |  | met |
| V2-H | 3 | coverage95 | fold_5 | 0.9526901669758813 | 0.9 | 0.98 |  | met |
| V2-H | 4 | coverage95 | peak | 0.9240196078431373 | 0.9 |  |  | met |
| V2-H | 4 | MAE | peak | 52.5098015356535 |  | 57.617758673520505 | best B0-B3 on matched peak | met |
| V2-H | 5 | MAE | fold_1 | 6.310802110246006 |  | 6.530232537302945 | best rolling B2/B3 | met |
| V2-H | 5 | MAE | fold_2 | 9.457089743262161 |  | 10.160199330508874 | best rolling B2/B3 | met |
| V2-H | 5 | MAE | fold_3 | 51.213622921785436 |  | 56.7082158826891 | best rolling B2/B3 | met |
| V2-H | 5 | MAE | fold_4 | 16.1242511972614 |  | 17.367639793808983 | best rolling B2/B3 | met |
| V2-H | 5 | MAE | fold_5 | 18.730145716433146 |  | 20.162626935989135 | best rolling B2/B3 | met |
| V2-H | 4 | WIS | peak | 30.102050231473346 |  | 33.72970535812474 | best B0-B3 on matched peak | met |
| V2-H | 5 | WIS | fold_1 | 3.855935752625375 |  | 4.147146167403628 | best rolling B2/B3 | met |
| V2-H | 5 | WIS | fold_2 | 5.981432938667355 |  | 6.339890674080492 | best rolling B2/B3 | met |
| V2-H | 5 | WIS | fold_3 | 30.22126634528976 |  | 33.940454346635754 | best rolling B2/B3 | met |
| V2-H | 5 | WIS | fold_4 | 9.54679415511936 |  | 10.400724362891893 | best rolling B2/B3 | met |
| V2-H | 5 | WIS | fold_5 | 11.026057654908808 |  | 12.102308138409143 | best rolling B2/B3 | met |
| V2-H | 6 | complete_finite_ordered | all_eligible | 1.0 | 1.0 | 1.0 |  | met |
| V2-P | 1 | S_MAE | equal_fold | 0.6457675850846845 |  | 0.5920298211373128 | best B0-B3 | not_met |
| V2-P | 2 | S_WIS | equal_fold | 0.6287217727210093 |  | 0.5750919366593932 | best B0-B3 | not_met |
| V2-P | 3 | coverage95 | fold_1 | 0.9310185185185185 | 0.9 | 0.98 |  | met |
| V2-P | 3 | coverage95 | fold_2 | 0.936081519221862 | 0.9 | 0.98 |  | met |
| V2-P | 3 | coverage95 | fold_3 | 0.9417613636363636 | 0.9 | 0.98 |  | met |
| V2-P | 3 | coverage95 | fold_4 | 0.9421296296296297 | 0.9 | 0.98 |  | met |
| V2-P | 3 | coverage95 | fold_5 | 0.9601113172541744 | 0.9 | 0.98 |  | met |
| V2-P | 4 | coverage95 | peak | 0.9240196078431373 | 0.9 |  |  | met |
| V2-P | 4 | MAE | peak | 52.65780188872363 |  | 57.617758673520505 | best B0-B3 on matched peak | met |
| V2-P | 5 | MAE | fold_1 | 6.341966242641303 |  | 6.530232537302945 | best rolling B2/B3 | met |
| V2-P | 5 | MAE | fold_2 | 9.443523631402769 |  | 10.160199330508874 | best rolling B2/B3 | met |
| V2-P | 5 | MAE | fold_3 | 51.05393417215354 |  | 56.7082158826891 | best rolling B2/B3 | met |
| V2-P | 5 | MAE | fold_4 | 16.219630000839047 |  | 17.367639793808983 | best rolling B2/B3 | met |
| V2-P | 5 | MAE | fold_5 | 18.833649365532423 |  | 20.162626935989135 | best rolling B2/B3 | met |
| V2-P | 4 | WIS | peak | 30.854812452733036 |  | 33.72970535812474 | best B0-B3 on matched peak | met |
| V2-P | 5 | WIS | fold_1 | 3.9416084906712174 |  | 4.147146167403628 | best rolling B2/B3 | met |
| V2-P | 5 | WIS | fold_2 | 6.067481989064118 |  | 6.339890674080492 | best rolling B2/B3 | met |
| V2-P | 5 | WIS | fold_3 | 30.573871569693733 |  | 33.940454346635754 | best rolling B2/B3 | met |
| V2-P | 5 | WIS | fold_4 | 9.77323240828227 |  | 10.400724362891893 | best rolling B2/B3 | met |
| V2-P | 5 | WIS | fold_5 | 11.351776635384352 |  | 12.102308138409143 | best rolling B2/B3 | met |
| V2-P | 6 | complete_finite_ordered | all_eligible | 1.0 | 1.0 | 1.0 |  | met |

## Resources, defects and limitations

Cumulative candidate policy-days: 5022/9,000, including the unchanged historical 3,730. Counts and every monitored command are in `resources.json`; review adds to the same ledger and its final evidence snapshot. Candidate machine time: 0.4991 hours/24. Active effort conservative upper bound: 1.49 hours/40, against the original 32-hour approximate timebox. Resumed jobs are serialized, numerical thread pools1. Peak measured process-tree RSS 1.170 GiB; disk upper bound 0.529 GiB (includes entire pre-existing Git store). No downloads, external services, cost, forbidden work or new reference fits.

New main fitting by fold and component (shared by H/P, not charged twice):

| fold | component | new_hourly_fit_records | primitive_calls | fit_seconds |
|---|---|---|---|---|
| fold_1 | A1 | 192 | 960 | 33.64369612518931 |
| fold_1 | B2 | 192 | 960 | 28.349304209987167 |
| fold_2 | A1 | 144 | 720 | 47.64989950400195 |
| fold_2 | B2 | 144 | 720 | 40.404686538822716 |
| fold_3 | A1 | 192 | 960 | 87.26423478676588 |
| fold_3 | B2 | 192 | 960 | 41.19167195915361 |
| fold_4 | A1 | 192 | 960 | 80.35673837384093 |
| fold_4 | B2 | 192 | 960 | 68.29201216693036 |
| fold_5 | A1 | 192 | 960 | 78.556679997826 |
| fold_5 | B2 | 192 | 960 | 69.74467583425576 |

H/P emission, data preparation and memory are measured jointly by monitored job, not invented per-policy allocations. B0/B1/B2/B3/A1 are saved vectors with zero new model-fit cost; their original measured costs remain in `reports/cp15/report.md` and fold run logs. Current scoring/reading costs are shared metric-only jobs in the ledger. Reference fits and their costs are not silently treated as newly generated.

The prior interrupted admission and independent FAIL remain preserved, including unknown RSS during the supervisor gap and unsupported early thread-enforcement assertions. Required evidence was regenerated under repaired monitoring; no old gap is claimed cured retrospectively. See `docs/track-b/evidence/cp-16/resumption-notice.md` and `resumption-feasibility.md`. Historical and current accounting are distinguished, with all debits retained. Atomic saves, cache identity, timestamp-resolution persistence and supervisor failure handling were repaired without changing the scientific recipe.

A65 historical vintage availability and revision assumptions remain inherited limitations. All five folds, including fold 3, are development/post-selection evidence; no new confirmatory claim, economics, exposure, service-level guarantee, promotion, CP-17 or publication is authorized. Existing `DATA-LICENSE.md` and source notices remain controlling.
