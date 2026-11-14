# PRES-6 landing — 2026-11-15

**PRES-6 is landed and deployed. The report now leads with the final product, in A8's order: the product opening,
How the product works, Product results, Business insights, then How the models compare. Product results shows v6's
development-period results from CP-28's stored forecasts. Business insights states that no economic evaluation exists.
The Space and MLflow are unchanged, and 4.7T is untouched.**
- **What is published:**
  - **the order (A8):** v6's results and their business meaning come before any model comparison. The comparison and
    the later sections are unchanged, apart from Integration review 4's wording recommendations;
  - **Product results, for v6 (A1 in the frozen records; policy `720fc581…`),** on development delivery days only,
    by rules committed before the numbers:
    - forecast against observed on three rule-chosen days and in ten forecast bins;
    - the daily error over time against the similar-day naive;
    - the error by material regime, with counts and block-bootstrap intervals;
    - coverage together with width at 50, 80 and 95%;
    - the explanation: CP-17-probe's committed attribution of v6 on two development days, labelled as one fitted
      model's attribution, never causality. Nothing was fitted or recomputed;
  - **Business insights:** the intended use, the measured implications with their limits, and the gap. No decision
    policy, cost model or trading simulation exists, and the page shows no profit figure;
  - **the README's glance** carries the same claims;
  - **the tools:** the link checker fails a redirect that ends on another host and records every hop; the receipt
    normalizes the Space's page by CP-18c's rule.
- **Next:**
  - 4.7T, no earlier than 2026-12-04, and the publication of its result;
  - the Owner's decision 30 (2026-11-15), no page-size limit, enters PUBLISH_RULES at the next publication round;
  - the follow-ups below.

## Identities

