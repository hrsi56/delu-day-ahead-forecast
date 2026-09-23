# Verdict — CP-16 — Integration — PASS

- Candidate SHA: `bf3ca602e32e99e45c7835e3f95148f62b608099`.
- Plan / version / bar: `capstone_v21.md`, `v21-r3`, complete §14.8, with §§2–9 and complete §14 controlling.
- Anchor SHA256: `67d2176865fea4d6ada0b13bafb128016970d78337d5a936890ddbff7c3ad6ed` (independently verified).
- Reviewer: fresh independent bounded Integration Critic `/root/integration_r3`, assigned by CP-16 Engineering Lead `/root`. No Builder story or conversation history was supplied; review used the committed candidate, assignment and actual execution.
- Checkout: `/Users/djourno/Downloads/PJM/.local/worktrees/cp-16/critic-r3`, fresh detached HEAD at the candidate. Cooperative read-only isolation; no sandbox-enforced immutability is claimed.
- Worktree clean before and after: **yes**, empty `git status --porcelain=v1`; HEAD unchanged. No candidate file or Git state changed. The shared ignored resource ledger and reviewer evidence were written outside the checkout as assigned.
- This PASS binds engineering evaluation at the candidate. It does not promote a model, authorize delivery/publication, or certify the post-review evidence commit before it exists. Item 10's necessary post-review mechanics are explicitly identified below.

## Verbatim bar excerpt

The excerpt below was checked byte-for-byte against the assigned excerpt and the candidate plan. It is the citation.

### 14.8 Complete CP-16 acceptance checklist

Every item is mandatory. Engineering PASS does not require a positive research finding; it
does require a complete valid evaluation and fresh binding Integration PASS.

1. Verify actual repository/input state and preserve other sessions' work and all v1/CP-15
   evidence. Commit the exact ratified amendment, execution brief and complete pre-run protocol
   on the authorized CP-16 candidate branch before new model comparison; document input,
   code, dependency, budget and protocol identities and all permitted origin/target keys.
2. Implement only the fixed A1/B2 central blend, the frozen causal hour-aware residual policy
   and the otherwise identical pooled control. Freeze the two constructions on permitted
   training data before outer scoring; prove that their only difference is hour-aware pooling.
3. Prove origin availability, training-only and origin-specific transforms, D−2 release,
   consume-once, genuine warm-up, complete-day/DST identity, sparse-hour fallback, cache
   identity and restart replay, with negative assertions accompanied by positive controls.
   Preserve relevant inherited namespace guards and all prohibited-partition boundaries.
4. Produce forecasts for every original eligible target in all five folds; report exact
   shared key counts, failed issuance and original exclusions, all finite ordered quantiles
   and emitted p50 separately from central. No missing eligible forecasts, altered targets
   or silently reduced denominators can support completed-evaluation PASS.
5. Independently verify emitted-vector scores, original seven-quantile WIS and equal-fold B0
   normalization, all required per-fold/hour/block/peak diagnostics and their denominators.
   Re-score saved B0/B1/B2/A1 references and B3's diagnostic comparisons without new fits or
   overwriting historical evidence. Keep native v1 pinball separate.
6. Apply the frozen research ranking/paired uncertainty/no-preference rule mechanically,
   report both point and interval effects including negative or mixed findings, and report
   all six unchanged original §8 diagnostics. Distinguish Engineering status, historical
   CP-15 product status, new research findings and product/delivery eligibility. No demonstrated
   joint preference is not equivalence or absence of benefit; disclose mixed effects. No post-hoc
   economic threshold or research-to-product promotion is permitted.
7. Enforce and report every adopted numeric resource/candidate cap, counting warm-up, inner
   selection, failed attempts, controls, corrections and independent reproduction. At the
   first exhausted cap retain partial evidence and return the appropriate non-PASS status;
   no unauthorized scope reduction or resource extension can cure an incomplete checklist.
8. Supply durable protocol, lineage, predictions, metrics, diagnostics, uncertainty, failure/
   resource logs, notices, reproducibility manifest and executable reproduction commands.
   Run relevant controls and regression checks; disclose defects/repairs and invalidated
   outputs. All development results retain their post-selection label and inherited limits.
9. Obtain one fresh independent Integration-Critic PASS on a clean detached checkout of
   the exact final candidate, covering this entire checklist, independently recomputed
   saved-prediction metrics and representative causal/component/state reproduction. Preserve
   commands, exit codes and limits; no self-certification or unsupported PASS.
