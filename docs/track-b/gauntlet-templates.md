# Track B Gauntlet — Canonical Templates

These are boundary-contract templates, not a second capstone plan. The ratified plan named in `progress.md` remains normative. Replace every bracketed field; never infer an anchor from the highest version on disk.

## 1. Orchestrator checkpoint brief

```markdown
# Track B Checkpoint Brief — [M#/CP-# or FM#/FCP-#]

Target repository: [absolute path or unambiguous repo name]
Authorized checkpoint: [exactly one checkpoint]
Ratified plan anchor: [exact filename and version from progress.md]
Complete checkpoint checklist: [exact citation to the full named CP/FCP checklist]
Supporting sections: [exact citations needed for this checkpoint]
Total checkpoint active-elapsed ceiling: [numeric hours covering orientation through terminal return]

## Orchestrator-reported expected state
- branch / commit / working-tree expectation
- completed predecessor and artifacts expected to exist
- data snapshot/cutoff expected

Engineering-Lead must verify this state against the repository before relying on it. A material mismatch is returned, not silently reconciled.

## Observable outcome
[The state that must exist when this checkpoint closes.]

## Complete authoritative checkpoint bar
- [every item in the named CP/FCP checklist, with citation]
- [...]

## Task-specific supporting extract
- [supporting-plan citation]: [faithful outcome-level statement]
- [...]

The complete named CP/FCP checklist remains controlling even if either extract accidentally omits an item. A supporting extract may not weaken, strengthen, or replace it.

## Applicable constraints
- [ratified architecture/data/method constraints]
- $0 expected run rate; $65/month policy ceiling
- M3 / 16 GB / CPU-only, unless the named plan says otherwise

## CP-2 mandatory label-blind four-catalog outcome (include only for CP-2)
- Exact metric/eligibility/tie-break authority: [`capstone_V6_4.md` §4.1 exact citation + excerpt]
- Protocol authority: [`capstone_V6_4.md` §12 CP-2 mandatory protocol exact citation + excerpt]
- Final candidate must commit blob-hash-bound `artifacts/cp2/blind/source-manifest.json` and `artifacts/cp2/blind/selection-declaration.json`.
- A fresh Blind Critic must recompute and freeze identity-free `A/B/C/D` metrics without choosing a winner; no mapping reveal is allowed before its schema-valid `PASS` is frozen.
- Fresh Integration must reveal, apply §4.1 identities/eligibility/tie-breaks, validate the chain, and match the committed winner.
- Machine contract/commands: `docs/track-b/schemas/cp2-blind-four-catalog.schema.json`; `blind-prepare`, `blind-recompute`, `blind-freeze`, `blind-reveal`, `blind-adjudicate` in `scripts/gauntlet_protocol.py`.
- Threat-boundary disclosure required: `ENFORCED_READ_ISOLATION` only with a real deny/read allowlist; otherwise `COOPERATIVE_PROCEDURAL`.

## Owner-only actions already authorized
- none / [credential, signup, browser-bound action, payment, publication]

## Stop and return
Run the bounded Gauntlet autonomously under `engineering-role.md`. Return exactly one consolidated Return Packet with PASS, BLOCKED, PLATEAU, or BUDGET_EXHAUSTED. Stop all Track B work before any later checkpoint. Do not plan or begin it.
```

Measure one active elapsed wall clock in UTC. Record raw seconds from `started_at_utc` to terminal return minus only logged, eligible all-context pauses. Parallel contexts overlap and never sum. New owner/credential/authority requirements return `BLOCKED`; they are not open-ended pauses.

Invalid briefs are returned before work begins if they omit the exact anchor or full-checklist citation, authorize more than one repo/checkpoint, or lack a numeric active-elapsed wall-clock ceiling. A brief cannot reduce the checkpoint bar: that requires an owner-ratified capstone/checkpoint amendment, a new exact anchor, and then a replacement brief.

## 2. Active `workbench.md`

Create this file only after a valid checkpoint brief arrives.

