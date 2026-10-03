"""CP-22 committed evidence re-derives from committed rows (§20.10 items 5-7 and 10).

These tests never re-run the bootstrap or re-score the saved references: each of those is a capped
analysis or reference pass (§20.8), and a test suite runs many times. They recompute the new
policies' losses from their committed predictions, re-derive every interval from the stored
replicates, and re-apply the three mechanical §20.6 rules to the committed rows -- each with a
negative control that must change the result.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from cp15.scoring import FOLDS, QUANTILES, score_hourly
from cp22 import scoring as S

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'reports/v4-revision'
pytestmark = pytest.mark.skipif(not (OUT / 'decisions.json').exists(), reason='CP-22 results not yet committed')


@pytest.fixture(scope='module')
def decisions():
    return json.loads((OUT / 'decisions.json').read_text())


@pytest.fixture(scope='module')
def new(decisions):
    parts = [pd.read_parquet(OUT / 'predictions.parquet')]
    if decisions['replacement']['winner']:
        parts.append(pd.read_parquet(OUT / 'predictions-w.parquet'))
    return pd.concat(parts, ignore_index=True)


@pytest.fixture(scope='module')
def metrics():
    return pd.read_csv(OUT / 'metrics.csv', float_precision='round_trip')


@pytest.fixture(scope='module')
def uncertainty():
    return pd.read_csv(OUT / 'uncertainty.csv', float_precision='round_trip')


@pytest.fixture(scope='module')
def criteria():
    return pd.read_csv(OUT / 'criteria.csv', float_precision='round_trip')


def test_every_new_policy_issues_all_10747_keys_finite_and_ordered(new, decisions):
    expected = pd.read_parquet(ROOT / 'reports/cp15/predictions.parquet', columns=['fold', 'timestamp_utc'],
                               filters=[('policy', '==', 'B0')])
    keys = set(zip(expected.fold, pd.to_datetime(expected.timestamp_utc, utc=True)))
    assert set(new.policy) == set(S.FIXED_NEW + (S.W_ARMS if decisions['replacement']['winner'] else ()))
    for policy, part in new.groupby('policy'):
        assert len(part) == 10747 and set(zip(part.fold, pd.to_datetime(part.timestamp_utc, utc=True))) == keys
        q = part[list(QUANTILES)].to_numpy(float)
        assert np.isfinite(q).all() and (np.diff(q, axis=1) >= 0).all()
        assert part.groupby('fold').size().to_dict() == S.FOLD_COUNTS
    assert pd.to_datetime(new.delivery_date).max() <= pd.Timestamp('2026-04-07')
    assert (new.evidence_class == 'development_post_selection').all()
    assert not np.array_equal(new.p50.to_numpy(), new.central.to_numpy())  # emitted p50 kept separate


def test_pn_is_issued_for_every_key():
    members = pd.read_parquet(OUT / 'members.parquet')
    assert len(members) == 10747 and np.isfinite(members[['PN-avg', 'PN-sel']].to_numpy()).all()
    assert not np.array_equal(members['PN-avg'].to_numpy(), members['PN-sel'].to_numpy())


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
        for source, policies in ((cp20, ('B0', 'B1', 'B2', 'B3', 'A1', 'H0', 'HG')), (cp21, ('HGL',))):
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


def test_the_three_rules_reapply_mechanically_to_the_committed_rows(uncertainty, criteria, metrics, decisions):
    w = decisions['replacement']['winner']
    rep = S.replacement(uncertainty, criteria, keys_complete=True)
    assert rep['winner'] == w and rep['verdict'] == decisions['replacement']['verdict']
    assert rep['first_unmet_condition'] == decisions['replacement']['first_unmet_condition']
    dl = S.dynamic_layer(uncertainty, criteria, metrics, w) if w else S.dynamic_layer(None, None, None, None)
    assert dl['verdict'] == decisions['dynamic_layer']['verdict']
    assert S.fast_component(uncertainty, criteria, dl)['verdict'] == decisions['fast_component']['verdict']
    for key, r in decisions['contrasts'].items():
        c, b = next((c, b) for c, b, _ in S.contrasts(w) if f'{c}-{b}' == key)
        assert S.joint_reading(uncertainty, c, b)['reading'] == r['reading']
    # negative control: moving one per-fold lower endpoint above zero changes a met condition 4
    if rep['candidates']['M']['conditions'][4]['met'] or rep['candidates']['R']['conditions'][4]['met']:
        cand = 'R' if rep['candidates']['R']['conditions'][4]['met'] else 'M'
        broken = uncertainty.copy()
        mask = broken.scope.eq('fold_1') & broken.candidate.eq(cand) & broken.baseline.eq('HGL') & broken.metric.eq('MAE')
        broken.loc[mask, 'ci_lower'] = 1.0
        assert not S.replacement(broken, criteria, keys_complete=True)['candidates'][cand]['conditions'][4]['met']
    else:  # every per-fold degradation removed: condition 4 becomes met for both
        repaired = uncertainty.copy()
        repaired.loc[repaired.scope.isin(FOLDS), 'ci_lower'] = np.minimum(repaired.loc[repaired.scope.isin(FOLDS), 'ci_lower'], -1e-9)
        again = S.replacement(repaired, criteria, keys_complete=True)
        assert again['candidates']['R']['conditions'][4]['met'] and again['candidates']['M']['conditions'][4]['met']


def test_hash_bound_files_are_stored_byte_for_byte():
    for name in ('protocol.json', 'lineage.json', 'decisions.json', 'replacement.json', 'predictions.parquet', 'members.parquet'):
        committed = subprocess.check_output(['git', 'show', f'HEAD:reports/v4-revision/{name}'], cwd=ROOT)
        assert committed == (OUT / name).read_bytes(), name
    attributes = subprocess.check_output(['git', 'check-attr', 'text', 'reports/v4-revision/protocol.json',
                                          'docs/track-b/evidence/cp-22/issued-brief.md'], cwd=ROOT, text=True)
    assert attributes.count('text: unset') == 2
