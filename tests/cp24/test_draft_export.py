"""CP-24's draft MLflow export (§23.12).

* The committed draft export (once it exists) equals a fresh build by `cp24.export`, which imports
  `scripts/mlflow_export.py`'s functions unchanged; a renamed run is caught. The comparison is meaningful while
  `scripts/mlflow_export.py` holds the bytes CP-24 started from (its SHA-256 in `reports/ddnn2/base-tree.json`).
  A later authorized change to that script skips it with the reason; the draft itself stays bound byte for byte
  by CP-24's artifact manifest (`tests/cp24/test_saved_evidence.py`).
* The files that never change (§23.13 item 16, §23.14) -- `scripts/mlflow_export.py`, the root `pyproject.toml`
  and `uv.lock`, CP-23's test-only lock and every file CP-21's to CP-23's manifests bind -- are proved unchanged
  in the candidate by `python -m cp24.basetree --check-rev <candidate>`, not by hashing them in this suite, which
  keeps running on `main` after authorized work changes them (`tests/cp24/test_base_tree.py`).
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


def _export_script_as_at_base() -> bool:
    record = json.loads((ROOT / 'reports/ddnn2/base-tree.json').read_text())
    return _sha(ROOT / 'scripts/mlflow_export.py') == record['sha256']['scripts/mlflow_export.py']


@pytest.mark.skipif(not DRAFT.exists(), reason='no CP-24 draft export (no scored attempt yet, or a stop)')
def test_the_committed_draft_equals_a_fresh_build_and_a_renamed_run_is_caught():
    if not _export_script_as_at_base():
        pytest.skip('scripts/mlflow_export.py changed after CP-24; the draft stays bound by its artifact manifest')
    from cp24 import export as X
    committed = json.loads(DRAFT.read_text())
    fresh = X.build(committed['scored_attempt'])
    assert json.loads(json.dumps(fresh, sort_keys=True, ensure_ascii=False)) == committed
    assert X.problems(fresh) == []
    renamed = copy.deepcopy(fresh)
    renamed['runs'][1]['run_name'] = 'something else'
    assert X.problems(renamed)
