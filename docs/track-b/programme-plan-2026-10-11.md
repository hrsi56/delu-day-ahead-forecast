# Programme plan after CP-24 — 2026-10-11

**Status: the order was approved by the Owner on 2026-10-11.** It is a planning aid, not an anchor.
The research anchor (`capstone_v21.md`) still governs. Each stage below opens only through its own
anchor section, brief and Owner gates.

**Origin.** The Owner's task list of 2026-10-11 and the Orchestrator's comments, with two rulings
the Owner made the same day:

- v5 is published before any new data enters a model;
- all the data is collected before anything is retrained or re-evaluated.

**The short path, chosen by the Owner on 2026-10-12.** After stages 3 and 4 reported, the
Orchestrator set out the remaining cost and the likely gain. The full plan would take about
three to four months, and new sources were expected to add 0–3% at most, with a real chance of
nothing. The Owner chose to continue **without new data sources**:

- **Stage 5 (CP-25) narrows** to our own gaps: the inventory, GFS for 2022-09-29 to 2023-03-24,
  and a check of every existing input against the new issue time (D−1 11:00 Europe/Berlin).
- **Stage 7 (CP-27) is dropped.** Stage 3's research stays as a documented finding, and its
  shortlist is a possible extension after the final product, not part of this programme.
- **Stage 8 (CP-28) runs on CP-26's stored forecasts,** without the union arm. Whether it runs at
  all is confirmed after CP-26.
- **Unchanged:** the issue time; the vintage standard; stage 6's full-calendar re-baseline; the
  freeze, 4.7T, the live stages and the final publication.

**The windows move, Owner, 2026-10-12.** While drafting the anchor amendment, the Orchestrator found
that `data/snapshot.parquet` already holds prices to 2026-09-06. v1 used 2026-04-09 to 2026-06-07
for its calibration and 2026-06-09 to 2026-09-06 for its published one-shot holdout
(`data/partitions.json`, `docs/cp2-model-report.md` §4). The fixed 4.7T window (2026-04-08 to
2026-07-06) therefore fell on exposed data. The Owner decided:

- **4.7T moves to 2026-09-07 to 2026-12-05,** the first 90 days after the snapshot's cutoff;
- **2026-04-08 to 2026-09-06 joins development,** so stage 6 evaluates through 2026-09-06;
- **the replay (stage 10) is withdrawn;** the live trial after 4.7T does its job on real days.

The expected time to the end is about two and a half to three months, most of it the live trial.

## The red line

Data dated after **2026-09-06** stays closed until 4.7T opens it (moved from 2026-04-07 on
2026-10-12; see the top). That covers three things:

- **Data on disk.** Every downloader refuses rows after the open boundary, in code. Only the 4.7T
  gate moves the boundary, and only to the end of that gate's window.
- **Reading.** No agent reads reports, news or analyses of market events after 2026-09-06. That
  is knowledge leakage too.
- **The window itself.** 4.7T's window (stage 9) is fixed now, before anyone looks, and is never
  extended after a result.

The red line governs development. The final product, once live, trains on all the data available
to it, to forecast days that have not happened yet.

## The order at a glance

| # | Stage | Kind | Starts after | Runs alongside |
|---|---|---|---|---|
| 1 | ✅ The codex r13: kept as notes, not merged | Orchestrator | done | — |
| 2 | ✅ Publish v5 (PRES-4): closed 2026-10-11 | Publication | done | — |
| 3 | ✅ Search for new data sources: report received 2026-10-12 | Research, no evaluation | done | — |
| 4 | Design the evaluation protocol: memo received and decided 2026-10-12; the anchor section next | Research and anchor | now | 5 |
| 5 | Collect our own data gaps and check the issue time (CP-25; narrowed 2026-10-12) | Checkpoint | 4 ratified | — |
| 6 | Re-baseline v1–v5 on the existing features, as the control arm (CP-26) | Checkpoint | 2 published, 4 ratified, 5 landed | — |
| 7 | ~~Admission tests for the new sources (CP-27)~~: dropped by the short path, 2026-10-12 | — | — | — |
| 8 | 4.8: choose the winner on stored forecasts (CP-28; confirmed after 6) | Checkpoint | 6 | — |
| 9 | Freeze one candidate (CP-17) and run 4.7T on 2026-09-07 to 2026-12-05 | Checkpoint and test | 8 | security hardening (11a) |
| 10 | ~~Replay daily retraining~~: withdrawn 2026-10-12 | — | — | — |
| 11 | Security hardening, controlled live trial, site activation (CP-18 → CP-19) | Live | 10 | — |
| 12 | Final publication and CV | Publication | 11 | — |

