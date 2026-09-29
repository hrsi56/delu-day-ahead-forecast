"""PUBLISH_RULES 1.0 (PRES-2): the contracts the migration added, each with a negative control.

* A1 -- every headline value names its metric beside it, on the page and in the README.
* A2 -- the comparison's finding is placed by N x H - (N - 1) x h with the measured header; the rule's arithmetic and
  its refusal of a finding one pixel too low are checked here, the browser measurements by
  `scripts/check_reader_paths.py release`.
* A3 -- the registry's predecessor relation is one dated chain; every adopted transition has its summary, and a group
  of rejected branches is never headed as the transition.
* A4 -- the released model's documentation covers every §5.1 subject, belongs to the model the registry names as
  released, and refuses a released model it has no documentation for; its evidence is the released model's own.
* A5 -- every chart inside a chapter's details has a heading and a descriptive route from the chapter.
* F02-F04 of the 2026-09-29 review -- an inline icon, the measured start beside the demo action, and the represented
  days beside the hours.
* F01 -- the demo's control repair is in the built page (its behaviour is measured in browsers, not here).
"""

from __future__ import annotations

import dataclasses
import json
import re
import sys

import pytest

from delu_forecast import derived as D
from delu_forecast import registry as G
from delu_forecast import research as R
from delu_forecast import research_claims as RC
from delu_forecast.claims import REPO_ROOT, build_claims

sys.path.insert(0, str(REPO_ROOT / "scripts"))

import build_pages as B  # noqa: E402
import build_wasm_space as W  # noqa: E402
import check_reader_paths as CRP  # noqa: E402
import readme_research  # noqa: E402

PAGE = REPO_ROOT / "docs" / "index.html"
README = REPO_ROOT / "README.md"


@pytest.fixture(scope="module")
def page() -> str:
    return PAGE.read_text()


def _text(html: str) -> str:
    return " ".join(re.sub(r"<[^>]+>", "", html).split())


def _section(document: str, ident: str) -> str:
    start = document.index(f'id="{ident}"')
    start = document.rindex("<section", 0, start)
    depth = 0
    for match in re.finditer(r"<section\b|</section>", document[start:]):
        depth += 1 if match.group(0).startswith("<section") else -1
        if depth == 0:
            return document[start:start + match.end()]
    raise AssertionError(f"{ident} is not closed")


# --------------------------------------------------------------------------- A1


def a1_problems(headline_text: str) -> list[str]:
    """Each headline percentage is followed, before the next number, by the name of its metric."""
    problems = []
    for match in re.finditer(r"\d+%", headline_text):
        rest = headline_text[match.end():]
        following = re.split(r"\d", rest, maxsplit=1)[0]
        if match.start() > 0 and "at least" in headline_text[max(0, match.start() - 12):match.start()]:
            continue  # the rule's own margin, "at least 10% below", names both scores ("error scores")
        if not re.search(r"(point-error|interval) score", following):
            problems.append(f"{match.group(0)} is not named by its metric")
    return problems


def test_a1_every_headline_value_names_its_metric(page):
    text = _text(RC.headline())
    assert a1_problems(text) == []
    assert "on the point-error score" in text and "on the interval score" in text
    assert RC.headline("md") in README.read_text()


def test_a1_negative_control_the_pres1_wording_is_caught():
    old = ("Met both accuracy targets set before the experiments: error scores at least 10% below the strongest "
           "benchmark, daily LEAR (v3: 14% and 17% below; the first of 8 policies tested to meet them).")
    assert len(a1_problems(old)) == 2


# --------------------------------------------------------------------------- A2 (the rule's arithmetic)


def test_a2_limit_is_n_screens_less_the_header_on_every_screen_after_the_first():
    assert CRP.a2_limit(900, 2, 56) == 1744
    assert CRP.a2_limit(844, 3, 56) == 2420
    assert CRP.screen_of(1744, 900, 56) == 2 and CRP.screen_of(1745, 900, 56) == 3


