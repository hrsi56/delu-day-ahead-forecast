"""The input class of a live day (the Owner's decision 31, CP-18d): its inputs all before the cutoff, or its load
forecast fetched after the cutoff.

**Decision 31.** When D's day-ahead load forecast cannot be shown to precede D's cutoff (D−1 11:00 Europe/Berlin), v6
(A1 in the frozen records) still issues D through the frozen chain, with the load forecast retrieved after the cutoff
(`cp18.live.history.fetched_after_cutoff`). That day is labelled "load forecast fetched after the cutoff", with that
copy's retrieval time (UTC), on every surface that shows it, and the evaluation reports such days apart from the days
whose inputs all precede the cutoff. Every other input keeps decision 22's rule, and the chain is unchanged.

**Two classes, and nothing else:**

| Class | Label | Fetch time |
|---|---|---|
| `before_cutoff` | "all inputs before the cutoff" | none |
| `load_forecast_after_cutoff` | "load forecast fetched after the cutoff" | the copy's retrieval time, UTC, not strictly before D's cutoff |

The label names the input's retrieval. It is never "late" and never "timely" (§24.13).

**Where the class is read.** A day record written from CP-18d on (`RECORD_SCHEMA`) carries the class itself, and it
must agree with the record's own availability evidence: for `before_cutoff`, D's required load forecast was admitted
against D's cutoff (by its retrieval or document time, or ruling 1's exception on development days); for
`load_forecast_after_cutoff`, it was not admitted, and the copy used is named with its retrieval time (a stand-in's
record without availability evidence, in the pipeline's tests, is checked on its label and cutoff only). A record of
CP-18a–c's schema (`LEGACY_SCHEMA`) predates decision 31: its D's load forecast was admitted before the cutoff, or the
day was never issued, so its class is derived as `before_cutoff` from that evidence. Anything else is refused
(`LabelMissing`): a CP-18d record without its class, an unknown class, a class its evidence contradicts, or an
after-cutoff class without its fetch time.
"""
from __future__ import annotations

from datetime import datetime, timezone

BEFORE = 'before_cutoff'
AFTER = 'load_forecast_after_cutoff'
TEXT = {BEFORE: 'all inputs before the cutoff', AFTER: 'load forecast fetched after the cutoff'}
ORDER = (BEFORE, AFTER)
FIELDS = ('input_class', 'input_class_text', 'load_forecast_fetched_utc')
RECORD_SCHEMA = 'cp18d-day-record-v1'
LEGACY_SCHEMA = 'cp18a-day-record-v1'
DECISION = ("the Owner's decision 31: D's load forecast was not shown before D's cutoff, so v6 issues D with the copy "
            'retrieved after the cutoff')


class LabelMissing(ValueError):
    """A day's input class is absent, unknown, or contradicted by its own evidence: the day is refused."""


def _instant(text) -> datetime | None:
    if not isinstance(text, str) or not text:
        return None
    value = datetime.fromisoformat(text.replace('Z', '+00:00'))
    if value.tzinfo is None:
        raise LabelMissing(f'a naive instant {text!r} in an input class')
    return value.astimezone(timezone.utc)


def _utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def label(input_class: str, fetched_utc: str | None = None) -> dict:
    """The three fields of a class. An after-cutoff class needs its copy's retrieval time; a before-cutoff one has none."""
    if input_class not in TEXT:
        raise LabelMissing(f'{input_class!r} is not an input class ({", ".join(ORDER)})')
    if input_class == AFTER:
        at = _instant(fetched_utc)
        if at is None:
            raise LabelMissing('a day labelled "load forecast fetched after the cutoff" needs that copy\'s retrieval time')
        return {'input_class': AFTER, 'input_class_text': TEXT[AFTER], 'load_forecast_fetched_utc': _utc(at)}
    if fetched_utc:
        raise LabelMissing('a day whose inputs all precede the cutoff names no fetch time after it')
    return {'input_class': BEFORE, 'input_class_text': TEXT[BEFORE], 'load_forecast_fetched_utc': None}


