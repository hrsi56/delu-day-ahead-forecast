# CP-20 research update and page copy: claim-to-evidence map

**2026-09-24 · Companion to [cp20-update.md](cp20-update.md), and the claim map for the page-wide
copy of PRES-1 (plan §8).** Each claim is mapped to a saved file and a row. The format and the
row-reference convention are those of the [CP-15/CP-16 claim map](cp15-cp16-claims.md): `L<n>` is
the physical line in the file, and for a CSV `L1` is the header. Nothing was recalculated,
refitted, replayed or downloaded; displayed values are rounded from the saved values.

**The rendered page and the README bind to these IDs.** Every research value on a public surface
carries a claim ID from this map or the CP-15/CP-16 map, and a record ID from
`src/delu_forecast/research.py`. `tests/test_30_research_claims_rendered.py` fails if a rendered
claim ID is missing from both maps.

**Default evidence class.** Every CP-20 result is **`development_post_selection`** and
exploratory ([R20](../../../reports/weather-ablation/report.md) L5, [I20](../evidence/cp-20/integration.md)).

## Source keys

| Key | File |
|---|---|
| R20 | [reports/weather-ablation/report.md](../../../reports/weather-ablation/report.md) |
| M20 | [reports/weather-ablation/metrics.csv](../../../reports/weather-ablation/metrics.csv) |
| U20 | [reports/weather-ablation/uncertainty.csv](../../../reports/weather-ablation/uncertainty.csv) |
| C20 | [reports/weather-ablation/criteria.csv](../../../reports/weather-ablation/criteria.csv) |
| D20 | [reports/weather-ablation/diagnostics.csv](../../../reports/weather-ablation/diagnostics.csv) |
| MS20 | [reports/weather-ablation/missingness.csv](../../../reports/weather-ablation/missingness.csv) |
| CC20 | [reports/weather-ablation/causal-controls.json](../../../reports/weather-ablation/causal-controls.json) |
| CS20 | [reports/weather-ablation/causal-controls-supplement.json](../../../reports/weather-ablation/causal-controls-supplement.json) |
| PF20 | [reports/weather-ablation/post-freeze-repairs.json](../../../reports/weather-ablation/post-freeze-repairs.json) |
| RN20 | [reports/weather-ablation/rights-notice.md](../../../reports/weather-ablation/rights-notice.md) |
| RF20 | [docs/track-b/evidence/cp-20/resource-final.json](../evidence/cp-20/resource-final.json) |
| I20 | [docs/track-b/evidence/cp-20/integration.md](../evidence/cp-20/integration.md) |
| IA20 | [docs/track-b/evidence/cp-20/integration-attempt-1/integration.md](../evidence/cp-20/integration-attempt-1/integration.md) |
| LD20 | [docs/track-b/cp-20-landing-2026-09-24.md](../cp-20-landing-2026-09-24.md) |
| DL | [DATA-LICENSE.md](../../../DATA-LICENSE.md) |
| PK15 | [reports/cp15/peak.csv](../../../reports/cp15/peak.csv) |
| RS15 | [reports/cp15/relative_scores.csv](../../../reports/cp15/relative_scores.csv) |
| RK15 | [reports/cp15/ranking.csv](../../../reports/cp15/ranking.csv) |
| BM15 | [reports/cp15/bootstrap_metadata.json](../../../reports/cp15/bootstrap_metadata.json) |
| M16 | [reports/v2-causal/metrics.csv](../../../reports/v2-causal/metrics.csv) |
| C16 | [reports/v2-causal/criteria.csv](../../../reports/v2-causal/criteria.csv) |
| PW10 | [reports/cp10/peak_windows.csv](../../../reports/cp10/peak_windows.csv) |
| SEL10 | [reports/cp10/selection.json](../../../reports/cp10/selection.json) |
| DM2 | [reports/cp2/dm_development.json](../../../reports/cp2/dm_development.json) |
| PM2 | [reports/cp2/development_pooled_metrics.csv](../../../reports/cp2/development_pooled_metrics.csv) |
| V1 | [`src/delu_forecast/claims.py`](../../../src/delu_forecast/claims.py), the one v1 claim set |
| DEMO | [reports/presentation/release-checks/2026-09-24-demo.json](../../../reports/presentation/release-checks/2026-09-24-demo.json) |
| CAP | [capstone_v21.md](../../../capstone_v21.md) (v21-r4): §7, §8, §14.4, §15.1–15.4 |
| PLAN | [presentation-and-tracking-plan-2026-09-24.md](../presentation-and-tracking-plan-2026-09-24.md) (revision 3, Owner-approved) |
| REV | The Owner's D1 editorial review, 2026-09-25: [`docs/track-b/evidence/pres-1/presentation-d1-editorial-review-2026-09-25.md`](../evidence/pres-1/presentation-d1-editorial-review-2026-09-25.md), byte-identical to the Owner's file |
| AUD | The Owner's final editorial audit, 2026-09-28: [`docs/track-b/evidence/pres-1/presentation-final-editorial-audit-2026-09-28.md`](../evidence/pres-1/presentation-final-editorial-audit-2026-09-28.md) |
| HR2 | [reports/cp2/holdout_report.json](../../../reports/cp2/holdout_report.json) |

