"""CP-28's committed records re-derive from committed inputs alone (no tag, no local input, no history)."""
from __future__ import annotations

from datetime import date
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from cp28 import inference, pipeline, reader

ROOT = Path(__file__).resolve().parents[2]
FORECAST, RESULTS = ROOT / pipeline.FORECAST, ROOT / pipeline.RESULTS

pytestmark = pytest.mark.skipif(not (RESULTS / 'manifest.json').exists(),
                                reason='CP-28 results are not committed in this tree (before the score stage)')


def daily():
    frame = pd.read_parquet(RESULTS / 'daily-losses.parquet')
    frame['day'] = [date.fromisoformat(d) for d in frame.day]
    return frame


def losses():
    out = {}
    for stream, part in daily().groupby('stream'):
        out[stream] = {d: (m, w) for d, m, w in zip(part.day, part.MAE, part.WIS)}
    return out


def test_manifests_bind_every_committed_file_and_none_exceeds_50_mb():
    for directory in (FORECAST, RESULTS):
        manifest = json.loads((directory / 'manifest.json').read_text())
        listed = {entry['path'] for entry in manifest['files']}
        assert listed == {str(p.relative_to(ROOT)) for p in directory.iterdir() if p.name != 'manifest.json'}
        for entry in manifest['files']:
            assert reader.sha256(ROOT / entry['path']) == entry['sha256'], entry['path']
    for path in [*(ROOT / pipeline.OUT).rglob('*'), *(ROOT / 'docs/track-b/evidence/cp-28').rglob('*')]:
        if path.is_file():
            assert path.stat().st_size < 50 * 1024 * 1024, path


def test_arm_losses_rederive_from_the_committed_forecasts_and_snapshot():
    ours, _, _ = pipeline.arm_losses(FORECAST, reader.prices(ROOT))
    stored = losses()
    for arm in inference.ARMS:
        assert set(ours[arm]) == set(stored[arm])
        for d, value in ours[arm].items():
            assert np.array_equal(np.asarray(value), np.asarray(stored[arm][d]), equal_nan=True), (arm, d)


def test_control_and_b0_losses_equal_cp26_stored_scores():
    cp26 = reader.read_table(ROOT, None, 'daily')
    stored = losses()
    for name, stream in (('v5', 'nominal/v5'), ('B0', 'nominal/B0')):
        part = cp26[(cp26.stream == stream) & cp26.eligible & cp26.available & ~cp26.failed]
        assert len(part) == sum(np.isfinite(v[0]) for v in stored[name].values())
        for d, m, w in zip(part.delivery_date, part.MAE, part.WIS):
            assert stored[name][d][0] == pytest.approx(m, rel=1e-12) and stored[name][d][1] == pytest.approx(w, rel=1e-12)


def test_compound_holm_pass_and_selection_rederive_from_endpoint_p_values():
    endpoints = pd.read_parquet(RESULTS / 'endpoints.parquet')
    holm = pd.read_csv(RESULTS / 'holm.csv')
    selection = json.loads((RESULTS / 'selection.json').read_text())
    assert len(endpoints) == 4 * 7 * 20
    passes = {arm: True for arm in inference.ARMS}
    for variant, _, _ in inference.VARIANTS:
        part = endpoints[endpoints.variant == variant]
        compound = {arm: float(part[part.arm == arm].p.max()) for arm in inference.ARMS}
        rows = inference.holm(compound)
        stored = holm[holm.variant == variant].set_index('arm')
        for row in rows:
            assert stored.loc[row['arm'], 'rejected'] == row['rejected']
            assert stored.loc[row['arm'], 'adjusted_p'] == pytest.approx(row['adjusted_p'], rel=0, abs=1e-15)
            passes[row['arm']] = passes[row['arm']] and row['rejected']
    assert passes == selection['passes_all_four']
    l = losses()
    wis = {arm: float(np.mean([l[arm][d][1] for d in inference.paired(l, arm)])) for arm in inference.ARMS}
    again = inference.select([a for a in inference.ARMS if passes[a]], wis)
    assert again['selected'] == selection['selected'] and again['tie_set'] == selection['tie_set']


def test_the_first_endpoint_rederives_from_a_fresh_registered_rng():
    endpoints = pd.read_parquet(RESULTS / 'endpoints.parquet')
    stored = endpoints[(endpoints.variant == 'primary14') & (endpoints.arm == 'A1') & (endpoints.endpoint == 0)].iloc[0]
    l = losses()
    days = inference.paired(l, 'A1')
    d = np.array([l['A1'][x][0] - 0.995 * l['v5'][x][0] for x in days])
    result = inference.test_endpoint(d, days, block_days=14, stratified=True, rng=np.random.default_rng(inference.SEED),
                                     required_cell=False)
    assert result['status'] == stored.status and result['p'] == stored.p and result['n'] == stored.n
