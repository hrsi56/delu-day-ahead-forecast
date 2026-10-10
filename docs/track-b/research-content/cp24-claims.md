# CP-24 research result: claim-to-evidence map

**2026-10 · Draft for the next publication (PUBLISH_RULES 1.3 §11; capstone v21-r11 §23.12).** Each claim the
publication may render is mapped to a committed file and row, in the format of the [CP-23](cp23-claims.md) map: `L<n>`
is the physical line in the file, and for a CSV `L1` is the header. Values here are rounded from the saved values; the
rendered surfaces bind to evidence records, never to these digits. Publication follows the Owner's landing and the
Owner's decisions (§23.12).

**Outcome:** adopted. **Default evidence class:** `development_post_selection`, exploratory.

## Source keys

| Key | File |
|---|---|
| R24 | [reports/ddnn2/report.md](../../../reports/ddnn2/report.md) |
| LIC24 | [reports/ddnn2/licence-admission.md](../../../reports/ddnn2/licence-admission.md) |
| REF24 | [reports/ddnn2/reference-checks.json](../../../reports/ddnn2/reference-checks.json) |
| RA24 | [reports/ddnn2/resource-admission.md](../../../reports/ddnn2/resource-admission.md) |
| PAR24 | [reports/ddnn2/v4-parity.json](../../../reports/ddnn2/v4-parity.json) |
| STEER24 | [docs/track-b/evidence/cp-24/steering/](../evidence/cp-24/steering/) |
| DR24 | [reports/ddnn2/draft-registry.json](../../../reports/ddnn2/draft-registry.json) |
| I24 | [docs/track-b/evidence/cp-24/integration.md](../evidence/cp-24/integration.md) |
| RET24 | [docs/track-b/evidence/cp-24/checkpoint-return.md](../evidence/cp-24/checkpoint-return.md) |
| CAP | capstone_v21.md (v21-r11), §23 |
| GATE24-1 | [reports/ddnn2/rounds/round-1/gate.json](../../../reports/ddnn2/rounds/round-1/gate.json) |
| RD24-1 | [reports/ddnn2/rounds/round-1/design.json](../../../reports/ddnn2/rounds/round-1/design.json) |
| M24 | [reports/ddnn2/attempt-1/metrics.csv](../../../reports/ddnn2/attempt-1/metrics.csv) |
| U24 | [reports/ddnn2/attempt-1/uncertainty.csv](../../../reports/ddnn2/attempt-1/uncertainty.csv) |
| C24 | [reports/ddnn2/attempt-1/criteria.csv](../../../reports/ddnn2/attempt-1/criteria.csv) |
| D24 | [reports/ddnn2/attempt-1/diagnostics.csv](../../../reports/ddnn2/attempt-1/diagnostics.csv) |
| DEC24 | [reports/ddnn2/attempt-1/decisions.json](../../../reports/ddnn2/attempt-1/decisions.json) |
| P24 | [reports/ddnn2/attempt-1/protocol.json](../../../reports/ddnn2/attempt-1/protocol.json) |
| CT24 | [reports/ddnn2/attempt-1/controls.json](../../../reports/ddnn2/attempt-1/controls.json) |
| DG24 | [reports/ddnn2/attempt-1/diagnostics.json](../../../reports/ddnn2/attempt-1/diagnostics.json) |
| GU24 | [reports/ddnn2/attempt-1/guards.json](../../../reports/ddnn2/attempt-1/guards.json) |
| DC24 | [reports/ddnn2/attempt-1/daily-cycle.json](../../../reports/ddnn2/attempt-1/daily-cycle.json) |
| FC24 | [reports/ddnn2/attempt-1/fit-cost.json](../../../reports/ddnn2/attempt-1/fit-cost.json) |
| LK24 | [reports/ddnn2/attempt-1/leakage-controls.json](../../../reports/ddnn2/attempt-1/leakage-controls.json) |
| X24 | [reports/ddnn2/mlflow-export-draft/cp24.json](../../../reports/ddnn2/mlflow-export-draft/cp24.json) |

## Claim map: CP-24

Status codes: **S** supported by a saved value or verdict; **S-d** supported, descriptive only; **Def** a
definition; **O** an Owner decision.

