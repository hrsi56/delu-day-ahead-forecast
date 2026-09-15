#!/usr/bin/env python3
"""Measure a first and a repeat visit to the WASM Space in real Chrome, over the DevTools protocol.

CP-3B item 4: exact hosts, request count and transferred bytes on a cold cache.
Earlier measurements stitched together a server log, the page's own Resource
Timing table and out-of-band HEAD requests, and each seam produced an error an
Integration review caught: an assumed gzip, a missed redirect host, a HEAD that
returns 405, favicon and manifest requests a fresh browser makes but the
measuring browser did not, and an HTTP/1.0 emulator that made a repeat visit
look uncacheable. This replaces the seams with one instrument.

What it does:

1. Serves `dist/space-wasm` with `scripts/measure_wasm_load.py --emulate-hf` on
   fresh ports: text direct over HTTP/1.1 with an ETag, binary files as a
   no-store 302 to a second origin standing in for us.aws.cdn.hf.co.
2. Launches headless Chrome with a brand-new profile, so every cache -- the
   Space's, jsDelivr's, PyPI's -- is genuinely cold.
3. Attaches to the page **and** every worker (Pyodide runs in a Web Worker) and
   records each network request: host, status, redirect hops, whether it came
   from cache, and `encodedDataLength` -- the bytes Chrome actually received,
   headers and body, as encoded on the wire. DevTools is not subject to
   Timing-Allow-Origin, so no size is out of view.
4. Waits until the page reports the identity check, then until the network is
   idle; then visits again in the same profile and records the repeat visit.

    uv run python scripts/record_wasm_load.py            # writes reports/cp3b/cdp_load.json
"""

from __future__ import annotations

import asyncio
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse

import websockets

ROOT = Path(__file__).resolve().parents[1]
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
RECORD = ROOT / "reports" / "cp3b" / "cdp_load.json"
READY_MARKER = "bitwise identical"


def free_port(pair: bool = False) -> int:
    while True:
        with socket.socket() as s:
            s.bind(("127.0.0.1", 0))
            port = s.getsockname()[1]
        if not pair:
            return port
        with socket.socket() as s:
            try:
                s.bind(("127.0.0.1", port + 1))
                return port
            except OSError:
                continue


class CDP:
    def __init__(self, ws):
        self.ws = ws
        self.next_id = 0
        self.pending: dict[int, asyncio.Future] = {}
        self.requests: dict[tuple[str, str], dict] = {}
        self.completed: list[dict] = []
        self.errors: list[str] = []
        self.sessions: dict[str, str] = {}
        self.last_network_event = time.monotonic()
        self.visit = "first"

    async def send(self, method: str, params: dict | None = None, session: str | None = None):
        self.next_id += 1
        message = {"id": self.next_id, "method": method, "params": params or {}}
        if session:
            message["sessionId"] = session
        future = asyncio.get_running_loop().create_future()
        self.pending[self.next_id] = future
        await self.ws.send(json.dumps(message))
        return await asyncio.wait_for(future, 60)

    async def enable(self, session: str) -> None:
        await self.send("Network.enable", {"maxTotalBufferSize": 0}, session)
        await self.send("Runtime.enable", {}, session)
        await self.send(
            "Target.setAutoAttach",
            {"autoAttach": True, "waitForDebuggerOnStart": True, "flatten": True},
            session,
        )
        try:
            await self.send("Runtime.runIfWaitingForDebugger", {}, session)
        except Exception:
            pass

    def _finish(self, key, bytes_, status=None, failed=None):
        entry = self.requests.pop(key, None)
        if entry is None:
            return
        entry["bytes"] = int(bytes_ or 0)
        if status is not None:
            entry["status"] = status
        if failed:
            entry["failed"] = failed
        entry["visit"] = self.visit
        self.completed.append(entry)

    async def reader(self):
        async for raw in self.ws:
            message = json.loads(raw)
            if "id" in message:
                future = self.pending.pop(message["id"], None)
                if future and not future.done():
                    if "error" in message:
                        future.set_exception(RuntimeError(message["error"]))
                    else:
                        future.set_result(message.get("result", {}))
                continue
            method, params, session = message.get("method"), message.get("params", {}), message.get("sessionId", "")
            if method == "Target.attachedToTarget":
                child = params["sessionId"]
                self.sessions[child] = params["targetInfo"]["type"]
                asyncio.ensure_future(self.enable(child))
            elif method == "Network.requestWillBeSent":
                self.last_network_event = time.monotonic()
                url = params["request"]["url"]
                key = (session, params["requestId"])
                if "redirectResponse" in params and key in self.requests:
                    redirect = params["redirectResponse"]
                    previous = self.requests[key]
                    previous.update(status=redirect.get("status"), from_cache=bool(redirect.get("fromDiskCache")))
                    self._finish(key, redirect.get("encodedDataLength", 0))
                if url.startswith(("data:", "blob:")):
                    continue
                self.requests[key] = {
                    "url": url, "host": urlparse(url).netloc, "context": self.sessions.get(session, "page"),
                    "status": None, "from_cache": False,
                }
            elif method == "Network.responseReceived":
                self.last_network_event = time.monotonic()
                key = (session, params["requestId"])
                if key in self.requests:
                    response = params["response"]
                    self.requests[key]["status"] = response.get("status")
                    self.requests[key]["from_cache"] = bool(
                        response.get("fromDiskCache") or response.get("fromServiceWorker") or response.get("fromPrefetchCache")
                    )
            elif method == "Network.requestServedFromCache":
                key = (session, params["requestId"])
                if key in self.requests:
                    self.requests[key]["from_cache"] = True
            elif method == "Network.loadingFinished":
                self.last_network_event = time.monotonic()
                self._finish((session, params["requestId"]), params.get("encodedDataLength", 0))
            elif method == "Network.loadingFailed":
                self.last_network_event = time.monotonic()
                self._finish((session, params["requestId"]), 0, failed=params.get("errorText", "failed"))
            elif method == "Runtime.exceptionThrown":
                self.errors.append(params.get("exceptionDetails", {}).get("text", "exception"))
            elif method == "Runtime.consoleAPICalled" and params.get("type") == "error":
                self.errors.append(" ".join(str(a.get("value", a.get("description", ""))) for a in params.get("args", [])))


