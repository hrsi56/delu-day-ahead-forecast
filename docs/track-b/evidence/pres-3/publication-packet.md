# PRES-3 publication packet — v4 on every surface, and the corrected planned list

**Template:** `docs/track-b/publication-packet-template.md` (SHA-256 `4efb0185…829cf`), every section,
completed from CP-21's draft packet `docs/track-b/evidence/cp-21/publication-packet.md`
(`b5ffceee…a075c`). **Rules:** PUBLISH_RULES 1.2 (`a43ac020…8bb15b`), incorporating Publication
Standard v1 (`01d721c2…9478cc`) and presentation plan revision 3 (`28119374…49812c`). **Research
anchor, read-only:** `capstone_v21.md` v21-r8 (`81d61271…c182`), §§17.6, 17.9, 18.1 and 18.5.
**Brief:** `docs/track-b/evidence/pres-3/issued-brief.md` (`57a8c7fb…773d7`), byte-identical to the
issued copy.

Numbers are never typed into a surface: each value below names the committed row it comes from, and
the evidence layer re-derives it. A file cannot name the commit that contains it, so this packet
writes `<final_candidate_sha>` and `<evidence_tip_sha>` where those belong; the checkpoint return and
`integration.md` give both. Every step in §8.2–8.6 is the Owner's (the brief's "Nothing else is
authorized"). Beyond the local checks and anonymous reads recorded in §7, this block takes one
external action, the MLflow upload the brief authorizes (§6).

## 1. Identity

| Item | Value |
|---|---|
| Publication block | PRES-3, brief `docs/track-b/evidence/pres-3/issued-brief.md` at `57a8c7fbc1b9b0d3c268e4af95a02a4a75276dda8224a24a6b1119ac03b773d7` |
| Checkpoint published | CP-21, brief `docs/track-b/evidence/cp-21/issued-brief.md` at `813fb8a476a7b6d10ecf0a5519e97ec8efc4ff36e0f13868676ad34534fc020f` |
| Governing research plan and version | `capstone_v21.md` v21-r6 §17 for CP-21's content (exact bytes at `evidence/cp-21:capstone_v21.md`, `ee402c47…67344`); v21-r8 (`81d61271…c182`) §17.6, §17.9, §18.1 and §18.5 for this block; rule `cp21-adoption` |
| Evidence tag and tip | `evidence/cp-21` at `1d13f99b1ab12f64719b439d0a9d4703bc7e1bdb`, frozen 2026-09-30 (`registry.py::EVIDENCE_TAGS`) |
| Final reviewed candidate (model code) | `260dcf9fb3f5706cb896991ba7b6edf4cd9494b6` (CP-21's Integration PASS; `mlflow_export.py::CHECKPOINTS["cp21"]`) |
| Report, review verdict, landing record | `reports/block-challenger/report.md`; `docs/track-b/evidence/cp-21/integration.md`; `docs/track-b/cp-21-landing-2026-09-30.md` (`569b471b…f9aed`), the source of v4's adoption date |
| This block's candidate and evidence tip | `<final_candidate_sha>` and `<evidence_tip_sha>` on `gauntlet/pres-3`, off `main` `17f354e42c0d6f3199227fe9d29df9f4dc8211e0` |

## 2. The registry entries, as entered (standard §5)

`src/delu_forecast/registry.py::_ENTRIES` holds packet §2's four draft entries exactly as drafted
(`tests/test_45_pres3_v4_publication.py::test_the_registry_holds_the_packets_draft_entries_exactly_apart_from_the_landing_identities`
compares every field with `reports/block-challenger/draft-registry.json`). Only the identities that
existed at landing were filled:

| Entry | Name | Status, date, source, reason |
|---|---|---|
| `v4` (generation) | v4 · three-block LightGBM added | adopted in research, 2026-09-30, `docs/track-b/cp-21-landing-2026-09-30.md`; predecessor `v3`, comparator `v3` |
| `pooled-lightgbm-weather` (study arm) | Pooled LightGBM with weather | not adopted, 2026-09-30, the landing record, "a study arm for attribution; never eligible for adoption" |
| `block-lightgbm` (study arm) | Three-block LightGBM | not adopted, 2026-09-30, the landing record, the same reason |
| `normalized-block-lightgbm` (study arm) | Normalized three-block LightGBM | not adopted, 2026-09-30, the landing record, the same reason |

Every other field (subtitle, short, codes `CP-21: HGL | L-P | L-R | L-N` on `common-10747h`, evidence
class, plan, rule, sources, claim map, run keys, style, anchor, checkpoint) is the draft's. v4's
encoding is the Owner's decision D6 of 2026-09-29: amber `#B45309`, a filled diamond, the direct
label "v4" (`build_pages.py::TOKENS`, `ROLE_STYLE`).

**Code additions to existing entries — all seven entered, none withheld:** `v3` CP-21 `HG`
("comparator, saved"), `v2` `H0` ("saved reference"), `naive` `B0` ("normalizer"), `v1` `B1`
("development replay"), `daily-lear` `B2`, `daily-lightgbm` `B3`, `normalized-lear` `A1`. None
changes a published record: the published v1–v3 chapters, the product documentation and both
earlier transitions are byte-identical to the published page (`test_45::test_every_historical_section_is_byte_identical_to_the_published_page`),
and the export's 23 published runs are unchanged (§6).

**Checkpoint and rule.** `CHECKPOINTS["CP-21"]`: run key `cp21`, evidence tag `evidence/cp-21`
at `1d13f99`, frozen 2026-09-30, report, verdict, landing record, children `HGL`, `L-P`, `L-R`,
`L-N`. `RULES["cp21-adoption"]`: set 2026-09-29, from v21-r6 §17.6 and `protocol.json`
`adoption_rule_verbatim`, frozen before scoring.

## 3. The claim map

`docs/track-b/research-content/cp21-claims.md` (`8df2e9a5…c37c43`, unchanged), registered in
`research_claims.py::CLAIM_MAPS`, with claims C100–C127 and the withheld claims W22–W27; W1–W21 stay
in force (`cp15-cp16-claims.md`, `cp20-claims.md`). The publication-level claims are
`docs/track-b/research-content/publication-claims.md` P51 (the adoption headline and its terms) and
P52 (the A3 transition), with source keys M21, U21, C21, AD21, PR21 and LR21, and PRES-3 notes on
P07, P08, P10, P16, P18–P21, P23–P26 and P33 where the comparison moved to CP-21's rows. The guards
W22–W26 are regular expressions in `research_claims.py::WITHHELD`, each with a negative control in
`test_45`.

## 4. The derived headline quantities (standard §3.3), re-derived from committed rows

| Quantity | Value | From |
|---|---|---|
| (a) The pre-specified verdict | **met** (`derived.adoption.v4.verdict`) | `reports/block-challenger/adoption.json` `verdict` and `conditions`, re-applied by `derived.py::ADOPTION_RULES` |
| The rule, in words, with its date | `RULES["cp21-adoption"].words`, set **2026-09-29** (`derived.adoption.v4.set_on`) | v21-r6 §17.6; `protocol.json` `adoption_rule_verbatim` |
| Distance from v3 in the rule's unit | ΔS_MAE −0.0301 [−0.0368, −0.0228]; ΔS_WIS −0.0266 [−0.0327, −0.0204] (`derived.adoption.v4.distance.*`) | `uncertainty.csv` rows `HGL-HG` MAE and WIS |
| N | **1** — HGL; the three study arms are never eligible under the rule (`derived.adoption.v4.tested`) | `protocol.json` `adoption_rule`; v21-r6 §17.2 |
| "Point comparison" label | not needed: both differences carry 95% intervals | `uncertainty.csv` |
| (b) The change against v3, as a share of v3's score | S_MAE −5%, S_WIS −5% (`derived.change.v4.*`, kind `ratio_change`) | `uncertainty.csv` `ratio` |
| Its 95% interval | S_MAE [−6%, −4%]; S_WIS [−6%, −4%] — CP-21's own bootstrap draws: seed 15042, 2,000 replicates, 7-day blocks, percentiles of `S_HGL,b / S_v3,b − 1` | `uncertainty.csv` `ratio_ci_lower`, `ratio_ci_upper`; `replicates.parquet` |
| (c) MAE per period, EUR/MWh | v4: ordinary periods 4.9–15.0; stress period (fold 3, the 2022 crisis) 47.0 (`derived.periods.v4.*`) | `metrics.csv` per-fold rows |

The headline, as rendered (`research_claims.py::headline_template`, adoption branch): "Met the
adoption rule set before the experiment: both error scores improved on v3's (v4 − v3: −0.0301
[−0.0368, −0.0228] on the point-error score, −0.0266 [−0.0327, −0.0204] on the interval score; 1
policy tested against the rule)", with the badge "Development · post-selection". It leads with the
verdict, names each metric beside its value (A1) and gives N; its terms beneath it define the error
scores, the adoption rule (its date, with a route to its four conditions), the paired difference,
policies and the evidence class.

