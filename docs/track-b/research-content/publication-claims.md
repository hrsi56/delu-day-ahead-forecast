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
