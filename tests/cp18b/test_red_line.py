"""CP-18b's red line over every file this round adds or changes, with no file skipped whole (§24.2).

No delivery day after 2026-09-06 is read, recorded, displayed or mentioned, except as a protocol or calendar date.
CP-18a's scanner (`tests/cp18a/test_red_line.py`), applied to this round's paths: JSON parsed, every string checked
(a bare date after the boundary must be a listed calendar or protocol date; a delivery-day key must hold a development
day), NumPy archives opened (instants and days end within the boundary), everything else scanned as bytes.
"""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
import io
import json
from pathlib import Path
import re
import zipfile

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
BOUNDARY = date(2026, 9, 6)
#: The round's own paths: every file it adds, and the files it changes (scanned whole).
ADDED = ('src/cp18/records.py', 'src/cp18/outcomes.py', 'src/cp18/evaluation.py', 'src/cp18/bundle.py',
         'src/cp18/controls.py', 'src/cp18/publish.py', 'src/cp18/spaceglue.py', 'src/cp18/live_claims.py',
         'tests/cp18b', 'reports/cp18b', 'docs/track-b/evidence/cp-18b', 'space-product',
         'scripts/build_product_space.py')
CHANGED = ('tests/test_24_live_namespace_is_walled_off.py', '.github/workflows/daily.yml')
#: Dates after the boundary that the round's files may name, each a calendar or protocol date, never a delivery day.
CALENDAR = {
    '2026-09-07': "4.7T's first window day, a protocol date (the day after the freeze origin)",
    '2026-09-08': 'the snapshot pull (data/README.md), a calendar date',
    '2026-09-23': "the last dated NCEP production-status capture (CP-25's GFS reconstruction), a calendar date",
    '2026-09-24': 'the credential exposure (docs/track-b/credential-exposure-2026-09-24.md), a calendar date',
    '2026-09-28': 'a document date cited by the issued brief',
    '2026-09-29': 'PUBLISH_RULES 1.0, a document date',
    '2026-09-30': "the Space plan and the Owner's daily-update exception, document dates",
    '2026-10-01': "the archived proposal's date, a document date",
    '2026-10-04': "the Owner's programme order (§22), a document date",
    '2026-10-10': 'the work-availability decision, a document date',
    '2026-10-12': "the Owner's CP-25 rulings, a document date",
    '2026-10-15': "CP-26's cold rerun folder name, a document date",
    '2026-10-19': "GitHub's ubuntu-latest image change (a comment in tests.yml), a calendar date",
    '2026-10-20': 'a document date cited by the issued brief',
    '2026-10-24': 'a document date cited by the issued brief',
    '2026-10-25': "the Owner's pre-CP-17 rulings, a document date",
    '2026-10-27': 'a document date cited by the issued brief',
    '2026-10-28': "the Owner's decisions 11-19, a document date",
    '2026-10-29': "the Owner's decisions 20-21, a document date",
    '2026-10-30': "the brief's issue and decisions 22-27, document dates",
    '2026-10-31': "this round's own run date, a calendar date",
    '2026-11-01': "this round's own run date, a calendar date",
    '2026-12-04': "4.7T's window opens no earlier than this, a protocol date",
    '2027-01-05': "S_13's last service day (k13.json's service_last, the day before S_14), a protocol date",
    '2027-01-06': 'S_14, the scheduled search (H4), a protocol date',
    '2026-11-02': 'a document date cited by the issued brief',
    '2026-11-03': 'a document date cited by the issued brief',
    '2026-11-04': "CP-18a's landing record and this brief's issue, document dates",
    '2026-11-05': "this round's own run date, a calendar date",
    '2026-12-05': "4.7T's last window day, a protocol date (the badge of CP-17's protocol §12)",
}
DAY_KEYS = {'day', 'delivery_day', 'days', 'planned', 'lookback', 'target_day', 'first_day', 'last_day', 'origin',
            'last_window_day', 'first_live_day', 'source_day', 'search_day', 'first', 'last'}
ISO_DATE = re.compile(rb'(?<![0-9])(20[0-9]{2})-([01][0-9])-([0-3][0-9])(T[0-9]{2}:[0-9]{2})?')
TIME_ARRAYS = re.compile(r'(_ns$|^key_ts$|^days$|^dates$)')
LAST_INSTANT = datetime(2026, 9, 6, 22, 0, tzinfo=timezone.utc)      # the end of the boundary's Berlin day


