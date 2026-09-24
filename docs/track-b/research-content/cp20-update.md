# CP-20 research update: weather features on the v2 policy (development evidence, post-selection)

**2026-09-24 · PRES-1 content (plan §8.3, §8.8). Prepared for public release; the Owner reviews it
before anything is published.** Every number here is copied from a saved file and rounded for
display. Nothing was recalculated, refitted, replayed or downloaded. Each statement is traced in
the [claim-to-evidence map](cp20-claims.md), which also lists gaps and withheld claims. The v2
content is in the [CP-15/CP-16 update](cp15-cp16-update.md).

> **Evidence class.** Every CP-20 result is **`development_post_selection`**. All comparisons and
> intervals are exploratory. There are no confirmatory, family-wise, product or economic claims.

## Status at a glance

| | CP-20 (capstone v21-r4, §15) |
|---|---|
| Engineering | **Integration PASS** at final candidate `3e9ff8b500c2c655fea810ae11886503927f176c` ([verdict](../evidence/cp-20/integration.md)). The first review **failed** at candidate `a7943fb6262c1a50b729bd92fe701c8be9428038` ([verdict](../evidence/cp-20/integration-attempt-1/integration.md)). |
| Primary contrast | **HG − H0: observed joint improvement.** Both upper interval endpoints are below zero. |
| Original §8 diagnostics | HG meets all six criteria. H0 (= v2) misses criteria 1 and 2 and meets 3–6. |
| Product status | Unchanged. No promotion, freeze, live policy, CP-17 or prospective clock follows from this result. |
| Retrieval | `evidence/cp-20` → `a7a9b2e3a4d0147a0c82835a853277e9c81c7945`; `land/cp-20` → `f450bc1a98c70544d8b1fb84c3496986551abb7f` ([landing record](../cp-20-landing-2026-09-24.md)) |

**Naming on public surfaces.** HG is **v3 · weather features**. H0 is **v2 · blended LEAR,
hour-aware intervals**: it is CP-16's V2-H, reproduced bitwise on all 10,747 keys. v3 is the
current research model. The released product, and the model the demo runs, is still **v1**.

## What was compared

- **Population.** The same **10,747** eligible target hours as CP-15 and CP-16, in five
  90-calendar-day folds (2,160 / 2,159 / 2,112 / 2,160 / 2,156 hours). Full fold 3 (the 2022
  crisis) has 2,112 hours on 88 dates. The crisis window 2022-08-15..31 has 408 hours on 17 days.
  No denominator changed, and no eligible key was dropped.
- **H0 (v2).** The no-weather CP-16 V2-H policy: a 50/50 blend of the A1 and B2 central
  forecasts, with hour-aware residual intervals.
- **HG (v3).** The same A1 and B2 recipes with **three weather columns appended**, the same 50/50
  blend and the same interval recipe. Each arm uses only its own issued errors.
- **Nothing else changed.** Same histories, folds, penalty search, seed 42 and release rules. No
  extra lag, interaction, feature subset, blend weight or residual tuning.

### The weather features

- **Source.** Operational NCEP GFS 0.25°, the 00 UTC run of the day before delivery, from the NCAR
  GDEX archive and the NOAA Open Data Dissemination bucket on AWS.
- **Region.** A fixed rectangle, **47–55.25°N, 5.5–15.5°E**, averaged with cos(latitude) weights. It
  is a regional weather proxy, not an exact DE-LU polygon and not a generation forecast.
- **The three features, for each delivery hour:**
  - mean wind speed at 10 m;
  - mean wind speed at 100 m;
  - mean downward shortwave radiation (DSWRF).
- **Recipe.** Wind components are interpolated in time; wind speed is computed per grid cell
  before the area average; DSWRF is de-averaged from the forecast's running means. Each feature
  also gets a missing indicator.
- **Missing weather.** Only delivery 2019-01-01 is missing, structurally: its run would be
  2018-12-31, before the input floor. Nothing was imputed from a failed retrieval.

## How the scores are defined

The definitions are unchanged from CP-15 and CP-16 ([capstone](../../../capstone_v21.md) §7,
§14.3, §15.4):

- **S_MAE, S_WIS (primary).** The mean of the five per-fold ratios to the similar-day naive (B0),
  with equal weight per fold. Lower is better. MAE uses the emitted p50. WIS uses seven
  quantiles.
- **Pooled MAE and WIS.** Weighted over all 10,747 hours, in EUR/MWh. Secondary description only.
- **The joint improvement rule.** "Observed joint improvement" needs the upper end of the ΔS_WIS
  interval below zero **and** the upper end of the ΔS_MAE interval at or below zero. Otherwise the
  result is "no demonstrated joint preference", which is not equivalence.
- **Intervals.** Paired moving-block bootstrap: seed 15042, 2,000 replicates, 7-calendar-day
  blocks, 95% percentile intervals. Exploratory, post-selection.

## Primary result: HG − H0

| Difference (v3 − v2) | Estimate | 95% interval |
|---|---:|---|
| ΔS_MAE, normalized point error | −0.0783 | [−0.1006, −0.0570] |
| ΔS_WIS, normalized interval score | −0.0838 | [−0.1044, −0.0655] |

