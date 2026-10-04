# CP-23 research result: claim-to-evidence map

**2026-10-04 · Draft for the next publication (PUBLISH_RULES 1.3 §11; capstone v21-r10 §21.9).** Each claim the
publication may render is mapped to a committed file and row, in the format of the [CP-22](cp22-claims.md) map: `L<n>`
is the physical line in the file, and for a CSV `L1` is the header. Values here are rounded from the saved values; the
rendered surfaces bind to evidence records, never to these digits. The publication block registers this map after the
Owner's landing, and only if the Owner decides to publish the branch.

**Default evidence class.** Every CP-23 result is **`development_post_selection`** and exploratory.

## Source keys

| Key | File |
|---|---|
| R23 | [reports/distribution-challenger/report.md](../../../reports/distribution-challenger/report.md) |
| M23 | [reports/distribution-challenger/metrics.csv](../../../reports/distribution-challenger/metrics.csv) |
| U23 | [reports/distribution-challenger/uncertainty.csv](../../../reports/distribution-challenger/uncertainty.csv) |
| C23 | [reports/distribution-challenger/criteria.csv](../../../reports/distribution-challenger/criteria.csv) |
| D23 | [reports/distribution-challenger/diagnostics.csv](../../../reports/distribution-challenger/diagnostics.csv) |
| DEC23 | [reports/distribution-challenger/decisions.json](../../../reports/distribution-challenger/decisions.json) |
| P23 | [reports/distribution-challenger/protocol.json](../../../reports/distribution-challenger/protocol.json) |
| SEL23 | [reports/distribution-challenger/selection.json](../../../reports/distribution-challenger/selection.json) |
| CT23 | [reports/distribution-challenger/controls.json](../../../reports/distribution-challenger/controls.json) |
| PAR23 | [reports/distribution-challenger/parity.json](../../../reports/distribution-challenger/parity.json) |
| REP23 | [reports/distribution-challenger/reproduction.json](../../../reports/distribution-challenger/reproduction.json) |
| DG23 | [reports/distribution-challenger/diagnostics.json](../../../reports/distribution-challenger/diagnostics.json) |
| DC23 | [reports/distribution-challenger/daily-cycle.json](../../../reports/distribution-challenger/daily-cycle.json) |
| FC23 | [reports/distribution-challenger/fit-cost.json](../../../reports/distribution-challenger/fit-cost.json) |
| LIC23 | [reports/distribution-challenger/licence-admission.md](../../../reports/distribution-challenger/licence-admission.md) |
| REF23 | [reports/distribution-challenger/reference-checks.json](../../../reports/distribution-challenger/reference-checks.json) |
| RA23 | [reports/distribution-challenger/resource-admission.md](../../../reports/distribution-challenger/resource-admission.md) |
| RP23 | [reports/distribution-challenger/replicates.parquet](../../../reports/distribution-challenger/replicates.parquet) |
| DR23 | [reports/distribution-challenger/draft-registry.json](../../../reports/distribution-challenger/draft-registry.json) |
| X23 | [reports/distribution-challenger/mlflow-export-draft/cp23.json](../../../reports/distribution-challenger/mlflow-export-draft/cp23.json) |
| I23 | [docs/track-b/evidence/cp-23/integration.md](../evidence/cp-23/integration.md) |
| RET23 | [docs/track-b/evidence/cp-23/checkpoint-return.md](../evidence/cp-23/checkpoint-return.md) |
| CAP | capstone_v21.md (v21-r10), §21 |

## Claim map: CP-23

Status codes: **S** supported by a saved value or verdict; **S-d** supported, descriptive only; **Def** a
definition; **O** an Owner decision.

