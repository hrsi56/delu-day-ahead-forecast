# PRES-2 — execution baseline record

Recorded 2026-09-29 by the Track B Engineering Lead before any implementation, under the
Owner-delivered PRES-2 brief (`docs/track-b/pres-2-execution-brief-2026-09-29.md`).

## 1. Brief identity and validation

| Item | Value |
|---|---|
| Launch brief, primary checkout (source) | SHA-256 `fa118734a6d82d34bf94836a20452a79aa6d7d9a56f8a5529084be20933ad47e`, 12,524 bytes, untracked |
| Launch brief, candidate copy | SHA-256 `fa118734a6d82d34bf94836a20452a79aa6d7d9a56f8a5529084be20933ad47e`, `cmp` identical |
| Owner-supplied checksum | `fa118734a6d82d34bf94836a20452a79aa6d7d9a56f8a5529084be20933ad47e` — match |

The brief was validated against `engineering-role.md` § *Required brief fields* before any
repository change: one repository, one checkpoint (PRES-2), pinned publication anchor and
execution plan, expected state, observable outcome, complete-bar citation (PUBLISH_RULES in full
plus plan §§1, 3–9), constraints, one timebox (about 32 hours), owner-only actions (none beyond
this exact-copy assembly) and a stop-and-return contract. The exact-copy baseline is the
"explicitly authorized baseline arrangement" that plan §6 P0.1 anticipates. No contradiction
with the plan was found.

## 2. Verified starting state (primary checkout, not modified)

```text
branch main, HEAD 01e394d475202bb44a226f2ac5403aa084dc5b4c (= origin/main)
git status --porcelain=v1:
 M AGENTS.md
 M progress.md
?? docs/PUBLISH_RULES.md
?? docs/track-b/pres-2-execution-brief-2026-09-29.md
?? docs/track-b/publication-postdeploy-independent-review-2026-09-29.md
?? docs/track-b/publish-rules-migration-plan-2026-09-29.md
staged: none
worktrees: the primary checkout only
local branches: main only; no gauntlet/* branch existed
core.hooksPath: .githooks (secret guard active)
```

This matches the brief's expected state; no material mismatch. The primary checkout remains on
`main` with every incoming edit in place. `progress.md` was not copied, opened, diffed or staged.
Disclosure: before the brief was read, one orientation command ran `wc -l` over a file list that
included `progress.md`; it printed only a line count, and no content was read.

## 3. Exact-copy governing baseline

| Path | Pinned SHA-256 | Source | Copy / committed blob |
|---|---|---|---|
| `AGENTS.md` | `ce2760612b19eb8321987c5ff1898946d306cf5f60e376922f87b0a160f1d7c4` | match | match |
| `docs/PUBLISH_RULES.md` (revision 1.0) | `03f106060d9a646ce0c0c986d2f5fb6549929f2ed7270f0c8678fbfd2293b3a3` | match | match |
| `docs/track-b/publish-rules-migration-plan-2026-09-29.md` (revision 1) | `24913b2b947aeef585e5994d61c91fed3c9eb0da830d6366c7f749e689b724c8` | match | match |
| `docs/track-b/publication-postdeploy-independent-review-2026-09-29.md` | `74d33d52b38aa96891d156c512c39d3cbcd7cc3484253d6fdae571b2796252cd` | match | match |
| `docs/track-b/pres-2-execution-brief-2026-09-29.md` | `fa118734a6d82d34bf94836a20452a79aa6d7d9a56f8a5529084be20933ad47e` | match | match |

Files were copied with `cp` and compared with `cmp`; each staged blob was hashed before commit.
No `.gitattributes` exists and `core.autocrlf=input` altered nothing.

- **Baseline commit:** `3702340660bbc1a5e1483ecaa206cd6709eb63a3` on `gauntlet/pres-2`,
  parent `01e394d475202bb44a226f2ac5403aa084dc5b4c`. It adds or replaces only the five paths above.

Incorporated identities already tracked at the base and unmodified:

| Path | SHA-256 |
|---|---|
| `docs/track-b/publication-standard-v1.md` | `01d721c2ba6316ca9a2f707e79da229bef732e91bad22f6ce457fb01e69478cc` |
| `docs/track-b/presentation-and-tracking-plan-2026-09-24.md` (revision 3) | `281193740a256a99a1676d53ef61c9babb5f744a7d0fb038927e305d1149812c` |
| `capstone_v21.md` (v21-r4, read-only research constraints) | `150bd53fa15067b1d138c95d0912f86a1e92ce74092059be09034758c1926167` |
| `docs/track-b/publication-runbook.md` | `462983758193e459642d0043870e256dda2429523b774601d5b32aa9f8630166` |
| `docs/track-b/publication-packet-template.md` | `2976a5f6d563bc7b9e4930da8f673a0a271d93e989d685898aabdb20cbd7a334` |
| `docs/track-b/publication-advisory-log.md` | `d1cb5309e43e3801bf1409016ddbd216279d92c2ed9ec9d48904439a9f59702f` |
| `docs/track-b/pres-1-landing-2026-09-29.md` | `410475d242b827ee7ae138617132575b12f97776472d1b57c9374ac28d725973` |
| `docs/track-b/evidence/pres-1/pres-1-conformance-brief-2026-09-28.md` | `51dd9b8685ea9feb774bd27a7d1241d7e678182dd93b1820cead686686d1f502` |

## 4. Public identity, re-verified read-only

Anonymous HTTPS reads at **2026-09-29T00:15:20Z**:

| Surface | Observation |
|---|---|
| Pages `https://hrsi56.github.io/delu-day-ahead-forecast/` | HTTP 200, 1,560,646 bytes, SHA-256 `d1227c0f64c6a478f6f076e713e2bed2755edf51d0b8f19522c9b978d42fab3d` |
| GitHub `main` (REST) | `01e394d475202bb44a226f2ac5403aa084dc5b4c` |
| HF Space (REST) | revision `59d941825755bf73eabb7ff20e31124fee305755`, sdk `static`, stage `RUNNING` |
| HF Space card (raw) | 16,210 bytes, SHA-256 `6c89e63e7439f69992f43715edf25a5d15f65cadff060d0870ec837d3540680f` = `space-wasm/README.md` at base |

These are identity observations only, not behaviour checks. Raw bytes are retained locally in
`.local/artifacts/pres-2/public-baseline/` (not part of the public proof).

## 5. Topology created by this checkpoint

| Ref / path | Purpose | State at creation |
|---|---|---|
| branch `gauntlet/pres-2` | PRES-2 local candidate and evidence chain | created at `01e394d`, then the baseline commit above |
| worktree `.local/worktrees/pres-2` | isolated Lead checkout; the primary checkout stays on `main` | clean after the baseline commit |

Nothing was staged or committed on `main`, and nothing was pushed, uploaded or deployed.
