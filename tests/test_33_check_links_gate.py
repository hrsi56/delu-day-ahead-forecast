"""Presentation plan §11.2 and §9.5 (F05): the link checker is a gate.

A required destination that fails makes it exit nonzero; local development servers and command
examples are classified as non-destinations and never fetched. Offline: the probe is mocked.
"""

from __future__ import annotations

import sys

from delu_forecast.claims import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT / "scripts"))

import check_links  # noqa: E402

SURFACE = (
    "Try https://hrsi56.github.io/delu-day-ahead-forecast/ or the tracking at "
    "https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow.\n"
    "make wasm-serve   # the Static Space, at http://127.0.0.1:8820\n"
    "open http://localhost:8000/docs/index.html and see https://<user>.github.io/<repo>/\n"
    'createElementNS("http://www.w3.org/2000/svg", "svg")\n'
)


def _surfaces(tmp_path):
    page = tmp_path / "page.html"
    page.write_text(SURFACE)
    return {"Page": page}


def _probe_all_ok(calls):
    def probe(url):
        calls.append(url)
        return {"status": 200, "final_url": url}
    return probe


def test_every_destination_resolving_passes_and_non_destinations_are_not_fetched(tmp_path):
    calls: list[str] = []
    code = check_links.main(surfaces=_surfaces(tmp_path), probe=_probe_all_ok(calls), record=None, gated=False)
    assert code == 0
    assert sorted(calls) == ["https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow",
                             "https://hrsi56.github.io/delu-day-ahead-forecast/"]


def test_local_servers_and_command_examples_are_classified():
    assert check_links.classify("http://127.0.0.1:8820") == "local"
    assert check_links.classify("http://localhost:8000/docs/index.html") == "local"
    assert check_links.classify("https://<user>.github.io/<repo>/") == "example"
    assert check_links.classify("http://www.w3.org/2000/svg") == "namespace"
    assert check_links.classify("https://hrsi56.github.io/delu-day-ahead-forecast/") == "destination"


def test_negative_control_a_mocked_404_fails_the_gate(tmp_path):
    def probe(url):
        if "github.io" in url:
            return {"status": 404, "final_url": url, "error": "HTTPError 404: Not Found"}
        return {"status": 200, "final_url": url}

    record = tmp_path / "record.json"
    code = check_links.main(surfaces=_surfaces(tmp_path), probe=probe, record=record, gated=False)
    assert code == 1
    import json

    body = json.loads(record.read_text())
    assert body["exit"] == 1
    assert body["failed_destinations"] == {"https://hrsi56.github.io/delu-day-ahead-forecast/": "HTTPError 404: Not Found"}
    assert body["not_destinations"]["http://127.0.0.1:8820"] == "local"


def test_negative_control_an_unreachable_destination_fails_the_gate(tmp_path):
    def probe(url):
        return {"status": None, "error": "URLError: timed out"}

    assert check_links.main(surfaces=_surfaces(tmp_path), probe=probe, record=None, gated=False) == 1
