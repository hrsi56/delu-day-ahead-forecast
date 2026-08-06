# Verdict — Integration — M0.5/CP-0

Status: PASS
Checkpoint: M0.5/CP-0
Candidate SHA: 12abbbd36dbc223ddb0133a8528547b908acddc6
Reviewed paths: the complete tree at this SHA — `src/pit_capture/`, `tests/pit_capture/`, `pyproject.toml`, `docs/track-b/evidence/cp-0/`, plus the controlling-plan and rule documents (`capstone_V6_6.md`, `docs/track-b/cp-0-defects.md`) read for context and cross-checked against the diff since the checkpoint's starting `main` tip
Controlling plan: `capstone_V6_6.md` · v6.6 · §12 M0.5/CP-0 complete checklist (+ §3, §4.0)
Bar excerpt (verbatim, verified present at this SHA — `capstone_V6_6.md` lines 461–473):
> The instrument performs one capture attempt for A65/A01 on DE-LU (`10Y1001A1001A82H`) at a supplied UTC instant and writes, to an append-only ledger: the immutable raw response, its SHA-256, `pulled_at` in UTC, the resolved Europe/Berlin local time, the delivery day D+1 it covers, whether that D+1 vector is complete under §4.0 DST rules, and an explicit `qualifying` / `not_qualifying` verdict with reason.
>
> **CP-0**
> - [ ] The instrument runs standalone, requires only `ENTSOE_API_TOKEN`, and writes an append-only ledger entry per attempt without mutating or overwriting any prior entry.
> - [ ] A failed, partial, or rate-limited request records a `not_qualifying` entry with its reason and never counts toward the three qualifying days (§3). A positive control proves a complete response records `qualifying`.
> - [ ] `pulled_at` is recorded in UTC and is the observed-available-by time; it is never rewritten as the source's first-publication time (§3).
> - [ ] Berlin DST is handled per §4.0: a capture in either 02:00 offset on a fall-back day resolves to a distinct UTC instant, and D+1 completeness is judged on the correct 23/24/25-hour day length.
> - [ ] Raw captures and ledger entries are hash-bound and immutable once written; a rerun cannot silently replace a prior attempt.
> - [ ] **Independent Critic PASS (mandatory):** a fresh Critic materializes its own fixtures outside the candidate checkout — including a truncated response, a rate-limit response, and a Berlin fall-back day — computes expected outcomes independently, and confirms each. Builder-authored tests are insufficient.
> - [ ] **Fresh Integration-Critic `PASS` at the exact `final_candidate_sha`/tree**, with the evidence tip above it containing verdict files only (`git diff --name-only <final_candidate_sha>..<evidence_tip_sha>` returns nothing outside `docs/track-b/evidence/<checkpoint>/`).

Artifact: `src/pit_capture/` (implementation), `tests/pit_capture/` (Builder tests), `docs/track-b/evidence/cp-0/pit-capture-round1.md` (component verdict)
Worktree clean before and after review: yes

## What I inspected

- `src/pit_capture/berlin_window.py` — pure DST-aware Europe/Berlin arithmetic derived from `zoneinfo` offsets, no hardcoded transition table.
- `src/pit_capture/capture.py` — `fetch_raw` (raw `requests.get`, deliberately not `entsoe-py`'s own request path), `classify` (pure function), `capture_attempt` (orchestration).
- `src/pit_capture/ledger.py` — hash-chained append-only JSONL ledger + content-addressed, chmod-0o444 raw-artifact store.
- `src/pit_capture/cli.py` — single entry point, one `os.environ` reference gating on `ENTSOE_API_TOKEN`.
- `docs/track-b/evidence/cp-0/pit-capture-round1.md` — the component Critic's verdict, read in full.
- `capstone_V6_6.md` §12 (M0.5 section) and its §3 / §4.0 supporting text.
- `pyproject.toml` diff; full repo diff-stat since the checkpoint's starting `main` tip (`a01275b`); `docs/track-b/cp-0-defects.md` for context confirming this candidate is a distinct clean-room re-run (different SHA lineage from the archived "attempt 1" that document discusses — that document's findings are process/contract defects already remedied in the v6.6 text this checklist is drawn from, not defects in this candidate).
- `tests/pit_capture/*.py` — read after building my own independent checks, for comparison only.

