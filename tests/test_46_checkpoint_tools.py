"""The checkpoint tools of the automation plan (items 1, 2, 4, 5 and 8): `scripts/bar.py`,
`scripts/gauntlet.py` and `scripts/progress_diff.py`, each run against a throwaway repository."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PLAN = """# Plan vX-r1 — test anchor

## 1. Alpha

Intro.

### 1.1 Complete checklist

1. **First item.** Do the first thing.
2. **Second item.** Do the second thing.

```text
# a comment in a fence is not a heading
```

### 1.2 Paths

Only these paths.

## 2. Beta

Later.
"""


def env(tmp_path: Path) -> dict[str, str]:
    clean = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    clean.update(GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@example.com", GIT_COMMITTER_NAME="t",
                 GIT_COMMITTER_EMAIL="t@example.com", GIT_CONFIG_GLOBAL=str(tmp_path / "gitconfig"),
                 GIT_CONFIG_NOSYSTEM="1")
    return clean


def git(repo: Path, e: dict[str, str], *args: str) -> str:
    return subprocess.run(["git", *args], cwd=repo, env=e, check=True, capture_output=True, text=True).stdout


def tool(repo: Path, e: dict[str, str], script: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(repo / "scripts" / script), *args], cwd=repo, env=e,
                          capture_output=True, text=True)


@pytest.fixture
def repo(tmp_path: Path):
    e = env(tmp_path)
    path = tmp_path / "repo"
    path.mkdir()
    git(path, e, "init", "-q", "-b", "main")
    (path / "plan.md").write_text(PLAN)
    for rel in ("scripts/bar.py", "scripts/gauntlet.py", "scripts/progress_diff.py", "engineering-role.md",
                "docs/track-b/gauntlet-templates.md"):
        (path / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(ROOT / rel, path / rel)
    git(path, e, "add", "-A")
    git(path, e, "commit", "-q", "-m", "base")
    return path, e


# ---- bar.py ------------------------------------------------------------------------------------

def test_bar_extracts_a_section_verbatim_and_ignores_fenced_hashes(repo):
    path, e = repo
    done = tool(path, e, "bar.py", "bar", "plan.md", "### 1.1 Complete checklist")
    assert done.returncode == 0
    assert done.stdout.startswith("### 1.1 Complete checklist\n")
    assert "# a comment in a fence is not a heading" in done.stdout
    assert "### 1.2" not in done.stdout and done.stdout.endswith("```\n")
    assert "sha256" in done.stderr
    without_hashes = tool(path, e, "bar.py", "bar", "plan.md", "1.1 Complete checklist")
    assert without_hashes.stdout == done.stdout


def test_check_accepts_an_exact_quote_and_names_the_first_doctored_line(repo, tmp_path):
    path, e = repo
    quoted = tool(path, e, "bar.py", "bar", "plan.md", "### 1.1 Complete checklist", "--quote").stdout
    good, bad = tmp_path / "good.md", tmp_path / "bad.md"
    good.write_text("Intro\n\n" + quoted + "\nAfter.\n")
    bad.write_text("Intro\n\n" + quoted.replace("Do the second thing", "Do something else") + "\n")
    assert tool(path, e, "bar.py", "check", str(good), "--source", "plan.md@HEAD").returncode == 0
    refused = tool(path, e, "bar.py", "check", str(bad), "--source", "plan.md@HEAD")
    assert refused.returncode == 1 and "Do something else" in refused.stdout


def brief_text(anchor: str = "`plan.md`, revision vX-r1, §1") -> str:
    return f"""# Track B Checkpoint Brief — CP-9

## Target
- Repository: test, `/tmp/repo`
- Authorized checkpoint: CP-9, exactly one.
- Ratified plan anchor: {anchor}

## Orchestrator-reported expected state
- Branch / commit: main.

## Observable outcome
A result.

## Complete authoritative checkpoint bar
§1.1, all items.

## Applicable constraints
None beyond the plan.

## Timebox
About 6 hours.

## Owner-only actions already authorized
None.