**Two rules set the order.**

- **v5 first.** v5 is the last generation on the current information and the current five folds.
  It is published before any model is fitted on new or newly completed data, so that the chain
  v1 → v5 stays comparable. Searching, protocol design and downloading may run before the
  publication; fitting on the new data may not.
- **All the data before any training.** One data checkpoint collects the existing gaps and every
  shortlisted new source in a single pass: one boundary guard, one manifest, one licence check.
  Nothing is retrained until it has landed.

**Why the re-baseline (6) still comes before the new-source tests (7)** (the rationale as approved;
stage 7 is dropped by the short path):

- **It is the control arm.** A source's test asks whether v5 with it beats v5 without it, under the
  new protocol. The "without" run is the re-baseline.
- **Attribution.** Changing the data and the evaluation method at once would hide which one moved
  the result.
- **It answers its own question:** does v5 hold across every eligible day? If it does not, 4.8
  starts from a different point.

Stages 6 and 7 run on the same collected data, so nothing is downloaded twice.

## Stage 1 — The codex r13: done, kept as notes

**What it was.** On 2026-10-11 the Orchestrator reviewed the uncommitted v21-r13 / PUBLISH_RULES 1.5
draft: the final product's daily lock-price decision and its simulated economic record.

**What the Owner decided.** It stays out of the anchor for now: there is no urgency, and amending
under pressure invites mistakes. Its ideas and open questions are kept in the
[lock-price notes](final-product-lock-price-notes-2026-10-11.md), for the final stage. Those open
questions include the issue time under GitHub automation, quote display rights, and the lack of a
quote archive.

**What remains.** The draft is preserved in `.local/artifacts/codex-r13-preserved-2026-10-11/`. The
branch and its worktree are deleted. Publication briefs keep pinning PUBLISH_RULES 1.4.

## Stage 2 — Publish v5 (PRES-4): done

**Closed 2026-10-11** ([closure record](pres-4-closure-2026-10-11.md)). v5 is on the report, the
README and MLflow, with CP-22 and CP-23 as branch cards; the Space stays on v1. The Owner landed
`aebebc1` (`land/pres-4`, `evidence/pres-4`) and pushed it, and every public check passed. The
independent post-deployment review was waived, with the rule change carried to stage 4. The page
has 3,733 bytes left under the budget, so the next generation's publication needs a compaction or
budget decision first (A-PRES4-5).

The name PRES-4 was reserved for CP-22's replacement plan, which never ran. That plan stays an
unexecuted record.

**Decided by the Owner on 2026-10-11,** departing from the recommendations below on D1:

- **D1, no compaction:** the v2 and v3 sections are not edited.
- **D2, yes:** CP-22 and CP-23 go in briefly and point by point, as "tested, not adopted", and
  into the comparison chart where there is something to add.
- **D3, built first:** `scripts/publication_receipt.py` and `scripts/prerelease.py`, on 2026-10-11.
- **D4, as recommended.**
- **The Space stays on v1** until the final product's freeze, so A-PRES3-7 waits for that
  deployment.

**Two risks the brief carries:**

- **The page budget:** 2.0 MB, against about 1.91 MB now. The brief requires fitting without
  touching v2 and v3, or stopping with the measured size.
