#!/usr/bin/env python3
"""SessionStart hook: keep the secret guard active and report the git state (automation plan item 3).

Created under the Owner's task-scoped Lockdown suspension of 2026-10-04 ("השעיית Lockdown",
granted for `.claude/settings.json` and this file). The same grant expressly authorizes this hook
to write `core.hooksPath` in any session, read-only and AMBIGUOUS ones included. The write only
restores the guard that `AGENTS.md` § Credentials requires: `.githooks/` in the main checkout. Git
otherwise commits without any hook when `core.hooksPath` is unset or points at a missing directory,
and the secret guard silently stops running.

It prints at most ten lines of git state and one helper line. It never prints `progress.md`, a
role document or an anchor, because a hook cannot know the session's role (`AGENTS.md` § Project
role router). Standard library only; it always exits 0 and reports its own errors on stdout,
because a hook's stderr reaches only the debug log.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

HELPER = "Checkpoint tools: `scripts/gauntlet.py --help` · `scripts/bar.py --help`"


def git(cwd: str, *args: str) -> str:
    done = subprocess.run(["git", *args], capture_output=True, text=True, cwd=cwd, timeout=10)
    if done.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {done.stderr.strip() or done.returncode}")
    return done.stdout.strip()


def session_cwd() -> str:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except (ValueError, OSError):
        payload = {}
    return payload.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()


def guard(cwd: str) -> str | None:
    common = git(cwd, "rev-parse", "--path-format=absolute", "--git-common-dir")
    root = os.path.dirname(common.rstrip("/"))
    hooks = os.path.join(root, ".githooks")
    current = subprocess.run(["git", "config", "--get", "core.hooksPath"], capture_output=True,
                             text=True, cwd=root, timeout=10).stdout.strip()
    if current and os.path.isdir(current if os.path.isabs(current) else os.path.join(root, current)):
        return None
    if not os.path.isdir(hooks):
        return f"secret guard: core.hooksPath is {current or 'unset'} and {hooks} is missing; nothing set"
    git(root, "config", "core.hooksPath", hooks)
    return f"secret guard: core.hooksPath was {current or 'unset'}; set to {hooks}"


def state(cwd: str) -> list[str]:
    lines = []
    branch = git(cwd, "rev-parse", "--abbrev-ref", "HEAD")
    head = git(cwd, "rev-parse", "--short=12", "HEAD")
    dirty = [line for line in git(cwd, "status", "--porcelain=v1").split("\n") if line.strip()]
    lines.append(f"git: {branch} at {head}; {len(dirty)} uncommitted path(s)")
    try:
        behind, ahead = git(cwd, "rev-list", "--left-right", "--count", "origin/main...main").split()
        lines.append(f"main: {ahead} ahead, {behind} behind origin/main (local refs, no fetch)")
    except RuntimeError:
        lines.append("main: no local origin/main to compare")
    trees = [line[len("worktree "):] for line in git(cwd, "worktree", "list", "--porcelain").split("\n")
             if line.startswith("worktree ")]
    if len(trees) > 1:
        lines.append(f"worktrees: {len(trees)}: " + ", ".join(trees[1:4]) + (" …" if len(trees) > 4 else ""))
    gauntlet = git(cwd, "for-each-ref", "--format=%(refname:short)", "refs/heads/gauntlet/").split()
    if gauntlet:
        lines.append("gauntlet branches: " + ", ".join(gauntlet[:5]))
    others = [b for b in git(cwd, "for-each-ref", "--format=%(refname:short)", "refs/heads/").split()
              if b != "main" and not b.startswith("gauntlet/")]
    if others:
        lines.append(f"other local branches: {len(others)}: " + ", ".join(others[:4]))
    stashes = [s for s in git(cwd, "stash", "list").split("\n") if s.strip()]
    if stashes:
        lines.append(f"stashes: {len(stashes)} (GitHub Desktop stashes on branch switches; check before relying on the tree)")
    return lines[:9]


def main() -> int:
    cwd = session_cwd()
    out: list[str] = []
    try:
        note = guard(cwd)
        if note:
            out.append(note)
        out.extend(state(cwd))
    except Exception as exc:  # noqa: BLE001 — a hook must never fail the session
        out.append(f"session-start hook: {type(exc).__name__}: {str(exc)[:160]}")
    print("\n".join(out[:10]))
    print(HELPER)
    return 0


if __name__ == "__main__":
    sys.exit(main())
