# CP-2 Label-Blind Four-Catalog Protocol

Read this file **only** when CP-2 is the authorized checkpoint. It is the complete, self-contained protocol extracted from `engineering-role.md`, `orchestrator-role.md`, and `docs/track-b/gauntlet-templates.md` so that those documents stay short at every other checkpoint. Nothing here is weakened by the move: the ratified scientific contract remains capstone §4.1 and the machine contract remains `docs/track-b/schemas/cp2-blind-four-catalog.schema.json`.

## 1. Engineering-Lead execution protocol


This protocol is mandatory at CP-2 and uses anonymous labels `A/B/C/D`; it is not generic Blind A/B. The scientific metric/eligibility/tie-break contract is the exact §4.1 text in the ratified capstone. The machine contract is `docs/track-b/schemas/cp2-blind-four-catalog.schema.json`, and the only valid transitions are `blind-prepare`, `blind-recompute`, `blind-freeze`, `blind-reveal`, and `blind-adjudicate` in `scripts/gauntlet_protocol.py`.

Before preparation, finish and commit the final candidate. It must contain two identity-bearing, hash-bound artifacts at fixed paths: `artifacts/cp2/blind/source-manifest.json` (real IDs `strict_base`, `residual_arm`, `scarcity_arm`, `both_arms`; frozen source paths/hashes; matched fold/row/nine-quantile schema; data/cutoff and rule identity) and `artifacts/cp2/blind/selection-declaration.json` (the Lead-computed real winner and its rule inputs). The Blind Critic must never receive or read either artifact or the identity-bearing prediction sources.

Execute one attempt in this order:

1. Allocate a new blind-review ID and Blind component run/piece/ref/support root, bound to the exact final SHA/tree; do not allocate Integration yet. `blind-prepare` draws a fresh cryptographically random 256-bit secret seed/nonce and permutation to `A/B/C/D`. It creates, without overwrite, `<repo>/.gauntlet/evidence/CP-2/_blind-custody/<blind-review-id>/` at mode `0700` with create-only `0600` files. Mapping, seed/nonce, source identities and the tool-generated identity-bearing `preparation-invocation.json` stay there. Any harness-level preparation log remains Lead-private and outside the Blind allowlist. The Blind component support root receives only anonymous interleaved `blind-public-input.csv`, identity-free `blind-public-manifest.json`, `blind-commitment.json` and `blind-preparation-receipt.json`. The commitment binds the hidden mapping and seed/nonce plus candidate/source/rule hashes **and the exact preparation-invocation hash**, so a rewritten invocation or the mere 24 possible mappings cannot open it. The safe public receipt is created strictly after the private custody record and binds that record's exact SHA-256 without exposing its contents; this makes later custody-record rewriting mechanically detectable from the frozen receipt.
2. Launch the fresh Blind Critic with a real read allowlist/sandbox when available. Its allowed inputs are that anonymous public input/manifest/commitment/receipt, the controlling §4.1 metric text and allowlisted recomputation code. Its denied surface includes custody, identity source manifest/files, selection declaration, reveal artifacts, the preparation-invocation record or harness logs and any Git/object-store route to them. It runs `blind-recompute` under the canonical Decimal/CSV schema and writes `blind-metrics.json` by `A/B/C/D` into its owned support root. Raw quantile crossing is accepted as submitted; inclusive q10≤y≤q90 coverage uses the submitted heads, with no M2 CQR/isotonic repair. The Critic verifies arithmetic/completeness and returns `PASS` or `FAIL`; it never identifies base, applies eligibility/tie-breaks, selects a label, or asserts the winner. Its verdict sets `blind_review.identity_decision` exactly to `NOT_PERFORMED`. Before that verdict is accepted, the validator scans every support filename and raw byte stream—including invalid UTF-8—and every string in the verdict for semantic catalog identities or the forbidden identity-input paths.
3. Complete post-review snapshot verification and validate the Blind verdict. Only after a schema-valid Blind `PASS`, invoke `blind-freeze` with a fresh Integration run ID and piece ID at the same final SHA/tree. This command is the **sole allocator** of that Integration run/ref/support identity: it first validates the Blind `PASS`, then mechanically gates fresh run/support initialization and non-moving ref creation, records `allocated_at_utc`, and rejects any pre-existing/preallocated run, support root, or ref. It then creates non-overwriting `blind-freeze.json` plus the single-link Integration-owned `frozen-blind-public-input.csv`, `frozen-blind-public-manifest.json`, `frozen-blind-commitment.json`, `frozen-blind-preparation-receipt.json` and `frozen-blind-metrics.json`, binding their exact bytes together with the Blind run/ref, final SHA/tree, schema, safe recomputation command and verdict hashes/times. The frozen `blind_component` object must exactly reproduce the revalidated verdict's run, piece, ref, verdict path/hash, integrity-manifest path/hash and record time; substituting another hash-valid file is invalid. A `FAIL` is preserved and restarted without reveal or an abandoned Integration run.
4. Only after freeze, run `blind-reveal`. It reads but never mutates custody, requires the exact canonical custody paths/file set/modes, validates invocation→public manifest→commitment→custody→receipt chronology, verifies the committed preparation-invocation hash, verifies the custody record against the frozen receipt's `custody_record_sha256`, compares every custody source role/repository path/hash with both the committed source manifest and hidden mapping preimage, and verifies all frozen hashes. It then copies—never hard-links—`blind-reveal.json`, `revealed-mapping.json`, all four `revealed-source-<semantic-role>.csv` files, `revealed-source-manifest.json`, `revealed-selection-declaration.json` and `revealed-preparation-record.json` into the Integration support root. Every copy is hash-bound and single-link. Never place reveal material in Blind support or return it to that Critic.
5. Launch fresh Integration at the same final SHA/tree. It runs `blind-adjudicate` only against the Integration-owned revealed copies and frozen anonymous metrics, never custody. It maps metrics to the real catalog IDs, applies the §4.1 exact 1%/2 pp/strict-4-of-5 eligibility and 0.1%/feature-count/calibration/fixed-order tie rules, validates the complete custody→commitment→metrics→freeze→reveal chronology, and compares the adjudicated winner with the committed selection declaration. `blind-adjudication.json` and command evidence live only in Integration's owned support root; the Integration run root still contains exactly the two canonical files.

