#!/usr/bin/env python3
"""CP-25 command line: the development inputs to 2026-09-06 (capstone v21-r13 §24.6).

Run from the repository root with the locked root environment, for example
`.venv/bin/python scripts/cp25_data_gaps.py <command>`. The GFS extraction runs in CP-20's pinned
ecCodes environment (`wx-venv`) through `timed`. Every compute job is charged to the CP-25 ledger
as wall time x workers (§24.6's ceilings).

    init-ledger                       create the cumulative CP-25 ledger (once)
    runs-manifest                     write the frozen 329-run GFS manifest
    timed --name N --workers K -- CMD run a command as a charged job
    features                          weather features for the gaps (CP-20's frozen conversion)
    inventory | tiers | calendar      the inventory, the tier register and margin table, the calendar and masks
    manifest                          the manifest with hashes
    scan                              credential scan of the outputs (names only, never values)
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

PRIMARY = Path('/Users/djourno/Downloads/PJM')
STATE = PRIMARY / '.local/artifacts/cp-25'
LEDGER = STATE / 'ledger.json'
WEATHER = STATE / 'weather'
REPORT = ROOT / 'reports/development-inputs'
RUN_MANIFEST = REPORT / 'gfs-run-manifest.json'


def cmd_init_ledger(_):
    from cp25.ledger import Ledger
    Ledger.initialise(LEDGER)
    print('initialised', LEDGER)


def cmd_runs_manifest(_):
    from cp25 import runs
    digest = runs.write(ROOT, RUN_MANIFEST)
    print(RUN_MANIFEST.relative_to(ROOT), digest)


def cmd_timed(args):
    from cp25.ledger import Ledger
    ledger = Ledger(LEDGER)
    command = args.command[1:] if args.command and args.command[0] == '--' else args.command
    job = ledger.begin_job(args.name, args.workers, ' '.join(command))
    env = dict(os.environ, MLFLOW_DISABLE_TELEMETRY='true', DO_NOT_TRACK='1', PYTHONDONTWRITEBYTECODE='1',
               OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1')
    code = None
    try:
        code = subprocess.call(command, env=env)
    finally:
        used = ledger.charge_job(job, final=True, exit_code=code)
        print(f'[cp25 ledger] job {job} {args.name}: exit {code}; machine-seconds used so far {used:.0f}',
              file=sys.stderr)
    return code


def cmd_build(args):
    from cp25 import build
    summary = {}
    out = Path(args.out).resolve() if args.out else None   # a scratch directory leaves the checkout untouched
    if args.part in ('weather', 'all'):
        summary['weather'] = build.weather(ROOT, WEATHER, out=out)
    if args.part in ('data', 'all'):
        summary['data'] = build.data_side(ROOT, WEATHER, out=out)
    print(json.dumps(summary, indent=1, default=str))


def cmd_identity(_):
    from cp25 import features
    result = features.conversion_identity(ROOT)
    (REPORT / 'conversion-identity.json').write_text(json.dumps(result, indent=1, sort_keys=True) + '\n')
    print(json.dumps(result, indent=1))
    return 0 if result['values_bitwise_identical'] and result['keys_identical'] and result['status_identical'] else 1


def cmd_resources(_):
    from cp25.ledger import Ledger
    state = Ledger(LEDGER).read()
    counts = state['counts']
    out = {'caps': state['caps'], 'counts': counts, 'peaks': state['peaks'],
           'machine_hours': round(counts.get('machine_seconds', 0) / 3600, 4),
           'transfer_gib': round(counts.get('transfer_bytes', 0) / 2**30, 4),
           'jobs': [{k: j.get(k) for k in ('name', 'workers', 'start_utc', 'end_utc', 'wall_seconds', 'charged_seconds', 'exit_code')}
                    for j in state['jobs']],
           'events': state['events'], 'cost_usd': 0,
           'basis': 'machine time = wall time x declared workers per job, charged by the job itself; transfer reserved before each request'}
    (REPORT / 'resources.json').write_text(json.dumps(out, indent=1, sort_keys=True, default=str) + '\n')
    print(json.dumps({k: out[k] for k in ('machine_hours', 'transfer_gib', 'peaks')}))


def cmd_manifest(_):
    from cp25 import build
    m = build.manifest(ROOT, {'extraction_directory': str(WEATHER), 'ledger': str(LEDGER)})
    print(len(m['outputs_sha256']), 'outputs hashed')


def cmd_scan(args):
    from cp25 import guard
    paths = [Path(p) for p in (args.paths or [REPORT, ROOT / 'docs/track-b/evidence/cp-25', STATE])]
    found = guard.scan(paths)
    print(json.dumps({'variables_set': guard.variables_set(), 'files_containing_a_value': found}, indent=1))
    return 1 if found else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='command', required=True)
    sub.add_parser('init-ledger').set_defaults(func=cmd_init_ledger)
    sub.add_parser('runs-manifest').set_defaults(func=cmd_runs_manifest)
    t = sub.add_parser('timed')
    t.add_argument('--name', required=True)
    t.add_argument('--workers', type=int, default=1)
    t.add_argument('command', nargs=argparse.REMAINDER)
    t.set_defaults(func=cmd_timed)
    b = sub.add_parser('build')
    b.add_argument('part', choices=['weather', 'data', 'all'])
    b.add_argument('--out', help='write into this directory instead of reports/development-inputs/')
    b.set_defaults(func=cmd_build)
    sub.add_parser('identity').set_defaults(func=cmd_identity)
    sub.add_parser('resources').set_defaults(func=cmd_resources)
    sub.add_parser('manifest').set_defaults(func=cmd_manifest)
    s = sub.add_parser('scan')
    s.add_argument('paths', nargs='*')
    s.set_defaults(func=cmd_scan)
    args = ap.parse_args(argv)
    return args.func(args) or 0


if __name__ == '__main__':
    sys.exit(main())
