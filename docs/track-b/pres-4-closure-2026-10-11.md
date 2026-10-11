# PRES-4 closure — 2026-10-11

**PRES-4 is closed. v5, "v5 · DDNN-2 added", is published on the report, the README and MLflow,
with CP-22 and CP-23 as branch cards, "tested, not adopted". v1 remains the released product and
the demo, and the Space is unchanged by the Owner's decision.** Every public check passed, two of
them after a first failure caused by a service's rate limit. The independent post-deployment
review was waived by the Owner for PRES-4, and the rule change that would end these waivers goes
into stage 4's suspension.

## Identities

| Item | Value |
|---|---|
| Brief | `docs/track-b/evidence/pres-4/issued-brief.md`, SHA-256 `54169c7c998958e850d451bf5c766dddbd559721f1920370020035e3bae57bdd`, issued 2026-10-11 at `bfadb39`, recorded at `e398a30` |
| Pinned rules | PUBLISH_RULES 1.4 `ccfe6199535dc104250ee1ed1d8ff57bf0b12fbfb4945a3521e2e29fad479a80`; research anchor `capstone_v21.md` v21-r12 `caf03d70…`, read-only |
| Starting `main` | `e398a30bb53ecd4c397aad0f34fd122d42e74553` |
| Independently checked candidate | `460750d02013a40ab3ac7dd92dcec1b1eb190eef` (Integration review 2, PASS) |
| Final candidate (the Integration PASS binds here) | `e7bdb60bfa5c4eecdfcac14f2325d7bb45d104a1` |
| Evidence tip / `evidence/pres-4` | `80ccc183d543ec0b9e91a8a871152a59f898009a` |
| Squash landing / `land/pres-4` | `aebebc193bc95501eaf36bfca87861acfb2697d3`, with the single parent `e398a30`; its tree equals the evidence tip's |
| Page | `docs/index.html`, SHA-256 `54708134fdfeb2ce3f2ee2d04b1f93008b7506917690a74d93548951a18d37ce`, 1,996,267 bytes (3,733 under the 2.0 MB budget) |
| README | SHA-256 `c816972a7ddb4509f4e7617f4f480588b2500becb9217d8d36a4afebee8315fc` |
| Space | unchanged: revision `0331088725fedab2f5a1ec804ae03bf960cf126f`, bundle `9028a11869a378ea5c3401a00ad46368e1c9e2f2f9f8732330d32b71af081585`, card `c92a2666…` |
| MLflow runs added | `cp22` `b93f1feafd634fa18b7af44724acb054` (children `A-LN` `32bda8bc…`, `A-LP` `ec67bfec…`, `A-PN-sel` `f7773812…`, `M` `8829c99a…`, `R` `f0c32587…`, `v3+DL` `449ca0aa…`, `v4+DL` `8f25ca7f…`); `cp23` `6bb5b17721a44502a32d7b074d4f5ec3` (`D` `7cf1e2b1…`, `v3+D` `a0244146…`, `v5` `7eed5eec…`); `cp24` `d6b8061fab3e4fa49bb6eb45e5aebdb7` (`D2` `dd360e32…`, `v3+D2` `004be421…`, `v5` `4efaef01…`). Full IDs: `pres-4-postdeploy-mlflow-mirror.json` |

## The return and its receipt

- **The Lead returned BLOCKED at the external gate on 2026-10-11,** about 17 hours after the
  brief: about 7.5 hours of work and 9.5 hours of usage-limit pauses, against a 24-hour timebox.
- **The Integration verdict is PASS,** `docs/track-b/evidence/pres-4/integration.md`, SHA-256
  `7df9f376…fb30`, binding `e7bdb60`.
  - Review 1 failed at `a852c0a` (`integration-review-1.md`, `8afc763e…`):
    - the v5 exact-ratio table printed the rounded point value in its interval columns, because
      an unknown render option fell back to the point estimate;
    - two headline definitions had drifted from the claims that bind them.

    Both were repaired in `1cae93f`; an unknown option is now refused.
  - Review 2 passed `460750d` (`integration-review-2.md`, `23a07bf8…`), after a usage-limit
    interruption.
  - A focused recheck passed `e7bdb60`, whose delta is the MLflow index and the final build.
  - The recheck verdict was re-issued once, to add the template's "Candidate SHA" line; nothing
    else changed (`43f9e2f3…` → `7df9f376…`).
