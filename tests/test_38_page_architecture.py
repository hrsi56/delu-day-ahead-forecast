"""Publication Standard v1 §1, §3.4, §6 and §7 (brief W4, W5, W8, W13), as amended by PUBLISH_RULES 1.0 (A1,
A3, A4): the page's architecture.

* The section order of PUBLISH_RULES 1.0 §5 (A4): the opening, the released product's documentation, the
  comparison, then the lineage and the chapters, with planned work after them.
* The headline block in the research status card, identical to the README's, with the terms it
  introduces directly below it; the release rule beside the demo action, outside any disclosure;
  the byline link; the comparison's finding and caveat above its chart. (The §1 pixel placements
  are measured in real browsers by `scripts/check_reader_paths.py placements` and recorded.)
* One generic renderer fills the chapter grammar's fixed slots; a chapter missing a slot fails.
* The branch cards attach to the lineage. v1's archive is byte-identical to `af0abb0`'s.
* Evidence tiers: every audit-grade link sits in an evidence row, labelled "<type>, frozen <date>"
  with its evidence tag's date. The stack line is rendered from the system view's data.
"""

from __future__ import annotations

import dataclasses
import hashlib
import re
import subprocess
import sys
from html.parser import HTMLParser

import pytest

from delu_forecast import registry as G
from delu_forecast import research_claims as RC
from delu_forecast.claims import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT / "scripts"))

import build_pages as B  # noqa: E402
import readme_research  # noqa: E402

PAGE = REPO_ROOT / "docs" / "index.html"
README = REPO_ROOT / "README.md"

#: v1's archive -- the whole `<details id="v1-archive">` element -- as published at af0abb0.
AF0ABB0_ARCHIVE_SHA256 = "d4d19223559b89747d981bfea86f1bc64661149e842dfee96898ba2b60196021"
AF0ABB0_ARCHIVE_CHARS = 961360


@pytest.fixture(scope="module")
def page() -> str:
    return PAGE.read_text()


def archive_element(document: str) -> str:
    start = document.index('<details class="disclosure archive" id="v1-archive">')
    depth = 0
    for match in re.finditer(r"<details\b|</details>", document[start:]):
        depth += 1 if match.group(0).startswith("<details") else -1
        if depth == 0:
            return document[start:start + match.end()]
    raise AssertionError("the archive element is not closed")


# --------------------------------------------------------------------------- §6 order


SECTION_ORDER = ('class="opening"', 'id="product"', 'id="research-results"', 'id="journey"', 'id="chapters"',
                 'id="planned"', 'id="system"', 'id="reproduce"', 'id="contribution"', 'id="attribution"')


def section_order_problems(document: str) -> list[str]:
    positions = [document.find(marker) for marker in SECTION_ORDER]
    if -1 in positions:
        return [f"missing section {SECTION_ORDER[positions.index(-1)]}"]
    return [] if positions == sorted(positions) else [f"sections out of the §6 order: {positions}"]


def test_the_sections_follow_the_standard_s_order(page):
    assert section_order_problems(page) == []


def _section_html(document: str, opening: str) -> str:
    start = document.index(opening)
    depth = 0
    for match in re.finditer(r"<section\b|</section>", document[start:]):
        depth += 1 if match.group(0).startswith("<section") else -1
        if depth == 0:
            return document[start:start + match.end()]
    raise AssertionError(f"{opening} is not closed")


def test_negative_control_planned_work_before_the_chapters_is_caught(page):
    planned = page[page.index('<section class="section planned"'):]
    planned = planned[:planned.index("</section>") + len("</section>")]
    moved = page.replace(planned, "").replace('<section class="section chapters"', planned + '<section class="section chapters"', 1)
    assert section_order_problems(moved)


def test_negative_control_the_product_documentation_after_the_comparison_is_caught(page):
    """A4: the released product's documentation sits directly after the opening, before the comparison."""
    product = _section_html(page, '<section class="section product"')
    moved = page.replace(product, "").replace('<section class="section" id="journey"', product + '<section class="section" id="journey"', 1)
    assert section_order_problems(moved)


def test_negative_control_the_comparison_after_the_lineage_is_caught(page):
    """A4: the overview comparison comes before the lineage and the chapters."""
    results = _section_html(page, '<section class="section" id="research-results"')
    moved = page.replace(results, "").replace('<section class="section chapters"', results + '<section class="section chapters"', 1)
    assert section_order_problems(moved)


def test_the_product_documentation_opens_directly_after_the_opening(page):
    opening_end = page.index("</section>", page.index('class="opening"')) + len("</section>")
    assert page[opening_end:page.index('<section class="section product"')].strip() == ""