10. Return the complete canonical checkpoint packet, both terminal SHAs and a verdict-only
    candidate-to-evidence delta, reachable evidence, branch/worktree/tag accounting, elapsed
    effort and all resource totals. End at CP-16's local result, including an honest negative
    result; no next checkpoint, final live-policy selection, publication or mainline operation.


## Commands actually run

All compute commands ran serially from the detached checkout through the candidate monitor and the same cumulative ledger. The definitions used were:

```sh
CP16_PY=/Users/djourno/Downloads/PJM/.venv/bin/python
CP16_BUDGET=/Users/djourno/Downloads/PJM/.local/artifacts/cp-16/budget.json
CP16_PROJECT=/Users/djourno/Downloads/PJM
CP16_LOGS=/Users/djourno/Downloads/PJM/.local/artifacts/cp-16
```

1. **Exit 0**:

```sh
"$CP16_PY" scripts/cp16_v2.py --monitor --ledger "$CP16_BUDGET" --project-root "$CP16_PROJECT" --log "$CP16_LOGS/r3-critic-tests.log" -- env CP16_REQUIRE_SAVED_EVIDENCE=1 "$CP16_PY" -m pytest tests/cp16 -q -s -p no:cacheprovider --basetemp="$CP16_PROJECT/.local/tmp/cp-16/r3-critic-tests"
```

Observed **84 passed in 41.09 seconds**; wrapper elapsed 42.039104 seconds, peak process-tree RSS 743,636,992 bytes, no abort. The separate saved-vector oracle does not import the CP-15/CP-16 scorer or models: it recomputed all metrics, diagnostic rows and denominators, criteria, ranking and 2,000 paired bootstrap replicates to atol/rtol `2e-12`. Its hand-calculated WIS, tamper, missing-calendar/variable-hour and tie controls also passed. The independent state oracle rebuilt all 638 real date-fold origins and all **21,494 H/P evaluation rows**, with **maximum absolute difference 0.0**, exact buffer/scale/central hashes, exact admission vector hashes, and matching persisted final states. Real admission-state restart matched saved first-evaluation vectors; wrong origin, scale, keys and training cache identities were refused. Synthetic tests cover D−2/D−1, consume-once, partial truth/day, 23/24/25-hour canonical identity, sparse fallback, linear quantiles/ties, issued versus current scale, positive sensitivity, and resource refusal/monitor failure. Real replay charged 1,276 + 152 policy-days; saved-reference and analysis counters each increased by one.

2. **Exit 0**:

```sh
"$CP16_PY" scripts/cp16_v2.py --monitor --ledger "$CP16_BUDGET" --project-root "$CP16_PROJECT" --log "$CP16_LOGS/r3-critic-components.log" -- "$CP16_PY" tests/cp16/reproduce_components.py --output "$CP16_LOGS/r3-critic-components.json"
```

Observed wrapper elapsed 90.968863 seconds, peak RSS 1,008,713,728 bytes, no abort. Fresh A1/B2 fits on fold 1 / 2020-07-01 and fold 2 / 2021-04-01 each reproduced with **0.0** maximum absolute forecast difference and exact model, imputer, scaler, training-target, normalization, hourly-training, inner-training and validation fingerprints. Each fitted component used 120 primitive calls. Delivery-day/future mutation gave **A1=0.0, B2=0.0**; the available D−1 positive mutation gave **A1=425.36057961143297, B2=485.17021664721653**. Limits were component atol `1e-8`, rtol `1e-10`, exact fingerprints and exact zero/nonzero causal assertions. Charged eight policy-days, eight component attempts and 960 primitive fits (768 inner, 192 final).

3. **Exit 0**:

```sh
"$CP16_PY" scripts/cp16_v2.py --monitor --ledger "$CP16_BUDGET" --project-root "$CP16_PROJECT" --log "$CP16_LOGS/r3-critic-guards.log" -- "$CP16_PY" -m pytest tests/cp15/test_pipeline.py tests/test_02_rolling_closed_left.py tests/test_05_schema_firewall.py tests/test_08_partition_integrity.py tests/test_12_partition_exclusion.py tests/test_24_live_namespace_is_walled_off.py -k 'not test_fit_delivery_mask_positive_d1_and_rolling_refit' -q -p no:cacheprovider --basetemp="$CP16_PROJECT/.local/tmp/cp-16/r3-critic-guards"
```

