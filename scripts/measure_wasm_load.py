#!/usr/bin/env python3
"""Serve the WASM export the way Hugging Face serves a Static Space, and count what a visitor downloads.

CP-3B item 4: network dependencies measured and disclosed, not described. This
page necessarily reaches a CDN for Pyodide and its wheels; the question is what
it costs, on the platform it will actually run on.

**The serving model is measured platform behaviour, not an assumption** --
checked on live public Static Spaces, 2026-09-15, read-only:

* Text files are served directly: `200`, **no compression** even to a client
  sending `Accept-Encoding: gzip, deflate, br`, an `ETag`, no `cache-control`.
  (Round 1 of this measurement gzipped them on the premise the platform would;
  the Integration Critic caught it.)
* Binary files are stored through Xet and served as `302` with
  `cache-control: no-store` (a ~1,048-byte body) to `us.aws.cdn.hf.co`, with a
  signed URL that **changes on every request**. Both hops send
  `access-control-allow-origin: *`. Because the URL rotates, a browser can never
  reuse a cached copy: binary files are fetched again on every visit.

`--emulate-hf` reproduces both on loopback: the app origin serves text with
ETag/304 and redirects binaries to a second origin (port + 1) standing in for
`us.aws.cdn.hf.co`, with a rotating query. A real browser then measures a cold
first visit and a repeat visit, and proves the page still works through the
redirects. Fresh ports give a cold cache, because the HTTP cache key includes
the port.

    uv run python scripts/measure_wasm_load.py --emulate-hf --port 8850 --log /tmp/wire.jsonl
    uv run python scripts/measure_wasm_load.py --replay reports/cp3b/cold_load_paths.jsonl
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import mimetypes
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

#: The live 302 body length observed on a Static Space redirect, 2026-09-15.
HF_REDIRECT_BODY_BYTES = 1048

_counter = itertools.count()


def is_binary(path: Path) -> bool:
    """The Hub's test, as closely as it can be observed: a NUL byte or non-UTF-8 content."""
    head = path.read_bytes()[:8192]
    if b"\x00" in head:
        return True
    try:
        head.decode("utf-8")
        return False
    except UnicodeDecodeError:
        return True


def _etag(raw: bytes) -> str:
    return '"' + hashlib.sha1(raw).hexdigest() + '"'


def _log(log_path: Path, record: dict) -> None:
    with _lock:
        with open(log_path, "a") as handle:
            handle.write(json.dumps(record) + "\n")


_lock = threading.Lock()


class AppHandler(SimpleHTTPRequestHandler):
    """The Space's static host."""

    # HTTP/1.1, as Hugging Face serves it. The stdlib default is HTTP/1.0, and
    # Chrome ignores ETag validators on HTTP/1.0 responses -- the first repeat-visit
    # measurement re-downloaded every file for that reason, and was wrongly
    # attributed to the browser's cache. Caught in an Integration review.
    protocol_version = "HTTP/1.1"

    def __init__(self, *args, log_path: Path, cdn_port: int | None, **kwargs):
        self.log_path = log_path
        self.cdn_port = cdn_port
        super().__init__(*args, **kwargs)

    def log_message(self, *args):  # quiet
        pass

    def do_GET(self):  # noqa: N802
        clean = self.path.split("?", 1)[0]
        path = Path(self.translate_path(clean))
        if path.is_dir():
            path = path / "index.html"
        if not path.is_file():
            return super().do_GET()

        if self.cdn_port is not None and is_binary(path):
            location = (
                f"http://127.0.0.1:{self.cdn_port}{clean}"
                f"?Expires={next(_counter)}&Signature={'x' * 900}"
            )
            body = b"Found. Redirecting to " + location.encode()
            body = body.ljust(HF_REDIRECT_BODY_BYTES, b" ")[:HF_REDIRECT_BODY_BYTES]
            self.send_response(302)
            self.send_header("Location", location)
            self.send_header("Cache-Control", "no-store")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            _log(self.log_path, {"origin": "app", "path": clean, "status": 302, "wire_bytes": len(body)})
            return

        raw = path.read_bytes()
        tag = _etag(raw)
        if self.headers.get("If-None-Match") == tag:
            self.send_response(304)
            self.send_header("ETag", tag)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", "0")
            self.end_headers()
            _log(self.log_path, {"origin": "app", "path": clean, "status": 304, "wire_bytes": 0})
            return
        self.send_response(200)
        self.send_header("Content-Type", mimetypes.guess_type(str(path))[0] or "application/octet-stream")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("ETag", tag)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(raw)
        _log(self.log_path, {"origin": "app", "path": clean, "status": 200, "wire_bytes": len(raw)})


