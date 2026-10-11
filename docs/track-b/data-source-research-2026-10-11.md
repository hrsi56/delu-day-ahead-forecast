# B-Research Stage 3: external data for DE-LU price forecasting

Research and retrieval date: **2026-10-11 UTC** (local handoff may fall on 2026-10-12). Historical delivery window: **2019-01-01–2026-04-07**. Forecast origin: **D−1 11:00 UTC**, strictly before, for delivery day D in Europe/Berlin. This is desk research for CP-25, not a collection run or an admission verdict. Documentation, terms, schedules and bounded archive-coverage metadata were inspected. No forecast or market observations were collected, and no account, purchase, subscription, enquiry or form submission was made. Current pages support documentation and product metadata only; no post-cutoff market values, movements, charts or events are reported.

## 1. Summary and CP-25 priority

**Build the planned German wind and solar forecasts from the existing as-issued GFS runs.** No examined free external German power-forecast archive establishes original pre-origin forecasts throughout the required window. The strongest new early power-forecast lead is **Elia's Belgian 11AM wind forecast** (Europe/Brussels is inferred from dataset metadata); it can complement German fundamentals, not replace them. Its matching solar field starts too late for a full-window experiment. [Elia wind metadata][ELW], [Elia solar metadata][ELS], [ENTSO-E renewable item][E69]

CP-25 should work through this **conditional collection queue**, in order. First resolve each stated admission blocker; exclude a source from the strict backtest if it cannot supply original versions or evidenced availability. No new product is certified here as an unconditional F1–F5 pass.

1. **Elia Belgian `dayahead11hforecast`, wind:** a named early forecast field, CC BY 4.0, and coverage before 2019; verify preservation of the original 11:00 issues and the live schema. [ELW], [ELT]
2. **Individual neighbours' D−1 and older prices:** inexpensive cross-market information with clear SMARD/Energinet reuse; recover original corrections/arrival evidence, establish each zone's coverage and a supported daily route. Keep Poland's opening gap explicit. [SP], [ST], [ENOLD], [ENNEW], [ENT]
3. **ENTSO-E neighbour load forecasts, 6.1.B and separately 6.1.C:** expressly reusable items and early nominal deadlines; original forecast revisions and per-zone starts remain unverified. [LB], [LW], [ER]
4. **ENTSO-E pre-auction forecast NTC and final flow-based parameters, 11.1/11.1.B:** a promising reuse route separate from JAO's restrictive terms; verify owner exceptions, border applicability and original domains. Core is a partial-period source. [NTC], [FB], [ER], [JG]
5. **Optional TIGGE ECMWF weather ensembles:** a long original-run archive under CC BY 4.0, but 48-hour delayed access forces older runs; Owner registration, centre-specific coverage and arrival checks are needed. It is weather augmentation, not an external power forecast. [TG], [TGT], [TGF]
6. **ECB deposit-facility rate and lagged USD/EUR reference rate:** low-priority, low-cost state/context features; verify historical release versions through the direct ECB API. €STR is a separate partial-window candidate, beginning October 2019. [ECBAPI], [ECBT], [ECBFIRST], [ECBFX]

Hold **RTE D−2 French load, GIE storage/LNG inventories, generation outages, EIA Brent and EUA auctions** for precise archive/rights enquiries. Do not spend CP-25 on Yahoo, Montel-sourced Ember quotes, FRED/ALFRED ML use, direct JAO without permission, or a daily API2 search already lacking a qualifying route. Missing original versions are the main cross-family gap; free visibility does not establish redistribution. This ranking is a research judgement, not an estimated forecast improvement. [RT], [GIED], [OUT], [EIAT], [EIAD], [EUAA], [FREDT], [JT]

## 2. Admission rules and interpretation

**P** means documented pass for the stated part; **N** means a documented failure; **U** means **unverified**. F4 is deliberately stricter than observation coverage: a latest historical value is insufficient when earlier releases were revised. A nominal deadline supports F3's schedule, not actual historical arrival. A current collector can establish future arrival, but cannot manufacture past evidence.

Explicit AI/ML clauses were found in EEX DataSource v8, JAO restricted-area terms and FRED/ALFRED services/API terms. No AI-specific bar was identified in the inspected CC BY grants or ECB/GIE reuse terms; this does not waive other licence conditions. [EEXT], [JT], [FREDT], [ECBT], [GIED]

Licence classes: **(a)** raw redistribution permitted under the named licence/terms; **(b)** derived features only, with an explicit grant; **(c)** private/internal use only; **(d)** prohibited or unclear for this public forecasting repository. No examined restrictive product was established as class (b). A numerical aggregate or trained model does not automatically cure an upstream licence restriction. Keep third-party attribution and native terms with the inputs; the repository's CC BY 4.0 declaration cannot relicense rights the project does not own.

Use separate `issued_at`, `available_at`, `valid_from`, `valid_to`, `revision/status`, provider/product and retrieval fields. Initialisation, sender creation, delivery time, portal modification time and file-generation time are different clocks. Original `available_at` must be evidenced or expressly labelled reconstructed. Reject a release at exactly 11:00 UTC because the instruction is **before** the origin.

The fixed origin is after the summer SDAC gate at 10:00 UTC. **Flag releases in [10:00,11:00) UTC on D−1 in summer**, even if they satisfy this requested origin. There is no scheduled such hazard for Elia's 11AM forecast under the inferred Europe/Brussels timezone or Core's final 10:30 CET/CEST domain. Event-driven outage releases can fall in that interval. EEX auction PDFs use an ambiguous literal CET clock and require the flag until seasonal handling is resolved. [ELW], [JTIME], [OUT], [EUA18], [EUA24A], [EUA24B]

Use UTC intervals for 23/24/25-hour delivery days. Where a price or MW forecast has quarter-hour granularity, form the hourly feature from four complete duration-weighted quarters; missing constituents yield a missing hour. Do not assume all products remained hourly through the window: Energinet's successor starts at PT15M on 2025-10-01. Holidays, a solar night-time zero, no scheduled auction, an absent message and a missing measurement are distinct states. [ENNEW]

## 3. Master table

All documentation and terms links in this table and its reference register were retrieved **2026-10-11 UTC**. Shared labels reduce repetition without changing product-specific conclusions. **SP**: individual SMARD price, EUR/MWh, D−1/earlier only; the manual describes publication after the earlier auction and later updates. Actual original arrival/corrections remain unverified. **EE**: EEX public conditions do not establish an open database grant; DataSource v8 §3.2.3 requires an appropriate AI licence where that contract applies. **Annual U** means numerical missingness is unverified separately for every year 2019–2025 and 2026-01-01–04-07. [SP], [EEXUSE], [EEXT]

### 3.1 Early power forecasts and weather

| Family | Provider and exact product | Documentation / terms | F1 free / auth | F2 evidence | F3 evidence | F4 evidence | F5 legal daily route | Publication time against origin | History / granularity / vintages | Class | Expected missingness | Caveats |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Wind | Elia `ods031`, `dayahead11hforecast`; live `ods086` | [ELW], [ELRTW], [ELT], [ELAPI] | P; anonymous | P; Elia licence incorporates CC BY 4.0 | Named 11AM issue; timezone inferred, arrival U | U; named early field, no revision history | P anonymous API; original live-field preservation U | 11AM; assuming dataset Europe/Brussels: 10:00 UTC winter / 09:00 summer D−1 | First non-null valid interval 2015-08-12 local; MW/PT15M; issue immutability U | a | 288 null intervals/category in 2019; 96 in 2021; other examined years none by aggregate count | Belgian, not German; see dossier and count evidence |
| Solar | Elia `ods032`, `dayahead11hforecast`; old live `ods087` | [ELS], [ELRTS], [ELT], [ELHOME] | P; anonymous | P; CC BY 4.0 | Named 11AM issue; timezone inferred, arrival U | N full window | U; successor schema needs verification | Same inferred Europe/Brussels 11AM clock | First non-null valid interval 2020-10-01 local; MW/PT15M; original revisions U | a | 2019 and 2020 through September structurally unavailable | Partial-window only; product migration metadata is not proof of continuity |
| Wind/solar | ENTSO-E A69 / A01, fixed 14.1.D | [E69], [ER], [EGTC] | P; registered token | N blanket CC BY assumption | N | U | Technical XML route; legal U | 18:00 Europe/Brussels D−1 = 17:00/16:00 UTC | MW/MTU; fixed latest pre-18 snapshot, original 2019 retention U | d | Annual U | Reject late issue |
| Wind/solar | ENTSO-E A69 / A18 current, 14.1.D | [E69], [ER], [EREST] | P; token | U; generation item omitted | U; every submission, no early guarantee | U; complete original versions not established | Technical XML; legal U | Event/update-dependent; clock U | MW/MTU; current latest is not an original archive | d | Annual U | Early +2 may exist; enquiry only |
| Wind/solar | ENTSO-E A69 / A40 fixed intraday, 14.1.D | [E69], [ER] | P; token | U | N | U | Technical XML; legal U | 08:00 Europe/Brussels **on D** = 07:00/06:00 UTC on D | Delivery-day snapshot, too late for D−1 origin | d | Annual U | Do not confuse D with D−1 |
| Wind | 50Hertz following-day wind forecast | [50W], [50T] | Public free; auth U | N/U; prior written consent | N under local-clock interpretation | U | Consent needed for automation | Snapshot 09:00, public 18:00 D−1; timezone U; if Berlin, 17:00/16:00 UTC public | MW/PT15M; eight-day internal horizon does not establish public +2 | d | Annual U; `n.v.` missing | Separate issue calculation from publication |
| Solar | 50Hertz following-day PV forecast | [50P], [50T] | Public free | Same consent restriction | Same late public release | U | Consent needed | Same 09:00 snapshot / 18:00 public; timezone U | MW/PT15M; first original forecast start U | d | Annual U; night zero can be valid | No early public +2 archive proved |
| Wind | TenneT actual/forecast wind feed-in | [TW] | Public free; auth U | U | N if local clock | U | Supported legal API U | Snapshot 08:00, public 18:00 D−1; timezone U | MW/PT15M on/offshore; original start U | d | Annual U | Publication clock distinct from label |
| Solar | TenneT actual/forecast solar feed-in | [TP] | Public free | U | U | U | U | Clock/timezone U | Archive start/native resolution/original issues U | d | Annual U | Do not import wind's schedule into PV |
| Wind | Amprion Wind Feed In, 08:00 forecast | [AW] | Free CSV/ZIP page | U | U; snapshot label only | U | Stable legal API U | 08:00 Uhr label; timezone/available_at U | MW; page distinguishes pre/post 2008-04-01 records; original start U | d | Annual U | No proven +2 publication |
| Solar | Amprion Photovoltaic Infeed | [AP] | Public free | U | U; future-day issue not proved | U | U | Clock/timezone U | Short-term estimate of actual supply from reference plants | d | Annual U | Cannot classify as an archived day-D forecast |
| Wind | TransnetBW wind Vortagesprognose | [BW], [BWD], [BT] | Public free | U; consent to duplicate | U | U | Legal API U | Previous-day issue; exact clock/timezone U | MW/control area; original start U | d | Annual U | Definition alone does not establish early arrival |
| Solar | TransnetBW PV Vortagesprognose | [BW], [BPD], [BT] | Public free | U; consent to duplicate | U | U | Legal API U | Clock/timezone U | MW/control area; original start U | d | Annual U | Same unresolved gates |
| Wind | netztransparenz old wind forecast | [NZ], [NZT] | Public free | U; written consent | U | N full window | N discontinued | Clock/timezone U | Ends 2022-12-15; excludes direct marketing | d | After end structural absence; earlier Annual U | Not national total wind |
| Solar | netztransparenz old solar forecast | [NZ], [NZT] | Public free | Same | U | N | N | Clock/timezone U | Same end/scope | d | Same | Do not splice unlike scopes silently |
| Wind/solar | netztransparenz current Vermarktungsprognose | [NZ], [NZT], [NZAPI] | Page free; API registration U | U | U | U | Exact legal endpoint U | Clock/+2 horizon U | TSO marketing quantity; full 2019 original history U | d | Annual U | Replacement is a different product |
| Wind/solar | Energy-Charts `/public_power_forecast`, country=de, current/intraday/day-ahead | [ECAPI], [ECSPEC], [ECNOTE], [ER] | P anonymous | U; API CC BY claim vs primary-owner scope unresolved | U | U | JSON API, legal provenance U | Labels/valid Unix time do not prove issue clock | Original start, old versions/as-of selector not established | d | Annual U | Wrapper cannot establish upstream rights/vintages |
| Load | Energy-Charts `/public_power_forecast`, load | [ECAPI], [ECSPEC] | P anonymous | Conditional CC BY item provenance | U | U | JSON API | Exact available_at U | Original 2019 issues U | a conditional | Annual U | Prefer attributable primary load item |
| Wind/solar | Energy-Charts `/v2/public_power_forecast`, week-ahead | [ECSPEC], [ECAPI] | P anonymous | U | U | U | JSON API, provenance U | Enum/horizon is not publication evidence | API launch is not archive start; `generated_at` not old arrival | d | Annual U | No established +2 full-window archive |
| Load | RTE Consumption v1.2 `short_term`, type=D−2 | [RTE], [RT] | Public API; OAuth registration; explicit free tariff U | Public reuse with attribution; feature-modification scope U | Schedule promising; actual U | U; past forecasts, not all revisions proven | Documented JSON/OAuth; conditional rights/registration | Recommended retrieval ~07:00, timezone U; if Paris, 06:00/05:00 UTC; not a release deadline | Since 2012-12-17; MW/PT30M; `updated_date`, default latest | d until feature rights clear | Annual U | Genuine +2 route, not admitted yet |
| Load | RTE Consumption `weekly_forecasts` | [RTE], [RT] | OAuth; tariff U | Same | U exact clock; valid D+3…D+9 | U | JSON/OAuth conditional | No new weekend issue; exact clock U | Since 2004-12-23 per guide; update-dated forecasts; product fields differ | d | Weekend non-issue intentional; Annual U | Cannot assume original issue completeness |
| Weather | DWD operational ICON open forecasts | [DWD], [DWDT] | P anonymous HTTP | P; CC BY 4.0, third-party exceptions | Run clock ≠ arrival; U | U; live feed not retained full-window proof | P open GRIB2 feed | Exact dissemination U | Open service July 2017; original archived 2019 access U | a | Annual U | Useful live weather, not proven historical replacement |
| Weather | DWD PAMORE ICON forecast archive | [PAM], [DWTUT], [DWDT] | Free qualifying institutions; registration, individual eligibility U | Conditional CC BY geodata | ≥48h old access; actual arrival U | N public retention | Archived extraction route; separate live feed | Old-run delay, exact upload U | Public forecast retention about 1.5 years; internal ICON archive since 2015-01-20 | a conditional | Older requested period outside retention | Internal storage is not public access |
| Weather | ECMWF operational open IFS/AIFS | [MW], [MWT] | P anonymous subset | P CC BY 4.0 + terms | Exact arrival U | N rolling retention | P HTTP/cloud | UTC initialisations; dissemination distinct | About 12 runs / 2–3 days; GRIB2 | a | Requested older runs absent from rolling feed | Does not backfill 2019 issues |
| Weather | ECMWF historical MARS operational archive | [MARS], [MWORDER] | Cost/waiver U; service agreement | Agreement-specific U | U arrival | Selected fields/start U | Agreement route | Original run clock does not prove access time | Operational archive exists; free full-window access U | d | Annual U | Owner purchase/waiver decision |
| Weather | TIGGE ECMWF centre `ecmf`, original ensembles | [TG], [TGT], [TGF], [TGAPI] | P after free registration/licence acceptance | P selected centre CC BY 4.0 | Schedule P, arrival U | Programme covers period; centre completeness U | P ECDS/CDS API after registration | Public 48h after init; D−3 00:00 UTC eligible D−1 00:00 UTC by schedule | Programme October 2006; six-hour leads, GRIB2; model versions change | a | Known surface-control loss across 710 dates 2006–2019; 2019 subset U | Weather only; do not mix NC-licensed centres |
| Weather | Open-Meteo single full runs | [OMS], [OMT] | Free hosted noncommercial; commercial subscription | Data CC BY 4.0; service restrictions | Init not observed arrival | N 2019 original window | Hosted terms conditional for product | Indicative processing delays only, actual U | IFS 2024-03-14 described as hindcasts; other full-run models 2026-04-02 | a data | Before starts structural absence | Hindcast is not original issue |
| Weather | Open-Meteo previous runs | [OMP], [OMT] | Same service terms | Same | Fixed lead ≠ full original run | N full-window multi-input coverage | Conditional hosted route | Historical arrival U | Mostly January 2024 onward; earlier variable/model exceptions do not establish whole window | a data | Before start structural absence | No substitute for complete issues |
| Weather | Open-Meteo stitched historical forecast | [OMH], [OMT] | Same | Same | N requested issue semantics | N original full-run semantics | API exists | Stitched successive short leads | Some IFS history since 2017 is stitched, not a D−1 issue archive | a data | Different product, not simple gaps | Reject; reanalysis also excluded |

