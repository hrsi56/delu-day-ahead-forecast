"""The registry: one source for every published identity, status and comparison (standard §5).

Publication Standard v1 §5 requires one entry per generation, branch, reference, study arm and
control, and requires every public surface to take its names, statuses and order from it: the
page's status pair, rail, jump row, lineage, comparison rows and chapter headers; the README's
headings; the Space cards' model line; and the `delu-generations` MLflow run names, parents,
descriptions and tags. Before PRES-1's conformance work those were typed in about 45 places in
nine files, and "current" was written into prose that becomes false the day v4 is adopted.

**Status is derived, never typed.** An entry carries a dated status history. A surface never
writes "current", "latest" or "the demo runs"; it asks this module, which answers from the
history -- `current_generation()`, `released()`, `status_sentence()` -- in the past tense and dated.

**One identity across experiment codes.** v2 is `V2-H` in CP-16 and `H0` in CP-20; v1 is `B1` in
CP-15 and `v1_reference` in CP-10. `by_code()` resolves either to the same entry, so a policy is
never renamed by the experiment that happens to evaluate it.

**Nothing here is a research number.** Dates, codes and names are identity; every score comes from
`delu_forecast.research` and `delu_forecast.derived`. `tests/test_35_registry.py` holds the
consistency checks and their negative controls.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from functools import lru_cache

# --------------------------------------------------------------------------- vocabularies (§5)

KINDS = ("generation", "branch", "reference", "study arm", "control")

ADOPTED_IN_RESEARCH = "adopted in research"
NOT_ADOPTED = "not adopted"
RELEASED = "released"
FINAL_CANDIDATE = "final candidate"
LIVE = "live"
RETIRED = "retired"
STATUSES = (ADOPTED_IN_RESEARCH, NOT_ADOPTED, RELEASED, FINAL_CANDIDATE, LIVE, RETIRED)

#: The hero shows the model with the highest status reached (standard §2): live, then final
#: candidate, then released, then research.
HERO_ORDER = (LIVE, FINAL_CANDIDATE, RELEASED, ADOPTED_IN_RESEARCH)

EVIDENCE_DEVELOPMENT = "development_post_selection"
EVIDENCE_CALIBRATION = "development_calibration_comparison"
EVIDENCE_V1_HOLDOUT = "confirmatory_style_not_power_qualified"

#: Evidence-class badges (plan §7.8, standard §2). The v1 text is verbatim and may wrap.
BADGES = {
    EVIDENCE_DEVELOPMENT: "Development · post-selection",
    EVIDENCE_CALIBRATION: "Development · post-selection",
    EVIDENCE_V1_HOLDOUT: "Confirmatory-style, not power-qualified",
}

#: Each evidence class's caveat, phrased as a property of the class (standard §1, Tone): it
#: never expires, and it appears once, where it applies.
CLASS_CAVEATS = {
    EVIDENCE_DEVELOPMENT: "development evidence, not a test on new data",
    EVIDENCE_CALIBRATION: "development evidence, not a test on new data",
    EVIDENCE_V1_HOLDOUT: "evaluated once, as specified in advance, on days never used for development or selection",
}

MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August", "September",
          "October", "November", "December")


class RegistryError(ValueError):
    """A surface asked for an identity or status the registry does not hold."""


# --------------------------------------------------------------------------- the entry (§5 fields)


@dataclass(frozen=True)
class Code:
    """One experiment code of an identity, with the population it was evaluated on there."""

    experiment: str
    code: str
    population: str
    note: str = ""


@dataclass(frozen=True)
class StatusEvent:
    """A dated status, with the record that establishes it."""

    status: str
    date: str
    source: str
    reason: str = ""


@dataclass(frozen=True)
class Entry:
    # identity
    id: str
    name: str
    subtitle: str
    kind: str
    # codes
    codes: tuple[Code, ...]
    # status history, dated
    statuses: tuple[StatusEvent, ...]
    # comparison
    comparator: str | None
    population: str | None
    # evidence
    evidence_class: str
    plan: str
    rules: tuple[str, ...]
    sources: tuple[str, ...]
    claim_map: str | None
    run_keys: tuple[str, ...]
    # presentation: the marker and colour role (plan §7.3, §7.8) and the page anchor
    style: str
    anchor: str | None = None
    #: The checkpoint that produced this identity first, and where a branch sits in the lineage.
    checkpoint: str | None = None
    after: str | None = None
    #: For branches: the question, and what the branch informed.
    question: str = ""
    informed: str | None = None
    #: A short form of the name for tight chart labels ("v3", "Daily LEAR").
    short: str = ""
    #: For a generation after the first: the adopted generation it replaced in research (A3). An
    #: explicit, validated relationship; never inferred from the version number or the name.
    predecessor: str | None = None

    @property
    def primary_code(self) -> str:
        return self.codes[0].code

    def code_in(self, experiment: str) -> str | None:
        for code in self.codes:
            if code.experiment == experiment:
                return code.code
        return None

    @property
    def version(self) -> str | None:
        """`v3` for a generation, None otherwise: a number exists only on adoption (plan §16 D2)."""
        match = re.match(r"^(v\d+) · ", self.name)
        return match.group(1) if match and self.kind == "generation" else None

    @property
    def status(self) -> StatusEvent | None:
        return self.statuses[-1] if self.statuses else None

    @property
    def badge(self) -> str:
        return BADGES[self.evidence_class]


# --------------------------------------------------------------------------- rules and checkpoints


@dataclass(frozen=True)
class Rule:
    """A decision rule the governing research plan set before the experiments it judges."""

    id: str
    plan: str
    words: str
    set_on: str
    provenance: tuple[str, ...]


RULES: dict[str, Rule] = {
    "criteria-1-2": Rule(
        id="criteria-1-2",
        plan="capstone_v21.md §8, criteria 1–2",
        words="each error score at least 10% below the strongest benchmark's",
        set_on="2026-09-15",
        provenance=(
            "capstone_v21.md: 'Active owner-authorized execution plan · 2026-09-15.'",
            "reports/cp15/attempt-1/capstone_v21.md: the anchor preserved from attempt 1; its §8 is identical",
            "bb5e678 (2026-09-16 00:17 +03:00): the pre-registration commit, reachable from evidence/cp-15",
            "0be8e56 (2026-09-16 03:15 +03:00): CP-15's results, committed after it",
        ),
    ),
    "joint-improvement": Rule(
        id="joint-improvement",
        plan="capstone_v21.md §14.4 and §15.4",
        words="both paired differences below zero: the interval score's upper 95% endpoint below zero and "
              "the point error's at or below zero",
        set_on="2026-09-23",
        provenance=("capstone_v21.md §14.4 (ratified O2 contract) and §15.4",),
    ),
    "cp21-adoption": Rule(
        id="cp21-adoption",
        plan="capstone_v21.md §17.6 (v21-r6)",
        words="HGL becomes v4 only if both paired differences against v3 improve (the interval score's upper 95% "
              "endpoint below zero, the point error's at or below zero), it meets all six original screening "
              "diagnostics, the evaluation is complete and valid, and no fold is decisively worse",
        set_on="2026-09-29",
        provenance=("capstone_v21.md v21-r6 §17.6 (ratified 2026-09-29)",
                    "reports/block-challenger/protocol.json adoption_rule_verbatim (frozen before scoring)"),
    ),
    "v1-holdout": Rule(
        id="v1-holdout",
        plan="capstone_V6_8.md §7.1",
        words="one pre-specified evaluation on a 90-day holdout, opened once",
        set_on="2026-09-09",
        provenance=("reports/cp2/holdout_report.json", "data/partitions.json"),
    ),
}


@dataclass(frozen=True)
class Checkpoint:
    """A checkpoint that produced registry entries: its owning entry and its evidence tag."""

    code: str
    run_key: str
    owner: str
    evidence_tag: str
    evidence_sha: str
    frozen_on: str
    report: str
    verdict: str
    landing: str
    #: The MLflow children, in the order the export and the UI list them.
    children: tuple[str, ...] = ()


CHECKPOINTS: dict[str, Checkpoint] = {
    "CP-10": Checkpoint("CP-10", "cp10", "calibration", "evidence/cp-15", "1bdc75b", "2026-09-16",
                        "reports/cp10/report.md", "docs/track-b/evidence/cp-10/integration.md",
                        "docs/track-b/cp-15-landing.md",
                        ("v1_reference", "c1_head_spread", "c1_price_volatility", "c2_aci_gamma_0.000001",
                         "c2_aci_gamma_0.000005", "c2_aci_gamma_0.00001", "c2_aci_gamma_0.00002")),
    "CP-15": Checkpoint("CP-15", "cp15", "model-comparison", "evidence/cp-15", "1bdc75b", "2026-09-16",
                        "reports/cp15/report.md", "docs/track-b/evidence/cp-15/integration.md",
                        "docs/track-b/cp-15-landing.md",
                        ("B0", "B1", "B2", "B3", "A1", "A2", "A3", "A4", "A5")),
    "CP-16": Checkpoint("CP-16", "cp16", "v2", "evidence/cp-16", "5ec8a92", "2026-09-23",
                        "reports/v2-causal/report.md", "docs/track-b/evidence/cp-16/integration.md",
                        "docs/track-b/cp-16-landing-2026-09-23.md", ("V2-P", "V2-H")),
    "CP-20": Checkpoint("CP-20", "cp20", "v3", "evidence/cp-20", "a7a9b2e", "2026-09-24",
                        "reports/weather-ablation/report.md", "docs/track-b/evidence/cp-20/integration.md",
                        "docs/track-b/cp-20-landing-2026-09-24.md", ("HG",)),
    "CP-21": Checkpoint("CP-21", "cp21", "v4", "evidence/cp-21", "1d13f99", "2026-09-30",
                        "reports/block-challenger/report.md", "docs/track-b/evidence/cp-21/integration.md",
                        "docs/track-b/cp-21-landing-2026-09-30.md", ("HGL", "L-P", "L-R", "L-N")),
}

#: Every evidence tag a public link may cite, with the date it froze (the date its commit was
#: made, in the author's time zone). An audit-grade link's label carries this date (standard §7).
EVIDENCE_TAGS: dict[str, tuple[str, str]] = {
    "evidence/cp-2": ("e491079", "2026-09-14"),
    "evidence/cp-3": ("73da531", "2026-09-15"),
    "evidence/cp-3b": ("0adc309", "2026-09-15"),
    "evidence/cp-15": ("1bdc75b", "2026-09-16"),
    "evidence/cp-16": ("5ec8a92", "2026-09-23"),
    "evidence/cp-20": ("a7a9b2e", "2026-09-24"),
    "evidence/cp-21": ("1d13f99", "2026-09-30"),
}

POPULATIONS = {
    "common-10747h": "the 10,747 eligible development hours shared by CP-15, CP-16, CP-20 and CP-21",
    "cp10-fold-block": "CP-10's full fold blocks, v1's nine-quantile scores",
    "v1-holdout-90d": "v1's pre-specified 90-day holdout, delivery 2026-06-09..2026-09-06",
}

_CP15 = "docs/track-b/research-content/cp15-cp16-claims.md"
_CP20 = "docs/track-b/research-content/cp20-claims.md"
_CP21 = "docs/track-b/research-content/cp21-claims.md"
_LANDING21 = "docs/track-b/cp-21-landing-2026-09-30.md"
#: CP-21's committed rows, the sources of its entries (the publication packet's §2).
_CP21_SOURCES = ("reports/block-challenger/metrics.csv", "reports/block-challenger/uncertainty.csv",
                 "reports/block-challenger/criteria.csv", "reports/block-challenger/adoption.json")
_PLAN21 = "capstone_v21.md"


def _study(ident: str, code: str, name: str, subtitle: str, short: str = "") -> Entry:
    # A1 is the study's best challenger; CP-16 and CP-20 carry its saved rows as a comparator.
    later = (Code("CP-16", code, "common-10747h"), Code("CP-20", code, "common-10747h"),
             Code("CP-21", code, "common-10747h")) if code == "A1" else ()
    return Entry(
        id=ident, name=name, subtitle=subtitle, kind="study arm",
        codes=(Code("CP-15", code, "common-10747h"), *later),
        statuses=(StatusEvent(NOT_ADOPTED, "2026-09-16", "docs/track-b/cp-15-landing.md",
                              "no study policy met the product criteria"),),
        comparator="daily-lear", population="common-10747h", evidence_class=EVIDENCE_DEVELOPMENT,
        plan=f"{_PLAN21} §5–§8 (v21-r1)", rules=("criteria-1-2",),
        sources=("reports/cp15/relative_scores.csv", "reports/cp15/criteria.csv"), claim_map=_CP15,
        run_keys=(f"cp15/{code}",), style="study", checkpoint="CP-15", short=short or name,
    )


def _reference(ident: str, code: str, name: str, subtitle: str, *, comparator: str | None, note: str = "") -> Entry:
    return Entry(
        id=ident, name=name, subtitle=subtitle, kind="reference",
        codes=(Code("CP-15", code, "common-10747h", note), Code("CP-16", code, "common-10747h", note),
               Code("CP-20", code, "common-10747h", note), Code("CP-21", code, "common-10747h", note)),
        statuses=(), comparator=comparator, population="common-10747h", evidence_class=EVIDENCE_DEVELOPMENT,
        plan=f"{_PLAN21} §5 (v21-r1)", rules=(), sources=("reports/cp15/relative_scores.csv",),
        claim_map=_CP15, run_keys=(f"cp15/{code}",), style="reference", checkpoint="CP-15", short=name,
    )


def _cp10(ident: str, code: str, name: str, subtitle: str, note: str = "") -> Entry:
    return Entry(
        id=ident, name=name, subtitle=subtitle, kind="study arm",
        codes=(Code("CP-10", code, "cp10-fold-block", note),),
        statuses=(StatusEvent(NOT_ADOPTED, "2026-09-16", "docs/track-b/cp-15-landing.md",
                              "recalibrating v1 without refitting it was not enough"),),
        comparator="v1", population="cp10-fold-block", evidence_class=EVIDENCE_CALIBRATION,
        plan="capstone_v20.md §4 and §9 CP-10", rules=(), sources=("reports/cp10/metrics.csv",),
        claim_map=_CP20, run_keys=(f"cp10/{code}",), style="study", checkpoint="CP-10", short=name,
    )


def _cp21_arm(ident: str, code: str, name: str, subtitle: str, short: str) -> Entry:
    return Entry(
        id=ident, name=name, subtitle=subtitle, kind="study arm",
        codes=(Code("CP-21", code, "common-10747h"),),
        statuses=(StatusEvent(NOT_ADOPTED, "2026-09-30", _LANDING21,
                              "a study arm for attribution; never eligible for adoption"),),
        comparator="v3", population="common-10747h", evidence_class=EVIDENCE_DEVELOPMENT,
        plan=f"{_PLAN21} §17 (v21-r6)", rules=("cp21-adoption",), sources=_CP21_SOURCES, claim_map=_CP21,
        run_keys=(f"cp21/{code}",), style="study", checkpoint="CP-21", short=short,
    )


#: Every published identity. The order within a kind is the order surfaces show it in:
#: generations oldest first (the lineage reads left to right; chapters reverse it), branches in
#: time order, references and study arms in the comparison's fixed order.
_ENTRIES: tuple[Entry, ...] = (
    # ---- generations -------------------------------------------------------------------
    Entry(
        id="v1", name="v1 · released LightGBM", subtitle="Nine-quantile LightGBM with calibrated intervals",
        kind="generation",
        codes=(Code("CP-15", "B1", "common-10747h", "development replay"),
               Code("CP-16", "B1", "common-10747h", "development replay"),
               Code("CP-20", "B1", "common-10747h", "development replay"),
               Code("CP-10", "v1_reference", "cp10-fold-block", "unscaled CQR reference"),
               Code("CP-21", "B1", "common-10747h", "development replay")),
        statuses=(StatusEvent(RELEASED, "2026-09-15", "land/cp-3 and land/cp-3b, 2026-09-15"),),
        comparator="naive", population="v1-holdout-90d", evidence_class=EVIDENCE_V1_HOLDOUT,
        plan="capstone_V6_8.md", rules=("v1-holdout",),
        sources=("reports/cp2/holdout_report.json", "reports/cp15/relative_scores.csv"),
        claim_map=None, run_keys=("cp15/B1", "cp10/v1_reference"), style="v1", anchor="#v1",
        checkpoint="CP-3", short="v1",
    ),
    Entry(
        id="v2", name="v2 · blended LEAR, hour-aware intervals",
        subtitle="Two LEAR forecasts blended, hour-aware intervals", kind="generation",
        codes=(Code("CP-16", "V2-H", "common-10747h"), Code("CP-20", "H0", "common-10747h"),
               Code("CP-21", "H0", "common-10747h", "saved reference")),
        statuses=(StatusEvent(ADOPTED_IN_RESEARCH, "2026-09-23", "docs/track-b/cp-16-landing-2026-09-23.md"),),
        comparator="daily-lear", population="common-10747h", evidence_class=EVIDENCE_DEVELOPMENT,
        plan=f"{_PLAN21} §14 (v21-r3)", rules=("criteria-1-2", "joint-improvement"),
        sources=("reports/v2-causal/metrics.csv", "reports/v2-causal/uncertainty.csv", "reports/v2-causal/criteria.csv"),
        claim_map=_CP15, run_keys=("cp16", "cp16/V2-H"), style="v2", anchor="#v2", checkpoint="CP-16", short="v2",
        predecessor="v1",
    ),
    Entry(
        id="v3", name="v3 · weather features", subtitle="v2 plus three weather forecast inputs",
        kind="generation",
        codes=(Code("CP-20", "HG", "common-10747h"), Code("CP-21", "HG", "common-10747h", "comparator, saved")),
        statuses=(StatusEvent(ADOPTED_IN_RESEARCH, "2026-09-24", "docs/track-b/cp-20-landing-2026-09-24.md"),),
        comparator="v2", population="common-10747h", evidence_class=EVIDENCE_DEVELOPMENT,
        plan=f"{_PLAN21} §15 (v21-r4)", rules=("criteria-1-2", "joint-improvement"),
        sources=("reports/weather-ablation/metrics.csv", "reports/weather-ablation/uncertainty.csv",
                 "reports/weather-ablation/criteria.csv"),
        claim_map=_CP20, run_keys=("cp20", "cp20/HG"), style="v3", anchor="#v3", checkpoint="CP-20", short="v3",
        predecessor="v2",
    ),
    Entry(
        id="v4", name="v4 · three-block LightGBM added", subtitle="v3 plus a three-block LightGBM member",
        kind="generation",
        codes=(Code("CP-21", "HGL", "common-10747h"),),
        statuses=(StatusEvent(ADOPTED_IN_RESEARCH, "2026-09-30", _LANDING21),),
        comparator="v3", population="common-10747h", evidence_class=EVIDENCE_DEVELOPMENT,
        plan=f"{_PLAN21} §17 (v21-r6)", rules=("cp21-adoption",), sources=_CP21_SOURCES,
        claim_map=_CP21, run_keys=("cp21", "cp21/HGL"), style="v4", anchor="#v4", checkpoint="CP-21", short="v4",
        predecessor="v3",
    ),
    # ---- branches ------------------------------------------------------------------------
    Entry(
        id="calibration", name="Calibration experiment", subtitle="Recalibrating v1 without refitting it",
        kind="branch", codes=(Code("programme", "CP-10", "cp10-fold-block"),),
        statuses=(StatusEvent(NOT_ADOPTED, "2026-09-16", "docs/track-b/cp-15-landing.md",
                              "recalibrating v1 without refitting it was not enough"),),
        comparator="v1", population="cp10-fold-block", evidence_class=EVIDENCE_CALIBRATION,
        plan="capstone_v20.md §4 and §9 CP-10", rules=(), sources=("reports/cp10/peak_windows.csv",),
        claim_map=_CP20, run_keys=("cp10",), style="branch", anchor="#branch-calibration",
        checkpoint="CP-10", after="v1",
        question="Can recalibrating v1, without refitting it, repair its coverage in the 2022 crisis?",
        short="Calibration experiment",
    ),
    Entry(
        id="model-comparison", name="Model comparison study", subtitle="Nine forecasting policies on identical hours",
        kind="branch", codes=(Code("programme", "CP-15", "common-10747h"),),
        statuses=(StatusEvent(NOT_ADOPTED, "2026-09-16", "docs/track-b/cp-15-landing.md",
                              "no policy met the product criteria"),),
        comparator="daily-lear", population="common-10747h", evidence_class=EVIDENCE_DEVELOPMENT,
        plan=f"{_PLAN21} §5–§8 (v21-r1)", rules=("criteria-1-2",),
        sources=("reports/cp15/relative_scores.csv", "reports/cp15/peak.csv", "reports/cp15/criteria.csv"),
        claim_map=_CP15, run_keys=("cp15",), style="branch", anchor="#branch-model-comparison",
        checkpoint="CP-15", after="calibration", informed="v2",
        question="Which forecasting approach copes best with the 2022 crisis?",
        short="Model comparison study",
    ),
    # ---- references ----------------------------------------------------------------------
    _reference("naive", "B0", "Similar-day naive", "The forecast every error score divides by",
               comparator=None, note="normalizer"),
    _reference("daily-lear", "B2", "Daily LEAR", "The strongest benchmark: a daily linear model",
               comparator="naive"),
    _reference("daily-lightgbm", "B3", "Daily LightGBM", "Gradient-boosted trees refitted every day",
               comparator="naive"),
    # ---- study arms (CP-15) --------------------------------------------------------------
    _study("normalized-lear", "A1", "Normalized LEAR", "LEAR on a normalized price target"),
    _study("normalized-lightgbm", "A2", "Normalized LightGBM", "LightGBM on a normalized price target"),
    _study("component-mean", "A3", "Normalized component mean", "Mean of the normalized components"),
    _study("normalized-lear-84d", "A4", "84-day normalized LEAR", "Normalized LEAR with a shorter history"),
    _study("component-mean-variant", "A5", "Normalized component mean, variant",
           "A variant of the normalized component mean"),
    # ---- control (CP-16) -----------------------------------------------------------------
    Entry(
        id="pooled-control", name="Pooled-interval control", subtitle="v2's blend with pooled residual intervals",
        kind="control", codes=(Code("CP-16", "V2-P", "common-10747h"),),
        statuses=(StatusEvent(NOT_ADOPTED, "2026-09-23", "docs/track-b/cp-16-landing-2026-09-23.md",
                              "the control that isolates hour-aware intervals"),),
        comparator="daily-lear", population="common-10747h", evidence_class=EVIDENCE_DEVELOPMENT,
        plan=f"{_PLAN21} §14 (v21-r3)", rules=("criteria-1-2", "joint-improvement"),
        sources=("reports/v2-causal/metrics.csv", "reports/v2-causal/uncertainty.csv"),
        claim_map=_CP15, run_keys=("cp16/V2-P",), style="control", checkpoint="CP-16",
        short="Pooled-interval control",
    ),
    # ---- study arms (CP-21): the ladder that attributes v4's change; never eligible for adoption ----------
    _cp21_arm("pooled-lightgbm-weather", "L-P", "Pooled LightGBM with weather", "One 24-hour LightGBM on v3 information",
              "Pooled LightGBM"),
    _cp21_arm("block-lightgbm", "L-R", "Three-block LightGBM", "Night, solar and peak models, raw price",
              "Block LightGBM"),
    _cp21_arm("normalized-block-lightgbm", "L-N", "Normalized three-block LightGBM",
              "The block models on a normalized price", "Normalized block LightGBM"),
    # ---- the calibration experiment's arms (CP-10) ---------------------------------------
    _cp10("cp10-head-spread", "c1_head_spread", "Scaled conformal, head spread",
          "Conformal scores scaled by the heads' spread"),
    _cp10("cp10-price-volatility", "c1_price_volatility", "Scaled conformal, price volatility",
          "Conformal scores scaled by recent price volatility", "selected scale"),
    _cp10("cp10-aci-0.000001", "c2_aci_gamma_0.000001", "Adaptive conformal, gamma 0.000001",
          "Adaptive conformal intervals, smallest step"),
    _cp10("cp10-aci-0.000005", "c2_aci_gamma_0.000005", "Adaptive conformal, gamma 0.000005",
          "Adaptive conformal intervals, second step"),
    _cp10("cp10-aci-0.00001", "c2_aci_gamma_0.00001", "Adaptive conformal, gamma 0.00001",
          "Adaptive conformal intervals, third step"),
    _cp10("cp10-aci-0.00002", "c2_aci_gamma_0.00002", "Adaptive conformal, gamma 0.00002",
          "Adaptive conformal intervals, largest step", "selected step"),
)

#: The order of the shared comparison's rows (plan §8.2): generations newest first, then the
#: benchmarks and the study's best challenger by score, v1's development replay, and the naive.
COMPARISON_ORDER = ("v4", "v3", "v2", "daily-lear", "normalized-lear", "daily-lightgbm", "v1", "naive")

#: The shared comparison as v3's chapter published it, from CP-20's rows. It redraws the overview that the
#: `cp20/HG` MLflow run carries as an artifact, byte for byte: a published record never changes (§17.9).
V3_COMPARISON_ORDER = ("v3", "v2", "daily-lear", "normalized-lear", "daily-lightgbm", "v1", "naive")

#: The marker-key words for the non-generation styles.
STYLE_LABELS = {"reference": "reference", "study": "study arm", "control": "control arm"}


#: The order of the scores chart at the time of v2 (the v2 chapter's protocol detail).
V2_SCORES_ORDER = ("v2", "pooled-control", "daily-lear", "normalized-lear", "daily-lightgbm", "v1")

#: The crisis window's rows in v3's chapter: v1, the study's best challenger, then the generations after it.
#: Pinned, as the chapter and the `cp20/HG` MLflow run published them.
V3_CRISIS_ORDER = ("v1", "normalized-lear", "v2", "v3")

#: The crisis window's rows in v4's chapter, which shows the window (runbook §2 step 6): the adopted
#: generations CP-21 scored on it, oldest first, so v4's peak error sits beside v3's on one readable scale.
CRISIS_ORDER = ("v2", "v3", "v4")

#: The release rule, stated once (standard §5): the demo runs the released model.
RELEASE_RULE = (
    "Research generations are not released one by one; only the final model, after its one-shot test "
    "and live run, replaces the released one."
)


# --------------------------------------------------------------------------- lookups


@lru_cache(maxsize=1)
def entries() -> tuple[Entry, ...]:
    ids = [entry.id for entry in _ENTRIES]
    if len(ids) != len(set(ids)):
        raise RegistryError("duplicate registry id")
    return _ENTRIES


@lru_cache(maxsize=1)
def _by_id() -> dict[str, Entry]:
    return {entry.id: entry for entry in entries()}


def get(ident: str) -> Entry:
    try:
        return _by_id()[ident]
    except KeyError:
        raise RegistryError(f"no registry entry {ident!r}") from None


@lru_cache(maxsize=1)
def _by_code() -> dict[str, Entry]:
    out: dict[str, Entry] = {}
    for entry in entries():
        for code in entry.codes:
            if code.code in out and out[code.code].id != entry.id:
                raise RegistryError(f"code {code.code!r} names two identities")
            out[code.code] = entry
    return out


def by_code(code: str) -> Entry:
    """The one identity behind an experiment code: `H0` and `V2-H` are both v2."""
    try:
        return _by_code()[code]
    except KeyError:
        raise RegistryError(f"no registry entry carries the code {code!r}") from None


def codes() -> tuple[str, ...]:
    """Every experiment code in the registry: the lint's generated denylist (standard §4)."""
    return tuple(sorted({code.code for entry in entries() for code in entry.codes}))