## Claim map: CP-20

Status codes, as in the CP-15/CP-16 map: **S** supported by a saved value or verdict; **S-d**
supported, descriptive only; **I** an inference from design plus saved values, usable only in the
wording given; **Def** a definition; **O** an Owner decision.

### Status, identity and retrieval

| ID | Claim as used | Source → table/row | Status |
|---|---|---|---|
| C60 | CP-20 Integration **PASS** at final candidate `3e9ff8b500c2c655fea810ae11886503927f176c`. Integration attempt 1 **FAIL** at `a7943fb6262c1a50b729bd92fe701c8be9428038`. | I20 L1; IA20 L1; PF20 `integration_attempts`; LD20 "Landing and preservation" | S |
| C61 | Retrieval: `evidence/cp-20` = `a7a9b2e3a4d0147a0c82835a853277e9c81c7945`; `land/cp-20` = `f450bc1a98c70544d8b1fb84c3496986551abb7f`. | LD20 "Landing and preservation" | S |
| C62 | No promotion, freeze, live policy, CP-17, prospective clock or product qualification follows. | R20 L3; CAP §15.4 last sentence; LD20 "Scientific status" | S |

### Population, arms and definitions

| ID | Claim | Source → table/row | Status |
|---|---|---|---|
| C63 | The same 10,747 eligible hours in five folds (2,160 / 2,159 / 2,112 / 2,160 / 2,156). Fold 3 has 2,112 hours on 88 dates; the crisis window 2022-08-15..31 has 408 hours on 17 days. No key was dropped. | R20 L144; M20 L2 (`n_hours`), L33–37; D20 L837, L977 | S |
| C64 | H0 is CP-16's V2-H, reproduced bitwise on all 10,747 keys. | R20 L144 (`bitwise_equal: True`, `max_abs_difference: 0.0`) | S |
| C65 | HG uses the same A1/B2 recipes with three weather columns (and their missing indicators) appended; same blend, interval recipe, histories, folds, penalty search and seed 42; each arm uses its own issued errors. | CAP §15.1, §15.2 item 4; R20 L144 | Def/S |
| C66 | Weather: operational GFS 0.25°, D−1 00 UTC, from NCAR GDEX and NOAA NODD on AWS; a fixed 47–55.25°N, 5.5–15.5°E box with cos(latitude) weights; mean wind speed at 10 m and 100 m (per cell before averaging) and mean DSWRF (de-averaged). A regional proxy, not a DE-LU polygon or a generation forecast. | CAP §15.2 items 1–4; R20 L148–150; RN20 "Source" | Def/S |
| C67 | Only delivery 2019-01-01 is missing, structurally; no run was classified missing and nothing was imputed from a failed retrieval. | MS20 L2; R20 L150 | S |
| C68 | S_MAE/S_WIS are equal-fold ratios to B0; the joint improvement rule needs upper ΔS_WIS < 0 and upper ΔS_MAE ≤ 0; intervals are a paired 7-day block bootstrap, seed 15042, 2,000 replicates, 95% percentile. | CAP §7, §14.4, §15.4; U20 `replicates`, `confidence` (L2–13); BM15 | Def |

### Primary contrast

| ID | Claim | Source → table/row | Status |
|---|---|---|---|
| C69 | ΔS_MAE (HG − H0) = −0.0783, 95% interval [−0.1006, −0.0570]. | U20 L12 | S |
| C70 | ΔS_WIS (HG − H0) = −0.0838, 95% interval [−0.1044, −0.0655]. | U20 L13 | S |
| C71 | Both intervals lie wholly below zero: **observed joint improvement**, exploratory, development after selection. | U20 L12–13; R20 L5; I20 | S |
| C72 | Per fold (EUR/MWh, paired mean daily loss difference), all five point estimates favour HG for MAE and for WIS. | U20 L2–11 | S-d |
| C73 | In fold 3 the MAE difference is −3.18 [−6.09, +0.037]: the interval crosses zero. | U20 L6 | S-d |

