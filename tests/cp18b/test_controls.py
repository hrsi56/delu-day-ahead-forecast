"""The negative controls (the Space plan §7 step 6, PUBLISH_RULES §7.3) and §16.4's positive controls, on the gate.

Every rule `verify_bundle` checks has a tampered copy that is refused; R7's raised error is a refusal; an altered
identity, a future label and a crossed red line are refused; a mismatched recomputation shows ✗ with both values and
blocks publication; a pending outcome stays unscored; stale and failed fits are shown as such; missing, zero and
negative prices, and partial and DST days, are scored as the frozen definitions say.
"""
from __future__ import annotations

from datetime import date, datetime, timedelta
import json

import pytest

from cp17.issue import canonical_hours
from cp18 import bundle as B, controls as C, evaluation as EV, spaceglue as G
from cp18b.support18b import issuing_platform, ROOT, build, load

RULES = ('1_manifest_invalid_state_late', '2_listed_file_missing', '2_one_byte_changed_unhashed',
         '2_unreadable_json_rehashed', '2_unreadable_npz_rehashed', '3_unlisted_file_served', '4_wrong_kind',
         '4_outcomes_fail_their_schema', '5_training_window_bit_flipped', '5_training_window_meta_changed',
         '6_future_label_leak_target_day_price', '6_released_error_after_d_minus_2', '7_artifact_identity_altered',
         '7_manifest_names_another_artifact', '7_issued_forecast_not_the_artifacts', 'r7_verifier_raises',
         'identity_policy_altered', 'identity_package_altered', 'red_line_series_past_the_boundary', 'recompute_mismatch')


def test_every_negative_control_is_refused_and_the_served_bundle_is_not(files):
    value = C.verify_controls(files, ROOT)
    assert sorted(value['controls']) == sorted(RULES)
    assert value['all_refused'] and value['served_bundle']
    committed = load(ROOT / 'reports/cp18b/controls.json')
    assert {k: v['refused'] for k, v in committed['controls'].items()} == {k: True for k in RULES}


def test_a_tampered_file_is_detected(files):
    v = B.gate(dict(files, **{'outcomes.json': C._flip(files['outcomes.json'])}), ROOT)
    assert not v['publishable'] and 'outcomes.json: its SHA-256 or size differs from the manifest' in v['verify']['problems']


def test_a_mismatched_recomputation_shows_both_values_and_blocks_publication(files):
    check = G.recompute(C.mismatch(files))
    row = next(r for r in check['rows'] if r['recomputed'] and not r['match'])
    assert check['blocks_publication'] and row['blocks_publication'] and row['policy'] == 'product'
    shown = {s['path']: s for s in row['shown']}['pooled/mae_eur']
    assert shown['committed'] == pytest.approx(shown['recomputed'] + 0.01)
    assert row['mismatches'][0]['path'] == 'pooled/mae_eur'


@issuing_platform
def test_a_pending_outcome_stays_unscored(live, tmp_path):
    class Nothing:
        def send(self, request):
            from cp18.live.transport import ReplayMiss
            raise ReplayMiss('no retrieval in this control')
    record = build(live, tmp_path / 'b', transport=Nothing())
    out = json.loads((tmp_path / 'b' / 'outcomes.json').read_text())
    assert all(p['price'] is None for p in out['prices'])
    rehearsal = next(w for w in record['daily_windows'] if w['evidence_class'] == G.REHEARSAL and w['policy'] == 'product')
    assert all(not d['scored'] and d['scored_hours'] == 0 for d in rehearsal['record']['days'])
    assert rehearsal['record']['pooled'] == {'scored_days': 0, 'scored_hours': 0, 'pending_or_unscored_days': 5,
                                             'partial_days': 0}
    assert B.gate(B.read(tmp_path / 'b'), ROOT)['publishable']


@issuing_platform
def test_a_stale_and_a_failed_artifact_are_shown_as_such(live, tmp_path):
    from cp18.store import LiveStore
    later = datetime.fromisoformat('2026-09-06T10:00:00+02:00')
    assert build(live, tmp_path / 's', now=later)['freshness']['state'] == 'stale'
    LiveStore(live / 'store').record_not_issued(date(2026, 9, 6), 'inputs', ['control'])
    failed = build(live, tmp_path / 'f', now=later)
    manifest = json.loads((tmp_path / 'f' / 'manifest.json').read_text())
    assert manifest['freshness'] == {'state': 'failed', 'as_of_day': '2026-09-06', 'latest_issued_day': '2026-09-05'}
    assert "2026-09-06, a live day's inputs that cannot be shown to precede its cutoff" in manifest['product']['evidence_label']