```markdown
# Active Track B Workbench — [checkpoint]

Plan anchor:
Checkpoint evidence root (`.gauntlet/evidence/<checkpoint>/`):
Current run support root (`.gauntlet/evidence/<checkpoint>/_support/<run-id>/`):
Candidate branch/full commit SHA/tree:
Checkpoint active-elapsed ceiling:
started_at_utc:
last_updated_at_utc:
Consumed active elapsed: [raw seconds / decimal hours]

## Eligible pause ledger
| paused_at_utc | resumed_at_utc | duration seconds | reason/evidence | all contexts stopped? |
|---|---|---:|---|---|

## Authorized goal and bar
- criterion → evidence required

## Lead-chosen pieces
| Piece | Disjoint owned paths/artifact | Isolated Builder path/state | Lead serial-integration SHA | Fresh Critic state | Largest open gap |
|---|---|---|---|---|---|

## Mandatory independent surfaces in scope
| Surface | Applicable? | Critic evidence/verdict |
|---|---|---|
| Temporal normalization | | |
| Champion/benchmark schema firewall | | |
| A75 climatology fit lineage | | |
| CP-2 label-blind four-catalog metric recomputation and freeze-before-reveal chain | | |
| M3 hand-checkable CQR threshold recomputation | | |

## Mandatory M1 acceptance-oracle pack (when CP-1 is active)
| Oracle | Independent fixture SHA-256 | Independent expected result | Critic commands/evidence/verdict |
|---|---|---|---|
| M1-O1 — misaligned PT15M chunk stitch | | exactly one four-quarter mean; no three-quarter mean | |
| M1-O2 — missing quarter | | no hourly value; explicit incomplete/recovery | |
| M1-O3 — Berlin fall-back hour | | both 02:00 offsets survive as distinct UTC; 25 rows; true duplicate rejected | |
| M1-O4 — A75 fit-lineage poison | | calibration/eval poison is inert; proper-training poison changes fit | |
| M1-O5 — champion/benchmark schema poison | | valid champion passes; A69/A69-derived/actual injection fails closed; benchmark adds only approved A69 fields and rejects actuals | |

## CP-2 label-blind chain (when CP-2 is active)
Blindness strength: ENFORCED_READ_ISOLATION | COOPERATIVE_PROCEDURAL
Committed source manifest / selection declaration paths and blob hashes: `artifacts/cp2/blind/source-manifest.json` / ... ; `artifacts/cp2/blind/selection-declaration.json` / ...
Current blind-review ID / attempt:
Blind component run/piece/ref/support root:
Custody root (private; never expose contents here):
`blind-public-input.csv` / public manifest / commitment hashes:
Blind metrics / verdict / freeze state:
Integration run/piece/ref/support root:
Reveal / adjudication state:
Latest invalidation/reset reason:

## Integration
- exact final candidate commit SHA/tree:
- reproduction commands:
- tool-generated integrity manifest path/hash:
- schema-valid Critic verdict path/hash:
- fresh Integration-Critic verdict:

## Critic runs
| Unique immutable run ID / piece | Component/Integration | Pre-created candidate ref/SHA | Run root / owned support root | Integrity manifest path/hash | Committed schema hash | Schema-valid verdict path/hash/result |
|---|---|---|---|---|---|---|

## Preserved candidate refs
| Local `refs/gauntlet-evidence/...` ref | Exact SHA | Purpose | Verified? |
|---|---|---|---|

## Exact blocker, if terminal
- none / exact owner or authority request
```

The workbench is temporary engineering state, ignored by Git, and never included in a candidate commit or Critic checkout/context. The Orchestrator never reads it and `progress.md` never imports it. At terminal return, archive a renamed final snapshot at checkpoint-evidence-root level, outside every immutable Critic run directory, only if it contains unique evidence; otherwise delete it. Never carry an active root workbench into the next checkpoint.

At M1, the oracle table is mandatory rather than illustrative. A fresh Critic—not the Builder—materializes and hashes every fixture outside the candidate checkout, computes the expected outcome independently, and records exact commands and results. Repository property tests do not substitute for these five verdicts.

For every component or Integration Critic, choose new ref-safe `<critic-run-id>` and `<piece>` values, initialize its run root, and create/verify its candidate ref at the exact current checkpoint `HEAD` **before** launching the review:

```text
python3 scripts/gauntlet_protocol.py init-evidence --repo-root <abs> --checkpoint <id> --run-id <critic-run-id>
python3 scripts/gauntlet_protocol.py create-ref --repo-root <abs> --checkpoint <id> --run-id <critic-run-id> --piece <piece> --candidate-sha <full-current-head-sha>
python3 scripts/gauntlet_protocol.py verify-ref --repo-root <abs> --checkpoint <id> --run-id <critic-run-id> --piece <piece> --candidate-sha <full-current-head-sha>
```

Under one exclusive initialization lock, `init-evidence` creates both `.gauntlet/evidence/<checkpoint>/<critic-run-id>/` and `.gauntlet/evidence/<checkpoint>/_support/<critic-run-id>/` and rolls back an ordinary partial-creation failure. Neither may preexist, be reused, or traverse symlinks; an observed half-pair fails closed rather than being completed or reused. This is lock/rollback/fail-closed pair initialization, not an atomic paired-directory primitive. The run directory eventually contains exactly `integrity-manifest.json` and `critic-verdict.json`. Every file-backed artifact/input, command stdout/stderr and decision-evidence path declared by this verdict must be a regular non-symlink file physically under its exact owned support root, with SHA-256 and inode link count (`st_nlink`) exactly one. A hard-linked inode is invalid: it may not be borrowed or shared across another support root, run, temporary directory, snapshot, or any other path. Use safe hash/lineage manifests instead of raw restricted or impractically large data. Prose-only observations are not evidence. A changed candidate requires a new run ID/piece/ref/support root.

