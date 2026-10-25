# CP-28 report — 4.8 on stored forecasts: seven arms against the control

**Evidence class:** `development_post_selection`; 4.7T carries the protection. **Authority:** `capstone_v21.md` v21-r17 §24.8 (anchor `3124451da84c3cd99fae728c371207aace6ae537474f7769d0ff6333ee53e4fc`, section `5eaaa7c8ee418e1b4dc0029ccb66c862f3b6bc7fca1bbc451c4850bd39d84d26`), the frozen protocol `docs/track-b/evidence/cp-26/cp28-frozen-protocol-v21-r14.md` (`2b9286b0e948f59f97de33315a8b4fb3ef121003fc4ba82355b1ccf6585497a8`), the issued brief `docs/track-b/evidence/cp-28/issued-brief.md` (`57cb6d53519ede4b709face3000caca13f7358f349c9827773871ec987fb6ba3`). CP-28's Holm control is conditional on the Owner's decision to run it, which followed CP-26's report (which already showed DDNN-2 alone, A1's forecasts, on this calendar).

## The decision

**A1 is selected** (DDNN-2 alone, with its own Johnson SU quantiles): lowest WIS.

Passing all four analyses: A1, A2, A3, A4, A5, A6, A7. Primary Holm rejections: A1, A2, A3, A4, A5, A6, A7. Inconclusive (primary pass, failed a variant): none.

## Losses against the control and B0 (paired dates; descriptive intervals)

| arm | rule | dates | MAE | vs control | 95% | vs B0 | WIS | vs control | 95% | vs B0 |
|---|---|---|---|---|---|---|---|---|---|---|
| A1 | DDNN-2 alone, with its own Johnson SU quantiles | 2068 | 17.187 | -6.9% | -9.1% to -5.1% | -50.3% | 9.683 | -10.9% | -12.9% to -9.0% | -54.2% |
| A2 | equal weights (1/3, 1/3, 1/3), its own H layer | 2068 | 17.569 | -4.8% | -5.5% to -4.2% | -49.2% | 10.364 | -4.7% | -5.2% to -4.1% | -51.0% |
| A3 | global simplex-grid MAE fit on the latest ≤728 dates (min 364), deployed 0.5·fit + 0.5·w0 | 2068 | 17.435 | -5.6% | -6.3% to -4.8% | -49.5% | 10.309 | -5.2% | -5.8% to -4.5% | -51.2% |
| A4 | per-block grid fits (min 728), deployed 0.25·block + 0.75·A3 deployed; before 728 = A3 | 2068 | 17.274 | -6.4% | -7.2% to -5.5% | -50.0% | 10.231 | -5.9% | -6.6% to -5.1% | -51.6% |
| A5 | NumPy 16→8→3 meta-learner (min 364), deployed 0.5·network + 0.5·w0 | 2068 | 17.519 | -5.1% | -5.7% to -4.3% | -49.3% | 10.382 | -4.5% | -5.0% to -3.8% | -50.9% |
| A6 | A3's fit unshrunk (min 364) | 2068 | 17.100 | -7.4% | -8.7% to -5.9% | -50.5% | 10.129 | -6.8% | -8.0% to -5.5% | -52.1% |
| A7 | A5's network unshrunk (min 364) | 2068 | 17.276 | -6.4% | -7.6% to -5.0% | -50.0% | 10.294 | -5.3% | -6.3% to -4.1% | -51.3% |

Control on the same 2068 dates: MAE 18.460 EUR/MWh (-46.6% vs B0 34.553); WIS 10.871 (-48.6% vs B0 21.142). Intervals are studentized, from each arm's own primary overall-endpoint resamples; they are descriptive, never a substitute for the registered 0.995/1.02 tests.

## The compound test and Holm, in all four analyses

