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
