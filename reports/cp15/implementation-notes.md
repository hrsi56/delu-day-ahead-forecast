# CP-15 implementation and numerical repair record

The comparison protocol remains byte-identical to preregistration commit
bb5e67882fcfdf65b963d25ce785a3999816dfc2. No outer evaluation score or ranking
had been produced when the repair below was selected.

## Fixed-tolerance LEAR continuation

Initial warm-up runs stopped on 2020-06-05 and 2021-03-01 with sklearn
ConvergenceWarning. A diagnostic on 2020-06-05 isolated a 56-row, 350-column
inner-training regression: alpha 0.0008207878053009869, 20,000 iterations,
normalized dual gap 8.386406227109797e-05 (unnormalized gap .004696387,
tolerance .003773). The failed fit was not accepted and no complete origin was
cached for that day. Initial fold invocations exited 1; their logs are retained
in the ignored cache/log area with final hashes in execution evidence.

The fix continues the **same** sklearn Lasso optimization from its current
coefficients, at the **same** penalty, training data, tolerance and 20,000
iterations per solver call. At most ten calls are allowed. Every accepted fit
must terminate without ConvergenceWarning; ten exhausted calls fail explicitly.
This changes computational effort, not the finite penalty grid, statistical
objective, chronological validation, target representation or acceptance of
convergence. Per-hour fit records retain total iterations and solver calls for
every grid penalty and final fit. The complete core is rerun under its new
source fingerprint, including earlier successful warm-up origins.

## Execution and resource accounting

Origins execute chronologically within each fold; at most two independent fold
processes run concurrently on CPU. Each LightGBM fit retains its four registered
threads, and BLAS uses one thread. No state or errors cross folds. Fit durations
are measured per model; process peak RSS is shared across that fold's policies
and is labeled as shared, not attributed to a single estimator. Ensembles and
B0/B1 perform no model fits. Cached central forecasts retain their original fit
records; cache hits are counted separately from logical policy fits.

Regression tests, independent artifact checks, and the first uncached
representative reproduction briefly overlapped the fold queues on the same
machine. Timing reflects this shared local workload; it is not an isolated
estimator throughput benchmark. The reported fold peak RSS comes from the
Python worker's `resource.getrusage(RUSAGE_SELF).ru_maxrss` (bytes on macOS).
The separate `/usr/bin/time -l` logs wrap `uv` and must not be mistaken for the
Python worker's memory measurement.
Their `real` wall time does cover the complete invocation. Both that value and
the narrower fold-loop timer are reported: the latter starts after input/feature
construction and warm-up boundary discovery, so it excludes those initial costs.

## LEAR implementation provenance

The model uses separate hourly L1 regressions with cross-hour price lags and
available load forecasts. Method structure was checked against the authors'
[LEAR implementation](https://github.com/jeslago/epftoolbox/blob/master/epftoolbox/models/_lear.py)
on 2026-09-16. The implementation here is original code using scikit-learn;
it does not copy or depend on epftoolbox's AGPL source. Chronological validation
and the representation comparison follow the ratified CP-15 protocol.
