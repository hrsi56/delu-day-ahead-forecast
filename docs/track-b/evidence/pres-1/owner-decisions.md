# PRES-1: the Owner's decisions in the session

Each entry is an instruction the Owner gave in the PRES-1 Engineering Lead session, with its date.
Approving a plan or a phase is never a public-action instruction (brief §5). No public action has
been instructed so far.

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
