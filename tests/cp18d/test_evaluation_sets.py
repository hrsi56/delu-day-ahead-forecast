"""The evaluation keeps the two input classes apart (the Owner's decision 31, CP-18d; O32, O33): the prospective
record's days with every input before the cutoff on their own, all issued days beside them, each with its count; the
browser's recomputation (`cp18.spaceglue.recompute`) selects the same days; the running intervals are per set.

A synthetic served bundle (CP-18b's `test_controls._synthetic` shape) on live days. No network, no Pyodide.
"""
from __future__ import annotations

from datetime import date, timedelta
import json

from cp17.issue import canonical_hours
from cp18 import evaluation as EV, inputclass, outcomes as OC, running, spaceglue as G

DAYS = [date(2026, 11, 3) + timedelta(days=i) for i in range(6)]
AFTER = {date(2026, 11, 5), date(2026, 11, 8)}


def synthetic() -> dict[str, bytes]:
    forecasts = {'schema': 'cp17b-issued-forecasts-v2', 'levels': [0.025, 0.1, 0.25, 0.5, 0.75, 0.9, 0.975], 'days': []}
    view = {}
    for i, d in enumerate(DAYS):
        keys = canonical_hours(d)
        q = [[10.0 * k + j * 3 + i for j in range(7)] for k in range(len(keys))]
        label = (inputclass.label(inputclass.AFTER, f'{d - timedelta(days=1)}T11:00:00Z') if d in AFTER
                 else inputclass.label(inputclass.BEFORE))
        forecasts['days'].append({'delivery_day': str(d), 'issue_utc': '', 'issuing_artifact_sha256': '0' * 64,
                                  'issued_policy': 'A1', 'display': '', 'keys': keys, 'quantiles': q, 'partial': None,
                                  **label})
        view[str(d)] = {'status': 'final', 'keys': keys, 'prices': [10.0 * k + 8 for k in range(len(keys))],
                        'revised_utc': [''] * len(keys), 'first': {'published_utc': ''}}
    out = OC.bundle_outcomes(DAYS, view)
    ev = EV.evaluation_bundle([], EV.daily_windows(forecasts, out, [], sets=True))
    return {'issued-forecasts.json': json.dumps(forecasts).encode(), 'outcomes.json': json.dumps(out).encode(),
            'evaluation.json': json.dumps(ev).encode()}


def test_the_prospective_record_is_reported_whole_and_without_the_days_fetched_after_the_cutoff():
    windows = json.loads(synthetic()['evaluation.json'])['windows']
    prospective = [w for w in windows if w['window'] == 'prospective']
    whole = next(w for w in prospective if w['policy'] == 'product' and w['subset'] == 'all')
    before = next(w for w in prospective if w['policy'] == 'product' and w['subset'] == EV.SUBSET_BEFORE)
    assert whole['issued_days'] == 6 and before['issued_days'] == 4
    assert [d['day'] for d in whole['record']['days']] == [str(d) for d in DAYS]
    assert [d['day'] for d in before['record']['days']] == [str(d) for d in DAYS if d not in AFTER]
    assert before['evidence_class'].endswith('issued days with every input before the cutoff')
    assert 'late' not in json.dumps([w['evidence_class'] for w in windows]).lower()


def test_the_browsers_recomputation_selects_the_same_days_for_each_set():
    check = G.recompute(synthetic())
    assert check['match'] and not check['blocks_publication'] and check['recomputed_windows'] == 8
    rows = [r for r in check['rows'] if r['window'] == 'prospective' and r['policy'] == 'product']
    assert [len(r['days']) for r in rows] == [6, 4]


def test_a_development_bundle_of_cp18b_records_keeps_cp18bs_windows():
    files = synthetic()
    forecasts, out = json.loads(files['issued-forecasts.json']), json.loads(files['outcomes.json'])
    assert not any('subset' in w for w in EV.daily_windows(forecasts, out, []))


def test_the_running_intervals_are_per_set_with_their_counts():
    windows = json.loads(synthetic()['evaluation.json'])['windows']
    r = running.running(windows, replicates=50)
    sets = {s['set']: s for s in r['sets']}
    assert [s['set'] for s in r['sets']] == ['before_cutoff', 'all']
    assert sets['all']['issued_days'] == 6 and sets['all']['scored_days'] == 6
    assert sets['before_cutoff']['issued_days'] == 4 and sets['before_cutoff']['scored_days'] == 4
    assert r['series'] == sets['all']['series'] and len(sets['before_cutoff']['series']['mae']) == 4
    assert sets['before_cutoff']['series']['mae'][-1]['mean'] != sets['all']['series']['mae'][-1]['mean']