Negative values favour v3. Both intervals lie wholly below zero, so the joint improvement rule is
met: **observed joint improvement**, development evidence after selection.

**Fold by fold** (paired mean daily loss difference, EUR/MWh; descriptive):

| Fold | ΔMAE | 95% interval | ΔWIS | 95% interval |
|---|---:|---|---:|---|
| 1 | −1.06 | [−1.68, −0.52] | −0.65 | [−1.01, −0.36] |
| 2 | −1.08 | [−2.00, −0.26] | −0.85 | [−1.43, −0.39] |
| 3 (crisis) | −3.18 | [−6.09, **+0.037**] | −2.43 | [−4.02, −0.78] |
| 4 | −1.49 | [−2.72, −0.20] | −1.03 | [−1.79, −0.30] |
| 5 | −3.10 | [−4.19, −1.70] | −1.98 | [−2.44, −1.28] |

All five point estimates favour v3. **In fold 3, the 2022 crisis, the MAE interval crosses zero**:
its upper end is +0.037 EUR/MWh.

## The seven policies on the same hours

S-scores are ratios to B0 (lower is better). Pooled values are EUR/MWh.

| Policy | S_MAE | S_WIS | Pooled MAE | Pooled WIS |
|---|---:|---:|---:|---:|
| v3 · weather features (HG) | 0.5658 | 0.5322 | 18.26 | 10.67 |
| v2 · blended LEAR, hour-aware intervals (H0 = V2-H) | 0.6441 | 0.6160 | 20.23 | 12.05 |
| Daily LEAR (reference, B2) | 0.6578 | 0.6390 | 20.98 | 12.66 |
| Normalized LEAR (study challenger, A1) | 0.6723 | 0.6460 | 20.71 | 12.45 |
| Daily LightGBM (reference, B3) | 0.7841 | 0.7399 | 26.32 | 15.17 |
| v1 · released LightGBM (development replay, B1) | 1.0518 | 0.9856 | 41.74 | 25.25 |
| Similar-day naive (normalizer, B0) | 1.0000 | 1.0000 | 32.81 | 20.02 |

The references are identical to CP-15 and CP-16. B1 is v1's development replay: the same 448
development days as v1's own report, scored here on the shared seven-quantile grid.

## Original §8 diagnostics

| Criterion | Limit | H0 (v2) | HG (v3) |
|---|---|---|---|
| 1. S_MAE ≤ 0.90 × best B0–B3 | 0.59203 | 0.6441, not met | 0.5658, met |
| 2. S_WIS ≤ 0.90 × best B0–B3 | 0.57509 | 0.6160, not met | 0.5322, met |
| 3. 95% coverage 0.90–0.98 in every fold | — | met | met |
| 4. Crisis window: coverage ≥ 0.90; MAE and WIS no worse than best B0–B3 | MAE 57.62, WIS 33.73 | met | met |
| 5. Every fold: MAE and WIS ≤ 1.05 × best rolling B2/B3 | per fold | met | met |
| 6. Complete, finite, ordered forecasts | — | met | met |

As a diagnostic, HG is the first policy evaluated against these criteria in this programme to
meet all six. The CP-15 challengers failed criteria 1, 2 and 5 (A2 also 4), and CP-16's H and P
failed criteria 1 and 2. This is a development diagnostic, not a product qualification.

## Where it helps and where it does not

- **The crisis window, 2022-08-15..31** (408 hours; descriptive only):

  | Generation | MAE (EUR/MWh) | Hits inside the 95% interval |
  |---|---:|---:|
  | v1 · released LightGBM | 275.26 | 79/408 |
  | Normalized LEAR (A1) | 49.88 | 378/408 |
  | v2 | 52.51 | 377/408 |
  | v3 | 47.52 | 383/408 |

- **Narrower intervals, coverage close to v2's.** v3's mean 95% interval width is lower than v2's
  in every fold (pooled 106.24 against 124.64 EUR/MWh). Its pooled 95% coverage is 0.9377 against
  0.9389, and its fold 95% coverage is slightly lower than v2's in folds 2–5. Every fold stays
  inside 0.90–0.98.
- **The 50% interval.** Pooled 50% coverage is 0.4937 for v3 and 0.4993 for v2.
- **Hours of the day.** Per-fold MAE by local hour is saved for both arms and is shown as a
  descriptive chart only. No hour or block effect is claimed.

## Limitations

- **The gain belongs to the bundle.** The three weather features were added together. No arm
  isolates wind at 10 m, wind at 100 m or radiation, so the improvement is not attributed to any
  single feature.
- **Fold 3.** The crisis-fold MAE interval crosses zero (upper end +0.037 EUR/MWh).
- **Development status.** The folds are known historical periods, and the 2022 crisis motivated
  the programme's hypotheses. The results are development evidence after selection. They cannot
  become unseen evidence, and no prospective clock has started.
- **Weather availability is reconstructed.** Public availability of each GFS run before D−1
  11:00 UTC is reconstructed from dated NCEP production-status averages with an assumed
  dissemination lag. It is not a per-day delivery guarantee, and admission does not certify live
  use.