### Scores and diagnostics

| ID | Claim | Source → table/row | Status |
|---|---|---|---|
| C74 | Equal-fold scores of the seven policies: HG 0.5658/0.5322, H0 0.6441/0.6160, B2 0.6578/0.6390, A1 0.6723/0.6460, B3 0.7841/0.7399, B1 1.0518/0.9856, B0 1.0000/1.0000; pooled MAE/WIS in EUR/MWh from the pooled rows. | M20 L44–50; pooled L2, L8, L14, L20, L26, L32, L38 | S |
| C75 | The references (B0–B3, A1) are identical in CP-15, CP-16 and CP-20, and H0 equals CP-16 V2-H. | RS15 L2–6; M16 L44–49; M20 L44–49; R20 L144 | S |
| C76 | B1 is v1's development replay on the same 448 development days as v1's own report. | M20 L8 (`n_days` 448); DM2 (`n_days` 448) | S |
| C77 | HG meets all six original §8 criteria; H0 misses criteria 1 and 2 (0.6441 > 0.59203; 0.6160 > 0.57509) and meets 3–6. Limits: 0.59203, 0.57509; crisis MAE 57.62, WIS 33.73. | C20 L2–43 | S |
| C78 | HG is the first policy evaluated against the original §8 criteria in this programme to meet all six: the CP-15 challengers failed 1, 2 and 5 (A2 also 4), and CP-16's H and P failed 1 and 2. | C20 L23–43; RK15 L2–6; C16 L2–3, L22–23 | I |
| C79 | Crisis window (descriptive): v1 275.26 EUR/MWh and 79/408 hits; A1 49.88 and 378/408; v2 52.51 and 377/408; v3 47.52 and 383/408. | PK15 L8, L2; C20 L10, L31; D20 L837, L977 (`hit_count95`) | S-d |
| C80 | v3's mean 95% interval width is lower than v2's in every fold (pooled 106.24 against 124.64 EUR/MWh); its pooled 95% coverage is 0.9377 against 0.9389; its fold 95% coverage is slightly lower than v2's in folds 2–5; every fold stays within 0.90–0.98. | M20 L32–43 (`mean_width95`, `coverage95`); C20 L25–29 | S-d |
| C81 | Pooled 50% coverage: v3 0.4937, v2 0.4993. Pooled 80%: v3 0.7914, v2 0.7906. | M20 L32, L38 | S-d |
| C82 | Per-fold MAE by local hour for H0 and HG is shown descriptively; no hour or block effect is claimed. | D20 L702–833 (H0), L842–973 (HG), scope `hour` | S-d |

### Limitations

| ID | Claim | Source → table/row | Status |
|---|---|---|---|
| C83 | The three weather features were added together; no arm isolates any one of them, so the gain is not attributed to a single feature. | CAP §15.1 ("no feature subset"), §15.2 item 4 | Def/I |
| C84 | The folds are known historical periods; the results are development evidence after selection and cannot become unseen evidence. | R20 L156; CAP §15.4 | S |
| C85 | Availability of each GFS run before D−1 11:00 UTC is reconstructed, not a per-day delivery guarantee; admission does not certify live use. | R20 L152; CAP §15.2 | S |
| C86 | The box is a fixed rectangle, not the DE-LU zone, and the features are weather, not generation. | CAP §15.2 item 3; R20 L148 | Def |
| C87 | Inherited A65 vintage and revision assumptions carry over; residual intervals are empirical with no conformal guarantee. | R20 L156; CAP §6 | S |
| C88 | v3 does not run in the demo; the released product and the in-browser demo are v1. | V1 (`SHIPPED_IS_EVALUATED`, `wasm_identity`); `space-wasm/README.md` | S |

### Protocol, review and cost

| ID | Claim | Source → table/row | Status |
|---|---|---|---|
| C89 | Frozen causal controls on 2020-07-01 and 2025-05-01: delivery-day/future mask 0.0; available D−1 price mutation moved the forecast; future weather 0.0. | CC20 `controls` | S |
| C90 | The frozen ×3 weather control could not fail (the training-only scaler undoes it); it was kept as an invariance check and two controls that can fail were added, both passing (r13). | PF20 `repairs` r13; CS20 `all_passed` | S |
| C91 | Integration attempt 1 failed because a frozen input's recorded hash was that of its bytes with Windows line endings, so the reproduction commands refused to run in a clean checkout; the bytes were restored to the recorded identity (r14) and a fresh review passed. | IA20 L101, L108; PF20; I20 L116 | S |
| C92 | 2,476 GFS runs and 123,800 decoded messages; 136.0 GiB transferred; 40.09 machine-hours; $0 external cost. | R20 L150; RF20 `transfer_gib`, `machine_hours`, `external_cost_usd` | S |
| C93 | v3 needs a daily GFS retrieval; delivery 2019-01-01 is structurally missing. | CAP §15.2; MS20 L2 | S |
| C94 | The GFS attribution line, verbatim. | DL L26–28; RN20 "Attribution" | S |

