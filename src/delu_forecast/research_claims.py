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

from . import research as R

REPO_ROOT = R.REPO_ROOT
CLAIM_MAPS = (
    REPO_ROOT / "docs" / "track-b" / "research-content" / "cp15-cp16-claims.md",
    REPO_ROOT / "docs" / "track-b" / "research-content" / "cp20-claims.md",
)

# --------------------------------------------------------------------------- names and labels

#: Plain names first; codes are secondary metadata (plan §7.1, Appendix A).
POLICY_NAMES: dict[str, str] = {
    "HG": "v3 · weather features",
    "H0": "v2 · blended LEAR, hour-aware intervals",
    "V2-H": "v2 · blended LEAR, hour-aware intervals",
    "V2-P": "v2 control · pooled intervals",
    "B0": "Similar-day naive",
    "B1": "v1 · released LightGBM",
    "B2": "Daily LEAR",
    "B3": "Daily LightGBM",
    "A1": "Normalized LEAR",
    "A2": "Normalized LightGBM",
    "A3": "Normalized component mean",
    "A4": "84-day normalized LEAR",
    "A5": "Normalized component mean, variant",
}

#: The role each policy plays in a comparison: a generation, a reference or a study arm.
POLICY_ROLES: dict[str, str] = {
    "HG": "generation", "H0": "generation", "V2-H": "generation", "B1": "generation",
    "B0": "reference", "B2": "reference", "B3": "reference",
    "A1": "study", "A2": "study", "A3": "study", "A4": "study", "A5": "study", "V2-P": "control",
}

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
CONTRIBUTION_STATEMENT = (
    "I led this project, from defining the problem and the success criteria to the decisions on "
    "the research direction and on how the product is presented. The work was carried out with "
    "the help of AI agents for writing code, analysis and documentation, in a process that "
    "included automated tests and reviews kept separate from the execution. Responsibility for "
    "adoption decisions, for approving the deliverables and for publication was mine."
)

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

