# Track B Gauntlet — Rule Inventory (Phase 1 prune, 2026-08-05)

**Purpose.** Enumerate every normative rule in the four prose documents before the prune, so the
post-prune state can be proved complete rather than asserted complete. This is a working artifact
for the prune, **not** agent context — it is never loaded into a Builder or Critic.

**Sources inventoried (complete read):**
`capstone_V6_5.md` §12 (L393–L425) · `engineering-role.md` (241 lines) ·
`docs/track-b/gauntlet-templates.md` (405 lines) · `docs/track-b/cp2-blind-protocol.md` (173 lines)

**Post-prune ownership:** `CAP` = `capstone_V6_5.md` §12 (the bar) · `ROLE` = `engineering-role.md`
(the process) · `TMPL` = `gauntlet-templates.md` (forms only) · `CP2` = `cp2-blind-protocol.md`
(CP-2 only) · `PROG` = `progress.md` (program state).

**Count: 148 normative rules. Target after prune: 148.**

---

## Defects surfaced by the inventory itself

These are not prune decisions — they are live inconsistencies found while enumerating.

| # | Defect | Evidence |
|---|---|---|
| **D-1** | **The rerun-all rule survives in three more places** than the 2026-08-04 fix caught. All three contradict E5. | `engineering-role.md:40` "all bound to the exact final candidate SHA/tree"; `engineering-role.md:196` and `gauntlet-templates.md:372` table header "(must equal final for relied-on PASS)" |
| **D-2** | **Reserve table omits CP-0.** Capstone says 22 h; progress.md says 24 h incl. CP-0's 2 h. | `capstone_V6_5.md:425` vs `progress.md:36` |
| **D-3** | **Stale CP-2 protocol citation.** Brief template cites §12 as protocol authority; after the prune the protocol lives only in `CP2`. | `gauntlet-templates.md:44` |

D-1 is the same class as the defect we repaired yesterday, and it is why the inventory runs first.

---

## A — Authority and brief validity (10)

| ID | Rule | Currently in | → |
|---|---|---|---|
| A1 | Orchestrator alone decides when Track B runs, which single checkpoint is authorized, and the numeric ceiling | CAP L403 · ROLE 5, 28 | ROLE |
| A2 | Lead decides how: implementation, decomposition, parallelism, agent count, internal windows | CAP L403, L405 · ROLE 28, 34 | ROLE |
| A3 | Yarden carries one brief in and one packet back; never routes Builder/Critic messages | CAP L403 · ROLE 37 · TMPL 235 | ROLE |
| A4 | Engineering source of truth is the exact ratified plan named in the active brief; never the highest-numbered file on disk | ROLE 7 · TMPL 3 | ROLE |
| A5 | Brief must name: repo · one checkpoint · exact anchor · expected state · observable goal · complete CP/FCP checklist citation · supporting extract · constraints · numeric ceiling · owner-only actions · stop-and-return | CAP L399 · ROLE 15–26 · TMPL 8–56 | ROLE (rule) + TMPL (form) |
| A6 | Missing anchor, full-checklist citation, or numeric ceiling, or >1 repo/checkpoint ⇒ invalid brief, returned before work | CAP L399 · ROLE 7 · TMPL 60 | ROLE |
| A7 | A supporting extract cannot narrow, weaken, strengthen, or replace the complete checklist | CAP L395 · ROLE 7, 40 · TMPL 35 | CAP |
| A8 | A brief cannot reduce the bar; that needs owner-ratified amendment + new anchor + replacement brief | ROLE 103 · TMPL 60, 403 | CAP |
| A9 | Co-located orchestration docs are not engineering context; don't read `orchestrator-role.md`, `progress.md`, syllabus, or Track A/C during execution | ROLE 9 | ROLE |
| A10 | A standalone advisory brief cannot open or close a checkpoint; "execute the capstone" without a brief authorizes nothing | ROLE 11 | ROLE |

## B — Execution loop (10)

| ID | Rule | Currently in | → |
|---|---|---|---|
| B1 | Verify real repo state; never trust the expected-state paragraph; report material mismatch | ROLE 32 · TMPL 22 | ROLE |
| B2 | Plan aloud before editing, 2–3 paragraphs — engineering reasoning for Yarden, not a competing spec | ROLE 33 | ROLE |
| B3 | Choose the smallest important pieces that can be built and judged independently | ROLE 34 | ROLE |
| B4 | Builder receives observable goal, concrete bar, relevant ratified rules, disjoint owned paths, required evidence; works in a Lead-created isolated writable detached worktree; edits only allowlisted paths | CAP L405 · ROLE 35 · TMPL 155–167 | ROLE |
| B5 | Builders never stage, commit, merge, switch branches, update refs, or share a writable Git index | CAP L405 · ROLE 35 · TMPL 167 | ROLE |
| B6 | Parallelize only disjoint ownership | CAP L405 · ROLE 35 | ROLE |
| B7 | Lead is sole Git writer: imports exact allowlisted paths, verifies staged set equals allowlist, commits serially on local disposable `gauntlet/<checkpoint>` — never `main`, never pushed | CAP L405 · ROLE 36 · TMPL 167 | ROLE |
| B8 | Builder never grades its own work, self-certifies, or closes a CP item | CAP L405 · ROLE 40 · TMPL 167 | **CAP** (bar) + ROLE |
| B9 | FAIL routes internally to the Builder and reruns the independent check; no arbitrary round count | CAP L405, L407 · ROLE 37 · TMPL 235 | ROLE |
| B10 | Continue while a meaningful gap remains and the ceiling permits | ROLE 37 | ROLE |

## C — Critic isolation (13)

| ID | Rule | Currently in | → |
|---|---|---|---|
| C1 | Critic receives unique ref-safe run ID + piece ID, full candidate SHA/tree, pre-created evidence ref, exact committed-plan binding, input hashes (or explicit N/A), reproduction commands, expected output/tolerance | CAP L405 · ROLE 46 · TMPL 182–209 | ROLE |
| C2 | `plan.filename` safe repo-relative `.md`; `plan.sha256` = blob bytes at candidate SHA; `plan.bar_excerpt` non-empty and verbatim in that blob. Absolute path, `..`, non-Markdown, working-tree file, mismatched hash, or absent excerpt invalidates | CAP L405, L407 · ROLE 46 · TMPL 188–192, 222 | ROLE |
| C3 | Critic works only from a newly created clean detached worktree at that SHA outside the Builder checkout (or immutable snapshot with equivalent provenance); reviewing an uncommitted diff is invalid | CAP L405 · ROLE 47 · TMPL 172 | ROLE |
| C4 | Critic never receives the Builder checkout, uncommitted diff, reasoning, summary, history, or `workbench.md` | CAP L405, L409 · ROLE 36, 47 · TMPL 172 | ROLE |
| C5 | Tool-generated integrity manifest created in the run root **before** review, recording create event, `HEAD`, `HEAD^{tree}`, empty status, absence of root `workbench.md`, checkout path, run ID, tool version, UTC. Helper owns it | CAP L405 · ROLE 48 · TMPL 206, 218 | ROLE |
| C6 | Preserve the pre-review manifest SHA-256 as an input to `verify` | ROLE 48–49 · TMPL 218, 224 | ROLE |
| C7 | Mandatory cache routing before any command (`PYTHONDONTWRITEBYTECODE`, `PYTHONPYCACHEPREFIX`, every tool writing beside its input). A verify failing on an ignored byproduct is a procedure error that still invalidates; remedy is a fresh run, never cleaning | ROLE 48 · TMPL 197–200 | ROLE |
| C8 | Repeat integrity checks after running **without** cleaning/resetting/restoring; before/after SHA and tree must match and status stay empty | ROLE 49 · TMPL 232 | ROLE |
| C9 | `verify` refuses on missing create record, mismatched pre-review manifest SHA, or mismatched recorded SHA/tree/path/run ID | ROLE 49 · TMPL 232 | ROLE |
| C10 | Any mismatch invalidates the review and requires a new clean checkout and fresh Critic | CAP L405 · ROLE 49 | ROLE |
| C11 | Critic never authors or repairs the integrity manifest; a valid manifest alone is not a verdict | ROLE 50 · TMPL 232 | ROLE |
| C12 | Critic is read-only: no editing the checkout, no inspecting Builder workspaces, no redesign | ROLE 39 · TMPL 232 | ROLE |
| C13 | Verdict written only after successful `verify`; its UTC record time cannot precede verify | ROLE 50 · TMPL 232 | ROLE |

## D — Verdict record (7)

