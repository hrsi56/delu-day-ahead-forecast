# PRES-1 reader tasks, D1 specimen (plan §11.4)

**2026-09-25.** Readers are not coached. Each is asked to find the product, name the released and
research versions, explain the main improvement, find a rejected idea, name a remaining uncertainty
and open the evidence for one claim.

| Reader | Status |
|---|---|
| Agent without context (a fresh subagent that saw only the page as a visitor sees it) | Done, below |
| The Owner | Done at Stop 1: editorial review of 2026-09-25, which returned D1 for the correction round below |
| Agent without context, round 2 | Done on the corrected page, below |
| A person who does not know the project | Optional, to do |

## Agent reader

**What it was given.** Viewport screenshots of the specimen at 1,440 px (13 screens) and 390 px (26
screens), the visible page text in reading order, and the list of links with their destinations,
all with every disclosure closed. It was told to read screen by screen as a visitor scrolls, to stop
as soon as it could answer, and to open no other file. It cannot measure seconds, so the number of
screens it had seen before answering stands in for time.

| # | Task | Answer (summary) | First found | Screens seen |
|---|---|---|---|---|
| 1 | Find the product | "Try the v1 demo" goes to the Hugging Face Space and runs in the browser (about 57 MB); the static replay chart on the page | 1,440 screen 1 | 1 |
| 2 | Released and research versions | v1 (released LightGBM); v3 (weather features, "Development · post-selection") | 1,440 screen 1 | 1 |
| 3 | The main improvement | v3 adds three weather inputs to v2; against v2 the normalized point error changes by −0.0783 (95% interval −0.1006 to −0.0570) and the interval score by −0.0838, on the same 10,747 hours | Number on screen 1, understood on screen 3 | 3 |
| 4 | A rejected idea | CP-10's recalibration of v1: crisis coverage rose from 19.36% to 32.11%, not enough | 1,440 screen 2 (reason on screen 8) | 2 |
| 5 | A remaining uncertainty | Backtests on known periods only; no fresh-data test or live operation yet | 1,440 screen 2 (explicit on screens 5–6) | 2 |
| 6 | Evidence for one claim | "Source rows" → `reports/weather-ablation/metrics.csv` at `evidence/cp-20`, line 44; "Reviewed result" → the CP-20 Integration verdict | 1,440 screen 3 | 3 |

**Phone check.** Tasks 1 and 2 were answered on the first phone screen, arguably more easily than on
desktop.

**Confusion between research progress and the released product.** Mostly none: "Released demo v1",
"Try the v1 demo" and "v3 does not run in the demo" were clear. Three pulls the other way: "Adopted"
could read as "put into the product"; the opening's research number sat just under the demo block;
and v1's two different scores (worse than the naive on development folds, better on its holdout)
left the reader unsure how good the product is until the Definitions disclosure.

### What was changed in response (before Stop 1)

| Finding | Change |
|---|---|
| "Try thev1demo" in the v1 chapter and "experimentdelu-cp2": spaces lost around inline labels | Quiet links and the primary action no longer use flex layout, so inline spaces survive |
| The opening's number could not be read on its own and could be misread as "7.8% better" | The summary now says what is subtracted from what, what the ratio is to, which sign favours v3, and that it is development evidence, not a test on new data |
| "Adopted" read as "put into the product" | "Adopted in research"; v3's line adds "not in the demo" |
| The crisis window's relation to fold 3 was not stated (−3.18 over the fold against −4.99 in the window) | The Crisis window disclosure now opens with "the 17 days of the 2022 price peak inside fold 3" |
| "Where it does not help" introduced narrower intervals, which read as a gain | "What it gives up": narrower intervals in exchange for slightly lower coverage |
| The struck-through MLflow placeholder looked broken | Shown as muted text: "MLflow comparison (link added when the runs are published)" |
| The demo's purpose was not said, and "no server" sat oddly next to a Hugging Face link | The startup line says the demo replays v1 over its holdout days, what the reader controls, and that the forecast is computed in the browser from a static page |
| "Open the interactive replay" pointed into a collapsed section without saying so | The link says "(in the original v1 report)"; the page's script opens the section |
| "Lineage" in the side rail against "Journey" in the navigation | The rail says "Journey" |
| The long value overlapped a plotted point in the v2 chart | A value too long for the value column moves to its own line under the mark |

### Left for the Owner (not changed)

- **Contribution placement.** The reader would move it up; plan §7.2 places it after Reproduce.
- **A plain-language summary with derived percentages** ("about 12% lower"). Plan §8.1 allows at most one
  saved difference in the opening and no new percentage, so the saved −0.0783 stays.
- **Undefined vocabulary on first reading** (equal-fold, S_MAE, LEAR, CP codes, `NOT_DEMONSTRATED`,
  the work-item numbers). Definitions sit in the "Definitions" disclosure by design (§7.2); whether
  more belongs above the fold is a design decision.
