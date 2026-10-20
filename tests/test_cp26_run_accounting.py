"""Scientific-run views retain historical and unrelated cumulative spending."""
from cp26.budget import Budget, add_seconds, scientific_run_summary


def test_run_view_counts_each_receipt_once_and_excludes_history_and_other_work():
    state = {'counts': {}, 'accounting': {'measured_seconds': 100.,
        'reported_seconds': 10., 'reserved_seconds': 2826.},
        'scientific_runs': {'cold': {'cumulative_baseline': {'machine_hours': 2936 / 3600}}},
        'jobs': [{'run_id': 'cold', 'charged_wall_seconds': 12., 'workers': 3},
                 {'run_id': 'other', 'charged_wall_seconds': 5., 'workers': 1}],
        'charges': [{'kind': 'reported', 'seconds': 2., 'source': {'run_id': 'cold'}},
                    {'kind': 'reserved', 'seconds': 2826., 'source': {}}]}
    add_seconds(state, 43.)
    first = scientific_run_summary(state, 'cold')
    assert first['measured_seconds'] == 36.
    assert first['reported_seconds'] == 2.
    assert first['reserved_seconds'] == 0.
    assert first['total_seconds'] == 38.
    assert first['cumulative_machine_hours'] == 2979 / 3600
    assert scientific_run_summary(state, 'cold') == first
    assert state['accounting']['reserved_seconds'] == 2826.


def test_registered_run_starts_at_zero_even_with_historical_spending():
    state = {'counts': {}, 'accounting': {'measured_seconds': 99.,
        'reported_seconds': 7., 'reserved_seconds': 2826.},
        'scientific_runs': {'cold': {'cumulative_baseline': {'machine_hours': 2932 / 3600}}}}
    result = scientific_run_summary(state, 'cold')
    assert result['total_seconds'] == 0.
    assert result['machine_hours'] == 0.
    assert result['historical_baseline_hours'] == 2932 / 3600


def test_resource_view_retains_attributed_maintenance_receipts(tmp_path):
    budget = Budget(tmp_path / 'budget.json')
    budget.initialise()
    with budget.transaction() as state:
        state['scientific_runs'] = {'cold': {'cumulative_baseline': {'machine_hours': 0.0}}}
    budget.record_charge('setup', 2.0, 'measured', {'run_id': 'cold'})
    budget.record_charge('reported', 3.0, 'reported', {'run_id': 'cold'})
    full = scientific_run_summary(budget.read(), 'cold')
    hot = scientific_run_summary(budget.resource_read(), 'cold')
    assert full == hot
    assert hot['measured_seconds'] == 2.0
    assert hot['reported_seconds'] == 3.0