| ID | Rule | Currently in | → |
|---|---|---|---|
| D1 | Verdict contains PASS/FAIL, run/piece/Critic IDs, candidate SHA/tree, evidence ref, schema path+hash, artifact path/hash or N/A, complete plan binding, input paths/hashes, exact commands with exit codes and stdout/stderr paths/hashes, expected output/tolerance, final manifest path/SHA, hashed evidence, largest gap, next acceptance test, UTC time | CAP L405 · ROLE 50 · TMPL 220–230 | ROLE |
| D2 | Integration record also binds every relied-on component verdict path/hash/piece and its candidate SHA/tree | CAP L407 · ROLE 50 | ROLE |
| D3 | Every component names the same checkpoint and plan identity as Integration; each keeps a piece-appropriate citation and excerpt; the excerpt (not the citation) is proven verbatim; pairs need not be identical | CAP L407 · ROLE 50 · TMPL 284, 396 | ROLE |
| D4 | Two distinct records per review — helper-owned integrity manifest and separate schema-valid verdict. Neither substitutes for the other | CAP L405, L409 · ROLE 50, 73 | ROLE |
| D5 | Do not hand-transcribe derivable fields; run `scaffold-verdict` first | ROLE 50 | ROLE |
| D6 | `validate-verdict` must pass before a record is used; `gauntlet_protocol.py` is the authoritative fail-closed enforcement of the declarative schema | ROLE 50 · TMPL 225 | ROLE |
| D7 | Verdict returns the single largest meaningful gap and the exact next acceptance test | CAP L405, L407 · ROLE 36 · TMPL 228–229 | **CAP** (bar) + ROLE |

## E — Staleness and integration (8) — *repaired 2026-08-04; see D-1*

| ID | Rule | Currently in | → |
|---|---|---|---|
| E1 | Every component verdict declares a non-empty `reviewed_paths` set of safe repo-relative paths existing in the candidate tree at its bound SHA | CAP L407 · ROLE 39 · TMPL 284 | ROLE |
| E2 | Component `PASS` binds **iff** (a) its candidate is an ancestor of the final candidate, (b) the diff restricted to `reviewed_paths` is empty, (c) the declared set matches the referenced record | CAP L407 · ROLE 39, 223 · TMPL 284, 396 | ROLE |
| E3 | A stale verdict, and only a stale verdict, reruns with a new run ID/ref; a repair touching no reviewed path reruns nothing | CAP L407 · ROLE 39 · TMPL 284, 396 | ROLE |
| E4 | `reviewed_paths` declared honestly and broadly; understating them is the sole unsoundness. Integration verifies each declared path exists in the candidate tree | CAP L407 · ROLE 39 | ROLE |
| E5 | A current component `PASS` binds its **own earlier** SHA/tree; only the Integration Critic runs at the final SHA/tree | CAP L407 · TMPL 396 — **contradicted at ROLE 40, ROLE 196, TMPL 372 (D-1)** | ROLE |
| E6 | One fresh read-only Integration Critic at the final SHA/tree, separate new clean detached checkout, same two-record contract | CAP L407 · ROLE 39 · TMPL 241–262 | ROLE |
| E7 | Integration verifies the complete checkpoint artifact, current component verdicts, contract consistency, hard invariants, reported metrics, documentation; does not redesign | CAP L407 · ROLE 39 · TMPL 281–288, 313 | ROLE |
| E8 | Integration FAIL re-enters the repair loop; the repair invalidates only verdicts whose reviewed paths it touched | CAP L407 · ROLE 39 | ROLE |

## F — Mandatory surfaces and oracles (6) — **scientific risk, stays in CAP**

| ID | Rule | Currently in | → |
|---|---|---|---|
| F1 | Five mandatory component critic surfaces when in scope: temporal normalization · champion/benchmark schema firewall · A75 climatology fit lineage · CP-2 label-blind four-catalog metric-only recomputation · M3 CQR threshold recomputation on the §6.2 hand-checkable fixture and persisted calibration predictions | CAP L405 · ROLE 38 · TMPL 89–96 | **CAP** |
| F2 | At M1, surfaces 1–3 are unsatisfied until a fresh Critic independently executes all five §9.4 acceptance oracles (M1-O1…O5) | CAP L405 · ROLE 38 · TMPL 98–105, 140 | **CAP** |
| F3 | The Critic — not the Builder — materializes and hashes oracle fixtures outside the candidate checkout and computes expected results independently; repository property tests do not substitute | ROLE 38 · TMPL 140 | **CAP** |
| F4 | A Builder may not issue these verdicts for its own work | ROLE 38 | **CAP** |
| F5 | The Lead may add another Critic only when risk justifies the cost within the supplied ceiling | CAP L405 | **CAP** |
| F6 | No comparison is called blind merely because labels were renamed | ROLE 36, 93 · TMPL 235 | **CAP** |

## G — Evidence storage (9)

| ID | Rule | Currently in | → |
|---|---|---|---|
| G1 | Live evidence root is ignored `<repo>/.gauntlet/evidence/<checkpoint>/`, outside every Builder/Critic worktree and outside the candidate Git tree | CAP L409 · ROLE 63–73 · TMPL 150 | ROLE |
| G2 | `init-evidence` under one exclusive lock creates the run root and `_support/<run-id>/` pair, rolling back an ordinary partial failure; neither may preexist, be reused, or traverse a symlink; a half-pair fails closed. Not an atomic paired-directory primitive | CAP L409 · ROLE 73 · TMPL 150 | ROLE · **P2 candidate** |
| G3 | The run root contains exactly `integrity-manifest.json` and `critic-verdict.json`; never reused or mutated | CAP L409 · ROLE 73 · TMPL 150 | ROLE |
| G4 | Every file-backed artifact/input/stdout/stderr/decision-evidence path is a regular non-symlink file physically under its owned support root, SHA-256-bound, `st_nlink` exactly 1; a path outside that root is invalid regardless of hash | CAP L409 · ROLE 73 · TMPL 150, 227 | ROLE · **P2 candidate** (`st_nlink`, symlink) |
| G5 | Safe hash/lineage manifests substitute for raw restricted or impractically large data | CAP L409 · ROLE 73 · TMPL 150 | ROLE |
| G6 | Unhashed prose or observations are not decision evidence | CAP L409 · ROLE 73 · TMPL 150 | ROLE |
| G7 | The frozen workbench and Return Packet may live at checkpoint-root level; they are not verdict evidence | CAP L409 · ROLE 73 | ROLE |
| G8 | Live verdicts/manifests never under `docs/` while the checkpoint is open (would change the candidate SHA and recursively invalidate); the constraint expires at terminal return | CAP L409 · ROLE 73 | ROLE |
| G9 | A changed candidate requires a new run ID, piece, ref, and support root | ROLE 75 · TMPL 150 | ROLE |

## H — Candidate refs (6)

| ID | Rule | Currently in | → |
|---|---|---|---|
| H1 | `create-ref` makes the exact non-overwriting local `refs/gauntlet-evidence/<checkpoint>/<run-id>/<piece>` at candidate `HEAD`, before the Critic snapshot; the tool requires candidate SHA to equal current `gauntlet/<checkpoint>` `HEAD` | CAP L405, L409 · ROLE 75 · TMPL 142–147 | ROLE |
| H2 | `verify-ref` before launch and again before any terminal Return Packet, for every cited candidate including the final | ROLE 75 · TMPL 320–324 | ROLE |
| H3 | Refs never move or publish; only Yarden may delete them | CAP L409 · ROLE 75 | ROLE |
| H4 | The disposable `gauntlet/<checkpoint>` branch is not spent until all cited SHAs are reachable through evidence refs | CAP L409 · ROLE 75 | ROLE |
| H5 | Removing a Critic snapshot or Builder worktree does not remove its evidence records or refs | ROLE 75 | ROLE |
| H6 | All checkpoint, run, and piece IDs must be ref-safe identifiers accepted by the tool | ROLE 75 | ROLE |

## I — Ceiling and clock (10)