- **A regional proxy.** The box is a fixed rectangle, not the DE-LU bidding zone, and the features
  are weather, not generation.
- **Inherited assumptions.** The A65 load-forecast vintage and revision assumptions carry over.
  Residual intervals are empirical; they carry no conformal coverage guarantee.
- **v3 does not run in the demo.** The released product and the in-browser demo are v1.

## Protocol and review details

- **Frozen causal controls ran as planned** on two real days (2020-07-01 and 2025-05-01): a
  delivery-day or future mask changed the forecast by exactly 0.0, an available D−1 price
  mutation moved it, and future weather changed nothing.
- **Supplementary controls were added after one frozen check was found unable to fail.** The
  frozen positive control multiplied all available weather by 3; the training-only scaler undoes
  that, so it "passed" on floating-point noise. It was kept and relabelled as an invariance check,
  and two controls that can fail were added: a shift of the target day's weather and a seeded
  permutation of the training-history weather. Both passed (repair r13).
- **The first independent review failed; a fresh review passed.** Integration attempt 1 found that
  one frozen input's recorded hash was the hash of its bytes with Windows line endings, so the
  reproduction commands refused to run in a clean checkout. The file's bytes were restored to the
  recorded identity (repair r14), and a fresh Integration review passed at the final candidate.
  This is an independent Integration review within this project's process, not peer review or
  external validation.
- **Cost:** 2,476 GFS runs and 123,800 decoded messages; 136.0 GiB transferred; 40.09
  machine-hours; $0 external cost. No GPU and no cloud compute.
- **Dependency.** v3 needs a daily GFS retrieval. Delivery 2019-01-01 is structurally missing.
- **Weather attribution.** Weather: derived from NCEP GFS 0.25° (NOAA/NWS/NCEP) via NCAR GDEX
  d084001 (doi:10.5065/D65D8PWK) and NOAA Open Data Dissemination on AWS. Modified and aggregated
  by this project; not an official NOAA product.

## Decision

- **Problem.** v2 used market data only.
- **Hypothesis.** Forecast wind and solar drive both the level and the shape of prices.
- **Change.** Three frozen weather features, added to v2's recipes without other changes.
- **Result.** The joint improvement rule is met, and all five folds favour v3. As diagnostics, v3
  is the first policy evaluated against the original §8 criteria to meet all six.
- **Limitation.** The bundle, fold 3 and development status, above.
- **Decision.** Adopted as the current research model (**v3 · weather features**). Adopted means
  adopted within this research programme; it is not deployed and not externally validated.

## Reproduction

The reviewed instructions are in [`reports/weather-ablation/reproduce.md`](../../../reports/weather-ablation/reproduce.md).
They were **not run** for this update: the CP-20 analysis and reference passes are exhausted, and
the presentation reads saved outputs only. Exact historical bytes: `git show evidence/cp-20:<path>`.

## Chart specifications

| # | Chart | Unit | Placement | Data |
|---|---|---|---|---|
| C2a | Equal-fold HG − H0 for ΔS_MAE and ΔS_WIS; negative favours v3; zero and the full interval extent shown | Normalized score (ratio to B0) | Main chart | `uncertainty.csv` L12–13 |
| C1 | The GFS box and the feature recipe | — | Disclosure "How the weather features are built" | Static (this document) |
| C2b | HG − H0 per fold, MAE and WIS in separate panels; fold 3's crossing of zero never cropped | EUR/MWh, paired mean daily loss difference | Disclosure "Consistency across folds" | `uncertainty.csv` L2–11 |
| C3 | MAE and WIS per fold for v1, v2 and v3; each fold on its own labelled scale, the three generations sharing it | EUR/MWh | Same disclosure | `metrics.csv` per-fold rows |
| C4 | Crisis window MAE and 95% hits | EUR/MWh; hits out of 408 | Disclosure "Crisis window" | CP-15 `peak.csv` (v1, A1); `criteria.csv` criterion 4 and `diagnostics.csv` peak rows (v2, v3) |
| C5 | MAE by local hour, v2 against v3, one panel per fold | EUR/MWh | Disclosure "Hours of the day" | `diagnostics.csv` hour rows |
| C6 | Coverage and mean interval width at 50%, 80% and 95% | Fraction; EUR/MWh | Disclosure "Coverage and interval width" | `metrics.csv` pooled rows |

C2 never invents a normalized interval per fold: the per-fold intervals are in EUR/MWh.

## README and site summary

> **v3 · weather features (CP-20, development evidence after selection).** Adding three frozen
> GFS weather features (mean wind speed at 10 m and 100 m, and mean solar radiation over a fixed
> regional box) to the v2 policy changed the normalized point error by −0.0783 [−0.1006, −0.0570]
> and the normalized interval score by −0.0838 [−0.1044, −0.0655] on the same 10,747 historical
> hours; negative favours v3. All five folds favour v3, although the crisis fold's MAE interval crosses zero. The gain
> belongs to the three features together; no experiment isolates one of them. v3 is the current
> research model. The released product and the in-browser demo are v1.