def of_kind(kind: str) -> tuple[Entry, ...]:
    if kind not in KINDS:
        raise RegistryError(f"unknown kind {kind!r}")
    return tuple(entry for entry in entries() if entry.kind == kind)


def generations(*, newest_first: bool = False) -> tuple[Entry, ...]:
    ordered = sorted(of_kind("generation"), key=lambda entry: int(entry.version[1:]))
    return tuple(reversed(ordered)) if newest_first else tuple(ordered)


def branches() -> tuple[Entry, ...]:
    return of_kind("branch")


def generation_of(code: str) -> str | None:
    """The adopted generation a code belongs to, or None: references and study arms have none."""
    entry = _by_code().get(code)
    return entry.version if entry is not None else None


def with_status(status: str) -> tuple[Entry, ...]:
    return tuple(entry for entry in entries() if entry.status is not None and entry.status.status == status)


def current_generation() -> Entry:
    """The newest generation adopted in research or beyond: the headline's subject (§3.4)."""
    candidates = [entry for entry in generations()
                  if entry.status is not None and entry.status.status in HERO_ORDER]
    if not candidates:
        raise RegistryError("no adopted generation")
    return candidates[-1]


def released() -> Entry:
    """The released model: the one the demo runs (the release rule, §5)."""
    found = [entry for entry in generations() if entry.status is not None and entry.status.status == RELEASED]
    if len(found) != 1:
        raise RegistryError(f"exactly one released model is required; found {len(found)}")
    return found[0]


