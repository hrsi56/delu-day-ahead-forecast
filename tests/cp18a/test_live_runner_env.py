"""The live-input builder as a GitHub runner runs it: committed files only, and no native LightGBM.

A `macos-26` runner has no libomp, so the native LightGBM cannot load there (CP-17c's run 1; this round's runner run
5). The builder fits nothing, so it must never import it. In a child process whose import system refuses `lightgbm`,
this builds 2026-09-06 (a parity origin and the last shadow day) from the committed dry-run material only:
- the recorded responses `reports/cp18a/dryrun/recorded/` (rendered market responses and recorded GFS runs), archived
  through the retrieval clients;
- A1's `k13.json` and the freeze-origin state at `reports/cp18a/dryrun/pinned/`, whose buffers (CP-26's, after
  2026-09-06's release) are the ones the development builder's 2026-09-06 parity payloads carry;

and requires the four payloads' SHA-256s to equal the development builder's, as `reports/cp18a/live-equality.json`
records them. It needs no `.local/` and runs in CI.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import platform
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
CHILD = r'''
import json, sys
from datetime import date
from pathlib import Path

class RefuseLightGBM:
    def find_spec(self, name, path=None, target=None):
        if name == 'lightgbm' or name.startswith('lightgbm.'):
            raise ImportError('lightgbm refused: a runner cannot load it (no libomp)')
        return None
sys.meta_path.insert(0, RefuseLightGBM())

root, work = Path(sys.argv[1]), Path(sys.argv[2])
from cp17.shadow import ShadowStates
from cp18.live import archive as AR, recorded as R
from cp18.live.build import build_day
recorded = root / 'reports/cp18a/dryrun/recorded'
pinned = root / 'reports/cp18a/dryrun/pinned/local/artifacts'
day, base_end = date(2026, 9, 6), date(2026, 8, 27)
archive = AR.Archive(work / 'archive')
for d in [date(2026, 8, 28 + i) for i in range(4)] + [date(2026, 9, i) for i in range(1, 7)]:
    item = R.archive_day(archive, recorded / 'replay', d, root, 'smard', [recorded / 'gfs'])
    assert not item['verify'], item
state = ShadowStates.from_dict(json.loads((pinned / 'cp-17c/state/freeze-origin-state.json').read_text()))
result = build_day(day, archive=archive, base_end=base_end, buffers={p: state.buffer(p) for p in ('v4', 'v2', 'B0')},
                   search_dir=pinned / 'cp-17/inputs/reports/rebaseline/cold-rerun-2026-10-15/search-results/nominal',
                   out=work / 'payloads', root=root)
print(json.dumps({'status': result['status'], 'cause': result['cause'],
                  'payload_sha256': {p: v['payload_sha256'] for p, v in result['payloads'].items()},
                  'lightgbm_loaded': 'lightgbm' in sys.modules}))
'''


@pytest.mark.skipif((platform.system(), platform.machine()) != ('Darwin', 'arm64'),
                    reason='the payload bytes are pinned on the issuing host platform, darwin-arm64 (the macos-26 runner '
                           'and the M3); on GitHub CI\'s Linux x86_64, A1\'s and v4\'s payload bytes differ (found at CP-18a\'s landing)')
def test_the_live_builder_needs_no_lightgbm_and_no_local_files(tmp_path):
    reference = {}
    for row in json.loads((ROOT / 'reports/cp18a/live-equality.json').read_text())['days']:
        if row['day'] == '2026-09-06' and row['set'] == 'parity':      # the native-parity payloads: CP-26's buffers
            reference = {s['policy']: s['payload_sha256']['reference'] for s in row['stems']}
    assert set(reference) == {'A1', 'v4', 'v2', 'B0'}
    env = {**{k: v for k, v in os.environ.items() if k in ('PATH', 'HOME', 'TMPDIR')},
           'PYTHONPATH': str(ROOT / 'src'), 'CP17_PROJECT_ROOT': str(tmp_path / 'no-project-root'),
           'CP26_PROJECT_ROOT': str(tmp_path / 'no-project-root'),
           **{n: '1' for n in ('OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
                               'NUMEXPR_NUM_THREADS')}, 'MLFLOW_DISABLE_TELEMETRY': 'true', 'DO_NOT_TRACK': '1'}
    done = subprocess.run([sys.executable, '-c', CHILD, str(ROOT), str(tmp_path)], capture_output=True, text=True,
                          env=env, cwd=tmp_path, timeout=900)
    assert done.returncode == 0, done.stderr[-3000:]
    result = json.loads(done.stdout.strip().splitlines()[-1])
    assert result['status'] == 'built', result['cause']
    assert result['lightgbm_loaded'] is False
    assert result['payload_sha256'] == reference
