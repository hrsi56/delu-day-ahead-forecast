"""CP-18e's rehearsal of decision 33's serving rule, end to end, on a development day (run locally).

**The day.** 2026-08-31, the dry run's first day: a wall clock of 2026-08-30 12:00 Berlin plans it alone. Every leg is a
fresh pipeline checkout set up as CP-18a's forced days set theirs up (`cp18.forced.setup`: a bare origin whose `main`
holds the candidate's tree and a store at CP-17b's host state before 2026-08-31, the hooks active), the live-input
builder replaying the recorded responses, the real H2 gate (the canary fit included) and `cp17.daily.issue_day` under the
frozen host. Nothing is retrieved from the network, nothing is pushed anywhere but the leg's own bare origin, and no day
after 2026-09-06 is planned (the development guard is in force throughout).

| Leg | Code | Serving rule (the pipeline's injection point, `serving=`) | Expected |
|---|---|---|---|
| `old` | `src/` at 5133b02c (extracted) | its own: CP-26's schedule | issued from S_13 |
| `new` | this candidate | its own: `cp18.serving.LIVE` | issued from S_13, the same day as `old` |
| `decision33` | this candidate | `Rule(scheduled)`, the schedule giving 2026-08-31 to S_14 | issued from S_13; the record names S_13 and decision 33 |
| `control` | this candidate | `scheduled` itself, a plain callable: the rule before decision 33 (as CP-18a's forced days) | open: "S_14's state not in place" |

**Compared.** `new` against `old` (nothing before S_14's day changes): the four payloads byte for byte, the artifact,
the day's record and the run's item for the day, except the run's own fields (its id, times and durations). The
artifact records its own attempt's wall time and peak memory (`resources`), so its hash differs between any two runs of
the same day; every other field of it, the forecast's `quantiles_sha256` included, must be equal. `decision33` against
`old`: the same payloads and the same artifact; the record differs only by `serving_rule` and the run's own fields.
The `old` leg runs in its own interpreter with `PYTHONPATH` at the code of 5133b02c, extracted by `git archive` and
checked against that commit's `src` tree hash; the candidate differs from it under `src/` in `src/cp18/` only.

    PYTHONPATH=src python -m cp18.serving_rehearsal --project /Users/djourno/Downloads/PJM --work <dir> \
        --out reports/cp18e/rehearsal.json
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

DAY = '2026-08-31'
NOW = '2026-08-30T12:00:00+02:00'
OLD = '5133b02c26dd1e369393362cedc524b8998d2e56'
LEGS = ('old', 'new', 'decision33', 'control')
BLAS = ('OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS')
#: The run's own fields in a record or a run's item: its id, its times and durations, the scratch paths of its leg, and
#: the artifact's hash, which covers the artifact's measured resources (below). Nothing else may differ.
RUN_FIELDS = ('run_id', 'run_started_utc', 'issuance_started_utc', 'issuance_finished_utc', 'process_seconds',
              'process_seconds_sum', 'issue_day_seconds', 'gate.started_utc', 'started_utc', 'seconds', 'timings',
              'inputs.timings', 'inputs.payloads', 'inputs.search.path', 'artifact_sha256')
#: The artifact's own measurements of its attempt (`cp17.issue`: wall time and peak memory), and its hash over them.
ARTIFACT_RUN_FIELDS = ('artifact_sha256', 'resources', 'attempts[0].resources', 'attempts[0].seconds')
#: The shadow fits' own measurements in a record (`cp17.daily`: each shadow's wall time and peak memory).
SHADOW_MEASURES = re.compile(r'^shadows\.[A-Za-z0-9]+\.(peak_bytes|wall_seconds)$')

#: One leg, in its own interpreter. It uses only what both codes have (`cp18.forced.setup`, `cp18.pipeline.run`).
LEG = r'''
import hashlib, json, shutil, sys
from datetime import date
from pathlib import Path
candidate, project, work, mode, out, day, now = sys.argv[1:8]
candidate, project, work, out, DAY = Path(candidate), Path(project), Path(work), Path(out), date.fromisoformat(day)
from cp18 import forced, pipeline, plan
from cp18.claim import Claim
from cp18.live_inputs import LiveInputs
from cp18.store import STORE_PATH, LiveStore
from cp26.search import serving_search

def scheduled(d):
    """The schedule, with the rehearsal's day given to S_14."""
    return 14 if d == DAY else serving_search(d)

