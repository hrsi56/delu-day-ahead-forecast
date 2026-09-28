# PRES-1 reader tasks, final round (plan §11.4; final audit step 7)

**2026-09-28, at `9d2ca92`** (the finishing round), before the reader-driven fixes at `126abea`.

**The reader.** A fresh subagent with no context, not coached. It opened only a pack built from
the committed page with every disclosure closed:

- 11 desktop screens at 1,440 × 900 and 18 phone screens at 390 × 844;
- the visible text and links;
- the README's research block.

The "screens" below count screenshots, not human reading time.

| # | Task | Answer (summary) | First found (desktop / phone) |
|---|---|---|---|
| 1 | The product and how to try it | Hourly day-ahead price forecasts with uncertainty, on past days; "Try the v1 demo" runs in the browser after about 57 MB | 1 / 1 |
| 2 | Released and research versions | v1 is released and runs in the demo; v3 (weather features) is the latest research, "Adopted in research · not in the demo" | 1 / 1 |
| 3 | What improved, against what, how sure | v3 adds wind and solar forecasts to v2; on the same past hours it misses the price by less and draws better ranges. A clear but moderate step. Fairly sure on past data, but chosen after seeing it, less certain in the 2022 crisis, untested on future data | 2 (detail 5) / 2 (detail 8) |
| 4 | A rejected idea | Recalibrating v1's bands without changing the model improved coverage too little | 2 / 3 |
| 5 | A remaining uncertainty | Performance on future data; the separate effect of each weather input | 2 / 2 |
| 6 | Evidence for one claim | "View source values" → `uncertainty.csv#L12` at `evidence/cp-20`; "Read the review" → the CP-20 Integration review | 5 / 8 |

**The two understanding checks the audit added.**

- **Score or difference:** −0.0783 was read as a difference, v3 − v2, with negative favouring v3, both
  on the page ("Difference, v3 − v2", consistent with 0.5658 − 0.6441) and in the README ("Negative
  values favour v3"). Correct in both places.
- **Prediction interval or confidence interval:** both were defined correctly. The reader was
  briefly misled where the v3 chapter moved from "95% confidence intervals remain below zero" to
  "the intervals are narrower … 95% coverage" without naming them, and by "point-error interval" in
  the v2 chart note.

**Research progress against the released product.** No real confusion. "Demo v1 · Released
model" and "The released demo continues to run v1" read as intended.

## Changed in response (`126abea`)

| Finding | Change |
|---|---|
| "The intervals are narrower" after a sentence about confidence intervals | "the prediction intervals are narrower" |
| "point-error interval" in the v2 chart note | "point-error confidence interval" (desktop and phone) |
| Checkpoint codes (CP-10, CP-15) on the lineage cards | Removed from the cards; they stay in the chapters' detail layer (audit F04) |
| The licence line read "Research only: Weather: derived from…" | The GFS attribution is one sentence naming the v3 research model |

## Checked and left as they are

- **v1 scores 1.0518 but beat the naive on its holdout.** Deliberate. The v1 row says it is v1's
  development replay, the v1 chapter carries the holdout, and the "Definitions" disclosure reconciles
  the two.
- **"link added when the runs are published".** The honest state until F1 (audit F10).
- **The full endpoint twice (chart note and interpretation), p = 1.98e-18, and the exact v1 label
  beside its badge.** Required by invariants 9 and 24 and by the v1 label rule (audit §4; F06).
- **"Explore this forecast" might be broken, and links without text.** `check_reader_paths.py route`
  shows the link opens the archive at the replay. The textless links are inside the closed archive,
  where the text extractor sees nothing.
- **The sticky header over headings in the screenshots.** A capture artifact; anchored headings keep
  their scroll margin (`test_sticky_header_never_covers_anchored_headings`).
- **"trained champion" in the licence sentence.** v1's own licensing text, outside the brief's
  `claims.py` allowlist; not changed.
