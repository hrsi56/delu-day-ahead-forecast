"""The research claims every public surface may render, and how (presentation plan §9.1, §9.3).

Each piece of research wording is a **block**: an approved template bound to one claim ID from
the claim maps (`docs/track-b/research-content/cp15-cp16-claims.md` and `cp20-claims.md`) and to
the evidence records its numbers come from. A generator never types a research number; it asks
for a block, and the block fills its numbers from `delu_forecast.research`.

Template tokens:

* `{r:RECORD}` a record's value; `{r:RECORD|ci}` its interval "[low, high]"; `|lo`, `|hi` one
  endpoint; `|pct` a fraction as a percentage; `|exact` / `|exact_hi` the full decimal
  expansion; `|p=N` N decimal places.
* `{s:KIND:TEXT}` a structural numeral -- a version label, date, fold index, section number or
  control value -- declared as such so it cannot carry a research result.
* `{v1:KEY}` a v1 claim from `claims.py`, the one v1 claim set.
* `**bold**` and `` `code` `` as in Markdown.

In HTML a value becomes `<data value=… data-claim=… data-record=…>`; inside SVG the renderer puts
the same `data-claim`/`data-record` attributes on the `<text>` or mark itself (`<data>` is not
valid SVG). In Markdown the same template renders plain text, so the README and the page cannot
disagree about a number. `tests/test_30_research_claims_rendered.py` holds the guards.
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from pathlib import Path

from . import derived as D
from . import registry as G
from . import research as R

REPO_ROOT = R.REPO_ROOT
CLAIM_MAPS = (
    REPO_ROOT / "docs" / "track-b" / "research-content" / "cp15-cp16-claims.md",
    REPO_ROOT / "docs" / "track-b" / "research-content" / "cp20-claims.md",
    REPO_ROOT / "docs" / "track-b" / "research-content" / "publication-claims.md",
)

# --------------------------------------------------------------------------- names and labels

# Names, kinds and statuses are not typed here: they come from `delu_forecast.registry`
# (standard §5), which replaced the hand-written POLICY_NAMES and POLICY_ROLES maps.

#: Evidence badges (plan §7.8). The v1 text is verbatim and may wrap; it is never shortened.
BADGE_DEVELOPMENT = "Development · post-selection"
BADGE_V1_HOLDOUT = "Confirmatory-style, not power-qualified"
BADGE_PROSPECTIVE = "Prospective"  # reserved for the live model; not rendered yet (plan §15)

#: Adoption labels: text, separate from the badge, and never a success colour or check mark.
ADOPTED = "Adopted"
NOT_ADOPTED = "Not adopted"
PLANNED = "Planned, not evaluated"

#: The Owner's contribution statement (plan §8.9), displayed exactly as written. It is not a
#: research claim, and only the Owner changes it.
#: The Owner's contribution statement. Plan §8.9 carried the first English rendering; at Stop 1
#: (2026-09-25) the Owner approved the wording proposed in the D1 editorial review, shown as written.
CONTRIBUTION_STATEMENT = (
    "I led the project's problem definition, evaluation criteria and research direction, and made "
    "the decisions on model adoption and product presentation. AI agents assisted with "
    "implementation, analysis and documentation. Automated tests and reviews separate from "
    "implementation supported verification. I retained responsibility for approving deliverables "
    "and publication."
)

#: The Owner's approved public name (Stop 1, 2026-09-25), used once as a byline near the opening
#: and to sign the contribution statement.
OWNER_PUBLIC_NAME = "Yarden Viktor Dejorno"

# --------------------------------------------------------------------------- blocks


@dataclass(frozen=True)
class Block:
    key: str
    claim_id: str
    template: str
    surfaces: frozenset[str]
    status: str = "published"

    def records(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(match.group(1) for match in _RECORD_TOKEN.finditer(self.template)))


def _block(key: str, claim_id: str, template: str, *surfaces: str) -> Block:
    return Block(key, claim_id, " ".join(template.split()), frozenset(surfaces or ("page",)))


PAGE, README = "page", "readme"

_HG_MAE = "cp20.uncertainty.HG-H0.equal_fold.MAE"
_HG_WIS = "cp20.uncertainty.HG-H0.equal_fold.WIS"
_HP_MAE = "cp16.uncertainty.V2-H-V2-P.equal_fold.MAE"
_HP_WIS = "cp16.uncertainty.V2-H-V2-P.equal_fold.WIS"
_HB_MAE = "cp16.uncertainty.V2-H-B2.equal_fold.MAE"
_HB_WIS = "cp16.uncertainty.V2-H-B2.equal_fold.WIS"
_PB_MAE = "cp16.uncertainty.V2-P-B2.equal_fold.MAE"
_PB_WIS = "cp16.uncertainty.V2-P-B2.equal_fold.WIS"

#: The generation the headline is about, and the one it was compared with, read from the registry
#: when this module loads: no template types "the latest research model" (standard §5).
_CUR = G.current_generation()
_CMP = G.get(_CUR.comparator)

BLOCKS: tuple[Block, ...] = (
    # ---- the terms the headline introduces, directly below it (standard §1 ii, §3.1) ----------------
    _block("terms.error_scores", "P21", """**Error scores:** error relative to a simple naive forecast, averaged over the
           test periods; lower is better.""", PAGE, README),
    _block("terms.targets", "P21", """**Accuracy targets:** set on {r:derived.rule.set_on}; the distances are point
           comparisons.""", PAGE, README),
    _block("terms.benchmark", "P21", """**{g:daily-lear.name}:** the strongest benchmark, a linear model refitted
           daily.""", PAGE, README),
    _block("terms.policies", "P21", """**Policies:** the models and variants tested.""", PAGE, README),
    _block("terms.class", "P21", """**{g:current.badge}:** development evidence, not a test on new data.""",
           PAGE, README),
    # ---- the comparison: the change against the comparator, and the main caveat (§1 i) ---------------
    _block("comparison.finding", "P24", f"""{{g:{_CUR.id}.version}} against {{g:{_CMP.id}.version}}, as a share of
           {{g:{_CMP.id}.version}}'s error scores: {{r:derived.change.{_CUR.id}.S_MAE}}
           {{r:derived.change.{_CUR.id}.S_MAE|ci}} (point) and {{r:derived.change.{_CUR.id}.S_WIS}}
           {{r:derived.change.{_CUR.id}.S_WIS|ci}} (interval), with {{s:level:95%}} confidence intervals.""",
           PAGE, README),
    _block("comparison.caveat", "P24", """Development evidence, not a test on new data. Meeting the targets is a
           development diagnostic, not a product qualification.""", PAGE, README),
    _block("comparison.sub", "P07", """Seven policies · the same {r:cp20.metrics.B0.pooled.n_hours} historical hours ·
           error scores averaged with equal weight over five test periods · lower is better"""),
    _block("comparison.howto", "C68", """Each score divides a model's error by that of a simple similar-day forecast in the
           same period, which therefore scores {r:cp20.metrics.B0.equal_fold.S_MAE|p=3}. The interval score accounts
           for both interval width and missed outcomes."""),
    _block("comparison.scale", "P26", f"""For scale, as mean absolute error per test period: {{g:{_CUR.id}.version}}
           {{r:derived.periods.{_CUR.id}.ordinary_low}}–{{r:derived.periods.{_CUR.id}.ordinary_high}} EUR/MWh in the
           four ordinary periods and {{r:derived.periods.{_CUR.id}.stress}} EUR/MWh in the {{s:date:2022}} crisis
           period; the similar-day naive {{r:derived.periods.naive.ordinary_low}}–{{r:derived.periods.naive.ordinary_high}}
           and {{r:derived.periods.naive.stress}} EUR/MWh. Context only: the error scores rank the policies.""",
           PAGE, README),
    _block("overview.v1pointer", "P09", """{g:v1.version} appears here as its development replay; its one-shot holdout
           results are in the {g:v1.version} chapter."""),
    _block("overview.fairness", "P08", """The five test periods are called folds below; the third covers the {s:date:2022}
           price crisis. These are development results, not a test on new data."""),
    # README-only: the page states the shared hours in the comparison's subtitle.
    _block("overview.fairness.readme", "P08", """Every policy was evaluated on the same {r:cp20.metrics.B0.pooled.n_hours}
           historical hours across five test periods (folds); the third covers the {s:date:2022} price crisis. Scores are
           normalized within each period, then averaged with equal weight. These are development results, not a test on
           new data.""", README),
    _block("overview.fairness.detail", "P08", """Paired intervals come from a moving-block bootstrap with seed
           {r:cp20.protocol.bootstrap_seed}, {r:cp20.protocol.replicates} replicates and
           {r:cp20.protocol.block_days}-day blocks, resampled identically for every policy. They are confidence
           intervals of an estimated difference, not forecast intervals."""),
    _block("overview.f07", "P09", """**Why {s:version:v1} scores {r:cp20.metrics.B1.equal_fold.S_MAE|p=3} in the shared
           development comparison but {r:cp2.dm_development.point_vs_naive.relative_improvement_pct|abs}% worse in its own
           report.** Both figures describe the same {r:cp2.dm_development.point_vs_naive.n_days} development days.
           {s:version:v1}'s report compared its daily absolute error with the raw similar-day naive (MAE
           {r:cp2.development_pooled_metrics.similar_day_naive.point.MAE} EUR/MWh) and pooled all days, so the
           {s:date:2022} crisis dominates. This comparison gives each of the five folds equal weight, and its naive
           reference is the forecast's emitted median after the common residual layer (MAE
           {r:cp20.metrics.B0.pooled.MAE} EUR/MWh). {s:version:v1}'s own error is {r:cp20.metrics.B1.pooled.MAE} EUR/MWh
           in both. {s:version:v1}'s original nine-quantile pinball is a different score from the seven-quantile interval
           score used here.""", PAGE, README),
    _block("overview.definitions", "C68", """**The point-error score (S_MAE)** is the mean over the five historical test
           periods (folds) of a policy's MAE divided by the similar-day naive's MAE in the same period; **the interval
           score (S_WIS)** does the same for the weighted interval score, which rewards narrow intervals and penalizes
           missed outcomes. MAE uses the emitted median."""),
    # ---- the v3 chapter (the chapter grammar, standard §6) ------------------------------------------
    _block("v3.question", "P29", """Do weather forecasts available before the auction improve {g:v2.version}?"""),
    # README-only: the page shows the inputs in its feature diagram, beside a one-line summary.
    _block("v3.change", "C65", """{g:v2.version} used price history, the load forecast and calendar inputs.
           {g:v3.version} added forecast wind speed and solar radiation available before the auction, while keeping the
           same underlying modeling setup for the comparison.""", README),
    _block("v3.change.short", "C65", """{g:v3.version} adds weather forecasts available before the auction to
           {g:v2.version}'s inputs; the modelling setup is otherwise unchanged."""),
    _block("v3.chart_headline", "C71", """Weather inputs lowered both error scores against {g:v2.version}."""),
    _block("v3.reading", "P30", """Both confidence intervals lie below zero and every test period favours
           {g:v3.version}; its prediction intervals are narrower in every period, with pooled {s:level:95%} coverage
           slightly lower, {r:cp20.metrics.HG.pooled.coverage95} against {r:cp20.metrics.H0.pooled.coverage95}.""",
           PAGE, README),
    # README-only: the page shows these differences once, in the main chart and its table.
    _block("v3.outcome.head", "C69", """Difference in error score ({s:version:v3} − {s:version:v2}), with {s:level:95%}
           confidence intervals. Below zero favours {s:version:v3}.""", README),
    _block("v3.outcome.mae", "C69", """Point-error score: {r:%s} {r:%s|ci}""" % (_HG_MAE, _HG_MAE), README),
    _block("v3.outcome.wis", "C70", """Interval score: {r:%s} {r:%s|ci}""" % (_HG_WIS, _HG_WIS), README),
    _block("v3.caveat.bundle", "C83", """**Which weather feature drives the gain.** The three were evaluated together, so
           no single feature's contribution is isolated.""", PAGE, README),
    _block("v3.caveat.fold3", "C73", """**A point-error gain within the {s:date:2022} crisis period on its own.** There
           its confidence interval crosses zero: {r:cp20.uncertainty.HG-H0.fold_3.MAE|p=1}
           {r:cp20.uncertainty.HG-H0.fold_3.MAE|ci1} EUR/MWh.""", PAGE, README),
    _block("v3.caveat.class", "C84", """**Performance on new data.** This is development evidence, not a test on new
           data.""", PAGE, README),
    _block("v3.decision", "C95", """{g:v3.status} It met the joint improvement rule against {g:v2.version} and both
           accuracy targets.""", PAGE, README),
    _block("v3.criteria", "C78", """As a diagnostic, {s:version:v3} is the first policy evaluated against the original
           criteria to meet all six; {s:version:v2} misses criteria {s:criterion:1} and {s:criterion:2}. This is a
           development diagnostic, not a product qualification."""),
    _block("v3.helps", "C79", """**During the {s:date:2022} price peak**, a {r:cp20.diagnostics.HG.peak.n_days}-day
           window inside the crisis period, MAE went from {r:cp20.criteria.H0.c4.peak.MAE|p=1} to
           {r:cp20.criteria.HG.c4.peak.MAE|p=1} EUR/MWh. Descriptive only; the hours inside the interval are in the
           chart."""),
    _block("v3.hurts", "C80", """The prediction intervals are narrower in every period, while pooled {s:level:95%}
           coverage is slightly lower, {r:cp20.metrics.HG.pooled.coverage95} against
           {r:cp20.metrics.H0.pooled.coverage95} for {s:version:v2}."""),
    _block("v3.recipe", "C66", """Operational NCEP GFS {s:grid:0.25°}, the {s:time:00 UTC} run of the
           day before delivery. Wind components are interpolated to each delivery hour; wind speed is
           computed per grid cell before a cos(latitude)-weighted average over the fixed box
           {s:coordinates:47–55.25°N, 5.5–15.5°E}; radiation is de-averaged from the forecast's running
           means. Each feature has a missing indicator. A regional weather proxy: not the DE-LU zone's exact
           outline and not a generation forecast."""),
    _block("v3.missing", "C67", """Only delivery {s:date:2019-01-01} has no weather, structurally: its
           run would be {s:date:2018-12-31}, before the input floor. Nothing was imputed from a failed
           retrieval."""),
    _block("v3.availability", "C85", """Availability of each run before the {s:time:D−1 11:00 UTC}
           forecast origin is reconstructed from dated NCEP production records with an assumed
           dissemination lag. It is not a per-day delivery guarantee."""),
    _block("v3.controls", "C89", """Frozen causal controls ran on {s:date:2020-07-01} and
           {s:date:2025-05-01}: masking the delivery day or the future changed the forecast by exactly
           zero, an available day-before price change moved it, and future weather changed
           nothing."""),
    _block("v3.controls.supplement", "C90", """One frozen check could not fail: multiplying all
           weather by a constant is undone by the training-only scaler. It was kept as an invariance
           check, and two controls that can fail were added, a shift of the target day's weather and a
           permutation of the training weather. Both passed (repair {s:repair:r13})."""),
    _block("v3.review", "C91", """The first independent Integration review within this project's
           process failed: one frozen input's recorded hash described its bytes with Windows line
           endings, so the reproduction commands refused to run in a clean checkout. The bytes were
           restored to the recorded identity (repair {s:repair:r14}) and a fresh Integration review
           passed."""),
    _block("v3.cost", "C92", """{r:cp20.extraction.complete_runs} GFS runs and
           {r:cp20.extraction.target_messages} decoded messages; {r:cp20.resources.transfer_gib} GiB
           transferred; {r:cp20.resources.machine_hours} machine-hours; external cost
           ${r:cp20.resources.external_cost_usd}."""),
    _block("v3.dependency", "C93", """{s:version:v3} needs one GFS retrieval per delivery day."""),
    # ---- the v2 chapter ------------------------------------------------------------------------------
    _block("v2.question", "P29", """Could a different forecasting model repair {g:v1.version}'s failure in the
           {s:date:2022} crisis?"""),
    _block("v2.problem", "C53", """{s:version:v1} substantially underestimated prices during the
           {s:date:2022} crisis. Recalibrating its intervals improved coverage, but the improvement was
           insufficient."""),
    _block("v2.change", "C10", """{g:v2.version} combines two LEAR forecasts (LEAR: a regularized linear model fitted for
           each hour) with intervals that account for the hour of the day. A control uses the same blend with pooled
           intervals, so the interval methods can be compared.""", PAGE, README),
    _block("v2.chart_headline", "C37", """{g:v2.version} lowered both error scores against {g:daily-lear.inline}."""),
    _block("v2.reading", "C34", """Against {g:daily-lear.inline} both confidence intervals lie below zero; against its
           pooled-interval control only the interval score improved, and the point-error interval ends just above
           zero, at {r:%s|hi}: not equivalence.""" % _HP_MAE),
    _block("v2.caveat.attribution", "C41", """**That hour-aware intervals caused the gain over
           {g:daily-lear.inline}.** The pooled-interval control also passes the per-period criterion.""", PAGE, README),
    _block("v2.caveat.split", "C41", """**How the gain splits between the blend and the interval layer.** The experiment
           does not separate them.""", PAGE, README),
    _block("v2.caveat.class", "P31", """**Performance on new data.** This is development evidence, not a test on new
           data.""", PAGE, README),
    _block("v2.decision", "P32", """{g:v2.status} {g:v3.version} was built on it.""", PAGE, README),
    # README-only: the page states these in its reading and carries them in the chart and table.
    _block("v2.result.hb2", "C37", """Against {g:daily-lear.inline} ({s:version:v2} − {g:daily-lear.inline}),
           {s:version:v2} meets the joint improvement rule as exploratory evidence: point-error score difference
           {r:%s} {r:%s|ci}, interval-score difference {r:%s} {r:%s|ci}.""" % (_HB_MAE, _HB_MAE, _HB_WIS, _HB_WIS),
           README),
    _block("v2.result.hp", "C34", """Against its pooled-interval control ({s:version:v2} − control), there is
           **no demonstrated joint preference**: the interval-score difference is {r:%s} {r:%s|ci}, but the
           point-error difference's interval ends just above zero, {r:%s} [{r:%s|lo}, {r:%s|hi}]. This is
           not equivalence.""" % (_HP_WIS, _HP_WIS, _HP_MAE, _HP_MAE, _HP_MAE), README),
    _block("v2.result.pb2", "C38", """The pooled-interval control against {g:daily-lear.inline} does not meet the rule:
           its interval-score interval, {r:%s|ci}, spans zero.""" % _PB_WIS),
    _block("v2.result.criteria", "C39", """Both {s:version:v2} arms miss criteria {s:criterion:1–2}, the
           point-error and interval-score thresholds, and meet criteria {s:criterion:3–6}."""),
    # ---- the branch cards (standard §6) ------------------------------------------------------------
    _block("branch.calibration.question", "P27", """Could recalibrating {g:v1.version}, without refitting it, repair its
           coverage in the {s:date:2022} crisis?""", PAGE, README),
    _block("branch.calibration.result", "P12", """Against {g:v1.version}, on the matched crisis window: the hours inside
           the {s:level:95%} interval rose from {r:cp10.peak_windows.v1_reference.covered_95} to
           {r:cp10.peak_windows.c1_price_volatility.covered_95} of {r:cp10.peak_windows.c1_price_volatility.n_obs}.""",
           PAGE, README),
    _block("branch.calibration.reason", "P27", """Recalibration alone was not enough: the model itself had to adapt.""",
           PAGE, README),
    _block("branch.model-comparison.question", "P27", """Which forecasting approach copes best with the {s:date:2022}
           crisis?""", PAGE, README),
    _block("branch.model-comparison.result", "C21", """Nine policies on the same hours, none meeting the product
           criteria. {g:normalized-lear.name} cut crisis-window MAE to {r:cp15.peak.A1.MAE|p=1} EUR/MWh, but
           {g:daily-lear.inline} kept the better error scores: {r:cp15.relative_scores.B2.S_MAE|p=3} and
           {r:cp15.relative_scores.B2.S_WIS|p=3} against {r:cp15.relative_scores.A1.S_MAE|p=3} and
           {r:cp15.relative_scores.A1.S_WIS|p=3}.""", PAGE, README),
    _block("branch.model-comparison.reason", "P27", """No policy met the criteria; the study informed {g:v2.version}'s
           blend of two LEAR forecasts.""", PAGE, README),
    # ---- the v1 chapter (standard §4; its archive is preserved as published) ------------------------
    _block("v1.what", "P11", """A LightGBM ensemble forecasting nine quantiles for every hour, calibrated
           into {s:level:50 / 80 / 95%} prediction intervals, and shipped exactly as it was evaluated.""", PAGE, README),
    _block("v1.holdout", "P11", """On its pre-specified {v1:holdout_days}-day holdout, {s:version:v1} beat the
           similar-day naive: MAE {v1:holdout_mae_champion|p=1} against {v1:holdout_mae_naive|p=1} EUR/MWh, and mean
           pinball loss {v1:holdout_pinball_champion|p=1} against {v1:holdout_pinball_naive|p=1} EUR/MWh. A one-sided
           Diebold–Mariano test on the daily pinball-loss vectors gave {v1:holdout_dm_p_value|pfloor}; it tests the
           probabilistic forecast, not the MAE difference.""", PAGE, README),
    _block("v1.unflattering", "P11", """**Where it falls short.** On the development folds its point
           error is {v1:development_dm_point_relative} than the naive's, pooled over all days (a one-sided test
           for an improvement gives p = {v1:development_dm_point_p_value}: no evidence of an advantage). Over the
           August {s:date:2022} peak weeks its {s:level:95%} interval covered {r:cp15.peak.B1.coverage95|p=3}
           of outcomes.""", PAGE, README),
    _block("v1.lesson", "P11", """**Why:** its crisis errors were about price level, not shape. On the
           crisis window the bias was {r:cp15.peak.B1.bias|p=1} EUR/MWh, and the daily mean-level error was
           {r:cp15.peak.B1.daily_mean_level_MAE|p=1} EUR/MWh against a within-day shape error of
           {r:cp15.peak.B1.within_day_shape_MAE|p=1} EUR/MWh.""", PAGE, README),
)