- **The full H−P endpoint looks like a bug to a newcomer.** It is printed in full by invariant 9.
- **The phone header drops the site title** to fit the three navigation links.

## Round 2: after the Owner's editorial review (2026-09-25)

The Owner returned D1 for a correction round (review document
`docs/track-b/presentation-d1-editorial-review-2026-09-25.md` in the main checkout, SHA-256
`2193d2e5245bc1a3dbc70bf719c3265ebd84439a8afd9cf3e02b83b41f77b5f5`, not committed on this branch).
The review asks that the rerun record whether the reader can explain what improved, not merely
locate a number.

**What the new reader was given.** A fresh subagent with no context got the same kind of pack as
before, built from the corrected `docs/index.html` with every disclosure closed: 12 desktop screens
at 1,440 × 900, 19 phone screens at 390 × 844, the visible text and the visible links. It opened no
other file.

| # | Task | Answer (summary) | First found (desktop) | Phone |
|---|---|---|---|---|
| 1 | Find the product | Next-day hourly price forecasts with a range of likely prices; "Try the v1 demo" runs in the browser, about 57 MB | Screen 1 | Screen 1 |
| 2 | Released and research versions | v1 is released and runs in the demo; v3, with weather features, is the latest research and not in the demo | Screen 1 | Screen 1 |
| 3 | Explain what improved | v3 added wind and sun forecasts to v2; both the best-guess price and the ranges got somewhat more accurate than v2's, on the historical periods used to develop and choose the model; not yet tested on new data, and less certain in the 2022 crisis | Screen 2 (headline), screen 5 (certainty) | Screen 2 |
| 4 | A rejected idea | Recalibrating v1's ranges helped a little but not enough, so the model was changed instead | Screen 2 | Screen 3 |
| 5 | A remaining uncertainty | Performance on future data is unknown; the gain cannot be pinned to one weather input | Screen 2 | Screen 2 |
| 6 | Evidence for one claim | "View source values" → `reports/weather-ablation/uncertainty.csv` at `evidence/cp-20`, line 12; or the full CP-20 report | Screen 3 | — |

**Result.** The reader explained the improvement in its own words, with its comparator (v2), its
scope (development, historical periods) and its main qualification (the 2022 crisis fold), without
copying a number. In round 1 the same task needed three screens and was answered with the
normalized difference itself.

**Research progress against the released product.** No confusion. It named "Adopted in research ·
not in the demo" and "The demo continues to run v1" as clear, and noted two weaker nudges.

### Changed in response (round 2)

| Finding | Change |
|---|---|
| Phone lineage: the two experiment cards follow v3, so they read as later than v3 | A label, "Experiments between v1 and v2", heads the branch cards; they have solid outlines, because dashed outlines mean "planned" on this page |
| "less certain in the 2022 crisis fold" next to "Where it helps: in the 2022 crisis window" reads as a mixed message; fold, window and period seem interchangeable | "Where it helps most: in the 2022 price peak, a short window inside the crisis fold, …"; the fair-comparison note now introduces the five historical test periods as "folds" and says the third covers the 2022 crisis |
| "the three-feature bundle" beside a list of four items | The missing-data indicator is a note under the three features, not a fourth item |
| "How it improved, newest first" could suggest the product improved | "How the research improved, newest first" |
| "Space cards" is internal vocabulary | "the demo's description cards" |
| Line spacing jumped around inline links on phones | Links inside running text are inline, with no extra padding |
| The rebuild command was cut off at the right edge on phones | Command blocks wrap on phones; the copied text is unchanged |

### Checked and left as they are

- **The full H−P endpoint and "see below" look like a formatting bug to a newcomer.** Invariant 9
  prints the endpoint in full. The interpretation under the chart says in words that the point-error
  interval "extends slightly above zero" before giving the endpoint, and the chart row points to the
  full value printed under the plot instead of repeating it.
- **"Compare experiment runs (link added when the runs are published)" appears four times** while
  the v1 archive already links its MLflow experiment. The new runs are not published yet (F1
  needs the Owner's explicit instruction), so each evidence row says so; the text goes once F1
  lands.
- **The released v1 scores worse than the naive in the development comparison (1.0518) but beat it
  on its holdout.** Both statements are true and deliberate. The v1 row carries "Development
  replay; its separate holdout results are in the v1 chapter", and the v1 chapter reconciles them
  under "Where it falls short".
- **About 25 links "without text"** are links inside the closed v1 archive, whose text is hidden
  while the archive is closed. The extraction read them as empty; they have text when open.
- **"Explore this forecast" might land on nothing.** A browser check (`check_reader_paths.py
  route`) shows it opens the archive and lands on the replay at 390, 360 and 320 px.
- **The preview label under the sticky header on phone screen 2** is where the screen boundary
  fell in the pack; scrolling shows it.
- **Jargon in deeper sections** (S_MAE, post-selection, "trained champion" in the archived v1
  report). The Owner's review (§5.6) keeps formulas and internal codes in the deeper layers.