async def wait_ready_and_idle(cdp: CDP, page: str, timeout: float = 300, idle: float = 8) -> float:
    start = time.monotonic()
    while time.monotonic() - start < timeout:
        try:
            result = await cdp.send(
                "Runtime.evaluate",
                {"expression": f"document.body ? document.body.innerText.includes({READY_MARKER!r}) : false", "returnByValue": True},
                page,
            )
            if result.get("result", {}).get("value"):
                break
        except Exception:
            pass
        await asyncio.sleep(1)
    else:
        raise TimeoutError("the page never reported the identity check")
    ready_after = time.monotonic() - start
    while time.monotonic() - cdp.last_network_event < idle:
        await asyncio.sleep(1)
    return ready_after


def summarise(entries: list[dict], names: dict[str, str]) -> dict:
    hosts: dict[str, dict] = defaultdict(lambda: {"requests": 0, "bytes": 0, "redirects": 0, "from_cache": 0, "not_modified": 0, "failed": 0})
    for entry in entries:
        host = names.get(entry["host"], entry["host"])
        bucket = hosts[host]
        bucket["requests"] += 1
        bucket["bytes"] += entry["bytes"]
        bucket["redirects"] += int(entry.get("status") in (301, 302, 303, 307, 308))
        bucket["from_cache"] += int(entry.get("from_cache"))
        bucket["not_modified"] += int(entry.get("status") == 304)
        bucket["failed"] += int(bool(entry.get("failed")))
    return {
        "hosts": dict(sorted(hosts.items(), key=lambda kv: -kv[1]["bytes"])),
        "requests": sum(h["requests"] for h in hosts.values()),
        "bytes": sum(h["bytes"] for h in hosts.values()),
        "contexts": dict(Counter(entry["context"] for entry in entries)),
    }


