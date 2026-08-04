# Capstone v6.3 → v6.4 Amendments — Gauntlet Execution Contract and Statistical-Audit Corrections

*Authored and owner-ratified 2026-08-02. The changes are already applied in `capstone_V6_5.md`. This sheet is the durable change record; it does not authorize M1 execution by itself. M0 remains closed, M1 has not started, and CP-1 remains the next Track B checkpoint.*

## Scope and invariants preserved

This release changes the Track B execution contract and closes three methodological evidence gaps. It does **not** reopen the scientific/product scope.

Preserved unchanged:

- all five §0 decisions;
- strict-gate champion and the runtime ban on delivery-day A69/actual columns;
- A75 as a proper-training-only fit target;
- the four 2×2 catalogs, retention rule, and deterministic winner;
- five pinned walk-forward folds and 24-hour embargo;
- nine LightGBM quantile heads, four CQR pairs, unshifted p50, isotonic-last;
- three-stage coverage and the final-output empirical coverage gate;
- the §7.2 post-gate benchmark;
- the five §9.4 property tests;
- gas/weather/SFTP decisions, spectral boundaries, DuckDB mart, health report, static-first page, and every surviving §13 boundary.

## AMD-1 — Selection-separated forward confirmatory audit

### Problem corrected

The five pinned folds participate in catalog selection, tuning, and development. Their DM p-values therefore cannot also be presented as untouched confirmatory evidence.

### Ratified contract

- CP-1 freezes `selection_cutoff` at the last complete delivery date in the M1 selection snapshot.
- Every later delivery date belongs to a quarantined forward-audit partition.
- No post-cutoff target, prediction loss, metric, comparison, or narrative may enter catalog selection, tuning, calibration, or remediation for this release.
- The five original folds stay unchanged and remain the M2 development gate plus regime/stress diagnosis; their DM results are labeled `development_post_selection` and are descriptive.
- CP-2 freezes catalog, hyperparameters, preprocessing, seeds, comparator, loss construction, code commit, and manifests.
- CP-3 freezes the complete CQR-then-isotonic champion before audit outcomes are opened.
- The forward audit runs once on the first eligible fixed window and is never recycled into training or repair. A post-audit change requires a new model release and a new future window.

### Duration and power rule

Before outcomes are opened:

1. `δ*` is fixed at 10% of the similar-day naïve mean daily pinball loss on development Folds 4–5.
2. `LRV_ref` is the larger Fold-4/Fold-5 Newey–West long-run variance from the frozen final pipeline.
3. `N_80 = ceil(((z_0.95 + z_0.80)^2 × LRV_ref) / δ*^2)`.
4. `N_required = max(90 complete delivery days, N_80)`, spanning at least twelve complete calendar weeks.
5. Eligibility is determined from input/target completeness only, before losses are inspected.

If `N_available < N_required`, outcomes remain sealed and status is `PENDING_UNDERPOWERED`; no inferential p-value becomes a gate. Once eligible, the one-sided daily-vector probabilistic DM runs once at α=0.05. `CONFIRMED` requires `mean(d)<0` and `p<0.05`; otherwise status is `NOT_CONFIRMED`. All three statuses govern the public claim: `PENDING_UNDERPOWERED` permits no confirmatory headline, `CONFIRMED` supports only the pre-registered claim, and `NOT_CONFIRMED` forbids that claim. None changes the honesty of the artifact.

### Sections changed

§5.1, §7.1, §9.1, §10, CP-1, CP-2, CP-3, CP-5.

## AMD-2 — Point-in-time load evidence

### Problem corrected

The Month-0 spike observed A65/A01 at 15:35 CEST D-1. That supports availability but occurs after the 12:00 gate and cannot prove empirical pre-gate presence.

### Ratified capture contract

- Regulation 543/2013 remains the regulatory pre-gate basis.
- M1 captures A65/A01 on at least three non-consecutive delivery days at approximately 10:30 and 11:45 Europe/Berlin on D-1.
- Each qualifying day must show a complete DST-aware D+1 vector before 12:00.
- Failed, partial, or rate-limited attempts remain in the ledger but do not count.
- Raw responses are retained and each attempt records identifiers, delivery date, gate/pull timestamps, UTC offset, status, expected/observed rows, completeness, first/last delivery time, latest complete time, SHA-256, artifact path, and outcome class.
- Regulatory proof, “observed available by” evidence, and exact first-publication time remain distinct claims.
- A69 remains post-gate/benchmark-only; A75 remains a fit target, never runtime.

### Sections changed

§3, §5.2, R-2, CP-1.

## AMD-3 — Experiment lineage replaces run counting

### Problem corrected

