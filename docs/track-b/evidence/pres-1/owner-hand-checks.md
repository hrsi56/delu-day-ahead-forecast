## The §11.3 checks that need a person (desktop Safari, iPhone Safari, VoiceOver)

Everything else in the §11.3 Report and Demo rows is measured and recorded in Chrome and in
Playwright's WebKit engine (`reports/presentation/release-checks/`). These checks need a real
Safari, a real iPhone and a screen reader. That is about fifteen minutes per device. Chromium and
Playwright's WebKit do not count as Safari on a real device (final audit F11).

**Run them on the final candidate the Lead names.** Record its SHA, and the `index_html_sha256` in
`reports/cp3b/space_wasm_bundle.json` for the demo.

**The report:** open `.local/worktrees/pres-1/lead/docs/index.html` in Safari. For the iPhone, serve
the folder from the Mac:

```bash
python3 -m http.server 8000 --bind 0.0.0.0 --directory .local/worktrees/pres-1/lead/docs
```

Then open `http://<the Mac's LAN address>:8000/` on the phone.

**The demo (local build):** serve the built Space the same way:

```bash
python3 -m http.server 8765 --bind 0.0.0.0 --directory .local/worktrees/pres-1/lead/dist/space-wasm
```

Then open `http://<the Mac's LAN address>:8765/`. If the demo will not start over plain HTTP on the
phone, record that, and run the demo rows again after the Space redeploy (F7).

| # | Check | Desktop Safari | iPhone Safari |
|---|---|---|---|
| R1 | The report never scrolls sideways. On the Mac, also at 200% zoom (⌘+ twice). | ☐ | ☐ |
| R2 | The charts are readable, with no label crossing another. | ☐ | ☐ |
| R3 | "Explore this forecast" opens the v1 report at the replay. The replay redraws to fit; 95% shows 0.9398, and moving the slider off ×1.00 shows the scenario note. | ☐ | ☐ |
| R4 | Keyboard, Mac only: Tab (Option+Tab in Safari) moves through the page in order, with a visible focus ring. Enter opens a "View values" section. | ☐ | — |
| R5 | Tap targets feel comfortable: the evidence links, the "View values" rows and the header links. | — | ☐ |
| R6 | VoiceOver (⌘F5 on the Mac, or Settings → Accessibility on the phone): a closed section is read as collapsed and an opened one as expanded; a chart is announced by its title. | ☐ | ☐ |
| R7 | One figure in the v1 report opens full size on tap or click, and closes. | ☐ | ☐ |
| D1 | The demo shows "Starting the v1 demo" at once, then the forecast; the card closes when it is ready. | ☐ | ☐ |
| D2 | The level control (50/80/95 %) and the load slider both change the forecast. | ☐ | ☐ |
| D3 | The forecast chart is readable on the phone, and the controls stack. | — | ☐ |
| D4 | "View the report" in the loading card opens the report. | ☐ | ☐ |

**What to send back:** the device and browser version for each column, the date, and "all pass" or
the numbers that failed. They are recorded the way the device test of 2026-09-24 was.
