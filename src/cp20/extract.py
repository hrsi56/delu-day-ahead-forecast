"""Resumable CP-20 GFS extraction job (extraction environment, run under the monitor).

Usage: python -m cp20.extract --manifest M --out DIR --select subset|all [--workers N]
                              [--stop-transfer-gib G] [--inventory-added]

* One exclusive lock per output directory; a second instance exits immediately.
* Every target message attempt is appended (and fsynced) to ``attempts.jsonl`` and
  charged to the ledger *before* its requests are sent. Production uses at most two
  attempts per message; the third is reserved for independent review. Owner decision O1
  adds up to two production attempts only where pre-run testing consumed attempts; those
  are also logged in ``prerun_replacement_attempts.jsonl`` and a separate ledger counter.
* A run is complete only when its ``runs/<run>.json`` exists with status ``complete`` and
  its ``runs/<run>.npz`` matches the recorded sha256; completed runs are re-validated
  and reused on resume, never refetched. Partial runs are discarded, their attempts kept.
* Exit codes: 0 all selected runs complete; 2 stopped/partial (signal or stop line);
  4 material contradiction with admission (evidence written, task must stop);
  5 finished with runs that failed after the bounded attempts (classified, not imputed).
"""
from __future__ import annotations

import argparse
import datetime as dt
import fcntl
import json
import os
from pathlib import Path
import signal
import sys
import threading
import time
from collections import deque

import numpy as np

from .budget import Budget, CapExceeded, GIB, atomic
from .gfs import (FIELDS, GROUPS, LEADS, BOX_LATS, BOX_LONS, Contradiction, IntegrityError, NcarLocator,
                  OffsetModel, aws_url, check_frame, decode, ncar_url, parse_idx, sha, version,
                  version_evidence)
from .net import Fetcher, NetworkError, TransferError

# Section 15.5: 3 attempts per target message including retries and review. Production uses at
# most 2, so every message keeps one attempt for independent review (r5 reverted).
PRODUCTION_ATTEMPTS = 2
# Owner decision O1 (2026-09-23, in session): up to two additional production attempts per target
# message whose allowance was consumed by pre-run testing (subset jobs 3, 11 and 12, i.e. every
# attempt logged before the full extraction job started), logged separately; no other cap change.
PRERUN_CUTOFF_EPOCH = 1790184500.409214  # start_epoch of gfs-extract job index 16 (--select all)
PRERUN_REPLACEMENT_MAX = 2
# Observed pgrb2.0p25 .idx objects are ~33 KB (admission inventory); the bound is charged up front.
IDX_BOUND = 100_000
_decode_lock = threading.Lock()


def _date(s):
    return dt.date.fromisoformat(s)


class Attempts:
    def __init__(self, path: Path, budget: Budget):
        self.path, self.budget, self.lock = path, budget, threading.Lock()
        self.replacements = path.with_name('prerun_replacement_attempts.jsonl')
        self.counts, self.prerun = {}, {}
        if path.exists():
            for line in path.read_text().splitlines():
                r = json.loads(line)
                key = (r['run'], r['lead'], r['field'])
                self.counts[key] = self.counts.get(key, 0) + 1
                if r['epoch'] < PRERUN_CUTOFF_EPOCH:
                    self.prerun[key] = self.prerun.get(key, 0) + 1

    def used(self, run, lead):
        return max(self.counts.get((run, lead, f), 0) for f in FIELDS)

    def extra(self, run, lead):
        """Owner-approved O1 allowance: replaces attempts consumed by pre-run testing, at most two."""
        return min(PRERUN_REPLACEMENT_MAX, max(self.prerun.get((run, lead, f), 0) for f in FIELDS))

    def begin(self, run, lead, endpoint, purpose):
        with self.lock:
            used, extra = self.used(run, lead), self.extra(run, lead)
            if used >= PRODUCTION_ATTEMPTS + extra:
                raise IntegrityError(f'{run} f{lead:03d}: production attempt allowance exhausted')
            replacement = used >= PRODUCTION_ATTEMPTS
            if replacement:
                purpose = f'owner_approved_prerun_replacement:{purpose}'
                self.budget.reserve(message_attempts=len(FIELDS), prerun_replacement_attempts=len(FIELDS))
            else:
                self.budget.reserve(message_attempts=len(FIELDS))
            with self.path.open('a') as fh:
                for field in FIELDS:
                    key = (run, lead, field)
                    self.counts[key] = self.counts.get(key, 0) + 1
                    record = {'run': run, 'lead': lead, 'field': field, 'endpoint': endpoint,
                              'attempt': self.counts[key], 'purpose': purpose, 'epoch': time.time()}
                    fh.write(json.dumps(record) + '\n')
                    if replacement:
                        with self.replacements.open('a') as rf:
                            rf.write(json.dumps({**record, 'prerun_attempts': self.prerun.get(key, 0),
                                                 'owner_decision': 'O1'}) + '\n')
                fh.flush()
                os.fsync(fh.fileno())