| ID | Rule | Currently in | → |
|---|---|---|---|
| I1 | The ceiling covers orientation through terminal packet, measured as one active elapsed wall clock, not additive agent effort | CAP L399, L403 · ROLE 97 · TMPL 58 | ROLE |
| I2 | `consumed = terminal_at_utc − started_at_utc − Σ eligible_pause_seconds` | ROLE 99 | ROLE |
| I3 | Record start, each paused/resumed pair with reason and evidence, terminal, and raw seconds in both workbench and packet; raw seconds enforce, decimal hours display only | CAP L409 · ROLE 101 · TMPL 76–80, 339–340 | ROLE |
| I4 | A pause is eligible only while **all** authorized Lead/Builder/Critic/Integration/test/tool activity is stopped, for an already-authorized external dependency or platform suspension | ROLE 101 · TMPL 58 | ROLE |
| I5 | A newly required owner action, credential, source, or authority returns terminal `BLOCKED` — not an indefinite pause | ROLE 101 · TMPL 58 | ROLE |
| I6 | Parallel contexts overlap on the single clock and never sum | CAP L399 · ROLE 101 · TMPL 58 | ROLE |
| I7 | Approaching the ceiling is a prioritization signal, never permission to weaken a ratified criterion; reaching it before PASS produces `BUDGET_EXHAUSTED` | CAP L407 · ROLE 103 | **CAP** (bar) + ROLE |
| I8 | Only the Orchestrator may issue a replacement brief with a changed ceiling; the owner authorizes added time **to the Orchestrator**, and the Lead may not accept a direct extension or resume before the replacement brief | CAP L425 · ROLE 103 · TMPL 403 | **CAP** |
| I9 | The Lead allocates internal target windows but cannot enlarge the ceiling | CAP L399 · ROLE 5, 34 | ROLE |
| I10 | Gauntlet planning reserve — **CP-0 2 h**, CP-1 6 h, CP-2 5 h, CP-3 5 h, CP-4 3 h, CP-5 3 h = **24 h**. Planning-load estimates, not additive agent-hours or Lead-granted budgets; the Orchestrator combines reserve with milestone allocation at issue time | CAP L425 (**omits CP-0, says 22 h — D-2**) · PROG 36 | **CAP** + PROG |

## J — `workbench.md` (6)

| ID | Rule | Currently in | → |
|---|---|---|---|
| J1 | Exists only while the authorized checkpoint is active; created only after a valid brief arrives | CAP L409 · ROLE 107 · TMPL 64 | ROLE |
| J2 | Git-ignored; never enters a candidate commit or Critic checkout/context | CAP L409 · ROLE 116 · TMPL 138 | ROLE |
| J3 | Operational visibility only — not program state, acceptance authority, audit log, or second tracker | CAP L409 · ROLE 116 · TMPL 138 | ROLE |
| J4 | The Orchestrator never reads it, Yarden never carries it upward, `progress.md` never imports from it | CAP L409 · ROLE 116 · TMPL 138 | ROLE |
| J5 | May show goal/bar + anchor, ceiling + timestamps + pause ledger + raw seconds, Lead-chosen pieces + artifact paths, current evidence, latest verdict + largest open gap, exact terminal blocker | ROLE 109–114 · TMPL 67–135 | TMPL (form) |
| J6 | At terminal return: freeze a renamed snapshot at checkpoint-evidence-root level outside every immutable run dir, only if it holds unique evidence (else delete); remove as active root workbench; never carry into the next checkpoint | CAP L409 · ROLE 116 · TMPL 138 | ROLE |

## K — Terminal conditions (10)

| ID | Rule | Currently in | → |
|---|---|---|---|
| K1 | Exactly one terminal status: `PASS` \| `BLOCKED` \| `PLATEAU` \| `BUDGET_EXHAUSTED` | CAP L407 · ROLE 141–146 · TMPL 55, 329 | **CAP** |
| K2 | `PASS` requires every checklist item + every applicable mandatory independent check + complete valid records for every required review + current fresh Integration `PASS` + computed-current binding for every relied-on component `PASS` | CAP L407 · ROLE 40, 223 · TMPL 396 | **CAP** |
| K3 | `BLOCKED` = owner credential/action, new authority, ratified-methodology change, destructive/public action, missing or untestable acceptance bar, or plan/reality resolution required | ROLE 144 · TMPL 401 | **CAP** |
| K4 | `PLATEAU` = the next improvement is not worth its cost, or two material repair attempts produced no meaningful improvement | CAP L407 · ROLE 145 · TMPL 402 | **CAP** |
| K5 | `BUDGET_EXHAUSTED` = the raw-seconds ceiling is reached before `PASS` | CAP L407 · ROLE 146 | **CAP** |
| K6 | No terminal status weakens the bar or advances the checkpoint | CAP L407 · TMPL 405 | **CAP** |
| K7 | A non-PASS return preserves evidence and states the smallest exact decision, authority, or resource change needed; never report partial work as `PASS` | ROLE 148 | ROLE |
| K8 | Integration `NOT_RUN` only in a non-PASS packet stating the exact terminal reason that prevented it; never implies a pass | CAP L407 · ROLE 223 · TMPL 396 | **CAP** |
| K9 | At **every** terminal return, stop all Track B work — do not inspect, research, scaffold, branch for, or plan the next checkpoint | CAP L407 · ROLE 150 · TMPL 55, 405 | **CAP** |
| K10 | The Lead or Builder cannot self-certify closure | ROLE 40 | **CAP** |

## L — Return Packet (11)

| ID | Rule | Currently in | → |
|---|---|---|---|
| L1 | Sole upward artifact; header carries status, repo, anchor, evidence roots, frozen root, final candidate commit/tree/branch, working-tree state, data snapshot/cutoff/hash, ceiling, start/terminal UTC, pause ledger, consumed raw seconds, Integration verdict + manifest/verdict paths and hashes | CAP L409 · ROLE 155–171 · TMPL 327–343 | TMPL |
| L2 | Critic run inventory table | ROLE 173–175 · TMPL 345–347 | TMPL |
| L3 | CP-2 chain table (CP-2 only) | ROLE 177–185 · TMPL 349–361 | CP2 |
| L4 | Preserved candidate refs table with verified-reachable column | ROLE 187–189 · TMPL 363–365 | TMPL |
| L5 | Complete named CP/FCP checklist table mapping **every** item to PASS/OPEN + direct evidence — always the complete checklist, never a convenience extract | CAP L409 · ROLE 191–193, 223 · TMPL 367–369, 396 | **CAP** (rule) + TMPL (form) |
| L6 | Independent criticism table | ROLE 195–197 · TMPL 371–373 | TMPL |
| L7 | Engineering decisions: decision + rationale, rejected alternatives, largest failure uncovered and how repaired | CAP L409 · ROLE 199–202 · TMPL 375–378 | TMPL |
| L8 | Reproduction: exact commands, artifacts, metrics/screenshots | ROLE 204–207 · TMPL 380–383 | TMPL |
| L9 | Open risks or exact owner action | ROLE 209–210 · TMPL 385–386 | TMPL |
| L10 | 3–5 defense questions grounded in actual architecture, tradeoffs, and evidence; they never alter engineering CP criteria | CAP L409 · ROLE 212–216, 221 · TMPL 388–389 | **CAP** (rule) + TMPL (form) |
| L11 | States that Track B has stopped and no later-checkpoint work has begun | CAP L409 · ROLE 218 · TMPL 391 | TMPL |

## M — Evidence freezing (4)

| ID | Rule | Currently in | → |
|---|---|---|---|
| M1 | `.gauntlet/` is git-ignored, so records are untracked; refs keep candidate commits reachable but nothing keeps the proof of review | ROLE 120–124 | ROLE |
| M2 | After the terminal Return Packet, and only then, run `freeze-evidence` to `docs/track-b/evidence/<checkpoint>` | ROLE 126–131 | ROLE |
| M3 | `freeze-evidence` revalidates every record, copies each run's manifest and verdict, and writes `frozen-evidence.json` indexing run, verdict, candidate SHA, ref, and hash | ROLE 133–135 | ROLE |
| M4 | Freezing invalidates nothing; committing it is Yarden's decision | ROLE 135–137 | ROLE |

## N — Orchestrator receipt (7)

| ID | Rule | Currently in | → |
|---|---|---|---|
| N1 | Orchestrator checks the packet names the authorized repo/checkpoint/anchor, maps every checklist item to direct evidence, includes all applicable surfaces and M1 oracles, and hides no open item behind `PASS` | TMPL 396 | TMPL |
| N2 | Supported `PASS` → close only that checkpoint in `progress.md`, summarize evidence, then ask Yarden explicitly whether to authorize the next stage | TMPL 400 | TMPL |
| N3 | `BLOCKED` → request only the exact owner action, authority, or resolution named by the packet | TMPL 401 | TMPL |
| N4 | `PLATEAU` → decide whether the remaining improvement warrants a new bounded brief; never relabel it `PASS` | TMPL 402 | TMPL |
| N5 | `BUDGET_EXHAUSTED` → decide whether to issue a replacement brief with a numeric extension; a reduced bar first requires an owner-ratified amendment and new anchor | TMPL 403 | TMPL |
| N6 | No terminal status automatically opens the next checkpoint | TMPL 405 | **CAP** |
| N7 | The Orchestrator verifies by reported `validate-verdict` / `verify-ref` exit codes, not by re-deriving hashes | TMPL 396 (implicit) | TMPL |

