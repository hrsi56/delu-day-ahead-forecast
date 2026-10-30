# Capstone v21-r18 → v21-r19 — the issuing host on a GitHub runner, and a publication time that is not a claim

**Owner authority, 2026-10-30.** The Owner's decisions 22–25 are recorded in
`docs/track-b/owner-decisions-2026-10-30.md`, SHA-256
`1286548362b5618e3fb01c616d673c0af83dd79effeaf102bb9727ac219aabab`.
- **Decision 25 grants the authority.** It covers "the Lockdown suspensions each named step needs", among
  them "`capstone_v21.md` and its amendment record for r19". The Orchestrator runs these steps "without
  asking again".
- **His words with it:** "רוץ באופן עצמאי כל עוד אין בעיות חדשות שצצות החלטות משמעותיות אני מאשר לך
  לפעול עצמאית לחלוטין" ("Run independently. Unless new problems or significant decisions come up, I
  authorize you to act fully on your own.").
- **Decision 24** let the Orchestrator choose between Linux and macOS once a runner passed cleanly.
  CP-17c-probe landed on 2026-10-30 with both runners passing cleanly.

**The scope of the suspension.** It covers four things:
- `capstone_v21.md`;
- this amendment record;
- the directly necessary consistency edits to `progress.md`;
- the commit and push of these files to `main`.

It ends at this task's terminal return. It does not authorize:
- any other governance file, `AGENTS.md` and `docs/PUBLISH_RULES.md` included;
- a change to any code, test, frozen record, verdict or freeze;
- publication;
- opening 4.7T or any other checkpoint.

**The base:** r18 at `e9423ea5:capstone_v21.md`, SHA-256
`9caf83393a08df6851f7e829722583a142ebc2354ee99a3bbaa015d929f3d401`. When this revision was applied,
`main` was `7812e091`, CP-17c-probe's closure, on top of its landing `a92e0525`.

| Scope | r18 | r19 |
|---|---|---|
| The issuing host | the Homebrew Node.js v26.7.0 binary `1ef99ea2…` on the Owner's Mac; any other binary or machine is a runtime change (§24.12) | from CP-17c's landing on, the official Node.js v26.7.0 darwin-arm64 binary `a9bd0630…`. It runs on a GitHub-hosted `macos-26` runner for the daily product, and on the Owner's Mac for 4.7T and local runs. A machine that passes the checks is not a runtime change. The pins, the binary, the machine and a canary fit are checked before each run's first issuance (§24.13; H1, H2) |
| The publication time | "before 12:00 local"; "a late forecast is recorded as late" (§24.4); "numeric origin/deadlines" (§16.2) | no deadline and no "late" label. The cutoff is unchanged at D−1 11:00 Berlin, strictly before. Availability is judged by publication time against the cutoff, never by the run time. The run time stays in the lineage, and the panel states the last training (§24.13; decision 22) |
| CP-19's count | "real timely forecasts and failures" (§16.4) | issued and not-issued delivery days (§24.13; decision 22) |
| Missed days | — | a catch-up in order within a three-day lookback, at most four issuances per run. The ceilings bound a run at about 4¼ hours, not decision 23's "about an hour"; measured, about 21 minutes (§24.13; decision 23) |
| A1's policy identity for 4.7T | CP-17b's `439115fb…` | CP-17c's, which also fixes R7's `schema.py` defect on its error path only. CP-17c's landing record states the values 4.7T's brief cites. If CP-17c cannot land, 4.7T waits for the Owner (§24.13; H3) |
| S_14 | "under the same phase and rules" (§24.9) | natively on the Owner's M3, the machine that ran S_13 (§24.13; H4) |
| 4.7T's other terms, its calendar, its ceiling and no cloud | §24.12 | unchanged |

**What changes in the file:**
- **A new authority notice** at the top. r18's title gains "Historical", and a separating rule is
  inserted.
- **A new §24.13** at the end.

**What does not change:**
- **Everything else below the new notice** stays byte for byte: the historical headers, §§1–23 and
  §§24.1–24.12. So CP-26's test of §§1–23 against r13 (`tests/test_cp26_repair_contract.py`) still
  holds.
- **No frozen record.** CP-17b's freeze, its 4.7T protocol, the verdicts and the landing records stay as
  committed. §24.13 supersedes two frozen sentences on daily operation, for CP-18, and names them: the
  protocol's "issued at 11:00 local, before the 12:00 gate", and the freeze record §11's "issued at 11:00
  local". It also reads the protocol's references to CP-17b's freeze manifest and freeze identity as
  CP-17c's, from CP-17c's landing.
- **No governance file besides this one and the anchor.** `AGENTS.md`'s daily-update exception needs no
  change (§24.13).
- **The checks.** CP-17b's `refreeze verify` reads its governance pins from frozen copies, so this
  revision leaves it green, as r18 did.

