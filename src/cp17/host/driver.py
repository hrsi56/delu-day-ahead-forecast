"""The Python every Pyodide host executes: the issuing host (Node.js) and the browser load this file as text
from the unpacked package, so its hash is in the package manifest like every other shipped file.

Globals set by the host: MODE ('fit' or 'issue'), STEM or DAY, POLICY, ATTRIBUTION, GFS_AVAILABLE, and
MEASURE (a host function returning the process's peak resident memory and the WebAssembly heap, in bytes).
The payload files are at /home/pyodide/<policy>-<day>.npz and .json. The last expression is the run as JSON.

- **fit**: one policy's daily fit from its payload, as `cp17.dailyfit.run` (the parity and browser checks).
- **issue**: the product's issuance at DAY under the frozen failure policy (`cp17.issue.decide`), fitting only
  the policies the chain reaches, then the issued artifact with the measured wall time and peak memory.
- **score**: §19.5's evaluation record (`cp17.scoring.evaluate`) of /home/pyodide/score-input.json, as the
  Space recomputes it.
"""
from datetime import date
import hashlib, json, os, sys, time
SRC = '/home/pyodide/src'
sys.path.insert(0, SRC)
stubs = []
try:
    import resource
except ImportError:
    sys.path.insert(0, SRC + '/cp17/stubs/fallback')
    import resource
    stubs.append('resource')
sys.path.append(SRC + '/cp17/stubs/absent')
import numpy as np
from cp17 import dailyfit


def _paths(stem):
    npz = f'/home/pyodide/{stem}.npz'
    return (npz if os.path.exists(npz) else None), f'/home/pyodide/{stem}.json'


def _measure():
    m = MEASURE().to_py() if hasattr(MEASURE, 'to_py') else MEASURE()
    return {k: int(v) for k, v in dict(m).items()}


started = time.perf_counter()
if MODE == 'fit':
    npz, meta = _paths(STEM)
    out = {'result': dailyfit.run(POLICY, npz, meta, attribution=bool(ATTRIBUTION))}
elif MODE == 'issue':
    from cp17 import issue
    day = date.fromisoformat(DAY)
    payloads = {}

    def attempts(policy):
        npz, meta = _paths(f'{policy}-{DAY}')
        arrays, meta_value = dailyfit.load(npz, meta)
        payloads[policy] = {'payload_sha256': meta_value.get('payload_sha256')}
        return issue.attempt(policy, lambda: dailyfit.run(policy, npz, meta, attribution=True, export=True), day,
                             arrays, meta_value)

    decision = issue.decide(day, bool(GFS_AVAILABLE), attempts)
    wall = time.perf_counter() - started
    memory = _measure()
    exported = {}
    for a in decision['attempts']:
        if 'result' in a:
            fitted = a['result'].pop('_arrays', None)
            if a['policy'] == decision['issued_policy'] and fitted:
                exported = fitted
    if exported:
        dailyfit.save_npz('/home/pyodide/artifact-arrays.npz', exported)
    identity = json.loads(IDENTITY) if 'IDENTITY' in globals() else {}
    out = {'decision': decision, 'artifact': issue.artifact(
        decision, identity=identity, payloads=payloads, parent_sha256=None, data_refresh_utc=DATA_REFRESH_UTC,
        host=json.loads(HOST), wall_seconds=wall, peak_bytes=max(memory.values())), 'memory': memory,
        'exported_arrays': sorted(exported)}
elif MODE == 'score':
    from cp17 import scoring
    with open('/home/pyodide/score-input.json', encoding='utf-8') as handle:
        item = json.load(handle)
    outcomes = {k: (float('nan') if v is None else v) for k, v in item['outcomes'].items()}
    out = {'records': {name: scoring.evaluate(issued, outcomes) for name, issued in item['windows'].items()}}
else:
    raise ValueError(f'unknown MODE {MODE}')
seconds = time.perf_counter() - started
loaded = sorted(n for n, m in sys.modules.items() if getattr(m, '__file__', None) and m.__file__.startswith(SRC + '/'))
files = {}
for name in loaded:
    path = sys.modules[name].__file__
    with open(path, 'rb') as handle:
        files[os.path.relpath(path, SRC)] = hashlib.sha256(handle.read()).hexdigest()
with open(SRC + '/cp17/host/driver.py', 'rb') as handle:
    files['cp17/host/driver.py'] = hashlib.sha256(handle.read()).hexdigest()
if 'holidays' in sys.modules and getattr(sys.modules['holidays'], '__file__', '').startswith(SRC + '/'):
    stubs.append('holidays')
import pandas, platform
out.update({'seconds': seconds, 'stubs': stubs, 'source_sha256': files, 'python': sys.version.split()[0],
            'numpy': np.__version__, 'pandas': pandas.__version__, 'platform': platform.platform()})
json.dumps(out, allow_nan=False)