kw = {}
if mode == 'decision33':
    from cp18.serving import Rule
    kw['serving'] = Rule(scheduled)
elif mode == 'control':
    kw['serving'] = scheduled
checkout = forced.setup(candidate, work)
inputs = LiveInputs(checkout, project, checkout / forced.RECORDED)
settings = pipeline.Settings(root=checkout, project=project, out=work / 'out', host_kind='local',
                             run_label=f'cp18e-{mode}')
record = pipeline.run(settings, plan.parse_now(now), claim=Claim(checkout), inputs=inputs, **kw)
store = LiveStore(checkout / STORE_PATH)
head = store.verify()
folder = checkout / STORE_PATH / 'issued' / day
payloads = settings.out / 'payloads' / day
summary = {'mode': mode, 'code': [p for p in sys.path if p.endswith('src')][:1],
           'run': {k: record.get(k) for k in ('planned', 'outcome', 'exit', 'days', 'closed')},
           'store_days': store.days(), 'store_head': head['entry_sha256'],
           'record': json.loads((folder / 'record.json').read_text()) if (folder / 'record.json').exists() else None,
           'artifact': json.loads((folder / 'artifact.json').read_text()) if (folder / 'artifact.json').exists() else None,
           'payload_files': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(payloads.glob('*'))}
                            if payloads.is_dir() else {},
           'origin_log': __import__('subprocess').run(['git', '-C', str(work / 'origin.git'), 'log', '--format=%an %s',
                                                       'main'], capture_output=True, text=True).stdout.splitlines()[:4]}
out.write_text(json.dumps(summary, indent=1, sort_keys=True, default=str) + '\n')
for name in ('seed', 'origin.git', 'checkout', 'out'):
    shutil.rmtree(work / name, ignore_errors=True)
