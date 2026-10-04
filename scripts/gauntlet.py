#!/usr/bin/env python3
"""Checkpoint mechanics: identity, return, receipt, Critic launch and closure (automation plan
items 1, 4 and 5).

Pure git and the standard library. It records and checks topology; every judgement stays with the
Lead, the Critic, the Orchestrator or the Owner. LAND is the Owner's, by hand: this script only
prints its commands.

Self-contained, so that a party checking someone else's work can run `main`'s copy:

    git show main:scripts/gauntlet.py | python3 -I - <command> ...

It imports nothing from `scripts/`, uses no `__file__`-relative path and reads no stdin; it calls
`scripts/bar.py` the same way, from `main`. Per-checkpoint state lives in the main checkout under
`.local/artifacts/<cp>/`, found through `git rev-parse --git-common-dir`, so it works from a
worktree too. `<cp>` is the branch suffix, for example `cp-23`.

Lead, at the start and the return of a checkpoint:
    start <cp>                                  record the baseline (never overwritten)
    return <cp> <final_candidate_sha> [<tip>]   check the evidence; print the return's blocks

Lead, for the one Integration Critic:
    critic-open <cp> <sha> <assignment.md>      clean detached worktree at the candidate
    critic-brief <cp>                           the Critic's generated brief (run from main)
    critic-close <cp>                           check, remove the worktree, hash the verdict

Orchestrator:
    receipt <cp> <final_candidate_sha> <evidence_tip_sha>   templates §4's receipt, verbatim
    inspect <branch> [--final SHA]              the INSPECT block, and findings for any branch
    citations <cp>                              who names gauntlet/<cp>: live, historical, locked
    discard <cp> <k>                            tag archive/<cp>-attempt-<k> at the branch tip
    reclaim <cp> --disposition land|discard     bundle, then delete the branch and its worktrees
    land-commands <cp>                          print the Owner's non-interactive LAND sequence
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from datetime import datetime, timezone

EVIDENCE = "docs/track-b/evidence/{cp}/"
LOCKED = (
    "AGENTS.md", "CLAUDE.md", "engineering-role.md", "orchestrator-role.md", "notebooklm-role.md",
    "docs/track-b/gauntlet-templates.md", "capstone_*.md", "capstone_[Vv]*.md", "syllabus_v*.md",
    "program-stage-sequence.md", "docs/PUBLISH_RULES.md", "docs/track-b/publication-standard-v1.md",
    "docs/track-b/rule-inventory.md", "docs/track-b/cp-0-defects.md", "*-amendments.md", ".claude/*",
)
HISTORICAL = ("docs/track-b/evidence/*", "docs/track-b/*-landing-*.md", "docs/track-b/*-closure-*.md",
              "docs/track-b/*-receipt-*.md", "reports/*")
SHA_TOKEN = re.compile(r"(?<![0-9A-Za-z…])[0-9a-f]{7,40}(?![0-9A-Za-z…])")


# ---- git helpers -------------------------------------------------------------------------------

def git(*args: str, cwd: str | None = None, check: bool = True) -> str:
    done = subprocess.run(["git", *args], capture_output=True, text=True, cwd=cwd)
    if check and done.returncode != 0:
        raise SystemExit(f"gauntlet: git {' '.join(args)} failed: {done.stderr.strip()}")
    return done.stdout


def git_ok(*args: str, cwd: str | None = None) -> bool:
    return subprocess.run(["git", *args], capture_output=True, cwd=cwd).returncode == 0


def resolve(rev: str, cwd: str | None = None) -> str | None:
    done = subprocess.run(["git", "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}"],
                          capture_output=True, text=True, cwd=cwd)
    return done.stdout.strip() or None


def show(rev: str, path: str) -> bytes | None:
    done = subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True)
    return done.stdout if done.returncode == 0 else None


def main_checkout() -> str:
    common = git("rev-parse", "--path-format=absolute", "--git-common-dir").strip()
    return os.path.dirname(common.rstrip("/"))


def state_dir(cp: str) -> str:
    return os.path.join(main_checkout(), ".local", "artifacts", cp)


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def worktrees(cwd: str | None = None) -> list[dict]:
    items, item = [], {}
    for line in git("worktree", "list", "--porcelain", cwd=cwd).split("\n"):
        if not line.strip():
            if item:
                items.append(item)
            item = {}
            continue
        key, _, value = line.partition(" ")
        item[key] = value or True
    if item:
        items.append(item)
    return items


def snapshot() -> dict:
    refs = {}
    for line in git("for-each-ref", "--format=%(refname) %(objectname)", "refs/heads", "refs/tags").split("\n"):
        if line.strip():
            name, sha = line.split(" ", 1)
            refs[name] = sha
    return {
        "utc": now_utc(),
        "head": resolve("HEAD"),
        "branch": git("rev-parse", "--abbrev-ref", "HEAD").strip(),
        "main": resolve("main"),
        "origin_main": resolve("refs/remotes/origin/main"),
        "worktrees": [w.get("worktree") for w in worktrees()],
        "refs": refs,
        "stashes": [s for s in git("stash", "list", "--format=%H %gs").split("\n") if s.strip()],
        "status": [s for s in git("status", "--porcelain=v1").split("\n") if s.strip()],
    }


def matches(path: str, patterns: tuple[str, ...]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)


def run_shown(command: str, cwd: str) -> None:
    """Print a command verbatim, then its raw output and exit code."""
    done = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=cwd)
    print(f"$ {command}")
    output = done.stdout + done.stderr
    if output:
        print(output.rstrip("\n"))
    print(f"(exit {done.returncode})\n")


def bar_from_main(*args: str) -> subprocess.CompletedProcess:
    source = show("main", "scripts/bar.py")
    if source is None:
        raise SystemExit("gauntlet: main has no scripts/bar.py")
    return subprocess.run([sys.executable, "-I", "-", *args], input=source, capture_output=True)


def section(text: str, heading: str) -> str:
    """From `heading` (a full line) to the next heading of the same or a higher level. Lines
    inside fenced code blocks are never headings: the templates' forms start with '# '."""
    lines = text.split("\n")
    level = len(heading) - len(heading.lstrip("#"))
    fenced, start, end = False, None, len(lines)
    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if start is None:
            if line.rstrip() == heading:
                start = i
        elif re.match(rf"^#{{1,{level}}} ", line):
            end = i
            break
    if start is None:
        return ""
    return "\n".join(lines[start:end]).rstrip() + "\n"


