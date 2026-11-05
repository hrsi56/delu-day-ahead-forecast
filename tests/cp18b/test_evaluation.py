"""The committed evaluation records (`cp18.evaluation`): `cp17.scoring.evaluate`, per window and policy, never pooled."""
from __future__ import annotations

from datetime import date
import json

import pytest

from cp17 import scoring
from cp18 import evaluation as EV, spaceglue as G
from cp18b.support18b import ROOT, load

DEV = ROOT / EV.DEVELOPMENT_FILE


def test_the_static_development_records_equal_cp17s_scoring_check():
    value = load(DEV)
    assert value['schema'] == EV.SCHEMA and EV.matches_scoring_check(value, ROOT) == []
    assert sorted(value['summaries']) == ['autumn-2025/A1', 'autumn-2025/B0', 'spring-summer-2026/A1',
                                          'spring-summer-2026/B0']
    for w in value['windows']:
        assert w['window'] == 'development' and w['evidence_class'].startswith(G.DEVELOPMENT)
        assert w['record']['schema'] == 'cp17-evaluation-v1' and w['record']['tau_eur'] == scoring.TAU_EUR
        assert all(date.fromisoformat(d['day']) <= G.BOUNDARY for d in w['record']['days'])


def test_the_static_records_hold_dst_and_partial_days_and_the_hard_prices():
    windows = {(w['evidence_class'].split(' · ')[3], w['policy']): w['record'] for w in load(DEV)['windows']}
    autumn, spring = windows[('autumn-2025 (2025-10-01 to 2025-11-30)', 'product')], \
        windows[('spring-summer-2026 (2026-03-01 to 2026-09-06)', 'product')]
    assert {d['canonical_hours'] for d in autumn['days']} == {24, 25}
    assert {d['canonical_hours'] for d in spring['days']} == {23, 24}
    assert autumn['pooled']['partial_days'] == spring['pooled']['partial_days'] == 3


@pytest.mark.skipif(not __import__('cp17.tools.ledger', fromlist=['available']).available(ROOT),
                    reason="CP-26's stored ledger (the local-only evidence/cp-26 extract) is absent")
def test_the_static_records_are_recomputed_from_cp26s_ledger():
    from cp18.records import dump_bytes
    assert dump_bytes(EV.development(ROOT)) == DEV.read_bytes()


def test_the_three_windows_never_pool(files):
    ev = json.loads(files['evaluation.json'])
    forecasts = json.loads(files['issued-forecasts.json'])
    issued = sorted(d['delivery_day'] for d in forecasts['days'])
    by = {}
    for w in ev['windows']:
        assert w['window'] in ('development', '4.7T', 'prospective') and w['policy'] in ('product', 'B0')
        by.setdefault((w['window'], w['evidence_class']), []).append(w)
    rehearsal = [w for w in ev['windows'] if w['evidence_class'] == G.REHEARSAL]
    assert [w['policy'] for w in rehearsal] == ['product', 'B0']
    assert [d['day'] for d in rehearsal[0]['record']['days']] == issued
    for name in ('4.7T', 'prospective'):
        entries = [w for w in ev['windows'] if w['window'] == name]
        assert [w['policy'] for w in entries] == ['product', 'B0']
        assert all(w['record']['days'] == [] and w['record']['pooled']['scored_days'] == 0 for w in entries)
    assert [w for w in ev['windows'] if w['window'] == '4.7T'][0]['evidence_class'] == G.FRESH_TEST
    assert [w for w in ev['windows'] if w['window'] == 'prospective'][0]['evidence_class'] == G.PROSPECTIVE


def test_the_dry_run_days_are_never_prospective_or_47t():
    days = ['2026-08-31', '2026-09-01', '2026-09-02', '2026-09-03', '2026-09-05']
    assert G.window_days({'window': 'prospective', 'evidence_class': G.PROSPECTIVE}, days) == []
    assert G.window_days({'window': '4.7T', 'evidence_class': G.FRESH_TEST}, days) == []
    assert G.window_days({'window': 'development', 'evidence_class': G.REHEARSAL}, days) == days
    assert G.window_days({'window': 'prospective', 'evidence_class': G.PROSPECTIVE}, days + ['2026-09-07']) == ['2026-09-07']


def test_the_daily_record_is_committed_once_per_as_of_day(tmp_path, files):
    from cp18.records import LogRefused
    ev = json.loads(files['evaluation.json'])
    daily = [w for w in ev['windows'] if G.recomputed(w)]
    entry = EV.commit_daily(tmp_path, date(2026, 9, 5), daily, 'a' * 64, 'run')
    assert entry['file'] == '2026-09-05.json'
    with pytest.raises(LogRefused):
        EV.commit_daily(tmp_path, date(2026, 9, 5), daily, 'a' * 64, 'run')


def test_the_rehearsal_agrees_with_the_static_development_record_on_shared_days(files):
    """The dry runs reissued CP-17c's frozen A1 bit for bit; where a dry-run day is also in CP-17's development window
    (2026-08-31 to 2026-09-05), the two records must give that day the same statistics."""
    static = [w for w in load(DEV)['windows'] if w['policy'] == 'product' and 'spring-summer-2026' in w['evidence_class']][0]
    rehearsal = [w for w in json.loads(files['evaluation.json'])['windows']
                 if w['evidence_class'] == G.REHEARSAL and w['policy'] == 'product'][0]
    by_day = {d['day']: d for d in static['record']['days']}
    shared = [d for d in rehearsal['record']['days'] if d['day'] in by_day]
    assert shared, 'no shared day'
    for d in shared:
        s = by_day[d['day']]
        if d['keys'] == s['keys']:
            assert d['mae_eur'] == pytest.approx(s['mae_eur'], abs=1e-6)