# --------------------------------------------------------------------------- the opening (§1, §3.4)


def test_the_headline_block_is_in_the_research_status_card_and_matches_the_readme(page):
    card = page[page.index('<div class="status status-research">'):]
    card = card[:card.index("</div>")]
    assert f'<dd class="headline" id="headline" data-block="headline">{RC.headline()}</dd>' in card
    readme = README.read_text()
    assert RC.headline("md") in readme[:readme.index(readme_research.GLANCE_END)]
    text = re.sub(r"<[^>]+>", "", RC.headline())
    assert text == re.sub(r"`", "", RC.headline("md"))
    # PUBLISH_RULES 1.0 A1: each headline value names its metric beside it. v4 leads with its own rule (§3.3 a).
    assert text.startswith("Met the adoption rule set before the experiment, which required both error scores to "
                           "improve on v3's and no test period to be decisively worse (v4 − v3: −0.0301 "
                           "[−0.0368, −0.0228] on the point-error score and −0.0266 [−0.0327, −0.0204] on the interval "
                           "score; 1 policy tested against the rule).")
    # The v3-era form, from the same generator, is unchanged for a generation led by the accuracy targets.
    claim, v3_form = RC.headline_template(G.get("v3"))
    assert re.sub(r"<[^>]+>", "", RC.render_template(claim, v3_form)).startswith(
        "Met both accuracy targets set before the experiments: error scores at least 10% below the strongest "
        "benchmark, daily LEAR (v3: 14% below on the point-error score and 17% below on the interval score; the "
        "first of 8 policies tested to meet them).")


def test_the_terms_are_defined_directly_below_the_headline(page):
    headline_end = page.index('<dd class="headline" id="headline"')
    terms = page.index('<dd class="headline-terms">')
    between = page[page.index("</dd>", headline_end) + len("</dd>"):terms]
    assert between.strip() == ""
    for key in B.HEADLINE_TERMS:
        assert f'data-block="{key}"' in page[terms:terms + 4000]


def test_the_release_rule_is_beside_the_demo_action_and_outside_any_disclosure(page):
    action = page.index('class="btn-primary external"')
    rule = page.index('data-block="release-rule"')
    assert 0 < rule - action < 700, "the release rule follows the demo action directly"
    opened = page.rfind("<details", 0, rule)
    assert opened == -1 or page.rfind("</details>", 0, rule) > opened
    assert "The demo runs the released model, " in page[rule:rule + 400]


def test_the_byline_links_to_the_contribution(page):
    assert f'<p class="byline">Led by {RC.OWNER_PUBLIC_NAME} · <a href="#contribution">Contribution</a></p>' in page


def test_the_latest_research_summary_is_gone(page):
    assert "Latest research" not in page and "opening-summary" not in page
    assert "We retained" not in page and "current research model" not in page


def test_the_comparison_finding_and_caveat_sit_above_its_chart(page):
    section = page[page.index('id="research-results"'):]
    finding = section.index('id="comparison-finding"')
    caveat = section.index('data-block="comparison.caveat"')
    chart = section.index('data-chart-id="overview"')
    assert finding < caveat < chart
    assert "a development diagnostic, not a product qualification" in section[caveat:chart]


# --------------------------------------------------------------------------- the chapter grammar (§6)


def test_every_research_chapter_fills_the_grammar():
    for slots in (B.v4_slots(), B.v3_slots(), B.v2_slots()):
        assert B.slot_problems(slots) == [], slots.entry.id


def test_the_page_renders_its_research_chapters_through_the_grammar(page):
    rendered = re.findall(r'<article class="chapter" id="(v\d+)"[^>]*data-grammar="chapter"', page)
    assert rendered == ["v4", "v3", "v2"]
    for chapter in rendered:
        body = page[page.index(f'<article class="chapter" id="{chapter}"'):]
        body = body[:body.index("</article>")]
        slots = [slot for slot in re.findall(r'data-slot="([^"]+)"', body)]
        assert slots == ["question", "main-chart", "not-established", "decision", "evidence", "details"], (chapter, slots)


@pytest.mark.parametrize("empty", ["question", "headline", "reading", "decision", "evidence"])
def test_negative_control_a_chapter_missing_a_slot_fails(empty):
    slots = dataclasses.replace(B.v3_slots(), **{empty: ""})
    with pytest.raises(B.ChapterError, match=empty):
        B.render_chapter(slots)