## 5. Slot texts, as published (standard §6)

The chapter's blocks are `research_claims.py::BLOCKS` keys `v4.*`, rendered by
`build_pages.py::v4_slots` into `render_chapter`'s slots. Differences from the draft, all editorial and
none changing a claim:

- the headline and its terms were shortened to meet A2 (release attempt 1);
- the reading lists the rule's four conditions as met, naming the six screening criteria that are
  one of them, rather than saying that "the rule adopted the change" (editorial V3; the fresh reader;
  C109); the decision reads "In September 2026, v4 was adopted in research. It met the adoption rule
  set before the experiment against v3; the released model, v1, did not change. The three study arms
  were built only to separate the change into steps, and were never candidates for adoption." (C127,
  P51; the fresh reader);
- "policy", which the headline uses, is defined beneath it (the fresh reader; PUBLISH_RULES §2);
- the rule's four conditions are the protocol detail's `v4.rule` (C101), which the README's v4
  section also carries and the headline's term links to (V3);
- the study arms read "no demonstrated joint preference" (V4, W25); every interval of a
  difference or ratio is a "confidence interval" (V5); v4 has "the same information" as v3, not
  "the same inputs"; pooled coverage is given at every level.

| Slot | Block | Claim |
|---|---|---|
| The question | `v4.question` — "Does adding a nonlinear, block-structured forecaster to v3 improve both of its error scores?" | C104 |
| The change | `v4.change` | C104 |
| The main chart and its headline | `v4-c2a`, the paired differences against v3 on both scores with 95% confidence intervals; `v4.chart_headline` — −5% [−6%, −4%] on each score, as a share of v3's | C107, C108 |
| The reading | `v4.reading` | C109 |
| Not established | `v4.caveat.class` (new data), `v4.caveat.blocks` (the block split, C111), `v4.caveat.peak` (the August 2022 peak, C120) | C125, C111, C120 |
| The decision, dated | `v4.decision` | C127 |
| The evidence row | the report, the review verdict, the claim map, `compare:v4` | — |
| Details | method (`v4.method.blend`, `.inputs`, `.ladder` with C106's bundling, `.split` exactly as C111, `.arms`), per-period consistency (`v4.folds`), stress period (`v4.absolute`, `v4.peak`), coverage and width (`v4.coverage`), protocol and review (`v4.rule`, `v4.criteria`, `v4.parity`, `v4.controls`, `v4.cost`) | C101–C124 |

**The ladder, the block split and the peak.** The ladder B3 → pooled → three-block → v4 is the method
detail's, as the brief's extract places it, with C106's bundling in its paragraph, its chart label and
its description; the chapter's visible "Explore these results" routes to it ("The ladder: what each
step added", A5). The block split reads exactly as C111 ("no demonstrated joint preference") on the
reading path, in the chapter's "not established" and the transition. The peak finding C120 is on the
reading path too, in the chapter's "not established" and the transition's limits, and in full in the
stress-period detail (`test_45::test_the_peak_finding_is_on_the_reading_path_not_only_in_a_disclosure`).

### 5a. The adopted transition (A3)

| Field | Value |
|---|---|
| Title | "From v3 to v4: adding a three-block LightGBM" (`transition.v3-v4.title`) |
| Predecessor and dates | `v3`, adopted in research 2026-09-24; v4 adopted in research 2026-09-30 |
| The change | `transition.v3-v4.change`: v3's inputs and two LEAR forecasts kept; a three-block LightGBM forecaster (separate models for the night, the solar hours, and the shoulder and peak hours) with one third of the weight; intervals re-estimated on the new errors |
| The comparator set in advance | `v3`, also the predecessor (`transition.v3-v4.comparator`); no `predecessor` block is needed |
| The result | −5% [−6%, −4%] on both scores, as a share of v3's, with 95% confidence intervals of that ratio from CP-21's own draws; development evidence (`transition.v3-v4.result`) |
| What it does not establish | the block split (C111); a gain over the August 2022 peak, where v4's point error is higher than v3's (C120) (`transition.v3-v4.limits`) |
| The decision and the route | adopted in research 2026-09-30; route to `#v4-chart-title` |

### 5b. The released model's documentation (A4)

Not applicable: the released model does not change. v1 stays released and the demo runs it; the
product documentation is byte-identical to the published page.

### 5c. The chart routes (A5)

| Chart | Its heading | The route's label | Where the route starts |
|---|---|---|---|
| `v4-c2a` | `#v4-chart-title` | "The comparison chart and its evidence, in the v4 chapter" | the transition summary |
| `v4-ladder` | `#v4-ladder-steps` | "The ladder: what each step added" | the v4 chapter's "Explore these results" |
| `v4-arms` | `#v4-arms-against-v3` | "Each study arm against v3" | the same |
| `v4-c2b` | `#v4-per-period-differences` | "Did v4 help in every test period?" | the same |
| `v4-c3` | `#v4-absolute-errors` | "Absolute errors per test period, for v3 and v4" | the same |
| `v4-c4` | `#v4-peak` | "The August 2022 peak: where v4's point error is higher" | the same |
| `v4-c6` | `#v4-coverage` | "Did the intervals get more reliable, or only wider?" | the same |

Generated from the chapter's detail headings (`build_pages.py::explore_routes`); A5's discovery check
follows every route (§7).

### 5d. Final-product transition / daily operation (A7/A8/A9)

Not applicable: no final-product designation, rollout, Live or final-product Space exists (brief;
PUBLISH_RULES §1.3; v21-r8 §§16, 19 not triggered).

## 6. The MLflow export

- **The final export:** `reports/presentation/mlflow-export/cp21.json` (`68d165142e720e2bc0485e511fe85fe1bff40efddb6bce50290f53ddc904ff7f`), built
  by the draft's code path with the real registry (`mlflow_export.py::CHECKPOINTS["cp21"]`: model code
  `260dcf9f…`, evidence `evidence/cp-21@1d13f99`, completed 2026-09-30T00:57:44Z). Parent `cp21`,
  children `cp21/HGL`, `cp21/L-P`, `cp21/L-R`, `cp21/L-N`, experiment `delu-generations`.
