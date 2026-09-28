# Publication Standard v1: claim map for the headline, the derived records and the registry

**2026-09-28 · PRES-1 conformance (brief W3–W9).** The claims below carry the wording the
[Publication Standard v1](../evidence/pres-1/publication-standard-v1.md) requires on every surface:
the headline block, its definitions, the orientation sentences, the dated statuses and the release
rule. Every number in them is a **typed derived record** from `src/delu_forecast/derived.py`, or an
evidence record from `src/delu_forecast/research.py`; every name and status comes from the
registry, `src/delu_forecast/registry.py`. The format and the row-reference convention are those of
the [CP-15/CP-16 claim map](cp15-cp16-claims.md) (`L<n>` is the physical line; for a CSV, `L1` is
the header). Nothing was recalculated from predictions, refitted, replayed or downloaded: a derived
record is arithmetic on committed cells.

**Default evidence class.** Every research result here is **`development_post_selection`**
([R20](../../../reports/weather-ablation/report.md) L5; [CP-15/CP-16 map](cp15-cp16-claims.md)).

## Source keys

| Key | File |
|---|---|
| A21 | [capstone_v21.md](../../../capstone_v21.md) (the ratified research anchor) |
| A21-1 | [reports/cp15/attempt-1/capstone_v21.md](../../../reports/cp15/attempt-1/capstone_v21.md) (the anchor preserved from attempt 1) |
| C15 | [reports/cp15/criteria.csv](../../../reports/cp15/criteria.csv) |
| C16 | [reports/v2-causal/criteria.csv](../../../reports/v2-causal/criteria.csv) |
| C20 | [reports/weather-ablation/criteria.csv](../../../reports/weather-ablation/criteria.csv) |
| M16 | [reports/v2-causal/metrics.csv](../../../reports/v2-causal/metrics.csv) |
| M20 | [reports/weather-ablation/metrics.csv](../../../reports/weather-ablation/metrics.csv) |
| U16 | [reports/v2-causal/uncertainty.csv](../../../reports/v2-causal/uncertainty.csv) |
| U20 | [reports/weather-ablation/uncertainty.csv](../../../reports/weather-ablation/uncertainty.csv) |
| RS15 | [reports/cp15/relative_scores.csv](../../../reports/cp15/relative_scores.csv) |
| P10 | [reports/cp10/protocol.json](../../../reports/cp10/protocol.json) |
| REG | [src/delu_forecast/registry.py](../../../src/delu_forecast/registry.py) |
| DER | [src/delu_forecast/derived.py](../../../src/delu_forecast/derived.py) |
| STD | [Publication Standard v1](../evidence/pres-1/publication-standard-v1.md) |

## Claim map: derived records (standard §3.3)

