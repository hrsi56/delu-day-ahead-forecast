# Independent programme-plan review — 22 September 2026

**Verdict: TARGETED REVISION REQUIRED.** The revised plan's principal numerical corrections withstand independent checking. Its most consequential remaining defect is the execution graph: weather admission still appears to gate the existing-input v2 route, a research release appears to depend on new v2 results, and final disposition does not explicitly wait for optional recombination. These are repairable dependencies, not grounds to restart programme design or commission another broad review.

**Smallest sufficient next step:** transfer the accompanying bounded rewrite brief. After that document repair, request an Owner decision on the next delivery and a separate brief for a single existing-input v2 experiment. A local research-content package using completed CP-15 evidence can be prepared independently when authorized. Weather admission can also be separately authorized; it need not precede either of those paths. Full programme execution remains conditional on Owner choices, an authorized additive amendment and checkpoint briefs. This review opens no work item.

## Scope, independence and evidence identity

Role established from the complete `AGENTS.md` and the Owner's explicit task: **Owner-directed bounded programme-plan reviewer**, neither Engineering Lead checkpoint execution nor Orchestrator state maintenance. No agents were launched. Only this review and its rewrite brief are durable additions. Existing dirty files, the reviewed plan, all anchors, evidence, Q&A, source, tests and model artifacts were preserved. No reserved outcome partition was inspected; reading partition definitions did not read their outcomes. No forecast candidate was trained.

The current plan was read in full before `docs/track-b/plan-review-2026-09-22.md`. Initial diagnosis was saved first in `.local/independent-review-2026-09-22/initial-diagnosis.md`: preserve the improved qualification/contamination language; investigate unnecessary weather gating, research-release dependencies, family-only budgets, the 4.7/4.8 ordering, vintage admission, battery specification and ambiguous verification labels. It also flagged the median-pinball scaling error. Subsequent work confirmed these concerns without resurrecting the prior review's already-corrected impossibility allegations.

The earlier review was then read and challenged. Its revised LP scores, day-switching statistics, interval diagnostics, A69 calculation and principal battery sensitivities reproduce. Its original-controller illustration was not rerun. Some verification labels need narrower objects; its battery policy omits a tie rule; its executable appendices do not reproduce every number quoted in its prose. Those are findings below, not reasons to reject everything it established.

Input SHA256 identities:

| File | SHA256 |
|---|---|
| Reviewed plan | `290107db5abdd0623c519bfe1c745bec75a51980cd3f3b8b707d0e69458fee72` |
| Earlier review | `29c6b3927f9796bd64b8551261e49525a587febfe5601df0a50d503f17e4bf00` |
| `capstone_v21.md` | `44ea4e545d2caa276a36a7a70db6ea044b3975196ead06f3ce59f976c83354b3` |
| `reports/cp15/protocol.json` | `051e4b7cdd1d5db68b26e6d6bc17333c4055c4bcbe5ea693d1d647fe355ccdd6` |
| `reports/cp15/predictions.parquet` | `1a606d613ba5f6af82712a7e44adcaf639ba0ece1b7865f407f559fafafeda92` |
| `reports/cp2/a69_benchmark_predictions.parquet` | `81347d054eecb72002c61bf725ea697ef96e3883c6b79cf464ab35ff843d2e90` |
| `data/partitions.json` | `6bee065368b721ae8092ba287e04bb6dda0d4bde80909e72380503ba61e0b090` |

Existing environment: Python 3.13.15, NumPy 2.4.6, pandas 3.0.3, SciPy 1.18.1. No dependencies were installed. Independently written analysis is retained in the ignored project-local directory above: `verify.py`, `diagnostics.py`, `battery.py`, `ties.py`, their JSON/CSV outputs and preservation manifests. Essential methods, populations and findings are recorded here; scratch is not their only record.

## Verification gate — PASS

An independent harness was written from `protocol.json` before reading the earlier review. It does not import the project's or prior review's metric functions. There are 96,723 rows, nine policies and **10,747 identical target keys and truths per policy**, with no duplicate policy/fold/timestamp keys. Emitted quantiles and truth are finite and quantiles ordered. Fold counts: **2,160 / 2,159 / 2,112 / 2,160 / 2,156**. The original eligible prediction population was retained without extra filtering; feature eligibility was not reconstructed from the snapshot.

For each row, `MAE = abs(y-p50)` using the **emitted** p50. For each interval with alpha .5/.2/.05 and endpoint levels (.25,.75)/(.10,.90)/(.025,.975), form `alpha/2*(u-l) + max(l-y,0) + max(y-u,0)`. Add `.5*abs(y-p50)` and divide by 3.5. Average each loss within a fold; divide by the corresponding B0 fold mean; average the five ratios equally. This is not a pooled-loss ratio or the nine-quantile native v1 pinball.

| Arm | Independently calculated S_MAE | S_WIS | Five-decimal gate |
|---|---:|---:|---|
| B0 | 1.0000000000 | 1.0000000000 | REPRODUCED |
| B2 | 0.6578109124 | 0.6389910407 | REPRODUCED |
| A1 | 0.6722908121 | 0.6460150916 | REPRODUCED |
| A2 | 0.7737135304 | 0.7316680120 | REPRODUCED |