BLOCKS_BY_KEY: dict[str, Block] = {block.key: block for block in BLOCKS}

#: Chart claims: the records each figure may plot, beyond those its caption names.
CHART_CLAIMS: dict[str, str] = {
    "overview": "P07",
    "v3.c2a": "C69",
    "v3.c2b": "C72",
    "v3.c3": "C74",
    "v3.c4": "C79",
    "v3.c5": "C82",
    "v3.c6": "C80",
    "v2.chart1": "C31",
    "v2.chart2": "C37",
    "preview": "P05",
    "targets": "P25",
}

#: Claims bound outside a block: single chart rows where a chart mixes claims (v2's three
#: contrasts), the target verdicts in the comparison, and the demo's startup figure (P13).
ROW_CLAIMS: tuple[str, ...] = ("C33", "C34", "C38", "C70", "P13", "P16", "P20", "P22", "P23", "P28")

#: README research blocks (plan §9.4), each rendered from the same template as the page.
README_BLOCKS: tuple[str, ...] = tuple(block.key for block in BLOCKS if README in block.surfaces)

#: Records shown in full wherever they appear in a value table (standard §4; plan §6 invariant 9 as amended).
EXACT_FIELDS: set[tuple[str, str]] = set()


# --------------------------------------------------------------------------- the headline (standard §3.4)