def _view(bottom: float, header: float = 56, seen: tuple[float, ...] = ()) -> dict:
    placements = {"header_px": header, "headline": {"top": 60, "bottom": 700}, "terms": {"top": 705, "bottom": 800},
                  "finding": {"top": bottom - 50, "bottom": bottom}, "finding_chart": {"top": bottom + 20},
                  "release_rule": {"top": 300}, "demo_action": {"bottom": 290}, "byline": {"top": 10},
                  "release_rule_in_disclosure": False, "byline_in_disclosure": False,
                  "scroll_width": 1440, "client_width": 1440}
    return {"viewport": "1440x900", "view": "1440x900", "placements": placements,
            "placement_screens": {"header_px_seen": list(seen)} if seen else None}


def test_a2_a_finding_at_the_limit_passes_and_one_pixel_lower_fails():
    assert CRP.placement_findings(_view(1744)) == []
    assert any("beyond 1744" in problem for problem in CRP.placement_findings(_view(1745)))


def test_a2_negative_control_the_largest_header_seen_on_the_route_decides():
    assert any("beyond" in problem for problem in CRP.placement_findings(_view(1740, seen=(56, 64))))


def test_a2_negative_control_an_unmeasured_header_is_a_finding():
    assert any("not measured" in problem for problem in CRP.placement_findings(_view(1600, header=0)))


# --------------------------------------------------------------------------- A3


def test_a3_the_predecessor_relation_is_one_dated_chain():
    assert G.transition_problems() == []
    assert [(item.predecessor.id, item.successor.id) for item in G.transitions(newest_first=False)] == [("v1", "v2"), ("v2", "v3")]
    assert [item.comparator_is_predecessor for item in G.transitions(newest_first=False)] == [False, True]


@pytest.mark.parametrize("change, expected", [
    ({"v3": {"predecessor": None}}, "exactly one generation starts the main line"),
    ({"v2": {"predecessor": "daily-lear"}}, "is not a registered generation"),
    ({"v3": {"predecessor": "v1"}}, "precedes both"),
    ({"v1": {"predecessor": "v3"}}, "starts the main line"),
])
def test_a3_negative_controls_a_broken_chain_is_refused(change, expected):
    entries = tuple(dataclasses.replace(entry, **change[entry.id]) if entry.id in change else entry for entry in G.entries())
    assert any(expected in problem for problem in G.transition_problems(entries))


def test_a3_negative_control_a_successor_adopted_before_its_predecessor_is_refused():
    v2 = G.get("v2")
    early = dataclasses.replace(v2, statuses=(dataclasses.replace(v2.statuses[0], date="2026-09-01"),))
    entries = tuple(early if entry.id == "v2" else entry for entry in G.entries())
    assert any("adopted before its predecessor" in problem for problem in G.transition_problems(entries))


def test_a3_every_transition_has_its_summary_and_the_branches_are_headed_apart(page):
    journey = _section(page, "journey")
    for item in G.transitions():
        card = journey[journey.index(f'data-transition="{item.id}"'):]
        card = card[:card.index("</article>")]
        for field in ("Predecessor", "What changed", "Comparator", "Result", "Not established", "Decision"):
            assert f"<dt>{field}</dt>" in card, (item.id, field)
        assert f'href="#{item.successor.id}-chart-title"' in card
        if not item.comparator_is_predecessor:
            assert "<dt>Against the predecessor</dt>" in card and "No paired interval" in _text(card)
    assert "Experiments not adopted between" in _text(journey)
    assert not re.search(r"Experiments (between|after) ", _text(journey))
    assert journey.index('class="transitions"') < journey.index('class="branches"')


def test_a3_negative_control_a_transition_without_its_summary_blocks_stops_the_build(monkeypatch):
    blocks = {key: block for key, block in RC.BLOCKS_BY_KEY.items() if not key.startswith("transition.v2-v3.")}
    monkeypatch.setattr(RC, "BLOCKS_BY_KEY", blocks)
    with pytest.raises(B.ChapterError, match="v2-v3"):
        B.transitions_html()


