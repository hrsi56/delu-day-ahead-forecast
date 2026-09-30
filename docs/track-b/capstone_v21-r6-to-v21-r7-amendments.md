# Capstone v21-r6 → v21-r7 — distribution challenger: DDNN only, in NumPy (Owner-authorized)

**Authorized by the Owner on 2026-09-30. A documentation amendment only: it opens no
checkpoint, runs nothing and publishes nothing.**

## Decision and authority

On 2026-09-30 the Owner wrote:

> יש לך הרשאה מלאה. תערוך בעוגנים את ההתייחסות ל DDNN ו TabPFN. אנחנו נוותר על TabPFN.
> קבע ש-DDNN נכתב מההתחלה ב-numpy בלבד. PyTorch ישמש רק כבדיקת נכונות על המחשב.

In English: you have full authority. Edit the anchors' treatment of DDNN and TabPFN. We are
dropping TabPFN. Set that DDNN is written from the start in NumPy only. PyTorch will serve only
as a correctness check on the development machine.

**How it came about.** Earlier the same day the Owner asked for a one-click option to retrain
the final product in the browser, so that anyone who wants to check it can, and asked what is
possible. The consultation found:

- The current Static Space runs v1's nine LightGBM boosters under Pyodide, bitwise equal to the
  frozen artifact. It runs inference only; it does not train.
- Pyodide provides NumPy and LightGBM, which the demo already uses, and scikit-learn. It
  provides no PyTorch.
- The research leader's components, LEAR through scikit-learn's Lasso and LightGBM, can in
  principle be retrained under Pyodide. CP-21 measured HGL's cold daily cycle at a median of
  24.7 s and a maximum of 69.4 s on the M3 with four processes. Browser timings are unmeasured.
- DDNN is a small multi-output network. Written once in NumPy, it needs no second
  implementation for the browser. Written in PyTorch and rewritten later, the browser would
  train a similar model, not the evaluated one.
- TabPFN is a pretrained transformer. Its daily update would be context replacement, which
  §16.2 does not count as training. It has no Pyodide runtime, and its licence entry was open.
- Training is sensitive to floating-point order. Equality between a browser run and a native
  run must be measured, not assumed; in a neural network, small differences can grow during
  training.

The Owner then asked whether rewriting DDNN for the browser was reasonable. The recommendation
was to write it once, from the start, in NumPy, and to keep PyTorch as a test reference only.
The Owner adopted that and dropped TabPFN.

**Authority.** The Owner's grant acts as a task-scoped Lockdown suspension. It covers:

- `capstone_v21.md` revision v21-r7: a new header and §18;
- this record;
- directly necessary consistency edits to `docs/track-b/v3-plan-handoff-2026-09-22.md` and
  `progress.md`.

This task reads "full authority" as also covering a commit of these documents to the session
branch `claude/browser-model-retraining-options-r16r4p`, its push, and a draft pull request.
Landing on `main` remains the Owner's, by hand. The grant is not a standing exception, and the
suspension ends at this task's terminal return.

## Identities

| Item | Identity |
|---|---|
| Incoming `main` = `origin/main` | `4e37cf7926c87744188b679cef5a7d29e9ef6499` (the CP-21 commit, "HGL adopted in research as v4") |
| Previous research authority | v21-r6 at `270a0a0:capstone_v21.md`, SHA-256 `ee402c4703d176f8181ed82966c978ad84c3c73a0cdb1d3567871f58bc867344` |
| Revised anchor | `capstone_v21.md` v21-r7, SHA-256 `e6a4e301d5db080c6427f925f51e2cf69367c42225b292c78050117003aa7b0c` |
| Programme handoff | `ddc6bd3a68a917f314f9d6d032c68d5ed8d0b2b6c8226055e00b839dfb727c70` before; `cf498c44669fdcb81cad063afb69e232b3f0d62ba1642452df6eaa1b511a28d8` after |
| Publication anchor | PUBLISH_RULES 1.1, SHA-256 `91eea445434718a163f03bcfd82e1db275a9d98311e76eb6cd1365f3707584f3`, unchanged |
| This record | Its SHA-256 is recorded in `progress.md`, since a file cannot carry its own hash |

**What v21-r7 adds:** a revision header and §18. It deletes and alters no existing line; `git
diff` against v21-r6 shows 118 added lines and none removed. CP-21's evidence binds the v21-r6
bytes and is neither reopened nor rescored.

