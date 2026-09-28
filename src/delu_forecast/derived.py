"""Typed derived records: the headline quantities of Publication Standard v1 §3.3 (brief W3).

`delu_forecast.research` publishes committed cells exactly as saved. A headline also needs a few
quantities that no single cell holds: whether a policy met the pre-specified targets, how far it
sits from the targets' comparator, how many policies had been tested against the same rule, when
the rule was set, the change against a comparator as a share of the comparator's score, and the
range of absolute errors over the ordinary test periods. Each one is a **typed derived record**
here: a formula over named evidence records, computed with exact decimals from the committed rows,
carrying its inputs, its unit and the claim that maps it. Nothing is fitted, scored or retrieved.

`validate_all()` recomputes every record from a fresh read of the committed files, independent of
the caches, and `tests/test_36_derived_records.py` re-derives the standard's Appendix values and
shows that a perturbed source row fails.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from decimal import ROUND_HALF_EVEN, Decimal
from functools import lru_cache
from pathlib import Path

from . import registry as G
from . import research as R

REPO_ROOT = R.REPO_ROOT

# --------------------------------------------------------------------------- units

#: A relative change in whole percent: the only kind of percentage the reading path may carry
#: besides structural levels and v1's protected statements (standard §3.3, §4).
UNIT_RELATIVE = "relative change, percent"
UNIT_COUNT = "count"
UNIT_LABEL = "label"
UNIT_DATE = "date"
UNIT_EUR = R.UNIT_EUR

#: Where the committed rows of each checkpoint's criteria and scores live.
CRITERIA_FILES = {
    "CP-15": ("cp15", "reports/cp15/criteria.csv"),
    "CP-16": ("cp16", "reports/v2-causal/criteria.csv"),
    "CP-20": ("cp20", "reports/weather-ablation/criteria.csv"),
}
REFERENCE_CODES = ("B0", "B1", "B2", "B3")
FOLDS = ("fold_1", "fold_2", "fold_3", "fold_4", "fold_5")


class DerivedError(ValueError):
    """A derived record no longer follows from its committed inputs."""


@dataclass(frozen=True)
class DerivedRecord:
    record_id: str
    kind: str
    subject: str | None
    unit: str
    value: str
    inputs: tuple[str, ...]
    formula: str
    display_precision: int
    claim: str
    ci_low: str | None = None
    ci_high: str | None = None
    label: str = ""
    sources: tuple[str, ...] = field(default=())

    @property
    def interval(self) -> bool:
        return self.ci_low is not None


# --------------------------------------------------------------------------- the inputs


def _d(record_id: str, which: str = "value") -> Decimal:
    record = R.get(record_id)
    raw = {"value": record.raw, "ci_low": record.ci_low_raw, "ci_high": record.ci_high_raw}[which]
    return Decimal(raw)


def _score_record(experiment: str, code: str, score: str) -> str:
    """The equal-fold score record of a policy in one checkpoint's committed rows."""
    if experiment == "CP-15":
        return f"cp15.relative_scores.{code}.{score}"
    prefix = {"CP-16": "cp16", "CP-20": "cp20"}[experiment]
    return f"{prefix}.metrics.{code}.equal_fold.{score}"


def _criteria_policies(experiment: str) -> tuple[str, ...]:
    prefix, _ = CRITERIA_FILES[experiment]
    found = []
    for record_id, record in R.records().items():
        if record_id.startswith(f"{prefix}.criteria.") and record_id.endswith(".c1.equal_fold.S_MAE"):
            found.append(record.policy_code)
    return tuple(dict.fromkeys(found))


def _strongest_reference(experiment: str, score: str) -> tuple[str, str]:
    """(code, record) of the lowest score among B0–B3: the rule's comparator (capstone §8)."""
    candidates = [(code, _score_record(experiment, code, score)) for code in REFERENCE_CODES]
    candidates = [(code, record_id) for code, record_id in candidates if record_id in R.records()]
    return min(candidates, key=lambda pair: _d(pair[1]))


def _relative(numerator: Decimal, denominator: Decimal) -> Decimal:
    return (numerator / denominator - 1) * 100


def _share(numerator: Decimal, denominator: Decimal) -> Decimal:
    return numerator / denominator * 100