## O — CP-2 label-blind protocol (12) — **entire domain → CP2, loaded only at CP-2**

| ID | Rule | Currently in | → |
|---|---|---|---|
| O1 | Applies only when CP-2 is the authorized checkpoint; imposes nothing elsewhere | CAP L411 · ROLE 93 · TMPL 237–239 | CP2 |
| O2 | Machine contract is `cp2-blind-four-catalog.schema.json`; canonical transitions are `blind-prepare/recompute/freeze/reveal/adjudicate` | CAP L413 · TMPL 48 | CP2 |
| O3 | Final candidate must already commit `source-manifest.json` and `selection-declaration.json`; never supplied to the Blind Critic | CAP L413 · TMPL 45 | CP2 |
| O4 | `blind-prepare` draws a 256-bit secret seed/nonce and fresh unbiased permutation to `A/B/C/D`; custody dir `0700`/files `0600`, create-only | CAP L415 | CP2 · **P2 candidate** |
| O5 | Commitment binds mapping preimage, seed/nonce, candidate SHA/tree, source-manifest hash, frozen source hashes, invocation hash, rule identity | CAP L415 | CP2 · **P2 candidate** |
| O6 | Blind Critic recomputes identity-free metrics only; never identifies the base, applies eligibility/tie-breaks, selects a label, or asserts a winner | CAP L416 · TMPL 46, 361 | **CAP** (scientific) + CP2 |
| O7 | Identity scan of every support filename, raw byte stream, and verdict string before the verdict is accepted | CAP L416 | CP2 |
| O8 | `blind-freeze` runs only after a schema-valid Blind `PASS`; it is the sole allocator of the Integration run/ref/support identity | CAP L417 | CP2 |
| O9 | `blind-reveal` refuses without a valid freeze or on any changed frozen byte; copies (never hard-links) into the Integration support root | CAP L418 | CP2 · **P2 candidate** |
| O10 | Adjudication only in fresh Integration, against Integration-owned copies, never custody; the real winner must equal the committed selection declaration | CAP L419 · TMPL 47, 290–316 | **CAP** (scientific) + CP2 |
| O11 | Threat boundary: modes/prompts/hashes are custody and chronology evidence, **not** adversarial secrecy from a same-UID process. `ENFORCED_READ_ISOLATION` only with a real read allowlist/sandbox; otherwise `COOPERATIVE_PROCEDURAL` | CAP L421 · TMPL 49, 398 | CP2 |
| O12 | Fail-closed restart: any candidate/source/rule/selection change, Blind `FAIL`, premature exposure, tamper, reuse, or winner mismatch invalidates the whole attempt; new IDs, seed, permutation, custody. A revealed mapping is never reused | CAP L423 · TMPL 398 | CP2 · **P2 candidate** |

## P — Debugging, research, constraints, communication (9)

| ID | Rule | Currently in | → |
|---|---|---|---|
| P1 | Own the debugging loop end to end: read the actual error, fix the cause, rerun the affected bar and relevant regression/invariant checks | ROLE 227 | ROLE |
| P2 | Research only if the active brief authorizes it; keep it inside the same scope and ceiling | ROLE 228 | ROLE |
| P3 | A source blocked by login/paywall/bot detection/region/rate limit returns terminal `BLOCKED` naming the exact artifact; never ask Yarden mid-loop or silently substitute a weaker source; skip an optional source only when the plan permits and record the effect | ROLE 229 | ROLE |
| P4 | Budget: $0 expected run rate, $65/month policy ceiling (target $5–25); no paid service where a ratified local/free path exists | ROLE 233 · TMPL 39 | ROLE |
| P5 | Hardware: M3 / 16 GB / CPU-only; stream or chunk large pulls; never accumulate the full archive in RAM | ROLE 234 · TMPL 40 | ROLE |
| P6 | Data: only the sources and fallbacks the named plan permits; never reintroduce PJM, a geo-fragile vendor, or non-redistributable data | ROLE 235 | ROLE |
| P7 | Scope: build exactly the authorized checkpoint; §13 "What this project is NOT" boundaries stay closed absent an owner-ratified amendment | ROLE 236 | ROLE |
| P8 | Reproducibility: pinned deps, fixed seeds, committed legally redistributable snapshot and attribution, tagged code, traceable experiment lineage | ROLE 237 | ROLE |
| P9 | Reply in English; direct and technically precise; show Lead-level reasoning; no low-value agent chatter; own mistakes plainly | ROLE 241 | ROLE |

---

## Post-prune destination summary

| Owner | Rules | Note |
|---|---|---|
| **CAP** `capstone_V6_5.md` §12 | 26 (A7, A8, B8, D7, F1–F6, I7, I8, I10, K1–K10, L5, L10, N6, O6, O10) | The bar only |
| **ROLE** `engineering-role.md` | 91 | The process; sole owner of execution mechanics |
| **TMPL** `gauntlet-templates.md` | 19 | Forms + Orchestrator receipt; no normative prose it does not own |
| **CP2** `cp2-blind-protocol.md` | 12 | Loaded only at CP-2 |
| **PROG** `progress.md` | 1 (I10 shared) | Program state |
| **Total** | **148** | **No rule dropped** |

Nine rules are deliberately co-owned (bar in CAP, mechanics in ROLE/TMPL): A5, B8, D7, I7, I10, L5, L10, O6, O10. Co-ownership is stated once in each place with an explicit cross-reference, never restated in full.

## Verification protocol for Phase 1

1. Apply the cuts.
2. For each rule ID, confirm the rule is present in its assigned owner.
3. Confirm no rule appears normatively outside its assigned owner (cross-references excepted).
4. Fix D-1, D-2, D-3 in the same pass.
5. Re-run the suite.
6. Record the result here as a dated verification block.

---

# Phase 1 verification — 2026-08-05 — **PASS**

## Count correction

**The rule total is 138, not 148.** The header and summary table above were written with an
addition error; the per-domain counts were correct throughout and are unchanged. Domains sum:
A 10 · B 10 · C 13 · D 7 · E 8 · F 6 · G 9 · H 6 · I 10 · J 6 · K 10 · L 11 · M 4 · N 7 · O 12 ·
P 9 = **138**. Corrected ownership split: **CAP 27 · ROLE 85 · TMPL 16 · CP2 10 = 138.**
(CAP 27, not 26 — K7 routes to ROLE, which the earlier summary double-counted.)

## Result

All **138** rules verified present in their assigned owner by normalized-whitespace substring
match. Two flags were raised on the first pass:

| Flag | Verdict | Action |
|---|---|---|
| **O6** absent from CAP | **False positive** — the phrase wraps across a line break; grep missed it, normalized match found it | none |
| **G4** absent from ROLE | **REAL — a genuine near-drop** | fixed |
| **I9** absent from ROLE | **REAL — partial coverage only** | fixed |

**G4** (`st_nlink` / hard-linked-inode invalidity) was stated in `capstone_V6_5.md` §12 L409 and in
the templates, but never in `engineering-role.md` — its assigned owner. Deleting the capstone
paragraph would have left the rule stated only in a form document. Restored to
`engineering-role.md` § *Live evidence and commit retention*.

**I9** (the Lead allocates internal target windows but cannot enlarge the ceiling) was in
`capstone_V6_5.md` L399, which the prune compressed. ROLE covered both halves only implicitly
across three separate sentences. Now stated explicitly in § *Active-elapsed wall-clock ceiling*.

This is the second time the inventory method caught a live rule loss that a targeted grep did not.

## D-fixes

| Defect | Status | Evidence |
|---|---|---|
| **D-1** — rerun-all surviving at `engineering-role.md:40`, `:196`, `gauntlet-templates.md:372` | **CLOSED** | Zero matches repo-wide for `must equal final` / `bound to the exact final candidate` / `invalidates all earlier` / `no selective reuse` |
| **D-2** — reserve table omitted CP-0 (22 h vs 24 h) | **CLOSED** | `capstone_V6_5.md` now reads `CP-0 2 h; … — 24 h total`, matching `progress.md:36` |
| **D-3** — brief template cited §12 as CP-2 protocol authority | **CLOSED** | Repointed to `docs/track-b/cp2-blind-protocol.md`; zero stale §12-protocol citations |

## Measured reduction

