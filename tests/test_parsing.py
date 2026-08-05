"""Payload parsing and DST-aware completeness assessment."""
from __future__ import annotations

from datetime import datetime, timezone

import pytest
from a65_xml import build_day, build_document, build_period, synthetic_load
from conftest import FIXTURE_DIR

from pit_capture.parsing import PayloadParseError, assess_completeness, parse_a65_payload
from pit_capture.timewindow import derive_window

PULL_2026_08_05 = datetime(2026, 8, 5, 8, 30, tzinfo=timezone.utc)
COMPLETE = FIXTURE_DIR / "a65_a01_de-lu_2026-08-06_complete_96.xml"
TRUNCATED = FIXTURE_DIR / "a65_a01_de-lu_2026-08-06_truncated_80.xml"
GAP_AT_40 = FIXTURE_DIR / "a65_a01_de-lu_2026-08-06_gap_at_40.xml"
NAN_AT_50 = FIXTURE_DIR / "a65_a01_de-lu_2026-08-06_nan_at_50.xml"


def _assess(path_or_text, pull=PULL_2026_08_05):
    text = path_or_text.read_text() if hasattr(path_or_text, "read_text") else path_or_text
    doc = parse_a65_payload(text)
    return doc, assess_completeness(doc, derive_window(pull))


def test_complete_fixture_parses_to_96_of_96():
    doc, result = _assess(COMPLETE)
    assert doc.document_type == "A65"
    assert doc.process_type == "A01"
    assert doc.curve_types == ["A03"]
    assert doc.resolutions == ["PT15M"]
    assert result.expected_rows == 96
    assert result.observed_rows == 96
    assert result.completeness_ratio == 1.0
    assert result.missing_slots == 0
    assert result.null_slots == 0
    assert result.issues == []
    assert result.first_delivery_timestamp_utc == datetime(2026, 8, 5, 22, 0, tzinfo=timezone.utc)
    assert result.last_delivery_timestamp_utc == datetime(2026, 8, 6, 21, 45, tzinfo=timezone.utc)
    assert result.latest_fully_populated_timestamp_utc == result.last_delivery_timestamp_utc


def test_created_date_time_is_read_and_kept_separate():
    doc = parse_a65_payload(COMPLETE.read_text())
    assert doc.created_at_utc == datetime(2026, 8, 5, 6, 42, 11, tzinfo=timezone.utc)


def test_truncated_response_is_short():
    _, result = _assess(TRUNCATED)
    assert result.observed_rows == 80
    assert result.expected_rows == 96
    assert result.missing_slots == 16
    assert result.completeness_ratio == round(80 / 96, 6)
    assert result.latest_fully_populated_timestamp_utc == datetime(
        2026, 8, 6, 17, 45, tzinfo=timezone.utc
    )


def test_interior_gap_caps_latest_fully_populated_before_the_gap():
    """Not simply the last non-null row: a hole at slot 40 caps it at slot 39."""
    _, result = _assess(GAP_AT_40)
    assert result.observed_rows == 95
    assert result.missing_slots == 1
    assert result.last_delivery_timestamp_utc == datetime(2026, 8, 6, 21, 45, tzinfo=timezone.utc)
    # slot 39 ends the leading contiguous run: 22:00Z + 38 * 15 min.
    assert result.latest_fully_populated_timestamp_utc == datetime(
        2026, 8, 6, 7, 30, tzinfo=timezone.utc
    )


def test_empty_quantity_counts_as_a_nan_slot():
    _, result = _assess(NAN_AT_50)
    assert result.observed_rows == 95
    assert result.null_slots == 1
    assert result.missing_slots == 0
    assert "empty/NaN" in " ".join(result.issues)
    # slot 49 ends the leading contiguous run: 22:00Z + 48 * 15 min.
    assert result.latest_fully_populated_timestamp_utc == datetime(
        2026, 8, 6, 10, 0, tzinfo=timezone.utc
    )


def test_hourly_resolution_expected_count_is_day_length():
    xml = build_day(
        start_utc=datetime(2026, 8, 5, 22, 0, tzinfo=timezone.utc),
        slots=24,
        resolution="PT60M",
    )
    _, result = _assess(xml)
    assert result.resolution == "PT60M"
    assert result.expected_rows == 24
    assert result.observed_rows == 24


