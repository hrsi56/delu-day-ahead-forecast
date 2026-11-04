"""The glue the Space and the pipeline share (`cp18.spaceglue`): the recomputation, attribution and features from the
served fitted artifact, and the retrain comparison. The browser runs the same file; here it runs natively."""
from __future__ import annotations

import ast
import json
from pathlib import Path

import numpy as np
import pytest

from cp18 import controls as C, spaceglue as G
from cp18b.support18b import DOWNLOADS, ROOT, local_only

GLUE = ROOT / 'src/cp18/spaceglue.py'
HOST_RUN = DOWNLOADS / '41204328732/run/runs/A1-2026-09-05-99uiyjua/run.json'


def test_the_recomputation_matches_on_the_served_bundle(files):
    check = G.recompute(files)
    assert check['match'] and not check['blocks_publication'] and check['recomputed_windows'] == 6
    rows = [r for r in check['rows'] if r['recomputed']]
    assert {(r['window'], r['policy']) for r in rows} == {(w, p) for w in ('development', '4.7T', 'prospective')
                                                          for p in ('product', 'B0')}
    rehearsal = next(r for r in rows if r['evidence_class'] == G.REHEARSAL and r['policy'] == 'product')
    assert rehearsal['compared'] > 200 and all(s['recomputed'] == s['committed'] for s in rehearsal['shown'])
    static = [r for r in check['rows'] if not r['recomputed']]
    assert len(static) == 4 and all('static, from evidence' in r['note'] for r in static)


def test_explain_reproduces_the_issued_fit_and_adds_up(files):
    e = G.explain(files)
    assert e['reproduced'] == 'bit for bit' or e['reproduced'].startswith('within the frozen recomputation tolerance')
    phi = np.asarray(e['phi_eur'])
    assert phi.shape == (len(e['players']), 24) and e['coalitions'] == 2 ** len(e['players'])
    assert np.allclose(phi.sum(axis=0), np.asarray(e['full_p50']) - np.asarray(e['baseline_p50']), atol=1e-9)
    assert e['efficiency_max_abs'] < 1e-9 and 'never causality' in e['wording']


@local_only(HOST_RUN, "the issuing host's run record of 2026-09-05 (CP-18a's download)")
def test_explain_equals_the_issuing_hosts_attribution_within_rounding(files):
    host = json.loads(HOST_RUN.read_text())['python']['result']['attribution']
    e = G.explain(files)
    assert e['players'] == host['players']
    assert np.abs(np.asarray(e['phi_eur']) - np.asarray(host['phi_eur'])).max() < 1e-9


def test_explain_refuses_arrays_that_are_not_the_issued_fits(files):
    import io
    with np.load(io.BytesIO(files['artifact-arrays.npz'])) as z:
        arrays = {k: z[k] for k in z.files}
    arrays['member0_param0'] = arrays['member0_param0'] * 1.001
    trial = dict(files, **{'artifact-arrays.npz': C._npz_bytes(arrays)})
    with pytest.raises(ValueError, match='do not reproduce the issued quantiles'):
        G.explain(trial)


def test_features_in_source_units_with_reliance(files):
    f = G.features(files)
    units = {r['name']: r['unit'] for r in f['inputs']}
    assert units['price_d1_h00'] == 'EUR/MWh' and units['load_d0_h00'] == 'MW' and units['gfs_h00_dswrf'] == 'W/m²'
    assert all(r['percentile'] is None or 0 <= r['percentile'] <= 1 for r in f['inputs'])
    assert {r['group'] for r in f['reliance']} <= set(__import__('cp17.attribution', fromlist=['GROUPS']).GROUPS)
    assert f['window_days'] > 700 and 'not causality' in f['wording']


@local_only(HOST_RUN, "the issuing host's run record of 2026-09-05 (CP-18a's download)")
def test_a_retrain_equal_to_the_issued_fit_is_identical_bit_for_bit(files):
    result = json.loads(HOST_RUN.read_text())['python']['result']
    report = G.retrain_report(json.loads(files['artifact.json']), result)
    assert report['status'] == 'identical bit for bit' and report['selections_match'] and report['payload_sha256_equal']
    assert set(report['deviation']['max_abs_eur_by_level']) == {'p025', 'p10', 'p25', 'p50', 'p75', 'p90', 'p975'}
    assert all(not r['differences'] for r in report['selections'])


def test_a_retrain_on_another_day_is_different(files):
    artifact = json.loads(files['artifact.json'])
    report = G.retrain_report(artifact, {'day': '2026-09-04', 'index': artifact['keys'], 'quantiles': artifact['quantiles']})
    assert report['status'] == 'different'


@pytest.mark.stress
def test_a_retrain_with_a_changed_seed_is_reported_different(files, tmp_path):
    """The negative control, for real: A1 refitted natively on the served window with member 0's seed changed."""
    from cp17 import dailyfit
    variant = C.seed_variant(files)
    artifact = json.loads(files['artifact.json'])
    stem = f"A1-{artifact['delivery_day']}"
    (tmp_path / f'{stem}.json').write_bytes(variant[f'{stem}.json'])
    (tmp_path / f'{stem}.npz').write_bytes(variant[f'{stem}.npz'])
    result = dailyfit.run('A1', tmp_path / f'{stem}.npz', tmp_path / f'{stem}.json')
    report = G.retrain_report(artifact, result)
    assert report['status'] == 'different' and report['measured_status'] == 'different'
    assert report['selections'][0]['differences'] and report['deviation']['max_abs_eur'] > 0.01


def test_the_glue_imports_only_the_frozen_package_numpy_and_the_standard_library():
    tree = ast.parse(GLUE.read_text())
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names |= {a.name.split('.')[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.level == 0:
            names.add(node.module.split('.')[0])
    assert names <= {'__future__', 'datetime', 'io', 'json', 'os', 'tempfile', 'numpy', 'cp17', 'cp24'}
    zipped = json.loads((ROOT / 'docs/track-b/evidence/cp-17c/freeze-manifest.json').read_text())
    shipped = zipped['policy_identity']['code']
    assert shipped['package_sha256']
