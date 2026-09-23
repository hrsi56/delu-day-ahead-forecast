# Weather admission and research-content intake — 2026-09-23

**Accepted:** GFS ADMIT for the dossier's inventoried scope under its disclosed assumptions;
ICON NOT_ADMITTED; CP-15/16 content accepted as a local draft for Owner review. No README/site
change, publication or model result follows. CP-20 v21-r4 is now ratified and execution separately
authorized (2026-09-23); see the issued brief. CP-16 closure is not reopened.

## Evidence and disposition

| Issued requirement | Return and intake finding |
|---|---|
| Weather access and source limits | `reports/weather-admission/dossier.md` §3 records anonymous NCAR/AWS access and authenticated HF account/gated-file 206 at pinned ICON revision. Two products, no replacement search or paid access. Token not inspected/reused at intake. |
| Actual decoded fields, leads and DST | §§4–5, `decoded/summary.csv` and 22 per-run JSONs document 12 GFS / 10 ICON bundles, version/schema checks, wind heights, h22–h46 support through h48, 23/24/25-hour days, units/averaging and endpoint compatibility. Existing decoding evidence accepted, not rerun. |
| Complete historical inventory | `inventory/gfs_required_runs.csv`, `coverage_by_archive_fold_field.csv`, `verdicts.csv`: 2,468 combined GFS runs; AWS 2021-02-02 absence filled by NCAR; NCAR 2024-09-15 f039 truncation filled by AWS. ICON documented absence/defects and unsupported hub-height winds justify NOT_ADMITTED, not failed token access. |
| Field-presence evidence limits | NCAR-only 2019–2020 and the NCAR fill use inferred field presence from file integrity/size and decoded version layout; not exhaustive per-message verification. Every extracted message must be checked in CP-20. Admission is conditional on this disclosed basis. |
| Historical availability | §6 and dated `availability/`/`sources/` evidence support reconstructed availability under the approved rule. NCEP production completion averages plus assumed public-server dissemination lag do not prove every cycle arrived; no current-schedule-only inference or contemporaneous-log requirement is imposed. |
| Boundary/conversion limits | Delivery 2019-01-01 has no permitted D−1 run. §5.3/§11 disclose the radiation check defined after sampling, coarse packing and clipping need. These remain visible and are fixed prospectively in ratified §15, not retroactively preregistered. |
| Weather resource caps | Reported 1.5 active h, 34/48 decoding attempts, 3,678,795,640 transfer bytes/4 GiB, peak disk 1.87/8 GiB, sampled summed RSS ≤562 MiB/8 GiB, ~1.3/8 machine h; failures/duplicates included. Aggregate sampling started 13:10Z; earlier single-run RSS exists but is not continuous historical aggregate proof. No retroactive compliance claim. |
| Content scope/claims | Two requested Markdown drafts, score/all-six-criteria tables, two chart specifications, reusable summary and claim map. H−P no joint preference, exploratory H−B2 improvement, criterion-5 attribution limits and original product failures preserved. Existing accepted saved values/verdicts used; no metric or model rerun. |
| Content limits | No publication/rendering or README/site edits. Returned files do not record actual active effort/correction-round count; acceptance is of local content, not an assertion that this unreported accounting was independently verified. No further content execution is requested. |

Intake read the returns and their supporting saved tables/manifests/source excerpts, checked
all 53 weather report checksums and source/destination preservation, and checked only the new
warm-up dependency. It did not repeat access, downloads, decoding, statistical tests, modelling
or the already accepted Integration reviews. The app-created worktrees were declared by the
Owner and are not a configuration defect.

## Smallest corrections and next dependency

1. Corrected dossier §8's **“without any fallback”** contradiction: admission does not remove
   structural 2019-01-01 missingness or the need for an explicit failure/fallback rule.
   Only that prose and its checksum entry changed; original executor bytes/checksums retained.
2. Content's 377 H/P peak hits are accepted saved CP-16 diagnostics, not an extra Owner
   parameter decision. Local scope is approved; public use remains out of scope. Narrowed
   “hour awareness cannot explain the change” to “cannot uniquely explain the shared
   transition”; H−P measures the incremental effect. CAP line citations now explicitly bind
   historical v21-r3 bytes so the new draft does not invalidate them.
3. The weather inventory used CP-15 warm-up, while CP-16's training-only admission needs
   earlier warm-up. Comparing existing date manifests identifies exactly **eight uninventoried
   runs: 2023-03-24..31**. The minimum fix is a targeted GFS pre-fit field/lead/availability
   check within CP-20's approved caps; no broad re-admission or experiment was run here.
   CP-20 inherits the 638 CP-16 origins and requires 2,476 unique weather runs in total.
4. Propose fixed conversion and missing-input rules in §15, including training-only inherited
   imputation/indicators for confirmed weather gaps; resource-limited incomplete extraction
   cannot be disguised as a missing-input fallback. The revised scientific specification and D4 ceilings are
   now ratified; CP-20 execution is separately authorized as recorded below.

## Import, preservation and reclamation

Before removing anything, copied **54** weather-report files and **2** content files into the
same relative paths in the main working tree, and moved **4,583** recovery/environment files
from the weather worktree's `.local/weather-admission/` to main's `.local/weather-admission/`.
All source/destination hashes or symlink targets matched. These three destination directories
were absent; no destination content was overwritten. Original report/content copies, full
manifests and the two worktrees' incidental `.claude/settings.local.json`/`.DS_Store` files are
preserved under `.local/artifacts/weather-intake-cp20-20260923/`; no configuration was edited.
The moved decoder environment is historical recovery: embedded old paths may need rebuilding
under a future authorized budget; no environment execution was attempted during intake.

| Reclaimed Owner-declared branch/worktree suffix | Verified preservation tag | Tip / unique commits |
|---|---|---|
| `claude/weather-archive-executor-handoff-6abd84` | `archive/weather-admission-20260923` | `110ce15e8b8fff4cc9b08e33e1b948ad9a50c310` / 0 |
| `claude/cp15-cp16-research-handoff-8755f6` | `archive/cp15-cp16-content-20260923` | same / 0 |

Both tags were created and their exact commit/reachability checked before each authorized
worktree removal and branch deletion. No unique commits existed; tags preserve the base tips,
**not uncommitted deliverables**. The imported files and backup manifests preserve those.
Only main and its primary checkout remain; main HEAD and index are unchanged. No commits,
mainline merge or publication. Old worktree references retrieve from the same relative paths
in the main checkout; original executor bytes retrieve from the local intake archive.

## Issued handoff

[Ratified specification](../../capstone_v21.md#15-cp-20--direct-gfs-paired-research-ablation-v21-r4-ratified),
[one-page brief](cp-20-direct-weather-brief.md) and
[one-page amendment](capstone_v21-r3-to-v21-r4-amendments.md) implement programme 4.0b for 4.4D.
No material blocker to preparing the draft remains. Subsequent bounded revision records D4
ceilings approved (120 aggregate machine-hours, other caps unchanged) and the three-feature
wind-speed/radiation recipe. Owner ratification and separate CP-20 execution/§15.7 packaging
authorization are recorded, 2026-09-23. Eight-run evidence and Lead feasibility/accounting
remain pre-fit execution conditions, not implied successes or routine Owner decisions. The
scoped issuance suspension ends at terminal return. The interview lesson is captured via the prescribed Q&A appender.