BLOCKS: tuple[Block, ...] = (
    # ---- opening -------------------------------------------------------------
    _block("opening.summary", "P04",
           """Latest research result: {s:version:v3} minus {s:version:v2} in point error, each measured as a
           ratio to a simple similar-day forecast on the same historical hours: {r:%s} {r:%s|ci}; negative
           favours {s:version:v3}. Development evidence on known historical periods, not yet a test on new
           data.""" % (_HG_MAE, _HG_MAE)),
    # ---- overview ------------------------------------------------------------
    _block("overview.finding", "P07",
           """{s:version:v3}'s equal-fold point error is {r:cp20.metrics.HG.equal_fold.S_MAE} and its
           interval score {r:cp20.metrics.HG.equal_fold.S_WIS} times the similar-day naive's, the
           lowest of the seven policies. {s:version:v1}'s development replay scores
           {r:cp20.metrics.B1.equal_fold.S_MAE} and {r:cp20.metrics.B1.equal_fold.S_WIS}."""),
    _block("overview.qualification", "P07",
           """These are development results after selection: the folds are known historical periods,
           and the dashed limits are the plan's diagnostic criteria {s:criterion:1–2}
           ({r:cp20.criteria.HG.c1.equal_fold.S_MAE.upper_limit} and
           {r:cp20.criteria.HG.c2.equal_fold.S_WIS.upper_limit}), not a certification."""),
    _block("overview.fairness", "P08",
           """Every policy is scored on the same {r:cp20.metrics.B0.pooled.n_hours} hours over
           {r:cp20.metrics.B0.pooled.n_days} delivery days in five folds. Each fold counts equally, so
           the {s:date:2022} crisis fold is not diluted by the calmer ones, and every score is a ratio
           to the similar-day naive on the same fold."""),
    _block("overview.fairness.detail", "P08",
           """Paired intervals come from a moving-block bootstrap with seed
           {r:cp20.protocol.bootstrap_seed}, {r:cp20.protocol.replicates} replicates and
           {r:cp20.protocol.block_days}-day blocks, resampled identically for every policy. They are
           confidence intervals of an estimated difference, not forecast intervals."""),
    _block("overview.f07", "P09",
           """**Why {s:version:v1} scores {r:cp20.metrics.B1.equal_fold.S_MAE} here but
           {r:cp2.dm_development.point_vs_naive.relative_improvement_pct|abs}% worse in its own
           report.** Both figures describe the same {r:cp2.dm_development.point_vs_naive.n_days}
           development days. {s:version:v1}'s report compared its daily absolute error with the raw
           similar-day naive (MAE {r:cp2.development_pooled_metrics.similar_day_naive.point.MAE}
           EUR/MWh) and pooled all days, so the {s:date:2022} crisis dominates. This comparison gives
           each of the five folds equal weight, and its naive reference is the forecast's emitted
           median after the common residual layer (MAE {r:cp20.metrics.B0.pooled.MAE} EUR/MWh).
           {s:version:v1}'s own error is {r:cp20.metrics.B1.pooled.MAE} EUR/MWh in both.
           {s:version:v1}'s original
           nine-quantile pinball is a different score from the seven-quantile WIS used here."""),
    _block("overview.definitions", "C68",
           """**S_MAE** is the mean over the five folds of a policy's MAE divided by the similar-day
           naive's MAE on the same fold; **S_WIS** does the same for the weighted interval score,
           which rewards narrow intervals and penalizes missed outcomes. Lower is better for both, and
           the naive scores {r:cp20.metrics.B0.equal_fold.S_MAE} by definition. MAE uses the emitted
           median."""),
    # ---- v3 chapter ----------------------------------------------------------
    _block("v3.problem", "C95", """{s:version:v2} used market data only: prices, the load forecast and
           the calendar."""),
    _block("v3.hypothesis", "C95", """Forecast wind and solar drive both the level and the shape of
           the next day's prices, so a weather forecast available before the auction should improve
           point and interval forecasts together."""),
    _block("v3.change", "C65", """Three weather features from the day-before GFS forecast were appended
           to {s:version:v2}'s two component models, each with a missing indicator. The blend, the
           interval layer, the histories, the folds and the seed stayed exactly as in
           {s:version:v2}."""),
    # README-only: the page draws the same two values as outcome tiles.
    _block("v3.outcome.mae", "C69", """Normalized point error {r:%s} {r:%s|ci}""" % (_HG_MAE, _HG_MAE), "readme"),
    _block("v3.outcome.wis", "C70", """Normalized interval score {r:%s} {r:%s|ci}""" % (_HG_WIS, _HG_WIS), "readme"),
    _block("v3.result", "C71", """Both {s:level:95%} intervals lie wholly below zero, so the plan's joint
           improvement rule is met: an observed joint improvement over {s:version:v2}, development
           evidence after selection. All five folds favour {s:version:v3}."""),
    _block("v3.criteria", "C78", """As a diagnostic, {s:version:v3} is the first policy evaluated
           against the original criteria to meet all six; {s:version:v2} misses criteria
           {s:criterion:1} and {s:criterion:2}. This is a development diagnostic, not a product
           qualification."""),
    _block("v3.helps", "C79", """**Where it helps:** in the {s:date:2022} crisis window, MAE goes from
           {r:cp20.criteria.H0.c4.peak.MAE} to {r:cp20.criteria.HG.c4.peak.MAE} EUR/MWh, and the hours
           inside the {s:level:95%} interval from {r:cp20.diagnostics.H0.peak.hit_count95} to
           {r:cp20.diagnostics.HG.peak.hit_count95} of {r:cp20.diagnostics.HG.peak.n_hours}.
           Descriptive only: {r:cp20.diagnostics.HG.peak.n_days} days."""),
    _block("v3.hurts", "C80", """**What it gives up:** {s:version:v3}'s intervals are narrower in every
           fold, and in exchange its pooled {s:level:95%} coverage is slightly lower than {s:version:v2}'s,
           {r:cp20.metrics.HG.pooled.coverage95} against {r:cp20.metrics.H0.pooled.coverage95}."""),
    _block("v3.caveat.bundle", "C83", """**The gain belongs to the bundle.** The three features were
           added together, and no arm isolates wind at {s:height:10 m}, wind at {s:height:100 m} or
           radiation, so the improvement is not attributed to any one of them."""),
    _block("v3.caveat.fold3", "C73", """**In fold {s:fold:3}, the {s:date:2022} crisis, the MAE
           interval crosses zero:** {r:cp20.uncertainty.HG-H0.fold_3.MAE}
           {r:cp20.uncertainty.HG-H0.fold_3.MAE|ci} EUR/MWh."""),
    _block("v3.caveat.development", "C84", """**Development evidence.** The folds are known historical
           periods and the {s:date:2022} crisis motivated these hypotheses, so the results cannot
           become unseen evidence. No prospective clock has started."""),
    _block("v3.decision", "C95", """Adopted as the current research model, **{s:version:v3} · weather features**.
           Adopted means adopted within this research programme: {s:version:v3} does not run in the
           demo, and nothing here implies deployment or outside validation."""),
    _block("v3.recipe", "C66", """Operational NCEP GFS {s:grid:0.25°}, the {s:time:00 UTC} run of the
           day before delivery. Wind components are interpolated to each delivery hour; wind speed is
           computed per grid cell before a cos(latitude)-weighted average over the fixed box
           {s:coordinates:47–55.25°N, 5.5–15.5°E}; radiation is de-averaged from the forecast's running
           means. A regional weather proxy: not the DE-LU zone's exact outline and not a generation
           forecast."""),
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
    # ---- v2 chapter ----------------------------------------------------------
    _block("v2.problem", "C53", """{s:version:v1} collapsed in the {s:date:2022} crisis. In the crisis
           window its MAE was {r:cp15.peak.B1.MAE} EUR/MWh, and {r:cp15.peak.B1.hit_count95} of
           {r:cp15.peak.B1.n_hours} hours fell inside its {s:level:95%} interval."""),
    _block("v2.branch.cp10", "P12", """**First attempt, not adopted ({s:checkpoint:CP-10}).** Recalibrating
           {s:version:v1} without refitting it raised crisis-window {s:level:95%} coverage from
           {r:cp10.peak_windows.v1_reference.coverage_95|pct} to
           {r:cp10.peak_windows.c1_price_volatility.coverage_95|pct}. Not enough: the model itself
           had to adapt."""),
    _block("v2.branch.cp15", "C21", """**The study that informed {s:version:v2} ({s:checkpoint:CP-15}).** Nine policies
           were compared on the same hours. Normalized LEAR cut crisis-window MAE to
           {r:cp15.peak.A1.MAE} EUR/MWh, but no policy met the product criteria
           (`NOT_DEMONSTRATED`), and the daily LEAR reference had the better primary scores:
           {r:cp15.relative_scores.B2.S_MAE} and {r:cp15.relative_scores.B2.S_WIS} against
           {r:cp15.relative_scores.A1.S_MAE} and {r:cp15.relative_scores.A1.S_WIS}."""),
    _block("v2.change", "C10", """{s:version:v2} blends the two central forecasts {s:ratio:50/50} and adds
           hour-aware residual intervals (H). A control arm (P) keeps the same blend with pooled
           intervals, so H against P measures hour awareness alone."""),
    _block("v2.result.hb2", "C37", """Against the daily LEAR reference, {s:version:v2} meets the joint
           improvement rule as exploratory evidence: point error {r:%s} {r:%s|ci}, interval score
           {r:%s} {r:%s|ci}.""" % (_HB_MAE, _HB_MAE, _HB_WIS, _HB_WIS)),
    _block("v2.result.hp", "C34", """Against its pooled control, there is **no demonstrated joint
           preference**: the interval score improves, {r:%s} {r:%s|ci}, but the point-error interval
           ends just above zero, {r:%s} [{r:%s|lo}, {r:%s|exact_hi}]. This is not
           equivalence.""" % (_HP_WIS, _HP_WIS, _HP_MAE, _HP_MAE, _HP_MAE)),
    _block("v2.result.pb2", "C38", """The pooled control against the daily LEAR reference does not meet
           the rule either: its interval-score interval, {r:%s|ci}, spans zero.""" % _PB_WIS),
    _block("v2.result.criteria", "C39", """Both {s:version:v2} arms miss criteria {s:criterion:1–2}
           ({r:cp16.metrics.V2-H.equal_fold.S_MAE} and {r:cp16.metrics.V2-P.equal_fold.S_MAE} against
           {r:cp16.criteria.V2-H.c1.equal_fold.S_MAE.upper_limit}) and meet criteria
           {s:criterion:3–6}."""),
    _block("v2.limitation", "C41", """The improvement over the daily LEAR reference is not attributed
           to hour-aware intervals alone, because the pooled control passes the same fold criterion;
           the split between the blend and the interval layer is not isolated."""),
    _block("v2.decision", "C95", """Adopted as the research model that {s:version:v3} builds on:
           **{s:version:v2} · blended LEAR, hour-aware intervals**."""),
    # ---- v1 chapter ----------------------------------------------------------
    _block("v1.what", "P11", """{s:version:v1} is the released product: a LightGBM nine-quantile
           ensemble with calibrated {s:level:50 / 80 / 95%} intervals, evaluated once on a
           pre-specified holdout and shipped exactly as evaluated. The demo runs it in your
           browser."""),
    _block("v1.holdout", "P11", """On the one-shot {v1:holdout_days}-day holdout: MAE
           {v1:holdout_mae_champion} against {v1:holdout_mae_naive} EUR/MWh for the similar-day naive;
           mean pinball loss {v1:holdout_pinball_champion} against {v1:holdout_pinball_naive}; DM
           p = {v1:holdout_dm_p_value}."""),
    _block("v1.unflattering", "P11", """**Two unflattering results, kept in view.** On the development
           folds the point-accuracy test shows a deficit, not merely no advantage: statistic
           +{v1:development_dm_point_statistic_abs}, p = {v1:development_dm_point_p_value}, the median
           {v1:development_dm_point_relative} than the naive. And over the August {s:date:2022} peak
           weeks its {s:level:95%} interval covered {r:cp15.peak.B1.coverage95|p=3} of outcomes."""),
    _block("v1.lesson", "P11", """**The lesson from the crisis:** the errors were about price level, not
           shape. On the crisis window the bias was {r:cp15.peak.B1.bias} EUR/MWh; the daily
           mean-level error was {r:cp15.peak.B1.daily_mean_level_MAE} against a within-day shape error
           of {r:cp15.peak.B1.within_day_shape_MAE}."""),
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
}

