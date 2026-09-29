# PRES-2 closure — 2026-09-29

**Closed by the Owner's decision, after his own manual check of the public site and Space.** The
Owner said: "בדקתי ידנית בעצמי. אפשר לסגור הכל" ("I checked it manually myself; everything can be
closed"), and then: "בצע בעצמך מה שצריך" ("do what is needed yourself"). This record is the
closure. It is not an independent postdeploy verdict, and it claims none.

## Identities

- **Rules:** PUBLISH_RULES 1.0, SHA-256
  `03f106060d9a646ce0c0c986d2f5fb6549929f2ed7270f0c8678fbfd2293b3a3`, preserved at
  `evidence/pres-2:docs/PUBLISH_RULES.md`. PRES-2 keeps this contract; 1.1 governs later
  publications.
- **Reviewed candidate:** `d7d57e316a0afa198a2196bf4a2f1a3ac4a7c987`. Its Integration PASS covers
  the local-ready milestone:
  - [the verdict](evidence/pres-2/integration.md);
  - [the acceptance matrix](evidence/pres-2/acceptance.md).
- **Evidence tip:** `871c0e27a3cba9f1b2d937a2482e5dfda7bbf9c7`, tagged `evidence/pres-2`.
- **Landing:** `a5436162cd7a0c6bc1fdee3c60534928add756c7`, tagged `land/pres-2`. Both tags are on
  `origin`.
- **Pages:** the served page's SHA-256 is `f36314e28811ed4b7ec41bc73dfd481ddb112815effabfc4e7b3ae74d8edab1d`,
  equal to `docs/index.html` at `land/pres-2`.
- **Space:**
  - revision `0c550e863711e19abbb35219cf64d45dfb39c888`;
  - bundle `8007f0d2a9c09a8c2c3182745dac6b38956a9a0ad8f58541f32472b674d5bb4e`, 805 files, 44,164,910
    bytes;
  - see the [deployment receipt](pres-2-space-deployment-2026-09-29.md), committed at `5a6b585`.
- **MLflow:** the 23-run export is unchanged. Nothing was uploaded.

## Acceptance, as it actually happened

| Item | Disposition |
|---|---|
| Local acceptance | Integration PASS on `d7d57e3`, with the acceptance matrix |
| Public identity | Pages byte identity. On the Space: all 805 file identities, the public card, and the HTML after removing only the host-injected script. All from the deployment receipt. |
| Targeted public behaviour | Four public demo configurations succeeded: Chrome and WebKit, each at 1,440 × 900 and 390 × 844. The first Chrome desktop run hit sixteen HTTP 429 errors; it is kept on record with its successful retry. |
| The rest of the P8 matrix: the report, charts, accessibility, failure states, and the postdeploy MLflow, route and link matrix | Covered by **the Owner's manual public check**, 2026-09-29. It is recorded as his check, not as automated evidence, and no machine-readable record exists for it. |
| A new independent postdeploy review | **Waived by the Owner, for PRES-2 only.** This is a one-time exception: it is not a PASS, and the standing rule is unchanged. Every later publication needs its independent check (plan revision 3 §16, decision 3; PUBLISH_RULES §10). |
| F01–F04 of the [2026-09-29 independent postdeploy review](publication-postdeploy-independent-review-2026-09-29.md) | Fixed in PRES-2 and accepted locally. **Closed publicly** on the Owner's manual check, after the Space deployment. |
| `style.css` on the Space | A leftover from before PRES-1, which neither upload deleted. The served app and the reviewed bundle do not reference it: a search of the bundle finds only `.style.cssText`. The Space holds 806 files: the 805 reviewed plus this one. **Accepted by the Owner and not deleted now.** The next Space deployment removes every remote file that is not in its reviewed bundle. |
| Real Safari, a physical phone, a screen reader | Not used, as in every PRES record |

## Reclamation (templates §4)

- **Disposition:** LAND, as `a543616`, tagged `land/pres-2`.
- **Verified before deleting anything:**
  - all 12 of the branch's commits outside `main`, including `d7d57e3` and `871c0e2`, are reachable
    from `evidence/pres-2`;
  - both tags are on `origin`;
  - no `gauntlet/*` branch exists on `origin`.
- **Reclaimed:**
  - deleted the local branch `gauntlet/pres-2`, which was at `871c0e2`;
  - removed the worktree `.local/worktrees/pres-2`. It was clean and held only ignored caches,
    about 1.1 GB: `.venv`, `__pycache__`, `app/public` and `dist`;
  - removed the empty leftover folder `.local/worktrees/pres-1`, which held only a Finder
    `.DS_Store`. No branch or worktree remains except `main`.
- **Repointed:**
  - `progress.md`;
  - the deployment receipt, whose "Remaining scope" now points here.

  Frozen records, meaning the PRES-2 brief and the evidence files, keep their wording. The branch
  name there refers to the history the tags preserve.
- **Retained recovery material:** `.local/artifacts/pres-2/`, about 355 MB, including the deployed
  bundle `space-wasm-8007f0d2/` and the postdeploy snapshots.

## Unrelated housekeeping, on the Owner's instruction

Dropped one stale stash:

- its SHA was `fe6374b021f71ac68d13551bc534301092f6d631`;
- GitHub Desktop created it on 2026-08-06, on `claude/modest-bardeen-96zee0`, a branch that no
  longer exists;
- it held only an empty macOS `Icon\r` file;
- its base, `658c901`, is in `main`.

No stash remains.

## Carried forward

- **PRES-2's advisories R1–R7,** in the Integration verdict and the
  [advisory log](publication-advisory-log.md), stay as recommendations for the next publication.
- **The next publication:**
  - pins PUBLISH_RULES 1.1;
  - accounts for every surface: Pages, the Space, MLflow and the README (runbook §1a, packet §8);
  - deletes stale files from the Space when it deploys.
