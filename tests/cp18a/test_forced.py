"""One forced cause of each kind of day not issued, through the real pipeline (`cp18.forced`): the real checkout and
hooks, claim, store, H2 checks with the canary, the live-input builder and `cp17.daily`; no issuance fit runs. Marked
`stress` (local, about three minutes) and skipped where the local runtime is absent."""
from __future__ import annotations

import os
from pathlib import Path

import pytest

from cp17 import runtime
from cp18 import causes, forced

ROOT = Path(__file__).resolve().parents[2]
PROJECT = Path(os.environ.get('CP17_PROJECT_ROOT') or runtime.project_root())
LOCAL = (PROJECT / runtime.NODE_RELATIVE, PROJECT / runtime.PYODIDE_DIR / 'pyodide.asm.wasm',
         PROJECT / '.local/artifacts/cp-17c/bundle/src.zip', PROJECT / runtime.K13, PROJECT / runtime.CANARY_DIR)

pytestmark = [pytest.mark.stress,
              pytest.mark.skipif(not all(p.exists() for p in LOCAL), reason='the local runtime or states are absent')]


def test_each_cause_is_forced_and_recorded(tmp_path, monkeypatch):
    monkeypatch.setenv('CP17_PROJECT_ROOT', str(PROJECT))
    for name in ('OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS'):
        monkeypatch.setenv(name, '1')
    record = forced.run(ROOT, PROJECT, tmp_path)
    assert record['found'] == forced.EXPECTED and record['every_cause_forced']
    assert sorted(set(record['found'].values())) == sorted(causes.ORDER)
    assert record['gate_a'] == {'failed': 'machine', 'not_run': ['canary']}
    assert record['gate_b']['passed'] and record['issued'] == []
    assert record['inputs_2026_09_03']['shown'] is False
