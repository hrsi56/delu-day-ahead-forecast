# Verdict — pit-capture-instrument — round 1

Status: PASS
Checkpoint: M0.5/CP-0
Candidate SHA: 7526310b9db81ff67b3d26ba03389c16af659027
Controlling plan: capstone_V6_5.md · v6.5 · §12 M0.5/CP-0 items 1-5 (+ §3, §4.0)
Bar excerpt (verbatim, verified present at this SHA, capstone_V6_5.md lines 456-461):
> **CP-0**
> - [ ] The instrument runs standalone, requires only `ENTSOE_API_TOKEN`, and writes an append-only ledger entry per attempt without mutating or overwriting any prior entry.
> - [ ] A failed, partial, or rate-limited request records a `not_qualifying` entry with its reason and never counts toward the three qualifying days (§3). A positive control proves a complete response records `qualifying`.
> - [ ] `pulled_at` is recorded in UTC and is the observed-available-by time; it is never rewritten as the source's first-publication time (§3).
> - [ ] Berlin DST is handled per §4.0: a capture in either 02:00 offset on a fall-back day resolves to a distinct UTC instant, and D+1 completeness is judged on the correct 23/24/25-hour day length.
> - [ ] Raw captures and ledger entries are hash-bound and immutable once written; a rerun cannot silently replace a prior attempt.

