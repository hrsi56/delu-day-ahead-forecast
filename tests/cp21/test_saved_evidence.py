"""CP-21 committed evidence re-derives from committed rows (§17.10 items 5-7 and 10).

These tests never re-run the bootstrap or re-score the seven saved references: each of those is
a capped analysis or reference pass (§17.8), and a test suite runs many times. They recompute the
four new arms' losses from their committed predictions, re-derive every interval from the stored
replicates, and re-apply the mechanical §17.6 rule to the committed rows.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from cp15.scoring import FOLDS, QUANTILES, score_hourly
from cp21 import scoring as S

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'reports/block-challenger'
pytestmark = pytest.mark.skipif(not (OUT / 'adoption.json').exists(), reason='CP-21 results not yet committed')


@pytest.fixture(scope='module')
def new():
    return pd.read_parquet(OUT / 'predictions.parquet')


@pytest.fixture(scope='module')
def metrics():
    return pd.read_csv(OUT / 'metrics.csv', float_precision='round_trip')


@pytest.fixture(scope='module')
def uncertainty():
    return pd.read_csv(OUT / 'uncertainty.csv', float_precision='round_trip')


def test_every_new_arm_issues_all_10747_keys_finite_and_ordered(new):
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


def test_emitted_p50_is_kept_separate_from_the_central_forecast(new):
    assert not np.array_equal(new.p50.to_numpy(), new.central.to_numpy())


def test_new_arm_metrics_recompute_from_committed_predictions(new, metrics):
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
    # S scores: equal-fold ratios to B0's committed per-fold rows
    equal = metrics.loc[metrics.scope.eq('equal_fold')].set_index('policy')
    for policy in S.NEW:
        for metric in ('MAE', 'WIS'):
            ratio = np.mean([per_fold.loc[(policy, f), metric] / per_fold.loc[('B0', f), metric] for f in FOLDS])
            assert abs(ratio - equal.loc[policy, f'S_{metric}']) <= 1e-12


def test_saved_reference_rows_equal_cp20s_committed_metrics(metrics):
    """The seven saved references were scored once, metric-only, and equal CP-20's rows."""
    cp20 = pd.read_csv(ROOT / 'reports/weather-ablation/metrics.csv', float_precision='round_trip')
    for scope in ('per_fold', 'pooled'):
        ours = metrics.loc[metrics.scope.eq(scope) & metrics.policy.isin(S.SAVED)].set_index(['policy', 'fold']).sort_index()
        theirs = cp20.loc[cp20.scope.eq(scope)].set_index(['policy', 'fold']).sort_index()
        for column in ('MAE', 'WIS', 'coverage95', 'n_hours'):
            np.testing.assert_allclose(ours[column].to_numpy(float), theirs[column].to_numpy(float), rtol=0, atol=1e-9)


def test_every_interval_rederives_from_its_stored_replicates(uncertainty):
    draws = pd.read_parquet(OUT / 'replicates.parquet')
    assert set(draws.replicate) == set(range(S.BOOTSTRAP_REPLICATES))
    for row in uncertainty.itertuples():
        d = draws.loc[draws.scope.eq(row.scope) & draws.candidate.eq(row.candidate) & draws.baseline.eq(row.baseline)
                      & draws.metric.eq(row.metric)]
        assert len(d) == S.BOOTSTRAP_REPLICATES
        lo, hi = np.quantile(d.difference, [.025, .975], method='linear')
        assert (lo, hi) == (row.ci_lower, row.ci_upper)  # exact: the CSV holds the shortest round-trip repr
        if row.scope == 'equal_fold':
            rlo, rhi = np.quantile(d.ratio, [.025, .975], method='linear')
            assert (rlo, rhi) == (row.ratio_ci_lower, row.ratio_ci_upper)
    scores = pd.read_parquet(OUT / 'replicate-scores.parquet')
    for c, b in S.CONTRASTS:
        for metric in ('MAE', 'WIS'):
            sc = scores.loc[scores.policy.eq(c) & scores.metric.eq(metric)].S.to_numpy()
            sb = scores.loc[scores.policy.eq(b) & scores.metric.eq(metric)].S.to_numpy()
            d = draws.loc[draws.scope.eq('equal_fold') & draws.candidate.eq(c) & draws.baseline.eq(b) & draws.metric.eq(metric)]
            np.testing.assert_array_equal(d.difference.to_numpy(), sc - sb)
            np.testing.assert_array_equal(d.ratio.to_numpy(), sc / sb - 1)