| ID | Claim | Source → table/row | Status |
|---|---|---|---|
| C400 | CP-24's Integration verdict and the reviewed final candidate are recorded in I24 and the CP-24 checkpoint return; the evidence tag and landing record are pending at landing. | I24; RET24 | S (pending) |
| C401 | The rule `cp24-adoption` was set on 2026-10-05 (v21-r11, ratified under the Owner's delegation) and frozen, verbatim, in each scored attempt's protocol before any of its warm-up or evaluation fits. | CAP §23.9; P24 `rule_verbatim` | S |
| C402 | No product change, promotion, freeze, Live, final-product designation or economic claim follows; v1 is the released product and the demo. | CAP §23.9 (what adoption means) | S |
| C403 | DDNN-2 is a NumPy-only feed-forward network on one row per delivery day with 24 Johnson SU heads, exactly v4's sources in day-level form; every member trains on [max(2019-01-01, D−728), D) minus its own random 20% of whole calendar weeks (never the last 7 days), early-stopped on the seven-level pinball loss; NLL for 20 epochs, then κ·NLL + (1−κ)·pinball over 19 levels; four tuned configurations × two seeds combined by the per-level median. | CAP §23.3; RD24 `recipe` | Def |
| C404 | Entry: 4.6L′ PASS (provenance; CP-23's reference reused); the import audit, the finite-difference checks and the PyTorch reference (32 of 32 checks, torch 2.14.1, tolerances frozen before the first run) passed; 4.6R′ on pre-fold data: **PASS**, fixing 128 trials per fold per round. | LIC24; REF24; RA24; CAP §23.7 | S |
| C405 | v4's members at the gate days run their unchanged code; their code path, with the weather-coverage wrapper, reproduces the committed A1_w, B2_w, L-N, L-R, v3 and v4 vectors bit for bit at 11 covered origins, and the unwrapped code refuses a fold-4 gate day. | PAR24 | S |
| C411 | Pre-fold round 1: gate **passed** on 280 pre-fold days — G0 met; G1 MAE(v5) 12.538 vs MAE(v4) 12.849 EUR/MWh (met); G2 MAE(DDNN-2)/MAE(L) 0.852 vs 1.10 (met); G3 cap share 0.088% vs 0.1% (met). A screen, not a claim. | GATE24-1 | S-d |
| C419 | Steering: 2 committed exchange file(s) under `docs/track-b/evidence/cp-24/steering/`; 1 pre-fold round(s) and 1 scored attempt(s). | STEER24 | S |
| C420 | Scored attempt 1, v5 − v4: ΔS_MAE −0.0133 [95% −0.0161, −0.0096; 97.5% −0.0166, −0.0091] (−2.5% of v4's score); ΔS_WIS −0.0119 [95% −0.0143, −0.0087; 97.5% −0.0147, −0.0084] (−2.4%). | U24 L112, L113 | S |
| C421 | Rule `cp24-adoption` for v5 in attempt 1: all five conditions met (condition 1 met; condition 2 met; condition 3 met; condition 4 met; condition 5 met; condition 3's Engineering PASS is the fresh Integration verdict). | DEC24 `adoption`; C24; U24 per-fold rows | S |
| C422 | The mechanical result of `cp24-adoption` in attempt 1: **v5 is adopted in research as v5 ("v5 · DDNN-2 member added", predecessor v4)**. | DEC24 `adoption.verdict` | S |
| C424 | v5 against v3 (reference): ΔS_MAE −0.0434 [−0.0491, −0.0366] (−7.7% [−8.5%, −6.4%]), ΔS_WIS −0.0386 [−0.0437, −0.0326] (−7.2% [−8.0%, −6.1%]): **observed joint improvement**; the point-error score (S_MAE) difference's 95% interval lies wholly below zero (better) and the interval score (S_WIS) difference's 95% interval lies wholly below zero (better). | U24 L114, L115; DEC24 `contrasts` | S |
| C425 | DDNN-2 alone against L, its same-information twin (point only): ΔS_MAE −0.0712 [−0.0910, −0.0545] (−12.9%); WIS not defined (L has no interval forecast): **MAE only (L has no interval forecast): lower (better)**. | U24 L116; DEC24 `contrasts` | S-d |
| C426 | DDNN-2 alone against v3 (LEAR): ΔS_MAE −0.0872 [−0.1107, −0.0662] (−15.4% [−18.8%, −11.8%]), ΔS_WIS −0.1052 [−0.1272, −0.0845] (−19.8% [−23.0%, −16.0%]): **observed joint improvement**; the point-error score (S_MAE) difference's 95% interval lies wholly below zero (better) and the interval score (S_WIS) difference's 95% interval lies wholly below zero (better). | U24 L118, L119; DEC24 `contrasts` | S-d |
| C427 | DDNN-2 alone against v4: ΔS_MAE −0.0571 [−0.0786, −0.0388] (−10.7% [−14.0%, −7.3%]), ΔS_WIS −0.0785 [−0.0982, −0.0608] (−15.5% [−18.8%, −11.9%]): **observed joint improvement**; the point-error score (S_MAE) difference's 95% interval lies wholly below zero (better) and the interval score (S_WIS) difference's 95% interval lies wholly below zero (better). | U24 L120, L121; DEC24 `contrasts` | S-d |
| C428 | DDNN-2 against CP-23's DDNN: ΔS_MAE −0.1534 [−0.1795, −0.1242] (−24.3% [−27.0%, −20.3%]), ΔS_WIS −0.1436 [−0.1686, −0.1107] (−25.2% [−28.0%, −20.3%]): **observed joint improvement**; the point-error score (S_MAE) difference's 95% interval lies wholly below zero (better) and the interval score (S_WIS) difference's 95% interval lies wholly below zero (better). | U24 L122, L123; DEC24 `contrasts` | S-d |
| C429 | DDNN-2 in LightGBM's place ((v3 + DDNN-2) − v4): ΔS_MAE −0.0200 [−0.0257, −0.0130] (−3.7% [−4.7%, −2.4%]), ΔS_WIS −0.0181 [−0.0233, −0.0118] (−3.6% [−4.5%, −2.3%]): **observed joint improvement**; the point-error score (S_MAE) difference's 95% interval lies wholly below zero (better) and the interval score (S_WIS) difference's 95% interval lies wholly below zero (better). | U24 L124, L125; DEC24 `contrasts` | S-d |
| C430 | Beside it, CP-23's DDNN in LightGBM's place ((v3 + CP-23's DDNN) − v4): ΔS_MAE 0.0157 [0.0081, 0.0232] (+2.9% [+1.5%, +4.3%]), ΔS_WIS 0.0155 [0.0074, 0.0222] (+3.1% [+1.4%, +4.3%]): **observed joint worsening**; the point-error score (S_MAE) difference's 95% interval lies wholly above zero (worse) and the interval score (S_WIS) difference's 95% interval lies wholly above zero (worse). | U24 L126, L127; DEC24 `contrasts` | S-d |
| C431 | DDNN-2 as v3's third member ((v3 + DDNN-2) − v3): ΔS_MAE −0.0501 [−0.0563, −0.0425] (−8.9% [−9.7%, −7.5%]), ΔS_WIS −0.0448 [−0.0502, −0.0383] (−8.4% [−9.2%, −7.2%]): **observed joint improvement**; the point-error score (S_MAE) difference's 95% interval lies wholly below zero (better) and the interval score (S_WIS) difference's 95% interval lies wholly below zero (better). | U24 L128, L129; DEC24 `contrasts` | S-d |
| C432 | Whether LightGBM still adds once DDNN-2 is present (v5 − (v3 + DDNN-2)): ΔS_MAE 0.0067 [0.0033, 0.0097] (+1.3% [+0.6%, +1.8%]), ΔS_WIS 0.0062 [0.0031, 0.0089] (+1.3% [+0.6%, +1.8%]): **observed joint worsening**; the point-error score (S_MAE) difference's 95% interval lies wholly above zero (worse) and the interval score (S_WIS) difference's 95% interval lies wholly above zero (worse). | U24 L132, L133; DEC24 `contrasts` | S-d |
| C433 | Equal-fold S_MAE/S_WIS (attempt 1): v5 0.5223/0.4937, v4 0.5357/0.5056, v3 + DDNN-2 0.5156/0.4874, v3 0.5658/0.5322, DDNN-2 alone 0.4785/0.4271, CP-23's DDNN 0.6319/0.5706. | M24 equal-fold rows | S |
| C434 | Original §8 screen (diagnostic): DDNN-2 alone met, v3 met, v4 met, v3 + DDNN-2 met, v5 met. | C24 | S |
| C435 | v5 per-fold MAE: ordinary folds 4.8–14.4 EUR/MWh; stress fold 3 45.5 EUR/MWh (v4: 47.0; v3: 48.0). | M24 L63–L67 | S |
| C436 | DDNN-2 alone, calibration (pooled): 50/80/95% coverage 0.484 / 0.794 / 0.954; PIT shares below 0.05 and above 0.95 0.051 and 0.045 (0.05 each if calibrated). | DG24 `calibration` | S-d |
| C437 | Pooled error correlations: D2 with D 0.79, D2 with HG 0.83, D2 with L 0.80, D with L 0.83, HG with L 0.79. | DG24 `error_correlations_pooled` | S-d |
| C438 | Guards over 5,088 attempt member fits: cap activations 583 emitted slot-levels; winsorised forecast inputs 12,972; ensemble crossings restored 0; nonfinite-loss stops 0. | GU24 | S |
| C439 | All §23.10 controls and the inherited ones passed (80 checks), each negative paired with a positive: masking and future inputs exactly 0.0; a non-uniform D−1 mutation, weather permutations, held-out weeks and recent training days move DDNN-2; search and gate outcomes after their cut-offs change nothing; pre-registration by ancestry; composite parity on every key; restart replay and cache refusals. | CT24 | S |
| C440 | Fit cost and the daily cycle (diagnostic only): 5,088 attempt member fits, median eight-member ensemble 17.5 s per origin; v5's cold daily cycle median 17 s, maximum 42 s at 25 origins. | FC24; DC24 | S |
| C441 | Leakage ruled out at every origin: with every outcome on or after the delivery day destroyed, the frozen eight-member ensemble refitted at all 636 warm-up and evaluation origins reproduces the committed DDNN-2 vectors bit for bit (636 of 636); a D−1 price mutation moves them and a planted one-day leak is detected in every fold; the search and gate controls hold in all 5 folds. | LK24 | S |
| C449 | Development evidence after selection on the same five folds CP-15 and CP-20 to CP-23 used; DDNN-2 is the second DDNN decision on them; not a test on new data; 4.7T carries the protection. | CAP §23.1 | S |

## Withheld claims: do not use

W1–W41 in the earlier maps stay in force. CP-24 adds:

| ID | Withheld claim | Reason / controlling source |
|---|---|---|
| W42 | Saying that distributional neural networks "do not work" or "cannot help" in general | One design family under one rule (C403, C421 or the gate claims); no demonstrated preference is not a proof of absence. |
| W43 | Calling v5 and v4 equivalent | A mixed or spanning result is no demonstrated joint preference (CAP §23.9). |
| W44 | Attributing any forecast or metric to PyTorch | PyTorch is a test-only correctness reference (CAP §18.3). |
| W45 | Stating or implying that v5 or DDNN-2 is the product, is live, runs in the demo or retrains in the browser | v1 is the released product and demo (C402); runtimes other than the evaluated one are unmeasured. |
| W46 | Presenting the gate as evidence of improvement | The gate is a screen on pre-fold days, not a claim (CAP §23.6). |
| W47 | Quoting a 95% interval as the decision interval for v5 − v4 | Condition 1 reads the attempts-adjusted 97.5% interval. |
| W48 | Quoting any CP-24 number without its evidence class, or as a confirmatory or significance result | Development after selection; exploratory intervals. |

## Gaps: documented, not resolved

| ID | Gap | Why it stays open |
|---|---|---|
| G30 | Learned weights, new information, other families | Excluded: 4.8 and stage 7 (CAP §23.5, §22). |
| G31 | Hosted-service and product uses | Unresolved in 4.6L; carried to 4.7 and 4.10 (LIC24). |
| G32 | DDNN-2 in another runtime and its equality with the evaluated code | Unmeasured (CAP §18.2 item 4). |
| G33 | Status dates, the evidence tag and the landing record | They exist only at landing (pending fields). |