def headline_template(entry: G.Entry | None = None) -> tuple[str, str]:
    """(claim, template) of the headline block, generated from the registry's current generation and
    its derived records. It leads with the pre-specified verdict when a rule existed (§3.3 a), and with
    the change against the comparator otherwise (§3.3 b)."""
    entry = entry or G.current_generation()
    verdict_id = f"derived.criteria.{entry.id}.verdict"
    if "criteria-1-2" in entry.rules and verdict_id in D.records():
        margins = {D.get(f"derived.rule.margin.{score}").value for score in ("S_MAE", "S_WIS")}
        if len({D.display(D.get(f"derived.rule.margin.{s}")) for s in ("S_MAE", "S_WIS")}) != 1:
            raise ClaimError(f"the two targets' margins differ: {sorted(margins)}")
        benchmark = D.get("derived.rule.margin.S_MAE").subject
        base = f"derived.criteria.{entry.id}"
        if D.get(f"{base}.verdict").value == "met":
            first = D.get(f"{base}.first_to_meet").value == "yes"
            tail = ("the first of {r:%s.tested} policies tested to meet them" % base if first
                    else "one of the {r:%s.tested} policies tested against them" % base)
            template = (
                "Met both accuracy targets set before the experiments: error scores at least "
                "{r:derived.rule.margin.S_MAE} below the strongest benchmark, {g:%s.inline} "
                "({g:%s.version}: {r:%s.distance.S_MAE|abs} and {r:%s.distance.S_WIS|abs} below; %s)."
                % (benchmark, entry.id, base, base, tail))
        else:
            template = (
                "Did not meet the accuracy targets set before the experiments: error scores at least "
                "{r:derived.rule.margin.S_MAE} below the strongest benchmark, {g:%s.inline} "
                "({g:%s.version}: {r:%s.distance.S_MAE} and {r:%s.distance.S_WIS} against it; "
                "{r:%s.tested} policies tested)." % (benchmark, entry.id, base, base, base))
        return "P20", template
    change = f"derived.change.{entry.id}"
    comparator = G.get(entry.comparator)
    return "P20", (
        "Against {g:%s.version}, the error scores changed by {r:%s.S_MAE} {r:%s.S_MAE|ci} and "
        "{r:%s.S_WIS} {r:%s.S_WIS|ci}, as a share of {g:%s.version}'s score."
        % (comparator.id, change, change, change, change, comparator.id))


