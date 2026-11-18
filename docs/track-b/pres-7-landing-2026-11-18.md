# PRES-7 landing — 2026-11-18

**PRES-7 is landed and deployed. The report's Business insights now shows what v6's forecasts were worth to a battery
on the development days: CP-29's cumulative profit chart, with every limit stated. The Space and MLflow are unchanged,
and 4.7T is untouched.**
- **What is published** (decision 32's evaluation, from `reports/cp29/daily.csv` only):
  - **the profit chart:** the cumulative net profit of a price-taking 1 MW / 2 MWh battery over the 2,068 development
    days, scheduled the day before by the median rule from v6's, the similar-day naive's and perfect forecasts and
    settled at the cleared day-ahead price, with doing nothing as the zero line. Labelled simulated, development,
    post-selection;
  - **beside it, CP-29's claims C1101–C1108 and PRES-7's C1201–C1204:**
    - v6 earned 89.5% of perfect foresight's profit and the naive 76.6%;
    - v6 − naive, paired over the same days: +37,080 EUR [+32,320, +42,310];
    - v6 against v5 on v5's days: no advantage shown (an interval spanning zero);
    - also the losing days, the drawdown, the wear-cost sensitivity, the regimes, the risk-aware rule and the
      untraded days;
  - **the limits on the page:** a simulation, not realized income; day-ahead arbitrage only; a price-taker; hourly;
    post-selection; not a trading recommendation; no return or payback;
  - **"Not evaluated." replaces the gap sentence:** intraday, reserves, a real battery's costs and the live record;
  - **the README** carries the same business claims, through the claim layer;
  - **beside it:**
    - **decision 30:** the page-size assertions are removed, and the size is measured and recorded;
    - **O51 item 7:** the comparison chart's axis now holds v6's interval-score marker;
    - **O51 item 8:** one glossary-and-wording pass over the opening and the comparison. No number changed.
- **Next:** 4.7T, no earlier than 2026-12-04, and the publication of its result; the wording items of O69 in the next
  presentation round.

## Identities

| Item | Value |
|---|---|
| Brief | `docs/track-b/evidence/pres-7/issued-brief.md`, SHA-256 `b6a45b6002969c238547938661841e74f7b44f343fc60e3a56ced02879451175`, issued at `a5db292a` (envelope `639f332d…`) |
| Anchors | `docs/PUBLISH_RULES.md` 1.5 (`1bc0c523…`), with decision 30 superseding its page budget; `capstone_v21.md` v21-r20 (`80341681…`); the contract (`21a92085…`), all unchanged |
| The Orchestrator's rulings during the round | O62, O63 (CP-29's round-scoped test replaced), O66 (the hold for CP-18d) |
| Final candidate (the focused recheck binds here) | `e464b69e80902d029272628e6c35fa21fb9c1ed3`. Verdict `docs/track-b/evidence/pres-7/integration.md`: PASS. Integration review 1 passed at the candidate `364ac020` (`integration-review-1.md`) |
| Evidence tip / `evidence/pres-7` | `2264b335ac834ab0e587467e8f59d23952401b47`. It adds only `integration.md` |
| Squash landing / `land/pres-7` | `a145acaf330870c0ac7d6489b15e74fb40414456`, on `main` `bf3032c5` (CP-18d's close commit, after the runner's data-only commits). Its tree `9f4d23b8ea9bc6f9df32116bcedcbde4ddd6154d` equals `git merge-tree --write-tree bf3032c5 2264b335`. 29 paths |
| The page | `docs/index.html`, SHA-256 `7fd8dd2f462da049942dd438a14c8538bdc09536bdfa8760bfffbbd73abafc5e`, 2,082,672 bytes (+84,799 over PRES-6's; no limit, decision 30). README `efe8c08da7d03861e9b6075e6bc28f8fe321d749d44e56e965699b94547c07d1` |
| Publication packet | `docs/track-b/evidence/pres-7/publication-packet.md` |

## The return and the landing

- **The Lead returned PASS.** `gauntlet.py return` found 0 problems; `citations` found no document naming the branch.
- **The Orchestrator's own checks:**
  - **The paths.** All 29 are inside the brief's allowed paths: the report, the README and the build record; the build,
    the claim layer and their tests; CP-29's one test under O63; the research content; the release records; and the
    evidence. Nothing changed under the anchors, PUBLISH_RULES, the contract, `src/cp29/`, `reports/cp29/`, `src/cp18/`,
    `space-product/`, `live/` or the workflows.
  - **No overlap with `main`.** Between the issue and the landing, `main` changed CP-29's and CP-18d's paths and
    `live/` only; none is a PRES-7 path.
  - **The staged paths equal the evidence tip's,** and nothing else is staged.
  - **The evidence date.** The tip's commit date and the registry's `evidence/pres-7` date are both 2026-11-18.
- **The history-free CI** (`CI=true`, Python 3.12, Git's global configuration hidden):

  | Commit | Result | Log |
  |---|---|---|
  | `bf3032c5`, CP-18d's close | every step exited 0: 3,579 passed and 79 skipped | `.local/artifacts/cp-18d/close-ci312.log` (`7591d2f0…`) |
  | `a145acaf`, the squash | every step exited 0: 3,607 passed and 80 skipped | `.local/artifacts/pres-7/land-ci312.log` (`8e48c579…`) |

- **The secret guard and the leak scan** passed on the outgoing refs, and the publication guard passed on the tree.
  One push carried CP-18d's close commit and PRES-7's landing, at 20:42 UTC, while the daily chain's link was in its
  Linux tick, with no macOS job running.
- **GitHub's CI** passed at `a145acaf` (`invariant-tests` run 44393367056).

## The public checks (packet §8.5)

| Surface | Intended | Observed, UTC (2026-11-18) | Record |
|---|---|---|---|
| GitHub `main` | `a145acaf` | `a145acaf`, 20:42:56Z | `reports/presentation/release-checks/pres-7-publication-receipt.json`: PASS on the first attempt |
| Pages | `7fd8dd2f…`, 2,082,672 bytes, the focused recheck's page | the same, 20:42:57Z | the same: PASS |
| README | `efe8c08d…` | the same | read from `raw.githubusercontent.com` |
| Space files | the runner's publication of run 44344692957, taken from its `daily` artifact (CP-18d's full build, verified by `cp18.runner_artifact verify`) with the fitted arrays fetched from the Space; identity `9795945be840bd45784b988a40a2615c814a91aaa4726bfa0367823e747a1589` | revision `cf9a429a…`, every file equal, none extra or missing | the receipt: PASS |
| Space direct page | `7b962a0f…` | equal after `cp18.publish.normalized` | the receipt: PASS |
| Public MLflow | the committed export, 105 runs | 105 found | `pres-7-postdeploy-mlflow-mirror.json`: PASS |
| Links | every destination 200 on the host it names | 0 failed and 0 cross-host redirects; every hop recorded; DagsHub's gated pages answer 302 to its own login | `pres-7-postdeploy-links.json` |
| The report in browsers | §10's checks; A2 on the product finding | passed on the first attempt (21:03Z): Chrome and WebKit at every width and the emulated iPhone, 59 discovery routes each, the profit chart's route included. The product finding ends at 1,714.6 / 1,715.3 px of 1,744 at 1440 and 2,407.5 / 2,407.3 px of 2,420 at 390, the local release check's values | `pres-7-public-report.json` |
| MLflow routes in browsers | every verified route | passed on the first attempt (21:04Z), Chromium and WebKit, 11 routes | `pres-7-public-mlflow-routes-postdeploy.json` |

## A12

**Not triggered.** The served page and README are the focused recheck's, byte for byte; the public MLflow equals the
committed export; and every required public check passed on its first attempt. The points where packet §8.6 said an
independent check could add something are covered by the public records: the deployed Business insights and the
product finding's placement in both engines at every width (`pres-7-public-report.json`), and every Space link checked
without following redirects (`cross_host_redirects` empty). No independent post-deployment check was run (O70, as
O50 at PRES-6).

## Disclosures

- **The Space's build for the receipt came from the runner's artifact,** not assembled: CP-18d's landing made the
  artifact keep the whole build. This closes PRES-6's O51 item 5.
- **The Lead's disclosures** are in packet §10.2. Among them:
  - C1103 is reworded on every surface, its claim and records unchanged;
  - the lint's precision rule gains the one-decimal daily money case;
  - the comparison's axis widens on both variants;
  - release-check attempt 1 was stopped and wrote no record;
  - the A2 phone margin narrows to 12.5 px.
- **The prerelease's two known exceptions** (packet §7):
  - the 3.12 interpreter pin of `test_refreeze17c`, as at PRES-5 and PRES-6;
  - one link answering 404 before the evidence tag was pushed. The public link check after the push found no failure.
- **The O66 hold:** PRES-7 waited, from 2026-11-18 14:41 to 16:15 UTC, so that CP-18d could meet its deadline within
  the account's shared usage limit.
- **Usage-limit pauses:** three in the Lead's round, recorded in its ledger. Machine-hours: at most 5.4 of 10.

## The Orchestrator's rulings at the landing (decision 27)

- **O69: PRES-7's open items** (packet §10.3), as the Lead proposed:
  1. A2's phone margin of 12.5 px is accepted; anything added above the product finding is re-measured;
  2. the status-word lint's reach, "among 7 arms" in v6's chapter and the fresh readers' other confusions go to the
     next presentation round, with CP-18d's "runs daily" sentence (O67);
  3. the receipt against the runner's artifact: closed;
  4. CP-29's open item 1 stays with the round that applies the contract to the live record;
  5. the release check's `page_sha256` field goes to a later tooling round.
- **O70: A12** (above).

## Reclamation

`gauntlet/pres-7` was reclaimed after the public checks: its bundle is
`.local/artifacts/pres-7-reclaim-20261118/gauntlet-pres-7.bundle` (verified), the evidence tag `evidence/pres-7` keeps
its tip, and its worktree is removed. No live document names the branch.
