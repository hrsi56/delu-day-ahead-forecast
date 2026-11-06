"""The live bundle's rules (CP-18c items 5, 6 and 9): O18's N1 source labels, the red line on the research windows only,
nothing labelled 4.7T, the classes never pooled, the live label, and the manifest's time notation.

Synthetic inputs over CP-18b's committed development bundle (`reports/cp18b/bundle/`), so GitHub's CI runs them.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from cp18 import bundle as B, outcomes as OC

ROOT = Path(__file__).resolve().parents[2]
DEV = ROOT / 'reports/cp18b/bundle'


def _observed(where, x, rid):
    return {'archive': where, 'archive_day': x, 'record_id': rid}


def test_n1_each_price_names_the_archive_and_record_that_served_it():
    keys = OC.canonical_keys(__import__('datetime').date(2026, 11, 6))
    item = {'status': 'published', 'keys': keys, 'prices': [50.0] * len(keys), 'revised_utc': [''] * len(keys),
            'first': {**_observed('input archive', '2026-11-07', 'price-smard-bucket-01@x'), 'published_utc': 'p'},
            'revisions': [{**_observed('outcome retrieval', '2026-11-06', 'price-smard-bucket-01'),
                           'keys': [keys[3]]}]}
    named = OC.named_sources(item)
    assert named[0] == ('SMARD chart_data filter 4169 (day-ahead price, DE-LU), input archive '
                        'live/inputs/days/2026-11-07/ record price-smard-bucket-01@x')
    assert 'live/outcomes/archive/days/2026-11-06/' in named[3] and named[3] != named[0]
    day = __import__('datetime').date(2026, 11, 6)
    live = OC.bundle_outcomes([day], {str(day): item}, named=True)
    dev = OC.bundle_outcomes([day], {str(day): item})
    assert [p['source'] for p in live['prices']] == named
    assert {p['source'] for p in dev['prices']} == {OC.SOURCE}            # a dry run keeps CP-18b's label (bytes)


def _files():
    if not DEV.is_dir():
        pytest.skip('CP-18b\'s committed development bundle is absent')
    return B.read(DEV)


def _with_evaluation(files, change):
    ev = json.loads(files['evaluation.json'])
    change(ev['windows'])
    return dict(files, **{'evaluation.json': json.dumps(ev).encode()})


def test_the_red_line_applies_to_the_research_windows_only():
    files = _files()
    assert B.identity_problems(files, ROOT) == []
    series = json.loads(files['series.json'])
    series['last_day'] = '2026-09-07'
    assert any('research window' in p for p in B.identity_problems(dict(files, **{'series.json': json.dumps(series).encode()}), ROOT))

    def dev_day_after(windows):
        w = next(w for w in windows if w['window'] == 'development' and w['record']['days'])
        w['record']['days'][0]['day'] = '2026-11-06'
    assert any('research window' in p for p in B.identity_problems(_with_evaluation(files, dev_day_after), ROOT))
    # the live record's issued days and outcomes after the boundary are not a research window
    fc = json.loads(files['issued-forecasts.json'])
    fc['days'][0]['delivery_day'] = '2026-11-06'
    assert not any('red line' in p for p in B.identity_problems(dict(files, **{'issued-forecasts.json': json.dumps(fc).encode()}), ROOT))


def test_nothing_is_labelled_4_7t_and_the_classes_never_pool():
    files = _files()

    def scored_47t(windows):
        w = next(w for w in windows if w['window'] == '4.7T')
        w['record']['days'] = [{'day': '2026-11-06'}]
    assert any('4.7T' in p for p in B.identity_problems(_with_evaluation(files, scored_47t), ROOT))

    def pooled(windows):
        w = next(w for w in windows if w['window'] == 'prospective')
        w['record']['days'] = [{'day': '2026-09-05'}]
    assert any('never pool' in p for p in B.identity_problems(_with_evaluation(files, pooled), ROOT))


def test_the_live_label_and_the_manifest_time_notation():
    label = B.evidence_label([{'day': '2026-11-03', 'status': 'not issued', 'cause': 'inputs',
                               'text': "a live day's inputs that cannot be shown to precede its cutoff"},
                              {'day': '2026-10-01', 'status': 'outside', 'cause': None, 'text': 'outside'}],
                             live_from='2026-11-03')
    assert label.startswith('v6 · DDNN-2 alone (A1 in the frozen records) · final candidate · pending 4.7T; the live '
                            'product\'s own issued days from 2026-11-03')
    assert 'prospective evaluation in progress' in label and "never 4.7T's" in label and '2026-10-01' not in label
    assert B.evidence_label([]) == B.EVIDENCE_LABEL
    times = {'last_training_utc': '2026-11-05T10:00:00+00:00', 'data_refresh_utc': '2026-11-05T21:46:40Z',
             'issuance_utc': '2026-11-05T10:00:00+00:00'}
    assert B.manifest_times(times)['data_refresh_utc'] == '2026-11-05T21:46:40+00:00'
    assert B.manifest_times(times)['issuance_utc'] == times['issuance_utc']
