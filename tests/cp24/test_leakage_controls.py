"""The committed future-blind leakage controls of scored attempt 1 (§23.13 item 9; §23.10 at full coverage).

`src/cp24/leakage.py` refitted the frozen ensemble at every one of the 636 origins after destroying every outcome
dated on or after the delivery day. It also ran paired positives in every fold, the search and gate controls fold
by fold, and exhaustive structural checks. This test never refits, because each refit is a capped control fit
(§23.11). It re-derives the committed summary from the committed per-origin rows and checks that every positive
moved and every fold is covered. Each aggregate is paired with a negative that flips it. It reads only CP-24's
own files, and is skipped until they are committed.
"""
import json
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
AD = ROOT / 'reports/ddnn2/attempt-1'
SUMMARY = AD / 'leakage-controls.json'
ROWS = AD / 'leakage-by-origin.csv'
FOLDS = [f'fold_{i}' for i in range(1, 6)]
BITWISE = ['quantiles_bitwise', 'central_bitwise', 'members_params_bitwise', 'members_best_epoch_equal', 'timestamps_equal']

pytestmark = pytest.mark.skipif(not SUMMARY.exists(), reason='no committed CP-24 leakage controls yet')


def _all_bitwise(rows: pd.DataFrame) -> bool:
    return bool(rows[BITWISE].to_numpy(bool).all() and rows.error.isna().all() and (rows.max_abs_difference == 0).all())


def test_every_origin_is_bitwise_with_the_future_destroyed():
    s = json.loads(SUMMARY.read_text())
    rows = pd.read_csv(ROWS, float_precision='round_trip')
    assert len(rows) == 636 and len(rows[['fold', 'day']].drop_duplicates()) == 636
    assert rows.stage.value_counts().to_dict() == {'evaluation': 448, 'warmup': 188}
    assert _all_bitwise(rows)
    assert s['blind']['origins'] == s['blind']['bitwise'] == 636
    assert s['blind']['committed_predictions'] == {'evaluation_days_in_predictions': 448, 'days_equal_bitwise': 448,
                                                   'keys_compared': 10747}
    # the rows are exactly the scored attempt's DDNN-2 origins
    fits = pd.read_parquet(AD / 'fits.parquet', columns=['fold', 'phase', 'delivery_date'])
    committed = {(f, str(pd.Timestamp(d).date()), 'warmup' if p == 'warmup' else 'evaluation')
                 for f, p, d in fits.drop_duplicates().itertuples(index=False)}
    assert set(zip(rows.fold, rows.day, rows.stage)) == committed
    # negative control: a single origin that differed would fail the aggregate
    bad = rows.copy()
    bad.loc[bad.index[-1], 'members_params_bitwise'] = False
    assert not _all_bitwise(bad)


def test_every_positive_moved_in_every_fold_and_the_search_and_gate_hold_fold_by_fold():
    s = json.loads(SUMMARY.read_text())
    t = s['threshold_eur_mwh']
    d1, plant = s['positives']['d1_evening_prices'], s['positives']['planted_one_day_leak']
    assert {r['fold'] for r in d1} == {r['fold'] for r in plant} == set(FOLDS)
    assert all(r['error'] is None and r['rows_mutated'] > 0 and r['max_abs_difference'] > t for r in d1)
    assert all(r['error'] is None and r['leaky_window_contains_d'] and r['leak_detected_max_abs_difference'] > t
               for r in plant)
    sg = s['search_and_gate_by_fold']
    assert sorted(sg) == FOLDS
    for v in sg.values():
        search, gate = v['search'], v['gate']
        assert search['negative_identical'] and search['pinball_sum_with_outcomes_from_cutoff_mutated'] == search['pinball_sum_ledger']
        assert search['positive_changed'] and search['pinball_sum_with_a_validation_day_mutated'] != search['pinball_sum_ledger']
        assert search['batch_end'] < search['cutoff']
        assert gate['negative_identical'] and gate['negative_max_abs_difference'] == 0.0
        assert gate['positive_max_abs_difference'] > t
    st = s['structure']
    assert st['entries_checked'] == 636 and st['members_checked'] == 5088 and st['window_problems'] == []
    assert st['search_batches_checked'] == 3464 and st['search_batch_problems'] == [] and st['gate_problems'] == []
    assert s['all_passed'] and all(s['checks'].values()) and len(s['checks']) == 12
    # negative control: a positive that did not move fails its check
    assert not all(r['max_abs_difference'] > t for r in [*d1, {'max_abs_difference': 0.0}])


def test_the_frozen_code_guard_names_only_the_owners_maintenance():
    guard = json.loads(SUMMARY.read_text())['frozen_guard']
    protocol = json.loads((AD / 'protocol.json').read_text())
    assert guard['protocol_commit'] == '62b8e51f483f2c35dad3dc6273ea60f021d97365'
    assert guard['implementation_files'] == len(protocol['implementation_sha256'])
    assert guard['frozen_inputs'] == len(protocol['frozen_inputs_sha256'])
    exceptions = guard['maintenance_exceptions']
    assert sorted(exceptions) == ['scripts/cp24_ddnn2.py', 'src/cp24/budget.py']
    for name, e in exceptions.items():
        assert e['maintenance_commit'] == '9667fb4698076fe942aae2246e44366e91efd388'
        assert e['frozen_sha256'] == protocol['implementation_sha256'][name] != e['maintenance_sha256']