def _text(value: Decimal) -> str:
    return format(value.normalize(), "f")


# --------------------------------------------------------------------------- the rule (§3.3 a)

RULE = G.RULES["criteria-1-2"]
#: The rule's own date, as its anchor states it, and the committed files that establish it.
RULE_DATE_LINE = "**Active owner-authorized execution plan · 2026-09-15.**"
RULE_DATE_SOURCES = ("capstone_v21.md", "reports/cp15/attempt-1/capstone_v21.md")


def section_8(text: str) -> str:
    """Capstone §8, the product-feasibility criteria, as committed."""
    start = text.index("## 8. Product feasibility decision")
    return text[start:text.index("## 9.", start)]


def _rule_date() -> str:
    for path in RULE_DATE_SOURCES:
        if RULE_DATE_LINE not in (REPO_ROOT / path).read_text():
            raise DerivedError(f"{path} no longer dates the rule 2026-09-15")
    anchor, attempt_1 = ((REPO_ROOT / path).read_text() for path in RULE_DATE_SOURCES)
    if section_8(anchor) != section_8(attempt_1):
        raise DerivedError("§8 of the anchor differs from the anchor preserved from attempt 1")
    return re.search(r"(\d{4}-\d{2}-\d{2})", RULE_DATE_LINE).group(1)


# --------------------------------------------------------------------------- the stress period (§3.3 c)

#: The research protocol names the stress period: fold 3, the 2022 crisis (capstone v21 §3 and §7;
#: CP-10's protocol calls it its diagnostic fold). It is read, never assumed.
STRESS_QUOTES = (
    ("capstone_v21.md", "Report fold 3 and August 15–31 with their own dates and denominators"),
    ("capstone_v21.md", "The equal fold weighting is deliberate so a crisis fold is not diluted"),
)


def stress_period() -> str:
    for path, quote in STRESS_QUOTES:
        if quote not in (REPO_ROOT / path).read_text():
            raise DerivedError(f"{path} no longer names the stress period")
    fold = R._json("reports/cp10/protocol.json")["diagnostic_fold"]
    if fold != "fold_3":
        raise DerivedError(f"the protocol's diagnostic fold is {fold}, not fold_3")
    return fold


# --------------------------------------------------------------------------- building the records


def _decision(entry: G.Entry) -> G.StatusEvent:
    """The first evaluated-policy decision, with its dated committed landing provenance."""
    landing = G.CHECKPOINTS[entry.checkpoint].landing
    events = [event for event in entry.statuses if event.source == landing]
    if not events:
        raise DerivedError(f"{entry.id}: no decision tied to {landing}")
    event = min(events, key=lambda item: item.date)
    if event.date not in (REPO_ROOT / landing).read_text().splitlines()[0]:
        raise DerivedError(f"{entry.id}: decision date differs from {landing}")
    return event


def _decision_counts(census: dict[str, tuple[str, bool]]) -> dict[str, tuple[str, str]]:
    """Same-date policies share a boundary; no CSV order breaks a simultaneous result tie."""
    return {
        subject: (
            str(sum(other_date <= date for other_date, _ in census.values())),
            "yes" if met and not any(other != subject and other_met and other_date <= date
                                    for other, (other_date, other_met) in census.items()) else "no",
        ) for subject, (date, met) in census.items()
    }


def _fresh_decision_counts(fresh: R.FreshRead) -> dict[str, tuple[str, str]]:
    """Independent census from hash-checked CSV rows, not cached derived verdicts/counts."""
    census = {}
    for experiment in sorted(CRITERIA_FILES, key=lambda exp: G.CHECKPOINTS[exp].frozen_on):
        _, path = CRITERIA_FILES[experiment]
        rows = fresh.matches(path, {"scope": "equal_fold"})
        for code in sorted({row["policy"] for row in rows}):
            entry = G.by_code(code)
            if entry.id in census:
                continue  # H0 is the already evaluated V2-H, never a ninth policy.
            verdict = []
            for criterion, metric in (("1", "S_MAE"), ("2", "S_WIS")):
                matches = [row for row in rows if row["policy"] == code
                           and row["criterion"] == criterion and row["metric"] == metric]
                if len(matches) != 1:
                    raise DerivedError(f"{experiment}/{code}: expected one row for criterion {criterion}")
                row = matches[0]
                verdict.append(Decimal(row["actual"]) <= Decimal(row["upper_limit"]))
            census[entry.id] = (_decision(entry).date, all(verdict))
    # Recompute directly, without calling the builder's count routine.
    passed_dates = [date for date, passed in census.values() if passed]
    first_date = min(passed_dates) if passed_dates else None
    first_subjects = {subject for subject, (date, passed) in census.items() if passed and date == first_date}
    return {subject: (str(len({other for other, (other_date, _) in census.items() if other_date <= date})),
                      "yes" if first_subjects == {subject} else "no")
            for subject, (date, _) in census.items()}


