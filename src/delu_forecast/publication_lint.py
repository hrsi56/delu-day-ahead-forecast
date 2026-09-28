"""Publication checks over the rendered surfaces (Publication Standard v1 §4, §5, §8, §11).

This module holds the checks that read what a reader receives -- the built page, the README, the
Space cards and the MLflow export -- and compare it with the registry and the claim layer:

* **Registry consistency (§5).** Every registered generation and branch has each surface that
  derives from it, and no surface names an identity the registry does not hold.

Each check returns a list of problems, one line each; an empty list means it holds. The tests
(`tests/test_35_registry.py` and its companions) run every check on the committed surfaces and on
a deliberately broken copy, so a check that cannot fail is caught.
"""

from __future__ import annotations

import re

from . import registry as G

_VERSION_HREF = re.compile(r'href="#(v\d+)"')


def _section(document: str, opening: str, closing: str) -> str | None:
    start = document.find(opening)
    if start < 0:
        return None
    end = document.find(closing, start)
    return document[start:end if end >= 0 else len(document)]


# --------------------------------------------------------------------------- registry consistency (§5)


def page_consistency_problems(page: str) -> list[str]:
    """The page against the registry: chapters, rail, jump row, lineage and comparison rows."""
    problems: list[str] = []
    versions = [entry.version for entry in G.generations()]
    chapters = re.findall(r'<article class="chapter[^"]*" id="(v\d+)"', page)
    for version in versions:
        if version not in chapters:
            problems.append(f"page: registered generation {version} has no chapter")
    for version in chapters:
        if version not in versions:
            problems.append(f"page: chapter {version} is not a registered generation")
    newest_first = [entry.version for entry in G.generations(newest_first=True)]
    if [version for version in chapters if version in versions] != newest_first:
        problems.append(f"page: chapters are not in the registry's order {newest_first}")
    for name, opening, closing in (("rail", '<nav class="rail"', "</nav>"), ("jump row", '<nav class="jump"', "</nav>"),
                                   ("lineage", '<ol class="mainline"', "</ol>")):
        block = _section(page, opening, closing)
        if block is None:
            problems.append(f"page: no {name}")
            continue
        linked = _VERSION_HREF.findall(block)
        for version in versions:
            if version not in linked:
                problems.append(f"page: registered generation {version} is missing from the {name}")
        for version in linked:
            if version not in versions:
                problems.append(f"page: the {name} names {version}, which is not registered")
    branches = _section(page, '<ul class="branches"', "</ul>") or ""
    for entry in G.branches():
        if entry.name not in branches:
            problems.append(f"page: registered branch {entry.name!r} is missing from the lineage")
    overview = _section(page, 'data-chart-id="overview"', "</div>") or ""
    for entry in G.comparison_rows():
        code = entry.code_in(G.COMPARISON_EXPERIMENT)
        if f'data-record="cp20.metrics.{code}.equal_fold.S_MAE"' not in overview:
            problems.append(f"page: comparison row {entry.id} ({code}) is missing")
    return problems


def readme_consistency_problems(readme: str) -> list[str]:
    """The README against the registry: one heading per registered generation, none for another."""
    problems: list[str] = []
    headings = re.findall(r"^#{2,4} (.+)$", readme, re.MULTILINE)
    for entry in G.generations():
        if not any(heading.startswith(entry.name) or heading == G.label(entry, "readme") for heading in headings):
            problems.append(f"README: registered generation {entry.version} has no heading")
    registered = {entry.version for entry in G.generations()}
    for heading in headings:
        match = re.match(r"^(v\d+) · ", heading)
        if match and match.group(1) not in registered:
            problems.append(f"README: heading {heading!r} names an unregistered generation")
    return problems


def export_consistency_problems(files: dict[str, dict]) -> list[str]:
    """The MLflow export against the registry: the contract of `scripts/mlflow_export.py`."""
    problems = []
    runs = [run for name, content in files.items() if name != "manifest" for run in content["runs"]]
    keys = {run["run_key"] for run in runs}
    for key in G.expected_run_keys():
        if key not in keys:
            problems.append(f"export: registered run {key} is missing")
    for run in runs:
        key = run["run_key"]
        if key not in G.expected_run_keys():
            problems.append(f"export: run {key} is not registered")
        elif run["run_name"] != G.mlflow_run_name(key):
            problems.append(f"export: {key} is not named from the registry")
    return problems


__all__ = [
    "export_consistency_problems",
    "page_consistency_problems",
    "readme_consistency_problems",
]