B0 fold MAE denominators: **8.63313889, 16.17162575, 86.94887311, 22.98456481, 30.50341489**. WIS denominators: **5.70904148, 10.88716980, 51.72695987, 14.56124060, 17.91506629**. The unchanged §8 aggregate limits are .9×.6578109124 = **.5920298211** and .9×.6389910407 = **.5750919367**. CP-15 remains Engineering PASS / `product_feasibility = NOT_DEMONSTRATED`, consistent with its landing and selection records.

## Pass A — Evidence and inference

Verification vocabulary applies to a named proposition: **REPRODUCED** for matching a specified calculation/source; **REPRODUCED WITH DEVIATION** for a related specified calculation whose result or population differs; **NOT REPRODUCED** for a sufficiently specified claim that does not match; **NOT TESTED** when its recipe/evidence is missing or it was not attempted. None is a qualification verdict.

### Combinations and day switching

Use emitted p50 columns in arm order **B1, B2, B3, A1, A2, A4**. Set row coefficient `c_i = 1/(5*n_f*MAE_B0,f)`. Solve the L1 linear program `min sum(c_i*t_i)` subject to `t_i >= ±(X_i*w-y_i)`, nonnegative weights summing to one. Separate group solves allow fold, Europe/Berlin hour, or fold×hour weights; summing their objective contributions preserves the original equal-fold objective. All solves succeeded. The per-row convex result is distance from truth to `[min(X_i),max(X_i)]`; the discrete result selects the smallest absolute error.

| Diagnostic | This review | Status relative to revised ledger |
|---|---:|---|
| Six-arm mean S_MAE | .6713616681 | REPRODUCED |
| Static convex optimum | .6354381119 | REPRODUCED |
| Fold convex optimum | .6247236318 | REPRODUCED |
| Hour convex optimum | .6263397609 | REPRODUCED |
| Fold×hour convex optimum | .6040659194 | REPRODUCED |
| Per-row discrete / convex oracle | .3344526097 / .2724531881 | REPRODUCED |
| Pooled-MAE optimum, then equal-fold score: static / hour | .6374245877 / .6301085200 | REPRODUCED |
| A1+B2 emitted-vector mean, S_MAE / S_WIS | .6446561939 / .6200244509 | REPRODUCED |
| A1+B2 central mean, before its new residual layer | .6406962203 S_MAE | REPRODUCED against earlier review; not measured v2 |
| A1/A3/A5/B2 emitted-p50 mean | .6427958857 S_MAE | REPRODUCED |

Static weights are .03599364/.47846095/.05453484/.30789722/.10668956/.01642379. The pooled objective explains numbers near the original .63744/.63015, but does not prove which unavailable implementation produced them. A restricted optimum below its own class's alternatives is not an information ceiling; no nonlinear, conditional, signed/intercept, differently represented or newly trained model is bounded by these figures. Even a small restricted oracle gap does not itself quantify the expected research payoff. The revised plan appropriately avoids these overclaims. Reduced-grid .63487/.61383 and rolling QRA .64590/.63423 are not full-grid v2 results; exact QRA, stacker and learned-block recipes remain **NOT TESTED**.

For switching, compute daily means of A1/B2 emitted absolute errors, choose A1 on strictly lower daily loss, and score the chosen hourly losses with the same `c_i`. A1 wins **227/448 days**, crisis **53/88**. Fold/day/row switch oracles are **.6513817046/.5991890302/.5305472317**, all **REPRODUCED**. Per-fold A1/B2 MAE is **6.81990/6.21927; 9.95336/9.67638; 51.21276/54.00782; 16.74044/16.54061; 19.48164/19.20250**.

Lag-1 correlation concatenating only within-fold adjacent represented days is **.07888943** over 443 pairs, mean run **2.14354067**, reproducing the review. Requiring actual consecutive calendar dates leaves 442 pairs and gives **.08133594**, with the same mean run. Neither measures conditional predictability. The oracle daily result also weights error magnitude, unlike a classifier's accuracy. The original 42.8% and earlier review's separately fitted 51.67% illustration are **NOT TESTED here**; no controller was fitted. Deferral remains a sensible budget choice, not a mathematical impossibility.

### Battery: robust caution, not a general winning model

Independently solve with explicit SOC variables `e_0..e_N`: maximize forecast `sum[p_t*(dis_t-ch_t)-k*(ch_t+dis_t)]`, `e_(t+1)=e_t+sqrt(.9)*ch_t-dis_t/sqrt(.9)`, 0≤ch/dis≤1, 0≤e≤2, e_0=e_N=0. Settle the frozen dispatch at truth. The one-cycle variant additionally limits `sum(dis/sqrt(.9))≤2`; the €10 variant charges €10 per grid MWh on **both** charge and discharge and imposes binary exclusive modes. The efficiency split, cost and daily resets are assumptions, not Owner economics.

Require the complete canonical UTC set for each Europe/Berlin delivery day. **444 complete days** remain. Excluded represented days are 2021-04-04 and 2026-03-30, 03-31, 04-05 (each 23 of 24 expected hours). Two whole fold-3 dates are already absent from CP-15. Statistical scores still use all 10,747 rows. Complete-day economics is a conditional sample, not a claim about outage-inclusive operational value.

