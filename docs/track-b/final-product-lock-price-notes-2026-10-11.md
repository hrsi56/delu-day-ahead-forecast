# Final product — lock-price decision: notes for the final stage

**Status: notes, not a plan of record.** Nothing here is ratified, binding or scheduled. The
anchor (`capstone_v21.md`) and PUBLISH_RULES are unchanged by it.

**Origin.** Another Orchestrator session drafted these ideas on 2026-10-10 as an anchor revision
(v21-r13, PUBLISH_RULES 1.5) on the branch `codex/final-product-price-lock-plan`. On 2026-10-11
the Owner decided not to put them into the anchor now: there is no urgency, and doing it under
pressure invites mistakes. The ideas are kept here, to be taken up when the final product
(CP-17 to CP-19) and the final publication are planned.

**The full draft is preserved** in `.local/artifacts/codex-r13-preserved-2026-10-11/`:

- `r13-tracked.patch`, which applies cleanly to `7ff6a50`;
- copies of every changed file and the draft amendment record;
- the drafting session's validation record;
- `SHA256SUMS`.

The source-check files it cites are in `/Users/djourno/Downloads/PJM-extension-planning/`, a
location the Owner chose. The specific prices observed in that check stay in the preserved draft,
not in this note.

## 1. The idea

Each day the live product forecasts tomorrow and also recommends a **maximum lock price**:
"Lock only at or below X EUR/MWh". It later compares that decision with real market quotes and the
actual outcome. It shows **forecast error separately from cumulative simulated economic value**.

It is a portfolio demonstration, with three limits:

- no real trades, broker or retail contract;
- no paid service;
- the existing insight graphs stay.

**Why it is worth doing.** Forecast accuracy alone does not answer whether to lock or wait. A real
delayed quote alone does not show that a strategy works. Together they show the forecast's value
for a decision. The difference between forecast error and economic value is also a good interview
answer, deferred from the drafting session.

## 2. The economic use case

- **Exposure.** A flat 1 MW consumption in DE-LU on the next delivery day: Q = 23, 24 or 25 MWh,
  by the day's actual hours.
- **Instrument.** The matching **EEX German Power Base Day Future**: one contract for that exact
  date, identified by its contract reference and ISIN. Never a week, weekend, month or another
  date because it happens to have a quote.
- **Scope limits.** No load shifting, storage, partial hedge or position building. Each day is an
  independent all-or-none simulated hedge.
- **Floating reference Y.** The delivery day's load-weighted day-ahead price, under the
  contract's settlement definition, from the native market intervals. Reconcile the official
  final futures settlement with a reconstructed day-ahead average before claiming they are equal.
- **The cost convention:**
  - `C_wait = Q·Y + K_wait`;
  - `C_lock(f) = Q·f + K_lock`;
  - `saving = C_wait − C_lock(f)` when locked, and zero for a valid wait.

  The K terms hold only each alternative's frozen incremental costs. A financial hedge plus
  floating purchase gives an equivalent fixed cost; it is not a retail price at the futures ask.
- **Labels.** These are simulated avoided costs, not trading profits or a return on capital. A day
  that cannot be evaluated is null, never a zero.

## 3. The decision rule

- **The daily aggregate needs its own distribution.** Hourly quantiles do not add up to a
  quantile of the daily sum. Averaging hourly p50s is not a daily median, and averaging hourly
  lower bounds is not a daily bound. The method needs its own causal calibration, for example a
  daily-residual calibration with a window and a minimum support.
- **The threshold.** With `V = Y + (K_wait − K_lock)/Q`, a target probability α and a safety
  margin m, `X = sup{ f : P(V − f ≥ m | information at issue) ≥ α }`. X may be negative; round
  down to the tick.
- **Two different probabilities.** The probability that defines X is not the same as the
  probability of saving at a given ask, `p_save(f) = P(C_wait > C_lock(f))`. Display them
  separately. Neither means "the point price is correct".