- **A-PRES3-1 changes `scripts/mlflow_export.py`,** which CP-23's tests bind. It needs the Owner's
  `AMENDED_BY_…` treatment, authorized in the brief.

The decisions as they were put to the Owner, with the Orchestrator's recommendations:

| # | Decision | Recommendation |
|---|---|---|
| D1 | Compaction of the one-page report for a fifth generation (PUBLISH_RULES §14) | Full sections for v4 and v5; v2–v3 collapsed into a lineage table |
| D2 | Publish CP-22 and CP-23 as "tested, not adopted" | Yes, in the same publication |
| D3 | Automation items 6 (post-deploy receipt) and 7 (pre-review check runner) | Build both before the brief, as one small task |
| D4 | PRES-3's open advisories | A-PRES3-1 (the MLflow description) in this publication; A-PRES3-7 (GFS attribution) only if the Space is redeployed; A-PRES3-5 deferred, since it needs a suspension |

**What the publication must say plainly:**

- v5 was adopted on 17% of days, with no October–December and one winter;
- DDNN-2 alone is descriptive only;
- the evidence is post-selection development evidence, and v1 remains the product;
- a full re-evaluation follows.

**Route:** the brief, a Lead, one fresh independent review, the Owner's publication authority.

## Stage 3 — Search for new data sources: done

**Received 2026-10-12** ([research report](data-source-research-2026-10-11.md), with the
[Elia coverage counts](research/stage3-elia-coverage-metadata-2026-10-11.json)). 78 products
were assessed against the five filters, and none passed all five without conditions. The
Orchestrator checked the decisive claims against the primary pages: Elia's 11:00 field and its
CC BY 4.0 licence, ENTSO-E's reuse list, and the TIGGE licence. No market value after 2026-04-07
appears in the report.

- **Wind and solar:** our own forecast from GFS (4.4V), as planned. No free German archive of
  forecasts published before the origin, kept as issued, was found.
- **CP-25's conditional list, in order:**
  1. Elia's Belgian `dayahead11hforecast` wind field (CC BY 4.0, published at 11:00 Brussels);
  2. the neighbours' D−1 and older prices, zone by zone (SMARD, Energinet; CC BY 4.0);
  3. the neighbours' load forecasts, ENTSO-E 6.1.B and 6.1.C;
  4. the pre-auction capacities, ENTSO-E 11.1 and the flow-based parameters 11.1.B (Core from
     2022-06-09 only);
  5. optionally, TIGGE's ECMWF ensembles (CC BY 4.0, 48 hours late, registration needed);
  6. the ECB deposit-facility rate and the lagged USD/EUR reference rate.
- **Held:** RTE's D−2 French load, GIE storage and LNG, generation outages, EIA Brent and EUA
  auctions. **Rejected,** with reasons in the report: every free fuel route found, the volatility
  indices, Euribor, FRED/ALFRED, direct JAO, the German TSOs' forecasts and Open-Meteo's archives.
- **The Owner's decisions, 2026-10-12:**
  - **No enquiry or registration for now.** The report's nine Owner questions stay open.
  - **The vintage standard** in stage 4 below, which decides how each product enters.

The stage as planned on 2026-10-11 follows; the issued brief is SHA-256 `d3ee57cd…`.

Desk research only: no download into the project and no evaluation. Its output is a shortlist,
which stage 5 collects.

**The candidates:**

- **Energy prices:** gas (TTF), carbon (EUA) and coal. They are the strongest candidates, but often
  licence-restricted, and the repository is public.
- **Interest rates and a fear index.** Worth testing, with a low prior for hourly prices.
- **Neighbouring zones and cross-border links.** Neighbours' day-D prices are set in the same
  coupled auction, so they are leakage. Only D−1 and older prices qualify, plus capacities and
  flow-based parameters published before the auction.
