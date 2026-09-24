# PRES-1 reader tasks, D1 specimen (plan §11.4)

**2026-09-25.** Readers are not coached. Each is asked to find the product, name the released and
research versions, explain the main improvement, find a rejected idea, name a remaining uncertainty
and open the evidence for one claim.

| Reader | Status |
|---|---|
| Agent without context (a fresh subagent that saw only the page as a visitor sees it) | Done, below |
| The Owner | To do at Stop 1 |
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
