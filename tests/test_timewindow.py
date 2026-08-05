"""Time derivation: UTC-instant discipline, Berlin DST, expected row counts."""
from __future__ import annotations

from datetime import date, datetime, timezone

import pytest

from pit_capture.timewindow import UsageError, derive_window, parse_utc_instant


def test_parse_utc_instant_accepts_z_and_explicit_offset():
    assert parse_utc_instant("2026-08-05T08:30:00Z") == datetime(
        2026, 8, 5, 8, 30, tzinfo=timezone.utc
    )
    assert parse_utc_instant("2026-08-05T08:30:00+00:00") == datetime(
        2026, 8, 5, 8, 30, tzinfo=timezone.utc
    )


def test_parse_utc_instant_rejects_naive_input():
    with pytest.raises(UsageError, match="explicit UTC instant"):
        parse_utc_instant("2026-08-05T08:30:00")


def test_parse_utc_instant_rejects_non_utc_offset():
    with pytest.raises(UsageError, match="must be UTC"):
        parse_utc_instant("2026-08-05T10:30:00+02:00")


def test_parse_utc_instant_rejects_garbage():
    with pytest.raises(UsageError, match="not a valid ISO-8601"):
        parse_utc_instant("yesterday morning")


def test_normal_summer_day_is_24_hours_and_96_slots():
    window = derive_window(datetime(2026, 8, 5, 8, 30, tzinfo=timezone.utc))
    assert window.local_pull_time.isoformat() == "2026-08-05T10:30:00+02:00"
    assert window.utc_offset == "+02:00"
    assert window.delivery_date == date(2026, 8, 6)
    assert window.gate_at_utc == datetime(2026, 8, 5, 10, 0, tzinfo=timezone.utc)
    assert window.window_start_utc == datetime(2026, 8, 5, 22, 0, tzinfo=timezone.utc)
    assert window.window_end_utc == datetime(2026, 8, 6, 22, 0, tzinfo=timezone.utc)
    assert window.day_length_hours == 24
    assert window.expected_rows("PT15M") == 96
    assert window.expected_rows("PT60M") == 24


def test_winter_day_gate_is_11_utc():
    window = derive_window(datetime(2026, 1, 14, 9, 30, tzinfo=timezone.utc))
    assert window.utc_offset == "+01:00"
    assert window.gate_at_utc == datetime(2026, 1, 14, 11, 0, tzinfo=timezone.utc)
    assert window.day_length_hours == 24


def test_spring_forward_delivery_day_is_23_hours_and_92_slots():
    # Pull on 2026-03-28 -> delivery day 2026-03-29, the Berlin spring-forward day.
    window = derive_window(datetime(2026, 3, 28, 9, 30, tzinfo=timezone.utc))
    assert window.delivery_date == date(2026, 3, 29)
    assert window.window_start_utc == datetime(2026, 3, 28, 23, 0, tzinfo=timezone.utc)
    assert window.window_end_utc == datetime(2026, 3, 29, 22, 0, tzinfo=timezone.utc)
    assert window.day_length_hours == 23
    assert window.expected_rows("PT15M") == 92
    assert window.expected_rows("PT60M") == 23


def test_fall_back_delivery_day_is_25_hours_and_100_slots():
    # Pull on 2026-10-24 -> delivery day 2026-10-25, the Berlin fall-back day.
    window = derive_window(datetime(2026, 10, 24, 8, 30, tzinfo=timezone.utc))
    assert window.delivery_date == date(2026, 10, 25)
    assert window.window_start_utc == datetime(2026, 10, 24, 22, 0, tzinfo=timezone.utc)
    assert window.window_end_utc == datetime(2026, 10, 25, 23, 0, tzinfo=timezone.utc)
    assert window.day_length_hours == 25
    assert window.expected_rows("PT15M") == 100
    assert window.expected_rows("PT60M") == 25


def test_fall_back_day_two_local_0230_instants_stay_distinct():
    """CP-0 item 4: both Berlin 02:30 instants on 2026-10-25 remain distinct."""
    first = derive_window(parse_utc_instant("2026-10-25T00:30:00Z"))  # 02:30 CEST
    second = derive_window(parse_utc_instant("2026-10-25T01:30:00Z"))  # 02:30 CET

    assert first.local_pull_time.strftime("%H:%M") == "02:30"
    assert second.local_pull_time.strftime("%H:%M") == "02:30"

    assert first.utc_offset == "+02:00"
    assert second.utc_offset == "+01:00"
    assert first.pulled_at_utc != second.pulled_at_utc
    assert (second.pulled_at_utc - first.pulled_at_utc).total_seconds() == 3600

    # Same Berlin calendar day -> same delivery day and the same 12:00 gate.
    assert first.delivery_date == second.delivery_date == date(2026, 10, 26)
    assert first.gate_at_utc == second.gate_at_utc == datetime(
        2026, 10, 25, 11, 0, tzinfo=timezone.utc
    )
    # The two local renderings differ only by offset, never by wall-clock text.
    assert first.local_pull_time.isoformat() == "2026-10-25T02:30:00+02:00"
    assert second.local_pull_time.isoformat() == "2026-10-25T02:30:00+01:00"


def test_expected_rows_rejects_resolution_that_does_not_tile_the_day():
    window = derive_window(datetime(2026, 3, 28, 9, 30, tzinfo=timezone.utc))  # 23 h day
    with pytest.raises(ValueError, match="not a whole multiple"):
        window.expected_rows("PT2H")
