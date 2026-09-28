"""Publication Standard v1 §12 (brief W15): the runbook's touchpoints match the registry and the renderer.

Every `file::symbol` the runbook names must exist at module level in that file, and each list the
runbook marks (`<!-- runbook:name -->`) must equal the code's own: the registry's fields, kinds and
statuses, the chapter grammar's slots and detail menu, and the MLflow route patterns. Negative
controls show that a runbook which falls behind the code fails.
"""

from __future__ import annotations

import ast
import dataclasses
import re
import sys
from functools import lru_cache
from pathlib import Path

import pytest

from delu_forecast import registry as G
from delu_forecast.claims import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT / "scripts"))

import build_pages  # noqa: E402

RUNBOOK = REPO_ROOT / "docs" / "track-b" / "publication-runbook.md"
TOUCHPOINT = re.compile(r"`([\w./-]+\.py)::([A-Za-z_]\w*)`")


@lru_cache(maxsize=None)
def module_names(relative: str) -> frozenset[str]:
    """The names a file defines at module level: functions, classes and assignments."""
    tree = ast.parse((REPO_ROOT / relative).read_text())
    names = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            names.update(target.id for target in node.targets if isinstance(target, ast.Name))
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            names.add(node.target.id)
    return frozenset(names)


def marked(text: str, name: str) -> list[str]:
    """The backticked items between `<!-- runbook:name -->` and its closing marker, in order."""
    match = re.search(rf"<!-- runbook:{re.escape(name)} -->(.*?)<!-- /runbook:{re.escape(name)} -->", text, re.DOTALL)
    if match is None:
        return []
    body = match.group(1)
    if name == "statuses":  # the first cell of each table row
        return re.findall(r"^\| `([^`]+)` \|", body, re.MULTILINE)
    if name == "registry-fields":  # the fields listed after each group's colon
        return [item for line in body.splitlines() if ":" in line
                for item in re.findall(r"`(\w+)`", line.split(":", 1)[1].split("(")[0])]
    return re.findall(r"`([^`]+)`", body)


def route_pattern(route_id: str) -> str:
    kind, _, ident = route_id.partition(":")
    if not ident or ident == "overview":
        return route_id
    return f"{kind}:<{G.get(ident).kind} id>"


def runbook_problems(text: str) -> list[str]:
    problems = []
    touchpoints = TOUCHPOINT.findall(text)
    if len(touchpoints) < 30:
        problems.append(f"only {len(touchpoints)} touchpoints")
    for relative, symbol in touchpoints:
        if not (REPO_ROOT / relative).is_file():
            problems.append(f"{relative} does not exist")
        elif symbol not in module_names(relative):
            problems.append(f"{relative}::{symbol} is not defined there")
    expected = {
        "registry-fields": sorted(field.name for field in dataclasses.fields(G.Entry)),
        "kinds": list(G.KINDS),
        "statuses": list(G.STATUSES),
        "slots": [field.name for field in dataclasses.fields(build_pages.ChapterSlots) if field.name != "entry"],
        "details": list(build_pages.DETAIL_MENU),
        "routes": list(dict.fromkeys(route_pattern(route) for route in G.expected_routes())),
    }
    for name, wanted in expected.items():
        found = marked(text, name)
        if (sorted(found) if name == "registry-fields" else found) != wanted:
            problems.append(f"runbook:{name} lists {found}, the code has {wanted}")
    return problems


@pytest.fixture(scope="module")
def runbook() -> str:
    return RUNBOOK.read_text()


def test_the_runbook_matches_the_registry_and_the_renderer(runbook):
    assert runbook_problems(runbook) == []


def test_the_runbook_covers_every_scenario_the_standard_names(runbook):
    for heading in ("## 2. A new adopted generation", "## 3. A branch card", "## 4. A changed population",
                    "## 5. Status transitions"):
        assert heading in runbook


def test_negative_control_a_touchpoint_that_no_longer_exists(runbook):
    doctored = runbook.replace("`scripts/build_pages.py::chapter_sequence`", "`scripts/build_pages.py::chapter_list`", 1)
    assert "scripts/build_pages.py::chapter_list is not defined there" in runbook_problems(doctored)


def test_negative_control_a_registry_field_the_runbook_does_not_list(runbook):
    doctored = runbook.replace("`comparator`, `population`", "`comparator`", 1)
    assert any(problem.startswith("runbook:registry-fields") for problem in runbook_problems(doctored))


def test_negative_control_a_status_or_slot_out_of_step(runbook):
    doctored = runbook.replace("| `retired` |", "| `withdrawn` |", 1)
    assert any(problem.startswith("runbook:statuses") for problem in runbook_problems(doctored))
    doctored = runbook.replace("`reading`, `not_established`", "`not_established`, `reading`", 1)
    assert any(problem.startswith("runbook:slots") for problem in runbook_problems(doctored))


def test_negative_control_a_route_pattern_the_registry_does_not_derive(runbook):
    doctored = runbook.replace("`compare:<branch id>`", "`compare:<branch id>`, `run:<generation id>`", 1)
    assert any(problem.startswith("runbook:routes") for problem in runbook_problems(doctored))
