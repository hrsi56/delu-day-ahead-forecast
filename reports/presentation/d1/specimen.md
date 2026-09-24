# D1 visual specimen: record for the Owner's review

**PRES-1, 2026-09-25 (plan §12 D1, design review D10), round 2.** The Owner kept the design
direction at Stop 1 and returned D1 for a correction round. The review is
`docs/track-b/presentation-d1-editorial-review-2026-09-25.md` in the main checkout (SHA-256
`2193d2e5245bc1a3dbc70bf719c3265ebd84439a8afd9cf3e02b83b41f77b5f5`; not committed on this branch).
This record describes the corrected specimen. The specimen is built by the real generator from real
content; nothing in it is mocked.

## How to open it

```bash
uv run python scripts/build_pages.py --specimen .local/artifacts/presentation/d1-r2
open .local/artifacts/presentation/d1-r2/index.html
```

| File | What it shows |
|---|---|
| `index.html` | The whole page with real content. Its "Consistency across folds" disclosure starts open, as the specimen's opened secondary diagnostic. |
| `token-sheet.html` | The tokens with computed contrast, the type scale and the component states |
| `demo-states.html` | The Space's loading, failure, retrying and ready states, with the review's R08 wording |
| `stress-7.html` | Local only: seven generations, with v4–v7 as labelled placeholders. It is never published; a test refuses placeholder text on the real page. |
| `screenshots/` | Full-page screenshots at 1,440, 768, 390, 360 and 320 px, closed and with every disclosure open |
| `charts/` | Every chart photographed at 1,440, 390, 360 and 320 px, closed and open, plus the enlarged-figure view |
| `route/` | The phone landing screens after "Explore this forecast" |

`docs/index.html` on the branch is the same page without the specimen's opened disclosure. The
round-1 specimen stays in `.local/artifacts/presentation/d1/` for comparison.

## What changed, by review item

| Item | Change | How it was checked |
|---|---|---|
| R01 opening | The review's copy: eyebrow, title "Day-ahead electricity forecasts, with uncertainty.", description, status pair (demo v1 · Released model; research v3 · Weather features), the three actions, a one-line startup note, and a closed "What the demo does and startup details" disclosure whose measurement is read from the Phase 0 release record. The preview is labelled "Historical forecast · v1", with its caption, legend and "Explore this forecast". The research takeaway is the review's qualitative sentence; the opening shows no number. | Claim map rows P01–P06, P13; page guards (tests 30–31) |
| R02 phone order | The lineage is two plain-language lines; planned work is a one-sentence teaser plus a closed "See planned experiments"; the side rail lists generations only. | At 390 × 844 the preview starts at 841 px (1.0 screen) and the comparison at 2,572 px (round 1: about 3,600) |
| R03 repetition | Outcome tiles removed. Each chapter leads with its editorial subtitle, what changed, one main chart, one interpretation and one visible qualification. Values sit in "View values" tables. The opening shows no delta; the v3 outcome and v2 result sentences are README-only. | Reader rerun (below) |
| R04 v2 chart collision | The long upper endpoint is no longer overprinted in the row: the row shows "[−0.0036, see below]", and the full `+0.000003857628092332211` is printed under the plot, in the interpretation and in the values table. On phones, row values are left-aligned under their mark, clear of the zero line. | Chart check: no text overlap or clipping at 1,440, 390, 360 and 320 px |
| R05 whole reader route legible | Phone charts are drawn for a 296-unit column, with wrapped labels and 12 px page gutters under 340 px. v1's archived interactive replay now draws at its rendered width (12 px text, fewer hour ticks on phones) and redraws when the archive opens or the window resizes; its controls, the 95% coverage (0.9398) and the ×1.02 scenario caveat behave as before. | Route check at 390, 360 and 320 px: 12 px replay text, controls working |
| R06 wrong Results link | The research comparison is `#research-results`; the archive keeps `#results`. Every id on the page is unique. | Test 31 (unique ids, with a negative control); route check: the archive's "5 · Results" lands inside v1 |
| R07 table alternatives | Every research chart has a "View values" table from the same typed rows: overview, v3 C2a–C6, v2 charts 1 and 2. The preview has its caption; the full replay is in the archived report. | Page structure test; binding guards |
| R08 wording | The five page-copy changes, plus the two demo-state sentences ("Forecast calculations run locally in your browser."; "You can view the saved forecast and research results in the report without loading the model."). The system view separates the enforced information cutoff from documented source-availability assumptions and links the assumptions. `uv sync` is separated from the evidence rebuild. | Page text; stale-phrase guard |
| §5.1 header and rail | The rail's duplicate page list is gone. The phone header shows "DE-LU forecasts" (≤620 px) or "DE-LU" (≤440 px), as a home link with the full name as its accessible name. | Screenshots |
| §5.6 terms at first use | The fair-comparison note introduces the five historical test periods as "folds" and names the 2022 crisis fold; the overview explains normalized scores beside the chart; the v2 story explains the baseline and the control. | Reader rerun |

## Visual pass over every chart

The Owner asked for a visual pass over every chart. Each chart was photographed and measured at
1,440, 390, 360 and 320 px, closed and with every disclosure open: the preview, the overview, v3
C2a–C6, v2 charts 1 and 2, v1's archived replay and its controls, and the archive's seven figures.
`check_reader_paths.py charts` measures text overlap, text cut off at the chart edge and the smallest
rendered text. `route` follows the preview into the replay on phones.

Defects the pass found beyond the review, all fixed:

