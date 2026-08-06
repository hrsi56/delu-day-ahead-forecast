"""Pure, DST-aware Europe/Berlin calendar-day arithmetic.

Everything here is a pure function over stdlib `datetime`/`zoneinfo` types:
no network I/O, no hardcoded table of transition dates. DST transitions are
discovered by asking `zoneinfo` for the UTC offset in effect at each local
instant, never assumed or looked up from a fixed list of dates.
"""

from __future__ import annotations

from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

BERLIN = ZoneInfo("Europe/Berlin")

_QUARTER_HOUR = timedelta(minutes=15)


def delivery_day_window_utc(delivery_date: date) -> tuple[datetime, datetime]:
    """UTC instants for local Berlin midnight-to-midnight of `delivery_date`.

    Start is inclusive, end is exclusive. Neither boundary falls inside the
    Berlin DST fold/gap (both spring-forward and fall-back transitions
    happen at local 02:00/03:00, never at midnight), so both are always
    unambiguous local instants.
    """
    start_local = datetime.combine(delivery_date, time(0, 0), tzinfo=BERLIN)
    end_local = datetime.combine(delivery_date + timedelta(days=1), time(0, 0), tzinfo=BERLIN)
    return start_local.astimezone(timezone.utc), end_local.astimezone(timezone.utc)


def expected_quarter_hour_count(delivery_date: date) -> int:
    """Expected PT15M row count for `delivery_date`: 92/96/100, derived from
    the actual UTC span of the Berlin local day (never a lookup table)."""
    start_utc, end_utc = delivery_day_window_utc(delivery_date)
    span_seconds = (end_utc - start_utc).total_seconds()
    quarter_hours, remainder = divmod(span_seconds, _QUARTER_HOUR.total_seconds())
    assert remainder == 0, "Berlin local-day span was not a whole number of quarter hours"
    return int(quarter_hours)


def local_hour_count(delivery_date: date) -> int:
    """Local Berlin hour count for `delivery_date`: 23/24/25."""
    start_utc, end_utc = delivery_day_window_utc(delivery_date)
    span_seconds = (end_utc - start_utc).total_seconds()
    hours, remainder = divmod(span_seconds, 3600)
    assert remainder == 0, "Berlin local-day span was not a whole number of hours"
    return int(hours)


def gate_at_utc(delivery_date: date) -> datetime:
    """Europe/Berlin local noon on `delivery_date - 1 day`, in UTC.

    Local noon is never inside a DST fold/gap, so this is always an
    unambiguous local instant regardless of which offset (CET/CEST) is in
    effect that day.
    """
    d_minus_1 = delivery_date - timedelta(days=1)
    local_noon = datetime.combine(d_minus_1, time(12, 0), tzinfo=BERLIN)
    return local_noon.astimezone(timezone.utc)


def resolve_local(instant_utc: datetime) -> dict:
    """Resolve a real UTC instant to its Europe/Berlin wall-clock rendering.

    Returns {"local_iso": ..., "utc_offset": "+01:00"|"+02:00", "is_dst": bool}.
    Because the input is always an unambiguous absolute UTC instant (never a
    bare local time string), converting it via `astimezone` is inherently
    correct even across the fall-back fold: two UTC instants an hour apart
    that both display the same Berlin wall-clock digits still carry distinct
    `tzinfo`/offset once resolved from their own UTC instant.
    """
    if instant_utc.tzinfo is None:
        raise ValueError("instant_utc must be timezone-aware")
    local = instant_utc.astimezone(BERLIN)
    offset = local.utcoffset()
    total_minutes = int(offset.total_seconds() // 60)
    sign = "+" if total_minutes >= 0 else "-"
    total_minutes = abs(total_minutes)
    offset_str = f"{sign}{total_minutes // 60:02d}:{total_minutes % 60:02d}"
    return {
        "local_iso": local.isoformat(),
        "utc_offset": offset_str,
        "is_dst": bool(local.dst()),
    }


def expected_quarter_hour_grid_utc(delivery_date: date) -> list[datetime]:
    """The expected PT15M grid for `delivery_date`, as a list of UTC instants
    (start inclusive, one entry per quarter hour). Not part of the required
    public surface in the brief, but shared by berlin_window's own callers
    and by capture.classify so the grid is only ever computed one way."""
    start_utc, _ = delivery_day_window_utc(delivery_date)
    n = expected_quarter_hour_count(delivery_date)
    return [start_utc + i * _QUARTER_HOUR for i in range(n)]