# ---- start and return (item 1) ----------------------------------------------------------------

def cmd_start(args: argparse.Namespace) -> int:
    folder = state_dir(args.cp)
    path = os.path.join(folder, "start.json")
    if os.path.exists(path):
        print(f"gauntlet: {path} exists. It is this checkpoint's only baseline and is never overwritten.")
        return 1
    os.makedirs(folder, exist_ok=True)
    state = snapshot()
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(f"recorded {path} at {state['utc']}: HEAD {state['head'][:12]} on {state['branch']}, "
          f"main {str(state['main'])[:12]}, origin/main {str(state['origin_main'])[:12]}, "
          f"{len(state['worktrees'])} worktree(s), {len(state['stashes'])} stash(es), "
          f"{len(state['status'])} uncommitted path(s)")
    return 0


def identity_shas(text: str) -> list[str]:
    found = []
    for line in text.split("\n"):
        if re.search(r"revision|space|hub", line, flags=re.I):
            continue
        for token in SHA_TOKEN.findall(line):
            if re.search(r"[a-f]", token) and token not in found:
                found.append(token)
    return found


def cmd_return(args: argparse.Namespace) -> int:
    cp = args.cp
    problems: list[str] = []
    final = resolve(args.final) or args.final
    tip = resolve(args.tip)
    if not resolve(args.final) or not tip:
        raise SystemExit("gauntlet: the final candidate or the evidence tip does not resolve")
    branch = f"gauntlet/{cp}"
    evidence = EVIDENCE.format(cp=cp)
    if final == tip:
        problems.append("the final candidate and the evidence tip are the same commit")
    if not git_ok("merge-base", "--is-ancestor", final, tip):
        problems.append("the final candidate is not an ancestor of the evidence tip")
    delta = [p for p in git("diff", "--name-only", f"{final}..{tip}").split("\n") if p.strip()]
    outside = [p for p in delta if not p.startswith(evidence)]
    if outside:
        problems.append(f"the delta leaves {evidence}: {outside}")

    verdict = show(tip, evidence + "integration.md")
    result = "missing"
    if verdict is None:
        problems.append(f"no {evidence}integration.md at the evidence tip")
    else:
        text = verdict.decode("utf-8")
        head = re.match(r"^# Verdict — (.+?) — Integration — (PASS|FAIL|BLOCKED)\b", text)
        result = head.group(2) if head else "unreadable"
        if not head or head.group(1).strip().lower().replace(" ", "-") != cp.lower():
            problems.append("the verdict's first line is not '# Verdict — <cp> — Integration — <result>'")
        if result != "PASS":
            problems.append(f"the verdict reads {result}, not PASS")
        candidate = next((line for line in text.split("\n") if "Candidate SHA" in line), "")
        if final not in candidate:
            problems.append("the verdict's Candidate SHA line does not cite the final candidate in full")

    returned = show(tip, evidence + "checkpoint-return.md")
    cited: list[str] = []
    if returned is not None:
        block = re.search(r"^## Identity\n(.*?)(?=^## )", returned.decode("utf-8"), flags=re.S | re.M)
        cited = identity_shas(block.group(1)) if block else []
    if verdict is not None:
        cited += [s for s in identity_shas(next((l for l in verdict.decode("utf-8").split("\n")
                                                 if "Candidate SHA" in l), "")) if s not in cited]
    for token in cited:
        sha = resolve(token)
        if sha is None:
            problems.append(f"cited SHA {token} does not resolve to a commit")
        elif not git_ok("merge-base", "--is-ancestor", sha, tip):
            outside_refs = git("for-each-ref", "--contains", sha, "--format=%(refname)").split()
            if not outside_refs:
                problems.append(f"cited SHA {token} is reachable from no branch or tag")

    brief = show(tip, evidence + "issued-brief.md")
    canonical = os.path.join(state_dir(cp), "issued-brief.md")
    brief_note = "no canonical copy in .local"
    if brief is None:
        problems.append(f"no {evidence}issued-brief.md at the evidence tip")
    elif os.path.exists(canonical):
        with open(canonical, "rb") as handle:
            same = sha256(handle.read()) == sha256(brief)
        brief_note = f"sha256 {sha256(brief)}, {'equal to' if same else 'DIFFERENT FROM'} the canonical copy"
        if not same:
            problems.append("the packaged brief differs from its canonical copy")

    start_path = os.path.join(state_dir(cp), "start.json")
    now = snapshot()
    since: list[str] = []
    base = git("merge-base", "main", tip).strip()
    elapsed = "unknown: no start.json"
    if os.path.exists(start_path):
        with open(start_path, encoding="utf-8") as handle:
            start = json.load(handle)
        base = start.get("main") or base
        for name in sorted(set(now["refs"]) - set(start["refs"])):
            since.append(f"created {name} at {now['refs'][name][:12]}")
        for name in sorted(set(start["refs"]) - set(now["refs"])):
            since.append(f"deleted {name} (was {start['refs'][name][:12]})")
        for key in ("main", "origin_main"):
            if start.get(key) != now.get(key):
                since.append(f"{key.replace('_', '/')} moved from {str(start.get(key))[:12]} to {str(now.get(key))[:12]}")
        for path in sorted(set(now["worktrees"]) - set(start["worktrees"])):
            since.append(f"worktree present now, not at start: {path}")
        for path in sorted(set(start["worktrees"]) - set(now["worktrees"])):
            since.append(f"worktree gone since start: {path}")
        for stash in now["stashes"]:
            if stash not in start["stashes"]:
                since.append(f"stash created since start: {stash}")
        hours = (datetime.fromisoformat(now["utc"]) - datetime.fromisoformat(start["utc"])).total_seconds() / 3600
        elapsed = (f"about {round(hours * 2) / 2:g} wall-clock hours since start ({start['utc']}), to the "
                   "nearest half hour; subtract the pauses you recorded")

    print("## Identity")
    print(f"- final_candidate_sha: `{final}`   (every bar binds here)")
    print(f"- evidence_tip_sha: `{tip}`   (state it in the terminal message: a file cannot contain its own SHA)")
    print(f"- git diff --name-only {final}..{tip}:\n\n  ```text")
    for path in delta:
        print(f"  {path}")
    print("  ```\n")
    print("## Repository state")
    dirty = len(now["status"])
    print(f"- Branch: {branch} at `{(resolve(branch) or 'missing')[:12]}`; HEAD on {now['branch']}; "
          f"working tree: {'clean' if not dirty else f'{dirty} uncommitted path(s)'}")
    print(f"- main `{str(now['main'])[:12]}`, origin/main `{str(now['origin_main'])[:12]}` (local refs, no fetch)")
    if since:
        print("- Since start:")
        for line in since:
            print(f"  - {line}")
    elif os.path.exists(start_path):
        print("- Since start: no branch, tag, worktree, stash or main movement")
    print(f"- Issued brief: {brief_note}\n")
    print("## Integration verdict")
    print(f"- Path: {evidence}integration.md   Result: {result}")
    print(f"- Candidate SHA it binds: `{final}`\n")
    print(f"## Files changed\n\n```text\n{git('diff', '--stat', f'{base}..{tip}').rstrip()}\n```")
    print("(add one line of rationale per file)\n")
    print(f"## Elapsed\n\n{elapsed}\n")
    print(f"checks: {len(cited)} cited SHA(s) examined; {len(problems)} problem(s)")
    for problem in problems:
        print(f"PROBLEM: {problem}")
    return 1 if problems else 0


