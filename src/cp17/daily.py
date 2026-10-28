"""The daily issuance on the issuing host: the frozen chain, the shadow issuances, and the issued artifact.

This is the driver CP-18's pipeline calls once per delivery day, after the day's payloads are built. It is part
of the frozen policy identity (CP-17's review, N1), though it runs natively, because it starts the issuing host.

- **Each attempt** runs the package's own fit (`host/driver.py`, fit mode) in a fresh Pyodide process under the
  pinned Node.js (decision 10). Each attempt has a fresh output path, so no earlier record can be read as its
  result, and a timeout equal to the success definition's wall-time ceiling. A process that is killed, times
  out, dies without a record, or leaves an unreadable or mismatched record is a failed fit, and the chain moves
  on. Its measured wall time and peak resident memory judge criterion 5 (`cp17.issue.attempt`).
- **The chain** is `cp17.issue.decide` with the artifact built and verified inside it (criterion 4, N3).
- **The shadows** (decision 14). After the chain, v4, v2 and B0 are fitted for the same day if the chain did not
  already fit them. They are registered in their own states (`cp17.shadow.ShadowStates`) and never published.
- **The native comparison** (`comparison_day`) runs the same chain in-process with criterion 5 not judged. It is
  labelled as the comparison and can never issue (N2).
"""
from __future__ import annotations

from datetime import date
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time

from . import dailyfit, issue
from .shadow import POLICIES as SHADOW_POLICIES

NODE = '/opt/homebrew/Cellar/node/26.7.0/bin/node'
RUNNER = Path(__file__).resolve().parent / 'host' / 'node_run.mjs'
#: The pinned Pyodide 0.28.0 packages the package's import closure needs (the lock adds their dependencies).
PACKAGES = ('numpy', 'pandas', 'scikit-learn', 'lightgbm', 'requests', 'tzdata')
TIMEOUT_SECONDS = issue.WALL_LIMIT_SECONDS


class Host:
    """The issuing host: the pinned Node.js, the pinned Pyodide folder and the frozen package's zip."""

    def __init__(self, pyodide: Path, package_zip: Path, node: str = NODE, timeout: float = TIMEOUT_SECONDS):
        self.pyodide, self.package_zip, self.node, self.timeout = Path(pyodide), Path(package_zip), node, timeout

    def run(self, payloads: Path, stem: str, out: Path) -> dict:
        """One attempt in a fresh process, with a fresh output path. Never raises: a failure is in `errors`."""
        out.mkdir(parents=True, exist_ok=True)
        folder = Path(tempfile.mkdtemp(prefix=f'{stem}-', dir=out))
        target = folder / 'run.json'
        command = [self.node, str(RUNNER), 'fit', str(self.pyodide), str(self.package_zip), str(payloads), stem, '1',
                   ','.join(PACKAGES), str(target)]
        started = time.perf_counter()
        try:
            proc = subprocess.run(command, capture_output=True, text=True, timeout=self.timeout,
                                  env={**os.environ, 'CP17_EXPORT': '1'})
        except subprocess.TimeoutExpired:
            return {'target': stem, 'errors': [f'the attempt timed out after {self.timeout} s and was killed'],
                    'total_ms': (time.perf_counter() - started) * 1000, 'process_rss_peak_bytes': 0, 'folder': str(folder)}
        wall_ms = (time.perf_counter() - started) * 1000
        if not target.exists():
            return {'target': stem, 'errors': [f'the attempt left no record (exit {proc.returncode})'],
                    'total_ms': wall_ms, 'process_rss_peak_bytes': 0, 'folder': str(folder)}
        try:
            run = json.loads(target.read_text())
        except (OSError, ValueError) as exc:
            return {'target': stem, 'errors': [f'the attempt left an unreadable record ({type(exc).__name__})'],
                    'total_ms': wall_ms, 'process_rss_peak_bytes': 0, 'folder': str(folder)}
        if run.get('target') != stem or run.get('mode') != 'fit':
            return {'target': stem, 'errors': ['the attempt left a record of another run'], 'total_ms': wall_ms,
                    'process_rss_peak_bytes': 0, 'folder': str(folder)}
        run['folder'] = str(folder)
        run['driver_wall_ms'] = wall_ms
        return run


