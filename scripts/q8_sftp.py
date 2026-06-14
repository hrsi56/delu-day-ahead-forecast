"""Q8 -- ENTSO-E SFTP bulk path reachability (capstone S3, R-3).

The ENTSO-E Transparency Platform also offers an account-scoped SFTP server
with monthly bulk CSVs, named in the capstone as a second ingestion route if
the chunked API proves slow.

This probe only checks *network* reachability of the SFTP host on port 22
from the current machine -- it does not attempt to authenticate (SFTP
credentials are separate from the ENTSOE_API_TOKEN and are not present in
this environment).

Usage: uv run scripts/q8_sftp.py
"""
from __future__ import annotations

import socket
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from spike.entsoe_helpers import write_evidence

SFTP_HOST = "sftp-transparency.entsoe.eu"
SFTP_PORT = 22


def main() -> None:
    evidence = {"probe": "q8_sftp", "host": SFTP_HOST, "port": SFTP_PORT}
    try:
        with socket.create_connection((SFTP_HOST, SFTP_PORT), timeout=10):
            evidence["status"] = "REACHABLE"
            print(f"{SFTP_HOST}:{SFTP_PORT} -- TCP connect OK")
    except OSError as e:
        evidence["status"] = "UNREACHABLE"
        evidence["error"] = f"{type(e).__name__}: {e}"
        print(f"{SFTP_HOST}:{SFTP_PORT} -- TCP connect FAILED: {type(e).__name__}: {e}")
        print("This commonly means the sandbox's outbound network policy blocks non-HTTP(S) ports.")
        print(f"Re-run on Yarden's M3 to check the real-world result: nc -zv {SFTP_HOST} {SFTP_PORT}")

    out = write_evidence("q8_sftp", evidence)
    print(f"\nEvidence written to {out}")


if __name__ == "__main__":
    main()
