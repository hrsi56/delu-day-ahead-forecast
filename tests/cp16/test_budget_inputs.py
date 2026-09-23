"""Refusal controls for CP-16's inherited identity and persistent ceilings."""
from pathlib import Path
import json
import pytest
from cp16.budget import Budget, CAPS
from cp16.inputs import identities

ROOT=Path(__file__).resolve().parents[2]


def test_inherited_identity_positive_and_wrong_input_refusal(monkeypatch):
    import cp16.inputs as module
    p, hashes=identities(ROOT)
    assert p['seed']==42 and hashes['data/snapshot.parquet']
    original=module.sha
    monkeypatch.setattr(module,'sha',lambda path:'0'*64 if str(path).endswith('src/cp15/models.py') else original(path))
    with pytest.raises(ValueError,match='saved artifact identity'):identities(ROOT)


def test_persistent_budget_refuses_attempt_before_it_runs(tmp_path):
    path=tmp_path/'budget.json';b=Budget(path)
    b.reserve(component_attempts=CAPS['component_attempts']-1)
    resumed=Budget(path);resumed.reserve(component_attempts=1)
    with pytest.raises(RuntimeError,match='hard cap'):resumed.reserve(component_attempts=1)
    assert resumed.read()['counts']['component_attempts']==CAPS['component_attempts']


def test_budget_multi_counter_transaction_is_atomic(tmp_path):
    b=Budget(tmp_path/'budget.json');b.reserve(inner_fits=CAPS['inner_fits'])
    with pytest.raises(RuntimeError):b.reserve(primitive_fits=1,inner_fits=1)
    assert b.read()['counts'].get('primitive_fits',0)==0
    b.reserve(primitive_fits=1,final_fits=1)
    assert b.read()['counts']['primitive_fits']==1


def test_budget_refuses_contract_replacement(tmp_path):
    path=tmp_path/'budget.json';b=Budget(path);b.reserve(policy_days=2)
    state=b.read();state['caps']['policy_days']+=1;path.write_text(json.dumps(state))
    with pytest.raises(ValueError,match='contract changed'):Budget(path).reserve(policy_days=1)
