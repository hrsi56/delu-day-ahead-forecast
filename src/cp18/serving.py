"""The live serving rule (the Owner's decision 33, CP-18e): S_13's state serves every live delivery day.

**The schedule.** CP-26's 182-day schedule (`cp26.search.serving_search`) names search S_k for the delivery days from
S_k's day to the day before S_(k+1)'s (§24.7). Its searches S_0 to S_13 are the development record and stay as they are;
`cp26.search` is not edited.

**Decision 33** (the Owner's, recorded beside CP-18e's brief): DDNN-2's searches in operation end at S_13
(2026-07-08). S_14 (182 days later) and every later search are not run, and v6 keeps S_13's state, the one A1's freeze pins
(`cp17.runtime.K13`), for every later delivery day too. The rule is the schedule's search capped at S_13:

| Delivery day | The schedule | The live rule |
|---|---|---|
| before S_14's day | S_k | S_k, unchanged (`min(k, 13) == k`) |
| from S_14's day on | S_14, S_15, ... | S_13 |

So every live day's search state is the pinned S_13, validated as before (`cp26.search.validate_ensemble(..., 13,
'nominal')`, its own member seeds), and nothing re-labels it as another search.

- `LIVE` is the rule every live call site asks (`cp18.pipeline`, `cp18.live.payloads`, `cp18.bundle`).
- `Rule(schedule)` is the same rule over another schedule: the pipeline's injection point for the serving search
  (`cp18.pipeline.run(..., serving=...)`), which CP-18e's rehearsal uses to give a development day to S_14.
- `Rule.record(day)` is the issued record's field for a day the schedule gives to a later search (`serving_rule`); a day
  the schedule gives to S_13 or earlier gets none, so its record is the record of the code before decision 33.
- `refuse_later(k)`: a later search's state never enters the live store (`cp18 search --k 14`, H4's route).

**The rule before decision 33** was the schedule itself. A plain callable passed as `serving` still acts as such a rule
(CP-18a's forced days give 2026-09-02 to S_14 that way, and CP-18e's negative control), so the cause "S_14's state not
in place" stays reachable through that injection only; `LIVE` never names a search after S_13.
"""
from __future__ import annotations

from datetime import date

LAST = 13
DECISION = 33
TEXT = ("S_13's state serves this day: DDNN-2's searches in operation end at S_13, and S_14 and every later search are "
        "not run (the Owner's decision 33)")


class LaterSearchRefused(ValueError):
    """A search after S_13 was offered to the live product (decision 33)."""


def schedule(day: date) -> int | None:
    """CP-26's 182-day schedule, unchanged: the search S_k it names for `day` (None before S_0)."""
    from cp26.search import serving_search
    return serving_search(day)


def search_day(k: int) -> str:
    from cp26.search import search_day as day_of
    return str(day_of(k))


class Rule:
    """Decision 33's serving rule over a schedule (CP-26's by default): the schedule's search, capped at S_13."""

    def __init__(self, scheduled=None):
        self.scheduled = scheduled or schedule

    def __call__(self, day: date) -> int | None:
        k = self.scheduled(day)
        return None if k is None else min(k, LAST)

    def record(self, day: date) -> dict:
        """`{'serving_rule': ...}` for a day the schedule gives to a search after S_13; `{}` otherwise."""
        k = self.scheduled(day)
        if k is None or k <= LAST:
            return {}
        return {'serving_rule': {'search': LAST, 'search_day': search_day(LAST), 'scheduled_search': k,
                                 'scheduled_search_day': search_day(k), 'decision': DECISION, 'text': TEXT}}


LIVE = Rule()


def serving_search(day: date) -> int | None:
    """The live serving search of `day`: `LIVE(day)`."""
    return LIVE(day)


def refuse_later(k: int) -> None:
    """A search after S_13 never serves a live day, so its state never enters the live store."""
    if isinstance(k, int) and k > LAST:
        raise LaterSearchRefused(
            f'search {k} is refused: DDNN-2\'s searches in operation end at S_{LAST} (the Owner\'s decision {DECISION}); '
            f'S_{LAST}\'s pinned state serves every live day')