class CdnHandler(SimpleHTTPRequestHandler):
    """Stands in for us.aws.cdn.hf.co: bytes with CORS and an ETag, no cache-control."""

    protocol_version = "HTTP/1.1"

    def __init__(self, *args, log_path: Path, **kwargs):
        self.log_path = log_path
        super().__init__(*args, **kwargs)

    def log_message(self, *args):  # quiet
        pass

    def do_GET(self):  # noqa: N802
        clean = self.path.split("?", 1)[0]
        path = Path(self.translate_path(clean))
        if not path.is_file():
            return super().do_GET()
        raw = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mimetypes.guess_type(str(path))[0] or "application/octet-stream")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("ETag", _etag(raw))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(raw)
        _log(self.log_path, {"origin": "cdn", "path": clean, "status": 200, "wire_bytes": len(raw)})


def replay(paths_log: Path, directory: Path) -> dict:
    """First-visit bytes for a recorded cold load, recomputed on the current bundle.

    The request set -- including which redirects the browser actually followed
    to the CDN origin -- comes from a real browser's first visit. This re-applies
    the serving model to those exact requests so the published figure describes
    the final bundle without re-running a browser after every regeneration.
    """
    app_paths, cdn_paths = [], []
    for line in paths_log.read_text().splitlines():
        if not line.strip():
            continue
        entry = json.loads(line)
        path = entry["path"].split("?", 1)[0]
        bucket = cdn_paths if entry.get("origin") == "cdn" else app_paths
        if path not in bucket:
            bucket.append(path)
    app_bytes = cdn_bytes = redirects = 0
    for path in app_paths:
        file = directory / path.lstrip("/")
        if file.is_dir() or path == "/":
            file = file / "index.html"
        if is_binary(file):
            redirects += 1
            app_bytes += HF_REDIRECT_BODY_BYTES
        else:
            app_bytes += file.stat().st_size
    for path in cdn_paths:
        cdn_bytes += (directory / path.lstrip("/")).stat().st_size
    return {
        "app_requests": len(app_paths), "app_bytes": app_bytes, "redirects": redirects,
        "cdn_requests": len(cdn_paths), "cdn_bytes": cdn_bytes,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8850)
    parser.add_argument("--directory", default="dist/space-wasm")
    parser.add_argument("--log", type=Path, default=Path("/tmp/wasm_wire.jsonl"))
    parser.add_argument("--emulate-hf", action="store_true", help="binary files 302 to a CDN origin on port+1")
    parser.add_argument("--replay", type=Path, default=None)
    args = parser.parse_args()
    if args.replay:
        print(json.dumps(replay(args.replay, Path(args.directory))))
        return 0

    args.log.write_text("")
    cdn_port = args.port + 1 if args.emulate_hf else None
    app = ThreadingHTTPServer(
        ("127.0.0.1", args.port),
        partial(AppHandler, directory=args.directory, log_path=args.log, cdn_port=cdn_port),
    )
    if cdn_port:
        cdn = ThreadingHTTPServer(
            ("127.0.0.1", cdn_port), partial(CdnHandler, directory=args.directory, log_path=args.log)
        )
        threading.Thread(target=cdn.serve_forever, daemon=True).start()
    print(
        f"app http://127.0.0.1:{args.port}"
        + (f", CDN stand-in http://127.0.0.1:{cdn_port}" if cdn_port else "")
        + f" (uncompressed, ETag, binary -> no-store 302); logging to {args.log}"
    )
    app.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
