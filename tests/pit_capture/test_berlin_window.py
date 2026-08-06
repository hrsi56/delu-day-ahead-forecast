"""Pure DST-correctness tests for berlin_window.py. No network.

EU DST rule: clocks change on the last Sunday of March (spring-forward) and
the last Sunday of October (fall-back). For 2026 that is 2026-03-29 (spring)
and 2026-10-25 (fall) -- verified independently by scanning zoneinfo's own
UTC-offset table for 2026 (not by trusting a hardcoded assumption):

    2026-03-29 01:00 UTC: Europe/Berlin offset 1:00:00 -> 2:00:00
    2026-10-25 01:00 UTC: Europe/Berlin offset 2:00:00 -> 1:00:00

Both are last-Sunday-of-the-month, matching the EU rule.
"""

from datetime import date, datetime, timedelta, timezone

from pit_capture.berlin_window import (
    expected_quarter_hour_count,
    gate_at_utc,
    local_hour_count,
    resolve_local,
)

SPRING_FORWARD_DELIVERY_DATE = date(2026, 3, 29)
FALL_BACK_DELIVERY_DATE = date(2026, 10, 25)
ORDINARY_DELIVERY_DATE = date(2026, 6, 15)


def test_spring_forward_day_has_23_hours_92_quarter_hours():
    assert expected_quarter_hour_count(SPRING_FORWARD_DELIVERY_DATE) == 92
    assert local_hour_count(SPRING_FORWARD_DELIVERY_DATE) == 23


def test_fall_back_day_has_25_hours_100_quarter_hours():
    assert expected_quarter_hour_count(FALL_BACK_DELIVERY_DATE) == 100
    assert local_hour_count(FALL_BACK_DELIVERY_DATE) == 25


def test_ordinary_day_has_24_hours_96_quarter_hours():
    assert expected_quarter_hour_count(ORDINARY_DELIVERY_DATE) == 96
    assert local_hour_count(ORDINARY_DELIVERY_DATE) == 24


def test_fall_back_02_15_resolves_to_two_distinct_correctly_labeled_utc_instants():
    # Two UTC instants exactly one hour apart, both displaying Berlin
    # wall-clock 02:15 on the fall-back day: 00:15 UTC is the first (CEST,
    # +02:00) occurrence, 01:15 UTC is the second (CET, +01:00) occurrence,
    # since the fold happens at 01:00 UTC (03:00 CEST -> 02:00 CET).
    first_instant_utc = datetime(2026, 10, 25, 0, 15, tzinfo=timezone.utc)
    second_instant_utc = datetime(2026, 10, 25, 1, 15, tzinfo=timezone.utc)

    assert second_instant_utc - first_instant_utc == timedelta(hours=1)
    assert first_instant_utc != second_instant_utc

    first = resolve_local(first_instant_utc)
    second = resolve_local(second_instant_utc)

    assert first["local_iso"].startswith("2026-10-25T02:15:00")
    assert second["local_iso"].startswith("2026-10-25T02:15:00")

    assert first["utc_offset"] == "+02:00"
    assert first["is_dst"] is True

    assert second["utc_offset"] == "+01:00"
    assert second["is_dst"] is False

    assert first["utc_offset"] != second["utc_offset"]


def test_gate_at_utc_is_berlin_noon_on_d_minus_1_and_is_dst_aware():
    # Ordinary summer day: Berlin is CEST (+02:00), so noon local = 10:00 UTC.
    gate = gate_at_utc(ORDINARY_DELIVERY_DATE)
    assert gate == datetime(2026, 6, 14, 10, 0, tzinfo=timezone.utc)

    # Winter delivery day: Berlin is CET (+01:00), so noon local = 11:00 UTC.
    winter_gate = gate_at_utc(date(2026, 1, 15))
    assert winter_gate == datetime(2026, 1, 14, 11, 0, tzinfo=timezone.utc)
