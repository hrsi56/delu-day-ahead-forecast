"""Small affected checks; no data fit, receipt replacement or synthetic ledger."""
import hashlib
import json
import os
from pathlib import Path
import runpy
import time

from cp26 import budget as B, execution as E

root = Path.cwd()
directory = root / 'docs/track-b/evidence/cp-26/cold-rerun-2026-10-15'
assert hashlib.sha256((directory / 'daily-execution-v21-r16-empty-keys.py').read_bytes()).hexdigest() == '98b6945682bc05ebf4b993779949f181ef85931cf102ccf0b256460274b404ed'
phase = next(E._read(p) for p in (root / 'reports/rebaseline/cold-rerun-2026-10-15/daily-physical-completion').glob('fit-route-*.json')
             if E._read(p).get('route') == 'nominal' and E._read(p).get('first') == '2022-09-07')
assert all(hashlib.sha256((root / name).read_bytes()).hexdigest() == sha
           for name, sha in phase['fit_identity']['code'].items())
module = runpy.run_path(str(directory / 'quiescent-exit-v21-r16.py'), run_name='cp26_closing_check')
real = B.Budget()


class DisagreeingObservation:
    """Alter only an in-memory expected union; never write it to the live ledger."""
    def resource_read(self):
        state = real.resource_read()
        state = {**state, 'jobs': list(state['jobs'])}
        index = int(os.environ['CP26_JOB_INDEX'])
        job = {**state['jobs'][index]}
        job['worker_identities'] = [*job.get('worker_identities', []),
                                   {'pid': os.getpid(), 'create_time': 0.0}]
        state['jobs'][index] = job
        return state


started = time.monotonic()
try:
    module['settle_observers'](DisagreeingObservation())
except RuntimeError as error:
    assert 'did not settle within14seconds' in str(error)
else:
    raise AssertionError('an observer union disagreement passed closing')
elapsed = time.monotonic() - started
assert 14. <= elapsed <= 17.5
value = {'status': 'CHECKS_PASSED_AWAITING_REAL_OUTER_CLOSE',
         'original_entry_point_sha256': '98b6945682bc05ebf4b993779949f181ef85931cf102ccf0b256460274b404ed',
         'scientific_source_files_unchanged': len(phase['fit_identity']['code']),
         'altered_observation_writes': 0, 'disagreement_rejected': True,
         'deadline_seconds_observed': elapsed,
         'note': 'The outer wrapper next performs the real successful closing handshake. Its supervised terminal receipt is checked separately.'}
path = directory / 'quiescent-exit-checks-v21-r16.json'
assert not path.exists()
path.write_text(json.dumps(value, sort_keys=True, indent=1) + chr(10))
print(json.dumps(value), flush=True)
