"""CP-17-probe's committed records, recomputed: they run on CI from the committed files alone.

* the retrieval manifest: software only, every Pyodide wheel equal to its release lock, no data byte;
* the native reference: bitwise equal to CP-26's stored forecasts, its hashes recomputed from its values;
* the measurement table: every deviation recomputed from the committed native and browser quantiles
  (counts exactly, real values within 1e-12 absolute), every selection matched, no non-local request,
  and every WebAssembly host bitwise equal to every other;
* the bundle: the files the browsers executed are this checkout's files, byte for byte;
* the red line: no date in any record after 2026-09-06.
"""
from __future__ import annotations

from datetime import date
import hashlib
import json
from pathlib import Path
import re

import numpy as np
import pytest

from cp17probe import compare
from cp17probe.dailyfit import array_hash

ROOT = Path(__file__).resolve().parents[2]
RECORDS = ROOT / 'reports/cp17-probe'
STEMS = ('A1-2026-09-06', 'A1-2026-03-29', 'v2-2026-09-06')
BOUNDARY = date(2026, 9, 6)


def load(name):
    return json.loads((RECORDS / name).read_text())


def test_retrieval_was_software_only_and_matches_the_release_lock():
    m = load('retrieval-manifest.json')
    assert m['data_bytes_retrieved'] == 0 and m['pyodide']['version'] == '0.28.0'
    files = m['pyodide']['files']
    assert all(f['url'].startswith('https://cdn.jsdelivr.net/pyodide/v0.28.0/full/') for f in files)
    wheels = [f for f in files if f['url'].endswith(('.whl', 'openblas-0.3.26.zip'))]
    assert len(wheels) == 17 and all(f['lock_sha256_match'] is True for f in wheels)
    assert m['pyodide']['total_bytes'] == sum(f['bytes'] for f in files)
    c = m['chromium']
    assert c['url'] == 'https://cdn.playwright.dev/builds/cft/153.0.8010.12/mac-arm64/chrome-mac-arm64.zip'
    assert c['bytes'] == 190970181 and 'did not download' in c['ffmpeg']


def test_the_native_reference_is_bitwise_cp26_and_its_hashes_recompute():
    ref = load('native-reference.json')
    assert ref['status'] == 'PASS' and set(ref['results']) == set(STEMS)
    for stem in STEMS:
        result, check = ref['results'][stem], ref['checks'][stem]
        q = np.asarray(result['quantiles'], float)
        assert array_hash(q) == result['quantiles_sha256'] == check['actual_quantiles_sha256'] \
            == check['expected_quantiles_sha256']
        assert check['bitwise_equal'] and check['max_abs_difference'] == 0.0 and check['selections']['all_match']


def test_every_reported_deviation_recomputes_from_the_committed_quantiles():
    native = load('native-reference.json')['results']
    browser = load('browser-results.json')
    table = load('measurements.json')
    by = {(r['browser'], r['stem']): r for r in browser['runs']}
    assert len(table['runs']) == 6 and {(r['browser'], r['stem']) for r in table['runs']} == \
        {(b, s) for b in ('chromium', 'webkit') for s in STEMS}
    for row in table['runs']:
        run = by[(row['browser'], row['stem'])]
        assert not row['errors'] and row['payload_sha256_equal'] and row['source_identical_to_checkout']
        assert row['blocked_non_local_requests'] == [] and set(row['stubs_engaged']) <= {'holidays', 'resource'}
        again = compare.deviation(native[row['stem']]['quantiles'], run['python']['result']['quantiles'])
        assert again['bitwise_equal'] == row['deviation']['bitwise_equal']
        assert abs(again['max_abs_eur'] - row['deviation']['max_abs_eur']) <= 1e-12
        for level, value in again['max_abs_eur_by_level'].items():
            assert abs(value - row['deviation']['max_abs_eur_by_level'][level]) <= 1e-12
        sel = (compare.a1_selections if row['policy'] == 'A1' else compare.v2_selections)(
            native[row['stem']], run['python']['result'])
        assert sel['all_match'] and row['selections']['all_match']
        assert row['status'] == ('identical bit for bit' if again['bitwise_equal'] else 'different')


def test_every_webassembly_host_produced_the_same_bits():
    browser = load('browser-results.json')
    for stem in STEMS:
        hashes = {r['browser']: r['python']['result']['quantiles_sha256'] for r in browser['runs'] if r['stem'] == stem}
        node = load(f'node-{stem}.json')
        hashes['node'] = node['python']['result']['quantiles_sha256']
        assert len(hashes) == 3 and len(set(hashes.values())) == 1, (stem, hashes)
        assert array_hash(np.asarray(node['python']['result']['quantiles'], float)) == hashes['node']
    assert all(sorted(h['browsers_bitwise_equal_to_node']) == ['chromium', 'webkit']
               for h in load('measurements.json')['node_pyodide'].values())


def test_the_browsers_executed_this_checkouts_files():
    bundle = load('bundle-manifest.json')
    for name, digest in bundle['files_sha256'].items():
        assert hashlib.sha256((ROOT / 'src' / name).read_bytes()).hexdigest() == digest, name
    for run in load('browser-results.json')['runs']:
        assert all(bundle['files_sha256'][k] == v for k, v in run['python']['source_sha256'].items())


@pytest.mark.parametrize('name', ['native-reference.json', 'browser-results.json', 'measurements.json',
                                  *(f'node-{s}.json' for s in STEMS)])
def test_no_record_holds_a_day_after_the_boundary(name):
    text = (RECORDS / name).read_text()
    days = {date.fromisoformat(d) for d in re.findall(r'(20\d\d-\d\d-\d\d)', text)}
    assert days and max(days) <= BOUNDARY, sorted(d for d in days if d > BOUNDARY)[:5]
    instants = re.findall(r'20\d\d-\d\d-\d\dT\d\d:\d\d:\d\d\+00:00', text)
    assert all(t <= '2026-09-06T21:00:00+00:00' for t in instants)
