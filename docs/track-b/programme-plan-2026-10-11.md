# Programme plan after CP-24 — 2026-10-11

**Status: the order was approved by the Owner on 2026-10-11.** It is a planning aid, not an anchor.
The research anchor (`capstone_v21.md`) still governs. Each stage below opens only through its own
anchor section, brief and Owner gates.

**Origin.** The Owner's task list of 2026-10-11 and the Orchestrator's comments, with two rulings
the Owner made the same day:

- v5 is published before any new data enters a model;
- all the data is collected before anything is retrained or re-evaluated.

## The red line

Data dated after **2026-04-07** stays closed until 4.7T opens it. That covers three things:

- **Data on disk.** Every downloader refuses rows after the open boundary, in code. Only the 4.7T
  gate moves the boundary, and only to the end of that gate's window.
- **Reading.** No agent reads reports, news or analyses of market events after 2026-04-07. That
  is knowledge leakage too.
- **The windows themselves.** Both post-boundary windows (stages 9 and 10) are fixed now, before
  anyone looks, and are never extended after a result.

The red line governs development. The final product, once live, trains on all the data available
to it, to forecast days that have not happened yet.

## The order at a glance

| # | Stage | Kind | Starts after | Runs alongside |
|---|---|---|---|---|
| 1 | ✅ The codex r13: kept as notes, not merged | Orchestrator | done | — |
| 2 | Publish v5 (PRES-4) | Publication | the Owner's four decisions | 3, 4, 5 |
| 3 | Search for new data sources | Research, no evaluation | now | 2, 4 |
| 4 | Design the evaluation protocol | Research and anchor | now | 2, 3, 5 |
| 5 | Collect all the data: existing gaps and every shortlisted new source (CP-25) | Checkpoint | 3 | 2, 4 |
| 6 | Re-baseline v1–v5 on the existing features, as the control arm (CP-26) | Checkpoint | 2 published, 4 ratified, 5 landed | — |
| 7 | Admission tests for the new sources against that control (CP-27) | Checkpoint | 6 | — |
| 8 | 4.8: choose the winner (CP-28) | Checkpoint | 7 | — |
| 9 | Freeze one candidate (CP-17) and run 4.7T | Checkpoint and test | 8 | security hardening (11a) |
| 10 | Replay daily retraining on the next 90 days | Test | 9 passed | 11a |
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

**Why the re-baseline (6) still comes before the new-source tests (7):**

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

## Stage 2 — Publish v5 (PRES-4)

The name PRES-4 was reserved for CP-22's replacement plan, which never ran. That plan stays an
unexecuted record.

**The Owner's decisions before the brief** (binding, v21-r10 §22), with the Orchestrator's
recommendations:

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

## Stage 3 — Search for new data sources

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

- **The days:** every eligible day, about 1,926 from 2020-12-29 to 2026-04-07, with the never-scored
  days reported apart as a diagnostic and the old folds kept as the historical record.
- **The training rule:** the refit cadence should match production (daily, under §16). The
  window length, 728 days or expanding, is chosen before the run.
- **The metrics, the tests and the seasonal and regime breakdowns.**
- **The policies:** v1 to v5, with DDNN-2 alone as descriptive.
- **The data-admission rule for stage 7,** with control for testing many sources on the same days.
- **The walk-forward rule for stage 8:** a combining model learns only from members' forecasts for
  earlier days that they never trained on.
- **The compute ceilings.**

**Owner gates:** the research brief; the anchor section with its suspension.

## Stage 5 — Collect all the data (CP-25)

**The gap was our choice, not the source's.** The days were available; no fold needed them.

- **5a. Inventory.** Every input series the generations use, from 2019-01-01 to 2026-04-07. Record
  every gap with its cause: our extraction or the source.
- **5b. Fill the existing gaps,** starting with GFS for 2022-09-29 to 2023-03-24.
- **5c. Collect every source stage 3 shortlisted,** over the same period.
- **The rules for 5b and 5c:**
  - The boundary guard is in every downloader.
  - Each value enters as it was available at forecast time. Revised series, such as actual load
    and generation, enter only in the version known on the day, or only as lags.
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
features only.** The new sources wait for stage 7.

**Output:**

- the full-coverage results of the existing generations: the new baseline, and stage 7's control
  arm;
- every member's out-of-sample forecast for every eligible day, which feeds stage 8.

**The rule:** whatever these results show, they are reported, not tuned against. If v5 does not
hold, the record says so.

## Stage 7 — Admission tests for the new sources (CP-27)

Each collected candidate is tested against stage 6's control, under stage 4's admission rule, on
the same snapshot.

## Stage 8 — 4.8: choose the winner (CP-28)

**The candidates:**

- DDNN-2 alone;
- fixed blends and per-block weights;
- stacking with a NumPy meta-learner.

All are fitted with stage 7's admitted data.

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

**The window:** 2026-04-08 to 2026-07-06, 90 days. The boundary moves to 2026-07-06 only, and the
test is opened once. Its results are never used for tuning or for choosing another candidate.

## Stage 10 — Replay daily retraining on the next 90 days

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
2. Stage 2: D1–D4 above, then the publication's own gates.
3. Stages 3 and 4: the two research briefs, then the protocol's ratification.
4. Stage 5: the anchor section, the retrieval approval and the LAND.
5. Stages 6, 7 and 8: each checkpoint's anchor section and LAND.
6. Stage 9: the frozen candidate and every pre-registered term, before the test opens.
7. Stage 10: the anchor change to CP-18.
8. Stage 11: the live trial's length, and the final activation.

**Saving suspensions.** One anchor amendment can fix the programme order, the red line and both
post-boundary windows at once. Each later stage then needs only its own section.