'''


def _git(*args, cwd=None) -> str:
    done = subprocess.run(['git', *args], cwd=cwd, capture_output=True, text=True)
    if done.returncode:
        raise RuntimeError(f'git {args[0]}: {done.stderr.strip()[-400:]}')
    return done.stdout.strip()


def extract_old(candidate: Path, target: Path) -> dict:
    """`src/` at 5133b02c, by `git archive`, checked against that commit's tree hash for `src`."""
    target.mkdir(parents=True, exist_ok=True)
    archive = subprocess.run(['git', '-C', str(candidate), 'archive', OLD, 'src'], capture_output=True, check=True).stdout
    subprocess.run(['tar', '-x', '-C', str(target)], input=archive, check=True)
    probe = target / '.probe'
    shutil.rmtree(probe, ignore_errors=True)
    _git('init', '-q', str(probe))
    shutil.copytree(target / 'src', probe / 'src')
    _git('-C', str(probe), 'add', '-A')
    tree = _git('-C', str(probe), 'write-tree')
    sub = _git('-C', str(probe), 'rev-parse', f'{tree}:src')
    shutil.rmtree(probe)
    expected = _git('-C', str(candidate), 'rev-parse', f'{OLD}:src')
    if sub != expected:
        raise RuntimeError(f'the extracted src tree {sub} is not {OLD}:src {expected}')
    changed = _git('-C', str(candidate), 'diff', '--name-only', OLD, 'HEAD', '--', 'src').splitlines()
    return {'commit': OLD, 'src_tree': sub, 'src': str(target / 'src'),
            'candidate_src_changes': changed,
            'candidate_differs_under_src_only_in_cp18': all(p.startswith('src/cp18/') for p in changed)}


def run_leg(mode: str, candidate: Path, project: Path, work: Path, src: Path) -> dict:
    folder = work / mode
    folder.mkdir(parents=True, exist_ok=False)
    env = {k: v for k, v in os.environ.items() if k != 'PYTHONPATH'}
    env.update({'PYTHONPATH': str(src), 'CP17_PROJECT_ROOT': str(project), 'MLFLOW_DISABLE_TELEMETRY': 'true',
                'DO_NOT_TRACK': '1', **{n: '1' for n in BLAS}})
    out = work / f'{mode}.json'
    started = datetime.now()
    done = subprocess.run([sys.executable, '-c', LEG, str(candidate), str(project), str(folder), mode, str(out), DAY, NOW],
                          cwd=work, env=env, capture_output=True, text=True)
    seconds = (datetime.now() - started).total_seconds()
    if done.returncode or not out.exists():
        raise RuntimeError(f'leg {mode} failed (exit {done.returncode}): {done.stderr.strip()[-1500:]}')
    value = json.loads(out.read_text())
    value['wall_seconds'] = seconds
    return value


def diff(a, b, path: str = '') -> list[str]:
    """The dotted paths at which two JSON values differ."""
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for key in sorted(set(a) | set(b)):
            sub = f'{path}.{key}' if path else key
            out += [sub] if key not in a or key not in b else diff(a[key], b[key], sub)
        return out
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        return [p for i, (x, y) in enumerate(zip(a, b)) for p in diff(x, y, f'{path}[{i}]')]
    return [] if a == b else [path or '.']


def _run_field(path: str, fields=RUN_FIELDS) -> bool:
    if fields is RUN_FIELDS and SHADOW_MEASURES.match(path):
        return True
    return any(path == f or path.startswith(f + '.') or path.startswith(f + '[') for f in fields)


def compare(a: dict, b: dict) -> dict:
    """Two issued legs: payloads byte for byte, the artifact, the record and the run's item, the run's fields apart."""
    record = diff(a['record'], b['record'])
    item = diff(a['run']['days'][DAY], b['run']['days'][DAY])
    artifact = diff(a['artifact'], b['artifact'])
    return {'payload_files_equal': bool(a['payload_files']) and a['payload_files'] == b['payload_files'],
            'artifact_differs_at': [p for p in artifact if not _run_field(p, ARTIFACT_RUN_FIELDS)],
            'artifact_differs_at_run_fields': [p for p in artifact if _run_field(p, ARTIFACT_RUN_FIELDS)],
            'quantiles_sha256_equal': a['artifact']['quantiles_sha256'] == b['artifact']['quantiles_sha256'],
            'record_differs_at': [p for p in record if not _run_field(p)],
            'record_differs_at_run_fields': [p for p in record if _run_field(p)],
            'run_item_differs_at': [p for p in item if not _run_field(p)],
            'run_item_differs_at_run_fields': [p for p in item if _run_field(p)]}


def judge(legs: dict, project: Path) -> dict:
    from cp17 import runtime
    from . import causes, serving
    pinned = runtime.sha256_file(project / runtime.K13)
    old, new, d33, control = (legs[m] for m in LEGS)
    out = {'new_vs_old': compare(new, old), 'decision33_vs_old': compare(d33, old)}
    rule = (d33['record'] or {}).get('serving_rule') or {}
    search = ((d33['record'] or {}).get('inputs') or {}).get('search') or {}
    item = control['run']['days'].get(DAY) or {}
    checks = {
        'old_issued': old['run']['days'][DAY]['status'] == 'issued' and old['record'] is not None,
        'new_issued': new['run']['days'][DAY]['status'] == 'issued',
        'new_equals_old': not out['new_vs_old']['record_differs_at'] and not out['new_vs_old']['run_item_differs_at']
        and out['new_vs_old']['payload_files_equal'] and not out['new_vs_old']['artifact_differs_at']
        and out['new_vs_old']['quantiles_sha256_equal'],
        'new_record_has_no_serving_rule': 'serving_rule' not in (new['record'] or {}),
        'decision33_issued': d33['run']['days'][DAY]['status'] == 'issued',
        'decision33_built_from_s13': search.get('k') == 13 and search.get('file_sha256') == pinned
        and search.get('search_day') == '2026-07-08' and d33['artifact']['lineage']['training']['search'] == 13,
        'decision33_names_decision_33': rule.get('search') == 13 and rule.get('scheduled_search') == 14
        and rule.get('decision') == 33 and rule.get('text') == serving.TEXT,
        'decision33_same_payloads_and_forecast_as_old': out['decision33_vs_old']['payload_files_equal']
        and out['decision33_vs_old']['quantiles_sha256_equal'] and not out['decision33_vs_old']['artifact_differs_at'],
        'decision33_record_differs_only_by_serving_rule': out['decision33_vs_old']['record_differs_at'] == ['serving_rule']
        and out['decision33_vs_old']['run_item_differs_at'] == ['serving_rule'],
        'control_open_with_s14': item.get('status') == 'open' and item.get('cause') == causes.S14
        and item.get('cause_text') == "S_14's state not in place" and item.get('search') == 14
        and control['record'] is None and DAY not in control['store_days'] and control['run']['exit'] == 1,
    }
    out.update(checks=checks, as_expected=all(checks.values()), pinned_k13_sha256=pinned)
    return out


# ------------------------------------------------------------------ the live record's issued days, recomputed
#: What a recomputation may differ in from the issued record's `inputs`: its timings, its scratch paths, and the run's
#: own acquisitions (the original run acquired its archive day; a recomputation reads it and retrieves nothing).
LIVE_RUN_FIELDS = ('timings', 'payloads', 'search.path', 'acquired')

#: One code's recomputation of the live record's issued days, in its own interpreter, from a scratch copy of `live/`.
#: It uses only what both codes have; the serving search is each code's own (`cp18.serving.LIVE` where it exists,
#: CP-26's schedule at 5133b02c).
LIVE_LEG = r'''
import hashlib, json, sys
from datetime import date
from pathlib import Path
candidate, project, live, out = (Path(p) for p in sys.argv[1:5])
from cp17.shadow import ShadowStates
from cp18 import boundary
from cp18.live.transport import Transport, TransportError
from cp18.live_inputs import LiveInputs
from cp18.store import LiveStore
try:
    from cp18.serving import LIVE as rule