| Surface | Before | After | Δ |
|---|---:|---:|---:|
| `capstone_V6_5.md` §12 execution contract | 2,101 | **901** | −57% |
| `docs/track-b/gauntlet-templates.md` | 3,683 | **2,762** | −25% |
| `engineering-role.md` | 3,836 | **3,512** | −8% |
| `AGENTS.md` | 777 | 777 | — |
| **Total loaded per checkpoint** | **10,808** | **8,506** | **−21%** |
| `cp2-blind-protocol.md` | loaded always (partly) | **CP-2 only** | 2,338 words off every non-CP-2 checkpoint |

**The ~4,000-word target was not met, and was not reachable.** It was estimated before the
enumeration existed. With 138 rules preserved and 85 of them legitimately owned by
`engineering-role.md`, ~8,500 words is the floor for a relocation-only pass. The deeper cut is
Phase 2, which *removes* rules (the nine Phase-2 candidates) rather than relocating them.

What the pass did buy beyond word count: single ownership per rule, which closes the drift class
that produced D-1 across two separate sessions; and CP-2's protocol off the context of every
checkpoint that is not CP-2.

## Phase-2 candidates — confirmed intact

All nine relocated unchanged, none removed: **G2** (exclusive init lock, rollback, half-pair
fail-closed) · **G4** (`st_nlink`, symlink rejection) · **O4** (256-bit seed, `0700`/`0600` custody)
· **O5** (commitment binding) · **O9** (copy-never-hard-link reveal) · **O12** (fail-closed restart
chain). Phase 2 removes rules and therefore requires its own before/after count, not this one.

## Suite

`69 passed, 18 subtests passed` — green before and after. No code, schema, or test file was touched
in Phase 1.

## Files changed

`capstone_V6_5.md` · `engineering-role.md` · `docs/track-b/gauntlet-templates.md` ·
`capstone_V6_4-to-V6_5-amendments.md` · `capstone_V6_3-to-V6_4-amendments.md` · `progress.md` ·
`docs/track-b/rule-inventory.md` (new). **No version bump** — relocation only; no bar, checklist
item, invariant, or acceptance criterion changed.

---

# Phase 2 rule-delta — 2026-08-05 — **PREPARED, NOT EXECUTED**

## Count correction

**There are 6 Phase-2 candidates, not 9.** The Phase-1 verification block wrote "all nine"
while listing six IDs. The marked candidates in the tables above are and always were:
**G2, G4, O4, O5, O9, O12.**

## Per-clause disposition

Retirement operates on **clauses**, not whole rules. Only one rule retires outright.

| Rule | Clause | Disposition | Reasoning |
|---|---|---|---|
| G2 | exclusive init lock + rollback | **RETAIN** | Concurrency guard for parallel Critic init, not an isolation claim. Nothing in the docs disclaims it. |
| G2 | run/support root may not preexist or be reused | **RETAIN** | Load-bearing: stops stale evidence masquerading as a fresh run. |
| G2 | may not traverse a symlink | **RETAIN — reclassified** | Originally marked a candidate. It is **containment**, not secrecy: a symlinked evidence root genuinely breaks "evidence is physically where it claims." Different threat class from the disclaimed one. |
| G2 | observed half-pair fails closed | **RETAIN** | Prevents a real half-initialized state. |
| G2 | "not an atomic paired-directory primitive" | **RETIRE** | Disclaimer prose about what the mechanism is not. Carries no obligation. |
| G4 | evidence physically under its own owned support root | **RETAIN** | The load-bearing half of G4. |
| G4 | evidence carries SHA-256 | **RETAIN** | — |
| G4 | evidence is a regular non-symlink file | **RETAIN** | Containment, as G2 above. |
| G4 | `st_nlink` exactly one / hard-linked inode invalid | **RETIRE** | **Blocks hard-linking while copying is explicitly permitted and produces an identical hash.** The permitted alternative achieves the identical outcome, so the check constrains nothing. O9 exists solely to mandate that alternative. |
| O4 | 256-bit secret seed | **RETIRE** | Defends against enumerating 24 permutations against the commitment — while `capstone_V6_3-to-V6_4-amendments.md:155` concedes direct custody reading by a same-UID process is unprevented. Strong lock, conceded-open door. |
| O4 | custody `0700` / files `0600` **as a validity gate** | **RETIRE** | Same concession, stated verbatim in the docs. Creation modes stay (free); *enforcement* on read goes. |
| O4 | fresh unbiased permutation into a create-only custody dir | **RETAIN** | This is the actual blinding. |
| O5 | cryptographic commitment binding preimage + seed | **RETIRE** | Its purpose is proving the mapping was fixed before recompute. Under `COOPERATIVE_PROCEDURAL` a create-only record with a timestamp carries the same weight as everything else in the chain. |
| O5 | mapping fixed **before** metrics are computed | **RETAIN** | The chronology property is the real guarantee and survives without the crypto. |
| O9 | copy rather than hard-link on reveal | **RETIRE (whole rule)** | Exists only to enforce the `st_nlink` rule it pairs with. Moot once G4's clause goes. |
| O12 | new seed / custody directory per attempt | **RETIRE** | Tied to the retired crypto. |
| O12 | a revealed mapping is never reused; restart draws a new permutation | **RETAIN** | Load-bearing: a reused mapping is knowable to the next Blind Critic. |

**Net: 138 → 137 rules.** One rule retires outright (**O9**); five are reduced in scope
(**G2, G4, O4, O5, O12**); **132 are untouched**.

## The scoping finding — this changes Phase 2

Measuring where the retired clauses actually live:

| Target | Code location | General or CP-2? |
|---|---|---|
| `st_nlink` @ `gauntlet_protocol.py:411` | `_read_single_link_file` | **CP-2 only** — all 15 callers are `blind-*` / custody paths |
| `st_nlink` @ `:3622` | custody snapshot | **CP-2 only** |
| Mode enforcement — all 6 `_require_mode` sites | `:2156, :2526, :2534, :2767, :2796, :3616` | **CP-2 only** — every site is literally labelled `"CP-2 …"` |
| Tool-binding runtime hash | `_cp2_require_runtime_tool_hash` | **CP-2 only** |
| Seed / commitment / custody / preimage / receipt | ~1,108 lines (19% of the file) | **CP-2 only** |
| `_reject_symlinked_evidence_ancestors` | 4–5 general sites | General — **but RETAINED** (reclassified above) |

**Every clause approved for retirement lives inside the CP-2 blind protocol.** The general-purpose
evidence machinery contains nothing that the documents disclaim. Phase 2 is therefore not "cut the
filesystem hardening and, separately, the CP-2 chain" — the filesystem hardening *is* the CP-2
chain's plumbing. Phase 2 is one thing: **the CP-2 blind-protocol simplification.**

## Consequences

1. **Size.** ~1,108 tool lines, the 1,074-line `test_cp2_blind_protocol.py`, and the 1,578-line
   `cp2-blind-four-catalog.schema.json`. The plan estimated Phase 2 at **~2 h**. That estimate is
   wrong by a wide margin — the same class of error as the ~4,000-word target.
2. **Dormancy.** None of this code executes before **M2/CP-2**, projected syllabus Month 3. CP-0
   and CP-1 never touch it.
3. **Signal.** CP-0 is the first real run of the *evidence and verdict* machinery — the part
   Phase 2 does **not** touch. Running CP-0 first costs nothing here and yields the measurements
   Phase 3 needs.

## Recommendation

Reorder to **CP-0 → Phase 2 (CP-2 simplification) → Phase 3**, and re-estimate Phase 2 honestly
before executing it. Nothing is lost: the retired clauses cannot fire before Month 3.

---

# Phase 2 execution record — 2026-08-05 — **STAGE 1 EXECUTED · REMAINDER ABORTED**

Owner authorized the "Core" variant with the time constraint removed (Gauntlet reserve raised
24 h → 48 h). Stage 1 executed and verified. The remaining crypto pass was then **deliberately
abandoned on the merits**, not on cost.

## Executed — Stage 1, suite green throughout

`scripts/gauntlet_protocol.py` **5,649 → 5,626 lines**.

| Removed | Result |
|---|---|
| `st_nlink` gate in `_read_single_link_file` | **zero occurrences remain repo-wide** |
| `st_nlink` + `0o600` gates in `_cp2_custody_snapshot` | snapshot keeps its functional hash/size comparison |
| `_require_mode` — the function and **all six call sites** | zero occurrences remain |

`0o600`/`0o700` **creation** modes are retained by design: creating files private is free and is not
a validity gate. The custody snapshot's before/after comparison is retained because it proves the
*reveal step did not mutate custody* — a correctness property of our own code, not an adversarial
control.

## Aborted — the commitment / preimage / receipt / seed layer

