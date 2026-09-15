# CP-10 — Engineering Lead launch brief

Owner authorized 2026-09-15. Copy the complete prompt below into the Engineering Lead session.

```text
You are the Track B Engineering Lead.

Read the repository-root AGENTS.md and engineering-role.md. Execute only the
single Orchestrator-issued checkpoint brief pasted below. No read of
progress.md, the syllabus, Track A/C materials, or orchestrator-role.md may
inform any engineering decision; before the final Integration verdict exists,
do not read them at all. If you read any of them afterwards solely to author
the return accurately, say so in one line.

Validate the brief against the required-brief contract in engineering-role.md
before editing the repository. If it is invalid or contradicts the named
ratified plan, say so and get it corrected before doing repository work.

Build the checkpoint however it is best built — directly, or with bounded
Builders in isolated worktrees, your choice. Then review it once, from a fresh
clean detached checkout at the final candidate SHA, with one Integration
Critic. Stop at the terminal checkpoint return and do not inspect, plan, or
begin the next checkpoint.

ORCHESTRATOR BRIEF — BEGIN

# Track B Checkpoint Brief — M4/CP-10

## Target
- Repository: DE-LU day-ahead forecasting, /Users/djourno/Downloads/PJM.
- Authorized checkpoint: CP-10 only — M4 calibration.
- Ratified plan anchor: capstone_v20.md, v20, ratified 2026-09-15.

## Orchestrator-reported expected state
- Branch / commit: main and origin/main both resolve to
  24da4bd13188a4d0e4e7589c61206d8cd62e5ae8. The live remote main was also
  checked at handover and matched. Verify the actual starting state yourself.
- Working tree: clean before preparation of this brief. At delivery, the
  Orchestrator leaves two unstaged orchestration files for owner review:
  progress.md (updated) and docs/track-b/cp-10-brief.md (new). The owner may
  commit these before launch; do not assume either state. Preserve these
  orchestration changes without reading progress.md or absorbing it into
  your engineering work. Report other or intervening changes as found.
- What already exists: v1 is complete, released and closed through CP-3B;
  data/features, the nine-head LightGBM ensemble, calibration, and preserved
  development/holdout evidence exist. The handover reports 191 passing tests
  and the completed 2026-09-15 repository audit; the Orchestrator has not
  rerun that suite or re-derived that audit. Verify relevant starting evidence.
- capstone_v20.md §2.4's pre-CP-10 run-count reconciliation is already done.
  CP-10 has not been executed; no v2 artifact is frozen and no 90-day clock
  has started. CP-3B's missing Integration verdict is disclosed below.
- Verify this yourself before relying on it, and report any material mismatch.

## Observable outcome
A reproducible, independently reviewed calibration comparison establishes which
ratified method is selected on folds {1,2,4,5}, shows every candidate's results
including diagnostic fold_3, and reports whether the pre-registered fix worked.
An unfavourable performance result is a valid outcome; it must not be tuned away.

## Complete authoritative checkpoint bar
capstone_v20.md §9, the COMPLETE CP-10 row, together with its checkpoint
execution and final-candidate verdict requirements, is controlling. The row is:

> All §4.3 candidates implemented with exact fixtures; selection on folds {1,2,4,5} only; the full table including fold_3 for **every** candidate **including the losers**; rule-5 falsification evaluated and reported whichever way it lands; zero crossings; a positive control on every negative assertion; C-2's two-day lag proved with the masking control rather than assumed

Read §4 in full and §§3 and 13 as supporting requirements. C-3 is explicitly
rejected and NOT implemented under §4.3; its recorded rejection is the
deliverable. References to a plan's §12 in the inherited template are generic
legacy numbering: this checkpoint's complete checklist is v20 §9, CP-10.
No convenience extract below narrows or replaces that bar.

## Task-specific supporting extract
- §4.2: the method set is frozen before v2 code runs. Select using one scalar:
  observation-weighted pooled mean pinball on {1,2,4,5}; ties go to the simpler
  method in the listed order. fold_3 is diagnostic only, reported for every
  candidate including losers, and may not influence parameters or selection.
- §4.2 rule 5: if the selected method's fold_3 95% coverage does not exceed
  0.194 by at least 0.20 absolute, report that the fix did not work and retain
  v1 as the recommended frozen artifact. Report the exact evaluation window
  and denominator so the result is inspectable. No fold_3-specific parameter,
  crisis flag, regime switch, or hindsight date threshold is permitted.
- §4.3: run C-1 with BOTH frozen scale estimators: raw head spread
  q_hat_0.95 - q_hat_0.05, and trailing rolling price volatility under the
  delivery-day availability boundary. Run C-2 ACI with gamma selected on
  {1,2,4,5} from a grid frozen before selection runs. The method and scale
  set may not expand; engineering details remain your responsibility.
- §4.3: C-2 may use feedback only through fully observed delivery day D-2 at
  the 12:00 CET D-1 origin. Prove this two-day lag with masking and a positive
  control; do not infer it from a label or assume accumulated history fixes it.
- §4.3 carried bars: the unscaled n_cal=20 one-based-rank fixture remains
  {20,19,17,11} -> Q={8,7,5,-1}; the scaled path gets an exact fixture before
  use. All implemented candidates need exact fixtures. Isotonic stays last.
- §§3 and 13: masking delivery-day prices changes output by exactly 0.0,
  with a D-1 mutation that moves it. Preserve the schema firewall's refusal
  of post-gate A69 and same-day actual columns. Negative assertions need
  positive controls. Zero quantile crossings after the full pipeline is the
  hard correctness gate; favourable performance is never an acceptance gate.

## Applicable constraints
- Governance Lockdown remains active. Do not edit locked plans, rulebooks,
  governance records or agent configuration. If a necessary change arises,
  follow AGENTS.md's exact owner-suspension procedure; do not silently repair
  or reinterpret conflicting ratified requirements.
- Preserve v1: models/champion/, data/snapshot.parquet, data/partitions.json,
  docs/cp2-model-report.md, reports/cp2/, the v1 report, the closed delu-cp2
  experiment, and existing land/* and evidence/* tags are evidence, not
  editable calibration outputs. Keep the reported point-MAE p=0.948 and
  0.194 coverage collapse intact. New calibration results are development
  evidence; neither v1's spent holdout nor a new holdout may be evaluated here.
- Scope is calibration only. No model rewrite, hyperparameter re-search,
  new feature/data track, fuel-price layer, frozen-artifact release, registry
  promotion, daily service or scorecard work. The C-2 sequential-conformal
  amendment is scoped to C-2 only. CP-11 and later are not authorized.
- Reproducibility and the ratified source/availability boundaries remain in
  force: pinned dependencies, fixed seeds, inspectable inputs and reproduction
  commands. Use existing legal data within the plan; preserve its attribution.
- Local Apple M3, 16 GB unified memory, CPU only; $0 expected run rate. The
  inherited $65/month ceiling is not permission to incur cost. Source research
  needed to execute CP-10 is within scope and the same timebox.
- Publication and mainline history are owner-only. No push, remote publication,
  merge into main, or commit/stage on main. Local checkpoint candidate and
  evidence commits follow engineering-role.md on gauntlet/cp-10 only.
- CP-3B landed with item 6 unmet: no Integration verdict binds its final
  candidate. The record is docs/track-b/evidence/cp-3b/item-6-NOT-COMPLETED.md.
  THIS IS NOT A PRECEDENT. CP-10 requires a fresh Integration PASS binding
  the exact final_candidate_sha; no landing without that binding verdict.

## Timebox
Approximately 4 hours, orientation through terminal return. Report elapsed
hours to the nearest half hour. Crossing this estimate triggers the inherited
scope check, not an automatic stop or permission to weaken the checklist.

## Owner-only actions already authorized
The owner authorized CP-10 and supplied this access information on 2026-09-15:
the following variables are available through the macOS launchctl environment:
- DAGSHUB_USER_TOKEN
- MLFLOW_TRACKING_URI
- HF_TOKEN
- ENTSOE_API_TOKEN

Check process inheritance first. If needed, retrieve a named variable using
launchctl getenv inside the consuming process and capture its output privately;
never invoke a bare secret-printing command in visible tool output. Report only
presence/absence, never values. The Orchestrator records owner-supplied access
information; it has not read or tested these secrets. Availability in launchctl
does not guarantee an already-running session inherited the variables.

Existing MLFLOW_TRACKING_USERNAME and MLFLOW_TRACKING_PASSWORD are also reported
in ~/.zshrc; inspect presence via an interactive zsh context if needed, without
printing values. MLflow uses HTTP basic authentication, not Bearer. Do not infer
the MLflow client is configured solely because DAGSHUB_USER_TOKEN is present.
ENTSO-E request URLs and exception text can contain the token; redact both
before logging. Use credentials only as needed within CP-10's authorized scope.
Their availability grants no publication, destructive operation, external cost,
registry promotion or additional checkpoint authority. No such owner-only
action is authorized by this brief.

## Stop and return
Return exactly one of PASS / BLOCKED / INCOMPLETE using
docs/track-b/gauntlet-templates.md §3. Map the complete v20 §9 CP-10 checklist
to direct evidence. Include the Integration verdict path, full
final_candidate_sha and evidence_tip_sha, and the actual evidence-only delta
between them, plus reproduction results, elapsed hours and the Landing report.
Declare every branch, worktree and tag created, with purpose, state and proposed
disposition as required by AGENTS.md. Any interview-answer capture trigger is
named in one line only; capture is suspended and no document entry is filed.
Do not begin, scaffold, or plan the next checkpoint. Do not commit to main,
publish, or push. One brief in, one packet out; the owner carries the handoff.

ORCHESTRATOR BRIEF — END
```