except ImportError:
    from cp26.search import serving_search as rule

class NoNetwork(Transport):
    def send(self, request):
        raise TransportError('CP-18e recomputes from the committed archive only; nothing is retrieved')

class Inputs(LiveInputs):
    @property
    def archive_root(self):
        return live / 'inputs'

store = LiveStore(live / 'store')
head = store.verify()
ledger = store.entries()
days = {}
with boundary.live():
    inputs = Inputs(candidate, project, None, transport=NoNetwork())
    for i, entry in enumerate(ledger):
        if entry['kind'] != 'issuance':
            continue
        day = entry['day']
        d = date.fromisoformat(day)
        state = ShadowStates.from_dict(json.loads((store.folder / ledger[i - 1]['state_file']).read_text()))
        state.release(d, inputs.truth(d))
        k = rule(d)
        folder = out.parent / (out.stem + '-payloads') / day
        built = inputs.build(d, buffers={p: state.buffer(p) for p in ('v4', 'v2', 'B0')},
                             search_file=Path(inputs.search_file(k)), out=folder)
        built.pop('payloads', None)
        days[day] = {'serving': k, 'built': built,
                     'files': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(folder.glob('*'))}}
out.write_text(json.dumps({'store_head': head['entry_sha256'], 'days': days}, indent=1, sort_keys=True,
                          default=str) + '\n')