| Chart | Defect | Fix |
|---|---|---|
| v3 C2a, v2 chart 2 (phones) | The leftmost tick label ("−0.12", "−0.04") was cut off at the left edge | Phone scales start 22 units in |
| v2 chart 2, C2a, C2b (phones) | Right-aligned values crossed the black zero line | Values are left-aligned under their row |
| Overview, v2 chart 1 (phones) | Reference lines ran through the row labels | Row labels carry a white halo |
| v3 C5 (all widths) | The axis caption touched the last panel's hour labels | 14 px more space |
| v3 C6 (desktop) | The coverage panel's label column was narrower than "50% interval" | The label column fits its longest label |
| v3 C3, C6 | Overlapping marks (v2 and v3 almost equal) merged into one shape | A surface-coloured ring under every mark |
| v1 replay (desktop) | 11 px text | 12 px at every width |
| Archive figures | The seven v1 figures render at 0.19–0.46 of their size on phones, and the three spectral figures at 0.19 on desktop, so their text is unreadable | Each figure opens full size in a dialog on click, Enter or Space (fit to width on desktop; about twice the screen width on a phone, scrollable), reusing the embedded image; Escape closes it and returns focus. The archive's layout is unchanged. |
| Whole page at 320 px, archive open | 14 px horizontal overflow from an unbreakable URL in the archive | Archive paragraphs and list items wrap long words |

## Measured layout (Chrome 153, fresh context; `layout-measurements.json`)

| Width | Horizontal overflow (closed / open) | Smallest chart text | Chart captures with overlap or clipping |
|---|---|---|---|
| 1,440 px | none / none | 12 px (v1 replay); new charts 12.26 px (preview) | 0 of 16 |
| 768 px | none / none | 12 px (v1 replay) | not measured per chart |
| 390 px | none / none | 12 px (v1 replay); new charts 14.58 px | 0 of 16 |
| 360 px | none / none | 12 px (v1 replay); new charts 13.26 px | 0 of 16 |
| 320 px | none / none | 12 px (v1 replay); new charts 12.21 px | 0 of 16 |

The 12 px floor (invariant 23) now holds at every measured width, including 320 px and the
archived replay. Round 1 recorded 10.64 px at 320 px and did not measure the replay.

| Viewport | Preview starts | Comparison starts | Screens to preview / comparison |
|---|---|---|---|
| 390 × 844 | 841 px | 2,572 px | 1.00 / 3.05 |
| 360 × 780 | 920 px | 2,679 px | 1.18 / 3.43 |
| 320 × 640 | 974 px | 2,774 px | 1.52 / 4.33 |
| 1,440 × 900 | 104 px | 1,813 px | 0.12 / 2.01 |

## Tokens (plan §7.3, unchanged)

Contrast was computed from the hex values with the WCAG relative-luminance formula (vs white /
vs the canvas):

| Token | Value | vs white | vs canvas |
|---|---|---:|---:|
| `--canvas` | `#FAFAFA` | 1.04 | 1.00 |
| `--surface` | `#FFFFFF` | 1.00 | 1.04 |
| `--border` | `#E4E4E7` | 1.27 | 1.22 |
| `--text` | `#18181B` | 17.72 | 16.97 |
| `--text-2` | `#52525B` | 7.73 | 7.41 |
| `--accent` | `#1D4ED8` | 6.70 | 6.42 |
| `--primary` | `#18181B` | 17.72 | 16.97 |
| `--primary-hover` | `#3F3F46` | 10.44 | 10.01 |
| `--primary-pressed` | `#52525B` | 7.73 | 7.41 |
| `--v1` | `#475569` | 7.58 | 7.26 |
| `--v2` | `#6D28D9` | 7.10 | 6.81 |
| `--v3` | `#0F766E` | 5.47 | 5.24 |
| `--ref` | `#71717A` | 4.83 | 4.63 |
| `--badge-bg` | `#F4F4F5` | 1.10 | 1.05 |
| `--badge-text` | `#3F3F46` | 10.44 | 10.01 |
| `--caveat-rule` | `#52525B` | 7.73 | 7.41 |
| `--grid` | `#E4E4E7` | 1.27 | 1.22 |

- **Generation colours against each other:** v1/v2 1.07:1, v1/v3 1.38:1, v2/v3 1.30:1. Each
  generation therefore also has its own marker (v1 triangle, v2 square, v3 circle), and every
  mark carries a direct label or value.
- **Decorative only:** the border and grid colours. Borders that carry state (the adopted-feature
  box, dashed planned items, the caveat rule, the focus outline) use `--text-2`, `--v3` or
  `--accent`, all above 3:1. Dashed outlines now mean "planned" only; the finished experiments in
  the lineage have solid outlines.

## Waiting on the Owner

- **Contribution wording.** The review proposes a replacement (§5.2), subject to the Owner's
  explicit approval. The page still shows the plan §8.9 wording, unchanged.
- **A public name for a byline.** The review recommends a compact byline near the opening, linked to
  the full statement (§5.2, §5.4). It needs the Owner's approved public name, so no byline is shown.
- **The 2026-09-24 device test.** The device, browser and outcome are still unrecorded; emulated
  widths do not stand in for them (§5.3).

## Not checked in D1

- **Desktop Safari and a real iPhone.** WebKit ran through Playwright for the demo only. The §11.3
  browser and accessibility checklist runs in Phase E. That checklist covers keyboard order
  (including the figure dialog), 200% zoom and screen-reader announcements.
- **No WCAG conformance is claimed** from screenshots or computed contrast.
