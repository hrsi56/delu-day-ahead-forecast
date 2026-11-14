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


# --- PRES-6 outcome 5: a redirect that ends on another host fails, and the chain is recorded ----------------------

import json  # noqa: E402

FIXTURE = REPO_ROOT / "tests" / "fixtures" / "pres6" / "recorded.json"


def _replay(hops):
    """A `fetch_once` that answers each URL as the recorded hops did, and fails on any URL it was not given."""
    answers = {hop["url"]: {"status": hop["status"], "location": hop["location"]} for hop in hops}

    def fetch(url):
        assert url in answers, f"not recorded: {url}"
        return dict(answers[url])
    return fetch


def test_the_recorded_bare_history_route_fails_as_a_cross_host_redirect(tmp_path):
    recorded = json.loads(FIXTURE.read_text())["space_history_redirect"]
    url, hops = recorded["linked_url"], recorded["hops"]
    assert [hop["status"] for hop in hops] == [302, 307, 200]
    result = check_links.probe(url, fetch=_replay(hops))
    assert result["status"] == 200 and result["final_url"] == "https://huggingface.co/History"
    assert result["cross_host_redirect"] and result["final_host"] == "huggingface.co"
    assert [(h["status"], h["from"], h["to"]) for h in result["redirects"]] == [
        (302, url, "https://huggingface.co/history"),
        (307, "https://huggingface.co/history", "https://huggingface.co/History")]
    # through the gate, as the receipt's link row runs it: a 200 at the end is not a pass
    page = tmp_path / "page.html"
    page.write_text(f'<a href="{url}">history</a>\n')
    record = tmp_path / "record.json"
    probe = lambda u: check_links.probe(u, fetch=_replay(hops))  # noqa: E731
    assert check_links.main(surfaces={"Page": page}, probe=probe, record=record, gated=False) == 1
    body = json.loads(record.read_text())
    assert body["cross_host_redirects"] == [url] and list(body["failed_destinations"]) == [url]
    assert body["links"][url]["redirects"][0]["location"] == "https://huggingface.co/history"
    assert "another host" in body["failed_destinations"][url]


def test_positive_control_a_redirect_within_the_named_host_passes_and_is_recorded(tmp_path):
    # the A12 review's same-origin case: `…static.hf.space/` answers 302 to `/index.html` (finding 3)
    root = "https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/"
    hops = [{"url": root, "status": 302, "location": "/index.html"},
            {"url": root + "index.html", "status": 200, "location": None}]
    result = check_links.probe(root, fetch=_replay(hops))
    assert result["status"] == 200 and not result["cross_host_redirect"]
    assert result["redirects"] == [{"status": 302, "from": root, "location": "/index.html", "to": root + "index.html"}]
    page = tmp_path / "page.html"
    page.write_text(f'<a href="{root}">Space</a>\n')
    probe = lambda u: check_links.probe(u, fetch=_replay(hops))  # noqa: E731
    assert check_links.main(surfaces={"Page": page}, probe=probe, record=None, gated=False) == 0


def test_a_loop_and_a_location_less_redirect_fail():
    loop = check_links.probe("https://a.test/x", fetch=lambda u: {"status": 302, "location": u}, max_hops=3)
    assert loop["status"] is None and "more than 3 redirects" in loop["error"] and len(loop["redirects"]) == 4
    bare = check_links.probe("https://a.test/x", fetch=lambda u: {"status": 301, "location": None})
    assert bare["status"] == 301 and "without a Location" in bare["error"] and bare["redirects"] == []