- **The Orchestrator's receipt** (templates §4, and the return checks of `gauntlet.py return`):
  - `e7bdb60..80ccc18` is the two verdict files only;
  - `main` = `origin/main` = `e398a30` after a fetch: nothing was pushed, and the Lead created no
    tag, stash or other branch;
  - the return checks found 0 problems, and the verdict reads PASS at the final candidate in full;
  - the receipt's last command exits 1 by design: it reads the verdict in the primary checkout,
    which is on `main`. The verdict was read at the tip;
  - the packaged brief is byte-identical to the issued one;
  - every §13 area of the return's checklist carries direct evidence.
- **Independent checks before the LAND:**
  - the public MLflow mirror, anonymously against the tip's export, at 18:04 UTC: 44 of 44 runs,
    16,753 metric points, 10 of 10 routes by REST, no mismatch;
  - the Space at `0331088…`, RUNNING, its card `c92a2666…`;
  - the tip's page and README equal the hashes above;
  - no untracked twins; `progress.md`, the one uncommitted file, is untouched by the branch.

## The Owner's steps

1. **The LAND, by hand,** 2026-10-11 at 18:25:30 UTC: the squash, the staged-tree check against
   the evidence tip, `git commit -F .local/artifacts/pres-4/land-commit-message.txt`, and both
   tags.
2. **Before the push:** the value-based secret scan printed `SECRET-SCAN-CLEAN`; the publication
   guard passed.
3. **The push** of `main`, `land/pres-4` and `evidence/pres-4`, at about 18:27 UTC. CI passed on
   `aebebc1` and `80ccc18`; Pages deployed at 18:28:23 UTC.
4. **No Space upload,** by the Owner's decision.
5. **The independent public review was waived by the Owner,** for PRES-4: the Orchestrator's
   recommendation, chosen on 2026-10-11.
   - **The basis.** As for PRES-3: the served page, README and Space files are byte-identical to
     the reviewed final candidate, and MLflow equals the committed export. The content had an
     editorial review, a fresh reader, two independent Integration reviews and a focused recheck.
     The public behaviour was tested on the live services.
   - **What is given up.** No independent reader checked the live surfaces for hosting-only
     effects.
   - **It is the third consecutive waiver.** With it the Owner chose the rule change: require the
     independent post-deployment review only when the served bytes differ from the independently
     reviewed bytes or a public check fails without a passing retry. It goes into the Lockdown
     suspension stage 4 already needs ([programme plan](programme-plan-2026-10-11.md), stage 4).

## The public checks

The Orchestrator ran them, read-only and anonymous, 2026-10-11 18:28–18:55 UTC. Raw logs are in
`.local/artifacts/pres-4/`.

| Surface | Intended identity | Observed public identity and UTC time | Verification record and result | Outstanding |
|---|---|---|---|---|
| GitHub source / README | `aebebc1`; README `c816972a…` | `origin/main` = `aebebc1` at 18:28:55; the raw README equals `c816972a…` | `pres-4-publication-receipt.json` (`681fefb3…`): PASS | none |
| GitHub Pages | page `54708134…`, 1,996,267 bytes | `54708134…` from 18:28:44, again at 18:28:55 | the receipt: PASS. `pres-4-public-report.json` (`3cdc7b08…`): passed, 40 routes in Chrome and WebKit at both widths | none |
| Public MLflow | 44 runs equal to the export, `cp22`, `cp23` and `cp24` added; 10 routes | 44 of 44 runs and 16,753 metric points at 18:28:58 | `pres-4-postdeploy-mlflow-mirror.json` (`48398a17…`): passed. `pres-4-public-mlflow-routes-postdeploy.json` (`88d912af…`): a **first failure**, the 12-run overview comparison, on DagsHub HTTP 429s with every expected text present; the other 9 routes passed in both engines. `pres-4-public-mlflow-routes-postdeploy-retry-1.json` (`55ed6e63…`): all 10 routes passed in Chromium and WebKit at 18:55 | none |
| Hugging Face Space card | `c92a2666…`, unchanged | `c92a2666…`; the Space static, public, RUNNING, at `0331088…` | anonymous API and raw fetch; the receipt's Space-files row: PASS | none |
| Hugging Face direct demo | bundle `9028a118…`, running v1 | every served file equals the bundle; the served page equals the bundle's `index.html` (`fcb0ed13…`) once Hugging Face's injected script is removed, at 18:28:56–57 | the receipt: PASS. `pres-4-public-demo.json` (`ff056360…`): a **first failure**, both Chrome runs timed out at 181 s on HTTP 429s and showed the failure page with its retry; both WebKit runs were ready in 20.5–21.6 s. `pres-4-public-demo-retry-1.json` (`41a5c50f…`): Chrome ready in 18.8–19.4 s with no error. `pres-4-public-demo-a11y.json` (`f9bfcdcd…`): passed. `pres-4-public-states.json` (`69124719…`): the failure, hang and asset-failure states and the retry behaved as specified in both engines | none; the cold-visit 429 is a known service limitation |

