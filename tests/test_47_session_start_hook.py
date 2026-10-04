"""The SessionStart hook (automation plan item 3): it restores the secret guard's `core.hooksPath`,
reports the git state in a few lines, and never fails a session."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / ".claude" / "hooks" / "session_start.py"


def env(tmp_path: Path) -> dict[str, str]:
    clean = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    clean.update(GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@example.com", GIT_COMMITTER_NAME="t",
                 GIT_COMMITTER_EMAIL="t@example.com", GIT_CONFIG_GLOBAL=str(tmp_path / "gitconfig"),
                 GIT_CONFIG_NOSYSTEM="1")
    return clean


def run_hook(cwd: Path, e: dict[str, str]) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(HOOK)], input=json.dumps({"cwd": str(cwd), "source": "startup"}),
                          capture_output=True, text=True, env=e, cwd=cwd)


def make_repo(tmp_path: Path, e: dict[str, str]) -> Path:
    repo = tmp_path / "repo"
    (repo / ".githooks").mkdir(parents=True)
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=repo, env=e, check=True)
    (repo / "a.txt").write_text("a\n")
    subprocess.run(["git", "add", "a.txt"], cwd=repo, env=e, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "a"], cwd=repo, env=e, check=True)
    return repo


def hooks_path(repo: Path, e: dict[str, str]) -> str:
    return subprocess.run(["git", "config", "--get", "core.hooksPath"], cwd=repo, env=e,
                          capture_output=True, text=True).stdout.strip()


def test_the_hook_sets_an_unset_guard_and_reports_briefly(tmp_path):
    e = env(tmp_path)
    repo = make_repo(tmp_path, e)
    done = run_hook(repo, e)
    assert done.returncode == 0
    assert Path(hooks_path(repo, e)).resolve() == (repo / ".githooks").resolve()
    lines = done.stdout.strip().split("\n")
    assert len(lines) <= 11
    assert "core.hooksPath was unset" in lines[0] and lines[-1].startswith("Checkpoint tools:")
    again = run_hook(repo, e)
    assert "core.hooksPath" not in again.stdout and "git: main at" in again.stdout


def test_the_hook_repairs_a_guard_pointing_at_a_missing_directory(tmp_path):
    e = env(tmp_path)
    repo = make_repo(tmp_path, e)
    subprocess.run(["git", "config", "core.hooksPath", str(tmp_path / "gone")], cwd=repo, env=e, check=True)
    done = run_hook(repo, e)
    assert done.returncode == 0 and "set to" in done.stdout
    assert Path(hooks_path(repo, e)).resolve() == (repo / ".githooks").resolve()


def test_the_hook_never_fails_outside_a_repository(tmp_path):
    e = env(tmp_path)
    outside = tmp_path / "plain"
    outside.mkdir()
    done = run_hook(outside, e)
    assert done.returncode == 0 and "session-start hook:" in done.stdout


def test_the_settings_wire_the_hook_for_every_session_start():
    settings = json.loads((ROOT / ".claude" / "settings.json").read_text())
    entry = settings["hooks"]["SessionStart"][0]
    assert set(entry["matcher"].split("|")) >= {"startup", "resume", "clear", "compact"}
    assert entry["hooks"][0]["command"].endswith('.claude/hooks/session_start.py"')
