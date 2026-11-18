"""The committed live record (CP-18c items 2-5): the store verifies, the archive verifies, every issued day's load
forecast was shown by a retrieval strictly before its own cutoff, every not-issued day carries one of the five causes,
and the outside days are the carry's. Skipped, with the reason, where the live record is absent."""
from __future__ import annotations

from datetime import date
import json
from pathlib import Path

import pytest

from cp18 import boundary, causes, inputclass
from cp18.live import acquire as AQ
from cp18.live.archive import Archive
from cp18.store import INPUTS_PATH, STORE_PATH, LiveStore

ROOT = Path(__file__).resolve().parents[2]
pytestmark = pytest.mark.skipif(not (ROOT / STORE_PATH / 'ledger.jsonl').is_file(),
                                reason='the live record is absent in this checkout (live/store)')


def test_the_store_verifies_and_starts_from_the_freeze_origin_carried_by_decision_28():
    store = LiveStore(ROOT / STORE_PATH)
    store.verify()
    entries = store.entries()
    assert entries[0]['kind'] == 'genesis' and entries[0]['origin'] == '2026-09-06' and entries[0]['first_day'] == '2026-09-07'
    carry = [e for e in entries if e['kind'] == 'carry']
    assert len(carry) == 1 and carry[0]['last_window_day'] == '2026-09-06' and 'decision 28' in carry[0]['reason']
    days = store.days()
    first_live = carry[0]['first_live_day']
    assert all(v['status'] == 'outside' for d, v in days.items() if d < first_live)
    for d, v in days.items():
        if v['status'] == 'not issued':
            assert causes.text(v['cause'])
    assert any(v['status'] == 'issued' for v in days.values())


def test_every_issued_days_load_forecast_was_shown_before_its_own_cutoff_and_the_archive_verifies():
    store = LiveStore(ROOT / STORE_PATH)
    issued = sorted(d for d, v in store.days().items() if v['status'] == 'issued')
    with boundary.live():
        archive = Archive(ROOT / INPUTS_PATH)
        for x in archive.days():
            assert archive.verify(x) == [], x
        for d in issued:
            shown = AQ.load_forecast_shown(archive, date.fromisoformat(d))
            # CP-18d (decision 31; O68): a day issued with the load forecast fetched after the cutoff carries that label,
            # checked against its own evidence by `inputclass.of_record`; its archived copy is complete, and not
            # admitted before the cutoff. Every other issued day keeps CP-18c's assertion unchanged.
            record = json.loads((ROOT / STORE_PATH / 'issued' / d / 'record.json').read_text())
            if inputclass.of_record(record)['input_class'] == inputclass.AFTER:
                assert shown['complete'] and not shown['admitted'], (d, shown)
                continue
            assert shown['shown'] and shown['admitted'] and shown['complete'], (d, shown)
