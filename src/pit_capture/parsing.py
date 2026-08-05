"""Parse the *already-retrieved* A65/A01 payload.

Single-request integrity: this module never touches the network. Every reported
count, timestamp and completeness figure is derived from the same bytes that
were hashed and written to the raw artifact, so the evidence and the verdict
cannot drift apart.
"""
from __future__ import annotations

import math
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

from .timewindow import UTC, resolution_to_timedelta


class PayloadParseError(ValueError):
    """The payload is not a parseable A65 GL_MarketDocument."""


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _text(element: ET.Element, name: str) -> str | None:
    for child in element:
        if _local(child.tag) == name:
            return (child.text or "").strip()
    return None


def _children(element: ET.Element, name: str) -> list[ET.Element]:
    return [child for child in element if _local(child.tag) == name]


def _parse_entsoe_stamp(text: str) -> datetime:
    """ENTSO-E stamps are UTC: ``2026-08-05T22:00Z`` or ``...:04Z``.

    A malformed stamp (``createdDateTime`` or a Period ``start``/``end``) is a
    payload defect, not a crash: it is reported as ``PayloadParseError`` so the
    attempt still ends in a ``not_qualifying`` ledger entry instead of an
    unhandled exception.
    """
    raw = text.strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError as exc:
        raise PayloadParseError(f"unparseable ENTSO-E timestamp {text!r}: {exc}") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(UTC)


@dataclass
class ParsedPeriod:
    start_utc: datetime
    end_utc: datetime
    resolution: str
    positions: list[int]
    missing_positions: list[int]
    null_positions: list[int]


@dataclass
class ParsedDocument:
    """Everything the ledger needs, read out of one payload."""

    created_at_utc: datetime | None
    document_type: str | None
    process_type: str | None
    curve_types: list[str]
    resolutions: list[str]
    periods: list[ParsedPeriod] = field(default_factory=list)
    #: delivery timestamp (UTC) -> quantity; ``None`` marks an explicitly empty
    #: or non-numeric quantity (a NaN slot).
    points: dict[datetime, float | None] = field(default_factory=dict)
    timeseries_count: int = 0

    @property
    def resolution(self) -> str | None:
        """The single detected resolution, or ``None`` when absent/mixed."""
        if len(self.resolutions) == 1:
            return self.resolutions[0]
        return None

    @property
    def mixed_resolutions(self) -> bool:
        return len(self.resolutions) > 1


