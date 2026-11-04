"""The data-only record logs (`cp18.records`): append-only, hash-chained, each file written once."""
from __future__ import annotations

import json

import pytest

from cp18.records import LogRefused, RecordLog


def test_append_and_verify(tmp_path):
    log = RecordLog(tmp_path)
    a = log.append('k', 'a.json', {'x': 1})
    b = log.append('k', 'b/b.json', {'y': [1, 2]}, extra='field')
    assert log.verify() == [a, b]
    assert b['previous_entry_sha256'] == a['entry_sha256'] and b['extra'] == 'field'
    assert log.read(b) == {'y': [1, 2]} and log.latest('k') == b


def test_a_record_file_is_never_replaced(tmp_path):
    log = RecordLog(tmp_path)
    log.append('k', 'a.json', {'x': 1})
    with pytest.raises(LogRefused, match='never replaced'):
        log.append('k', 'a.json', {'x': 2})


def test_an_altered_file_is_refused(tmp_path):
    log = RecordLog(tmp_path)
    log.append('k', 'a.json', {'x': 1})
    (tmp_path / 'a.json').write_text('{"x": 2}\n')
    with pytest.raises(LogRefused, match='absent or altered'):
        log.verify()


def test_a_dropped_or_rewritten_line_is_refused(tmp_path):
    log = RecordLog(tmp_path)
    for n in range(3):
        log.append('k', f'{n}.json', {'n': n})
    lines = log.ledger.read_text().splitlines()
    log.ledger.write_text('\n'.join(lines[:1] + lines[2:]) + '\n')
    with pytest.raises(LogRefused):
        log.verify()
    entry = json.loads(lines[1])
    entry['kind'] = 'edited'
    log.ledger.write_text('\n'.join([lines[0], json.dumps(entry, sort_keys=True), lines[2]]) + '\n')
    with pytest.raises(LogRefused, match='its own hash'):
        log.verify()
