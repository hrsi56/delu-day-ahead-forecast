"""Pytest plugin: keep the process environment out of test and collection failure output (CP-18a item 7, P0-3).

A bare `os.environ[...]` read of a missing variable raises KeyError inside `os._Environ.__getitem__`. Pytest's
long traceback then prints that frame's arguments, and its `self` is the environment's repr, credentials
included. That is how the DagsHub token reached a public commit
(docs/track-b/credential-exposure-2026-09-24.md).

Registered with `-p environ_redact` in pytest.ini's addopts; pytest applies the ini's `pythonpath` (which holds
tests/) before it imports `-p` plugins, so the module is found under every entry point. Two hook wrappers rewrite
every report before anything prints or stores it: in the failure text and in the captured-output sections, each
environment repr, from its opening `environ(` and brace to the end of that line, becomes `environ(<redacted>)`.
Only that repr is touched; everything else in the report keeps its structure. If a repr object cannot be
rewritten in place, the report's text is replaced by its redacted rendering.

`tests/cp18a/test_environ_access.py` keeps new bare reads out of the code in the first place;
`tests/cp18a/test_environ_redact.py` proves the leak and this fix in a child pytest run.
"""
from __future__ import annotations

import dataclasses
import re

import pytest

ENVIRON = re.compile(r"(environb?)\(\{[^\n]*")


def redact_text(text: str) -> str:
    return ENVIRON.sub(lambda match: f"{match.group(1)}(<redacted>)", text)


def _redact(value, seen: set[int]):
    """Redact strings inside a pytest repr object tree in place; return the (possibly new) value."""
    if isinstance(value, str):
        return redact_text(value)
    if isinstance(value, tuple):
        return tuple(_redact(item, seen) for item in value)
    if isinstance(value, list):
        value[:] = [_redact(item, seen) for item in value]
        return value
    if dataclasses.is_dataclass(value) and not isinstance(value, type) and id(value) not in seen:
        seen.add(id(value))
        for field in dataclasses.fields(value):
            current = getattr(value, field.name, None)
            new = _redact(current, seen)
            if new is not current:
                try:
                    setattr(value, field.name, new)
                except (AttributeError, TypeError, dataclasses.FrozenInstanceError):
                    pass
    return value


def _text(longrepr) -> str:
    try:
        return str(longrepr)
    except Exception:  # an unprintable repr prints nothing, so there is nothing to redact
        return ""


def redact_report(report) -> None:
    longrepr = report.longrepr
    if isinstance(longrepr, (str, tuple)):
        report.longrepr = _redact(longrepr, set())
    elif longrepr is not None:
        rendered = _text(longrepr)
        if ENVIRON.search(rendered):
            _redact(longrepr, set())
            if ENVIRON.search(_text(longrepr)):
                report.longrepr = redact_text(rendered)
    if report.sections:
        report.sections = [(title, redact_text(content)) for title, content in report.sections]


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    report = yield
    redact_report(report)
    return report


@pytest.hookimpl(wrapper=True)
def pytest_collectreport(report):
    redact_report(report)
    return (yield)
