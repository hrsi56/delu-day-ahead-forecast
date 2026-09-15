# CP-15 — prehistory preflight

**Engineering: BLOCKED · product_feasibility: NOT_DEMONSTRATED**

Best observed policy: **none (comparison not run)**. Qualified policy: **none**.
No CP-15 MAE, WIS, coverage, crisis-behaviour or ranking result exists. All six
product criteria are **unassessed**, not measured failures. The preflight does
not establish that adaptive forecasting fails or succeeds.

## Exact obstacle

The named v21 §5 requires precisely 728 preceding calendar days for B2, B3, A1
and A2; A3/A5 depend on those policies. The preserved snapshot starts on
2019-01-01. Fold 1 starts on 2020-07-01. Its first 728-day training interval is
2018-07-04 through 2020-06-30: **181 leading calendar days / 4,345 canonical
hours are absent**. Every one of its 90 evaluation origins lacks leading archive
support. No preceding-window boundary was moved to 2019-01-01.

At an evaluation origin D, 28 complete released error days can end no later than
D-2. Even assuming no missing days, the first warm-up issuance is therefore
D-29, or 2020-06-02. That issuance requires training history from 2018-06-05:
**210 calendar days / 5,041 canonical hours precede the archive**. This is an
optimistic bound, not a completed warm-up schedule; inherited incomplete days
may require earlier issuance. The inherited 720-hour predictor window also
requires source history before the first training origin. No synthetic or
in-sample residuals were substituted for these missing forecasts.

The 84-day policy and folds 2–5 have leading archive support. This is a support
test only, not proof of adequate model sample size, complete predictors or
successful rolling fits. `history-windows.csv` records each inspected origin,
exact calendar boundaries, canonical hours, available snapshot rows and
inherited eligible training rows. It distinguishes absent archive support from
ordinary eligibility exclusions. The ordinary exclusions are not declared
illegal or required to be zero.

V21 also delegates declaration of a minimum training-row sufficiency threshold.
No threshold has been frozen, and no scores have been inspected to set one.
Treating the absent first six to seven months as acceptable would need an
explicit resolution of the exact-history requirement; this audit does not
silently reinterpret it as an expanding fit over the available 2019-onward
archive. The governing text is:

> Use precisely 728 or 84 preceding calendar days; filter by inherited admissibility. Predeclare
> minimum training-row sufficiency and require complete evaluation predictions. If adequate
> prehistory is unavailable, report the exact deficiency; do not silently shorten windows or
> drop a fold.

## Original evaluation rows preserved

| Fold | Original eligible hours | Represented days | Inherited excluded hours |
|---|---:|---:|---:|
| 1 | 2160 | 90 | 0 |
| 2 | 2159 | 90 | 1 |
| 3 | 2112 | 88 | 48 |
| 4 | 2160 | 90 | 0 |
| 5 | 2156 | 90 | 3 |

Total: **10,747 hours**. The August 15–31, 2022 slice contains **408 hours**.
Every original saved development date and target was checked against the
inherited base-catalog eligibility mask. This is lineage validation, not a new
forecast comparison. The date-based flags in the inherited catalog were used
only to reproduce eligibility; no new model consumed them.

## Reproduction and controls

The immutable inputs and preflight-only protocol were committed at
`884261d30284877092eadda9bfb6704f0ec1e890` before audit implementation.
This protocol does **not** claim a fully frozen comparison:
the modelling, regularization, scaling, quantile, bootstrap and resource choices
must still be committed before a future comparison can run.

From the isolated checkout:

```sh
uv sync --frozen --offline
uv run --frozen pytest -q tests/cp15
uv run --frozen python scripts/cp15_forecasting.py --preflight --output /tmp/cp15-preflight-reproduction
```

The last command deliberately exits **2** after writing `preflight.json` and
`history-windows.csv` to record the missing archive support. It performs zero
model fits. A successful preflight would still not be checkpoint acceptance.
The audit's snapshot read passes a `delivery_date <= 2026-04-07` predicate and
an explicit four-column projection to the Parquet reader before materializing
inputs. Whole-file hashes establish immutable input identity, without treating
reserved outcomes as model inputs. The six new tests cover missing archive
support with a supplied-history positive control, allowed/refused history
lengths, 23/24/25-hour calendar arithmetic, and reader-boundary refusal with a
positive control. They do not stand in for the unimplemented causal model tests.

Dependency/input/protocol hashes and starting topology are in `protocol.json`
and `starting-state.json`. `validation.json` records commands actually run,
exit codes, runtime and memory. Existing regression controls are rerun separately;
historical frozen-model replay in those controls is not a CP-15 fit, selection
or new holdout evaluation. The ignored browser payload is regenerated from
the committed implementation with its tracked manifest redirected to `/tmp`.

## Unmet deliverables and independent review

No B0–B3/A1–A5 comparison, signed-residual buffer, rolling fit, normalization
fixture, model availability control, WIS/ranking/product screening, bootstrap,
Chronos-2 probe or structural-input feasibility sheet was completed. The data
blocker was discovered first. Probe access/resource limitations are therefore
**not tested**, not alleged. No downloads, credential-dependent requests,
remote logging, registry mutations or publication occurred.

The full checklist remains open. A fresh Critic must evaluate this exact
committed artifact and report its limitations; a verified preflight is not an
Integration PASS for CP-15. The eventual verdict is retained under
`docs/track-b/evidence/cp-15/` after its independent review.

## Smallest owner decision

Resolve the fold-1 prehistory policy before completing the comparison protocol:
authorize an admissible earlier-data input with historical availability and
license evidence, preserving the original snapshot, **or** ratify a specific
missing-history alternative to v21 §5. Earlier load forecasts as well as prices
and predictor lookback would need verification; no acquisition feasibility is
claimed here. If the alternative changes the locked plan, the Owner must
manually and temporarily suspend Governance Lockdown for that exact §5 change
and directly necessary consistency edits. No governance amendment has been
prepared or performed by this checkpoint.

Original CP-10 source, models, data, results, evidence and primary dirty files
remain intact. No work on a later checkpoint was inspected or started.