| analysis | A1 | A2 | A3 | A4 | A5 | A6 | A7 |
|---|---|---|---|---|---|---|---|
| primary14 | p=0.0042, adj 0.0042 **rejected** | p=1.0e-04, adj 0.0007 **rejected** | p=1.0e-04, adj 0.0007 **rejected** | p=1.0e-04, adj 0.0007 **rejected** | p=1.0e-04, adj 0.0007 **rejected** | p=1.0e-04, adj 0.0007 **rejected** | p=0.0002, adj 0.0007 **rejected** |
| sensitivity7 | p=0.0069, adj 0.0069 **rejected** | p=1.0e-04, adj 0.0007 **rejected** | p=1.0e-04, adj 0.0007 **rejected** | p=1.0e-04, adj 0.0007 **rejected** | p=1.0e-04, adj 0.0007 **rejected** | p=1.0e-04, adj 0.0007 **rejected** | p=0.0003, adj 0.0007 **rejected** |
| sensitivity28 | p=0.0022, adj 0.0022 **rejected** | p=1.0e-04, adj 0.0007 **rejected** | p=1.0e-04, adj 0.0007 **rejected** | p=1.0e-04, adj 0.0007 **rejected** | p=1.0e-04, adj 0.0007 **rejected** | p=1.0e-04, adj 0.0007 **rejected** | p=1.0e-04, adj 0.0007 **rejected** |
| unstratified14 | p=0.0053, adj 0.0053 **rejected** | p=1.0e-04, adj 0.0007 **rejected** | p=1.0e-04, adj 0.0007 **rejected** | p=1.0e-04, adj 0.0007 **rejected** | p=1.0e-04, adj 0.0007 **rejected** | p=1.0e-04, adj 0.0007 **rejected** | p=0.0002, adj 0.0007 **rejected** |

Holm sorts the seven compound p-values (ties by arm number) and compares position j with 0.05/(8−j), stopping at the first failure; failed or unexecuted arms stay in the family at p = 1. An arm passes only if Holm rejects it in the primary 14-day analysis and in each of the 7-day, 28-day and unstratified 14-day variants.

## The twenty endpoints (primary analysis)

| arm | compound p | first endpoint at the maximum | overall:overall:MAE | overall:overall:WIS | year:2021:MAE | year:2021:WIS | year:2022:MAE | year:2022:WIS | year:2023:MAE | year:2023:WIS | year:2024:MAE | year:2024:WIS | year:2025:MAE | year:2025:WIS | season:DJF:MAE | season:DJF:WIS | season:MAM:MAE | season:MAM:WIS | season:JJA:MAE | season:JJA:WIS | season:SON:MAE | season:SON:WIS |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A1 | 0.0042 | year:2025:MAE | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 0.0008 | 0.0002 | 0.0028 | 1.0e-04 | 0.0042 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 |
| A2 | 1.0e-04 | overall:overall:MAE | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 |
| A3 | 1.0e-04 | overall:overall:MAE | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 |
| A4 | 1.0e-04 | overall:overall:MAE | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 |
| A5 | 1.0e-04 | overall:overall:MAE | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 |
| A6 | 1.0e-04 | overall:overall:MAE | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 |
| A7 | 0.0002 | year:2025:WIS | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 0.0002 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 | 1.0e-04 |

Endpoint statuses across all four analyses: primary14 computable 140; sensitivity28 computable 140; sensitivity7 computable 140; unstratified14 computable 140.
Each endpoint's mean differential d = L_arm − 0.995·L_v5 (improvement) or L_arm − 1.02·L_v5 (non-inferiority) is in `results/endpoints.parquet`, with n, HAC variance, statistic, lower-tail count and status.

## Selection

Passing arms' paired WIS: A1 9.6825, A2 10.3641, A3 10.3086, A4 10.2313, A5 10.3824, A6 10.1294, A7 10.2940.
Best: A1; tie bound 9.730945278371918; tie set ['A1']; selected **A1** (simplicity order A1, A2, A3, A6, A4, A5, A7).

## Startup, support and equivalence to v5

- First CP-28 learning date (first complete all-member-valid released date): 2020-02-29.
- 364 released learning dates first reached at origin 2021-03-06 (window 2020-02-29..2021-03-04, span 370 days). Before it, A3, A5, A6 and A7 issue with v5's weights (their own H layers), and A4 equals A3.
- 728 first reached at origin 2022-03-12 (window 2020-02-29..2022-03-10, span 741 days). Until then A4 equals A3's deployed weights, so A4's early cells test A3's weights to that extent.
- Final window at 2026-09-06: 728 dates, 2024-08-25..2026-09-04 (741 days). Activation follows actual support; no date was promised.

| arm | scored dates at v5's startup weights | of which native | weight rules on scored dates |
|---|---|---|---|
| A1 | 0 | 0 | none 2068 |
| A2 | 0 | 0 | equal 2068 |
| A3 | 67 | 67 | fitted_shrunk 2001, startup_w0 67 |
| A4 | 67 | 67 | block_fitted_shrunk 1631, a3_deployed 370, startup_w0 67 |
| A5 | 67 | 67 | fitted_shrunk 2001, startup_w0 67 |
| A6 | 67 | 67 | fitted 2001, startup_w0 67 |
| A7 | 67 | 67 | fitted 2001, startup_w0 67 |

## Fallbacks, by arm, source and reason (scored dates)

