# PRES-1 landing, publication and closure — 2026-09-29

**CLOSED — LAND; F6–F8 complete.** The Owner explicitly reaffirmed D5 as a PRES-1-only
exception to the current AGENTS.md mainline/publication restrictions. It names candidate
`a0302dd6c5ff6714709b4f3a3b742f71a4b596a7` and evidence tip
`0df6dda203ea31ab35b34e7ad69d2a2e3e871ebf`, already accepted at [receipt/F5](pres-1-receipt-2026-09-29.md).
No F1 repeat, governance edit, guard bypass, new research or later checkpoint was authorized or performed.

## Published artifacts and F6–F7

- [Report](https://hrsi56.github.io/delu-day-ahead-forecast/) and
  [repository/README](https://github.com/hrsi56/delu-day-ahead-forecast).
- [Hugging Face Space](https://huggingface.co/spaces/Yarden-Viktor/delu-day-ahead-forecast)
  ([direct app](https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/)).
- [MLflow research experiment](https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow/#/experiments/1).
  This is the Lead's existing F1 upload; this task only read/verified it.

**F6:** fetched origin and verified unchanged starting main `a8bee0ce5b3d1f25d0b477c88c53c21f50bd163f`.
Receipt/F5/explicit authority and Q&A entry 35 were committed separately as `a067d2f`.
`git merge --squash 0df6dda203ea31ab35b34e7ad69d2a2e3e871ebf` landed **114 approved paths**,
each staged blob checked byte-for-byte against the evidence tip. No merge conflict or content
repair. Squash commit: **`265661da4d8ae2565003c8ab6e8525f9ffec45d3`**,
“Publish the v1–v3 research presentation with registry-driven claims and verified MLflow routes”.

Both preservation tags were created, verified locally and pushed with main:

| Tag | Preserved SHA |
|---|---|
| `land/pres-1` | `265661da4d8ae2565003c8ab6e8525f9ffec45d3` |
| `evidence/pres-1` | `0df6dda203ea31ab35b34e7ad69d2a2e3e871ebf` |

The actual secret/commit-message/pre-push hooks ran; the newly landed pre-push hook also ran
the fail-closed publication guard. `core.hooksPath` stayed unchanged. No `--no-verify`.
The approved generated HTML contains one pre-existing whitespace-only line (line 454), reported
by the staged diff whitespace check. It was preserved to keep the approved bytes; the publication
and secret guards passed. This is not presented as a clean whitespace result.

**F7:** uploaded the already verified exact bundle, without rebuilding or modifying it, using
`HfApi.upload_folder` (the same Hub upload operation as `hf upload`). Authenticated account
`Yarden-Viktor`; stored HF_TOKEN consumed only inside the process. No token printed, persisted,
changed or login configuration written. The credential-value guard scanned outbound files first.
[Space commit `59d941825755bf73eabb7ff20e31124fee305755`](https://huggingface.co/spaces/Yarden-Viktor/delu-day-ahead-forecast/commit/59d941825755bf73eabb7ff20e31124fee305755).

All **805 files / 44,162,180 bytes** verified against remote blob/LFS hashes at that revision;
bundle SHA256 **`b046c69b899bb9d5a2b2f9aeb3e5b3eebfdda820a419137ef5cdf8b8ac8f7c3d`**.
The existing unused Hub `style.css` remains, as documented in deploy.md; it is outside the
approved bundle and was not deleted. Hosting inserts its public `window.huggingface` metadata
script in served HTML; removing only that insertion yields the exact approved index hash.

## F8 results

[Aggregate result: PASS](../../reports/presentation/release-checks/2026-09-29-postdeploy-summary.json).
Initial failures are retained, not replaced by successful retries.

| Check | Actual result / evidence |
|---|---|
| Pages | Public bytes equal approved `docs/index.html`, 1,560,646 bytes; SHA256 `d1227c0f64c6a478f6f076e713e2bed2755edf51d0b8f19522c9b978d42fab3d`; [record](../../reports/presentation/release-checks/2026-09-29-postdeploy-pages-identity.json) |
| Space identity | All uploaded file hashes match; served index matches after documented host injection; [deployment](../../reports/presentation/release-checks/2026-09-29-space-deployment.json), [served identity](../../reports/presentation/release-checks/2026-09-29-postdeploy-space-identity.json) |
| Cold starts and controls | Chrome/WebKit at desktop/phone all have successful fresh anonymous runs, 20.3–21.0 s, both controls change the view, no failed request/console error in successful runs; [initial four runs](../../reports/presentation/release-checks/2026-09-29-postdeploy-demo.json), [targeted Chrome desktop retry](../../reports/presentation/release-checks/2026-09-29-postdeploy-demo-chrome-retry.json) |
| MLflow mirror | 23/23 runs, 6,928 metric points; complete histories/params/tags/parents/artifacts verified, no problem; [record](../../reports/presentation/release-checks/2026-09-29-postdeploy-mlflow-mirror.json) |
| Anonymous reader routes | Six intended routes in both engines; one transient WebKit overview failure resolved by a fresh targeted retry; [initial routes](../../reports/presentation/release-checks/2026-09-29-postdeploy-mlflow-routes.json), [retry](../../reports/presentation/release-checks/2026-09-29-postdeploy-mlflow-route-retry.json) |
| Settled comparison charts | Five routes × two engines = ten successful checks; actual Plotly charts, no skeletons, missing expected identity or HTTP errors; [record](../../reports/presentation/release-checks/2026-09-29-postdeploy-mlflow-settled.json) |
| Link gate | All required destinations pass; gated repository UI routes remain expected login redirects and are not advertised as anonymous tracking; [record](../../reports/presentation/release-checks/2026-09-29-postdeploy-links.json) |
| Public CI | Main landing [invariant-tests](https://github.com/hrsi56/delu-day-ahead-forecast/actions/runs/36489076520), landing tag [checks](https://github.com/hrsi56/delu-day-ahead-forecast/actions/runs/36489076555), evidence tag [checks](https://github.com/hrsi56/delu-day-ahead-forecast/actions/runs/36489078650), and [Pages deployment](https://github.com/hrsi56/delu-day-ahead-forecast/actions/runs/36489075497): success |

**Observed availability limitation:** first Chrome desktop load received Hugging Face 429s;
initial WebKit overview route received one DagsHub artifact-list 429. Both failed observations
remain in their original records. Targeted fresh retries succeeded without code, asset,
credential or threshold changes. This proves successful post-deploy operation, not uninterrupted
availability. Real Safari, real iPhone and a screen reader were not used. Historical effort,
added-disk baseline and cold-reader limits in the Lead return remain unchanged.

## Disposition, references and retained material

After F8 passed, verified local/remote tags and that every cited review candidate is an ancestor
of `evidence/pres-1`. The deployment directory was copied to
`.local/artifacts/pres1-publication-20260929/space-wasm/`; source/destination file hashes matched
before removal. Lead status was clean at the exact evidence tip.

Removed the checkpoint worktree and deleted `gauntlet/pres-1`. The first `git worktree remove`
deregistered and removed its contents but left a Finder-created `.DS_Store`; that sole remaining
file was backed up and the directory removed. Only main and the primary checkout remain.
Disposable environment/compiled/runtime caches were reclaimed; no source/evidence was lost.

Live receipt links now use committed `docs/track-b/evidence/pres-1/` paths. The original briefs
and immutable verdict/return documents remain byte-identical historical instructions; their old
branch/checkout references resolve through **`evidence/pres-1:<original repository path>`**.
They are not active routing instructions. Deployment bundle references resolve to the retained
copy above. No new authority, threshold, model promotion or CP-21 opening follows closure.

Retained recovery: `.local/tmp/pres-1/`, `.local/artifacts/presentation/`, the prior receipt
folder, and `.local/artifacts/pres1-publication-20260929/` (exact bundle, manifests, screenshots,
logs, tag/reclamation records and full diff). Shared `.local/cache/uv` and `.local/tools/` remain.
These are local recovery; required results are committed in the paths linked above.
W16/template edits remain a separate task requiring its own applicable authority; none performed.