## 3. Builder assignment

```markdown
# Builder assignment — [piece]

Authorized checkpoint:
Lead-created isolated writable detached worktree/snapshot:
Disjoint owned paths/artifact (exact allowlist):
Observable goal:
Concrete acceptance bar:
Relevant ratified rules/citations:
Required tests/reproduction/evidence:
Forbidden scope:
Target wall-clock window within the checkpoint ceiling (Lead-set, non-authoritative):

Implement only this bounded piece and edit only the allowlisted paths. Do not stage, commit, merge, switch branches, update refs, create/remove worktrees, or share a writable Git index with another Builder. Return the changed-path list, artifact/input hashes, exact reproduction commands, evidence, known gaps, and active-elapsed timing to the Engineering Lead. The Lead alone inspects and imports the allowlisted paths, verifies the staged path set, and commits serially on `gauntlet/<checkpoint>`. Do not self-certify the checkpoint or ask a Critic to review an uncommitted diff.
```

## 4. Independent Critic assignment

Use a fresh read-only context and the mandatory isolated protocol in `engineering-role.md`. The Lead first initializes the run plus its uniquely owned `_support/<run-id>/` root and creates/verifies its non-moving candidate evidence ref at the exact current checkpoint `HEAD`. Then create a clean detached checkout at that full candidate SHA outside every Builder tree. `workbench.md`, Builder history, summaries, and uncommitted files must be absent. The unique Critic run root is outside the checkout and reserved for exactly the tool-generated integrity manifest and separate verdict record; every declared file-backed artifact/input/cache/output/fixture/log/evidence path belongs under the exact owned support root, carries SHA-256, and has `st_nlink == 1` so no inode is shared through a hard link.

```text
scripts/gauntlet_critic_snapshot.sh create <full-sha> <outside-snapshot-path> <absolute-manifest-path> <critic-run-id>
scripts/gauntlet_critic_snapshot.sh verify <full-sha> <outside-snapshot-path> <absolute-manifest-path> <pre-review-manifest-sha256>
```

```markdown
# Independent Critic — [piece or mandatory surface]

Authorized checkpoint:
Piece ID: [mandatory ref-safe ID]
Pre-created candidate evidence ref: [`refs/gauntlet-evidence/<checkpoint>/<critic-run-id>/<piece>`]
Full candidate commit SHA:
Full candidate tree:
Candidate artifact path/SHA-256:
`plan.filename` (safe repository-relative committed `.md` path):
`plan.sha256` (exact SHA-256 of that blob's bytes at candidate SHA):
`plan.version` (human-readable version):
`plan.bar_citation` (exact human citation):
`plan.bar_excerpt` (non-empty verbatim text present in that same blob):
Observable goal:
Decision-bearing input/data SHA-256 (or explicit N/A):
Exact reproduction commands:
Expected output/tolerance:
Command stdout/stderr destinations (absolute, outside run root):
Unique immutable Critic run ID: [mandatory ref-safe ID; never reused]
Critic ID: [ref-safe harness context ID when suitable; otherwise assigned]
Critic run root: [absolute `<repo>/.gauntlet/evidence/<checkpoint>/<critic-run-id>/`]
Critic-owned support root: [absolute `<repo>/.gauntlet/evidence/<checkpoint>/_support/<critic-run-id>/`]
Tool-generated integrity manifest path: [absolute `<run-root>/integrity-manifest.json`]
Critic verdict record path: [absolute `<run-root>/critic-verdict.json`]
Canonical verdict schema: [docs/track-b/schemas/critic-verdict.schema.json]
Committed verdict-schema SHA-256: [hash of the schema blob at candidate SHA]

## Before-review integrity
- `git rev-parse --verify HEAD`:
- `git rev-parse --verify 'HEAD^{tree}'`:
- `git diff --quiet`: PASS
- `git diff --cached --quiet`: PASS
- `git status --porcelain=v1 --untracked-files=all --ignored=matching`: EMPTY
- `test ! -e workbench.md`: PASS
- pre-review integrity-manifest SHA-256: [helper create output]

Inspect and rerun independently. Return:
- Verdict: PASS | FAIL
- Bound piece/evidence-ref/candidate SHA/tree, committed schema hash, artifact hash, complete `plan.filename`/`plan.version`/`plan.sha256`/`plan.bar_citation`/`plan.bar_excerpt` binding, and input hashes; prove that the verbatim excerpt occurs in the committed blob
- Exact commands actually executed with exit codes and stdout/stderr absolute paths/SHA-256
- Tool-generated create/verify integrity-manifest path and final SHA-256 from `scripts/gauntlet_critic_snapshot.sh` or equivalent; `verify` receives the recorded pre-review manifest SHA-256
- Separate Critic-verdict path and SHA-256, validated by `python3 scripts/gauntlet_protocol.py validate-verdict --verdict <absolute-path>` against `docs/track-b/schemas/critic-verdict.schema.json`
- Evidence actually inspected/recomputed
- Every file-backed artifact/input/command/evidence path under this run's exact owned support root, with SHA-256, inode link count exactly one, and UTC record time required by the canonical schema; no hard-linked/cross-run/external path or unhashed observation substitutes
- The single largest meaningful gap
- The exact next acceptance test
- Any scope or methodology conflict

Do not edit the checkout or inspect any Builder workspace. Do not author or repair the helper-owned integrity manifest. Repeat every integrity check after review without cleaning/resetting first. `verify` must refuse a missing/mismatched create record or pre-review manifest hash. Write the verdict only after successful verify; its UTC record time cannot precede verify. Any changed SHA/tree/ref, nonempty status, workbench presence, invalid schema, unsafe/mismatched plan path or blob hash, `bar_excerpt` absent from the bound blob, unhashed or hard-linked support evidence, or missing provenance field invalidates the verdict. Do not redesign the project and do not accept claims that are not reproducible from the artifact.
```