def target_sentence(target: str = "html") -> str:
    """The target line in words, with its date, and N (standard §15 amending plan §8.2): what the
    comparison's dashed lines mark, how many policies were tested against it and who met it."""
    entry = G.current_generation()
    base = f"derived.criteria.{entry.id}"
    benchmark = D.get("derived.rule.margin.S_MAE").subject
    template = ("The dashed lines mark the targets: each error score at least {r:derived.rule.margin.S_MAE} below "
                "the strongest benchmark, {g:%s.inline} (set {r:derived.rule.set_on}). {r:%s.tested} policies were "
                "tested against them; " % (benchmark, base))
    met = [record.subject for record in D.records().values() if record.kind == "verdict" and record.value == "met"]
    if D.get(f"{base}.verdict").value == "met" and D.get(f"{base}.first_to_meet").value == "yes" and met == [entry.id]:
        template += "{g:%s.version} met both, the first and only one to do so." % entry.id
    elif D.get(f"{base}.verdict").value == "met":
        template += "{g:%s.version} met both." % entry.id
    else:
        template += "{g:%s.version} did not meet them." % entry.id
    return render_template("P25", template, target)


def headline(target: str = "html") -> str:
    """The headline block: one sentence plus the evidence-class badge, identical on the page and in
    the README (§3.4)."""
    claim_id, template = headline_template()
    sentence = render_template(claim_id, template, target)
    badge = G.current_generation().badge
    if target == "md":
        return f"{sentence} `{badge}`"
    return f'{sentence} <span class="badge badge-development">{html.escape(badge)}</span>'


