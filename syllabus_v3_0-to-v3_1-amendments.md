# syllabus_v3_0 → v3_1 — Amendment Sheet

*Authored 2026-07-12 by the orchestrator. Merges the ratified expansion into the syllabus: the gap-analysis staged additions (optimization block, classification arc, riders, LO3/LO2 partial reopens), the spectral-EDA row (aligning with `capstone_V6_2.md` §4.2), and the interview-algorithms supplementary block. Adds the stage-gated pointer to the companion Binary Classification Mini-Capstone.*

**Unlike the capstone sheet, this one is NOT purely additive.** Three classes of reword are required and are flagged inline: (a) the Month-2 **FFT/spectrograms row is replaced** (its "not used in the lean capstone" claim is false under v6.2); (b) **C4-1 is superseded** by CLS-1 (one subsection rewritten + a global read-rule); (c) **operative capstone references update** `capstone_V6_1.md` v6.1 → `capstone_V6_2.md` v6.2 (the standard alignment-release pattern, same as v3.0 did for the market conversion — historical delta paragraphs keep their old references). Everything else is additive.

**How to apply (either path):**
- **Manual:** open `syllabus_v3_0.md`, apply AMD-1…AMD-11 at the stated anchors, save as `syllabus_v3_1.md`.
- **B-Claude (~15 min):** brief Claude Code: "Apply `syllabus_v3_0-to-v3_1-amendments.md` to `syllabus_v3_0.md` verbatim; output `syllabus_v3_1.md`; diff review confirming only the flagged rewords changed beyond insertions."


---

## AMD-1 — Header: title, version delta, pace decision, global reference update

**(a) Title line.** Anchor: `# Accelerated DS Syllabus — v3.0 — for capstone_V6_1.md v6.1 (German DE-LU Lean DS Capstone with Cloud-Backed Showcase)`
→ change to: `# Accelerated DS Syllabus — v3.1 — for capstone_V6_2.md v6.2 (German DE-LU Lean DS Capstone with Cloud-Backed Showcase)`

**(b) Global reference update (reword class c).** In all **operative** rows/paragraphs, `capstone_V6_1.md` v6.1 → `capstone_V6_2.md` v6.2. Do NOT touch the historical delta paragraphs (v2→v2.1 … v2.3→v3.0), which correctly cite the versions of their time.

**(c) Pace paragraph.** Anchor: the header paragraph ending "…Cuts come from the KILL and COMPRESS lists, not from KEEP-authoring depth." Append:

> **(v3.1 pace amendment, 2026-07-12):** v3.1 is an **expansion release**, adopted under an explicit owner decision to optimize hire probability over the calendar envelope. Net new load ≈ 90–95h inside Months 0–5 (per-month math in the stage map's load appendix): Months 2–4 each run ~5–5.5 weeks at the 20–22h/week budget (or the budget rises to ~26–27h/week to hold 4-week months); the flagship envelope (G5) slides from ~mid-Dec to ~mid/late-January 2027. **Two anchors do not move:** active applications still begin at the start of program-Month 5 (in-market before the envelope closes), and the interview-algorithms block closes at the Month-4 gate, before applications. The post-envelope companion arc (fraud mini-capstone, ~92h, Months 6–7) is scheduled by the stage map, not this syllabus — see the pointer section added at the end (AMD-11).

**(d) New delta paragraph.** Anchor: immediately after the "**v2.3 → v3.0 delta (market conversion).**" paragraph. Insert:

> **v3.0 → v3.1 delta (expansion release, 2026-07-12).** Adopts the four-course gap-analysis (6.006 / 18.065 / 6.341x / CS229 audited against this syllabus), the spectral-extension spec v1.0, and the algorithms-block spec v1.0; aligns with `capstone_V6_2.md` v6.2. *Added:* Month-0 PCA upgrade to [APPLIED-AUTH] (**LO3 partially reopened** — PCA only, on interview-frequency evidence; the full [AUTH]+Eckart–Young upgrade **remains rejected**); a Month-1 18.065 matrix rider [REC, ~4h]; a **Month 1→2 seam optimization section** [AUTH, ~10h: 18.065 L21–23, L25] with NN/backprop + optional Fourier riders around the CNN; the Month-2 **spectral-EDA row** [APPLIED-AUTH, 6–10h] replacing the obsolete FFT/spectrograms row (capstone v6.2 §4.2 — the "not used in the lean capstone" claim is retired); the **CLS-1/CLS-2 classification arc** in Month 3 (CLS-1 [AUTH, ~12h] supersedes C4-1; CLS-2 [~8h]: bias-variance [AUTH], SVM/kernels [REC], ERM [REC]); the **ALG interview-algorithms supplementary block** [APPLIED-AUTH, ~48h staggered Months 2–4, NeetCode-driven, 6.006 as backbone]; Month-4 **UNSUP** (~7h: k-means [APPLIED-AUTH], EM/GMM [REC]), **CAUS** (~6h — **LO2 reopened in light form**; the capstone's no-causal-claim boundary is untouched), and the **ERR rider** (CS229 L13 error analysis [APPLIED-AUTH], ~3h on the M3 diagnostics); three spectral interview Q&As in Month 5. *Absorption notes:* CS229 L8 (splits/CV) absorbs into the Month-2 walk-forward row; CS229 L10 (trees/ensembles) was already this syllabus's cited source; CS229 L11–12 are duplicates of the 18.065 L26–27 rider (skip). *Standing rejections:* SC3-learn and SC5-learn carry forward unchanged. *Pointer added:* post-envelope companion arc (Binary Classification Mini-Capstone) — pointer only, stage-gated.

---

## AMD-2 — Month 0: PCA upgrade (LO3 partial reopen)

**Anchor:** the Month-0 table row beginning `| SVD as generalization of eigendecomposition; PCA as SVD on centered data matrix; variance-explained interpretation | [REC] | …`

**Action:** change that row's depth cell from `[REC]` to `**[APPLIED-AUTH] (PCA; v3.1 LO3 partial reopen)** — SVD framing and Eckart–Young remain [REC]`, and append to its resource cell: `; CS229 PCA lecture + 18.065 L6 for the applied upgrade (~2–3h incremental)`. The condition-number row is unchanged.

**Timing note (append under the Month-0 table):**

> **v3.1 timing note:** if L5 has already been briefed or closed at [REC] by the time v3.1 is adopted, the PCA upgrade does not reopen Month 0 — it runs as a ~2–3h Month-1 rider alongside L-MTX (below). Either way the deliverable standard is the [APPLIED-AUTH] one: explain variance-explained, when/why to use PCA, and its limits, cold, in interview.

---

## AMD-3 — Month 1: the 18.065 matrix rider (L-MTX)

**Anchor:** Month 1, the "**Parallel blocks this month:**" bullet list, immediately after the "**A/B testing / experimentation** [REC] (~4h, v2.3 C4)…" bullet. Insert a new bullet:

> - **18.065 matrix riders** [REC] (~4h, v3.1 L-MTX) — parallel filler: L5 positive-definite/PSD and covariance intuition; L8 vector/matrix norms and the L1/L2 ↔ regularization link; L9 the four ways to solve least squares (feeds the Month-3 Ridge baseline directly); L10 condition-number difficulties with Ax=b (extends the Month-0 collinearity answer). Recognition depth only — no derivations authored.

---

## AMD-4 — New seam section: First-Principles Optimization (L-OPT) + CNN riders

**Anchor:** insert a new section between the end of Month 1 (after its "**Coding deliverables:**" list and the closing `---`) and the heading `## Month 2 — Time-Series, Cross-Validation, and Tree-Based ML — Capstone M1 Interleaves Here`.

**Insert (verbatim):**

> ## Month 1→2 Seam — First-Principles Optimization (v3.1)
>
> **Time:** ~10h (L-OPT) + the existing 16h-capped CNN build + ~5h of riders; the seam widens from ~1 week to ~2 weeks.
> **Goal:** Close the program's first-principles optimization gap **before** the CNN build — gradient descent, momentum, and SGD are directly tested in Israeli DS interviews and underpin both the deep-learning surface and the "gradient boosting = functional gradient descent" framing that carries the Month-3 LightGBM defense.
>
> | Sub-topic | Depth | Resource | Capstone link |
> |---|---|---|---|
> | Minimizing a function step by step; gradient descent geometry, learning rate, convergence intuition | [AUTH] | 18.065 L21–L22 (Strang) | LightGBM fits trees to negative gradients (capstone §6.1) — this is the principle underneath |
> | Momentum / accelerated gradient descent | [AUTH] | 18.065 L23 | Interview surface (optimizer families); feeds the CNN's optimizer choice |
> | Stochastic gradient descent: minibatches, noise-as-feature, why SGD generalizes | [AUTH] | 18.065 L25 | CNN training loop; the "SGD vs Adam" interview answer |
> | Linear regression by gradient descent (unifying view) | [REC] | CS229 L2 — absorbed as reinforcement, not a separate block | Connects to the Month-0 normal-equations work and the Ridge baseline |
>
> **Riders around the CNN build (v3.1 DL+, ~5h total):** immediately before or during the CNN mini-project, (a) **NN structure + backpropagation** [REC] via 18.065 L26–L27 — primary source; CS229 L11–L12 cover the same ground and are skipped as duplicates; understand backprop, don't memorize it; (b) **optional enrichment:** 18.065 L31–L32 (circulant eigenvectors / Fourier matrix; the convolution rule) [REC] — bridges the signal-processing background to the CNN's convolution operation and to the Month-2 spectral-EDA block. The CNN build itself is unchanged: same 16h hard cap, same scope red line, same routing (see the DL block in *Supplementary Interview-Readiness Blocks*).

---

## AMD-5 — Month 2: spectral row replaces the FFT row; ALG-1 begins; interleave additions

**(a) Row replacement (reword class a).** Anchor — the Month-2 table row:
`| FFT / spectrograms | [REC] | None new — leverage Yarden's existing signal-processing background | Recognition only; not used in the lean capstone |`

**Replace with:**

> | Spectral EDA of the DE-LU price series: DFT frames and frequency resolution; why the raw periodogram is inconsistent; **Welch's method** (Hann window, averaged modified periodograms, the variance–resolution trade-off); detrend/difference before the periodogram (low-frequency leakage); per-regime spectra as evidence of regime non-stationarity; ACF cross-check; optional MSTL | **[APPLIED-AUTH]** | `scipy.signal.welch` + statsmodels ACF/MSTL; 6.341x U8–U9 selected fragments (~40–50 min theory refresh, inside the block); the existing signal-processing background does the rest | **Capstone v6.2 §4.2** — confirms the 24h/168h/12h seasonal structure behind the calendar/residual-load features and the per-regime spectral change behind the three-regime folds; 6–10h inside M1's window; three CP-1 items + R-5 guardrails per §4.2; one showcase figure earmarked for M4 (§10 item 3b) |

**(b) Parallel-block paragraph.** Anchor — the Month-2 paragraph beginning "**Parallel block (non-capstone):** the **SQL raw-query authoring block** begins…". Append to it:

> **Also this month (v3.1):** the **interview-algorithms block (ALG)** begins its light start — ~2h/week (~8h): Arrays & Hashing + Two Pointers, 6.006 L4 anchor, Python-idioms sub-block, solutions repo + progress log created. Full detail, cadence, downgrade rule, and the capstone-wins conflict rule in the *Supplementary Interview-Readiness Blocks* section.

**(c) Capstone interleave.** Anchor — the interleave bullet "- KFT/LAG leakage audit drafted…". Insert a new bullet after it:

> - **Spectral EDA (v6.2 §4.2)** lands after the bulk pull (it consumes the ingested series) and before the CV-design work it partly justifies: `spectral_eda.py`, three mandatory figures, README interpretation paragraph. R-5 scope guardrails apply (no filters/wavelets/frequency-domain forecasting).

**(d) CP-1 bullet.** Anchor — the bullet "- CP-1 closes M1 (incl. the ENTSO-E↔SMARD reconciliation gate and the CC BY attribution item)." Append to it: "**and the three §4.2 spectral checklist items (v6.2)**."

---

## AMD-6 — Month 3: CLS-1/CLS-2 supersede C4-1; ALG-2 ramps

**(a) Parallel-blocks paragraph (reword class b).** Anchor — the Month-3 paragraph beginning "**Parallel blocks (non-capstone):** the **SQL raw-query authoring block** (begun in Month 2) completes this month…" and ending "…Full detail in the Supplementary section."

**Replace the sentence beginning "**Also this month (v2.3 C4):**…" with:**

> **Also this month (v3.1):** the **classification theory arc** lands — **CLS-1** [AUTH, ~12h; supersedes C4-1, whose 10–12h budget it absorbs] early in the month, **CLS-2** [~8h] mid-month — and **timed take-home rehearsal #1** (~4h box) lands late in the month, consuming CLS-1's output. The **ALG block ramps** (~5h/week, ~20h: Sliding Window, Stack, Binary Search, Heaps/Top-K) as SQL completes and frees its slot. Full detail in the Supplementary section.

**(b) Global read-rule (add as a one-line note at the end of the same paragraph):**

> *(v3.1 supersession: wherever this document or its briefs reference C4-1, read CLS-1.)*

---

## AMD-7 — Month 4: ALG-3 peak, UNSUP, CAUS, ERR rider

**(a) Parallel-blocks line.** Anchor — the Month-4 line "**Parallel blocks (non-capstone, v2.3 C4):** **timed take-home rehearsal #2** (~4h box) and the **first mock interview** land this month — see *Supplementary Interview-Readiness Blocks*." Append:

> **Also this month (v3.1):** the **ALG block peaks and closes** (~5h/week, ~20h: Trees + BFS/DFS on grids/graphs, intro 1-D DP, plus the ≥4 timed 25-min mock solves — nothing bleeds into Month 5); the **UNSUP block** (~7h: k-means [APPLIED-AUTH], EM/GMM [REC]) and the **CAUS block** (~6h, LO2 light reopen — causal-inference frame [REC] + A/B experiment-design deepening [APPLIED-AUTH]) run as parallel filler. Full detail in the Supplementary section.

**(b) Capstone interleave.** Anchor — the Month-4 interleave bullet list (the M3 items: CQR layer, SHAP plots, permutation importance, regime-stratified error table, reliability diagram). Insert one bullet after the regime-stratified-error-table bullet:

> - **ERR rider (v3.1, ~3h):** apply the CS229 L13 error-analysis method [APPLIED-AUTH] to the regime-stratified error table — bucket the largest errors, name the dominant failure mode per regime, estimate the ceiling from fixing each bucket. Becomes a standing diagnostic habit and an interview-ready story.

---

## AMD-8 — Month 5: three spectral interview Q&As

**Anchor:** the Month-5 interview-prep row, inside its long sub-topic cell, immediately after `**"why a thin CI but no regression matrix?"**`. Insert:

> , **"how did you choose your seasonal features?"** (the Welch periodogram answer — 24h/168h/12h peaks, Weron 2014 / Lago et al. 2018 as the literature echo; v6.2 §13), **"how do you know your folds respect the regime changes?"** (change-point detection + per-regime periodograms showing spectral non-stationarity; v6.2 §13), and **"where did your signal-processing background help?"** (Welch-vs-raw-periodogram, windowing, variance–resolution; v6.2 §13)

*(The row's resource cell already updates to v6.2 via AMD-1b.)*

---

## AMD-9 — Supplementary section: ALG block added; C4-1 rewritten as CLS-1; CLS-2, UNSUP, CAUS added; firewall note extended

**(a) New ALG block.** Anchor: insert immediately **after** the end of the "### SQL — Raw-Query Authoring Against a Real DB" subsection (after its coding-deliverable paragraph) and **before** "### DL — Standalone CNN Mini-Project (Outside Capstone Scope)".

**Insert (verbatim):**

> ### ALG — Interview Algorithms (v3.1) [APPLIED-AUTH]
>
> **Goal:** Clear the LeetCode-style algorithmic coding screen used by a large share of Israeli DS employers (Wix: SQL + LeetCode-style Python; Lightricks: LeetCode question + classic data-structures round; Gong: algorithmic problem-solving; Mobileye: algorithms proficiency). The instrument is a **NeetCode 150 subset on high-frequency patterns** with MIT 6.006 as the theory backbone — not full-course consumption, and not competitive programming. DS screens are materially easier than SWE screens: the hard graph/DP tail is deliberately trimmed.
>
> | Pattern | Problems | Hours | 6.006 anchor | Example problems |
> |---|---|---|---|---|
> | Arrays & Hashing | 12 | 11 | L4 | Two Sum; Group Anagrams; Top-K Frequent; Product Except Self |
> | Two Pointers | 6 | 5 | (L3 foundation) | Valid Palindrome; 3Sum; Container With Most Water |
> | Sliding Window | 6 | 6 | — | Buy/Sell Stock; Longest Substring w/o Repeating; Min Window Substring |
> | Stack | 5 | 4 | — | Valid Parentheses; Min Stack; Daily Temperatures |
> | Binary Search | 6 | 6 | L3 | Binary Search; Koko Eating Bananas; Rotated Sorted Array |
> | Heaps / Top-K | 5 | 5 | L8 | Kth Largest; K Closest Points; Task Scheduler |
> | Trees + BFS/DFS (grids & graphs) | 10 | 8 | L9–L10 | Invert Tree; Level-Order; Number of Islands; Clone Graph; Rotting Oranges |
> | Intro DP (1-D) | 6 | 5 | L15–L16 | Climbing Stairs; House Robber; Coin Change; LIS |
> | Python-idioms sub-block (woven in) | — | 2 | — | `Counter`, `defaultdict`, `heapq`, `sorted(key=…)`, comprehensions, `enumerate`/`zip` |
> | **Total** | **~50 target** | **~48h** | | |
>
> **Placement & cadence (staggered — defended):** Month 2 light start (~2h/week, ~8h: patterns 1–2) while SQL is heaviest; Month 3 ramp (~5h/week, ~20h: patterns 3–6) as SQL completes and frees its slot; Month 4 peak (~5h/week, ~20h: patterns 7–8 + mocks). **The block closes at the Month-4 gate — nothing bleeds into Month 5** (applications). Done-conditions: **end Month 2:** ≥12 solved incl. all Arrays/Hashing; **end Month 3:** ≥32 solved through Heaps/Top-K, solutions repo public and pattern-organized; **end Month 4:** ≥50 solved, all patterns, ≥4 timed mocks logged.
>
> **The 6.006 anchors are watched inside the block** as [REC]-style refreshers (a heap primer before Top-K, a BFS/DFS primer before graphs) — never as separate L-blocks; the learning-block sequence stays reserved for the core curriculum.
>
> **Re-solve policy:** any problem failed, or solved only with the solution open, is re-queued and re-solved after 1 week; a pattern is complete only when all its problems pass first-try on the latest attempt. **Tracking:** `progress_log.md` table — Date | Problem | Pattern | Difficulty | First-try? | Time | Re-solve due.
>
> **Month-4 timed-mock protocol:** ≥4 mock solves, each one unseen Medium (or two Easies) in a hard 25-minute box, **talking aloud** (brute force → optimization → complexity), plain editor, no autocomplete/AI. Pass = correct + near-optimal + clear verbal reasoning inside the box. Fails become re-solves.
>
> **Deliverable & signal:** a clean, pattern-organized public solutions repo with 2–3-line approach/complexity notes per solution — a mild profile positive and a spaced-repetition store; the *real* deliverable is screen performance, not repo aesthetics.
>
> **Pre-committed downgrade rule (verbatim):** *If by end of Month 3 the C8 target-list research shows ≥80% of active-funnel companies use a take-home / dataset-assignment format (Riskified/CyberArk-style) rather than a live algorithmic-coding screen, downgrade the remaining Month-4 block from [APPLIED-AUTH] to [REC] maintenance: 1 problem/week, drop the mock protocol to 2 mocks, and reallocate the freed ~15h to the capstone M3–M4 diagnostics and take-home rehearsal.*
>
> **Conflict-resolution rule (verbatim):** *The algorithms block never blocks a capstone milestone (M1–M5) or checkpoint (CP-1–CP-5). In any week where a capstone milestone is at risk or the weekly budget is exceeded, algorithms yields first: skip that week's problems, preserve the re-solve queue, resume the following week. Missed weeks are absorbed by the Month-4 buffer, never by delaying a capstone CP.*
>
> **Anti-goals:** no full 6.006 consumption; no competitive-programming tail (no segment trees, no Dijkstra/Bellman-Ford beyond recognition, no Hard-grinding); no start before Month 2 (Months 0–1 math is the binding constraint); never a portfolio centerpiece.

**(b) C4-1 rewritten as CLS-1 (reword class b).** Anchor: the subsection "**C4-1 — Classification & metrics.**" (its intro paragraph, table, and Placement/Deliverable lines).

**Replace the whole C4-1 subsection with:**

> **CLS-1 — Classification theory arc, part 1 (v3.1; supersedes C4-1).** The biggest structural gap in the program: everything taught is regression/forecasting while most Israeli DS screens probe classification, and the flagship artifact is regression-only. CLS-1 upgrades the old C4-1 from [AUTH-light] metrics coverage to a true [AUTH] theory arc, absorbing C4-1's 10–12h budget into ~12h.
>
> | Sub-topic | Depth | Resource | Link |
> |---|---|---|---|
> | Logistic regression: decision boundary, MLE derivation, regularization | [AUTH] | CS229 L3 | Core interview topic; the interpretable baseline of every classification take-home |
> | Perceptron + GLMs — the exponential-family view unifying linear/logistic/Poisson | [AUTH] | CS229 L4 | Elegant interview material; unifies the Month-0 OLS work with classification |
> | GDA + Naive Bayes; the generative-vs-discriminative distinction | [AUTH] | CS229 L5 | Classic interview question, asked almost verbatim |
> | Metrics surface (absorbed from C4-1): ROC/PR and when each is right, confusion-matrix trade-offs, threshold selection, class imbalance (weights vs resampling vs threshold moving), calibration-curve awareness | [AUTH] | sklearn docs; one focused imbalanced-learning tutorial | Gates the interview funnel; rides the Month-2 tree/boosting intuition |
>
> **Placement & cap:** early Month 3, parallel filler, **~12h**. **Deliverable:** one notebook on a public imbalanced tabular dataset — logistic + LightGBM classifier, a Naive-Bayes-vs-logistic generative/discriminative comparison note, ROC/PR comparison, threshold tuning against a stated cost trade-off, calibration curve. Feeds take-home rehearsal #1 directly. *(Post-envelope, this arc is also the theory prerequisite of the companion classification artifact — see the pointer section; nothing here enters the DE-LU capstone.)*
>
> **CLS-2 — Classification theory arc, part 2 (v3.1).** ~8h, mid/late Month 3, parallel filler: **bias-variance trade-off [AUTH]** (the formal decomposition + the 60-second interview answer — asked constantly); **SVMs: margins + the kernel trick [REC]**; **ERM / generalization frame [REC]** (VC dimension recognition-only). Resources: CS229 L6–L7, L9; ESL selected sections. **Deliverable:** a one-page bias-variance derivation + a kernel one-pager.

**(c) C4-2 pointer.** Anchor: end of the "**C4-2 — A/B testing / experimentation.**" paragraph. Append: "*(v3.1: extended in Month 4 by the CAUS block below.)*"

**(d) New UNSUP + CAUS subsections.** Anchor: insert immediately **after** the C4-4 paragraph and **before** the "**Firewall note**…" paragraph.

**Insert (verbatim):**

> **UNSUP — Unsupervised essentials (v3.1).** ~7h, Month-4 parallel filler: **k-means [APPLIED-AUTH]** — inertia, choosing k, failure modes, when clustering is the wrong tool; it appears in take-homes and screens. **EM/GMM [REC]** — soft assignment, the E/M alternation intuition (CS229 L14); **factor analysis** recognize-only. **Deliverable:** one clustering notebook on the CLS-1 take-home dataset (clusters as EDA, not as the model).
>
> **CAUS — Causal frame + experimentation deepening (v3.1; LO2 reopened in light form).** ~6h, Month-4 parallel filler, extending C4-2: potential-outcomes framing and confounding [REC]; why the capstone deliberately makes **no** causal claim (the §13 boundary, now defensible from first principles rather than by fiat); A/B experiment-design deepening [APPLIED-AUTH] — power/MDE, randomization units, sequential-peeking pitfalls, a CUPED mention. Converts the published clinical-research statistics background (bootstrap-mediation SEM work) into a named interview asset. **Deliverable:** the C4-2 cheat sheet extended to two pages + one fully-designed experiment write-up. *(The "Does NOT Teach" causal boundary is amended, not deleted — see AMD-10.)*

**(e) Firewall note (append one sentence).** Anchor: the paragraph "**Firewall note (mirrors the CNN/SQL reconciliation):** none of the four blocks enters the DE-LU capstone…". Append:

> The v3.1 additions (ALG, CLS-1/2, UNSUP, CAUS) inherit the same firewall: none enters the DE-LU capstone. The one deliberate exception in v3.1 is the **spectral-EDA block**, which is *not* a supplementary block at all — it is capstone scope (v6.2 §4.2) and lives in the Month-2 table.

---

## AMD-10 — "What This Syllabus Does NOT Teach": reopen records

**(a) Opening paragraph.** Anchor: the paragraph ending "…so the boundaries below are re-ratified, not merely inherited." Append:

> **Amended at v3.1 (2026-07-12):** two of the four rejection records are partially reopened on new evidence, per the four-course gap analysis. **LO3 — partially reopened:** PCA rises to [APPLIED-AUTH] on interview-frequency grounds (a targeted reopen justified by the funnel, not by the capstone); the original rejection's substance stands — no [AUTH] SVD arc, Eckart–Young stays [REC]. **LO2 — reopened in light form** as the Month-4 CAUS block, converting the clinical-research background into interview surface; the capstone's no-causal-claim boundary is untouched. **SC3-learn and SC5-learn stand unchanged** (the EnbPI pre-committed reopen condition remains the only path back).

**(b) Causal paragraph.** Anchor: the causal-inference paragraph's closing parenthetical "…Backlog-only.)*". Append immediately after it:

> *(Amended v3.1: LO2 partially reopened as the CAUS interview-surface block — see Supplementary. The boundary in this paragraph is unchanged: the artifact still makes no causal claim, and CAUS makes that boundary defensible from first principles.)*

---

## AMD-11 — End of document: stage-gated companion pointer

**Anchor:** the very end of the document (after the last "Does NOT Teach" paragraph).

**Insert (verbatim):**

> ## Post-Envelope Companion Arc (pointer only — v3.1)
>
> After capstone CP-5 closes and the Month-5 gate passes, a second, standalone Track B artifact begins: the **Binary Classification Mini-Capstone** (IEEE-CIS fraud detection — file: `Binary Classification Mini-Capstone.md` in project knowledge), ~92h across program-Months 6–7, running inside the active application phase. Within *this* syllabus, its learning prerequisites are already complete by the end of Month 4 (CLS-1/2, UNSUP, the metrics-and-calibration surface), so take-homes arriving from Month 5 onward are covered before the artifact itself ships.
>
> **This pointer is deliberately all this syllabus says about it.** No month in this document depends on that plan, and it is **not read, briefed, or consumed before its time** — its execution anchors are the orchestrator instructions and the program-stage-sequence map (rows B-Man3, FM0–FM5, FCP-1–5, G6), which sequence and brief it when its time comes.