`≥5 experiments` rewards cosmetic runs and does not prove a defensible decision trail.

### Ratified contract

Every decision-bearing MLflow run or grouped search records:

- hypothesis ID and pre-run hypothesis;
- parent run/baseline and intended delta;
- fixed search/tuning budget;
- snapshot hash, training cutoff, and audit-exclusion manifest hash;
- fold/catalog IDs, code commit, seed, metrics, and artifact links;
- terminal `keep`, `reject`, or `invalid` decision with rationale;
- `evidence_class = development_post_selection | forward_confirmatory` for DM evidence.

All four catalog experiments, the selected CP-2 model, M3 calibration, and registered champion form one public traceable lineage. No minimum run count applies.

### Sections changed

§9.1, §9.3, §10, CP-2, CP-4, CP-5.

## AMD-4 — Mandatory independent CQR threshold critic

### Failure surface

The CQR threshold rank is mathematical one-based indexing. A plausible off-by-one implementation can produce credible-looking coverage while using the wrong conformity score.

### Binding rule

For each pair:

`k = ceil((n_cal + 1) × (1 − α))`

`k` is one-based; a zero-based implementation reads `scores[k−1]`. It must not read `scores[k]`, use an interpolated default quantile, or silently clip an out-of-range rank. The production calibration slices are large enough for a finite threshold at every planned α.

The independent M3 Critic starts from the raw synthetic rows `j=0,…,19` with `(q̂_lo,j,q̂_hi,j,y_j)=(100,140,111−j)`, recomputes `E_j=max{q̂_lo,j−y_j,y_j−q̂_hi,j}=j−11`, and thereby obtains the sorted scores `−11,−10,…,8`:

| α | one-based k | zero-based position | expected Q |
|---:|---:|---:|---:|
| 0.05 | 20 | 19 | 8 |
| 0.10 | 19 | 18 | 7 |
| 0.20 | 17 | 16 | 5 |
| 0.50 | 11 | 10 | −1 |

It also verifies negative-Q narrowing, unshifted p50, isotonic as a separate last step, and all four real thresholds from persisted calibration predictions for at least one fold.

This is the fifth mandatory **Critic surface**. It does not change the count of five §9.4 property tests; the fixture joins thin CI at M3.

### Sections changed

§6.2, §9.4/CI note, CP-3.

## AMD-5 — Track B Gauntlet execution contract

### Authority split

- The Orchestrator chooses the repo, single checkpoint, exact ratified anchor, goal/bar, complete named checkpoint checklist, timing, and numeric total active-elapsed wall-clock ceiling.
- The Engineering Lead chooses implementation, decomposition, agent count, parallelism, internal allocation, and review rounds.
- Yarden transfers one brief inward and one terminal return packet outward. He never routes internal agent messages.

### Independent execution

- Important pieces use separate fresh-context Builders and fresh read-only Critics.
- **Operational hardening, owner-ratified 2026-08-04:** the Engineering Lead is the sole Git writer on local disposable `gauntlet/<checkpoint>`. Builders work only in Lead-created isolated writable detached worktrees/snapshots on disjoint allowlisted paths and never stage, commit, merge/switch branches, update refs, or share a writable index. The Lead imports exact allowlisted paths, verifies the staged path set, and commits serially.
- Every candidate is committed by the Lead before review. Critics work only from a newly created clean detached worktree at the full candidate SHA/tree (or immutable equivalent), never any Builder checkout/uncommitted diff and never `workbench.md`.
- Before each component or Integration review, the Lead allocates its run/piece IDs and creates a non-overwriting `refs/gauntlet-evidence/<checkpoint>/<run-id>/<piece>` ref at the exact current candidate `HEAD`. Each unique run root contains exactly two records outside the checkout: a helper-owned integrity manifest with matching clean create/verify SHA/tree/status evidence and pre-review-manifest hash protection, and a schema-valid Critic verdict binding piece/ref, candidate SHA/tree, committed schema/tool hashes and artifact hash. The verdict's plan binding is exact: `plan.filename` is a safe repository-relative committed `.md` path, `plan.sha256` hashes that blob's bytes at the candidate SHA, `plan.version` and `plan.bar_citation` are the human identifiers, and the verbatim `plan.bar_excerpt` must occur in the same bound blob. It also binds decision-bearing input hashes, exact commands/tolerances plus exit codes and stdout/stderr hashes, and hashed inspected evidence. Neither record substitutes for the other. Any missing/invalid record/ref, unsafe or mismatched plan binding, absent/non-verbatim excerpt, reused/mutable run, unhashed evidence, dirty checkout, or changed SHA/tree invalidates the verdict.
- A FAIL returns one largest meaningful gap and exact rerun condition.
- There is no arbitrary round count.
- Mandatory surfaces when in scope: temporal normalization; champion/benchmark firewall; A75 fit lineage; four-catalog recomputation; M3 CQR threshold recomputation.
- At M1, the first three surfaces execute five independent oracles: misaligned-chunk stitch, missing-quarter rejection, fall-back DST identity, A75 fit-lineage poisoning, and runtime-schema poisoning. The Critic materializes/hashes the inputs and computes expected results independently; Builder tests alone are insufficient.
- Every component `PASS` used for terminal `PASS` must bind the exact final candidate SHA/tree. Any candidate change invalidates all earlier component `PASS` verdicts, so all required component Critics rerun; selective reuse by reviewed path is forbidden. Every checkpoint ends with a fresh Integration Critic in a separate clean detached checkout at that same final SHA/tree. Relied-on component and Integration verdicts share the plan identity (`plan.filename`, `plan.version`, and `plan.sha256`), while each keeps a piece-appropriate `plan.bar_citation` and `plan.bar_excerpt`; each excerpt is independently validated verbatim against that same blob, and citation/excerpt pairs need not match one another.