# --------------------------------------------------------------------------- rendering

_TOKEN = re.compile(r"\{(r|s|g|v1):([^{}]+)\}")
_RECORD_TOKEN = re.compile(r"\{r:([^|{}]+)(?:\|[^{}]*)?\}")
_BOLD = re.compile(r"\*\*(.+?)\*\*")
_CODE = re.compile(r"`([^`]+)`")


class ClaimError(ValueError):
    """A template, binding or rendering request that the claim layer refuses."""


def _html_value(claim_id: str, record_id: str, which: str, text: str, raw: str) -> str:
    field = "" if which == "value" else f' data-field="{which}"'
    return (
        f'<data value="{html.escape(raw)}" data-claim="{claim_id}" data-record="{record_id}"{field}>'
        f"{html.escape(text)}</data>"
    )


def structural(kind: str, text: str, target: str = "html") -> str:
    """A declared structural numeral: labels, dates, fold indices, control values."""
    if target == "md":
        return text
    return f'<span data-structural="{html.escape(kind)}">{html.escape(text)}</span>'


def _value_text(record: R.EvidenceRecord, which: str, option: str | None) -> str:
    if (record.record_id, which) in EXACT_FIELDS or option == "exact":
        return R.display(record, which, style="exact")
    if option == "pct":
        return R.display(record, which, style="percent")
    if option and option.startswith("p="):
        return R.display(record, which, precision=int(option[2:]))
    if option == "abs":
        text = R.display(record, which)
        return text.lstrip("+" + R.MINUS)
    return R.display(record, which)


