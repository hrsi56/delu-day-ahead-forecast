# Publication advisory log

**Publication Standard v1 §11.** Only a violation of a clause in force, or of a brief's acceptance
criteria, blocks a publication. Every other finding is recorded here. After each publication the
Orchestrator reviews the log and may propose amendments to the Owner (§13); the Owner ratifies each
new version. Entries are appended, never edited; a later entry may close an earlier one.

| Field | Meaning |
|---|---|
| ID | `A-<publication>-<n>` |
| Source | Who found it: the Lead, an independent checker, a cold reader, the Orchestrator |
| Finding | What was observed, with where |
| Why advisory | Why it does not violate a clause in force or the brief's acceptance |
| Proposal | What might change, and who decides |

---

## PRES-1 (the conformance task, 2026-09-28)

| ID | Source | Finding | Why advisory | Proposal |
|---|---|---|---|---|
| A-PRES1-1 | Lead | W2's acceptance asks for an unchanged digest on every export artifact and for changed names, descriptions and tags. `summary.json` and `README.md` carry the run's name (and tags), so their bytes must change when the name does. | Met as the Owner resolved on 2026-09-28: byte identity for every artifact without identity; for the 46 identity-bearing artifacts, restoring the old name and tags reproduces the old SHA-256 exactly (`registry-zero-diff.md`) | Word the next registry-change acceptance as "every artifact digest unchanged, or reproduced exactly by restoring the old identity fields". Orchestrator |
| A-PRES1-2 | Lead | Playwright 1.63's public API exposes no WebKit accessibility tree. The §10 check reads WebKit's own accessibility properties through its inspector protocol (`DOM.getAccessibilityPropertiesForNode`), reached through a private playwright-core API. | The evidence is WebKit's; only the access path is private. A Playwright upgrade may break it, and the check then fails loudly rather than passing | Pin the Playwright tool version in the runbook, or adopt a supported API if one appears. Orchestrator (tooling) |
| A-PRES1-3 | Lead | marimo copies each linked stylesheet into its widgets' shadow roots, where relative font URLs resolve against the page; WebKit asked the Space's root for three fonts. The build now ships all 67 stylesheet targets at the root too (2.0 MB, 67 files). | W12 is met: zero failed requests in both engines. The extra files are copies, not a calculation | Re-check after a marimo upgrade; drop the copies if marimo fixes the resolution. Orchestrator (tooling) |
| A-PRES1-4 | Lead | The comparison's finding sentence ends at about 2,490 px on a 390 × 844 phone, 42 px inside the 2,532 px floor (§1), and at about 1,767 px on desktop, 33 px inside 1,800. The desktop margin is thin because the opening's right-hand column must stay about 460 px wide for the preview's chart text to reach 12 px. | Within the placement | Any copy added to the opening or above the comparison needs a measurement in both engines first (runbook §2, "Limits to watch"); a compaction of the opening is the Owner's design decision. Orchestrator |
| A-PRES1-5 | Lead | The status lint's synonym family flagged "this bundle remains runnable locally" on the container Space card, a statement about the bundle, not a model's status. The word was changed to "runs" under the Owner's focused extension of `build_space.py`. | Satisfied by the change | Keep the lint subject-blind (cheap, and the checker's rubric catches intent); note the pattern in the checker's rubric. Orchestrator |
| A-PRES1-6 | Lead | The container Space card (`space/README.md`) was outside the brief's write allowlist, although the standard's §8 "Space card" rule reaches it. The Owner extended the allowlist on 2026-09-28. | Resolved by the Owner's extension | Future publication briefs name `scripts/build_space.py` with the other surface generators. Orchestrator |
| A-PRES1-7 | Lead | MLflow run names carry the experiment code in parentheses, for example "v3 · weather features (HG)". MLflow views are reader-grade links (§7), and a reader following one meets the codes. | The reading path (§1) is the page and the README's top block; MLflow pages are the deep layer, where codes may appear (§4) | Consider code-free run names with the code as a tag only, before the next upload, since run names become public at upload. Owner (names are fixed before upload) |
| A-PRES1-8 | Lead | Both Space cards' shared body still uses CP-3's word "champion" for v1 (for example the holdout table's "Champion" column). | The standard's §8 card rule covers the model line and links, which come from the registry; "champion" is v1's frozen CP-3 vocabulary and names no status | Align the body with the registry's name in a later card pass. Orchestrator |
