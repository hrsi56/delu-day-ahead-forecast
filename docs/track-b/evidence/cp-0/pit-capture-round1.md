# Verdict — pit-capture — round 1

Status: PASS
Checkpoint: M0.5/CP-0
Candidate SHA: 1a1defc6a856e1cfb748f7486eedfd2522b0cb09
Reviewed paths: src/pit_capture/, tests/pit_capture/
Controlling plan: capstone_V6_6.md · v6.6 · §12 M0.5/CP-0 (+ §3, §4.0)
Bar excerpt (verbatim, verified present at this SHA — `capstone_V6_6.md` lines 461-471):
> The instrument performs one capture attempt for A65/A01 on DE-LU (`10Y1001A1001A82H`) at a supplied UTC instant and writes, to an append-only ledger: the immutable raw response, its SHA-256, `pulled_at` in UTC, the resolved Europe/Berlin local time, the delivery day D+1 it covers, whether that D+1 vector is complete under §4.0 DST rules, and an explicit `qualifying` / `not_qualifying` verdict with reason.
>
> **CP-0**
> - [ ] The instrument runs standalone, requires only `ENTSOE_API_TOKEN`, and writes an append-only ledger entry per attempt without mutating or overwriting any prior entry.
> - [ ] A failed, partial, or rate-limited request records a `not_qualifying` entry with its reason and never counts toward the three qualifying days (§3). A positive control proves a complete response records `qualifying`.
> - [ ] `pulled_at` is recorded in UTC and is the observed-available-by time; it is never rewritten as the source's first-publication time (§3).
> - [ ] Berlin DST is handled per §4.0: a capture in either 02:00 offset on a fall-back day resolves to a distinct UTC instant, and D+1 completeness is judged on the correct 23/24/25-hour day length.
> - [ ] Raw captures and ledger entries are hash-bound and immutable once written; a rerun cannot silently replace a prior attempt.

(§3 and §4.0 supporting excerpts, lines 81/83/93, also confirmed verbatim present via `grep -n` against this SHA.)

Artifact: src/pit_capture/
Worktree clean before and after review: yes

## What I inspected

