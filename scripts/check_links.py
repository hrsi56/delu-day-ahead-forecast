#!/usr/bin/env python3
"""Resolve every external link on every public surface, from an anonymous client.

CP-3 item 3 asks that the static page render "every asset and link", and the
plan's link discipline (§9.1/§9.2) is only meaningful if it is checked the way a
stranger sees it. So this runs **unauthenticated** -- no cookies, no token, no
logged-in browser -- and records the status every URL returned.

Deliberately not a pytest: it needs the network, and the committed test suite and
CI must stay runnable offline without a credential. `tests/test_33_check_links_gate.py`
drives it with a mocked probe.

It exits 1 when any destination does not answer 200 (plan §11.2, F05). A documented local
server (`http://127.0.0.1:...`) or a command-example placeholder is classified, recorded and not
fetched: it is not a place a reader can go.

**Redirects are followed one hop at a time, never by the client** (PRES-6, outcome 5). Every hop's status and
`Location` is recorded as the link's redirect chain. A link whose chain ends on a host other than the one the link
names fails, even when that host answers 200: the reader was sent somewhere the surface never named. The Space's
retired bare `/history/` route, which answered 302 to `https://huggingface.co/history`, is that case.

    uv run python scripts/check_links.py
"""

from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from delu_forecast.claims import FORBIDDEN_DAGSHUB_PATHS, build_claims  # noqa: E402

RECORD = ROOT / "reports" / "cp3" / "link_check.json"
SURFACES = {
    "Pages export": ROOT / "docs" / "index.html",
    "Space card": ROOT / "space" / "README.md",
    "Static Space card": ROOT / "space-wasm" / "README.md",
    "README": ROOT / "README.md",
}
#: The SVG namespace is an XML identifier passed to `createElementNS`, not a URL
#: the browser ever fetches.
NOT_A_LINK = {"http://www.w3.org/2000/svg"}

_URL = re.compile(r'https?://[^\s"\'<>)\]]+')

#: Hosts that are this machine: documentation examples of a local server, never a destination.
LOCAL_HOSTS = ("127.0.0.1", "localhost", "0.0.0.0")


def classify(url: str) -> str:
    """What a URL on a public surface is (plan §11.2, F05).

    `namespace` is an XML identifier, `local` a documented local development server,
    `example` a placeholder in a command example; only a `destination` is a place a reader can go,
    and every destination is required to resolve."""
    if url in NOT_A_LINK:
        return "namespace"
    host = urllib.parse.urlsplit(url).hostname or ""
    if host in LOCAL_HOSTS:
        return "local"
    if "<" in url or "{" in url or host.endswith(("example.com", "example.org")):
        return "example"
    return "destination"


#: The statuses that carry a `Location` to follow.
REDIRECTS = (301, 302, 303, 307, 308)
#: More hops than this is a loop or a chain no reader should be sent down; the link fails.
MAX_HOPS = 10


def host(url: str) -> str:
    """The host a URL names, lower-cased and without a port; an empty string when it names none."""
    return (urllib.parse.urlsplit(url).hostname or "").lower()


def fetch_once(url: str) -> dict[str, object]:
    """One anonymous GET that does not follow a redirect: the status and, for a redirect, its `Location`."""
    request = urllib.request.Request(url, method="GET", headers={"User-Agent": "delu-link-check/1.0"})
    opener = urllib.request.build_opener(_NoRedirect)
    try:
        with opener.open(request, timeout=25) as response:
            return {"status": response.status, "location": response.headers.get("Location")}
    except urllib.error.HTTPError as exc:
        out: dict[str, object] = {"status": exc.code, "location": exc.headers.get("Location") if exc.headers else None}
        if exc.code not in REDIRECTS:
            out["error"] = f"HTTPError {exc.code}: {exc.reason}"
        return out
    except Exception as exc:
        return {"status": None, "error": f"{type(exc).__name__}: {exc}"[:200]}