### CP-2 label-blind four-catalog hardening — owner-ratified 2026-08-04

The scientific four-catalog rule is unchanged but its boundaries are now exact in capstone §4.1: machine IDs `strict_base`, `residual_arm`, `scarcity_arm`, `both_arms`; observation-weighted pinball across all frozen rows/folds/nine quantiles; inclusive submitted q10≤y≤q90 raw coverage; Decimal/canonical CSV arithmetic; equality passing at 1%, 2 pp and 0.1%; strict positive improvement on at least four folds; explicit base-loss-zero and minimum-loss-zero behavior; and feature-count, absolute calibration-error, then fixed arm-order tie-break. Raw crossing is legal and unchanged at M2; CQR/isotonic remain M3.

CP-2 now requires a **label-blind four-catalog review**, never generic Blind A/B. The final candidate first commits hash-bound `artifacts/cp2/blind/source-manifest.json` and `artifacts/cp2/blind/selection-declaration.json`. `blind-prepare` creates the anonymous interleaved `blind-public-input.csv`, `blind-public-manifest.json`, `blind-commitment.json` and `blind-preparation-receipt.json` in the Blind support root, while its 256-bit seed/permutation, real mapping, source identities and tool-generated `preparation-invocation.json` remain create-only under `.gauntlet/evidence/CP-2/_blind-custody/<blind-review-id>/` (`0700` directory, `0600` files); any harness log remains Lead-private and outside the Blind allowlist. The commitment binds the exact preparation-invocation hash, and the later safe receipt binds the exact custody-record hash. The Blind Critic runs `blind-recompute`, freezes identity-free `blind-metrics.json` only, hash-binds the receipt in `blind_review`, sets `blind_review.identity_decision` to `NOT_PERFORMED`, and never applies eligibility/tie-breaks or chooses a winner; every support filename/raw byte stream and every verdict string is identity-scanned. Only after its schema-valid `PASS` may `blind-freeze`, as the sole allocator, create a fresh Integration run/ref/support from supplied fresh run/piece IDs; it rejects every preallocated identity, exactly reproduces the revalidated verdict/integrity provenance, then creates `blind-freeze.json` and five Integration-owned frozen copies before `blind-reveal` creates `blind-reveal.json`. Reveal verifies invocation→manifest→commitment→custody→receipt chronology, the receipt-bound custody hash, and every custody source path/hash against the committed source manifest and hidden preimage; it then copies—never hard-links—the mapping, four real canonical source CSVs, source manifest, selection declaration and safe preparation record into Integration support. Fresh Integration runs `blind-adjudicate` only against those copies, creates `blind-adjudication.json`, validates the chain and verifies the committed winner. Run roots remain exactly two files; all other files live in their owned support roots. The machine contract is `docs/track-b/schemas/cp2-blind-four-catalog.schema.json` and the five canonical commands in `scripts/gauntlet_protocol.py`.

Every record is create-only. Any SHA/source/rule/selection change, Blind `FAIL`, premature exposure, tamper, reuse or winner mismatch preserves the attempt but forces new blind/run/ref IDs, 256-bit seed/permutation/custody and complete freeze/reveal/Integration chain; revealed maps are never reused. `0700/0600` and hashes prove custody state/chronology, not non-observation by a same-UID process. Only a real read sandbox/allowlist excluding custody, identity source files/manifest, selection, reveal/preparation material or harness logs and Git/object-store bypass supports `ENFORCED_READ_ISOLATION`; otherwise the packet must say `COOPERATIVE_PROCEDURAL`.

