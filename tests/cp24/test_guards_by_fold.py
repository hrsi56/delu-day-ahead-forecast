"""The per-fold guard diagnostic (§23.8, as S1 asked): synthetic member records, DST days included.

Each key takes its local-hour slot's cap flags, so a 23-hour day emits 23 x 7 hour-levels per member and
a 25-hour day 25 x 7, with the repeated hour counted twice; the per-fold totals must equal the scoring
job's `guard_report`, which reads the same records.
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd
import pytest

from cp24.diagnostics import guards_by_fold
from cp24.evaluate import guard_report


def _day_utc(day: str) -> list[str]:
    start = pd.Timestamp(day, tz='Europe/Berlin')
    end = start + pd.DateOffset(days=1)
    return [str(t) for t in pd.date_range(start, end, freq='h', inclusive='left').tz_convert('UTC')]


def _member(j: int, active: np.ndarray, nonfinite: bool = False) -> dict:
    zero = {'winsor_low': 0, 'winsor_high': 0}
    return {'member': j, 'rank': j // 2 + 1, 'config': f't{j // 2:03d}', 'seed': 100 + j, 'active': active.tolist(),
            'guards': {'winsor_train': {'winsor_low': 2, 'winsor_high': 1}, 'winsor_hold': zero,
                       'winsor_forecast': {'winsor_low': 0, 'winsor_high': j % 2}, 'cap_forecast_slot_levels': int(active.sum()),
                       'events': [{'event': 'nonfinite_training_loss'}] if nonfinite else []}}


def _write(base, fold, day, stage, members, crossed=0):
    path = base / fold / f'{day}.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({'fold': fold, 'day': day, 'stage': stage, 'timestamp_utc': _day_utc(day),
                                'crossed_rows': crossed, 'members': members}))


@pytest.fixture()
def attempt(tmp_path, monkeypatch):
    monkeypatch.setenv('CP24_PROJECT_ROOT', str(tmp_path))
    fits = tmp_path / '.local' / 'artifacts' / 'cp-24' / 'attempt-1' / 'fits'
    quiet = np.zeros((24, 7), int)
    spring = quiet.copy()
    spring[2, :] = 1          # slot 2 does not exist on 2020-03-29 (23 hours): emitted nothing
    spring[5, 6] = 1          # one capped level at 05:00
    autumn = quiet.copy()
    autumn[2, 0] = 1          # slot 2 occurs twice on 2020-10-25 (25 hours): two capped hour-levels
    _write(fits, 'fold_1', '2020-03-29', 'warmup', [_member(0, spring)] + [_member(j, quiet) for j in range(1, 8)], crossed=1)
    _write(fits, 'fold_1', '2020-10-25', 'evaluation', [_member(0, quiet), _member(1, autumn, nonfinite=True)]
           + [_member(j, quiet) for j in range(2, 8)])
    _write(fits, 'fold_2', '2021-03-01', 'evaluation', [_member(j, quiet) for j in range(8)])
    protocol = tmp_path / 'reports' / 'ddnn2' / 'attempt-1' / 'protocol.json'
    protocol.parent.mkdir(parents=True)
    protocol.write_text(json.dumps({'folds': {'fold_1': {'gate': {'cap_share': 0.0033}}, 'fold_2': {'gate': {'cap_share': 0.0001}}},
                                    'gate': {'conditions': {'G3': {'share': 0.00088}}}}))
    return tmp_path


def test_per_fold_shares_follow_the_keys_slots(attempt):
    guards = guard_report(attempt, 1)
    table, members = guards_by_fold(attempt, 1, guards)
    t = table.set_index(['scope', 'stage'])
    warm = t.loc[('fold_1', 'warmup')]
    assert warm.emitted_hour_levels == 8 * 23 * 7 and warm.cap_hour_levels == 1          # slot 2 absent on the spring day
    assert warm.cap_slot_levels_forecast == 8                                            # the raw slot count keeps it
    ev = t.loc[('fold_1', 'evaluation')]
    assert ev.emitted_hour_levels == 8 * 25 * 7 and ev.cap_hour_levels == 2              # the repeated hour counts twice
    assert ev.nonfinite_loss_stops == 1 and ev.member_fits_with_cap == 1
    allf = t.loc[('fold_1', 'all')]
    assert allf.cap_hour_levels == 3 and allf.member_fits == 16 and allf.ensemble_crossings_restored == 1
    assert allf.cap_share == pytest.approx(3 / (8 * 23 * 7 + 8 * 25 * 7))
    assert allf.largest_member_fit_share_of_capped == pytest.approx(2 / 3)
    assert allf.gate_cap_share_round == pytest.approx(0.0033)
    pooled = t.loc[('pooled', 'all')]
    assert pooled.member_fits == 24 and pooled.cap_hour_levels == 3 and pooled.gate_cap_share_round == pytest.approx(0.00088)
    assert np.isnan(t.loc[('fold_2', 'all')].largest_member_fit_share_of_capped)
    m = members.set_index(['fold', 'member'])
    assert m.loc[('fold_1', 1)].cap_hour_levels == 2 and m.loc[('fold_1', 1)].share_of_fold_capped == pytest.approx(2 / 3)
    assert m.loc[('fold_1', 0)].member_fits == 2


def test_disagreement_with_the_scoring_report_fails(attempt):
    guards = guard_report(attempt, 1)
    guards['by_fold']['fold_1']['winsor_values_forecast'] += 1
    with pytest.raises(ValueError, match='differ from guards.json'):
        guards_by_fold(attempt, 1, guards)