Do not describe a comparison as blind merely because labels were renamed. CP-2 must use the mandatory label-blind four-catalog protocol below. On any `FAIL`, Engineering-Lead routes the evidence directly back to a Builder and later launches a fresh critic; Yarden does not relay messages.

### 4.1 CP-2 label-blind four-catalog component Critic

Before this handoff, the final candidate already commits `artifacts/cp2/blind/source-manifest.json` and `artifacts/cp2/blind/selection-declaration.json`. The Lead initializes only the Blind component run/ref/support and private custody; Integration is not allocated unless this component returns schema-valid `PASS`. The tool-generated identity-bearing `preparation-invocation.json` and every identity-bearing source file stay in create-only custody; any harness log remains Lead-private and outside the Blind allowlist. None enters this support root or prompt. The hidden commitment binds the exact preparation-invocation hash, and the later safe public receipt binds the exact private custody-record hash without exposing its contents. The canonical preparation invocation is:

```text
python3 scripts/gauntlet_protocol.py blind-prepare --repo-root <ABS_REPO> --candidate-sha <FULL_SHA> --blind-review-id <ID> --component-run-id <RUN>
```

```markdown
# CP-2 Blind Metric Critic — anonymous A/B/C/D

Authorized checkpoint: CP-2
Blind review ID:
Blind component piece/run ID:
Pre-created candidate evidence ref:
Full final candidate commit SHA/tree:
Blind component run root:
Blind component owned support root:
Tool integrity manifest path and pre-review hash:
Critic verdict path:
General verdict schema path/blob SHA-256:
CP-2 blind schema path/blob SHA-256: [docs/track-b/schemas/cp2-blind-four-catalog.schema.json]
Canonical tool path/blob SHA-256: [scripts/gauntlet_protocol.py]
`plan.filename` / `plan.version` / `plan.sha256`:
Piece-specific `plan.bar_citation` / verbatim `plan.bar_excerpt`:
Anonymous interleaved CSV path/SHA-256: [<ABS_BLIND_SUPPORT>/blind-public-input.csv]
Identity-free public manifest path/SHA-256: [<ABS_BLIND_SUPPORT>/blind-public-manifest.json]
Mapping commitment path/SHA-256: [<ABS_BLIND_SUPPORT>/blind-commitment.json]
Safe identity-free preparation receipt path/SHA-256: [<ABS_BLIND_SUPPORT>/blind-preparation-receipt.json]
Read-isolation class: ENFORCED_READ_ISOLATION | COOPERATIVE_PROCEDURAL
Enforced allowlist/deny mechanism or candid limitation:

Allowed inputs are only `blind-public-input.csv`/public manifest/commitment/safe
receipt, the exact §4.1 metric text, the two schemas, and allowlisted recomputation
code. Do not read custody, identity-bearing source manifest/files, committed
selection declaration, reveal artifacts, the preparation-invocation record or
any harness log, Builder
material, or any Git/object-store route to those identities. A detached checkout
with unrestricted reads does not support an enforced-blindness claim.

Run the following command independently:

`python3 scripts/gauntlet_protocol.py blind-recompute --support-root <ABS_BLIND_SUPPORT> --blind-review-id <ID>`

Validate the exact public header
`label,fold_id,row_id,y,q025,q05,q10,q25,q50,q75,q90,q95,q975`, canonical
UTF-8/LF rows in sort `(fold_id numeric, row_id UTF-8 byte order, label A→D)`,
opaque `row_id` values matching `^r[0-9]{6,}$`, matched rows/folds, all nine raw
quantiles, finite base-10 Decimal inputs and deterministic output. A `row_id`
contains no timestamp or catalog identity; do not receive or consult any timestamp/
identity lookup, which remains outside the Blind context.
Compute observation-weighted pooled/fold pinball and inclusive submitted
q10≤y≤q90 coverage exactly. Raw crossing is allowed: do not repair, reject,
isotonize or calibrate it at M2.

Return PASS only for complete, schema-valid identity-free arithmetic. Write
metrics by A/B/C/D in `blind-metrics.json` and bind them in the verdict's `blind_review`. Never infer
which label is base, apply eligibility or tie-breaks, select a label, or state a
winner. Complete snapshot verify and general verdict validation, then stop.
Do not reveal or request the mapping.

Before accepting the verdict, run the authoritative validator so that every
support filename and raw byte stream—including invalid UTF-8—and every string
anywhere in the verdict is rejected if it contains a semantic catalog identity
or forbidden identity-input path.
```