def cmd_receipt(args: argparse.Namespace) -> int:
    """Templates §4's receipt list, verbatim, with raw output and exit codes (Owner, 2026-10-04:
    the templates list governs). It adds no command; the confirmations stay the Orchestrator's."""
    repo = main_checkout()
    final, tip, cp = args.final, args.tip, args.cp
    quoted = shlex.quote(repo)
    for command in (
        f"git -C {quoted} log --oneline -3 {tip}",
        f"git -C {quoted} diff --name-only {final}..{tip}",
        f"git -C {quoted} status --porcelain=v1",
        f"git -C {quoted} branch -vv",
        f"test -f docs/track-b/evidence/{cp}/integration.md && head -5 docs/track-b/evidence/{cp}/integration.md",
    ):
        run_shown(command, repo)
    return 0


# ---- the Integration Critic (item 5) ----------------------------------------------------------

def critic_records(cp: str) -> list[dict]:
    path = os.path.join(state_dir(cp), "critic-open.json")
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def save_records(cp: str, records: list[dict]) -> None:
    with open(os.path.join(state_dir(cp), "critic-open.json"), "w", encoding="utf-8") as handle:
        json.dump(records, handle, indent=2, sort_keys=True)
        handle.write("\n")


def clean_at(path: str, sha: str) -> bool:
    if not os.path.isdir(path):
        return False
    status = git("status", "--porcelain=v1", cwd=path, check=False)
    return not status.strip() and resolve("HEAD", cwd=path) == sha