- **The "+2" idea:** an early forecast that already covers day D. It qualifies only if it was
  published before our forecast time.
- **External wind and solar forecasts, in place of building 4.4V ourselves.** This needs an archive
  of forecasts as they were issued, not actuals or reanalysis, with real publication times. By
  regulation, ENTSO-E's day-ahead wind and solar forecast is due only by 18:00 the day before,
  after the 12:00 auction. If no admissible archive exists, 4.4V is built from GFS as planned.

**The starting point** is the existing scope note in `progress.md` (Notes, [Data admission
research]), with CP-15's five admission checks (`reports/cp15/feasibility/structural_inputs.md`).
CP-15 already found no free, redistributable, origin-correct TTF series from 2019.

**Every shortlisted source passes four filters:**

- it is free;
- it is redistributable;
- its publication time precedes the issue deadline;
- its data runs to 2026-04-07 only.

**Owner gate:** the research brief.

## Stage 4 — Design the evaluation protocol

**First, an external research run.** It reviews best practice for evaluating day-ahead price
forecasts: rolling recalibration, window length, season and regime coverage, and the tests
(Diebold–Mariano, Giacomini–White). Then the Orchestrator writes the protocol as an anchor
section, and an independent plan critic reviews it.

**What the protocol fixes in advance:**

- **The days:** every eligible day, about 1,926 from 2020-12-29 to 2026-04-07 (2,078 to 2026-09-06
  since the window move of 2026-10-12), with the never-scored
  days reported apart as a diagnostic and the old folds kept as the historical record.
- **The training rule:** the refit cadence should match production (daily, under §16). The
  window length, 728 days or expanding, is chosen before the run.
- **The metrics, the tests and the seasonal and regime breakdowns.**
- **The policies:** v1 to v5, with DDNN-2 alone as descriptive.
- **The data-admission rule for stage 7,** with control for testing many sources on the same days.
- **The walk-forward rule for stage 8:** a combining model learns only from members' forecasts for
  earlier days that they never trained on.
- **The compute ceilings.**

**The research memo, received 2026-10-12:**
[stage-4-methodology-memo-2026-10-12.md](stage-4-methodology-memo-2026-10-12.md), from the brief
`fae94cc6…`. It recommends the protocol's values: daily refits on a 728-day window; v5 as the
research control; p50 MAE and WIS, averaged over hours within each day and then with equal weight
per day; paired 14-day blocks with 10,000 replicates; more than 0.5% improvement plus 2% year and
season non-inferiority, under Holm; an early admission slice (2020-12-29 to 2024-12-31) and a later
confirmation slice (2025-01-01 to 2026-04-07) for new sources; and +1, +6 and +24-hour delay checks
for tier 2. The agent disclosed that one search showed it an excerpt from after 2026-04-07, which it
discarded; nothing in the memo comes from that period.

- **A correction to the brief.** The Orchestrator's brief said DDNN-2 alone is never an eligible
  candidate. That holds for CP-26 only: stage 8 makes it a CP-28 arm. The memo followed the brief,
  and the anchor section follows this plan.

**The Owner's decisions on the memo, 2026-10-12:**

1. **The issue time becomes D−1 11:00 Europe/Berlin,** one hour before the 12:00 auction gate,
   all year (10:00 UTC in winter, 09:00 UTC in summer). Inputs must be published strictly before
   it. It replaces D−1 11:00 UTC, which in summer fell after the gate and after the results were
   public, from CP-25 on, through the anchor amendment. Earlier records keep 11:00 UTC. CP-25
   checks every input against the new time.
2. **CP-28 pre-registers the plan's arms,** each specified in full before CP-26's results:
   DDNN-2 alone; equal weights; one learned global weight set; per-block weights (three hour
   blocks, shrunk toward the global weights); and the NumPy meta-learner on regime features.
3. **CP-27 may admit several sources.** Each of up to eight packages passes the early and later
   gates on its own, under Holm across all eight; CP-28 adds one pre-registered arm, v5 plus every
   admitted source.