def parse_a65_payload(xml_text: str) -> ParsedDocument:
    """Parse an A65 GL_MarketDocument string into positions and timestamps.

    Point positions are honoured literally: a position that is absent from a
    Period is recorded as a gap. ENTSO-E ``curveType`` A03 (variable-sized
    block) would in principle allow an omitted point to mean "the previous
    value repeats"; this instrument deliberately does not infer such values,
    because the capture contract asks whether the D+1 vector was *published*,
    not whether it can be reconstructed. ``curve_types`` is recorded in the
    ledger so an auditor can see which convention the payload used.
    """
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        raise PayloadParseError(f"payload is not well-formed XML: {exc}") from exc

    if _local(root.tag) != "GL_MarketDocument":
        raise PayloadParseError(
            f"unexpected root element {_local(root.tag)!r}; expected GL_MarketDocument"
        )

    created_raw = _text(root, "createdDateTime")
    created_at = _parse_entsoe_stamp(created_raw) if created_raw else None

    process_type = None
    for child in root:
        if _local(child.tag).endswith("processType"):
            process_type = (child.text or "").strip()
            break

    doc = ParsedDocument(
        created_at_utc=created_at,
        document_type=_text(root, "type"),
        process_type=process_type,
        curve_types=[],
        resolutions=[],
    )

    for series in _children(root, "TimeSeries"):
        doc.timeseries_count += 1
        curve_type = _text(series, "curveType")
        if curve_type and curve_type not in doc.curve_types:
            doc.curve_types.append(curve_type)

        for period in _children(series, "Period"):
            resolution = _text(period, "resolution")
            if not resolution:
                raise PayloadParseError("Period is missing <resolution>")
            if resolution not in doc.resolutions:
                doc.resolutions.append(resolution)

            interval = _children(period, "timeInterval")
            if not interval:
                raise PayloadParseError("Period is missing <timeInterval>")
            start_raw = _text(interval[0], "start")
            end_raw = _text(interval[0], "end")
            if not start_raw or not end_raw:
                raise PayloadParseError("Period timeInterval is missing start/end")
            start_utc = _parse_entsoe_stamp(start_raw)
            end_utc = _parse_entsoe_stamp(end_raw)

            try:
                step = resolution_to_timedelta(resolution)
            except ValueError as exc:
                raise PayloadParseError(str(exc)) from exc

            positions: list[int] = []
            null_positions: list[int] = []
            for point in _children(period, "Point"):
                position_raw = _text(point, "position")
                if position_raw is None:
                    raise PayloadParseError("Point is missing <position>")
                try:
                    position = int(position_raw)
                except ValueError as exc:
                    raise PayloadParseError(f"non-integer <position> {position_raw!r}") from exc
                quantity_raw = _text(point, "quantity")
                value: float | None
                if quantity_raw is None or quantity_raw == "":
                    value = None
                else:
                    try:
                        value = float(quantity_raw)
                    except ValueError:
                        value = None
                if value is not None and math.isnan(value):
                    value = None
                if value is None:
                    null_positions.append(position)
                positions.append(position)
                doc.points[start_utc + (position - 1) * step] = value

            slots = int((end_utc - start_utc) // step) if end_utc > start_utc else 0
            declared = set(range(1, slots + 1))
            missing = sorted(declared - set(positions))
            doc.periods.append(
                ParsedPeriod(
                    start_utc=start_utc,
                    end_utc=end_utc,
                    resolution=resolution,
                    positions=sorted(positions),
                    missing_positions=missing,
                    null_positions=sorted(null_positions),
                )
            )

    return doc


@dataclass
class Completeness:
    """Row counts and timestamps for one delivery-day window."""

    resolution: str | None
    expected_rows: int | None
    observed_rows: int
    completeness_ratio: float | None
    first_delivery_timestamp_utc: datetime | None
    last_delivery_timestamp_utc: datetime | None
    latest_fully_populated_timestamp_utc: datetime | None
    missing_slots: int | None
    null_slots: int
    points_outside_window: int
    issues: list[str]


def assess_completeness(doc: ParsedDocument, window) -> Completeness:
    """Judge the D+1 vector against the DST-aware expected grid.

    ``latest_fully_populated_timestamp_utc`` is the end of the *leading
    contiguous* fully-populated run: the last expected timestamp at or before
    which every expected slot is populated. It is not simply the last non-null
    row -- a gap in the middle caps it at the slot before the gap, even when
    later slots carry values.
    """
    issues: list[str] = []
    all_stamps = sorted(doc.points)
    first_ts = all_stamps[0] if all_stamps else None
    last_ts = all_stamps[-1] if all_stamps else None

    if not doc.resolutions:
        issues.append("payload contains no Period/resolution")
        return Completeness(
            resolution=None,
            expected_rows=None,
            observed_rows=0,
            completeness_ratio=None,
            first_delivery_timestamp_utc=first_ts,
            last_delivery_timestamp_utc=last_ts,
            latest_fully_populated_timestamp_utc=None,
            missing_slots=None,
            null_slots=0,
            points_outside_window=len(doc.points),
            issues=issues,
        )

    if doc.mixed_resolutions:
        issues.append(
            "payload mixes resolutions "
            + "/".join(doc.resolutions)
            + "; expected row count is undefined"
        )
        return Completeness(
            resolution=None,
            expected_rows=None,
            observed_rows=len(doc.points),
            completeness_ratio=None,
            first_delivery_timestamp_utc=first_ts,
            last_delivery_timestamp_utc=last_ts,
            latest_fully_populated_timestamp_utc=None,
            missing_slots=None,
            null_slots=sum(1 for v in doc.points.values() if v is None),
            points_outside_window=0,
            issues=issues,
        )

    resolution = doc.resolutions[0]
    try:
        expected_rows = window.expected_rows(resolution)
        grid = window.expected_grid(resolution)
    except ValueError as exc:
        issues.append(str(exc))
        return Completeness(
            resolution=resolution,
            expected_rows=None,
            observed_rows=len(doc.points),
            completeness_ratio=None,
            first_delivery_timestamp_utc=first_ts,
            last_delivery_timestamp_utc=last_ts,
            latest_fully_populated_timestamp_utc=None,
            missing_slots=None,
            null_slots=sum(1 for v in doc.points.values() if v is None),
            points_outside_window=0,
            issues=issues,
        )

    grid_set = set(grid)
    observed_rows = 0
    missing_slots = 0
    null_slots = 0
    latest_fully_populated: datetime | None = None
    run_broken = False
    for slot in grid:
        value = doc.points.get(slot, "__absent__")
        populated = value != "__absent__" and value is not None
        if populated:
            observed_rows += 1
            if not run_broken:
                latest_fully_populated = slot
        else:
            run_broken = True
            if value == "__absent__":
                missing_slots += 1
            else:
                null_slots += 1

    outside = sum(1 for stamp in doc.points if stamp not in grid_set)
    if missing_slots:
        issues.append(f"{missing_slots} expected slot(s) absent from the payload")
    if null_slots:
        issues.append(f"{null_slots} expected slot(s) present but empty/NaN")
    if outside:
        issues.append(f"{outside} point(s) fall outside the D+1 delivery window")

    return Completeness(
        resolution=resolution,
        expected_rows=expected_rows,
        observed_rows=observed_rows,
        completeness_ratio=round(observed_rows / expected_rows, 6) if expected_rows else None,
        first_delivery_timestamp_utc=first_ts,
        last_delivery_timestamp_utc=last_ts,
        latest_fully_populated_timestamp_utc=latest_fully_populated,
        missing_slots=missing_slots,
        null_slots=null_slots,
        points_outside_window=outside,
        issues=issues,
    )
