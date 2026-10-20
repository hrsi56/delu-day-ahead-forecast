"""Lightweight gate tests: exact bits, custody, keys, complete coverage and fail-closed execution.

No model is fitted and no evaluation loss is computed. The real-reference test reads only
guarded, sampled central columns from manifest-bound committed old-fold artifacts.
"""
from datetime import date
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

from cp26 import parity as P
from cp25 import guard


def _keys():
    return pd.date_range('2021-03-31T22:00:00Z', periods=2, freq='h').as_unit('ns')


def test_bits_require_signed_zero_precision_shape_and_finite_values():
    assert not P.bitwise_equal(np.array([0.0]), np.array([-0.0]))
    assert not P.bitwise_equal(np.array([1.0]), np.array([np.nextafter(1.0, 2.0)]))
    assert not P.bitwise_equal(np.array([1.0]), np.array([1.0], dtype=np.float32))
    assert not P.bitwise_equal(np.array([np.nan]), np.array([np.nan]))
    assert not P.bitwise_equal(np.array([1.0]), np.array([[1.0]]))
    assert P.bitwise_equal(np.array([1.0, -0.0]), np.array([1.0, -0.0], dtype='>f8'))


def test_compare_keeps_exact_bits_and_refuses_reordered_keys():
    expected = np.array([1.0, 2.0])
    altered = expected.copy()
    altered[1] = np.nextafter(2.0, 3.0)
    out = P.compare(expected, altered, _keys(), _keys())
    assert out['keys_equal'] and not out['bitwise_equal']
    assert out['expected_float64_bits'] == ['3ff0000000000000', '4000000000000000']
    assert out['expected_sha256'] != out['actual_sha256']
    assert out['actual_float64_bits'][1] == '4000000000000001'
    out = P.compare(expected, expected, _keys(), _keys()[::-1])
    assert not out['keys_equal'] and not out['bitwise_equal']
    assert out['actual_timestamp_utc'] != list(map(str, _keys()))


def test_reference_read_guards_before_materialisation(monkeypatch, tmp_path):
    called = []
    monkeypatch.setattr(P.pd, 'read_parquet', lambda *a, **k: called.append(True))
    with pytest.raises(guard.BoundaryRefused):
        P._day(tmp_path, 'ref.parquet', 'fold_2', date(2026, 9, 7), ('central',))
    assert called == []


def test_reference_read_uses_exact_day_filters_and_excludes_truths(monkeypatch, tmp_path):
    day = date(2021, 4, 1)
    calls = []
    def read(path, **kwargs):
        calls.append(kwargs)
        return pd.DataFrame({'fold': ['fold_2'] * 2, 'delivery_date': [day] * 2,
                             'timestamp_utc': _keys(), 'central': [1.0, 2.0], 'policy': ['A1'] * 2})
    monkeypatch.setattr(P.pd, 'read_parquet', read)
    frame = P._day(tmp_path, 'ref.parquet', 'fold_2', day, ('central',), 'A1')
    assert len(frame) == 2
    assert calls[0]['filters'] == [('delivery_date', '==', day), ('fold', '==', 'fold_2'), ('policy', '==', 'A1')]
    assert 'y_true' not in calls[0]['columns']


def test_custody_refuses_uncommitted_or_unmanifested_reference(monkeypatch, tmp_path):
    (tmp_path / 'ref.json').write_text('{}')
    actual = P.sha(tmp_path / 'ref.json')
    (tmp_path / 'manifest.json').write_text(json.dumps({'artifact_sha256': {'ref.json': actual}}))
    monkeypatch.setattr(P, 'SOURCES', {'fixture': P.Source('commit', 'manifest.json', ('ref.json',))})
    monkeypatch.setattr(P.H, 'git_blob_sha256', lambda root, rev, name: P.sha(root / name))
    assert P.verify_sources(tmp_path)['fixture']['files_sha256']['ref.json'] == actual
    monkeypatch.setattr(P.H, 'git_blob_sha256', lambda root, rev, name: 'changed' if name == 'ref.json' else P.sha(root / name))
    with pytest.raises(P.H.HarnessError, match='committed'):
        P.verify_sources(tmp_path)
    monkeypatch.setattr(P.H, 'git_blob_sha256', lambda root, rev, name: P.sha(root / name))
    (tmp_path / 'manifest.json').write_text(json.dumps({'artifact_sha256': {}}))
    with pytest.raises(P.H.HarnessError, match='committed'):
        P.verify_sources(tmp_path)