The memo's other values are the default for the anchor section, which the Owner ratifies.

**The vintage standard, decided by the Owner on 2026-10-12** after stage 3 found that almost no
source keeps its first-published values:

1. **Original vintages with publication timestamps** enter the main evaluation.
2. **Preserved original values, with availability reconstructed from documented schedules,** may
   enter, with disclosure and delay-sensitivity checks.
3. **Revised historical values without original vintages** are excluded from the main evaluation
   and tested separately.

Reconstructing the availability time is acceptable; substituting retrospectively corrected values
is not. Each product is verified individually, and licensing remains mandatory. The protocol turns
this into its admission rule, and CP-25 records each product's tier.

**Owner gates:** the research brief; the anchor section with its suspension.

**The same suspension carries one publication-rule change,** chosen by the Owner on 2026-10-11 at
PRES-4's closure: require the independent post-deployment review only when the served bytes differ
from the independently reviewed bytes, or a public check fails without a passing retry. PRES-2,
PRES-3 and PRES-4 each waived it on that basis.

## Stage 5 — Collect all the data (CP-25)

**The gap was our choice, not the source's.** The days were available; no fold needed them.

- **5a. Inventory.** Every input series the generations use, from 2019-01-01 to 2026-04-07 (to
  2026-09-06 since the window move of 2026-10-12). Record
  every gap with its cause: our extraction or the source.
- **5b. Fill the existing gaps,** starting with GFS for 2022-09-29 to 2023-03-24.
- **5c. ~~Collect every source stage 3 shortlisted~~:** dropped by the short path (2026-10-12).
- **5e. The issue time.** Check every existing input against D−1 11:00 Europe/Berlin, strictly
  before, with its vintage tier recorded.
- **The rules for 5b and 5c:**
  - The boundary guard is in every downloader.
  - Each value enters as it was available at forecast time. Revised series, such as actual load
    and generation, enter only in the version known on the day, or only as lags.
  - Each product's vintage tier is recorded under the Owner's standard (stage 4): original
    vintages, preserved values with reconstructed availability, or revised history, which stays
    out of the main evaluation.
  - Each source has its provenance and licence recorded.
  - Credentials follow `AGENTS.md`: no value in a log, URL or error message, with tests for it.
- **5d. GFS availability at forecast time, historically.** Reconstruct each run's arrival from the
  archive's timestamps, against the issue deadline. The live half is measured in stage 11.
- **Output:** one frozen, complete snapshot with a manifest and a coverage report, covering the
  existing inputs and the new candidates.

**Owner gates:** the anchor section with its suspension; the retrieval approval (free sources, $0);
the brief; the LAND.

## Stage 6 — Re-baseline v1–v5 on all eligible days (CP-26)

Run every generation under stage 4's protocol, on stage 5's snapshot, **with the existing
features only.** Under the short path no new source follows.

**Output:**

- the full-coverage results of the existing generations: the new baseline (under the short path
  there is no stage 7 to control for);
- every member's out-of-sample forecast for every eligible day, which feeds stage 8.

**The rule:** whatever these results show, they are reported, not tuned against. If v5 does not
hold, the record says so.

## Stage 7 — Admission tests for the new sources (CP-27): dropped

**Dropped by the Owner's short path, 2026-10-12.** The plan as approved on 2026-10-11 tested each
collected candidate against stage 6's control, under stage 4's admission rule, on the same
snapshot.

## Stage 8 — 4.8: choose the winner (CP-28)

**The candidates:**

- DDNN-2 alone;
- fixed blends and per-block weights;
- stacking with a NumPy meta-learner.

All are fitted with stage 7's admitted data. **Decided 2026-10-12** (stage 4): DDNN-2 alone; equal
weights; one learned global weight set; per-block weights; the NumPy meta-learner on regime
features; and one union arm, v5 plus every source CP-27 admits. **Under the short path
(2026-10-12)** the union arm falls away, every arm learns from CP-26's stored member forecasts, and
whether CP-28 runs is confirmed after CP-26.