def hero() -> Entry:
    """The model with the highest status reached: live, final candidate, released, research (§2)."""
    for status in HERO_ORDER:
        found = [entry for entry in generations() if entry.status is not None and entry.status.status == status]
        if found:
            return found[-1]
    raise RegistryError("no generation has a status")


def population_in(entry: Entry, experiment: str) -> str:
    """The comparability ID of an identity's evaluated population in one experiment."""
    for code in entry.codes:
        if code.experiment == experiment:
            return code.population
    raise RegistryError(f"{entry.id} was not evaluated in {experiment}")


#: The experiment whose committed rows the shared comparison draws (plan §8.2).
COMPARISON_EXPERIMENT = "CP-21"

#: Each experiment's record prefix in `delu_forecast.research`.
EXPERIMENT_PREFIX = {"CP-15": "cp15", "CP-16": "cp16", "CP-20": "cp20", "CP-21": "cp21"}


def comparison_prefix(experiment: str | None = None) -> str:
    """The record prefix of the experiment whose rows a comparison draws: `cp21.metrics.…`."""
    return EXPERIMENT_PREFIX[experiment or COMPARISON_EXPERIMENT]


def comparison_rows(order: tuple[str, ...] | None = None, experiment: str | None = None) -> tuple[Entry, ...]:
    """The shared comparison's rows, refusing a mix of evaluated populations (standard §5). Without arguments, the
    live comparison; v3's pinned one is `comparison_rows(V3_COMPARISON_ORDER, "CP-20")`."""
    order, experiment = order or COMPARISON_ORDER, experiment or COMPARISON_EXPERIMENT
    rows = tuple(get(ident) for ident in order)
    populations = {population_in(entry, experiment) for entry in rows}
    if len(populations) != 1:
        raise RegistryError(f"one comparison chart holds one comparability ID; got {sorted(populations)}")
    return rows


