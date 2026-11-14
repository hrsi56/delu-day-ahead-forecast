# PRES-5 landing — 2026-11-14

**PRES-5 is landed and deployed. The report and the README publish the research since v5, with "v6 · DDNN-2 alone"
(A1 in the frozen records) in v5's comparison, CP-26's re-baseline, CP-28's selection, the freeze with 4.7T's
registered terms, and the live product. MLflow holds CP-26's and CP-28's runs. 4.7T is untouched.**
- **What is published:**
  - **v6 in v5's comparison,** on v5's own 10,747 hours over 448 days: −6% [−9%, −2%] in MAE and −11% [−15%, −8%] in
    interval score against v5, development data, post-selection. v5's and the naive's rows are CP-24's, unchanged.
    v6 is never "adopted" by v5's rule;
  - **CP-26's every-day results,** beside the five periods and never pooled with them;
  - **CP-28's selection:** the rule, the seven arms and the result;
  - **the freeze** (CP-17, CP-17b, CP-17c; policy `720fc581…`) **and 4.7T's registered terms,** as its
    pre-registration;
  - **the product:** v6 "final candidate · pending 4.7T", the live Space linked with "prospective evaluation in
    progress", no live number on the report, and v1 the historical demo.
- **After the deployment, one public defect was found and fixed (O44).** For about 55 minutes the link to v1's
  historical demo sent readers to an unrelated profile. The Disclosures below give the details.
- **Next:**
  - the live product's first runner day, 2026-11-15;
  - 4.7T, no earlier than 2026-12-04;
  - the publication of its result, with A8's product-first order (O38).

## Identities