Observed **48 passed, 3 deselected in 5.00 seconds**; wrapper elapsed 5.969266 seconds, peak RSS 340,770,816 bytes, no abort. Deselection was the three explicitly excluded inherited model-fit cases, not a failed test. Applicable schema, rolling, partition and live-namespace guards passed. Synthetic inherited checks also verified origin-specific 168-hour transforms and DST handling. No live mutation or unauthorized reference model fit occurred.

4. **Exit 0**, reviewer-authored metadata audit (no new outcome scoring or real replay):

```sh
"$CP16_PY" scripts/cp16_v2.py --monitor --ledger "$CP16_BUDGET" --project-root "$CP16_PROJECT" --log "$CP16_LOGS/r3-critic-metadata.log" -- "$CP16_PY" "$CP16_PROJECT/.local/tmp/cp-16/critic-r3/metadata_audit.py"
```

Observed 28 artifact hashes, 20 implementation hashes, 34 input identities and all pinned installed dependencies matching. The exact complete protocol is present unchanged in pre-run commit `9cf64e2403cdcf7d367a06da72688b0d55e39f1f`; all 35 training-only admission dates and their committed freeze match `225cc92b53f917d920a037881604d1cd6cc6e9db`. Thirteen preserved historical report/evidence artifacts match their original bytes at `41b0e6d222a3d65d474ac5974c6eb7017db317e8`. All 87 changed files are within the supplied governance packaging and CP-16 envelope. No changes to inherited CP-15 source/results, data, models or CP-2 results. All cited earlier candidates/freeze commits remain ancestors of `gauntlet/cp-16`. Wrapper elapsed 0.800119 seconds, peak RSS 132,972,544 bytes, no abort.

Read-only inspection commands also returned exit 0: `git status --porcelain=v1`, `git rev-parse HEAD`, `shasum -a 256 capstone_v21.md`, `git log --format='%H %s' -10`, `git diff --stat main...HEAD`, `git worktree list`, `git branch -vv`, `git rev-list --left-right --count main...gauntlet/cp-16`, `git tag --list 'land/cp-16*' 'evidence/cp-16*' 'archive/cp-16*'`, and `git log --format='%H %cI %s' 41b0e6d222a3d65d474ac5974c6eb7017db317e8..HEAD`. File inspection used `cat`, `sed`, `rg`, and `tail` on the evidence/source paths listed below. Initial and final status were empty; main remained `6621402b2be9aed85be433432bcffffb56adf3e4`; candidate branch was six ahead/zero behind main; no CP-16 disposition tags existed.

## Evidence actually inspected

