# PRES-2 — Hugging Face deployment receipt, 2026-09-29

**Deployment completed; targeted public demo checks passed after one retained retry.**
This is a publisher's deployment receipt, not a new independent postdeploy verdict or closure
of the full PRES-2/P8 matrix. The product remains released v1; this publishes PRES-2's reviewed
presentation/accessibility changes, not research v3 or a new daily-training system.

## Authority and starting state

The Owner explicitly asked to upload PRES-2 to the Space, authorized doing so, and reported
having committed/pushed main. Verified clean main and remote main at
`81ab3be430a73c0938a579e117c51e99ec96f72f` before deployment. Deployment/hash/secret-guard/browser
helper source was unchanged from `evidence/pres-2`. No repository code, policy, branch or Git
history was changed; no local commit/push or MLflow upload was performed.

PRES-2 retains its original PUBLISH_RULES 1.0 acceptance contract. Independent candidate PASS
binds `d7d57e316a0afa198a2196bf4a2f1a3ac4a7c987`, evidence tip
`871c0e27a3cba9f1b2d937a2482e5dfda7bbf9c7`. The exact preserved bundle was deployed, without
rebuilding or rerunning local product tests.

## Deployment and identities

- Previous Space revision: `59d941825755bf73eabb7ff20e31124fee305755` (PRES-1).
- New revision: [`0c550e863711e19abbb35219cf64d45dfb39c888`](https://huggingface.co/spaces/Yarden-Viktor/delu-day-ahead-forecast/commit/0c550e863711e19abbb35219cf64d45dfb39c888).
- Upload: 2026-09-29 11:06:09–11:06:23 UTC; public Static Space, RUNNING at the subsequent read.
- Bundle SHA-256: `8007f0d2a9c09a8c2c3182745dac6b38956a9a0ad8f58541f32472b674d5bb4e`;
  805 files / 44,164,910 bytes. Credential-value guard passed. All 805 remote repository file
  identities matched; pre-existing unused `style.css` was retained, not deleted.
- Public card matches raw bytes: `c92a2666d76255b24d8e0fb159f97bedcbee0a7a948fb6afeac4b02089bb9a67`.
- Direct app raw HTML hash: `0122c63cbe668e323afde577782e6b6e056f8d2f476311ef717d9bcae77f50db`.
  The initial raw comparison did not match. Inspection established one 101-byte host-injected
  `window.huggingface` metadata script at byte offset 41; removing only that script yields exact
  reviewed HTML hash `fcb0ed136f063276252c9d2230181a848d94f17ce59ef4cc7945cdd8dcb16a8e`.
  Both raw comparison and precise normalization evidence are retained. Repository-wide file
  verification does not assert that every CDN-served asset was separately fetched and hashed.

## Actual public browser checks

Fresh anonymous browser contexts opened the [direct public app](https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/).
Each successful run displayed the forecast, switched the interval from 80% to 95%, and changed
the scenario slider from 1 to 1.01; both actions changed the view.

| Engine | Viewport | Forecast visible | Result |
|---|---|---|---|
| chrome 154.0.8037.58 | 1440x900 | 19.3 s | both controls changed the view; no console/request errors or overflow |
| chrome 154.0.8037.58 | 390x844 | 19.2 s | both controls changed the view; no console/request errors or overflow |
| webkit 26.6 | 1440x900 | 21.4 s | both controls changed the view; no console/request errors or overflow |
| webkit 26.6 | 390x844 | 20.8 s | both controls changed the view; no console/request errors or overflow |

**First failure retained:** Chrome 1440×900 initially received sixteen HTTP 429 asset errors
from the public Space host, then displayed the failure/retry/report fallback; readiness timed
out at 181.2 seconds. A fresh targeted retry of that same configuration succeeded. The three
other first-run configurations succeeded. This is an observed service rate-limit interruption,
not merely a local test-environment restriction. The later success does not erase the failure
or guarantee continuous availability. Timings are observations, not a new performance benchmark.

## Evidence

- [Upload and remote file verification](../../reports/presentation/release-checks/pres-2-space-deployment.json).
- [First raw public identity comparison](../../reports/presentation/release-checks/pres-2-space-public-identity.json).
- [Normalized public identity](../../reports/presentation/release-checks/pres-2-space-public-identity-normalized.json).
- [Four initial public browser runs](../../reports/presentation/release-checks/pres-2-public-demo.json).
- [Targeted Chrome desktop retry](../../reports/presentation/release-checks/pres-2-public-demo-chrome-desktop-retry-1.json).
- Local HTML snapshot and incoming progress: `.local/artifacts/pres-2/space-postdeploy/`.

## Remaining scope

The requested upload is complete. The full P8 report/chart/accessibility/failure-injection,
postdeploy MLflow/route/link matrix and new independent review have not been completed by this
receipt. No real Safari, physical phone or screen reader was used; WebKit/phone sizes are
emulated. Do not close all F01–F04 or PRES-2 from these targeted checks. Preserve the Lead
branch/worktree and evidence until the remaining acceptance/disposition work is completed.
The MLflow export is unchanged and was not reuploaded. Deployment records and progress changes
remain uncommitted for Owner review.

**Status update, 2026-09-29 (after this receipt).**

- These records were committed and pushed at `5a6b585`.
- The Owner then closed PRES-2 after his own manual public check. The remaining scope above was
  settled by that decision; see the [closure record](pres-2-closure-2026-09-29.md).
- The Lead branch and its worktree have been reclaimed. The tags preserve the evidence.
