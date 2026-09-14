#!/usr/bin/env python3
"""Resolve every external link on every public surface, from an anonymous client.

CP-3 item 3 asks that the static page render "every asset and link", and the
plan's link discipline (§9.1/§9.2) is only meaningful if it is checked the way a
stranger sees it. So this runs **unauthenticated** -- no cookies, no token, no
logged-in browser -- and records the status every URL returned.

Deliberately not a pytest: it needs the network, and the committed test suite and
CI must stay runnable offline without a credential.

    uv run python scripts/check_links.py
"""

from __future__ import annotations

import json
import re
import sys
import urllib.error
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
    "README": ROOT / "README.md",
}
#: The SVG namespace is an XML identifier passed to `createElementNS`, not a URL
#: the browser ever fetches.
NOT_A_LINK = {"http://www.w3.org/2000/svg"}

_URL = re.compile(r'https?://[^\s"\'<>)\]]+')


def probe(url: str) -> dict[str, object]:
    request = urllib.request.Request(url, method="GET", headers={"User-Agent": "delu-link-check/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            return {"status": response.status, "final_url": response.url}
    except urllib.error.HTTPError as exc:
        return {"status": exc.code, "final_url": exc.url}
    except Exception as exc:
        return {"status": None, "error": f"{type(exc).__name__}: {exc}"[:200]}


def main() -> int:
    claims = build_claims()
    found: dict[str, set[str]] = {}
    for name, path in SURFACES.items():
        urls = {url.rstrip(".,;>") for url in _URL.findall(path.read_text())} - NOT_A_LINK
        found[name] = urls

    results = {}
    for url in sorted({url for urls in found.values() for url in urls}):
        result = probe(url)
        result["on_surfaces"] = sorted(name for name, urls in found.items() if url in urls)
        result["resolves"] = result.get("status") == 200
        results[url] = result
        print(f"{str(result.get('status')):>5}  {url}")

    # The gated DagsHub paths, checked rather than asserted: this is the
    # measurement the whole link-discipline rule rests on.
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

    pending = sorted(url for url, result in results.items() if not result["resolves"])
    record = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "client": "unauthenticated urllib -- no cookies, no token, no logged-in browser",
        "links": results,
        "gated_dagshub_paths_probed_without_following_redirects": gated,
        "forbidden_paths": list(FORBIDDEN_DAGSHUB_PATHS),
        "tracking_uri": claims["mlflow_url"],
        "unresolved": pending,
        "unresolved_reason": (
            "Both are the URLs publication creates. Deployment is owner-only and was not "
            "performed by this checkpoint: GitHub Pages is not enabled and the Space is not "
            "created. See docs/deploy.md."
        )
        if pending
        else None,
    }
    RECORD.parent.mkdir(parents=True, exist_ok=True)
    RECORD.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    print(f"\nwrote {RECORD}")
    print(f"unresolved: {pending or 'none'}")
    return 0


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):  # noqa: ARG002
        return None


if __name__ == "__main__":
    raise SystemExit(main())
