"""CP-3 item 3: the static Pages export performs zero runtime calls.

The check reads the built document and enumerates every position that would make
a browser fetch something without a user action. Hyperlinks are exempt by design
-- §9.2 requires the page to link the Space and the public MLflow UI -- and an
`<a href>` is followed only on a click.

The positive controls are the point. One is synthetic: each forbidden
construction is reintroduced and must be caught. One is real: `marimo export
html`, the build path §9.2 names first, emits 181 CDN references, and the same
scanner run against a fresh export must report them. That is what justified
taking the plan's purpose-built fallback instead.
"""

from __future__ import annotations

import json
import re

import pytest

from delu_forecast.claims import REPO_ROOT, build_claims
from delu_forecast.static_audit import audit_html

PAGE = REPO_ROOT / "docs" / "index.html"
BUILD_RECORD = REPO_ROOT / "reports" / "cp3" / "pages_build.json"


@pytest.fixture(scope="module")
def document() -> str:
    return PAGE.read_text()


def test_the_page_is_built(document):
    assert PAGE.exists()
    assert (PAGE.parent / ".nojekyll").exists(), "GitHub Pages would otherwise run Jekyll"
    assert document.lstrip().startswith("<!DOCTYPE html>")
    assert len(document) > 200_000, "a page with no embedded figures is not the §10 reading order"


def test_zero_runtime_calls(document):
    findings = audit_html(document)
    assert not findings, "the static page would fetch at runtime:\n  " + "\n  ".join(
        str(finding) for finding in findings
    )


def test_every_image_is_embedded(document):
    sources = re.findall(r"<img[^>]*\bsrc\s*=\s*[\"']([^\"']+)", document)
    assert len(sources) >= 7, f"expected the §10 figures, found {len(sources)}"
    assert all(source.startswith("data:image/") for source in sources), sources


def test_no_external_stylesheet_or_font(document):
    assert "<link" not in document.lower() or not re.search(
        r"<link[^>]+href\s*=\s*[\"']https?://", document, re.IGNORECASE
    )
    assert "@font-face" not in document, "a web font is a runtime call"
    assert "fonts.googleapis" not in document and "fonts.gstatic" not in document


def test_the_only_scripts_are_inline(document):
    for tag in re.findall(r"<script[^>]*>", document, re.IGNORECASE):
        assert "src=" not in tag.lower(), tag


def test_links_that_do_exist_point_where_the_plan_says(document):
    claims = build_claims()
    assert claims["space_url"] in document, "§9.2 requires the Space to be linked beneath the report"
    assert claims["mlflow_url"] in document, "§9.2 requires the public MLflow UI to be linked"
    assert claims["space_link_label"] in document, "free-tier sleep must be disclosed on the link"


# -- positive controls -------------------------------------------------------


@pytest.mark.parametrize(
    "injection",
    [
        '<script src="https://cdn.jsdelivr.net/npm/thing.js"></script>',
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Lora">',
        '<img src="https://huggingface.co/spaces/hrsi56/delu/preview.png">',
        '<iframe src="https://huggingface.co/spaces/hrsi56/delu"></iframe>',
        '<link rel="preconnect" href="https://cdn.jsdelivr.net">',
        '<style>@import url("https://example.com/a.css");</style>',
        '<style>body{background:url(https://example.com/b.png)}</style>',
        '<script>fetch("https://example.com/beacon")</script>',
        '<script>navigator.sendBeacon("/x")</script>',
        '<a href="/x" ping="https://example.com/track">x</a>',
        '<meta http-equiv="refresh" content="0;url=https://example.com">',
    ],
)
def test_positive_control_each_forbidden_construction_is_caught(document, injection):
    corrupted = document.replace("</body>", injection + "</body>")
    assert corrupted != document
    assert audit_html(corrupted), f"scanner missed: {injection}"


def test_positive_control_a_plain_hyperlink_is_not_a_finding(document):
    corrupted = document.replace("</body>", '<a href="https://example.com">x</a></body>')
    assert not audit_html(corrupted), "an ordinary link is not a runtime call"


def test_the_build_record_states_why_marimo_export_was_rejected():
    """§9.2 names `marimo export html` first and allows a fallback. The reason
    this build took the fallback is recorded as a measurement, not an opinion."""
    record = json.loads(BUILD_RECORD.read_text())
    assert record["marimo_export_external_reference_count"] > 0
    assert "cdn.jsdelivr.net" in record["marimo_export_external_hosts"]
    assert "zero runtime calls" in record["marimo_export_html_rejected_because"]
    assert record["build_path"].startswith("purpose-built static assembly")


def test_positive_control_the_scanner_catches_a_real_marimo_export(tmp_path):
    """Not a synthetic injection: build the export §9.2 names and scan it."""
    import shutil
    import subprocess

    if shutil.which("marimo") is None and not (REPO_ROOT / ".venv" / "bin" / "marimo").exists():
        pytest.skip("marimo is not installed in this environment")
    target = tmp_path / "export.html"
    result = subprocess.run(
        ["marimo", "export", "html", "app/showcase.py", "-o", str(target)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=900,
        env={**__import__("os").environ, "MLFLOW_DISABLE_AGENT_HINT": "1"},
    )
    if result.returncode != 0 or not target.exists():
        pytest.skip(f"marimo export unavailable here: {result.stderr[-200:]}")
    findings = audit_html(target.read_text())
    hosts = {finding.detail.split("/")[2] for finding in findings if "//" in finding.detail}
    assert findings, "marimo's HTML export was expected to reference external assets"
    assert "cdn.jsdelivr.net" in hosts, hosts