def _criteria_records() -> list[DerivedRecord]:
    """Per evaluated policy: the verdict on criteria 1–2, its distance from the rule's comparator in
    the rule's unit, N tested up to its decision, and whether it was the first to meet the rule."""
    out: list[DerivedRecord] = []
    date = _rule_date()
    out.append(DerivedRecord(
        "derived.rule.set_on", "rule_date", None, UNIT_DATE, date, (), "the anchor's own date line; §8 equal to "
        "the anchor preserved from attempt 1", 0, "P17", sources=RULE_DATE_SOURCES + RULE.provenance[2:]))
    for score, criterion in (("S_MAE", "c1"), ("S_WIS", "c2")):
        code, reference = _strongest_reference("CP-20", score)
        limit = f"cp20.criteria.HG.{criterion}.equal_fold.{score}.upper_limit"
        margin = -_relative(_d(limit), _d(reference))
        out.append(DerivedRecord(
            f"derived.rule.margin.{score}", "rule_margin", G.by_code(code).id, UNIT_RELATIVE, _text(margin),
            (limit, reference), "(1 − limit / lowest reference score) × 100", 0, "P17",
            label=f"below {G.by_code(code).name}'s score"))
    census: dict[str, tuple[str, bool]] = {}
    count_inputs: list[str] = []
    decision_sources: set[str] = set()
    for experiment in ("CP-15", "CP-16", "CP-20"):
        prefix, _ = CRITERIA_FILES[experiment]
        for code in _criteria_policies(experiment):
            entry = G.by_code(code)
            passed, inputs, distances = [], [], {}
            for score, criterion in (("S_MAE", "c1"), ("S_WIS", "c2")):
                actual = f"{prefix}.criteria.{code}.{criterion}.equal_fold.{score}"
                limit = actual + ".upper_limit"
                scored = _score_record(experiment, code, score)
                ref_code, reference = _strongest_reference(experiment, score)
                if _d(actual) != _d(scored):
                    raise DerivedError(f"{actual} is not the committed score {scored}")
                passed.append(_d(actual) <= _d(limit))
                inputs += [actual, limit, reference, scored]
                distances[score] = (_relative(_d(scored), _d(reference)), (scored, reference), ref_code)
            verdict = "met" if all(passed) else "not met"
            base = f"derived.criteria.{entry.id}"
            if f"{base}.verdict" in {record.record_id for record in out}:
                continue  # one identity, one verdict: CP-20's H0 re-reports v2 (= V2-H) unchanged
            out.append(DerivedRecord(f"{base}.verdict", "verdict", entry.id, UNIT_LABEL, verdict, tuple(inputs),
                                     "actual ≤ upper limit for criterion 1 and criterion 2", 0, "P16",
                                     label="point comparison"))
            for score, (value, pair, ref_code) in distances.items():
                out.append(DerivedRecord(
                    f"{base}.distance.{score}", "distance", entry.id, UNIT_RELATIVE, _text(value), pair,
                    "(policy score / lowest reference score − 1) × 100", 0, "P16",
                    label=f"point comparison with {G.by_code(ref_code).name}"))
            event = _decision(entry)
            census[entry.id] = (event.date, verdict == "met")
            count_inputs.extend(inputs)
            decision_sources.add(event.source)
    counts = _decision_counts(census)
    for subject in sorted(census):
        tested, first = counts[subject]
        base = f"derived.criteria.{subject}"
        for kind, value, formula in (
            ("tested", tested, "distinct evaluated identities with decision date ≤ this policy's decision date"),
            ("first_to_meet", first, "sole policy meeting the rule at the earliest passing decision date"),
        ):
            out.append(DerivedRecord(f"{base}.{kind}", kind, subject,
                                     UNIT_COUNT if kind == "tested" else UNIT_LABEL, value,
                                     tuple(count_inputs), formula, 0, "P16",
                                     sources=tuple(sorted(decision_sources))))
    return out


