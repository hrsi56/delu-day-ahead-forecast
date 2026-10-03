# CP-22 research result: claim-to-evidence map

**2026-10-03 · Draft for PRES-4 (PUBLISH_RULES 1.3 §11; capstone v21-r9 §20.9).** Each claim the publication may
render is mapped to a committed file and row, in the format of the [CP-21](cp21-claims.md) map: `L<n>` is the
physical line in the file, and for a CSV `L1` is the header. Values here are rounded from the saved values; the
rendered surfaces bind to evidence records, never to these digits. The publication block registers this map
after the Owner's landing, and only after the Owner's decision (no replacement).

**Default evidence class.** Every CP-22 result is **`development_post_selection`** and exploratory.

## Source keys

| Key | File |
|---|---|
| R22 | [reports/v4-revision/report.md](../../../reports/v4-revision/report.md) |
| M22 | [reports/v4-revision/metrics.csv](../../../reports/v4-revision/metrics.csv) |
| U22 | [reports/v4-revision/uncertainty.csv](../../../reports/v4-revision/uncertainty.csv) |
| C22 | [reports/v4-revision/criteria.csv](../../../reports/v4-revision/criteria.csv) |
| D22 | [reports/v4-revision/diagnostics.csv](../../../reports/v4-revision/diagnostics.csv) |
| DEC22 | [reports/v4-revision/decisions.json](../../../reports/v4-revision/decisions.json) |
| P22 | [reports/v4-revision/protocol.json](../../../reports/v4-revision/protocol.json) |
| CT22 | [reports/v4-revision/controls.json](../../../reports/v4-revision/controls.json) |
| PAR22 | [reports/v4-revision/parity.json](../../../reports/v4-revision/parity.json) |
| REP22 | [reports/v4-revision/reproduction.json](../../../reports/v4-revision/reproduction.json) |
| INV22 | [reports/v4-revision/investigation.json](../../../reports/v4-revision/investigation.json) |
| DC22 | [reports/v4-revision/daily-cycle.json](../../../reports/v4-revision/daily-cycle.json) |
| FC22 | [reports/v4-revision/fit-cost.json](../../../reports/v4-revision/fit-cost.json) |
| RP22 | [reports/v4-revision/replicates.parquet](../../../reports/v4-revision/replicates.parquet) |
| DR22 | [reports/v4-revision/draft-registry.json](../../../reports/v4-revision/draft-registry.json) |
| X22 | [reports/v4-revision/mlflow-export-draft/cp22.json](../../../reports/v4-revision/mlflow-export-draft/cp22.json) |
| I22 | [docs/track-b/evidence/cp-22/integration.md](../evidence/cp-22/integration.md) |
| RET22 | [docs/track-b/evidence/cp-22/checkpoint-return.md](../evidence/cp-22/checkpoint-return.md) |
| CAP | capstone_v21.md (v21-r9), §20 |

## Claim map: CP-22

Status codes: **S** supported by a saved value or verdict; **S-d** supported, descriptive only; **Def** a
definition; **O** an Owner decision.