- Exact assignment, `engineering-role.md`, canonical template §2 and terminal §3, controlling plan §§2–9 and complete §14, issued CP-16 brief.
- All `src/cp16/*.py`, the driver, inherited `src/cp15/data.py` and `models.py`, and the independent saved-vector/state/component checks plus residual, input, resumption, monitor and relevant inherited pipeline tests. Production scoring implementation was checked against the independent scalar/vector oracles and the ratified formulas.
- `reports/v2-causal/protocol.json`, `input-manifest.json`, `artifact-manifest.json`, lineage/admission state through independent verification, predictions through both independent audits, every numeric table through the independent table checker, empty current failures, `resources.json`, report and reproduction instructions.
- `data/partitions.json`; permitted projected raw inputs only through monitored replay/component checks. No spent holdout/reserved-tail outcomes were materialized by review. Input hashing is identity verification, not outcome access for fitting or selection.
- Resumption feasibility and limitation notices; historical packet/reviewer identity to establish their historical status; all 13 preserved historical artifacts by byte comparison; prior FAIL/candidate chain by reachability. Current fresh reviewer identity is recorded in this verdict and must replace the historical top-level reviewer record during terminal evidence packaging.
- Actual new review command logs, component JSON, metadata script/output and shared budget ledger. No orchestrator, progress, syllabus or Track A/C document was read.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1 | Repository/input preservation and committed complete pre-run identities | PASS | Clean exact candidate; 34 input/20 implementation hashes and dependencies match; protocol freeze precedes admission and evaluation in candidate history; original and historical artifacts unchanged/reachable; complete permitted keys and origin manifest verified. |
| 2 | Fixed A1/B2 central blend and only H/P pooling difference | PASS | Shared state and emitted-vector parity checks; blend uses genuine central forecasts and issued A1 scale; fixed n/(n+56), 14-day fallback and 28-day buffer; all 35 training-only dates frozen before outer comparison; no alternative recipe. |
| 3 | Causal/component/state invariants, controls and forbidden boundaries | PASS | Independent complete H/P state replay, real restart/cache refusals, exact fresh component/fingerprint reproduction, exactly-zero delivery mutation and nonzero D−1 control; synthetic/DST/scale tests and 48 inherited guards. Load predicate/projection precedes outcome materialization. |
| 4 | Every original eligible target, denominators and valid emitted quantiles | PASS | 75,229 rows, seven policies ×10,747 identical keys; fold counts 2,160/2,159/2,112/2,160/2,156; immutable matched truth/references; zero missing/nonfinite/crossings/failures. Central and shifted p50 separately retained and scored. Original exclusions independently enumerated below. |
| 5 | Independently verified scores, diagnostics and immutable references | PASS | Independent formulas recalculate MAE/RMSE/WIS, central effect, coverage/width/misses, daily level/shape, hours/blocks/peak/recovery and all denominators within 2e-12; five saved references match original vectors exactly; native nine-quantile v1 pinball stays separate. |
| 6 | Frozen ranking, paired uncertainty and six original diagnostics | PASS | Independent full 2,000-replicate bootstrap and index fingerprint; all 42 criterion rows; H then P descriptive ranking; primary no demonstrated joint preference; H−B2 joint improvement and P−B2 mixed evidence correctly disclosed; both new §8 results not_met, historical CP-15 NOT_DEMONSTRATED, no delivery authorization. |
| 7 | Every cap and cumulative historical/review accounting | PASS | Same persistent ledger, pre-call fit/replay reservations, fail-closed monitor controls; historical3,730 retained unchanged; final review counters below every cap; historical RSS/thread gaps explicitly unknown rather than retrospectively certified; required evidence regenerated. Details below. |
| 8 | Durable complete artifacts, reproducibility and defect disclosure | PASS | All required artifacts present and hashed, production/verification commands executable, tests and regression controls pass, prior failed/invalid evidence retained, resumption repair/fixture defect disclosed, current outputs development_post_selection with inherited limits. New local reviewer files must be imported into evidence in terminal packaging. |
| 9 | Fresh exact-candidate independent Integration | PASS | This clean detached read-only review independently recomputed metrics/uncertainty, every H/P vector and representative components/causal controls; commands/exits/tolerances preserved. Reviewer did not build or repair the candidate. |
| 10 | Canonical terminal packet, two SHAs, evidence-only delta and local stop | PASS for candidate readiness; post-review mechanics unverified | Candidate contains all evaluation evidence and a valid prescribed two-SHA procedure. The historical packet is not the current terminal return. Lead must import this verdict/logs/script, refresh reviewer identity/resource snapshot and canonical packet under evidence paths, commit evidence only, name actual evidence tip and verify delta/reachability, then remove the assigned Critic checkout and stop. No claim that these future steps already occurred. |

## Independent population and research observations

Original exclusions relative to actual local canonical calendars: fold1 0; fold2 one hour on 2021-04-04; fold3 24 hours each on 2022-07-20 and 2022-07-21; fold4 0; fold5 one hour each on 2026-03-30, 2026-03-31 and 2026-04-05. Fold5's full calendar contains2,159 hours because of spring DST; its three original exclusions leave2,156. These are inherited exclusions, not new failed issuances. Full fold3 is2,112 hours/88 represented dates; peak2022-08-15..31 is408 hours/17 dates.

H/P primary equal-fold scores are H: S_MAE0.6440721386286878, S_WIS0.6160299894915677; P: S_MAE0.6457675850846845, S_WIS0.6287217727210093. H−P MAE difference−0.0016954464559965077 has 95% interval [−0.003623724975937509, +0.000003857628092332211]; WIS difference−0.012691783229441422 has interval [−0.015571242603026905, −0.010911902067713655]. The small positive MAE endpoint cannot be rounded to zero to pass the joint rule. Thus **no demonstrated joint preference**, without claiming equivalence or no benefit/harm. Both policies fail unchanged original criteria1 and2; criteria3–6 are met. These are post-selection research findings, not promotion authority.

## Resource and scope accounting

After the four monitored reviewer commands, shared cumulative totals were:

