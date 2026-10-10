"""The publication tools of the automation plan (items 6 and 7): `scripts/publication_receipt.py` and
`scripts/prerelease.py`, run against fakes -- no network, no Hub, no subprocess beyond `git rev-parse`."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import deploy_space  # noqa: E402
import prerelease as PRE  # noqa: E402
import publication_receipt as R  # noqa: E402
from build_wasm_space import bundle_sha256  # noqa: E402

INJECTION = b'<script>window.huggingface={variables:{"SPACE_CREATOR_USER_ID":"0123abcd"}};</script>'
PAGE = b"<!DOCTYPE html><html><head><title>demo</title><script>app()</script></head><body></body></html>"
SECRET = ("FIXTURE_TOKEN", b"fixture-secret-value-0123456789")


@pytest.fixture
def bundle(tmp_path: Path, monkeypatch) -> Path:
    monkeypatch.setenv("SECRET_GUARD_ENV_ONLY", "1")
    root = tmp_path / "bundle"
    (root / "assets").mkdir(parents=True)
    (root / "index.html").write_bytes(PAGE)
    (root / "assets" / "app.js").write_text("console.log('demo')\n")
    (root / "README.md").write_text("---\nsdk: static\n---\n# demo\n")
    return root


class FakeHub:
    def __init__(self, files, *, sdk="static", private=False):
        self.files, self.sdk, self.private = files, sdk, private

    def identity(self):
        return {"sdk": self.sdk, "private": self.private, "revision": "f" * 40, "stage": "RUNNING"}

    def tree(self, revision):
        assert revision == "f" * 40
        return self.files


# --- item 6: the post-deploy receipt -------------------------------------------------------------------------------

def test_only_the_hugging_face_script_is_removed():
    served = PAGE.replace(b"<head>", b"<head>" + INJECTION)
    normalized, found = R.normalize_space_page(served)
    assert (normalized, found) == (PAGE, 1)
    assert R.normalize_space_page(PAGE) == (PAGE, 0)
    assert b"<script>app()</script>" in normalized


def test_the_space_page_matches_only_after_the_injection_is_removed(bundle):
    served = PAGE.replace(b"<head>", b"<head>" + INJECTION)
    ok = R.check_space_page(bundle, "https://space", get=lambda url: served)
    assert ok["passed"] and not ok["exact_bytes_match"] and ok["injected_script_count"] == 1
    assert ok["normalized_sha256"] == hashlib.sha256(PAGE).hexdigest() != ok["sha256"]
    tampered = R.check_space_page(bundle, "https://space", get=lambda url: served.replace(b"demo", b"other"))
    assert not tampered["passed"]


def test_the_space_files_must_be_the_reviewed_bundle(bundle):
    expected = bundle_sha256(bundle)
    served = deploy_space.local_files(bundle)
    assert R.check_space_files(bundle, expected, hub=FakeHub(served))["passed"]
    changed = {**served, "assets/app.js": {"sha1": "0" * 40, "sha256": None}}
    result = R.check_space_files(bundle, expected, hub=FakeHub(changed))
    assert not result["passed"] and result["mismatched"] == ["assets/app.js"]
    extra = {**served, "style.css": {"sha1": "1" * 40, "sha256": None}}
    assert R.check_space_files(bundle, expected, hub=FakeHub(extra))["extra"] == ["style.css"]
    assert not R.check_space_files(bundle, expected, hub=FakeHub(served, private=True))["passed"]
    with pytest.raises(SystemExit, match="not the reviewed"):
        R.check_space_files(bundle, "0" * 64, hub=FakeHub(served))


def test_pages_and_github_compare_intended_with_observed():
    page = b"<html>report</html>"
    assert R.check_pages("abc", "https://pages", page=lambda c: page, get=lambda u: page)["passed"]
    assert not R.check_pages("abc", "https://pages", page=lambda c: page, get=lambda u: page + b" ")["passed"]
    assert R.check_github("a" * 40, remote=lambda: "a" * 40)["passed"]
    assert not R.check_github("a" * 40, remote=lambda: "b" * 40)["passed"]


def test_every_attempt_and_the_first_failure_are_kept():
    outcomes = iter([{"passed": False, "observed": "stale"}, RuntimeError("HTTP Error 429"),
                     {"passed": True, "intended": "x", "observed": "x"}])

    def check():
        outcome = next(outcomes)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome

    waits: list[float] = []
    result = R.attempt(check, retries=3, wait=7, sleep=waits.append)
    assert result["passed"] and len(result["attempts"]) == 3 and waits == [7, 7]
    assert result["first_failure"]["observed"] == "stale"
    assert result["attempts"][1]["error"] == "RuntimeError: HTTP Error 429"
    gave_up = R.attempt(lambda: {"passed": False, "observed": "old"}, retries=1, wait=0, sleep=lambda s: None)
    assert not gave_up["passed"] and len(gave_up["attempts"]) == 2


def test_the_receipt_writes_one_record_and_fails_on_any_surface(tmp_path):
    checks = {"GitHub main": lambda: {"passed": True, "intended": "a", "observed": "a"},
              "GitHub Pages": lambda: {"passed": False, "intended": "h1", "observed": "h2"}}
    body, code = R.receipt("a" * 40, tmp_path, "e" * 64, tmp_path / "out", "2026-10-11", retries=1, wait=0,
                           checks=checks, sleep=lambda s: None)
    record = json.loads((tmp_path / "out" / "2026-10-11-publication-receipt.json").read_text())
    assert code == 1 and record["status"] == "FAIL" and body["status"] == "FAIL"
    assert set(record["surfaces"]) == {"GitHub main", "GitHub Pages"}
    assert len(record["surfaces"]["GitHub Pages"]["attempts"]) == 2
    rows = body["table"]
    assert rows[0].startswith("| Surface | Intended identity |")
    assert "| GitHub Pages | `h1` | `h2`" in rows[3] and "FAIL after 1 retry" in rows[3] and "recheck" in rows[3]
    passing = {"GitHub main": lambda: {"passed": True, "intended": "a", "observed": "a"}}
    assert R.receipt("a" * 40, tmp_path, "e" * 64, tmp_path / "ok", "d", checks=passing)[1] == 0


# --- item 7: the pre-review check runner ---------------------------------------------------------------------------

def test_the_ci_steps_come_from_the_workflow():
    runs, conditional = PRE.ci_steps()
    argvs = [argv for _, argv in runs]
    assert ["uv", "sync", "--locked", "--dev"] in argvs and ["uv", "run", "pytest", "-q"] in argvs
    assert all(argv[0] != "uses" for argv in argvs)
    assert any("publication_guard" in name or "placeholder" in name.lower() for name in conditional)


def test_the_plan_runs_in_the_runbook_order(tmp_path):
    checks = PRE.plan("pre-final", tmp_path / "env")
    names = [c["name"] for c in checks]
    assert names[0] == "Python 3.13, before pytest: Build the browser payload (M3.5 item 2)"
    assert names[1] == "pytest, Python 3.13" and checks[1]["env"] == {"UV_PYTHON": "3.13"}
    tail = ["make verify", "make lint-publication", "rebuild the presentation",
            "the tree is unchanged after the rebuild", "links", "publication guard (tree)"]
    assert names[-len(tail):] == tail
    ci = [c for c in checks if c["name"].startswith("CI, Python 3.12")]
    assert ci and all(c["env"] == {"UV_PROJECT_ENVIRONMENT": str(tmp_path / "env"), "UV_PYTHON": "3.12"} for c in ci)
    assert checks[-1]["expect"] == [1] and PRE.plan("final", tmp_path / "env")[-1]["expect"] == [0]


def test_credential_lines_are_dropped_and_named():
    text = f"ok line\nurl?token={SECRET[1].decode()}\nlast line\n"
    kept, found = PRE.redact(text, [SECRET])
    assert kept == "ok line\nlast line\n" and found == ["FIXTURE_TOKEN"]
    assert SECRET[1].decode() not in kept


def test_pytest_counts_are_read_from_the_summary():
    out = "....\n= 1474 passed, 13 skipped, 1 error in 312.40s (0:05:12) =\n"
    assert PRE.counts(out) == {"passed": 1474, "skipped": 13, "error": 1}
    assert PRE.counts("no summary here\n") == {}


class FakeRunner:
    def __init__(self, results):
        self.results, self.calls = results, []

    def __call__(self, argv, **kwargs):
        self.calls.append((argv, kwargs.get("env", {})))
        code, out = self.results.get(" ".join(argv), (0, ""))
        return subprocess.CompletedProcess(argv, code, stdout=out, stderr="")


def test_the_run_records_only_what_the_plan_allows(tmp_path):
    runner = FakeRunner({
        "uv run pytest -q": (0, f"= 10 passed in 1.0s =\nleak {SECRET[1].decode()}\n"),
        "git status --porcelain": (0, " M docs/index.html\n"),
        "python3 scripts/publication_guard.py tree": (1, "non-final build record\n"),
    })
    body, code = PRE.prerelease("pre-final", "2026-10-11", tmp_path / "out", tmp_path / "raw", runner=runner,
                                secrets=[SECRET])
    text = (tmp_path / "out" / "2026-10-11-prerelease.json").read_text()
    record = json.loads(text)
    assert code == 1 and record["status"] == "FAIL" and SECRET[1].decode() not in text
    by_name = {c["name"]: c for c in record["checks"]}
    assert by_name["pytest, Python 3.13"]["result"] == "UNEXPECTED"
    assert by_name["pytest, Python 3.13"]["credential_values_found"] == [
        "the value of FIXTURE_TOKEN; its lines were dropped"]
    assert by_name["the tree is unchanged after the rebuild"]["result"] == "UNEXPECTED"
    assert by_name["publication guard (tree)"]["result"] == "as expected"
    allowed = {"name", "argv", "expected_exit", "exit", "seconds", "counts", "result", "python", "changed_paths",
               "credential_values_found"}
    assert all(set(check) <= allowed for check in record["checks"])
    logs = sorted((tmp_path / "raw" / "2026-10-11").glob("*.log"))
    assert logs and all(SECRET[1].decode() not in log.read_text() for log in logs)
    ci_envs = [env for argv, env in runner.calls if env.get("UV_PYTHON") == "3.12"]
    assert ci_envs and all(env["UV_PROJECT_ENVIRONMENT"] == str(tmp_path / "raw" / "py312-env") for env in ci_envs)


def test_a_check_never_inherits_the_callers_uv_selection(tmp_path, monkeypatch):
    monkeypatch.setenv("UV_PYTHON", "3.99")
    monkeypatch.setenv("UV_PROJECT_ENVIRONMENT", "/elsewhere")
    runner = FakeRunner({})
    PRE.prerelease("final", "d", tmp_path / "out", tmp_path / "raw", runner=runner, secrets=[])
    envs = {" ".join(argv): env for argv, env in runner.calls}
    assert envs["uv run pytest -q"]["UV_PYTHON"] in ("3.13", "3.12")
    assert all(env.get("UV_PYTHON") != "3.99" and env.get("UV_PROJECT_ENVIRONMENT") != "/elsewhere"
               for env in envs.values())
    assert "UV_PYTHON" not in envs["make verify"] and "UV_PROJECT_ENVIRONMENT" not in envs["make verify"]


def test_a_clean_run_passes_and_a_dirty_tree_is_refused(tmp_path, monkeypatch):
    runner = FakeRunner({"python3 scripts/publication_guard.py tree": (1, "")})
    body, code = PRE.prerelease("pre-final", "d", tmp_path / "out", tmp_path / "raw", runner=runner, secrets=[])
    assert code == 0 and body["status"] == "PASS" and not body["partial"]
    monkeypatch.setattr(PRE, "clean_tree", lambda: [" M scripts/x.py"])
    assert PRE.main(["--out-dir", str(tmp_path / "never")]) == 2
    assert not (tmp_path / "never").exists()
