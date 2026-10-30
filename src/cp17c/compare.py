"""CP-17c's comparison, offline: the runner's and the Owner's M3's results against CP-17b's records.

- **fetch** (needs `gh`, read-only): one run's artifacts, each downloaded as its zip and checked against the digest
  GitHub recorded, with the run's jobs, steps and billable time.
- **compare:** from the downloaded results (each file checked against its job's `results-sha256.txt`) and the
  local results, for each machine:
  - **the H2 checks:** the gate passed in every run, `refreeze verify` printed exactly `verified`, and each forced
    failure stopped at its own check with nothing issued; the machine as recorded (image, CPU, cores, memory);
  - **the freeze-origin store:** initialized from the freeze-origin states and loaded back, CP-17's buffers;
  - **A1's parity at the nine origins,** bit for bit against `reports/cp17b/host-parity.json`: 2025-10-26 and
    2026-03-29 from the checks run, 2026-08-31 to 2026-09-06 from the late shadow block's A1 issuances, whose payloads
    are the same (checked);
  - **the 14 shadow days:** every buffer against CP-17b's host shadow run at every origin, every fit's quantiles
    against its reference run, every intake, every artifact, the final state against CP-17b's, the store's chain, and
    the stitch (the early block's last state is the late block's start state);
  - **timing and memory** per fit against 15 minutes and 4 GiB, and the cost: one issuance, and decision 23's four
    issuances with the canary, from the sequential issuances;
  - **minutes** as a private repository counts them.

    PYTHONPATH=src python -m cp17c.compare fetch --repo hrsi56/delu-host-refreeze --run <id> --dest <dir> --record <json>
    PYTHONPATH=src python -m cp17c.compare compare --inputs <inputs.json> --artifacts <json> --downloads <dir> \\
        --local <dir> --out <measurement.json>
"""
from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta
import json
import math
from pathlib import Path
import statistics
import subprocess
import zipfile

from .run import dump, sha256_file

FIRST, SPLIT, LAST = date(2026, 8, 24), date(2026, 8, 31), date(2026, 9, 6)
NINE = ('A1-2025-10-26', 'A1-2026-03-29') + tuple(f'A1-{SPLIT + timedelta(days=i)}' for i in range(7))
POLICIES = ('A1', 'v4', 'v2', 'B0')
WALL, PEAK = 900, 4 * 1024 ** 3
MULTIPLIER = {'MACOS': 10, 'UBUNTU': 1}
BLOCKS = {'late': (SPLIT, LAST), 'early': (FIRST, SPLIT - timedelta(days=1))}


# --- fetch --------------------------------------------------------------------------------------------------------

def _gh(*args: str) -> str:
    return subprocess.run(['gh', *args], capture_output=True, text=True, check=True).stdout


def _seconds(start: str | None, end: str | None) -> float | None:
    if not start or not end:
        return None
    parse = lambda t: datetime.fromisoformat(t.replace('Z', '+00:00'))   # noqa: E731
    return (parse(end) - parse(start)).total_seconds()