def _render_derived(claim_id: str, record_id: str, option: str | None, target: str) -> str:
    """A typed derived record (standard §3.3) in HTML or Markdown: whole percent, one decimal for
    EUR/MWh, the word itself for a label or a date. It carries `data-derived` beside its claim."""
    record = D.get(record_id)

    def one(which: str, style: str | None) -> str:
        text = D.display(record, which, style=style)
        raw = {"value": record.value, "ci_low": record.ci_low, "ci_high": record.ci_high}[which]
        if target == "md":
            return text
        field = "" if which == "value" else f' data-field="{which}"'
        return (f'<data value="{html.escape(raw)}" data-claim="{claim_id}" data-record="{record_id}" '
                f'data-derived="{record.kind}"{field}>{html.escape(text)}</data>')

    if option == "ci":
        if not record.interval:
            raise ClaimError(f"{record_id} has no interval")
        return f"[{one('ci_low', None)}, {one('ci_high', None)}]"
    if option in ("lo", "hi"):
        return one("ci_low" if option == "lo" else "ci_high", None)
    return one("value", option if option in ("abs", "exact") else None)


def _render_record(claim_id: str, spec: str, target: str) -> str:
    record_id, _, option = spec.partition("|")
    option = option or None
    if D.is_derived(record_id):
        return _render_derived(claim_id, record_id, option, target)
    record = R.get(record_id)

    def one(which: str, opt: str | None) -> str:
        text = _value_text(record, which, opt)
        raw = {"value": record.raw, "ci_low": record.ci_low_raw, "ci_high": record.ci_high_raw}[which]
        return text if target == "md" else _html_value(claim_id, record_id, which, text, raw)

    if option in ("ci", "ci1", "ciexact"):
        if record.interval is None:
            raise ClaimError(f"{record_id} has no interval")
        places = {"ci1": "p=1", "ciexact": "exact"}.get(option)
        return f"[{one('ci_low', places)}, {one('ci_high', places)}]"
    if option == "lo":
        return one("ci_low", None)
    if option == "hi":
        return one("ci_high", None)
    if option == "exact_hi":
        return one("ci_high", "exact")
    return one("value", option)


#: The p-value floor on the reading path (standard §4): below it, "p < 10⁻⁶"; the exact value stays
#: in the value table.
P_FLOOR = 1e-6
P_FLOOR_TEXT = "p < 10⁻⁶"


