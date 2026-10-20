"""Physical callers of frozen CP-26 daily APIs; no scientific overrides.

Every invocation is one monitored worker, not a subprocess orchestrator.
Route fits use bounded chronological windows and write only their native cache.
One replay owner consumes a ready prefix; missing caches never trigger a fit in
cache-only mode. Prefits are not daily issuances or a discount to their budget.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager, ExitStack
from datetime import date
import fcntl
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROUTES = ('nominal', 'noload', 'gfs6')
SCHEMA = 'cp26-daily-physical-phase-v1'


@contextmanager
def lease(directory, name):
    """Nonblocking OS lock; process exit releases it without deleting evidence."""
    if name not in ('replay', *(f'fit-{route}' for route in ROUTES)):
        raise ValueError('unregistered daily lease identity')
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / f'daily-{name}.lock').open('a+b') as handle:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise RuntimeError(f'daily execution already owned: {name}') from error
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def require_custody(root):
    """The exact physical caller must be committed before it can consume data."""
    root, path = Path(root).resolve(), Path(__file__).resolve()
    relative = str(path.relative_to(root))
    raw = path.read_bytes()
    committed = subprocess.check_output(['git', 'show', f'HEAD:{relative}'], cwd=root)
    if raw != committed:
        raise RuntimeError('daily execution caller must be committed before fitting or replay')
    return {'path': relative, 'sha256': hashlib.sha256(raw).hexdigest()}


def _check_caller(root, expected):
    if require_custody(root) != expected:
        raise RuntimeError('daily execution caller custody changed during invocation')


class GuardedCache:
    """Use the original FitCache validator and one fresh gate per route/origin.

    A read-only miss raises before fit_members_cached can enter its fitting
    branch. A failed entry is a terminal native result, never a miss or retry.
    """
    def __init__(self, cache, gate, *, readonly, custody=None):
        self.wrapped, self.gate, self.readonly = cache, gate, bool(readonly)
        self.custody = custody
        self.route, self.identity, self.base = cache.route, cache.identity, cache.base
        self.last_guarded_day = None

    def path(self, day, member):
        return self.wrapped.path(day, member)

    def load(self, day, member, index, issue_utc, *, ensemble=None):
        if day != self.last_guarded_day:
            if self.custody is not None:
                self.custody()
            # Full admission is checked by _setup and run_forecasts at each
            # bounded phase boundary. Match the production calendar driver:
            # retain the existing live resource/ownership/source gate per day
            # without reparsing every historical search and issuance per fit.
            self.gate('prepare')
            self.last_guarded_day = day
        result = self.wrapped.load(day, member, index, issue_utc, ensemble=ensemble)
        if result is None:
            if self.readonly:
                raise RuntimeError(f'cache-only replay lacks native result: {self.route}/{day}/{member}')
        return result

    def save(self, *args, **kwargs):
        if self.readonly:
            raise RuntimeError('cache-only replay may not save or fit a native member')
        return self.wrapped.save(*args, **kwargs)


def _setup(root, budget):
    from cp26 import execution as E, gates as G
    from cp26.budget import Budget
    budget = budget or Budget()
    G.authorize_consuming_process(root)
    protocol = G.protocol_identity(root)
    gate = G.ExecutionGate(root, budget=budget)
    E._gate(gate, 'forecast', fitting=True)
    paths = E.Paths.build(root)
    return budget, protocol, gate, paths, E.manifest_for(paths, protocol)


def _phase(paths, mode, caller, protocol, manifest, detail, budget):
    """Deterministic immutable terminal evidence; supervisor alone charges time."""
    from cp26 import execution as E
    _check_caller(paths.root, caller)
    value = E._signed({'schema': SCHEMA, 'status': 'COMPLETE', 'mode': mode,
                       'caller': caller, 'protocol': protocol,
                       'execution_manifest_sha256': manifest['content_sha256'], **detail})
    phase_id = E.digest({'mode': mode, 'caller': caller, 'protocol': protocol,
                         'route': detail.get('route'), 'first': detail.get('first'), 'through': detail['through']})
    path = paths.output / 'daily-physical-completion' / f'{mode}-{phase_id}.json'
    E._immutable(path, value)
    E.record_evidence_once(budget, f'physical-daily/{phase_id}',
                          {'phase_sha256': value['content_sha256'], 'path': str(path.relative_to(paths.root))})
    return value


def fit_route(root, route, first, through, *, budget=None):
    """Exactly one route/cache owner; explicit dates never alter training windows."""
    from cp26 import execution as E, harness as H
    if route not in ROUTES:
        raise ValueError('fit route must be nominal, noload or gfs6')
    days = E.calendar(first, through)
    root = Path(root).resolve()
    caller = require_custody(root)
    with lease(H.art() / 'cold-rerun-2026-10-15/route-leases', f'fit-{route}'):
        return _fit_route_owned(root, route, days, caller, budget)


def _fit_route_owned(root, route, days, caller, budget):
    from cp26 import execution as E, harness as H, search as S
    from cp26.members import Context, RUN_MEMBERS
    from cp26.fits import FitCache, frozen_fit_identity, fit_members_cached
    budget, protocol, gate, paths, manifest = _setup(root, budget)
    # Validate every serving result needed by this bounded window before the
    # first native fit. No absent search is treated as scientific unavailability.
    ensembles = {k: E.terminal_search(paths, route, k, manifest)
                 for k in sorted({S.serving_search(day) for day in days}-{None})}
    context = Context.build(root, H.GFS6 if route == 'gfs6' else H.NEW, route)
    original = FitCache(paths.local / 'fits', route, frozen_fit_identity(context, protocol))
    cache = GuardedCache(original, gate, readonly=False,
                         custody=lambda: _check_caller(root, caller))
    records = []
    for day in days:
        # Revalidate the serving result so an interrupted/replaced terminal
        # search cannot be silently relied on after admission of a long window.
        k = S.serving_search(day)
        ensemble = E.terminal_search(paths, route, k, manifest) if k is not None else None
        if k is not None and ensemble != ensembles[k]:
            raise RuntimeError('bounded native fit serving search changed after admission')
        fits = fit_members_cached(context, day, cache, ensemble=ensemble, k=k)
        if set(fits) != set(RUN_MEMBERS[route]):
            raise RuntimeError('native route cache omitted a registered member')
        evidence = {'day': str(day), 'search': k,
                    'ensemble_sha256': E.digest(ensemble) if ensemble is not None else None,
                    'members': {name: {'status': fits[name]['status'],
                                       'cache_content_sha256': fits[name]['cache_content_sha256']}
                                for name in RUN_MEMBERS[route]}}
        # The immutable phase below preserves every native cache hash. Do not
        # duplicate this growing metadata in the hot resource ledger or claim an
        # issuance before chronological replay. Supervisors retain actual time.
        records.append(evidence)
        print(json.dumps({'status': 'NATIVE_ROUTE_CACHE_READY', 'route': route, 'day': str(day)}), flush=True)
    return _phase(paths, 'fit-route', caller, protocol, manifest,
                  {'route': route, 'first': str(days[0]), 'through': str(days[-1]),
                   'fit_identity': original.identity, 'days': records,
                   'daily_issuances_claimed': False, 'forecast_outputs_created': False}, budget)


def replay_cached(root, through, *, budget=None):
    return _replay(root, through, readonly=True, budget=budget)


def serial_slice(root, through, *, budget=None):
    return _replay(root, through, readonly=False, budget=budget)


def _replay(root, through, *, readonly, budget):
    from cp26 import execution as E, harness as H
    E.calendar(last=through)
    root = Path(root).resolve()
    caller = require_custody(root)
    with ExitStack() as locks:
        directory = H.art() / 'cold-rerun-2026-10-15/route-leases'
        locks.enter_context(lease(directory, 'replay'))
        if not readonly:
            # Same lease names as route prefits. All are nonblocking and unwind
            # together, so serial mode cannot steal a cache from a route worker.
            for route in ROUTES:
                locks.enter_context(lease(directory, f'fit-{route}'))
        return _replay_owned(root, through, readonly, caller, budget)


def _replay_owned(root, through, readonly, caller, budget):
    from cp26 import execution as E, scoring as S
    from cp26.state import ReplayState
    budget, protocol, gate, paths, manifest = _setup(root, budget)
    population = S.load_population(root)
    keys = population.keys_by_day()
    population.verify_key_mapping(keys)
    contexts, originals = E.contexts_and_caches(paths, protocol)
    caches = {route: GuardedCache(originals[route], gate, readonly=readonly,
                                 custody=lambda: _check_caller(root, caller)) for route in ROUTES}
    result = E.run_forecasts(root, protocol, keys, gate=gate, through=through,
                             budget=budget, contexts=contexts, caches=caches)
    saved = ReplayState.load(paths.state(protocol), protocol) if paths.state(protocol).exists() else \
            ReplayState.load(paths.output / 'replay-state.json', protocol)
    E._validate_state_calendar(saved)
    if saved.last_origin != through:
        raise RuntimeError('physical replay did not complete its requested chronological prefix')
    ledger = []
    for day in E.calendar(last=through):
        value = E._read(paths.day(day))
        if value.get('policies') != {name: policy.records[str(day)] for name, policy in saved.policies.items()}:
            raise RuntimeError('physical replay completion differs from original saved issuance')
        ledger.append({'day': str(day), 'content_sha256': value['content_sha256']})
    return _phase(paths, 'replay-cached' if readonly else 'serial-slice', caller, protocol, manifest,
                  {'through': str(through), 'replay_state_sha256': saved.to_dict()['content_sha256'],
                   'ledger': ledger, 'slice': result, 'cache_only': bool(readonly)}, budget)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='mode', required=True)
    fitting = commands.add_parser('fit-route')
    fitting.add_argument('route', choices=ROUTES)
    fitting.add_argument('first', type=date.fromisoformat)
    fitting.add_argument('through', type=date.fromisoformat)
    replay = commands.add_parser('replay-cached')
    replay.add_argument('through', type=date.fromisoformat)
    serial = commands.add_parser('serial-slice')
    serial.add_argument('through', type=date.fromisoformat)
    args = parser.parse_args(argv)
    root = Path.cwd()
    if args.mode == 'fit-route':
        value = fit_route(root, args.route, args.first, args.through)
    elif args.mode == 'replay-cached':
        value = replay_cached(root, args.through)
    else:
        value = serial_slice(root, args.through)
    print(json.dumps(value, sort_keys=True), flush=True)


if __name__ == '__main__':
    sys.path.insert(0, str(Path.cwd() / 'src'))
    main()
