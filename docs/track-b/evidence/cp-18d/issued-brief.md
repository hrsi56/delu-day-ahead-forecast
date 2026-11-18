# Track B Checkpoint Brief — CP-18d (no missing day: v6 with the late load forecast, an earlier acquisition, and the live product's follow-ups)

*Issued by the Orchestrator on 2026-11-15, Asia/Jerusalem, under the Owner's decisions 27, 28, 29 and 31.*

## Target
- Repository: DE-LU day-ahead forecasting, `/Users/djourno/Downloads/PJM` (origin
  `hrsi56/delu-day-ahead-forecast`, public). The checkpoint runs locally, in the Lead's own worktree. It may also run
  dry runs in CP-18a's public scratch repository `hrsi56/delu-pipeline-dryrun`.
- Authorized checkpoint: CP-18d, exactly one. No other checkpoint runs beside it.
- **Why.** On the live product's first runner day, GitHub's scheduler started none of the acquisition jobs before
  D's cutoff, and started a later job about 5 hours late. The Orchestrator dispatched the day by hand (CP-18c's
  landing record, "The runner's first day"). Under decision 22 a day whose load forecast was not retrieved before
  the cutoff is not issued. The Owner ruled that no day goes missing for this reason (decision 31).
- **What it does:**
  1. **Decision 31, the late load forecast.** When D's day-ahead load forecast cannot be shown to precede D's cutoff,
     v6 (A1 in the frozen records) still issues D, with the load forecast retrieved after the cutoff, labelled, and
     reported separately in the evaluation. Nothing frozen changes.
  2. **An earlier acquisition.** The acquisition starts early enough, and waits inside its job, so that a scheduler
     delay like the first day's still retrieves the forecast before the cutoff. The schedule is set from the
     Orchestrator's experiment, `.github/workflows/schedule-probe.yml`.
  3. **The claim over a moved `main`** (O47). A push to `main` during a run no longer discards that run's records.
  4. **The live product's follow-ups:** its wording (O45 item 8; PRES-5's A12 review) and the runner's artifact.
- **What follows it:** the Orchestrator's LAND and the first runner day under the change; 4.7T, no earlier than
  2026-12-04, exactly as registered; the publication of 4.7T's result.
- Ratified plan anchor: `capstone_v21.md`, revision v21-r20, SHA-256 `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`.
  - **The bar** is quoted below: §24.13's "The publication time (decision 22)", "The catch-up (decision 23)" and
    "For CP-18"; §24.14's "What stays exactly as registered"; PUBLISH_RULES 1.5 A9.
  - **Decision 31 supersedes one sentence of §24.13** for the load forecast only: "A live day whose inputs cannot be
    shown this way is not issued". The anchor records it at its next revision. Every other sentence of §24.13
    stands, including "There is no 'late' status and no 'late' label" and "No public wording claims that a forecast
    was published before the auction, or before its outcome".
  - **PUBLISH_RULES** `docs/PUBLISH_RULES.md`, revision 1.5, SHA-256
    `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`.
- **The frozen policy, which this round runs and never changes:** CP-17c's freeze, policy identity
  `720fc581be6206eba8ed303e689e63c09272a189564090a547d93fc9e7db62dc`. `refreeze verify` on its manifest prints
  `verified` at the final candidate.
- **The landed live product, this round's input:** CP-18c, `docs/track-b/cp-18c-landing-2026-11-13.md`
  (`cfd20128224ef1cbf3e7fa409ba93bb297177d72edafbfa16856a1853ad9205d`), `land/cp-18c` = `f55c4eae`, with its section "The runner's first day".
- **The Owner's decisions:** 1–19 bound by the frozen copies; 20–21 (`owner-decisions-2026-10-29.md`); 22–25
  (`owner-decisions-2026-10-30.md`); 26–27 (`progress.md`); 28 (`docs/track-b/owner-decisions-2026-11-05.md`,
  `4daa5617e51208b0994eac925d51078ea43481e6fb1017aec3576c0936490215`); 29–31 (`docs/track-b/owner-decisions-2026-11-15.md`, `ad1beb9f9e7ee235195db96d63d8c3684a5d664f29d51622c866538620c7a323`).
- **The Orchestrator's rulings that bind this round** (decision 27, logged for the Owner): O13 (the status wording),
  O14, O16 (visual choices are the Owner's), O17, O18 (the issue-time labels), O31–O33 (the live record's charts),
  O41 and O47 (the first runner day).