- **Against CP-21's draft** (`reports/block-challenger/mlflow-export-draft/cp21.json`, `0f23d52d…5603`):
  `mlflow_export.py::final_vs_draft` — equal apart from the pending fields (`delu.evidence_ref`,
  `delu.model_code_sha`, `delu.original_completed_utc`, `delu.status`, `mlflow.note.content` on all
  five runs); the only addition is eight chart artifacts on `cp21/HGL` (plan §10.6): `overview`,
  `v4-c2a`, `v4-ladder`, `v4-arms`, `v4-c2b`, `v4-c3`, `v4-c4`, `v4-c6`. Differences: none.
- **Against the last published export** (`main` `17f354e`): `--diff-against 17f354e` — runs 23 → 28,
  added exactly the five cp21 runs; 0 identity changes, no substantive change, 55 of 55 artifact
  digests unchanged, `only_identity` true, experiment tags unchanged. The experiment description stays
  the published one: rewriting it would be an experiment-level write, which is not authorized
  (`EXPERIMENT_NOTE_CHECKPOINTS` pinned to CP-10/15/16/20).
- **Expected routes:** `experiment` and `compare:v4` (`registry.py::expected_routes`; `compare:v4`
  = `cp21/HGL`, `cp21/L-P`, `cp21/L-R`, `cp21/L-N`, `cp20/HG`).
