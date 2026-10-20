# CP-26 search and interval startup support — before fits or scoring

The existing v21-r13 §24.7 search schedule cannot form ensembles for k=0 or k=1.
This is an input-support result, not a model score. The exact count-only evidence is
`reports/rebaseline/search-support.json`; the guarded reproduction script is
`scripts/cp26_search_support.py`. The reference seeds in that evidence are explicitly illustrative
CP-24 seeds, not registered CP-26 seeds. The impossibility proof considers every possible
held-out-week choice and therefore does not depend on choosing a trial seed.

The landed `cp24.design` requires at least 250 eligible training dates after holding out whole
weeks, and 14 held-out dates. Genuine target support starts on 2019-01-31. Both s4 and MAD
statistics and the inherited feature/target mask enter the support calculation. No missing
weather record accounts for the early exclusion.

| Search | Batches | Oldest batch | Largest possible training support there | Ensemble consequence |
|---|---:|---|---:|---|
| k=0, 2020-01-01 | 6 | 2019-07-17 | 156 | No trial can run all six batches successfully |
| k=1, 2020-07-01 | 11 | 2019-08-28 | 191 | No trial can run all eleven batches successfully |
| k=2, 2020-12-30 | 11 | 2020-02-26 | 331 (minimum 307) | Every batch has enough support for every held-out split |

`cp24.sampler.pooled` and `cp24.search.pooled_metric` rank a failed batch at infinity; ensemble
selection excludes nonfinite all-batch loss. The first two searches therefore cannot supply
the four required distinct configurations. The no-load and GFS-delay variants share this
structural problem. No CP-24 ensemble may replace a CP-26 search ensemble.

No native D2 exists throughout the complete CP-26 warm-up, 2020-01-01 through 2020-12-28,
or on the first scored date, 2020-12-29. Its first potentially viable search serves from
2020-12-30. Search and fit success from that date remains untested.

The prior handoff estimated about 30 scored v5 fallback dates. The strict buffer rule makes
that estimate incorrect. The landed `cp16.residuals.SharedResidualState` permits central-only
warm-up issuance and requires 28 complete released own-error dates before producing H
quantiles. With no warm-up D2, v5 has no native central issuance and an empty H buffer.
On 2020-12-30 even a successful native D2 cannot make v5 issue H quantiles. §24.7 requires
B0 fallback and forbids adding anything to a policy's buffer on fallback or failed days.
Thus the buffer remains empty by induction throughout the scored calendar. The same applies
to the no-load v5 variant and the GFS-delay v5 run. This is a protocol consequence, not an
observed forecast result. No fallback counts or numerical forecast scores are claimed here.

The literal plan still permits a complete failure-accounting experiment. Its control would
always use B0 where that fallback is available, or be missing where B0 also fails. The greater
than 1% disclosure duty would apply. This support finding alone does not invalidate such a
run or constitute an Integration verdict. It does require correcting the handoff's expectation
before committing the full resource spend. The Owner has been asked whether to run that
literal experiment or wait for a ratified correction and a new brief.

A possible narrow correction, requiring Owner ratification, would change the earliest retained
batch start from 2019-07-01 to 2019-12-01 and the asserted counts from B_0=6 to B_0=1,
B_1=7. The existing latest k=0 batch starts 2019-12-04: its possible training support is
244–268, and only 54 of 128 illustrative CP-24 seeds satisfy the minimum. Even that correction
does not promise four successful distinct configurations; fixed CP-26 fit seeds and actual
training must still be verified. No anchor, brief, minimum-row guard or seed was altered.

No fit, forecast, evaluation metric or CP-28 arm was produced by this support audit. All
inputs were local, filtered through the CP-25 boundary guard, and the computation was recorded
under CP-26's cumulative resource monitor.
