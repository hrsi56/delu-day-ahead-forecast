"""Point-in-time capture instrument for ENTSO-E A65/A01 on DE-LU.

One capture attempt -> one immutable, hash-chained ledger row (capstone_V6_5.md
Section 3 capture contract, Section 4.0 DST rules, Section 12 M0.5/CP-0).
"""
from __future__ import annotations

INSTRUMENT_VERSION = "pit-capture/1.0.0"

SOURCE = "ENTSO-E Transparency Platform"
SOURCE_ENDPOINT = "https://web-api.tp.entsoe.eu/api"
DOCUMENT_TYPE = "A65"
PROCESS_TYPE = "A01"
BIDDING_ZONE = "DE-LU"
BIDDING_ZONE_EIC = "10Y1001A1001A82H"

#: Recorded verbatim in every ledger row: a successful capture proves only that
#: the D+1 vector was *observed available by* ``pulled_at_utc``. It is never
#: rewritten as the source's first-publication time (Section 3, CP-0 item 3).
PULLED_AT_SEMANTICS = (
    "observed-available-by: pulled_at_utc is the supplied observation instant, "
    "not the source's first-publication time"
)

__all__ = [
    "INSTRUMENT_VERSION",
    "SOURCE",
    "SOURCE_ENDPOINT",
    "DOCUMENT_TYPE",
    "PROCESS_TYPE",
    "BIDDING_ZONE",
    "BIDDING_ZONE_EIC",
    "PULLED_AT_SEMANTICS",
]
