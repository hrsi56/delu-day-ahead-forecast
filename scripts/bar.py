#!/usr/bin/env python3
"""Plan-checklist extractor and brief checker (automation plan item 2).

Text extraction, hashing and byte comparison. The judgement about a brief's content stays the
Orchestrator's; this script checks form only.

Self-contained: standard library and git only, no import from `scripts/`, no `__file__`-relative
path and no stdin input. A party checking someone else's work runs `main`'s copy:

    git show main:scripts/bar.py | python3 -I - <command> ...

Commands:

    bar <plan> "<heading>" [--at SHA] [--quote]
        Print a plan section verbatim, from its heading to the next heading of the same or a
        higher level (trailing blank lines dropped). The heading may be given with or without its
        leading '#'s and must match exactly. Prints the plan's SHA-256 at that commit on stderr.

    check <file> --source <path>@<sha> [--source ...]
        Every '>'-quoted block in <file> (a brief, assignment or verdict) must appear byte for
        byte in one of the sources at its commit. Leading whitespace, then '>' and one following
        space, are stripped first. Exits 1 at the first block that does not match.

    brief <brief.md>
        Checks the templates §1 form: every required section, the three Target fields, no
        template placeholder left, one checkpoint, a numeric timebox, and a plan anchor whose file
        exists and whose cited section resolves. Prints the brief's SHA-256.

    identity <file> [--at SHA]
        Prints the file's revision line and SHA-256 at that commit.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys

REQUIRED_SECTIONS = (
    "Target",
    "Orchestrator-reported expected state",
    "Observable outcome",
    "Complete authoritative checkpoint bar",
    "Applicable constraints",
    "Timebox",
    "Owner-only actions already authorized",
    "Stop and return",
)
TARGET_FIELDS = ("Repository:", "Authorized checkpoint:", "Ratified plan anchor:")
TEMPLATES = "docs/track-b/gauntlet-templates.md"
HEADING = re.compile(r"^(#{1,6}) (.*?)\s*$")
CHECKPOINT_ID = re.compile(r"\b(?:CP-\d+[a-z]?|PRES-\d+|M\d+(?:\.\d+)?)\b")


def git(*args: str) -> str:
    done = subprocess.run(["git", *args], capture_output=True, text=True)
    if done.returncode != 0:
        raise SystemExit(f"bar: git {' '.join(args)} failed: {done.stderr.strip()}")
    return done.stdout


def git_bytes(*args: str) -> bytes:
    done = subprocess.run(["git", *args], capture_output=True)
    if done.returncode != 0:
        raise SystemExit(f"bar: git {' '.join(args)} failed: {done.stderr.decode(errors='replace').strip()}")
    return done.stdout


def show(path: str, sha: str) -> bytes:
    return git_bytes("show", f"{sha}:{path}")


def full_sha(rev: str) -> str:
    return git("rev-parse", "--verify", f"{rev}^{{commit}}").strip()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def section(text: str, heading: str) -> list[str]:
    """The lines of the section that starts at `heading`, trailing blank lines dropped."""
    lines = text.split("\n")
    wanted = heading.strip()
    start = level = None
    end = len(lines)
    fenced = False
    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        match = None if fenced else HEADING.match(line)
        if not match:
            continue
        if start is None:
            if line.rstrip() == wanted or (not wanted.startswith("#") and match.group(2) == wanted):
                start, level = i, len(match.group(1))
        elif len(match.group(1)) <= level:
            end = i
            break
    if start is None:
        raise SystemExit(f"bar: no heading matches {heading!r} exactly")
    body = lines[start:end]
    while body and not body[-1].strip():
        body.pop()
    return body


def cmd_bar(args: argparse.Namespace) -> int:
    sha = full_sha(args.at)
    data = show(args.plan, sha)
    body = section(data.decode("utf-8"), args.heading)
    text = "\n".join(body) + "\n"
    if args.quote:
        text = "".join(f"> {line}".rstrip() + "\n" for line in body)
    sys.stdout.write(text)
    excerpt = ("\n".join(body) + "\n").encode("utf-8")
    print(f"plan {args.plan} at {sha}: sha256 {sha256(data)}; "
          f"section {len(body)} lines, {len(excerpt)} bytes, sha256 {sha256(excerpt)}", file=sys.stderr)
    return 0


def quote_blocks(text: str) -> list[tuple[int, list[str]]]:
    """Maximal runs of '>'-quoted lines, as (first line number, stripped lines)."""
    blocks: list[tuple[int, list[str]]] = []
    current: list[str] = []
    first = 0
    for number, line in enumerate(text.split("\n"), start=1):
        stripped = line.lstrip()
        if stripped.startswith(">"):
            if not current:
                first = number
            content = stripped[1:]
            current.append(content[1:] if content.startswith(" ") else content)
        elif current:
            blocks.append((first, current))
            current = []
    if current:
        blocks.append((first, current))
    return blocks


def cmd_check(args: argparse.Namespace) -> int:
    if not args.source:
        raise SystemExit("bar: check needs at least one --source <path>@<sha>")
    sources = []
    for spec in args.source:
        path, _, rev = spec.rpartition("@")
        if not path or not rev:
            raise SystemExit(f"bar: a source must be <path>@<sha>, not {spec!r}")
        sha = full_sha(rev)
        sources.append((f"{path}@{sha[:12]}", show(path, sha).decode("utf-8")))
    with open(args.file, encoding="utf-8") as handle:
        blocks = quote_blocks(handle.read())
    if not blocks:
        print(f"bar: {args.file} has no '>'-quoted block")
        return 1
    for first, lines in blocks:
        text = "\n".join(lines)
        found = next((name for name, source in sources if text in source), None)
        if found:
            print(f"ok: lines {first}–{first + len(lines) - 1} ({len(text.encode())} bytes) appear in {found}")
            continue
        # Report the first line where the longest matching prefix breaks.
        best = 0
        for _, source in sources:
            k = 0
            while k < len(lines) and "\n".join(lines[: k + 1]) in source:
                k += 1
            best = max(best, k)
        bad = lines[best] if best < len(lines) else lines[-1]
        print(f"MISMATCH: {args.file}:{first + best} is not in any source after the quote's first "
              f"{best} line(s): {bad[:160]!r}")
        return 1
    return 0


def template_placeholders(text: str) -> set[str]:
    """The bracketed placeholders of templates §1's form, read from main."""
    try:
        templates = show(TEMPLATES, "main").decode("utf-8")
        form = "\n".join(section(templates, "## 1. Orchestrator checkpoint brief"))
    except SystemExit:
        form = ""
    found = set(re.findall(r"\[[^\]\n]+\]", form))
    found.update({"[...]", "[…]"})
    return {token for token in found if token in text}