#: Claims bound outside a block: single chart rows where a chart mixes claims (v2's three
#: contrasts), and the demo's startup figure beside the primary action (P13).
ROW_CLAIMS: tuple[str, ...] = ("C33", "C34", "C38", "C70", "P13")

#: README research block, in order (plan §9.4).
README_BLOCKS: tuple[str, ...] = (
    "opening.summary", "overview.fairness", "v3.change", "v3.outcome.mae", "v3.outcome.wis",
    "v3.result", "v3.caveat.bundle", "v3.caveat.fold3", "v2.result.hb2", "v2.result.hp",
    "v2.branch.cp10", "overview.f07",
)
for _key in README_BLOCKS:
    BLOCKS_BY_KEY[_key] = Block(
        BLOCKS_BY_KEY[_key].key, BLOCKS_BY_KEY[_key].claim_id, BLOCKS_BY_KEY[_key].template,
        BLOCKS_BY_KEY[_key].surfaces | {README},
    )
BLOCKS = tuple(BLOCKS_BY_KEY[block.key] for block in BLOCKS)

#: Records whose value must always be shown in full, never rounded (plan §6 invariant 9).
EXACT_FIELDS = {(_HP_MAE, "ci_high")}

# --------------------------------------------------------------------------- rendering

_TOKEN = re.compile(r"\{(r|s|v1):([^{}]+)\}")
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