| arm | scored | fallback | by source | by reason |
|---|---|---|---|---|
| A1 | 2068 | 18 | {'native': 2050, 'v5': 18} | {'member_invalid': 18} |
| A2 | 2068 | 18 | {'native': 2050, 'v5': 18} | {'member_invalid': 18} |
| A3 | 2068 | 18 | {'native': 2050, 'v5': 18} | {'member_invalid': 18} |
| A4 | 2068 | 18 | {'native': 2050, 'v5': 18} | {'member_invalid': 18} |
| A5 | 2068 | 18 | {'native': 2050, 'v5': 18} | {'member_invalid': 18} |
| A6 | 2068 | 18 | {'native': 2050, 'v5': 18} | {'member_invalid': 18} |
| A7 | 2068 | 18 | {'native': 2050, 'v5': 18} | {'member_invalid': 18} |

On the 18 fallback dates (2022-12-04 … 2023-06-20), the control's own emitted forecast, as CP-26 scored it, was: {'B0': 18} (CP-26 `scores/daily.parquet`). The copies are scored as emitted.

A missing member makes every arm use the control's complete forecast that day (then B0's); a solver failure uses A2's complete forecast; an H-history shortage, missing scale or failed H construction uses the control, then B0. Copied forecasts are scored as emitted and never enter an H buffer or the learning ledger.

## Descriptive breakdowns (point estimates; no gate)

**MAE, ratio to the control by mask, year and season.**

| arm | all | never scored | old folds | newly opened | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | DJF | MAM | JJA | SON |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A1 | -6.9% | -7.4% | -5.6% | -3.9% | -51.5% | -10.6% | -6.7% | -8.5% | -5.8% | -3.8% | -5.8% | -8.5% | -7.7% | -4.0% | -7.1% |
| A2 | -4.8% | -5.4% | -2.6% | -5.7% | -24.5% | -5.5% | -2.9% | -6.8% | -6.1% | -4.9% | -5.2% | -5.6% | -4.9% | -4.1% | -4.5% |
| A3 | -5.6% | -5.9% | -4.7% | -4.6% | -0.0% | -6.1% | -4.9% | -6.7% | -6.2% | -5.1% | -4.9% | -5.8% | -5.6% | -4.5% | -6.1% |
| A4 | -6.4% | -7.1% | -5.5% | -5.7% | -0.0% | -6.1% | -5.8% | -8.0% | -7.3% | -6.0% | -5.9% | -6.7% | -6.4% | -5.4% | -7.0% |
| A5 | -5.1% | -6.1% | -3.5% | -4.6% | -0.0% | -4.8% | -3.4% | -7.1% | -7.4% | -5.1% | -4.8% | -6.5% | -4.4% | -4.1% | -5.1% |
| A6 | -7.4% | -8.3% | -5.8% | -6.4% | -0.0% | -8.7% | -6.2% | -9.2% | -8.3% | -6.5% | -6.6% | -7.6% | -7.4% | -5.6% | -8.6% |
| A7 | -6.4% | -8.1% | -3.7% | -6.2% | -0.0% | -6.3% | -4.0% | -9.2% | -10.3% | -5.7% | -5.8% | -9.4% | -4.5% | -4.9% | -6.4% |

**WIS, ratio to the control by mask, year and season.**

| arm | all | never scored | old folds | newly opened | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | DJF | MAM | JJA | SON |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A1 | -10.9% | -10.2% | -10.0% | -11.6% | -50.0% | -13.8% | -10.0% | -11.0% | -9.6% | -10.6% | -12.2% | -10.6% | -12.3% | -9.6% | -11.3% |
| A2 | -4.7% | -5.2% | -3.0% | -4.9% | -21.9% | -5.1% | -3.8% | -6.4% | -5.6% | -3.4% | -4.4% | -5.2% | -5.2% | -4.2% | -4.1% |
| A3 | -5.2% | -5.5% | -4.3% | -4.0% | -0.0% | -6.1% | -5.1% | -6.3% | -5.5% | -3.8% | -4.1% | -5.4% | -5.4% | -4.4% | -5.5% |
| A4 | -5.9% | -6.5% | -4.9% | -4.9% | -0.0% | -6.1% | -5.9% | -7.4% | -6.4% | -4.3% | -4.9% | -6.0% | -6.2% | -5.1% | -6.2% |
| A5 | -4.5% | -5.6% | -3.1% | -4.2% | -0.0% | -4.5% | -3.2% | -6.6% | -6.3% | -3.7% | -4.0% | -5.6% | -4.0% | -3.8% | -4.4% |
| A6 | -6.8% | -7.5% | -5.3% | -5.6% | -0.0% | -8.5% | -7.0% | -8.5% | -7.1% | -4.0% | -5.5% | -6.7% | -7.3% | -5.6% | -7.6% |
| A7 | -5.3% | -7.1% | -3.1% | -5.3% | -0.0% | -5.6% | -4.0% | -8.3% | -8.0% | -3.0% | -4.2% | -7.1% | -3.9% | -4.6% | -5.4% |