- **Execution inputs.** Verify each hash before relying on it:

  | Input | Path | SHA-256 |
  |---|---|---|
  | CP-18c's landing record (the runner's first day; O40–O42, O47) | `docs/track-b/cp-18c-landing-2026-11-13.md` | `cfd20128224ef1cbf3e7fa409ba93bb297177d72edafbfa16856a1853ad9205d` |
  | The Owner's decisions 29–31 | `docs/track-b/owner-decisions-2026-11-15.md` | `ad1beb9f9e7ee235195db96d63d8c3684a5d664f29d51622c866538620c7a323` |
  | Decision 28 | `docs/track-b/owner-decisions-2026-11-05.md` | `4daa5617e51208b0994eac925d51078ea43481e6fb1017aec3576c0936490215` |
  | CP-17c's freeze manifest (policy identity 720fc581…) | `docs/track-b/evidence/cp-17c/freeze-manifest.json` | `ceab430989d0050a2e8c0cf80f9fa22d0929a9dacfde69fc6c98127605752532` |
  | PRES-5's landing record (O45 item 8) | `docs/track-b/pres-5-landing-2026-11-14.md` | `6a9a5499074c6866bc18e6012c6007f83a081d8182c9a95d084203c0768c5f36` |
  | PRES-5's A12 review (the Space's wording) | `docs/track-b/pres-5-a12-postdeploy-review-2026-11-14.md` | `7632db7c249ff6501be1690701898f90188fd382255d1d13cdb72d65f558aba0` |
  | PRES-6's landing record | `docs/track-b/pres-6-landing-2026-11-15.md` | `415e2e7c89a47018546b91ac4bd46f40622440fdbc049b5b39b782196bbc198b` |
  | The daily workflow | `.github/workflows/daily.yml` | `2168e42c74eb46cd7c8f03a9e096ce55b9191e8075a2f72d5e5eadd9ef06a128` |
  | The schedule probe (the Orchestrator's) | `.github/workflows/schedule-probe.yml` | `49900d509d83c134b4995956696a26c61df5b47d24694f266e579db6a9dea615` |
  | The acquisition | `src/cp18/acquire.py` | `be5eb840a8102d428724e5407617031bf1f3bcad6e41fb64e28e22fa987b9db7` |
  | The claim | `src/cp18/claim.py` | `2993c060f6a79342cf2123d1abe52e12afcd7734b1c90ad6033fe4fab2e95dc2` |
  | The causes | `src/cp18/causes.py` | `aa02af7f66484b0acf6cbb11b7f3d4cf1ff1b22c102fe75fe2011556b7b709c0` |
  | The live inputs | `src/cp18/live_inputs.py` | `1200ca524699e986f1d7152940f35944fdda1e267a4cbdf0887599ab33e29e88` |
  | The availability rule | `src/cp18/live/availability.py` | `352c40aa1e0ff614f32bb5de930dd1e0f7cf7387b8ac41226cd1477ec38e7649` |
  | The Space's claims | `src/cp18/live_claims.py` | `5917d5a428b263fb54e23974139432b0d3e6a779d9158508c39181900e2fe3ed` |

## Orchestrator-reported expected state
- **Branch / commit:** `main` = `origin/main` at the commit that records this brief's issue, a descendant of PRES-6's
  closure through the runner's data-only commits. The issue commit changes only `progress.md`.
  - **`main` moves during this round.** The live product's daily runner pushes data-only commits to `main`, by the
    author `delu-daily`, touching only `live/`. Never write under `live/`. The packet's LAND commands assume a moved
    `main`.
  - **The schedule probe** `.github/workflows/schedule-probe.yml` is on `main` from PRES-6's closure (2026-11-15). It
    runs hourly at :07 from 00:07 to 09:07 UTC, one job on `ubuntu-latest` and one on `macos-26`, and its run names
    carry the cron line. It is the Orchestrator's.
  - **Tags:** every landed checkpoint's `land/` and `evidence/` tags are pushed, except `evidence/cp-26` = `ca20331`,
    which is **local-only and never pushed**. The rulesets refuse moving or deleting a `land/`, `evidence/` or
    `archive/` tag, and refuse pushing a `gauntlet/*` branch.
  - **Branches and worktrees:** `main` only. No other checkpoint runs beside this one.
- **Working tree:** the primary checkout is on `main` and clean apart from ignored material.
  - **The Orchestrator uses it.** Never switch its branch, and never write a tracked file in it. Your only writes
    there are under `.local/artifacts/cp-18d/`, `.local/tmp/cp-18d/` and the worktrees under `.local/worktrees/cp-18d/`.
  - **The canonical brief** is `.local/artifacts/cp-18d/issued-brief.md`. Package that file byte for byte.
  - **A Finder `.DS_Store`** may sit in ignored folders such as `space-product/`. It is local-only and fails
    `tests/cp18c/test_space_live.py::test_the_page_sources_type_neither_the_old_name_nor_a_bare_issued_at` in the
    primary checkout only. A clean worktree does not have it.
- **The live product:**
  - the daily workflow `.github/workflows/daily.yml`, on the `macos-26` runner, scheduled (repository variable
    `DAILY_SCHEDULE` = `enabled`): acquisitions at 07:40, 08:20 and 09:20 UTC, the run at 10:40 UTC, a retry and
    keep-alive at 13:40 UTC. D's cutoff is D−1 10:00 UTC in winter. The Owner entered the repository secrets;
    agents never handle their values;
  - on 2026-11-14 the scheduler fired none of the acquisitions or the run, and fired the 13:40 job at 18:50 UTC. The
    Orchestrator dispatched the acquisition and the run by hand, and checks each day;
  - the live store and the archive are on `main` under `live/`; `live/inputs/days/` holds each day's retrievals with
    their times. On 2026-11-06, -07, -08, -14 and -15 the load forecast first appeared between 09:03 and 09:17 UTC;
  - the Space `Yarden-Viktor/delu-day-ahead-forecast` is published by each run. Of the live record's first 13 days
    (2026-11-03 to 2026-11-15, `live/store/ledger.jsonl`), it issued 2026-11-06, -07, -08, -14 and -15. It did not
    issue 2026-11-09 (no run within the lookback) or the seven others (inputs that cannot be shown to precede the
    cutoff: 2026-11-03 to -05 and 2026-11-10 to -13). Decision 31 addresses that cause.
- **No local fallback** (decision 29). The `launchd` file CP-18c wrote stays uninstalled.
- **What already exists for this round:** CP-18a–c's pipeline (`src/cp18/`), its tests (`tests/cp18a/`–`cp18c/`),
  the Space's sources (`space-product/`, `scripts/build_product_space.py`), and the scratch repository
  `hrsi56/delu-pipeline-dryrun` with fake credentials.
- **Credentials:** none are needed locally. The scratch repository holds fake ones only.
- Verify this yourself before relying on it, and report any material mismatch.

## Observable outcome
When this checkpoint closes, after the Orchestrator's LAND, a delivery day is never missing because its acquisition
ran late. Each day v6 issues says whether its load forecast was retrieved before the cutoff or after it, and the
evaluation keeps the two apart.

1. **The late load forecast (decision 31).**
   - **When it applies:** D's load forecast is not shown before D's cutoff, by the existing rule
     (`cp18.acquire`, `cp18.live`): the acquisition did not run, found nothing before the cutoff, or failed.
   - **What happens:** a later acquisition or run retrieves D's load forecast after the cutoff and archives it like
     any retrieval, with its retrieval time, its request and its body. v6 issues D through the frozen chain
     (`cp17.daily`, `cp17.issue.decide`) with that copy. The chain, its fallbacks and the frozen package are
     unchanged.
   - **Every other input** keeps decision 22's rule: judged by its publication time against D's cutoff. If an input
     other than the load forecast cannot be shown to precede the cutoff, the day keeps its existing cause and
     fallback.
   - **Within decision 23's lookback,** a day whose acquisition failed is issued by a later run with the late copy.
     A day is still never issued twice, and no issued forecast is replaced.
   - **If no copy can be retrieved at all** (the source is down), the day stays open inside the lookback, and its
     cause is recorded as now.
   - **The label.** The issued record, the store, the bundle and every Space surface that shows the day name its
     input class: all inputs before the cutoff, or "load forecast fetched after the cutoff", with that copy's
     retrieval time (UTC). The wording names the input's retrieval. It is never "late" and never "timely" (§24.13).
   - **The evaluation (O32, O33).** The live record's scores, charts and cumulative intervals report the days whose
     inputs all precede the cutoff on their own, and all issued days beside them, each stating its count. The
     Lead proposes the exact display, and the Orchestrator rules (O16 for visual choices).
   - **CP-19's count** (§24.13): a late-copy day is issued, and counted as issued with its label.
2. **An earlier acquisition (decision 31's experiment).**
   - **The measurement.** From `schedule-probe.yml`'s runs (`gh run list --workflow schedule-probe.yml`, read-only):
     for each cron hour, the scheduler's delay (the run's creation time against its cron time) and the `macos-26`
     queue (the job's start against the run's creation), over every probe day available at the measurement, at least
     three. Committed as `reports/cp18d/schedule-probe.json`, with its method.
   - **The schedule.** `daily.yml`'s acquisition starts early enough that the measured delays still reach D's load
     forecast before the cutoff, and waits inside its job until the forecast is published or the cutoff's margin
     arrives (`cp18.acquire`'s polling, its `--window-hours`). Each job stays inside GitHub's 6-hour job limit. More
     than one acquisition start may be scheduled; two acquisitions never write the same day twice.
   - **Unchanged:** the acquisition is still the only retrieval that can show D's load forecast before the cutoff. The
     run's schedule may move if the measurement shows a reason, with the reason stated.
   - **GitHub's rule that disables an idle scheduled workflow** stays handled.
3. **The claim over a moved `main` (O47).** A run whose records step finds `main` moved by commits that touch none of
   the run's own paths re-applies its records on the new `main` and pushes, instead of discarding them.
   - It never overwrites a commit it did not make, never force-pushes, and never writes a path outside `live/`.
   - A moved `main` that touches the run's own paths still refuses, as now.
   - A test reproduces O47's case: an unrelated commit pushed during the records step, and the records kept.
4. **The live product's follow-ups.**
   - **The two "A1" sentences** in the Space's claims (O45 item 8): the product's name is "v6 · DDNN-2 alone"; "A1"
     appears only as "A1 in the frozen records". The unused designation sentence is removed or used.
   - **"Runs daily"** (PRES-5's A12 review): where a surface says the product runs daily, it describes the schedule,
     and the record's issued and not-issued days stay visible with their causes.
   - **v1's history page:** the host's preview tags name v1's historical demo, not v6.
   - None of these changes a number.
   - **The runner's Actions artifact** holds the Space's whole build apart from the fitted arrays it deletes on
     purpose, with the build's own record, so that a public check can verify a runner-published Space without
     assembling it (PRES-6's landing record, the Disclosures).
5. **The rehearsal.** In the scratch repository, with fake credentials only, dry runs on development days through
   2026-09-06 show, end to end:
   - a normal day, all inputs before the cutoff;
   - a missed acquisition, issued with the late copy and labelled;
   - a run whose `main` moved during its records step, records kept;
   - the earlier acquisition's schedule and in-job wait.
   No real secret goes to any runner in this round.
6. **The tests and the controls.**
   - A negative control for each rule: a late copy refused for an input other than the load forecast; a day issued
     twice refused; an issued forecast replaced refused; the label missing refused; a moved `main` touching the run's
     own paths refused.
   - CP-18c's tests stay green. Where decision 31 changes a behaviour they assert, the change is stated beside the test,
     as O36 did, and only that assertion changes.
7. **The packet's table for the Orchestrator's steps after the LAND, in order:**
   - the LAND on a moved `main` (the runner's data-only commits) and the push, outside the daily jobs;
   - GitHub's CI;
   - the first runner day under the change, and how to check its label;
   - the removal of `schedule-probe.yml` once its measurement is committed.

   Each step has its exact command and its check.

## Complete authoritative checkpoint bar
Verbatim, extracted by `scripts/bar.py bar … --at c7d33ebc --quote` from `main` at the issue.
(The excerpt is the citation. Any line number is a courtesy and is non-binding.)

**`capstone_v21.md` v21-r20 §24.13, "The publication time (decision 22)"** (the file `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`; the section 39 lines, 2762 bytes, SHA-256 `8b656f9ae608f63ef630fa12f02416f894d99ebd82aa4222d37193af61311f47`):

> #### The publication time (decision 22)
>
> - **The information cutoff is unchanged:** D−1 11:00 Europe/Berlin, strictly before (§24.4).
>   - A run may happen at any time after the cutoff.
>   - Its payload holds only inputs published before the cutoff. So a later run issues the same forecast,
>     under the condition below.
> - **"Before the outcome"** in the frozen rules means without access to D's outcome, under the target-day
>   embargo (§24.4). It does not mean wall-clock time.
> - **Availability is judged by publication time against D's own cutoff, never by the run time.** The
>   tier register and the Owner's tier, margin and GFS rulings (§24.5) apply unchanged. This covers each
>   input and the GFS-availability flag (§24.12, decision 11).
>   - **For the live pipeline, CP-18 makes this verifiable** in one of three ways:
>     - each day's inputs are retrieved and archived by the cutoff;
>     - each input is taken from a source that preserves its vintage;
>     - for an input the tier register admits with reconstructed availability (tier 2), its documented
>       schedule.
>   - **A live day whose inputs cannot be shown this way is not issued,** and its cause is recorded.
>   - **4.7T's window keeps its registered vintage terms** (the protocol's §3, "Vintages").
> - **A delivery day is issued or not issued.** There is no "late" status and no "late" label.
> - **What stays recorded:**
>   - each issuance's actual run time, in its lineage (§16.2);
>   - the date of the last training, which the product's panel states.
> - **No public wording claims** that a forecast was published before the auction, or before its outcome.
> - **What this supersedes:**
>   - **§24.4's sentence** "The live product publishes its forecast before 12:00 local. CP-18 fixes the
>     schedule, its deadline and its failure rule; a late forecast is recorded as late." CP-18 fixes the
>     schedule and the failure rule. There is no deadline.
>   - **§16.2's "numeric origin/deadlines".** CP-18's brief fixes the origin and the cutoff, and no
>     deadline.
>   - **§16.4's CP-19 row,** where "count real timely forecasts and failures" becomes "count issued and
>     not-issued delivery days". CP-19's at least 90 consecutive delivery days count every day, issued or
>     not issued.
> - **§16.2's rule stands:** "Do not ... backfill a late forecast as timely". No forecast is labelled timely.
>   A catch-up issuance carries its own run time and relabels nothing.
> - **`AGENTS.md`'s daily-update exception needs no change.** It reads: "A failed or late day is published
>   as failed or stale, never skipped silently or backfilled as timely." Under this section:
>   - a day that is not issued is shown as not issued;
>   - the panel shows the date of its last training;
>   - nothing is labelled timely.

**`capstone_v21.md` v21-r20 §24.13, "The catch-up (decision 23)"** (the file `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`; the section 17 lines, 1101 bytes, SHA-256 `3403ca7bb739f7a816bf0cac277df14fdcab15570a2748e77c71515cd7edc4e0`):

> #### The catch-up (decision 23)
>
> - **Each run** issues, in chronological order:
>   - the missed delivery days within a lookback of three days before the current target day;
>   - then the current target day.
> - **At most four issuances run in one run.**
> - **A day older than the lookback is never issued.** It stays not issued, so the backlog never exceeds
>   three days and every run reaches the current day.
> - **Each catch-up** uses only inputs published before that day's own cutoff, as judged above, and never
>   replaces an issued forecast.
> - **The bound in time.**
>   - Each fit keeps its 15-minute ceiling.
>   - Decision 23's record says "a run takes at most about an hour". That counts one fit per issuance.
>   - With A1 and three shadows per issuance, the ceilings bound a four-issuance run, with its canary, at
>     about 4¼ hours. That is inside GitHub's 6-hour job limit, by GitHub's published terms.
>   - Measured on `macos-26`, one issuance took 270–284 s, and four with the canary about 21 minutes.
> - **CP-18 may shorten the lookback** after measuring the runtime. It may not remove the bound.

**`capstone_v21.md` v21-r20 §24.13, "For CP-18"** (the file `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`; the section 30 lines, 1991 bytes, SHA-256 `9121e5576a19b96fb40e5062af8fd7329e243a6fdd97bbf8f22bdca3e709750a`):

> #### For CP-18
>
> These add to §24.12's list "For CP-18", as amended above:
> - **the unattended pipeline on the `macos-26` runner.** It calls `cp17.daily` once per issuance, with the
>   checks above and decision 23's catch-up. It has a schedule and a failure rule, and no deadline;
> - **the public runner class's timing,** measured in the product's repository on development days before
>   the first live issuance, against criterion 5's ceilings;
> - **the cause of each day that is not issued,** in the record. The causes are:
>   - a failed issuance by the chain;
>   - a failed H2 check;
>   - a live day's inputs that cannot be shown to precede its cutoff;
>   - no run within the lookback;
>   - S_14's state not in place;
> - **one issuance per delivery day across the runner and the local fallback.** The issued record is the
>   single source, and no issued forecast is replaced;
> - **how the states are carried** from 4.7T's last window day to the first live day;
> - **a live day's input availability,** made verifiable as the publication time above requires;
> - **the credentials as GitHub secrets.** The Owner enters them himself (decision 25), and agents never
>   handle their values;
> - **`AGENTS.md`'s conditions on the runner:**
>   - the secret guard and the pre-push guards run on the runner's own commits and pushes;
>   - credentials are used only as stored variables inside the consuming process;
> - **public run logs.** The repository is public, so its run logs are public. Credentials, and any value
>   derived from them, are never printed;
> - **GitHub's rule that disables a scheduled workflow** after a period without repository activity. CP-18
>   shows how the pipeline stays enabled;
> - **a local fallback on the Owner's Mac,** with the same binary and the same checks;
> - **the red line on the runner.** Until CP-18's brief retires the boundary guard after 4.7T (§24.2), the
>   runner's pipeline runs only on development data through 2026-09-06 (decision 7). No scheduled run
>   retrieves later data.

**`capstone_v21.md` v21-r20 §24.14, "What stays exactly as registered"** (the file `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`; the section 16 lines, 1161 bytes, SHA-256 `0e1f357969f5bad69b4e5dbc4682631196a77b4580381b6ef887cb96b7607c84`):

> #### What stays exactly as registered
>
> - **A1's freeze.** CP-17c's policy identity `720fc581be6206eba8ed303e689e63c09272a189564090a547d93fc9e7db62dc`,
>   its manifest and the frozen package stay unchanged. `refreeze verify` guards them, and the live pipeline
>   calls the package without editing it.
> - **4.7T, in every registered term** (§24.12, §24.13):
>   - the window, delivery days 2026-09-07 to 2026-12-05;
>   - the candidate, the comparators, the scores, the pass conditions, the margins and the failure rules;
>   - the vintage terms (the protocol's §3);
>   - the machine (the Owner's Mac, no cloud) and the H2 checks before its first issuance;
>   - the calendar: it opens no earlier than 2026-12-04, after the price for 2026-12-05 is published;
>   - the audit, the Owner's declaration and his retrieval approval.
> - **4.7T issues its window itself.** Its issuance starts from the freeze-origin state, runs on the Owner's Mac
>   under its terms, and keeps its own store. Nothing the live product issues is 4.7T's issuance or score.
> - **No registered term changes from here until 4.7T is scored.** A proposal to change one returns 4.7T to the
>   Owner as BLOCKED.

**`docs/PUBLISH_RULES.md` revision 1.5 A9** (the file `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`; the section 14 lines, 833 bytes, SHA-256 `c264126b70356802d2ca526386d9aa54a6219b2974a2aef0e517147ff18bf4bc`):

> ### A9 — The final-product Space
>
> **Observed need:** on 2026-09-30 the Owner found the Space uninformative for a daily product.
> The Owner asked for a daily-trained tool with a "Train it yourself" button, today and tomorrow
> panels, and views for data, features, validation, explainability, reliability, the forecast and
> limitations. The existing rules specified only the demo's states, its startup metadata and the
> panel's fields.
>
> **Addition, conditional on A8's trigger:** §7.3.
>
> **Check:** the §7.3 acceptance record, on the candidate and on the public Space.
> **Maintenance:** views render from the daily bundle and the shared claim layer, with no second
> claim source and no hand-typed numbers. The daily pipeline's cost is bounded by the CP-18 brief.
> This amendment adds no model, research, schedule or publication authority.

**Further items,** which bind this candidate as well:

1. **4.7T stays exactly as registered** (§24.14). No 4.7T issuance, store, score or audit runs in this round. Nothing
   the live product issues is 4.7T's.
2. **A1 stays frozen.** No file of the frozen package, its manifest, `src/cp17*` or the freeze's evidence changes.
   `refreeze verify` prints `verified` at the final candidate.
3. **The red line.** The live pipeline is exempt (r20 §24.14). No research number, chart or choice uses data after
   2026-09-06. The rehearsal uses development days only.
4. **Decision 22's other rules stand:** the cutoff, the judgement by publication time for every other input, the run
   time recorded in the lineage, no deadline.
5. **Critic and return:** `docs/track-b/gauntlet-templates.md` §§2–3.

Map every applicable item to evidence. The extract below does not narrow this bar.

## Task-specific supporting extract
- **The live product runs every day during this round,** from `main`, on the runner. Never push to the product
  repository, never write under `live/`, and never dispatch or cancel its workflows. The Orchestrator owns them.
- **The probe is the Orchestrator's.** Read its runs; do not edit, dispatch or remove it.
- **The ceilings:** 12 local machine-hours, summed over workers' wall time, at most 4 concurrent workers, CPU only;
  GitHub runner minutes in the scratch repository as the rehearsal needs. Keep a ledger, and stop before a ceiling.
- **Presentation.** Visual choices are the Owner's (O16). Build to the Space's existing tokens and components.

## Applicable constraints
- **Homebrew's `node` stays pinned and installed.**
- **Credentials:** none are needed locally. Never print, log or echo a credential value. The scratch repository uses
  fake credentials only. Export `MLFLOW_DISABLE_TELEMETRY=true` and `DO_NOT_TRACK=1`.
- **Allowed paths:**
  - `src/cp18/` and `tests/cp18a/`, `tests/cp18b/`, `tests/cp18c/` (only as item 6 allows), `tests/cp18d/`;
  - `.github/workflows/daily.yml`;
  - `space-product/` and `scripts/build_product_space.py`;
  - `reports/cp18d/` and `docs/track-b/evidence/cp-18d/`.

  No anchor, governance file, `docs/PUBLISH_RULES.md`, `progress.md`, frozen record, `src/cp17*`, `live/`,
  `.github/workflows/schedule-probe.yml`, the report (`docs/index.html`, `README.md`) or the exposure ledger.
- **Before editing a tracked file,** check that no earlier evidence binds its bytes. That includes:
  - `src/cp26/harness.py`'s `PINS`;
  - `tests/pres5_landed_code.py`;
  - every freeze manifest's governance pins;
  - CP-18c's evidence (`reports/cp18c/`, `docs/track-b/evidence/cp-18c/`).
- **Tools:**
  1. run `scripts/gauntlet.py start cp-18d` first, from the primary checkout;
  2. create the worktree with
     `git -C /Users/djourno/Downloads/PJM worktree add -b gauntlet/cp-18d .local/worktrees/cp-18d/lead main`;
  3. run the independent check through `critic-open`, `critic-brief` and `critic-close`. **The first line of the
     Critic's launch assignment** forbids opening the Claude memory directory;
  4. check the return with `scripts/gauntlet.py return`.
- **Memory:** do not open or edit the files in the Claude memory directory
  (`~/.claude/projects/-Users-djourno-Downloads-PJM/memory/`).
- **Owner-facing Git commands** must be non-interactive.

## Timebox
About 16 active hours from orientation to the terminal return.

## Owner-only actions already authorized
- **CP-18d's execution** under decisions 27, 28 and 31 and this brief, on `gauntlet/cp-18d`. The Orchestrator delivers
  this brief under the Owner's grant, and that delivery is the grant.
- **Dry runs in the scratch repository** `hrsi56/delu-pipeline-dryrun`, with fake credentials only, after the
  value-based secret scan of what is pushed there.
- **No action on the product.** No push, landing, merge or tag on the product repository, no Space upload, no write to
  the live store or `live/`, no workflow dispatch on the product repository, no governance edit. Those that apply
  are the Orchestrator's, after the return.

## Stop and return
- **First commit.** The first commit copies the canonical brief byte for byte to
  `docs/track-b/evidence/cp-18d/issued-brief.md`.
- **Questions.** If the brief is unclear or wrong, ask the Orchestrator, or stop at the conflict. The anchor, the
  Owner's decisions and PUBLISH_RULES prevail over this brief.
- **The return.** Return exactly one of PASS / BLOCKED / INCOMPLETE, using templates §3, with both terminal SHAs and
  the verdict-only delta, checked with `scripts/gauntlet.py return`.
  - Its "Open risk or exact owner action" section gives the packet's steps and every open item, with a proposed
    ruling for each.
  - Name the machine-hours used.
- Leave your worktree and branch for the LAND.
