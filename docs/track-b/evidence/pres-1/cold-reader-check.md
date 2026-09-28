# PRES-1 conformance: the cold-reader check (Publication Standard v1 §11)

**Outcome: PASS.** Both cold readers answered questions 1–5 in agreement with the registry and the
derived records, from the §1 placements. Their other observations are advisory; three reading
defects they found were fixed at `4dbdfbb`, and the rest are in
`docs/track-b/publication-advisory-log.md` (A-PRES1-9 to A-PRES1-18).

## How it was run

- **Page:** `docs/index.html` at `c6dda1f6b917f61f7793bcd57b23e2be086036ef` (SHA-256
  `222bf6442593988ea99c5e4d8c59db4a901192eb4b98009aefe0362f65f28b94`), every disclosure closed.
- **Screens:** written by `scripts/check_reader_paths.py release` (standard §10 record
  `reports/presentation/release-checks/2026-09-28-standard-s10.json`, `cold_reader_screens`): the page
  as a reader scrolls it, one viewport at a time, each step the viewport less the sticky header.
  - Desktop: Google Chrome 153 at 1,440 × 900, 12 screens, a step of 844 px.
  - Phone: Playwright's WebKit 26.6 at 390 × 844, 20 screens, a step of 788 px.
  - Kept under `.local/artifacts/presentation/release/cold-reader/` (not committed).
- **Readers:** two fresh agents, one per set of screens, given no project context: only the image
  paths, the reading rules and the six questions of §11. They were told to read nothing but the
  images, to answer as a sceptical data-science lead, and to cite the screen and the words on it
  for questions 1–5. Neither wrote anything in PRES-1.
- **Date:** 2026-09-28.

## Grading: answers 1–5 against the registry and the derived records

The pixel placements are the §10 record's (Chrome / WebKit). A cited screen covers document pixels
from `(n − 1) × step` for one viewport.

| Question | What the registry and the derived records hold | Desktop reader | Phone reader | Within the §1 placement |
|---|---|---|---|---|
| 1. The headline result, with its numbers | v3 met both targets set before the experiments: error scores at least 10% below daily LEAR; v3 14% and 17% below; the first of N = 8 policies (`derived.criteria.v3.*`); change against v2 −12% [−16%, −9%] and −14% [−17%, −11%] (`derived.change.v3.*`) | All of it, screen 1; the change against v2 on screens 2–3; also the per-period ranges 5.3–15.6 and 48.0, naive 8.6–30.5 and 86.9 (`derived.periods.*`) | All of it, screen 1; the change against v2 on screen 4 | Yes. The headline block ends at 775 / 775 px on desktop and 605 / 605 px on the phone, inside the first screen. The finding sentence ends at 1,766 / 1,767 px (limit 1,800) and 2,489 / 2,490 px (limit 2,532) |
| 2. Against what? | The rule's comparator: daily LEAR, the strongest benchmark; the registry's comparator for v3: v2; scores relative to the similar-day naive | Daily LEAR, the naive as the normalizer, and v2 with paired intervals; screens 1–3 | The same; screens 1, 4–6 | Yes. Daily LEAR is in the headline and defined directly below it |
| 3. How sure, and on what evidence | Development · post-selection; "development evidence, not a test on new data"; "a development diagnostic, not a product qualification"; the distances are point comparisons; the v3–v2 intervals exclude zero | All of these, with the screens and quotes; screens 1–3 | All of these; screens 1, 4 | Yes. The badge is on screen 1; the qualifier and the interval are in the comparison panel, above its chart |
| 4. What the demo runs, and why not the best model | The released model, v1; the release rule: research generations are not released one by one, and only the final model, after its one-shot test and live run, replaces the released one | Both, screen 1 | Both, screen 2 | Yes. The release rule is beside the demo action, outside any disclosure (§10 record: `release_rule_in_disclosure` false) |
| 5. What was tried and dropped | Branches not adopted: the calibration experiment and the model comparison study (2026-09-16); the pooled-interval control (2026-09-23); the study arms | Both branches, with their one-line reasons; the normalized-LEAR arm "not met"; screens 2, 3, 7 | Both branches; the pooled-interval control; the normalized-LEAR arm; screens 3, 4, 11, 13 | The journey layer (§1): the lineage follows the opening, in §6's order |

**Answer 6** (what each reader would ask the candidate) is advisory input. Both asked about: the
selection behind "8 policies" and the one-shot test's window, rule and power; an interval for the
headline distance itself; whether the day-before GFS run was available before the auction; why
wind speed and solar radiation rather than TSO generation forecasts; v1's holdout baseline; interval
coverage behind the interval-score gain; and what the candidate built and checked personally. These
are the return's interview-capture triggers.

