"""Publication Standard v1 §9 (brief W10): no placeholder or non-final build record reaches `main`.

The publication guard runs from `.githooks/pre-push` after the secret guard, which still runs first
and still fails closed; a CI step is its backstop. The guard and the real hook are exercised in a
throwaway repository: a placeholder, a non-final record, a missing record, an unreadable commit and
a missing guard all block; a final build bound for `main`, and anything bound elsewhere, passes; a
credential in the outgoing commit is blocked by the secret guard before the publication guard runs.
No credential is read or printed: the secret guard is restricted to the test's own environment.
"""

from __future__ import annotations

import json
import os
import secrets
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from delu_forecast.claims import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT / "scripts"))

import publication_guard as P  # noqa: E402

FINAL = json.dumps({"final": True}) + "\n"
DRAFT = json.dumps({"final": False}) + "\n"


def test_the_findings_rule():
    assert P.findings_for("<p>page</p>", FINAL) == []
    assert P.findings_for('<span data-unpublished="mlflow:cp20">x</span>', FINAL)
    assert P.findings_for("<p>page</p>", DRAFT)
    assert P.findings_for(None, FINAL) and P.findings_for("<p>page</p>", None)
    assert P.findings_for("<p>page</p>", "not json")


@pytest.fixture()
def repo(tmp_path):
    """A throwaway repository with the project's hooks and guards, and a fixture credential."""
    token = secrets.token_hex(20)
    env = {key: value for key, value in os.environ.items()
           if not any(word in key for word in ("TOKEN", "PASSWORD", "SECRET", "KEY"))}
    env.update(SECRET_GUARD_ENV_ONLY="1", GUARD_FIXTURE_TOKEN=token, HOME=str(tmp_path),
               GIT_CONFIG_GLOBAL=str(tmp_path / "gitconfig"), GIT_CONFIG_NOSYSTEM="1")
    path = tmp_path / "repo"
    (path / "scripts").mkdir(parents=True)
    (path / ".githooks").mkdir()
    for name in ("secret_guard.py", "publication_guard.py"):
        shutil.copy2(REPO_ROOT / "scripts" / name, path / "scripts" / name)
    shutil.copy2(REPO_ROOT / ".githooks" / "pre-push", path / ".githooks" / "pre-push")
    subprocess.run(["git", "init", "-q", str(path)], check=True, env=env)
    for key, value in (("user.email", "t@example.invalid"), ("user.name", "t"), ("commit.gpgsign", "false")):
        subprocess.run(["git", "config", key, value], cwd=path, check=True, env=env)
    return path, env, token


def commit(repo, page: str, record: str | None, extra: str = "") -> str:
    path, env, _ = repo
    (path / "docs").mkdir(exist_ok=True)
    (path / "reports" / "cp3").mkdir(parents=True, exist_ok=True)
    (path / "docs" / "index.html").write_text(page)
    record_path = path / "reports" / "cp3" / "pages_build.json"
    if record is None:
        record_path.unlink(missing_ok=True)
    else:
        record_path.write_text(record)
    (path / "notes.txt").write_text(extra)
    subprocess.run(["git", "add", "-A"], cwd=path, check=True, env=env)
    subprocess.run(["git", "commit", "-q", "-m", "c", "--allow-empty"], cwd=path, check=True, env=env)
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=path, check=True, env=env,
                          capture_output=True, text=True).stdout.strip()


def push_line(sha: str, remote_ref: str = "refs/heads/main") -> str:
    return f"refs/heads/work {sha} {remote_ref} {'0' * 40}\n"


def guard(repo, stdin: str) -> subprocess.CompletedProcess:
    path, env, _ = repo
    return subprocess.run([sys.executable, str(path / "scripts" / "publication_guard.py"), "pre-push", "origin",
                           "https://example.invalid/repo.git"], cwd=path, env=env, input=stdin,
                          capture_output=True, text=True)


def hook(repo, stdin: str) -> subprocess.CompletedProcess:
    path, env, _ = repo
    return subprocess.run(["sh", str(path / ".githooks" / "pre-push"), "origin", "https://example.invalid/repo.git"],
                          cwd=path, env=env, input=stdin, capture_output=True, text=True)


def test_a_final_build_bound_for_main_passes(repo):
    sha = commit(repo, "<p>page</p>", FINAL)
    assert guard(repo, push_line(sha)).returncode == 0
    assert hook(repo, push_line(sha)).returncode == 0


def test_negative_control_a_placeholder_bound_for_main_is_blocked(repo):
    sha = commit(repo, '<span data-unpublished="mlflow:experiment">x</span>', FINAL)
    result = hook(repo, push_line(sha))
    assert result.returncode == 1 and "placeholder" in result.stderr


def test_negative_control_a_non_final_build_record_bound_for_main_is_blocked(repo):
    sha = commit(repo, "<p>page</p>", DRAFT)
    result = hook(repo, push_line(sha))
    assert result.returncode == 1 and "non-final build record" in result.stderr


def test_negative_control_a_missing_record_or_an_unreadable_commit_is_blocked(repo):
    sha = commit(repo, "<p>page</p>", None)
    assert guard(repo, push_line(sha)).returncode == 1
    assert guard(repo, push_line("f" * 40)).returncode == 1
    assert guard(repo, "garbled line\n").returncode == 1


def test_a_push_elsewhere_or_a_deletion_is_not_checked(repo):
    sha = commit(repo, "<p>page</p>", DRAFT)
    assert guard(repo, push_line(sha, "refs/heads/gauntlet/pres-1")).returncode == 0
    assert guard(repo, f"(delete) {'0' * 40} refs/heads/main {sha}\n").returncode == 0


def test_the_secret_guard_runs_first_and_still_fails_closed(repo):
    _, _, token = repo
    sha = commit(repo, "<p>page</p>", DRAFT, extra=f"leak {token}\n")
    result = hook(repo, push_line(sha))
    assert result.returncode == 1
    assert "secret-guard: BLOCKED" in result.stderr
    assert "publication-guard" not in result.stderr, "the publication guard runs only after the secret guard passes"
    assert token not in result.stderr + result.stdout


def test_negative_control_a_missing_publication_guard_fails_closed(repo):
    path, _, _ = repo
    sha = commit(repo, "<p>page</p>", FINAL)
    (path / "scripts" / "publication_guard.py").unlink()
    result = hook(repo, push_line(sha))
    assert result.returncode == 1 and "refusing to push unchecked" in result.stderr


def test_the_hook_orders_the_guards_and_ci_has_the_backstop():
    text = (REPO_ROOT / ".githooks" / "pre-push").read_text()
    assert text.index("scripts/secret_guard.py") < text.index("scripts/publication_guard.py")
    assert os.access(REPO_ROOT / ".githooks" / "pre-push", os.X_OK)
    workflow = (REPO_ROOT / ".github" / "workflows" / "tests.yml").read_text()
    assert "python3 scripts/publication_guard.py tree" in workflow
    assert "if: github.ref == 'refs/heads/main'" in workflow


def test_the_tree_mode_reads_the_checked_out_record(tmp_path):
    (tmp_path / "docs").mkdir()
    (tmp_path / "reports" / "cp3").mkdir(parents=True)
    (tmp_path / "docs" / "index.html").write_text("<p>page</p>")
    (tmp_path / "reports" / "cp3" / "pages_build.json").write_text(DRAFT)
    assert P.main(["publication_guard.py", "tree", str(tmp_path)]) == 1
    (tmp_path / "reports" / "cp3" / "pages_build.json").write_text(FINAL)
    assert P.main(["publication_guard.py", "tree", str(tmp_path)]) == 0