def checkpoint_of_run_key(run_key: str) -> Checkpoint:
    prefix = run_key.split("/")[0]
    for checkpoint in CHECKPOINTS.values():
        if checkpoint.run_key == prefix:
            return checkpoint
    raise RegistryError(f"no checkpoint owns the run key {run_key!r}")


def entry_for_run_key(run_key: str) -> Entry:
    for entry in entries():
        if run_key in entry.run_keys:
            return entry
    raise RegistryError(f"no registry entry owns the run key {run_key!r}")


# --------------------------------------------------------------------------- derived wording


def month(iso: str) -> str:
    day = date.fromisoformat(iso)
    return f"{MONTHS[day.month - 1]} {day.year}"


def status_sentence(entry: Entry) -> str:
    """The dated, past-tense status (standard §5): 'In September 2026, v3 was adopted in research.'"""
    event = entry.status
    if event is None:
        raise RegistryError(f"{entry.id} has no status")
    subject = entry.version or f"the {entry.name[0].lower()}{entry.name[1:]}"
    verb = {"adopted in research": "was adopted in research", "not adopted": "was not adopted",
            "released": "was released", "final candidate": "became the final candidate",
            "live": "went live", "retired": "was retired"}[event.status]
    return f"In {month(event.date)}, {subject} {verb}."


