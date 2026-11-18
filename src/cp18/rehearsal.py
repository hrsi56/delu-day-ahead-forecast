"""CP-18d's rehearsal stand-ins: dry runs on development days only (through 2026-09-06), never a live day.

The rehearsal (the brief's item 5) shows, on the `macos-26` runner of the public scratch repository with fake
credentials only: a missed acquisition issued with the load forecast fetched after the cutoff and labelled; and the
earlier acquisition's in-job wait. Development days have no live retrieval of their load forecast (their stored
history rests on ruling 1's exception), so the rehearsal needs a stand-in source for it:

- **`StandInLoadForecast`** answers ENTSO-E's A65 load-forecast request (the live route, `cp18.live.entsoe`) for a
  development day: "no matching data" (ENTSO-E's own acknowledgement) before `published_at`, and from then on the
  development snapshot's load forecast of that day, rendered in A65's shape (`cp18.live.recorded.render_entsoe_day`),
  its `createdDateTime` the stand-in's clock. Its responses are `live` in provenance, so the availability rule judges
  them as it judges a live retrieval, by their time against the cutoff; every archive record they make names the
  stand-in as its origin (`origin`), so no record passes for a real retrieval. Any other request goes to `fallback`
  (the dry run's recorded replay), or is a miss.
- **`real_time_clock(start)`**: a simulated clock that advances with the real one, so the acquisition's polling waits
  for real while its cutoff is a development day's.

Every day served passes `cp25.guard.admit_delivery_day` (the development boundary), whatever mode the caller is in.
"""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
import time
from pathlib import Path

from cp25 import guard

UTC = timezone.utc
ORIGIN = ("CP-18d rehearsal stand-in: the development snapshot's load forecast rendered in ENTSO-E's A65 shape, "
          'served at the simulated clock (dry run on development days; not a retrieval)')
ACK = (b'<?xml version="1.0" encoding="utf-8"?><Acknowledgement_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-1:'
       b'acknowledgementdocument:7:0"><mRID>rehearsal</mRID><createdDateTime>{stamp}</createdDateTime><Reason>'
       b'<code>999</code><text>No matching data found</text></Reason></Acknowledgement_MarketDocument>')


def real_time_clock(start: datetime):
    """`start`, advancing with the real clock."""
    if start.tzinfo is None:
        raise ValueError('a naive simulated start')
    t0 = time.monotonic()
    return lambda: start.astimezone(UTC) + timedelta(seconds=time.monotonic() - t0)


class StandInLoadForecast:
    """A transport (`cp18.live.transport.Transport`) for the rehearsal: A65 from the development snapshot."""

    origin = ORIGIN

    def __init__(self, root, clock, published_at: datetime, fallback=None):
        from .live.recorded import snapshot
        self.root, self.clock, self.published_at, self.fallback = Path(root), clock, published_at, fallback
        self._snapshot = snapshot(self.root)
        self.sent: list[dict] = []

    def send(self, request):
        from cp15.data import day_hours  # noqa: F401 - the renderer's own dependency, imported early on purpose
        from .live import entsoe
        from .live.recorded import render_entsoe_day
        from .live.transport import ReplayMiss, Response
        request.admit()
        now = self.clock()
        stamp = now.astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
        params = dict(request.params)
        if request.url == entsoe.API and params.get('documentType') == 'A65':
            days = request.days()
            for d in days:
                guard.admit_delivery_day(d)
            self.sent.append({'url': request.url, 'days': [str(d) for d in days], 'at': stamp,
                              'published': now >= self.published_at})
            if now < self.published_at or len(days) != 1:
                return Response(200, {'Content-Type': 'application/xml'}, ACK.replace(b'{stamp}', stamp.encode()),
                                stamp, 'live', ORIGIN)
            from .live import archive as AR
            body = render_entsoe_day(self._snapshot, 'load_forecast', days[0])
            body = body.replace(AR.SNAPSHOT_PULLED_UTC.encode(), stamp.encode())
            return Response(200, {'Content-Type': 'application/xml'}, body, stamp, 'live', ORIGIN)
        if self.fallback is not None:
            return self.fallback.send(request)
        raise ReplayMiss('not served by the rehearsal stand-in')


def published_before(day: date, minutes: int) -> datetime:
    """An instant `minutes` before D's cutoff (the stand-in's publication in a late-copy rehearsal)."""
    guard.admit_delivery_day(day)
    return guard.issue_time(day) - timedelta(minutes=minutes)
