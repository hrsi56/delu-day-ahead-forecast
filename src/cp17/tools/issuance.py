"""The product's daily issuance at one origin, under the issuing host and natively (items 3 and 4).

- **The freeze-origin artifact:** delivery 2026-09-06, GFS available. A1 issues under the issuing host.
- **The failure policy, exercised for real:** 2026-09-06 with GFS declared unavailable (A1 skipped, v2
  issues), and 2022-12-04, one of the 18 development dates on which a DDNN-2 member stopped with a nonfinite
  loss (A1 fails, v4 issues).

The issuing host runs `cp17.issue.decide` in Pyodide under Node.js (`host/driver.py`, MODE 'issue'). The
same decision is taken natively from the same payloads, and the two are compared: the chain walked, each
attempt's status, the issued policy, and the issued quantiles by `cp17.retrain.compare`.

    OPENBLAS_NUM_THREADS=1 ... PYTHONPATH=src python -m cp17.tools.issuance --day 2026-09-06 --gfs 1 \\
        --payloads <dir> --bundle <src.zip> --identity <policy-identity.json> --out <dir>
"""
from __future__ import annotations

import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import subprocess
import time

from .. import dailyfit, issue, retrain
from . import ledger, payloads, states
from .bundle import PACKAGES
from .hosts import NODE, RUNNER, node_identity


def build_payloads(root: Path, day: date, folder: Path) -> dict:
    ctx = payloads.context(root)
    rebuilt = states.rebuild(root, ctx, [day])['buffers']
    built = {'A1': payloads.a1_payload(ctx, day, payloads.ensemble(ledger.inputs_dir(root), day)),
             'v4': payloads.v4_payload(ctx, day, rebuilt['v4'][day]), 'v2': payloads.v2_payload(ctx, day, rebuilt['v2'][day]),
             'B0': payloads.b0_payload(ctx, day, rebuilt['B0'][day])}
    return {p: payloads.write(a, m, folder, f'{p}-{day}') for p, (a, m) in built.items()}


def native_issuance(folder: Path, day: date, gfs: bool) -> dict:
    def attempts(policy):
        npz, meta = folder / f'{policy}-{day}.npz', folder / f'{policy}-{day}.json'
        arrays, value = dailyfit.load(npz, meta)
        return issue.attempt(policy, lambda: dailyfit.run(policy, npz, meta, attribution=True), day, arrays, value)
    started = time.perf_counter()
    decision = issue.decide(day, gfs, attempts)
    decision['seconds'] = time.perf_counter() - started
    return decision


def host_issuance(pyodide: Path, bundle: Path, folder: Path, day: date, gfs: bool, identity: Path, out: Path) -> dict:
    import os
    target = out / f'node-issue-{day}-gfs{int(gfs)}.json'
    # Development replay: the data are as available at the issue instant, which is the refresh time recorded.
    env = {**os.environ, 'CP17_DATA_REFRESH_UTC': issue.issue_utc(day)}
    proc = subprocess.run([NODE, str(RUNNER), 'issue', str(pyodide), str(bundle), str(folder), str(day), '1' if gfs else '0',
                           ','.join(PACKAGES), str(target), str(identity)], capture_output=True, text=True, env=env)
    run = json.loads(target.read_text())
    run['returncode'] = proc.returncode
    return run