def run_role(run_key: str) -> str:
    """A run's role inside its checkpoint (plan §10.5): an identity first produced elsewhere is a
    saved reference there; otherwise its kind decides."""
    entry, checkpoint = entry_for_run_key(run_key), checkpoint_of_run_key(run_key)
    if entry.checkpoint != checkpoint.code or entry.kind == "reference":
        return "reference"
    return "control" if entry.kind == "control" else "candidate"


def adopted_flag(entry: Entry) -> str:
    """`delu.adopted`: true once adopted in research or beyond, false when not adopted, n/a otherwise."""
    if entry.status is None:
        return "n/a"
    return "false" if entry.status.status in (NOT_ADOPTED, RETIRED) else "true"


def parent_run_keys() -> tuple[str, ...]:
    """The `delu-generations` parents, one per checkpoint, in time order."""
    return tuple(checkpoint.run_key for checkpoint in CHECKPOINTS.values())


def expected_run_keys() -> tuple[str, ...]:
    """Every `delu-generations` run the registry expects: each checkpoint's parent, then its children."""
    out = []
    for checkpoint in CHECKPOINTS.values():
        out.append(checkpoint.run_key)
        out += [f"{checkpoint.run_key}/{code}" for code in checkpoint.children]
    return tuple(out)


@dataclass(frozen=True)
class Transition:
    """One adopted generation replacing its predecessor in research (PUBLISH_RULES 1.0, A3)."""

    predecessor: Entry
    successor: Entry

    @property
    def id(self) -> str:
        return f"{self.predecessor.id}-{self.successor.id}"

    @property
    def comparator(self) -> Entry:
        """The comparator the governing protocol named for the successor, which may differ from the
        predecessor: v2 was judged against daily LEAR, v3 against v2."""
        return get(self.successor.comparator)

    @property
    def comparator_is_predecessor(self) -> bool:
        return self.successor.comparator == self.predecessor.id