## What confused the readers, and what was done

| # | Observation | Reader | Disposition |
|---|---|---|---|
| 1 | Audit-grade link labels read "frozen2026-09-24" | both | **Fixed at `4dbdfbb`.** An `.ev` link is a flex box, and the label's text run dropped the space before the date span; the label is now one span |
| 2 | "v1 has its own:" was followed by the v3, v2 and study links | desktop | **Fixed at `4dbdfbb`:** "Each experiment below has its own full reproduction; v1's is in its archive." |
| 3 | "v3 :" in the reproduction list (the same flex spacing) | seen in the fix's screenshot | **Fixed at `4dbdfbb`** |
| 4 | "14% and 17%" are not matched to point and interval on screen 1 | both | Advisory, A-PRES1-9: the headline is the standard's §3.4 text, which the locked core fixes |
| 5 | The chart says seven policies, the text says 8 were tested | both | Advisory, A-PRES1-10 |
| 6 | v1's 1.052, "28.58% worse" and its holdout win seem to clash; the reconciliation is in a closed disclosure | both | Advisory, A-PRES1-11: invariant 4's statements keep their exact form |
| 7 | v1 is "one LightGBM quantile model" in one place and "A LightGBM ensemble" in another | both | Advisory, A-PRES1-12 |
| 8 | Daily LEAR is "refitted daily" and "fitted for each hour" | desktop | Advisory, A-PRES1-12 (both are true: one model per hour, refitted daily) |
| 9 | v2's pooled-interval control differs from v2 in point error (−0.0017) | both | Advisory, A-PRES1-13 |
| 10 | "+0.0000039", "+0.037" and "28.58%" look over-precise | both | No change: §4 requires a near-zero value to keep its sign and two significant figures, and invariant 4 protects v1's statements. Advisory note A-PRES1-14 |
| 11 | "Trained champion" is never defined | desktop | Advisory, A-PRES1-15 (v1's frozen archive vocabulary) |
| 12 | The preview beside v3's headline shows v1 | desktop | Advisory, A-PRES1-16 (the preview is the demo's model, by design) |
| 13 | The footer's "no additional runtime requests" sits oddly beside a demo that downloads 57 MB | desktop | Advisory, A-PRES1-17 (the statement is about the report page) |
| 14 | Which interval level the interval score uses is not shown; "released" reads as "the model in the demo" | phone | Advisory, A-PRES1-18 |

## The desktop reader's answers to questions 1–5 (excerpts)

The reader's words, with bullet lists run together and its sceptical asides left out (they are summarized
under answer 6 and in the table above):

> **1. Headline result**
> v3 is v2's blended-LEAR model plus three GFS weather-forecast inputs. It is the only one of 8 tested policies to meet both accuracy targets set in advance: both error scores had to be at least 10% below daily LEAR. v3's point-error score is 14% below it and its interval score 17% below. As ratios to a naive forecast, that is 0.566 vs 0.658 (point) and 0.532 vs 0.639 (interval). Against its predecessor v2, the gains are −12% [−16%, −9%] (point) and −14% [−17%, −11%] (interval), with 95% CIs. In money, v3's MAE is 5.3–15.6 EUR/MWh in the ordinary periods and 48.0 in the 2022 crisis. The naive scores 8.6–30.5 and 86.9.
> - Screens 1, 2–3 and 3.
> - Quotes: "v3: 14% and 17% below; the first of 8 policies tested to meet them" (1); "−12% [−16%, −9%] (point) and −14% [−17%, −11%]" (2–3); "v3 met both, the first and only one to do so" (3).
>
> **2. Against what?**
> The main comparison is daily LEAR, called "the strongest benchmark". It is a regularized linear model per hour, refitted daily. Every score is a ratio to a similar-day naive forecast, which scores 1.000. The second comparison is v2, with paired CIs. The chart also shows: daily LightGBM: 0.784 / 0.740; a normalized-LEAR study arm: 0.672 / 0.646; the released v1: 1.052 / 0.986.
> - Screens 1–2, 3 and 7.
> - Quotes: "the strongest benchmark, a linear model refitted daily" (2); "divides a model's error by that of a simple similar-day forecast" (3); "a regularized linear model fitted for each hour" (7).
>
> **3. How sure, and on what evidence?**
> All the research evidence is a historical backtest over five periods (one is the 2022 crisis) and the same 10,747 hours. It is labelled development evidence, post-selection. Nothing has been tested on new data. Solid within that data: v3 beats v2; both paired 95% CIs exclude zero: −0.0783 [−0.1006, −0.0570] and −0.0838 [−0.1044, −0.0655]; every period favours v3. Weaker: the 14% and 17% against the target are point estimates with no interval; the point-error gain in the crisis period alone is not significant: −3.2 [−6.1, +0.037] EUR/MWh; no single weather feature's effect is isolated; v3's 95% intervals cover 0.9377. The only confirmatory-style test anywhere is v1's 90-day holdout, labelled "not power-qualified".
> - Screens 1, 2, 3, 5, 6 and 9.
> - Quotes: "the distances are point comparisons" (1); "development evidence, not a test on new data" (2); "a development diagnostic, not a product qualification" (3); "There its confidence interval crosses zero" (6).
>
> **4. What does the demo run, and why not the best model?**
> The demo runs v1, the released model: a LightGBM that forecasts nine quantiles per hour, with conformal-calibrated 50/80/95% intervals. It runs in the browser (about 57 MB on first visit), and the chart replays a held-out day (2026-09-06). v3 is not in the demo because only the final model replaces v1, after a one-shot test and a live run.
> - Screens 1, 9 and 10.
> - Quotes: "The demo runs the released model, v1." (1); "only the final model, after its one-shot test and live run, replaces the released one" (1); "Planned, not evaluated" (10).
>
> **5. What was tried and dropped?**
> Calibration experiment, not adopted: recalibrating v1 improved coverage, but not enough ("Recalibration alone was not enough" (2); "the improvement was insufficient" (7)). Model comparison study, not adopted: its normalized-LEAR arm was "not met" (3); "No policy met the criteria; the study informed v2's blend" (2). LightGBM left the research line when v2 replaced "one LightGBM quantile model" (7). The other five of the 8 tested policies: not shown.
>
> **Earliest screen for questions 1–4:** Screen 1 answers 1 and 4. For 2 and 3 I needed the top of screen 2, because the definitions of daily LEAR and "post-selection" are cut off at the bottom of screen 1.

