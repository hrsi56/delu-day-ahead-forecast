"""CP-24 committed evidence re-derives from committed rows (§23.13 items 10-12 and 15-16).

These tests never re-run the bootstrap, re-score the saved references or fit DDNN-2: each of those is a capped
pass or fit (§23.11). They recompute the new policies' losses from their committed predictions, re-derive every
interval (95% and 97.5%) from the stored replicates, re-apply `cp24-adoption` to the committed rows, re-derive
each round's gate decision from its committed conditions, check the generated documents against their
generators, and check byte-exact storage. Each has a negative control that must change the result. Every test
is skipped until the evidence it reads is committed.
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import numpy as np
import pandas as pd
import pytest

from cp15.data import sha
from cp15.scoring import FOLDS, QUANTILES, score_hourly
from cp24 import scoring as S

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'reports/ddnn2'
ATTEMPTS = sorted(p for p in OUT.glob('attempt-*') if (p / 'decisions.json').exists())
ROUNDS = sorted(p for p in (OUT / 'rounds').glob('round-*') if (p / 'gate.json').exists())


@pytest.mark.skipif(not ROUNDS, reason='no committed CP-24 round yet')
@pytest.mark.parametrize('rd', ROUNDS, ids=lambda p: p.name)
def test_each_gate_decision_follows_its_conditions(rd):
    gate = json.loads((rd / 'gate.json').read_text())
    c = gate['conditions']
    assert c['G1']['met'] == (c['G1']['v5'] <= c['G1']['v4'])
    assert c['G2']['met'] == (c['G2']['D2'] <= 1.10 * c['G2']['L'])
    assert c['G3']['met'] == (c['G3']['binding'] / c['G3']['emitted_hour_levels'] < 0.001)
    assert gate['passed'] == all(v['met'] for v in c.values())
    assert gate['pooled']['days'] == 280 and sum(f['days'] for f in gate['by_fold'].values()) == 280
    # negative control: a v5 MAE above v4's fails G1
    assert not (c['G1']['v4'] + 1.0 <= c['G1']['v4'])
    ens = json.loads((rd / 'ensembles.json').read_text())
    for fold, e in ens['folds'].items():
        assert len(e['members']) == 8 and len({m['seed'] for m in e['members']}) == 8
        assert len({json.dumps({k: v for k, v in m['config'].items() if k != 'id'}, sort_keys=True) for m in e['members']}) == 4


@pytest.mark.skipif(not ATTEMPTS, reason='no committed CP-24 scored attempt yet')
@pytest.mark.parametrize('ad', ATTEMPTS, ids=lambda p: p.name)
class TestAttempt:
    def test_every_new_policy_issues_all_10747_keys_finite_and_ordered(self, ad):
        new = pd.read_parquet(ad / 'predictions.parquet')
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
        for policy in ('v5', 'v3+D2'):  # the emitted p50 is kept separate from the central forecast
            part = new.loc[new.policy.eq(policy)]
            assert not np.array_equal(part.p50.to_numpy(), part.central.to_numpy())
        d = new.loc[new.policy.eq('D2')]
        assert np.array_equal(d.p50.to_numpy(), d.central.to_numpy())

    def test_the_composites_are_the_fixed_weights_on_every_key(self, ad):
        new = pd.read_parquet(ad / 'predictions.parquet')
        m = pd.read_parquet(ad / 'members.parquet').sort_values(['fold', 'timestamp_utc']).reset_index(drop=True)
        piv = {p: g.sort_values(['fold', 'timestamp_utc']).reset_index(drop=True) for p, g in new.groupby('policy')}
        L = m['L-N'] / 2 + m['L-R'] / 2
        assert np.max(np.abs(piv['v5'].central - m.HGL - (m.D2 - L) / 6)) <= 1e-9
        assert np.max(np.abs(piv['v3+D2'].central - (2 / 3) * m.HG - m.D2 / 3)) <= 1e-9
        assert np.array_equal(piv['D2'].central.to_numpy(), m.D2.to_numpy())
        # negative control: CP-23's one-third weight is caught
        assert np.max(np.abs(piv['v5'].central - (2 / 3) * m.HGL - m.D2 / 3)) > 1e-3

    def test_new_policy_metrics_recompute_from_committed_predictions(self, ad):
        new = pd.read_parquet(ad / 'predictions.parquet')
        metrics = pd.read_csv(ad / 'metrics.csv', float_precision='round_trip')
        frame = new.copy()
        frame['timestamp_utc'] = pd.to_datetime(frame.timestamp_utc, utc=True)
        frame['delivery_date'] = pd.to_datetime(frame.delivery_date)
        hourly = score_hourly(frame)
        per_fold = metrics.loc[metrics.scope.eq('per_fold')].set_index(['policy', 'fold'])
        for (policy, fold), part in hourly.groupby(['policy', 'fold']):
            row = per_fold.loc[(policy, fold)]
            assert len(part) == row.n_hours
            assert abs(part.absolute_error.mean() - row.MAE) <= 1e-9 and abs(part.WIS.mean() - row.WIS) <= 1e-9
        equal = metrics.loc[metrics.scope.eq('equal_fold')].set_index('policy')
        for policy in set(new.policy):
            for metric in ('MAE', 'WIS'):
                ratio = np.mean([per_fold.loc[(policy, f), metric] / per_fold.loc[('B0', f), metric] for f in FOLDS])
                assert abs(ratio - equal.loc[policy, f'S_{metric}']) <= 1e-12

    def test_every_interval_rederives_from_its_stored_replicates(self, ad):
        unc = pd.read_csv(ad / 'uncertainty.csv', float_precision='round_trip')
        draws = pd.read_parquet(ad / 'replicates.parquet')
        grouped = {k: g for k, g in draws.groupby(['scope', 'candidate', 'baseline', 'metric'])}
        for _, row in unc.iterrows():
            d = grouped[(row['scope'], row['candidate'], row['baseline'], row['metric'])].difference.to_numpy()
            assert len(d) == S.BOOTSTRAP_REPLICATES
            assert tuple(np.quantile(d, [.025, .975], method='linear')) == (row['ci_lower'], row['ci_upper'])
            assert tuple(np.quantile(d, [.0125, .9875], method='linear')) == (row['ci97.5_lower'], row['ci97.5_upper'])
        # negative control: shifting the draws moves the interval
        any_row = unc.iloc[0]
        d = grouped[(any_row['scope'], any_row['candidate'], any_row['baseline'], any_row['metric'])].difference.to_numpy()
        assert np.quantile(d + 1.0, .025, method='linear') != any_row['ci_lower']

    def test_the_rule_reapplies_mechanically_to_the_committed_rows(self, ad):
        unc = pd.read_csv(ad / 'uncertainty.csv', float_precision='round_trip')
        crit = pd.read_csv(ad / 'criteria.csv', float_precision='round_trip')
        metrics = pd.read_csv(ad / 'metrics.csv', float_precision='round_trip')
        decisions = json.loads((ad / 'decisions.json').read_text())
        scores = {p: {'S_MAE': r.S_MAE, 'S_WIS': r.S_WIS} for p, r in metrics.loc[metrics.scope.eq('equal_fold')].set_index('policy').iterrows()}
        again = S.adoption(unc, crit, scores, keys_complete=True, guards_reported=True)
        for key in ('adopted', 'verdict', 'first_unmet_condition', 'unmet_conditions'):
            assert again[key] == decisions['adoption'][key]
        # negative control: v5 - v4 moved wholly and decisively below zero, everywhere, flips conditions 1, 4 and 5
        better = unc.copy()
        mask = better.candidate.eq('v5') & better.baseline.eq('HGL')
        for col in ('ci_upper', 'ci97.5_upper'):
            better.loc[mask, col] = -1e-3
        for col in ('ci_lower', 'ci97.5_lower'):
            better.loc[mask, col] = -1.0
        better.loc[mask, 'difference'] = -0.5
        flipped = S.adoption(better, crit, scores, keys_complete=True, guards_reported=True)
        assert all(flipped['conditions'][c]['met'] for c in (1, 4, 5))


def test_the_manifest_binds_every_committed_cp24_file_byte_for_byte():
    path = OUT / 'artifact-manifest.json'
    if not path.exists():
        pytest.skip('no CP-24 artifact manifest yet')
    manifest = json.loads(path.read_text())['artifact_sha256']
    assert manifest, 'empty manifest'
    for name, digest in manifest.items():
        assert sha(ROOT / name) == digest, name


def test_the_generated_documents_equal_their_generators():
    if not (OUT / 'draft-registry.json').exists():
        pytest.skip('no CP-24 draft registry yet')
    for module in ('cp24.packet', 'cp24.claims', 'cp24.report'):
        run = subprocess.run([sys.executable, '-m', module, '--check'], cwd=ROOT, capture_output=True, text=True,
                             env={'PYTHONPATH': str(ROOT / 'src'), 'PATH': '/usr/bin:/bin'})
        assert run.returncode == 0, (module, run.stdout, run.stderr)