I built my own fixtures from scratch (own hand-authored XML, own scratch ledger, own scripts), entirely outside the worktree, in a private scratch directory, and computed expected values before invoking candidate code, for a DST fall-back check, a truncated-response check, a rate-limit check, a positive-control (complete response, pre-gate vs. post-gate) check, and a hash-chain/immutability check — reproducing 5 of the 5 bar-facing properties (items 1–5) independently, not merely reading the component verdict's prose.

## Commands actually run

```text
git status --porcelain && git rev-parse HEAD
→ exit 0, empty status, HEAD = 12abbbd36dbc223ddb0133a8528547b908acddc6
```

```text
grep -n "M0.5 — Point-in-time capture instrument" capstone_V6_6.md ; sed -n '453,473p' capstone_V6_6.md
→ exit 0. Text at lines 461-473 verbatim-matches the brief's blockquote, word for word.
```

```text
git diff --name-only 1a1defc6a856e1cfb748f7486eedfd2522b0cb09..12abbbd36dbc223ddb0133a8528547b908acddc6 -- src/pit_capture/ tests/pit_capture/
→ exit 0, EMPTY output — component PASS is not stale.
```

```text
git diff --stat a01275bddcbb081ca4377d799c7ebf9eafedbb7f..12abbbd36dbc223ddb0133a8528547b908acddc6
→ 12 files changed: docs/track-b/evidence/cp-0/pit-capture-round1.md, pyproject.toml,
  src/pit_capture/{__init__,berlin_window,capture,cli,ledger}.py,
  tests/pit_capture/{conftest,test_berlin_window,test_classify,test_ledger,test_live_smoke}.py
  — nothing outside the four expected areas.
```

```text
git diff a01275b..12abbbd -- pyproject.toml
→ packages = ["src/spike"] → ["src/spike", "src/pit_capture"]  (one line; src/spike diff is empty — untouched)
```

```text
/Users/djourno/Downloads/PJM/.venv/bin/python3 -c "find Sundays in Oct 2026"
→ Sundays: [4, 11, 18, 25]; last Sunday = 2026-10-25 (independently confirms the DST fall-back date)
```

```text
PYTHONPATH=src python3 -c "berlin_window.delivery_day_window_utc/expected_quarter_hour_count/local_hour_count/gate_at_utc/resolve_local for date(2026,10,25)"
→ window 2026-10-24T22:00Z..2026-10-25T23:00Z, qh=100, local_hours=25, gate=2026-10-24T10:00Z
  i1(00:30Z)→ local 02:30:00+02:00 is_dst=True ; i2(01:30Z)→ local 02:30:00+01:00 is_dst=False
  (matches the component verdict's independently-derived numbers exactly)
```

```text
PYTHONPATH=src python3 -c "own hand-built truncated (50/96 QH) GL_MarketDocument XML -> classify(...)"
→ status=present_partial, qualifying=False, reason=present_partial, observed=50/expected=96 → PASS
```

```text
PYTHONPATH=src python3 -c "classify(429, my-own-429-body, ...) and classify(500, ..., ...)"
→ 429 → status=request_error, qualifying=False, reason=rate_limited
  500 → status=request_error, reason=request_error (distinguishable from rate_limited) → PASS
```

```text
PYTHONPATH=src python3 -c "own hand-built complete (96/96 QH) XML -> classify at pre-gate and post-gate pulled_at"
→ pre-gate:  status=present_complete, qualifying=True,  reason=qualifying
  post-gate: status=present_complete, qualifying=False, reason=post_gate
  entry.pulled_at_utc == the exact instant passed in (never derived from the document) → PASS
```

```text
env -u ENTSOE_API_TOKEN PYTHONPATH=src python3 -m pit_capture.cli --pulled-at-utc ... --ledger-path .../ledger.jsonl --raw-dir .../raw
→ exit 1, RuntimeError: ENTSOE_API_TOKEN is not set...; find .../cli_test → no files created
grep -c "os.environ\|environ\[" src/pit_capture/*.py → cli.py:1, all others:0
```