def v1_display(key: str, option: str | None = None) -> str:
    """A v1 claim as the reading path shows it: `p=N` rounds to N decimals (standard §4), `pfloor`
    floors a p-value at 10⁻⁶. With no option it is the claim set's own string."""
    from .claims import build_claims

    text = build_claims()[key]
    if option and option.startswith("p="):
        return f"{float(text):.{int(option[2:])}f}".replace("-", R.MINUS)
    if option == "pfloor":
        return P_FLOOR_TEXT if float(text) < P_FLOOR else f"p = {text}"
    return text


def _v1(claim_id: str, spec: str, target: str) -> str:
    from .claims import build_claims

    key, _, option = spec.partition("|")
    raw = build_claims()[key]
    text = v1_display(key, option or None)
    if target == "md":
        return text
    shown = f' data-display="{html.escape(option)}"' if option else ""
    return (
        f'<data value="{html.escape(raw)}" data-claim="{claim_id}" data-v1="{key}"{shown}>'
        f"{html.escape(text)}</data>"
    )


def _structural_name(name: str, target: str) -> str:
    """A registry name with its version label declared structural: 'v3 · weather features'."""
    match = re.match(r"^(v\d+)( · .*)$", name)
    if target == "md" or match is None:
        return name if target == "md" else html.escape(name)
    return structural("version", match.group(1)) + html.escape(match.group(2))


def _registry(spec: str, target: str) -> str:
    """A registry token (standard §5): a name, version, badge or dated status, never typed in a template.

    `{g:ID.name}`, `{g:ID.inline}`, `{g:ID.version}`, `{g:ID.badge}`, `{g:ID.adoption}`,
    `{g:ID.status}` and `{g:release_rule}`; `ID` may be `current` or `released`."""
    if spec == "release_rule":
        sentence = G.release_sentence()
        if target == "md":
            return sentence
        version = G.released().version
        body = html.escape(sentence).replace(f" {version}.", " " + structural("version", version) + ".", 1)
        return f'<span data-status="release-rule">{body}</span>'
    ident, _, attribute = spec.partition(".")
    entry = G.resolve(ident)
    if attribute in ("name", "inline"):
        name = entry.name if attribute == "name" else G.inline_name(entry)
        text = _structural_name(name, target)
        return text if target == "md" else f'<span data-registry="{entry.id}">{text}</span>'
    if attribute == "version":
        if entry.version is None:
            raise ClaimError(f"{entry.id} has no version")
        return structural("version", entry.version, target)
    if attribute == "badge":
        return entry.badge if target == "md" else html.escape(entry.badge)
    if attribute == "adoption":
        return G.adoption_label(entry) if target == "md" else html.escape(G.adoption_label(entry))
    if attribute == "status":
        sentence = G.status_sentence(entry)
        if target == "md":
            return sentence
        month = G.month(entry.status.date)
        body = html.escape(sentence).replace(month, structural("date", month), 1)
        if entry.version:
            body = body.replace(f" {entry.version} ", " " + structural("version", entry.version) + " ", 1)
        return f'<span data-status="{entry.id}">{body}</span>'
    raise ClaimError(f"unknown registry token {spec!r}")


def render_template(claim_id: str, template: str, target: str = "html") -> str:
    """Render one template to HTML or Markdown. Every number comes from a record or a declared
    structural token; everything else is escaped text."""
    if target not in ("html", "md"):
        raise ClaimError(f"unknown target {target!r}")
    out, position = [], 0
    for match in _TOKEN.finditer(template):
        literal = template[position:match.start()]
        out.append(literal if target == "md" else html.escape(literal, quote=False))
        kind, body = match.groups()
        if kind == "r":
            out.append(_render_record(claim_id, body, target))
        elif kind == "s":
            structural_kind, _, text = body.partition(":")
            out.append(structural(structural_kind, text, target))
        elif kind == "g":
            out.append(_registry(body, target))
        else:
            out.append(_v1(claim_id, body, target))
        position = match.end()
    tail = template[position:]
    out.append(tail if target == "md" else html.escape(tail, quote=False))
    text = "".join(out)
    if target == "html":
        text = _BOLD.sub(r"<strong>\1</strong>", text)
        text = _CODE.sub(r"<code>\1</code>", text)
    return text


def render(key: str, target: str = "html", *, surface: str = PAGE) -> str:
    """Render a published block for a surface; a withheld or off-surface block is refused."""
    block = BLOCKS_BY_KEY.get(key)
    if block is None:
        raise ClaimError(f"no block {key!r}")
    if block.status != "published":
        raise ClaimError(f"block {key!r} is {block.status}")
    if surface not in block.surfaces:
        raise ClaimError(f"block {key!r} may not appear on the {surface}")
    return render_template(block.claim_id, block.template, target)


def svg_binding(claim_id: str, record_id: str, which: str = "value") -> str:
    """The attributes an SVG `<text>` or mark carries for a research value (no `<data>` in SVG)."""
    if claim_id not in all_claim_ids():
        raise ClaimError(f"unknown claim {claim_id!r}")
    if D.is_derived(record_id):
        record = D.get(record_id)
        field = "" if which == "value" else f' data-field="{which}"'
        return f' data-claim="{claim_id}" data-record="{record_id}" data-derived="{record.kind}"{field}'
    R.get(record_id)
    field = "" if which == "value" else f' data-field="{which}"'
    return f' data-claim="{claim_id}" data-record="{record_id}"{field}'


def svg_value(record_id: str, which: str = "value", option: str | None = None) -> str:
    if D.is_derived(record_id):
        return D.display(D.get(record_id), which, style="abs" if option == "abs" else None)
    return _value_text(R.get(record_id), which, option)