def first_status(entry: Entry) -> StatusEvent:
    """The event that put an identity on the main line: its adoption or release, dated."""
    if not entry.statuses:
        raise RegistryError(f"{entry.id} has no status")
    return entry.statuses[0]


def transition_problems(entries_: tuple[Entry, ...] | None = None) -> list[str]:
    """Why the predecessor relationships are not one dated chain of adopted generations."""
    pool = entries_ if entries_ is not None else entries()
    by_id = {entry.id: entry for entry in pool}
    gens = [entry for entry in pool if entry.kind == "generation"]
    problems = []
    for entry in pool:
        if entry.predecessor is not None and entry.kind != "generation":
            problems.append(f"{entry.id}: only a generation has a predecessor")
    firsts = [entry.id for entry in gens if entry.predecessor is None]
    if len(firsts) != 1:
        problems.append(f"exactly one generation starts the main line; found {firsts}")
    successors: dict[str, str] = {}
    for entry in gens:
        if entry.predecessor is None:
            continue
        before = by_id.get(entry.predecessor)
        if before is None or before.kind != "generation":
            problems.append(f"{entry.id}: predecessor {entry.predecessor!r} is not a registered generation")
            continue
        if entry.predecessor in successors:
            problems.append(f"{entry.predecessor} precedes both {successors[entry.predecessor]} and {entry.id}")
        successors[entry.predecessor] = entry.id
        if not (entry.statuses and before.statuses) or first_status(before).date > first_status(entry).date:
            problems.append(f"{entry.id}: adopted before its predecessor {before.id}")
    # one chain: following predecessors from every generation reaches the first without a cycle
    for entry in gens:
        seen, node = set(), entry
        while node is not None and node.predecessor is not None:
            if node.id in seen:
                problems.append(f"{entry.id}: the predecessor chain loops")
                break
            seen.add(node.id)
            node = by_id.get(node.predecessor)
    return problems


