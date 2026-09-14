# Lead note — disposition of the CP-2 Integration findings

Written after the binding verdict (`integration.md`, `PASS` on `f3a1b7d7a1bddd50fb53c3b85e19327928fba4f0`)
so the reviewed candidate is not altered by the act of recording the response. It changes no code,
no artifact and no metric.

Three fresh Integration reviews ran, each on its own candidate. Rounds 1 and 2 returned `PASS` and
were nonetheless superseded: I repaired what they found, plus defects I found myself, and produced a
new final candidate each time. That history is retained in `integration-round-1.md` and
`integration-round-2.md`.

| Finding | Round | Disposition |
|---|---|---|
| F1 — the holdout report hardcoded "five completed runs"; MLflow showed eight | 1 | **Fixed** at `380e7a0`, then fixed again at `525fc2d` when round 2 showed the replacement counter also understated itself. No count is kept in the file now; the note names the public MLflow record as authoritative and says why. |
| F2 — the one-shot DM label used a hyphen where the plan uses an em dash, in the README and `holdout_report.json` | 1 | **Fixed** at `380e7a0`. All three surfaces now carry the plan's em dash. |
| F5 — the A69-augmented arm's pooled loss was the one headline number not recomputable from committed artifacts | 1 | **Fixed** at `380e7a0`. Both arms' raw predictions are persisted to `reports/cp2/a69_benchmark_predictions.parquet`; round 3 recomputed the headline from them to 5.5e-16 relative. |
| F3, F4, F6, F7 | 1 | **No action.** F3 and F4 were points where the Critic brief was stricter than the plan's bar. F6 (a stage artifact carrying its parent's code SHA) and F7 (448 of 450 eval days, 456 null-proxy rows) are coherent and already disclosed. |
| Obs 1 — `completed_runs_recorded` read 1 against nine real runs | 2 | **Fixed** at `525fc2d` by deleting the field. A local counter resets whenever a previous report lacked the key, so it could not do the job the hardcoded number failed at either. |
| Obs 2 — the README stated the selected catalog before the two pooled losses | 2 | **Fixed** at `525fc2d`. The README now leads with both unrounded losses and the percentage difference, matching the report. |
| Round 3 — "`docs/cp2-model-report.md` §1 attributes the null-proxy rows to the wrong feed … *a missing A65 hour on 2025-07-09*" | 3 | **Not a defect. Verified as a misreading of the report.** |
| Round 3 — "29.4 MB on disk" is 29.4 MiB (30.8 MB decimal) | 3 | **Accepted, not fixed.** The measurement is right and the label follows the near-universal loose convention. Recorded here for CP-3 rather than spent as a fourth review cycle. |

## The A65/A75 finding, checked rather than accepted

The report does not say A65. At the reviewed SHA, `docs/cp2-model-report.md:54` reads:

> … chiefly a missing **A75** hour on 2025-07-09 that invalidates the following 42 target days …

and `scripts/cp2_report.py:174`, which generates that line, carries the same word. Re-derived from
the committed snapshot:

```
2025-07-09   A65 load_forecast_mw nulls: 0   A75 vre_actual_mw nulls: 1   A69 vre_forecast_mw nulls: 0
whole snapshot   A65 nulls: 194   A75 nulls: 1   A69 nulls: 3
```

A75 is the correct attribution, the report already makes it, and 2025-07-09 carries the only A75
null in the entire snapshot. The Critic's own supporting analysis reaches A75 — it cites
`ingest.py`, plan §4.1 and the `vre_actual_mw.notna()` completeness rule at `features.py:176`, and
concludes the window "is an A75 rule end to end." It then reported the document as saying A65, which
it does not. The reasoning was right and the quotation was wrong.

Recorded rather than silently dismissed, because the finding is the kind that *should* be raised:
A65/A69/A75 separation is the spine of the strict-gate argument, and a reviewer challenging it is
doing its job. Verifying the challenge is doing mine.