| Policy | Closure EUR/day | Closure equal-fold PF capture | One-cycle EUR/day | One-cycle + €10 + exclusive EUR/day | Last variant equal-fold PF capture |
|---|---:|---:|---:|---:|---:|
| B0 | 221.90379* | 86.56828%* | 173.90896* | 134.03988* | 67.50987%* |
| A1 | 224.85102 | 88.10806% | 175.19820 | 135.76451 | 73.78265% |
| B2 | 226.58789 | 89.59339% | 175.36788 | 136.30737 | 77.17351% |
| B3 | 228.14720 | 90.64350% | 176.42759 | 135.58496 | 70.97354% |
| Blend | 230.29167 | 90.71006% | 178.37935 | 139.27263 | 77.70808% |
| A2 | 232.09770 | 91.45283% | 179.96894 | 139.86507 | 75.45840% |
| PF | 251.84875 | 100% | 200.00916 | 161.23963 | 100% |

Except B0*, these reproduce the earlier review to its printed precision. *B0 is **REPRODUCED WITH DEVIATION** using the equivalent explicit-state formulation. A separately implemented cumulative-state LP gives its quoted closure **221.86397554**. Fourteen days have different dispatches with forecast objectives equal within 1.2e−13. On 2025-07-27, the equal-optimum dispatches realize **120.12548 versus 153.19398 EUR**, without either optimization seeing truth. This diagnoses solver tie selection, not a revenue formula failure. Non-closure B0 deviations were observed but not individually tie-audited; they should not be called exact replications.

Closure has **1,318 simultaneous charge/discharge hour-policy instances** and roughly **1.97–2.10 cycles/day**, reproducing the prior warning. It is a relaxation, not an implicit one-cycle battery. A2 leads pooled EUR/day in these three settings, but loses the €10 equal-fold PF-capture comparison to blend/B2. Equal-fold capture averages `mean revenue_model,f / mean revenue_PF,f`; the displayed pooled EUR/day ratio is a different estimand. For example, closure A2 is **92.15758%** on pooled ratios versus **91.45283%** on equal-fold ratios. PF benchmarks must be reoptimized under each identical decision specification; a zero/nonpositive PF denominator needs an explicit reporting rule.

The level-sensitive counterexample also reproduces: `(50-y)*I(p50<50)` averaged across all original target hours gives **A1 6.85249, B2 6.81997, A2 6.31212, blend 6.87053 EUR/target-hour**. This is buying at the hourly price and reselling at the fixed strike (or equivalent avoided-cost exposure), not buying at a fixed €50 strike. The plan's description should state the cashflow direction. Median-threshold dispatch is a forecast proxy, not generally the expected-profit optimum.

Bootstrap reproduction: closure A2−blend daily differences, seed 15042, 2,000 replicates; within each fold's full 90-date calendar draw uniform noncircular 7-date block starts, concatenate ceil(90/7) blocks, truncate to 90, retain missing dates as NaN; pool represented days across folds, taking a paired mean. Result **+1.80603626 EUR/day, 95% percentile interval [−.48577113, 4.29188849]**, **REPRODUCED**. The €30 sensitivity and €10 bootstrap were **NOT TESTED here**. The original author's underspecified table remains **NOT TESTED as an exact experiment**; the related experiments differ from it. There is no confirmatory superiority test or representative annual value.

### IR-04 — Medium: the economic policy needs an executable decision contract

