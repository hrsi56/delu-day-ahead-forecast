"""The issuing host and the browser, rerun from this checkout (timing-sensitive, `stress`).

It rebuilds the frozen package from the checkout's `src/`, then retrains A1 for 2026-09-06 under Pyodide in
Node.js and in Chromium, and requires:
- both bit-identical to the committed issuing-host record;
- the checkout's own files executed;
- no non-local request.

It needs the pinned runtimes (`.local/tools/`) and the reproduction's payloads (`.local/artifacts/cp-17/final/`),
so it skips with that reason where they are absent, as on CI. `CP17_PROJECT_ROOT` names the checkout holding
`.local/`; `CP17_BROWSERS` (default `chromium`) chooses the browsers.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess

import pytest

from cp17.tools import bundle, hosts, ledger

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ledger.project_root(ROOT)
PYODIDE = PROJECT / '.local/tools/pyodide-0.28.0'
PAYLOADS = PROJECT / '.local/artifacts/cp-17/final/native/payloads'
PLAYWRIGHT = PROJECT / '.local/tools/playwright/bin/python'
STEM = 'A1-2026-09-06'

pytestmark = [pytest.mark.stress,
              pytest.mark.skipif(not (PYODIDE.exists() and Path(hosts.NODE).exists() and (PAYLOADS / f'{STEM}.npz').exists()),
                                 reason='the pinned Pyodide, Node.js and the reproduction payloads are absent')]


@pytest.fixture(scope='module')
def package(tmp_path_factory):
    out = tmp_path_factory.mktemp('package') / 'src.zip'
    manifest = bundle.build(ROOT / 'src', out)
    # Superseded at CP-17b, and again at CP-17c: the frozen package is CP-17c's re-frozen one (its freeze manifest).
    # The fit it runs is unchanged, so the issued quantiles below must still be CP-17's committed issuing-host
    # record, bit for bit.
    committed = json.loads((ROOT / 'docs/track-b/evidence/cp-17c/freeze-manifest.json').read_text())['policy_identity']['code']
    assert manifest['files_sha256'] == committed['files_sha256'], 'the checkout differs from the frozen package'
    return out, manifest


def committed_host():
    rows = json.loads((ROOT / 'reports/cp17/host-parity.json').read_text())['issuing_host_parity']
    return next(r for r in rows if r['stem'] == STEM)


def test_issuing_host_reproduces_its_record(package, tmp_path):
    zip_path, manifest = package
    hosts.run_node(PYODIDE, zip_path, PAYLOADS, STEM, tmp_path, True)
    run = json.loads((tmp_path / f'node-{STEM}.json').read_text())
    assert not run['errors'], run['errors']
    assert run['python']['result']['quantiles_sha256'] == committed_host()['issued_quantiles_sha256']
    assert run['blocked_non_local_requests'] == []
    assert all(manifest['files_sha256'][k] == v for k, v in run['python']['source_sha256'].items())


@pytest.mark.skipif(not PLAYWRIGHT.exists(), reason='the pinned Playwright browsers are absent')
def test_browser_reproduces_the_issuing_host(package, tmp_path):
    zip_path, manifest = package
    out = tmp_path / 'browser.json'
    env = {**os.environ, 'PLAYWRIGHT_BROWSERS_PATH': str(PROJECT / '.local/tools/ms-playwright')}
    subprocess.run([str(PLAYWRIGHT), str(ROOT / 'src/cp17/tools/measure.py'), '--pyodide', str(PYODIDE), '--bundle',
                    str(zip_path.parent), '--payloads', str(PAYLOADS), '--out', str(out), '--runs', STEM,
                    '--browsers', os.environ.get('CP17_BROWSERS', 'chromium'), '--attribution', '1'], check=True, env=env)
    for run in json.loads(out.read_text())['runs']:
        assert not run.get('errors'), run.get('errors')
        assert run['python']['result']['quantiles_sha256'] == committed_host()['issued_quantiles_sha256'], run['browser']
        assert run['blocked_non_local_requests'] == []
        assert all(manifest['files_sha256'][k] == v for k, v in run['python']['source_sha256'].items())
