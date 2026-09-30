# CP-21 research result: claim-to-evidence map

**2026-09-29 · Draft for the publication block (PUBLISH_RULES 1.1 §11; capstone v21-r6 §17.9).** Each claim
the publication may render is mapped to a committed file and row. The format follows the
[CP-15/CP-16](cp15-cp16-claims.md) and [CP-20](cp20-claims.md) maps: `L<n>` is the physical line in the
file, and for a CSV `L1` is the header. Values here are rounded from the saved values; the rendered
surfaces bind to evidence records, never to these digits. This map is not yet one of the claim maps
the page reads: the publication block registers it after the Owner's landing.

**Default evidence class.** Every CP-21 result is **`development_post_selection`** and exploratory.

## Source keys

| Key | File |
|---|---|
| R21 | [reports/block-challenger/report.md](../../../reports/block-challenger/report.md) |
| M21 | [reports/block-challenger/metrics.csv](../../../reports/block-challenger/metrics.csv) |
| U21 | [reports/block-challenger/uncertainty.csv](../../../reports/block-challenger/uncertainty.csv) |
| C21 | [reports/block-challenger/criteria.csv](../../../reports/block-challenger/criteria.csv) |
| D21 | [reports/block-challenger/diagnostics.csv](../../../reports/block-challenger/diagnostics.csv) |
| A21 | [reports/block-challenger/adoption.json](../../../reports/block-challenger/adoption.json) |
| P21 | [reports/block-challenger/protocol.json](../../../reports/block-challenger/protocol.json) |
| CT21 | [reports/block-challenger/controls.json](../../../reports/block-challenger/controls.json) |
| HP21 | [reports/block-challenger/hg-parity.json](../../../reports/block-challenger/hg-parity.json) |
| DC21 | [reports/block-challenger/daily-cycle.json](../../../reports/block-challenger/daily-cycle.json) |
| FC21 | [reports/block-challenger/fit-cost.json](../../../reports/block-challenger/fit-cost.json) |
| RP21 | [reports/block-challenger/replicates.parquet](../../../reports/block-challenger/replicates.parquet) |
| DR21 | [reports/block-challenger/draft-registry.json](../../../reports/block-challenger/draft-registry.json) |
| X21 | [reports/block-challenger/mlflow-export-draft/cp21.json](../../../reports/block-challenger/mlflow-export-draft/cp21.json) |
| I21 | [docs/track-b/evidence/cp-21/integration.md](../evidence/cp-21/integration.md) |
| RET21 | [docs/track-b/evidence/cp-21/checkpoint-return.md](../evidence/cp-21/checkpoint-return.md) |
| CAP | capstone_v21.md (v21-r6), §17 |

## Claim map: CP-21

Status codes, as in the earlier maps: **S** supported by a saved value or verdict; **S-d** supported,
descriptive only; **I** an inference from design plus saved values; **Def** a definition; **O** an Owner
decision.

