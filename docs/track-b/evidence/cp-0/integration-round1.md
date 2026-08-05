# Verdict — M0.5/CP-0 Integration — round 1

Status: PASS
Checkpoint: M0.5/CP-0
Candidate SHA: 63ebfaba701fbe54e5533170ac89c08204184446
Controlling plan: capstone_V6_5.md · v6.5 · §12 M0.5/CP-0 (all 7 items) + §3 + §4.0
Bar excerpt (verbatim, verified present at this SHA, capstone_V6_5.md lines 459-466):
> **CP-0**
> - [ ] The instrument runs standalone, requires only `ENTSOE_API_TOKEN`, and writes an append-only ledger entry per attempt without mutating or overwriting any prior entry.
> - [ ] A failed, partial, or rate-limited request records a `not_qualifying` entry with its reason and never counts toward the three qualifying days (§3). A positive control proves a complete response records `qualifying`.
> - [ ] `pulled_at` is recorded in UTC and is the observed-available-by time; it is never rewritten as the source's first-publication time (§3).
> - [ ] Berlin DST is handled per §4.0: a capture in either 02:00 offset on a fall-back day resolves to a distinct UTC instant, and D+1 completeness is judged on the correct 23/24/25-hour day length.
> - [ ] Raw captures and ledger entries are hash-bound and immutable once written; a rerun cannot silently replace a prior attempt.
> - [ ] **Independent Critic PASS (mandatory):** a fresh Critic materializes its own fixtures outside the candidate checkout — including a truncated response, a rate-limit response, and a Berlin fall-back day — computes expected outcomes independently, and confirms each. Builder-authored tests are insufficient.
> - [ ] Fresh Integration-Critic `PASS` at the exact final candidate SHA/tree.
Artifact: scripts/pit_capture.py, src/pit_capture/**, docs/track-b/evidence/cp-0/pit-capture-instrument-round1.md
Worktree clean before and after review: yes

## What I inspected

- `capstone_V6_5.md` §3 (lines 65-84, point-in-time capture contract), §4.0 (lines 89-93, time indexing/DST), §12 M0.5/CP-0 (lines 446-473) — read directly, not from paraphrase.
- `docs/track-b/evidence/cp-0/pit-capture-instrument-round1.md` — full file (component verdict).
- Full source: `scripts/pit_capture.py`, `src/pit_capture/__init__.py`, `capture.py`, `cli.py`, `fetch.py`, `ledger.py`, `parsing.py`, `timewindow.py`.
- `pyproject.toml`, `tests/` directory listing.
- Git topology: `git log --oneline --graph --all`, `git branch -a -v`, `git for-each-ref`, `git symbolic-ref -q HEAD`.

## Commands actually run

All ledger/raw output routed to a scratch directory outside the worktree; worktree re-checked clean after every command.

1. `git status --porcelain` → empty; `git rev-parse HEAD` → matches candidate SHA (repeated at end, unchanged).
2. `git symbolic-ref -q HEAD` → exit 1, confirming genuinely detached HEAD.
3. `git log --oneline -3` → `63ebfab` → `7526310` → `d7bdd5f`. Linear, no merge commit.
4. `git merge-base --is-ancestor 7526310 63ebfab` → true.
5. `git diff --name-only 7526310..63ebfab -- scripts/pit_capture.py src/pit_capture tests pyproject.toml` → empty.
6. `git diff --stat d7bdd5f..63ebfab` → touches only `pyproject.toml`, `scripts/pit_capture.py`, `src/pit_capture/**`, `tests/**`, `docs/track-b/evidence/cp-0/pit-capture-instrument-round1.md`. No M1/CP-1/B-Man-PIT scope creep.
7. `uv run --with entsoe-py==0.8.0 --with pandas --with requests --with pytest pytest tests/ -q` → 42 passed, exit 0.
8. Live-fixture capture via `--replay-xml` at the documented example instant → `presence=present_complete`, `verdict=not_qualifying` (real wall-clock skew, as documented); with `--max-clock-skew-seconds` override → `verdict=qualifying`, `pulled_at_is_pre_gate=true`.
9. Same against the truncated fixture → `presence=present_partial`, `verdict=not_qualifying`, `80/96`.
10. `verify` on that ledger → `OK: 1 entries, 0 failing`.
11. Independent tamper tests: edited ledger row text → `verify` reports `FAIL: entry_sha256 mismatch`, exit 1; flipped one byte of the raw artifact then reran the identical capture → `ABORTED (no ledger entry written): refusing to overwrite existing raw artifact with different bytes`, exit 3, ledger untouched.
12. Independent append-only check: two captures into the same ledger, line 1 byte-identical before/after (`diff` empty).
13. Independent stdlib-only (`zoneinfo`, no `pit_capture` import) DST fact-check: Berlin 2026 fall-back transition at `2026-10-25T01:00:00+00:00`; `2026-10-25T00:30:00Z`/`2026-10-25T01:30:00Z` both render Berlin local `02:30` at offsets `+02:00`/`+01:00`; delivery-day window for 2026-10-25 independently computed as `2026-10-24T22:00Z → 2026-10-25T23:00Z`, span 25.0h/100 PT15M slots — matches the code exactly.
14. Credential-surface grep: only `ENTSOE_API_TOKEN` referenced anywhere in the owned paths; no other config/credential dependency.
15. Dangling-reference sweep of CP-0-owned paths: none found.
16. Final re-check: `git status --porcelain` empty; `HEAD` unchanged.

## Bar comparison

| Criterion | Evidence | Result |
|---|---|---|
| 1. Standalone (`ENTSOE_API_TOKEN` only) + append-only, never mutates prior entries | Command 14; `ledger.py` `append_entry` (mode `"a"`, fsync, never reads-to-modify); Command 12 | PASS |
| 2. Failed/partial/rate-limited → `not_qualifying` w/ reason, never counts toward 3 days; positive control → `qualifying` | Command 8 (qualifying path); Command 9 (partial → not_qualifying); component verdict's independent rate-limit reproduction (re-verified: candidate paths unchanged since that review) | PASS |
| 3. `pulled_at` recorded in UTC, observed-available-by, never rewritten as first-publication time | `__init__.py` `PULLED_AT_SEMANTICS`; `capture.py` keeps `source_created_at_utc` as a wholly separate field; component verdict's independent reproduction, re-verified against unchanged source | PASS |
| 4. Berlin DST: either 02:00 offset on a fall-back day → distinct UTC instant; D+1 completeness on correct 23/24/25h day length | Command 13, fully independent stdlib computation, matches `timewindow.py` exactly | PASS |
| 5. Raw captures and ledger entries hash-bound and immutable; rerun cannot silently replace a prior attempt | Command 11, both tamper cases reproduced directly | PASS |
| 6. Independent Critic PASS (component verdict) | `docs/track-b/evidence/cp-0/pit-capture-instrument-round1.md`: Status PASS, candidate SHA confirmed an ancestor of final with empty reviewed-path diff (Commands 4-5), fixtures genuinely hand-authored outside the candidate checkout and computed before execution, `tests/` never opened or cited. One cosmetic defect: its bar-excerpt line citation (456-461) is off by 3 from the actual 459-464 — text itself is verbatim-correct. Non-blocking | PASS |
| 7. Fresh Integration-Critic PASS at final SHA/tree | This review | PASS |

**Process/topology sanity:** `d7bdd5f → 7526310 → 63ebfab` is linear, no merge commit; worktree HEAD is genuinely detached; `main` sits untouched at `d7bdd5f`. A sibling branch `claude/gauntlet-loop-article-19d7ae` @ `b8b70e6` branches from the same base roughly one minute after the candidate's instrument commit and records a **separate, earlier, correctly-refused** CP-0 brief attempt (2 of 10 required fields) plus a five-item structural-defects ledger (`docs/track-b/cp-0-defects.md`) in the Gauntlet contract itself. It shares no commits with this candidate beyond the common base, does not touch the reviewed paths, and explicitly states "no bar, checklist item, invariant, or acceptance criterion changed." It does not affect this PASS. It gates **CP-1** planning (not CP-0, and not B-Man-PIT) behind a governance amendment — outside this checkpoint's scope, but material for the Orchestrator to reconcile.

## Largest remaining gap

None on the CP-0 bar itself. The one open thread is process-level: the sibling branch's defects ledger explicitly invites this checkpoint's Return Packet to append operational findings before it closes — see the Return Packet's addendum.

## Exact next acceptance test

None required for CP-0 closure. Before CP-1 is briefed, the Orchestrator adjudicates `docs/track-b/cp-0-defects.md` D-CP0-1..5 per `progress.md`'s Blockers entry.

## Non-blocking observations

- Component verdict's bar-excerpt line citation is off by 3 lines (cosmetic).
- `run_capture`'s default 120s clock-skew bound means a `--replay-xml` run whose `--at-utc` isn't within ~2 minutes of the real wall clock reports `not_qualifying` regardless of completeness unless `--max-clock-skew-seconds` is passed explicitly — sound, documented design, reproduced directly, not a gap.
