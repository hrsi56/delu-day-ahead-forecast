# M3.5/CP-3B item 6 — NOT COMPLETED

**Status: NOT COMPLETED. Closed 2026-09-15 by owner decision, unmet.**

This file exists so the gap is a record rather than an absence. CP-3B landed at `7f16f4e`
(`land/cp-3b`) with five of its six items met.

## The bar, as written

> **6. One fresh Integration Critic `PASS`** on a final candidate SHA, from a clean detached
> worktree, with a verdict-only delta to the evidence tip.

## What actually happened

| Round | Candidate | Verdict |
|---|---|---|
| 1 | — | **FAIL** — recorded at `f55dd75` |
| 2 | `8c39262` | **FAIL** — two untrue sentences and one wrong measurement; all three fixed |
| 3 | `55a70e7` | **INTERRUPTED** — cut off twice by usage limits. Partial notes read `PASS` on items 1–3; recorded at `0adc309` as notes, explicitly **not a verdict** |

No review binds the final candidate `55a70e78da760aa95c32169c72946860bcf28f41`. The Lead returned
`INCOMPLETE` rather than `PASS`, and stopped the loop at the owner's instruction rather than
starting a fifth review.

## What stood in for it

Nothing replaces an independent review, and this section does not claim otherwise. What exists is
the Orchestrator's own verification, run before landing and recorded in the landing commit:

- 185 tests pass from a clean `uv run pytest`.
- **The hard gate re-verified independently, not re-run.** The browser champion was rebuilt the way
  the notebook builds it and compared against the frozen `mlflow.pyfunc` artifact on delivery days
  the Lead's fixture does **not** contain: 8 days with finite output, 1,728 values, max
  |deviation| `0.0`, NaN patterns identical row by row. The Lead's own 54-day fixture covers 1,296
  rows and 11,628 values at the same `0.0`. Four positive controls all break the gate.
- The 238 days on which the browser fails closed were traced rather than assumed: the app has no day
  selector, it forecasts `2026-09-06`, and that day is inside the proved fixture. `series.json` is a
  sparse 302-day payload, so a day without a full 720h window must fail closed rather than fabricate.
- `docs/index.html` re-scanned with an independent matcher: 0 fetching references, 7 `data:` URIs.
- `make verify` PASS, zero disagreements across every surface.
- The app driven in a real browser: Pyodide boots, the boosters execute, the fan chart renders.

## Why this is recorded rather than quietly closed

The checkpoint contract exists because a Lead's own Integration Critic passed CP-1's first attempt
while 95.83% of its rows leaked. An independent review is the control on exactly that failure mode.
Landing without one is a real reduction in assurance, and calling it anything else would be the kind
of overclaim this project's whole method is built to prevent.

## Consequence for the next checkpoint

**This is not a precedent.** M4/CP-4 decides whether a calibration method works — the point at which
an independent verdict is the substance of the checkpoint rather than bookkeeping. Its brief states
that no landing occurs without a fresh Integration Critic verdict binding the final candidate SHA.
