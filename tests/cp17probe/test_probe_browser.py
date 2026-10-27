"""CP-17-probe: one browser measurement, rerun, against the committed records (stress; local runtimes only).

It serves the pinned Pyodide release and a freshly built bundle of this checkout, runs A1's daily fit for
delivery 2026-09-06 in each browser named by `CP17_PROBE_BROWSERS` (default Chromium), and requires
that the rerun matches the committed browser record bit for bit, that every selection matches the
native fit, and that the browser executed this checkout's files and nothing from the network. It skips
where the runtimes or the payloads are absent, as on CI: they live under `.local/` and are never
committed. `CP17_PROBE_PROJECT_ROOT` names the checkout holding `.local/`.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess

import pytest

from cp17probe import compare
from cp17probe.bundle import build

ROOT = Path(__file__).resolve().parents[2]
PROJECT = Path(os.environ.get('CP17_PROBE_PROJECT_ROOT', '/Users/djourno/Downloads/PJM'))
TOOLS = PROJECT / '.local/tools'
PYODIDE = TOOLS / 'pyodide-0.28.0'
PLAYWRIGHT = TOOLS / 'playwright/bin/python'
BROWSERS = TOOLS / 'ms-playwright'
PAYLOADS = PROJECT / '.local/artifacts/cp-17-probe/final/payloads'
RECORDS = ROOT / 'reports/cp17-probe'
STEM = 'A1-2026-09-06'
NEEDED = (PYODIDE / 'pyodide.asm.wasm', PLAYWRIGHT, BROWSERS / 'chromium-1243', BROWSERS / 'webkit-2359',
          PAYLOADS / f'{STEM}.npz')

pytestmark = [pytest.mark.stress,
              pytest.mark.skipif(not all(p.exists() for p in NEEDED),
                                 reason='the pinned Pyodide 0.28.0, Playwright 1.63.0 browsers and probe payloads '
                                        '(.local/, never committed) are absent')]


def test_one_browser_measurement_reproduces_the_committed_record(tmp_path):
    bundle = build(ROOT / 'src', tmp_path / 'bundle' / 'src.zip')
    out = tmp_path / 'browser-results.json'
    browsers = os.environ.get('CP17_PROBE_BROWSERS', 'chromium')
    env = dict(os.environ, PLAYWRIGHT_BROWSERS_PATH=str(BROWSERS))
    done = subprocess.run([str(PLAYWRIGHT), str(ROOT / 'src/cp17probe/measure.py'), '--pyodide', str(PYODIDE),
                           '--bundle', str(tmp_path / 'bundle'), '--payloads', str(PAYLOADS), '--out', str(out),
                           '--browsers', browsers, '--runs', STEM, '--timeout', '900'],
                          env=env, capture_output=True, text=True, timeout=1800)
    assert done.returncode == 0, done.stdout + done.stderr
    roots = {'/app/': ROOT / 'src/cp17probe/browser', '/pyodide/': PYODIDE, '/bundle/': tmp_path / 'bundle',
             '/payloads/': PAYLOADS}
    table = compare.build(RECORDS / 'native-reference.json', out, roots, tmp_path / 'bundle' / 'src.json')
    committed = json.loads((RECORDS / 'browser-results.json').read_text())
    for row, run in zip(table['runs'], json.loads(out.read_text())['runs']):
        assert row['payload_sha256_equal'] and row['source_identical_to_checkout'], row
        assert row['selections']['all_match'], row['selections']
        assert row['blocked_non_local_requests'] == [] and set(row['stubs_engaged']) <= {'holidays', 'resource'}
        assert run['python']['source_sha256'] == {k: v for k, v in bundle['files_sha256'].items()
                                                  if k in run['python']['source_sha256']}
        before = [r for r in committed['runs'] if r['browser'] == row['browser'] and r['stem'] == STEM][0]
        assert run['python']['result']['quantiles_sha256'] == before['python']['result']['quantiles_sha256']
        assert run['python']['result']['attribution']['phi_eur'] == before['python']['result']['attribution']['phi_eur']