def priors(admission: Path) -> dict:
    """Learned-offset priors from the admission's decoded samples (read-only)."""
    out = {}
    names = {'u10': 'u10', 'ssrd': 'dswrf', 'u_hub': 'u100'}
    for path in sorted((admission / 'decoded').glob('gfs_*.json')):
        d = json.loads(path.read_text())
        run = _date(path.stem[4:])
        for key, rec in d['leads'].items():
            lead = int(key[1:])
            size = rec['source'].get('file_bytes') or d.get('comparisons', {}).get('ncar_vs_aws', {}).get(key, {}).get('aws_bytes')
            if not size:
                continue
            for src, anchor in names.items():
                f = rec['fields'].get(src)
                if f:
                    out.setdefault((version(run), lead, anchor), []).append((run, f['byte_range'][0] / size))
    return out


class Extractor:
    def __init__(self, args, budget):
        self.args, self.budget = args, budget
        self.out = Path(args.out)
        (self.out / 'runs').mkdir(parents=True, exist_ok=True)
        self.fetcher = Fetcher(budget, self.out / 'requests.jsonl', int(args.stop_transfer_gib * GIB))
        self.attempts = Attempts(self.out / 'attempts.jsonl', budget)
        model_path = self.out / 'offset_model.json'
        learned = {}
        if model_path.exists():
            for item in json.loads(model_path.read_text())['observations']:
                learned.setdefault(tuple(item['key']), []).append((_date(item['run']), item['frac']))
        self.model = OffsetModel(priors(Path(args.admission)), learned)
        self.locator = NcarLocator(self.fetcher, self.model)
        self.stop = threading.Event()
        self.drain = threading.Event()
        self.reason = None
        self.lock = threading.Lock()
        self.progress = {'complete': 0, 'reused': 0, 'failed': [], 'started_epoch': time.time()}
        self.network_failures = []

    # ------------------------------------------------------------ completion / resume
    def completed(self, run):
        meta, arrays = self.out / 'runs' / f'{run}.json', self.out / 'runs' / f'{run}.npz'
        if not meta.exists():
            return False
        record = json.loads(meta.read_text())
        if record.get('status') != 'complete' or not arrays.exists():
            return False
        if sha(arrays.read_bytes()) != record['npz_sha256']:
            bad = self.out / 'invalid'
            bad.mkdir(exist_ok=True)
            stamp = int(time.time())
            meta.rename(bad / f'{run}.{stamp}.json')
            arrays.rename(bad / f'{run}.{stamp}.npz')
            self.budget.event('invalid_completed_run_quarantined', run=run)
            return False
        return True

    # ------------------------------------------------------------ one (run, lead)
    def _aws_lead(self, run, lead, rec):
        url = aws_url(run, lead)
        _, _, idx = self.fetcher.get(url + '.idx', f'aws idx {run} f{lead:03d}', max_body=IDX_BOUND)
        size = rec['object_bytes'][f'f{lead:03d}'].get('aws')
        found = parse_idx(idx.decode('utf8', 'replace'), run, lead, size)
        messages, spans = {}, []
        for field in sorted(FIELDS, key=lambda f: found[f]['offset']):
            o, e = found[field]['offset'], found[field]['end']
            if spans and spans[-1][1] + 1 == o:
                spans[-1][1] = e
                spans[-1][2].append(field)
            else:
                spans.append([o, e, [field]])
        for o, e, group in spans:
            _, _, blob = self.fetcher.get(url, f'aws {run} f{lead:03d} {"+".join(group)}', byte_range=(o, e))
            for field in group:
                a, b = found[field]['offset'] - o, found[field]['end'] - o + 1
                messages[field] = (blob[a:b], {'url': url, 'byte_range': [found[field]['offset'], found[field]['end']],
                                               'idx_line': found[field]['idx_line'], 'idx_sha256': sha(idx)})
        return messages

    def _ncar_size(self, run, lead, rec):
        size = rec['object_bytes'][f'f{lead:03d}'].get('ncar')
        if size:
            return size
        _, headers, _ = self.fetcher.get(ncar_url(run, lead), f'ncar size {run} f{lead:03d}', byte_range=(0, 0))
        return int(headers['Content-Range'].rpartition('/')[2])

    def _ncar_lead(self, run, lead, rec):
        url, size = ncar_url(run, lead), self._ncar_size(run, lead, rec)
        messages, trace = {}, []
        for group in GROUPS:
            located, window = self.locator.find_group(url, run, lead, size, group, trace)
            first, blob, reused = self.locator.payload(url, run, lead, located, window,
                                                       f'ncar {run} f{lead:03d} {"+".join(group)}')
            for field in group:
                loc = located[field]
                messages[field] = (blob[loc.offset - first: loc.offset - first + loc.length],
                                   {'url': url, 'byte_range': [loc.offset, loc.offset + loc.length - 1],
                                    'file_bytes': size, 'window_bytes_reused': reused})
        return messages, trace

    def _lead(self, run, lead, rec, endpoint, purpose):
        self.attempts.begin(run.isoformat(), lead, endpoint, purpose)
        trace = None
        if endpoint == 'aws':
            messages = self._aws_lead(run, lead, rec)
        else:
            messages, trace = self._ncar_lead(run, lead, rec)
        out = {}
        for field in FIELDS:
            msg, source = messages[field]
            check_frame(msg, source['byte_range'][1] - source['byte_range'][0] + 1)
            with _decode_lock:
                meta, box, quantum = decode(msg, run, lead, field)
            evidence = version_evidence(run, field, meta, endpoint, source['url'])
            out[field] = (msg, box, {'field': field, 'lead': lead, 'endpoint': endpoint, **source,
                                     'bytes': len(msg), 'sha256': sha(msg), 'packing_quantum': quantum,
                                     'retrieved_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                                     'version_evidence': evidence, 'purpose': purpose,
                                     'meta': {k: v for k, v in meta.items() if v is not None}})
        self.budget.reserve(decoded_messages=len(FIELDS))
        return out, trace

    # ------------------------------------------------------------ one run
    def run(self, rec):
        run = _date(rec['run_00z'])
        key = rec['run_00z']
        if self.stop.is_set():
            return
        if self.completed(key):
            with self.lock:
                self.progress['reused'] += 1
            return
        began = time.time()
        data = np.full((len(FIELDS), len(LEADS), len(BOX_LATS), len(BOX_LONS)), np.nan)
        records, traces, failures = [], {}, []
        raw = self.out / 'raw' / key
        for j, lead in enumerate(LEADS):
            if self.stop.is_set():
                return  # partial run discarded; attempts already recorded
            result = None
            endpoint, purpose = rec['primary_endpoint'], 'production'
            alternate_used = False
            while True:
                try:
                    result, trace = self._lead(run, lead, rec, endpoint, purpose)
                    if trace is not None:
                        traces[f'f{lead:03d}'] = trace
                    break
                except (IntegrityError, TransferError) as exc:
                    failures.append({'lead': lead, 'endpoint': endpoint, 'purpose': purpose, 'error': str(exc)[:300],
                                     'kind': type(exc).__name__})
                    if 'allowance exhausted' in str(exc):
                        break
                    if isinstance(exc, NetworkError):
                        # A network stall is not an object failure: retry the same endpoint on a fresh
                        # connection; a burst of network failures halts (resumable) before attempts burn.
                        if self._network_failure():
                            return
                        purpose = 'transient_retry'
                    elif rec['alternate_endpoint'] and not alternate_used:
                        endpoint, purpose, alternate_used = rec['alternate_endpoint'], 'alternate_endpoint', True
                    else:
                        purpose = 'transient_retry'
                    continue
                except Contradiction as exc:
                    self._halt('contradiction', {'run': key, 'lead': lead, 'endpoint': endpoint, 'error': str(exc)})
                    return
                except CapExceeded as exc:
                    self._halt('cap_or_stop_line', {'run': key, 'lead': lead, 'error': str(exc)})
                    return
            if result is None:
                self._failed_run(rec, failures, began)
                return
            for i, field in enumerate(FIELDS):
                msg, box, record = result[field]
                data[i, j] = box
                if rec['retain_raw']:
                    raw.mkdir(parents=True, exist_ok=True)
                    (raw / f'f{lead:03d}_{field}_{record["endpoint"]}.grib2').write_bytes(msg)
                    record['raw_retained'] = True
                records.append(record)
        arrays = self.out / 'runs' / f'{key}.npz'
        tmp = arrays.with_name(f'{key}.tmp.npz')
        np.savez_compressed(tmp, data=data, lats=BOX_LATS, lons=BOX_LONS, fields=np.array(FIELDS),
                            leads=np.array(LEADS))
        os.replace(tmp, arrays)
        atomic(self.out / 'runs' / f'{key}.json', {
            'status': 'complete', 'run_00z': key, 'delivery_day': rec['delivery_day'], 'version': version(run),
            'npz_sha256': sha(arrays.read_bytes()), 'messages': records, 'failed_attempts': failures,
            'locate_traces': traces, 'elapsed_s': round(time.time() - began, 2),
            'nonfinite_box_values': int((~np.isfinite(data)).sum()),
            'written_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())})
        with self.lock:
            self.progress['complete'] += 1
            self._save_progress()
        print(key, 'complete', round(time.time() - began, 1), 's', flush=True)

    def _network_failure(self, window=600.0, limit=5):
        now = time.time()
        with self.lock:
            self.network_failures = [t for t in self.network_failures if now - t < window] + [now]
            burst = len(self.network_failures) >= limit
        if burst:
            self._halt('network_degraded', {'failures_in_window': len(self.network_failures), 'window_s': window})
        return burst

    def _failed_run(self, rec, failures, began):
        path = self.out / 'failures.jsonl'
        entry = {'run': rec['run_00z'], 'class': 'extraction_failed_after_bounded_attempts',
                 'imputable': False, 'failures': failures, 'elapsed_s': round(time.time() - began, 1)}
        with self.lock:
            with path.open('a') as fh:
                fh.write(json.dumps(entry) + '\n')
            self.progress['failed'].append(rec['run_00z'])
            self._save_progress()
        print(rec['run_00z'], 'FAILED', failures[-1:], flush=True)

    def _halt(self, reason, evidence):
        with self.lock:
            if self.reason is None:
                self.reason = reason
                atomic(self.out / f'halt-{int(time.time())}.json', {'reason': reason, **evidence})
        self.stop.set()
        print('HALT', reason, evidence, flush=True)

    def _save_progress(self):
        atomic(self.out / 'offset_model.json', {'observations': self.model.observations()})
        atomic(self.out / 'progress.json', {**self.progress, 'requests': self.fetcher.stats,
                                            'updated_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())})


def inventory_added(extractor, runs):
    """Targeted pre-fit listing checks for the eight runs admission did not inventory."""
    path = extractor.out / 'added_inventory.jsonl'
    done = {json.loads(l)['run'] for l in path.read_text().splitlines()} if path.exists() else set()
    import re
    for rec in runs:
        key = rec['run_00z']
        if key in done:
            continue
        run = _date(key)
        ymd = run.strftime('%Y%m%d')
        entry = {'run': key, 'aws_files': {}, 'aws_idx': {}, 'ncar_files': {}}
        for pre in ('f02', 'f03', 'f04'):
            prefix = f'gfs.{ymd}/00/atmos/gfs.t00z.pgrb2.0p25.{pre}'
            _, _, body = extractor.fetcher.get(f'https://noaa-gfs-bdp-pds.s3.amazonaws.com/?list-type=2&prefix={prefix}',
                                               f'added inventory aws listing {key} {pre}', max_body=2_000_000)
            for obj, size in re.findall(r'<Key>([^<]+)</Key>.*?<Size>(\d+)</Size>', body.decode('utf8', 'replace'), re.S):
                m = re.search(r'\.f(\d{3})(\.idx)?$', obj)
                if m and int(m.group(1)) in LEADS:
                    (entry['aws_idx'] if m.group(2) else entry['aws_files'])[f'f{m.group(1)}'] = int(size)
        _, _, body = extractor.fetcher.get(
            f'https://tds.gdex.ucar.edu/thredds/catalog/files/g/d084001/{run.year}/{ymd}/catalog.xml',
            f'added inventory ncar catalog {key}', max_body=3_000_000)
        for m in re.finditer(r'<dataset name="gfs\.0p25\.(\d{10})\.f(\d{3})\.grib2".*?<dataSize units="Mbytes">([\d.]+)</dataSize>\s*<date type="modified">([^<]+)</date>',
                             body.decode('utf8', 'replace'), re.S):
            init, lead, mb, mod = m.groups()
            if init == ymd + '00' and int(lead) in LEADS:
                entry['ncar_files'][f'f{lead}'] = {'mbytes': float(mb), 'modified': mod}
        entry['aws_complete'] = len(entry['aws_files']) == 10 and len(entry['aws_idx']) == 10
        entry['ncar_complete'] = len(entry['ncar_files']) == 10
        with path.open('a') as fh:
            fh.write(json.dumps(entry, sort_keys=True) + '\n')
        for lead in LEADS:
            size = entry['aws_files'].get(f'f{lead:03d}')
            if size:
                rec['object_bytes'][f'f{lead:03d}']['aws'] = size
        print('added inventory', key, entry['aws_complete'], entry['ncar_complete'], flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--manifest', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--admission', required=True)
    ap.add_argument('--select', default='subset')
    ap.add_argument('--workers', type=int, default=int(os.environ.get('CP20_WORKERS', '1')))
    ap.add_argument('--stop-transfer-gib', type=float, default=150.0)
    ap.add_argument('--inventory-added', action='store_true')
    ap.add_argument('--endpoint', choices=['aws', 'ncar'], required=True,
                    help='one endpoint per job: concurrent AWS and NCAR bulk flows collapse the AWS flow on this link')
    args = ap.parse_args()
    if not 1 <= args.workers <= 4 or args.workers > int(os.environ.get('CP20_WORKERS', args.workers)):
        raise SystemExit('workers must be within the monitor-declared allowance (<=4)')
    budget = Budget(os.environ['CP20_LEDGER'])
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    lock = (out / 'extract.lock').open('a')
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise SystemExit('another extraction instance holds this output directory')
    manifest = json.loads(Path(args.manifest).read_text())
    runs = manifest['runs']
    if args.select == 'subset':
        runs = [r for r in runs if r['subset']]
    elif args.select != 'all':
        wanted = set(args.select.split(','))
        runs = [r for r in runs if r['run_00z'] in wanted]
    # Single-endpoint jobs (r8): diagnosis showed that an AWS range collapses to a trickle while
    # an NCAR bulk flow is active on this link, although either endpoint alone is healthy. Runs
    # are processed in date order (which also keeps NCAR offset predictions local).
    runs = sorted((r for r in runs if r['primary_endpoint'] == args.endpoint), key=lambda r: r['run_00z'])
    queue = deque(runs)
    ex = Extractor(args, budget)

    def on_signal(signum, _frame):
        # First stop request drains: no new run starts, in-flight runs finish and are saved.
        # A second request stops immediately (partial runs discarded, never imputed).
        ex.reason = ex.reason or f'signal_{signum}'
        if ex.drain.is_set():
            ex.stop.set()
        ex.drain.set()
    signal.signal(signal.SIGTERM, on_signal)
    signal.signal(signal.SIGINT, on_signal)
    added = [r for r in runs if not r['admission']['inventoried']]
    if added and args.inventory_added:
        inventory_added(ex, added)
    elif added:
        raise SystemExit('added runs require --inventory-added targeted checks first')
    print(f'extraction start: {len(runs)} {args.endpoint} runs, workers={args.workers}', flush=True)
    qlock = threading.Lock()

    def lane(_):
        while not ex.stop.is_set() and not ex.drain.is_set():
            with qlock:
                if not queue:
                    return
                rec = queue.popleft()
            try:
                ex.run(rec)
            except Exception as exc:  # noqa: BLE001 - an unexpected worker error halts cleanly
                ex._halt('worker_error', {'run': rec['run_00z'], 'error': repr(exc)})
    threads = [threading.Thread(target=lane, args=(k,), daemon=True) for k in range(args.workers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    ex._save_progress()
    done = [r['run_00z'] for r in runs if ex.completed(r['run_00z'])]
    summary = {'selected': len(runs), 'complete': len(done), 'failed': sorted(set(ex.progress['failed'])),
               'halt_reason': ex.reason, 'requests_this_invocation': ex.fetcher.stats,
               'finished_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
    summary['drained'] = ex.drain.is_set() and not ex.stop.is_set()
    atomic(out / f'summary-{args.select if args.select in ("subset", "all") else "custom"}-{args.endpoint}.json', summary)
    print(json.dumps(summary), flush=True)
    if ex.reason == 'contradiction':
        return 4
    if ex.reason is not None:
        return 2
    if summary['failed']:
        return 5
    return 0 if len(done) == len(runs) else 2


if __name__ == '__main__':
    sys.exit(main())
