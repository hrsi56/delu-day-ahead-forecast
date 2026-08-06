"""CLI entry point: one capture attempt per invocation.

    python -m pit_capture.cli --pulled-at-utc <ISO8601> \
        [--delivery-date YYYY-MM-DD] [--ledger-path PATH] [--raw-dir PATH]
"""

from __future__ import annotations

import argparse
import os
from datetime import date, datetime, timezone
from pathlib import Path

from .capture import capture_attempt

DEFAULT_LEDGER_PATH = Path("data/pit_capture/ledger.jsonl")
DEFAULT_RAW_DIR = Path("data/pit_capture/raw")


def _parse_instant(value: str) -> datetime:
    """Parse an explicit, unambiguous ISO8601 UTC instant. A bare
    offset-less string is rejected, since the entire point of `pulled_at` is
    that it is unambiguous UTC."""
    candidate = value.strip()
    if candidate.endswith("Z") or candidate.endswith("z"):
        candidate = candidate[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"--pulled-at-utc must be an ISO8601 instant with an explicit UTC "
            f"offset (e.g. '2026-08-06T12:00:00Z' or "
            f"'2026-08-06T12:00:00+00:00'), got {value!r}"
        )
    if parsed.tzinfo is None:
        raise argparse.ArgumentTypeError(
            f"--pulled-at-utc must include an explicit UTC offset (a bare "
            f"offset-less instant is ambiguous), got {value!r}"
        )
    return parsed.astimezone(timezone.utc)


def _parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"--delivery-date must be YYYY-MM-DD, got {value!r}")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m pit_capture.cli",
        description="Perform one ENTSO-E A65/A01 DE-LU capture attempt and append it to the ledger.",
    )
    parser.add_argument(
        "--pulled-at-utc",
        required=True,
        type=_parse_instant,
        help="Explicit UTC instant this capture attempt is being made at, e.g. 2026-08-06T12:00:00Z",
    )
    parser.add_argument(
        "--delivery-date",
        type=_parse_date,
        default=None,
        help="Delivery day to capture (YYYY-MM-DD). Defaults to (Berlin-local calendar date of --pulled-at-utc) + 1 day.",
    )
    parser.add_argument("--ledger-path", type=Path, default=DEFAULT_LEDGER_PATH)
    parser.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW_DIR)
    return parser


def main(argv=None) -> int:
    args = build_arg_parser().parse_args(argv)

    token = os.environ.get("ENTSOE_API_TOKEN")
    if not token:
        raise RuntimeError(
            "ENTSOE_API_TOKEN is not set in the environment; refusing to run "
            "(no partial ledger write)."
        )

    entry = capture_attempt(
        pulled_at_utc=args.pulled_at_utc,
        delivery_date=args.delivery_date,
        token=token,
        ledger_path=args.ledger_path,
        raw_dir=args.raw_dir,
    )
    print(
        f"delivery_date={entry.delivery_date} status={entry.status} "
        f"qualifying={entry.qualifying} reason={entry.qualifying_reason}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
