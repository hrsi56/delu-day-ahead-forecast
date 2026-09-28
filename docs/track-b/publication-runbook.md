# Publication runbook

**Publication Standard v1 §12; written by the PRES-1 conformance task (brief W15), 2026-09-28.**
This lists every place a publication touches: the files and symbols to change, in order, for an
adopted generation, a branch card, a changed population and each status transition the registry
defines. It does not add requirements; the standard, the checkpoint's brief and plan revision 3
(as the standard's §15 amends it) govern.

**How it stays true.** Every touchpoint below is written `file::symbol`.
`tests/test_42_publication_runbook.py` resolves each one in the code, and checks that the lists
between `runbook:` markers equal the registry's and the renderer's own: the registry's fields,
kinds and statuses, the chapter grammar's slots and detail menu, and the MLflow route patterns. A
runbook that falls behind the code fails CI.

**Generated files are never hand-edited.** Every surface is rebuilt by
`uv run python scripts/rebuild_presentation.py` (the page, the README's generated blocks, both
Space cards and the MLflow export), and the Space bundle by `make wasm`.

---

## 1. The order of a publication (standard §12)

1. **Build from the packet** (`docs/track-b/publication-packet-template.md`): the checkpoint's
   return carries it.
2. **One editorial review** against the standard.
3. **The cold-reader check** (standard §11): a fresh agent, the rendered screens only, disclosures
   closed, six questions.
4. **The independent check**, in a clean detached worktree at the candidate SHA.
5. **The MLflow upload and verification:** `scripts/mlflow_publish.py::main` (on the Owner's
   instruction for that action), then `scripts/verify_mlflow_mirror.py::verify`, the browser route
   check `scripts/check_reader_paths.py::mlflow_routes`, and the index,
   `scripts/verify_mlflow_mirror.py::write_index`.
6. **The final build:** `scripts/build_pages.py::main` with `--final`, which refuses unless the
   index covers `src/delu_forecast/registry.py::expected_routes`
   (`scripts/build_pages.py::route_coverage`).
7. **A focused recheck** on the final SHA.
8. **Landing, push and the Space redeploy**, by the Owner or on his explicit instruction naming the
   action (`AGENTS.md` § Git and publication authority). The pre-push hook runs the secret guard,
   then `scripts/publication_guard.py::pre_push`.
9. **The post-deploy checks.**

---

## 2. A new adopted generation (v4)

The checkpoint's packet supplies every value. Work in this order; each step is one touchpoint.

| # | Touchpoint | What changes |
|---|---|---|
| 1 | `src/delu_forecast/registry.py::_ENTRIES` | The new entry, with every field of §5 below. Its first status is `adopted in research`, dated, with its landing record as the source. The version number is given only now, at adoption (plan §16 decision 2). |
| 2 | `src/delu_forecast/registry.py::CHECKPOINTS` | The checkpoint that produced it: its MLflow run key, owner, evidence tag and SHA, freeze date, report, verdict, landing record and children. |
| 3 | `src/delu_forecast/registry.py::EVIDENCE_TAGS` | The checkpoint's evidence tag and the date it froze: every audit-grade label takes its date from here (standard §7). |
| 4 | `src/delu_forecast/registry.py::RULES` | Only if the governing plan set a new pre-specified rule, with the date it was set. |
| 5 | `src/delu_forecast/registry.py::COMPARISON_ORDER` | Where the new generation sits in the comparison, newest first. `src/delu_forecast/registry.py::COMPARISON_EXPERIMENT` names the experiment whose population the comparison draws on; a new population is section 4, not this. |
| 6 | `src/delu_forecast/registry.py::CRISIS_ORDER` | Only if its chapter shows the crisis window. |
| 7 | `src/delu_forecast/research.py::SOURCES` | The checkpoint's committed rows, each pinned by its Git blob, and the records read from them (`src/delu_forecast/research.py::records`). No generator types a number. |
| 8 | `src/delu_forecast/derived.py::CRITERIA_FILES` | The checkpoint's criteria file, so the verdict, the distance from the comparator and N are derived (standard §3.3 a). |
| 9 | `src/delu_forecast/derived.py::CHANGES` | The change against its comparator, with the interval from the checkpoint's own bootstrap draws from CP-21 on (standard §3.3 b). |
| 10 | `src/delu_forecast/derived.py::PERIOD_SUBJECTS` | The per-period MAE ranges, with the stress period the protocol names (standard §3.3 c). |
| 11 | `docs/track-b/research-content/` | The checkpoint's claim map, registered in `src/delu_forecast/research_claims.py::CLAIM_MAPS`. |
| 12 | `src/delu_forecast/research_claims.py::BLOCKS` | The chapter's claim blocks, named `v4.<slot>`: at least the question, the change, the chart headline, the reading, one to three things not established and the dated decision. Status words come only through registry tokens (`{g:…}`). The headline block needs no edit: `src/delu_forecast/research_claims.py::headline_template` takes the current generation from the registry. |
| 13 | `scripts/build_pages.py::v3_slots` | The model for a `v4_slots` function returning `scripts/build_pages.py::ChapterSlots`, with its main chart as `scripts/build_pages.py::MainChart` panels. `scripts/build_pages.py::slot_problems` refuses a chapter that misses a slot. |
| 14 | `scripts/build_pages.py::chapter_sequence` | Register the new chapter builder. A registered generation without one is a build error. |
| 15 | `scripts/build_pages.py::CHARTS_BY_RUN` | The charts its MLflow run carries as artifacts. |
| 16 | `scripts/build_pages.py::TOKENS` | **The Owner decides first:** plan §7.8 encodes a generation by colour, and the tokens are his (standard §16, "At v4"). Then its colour and the classes in `scripts/build_pages.py::css`. |
| 17 | `scripts/mlflow_export.py::CHECKPOINTS` | The checkpoint's export specification: protocol, anchor version, model code SHA, evidence reference and note. Run names, parents, descriptions and tags then come from the registry (`src/delu_forecast/registry.py::mlflow_run_name`). |
| 18 | `tests/` | New re-derivation tests with negative controls for the new records (as `test_29` and `test_36` do); the registry, parity, lint and export contract tests need no edit. |

**What follows without an edit:** the opening's status pair and headline
(`scripts/build_pages.py::opening`), the rail and jump row (`scripts/build_pages.py::rail`,
`scripts/build_pages.py::jump_row`), the lineage (`scripts/build_pages.py::lineage`), the
comparison rows (`scripts/build_pages.py::overview_panels`), the chapter order, the README's
glance and generation list (`scripts/readme_research.py::build_glance`,
`scripts/readme_research.py::generation_section`), both Space cards' model line
(`scripts/build_space.py::model_lines`), the MLflow run set
(`src/delu_forecast/registry.py::expected_run_keys`) and routes
(`src/delu_forecast/registry.py::expected_routes`).

**Limits to watch.**

- **The §1 placements.** On 2026-09-28 the comparison's finding sentence ends at about 2,490 px of
  the 2,532 px a phone allows (390 × 844), and at about 1,767 px of 1,800 on desktop; the headline
  block ends at about 775 px of 900. A longer opening or lineage can push them out; measure in
  Chrome and WebKit before the independent check (`scripts/check_reader_paths.py::release`).
- **Chart text of at least 12 px at every width.** The opening's preview sits in the right-hand
  column; narrowing that column below about 460 px on desktop shrinks its text under 12 px.
- **The size budget, 2.0 MB** (standard §6). The page was 1.56 MB on 2026-09-28. If a chapter would
  breach it, or at v5, the Orchestrator proposes a compaction rule to the Owner.

## 3. A branch card (a checkpoint that yields only a rejected branch)

The headline stays with the current adopted generation (standard §3.5).

| # | Touchpoint | What changes |
|---|---|---|
| 1 | `src/delu_forecast/registry.py::_ENTRIES` | An entry of kind `branch`: a descriptive name (no version number), its question, what it informed, its comparator, and a dated `not adopted` status with a one-line reason. Its study arms are entries of kind `study arm`. |
| 2 | `src/delu_forecast/registry.py::CHECKPOINTS` | Its checkpoint, with the children MLflow lists under it. |
| 3 | `src/delu_forecast/registry.py::EVIDENCE_TAGS` | Its evidence tag and freeze date. |
| 4 | `src/delu_forecast/research_claims.py::BLOCKS` | `branch.<id>.question`, `branch.<id>.result` and `branch.<id>.reason`, mapped in its claim map. |
| 5 | `scripts/mlflow_export.py::CHECKPOINTS` | Its export specification. |

`scripts/build_pages.py::branch_card` draws the card and `scripts/build_pages.py::lineage` attaches
it where it belongs in time, including after the latest generation; the README lists it through
`scripts/readme_research.py::branch_section`; its MLflow route is `compare:<id>`.

## 4. A changed population

If the evaluated population changes, the page says so, and no metric is switched because of it
(standard §3.5).

| # | Touchpoint | What changes |
|---|---|---|
| 1 | `src/delu_forecast/registry.py::POPULATIONS` | A new comparability ID with a plain description. |
| 2 | `src/delu_forecast/registry.py::_ENTRIES` | The entry's `population`, and a `Code` per experiment carrying its population. |
| 3 | `src/delu_forecast/registry.py::COMPARISON_EXPERIMENT` | A new comparison, on the new population; the earlier comparison stays in its chapter (standard §5). The build refuses a chart that mixes comparability IDs (`src/delu_forecast/registry.py::population_in`). |
| 4 | `scripts/mlflow_export.py::CHECKPOINTS` | The export's comparability groups, so `delu.comparability_id` separates the two populations. |

## 5. Status transitions, as far as they are defined

A status is appended to the entry's dated history in `src/delu_forecast/registry.py::_ENTRIES`
(`src/delu_forecast/registry.py::StatusEvent`: status, date, source, reason). Nothing is typed on a
surface: templates are dated and in the past tense (`src/delu_forecast/registry.py::status_sentence`),
and the hero is the highest status reached (`src/delu_forecast/registry.py::hero`, in the order of
`src/delu_forecast/registry.py::HERO_ORDER`).

<!-- runbook:statuses -->
| Status | When | What it changes |
|---|---|---|
| `adopted in research` | A checkpoint lands and its brief adopts the generation | It becomes the current generation (`src/delu_forecast/registry.py::current_generation`): the headline block, the research half of the status pair, the chapter at the top |
| `not adopted` | A branch, study arm or control is rejected | Its card or row carries "Not adopted" with the reason (`src/delu_forecast/registry.py::adoption_label`) |
| `released` | The model the demo runs is released | The release rule names it (`src/delu_forecast/registry.py::release_sentence`); the demo, both Space cards and the released half of the status pair follow. Exactly one model is released (`src/delu_forecast/registry.py::released`) |
| `final candidate` | The final model is frozen for its one-shot test | Defined in the registry's vocabulary; the one-shot badge, wording, headline window and the rule for switching the hero are decided before that test (standard §16) |
| `live` | The final model runs prospectively | Defined in the registry's vocabulary; the live panel, `delu-live` and the registered policy wait for their triggers (standard §16) |
| `retired` | A model is withdrawn | Defined in the registry's vocabulary; its limitations stay in its archive (standard §8) |
<!-- /runbook:statuses -->

## 6. The registry entry's fields (standard §5)

Every entry carries all of them; `tests/test_35_registry.py` refuses one that does not.

<!-- runbook:registry-fields -->
- Identity: `id`, `name`, `subtitle`, `short`
- Kind: `kind`
- Codes: `codes` (one per experiment; one identity across codes, as v2 is `V2-H` in CP-16 and `H0` in CP-20)
- Status history, dated: `statuses`
- Comparison: `comparator`, `population`
- Evidence: `evidence_class`, `plan`, `rules`, `sources`, `claim_map`, `run_keys`
- Presentation and place: `style`, `anchor`, `checkpoint`, `after`, `question`, `informed`
<!-- /runbook:registry-fields -->

The kinds:

<!-- runbook:kinds -->
`generation`, `branch`, `reference`, `study arm`, `control`
<!-- /runbook:kinds -->

## 7. The chapter grammar (standard §6)

`scripts/build_pages.py::render_chapter` fills these slots, in this order:

<!-- runbook:slots -->
`question`, `change`, `chart`, `headline`, `reading`, `not_established`, `decision`, `evidence`, `details`
<!-- /runbook:slots -->

The details come only from this menu, in this order (`scripts/build_pages.py::DETAIL_MENU`):

<!-- runbook:details -->
`method`, `per-period consistency`, `stress period`, `coverage and width`, `protocol and review`
<!-- /runbook:details -->

v1's chapter follows §4 and its archive is never migrated (`scripts/build_pages.py::v1_chapter`).

## 8. MLflow routes

`src/delu_forecast/registry.py::expected_routes` derives the routes from the registry; each is
checked by REST and in a browser before it is linked, and a route that is not verified has its link
omitted (standard §9). The patterns:

<!-- runbook:routes -->
`experiment`, `compare:overview`, `compare:<generation id>`, `compare:<branch id>`
<!-- /runbook:routes -->

## 9. The checks before the independent check

Recorded under `reports/presentation/release-checks/` and in the checkpoint's evidence folder.

- `uv run pytest -q` on Python 3.13, and a clean Python 3.12 run of every step of
  `.github/workflows/tests.yml`.
- `make verify`; `make lint-publication`; `make publication-guard` (a non-final tree fails it by
  design until the final build).
- Determinism: `uv run python scripts/rebuild_presentation.py`, then `git status` is empty.
- `uv run python scripts/check_links.py`.
- The standard's §10 release checks: `scripts/check_reader_paths.py::main` in Chrome and WebKit at
  every width, with the accessibility trees, keyboard, touch, contrast and failed requests, and the
  §1 placements. Every record states that no real Safari, iPhone or screen reader was used.
- The standard's §11 cold-reader check.
