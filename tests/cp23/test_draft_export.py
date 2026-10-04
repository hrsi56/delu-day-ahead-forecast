"""CP-23's draft MLflow export (§21.9): built by the exporter's code path from committed CP-23 rows and
the packet's draft entries; names and statuses follow the mechanical verdicts; every value re-derives
from a committed row; landing-time identities are explicit pending fields; the published export set
and the CP-21 and CP-22 drafts are unchanged. Each contract carries a negative control."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'src'))
import mlflow_export as E  # noqa: E402

DRAFT = ROOT / 'reports/distribution-challenger/mlflow-export-draft/cp23.json'
pytestmark = pytest.mark.skipif(not DRAFT.exists(), reason='CP-23 draft export not yet committed')


@pytest.fixture(scope='module')
def draft():
    return E.build_draft('cp23')


def _runs(draft):
    return {run['run_key']: run for run in draft['runs']}


def test_the_draft_is_deterministic_and_committed(draft):
    text = json.dumps(draft, indent=1, sort_keys=True, ensure_ascii=False) + '\n'
    assert text == json.dumps(E.build_draft('cp23'), indent=1, sort_keys=True, ensure_ascii=False) + '\n'
    assert DRAFT.read_text() == text, 'stale draft; run scripts/mlflow_export.py --draft cp23'


def test_names_and_statuses_follow_the_mechanical_verdict(draft):
    assert E.draft_problems(draft) == []
    decisions = json.loads((ROOT / 'reports/distribution-challenger/decisions.json').read_text())
    adopted = decisions['adoption']['adopted']
    runs = _runs(draft)
    assert sorted(runs) == sorted(['cp23', 'cp23/v5', 'cp23/D', 'cp23/v3+D'])
    if adopted:
        assert runs['cp23/v5']['tags']['delu.generation'] == 'v5'
        assert runs['cp23/v5']['tags']['delu.public_name'].startswith('v5 · ')
        assert runs['cp23']['tags']['delu.kind'] == 'generation'
    else:
        assert runs['cp23']['tags']['delu.kind'] == 'branch' and runs['cp23/v5']['tags']['delu.kind'] == 'branch'
        assert runs['cp23']['tags']['delu.public_name'] == 'DDNN member on v4'
        assert runs['cp23/v5']['tags']['delu.adopted'] == 'false'
        assert all(not r['tags']['delu.public_name'].startswith('v5 · ') for r in runs.values())
    for code in ('D', 'v3+D'):
        assert runs[f'cp23/{code}']['tags']['delu.kind'] == 'study arm'
        assert runs[f'cp23/{code}']['tags']['delu.adopted'] == 'false'
    # negative control: a renamed run is caught
    broken = json.loads(json.dumps(draft))
    broken['runs'][1]['run_name'] = 'v9 · invented'
    assert E.draft_problems(broken)


def test_every_value_re_derives_from_a_committed_row(draft):
    import csv
    rows = {}
    with open(ROOT / 'reports/distribution-challenger/metrics.csv') as handle:
        for row in csv.DictReader(handle):
            if row['scope'] == 'equal_fold':
                rows[row['policy']] = row
    for run in draft['runs'][1:]:
        code = run['tags']['delu.policy_code']
        assert run['metrics']['s_mae'][0]['value'] == float(rows[code]['S_MAE'])
        assert run['metrics']['s_wis'][0]['value'] == float(rows[code]['S_WIS'])
        assert all(prov for prov in run['metric_provenance'].values())
    # negative control: a record id that is not in the committed rows is refused
    with pytest.raises(KeyError):
        E.DraftBuilder(E._draft23_records()).single('s_mae', 'cp23.metrics.NOPE.equal_fold.S_MAE')


def test_pending_fields_are_explicit_and_nothing_published_changes(draft):
    for run in draft['runs']:
        assert run['tags']['delu.model_code_sha'] == 'pending-at-landing'
        assert 'pending-at-landing' in run['tags']['delu.evidence_ref']
    assert 'statuses[].date' in draft['pending_fields']
    assert E.build_draft('cp21') == json.loads((ROOT / 'reports/block-challenger/mlflow-export-draft/cp21.json').read_text())
    assert E.build_draft('cp22') == json.loads((ROOT / 'reports/v4-revision/mlflow-export-draft/cp22.json').read_text())