| ID | Claim | Source → table/row | Status |
|---|---|---|---|
| P16 | **The pre-specified verdict, per evaluated policy.** Criteria 1–2 of capstone v21 §8: each error score at most 0.90 times the lowest score among B0–B3 (daily LEAR, B2, in both scores). Met or not met; the distance from daily LEAR in the rule's unit (the policy's score over daily LEAR's, minus one, in whole percent; a point comparison, no confidence interval exists); N, the distinct policies tested against the rule up to that decision, in checkpoint order, one identity counted once (v2 is V2-H in CP-16 and H0 in CP-20); and whether it was the first to meet the rule. Results: A1–A5 not met (N = 1–5); v2 not met, −2% / −4% (N = 6); the pooled-interval control not met (N = 7); **v3 met, −14% / −17%, N = 8, the first to meet it**. | C15 L2–L3, L23–L24, L44–L45, L65–L66, L86–L87; C16 L2–L3, L23–L24; C20 L2–L3, L23–L24 (`actual`, `upper_limit`); RS15, M16, M20 (`equal_fold` B0–B3); DER `derived.criteria.*` | S |
| P17 | **The rule, in words, with its date.** "At least 10% below the strongest benchmark": 10% is 1 − upper limit / daily LEAR's score, for both scores (C20 L23–L24 `upper_limit`; M20 `equal_fold` B2). The rule was set on **2026-09-15**: the anchor's own date line ("Active owner-authorized execution plan · 2026-09-15."), in A21 and in the anchor preserved from attempt 1 (A21-1), whose §8 is byte-identical to A21's. The pre-registration commit `bb5e678` (2026-09-16 00:17 +03:00) is reachable from the tag `evidence/cp-15`; CP-15's results were committed at `0be8e56` (03:15). | A21 L65, §8; A21-1 L3, §8; DER `derived.rule.*`; git `bb5e678`, `0be8e56`, `evidence/cp-15` | S |
| P18 | **The change against the comparator, as a share of the comparator's score.** The committed paired difference in each error score, and its 95% interval, each divided by the comparator's own equal-fold score (a fixed denominator). v3 against v2: point-error score −12% [−16%, −9%], interval score −14% [−17%, −11%]. v2 against daily LEAR: −2% [−4%, −1%] and −4% [−5%, −2%]. Never "N% lower error": absolute error changes by a different amount in each period. | U20 (`equal_fold` HG−H0); M20 (`equal_fold` H0); U16 (`equal_fold` V2-H−B2); M16 (`equal_fold` B2); DER `derived.change.*` | S |
| P19 | **Absolute context, EUR/MWh.** Mean absolute error per test period, as a range over the four ordinary periods, with the stress period stated separately. The protocol names the stress period: fold 3, 2022-07-01 to 2022-09-28, the 2022 crisis (A21 §7: "Report fold 3 and August 15–31 with their own dates and denominators"; CP-10's protocol calls it its diagnostic fold, P10 `diagnostic_fold`). v3 5.3–15.6 and 48.0; v2 6.3–18.7 and 51.2; daily LEAR 6.2–19.2 and 54.0; the naive 8.6–30.5 and 86.9. Context only: it never ranks and never leads (W11). | M20 (`per_fold` MAE, HG, H0, B2, B0); A21 §3, §7; P10; DER `derived.periods.*` | S |

## Claim map: the headline, the orientation layer and the registry's wording (standard §1, §3.4, §5)

| ID | Claim | Source → table/row | Status |
|---|---|---|---|
| P20 | **The headline block**, generated from the registry's current generation (v3) and its derived records, identical on the page's research status card and at the top of the README: "Met both accuracy targets set before the experiments: error scores at least 10% below the strongest benchmark, daily LEAR (v3: 14% and 17% below; the first of 8 policies tested to meet them)." with the badge "Development · post-selection". It leads with the pre-specified verdict because a rule existed (standard §3.4). | P16; P17; REG `current_generation()`; `research_claims.headline_template()` | S |
| P21 | **The terms the headline introduces**, defined directly below it: error scores (the standard §3.1 definition), accuracy targets (set 2026-09-15; the distances are point comparisons), daily LEAR (the strongest benchmark), policies, and the evidence class's own caveat ("development evidence, not a test on new data"). | STD §3.1, §1 (ii); P17; C68; C84 | Def |
| P22 | **The release rule, stated once, from the registry:** the demo runs the released model, v1; research generations are not released one by one; only the final model, after its one-shot test and live run, replaces the released one. Beside the demo action, outside any disclosure. | STD §5, §1 (iii); REG `RELEASE_RULE`, `released()` | Def |
| P23 | **Names and dated statuses from the registry:** every canonical name, the adoption labels (Released; Adopted in research; Not adopted) and the dated past-tense status sentences ("In September 2026, v3 was adopted in research."). The dates are the registry's status records: v1 released 2026-09-15 (CP-3 and CP-3B landings), v2 adopted in research 2026-09-23 (CP-16 landing), v3 2026-09-24 (CP-20 landing), the branches, study arms and control not adopted 2026-09-16 and 2026-09-23. | REG `_ENTRIES`; LD20; the CP-16 and CP-15 landing records | Def |
| P24 | **The comparison's finding and its main caveat** (standard §1 i): v3 against v2, as a share of v2's error scores, −12% [−16%, −9%] (point) and −14% [−17%, −11%] (interval), with 95% confidence intervals; "Development evidence, not a test on new data. Meeting the targets is a development diagnostic, not a product qualification." | P18; C71; C78 | S |
| P25 | **The target line in words**, with its date, N and a met / not-met column: "The dashed lines mark the targets: each error score at least 10% below the strongest benchmark, daily LEAR (set 2026-09-15). 8 policies were tested against them; v3 met both, the first and only one to do so." The comparison's and the v2 scores chart's rows carry each policy's verdict. | P16; P17 | S |
| P26 | **Absolute context** in the comparison: v3's mean absolute error per test period, 5.3–15.6 EUR/MWh in the four ordinary periods and 48.0 in the 2022 crisis period; the similar-day naive's 8.6–30.5 and 86.9. Context only. | P19 | S |
| P27 | **The branch cards** (standard §6): the calibration experiment asked whether recalibrating v1 without refitting it could repair its crisis coverage, and was not adopted because recalibration alone was not enough; the model comparison study asked which forecasting approach copes best with the 2022 crisis, and was not adopted as such (no policy met the criteria) but informed v2's blend of two LEAR forecasts. The diagnostics are P12 and C21. | P12; C21; C30; REG `calibration`, `model-comparison` | S/Def |
| P28 | **The stack line**, rendered from the system view's data: Python, entsoe-py, pandas, NumPy, DuckDB, LightGBM, scikit-learn, Parquet, GitHub Actions, GitHub Pages, marimo, Pyodide, the Hugging Face Static Space and MLflow on DagsHub. Each is a dependency in `pyproject.toml` or a service the project deploys to. | `pyproject.toml`; `.github/workflows/tests.yml`; `docs/deploy.md` | Def |
| P29 | **The chapters' questions** (the chapter grammar's first slot): v3 — do weather forecasts available before the auction improve v2? v2 — could a different forecasting model repair v1's failure in the 2022 crisis? | C65; C53; C10 | Def |
| P30 | **v3's reading, in one sentence:** both confidence intervals lie below zero and every test period favours v3; its prediction intervals are narrower in every period, with pooled 95% coverage slightly lower, 0.9377 against 0.9389. | C71; C72; C80 | S |
| P31 | **v2's development caveat,** phrased as a property of its evidence class: development evidence, not a test on new data. | R16; CP-15/CP-16 map (default evidence class) | S |
| P32 | **v2's decision, dated:** in September 2026, v2 was adopted in research; v3 was built on it. | P23; C65 (HG = H0 + weather) | S |