def files() -> list[Path]:
    out = []
    for rel in ADDED + CHANGED:
        path = ROOT / rel
        if path.is_file():
            out.append(path)
        elif path.is_dir():
            out += sorted(p for p in path.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    return out


def _date(match) -> date | None:
    try:
        return date(int(match[1]), int(match[2]), int(match[3]))
    except ValueError:
        return None


def text_problems(blob: bytes, now: datetime) -> list[str]:
    problems = []
    for m in ISO_DATE.finditer(blob):
        day = _date(m)
        if day is None or day <= BOUNDARY:
            continue
        stamp = m[4] is not None
        if stamp and day <= now.date() + timedelta(days=1):
            continue                                    # a wall-clock time of a run or a document
        if m.group(0)[:10].decode() not in CALENDAR:
            problems.append(f'{m.group(0).decode()} at byte {m.start()}')
    return problems


def json_problems(value, now: datetime, key: str = '') -> list[str]:
    problems = []
    if isinstance(value, dict):
        for k, v in value.items():
            problems += json_problems(k, now, '') + json_problems(v, now, str(k))
    elif isinstance(value, list):
        for v in value:
            problems += json_problems(v, now, key)
    elif isinstance(value, str):
        problems += [f'{key or "<string>"}: {p}' for p in text_problems(value.encode(), now)]
        if key in DAY_KEYS:
            for m in ISO_DATE.finditer(value.encode()):
                day = _date(m)
                if day is not None and day > BOUNDARY and m[4] is None:
                    problems.append(f'{key}: delivery day {m.group(0).decode()} is after the boundary')
    return problems


def npz_problems(blob: bytes) -> list[str]:
    problems = []
    with np.load(io.BytesIO(blob), allow_pickle=False) as z:
        for name in z.files:
            if not TIME_ARRAYS.search(name):
                continue
            a = np.asarray(z[name])
            if not a.size:
                continue
            if name.endswith('_ns') or name == 'key_ts':
                last = datetime.fromtimestamp(int(a.max()) / 1e9, tz=timezone.utc)
                if last >= LAST_INSTANT:
                    problems.append(f'{name}: an instant at or after the boundary day ends ({last:%Y-%m-%dT%H:%MZ})')
            else:
                last = a.astype('datetime64[D]').max() if a.dtype.kind == 'M' else np.datetime64('1970-01-01') + int(a.max())
                if str(last) > str(BOUNDARY):
                    problems.append(f'{name}: a day after the boundary ({last})')
    return problems


def problems_of(path: Path, now: datetime) -> list[str]:
    blob = path.read_bytes()
    if path.suffix == '.json':
        return json_problems(json.loads(blob), now)
    if path.suffix == '.jsonl':
        return [p for line in blob.splitlines() if line.strip() for p in json_problems(json.loads(line), now)]
    if path.suffix == '.npz':
        return npz_problems(blob) + text_problems(blob, now)
    if path.suffix in ('.whl', '.zip'):
        out = text_problems(blob, now)
        with zipfile.ZipFile(io.BytesIO(blob)) as z:
            for info in z.infolist():
                out += [f'{info.filename}: {p}' for p in text_problems(z.read(info), now)]
        return out
    return text_problems(blob, now)


def test_the_round_has_files_to_scan():
    found = files()
    assert len(found) > 40 and any(p.name == 'issued-brief.md' for p in found)
    assert any(p.name == 'manifest.json' and p.parent.name == 'bundle' for p in found)


@pytest.mark.parametrize('path', files(), ids=lambda p: str(p.relative_to(ROOT)))
def test_no_delivery_day_after_the_boundary(path):
    now = datetime.now(timezone.utc)
    assert problems_of(path, now) == []


def test_the_scanner_refuses_what_it_should():
    now = datetime(2026, 10, 31, tzinfo=timezone.utc)
    late = str(BOUNDARY + timedelta(days=40))
    assert text_problems(f'the forecast for {late}'.encode(), now)
    assert not text_problems(b'S_14 runs on 2027-01-06; a run at 2026-10-31T08:05:03Z', now)
    assert json_problems({'planned': [late]}, now)
    assert json_problems({'retrieved_utc': f'{BOUNDARY.year + 1}-02-01T00:00:00+00:00'}, now)     # a future wall clock
    assert json_problems({'day': '2026-10-30'}, now)                                # a calendar date as a delivery day
    buf = io.BytesIO()
    np.savez(buf, key_ts=np.array([int(LAST_INSTANT.timestamp() * 1e9)]), days=np.array([0]))
    assert npz_problems(buf.getvalue())
