"""The secret guard blocks a credential *value* in staged content, commit messages and outgoing
commits, and never prints the value it found (AGENTS.md § Credentials).

The fixture token is a random 40-character hex string, the same shape as the DagsHub token that
reached a public commit on 2026-09-24. No pattern scan recognizes that shape. The child
environment drops every real credential and restricts the guard to the environment, so these
tests never touch the developer's own secrets.
"""
from __future__ import annotations

import os
import re
import secrets
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
GUARD = ROOT / "scripts" / "secret_guard.py"
NULL = "0" * 40


@pytest.fixture
def repo(tmp_path):
    token = secrets.token_hex(20)
    env = {k: v for k, v in os.environ.items()
           if not re.search(r"TOKEN|SECRET|PASSWORD|PASSWD|API_?KEY|ACCESS_KEY|PRIVATE_KEY|MLFLOW", k, re.I)}
    env.update(SECRET_GUARD_ENV_ONLY="1", GUARD_FIXTURE_TOKEN=token, HOME=str(tmp_path),
               GIT_CONFIG_NOSYSTEM="1", GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@example.com",
               GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@example.com")
    path = tmp_path / "repo"
    subprocess.run(["git", "init", "-q", str(path)], check=True, env=env)
    return path, env, token


def _git(repo, *args):
    path, env, _ = repo
    return subprocess.run(["git", *args], cwd=path, env=env, check=True,
                          capture_output=True, text=True).stdout.strip()


def _guard(repo, *args, stdin=""):
    path, env, _ = repo
    return subprocess.run([sys.executable, str(GUARD), *args], cwd=path, env=env, input=stdin,
                          capture_output=True, text=True)


def _commit(repo, name, text):
    (repo[0] / name).write_text(text)
    _git(repo, "add", name)
    _git(repo, "commit", "-q", "-m", f"add {name}")
    return _git(repo, "rev-parse", "HEAD")


def test_staged_value_is_blocked_without_printing_it(repo):
    token = repo[2]
    (repo[0] / "leak.log").write_text(f"environ({{'MLFLOW_TRACKING_USERNAME': '{token}'}})\n")
    _git(repo, "add", "leak.log")
    result = _guard(repo, "pre-commit")
    output = result.stdout + result.stderr
    assert result.returncode == 1
    assert "GUARD_FIXTURE_TOKEN" in output and "leak.log" in output
    assert token not in output


def test_clean_staged_content_passes(repo):
    (repo[0] / "notes.md").write_text("MLFLOW_TRACKING_USERNAME is read from the environment.\n")
    _git(repo, "add", "notes.md")
    assert _guard(repo, "pre-commit").returncode == 0


def test_commit_message_is_checked(repo, tmp_path):
    message = tmp_path / "MSG"
    message.write_text(f"debug: token was {repo[2]}\n")
    result = _guard(repo, "commit-msg", str(message))
    assert result.returncode == 1 and repo[2] not in result.stdout + result.stderr


def test_outgoing_commit_is_checked_before_push(repo):
    head = _commit(repo, "report.txt", f"url?securityToken={repo[2]}\n")
    result = _guard(repo, "pre-push", "origin", "https://example.invalid/repo.git",
                    stdin=f"refs/heads/main {head} refs/heads/main {NULL}\n")
    output = result.stdout + result.stderr
    assert result.returncode == 1 and "report.txt" in output and repo[2] not in output


def test_clean_outgoing_commit_passes(repo):
    head = _commit(repo, "report.txt", "no credentials here\n")
    result = _guard(repo, "pre-push", "origin", "https://example.invalid/repo.git",
                    stdin=f"refs/heads/main {head} refs/heads/main {NULL}\n")
    assert result.returncode == 0


def test_short_values_are_not_treated_as_credentials(repo):
    path, env, _ = repo
    env["GUARD_SHORT_TOKEN"] = "abc123"
    (path / "code.py").write_text("x = 'abc123'\n")
    _git(repo, "add", "code.py")
    assert _guard(repo, "pre-commit").returncode == 0


@pytest.mark.parametrize("hook", ["pre-commit", "commit-msg", "pre-push"])
def test_each_hook_routes_to_the_guard(hook):
    wrapper = ROOT / ".githooks" / hook
    assert wrapper.is_file() and os.access(wrapper, os.X_OK)
    assert "scripts/secret_guard.py" in wrapper.read_text()