| ID | Claim | Source → table/row | Status |
|---|---|---|---|
| C200 | CP-22's Integration verdict and the reviewed final candidate are recorded in I22 and the CP-22 checkpoint return; the evidence tag and landing record are pending at landing. | I22; RET22 | S (pending) |
| C201 | The three rules `cp22-replacement`, `cp22-dynamic-layer` and `cp22-fast-component` were set on 2026-10-01 (the Owner's ratification) and frozen, verbatim, in the pre-run protocol before any main fit or score. | P22 `rules_verbatim`; CAP §20.6 | S |
| C202 | No product change, promotion, freeze, Live, final-product designation or economic claim follows; v1 remains the released product and the demo. | CAP §20.6 (what replacement means); DEC22 `statuses` | S |
| C203 | The same 10,747 eligible hours in five folds (2,160 / 2,159 / 2,112 / 2,160 / 2,156), 448 represented days; fold 3 (the stress period) has 2,112 hours on 88 days; the peak 2022-08-15..31 has 408 hours. | M22 L3–L7 (`n_hours`); D22 peak rows | S |
| C204 | PN is one pooled LightGBM for all 24 hours on the normalized price target, with exactly v3's and v4's information; its capacity-averaged form is the equal mean of four full-window fits (150/15, 300/31, 600/31 and 600/63 trees/leaves), and its selected form chooses one of them daily on the window's last 28 days. | CAP §20.2; P22 `members`, `capacity_grid`, `selection` | Def |
| C205 | Every composite is `(2/3)·c_v3 + (1/3)·member` with the member weight fixed at 1/3: R's member is PN averaged over capacities; M's is the mean of PN (selected) and the pooled raw LightGBM; v4's three-block construction's is the mean of the normalized and raw three-block LightGBM. Every non-dynamic composite uses v3's hour-aware interval layer on its own errors. | CAP §20.2; P22 `policies`; CT22 `composite_parity_max_abs_eur_mwh`, `non_dl_composites_on_h_path` | Def/S |
| C206 | The ladder, one change per step: v4 → M removes the block split (same raw/normalized mix and daily selection); M → the selected normalized member drops the raw half; that → R averages over capacities instead of selecting daily. | CAP §20.1 (the ladder); tests/cp22/test_pn_and_composites.py; CT22 `ladder_rows` | Def |
| C207 | The dynamic interval layer keeps v3's layer and changes two things, fixed before scoring: 7-day recency weights inside the 28-day buffer (weighted quantiles, effective counts, weighted median) and adaptive coverage (γ = 0.10 per day, α_t clipped to [α/5, min(2α, 0.9)], sorting if quantiles cross). The fast component adds a one-day kernel carrying one third of the weight. | CAP §20.3; P22 `interval_layers` | Def |
| C208 | R − v4 (three-block): ΔS_MAE 0.0011 [−0.0031, 0.0054] (+0.2% [−0.6%, +1.0%] of v4's score); ΔS_WIS 0.0010 [−0.0028, 0.0049] (+0.2% [−0.5%, +1.0%]). | U22 L162, L163 | S |
| C209 | Rule `cp22-replacement` for R: first unmet condition 4 (condition 1 met; condition 2 met; condition 3 met; condition 4 not met; condition 3's Engineering PASS is the fresh Integration verdict). Folds decisively worse in MAE or WIS (lower endpoint above zero): 1 (fold 4: MAE and WIS). | DEC22 `replacement.candidates.R`; C22; U22 per-fold rows | S |
| C210 | M − v4 (three-block): ΔS_MAE −0.0013 [−0.0036, 0.0016] (−0.2% [−0.7%, +0.3%] of v4's score); ΔS_WIS −0.0008 [−0.0030, 0.0022] (−0.2% [−0.6%, +0.4%]). | U22 L164, L165 | S |
| C211 | Rule `cp22-replacement` for M: first unmet condition 4 (condition 1 met; condition 2 met; condition 3 met; condition 4 not met; condition 3's Engineering PASS is the fresh Integration verdict). Folds decisively worse in MAE or WIS (lower endpoint above zero): 1 (fold 4: MAE and WIS). | DEC22 `replacement.candidates.M`; C22; U22 per-fold rows | S |
| C212 | The mechanical result of `cp22-replacement`: **no replacement: CP-22 stops at its return and the Owner decides; three-block v4 stays current**. | DEC22 `replacement.verdict` | S |
| C213 | Whether the replacement shows a joint improvement over v4 under §17.5's reading: not applicable (no replacement); R − v4 reads no demonstrated joint preference and M − v4 reads no demonstrated joint preference. | DEC22 `contrasts` | S |
| C214 | Rule `cp22-dynamic-layer`: not applicable — no winner W. | DEC22 `dynamic_layer` | S |
| C215 | Rule `cp22-fast-component`: not applicable: no winner W. | DEC22 `fast_component` | S |
| C216 | The full refinement against the minimal one (R − M): ΔS_MAE 0.0025 [−0.0016, 0.0058] (+0.5% [−0.3%, +1.1%]), ΔS_WIS 0.0018 [−0.0018, 0.0049] (+0.3% [−0.3%, +1.0%]): **no demonstrated joint preference**; both single-metric intervals span zero. | U22 L166, L167; DEC22 `contrasts` | S-d |
| C217 | Dropping the raw half (selected normalized pooled member − M): ΔS_MAE 0.0015 [−0.0025, 0.0048] (+0.3% [−0.5%, +0.9%]), ΔS_WIS 0.0005 [−0.0030, 0.0040] (+0.1% [−0.6%, +0.8%]): **no demonstrated joint preference**; both single-metric intervals span zero. | U22 L168, L169; DEC22 `contrasts` | S-d |
| C218 | Averaging against daily selection (R − selected normalized member): ΔS_MAE 0.0010 [−0.0009, 0.0025] (+0.2% [−0.2%, +0.5%]), ΔS_WIS 0.0012 [−0.0006, 0.0026] (+0.2% [−0.1%, +0.5%]): **no demonstrated joint preference**; both single-metric intervals span zero. | U22 L170, L171; DEC22 `contrasts` | S-d |
| C219 | Normalized against raw, pooled: ΔS_MAE −0.0023 [−0.0102, 0.0041] (−0.4% [−1.8%, +0.8%]), ΔS_WIS −0.0030 [−0.0099, 0.0035] (−0.6% [−1.9%, +0.7%]): **no demonstrated joint preference**; both single-metric intervals span zero. | U22 L172, L173; DEC22 `contrasts` | S-d |
| C220 | Descriptive: the blocks under normalization (normalized-block member − v4): ΔS_MAE 0.0006 [−0.0035, 0.0043] (+0.1% [−0.6%, +0.8%]), ΔS_WIS 0.0001 [−0.0035, 0.0038] (+0.0% [−0.7%, +0.7%]): **no demonstrated joint preference**; both single-metric intervals span zero. | U22 L174, L175; DEC22 `contrasts` | S-d |
| C221 | The dynamic layer on v4, descriptive: ΔS_MAE 0.0022 [−0.0041, 0.0077] (+0.4% [−0.7%, +1.4%]), ΔS_WIS 0.0225 [0.0161, 0.0308] (+4.5% [+3.1%, +6.1%]): **no demonstrated joint preference**; the interval score (S_WIS) difference's 95% interval lies wholly above zero (worse). | U22 L176, L177; DEC22 `contrasts` | S-d |
| C222 | The dynamic layer on v3, descriptive: ΔS_MAE 0.0018 [−0.0041, 0.0072] (+0.3% [−0.7%, +1.3%]), ΔS_WIS 0.0231 [0.0165, 0.0316] (+4.3% [+3.0%, +5.9%]): **no demonstrated joint preference**; the interval score (S_WIS) difference's 95% interval lies wholly above zero (worse). | U22 L178, L179; DEC22 `contrasts` | S-d |
| C223 | Equal-fold S_MAE/S_WIS: A-LN 0.5362/0.5056, A-LP 0.5381/0.5084, A-PN-sel 0.5358/0.5053, B3 0.7841/0.7399, v3 0.5658/0.5322, v4 0.5357/0.5056, M 0.5343/0.5048, R 0.5368/0.5066, v3+DL 0.5676/0.5553, v4+DL 0.5379/0.5281; every policy against v3 is in U22 (`reference_vs_v3`). | M22 equal-fold rows | S |
| C224 | Original §8 screen (diagnostic): A-LN met, A-LP met, A-PN-sel met, v3 met, v4 met, M met, R met, v3+DL met, v4+DL met. | C22 | S |
| C225 | R per-fold MAE: ordinary folds 5.0–14.9 EUR/MWh; stress fold 3 46.7 EUR/MWh (v4 three-block: 47.0; v3: 48.0). | M22 L51–L55, L47, L41 | S |
| C226 | Peak (descriptive, 17 days, small effective sample): R MAE 47.6, WIS 26.6 EUR/MWh, 95% coverage 0.939; v4 three-block MAE 50.1, WIS 28.0, coverage 0.936. No inference is drawn. | D22 L1292, L1148 | S-d |
| C227 | Decomposition of v4 − v3 along the ladder (equal-fold): v4 → M (the split removed) ΔS_MAE −0.0013, ΔS_WIS −0.0008; M → A-PN-sel (the raw half dropped) ΔS_MAE 0.0015, ΔS_WIS 0.0005; A-PN-sel → R (averaging over capacities instead of daily selection) ΔS_MAE 0.0010, ΔS_WIS 0.0012; v3 → R (v3 to R) ΔS_MAE −0.0290, ΔS_WIS −0.0256; v3 → v4 (v3 to v4 (CP-21)) ΔS_MAE −0.0301, ΔS_WIS −0.0266. The brackets sum to v4 − v3 exactly. | INV22 `ladder` | S-d |
| C228 | The member-weight curve is an oracle computed on outcomes and selects nothing: L-N lowest at 0.5, L-P lowest at 0.45, PN-avg lowest at 0.45, PN-sel lowest at 0.45, mean(PN-sel, L-P) lowest at 0.55, v4 member mean(L-N, L-R) lowest at 0.55 (central forecast, before any interval layer). The fixed weight stays 1/3. | INV22 `member_weight_curve` | S-d |
| C229 | Capacity-selection stability at evaluation origins (flip rate; median relative winner margin): PN pooled 0.54, 1.1%; L-P pooled 0.50, 1.3%; L-R night 0.53, 1.6%; L-R solar 0.48, 1.6%; L-R shoulder 0.52, 1.4%; L-N night 0.46, 1.6%; L-N solar 0.54, 1.4%; L-N shoulder 0.52, 1.2%. | INV22 `capacity_stability` | S-d |
| C230 | Extrapolation: 26 extreme or top-5% days, 8 above the origin's training-window maximum; per-member maxima are in the extrapolation table. | INV22 `extrapolation`; reports/v4-revision/investigation/extrapolation.csv | S-d |
| C231 | Reaction after the peak began (days from 2022-08-15): v4 ACI not applicable (no ACI), width 12; v4+DL ACI 3, width 4; v3 ACI not applicable (no ACI), width 12; v3+DL ACI 3, width 4. | INV22 `reaction_after_peak_start`; investigation/alpha-paths.csv | S-d |
| C232 | Sharp changes (the shock-day set and the three days after, pooled): largest_daily_mean_change/v3 MAE 20.3, WIS 12.0, cov95 0.927; largest_daily_mean_change/v3+DL MAE 21.0, WIS 13.2, cov95 0.954; largest_daily_mean_change/v4 MAE 19.6, WIS 11.5, cov95 0.937; largest_daily_mean_change/v4+DL MAE 20.5, WIS 12.8, cov95 0.956; peak_first_ten_days/v3 MAE 44.2, WIS 24.4, cov95 0.953; peak_first_ten_days/v3+DL MAE 43.3, WIS 24.7, cov95 0.969; peak_first_ten_days/v4 MAE 47.0, WIS 25.3, cov95 0.950; peak_first_ten_days/v4+DL MAE 45.1, WIS 25.5, cov95 0.969. | INV22 `shock_days` | S-d |
| C233 | LEAR's penalty-selection stability, from logged selections (no refit): A1 evaluation flip rate 0.11; A1 warm-up flip rate 0.10; B2 evaluation flip rate 0.10; B2 warm-up flip rate 0.09. | INV22 `lear_penalty_stability` | S-d |
| C234 | Fit cost and the daily cycle (diagnostic only): M cold cycle median 19 s, maximum 48 s at 25 origins; R cold cycle median 18 s, maximum 55 s at 25 origins; PN median per origin 5.0 s for eight fits against L-P's 3.2 s for five. | DC22; FC22 | S |
| C235 | v3 and v4 through CP-22's interval-layer path reproduce their committed vectors bit for bit on all 10,747 keys; an independent representative v3 and v4 slice, refitted, matches bit for bit; every reused vector matches its committed blob. | PAR22; REP22; P22 `cache_identities.verification` | S |
| C236 | All §20.7 and §17.7 controls passed (71 checks), each negative assertion paired with a positive control: delivery-day masking exactly 0.0; non-uniform D−1 mutation moves PN; non-monotone weather perturbations move PN; training-only selection; capacity-averaging and selection identity over all 636 PN fits; composite parity on every key; the dynamic layer's direction, clipping, weight and release controls; with no weights and no adaptive coverage it reproduces R's committed vectors bit for bit. | CT22 | S |
| C237 | Development evidence after selection on the same five folds CP-15, CP-20 and CP-21 used; not a test on new data; 4.7T carries the protection. | CAP §20.1 | S |
| C238 | The decision, dated at landing: no replacement: three-block v4 stays current and the Owner decides (§20.6). | DEC22; DR22; landing record (pending) | O (pending) |

## Withheld claims: do not use

W1–W27 in the earlier maps stay in force. CP-22 adds:

| ID | Withheld claim | Reason / controlling source |
|---|---|---|
| W28 | Calling R, M or v4 "equivalent", or any non-inferior result "no worse" without its interval | Non-inferiority means no 95% interval lies entirely above zero (CAP §20.6); never equivalence. |
| W29 | Presenting the member-weight curve as a better or recommended weight | An oracle on outcomes, not selectable (C228). |
| W30 | Naming a mechanism for the block split, or reopening its removal | The Owner removed the split in every outcome (CAP §20.1). |
| W31 | Stating or implying that a CP-22 policy or v4 runs in the demo, is the product, or is live | v1 remains the released product and demo (C202). |
| W32 | Presenting the daily-cycle or fit-cost figures as qualification for daily operation | A diagnostic only (§17.5 D3). |
| W33 | Quoting any CP-22 number without its evidence class, or as a confirmatory or significance result | Development after selection; exploratory intervals. |
| W34 | Describing the dynamic layer's coverage as a guarantee | An empirical layer with adaptive coverage, not a finite-sample guarantee (CAP §6, §20.3). |

## Gaps: documented, not resolved

| ID | Gap | Why it stays open |
|---|---|---|
| G23 | Learned or per-block member weights, seed ensembles, LEAR changes | Excluded (CAP §20.2; D6, D8). |
| G24 | The registry's revision event and the runbook's lists (A10 maintenance) | PRES-4's work after landing. |
| G25 | Status dates, the evidence tag and the landing record | They exist only at landing (pending fields). |