def cmd_critic_open(args: argparse.Namespace) -> int:
    cp = args.cp
    sha = resolve(args.sha)
    if not sha:
        raise SystemExit(f"gauntlet: {args.sha} does not resolve")
    with open(args.assignment, "rb") as handle:
        raw = handle.read()
    text = raw.decode("utf-8")
    plan = re.search(r"^Plan:\s*(\S+)", text, flags=re.M)
    heading = re.search(r"^Section:\s*(#{1,6} .+?)\s*$", text, flags=re.M)
    if not plan or not heading:
        raise SystemExit("gauntlet: the assignment needs 'Plan: <path>' and 'Section: <### heading>' lines")
    records = critic_records(cp)
    n = max([r["n"] for r in records], default=0) + 1
    root = main_checkout()
    path = os.path.join(root, ".local", "worktrees", cp, f"critic-{n}")
    if os.path.exists(path):
        raise SystemExit(f"gauntlet: {path} already exists")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    git("worktree", "add", "--detach", path, sha, cwd=root)
    if not clean_at(path, sha):
        raise SystemExit(f"gauntlet: {path} is not clean at {sha}")
    verdict = os.path.join(state_dir(cp), f"critic-{n}", "integration.md")
    os.makedirs(os.path.dirname(verdict), exist_ok=True)
    records.append({"n": n, "sha": sha, "worktree": path, "assignment": os.path.abspath(args.assignment),
                    "assignment_sha256": sha256(raw), "plan": plan.group(1), "section": heading.group(1),
                    "verdict": verdict, "opened_utc": now_utc(), "closed_utc": None})
    save_records(cp, records)
    print(f"critic-{n}: clean detached worktree {path} at {sha}")
    print(f"1. cd {path}")
    print("2. Launch one ordinary subagent (subagent_type general-purpose, never a fork) with exactly this prompt:")
    print(f"   Run `git show main:scripts/gauntlet.py | python3 -I - critic-brief {cp}` and follow it exactly.")
    print(f"3. Return to your own checkout, then run `scripts/gauntlet.py critic-close {cp}`.")
    return 0