def test_a3_the_readme_carries_the_same_transitions():
    text = README.read_text()
    for item in G.transitions():
        assert RC.render(f"transition.{item.id}.title", "md", surface=RC.README) in text
    assert "### Experiments not adopted between v1 and v2" in text and "Experiments that were not adopted" not in text


# --------------------------------------------------------------------------- A4


def test_a4_every_subject_is_documented_for_the_released_model(page):
    section = _section(page, "product")
    assert f'data-product="{G.released().id}"' in section
    subjects = " ".join(re.findall(r'data-subjects="([^"]+)"', section)).split()
    assert sorted(subjects, key=B.PRODUCT_SUBJECTS.index) == list(B.PRODUCT_SUBJECTS)
    routes = re.findall(r'<nav class="product-routes"[^>]*>.*?</nav>', section, re.DOTALL)[0]
    for anchor in re.findall(r'data-topic="([^"]+)"', section):
        assert f'href="#{anchor}"' in routes and f'<h3 id="{anchor}">' in section
    assert "How the product works" in section and "About v1" not in section


def test_a4_negative_control_an_undocumented_released_model_stops_the_build(monkeypatch):
    monkeypatch.setattr(G, "released", lambda: G.get("v3"))
    with pytest.raises(B.ProductDocsError, match="no documentation"):
        B.product_topics(build_claims(), B.build_chart_payload())


def test_a4_negative_control_a_missing_subject_stops_the_build(monkeypatch):
    def partial(C, payload):
        return tuple(topic for topic in B.v1_product_topics(C, payload) if "9" not in topic.subjects)

    monkeypatch.setitem(B.PRODUCT_DOCS, "v1", partial)
    with pytest.raises(B.ProductDocsError, match="missing"):
        B.product_topics(build_claims(), B.build_chart_payload())


def product_identity_problems(section: str, released: G.Entry) -> list[str]:
    """Evidence in the product documentation describes the released model: its own CP-2 record or holdout, or its
    development replay in the shared comparison; never another generation's result."""
    problems = []
    for record_id in set(re.findall(r'data-record="([^"]+)"', section)):
        if D.is_derived(record_id):
            problems.append(f"{record_id}: a research headline record in the product documentation")
            continue
        record = R.get(record_id)
        if record.generation != released.version and record.policy_code not in ("B0",):
            problems.append(f"{record_id} describes {record.generation or record.policy_code}, not {released.version}")
    return problems


def test_a4_the_documentation_s_evidence_belongs_to_the_released_model(page):
    assert product_identity_problems(_section(page, "product"), G.released()) == []


def test_a4_negative_control_another_generation_s_record_is_caught(page):
    doctored = _section(page, "product").replace(
        "</section>", '<data data-claim="P42" data-record="cp20.metrics.HG.equal_fold.S_MAE">0.5658</data></section>', 1)
    assert any("not v1" in problem for problem in product_identity_problems(doctored, G.released()))


def test_a4_fold5_and_frozen_shap_are_labelled_as_different_evidence():
    frozen = R.get("cp2.diagnostics.frozen_shap.1.mean_abs_shap")
    fold5 = R.get("cp2.diagnostics.fold5_shap.1.mean_abs_shap")
    assert frozen.evidence_class == R.EVIDENCE_CLASS_IN_SAMPLE and fold5.evidence_class == R.EVIDENCE_CLASS_DEVELOPMENT
    identity = _text(RC.render("product.attribution.identity"))
    assert "in-sample diagnostic" in identity and "out of sample" in identity
    assert "not make them the same evidence" in identity


def test_a4_the_released_model_s_own_records_agree_with_the_claim_set_and_the_shared_comparison():
    claims = build_claims()
    for level in ("50", "80", "95"):
        final = R.get(f"cp2.reliability.final.{level}").raw
        assert R.get(f"cp2.regime.all.coverage_{level}").raw == final == R.get(f"cp20.metrics.B1.pooled.coverage{level}").raw
        assert f"{float(R.get(f'cp2.holdout.coverage.final.{level}').raw):.4f}" == claims[f"holdout_coverage_{level}"]
    assert R.get("cp2.regime.all.n_obs").raw == "10747" and R.get("cp2.regime.all.n_days").raw == "448"


