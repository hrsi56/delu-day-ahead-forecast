"""CP-18a item 7, P0-2: the value-free leak scan (`scripts/leak_scan.py`) and its fingerprint generator
(`scripts/credential_fingerprints.py`), on fake fixtures only.

Every scan, hook and generator run happens in a child process whose environment is built from scratch: PATH, a
temporary HOME and git identity, and the fake values this module generates at run time. No real credential is
read, and no token-shaped literal is committed here: tokens, dump lines and prefixes are assembled at run time.
Each test builds its own throwaway repositories with a copy of the scripts and hooks, so nothing depends on
this repository's history, tags or local-only inputs.
"""
from __future__ import annotations

import json
import os
import secrets
import shutil
import string
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import leak_scan  # noqa: E402

NAME = "LEAK_FIXTURE_TOKEN"
NULL = "0" * 40
SCRIPTS = ("secret_guard.py", "leak_scan.py", "credential_fingerprints.py", "publication_guard.py")


def _random(alphabet: str, size: int) -> str:
    return "".join(secrets.choice(alphabet) for _ in range(size))


def _value() -> str:
    """A fake literal value: random hex plus an upper-case letter, so never a placeholder word."""
    return secrets.token_hex(16) + "Q7"


def _environ_repr(name: str, value: str) -> str:
    """A pytest-style environment repr line, assembled so that this file's source never holds one."""
    return "self = " + "environ" + "({'" + name + "': '" + value + "', 'HOME': '/tmp'})\n"


def _base_env(tmp_path: Path) -> dict[str, str]:
    home = tmp_path / "home"
    home.mkdir(exist_ok=True)
    return {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": str(home), "SECRET_GUARD_ENV_ONLY": "1",
            "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": str(home / "gitconfig"),
            "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.invalid",
            "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.invalid", "LC_ALL": "C"}


class Fixture:
    """A throwaway repository holding copies of the scripts and hooks; `env` never holds the fake value."""

    def __init__(self, tmp_path: Path) -> None:
        self.path = tmp_path / "repo"
        self.env = _base_env(tmp_path)
        self.token = secrets.token_hex(20)
        (self.path / "scripts").mkdir(parents=True)
        for name in SCRIPTS:
            shutil.copy2(ROOT / "scripts" / name, self.path / "scripts" / name)
        (self.path / ".githooks").mkdir()
        for hook in ("pre-commit", "commit-msg", "pre-push"):  # never a committed fingerprint file
            shutil.copy2(ROOT / ".githooks" / hook, self.path / ".githooks" / hook)
        self.git("init", "-q", "-b", "main")
        self.git("config", "commit.gpgsign", "false")

    @property
    def fingerprints(self) -> Path:
        return self.path / ".githooks" / "credential-fingerprints.json"

    def git(self, *args: str, check: bool = True, env: dict | None = None) -> subprocess.CompletedProcess:
        return subprocess.run(["git", *args], cwd=self.path, env=env or self.env, check=check,
                              capture_output=True, text=True)

    def run(self, script: str, *args: str, stdin: str = "", env: dict | None = None) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(self.path / "scripts" / script), *args], cwd=self.path,
                              env=env or self.env, input=stdin, capture_output=True, text=True)

    def write_fingerprints(self) -> subprocess.CompletedProcess:
        """Fingerprint the fake value, which exists only in this one child's environment."""
        result = self.run("credential_fingerprints.py", "write", "--env-only", env={**self.env, NAME: self.token})
        assert result.returncode == 0, result.stderr
        return result

    def stage(self, name: str, text: str) -> None:
        (self.path / name).write_text(text)
        self.git("add", name)

    def commit(self, name: str, text: str, message: str = "c") -> str:
        self.stage(name, text)
        self.git("commit", "-q", "-m", message)  # no hooks are configured until a test sets core.hooksPath
        return self.git("rev-parse", "HEAD").stdout.strip()


@pytest.fixture
def repo(tmp_path) -> Fixture:
    return Fixture(tmp_path)


def _output(result: subprocess.CompletedProcess) -> str:
    return result.stdout + result.stderr