### 3.2 Neighbours, links and outages

The eleven price rows are individual zones; avoid a changing neighbour-average basket. Swiss prices are requested lagged neighbour information; verify the Swiss product's own auction schedule rather than declaring it a member of SDAC. For the load and capacity rows, enumerate only real border/area combinations in CP-25. [SP]

| Family | Provider and exact product | Documentation / terms | F1 | F2 | F3 | F4 | F5 | Publication time against origin | History / granularity / vintages | Class | Expected missingness | Caveats |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Price | SMARD SP: AT | [SP], [ST] | P no account | P CC BY 4.0 | Lag schedule P; arrival U | U original versions | Supported daily API U | Earlier auction; SP | AT split 2018-10-01; native price MTU | a | Annual U | Zone definition predates window; coverage unverified |
| Price | SMARD SP: CH | [SP], [ST] | P | P | U exact Swiss clock | U | U | Earlier auction; clock U | Exact series start U | a | Annual U | Separate Swiss schedule |
| Price | SMARD SP: FR | [SP], [ST] | P | P | SP | U | U | SP | Start/original revisions U | a | Annual U | D−1/earlier only |
| Price | SMARD SP: NL | [SP], [ST] | P | P | SP | U | U | SP | Start/original revisions U | a | Annual U | D−1/earlier only |
| Price | SMARD SP: BE | [SP], [ST], [SBE] | P | P | SP | U | U | SP | Price history documented to 2015; originals U | a | Annual U | Catalogue addition date ≠ price start |
| Price | SMARD SP: DK1 | [SP], [ST] | P | P | SP | U | U | SP | Start/original revisions U | a | Annual U | Energinet alternative |
| Price | SMARD SP: DK2 | [SP], [ST] | P | P | SP | U | U | SP | Start/original revisions U | a | Annual U | Energinet alternative |
| Price | SMARD SP: PL | [SP], [ST] | P | P | SP | N opening window | U | SP | Missing through 2019-11-19, currency-related | a | Known opening gap; later Annual U | Do not fabricate euro prices |
| Price | SMARD SP: CZ | [SP], [ST] | P | P | SP | U | U | SP | Start/original revisions U | a | Annual U | D−1/earlier only |
| Price | SMARD SP: NO2 | [SP], [ST], [SBE] | P | P | SP | U | U | SP | History documented to 2015; originals U | a | Annual U | NO2, not all Norway |
| Price | SMARD SP: SE4 | [SP], [ST] | P | P | SP | U | U | SP | Start/original revisions U | a | Annual U | Energinet alternative |
| Price | Energinet `Elspotprices`, DK1/DK2/NO2/SE4 | [ENOLD], [ENT], [ENAPI] | P anonymous | P CC BY 4.0 | Earlier-delivery lag; original arrival U | U per-zone original history | P via successor | Exact old release clock U | Catalogue 1999-07-01; hourly through 2025-09-30; no issue/version fields | a | Annual U | Catalogue start ≠ every zone's start |
| Price | Energinet `DayAheadPrices`, DK1/DK2/NO2/SE4 | [ENNEW], [ENT], [ENAPI] | P anonymous | P | Lagged only | N alone; combine old product | P JSON/CSV API | Suggested tomorrow polling 13:00–14:00 CET; seasonal notation U | Starts 2025-10-01; EUR/MWh/PT15M; TimeUTC/TimeDK | a | Annual U after start | Ignore tomorrow/D prices |
| Price | ENTSO-E Energy Prices 12.1.D, requested zones | [PRICE], [ER], [EGTC] | P token | U; omitted from CC BY list | Lagged arrival U | U | Technical P, legal U | Exact original clock U | Variable MTU; no version field in file schema | d | Annual U | Prefer separately licensed route |
| Load | ENTSO-E 6.1.B A65/A01, requested eleven neighbour areas | [LB], [LS], [ER], [EREST] | P registered token | P exact item CC BY, exclusions | Deadline P for noon local gate; actual U | U original revisions | P XML; as-of retrieval U | Two hours before gate: 10:00 CET/CEST = 09:00/08:00 UTC | MW/native MTU; per-area starts U | a | Annual U | Confirm zone-specific gates, including CH |
| Load | ENTSO-E 6.1.C A65/A31, same areas | [LW], [ER], [EREST] | P token | P item-scoped | Nominal early; exact zone U | U original revisions | P XML; versions U | Friday W−1, two hours before gate; 14:00 local if no gate | Daily min/max MW; optional finer MTU; starts U | a | Annual U | Separate coarse feature, not hourly interpolation |
| Capacity | ENTSO-E forecast day-ahead transfer capacity 11.1 / A61 | [NTC], [NTCS], [ER] | P token | P listed item, owner exclusions | Deadline P; arrival U | U originals | P technical/legal item route | One hour before gate: 11:00 CET/CEST = 10:00/09:00 UTC | Directional MW/native MTU; optional; UpdateTime UTC | a | Annual U; topology absence distinct | Only valid pre-auction D forecasts |
| Capacity | ENTSO-E final pre-auction flow-based parameters 11.1.B | [FB], [FBS], [ER] | P token/file access | P listed item, exclusions | Deadline P; actual U | U region/vintages | P API/file; exact history U | One hour before gate, as above | RAM MW/PTDF/CNEC; region/schema changes | a | Core pre-June 2022 absent; others U | Final input domain, not coupling output |
| Capacity | JAO Core initial virgin domain | [JH], [JT], [JG] | Public view free; API auth U | U/restricted; ML permission needed | Nominal early; arrival U | N full window | Legal automation U | 01:15 D−1; initial winter clock convention U | Core delivery begins 2022-06-09; old arrivals U | d | 2019–2021 and early 2022 absent | Preliminary ≠ final domain |
| Capacity | JAO Core final domain, Max Exchanges, D2CF | [JH], [JT], [JTIME], [JG] | Same | Same | Schedule P; actual U | N full window | Legal automation U | 10:30 CET/CEST D−1 = 09:30/08:30 UTC | Same Core start; original arrival U | d | Same | Not a 10–11 UTC summer publication |
| Outage | ENTSO-E generation/production 15.1.A/B/C/D, DE and neighbours | [OUT], [OUTS], [ER], [FMS], [EPARAM] | Free token/login | U; item absent from reuse list | Version clock capable; event-driven | U all versions since 2019 | Technical P; legal U | H+1 reporting after decision/change; VersionPublicationTimestamp UTC | MW/unit/event; Version,OldVersion,Status and publication fields | d | Annual U; thresholds/silence ≠ zero | REST update query returns latest revision only |
| Outage | EEX UMM non-usability generation, DE | [EEXUMM], [EEXDISC], [EEXAPI], [EEXT] | Free web; paid API | Private/permission; AI clause | Event-driven actual timestamps in paid route | N free window; all versions U | N free legal API | Immediate; API publication/modification UTC fields | Free rolling five years; full 2019 not available now | c/d | Annual U | Written public/ML licence and version archive needed |

### 3.3 Fuel and carbon

