"""CP-18a item 7, P0-3 (b): the pytest plugin `tests/environ_redact.py` keeps the environment out of failure output.

Each child pytest run uses this repository's pytest.ini (so the plugin arrives through the real `-p` registration)
and an environment built from scratch: a fake token generated at run time, PATH and a temporary HOME. A test
reads a missing variable with a bare subscript. With the plugin, the output lacks the fake; without it (`-p
no:environ_redact`, the negative control), the output contains it. That proves both the leak mechanism and the
fix, for a failing test, for its captured output and for a collection error, under `python -m pytest` and under
the `pytest` entry point that CI's `uv run pytest` uses.
"""
from __future__ import annotations

import os
import secrets
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
NAME = "REDACT_FIXTURE_TOKEN"

FAILING_TESTS = '''\
import os


def test_reads_a_missing_variable():
    os.environ["CP18A_FAKE_MISSING"]


def test_prints_the_environment_then_fails():
    print(os.environ)
    assert False
'''
COLLECTION_ERROR = '''\
import os

VALUE = os.environ["CP18A_FAKE_MISSING"]
'''
ENTRY_POINTS = {"python -m pytest": [sys.executable, "-m", "pytest"],
                "pytest entry point": [str(Path(sys.executable).parent / "pytest")]}


def _child(tmp_path: Path, source: str, command: list[str], *extra: str) -> tuple[str, str, int]:
    test = tmp_path / "test_child.py"
    test.write_text(source)
    token = secrets.token_hex(20)
    env = {NAME: token, "PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": str(tmp_path),
           "PYTHONDONTWRITEBYTECODE": "1"}
    result = subprocess.run([*command, "-c", str(ROOT / "pytest.ini"), "--rootdir", str(tmp_path),
                             "-p", "no:cacheprovider", str(test), *extra],
                            cwd=tmp_path, env=env, capture_output=True, text=True)
    return result.stdout + result.stderr, token, result.returncode


def test_the_plugin_is_loaded_in_this_session(request):
    assert request.config.pluginmanager.has_plugin("environ_redact")


@pytest.mark.parametrize("entry", ENTRY_POINTS)
def test_a_bare_read_of_a_missing_variable_does_not_print_the_environment(tmp_path, entry):
    output, token, code = _child(tmp_path, FAILING_TESTS, ENTRY_POINTS[entry])
    assert code == 1 and "2 failed" in output and "KeyError" in output
    assert "environ(<redacted>)" in output
    assert token not in output and NAME not in output


@pytest.mark.parametrize("entry", ENTRY_POINTS)
def test_negative_control_without_the_plugin_the_environment_is_printed(tmp_path, entry):
    output, token, code = _child(tmp_path, FAILING_TESTS, ENTRY_POINTS[entry], "-p", "no:environ_redact")
    assert code == 1 and "2 failed" in output
    assert token in output and "environ(<redacted>)" not in output


def test_a_collection_error_is_redacted_and_its_negative_control_leaks(tmp_path):
    command = ENTRY_POINTS["python -m pytest"]
    output, token, code = _child(tmp_path, COLLECTION_ERROR, command, "--tb=long")
    assert code == 2 and "KeyError" in output and token not in output and "environ(<redacted>)" in output
    output, token, code = _child(tmp_path, COLLECTION_ERROR, command, "--tb=long", "-p", "no:environ_redact")
    assert code == 2 and token in output


def test_the_redaction_touches_only_the_environment_repr():
    import environ_redact

    text = ("self = " + "environ" + "({'A': 'secret', 'B': 'x'})\nkey = 'CP18A_FAKE_MISSING'\n"
            "E   KeyError: 'CP18A_FAKE_MISSING'\n")
    assert environ_redact.redact_text(text) == ("self = environ(<redacted>)\nkey = 'CP18A_FAKE_MISSING'\n"
                                                "E   KeyError: 'CP18A_FAKE_MISSING'\n")
    assert environ_redact.redact_text("os.environ.get('X') is None\n") == "os.environ.get('X') is None\n"