```text
PYTHONPATH=src python3 -c "own scratch ledger.append_entry x2, hand-corrupt line 0, retry append, restore, retry, then write_raw_artifact + direct open('w') on the chmod'd file"
→ e1/e2 appended cleanly; corrupted-ledger append → ValueError "entry_hash does not match its own content";
  after restore, e3 appends and line0 stays byte-identical to e1;
  write_raw_artifact idempotent (same sha256 path on repeat write);
  direct open(path,'w') on the artifact → PermissionError: [Errno 13] Permission denied → PASS
```

```text
python3 -c "inspect.getsource(entsoe.entsoe.EntsoeRawClient._base_request)"
→ confirms entsoe-py's own request path raises typed exceptions (NoMatchingDataError etc.) via
  response.raise_for_status() and does not preserve the raw failure body on error paths — verifies
  fetch_raw's docstring claim (bypassing entsoe-py's own request path to preserve raw failure bodies)
  is literally true, not just asserted.
```

```text
git status --porcelain && python3 -m pytest tests/pit_capture/ -v -rs
→ exit 0, empty status before the run (clean worktree)
→ 14 passed, 3 skipped, 2 warnings
  SKIPPED: test_positive_control_real_complete_response... (fixtures/complete_response_sample.xml
    not captured — ENTSO-E in scheduled maintenance)
  SKIPPED x2: test_live_smoke.py (PIT_CAPTURE_RUN_LIVE_TESTS=1 not set)
```

```text
PYTHONPATH=src python3 -c "fetch_raw(date.today()-1day, os.environ['ENTSOE_API_TOKEN'])"
→ status=503, text[:800] = genuine HTML "Transparency Platform" maintenance page (not JSON/XML)
  — independently reproduces the live-maintenance condition claimed by the verdict and the skip
  reason, confirmed right now (2026-08-06), not merely trusted.
```

```text
grep -rniE "three.qualifying|reconcil|schedule|multi.?day|duckdb|SQL.?mart|CP-1|CP1|smard" src/pit_capture/ tests/pit_capture/
→ no matches except the skip-reason string "scheduled maintenance" — no M1/CP-1 data-layer or
  multi-day scheduling/reconciliation code present.
find docs/track-b/evidence -type f → only docs/track-b/evidence/cp-0/pit-capture-round1.md
```

```text
git log --oneline a01275b..12abbbd
→ 1a1defc "M0.5/CP-0: point-in-time capture instrument for A65/A01 (DE-LU)"
  12abbbd "M0.5/CP-0: component Critic verdict — pit-capture round 1 — PASS"
  (exactly two commits; the second adds only the verdict file — matches the brief's stated shape)
```

```text
git status --porcelain (final) && git rev-parse HEAD
→ exit 0, empty status, HEAD unchanged at 12abbbd36dbc223ddb0133a8528547b908acddc6
```

## Bar comparison