#: The change against the comparator as a share of the comparator's score (§3.3 b): the committed
#: paired difference and its 95% interval, each divided by the same fixed denominator.
CHANGES = {
    "v3": ("cp20.uncertainty.HG-H0.equal_fold.{metric}", "cp20.metrics.H0.equal_fold.{score}"),
    "v2": ("cp16.uncertainty.V2-H-B2.equal_fold.{metric}", "cp16.metrics.B2.equal_fold.{score}"),
}


def _change_records() -> list[DerivedRecord]:
    out = []
    for subject, (difference, denominator) in CHANGES.items():
        comparator = G.get(G.get(subject).comparator)
        for metric, score in (("MAE", "S_MAE"), ("WIS", "S_WIS")):
            diff_id, denom_id = difference.format(metric=metric), denominator.format(score=score)
            denom = _d(denom_id)
            out.append(DerivedRecord(
                f"derived.change.{subject}.{score}", "share_change", subject, UNIT_RELATIVE,
                _text(_share(_d(diff_id), denom)), (diff_id, denom_id),
                "paired difference / comparator's score × 100; the interval divided by the same denominator",
                0, "P18", ci_low=_text(_share(_d(diff_id, "ci_low"), denom)),
                ci_high=_text(_share(_d(diff_id, "ci_high"), denom)),
                label=f"as a share of {comparator.short}'s score"))
    return out


#: Absolute context (§3.3 c): per-period MAE in EUR/MWh for these identities.
PERIOD_SUBJECTS = ("v3", "v2", "daily-lear", "naive")


def _period_records() -> list[DerivedRecord]:
    out = []
    stress = stress_period()
    out.append(DerivedRecord("derived.periods.stress_period", "stress_period", None, UNIT_LABEL, stress, (),
                             "the protocol's named stress period", 0, "P19",
                             sources=tuple(path for path, _ in STRESS_QUOTES) + ("reports/cp10/protocol.json",)))
    for subject in PERIOD_SUBJECTS:
        code = G.get(subject).code_in(G.COMPARISON_EXPERIMENT)
        ordinary = [f"cp20.metrics.{code}.{fold}.MAE" for fold in FOLDS if fold != stress]
        low = min(ordinary, key=_d)
        high = max(ordinary, key=_d)
        for which, record_id in (("low", low), ("high", high)):
            out.append(DerivedRecord(
                f"derived.periods.{subject}.ordinary_{which}", "period_range", subject, UNIT_EUR,
                R.get(record_id).raw, tuple(ordinary),
                f"{'minimum' if which == 'low' else 'maximum'} MAE over the ordinary test periods", 1, "P19"))
        stress_id = f"cp20.metrics.{code}.{stress}.MAE"
        out.append(DerivedRecord(f"derived.periods.{subject}.stress", "period_stress", subject, UNIT_EUR,
                                 R.get(stress_id).raw, (stress_id,), "MAE in the stress period", 1, "P19"))
    return out


@lru_cache(maxsize=1)
def records() -> dict[str, DerivedRecord]:
    built = _criteria_records() + _change_records() + _period_records()
    out: dict[str, DerivedRecord] = {}
    for record in built:
        if record.record_id in out:
            raise DerivedError(f"duplicate derived record {record.record_id}")
        out[record.record_id] = record
    return out


def get(record_id: str) -> DerivedRecord:
    try:
        return records()[record_id]
    except KeyError:
        raise DerivedError(f"no derived record {record_id!r}") from None


def is_derived(record_id: str) -> bool:
    return record_id.startswith("derived.")


# --------------------------------------------------------------------------- validation