def test_negative_control_too_many_caveats_or_an_off_menu_detail_fails():
    slots = B.v3_slots()
    with pytest.raises(B.ChapterError):
        B.render_chapter(dataclasses.replace(slots, not_established=slots.not_established + ("v3.caveat.class",)))
    with pytest.raises(B.ChapterError):
        B.render_chapter(dataclasses.replace(slots, details=(("hours of the day", "<p>x</p>"),)))


def test_negative_control_a_main_chart_without_the_comparator_fails():
    slots = B.v2_slots()
    panels = tuple(dataclasses.replace(panel, rows=panel.rows[1:]) for panel in slots.chart.panels)  # drop v2 − LEAR
    with pytest.raises(B.ChapterError, match="comparator"):
        B.render_chapter(dataclasses.replace(slots, chart=dataclasses.replace(slots.chart, panels=panels)))


def test_chart_headlines_are_claim_bound_blocks(page):
    for chapter in ("v3", "v2"):
        assert f'<h3 id="{chapter}-chart-title" class="panel-title" data-block="{chapter}.chart_headline">' in page


# --------------------------------------------------------------------------- lineage and archive


def test_the_branch_cards_attach_to_the_lineage_with_their_content(page):
    lineage = page[page.index('id="journey"'):page.index('id="chapters"')]
    for entry in G.branches():
        card = lineage[lineage.index(f'id="{entry.anchor[1:]}"'):]
        card = card[:card.index("</li>")]
        assert f"{entry.name}<" in card and ">Not adopted<" in card
        for part in ("question", "result", "reason"):
            assert f'data-block="branch.{entry.id}.{part}"' in card, (entry.id, part)
        assert 'class="evidence-row"' in card


def test_v1s_archive_is_byte_identical_to_af0abb0(page):
    archive = archive_element(page)
    assert len(archive) == AF0ABB0_ARCHIVE_CHARS
    assert hashlib.sha256(archive.encode()).hexdigest() == AF0ABB0_ARCHIVE_SHA256


def test_the_recorded_archive_hash_is_af0abb0s_where_history_is_available():
    shown = subprocess.run(["git", "show", "af0abb0:docs/index.html"], cwd=REPO_ROOT, capture_output=True, text=True)
    if shown.returncode != 0:
        pytest.skip("Git history is not available in this checkout (shallow CI clone)")
    assert hashlib.sha256(archive_element(shown.stdout).encode()).hexdigest() == AF0ABB0_ARCHIVE_SHA256


def test_negative_control_an_edited_archive_is_caught(page):
    archive = archive_element(page)
    edited = page.replace(archive, archive.replace("preserved as published", "preserved"), 1)
    assert hashlib.sha256(archive_element(edited).encode()).hexdigest() != AF0ABB0_ARCHIVE_SHA256


def test_the_page_stays_within_its_size_budget(page):
    assert len(page.encode()) <= 2_000_000


def test_the_generation_colours_and_markers_stay():
    assert B.TOKENS["v1"] == "#475569" and B.TOKENS["v2"] == "#6D28D9" and B.TOKENS["v3"] == "#0F766E"
    assert [B.ROLE_STYLE[v]["marker"] for v in ("v1", "v2", "v3")] == ["triangle", "square", "circle"]


# --------------------------------------------------------------------------- evidence tiers (§7)


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[dict[str, str]] = []
        self.links: list[dict] = []
        self.current: dict | None = None

    def handle_starttag(self, tag, attrs):
        attributes = {k: v or "" for k, v in attrs}
        if tag == "a":
            self.current = {"href": attributes.get("href", ""), "text": "",
                            "in_row": any("evidence-row" in el.get("class", "") for el in self.stack),
                            "in_archive": any(el.get("class", "").startswith("v1-archive") or el.get("id") == "v1-archive"
                                              for el in self.stack)}
        if tag not in ("br", "img", "meta", "link", "input", "hr"):
            self.stack.append(attributes)

    def handle_endtag(self, tag):
        if tag == "a" and self.current is not None:
            self.links.append(self.current)
            self.current = None
        if self.stack and tag not in ("br", "img", "meta", "link", "input", "hr"):
            self.stack.pop()

    def handle_data(self, data):
        if self.current is not None:
            self.current["text"] += data


AUDIT_TARGET = re.compile(r"/blob/(?P<ref>[^/]+(?:/[^/]+)?)/(?P<path>(reports/|docs/track-b/evidence/)[^#?]*|[^#?]*-claims\.md|[^#?]*\.csv)")