The `blind_review` object must bind `blind_review_id`, `public_manifest {path, sha256}`, `commitment {path, sha256}`, `preparation_receipt {path, sha256}`, `metrics {path, sha256}`, `protocol_schema {repo_relative_path, sha256}`, `recompute_command`, and the exact constant `identity_decision: NOT_PERFORMED`. Exactly one relied-on component verdict may carry it. A paired custody+receipt rewrite after review must therefore make that verdict stale.

Blind component support contains only `blind-public-input.csv`, `blind-public-manifest.json`, `blind-commitment.json`, `blind-preparation-receipt.json`, `blind-metrics.json`, and its safe recomputation command/evidence files. Its run root remains exactly the two canonical records. `0700/0600` custody is outside the Critic read context and is not evidence of adversarial secrecy from another same-UID process.

## 5. CP-2 freeze and reveal handoffs

### 5.1 Freeze handoff — Lead/tool only

```markdown
# CP-2 Freeze Authorization

Blind review ID:
Exact final candidate SHA/tree:
Schema-valid Blind PASS verdict path/SHA-256:
Blind integrity manifest path/SHA-256:
Blind run/piece/ref:
`blind-public-input.csv` / public manifest / commitment / metrics paths and hashes:

Supply fresh Integration run and piece IDs but do not initialize either identity.
`blind-freeze` is the sole allocator: it verifies the Blind verdict/ref first,
rejects every pre-existing run/support/ref, and only if the verdict is schema-valid
PASS initializes the fresh Integration run/support and creates its ref at the same
final SHA/tree. It then writes the create-only freeze plus the five
Integration-owned single-link copies `frozen-blind-public-input.csv`,
`frozen-blind-public-manifest.json`, `frozen-blind-commitment.json`,
`frozen-blind-preparation-receipt.json`, and `frozen-blind-metrics.json` into that
Integration support root. Its `blind_component` object must exactly reproduce the
revalidated verdict's run, piece, ref, verdict path/hash, integrity-manifest
path/hash and record time; another hash-valid file is not a substitute. Bind all
listed hashes and UTC chronology. On FAIL, mismatch,
preexisting output or tamper, do not reveal; preserve every allocated or partial
attempt and restart with wholly new IDs and custody.

Canonical invocation:
`python3 scripts/gauntlet_protocol.py blind-freeze --repo-root <ABS_REPO> --blind-review-id <ID> --component-verdict <ABS_CRITIC_VERDICT> --integration-run-id <RUN> --integration-piece <PIECE>`
```

### 5.2 Reveal handoff — Lead/tool only

```markdown
# CP-2 Reveal Authorization

Blind review ID:
Integration run/piece/ref/support:
Freeze path/SHA-256/time:
Private custody-record path/SHA-256, receipt-bound SHA-256, and directory/file modes:

Run `blind-reveal` only after revalidating the frozen PASS and unchanged hashes.
Read but never mutate custody. Verify invocation→public manifest→commitment→custody→receipt
chronology, the 256-bit-seeded commitment, and that the frozen receipt's
`custody_record_sha256` matches the exact private custody record. Compare every
custody source role/repository path/hash with both the committed source manifest
and the hidden mapping preimage. Copy—never
hard-link—the mapping, all four identity-bearing canonical source prediction
CSVs, source manifest, committed selection declaration, and safe post-reveal
preparation record into Integration's owned support root. Create the reveal once;
record every path/hash/time. Never write reveal material to Blind support or
return it to the Blind Critic. Stop before adjudication.

Canonical invocation:
`python3 scripts/gauntlet_protocol.py blind-reveal --repo-root <ABS_REPO> --blind-review-id <ID> --integration-run-id <RUN>`
```

