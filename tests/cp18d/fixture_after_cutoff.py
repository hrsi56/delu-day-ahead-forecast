"""A TEST FIXTURE, never a record: a copy of a live store in which one issued day is relabelled as issued with its load
forecast fetched after the cutoff (the Owner's decision 31), its ledger re-chained so that the copy verifies.

Why it exists. No live day has been issued with the copy fetched after the cutoff yet (decision 31 starts with CP-18d's
LAND), and nothing here may retrieve live data or write under `live/`. The Space's surfaces and the bundle's
evaluation per input class still need a realistic store to render: the committed live record, with one day's record
rewritten as CP-18d's pipeline writes a day issued with that copy. Its artifact, forecast and state are untouched; only
its day record (the label and its availability evidence) changes, and every later ledger entry's hash is recomputed by
CP-17c's own formula (`cp17c.store._canonical`). The copy is used by tests and local acceptance only, and every file
it writes says so (`FIXTURE`).

    PYTHONPATH=src python tests/cp18d/fixture_after_cutoff.py --live <copy of live/> --day 2026-11-14 \
        --fetched 2026-11-13T10:47:12Z
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from cp17c.store import _canonical, _sha_bytes, _write
from cp18 import inputclass
from cp18.store import STORE_PATH, LiveStore

FIXTURE = ('TEST FIXTURE (CP-18d): this day record was rewritten from a day issued with every input before the cutoff, '
           'to render a day issued with the load forecast fetched after the cutoff; it is not a record of the live '
           'product')


def relabel(live: Path, day: str, fetched_utc: str) -> dict:
    """Rewrite `day`'s record in the store copy under `live` (its `store/`), re-chain the ledger, verify."""
    folder = Path(live) / 'store'
    if (Path(live).resolve().parent / '.git').exists():
        raise SystemExit('refused: the fixture rewrites a copy of the live record, never a checkout\'s own live/')
    lines = (folder / 'ledger.jsonl').read_text().splitlines()
    entries = [json.loads(line) for line in lines]
    index = next(i for i, e in enumerate(entries) if e.get('kind') == 'issuance' and e['day'] == day)
    rel = entries[index]['record_file']
    record = json.loads((folder / rel).read_text())
    lf = inputclass.required_load_forecast(record)
    if lf is None:
        raise SystemExit(f'{day}: its record holds no availability evidence to rewrite')
    lf.update(admitted=False, fetched_after_cutoff=True, fetched_utc=fetched_utc,
              publication_utc=fetched_utc, basis_id='retrieval_time',
              reason=f"published {fetched_utc}, not strictly before the cutoff {lf.get('cutoff_utc')}",
              used="decision 31: D's load forecast fetched after the cutoff", fixture=FIXTURE)
    record['inputs']['availability']['load_forecast_copy'] = {'record': lf.get('record'), 'fetched_utc': fetched_utc,
                                                             'cutoff_utc': lf.get('cutoff_utc'), 'fixture': FIXTURE}
    record.update(schema=inputclass.RECORD_SCHEMA, fixture=FIXTURE,
                  **inputclass.label(inputclass.AFTER, fetched_utc))
    inputclass.of_record(record)                                    # the rewritten record must be a valid one
    entries[index]['record_file_sha256'] = _write(folder / rel, record)
    for i in range(index, len(entries)):
        entry = {k: v for k, v in entries[i].items() if k != 'entry_sha256'}
        entry['previous_entry_sha256'] = entries[i - 1]['entry_sha256'] if i else None
        entry['entry_sha256'] = _sha_bytes(_canonical(entry))
        entries[i] = entry
    (folder / 'ledger.jsonl').write_text(''.join(json.dumps(e, sort_keys=True, allow_nan=False) + '\n'
                                                 for e in entries))
    head = json.loads((folder / 'head.json').read_text())
    head['entry_sha256'] = entries[-1]['entry_sha256']
    _write(folder / 'head.json', head)
    LiveStore(folder).verify()
    return {'day': day, 'fetched_utc': fetched_utc, 'record_file': rel, 'fixture': FIXTURE}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--live', required=True, type=Path, help='a COPY of the live record (its store/ is rewritten)')
    ap.add_argument('--day', required=True)
    ap.add_argument('--fetched', required=True, help='the copy\'s retrieval time, UTC, after the day\'s cutoff')
    args = ap.parse_args(argv)
    print(json.dumps(relabel(args.live, args.day, args.fetched)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