| ID | Claim | Source → table/row | Status |
|---|---|---|---|
| C300 | CP-23's Integration verdict and the reviewed final candidate are recorded in I23 and the CP-23 checkpoint return; the evidence tag and landing record are pending at landing. | I23; RET23 | S (pending) |
| C301 | The rule `cp23-adoption` was set on 2026-10-04 (the Owner's ratification of v21-r10) and frozen, verbatim, in the pre-run protocol before any main-run fit or score. | P23 `rule_verbatim`; CAP §21.6 | S |
| C302 | No product change, promotion, freeze, Live, final-product designation or economic claim follows; v1 is the released product and the demo. | CAP §21.6 (what adoption means); DEC23 `statuses` | S |
| C303 | The same 10,747 eligible hours in five folds (2,160 / 2,159 / 2,112 / 2,160 / 2,156), 448 represented days; fold 3 (the stress period) has 2,112 hours on 88 days; the peak 2022-08-15..31 has 408 hours. | M23 L3–L7 (`n_hours`); D23 peak rows | S |
| C304 | DDNN is a feed-forward network (ELU) with a Johnson SU distributional head, written in NumPy and the Python standard library only. It has exactly v4's information on the normalized price target, one row per delivery hour; four configurations (C1 [32], C2 [32, 32], C3 [64, 64], C4 [128, 128]), one chosen per fold before its first origin on training data only; early stopping on the window's last 28 days; four seeds combined by averaging quantiles; the median is both the p50 and the central forecast. | CAP §21.2; P23 `ddnn` | Def |
| C305 | The entry gates passed in order: 4.6L permits research use and retention (hosted service and product unresolved, carried to 4.7); the import audit, the finite-difference gradient checks and the PyTorch reference (26 of 26 checks, torch 2.14.1, at tolerances frozen before the first run) passed; 4.6R on training data only: **PASS** (projected 15.2 of 60 machine-hours; 2,624 of 4,000 main fits). | LIC23; REF23; RA23; CAP §21.3–§21.4 | S |
| C306 | v5 = (2/3)·v4 + (1/3)·DDNN, and v3 plus a DDNN member = (2/3)·v3 + (1/3)·DDNN, each with v3's hour-aware interval layer re-estimated on its own errors; DDNN alone uses its own Johnson SU quantiles. The member weight is fixed at 1/3, as LightGBM's was in v4. | CAP §21.2; P23 `policies`; CT23 `composite_parity_max_abs_eur_mwh` (1.4e-13 EUR/MWh) | Def/S |
| C307 | Configuration chosen per fold, before its first origin: fold 1 C2; fold 2 C4; fold 3 C2; fold 4 C3; fold 5 C4. | SEL23 | S |
| C308 | v5 − v4 (three-block): ΔS_MAE 0.0064 [−0.0016, 0.0149] (+1.2% [−0.3%, +2.7%] of v4's score); ΔS_WIS 0.0071 [−0.0009, 0.0138] (+1.4% [−0.2%, +2.7%]). | U23 L72, L73 | S |
| C309 | Rule `cp23-adoption` for v5: first unmet condition 1 (condition 1 not met; condition 2 met; condition 3 met; condition 4 not met; condition 3's Engineering PASS is the fresh Integration verdict). Folds decisively worse in MAE or WIS (lower endpoint above zero): 1 (fold 3: MAE). | DEC23 `adoption`; C23; U23 per-fold rows | S |
| C310 | The mechanical result of `cp23-adoption`: **v5 is not adopted: CP-23 becomes the branch "DDNN member on v4"**. | DEC23 `adoption.verdict` | S |
| C311 | v5 against v3 (reference): ΔS_MAE −0.0237 [−0.0354, −0.0105] (−4.2% [−6.1%, −1.8%]), ΔS_WIS −0.0196 [−0.0307, −0.0093] (−3.7% [−5.6%, −1.7%]): **observed joint improvement**; the point-error score (S_MAE) difference's 95% interval lies wholly below zero (better) and the interval score (S_WIS) difference's 95% interval lies wholly below zero (better). | U23 L74, L75; DEC23 `contrasts` | S |
| C312 | DDNN alone against v4, descriptive: ΔS_MAE 0.0962 [0.0635, 0.1235] (+18.0% [+11.5%, +22.9%]), ΔS_WIS 0.0651 [0.0299, 0.0898] (+12.9% [+5.9%, +17.7%]): **observed joint worsening**; the point-error score (S_MAE) difference's 95% interval lies wholly above zero (worse) and the interval score (S_WIS) difference's 95% interval lies wholly above zero (worse). | U23 L76, L77; DEC23 `contrasts` | S-d |
| C313 | DDNN alone against v3, descriptive: ΔS_MAE 0.0661 [0.0315, 0.0949] (+11.7% [+5.4%, +16.6%]), ΔS_WIS 0.0384 [0.0025, 0.0645] (+7.2% [+0.5%, +12.0%]): **observed joint worsening**; the point-error score (S_MAE) difference's 95% interval lies wholly above zero (worse) and the interval score (S_WIS) difference's 95% interval lies wholly above zero (worse). | U23 L78, L79; DEC23 `contrasts` | S-d |
| C314 | DDNN as v3's third member ((v3 plus a DDNN member) − v3): ΔS_MAE −0.0144 [−0.0235, −0.0052] (−2.5% [−4.1%, −0.9%]), ΔS_WIS −0.0111 [−0.0200, −0.0038] (−2.1% [−3.7%, −0.7%]): **observed joint improvement**; the point-error score (S_MAE) difference's 95% interval lies wholly below zero (better) and the interval score (S_WIS) difference's 95% interval lies wholly below zero (better). | U23 L80, L81; DEC23 `contrasts` | S-d |
| C315 | Beside it, LightGBM as v3's third member (v4 − v3, CP-21's contrast recomputed on the same index set): ΔS_MAE −0.0301 [−0.0368, −0.0228] (−5.3% [−6.4%, −4.0%]), ΔS_WIS −0.0266 [−0.0327, −0.0204] (−5.0% [−6.0%, −3.8%]): **observed joint improvement**; the point-error score (S_MAE) difference's 95% interval lies wholly below zero (better) and the interval score (S_WIS) difference's 95% interval lies wholly below zero (better). | U23 L82, L83; DEC23 `contrasts` | S-d |
| C316 | Whether LightGBM still adds once DDNN is present (v5 − (v3 plus a DDNN member)): ΔS_MAE −0.0093 [−0.0136, −0.0035] (−1.7% [−2.5%, −0.6%]), ΔS_WIS −0.0085 [−0.0122, −0.0040] (−1.6% [−2.3%, −0.8%]): **observed joint improvement**; the point-error score (S_MAE) difference's 95% interval lies wholly below zero (better) and the interval score (S_WIS) difference's 95% interval lies wholly below zero (better). | U23 L84, L85; DEC23 `contrasts` | S-d |
| C317 | Equal-fold S_MAE/S_WIS: v5 0.5421/0.5127, v4 0.5357/0.5056, v3+D 0.5514/0.5211, v3 0.5658/0.5322, D 0.6319/0.5706. | M23 equal-fold rows | S |
| C318 | Original §8 screen (diagnostic): D not_met, v3 met, v4 met, v3+D met, v5 met. | C23 | S |
| C319 | v5 per-fold MAE: ordinary folds 5.0–15.2 EUR/MWh; stress fold 3 48.9 EUR/MWh (v4 three-block: 47.0; v3: 48.0). | M23 L45–L49, L41, L35 | S |
| C320 | Peak (descriptive, 17 days, small effective sample): v5 MAE 49.9, WIS 27.8 EUR/MWh, 95% coverage 0.939; v4 three-block MAE 50.1, WIS 28.0, coverage 0.936. No inference is drawn. | D23 L1148, L1004 | S-d |
| C321 | DDNN alone, calibration (pooled): 50/80/95% coverage 0.441 / 0.743 / 0.925; share of actuals below its 2.5% and above its 97.5% quantile 0.040 and 0.034; PIT shares below 0.05 and above 0.95 0.072 and 0.070 (0.05 each if calibrated). | DG23 `calibration`; diagnostics/calibration-by-level.csv, pit-histogram.csv | S-d |
| C322 | Extrapolation: on 26 extreme or top-5% days, hours forecast above the origin's training-window maximum: DDNN alone 0, v3 1, v4 0, v3+D 0, v5 0. | DG23 `extrapolation`; diagnostics/extrapolation.csv | S-d |
| C323 | Ensemble and seeds: the ensemble median's MAE 21.20 EUR/MWh against the single seeds' 22.12, 21.78, 22.91, 22.32; member medians spread 6.90 EUR/MWh around the ensemble median. | DG23 `seed_stability_pooled` | S-d |
| C324 | Fit cost and the daily cycle (diagnostic only): 2,624 main-run member fits, median four-seed ensemble 6.5 s per origin; v5's cold daily cycle (DDNN, ensemble, interval layer, issuance) median 12 s, maximum 39 s at 25 origins, beside v4's own component cycle measured by CP-21 (median 25 s). | FC23; DC23 | S |
| C325 | v3 and v4 through CP-23's interval-layer path reproduce their committed vectors bit for bit on all 10,747 keys; an independent representative v3 and v4 slice, refitted, matches bit for bit; every reused vector matches its committed blob. | PAR23; REP23; P23 `cache_identities.verification` | S |
| C326 | All §21.7, §17.7 and applicable §20.7 controls passed (61 checks), each negative paired with a positive control: delivery-day masking and future weather exactly 0.0; a non-uniform D−1 mutation and non-monotone weather perturbations move DDNN; early stopping responds to inner-validation outcomes and the configuration choice ignores evaluation outcomes; a fresh process refits the main run's members bit for bit; composite parity on every key; restart replay and cache refusals. | CT23 | S |
| C327 | Development evidence after selection on the same five folds CP-15, CP-20, CP-21 and CP-22 used; not a test on new data; 4.7T carries the protection. | CAP §21.1 | S |
| C328 | The decision, dated at landing: v5 is not adopted; CP-23 becomes the branch "DDNN member on v4", and the Owner decides whether the branch is published. | DEC23; DR23; landing record (pending) | O (pending) |

## Withheld claims: do not use

W1–W34 in the earlier maps stay in force. CP-23 adds:

| ID | Withheld claim | Reason / controlling source |
|---|---|---|
| W35 | Saying that DDNN, or neural networks, "do not work", "cannot help" or are worse than LightGBM in general | One design was tested against one rule (C304, C310); no demonstrated joint preference is not a proof of absence. |
| W36 | Calling v5 and v4 equivalent, or v5 "as good as" v4 | A mixed or spanning result is no demonstrated joint preference, never equivalence (CAP §21.6). |
| W37 | Attributing any forecast, quantile or metric to PyTorch, or presenting PyTorch as part of the model | PyTorch is a host-side, test-only correctness reference (CAP §18.3, §21.3). |
| W38 | Stating or implying that v5 or DDNN runs in the demo, is the product, is live, or retrains in the browser | v1 is the released product and demo (C302); browser runtime and equality between runtimes are unmeasured (CAP §18.2 item 4). |
| W39 | Describing DDNN's coverage or its PIT histogram as calibrated or guaranteed | Descriptive diagnostics only (C321). |
| W40 | Presenting the fit-cost or daily-cycle figures as qualification for daily operation | A diagnostic only (§17.5 D3); v4's components were not refitted in CP-23 (C324). |
| W41 | Quoting any CP-23 number without its evidence class, or as a confirmatory or significance result | Development after selection; exploratory intervals. |

## Gaps: documented, not resolved

| ID | Gap | Why it stays open |
|---|---|---|
| G26 | Learned or per-block member weights, other DDNN designs, new information | Excluded: 4.8 and stage 7 (CAP §21.2, §22). |
| G27 | Hosted-service and product uses of DDNN | Unresolved in 4.6L; carried to 4.7 and 4.10 (LIC23). |
| G28 | DDNN in another runtime (browser) and its equality with the evaluated code | Unmeasured (CAP §18.2 item 4). |
| G29 | Status dates, the evidence tag and the landing record | They exist only at landing (pending fields). |