| ID | Claim | Source → table/row | Status |
|---|---|---|---|
| C100 | CP-21 Integration verdict and the reviewed final candidate are recorded in I21 and the CP-21 checkpoint return; the evidence tag and landing record are pending at landing. | I21; RET21 | S (pending) |
| C101 | Rule `cp21-adoption` was set on 2026-09-29 (the Owner's ratification) and frozen, verbatim, in the pre-run protocol before any fit or score. | P21 `adoption_rule_verbatim`; CAP §17.6 | S |
| C102 | No product change, promotion, freeze, Live, final-product designation or economic claim follows; v1 remains the released product and demo. | CAP §17.1, §17.6; A21 `status` | S |
| C103 | The same 10,747 eligible hours in five folds (2,160 / 2,159 / 2,112 / 2,160 / 2,156), 448 represented days; fold 3 (the stress period) has 2,112 hours on 88 days; the peak 2022-08-15..31 has 408 hours. | M21 L3–L7 (`n_hours`); M21 L5; D21 peak rows | S |
| C104 | HGL's central forecast is `A1_w/3 + B2_w/3 + L-N/6 + L-R/6`: v3's two LEAR components (bit for bit) with weight 2/3 in total and the mean of the raw and normalized three-block LightGBM forecasts with weight 1/3; v3's hour-aware interval layer is re-estimated on HGL's own errors. The weights were fixed before any result and never tuned. | CAP §17.2; P21 `blend`, `h_layer`; CT21 `hgl_blend_parity_max_abs_eur_mwh` | Def/S |
| C105 | Every LightGBM arm has exactly v3's information: CP-15's 23 LightGBM features plus the three frozen GFS columns and their missing indicators; blocks night 22–05, solar 10–16, shoulder/peak 06–09 and 17–21 (Europe/Berlin); four capacity configurations (150/15, 300/31, 600/31, 600/63 trees/leaves) selected at every origin on the window's last 28 days by MAE in EUR/MWh, ties to the smaller, then refitted. | CAP §17.3; P21 `features`, `capacity_grid`, `selection` | Def |
| C106 | The ladder B3 → pooled LightGBM → three-block LightGBM → HGL adds, in turn, weather (bundled with training-only capacity selection and the missing-input rule, so it is not an isolated weather effect), the block split (controlled: same rows, target, features, grid, selection rule and interval recipe), and the blend into v3. | CAP §17.1; CT21 `pooled_block_rows_equal` | Def |
| C107 | ΔS_MAE (HGL − v3) = −0.0301, 95% interval [−0.0368, −0.0228]; as a share of v3's score −5% [−6%, −4%]. | U21 L72 | S |
| C108 | ΔS_WIS (HGL − v3) = −0.0266, 95% interval [−0.0327, −0.0204]; as a share of v3's score −5% [−6%, −4%]. | U21 L73 | S |
| C109 | The mechanical verdict of rule `cp21-adoption`: **v4** (condition 1 met; condition 2 met; condition 3 met; condition 4 met; condition 3's Engineering PASS is the fresh Integration verdict). | A21 `verdict`, `conditions`; C21 HGL rows; U21 HGL rows | S |
| C110 | Per fold (EUR/MWh, paired mean daily loss difference, HGL − v3): fold_1 MAE −0.32 [−0.49, −0.18], WIS −0.19 [−0.28, −0.10]; fold_2 MAE −0.67 [−1.03, −0.36], WIS −0.35 [−0.53, −0.19]; fold_3 MAE −1.01 [−2.56, 0.59], WIS −0.78 [−1.70, 0.09]; fold_4 MAE −0.86 [−1.11, −0.63], WIS −0.47 [−0.63, −0.32]; fold_5 MAE −0.69 [−0.97, −0.22], WIS −0.37 [−0.50, −0.14]. Folds decisively worse (lower endpoint above zero): 0. | U21 L2, L3, L16, L17, L30, L31, L44, L45, L58, L59 | S-d |
| C111 | Block split (three-block minus pooled LightGBM): ΔS_MAE 0.0050 [−0.0084, 0.0142], ΔS_WIS 0.0063 [−0.0050, 0.0135]: **no demonstrated joint preference** under §17.5's endpoint reading (a development finding, not an adoption criterion). | U21 L74, L75; A21 `block_split` | S |
| C112 | weather bundled with capacity selection: ΔS_MAE −0.2056 [−0.2377, −0.1766], ΔS_WIS −0.1922 [−0.2278, −0.1659]: observed joint improvement; the point-error score (S_MAE) difference's 95% interval lies wholly below zero (better) and the interval score (S_WIS) difference's 95% interval lies wholly below zero (better) (descriptive). | U21 L76, L77 | S-d |
| C113 | target representation: ΔS_MAE −0.0066 [−0.0304, 0.0144], ΔS_WIS −0.0138 [−0.0348, 0.0065]: no demonstrated joint preference; both single-metric intervals span zero (descriptive). | U21 L78, L79 | S-d |
| C114 | pooled LightGBM against v3: ΔS_MAE 0.0127 [−0.0088, 0.0427], ΔS_WIS 0.0155 [−0.0039, 0.0412]: no demonstrated joint preference; both single-metric intervals span zero (descriptive). | U21 L80, L81 | S-d |
| C115 | three-block LightGBM against v3: ΔS_MAE 0.0177 [−0.0065, 0.0458], ΔS_WIS 0.0218 [0.0004, 0.0450]: no demonstrated joint preference; the interval score (S_WIS) difference's 95% interval lies wholly above zero (worse) (descriptive). | U21 L82, L83 | S-d |
| C116 | normalized three-block LightGBM against v3: ΔS_MAE 0.0112 [−0.0080, 0.0324], ΔS_WIS 0.0080 [−0.0086, 0.0270]: no demonstrated joint preference; both single-metric intervals span zero (descriptive). | U21 L84, L85 | S-d |
| C117 | Equal-fold S_MAE/S_WIS: HGL 0.5357/0.5056, HG 0.5658/0.5322, L-P 0.5785/0.5477, L-R 0.5835/0.5540, L-N 0.5769/0.5402, B3 0.7841/0.7399; all eleven policies in M21. | M21 L75–L78, L74, L71 | S |
| C118 | HGL per-fold MAE: ordinary folds 4.9–15.0 EUR/MWh; stress fold 3 47.0 EUR/MWh (v3: 48.0). | M21 L45–L49, L41 | S |
| C119 | Original §8 screen (diagnostic): HG met, HGL met, L-N met, L-P not_met, L-R not_met. | C21; A21 `conditions.2` | S |
| C120 | Peak (descriptive, 17 days, small effective sample): HGL MAE 50.1 and WIS 28.0 EUR/MWh, 95% coverage 0.936 (382/408 hours); v3 MAE 47.5 and WIS 27.3, coverage 0.939. On the peak, HGL's point error is higher than v3's; no inference is drawn. | D21 L1141, L998 | S-d |
| C121 | Coverage is reported with mean, median and 95th-percentile width and tail misses, per fold, hour and block, with the 56-date support rule for block and hour statements; no hour or block effect is claimed. | M21 per-fold rows; D21 `hour`, `block` rows | S-d |
| C122 | v3 through CP-21's interval-layer path reproduces the accepted CP-20 vectors bit for bit on all 10,747 keys; the cached v3 components match their CP-20 fingerprints; the frozen weather regenerates bit for bit from the 2,476 retained grids. | HP21; P21 `cache_identities`, `weather.regenerated_from_grids` | S |
| C123 | All §17.7 controls passed (49 checks): delivery-day masking exactly 0.0; a non-uniform D−1 price mutation moves every arm; future weather exactly 0.0; cross-date permutation and within-day rearrangement of weather move every LightGBM arm (non-monotone, so not absorbed by the trees); training-only selection; pooled–block row parity; DST blocks; state and cache refusals; the 2026-04-07 guard. | CT21 `all_passed`, `origins`, `state`, `population` | S |
| C124 | Main-run LightGBM fits: 22,260; block against pooled wall time 1.75×; HGL's cold daily cycle on the M3 with four workers: median 25 s, maximum 69 s at 25 origins (diagnostic only, not a selection criterion). | FC21; DC21 | S |
| C125 | Development evidence after selection on the same five folds; not a test on new data; the fresh-data test 4.7T stays reserved. | CAP §17.1 | S |
| C126 | No contrast isolates individual weather features, and the block split is tested on the raw target only, with one seed. | CAP §17.2 (out of scope) | Def |
| C127 | The decision, dated at landing: HGL becomes **v4 · three-block LightGBM added**, with predecessor v3. | A21; DR21; landing record (pending) | O (pending) |

## Withheld claims: do not use

W1–W21 in the [CP-15/CP-16](cp15-cp16-claims.md#withheld-claims-do-not-use) and [CP-20](cp20-claims.md) maps stay in
force. CP-21 adds:

| ID | Withheld claim | Reason / controlling source |
|---|---|---|
| W22 | Calling the block split beneficial or harmful beyond its §17.5 reading, or naming a mechanism for it | The finding is exactly C111's reading; no mechanism was tested. |
| W23 | Attributing the change from daily LightGBM to the pooled arm to weather alone | That step also changes capacity selection and the missing-input rule (C106). |
| W24 | Stating or implying that HGL, a CP-21 arm or v4 runs in the demo, is the product, or is live | v1 remains the released product and demo (C102). |
| W25 | Calling a mixed or non-significant contrast "equivalent", "no effect", "no benefit" or "no harm" | Not established by the rule (CAP §14.4, §17.6). |
| W26 | Presenting the daily-cycle or fit-cost figures as qualification for daily operation | A diagnostic only (Owner decision D3); §16 governs a final product (C124). |
| W27 | Quoting any CP-21 number without its evidence class, or as a confirmatory or significance result | Development after selection; exploratory intervals (C125). |

## Gaps: documented, not resolved

| ID | Gap | Why it stays open |
|---|---|---|
| G21 | No normalized pooled arm, residual-correction model or learned blend weights | Out of scope by design (CAP §17.2); programme 4.8 owns learned weights. |
| G22 | Adoption and status dates, the evidence tag and the landing record | They exist only at landing; the publication block fills them (pending fields). |