def _assert_no_value(result, token: str) -> None:
    output = _output(result)
    assert token not in output and token[:len(token) // 2] not in output


# --- F1: fingerprints ---------------------------------------------------------------------------------------

def test_a_staged_fake_token_is_blocked_by_name_not_value(repo):
    repo.write_fingerprints()
    repo.stage("leak.log", f"debug output {repo.token} end\n")
    result = repo.run("leak_scan.py", "pre-commit")
    assert result.returncode == 1
    assert f"F1 the value of {NAME} appears in leak.log (staged)" in result.stderr
    _assert_no_value(result, repo.token)


def test_a_file_holding_only_the_first_half_is_blocked_by_the_prefix(repo):
    repo.write_fingerprints()
    repo.stage("half.txt", f"truncated: {repo.token[:20]}\n")
    result = repo.run("leak_scan.py", "pre-commit")
    assert result.returncode == 1
    assert f"F1 the first 20 characters of {NAME} appear in half.txt (staged)" in result.stderr
    _assert_no_value(result, repo.token)


def test_a_placeholder_token_passes_f1(repo):
    repo.write_fingerprints()
    repo.stage("notes.txt", "token: FAKE_TOKEN_" + "0" * 12 + "\n")
    result = repo.run("leak_scan.py", "pre-commit")
    assert result.returncode == 0, result.stderr
    assert "F1" not in result.stderr and "absent" not in result.stderr


def test_the_commit_message_is_scanned(repo, tmp_path):
    repo.write_fingerprints()
    message = tmp_path / "MSG"
    message.write_text(f"debug: the token was {repo.token}\n")
    result = repo.run("leak_scan.py", "commit-msg", str(message))
    assert result.returncode == 1 and f"the value of {NAME} appears in the commit message" in result.stderr
    _assert_no_value(result, repo.token)


def test_pre_push_scans_the_outgoing_commits_and_their_messages(repo):
    repo.write_fingerprints()
    clean = repo.commit("a.txt", "clean\n")
    assert repo.run("leak_scan.py", "pre-push", "origin", stdin=f"refs/heads/w {clean} refs/heads/w {NULL}\n"
                    ).returncode == 0
    leaked = repo.commit("b.txt", f"url?x={repo.token}\n")
    result = repo.run("leak_scan.py", "pre-push", "origin", "https://example.invalid/r.git",
                      stdin=f"refs/heads/w {leaked} refs/heads/w {NULL}\n")
    assert result.returncode == 1 and f"{NAME} appears in b.txt (commit {leaked[:10]})" in result.stderr
    _assert_no_value(result, repo.token)
    message_only = repo.commit("c.txt", "clean\n", message=f"note {repo.token}")
    result = repo.run("leak_scan.py", "pre-push", "origin",
                      stdin=f"refs/heads/x {message_only} refs/heads/x {leaked}\n")
    assert result.returncode == 1 and f"the message of commit {message_only[:10]}" in result.stderr
    deletion = repo.run("leak_scan.py", "pre-push", "origin", stdin=f"(delete) {NULL} refs/heads/w {leaked}\n")
    assert deletion.returncode == 0


def test_the_outgoing_set_is_the_secret_guards(repo):
    """The leak scan sends nothing the secret guard would not check, and misses nothing it would."""
    first = repo.commit("a.txt", "one\n")
    second = repo.commit("b.txt", "two\n")
    repo.git("update-ref", "refs/remotes/origin/main", first)
    probe = (f"import sys; sys.path.insert(0, 'scripts'); import leak_scan; "
             f"print(' '.join(leak_scan.outgoing_commits('origin', 'refs/heads/main {second} refs/heads/main "
             f"{first}')))")
    listed = subprocess.run([sys.executable, "-c", probe], cwd=repo.path, env=repo.env, capture_output=True,
                            text=True, check=True).stdout.split()
    assert listed == [second]


# --- F2 and F3: dump shapes and prefixes ----------------------------------------------------------------------

def test_a_runtime_built_environ_repr_is_blocked_by_f2_with_f1_absent(repo):
    repo.stage("trace.log", _environ_repr("SOME_VARIABLE", _random(string.ascii_letters, 16)))
    result = repo.run("leak_scan.py", "pre-commit")
    assert result.returncode == 1
    assert "credential-fingerprints.json is absent; F1 (fingerprints) skipped" in result.stderr
    assert "F2-environ-repr (a Python os.environ repr) in trace.log (staged), line 1" in result.stderr


def test_the_plans_escaped_regex_passes(repo):
    repo.stage("plan.md", "F2 matches `" + r"environ\(\{'[A-Za-z_]+': '" + "` in committed files.\n")
    result = repo.run("leak_scan.py", "pre-commit")
    assert result.returncode == 0, result.stderr


def test_a_known_prefix_is_blocked_by_f3_without_printing_it(repo):
    fake = "gh" + "p_" + _random(string.ascii_letters + string.digits, 36)
    repo.stage("config.yml", f"token: {fake}\n")
    result = repo.run("leak_scan.py", "pre-commit")
    assert result.returncode == 1 and "F3-github-token" in result.stderr and fake not in _output(result)


@pytest.mark.parametrize("line, rule", [
    ("declare -x {name}=\"{value}\"", "F2-env-assignment"),
    ("export {name}={value}", "F2-env-assignment"),
    ("{name}={value}", "F2-env-assignment"),
    ("+ export {name}='{value}'", "F2-env-assignment"),
    ("payload = {{'{name}': '{value}'}}", "F2-credential-entry"),
    ("{{\"{name}\": \"{value}\"}}", "F2-credential-entry"),
    ("GET https://web-api.tp.entsoe.eu/api?documentType=A44&securityToken={uuid}&in_Domain=x",
     "F2-security-token"),
])
def test_dump_shapes_with_literal_values_are_found(line, rule):
    value = _value()
    text = line.format(name="FIXTURE_API_KEY", value=value, uuid=f"{secrets.token_hex(4)}-{secrets.token_hex(2)}-"
                       f"{secrets.token_hex(2)}-{secrets.token_hex(2)}-{secrets.token_hex(6)}")
    assert (rule, 1) in leak_scan.shape_findings(text.encode())


@pytest.mark.parametrize("line", [
    "export HF_TOKEN=$HF_TOKEN",
    "export ENTSOE_API_TOKEN=\"${ENTSOE_API_TOKEN}\"",
    "HF_TOKEN=<your token>",
    "MLFLOW_TRACKING_PASSWORD=REDACTED_VALUE_HERE",
    "export MLFLOW_DISABLE_TELEMETRY=true",
    "TOKENIZERS_PARALLELISM=false",
    "url = f'{BASE}?securityToken={token}&documentType=A44'",
    "securityToken=<redacted>",
    "token = os.environ.get('ENTSOE_API_TOKEN')",
    "{'DAGSHUB_USER_TOKEN': 'set', 'HF_TOKEN': 'unset'}",
    "def test_secret_guard_blocks_a_staged_value_without_printing_it_or_its_prefix():",
])
def test_references_placeholders_and_prose_pass(line):
    assert leak_scan.shape_findings(line.encode()) == []


def test_findings_name_the_line_and_never_the_text():
    value = _value()
    content = f"header\nexport FIXTURE_SECRET={value}\n".encode()
    assert leak_scan.shape_findings(content) == [("F2-env-assignment", 2)]
    findings, suppressed = leak_scan.scan([leak_scan.Item("x.env", "x.env", content)], None, allowlist={})
    assert suppressed == 0 and findings and all(value not in f for f in findings)


def test_the_allowlist_suppresses_only_its_exact_path_and_rule():
    repr_line = _environ_repr("A", "b").encode()
    gh = ("gh" + "p_" + _random(string.ascii_letters, 36)).encode()
    allow = {("logs/old.log", "F2-environ-repr"): "a fixture reason"}
    items = [leak_scan.Item("logs/old.log", "logs/old.log", repr_line + gh),
             leak_scan.Item("logs/new.log", "logs/new.log", repr_line),
             leak_scan.Item("the commit message", None, repr_line)]
    findings, suppressed = leak_scan.scan(items, None, allowlist=allow)
    assert suppressed == 1
    assert [f.split(" in ")[1].split(",")[0] for f in findings] == ["logs/old.log", "logs/new.log",
                                                                    "the commit message"]
    assert "F3-github-token" in findings[0]


def test_every_allowlist_entry_is_exact_reasoned_and_never_f1():
    for (path, rule), reason in leak_scan.ALLOWLIST.items():
        assert rule in leak_scan.RULES and not rule.startswith("F1"), (path, rule)
        assert not any(c in path for c in "*?[") and not path.startswith("/"), path
        assert len(reason.split()) >= 6, (path, rule)
    print(f"\nleak-scan allowlist: {len(leak_scan.ALLOWLIST)} entries")


def test_the_credential_word_prefilter_covers_the_guards_name_rule():
    """The fast prefilter must see every name the secret guard's rule matches."""
    for name in ("X_TOKEN", "my_secret", "DB_PASSWORD", "PASSWD", "OPENAI_APIKEY", "SOME_API_KEY",
                 "AWS_ACCESS_KEY_ID", "SSH_PRIVATE_KEY"):
        assert leak_scan.CREDENTIAL_NAME.search(name)
        line = f"{name}={_value()}".encode()
        assert leak_scan.shape_findings(line) == [("F2-env-assignment", 1)], name


# --- modes, tree and ci -------------------------------------------------------------------------------------

def test_tree_mode_scans_tracked_and_untracked_files_but_not_ignored_ones(repo):
    repo.commit(".gitignore", "ignored/\n")
    (repo.path / "ignored").mkdir()
    (repo.path / "ignored" / "trace.log").write_text(_environ_repr("A", "b"))
    clean = repo.run("leak_scan.py", "tree")
    assert clean.returncode == 0 and "leak-scan: clean" in clean.stdout, clean.stderr
    (repo.path / "new.log").write_text(_environ_repr("A", "b"))
    result = repo.run("leak_scan.py", "tree")
    assert result.returncode == 1 and "in new.log, line 1" in result.stderr


@pytest.mark.parametrize("before", [NULL, "", "${{ github.event.before }}"])
def test_ci_without_a_usable_before_scans_the_tree(repo, before):
    head = repo.commit("trace.log", _environ_repr("A", "b"))
    for after in (head, "${{ github.sha }}", ""):
        result = repo.run("leak_scan.py", "ci", before, after)
        assert result.returncode == 1, result.stderr
        assert "scanning the tree" in result.stderr and "in trace.log, line 1" in result.stderr
    repo.git("rm", "-q", "trace.log")
    repo.git("commit", "-q", "-m", "clean")
    assert repo.run("leak_scan.py", "ci", before, "${{ github.sha }}").returncode == 0
    assert repo.run("leak_scan.py", "ci").returncode == 0


def test_ci_scans_the_pushed_range_after_completing_a_shallow_clone(repo, tmp_path):
    base = repo.commit("a.txt", "clean\n")
    repo.commit("trace.log", _environ_repr("A", "b"))
    repo.git("rm", "-q", "trace.log")
    repo.git("commit", "-q", "-m", "removed again")
    head = repo.git("rev-parse", "HEAD").stdout.strip()
    origin = tmp_path / "origin.git"
    subprocess.run(["git", "clone", "-q", "--bare", str(repo.path), str(origin)], env=repo.env, check=True)
    clone = tmp_path / "clone"
    subprocess.run(["git", "clone", "-q", "--depth", "1", f"file://{origin}", str(clone)], env=repo.env, check=True)
    shutil.copytree(repo.path / "scripts", clone / "scripts")
    scan = [sys.executable, "scripts/leak_scan.py", "ci", base, head]
    result = subprocess.run(scan, cwd=clone, env=repo.env, capture_output=True, text=True)
    assert result.returncode == 1, result.stderr
    assert "scanning 2 pushed commit(s), then the tree" in result.stderr
    assert "F2-environ-repr" in result.stderr and "trace.log (commit" in result.stderr
    # Negative control: the same range in a shallow clone whose origin cannot complete it fails closed.
    stranded = tmp_path / "stranded"
    subprocess.run(["git", "clone", "-q", "--depth", "1", f"file://{origin}", str(stranded)], env=repo.env,
                   check=True)
    subprocess.run(["git", "remote", "set-url", "origin", f"file://{tmp_path / 'missing.git'}"], cwd=stranded,
                   env=repo.env, check=True)
    shutil.copytree(repo.path / "scripts", stranded / "scripts")
    result = subprocess.run(scan, cwd=stranded, env=repo.env, capture_output=True, text=True)
    assert result.returncode == 1 and "the pushed range is unreadable" in result.stderr


def test_ci_refuses_a_range_that_is_not_commit_ids(repo):
    repo.commit("a.txt", "clean\n")
    result = repo.run("leak_scan.py", "ci", "main~1; rm -rf /", "HEAD")
    assert result.returncode == 1 and "not a pair of commit ids" in result.stderr


def test_an_unknown_mode_is_refused(repo):
    assert repo.run("leak_scan.py", "everything").returncode == 2


# --- the fingerprint file -----------------------------------------------------------------------------------

def test_write_prints_names_only_and_the_scanner_accepts_the_file(repo):
    result = repo.write_fingerprints()
    data = json.loads(repo.fingerprints.read_text())
    assert NAME in result.stdout and repo.token not in _output(result)
    assert all(entry["sha256"] not in _output(result) for entry in data["entries"])
    entry = next(e for e in data["entries"] if e["name"] == NAME)
    assert entry["length"] == 40 and entry["alphabet"] == "hex-lower" and entry["prefix_len"] == 20
    assert repo.token not in repo.fingerprints.read_text()
    assert leak_scan.load_fingerprints(repo.fingerprints)


def test_write_is_append_only_and_idempotent(repo):
    repo.write_fingerprints()
    first = json.loads(repo.fingerprints.read_text())["entries"]
    again = repo.run("credential_fingerprints.py", "write", "--env-only", env={**repo.env, NAME: repo.token})
    assert again.returncode == 0 and "already present" in again.stdout
    rotated = secrets.token_hex(20)
    repo.run("credential_fingerprints.py", "write", "--env-only", env={**repo.env, NAME: rotated})
    entries = json.loads(repo.fingerprints.read_text())["entries"]
    assert entries[:len(first)] == first and len(entries) == len(first) + 1
    for value in (repo.token, rotated):  # the revoked value stays detectable
        repo.stage("leak.txt", value + "\n")
        assert repo.run("leak_scan.py", "pre-commit").returncode == 1


def test_a_low_entropy_value_is_refused_and_nothing_is_written(repo):
    weak = secrets.token_hex(8)  # 16 hex characters: 64 bits
    result = repo.run("credential_fingerprints.py", "write", "--env-only", env={**repo.env, NAME: weak})
    assert result.returncode == 1 and "REFUSED" in result.stderr and NAME in result.stderr
    assert "below 128 bits" in result.stderr and weak not in _output(result)
    assert not repo.fingerprints.exists()


def test_write_with_only_restricts_the_names(repo):
    other = secrets.token_hex(20)
    env = {**repo.env, NAME: repo.token, "OTHER_FIXTURE_TOKEN": other}
    result = repo.run("credential_fingerprints.py", "write", "--env-only", "--only", NAME, env=env)
    assert result.returncode == 0
    assert [e["name"] for e in json.loads(repo.fingerprints.read_text())["entries"]] == [NAME]
    missing = repo.run("credential_fingerprints.py", "write", "--env-only", "--only", "ABSENT_TOKEN", env=env)
    assert missing.returncode == 1 and "no value found for ABSENT_TOKEN" in missing.stderr


@pytest.mark.parametrize("mutate", [
    lambda text, data: "{not json",
    lambda text, data: json.dumps({**data, "schema": "other/1"}),
    lambda text, data: json.dumps({**data, "entries": []}),
    lambda text, data: json.dumps({**data, "entries": [{k: v for k, v in data["entries"][0].items()
                                                         if k != "salt"}]}),
    lambda text, data: json.dumps({**data, "entries": [{**data["entries"][0], "alphabet": "emoji"}]}),
    lambda text, data: json.dumps({**data, "entries": [{**data["entries"][0], "length": 16}]}),
    lambda text, data: json.dumps({**data, "entries": [{**data["entries"][0], "sha256": "00"}]}),
])
def test_a_malformed_fingerprint_file_fails_closed(repo, mutate):
    repo.write_fingerprints()
    text = repo.fingerprints.read_text()
    repo.fingerprints.write_text(mutate(text, json.loads(text)))
    repo.stage("clean.txt", "nothing here\n")
    result = repo.run("leak_scan.py", "pre-commit")
    assert result.returncode == 1 and "is malformed" in result.stderr
    refused = repo.run("credential_fingerprints.py", "write", "--env-only", env={**repo.env, NAME: repo.token})
    assert refused.returncode == 1 and "malformed" in refused.stderr


def test_alphabets_and_entropy_estimates():
    assert leak_scan.smallest_alphabet(secrets.token_hex(20)) in ("hex-lower", "hex-upper")
    uuid_like = f"{secrets.token_hex(4)}-{secrets.token_hex(2)}-{secrets.token_hex(2)}-{secrets.token_hex(8)}a"
    assert leak_scan.smallest_alphabet(uuid_like) == "hex-lower-dash"
    assert leak_scan.smallest_alphabet("hf_" + _random(string.ascii_letters, 34)) == "word"
    assert leak_scan.smallest_alphabet("café") is None
    assert leak_scan.bits(40, "hex-lower") == 160
    assert leak_scan.bits(32, "hex-lower") >= leak_scan.MIN_BITS > leak_scan.bits(31, "hex-lower")


# --- the hooks ----------------------------------------------------------------------------------------------

def _hooked(repo: Fixture) -> None:
    repo.git("config", "core.hooksPath", str(repo.path / ".githooks"))


def test_the_pre_commit_hook_runs_the_scan_after_the_guard(repo):
    repo.write_fingerprints()
    _hooked(repo)
    repo.stage("leak.log", f"value {repo.token}\n")
    # No value in the environment (as in CI or a fresh clone): the guard passes and the scan blocks by name.
    result = repo.git("commit", "-q", "-m", "try", check=False)
    assert result.returncode == 1
    assert f"leak-scan: BLOCKED - F1 the value of {NAME} appears in leak.log (staged)" in result.stderr
    _assert_no_value(result, repo.token)
    assert repo.git("rev-parse", "--verify", "-q", "HEAD", check=False).returncode != 0, "nothing was committed"
    # With the value present, the secret guard blocks first and the scan never runs.
    first = repo.git("commit", "-q", "-m", "try", check=False, env={**repo.env, NAME: repo.token})
    assert first.returncode == 1 and "secret-guard: BLOCKED" in first.stderr and "leak-scan" not in first.stderr
    _assert_no_value(first, repo.token)


def test_the_commit_msg_hook_runs_the_scan(repo):
    repo.write_fingerprints()
    _hooked(repo)
    repo.stage("ok.txt", "clean\n")
    result = repo.git("commit", "-q", "-m", f"debug {repo.token}", check=False)
    assert result.returncode == 1 and "F1 the value of" in result.stderr and "the commit message" in result.stderr
    _assert_no_value(result, repo.token)
    assert repo.git("commit", "-q", "-m", "clean message", check=False).returncode == 0


def test_the_pre_push_hook_runs_the_scan_between_the_guards(repo):
    repo.write_fingerprints()
    head = repo.commit("b.txt", f"x={repo.token}\n")
    hook = subprocess.run(["sh", str(repo.path / ".githooks" / "pre-push"), "origin", "https://example.invalid/r"],
                          cwd=repo.path, env=repo.env, input=f"refs/heads/w {head} refs/heads/w {NULL}\n",
                          capture_output=True, text=True)
    assert hook.returncode == 1 and "leak-scan: BLOCKED - F1" in hook.stderr
    assert "publication-guard" not in hook.stderr
    _assert_no_value(hook, repo.token)
    text = (ROOT / ".githooks" / "pre-push").read_text()
    assert text.index('"$guard" "$(basename "$0")"') < text.index('"$leak" pre-push') < text.index(
        '"$publication" pre-push')


@pytest.mark.parametrize("hook", ["pre-commit", "commit-msg", "pre-push"])
def test_a_hook_that_cannot_run_the_scan_refuses(repo, hook):
    (repo.path / "scripts" / "leak_scan.py").unlink()
    repo.commit("a.txt", "clean\n")
    head = repo.git("rev-parse", "HEAD").stdout.strip()
    message = repo.path / "MSG"
    message.write_text("clean\n")
    args = {"pre-commit": [], "commit-msg": [str(message)], "pre-push": ["origin", "https://example.invalid/r"]}
    result = subprocess.run(["sh", str(repo.path / ".githooks" / hook), *args[hook]], cwd=repo.path, env=repo.env,
                            input=f"refs/heads/w {head} refs/heads/w {NULL}\n", capture_output=True, text=True)
    assert result.returncode == 1 and "leak_scan.py is missing; refusing" in result.stderr


@pytest.mark.parametrize("hook", ["pre-commit", "commit-msg", "pre-push"])
def test_each_hook_calls_the_scan_after_the_guard(hook):
    text = (ROOT / ".githooks" / hook).read_text()
    assert os.access(ROOT / ".githooks" / hook, os.X_OK) and text.startswith("#!/bin/sh\n")
    assert "scripts/secret_guard.py" in text and "scripts/leak_scan.py" in text
    guard_runs = text.index('"$guard" "$(basename "$0")"')
    scan_runs = text.index('"$leak" pre-push' if hook == "pre-push" else 'exec "$py" "$leak" "$(basename "$0")"')
    assert guard_runs < scan_runs


def test_ci_runs_the_scan_first():
    import yaml

    steps = yaml.safe_load((ROOT / ".github" / "workflows" / "tests.yml").read_text())["jobs"]["properties"]["steps"]
    assert steps[0]["uses"].startswith("actions/checkout@")
    assert steps[1]["run"] == 'python3 scripts/leak_scan.py ci "${{ github.event.before }}" "${{ github.sha }}"'
    assert "if" not in steps[1]
    assert steps[2]["uses"].startswith("astral-sh/setup-uv@")