def test_spring_forward_day_expects_92_slots():
    start = datetime(2026, 3, 28, 23, 0, tzinfo=timezone.utc)
    xml = build_day(start_utc=start, slots=92)
    _, result = _assess(xml, pull=datetime(2026, 3, 28, 9, 30, tzinfo=timezone.utc))
    assert result.expected_rows == 92
    assert result.observed_rows == 92
    assert result.completeness_ratio == 1.0


def test_fall_back_day_expects_100_slots():
    start = datetime(2026, 10, 24, 22, 0, tzinfo=timezone.utc)
    xml = build_day(start_utc=start, slots=100)
    _, result = _assess(xml, pull=datetime(2026, 10, 24, 8, 30, tzinfo=timezone.utc))
    assert result.expected_rows == 100
    assert result.observed_rows == 100
    assert result.completeness_ratio == 1.0


def test_a_96_slot_payload_on_a_25_hour_day_is_short():
    """The naive 'always 96' assumption must not read as complete."""
    start = datetime(2026, 10, 24, 22, 0, tzinfo=timezone.utc)
    xml = build_day(start_utc=start, slots=96)
    _, result = _assess(xml, pull=datetime(2026, 10, 24, 8, 30, tzinfo=timezone.utc))
    assert result.expected_rows == 100
    assert result.observed_rows == 96
    assert result.missing_slots == 4


def test_mixed_resolutions_are_flagged_not_silently_chosen():
    start = datetime(2026, 8, 5, 22, 0, tzinfo=timezone.utc)
    first = build_period(
        start_utc=start,
        resolution="PT15M",
        quantities=[synthetic_load(i) for i in range(1, 49)],
    )
    second = build_period(
        start_utc=datetime(2026, 8, 6, 10, 0, tzinfo=timezone.utc),
        resolution="PT60M",
        quantities=[synthetic_load(i) for i in range(1, 13)],
    )
    xml = build_document(
        periods=[first, second],
        created_at_utc=datetime(2026, 8, 5, 6, 0, tzinfo=timezone.utc),
        doc_start_utc=start,
        doc_end_utc=datetime(2026, 8, 6, 22, 0, tzinfo=timezone.utc),
    )
    _, result = _assess(xml)
    assert result.resolution is None
    assert result.expected_rows is None
    assert "mixes resolutions" in " ".join(result.issues)


def test_non_xml_payload_raises_parse_error():
    with pytest.raises(PayloadParseError, match="not well-formed"):
        parse_a65_payload("<html><body>gateway timeout")


def test_wrong_root_element_raises_parse_error():
    with pytest.raises(PayloadParseError, match="GL_MarketDocument"):
        parse_a65_payload('<?xml version="1.0"?><Acknowledgement_MarketDocument/>')


def test_malformed_created_date_time_raises_parse_error_not_value_error():
    """A garbled createdDateTime must become a PayloadParseError (caught by
    the caller and turned into a not_qualifying ledger entry), never a bare
    ValueError escaping out of datetime.fromisoformat uncaught."""
    xml = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<GL_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:'
        'generationloaddocument:3:0">\n'
        "  <type>A65</type>\n"
        "  <process.processType>A01</process.processType>\n"
        "  <createdDateTime>not-a-timestamp</createdDateTime>\n"
        "</GL_MarketDocument>\n"
    )
    with pytest.raises(PayloadParseError, match="unparseable ENTSO-E timestamp"):
        parse_a65_payload(xml)


def test_malformed_period_start_raises_parse_error_not_value_error():
    xml = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<GL_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:'
        'generationloaddocument:3:0">\n'
        "  <type>A65</type>\n"
        "  <process.processType>A01</process.processType>\n"
        "  <createdDateTime>2026-08-05T06:00:00Z</createdDateTime>\n"
        "  <TimeSeries>\n"
        "    <mRID>1</mRID>\n"
        "    <curveType>A03</curveType>\n"
        "    <Period>\n"
        "      <timeInterval>\n"
        "        <start>garbage</start>\n"
        "        <end>2026-08-06T22:00Z</end>\n"
        "      </timeInterval>\n"
        "      <resolution>PT15M</resolution>\n"
        "    </Period>\n"
        "  </TimeSeries>\n"
        "</GL_MarketDocument>\n"
    )
    with pytest.raises(PayloadParseError, match="unparseable ENTSO-E timestamp"):
        parse_a65_payload(xml)