### Decision

| ID | Claim | Source → table/row | Status |
|---|---|---|---|
| C95 | Decision story (problem, hypothesis, change, result, limitation) and adoption of HG as the current research model, **v3 · weather features**. "Adopted" means adopted within this research programme. | PLAN §8.3, §7.7, §7.8, §16 decision 2; C69–C80 | O |

## Claim map: page-wide copy (PRES-1)

These claims carry the page's own wording. Numbers in them come from the records cited.

| ID | Claim | Source → table/row | Status |
|---|---|---|---|
| P01 | Eyebrow and title: "German–Luxembourg electricity market"; "Day-ahead electricity forecasts, with uncertainty." | PLAN §8.1; REV §4A | Copy |
| P02 | Description: "Explore hourly price forecasts and prediction intervals on historical days. See how successive research models improved, what failed, and how each result was checked." | PLAN §8.1; REV §4A | Copy |
| P03 | Status pair: demo **v1** · Released model; research **v3** · Weather features, Development · post-selection. | PLAN §8.1; REV §4A; C95 | O |
| P04 | The opening's research takeaway, qualitative and with no number: adding weather inputs improved both point-error and interval scores against v2 in development tests; performance on future data is still to be evaluated. It rests on both equal-fold differences and their 95% intervals lying wholly below zero (ΔS_MAE −0.0783 [−0.1006, −0.0570]; ΔS_WIS −0.0838 [−0.1044, −0.0655]), shown in the v3 chapter. | C69, C70 (U20 L12–13); C95 | S |
| P05 | The product preview, labelled "Historical forecast · v1": v1's saved historical replay for the default delivery day, ×1.00 load scenario, 80% level, captioned as a historical replay, not a live forecast; "Explore this forecast" opens the replay in the original v1 report. | V1 (`replay_label`); `scripts/build_pages.py` fan-chart payload; REV §4A | S |
| P06 | Lineage in plain words: v1 is the released demo; v2 changed the forecasting approach (blended LEAR, hour-aware intervals); v3 added weather inputs. Two branches: the calibration experiment (CP-10), not adopted because recalibrating v1 was not enough, and the model comparison study (CP-15), which informed v2. | PLAN §7.7, §8.4; REV §4B; C95; SEL10; RK15 | O/S |
| P07 | The overview comparison, titled "v3 leads the shared development comparison." with the subtitle "Seven policies · the same 10,747 historical hours · equal-weight averages across five periods. Lower scores are better.": equal-fold S_MAE and S_WIS against the similar-day naive, development after selection; reference lines at 1.00 and at the diagnostic limits 0.59203 and 0.57509, which are not certification. **PRES-2 (2026-09-29):** the subtitle states the represented days beside the hours from the same committed row, "7 policies · the same 10,747 historical hours over 448 days · …", with the row count taken from the registry's comparison (review F04; plan §7.9). | C74; C77 (C20 L2–3); M20 L2 (`n_hours`, `n_days`); AUD §4 | S |
| P08 | Fairness note: the shared population of 10,747 hours over 448 days, equal-fold scoring and development status; one level deeper, the bootstrap settings and the fold table. | C63; C68; M20 L2 (`n_days`) | S/Def |
| P09 | F07 note: v1 scores 1.05 in the shared development comparison and "28.58% worse" in its own report over the same 448 days. v1's report compares with the raw similar-day naive (MAE 32.45 EUR/MWh) and pools all days; this comparison weights five folds equally against the naive's emitted median after the common residual layer (MAE 32.81 EUR/MWh). v1's own MAE is 41.74 EUR/MWh in both. | DM2 (`relative_improvement_pct`, `n_days`); PM2 L4, L8; M20 L2, L8, L45 | S |
| P10 | Planned, not evaluated: a one-sentence teaser, then a closed disclosure with descriptive names first — alternative model families (4.6 DDNN/TabPFN), wind and solar generation forecasts (4.4V VRE), models for different parts of the day (4.5 three-block LightGBM; "Do separate models for different hours improve forecasts?"), combining models (4.8), and a frozen-protocol evaluation then prospective monitoring (4.7T and live), whose evaluation window and evidence classification remain to be finalized (PLAN §15); each with its question and the evidence that would decide it, "subject to the active plan"; no score, version number or date. | PLAN §8.6, §15; AUD F05 | O |
| P11 | v1 chapter: the one-shot holdout values under the exact label, with the holdout Diebold–Mariano test identified as a one-sided test on the daily pinball-loss vectors (it tests the probabilistic forecast, not the MAE difference); the two unflattering results (development point error 28.58% worse than the naive's, pooled over all days, with a one-sided test for an improvement at p = 0.948, so no evidence of an advantage; 0.194 crisis coverage); the crisis lesson: bias −269.45, level MAE 269.45 against shape MAE 66.88 EUR/MWh on the crisis window. | V1 (`holdout_*`, `development_dm_point_*`, `limitation_coverage_divergence`); HR2 `dm.analysis` = `probabilistic_daily_vector_pinball`; PK15 L8 (`bias`, `daily_mean_level_MAE`, `within_day_shape_MAE`); AUD F06 | S |
| P12 | CP-10: recalibrating v1 without refitting raised crisis-window 95% coverage from 19.36% to 32.11% (79/408 → 131/408); not adopted. | PW10 L2, L4; SEL10 `same_window_diagnostic` | S |
| P13 | Demo startup: a short visible note (runs in the browser; about 57 MB on a first visit; startup time varies) and a closed disclosure with what the demo does and the recorded cold-start measurement — seconds, browser, machine and date read from the release record, never typed into the generator. **PRES-2 (2026-09-29):** the measured start, browser, machine, date and last verification date moved beside the action, outside the disclosure (review F03; plan §7.11); see P34. | V1 (`wasm_cold_load_mb`); DEMO `runs`, `playwright_host`, `date`; REV §4A | S |
| P14 | Adoption labels and evidence badges are separate signals; "Adopted" never implies deployment or outside validation. | PLAN §7.8 | Def |
| P15 | Contribution statement: the Owner's wording as approved at Stop 1 on 2026-09-25 (the D1 review's proposed replacement for the plan §8.9 rendering), displayed as written and signed with the Owner's approved public name, which also appears once as a byline near the opening ("Led by …", linked to the statement). Not a research claim. | PLAN §8.9; REV §5.2, §5.4; the Owner's Stop 1 answers, 2026-09-25 | O |