def test_a_changed_seed_window_is_refused_by_the_gate_and_reported_different(files):
    variant = C.seed_variant(files)
    verdict = B.gate(variant, ROOT)
    assert not verdict['publishable'] and any('training window' in p for p in verdict['identity'])
    artifact = json.loads(files['artifact.json'])
    meta = json.loads(variant[f"A1-{artifact['delivery_day']}.json"])
    retrained = {'day': artifact['delivery_day'], 'index': artifact['keys'], 'quantiles': artifact['quantiles'],
                 'payload_sha256': meta['payload_sha256'], 'members': artifact['lineage']['training']['members'],
                 'search': artifact['lineage']['training']['search'],
                 'ensemble_content_sha256': artifact['lineage']['training']['ensemble_content_sha256']}
    report = G.retrain_report(artifact, retrained)
    assert report['status'] == 'different' and report['measured_status'] == 'identical bit for bit'
    assert not report['payload_sha256_equal']


def test_missing_zero_and_negative_prices_keep_the_bundle_publishable_and_partial(files):
    variant = C.prices_variant(files)
    assert B.gate(variant, ROOT)['publishable']
    day = json.loads(files['artifact.json'])['delivery_day']
    ev = json.loads(variant['evaluation.json'])
    rec = next(w for w in ev['windows'] if w['evidence_class'] == G.REHEARSAL and w['policy'] == 'product')['record']
    d = next(x for x in rec['days'] if x['day'] == day)
    assert d['scored_hours'] == d['canonical_hours'] - 1 and d['completeness'] == pytest.approx(23 / 24)
    assert rec['pooled']['partial_days'] == 1


def _synthetic(days: list[date], hours_missing: dict[date, int] | None = None) -> dict[str, bytes]:
    """A minimal served bundle for the recomputation: issued forecasts, outcomes and committed records only."""
    from cp18 import outcomes as OC
    hours_missing = hours_missing or {}
    forecasts = {'schema': 'cp17b-issued-forecasts-v2', 'levels': [0.025, 0.1, 0.25, 0.5, 0.75, 0.9, 0.975], 'days': []}
    view = {}
    for i, d in enumerate(days):
        keys = canonical_hours(d)[hours_missing.get(d, 0):]
        q = [[10.0 * k + j * 3 + i for j in range(7)] for k in range(len(keys))]
        forecasts['days'].append({'delivery_day': str(d), 'issue_utc': '', 'issuing_artifact_sha256': '0' * 64,
                                  'issued_policy': 'A1', 'display': '', 'keys': keys, 'quantiles': q, 'partial': None})
        full = canonical_hours(d)
        prices = [(-7.0 if k % 5 == 0 else 0.0 if k % 7 == 0 else 10.0 * k + 8) for k in range(len(full))]
        prices[-1] = None
        view[str(d)] = {'status': 'partial', 'keys': full, 'prices': prices, 'revised_utc': [''] * len(full),
                        'first': {'published_utc': ''}}
    out = OC.bundle_outcomes(days, view)
    ev = EV.evaluation_bundle([], EV.daily_windows(forecasts, out, []))
    return {'issued-forecasts.json': json.dumps(forecasts).encode(), 'outcomes.json': json.dumps(out).encode(),
            'evaluation.json': json.dumps(ev).encode()}


def test_dst_and_partial_days_are_scored_with_their_canonical_hours():
    days = [date(2025, 10, 26), date(2026, 3, 29), date(2026, 3, 30)]
    files = _synthetic(days, {date(2026, 3, 30): 1})
    check = G.recompute(files)
    assert check['match'] and check['recomputed_windows'] == 6
    rec = json.loads(files['evaluation.json'])['windows'][0]['record']
    by = {d['day']: d for d in rec['days']}
    assert by['2025-10-26']['canonical_hours'] == 25 and by['2025-10-26']['scored_hours'] == 24
    assert by['2026-03-29']['canonical_hours'] == 23 and by['2026-03-29']['scored_hours'] == 22
    assert by['2026-03-30']['keys'] == 23 and by['2026-03-30']['scored_hours'] == 22
    assert rec['pooled']['partial_days'] == 3


def test_future_label_leakage_is_refused_and_the_red_line_holds(files):
    value = C.verify_controls(files, ROOT)['controls']
    assert value['6_future_label_leak_target_day_price']['refused']
    assert "the target day's outcome is present" in value['6_future_label_leak_target_day_price']['reasons'][0]
    assert value['red_line_series_past_the_boundary']['refused']
    assert G.BOUNDARY + timedelta(days=1) == date(2026, 9, 7)
