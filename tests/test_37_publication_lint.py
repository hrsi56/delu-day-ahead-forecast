"""Publication Standard v1 §4 and §5 (brief W6, W7): the publication lint, and its negative controls.

The lint passes on the built page, the README's generated top block and the template sources.
Each rule family -- codes, precision, percentages, status words -- is shown to fail on a
deliberately broken input, and the reading path is shown to be the one the standard defines.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from delu_forecast import publication_lint as L
from delu_forecast import registry as G
from delu_forecast.claims import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT / "scripts"))

import readme_research  # noqa: E402

PAGE = REPO_ROOT / "docs" / "index.html"


@pytest.fixture(scope="module")
def page() -> str:
    return PAGE.read_text()


@pytest.fixture(scope="module")
def glance() -> str:
    return readme_research.build_glance("html")


def test_the_lint_passes_on_the_page_the_readme_and_the_templates(page, glance):
    results = L.lint(REPO_ROOT, page, glance)
    assert results == {"page": [], "readme": [], "templates": []}, results


def test_the_readme_glance_reads_the_same_in_markdown_and_in_html(glance):
    """The lint reads the HTML rendering of the README's top block; it must say what the Markdown says."""
    import re

    markdown = readme_research.build_glance("md")
    plain_md = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", markdown)
    plain_md = re.sub(r"<!--.*?-->|[*`#]|^- ", "", plain_md, flags=re.MULTILINE)
    assert re.sub(r"\s+", "", plain_md) == re.sub(r"\s+", "", L.reading_text("<div>" + glance + "</div>"))


# --------------------------------------------------------------------------- the reading path


def test_the_reading_path_skips_closed_disclosures_value_tables_and_phone_charts():
    document = (
        '<p>shown</p><details><summary>Title</summary><p>hidden body</p></details>'
        '<details open><summary>Open</summary><p>open body</p></details>'
        '<table class="data"><tr><td>table cell</td></tr></table>'
        '<svg class="d" data-chart="c"><title>t</title><text>desktop</text></svg>'
        '<svg class="m" data-chart="c"><text>phone</text></svg><script>var x = 1;</script>'
    )
    text = L.reading_text(document)
    assert text == "shown Title Open open body desktop"


# --------------------------------------------------------------------------- negative controls, one per family


def test_negative_control_codes(page):
    for injected in ("CP-20", "C69", "§4", "S_MAE", "NOT_DEMONSTRATED", "HG", "V2-P", "B2"):
        broken = page.replace('<h2 id="results-h">How the models compare', f'<h2 id="results-h">How the models compare {injected}', 1)
        assert any(finding.startswith("codes:") for finding in L.lint_document(broken)), injected


def test_negative_control_codes_denylist_is_generated_from_the_registry():
    assert set(L.code_denylist()) >= {"A1", "B0", "HG", "H0", "V2-H", "V2-P", "v1_reference"}
    assert all(code in G.codes() for code in L.code_denylist())


def test_negative_control_precision_unbound_numeral(page):
    broken = page.replace('<h2 id="results-h">How the models compare', '<h2 id="results-h">How the 7 models compare', 1)
    assert any("unbound numeral" in finding for finding in L.lint_document(broken))


def test_negative_control_precision_too_many_significant_figures(page):
    shown = '>0.566</text>'
    assert shown in page
    broken = page.replace(shown, '>0.56576</text>', 1)
    assert any("more than four significant figures" in finding for finding in L.lint_document(broken))


def test_negative_control_precision_eur_decimals(page):
    marker = 'data-record="derived.periods.v3.stress" data-derived="period_stress">48.0<'
    assert marker in page
    broken = page.replace(marker, marker.replace(">48.0<", ">48.04<"), 1)
    assert any("not shown to one decimal" in finding for finding in L.lint_document(broken))


def test_negative_control_precision_a_near_zero_value_rounded_across_its_sign():
    document = ('<p><data value="3.857628092332211e-06" data-claim="C34" '
                'data-record="cp16.uncertainty.V2-H-V2-P.equal_fold.MAE" data-field="ci_high">0.0000</data></p>')
    assert L.lint_document(document)
    fine = document.replace(">0.0000<", ">+0.0000039<")
    assert not L.lint_document(fine)


def test_negative_control_precision_two_precisions_in_one_chart(page):
    shown = '>0.644</text>'
    assert shown in page
    broken = page.replace(shown, '>0.6441</text>', 1)
    assert any("precisions" in finding for finding in L.lint_document(broken))


def test_negative_control_percentages(page):
    broken = page.replace('<h2 id="results-h">How the models compare', '<h2 id="results-h">How the models compare <span data-structural="label">12%</span>', 1)
    assert any(finding.startswith("percentages:") for finding in L.lint_document(broken))


def test_negative_control_status_words():
    strings = [("scripts/build_pages.py", 1, "We retained v3 as the current research model."),
               ("scripts/build_pages.py", 2, "The demo runs v1."),
               ("scripts/readme_research.py", 3, "v3 is still the latest.")]
    findings = L.status_findings(strings)
    assert len(findings) >= 4
    assert not L.status_findings([("x", 1, "chapters, newest first; in September 2026, v3 was adopted")])


def test_negative_control_status_words_in_a_real_template(monkeypatch, tmp_path):
    source = (REPO_ROOT / "scripts" / "readme_research.py").read_text()
    doctored = source.replace('"## Generations, newest first",', '"## Generations, newest first; v3 is the current model",', 1)
    assert doctored != source
    (tmp_path / "scripts").mkdir()
    (tmp_path / "src" / "delu_forecast").mkdir(parents=True)
    for relative in L.TEMPLATE_SOURCES:
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(doctored if relative == "scripts/readme_research.py" else (REPO_ROOT / relative).read_text())
    assert any("'current'" in finding for finding in L.status_findings(L.template_strings(tmp_path)))


def test_the_lint_script_exits_nonzero_on_a_finding(monkeypatch, capsys):
    import lint_publication

    monkeypatch.setattr(lint_publication, "run", lambda: {"page": ["codes: x"], "readme": [], "templates": []})
    assert lint_publication.main() == 1
    monkeypatch.setattr(lint_publication, "run", lambda: {"page": [], "readme": [], "templates": []})
    assert lint_publication.main() == 0
