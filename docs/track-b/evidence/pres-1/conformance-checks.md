# PRES-1 conformance: the checks before the independent check (brief §5.4)

**All green at `5d8ce9b64cd8541c65afa4ce6363463e2040582f`** (the code the independent check reviews;
the commit that adds this record changes evidence and records only). Run on 2026-09-28 on this Mac
(arm64, Darwin 25.5.0). Every command ran with credential-like variables removed from its
environment by a wrapper that prints nothing about the environment.

`5d8ce9b` changes one thing after `4dbdfbb`: a build record is now final exactly when nothing is
omitted, so that a plain rebuild reproduces the final build. The page, the README and both Space
cards are byte-identical between the two (`git diff --stat 4dbdfbb 5d8ce9b` names none of them), so
the §10 record, the cold-reader record and the Space bundle measured at `4dbdfbb` describe
`5d8ce9b`'s surfaces too. The suite, the CI-equivalent run, the rebuild and the link check were run
again at `5d8ce9b`.

| Check (brief §5.4) | Where | Result |
|---|---|---|
| Full suite, local Python 3.13.15 | the lead worktree at `5d8ce9b`, clean | `uv run pytest -q`: **927 passed, 7 skipped** in 153.1 s (at `4dbdfbb`: the same, 118.9 s) |
| Clean Python 3.12 CI-equivalent run, every step of `.github/workflows/tests.yml` | a new clean detached worktree at `5d8ce9b` (`.local/worktrees/pres-1/ci-6`, removed afterwards) | every step exit 0 (below) |
| `make verify` | `ci-6` | "PASS — every bound claim agrees on every surface; the static page fetches nothing; the headline, names and statuses agree across surfaces" |
| Determinism: a rebuild, then `git status` | `ci-6` | `uv run python scripts/rebuild_presentation.py`, then `git status --porcelain` empty |
| `check_links.py` | the lead at `5d8ce9b` | "failed destinations: none" (`reports/cp3/link_check.json`) |
| The standard's §10 release checks | the lead at `4dbdfbb`; the page is byte-identical at `5d8ce9b` | **passed** (`reports/presentation/release-checks/2026-09-28-standard-s10.json`; below) |
| The standard's §11 cold-reader check | two fresh readers | **PASS** (`cold-reader-check.md`) |

## The Python 3.12 CI-equivalent run

- **Interpreter:** CPython 3.12.14, uv's managed build under `.local/tools/python`; `UV_PYTHON=3.12`
  for every step, as `astral-sh/setup-uv` sets it with `python-version: "3.12"`; `UV_OFFLINE=1`, so
  nothing was downloaded.
- `git status --porcelain` was empty before, after the CI steps and after the rebuild.
  `pyproject.toml` (`aa35326a…`) and `uv.lock` (`5d2aecc3…`) are byte-identical to `main` at
  `a8bee0c`.

| Step | Exit | Observed |
|---|---|---|
| `uv sync --locked --dev` | 0 | the lock resolved as committed |
| `uv run python --version` | 0 | Python 3.12.14 |
| `uv run python scripts/build_wasm_payload.py` | 0 | payload built |
| `uv run pytest -q` | 0 | 927 passed, 7 skipped in 125.4 s |
| `uv run pytest tests/test_10_cqr_order_statistic.py -q` | 0 | 8 passed |
| `uv run python scripts/verify_release.py` | 0 | PASS, including the cross-surface parity section |
| `uv run pytest tests/test_22_wasm_equivalence.py -q` | 0 | 15 passed |
| `python3 scripts/publication_guard.py tree` (runs only on `main`) | 1 | **Blocked, as designed:** this tree carries a non-final build record and omits the six MLflow links until the verified index exists. It passes only after the final build (F4) |

Also in `ci-6`: `make lint-publication` exit 0 (page, README and template sources: no finding) and
`uv run python scripts/mlflow_export.py --check` exit 0 ("the committed export is current").
Earlier runs of the same steps, at `7403f94` (`ci-3`), `c6dda1f` (`ci-4`) and `4dbdfbb` (`ci-5`), were
green too; each worktree was removed.

The publisher's dry run at the candidate (`uv run python scripts/mlflow_publish.py --dry-run`, no
network): "23 runs, 6928 metric points, 55 artifacts; outbound scan clean; export current".

## The Space bundle

`make wasm` in the project environment (Python 3.13.15) at `4dbdfbb` (whose Space inputs `5d8ce9b`
leaves unchanged) reproduces the committed
record exactly: `reports/cp3b/space_wasm_bundle.json` unchanged, **bundle SHA-256
`eb122883896d755fd3314b6b5d361c1f6d23e0251412edfeeeef5c6201b8aacb`**, 805 files,
44,162,066 bytes, 315 references checked, none missing. The hash is recomputable from the built
folder:

```bash
cd dist/space-wasm && find . -type f | sed 's|^\./||' | LC_ALL=C sort | while read f; do shasum -a 256 "$f"; done | shasum -a 256
```

A build under Python 3.12 gives `302b655f…`: only the nine boosters differ, in one gzip header byte
(the OS field: Python 3.13's `gzip` writes 255, Python 3.12 inherits zlib's 19 on macOS). Their
decompressed bytes are identical, and every other file is byte-identical. The Space card changes at
the final build (F4), which adds the MLflow link, so the bundle hash for the redeploy is the one
recorded after F4.