Every public/custody/metrics/freeze/reveal/adjudication record is create-only. A changed candidate/source/rule/selection, Blind `FAIL`, premature exposure, tamper, reuse or later winner mismatch preserves the old attempt but forces a new blind ID, Blind and Integration runs/refs, 256-bit seed/permutation/custody and complete chain. Never reuse a revealed mapping.

## 6. Fresh Integration Critic

```markdown
# Fresh Integration Critic — [checkpoint]

Authorized checkpoint:
Full final candidate commit SHA:
Full final candidate tree:
Final candidate artifact path/SHA-256:
`plan.filename` (safe repository-relative committed `.md` path):
`plan.sha256` (exact SHA-256 of that blob's bytes at final candidate SHA):
`plan.version` (human-readable version):
`plan.bar_citation` (complete checkpoint citation):
`plan.bar_excerpt` (non-empty verbatim text present in that same blob):
Decision-bearing input/data SHA-256 (or explicit N/A):
Clean reproduction commands:
Expected output/tolerances:
Data snapshot/cutoff/hash:
Component and mandatory-surface schema-valid verdict paths/hashes:
Component tool-generated integrity-manifest paths/hashes:
Canonical verdict schema: [docs/track-b/schemas/critic-verdict.schema.json]
Fresh detached checkout before-review integrity evidence:

## CP-2 revealed chain inputs (mandatory only for CP-2)
Blind review ID:
Blindness strength + enforced mechanism/candid limitation:
CP-2 blind schema path/blob SHA-256 and tool blob SHA-256:
Committed identity source-manifest repo path/blob SHA-256: `artifacts/cp2/blind/source-manifest.json` / ...
Committed selection-declaration repo path/blob SHA-256/declared winner: `artifacts/cp2/blind/selection-declaration.json` / ...
Blind component run/piece/ref and manifest/verdict paths/hashes:
Anonymous `blind-public-input.csv`/public-manifest/commitment/metrics paths/hashes:
Freeze path/hash/time:
Reveal path/hash/time:
Integration-owned copied mapping path/hash:
Integration-owned four real source CSV paths/hashes:
Integration-owned copied source manifest path/hash:
Integration-owned copied selection declaration path/hash:
Safe post-reveal preparation record path/hash:
Adjudication/chain-validation destination:

From this fresh read-only context, verify:
1. every item in the complete named CP/FCP checklist against direct evidence;
2. all current independent verdicts and mandatory surfaces;
3. every component `PASS` used for terminal `PASS` binds its declared piece, pre-created evidence ref, the exact final candidate SHA/tree, the same checkpoint and plan identity (`plan.filename`, `plan.version`, and `plan.sha256`) as Integration, the committed schema, and current input hashes; each component and Integration verdict retains its own piece-appropriate `plan.bar_citation` and `plan.bar_excerpt`, and each excerpt is independently proven verbatim in that same committed blob; any candidate change invalidates all earlier component `PASS` verdicts, so rerun all required component Critics with new run IDs/refs rather than selectively reusing by path;
4. cross-component contracts and hard invariants;
5. metrics recomputed from frozen predictions where applicable;
6. clean-environment reproducibility and documentation consistency;
7. absence of unauthorized later-checkpoint work.

For CP-2 also run
`python3 scripts/gauntlet_protocol.py blind-adjudicate --integration-support-root <ABS_INTEGRATION_SUPPORT> --blind-review-id <ID>`
only against Integration-owned copies and
the frozen anonymous metrics—never custody. Verify the commitment's 256-bit-secret
preimage, the frozen receipt-to-custody-record hash binding, exact custody-source
path/hash equality with the committed manifest/preimage, create-only chronology,
exact Blind verdict/integrity provenance, Blind PASS freeze strictly before reveal,
candidate/source/rule/selection hashes, and that no old ID/map/record was reused.
Apply the exact §4.1 identities `strict_base | residual_arm | scarcity_arm |
both_arms`, observation-weighted nine-quantile Decimal metrics, inclusive raw
q10≤y≤q90 coverage, exact eligibility boundaries and deterministic tie-break.
Raw crossing remains unmodified. Verify that the adjudicated real winner equals
the committed selection declaration. Bind the resulting adjudication record in
the Integration verdict's `blind_adjudication`. A mismatch is FAIL; after any
needed candidate repair, the entire Blind/freeze/reveal/Integration chain uses
new IDs, refs, seed/permutation and custody even if candidate bytes are unchanged.

Also verify that every revealed identity-bearing source CSV has exact header
`fold_id,row_id,y,q025,q05,q10,q25,q50,q75,q90,q95,q975`, canonical sort
`(fold_id numeric, row_id UTF-8 byte order)`, and the same opaque
`^r[0-9]{6,}$` row universe as the anonymous input. Timestamp/identity lookup
evidence is post-reveal Integration material and never Blind input.

Repeat the full integrity check after review without cleanup. Return PASS or FAIL in a separate schema-valid Integration verdict record with the same mandatory SHA/tree/bar/input/command/integrity provenance, evidence inspected, the single largest gap, and the exact next acceptance test. Do not redesign.
```

