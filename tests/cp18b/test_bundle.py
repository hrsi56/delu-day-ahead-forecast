"""The dated bundle (`cp18.bundle`): the seven kinds, built from the live store, verified, gated, and sized.

The committed bundle `reports/cp18b/bundle/` was built from the committed dry-run store as of 2026-09-05 10:00
Europe/Berlin; the build is deterministic, so it is rebuilt here and compared byte for byte.
"""
from __future__ import annotations

from datetime import date, datetime
import json

import pytest

from cp17.schema import FILE_KIND, KINDS, TRAINING_FILE
from cp18 import bundle as B, spaceglue as G
from cp18.store import LiveStore
from cp18b.support18b import BUNDLE, DOWNLOADS, NOW, ROOT, STORE, build, load, local_only


def test_the_committed_bundle_verifies_and_passes_the_gate(files):
    verdict = B.gate(files, ROOT)
    assert verdict['verify'] == {'accepted': True, 'problems': [], 'raised': None}
    assert verdict['identity'] == [] and verdict['publishable'] and verdict['recompute']['match']


def test_the_seven_kinds_and_nothing_else(files):
    manifest = json.loads(files['manifest.json'])
    kinds = {f['kind'] for f in manifest['files']} | {'manifest'}
    assert kinds == set(KINDS)
    assert {f['path'] for f in manifest['files']} | {'manifest.json'} == set(files)
    for f in manifest['files']:
        assert f['kind'] == (FILE_KIND.get(f['path']) or ('training_window' if TRAINING_FILE.match(f['path']) else None))


def test_the_build_is_deterministic_and_reproduces_the_committed_bundle(live, tmp_path):
    record = build(live, tmp_path / 'bundle')
    assert B.read(tmp_path / 'bundle') == B.read(BUNDLE)
    assert record['manifest_sha256'] == load(ROOT / 'reports/cp18b/bundle-build.json')['manifest_sha256']


def test_the_manifest_names_the_served_identity(files):
    manifest = json.loads(files['manifest.json'])
    frozen = load(ROOT / 'docs/track-b/evidence/cp-17c/freeze-manifest.json')
    assert manifest['policy'] == {'policy_identity_sha256': frozen['policy_identity_sha256'],
                                  'package_sha256': frozen['policy_identity']['code']['package_sha256'],
                                  'issuing_host': 'Pyodide 0.28.0 in Node.js v26.7.0'}
    store = LiveStore(STORE)
    store.verify()
    entry = [e for e in store.entries() if e['kind'] == 'issuance'][-1]
    assert manifest['artifact']['artifact_sha256'] == entry['artifact_sha256'] == json.loads(files['artifact.json'])['artifact_sha256']
    assert manifest['times'] == json.loads(files['artifact.json'])['times']


def test_every_issued_day_is_served_from_its_own_artifact(files):
    store = LiveStore(STORE)
    forecasts = json.loads(files['issued-forecasts.json'])
    issued = B.issued_days(store)
    assert [d['delivery_day'] for d in forecasts['days']] == [e['day'] for e in issued if e['artifact']['issued_policy']]
    for d, e in zip(forecasts['days'], issued):
        assert d['issuing_artifact_sha256'] == e['artifact']['artifact_sha256'] and d['quantiles'] == e['artifact']['quantiles']


def test_freshness_fresh_stale_failed_and_the_not_issued_days(live, tmp_path):
    fresh = build(live, tmp_path / 'fresh')
    assert fresh['freshness']['state'] == 'fresh' and fresh['freshness']['as_of_day'] == '2026-09-05'
    gaps = {g['day']: g for g in fresh['not_issued']}
    assert gaps['2026-09-04']['status'] == 'outside'
    stale = build(live, tmp_path / 'stale', now=datetime.fromisoformat('2026-09-06T10:00:00+02:00'))
    assert stale['freshness'] | {} == {**stale['freshness'], 'state': 'stale', 'latest_issued_day': '2026-09-05',
                                       'as_of_day': '2026-09-06'}
    LiveStore(live / 'store').record_not_issued(date(2026, 9, 6), 'h2', ['control'])
    failed = build(live, tmp_path / 'failed', now=datetime.fromisoformat('2026-09-06T10:00:00+02:00'))
    assert failed['freshness']['state'] == 'failed' and failed['freshness']['target_cause'] == 'h2'
    label = json.loads((tmp_path / 'failed' / 'manifest.json').read_text())['product']['evidence_label']
    assert '2026-09-06, a failed H2 check' in label and '2026-09-04, outside the issued record' in label
    for folder in ('fresh', 'stale', 'failed'):
        text = (tmp_path / folder / 'manifest.json').read_text().lower()
        assert 'late' not in text.replace('latest', '') and 'timely' not in text
        assert B.gate(B.read(tmp_path / folder), ROOT)['publishable']          # an honest state is publishable


def test_the_size_budget_is_measured_and_disclosed(files):
    size = B.size(files)
    record = load(ROOT / 'reports/cp18b/bundle-build.json')['size']
    assert size == record
    assert set(size['first_visit_files']) == set(B.START_FILES)
    assert size['training_window_bytes'] == sum(len(v) for k, v in files.items() if k.startswith('A1-'))
    assert size['first_visit_bundle_bytes'] < size['training_window_bytes'] < size['on_request_bytes']


def test_b0_context_equals_the_issuing_hosts_shadow(files):
    store = LiveStore(STORE)
    shadows = {e['day']: e['record']['shadows']['B0']['quantiles_sha256'] for e in B.issued_days(store)}
    items, absent = G.b0_items(files, sorted(shadows))
    assert not absent and {it['day']: it['quantiles_sha256'] for it in items} == shadows


def test_the_series_ends_at_the_last_published_day_within_the_boundary(files):
    series = json.loads(files['series.json'])
    assert series['last_day'] == '2026-09-05' and series['first_day'] == '2019-01-01'
    assert B.last_published(datetime.fromisoformat('2026-09-06T23:00:00+02:00')) == date(2026, 9, 6)
    assert B.last_published(NOW) == date(2026, 9, 5)


@local_only(DOWNLOADS / '41204328732/results-sha256.txt', "CP-18a's downloaded run records")
def test_the_committed_store_is_the_runs_carried_store():
    sources = load(ROOT / 'reports/cp18b/sources.json')['store']
    run = {line.split('  ', 1)[1][2:]: line.split('  ', 1)[0]
           for line in (DOWNLOADS / '41204328732/results-sha256.txt').read_text().splitlines()}
    assert sources['equal_to_the_run_results_sha256']
    assert all(run['live/' + k] == v for k, v in sources['files'].items())


def test_a_refused_bundle_is_not_publishable(files):
    from cp18.controls import mismatch
    verdict = B.gate(mismatch(files), ROOT)
    assert not verdict['publishable'] and verdict['recompute']['blocks_publication']
