# PRES-5 — independent post-deployment check (PUBLISH_RULES 1.5 §10.5, A12; §10.3, A6)

**Checker:** a fresh agent that authored none of PRES-5, its fix (O44) or its reviews. Rules: `docs/PUBLISH_RULES.md`
1.5 (`1bc0c523…f94e`), A6, A12, §8–§10; the packet `docs/track-b/evidence/pres-5/publication-packet.md` §8–§9
(`2b67c80c…56a7`). Every observation is anonymous and read-only (curl, urllib, Playwright fresh contexts; no cookie,
token or credential; `MLFLOW_DISABLE_TELEMETRY`/`DO_NOT_TRACK` set). Scratch output in `.local/tmp/pres-5-a12/`.
Findings 1–10 were written before any earlier review or landing record was opened.

**Why A12 applies.** Condition 1: the served page and README changed after the binding review (O44, `eac95cae`,
`50d51507`). Condition 2: the receipt's "Hugging Face direct demo page" row failed in both receipts with no passing retry.

## Identities (2026-11-14, UTC)

| Surface | Intended | Observed | Time | Result |
|---|---|---|---|---|
| GitHub `main` | `50d51507bc2550ab89efba4d2130fe8124ada5d7` | same (`git ls-remote`) | 01:06:16, again 01:17:42 | equal |
| `land/pres-5` / `evidence/pres-5` | `8bcfc454…6e3` / `511e91e3…889` | same (lightweight tags) | 01:06:16 | equal |
| Pages report | `983a75c4…9475`, 1,848,955 B | same; `last-modified` 2026-11-13 22:56:26 GMT, `x-cache: MISS` | 01:06:25, again 01:17:42 | equal raw; no host injection |
| README (raw `main`) | `bc98e9cc…c472`, 59,830 B | same | 01:06:26, again 01:17:42 | equal raw |
| Space (API) | revision `ec97c54fa4b3cafad9d2faa1178da4be7d57ad38` | same; static, RUNNING, public, lastModified 2026-11-13T19:55:47Z | 01:08:14, again 01:17:42 | equal |
| Space `index.html` | `7b962a0f…9553`, 2,427 B (`pub-3/space/index.html`) | raw `e9f37753…b9da`, 2,922 B → normalized `7b962a0f…9553`, 2,427 B | 01:08:28 | equal after normalization |
| Space `history/index.html` | `fcb0ed13…6a8e`, 85,405 B (`pub-3/space/history/index.html`) | raw `eca0481d…af35`, 85,900 B → normalized `fcb0ed13…6a8e` | 01:08:28 | equal after normalization |
| Space card `README.md` @ `ec97c54f` | `263b7bef…21fd` (pub-3) | same | 01:10:31 | equal |
| Public MLflow `delu-generations` (id 1) | committed export, 105 runs | 105 active runs, all equal (finding 7) | 01:11:57 | equal |