| Family | Provider and exact product | Documentation / terms | F1 | F2 | F3 | F4 | F5 | Publication time against origin | History / granularity / vintages | Class | Expected missingness | Caveats |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Gas | EEX TTF Day EGSI | [EGSI], [EEXFAQ], [EEXUSE], [EEXT] | Free view; paid full API | EE | N ordinary D−1 trading-day result under documented method; historical exceptions U | N free window | Paid route; free legal U | 2021 method:08:00–18:00 CET on preceding exchange trading day; end17:00 UTC literal,16:00 ifCEST; DST convention U | Daily index; free indices ≤1 year; originals U | d | Trading calendars; Annual U | Older published lag could be causal if licensed |
| Gas | EEX THE Day EGSI | Same | Same | EE | Same | N as THE since 2019 | Same | Same window | THE begins 2021-10-01 from NCG/GASPOOL merger | d | Merger/holidays; Annual U | Predecessors must be explicit |
| Gas | EEX TTF Neutral Gas Price, provisional vs final | [NGP], [EEXUSE], [EEXT] | Free final CSV/view | EE | Provisional arrival U | N 60-day final history | Legal snapshots U | Every15min; exact refresh timezone U; final after gasday | Gas-day provisional D/D+1/D+2; free final last60 days | d | Trade/version-dependent; Annual U | “+2” does not supply retained provisional issues |
| Gas proxy | THE preliminary daily imbalance prices | [THE], [THES], [THET] | Public XML; auth U | Written consent | Clock/arrival U | N explicitly not historicised | Technical XML; legal U | Hourly; timezone U | Provisional D−1…D+1 only | d | Annual U | Not a TTF quote |
| Gas proxy | THE VTP/final imbalance prices, NCG/GASPOOL predecessor archives | [THE], [THES], [THET], [THENC], [THEGP] | Public XML/archive | Consent U | First release U | U originals; THE2021 start | Technical XML; legal U | Clock/timezone U | EUR/MWh/gasday; predecessor products distinct | d | Annual U | Final is not past provisional value |
| Gas proxy | Bundesnetzagentur THE day/month-ahead presentation | [BNG] | Free page | Upstream EEX rights U | Clock U | U | N not machine-readable | Weekday update; clock/timezone U | Presentation, no original-vintage route proved | d | Weekends plus Annual U | Official presentation ≠ reuse grant |
| Gas proxy | ACER DES Spot EU LNG assessment | [ACERSTART], [ACERTIME], [AEGIS] | Public report; access U | U exact database grant | Deadline after origin; actual first release U | N starts 2023 | Legal API U | By18:00 CET working day; literal17:00 UTC, DST U | Daily LNG, not TTF/THE | d | Working days/transaction sufficiency | Outside full-window scope |
| Gas | Ember TTF/THE settlement input | [EMBER], [EMBEROLD] | Free presentation | Montel sourcing; contract U | U | U | U legal API | Clock/timezone U | Original quote/roll issues U | d | Annual U | Footer licence not upstream permission |
| Coal | Ember front-month API2 Rotterdam input | [EMBER] | Same | Same | U | U | U | U | Contract/roll originals U | d | Annual U | Not verified open API2 |
| Carbon | Ember front-December EUA input | [EMBER] | Same | Same | U | U | U | U | Annual roll/source vintages U | d | Annual U | No derived-only grant proved |
| Gas | Yahoo Finance TTF candidate, ticker unverified | [YAHOO] | Free view; authorised API U | Redistribution prohibited | U | U | U permitted route | U | Exact contract/start U | d | Annual U | Reject unofficial scraping |
| Oil | EIA Europe Brent Spot FOB `PET.RBRTE.D` | [EIAD], [EIAH], [EIAT], [EIAAPI] | Free; key registration | U private-source exception | Exact first release U | U original releases | Stable API, conditional rights/key | EIA clock/timezone U; observation date insufficient | USD/barrel daily; observations begin 1987-05-20; sourceRefinitiv/LSEG | d | Non-trading days; Annual U | Government host ≠ all-source public domain |
| Oil archive | ALFRED `DCOILBRENTEU` | [FREDT], [FREDV], [FREDOBS], [ALFRED] | Free; API key | N current ML restriction | Date-only vintages, subday U | Original vintage completeness U | N legal ML route | Vintage date, not arrival UTC | Release metadata since 2011-04-06; daily Brent | d | Annual U | Reject despite helpful vintage API |
| Coal proxy | World Bank Pink Sheet Coal(Australia) | [WB], [WBT], [WBH], [WBREV], [WBTIME] | P no account files | Default CC BY4, source exceptions | Monthly release clock U | N daily; originals U | Monthly files only | Second business day/month; timezone/clock U | USD/tonne monthly; dataset1960 onward, coal-specific start U | a conditional | Intentional monthly frequency; Annual U | Low-priority monthly experiment only |
| Coal proxy | World Bank Coal(South Africa) | Same | Same | Same | Same | Same; estimates revised | Same | Same | USD/tonne monthly | a conditional | Estimates/revisions; Annual U | Not API2 |
| Gas proxy | World Bank Natural gas(Europe) | [WB], [WBT], [WBREV], [WBDEF] | Same | Same | Same | N daily/original latest table | Monthly only | Same | Monthly regional composite; definition continuity U | a conditional | Monthly/estimates; Annual U | Not exact TTF |
| Carbon proxy | EEX EUA primary-auction spot report | [EUAA], [EUA18], [EUA24A], [EUA24B], [EEXFAQ], [EEXUSE] | Free report/ZIP | U open raw/features grant | Intended early, arrival U | Observation archive long; originals U | Public files; legal automation U | ~11:10 CET vs~11:05 CET PDFs; FAQ11:00 CE(S)T; see dossier | EUR/allowance/auction;2012–2025 archive plus2026 report metadata | d | Non-auction days/cancellations; Annual U | Primary auction ≠ secondary market |

### 3.4 Financial indicators, storage and hydro

| Family | Provider and exact product | Documentation / terms | F1 | F2 | F3 | F4 | F5 | Publication time against origin | History / granularity / vintages | Class | Expected missingness | Caveats |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Rates | ECB deposit facility `FM.D.U2.EUR.4F.KR.DFR.LEV` | [ECBDFR], [ECBAPI], [ECBT], [ECBDEC] | Free direct API; no key documented | P ECB attribution/modified-data terms | Last published decision only | U release-version audit | P SDMX/CSV API | Decision13:45 CET before 2022-07-21,14:15 CET thereafter, both too late for same origin | Daily policy-state %, from 1999; announcement/effective dates distinct | a custom | Changes sparse; weekends valid carried state; missing releases U | Use only announcements already public; distinguish current and announced-future rates |
| FX | ECB USD/EUR `EXR.D.USD.EUR.SP00.A` | [ECBFX], [ECBAPI], [ECBT] | Same | Same | Prior release only | U originals | P direct API | Around16:00 CET since 2016-07-01; literal15:00 UTC,14:00 ifCEST; both late | Daily business-day USD perEUR, fromJan 1999 | a custom | Business-day release calendar; Annual U | Snapshot14:15 CET is not publication |
| Rates | ECB €STR `EST.B.EU000A2X2A25.WT` | [ECBQA], [ECBFIRST], [ECBAPI], [ECBT], [ECBMETH] | Free, no licence fee | P custom attribution | Schedule P; actual exception U | N Jan–Sep 2019 | P direct API | Normally08:00 CET; correction09:00 CET; broader methodology bounds09:00/11:00 CET | First 2019-10-02 for 2019-10-01transactions; final after correction window | a custom | TARGET nonpublication days intentional | Pre€STR uses revised data; no causal backfill |
| Yield | Bundesbank10 year current federal security `BBSSY.D.REN.EUR.A630.000000 WT1010.A` | [BBY], [BBAPI], [BBT], [BBWEB] | Free API; key/rate U | Own ESCB stats reusable; third-party provenance U | Clock/arrival U | Start/original issues U | P technical API; exact rights U | Timezone/first release U | Daily %p.a.; security roll/composition matters | a conditional | Trading days; Annual U | Observation date does not establish origin knowledge |
| Rates | EMMI Euribor, requested tenor would need specification | [EMMIT], [EMMIMETA] | Free last25day view; licensed histories | N public project grant | Exact clock U here | N free full history | N free open-product route | Clock/timezone U | Historic/derived external licences required | c/d | Business days; Annual U | Registration/subscription Owner-only |
| Volatility | STOXX/DAX VDAX-NEW `V1X` | [STOXXT], [STOXXHELP] | Public view; full history licensed | N private/noncommercial view-only terms | Closing-release arrival U | N free history | N unlicensed automation | Clock/timezone U | Index points; public history ~3months | c/d | Exchange days; Annual U | Derivatives/models/redistribution need licence |
| Volatility | STOXX VSTOXX `V2TX` (V2X family) | [STOXXT], [STOXXHELP] | Same | Same | U | Same | Same | U | Implied euro-area volatility index | c/d | Exchange days; Annual U | No qualifying free equivalent identified |
| Storage | GIE AGSI+, Germany aggregate and facility records | [GIED], [GIEAPI], [GIETIME] | Free API; Owner key registration | P custom reuse/attribution | Prior published run only; arrivals U | U historical versions; revisions allowed | P JSON/key after registration | Processing19:30 CET and23:00(second timezone unspecified); DST U | Daily TWh stock/GWh-d flows; requests back 2011, facility-dependent starts, some 2016-04-07 | a custom | StatusE/C/N; annual actual gaps U | Gasday is valid interval, not issue time |
| LNG | GIE ALSI, EU/country terminal stock/send-out | [GIED], [GIEAPI] | Same | Same | Same prior-run condition | U historical versions | P JSON/key | Same documented processing convention | Daily GWh stock/GWh-d flow; requested history 2012, coverage U | a custom | Provider gaps/status, Annual U | Not a daily hub-price replacement |
| Hydro | NVE weekly reservoir levels, NO2/other areas | [NVE], [NVE 2019], [NVEMETHOD], [NVESPEC] | Anonymous documented API | P NLOD, compatibleCCBY3.0Norway | Prior published report only | U originals/full 2019 | P JSON/XML API | Wednesday13:00; timezone U; ifOslo=12:00UTCwinter/11:00summer, excludes new issue | Weekly fillfraction/GWh; public route 2019-04-08, older series coverage U | a NLOD | Holidays shift release; Annual U | New API start ≠ original series start |

## 4. Admission dossiers for the collection queue

These are specifications for a future authorised collector. Proposed imputation rules are research recommendations. They are not provider guarantees and do not permit collection before legal or account conditions are met.

### 4.1 Elia early Belgian wind

**Product.** `ods031.dayahead11hforecast`, MW, Belgian grid, PT15M; keep region, on/offshore and grid-connection category. Schema gives the interval start in UTC for API/downloads and local display time. The five disjoint categories found in the bounded coverage query are Federal/offshore/Elia; Flanders/onshore/DSO; Flanders/onshore/Elia; Wallonia/onshore/DSO; Wallonia/onshore/Elia. Do not combine overlapping totals and components. The first non-null interval is 2015-08-12 local; that proves stored coverage, not immutable issue preservation. [ELW], [ELCOUNTSTART]

**Vintage contract.** The field says published at 11AM; interpreting that as Europe/Brussels follows the dataset timezone metadata, but the publication-clock linkage is **inferred**, not explicit. Confirm the timezone before admission. Valid end follows the resolution. The historical schema supplies neither issue-specific `available_at` nor old revision/status fields. Require Elia to confirm that this named field retains the original 11:00 release, how corrected issues are represented and whether publication delay logs exist. Retain actual future first-seen time and payload hash from live `ods086`. Never use `mostrecentforecast` or an overwritten `weekaheadforecast` as an earlier issue. The 18:00 field is late. [ELW], [ELRTW]

**Missingness evidence.** Only bounded aggregate counts were requested; no forecast MW values were returned. Each of the five categories had the following counts. Counts cannot detect a missing timestamp replaced by a duplicate; CP-25 must check unique keys and original issues. Full years use Europe/Brussels boundaries; 2026 ends after local 2026-04-07. [Primary query recipe][ELQ], [durable count responses](research/stage3-elia-coverage-metadata-2026-10-11.json)

| Year | Expected PT15M intervals/category | Stored rows/category | Non-null 11:00 field/category | Null field/category |
|---|---:|---:|---:|---:|
| 2019 | 35,040 | 35,040 | 34,752 | 288 |
| 2020 | 35,136 | 35,136 | 35,136 | 0 |
| 2021 | 35,040 | 35,040 | 34,944 | 96 |
| 2022 | 35,040 | 35,040 | 35,040 | 0 |
| 2023 | 35,040 | 35,040 | 35,040 | 0 |
| 2024 | 35,136 | 35,136 | 35,136 | 0 |
| 2025 | 35,040 | 35,040 | 35,040 | 0 |
| 2026  through 04-07 | 9,308 | 9,308 | 9,308 | 0 |

**Rule.** Aggregate only complete disjoint components from the same early issue. Calm-wind zero is valid; null is not zero. An older forecast may fill only if it explicitly covers D and was available before origin. Otherwise retain missing/age flags and use a training-fold-only fallback, including the project's own GFS model. Do not repair early-field nulls using the evening or current curve.

**Coverage, rights and retrieval.** Raw/derived redistribution is permitted by the Elia CC BY 4.0 licence with Elia attribution; no AI-specific restriction was identified in that licence. Original-vintage confirmation is still required. Anonymous GET `https://opendata.elia.be/api/explore/v2.1/catalog/datasets/ods031/records` supports bounded filters and JSON; documented export routes can serve CSV/JSON. Live wind dataset `ods086` has the same named field. Numerical quotas are **unverified**; follow published API limits/429 handling when CP-25 verifies them. Solar `ods032` is excluded from the full-window queue because its 11:00 field starts 2020-10-01; its announced successor schema also needs checking for a later partial-window experiment. [ELT], [ELAPI], [ELRTW], [ELCOUNTSTARTS], [ELHOME]

### 4.2 Lagged neighbour prices

**Product.** Individual auction prices in EUR/MWh for AT, CH, FR, NL, BE, DK1, DK2, PL, CZ, NO2, SE4, for delivery **D−1 and earlier**. Keep zone identity and native intervals; do not use the changing SMARD mean basket. Prefer Energinet's documented API for its four areas and separately licensed SMARD prices for the rest, subject to a supported daily SMARD route. Starts are in the table; unverified starts require CP-25 confirmation. [SP], [SBE], [ENOLD], [ENNEW]

**Vintage.** Energinet old delivery fields are HourUTC/HourDK/PriceArea; successor fields TimeUTC/TimeDK/PriceArea. Neither schema establishes daily first publication or old corrections. SMARD's latest downloadable history is also insufficient to prove original corrections. Require original-publication evidence or documented finality before treating an earlier auction value as immutable. Keep historical correction timestamps; never use a later correction at an earlier origin. [ENOLD], [ENNEW], [SP]