| Resource | Observed cumulative | Cap |
|---|---:|---:|
| Policy-days | 6,458 (includes historical3,730) | 9,000 |
| Component attempts / main subset | 121 /93 | 2,000 /1,500 |
| Primitive fits / inner / final | 14,484 /11,588 /2,896 | 240,000 /192,000 /48,000 |
| Saved-reference passes / analysis passes | 2 /2 | 3 /3 |
| Charged machine seconds | 1,936.6892893761687 | 86,400 |
| Active effort upper bound at last sample | 5,716.285843133926 seconds | 144,000 |
| Highest measured historical process-tree RSS | 1,256,341,504 bytes | 10,737,418,240 |
| Highest measured checkpoint disk upper bound | 567,967,852 bytes | 21,474,836,480 |

The final Lead handover must refresh elapsed/effort accounting through terminal packaging. The observed reviewer runs added1,436 policy-days, eight attempts,960 primitive calls and one reference/analysis pass each. No full-suite retry was made. Fixed scope: two new policies plus five saved references; one hourly residual recipe plus one pooled control; two inherited central configurations; one inherited feature recipe; seeds42/15042; two blend members;638 unique date-fold keys (each fold≤150),35 admission dates ×two policies. Zero alternative outer-score trials, new reference fits, sources, downloads, economic/weather/neural/VRE runs, GPU/cloud jobs, external cost, schedules or remote mutations. Resumed numerical compute is serialized with BLAS environment one; actual resumed threadpool evidence is preserved. Historical monitor-failure RSS and early thread claims remain unknown, as explicitly permitted/disclosed by the resumption contract; regenerated evidence supplies current acceptance.

## Terminal evidence obligations and accountability

No branch, worktree or tag was created by this Critic. The Lead-created fresh detached `critic-r3` checkout remains clean at the reviewed SHA for Lead removal after evidence import. The active `gauntlet/cp-16` and `lead` checkout remain owned by the Lead. No mainline or publication operation was performed. The historical candidate/evidence, protocol and admission commits are reachable on the candidate branch.

This is the engineering verdict, not the canonical checkpoint return. Before a terminal checkpoint PASS, the Lead must preserve the current review evidence under `docs/track-b/evidence/cp-16/`, update only that evidence directory for the canonical return/current reviewer identity/final resource accounting, and verify:

```sh
git diff --name-only bf3ca602e32e99e45c7835e3f95148f62b608099..<actual_evidence_tip_sha>
git merge-base --is-ancestor bf3ca602e32e99e45c7835e3f95148f62b608099 gauntlet/cp-16
```

The first command must name nothing outside the checkpoint evidence directory. Actual evidence tip, final canonical packet, final effort accounting, verdict import and worktree removal are necessarily unverified post-review actions. Any source/report/protocol change requires a new final candidate and fresh independent review. No next checkpoint or live-policy selection is authorized by this PASS.

Interview-answer capture trigger for Lead return: preserving missing calendar dates and variable-hour denominators in paired bootstrap, and why a tiny positive MAE confidence endpoint prevents joint preference despite a supported WIS gain. Critic files no Q&A.

## Reviewer artifacts and hashes

Paths below are local reviewer artifacts for durable import; the metadata script contains only provenance/identity/metadata checks and no new outcome scoring. The Lead must not leave these as sole ignored copies.

caf89182cd7c27e9b0f1ad5148cdbd68e7880530add4fda57ba2fc29859a5f55  /Users/djourno/Downloads/PJM/.local/artifacts/cp-16/r3-critic-tests.log
11966cc2b8bb78eb60357c8d48530562b29fb9934e439413fe30c9029c675e1c  /Users/djourno/Downloads/PJM/.local/artifacts/cp-16/r3-critic-components.log
2f89f5f81c6c8f6d5b313f4b1c5563cac3f3d643a6faf86602b7bd1f34360071  /Users/djourno/Downloads/PJM/.local/artifacts/cp-16/r3-critic-components.json
e95df1f8d9f2aaf0bb91bc3ed446f855b9d79cb6eb79bddc056714a27baf9854  /Users/djourno/Downloads/PJM/.local/artifacts/cp-16/r3-critic-guards.log
6ee391f0f0dc1e6f970925641880d6d599c9623ce15d6e0382f81e77e6cd2237  /Users/djourno/Downloads/PJM/.local/artifacts/cp-16/r3-critic-metadata.log
bfd7b8326cebb90ae278ce0c6b47db2cdfa36316c01c305c0f79552a771c7d49  /Users/djourno/Downloads/PJM/.local/tmp/cp-16/critic-r3/metadata_audit.py