def validate_all() -> list[str]:
    """Recompute every derived record from a fresh read of its committed inputs. Empty means all hold.

    Each input record is re-read from its committed row (and its file's blob checked), then the
    derived value is recomputed from those fresh values, independent of every cache."""
    problems = []
    fresh = R.FreshRead()
    cache: dict[tuple[str, str], Decimal] = {}

    def value(record_id: str, which: str = "value") -> Decimal:
        key = (record_id, which)
        if key not in cache:
            derived = R.rederive(R.get(record_id), fresh)
            cache[key] = Decimal(derived["value" if which == "value" else which])
        return cache[key]

    counts = None
    for record in records().values():
        try:
            if record.kind == "rule_date":
                expected = _rule_date()
            elif record.kind == "stress_period":
                expected = stress_period()
            elif record.kind == "rule_margin":
                limit, reference = record.inputs
                expected = _text(-_relative(value(limit), value(reference)))
            elif record.kind == "distance":
                actual, reference = record.inputs
                expected = _text(_relative(value(actual), value(reference)))
            elif record.kind == "verdict":
                groups = [record.inputs[i:i + 4] for i in range(0, len(record.inputs), 4)]
                for actual, _limit, _reference, scored in groups:
                    if value(actual) != value(scored):
                        problems.append(f"{record.record_id}: {actual} no longer equals the committed score {scored}")
                expected = "met" if all(value(a) <= value(lim) for a, lim, _, _ in groups) else "not met"
            elif record.kind in ("tested", "first_to_meet"):
                if counts is None:
                    counts = _fresh_decision_counts(fresh)
                expected = counts[record.subject][0 if record.kind == "tested" else 1]
            elif record.kind == "share_change":
                diff_id, denom_id = record.inputs
                denom = value(denom_id)
                expected = _text(_share(value(diff_id), denom))
                low, high = _text(_share(value(diff_id, "ci_low"), denom)), _text(_share(value(diff_id, "ci_high"), denom))
                if (low, high) != (record.ci_low, record.ci_high):
                    problems.append(f"{record.record_id}: interval no longer follows from its rows")
            elif record.kind == "period_range":
                values = [value(record_id) for record_id in record.inputs]
                pick = min(values) if record.record_id.endswith("_low") else max(values)
                expected = _text(pick)
            elif record.kind == "period_stress":
                expected = _text(value(record.inputs[0]))
            else:
                problems.append(f"{record.record_id}: unknown kind {record.kind}")
                continue
            recorded = record.value if record.unit in (UNIT_LABEL, UNIT_DATE) else _text(Decimal(record.value))
            if expected != recorded:
                problems.append(f"{record.record_id}: {recorded!r} no longer follows from its rows ({expected!r})")
        except (R.EvidenceError, DerivedError, KeyError) as exc:
            problems.append(f"{record.record_id}: {exc}")
    return problems


# --------------------------------------------------------------------------- display


def display(record: DerivedRecord, which: str = "value", *, style: str | None = None) -> str:
    """The one display string for a derived value (standard §4): whole percent for relative
    changes, one decimal for EUR/MWh, the word itself for labels and dates. `style="abs"` drops the
    sign ("14% below" reads the sign in words)."""
    raw = {"value": record.value, "ci_low": record.ci_low, "ci_high": record.ci_high}[which]
    if raw is None:
        raise DerivedError(f"{record.record_id} has no {which}")
    if record.unit in (UNIT_LABEL, UNIT_DATE):
        return raw
    places = record.display_precision + (2 if style == "exact" else 0)  # value tables carry two more places
    quantized = Decimal(raw).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_EVEN)
    if quantized == 0:
        quantized = abs(quantized)
    text = f"{abs(quantized):,.{places}f}" if record.unit == UNIT_COUNT else f"{abs(quantized):.{places}f}"
    if style == "abs":
        sign = ""
    else:
        sign = R.MINUS if quantized < 0 else ""
    suffix = "%" if record.unit == UNIT_RELATIVE else ""
    return f"{sign}{text}{suffix}"


__all__ = [
    "CHANGES", "DerivedError", "DerivedRecord", "PERIOD_SUBJECTS", "RULE", "UNIT_COUNT", "UNIT_DATE", "UNIT_EUR",
    "UNIT_LABEL", "UNIT_RELATIVE", "display", "get", "is_derived", "records", "section_8", "stress_period",
    "validate_all",
]