@pytest.fixture
def fake_gate(monkeypatch):
    """Substitute model fitting with two fixed values, preserving the real gate's control flow."""
    sample = ('fold_2', date(2021, 4, 1))
    monkeypatch.setattr(P, 'SAMPLES', (sample,))
    central = {name: np.array([1.0, 2.0]) for name in P.MEMBERS}
    central.update(P.assemble(central))
    refs = {sample: {'keys': _keys(), 'central': central,
                     'ensemble': {'complete': True, 'members': [{'seed': 42}]}}}
    monkeypatch.setattr(P, 'load_references', lambda root: (refs, {'fixture': 'custody'}))
    monkeypatch.setattr(P.H, 'input_fingerprint', lambda root: 'inputs')
    monkeypatch.setattr(P.H, 'check_blas', lambda: None)
    monkeypatch.setattr(P, 'sha', lambda path: 'code')
    monkeypatch.setattr(P.subprocess, 'check_output', lambda *a, **k: 'candidate\n')
    builds, fits = [], []
    def build(root, settings, variant, restore=False):
        builds.append((settings, variant, restore))
        return SimpleNamespace(settings=settings, noload_active=False, variant=variant,
                               restore=restore, data=SimpleNamespace(index=_keys(), rows=lambda day: np.array([0, 1])))
    monkeypatch.setattr(P.M.Context, 'build', build)
    def fit(ctx, day, *, ensemble, k):
        assert ensemble == refs[sample]['ensemble'] and k is None
        fits.append((ctx.variant, ctx.restore, day))
        return {'status': 'ok', 'central': np.array([1.0, 2.0]), 'records': [], 'fits': {'fixture': 1}}
    monkeypatch.setattr(P.M, 'FITTERS', {name: fit for name in P.MEMBERS})
    return builds, fits


def test_complete_gate_runs_both_paths_and_saves_success_only_at_end(fake_gate, tmp_path, monkeypatch):
    stages = []
    original = P.atomic
    def save(path, obj):
        stages.append((obj['status'], len(obj['checks'])))
        original(path, obj)
    monkeypatch.setattr(P, 'atomic', save)
    report = P.run(tmp_path)
    builds, fits = fake_gate
    assert builds == [(P.H.OLD, 'nominal', False), (P.H.OLD, 'noload', True)]
    assert len(fits) == 16
    assert report['status'] == 'PASS' and len(report['checks']) == 24
    assert all(status == 'RUNNING' for status, _ in stages[:-1])
    assert stages[-1] == ('PASS', 24)
    assert json.loads((tmp_path / P.OUT).read_text())['status'] == 'PASS'
    P.validate_report(report)


def test_gate_stops_after_first_bit_mismatch_and_saves_exact_failure(fake_gate, tmp_path, monkeypatch):
    calls = []
    def wrong(ctx, day, **kwargs):
        calls.append(day)
        return {'status': 'ok', 'central': np.array([1.0, np.nextafter(2.0, 3.0)])}
    monkeypatch.setitem(P.M.FITTERS, 'B0', wrong)
    with pytest.raises(P.ParityFailed) as exc:
        P.run(tmp_path)
    assert len(calls) == 1
    assert len(exc.value.report['checks']) == 1
    saved = json.loads((tmp_path / P.OUT).read_text())
    assert saved['status'] == 'FAIL' and saved['checks'][0]['actual_float64_bits'][1] == '4000000000000001'
    with pytest.raises(P.H.HarnessError, match='failed, incomplete'):
        P.validate_report(saved)


@pytest.mark.parametrize('damage', ['missing', 'duplicate', 'false_bits', 'keys'])
def test_consumer_refuses_incomplete_or_corrupted_gate(fake_gate, tmp_path, damage):
    report = P.run(tmp_path)
    if damage == 'missing':
        report['checks'].pop()
    elif damage == 'duplicate':
        report['checks'].append(report['checks'][0])
    elif damage == 'false_bits':
        report['checks'][0]['actual_float64_bits'] = ['0000000000000000'] * 2
    else:
        report['checks'][0]['actual_timestamp_utc'].reverse()
    with pytest.raises(P.H.HarnessError, match='failed, incomplete'):
        P.validate_report(report)


def test_real_references_are_committed_and_internally_bitwise_consistent(monkeypatch):
    from cp26.gates import OUTPUT
    root = Path(__file__).resolve().parents[1]
    # Each reference's evidence commit is reachable only from a local evidence/<cp> tag, which a
    # squash LAND and CI's depth-1 checkout do not carry. The parity gate recorded every blob it
    # verified at those commits, so custody reads that record instead of the Git history.
    recorded = json.loads((root / OUTPUT / 'parity.json').read_text())['reference_custody']
    blobs = {(item['evidence_commit'], name): digest for item in recorded.values()
             for name, digest in [(item['manifest'], item['manifest_sha256']), *item['files_sha256'].items()]}
    monkeypatch.setattr(P.H, 'git_blob_sha256', lambda _root, rev, name: blobs[(rev, name)])
    refs, custody = P.load_references(root)
    assert custody == recorded
    assert len(refs) == 4 and set(custody) == {'cp15', 'cp16', 'cp20', 'cp21', 'cp23', 'cp24'}
    for (fold, day), ref in refs.items():
        assert fold in {'fold_2', 'fold_3', 'fold_4', 'fold_5'}
        assert day <= P.H.OLD_BOUNDARY
        assert len(ref['ensemble']['members']) == 8
        assert all(set(m) == {'config', 'rank', 'seed'} for m in ref['ensemble']['members'])
        assert len(ref['keys']) == len(ref['central']['B0'])
        assert set(ref['central']) == set(P.MEMBERS + P.POLICIES)
