"""The live claim builder (`cp18.live_claims`): every text from the claim layer or a committed record, O13 and O14."""
from __future__ import annotations

import json
import re

import pytest

from cp18.live_claims import LIMITATION_ORDER, build_live_claims, text
from cp18b.support18b import ROOT, load


@pytest.fixture(scope='module')
def claims():
    return build_live_claims(ROOT, rehearsal_days=('2026-08-31', '2026-09-05'))


def test_o13_status_and_hero_rule(claims):
    v = claims['values']
    assert v['live_product_status'] == 'final candidate · pending 4.7T'
    assert 'becomes "live" only at CP-18\'s activation, which requires a passed 4.7T' in v['live_hero_rule']
    assert build_live_claims(ROOT, fresh_test='passed')['values']['live_product_status'] == 'live'
    failed = build_live_claims(ROOT, fresh_test='failed')['values']
    assert failed['live_released_product'] == 'v1 stays the released product'
    protocol = (ROOT / 'docs/track-b/evidence/cp-17/4-7t-frozen-protocol.md').read_text()
    assert ' '.join(protocol.split()).count(v['live_fresh_test_badge']) == 1


def test_o14_wording_is_cp17s_proposal_plus_f1_at_its_largest_observed_figure(claims):
    wording = claims['values']['live_retrain_wording']
    report = ' '.join((ROOT / 'reports/cp17/report.md').read_text().split())
    proposal = wording.split(' The issued values were computed')[0]
    assert proposal in report and proposal.startswith("Retraining this day's model")
    identity = load(ROOT / 'docs/track-b/evidence/cp-17c/freeze-manifest.json')['policy_identity']
    largest = re.search(r'by up to ([0-9.]+) EUR/MWh', identity['disclosures']['F1_largest_observed']).group(1)
    assert largest == '0.082'
    assert wording.endswith(f"differed from native arithmetic by up to {largest} EUR/MWh (A1's p2.5 on 2026-03-30), "
                            'the largest difference observed, not a bound.')
    anchor = ' '.join((ROOT / 'capstone_v21.md').read_text().split())
    assert 'The largest difference observed is 0.082 EUR/MWh,' in anchor


def test_the_limitations_are_generated_and_complete(claims):
    keys = [k for _, k in claims['limitations']]
    assert keys[:len(LIMITATION_ORDER)] == [f'live_limitation_{t}' for t in LIMITATION_ORDER]
    assert all(text(claims, k) for k in keys)
    assert 'limitation_mtu_averaging' in keys and 'gfs_attribution' in keys


def test_no_text_claims_late_timely_correctness_or_confidence(claims):
    for key, value in claims['values'].items():
        low = value.lower()
        assert not re.search(r'\blate\b|\btimely\b|% correct|confidence', low), key
        assert 'before the auction' not in low or 'no forecast is claimed' in low, key


def test_the_wording_labels_are_a9s(claims):
    v = claims['values']
    assert v['live_counterfactual_label'] == 'counterfactual scenario — not an issued forecast'
    assert v['live_retrained_label'] == 'your retrained model'
    assert v['live_prospective_label'] == 'prospective evaluation in progress'
    assert v['live_percentage_label'] == 'share of scored hours within ±10 EUR/MWh of the published price'