## How it was checked

The records are in `.local/artifacts/r19/`, which Git ignores (`/.local/`), so they are cited by hash.

| Record | SHA-256 | Result |
|---|---|---|
| The plan critic's brief, `plan-critic-brief.md` | `70f8e81be23666fee03df6e7d66036a4586b9ba9dd3fb2c4ba43a90daa27839f` | — |
| The first candidate: the anchor, with its record `aae87d8d…`. Both were rewritten in place after the review | `ba466946c46f6f900ba46b8d8022e5e545483cbcecc9143e2a582427acbb1bd9` | — |
| The review, `plan-critic-review.md` | `db493eaf194d2423260efaad5171c3917667e6bbd1ee0fb346ab1d7e892301cc` | READY WITH FIXES: 0 blocking, 6 major, 11 minor. Every hash, quote and figure matched its source, and no CI step was at risk |
| The second candidate: the anchor, with its record `0dd4f855…` | `acb9ba6a701c1a4c0dfb720690c3227c0778f29014f4378bceb8ac1764e64fa1` | — |
| The critic's check of the fixes, `plan-critic-check.md` | `6d843d8fa4a2ed6c91fa732fb8bfe01dfdf6e592b4c68f60da3f8880bbedafc8` | READY WITH FIXES. All 17 findings resolved. The replacement text brought 2 new major and 4 new minor points, N1–N6 |
| History-free CI on the second candidate's tree (`ci-cand2.log`; `.local/artifacts/r18/r19-cand2-validation/ci312/results.json`) | `0c282d33…`; `5643aadf…` | every step exits 0, with 2,446 passed and 46 skipped, the same as unamended |

**N1–N6 were applied** as the check gave them:
- **N1:** native parity, and the browsers' parity, are shown on the Owner's M3 only;
- **N2:** the availability rule is the live pipeline's, under the tier register and the Owner's rulings
  unchanged. Tier 2's documented schedules are admitted, and 4.7T keeps its registered vintage terms;
- **N3:** a failed check before 4.7T's window is a blocker, not a day's outcome;
- **N4:** S_13's figure is native fit time;
- **N5:** this record names what §24.13 re-reads, where its figures come from, and GitHub's terms;
- **N6:** the zlib value is CP-17b's recorded one, and CP-17c records its own.

**One change after the check, the Orchestrator's own.** CP-17c measures on a private repository's
`macos-26`, not a public one. CP-18 measures the public class's timing in the product's repository before
the first live issuance.
- **The reason.** A public scratch repository's runs would need A1's search state and CP-17c's
  material, and would publish them before decision 25's one complete publication.
- **Why this is safe.** The arithmetic is checked by the canary on every run. Each fit's ceiling fails
  closed on a slower class.

The CI run on the final tree is recorded in `progress.md`'s session log.

**The dispositions of the review's findings.** Every finding was applied, as the critic gave it, unless
the row says otherwise.

| Finding | Disposition |
|---|---|
| M1, the contradicted sentences not superseded by name | applied: §24.12's CP-18 items, §16.2's "numeric origin/deadlines" and the freeze record §11. A machine that passes the checks is not a runtime change |
| M2, how 4.7T binds to CP-17c, and no route if CP-17c fails | applied |
| M3, what the runner needs | applied: the Pyodide folder, the zip check, the states, the CPython pin outside the hash-bound lock, the lineage fields, and where CP-17c shows what |
| M4, "about an hour" | applied: about 4¼ hours by the ceilings, about 21 minutes measured. The Owner is told of the correction to decision 23's record |
| M5, the catch-up against "before the outcome" | applied, scoped by N2 |
| M6, H2 per run or per issuance, and 4.7T | applied: once per run; once before 4.7T's window; the image check; the canary's value as CP-17c records it |
| m1, "re-freeze" against "landing" | applied: from CP-17c's landing |
| m2, the Owner's declaration and H1–H4 | applied: H1–H4 are registrations the audit checks |
| m3, the 50 MB limit | applied |
| m4, H1's overclaims | applied, reworded |
| m5, H4's details | applied, reworded |
| m6, H3's bounds | applied |
| m7, the §14 ruling | applied, reworded |
| m8, the notice against the decisions record | applied |
| m9, the missing CP-18 items | applied |
| m10, the red line on the runner | applied |
| m11, the base and the landing record's hash | applied |

**What r19 did not need:**
- **No experiment, fit or download.** Every figure it states comes from committed records:
  CP-17c-probe's reports and landing record, and CP-17b's reports and freeze manifest. There are two
  exceptions:
  - the 4¼-hour bound, which is arithmetic on the frozen ceilings;
  - GitHub's 6-hour job limit and 100 MB file limit, which are stated as GitHub's published terms.
- **No 4.7T information.** No delivery day after 2026-09-06 exists on this machine, or was read or
  inferred.