Distinct SHAs: reviewed final candidate `300926de` (page `2fc5bd0a…b28b`, README `eb76fabf…8cc8`, identical at
`evidence/pres-5` and `land/pres-5`); landing `8bcfc454` (parent `0be84bdd`, CP-18c's closure: main had moved); O43
merge repair `d1061484`; O44 `eac95cae` + `50d51507` (deployed). Space: CP-18c's publication `ec97c54f`.

## Findings (formed before reading earlier reviews)

**No existing-rule violation was established.** Each finding is an observation with its evidence.

1. **Served page differs from the reviewed page only in the O44 link targets.** A line-then-character diff of the
   served bytes against `300926de:docs/index.html` gives exactly three insertions of `index.html`. They are in the
   `href` of the three links to v1's historical demo (lines 465, 640, 643), and add 30 bytes. Link texts, structure
   and everything else are byte-identical.
2. **The served README differs only in the O44 link targets.** The same diff against `300926de:README.md` gives three
   insertions of `index.html` (lines 19, 446, 454) and 30 bytes. Nothing else changed.
3. **No link sends a reader off the site it names.** At 01:07:03–01:07:52 I checked every distinct absolute link on
   both surfaces without following redirects: 59 links, after excluding the SVG namespace and README's
   `127.0.0.1:8820` command example.
   - 57 answered 200, among them the Space page and `…static.hf.space/history/index.html` (text/html, 85,900 B). Two
     redirected within their own origin: `….mlflow` → `….mlflow/` (301), `…static.hf.space/` → `/index.html` (302).
   - The retired target `…/history/` still answers 302 → `https://huggingface.co/history` (01:07:58), and `…/history`
     404. Neither appears on either surface: all six history references are `history/index.html`, and no prose names
     the bare route.
   - README's 27 relative links all exist at `50d51507`, and the page's 71 internal anchors all have targets.
4. **The Space serves CP-18c's reviewed bundle; `normalized` removes exactly the host's injection.** I ran
   `src/cp18/publish.py::normalized` (PYTHONPATH=src, project venv) on the fetched bytes.
   - It removed 495 bytes from each page: the `window.huggingface` creator script and one og/twitter meta run.
   - Both pages then equal pub-3 byte for byte.
   - At `ec97c54f` all 859 tree files match pub-3 (git-blob SHA-1 or LFS SHA-256), none missing or extra; the five
     served `app/` files are byte-equal. Limitation: I did not fetch all 859 from the static host.
   - The receipt's failed row (normalized `40f3ce65…`) is its normalizer's gap (it keeps the meta run), not a product
     difference.
5. **v1's historical demo is served on the Space's own origin.** The served history page equals `index.html` at Space
   revision `0331088725fe…` (PRES-4's v1 bundle) after normalization.
   - Its 181 relative assets: 171 answer 200 on the origin. Ten binaries (fonts, two PNGs, the favicon) 302 to
     `us.aws.cdn.hf.co`, Hugging Face's own file storage. These are sub-resources, not reader links.
   - In Chromium 153, from a cold start, it rendered "DE-LU day-ahead price forecast · v1 … Historical out-of-sample
     replay … Verdict bitwise identical" in 46.5 s (01:14:19–01:15:05). There were no failed requests and no page
     errors.
6. **The report's claims about the Space are true.** The report says the Space runs "v6 · DDNN-2 alone", "final
   candidate · pending 4.7T", "prospective evaluation in progress", has Explainability, Features and Reliability views,
   and keeps v1 as the historical demo.
   - The Space root's title is "v6 · DDNN-2 alone · final candidate · pending 4.7T" in both engines, and its body
     shows all three strings.
   - `claims.json` carries these values (`live_product_name`, `live_product_status`, `live_prospective_label`); in
     `live-record.json` every issued day has `policy: A1` under the label "prospective evaluation in progress".
   - `main.js` renders Forecast, Explainability, Features, Reliability and History (link `history/index.html`). The
     Space card is titled "v6 · DDNN-2 alone" and embeds `…static.hf.space/index.html` at `ec97c54f`.
7. **The public MLflow equals the committed export.** I ran my own anonymous REST comparison against
   `reports/presentation/mlflow-export/*.json`, without the project's verifier.
   - Each of the 105 run keys maps to exactly one server run, with the run ID in
     `pres-5-fix-1-postdeploy-mlflow-mirror.json`. Names, parameters, export tags, metric keys, latest value and
     step, and parent IDs are equal; no extra runs.
   - The experiment description names all ten parents (`cp26`, `cp28` included); every run ID in the page's ten
     comparison links exists.
   - Rendered in Chrome 157.0.8103.51 and WebKit 26.6 (01:16:47–01:17:14): `experiment`, `compare:v6` and
     `compare:overview` passed, each comparison with 3 plots, 0 skeletons and no API errors.
   - Limitation: I did not re-fetch the full metric histories (17,003 points); the mirror record covers them.
8. **The red line holds.** The served page has 58 ISO dates after 2026-09-06 (18 distinct). Every one is a label:
   - decision, rule, freeze, evidence and measurement dates;
   - 4.7T's registered window, 2026-09-07 to 2026-12-05, opening no earlier than 2026-12-04.

   No market number for a delivery day after 2026-09-06 appears. The only delivery-day chart is 2026-04-07, and the
   every-day panel ends 2026-09-06. Finding 1 also confirms that nothing else on the page changed.
9. **The report makes no runtime requests.** Playwright Chromium 153 and WebKit 26.6 at 1440×900 (01:13:01–01:14:07):
   status 200, no failed request, no request beyond the page itself.
10. **CI observations.** `invariant-tests` passed at `50d51507` (run 43523243887) and at `d1061484`, and Pages
    deployments succeeded.
    - The `land/pres-5` tag push ran `invariant-tests` on `8bcfc454` (run 43515781376, 22:01:34Z): failed at
      `uv run pytest -q`; logs need sign-in. Of PRES-5's 75 paths at the landing, only `tests/test_24_…` differs from
      the evidence tip (it also carries CP-18c's 48 lines). Test files, not served surfaces: they do not decide this check.

### First failures and retries seen (from the records; none hidden by a later pass)

- **Receipt 1** (`pres-5-publication-receipt.json`, 22:02:44–22:38:23Z, landing `d1061484`), status FAIL:
  - Direct demo failed three times (22:02:47, 22:03:18, 22:03:48), normalized `40f3ce65…` ≠ `7b962a0f…`.
  - MLflow returned HTTP 500 at 22:03:49 and 22:15:25, then passed at 22:19:10 (105/105).
  - Links "passed" at 22:37:44 while recording `…/history/` → `https://huggingface.co/History` as a 200: a false pass,
    repaired by O44.
- **Receipt fix-1** (22:56:57–23:16:48Z, landing `50d51507`), status FAIL:
  - Pages, main, Space files (859), MLflow (22:58:00) and links (23:16:15; no final URL on another host) passed.
  - Direct demo failed again three times (22:56:59, 22:57:30, 22:58:00) with the same normalizer gap. Finding 4 is
    its targeted check.
- **My own runs:** the first Playwright launch failed because the chromium headless shell is not installed. I reran
  with the full Chromium build; that was a test-environment limit, not a product failure. No other failure.

### §9 matrix rows applied

| Check | This check | Result |
|---|---|---|
| Engines | Playwright Chromium 153.0.8010.12; Google Chrome 157.0.8103.51 (channel chrome); Playwright WebKit 26.6 | recorded |
| Widths / layout / zoom / a11y tree / keyboard / touch / contrast / chart meaning | Not re-run by me: only three `href` values changed (§10.1 byte identity). The Orchestrator's `pres-5-public-report.json` (01:13:34Z, Chrome 157 / WebKit 26.6, 1440–320 and emulated iPhone 15) has 0 problems, 0 HTTP errors and 0 contrast failures, and passes the keyboard check (162 stops) | carried + record |
| Demo | Fresh anonymous visits to the live root and `history/index.html` in both engines; v1's identity check computed in Chromium. Failure/retry states not exercised (CP-18c's) | pass |
| Requests and links | Findings 3 and 9 | pass |
| MLflow | Finding 7. The Orchestrator's `pres-5-public-mlflow-routes-postdeploy.json` (01:15:37Z) passes all 11 routes in both engines | pass |
| Real Safari, iPhone, screen reader | not used | — |

### Recommendations (not violations)

- **R1.** The link checker counts a followed redirect's 200 as a pass even when `final_url` is on another host. Fail
  when the final origin differs from the named one.
- **R2.** Give the receipt's direct-demo row `cp18.publish.normalized`, so the row stops failing on every run.
- **R3 (CP-18c's surface).** Both observations below concern CP-18c's surface:
  - The host also injects `og:title "v6 · DDNN-2 alone"` into v1's history page.
  - `claims.json` keeps an unrendered, stale `live_product_designation` ("v1 remains the product until CP-19").
- **R4 (CP-18c's surface).** "Runs … daily" describes the schedule. The live record at `ec97c54f` issued 4 of 12 live
  days (11-06, 11-07, 11-08, 11-14). Each of the other 8 is published with its cause: inputs on 7, no run on 11-09.

No rule amendment is proposed.

## Comparison with earlier records (read only after findings 1–10 and R1–R4 above were written)

I read `integration.md` (binding, `300926de`), reviews 1–4 (searched for the history route, the Space and A12) and
`docs/track-b/pres-5-landing-2026-11-14.md` (uncommitted; its A12 section is a placeholder).

- **Agreement.** The landing record's identities, the O44 exposure (22:02–22:56Z), the false link pass, the receipt's
  normalizer gap, the CI results (`land/pres-5` red on the test that O43 repairs) and the shared `tests/test_24` all
  match my findings 1–4, 9 and 10. Its follow-ups match my R1 and R2.
- **Not covered before deployment.** Reviews 1–4 passed "v1's historical demo at `/history/`" on local content only.
  None saw the host's redirect. Review 4's O-2 (Space name "v6 · DDNN-2 alone") is confirmed by finding 6.
- **Differences, both minor:**
  - The landing record says "five links" name `history/index.html`. I count six: three on the page and three in the
    README.
  - Its item 8 says the Space shows the designation sentence. `main.js` does not reference
    `live_product_designation`. I did not trace when `live_fresh_test_wording` ("A1 was frozen…") is displayed.

Verdict: PASS