The demo's cold start on this bundle, served locally (brief W12,
`reports/presentation/release-checks/2026-09-28-demo-w12.json`):

| Engine | Viewport | Ready | Seconds to a visible forecast | Failed requests | Console errors |
|---|---|---|---|---|---|
| Chrome 153 | 1,440 × 900 | yes | 10.2 | 0 | 0 |
| Chrome 153 | 390 × 844 | yes | 10.1 | 0 | 0 |
| WebKit 26.6 | 1,440 × 900 | yes | 11.7 | 0 | 0 |
| WebKit 26.6 | 390 × 844 | yes | 10.2 | 0 | 0 |

## The §10 release checks

`scripts/check_reader_paths.py release docs/index.html` in Google Chrome 153 (through Playwright's
`channel="chrome"`) and Playwright's WebKit 26.6, every disclosure closed unless stated.

**The §1 placements (brief W4), and chart rendering at every width:**

| Engine | View | Headline block ends | Finding sentence ends | Chart text, smallest (closed / open) | Overflow | Failed requests |
|---|---|---|---|---|---|---|
| Chrome | 1,440 × 900 | 774.6 px (< 900) | 1,765.6 px (≤ 1,800) | 12.38 / 12.38 px | none | 0 |
| Chrome | 768 × 1,024 | 624.5 | 2,415.3 | 19.32 / 19.32 | none | 0 |
| Chrome | 390 × 844 | 604.6 px (< 844) | 2,488.5 px (≤ 2,532) | 14.58 / 14.58 | none | 0 |
| Chrome | 360 × 780 | 629.6 | 2,638.9 | 13.26 / 13.26 | none | 0 |
| Chrome | 320 × 640 | 653.6 | 2,756.6 | 12.21 / 12.21 | none | 0 |
| WebKit | 1,440 × 900 | 775.3 px (< 900) | 1,767.0 px (≤ 1,800) | 12.38 / 12.38 | none | 0 |
| WebKit | 768 × 1,024 | 599.0 | 2,391.2 | 19.32 / 19.32 | none | 0 |
| WebKit | 390 × 844 | 604.7 px (< 844) | 2,490.1 px (≤ 2,532) | 14.58 / 14.58 | none | 0 |
| WebKit | 360 × 780 | 629.7 | 2,640.5 | 13.26 / 13.26 | none | 0 |
| WebKit | 320 × 640 | 653.7 | 2,756.6 | 12.21 / 12.21 | none | 0 |
| WebKit | emulated iPhone 15 | 604.7 | 2,491.7 | 14.71 / 14.71 | none | 0 |

At every view the terms sit directly below the headline block, the finding sentence sits above the
comparison's chart, the release rule sits beside the demo action outside any disclosure, and the
byline links to the contribution statement. The numeric placements bind at 1,440 × 900 and
390 × 844; the other widths are recorded.

**The accessibility trees, in each engine's own tree** (1,440 × 900 and 390 × 844):

| Rule (§10) | Chrome | WebKit |
|---|---|---|
| Disclosures expose an expanded state | each visible summary is a DisclosureTriangle with `expanded: false` (18 of 18 closed), then `true` once opened with Enter (24 of 24) | each visible disclosure exposes `expanded: false` (18 of 18), then `true` (24 of 24); WebKit states it on the `details` element, its summary carrying the name |
| Charts are named | 4 visible charts closed, 11 open, each an `image` with a name | the same |
| No control is unnamed | 57 visible controls closed (54 on the phone), 120 open (117), each named | the same |

**How each tree was read.** Chrome: its own accessibility tree, per node, through the DevTools
protocol (`Accessibility.getPartialAXTree`). WebKit: WebKit's own accessibility properties, per node,
through WebKit's inspector protocol (`DOM.getAccessibilityPropertiesForNode`, the data Web
Inspector's accessibility panel shows). Playwright 1.63's public API exposes no accessibility tree,
so the WebKit read runs in the Playwright driver's Node, in process, and reaches the page's inspector
session through playwright-core's in-process connection, a private API: if an upgrade removes it,
the check fails; it cannot pass silently. This closes the WebKit gap with WebKit's own evidence
rather than an ARIA snapshot computed by Playwright. Visibility uses `checkVisibility()`, because a
closed disclosure's content stays laid out under `content-visibility: hidden` in both engines.

**Keyboard, touch, contrast and zoom** (both engines): 57 focus stops in document order, each with
visible focus (WebKit moves with Option+Tab, as Safari does); a summary toggles on Enter; an anchor
into a closed disclosure opens it; 95 touch targets at 390 px, none under 44 px; text contrast
(2,374 elements at 1,440, 2,368 at 390) and non-text contrast (550 and 528 chart shapes), none below
threshold; no overflow at 200% zoom or at 320 px reflow, closed or open.

**Not used:** no real Safari, no real iPhone and no screen reader (standard §10). The phone widths
are emulated viewports, and the iPhone is Playwright's emulated device in WebKit.

**What the check caught.** Its first run found the opening's preview chart drawn with text of
10.8 px on desktop and 11.9 px at 320 px: the W4 layout had narrowed the opening's right-hand column.
The baseline's column ratio and small-phone padding were restored at `7403f94`, and the placements
still hold.