Every custody/public/metrics/freeze/reveal/adjudication record is create-only. No reveal is legal before freeze. Any candidate SHA/tree, source/hash, §4.1 rule/canonicalization or committed selection change; Blind `FAIL`; premature exposure; tamper; reused ID/path/record; or Integration winner mismatch invalidates the whole attempt. Preserve it, then allocate a new blind ID, Blind and Integration run IDs/refs/support roots, seed/nonce, permutation, custody, Critic, freeze, reveal and adjudication. Never reuse a revealed map.

Be candid about the threat boundary. `0700/0600`, prompts and hashes prove state and chronology, not that another process under the same Unix UID did not observe a file. Claim `ENFORCED_READ_ISOLATION` only when the harness actually enforces the deny surface above. A detached checkout with unrestricted reads is insufficient. Otherwise record `COOPERATIVE_PROCEDURAL` label-blinding in the Return Packet and never describe it as cryptographically enforced. CP-2 terminal `PASS` requires the Blind component `PASS`, valid freeze/reveal/adjudication chain, and fresh Integration `PASS`; the packet lists every attempt, reset reason, path, hash, UTC transition and threat-boundary label.

Canonical command entry points:

```text
python3 scripts/gauntlet_protocol.py blind-prepare --repo-root <ABS_REPO> --candidate-sha <FULL_SHA> --blind-review-id <ID> --component-run-id <RUN>
python3 scripts/gauntlet_protocol.py blind-recompute --support-root <ABS_BLIND_SUPPORT> --blind-review-id <ID>
python3 scripts/gauntlet_protocol.py blind-freeze --repo-root <ABS_REPO> --blind-review-id <ID> --component-verdict <ABS_CRITIC_VERDICT> --integration-run-id <RUN> --integration-piece <PIECE>
python3 scripts/gauntlet_protocol.py blind-reveal --repo-root <ABS_REPO> --blind-review-id <ID> --integration-run-id <RUN>
python3 scripts/gauntlet_protocol.py blind-adjudicate --integration-support-root <ABS_INTEGRATION_SUPPORT> --blind-review-id <ID>
```

