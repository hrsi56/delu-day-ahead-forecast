# Weather-archive admission — executor handoff

**Engineering Lead · programme 4.1 only · 2026-09-23.** Repository:
`/Users/djourno/Downloads/PJM`; starting main `110ce15e8b8fff4cc9b08e33e1b948ad9a50c310`.
Owner approves corrected bounded execution and carries this handoff; no model checkpoint opens.
Read `AGENTS.md` and `engineering-role.md`. Controlling anchor: [v21-r3](../../capstone_v21.md)
§§2–3; task requirements: [programme §4.1](v3-plan-handoff-2026-09-22.md#work-4-1),
[4.B](v3-plan-handoff-2026-09-22.md#section-4-b), §5.9 and §3.2.

**Ceilings.** Stop at **16 cumulative active hours**, including preparation, decoding,
failures, checks and return; coverage/publication evidence is due then. **2 archive products:**
GFS 0.25° and OCF ICON-EU; no replacement-provider search. Verify actual NCAR coverage first;
do not assume its cutoff. Permit NCAR-linked **NOAA GFS AWS** for the same product, including
missing 2026 tail; verify cross-endpoint product/grid/field/lead compatibility. Fold 5 ends
**2026-04-07**. **24 distinct initialization runs: 12 GFS combined across endpoints, 12 ICON**;
one decoded bundle/run; **48 decoding attempts**, including failures/retries.
**6 native fields/bundle:** four wind components (u/v at 10 m and documented higher near-hub
level), plus downward shortwave radiation (ICON **ASWDIR_S + ASWDIFD_S**). Validate units,
averaging periods and alignment before combining. Pressure levels are not turbine heights;
report unsupported heights/missing fields explicitly. Native endpoints **h0–h48**, only those
needed for hour starts and accumulation/interpolation; subset/range-read where available.
Maximum **4 GiB cumulative transfer** (metadata, dependencies, samples, failures/retries),
**8 GiB additional disk**, **8 GiB aggregate RSS**, **8 machine-hours**, **4 CPU cores**;
Local CPU only; **$0**, **0 fits/model runs/full-archive downloads**. Log usage; stop before
any cap is exceeded. Maxima, not targets/feasibility estimates; free access only.

**Access.** Owner reports accepting OCF ICON-EU conditions and `HF_TOKEN` availability through
`launchctl`. Use it for authorized read-only access without printing/persisting its value.
Verify authenticated account and gated-file access with a minimal request before substantial
retrieval; report actual status, not presumed token access from terms acceptance. Return
unresolved access/registration/terms needs without paid workarounds; requests count toward caps.

**Evidence required.** Freeze a sample manifest before retrieval: earliest required history,
crisis, modern period, spring/fall DST (23/24/25-hour days), and relevant schema/grid changes.
Apply the inherited five-fold history starts, genuine warm-up, 2019 floor and D−1 boundary
exactly as §4.1; inventories must cover every required run/field, not only sampled dates.
Decode actual values and metadata. Demonstrate **h22–h46 hour starts**, including supporting
endpoints through **h48**. Dated primary-source dissemination documentation applicable to
the model version, historical period, cycle and every required lead suffices for
**“reconstructed availability” before D−1 11:00 UTC**; retain dated source fingerprints.
Per-day contemporaneous logs are not mandatory. Disclose assumptions/exceptions: schedules
do not prove uninterrupted delivery; a current schedule alone cannot establish historical
timing. Initialization, retrieval and archive start dates alone are insufficient. Exclude
hindcasts, analyses and later updates. Retain all §4.1 lineage/conversion/aggregation requirements.

**Return once.** Write `reports/weather-admission/`: dossier, inventories, manifests/hashes,
decoded evidence, source extracts, usage, gaps, extraction-volume/time estimates, service/rights
limits and reproduction commands; raw caches/scratch in `.local/`.
**ADMIT/NOT_ADMITTED per archive × fold × field**; unproven coverage/availability at deadline
is NOT_ADMITTED for that scope. Distinguish access/budget gaps from archive absence.
Return §3.2 options without selecting one. Historical admission does not certify live suitability.
No experiment, full extraction, CP-17, governance/progress edit, staging/commit or publication.