def fetch(repo: str, run_id: str, dest: Path, record: Path) -> dict:
    run = json.loads(_gh('api', f'repos/{repo}/actions/runs/{run_id}'))
    jobs = json.loads(_gh('api', f'repos/{repo}/actions/runs/{run_id}/jobs?per_page=100'))['jobs']
    timing = json.loads(_gh('api', f'repos/{repo}/actions/runs/{run_id}/timing'))
    listed = json.loads(_gh('api', f'repos/{repo}/actions/runs/{run_id}/artifacts?per_page=100'))['artifacts']
    folder = dest / str(run_id)
    folder.mkdir(parents=True, exist_ok=True)
    artifacts = []
    for item in listed:
        zpath = folder / f"{item['name']}.zip"
        zpath.write_bytes(subprocess.run(['gh', 'api', f"repos/{repo}/actions/artifacts/{item['id']}/zip"],
                                         capture_output=True, check=True).stdout)
        digest = sha256_file(zpath)
        if item.get('digest') and item['digest'] != f'sha256:{digest}':
            raise SystemExit(f"{item['name']}: the zip is not the artifact GitHub recorded")
        with zipfile.ZipFile(zpath) as z:
            z.extractall(folder / item['name'])
        artifacts.append({'id': item['id'], 'name': item['name'], 'size_in_bytes': item['size_in_bytes'],
                          'digest': item.get('digest'), 'zip_sha256': digest, 'path': f"{run_id}/{item['name']}"})
    value = json.loads(record.read_text()) if record.exists() else {'schema': 'cp17c-artifacts-v1', 'repo': repo, 'runs': {}}
    value['runs'][str(run_id)] = {
        'run_attempt': run.get('run_attempt'), 'head_sha': run.get('head_sha'), 'status': run.get('status'),
        'conclusion': run.get('conclusion'), 'created_at': run.get('created_at'), 'updated_at': run.get('updated_at'),
        'jobs': [{'id': j['id'], 'name': j['name'], 'labels': j.get('labels'), 'runner_name': j.get('runner_name'),
                  'status': j['status'], 'conclusion': j['conclusion'], 'started_at': j.get('started_at'),
                  'completed_at': j.get('completed_at'), 'seconds': _seconds(j.get('started_at'), j.get('completed_at')),
                  'steps': [{'name': s['name'], 'conclusion': s['conclusion'],
                             'seconds': _seconds(s.get('started_at'), s.get('completed_at'))} for s in j.get('steps', [])]}
                 for j in jobs],
        'billable': timing.get('billable'), 'artifacts': artifacts}
    dump(record, value)
    return value


def counted_minutes(artifacts: dict) -> dict:
    """Each job rounded up to a whole minute, macOS at ten times; GitHub's billable figures kept beside."""
    out, total = {}, 0
    for run_id, run in sorted(artifacts['runs'].items()):
        own = {}
        for job in run['jobs']:
            if job['seconds'] is None:
                continue
            setup = 0.0
            for step in job.get('steps', []):
                if step['name'].startswith('The run'):
                    break
                setup += step['seconds'] or 0.0
            os_name = 'MACOS' if any('macos' in label for label in job.get('labels') or []) else 'UBUNTU'
            own[job['name']] = {'os': os_name, 'seconds': job['seconds'], 'setup_seconds': setup,
                                'minutes': math.ceil(job['seconds'] / 60),
                                'counted': math.ceil(job['seconds'] / 60) * MULTIPLIER[os_name]}
        billable = sum(math.ceil(j['duration_ms'] / 60000) * MULTIPLIER[o]
                       for o, item in (run.get('billable') or {}).items() for j in item.get('job_runs', []))
        out[run_id] = {'jobs': own, 'counted_from_job_times': sum(v['counted'] for v in own.values()),
                       'counted_from_billable': billable}
        total += max(billable, out[run_id]['counted_from_job_times'])
    return {'runs': out, 'counted_total': total,
            'rule': 'per job, rounded up to the minute; macOS x10 (the larger of the two counts per run)'}


# --- compare ------------------------------------------------------------------------------------------------------

def _hashes(folder: Path) -> dict:
    """The job's own results-sha256.txt, every file checked against it."""
    listed = {}
    for line in (folder / 'results-sha256.txt').read_text().splitlines():
        digest, rel = line.split(None, 1)
        listed[rel.strip().removeprefix('./')] = digest
    bad = [rel for rel, digest in listed.items() if sha256_file(folder / rel) != digest]
    if bad:
        raise SystemExit(f'{folder}: files differ from results-sha256.txt: {bad[:5]}')
    return listed


def _load(folder: Path, rel: str, listed: dict | None):
    if listed is not None and rel not in listed:
        raise SystemExit(f'{folder / rel}: not among the job\'s hashed results')
    return json.loads((folder / rel).read_text())


def _fit(ref: dict, attempt_resources: dict | None, row: dict, executed_ok) -> dict:
    wall = (row.get('total_ms') or 0) / 1000
    peak = row.get('process_rss_peak_bytes') or 0
    return {'quantiles_sha256': row.get('quantiles_sha256'), 'reference_quantiles_sha256': ref['quantiles_sha256'],
            'bit_identical': row.get('quantiles_sha256') == ref['quantiles_sha256'] and not row.get('errors'),
            'payload_equal': row.get('result_payload_sha256') == ref['payload_sha256'],
            'executed_files_match_package': executed_ok(row.get('executed_files')),
            'wall_seconds': wall, 'peak_bytes': peak, 'within_ceilings': 0 < wall <= WALL and 0 < peak <= PEAK,
            'reference_wall_seconds': ref['total_ms'] / 1000, 'wall_ratio_to_reference': wall / (ref['total_ms'] / 1000),
            'node': row.get('node'), 'pyodide': row.get('pyodide'), 'blocked_non_local_requests': row.get('blocked_non_local_requests'),
            'resources': attempt_resources}


