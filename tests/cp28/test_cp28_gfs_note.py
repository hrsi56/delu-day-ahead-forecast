"""The r17 GFS note: mixture algebra on synthetic values, and byte regeneration from CP-26's stored outputs."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from cp28 import gfs_note, reader

ROOT = Path(__file__).resolve().parents[2]
NOTE = ROOT / 'docs/track-b/evidence/cp-28/gfs-postresults'


def test_break_even_cases():
    assert gfs_note.break_even(10.0, 12.0, 11.0) == (0.5, 'crossing')
    p, status = gfs_note.break_even(10.0, 12.0, 13.0)
    assert p is None and status == 'no crossing in [0,1]'
    p, status = gfs_note.break_even(10.0, 12.0, 9.0)
    assert p is None and status == 'no crossing in [0,1]'
    assert gfs_note.break_even(10.0, 10.0, 11.0)[0] is None
    assert gfs_note.break_even(10.0, 9.0, 11.0)[1].startswith('S below N')


def test_mixture_reproduces_endpoints_and_break_even():
    rows = gfs_note.mixture([{'model': 'v5', 'metric': 'MAE', 'population': 'p', 'slice': 's', 'value': 'v',
                              'n_pairs': 3, 'nominal_mean': 10.0, 'gfs6_mean': 14.0, 'v2_mean': 12.0}])
    row = rows[0]
    assert row['L_p0'] == 10.0 and row['L_p1'] == 14.0 and row['L_p0.5'] == 12.0
    assert row['p_star'] == 0.5


def test_summary_pairs_only_complete_dates_and_uses_ratio_of_means():
    left = pd.Series([10.0, 20.0, np.nan], index=[1, 2, 3])
    right = pd.Series([11.0, 26.0, 5.0], index=[1, 2, 3])
    stats = gfs_note.summary(left, right)
    assert stats['n_pairs'] == 2 and stats['missing_pairs'] == 1
    assert stats['ratio'] == pytest.approx(37.0 / 30.0)   # never the mean of daily ratios (1.1 and 1.3)


def test_blocks_partition_the_local_day():
    hours = [h for block in gfs_note.BLOCKS.values() for h in block]
    assert sorted(hours) == list(range(24))


def test_note_regenerates_byte_for_byte(tmp_path):
    local = reader.local_root(ROOT)
    if local is None:
        pytest.skip('CP-26 local analysis outputs (.local/artifacts/cp-26/...) are absent; the note cannot be regenerated here')
    gfs_note.main([str(ROOT), str(tmp_path)])
    for name in ('note.md', 'table.csv', 'provenance.json'):
        assert (tmp_path / name).read_bytes() == (NOTE / name).read_bytes(), name