| Item | Value |
|---|---|
| Brief | `docs/track-b/evidence/pres-6/issued-brief.md`, SHA-256 `bdb78f02894896d2ee1f249355d23351f972cdb217d4d906d22561172f40e5f6`, issued at `87811abc` |
| Anchors | `capstone_v21.md` v21-r20 (`80341681…`) and `docs/PUBLISH_RULES.md` 1.5 (`1bc0c523…`), unchanged |
| The Owner's mandate | Decisions 27 and 28, and his question of 2026-11-14 |
| The Orchestrator's rulings during the round | O46, O48, O49 and O49a |
| Final candidate (the focused recheck binds here) | `4ecfcd094f4b103b57a5f16013a8089ccbd3e9f2`. Verdict `docs/track-b/evidence/pres-6/integration.md`. Integration review 1 failed at `f8fcd723` (one finding, fixed); review 2 passed at `6dfca90f`; review 3, the final verdict, passed at the final candidate |
| Evidence tip / `evidence/pres-6` | `f497879f96fd87047469a9d5cf285c7421f7f916`. It adds only `integration.md` and the packet's record of it to the candidate |
| Squash landing / `land/pres-6` | `fe2460fc0147e5784e9eed2d2313b06161b58a13`, on `main` `8c5f7df2` (the runner's data-only commits after `29b6431e`). Its tree `2b6ff445b09acc8c2edc281c09c86385ba958e5a` equals `git merge-tree --write-tree 8c5f7df2 f497879f`. PRES-6's 45 paths equal the evidence tip's, and every other path equals `main`'s. +82,829 / −68 |
| The page | `docs/index.html`, SHA-256 `5e294d40790f3415c14cf932e94f1351e2e99a0b84d6efd3d2321046d7eccdaa`, 1,997,873 bytes (2,127 under the 2.0 MB budget). README `da9ae187766c895d102676b16a5870540029d471b26687fe78cc3319edc77e1a` |
| Publication packet | `docs/track-b/evidence/pres-6/publication-packet.md` |

## The return and the landing

- **The Lead returned PASS.** `gauntlet.py return` found 0 problems; `citations` found no document naming the branch.
- **The Orchestrator's own checks:**
  - **The paths.** All 45 are inside the brief's allowed paths: the report, the README and the build record; the
    build, the claim layer and their tests; the link checker and the receipt with their tests; the reader-path
    checker under O48; the research content; `reports/pres6/`; the release records; and the evidence. Nothing changed
    under the anchors, PUBLISH_RULES, `AGENTS.md`, `progress.md`, `src/cp18/`, `space-product/`, `live/`, the
    workflows, `tests/cp18c/`, `uv.lock` or `pyproject.toml`.
  - **The MLflow export's manifest** gains seven source entries for `reports/pres6/product-results/` and changes
    nothing else. PRES-5's packet cites its earlier hash as a historical record, and no test binds it. MLflow itself
    is unchanged.
  - **The red line.** Product results' rows end on 2026-09-06. The only date the page adds after the red line is the
    evidence label "frozen 2026-11-15".
  - **The evidence date.** The tip's commit date and the registry's `evidence/pres-6` date are both 2026-11-15.
  - **No overlap with `main`.** Between the branch point and the landing, `main` changed only CP-18c's landing record
    and the runner's `live/` paths.
- **The history-free CI** (`CI=true`, Python 3.12, Git's global configuration hidden):

  | Commit | Result | Log |
  |---|---|---|
  | `fe2460fc`, the squash | every step exited 0: 3,367 passed and 74 skipped | `.local/artifacts/pres-6/land-ci312.log` (`357fda61…`) |

- **The secret guard and the leak scan** passed on the outgoing refs before the push, and the publication guard
  passed on the tree. No daily job ran during the push (the last finished at 18:50Z the day before).
- **GitHub's CI** passed on all three refs: `main` and `land/pres-6` at `fe2460fc` (3,356 passed, 85 skipped on
  `main`), and `evidence/pres-6`.

## The public checks (packet §8.5)

| Surface | Intended | Observed, UTC (2026-11-14) | Record |
|---|---|---|---|
| GitHub `main` | `fe2460fc` | `fe2460fc`, 23:08:52Z | `reports/presentation/release-checks/pres-6-publication-receipt.json`: PASS on the first attempt |
| Pages | `5e294d40790f3415c14cf932e94f1351e2e99a0b84d6efd3d2321046d7eccdaa`, 1,997,873 bytes, the focused recheck's page | the same, served from 23:08:41Z | the same: PASS |
| README | `da9ae187…` | the same | read from `raw.githubusercontent.com` |
| Space files | the runner's publication at revision `91898ce5`, assembled as the Disclosures say, identity `50ed50ed…`, 861 files | revision `91898ce5…`, every file equal, none extra or missing | the receipt: PASS |
| Space direct page | the build's `index.html`, `7b962a0f…` | equal after `cp18.publish.normalized`, the receipt's new rule | the receipt: PASS |
| Public MLflow | the committed export, 105 runs | 105 found, on the first attempt | `pres-6-postdeploy-mlflow-mirror.json` |
| Links | every destination 200 on the host it names | 0 failed and 0 cross-host redirects. Every hop is recorded; the Space's root redirects to its own `index.html`. DagsHub's gated pages answer 302 to its own login, probed without following, as before | `pres-6-postdeploy-links.json` |
| The report in browsers | §10's checks; A2 on the product finding (A8) | passed: Chrome and WebKit at every width and the emulated iPhone, 54 routes each. The product finding ends at 1,667.6 px of 1,744 at 1440 and 2,369.5 px of 2,420 at 390 | `pres-6-public-report.json` |
| MLflow routes in browsers | every verified route | passed, Chromium and WebKit | `pres-6-public-mlflow-routes-postdeploy.json` |

## A12

**Not triggered.** The served page and README are the focused recheck's, byte for byte, the public MLflow equals
the committed export, and every required public check passed on its first attempt. The two points where packet §8.6
said an independent check could add something are covered by the public records: the deployed order and the
product finding's placement in both engines (`pres-6-public-report.json`), and the new link rule run live
(`cross_host_redirects` empty). No independent post-deployment check was run (O50).

## Disclosures

- **The runner's Actions artifact is named `daily`,** not `pipeline` as packet §8.5 says, and it holds only the
  Space's changed files (12 of them, the dotfile `.gitattributes` dropped by the upload) and the dated bundle. The
  Orchestrator assembled the Space's full build from CP-18c's publication 3 build, the run's files, the run's bundle
  as `payloads/`, and the Space's `payloads/artifact-arrays.npz`, which the runner deletes before the upload. Two
  stale payloads of 2026-11-14 were removed. The assembled build equals the build's own record
  (`app/space-build.json` and `app/history-files.json`, 860 files) byte for byte. Its identity is
  `50ed50ede272702d4f95e2f04a765e2e662aca6fea40f7124ed71d16a66cf70f`. The runner's own served-identity check had
  already passed at revision `91898ce5` (878 files, no problem).
- **The Lead's disclosures** are in packet §10.2: Integration review 1's false premise and its correction, §0's two
  corrections before use, a duplicate `regime_table()` found before review, the explanation chart's labels, the
  live-recorded fixtures, the ledger's bounds, and one stopped test run.
- **Usage-limit pauses:** two in the Lead's round, recorded in its ledger. Machine-hours: at most 7.4 of 10.

## The Orchestrator's rulings at the landing (decision 27)

- **O50: A12 not triggered** (above).
- **O51: PRES-6's open presentation items** (packet §10.3):
  1. A2's phone margin of 50.5 px: accepted. Anything added above the product finding is re-measured.
  2. The page budget's 2,127 bytes: superseded by the Owner's decision 30, no page-size limit.
  3. The naive's coverage not shown: accepted.
  4. The explanation on two development days: accepted. A population attribution needs its own authorized run.
  5. The receipt's Space rows against a runner-published Space: run, and passed against the assembled build.
     The runner's artifact holds only the changed files, so the receipt needs the assembly step. That is a tooling
     follow-up.
  6. Business insights without a chart: accepted (A8).
  7. The comparison chart's clipped v6 interval-score marker on phones: a small fix in the next presentation round.
  8. The fresh reader's confusions in unchanged sections: one glossary-and-wording pass in the next presentation
     round.
- **Follow-ups:**
  - for the next presentation round: items 7 and 8; the page budget's removal (decision 30); the receipt against
    the runner's partial artifact;
  - for CP-18d (decision 31): the late load forecast, the earlier acquisition, the claim over a moved `main`, and
    the Space's wording (O45 item 8 and PRES-5's A12 review);
  - the economic evaluation that Business insights names as its gap. The rules allow it only after the Owner
    authorizes a use case and its contract (PUBLISH_RULES §5.1a; the anchor's §16.3). It was put to the Owner on
    2026-11-15.