def transitions(*, newest_first: bool = True) -> tuple[Transition, ...]:
    """Every adopted transition, from the validated predecessor relationships (A3)."""
    problems = transition_problems()
    if problems:
        raise RegistryError("; ".join(problems))
    out = [Transition(get(entry.predecessor), entry) for entry in generations() if entry.predecessor]
    out.sort(key=lambda item: first_status(item.successor).date, reverse=newest_first)
    return tuple(out)


def transition_into(entry: Entry) -> Transition | None:
    return next((item for item in transitions() if item.successor.id == entry.id), None)


def inline_name(entry: Entry) -> str:
    """The name inside a sentence: 'daily LEAR', 'the similar-day naive'; a version keeps its case."""
    if entry.version or entry.name[:2].isupper():
        return entry.name
    return entry.name[0].lower() + entry.name[1:]


ADOPTION_LABELS = {ADOPTED_IN_RESEARCH: "Adopted in research", NOT_ADOPTED: "Not adopted", RELEASED: "Released",
                   FINAL_CANDIDATE: "Final candidate", LIVE: "Live", RETIRED: "Retired"}


def adoption_label(entry: Entry) -> str:
    """The adoption label (plan §7.8): text, separate from the badge, from the dated status."""
    if entry.status is None:
        raise RegistryError(f"{entry.id} has no status")
    return ADOPTION_LABELS[entry.status.status]


