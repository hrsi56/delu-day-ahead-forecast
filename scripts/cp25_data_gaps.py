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
    s = sub.add_parser('scan')
    s.add_argument('paths', nargs='*')
    s.set_defaults(func=cmd_scan)
    args = ap.parse_args(argv)
    return args.func(args) or 0


if __name__ == '__main__':
    sys.exit(main())
