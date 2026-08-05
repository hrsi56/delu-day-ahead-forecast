"""CLI: ``pit_capture.py capture`` and ``pit_capture.py verify``."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import INSTRUMENT_VERSION
from .capture import (
    DEFAULT_LEDGER,
    DEFAULT_MAX_CLOCK_SKEW_SECONDS,
    DEFAULT_RAW_DIR,
    EXIT_ARTIFACT_CONFLICT,
    EXIT_OK,
    EXIT_USAGE,
    EXIT_VERIFY_FAILED,
    run_capture,
)
from .ledger import LedgerError, verify_ledger
from .timewindow import UsageError, parse_utc_instant

DESCRIPTION = (
    "Point-in-time capture instrument for ENTSO-E A65/A01 (day-ahead total load "
    "forecast) on DE-LU (10Y1001A1001A82H). One attempt, one immutable ledger row."
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pit_capture.py", description=DESCRIPTION)
    parser.add_argument("--version", action="version", version=INSTRUMENT_VERSION)
    sub = parser.add_subparsers(dest="command", required=True)

    capture = sub.add_parser(
        "capture",
        help="perform one capture attempt and append one ledger row",
        description="Perform one A65/A01 capture attempt at the supplied UTC instant.",
    )
    capture.add_argument(
        "--at-utc",
        required=True,
        metavar="ISO8601",
        help="observation instant, explicit UTC (e.g. 2026-08-05T08:30:00Z or ...+00:00)",
    )
    capture.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER, help="ledger JSONL path")
    capture.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW_DIR, help="raw artifact dir")
    capture.add_argument(
        "--replay-xml",
        type=Path,
        default=None,
        help="parse this local XML file instead of performing the HTTP request (offline path)",
    )
    capture.add_argument(
        "--max-clock-skew-seconds",
        type=int,
        default=DEFAULT_MAX_CLOCK_SKEW_SECONDS,
        help=f"tolerated |pulled_at_utc - wall clock| (default {DEFAULT_MAX_CLOCK_SKEW_SECONDS})",
    )
    capture.add_argument("--json", action="store_true", help="print the ledger row as JSON")

    verify = sub.add_parser(
        "verify",
        help="re-walk the ledger: row hashes, chain order, raw-artifact hashes",
        description="Verify ledger integrity end to end. Exit 0 only if everything verifies.",
    )
    verify.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER, help="ledger JSONL path")
    verify.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW_DIR, help="raw artifact dir")
    verify.add_argument("--quiet", action="store_true", help="print the summary only")
    return parser


def _cmd_capture(args: argparse.Namespace, parser: argparse.ArgumentParser) -> int:
    try:
        at_utc = parse_utc_instant(args.at_utc)
    except UsageError as exc:
        parser.error(str(exc))  # argparse exits 2; no ledger entry is written

    if args.replay_xml is not None and not Path(args.replay_xml).is_file():
        parser.error(f"--replay-xml file not found: {args.replay_xml}")
    if args.max_clock_skew_seconds < 0:
        parser.error("--max-clock-skew-seconds must be >= 0")

    try:
        result = run_capture(
            at_utc=at_utc,
            ledger_path=Path(args.ledger),
            raw_dir=Path(args.raw_dir),
            replay_xml=Path(args.replay_xml) if args.replay_xml is not None else None,
            max_clock_skew_seconds=args.max_clock_skew_seconds,
        )
    except UsageError as exc:
        parser.error(str(exc))
    except LedgerError as exc:
        print(f"ABORTED (no ledger entry written): {exc}", file=sys.stderr)
        return EXIT_ARTIFACT_CONFLICT

    entry = result.entry
    if args.json:
        print(json.dumps(entry, sort_keys=True, separators=(",", ":"), ensure_ascii=False))
    else:
        print(
            f"entry {entry['entry_index']} appended to {args.ledger}\n"
            f"  capture_mode : {entry['capture_mode']}\n"
            f"  delivery_date: {entry['delivery_date']} "
            f"({entry['day_length_hours']}h, resolution {entry['resolution']})\n"
            f"  pulled_at_utc: {entry['pulled_at_utc']} "
            f"(local {entry['local_pull_time']}, offset {entry['utc_offset']})\n"
            f"  gate_at_utc  : {entry['gate_at_utc']}\n"
            f"  presence     : {entry['presence']} "
            f"({entry['observed_rows']}/{entry['expected_rows']} rows)\n"
            f"  payload      : {entry['payload_sha256']} -> {entry['raw_artifact_path']}\n"
            f"  verdict      : {entry['verdict']} -- {entry['reason']}\n"
            f"  counts_toward_section_3_qualifying_days: "
            f"{entry['counts_toward_section_3_qualifying_days']}"
        )
    return EXIT_OK


def _cmd_verify(args: argparse.Namespace) -> int:
    report = verify_ledger(Path(args.ledger), Path(args.raw_dir))
    for problem in report.problems:
        print(f"LEDGER: {problem}", file=sys.stderr)
    for entry in report.entries:
        if entry.ok:
            if not args.quiet:
                print(f"entry {entry.entry_index} (line {entry.line_number}): OK")
        else:
            for problem in entry.problems:
                print(
                    f"entry {entry.entry_index} (line {entry.line_number}): FAIL: {problem}",
                    file=sys.stderr,
                )
    failed = sum(1 for entry in report.entries if not entry.ok)
    verdict = "OK" if report.ok else "FAILED"
    print(f"{verdict}: {report.entry_count} entries, {failed} failing, ledger {args.ledger}")
    return EXIT_OK if report.ok else EXIT_VERIFY_FAILED


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "capture":
        return _cmd_capture(args, parser)
    if args.command == "verify":
        return _cmd_verify(args)
    parser.error(f"unknown command {args.command!r}")  # pragma: no cover
    return EXIT_USAGE  # pragma: no cover


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