**The rules:**

- The combining model learns walk-forward, only from earlier days' out-of-sample member forecasts.
- The selection rule is fixed before anyone looks.
- No arm is required to win, and DDNN-2 alone may be the best model.
- The winner is post-selection; 4.7T carries the protection.

## Stage 9 — Freeze one candidate (CP-17) and run 4.7T

**Fixed before the test opens:**

- the candidate;
- its retraining rule during the test;
- the reference model;
- the pass conditions;
- the lock-price policy, if the final product adopts the
  [lock-price idea](final-product-lock-price-notes-2026-10-11.md);
- what happens on failure. The runner-up never moves up, and v1 stays the product.

**The window:** 2026-09-07 to 2026-12-05, 90 days (moved on 2026-10-12 from 2026-04-08 to
2026-07-06, which v1 had used). The boundary moves to 2026-12-05 only, and the test is opened once.
Its results are never used for tuning or for choosing another candidate.

## Stage 10 — Replay daily retraining on the next 90 days: withdrawn

**Withdrawn by the Owner, 2026-10-12.** Its window, 2026-07-07 to 2026-10-04, fell mostly inside
v1's holdout, and the live trial after 4.7T exercises daily retraining on real days. The plan as
approved follows.

**The window:** 2026-07-07 to 2026-10-04, 90 days, opened only after stage 9 passes.

**What it does:** the frozen candidate retrains on its pre-registered cadence and forecasts each
day in turn, from data as it was available at the time.

**What a replay proves:** the statistical behaviour of an updating model on fresh data, in days
rather than months.

**What it cannot prove:**

- that GFS and the prices really arrive in time;
- outages, the scheduler, credentials and the site itself, since archived data is complete and
  sometimes revised;
- the lock-price decisions. The free quote feed keeps no archive, so they can only be evaluated on
  days whose quotes were collected as they happened (notes §6).

**Anchor change:** this replaces the statistical part of CP-18's 90 live days, so it needs an
amendment.

## Stage 11 — Security hardening, controlled live trial and site activation (CP-18 → CP-19)

- **11a. Security hardening.** The daily pipeline handles credentials every day. It can be prepared
  during stages 9–10.
- **11b. The live trial.** It proves operations: GFS and price arrival against the issue time,
  failure handling, credentials, and the site updating. The Orchestrator recommends at least four
  weeks, so that real delays and outages occur; the length is the Owner's decision. If the
  lock-price idea is adopted, its economic evaluation needs enough collected quote days too.
- **11c. CP-19:** the final activation and publication decision.

## Stage 12 — Final publication and CV

The final product, its report, and the CV surfaces, under the publication rules in force then.

## The Owner's decision points, in order

1. Stage 1: done. r13 is kept as notes, and the codex branch is deleted.
2. Stage 2: done. D1–D4 above, the LAND and the push on 2026-10-11.
3. Stages 3 and 4: stage 3 done, with the vintage standard and no enquiries (2026-10-12); stage
   4's memo decided the same day (issue time, CP-28 arms, several sources); then the anchor
   section and its ratification.
4. The short path (2026-10-12): done.
5. Stage 5: the anchor section, the retrieval approval and the LAND.
6. Stages 6 and 8: each checkpoint's anchor section and LAND; stage 8 is confirmed after stage 6.
7. Stage 9: the frozen candidate and every pre-registered term, before the test opens.
8. ~~Stage 10: the anchor change to CP-18~~ (the replay is withdrawn).
9. Stage 11: the live trial's length, and the final activation.

**Saving suspensions.** One anchor amendment can fix the programme order, the red line and both
post-boundary windows at once, and the same suspension can carry the conditional public-review rule
(stage 4). Each later stage then needs only its own section.
