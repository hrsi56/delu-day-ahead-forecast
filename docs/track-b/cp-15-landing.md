# CP-15 landing record — 2026-09-16

> Subsequent owner-authorized consolidation leaves only `/Users/djourno/Downloads/PJM`
> on `main`. Temporary checkout paths and retained-branch descriptions below record the
> landing-time state. Retrieve current evidence from the sole checkout or `evidence/cp-15`.
> The pending documents/Q&A were consolidated; superseded drafts remain in the project-local
> `.local/artifacts/PJM-consolidation-backup-2026-09-16` archive.

## Disposition and authority

LAND of the completed experiment and evidence, including four inherited CP-10 commits.
The owner explicitly authorized commit, merge and push for this task. This instruction
supersedes the default owner-executed landing/publication procedure for this task only;
no standing governance text was amended. Product feasibility remains **NOT_DEMONSTRATED**.
No policy is frozen or promoted, no reserved outcomes are opened, and no prospective clock starts.

## Immutable identities

| Item | Reference |
|---|---|
| Reviewed candidate | `fc4aee038cf898998a292506df62ddb0dcfaf22a` |
| Reviewed evidence tip | `1bdc75b8ab943092bb8de6ba893defb9e12250d8` |
| Experiment squash / `land/cp-15` | `0be8e56726262336ead20adc70c69668ba59e1f6` |
| Permanent chain / `evidence/cp-15` | `1bdc75b8ab943092bb8de6ba893defb9e12250d8` |
| Verified identical experiment/evidence tree | `53a093a8ae22d9bc8dc93ac127008c6cd124e244` |
| Previous main | `3618658ec16d57795a69c68ccb4cbdab926d73a5` |
| Inherited CP-10 evidence tip | `4039ce24150b36ea233b043061e68eb2be78cbbe` |

The experiment commit contains exactly the reviewed evidence-tip tree: 150 changed files,
147,745 insertions and 12 deletions relative to previous main. Operational progress and this
record are committed separately. The landing does not alter source, predictions, thresholds,
plan bytes, verdicts or conclusions. The original failed attempt remains preserved.

[Binding Integration PASS](evidence/cp-15/integration.md) ·
[Scientific report](evidence/cp-15/report.md).
The previously reported 339 passing tests and independent reproductions are accepted from
Integration; the Orchestrator did not rerun engineering or independently recompute scores.
Landing checks: staged tree identity, whitespace validation, candidate ancestry under the
evidence tag, ref reconciliation and preservation of pending work.

## Current retrieval and lifecycle

- `gauntlet/cp-15` was dispositioned LAND and deleted only after verifying its evidence tag.
- `/Users/djourno/Downloads/PJM-cp-15` was removed after preserving all 26 ignored top-level
  paths, including environments, caches and logs. Temporary Builder/Critic worktrees were
  already removed by the Engineering Lead.
- Current main checkout: `/Users/djourno/Downloads/PJM-main-landing`, created for this landing.
  Read current CP-15 reports/evidence there. Historical briefs/verdicts keep original execution
  paths and branch names as historical facts; retrieve their exact tree through `evidence/cp-15`.
- Primary `/Users/djourno/Downloads/PJM` remains dirty and preserved. After the owner’s
  cleanup request, `gauntlet/cp-10` was renamed `codex/orchestration-pending`; its HEAD and
  pending files were preserved. CP-10 history remains reachable through `evidence/cp-15`.
  Its CP-10 code is included in this landing; its pending orchestration/docs/Q&A work is separate.
- `/Users/djourno/Downloads/PJM-orchestrator-v20-review` on `codex/v20-plan-corrections` remains
  dirty and preserved. Neither retained branch was reset, deleted or published.
- Created tags: only `land/cp-15` and `evidence/cp-15`. No new branch was created.
- Local backup/verification packet:
  `/Users/djourno/Downloads/PJM/.local/artifacts/PJM-cp15-landing-record-2026-09-16/`.
  `pending-work-manifest.json` records pre-landing file hashes; `checkpoint-local-artifacts.json`
  maps retained caches/logs. `landed-experiment.diff` contains the full experiment diff.
- Original detailed per-file engineering rationale remains in
  `/Users/djourno/Downloads/PJM/.local/artifacts/PJM-cp15-r1-handoff/files-changed.md`.

## Next decision

CP-16 requires a bounded candidate set, complete acceptance bar, owner-authorized scoped
plan amendment and a new brief. B2 and A1 supply the comparison references. Historical
as-of input availability remains a research constraint; the Chronos-2 feasibility probe is
not evidence of product quality or a blind historical test. Existing development results
remain post-selection. No executor or next checkpoint was started by this landing.
