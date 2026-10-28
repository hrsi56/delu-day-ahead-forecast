"""CP-17 on the real development inputs: the payloads, the rebuilt interval states, and one native parity
origin against CP-26's stored forecast.

These need CP-26's local-only stored state (the `evidence/cp-26` extract in `.local/artifacts/cp-17/inputs/`),
so they skip with that reason where it is absent, as on CI. `CP17_PROJECT_ROOT` names the checkout that
holds `.local/`. BLAS must be at one thread, as CP-26 ran.
"""
from __future__ import annotations

from datetime import date
import json
import os
from pathlib import Path

import numpy as np
import pytest

from cp17 import dailyfit, issue, schema
from cp17.tools import ledger, parity, payloads, states

ROOT = Path(__file__).resolve().parents[2]
DAY = date(2026, 9, 6)
BLAS = ('OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS')

pytestmark = pytest.mark.skipif(not ledger.available(ROOT),
                                reason="CP-26's local-only stored state (the evidence/cp-26 extract) is absent")


@pytest.fixture(scope='module')
def ctx():
    if any(os.environ.get(n) != '1' for n in BLAS):
        pytest.skip('BLAS threads must be set to 1 before NumPy loads, as in CP-26 (export the five *_NUM_THREADS=1)')
    return payloads.context(ROOT)


@pytest.fixture(scope='module')
def buffers(ctx):
    return states.rebuild(ROOT, ctx, [DAY])


def test_states_rebuild_and_check(buffers):
    for policy in states.POLICIES:
        buf = buffers['buffers'][policy][DAY]
        assert len(buf) == 28 and buf[-1]['day'] == '2026-09-04' and buf[0]['day'] == '2026-08-08'
        assert buffers['checked_days'][policy] >= 28
    record = json.loads((ROOT / 'docs/track-b/evidence/cp-17/freeze-manifest.json').read_text())
    assert record['initial_state']['buffers_sha256'] == {p: states.buffer_sha256(buffers['buffers'][p][DAY])
                                                         for p in states.POLICIES}


def test_payloads_are_the_recorded_ones_and_embargoed(ctx, buffers):
    committed = json.loads((ROOT / 'reports/cp17/native-parity.json').read_text())['origins'][str(DAY)]['payload_sha256']
    b = buffers['buffers']
    built = {'A1': payloads.a1_payload(ctx, DAY, payloads.ensemble(ledger.inputs_dir(ROOT), DAY)),
             'v2': payloads.v2_payload(ctx, DAY, b['v2'][DAY]), 'v4': payloads.v4_payload(ctx, DAY, b['v4'][DAY]),
             'B0': payloads.b0_payload(ctx, DAY, b['B0'][DAY])}
    for policy, (arrays, meta) in built.items():
        assert meta['payload_sha256'] == committed[policy], policy
        assert schema.check_training_window(meta, arrays) == [], policy
        assert issue.check_inputs(policy, arrays, meta) == [], policy


def test_a1_native_parity_with_cp26(ctx):
    arrays, meta = payloads.a1_payload(ctx, DAY, payloads.ensemble(ledger.inputs_dir(ROOT), DAY))
    result = dailyfit.fit_a1(arrays, meta)
    stored = ledger.day(ROOT, DAY)['members']['nominal']['D2']
    check = parity.check_d2(result, stored)
    assert check['pass'] and check['quantiles_bitwise'], check
    assert issue.check_emission(result, DAY) == []


def test_issue_time_matches_cp26_ledger():
    value = ledger.day(ROOT, DAY)
    assert value['lineage']['nominal']['issue_utc'] == issue.issue_utc(DAY)
