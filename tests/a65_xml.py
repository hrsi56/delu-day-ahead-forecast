"""Builder for small, realistic A65/A01 GL_MarketDocument fixtures.

Mirrors the shape of a real DE-LU response (single TimeSeries, single Period,
``curveType`` A03, ``PT15M`` resolution, ``<Point><position>/<quantity>``).
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

NS = "urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0"

RESOLUTION_STEP = {
    "PT15M": timedelta(minutes=15),
    "PT30M": timedelta(minutes=30),
    "PT60M": timedelta(hours=1),
    "PT1H": timedelta(hours=1),
}


def _stamp(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


def _stamp_seconds(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def build_period(
    *,
    start_utc: datetime,
    resolution: str,
    quantities: list[float | None],
    positions: list[int] | None = None,
    end_utc: datetime | None = None,
) -> str:
    """One ``<Period>``. ``positions`` defaults to 1..len(quantities).

    A ``None`` quantity emits an empty ``<quantity/>`` (a NaN slot); omitting a
    position from ``positions`` leaves a gap.
    """
    step = RESOLUTION_STEP[resolution]
    if positions is None:
        positions = list(range(1, len(quantities) + 1))
    if end_utc is None:
        end_utc = start_utc + step * max(positions)
    points = []
    for position, quantity in zip(positions, quantities, strict=True):
        value = "" if quantity is None else f"{quantity:.6f}"
        points.append(
            "            <Point>\n"
            f"              <position>{position}</position>\n"
            f"              <quantity>{value}</quantity>\n"
            "            </Point>"
        )
    body = "\n".join(points)
    return (
        "        <Period>\n"
        "          <timeInterval>\n"
        f"            <start>{_stamp(start_utc)}</start>\n"
        f"            <end>{_stamp(end_utc)}</end>\n"
        "          </timeInterval>\n"
        f"          <resolution>{resolution}</resolution>\n"
        f"{body}\n"
        "        </Period>"
    )


def build_document(
    *,
    periods: list[str],
    created_at_utc: datetime,
    doc_start_utc: datetime,
    doc_end_utc: datetime,
    curve_type: str = "A03",
    one_timeseries_per_period: bool = False,
) -> str:
    """Wrap ``periods`` in a GL_MarketDocument."""
    if one_timeseries_per_period:
        series_blocks = [_timeseries([period], curve_type, index + 1) for index, period in enumerate(periods)]
    else:
        series_blocks = [_timeseries(periods, curve_type, 1)]
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        f'<GL_MarketDocument xmlns="{NS}">\n'
        "  <mRID>fixture0000000000000000000000000</mRID>\n"
        "  <revisionNumber>1</revisionNumber>\n"
        "  <type>A65</type>\n"
        "  <process.processType>A01</process.processType>\n"
        '  <sender_MarketParticipant.mRID codingScheme="A01">10X1001A1001A450'
        "</sender_MarketParticipant.mRID>\n"
        "  <sender_MarketParticipant.marketRole.type>A32</sender_MarketParticipant.marketRole.type>\n"
        '  <receiver_MarketParticipant.mRID codingScheme="A01">10X1001A1001A450'
        "</receiver_MarketParticipant.mRID>\n"
        "  <receiver_MarketParticipant.marketRole.type>A33"
        "</receiver_MarketParticipant.marketRole.type>\n"
        f"  <createdDateTime>{_stamp_seconds(created_at_utc)}</createdDateTime>\n"
        "  <time_Period.timeInterval>\n"
        f"    <start>{_stamp(doc_start_utc)}</start>\n"
        f"    <end>{_stamp(doc_end_utc)}</end>\n"
        "  </time_Period.timeInterval>\n"
        + "\n".join(series_blocks)
        + "\n</GL_MarketDocument>\n"
    )


def _timeseries(periods: list[str], curve_type: str, mrid: int) -> str:
    return (
        "    <TimeSeries>\n"
        f"      <mRID>{mrid}</mRID>\n"
        "      <businessType>A04</businessType>\n"
        "      <objectAggregation>A01</objectAggregation>\n"
        '      <outBiddingZone_Domain.mRID codingScheme="A01">10Y1001A1001A82H'
        "</outBiddingZone_Domain.mRID>\n"
        "      <quantity_Measure_Unit.name>MAW</quantity_Measure_Unit.name>\n"
        f"      <curveType>{curve_type}</curveType>\n"
        + "\n".join(periods)
        + "\n    </TimeSeries>"
    )


def synthetic_load(index: int) -> float:
    """A plausible DE-LU load shape, deterministic and readable."""
    return round(42000.0 + 6000.0 * (index % 96) / 96.0, 6)


def build_day(
    *,
    start_utc: datetime,
    slots: int,
    resolution: str = "PT15M",
    created_at_utc: datetime | None = None,
    drop_positions: set[int] | None = None,
    null_positions: set[int] | None = None,
    truncate_after: int | None = None,
    curve_type: str = "A03",
) -> str:
    """A whole delivery day, optionally damaged in one specific way."""
    step = RESOLUTION_STEP[resolution]
    end_utc = start_utc + step * slots
    drop_positions = drop_positions or set()
    null_positions = null_positions or set()
    positions: list[int] = []
    quantities: list[float | None] = []
    for position in range(1, slots + 1):
        if position in drop_positions:
            continue
        if truncate_after is not None and position > truncate_after:
            continue
        positions.append(position)
        quantities.append(None if position in null_positions else synthetic_load(position))
    if created_at_utc is None:
        created_at_utc = start_utc - timedelta(hours=12)
    period = build_period(
        start_utc=start_utc,
        resolution=resolution,
        quantities=quantities,
        positions=positions,
        end_utc=end_utc,
    )
    return build_document(
        periods=[period],
        created_at_utc=created_at_utc,
        doc_start_utc=start_utc,
        doc_end_utc=end_utc,
        curve_type=curve_type,
    )
