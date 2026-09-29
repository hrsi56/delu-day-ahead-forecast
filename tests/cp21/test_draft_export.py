"""CP-21's draft MLflow export (§17.9): built by the exporter's code path from committed CP-21 rows
and the packet's draft entries; names and statuses follow the mechanical verdict; every value
re-derives from a committed row; landing-time identities are explicit pending fields; the
published export set is untouched. Each contract carries a negative control."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import mlflow_export as E  # noqa: E402

DRAFT = ROOT / 'reports/block-challenger/mlflow-export-draft/cp21.json'
pytestmark = pytest.mark.skipif(not DRAFT.exists(), reason='CP-21 draft export not yet committed')


@pytest.fixture(scope='module')
def draft():
    return E.build_draft('cp21')


def _runs(draft):
    return {run['run_key']: run for run in draft['runs']}


def test_the_draft_is_deterministic_and_committed(draft):
    text = json.dumps(draft, indent=1, sort_keys=True, ensure_ascii=False) + '\n'
    assert text == json.dumps(E.build_draft('cp21'), indent=1, sort_keys=True, ensure_ascii=False) + '\n'
    assert DRAFT.read_text() == text, 'stale draft; run scripts/mlflow_export.py --draft cp21'


def test_the_draft_matches_its_draft_entries_and_the_mechanical_verdict(draft):
    assert E.draft_problems(draft) == []
    spec, entries, checkpoint = E.draft_registry()
    adoption = json.loads((ROOT / 'reports/block-challenger/adoption.json').read_text())
    adopted = adoption['verdict'] == 'v4'
    runs = _runs(draft)
    assert sorted(runs) == ['cp21', 'cp21/HGL', 'cp21/L-N', 'cp21/L-P', 'cp21/L-R']
    hgl = runs['cp21/HGL']['tags']
    assert hgl['delu.kind'] == ('generation' if adopted else 'study arm')
    assert hgl['delu.generation'] == ('v4' if adopted else 'none')
    assert hgl['delu.adopted'] == ('true' if adopted else 'false')
    assert runs['cp21']['tags']['delu.kind'] == ('generation' if adopted else 'branch')
    if not adopted:
        assert runs['cp21']['tags']['delu.public_name'] == 'Three-block LightGBM on v3'
        assert all(not r['tags']['delu.public_name'].startswith('v4') for r in runs.values())
    for code in ('L-P', 'L-R', 'L-N'):
        assert runs[f'cp21/{code}']['tags']['delu.kind'] == 'study arm'
        assert runs[f'cp21/{code}']['tags']['delu.adopted'] == 'false'
    for run in runs.values():
        if run['parent']:
            assert run['tags']['delu.comparator'] == 'v3 · weather features'
    # negative control: a renamed run is caught
    broken = json.loads(json.dumps(draft))
    broken['runs'][1]['run_name'] = 'v9 · invented'
    assert E.draft_problems(broken)


def test_every_value_rederives_from_a_committed_row(draft):
    runs = _runs(draft)
    metrics = pd.read_csv(ROOT / 'reports/block-challenger/metrics.csv', float_precision='round_trip')
    uncertainty = pd.read_csv(ROOT / 'reports/block-challenger/uncertainty.csv', float_precision='round_trip')
    equal = metrics.loc[metrics.scope.eq('equal_fold')].set_index('policy')
    per_fold = metrics.loc[metrics.scope.eq('per_fold')].set_index(['policy', 'fold'])
    unc = uncertainty.set_index(['scope', 'candidate', 'baseline', 'metric'])
    for code in ('HGL', 'L-P', 'L-R', 'L-N'):
        m = runs[f'cp21/{code}']['metrics']
        assert m['s_mae'][0]['value'] == equal.loc[code, 'S_MAE'] and m['s_wis'][0]['value'] == equal.loc[code, 'S_WIS']
        assert [p['value'] for p in m['fold_mae_eur']] == [per_fold.loc[(code, f), 'MAE'] for f in E.FOLDS]
        for candidate, base, slug in E.DRAFT_CONTRASTS[f'cp21/{code}']:
            for metric, score in (('MAE', 'mae'), ('WIS', 'wis')):
                row = unc.loc[('equal_fold', candidate, base, metric)]
                assert m[f'delta_s_{score}_vs_{slug}'][0]['value'] == row.difference
                assert m[f'delta_s_{score}_vs_{slug}_ci_high'][0]['value'] == row.ci_upper
                assert m[f'ratio_s_{score}_vs_{slug}'][0]['value'] == row.ratio
                assert m[f'ratio_s_{score}_vs_{slug}_ci_low'][0]['value'] == row.ratio_ci_lower
                folds = [unc.loc[(f, candidate, base, metric)].ci_lower for f in E.FOLDS]
                assert [p['value'] for p in m[f'delta_fold_{score}_eur_vs_{slug}_ci_low']] == folds
        assert all(len(points) for points in m.values())
        assert set(runs[f'cp21/{code}']['metric_units']) == set(m)


def test_a_changed_committed_row_changes_the_draft(monkeypatch, draft):
    real = E.R._rows

    def altered(path):
        rows = real(path)
        if path == E.CP21['metrics']:
            rows = [(line, {**row, 'S_MAE': '0.1'} if row['scope'] == 'equal_fold' and row['policy'] == 'HGL' else row)
                    for line, row in rows]
        return rows
    monkeypatch.setattr(E.R, '_rows', altered)
    rebuilt = _runs(E.build_draft('cp21'))
    assert rebuilt['cp21/HGL']['metrics']['s_mae'][0]['value'] == 0.1 != _runs(draft)['cp21/HGL']['metrics']['s_mae'][0]['value']


def test_landing_time_identities_are_explicit_pending_fields(draft):
    spec, _, _ = E.draft_registry()
    assert set(spec['pending_fields']) >= {'statuses[].date', 'checkpoint.evidence_sha', 'checkpoint.landing', 'model_code_sha'}
    assert draft['pending_fields'] == spec['pending_fields'] and draft['status'] == 'draft'
    for run in draft['runs']:
        assert run['tags']['delu.model_code_sha'] == spec['pending']
        assert spec['pending'] in run['tags']['delu.evidence_ref'] and spec['pending'] in run['tags']['delu.status']


def test_the_published_export_set_is_unchanged(draft):
    files = E.build_export()
    assert E.contract_problems(files) == []
    for name, text in E.render(files).items():
        assert (E.EXPORT_DIR / name).read_text() == text
    assert 'cp21' not in files and not any(r['run_key'].startswith('cp21') for r in files['manifest']['runs'])
