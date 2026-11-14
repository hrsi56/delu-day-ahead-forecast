# The Owner's decisions on the live product's daily operation and the page budget — 2026-11-14/15

**Authority.** The Owner, in the session of 2026-11-14/15, after the live product's first runner day and PRES-6's
return. GitHub's scheduler had fired none of the first day's acquisition and run jobs, and fired a later job about 5
hours late; the Orchestrator dispatched the day's jobs by hand. His words, quoted in full and in order:

> בלי מנגנון גיבוי.

> לא צריך מגבלה מצידי...

> אני לא רוצה שיהיו ימים חסרים בגלל זה ולמשימה של גיא האב תמיד ייקח זמן משמעותי לרוץ והיא תפספס
> אם לעשות שאם פספס את נקודת החיתוך זה ירוץ בלי הנתון הזה,
> ולערוך ניסוי לגבי הרצה של המשימה בגיטהאב מוקדם יותר

> אוקי... v6 עם העותק המאוחר

In English:

> No fallback mechanism.

> No limit is needed on my side...

> I don't want days to be missing because of this, and GitHub's job will always take significant time to run and it
> will miss. So make it that if it missed the cutoff, it runs without this input, and run an experiment on running
> the job on GitHub earlier.

> OK... v6 with the late copy.

**Context for the last two.** The day-ahead load forecast is the one input whose availability before D's cutoff
(D−1 11:00 Europe/Berlin) only a retrieval before the cutoff can show: no source keeps its earlier versions, and
Regulation 543/2013 Art. 6(2)(b) requires an update on a significant change (CP-25's tier register: tier 3). Under
decision 22 (r19 §24.13), a live day that cannot show its inputs precede the cutoff is not issued. The Orchestrator
explained that v6 cannot drop an input of its frozen network, so "without it" would mean the frozen chain's last
fallback, the similar-day naive B0, with about twice v6's development error (MAE 34.6 against 17.2 EUR/MWh over
2,068 development days). The alternative was v6 with the load forecast fetched after the cutoff, labelled. He chose
the second.

**Why a new record.** Decision 28 is in `owner-decisions-2026-11-05.md`. This continues the numbering. It was taken
without any 4.7T outcome, since none exists.

29. **No local fallback for the daily operation.** The live product's daily jobs run on GitHub's `macos-26` runner
    only. The Mac's `launchd` fallback (O23) is not installed. When GitHub's scheduler does not start a job, the
    Orchestrator dispatches it by hand.

30. **The report has no page-size limit.** PUBLISH_RULES 1.5 §5.2's "self-contained page budget remains 2.0 MB" and
    §14's size-budget trigger are removed at the next publication round, with the test that enforces them.
    - The one-page, self-contained rule is unchanged.
    - The page's size is still measured and stated.
    - PRES-6 lands as reviewed, within the old budget.

31. **No delivery day goes missing because the acquisition missed the cutoff.**
    - **When D's load forecast cannot be shown to precede D's cutoff,** v6 still issues D, with the load forecast
      retrieved after the cutoff. The day is labelled "load forecast fetched after the cutoff", with that copy's
      retrieval time, on every surface that shows it, and the evaluation reports such days separately from the days
      whose inputs all precede the cutoff.
    - **What this changes in decision 22:** its consequence, "a live day that cannot show it is not issued", for this
      one input only. Every other input is still judged by its publication time against the cutoff, and the frozen
      chain's fallbacks are unchanged.
    - **Nothing frozen changes.** A1 (v6) runs under CP-17c's policy identity `720fc581…`. 4.7T stays exactly as
      registered.
    - **An experiment with an earlier start** on GitHub measures how late the scheduler starts a job at each hour
      before the cutoff. Its result sets when the acquisition starts, so that fewer days need the late copy.
    - **The change is made in a reviewed CP-18 round (CP-18d)** and lands like any other.