def evidence_tier_problems(document: str) -> list[str]:
    """Standard §7: an audit-grade link (reports/, docs/track-b/evidence/, a claim map or a CSV)
    appears only in an evidence row, at an evidence tag, labelled "<type>, frozen <date>" with that
    tag's date. v1's archive is a frozen record and keeps its own links."""
    parser = Links()
    parser.feed(document)
    problems = []
    for link in parser.links:
        match = AUDIT_TARGET.search(link["href"])
        if not match or link["in_archive"]:
            continue
        ref = next((tag for tag in G.EVIDENCE_TAGS if f"/blob/{tag}/" in link["href"]), None)
        label = " ".join(link["text"].split()).rstrip(" ↗")
        if not link["in_row"]:
            problems.append(f"audit link outside an evidence row: {label!r}")
        if ref is None:
            problems.append(f"audit link not at an evidence tag: {link['href']}")
            continue
        wanted = rf"^.+, frozen {G.EVIDENCE_TAGS[ref][1]}$"
        if not re.match(wanted, label):
            problems.append(f"audit link label {label!r} is not '<type>, frozen {G.EVIDENCE_TAGS[ref][1]}'")
    return problems


def test_audit_grade_links_are_labelled_and_sit_in_evidence_rows(page):
    assert evidence_tier_problems(page) == []
    assert "Full report" not in page


def test_negative_control_a_misplaced_or_mislabelled_audit_link_is_caught(page):
    url = B.github("reports/weather-ablation/report.md", "evidence/cp-20")
    loose = page.replace("</main>", f'<p><a href="{url}">Full report</a></p></main>', 1)
    assert any("outside an evidence row" in problem for problem in evidence_tier_problems(loose))
    wrong_date = page.replace("Engineering report, frozen <span data-structural=\"date\">2026-09-24</span>",
                              "Engineering report, frozen <span data-structural=\"date\">2026-09-25</span>", 1)
    assert any("frozen 2026-09-24" in problem for problem in evidence_tier_problems(wrong_date))
    at_main = page.replace("/blob/evidence/cp-20/reports/weather-ablation/report.md",
                           "/blob/main/reports/weather-ablation/report.md", 1)
    assert any("not at an evidence tag" in problem for problem in evidence_tier_problems(at_main))


def test_the_readme_s_audit_links_are_labelled_at_their_tags():
    text = README.read_text()
    generated = text[text.index(readme_research.GLANCE_START):text.index(readme_research.END)]
    for label, url in re.findall(r"\[([^\]]+)\]\((https://github\.com/[^)]+)\)", generated):
        match = AUDIT_TARGET.search(url)
        if not match:
            continue
        ref = next(tag for tag in G.EVIDENCE_TAGS if f"/blob/{tag}/" in url)
        assert re.match(rf"^.+, frozen {G.EVIDENCE_TAGS[ref][1]}$", label), (label, url)


# --------------------------------------------------------------------------- the stack line (W13)


def test_the_stack_line_is_rendered_from_the_system_view(page):
    tools = B.stack_tools()
    line = page[page.index('<p class="stack-line" data-stack="system-view">'):]
    line = line[:line.index("</p>")]
    for tool in tools:
        assert tool in line
    assert tools == tuple(dict.fromkeys(t for _, _, state, ts in B.SYSTEM_VIEW if state == "implemented" for t in ts))
    assert page.index('id="system"') < page.index('data-stack="system-view"') < page.index('id="reproduce"')


# Regression for independent-check-3 F2: inspect the actual evidence row, not just slot labels.
def chapter_evidence_order_problems(document):
    class Order(HTMLParser):
        def __init__(self):
            super().__init__()
            self.markers = []

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if attrs.get("data-slot") in ("not-established", "decision", "details"):
                self.markers.append(attrs["data-slot"])
            if "ev" in attrs.get("class", "").split():
                self.markers.append("evidence-row")

    parsed = Order()
    parsed.feed(document)
    needed = ["not-established", "decision", "evidence-row", "details"]
    try:
        positions = [parsed.markers.index(marker) for marker in needed]
    except ValueError:
        return ["missing chapter boundary"]
    return [] if positions == sorted(positions) else ["chapter evidence out of order"]


@pytest.mark.parametrize("factory", [B.v3_slots, B.v2_slots])
def test_evidence_follows_limitations_and_decision_before_details(factory):
    assert chapter_evidence_order_problems(B.render_chapter(factory())) == []


@pytest.mark.parametrize("before", ['<aside class="caveats"', '<div class="decision"'])
@pytest.mark.parametrize("factory", [B.v3_slots, B.v2_slots])
def test_negative_control_moving_evidence_before_limitation_or_decision_fails(factory, before):
    slots = factory()
    html = B.render_chapter(slots)
    assert html.count(slots.evidence) == 1
    moved = html.replace(slots.evidence, "").replace(before, slots.evidence + before, 1)
    assert chapter_evidence_order_problems(moved)
