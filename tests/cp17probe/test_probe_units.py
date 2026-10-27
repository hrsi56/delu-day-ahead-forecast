"""CP-17-probe units: payload identity, the comparison rules, the stubs, the server and the bundle (synthetic)."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import threading
import urllib.error
import urllib.request

import numpy as np
import pytest

from cp17probe import compare, dailyfit
from cp17probe.attribution import column_group
from cp17probe.measure import Server, category

SRC = Path(__file__).resolve().parents[2] / 'src'


def _module(path: Path):
    spec = importlib.util.spec_from_file_location(f'probe_stub_{path.stem}', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_index_hash_is_independent_of_the_runtime_integer_width():
    values = [3, 5, 700]
    narrow, wide = np.array(values, dtype=np.int32), np.array(values, dtype=np.int64)
    assert dailyfit.index_hash(narrow, 10) == dailyfit.index_hash(wide, 10) == dailyfit.array_hash(wide + 10)
    # Control: the landed hash of the raw arrays does differ by width, which is why the probe canonicalises.
    assert dailyfit.array_hash(narrow) != dailyfit.array_hash(wide)


def test_payload_identity_covers_every_array_and_the_meta(tmp_path):
    arrays = {'a': np.arange(4.0), 'b': np.ones((2, 3))}
    meta = {'schema': dailyfit.A1_SCHEMA, 'day': '2026-09-06'}
    base = dailyfit.payload_digest(arrays, meta)
    changed = dict(arrays, a=np.array([0.0, 1.0, 2.0, np.nextafter(3.0, 4.0)]))
    assert dailyfit.payload_digest(changed, meta) != base
    assert dailyfit.payload_digest(arrays, dict(meta, day='2026-09-05')) != base


def test_run_refuses_a_tampered_payload(tmp_path):
    arrays = {'a': np.arange(4.0)}
    meta = {'schema': dailyfit.A1_SCHEMA}
    meta['payload_sha256'] = dailyfit.payload_digest(arrays, meta)
    np.savez_compressed(tmp_path / 'p.npz', a=np.arange(4.0) + 1)
    (tmp_path / 'p.json').write_text(json.dumps(meta))
    with pytest.raises(ValueError, match='recorded identity'):
        dailyfit.run('A1', tmp_path / 'p.npz', tmp_path / 'p.json')


def test_deviation_reports_bitwise_and_per_level_differences():
    q = np.linspace(10.0, 80.0, 24 * 7).reshape(24, 7)
    same = compare.deviation(q, q.copy())
    assert same['bitwise_equal'] and same['max_abs_eur'] == 0.0
    nudged = q.copy()
    nudged[5, 6] = np.nextafter(nudged[5, 6], np.inf)
    diff = compare.deviation(q, nudged)
    assert not diff['bitwise_equal'] and 0 < diff['max_abs_eur'] < 1e-12
    assert diff['max_abs_eur_by_level']['p975'] == diff['max_abs_eur'] and diff['max_abs_eur_by_level']['p50'] == 0.0
    assert compare.deviation(q, q[:23])['shape_equal'] is False


def _member(**changes):
    row = {f: 0 for f in compare.A1_SELECTIONS + compare.A1_DIAGNOSTICS}
    row.update({'member': 0, 'seed': 1, 'held_out_weeks': ['2024-09-23'], 'events': []})
    row.update(changes)
    return row


def test_a1_selections_separate_selections_from_bitwise_diagnostics():
    native = {'members': [_member(member=i) for i in range(8)], 'crossed_rows': 0}
    same_selection = {'members': [_member(member=i, params_sha256='other') for i in range(8)], 'crossed_rows': 0}
    out = compare.a1_selections(native, same_selection)
    assert out['all_match'] and all(d['differences'] == ['params_sha256'] for d in out['diagnostics'])
    epoch = {'members': [_member(member=i, best_epoch=1 if i == 3 else 0) for i in range(8)], 'crossed_rows': 0}
    out = compare.a1_selections(native, epoch)
    assert not out['all_match'] and out['members'][3]['differences'] == ['best_epoch']
    assert not compare.a1_selections(native, dict(native, crossed_rows=1))['all_match']
    assert not compare.a1_selections(native, {'members': native['members'][:7], 'crossed_rows': 0})['all_match']


def test_v2_selections_name_the_hour_whose_alpha_differs():
    hours = [{'local_hour': h, 'selected_relative_alpha': 0.01, 'final_n_iter': 5} for h in range(24)]
    h_layer = {k: 'x' for k in compare.H_SELECTION}
    native = {'selections': {'A1': hours, 'B2': hours}, 'h_layer': dict(h_layer, central_sha256='c'),
              'train_rows_sha256': {'A1': 'a', 'B2': 'b'}}
    other = json.loads(json.dumps(native))
    other['selections']['B2'][7]['selected_relative_alpha'] = 0.02
    other['selections']['A1'][2]['final_n_iter'] = 6
    out = compare.v2_selections(native, other)
    assert not out['all_match'] and out['alpha_differences_by_hour'] == {'A1': [], 'B2': [7]}
    assert out['diagnostics']['A1'] == ['final_n_iter']
    assert compare.v2_selections(native, json.loads(json.dumps(native)))['all_match']
    # The central's hash is a value, not a selection; the buffer is a selection.
    assert compare.v2_selections(native, dict(native, h_layer=dict(h_layer, central_sha256='d')))['all_match']
    assert not compare.v2_selections(native, dict(native, h_layer=dict(h_layer, buffer_sha256='y',
                                                                          central_sha256='c')))['all_match']


def test_every_ddnn2_column_has_one_attribution_group():
    expected = {'price_d1_h00': 'price_d1', 'price_d7_h23': 'price_d7', 'load_d0_h05': 'load_d0',
                'load_d7_h23': 'load_d7', 'gfs_h00_wind10': 'gfs', 'missing_gfs_h03_dswrf': 'gfs',
                'price_roll_mean_168h': 'stats', 'negative_price_count_168h': 'stats', 'weekday_3': 'weekday',
                'is_bridge_day': 'calendar', 'day_type_2': 'calendar', 'month_12': 'calendar'}
    assert {name: column_group(name) for name in expected} == expected
    with pytest.raises(ValueError):
        column_group('crisis_period')


def test_the_holidays_stub_fails_on_any_use():
    stub = _module(SRC / 'cp17probe/stubs/absent/holidays.py')
    with pytest.raises(RuntimeError, match='must not reach it'):
        stub.country_holidays('DE', years=[2026])


def test_the_resource_fallback_reports_zero():
    fallback = _module(SRC / 'cp17probe/stubs/fallback/resource.py')
    assert fallback.FALLBACK and fallback.getrusage(fallback.RUSAGE_SELF).ru_maxrss == 0


def test_the_probe_server_counts_bytes_and_refuses_paths_outside_its_roots(tmp_path):
    (tmp_path / 'app').mkdir()
    (tmp_path / 'app' / 'page.html').write_bytes(b'x' * 123)
    (tmp_path / 'secret.txt').write_text('no')
    server = Server({'/app/': tmp_path / 'app'})
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_address[1]}'
    try:
        assert len(urllib.request.urlopen(base + '/app/page.html').read()) == 123
        for path in ('/app/../secret.txt', '/app/missing.html', '/other/page.html'):
            with pytest.raises(urllib.error.HTTPError):
                urllib.request.urlopen(base + path)
        assert [s['bytes'] for s in server.served if s['status'] == 200] == [123]
    finally:
        server.shutdown()
    assert [category(p) for p in ('/app/x', '/pyodide/pyodide.asm.wasm', '/pyodide/python_stdlib.zip',
                                  '/pyodide/numpy-2.2.5-cp313-cp313-pyodide_2025_0_wasm32.whl',
                                  '/pyodide/openblas-0.3.26.zip', '/bundle/src.zip', '/payloads/a.npz')] == \
        ['page', 'runtime', 'runtime', 'packages', 'packages', 'code', 'data']


def test_the_bundle_ships_the_landed_closure_byte_for_byte_and_deterministically(tmp_path):
    from cp17probe.bundle import STUBS, build
    first = build(SRC, tmp_path / 'one' / 'src.zip')
    second = build(SRC, tmp_path / 'two' / 'src.zip')
    assert first['zip_sha256'] == second['zip_sha256']
    files = first['files_sha256']
    for name in ('cp24/ddnn2.py', 'cp24/design.py', 'cp24/member.py', 'cp15/models.py', 'cp16/residuals.py',
                 'cp21/lgbm.py', 'cp17probe/dailyfit.py', 'cp17probe/attribution.py', *STUBS):
        assert files[name] == hashlib.sha256((SRC / name).read_bytes()).hexdigest()
    # Native-only modules and CP-26's guarded harness never reach the browser.
    assert not any(n.startswith('cp26/') or n in ('cp17probe/native.py', 'cp17probe/payload.py',
                                                    'cp17probe/measure.py', 'cp17probe/compare.py') for n in files)