def test_a4_the_product_sources_are_blob_pinned_and_kept_out_of_the_mirror_manifest():
    for path, source in R.PRODUCT_SOURCES.items():
        R.check_source(path)
        assert path not in R.SOURCES and source.tag == "evidence/cp-2"
    manifest = json.loads((REPO_ROOT / "reports/presentation/mlflow-export/manifest.json").read_text())
    assert not set(R.PRODUCT_SOURCES) & set(manifest["sources"])


def test_a4_negative_control_a_changed_product_source_is_caught(monkeypatch):
    path = next(iter(R.PRODUCT_SOURCES))
    monkeypatch.setitem(R.PRODUCT_SOURCES, path, dataclasses.replace(R.PRODUCT_SOURCES[path], blob="0" * 40))
    with pytest.raises(R.EvidenceError, match="has changed"):
        R.check_source(path)


# --------------------------------------------------------------------------- A5


def detail_route_problems(chapter_html: str) -> list[str]:
    """Every chart inside a chapter's details sits under a detail heading that the chapter routes to."""
    problems = []
    navs = re.findall(r'<nav class="explore".*?</nav>', chapter_html, re.DOTALL)
    routes = set(re.findall(r'href="#([^"]+)"', navs[0])) if navs else set()
    details = chapter_html[chapter_html.index('data-slot="details"'):]
    for chart in re.finditer(r'<div class="chart" data-chart-id="([^"]+)"', details):
        # the heading must be inside the chart's own disclosure, before it
        own = details.rfind('<details class="disclosure" id="', 0, chart.start())
        heads = re.findall(r'<h4 class="detail-head" id="([^"]+)"', details[own:chart.start()])
        if not heads:
            problems.append(f"{chart.group(1)} has no detail heading before it")
        elif heads[-1] not in routes:
            problems.append(f"{chart.group(1)}'s heading {heads[-1]} has no route")
    return problems


@pytest.mark.parametrize("chapter", ["v3", "v2"])
def test_a5_every_detail_chart_has_a_descriptive_route(page, chapter):
    html = page[page.index(f'<article class="chapter" id="{chapter}"'):]
    html = html[:html.index("</article>")]
    assert detail_route_problems(html) == []
    assert "Explore these results" in html


def test_a5_negative_control_a_chart_without_its_heading_is_caught(page):
    html = page[page.index('<article class="chapter" id="v3"'):]
    html = html[:html.index("</article>")]
    doctored = re.sub(r'<h4 class="detail-head" id="v3-crisis">.*?</h4>', "", html, count=1, flags=re.DOTALL)
    assert any("v3-c4" in problem for problem in detail_route_problems(doctored))


def test_a5_the_preview_leads_to_the_product_replay_and_the_archive_keeps_its_route(page):
    assert 'href="#product-forecast">Explore this forecast' in page
    assert 'href="#forecast">The replay in the archived report' in page


# --------------------------------------------------------------------------- F02, F03, F04


def test_f02_the_page_carries_its_own_icon_inline(page):
    head = page[:page.index("</head>")]
    icons = re.findall(r'<link rel="icon" href="([^"]+)"', head)
    assert icons and all(icon.startswith("data:") for icon in icons)


def test_f02_the_icon_carries_no_address_for_the_link_gate(page):
    import check_links
    head = page[:page.index("</head>")]
    icon = re.findall(r'<link rel="icon" href="([^"]+)"', head)[0]
    assert icon.startswith("data:image/svg+xml;base64,") and not check_links._URL.findall(icon)


def test_f02_negative_control_an_icon_with_its_namespace_in_clear_is_read_as_an_address():
    import html
    import check_links
    clear = html.escape("data:image/svg+xml," + B.FAVICON_SVG, quote=True)
    assert check_links._URL.findall(clear)


