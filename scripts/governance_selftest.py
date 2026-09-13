#!/usr/bin/env python3
"""D-CP0-20 re-test: no role may be denied the means to meet an obligation it carries.

The defect this guards (D-CP0-20, found 2026-08-10, remedied at `3670949`):
`orchestrator-role.md` said flatly **"you have no shell"** while the receipt gate
required the Orchestrator to run commands. The rule was right and the thing that
made it executable was absent. The remedy did not grant a capability — it restated
the limit as *scope*, preserving the obligation and naming a route:

    before:  "You do not audit evidence files yourself, and you have no shell: ..."
    after :  "If your context has no shell, the obligation does not lapse:
              direct a read-only agent to run exactly those commands ..., or ask
              the owner to run them."

So the invariant is not "the phrase 'no shell' must not appear". It is:

    A capability denial is a defect when it is UNCONDITIONAL and nothing
    preserves the obligation that depends on it.

A conditional accommodation that keeps the obligation alive and names a route is
the remedy, not the defect — which is why a naive phrase grep would flag the fix.

Run with `--self-test` to prove the check can fail: it is executed against the
real pre-remedy sentence from Git history and must report a defect.

Usage:
    python3 scripts/governance_selftest.py
    python3 scripts/governance_selftest.py --self-test
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CORPUS = [
    "AGENTS.md",
    "CLAUDE.md",
    "orchestrator-role.md",
    "engineering-role.md",
    "notebooklm-role.md",
    "docs/track-b/gauntlet-templates.md",
    "docs/track-b/rule-inventory.md",
    "docs/track-b/cp-0-defects.md",
]

# A claim that a role lacks a MEANS. Deliberately narrow: it must be about an
# instrument (shell, terminal, tool, access), not about authority or a status.
DENIAL = re.compile(
    r"\b(?:you|the \w+(?:-\w+)?)\s+"
    r"(?:have\s+no|has\s+no|do\s+not\s+have|does\s+not\s+have|lacks?|cannot|can't|may\s+not)\s+"
    r"(?:\w+\s+){0,3}?"
    r"(shell|terminal|command line|commands?|tooling|tools?|filesystem|network)\b",
    re.IGNORECASE,
)

# The remedy's shape: the denial is conditional, and the obligation survives it.
CONDITIONAL = re.compile(r"\b(if|when|where|unless|should)\b", re.IGNORECASE)
OBLIGATION_PRESERVED = re.compile(
    r"does not lapse|still (?:applies|holds|stands|required)|obligation (?:remains|stands)|"
    r"direct a|ask the owner|route it|delegate|have (?:someone|an agent)|instead",
    re.IGNORECASE,
)

# Phrases that make a match a false positive: "terminal status" is a verdict word
# in this corpus, not an instrument.
NOT_AN_INSTRUMENT = re.compile(r"terminal (?:status|statuses|return|result|packet)", re.IGNORECASE)

# Reported speech, not a rule. The defect ledger quotes defective text by design —
# that is its job. A denial inside quote marks, in a sentence that marks itself as a
# citation, is evidence of a past defect rather than a live one. Both conditions are
# required: a bare quoted denial with no citation marker still fails.
CITATION = re.compile(
    r"\bread:|\bstated|\bsaid\b|\bformerly\b|\bpreviously\b|\bhistorical\b|"
    r"\bretired\b|\bsuperseded\b|\bStatement\.|\bremedied\b|\bused to\b|\bwas written\b",
    re.IGNORECASE,
)


def _is_reported_speech(text: str, abs_pos: int) -> bool:
    """True when the denial at `abs_pos` is a citation of past text rather than a live rule.

    Checked against a window of the FULL document, not the sentence: a citation
    lead-in ends in a colon, and the sentence splitter breaks there, so the marker
    and the quotation land in different sentences. Requires BOTH an enclosing quote
    and a citation marker — quote marks alone never excuse a denial.
    """
    lo, hi = max(0, abs_pos - 300), min(len(text), abs_pos + 300)
    window = text[lo:hi]
    rel = abs_pos - lo
    quoted = any(
        a < rel < b
        for pat in (r'"[^"]{0,500}"', r'\u201c[^\u201d]{0,500}\u201d')
        for a, b in ((m.start(), m.end()) for m in re.finditer(pat, window))
    )
    return quoted and bool(CITATION.search(window))


def sentences(text: str) -> list[tuple[int, str]]:
    """(line number, sentence). Sentences may span lines; the line is where it starts."""
    out, line_no, buf, start = [], 1, [], 1
    for ch in text:
        buf.append(ch)
        if ch == "\n":
            line_no += 1
        if ch in ".:!?" and len("".join(buf).strip()) > 20:
            out.append((start, "".join(buf).strip()))
            buf, start = [], line_no
    if buf:
        out.append((start, "".join(buf).strip()))
    return out


def inspect(label: str, text: str) -> list[dict]:
    findings, cursor = [], 0
    for line_no, sent in sentences(text):
        abs_start = text.find(sent[:40], cursor) if sent[:40] else cursor
        if abs_start < 0:
            abs_start = cursor
        cursor = abs_start + max(1, len(sent) - 1)
        m = DENIAL.search(sent)
        if not m:
            continue
        if NOT_AN_INSTRUMENT.search(sent):
            continue
        if _is_reported_speech(text, abs_start + m.start(1)):
            continue  # a quoted past defect, cited as evidence — not a live rule
        conditional = bool(CONDITIONAL.search(sent))
        preserved = bool(OBLIGATION_PRESERVED.search(sent))
        if conditional and preserved:
            continue  # the remedy's shape: obligation survives, route named
        findings.append(
            {
                "file": label,
                "line": line_no,
                "means": m.group(1),
                "conditional": conditional,
                "obligation_preserved": preserved,
                "text": " ".join(sent.split())[:240],
            }
        )
    return findings


def report(findings: list[dict]) -> None:
    for f in findings:
        print(f"    {f['file']}:{f['line']}  denies '{f['means']}'  "
              f"(conditional={f['conditional']}, obligation_preserved={f['obligation_preserved']})")
        print(f"      {f['text']}")


def run_corpus() -> list[dict]:
    findings = []
    for rel in CORPUS:
        p = ROOT / rel
        if not p.exists():
            print(f"  skip (absent): {rel}")
            continue
        findings += inspect(rel, p.read_text(encoding="utf-8"))
    return findings


# The genuine pre-remedy sentence, recovered from `d91b8c3:orchestrator-role.md`.
HISTORICAL_DEFECT = (
    "You do not audit evidence files yourself, and you have no shell: the record-level "
    "rules are enforced by the Engineering Lead and the Critics, not by you."
)
HISTORICAL_REMEDY = (
    "If your context has no shell, the obligation does not lapse: direct a read-only agent "
    "to run exactly those commands and report the raw output, or ask the owner to run them."
)


def self_test() -> int:
    print("Negative control — the check must FAIL on the real pre-remedy text")
    print("(recovered from d91b8c3:orchestrator-role.md, the revision D-CP0-20 was raised against)\n")
    bad = inspect("<historical pre-remedy>", HISTORICAL_DEFECT)
    good = inspect("<historical post-remedy>", HISTORICAL_REMEDY)

    print(f"  pre-remedy  -> {len(bad)} finding(s)   expected >=1")
    report(bad)
    print(f"\n  post-remedy -> {len(good)} finding(s)  expected 0")
    report(good)

    ok = len(bad) >= 1 and len(good) == 0
    print(f"\n  RESULT: {'the check can fail, and does not flag its own remedy — VALID' if ok else '*** THE CHECK IS NOT DISCRIMINATING — DO NOT TRUST IT ***'}")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--self-test", action="store_true", help="prove the check can fail")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    print("D-CP0-20 re-test — obligation/means cross-check over the governance corpus\n")
    findings = run_corpus()
    print()
    if findings:
        print(f"  {len(findings)} unconditional capability denial(s) found:\n")
        report(findings)
        print("\n  RESULT: FAIL — a role is denied a means with no surviving obligation or route.")
        return 1
    print(f"  {len(CORPUS)} documents scanned, no unconditional capability denial.")
    print("\n  RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
