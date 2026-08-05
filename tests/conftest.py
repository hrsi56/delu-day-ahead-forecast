"""Shared fixtures. Adds ``src/`` to ``sys.path`` for direct pytest runs."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture
def ledger_paths(tmp_path: Path) -> tuple[Path, Path]:
    """(ledger.jsonl, raw/) under an isolated tmp dir."""
    return tmp_path / "ledger.jsonl", tmp_path / "raw"
