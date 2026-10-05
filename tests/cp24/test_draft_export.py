"""CP-24's draft MLflow export (§23.12) and the files that never change (§23.13 item 16, §23.14).

* `scripts/mlflow_export.py`, the root `pyproject.toml` and `uv.lock`, and CP-23's test-only lock are byte-identical
  to their committed identities; every file CP-21's to CP-23's artifact manifests bind is unchanged.
* The committed draft export (once it exists) equals a fresh build by `cp24.export`, which imports
  `scripts/mlflow_export.py`'s functions unchanged; a renamed run is caught.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DRAFT = ROOT / 'reports/ddnn2/mlflow-export-draft/cp24.json'


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_cp23s_test_only_reference_lock_is_unchanged():
    """The one lock CP-24 reuses (§23.7); every other unchanged file is tests/cp24/test_base_tree.py's."""
    assert _sha(ROOT / 'tests/cp23/torch-reference/uv.lock') == 'b3164a375e871396e685d0e887972b092fcd0c24a7fe0047167e8fc41c25dfed'


@pytest.mark.skipif(not DRAFT.exists(), reason='no CP-24 draft export (no scored attempt yet, or a stop)')
def test_the_committed_draft_equals_a_fresh_build_and_a_renamed_run_is_caught():
    from cp24 import export as X
    committed = json.loads(DRAFT.read_text())
    fresh = X.build(committed['scored_attempt'])
    assert json.loads(json.dumps(fresh, sort_keys=True, ensure_ascii=False)) == committed
    assert X.problems(fresh) == []
    renamed = copy.deepcopy(fresh)
    renamed['runs'][1]['run_name'] = 'something else'
    assert X.problems(renamed)
