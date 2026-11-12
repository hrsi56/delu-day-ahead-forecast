# PRES-5: claim-to-evidence map

**2026-11-05 · PRES-5, under PUBLISH_RULES 1.5 and research v21-r20 §24.14 item 6.** The claims the publication of
the research since v5 renders: A1, the final candidate, in v5's comparison; CP-26's re-baseline on every development
day; CP-28's selection; the freeze and 4.7T's registered terms; and the live product. Each claim is mapped to a
committed file and the field it reads. Values here are rounded from the saved values; the rendered surfaces bind to
evidence records of `src/delu_forecast/research.py` or derived records of `src/delu_forecast/derived.py`, never to these
digits. Every research number uses development data only, delivery days through 2026-09-06 (§24.14, P1).

**Default evidence class:** `development_post_selection`. 4.7T is A1's one test; nothing here is a test result.

**Naming (the Orchestrator's ruling O30, 2026-11-05, at the Owner's request).** A1 is published as the newest generation,
**"v6 · DDNN-2 alone"**, selected by CP-28's pre-specified rule, with the status "final candidate · pending 4.7T". The
frozen records keep "A1", so the surfaces say "v6 (A1 in the frozen records)" where the identity is shown. The claims
below say A1 where they quote a frozen record and v6 where they describe the publication.

## Source keys

