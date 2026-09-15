#!/usr/bin/env python3
"""Serve the WASM export while counting exactly what a cold visitor downloads.

CP-3B item 4: the network dependencies are measured and disclosed, not
described. Unlike `docs/index.html` -- which fetches nothing and whose
zero-runtime-calls property must not regress -- this page necessarily reaches a
CDN for Pyodide and its wheels, and pulls the nine boosters from its own origin.
Publishing the number is the price of that choice.

This serves on a fresh port so the browser's HTTP cache is cold (the cache key
includes the port), and logs the compressed bytes actually put on the wire for
every same-origin request. Cross-origin CDN traffic is counted in the browser
from the Resource Timing API, by `scripts/record_wasm_load.py`.

    uv run python scripts/measure_wasm_load.py --port 8821 --log /tmp/wire.jsonl
"""

from __future__ import annotations

import argparse
import gzip
import json
import mimetypes
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

#: Hugging Face serves Static Spaces through a CDN with compression on, so a
#: measurement taken against an uncompressed local server would flatter nothing
#: and mislead about everything. These are the types a CDN compresses.
COMPRESSIBLE = {
    ".html", ".js", ".css", ".json", ".txt", ".py", ".svg", ".map", ".webmanifest", ".wasm",
}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, log_path: Path, **kwargs):
        self.log_path = log_path
        super().__init__(*args, **kwargs)

    def log_message(self, *args):  # quiet
        pass

    def do_GET(self):  # noqa: N802
        path = Path(self.translate_path(self.path))
        if path.is_dir():
            path = path / "index.html"
        if not path.is_file():
            return super().do_GET()
        raw = path.read_bytes()
        suffix = path.suffix.lower()
        accepts_gzip = "gzip" in self.headers.get("Accept-Encoding", "")
        if suffix in COMPRESSIBLE and accepts_gzip:
            body, encoding = gzip.compress(raw, 6), "gzip"
        else:
            body, encoding = raw, None
        self.send_response(200)
        self.send_header("Content-Type", mimetypes.guess_type(str(path))[0] or "application/octet-stream")
        self.send_header("Content-Length", str(len(body)))
        if encoding:
            self.send_header("Content-Encoding", encoding)
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        self.end_headers()
        self.wfile.write(body)
        with open(self.log_path, "a") as handle:
            handle.write(
                json.dumps(
                    {
                        "path": self.path,
                        "wire_bytes": len(body),
                        "raw_bytes": len(raw),
                        "encoding": encoding,
                    }
                )
                + "\n"
            )


def replay(paths_log: Path, directory: Path) -> tuple[int, int]:
    """Same-origin wire bytes for a recorded cold load, recomputed on the current bundle.

    The request set comes from a real browser cold load (the server log); this
    re-applies the server's own gzip rule to those exact paths. It lets the
    published byte count describe the final bundle without re-running a browser
    after every regeneration of a few-kilobyte JSON file.
    """
    seen = {}
    for line in paths_log.read_text().splitlines():
        if line.strip():
            entry = json.loads(line)
            seen.setdefault(entry["path"].split("?", 1)[0], entry)
    total = 0
    for path in seen:
        file = directory / path.lstrip("/")
        if file.is_dir() or path == "/":
            file = file / "index.html"
        raw = file.read_bytes()
        total += len(gzip.compress(raw, 6)) if file.suffix.lower() in COMPRESSIBLE else len(raw)
    return len(seen), total


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8821)
    parser.add_argument("--directory", default="dist/space-wasm")
    parser.add_argument("--log", type=Path, default=Path("/tmp/wasm_wire.jsonl"))
    parser.add_argument("--replay", type=Path, default=None,
                        help="recompute same-origin bytes for a recorded cold-load path log, then exit")
    args = parser.parse_args()
    if args.replay:
        requests, total = replay(args.replay, Path(args.directory))
        print(json.dumps({"same_origin_requests": requests, "same_origin_wire_bytes": total}))
        return 0
    args.log.write_text("")
    handler = partial(Handler, directory=args.directory, log_path=args.log)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    print(f"serving {args.directory} on http://127.0.0.1:{args.port} (gzip on), logging to {args.log}")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