async def run(url: str, names: dict[str, str], debug_port: int) -> dict:
    version = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{debug_port}/json/version", timeout=10).read())
    async with websockets.connect(version["webSocketDebuggerUrl"], max_size=None) as ws:
        cdp = CDP(ws)
        reader = asyncio.ensure_future(cdp.reader())
        target = (await cdp.send("Target.createTarget", {"url": "about:blank"}))["targetId"]
        page = (await cdp.send("Target.attachToTarget", {"targetId": target, "flatten": True}))["sessionId"]
        cdp.sessions[page] = "page"
        await cdp.enable(page)
        await cdp.send("Page.enable", {}, page)

        visits = {}
        for visit in ("first", "repeat"):
            cdp.visit = visit
            before = len(cdp.completed)
            errors_before = len(cdp.errors)
            await cdp.send("Page.navigate", {"url": url}, page)
            ready = await wait_ready_and_idle(cdp, page)
            entries = [e for e in cdp.completed[before:] if e["visit"] == visit]
            visits[visit] = {
                **summarise(entries, names),
                "seconds_to_identity_check": round(ready, 1),
                "errors": cdp.errors[errors_before:],
                "requests_detail": [
                    {"host": names.get(e["host"], e["host"]), "path": urlparse(e["url"]).path, "status": e.get("status"),
                     "bytes": e["bytes"], "from_cache": e.get("from_cache"), "context": e["context"],
                     **({"failed": e["failed"]} if e.get("failed") else {})}
                    for e in entries
                ],
            }
        reader.cancel()
        return visits


def main() -> int:
    if not Path(CHROME).exists():
        raise SystemExit(f"Chrome not found at {CHROME}")
    if not (ROOT / "dist" / "space-wasm" / "index.html").exists():
        raise SystemExit("dist/space-wasm is absent; run `make wasm` first")

    app_port = free_port(pair=True)
    # The CDN stand-in binds app_port + 1 only once the server starts, so the OS
    # could hand that port to DevTools first; exclude it explicitly.
    debug_port = free_port()
    while debug_port in (app_port, app_port + 1):
        debug_port = free_port()
    wire = Path(tempfile.mkdtemp(prefix="cdp-wire-")) / "wire.jsonl"
    server = subprocess.Popen(
        [sys.executable, str(ROOT / "scripts" / "measure_wasm_load.py"), "--emulate-hf",
         "--port", str(app_port), "--log", str(wire)],
        cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    profile = tempfile.mkdtemp(prefix="cdp-profile-")
    chrome = subprocess.Popen(
        [CHROME, "--headless=new", f"--remote-debugging-port={debug_port}", f"--user-data-dir={profile}",
         "--no-first-run", "--no-default-browser-check", "--disable-extensions",
         "--disable-background-networking", "--disable-component-update", "--disable-sync",
         "--metrics-recording-only", "--no-pings", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        for _ in range(60):
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{debug_port}/json/version", timeout=2)
                urllib.request.urlopen(f"http://127.0.0.1:{app_port}/index.html", timeout=2)
                break
            except Exception:
                time.sleep(0.5)
        names = {
            f"127.0.0.1:{app_port}": "the Space's static host (emulated)",
            f"127.0.0.1:{app_port + 1}": "us.aws.cdn.hf.co (emulated)",
        }
        visits = asyncio.run(run(f"http://127.0.0.1:{app_port}/index.html", names, debug_port))
    finally:
        chrome.terminate()
        server.terminate()
        try:
            chrome.wait(10)
        except Exception:
            chrome.kill()
        shutil.rmtree(profile, ignore_errors=True)

    server_log = [json.loads(line) for line in wire.read_text().splitlines() if line.strip()]
    record = {
        "instrument": "headless Chrome over the DevTools protocol, brand-new profile, page and every worker attached",
        "chrome": subprocess.run([CHROME, "--version"], capture_output=True, text=True).stdout.strip(),
        "serving": "scripts/measure_wasm_load.py --emulate-hf (HTTP/1.1; text direct with ETag; binary files as a no-store 302 to a CDN stand-in)",
        "byte_definition": "Network.loadingFinished / redirectResponse encodedDataLength: bytes Chrome received for each request, headers and body, as encoded on the wire",
        "visits": visits,
        "server_status_counts": dict(Counter(f"{e['origin']} {e['status']}" for e in server_log)),
    }
    RECORD.parent.mkdir(parents=True, exist_ok=True)
    RECORD.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    for visit, data in visits.items():
        print(f"{visit}: {data['requests']} requests, {data['bytes']:,} B, identity check after {data['seconds_to_identity_check']} s, errors {len(data['errors'])}")
        for host, info in data["hosts"].items():
            print(f"   {host:42s} {info['requests']:4d} req {info['bytes']:>12,} B  redirects {info['redirects']:2d}  cache {info['from_cache']:3d}  304 {info['not_modified']:3d}  failed {info['failed']}")
    print(f"wrote {RECORD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