Attempted and reverted: `cp2_permutation` → `SystemRandom().shuffle()` broke two callers, and the
fix cascades irreducibly into `prepare`, five validators, and the freeze/reveal chain. That work is
atomic; a half-applied record-shape change is a worse state than either endpoint.

**Why it was abandoned rather than rescheduled:**

1. **The remaining layer is already honestly labelled.** The §12 / `cp2-blind-protocol.md` threat
   boundary *mandates* the `COOPERATIVE_PROCEDURAL` label absent a real read sandbox, and states
   verbatim that the disclosure "does not turn hashes into proof of blindness." The system does not
   overstate itself. This defuses the correctness-and-honesty argument that justified the cut — an
   argument that **does** hold for what Stage 1 removed (silent gates, no disclosure, blocking
   nothing since copying is permitted and yields an identical hash).
2. **What is left is a size argument, and size does not apply here.** `gauntlet_protocol.py` is
   **executed, never loaded into agent context** — Phase 1 already removed the prose that was
   actually costing us. Line count in a dormant module has no effect on the Gauntlet loop.
3. **Risk asymmetry.** The blind protocol is the machinery that makes the CP-2 four-catalog
   selection honest — the scientific centerpiece of the strict-gate design. A refactor bug
   introduced now would not surface until **M2/CP-2 in Month 3**, with no intervening run to catch
   it, at the exact moment the protocol is needed. Against ~600 lines in code that is green and
   tested, that is a bad trade.

## Rule-ledger effect

**No rule fully retires. The count stays 138.**

| Rule | Effect |
|---|---|
| **G4** | `st_nlink` / hard-linked-inode clause **retired**. Containment, non-symlink, and SHA-256 clauses retained. |
| **O4** | Custody `0700`/`0600` **enforcement** clause retired. Fresh permutation, create-only custody, and creation modes retained. |
| **O9** | **VESTIGIAL.** Reveal still copies rather than hard-links, but the `st_nlink` rule it enforced against is gone. Harmless and correct behaviour; it is no longer load-bearing and must not be cited as a control. |
| G2, O5, O12 | **Untouched.** Lock, no-reuse, fail-closed, commitment chronology, and never-reuse-a-revealed-mapping all stand as written. |

## Re-entry trigger

Do **not** schedule the crypto simplification as standalone work. If CP-2 code must be modified
before Month 3 for any other reason, do it then — the blast radius is already open and the marginal
risk approaches zero. Otherwise it stands as accepted, disclosed, dormant surplus.

## Suite

`69 passed, 18 subtests passed` — green before Stage 1, after Stage 1, and after the revert of the
attempted crypto work. No test, schema, or documentation file was modified by Phase 2.

---

# OPTION C — machinery retired, governance kept — 2026-08-05

Owner executive call, superseding the Phase 2 abort. The protocol tooling is deleted outright; the
governance it was built to enforce is retained in full and now rests on markdown verdicts and plain
`git worktree` isolation.

**Rationale of record.** The sprint's value came from the **external review of the plan**
(AMD-1/2/3) and from **Builder≠Critic separation**. The tooling assumed a threat model of agent
*malice*; the real risk is agent *error*, and error is caught by a fresh Critic inspecting the real
artifact — not by hash-chaining a verdict record. 10,587 lines of incidental protocol were not worth
carrying through five checkpoints.

## Deleted — 10,587 lines

`scripts/gauntlet_protocol.py` 5,625 · `schemas/cp2-blind-four-catalog.schema.json` 1,578 ·
`tests/test_gauntlet_protocol.py` 1,235 · `tests/test_cp2_blind_protocol.py` 1,074 ·
`schemas/critic-verdict.schema.json` 626 · `scripts/gauntlet_critic_snapshot.sh` 276 ·
`docs/track-b/cp2-blind-protocol.md` 173

## Rule ledger — 138 → 105

**33 rules retire** with the machinery. Every one was a property *of the tooling*, not of the
review.

| Domain | Retired | Why |
|---|---|---|
| **C** — Critic isolation | C5, C6, C7, C9, C11 | Tool-generated integrity manifest, pre-review manifest hash, `PYTHONPYCACHEPREFIX` routing, `verify` refusal conditions, manifest authorship ban. All existed to serve the manifest. |
| **D** — Verdict record | D4, D5, D6 | Two-record separation, `scaffold-verdict`, `validate-verdict`/JSON schema. |
| **G** — Evidence storage | G2, G3, G4, G5, G6, G9 | Init lock, run-root file set, support-root containment/hashing, lineage-manifest substitution, unhashed-prose rule, new-run-on-change. |
| **H** — Candidate refs | H1–H6 (all) | The `refs/gauntlet-evidence/*` namespace. The checkpoint branch keeps candidate SHAs reachable. |
| **M** — Evidence freezing | M1–M4 (all) | `freeze-evidence`. Verdicts are now committed directly, so nothing needs thawing. |
| **O** — CP-2 protocol | O2, O3, O4, O5, O7, O8, O9, O11, O12 | Machine contract, commitment, custody modes, seed, identity scan, freeze/reveal command chain, copy-not-hard-link, `ENFORCED_READ_ISOLATION` eligibility, fail-closed restart machinery. |

**8 rules are reduced, not retired:** C1 (brief contents, now checkable by hand), C8 (post-review
`git status` instead of a manifest re-verify), C13, D1 (markdown fields), G1 (`docs/track-b/evidence/`),
G7, G8, O1.

**105 rules survive untouched** — every rule in domains **A** (authority), **B** (execution loop),
**E** (staleness), **F** (mandatory surfaces and M1 oracles), **I** (ceiling), **J** (workbench),
**K** (terminal conditions), **L** (Return Packet), **N** (receipt), **P** (constraints), plus the
scientific CP-2 bar **O6** and **O10**.

**Nothing in `capstone_V6_5.md`'s checklists changed.** No bar, checklist item, invariant, or
acceptance criterion was weakened. The retired rules were process mechanics owned by
`engineering-role.md` and the templates.

## What replaces them

| Was | Is |
|---|---|
| `init-evidence` + run/support roots + integrity manifest | `git worktree add --detach <path> <sha>` and `git status --porcelain` |
| `create-ref` / `verify-ref` / `refs/gauntlet-evidence/*` | the candidate SHA cited in the verdict, reachable on `gauntlet/<checkpoint>` |
| `scaffold-verdict` + `validate-verdict` + JSON schema | the markdown verdict template, `gauntlet-templates.md` §5 |
| `freeze-evidence` | verdicts committed under `docs/track-b/evidence/<checkpoint>/` as they are written |
| commitment / custody / reveal chain | the Lead withholds the mapping file and reveals after the Blind verdict; `COOPERATIVE_PROCEDURAL`, never claimed as enforced |

## Verification

Orphan sweep clean across every live document: `README.md`, `AGENTS.md`, `orchestrator-role.md`,
`engineering-role.md`, `capstone_V6_5.md`, `gauntlet-templates.md`, `progress.md`. Historical
session-log entries and the amendment sheets retain their references by design — they are the record
of what was built and why it was removed.

No test suite remains; `tests/` is empty until M1 creates the real invariant tests that
`capstone_V6_5.md` §9.4 requires. That is the correct state: there is no longer any protocol to test,
and the tests that existed tested only the protocol.

---

# v6.6 amendment inventory — BEFORE — 2026-08-05

**Purpose.** Enumerate every normative rule the v6.6 Gauntlet amendment (AMD-G1 … G14) will touch,
**before** any of it is authored, so the post-amendment state can be *proved* complete rather than
asserted complete. Phase 2.1 of `docs/track-b/gauntlet-amendment-plan.md`. This is a working
artifact, never agent context.

**Why it runs first.** The method has now caught a live rule loss twice — `G4` and `I9` in Phase 1 —
that targeted greps missed. This amendment touches **five** documents instead of four, and three of
its remedies land in a document that has never been enumerated at all. Authoring first would repeat
the exact failure the method exists to prevent.

**Sources inventoried (complete read):** `capstone_V6_5.md` §12 · `engineering-role.md` ·
`docs/track-b/gauntlet-templates.md` · `AGENTS.md` · **`orchestrator-role.md` (first time — see
D-CP0-14)**.

## Two findings from the enumeration itself

These are not amendment decisions. They are defects in the ledger, found while preparing to use it,
and both are filed in `cp-0-defects.md`.

**D-CP0-14 — `orchestrator-role.md` was never inventoried.** Phase 1's sources were the capstone,
the role doc, the templates, and the CP-2 protocol file. The Orchestrator side of the contract has
never been enumerated, single-owned, or checked against loss — and AMD-G4, G7, and G13 all land
there. **Remedied below as domain Q**, enumerated here for the first time.