**Calibration (mean daily coverage and width, EUR/MWh; descriptive).**

| arm | cov 50 | cov 80 | cov 95 | width 50 | width 80 | width 95 |
|---|---|---|---|---|---|---|
| A1 | 0.478 | 0.783 | 0.944 | 25.5 | 51.7 | 88.8 |
| A2 | 0.477 | 0.776 | 0.929 | 25.2 | 53.2 | 99.1 |
| A3 | 0.480 | 0.778 | 0.930 | 24.9 | 52.9 | 98.8 |
| A4 | 0.481 | 0.778 | 0.930 | 24.7 | 52.4 | 98.2 |
| A5 | 0.480 | 0.778 | 0.930 | 25.0 | 53.3 | 99.6 |
| A6 | 0.479 | 0.779 | 0.931 | 24.5 | 51.7 | 97.2 |
| A7 | 0.481 | 0.778 | 0.930 | 24.6 | 52.8 | 99.1 |

## The r17 GFS note (separate; outside this family)

Committed before any arm ran (`docs/track-b/evidence/cp-28/gfs-postresults/`). On 2068 paired dates GFS+6 worsens nominal v5 MAE +14.0% (registered 95% +10.3% to +16.1%) and WIS +15.5% (+12.1% to +17.6%). The weather-independent v2 is about level with the delayed-weather route on CP-25's affected dates and far behind the on-time route; the note does not recommend an availability-switching experiment on present evidence. It changes no arm, control or rule here.

## Disclosures

- **Evidence class.** Development, post-selection. CP-28 cannot establish performance on unseen data; 4.7T carries the protection. A pass is a research selection, not a confirmation.
- **The control** is nominal v5 as landed, including its day-ahead load forecast: tier 3 under the Owner's recorded exception (CP-25 rulings §1), with the historical-revision risk disclosed. The target price is tier 2 with SMARD's "update possible" caveat (§2). Prices +24 h, GFS +24 h and load +1 h are accepted structural timing risks (§3), to be measured in CP-18. GFS+6 is **fragile** (Owner ruling 2026-10-19).
- **A6 and A7 are unshrunk** (Owner, 2026-10-12): they may place any weight, up to 100%, on one member, and are the arms most exposed to overfitting and to lag at regime changes. The gates, the simplicity order and 4.7T are their protection.
- **Minimum-history equivalence.** Learned arms equal v5's weights until 364 released learning dates exist, and A4 equals A3 until 728. These are native rules, labelled `startup_w0`/`a3_deployed`, never fallbacks.
- **Identity cross-checks.** CP-28's learning dates equal CP-26's stored learning ledger: {'cp26_released_rows': 2313, 'cp28_rows_through_same_date': 2313, 'identical_dates': True}. Issue-time states against CP-26's table: {'agreeing': {'high_volatility': 2078, 'negative_price_risk': 2078, 'volatility_unknown': 2078}, 'dates': 2078, 'max_volatility_relative_difference': 6.258477696670809e-14}.
- **Bootstrap degeneracies and missing cells** are listed by status above; a deficient or uncomputable endpoint counts with p = 1 and consumes no draw.
- **No later look.** Nothing was rerun, re-specified or added after the first score.

## Reproduction and retention

- Forecast stage: `python -m cp28.pipeline forecast <root>` (manifest `reports/cp28/forecast/manifest.json`, 2441 origins, 17087 arm-days, wall 338.1 s).
- Score stage: `python -m cp28.pipeline score <root>` (manifest `reports/cp28/results/manifest.json`, wall 133.3 s).
- Bulk retention, local only: 29 files under `.local/artifacts/cp-28/bulk/bootstrap`, each listed with size and SHA-256 in `reports/cp28/results/bulk-manifest.json` (every computable endpoint's block starts and replicate statistics; the descriptive ratio pivots).
- Origin-level weights, shared-fit identifiers, window dates, scaler statistics and parameters, feature support, issue-time states, native centrals, emitted quantiles, statuses and H-buffer provenance are in `reports/cp28/forecast/`.

## Resources

Machine time, peak memory and every ledgered job are in `docs/track-b/evidence/cp-28/resources.json` (CP-28's 40-machine-hour ceiling; one worker per job, BLAS 1, CPU only, no cloud or GPU).