**Missingness.** Annual counts are unverified for all eight requested year bins. Poland's 2019-01-01–11-19 gap is documented; no annual numerical completeness is claimed for other zones. Auctions are not absent merely because a day is a weekend or holiday. UTC conversion must preserve repeated autumn hours and the absent spring local hour. [SP]

**Rule.** Use the newest known earlier-delivery result; enforce `delivery_day < D` even if an API defaults to tomorrow. For isolated absence, a predeclared last-known same-zone carry-forward can supply a feature with age/missing flags; retain the original missing cell. Do not bridge Poland's long opening gap with another country's price. Use complete quarter-hours for hourly aggregation after the product change.

**Rights/retrieval.** SMARD and Energinet permit CC BY 4.0 use, attribution and adaptation. Energinet anonymous GET `https://api.energidataservice.dk/dataset/{Elspotprices|DayAheadPrices}` returns JSON/CSV; follow date-bound/timezone guidance, pagination, caching and 429 handling. Dataset-specific limits rather than a common numeric quota are documented; successor metadata suggests five-minute polling during its update window. SMARD documents download access, but a supported legal daily API was not established in this research. That is an F5 blocker, not permission to rely on an undocumented endpoint. [ST], [ENT], [ENAPI], [ENNEW], [SP]

### 4.3 Neighbour load, ENTSO-E 6.1.B and 6.1.C

**Product.** Total-load forecast MW in each requested neighbour area. Day-ahead 6.1.B/A65/A01 has native MTU intervals; week-ahead 6.1.C/A65/A31 supplies daily extrema, with optional finer data. Per-area first dates are unverified. Platform operation since 2015 does not demonstrate complete item/area coverage. The nominal day-ahead deadline for a noon CET/CEST gate is 09:00/08:00 UTC D−1. [LB], [LW]

**Vintage.** Preserve XML document identity/revision/creation time where supplied; creation is not platform availability. The file schema has valid UTC time, resolution, area, TotalLoad and UpdateTime, but no old-version publication field. GUI value history exists; complete programmatic original versions since 2019 remain unverified. Significant forecast revisions can make today's historical reply unsuitable for a past origin. [LS], [EHISTORY]

**Missingness/rule.** All eight annual bins are unverified; absence differs from zero load or a holiday. Choose the last actual pre-origin version covering D. An older issue can substitute only within its explicitly valid horizon. Never relabel yesterday's load curve as a forecast for D. Keep weekly extrema as daily features, valid for their own week; do not fabricate an hourly curve. If unavailable, use a training-only seasonal fallback and explicit age/missing flags.

**Rights/retrieval.** Exact load items are CC BY 4.0 subject to primary-owner exclusions. Use free registered token with XML GET/POST `https://web-api.tp.entsoe.eu/api`, `documentType=A65`, process A01 or A31 and explicit area/dates. Published rate cap is 400 requests/minute per account/token; keep collection far below it. Do not inspect the existing token's value. API availability does not prove an all-version retrieval route. [ER], [EGTC], [EREST], [ERATE], [ETOKEN]

### 4.4 Pre-auction capacity

**Product.** Directional forecast NTC MW per real border/MTU (11.1), and final pre-auction RAM MW/PTDF per CNEC/region/MTU (11.1.B). Keep border direction, constraint identifiers and domain stage. These are feasible-domain inputs, not exchanged energy. An exact first original record for each border/region is unverified. Core starts delivery 2022-06-09; a full 2019 bridge to CWE has not been demonstrated. [NTC], [FB], [JG], [JCWE]

**Vintage.** Valid intervals and UpdateTime UTC are documented, but original old-version/arrival retention is unverified. JAO monitoring/pending flags and nominal deadlines do not establish historical arrival; the provider documents delays. Core final 10:30 CET winter/CEST summer is 09:30/08:30 UTC, before both the origin and summer gate. [NTCS], [FBS], [JTIME], [JDELAY]

**Missingness/rule.** All annual numerical counts are unverified. For Core, 2019–2021 and 2022 through June8 are structurally absent. Optional NTC publication and changing topology create additional gaps. A nonexistent link/CNEC is not a zero-capacity constraint. Select the newest pre-origin domain valid for D; use an older issue only if it still covers D. Do not carry yesterday's domain into a different delivery day. Domain-stage, missing and stale flags are required.

**Rights/retrieval.** Prefer the separate ENTSO-E CC BY grant for the exact capacity items and applicable owners; obtain an all-version export route before admission. REST token/XML and File Library routes are documented; product-specific complete history is unverified. JAO's Core GET API exists, but exact auth/quota and permission for public API automation/ML/features are unresolved. Its terms restrict automated access/copying and require authorization for ML/AI/advanced statistics in the restricted-area conditions; do not generalize an unexamined API exception. No request for permission was sent. [ER], [EREST], [FMS], [JAPI], [JT]

### 4.5 TIGGE original ECMWF ensembles

**Product.** Centre `ecmf` original medium-range weather ensembles, global, GRIB2, six-hour lead steps. Programme archive begins October 2006; selected-centre earliest complete fields and 2019 gaps are unverified. Preserve centre/model/member/grid changes. Candidate fields include 10m wind u/v (m/s), temperature (K) and radiation; TIGGE `ssr` is accumulated **net** solar energy (J/m²), not downward GHI. [TG], [TGP], [TGM]

**Vintage.** Initialisation UTC is `issued_at`, not actual upload. The public 48h delay gives a reconstructed earliest eligibility, not evidenced arrival. D−3 00:00 UTC is scheduled accessible D−1 00:00 UTC and covers delivery D within UTC bounds +70…+95h depending on season/DST. Retrieve six-hour bracketing steps +66…+96h and define any interpolation/aggregation explicitly; these weather steps are not native hourly power forecasts. Do not use the D−1 run before its delayed public access. Preserve model version, member, lead, valid interval and first-seen time. [TGT], [TG]

**Missingness.** Each annual bin is unverified. The FAQ identifies lost surface-control fields on 710 dates across 2006–2019; the 2019 subset and perturbed-member impact require audit. GRIB missing bitmap differs from calm wind or zero radiation. [TGF]

**Rule.** Use the newest older run known available before origin if it covers D; retain age and missing flags. Deaccumulate radiation within a single run/member before averaging; no differences across runs. Evaluate older ensembles as a separate experiment; do not assume the late-power-forecast benchmark's gain transfers.

**Rights/retrieval.** ECMWF centre is CC BY4.0 under the current centre-scoped licence; some other centres are noncommercial and must not be mixed into this public product by default. Owner free registration and licence acceptance are required. Current ECDS API `https://ecds.ecmwf.int/api`, dataset `tigge-forecasts`, via `cdsapi`, with explicit centre/date/time/member/variable/lead/grid requests; GRIB2. Route migration is product metadata, not a market event. Numeric quotas are unverified. [TGT], [TGAPI]

### 4.6 Direct ECB state/context series

**Products.** Deposit-facility rate %, effective-state series from 1999; USD perEUR reference rate, business-day series fromJan 1999. €STR % is optional only for a later start: first publication 2019-10-02 for 2019-10-01. Do not substitute retrospectively revised pre€STR into January–September 2019. [ECBDFR], [ECBFX], [ECBFIRST]

**Vintage.** Policy decisions need announcement time and effective start/end, which are distinct. The current-rate feature uses the state effective at origin; a separately labelled future-effective rate for D is permissible only when its announcement was already public before origin. Rate decisions published after origin become usable at a later origin, even when a daily effective-date table does not carry announcement time. FX uses its last prior published reference rate because its afternoon release is late. API `includeHistory=true` can request production and previous versions; `updatedAfter` is a delta filter, not an as-of selector. Series-specific original version retention is unverified. [ECBDEC], [ECBFX], [ECBAPI]

**Missingness/rule.** Annual numerical audit is unverified. A policy rate remains valid across weekends until the next effective change; sparse change records are not holes. FX/€STR follow their publication calendars; use last known release with age and nonpublication-day flags. Do not fill a missing expected release with a later value. €STR opening 2019 gap is structural. Ordinary €STR publication08:00 CET and permitted09:00 CET correction both precede origin; methodology's broader no-later-than09:00/11:00 CET bounds should be preserved as a documentation difference, not silently substituted for the operational clock. [ECBQA], [ECBMETH], [ECBFIRST]

**Rights/retrieval.** ECB custom terms allow free accurate reproduction/distribution with credit and explicitly labelled modifications; no ML prohibition was identified. Retain that notice rather than assert a native CC BY licence. Anonymous documented SDMX service `https://data-api.ecb.europa.eu/service/data/{flow}/{key}` supports bounded periods and CSV/JSON/SDMX; request history then reconstruct each release. No key requirement is documented; numeric rate cap is unverified. [ECBT], [ECBAPI], [ECBEX]

## 5. Wind and solar: +2 versus the own GFS model

The requested +2 route is sound **only when an issue explicitly covers D and was publicly available before the origin**. A model's eight-day internal horizon, an 08:00/09:00 calculation label or a `week-ahead` API enum does not meet that condition. The four German TSO products examined do not establish a reusable original +2 archive. 50Hertz and TenneT wind descriptions distinguish early calculation from evening publication; netztransparenz's discontinued forecasts omit directly marketed production and stop in 2022. [50W], [50P], [TW], [NZ]

The ENTSO-E starting claim is confirmed for **A01**: the fixed day-ahead curve is the latest forecast before18:00 Brussels D−1. It should not be extended to say that **A18 is impossible**: each current submission can in principle include earlier D coverage, but early horizon, primary-owner rights and old versions are unverified. **A40** fixes08:00 Brussels on delivery D, which is after the requested D−1 origin. The generation item has no blanket reuse-list grant. [E69], [ER]

Elia demonstrates that an explicitly early external power field can exist. Its Belgian wind field is worth CP-25 verification; its solar field cannot cover 2019. RTE's D−2 load route is another genuine multi-day product, but it does not provide German wind/PV and still needs original versions and feature-reuse clarification. [ELW], [ELS], [RTE], [RT]

DWD and ECMWF operational open data have legal live routes; free full-window original archive access was not established. PAMORE's public forecast retention is too short, despite older internal ICON storage. TIGGE is the distinct long-archive option, with older delayed runs and changing model grids. Open-Meteo full runs and previous runs do not provide the required 2019 coverage; stitched forecasts and hindcasts are not original issues. Reanalysis such as ERA5 remains excluded. [DWD], [PAM], [DWTUT], [MW], [TG], [OMS], [OMP], [OMH]

**Recommendation:** proceed with the planned GFS-to-power models and preserve weather initialisation, actual availability, capacity/plant inputs and training labels as known at each origin. Train wind and solar conversions inside each training fold; lag actual-power labels until their own publication permits use. Treat capacities and plant changes as dated inputs, not today's fleet applied retrospectively. An admitted Elia forecast or TIGGE ensemble can later be a separately evaluated addition. This research did not revisit existing GFS sourcing or its project-owned extraction gap.

The approximately19.5% pooled pinball-loss benefit of the unavailable late forecast is **Owner-supplied project evidence**, not a result re-estimated here. It prioritizes early fundamentals; it does not promise the same improvement for an older forecast or own model.

Peer-reviewed support is consistent with that priority. Lago et al.(2021) use load/renewable fundamentals and cross-market information in electricity-price benchmarks; their datasets do not certify our origin or reuse. Marcjasz et al.(2023) examine German probabilistic forecasting with own-price lags, load/renewables and lagged fuel/carbon inputs; their forecast timing cannot be imported into this project. Maciejowska, Nitka and Weron(2021) motivate improving load/wind/solar forecasts. The ranking here is an inference from those studies plus the project's own benchmark; CP-25 collects and a later checkpoint tests value. [LAGO], [MARC], [MNW]

## 6. Held sources and precise admission checks

### 6.1 RTE French D−2 load

The guide documents mainland France load including grid losses and excluding pumped-storage consumption, MW/PT30M for D−2, historical resource since 2012-12-17. It recommends a call around 07:00 for D−2 and optionally later for updates; this is **not a publication deadline**. The recommendation's timezone is unverified. Returned timestamps are explicitly Paris UTC+1 in winter/UTC+2 in summer. Each interval has `start_date`, `end_date`, `updated_date`; the API defaults to latest, and bounded past requests do not establish all old revisions. Up to186 days/request, JSON GET `https://digital.iservices.rte-france.com/open_api/consumption/v1/short_term?type=D-2&start_date=…&end_date=…`, OAuth2 registration. Numerical rate cap is unverified. [RTE]

All annual counts are unverified. Require original issue/arrival/version retention, not only a D−2 label. Use an earlier issue only if it still covers D; absence is not a holiday zero. RTE terms permit attributed public-data reuse but prohibit modification/distortion of portal/content; the applicability to independently derived forecast features should be clarified before admission. No AI-specific restriction was identified there. Registration, explicit tariff confirmation and any enquiry are Owner decisions. [RT]

### 6.2 GIE AGSI+ and ALSI