def open_record(cp: str) -> dict | None:
    records = [r for r in critic_records(cp) if not r.get("closed_utc")]
    return records[-1] if records else None


def cmd_critic_brief(args: argparse.Namespace) -> int:
    cp = args.cp
    record = open_record(cp)
    if record is None or not clean_at(record["worktree"], record["sha"]):
        print("gauntlet: no critic-open record matches a clean worktree at its SHA", file=sys.stderr)
        return 1
    with open(record["assignment"], "rb") as handle:
        raw = handle.read()
    if sha256(raw) != record["assignment_sha256"]:
        print("gauntlet: the assignment changed after critic-open", file=sys.stderr)
        return 1
    excerpt = bar_from_main("bar", record["plan"], record["section"], "--at", record["sha"], "--quote")
    if excerpt.returncode != 0:
        print(excerpt.stderr.decode(errors="replace").strip(), file=sys.stderr)
        return 1
    roles = (show("main", "engineering-role.md") or b"").decode("utf-8")
    templates = (show("main", "docs/track-b/gauntlet-templates.md") or b"").decode("utf-8")
    protocol = section(roles, "## Integration Critic protocol")
    form = section(templates, "## 2. Integration Critic assignment and verdict")
    wt, sha, verdict = record["worktree"], record["sha"], record["verdict"]
    print(f"# Integration Critic — {cp.upper()}\n")
    print("## Candidate")
    print(f"- Full SHA: {sha}")
    print(f"- Clean detached worktree, already created for you: {wt}")
    print(f"- Confirm `git -C {wt} status --porcelain` is empty before and after your review.\n")
    print("## Controlling plan")
    print(f"- File: {record['plan']}   Bar: {record['section']}")
    print(f"- Identity: {excerpt.stderr.decode().strip()}")
    print("- Verbatim bar excerpt (confirm it appears in that file at this SHA, for example with "
          f"`git show main:scripts/bar.py | python3 -I - check <your verdict> --source {record['plan']}@{sha}`):\n")
    print(excerpt.stdout.decode("utf-8"))
    print("## The Lead's assignment\n")
    print(raw.decode("utf-8").rstrip() + "\n")
    print("## Fixed rules for this review")
    print(f"- Run every command as `git -C {wt} …` or `cd {wt} && …`: a `cd` does not persist between tool calls.")
    print("- Perform no Git write of any kind: no commit, branch, tag, stash, push or worktree command.")
    print(f"- Write your verdict to this absolute path, outside the worktree: {verdict}")
    print("- Leave the worktree in place; the Lead removes it with critic-close.\n")
    print(protocol)
    print(form)
    return 0


def cmd_critic_close(args: argparse.Namespace) -> int:
    cp = args.cp
    records = critic_records(cp)
    record = open_record(cp)
    if record is None:
        raise SystemExit(f"gauntlet: no open Critic record for {cp}")
    if not clean_at(record["worktree"], record["sha"]):
        print(f"gauntlet: {record['worktree']} is not clean at {record['sha']}; nothing removed")
        return 1
    if not os.path.exists(record["verdict"]):
        print(f"gauntlet: no verdict at {record['verdict']}; nothing removed")
        return 1
    with open(record["verdict"], "rb") as handle:
        digest = sha256(handle.read())
    git("worktree", "remove", record["worktree"], cwd=main_checkout())
    git("worktree", "prune", cwd=main_checkout())
    for r in records:
        if r["n"] == record["n"]:
            r["closed_utc"], r["verdict_sha256"] = now_utc(), digest
    save_records(cp, records)
    print(f"critic-{record['n']}: worktree removed; verdict sha256 {digest}")
    print(f"Copy it to {EVIDENCE.format(cp=cp)}integration.md and commit it as the sole Git writer.")
    return 0