def release_sentence() -> str:
    """The release rule, stated once (standard §5), with the released model named from the history."""
    return f"The demo runs the released model, {released().version}. {RELEASE_RULE}"


def resolve(ident: str) -> Entry:
    """A registry id, or one of the derived aliases `current` and `released`."""
    if ident == "current":
        return current_generation()
    if ident == "released":
        return released()
    return get(ident)


def common_run_key(entry: Entry) -> str:
    """An identity's run on the shared population (CP-15/16/20): v2's is CP-16's V2-H, never H0."""
    for key in entry.run_keys:
        if "/" in key and not key.startswith("cp10/"):
            return key
    raise RegistryError(f"{entry.id} has no run on the shared population")


def expected_routes() -> dict[str, tuple[str, tuple[str, ...]]]:
    """Every MLflow reader route the surfaces advertise once it is verified (standard §9), as
    `{route id: (kind, run keys)}`: the experiment, the shared comparison, each research
    generation against its comparator, and each branch's own runs. Nothing else is advertised."""
    routes: dict[str, tuple[str, tuple[str, ...]]] = {"experiment": ("experiment", ())}
    routes["compare:overview"] = ("compare", tuple(common_run_key(entry) for entry in comparison_rows()))
    for entry in generations():
        checkpoint = CHECKPOINTS.get(entry.checkpoint)
        if checkpoint is None:
            continue  # v1's runs are its own experiment's, delu-cp2
        runs = tuple(f"{checkpoint.run_key}/{code}" for code in checkpoint.children)
        routes[f"compare:{entry.id}"] = ("compare", runs + (common_run_key(get(entry.comparator)),))
    for entry in branches():
        checkpoint = CHECKPOINTS[entry.checkpoint]
        routes[f"compare:{entry.id}"] = ("compare", tuple(f"{checkpoint.run_key}/{code}" for code in checkpoint.children))
    return routes


def mlflow_run_name(run_key: str) -> str:
    """A run's public name in `delu-generations`: its registry name, then its code in that experiment."""
    if "/" not in run_key:
        checkpoint = checkpoint_of_run_key(run_key)
        return f"{get(checkpoint.owner).name} ({checkpoint.code})"
    entry = entry_for_run_key(run_key)
    checkpoint = checkpoint_of_run_key(run_key)
    code = run_key.split("/", 1)[1]
    note = next((c.note for c in entry.codes if c.code == code and c.experiment == checkpoint.code), "")
    if entry.code_in(checkpoint.code) != code:
        raise RegistryError(f"{run_key}: {entry.id} has no code {code} in {checkpoint.code}")
    return f"{entry.name} ({code}{', ' + note if note else ''})"


__all__ = [
    "ADOPTED_IN_RESEARCH", "BADGES", "CHECKPOINTS", "CLASS_CAVEATS", "COMPARISON_ORDER", "CRISIS_ORDER", "Checkpoint", "Code",
    "EVIDENCE_CALIBRATION", "EVIDENCE_DEVELOPMENT", "EVIDENCE_TAGS", "EVIDENCE_V1_HOLDOUT", "Entry",
    "FINAL_CANDIDATE", "HERO_ORDER", "KINDS", "LIVE", "NOT_ADOPTED", "POPULATIONS", "RELEASED", "RELEASE_RULE",
    "RETIRED", "RULES", "STYLE_LABELS", "RegistryError", "Rule", "STATUSES", "StatusEvent", "Transition",
    "V2_SCORES_ORDER", "V3_COMPARISON_ORDER", "V3_CRISIS_ORDER", "EXPERIMENT_PREFIX", "comparison_prefix", "branches", "by_code", "codes", "first_status", "transition_into", "transition_problems",
    "transitions",
    "adopted_flag", "common_run_key", "comparison_rows", "expected_routes", "expected_run_keys", "run_role", "COMPARISON_EXPERIMENT", "current_generation", "entries", "entry_for_run_key", "generation_of", "generations",
    "get", "hero", "mlflow_run_name", "month", "adoption_label", "inline_name", "of_kind", "parent_run_keys", "release_sentence", "resolve", "population_in", "released", "status_sentence", "with_status",
]