## Gaps: documented, not resolved

| ID | Gap | Why it stays open |
|---|---|---|
| G11 | No cross-fold average by hour is shown: C5 shows the saved per-fold hour rows only. | Averaging across folds would be a new aggregate; the per-fold rows are enough for a descriptive view. |
| G12 | C3 gives each fold its own labelled scale, shared by the three generations inside the fold. | v1's crisis-fold MAE (140.99) would otherwise hide v2 and v3 in every other fold; the paired view is C2b. |
| G13 | The demo's measured start time depends on the device, network and browser. | Published with its context (P13), never as a universal duration. |
| G14 | The Owner's demo device test (2026-09-24) has no recorded device, browser or outcome. | Requested at Stop 1 (DEMO `owner_device_test`). |
| G15 | MLflow comparison and run routes are advertised only after the authorized upload and both route checks. | PLAN §10.10, §12 Phase F. Until then the evidence row shows them as unavailable. |

## Withheld claims: do not use

W1–W16 are in the [CP-15/CP-16 map](cp15-cp16-claims.md#withheld-claims-do-not-use) and stay in
force. PRES-1 adds:

| ID | Withheld claim | Reason / controlling source |
|---|---|---|
| W17 | Attributing the weather gain to any single feature ("wind drives the gain", "radiation helps") | No arm isolates a feature (C83; PLAN §8.8). |
| W18 | Calling the Integration review "peer review" or "external validation" | It is an independent Integration review within this project's process (PLAN §7.6, §8.8). |
| W19 | Stating or implying that v3 runs in the demo or live | The demo and the released product are v1 (C88). |
| W20 | Comparing v3 with v1 as a headline ratio without the comparison's definition and the development label | PLAN §8.1, §8.8; the F07 note (P09) explains why the two v1 figures differ. |
| W21 | Calling v1's holdout "confirmatory" without "-style, not power-qualified" | The exact label is "confirmatory-style, not power-qualified" (V1 `HOLDOUT_DM_LABEL`; PLAN §6 invariant 4). |

## Exact unresolved items for the Owner

1. **G14:** the device, browser and outcome of the 2026-09-24 demo test.
2. **P15:** confirm the English rendering of the contribution statement (PLAN §8.9) at D1.
3. **G15:** MLflow routes stay unavailable on the page until the Owner authorizes the upload (F1)
   and the route checks pass (F3).