### Terminal states

`PASS`, `BLOCKED`, `PLATEAU`, or `BUDGET_EXHAUSTED`. Only PASS advances, and only after every criterion, applicable mandatory Critic, and Integration Critic pass. Budget exhaustion never weakens the bar. At every terminal state Track B stops before inspecting or planning the next checkpoint.

### Workbench and return

`workbench.md` is ignored by Git and is active-checkpoint operational visibility only. It never enters a candidate commit or Critic checkout/context. The Orchestrator never reads it, Yarden never carries it upward, and `progress.md` never imports from it. A renamed final snapshot is archived with checkpoint evidence only if unique, or removed at terminal return, and never reused in the next checkpoint.

Live review evidence resides only under ignored `<repo>/.gauntlet/evidence/<checkpoint>/`, outside every Builder/Critic worktree and candidate Git tree. Under one exclusive initialization lock, `init-evidence` creates every unique immutable `<critic-run-id>/` child together with `_support/<critic-run-id>/` and rolls back an ordinary partial-creation failure; neither may preexist, be reused or traverse symlinks, and an observed half-pair fails closed rather than being completed. This is lock/rollback/fail-closed pair initialization, not an atomic paired-directory primitive. The run child contains exactly its integrity manifest and verdict record. Every file-backed artifact/input, command stdout/stderr or evidence path in that verdict must be a regular non-symlink file inside its uniquely owned support root, have SHA-256, and have inode link count (`st_nlink`) exactly one. A hard-linked inode is invalid and may not be borrowed or shared across another support root, run, temporary directory, snapshot, or any other path; safe hash/lineage manifests replace raw restricted or impractically large data. The optional frozen workbench and terminal packet may remain elsewhere under the checkpoint root because they are not verdict evidence. Prose-only observations do not satisfy evidence. Live evidence is not committed under `docs/`, which would recursively change the reviewed SHA. Candidate refs are created before review, never pushed or moved, and only Yarden may delete them; before terminal return the Lead reverifies every cited ref, and the disposable branch is not spent until that succeeds.

The Checkpoint Return Packet is the only upward artifact. It maps the complete named checklist to reproduction evidence; inventories every unique Critic run/root/support root and every ref/SHA pair; records active-elapsed UTC timestamps, eligible pauses, raw consumed seconds, separate integrity-manifest and schema-valid verdict paths/hashes, Critic SHA/tree, exact `plan.filename`/`plan.version`/`plan.sha256`/`plan.bar_citation`/verbatim `plan.bar_excerpt`, input and command provenance, single-link support-file validation, and Integration verdict; preserves decisions/rejected alternatives and the largest repaired failure; includes 3–5 defense questions; and declares Track B stopped.

### Measurable execution clock

The 22 h reserve below remains a **program planning-load estimate**. Each issued checkpoint ceiling is enforced as one active elapsed wall clock from orientation through terminal return:

`consumed_active_elapsed_seconds = terminal_at_utc − started_at_utc − Σ eligible_pause_seconds`

All timestamps are ISO-8601 UTC. An eligible pause requires every authorized context/tool to be stopped for an already-authorized external dependency or platform suspension. Parallel contexts overlap and never sum. A newly needed owner action, credential, source, or authority terminates `BLOCKED`; it is not an excluded pause. Raw seconds control exhaustion; displayed decimal hours are informational.

## Cost and schedule consequence

Ratified incremental reserve:

| Checkpoint | Gauntlet reserve |
|---|---:|
| CP-1 | 6 h |
| CP-2 | 5 h |
| CP-3 | 5 h |
| CP-4 | 3 h |
| CP-5 | 3 h |
| **Total** | **22 h** |

At issue time the Orchestrator adds the relevant reserve to the milestone's existing allocation and writes one numeric active-elapsed ceiling in the brief. The net program planning envelope changes from ≈705 h to **≈727 h**; G5 and G6 move by roughly one week while application and ALG gates remain fixed.

## Version and distribution consequence

- Current flagship anchor: `capstone_V6_5.md` v6.4.
- Current stage map: v6.
- The parked DEC-AWS proposal is rebased to **v6.4 → v6.5** and, if ratified, rebuilds map **v6 → v7**.
- `engineering-role.md`, `orchestrator-role.md`, `AGENTS.md`, `CLAUDE.md`, `program-stage-sequence.md`, `progress.md`, `README.md`, and the canonical Hebrew guide are updated in the same authoring pass.
- Operational templates never hardcode a future version; each brief supplies the exact ratified anchor.

*End of v6.3 → v6.4 amendment record.*