def sections_of(text: str) -> dict[str, str]:
    parts: dict[str, str] = {}
    name = None
    buffer: list[str] = []
    fenced = False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            fenced = not fenced
        if line.startswith("## ") and not fenced:
            if name is not None:
                parts[name] = "\n".join(buffer)
            name, buffer = line[3:].strip(), []
        elif name is not None:
            buffer.append(line)
    if name is not None:
        parts[name] = "\n".join(buffer)
    return parts


def cmd_brief(args: argparse.Namespace) -> int:
    with open(args.brief, "rb") as handle:
        raw = handle.read()
    text = raw.decode("utf-8")
    problems: list[str] = []
    parts = sections_of(text)
    for name in REQUIRED_SECTIONS:
        if name not in parts or not parts[name].strip():
            problems.append(f"missing or empty section: ## {name}")
    target = parts.get("Target", "")
    lines = {field: next((line for line in target.split("\n") if line.lstrip("- ").startswith(field)), None)
             for field in TARGET_FIELDS}
    for field, line in lines.items():
        if line is None:
            problems.append(f"Target lacks the field {field!r}")
    placeholders = template_placeholders(text)
    if placeholders:
        problems.append(f"template placeholders left: {sorted(placeholders)}")
    checkpoint = lines.get("Authorized checkpoint:") or ""
    ids = sorted(set(CHECKPOINT_ID.findall(checkpoint)))
    if len(ids) != 1:
        problems.append(f"the authorized checkpoint names {len(ids)} checkpoints ({ids}), not exactly one")
    hours = re.findall(r"(\d+(?:\.\d+)?)\s*(?:active\s+)?(?:hours?|h)\b", parts.get("Timebox", ""))
    if not hours:
        problems.append("the timebox carries no figure in hours")
    anchor = lines.get("Ratified plan anchor:") or ""
    plan = re.search(r"`([^`]+\.md)`", anchor)
    cited = re.search(r"§\s*(\d+(?:\.\d+)*)", anchor)
    if not plan:
        problems.append("the plan anchor names no `<file>.md`")
    else:
        listed = git("ls-tree", "--name-only", "HEAD", "--", plan.group(1)).strip()
        if not listed:
            problems.append(f"the plan file {plan.group(1)} is not in HEAD")
        elif cited:
            plan_text = show(plan.group(1), "HEAD").decode("utf-8")
            number = cited.group(1)
            if not re.search(rf"^#{{1,6}} {re.escape(number)}[. ]", plan_text, flags=re.M):
                problems.append(f"§{number} does not resolve to a heading in {plan.group(1)}")
    for problem in problems:
        print(f"PROBLEM: {problem}")
    print(f"brief {args.brief}: sha256 {sha256(raw)}; checkpoint {ids[0] if len(ids) == 1 else '?'}; "
          f"timebox figures {hours}")
    return 1 if problems else 0


def cmd_identity(args: argparse.Namespace) -> int:
    sha = full_sha(args.at)
    data = show(args.file, sha)
    lines = data.decode("utf-8").split("\n")[:60]
    revision = next((line for line in lines if re.search(r"\*\*Revision:?\*\*|^Revision\b", line)), None)
    if revision is None:
        revision = next((line for line in lines if HEADING.match(line) and re.search(r"\bv\d+(?:-r\d+)?\b", line)), None)
    if revision is None:
        revision = next((line for line in lines if HEADING.match(line)), "(no revision line)")
    print(f"{args.file} at {sha}")
    print(f"revision line: {revision.strip()}")
    print(f"sha256: {sha256(data)}")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="bar.py", description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("bar", help="print a plan section verbatim")
    p.add_argument("plan")
    p.add_argument("heading")
    p.add_argument("--at", default="HEAD")
    p.add_argument("--quote", action="store_true", help="prefix every line with '> '")
    p.set_defaults(func=cmd_bar)
    p = sub.add_parser("check", help="check quoted blocks against their sources")
    p.add_argument("file")
    p.add_argument("--source", action="append", default=[])
    p.set_defaults(func=cmd_check)
    p = sub.add_parser("brief", help="check a brief's templates §1 form")
    p.add_argument("brief")
    p.set_defaults(func=cmd_brief)
    p = sub.add_parser("identity", help="print a file's revision line and SHA-256")
    p.add_argument("file")
    p.add_argument("--at", default="HEAD")
    p.set_defaults(func=cmd_identity)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