**D-CP0-15 — the domain tables above are one amendment out of date.** Option C retired 33 rules and
reduced 8 more, and recorded that as an appended delta. The tables were never restated, so they still
describe machinery that no longer exists: `E6` cites the "two-record contract", `C1` a "pre-created
evidence ref", `G1` the `.gauntlet/` root, `N7` the deleted `validate-verdict`/`verify-ref` exit
codes. Inversely, `engineering-role.md:56`'s cache-routing sentence is **in force but unledgered** —
a surviving remnant of retired `C7`, and the reason D-CP0-9 stayed invisible.

**Consequence for this pass:** every rule statement used below is re-derived from the **current**
document text, not carried forward from the tables above. AMD-G14 extends to restating the 8 reduced
rules in place and striking the 33 retired ones where they sit.

## Baseline

| | Count |
|---|---:|
| Phase 1 enumeration | 138 |
| Retired by Option C | −33 |
| **Live executor-side rules (domains A–P)** | **105** |
| Domain Q — `orchestrator-role.md`, newly enumerated | +23 |
| **Enumerated baseline entering the amendment** | **128** |

Live domain arithmetic: A 10 · B 10 · C 8 · D 4 · E 8 · F 6 · G 3 · H 0 · I 10 · J 6 · K 10 ·
L 11 · M 0 · N 7 · O 3 · P 9 = **105**. Domains H and M are empty — their entire subject matter
(the evidence-ref namespace, evidence freezing) went with the machinery. **AMD-G13 re-enters that
territory with different mechanics**, which is why it needs its own enumeration rather than reviving
retired IDs.

## Domain Q — Orchestrator-side rules (23) — *first enumeration, D-CP0-14*

| ID | Rule | Currently in | → |
|---|---|---|---|
| Q1 | The Orchestrator holds strategic context no executor has; an executor missing context it needs is a routing failure, not an executor failure | ORCH *hierarchy* | ORCH |
| Q2 | Subagents are never briefed by the Orchestrator; referenced only at outcome level | ORCH *hierarchy* | ORCH |
| Q3 | Delegate to a specific executor with a specific brief, never to "the team" | ORCH *hierarchy* | ORCH |
| Q4 | Briefs inherit executor role-doc workflow defaults instead of duplicating them | ORCH *role docs* | ORCH |
| Q5 | The B-Claude brief names exactly one repo, one checkpoint, one ratified anchor, one numeric ceiling; cites the complete checklist; may carry a task-specific extract without narrowing it; never dictates implementation or decomposition | ORCH *role docs*, *Type B-Claude* · co-owned with A5 | ORCH + CAP |
| Q6 | A Return Packet is evidence for the gate decision, never authorization to begin the next checkpoint | ORCH *role docs* · co-owned with N6 | ORCH |
| Q7 | The Orchestrator decides what runs, when, in which repo, against which single checkpoint, under which constraints and ceiling; the Lead owns how | ORCH *Track B* · co-owned with A1/A2 | ORCH |
| Q8 | The Orchestrator does not rewrite ratified criteria, inspect the internal workbench, or mediate between subagents | ORCH *Track B* · co-owned with J4 | ORCH |
| Q9 | "Execute the capstone" resolves to one valid brief for the next schedulable checkpoint; never blanket authorization; if Track B is not schedulable, name the controlling gate | ORCH *Track B* · co-owned with A10 | ORCH |
| Q10 | The fixed launch envelope is delivered as one copy-paste-ready prompt with the canonical brief between markers; it is transport, not a second brief; no commentary inside the fence, no canonical field omitted | ORCH *Type B-Claude* | ORCH |
| Q11 | Do not emit the envelope for a closed prerequisite, an advisory block, B-Manual, or B-Research; state which gate controls instead | ORCH *Type B-Claude* | ORCH |
| Q12 | Clock accounting as stated to the Orchestrator: one active elapsed wall clock, parallel contexts overlap and never sum, ceiling exhaustion is a non-`PASS` terminal, only the Orchestrator extends it | ORCH *Type B-Claude* · co-owned with I1–I8 | ORCH |
| Q13 | Execution defaults inherited from `engineering-role.md` (sole Git writer, isolated Builder worktrees, committed verdicts) are not brief content and not Orchestrator-managed state | ORCH *Type B-Claude* | ORCH |
| Q14 | One checkpoint block may contain many internal turns but remains one Orchestrator block; the owner returns only when the terminal packet exists | ORCH *Session lifecycle* | ORCH |
| Q15 | Silence never closes a Track B CP/FCP; only the consolidated Return Packet can support closure | ORCH *Session lifecycle*, *Verification* | ORCH |
| Q16 | Assume perfect execution of prior blocks unless stated otherwise or a Track A checkpoint was crossed; this carry-forward never applies to Track B closure | ORCH *Closing* | ORCH |
| Q17 | Close a checkpoint only from its consolidated packet, mapping every item in the full checklist to inspectable evidence | ORCH *Verification* · co-owned with N1/L5 | ORCH |
| Q18 | At CP-1 the packet must carry independent verdicts for all five M1 acceptance oracles; Builder tests do not substitute | ORCH *Verification* · co-owned with F2/F3 | ORCH |
| Q19 | The Orchestrator does not audit evidence files and has no shell; record-level rules are enforced by the Lead and evidenced in committed verdicts. The gate is the packet and the verdict files it names, never the internal workbench | ORCH *Verification* | ORCH |
| Q20 | CP-2 receipt gate: the packet must be labelled `COOPERATIVE_PROCEDURAL`; reject any packet claiming cryptographic enforcement | ORCH *Verification* · co-owned with the CP-2 honesty label, now in ROLE (O11 retired by Option C) | ORCH |
| Q21 | `progress.md` is read at session start and regenerated **in full** when durable state changes; never paraphrased from memory | ORCH *Regeneration contract* | ORCH |
| Q22 | Run the omission diff before output; every item present before and absent now is resolved-and-logged or pruned-under-the-rule. Silent drops are the failure mode the contract exists to prevent | ORCH *Regeneration contract* | ORCH |
| Q23 | The regeneration contract applies to `progress.md` and nothing else | ORCH *Regeneration contract* | ORCH |

## Rules the amendment amends (26)

No rule is retired by this amendment.

| Rule | AMD | Change |
|---|---|---|
| A5 | G6 | Referenced, not changed — the packet must now reproduce every required field verbatim |
| A6 | G5 | Invalid brief returns the named terminal status `BRIEF_INVALID` instead of an unnamed "discrepancy" |
| A9 | G2 | Prohibition scoped to **influence**; a declared post-Integration read solely to author the packet is permitted |
| B1 | G10 | State verification extends to repository topology, recorded at start and at terminal return |
| B4 | G8 | The Builder worktree's seed is declared; seeding from prior work is permitted and forces whole-artifact review |
| C1 | G14 | Restate from current text — the "pre-created evidence ref" clause is retired machinery (D-CP0-15) |
| C8 | G14 | Restate — post-review check is `git status --porcelain`, not a manifest re-verify |
| D1 | G11 | Line citations optional and explicitly non-binding; only the verbatim excerpt is load-bearing |
| E2 | G1 | "final candidate" → `final_candidate_sha`; semantics unchanged |
| E5 | G1 | Same terminology change; the earlier-SHA binding is preserved exactly |
| E6 | G1 | Integration runs at `final_candidate_sha`; strike the retired "two-record contract" clause |
| F1 | G12 | The packet declares in-scope/out-of-scope **with a reason** for each of the five surfaces |
| G1 | G14 | Restate — evidence lives at `docs/track-b/evidence/<checkpoint>/`, not `.gauntlet/` |
| — | G9 | `engineering-role.md:56` cache routing: **demote to recommendation** and re-ledger, or drop. Currently in force and unledgered |
| I1 | G5 | Brief validation precedes the clock and consumes no ceiling |
| I2 | G5 | The clock starts at the first repository-state verification performed under a **valid** brief |
| K1 | G5 | Status vocabulary becomes five: `PASS` · `BLOCKED` · `PLATEAU` · `BUDGET_EXHAUSTED` · `BRIEF_INVALID` |
| K2 | G1 | `PASS` binds `final_candidate_sha`; the evidence tip is not the bound SHA |
| L1 | G1,G2,G3,G8,G10 | Header carries two SHAs; adds the provenance block, Landing Report, Builder seeds, and topology |
| L5 | G6 | Adds the reproduced required brief fields alongside the checklist table |
| L6 | G12 | Independent-criticism table carries the surface scope declaration |
| N1 | G1,G2,G6,G12 | Gate gains: the verdict-only delta check, the provenance block, brief-field validation, surface scope |
| N7 | G14 | Restate — cites `validate-verdict`/`verify-ref` exit codes that no longer exist (D-CP0-15) |
| Q5 · Q10 | G4 | Envelope names a minimum executor tier and reasoning effort, and requires a session-freshness declaration |
| Q15 | G7 | Silence still never closes — and gains the abandonment convention it currently lacks |
| Q19 | G3,G13 | The gate gains the landing inspection and the reclamation step |

