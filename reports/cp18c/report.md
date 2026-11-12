# CP-18c — the live product's activation, before 4.7T

**The live product runs.** Under the Owner's decision 28 and anchor v21-r20 §24.14, CP-18c retired the boundary guard
for the live pipeline only, downloaded the live pipeline's data from 2026-09-07 through the present, seeded the live
store at the freeze origin and carried it to 2026-11-03, and issued the first live delivery days with the frozen A1 on
the Owner's Mac (the issuing host's local fallback). It built the dated bundle and the final-product Space from the
live record, and made the daily operation ready to run unattended. Nothing under `src/cp17/` or `src/cp17c/` changed;
`refreeze verify` on CP-17c's manifest prints `verified`. Nothing live is 4.7T's, and 4.7T stays exactly as registered.

The public name is "v6 · DDNN-2 alone" (the Orchestrator's O30); the frozen records keep "A1", and this report uses
"A1" where it means the frozen identity.

## Results

| Item (brief) | Result |
|---|---|
| 1. The guard, live only | `cp18.boundary`: inside `boundary.live()` each delivery day is admitted through the present (the next day whose cutoff is ahead) and judged against its own cutoff; outside it, every check is `cp25.guard`'s. `src/cp25/guard.py` is bound by CP-17c's freeze manifest, so it was not edited: the route is in `src/cp18/`. Research paths still refuse any row after 2026-09-06 (`tests/cp18c/test_guard_two_sides.py`) |
| 2. All the data, through the present | `live/inputs/days/2026-09-07 … 2026-11-07/`: SMARD prices, ENTSO-E A65 load forecasts, GFS (AWS listing, index, byte ranges, decoded by CP-20's decoder with ecCodes 2.49.0). Each response with URL, retrieval time, size, SHA-256 and publication evidence |
| 3. The live store | Genesis at 2026-09-06 (`seed-store --genesis …freeze-origin-state.json:2026-09-07:2026-09-06`), carried to 2026-11-03 with decision 28 as the reason; 2026-09-07..11-02 outside, never issued |
| 4. The first live issuances | 2026-11-06, 11-07 and 11-08 issued by A1 on the Owner's Mac after the H2 gate; 2026-11-03..05 not issued, cause "a live day's inputs that cannot be shown to precede its cutoff"; the gap 2026-11-09..13 (§4) |
| 5. Outcomes and evaluation | Reconciled through `cp18.outcomes` with the live transport; each price names its archive and record (N1); the live days are the prospective window only |
| 6. The bundle and the Space | `cp18.bundle --mode live`: the gate passes (R7, the frozen identity, the native recompute), the red line on the research windows only, 20 of 20 negative controls refused. The Space from the live record (`--live`), v1 at `/history/`; the browser acceptance 590 passed, 0 failed, 1 not run |
| 7. The publication | After the Integration PASS (the return records it) |
| 8. The daily operation | §9 below |
| 9. N5, N1, N7, the bridge-day edge, the rulesets | Done (§§4, 6, 7); the rulesets stay CP-18a's written `reports/cp18a/rulesets/`, applied by the Orchestrator after the LAND |
| 10. The exposure ledger's continuation | `docs/track-b/exposure-ledger-continued.md`, entry 6, dated 2026-11-05 by the first retrieval; no market value |
| 11. Tests and controls | `tests/cp18c/` (guard sides, carry, N5, bridge-day, acquisition, running intervals, live bundle, live record, Space, workflow, fallback); `test_24` extended; CP-18b's controls refused on the live bundles |

## 1. The guard, retired for the live pipeline only

- **Why a route.** `src/cp25/guard.py` (`3648d562…`) is listed in CP-17c's freeze manifest. Editing its `BOUNDARY` would
  change the frozen package. `src/cp18/boundary.py` holds the live boundary instead, and every boundary check on the
  live pipeline's path (`cp18.plan`, `cp18.live.transport`, `archive`, `history`, `build`, `payloads`, `gfs`,
  `cp18.live_inputs`, `cp18.outcomes`) calls it.
- **Two modes.** Outside a `live()` block every check delegates to `cp25.guard`, unchanged: CP-18a's and CP-18b's dry
  runs, CP-25's downloaders, CP-17c's development builder (`cp17.tools.payloads`, which calls `cp25.guard` directly
  and refuses even inside the block) and every development report. Inside it — entered only by `cp18 run --mode
  live`, `cp18 acquire`, `cp18.live.acquire` and `cp18.bundle --mode live` — a delivery day is admitted up to the next
  day whose cutoff is still ahead, a GFS run only if initialized at or before the present, and a market request may
  not start after the present.
- **What stays.** The 2019 floor, the 00 UTC cycle, f021–f048, the AWS URL shapes and the credential refusal are
  `cp25.guard`'s own functions. Each day's own cutoff (`cp18.live.availability`), the target-day embargo and ruling
  1's scope (the stored development history only) are unchanged in either mode.

## 2. The data

- **Sources.** Prices: SMARD `chart_data` filter 4169 (the snapshot's route; tier 2, the documented schedule admits a
  later retrieval). GFS: the AWS archive, its `LastModified` listing as the vintage-preserving evidence (ruling 4).
  Load forecast: **ENTSO-E A65 (process A01), not SMARD**. SMARD's load-forecast bucket for D was created at 14:31 UTC
  on D−1 (its `meta_data.created`), after D's 10:00 UTC cutoff, so SMARD can never show D's load forecast in time.
  TSOs publish it on the Transparency Platform by D−1 10:00 local (Reg. 543/2013 Art. 6). A65 is the plan's own
  series (`data/README.md`); the 2026-09-08 snapshot used SMARD because the API was unavailable then.
- **Retrievals** (`reports/cp18c/evidence/retrievals.json`, the live archive's and the outcomes' records through
  2026-11-12): 5,010 requests, 3,138,995,845 bytes, from 2026-11-05T08:17:13Z — 3,400 GFS byte ranges (3.11 GB, kept as
  hashes and sizes only), 680 GFS listings, 680 GFS indexes, 92 ENTSO-E documents, 158 SMARD files. The committed
  `live/` is 53.9 MB (the 20 MB `k13.json` is the same blob as `reports/cp18a/dryrun/pinned/`'s); no file over 50 MB.
- **TLS.** The interpreter's own store lacks ENTSO-E's root (Sectigo R46); the live transport verifies against
  certifi's bundle, which `uv.lock` pins, and never turns verification off.
- **Availability by publication time.** 2026-11-06's load forecast was retrieved at 09:17:52Z, 2026-11-07's at
  09:07:44Z, each before its 10:00Z cutoff; the history days' load forecasts were retrieved 08:19–08:25Z on
  2026-11-05, before 2026-11-06's cutoff. 2026-11-03..05's were retrieved after their cutoffs, so those days were not
  issued. Every GFS run from 2026-09-07 to 2026-11-07 was listed before its own day's cutoff.
- **The live-input builder** runs on darwin-arm64 only (CP-18a's disclosure): the Owner's Mac here, the `macos-26`
  runner in the workflow.

## 3. The live store

`live/store/`: genesis at the freeze origin (state `1388d74d…`), the carry 2026-09-06 → 2026-11-03 (decision 28),
then the runs. `LiveStore.record_carry` gained one case: a store that has decided no day carries from its genesis
origin, and `verify()` refuses a first carry that does not start there.

## 4. The first live issuances

| Run | Host | Started (UTC) | Outcome |
|---|---|---|---|
| `local-20261105-first-live` | the Owner's Mac | 2026-11-05T21:50:49 | The H2 gate's pins check failed: `refreeze verify` looked for the issuing host's local files in the pipeline's own clone, not the project. Nothing issued; 2026-11-03..06 left open with the cause. Fixed (`cp18.__main__.pin_project`: a checkout that is not the project names it through `CP17_PROJECT_ROOT`) |
| `local-20261105-second-live` | the Owner's Mac | 2026-11-05T21:52:20 | The H2 gate passed (pins `verified`, the binary, the machine, the canary). 2026-11-03..05 not issued, their load forecasts not shown before their cutoffs; **2026-11-06 issued by A1**, issuance 21:54:19–21:57:41 (201 s), the run 321 s, peak 1.17 GB |
| `local-2026-11-07` | the Owner's Mac | 2026-11-06T10:20:02 | Acquisition 08:20Z with the load forecast at 09:07:44Z; **2026-11-07 issued by A1**, issuance 10:21:35–10:24:44 (189 s), the run 283 s |
| `local-2026-11-08` | the Owner's Mac | 2026-11-07T10:20 | The load forecast at 09:07:45Z; **2026-11-08 issued by A1** (211 s) |
| `local-2026-11-12-after-the-gap` | the Owner's Mac | 2026-11-12T13:5x | No run happened from 2026-11-07 until then (§10). 2026-11-09 closed as not issued, "no run within the lookback"; 2026-11-10..13 acquired after their cutoffs, so open, "a live day's inputs that cannot be shown to precede its cutoff"; they close with that cause when a later day is issued |

The claim (`origin`'s `main`) was a local bare repository standing in for the product repository: every commit went
through `.githooks`, nothing reached GitHub. The records are on `gauntlet/cp-18c`. The local operation continues daily
until the runner takes over (2026-11-14 to 11-18 scheduled); the records made after the final candidate sit in the local
claim, and the return's table carries them to `main` after the LAND, before the first runner dispatch.

**The evidence bundle** (`reports/cp18c/evidence/`): built from the candidate's live record as of 2026-11-12, manifest
`c0c32fe9…`, "stale" (2026-11-13 not decided yet), latest issued 2026-11-08, publishable; CP-18b's 20 negative controls
all refused; the Space built from it (first visit 572,789 bytes, 805 History files).

## 5. N5 and the bridge-day edge

- **N5.** An exception in a day's acquisition, release or build becomes that day's cause ("a live day's inputs that
  cannot be shown to precede its cutoff", with the redacted error), never an escaped run; the run's record, with its
  acquisitions, is published either way, so nothing is left uncommitted in the fallback's clone.
- **The 31-December Monday bridge-day edge** (2029, 2035) fails closed in the live builder: not built, the day not
  issued with that cause and the reason, until a later brief decides it.

## 6. The bundle

- **The live label** (the manifest's one free-text field): "v6 · DDNN-2 alone (A1 in the frozen records) · final
  candidate · pending 4.7T; the live product's own issued days from 2026-11-03, prospective evaluation in progress,
  never 4.7T's issuance or score; the development-period displays stay on days through 2026-09-06", then each day not
  issued with its cause.
- **The red line on the research windows only:** the served series and the development evaluation windows stay on
  days through 2026-09-06; a window labelled 4.7T may hold no scored day, and the prospective window no development
  day (the classes never pool).
- **N1.** A live bundle's prices each name the archive and record that served them (the first observation, or the
  revision that changed the price); a dry run's keep CP-18b's label, so its committed records reproduce byte for byte.
- **The manifest's time notation.** The first live artifact's data-refresh time is written `…Z` (the archive's form);
  the frozen manifest schema wants `…+00:00`. The manifest restates the same instant; the artifact is served as issued;
  the builder writes `+00:00` from 2026-11-07 on.
- **Controls.** CP-18b's 20 negative controls are refused on the live bundles; the recompute-mismatch control alters the
  prospective window when the rehearsal window scores no day.

## 7. The Space

`scripts/build_product_space.py --bundle <bundle> --out <dist> --live <live> --history reports/cp18c/history-v1/files`
builds it from the live record (the Space Builder's work):
- `app/live-record.json`, bound in `app/space-build.json`: each issued day's cutoff-based issue time beside its actual
  run (start, issuance start and end, host, run id) — **N7** — each day not issued with its cause, the outside range,
  and O33's running intervals;
- the wording from `cp18.live_claims` (O13, O14, O29, O30): "v6 · DDNN-2 alone", "final candidate · pending 4.7T",
  "prospective evaluation in progress"; v1 "the last released generation", historical, at `/history/`;
- O31's earlier days against published prices; O32's per-day MAE and interval score beside the development period's,
  with B0 as the reference; O33's running means with their 95% interval from 14 scored days (`cp18.running`);
- v1's deployed files, unchanged (805 files, 44,164,910 bytes, revision `0331088725fedab2f5a1ec804ae03bf960cf126f`,
  each matching the Hub's blob id), at `/history/`.

The browser acceptance (`tests/cp18c/space_acceptance.py`, `reports/cp18c/acceptance/acceptance.json`): Chromium and
WebKit, seven widths, 590 passed, 0 failed, 1 not run (WebKit's `<details>` state, as in CP-18b); zero non-local
requests; "Train it yourself" identical bit for bit in both engines.

## 8. O33's interval method

4.7T's registered dependence treatment (`cp17.tools.fresh_test`): `cp28.inference`'s moving-block studentized bootstrap,
7-day blocks, 10,000 replicates, Bartlett HAC at lag 14, stratified calendar runs; the studentized interval from its
replicate statistics. `cp28.inference.calendar_runs` admits every date through `cp25.guard`, so `cp18.running`
transcribes that one function without the admission and calls `cp28`'s own `draw_plan`, `hac_variance` and
`DrawPlan.indices`; `tests/cp18c/test_running.py` shows it bit-identical to `test_endpoint` on development dates. **The
minimum is 14 scored days** (two blocks); before it the running mean stands alone, with "interval from 14 scored days".

## 9. The daily operation

- **`daily.yml`** (the workflow Builder's work, imported):
  - **`schedule:`** — the acquisition before the cutoff at 07:40, 08:20 and 09:20 UTC (summer and winter time;
    `cp18 acquire --window-hours 3` makes one whose cutoff is far a no-op), the run after the cutoff at 10:40 UTC and a
    retry at 13:40 UTC (the claim makes a second run find nothing to issue, and record its run). The job is selected by
    `github.event.schedule`; a dispatch `mode` (`dry-run`, the default, `live`, `acquire-live`) starts any of them.
  - **The live run job:** `prepare --pinned live/pinned` (the states, Pyodide's 23 files and the official binary by
    hash), the ecCodes environment, `cp18 run --mode live --inputs live-http --remote origin`, then the bundle
    (`--arrays` from `$RESULTS/run/runs/A1-<day>-*/run-arrays.npz` before the results step deletes them, else
    `--refit`), the Space (`--live live --history reports/cp18c/history-v1/files`), the Hub publication
    (`cp18.publish --hub`, with the Hub client pinned, `huggingface_hub==0.36.2` as v1's deployment pinned it, in an
    ephemeral `uv run --with` overlay over the project's environment, which is never synced or changed), and the day's
    records through the claim.
  - **Secrets** inside the steps that use them: `ENTSOE_API_TOKEN` on the acquisition and run steps, `HF_TOKEN` on the
    publication step; the by-value scan step reads them to search the results for their values. `DAGSHUB_USER_TOKEN`
    is not used. `permissions: {}` at the top; `contents: write` only on the acquisition and run jobs (N6); the dry run
    reads. Every job has `timeout-minutes`; actions are pinned by commit SHA; one concurrency group.
  - **Staying enabled:** GitHub disables a scheduled workflow after 60 days without repository activity. Every live
    run, the acquisition included, pushes a data-only commit to `main`, and the 13:40 run doubles as the keep-alive.
  - **The dry run** keeps CP-18a's dispatch on development days; its throwaway checkout sets the committed live record
    aside before seeding its own store, so the real `live/` is never touched.
- **The rehearsal** in the public scratch repository `hrsi56/delu-pipeline-dryrun`, fake credentials only, development
  days only (`reports/cp18c/rehearsal/`): run 42221640423 (success, 689 s: genesis, one issuance, the bundle with
  `--arrays`, the Space, the local publication, the records, the GFS decode check) and run 42223428846 (success,
  291 s: the carried store, nothing to issue, the bundle by `--refit`). **0.27 of 3 job-hours.** The runner's ecCodes
  2.49.0 decoded the 2026-09-05 run equal to the archived decode, every message byte for byte.
- **The local fallback** (`python -m cp18.local run --mode live`, `acquire`): the same binary, checks and claim; it
  exports `CP17_PROJECT_ROOT` and `CP26_PROJECT_ROOT` first. Its two `launchd` agents,
  `reports/cp18c/launchd/com.delu.daily-acquire.plist` (11:10 and 11:40 Asia/Jerusalem) and `com.delu.daily-run.plist`
  (15:00), are written and tested (`plutil -lint`, the Jerusalem-to-Berlin times on every day of 2027–2028), not
  installed.
- **This round's operation** ran on the Owner's Mac from the Lead's session as background jobs, under `.local/`: each
  day's `cp18 acquire` before the cutoff, `cp18 run --mode live` after it, the bundle step and its records, against a
  local bare repository standing in for `origin`.

## 10. Disclosures

- **Usage-limit pauses.** 2026-11-05 about 06:22–08:10 and 08:52–21:44 UTC; 2026-11-06 about 00:10–07:50,
  08:00–12:50 and 13:15–17:50 UTC; then the weekly limit, 2026-11-06 about 18:00 UTC to 2026-11-12 about 13:50 UTC.
  Both Builders were interrupted several times and resumed from their own state.
- **The gap in the live record.** No run happened from the 2026-11-08 issuance (2026-11-07T10:24Z) until
  2026-11-12T13:5x: the weekly pause, with no job scheduled beyond 2026-11-08. 2026-11-09 is closed as not issued, no
  run within the lookback; 2026-11-10..13 are not issued, their load forecasts retrieved after their cutoffs. Days from
  2026-11-14 are scheduled on the Mac.
- **The first live run failed its H2 pins check** (the pipeline's clone is not the project), and issued nothing; fixed,
  and the second run issued. CP-18a's fallback rehearsal never ran the real gate from a separate clone.
- **SMARD publishes the load forecast after the cutoff** (its bucket's own creation time), so the live load forecast
  is ENTSO-E's A65, the plan's series. The development history keeps SMARD's values (the snapshot); the live days
  continue with A65.
- **Two transient GFS decodes failed** (49 of 50 messages, the 2026-09-22 and 2026-10-13 runs) in the three-worker bulk
  download; each sequential retry decoded all 50. In the daily operation a run retries whatever an archive day lacks.
- **TLS:** the live transport verifies against certifi's pinned bundle (the interpreter's store lacked ENTSO-E's root).
- **Hugging Face injects** a script and Open Graph tags into every served HTML file; the served-identity check compares
  HTML after removing exactly that injection, and records raw and normalized matches.
- **The first live artifact's data-refresh time** is written `…Z`; the bundle's manifest restates the same instant in
  the frozen manifest's `…+00:00`.
- **v1's files** are under `reports/cp18c/history-v1/` (CP-18b's tests police `space-product/` for dates, hashes and
  foreign URLs, which v1's demo carries), with its `.gitattributes` kept beside them, so this repository applies no LFS
  rule; the Space build places it at `/history/.gitattributes`.
- **N1 is live-only:** a dry run's bundle keeps CP-18b's source label, so CP-18b's committed records reproduce byte for
  byte.
- **The Orchestrator's O35:** one added line in `tests/cp18a/test_dry_run.py` (the throwaway seed clone runs
  `git rm -r -q --ignore-unmatch live` before `seed-store`), after checking that no freeze manifest, `PINS` or evidence
  binds its bytes (`a6e56482…` before the line, named nowhere). The same set-aside is in `src/cp18/forced.py` and in
  `daily.yml`'s dry run.
- **O33's runs** come from a transcription of `cp28.inference.calendar_runs` without its guard admission (the frozen
  function refuses every live date); everything else is `cp28`'s own code, shown bit-identical.
- **The committed browser acceptance** (`reports/cp18c/acceptance/acceptance.json`) ran on the two-day bundle
  (`689ab83f…`) before the live label took O30's name; the Integration review reruns the Space in Chromium and WebKit
  on the candidate's live bundle. O33's band was checked on a display-only build from development days (the live record
  has fewer than 14 scored days); that build is never served.
- **Retrievals outside the archive:** the Lead's SMARD probe (counts only), a smoke test into a scratch archive, the two
  failed GFS decodes, v1's 805 files and their listing, and the scratch rehearsal's development-day GFS (40 MB per run).
- **The Hub client** is not a project dependency, and the imported workflow and fallback called the publication without
  it, so every daily publication would have failed on its import. Found before the review and fixed in both callers:
  `cp18.publish.HUB_CLIENT` (`huggingface_hub==0.36.2`) through `uv run --frozen --no-sync --with`, leaving `uv.lock`
  and the issuing host's environment unchanged (`tests/cp18c/test_publish_hub.py`).
- **Cost:** 0.27 of 6 GitHub job-hours; about 6 local machine-hours before the Integration review
  (`reports/cp18c/evidence/compute-ledger.json`).