| Item | Value |
|---|---|
| Brief | `docs/track-b/evidence/pres-5/issued-brief.md`, SHA-256 `9eb2a58433f41739fc22744854c4c55b099cc05ca729b677e9b3b5ccef87ebc3`, issued at `3c8e158c` |
| Anchors | `capstone_v21.md` v21-r20 (`80341681…`) and `docs/PUBLISH_RULES.md` 1.5 (`1bc0c523…`), unchanged |
| The Owner's mandate | Decisions 25, 27 and 28 |
| The Orchestrator's rulings during the round | O25–O28, O30, O34, O38 and O39 |
| Final candidate (the focused recheck binds here) | `300926def8a841848ad02a74c25a5e0291b37f20`. Verdict `docs/track-b/evidence/pres-5/integration.md`, SHA-256 `4b1924dfb2d0cfe3515316c837d8e2158c45895b0e932e924bb91a98c27cb177`. Integration review 4's PASS at `48f56b0e` is `integration-review-4.md` (`fce6c28c…`) |
| Evidence tip / `evidence/pres-5` | `511e91e3e312f317dcc82f9fc33bf7aa79b5f889`. It adds only the two verdict files to the candidate |
| Squash landing / `land/pres-5` | `8bcfc4546979a11a1f7717df1b6bc526800236e3`, on `main` `0be84bdd` (CP-18c's closure). Its tree `1bbf616f6414aee9dd58c3b941abd1a6ebadd571` equals `git merge-tree --write-tree 0be84bdd 511e91e3`. PRES-5's paths equal the evidence tip's, except the one file both rounds changed, `tests/test_24`, which carries both. Every other path equals `main`'s. 75 files, +46,440 / −334 |
| The Orchestrator's commits after it | `d1061484` (O43, a test-only merge repair), `eac95cae` (O44, the history link), `50d51507` (O44, a test-only fix for the history-free reproduction) |
| Publication packet | `docs/track-b/evidence/pres-5/publication-packet.md` (`2b67c80c…`) |
| Reclaim bundle | `.local/artifacts/pres-5-reclaim-20261113/gauntlet-pres-5.bundle`, verified. The branch is deleted and `evidence/pres-5` keeps it |

## The return and the landing

- **The Lead returned PASS.** Integration reviews 1 to 3 failed, and each was repaired. Review 4 passed at
  `48f56b0e`, and the focused recheck passed at the final candidate. `gauntlet.py return` found 0 problems, and
  `citations` found one historical citation of the branch (CP-18c's issued brief), which is never repointed.
- **The Orchestrator's own checks:**
  - **The paths.** Every path is inside the brief's allowed paths: the report and its build and tests, the README,
    the research content, the registry, `reports/pres5/`, the presentation records and the evidence. Nothing changed
    under the anchors, PUBLISH_RULES, `AGENTS.md`, `progress.md`, the exposure ledger, `src/cp17*`, `src/cp18/`,
    `src/cp25/`, `space-product/`, `live/`, the workflows, `uv.lock` or `pyproject.toml`.
  - **The red line.** The page's dates after 2026-09-06 are labels only: evidence and freeze dates, and 4.7T's
    registered window 2026-09-07..12-05. No market number shows a later day.
  - **The evidence date.** The tip's commit date and the registry's `evidence/pres-5` date are both 2026-11-13.
- **The history-free CI** (`CI=true`, Python 3.12, Git's global configuration hidden):

  | Commit | Result | Log |
  |---|---|---|
  | `8bcfc454`, the squash | 1 failed, 3,296 passed and 72 skipped: CP-18c's wall test, merged with PRES-5's surfaces (O43) | `.local/artifacts/pres-5/land-ci312.log` (`bb304665…`) |
  | `d1061484`, the merge repair | every step exited 0, 3,297 passed and 72 skipped | `repair-ci312.log` (`12c0a0c9…`) |
  | `eac95cae`, the link fix | 1 failed, 3,297 passed: the evidence-date test in the reproduction's single commit, dated after midnight; the next commit fixes the test | `fix1-ci312.log` (`d0158478…`) |
  | `50d51507` | every step exited 0, 3,297 passed and 73 skipped | `fix2-ci312.log` (`83ce23ab…`) |

- **The secret guard and the leak scan** passed on the outgoing refs before each push, and the publication guard
  passed on the tree.
- **GitHub's CI:**
  - `main` passed at `d1061484` (3,285 passed, 84 skipped) and at `50d51507` (3,286 passed, 84 skipped);
  - `evidence/pres-5` passed;
  - `land/pres-5` failed on exactly the one test that O43 repairs. That run is kept as the record of the conflict.

## The public checks (packet §8.5)

| Surface | Intended | Observed, UTC | Record |
|---|---|---|---|
| GitHub `main` | `50d51507` | `50d51507`, 22:56:57Z | `reports/presentation/release-checks/pres-5-fix-1-publication-receipt.json`: PASS |
| Pages | `983a75c44b0f93dabd183ee810158aefbfa62adfb5545b4a433afe4b5bbb9475`, 1,848,955 bytes | the same, 22:56:45Z. The first deployment served the reviewed `2fc5bd0a…` at 22:02:33Z | the same: PASS (and `pres-5-publication-receipt.json` for the first) |
| README | `bc98e9cc…` (first `eb76fabf…`, the reviewed one) | the same | read from `raw.githubusercontent.com` |
| Space files | CP-18c's publication 3 build, `858968…` over 859 files | revision `ec97c54f…`, every file equal | the same: PASS |
| Space direct page | the build's `index.html`, `7b962a0f…` | FAIL in the receipt, whose normalizer removes only the old `window.huggingface` script. With CP-18c's normalization (`cp18.publish.normalized`), the served page equals the build | the receipt, and the Orchestrator's check |
| Public MLflow | the committed export, 105 runs | 105 found: after 2 retries the first time, and on the first attempt the second | `pres-5-postdeploy-mlflow-mirror.json`, `pres-5-fix-1-postdeploy-mlflow-mirror.json` |
| Links | every destination 200 | 0 failed. The first run's pass on the bare `/history/` was false: it followed the redirect | `pres-5-fix-1-postdeploy-links.json` |
| The report in browsers | §10's checks and §1's placements | passed: 48 routes each in Chromium and WebKit at 1440 and 390 | `pres-5-public-report.json` |
| MLflow routes in browsers | every verified route | passed, Chromium and WebKit | `pres-5-public-mlflow-routes-postdeploy.json` |

## A12

**Triggered** twice: the served page and README differ from the reviewed ones by the O44 link targets, and the
receipt's direct-page row failed without a passing retry. **The independent check passed**
([review](pres-5-a12-postdeploy-review-2026-11-14.md), SHA-256
`7632db7c249ff6501be1690701898f90188fd382255d1d13cdb72d65f558aba0`). Its checker wrote none of PRES-5 and formed its
findings before reading the earlier reviews.
- **The served surfaces.** The page and the README each differ from the reviewed ones by exactly the three
  `index.html` insertions in the history links.
- **The links.** 59 were checked without following redirects, and none leaves the site it names. The old bare
  route is on neither surface.
- **The Space.** After CP-18c's normalization, its pages equal publication 3's build byte for byte, and all 859
  files match. v1's demo runs at the fixed link ("Verdict bitwise identical", 46.5 s, Chromium).
- **The report's claims about the product hold.**
- **MLflow** equals the committed export, 105 of 105.
- **The red line holds.**
- **Its recommendations:**
  - the two tooling follow-ups below;
  - the host's preview tags on v1's history page name v6;
  - an unused stale designation sentence in the Space's claims;
  - "runs daily" describes the schedule, while the live record issued 4 of its first 12 days, each other day with
    its cause.

## Disclosures

- **The history link (O44).** The report and the README linked v1's demo as the Space's bare `/history/`.
  - **What it did:** the static host answers that URL with a 302 to `huggingface.co/history`, an unrelated user's
    profile. CP-18c had found and fixed this on the Space, but PRES-5 was reviewed on its own branch and kept the
    old link.
  - **Why the check missed it:** the post-deployment link check followed the redirect and counted the 200.
  - **The fix:** six links, three on the page and three in the README, now name `history/index.html`. They were regenerated from source, and only the link
    targets changed. `tests/test_50` now refuses a bare history route.
  - **Exposure:** about 55 minutes, 22:02–22:56Z on 2026-11-13.
- **The merge conflict between the two rounds (O43).** CP-18c's wall test refused the product's identity strings
  that PRES-5 shows by decision 28. PRES-5's own `test_24` exempts the same strings. The repair applies that
  exemption to CP-18c's test, and only to the four identity strings.
- **The page's bytes** moved from 1,848,925 to 1,848,955 with the link fix, within the 2.0 MB budget.
- **Usage-limit pauses:** twelve, the weekly limit among them. The return lists them, and each reviewer resumed in
  place.
- **Machine-hours:** about 10.6, within the 12 that O39 allowed for the last steps.
- **MLflow writes:** 61 runs created and 44 untouched, with the experiment description written once. The run IDs
  are in the return and in `pres-5-public-mirror.json`.

## The Orchestrator's rulings at the landing (decision 27)

- **O43 and O44:** above.
- **O45: PRES-5's open presentation items** (the return's list):
  1. A8: not yet triggered (O38).
  2. The receipt's Space rows: the Space is verified by CP-18c's normalization. The receipt's normalizer is to take
     CP-18c's rule at the next publication.
  3. v6's colour and hexagon: kept until the Owner chooses (O16).
  4. The live product's public start time: measured and bound at the next publication.
  5. The two `evidence/pres-5` links: they answer 200 after the push (the receipt's link row).
  6. CP-17c's manifest test under a local Python 3.12: out of scope, for CP-17c's tooling.
  7. The three packet rows that give the candidate's 1,848,408 bytes: read them as the candidate's.
  8. One product name across surfaces: the Space shows "v6 · DDNN-2 alone" as the name. Its claims file still
     says "A1" in two sentences. The designation line is unused, and when "A1 was frozen…" shows was not traced.
     Both are a wording fix for the Space's next change.
  9. Review 4's wording recommendations R1–R7: for the next publication.
- **Follow-ups, for the next publication round:**
  - the link checker refuses a redirect to another origin;
  - the receipt's host normalization follows CP-18c's;
  - the Space's two "A1" sentences;
  - R1–R7.