## Rules the amendment adds (25)

New IDs continue each domain; **R** is a new domain for landing and reclamation, replacing the
territory vacated by retired H and M.

| ID | Rule | AMD | Owner |
|---|---|---|---|
| A11 | An invalid brief is returned as `BRIEF_INVALID` before any repository edit, naming every missing or contradictory required field | G5 | ROLE |
| B11 | The Lead emits `started_at_utc` and its verified repository state as its **first observable output**, before any Builder is dispatched | G7 | ROLE |
| B12 | A Builder worktree seeded from pre-existing work is reviewed as a whole artifact, never as a diff | G8 | ROLE |
| C14 | The Lead declares, in the packet, the exhaustive set of documents read during the decision-bearing phase | G2 | ROLE |
| C15 | Any read performed after the final Integration verdict, solely to author the packet, is declared with its timing and what it did not influence | G2 | ROLE |
| C16 | The role-boundary guarantee is labelled `ASSERTED_ROLE_BOUNDARY`; no packet may imply harness-enforced read isolation | G2 | ROLE |
| E9 | `final_candidate_sha` is the SHA the Integration Critic reviewed; every bar binds to it | G1 | ROLE |
| E10 | `evidence_tip_sha` is the branch tip after the Integration verdict is committed | G1 | ROLE |
| E11 | The delta between them is verdict-only: `git diff --name-only <final>..<tip>` returns nothing outside `docs/track-b/evidence/<checkpoint>/`. A tip touching any other path invalidates the terminal `PASS` | G1 | ROLE + CAP |
| I11 | Brief validation is outside the ceiling; a `BRIEF_INVALID` return records `validation_started_at_utc` and `returned_at_utc`, explicitly excluded from consumed seconds | G5 | ROLE |
| K11 | `BRIEF_INVALID` — the authorization was malformed; no work started, no clock consumed, no repository edit made. Distinct from `BLOCKED`, which means work started and hit an owner-only dependency | G5 | **CAP** |
| K12 | A run that exceeds its ceiling in real elapsed time with no packet is **abandoned**, not `BUDGET_EXHAUSTED` — the latter asserts the ceiling was consumed by work, which an abandoned run cannot evidence | G7 | **CAP** + ORCH |
| L12 | The packet carries a provenance block: decision-phase reads, declared late reads, and the `ASSERTED_ROLE_BOUNDARY` label | G2 | TMPL |
| L13 | The packet carries a Landing Report: both terminal SHAs, the diff against `main`, branch commits, worktrees created and not created, other `gauntlet/*` branches, proposed disposition and commit message | G3 | TMPL |
| L14 | The packet reproduces every required brief field verbatim | G6 | TMPL |
| L15 | The packet declares each Builder worktree's seed — brief-authored, or copied from a named path at a named state | G8 | TMPL |
| L16 | The packet records repository topology at `started_at_utc` and at terminal return, and reports any change | G10 | TMPL |
| N8 | The gate runs the verdict-only delta check itself rather than accepting the packet's claim | G1 | TMPL |
| N9 | A packet with no provenance block is returned unread; an absent block is not an assertion that no late read occurred | G2 | TMPL |
| N10 | The gate reconciles the Landing Report against the live repository; a discrepancy is a gate failure, not a footnote | G3 | TMPL |
| R1 | **One-branch invariant:** at rest the repository has exactly `main`; while a checkpoint is open, exactly one `gauntlet/<checkpoint>`. Never a third | G13 | **AGENTS** |
| R2 | Every closed checkpoint receives exactly one disposition — **LAND** (owner squash, commit by hand, `tag land/<cp>`) or **DISCARD** (`tag archive/<cp>-attempt-<k>`) — and both end in branch deletion | G13 | AGENTS + ORCH |
| R3 | **Tag before delete, always.** A branch may never be deleted while any live document cites a SHA reachable only from it | G13 | **AGENTS** |
| R4 | **The citation follows the ref.** Retiring a branch repoints, in the same operation, every live document that named it | G13 | AGENTS + ORCH |
| R5 | Execution split: INSPECT, DISCARD, REPOINT and RECLAIM are agent-executed; **LAND is owner-authored by hand**. An agent may never delete a ref whose SHAs are not already reachable from a verified tag, nor a branch the owner has not dispositioned | G13 | **AGENTS** |

## Post-amendment ownership

**Correction, recorded rather than quietly fixed.** The first draft of this table read CAP 31 ·
ROLE 98 · TMPL 26 · AGENTS 5 · ORCH 23 · PROG 1 and summed to **184**, against a stated total of 153.
The per-domain counts and the 128 + 25 arithmetic were right throughout; the ownership row values were
carried over from the pre-Option-C split without subtracting the 33 retired rules. This is the same
class of error the Phase 1 inventory made (148 written, 138 actual) and is logged for the same reason:
the instrument that proves nothing was lost has to be auditable itself.

Derivation of the baseline split. Phase 1 assigned CAP 27 · ROLE 85 · TMPL 16 · CP2 10 = 138. Of the
33 rules Option C retired, **24 were ROLE-owned** (C5–C11 group 5, D4–D6 3, G2–G9 group 6, H1–H6 6,
M1–M4 4) and **9 were CP2-owned** (O2–O12 group). No CAP-owned or TMPL-owned rule was retired. The
one surviving CP2 rule, `O1`, moved to ROLE when `cp2-blind-protocol.md` was deleted. So
ROLE 85 − 24 + 1 = **62**, CAP **27**, TMPL **16** → **105**, plus domain Q **23** → **128**.

| Owner | Baseline | New | Post-amendment | Note |
|---|---:|---:|---:|---|
| **CAP** `capstone_V6_6.md` §12 | 27 | +3 | **30** | The bar — gains E11, K11, K12 |
| **ROLE** `engineering-role.md` | 62 | +9 | **71** | The process — gains A11, B11, B12, C14–C16, E9, E10, I11 |
| **TMPL** `gauntlet-templates.md` | 16 | +8 | **24** | Forms + receipt gate — gains L12–L16, N8–N10, plus §9 landing and §10 `BRIEF_INVALID` |
| **AGENTS** `AGENTS.md` | 0 | +5 | **5** | New owner — R1–R5, the ref lifecycle |
| **ORCH** `orchestrator-role.md` | 23 | 0 | **23** | Newly enumerated (Q1–Q23); amended by G4, G7, G13 but gains no new ID |
| **Total** | **128** | **+25** | **153** | **0 retired** |

`I10` remains co-owned with `progress.md` as a cross-reference, counted once under CAP. Nine
co-ownerships persist from Phase 1 and are stated once in each place with an explicit cross-reference,
never restated in full.

## Rules that must not change — the overcorrection guard

The CP-0 run validated these operationally. Phase 2.3's review checks each is present and unweakened:

**B8** Builder never grades its own work · **B7** sole Git writer · **B5** Builders never touch Git ·
**C3** fresh clean detached worktree at the candidate SHA · **C4** Critic never receives the
Builder's story · **E1–E4** computed staleness (E2/E5/E6 take terminology only, never semantics) ·
**F1–F6** mandatory surfaces and the Critic-materializes-fixtures rule · **B1** verify real state
(extended by G10, never relaxed) · **K9** hard stop at every terminal return · **I6** parallel
contexts never sum.

## Verification protocol for Phase 2.3

1. Author G1 … G14.
2. For each of the **153** IDs, confirm presence in its assigned owner by normalized-whitespace
   substring match — the method that caught `G4` and `I9`.
3. Confirm no rule appears normatively outside its assigned owner (cross-references excepted).
4. Confirm every rule in the overcorrection guard is present and unweakened.
5. Confirm the 8 Option-C-reduced rules and the 33 retired ones are restated or struck in place
   (D-CP0-15), and that `engineering-role.md:56` is either re-ledgered or dropped (D-CP0-9).
6. Record the result here as a dated verification block, including any rule the pass had to restore.

**Judged by a fresh context that did not author the amendment.** Builder ≠ Critic applies to the
contract itself; the alternative is the authors certifying their own work, which the contract forbids
everywhere else.