AGSI+ Germany daily storage stockTWh and injection/withdrawalGWh/d; ALSI LNG stockGWh and send-outGWh/d. API documentation permits historical requests back 2011(AGSI)/2012(ALSI), but facilities have differing starts and gaps. Records can be estimated(E), confirmed(C) or no-data(N), and amended without notice. `gasDayStart` is validity, not issue; no full old-version/as-of selector was established. Processing19:30 CET and23:00 is documented, with second-clock/DST ambiguity. At the morning origin use only the last already-published prior-evening run; its latest completed gasday is generally older than the D−1 calendar label suggests. A conservative calendar inference at the D−1 morning origin is normally gasDayStart D−3, published on the D−2 evening; actual publication, not that lag alone, controls admission. [GIEAPI], [GIETIME]

Every annual vintage/missingness count is unverified. Carry forward the last known published stock on nonrelease/gap days with age/status flags; flows are not stocks and should not be carried as physical flow estimates without a separate rule. Never treat N or null as zero inventory, or replace an estimated old value with a later confirmed value. Legal raw/derived reuse with GIE/AGSI/ALSI attribution is documented under custom terms, not native CC BY4.0. [GIED]

After Owner free-key registration, JSON GET `https://agsi.gie.eu/api?country=de&from=…&to=…&size=300&page=…`, analogous ALSI host, with `x-key` header. Documented60 requests/minute and300 rows/page; respect429/backoff. Complete original versions, actual historic arrival and clock convention remain enquiries; latest revised history is not eligible for the strict experiment. [GIEAPI]

### 6.3 Generation outages

ENTSO-E15.1 provides planned/forced generation availability, MW/unit/event interval. Current files have InstanceCode,Version,OldVersion,Status(Active/Cancelled/Withdrawn), VersionPublicationTimestamp UTC and valid outage times. This improves the technical assessment over a latest-only API: a version-capable replay schema is documented. Its complete retention since 2019 and primary-owner reuse are unverified;15.1 is omitted from the CC BY list. REST update bounds return the latest updated revision, not all historical messages. [OUTS], [EPARAM], [ER]

All annual counts are unverified. Reconstruct each origin from the latest then-public version; apply cancellation only from its publication onward, deduplicate plant/unit overlaps, and distinguish reporting thresholds/provider silence from zero outages. Flag summer10:00–11:00 UTC arrivals. No carry-forward across a message's valid end; delayed/new messages remain missing knowledge, not retrospectively repaired data.

File Library `https://fms.tp.entsoe.eu/` documents authenticated UTF-8 tab-delimited monthlyCSV, bearer login,100 requests/min/user/channel. File regeneration is not message publication. Owner account choice and owner-specific permission come before retrieval. EEX's alternative has rolling five-year free coverage, restrictive personal/noncommercial reuse and paidAPI/AI licensing; its documented UTC publication/modification fields do not prove every original version. [FMS], [EEXUMM], [EEXDISC], [EEXAPI], [EEXT]

### 6.4 EIA Brent and EUA auction proxy

**EIA:** exact Brent product/history in the table; observation time is not publication time, and original versions/first arrival are unverified. All annual gaps are unverified; non-trading days are intentional. If admitted, carry the latest actually published quote with age over nonrelease days, never a later revision. Direct API `https://api.eia.gov/v2/seriesid/PET.RBRTE.D`, free Owner key, JSON/XML; documented5000 JSON/300 XML rows per response, time-based cap unverified. EIA's private-material exception plus Refinitiv source blocks an unconditional public-domain claim. Obtain written source-specific rights and historical-release evidence. FRED is not a permitted ML fallback under current terms. [EIAD], [EIAH], [EIAT], [EIAAPI], [FREDT]

**EUA:** EEX primary-auction EUR/allowance results, auction-level, archive labelled 2012–2025 plus2026 report route. Original corrections/arrival and raw/feature permission remain unverified. Clock sources conflict: detailed website results~11:10 CET(2018/August 2024),~11:05 CET(September 2024), versusFAQ11:00 CE(S)T. Literal CET11:05–11:10=10:05–10:10 UTC, within the summer post-gate/pre-origin interval; seasonal CEST would be09:05–09:10 UTC. Preserve this ambiguity and actual-arrival requirement. [EUAA], [EUA18], [EUA24A], [EUA24B], [EEXFAQ]

All annual counts are unverified. Use each year's auction calendar; no-auction day, cancelled auction, missing report and numeric zero are separate states. After rights/vintages pass, carry only the most recent published result with age/auctioneer flags. The product page links report/ZIP files through `public.eex-group.com`; formal API, format/quotas and permitted automation are unverified. Do not label this secondary-market EUA or assume EEX's subscription terms automatically grant rights to the free report. [EUAA], [EEXUSE], [EEXT]

### 6.5 NVE hydro and remaining finance

NVE reservoir fill fraction/energy by Norwegian area is weekly, with a documented new public route 2019-04-08. January–March 2019 coverage and old issue/correction retention remain unverified. Measurement interval is generally Sunday24:00, sometimes older; that is not Wednesday publication. Published clock13:00 lacks explicit timezone in the retrieved schedule; if Europe/Oslo it is12:00UTCwinter or11:00UTCsummer, so the newly released Wednesday report misses the strict origin. Use the previous published report until a documented release. Holidays can defer it. [NVE 2019], [NVEMETHOD]

All annual counts are unverified. Carry a known report only until a predeclared maximum age, with age/coverage flags; no report is not zero reservoir. Anonymous documented JSON/XML endpoint `https://biapi.nve.no/magasinstatistikk/api/Magasinstatistikk/HentOffentligData` can return history; it was **not called**. Numeric quotas are unverified. NLOD attribution/reuse is documented; neither the API start nor a current historical curve establishes original 2019 vintages. [NVE], [NVESPEC]

Bundesbank's10-year yield needs start, release time, security-roll definition, source ownership and original revisions; direct documented API is `https://api.statistiken.bundesbank.de/rest/data/{flow}/{key}`, CSV/SDMX, numeric quota/auth requirement unverified. Its own-statistics reuse grant excludes third-party rights and requires accurate source identification. All annual counts are unverified; only last actual pre-origin releases could be carried with age. [BBY], [BBAPI], [BBT]

No qualifying free VDAX-NEW/VSTOXX history/live licence was found. For a free volatility **feature**, compute lagged realised volatility from the already licensed electricity-price history; this adds no external source and is not an implied equity-volatility index. Euribor needs an external-product/derived-data licence; €STR is the cleaner direct-provider route if the Owner accepts its shorter history. [STOXXT], [STOXXHELP], [EMMIT], [EMMIMETA], [ECBFIRST]

## 7. Starting claims: verdicts and corrections

| Starting claim | Evidence-backed disposition |
|---|---|
| No qualifying free TTF/THE history from 2019 | **Not overturned.** No all-filter route established. THE itself starts 2021-10-01; a predecessor bridge is a distinct choice. [EGSI] |
| EEX free history about60 days | **Correct for final NGP**, not universal: traded contracts45 days and indices up to1 year are described separately. Neither supplies original 2019 issues. [NGP], [EEXFAQ] |
| EEX DataSourcev8 AI clause | **Confirmed.** Valid 2025-11-01, §3.2.3 requires an appropriate AI licence; directly processable raw and derived media redistribution is not a default permission. [EEXT] |
| Yahoo redistribution / Ember Montel | **Yahoo confirmed.** Ember methodology confirms Montel sourcing; exact upstream licensing contract is **unverified**, rather than reproduced as an established grant. [YAHOO], [EMBER], [EMBEROLD] |
| EUA primary archive only 2012–2025 | **Coverage wording corrected:** a2026 report route also exists. Still primary auctions, with rights/vintages unresolved; no qualifying secondary-market archive found. [EUAA] |
| Coal monthly Pink Sheet only | **Not overturned for qualifying free source.** Monthly/revised latest history is unsuitable for the daily original-vintage layer; API2 trademark alone grants no data rights. [WB], [WBREV] |
| ENTSO-E reuse is item/owner scoped | **Confirmed.** Listed load/capacity items cannot confer rights on omitted generation/price/outage items; exceptions must be applied. [ER], [EGTC] |
| A69 day-ahead18:00; current/intraday unexamined | **Fixed A01 confirmed; A18/A40 now assessed.** A40 is delivery-day08:00, late; A18 could be early but rights/original versions remain unverified. [E69] |
| JAO01:15/10:30 timezone/history unknown | **Final10:30 verified CETwinter/CESTsummer** by ACER methodology; initial winter convention and actual original arrival remain unverified. Core begins 2022-06-09 delivery. Direct terms require permission. [JTIME], [JG], [JT] |
| Open-Meteo archives mostly 2024; stitched not issue; ERA5 excluded | **Confirmed with detail.** Full-run IFS 2024-03-14 is described as hindcasts; others 2026-04-02; earlier stitched/model-specific coverage does not establish the required original runs. [OMS], [OMP], [OMH] |
| EIA Brent as government public-domain shortcut | **Overturned as unconditional assumption.** Exact series cites private source; EIA's exception needs clarification. [EIAD], [EIAT] |

## 8. Rejections and stop conditions

| Product/route | Failed filter or unresolved blocker; do not repeat an unchanged search |
|---|---|
| Day-D prices in any zone | **F3 N**, same auction information explicitly excluded; lag only |
| Scheduled exchanges, coupling net positions, shadow prices/active constraints, intraday residual capacity | **F3 N**, post-coupling outputs; pre-auction grid-model forecasts must remain distinct [JH] |
| A69/A01; A40 | **F3 N**, evening D−1 / delivery-morning release [E69] |
| A69/A18 as latest historical curve | **F2/F4 U**, not an original pre-origin issue; provider enquiry needed [ER], [E69] |
| Four German TSOs as assumed early +2 | Clock/horizon/public rights/original archive not established;50Hertz/TenneTwind public release late [50W], [TW], [50T], [BT] |
| Discontinued netztransparenz wind/PV | **F4/F5 N**, ends 2022-12-15, unlike total-generation scope [NZ] |
| Energy-Charts labels as issue archive | **F3/F4 U**, no original-arrival/as-of proof; generation licence provenance unresolved [ECSPEC], [ER] |
| DWD PAMORE / rolling ECMWFopen | **F4 N** for documented public retention [PAM], [MW] |
| Open-Meteo stitched/hindcast/short-start archives; reanalysis | **F3/F4 N** requested original-issue semantics/coverage [OMS], [OMP], [OMH] |
| Elia11:00 solar full2019 window | **F4 N**, field first 2020-10-01 [ELCOUNTSTARTS] |
| Direct JAO without written permission | **F2/F5 U/restricted**, ML/automation/public reuse; **F4 N** Core2019 window [JT], [JG] |
| EEX/THE fuel shortcuts, Yahoo, Emberquotes | Rights/full original archive/live route not established; THE provisional explicitly not historicised [EEXT], [THE], [THET], [YAHOO], [EMBER] |
| ACER LNG as full2019 gas | **F4 N**, starts 2023 [ACERSTART] |
| World Bank latest table as daily as-issued fuel | Resolution N and revised history; dated monthly reports are a separate low-priority question [WB], [WBREV] |
| FRED/ALFRED Brent or financial ML features | **F2/F5 N** current service/ML prohibition; do not infer permission from series public-domain metadata [FREDT] |
| EEX free outage history | **F2/F4/F5 fail/unresolved**, five-year window, restricted reuse, paidAPI [EEXUMM], [EEXDISC], [EEXAPI] |
| ENTSO-E outage REST update filter alone | **F4 N** all-version requirement; latest revision only [EPARAM] |
| VDAX-NEW/VSTOXX; Euribor | **F2/F4/F5 N** unlicensed open product/full history [STOXXT], [STOXXHELP], [EMMIT] |
| €STR/pre€STR full-window splice | **F4 N**, opening history absent; revised pre€STR not original issue [ECBFIRST] |
| Latest GIE/NVE historical observations treated as original issues | **F4 U**, old versions/arrival not demonstrated [GIEAPI], [NVESPEC] |

## 9. Owner decisions

No enquiry or registration was performed. The following decisions precede any dependent collection:

1. **Elia:** seek confirmation that the 11:00 field preserves original issues, corrections and delays, and that the live wind/solar successors preserve that contract. This is the highest-priority archive enquiry.
2. **SMARD/Energinet/ENTSO-E:** request original publication/correction exports, per-zone starts and a supported SMARD daily route. For ENTSO-E ask specifically about all versions of6.1.B/6.1.C/11.1/11.1.B and primary-owner exceptions. Decide whether any additional File Library account is needed; do not assume the existing API token authenticates every service.
3. **RTE:** confirm free publicAPI access, original D−2 revisions/arrival since 2019, and raw/derived-feature/public ML rights under the portal terms; then decide on OAuth registration.
4. **TIGGE:** decide whether older ensembles justify collection cost; authorize free ECDS registration/licence acceptance only for approved CC BY centres. Ask for selected-centre completeness, missing-control dates and arrival guarantees. DWD/ECMWF original operational archives require separate eligibility/waiver/subscription decisions.
5. **Gas/carbon/outages/JAO:** any paid EEX or other-provider archive, subscription, JAO ML/API permission and generation primary-owner licence enquiry belongs to the Owner. Require a written grant covering the public project, raw redistribution or explicit public features, ML, complete2019 original versions and live automation. A research/internal licence alone is insufficient.
6. **EIA:** seek specific rights for Refinitiv-sourced Brent and original release timestamps; only then decide on free API-key registration. FRED/ALFRED is excluded unless the Owner deliberately obtains a written applicable exception.
7. **GIE/NVE:** request all-version/first-arrival evidence and timezone conventions; decide on GIE free-key registration. Current revised history must not enter a strict as-issued backtest.
8. **Partial-window choices:** decide whether PL beforeNovember 2019 absence, Elia solar fromOctober 2020, €STR fromOctober 2019, Core fromJune 2022 and monthly World Bank context deserve separate experiments. They cannot be silently promoted into the required full-window shortlist. The recommendation is to keep them outside the strict primary comparison until an explicit design decision.
9. **Finance:** any Euribor or implied-volatility subscription is optional and lower priority than early fundamentals. The direct ECB route and own lagged realised-volatility feature avoid those purchases, subject to the recorded vintage checks.

## 10. CP-25 completion evidence to require

For each candidate that survives Owner/provider decisions, CP-25 should produce a product/owner/licence manifest; original raw responses and hashes; original and reconstructed clock fields clearly distinguished; unique-key and23/24/25-hour checks; annual coverage/null/version/cancellation counts; documented release/calendar exceptions; and a legal live route with actual first-seen logging. No feature may use a later version to repair historical knowledge. Freeze the admitted set only after those checks, then leave predictive benefit to the later evaluation checkpoint.

**Annual coverage limit of this report:** apart from Elia's bounded field-count audit, numerical missingness and original-version completeness are unverified for each 2019,2020,2021,2022,2023,2024,2025 and2026 throughApril7. Structural gaps are identified separately in the tables. Documentation-only research cannot honestly supply missing counts that were never measured.

**Execution record:** one bounded research report and aggregate coverage evidence were written locally. No governance anchor, configuration, program state, source code or model was changed. No Git branch/worktree/tag was created and nothing was staged, committed or published. Temporary research packets are retained in `.local/artifacts/b-research-stage3/` as recovery material; the report and Elia evidence are the durable copies.

**Interview-answer trigger for the Orchestrator:** why we chose our own GFS power forecast after distinguishing calculation time from public arrival, and why an open historical table or an outage version schema did not alone establish causal, legally publishable inputs. No interview document was edited by this research agent.

## 11. Primary reference register

All references were retrieved **2026-10-11 UTC**. Each current link is cited only for documentation, terms, schedule or coverage metadata. The literature references support ranking, not dataset admission. Reference definitions follow below.

| ID | Primary documentation or terms |
|---|---|
| 50P | [50Hertz photovoltaic forecast description][50P] |
| 50T | [50Hertz reuse/automated-download conditions][50T] |
| 50W | [50Hertz wind forecast calculation/publication description][50W] |
| ACERSTART | [ACER LNG assessment launch metadata][ACERSTART] |
| ACERTIME | [ACER LNG assessment release schedule metadata][ACERTIME] |
| AEGIS | [ACER AEGIS public report route][AEGIS] |
| ALFRED | [ALFRED Brent release-start metadata; values not collected][ALFRED] |
| AP | [Amprion photovoltaic infeed product definition][AP] |
| AW | [Amprion wind feed-in forecast product][AW] |
| BBAPI | [Bundesbank SDMX API documentation][BBAPI] |
| BBT | [ESCB statistical reuse policy][BBT] |
| BBWEB | [Bundesbank general website use terms][BBWEB] |
| BBY | [Bundesbank current federal-security yield series identity][BBY] |
| BNG | [Bundesnetzagentur gas-price product/source and update metadata][BNG] |
| BPD | [TransnetBW photovoltaic previous-day forecast definition][BPD] |
| BT | [TransnetBW website reuse terms][BT] |
| BW | [TransnetBW grid data products][BW] |
| BWD | [TransnetBW wind previous-day forecast definition][BWD] |
| DWD | [DWD open operational data service][DWD] |
| DWDT | [DWD open-data legal notice and CC BY terms][DWDT] |
| DWTUT | [DWD ICON tutorial, internal archive history][DWTUT] |
| E69 | [ENTSO-E renewable forecast item 14.1.D][E69] |
| ECAPI | [Energy-Charts API documentation and service limits][ECAPI] |
| ECBAPI | [ECB API data/history/format documentation][ECBAPI] |
| ECBDEC | [ECB monetary-policy decision publication time change][ECBDEC] |
| ECBDFR | [ECB deposit-facility start/effective-date metadata for 1999][ECBDFR] |
| ECBEX | [ECB API examples][ECBEX] |
| ECBFIRST | [ECB euro short-term rate first release and pre-STR revisions][ECBFIRST] |
| ECBFX | [ECB foreign-exchange reference-rate history/publication methodology][ECBFX] |
| ECBMETH | [ECB March 2021 euro short-term rate methodology release bounds][ECBMETH] |
| ECBQA | [ECB euro short-term rate release and correction FAQ][ECBQA] |
| ECBT | [ECB copyright, attribution and modifications policy][ECBT] |
| ECNOTE | [Energy-Charts publication and source notes][ECNOTE] |
| ECSPEC | [Energy-Charts forecast OpenAPI schema][ECSPEC] |
| EEXAPI | [EEX Transparency API guide v008][EEXAPI] |
| EEXDISC | [EEX Transparency reuse disclaimer][EEXDISC] |
| EEXFAQ | [EEX historical windows and publication FAQ][EEXFAQ] |
| EEXT | [EEX DataSource General Conditions v8, valid 2025-11-01][EEXT] |
| EEXUMM | [EEX generation UMM product and free history metadata][EEXUMM] |
| EEXUSE | [EEX market-data use conditions][EEXUSE] |
| EGSI | [EEX 2021 technical EGSI product/index definition, calculation window and THE transition][EGSI] |
| EGTC | [ENTSO-E General Terms and Conditions][EGTC] |
| EHISTORY | [ENTSO-E GUI value details and historical submissions][EHISTORY] |
| EIAAPI | [EIA API v2 key, series-ID route and response limits][EIAAPI] |
| EIAD | [EIA spot-price definitions and Refinitiv source][EIAD] |
| EIAH | [EIA Brent initial-observation metadata; values not collected][EIAH] |
| EIAT | [EIA reuse and protected private-material exception][EIAT] |
| ELAPI | [Elia hosted Explore API documentation][ELAPI] |
| ELCOUNTSTART | [Elia dates-only bounded coverage query for ods031 early field][ELCOUNTSTART] |
| ELCOUNTSTARTS | [Elia dates-only bounded coverage query for ods032 early field][ELCOUNTSTARTS] |
| ELHOME | [Elia portal product and API migration notices][ELHOME] |
| ELQ | [Elia aggregate-only 2019 wind field-coverage query][ELQ] |
| ELRTS | [Elia near-real-time solar metadata][ELRTS] |
| ELRTW | [Elia near-real-time wind metadata][ELRTW] |
| ELS | [Elia historical Belgian photovoltaic metadata and field definitions][ELS] |
| ELT | [Elia Open Data Licence, incorporating CC BY 4.0][ELT] |
| ELW | [Elia historical Belgian wind dataset metadata and field definitions][ELW] |
| EMBER | [Ember prices/costs methodology and Montel attribution][EMBER] |
| EMBEROLD | [Ember 2023 supporting-data methodology][EMBEROLD] |
| EMMIMETA | [EMMI historical-data and external/derived product subscription metadata][EMMIMETA] |
| EMMIT | [EMMI 2026 benchmark/derived-data licence agreement example][EMMIT] |
| ENAPI | [Energinet documented dataset API][ENAPI] |
| ENNEW | [Energinet quarter-hour DayAheadPrices metadata and polling guidance][ENNEW] |
| ENOLD | [Energinet legacy Elspotprices catalogue metadata][ENOLD] |
| ENT | [Energinet data-use terms, CC BY 4.0][ENT] |
| EPARAM | [ENTSO-E request/update parameters and latest outage revision semantics][EPARAM] |
| ER | [ENTSO-E data-item/primary-owner reuse list][ER] |
| ERATE | [ENTSO-E account API rate limit][ERATE] |
| EREST | [ENTSO-E REST integration documentation][EREST] |
| ETOKEN | [ENTSO-E API token registration][ETOKEN] |
| EUA18 | [EEX 2018 auction process and result publication][EUA18] |
| EUA24A | [EEX August 2024 auction process][EUA24A] |
| EUA24B | [EEX September 2024 auction process][EUA24B] |
| EUAA | [EEX primary EUA report archive and 2026 route metadata][EUAA] |
| FB | [ENTSO-E pre-allocation flow-based parameter item][FB] |
| FBS | [ENTSO-E flow-based capacity file schema][FBS] |
| FMS | [ENTSO-E authenticated File Library guide][FMS] |
| FREDOBS | [FRED/ALFRED observation/vintage API fields][FREDOBS] |
| FREDT | [FRED/ALFRED current legal and API ML restrictions][FREDT] |
| FREDV | [FRED/ALFRED vintage-date API semantics][FREDV] |
| GIEAPI | [GIE AGSI/ALSI API v007, historical requests, status and processing][GIEAPI] |
| GIED | [GIE transparency-data reuse and source referral][GIED] |
| GIETIME | [GIE gas-day/UTC interval documentation][GIETIME] |
| JAPI | [JAO Core API documentation][JAPI] |
| JCWE | [JAO CWE historical retention notice][JCWE] |
| JDELAY | [JAO publication-delay documentation, 2025-04-29][JDELAY] |
| JG | [JAO Core launch/delivery start metadata][JG] |
| JH | [JAO Core publication handbook][JH] |
| JT | [JAO website, restricted-area and AI/ML terms][JT] |
| JTIME | [ACER-hosted Core methodology, seasonal publication timezone][JTIME] |
| LAGO | [Lago et al., 2021, Applied Energy 293, 116983, doi:10.1016/j.apenergy.2021.116983][LAGO] |
| LB | [ENTSO-E day-ahead load item 6.1.B][LB] |
| LS | [ENTSO-E load forecast file schema][LS] |
| LW | [ENTSO-E week-ahead load item 6.1.C][LW] |
| MARC | [Marcjasz et al., 2023, Energy Economics 125, 106843, doi:10.1016/j.eneco.2023.106843][MARC] |
| MARS | [ECMWF historical forecast archive access][MARS] |
| MNW | [Maciejowska, Nitka and Weron, 2021, doi:10.1016/j.eneco.2021.105273][MNW] |
| MW | [ECMWF operational open data and rolling retention][MW] |
| MWORDER | [ECMWF ordering and service agreements][MWORDER] |
| MWT | [ECMWF data-use terms][MWT] |
| NGP | [EEX NGP provisional/final history metadata][NGP] |
| NTC | [ENTSO-E forecast transfer capacity item 11.1][NTC] |
| NTCS | [ENTSO-E forecast transfer capacity file schema][NTCS] |
| NVE | [NVE reservoir API and NLOD reuse][NVE] |
| NVE2019 | [NVE 2019 public-route migration and weekly release metadata][NVE2019] |
| NVEMETHOD | [NVE reservoir statistics methodology and release exceptions][NVEMETHOD] |
| NVESPEC | [NVE reservoir OpenAPI schema, not observations][NVESPEC] |
| NZ | [netztransparenz discontinued wind/solar forecasts and replacement scope][NZ] |
| NZAPI | [netztransparenz API portal][NZAPI] |
| NZT | [netztransparenz imprint and reuse restrictions][NZT] |
| OMH | [Open-Meteo stitched historical forecast semantics][OMH] |
| OMP | [Open-Meteo previous-run coverage][OMP] |
| OMS | [Open-Meteo full-run coverage and hindcast documentation][OMS] |
| OMT | [Open-Meteo data/service terms][OMT] |
| OUT | [ENTSO-E generation/production outage item 15.1][OUT] |
| OUTS | [ENTSO-E versioned outage file schema][OUTS] |
| PAM | [DWD PAMORE archive eligibility and retention][PAM] |
| PRICE | [ENTSO-E energy price file schema][PRICE] |
| RT | [RTE portals General Terms, public data and exchange-data restrictions][RT] |
| RTE | [RTE Consumption v1.2 user guide][RTE] |
| SBE | [SMARD Belgian/NO2 price history coverage metadata][SBE] |
| SP | [SMARD user manual, zone prices, publication and known gap][SP] |
| ST | [SMARD CC BY 4.0 reuse][ST] |
| STOXXHELP | [STOXX public history/licensed download route][STOXXHELP] |
| STOXXT | [STOXX private-use, copying, derivative-model and automation restrictions][STOXXT] |
| TG | [ECMWF TIGGE ensemble forecast dataset][TG] |
| TGAPI | [TIGGE ECDS API migration and retrieval guide][TGAPI] |
| TGF | [TIGGE FAQ and lost surface-control fields][TGF] |
| TGM | [TIGGE centres/model characteristics][TGM] |
| TGP | [TIGGE parameter units and accumulation definitions][TGP] |
| TGT | [TIGGE centre-specific licences and 48-hour delay][TGT] |
| THE | [THE imbalance prices and non-historicised provisional values][THE] |
| THEGP | [THE GASPOOL predecessor archive metadata][THEGP] |
| THENC | [THE NCG predecessor archive metadata][THENC] |
| THES | [THE XML interface specification v2.1][THES] |
| THET | [THE reproduction-consent disclaimer][THET] |
| TP | [TenneT photovoltaic product][TP] |
| TW | [TenneT wind forecast product and timing][TW] |
| WB | [World Bank Pink Sheet file-route metadata][WB] |
| WBDEF | [World Bank historical gas/commodity definitions][WBDEF] |
| WBH | [World Bank monthly historical dataset start metadata][WBH] |
| WBREV | [World Bank October 2024 Pink Sheet revision notes][WBREV] |
| WBT | [World Bank dataset terms and third-party exceptions][WBT] |
| WBTIME | [World Bank historical monthly release-schedule documentation][WBTIME] |
| YAHOO | [Yahoo Finance redistribution policy][YAHOO] |

