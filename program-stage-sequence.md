# Program Stage Sequence — Capstone-First Routing Map (v8)

**Rebuilt at v6.7 (2026-09-07).** v7 linearized a syllabus-first program in which learning months gated engineering milestones. That contract is retired: **Track A is an optional parallel resource and gates nothing.** This map routes the work that is actually on the critical path, and offers the learning material as a sidecar indexed by the task it helps with.

**Governance (unchanged in kind).** Static by design — no status markers; all position and state live in `progress.md` and only there. Non-anchor — derived from the ratified capstone plan, which wins on any conflict. Planning aid, never authority. Rebuild only on explicit owner request.

**How to use it.** Read `progress.md` → find the row after the last completed stage → read **only** the sources that row's *Briefing sources* column names. That is the read; you do not re-read the anchor end-to-end to write a routine brief.
>>>>>>> claude/v6-7-verify-working-tree-f8ab80

---

## The critical path — three checkpoints

| # | Stage | Executor | Briefing sources | Done when |
|---|---|---|---|---|
| 0 | **PRE-1 — API token** | Yarden (manual) | `README.md` § *Setup* | Before CP-1 is briefed, `ENTSOE_API_TOKEN` is present in the execution environment and one read-only ENTSO-E request succeeds without exposing the value. **Status lives only in `progress.md`; this static map does not claim the prerequisite is currently open or closed.** |
| 1 | **M1 / CP-1 — Data layer and fixed features** | Engineering Lead | capstone §3, §4.0–§4.2, §5.1–§5.2, §9.3–§9.4, §9.6, and the complete CP-1 checklist in §12 | CP-1 returns `PASS` — 10 items, one fresh Integration verdict |
| 2 | **M2 / CP-2 — Model, calibration, analysis** | Engineering Lead | capstone §4.1, §5.1, §6.1–§6.3, §7.1–§7.2, §8.1–§8.4, §9.1, §9.3–§9.4, and the complete CP-2 checklist in §12 | CP-2 returns `PASS` — 10 items, one fresh Integration verdict |
| 3 | **TRIG-C — Track C activation** | Orchestrator | `orchestrator-role.md` § *Track C activation rules* | State flip in `progress.md` after CP-2 lands. Outreach, interview prep, target research and pipeline-building become continuously active. **Nothing gates applications** — Yarden opens them when he chooses |
| 4 | **M3 / CP-3 — Showcase and release** | Engineering Lead | capstone §9.1–§9.3, §9.6, §10, §10.1, and the complete CP-3 checklist in §12 | CP-3 returns `PASS` — 6 items, one fresh Integration verdict |
| 5 | **REL-1 — Publish** | Yarden (manual) | — | Pages live, Space live, MLflow public, `main` landed by hand with both tags. **Owner-only; never delegated** |
| 6 | **C-1 — Portfolio surfaces** | Yarden / C-Claude | `orchestrator-role.md` § *Track C activation rules* | CV and LinkedIn carry the Pages URL as primary. Optional, after release, never a checkpoint item |

**That is the whole critical path.** Every checkpoint closes on its own complete checklist plus one fresh Integration-Critic `PASS`; the disposition and reclamation procedure is `docs/track-b/gauntlet-templates.md` §4 under `AGENTS.md` § *Branch and ref lifecycle*.

---

## Optional learning sidecar

**None of these gate anything.** They are pulled when Yarden wants them, in any order, and never sit between two Track B rows. The syllabus (`syllabus_v3_2.md`) remains the source; NotebookLM remains the teacher. Indexed by the capstone task each one helps with:

| If you want more ground under… | Useful syllabus material | Depth worth taking it to |
|---|---|---|
| the walk-forward design, embargo reasoning, and why post-selection p-values are descriptive | walk-forward CV / leakage-taxonomy block | defend it in interview |
| quantile loss, pinball, and what CQR actually guarantees | conformal prediction / quantile regression material | defend it in interview |
| the Diebold–Mariano construction and Newey–West | time-series inference material | explain the construction |
| the Welch periodogram, windowing and leakage (§4.2) | signal-processing material | already strong — this is the existing background |
| LightGBM's mechanics under the hood | gradient-boosting material | recognize and discuss |
| the SQL window functions in §9.6 | SQL supplementary block (SQL-A/SQL-B) | practice; no deadline |
| algorithms for interview screens | ALG supplementary block | practice; no quota |

**Retired at v6.7:** the G0–G5 month gates, the monthly consolidation verdicts, the SQL-B application gate, the algorithm quotas, the curriculum calendar projections, and the total-program hour envelope. A learning block is now worth running when its value is worth the time, and that judgement is made once, in the moment, by the owner.

---

## Optional future projects

Neither starts automatically. Each requires a **new explicit owner instruction after CP-3**, and each should be re-scoped against the artifact that actually shipped rather than the one that was planned.

| Project | Status | Note |
|---|---|---|
| **Companion — Binary Classification Mini-Capstone** (IEEE-CIS fraud) | optional, not started | Was stage-gated to Months 6–7 behind G5. The automatic launch is retired; the plan document stands if it is ever opened |
| **AWS extension** (`aws-extension-spec_v1_1.md`) | **STALE / NOT SCHEDULED** | The automatic DEC-AWS ballot is retired. Its weekly-refresh, health-report, lookup-grid and outcome-gate premises no longer exist in the plan. If cloud work is wanted, write a new proposal |

---

## Completed history (short, for orientation only)

Program launched 2026-06-09. Month-0 de-risking spike 2026-06-12 (eight probes; `docs/spike-feed-status.md`) established the findings that still bind: A69 initial publication is post-gate; feature feeds are natively PT15M; ENTSO-E↔SMARD agree 96/96 within €0.01; revision metadata is a dead end. Capstone ratified through v6.0 → v6.1 → v6.2 → v6.3 → v6.4 → v6.5 → v6.6 → **v6.7**. M0.5/CP-0 executed, landed (`a911191`), tagged and reclaimed 2026-08-06; **its requirement was cancelled 2026-09-06** and the instrument retired at v6.7. Governance Lockdown ratified 2026-08-08. Early Track A work (L1–L5, Month-0 deliverables) was completed and remains worthwhile on its own terms; it now gates nothing.

*The map is for routing forward work, not for proving that every retired stage still has a home.*
