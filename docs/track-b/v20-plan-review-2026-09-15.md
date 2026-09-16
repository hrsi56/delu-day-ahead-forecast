> Historical review, superseded by v21. The unadopted v20-r1 draft is retained in
> `/Users/djourno/Downloads/PJM-consolidation-backup-2026-09-16/review/capstone_v20.md`.
> Its temporary branch/worktree was retired during owner-authorized consolidation.
> The original review below is retained as history.

# v20 plan correction review — 2026-09-15

## Authority, scope and isolation

The owner authorized the requested ACI-convention and frozen-registry-loading corrections,
including necessary consistency work, after an explicit request to suspend the Governance
Lockdown for that task. The owner also expressly required that the running Engineer's work not
be overwritten or interrupted. This authorization ends at this task's terminal return; it is
not a standing governance waiver.

The Orchestrator created `codex/v20-plan-corrections` at
`3618658ec16d57795a69c68ccb4cbdab926d73a5` in the separate worktree
`/Users/djourno/Downloads/PJM-orchestrator-v20-review`. Only that worktree is edited in this task.
The existing Orchestrator receipt in the primary checkout's `progress.md` was copied here;
the primary copy was not changed. No engineering artifact, active brief, original-checkout
anchor, tag, candidate commit or verdict was edited, and no executor was contacted or started.

The original `capstone_v20.md` SHA-256 is
`0902a70151cf2a36ef609c35effe49cce725a63eb8ba78478c43421c0507bda4`.
The corrected file identifies itself as **v20-r1**. It is a reviewable local revision awaiting
owner adoption, not a replacement quietly installed into the active CP-10 attempt.

## Corrections made

| ID | Original defect | Correction and controlling locations |
|---|---|---|
| R1 | §4.3 uses a coverage-event indicator without defining whether alpha is coverage or miscoverage. Under the cited paper's miscoverage convention the update direction is wrong. | Define nominal and adaptive miscoverage, use the miss indicator, name the `1 − α_t` quantile and require hit/miss direction fixtures. Explain equivalent coverage parameterization explicitly. Preserve the two-day feedback lag and frozen method/grid discipline. §4.3. |
| R2 | CP-11 registers artifacts, but CP-14's bar permits evaluating a local file without verifying it is the registered frozen artifact. | Record server identity without credentials, run ID, registered model name, numeric version, freeze timestamp and the complete inference-artifact fingerprint in the committed and tracking freeze records. CP-14 resolves those versions, compares identity and fingerprints, and evaluates the verified bytes. Missing records, mismatches and local fallback are covered by refusal controls before real holdout access. §§2.1, 5.1, 8 and 9. |
| R3 | §2.1 tells the daily job to load `@champion`; §§6.1 and 8 route the demo through `daily-demo`. | Align the daily URI with `@daily-demo`; frozen evaluation uses explicit versions and no moving alias. §2.1. |
| R4 | §9's prose says CP-12, CP-13 and CP-14 are mutually independent, while its table makes CP-13 depend on CP-12. §0 also places all MLflow work before calibration. | Preserve the table's dependency graph: CP-11 → CP-12 → CP-13, and CP-11 + 90 days → CP-14 independently. Describe MLflow work at its actual consuming checkpoints. §§0 and 9. |
| R5 | References to the “§5.2 boundary” point at an artifact-comparison section in v20; they actually mean the availability invariant re-ratified from v1. | Name v1 §5.2 at its re-ratification in §3; direct forward availability references to §3. This changes citations, not information cutoffs. §§3, 4.3, 6.1 and 6.4. |

### Sources and reasoning