def _executed_check(files_sha256: dict):
    def ok(executed) -> bool:
        return bool(executed) and all(files_sha256.get(k) == v for k, v in executed.items())
    return ok


def checks_part(folder: Path, listed: dict | None) -> dict:
    run = _load(folder, 'checks-run.json', listed)
    gate = run['gate']
    machine = next(c for c in gate['checks'] if c['check'] == 'machine')
    canary = next(c for c in gate['checks'] if c['check'] == 'canary')
    pins = next(c for c in gate['checks'] if c['check'] == 'pins')
    return {'gate_passed': gate['passed'], 'pins_output': pins['output'], 'pins_seconds': pins['seconds'],
            'canary': {k: canary.get(k) for k in ('quantiles_sha256', 'expected_quantiles_sha256', 'seconds', 'payload_sha256')}
            | {'resources': canary['attempt'].get('resources')},
            'gate_seconds': sum(c['seconds'] for c in gate['checks']),
            'machine': {'kind': machine['kind'], 'image_version': machine['image_version'],
                        **{k: machine['described'].get(k) for k in ('system', 'machine', 'cpu_model', 'hardware_model',
                                                                    'cpu_count', 'physical_cores', 'memory_bytes', 'os_version')},
                        'image_os': machine['described']['runner_env'].get('ImageOS')},
            'forced': {name: {'failed_at': r['failed'], 'not_run': r['not_run'], 'issuance_called': r['issuance_called'],
                              'as_expected': r['as_expected'],
                              'problem': next(c['problems'] for c in r['checks'] if c['check'] == r['failed'])[:1]}
                       for name, r in run['forced'].items()},
            'all_forced_as_expected': all(r['as_expected'] for r in run['forced'].values()),
            'freeze_origin_store': run['freeze_origin_store']}