| Criterion | Evidence | Result |
|---|---|---|
| 1. Standalone, only `ENTSOE_API_TOKEN` required, append-only writes, no mutation of prior entries | Single `os.environ` reference in the whole package; CLI run with token unset exits 1 before any write, no ledger/raw files created; independent ledger append/corrupt/restore test shows sequential appends never touch prior lines | PASS |
| 2. Failed/partial/rate-limited → `not_qualifying` + reason; positive control → `qualifying` | My own truncated (50/96), 429, 500, and complete (96/96) fixtures, run directly against `classify`, all matched independently-computed expectations, including the rate_limited vs. request_error distinction and the pre-gate/post-gate split | PASS |
| 3. `pulled_at` in UTC, observed-available-by, never rewritten from response content | `classify`'s recorded `pulled_at_utc` equals the exact instant I passed in, byte-for-byte, independent of document contents; confirmed both in my own test and the component verdict's Check 6 | PASS |
| 4. Berlin DST per §4.0: distinct UTC instants for both 02:00 offsets on fall-back day; correct 23/24/25-hour D+1 completeness | Independently confirmed 2026-10-25 is the last Sunday of Oct 2026; independently ran `berlin_window` against it and got window/qh/local-hours/gate/offset values matching the component verdict's numbers exactly, computed from bare `zoneinfo` reasoning first | PASS |
| 5. Raw captures/ledger entries hash-bound and immutable; rerun cannot silently replace a prior entry | Independent scratch-ledger test: hand-corrupting a prior line causes `append_entry` to raise before writing; restoring and re-appending leaves the first entry byte-identical; raw artifact is genuinely OS-permission-denied on direct write (0o444), not just claimed | PASS |
| 6. Independent Critic PASS (mandatory) — fixtures outside candidate checkout, truncated + rate-limit + fall-back day, independently computed and confirmed | Read `docs/track-b/evidence/cp-0/pit-capture-round1.md` in full: PASS status, candidate SHA `1a1defc6...`, verbatim bar excerpt verified present, fixtures built outside the worktree, never copied from `tests/`, all three required fixture types present plus extras (500 vs. 429 distinction, gate-timing, orchestration path), exact commands with real output, explicit statement that expected values were computed before running candidate code and that `tests/pit_capture/*.py` was read only afterward for comparison. Not a rubber stamp — cross-checked its central DST claim and hash-immutability claim myself and got matching independent results | PASS |
| 7. Fresh Integration-Critic `PASS` at `final_candidate_sha`, evidence tip verdict-only | This review, at `12abbbd36dbc223ddb0133a8528547b908acddc6`; `git diff --name-only 1a1defc6..12abbbd36` shows the only change between the component-reviewed SHA and this final SHA is the addition of `docs/track-b/evidence/cp-0/pit-capture-round1.md` itself — verdict-only, staleness computation sound | PASS |

**Not applicable at this checkpoint** (stated per the brief, not silently skipped):
- Metrics recomputed from frozen predictions — no model/metrics artifact exists at M0.5/CP-0.
- Champion/benchmark schema firewall — no champion features touched by this checkpoint.
- A75 climatology fit lineage — no A75/fit code exists in this piece.
- CP-2 label-blind four-catalog review — this is not CP-2.
- M3 CQR threshold recomputation — this is not M3.

## Largest remaining gap

None that blocks this bar. The one genuine residual gap — the Builder's own positive-control test against a byte-for-byte real ENTSO-E payload has never run, because the live platform has been in scheduled maintenance for the entire build (independently reproduced: identical HTTP 503 / HTML maintenance page live during this review) — is explicitly designed around by the plan itself: CP-0 authors and reviews the instrument only, B-Man-PIT executes it for real on qualifying days, and CP-1 independently verifies the resulting ledger against real captured data. It is correctly non-blocking here and is already recorded as such in the component verdict.

## Exact next acceptance test

Once `web-api.tp.entsoe.eu` exits maintenance, B-Man-PIT should run the reviewed instrument (`python -m pit_capture.cli --pulled-at-utc ...`) at the two scheduled Berlin pre-gate times on at least three non-consecutive delivery days per §3, producing a ledger with three `qualifying` entries; CP-1's fresh Critic then independently verifies the ledger's hashes, UTC provenance, DST handling, and D+1 completeness, closing the one path (a real live payload) that has so far only been exercised against reconstructed-from-documentation fixtures.

## Non-blocking observations

- `classify`'s gate check is strict `pulled_at_utc < gate` (not `<=`); an attempt landing at the exact gate instant is `post_gate`. This is a defensible reading of "before 12:00" and is worth keeping in mind for B-Man-PIT's scheduling margin, but is not a defect.
- `docs/track-b/cp-0-defects.md` (pre-existing, untouched by this candidate) documents that this checkpoint is a clean-room re-run superseding an earlier, differently-SHA'd "attempt 1" that was reviewed but never landed to `main` under a since-amended contract. That document's findings are about the Gauntlet contract/process, explicitly not about any capstone bar, and none of them bear on this candidate's correctness.
- The component verdict's fixture generator is a hand-built approximation of the real ENTSO-E `GL_MarketDocument` schema, sanity-checked against the real `entsoe.parsers.parse_loads` before use — reasonable rigor given the live-maintenance constraint, but its accuracy relative to the real API's actual payload shape remains formally unconfirmed until B-Man-PIT/CP-1.