- **Affected:** §§3.1, 4.0, 4.2, 4.9 and 5.6. **Challenged instruction:** “predefine economic decision” leaves solver ties, forecast functional, operational missing-day treatment and market resolution implicit.
- **Evidence/method:** independent dispatch and tie audit above; identical forecast optima can have different realized values. Hourly marginal quantiles also do not specify a joint path distribution for risk-sensitive storage dispatch.
- **Consequence:** a replay can be numerically correct yet implement a different policy. A backtest on complete hourly days cannot establish operational economics for a quarter-hour exposure with outages. The [European Commission's October 2025 notice](https://energy.ec.europa.eu/news/eu-electricity-trading-day-ahead-markets-becomes-more-dynamic-2025-10-01_en) confirms the move to 15-minute day-ahead trading.
- **Required correction:** name these fields in the future decision record: objective/forecast functional, settlement resolution and cashflows, all physical/cost constraints, deterministic tie rule/solver settings, missing-input execution fallback, value aggregation and denominator policy, uncertainty and externally justified surplus. Retain hourly economics as explicitly scoped unless the Owner authorizes a different product. Clarify the fixed-strike cashflow. Keep economics descriptive if the Owner cannot supply an independent rationale.
- **Unknown:** actual user, asset costs, risk preference, fill/imbalance assumptions, quarter-hour delivery choice and net-value margin. No values are selected here; no additional trading model is requested by this finding.

### VRE schedules and weather archive evidence

Primary sources were checked on **2026-09-22**. The named [SMARD forecast page](https://www.smard.de/page/en/wiki-article/5884/206318/forecast-data) says TSOs submit next-day data at 18:00 and distinguishes publication by that time. The [TenneT control-area wind page](https://netztransparenz.tennet.eu/electricity-market/transparency-pages/transparency-germany/network-figures/actual-and-forecast-wind-energy-feed-in) specifies 08:00 estimation and 18:00 publication. **REPRODUCED** for these routes. This supports withholding these feeds for the 11:00 UTC origin; an 18:00 deadline alone would not exclude earlier publication. It proves neither universal absence of a pre-gate VRE feed nor identical schedules for every TSO/solar product. The historical June n=1 observation was **NOT TESTED here**. No polling or new provider search is required to preserve the narrow conclusion.

| Primary source | Independently checked documentation | Admission implication |
|---|---|---|
| [NCAR d084001](https://gdex.ucar.edu/datasets/d084001/) | Operational GFS 0.25°, 2015-01-15 start; four UTC cycles; 3-hour steps to 240 h; wind and shortwave categories; CC BY 4.0. It warns NCAR updating will stop in early 2026 and points to AWS, despite a conflicting future-dated upper range. | Documented depth is plausible. Do not infer continuation from the upper timestamp. The earlier review's 2019 file-list URL was not retrievable through this session's web tool; individual files/fields were not decoded. |
| [OCF ICON-EU](https://huggingface.co/datasets/openclimatefix/dwd-icon-eu) | 2020-01-01 start; early 27-variable subset includes 10 m wind components, pressure-level winds and accumulated/mean direct/diffuse shortwave fields; March 2023 schema change; four cycles; gated access and archive no longer updated. | Crisis-depth candidate, not all-fold admission. Grid wind levels are not automatically hub-height generation features; do not treat pressure-level heights as fixed above-ground heights. |
| [OCF ICON-Global](https://huggingface.co/datasets/openclimatefix/dwd-icon-global) | March 2023 start, four cycles, 48–96 h runs. | Too late for crisis training; documentary start reproduced. |
| [Dynamical GFS](https://dynamical.org/catalog/noaa-gfs-forecast/) | 2021-05-01 start, init×lead preserved, hourly through 120 h; wind levels and shortwave listed. | Too late for the full crisis training window, possible later/continuation route. |
| [Dynamical ICON-EU](https://dynamical.org/catalog/dwd-icon-eu-forecast-5-day/) | 2026-02-10 start, hourly through 78 h, 120 h horizon; 10 m wind and direct/diffuse radiation. | Does not recover the old OCF history. Radiation averaging semantics differ across products and need conversion checks. |
| [Open-Meteo Historical Forecast](https://open-meteo.com/en/docs/historical-forecast-api) | GFS 2021-03-23; ICON family 2022-11-24; a stitched short-lead series. | Not evidence of the required single D−1 run. |
| [Open-Meteo Single Runs](https://open-meteo.com/en/docs/single-runs-api) | IFS HRES 2024-03-14, most others 2026-04-02; source text explicitly calls early IFS Cycle 49R1 coverage hindcasts and identifies Cycle 50R1 from 2026-05-12 06 UTC. | Earlier review's hindcast caveat reproduced. The same page's generic “exact forecast issued” language does not override its specific hindcast disclosure. Typical publication latency is not a historical availability audit. |
| [Open-Meteo Previous Runs](https://open-meteo.com/en/docs/previous-runs-api) | Fixed 1–7-day offsets, mostly January 2024; GFS 2 m temperature March 2021, JMA GSM/MSM 2018 exceptions. | A temperature exception is not wind/radiation coverage; offset-by-valid-time need not satisfy one day-ahead issue time. |

All start-date entries above are **REPRODUCED as documentation**, not decoded admission. Historical provider/model/version/variable/lead/publication continuity is **NOT TESTED** in full. No fold has become admitted by this review. NCAR has enough nominal historical depth to keep a common grid plausible; blanket historical impossibility remains unsupported.

Time arithmetic independently recomputed from partition dates gives first-evaluation training starts **2019-01-01 / 2019-04-04 / 2020-07-03 / 2023-05-04 / 2024-01-11**. Warm-up can extend the latter four earlier; the 2019 floor remains. Under D−1 00 UTC initialization and hour-start target timestamps, required leads are **23–46 h in winter, 22–45 h in summer; spring DST 23–45 h (23 targets), autumn DST 22–46 h (25 targets)**. Interval-valued radiation also needs its bounding steps/endpoints, potentially through h48 on a three-hour grid. This is lead arithmetic, not publication proof. Interpolating only among steps in an already released run is distinct from using later-run observations. Availability of every contributing field/step must precede 11:00 UTC, and pre-2019 initialization must not slip in at the first training boundary.

### IR-05 — Medium: archive admission needs explicit continuation and required-lead tests

- **Affected:** §§4.1, 4.9, 5.9. **Challenged instruction:** prioritize archives on documented depth, with only generic “continuation” and interpolation checks.
- **Evidence/method:** documentary table and independently calculated lead ranges above. NCAR explicitly warns of discontinued updates. Dynamical's [migration notice](https://dynamical.org/migration-2026/) asks users to plan for September 30, 2026, with dataset-by-dataset shutdown over following months; supported access uses STAC/Icechunk. This is an access migration, not proof that historical content disappears.
- **Consequence:** a valid historical dataset may fail during prospective issuance; an h24-only or temperature-only sample can falsely pass a general sample check.
- **Required correction:** include required lead/field endpoints, historical model/schema changes, a supported current access route, historical-to-live equivalence and a deadline/fallback for absent continuity evidence in the admission dossier. Keep the 16-active-hour stop and allow NOT_ADMITTED/gap-list closure. Distinguish provider operational publication from archive retrieval time and from reconstructed availability. Record source retrieval date and source-text fingerprint for admission claims.
- **Unknown:** exact historical release evidence, decoded field coverage, gaps, free extraction volume and sustainable live delivery. Do not turn this correction into a request to complete admission in the rewrite.

### Other recalculations and inference limits

Six-arm population SD versus A1 absolute error gives quintile MAEs **6.39401/10.72882/15.28001/22.48956/48.63872** and fold correlations **.41647/.07601/.00048/.25662/.20023**, **REPRODUCED** against the earlier review's explicitly defined variant. The original disagreement recipe and width-driver WIS .63425/.60691 remain **NOT TESTED**, not falsified by different features/populations.

A1 maximum within-day 95%-width range is **1.7053e−13**. Hour-specific mean widths **134.32455–134.42098**, night 00–05 coverage approximately **.993–.998** and midday 12–15 **.866–.888**, with the stated MAE ranges, reproduce. Different per-hour denominators explain the tiny mean-width differences. For a declared oracle, within each fold/hour take linear quantiles of raw signed `y-emitted_p50`, add them to emitted p50 and hold its .5 column fixed. S_WIS is **.61048142** for A1 and **.58936091** for the four-component mean; vectors remain ordered. These are **REPRODUCED** alternative oracles, not exact replications of the original .61009/.58927 constructions or forecasts of causal performance. The proposed causal range .589–.638, causal .63793 and original criterion-5 claim remain **NOT TESTED**. The actual v2 can fail honestly; its S_MAE changes if its residual median changes.

The architecture distinction is supported by `src/cp15/models.py` and protocol: hourly LEAR fits use cross-hour vectors, versus one pooled daily LightGBM using 23 features. B3/B2 MAE ratios reproduce at **1.626536/1.172716/1.133081** over night/shoulder/solar **3,579/4,032/3,136** rows. These diagnose the current fits, not causally identify architecture as the problem. A1 daily-level MAE **5.63408/7.40212/41.62120/9.25786/14.40437** reproduces. Equal-day shape MAE **4.83314/6.96725/35.48387/15.53149/14.95215** and protocol hourly **4.83314/6.96495/35.48387/15.53149/14.93592** also reproduce. They are not additive, and A2 has worse shape MAE than B2 in folds 2, 4 and 5 despite its storage revenue ranking.

The two A69 arms have identical ordered fold/date/truth sequences, also matching CP-15's ordered truth. The A69 artifact lacks an hourly timestamp column, so exact hourly-key lineage is not independently certified from that artifact alone. From these two 10,747-row arms, average `max(tau*(y-q),(tau-1)*(y-q))` across nine raw heads at .025/.05/.1/.25/.5/.75/.9/.95/.975 and all target rows. Result **13.0158415097→10.4787146325**, reduction **19.49260734%**, raw-p50 MAE **41.75983236→29.93830428**, **REPRODUCED**. This is a post-gate v1 feature bundle, not the proposed available-at-gate v3 inputs or normalized CP-15 point/interval policy. Fold 2 pinball actually worsens **5.92946717→6.08276822**. Thus the pooled lift establishes neither every-fold gain, calibrated coverage, transfer percentage nor in-house VRE recovery fraction. WIS/pinball comparisons require an identical quantile grid, calibration, population and normalization; the headline has none of those guarantees for v2/v3.

The full [TabPFN-2.5 v1.1 licence](https://huggingface.co/Prior-Labs/tabpfn_2_5/raw/main/LICENSE) confirms the eligibility/use, output and hosted-service restrictions underlying the plan's conditional admission. No paid or negotiated workaround is available within this task's constraints. This is verification of the text, not legal clearance of a proposed deployment. DDNN fit cost/quality/delivery, Chronos pretraining overlap and the ~57 MB browser/parity claim were **NOT TESTED here**; retain their reported/unknown status and future admission gates. No new family should be added because a conditional candidate is ineligible.

### IR-06 — Medium: verification labels must name the experiment and evidence provenance

- **Affected:** §5 introduction and §§5.2–5.6, 5.9; references to the earlier review. **Challenged claims:** heading-level NOT REPRODUCED for underspecified originals, and “archive start claim — NOT REPRODUCED” above now-correct dates.
- **Evidence/method:** the specified revised diagnostics match; originals lack recipes. Earlier review's embedded `recompute.py`/`supplement.py` do not explicitly reset p50 in their tail-oracle code, although prose reports fixed-p50 values; no bootstrap implementation is embedded there. Independent fixed-p50 and bootstrap recipes above recover the quoted values. This is incomplete executable coverage, not evidence of fabricated results.
- **Consequence:** readers cannot tell whether a claim is disproved, untested, or independently reproduced under a new formulation; the rewriter can accidentally promote oracle or secondary-source claims to measured v2 evidence.
- **Required correction:** identify original claim, specified variant, current result and status separately. Use NOT TESTED for exact underspecified originals, REPRODUCED for specified revised values, and WITH DEVIATION where a named related experiment differs. Link this review's methods for the fixed-p50, bootstrap and B0 tie caveats. Clarify within-fold adjacent represented days versus calendar-adjacent days. State the six-arm population explicitly. Retain original numbers where material, labelled historical/unverified; do not silently replace their experiments.
- **Unknown:** original QRA/stacker/controller/width-driver/battery recipes and any unavailable prior scratch. This review does not require reconstructing them to begin bounded work.

### IR-08 — Low: correct two numeric descriptions without changing scope

- **Affected:** §§4.5–4.8 and 6. **Challenged text:** all three blocks have “roughly 5,800” rows at full history; “τ=.5 pinball is MAE.”
- **Evidence/method:** night 22–05 has 8 hours, solar 10–16 has 7, shoulder has 9: nominal 728-day counts **5,824 / 5,096 / 6,552** before DST/eligibility. By the loss formula, .5 pinball is **.5×absolute error**, so its mean is **MAE/2**; minimizing it is equivalent to minimizing MAE.
- **Consequence:** the approximation understates the capacity imbalance; literal loss-scale equivalence is incorrect in a document distinguishing metric grids.
- **Required correction:** use the block-specific nominal counts (or state the average approximation) and correct the pinball scaling in the plan only. Preserve unmeasured fit-time/half-gap expectations as estimates; do not edit Q&A. Keep the 67,343 versus 2,160-row scope distinction and the 95.83% leakage lesson as historical disclosures if retained.
- **Unknown:** actual per-block fit costs, losses and early-fold effective samples; no promised improvement follows.

## Pass B — Programme design

The plan is substantially better than the original as described in the earlier critique. It names engineering versus product status, leaves bars to the Owner, admits negative experiments, keeps the failed §8 screen, and does not promise a weather gain or browser-compatible neural model. Those strengths should survive. The intended outcome must nevertheless drive the next package: a research result, a causal evaluated candidate, and a qualified live forecasting product have different finish conditions.

### IR-01 — High: separate the three delivery routes and remove accidental gates

- **Affected:** §§2, 3.3, 4 sequencing, 4.0, 4.3, 4.10. **Challenged instructions:** “After §4.1's decision” seek the amendment; “authorize 4.1, resolve §3, then 4.0→4.2”; 4.10 depends on 4.3, whose final claims depend on 4.2.
- **Evidence/method:** dependency trace. Table 4.0 correctly qualifies admission as “for weather scope,” but prose makes it general. Existing CP-15 research content requires neither weather nor a new v2 candidate, yet its completion route is not explicit.
- **Consequence:** an irrelevant archive blocker can delay a cheaper existing-input test; an honest research release cannot clearly finish if v2 fails or is not built.
- **Required correction:** make weather admission conditional on weather scope everywhere. Define existing-evidence research content/handoff independently of 4.2 and 4.9, still subject to the Owner-approved research route and any authorized additive amendment needed by that route. Candidate evaluation must finish on validated positive, negative or blocked results; only the qualified route requires ratified feasibility, freeze and prospective evaluation. Distinguish local package completion from Owner publication, whose timing agents do not control.
- **Unknown/reserved:** which delivery the Owner wants first and whether any research release is authorized. **Recommendation:** next produce the decision-ready packet for one fixed v2 test; allow an existing-evidence content package alongside it when authorized. This does not select the product/bar for the Owner.

### IR-03 — Medium: use controls to test the cheapest decision-changing hypothesis first

- **Affected:** §§4.2, 4.4–4.6 and sequencing. **Challenged instruction:** combine a new central blend and hour-aware residual layer in v2, then a 64–120-hour weather/VRE package without an explicit internal decision boundary.
- **Evidence/method:** emitted blend .64466 differs from central blend .64070; causal interval performance is unknown. VRE generation adds labels, revisions and held-forward prediction construction before any measured causal weather gain. The current table requires direct-weather versus VRE comparison even though the prose calls VRE optional.
- **Consequence:** a result can be uninformative about what helped; the expensive intermediate model can become a de facto prerequisite.
- **Required correction:** in the bounded v2 protocol, include an otherwise identical pooled-residual control to identify the hour-aware layer's contribution, keeping this a declared control rather than a tuning sweep. For weather, place a fixed direct-weather paired ablation before optional generation modelling, with a result/cost-based stop or separately justified authorization for that extension. A failed direct-weather test does not prove all VRE representations useless. Resolve “optional VRE” versus mandatory comparison. Keep new architecture tests optional and independently admitted; no automatic replacement search on failure.
- **Unknown:** relative gains, causal calibration support and runtime. **Optional recommendation:** choose one of three-block LightGBM or DDNN for the first architectural test based on admission/resource evidence; do not settle that Owner-authorized candidate choice here.

### IR-07 — High before qualification: expose operational issuance and registry gates

- **Affected:** §§3.2–3.3, 4.7–4.10. **Challenged instruction:** 4.9 compresses freeze and ≥90 days of evidence, referring to future freeze/evaluation briefs without explicitly naming the intervening operational-run authority and registry verification.
- **Evidence/method:** unchanged `capstone_v21.md` §§9–10 requires exact registry versions/fingerprints checked before outcome access; CP-18 needs operational/publication authorization separately from CP-17 freeze. The plan does preserve failure reporting and the 90-day clock, which is correct.
- **Consequence:** a reader could treat elapsed time after a file freeze as sufficient, or start a live/public scorecard without its stage authority. Optional recombination after a “final” disposition could change the policy subsequently claimed as frozen.
- **Required correction:** make the internal sequence explicit: finish all admitted comparisons (including 4.8 when admitted), final disposition, qualified feasibility verdict, freeze/register initialization, separately authorized prospective issuance/scorecard, registry-bound evaluation, local release handoff. Name the failure/staleness accounting and policy-change restart rule; no retuning or live dashboard feedback may select a champion during confirmation. A new policy starts a new evaluation; the prospective analysis must specify what observation/monitoring is permitted. Keep Owner publication distinct from local artifacts throughout.
- **Unknown/reserved:** final bar, operational metrics, allowed update/monitoring rules, registry identities, issue infrastructure and release route. Do not amend the anchor or invent those values in the rewrite.

Confirmation-window claims were checked against partition metadata: April 8–September 6 is 152 dates including embargo, final calibration and spent v1 holdout; April 8–September 22 is 168 dates only when including the review date, beyond the snapshot cutoff. No new model's lack of consumption makes these unseen. September 7 onward is not automatically collected or reserved. Retrospective CP-15-derived work remains `development_post_selection`. The contamination disclosure must remain intact: the 90.9% economic bar was chosen after seeing 90.7–91.4% candidates and must not be adopted as written. A later exploratory confidence interval does not rehabilitate that choice. A new external rationale cannot erase already-seen outcomes; it can define a future evaluation.

The missing consequential operational assumption is **historical sample success versus live decision success**: missing weather/price days and provider version changes can occur precisely during difficult regimes. Do not silently condition the released policy's performance on clean-input days. IR-04/05/07 require a frozen fallback and outage accounting, not an unbounded reliability project.

## Pass C — Executability

Each current item has a named role, a deliverable and an effort range, and most have a negative-result finish. Those are real improvements. “Engineering Lead” is a future accountable role, not an appointed executor; authorized briefs must assign the executor and reviewer. The table below audits every scheduled item. All require their stated future authority; none is authorized by the plan itself.

| Item / executor | Deliverable, dependency and finish assessment | Acceptance/decision, resources, stop and artifact gap |
|---|---|---|
| 4.0 / Orchestrator | Decision sheet, additive amendment, brief; Owner §3 and weather admission only for weather. Can finish blocked. | 4–8 h + Owner latency. Must obtain candidate counts, exact bars, protocol and allowlisted paths. Owner suspension/ratification remains required; no agent-selected bar. IR-01/02. |
| 4.1 / future Lead under feasibility brief | Documentary + decoded-sample dossier, per-provider/fold ADMIT or NOT_ADMITTED; no new model. | 8–16 h, hard 16-active-hour stop is clear; transfers/registration/queues additional. Cap provider/sample/byte scope in the brief, define field/lead obligations and artifact path. IR-05. |
| 4.2 / future Lead | Fixed v2, full-grid predictions, report, reproducible package; depends on 4.0. Failure completes an experiment without promotion. | 24–40 h is an estimate, not a maximum. Freeze residual grid/inner-validation/seed/replay budgets and artifact paths. Set exact point/interval/uncertainty bars through Owner decision; add pooled-layer control. IR-02/03. |
| 4.3 / future Lead, Owner content acceptance | Narrative/tables/chart specifications with evidence links. Existing-evidence outline can start independently; candidate claims wait for 4.2. | 6–10 h plus Owner review. Split research content completion from v2 content. Set output destination and correction-round stop; no rendering or visual QA. IR-01/02. |
| 4.4 / future Lead | Origin-safe pipeline and paired ablation on matched inherited rows; 4.1 admission + 4.0 weather brief. Negative gain is completion. | 64–120 h; transfer/extraction time unbounded separately. Direct-weather first, optional VRE only with explicit continuation case; finite feature/model/seed budget, failure artifact and fallback. IR-02/03/05. |
| 4.5 / future Lead | Three-block challenger and raw/normalized disposition; authorized candidate set, not dependency of v2. | 12–24 h; no numeric capacity grid/search/refit cap. Raw and normalized arms must count against the budget. “No justified gain” requires the future exact bar. IR-02/08. |
| 4.6 / future Lead | One admitted joint-distribution family, quantiles/runtime/delivery report; admission + explicit candidate authority. | 24–48 h per family, admission ≤4 h; family cap helps but configurations, seeds, ensembles, failed admissions and fit-hours remain unbounded. No automatic family substitution. Define admission-failure artifact. IR-02. |
| 4.7 / Orchestrator | Final retained/reference/rejected/deferred record after the admitted set. | 2–4 h; must include 4.8 results if admitted or its explicit deferral. Point to one final candidate/evidence identity; no unreviewed recombination after disposition. IR-02/07. |
| 4.8 / future Lead | Fixed/estimated combinations on identical rows; any new admitted arm + frozen protocol. Negative result can finish. | 8–16 h; “freeze family/grid” lacks numeric search/fit caps and minimum gain rule. Make it opt-in and upstream of final disposition; name output and stop. IR-02/07. |
| 4.9 / future Lead with Orchestrator/Owner stage gates | Qualified freeze, issued-forecast lineage and ≥90-day evaluation; feasibility PASS + final disposition. | 16–24 h + ≥90 days; operator/incident effort and registry/stage authority not adequately allocated. Specify whether estimate includes maintenance and what occurs on outages/policy changes. No elapsed-time-only completion. IR-02/07. |
| 4.10 / future Lead; Owner lands/publishes | Runnable bundle/notices/evidence/review/handoff; research route or qualified 4.9 route. | 8–16 h + Owner time; local handoff can finish before publication. Name artifact destination and Owner action, not an agent promise of publication. Negative/research route must be reachable. IR-01/02. |

### IR-02 — High before model execution: ranges and “bounded” are not resource caps

- **Affected:** §4 table and §§4.2–4.8. **Challenged instruction:** call work executable with an effort estimate, “training-only selection,” and “no endless search,” while candidate/search counts and most stop limits are left to future protocols without item-level blockers.
- **Evidence/method:** audit above. Only archive's 16-hour stop and model admission's 4-hour limit are explicit maxima. The proposed v2 path arithmetic **60–102 active hours** is correct (4.0+4.2+4.3+4.7+4.9+4.10) but excludes the prose-mandatory 8–16-hour archive gate, prospective operating effort and optional experiments. If that gate were intentional the stated route would be **68–118 h** before those other additions.
- **Consequence:** estimates can expand into many models/feature recipes/seeds; no executor knows when to stop or where a negative result must be deposited. A dense table can conceal unresolved protocol work.
- **Required correction:** designate a genuinely bounded first packet; for subsequent conditional items name each still-required decision/brief field rather than imply readiness. Before any fits, require numeric configuration/seed/ensemble/feature-search counts, maximum fit/compute and active-effort budgets, budget-exhaustion disposition, inner-selection and outer-scoring freeze, exact deliverable paths and an accountable reviewer. Count controls, refits/warm-up and optional recombination. Do not invent Owner resource limits; make unresolved limits explicit blockers to the affected item only. Identify transfer/Owner/operational elapsed dependencies separately.
- **Unknown:** actual local compute throughput, storage and available human time. No new benchmarking or candidate work is authorized here.

The current plan measures **380 lines / 4,109 whitespace-delimited words** (`wc -l -w`), genuinely compact in its present form. The earlier review reports the previous draft as 644/6,056; that original version was not independently re-counted here. Relative to those reported counts, the rewrite is about 41% fewer lines and 32% fewer words. Its decisions-first layout helps. It still spends a large ledger on old-author/reviewer columns while putting essential stops in dense cells. Further arbitrary shortening is not required: make one readable first work packet, show conditional future work as such, and link detailed evidence. No stylistic redesign is necessary.

## Handoff boundary and completion record

All material findings **IR-01 through IR-08** require explicit disposition in the separate rewrite session. IR-08 is low severity but a straightforward factual repair. Preserve already-correct evidence, not merely the criticisms. The rewrite brief is **READY FOR TRANSFER AS A DOCUMENT-ONLY TASK**; it does not certify the programme ready for execution. No governance suspension is needed to edit this proposed, non-ratified plan under the Owner's transferred instruction. Any genuinely necessary locked-file change must be surfaced as a blocker for a separately authorized task, never performed by the rewriter.

Unverified: full archive admission/publication history and source decoding; all new candidate quality/cost/delivery; original unspecified experiments; controller illustration; €30 economics and €10 bootstrap; live trading realism; original criterion-5 oracle claim; v1 browser-size/parity and historical presentation diagnostics beyond the checks described. No reserved outcomes, model fitting, source changes, visual QA or Q&A edits were used to resolve these gaps.

Task file accounting:

- `docs/track-b/v3-plan-independent-review-2026-09-22.md` — this independent three-pass critique, verification methods and findings.
- `docs/track-b/v3-plan-rewrite-brief-2026-09-22.md` — complete bounded document-rewriter prompt addressing those findings.
- `.local/independent-review-2026-09-22/` — retained reproducibility/recovery packet, initial diagnosis, independent scripts, outputs, input/preservation hashes, Git accounting and full task diff. Ignored, not staged; no essential result exists only here. No disposable worktree/cache was created.

The pre-existing tree contains eight modified tracked files and four untracked files, including the reviewed plan and earlier review. These are not this task's edits. Their full list, final porcelain status, ordinary diff statistics and the full two-document addition diff are included in the local terminal handoff packet. Ordinary `git diff` omits these untracked new documents; their task diff must use `/dev/null` versus each file, not stage them to make them visible.

Proposed commit message: `docs: independently review v2/v3 plan and prepare bounded rewrite handoff`

Branches, worktrees and tags created: **none**. No staging, commits or publication. Interview-answer capture trigger: equivalent forecast-optimal storage dispatches produced different realized value, demonstrating why policy tie rules and estimands must be frozen. Named here only; no Q&A entry filed.