# --------------------------------------------------------------------------- the maps


def all_claim_ids() -> set[str]:
    return {block.claim_id for block in BLOCKS} | set(CHART_CLAIMS.values()) | set(ROW_CLAIMS)


_MAP_ID = re.compile(r"^\|\s*((?:C|P|W)\d+)\s*\|", re.MULTILINE)


def claim_map_ids() -> set[str]:
    """Every claim ID defined in a claim map's tables."""
    found: set[str] = set()
    for path in CLAIM_MAPS:
        found |= set(_MAP_ID.findall(path.read_text()))
    return found


# --------------------------------------------------------------------------- phrase guards

#: Withheld claims (W1–W21) as phrases a surface must not contain. Each is written to catch the
#: claim, not an honest denial of it; `tests/test_30_research_claims_rendered.py` pins both.
WITHHELD_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = tuple(
    (wid, re.compile(pattern, re.IGNORECASE))
    for wid, pattern in (
        ("W1", r"\b(hour-aware intervals?|V2-H|H) (are|is) (better|preferred)\b"),
        ("W2", r"\b(H and P are equivalent|hour awareness has no effect)\b"),
        ("W3", r"\+?0\.0000\]|≈\s?0\b"),
        ("W4", r"hour-aware intervals fixed criterion"),
        ("W5", r"\bthe blend alone fixed\b"),
        ("W6", r"\b(product[- ]ready|production[- ]ready|qualified for production|promoted to production)\b"),
        ("W7", r"\bstatistically significant|significantly (beats|better|outperform)"),
        ("W8", r"\b(revenue|battery gain|annuali[sz]ed (value|gain|revenue))\b"),
        ("W9", r"\bbetter (solar|night|shoulder)[- ]hour\b"),
        ("W11", r"\bA1 beats B2\b"),
        ("W14", r"\b(Chronos-2|TabPFN|DDNN|VRE) (outperforms|beats|improves)\b"),
        ("W15", r"(?<!no )(?<!no conformal )\bcoverage guarantee\b|\bguaranteed coverage\b"),
        ("W17", r"\b(wind|radiation|solar)[^.]{0,40}\b(drives|explains|is responsible for) the (gain|improvement)\b"),
        ("W18", r"\bpeer[- ]review|external validation|externally validated\b"),
        ("W19", r"\b(v3 runs in|runs v3|try the v3|v3 demo|live v3)\b"),
        # A nominal interval level ("the 95% interval") is not a relative gain.
        ("W20", r"\bv3\b[^.]{0,60}\b\d+(\.\d+)?\s?(%(?!\s+(prediction |confidence )?interval)|x\b|times\b)[^.]{0,30}\bv1\b"),
        ("W21", r"(?<!never )(?<!not )\bconfirmatory\b(?!-style)"),
    )
)

#: Stale status text the reconciliation removes (plan §8.7). The phrase guard runs on every
#: public surface, including the archived v1 report and the Space cards.
STALE_PHRASES: tuple[str, ...] = (
    "delu-m4",
    "No v2 run exists yet",
    "When M4 is ratified",
    "the defect the planned v2 targets",
    "the planned v2",
    "Development update · 2026-09-16",
    "CP-16 needs a complete new acceptance bar",
    "CP-16 requires a complete acceptance bar",
    "Current development — 2026-09-16",
)


#: Absolute network and hosting claims that are not true as stated (final audit F07): opening the
#: report still downloads it, independence from a CDN after loading is not an availability guarantee,
#: and the Space is hosted. Checked on the active surfaces; v1's preserved archive keeps its history.
NETWORK_ABSOLUTES: tuple[str, ...] = (
    "fetches nothing",
    "fetches **nothing**",
    "without any download",
    "cannot fail when a CDN",
    "no server;",
    "there is no server",
    "instant report",
)


def network_absolute_findings(text: str) -> list[str]:
    lowered = text.lower()
    return [phrase for phrase in NETWORK_ABSOLUTES if phrase.lower() in lowered]


def withheld_findings(text: str) -> list[str]:
    """Withheld claims found in `text`, as `W<n>: <match>`."""
    flat = " ".join(text.split())
    return [f"{wid}: {match.group(0)!r}" for wid, pattern in WITHHELD_PATTERNS for match in pattern.finditer(flat)]


def stale_findings(text: str) -> list[str]:
    flat = " ".join(text.split())
    return [phrase for phrase in STALE_PHRASES if phrase in flat]


__all__ = [
    "ADOPTED",
    "BADGE_DEVELOPMENT",
    "BADGE_PROSPECTIVE",
    "BADGE_V1_HOLDOUT",
    "BLOCKS",
    "BLOCKS_BY_KEY",
    "Block",
    "CHART_CLAIMS",
    "CLAIM_MAPS",
    "CONTRIBUTION_STATEMENT",
    "ClaimError",
    "OWNER_PUBLIC_NAME",
    "EXACT_FIELDS",
    "NOT_ADOPTED",
    "PLANNED",
    "README_BLOCKS",
    "STALE_PHRASES",
    "WITHHELD_PATTERNS",
    "all_claim_ids",
    "claim_map_ids",
    "render",
    "render_template",
    "stale_findings",
    "structural",
    "target_sentence",
    "headline",
    "headline_template",
    "svg_binding",
    "svg_value",
    "withheld_findings",
]