def machine_part(root_folder: Path, inputs: dict, executed_ok, listed_by: dict) -> dict:
    """One machine: its checks run and its two shadow blocks."""
    from .store import Store
    refs = inputs['references']
    out = {'checks': checks_part(root_folder / 'checks', listed_by.get('checks')), 'parity': {}, 'shadow': {}}
    parity = _load(root_folder / 'checks', 'parity.json', listed_by.get('checks'))
    for row in parity['stems']:
        out['parity'][row['stem']] = _fit(refs['runs']['parity'][row['stem']], row['attempt'].get('resources'), row, executed_ok)
    gates = {'checks': out['checks']['gate_passed']}
    for block, (first, last) in BLOCKS.items():
        folder = root_folder / f'shadow-{block}'
        if not (folder / 'shadow' / 'shadow.json').exists() and not (folder / 'shadow.json').exists():
            out['shadow'][block] = None
            continue
        base = folder / 'shadow' if (folder / 'shadow' / 'shadow.json').exists() else folder
        listed = listed_by.get(f'shadow-{block}')
        prefix = 'shadow/' if base != folder else ''
        record = _load(folder, f'{prefix}shadow.json', listed)
        gate = _load(folder, f'{prefix}checks.json', listed)
        gates[block] = gate['passed']
        head = Store(base / 'store').verify()
        days = {}
        for d in [first + timedelta(days=i) for i in range((last - first).days + 1)]:
            day_rec = _load(folder, f'{prefix}store/issued/{d}/record.json', listed)
            fits = {p: _fit(refs['runs']['shadow'][f'{p}-{d}'], day_rec['resources'].get(p) if p == 'A1' else None,
                            day_rec['runs'][p], executed_ok) for p in POLICIES}
            days[str(d)] = {
                'path': day_rec['path'], 'issued_policy': day_rec['issued_policy'], 'artifact_verifies': day_rec['artifact_verifies'],
                'buffers_equal_payload': all(day_rec['buffers_equal_payload'].values()),
                'buffers_equal_reference': day_rec['buffers_sha256'] == refs['shadow_buffers_sha256'][str(d)],
                'intake': day_rec['intake'], 'all_registered': all(v == 'registered' for v in day_rec['intake'].values()),
                'fits': fits, 'all_bit_identical': all(f['bit_identical'] for f in fits.values()),
                'day_seconds_sum': day_rec['process_seconds_sum'], 'issue_day_seconds': day_rec['issue_day_seconds'],
                'day_process_seconds': record['days'][str(d)]['process_seconds']}
            if d >= SPLIT:
                out['parity'][f'A1-{d}'] = fits['A1'] | {'from': f'the late block\'s issuance of {d}'}
        final_state = json.loads((base / 'store' / head['state_file']).read_text())
        from cp17.shadow import ShadowStates
        out['shadow'][block] = {'days': days, 'gate_passed': gate['passed'], 'gate_seconds': sum(c['seconds'] for c in gate['checks']),
                                'store_verifies': True, 'entries': head['entries'],
                                'final_digest': ShadowStates.from_dict(final_state).digest(), 'final_state': final_state}
    late, early = out['shadow'].get('late'), out['shadow'].get('early')
    summary = {'gates_passed': gates}
    if late:
        summary['late_final_equals_reference_final'] = late['final_digest'] == refs['shadow_final_sha256']
    if late and early:
        from .state import _carried
        start = json.loads((Path(inputs['tree']) / 'states' / f'start-{SPLIT}.json').read_text()) if inputs.get('tree') else None
        summary['stitch_early_final_equals_late_start'] = (start is not None and _carried(early['final_state']) == _carried(start))
    for block in (late, early):
        if block:
            block.pop('final_state')
    fits = [f for b in out['shadow'].values() if b for d in b['days'].values() for f in d['fits'].values()] + \
           [f for s, f in out['parity'].items() if 'from' not in f]
    days = [d for b in out['shadow'].values() if b for d in b['days'].values()]
    summary.update({
        'parity_origins': sorted(out['parity']), 'parity_all_bit_identical': all(f['bit_identical'] for f in out['parity'].values())
        and len(out['parity']) == 9,
        'fits': len(fits), 'fits_bit_identical': sum(f['bit_identical'] for f in fits),
        'all_payloads_equal': all(f['payload_equal'] for f in fits),
        'all_executed_files_match_package': all(f['executed_files_match_package'] for f in fits),
        'all_within_ceilings': all(f['within_ceilings'] for f in fits),
        'wall_seconds_max': max(f['wall_seconds'] for f in fits), 'peak_bytes_max': max(f['peak_bytes'] for f in fits),
        'wall_ratio_to_reference_median': statistics.median(f['wall_ratio_to_reference'] for f in fits),
        'blocked_non_local_requests': sorted({u for f in fits for u in f['blocked_non_local_requests'] or []}),
        'shadow_days': len(days), 'shadow_all_buffers_equal_reference': all(d['buffers_equal_reference'] for d in days),
        'shadow_all_buffers_equal_payload': all(d['buffers_equal_payload'] for d in days),
        'shadow_all_registered': all(d['all_registered'] for d in days),
        'shadow_all_issued_a1': all(d['issued_policy'] == 'A1' for d in days),
        'shadow_all_artifacts_verify': all(d['artifact_verifies'] for d in days),
        'shadow_all_fits_bit_identical': all(d['all_bit_identical'] for d in days)})
    if days:
        summary['cost'] = cost(out)
    out['summary'] = summary
    return out


def cost(part: dict) -> dict:
    """One issuance (A1 and the three shadows, one after another), and decision 23's four issuances with the
    canary: the gate (the four checks) plus four consecutive days, from the sequential issuances."""
    one = [d['day_process_seconds'] for b in part['shadow'].values() if b for d in b['days'].values()]
    fours = []
    for b in part['shadow'].values():
        if not b:
            continue
        seq = [d['day_process_seconds'] for d in b['days'].values()]
        fours += [b['gate_seconds'] + sum(seq[i:i + 4]) for i in range(len(seq) - 3)]
    return {'one_issuance_seconds': {'min': min(one), 'median': statistics.median(one), 'max': max(one)},
            'four_issuances_with_canary_seconds': {'min': min(fours), 'median': statistics.median(fours), 'max': max(fours)}
            if fours else None,
            'basis': 'each day\'s own process (load and check the store, release, issue A1 and three shadows, append), '
                     'one after another; the gate is the run\'s four checks, the canary included'}