- **Links:** `pres-4-postdeploy-links.json` (`2ba84fe9…`) records no failed destination. The 302s
  to DagsHub's login are the gated-path controls.
- **The two 429s** are service-availability observations, not product defects. Neither proves
  uninterrupted availability, and the retries do not erase them.
- **A lesson for the next publication.** The first demo run started while the receipt's link and
  mirror checks were still running, so part of the load that drew the 429s was ours. Run the
  browser records after the receipt, not beside it.
- **Completion disposition:** complete on every surface, with one Owner waiver: the independent
  post-deployment review.

## Reclamation (templates §4)

- **Before deletion:** both tags were verified on origin, and `evidence/pres-4` contains the tip.
  The Lead's raw prerelease logs were copied to `.local/artifacts/pres-4/prerelease-raw/`.
- **`gauntlet.py reclaim pres-4 --disposition land`:**
  - a verified Git bundle of `e398a30..gauntlet/pres-4` and a ref snapshot in
    `.local/artifacts/pres-4-reclaim-20261011/`;
  - the worktree `.local/worktrees/pres-4/lead` removed, clean. Its ignored content was
    regenerable: `.venv`, the Python 3.12 check environment (848 MB), `app/public` and `dist`;
  - the branch `gauntlet/pres-4` deleted (it was `80ccc18`); the worktree records pruned.
- **Already removed by the Lead:** the three Critic worktrees, through `critic-close`. The branch
  was never pushed.
- **Live citations.** `gauntlet.py citations` listed one live citation, in `progress.md`, which is
  repointed in the same operation. The brief, the packet, the verdicts and the reviews are
  hash-bound records of the run and keep their bytes.

| Historical reference | Current retrieval |
|---|---|
| `gauntlet/pres-4`, the reviewed chain | `evidence/pres-4` |
| Any branch commit | Unchanged SHA, reachable through `evidence/pres-4` |
| The squashed publication | `land/pres-4` |
| `.local/worktrees/pres-4/lead/<path>` | The same path in the primary checkout; exact bytes through `git show evidence/pres-4:<path>` |

## Retained local material

`.local/` is ignored by Git and is not an off-device backup.

| Path | Content |
|---|---|
| `.local/artifacts/pres-4/` | The issued brief and its envelope, the Critic assignments and their worktree records, the drafts, the fresh-reader material, release and prerelease attempts, the final checks, the raw prerelease logs, the public-check logs and screenshots, and the LAND message |
| `.local/artifacts/pres-4-reclaim-20261011/` | The branch bundle and the ref snapshot |

## Carried forward

- **For the Owner (none blocks closure):**
  - **A-PRES4-5, the page budget:** 3,733 bytes are left. Compaction, or a budget change, must be
    decided before the next generation's publication;
  - A-PRES4-1, -2, -3 and -7: wording and naming proposals for a later publication;
  - A-PRES3-7: the GFS attribution wording, at the final product's Space deployment;
  - A-PRES3-5: the standard §15 note, in a suspension.
- **For the Orchestrator:** A-PRES4-4 (draft registries checked against §5 inside their own
  checkpoint), A-PRES4-6 (refresh the runbook's §2) and A-PRES4-8 (the export check's blind spot
  for descriptions). Plus two observations both Critics recorded: CP-22's reason merges the draft's
  two clauses, and the `--diff-against` summary omits the experiment-tag change.
- **Governance:** the conditional public-review rule, chosen by the Owner on 2026-10-11, in stage
  4's suspension.
- **Q&A:** three of the Lead's six named triggers are filed: the timing of CP-24's adoption rule,
  the silent fallback that Integration review 1 caught, and how a new generation is published
  without changing a published number.

Record-level scientific claims are taken as the return and the binding verdict report them. No
experiment, fit or test was rerun for this closure.
