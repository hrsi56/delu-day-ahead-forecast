# Capstone v21-r13 → v21-r14 — CP-26 repair candidate

**Authority, 2026-10-13:** the Owner's repair brief manually and temporarily suspends Governance
Lockdown for `capstone_v21.md` and this new amendment sheet, for the named CP-26 repair only.
It authorizes drafting and implementing the contract, local staging/commits on `gauntlet/cp-26`,
preservation, tests and resource reconciliation. It does not ratify the new bytes. r14 remains a
candidate for Owner review/ratification before the experiment resumes. The suspension ends at
the repair's final return. No other governance file, landed code or programme state may change.

**Base:** v21-r13 at `5cc3cc083c4340fd8d792eeaf6551a007987a877:capstone_v21.md`, SHA-256
`173799d818387b9d82db16b9ccd7195afaebbea8e11259809e4a8b704bd525a8`; its ratification commit is
`d58486da826b337bd58f469e122315c3142e360b`. The landed-code comparison base remains
`647d6eb81b2cf6e0cfaf4152f659d689ff973578`.

The normative changed text is in the candidate anchor's heading and §§24.7–24.9, and the exact
before/after is reproducible with `git diff 5cc3cc083c4340fd8d792eeaf6551a007987a877 <anchor_commit>
-- capstone_v21.md` (the noncircular anchor commit is recorded in the repair manifest).

| Location | r13 rule | r14 replacement and source |
|---|---|---|
| Heading | r13 ratified | r14 candidate; preserve historical r13 authority, no premature ratification. Owner brief |
| §24.7 search | Jan1 phase, newest blocks regardless of support, B0=6 | Jan15+182k, newest up to11 support-eligible blocks, extrema across all possible whole-week splits ≥250/14; list signed before fit. Owner contract1; independent audit |
| §24.7 seeds/ensemble | sampler fixed, ensemble four distinct/two seeds | Keep sampler128/space/halving/ranking/ties; separate frozen arithmetic seed domains; effective no-load identity removes id/load flags; exactly8, no resampling/retries/stale ensemble. Owner contract2; routine seed implementation frozen prospectively |
| §24.7 failures | blanket no errors from fallback dates | Valid pre-outcome own central and required scale may warm/recover when H history short; copied fallback remains scored/counts; member/solver/identity/scale/numerical-H failures never intake. Owner contract3 |
| §24.7 policy differences | implicit unchanged recipes | Explicit B0 raw errors/no A1 scale/no self fallback; v1-R nine heads+CQR/embargoes, never H. Owner contract4 |
| §24.7 ledger | generic issuance metadata | Separate score keys, canonical full own-error day and complete3-member learning day; continuous pending/consumed/scales/buffers/caches per route/policy. Owner contract5 |
| §24.7 pilot |14 origins,80% ceiling | Current ruling485/388; total cost includes history+reported+reserves, all42 searches; repair10h/no real search/pilot/replay/scores. Owner resource/stop contract |
| §24.8 | arm H and learning history startup implied | Own historical weights/scale; central warm-up/recovery; separate28 vs364/728; no fixed startup promise. Preserve7 arms,gates,Holm,shared fits,initial weights,selection. Owner contract6 |
| §24.9 | S14=2026-12-23 | S13=2026-07-08,S14=2027-01-06; protocol dates, no future data. Owner contract1 |

**Evidence:** `docs/track-b/evidence/cp-26/repair-v21-r14/independent-audit.txt`, SHA-256
`e53636c68dca3c0a12a6bd8d75c10ecc0ac8b653d648caf20d35aac6605118ba`, is a claim to reproduce,
not an acceptance verdict. Support-only reconstruction must use the actual landed mask/week
algorithm and frozen inputs; expected B=[1,7,11,…,11] and251/46 never replace that algorithm.

**Limits:** §§1–23 are unchanged; so are CP-25 outputs/masks, development boundary, delivery and
scored calendars, issue time, scores/inference, blend/H recipes, ceilings and historical records.
No new model training, real search, pilot, experimental replay or CP-26 score occurs in this repair.
Single winter-block search support does not promise four successful configurations, eight daily
fits, affordable execution or scientific generalization. Recovery buffers may span old calendar
days; the report must disclose their age. CP-28 arms are specified prospectively, not implemented.

The original issued brief and CP-28 protocol remain byte-identical historical documents. New
versioned documents and the active-document manifest record supersession and hashes. The
anchor is committed first; dependent identity pins name that full commit and its SHA-256 only
after it exists. No document contains its own commit/hash as a circular pin.
