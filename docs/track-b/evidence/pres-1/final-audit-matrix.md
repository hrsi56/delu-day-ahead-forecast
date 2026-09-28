# PRES-1: closing the final audit (F01–F11) and both independent-check rounds

**Source:** the Owner's final editorial audit of 2026-09-28
(`presentation-final-editorial-audit-2026-09-28.md` in this folder, SHA-256 `f702d4ee…ffd1d`).

- **Baseline:** the audit reviewed `d6ea57d`.
- **The finishing round:** landed at `9d2ca92`; the reader-driven fixes at `126abea`.
- **Where each result is checked:** "Check" names the test, command or record. The final
  candidate's independent verdict re-checks all of them.

## F01–F11

| # | Finding | Change | Files | Check and result |
|---|---|---|---|---|
| F01 | The README showed differences as scores and pointed at a chart it does not contain | The README says "Difference versus v2 in normalized score (v3 − v2), with 95% confidence intervals. Negative values favour v3." and gives "Point-error difference" and "Interval-score difference". The v2 lines name their comparator (v2 − daily LEAR, v2 − pooled control). There is no chart reference, and "here" became "the shared development comparison". | `research_claims.py`, `readme_research.py`, `README.md` | `test_the_readme_labels_differences_as_differences` passes; the README research block has been reread |
| F02.1 | `aria-labelledby="overview-title"` had no target | The comparison's title carries that id | `build_pages.py` | `test_every_accessibility_reference_resolves`, with a negative control: 0 unresolved references |
| F02.2 | v2's criteria sentence showed only criterion 1's two values | "Both v2 arms miss criteria 1–2, the point-error and interval-score thresholds, and meet criteria 3–6." | `research_claims.py` (`v2.result.criteria`) | The page binding tests pass; claim C39 is unchanged |
| F02.3 | "Closer to nominal is better" had no marked nominal | A dashed "nominal 95%" line at 95% of the window's hours, computed from the record. The crisis note says it is a computed target, not an observed count, and that there is no coverage guarantee. | `build_pages.py` (`c4_panels`, the crisis note) | Chart check: no overlap or clipping at four widths. Viewed at 1,440 and 390 px. |
| F02.4 | C3's axis ends read 8 and 4 | Already fixed at `3afae02` (`end_label`) | — | `test_axis_end_labels_state_their_domain_exactly`; the final check re-verifies it |
| F03 | Repeated conclusions and bold paragraphs | Removed the chapter preamble and v3's subtitle. The comparison title is "v3 leads the shared development comparison." with the audit's subtitle. The v3 interpretation, limitation and decision use the audit's wording. `.finding` is no longer bold. The crisis-window summary stays visible. | `build_pages.py`, `research_claims.py` | Main prose went from 1,582 to 1,325 words (−16%) at 390 px with disclosures closed, excluding charts, tables and the archive; the audit asked for about 20%, and what remains is approved copy, required labels and limitations. At 390 px the comparison starts at 2,572 px (was 2,624) and v3 at 5,209 px (was 5,573). |
| F04 | Internal meta-text | Removed "None has a score…", the CSS note, "Nothing here promotes…" and "instant report". The rebuild timing moved into "One measured rebuild", with its date and record. | `build_pages.py`, `readme_research.py`, `build_wasm_space.py` | `NETWORK_ABSOLUTES` guard; the page was reread |
| F05 | Future work promised "data that was never used" | "Frozen-protocol evaluation, then prospective monitoring": the evaluation window and evidence classification remain to be finalized. "Do separate models for different hours improve forecasts?" Licence and resource conditions are behind a link to the plan. | `build_pages.py` (`PLANNED_WORK`), claim map P10 | The page was reread; P10 updated |
| F06 | The availability claim was too broad, and the holdout DM was unidentified | "Forecast-cutoff checks; source-availability assumptions documented", with "Checked in code" separated from "Assumed and documented". The holdout DM is identified as a one-sided test on daily pinball-loss vectors, not on MAE; p = 0.948 is read as "no evidence of an advantage". | `build_pages.py`, `research_claims.py`, claim map P11 | `holdout_report.json`: `dm.analysis` = `probabilistic_daily_vector_pinball` |
| F07 | The demo and the cards were heavy and too absolute | Reordered the notebook, under the Owner-approved extension: title and replay label, controls and forecast, identity summary (with "Maximum absolute deviation"), limitations, then folded "What this page downloaded", "Evidence and tracking" and "Reproducibility"; the attribution stays visible. Added a phone drawing of the forecast chart (12.5 px text) with an outlined band; the controls wrap. The cards say "self-contained page with no additional runtime requests". Two Owner-approved `claims.py` strings drop "no server". | `app/wasm_showcase.py`, `build_wasm_space.py`, `claims.py`, `space-wasm/README.md` | The running local build was checked, not just the source (`2026-09-28-demo-local.json`, `2026-09-28-space-states-local.json`): ready in 10–12 s in Chrome and WebKit at 1,440 and 390 px, both controls change the view, all four startup paths pass. `test_22` equivalence passes; the notebook computes nothing new. |
| F08 | Archive statements about downloads and Docker are historical | A context note in the archive wrapper, and one under the replay heading, where the preview link lands. The historical text is unchanged. | `build_pages.py` (`v1_chapter`, `v1_archive`) | Invariant 24 holds (test_31) |
| F09 | Visual consistency | Each chart has one result title, then its interpretation, limitation, evidence and values. The v2 title uses the audit's wording. There is one attribution block, which the footer links to. The contribution is in body type. The unavailable evidence item aligns with its row. | `build_pages.py` | Screens at five widths; chart and a11y probes pass |
| F10 | MLflow links are a real publication blocker | Not hidden: the four `data-unpublished` markers stay, and `--final` still refuses them. The upload (F1), mirror check, real links and final build (F2–F4) need the Owner's instruction. | — | Open, by design, until F1 is instructed |
| F11 | Safari, iPhone and VoiceOver are not recorded | Checklist for the Owner, covering the report and the demo | `owner-hand-checks.md` | **Open**, awaiting the Owner's results |

## The final reader round

A fresh reader got the six tasks plus the audit's two checks: score against difference, and
confidence interval against prediction interval. It answered all of them correctly. The four points
it tripped on are fixed at `126abea`, and the rest are recorded in `reader-tasks-final.md`.

## The independent check's findings (rounds 1 and 2)

| Round | Finding | Disposition |
|---|---|---|
| 1 | Invariant 17: typed numbers in the MLflow notes and the token sheet | Fixed at `67570c8`. Numbers are read from records, and `test_no_generator_types_a_research_number` has negative controls. |
| 1 | §11.3 not on Safari or iPhone; non-text contrast not measured | Non-text contrast fixed at `67570c8`: the bands are outlined, and every chart shape is measured (0 below 3:1). Safari, iPhone and VoiceOver are F11, open. |
| 1 | C5 stated no direction | Fixed at `67570c8`: "lower is better" |
| 1 | Observation: the `delu-generations` note used the present tense before the upload | Fixed at `67570c8`: future tense until `mlflow_index.json` exists |
| 1 | Observation: the rebuild check depends on the build date | Pre-existing (`pages_build.json` stamps the date); recorded, not changed |
| 1 | Observation: the keyboard probe covered 40 stops | Fixed: it walks every stop (56) |
| 2 | §11.3 on the named devices | F11, open |
| 2 | C3 axis ends 8 and 4 for 7.5 and 4.5 | Fixed at `3afae02` |
