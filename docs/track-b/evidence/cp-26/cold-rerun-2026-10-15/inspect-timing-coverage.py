"""Inspect historical resource metadata only; import no old scientific state."""
from pathlib import Path
import hashlib
import json
import os
import sys

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / 'src'))
from cp26.budget import atomic
from cp26.costing import halving_fit_count
from cp26.gates import RUN_EVIDENCE, RUN_ID

if os.environ.get('CP26_RUN_ID') != RUN_ID or not os.environ.get('CP26_MONITORED_JOB'):
    raise RuntimeError('registered monitored timing inspection required')
old = ROOT / 'reports/rebaseline/continuation-v21-r14-accounting-3'
rows = []
for path in sorted((old / 'search-results').glob('*/*.json')):
    raw = path.read_bytes()
    value = json.loads(raw)
    fits = [b for t in value['trials'] for b in t['batches']]
    expected = halving_fit_count(value['B'])
    measured = [b.get('seconds') for b in fits]
    complete = len(fits) == expected and all(isinstance(s, (float, int)) and s > 0 for s in measured)
    rows.append({'route': value['route'], 'k': value['k'], 'B': value['B'],
                 'source': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(raw).hexdigest(),
                 'fit_records': len(fits), 'expected_fit_records': expected,
                 'complete_fit_timing_coverage': complete,
                 'total_recorded_fit_seconds': sum(s for s in measured if isinstance(s, (float, int))),
                 'maximum_recorded_fit_seconds': max(s for s in measured if isinstance(s, (float, int))),
                 'failed_fits': sum(b['status'] == 'failed' for b in fits),
                 'model_code_sha256': value['identity']['code_sha256']})
if len(rows) != 42:
    raise RuntimeError('historical search timing inventory is incomplete')
report = {'run_id': RUN_ID, 'use': 'resource evidence only; no old ensemble/config/cache/state imported',
          'resumed_job_elapsed_is_not_cold_cost': True, 'searches': rows,
          'all42_complete_fit_timing_coverage': all(r['complete_fit_timing_coverage'] for r in rows),
          'total_recorded_fit_hours': sum(r['total_recorded_fit_seconds'] for r in rows) / 3600,
          'incomplete': [(r['route'], r['k']) for r in rows if not r['complete_fit_timing_coverage']]}
atomic(ROOT / RUN_EVIDENCE / 'historical-timing-coverage.json', report)
print(json.dumps({k: v for k, v in report.items() if k != 'searches'}), flush=True)