[50P]: https://www.50hertz.com/de/Transparenz/Kennzahlen/ErzeugungEinspeisung/EinspeisungausPhotovoltaik "50Hertz photovoltaic forecast description"
[50T]: https://www.50hertz.com/de/Impressum "50Hertz reuse/automated-download conditions"
[50W]: https://www.50hertz.com/Transparenz/Kennzahlen/ErzeugungEinspeisung/EinspeisungausWindenergie "50Hertz wind forecast calculation/publication description"
[ACERSTART]: https://www.acer.europa.eu/node?page=64 "ACER LNG assessment launch metadata"
[ACERTIME]: https://www.acer.europa.eu/node?page=69 "ACER LNG assessment release schedule metadata"
[AEGIS]: https://aegis.acer.europa.eu/terminal/home "ACER AEGIS public report route"
[ALFRED]: https://alfred.stlouisfed.org/series?seid=DCOILBRENTEU "ALFRED Brent release-start metadata; values not collected"
[AP]: https://www.amprion.net/Grid-Data/Photovoltaic-Infeed/ "Amprion photovoltaic infeed product definition"
[AW]: https://www.amprion.net/Grid-Data/Wind-Feed-In/ "Amprion wind feed-in forecast product"
[BBAPI]: https://www.bundesbank.de/en/statistics/time-series-databases/help-for-sdmx-web-service/web-service-interface-data "Bundesbank SDMX API documentation"
[BBT]: https://www.bundesbank.de/resource/blob/621210/4acef2023eb61a0420fee6f2a2cbe064/mL/policy-reuse-escb-statistics-data.pdf "ESCB statistical reuse policy"
[BBWEB]: https://www.bundesbank.de/de/startseite/benutzerhinweise/nutzungsbedingungen-fuer-den-allgemeinen-gebrauch-der-website-763554 "Bundesbank general website use terms"
[BBY]: https://www.bundesbank.de/en/statistics/overview-of-the-statistical-series/-/3-yields-of-current-federal-securities-914558 "Bundesbank current federal-security yield series identity"
[BNG]: https://www.bundesnetzagentur.de/DE/Gasversorgung/aktuelle_gasversorgung/_svg/Gaspreise/Gaspreise.html "Bundesnetzagentur gas-price product/source and update metadata"
[BPD]: https://www.transnetbw.de/_Resources/Persistent/5/7/1/7/5717009f044e5fc1207fdf86cc2336d9b66c178a/Detailinformationen_Einspeisung-Fotovoltaik.pdf "TransnetBW photovoltaic previous-day forecast definition"
[BT]: https://www.transnetbw.de/de/nutzungsbedingungen "TransnetBW website reuse terms"
[BW]: https://www.transnetbw.de/de/transparenz/marktdaten/kennzahlen "TransnetBW grid data products"
[BWD]: https://www.transnetbw.de/_Resources/Persistent/c/9/8/3/c9834dddadebafa50102dee5f1a1e278cda8d5ea/Detailinformationen_Einspeisung-Windenergie.pdf "TransnetBW wind previous-day forecast definition"
[DWD]: https://www.dwd.de/EN/ourservices/opendata/opendata.html "DWD open operational data service"
[DWDT]: https://www.dwd.de/DE/service/rechtliche_hinweise/rechtliche_hinweise_node.html "DWD open-data legal notice and CC BY terms"
[DWTUT]: https://dwd.de/EN/ourservices/nwp_icon_tutorial/pdf_volume/icon_tutorial2024_en.pdf?__blob=publicationFile&v=3 "DWD ICON tutorial, internal archive history"
[E69]: https://transparencyplatform.zendesk.com/hc/en-us/articles/16648445340180-Generation-Forecasts-for-Wind-and-Solar-14-1-D "ENTSO-E renewable forecast item 14.1.D"
[ECAPI]: https://api.energy-charts.info/ "Energy-Charts API documentation and service limits"
[ECBAPI]: https://data.ecb.europa.eu/help/api/data "ECB API data/history/format documentation"
[ECBDEC]: https://www.ecb.europa.eu/press/pr/date/2022/html/ecb.pr220627~73acedf868.en.html "ECB monetary-policy decision publication time change"
[ECBDFR]: https://www.ecb.europa.eu/press/pr/date/1998/html/pr981222.fr.html "ECB deposit-facility start/effective-date metadata for 1999"
[ECBEX]: https://data.ecb.europa.eu/help/api/data-examples "ECB API examples"
[ECBFIRST]: https://www.ecb.europa.eu/stats/financial_markets_and_interest_rates/euro_short-term_rate/html/eurostr_overview.en.html "ECB euro short-term rate first release and pre-STR revisions"
[ECBFX]: https://www.ecb.europa.eu/press/pr/date/2015/html/pr151207.en.html "ECB foreign-exchange reference-rate history/publication methodology"
[ECBMETH]: https://www.ecb.europa.eu/stats/euro-short-term-rates/interest_rate_benchmarks/WG_euro_risk-free_rates/shared/pdf/ecb.ESTER_methodology_and_policies.en.pdf "ECB March 2021 euro short-term rate methodology release bounds"
[ECBQA]: https://www.ecb.europa.eu/stats/financial_markets_and_interest_rates/euro_short-term_rate/html/eurostr_qa.en.html "ECB euro short-term rate release and correction FAQ"
[ECBT]: https://www.ecb.europa.eu/services/using-our-site/disclaimer/html/index.en.html "ECB copyright, attribution and modifications policy"
[ECNOTE]: https://energy-charts.info/publishing-notes.html "Energy-Charts publication and source notes"
[ECSPEC]: https://api.energy-charts.info/openapi.json "Energy-Charts forecast OpenAPI schema"
[EEXAPI]: https://www.eex.com/fileadmin/EEX/Downloads/Market_Data/EEX_Group_DataSource/API/20251006_EEX_Transparency_Data_-_API_User_Guide_v008.pdf "EEX Transparency API guide v008"
[EEXDISC]: https://www.eex-transparency.com/disclaimer "EEX Transparency reuse disclaimer"
[EEXFAQ]: https://www.eex.com/en/faq "EEX historical windows and publication FAQ"
[EEXT]: https://www.eex.com/fileadmin/EEX/Downloads/Market_Data/EEX_Group_DataSource/General_Terms_of_Contract/WIP_Datasource_GC-v8_FINAL.pdf "EEX DataSource General Conditions v8, valid 2025-11-01"
[EEXUMM]: https://www.eex-transparency.com/power/de/umms/ "EEX generation UMM product and free history metadata"
[EEXUSE]: https://www.eex.com/en/market-data/indices-benchmark/indices "EEX market-data use conditions"
[EGSI]: https://www.eex.com/fileadmin/EEX/Markets/Natural_Gas/EGSI_Futures/EEX_trader_workshop_EGSI_Futures_Jun_2021.pdf "EEX 2021 technical EGSI product/index definition, calculation window and THE transition"
[EGTC]: https://transparencyplatform.zendesk.com/hc/article_attachments/40921869376401 "ENTSO-E General Terms and Conditions"
[EHISTORY]: https://transparencyplatform.zendesk.com/hc/en-us/articles/33729752039441-Value-details-and-value-history "ENTSO-E GUI value details and historical submissions"
[EIAAPI]: https://www.eia.gov/opendata/documentation.php "EIA API v2 key, series-ID route and response limits"
[EIAD]: https://www.eia.gov/dnav/pet/TblDefs/pet_pri_spt_tbldef2.asp "EIA spot-price definitions and Refinitiv source"
[EIAH]: https://www.eia.gov/dnav/pet/hist/leafhandler.ashx?f=d&n=pet&s=rbrte "EIA Brent initial-observation metadata; values not collected"
[EIAT]: https://www.eia.gov/about/copyrights_reuse.php "EIA reuse and protected private-material exception"
[ELAPI]: https://opendata.elia.be/api/explore/v2.1/console "Elia hosted Explore API documentation"
[ELCOUNTSTART]: https://opendata.elia.be/api/explore/v2.1/catalog/datasets/ods031/records?select=min(datetime)%20as%20first_valid%2Cmax(datetime)%20as%20last_valid&where=datetime%20%3C%20date'2026-04-07T22%3A00%3A00Z'%20and%20dayahead11hforecast%20is%20not%20null&limit=1 "Elia dates-only bounded coverage query for ods031 early field"
[ELCOUNTSTARTS]: https://opendata.elia.be/api/explore/v2.1/catalog/datasets/ods032/records?select=min(datetime)%20as%20first_valid%2Cmax(datetime)%20as%20last_valid&where=datetime%20%3C%20date'2026-04-07T22%3A00%3A00Z'%20and%20dayahead11hforecast%20is%20not%20null&limit=1 "Elia dates-only bounded coverage query for ods032 early field"
[ELHOME]: https://opendata.elia.be/pages/home/ "Elia portal product and API migration notices"
[ELQ]: https://opendata.elia.be/api/explore/v2.1/catalog/datasets/ods031/records?select=region%2Coffshoreonshore%2Cgridconnectiontype%2Ccount(*)%20as%20rows%2Ccount(dayahead11hforecast)%20as%20forecast_rows&where=datetime%20%3E%3D%20date'2018-12-31T23%3A00%3A00Z'%20and%20datetime%20%3C%20date'2019-12-31T23%3A00%3A00Z'&group_by=region%2Coffshoreonshore%2Cgridconnectiontype&limit=20 "Elia aggregate-only 2019 wind field-coverage query"
[ELRTS]: https://opendata.elia.be/api/explore/v2.1/catalog/datasets/ods087 "Elia near-real-time solar metadata"
[ELRTW]: https://opendata.elia.be/api/explore/v2.1/catalog/datasets/ods086 "Elia near-real-time wind metadata"
[ELS]: https://opendata.elia.be/api/explore/v2.1/catalog/datasets/ods032 "Elia historical Belgian photovoltaic metadata and field definitions"
[ELT]: https://opendata.elia.be/pages/licence/ "Elia Open Data Licence, incorporating CC BY 4.0"
[ELW]: https://opendata.elia.be/api/explore/v2.1/catalog/datasets/ods031 "Elia historical Belgian wind dataset metadata and field definitions"
[EMBER]: https://ember-energy.org/data/european-electricity-prices-and-costs/ "Ember prices/costs methodology and Montel attribution"
[EMBEROLD]: https://ember-energy.org/latest-insights/european-electricity-review-2023/supporting-materials/ "Ember 2023 supporting-data methodology"
[EMMIMETA]: https://inte.emmi-benchmarks.eu/globalassets/documents/pdf/communication/publications/newsletter_issue-2_oct-2021.pdf "EMMI historical-data and external/derived product subscription metadata"
[EMMIT]: https://www.emmi-benchmarks.eu/globalassets/documents/pdf/subscriptions/rates-plans/agreements/2026/emmi-clearing-services-license-agreement_2026v2.pdf "EMMI 2026 benchmark/derived-data licence agreement example"
[ENAPI]: https://www.energidataservice.dk/guides/api-guides "Energinet documented dataset API"
[ENNEW]: https://api.energidataservice.dk/meta/dataset/DayAheadPrices "Energinet quarter-hour DayAheadPrices metadata and polling guidance"
[ENOLD]: https://api.energidataservice.dk/meta/dataset/Elspotprices "Energinet legacy Elspotprices catalogue metadata"
[ENT]: https://www.energidataservice.dk/terms-and-conditions "Energinet data-use terms, CC BY 4.0"
[EPARAM]: https://transparencyplatform.zendesk.com/hc/en-us/articles/15696716612372-Request-Parameters "ENTSO-E request/update parameters and latest outage revision semantics"
[ER]: https://transparencyplatform.zendesk.com/hc/article_attachments/40921869379729 "ENTSO-E data-item/primary-owner reuse list"
[ERATE]: https://transparencyplatform.zendesk.com/hc/en-us/articles/12783148966036-API-Rate-Limit-Part-1 "ENTSO-E account API rate limit"
[EREST]: https://transparencyplatform.zendesk.com/hc/en-us/articles/15692855254548-Sitemap-for-Restful-API-Integration "ENTSO-E REST integration documentation"
[ETOKEN]: https://transparencyplatform.zendesk.com/hc/en-us/articles/12845911031188-How-to-get-security-token "ENTSO-E API token registration"
[EUA18]: https://www.eex.com/fileadmin/user_upload/20180213_Auctions-how_to_participate_Final.pdf "EEX 2018 auction process and result publication"
[EUA24A]: https://www.eex.com/fileadmin/EEX/Downloads/Markets/Environmentals/20240801_Auctions-how_to_participate_Final.pdf "EEX August 2024 auction process"
[EUA24B]: https://www.eex.com/fileadmin/EEX/Downloads/Markets/Environmentals/20240905_EU_ETS_-_Participation_in_the_auctions_and_outlook_secondary_market.pdf "EEX September 2024 auction process"
[EUAA]: https://www.eex.com/en/market-data/market-data-hub/environmentals/eex-eua-primary-auction-spot-download "EEX primary EUA report archive and 2026 route metadata"
[FB]: https://transparencyplatform.zendesk.com/hc/en-us/articles/16647585946644-Flow-based-Allocations-11-1 "ENTSO-E pre-allocation flow-based parameter item"
[FBS]: https://transparencyplatform.zendesk.com/hc/en-us/articles/30303878664977-FlowBasedCapacityAllocation-11-1-B-r3 "ENTSO-E flow-based capacity file schema"
[FMS]: https://transparencyplatform.zendesk.com/hc/en-us/articles/35960137882129-File-Library-Guide "ENTSO-E authenticated File Library guide"
[FREDOBS]: https://fred.stlouisfed.org/docs/api/fred/series_observations.html "FRED/ALFRED observation/vintage API fields"
[FREDT]: https://fred.stlouisfed.org/legal/ "FRED/ALFRED current legal and API ML restrictions"
[FREDV]: https://fred.stlouisfed.org/docs/api/fred/series_vintagedates.html "FRED/ALFRED vintage-date API semantics"
[GIEAPI]: https://www.gie.eu/transparency-platform/GIE_API_documentation_v007.pdf "GIE AGSI/ALSI API v007, historical requests, status and processing"
[GIED]: https://iip.gie.eu/data-usage "GIE transparency-data reuse and source referral"
[GIETIME]: https://www.gie.eu/download/2022/GIE_TRA_ROUNDTABLE_012.pdf "GIE gas-day/UTC interval documentation"
[JAPI]: https://publicationtool.jao.eu/core/api "JAO Core API documentation"
[JCWE]: https://www.jao.eu/news/jao-data-publication-tool-after-go-live-core-fb-da "JAO CWE historical retention notice"
[JDELAY]: https://www.jao.eu/news/core-publication-tool-data-delays "JAO publication-delay documentation, 2025-04-29"
[JG]: https://www.jao.eu/news/core-announcement-go-live-readiness "JAO Core launch/delivery start metadata"
[JH]: https://publicationtool.jao.eu/core/CORE_PublicationHandbook "JAO Core publication handbook"
[JT]: https://www.jao.eu/terms-conditions "JAO website, restricted-area and AI/ML terms"
[JTIME]: https://acer.europa.eu/sites/default/files/documents/en/Electricity/MARKET-CODES/CAPACITY-ALLOCATION-AND-CONGESTION-MANAGEMENT/16%20CCM/Action%204%20-%20CCM%20Core%20DA%20amended%20proposal.pdf "ACER-hosted Core methodology, seasonal publication timezone"
[LAGO]: https://arxiv.org/pdf/2008.08004 "Lago et al., 2021, Applied Energy 293, 116983, doi:10.1016/j.apenergy.2021.116983"
[LB]: https://transparencyplatform.zendesk.com/hc/en-us/articles/16647979768084-Total-Load-Day-Ahead-Actual-6-1-A-6-1-B "ENTSO-E day-ahead load item 6.1.B"
[LS]: https://transparencyplatform.zendesk.com/hc/en-us/articles/36492900251281-DayAheadTotalLoadForecast-6-1-B-r3 "ENTSO-E load forecast file schema"
[LW]: https://transparencyplatform.zendesk.com/hc/en-us/articles/16648042895252-Total-Load-Forecast-Week-Ahead-6-1-C- "ENTSO-E week-ahead load item 6.1.C"
[MARC]: https://arxiv.org/html/2207.02832v2 "Marcjasz et al., 2023, Energy Economics 125, 106843, doi:10.1016/j.eneco.2023.106843"
[MARS]: https://www.ecmwf.int/en/forecasts/access-forecasts/access-archive-datasets "ECMWF historical forecast archive access"
[MNW]: https://www.sciencedirect.com/science/article/abs/pii/S014098832100178X "Maciejowska, Nitka and Weron, 2021, doi:10.1016/j.eneco.2021.105273"
[MW]: https://www.ecmwf.int/en/forecasts/datasets/open-data "ECMWF operational open data and rolling retention"
[MWORDER]: https://www.ecmwf.int/en/forecasts/access-forecasts/ordering "ECMWF ordering and service agreements"
[MWT]: https://www.ecmwf.int/en/terms-use "ECMWF data-use terms"
[NGP]: https://www.eex.com/en/markets/natural-gas/gas-market-transparency "EEX NGP provisional/final history metadata"
[NTC]: https://transparencyplatform.zendesk.com/hc/en-us/articles/16647270294676-Forecasted-Day-ahead-Transfer-Capacities-11-1 "ENTSO-E forecast transfer capacity item 11.1"
[NTCS]: https://transparencyplatform.zendesk.com/hc/en-us/articles/47873087545489-ForecastedTransferCapacities-11-1-r3-1 "ENTSO-E forecast transfer capacity file schema"
[NVE]: https://api.nve.no/doc/magasinstatistikk/ "NVE reservoir API and NLOD reuse"
[NVE2019]: https://www.nve.no/nytt-fra-nve/nyheter-energi/magasinstatistikken-flytter-til-nve-no/ "NVE 2019 public-route migration and weekly release metadata"
[NVEMETHOD]: https://webfileservice.nve.no/API/PublishedFiles/Download/64edbe40-b965-4c90-a114-88162ffff454/201903383/3435075 "NVE reservoir statistics methodology and release exceptions"
[NVESPEC]: https://biapi.nve.no/magasinstatistikk/swagger/v1/swagger.json "NVE reservoir OpenAPI schema, not observations"
[NZ]: https://www.netztransparenz.de/de-de/Erneuerbare-Energien-und-Umlagen/Freiwillige-Ver%C3%B6ffentlichungen/Wind-und-Solarenergie-Prognose-bis-15122022 "netztransparenz discontinued wind/solar forecasts and replacement scope"
[NZAPI]: https://api-portal.netztransparenz.de/ "netztransparenz API portal"
[NZT]: https://www.netztransparenz.de/de-de/Impressum "netztransparenz imprint and reuse restrictions"
[OMH]: https://open-meteo.com/en/docs/historical-forecast-api "Open-Meteo stitched historical forecast semantics"
[OMP]: https://open-meteo.com/en/docs/previous-runs-api "Open-Meteo previous-run coverage"
[OMS]: https://open-meteo.com/en/docs/single-runs-api "Open-Meteo full-run coverage and hindcast documentation"
[OMT]: https://open-meteo.com/en/terms "Open-Meteo data/service terms"
[OUT]: https://transparencyplatform.zendesk.com/hc/en-us/articles/16652173943828-Planned-Unavailability-Changes-in-Actual-Availability-of-Generation-Production-Units-15-1-A-15-1-B-15-1-C-15-1-D "ENTSO-E generation/production outage item 15.1"
[OUTS]: https://transparencyplatform.zendesk.com/hc/en-us/articles/48639064005777-UnavailabilityOfProductionAndGenerationUnits-15-1-A-B-C-D-r3-1 "ENTSO-E versioned outage file schema"
[PAM]: https://www.dwd.de/EN/ourservices/pamore/pamore.html "DWD PAMORE archive eligibility and retention"
[PRICE]: https://transparencyplatform.zendesk.com/hc/en-us/articles/47308268140689-EnergyPrices-12-1-D-r3-1 "ENTSO-E energy price file schema"
[RT]: https://www.services-rte.com/fr/conditions-generales-d-utilisation.html "RTE portals General Terms, public data and exchange-data restrictions"
[RTE]: https://data.rte-france.org/web/guest/catalog/-/api/doc/user-guide/Consumption/1.2 "RTE Consumption v1.2 user guide"
[SBE]: https://www.smard.de/home/neu-auf-smard-daten-zum-handel-mit-belgien-und-norwegen-204448 "SMARD Belgian/NO2 price history coverage metadata"
[SP]: https://www.smard.de/resource/blob/220052/9d526adf4b948599da4a956dfae6dab9/smard-benutzerhandbuch-04-2026-data.pdf "SMARD user manual, zone prices, publication and known gap"
[ST]: https://www.smard.de/home/datennutzung "SMARD CC BY 4.0 reuse"
[STOXXHELP]: https://www.stoxx.com/help "STOXX public history/licensed download route"
[STOXXT]: https://stoxx.com/legal/stoxx-conditions-of-use/ "STOXX private-use, copying, derivative-model and automation restrictions"
[TG]: https://ecds.ecmwf.int/datasets/tigge-forecasts?tab=overview "ECMWF TIGGE ensemble forecast dataset"
[TGAPI]: https://confluence.ecmwf.int/spaces/DAC/pages/462894687/User+guide+for+migration+of+S2S+and+TIGGE+to+ECDS "TIGGE ECDS API migration and retrieval guide"
[TGF]: https://confluence.ecmwf.int/spaces/TIGGE/pages/40797492/FAQ "TIGGE FAQ and lost surface-control fields"
[TGM]: https://confluence.ecmwf.int/spaces/TIGGE/pages/40109876/Models "TIGGE centres/model characteristics"
[TGP]: https://confluence.ecmwf.int/spaces/TIGGE/pages/40109884/Parameters "TIGGE parameter units and accumulation definitions"
[TGT]: https://ecds.ecmwf.int/licences/tigge-licence "TIGGE centre-specific licences and 48-hour delay"
[THE]: https://www.tradinghub.eu/en-gb/Publications/Prices/Imbalance-Prices "THE imbalance prices and non-historicised provisional values"
[THEGP]: https://www.tradinghub.eu/en-gb/Ver%C3%B6ffentlichungen/Downloadcenter/Archiv-GASPOOL "THE GASPOOL predecessor archive metadata"
[THENC]: https://www.tradinghub.eu/en-gb/Publications/Downloadcenter/Archive-NetConnect-Germany "THE NCG predecessor archive metadata"
[THES]: https://www.tradinghub.eu/Portals/0/DLC%20Datenformate/2024/The_XML_Interface_V2.1_de_.pdf?ver=W26YVA1bNUtTeHRPf_bM2A%3D%3D "THE XML interface specification v2.1"
[THET]: https://www.tradinghub.eu/en-gb/Home/Disclaimer "THE reproduction-consent disclaimer"
[TP]: https://netztransparenz.tennet.eu/electricity-market/transparency-pages/transparency-germany/network-figures/actual-and-forecast-solar-energy-feed-in "TenneT photovoltaic product"
[TW]: https://netztransparenz.tennet.eu/electricity-market/transparency-pages/transparency-germany/network-figures/actual-and-forecast-wind-energy-feed-in "TenneT wind forecast product and timing"
[WB]: https://www.worldbank.org/en/research/commodity-markets "World Bank Pink Sheet file-route metadata"
[WBDEF]: https://thedocs.worldbank.org/en/doc/395981516914586689-0050022018/related/CMO31Pink31Sheet31July312014.pdf "World Bank historical gas/commodity definitions"
[WBH]: https://thedocs.worldbank.org/en/doc/386771467756369668-0050022016/render/CMOHistoricalDataMonthly.pdf "World Bank monthly historical dataset start metadata"
[WBREV]: https://thedocs.worldbank.org/en/doc/5d903e848db1d1b83e0ec8f744e55570-0350012021/related/CMO-Pink-Sheet-October-2024.pdf "World Bank October 2024 Pink Sheet revision notes"
[WBT]: https://data.worldbank.org/summary-terms-of-use "World Bank dataset terms and third-party exceptions"
[WBTIME]: https://thedocs.worldbank.org/en/doc/a5472ce5554628b5ff8f072705dcf9fd-0360012021/original/20210423-Commodity-Markets-Outlook-Recent-Developments-Outlook-and-Risks-John-Baffes-1.pdf "World Bank historical monthly release-schedule documentation"
[YAHOO]: https://help.yahoo.com/kb/finance/article-exchanges-data-delays-sln2310.html "Yahoo Finance redistribution policy"