For CP-2, `blind_adjudication` must bind `blind_review_id`, `freeze {path, sha256}`, `reveal {path, sha256}`, `adjudication {path, sha256}`, `selected_role`, and `selection_declaration {repo_relative_path, sha256}`. Terminal `PASS` requires the adjudication record's `match` to be `true`.

## 7. Consolidated Return Packet

Candidate refs were created before their reviews. Before returning, reverify every cited commit/ref with the associated immutable evidence run ID:

```text
python3 scripts/gauntlet_protocol.py verify-ref --repo-root <abs> --checkpoint <id> --run-id <id> --piece <id> --candidate-sha <full-sha>
```

```markdown
# Track B Checkpoint Return — [M#/CP-#]

Status: PASS | BLOCKED | PLATEAU | BUDGET_EXHAUSTED
Target repository:
Ratified plan anchor:
Checkpoint evidence root:
Exact final candidate commit/tree/branch:
Working-tree state:
Data snapshot/cutoff/hash:
Checkpoint active-elapsed ceiling:
started_at_utc / terminal_at_utc:
Eligible pause ledger (UTC, reason/evidence, all contexts stopped):
Consumed active elapsed: [raw seconds / decimal hours]
Integration verdict and evidence: PASS | FAIL | NOT_RUN — [evidence or exact reason]
Integration integrity manifest (tool-generated path/SHA-256):
Integration Critic verdict record (schema-valid path/SHA-256):

## Critic run inventory
| Unique immutable run ID / piece | Component/Integration | Pre-created candidate ref/SHA | Run root / owned support root | Integrity manifest path/hash | Committed schema hash | Schema-valid verdict path/hash/result |
|---|---|---|---|---|---|---|

## CP-2 label-blind four-catalog chain (mandatory only for CP-2)
Blindness strength: ENFORCED_READ_ISOLATION | COOPERATIVE_PROCEDURAL
Enforced read mechanism or candid same-UID limitation:
Committed source manifest path/blob SHA-256: `artifacts/cp2/blind/source-manifest.json` / ...
Committed selection declaration path/blob SHA-256/declared winner: `artifacts/cp2/blind/selection-declaration.json` / ...
CP-2 blind schema path/blob SHA-256 and tool path/blob SHA-256:

| Attempt / blind-review ID | Final SHA/tree | Blind run/piece/ref/support | Custody-record path/SHA-256 + receipt-bound SHA/modes | `blind-public-input.csv` / manifest / commitment / receipt hashes | Metrics path/hash + Blind verdict | Integration run/piece/ref/support | Freeze path/hash/time | Reveal + Integration-owned copy paths/hashes/time | Adjudication path/hash/winner | Result/reset reason |
|---|---|---|---|---|---|---|---|---|---|---|---|

Chronology check: prepare < Blind metrics < Blind verify/verdict PASS < Integration init/ref < freeze < reveal < adjudication < Integration verify/verdict.
Mapping reuse check: PASS | FAIL
Blind Critic did not choose or assert any winner: PASS | FAIL

## Preserved candidate refs
| Local evidence ref (`scripts/gauntlet_protocol.py create-ref/verify-ref`) | Exact commit SHA | Purpose | Verified reachable? |
|---|---|---|---|

## Complete named CP/FCP checklist
| Criterion citation | PASS/OPEN | Direct evidence/reproduction |
|---|---|---|

## Independent criticism
| Piece/surface | Critic/run ID | Candidate SHA/tree (must equal final for relied-on PASS) | Artifact/input hashes | Plan filename/blob hash/version/citation + verbatim excerpt | Exact commands/tolerances | Integrity manifest path/hash | Schema-valid verdict path/hash/result | Largest gap and disposition |
|---|---|---|---|---|---|---|---|---|

## Engineering decisions
- decision and rationale
- rejected alternatives and why
- largest failure uncovered by the Gauntlet and how it was repaired

## Reproduction
- exact commands
- artifacts
- metrics/screenshots where applicable

## Open risks or exact owner action
- none / exact request

## Defense questions
1. [3–5 questions grounded in actual architecture, tradeoffs, and evidence]

Track B has stopped. No later-checkpoint work has begun.
```