def _paths(payloads: Path, policy: str, day: date) -> tuple[Path | None, Path]:
    npz = payloads / f'{policy}-{day}.npz'
    return (npz if npz.exists() else None), payloads / f'{policy}-{day}.json'


def issue_day(day: date, gfs_available: bool, payloads: Path, *, host: Host, out: Path, identity: dict,
              parent_sha256: str | None = None, data_refresh_utc: str = '', states=None) -> dict:
    """The day's issuance under the issuing host, then the shadows; registers every fit in `states` if given."""
    payloads, out = Path(payloads), Path(out)
    started = time.perf_counter()
    runs, inputs = {}, {}

    def host_run(policy):
        if policy not in runs:
            runs[policy] = host.run(payloads, f'{policy}-{day}', out)
        return runs[policy]

    def attempts(policy):
        npz, meta = _paths(payloads, policy, day)
        arrays, value = dailyfit.load(npz, meta)
        inputs[policy] = {'payload_sha256': value.get('payload_sha256')}

        def fit():
            run = host_run(policy)
            if run.get('errors'):
                raise dailyfit.FitFailure(run['errors'][0][-2000:])
            return run['python']['result']

        def measured():
            run = runs[policy]
            return {'wall_seconds': run['total_ms'] / 1000, 'peak_bytes': int(run['process_rss_peak_bytes'])}
        return issue.attempt(policy, fit, day, arrays, value, resources=measured)

    def finalize(decision):
        run = runs[decision['issued_policy']]
        host_identity = {'runtime': 'pyodide', 'pyodide': run.get('pyodide_version'), 'node': run.get('node'),
                         'process': 'one fresh process per attempt'}
        return issue.artifact(decision, identity=identity, payloads=inputs, parent_sha256=parent_sha256,
                              data_refresh_utc=data_refresh_utc, host=host_identity)

    decision = issue.decide(day, gfs_available, attempts, finalize)
    issued_seconds = time.perf_counter() - started
    shadows = {}
    for policy in SHADOW_POLICIES:
        if policy == 'B0' and not _paths(payloads, 'B0', day)[1].exists():
            continue
        run = host_run(policy)
        result = None if run.get('errors') else run['python']['result']
        shadow = {'fitted_by': 'chain' if any(a['policy'] == policy and a['status'] != 'skipped'
                                              for a in decision['attempts']) else 'shadow',
                  'status': 'failed' if result is None else 'ok', 'errors': run.get('errors', []),
                  'wall_seconds': run['total_ms'] / 1000, 'peak_bytes': int(run.get('process_rss_peak_bytes') or 0),
                  'quantiles_sha256': result['quantiles_sha256'] if result else None}
        if states is not None:
            shadow['intake'] = states.issue(policy, day, result)
        shadows[policy] = shadow
    return {'day': str(day), 'gfs_available': gfs_available, 'decision': decision, 'artifact': decision.get('artifact'),
            'shadows': shadows, 'runs': runs, 'issued_seconds': issued_seconds,
            'total_seconds': time.perf_counter() - started}


def comparison_day(day: date, gfs_available: bool, payloads: Path) -> dict:
    """The same chain natively, in-process, criterion 5 not judged: labelled as the comparison; it never issues."""
    payloads = Path(payloads)

    def attempts(policy):
        npz, meta = _paths(payloads, policy, day)
        arrays, value = dailyfit.load(npz, meta)
        return issue.attempt(policy, lambda: dailyfit.run(policy, npz, meta, attribution=True), day, arrays, value)
    started = time.perf_counter()
    decision = issue.decide(day, gfs_available, attempts)
    decision.update(comparison=True, seconds=time.perf_counter() - started)
    return decision