- **The upload** (the brief's one authorized external action; runbook §1 step 5): after the independent
  check passes at the candidate and outside the Friday–Saturday window, `scripts/mlflow_publish.py
  --target public --authorized-runs cp21,cp21/HGL,cp21/L-P,cp21/L-R,cp21/L-N`, which reads the
  service first and refuses before any write unless every write belongs to those five runs
  (`write_plan`); log `reports/presentation/release-checks/pres-3-mlflow-upload.json`. Then the mirror
  verification (`pres-3-public-mirror.json`), the browser routes in both engines
  (`pres-3-public-mlflow-routes.json`), the index (`reports/presentation/mlflow_index.json`) and the
  final build (`build_pages.py --final`). The run IDs are in the mirror record; the return names them.
  The candidate's page omits the comparison's MLflow link, because the verified route lists v3's seven
  runs and the page draws eight; the index written after the upload restores it.

## 7. Checks run

Records under `reports/presentation/release-checks/` unless a path says otherwise. First failures
and superseded runs are kept beside their retries. A check run on `4b64fd229ddf0dbd4cd524bbfe58f8540a27ca11` covered a
tree that differs from the candidate only in the check records that commit adds.

| Check (runbook §9; brief "Reviews and evidence") | Record | Result |
|---|---|---|
| pytest, Python 3.13 | `pres-3-pytest-3.13.txt` | 1,280 passed, 7 skipped (Python 3.13.15, at `4b64fd2`) |
| A clean Python 3.12 run of every step of `.github/workflows/tests.yml`, in a fresh detached worktree | `pres-3-ci312.txt` | every step passed on Python 3.12.14 at `4b64fd2`: `uv sync --locked`, the payload build, pytest (1,280 passed, 7 skipped), the CQR fixture, cross-surface agreement, the WASM equivalence (15 passed); the worktree clean before and after. The publication guard runs only on `main` in CI |
| `make verify` | — | PASS: every bound claim agrees on every surface; the static page fetches nothing; the headline, names and statuses agree across surfaces |
| `make lint-publication` | — | PASS: page, README and templates 0 findings |
| `make publication-guard` | — | BLOCKED, by design: "reports/cp3/pages_build.json is a non-final build record (final: false)"; it passes only on the `--final` build |
| Determinism: `rebuild_presentation.py`, then `git status` | `pres-3-determinism.txt` | `git status` empty after the rebuild and after `make wasm`; the bundle reproduces `9028a118…` (at `4b64fd2`) |
| Links (`check_links.py`) | `pres-3-links.json` | no failed destination; the gated DagsHub UI URLs redirect to login, as controls |
| The §10 release checks and the placements, Chrome 154.0.8037.58 and WebKit 26.6, 1440 × 900, 768 × 1024, 390 × 844, 360 × 780, 320 × 640 and the emulated iPhone 393 × 659 | `pres-3-local-release.json` (attempt 4, the candidate's page) | passed: the headline block ends at 800.6 / 801.3 px (desktop) and 628.6 / 628.7 px (phone); the finding at 1,702.6 / 1,703.3 px (A2 limit 1,744) and 2,400.5 px (limit 2,420); chart text at least 12.21 px (320 px) and 14.58 px (390 px); no chart overlap or clipping; no console error, failed request, HTTP error or resource after the document; accessibility trees, keyboard, touch, contrast, 200% zoom and 320 px reflow in both engines |
| — its earlier attempts | `pres-3-local-release-attempt-1.json` (failed: the finding at 1,808.6 / 2,541.5 px, beyond A2; chart text overlapping in the comparison and the v4 arms charts); `-attempt-2.json` (passed, `7dd234b`); `-attempt-3.json` (passed, `d9c4438`, the fresh reader's screens) | superseded by attempt 4; a run on the page between attempts 3 and 4 was stopped and left no record |
| A5 discovery, from the closed default page, by mouse, keyboard and deep link | inside the release record | 33 routes in each engine at both placement sizes |
| The demo: cold start and controls; accessibility and keyboard; startup states | `pres-3-local-demo.json`, `pres-3-local-demo-a11y.json`, `pres-3-local-states.json` | ready in 10.2–12.8 s, 0 console errors, 0 failed requests; named controls, no target under 44 px, keyboard operation; loading, failure and retry. The bundle has not changed since |
| The bundle and the Space, anonymous and read-only | `pres-3-space-bundle.json`, `pres-3-space-check.json` | 805 files, `9028a118…`; deletion set exactly `style.css`; nine header-only changes; nothing written |
| The export | `pres-3-export-diff.json`, `pres-3-export-final-vs-draft.json` | `--check` current; runs 23 → 28, only cp21's five added, `only_identity` true; the final export equals the draft apart from its pending fields |
| `deploy_space.py`, offline | `tests/test_44_deploy_space.py` | 21 tests, in the pytest run |
| The value-based secret scan of every outgoing commit | `scripts/secret_guard.py pre-push` over `gauntlet/pres-3` | clean; the pre-commit and commit-msg hooks ran on every commit |
| One editorial review | `docs/track-b/evidence/pres-3/editorial.md` | 5 violations, repaired in `d9c4438`; 14 recommendations dispositioned in the advisory log |
| The fresh reader | `docs/track-b/evidence/pres-3/fresh-reader.md` | answers 1–5 agree; 1 violation found and repaired |
| The independent check, and the focused recheck at the final SHA | `docs/track-b/evidence/pres-3/integration.md` | after this packet |

No real Safari, real iPhone or screen reader was used; the phone widths are emulated viewports, and
the iPhone is Playwright's emulated device in WebKit.

## 8. Publication completion receipt and the Owner's packet

### 8.0 What would be published

| Surface | Reviewed output | Identity | Now public |
|---|---|---|---|
| Report, GitHub Pages | `docs/index.html` at `<final_candidate_sha>`, the `--final` build | `<final_page_sha256>` (the return and `integration.md`); at the candidate, before the index, 1,906,528 bytes, `90909512…a47bd` | 1,684,252 bytes, `f36314e28811ed4b7ec41bc73dfd481ddb112815effabfc4e7b3ae74d8edab1d` (PRES-2), read 2026-09-30T22:25:17Z |
| README | `README.md` at `<final_candidate_sha>` | `<final_readme_sha256>`; at the candidate `09e7dc66…c10c91` | at `main` `17f354e`: `3a16a70a…` |
| Static Space bundle | `dist/space-wasm/`, from `make wasm` at the landed tree | `bundle_sha256` `9028a11869a378ea5c3401a00ad46368e1c9e2f2f9f8732330d32b71af081585`, 805 files, 44,164,910 bytes; every file with its size, Git blob SHA-1 and SHA-256 in `reports/presentation/release-checks/pres-3-space-bundle.json`; an exact copy at `.local/artifacts/pres-3/space-wasm-9028a118/` | revision `0c550e863711e19abbb35219cf64d45dfb39c888`: PRES-2's bundle `8007f0d2…` plus `style.css` (`pres-3-space-check.json`) |
| Space change | the one Hub commit of §8.4 | adds none; changes the nine `public/boosters/*.txt.gz.b64` (their gzip header's OS byte only, A-PRES3-2; the decoded boosters are identical and the equivalence gate passes); **deletes exactly `style.css`** | — |
| Static Space card | `space-wasm/README.md` (the bundle's `README.md`) | `c92a2666d76255b24d8e0fb159f97bedcbee0a7a948fb6afeac4b02089bb9a67`, unchanged | the same |
| Space card (container, not hosted) | `space/README.md` | `745bbb932d78afbecdca3964af4885d223fd9301cd628bde1744f08e9f71d553`, unchanged | repository file only |
| MLflow `delu-generations` | `reports/presentation/mlflow-export/` | 28 runs; `cp21.json` `68d16514…4ff7f`; the five cp21 runs uploaded before the final build (§6), their run IDs in `pres-3-public-mirror.json` | 23 runs, no cp21 run (PRES-2) |

The demo still runs v1: the model, its payload and the v1 claims are unchanged; the cards name v1.

### 8.1 Receipt — intended identities (the Owner and the public checker complete the rest)

| Surface | Intended identity | Action / unchanged rationale | Observed public identity and UTC time | Verification record and result | Outstanding action |
|---|---|---|---|---|---|
| GitHub source / README | `land/pres-3` (the squash of `<evidence_tip_sha>`, same tree); README `<final_readme_sha256>`, whose glance and generation list name v4 | push by the Owner (§8.3) | the Owner fills: pushed revision, time | served README hash (§8.5) | §8.2–8.3 |
| GitHub Pages | `<final_page_sha256>`: v4 headline, chapter, transition, comparison row, corrected planned list | deploy by the push (§8.3) | the Owner fills: served hash, time | `pres-3-public-report.json`, `pres-3-public-links.json` | §8.3, §8.5 |
| Public MLflow | `cp21` and its four children in `delu-generations`, equal to `cp21.json` `68d16514…`; routes `experiment` and `compare:v4`; the 23 earlier runs unchanged | the authorized upload in this block, verified before the final build (§6) | run IDs and verification time: `pres-3-public-mirror.json` | `pres-3-public-mirror.json`, `pres-3-public-mlflow-routes.json`; after publication `pres-3-public-mirror-postdeploy.json`, `pres-3-public-mlflow-routes-postdeploy.json` | post-deployment reverification (§8.5) |
| Hugging Face Space card | `c92a2666…`, unchanged; it rides in the bundle | redeployed with the bundle (§8.4) | the Owner fills: Hub revision, public visibility, card hash | the card's raw bytes (§8.5) | §8.4–8.5 |
| Hugging Face direct demo | bundle `9028a118…`, serving the same v1 artifact; `style.css` deleted | deploy by the Owner with `deploy_space.py --upload --delete style.css` (§8.4) | the Owner fills: `after_revision` | `pres-3-space-deployment.json` (served set equals the bundle by path and hash); `pres-3-public-demo.json`, `pres-3-public-demo-a11y.json`, `pres-3-public-states.json` | §8.4–8.5 |

- **Publication-to-MLflow mapping:** `<final_candidate_sha>` → export `cp21.json` `68d16514…` (and
  `manifest.json`) → the cp21 run IDs in `pres-3-public-mirror.json` → the routes in
  `reports/presentation/mlflow_index.json`.
- **Final product and daily updates:** not applicable (no final-product designation).
- **Completion disposition:** incomplete until the Owner's steps and their public checks; the
  independent public review gives the PASS / FAIL / INCOMPLETE verdict.
- **Authority:** the MLflow upload, by the brief (the Owner's decision of 2026-09-30). The landing,
  the push, the Pages deployment and the Space commit with its deletion each need the Owner's own
  instruction; this packet grants none.

Every command below is the Owner's, run from the primary checkout, `/Users/djourno/Downloads/PJM`.
None opens a pager or an editor. Substitute `<evidence_tip_sha>`, `<final_page_sha256>` and `<final_readme_sha256>` from the
return, which also gives these commands with them filled in. Keep every record a step writes, first failures included.

### 8.2 Step 1 — the LAND

The primary checkout was on `main` at `17f354e`, with the Orchestrator's ` M progress.md`; the branch
does not touch `progress.md`. If `main` has moved, stop: the tree check below assumes the branch's
base.

```bash
git --no-pager rev-parse --abbrev-ref HEAD
```

Expect `main`.

```bash
git --no-pager rev-parse HEAD gauntlet/pres-3
```

Expect `17f354e42c0d6f3199227fe9d29df9f4dc8211e0`, then `<evidence_tip_sha>`.

```bash
git --no-pager status --porcelain=v1
```

Expect exactly ` M progress.md`. Any other line: stop and resolve it first.

**No untracked twin** (a file in the working tree at a path the branch adds or changes would block
or be overwritten by the squash):

```bash
git --no-pager diff --name-only 17f354e42c0d6f3199227fe9d29df9f4dc8211e0 <evidence_tip_sha> | while IFS= read -r f; do git ls-files --error-unmatch -- "$f" >/dev/null 2>&1 && ! git --no-pager diff --quiet -- "$f" && echo "MODIFIED $f"; git ls-files --error-unmatch -- "$f" >/dev/null 2>&1 || { [ -e "$f" ] && echo "TWIN $f"; }; done; echo twins-checked
```

Expect only `twins-checked`.

```bash
git --no-pager merge --squash gauntlet/pres-3
```

Expect `Updating 17f354e..<first 7 of evidence_tip_sha>`, `Fast-forward`, `Squash commit -- not
updating HEAD`, then the diffstat; no `CONFLICT` line.

```bash
test "$(git write-tree)" = "$(git rev-parse '<evidence_tip_sha>^{tree}')" && echo STAGED-TREE-EQUALS-EVIDENCE-TIP
```

Expect `STAGED-TREE-EQUALS-EVIDENCE-TIP`. If it does not print, stop: nothing is committed yet
(`git merge --abort` is not needed for a squash; `git reset --merge` restores the index).

```bash
git commit -F .local/artifacts/pres-3/msgs/land.txt
```

Expect `[main <land_sha>] Publish PRES-3: v4 on every surface, and the corrected planned list`,
then the summary. The secret guard runs in the pre-commit and commit-msg hooks and prints nothing
when clean.

```bash
git tag land/pres-3 HEAD
```

```bash
git tag evidence/pres-3 <evidence_tip_sha>
```

Both print nothing.

```bash
git --no-pager diff --stat HEAD <evidence_tip_sha>
```

Expect no output: the landed tree is the reviewed evidence tip's.

```bash
git --no-pager status --porcelain=v1
```

Expect exactly ` M progress.md`.

### 8.3 Step 2 — the push

**The value-based secret scan first**, over exactly what the push will send: the same guard the
pre-push hook runs, reading the credential values inside the process and printing only a variable's
name and a path if one is found.

```bash
printf '%s %s %s %s\n' refs/heads/main "$(git rev-parse main)" refs/heads/main "$(git rev-parse origin/main)" refs/tags/land/pres-3 "$(git rev-parse land/pres-3)" refs/tags/land/pres-3 0000000000000000000000000000000000000000 refs/tags/evidence/pres-3 "$(git rev-parse evidence/pres-3)" refs/tags/evidence/pres-3 0000000000000000000000000000000000000000 | python3 scripts/secret_guard.py pre-push origin "$(git remote get-url origin)" && echo SECRET-SCAN-CLEAN
```

Expect `SECRET-SCAN-CLEAN`. A `secret-guard: BLOCKED` line means stop and tell no one the value
(AGENTS.md § Credentials).

```bash
python3 scripts/publication_guard.py tree
```

Expect a PASS line: the landed page is the final build.

```bash
git push origin main land/pres-3 evidence/pres-3
```

Expect `17f354e..<land_sha>  main -> main` and two `[new tag]` lines. The pre-push hook repeats both
guards. GitHub Pages then serves `docs/`.

### 8.4 Step 3 — the Space upload, with the deletion

Rebuild the bundle from the landed tree and check it. Check mode reads no credential for use and
writes nothing remote:

```bash
make wasm
```

```bash
uv run python scripts/deploy_space.py --bundle dist/space-wasm --expect 9028a11869a378ea5c3401a00ad46368e1c9e2f2f9f8732330d32b71af081585 --delete style.css
```

Expect `bundle_sha256` `9028a118…`, `files` 805, `credential_guard` `passed`, `planned_adds` `[]`,
`planned_changes` the nine `public/boosters/*.txt.gz.b64` files (their gzip header byte, A-PRES3-2;
the decoded boosters are identical), `planned_deletes` `["style.css"]`, `declared_matches` true,
and a `before_revision` (`0c550e863711e19abbb35219cf64d45dfb39c888` when read on 2026-09-30,
`pres-3-space-check.json`). If the rebuilt hash differs, stop: the exact reviewed copy is in
`.local/artifacts/pres-3/space-wasm-9028a118/`, and a different bundle needs its own review. If the
deletion set is not exactly `style.css`, stop.

```bash
uv run --with huggingface_hub python scripts/deploy_space.py --bundle dist/space-wasm --expect 9028a11869a378ea5c3401a00ad46368e1c9e2f2f9f8732330d32b71af081585 --upload --delete style.css --record reports/presentation/release-checks/pres-3-space-deployment.json
```

It refuses before any write unless the deletion set is exactly `style.css`; then makes one Hub
commit against the revision it has just read, with the nine changed files and the one deletion;
then lists the tree at the new revision and requires the served file set to equal the bundle by path
and per-file hash. Expect exit 0 and, in the record, `status` `deployed`, `verified` true, `commit`
and `after_revision` set, no mismatched, extra or missing path. `HF_TOKEN` is read inside the
commit and never printed. Pages and the Space do not change atomically: run this soon after step 2.

### 8.5 Step 4 — the A6 public checks, per surface

Each writes a new record; keep a first failure beside its retry. The Playwright commands need
`PLAYWRIGHT_BROWSERS_PATH=/Users/djourno/Downloads/PJM/.local/tools/ms-playwright` (A-PRES3-4).

```bash
curl -s https://hrsi56.github.io/delu-day-ahead-forecast/ | shasum -a 256
```

Expect `<final_page_sha256>` once Pages has deployed (now `f36314e2…`, PRES-2's).

```bash
curl -s https://raw.githubusercontent.com/hrsi56/delu-day-ahead-forecast/main/README.md | shasum -a 256
```

Expect `<final_readme_sha256>`.

```bash
curl -s https://huggingface.co/api/spaces/Yarden-Viktor/delu-day-ahead-forecast | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['sdk'], 'private' if d['private'] else 'public', d['sha'], (d.get('runtime') or {}).get('stage'))"
```

Expect `static public <after_revision from pres-3-space-deployment.json> RUNNING`.

```bash
curl -s https://huggingface.co/spaces/Yarden-Viktor/delu-day-ahead-forecast/raw/main/README.md | shasum -a 256
```

Expect `c92a2666d76255b24d8e0fb159f97bedcbee0a7a948fb6afeac4b02089bb9a67` (the card is unchanged).

```bash
.local/tools/playwright/bin/python scripts/check_reader_paths.py release https://hrsi56.github.io/delu-day-ahead-forecast/ --shots .local/artifacts/pres-3/public-report --out reports/presentation/release-checks/pres-3-public-report.json
```

```bash
.local/tools/playwright/bin/python scripts/check_reader_paths.py demo --engine chrome --engine webkit --viewport 1440x900 --viewport 390x844 --url https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/ --out reports/presentation/release-checks/pres-3-public-demo.json
```

```bash
.local/tools/playwright/bin/python scripts/check_reader_paths.py demo-a11y --engine chrome --engine webkit --viewport 1440x900 --viewport 390x844 --url https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/ --out reports/presentation/release-checks/pres-3-public-demo-a11y.json
```

```bash
.local/tools/playwright/bin/python scripts/check_reader_paths.py states --engine chrome --engine webkit --url https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/ --out reports/presentation/release-checks/pres-3-public-states.json
```

```bash
MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=true uv run python scripts/verify_mlflow_mirror.py verify --target public --out reports/presentation/release-checks/pres-3-public-mirror-postdeploy.json
```

```bash
.local/tools/playwright/bin/python scripts/check_reader_paths.py mlflow-routes --mirror-record reports/presentation/release-checks/pres-3-public-mirror-postdeploy.json --shots .local/artifacts/pres-3/public-mlflow-postdeploy --out reports/presentation/release-checks/pres-3-public-mlflow-routes-postdeploy.json
```

```bash
uv run python -c "import sys; from pathlib import Path; sys.path.insert(0, 'scripts'); import check_links; raise SystemExit(check_links.main(record=Path('reports/presentation/release-checks/pres-3-public-links.json')))"
```

Each passes with `passed` true (the mirror: every expected run and route verified). The states
check forces failures inside the test browser only; it changes nothing on Hugging Face. The demo's
cold start is re-measured on the new bundle (R2): if it differs materially from the page's
measurement, the page's record is updated in a later publication, not by editing the served page.

**The independent public review.** A checker that wrote none of PRES-3's changes reads these
records and the served surfaces fresh, forms its findings before reading earlier reviews, and writes
a new, dated review under `docs/track-b/` with the per-surface identities (§10.3), the §9 matrix it
could apply, first failures and retries, and its PASS / FAIL / INCOMPLETE verdict (§10.4).

### 8.6 Step 5 — the receipt

Fill §8.1's last three columns from those records: the observed identity and UTC time per surface,
the record and its result, and any outstanding action. The closure record's inputs: the landing SHA
and tags; the pushed revision; Pages' served hash; the Space's `after_revision`, the deletion
(`style.css`) and the served-set verification; the MLflow run IDs and the post-deployment mirror and
route records (§6); the independent public review and its verdict; and every first failure with its
retry. The disposition is complete only when every row is verified.

### 8.7 If publication fails

Stop the rollout and name each affected URL and revision. The identities to restore are `main`
`17f354e42c0d6f3199227fe9d29df9f4dc8211e0` (Pages `f36314e28811ed4b7ec41bc73dfd481ddb112815effabfc4e7b3ae74d8edab1d`)
and Space revision `0c550e863711e19abbb35219cf64d45dfb39c888`. The uploaded cp21 runs stay: they
are the committed evidence, and removing a tracking run is not part of any recovery. No force-push,
history rewrite or MLflow change is part of a recovery; a rollback is its own Owner action.


## 9. Applicability matrix

### 9.1 PUBLISH_RULES 1.2, clause by clause

| Clause | Applies | Evidence |
|---|---|---|
| §1.1–1.3 authority, identities, categories | yes | §1 above; the brief pins 1.2 and the anchors; A1–A6 inherited and applied, A7–A9 not triggered (§5d) |
| §2 reader contract and placements; A1, A2 | yes | Release record `pres-3-local-release.json`: headline block ends 800.6 / 801.3 px (desktop, of 900) and 628.6 / 628.7 px (phone); the finding ends 1,677.6 / 1,678.3 px (A2 limit 1,744) and 2,379.5 px (limit 2,420); the terms sit directly beneath the headline; the release rule beside the demo action, outside a disclosure. A1: `test_45::test_the_headline_leads_with_the_rules_verdict_and_names_each_metric`; the fresh reader's answer 1 (`fresh-reader.md`) |
| §3.1 evidence classes; W1–W27 | yes | Badge "Development · post-selection"; `v4.caveat.class`; W22–W26 guards and negative controls (`test_45::test_negative_controls_cp21s_withheld_claims_are_caught`, `test_no_surface_carries_a_withheld_claim`) |
| §3.2 scores, comparisons, uncertainty | yes | §4 above: verdict, rule and date, distance, N, the ratio change with CP-21's own interval, per-period MAE with fold 3 separate; one population (`common-10747h`, 10,747 hours over 448 days); the block split stated as "no demonstrated joint preference", never equivalence; C106's bundling disclosed |
| §3.3 counting | yes | N = 1 for `cp21-adoption`; the target census (12 policies) is its own derived record (`census_sentence`), stated apart from the chart's 8 rows |
| §3.4 provenance and formatting | yes | Every number bound to a record (`make verify`: every bound claim agrees on every surface); `make lint-publication` 0 findings; four significant figures, whole percentages, one decimal for EUR/MWh |
| §4 identity, transitions, branches; A3 | yes | Registry (§2); transition `transition.v3-v4.*` (§5a); the study arms are rows and ladder steps, not branches; `tests/test_43_publish_rules_migration.py`, `test_45::test_the_transition_title_and_the_encoding` |
| §5 architecture; A4 | yes, unchanged order | The section order is PRES-2's; the product documentation is byte-identical (`test_45::test_every_historical_section_is_byte_identical_to_the_published_page`) |
| §5.1 twelve product subjects | unchanged | The released model does not change (§5b) |
| §5.1a, A8 | no | No final-product designation (brief) |
| §5.2 chapter grammar; 2.0 MB budget | yes | `build_pages.py::slot_problems` refuses a chapter missing a slot; page 1,906,528 bytes at the candidate (1.91 MB), under 2.0 MB; compaction waits for v5 (§14) |
| §6 charts, discovery; A5 | yes | Discovery: 33 routes in both engines at both placement sizes, by mouse, keyboard and deep link (`pres-3-local-release.json` `discovery`); smallest chart text 12.21 px at 320 px and 14.58 px at 390 px; no overlaps or clipping; shape and direct labels beside colour |
| §7.1 product contract | yes, unchanged | The demo still runs v1: `pres-3-local-demo.json` (cold start 10.2–12.8 s, controls respond, 0 console errors, 0 failed requests), `pres-3-local-demo-a11y.json` (named controls, no target under 44 px, keyboard), `pres-3-local-states.json` (loading, failure, retry); the bitwise equivalence gate passes (`tests/test_22_wasm_equivalence.py`) |
| §7.2 live, §7.3 final-product Space (A7, A9) | no | Not triggered (brief; §1.3) |
| §8 public surfaces | yes | README, cards and export follow from the registry (`make verify`: headline, names and statuses agree across the page, README, both Space cards and the export; zero fetches); cards unchanged; MLflow per §6 |
| §9 browser and accessibility matrix | yes | `pres-3-local-release.json`: Chrome 154.0.8037.58 and WebKit 26.6 at 1440 × 900, 768 × 1024, 390 × 844, 360 × 780, 320 × 640 and the emulated iPhone 393 × 659; accessibility trees, keyboard, touch, contrast, 200% zoom and 320 px reflow; no failed request, HTTP error or resource after the document. No real Safari, iPhone or screen reader was used |
| §10.1 editorial and independence | yes | `editorial.md`; `integration.md` by a fresh Critic that wrote none of the changes |
| §10.2 fresh reader | yes | `fresh-reader.md`: the six unchanged questions, closed-state screens only, answers preserved |
| §10.3, A6 public checks | the Owner's | §8.5 below: every surface, by a checker that wrote none of the changes |
| §10.4 verdict | yes | `integration.md` |
| §11 packet and sequence | yes | This packet; the order in §7 |
| §12 baseline coverage | yes | Plan invariants 1, 3, 10, 13, 14, 16, 17, 18, 19, 21 and 26 in particular: zero runtime network (`make verify`); generated outputs only regenerated (determinism in §7); nothing dated after 2026-04-07; `pyproject.toml` and `uv.lock` unchanged; no public text on retired tooling; no placeholder reaches `main` (`make publication-guard` passes only on the final tree); planned work unscored and unnumbered |
| §13 acceptance record | yes | §9.2 |
| §14 triggers | yes | "v4: the Owner decides the encoding" — decided (D6); "v5 or size-budget breach" — not reached |
| §§15–17 | read | A1–A6 applied as above; A7–A9 not triggered |

### 9.2 The §13 acceptance record

| Area | Record |
|---|---|
| Authority | §1; PUBLISH_RULES 1.2 `a43ac020…`; v21-r8 `81d61271…`; the brief `57a8c7fb…`; A7–A9 N/A |
| Identity | Branch `gauntlet/pres-3`; `<final_candidate_sha>`, `<evidence_tip_sha>`; the served identities today and after the Owner's steps (§8) |
| Claims | §§3–4; `make verify`; `test_45` re-derivations with negative controls |
| Reader | Placements (§9.1); `fresh-reader.md` |
| Journey | §5a; the study arms as ladder steps and rows; planned list per §9.5 |
| Content | Product documentation byte-identical; v4's chapter concise, with its details in named disclosures |
| Charts | §9.1 §6 row; §5c routes |
| Product | §9.1 §7.1 row |
| Accessibility | §9.1 §9 row |
| Tracking | §6; the upload, mirror verification, REST and browser routes and the index (§7) |
| Release | The final build, guards and tests (§7); `integration.md` at the candidate and its focused recheck at the final SHA |
| Public check | The Owner's (§8.5) |
| Follow-up | `editorial.md`, the advisory log's PRES-3 section, §10 |
| Final product, daily panel, business, final-product Space | not applicable (not triggered) |

### 9.3 The runbook

| Runbook item | Where | Evidence |
|---|---|---|
| §2.1 entry | `registry.py::_ENTRIES` (`v4`, three study arms; predecessor `v3`) | `test_35` (fields, `transition_problems`), `test_45` (draft equality) |
| §2.2 checkpoint | `registry.py::CHECKPOINTS["CP-21"]` | `test_45`, `test_34` |
| §2.3 evidence tag | `registry.py::EVIDENCE_TAGS["evidence/cp-21"]` = `1d13f99`, 2026-09-30 | `test_45` |
| §2.4 rule | `registry.py::RULES["cp21-adoption"]`, set 2026-09-29 | `test_45::test_negative_control_a_rule_date_the_anchor_does_not_state_is_refused` |
| §2.5 comparison order | `registry.py::COMPARISON_ORDER` with v4 first; `COMPARISON_EXPERIMENT = "CP-21"` (the same population, `common-10747h`; 2,254 shared cells equal CP-20's) | `test_45::test_the_comparison_moved_to_cp21s_rows_which_equal_cp20s_on_every_shared_policy` |
| §2.6 crisis order | `registry.py::CRISIS_ORDER` = (v2, v3, v4); v3's chapter pinned to `V3_CRISIS_ORDER` | `test_45::test_negative_control_a_v3_chart_fed_the_current_generation_cannot_redraw_silently` |
| §2.7 sources | `research.py::SOURCES` CP-21 blobs; `records()` validates 14,948 records | `test_29`, `test_36`, `test_45` |
| §2.8 criteria | `derived.py::CRITERIA_FILES["CP-21"]`; `ADOPTION_RULES` for the rule's verdict | `test_36`, `test_45::test_the_derived_headline_quantities` and its negative control |
| §2.9 change | `derived.py::RATIO_CHANGES` (the ratio interval from CP-21's own draws) | `test_45` |
| §2.10 periods | `derived.py::PERIOD_SUBJECTS` including v4; fold 3 the stress period | `test_45` |
| §2.11 claim map | `research_claims.py::CLAIM_MAPS` includes `cp21-claims.md` | `test_30` (every block renders from its claim), `test_45` |
| §2.12 blocks | `research_claims.py::BLOCKS` `v4.*`; the headline through `headline_template`'s adoption branch | `test_45`, `make lint-publication` |
| §2.12a transition | `transition.v3-v4.*` (title, change, comparator, result, limits; no `predecessor`: the comparator is the predecessor) | `test_43`, `test_45` |
| §2.13 slots | `build_pages.py::v4_slots`, `v4_chapter`; details under `detail_head`; routes from `explore_routes` | `slot_problems`; A5 discovery |
| §2.14 chapter sequence | `build_pages.py::chapter_sequence` | `test_38` |
| §2.15 run charts | `build_pages.py::CHARTS_BY_RUN["cp21/HGL"]`; `cp20/HG` pinned (`PINNED_CHARTS`) | `test_34::test_candidate_runs_carry_the_pages_own_charts` |
| §2.16 tokens | `build_pages.py::TOKENS["v4"]` `#B45309`, a filled diamond (D6) | `test_45::test_the_transition_title_and_the_encoding` |
| §2.17 export | `mlflow_export.py::CHECKPOINTS["cp21"]` | `test_34`, `tests/cp21/test_draft_export.py`, `test_45` |
| §2.18 tests | `tests/test_45_pres3_v4_publication.py`; updates to tests 34–39 and 43 | full pytest (§7) |
| §2 "What follows without an edit" | opening, rail, jump row, lineage, `overview_panels`, README glance and generation list, both cards' model line (unchanged: v1), run set and routes | `make verify`; `test_38`; `test_42` |
| §2 "Limits to watch" | placements, 12 px chart text, 2.0 MB budget | §9.1 |
| §1 order | editorial → fresh reader → independent check → upload → final build → focused recheck → the Owner's steps | §7 |
| §1a receipt | §8.1 | — |
| §8 routes | `experiment`, `compare:v4` verified by REST and in both engines before the final build | §7 |
| §9 checks | every item | §7 |

### 9.4 The CP-21 publication plan (scope)

| Item | Evidence |
|---|---|
| §4, outcome A, steps 1–18 | §9.3 |
| §4 "Headline" | §4 above; the orientation carries each change as a share of v3's score with CP-21's own interval |
| §4 "Released product" | v1 unchanged; the opening pairs research v4 with released v1 (`test_45::test_the_opening_pairs_research_v4_with_released_v1`) |
| §4 "Limits to check" | §9.1; compaction waits for v5 |
| §6 every surface | §8.1; the `style.css` deletion is in the Space step (§8.4) |
| §7 sequence | §7 and §8 |

### 9.5 Research anchor v21-r8 §18.5 — the planned list

"Planned, not evaluated" carries **4.6 · A distributional neural network** (DDNN) alone, with a
question that names v4 as the comparator and commits to no design; 4.5 has left the list (CP-21
evaluated it); every other item keeps its content; W14 is unchanged. No "TabPFN" or "tabular
foundation model" appears on the page, the README or either Space card
(`test_45::test_the_planned_list_is_corrected_on_every_generated_surface`,
`test_the_other_planned_items_keep_their_content`, `test_the_claim_guard_w14_is_unchanged`, and
their negative controls). Historical records that name TabPFN stay as written.

## 10. Advisories carried with this packet

- The editorial review's recommendations deferred with reasons (6, 11, 13 in part, 14) and its
  proposed amendment PA1, in the advisory log's PRES-3 section; A-PRES3-1 to A-PRES3-7.
- The fresh reader's observations and answer 6 (`fresh-reader.md`).
- Any recommendation in `integration.md`.

None is a violation of an effective rule.
