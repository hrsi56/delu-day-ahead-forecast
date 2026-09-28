# PRES-1: the Owner's decisions in the session

Each entry is an instruction the Owner gave in the PRES-1 Engineering Lead session, with its date.
Approving a plan or a phase is never a public-action instruction (brief §5). Until 2026-09-28 no
public action had been instructed; the one public action PRES-1 now authorizes is F1, below.

| Date | Decision | Scope |
|---|---|---|
| 2026-09-24 | Execute the PRES-1 brief; stop at Stop 1 and Stop 2; public actions only when named | The dispatch |
| 2026-09-25 | D1 returned for a correction round, with an editorial review (SHA-256 `2193d2e5…77b5f5`) | Stop 1 |
| 2026-09-25 | One more D1 correction: "Where it helps most" becomes "Performance during the 2022 price peak" | Stop 1 |
| 2026-09-25 | The review's contribution wording approved; public name "Yarden Viktor Dejorno" for the byline | Stop 1 |
| 2026-09-25 | Device test of 2026-09-24: everything was in order (device and browser not supplied); continue | Stop 1; D1 approved |
| 2026-09-28 | The final editorial audit (SHA-256 `f702d4ee…ffd1d`), with eleven finishing items F01–F11 | The finishing round |
| 2026-09-28 | Allowlist extension: text and layout in `app/wasm_showcase.py` (the demo notebook), with no change to any calculation, policy or locked document; consistency and identity checks required | F07 |
| 2026-09-28 | Commit the D1 review (25 Sep) and the final audit (28 Sep) byte-for-byte into this folder | Evidence |
| 2026-09-28 | Two edits in `src/delu_forecast/claims.py`, outside its brief allowlist: the Space link label loses "no server", and "There is no server to wake." becomes "A Static Space has no server-side process to wake." | F07 |

The two review documents are in this folder, byte-identical to the Owner's files in the main
checkout:

- `presentation-d1-editorial-review-2026-09-25.md` — SHA-256 `2193d2e5245bc1a3dbc70bf719c3265ebd84439a8afd9cf3e02b83b41f77b5f5`
- `presentation-final-editorial-audit-2026-09-28.md` — SHA-256 `f702d4ee43555f1d4f437d21d31c9f8aed3b02a199a39ded50532fb3699ffd1d`

## 2026-09-28: the Publication Standard and the conformance brief

The retired PRES-1 Lead session receives nothing further. The Owner carried the conformance brief
to a new Engineering Lead session, which executes it. Both documents are in this folder,
byte-identical to the ratified files in the main checkout:

- `publication-standard-v1.md` — SHA-256 `01d721c2ba6316ca9a2f707e79da229bef732e91bad22f6ce457fb01e69478cc`
- `pres-1-conformance-brief-2026-09-28.md` — SHA-256 `51dd9b8685ea9feb774bd27a7d1241d7e678182dd93b1820cead686686d1f502`

**The standard's ratification (its §17), 2026-09-28:**

| # | Decision | Outcome |
|---|---|---|
| D1 | Ratify Publication Standard v1, with the locked core of its §13 | Ratified; the core is protected by detection until it enters the Lockdown's locked set |
| D2 | The §15 amendments to plan revision 3: the headline and target line; planned work after the chapters; the endpoint and p-value display; the per-model scope of invariant 5 | Approved |
| D3 | The date boundary: v1's published holdout replay (the opening preview and v1's archive) stays as published; no research generation's number, chart or choice uses data after 2026-04-07 before the final test | Confirmed |
| D4 | The repository root | Withdrawn: the Owner's personal decision, outside the standard |
| D5 | Execution and authority | Approved, with the scope widened to "including everything" in a new Lead session. Authorizes the Lead's F1 public MLflow upload after an independent PASS, and, after the Orchestrator's verification, landing, push and the Space redeploy by the Orchestrator |
| D6 | Extend the 2026-09-24 decision-4 suspension (the MLflow step in the landing templates) to the publication packet | Approved; applied by the Orchestrator in a separate task after PRES-1 lands |
| D7 | A human cold read before publication | Left as an option: an addition, never a gate |

**The Owner's instructions of 2026-09-28:**

| Instruction | Consequence for PRES-1 |
|---|---|
| The Owner runs no tests and no visual checks himself | Final audit F11 (`owner-hand-checks.md`) is not run by the Owner; it is replaced by the automated checks below |
| His final visual approval of PRES-1 (plan §12, F5) is delegated to the Orchestrator | The Orchestrator gives it on the final candidate, in its own screenshots, before landing |
| Real Safari, a real iPhone and VoiceOver are replaced by the automated checks of the standard's §10 | Every release-check record states that none of them was used |
| Rendering, screenshots and visual checks by agents are authorized for PRES-1 (plan §11.3; brief §2) | The Lead and the independent checker render and measure the page |

**The one public action authorized: F1** (standard §17 D5, given through the conformance brief
§7). Upload the committed export to the `delu-generations` experiment on DagsHub, once the brief's
§5 gate holds: one independent PASS on a candidate containing W1–W15, a current export with a
clean dry run, and the §9 credential checks. Nothing else public is authorized to the Lead: no
push, tag, Space redeploy, registry change or write to `delu-cp2`.