## Stop and return
Return PASS, BLOCKED or INCOMPLETE.
"""


def test_brief_checks_form_placeholders_checkpoint_timebox_and_anchor(repo, tmp_path):
    path, e = repo
    brief = tmp_path / "brief.md"
    brief.write_text(brief_text())
    ok = tool(path, e, "bar.py", "brief", str(brief))
    assert ok.returncode == 0, ok.stdout
    assert "checkpoint CP-9" in ok.stdout and "sha256" in ok.stdout
    brief.write_text(brief_text().replace("CP-9, exactly one.", "[exactly one]"))
    assert tool(path, e, "bar.py", "brief", str(brief)).returncode == 1
    brief.write_text(brief_text(anchor="`plan.md`, §7"))
    unresolved = tool(path, e, "bar.py", "brief", str(brief))
    assert unresolved.returncode == 1 and "§7 does not resolve" in unresolved.stdout
    brief.write_text(brief_text().replace("## Timebox\nAbout 6 hours.", "## Timebox\nSoon."))
    assert tool(path, e, "bar.py", "brief", str(brief)).returncode == 1


def test_identity_prints_the_revision_line_and_hash(repo):
    path, e = repo
    done = tool(path, e, "bar.py", "identity", "plan.md")
    assert done.returncode == 0
    assert "revision line: # Plan vX-r1 — test anchor" in done.stdout and "sha256:" in done.stdout


# ---- gauntlet.py --------------------------------------------------------------------------------

def checkpoint(path: Path, e: dict[str, str], extra_tip_path: str | None = None) -> tuple[str, str]:
    """A gauntlet/cp-9 branch: a candidate commit, then a verdict-only evidence commit."""
    git(path, e, "switch", "-q", "-c", "gauntlet/cp-9")
    (path / "src.py").write_text("x = 1\n")
    git(path, e, "add", "-A")
    git(path, e, "commit", "-q", "-m", "candidate")
    final = git(path, e, "rev-parse", "HEAD").strip()
    evidence = path / "docs/track-b/evidence/cp-9"
    evidence.mkdir(parents=True)
    (evidence / "integration.md").write_text(f"# Verdict — CP-9 — Integration — PASS\n\n"
                                             f"- **Candidate SHA:** `{final}`\n")
    (evidence / "checkpoint-return.md").write_text(f"# Return\n\n## Identity\n- final_candidate_sha: `{final}`\n\n"
                                                   "## Repository state\n")
    (evidence / "issued-brief.md").write_text("brief\n")
    canonical = path / ".local/artifacts/cp-9"
    canonical.mkdir(parents=True, exist_ok=True)
    (canonical / "issued-brief.md").write_text("brief\n")
    if extra_tip_path:
        (path / extra_tip_path).write_text("late change\n")
    git(path, e, "add", "docs", *( [extra_tip_path] if extra_tip_path else []))
    git(path, e, "commit", "-q", "-m", "verdict")
    return final, git(path, e, "rev-parse", "HEAD").strip()


def test_start_records_once_and_return_checks_the_verdict_only_delta(repo):
    path, e = repo
    first = tool(path, e, "gauntlet.py", "start", "cp-9")
    assert first.returncode == 0 and (path / ".local/artifacts/cp-9/start.json").exists()
    assert tool(path, e, "gauntlet.py", "start", "cp-9").returncode == 1
    final, tip = checkpoint(path, e)
    done = tool(path, e, "gauntlet.py", "return", "cp-9", final, tip)
    assert done.returncode == 0, done.stdout
    assert "## Identity" in done.stdout and "created refs/heads/gauntlet/cp-9" in done.stdout
    assert "equal to the canonical copy" in done.stdout and "0 problem(s)" in done.stdout


def test_return_refuses_a_tip_that_leaves_the_evidence_folder(repo):
    path, e = repo
    final, tip = checkpoint(path, e, extra_tip_path="src.py")
    done = tool(path, e, "gauntlet.py", "return", "cp-9", final, tip)
    assert done.returncode == 1 and "the delta leaves" in done.stdout


def test_land_commands_are_printed_non_interactive_and_never_run(repo):
    path, e = repo
    final, tip = checkpoint(path, e)
    before = git(path, e, "rev-parse", "main")
    done = tool(path, e, "gauntlet.py", "land-commands", "cp-9")
    assert done.returncode == 0
    assert "git commit -F .local/artifacts/cp-9/land-commit-message.txt" in done.stdout
    assert "git --no-pager diff --cached --stat" in done.stdout and f"git tag evidence/cp-9 {tip}" in done.stdout
    assert git(path, e, "rev-parse", "main") == before


def test_reclaim_refuses_without_a_tag_then_bundles_and_deletes(repo):
    path, e = repo
    final, tip = checkpoint(path, e)
    git(path, e, "switch", "-q", "main")
    assert tool(path, e, "gauntlet.py", "reclaim", "cp-9", "--disposition", "land").returncode == 1
    git(path, e, "tag", "evidence/cp-9", tip)
    git(path, e, "tag", "land/cp-9", "main")
    done = tool(path, e, "gauntlet.py", "reclaim", "cp-9", "--disposition", "land")
    assert done.returncode == 0, done.stdout
    assert not git(path, e, "branch", "--list", "gauntlet/cp-9").strip()
    bundles = list((path / ".local/artifacts").glob("cp-9-reclaim-*/gauntlet-cp-9.bundle"))
    assert len(bundles) == 1
    git(path, e, "bundle", "verify", str(bundles[0]))


def test_critic_open_brief_close(repo, tmp_path):
    path, e = repo
    final, _ = checkpoint(path, e)
    assignment = tmp_path / "assignment.md"
    assignment.write_text("Plan: plan.md\nSection: ### 1.1 Complete checklist\n\nReproduce: run the tests.\n")
    opened = tool(path, e, "gauntlet.py", "critic-open", "cp-9", final, str(assignment))
    assert opened.returncode == 0, opened.stderr
    worktree = path / ".local/worktrees/cp-9/critic-1"
    assert worktree.is_dir()
    brief = tool(path, e, "gauntlet.py", "critic-brief", "cp-9")
    assert brief.returncode == 0, brief.stderr
    assert "> 2. **Second item.** Do the second thing." in brief.stdout
    assert "## Integration Critic protocol" in brief.stdout and "Perform no Git write" in brief.stdout
    assert "# Verdict — [checkpoint] — Integration" in brief.stdout
    refused = tool(path, e, "gauntlet.py", "critic-close", "cp-9")
    assert refused.returncode == 1 and worktree.is_dir()
    verdict = path / ".local/artifacts/cp-9/critic-1/integration.md"
    verdict.write_text("# Verdict — CP-9 — Integration — PASS\n")
    closed = tool(path, e, "gauntlet.py", "critic-close", "cp-9")
    assert closed.returncode == 0 and not worktree.exists()
    records = json.loads((path / ".local/artifacts/cp-9/critic-open.json").read_text())
    assert records[0]["closed_utc"] and len(records[0]["verdict_sha256"]) == 64
    assert tool(path, e, "gauntlet.py", "critic-brief", "cp-9").returncode == 1


def test_citations_separate_live_historical_and_locked(repo):
    path, e = repo
    (path / "capstone_v99.md").write_text("works on gauntlet/cp-9\n")
    (path / "notes.md").write_text("see gauntlet/cp-9\n")
    git(path, e, "add", "-A")
    git(path, e, "commit", "-q", "-m", "docs")
    done = tool(path, e, "gauntlet.py", "citations", "cp-9")
    live = done.stdout.split("historical")[0]
    assert "notes.md" in live and "capstone_v99.md" not in live
    assert "capstone_v99.md" in done.stdout.split("locked")[1]


def test_receipt_prints_each_listed_command_with_its_exit_code(repo):
    path, e = repo
    final, tip = checkpoint(path, e)
    done = tool(path, e, "gauntlet.py", "receipt", "cp-9", final, tip)
    assert done.returncode == 0
    assert done.stdout.count("$ ") == 5 and done.stdout.count("(exit ") == 5
    assert "# Verdict — CP-9 — Integration — PASS" in done.stdout


# ---- progress_diff.py ---------------------------------------------------------------------------

PROGRESS = """# Programme state

## 1. Current Position

**Next pending Track B checkpoint: CP-9.**

## 2. Setup State

- **ACTION-REQUIRED:** do a thing.

## 3. Strategic Anchors

- anchor

## 4. Standing Scope Decisions

- decision

## 5. Session Log — newest first

- entry recording the CP-9 receipt and its landing

## 6. Blockers / Open Questions

- **Open:** a question.

## 7. Notes for Future Sessions

- note
"""


def test_progress_diff_flags_protected_removals_and_always_exits_zero(repo):
    path, e = repo
    (path / "progress.md").write_text(PROGRESS)
    git(path, e, "add", "progress.md")
    git(path, e, "commit", "-q", "-m", "progress")
    (path / "progress.md").write_text(PROGRESS.replace("- **Open:** a question.\n", "")
                                      .replace("its landing", "its landing, compressed"))
    done = tool(path, e, "progress_diff.py")
    assert done.returncode == 0
    assert "skeleton: 7/7 present" in done.stdout
    assert "! Blockers / Open Questions: - **Open:** a question." in done.stdout
    assert "[edited] - entry recording the CP-9 receipt" in done.stdout