def compare(inputs_path: Path, artifacts_path: Path | None, downloads: Path | None, local: Path | None, tree: Path | None) -> dict:
    root = Path('.')
    inputs = json.loads(inputs_path.read_text())
    inputs['tree'] = str(tree) if tree else None
    manifest = json.loads((root / 'docs/track-b/evidence/cp-17c/freeze-manifest.json').read_text())
    executed_ok = _executed_check(manifest['policy_identity']['code']['files_sha256'])
    out = {'schema': 'cp17c-measurement-v1', 'inputs_sha256': sha256_file(inputs_path),
           'policy_identity_sha256': manifest['policy_identity_sha256'], 'ceilings': {'wall_seconds': WALL, 'peak_bytes': PEAK},
           'reference': {'host_parity': 'reports/cp17b/host-parity.json', 'shadow_run': 'reports/cp17b/shadow-run.json',
                         'reports_sha256': inputs['references']['reports_sha256']}}
    if artifacts_path is not None:
        artifacts = json.loads(artifacts_path.read_text())
        out['artifacts_sha256'] = sha256_file(artifacts_path)
        out['minutes'] = counted_minutes(artifacts)
        run_id, run = max(artifacts['runs'].items(), key=lambda kv: kv[1]['created_at'])
        folder = downloads / run_id
        listed = {a['name']: _hashes(folder / a['name']) for a in run['artifacts']}
        mapping = {name: folder / name for name in listed}
        stage = downloads / 'by-kind'
        out['runner'] = machine_part_from(mapping, inputs, executed_ok, listed)
        out['runner']['run_id'] = run_id
        out['runner']['host'] = {name: _host_files(folder / name, listed[name]) for name in listed}
    if local is not None:
        out['local'] = machine_part(local, inputs, executed_ok, {})
    return out


def _host_files(folder: Path, listed: dict) -> dict:
    out = {}
    for rel in ('cpython.json', 'node-retrieval.json', 'package.json', 'inputs-verified.json', 'uv-retrieval.json'):
        if rel in listed:
            out[rel.removesuffix('.json')] = json.loads((folder / rel).read_text())
    return out


def machine_part_from(mapping: dict, inputs: dict, executed_ok, listed: dict) -> dict:
    """The runner's artifacts are one folder per job (checks, shadow-late, shadow-early), each with `results/`'s tree."""
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for name, folder in mapping.items():
            (tmp / name).symlink_to(folder / name if name == 'checks' and (folder / 'checks').is_dir() else folder)
        return machine_part(tmp, inputs, executed_ok, {k: {r.removeprefix(f'{k}/') if k == 'checks' else r: h
                                                           for r, h in v.items()} for k, v in listed.items()})


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    f = sub.add_parser('fetch')
    f.add_argument('--repo', required=True)
    f.add_argument('--run', required=True)
    f.add_argument('--dest', required=True, type=Path)
    f.add_argument('--record', required=True, type=Path)
    c = sub.add_parser('compare')
    c.add_argument('--inputs', required=True, type=Path)
    c.add_argument('--artifacts', type=Path)
    c.add_argument('--downloads', type=Path)
    c.add_argument('--local', type=Path)
    c.add_argument('--tree', type=Path, help='the scratch tree (for the late block\'s start state)')
    c.add_argument('--out', required=True, type=Path)
    args = ap.parse_args(argv)
    if args.cmd == 'fetch':
        value = fetch(args.repo, args.run, args.dest, args.record)
        print(len(value['runs'][args.run]['artifacts']), 'artifacts', value['runs'][args.run]['conclusion'])
        return 0
    value = compare(args.inputs, args.artifacts, args.downloads, args.local, args.tree)
    dump(args.out, value)
    for machine in ('runner', 'local'):
        if machine in value:
            s = value[machine]['summary']
            print(machine, {k: s[k] for k in ('parity_all_bit_identical', 'fits', 'fits_bit_identical', 'all_within_ceilings',
                                              'shadow_days', 'shadow_all_buffers_equal_reference', 'gates_passed')})
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