def compare(native: dict, hosted: dict) -> dict:
    path_n = [(a['policy'], a['status']) for a in native['attempts']]
    path_h = [(a['policy'], a['status']) for a in hosted['attempts']]
    out = {'native_path': path_n, 'host_path': path_h, 'same_path': path_n == path_h,
           'issued_policy': hosted['issued_policy'], 'same_issued_policy': native['issued_policy'] == hosted['issued_policy'],
           'native_display': native['display'], 'host_display': hosted['display'],
           'causes': {a['policy']: a.get('cause') for a in hosted['attempts'] if a['status'] != 'ok'},
           'native_causes': {a['policy']: a.get('cause') for a in native['attempts'] if a['status'] != 'ok'}}
    n_issued = next((a for a in native['attempts'] if a['policy'] == native['issued_policy']), None)
    h_issued = next((a for a in hosted['attempts'] if a['policy'] == hosted['issued_policy']), None)
    if n_issued and h_issued:
        c = retrain.compare(hosted['issued_policy'], n_issued['result'], h_issued['result'])
        out.update(status_vs_native=c['status'], max_abs_eur_vs_native=c['deviation'].get('max_abs_eur'),
                   selections_match_native=c['selections_match'])
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='.', type=Path)
    ap.add_argument('--day', required=True)
    ap.add_argument('--gfs', required=True, choices=('0', '1'))
    ap.add_argument('--payloads', required=True, type=Path)
    ap.add_argument('--bundle', required=True, type=Path)
    ap.add_argument('--identity', required=True, type=Path)
    ap.add_argument('--pyodide', type=Path, default=Path('/Users/djourno/Downloads/PJM/.local/tools/pyodide-0.28.0'))
    ap.add_argument('--out', required=True, type=Path)
    args = ap.parse_args(argv)
    day, gfs = date.fromisoformat(args.day), args.gfs == '1'
    args.out.mkdir(parents=True, exist_ok=True)
    built = None
    if not (args.payloads / f'A1-{day}.json').exists():
        built = build_payloads(args.root, day, args.payloads)
    identity = json.loads(args.identity.read_text())
    from .freeze import digest
    short = args.out / 'host-identity.json'
    short.write_text(json.dumps({'policy_identity_sha256': digest(identity),
                                 'package_sha256': identity['code']['package_sha256']}, sort_keys=True))
    native = native_issuance(args.payloads, day, gfs)
    run = host_issuance(args.pyodide, args.bundle, args.payloads, day, gfs, short, args.out)
    if run.get('errors'):
        record = {'day': str(day), 'gfs_available': gfs, 'errors': run['errors']}
    else:
        hosted = run['python']['decision']
        artifact = run['python']['artifact']
        art_path = args.out / f'artifact-{day}-gfs{int(gfs)}.json'
        art_path.write_text(json.dumps(artifact, sort_keys=True, allow_nan=False) + '\n')
        arrays = args.out / f'node-issue-{day}-gfs{int(gfs)}-artifact-arrays.npz'
        record = {'day': str(day), 'gfs_available': gfs, 'built_payloads': built is not None,
                  'artifact': artifact, 'artifact_file_sha256': hashlib.sha256(art_path.read_bytes()).hexdigest(),
                  'artifact_arrays_sha256': hashlib.sha256(arrays.read_bytes()).hexdigest() if arrays.exists() else None,
                  'artifact_verifies': issue.verify_artifact(artifact) == [], 'comparison': compare(native, hosted),
                  'host': {'node': node_identity(), 'pyodide': run.get('pyodide_version'),
                           'total_seconds': run['total_ms'] / 1000, 'wasm_memory_bytes': run['wasm_memory_bytes'],
                           'process_rss_peak_bytes': run['process_rss_peak_bytes'], 'memory': run['python']['memory'],
                           'blocked_non_local_requests': run['blocked_non_local_requests'],
                           'executed_files': run['python']['source_sha256'], 'stubs': run['python']['stubs']},
                  'native_seconds': native['seconds']}
    path = args.out / f'issuance-{day}-gfs{int(gfs)}.json'
    path.write_text(json.dumps(record, indent=1, sort_keys=True, allow_nan=False) + '\n')
    c = record.get('comparison', {})
    print(day, 'gfs' if gfs else 'no-gfs', record.get('errors') or (c.get('host_path'), c.get('host_display'),
                                                                     c.get('status_vs_native')))
    return 0 if not record.get('errors') else 1


if __name__ == '__main__':
    raise SystemExit(main())