# ---- disposition and reclamation (item 4) -----------------------------------------------------

def cmd_inspect(args: argparse.Namespace) -> int:
    repo = main_checkout()
    tip = resolve(args.branch)
    if not tip:
        raise SystemExit(f"gauntlet: {args.branch} does not resolve")
    for command in ("git --no-pager worktree list", "git --no-pager branch -vv",
                    "git --no-pager tag --list 'land/*' 'evidence/*' 'archive/*'",
                    f"git --no-pager log --oneline --graph main..{tip}",
                    f"git --no-pager diff --stat main...{tip}"):
        run_shown(command, repo)
    if args.final:
        run_shown(f"git --no-pager diff --name-only {args.final}..{tip}", repo)
    if not args.branch.startswith("gauntlet/"):
        others = [r for r in git("for-each-ref", "--format=%(refname)").split()
                  if r not in (f"refs/heads/{args.branch}", f"refs/remotes/{args.branch}")]
        only = [s for s in git("rev-list", tip, "--not", *others).split() if s]
        ahead, behind = git("rev-list", "--left-right", "--count", f"{tip}...main").split()
        when = git("log", "-1", "--format=%cI", tip).strip()
        attached = [w.get("worktree") for w in worktrees() if w.get("HEAD") == tip]
        print(f"unknown branch {args.branch}: tip {tip[:12]} committed {when}; {ahead} ahead, {behind} behind main; "
              f"worktrees at its tip: {attached or 'none'}; {len(only)} commit(s) reachable only from it")
        for sha in only:
            hits = git("grep", "-l", "-e", sha[:7], "HEAD", "--", ".", check=False).split()
            live = [h.split(":", 1)[-1] for h in hits]
            if live:
                print(f"  {sha[:12]} is cited by: {live}")
        print("Escalate to the Owner with a recommendation; never delete it without a disposition and a tag.")
    return 0


def cmd_citations(args: argparse.Namespace) -> int:
    name = f"gauntlet/{args.cp}"
    hits = git("grep", "-n", "-F", name, "--", ".", check=False).split("\n")
    groups: dict[str, list[str]] = {"live (repoint)": [], "historical (never repointed)": [],
                                    "locked (repoint only under a suspension)": []}
    for hit in filter(None, hits):
        path = hit.split(":", 1)[0]
        if matches(path, LOCKED):
            groups["locked (repoint only under a suspension)"].append(hit)
        elif matches(path, HISTORICAL) or path.startswith(EVIDENCE.format(cp=args.cp)):
            groups["historical (never repointed)"].append(hit)
        else:
            groups["live (repoint)"].append(hit)
    for title, lines in groups.items():
        print(f"{title}: {len(lines)}")
        for line in lines:
            print(f"  {line[:200]}")
    return 0


def cmd_discard(args: argparse.Namespace) -> int:
    tag = f"archive/{args.cp}-attempt-{args.k}"
    tip = resolve(f"gauntlet/{args.cp}")
    if not tip:
        raise SystemExit(f"gauntlet: gauntlet/{args.cp} does not exist")
    if resolve(tag):
        raise SystemExit(f"gauntlet: {tag} already exists")
    git("tag", tag, tip)
    print(f"tagged {tag} at {tip}")
    return 0