def test_the_adoption_verdict_reapplies_mechanically_to_the_committed_rows(uncertainty):
    criteria = pd.read_csv(OUT / 'criteria.csv', float_precision='round_trip')
    committed = json.loads((OUT / 'adoption.json').read_text())
    again = S.adoption(uncertainty, criteria, keys_complete=True)
    assert again['verdict'] == committed['verdict']
    assert again['first_unmet_condition'] == committed['first_unmet_condition']
    assert again['unmet_conditions'] == committed['unmet_conditions']
    assert committed['rule']['set_on'] == '2026-09-29' and committed['candidate'] == 'HGL' and committed['comparator'] == 'HG'
    split = S.joint_reading(uncertainty, 'L-R', 'L-P')
    assert split['reading'] == committed['block_split']['reading']


def test_bootstrap_index_set_is_cp20s():
    lineage = json.loads((OUT / 'lineage.json').read_text())
    meta = lineage['research_summary']['bootstrap']
    assert meta['index_sha256'] == S.CP20_INDEX_SHA256 and meta['seed'] == 15042
    assert meta['replicates'] == 2000 and meta['block_days'] == 7


#: CP-21 files that the later, authorized publication block amended (PRES-3, 2026-09-30): the export gained CP-21's
#: specification (publication runbook §2 step 17), the draft-export test its post-publication invariant, and this test
#: this exemption. Their reviewed bytes stay at `evidence/cp-21`, which the manifest still describes exactly; every
#: other hash-bound file is checked byte for byte, as before.
AMENDED_BY_PUBLICATION = frozenset({'scripts/mlflow_export.py', 'tests/cp21/test_draft_export.py',
                                    'tests/cp21/test_saved_evidence.py'})


#: Owner-authorized work-availability amendment, 2026-10-10. Check these historical bytes
#: at the reviewed evidence tag; current monitor behaviour is tested in test_work_availability.
AMENDED_BY_WORK_AVAILABILITY = frozenset({
    'scripts/cp21_blocks.py', 'src/cp21/budget.py', 'src/cp21/protocol.py',
    'tests/cp21/test_guards.py',
})


def test_hash_bound_files_are_stored_byte_for_byte():
    manifest = json.loads((OUT / 'artifact-manifest.json').read_text())['artifact_sha256']
    assert (AMENDED_BY_PUBLICATION | AMENDED_BY_WORK_AVAILABILITY) <= set(manifest)
    for name, digest in manifest.items():
        if name in AMENDED_BY_PUBLICATION | AMENDED_BY_WORK_AVAILABILITY:
            continue
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
    protocol = json.loads((OUT / 'protocol.json').read_text())
    for name, digest in protocol['preflight_sha256'].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
    brief = ROOT / 'docs/track-b/evidence/cp-21/issued-brief.md'
    assert hashlib.sha256(brief.read_bytes()).hexdigest() == '813fb8a476a7b6d10ecf0a5519e97ec8efc4ff36e0f13868676ad34534fc020f'


def test_hg_parity_and_controls_passed():
    parity = json.loads((OUT / 'hg-parity.json').read_text())
    assert parity['bitwise_equal'] and parity['rows'] == 10747 and parity['keys_equal']
    controls = json.loads((OUT / 'controls.json').read_text())
    assert controls['all_passed']
    daily = json.loads((OUT / 'daily-cycle.json').read_text())
    assert daily['all_bitwise_checks_passed'] and daily['origins'] >= 20


def test_amended_files_keep_their_reviewed_bytes_at_the_evidence_tag():
    """The exemption hides nothing: the tag still holds the bytes the manifest bound (a shallow clone without the tag,
    as in CI, cannot check this and skips)."""
    import subprocess
    manifest = json.loads((OUT / 'artifact-manifest.json').read_text())['artifact_sha256']
    tag = subprocess.run(['git', 'rev-parse', '--verify', '--quiet', 'evidence/cp-21^{commit}'], cwd=ROOT,
                         capture_output=True, text=True)
    if tag.returncode != 0:
        pytest.skip('evidence/cp-21 is not in this checkout')
    for name in sorted(AMENDED_BY_PUBLICATION | AMENDED_BY_WORK_AVAILABILITY):
        data = subprocess.run(['git', 'show', f'evidence/cp-21:{name}'], cwd=ROOT, capture_output=True, check=True).stdout
        assert hashlib.sha256(data).hexdigest() == manifest[name], name
