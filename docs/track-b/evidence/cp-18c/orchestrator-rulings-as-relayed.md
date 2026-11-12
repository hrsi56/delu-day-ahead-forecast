# The Orchestrator's rulings during CP-18c, as relayed to the Lead

The Orchestrator relayed these to the CP-18c Lead by session message during the round, under decision 27 and logged
for the Owner's ratification. They are copied here verbatim, so the Integration review can check the candidate against
them; the Lead did not author them.

## O29 (2026-11-05)

> Orchestrator, for your Space's claims: I've made ruling O29 (decision 27), which binds this round's wording.
> - **Decision 28 moves decision 21's timing.** A1 replaces v1 as the product now, at CP-18c's activation, before 4.7T,
>   with the status "final candidate · pending 4.7T".
> - **Decision 21's fail branch stands:** on a failed or inconclusive 4.7T, v1 is the product again.
> - **The Space and the report document one product, A1** (§16.1's one identity). v1 is "the last released
>   generation", the historical demo at `/history/`.
>
> The basis is decision 28's own words, "ובהקפאה של הדמו צריך להיות לנו מוצר עובד לייב" ("in place of the frozen demo
> we should have a working live product"). It prevails over decision 21's earlier timing. Cite O29 in your return.

## O30, O31, O32 (2026-11-05)

> Rulings that bind this round (decision 27, logged for the Owner). They answer his questions of tonight: he wants A1
> live now, with yesterday's forecast, the next day's, and per-day error charts with the full breakdown.
>
> - **O29** (sent earlier): A1 is the product now, "final candidate · pending 4.7T". On a failed or inconclusive 4.7T,
>   v1 is the product again. One product identity across the Space and the report.
> - **O30, the public name:** "v6 · DDNN-2 alone", the newest generation after v5. The frozen records keep "A1", so the
>   served identity may say "v6 (A1 in the frozen records)". Use it in every live claim and view. It replaces
>   "A1 · DDNN-2 alone".
> - **O31, the first live day:** the earliest day inside decision 23's three-day lookback before the current target
>   day. Carry the store to that day, so the first run issues up to three catch-up days and then the target day. Each
>   uses only inputs published before its own cutoff, by §24.13's availability rule, and a day that cannot be shown so
>   is not issued, with its cause. From day one, the panel and the Forecast view then show earlier issued forecasts
>   against published prices, as well as tomorrow's.
> - **O32, per-day error charts in Validation** for every issued day: the daily MAE and interval score of the live
>   record, "prospective evaluation in progress", beside the development period's per-day errors. They sit with A9's
>   full breakdown: coverage with width per band, the similar-day naive as the reference, the counts, and the "Matches
>   the stored value" row. The live and development windows are never pooled. No percentage-correct and no confidence
>   wording.

## O33 (2026-11-05)

> Orchestrator, ruling O33 (decision 27), at the Owner's request. It adds to O32's Validation charts. Fix it now, before
> any live score exists.
>
> - **A cumulative chart for the live record:**
>   - the running mean daily MAE and interval score of the issued days;
>   - the paired difference against the similar-day naive;
>   - each with its 95% interval, drawn as a band that narrows as scored days accrue.
> - **The interval method** is 4.7T's registered dependence treatment: the protocol's §6, CP-26's paired,
>   non-circular, moving-block studentized bootstrap with 7-day blocks, as CP-28 landed it. It runs through the frozen
>   code, never a new estimator.
>   - **The minimum:** the interval appears from 14 scored days, two blocks. Before that, the running mean is shown
>     alone, with "interval from 14 scored days". Record the minimum in the return.
> - **Wording:**
>   - "95% interval of the mean daily error over n scored days";
>   - never "confidence", never a percentage-correct;
>   - never presented as 4.7T or as a test result. It is "prospective evaluation in progress".
> - **Kept apart from 4.7T:** the live record never pools with development, and never with 4.7T's own windows.

## O35 (2026-11-06), on the Lead's question

> Orchestrator: approved as an allowed-paths amendment, ruling O35 (decision 27). You may add
> `tests/cp18a/test_dry_run.py`, for that one added line only. The throwaway seed clone drops `live/` before
> `seed-store`.
>
> Conditions:
> 1. Check first that no freeze manifest, `PINS` or other evidence binds that file's bytes, and say so in the return.
> 2. Name the line, and the parallel changes in `src/cp18/forced.py` and `daily.yml`'s dry run, in the return's
>    disclosures.
> 3. `pytest -m stress` passes with it.
>
> Nothing else outside your paths is covered.

The Lead's question was to add, after the seed clone's `config core.hooksPath` line,
`sh('git', '-C', str(seed), 'rm', '-r', '-q', '--ignore-unmatch', 'live')`.

## Instructions of 2026-11-12 (after the weekly pause)

> **The live record has a gap.** Nothing ran from 2026-11-08 through today, so those days are not issued. Record their
> cause in the store, as the pipeline does, and disclose the gap in the return.
> **Keep the record going until the runner takes over:** acquire each day's inputs before its cutoff (D−1 11:00
> Berlin), so the next day can be issued … Run this from your session as a background job on this Mac, within the
> brief. Do not install `launchd`.
> **Priority:** reach the final candidate, the Integration Critic and the return quickly. The daily operation only
> starts unattended after my LAND.

The expected state was also updated on 2026-11-05: the Owner entered the three repository secrets
(`ENTSOE_API_TOKEN`, `HF_TOKEN`, `DAGSHUB_USER_TOKEN`) in `hrsi56/delu-day-ahead-forecast`; "No real secret goes to any
runner in this round, and the first runner dispatch is the Orchestrator's, after the LAND."
