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


def test_files_that_never_change_are_unchanged():
    assert _sha(ROOT / 'tests/cp23/torch-reference/uv.lock') == 'b3164a375e871396e685d0e887972b092fcd0c24a7fe0047167e8fc41c25dfed'
    lineage = json.loads((ROOT / 'reports/cp15/protocol.json').read_text())['input_sha256']
    cp15 = json.loads((ROOT / 'reports/cp15/artifact-manifest.json').read_text())['artifact_sha256']
    assert _sha(ROOT / 'uv.lock') == lineage['uv.lock'] and _sha(ROOT / 'pyproject.toml') == cp15['pyproject.toml']
    latest = {}   # a later checkpoint's manifest re-binds a path it legitimately extended (scripts/mlflow_export.py)
    for manifest in ('reports/block-challenger/artifact-manifest.json', 'reports/v4-revision/artifact-manifest.json',
                     'reports/distribution-challenger/artifact-manifest.json'):
        latest.update(json.loads((ROOT / manifest).read_text())['artifact_sha256'])
    assert 'scripts/mlflow_export.py' in latest
    for name, digest in latest.items():
        assert _sha(ROOT / name) == digest, name


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
