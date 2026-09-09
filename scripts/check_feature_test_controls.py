"""Ensure §9.4 assertions reject preserved/constructed faulty implementations.

Run with one of: attempt1, all_null_price, over_frozen, all_null_a65.
Fault injection is in memory only; no tracked file is modified.
"""
import contextlib
import io
import subprocess
import sys
import numpy as np
import pytest
import delu_forecast.features as features

kind = sys.argv[1]
original = features.build_base_features
rolling = [c for c in features.BASE_FEATURES if c.startswith('price_roll_') or c.startswith('negative_price_count_')]
price = [c for c in features.BASE_FEATURES if c.startswith('price_') or c.startswith('negative_price_count_')]
if kind == 'attempt1':
    source = subprocess.check_output(['git', 'show', 'c0b6e1809180f630ed3a861a8d138fde36460eae:src/delu_forecast/features.py'], text=True)
    namespace = {'__name__': 'delu_forecast.attempt1', '__package__': 'delu_forecast'}
    exec(compile(source, '<attempt1 committed features>', 'exec'), namespace)
    features.build_base_features = namespace['build_base_features']
else:
    def faulty(snapshot):
        result = original(snapshot)
        if kind == 'all_null_price':
            result[price] = np.nan
        elif kind == 'over_frozen':
            dates = result.index.tz_convert('Europe/Berlin').date
            daily = result[rolling].groupby(dates).first().shift(1)
            result[rolling] = daily.reindex(dates).to_numpy()
        elif kind == 'all_null_a65':
            result['load_forecast_day_mean_mw'] = np.nan
        else:
            raise ValueError(kind)
        return result
    features.build_base_features = faulty
path = 'tests/test_09_a65_daily_completeness.py' if kind == 'all_null_a65' else 'tests/test_02_rolling_closed_left.py'
output = io.StringIO()
with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
    code = pytest.main(['-q', '--tb=no', '-p', 'no:cacheprovider', path])
print(kind, 'pytest_exit=', int(code))
print(output.getvalue().strip())
assert int(code) == 1, 'Faulty implementation must be rejected by assertions, not an import/setup error'