- **One conservative fixed policy, frozen before testing.** α, m, costs, slippage and quote-age
  rules, the calibration window and minimum support are set on development data. The drafting
  session's illustrative 75% and 2 EUR/MWh were not approved. A visitor's risk or price control is
  a labelled counterfactual and never changes the issued record.
- **Abstain honestly.** Without adequate calibration, show `insufficient_calibration` and keep the
  price forecast.

## 4. The simulated decision and its comparisons

- **The order rule.** The issued X becomes one hypothetical standing limit order for the
  permitted window. The first eligible ask at or below X fills, if its quantity covers one
  contract.
  - No hindsight best price, no bid, mid or last-trade substitution, no second entry.
  - No qualifying ask in the window means wait.
- **Distinct no-decision states:** quote gaps, late issuance, a wrong contract and missing
  calibration. None of them counts as a successful lock.
- **Baselines,** on the same dates, load, quotes, window and costs:
  1. always float, the main reference;
  2. always lock at the first eligible ask;
  3. a similar-day naive forecast, under the same information and risk rule.

  Perfect foresight may be shown only as a labelled, unattainable bound.
- **Comparison rules.** Paired populations with counts, never different subsets unnamed.
  Net-value, drawdown and uncertainty definitions are frozen before outcomes.

## 5. Timing and calendar: an open problem

**The draft assumed a fixed morning clock.** Inputs would cut off at 09:30 Berlin time, issue at
10:50, and consider quotes from 10:55 to 11:55, all before the auction. The decision must
genuinely precede both the auction and the quotes it is judged against.

**The Owner's objection, 2026-10-11:** the daily pipeline will run on GitHub automation, which
cannot guarantee a specific time. Free Actions schedules can be delayed or skipped, and this
project already recorded "do not rely on a free Actions schedule for a hard deadline". So a fixed
issue time cannot be promised.

**Options to weigh at the final stage, none decided:**

- record the actual issue time, and judge the decision only against quotes after it;
- fix a latest useful issue time, and abstain when the run is later;
- run the issuing job somewhere that can keep a clock.

**Two further constraints:**

- **The information clock.** An earlier issue time means less information than the research
  origin (D−1 11:00 UTC), for example an earlier GFS run. The model that faces 4.7T should be
  trained and selected at the information set it will actually have.
- **The calendar.** Forecasts run all seven days, but contracts do not. Sunday and Monday day
  contracts can last trade on Friday, and a weekend forecast cannot use a Friday quote after the
  fact. Show `market_closed` or `no_eligible_window` rather than a simulated fill.

## 6. The quote source

**The candidate.** Deutsche Börse's free, delayed EEX pre-trade files, identified through EEX's
official product and contract metadata.

**The one-day check on 2026-10-09 and 10, recorded in the draft, found:**

- **Access:** no payment and no API key.
- **Delay and retention:** a documented 15-minute delay. Minute files are kept only until midnight
  of the next business day, so **there is no historical archive**.
- **The contract:** the matching day contract was found, and the whole proposed morning window
  was downloaded: 66 minute files, 59 with ask updates. A minute without an update does not prove
  an empty book.
- **Rate limit:** a four-worker burst got HTTP 429. Serial requests at least 2.2 seconds apart
  worked. That is an observation, not a published limit.

**What follows:**

- **No archive means evaluation only on collected days.** Economic results exist only for dates
  whose quotes were collected as they happened. A replay of past months cannot test the decision
  policy. Either the live period is long enough, or collection starts early. Collection could
  start early, for example sealed and unread until evaluation.
- **Free access is not a licence to redistribute.** The rights to show raw or derived quote data
  publicly must be admitted before anything is published. The repository and the site are
  public.
- **One day proves little.** It says nothing about winter, DST, liquidity, fills, rollover or
  cancellations.

## 7. The daily evidence ledger

One row per delivery date, even when no trade was possible. It holds:

- **Identity and timing:**
  - the policy, model and daily artifact identities;
  - the input and label cutoffs, issue and delivery times;
  - the daily aggregate's distribution and calibration identity.
- **The contract:** Q and profile, the contract ID, ISIN and delivery interval, and the calendar
  and settlement versions.
- **The policy and the decision:** the frozen α, m, costs, window, X, quote rule and fallback; the
  decision and its reason.
- **The quote:** its event, publication and receipt times, price and size, sequence and hashes;
  the selected event and the assumed fill.
- **The outcome and its scores:** the outcome with its revision history, Y, the forecast error,
  the policy and baseline costs, and the gross and net savings.

Issued forecasts and decisions are immutable. Reconciliation is versioned with as-of dates. Gaps
are shown, never filled as zeros. Development replay, protected test and prospective issuance stay
separate evidence classes.

## 8. Presentation

**The product panel** gains a decision strip:

- tomorrow's named daily aggregate forecast;
- Q, X, the issue time and the calibration support;
- the decision and freshness state;
- "Lock only at or below X". X is never presented as an offer.

**A "Lock-price decision" view,** after Forecast and before Validation, explains the chronology:
cutoff → fit → issued threshold → eligible quote → delayed receipt → outcome. It shows the
contract, the selected ask and its times, and the simulation assumptions.

**The required graphs,** all from the same ledger on the report and the Space:

1. issued forecast against outcome, with signed and absolute errors, kept apart from economics;
2. daily and cumulative net simulated savings and losses in EUR against always-float, with the
   paired always-lock and naive comparisons, the zero line, negative periods and counts;
3. reliability of the saving probability, with bins, resolved counts and support, and
   "insufficient evidence" until enough decisions resolve;
4. all-date coverage and action reasons: lock, wait, market closed, no eligible window, quote
   gap, failed or late fit, calibration shortfall, pending outcome;
5. sensitivity to costs, margin, entry constraints and forecast error, from frozen scenarios;
6. an audit table: stored against recomputed daily costs, ending in match or fail.

**Where it goes in the report:** economic graphs in Business insights, error evidence in Product
results.

**Wording:** "simulated net savings/losses", never "profit" or a return percentage without a real
denominator.

## 9. Acceptance and checks

**Acceptance is honest, reproducible operation, not profit.** A losing policy is reported as
losing. Ninety live dates do not mean 90 trades: the smaller eligible economic sample is reported
on its own.

**Negative controls the draft listed:**

- future-outcome or quote leakage, and backdated issuance;
- the wrong day or product, calendar closures, DST, zero and negative prices;
- quote gaps against no-update minutes, and stale, cancelled or undersized asks;
- ties and cost rounding;
- calibration shortfall, failed retraining, and late or revised outcomes;
- counterfeit zero savings and doubled hedge cashflows.

Every row, baseline and cumulative value is recomputed independently from the served ledger.

## 10. Open questions for the final stage

1. **Timing:** how a GitHub-automated pipeline issues a decision that verifiably precedes the
   quotes it is judged against (§5).
2. **The information clock:** at which information set to select and test the final model.
3. **Rights:** admitting public display of raw or derived EEX quote data, or showing only what
   is admitted.
4. **The quote archive:** whether to start a sealed collector early, so the economic part can be
   evaluated on enough dates.
5. **The numbers:** the daily-aggregate calibration method, α, m, costs, quote age, and the
   minimum support.
6. **Settlement:** reconciling the official EEX final settlement with the reconstructed day-ahead
   average.
7. **Resources:** compute, disk, retry and retention ceilings, at zero cost.

## 11. Small corrections the draft also carried

These are independent of the lock-price idea and were not applied:

- **The final-product Space plan's gap G7** still says unattended daily publication has no
  authority. The Owner granted it on 2026-09-30 in `AGENTS.md`'s standing exception.
- **The v3 plan handoff** still calls a business use case optional ("if any"). This idea would
  settle it if adopted.