'''


#: Decision 31's label in a build's availability (CP-18d): absent from the records CP-18c's code wrote.
LABEL_FIELDS = ('input_class', 'input_class_text', 'load_forecast_copy', 'load_forecast_fetched_utc')
MISSING = '<absent>'


def _at(value, path: str):
    """The value at a dotted path (`a.b[0].c`), or MISSING."""
    for part in re.findall(r'[^.\[\]]+|\[\d+\]', path):
        if part.startswith('['):
            i = int(part[1:-1])
            if not isinstance(value, list) or i >= len(value):
                return MISSING
            value = value[i]
        elif isinstance(value, dict) and part in value:
            value = value[part]
        else:
            return MISSING
    return value


def _explained(record: dict, path: str, held, recomputed) -> str | None:
    """Why a recomputed day's inputs differ from its issued record there, or None if no known reason applies."""
    if (record.get('schema') == 'cp18a-day-record-v1' and held == MISSING
            and path in {f'availability.{f}' for f in LABEL_FIELDS}):
        return "decision 31's label (CP-18d), which this CP-18c record predates"
    if isinstance(held, str) and isinstance(recomputed, str):
        try:
            same = datetime.fromisoformat(held.replace('Z', '+00:00')) == datetime.fromisoformat(recomputed)
        except ValueError:
            same = False
        if same:
            return 'the same instant, written ...Z in the record and ...+00:00 now (CP-18c\'s notation)'
    return None


def _live_leg(name: str, src: Path, candidate: Path, project: Path, work: Path) -> dict:
    live = work / f'{name}-live'
    shutil.copytree(candidate / 'live', live)
    env = {k: v for k, v in os.environ.items() if k != 'PYTHONPATH'}
    env.update({'PYTHONPATH': str(src), 'CP17_PROJECT_ROOT': str(project), 'MLFLOW_DISABLE_TELEMETRY': 'true',
                'DO_NOT_TRACK': '1', **{n: '1' for n in BLAS}})
    out = work / f'{name}.json'
    started = datetime.now()
    done = subprocess.run([sys.executable, '-c', LIVE_LEG, str(candidate), str(project), str(live), str(out)],
                          cwd=work, env=env, capture_output=True, text=True)
    if done.returncode or not out.exists():
        raise RuntimeError(f'live leg {name} failed (exit {done.returncode}): {done.stderr.strip()[-1500:]}')
    value = json.loads(out.read_text())
    value['wall_seconds'] = (datetime.now() - started).total_seconds()
    return value


def live_days(candidate: Path, project: Path, work: Path, refit: str | None) -> dict:
    """Every issued day of the live record, recomputed locally from what the store holds, by the code at 5133b02c and by
    this candidate: the state before the day (its ledger), D−2's release and the day's four payloads from the committed
    archive, and the serving search under each code's own rule. Nothing is retrieved (every request is refused), and
    nothing is written under `live/`: each leg reads its own scratch copy. Compared: the two codes byte for byte (the
    payload files and the build's record of the inputs), and each against the issued record's `inputs`. Optionally,
    A1's fit of one day again under the frozen host, from the candidate's payload, against the issued artifact."""
    from cp17 import daily, runtime
    from cp26.search import serving_search as schedule
    from datetime import date
    from .host import PACKAGE_ZIP
    from .store import LiveStore
    old = extract_old(candidate, work / 'old-src')
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = {'old': pool.submit(_live_leg, 'old', Path(old['src']), candidate, project, work),
                   'new': pool.submit(_live_leg, 'new', candidate / 'src', candidate, project, work)}
        legs = {m: f.result() for m, f in futures.items()}
    store = LiveStore(work / 'new-live' / 'store')
    pinned = runtime.sha256_file(project / runtime.K13)
    days, problems = {}, []
    for entry in store.entries():
        if entry['kind'] != 'issuance':
            continue
        day = entry['day']
        record = json.loads((store.folder / entry['record_file']).read_text())
        held, o, n = record['inputs'], legs['old']['days'][day], legs['new']['days'][day]
        item = {'schedule': schedule(date.fromisoformat(day)), 'serving_old': o['serving'], 'serving_new': n['serving'],
                'record_search': held['search']['k'], 'record_search_file_sha256': held['search']['file_sha256'],
                'record_has_serving_rule': 'serving_rule' in record,
                'new_vs_old_files_equal': bool(n['files']) and n['files'] == o['files'],
                'new_vs_old_built_differs_at': [p for p in diff(n['built'], o['built'])
                                                if not _run_field(p, LIVE_RUN_FIELDS)],
                'payload_sha256_equal_to_record': n['built'].get('payload_sha256') == held['payload_sha256'],
                'new_vs_record_differs_at': [p for p in diff(held, {k: n['built'].get(k) for k in held})
                                             if not _run_field(p, LIVE_RUN_FIELDS)]}
        # Each difference from the issued record, with both values and why: the record was written by an earlier code
        # (CP-18c's records lack decision 31's label, which CP-18d added), or the same instant in another notation.
        item['new_vs_record_values'] = {p: {'record': _at(held, p), 'recomputed': _at(n['built'], p),
                                            'explained': _explained(record, p, _at(held, p), _at(n['built'], p))}
                                        for p in item['new_vs_record_differs_at']}
        item['as_expected'] = (item['schedule'] == item['serving_old'] == item['serving_new'] == item['record_search']
                               == 13 and item['record_search_file_sha256'] == pinned
                               and item['new_vs_old_files_equal'] and not item['new_vs_old_built_differs_at']
                               and item['payload_sha256_equal_to_record'] and not item['record_has_serving_rule']
                               and all(v['explained'] for v in item['new_vs_record_values'].values()))
        if refit == day:
            artifact = json.loads((store.folder / entry['artifact_file']).read_text())
            host = daily.Host(project / runtime.PYODIDE_DIR, project / PACKAGE_ZIP)
            run = host.run(work / 'new-payloads' / day, f'A1-{day}', work / 'refit')
            result = (run.get('python') or {}).get('result') or {}
            issued = [m['params_sha256'] for m in artifact['lineage']['training']['members']]
            item['refit'] = {'errors': [str(e)[-300:] for e in run.get('errors') or []],
                             'issued_policy': artifact['issued_policy'],
                             'quantiles_sha256': result.get('quantiles_sha256'),
                             'artifact_quantiles_sha256': artifact['quantiles_sha256'],
                             'members_params_equal': [m['params_sha256'] for m in result.get('members', [])] == issued}
            item['refit']['equal'] = (not item['refit']['errors'] and item['refit']['members_params_equal']
                                      and result.get('quantiles_sha256') == artifact['quantiles_sha256'])
            item['as_expected'] = item['as_expected'] and item['refit']['equal']
        days[day] = item
        if not item['as_expected']:
            problems.append(day)
    return {'schema': 'cp18e-live-days-v1', 'candidate': _git('-C', str(candidate), 'rev-parse', 'HEAD'),
            'old_code': old, 'store_head': legs['new']['store_head'], 'store_head_old_leg': legs['old']['store_head'],
            'pinned_k13_sha256': pinned, 'days': days, 'issued_days': len(days),
            'leg_seconds': {m: v['wall_seconds'] for m, v in legs.items()},
            'as_expected': bool(days) and not problems, 'not_as_expected': problems}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog='python -m cp18.serving_rehearsal')
    ap.add_argument('--candidate', default=Path('.'), type=Path)
    ap.add_argument('--project', required=True, type=Path)
    ap.add_argument('--work', required=True, type=Path)
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--parallel', default=2, type=int)
    ap.add_argument('--live-days', action='store_true', help="recompute the live record's issued days instead")
    ap.add_argument('--refit', default=None, help='with --live-days: refit A1 for this issued day')
    args = ap.parse_args(argv)
    candidate, project, work = args.candidate.resolve(), args.project.resolve(), args.work.resolve()
    if work.exists() and any(work.iterdir()):
        raise SystemExit(f'{work} is not empty')
    # Every leg clones the candidate's HEAD when it starts and imports its `src/`: both must stay one commit throughout
    head = _git('-C', str(candidate), 'rev-parse', 'HEAD')
    if _git('-C', str(candidate), 'status', '--porcelain=v1', '--untracked-files=no', '--', 'src'):
        raise SystemExit(f'{candidate}: src/ differs from HEAD; commit or run from a clean checkout')
    work.mkdir(parents=True, exist_ok=True)
    started = datetime.now()

    def unmoved():
        if _git('-C', str(candidate), 'rev-parse', 'HEAD') != head:
            raise SystemExit(f'{candidate}: HEAD moved from {head} during the run; its record is void')

    if args.live_days:
        record = live_days(candidate, project, work, args.refit)
        unmoved()
        record['seconds'] = (datetime.now() - started).total_seconds()
        shutil.rmtree(work, ignore_errors=True)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(record, indent=1, sort_keys=True, default=str) + '\n')
        for day, item in record['days'].items():
            print(day, 'as expected' if item['as_expected'] else 'NOT AS EXPECTED', item.get('refit', {}).get('equal', ''))
        print('as expected:', record['as_expected'])
        return 0 if record['as_expected'] else 1
    old = extract_old(candidate, work / 'old-src')
    sources = {'old': Path(old['src']), 'new': candidate / 'src', 'decision33': candidate / 'src',
               'control': candidate / 'src'}
    with ThreadPoolExecutor(max_workers=max(1, min(args.parallel, 4))) as pool:
        futures = {m: pool.submit(run_leg, m, candidate, project, work, sources[m]) for m in LEGS}
        legs = {m: f.result() for m, f in futures.items()}
    unmoved()
    record = {'schema': 'cp18e-serving-rehearsal-v1', 'candidate': head,
              'day': DAY, 'wall_clock': NOW, 'old_code': old, 'legs': legs, **judge(legs, project),
              'seconds': (datetime.now() - started).total_seconds(),
              'leg_seconds_sum': sum(v['wall_seconds'] for v in legs.values())}
    shutil.rmtree(work / 'old-src', ignore_errors=True)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(record, indent=1, sort_keys=True, default=str) + '\n')
    for name, ok in record['checks'].items():
        print(f'{name}: {ok}')
    print('as expected:', record['as_expected'])
    return 0 if record['as_expected'] else 1


if __name__ == '__main__':
    sys.exit(main())
