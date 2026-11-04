"""CP-18a item 7, P0-3 (a): no new bare `os.environ[...]` read.

A missing variable read with a bare subscript raises KeyError inside `os._Environ.__getitem__`, and pytest's long
traceback prints that frame's `self`: the whole environment, credentials included (AGENTS.md § Credentials; the
DagsHub token reached a public commit that way). Read with `os.environ.get(...)` or `os.getenv(...)`
and fail with a message that names the variable.

The lint walks the AST of every `.py` file under src/, scripts/, app/, space*/ and tests/ and flags each
subscript in load context of `os.environ` (or `os.environb`, under any alias of `os`) or of `environ` imported
from `os`. Assignments, `del` and `.get` are fine. The frozen copies under models/champion/code/ and
docs/track-b/evidence/ are not scanned. Existing sites are listed in ALLOWLIST by (path, expression), each with
its reason, and the count is printed; new CP-18a code (src/cp18/) has no entry, so any bare read there fails.
"""
from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCANNED = ("src", "scripts", "app", "tests")  # plus every space*/ directory at the root
EXCLUDED = ("models/champion/code/", "docs/track-b/evidence/")
SKIPPED_PARTS = {"__pycache__", "node_modules"}

FROZEN = "frozen package (§16.2): a change is a re-freeze"
FIX_PENDING = "fix pending: landed checkpoint code changes only through a checkpoint"
CP16_FROZEN = (FIX_PENDING + "; the CP-16 test files are also hash-bound by reports/v2-causal/artifact-manifest.json "
               "(tests/cp16/conftest.py)")

#: (path, the read as `ast.unparse` prints it) -> reason. Every occurrence of that read in that file is covered.
ALLOWLIST: dict[tuple[str, str], str] = {
    ("src/cp17/runtime.py", "os.environ['CP17_PROJECT_ROOT']"): FROZEN,
    ("src/cp17/tools/ledger.py", "os.environ['CP17_PROJECT_ROOT']"): FROZEN,
    ("src/cp20/execution.py", "os.environ['CP20_LEDGER']"): FIX_PENDING,
    ("src/cp20/extract.py", "os.environ['CP20_LEDGER']"): FIX_PENDING,
    ("src/cp20/probe.py", "os.environ['CP20_LEDGER']"): FIX_PENDING,
    ("src/cp21/daily.py", "os.environ['CP21_LEDGER']"): FIX_PENDING,
    ("src/cp21/execution.py", "os.environ['CP21_LEDGER']"): FIX_PENDING,
    ("src/cp22/daily.py", "os.environ['CP22_LEDGER']"): FIX_PENDING,
    ("src/cp22/execution.py", "os.environ['CP22_LEDGER']"): FIX_PENDING,
    ("src/cp23/daily.py", "os.environ['CP23_LEDGER']"): FIX_PENDING,
    ("src/cp23/execution.py", "os.environ['CP23_LEDGER']"): FIX_PENDING,
    ("src/cp24/admission.py", "os.environ['CP24_LEDGER']"): FIX_PENDING,
    ("src/cp24/daily.py", "os.environ['CP24_LEDGER']"): FIX_PENDING,
    ("src/cp24/execution.py", "os.environ['CP24_LEDGER']"): FIX_PENDING,
    ("src/cp24/gate.py", "os.environ['CP24_LEDGER']"): FIX_PENDING,
    ("src/cp24/leakage.py", "os.environ['CP24_LEDGER']"): FIX_PENDING,
    ("src/cp24/search.py", "os.environ['CP24_LEDGER']"): FIX_PENDING,
    ("src/cp28/reader.py", "os.environ['CP28_LOCAL_ROOT']"): FIX_PENDING,
    ("src/delu_forecast/tracking.py", "os.environ[TRACKING_URI_VAR]"): FIX_PENDING,
    ("scripts/cp16_v2.py", "os.environ[k]"): FIX_PENDING,
    ("scripts/cp20_weather.py", "os.environ[k]"): FIX_PENDING,
    ("scripts/cp21_blocks.py", "os.environ[k]"): FIX_PENDING,
    ("scripts/cp22_revision.py", "os.environ[k]"): FIX_PENDING,
    ("scripts/cp23_ddnn.py", "os.environ[k]"): FIX_PENDING,
    ("scripts/cp24_ddnn2.py", "os.environ[k]"): FIX_PENDING,
    ("scripts/cp26_calibrate.py", "os.environ['CP26_JOB_ID']"): FIX_PENDING,
    ("scripts/cp26_calibrate.py", "os.environ['CP26_JOB_INDEX']"): FIX_PENDING,
    ("scripts/cp26_cold_run.py", "os.environ['CP26_JOB_ID']"): FIX_PENDING,
    ("scripts/cp26_cold_run.py", "os.environ['CP26_JOB_INDEX']"): FIX_PENDING,
    ("tests/cp16/reproduce_components.py", "os.environ['CP16_LEDGER']"): CP16_FROZEN,
    ("tests/cp16/test_state_results.py", "os.environ['CP16_LEDGER']"): CP16_FROZEN,
    ("tests/cp17cprobe/fake_node.py", "os.environ['CP17C_FAKE_RECORDS']"): FIX_PENDING,
}


