"""Time derivation: UTC instant -> Berlin local, delivery day, gate, D+1 window.

Every derived field comes from the supplied UTC instant. Nothing here ever
round-trips through a naive or ambiguous local time, so the two Berlin ``02:30``
instants on a fall-back day stay distinct (CP-0 item 4).
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

BERLIN = ZoneInfo("Europe/Berlin")
UTC = timezone.utc

#: 12:00 Europe/Berlin on D-1 (Section 3). Never ambiguous: Berlin DST
#: transitions happen at 02:00/03:00 local.
GATE_LOCAL_HOUR = 12

_DURATION_RE = re.compile(r"^PT(?:(\d+)H)?(?:(\d+)M)?$")


class UsageError(ValueError):
    """Bad operator input. Exit code 2, and no ledger entry is written."""


def parse_utc_instant(text: str) -> datetime:
    """Parse an explicit-UTC ISO-8601 instant.

    Accepts ``...Z`` and ``...+00:00``. A naive value, or one carrying a
    non-zero UTC offset, is a usage error: an unparseable argument is not a
    capture attempt.
    """
    raw = text.strip()
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00") if raw.endswith("Z") else raw)
    except ValueError as exc:
        raise UsageError(f"--at-utc is not a valid ISO-8601 datetime: {text!r} ({exc})") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise UsageError(
            f"--at-utc must be an explicit UTC instant (got naive {text!r}); "
            "use e.g. 2026-08-05T10:30:00Z or 2026-08-05T10:30:00+00:00"
        )
    if parsed.utcoffset() != timedelta(0):
        raise UsageError(
            f"--at-utc must be UTC (offset +00:00 or Z); got offset "
            f"{parsed.utcoffset()} in {text!r}"
        )
    return parsed.astimezone(UTC)


def format_utc(moment: datetime | None) -> str | None:
    """ISO-8601 with an explicit ``+00:00`` UTC offset."""
    if moment is None:
        return None
    return moment.astimezone(UTC).isoformat()


def format_offset(moment: datetime) -> str:
    """``+02:00`` / ``+01:00`` style UTC offset of a tz-aware instant."""
    offset = moment.utcoffset()
    if offset is None:  # pragma: no cover - guarded by callers
        raise ValueError("cannot format the UTC offset of a naive datetime")
    total = int(offset.total_seconds())
    sign = "+" if total >= 0 else "-"
    total = abs(total)
    return f"{sign}{total // 3600:02d}:{(total % 3600) // 60:02d}"


def resolution_to_timedelta(resolution: str) -> timedelta:
    """``PT15M``/``PT60M``/``PT1H`` -> timedelta. Raises ValueError otherwise."""
    match = _DURATION_RE.match(resolution.strip().upper())
    if not match or not any(match.groups()):
        raise ValueError(f"unsupported ENTSO-E resolution: {resolution!r}")
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    delta = timedelta(hours=hours, minutes=minutes)
    if delta <= timedelta(0):
        raise ValueError(f"non-positive resolution: {resolution!r}")
    return delta


@dataclass(frozen=True)
class CaptureWindow:
    """All time facts derived from one supplied UTC instant."""

    pulled_at_utc: datetime
    local_pull_time: datetime
    utc_offset: str
    pull_local_date: date
    delivery_date: date
    gate_at_utc: datetime
    window_start_utc: datetime
    window_end_utc: datetime
    day_length_hours: int

    def expected_rows(self, resolution: str) -> int:
        """DST-aware, resolution-aware expected row count.

        PT15M -> 92/96/100, PT60M -> 23/24/25. Derived from the true length of
        the delivery-day window, never from an assumed 24 hours (Section 4.0).
        """
        step = resolution_to_timedelta(resolution)
        span = self.window_end_utc - self.window_start_utc
        if span % step != timedelta(0):
            raise ValueError(
                f"delivery window {span} is not a whole multiple of resolution {resolution}"
            )
        return int(span // step)

    def expected_grid(self, resolution: str) -> list[datetime]:
        """Every expected delivery timestamp (UTC), in order."""
        step = resolution_to_timedelta(resolution)
        out: list[datetime] = []
        cursor = self.window_start_utc
        while cursor < self.window_end_utc:
            out.append(cursor)
            cursor += step
        return out


def derive_window(pulled_at_utc: datetime) -> CaptureWindow:
    """Derive Berlin local time, delivery day, gate, and the D+1 window."""
    if pulled_at_utc.tzinfo is None:
        raise ValueError("pulled_at_utc must be tz-aware UTC")
    pulled_at_utc = pulled_at_utc.astimezone(UTC)

    local_pull_time = pulled_at_utc.astimezone(BERLIN)
    pull_local_date = local_pull_time.date()
    delivery_date = pull_local_date + timedelta(days=1)

    gate_local = datetime.combine(pull_local_date, time(GATE_LOCAL_HOUR, 0), tzinfo=BERLIN)
    window_start_local = datetime.combine(delivery_date, time(0, 0), tzinfo=BERLIN)
    window_end_local = datetime.combine(delivery_date + timedelta(days=1), time(0, 0), tzinfo=BERLIN)

    window_start_utc = window_start_local.astimezone(UTC)
    window_end_utc = window_end_local.astimezone(UTC)
    span_hours = (window_end_utc - window_start_utc).total_seconds() / 3600.0
    if span_hours not in (23.0, 24.0, 25.0):  # pragma: no cover - Berlin only ever yields these
        raise ValueError(f"implausible Berlin day length: {span_hours} h for {delivery_date}")

    return CaptureWindow(
        pulled_at_utc=pulled_at_utc,
        local_pull_time=local_pull_time,
        utc_offset=format_offset(local_pull_time),
        pull_local_date=pull_local_date,
        delivery_date=delivery_date,
        gate_at_utc=gate_local.astimezone(UTC),
        window_start_utc=window_start_utc,
        window_end_utc=window_end_utc,
        day_length_hours=int(span_hours),
    )