The Blind component verdict carries `blind_review` with exactly the protocol binding `blind_review_id`, `public_manifest {path, sha256}`, `commitment {path, sha256}`, `preparation_receipt {path, sha256}`, `metrics {path, sha256}`, `protocol_schema {repo_relative_path, sha256}`, `recompute_command`, and the exact constant `identity_decision: NOT_PERFORMED`. Exactly one relied-on CP-2 component verdict may carry this field. Binding the receipt makes any paired custody+receipt rewrite after Blind review invalidate the verdict. The CP-2 Integration verdict carries `blind_adjudication` with `blind_review_id`, `freeze {path, sha256}`, `reveal {path, sha256}`, `adjudication {path, sha256}`, `selected_role`, and `selection_declaration {repo_relative_path, sha256}`. A CP-2 terminal `PASS` requires the adjudication record's `match` to be `true`.

## 2. Blind component Critic handoff

### 2.1 Blind component Critic assignment

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

## 3. Freeze and reveal handoffs

### 3.1 Freeze handoff — Lead/tool only

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

### 3.2 Reveal handoff — Lead/tool only

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

## 4. Orchestrator receipt gate

**CP-2 additional receipt gate — mandatory label-blind four-catalog review.** The packet must bind the final candidate's committed identity-bearing `artifacts/cp2/blind/source-manifest.json` and `artifacts/cp2/blind/selection-declaration.json`; anonymous `blind-public-input.csv`, `blind-public-manifest.json`, 256-bit-seeded `blind-commitment.json`, safe `blind-preparation-receipt.json` and independently recomputed Decimal `blind-metrics.json`; and the strict recorded order **Blind component schema-valid `PASS` < `blind-freeze`-owned fresh Integration run/ref initialization < `blind-freeze.json` < reveal**. The receipt must bind the exact private custody-record SHA-256, the Blind verdict must bind that receipt path/hash, and reveal must prove invocation→manifest→commitment→custody→receipt chronology plus exact custody source path/hash equality with the committed source manifest and hidden preimage. It must then bind verified `blind-reveal.json` and safe revealed copies, plus fresh `blind-adjudication.json` applying capstone §4.1 and matching the committed winner. `blind-freeze` is the sole allocator of the supplied fresh Integration run/piece IDs and must reject a pre-existing run, support root or ref; a preallocated Integration identity is not acceptable evidence of this order. Its `blind_component` block must exactly reproduce the revalidated component verdict's run/piece/ref, verdict path/hash, integrity-manifest path/hash and record time; another hash-valid file is not acceptable provenance. The Blind Critic recomputes identity-free metrics only and never chooses or asserts a label or winner. Custody lives at `.gauntlet/evidence/CP-2/_blind-custody/<blind-review-id>/` with `0700/0600` modes and outside the Blind Critic read context; component public evidence and post-freeze Integration evidence remain in their respective owned support roots, while each run root retains exactly two files. The packet lists all paths/hashes/UTC transitions and every preserved failed/restarted attempt. Any reveal before a frozen schema-valid `PASS`, changed SHA/source/rule/selection, `FAIL`, exposure, tamper, reuse or winner mismatch requires a wholly new blind ID, runs/refs, seed/permutation/custody and chain; a revealed map is never reused. Accept `ENFORCED_READ_ISOLATION` only with an actual read allowlist/sandbox excluding custody, identity artifacts, selection declaration, reveal/preparation material and Git/object-store bypasses. Otherwise require the candid label `COOPERATIVE_PROCEDURAL`; `0700/0600` and hashes prove state/chronology, not non-observation by another same-UID process. Missing or contradictory chain evidence invalidates CP-2 `PASS`.