def cmd_reclaim(args: argparse.Namespace) -> int:
    cp, root = args.cp, main_checkout()
    branch = f"gauntlet/{cp}"
    tip = resolve(f"refs/heads/{branch}")
    if not tip:
        raise SystemExit(f"gauntlet: {branch} does not exist (only gauntlet/* branches are reclaimed here)")
    tags = [f"evidence/{cp}"] if args.disposition == "land" else []
    tags += [t for t in git("tag", "--list", f"archive/{cp}-attempt-*").split() if t]
    keeping = [t for t in tags if resolve(t) and git_ok("merge-base", "--is-ancestor", tip, t)]
    if not keeping:
        print(f"gauntlet: refused. No tag ({tags or 'none'}) resolves and contains the tip {tip[:12]}.")
        return 1
    if args.disposition == "land" and not resolve(f"land/{cp}"):
        print(f"gauntlet: refused. land/{cp} does not resolve.")
        return 1
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    folder = os.path.join(root, ".local", "artifacts", f"{cp}-reclaim-{stamp}")
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "refs-before.txt"), "w", encoding="utf-8") as handle:
        handle.write(git("for-each-ref", "--format=%(refname) %(objectname)"))
    bundle = os.path.join(folder, f"gauntlet-{cp}.bundle")
    base = git("merge-base", "main", tip).strip()
    if base != tip:
        git("bundle", "create", bundle, f"{base}..{branch}", cwd=root)
        git("bundle", "verify", bundle, cwd=root)
    else:
        bundle = "none needed: the branch has no commit beyond main"
    prefix = os.path.join(root, ".local", "worktrees", cp) + os.sep
    for item in worktrees(cwd=root):
        path = item.get("worktree", "")
        if path.startswith(prefix):
            done = subprocess.run(["git", "worktree", "remove", path], capture_output=True, text=True, cwd=root)
            if done.returncode != 0:
                print(f"gauntlet: stopped. {path} could not be removed cleanly: {done.stderr.strip()}")
                return 1
            print(f"removed worktree {path}")
    git("branch", "-D", branch, cwd=root)
    git("worktree", "prune", cwd=root)
    leftover = prefix.rstrip(os.sep)
    if os.path.isdir(leftover) and set(os.listdir(leftover)) <= {".DS_Store"}:
        shutil.rmtree(leftover)
    print(f"reclaimed {branch} (was {tip}); kept by {keeping}; verified bundle {bundle}")
    print("Repoint the live documents `citations` lists, in the same operation.")
    return 0


def cmd_land_commands(args: argparse.Namespace) -> int:
    cp = args.cp
    tip = resolve(f"gauntlet/{cp}")
    if not tip:
        raise SystemExit(f"gauntlet: gauntlet/{cp} does not exist")
    message = f".local/artifacts/{cp}/land-commit-message.txt"
    print(f"# The Owner's LAND for {cp}, by hand, from the repository root. This script never runs it.")
    print("# Non-interactive throughout: no pager, no editor.")
    for line in ("git switch main",
                 "git --no-pager status --short --branch",
                 f"git merge --squash gauntlet/{cp}",
                 "git --no-pager diff --cached --stat | tail -1",
                 f"git commit -F {message}",
                 f"git tag land/{cp} HEAD",
                 f"git tag evidence/{cp} {tip}",
                 f"git push origin main land/{cp} evidence/{cp}"):
        print(line)
    if not os.path.exists(os.path.join(main_checkout(), message)):
        print(f"# Note: {message} does not exist yet; the Orchestrator prepares it.")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="gauntlet.py", description=__doc__.split("\n")[0],
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog="\n".join(__doc__.split("\n")[18:]))
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("start"); p.add_argument("cp"); p.set_defaults(func=cmd_start)
    p = sub.add_parser("return"); p.add_argument("cp"); p.add_argument("final")
    p.add_argument("tip", nargs="?", default="HEAD"); p.set_defaults(func=cmd_return)
    p = sub.add_parser("receipt"); p.add_argument("cp"); p.add_argument("final"); p.add_argument("tip")
    p.set_defaults(func=cmd_receipt)
    p = sub.add_parser("critic-open"); p.add_argument("cp"); p.add_argument("sha"); p.add_argument("assignment")
    p.set_defaults(func=cmd_critic_open)
    p = sub.add_parser("critic-brief"); p.add_argument("cp"); p.set_defaults(func=cmd_critic_brief)
    p = sub.add_parser("critic-close"); p.add_argument("cp"); p.set_defaults(func=cmd_critic_close)
    p = sub.add_parser("inspect"); p.add_argument("branch"); p.add_argument("--final")
    p.set_defaults(func=cmd_inspect)
    p = sub.add_parser("citations"); p.add_argument("cp"); p.set_defaults(func=cmd_citations)
    p = sub.add_parser("discard"); p.add_argument("cp"); p.add_argument("k"); p.set_defaults(func=cmd_discard)
    p = sub.add_parser("reclaim"); p.add_argument("cp")
    p.add_argument("--disposition", choices=("land", "discard"), required=True,
                   help="the Owner's disposition; reclaim refuses a branch nobody dispositioned")
    p.set_defaults(func=cmd_reclaim)
    p = sub.add_parser("land-commands"); p.add_argument("cp"); p.set_defaults(func=cmd_land_commands)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
