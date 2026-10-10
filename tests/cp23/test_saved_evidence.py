"""CP-23 committed evidence re-derives from committed rows (§21.10 items 9-11 and 14).

These tests never re-run the bootstrap, re-score the saved references or fit DDNN: each of those is a capped
pass or fit (§21.8), and a test suite runs many times. They recompute the new policies' losses from their
committed predictions, re-derive every interval from the stored replicates, re-apply `cp23-adoption` and the
configuration rule to the committed rows, and check that the generated documents equal their generators.
Each has a negative control that must change the result.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from cp15.scoring import FOLDS, QUANTILES, score_hourly
from cp23 import ddnn as D
from cp23 import scoring as S

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'reports/distribution-challenger'
pytestmark = pytest.mark.skipif(not (OUT / 'decisions.json').exists(), reason='CP-23 results not yet committed')


@pytest.fixture(scope='module')
def decisions():
    return json.loads((OUT / 'decisions.json').read_text())


@pytest.fixture(scope='module')
def new():
    return pd.read_parquet(OUT / 'predictions.parquet')


@pytest.fixture(scope='module')
def metrics():
    return pd.read_csv(OUT / 'metrics.csv', float_precision='round_trip')


@pytest.fixture(scope='module')
def uncertainty():
    return pd.read_csv(OUT / 'uncertainty.csv', float_precision='round_trip')


@pytest.fixture(scope='module')
def criteria():
    return pd.read_csv(OUT / 'criteria.csv', float_precision='round_trip')


def test_every_new_policy_issues_all_10747_keys_finite_and_ordered(new):
    expected = pd.read_parquet(ROOT / 'reports/cp15/predictions.parquet', columns=['fold', 'timestamp_utc'],
                               filters=[('policy', '==', 'B0')])
    keys = set(zip(expected.fold, pd.to_datetime(expected.timestamp_utc, utc=True)))
    assert set(new.policy) == set(S.NEW)
    for policy, part in new.groupby('policy'):
        assert len(part) == 10747 and set(zip(part.fold, pd.to_datetime(part.timestamp_utc, utc=True))) == keys
        q = part[list(QUANTILES)].to_numpy(float)
        assert np.isfinite(q).all() and (np.diff(q, axis=1) >= 0).all()
        assert part.groupby('fold').size().to_dict() == S.FOLD_COUNTS
    assert pd.to_datetime(new.delivery_date).max() <= pd.Timestamp('2026-04-07')
    assert (new.evidence_class == 'development_post_selection').all()
    for policy in ('v5', 'v3+D'):  # the emitted p50 is kept separate from the central forecast
        part = new.loc[new.policy.eq(policy)]
        assert not np.array_equal(part.p50.to_numpy(), part.central.to_numpy())
    d = new.loc[new.policy.eq('D')]
    assert np.array_equal(d.p50.to_numpy(), d.central.to_numpy())  # D's p50 is its central forecast, the ensemble median


def test_the_composites_are_the_fixed_one_third_member_on_every_key(new):
    members = pd.read_parquet(OUT / 'members.parquet').sort_values(['fold', 'timestamp_utc']).reset_index(drop=True)
    piv = {p: g.sort_values(['fold', 'timestamp_utc']).reset_index(drop=True) for p, g in new.groupby('policy')}
    assert len(members) == 10747 and np.isfinite(members[['D', 'HG', 'HGL']].to_numpy()).all()
    assert np.max(np.abs(piv['v5'].central - (2 / 3) * members.HGL - members.D / 3)) <= 1e-9
    assert np.max(np.abs(piv['v3+D'].central - (2 / 3) * members.HG - members.D / 3)) <= 1e-9
    assert np.array_equal(piv['D'].central.to_numpy(), members.D.to_numpy())
    # negative control: a different member weight is caught
    assert np.max(np.abs(piv['v5'].central - 0.6 * members.HGL - 0.4 * members.D)) > 1e-3


def test_new_policy_metrics_recompute_from_committed_predictions(new, metrics):
    frame = new.copy()
    frame['timestamp_utc'] = pd.to_datetime(frame.timestamp_utc, utc=True)
    frame['delivery_date'] = pd.to_datetime(frame.delivery_date)
    hourly = score_hourly(frame)
    per_fold = metrics.loc[metrics.scope.eq('per_fold')].set_index(['policy', 'fold'])
    for (policy, fold), part in hourly.groupby(['policy', 'fold']):
        row = per_fold.loc[(policy, fold)]
        assert len(part) == row.n_hours
        assert abs(part.absolute_error.mean() - row.MAE) <= 1e-9
        assert abs(part.WIS.mean() - row.WIS) <= 1e-9
        assert abs(part.hit95.mean() - row.coverage95) <= 1e-12
    equal = metrics.loc[metrics.scope.eq('equal_fold')].set_index('policy')
    for policy in set(new.policy):
        for metric in ('MAE', 'WIS'):
            ratio = np.mean([per_fold.loc[(policy, f), metric] / per_fold.loc[('B0', f), metric] for f in FOLDS])
            assert abs(ratio - equal.loc[policy, f'S_{metric}']) <= 1e-12


def test_saved_reference_rows_equal_their_committed_metrics(metrics):
    cp20 = pd.read_csv(ROOT / 'reports/weather-ablation/metrics.csv', float_precision='round_trip')
    cp21 = pd.read_csv(ROOT / 'reports/block-challenger/metrics.csv', float_precision='round_trip')
    for scope in ('per_fold', 'pooled'):
        for source, policies in ((cp20, ('B0', 'B1', 'B2', 'B3', 'A1', 'HG')), (cp21, ('HGL',))):
            ours = metrics.loc[metrics.scope.eq(scope) & metrics.policy.isin(policies)].set_index(['policy', 'fold']).sort_index()
            theirs = source.loc[source.scope.eq(scope) & source.policy.isin(policies)].set_index(['policy', 'fold']).sort_index()
            for column in ('MAE', 'WIS', 'coverage95', 'n_hours'):
                np.testing.assert_allclose(ours[column].to_numpy(float), theirs[column].to_numpy(float), rtol=0, atol=1e-9)


def test_every_interval_rederives_from_its_stored_replicates(uncertainty):
    draws = pd.read_parquet(OUT / 'replicates.parquet')
    assert set(draws.replicate) == set(range(S.BOOTSTRAP_REPLICATES))
    grouped = {k: g for k, g in draws.groupby(['scope', 'candidate', 'baseline', 'metric'])}
    for row in uncertainty.itertuples():
        d = grouped[(row.scope, row.candidate, row.baseline, row.metric)]
        assert len(d) == S.BOOTSTRAP_REPLICATES
        lo, hi = np.quantile(d.difference, [.025, .975], method='linear')
        assert (lo, hi) == (row.ci_lower, row.ci_upper)
        if row.scope == 'equal_fold':
            rlo, rhi = np.quantile(d.ratio, [.025, .975], method='linear')
            assert (rlo, rhi) == (row.ratio_ci_lower, row.ratio_ci_upper)
    scores = pd.read_parquet(OUT / 'replicate-scores.parquet')
    for c, b in {(r.candidate, r.baseline) for r in uncertainty.itertuples()}:
        for metric in ('MAE', 'WIS'):
            sc = scores.loc[scores.policy.eq(c) & scores.metric.eq(metric)].S.to_numpy()
            sb = scores.loc[scores.policy.eq(b) & scores.metric.eq(metric)].S.to_numpy()
            d = grouped[('equal_fold', c, b, metric)]
            np.testing.assert_array_equal(d.difference.to_numpy(), sc - sb)
            np.testing.assert_array_equal(d.ratio.to_numpy(), sc / sb - 1)


def test_the_rule_reapplies_mechanically_to_the_committed_rows(uncertainty, criteria, decisions):
    again = S.adoption(uncertainty, criteria, keys_complete=True)
    assert again['adopted'] == decisions['adoption']['adopted']
    assert again['verdict'] == decisions['adoption']['verdict']
    assert again['first_unmet_condition'] == decisions['adoption']['first_unmet_condition']
    assert again['unmet_conditions'] == decisions['adoption']['unmet_conditions']
    for key, r in decisions['contrasts'].items():
        c, b = next((c, b) for c, b, _ in S.contrasts() if f'{c}-{b}' == key)
        assert S.joint_reading(uncertainty, c, b)['reading'] == r['reading']
    # negative control: v5 - v4 moved wholly below zero in both scores and per fold satisfies conditions 1 and 4
    better = uncertainty.copy()
    mask = better.candidate.eq('v5') & better.baseline.eq('HGL')
    better.loc[mask, 'ci_upper'] = -1e-3
    better.loc[mask, 'ci_lower'] = -1.0
    flipped = S.adoption(better, criteria, keys_complete=True)
    assert flipped['conditions'][1]['met'] and flipped['conditions'][4]['met']
    assert flipped['adopted'] == bool(again['conditions'][2]['met'])


def test_the_configuration_choice_follows_its_rule_and_is_fixed_through_each_fold():
    sel = json.loads((OUT / 'selection.json').read_text())
    members = pd.read_parquet(OUT / 'members.parquet')
    order = [c['id'] for c in D.CONFIGS]
    for fold, entry in sel['folds'].items():
        losses = entry['holdout_mae']
        assert entry['selected'] == min(order, key=lambda c: (losses[c], order.index(c)))
        assert set(members.loc[members.fold.eq(fold), 'config']) == {entry['selected']}
        assert entry['rows']['holdout_last'] < entry['first_origin']
    # negative control: a tied loss goes to the smaller configuration, not the listed choice
    tied = dict(sel['folds']['fold_2']['holdout_mae'])
    tied['C1'] = tied[sel['folds']['fold_2']['selected']]
    assert min(order, key=lambda c: (tied[c], order.index(c))) == 'C1'


def test_the_generated_documents_equal_their_generators():
    env = {'PYTHONPATH': str(ROOT / 'src'), 'PATH': '/usr/bin:/bin'}
    for module in ('cp23.packet', 'cp23.claims'):
        run = subprocess.run([sys.executable, '-m', module, '--check'], cwd=ROOT, capture_output=True, text=True, env=env)
        assert run.returncode == 0, (module, run.stdout[-2000:], run.stderr[-2000:])


#: Owner-authorized work-availability amendment, 2026-10-10. Historical source hashes
#: bind the evidence tag; current monitor behaviour is tested in test_work_availability.
AMENDED_BY_WORK_AVAILABILITY = frozenset({
    'scripts/cp23_ddnn.py', 'src/cp23/budget.py', 'src/cp23/protocol.py',
    'tests/cp23/test_saved_evidence.py',
})


def test_byte_exact_storage_of_every_manifested_file():
    path = OUT / 'artifact-manifest.json'
    if not path.exists():
        pytest.skip('the artifact manifest is written at finalisation')
    from cp15.data import sha
    manifest = json.loads(path.read_text())['artifact_sha256']
    assert AMENDED_BY_WORK_AVAILABILITY <= set(manifest)
    for name, digest in manifest.items():
        if name not in AMENDED_BY_WORK_AVAILABILITY:
            assert sha(ROOT / name) == digest, name
    protocol = json.loads((OUT / 'protocol.json').read_text())
    assert sha(ROOT / 'docs/track-b/evidence/cp-23/issued-brief.md') == protocol['issued_brief']['sha256']
    for name in ('docs/track-b/evidence/cp-23/.gitattributes', 'reports/distribution-challenger/.gitattributes'):
        assert '* -text' in (ROOT / name).read_text()


def test_amended_files_keep_their_reviewed_bytes_at_the_evidence_tag():
    import hashlib
    manifest = json.loads((OUT / 'artifact-manifest.json').read_text())['artifact_sha256']
    tag = subprocess.run(['git', 'rev-parse', '--verify', '--quiet', 'evidence/cp-23^{commit}'],
                         cwd=ROOT, capture_output=True, text=True)
    if tag.returncode != 0:
        pytest.skip('evidence/cp-23 is not in this checkout')
    for name in sorted(AMENDED_BY_WORK_AVAILABILITY):
        data = subprocess.check_output(['git', 'show', f'evidence/cp-23:{name}'], cwd=ROOT)
        assert hashlib.sha256(data).hexdigest() == manifest[name], name