def test_f02_negative_control_a_page_without_an_icon_is_caught(page):
    stripped = re.sub(r'<link rel="icon"[^>]*>', "", page)
    assert not re.findall(r'<link rel="icon" href="data:', stripped[:stripped.index("</head>")])


def test_f03_the_measured_start_is_beside_the_action_outside_any_disclosure(page):
    action = page.index('class="btn-primary external"')
    startup = page.index('data-startup="measured"')
    assert 0 < startup - action < 1500
    opened = page.rfind("<details", 0, startup)
    assert opened == -1 or page.rfind("</details>", 0, startup) > opened
    demo = B.demo_measurement()
    line = _text(page[startup:page.index("</p>", startup)])
    assert f"after {demo['seconds']} s in Chrome {demo['browser'].split('.')[0]}" in line
    assert f"public demo, {demo['date']}" in line and f"last verified {demo['verified']}" in line
    assert "MB on a first visit" in line


def test_f03_negative_controls_a_local_or_failed_record_is_refused(tmp_path):
    """The measured start must come from the public demo, and "last verified" needs every run to have reached a
    forecast: a local measurement or a failed run is refused rather than printed."""
    record = json.loads(B.DEMO_CHECK.read_text())
    local = json.loads(json.dumps(record))
    for run in local["runs"]:
        run["url"] = "http://127.0.0.1:8820/"
    failed = json.loads(json.dumps(record))
    failed["runs"][-1]["ready"] = False
    for name, doctored, message in (("local.json", local, "public demo"), ("failed.json", failed, "did not reach")):
        path = tmp_path / name
        path.write_text(json.dumps(doctored))
        with pytest.raises(ValueError, match=message):
            B.demo_measurement(path)


def test_f04_the_visible_population_states_hours_and_days_from_one_record(page):
    sub = page[page.index('data-block="comparison.sub"'):]
    sub = sub[:sub.index("</p>")]
    assert 'data-record="cp20.metrics.B0.pooled.n_hours"' in sub and 'data-record="cp20.metrics.B0.pooled.n_days"' in sub
    text = _text(sub)
    assert f"{R.display(R.get('cp20.metrics.B0.pooled.n_hours'))} historical hours over " \
           f"{R.display(R.get('cp20.metrics.B0.pooled.n_days'))} days" in text
    assert f"{len(G.comparison_rows())} policies" in text


def test_the_census_distinction_is_derived(page):
    sentence = _text(RC.census_sentence())
    rows = G.comparison_rows()
    tested = [entry for entry in rows if f"derived.criteria.{entry.id}.verdict" in D.records()]
    assert f"The chart's {len(rows)} rows are not that census: {len(tested)} of them" in sentence
    assert 'data-block="comparison.census"' in page and 'data-block="comparison.census.detail"' in page
    detail = _text(RC.census_detail())
    assert detail.startswith(f"The {D.get('derived.criteria.v3.tested').value} policies tested against the targets")


# --------------------------------------------------------------------------- F01 (the built Space page)


def test_f01_the_control_repair_is_injected_once_and_requests_nothing():
    page = W.inject_a11y(W.inject_startup("<html><head></head><body><main></main></body></html>", build_claims()))
    assert W.a11y_findings(page) == []


def test_f01_negative_control_a_page_without_the_repair_is_caught():
    page = W.inject_startup("<html><head></head><body><main></main></body></html>", build_claims())
    assert W.a11y_findings(page) == ["the control repair is missing or injected twice"]
    with pytest.raises(ValueError):
        W.inject_a11y(W.inject_a11y(page))


def test_f01_the_recorded_space_build_carries_the_repair():
    manifest = json.loads((REPO_ROOT / "reports" / "cp3b" / "space_wasm_bundle.json").read_text())
    assert manifest["control_repair"]["injected"] is True and manifest["problems"] == []
    assert manifest["control_repair"]["menu_name"] == W.MENU_NAME