Artifact: scripts/pit_capture.py, src/pit_capture/**
Worktree clean before and after review: yes — `git status --porcelain` printed nothing and `git rev-parse HEAD` printed `7526310b9db81ff67b3d26ba03389c16af659027` both before and after the review. (Note: `uv run` created a gitignored `.venv/` and `src/pit_capture/__pycache__/` inside the worktree as a side effect of running the exact commands specified in the review brief from inside the worktree; both are covered by `.gitignore` and do not appear in `git status --porcelain`, so they do not affect this determination. No tracked file was touched.)

## What I inspected

- `capstone_V6_5.md` lines 65-84 (§3 point-in-time capture contract), 89-99 (§4.0 time indexing/DST), 446-472 (§12 M0.5/CP-0) — read directly in my worktree to confirm the bar text and supporting contract, not taken on trust from the brief.
- `scripts/pit_capture.py` (20 lines, full file) — thin entry point, `sys.path` shim, delegates to `pit_capture.cli.main`.
- `src/pit_capture/__init__.py` (34 lines, full file) — constants (`ENTSOE_API_TOKEN` is the only credential named anywhere), `PULLED_AT_SEMANTICS` string.
- `src/pit_capture/cli.py` (152 lines, full file) — argparse wiring for `capture`/`verify`; `capture` never crashes without a ledger row except on `UsageError` (bad `--at-utc`) or `LedgerError` (artifact-conflict refusal).
- `src/pit_capture/capture.py` (317 lines, full file) — `run_capture`: derives the window, performs the fetch (live/replay/injected `fetch_outcome`), writes the raw artifact (or aborts before appending), builds and appends the ledger entry. Verdict logic at lines 224-245: `qualifying = presence == "present_complete" and pre_gate and skew_ok and artifact_write_error is None`; `counts_toward_section_3_qualifying_days = bool(qualifying and outcome.capture_mode == "live")` (line 313-315) — replay/test captures can never count toward the three §3 qualifying days even if they qualify.
- `src/pit_capture/fetch.py` (166 lines, full file) — `FetchOutcome` dataclass (lines 31-48) confirmed as the real shape used to build the rate-limit driver; `fetch_live`/`fetch_replay` implementations; `_CapturingSession` keeps the raw response body even on an `HTTPError`/`NoMatchingDataError`.
- `src/pit_capture/ledger.py` (199 lines, full file) — `compute_entry_sha256` (canonical sorted-key JSON, `entry_sha256` key excluded from its own hash), `append_entry` (mode `"a"`, `fsync`), `write_raw_artifact` (refuses to overwrite a differing-bytes file, reuses identical bytes, atomic tmp-file + `os.replace` for new writes), `verify_ledger` (recomputes every row's hash, checks `entry_index`/`prev_entry_sha256` chain, re-hashes the raw artifact against `payload_sha256`).
- `src/pit_capture/parsing.py` (331 lines, full file) — `parse_a65_payload` (root-tag/TimeSeries/Period/Point walk, namespace-agnostic via local-name matching, literal-position honouring, no A03 gap-filling) and `assess_completeness` (DST-aware `expected_rows`/`expected_grid` sourced from `CaptureWindow`, `missing_slots` vs `null_slots` vs `points_outside_window` distinguished, `latest_fully_populated_timestamp_utc` capped at the first gap in the leading contiguous run).
- `src/pit_capture/timewindow.py` (154 lines, full file) — `parse_utc_instant` (rejects naive/non-UTC input), `derive_window` (Berlin local time via `zoneinfo`, gate at Berlin noon — never itself ambiguous since Berlin DST transitions occur at 02:00-03:00 local — `window_start/end_utc` from Berlin local midnight-to-midnight on the delivery day, `day_length_hours` asserted to be one of 23/24/25).
- I did not open `tests/` at all (per the brief's instruction that Builder-authored tests are insufficient evidence and must not be cited or copied from).

## Commands actually run

All fixtures hand-authored in `.../critic-fixtures/fixtures/*.xml` from my own reading of `parsing.py`, never copied from the candidate's `tests/`. Independent expectation computations (pure `zoneinfo`, no `pit_capture` import) live in `.../critic-fixtures/{find_dst_2026.py,compute_expectations.py,window_calc.py}` and were run and recorded in `.../critic-fixtures/EXPECTATIONS_BEFORE_RUN.md` **before** any of the commands below.

1. DST fact-finding (independent, stdlib-only): `python3 find_dst_2026.py` → exit 0. Output: Berlin 2026 spring-forward = 2026-03-29, fall-back = 2026-10-25 (both derived by scanning ambiguous/nonexistent local times via `zoneinfo`, not taken from any test or from the brief).

2. **Truncated response** (item 1 of the bar-comparison table below):
   `uv run --with entsoe-py==0.8.0 --with pandas --with requests python scripts/pit_capture.py capture --at-utc 2026-09-14T08:30:00Z --ledger .../run1_truncated/ledger.jsonl --raw-dir .../run1_truncated/raw --replay-xml .../fixtures/truncated_2026-09-15.xml --max-clock-skew-seconds 999999999 --json`
   → exit 0. Result: `observed_rows=80, expected_rows=96, missing_slots=16, presence=present_partial, verdict=not_qualifying` — matches my precomputed expectation exactly (window 2026-09-14T22:00Z→2026-09-15T22:00Z, 96 expected PT15M slots, fixture carries only positions 1-80).

3. **Rate-limit** (item 2, first half): `.../critic-fixtures/rate_limit_driver.py`, run as `uv run --with entsoe-py==0.8.0 --with pandas --with requests python rate_limit_driver.py <worktree>/src .../run2_ratelimit/ledger.jsonl .../run2_ratelimit/raw` → exit 0. My own 429 body (459 bytes, independently authored `Acknowledgement_MarketDocument`), independently hashed with `hashlib.sha256` **before** the call: `14840259f6b4a9e8c21ebc5a6d8e752cb0b3ac1bf4a3e151f262a5ee83aeaec8`. Constructed `FetchOutcome(capture_mode="live", http_status_code=429, status_detail="rate_limited", ...)` per the real dataclass shape read from `fetch.py`, and called `run_capture` directly. Result: entry written; `verdict=not_qualifying`; `payload_sha256` in the ledger == my precomputed hash (match); `http_status_code=429`; `status_detail=rate_limited`; `counts_toward_section_3_qualifying_days=false`; `raw_artifact_path` set and its on-disk bytes/hash both matched my exact 429 body byte-for-byte. All 9 driver-internal assertions printed `PASS`.

4. **Berlin fall-back, distinct instants** (item 4a): two captures against `fallback_instants_2026-10-26.xml`:
   `--at-utc 2026-10-25T00:30:00Z` (my precomputed UTC for Berlin 02:30 CEST, fold=0) → exit 0 → `pulled_at_utc=2026-10-25T00:30:00+00:00, local_pull_time=2026-10-25T02:30:00+02:00, utc_offset=+02:00`.
   `--at-utc 2026-10-25T01:30:00Z` (my precomputed UTC for Berlin 02:30 CET, fold=1) → exit 0 → `pulled_at_utc=2026-10-25T01:30:00+00:00, local_pull_time=2026-10-25T02:30:00+01:00, utc_offset=+01:00`.
   Both match my precomputation exactly: one hour apart, distinct UTC instants, same local clock reading, different offsets.

5. **Berlin fall-back, the delivery day itself** (item 4b): D-1 pull `--at-utc 2026-10-24T08:30:00Z` (my precomputed 10:30 CEST D-1) against two fixtures:
   - `fallback_full_2026-10-25.xml` (my own 100/100 PT15M fixture) → exit 0 → `delivery_date=2026-10-25, day_length_hours=25, expected_rows=100, observed_rows=100, missing_slots=0, presence=present_complete, verdict=qualifying`. Matches my precomputed 25h/100-slot expectation exactly (window 2026-10-24T22:00Z→2026-10-25T23:00Z, independently computed span 25.0h).
   - `fallback_short96_2026-10-25.xml` (same window, my own fixture with positions 97-100 dropped) → exit 0 → `expected_rows=100, observed_rows=96, missing_slots=4, presence=present_partial, verdict=not_qualifying` — correctly flagged as short, not misread as complete.

6. **`pulled_at` vs `createdDateTime`** (item 3): `--at-utc 2026-08-19T08:30:00Z` against `createdtime_2026-08-20.xml` (my own fixture with `createdDateTime=2026-08-01T00:00:00Z`, ~18 days before the pull) → exit 0 → `pulled_at_utc=2026-08-19T08:30:00+00:00` (== my supplied instant), `source_created_at_utc=2026-08-01T00:00:00+00:00` (== the fixture's own stamp), the two fields differ and neither is derived from the other.

7. **Standalone dependency check** (item 1, first half): `grep -rn "os\.environ\|getenv" src/pit_capture scripts/pit_capture.py` → single hit, `capture.py:90: os.environ.get("ENTSOE_API_TOKEN")`. A second grep for `config\.|Config\(|\.env` inside the same paths → no hits. No other credential/config dependency exists.

8. **Append-only** (item 1, second half): two sequential captures against the same `--ledger`/`--raw-dir` (`positive_control_2026-08-06.xml` then `truncated_2026-09-15.xml`) → both exit 0; ledger grew from 1 to 2 lines; `diff line1_before.txt line1_after.txt` → exit 0 (no output); `cmp line1_before.txt line1_after.txt` → exit 0. First line byte-for-byte unchanged.

9. **Hash-bound immutability, raw artifact** (item 5, first half): after the positive-control capture succeeded and wrote its raw artifact (sha256 `36717e1999ed...`), flipped one byte in that file on disk (new sha256 `b9c13a6ea3bc...`), then reran the identical `capture` command (same `--at-utc`, same `--replay-xml`, same `--ledger`/`--raw-dir`) → **exit 3**, stderr `ABORTED (no ledger entry written): refusing to overwrite existing raw artifact with different bytes: ... (existing sha256=b9c13a6ea3bc..., new sha256=36717e1999ed...)`. Ledger line count unchanged (still 1) — the rerun did not silently replace prior evidence.

10. **Hash-bound immutability, ledger row** (item 5, second half): restored the raw artifact to its original bytes; ran `verify` on the untouched ledger → exit 0, `entry 0 (line 1): OK`, `OK: 1 entries, 0 failing`. Then hand-edited one character inside that row's `"reason"` field (`complete` → `complXte`) directly in the JSONL file, re-ran `verify` → **exit 1**, `entry 0 (line 1): FAIL: entry_sha256 mismatch: recorded 87ce7c20..., recomputed 7ce3201e... (the row was edited after it was written)`, `FAILED: 1 entries, 1 failing`. The tampered row is correctly reported as failing, never as OK.

11. **Positive control** (item 2, second half): `--at-utc 2026-08-05T08:30:00Z` against my own full 96/96 `positive_control_2026-08-06.xml` → exit 0 → `presence=present_complete, verdict=qualifying, pulled_at_is_pre_gate=true`. (Bonus check, not itself a CP-0 item: `counts_toward_section_3_qualifying_days=false` for this same qualifying entry because `capture_mode=="replay"` — confirms replay can never itself count as a live B-Man-PIT day, which is the correct behavior for §3's "three qualifying days" to mean three *live* days.)

12. Final integrity re-check: `git -C <worktree> status --porcelain` → empty; `git -C <worktree> rev-parse HEAD` → `7526310b9db81ff67b3d26ba03389c16af659027`. Unchanged from the pre-review check.

## Bar comparison

| Criterion | Evidence | Result |
|---|---|---|
| 1. Standalone (`ENTSOE_API_TOKEN` only) + append-only, no mutation of prior entries | Command 7 (grep: only `ENTSOE_API_TOKEN` referenced anywhere in `src/pit_capture`/`scripts/pit_capture.py`); Command 8 (two sequential captures, ledger grew 1→2 lines, line 1 byte-identical before/after via `diff`/`cmp`) | PASS |
| 2. Failed/partial/rate-limited → `not_qualifying` with reason, never counts toward the 3 qualifying days; positive control → `qualifying` | Command 2 (truncated → `not_qualifying`, 80/96); Command 3 (429 → `not_qualifying`, `counts_toward_section_3_qualifying_days=false`, raw 429 body hash-bound and verified byte-for-byte); Command 11 (full 96/96 → `qualifying`) | PASS |
| 3. `pulled_at` recorded in UTC, is observed-available-by, never rewritten as source's first-publication time | Command 6: `pulled_at_utc` == my supplied `--at-utc` instant; `source_created_at_utc` == the fixture's own far-away `createdDateTime`; two distinct fields, never conflated | PASS |
| 4. Berlin DST: either 02:00 offset on a fall-back day → distinct UTC instant; D+1 completeness judged on correct 23/24/25h day length | Command 4 (02:30 CEST vs 02:30 CET → UTC instants 1h apart, distinct, same local clock reading, different offsets); Command 5 (fall-back delivery day itself independently computed as 25h/100-slot PT15M and confirmed exactly by the tool; a 96-slot fixture for the same day correctly flagged `missing_slots=4`, not misread as complete) | PASS |
| 5. Raw captures and ledger entries hash-bound and immutable; rerun cannot silently replace a prior attempt | Command 9 (byte-flipped raw artifact + identical rerun → refused, exit 3, ledger untouched); Command 10 (tampered `reason` field → `verify` reports that row `FAIL`, exit 1, not `OK`) | PASS |

## Non-blocking observations

- `run_capture`'s default `max_clock_skew_seconds` (120s) is tight enough that any `--at-utc` not within ~2 minutes of the real wall clock will itself force `not_qualifying` (via the `clock_skew_seconds` check at `capture.py:225-235`), independent of payload completeness. This is sound design for the live B-Man-PIT path (it catches an operator supplying the wrong instant) but means historical/offline `--replay-xml` runs must pass `--max-clock-skew-seconds` explicitly to test completeness/DST logic in isolation — which the CLI already supports and which I used throughout. Not a CP-0 gap; worth a one-line note in the instrument's own `--help` or README so a future B-Man-PIT operator isn't surprised by it.
- `counts_toward_section_3_qualifying_days` requires `capture_mode == "live"` in addition to `qualifying` (`capture.py:313-315`) — confirmed by Command 11 that a fully qualifying `--replay-xml` run still reports `false` here. This is the correct behavior (replay must never masquerade as one of the three live capture days) but is worth flagging explicitly since it's easy to misread the field name as tracking `verdict` alone.
- `uv run` (as specified by the review brief's own CLI instructions, executed from inside the worktree) created a gitignored `.venv/` and `src/pit_capture/__pycache__/`. Both are covered by `.gitignore`; `git status --porcelain` remains empty. Flagging only for completeness of the "worktree clean" attestation.