def required_load_forecast(record: dict) -> dict | None:
    """D's own load forecast's availability record (the one the build required), from a day record's inputs."""
    day = record.get('day')
    avail = (record.get('inputs') or {}).get('availability')
    if not isinstance(avail, dict):
        return None            # a stand-in's or the prebuilt development payloads' evidence: no per-input records
    found = [r for r in avail.get('records') or []
             if r.get('input') == 'load_forecast' and r.get('data_day') == day and r.get('required')]
    return found[-1] if found else None


def _check_evidence(record: dict, value: dict) -> None:
    lf = required_load_forecast(record)
    if lf is None:
        # A stand-in's record (the pipeline's tests) holds no availability evidence; the live builder always writes it
        # (`cp18.live.build`), so a live record is always checked against it.
        if value['input_class'] == AFTER:
            cutoff = _instant(record.get('cutoff_utc'))
            if cutoff is None or _instant(value['load_forecast_fetched_utc']) < cutoff:
                raise LabelMissing(f"{record.get('day')}: a copy fetched before the cutoff is not a copy fetched after it")
        return
    if value['input_class'] == BEFORE:
        if not lf.get('admitted') or lf.get('fetched_after_cutoff'):
            raise LabelMissing(f"{record.get('day')}: labelled {TEXT[BEFORE]!r}, but D's load forecast was not "
                               'admitted before the cutoff')
        return
    if lf.get('admitted') or not lf.get('fetched_after_cutoff'):
        raise LabelMissing(f"{record.get('day')}: labelled {TEXT[AFTER]!r}, but the evidence names no copy fetched "
                           'after the cutoff')
    if _instant(lf.get('fetched_utc')) != _instant(value['load_forecast_fetched_utc']):
        raise LabelMissing(f"{record.get('day')}: the label's fetch time is not the copy's retrieval time")
    cutoff = _instant(record.get('cutoff_utc') or lf.get('cutoff_utc'))
    if cutoff is None or _instant(value['load_forecast_fetched_utc']) < cutoff:
        raise LabelMissing(f"{record.get('day')}: a copy fetched before the cutoff is not a copy fetched after it")


def _check_issuance(record: dict, value: dict) -> None:
    """A copy fetched after the cutoff was fetched before the issuance that used it (the run fetches, then builds)."""
    started = _instant(record.get('issuance_started_utc'))
    fetched = _instant(value.get('load_forecast_fetched_utc'))
    if started is not None and fetched is not None and fetched > started:
        raise LabelMissing(f"{record.get('day')}: the copy's retrieval time is after the issuance that used it")


def of_record(record: dict) -> dict:
    """The class of a day record (an issuance's `record.json`, or the pipeline's record before it is written)."""
    schema = record.get('schema')
    if schema == LEGACY_SCHEMA:
        if any(k in record for k in FIELDS):
            raise LabelMissing(f"{record.get('day')}: a {LEGACY_SCHEMA} record carries no input class of its own")
        value = label(BEFORE)
        _check_evidence(record, value)
        return value
    if schema != RECORD_SCHEMA:
        raise LabelMissing(f"{record.get('day')}: a day record of schema {schema!r} has no known input class")
    if any(k not in record for k in FIELDS):
        raise LabelMissing(f"{record.get('day')}: the record carries no input class (decision 31's label is missing)")
    value = label(record['input_class'], record['load_forecast_fetched_utc'])
    if record['input_class_text'] != value['input_class_text']:
        raise LabelMissing(f"{record.get('day')}: the label's text is not its class's")
    _check_evidence(record, value)
    _check_issuance(record, value)
    return value


def of_build(built: dict) -> dict:
    """The class a built day carries (`cp18.live_inputs.LiveInputs.build`, or a stand-in's), checked."""
    if any(k not in built for k in FIELDS):
        raise LabelMissing('the built inputs carry no input class (decision 31\'s label is missing)')
    value = label(built['input_class'], built['load_forecast_fetched_utc'])
    if built['input_class_text'] != value['input_class_text']:
        raise LabelMissing("the built inputs' label text is not its class's")
    return value
