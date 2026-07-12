# capstone_V6_1 → V6_2 — Amendment Sheet

*Authored 2026-07-12 by the orchestrator. Merges the ratified spectral-analysis extension (spectral-extension-spec v1.0) into the capstone document and adds the single, stage-gated pointer to the companion Binary Classification Mini-Capstone. Apply the eight amendments below in order; each gives an exact anchor from the v6.1 text and the full text to insert. No existing v6.1 text is deleted or reworded anywhere — this is additive only.*

**How to apply (either path):**
- **Manual:** open `capstone_V6_1.md`, apply AMD-1…AMD-8 at the stated anchors, save as `capstone_V6_2.md`.
- **B-Claude (recommended, ~15 min):** the capstone doc is version-controlled on the repo's `main`. Brief Claude Code: "Apply the amendment sheet `capstone_V6_1-to-V6_2-amendments.md` to `capstone_V6_1.md` verbatim; output `capstone_V6_2.md`; commit; confirm the eight amendments and that no other line changed (diff review)."

**After applying — sync all three holders of the doc:** project knowledge, the NotebookLM notebook (version-guard swap per `notebooklm-role.md`), and the repo. The syllabus edit (v3.0 → v3.1) is a separate, deferred task per your instruction.

---

## AMD-1 — Version bump (document header)

**Anchor:** the document's title/version header (the line(s) identifying the document as v6.1, with the v6.0→v6.1 ratification history — §12 M0 reads "This document (v6.1; v6.0 ratified 2026-06-11, spike-adjudicated 2026-06-12)").

**Action:** update the header version to **v6.2** and append this delta line to the version history:

> **v6.1 → v6.2 (2026-07-12):** additive only. Spectral-EDA extension merged per `spectral-extension-spec.md` v1.0 — new §4.2 (Welch periodogram / per-regime spectra / ACF), CP-1 checklist expanded, R-5 added, one showcase section added to the §10 reading order and the M4 scope, three interview Q&As added to §13. One stage-gated pointer to the companion Binary Classification Mini-Capstone added at the end of §12. No v6.1 text removed or reworded; all §0 ratified decisions, boundaries, and rejected-item records carry forward unchanged.

**In §12 "M0 — Plan approved":** after "This document (v6.1; v6.0 ratified 2026-06-11, spike-adjudicated 2026-06-12)" append: "; v6.2 amendments merged 2026-07-12 (spectral extension + companion pointer — additive)".

---

## AMD-2 — New §4.2: Spectral EDA of the DE-LU price series

**Anchor:** end of §4.1. The last sentence of §4.1 is: "`gas_to_load_ratio` stays dead and is not resurrected in any form." Insert the new subsection **immediately after that sentence and immediately before** the heading "## 5. Methodology: Walk-Forward CV and Data Leakage Audit".

**Insert (verbatim):**