## 8. Orchestrator receipt and gate

The Orchestrator checks that the packet names the authorized repo/checkpoint/anchor, maps **every item in the full named CP/FCP checklist** to direct evidence, includes all applicable independent surfaces and M1 oracles, and does not hide an open item behind `PASS`. Every required component, oracle, and Integration review must have a unique immutable Critic run root containing exactly its separate tool-generated integrity manifest and schema-valid Critic verdict record plus its uniquely owned `_support/<run-id>/` root, with their paths/hashes, piece ID, pre-created candidate ref, committed schema hash, full candidate SHA/tree and artifact/input hashes, exact commands/tolerances, exit codes, stdout/stderr hashes, and hashed evidence. Each verdict must bind the controlling committed plan through safe repository-relative `.md` `plan.filename`, exact committed-blob `plan.sha256`, human `plan.version` and `plan.bar_citation`, and a verbatim `plan.bar_excerpt` that occurs in that same blob. Every file-backed verdict path must be physically inside that exact support root, have SHA-256, and have inode link count exactly one; a hard-linked or borrowed inode is invalid. For terminal `PASS`, every relied-on component `PASS` must bind the exact final candidate SHA/tree and checkpoint and share Integration's plan identity (`plan.filename`, `plan.version`, and `plan.sha256`). Its `plan.bar_citation` and `plan.bar_excerpt` remain piece-specific; the excerpt, not the human citation string, is independently proven verbatim in that same blob, and the pair need not equal Integration's checkpoint-wide citation/excerpt. Any candidate change invalidates all earlier component `PASS` verdicts and requires all required component Critics to rerun with new run IDs/refs. The packet must also enumerate and reverify every non-moving local `refs/gauntlet-evidence/...` ref. A missing field/ref, reused/mutable run/support root, invalid schema, unsafe/mismatched plan identity, piece-inappropriate citation, non-verbatim excerpt, cross-run/external/unhashed/hard-linked evidence, dirty checkout, changed SHA/tree, or review of uncommitted work invalidates that verdict and therefore invalidates `PASS`. A supported `PASS` requires a current fresh Integration-Critic `PASS`. For a non-`PASS` return, `NOT_RUN` is acceptable only with the exact terminal reason—`BLOCKED`, `PLATEAU`, or `BUDGET_EXHAUSTED`—that prevented integration; it never implies a pass.

For CP-2, also reject `PASS` unless the dedicated table proves one terminal **label-blind four-catalog review** chain: final committed `artifacts/cp2/blind/source-manifest.json` and `artifacts/cp2/blind/selection-declaration.json`; anonymous `blind-public-input.csv`/`blind-public-manifest.json`/`blind-commitment.json` plus a safe receipt binding the exact private custody-record hash; Blind identity-free `blind-metrics.json` and schema-valid component `PASS` with `identity_decision: NOT_PERFORMED` and no winner assertion; fresh Integration allocation only after that PASS; `blind-freeze.json` whose component provenance exactly reproduces that validated verdict/integrity pair, plus its five Integration-owned frozen copies before `blind-reveal.json`; copied (never hard-linked) revealed mapping, all four real source CSVs, source manifest and selection declaration inside Integration's support root; `blind-adjudication.json` chain validation and winner equality; and fresh Integration `PASS` with `blind_adjudication`. All artifacts are create-only, all attempts and resets are preserved, invocation→manifest→commitment→custody→receipt and PASS→allocation→freeze→reveal chronology/hashes match, and no revealed mapping is reused. `ENFORCED_READ_ISOLATION` requires an actual read sandbox/allowlist excluding custody, identities, selection, reveal/preparation material or harness logs and Git/object-store bypass; otherwise the only honest label is `COOPERATIVE_PROCEDURAL`. Modes and hashes do not prove non-observation by another same-UID process.

- Supported `PASS`: close only that checkpoint in `progress.md`, summarize its evidence, then ask Yarden explicitly whether to authorize the next stage.
- `BLOCKED`: request only the exact owner action, authority, or plan/reality resolution named by the packet.
- `PLATEAU`: decide whether the remaining improvement is worth a new bounded brief; never relabel it `PASS`.
- `BUDGET_EXHAUSTED`: decide whether to issue a replacement brief with a numeric extension. A reduced bar first requires an owner-ratified capstone/checkpoint amendment and new exact anchor; the Lead cannot extend or reduce scope itself.

No terminal status automatically opens the next checkpoint.