## The decisions, as §18 records them

| # | Decision | Section |
|---|---|---|
| T1 | TabPFN is withdrawn in every version: no candidate, comparator, recombination or product role. The TabPFN–DDNN comparison is withdrawn by decision, not reported as failed. Bringing TabPFN back needs a new Owner amendment. | §18.1 |
| N1 | DDNN's model code is written from scratch in NumPy and the Python standard library alone, and it is the single implementation behind every DDNN number. | §18.2 |
| N2 | PyTorch is only a correctness reference in tests on the development machine. It never trains a scored model, emits nothing that enters evidence, and is not a runtime dependency. The 4.6 brief ensures the tests cannot be skipped silently. | §18.3 |
| R1 | The 4.6 route follows: 4.6L becomes a provenance and licence record, 4.6R gains the correctness entry condition, 4.6C becomes a single-candidate comparison. §16 applies unchanged. | §18.4 |

## Consistency edits to the programme handoff

Each edited passage in the handoff is marked *2026-09-30*:

- a dated 4.6 update note at the top;
- the index rows for 4.6 and 4.6L;
- D4, which now names the DDNN route;
- the register rows for 4.6L, 4.6R and 4.6C. Their effort estimates are now marked as
  two-family estimates, which the brief re-estimates;
- the 4.6 brief prerequisites in §4.B;
- the candidate table: DDNN is the sole candidate and TabPFN is withdrawn;
- the browser-delivery paragraph. Its TabPFN-specific sentence on model-output terms is removed;
- §4.6L, retitled "Provenance and licence entry" and rewritten for DDNN's own code. The use
  table is kept;
- §4.6R: the correctness entry condition;
- §4.6C: single-candidate wording. An entry failure means no comparison runs;
- §4.7T: the rule for including DDNN;
- §4.7: the TabPFN ranking sentence and the TabPFN delivery-wording template are withdrawn;
- the daily-update manifest rows for DDNN and TabPFN;
- the §6 handoff line for 4.6.

## Left unchanged on purpose

- **PUBLISH_RULES 1.1.** Its sentence "No such exception is granted here to TabPFN, immutable v1
  or any other model" remains accurate, so the publication anchor is not revised.
- **Historical records that name TabPFN.** They describe what was planned when they were
  written: `docs/track-b/plan-review-2026-09-22.md`,
  `docs/track-b/v3-plan-independent-review-2026-09-22.md`,
  `docs/track-b/v3-plan-independent-review-2026-09-23.md`,
  `docs/track-b/v3-plan-rewrite-brief-2026-09-22.md`,
  `docs/track-b/v2-decision-brief-packet.md`,
  `docs/track-b/presentation-and-tracking-plan-2026-09-24.md`,
  `docs/track-b/research-content/cp15-cp16-claims.md` and
  `docs/track-b/research-content/cp20-claims.md`.
- **The public report and its generator.** `docs/index.html`, built by `scripts/build_pages.py`,
  lists the planned item "4.6 · DDNN / TabPFN" with the question "Does a distributional network,
  or a tabular foundation model, beat v3?". Changing it is publication. The next authorized
  publication block corrects it.
- **Claim guard W14** in `src/delu_forecast/research_claims.py`, which refuses an unsupported
  performance claim naming TabPFN or DDNN. It still does its job.
- **Role documents and the stage map.** `program-stage-sequence.md` has no 4.6 entry, and neither
  role document names either model.

## Not decided here

- **In-browser retraining of the final product.** Whether it is required, how binding it is and
  what equality it claims belong to the final-product briefs under §16, CP-17 and CP-18. The
  consultation's recommendation is recorded in `progress.md` as an open question, not ratified.
- **Where the official daily fit runs.** Running it in the same WebAssembly runtime as the
  browser might make equality attainable. It is an option to measure, not a decision.
- **4.6's comparator, information set and budgets.** They follow the standing decisions and D4
  when the brief is written. The standing decision "same information, same opponent" still
  names HG; updating it after CP-21 is a pending Owner question.

## Follow-ups

- The next publication block corrects the public planned item for 4.6.
- The first 4.6 brief cites v21-r7 §18 and fixes the §4.B fields, including the PyTorch test
  tolerances and how those tests are installed and run.