> ### 4.2 Spectral EDA (dominant-frequency confirmation) — merged at v6.2
>
> Before committing the calendar/seasonal feature set and the fold scheme, we confirm the series' dominant periodicities empirically. We compute a **Welch power-spectral-density estimate** of the detrended, log-untransformed hourly DE-LU price series (Hann window, 50% overlap, `nperseg` a power of two ≥ 2×168 so the daily and weekly bins are both resolved) and label the peaks at f = 1/24 h⁻¹ (daily), 1/168 h⁻¹ (weekly), and 1/12 h⁻¹ (half-day harmonic). These confirm the calendar features (hour-of-day, day-of-week) and the daily/weekly structure of the residual-load catalog — the same triad the EPF literature documents for European day-ahead prices (Weron 2014; Lago et al. 2018). To show that the spectrum is **non-stationary across regimes** — the empirical basis for the change-point-validated three-regime folds (§5.1) — we compute per-regime Welch periodograms (pre-crisis 2019–2021; crisis 2021–2022; normalization late-2022→) and note the elevated broadband floor and altered seasonal amplitude in the crisis regime (the crisis-era variance and negative-price spikes inflating the floor is a *feature* of the per-regime plot, not a defect to correct). An ACF plot with reference lines at lags 24h and 168h serves as the time-domain cross-check; an MSTL decomposition (periods 24, 168) is optional.
>
> **Implementation:** module `spectral_eda.py` + thin rendering notebook; detrend/difference before the periodogram so low-frequency trend does not swamp the peaks; irregular timestamps/DST are already resolved upstream by the §4.0 UTC discipline. **Committed artifacts (three mandatory, one optional):** `fig_welch_periodogram.png` (labeled 24h/168h/12h peaks), `fig_per_regime_periodogram.png` (three overlaid curves), `fig_acf_24_168.png`, optional `fig_mstl_decomposition.png`. Acceptance: runs end-to-end on the ingested series in <60s on the M3/16GB CPU stack; `annotate_peaks` returns rows within one FFT bin of 1/24 and 1/168 h⁻¹; no dependency beyond scipy/statsmodels/pandas/matplotlib. A 3–4 sentence interpretation paragraph is written into the project README linking peaks → seasonal features and per-regime spectral change → three-regime folds.
>
> **Scope guardrails (defended boundary, same class as §13):** descriptive analysis only. No filter design, no wavelet/EMD work, no forecasting in the frequency domain, no spectral features entering the model catalog at v6.2. The periodogram *justifies* features and folds; it proves no causal claim — the README paragraph says "confirms/justifies," never "proves." Budget 6–10h inside M1's window; overrun escalates per R-5 (§11). Depth [APPLIED-AUTH]: Yarden defends Welch-vs-raw-periodogram, windowing, leakage, and detrending in interview — cheap given the signal-processing background, and the whole strategic point of the extension.

---

## AMD-3 — §10 reading order: the spectral showcase section

**Anchor:** §10 "Artifact and Reading Order", the numbered reading-order list. Item (3) reads: "(3) feature catalog with the residual-load headline highlighted;".

**Action:** insert a new item between (3) and (4), numbered **(3b)** to avoid renumbering the list:

> (3b) **"Why these seasonal features? (spectral view)"** — the labeled Welch periodogram (or the per-regime overlay) with a one-paragraph interpretation: the 24h/168h/12h peaks that justify the calendar and residual-load seasonal structure, and the per-regime spectral change that motivates the three-regime folds. One static figure + one paragraph; **no spectral slider** (a live spectral control would add compute and code surface for zero interview payoff — the §9.2 slider set is unchanged);

---

## AMD-4 — §11 Risk Register: R-5

**Anchor:** end of §11, immediately after the last line of "### R-4 — 15-minute MTU transition" and immediately before the heading "## 12. Milestones and Checkpoints".

**Insert (verbatim):**

> ### R-5 — Spectral-EDA scope creep — added at v6.2
> **Description.** The §4.2 frequency-domain work expands into filter design, wavelets/EMD, or frequency-domain forecasting, consuming capstone time for no hiring payoff. **Mitigations:** the block is capped at the four §4.2 artifacts and the 6–10h budget; wavelet/EMD/frequency-domain-forecasting work is explicitly out of scope (§4.2 guardrails); any new dependency beyond scipy/statsmodels is a scope violation by definition. **Trigger to escalate:** >10h elapsed or any proposed dependency beyond the named set — stop, ship the mandatory three figures as-is, and carry the residual to the orchestrator. **Owner:** learner.

---

## AMD-5 — §12: M1 scope, the build-routing binding list, and the CP-1 checklist

**Three edits inside §12:**

**(a) Build-routing note.** The M1 binding list (the sentence beginning "The M1 brief must carry the v6.1 decisions binding M1: …" and ending "…confirm merge state before building)"). Append one item to the end of that list:

> ; and the **§4.2 spectral-EDA extension** (module, three mandatory figures, acceptance criteria, and the R-5 guardrails) — briefable inside the M1 block or as its own follow-on B-Claude block after the data layer lands, but in either case closing **before CP-1 closes**.

**(b) M1 milestone section.** At the end of the M1 milestone description, append:

> **Spectral EDA (v6.2, §4.2):** lands within M1's window, after ingestion (it consumes the pulled series) and before the CV-design work it partly justifies. Deliverables and acceptance per §4.2; showcase figure earmarked for M4 (§10 item 3b).

