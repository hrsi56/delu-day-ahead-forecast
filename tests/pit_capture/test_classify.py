"""Pure response-classification tests: call classify() directly, no
network. Covers CP-0 items 2 (failed/partial/rate-limited never qualify;
positive control proves a complete response records qualifying), 3
(pulled_at is recorded verbatim, never rewritten from the response), and
5 (classify itself does no I/O -- no mutation possible here).
"""

from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pytest

from pit_capture.berlin_window import gate_at_utc
from pit_capture.capture import classify

FIXTURES_DIR = Path(__file__).parent / "fixtures"
COMPLETE_RESPONSE_FIXTURE = FIXTURES_DIR / "complete_response_sample.xml"

_MISSING_FIXTURE_REASON = (
    "tests/pit_capture/fixtures/complete_response_sample.xml has not been "
    "captured yet: the ENTSO-E Transparency Platform was in scheduled "
    "maintenance (HTTP 503, 'Scheduled maintenance is currently underway') "
    "for the entire build session, confirmed by ~21 live attempts over "
    "~25 minutes. Re-run `fetch_raw(date(2026, 8, 5), token)` from "
    "pit_capture.capture once the platform is back and save response_text "
    "to this path -- no code changes needed, this test will then run."
)

# --- Synthetic fixtures (built inline, not committed as files) ----------

_TRUNCATED_XML_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<GL_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0">
  <mRID>synthetic-truncated</mRID>
  <revisionNumber>1</revisionNumber>
  <type>A65</type>
  <process.processType>A01</process.processType>
  <time_Period.timeInterval>
    <start>2026-08-05T00:00Z</start>
    <end>2026-08-06T00:00Z</end>
  </time_Period.timeInterval>
  <TimeSeries>
    <mRID>1</mRID>
    <businessType>A04</businessType>
    <objectAggregation>A01</objectAggregation>
    <outBiddingZone_Domain.mRID codingScheme="A01">10Y1001A1001A82H</outBiddingZone_Domain.mRID>
    <quantity_Measure_Unit.name>MAW</quantity_Measure_Unit.name>
    <curveType>A03</curveType>
    <Period>
      <timeInterval>
        <start>2026-08-05T00:00Z</start>
        <end>2026-08-05T12:00Z</end>
      </timeInterval>
      <resolution>PT15M</resolution>
      {points}
    </Period>
  </TimeSeries>
</GL_MarketDocument>
"""


def _build_truncated_response(n_points: int = 48) -> str:
    # Only the first half of the delivery day (positions 1..48 of 96) is
    # present -- the tail of the day was dropped, e.g. a genuinely partial
    # publication.
    points = "\n".join(
        f"      <Point><position>{i}</position><quantity>{40000 + i}</quantity></Point>"
        for i in range(1, n_points + 1)
    )
    return _TRUNCATED_XML_TEMPLATE.format(points=points)


_RATE_LIMITED_TEXT = (
    "<html><head><title>429 Too Many Requests</title></head>"
    "<body><h1>Too Many Requests</h1>"
    "<p>You have exceeded your request quota for this API key.</p></body></html>"
)

_ABSENT_XML = """<?xml version="1.0" encoding="utf-8"?>
<Acknowledgement_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:acknowledgementdocument:6:0">
  <mRID>synthetic-absent</mRID>
  <Reason>
    <code>999</code>
    <text>No matching data found for Data item Load Forecast Day Ahead, Type A65 [12.1.C], BiddingZone_Domain =10Y1001A1001A82H, ...</text>
  </Reason>
</Acknowledgement_MarketDocument>
"""

_DELIVERY_DATE_FOR_SYNTHETIC = date(2026, 8, 5)


def _well_before_gate(delivery_date: date) -> datetime:
    return gate_at_utc(delivery_date) - timedelta(days=2)


def test_truncated_response_is_present_partial_and_not_qualifying():
    raw_text = _build_truncated_response(n_points=48)
    pulled_at = _well_before_gate(_DELIVERY_DATE_FOR_SYNTHETIC)

    entry = classify(200, raw_text, None, pulled_at, _DELIVERY_DATE_FOR_SYNTHETIC)

    assert entry.status == "present_partial"
    assert entry.qualifying is False
    assert entry.qualifying_reason == "present_partial"
    assert entry.expected_row_count == 96
    assert entry.observed_row_count == 48
    assert entry.completeness_ratio == 0.5


def test_rate_limited_response_is_request_error_and_not_qualifying():
    pulled_at = _well_before_gate(_DELIVERY_DATE_FOR_SYNTHETIC)

    entry = classify(429, _RATE_LIMITED_TEXT, None, pulled_at, _DELIVERY_DATE_FOR_SYNTHETIC)

    assert entry.status == "request_error"
    assert entry.qualifying is False
    assert "rate" in entry.qualifying_reason.lower()
    assert entry.http_status == 429
    # a body was present even though the request failed -- it must still be hashed/retained
    assert entry.payload_sha256 is not None


def test_absent_response_is_absent_and_not_qualifying():
    pulled_at = _well_before_gate(_DELIVERY_DATE_FOR_SYNTHETIC)

    entry = classify(200, _ABSENT_XML, None, pulled_at, _DELIVERY_DATE_FOR_SYNTHETIC)

    assert entry.status == "absent"
    assert entry.qualifying is False
    assert entry.qualifying_reason == "absent"
    assert entry.observed_row_count == 0


def test_connection_failure_has_no_body_and_is_request_error():
    pulled_at = _well_before_gate(_DELIVERY_DATE_FOR_SYNTHETIC)
    exc = ConnectionError("simulated connection failure")

    entry = classify(None, None, exc, pulled_at, _DELIVERY_DATE_FOR_SYNTHETIC)

    assert entry.status == "request_error"
    assert entry.qualifying is False
    assert entry.payload_sha256 is None  # genuinely no body to hash
    assert entry.raw_artifact_path is None


@pytest.mark.skipif(not COMPLETE_RESPONSE_FIXTURE.exists(), reason=_MISSING_FIXTURE_REASON)
def test_positive_control_real_complete_response_is_present_complete_and_qualifying():
    fixture_path = COMPLETE_RESPONSE_FIXTURE
    raw_text = fixture_path.read_text(encoding="utf-8")

    # The fixture covers delivery date 2026-08-05 (a fully-elapsed,
    # already-settled historical day at the time it was captured).
    delivery_date = date(2026, 8, 5)
    pulled_at = _well_before_gate(delivery_date)  # two days before that day's real gate

    entry = classify(200, raw_text, None, pulled_at, delivery_date)

    assert entry.status == "present_complete"
    assert entry.qualifying is True
    assert entry.qualifying_reason == "qualifying"
    assert entry.expected_row_count == 96
    assert entry.observed_row_count == 96
    assert entry.completeness_ratio == 1.0


def test_pulled_at_utc_is_recorded_verbatim_never_derived_from_response():
    # Uses the synthetic (not the real) fixture -- this guarantee doesn't
    # depend on real ENTSO-E data, only on classify() never substituting
    # `pulled_at_utc` for anything derived from the response content.
    raw_text = _build_truncated_response(n_points=48)
    delivery_date = _DELIVERY_DATE_FOR_SYNTHETIC

    exact_instant = datetime(2026, 8, 3, 7, 42, 13, tzinfo=timezone.utc)
    entry = classify(200, raw_text, None, exact_instant, delivery_date)

    assert entry.pulled_at_utc == exact_instant
    # sanity: a plainly different instant must not accidentally match.
    assert entry.pulled_at_utc != datetime(2026, 8, 6, 12, 58, 31, tzinfo=timezone.utc)
