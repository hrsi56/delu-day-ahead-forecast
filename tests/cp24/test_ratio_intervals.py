"""The 97.5% and 95% ratio intervals of every §23.8 contrast (capstone v21-r11 §23.8), from the stored draws only.

`reports/ddnn2/attempt-<k>/ratio-intervals.csv` must equal a fresh derivation by `cp24.ratios` from the committed
equal-fold ratio draws. Its 95% interval must equal the committed `uncertainty.csv`. Its 97.5% interval must sit at
the scoring code's decision levels, and within 1e-12 of the literal 1.25% and 98.75% percentiles. A contrast with no
defined interval forecast stays undefined. The test reads only CP-24's own files, never rescores, and is skipped
until the table is committed.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from cp24 import ratios as R

ROOT = Path(__file__).resolve().parents[2]
ATTEMPTS = sorted(p for p in (ROOT / 'reports/ddnn2').glob('attempt-*') if (p / 'ratio-intervals.csv').exists())


@pytest.mark.skipif(not ATTEMPTS, reason='no committed CP-24 ratio intervals yet')
@pytest.mark.parametrize('ad', ATTEMPTS, ids=lambda p: p.name)
def test_the_ratio_intervals_rederive_from_the_stored_draws(ad):
    k = int(ad.name.split('-')[1])
    committed = (ad / 'ratio-intervals.csv').read_text()
    assert committed == R.text(R.build(ROOT, k))
    table = pd.read_csv(ad / 'ratio-intervals.csv', float_precision='round_trip')
    unc = pd.read_csv(ad / 'uncertainty.csv', float_precision='round_trip')
    eq = unc.loc[unc.scope.eq('equal_fold')]
    assert len(table) == len(eq) == 22
    assert set(zip(table.candidate, table.baseline, table.metric)) == set(zip(eq.candidate, eq.baseline, eq.metric))
    draws = pd.read_parquet(ad / 'replicates.parquet', filters=[('scope', '==', 'equal_fold')])
    keyed = {key: g.sort_values('replicate')['ratio'].to_numpy(float) for key, g in draws.groupby(['candidate', 'baseline', 'metric'])}
    for _, row in table.iterrows():
        u = eq.loc[eq.candidate.eq(row.candidate) & eq.baseline.eq(row.baseline) & eq.metric.eq(row.metric)].iloc[0]
        if not row.defined:
            assert not bool(u.defined) and np.isnan(row[['ratio', 'ratio_ci95_lower', 'ratio_ci97.5_upper']].to_numpy(float)).all()
            continue
        d = keyed[(row.candidate, row.baseline, row.metric)]
        assert len(d) == 2000 and row.ratio == u.ratio
        assert (row.ratio_ci95_lower, row.ratio_ci95_upper) == (u.ratio_ci_lower, u.ratio_ci_upper)
        lo, hi = row['ratio_ci97.5_lower'], row['ratio_ci97.5_upper']
        assert lo <= row.ratio_ci95_lower <= row.ratio_ci95_upper <= hi
        assert np.allclose(np.quantile(d, [.0125, .9875], method='linear'), (lo, hi), rtol=0, atol=1e-12)
    # the undefined row: L has no interval forecast
    undefined = table.loc[~table.defined.astype(bool)]
    assert set(zip(undefined.candidate, undefined.baseline, undefined.metric)) == {('D2', 'L', 'WIS')}
    # the decision contrast, v5 - v4
    v = table.set_index(['candidate', 'baseline', 'metric'])
    assert v.loc[('v5', 'HGL', 'MAE'), 'ratio_ci97.5_upper'] < 0 and v.loc[('v5', 'HGL', 'WIS'), 'ratio_ci97.5_upper'] < 0
    # negative control: shifted draws move the 97.5% interval
    any_key = next(iter(keyed))
    assert np.quantile(keyed[any_key] + 0.01, .0125, method='linear') != v.loc[any_key, 'ratio_ci97.5_lower']
