"""The evaluation keeps the two input classes apart (the Owner's decision 31, CP-18d; O32, O33): the prospective
record's days with every input before the cutoff on their own, all issued days beside them, each with its count
(`cp18.evaluation.class_sets`, `cp18.running.running(..., classes=)`), computed at the Space's build from the served
bundle and the live store's classes. The bundle itself keeps the frozen schema: a store holding a day issued with the
load forecast fetched after the cutoff still gives a bundle `cp17.schema.verify_bundle` accepts (the scratch
rehearsal's finding, run 43670023047: labels written into the bundle's files were refused).
"""
from __future__ import annotations

from datetime import date, timedelta
import json
from pathlib import Path

import pytest

from cp17.issue import canonical_hours
from cp18 import evaluation as EV, inputclass, outcomes as OC, running, spaceglue as G

from cp18b.support18b import build, live  # noqa: F401 - `live` is CP-18b's fixture

DAYS = [date(2026, 11, 3) + timedelta(days=i) for i in range(6)]
AFTER = {date(2026, 11, 5), date(2026, 11, 8)}
CLASSES = {str(d): (inputclass.AFTER if d in AFTER else inputclass.BEFORE) for d in DAYS}


def synthetic() -> dict[str, bytes]:
    forecasts = {'schema': 'cp17b-issued-forecasts-v2', 'levels': [0.025, 0.1, 0.25, 0.5, 0.75, 0.9, 0.975], 'days': []}
    view = {}
    for i, d in enumerate(DAYS):
        keys = canonical_hours(d)
        q = [[10.0 * k + j * 3 + i for j in range(7)] for k in range(len(keys))]
        forecasts['days'].append({'delivery_day': str(d), 'issue_utc': '', 'issuing_artifact_sha256': '0' * 64,
                                  'issued_policy': 'A1', 'display': '', 'keys': keys, 'quantiles': q, 'partial': None})
        view[str(d)] = {'status': 'final', 'keys': keys, 'prices': [10.0 * k + 8 for k in range(len(keys))],
                        'revised_utc': [''] * len(keys), 'first': {'published_utc': ''}}
    out = OC.bundle_outcomes(DAYS, view)
    ev = EV.evaluation_bundle([], EV.daily_windows(forecasts, out, []))
    return {'issued-forecasts.json': json.dumps(forecasts).encode(), 'outcomes.json': json.dumps(out).encode(),
            'evaluation.json': json.dumps(ev).encode()}


def test_the_bundle_windows_keep_the_frozen_schema():
    windows = json.loads(synthetic()['evaluation.json'])['windows']
    assert len(windows) == 6 and not any(set(w) - {'window', 'evidence_class', 'policy', 'record'} for w in windows)
    forecasts = json.loads(synthetic()['issued-forecasts.json'])
    assert not any(set(d) & set(inputclass.FIELDS) for d in forecasts['days'])


def test_the_prospective_record_per_class_with_its_counts():
    value = EV.class_sets(synthetic(), CLASSES)
    sets = {s['set']: s for s in value['sets']}
    assert [s['set'] for s in value['sets']] == ['before_cutoff', 'all']
    assert sets['all']['issued_days'] == 6 and sets['before_cutoff']['issued_days'] == 4
    assert sets['before_cutoff']['days'] == [str(d) for d in DAYS if d not in AFTER]
    product = {s: next(w for w in sets[s]['windows'] if w['policy'] == 'product')['record'] for s in sets}
    assert [d['day'] for d in product['before_cutoff']['days']] == sets['before_cutoff']['days']
    assert product['before_cutoff']['pooled']['mae_eur'] != product['all']['pooled']['mae_eur']
    assert sets['before_cutoff']['evidence_class'].endswith('issued days with every input before the cutoff')
    assert 'late' not in json.dumps(value).lower()


def test_negative_control_an_issued_day_without_its_class_is_refused():
    with pytest.raises(ValueError, match='without an input class'):
        EV.class_sets(synthetic(), {k: v for k, v in CLASSES.items() if k != '2026-11-05'})
    windows = json.loads(synthetic()['evaluation.json'])['windows']
    with pytest.raises(ValueError, match='without an input class'):
        running.running(windows, classes={k: v for k, v in CLASSES.items() if k != '2026-11-05'}, replicates=20)


def test_the_running_intervals_are_per_set_with_their_counts():
    windows = json.loads(synthetic()['evaluation.json'])['windows']
    r = running.running(windows, classes=CLASSES, replicates=50)
    sets = {s['set']: s for s in r['sets']}
    assert [s['set'] for s in r['sets']] == ['before_cutoff', 'all']
    assert sets['all']['issued_days'] == 6 and sets['all']['scored_days'] == 6
    assert sets['before_cutoff']['issued_days'] == 4 and sets['before_cutoff']['scored_days'] == 4
    assert r['series'] == sets['all']['series'] and len(sets['before_cutoff']['series']['mae']) == 4
    assert sets['before_cutoff']['series']['mae'][-1]['mean'] != sets['all']['series']['mae'][-1]['mean']
    assert running.running(windows, replicates=20)['sets'] == []                       # no classes: CP-18c's shape


def test_a_store_with_a_day_fetched_after_the_cutoff_still_gives_a_bundle_the_frozen_verifier_accepts(live, tmp_path):
    from cp18 import bundle as B
    from cp18d.fixture_after_cutoff import relabel
    from cp18.live_claims import live_record
    from cp18.store import LiveStore
    store = LiveStore(live / 'store')
    day = sorted(d for d, v in store.days().items() if v['status'] == 'issued')[0]
    relabel(live, day, f'{date.fromisoformat(day) - timedelta(days=1)}T09:30:00Z')   # after the CEST cutoff (09:00Z)
    record = build(live, tmp_path / 'bundle')
    files = B.read(tmp_path / 'bundle')
    verdict = B.gate(files, Path(__file__).resolve().parents[2])
    assert verdict['publishable'] and verdict['verify']['accepted'], verdict['verify']['problems'][:5]
    classes = {i['day']: i['input_class'] for i in live_record(live)['issued']}
    assert classes[day] == inputclass.AFTER
    sets = {s['set']: s for s in EV.class_sets(files, classes)['sets']}
    assert sets['all']['issued_days'] == sets['before_cutoff']['issued_days'] == 0      # development days: no prospective day
