# D1 visual specimen: record for the Owner's review

**PRES-1, 2026-09-25 (plan §12 D1, design review D10).** The specimen is built by the real
generator from real content; nothing in it is mocked. The Owner approves or amends the desktop
and phone compositions before the template is extended (Stop 1).

## How to open it

```bash
uv run python scripts/build_pages.py --specimen .local/artifacts/presentation/d1
open .local/artifacts/presentation/d1/index.html
```

| File | What it shows |
|---|---|
| `index.html` | The whole page with real content. Its "Consistency across folds" disclosure starts open, as the specimen's opened secondary diagnostic. |
| `token-sheet.html` | The tokens with computed contrast, the type scale, and the component states |
| `demo-states.html` | The Space's loading, failure, retrying and ready states, built from the markup D2 injects into the Space |
| `stress-7.html` | Local only: seven generations, with v4–v7 as labelled placeholders, to test the rail, the jump row and the chapter rhythm. It is never published; a test refuses placeholder text on the real page. |
| `screenshots/` | Full-page screenshots at 1,440, 768, 390 and 360 px, with every disclosure closed and again with every disclosure open, plus a 320 px reflow check (not committed, plan §11.3) |

`docs/index.html` on the branch is the same page without the specimen's opened disclosure.

## What D1 covers (plan §12, D1)

| # | Required | Where |
|---|---|---|
| 1 | Opening with the v1 preview, the status pair and the action hierarchy | Top of the page: title, supporting sentence, "Released demo · v1" and "Latest research · v3", one primary action (Try the v1 demo), two quiet routes, the startup line with its measurement context, and v1's saved historical replay as a static chart labelled "Historical replay". |
| 2 | Branching lineage and the full seven-policy comparison | "How it evolved": v1 → v2 → v3 on the main line; CP-10, CP-15 and CP-20 as branches with what they informed; planned work in a separate, unscored block. "What improved": the two-panel dot plot, fairness note, table alternative and definitions (including the F07 note). |
| 3 | A complete v3 chapter with its caveats and one secondary diagnostic opened | Problem, hypothesis, change and feature diagram; two outcome tiles; the main chart (C2a); where it helps and where it does not; the caveats; the decision; the evidence row; disclosures C1–C6 and protocol details. |
| 4 | The longest badge, the long H−P endpoint, an evidence row, a table and disclosure states | The v1 holdout badge; `+0.000003857628092332211` in the v2 chapter's chart, sentence and token sheet; evidence rows with MLflow shown as unavailable until publication; tables; closed and open disclosures. |
| 5 | Desktop and phone layouts, and a seven-generation stress case | The screenshots; `stress-7.html` |
| 6 | A specimen of the demo states | `demo-states.html` |

## Tokens (plan §7.3, unchanged as the starting point)

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
  `--accent`, all above 3:1.
- **Additions to §7.3:** hover and pressed shades of the primary action, the badge colours, the
  caveat rule and the grid colour.

## Measured layout (Chrome 153, fresh context; `layout-measurements.json`)

| Width | Horizontal overflow | Smallest rendered chart text |
|---|---|---|
| 1,440 px | none | 12.26 px |
| 768 px | none | 17.88 px (phone variants from 819 px down) |
| 390 px | none | 13.49 px |
| 360 px | none | 12.27 px |
| 320 px (reflow) | none | 10.64 px |

With every disclosure open the results are the same. The 12 px floor (invariant 23) is set at
390 px and holds down to 360 px; at the 320 px reflow width chart text is 10.6 px, readable but
below the floor.

## Not checked in D1

- **Desktop Safari and a real iPhone.** WebKit ran through Playwright for the demo only. The
  §11.3 browser and accessibility checklist, including keyboard order, 200% zoom and screen-reader
  announcements, runs in Phase E.
- **No WCAG conformance is claimed** from screenshots or computed contrast.