- `src/pit_capture/berlin_window.py` — pure DST-aware date arithmetic (no hardcoded transition-date table; derives everything from `zoneinfo` offsets).
- `src/pit_capture/capture.py` — `fetch_raw` (real HTTP GET, bypassing entsoe-py's own request path specifically to preserve raw failure bodies), `classify` (pure, no I/O — the function a Critic calls directly against fixtures), `capture_attempt` (orchestrates fetch → classify → raw-artifact write → ledger append).
- `src/pit_capture/ledger.py` — hash-chained append-only JSONL ledger (`_verify_chain` re-verifies the entire existing chain before every append) and a content-addressed, chmod-0o444 raw-artifact store.
- `src/pit_capture/cli.py` — single entry point, `ENTSOE_API_TOKEN` env-var gate before any I/O.

Fixtures built entirely by me under `/private/tmp/critic-pit-capture-fixtures/` (never inside the worktree, never copied from `tests/pit_capture/`):
- `build_fixtures.py` — a from-scratch ENTSO-E `GL_MarketDocument` (A65/A01) XML generator, built from my own knowledge of the public ENTSO-E Transparency Platform document schema (`TimeSeries`/`Period`/`Point[position,quantity]`, UTC `Z`-suffixed `start`/`end`), with a configurable subset of quarter-hour positions (for truncation) and a genuine `Acknowledgement_MarketDocument` "no data" shape. I sanity-checked this fixture against the real `entsoe.parsers.parse_loads` (a real third-party library, not candidate code) before using it in any check — it parsed into a full 96-row `DataFrame` as expected.
- `check1_truncated.py` … `check6_pulled_at.py`, `check_orchestration.py` — one script per check, each computing its expected result independently before invoking candidate code.

I computed all expected values (row counts, gate times, DST offsets, fall-back date) independently in scratch Python before ever running the candidate's functions, per the brief's requirement, and only looked at `tests/pit_capture/*.py` afterward, for comparison.

## Commands actually run

```text
git -C /Users/djourno/Downloads/PJM-gauntlet/cp-0/critic-pit-capture-round1 status --porcelain
git -C /Users/djourno/Downloads/PJM-gauntlet/cp-0/critic-pit-capture-round1 rev-parse HEAD
→ exit 0, empty status, HEAD = 1a1defc6a856e1cfb748f7486eedfd2522b0cb09
```

```text
/Users/djourno/Downloads/PJM/.venv/bin/python3 -c "<independent last-Sunday-of-Oct-2026 + zoneinfo fold check>"
→ exit 0
Sundays in Oct 2026: [10-04, 10-11, 10-18, 10-25]; Last Sunday: 2026-10-25
fold0 2026-10-25 02:30:00+02:00 → UTC 2026-10-25T00:30:00Z
fold1 2026-10-25 02:30:00+01:00 → UTC 2026-10-25T01:30:00Z
start_utc 2026-10-24T22:00Z, end_utc 2026-10-25T23:00Z, span 25.0h / 100 quarter-hours
```
Independently confirms the brief's 2026-10-25 fall-back claim and derives 25h/100QH from the raw UTC span, not from any candidate formula.

```text
/Users/djourno/Downloads/PJM/.venv/bin/python3 <berlin_window sanity against my independent numbers>
→ exit 0
expected_qh=100, local_hours=25, window=(2026-10-24T22:00Z,2026-10-25T23:00Z), gate_at_utc=2026-10-24T10:00Z
i1(2026-10-25T00:30Z) → {'local_iso':'...02:30:00+02:00','utc_offset':'+02:00','is_dst':True}
i2(2026-10-25T01:30Z) → {'local_iso':'...02:30:00+01:00','utc_offset':'+01:00','is_dst':False}
```
Matches my independent derivation exactly.

```text
/Users/djourno/Downloads/PJM/.venv/bin/python3 /private/tmp/critic-pit-capture-fixtures/check1_truncated.py
→ exit 0
status: present_partial
qualifying: False, qualifying_reason: present_partial
expected_row_count: 96, observed_row_count: 86, completeness_ratio: 0.895833...
CHECK 1 PASS
```
Delivery day 2026-08-06 (ordinary 24h day). I removed 10 of 96 quarter-hour positions from my own XML fixture; independently expected 96 (24×4) and 86 observed. Candidate matched exactly, reason traceable to "partial".

```text
/Users/djourno/Downloads/PJM/.venv/bin/python3 /private/tmp/critic-pit-capture-fixtures/check2_rate_limited.py
→ exit 0
status: request_error, qualifying: False, qualifying_reason: rate_limited
500 status: request_error, reason: request_error
CHECK 2 PASS / CHECK 2b PASS
```
HTTP 429 fixture → `not_qualifying` with reason `rate_limited`, distinguishable from a generic 500's reason `request_error` and never conflated with `absent`.

```text
/Users/djourno/Downloads/PJM/.venv/bin/python3 /private/tmp/critic-pit-capture-fixtures/check3_fallback.py
→ exit 0
independently confirmed fall-back delivery date: 2026-10-25
independent UTC span (hours): 25.0
candidate berlin_window matches independent derivation: local_hours=25, qh=100
i_cest -> {'local_iso': '2026-10-25T02:30:00+02:00', 'utc_offset': '+02:00', 'is_dst': True}
i_cet  -> {'local_iso': '2026-10-25T02:30:00+01:00', 'utc_offset': '+01:00', 'is_dst': False}
CHECK 3(a)+3(b) PASS
entry.expected_row_count: 100, entry.observed_row_count: 100, status: present_complete, qualifying: True
CHECK 3(c) PASS
```

```text
/Users/djourno/Downloads/PJM/.venv/bin/python3 /private/tmp/critic-pit-capture-fixtures/check4_gate_timing.py
→ exit 0
independently-expected gate: 2026-08-05 10:00:00+00:00  (== Berlin noon CEST D-1)
PRE-GATE  status: present_complete qualifying: True  reason: qualifying
AT-GATE   status: present_complete qualifying: False reason: post_gate
POST-GATE status: present_complete qualifying: False reason: post_gate
CANDIDATE ENFORCES GATE TIMING: post-gate complete response is NOT qualifying.
```
Same complete XML fixture, three different `pulled_at` instants. The candidate does enforce the §3 pre-gate timing condition (`classify` compares `pulled_at_utc < gate_at_utc(...)`), not just completeness — this closes the gap the brief flagged as a possibility to check for.

```text
/Users/djourno/Downloads/PJM/.venv/bin/python3 /private/tmp/critic-pit-capture-fixtures/check5_immutability.py
→ exit 0
TEST A PASS: first entry byte-identical after second append
TEST B PASS: append correctly refused on hand-corrupted ledger (ValueError: entry_hash does not match its own content)
TEST C PASS: duplicate raw payload write is idempotent, no overwrite
TEST D PASS: raw artifact mode = 0o444 (no write bits for owner/group/other)
TEST E PASS: OS refused direct write to the read-only raw artifact ([Errno 13] Permission denied)
```
Scratch ledger built entirely outside the worktree at `/private/tmp/critic-pit-capture-fixtures/scratch_ledger/`. Test E is a real OS-level write attempt against the chmod'd file (not just an inspection of mode bits) — genuinely refused, confirming immutability is enforced, not just claimed.

```text
grep -n "open(\|\.write_text(\|write_bytes(" src/pit_capture/*.py
→ ledger.py:103  open(ledger_path, "a", ...)      [append, non-truncating]
→ ledger.py:145  os.fdopen(fd, "wb")               [brand-new tempfile.mkstemp fd, not an existing file]
```
No code path opens an existing artifact/ledger file in truncating `'w'` mode.

```text
/Users/djourno/Downloads/PJM/.venv/bin/python3 /private/tmp/critic-pit-capture-fixtures/check6_pulled_at.py
→ exit 0
passed in : 2026-08-05T07:13:42.123456+00:00
recorded  : 2026-08-05T07:13:42.123456+00:00
CHECK 6 PASS / CHECK 6b PASS (explicit +02:00 offset input converts correctly, still byte-identical instant)
```
XML fixture embedded a `createdDateTime`/period start far from `pulled_at`; the recorded `pulled_at_utc` is exactly and only the value I passed in.

```text
env -u ENTSOE_API_TOKEN PYTHONPATH=src /Users/djourno/Downloads/PJM/.venv/bin/python3 -m pit_capture.cli --pulled-at-utc 2026-08-05T09:00:00Z --delivery-date 2026-08-06 --ledger-path .../ledger.jsonl --raw-dir .../raw
→ exit 1
RuntimeError: ENTSOE_API_TOKEN is not set in the environment; refusing to run (no partial ledger write).
find .../scratch_cli_run/ → only the empty parent dir; no ledger.jsonl, no raw/ created
```
Fails fast, before any write, with a clear message; confirmed by both reading `cli.py` (only one `os.environ` reference in the whole package) and by executing it with the var unset.

```text
/Users/djourno/Downloads/PJM/.venv/bin/python3 /private/tmp/critic-pit-capture-fixtures/check_orchestration.py
→ exit 0
attempt 1: present_complete True qualifying .../raw/9a6b0631....xml
attempt 2: present_complete True qualifying .../raw/9a6b0631....xml
PASS: sequential real capture_attempt calls append without mutating prior entry
PASS: raw artifact written read-only via full orchestration path (mode 0o444)
PASS: hash chain correctly links attempt 2 to attempt 1 (entry_seq 0,1; prev_entry_hash chains)
```
Extra check beyond the brief's seven, exercising `capture_attempt` itself (not just the pure `classify`) with `fetch_raw` monkeypatched to avoid network — confirms the full write path, not only the pure-function path.

```text
PIT_CAPTURE_RUN_LIVE_TESTS=1 /Users/djourno/Downloads/PJM/.venv/bin/pytest tests/pit_capture/test_live_smoke.py -v -s
→ exit 1 (2 failed)
Both assert entry.status == "request_error" instead of "absent"/"present_complete"
```
Followed up by calling `fetch_raw` directly against the real API:
```text
status: 503
text[:1500]: <!doctype html>...<title>Transparency Platform</title>...
```
The real ENTSO-E Transparency Platform is currently in scheduled maintenance (a genuine HTML maintenance page, not JSON/XML). This is a live-environment condition, not a candidate defect — `classify` correctly routed the 503 to `request_error` rather than misreporting it as `absent` or `present_complete`, which is itself a correct outcome. This independently corroborates the exact same failure the Builder's own test-skip comment documents (`tests/pit_capture/test_classify.py` lines 19-27: "HTTP 503, 'Scheduled maintenance is currently underway'").

```text
PYTHONPATH=src /Users/djourno/Downloads/PJM/.venv/bin/python3 -m pytest tests/pit_capture/ -v
→ exit 0, 14 passed, 3 skipped (1 positive-control fixture missing + 2 live tests)
```
Informational only, run after my own independent checks, not relied on as evidence.

## Bar comparison

| Criterion | Evidence | Result |
|---|---|---|
| Standalone, only `ENTSOE_API_TOKEN` required, append-only writes | `grep` shows one env-var reference in the whole package; CLI run with token unset exits 1 pre-write, no ledger/raw files created | PASS |
| Failed/partial/rate-limited → `not_qualifying` with reason; positive control → `qualifying` | Checks 1, 2, 4 (pre-gate case) | PASS |
| `pulled_at` in UTC, observed-available-by time, never rewritten from response content | Check 6 (a and b) | PASS |
| Berlin DST per §4.0: distinct UTC instants for both 02:00 offsets on fall-back day; correct 23/24/25-hour D+1 completeness | Check 3 (independently-verified 2026-10-25, all three sub-parts) | PASS |
| Raw captures/ledger entries hash-bound and immutable; rerun cannot silently replace a prior attempt | Check 5 (A–E) + orchestration check | PASS |

## Largest remaining gap

Not a code defect, but a genuine residual verification gap: the Builder's own positive-control test against a **real** captured ENTSO-E response (`tests/pit_capture/fixtures/complete_response_sample.xml`) has never actually run — the fixture file doesn't exist, and the test is `skipif`'d with a documented reason (ENTSO-E was in maintenance for the entire build session). I independently reproduced this exact same 503/maintenance condition live during this review (see the `fetch_raw` call above), so this isn't a stale claim — it's still true right now. My own check 3(c)/4 positive-control passes, but against a schema I hand-built from public documentation and validated only against the real `entsoe.parsers.parse_loads` function, not against a byte-for-byte real API payload. This is inherent to the M0.5/CP-0 vs. B-Man-PIT split the plan itself designs (§12: CP-0 authors+reviews the instrument; B-Man-PIT executes it for real; CP-1 verifies the resulting ledger), so it does not block CP-0 on its own bar — but it means the "real response shape" assumption baked into both my fixture and the Builder's synthetic ones remains formally unconfirmed against a live payload until B-Man-PIT actually runs.

## Exact next acceptance test

As soon as `web-api.tp.entsoe.eu` is out of maintenance, run `PIT_CAPTURE_RUN_LIVE_TESTS=1 pytest tests/pit_capture/test_live_smoke.py -v -s` (or manually call `fetch_raw(date.today() - timedelta(days=1), token)` and feed the result through `classify`) and confirm `status == "present_complete"` with `observed_row_count == expected_row_count` for a real, fully-elapsed day — this closes the one path that has only ever been exercised against a reconstructed-from-documentation fixture, never a genuine live payload.

## Non-blocking observations

- `classify`'s gate check uses strict `pulled_at_utc < gate` (not `<=`); an attempt landing at the exact gate instant is `post_gate`/not-qualifying. This is the correct reading of the bar's "present before 12:00" wording, but worth noting as a deliberate boundary choice.
- The rate-limit/generic-error distinction lives only in `qualifying_reason` (`rate_limited` vs `request_error`); the coarser `status` enum field itself does not distinguish them, consistent with §3's four-value enum (`present_complete`/`present_partial`/`absent`/`request_error`) which has no separate rate-limit state.