- [Gibbs & Candès (2021), §2, equation (2)](https://arxiv.org/html/2106.00170v3#S2.E2),
  retrieved during this review: alpha is miscoverage; the update subtracts the miss indicator.
  A miss lowers alpha and raises the conformity quantile. Using coverage instead is an equivalent
  parameterization only if both the update and quantile argument are transformed consistently.
- [MLflow registry workflows](https://mlflow.org/docs/latest/ml/model-registry/workflow/#fetching-an-mlflow-model-from-the-model-registry),
  retrieved during this review: numeric versions can be loaded explicitly; aliases can be
  reassigned. This supports explicit version identity for the frozen evaluation. It does not
  establish that this repository's remote server has been tested; no remote credential was used.
- R3–R5 follow from internal contradictions in the supplied plan, without a claim about the
  engineering implementation or current hosting-platform capabilities.

Registration already supplies a third-party record of the freeze; the defect was the missing
binding from that record to the evaluation. Nor is registry metadata inherently immutable. The
corrected protocol compares it with the preserved CP-11 record rather than treating a mutable
server entry as its own proof. No new tracking service or registry framework is proposed.

## Remaining audit questions — not silently decided in this correction

The whole plan was read for context and direct consistency. This is **not** a completed independent
audit of every scientific, operational or platform claim. In particular, resolve these before a
CP-11 brief commits the prospective protocol:

1. **Frozen ACI state.** §4.3 describes an adaptive method, while §5.1 says “no re-threshold”.
   The freeze needs to state whether it freezes the update policy and initial state, allowing only
   prescribed lagged updates during one chronological evaluation, or prohibits all such updates.
   Those are different evaluated methods. No new permission to consume holdout feedback is
   introduced by the notation correction.
2. **Rule-5 comparison window.** §4.1 assigns 0.194 to 408 hours of August peak weeks, while
   §4.2 rule 5 says “fold_3 95% coverage”. Comparing full-fold coverage with that peak-only
   baseline would change the question. Confirm the intended same-window comparison in a
   prospective correction; do not silently alter an already-running attempt's acceptance metric.
   The Orchestrator did not read CP-10 results or recompute the historical metric.
3. **CP-11 prerequisites and reporting.** `v2-full` requires §6.1's data features before freeze,
   although the daily-service checkpoint comes later. The freeze brief must place that work
   explicitly. It must also resolve the currently undefined “does not degrade the primary
   endpoint” rule and the “interim status per §7.3” citation before the prospective experiment.
4. **Availability at publication.** §6.1 schedules a job after the day-ahead auction but also
   requires inputs available at the earlier gate. The future service brief needs explicit data
   timestamps and training/calibration/evaluation boundaries; a clock-time label alone does not
   prove prospective forecasting. The planned-outage feed also needs reconciliation with the
   daily path's prohibition on the ENTSO-E token. No platform or feed availability was tested here.

These are open plan questions, not findings against the current Engineer. Keeping them here
prevents the targeted correction from being misrepresented as a clean full-plan audit.

## The author's other handover notes

- The nine repaired repository defects were the previous author's self-review. Ratification and
  independent audit remain different statuses; this correction does not certify all of v20.
- A clarification can reveal an incorrect assumption. Verify the artifact or current primary
  source before asserting that a checkpoint covers a requirement or a platform supports a path.
- The author describes two namespace-test assertions as deliberately vacuous until live claims
  exist, with a synthetic-key positive control. That explanation is preserved, not re-certified.
  `tests/test_24_live_namespace_is_walled_off.py` and its control were not inspected or run here;
  this is a plan correction, not an engineering audit.

## Adoption and the active CP-10 attempt

Let the dispatched attempt reach its terminal packet against its own original committed anchor.
This work does not interrupt it, request a mid-run rebase, change its tests, reinterpret a verdict,
or retrospectively change its bar. A verdict against the original content remains evidence of
that exact content, not evidence of conformance to v20-r1.

After receipt, the Orchestrator checks the packet through the prescribed record checks. Before
claiming conformance to an amended plan, any affected CP-10 work must be handled by a revised
brief and, where the candidate changes, a fresh Integration verdict. The Lead owns that engineering
work. No corrected-plan implementation or result is inferred from the current working files.

Owner review and mainline adoption remain owner-authored. The Orchestrator does not merge, push,
or commit this correction. The separate branch/worktree remains open for that review, with no
tags created and no existing refs deleted.

## Validation

- Exact original CP-10 bar is retained in v20-r1; original v1 figures, protected artifacts and
  the already-dispatched brief are unchanged.
- ACI directions were checked numerically for one synthetic hit and one synthetic miss, including
  the equivalence of coverage and miscoverage parameterizations. This validates the written
  correction only, not an implementation.
- Freeze identity, artifact verification and refusal requirements are traced from §5.1 into the
  CP-11/CP-14 bars; dependency prose matches the table; no forward availability citation points to
  the artifact-comparison §5.2.
- `git diff --check`, plan-diff review and `progress.md` omission review are completed before
  handover. Only `capstone_v20.md`, `progress.md` and this review note belong to this task.

Observed arithmetic control (`alpha=0.05`, `gamma=0.01`): a miss gives alpha `0.0405` and quantile
`0.9595`; a hit gives alpha `0.0505` and quantile `0.9495`. Both match the complemented coverage
parameterization within `1e-14`. The primary-checkout plan still has the original SHA-256 above
and that checkout remains on `gauntlet/cp-10`; no engineering-content inspection was used to
make this verification. The corrected plan SHA-256 is
`9365ee02d2688f4d10fa3b1fd39955128422cd41fefa3773f1f87dfb10c1b23d`.

## Branch and worktree handover

- Branch: `codex/v20-plan-corrections`, owned by this Orchestrator for the isolated correction.
- Worktree: `/Users/djourno/Downloads/PJM-orchestrator-v20-review`.
- Tip: `3618658ec16d57795a69c68ccb4cbdab926d73a5`; zero commits ahead and zero behind `main`
  at the final check. The changes are unstaged: two modified files and this new review note.
- Created tags: none. Created commits: none. Deleted refs/worktrees: none.
- Proposed disposition: leave this branch/worktree open for owner review and adoption after
  CP-10's terminal packet. It is not a `gauntlet/*` branch and is not eligible for automatic
  checkpoint reclamation. No deletion is authorized or performed by this task.
- Proposed commit message: `docs: clarify ACI and bind frozen evaluation to registry identity`.