def bare_reads(source: str, filename: str = "<fixture>") -> list[tuple[int, str]]:
    """(line, expression) for every bare environment subscript read in the source."""
    tree = ast.parse(source, filename)
    os_names, environ_names = {"os"}, set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "os" or alias.name.startswith("os."):
                    os_names.add(alias.asname or "os")
        elif isinstance(node, ast.ImportFrom) and node.module == "os":
            environ_names |= {alias.asname or alias.name for alias in node.names
                              if alias.name in ("environ", "environb")}
    found = []
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Subscript) and isinstance(node.ctx, ast.Load)):
            continue
        target = node.value
        if ((isinstance(target, ast.Attribute) and target.attr in ("environ", "environb")
             and isinstance(target.value, ast.Name) and target.value.id in os_names)
                or (isinstance(target, ast.Name) and target.id in environ_names)):
            found.append((node.lineno, ast.unparse(node)))
    return sorted(found)


def scan(root: Path) -> list[tuple[str, int, str]]:
    folders = [root / name for name in SCANNED] + sorted(p for p in root.glob("space*") if p.is_dir())
    found = []
    for folder in folders:
        for file in sorted(folder.rglob("*.py")):
            relative = file.relative_to(root).as_posix()
            if relative.startswith(EXCLUDED) or SKIPPED_PARTS & set(file.parts) or not file.is_file():
                continue
            found += [(relative, line, expr) for line, expr in bare_reads(file.read_text(encoding="utf-8"),
                                                                          relative)]
    return found


def violations(found, allowlist=ALLOWLIST) -> list[str]:
    return [f"{path}:{line}: {expr}" for path, line, expr in found if (path, expr) not in allowlist]


def test_no_bare_environ_read_outside_the_allowlist(capsys):
    found = scan(ROOT)
    covered = sum(1 for path, _, expr in found if (path, expr) in ALLOWLIST)
    with capsys.disabled():
        print(f"\nenviron-access lint: {len(ALLOWLIST)} allowlist entries covering {covered} bare reads, "
              "each with its reason")
    problems = violations(found)
    assert not problems, ("bare os.environ[...] reads print the whole environment when the variable is missing; "
                          "use os.environ.get(...) and fail naming the variable:\n" + "\n".join(problems))
    stale = sorted(set(ALLOWLIST) - {(path, expr) for path, _, expr in found})
    assert not stale, f"allowlist entries that no longer match a read; remove them: {stale}"


def test_every_allowlist_entry_has_a_reason_and_new_cp18_code_has_none():
    assert not [path for path, _ in ALLOWLIST if path.startswith("src/cp18/")]
    for (path, _), reason in ALLOWLIST.items():
        if path.startswith(("src/cp17/", "src/cp17c/")):
            assert reason == FROZEN, path
        else:
            assert reason.startswith(FIX_PENDING), path


FIXTURE = '''\
import os
import os as system
from os import environ, environ as env, getenv

a = os.environ.get("FAKE_MISSING")
b = getenv("FAKE_MISSING")
os.environ["FAKE_SET"] = "1"
del os.environ["FAKE_SET"]
c = "FAKE_MISSING" in os.environ
d = os.environ['FAKE_MISSING']
e = environ["FAKE_MISSING"]
f = env["FAKE_MISSING"]
g = system.environ["FAKE_MISSING"]
h = os.environb[b"FAKE_MISSING"]
'''


def test_the_lint_flags_each_bare_read_with_its_line_and_passes_the_safe_forms():
    assert bare_reads(FIXTURE) == [(10, "os.environ['FAKE_MISSING']"), (11, "environ['FAKE_MISSING']"),
                                   (12, "env['FAKE_MISSING']"), (13, "system.environ['FAKE_MISSING']"),
                                   (14, "os.environb[b'FAKE_MISSING']")]
    assert bare_reads("import os\nx = os.environ.get('FAKE_MISSING')\n") == []


def test_a_new_bare_read_under_src_cp18_fails_even_for_an_allowlisted_expression(tmp_path):
    (tmp_path / "src" / "cp18").mkdir(parents=True)
    (tmp_path / "src" / "cp18" / "daily.py").write_text("import os\nROOT = os.environ['CP28_LOCAL_ROOT']\n")
    (tmp_path / "src" / "cp28").mkdir()
    (tmp_path / "src" / "cp28" / "reader.py").write_text("import os\nROOT = os.environ['CP28_LOCAL_ROOT']\n")
    assert violations(scan(tmp_path)) == ["src/cp18/daily.py:2: os.environ['CP28_LOCAL_ROOT']"]


def test_every_scanned_root_is_covered_and_the_frozen_copies_are_not(tmp_path):
    bare = "import os\nx = os.environ['FAKE_MISSING']\n"
    for relative in ("src/a.py", "scripts/b.py", "app/c.py", "space/d.py", "space-wasm/e.py", "tests/f.py",
                     "models/champion/code/g.py", "docs/track-b/evidence/cp-1/h.py", "other/i.py",
                     "tests/__pycache__/j.py"):
        (tmp_path / relative).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / relative).write_text(bare)
    assert sorted(path for path, _, _ in scan(tmp_path)) == ["app/c.py", "scripts/b.py", "space-wasm/e.py",
                                                             "space/d.py", "src/a.py", "tests/f.py"]
