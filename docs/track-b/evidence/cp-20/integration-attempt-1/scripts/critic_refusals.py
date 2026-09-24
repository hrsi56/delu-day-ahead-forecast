"""Synthetic refusal checks (no research data) and the frozen-protocol gate at the clean candidate."""
import json, sys, traceback
from datetime import date, timedelta
from pathlib import Path
import numpy as np, pandas as pd
ROOT = Path.cwd(); sys.path.insert(0, str(ROOT / 'src'))
from cp15.data import prepare, history_start, day_hours, RAW_COLUMNS
out = {}
p = json.loads((ROOT / 'reports/cp15/protocol.json').read_text())
days = [date(2018, 12, 31) + timedelta(days=i) for i in range(10)]
ts = np.concatenate([day_hours(d).to_numpy() for d in days])
fr = pd.DataFrame({'timestamp_utc': pd.DatetimeIndex(ts), 'delivery_date': [t.tz_convert('Europe/Berlin').date() for t in pd.DatetimeIndex(ts)],
                   'price_eur_mwh': 50.0, 'load_forecast_mw': 50000.0})[RAW_COLUMNS]
try:
    prepare(fr, p); out['prepare_pre2019'] = 'NOT REFUSED'
except ValueError as e:
    out['prepare_pre2019'] = f'refused: {e}'
out['history_start_A1_2019_06_01'] = str(history_start(date(2019, 6, 1), 'A1'))
out['history_start_B2_2020_12_31'] = str(history_start(date(2020, 12, 31), 'B2'))
try:
    history_start(date(2019, 2, 1), 'A4'); out['history_start_A4_pre2019'] = 'NOT REFUSED'
except ValueError as e:
    out['history_start_A4_pre2019'] = f'refused: {e}'
from cp20.weather import missing_day, ConversionRefused
try:
    missing_day(date(2020, 1, 1), 'network_failure', 'x'); out['missing_day_nonimputable_class'] = 'NOT REFUSED'
except ConversionRefused as e:
    out['missing_day_nonimputable_class'] = f'refused: {e}'
from cp20.execution import check_protocol
try:
    check_protocol(ROOT); out['check_protocol_at_clean_candidate'] = 'passed'
except Exception as e:
    out['check_protocol_at_clean_candidate'] = f'{type(e).__name__}: {e}'
print(json.dumps(out, indent=1))
json.dump(out, open('/Users/djourno/Downloads/PJM/.local/artifacts/cp-20/critic/out/refusals.json', 'w'), indent=1)
