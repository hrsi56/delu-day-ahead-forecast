## The §11.3 checks that need a person (desktop Safari, iPhone Safari, VoiceOver)

Everything else in the §11.3 Report row is measured and recorded in Chrome and in Playwright's
WebKit engine (`release-checks/2026-09-27.json`). These checks need a real Safari, a real iPhone and
a screen reader. That is about ten minutes on each device.

**Open the candidate page:** `.local/worktrees/pres-1/lead/docs/index.html` (on the Mac, double-click
it, or run `open -a Safari` on the path). For the iPhone, AirDrop the file, or serve the folder:
`python3 -m http.server 8000 --bind 0.0.0.0 --directory .local/worktrees/pres-1/lead/docs`, then open
`http://<the Mac's LAN address>:8000/` on the phone.

| # | Check | Desktop Safari | iPhone Safari |
|---|---|---|---|
| 1 | The page never scrolls sideways. On the Mac, also at 200% zoom (⌘+ twice). | ☐ | ☐ |
| 2 | The charts are readable, with no label crossing another. | ☐ | ☐ |
| 3 | "Explore this forecast" opens the v1 report at the replay. The replay redraws to fit; 95% shows 0.9398, and moving the slider off ×1.00 shows the scenario note. | ☐ | ☐ |
| 4 | Keyboard, Mac only: Tab (Option+Tab in Safari) moves through the page in order, with a visible focus ring. Enter opens a "View values" section. | ☐ | — |
| 5 | Tap targets feel comfortable: the evidence links, the "View values" rows and the header links. | — | ☐ |
| 6 | VoiceOver (⌘F5 on the Mac, or Settings → Accessibility on the phone): a closed section is read as collapsed and an opened one as expanded; a chart is announced by its title. | ☐ | ☐ |
| 7 | One figure in the v1 report opens full size on tap or click, and closes. | ☐ | ☐ |

**What to send back:** the device and browser version for each column, and "all pass" or the numbers
that failed. That is recorded as the device test was.