def _render_record(claim_id: str, spec: str, target: str) -> str:
    record_id, _, option = spec.partition("|")
    record = R.get(record_id)
    option = option or None

    def one(which: str, opt: str | None) -> str:
        text = _value_text(record, which, opt)
        raw = {"value": record.raw, "ci_low": record.ci_low_raw, "ci_high": record.ci_high_raw}[which]
        return text if target == "md" else _html_value(claim_id, record_id, which, text, raw)

    if option == "ci":
        if record.interval is None:
            raise ClaimError(f"{record_id} has no interval")
        return f"[{one('ci_low', None)}, {one('ci_high', None)}]"
    if option == "lo":
        return one("ci_low", None)
    if option == "hi":
        return one("ci_high", None)
    if option == "exact_hi":
        return one("ci_high", "exact")
    return one("value", option)


def _v1(claim_id: str, key: str, target: str) -> str:
    from .claims import build_claims

    text = build_claims()[key]
    if target == "md":
        return text
    return (
        f'<data value="{html.escape(text)}" data-claim="{claim_id}" data-v1="{key}">'
        f"{html.escape(text)}</data>"
    )


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
    R.get(record_id)
    field = "" if which == "value" else f' data-field="{which}"'
    return f' data-claim="{claim_id}" data-record="{record_id}"{field}'


def svg_value(record_id: str, which: str = "value", option: str | None = None) -> str:
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
        ("W20", r"\bv3\b[^.]{0,60}\b\d+(\.\d+)?\s?(%|x\b|times\b)[^.]{0,30}\bv1\b"),
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
    "EXACT_FIELDS",
    "NOT_ADOPTED",
    "PLANNED",
    "POLICY_NAMES",
    "POLICY_ROLES",
    "README_BLOCKS",
    "STALE_PHRASES",
    "WITHHELD_PATTERNS",
    "all_claim_ids",
    "claim_map_ids",
    "render",
    "render_template",
    "stale_findings",
    "structural",
    "svg_binding",
    "svg_value",
    "withheld_findings",
]
