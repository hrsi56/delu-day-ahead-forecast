"""Physical route partition of the frozen CP26 search API; no model overrides."""
from pathlib import Path
import json
import hashlib
import subprocess
import sys
import fcntl
from contextlib import contextmanager


@contextmanager
def route_lease(directory, route):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / f'search-{route}.lock').open('a+b') as handle:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise RuntimeError(f'route search already owned: {route}') from error
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def require_custody(root):
    path = Path(__file__).resolve()
    relative = str(path.relative_to(root))
    raw = path.read_bytes()
    if subprocess.check_output(['git', 'show', f'HEAD:{relative}'], cwd=root) != raw:
        raise RuntimeError('route execution caller must be committed before fitting')
    return {'path': relative, 'sha256': hashlib.sha256(raw).hexdigest()}


def run(root, route, budget=None):
    if route not in ('nominal', 'noload', 'gfs6'):
        raise ValueError('route must be one of the three frozen CP26 routes')
    from cp26 import harness as H
    root = Path(root).resolve()
    caller = require_custody(root)
    with route_lease(H.art() / 'cold-rerun-2026-10-15' / 'route-leases', route):
        return run_owned(root, route, caller, budget)


def run_owned(root, route, caller, budget):
    from cp26 import execution as E, search as S, gates as G
    from cp26.budget import Budget
    G.authorize_consuming_process(root)
    protocol = G.protocol_identity(root)
    gate = G.ExecutionGate(root)
    gate('search')
    paths = E.Paths.build(root)
    manifest = E.manifest_for(paths, protocol)
    budget = budget or Budget()
    results = []
    for k in range(S.SEARCH_COUNT):
        gate('search')
        S.execute_search(root, paths.plan(route, k), paths.trial_cache(route, k), paths.result(route, k))
        result = E.terminal_search(paths, route, k, manifest)
        E.record_evidence_once(budget, f'search/{E.digest(protocol)}/{route}/{k}',
            {'result_sha256': result['content_sha256'], 'status': result['status']},
            {'completed_search_results': 1, 'unavailable_search_results': int(result['status'] == 'unavailable')})
        results.append({'k': k, 'status': result['status'], 'content_sha256': result['content_sha256']})
        print(json.dumps({'status': 'REGISTERED_SEARCH_TERMINAL', 'route': route, **results[-1]}), flush=True)
    value = E._signed({'schema': 'cp26-route-search-completion-v1', 'status': 'ROUTE_SEARCHES_COMPLETE',
                       'route': route, 'protocol': protocol, 'caller': caller,
                       'searches': len(results), 'results': results})
    return E._immutable(paths.output / 'route-search-completion' / f'{route}.json', value)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('supply exactly one frozen route')
    sys.path.insert(0, str(Path.cwd() / 'src'))
    print(json.dumps(run(Path.cwd(), sys.argv[1])), flush=True)