**(c) CP-1 checklist.** Append three items to the CP-1 checklist:

> - ☐ `spectral_eda.py` runs end-to-end on the ingested series; ≥3 figures committed (Welch periodogram with labeled 24h/168h/12h peaks; per-regime periodogram overlay; ACF cross-check).
> - ☐ Dominant peaks at 24h and 168h present and annotated; the half-day (12h) harmonic identified.
> - ☐ README interpretation paragraph (3–4 sentences) links peaks → seasonal features and per-regime spectral change → three-regime folds; wording says "confirms/justifies," never "proves."

---

## AMD-6 — §12: M4 scope line (showcase)

**Anchor:** the M4 milestone description in §12 (the local-showcase milestone: marimo end-to-end, champion registered, slider lookup + OOD flags).

**Action:** append one sentence to the M4 scope:

> The showcase includes the §10 item-(3b) spectral section — the labeled periodogram figure + one interpretation paragraph, rendered as a static section with **no slider** (the three-slider set is unchanged).

---

## AMD-7 — §13: three interview Q&As (spectral)

**Anchor:** §13, inside the prepared interview answers (place adjacent to the existing seasonal/collinearity/regime answers — e.g., immediately after the "how did you detect collinearity?" answer or at the end of the answer set).

**Insert (verbatim):**

> **"How did you choose your seasonal features?"** — *"I didn't just assume 24h and weekly cycles — I confirmed them. A Welch periodogram of the detrended price series shows clear peaks at 24h, 168h and a 12h harmonic, which is exactly what the EPF literature reports (Weron 2014; Lago et al. 2018). That's the empirical justification for my hour-of-day, day-of-week and residual-load seasonal features."*
>
> **"How do you know your walk-forward folds respect the regime changes?"** — *"Two ways. Change-point detection with `ruptures` located the 2021–22 crisis onset and the late-2022 normalization boundaries; and per-regime periodograms show the spectrum itself is non-stationary — the seasonal amplitude and the noise floor differ across the three regimes — so a single global fold scheme would leak regime structure. That's why the folds are cut at the change points."*
>
> **"You have a signal-processing background — where did it help here?"** — *"The spectral EDA. I used Welch's method rather than a raw periodogram because the series is long, noisy and non-stationary; averaging modified periodograms with a Hann window trades a little frequency resolution for much lower variance, which is what you want when you're confirming known cycles rather than hunting faint tones."*

---

## AMD-8 — §12 close: stage-gated pointer to the companion Binary Classification Mini-Capstone

**Anchor:** end of §12, immediately after the CP-5 checklist (and before §13).

**Insert (verbatim):**

> ### Post-CP-5 — Companion artifact (pointer only)
>
> After CP-5 closes and the program's Month-5 gate passes, a **second, standalone Track B artifact** begins: the **Binary Classification Mini-Capstone** (IEEE-CIS fraud detection — file: `Binary Classification Mini-Capstone.md` in project knowledge). It is the portfolio's classification counterpart to this project's regression/forecasting arc and reuses this project's toolchain (LightGBM, MLflow/DagsHub, HF Spaces, Docker multi-stage, isotonic calibration, bootstrap CIs).
>
> **This pointer is deliberately all this document says about it.** Nothing in M0–M5 depends on that document, and it is **not read, briefed, or consumed before this point** — its execution anchors are the orchestrator instructions and the program-stage-sequence map (rows B-Man3, FM0–FM5, FCP-1–5, G6), which sequence and brief it when its time comes.

---

## Post-application integrity check (run once, after applying)

1. Exactly eight insertions; `diff` against v6.1 shows **zero deletions and zero reworded lines**.
2. §4.2 sits between §4.1's last sentence and the §5 heading; R-5 sits between R-4 and the §12 heading; the companion pointer sits between CP-5 and §13.
3. The §9.2 slider set, the §0 ratified decisions, the "What this project is NOT" boundaries, and all rejected-item records are untouched.
4. Version header reads v6.2 with the AMD-1 delta line.
5. Sync: repo `main` committed → project knowledge swapped → NotebookLM source swapped (version guard). Ratification anchor update (progress.md naming v6.2) happens at the next session's regeneration.
