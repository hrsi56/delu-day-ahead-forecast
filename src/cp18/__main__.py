"""The pipeline's commands, the same on the runner and on the Owner's Mac (`cp18.local` wraps them in one command).

    PYTHONPATH=src python -m cp18 prepare --root . --project . --retrieve-node --out <file>
    PYTHONPATH=src python -m cp18 run --root . --project . --out <dir> --host runner --now <ISO> \
        --inputs prebuilt:<payload folder> | live:<recorded responses> [--remote origin]
    PYTHONPATH=src python -m cp18 init-store --root . --state <file> --origin <day> --first-day <day> --source <text>
    PYTHONPATH=src python -m cp18 status --root .

**This round runs dry runs only** (`--mode dry-run`, the default and the only mode accepted): development days through
2026-09-06, with `--now` required, so the plan is computed from a simulated wall clock and never from today's. The red
line refuses any plan past the boundary in any case. CP-18's activation adds the live mode and the schedule.

The run's exit code: 0 done (or nothing to do, or a lost claim, which is a correct outcome); 1 a day was not issued;
2 refused before issuing, or the publication was refused; 3 the red line.
"""
from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import sys

BLAS = ('OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS')


def _dump(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=1, sort_keys=True, allow_nan=False, default=str) + '\n')


def _check_blas() -> None:
    import os
    if any(os.environ.get(n) != '1' for n in BLAS):
        raise SystemExit('export the five *_NUM_THREADS=1 before NumPy loads, as the freeze ran')


def make_inputs(spec: str, root: Path, project: Path):
    kind, _, where = spec.partition(':')
    if kind == 'prebuilt':
        from .inputs import PrebuiltInputs
        return PrebuiltInputs(root, project, Path(where))
    if kind == 'live':
        from .live_inputs import LiveInputs
        return LiveInputs(root, project, Path(where))
    raise SystemExit(f'--inputs {spec!r}: expected prebuilt:<folder> or live:<recorded responses>')


def cmd_prepare(args) -> int:
    from . import host
    root, project = args.root.resolve(), args.project.resolve()
    record = {'materialized': host.materialize(root, project) if args.materialize else None,
              'node': host.node(project, args.retrieve_node), 'package': host.package(root, project)}
    _dump(args.out, record)
    print('prepare:', 'pinned files', len(record['materialized'] or {}), '| node',
          (record['node'].get('binary') or {}).get('sha256', 'in place')[:16], '| package',
          'equal' if record['package']['equal_to_manifest'] else 'NOT EQUAL', flush=True)
    return 0 if record['package']['equal_to_manifest'] else 1


def cmd_run(args) -> int:
    _check_blas()
    from . import pipeline, plan
    from .claim import Claim
    if args.mode != 'dry-run':
        raise SystemExit('this round runs dry runs only; CP-18\'s activation adds the live mode')
    root, project, out = args.root.resolve(), args.project.resolve(), args.out.resolve()
    now = plan.parse_now(args.now)
    settings = pipeline.Settings(root=root, project=project, out=out, host_kind=args.host, mode=args.mode,
                                 run_label=args.run_label or '')
    record = pipeline.run(settings, now, claim=Claim(root, remote=args.remote, branch=args.branch),
                          inputs=make_inputs(args.inputs, root, project))
    _dump(out / 'run.json', record)
    print('run', record['run_id'], '|', record['outcome'], '|', 'planned', record['planned'], flush=True)
    for day, item in record['days'].items():
        print(' ', day, item.get('status'), item.get('policy') or item.get('cause_text') or '',
              f"{item.get('seconds', 0):.0f}s", flush=True)
    for item in record['closed']:
        print('  closed', item['day'], 'not issued:', item['cause_text'], flush=True)
    return record['exit']


def cmd_init_store(args) -> int:
    from cp17.shadow import ShadowStates
    from .store import STORE_PATH, LiveStore
    state = ShadowStates.from_dict(json.loads(args.state.read_text()))
    store = LiveStore.init(args.root / STORE_PATH, state, date.fromisoformat(args.origin), args.source,
                           date.fromisoformat(args.first_day))
    print('store', store.folder, 'head', store.verify()['entry_sha256'][:16])
    return 0


def cmd_status(args) -> int:
    from .store import STORE_PATH, LiveStore
    store = LiveStore(args.root / STORE_PATH)
    head = store.verify()
    print(json.dumps({'head': head, 'days': store.days(), 'runs': len(store.runs())}, indent=1, sort_keys=True))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog='python -m cp18')
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('prepare')
    p.add_argument('--root', default=Path('.'), type=Path)
    p.add_argument('--project', default=Path('.'), type=Path)
    p.add_argument('--materialize', action='store_true', help='copy the committed pinned files into .local/ by hash')
    p.add_argument('--retrieve-node', action='store_true', help='retrieve the official binary by hash (the runner)')
    p.add_argument('--out', required=True, type=Path)
    r = sub.add_parser('run')
    r.add_argument('--root', default=Path('.'), type=Path)
    r.add_argument('--project', default=Path('.'), type=Path)
    r.add_argument('--out', required=True, type=Path)
    r.add_argument('--host', choices=('runner', 'local'), required=True)
    r.add_argument('--mode', default='dry-run')
    r.add_argument('--now', required=True, help='the simulated wall clock of a dry run, with its offset')
    r.add_argument('--inputs', required=True)
    r.add_argument('--remote', default='origin')
    r.add_argument('--branch', default='main')
    r.add_argument('--run-label')
    i = sub.add_parser('init-store')
    i.add_argument('--root', default=Path('.'), type=Path)
    i.add_argument('--state', required=True, type=Path)
    i.add_argument('--origin', required=True)
    i.add_argument('--first-day', required=True)
    i.add_argument('--source', required=True)
    s = sub.add_parser('status')
    s.add_argument('--root', default=Path('.'), type=Path)
    args = ap.parse_args(argv)
    return {'prepare': cmd_prepare, 'run': cmd_run, 'init-store': cmd_init_store, 'status': cmd_status}[args.cmd](args)


if __name__ == '__main__':
    sys.exit(main())