The reader's answer 6 and its list of confusions are summarized above; the full returns are kept in the
Lead's session transcript, not committed.

## The phone reader's answers to questions 1–5 (excerpts)

The reader's words, shortened the same way:

> **1.** The research model v3 is v2's blended-LEAR model plus three weather-forecast inputs. It scores 0.566 on point error and 0.532 on interval error, where both scores are ratios to a naive forecast. That puts it 14% and 17% below the strongest benchmark, beating the target of at least 10% that was set in advance. It is the only one of 8 policies to meet both targets. Against the previous version, v2, it improves by −12% [−16%, −9%] on point error and −14% [−17%, −11%] on interval error, with 95% confidence intervals. Screens: 1, 4, 5, 6. On screen: "v3: 14% and 17% below; the first of 8 policies tested to meet them" (1); "0.566" (4) and "0.532" (5); "−12% [−16%, −9%] (point)" (4); "v3 met both, the first and only one" (6).
>
> **2.** Daily LEAR, described as the strongest benchmark: a linear model refitted daily. It scores 0.658 on point error and 0.639 on interval error. Every score is measured against a similar-day naive forecast, which scores 1.000. v3 is also compared with v2, which scores 0.644 and 0.616. Screens: 1, 4, 5, 6.
>
> **3.** Evidence class: development evidence, chosen after the fact. It is a backtest on 10,747 historical hours across five periods, one of them the 2022 crisis. v3 has had no held-out test and no live run. The 14% and 17% against LEAR are single numbers with no uncertainty shown. The v3–v2 comparisons have paired 95% confidence intervals; both exclude zero, and every test period favours v3. In the 2022 crisis alone the point-error gain's interval crosses zero. Screens: 1, 4, 7, 8, 9, 10. On screen: "development evidence, not a test on new data" and "the distances are point comparisons" (1); "a development diagnostic, not a product qualification" (4).
>
> **4.** It runs v1, the released LightGBM model that forecasts nine quantiles, with calibrated 50/80/95% prediction intervals, in the browser, replaying past held-out days. It isn't v3 because research versions aren't released one at a time; only the final model replaces the released one, after a one-shot test and a live run. Screens: 1, 2, 11, 14, 17. On screen: "The demo runs the released model, v1" and "only the final model, after its one-shot test and live run, replaces the released one" (2).
>
> **5.** Calibration experiment (not adopted): "Recalibration alone was not enough: the model itself had to adapt" (3). Model comparison study (not adopted): "No policy met the criteria; the study informed v2's blend of two LEAR forecasts" (3). Losing arms: normalized LEAR on its own, "targets: not met" (4); v2's pooled-interval control, "only the interval score improved" (13). Not yet tried: "Planned, not evaluated" (16).
>
> **Earliest screen for questions 1–4:** screen 2.

## Not used

No person read the page for this check; the standard makes a human cold read optional (§17, D7).
No real Safari, iPhone or screen reader was used (§10).