def probe(url: str, *, fetch=fetch_once, max_hops: int = MAX_HOPS) -> dict[str, object]:
    """Follow `url`'s redirects hop by hop, recording each, and say where the chain ends.

    The result's `status` and `final_url` are the last hop's. `redirects` is the chain, one
    `{"status", "from", "location", "to"}` per hop (`to` is `location` resolved against `from`).
    `cross_host_redirect` is true when the chain ends on a host other than the linked URL's."""
    chain: list[dict[str, object]] = []
    current = url
    out: dict[str, object] = {}
    for _ in range(max_hops + 1):
        hop = fetch(current)
        status, location = hop.get("status"), hop.get("location")
        if status in REDIRECTS and location:
            target = urllib.parse.urljoin(current, str(location))
            chain.append({"status": status, "from": current, "location": location, "to": target})
            current = target
            continue
        out = {"status": status, "final_url": current}
        if status in REDIRECTS:
            out["error"] = f"redirect {status} without a Location"
        elif hop.get("error"):
            out["error"] = hop["error"]
        break
    else:
        out = {"status": None, "final_url": current, "error": f"more than {max_hops} redirects"}
    out["redirects"] = chain
    out["final_host"] = host(current)
    out["cross_host_redirect"] = bool(chain) and host(current) != host(url)
    if out["cross_host_redirect"]:
        out["error"] = f"redirect ends on another host: {host(url)} -> {host(current)}"
    return out


def probe_gated() -> dict[str, dict]:
    """The gated DagsHub paths, checked rather than asserted: the link-discipline rule rests on it."""
    gated = {}
    for suffix in ("", "/experiments", "/models", "/src/main"):
        url = f"https://dagshub.com/hrsi56/delu-day-ahead-forecast{suffix}"
        request = urllib.request.Request(url, headers={"User-Agent": "delu-link-check/1.0"})
        opener = urllib.request.build_opener(_NoRedirect)
        try:
            with opener.open(request, timeout=25) as response:
                gated[url] = {"status": response.status, "location": response.headers.get("Location")}
        except urllib.error.HTTPError as exc:
            gated[url] = {"status": exc.code, "location": exc.headers.get("Location")}
        except Exception as exc:
            gated[url] = {"status": None, "error": f"{type(exc).__name__}: {exc}"[:200]}
        print(f"{str(gated[url].get('status')):>5}  {url} -> {gated[url].get('location')}")
    return gated


def check(surfaces: dict[str, Path], probe=probe) -> dict[str, dict]:
    """Every URL on every surface, classified; only destinations are fetched."""
    found: dict[str, set[str]] = {}
    for name, path in surfaces.items():
        found[name] = {url.rstrip(".,;>") for url in _URL.findall(path.read_text())}
    results = {}
    for url in sorted({url for urls in found.values() for url in urls}):
        kind = classify(url)
        result: dict[str, object] = {"kind": kind}
        if kind == "destination":
            result.update(probe(url))
            result["resolves"] = result.get("status") == 200 and not result.get("cross_host_redirect")
            hops = "".join(f" -> {hop['status']} {hop['to']}" for hop in result.get("redirects") or [])
            print(f"{str(result.get('status')):>5}  {url}{hops}")
        result["on_surfaces"] = sorted(name for name, urls in found.items() if url in urls)
        results[url] = result
    return results


def main(argv: list[str] | None = None, *, surfaces: dict[str, Path] | None = None, probe=probe,
         record: Path | None = RECORD, gated: bool = True) -> int:
    """Exit 1 when any required destination does not resolve (F05); the record says which and why."""
    claims = build_claims()
    results = check(surfaces or SURFACES, probe)
    failed = sorted(url for url, result in results.items() if result["kind"] == "destination" and not result["resolves"])
    body = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "client": "unauthenticated urllib -- no cookies, no token, no logged-in browser",
        "rule": "every destination on a public surface must answer 200 on the host it names: redirects are "
                "followed one hop at a time and recorded, and a chain that ends on another host fails; local "
                "servers, command examples and XML namespaces are classified and not fetched",
        "cross_host_redirects": sorted(url for url, result in results.items() if result.get("cross_host_redirect")),
        "links": results,
        "not_destinations": {url: result["kind"] for url, result in results.items() if result["kind"] != "destination"},
        "gated_dagshub_paths_probed_without_following_redirects": probe_gated() if gated else None,
        "forbidden_paths": list(FORBIDDEN_DAGSHUB_PATHS),
        "tracking_uri": claims["mlflow_url"],
        "failed_destinations": {url: results[url].get("error") or results[url].get("status") for url in failed},
        "exit": 1 if failed else 0,
    }
    if record is not None:
        record.parent.mkdir(parents=True, exist_ok=True)
        record.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n")
        print(f"\nwrote {record}")
    print(f"failed destinations: {failed or 'none'}")
    return 1 if failed else 0


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):  # noqa: ARG002
        return None


if __name__ == "__main__":
    raise SystemExit(main())