| Key | File |
|---|---|
| A1R | [reports/pres5/a1-in-v5/](../../../reports/pres5/a1-in-v5/) — `metrics.csv`, `uncertainty.csv`, `ratio-intervals.csv`, `summary.json`, `parity.json`, written by `src/delu_forecast/final_candidate.py` from the inputs below |
| FC28 | [reports/cp28/forecast/hourly.parquet](../../../reports/cp28/forecast/hourly.parquet) and `arm-days.parquet` (CP-28's stored forecasts; manifest `f092140e…`) |
| P24 | [reports/ddnn2/attempt-1/predictions.parquet](../../../reports/ddnn2/attempt-1/predictions.parquet), `metrics.csv` (v5's committed rows) |
| OS28 | [reports/cp28/owner-summary.json](../../../reports/cp28/owner-summary.json) |
| PK28 | [reports/cp28/publication-packet.json](../../../reports/cp28/publication-packet.json) `arms` |
| SEL28 | [reports/cp28/results/selection.json](../../../reports/cp28/results/selection.json) |
| R28 | [reports/cp28/report.md](../../../reports/cp28/report.md) |
| L28 | [docs/track-b/cp-28-landing-2026-10-25.md](../cp-28-landing-2026-10-25.md) |
| X26 | [reports/rebaseline/cold-rerun-2026-10-15/MLflow-export.json](../../../reports/rebaseline/cold-rerun-2026-10-15/MLflow-export.json) `runs[].metrics` |
| PK26 | [reports/rebaseline/cold-rerun-2026-10-15/presentation-v21-r16/publication-packet.json](../../../reports/rebaseline/cold-rerun-2026-10-15/presentation-v21-r16/publication-packet.json) `headline_quantities.comparisons` |
| R26 | [reports/rebaseline/cold-rerun-2026-10-15/presentation-v21-r16/report.md](../../../reports/rebaseline/cold-rerun-2026-10-15/presentation-v21-r16/report.md) |
| L26 | [docs/track-b/cp-26-landing-2026-10-21.md](../cp-26-landing-2026-10-21.md) |
| L17 | [docs/track-b/cp-17-landing-2026-10-28.md](../cp-17-landing-2026-10-28.md) |
| L17B | [docs/track-b/cp-17b-landing-2026-10-29.md](../cp-17b-landing-2026-10-29.md) |
| L17C | [docs/track-b/cp-17c-landing-2026-10-30.md](../cp-17c-landing-2026-10-30.md) |
| PROT | [docs/track-b/evidence/cp-17/4-7t-frozen-protocol.md](../evidence/cp-17/4-7t-frozen-protocol.md) |
| D20 | [docs/track-b/owner-decisions-2026-10-29.md](../owner-decisions-2026-10-29.md), decisions 20–21 |
| D28 | [docs/track-b/owner-decisions-2026-11-05.md](../owner-decisions-2026-11-05.md), decision 28 |
| L18B | [docs/track-b/cp-18b-landing-2026-11-05.md](../cp-18b-landing-2026-11-05.md) (O13, O17) |
| CAP | capstone_v21.md v21-r20, §24.4, §24.7, §24.8, §24.12, §24.14 |

## Claim map: A1 in v5's comparison

Status codes: **S** supported by a saved value or verdict; **S-d** supported, descriptive only; **Def** a definition;
**O** an Owner decision.

| ID | Claim | Source → table/row | Status |
|---|---|---|---|
| C901 | A1 is DDNN-2 alone with its own seven quantiles: no LEAR, no LightGBM, no blend; eight networks (four configurations, two seeds) refitted every day on the 728 days before the origin, issued at D−1 11:00 Europe/Berlin; frozen since 2026-10-30 for 4.7T. | CAP §24.7 "Training and information", "DDNN-2's training-only search"; CAP §24.8 "A1 keeps DDNN-2's own Johnson SU quantiles"; L17C | S |
| C902 | On v5's own population (10,747 hours, five periods, equal weights, B0 as the denominator), A1's equal-fold change against v5 is −6% [−9%, −2%] on S_MAE and −11% [−15%, −8%] on S_WIS at 95%, and [−10%, −2%] and [−15%, −8%] at 97.5%; A1's stored forecasts cover 10,747 of 10,747 hours, scored by CP-24's code with CP-20's draws, and the recomputed v5, v3 and B0 scores equal CP-24's committed rows exactly. | A1R `ratio-intervals.csv` (A1-v5), `uncertainty.csv` equal_fold rows, `summary.json` coverage, `parity.json` max_abs_difference 0 | S-d |
| C903 | Both paired differences A1 − v5 lie below zero at 95% and at 97.5%; against the naive, −51% [−54%, −46%] on S_MAE and −56% [−59%, −52%] on S_WIS. v5's adoption rule is not re-run and adopts nothing. | A1R `ratio-intervals.csv` (A1-B0), `uncertainty.csv` | S-d |
| C904 | A1's information set differs from v5's in these periods: issue time 11:00 Berlin against 11:00 UTC; daily refits on 728 days against one fit per period; its own searches every 182 days from 2020-01-15 on earlier data only; CP-25's data identity and registered vintages; the first period lies in CP-26's unscored warm-up (2020-01-01 to 2020-12-28), with less than 728 days of history. | A1R `summary.json` `information_set`; CAP §24.4, §24.7 "Days"; FC28 `arm-days.parquet` `scored` | S |
| C905 | A1 was selected on CP-26's calendar, which contains the old folds 2–5 (358 days), after CP-26's report had shown DDNN-2 alone as the best single model there; development evidence after selection; 4.7T is its one test. | CAP §24.8 "Disclosed in advance"; R28 "Disclosures"; L26 | S |
| C906 | CP-28 selected arm A1, now v6, on 2026-10-25 under its rule set 2026-10-12, N = 7 arms; the six others, blends of v5's members, also passed every gate and were not selected (SEL28 `passes_all_four`); CP-17 froze it on 2026-10-28, CP-17b re-froze it on 2026-10-29, CP-17c on 2026-10-30, the fit unchanged each time (L17B; L17C); its status is "final candidate · pending 4.7T"; it was selected by its own rule, never adopted by v5's; v1 is the last released generation (registry status "released"), its demo historical at the Space's `/history/`, and the product again if 4.7T does not pass. | L28; L17; L17B; L17C; SEL28 `passes_all_four`; L18B O13; D20 decisions 20–21; D28; the Orchestrator's rulings O27, O29, O30 | S, O |
| C907 | A1's per-period paired differences against v5 and its per-period MAE (ordinary periods 4.5–13.4 EUR/MWh, the 2022 crisis period 43.2), beside v5's. | A1R `metrics.csv` per_fold, `uncertainty.csv` per-fold rows; P24 `metrics.csv` | S-d |
| C908 | Pooled over the five periods, A1's 95% intervals covered 0.9447 of the hours at a mean width of 82.4 EUR/MWh, against v5's 0.9395 at 100.2 (100.248). | A1R `metrics.csv` pooled; P24 `metrics.csv` pooled | S-d |

## Claim map: CP-26, the re-baseline on every development day

| ID | Claim | Source → table/row | Status |
|---|---|---|---|
| C601 | CP-26 re-ran B0, v1's recipe, v2–v5 and DDNN-2 alone daily on every eligible development day, 2020-12-29 to 2026-09-06, 2,068 days, under one protocol; the old five-period results stay the historical record; development, post-selection; no adoption decision follows. | CAP §24.7; L26 "What CP-26 established"; R26 header | S |
| C602 | The every-day mean daily losses and their ratios to B0 for each stream and mask (all eligible: B0 34.6/21.1, v1-R 35.0/19.4, v2 22.6/13.4, v3 19.7/11.6, v4 18.6/10.9, v5 18.5/10.9, DDNN-2 alone 17.2/9.7 EUR/MWh, MAE/WIS). | X26 `runs[].metrics` (`MAE/raw_mean_daily_loss`, `WIS/raw_mean_daily_loss`, `*/B0_ratio`) | S-d |
| C603 | v5 against v4 on every eligible day: −1% [−1%, +1%] on MAE and on WIS (95%); the five-fold gain is not shown on every day; the interval spans zero, which does not establish equality (PUBLISH_RULES §3.2; Integration review 1, F4). | PK26 `headline_quantities.comparisons` (v5 vs v4, all_eligible), L26 | S-d |
| C604 | DDNN-2 alone (A1's forecasts) has the lowest every-day MAE and WIS, −7% and −11% against v5. The page and the README bind these to CP-28's control ratios with the selection's descriptive 95% intervals (`derived.cp28.A1.*`, block `everyday.finding.v6`), which equal X26's committed mean daily losses' ratios (`derived.cp26.v6-v5.*`). | X26 (nominal/D2 and nominal/v5, all_eligible); OS28 | S-d |
| C605 | The GFS +6 h route worsens v5 by +14% MAE (95% ratio interval 1.103–1.161) and +15% WIS (1.121–1.176): fragile. The no-load route moves v5 by under 1% MAE and about +1% WIS. | OS28 `gfs_note_headline` (CP-28's committed note on CP-26's outputs); X26 (noload/v5, nominal/v5) | S-d |

## Claim map: CP-28, the selection

| ID | Claim | Source → table/row | Status |
|---|---|---|---|
| C701 | The rule, set 2026-10-12 (the Owner) and frozen in CP-28's protocol before CP-26's first score: seven arms against nominal v5 on CP-26's calendar; improvement margin 0.995 on MAE and WIS; non-inferiority 1.02 in each complete year 2021–2025 and pooled season; compound maximum; Holm across seven at 0.05; the primary analysis and the 7-day, 28-day and unstratified variants; the lowest WIS among the passing arms, ties within 0.5% by simplicity. | CAP §24.8 "The arms", "The gates", "Selection"; R28 | S |
| C702 | All seven arms rejected their compound null under Holm in all four analyses; A1's compound p-values 0.0042, 0.0069, 0.0022, 0.0053. | OS28 `holm` | S |
| C703 | A1 has the lowest paired WIS, 9.68 EUR/MWh, and no arm lies within 0.5% of it (tie bound 9.73; the next lowest, A6, 10.13); A1 is selected. No blend of v5's members was selected. | SEL28 `wis_paired_with_control`, `tie_bound`, `selected` | S |
| C704 | Against the control on the 2,068 paired days, the six blends changed WIS by −4% to −7% and A1 by −11% [−13%, −9%] (descriptive studentized 95% intervals); MAE −7% [−9%, −5%] for A1. | PK28 `arms.*.ratio_to_control`, `ratio_to_control_ci95` | S-d |
| C705 | CP-28's Holm control is conditional on the Owner's decision to run it, which followed CP-26's report showing DDNN-2 alone on the same calendar. | CAP §24.8 "Disclosed in advance"; R28 | S |
| C607 | CP-26's disclosures, carried into v6's limitations: the day-ahead load forecast is tier 3 (its historical values are not original vintages), the target price is tier 2 with SMARD's "update possible" caveat, and the structural margins are accepted risks; the GFS +6 h route worsened v5 by +14% MAE (C605). | PK26 `claim_map` (the CP-25 rulings §1–§3 rows); docs/track-b/cp-25-rulings-2026-10-12.md; OS28 | S |
| C706 | Every arm has 18 fallback dates, 2022-12-04 to 2023-06-20, with a missing member; none falls in v5's five periods. | OS28 `fallbacks`; A1R `summary.json` `coverage.fallback_days` 0 | S |

## Claim map: the freeze and 4.7T, registered before the test

| ID | Claim | Source → table/row | Status |
|---|---|---|---|
| C801 | CP-17 froze A1 on 2026-10-28 as the product's complete daily policy, one package run unchanged by the issuing host and the browser; CP-17b re-froze it on 2026-10-29 with decisions 13–19; CP-17c re-froze it on 2026-10-30 under the `macos-26` issuing host, policy identity `720fc581…`, 58 of 58 fits bit-identical on the runner and on the Owner's M3. | L17; L17B; L17C | S |
| C802 | The issuing host is Pyodide 0.28.0 in Node.js v26.7.0 (decision 10), on a GitHub `macos-26` runner or the Owner's Mac. | L17; L17C | S |
| C803 | 4.7T's registered terms: delivery days 2026-09-07 to 2026-12-05, 90 days, opening no earlier than 2026-12-04, never extended, shortened or rolled; control v5 and reference B0, run under CP-26's rules; v3, v4 and v1's artifact descriptive; p50 MAE and seven-quantile WIS, daily losses; endpoints A1 − 0.995·v5 and A1 − B0 on both scores; the compound p-value the largest of four one-sided p-values, a pass at or below 0.05; a 7-day block bootstrap with 10,000 replicates; at least 60 of 90 dates paired and scored, else inconclusive; no runner-up moves up, the window is spent, a null result is valid. | PROT §§1–8; CAP §24.12 | S |
| C804 | What each result means: decision 28 put A1 (v6) on the Space before 4.7T, so a pass keeps it as the product and ends its "pending" status; a fail or an inconclusive result makes v1 the product again (decision 21's fail branch); the registered wording "It passed the pre-registered test" and "It did not pass; the window is spent, and v1 remains the product" (decision 20); the live record stays "prospective evaluation in progress" until at least 90 consecutive days are scored. | D20 decisions 20–21; D28; PROT §8, §12; CAP §24.14 item 5; the Orchestrator's ruling O29 | O |

## Claim map: the publication's own wording (PRES-5)

| ID | Claim | Source → table/row | Status |
|---|---|---|---|
| P60 | **The headline when the final candidate leads** (decision 20's fresh-headline window: development, post-selection results until 4.7T is scored): CP-28's verdict against v5 on all 2,068 days, each metric named (A1), "as shares of v5's, with descriptive 95% intervals" (editorial V3), and N = 7 policies tested; the rule "set before any result"; the terms beneath define the two errors, the selection rule, the final candidate and DDNN-2. The derived records `derived.cp28.*` and `derived.cp26.*` carry these changes as (ratio − 1) × 100. | OS28; PK28; SEL28; D20; PUBLISH_RULES §2, §3.2 | Def, O |
| P61 | **The product line in the opening**: the Space runs v6 daily, frozen, before its one test, by the Owner's decision to go live (decision 28: why this product runs this model, editorial V2); prospective evaluation in progress; a pass releases it, otherwise v1, the last released generation, is the product again (C804); v1's historical demo is linked at the Space's History. Beside the action (§7.1; Integration review 1, F1), the build's renderer reads from CP-18b's committed records the first visit's size (`reports/cp18b/space-build.json` `size.first_visit.bytes`, 551,515), the measured cold start in Chromium and WebKit (`reports/cp18b/acceptance.json`, the "fresh anonymous cold start" checks, 1.86 s), the browsers, the machine, the measurement date and the last verification; the Space served locally, on development data. v1's measured start of 2026-09-29 timed the earlier Space's root, which decision 28 gives to the live product, so the opening links v1's demo without timing it. v6's status reads "final candidate · pending 4.7T"; the page never says or implies that the Space runs v1 now. | D28; CAP §24.14 item 5; L18B (O13; O17; "The Space's first visit": 551,515 bytes); the Orchestrator's rulings O27, O29 | O |
| P62 | **The comparison with A1 first**: A1's row comes from A1R, scored on the same population; its finding sentence and caveat state that A1's forecasts come from a later protocol; MLflow holds no run of A1 on this population, so the comparison's MLflow route lists the twelve rows it holds. | A1R; the registry's `expected_routes` | S |
| P63 | **CP-28's arms in the registry**: CP-28's parent is v6's checkpoint; its six other arms are study arms, "not selected", without codes on the page (ruling O30); the arms' table in v6's chapter names them in words. | L28; SEL28; runbook §2 | S |
| P65 | **"From v5 to v6: DDNN-2 alone"** (A3): the predecessor v5, the change (DDNN-2 alone, its own quantiles, refitted daily), the comparator set in advance (v5, the selection rule's control, also the predecessor), the result on every development day and on v5's five periods with their intervals and class (development, post-selection, not 4.7T), and what it does not establish. | L28; A1R; OS28; PK28; ruling O30 | S, O |
| P66 | **"How the product works" documents v6**, the policy the Space runs (rulings O26 and O29: decision 28 of 2026-11-05 prevails over decision 21's timing of the product switch; decision 21's fail branch and its reason, one identity for panel, demo and daily policy, survive). The twelve subjects: data and cutoff, regimes, inputs with the seasonal rationale (3, 3b), validation, results, failures and reliability supported from A1R, OS28, PK28, X26 and the freeze records; attribution (6) and importance (7) not evaluated in the report, routed to the live product's Explainability and Features views; the forecast (10) routed to the live product; limitations from C905, C904, C605 and C607; running and checking it from L17C's `refreeze verify`. Shared facts kept after an applicability check: the target, the preprocessing, the regimes' development hours, the seasonal rationale of the calendar inputs. v1's manual stays in v1's chapter, its archive and the repository history (runbook §7a). | L17C; A1R; OS28; PK28; X26; D28; ruling O29 | S, O |
| P64 | **The planned list after PRES-5**: the re-evaluation on every eligible day (CP-26) and combining models (CP-28) leave the list; 4.7T at its date and the live trial, "prospective evaluation in progress", lead it; new input data and renewable-generation forecasts stay, unscored and unnumbered. | CAP §24.14; PUBLISH_RULES §5 item 6 | Def |

## Withheld claims: do not use

W1–W48 in the earlier maps stay in force, with one narrowing, dated: since decision 28 (2026-11-05), v6 (A1), DDNN-2
alone and frozen, is the policy the live product runs, so W45 no longer withholds that. W45 still withholds v5 as the
product, and "DDNN-2" as the demo or the product without the frozen v6's identity. PRES-5 adds:

| ID | Withheld claim | Reason / controlling source |
|---|---|---|
| W49 | Calling v6 (A1) "adopted" or "adopted in research" | It is the newest generation by the Owner's request (ruling O30), selected by CP-28's rule as the final candidate; no adoption rule decided it (PK28 `transition`), and v5's rule is not re-run (C903). |
| W50 | Presenting A1's comparison on v5's population as made under v5's protocol or information set | C904. |
| W51 | Pooling CP-26's every-day results with the five periods, or calling either a test on new data | C601; CAP §24.7. |
| W52 | Presenting any live forecast, score or price, or any number on a delivery day after 2026-09-06, as research, or calling the live record 4.7T's result | CAP §24.14 items 2 and 5; P1. |
| W53 | Giving v6 (A1) the status "live" or "released", or calling it the released product, before a passed 4.7T; or calling the prospective record an evaluation result. The Space's daily product is "the live product" (decision 28, §24.14 item 5); A1's status is "final candidate · pending 4.7T" | O13; D20; D21. |
