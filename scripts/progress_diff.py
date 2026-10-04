#!/usr/bin/env python3
"""The omission diff for `progress.md` (automation plan item 8).

Compares `progress.md` in the working tree with the last delivered version (`HEAD`, or
`--against <ref>`). It confirms that the seven sections of `orchestrator-role.md`'s mandatory
skeleton are present and in order, groups every removed block by section, and lists separately
the removals from what may never be dropped: Setup State, Strategic Anchors, Standing Scope
Decisions, Blockers / Open Questions, Notes for Future Sessions, and the next pending Track B
checkpoint in Current Position.

It always exits 0: whether each removal was resolved or pruned stays the Orchestrator's
judgement. It reads `progress.md`, so only the Orchestrator uses it; it must never be wired into a
hook.

    python3 scripts/progress_diff.py [--against REF] [--file progress.md]
"""
from __future__ import annotations

import argparse
import difflib
import re
import subprocess
import sys

SKELETON = ("Current Position", "Setup State", "Strategic Anchors", "Standing Scope Decisions",
            "Session Log", "Blockers / Open Questions", "Notes for Future Sessions")
PROTECTED = {"Setup State", "Strategic Anchors", "Standing Scope Decisions",
             "Blockers / Open Questions", "Notes for Future Sessions"}
NEXT_PENDING = "**Next pending Track B checkpoint"


def sections(text: str) -> list[tuple[str, list[str]]]:
    parts: list[tuple[str, list[str]]] = [("(preamble)", [])]
    for line in text.split("\n"):
        if line.startswith("## "):
            parts.append((re.sub(r"^\d+\.\s*", "", line[3:].strip()), []))
        else:
            parts[-1][1].append(line)
    return parts


def blocks(lines: list[str]) -> list[str]:
    """Top-level blocks: a bullet or table row at column 0 with everything indented under it, or
    a paragraph of consecutive column-0 lines."""
    out: list[list[str]] = []
    previous_blank = True
    for line in lines:
        if not line.strip():
            previous_blank = True
            continue
        starts_item = line.startswith(("- ", "|"))
        if line[0].isspace() and out:
            out[-1].append(line)
        elif starts_item or previous_blank or not out or out[-1][0].startswith(("- ", "|")):
            out.append([line])
        else:
            out[-1].append(line)
        previous_blank = False
    return [b for b in ("\n".join(block).rstrip() for block in out) if b.strip() != "---"]


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--against", default="HEAD")
    parser.add_argument("--file", default="progress.md")
    args = parser.parse_args(argv)
    old_text = subprocess.run(["git", "show", f"{args.against}:{args.file}"], capture_output=True,
                              text=True).stdout
    with open(args.file, encoding="utf-8") as handle:
        new_text = handle.read()
    old, new = sections(old_text), sections(new_text)
    names = [next((s for s in SKELETON if name.startswith(s)), name) for name, _ in new[1:]]
    present = [name for name in SKELETON if name in names]
    missing = [name for name in SKELETON if name not in names]
    ordered = [name for name in names if name in SKELETON] == present
    print(f"skeleton: {len(present)}/7 present{'' if ordered else ', OUT OF ORDER'}"
          + (f"; missing {missing}" if missing else ""))
    new_blocks = {name: blocks(lines) for name, lines in new}
    protected_hits: list[str] = []
    for name, lines in old:
        before = blocks(lines)
        after = new_blocks.get(name, [])
        removed = [b for b in before if b not in after]
        if not removed:
            continue
        print(f"\n## {name}: {len(removed)} block(s) removed or edited")
        for block in removed:
            first = block.split("\n", 1)[0][:150]
            close = difflib.get_close_matches(block, after, n=1, cutoff=0.6)
            label = "edited" if close else "removed"
            print(f"  - [{label}] {first}")
            if not close and (name in PROTECTED or block.startswith(NEXT_PENDING)):
                protected_hits.append(f"{name}: {first}")
    print(f"\nprotected removals (resolve each in the Session Log, or restore it): {len(protected_hits)}")
    for hit in protected_hits:
        print(f"  ! {hit}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
