"""Independent CP-16 saved-vector arithmetic audit, never a review verdict.

No CP-15/CP-16 scorer/model is imported. A module fixture charges one reference
and one analysis pass before reading production vectors. Invoke under the shared
monitor with CP16_LEDGER and CP16_REQUIRE_SAVED_EVIDENCE=1 for acceptance. This
metric-only analysis does not replay forecast state or consume policy-days.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "reports/v2-causal"
POLICIES = ("B0", "B1", "B2", "B3", "A1", "V2-H", "V2-P")
CANDIDATES = POLICIES[-2:]
FOLDS = tuple(f"fold_{i}" for i in range(1, 6))
WINDOWS = dict(zip(FOLDS, (("2020-07-01", "2020-09-28"), ("2021-04-01", "2021-06-29"),
    ("2022-07-01", "2022-09-28"), ("2025-05-01", "2025-07-29"), ("2026-01-08", "2026-04-07"))))
COUNTS = dict(zip(FOLDS, (2160, 2159, 2112, 2160, 2156)))
QUANTILES = ("p025", "p10", "p25", "p50", "p75", "p90", "p975")
PROBS = np.array([.025, .10, .25, .50, .75, .90, .975])
INTERVALS = ((50, .5, "p25", "p75"), (80, .2, "p10", "p90"), (95, .05, "p025", "p975"))
CONTRASTS = (("V2-H", "V2-P"), ("V2-H", "B2"), ("V2-P", "B2"))
KEYS = ["fold", "timestamp_utc"]


def close(actual, expected):
    np.testing.assert_allclose(actual, expected, rtol=2e-12, atol=2e-12, equal_nan=True)


def canonical(frame):
    frame = frame.copy()
    times = pd.to_datetime(frame.timestamp_utc, errors="raise")
    assert times.dt.tz is not None, "naive canonical timestamp"
    frame["timestamp_utc"] = times.dt.tz_convert("UTC").dt.as_unit("ns")
    dates = pd.to_datetime(frame.delivery_date, errors="raise")
    assert dates.dt.tz is None and dates.eq(dates.dt.normalize()).all()
    frame["delivery_date"] = dates.dt.as_unit("ns")
    return frame


def compare(actual, expected, keys):
    """Every oracle field is checked, including structural NaNs and labels."""
    assert not actual.duplicated(keys).any(), keys
    assert not expected.duplicated(keys).any(), keys
    left, right = actual.set_index(keys).sort_index(), expected.set_index(keys).sort_index()
    pd.testing.assert_index_equal(left.index, right.index, exact=False)
    for col in right.columns:
        assert col in left, col
        if pd.api.types.is_numeric_dtype(right[col]):
            close(left[col].to_numpy(float), right[col].to_numpy(float))
        else:
            assert left[col].fillna("<missing>").astype(str).tolist() == right[col].fillna("<missing>").astype(str).tolist(), col


def validate_vectors(frame, saved):
    assert len(frame) == 75229 and set(frame.policy) == set(POLICIES)
    assert set(frame.fold) == set(FOLDS)
    assert not frame.duplicated(["policy", "timestamp_utc"]).any()
    assert frame.timestamp_utc.eq(frame.timestamp_utc.dt.floor("h")).all()
    local = frame.timestamp_utc.dt.tz_convert("Europe/Berlin").dt.tz_localize(None)
    assert local.dt.normalize().eq(frame.delivery_date).all()
    values = frame[["y_true", "central", "scale", *QUANTILES]].to_numpy(float)
    assert np.isfinite(values).all() and frame.scale.gt(0).all()
    assert (np.diff(frame[list(QUANTILES)].to_numpy(float), axis=1) >= 0).all()
    original = saved.loc[saved.policy.eq("B0")].set_index(KEYS).sort_index()
    assert original.groupby(level="fold").size().to_dict() == COUNTS
    for policy in POLICIES:
        arm = frame.loc[frame.policy.eq(policy)].set_index(KEYS).sort_index()
        pd.testing.assert_index_equal(arm.index, original.index, exact=False)
        assert np.array_equal(arm.y_true.to_numpy(), original.y_true.to_numpy())
        assert np.array_equal(arm.delivery_date.to_numpy(), original.delivery_date.to_numpy())
        for fold, (start, end) in WINDOWS.items():
            assert arm.xs(fold).delivery_date.between(start, end).all()
        f3 = arm.xs("fold_3")
        peak = f3.loc[f3.delivery_date.between("2022-08-15", "2022-08-31")]
        assert len(f3) == 2112 and f3.delivery_date.nunique() == 88
        assert len(peak) == 408 and peak.delivery_date.nunique() == 17
        if policy in POLICIES[:5]:
            prior = saved.loc[saved.policy.eq(policy)].set_index(KEYS).sort_index()
            pd.testing.assert_index_equal(arm.index, prior.index, exact=False)
            assert np.array_equal(arm[["central", "scale", *QUANTILES]].to_numpy(),
                                  prior[["central", "scale", *QUANTILES]].to_numpy())
    arms = {p: frame.loc[frame.policy.eq(p)].set_index(KEYS).sort_index() for p in POLICIES}
    assert np.array_equal(arms["V2-H"][["central", "scale"]], arms["V2-P"][["central", "scale"]])
    close(arms["V2-H"].central, .5 * (arms["A1"].central + arms["B2"].central))
    assert np.array_equal(arms["V2-H"].scale, arms["A1"].scale)


def losses(frame):
    """Independent vector formulas; level/shape use whole issued delivery days."""
    x = frame.copy()
    y, median = x.y_true.to_numpy(float), x.p50.to_numpy(float)
    error = median - y
    x["ae"], x["se"], x["bias_value"] = abs(error), error**2, error
    x["central_ae"] = abs(x.central.to_numpy(float) - y)
    daily = x.groupby(["policy", "fold", "delivery_date"])
    center_y, center_p = daily.y_true.transform("mean"), daily.p50.transform("mean")
    x["level"] = abs(center_p - center_y)
    x["shape"] = abs((x.p50 - center_p) - (x.y_true - center_y))
    weighted = .5 * abs(error)
    for nominal, alpha, lo, hi in INTERVALS:
        low, high = x[lo].to_numpy(float), x[hi].to_numpy(float)
        below, above = y < low, y > high
        width = high - low
        score = width + (2 / alpha) * (low - y) * below + (2 / alpha) * (y - high) * above
        weighted += alpha / 2 * score
        x[f"width{nominal}"] = width
        x[f"lower{nominal}"], x[f"upper{nominal}"], x[f"hit{nominal}"] = below, above, ~(below | above)
    x["wis"] = weighted / 3.5
    residual = y[:, None] - x[list(QUANTILES)].to_numpy(float)
    x["pinball"] = np.maximum(PROBS * residual, (PROBS - 1) * residual).mean(axis=1)
    x["hour"] = x.timestamp_utc.dt.tz_convert("Europe/Berlin").dt.hour
    return x


def summarize(x):
    dates = sorted(x.delivery_date.dt.strftime("%Y-%m-%d").unique().tolist())
    result = dict(n_hours=len(x), n_days=len(dates), first_delivery_date=dates[0] if dates else None,
                  last_delivery_date=dates[-1] if dates else None, represented_dates=json.dumps(dates),
                  MAE=x.ae.mean(), RMSE=np.sqrt(x.se.mean()), WIS=x.wis.mean(), mean_pinball_7=x.pinball.mean(),
                  raw_central_MAE=x.central_ae.mean(), centering_effect=(x.ae-x.central_ae).mean(),
                  bias=x.bias_value.mean(), daily_mean_level_MAE=x.groupby(["fold", "delivery_date"])["level"].first().mean(),
                  within_day_shape_MAE=x["shape"].mean(), missing_count=0, crossings=0)
    for nominal, *_ in INTERVALS:
        widths = x[f"width{nominal}"]
        result.update({f"coverage{nominal}": x[f"hit{nominal}"].mean(),
                       f"hit_count{nominal}": int(x[f"hit{nominal}"].sum()),
                       f"lower_miss_count{nominal}": int(x[f"lower{nominal}"].sum()),
                       f"upper_miss_count{nominal}": int(x[f"upper{nominal}"].sum()),
                       f"mean_width{nominal}": widths.mean(), f"median_width{nominal}": widths.median(),
                       f"p95_width{nominal}": widths.quantile(.95, interpolation="linear")})
    return result


def tables(frame):
    x = losses(frame)
    metrics, diagnostics, daily = [], [], []
    for policy in POLICIES:
        selected = x.loc[x.policy.eq(policy)]
        metrics.append(dict(policy=policy, scope="pooled", fold="all", **summarize(selected)))
        for fold, (start, end) in WINDOWS.items():
            part = selected.loc[selected.fold.eq(fold)]
            metrics.append(dict(policy=policy, fold=fold, scope="per_fold", window_start=start,
                                window_end=end, calendar_days=90, **summarize(part)))
            blocks = {"night": set(range(0, 6)) | {22, 23}, "solar": set(range(10, 17)),
                      "shoulder": set(range(6, 10)) | set(range(17, 22))}
            subsets = [("hour", str(h), part.loc[part.hour.eq(h)]) for h in range(24)]
            subsets += [("block", b, part.loc[part.hour.isin(hours)]) for b, hours in blocks.items()]
            for scope, group, subset in subsets:
                diagnostics.append(dict(policy=policy, fold=fold, scope=scope, group=group,
                    support_status="eligible" if subset.delivery_date.nunique() >= 56 else "support_limited",
                    minimum_dates=56, uncertainty_claim="none_descriptive_diagnostics", **summarize(subset)))
            by_day = {day: rows for day, rows in part.groupby("delivery_date")}
            for day in pd.date_range(start, end):
                rows = by_day.get(day, part.iloc[:0])
                record = dict(policy=policy, fold=fold, scope="daily", delivery_date=str(day.date()), n_hours=len(rows))
                record.update({"MAE": rows.ae.mean(), "WIS": rows.wis.mean(), "coverage95": rows.hit95.mean(),
                    "hit_count95": rows.hit95.sum() if len(rows) else np.nan,
                    "lower_miss_count95": rows.lower95.sum() if len(rows) else np.nan,
                    "upper_miss_count95": rows.upper95.sum() if len(rows) else np.nan,
                    "mean_width95": rows.width95.mean()})
                daily.append(record)
        f3 = selected.loc[selected.fold.eq("fold_3")]
        peak = f3.loc[f3.delivery_date.between("2022-08-15", "2022-08-31")]
        diagnostics.append(dict(policy=policy, fold="fold_3", scope="peak", group="August15-31",
            window_start="2022-08-15", window_end="2022-08-31", calendar_days=17,
            support_status="support_limited", evidence_class="descriptive_only_small_effective_sample", **summarize(peak)))
        for day in (1, 8, 15, 22):
            start, end = f"2022-09-{day:02}", f"2022-09-{day+6:02}"
            diagnostics.append(dict(policy=policy, fold="fold_3", scope="recovery", group=start,
                window_start=start, window_end=end, calendar_days=7, evidence_class="descriptive_only",
                **summarize(f3.loc[f3.delivery_date.between(start, end)])))
    metrics = pd.DataFrame(metrics)
    for name in ("MAE", "WIS"):
        denominator = metrics.loc[metrics.scope.eq("pooled") & metrics.policy.eq("B0"), name].iloc[0]
        metrics[f"pooled_ratio_{name}"] = np.where(metrics.scope.eq("pooled"), metrics[name]/denominator, np.nan)
    return metrics, pd.DataFrame(diagnostics), pd.DataFrame(daily)


def safe_ratio(a, b):
    a, b = np.broadcast_arrays(np.asarray(a, float), np.asarray(b, float))
    out = np.full(a.shape, np.nan)
    np.divide(a, b, out=out, where=np.isfinite(b) & (b > 0))
    return out


def decision(metrics, diagnostics):
    folds = metrics.loc[metrics.scope.eq("per_fold")].set_index(["policy", "fold"])
    peak = diagnostics.loc[diagnostics.scope.eq("peak")].set_index("policy")
    scores = {p: {"S_"+m: np.mean([safe_ratio(folds.loc[(p,f),m], folds.loc[("B0",f),m])
              for f in FOLDS]) for m in ("MAE", "WIS")} for p in POLICIES}
    rows = []
    def add(p, c, m, scope, actual, lower=np.nan, upper=np.nan, comparator=None):
        defined = np.isfinite(actual)
        passed = bool(defined and (np.isnan(lower) or actual >= lower) and (np.isnan(upper) or actual <= upper))
        rows.append(dict(policy=p, criterion=c, metric=m, scope=scope, actual=actual, lower_limit=lower,
                         upper_limit=upper, comparator=comparator, passed=passed,
                         status=("met" if passed else "not_met") if defined else "unassessed"))
    for p in CANDIDATES:
        for c, m in ((1,"MAE"), (2,"WIS")):
            add(p,c,"S_"+m,"equal_fold",scores[p]["S_"+m],upper=.9*min(scores[b]["S_"+m] for b in POLICIES[:4]),comparator="best B0-B3")
        for f in FOLDS:
            add(p,3,"coverage95",f,folds.loc[(p,f),"coverage95"],.90,.98)
        add(p,4,"coverage95","peak",peak.loc[p,"coverage95"],lower=.90)
        for m in ("MAE","WIS"):
            add(p,4,m,"peak",peak.loc[p,m],upper=min(peak.loc[b,m] for b in POLICIES[:4]),comparator="best B0-B3 on matched peak")
            for f in FOLDS:
                add(p,5,m,f,folds.loc[(p,f),m],upper=1.05*min(folds.loc[(b,f),m] for b in ("B2","B3")),comparator="best rolling B2/B3")
        add(p,6,"complete_finite_ordered","all_eligible",1,1,1)
    ranking = sorted(CANDIDATES, key=lambda p:(scores[p]["S_WIS"],scores[p]["S_MAE"],p!="V2-P"))
    if not all(np.isfinite(list(s.values())).all() for s in scores.values()):
        ranking = None
    equal = pd.DataFrame([dict(policy=p,scope="equal_fold",fold="all",**scores[p]) for p in POLICIES])
    return equal, pd.DataFrame(rows), ranking


def bootstrap(daily):
    """Scalar block concatenation and replicate weighting, independent of scorer."""
    rng = np.random.default_rng(15042)
    digest = hashlib.sha256()
    results, normalized_draws, normalized_points = [], [], []
    def intervals(scope, point, draws):
        for candidate, baseline in CONTRASTS:
            a, b = POLICIES.index(candidate), POLICIES.index(baseline)
            for mi, metric in enumerate(("MAE", "WIS")):
                contrast = draws[:,a,mi] - draws[:,b,mi]
                difference = point[a,mi] - point[b,mi]
                undefined = int((~np.isfinite(contrast)).sum())
                resolved = undefined == 0 and np.isfinite(difference)
                low, high = np.percentile(contrast,[2.5,97.5],method="linear") if resolved else (np.nan,np.nan)
                results.append(dict(scope=scope,candidate=candidate,baseline=baseline,metric=metric,
                    difference=difference,ci_lower=low,ci_upper=high,undefined_replicates=undefined,
                    status="resolved" if resolved else "unresolved_uncertainty",replicates=2000,confidence=.95,
                    estimand="equal-fold B0-normalized eligible-hour mean difference" if scope=="equal_fold" else "paired mean daily loss difference",
                    evidence_class="exploratory_post_selection" if scope=="equal_fold" else "descriptive_paired_daily"))
    for fold, window in WINDOWS.items():
        part = daily.loc[daily.fold.eq(fold)].copy()
        part["delivery_date"] = pd.to_datetime(part.delivery_date)
        dates = pd.date_range(*window)
        assert len(part)==630 and not part.duplicated(["policy","delivery_date"]).any()
        arms = [part.loc[part.policy.eq(p)].set_index("delivery_date").reindex(dates) for p in POLICIES]
        values = np.stack([a[["MAE","WIS"]].to_numpy(float) for a in arms],axis=1)
        counts = np.stack([a.n_hours.to_numpy(float) for a in arms],axis=1)
        assert np.isfinite(counts).all() and (counts>=0).all() and (counts==counts[:,:1]).all()
        represented = counts[:,0]>0
        assert np.array_equal(np.isfinite(values),np.broadcast_to(represented[:,None,None],values.shape))
        point = (values[represented]*counts[represented,:,None]).sum(axis=0)/counts.sum(axis=0)[:,None]
        daily_point = values[represented].mean(axis=0)
        draws, daily_draws = np.empty((2000,7,2)), np.empty((2000,7,2))
        for replicate in range(2000):
            starts = rng.integers(0,84,size=13)
            sample = np.concatenate([np.arange(start,start+7) for start in starts])[:90]
            digest.update(np.asarray(sample,dtype="<i8").tobytes())
            selected = sample[represented[sample]]
            draws[replicate] = safe_ratio((values[selected]*counts[selected,:,None]).sum(axis=0),counts[selected].sum(axis=0)[:,None])
            daily_draws[replicate] = values[selected].mean(axis=0) if len(selected) else np.nan
        intervals(fold,daily_point,daily_draws)
        normalized_points.append(safe_ratio(point,point[0:1]))
        normalized_draws.append(safe_ratio(draws,draws[:,0:1]))
    intervals("equal_fold",np.mean(normalized_points,axis=0),np.mean(normalized_draws,axis=0))
    return pd.DataFrame(results), digest.hexdigest()


@pytest.fixture(scope="module")
def evidence():
    if not (REPORT/"predictions.parquet").exists():
        if os.environ.get("CP16_REQUIRE_SAVED_EVIDENCE")=="1":
            pytest.fail("required saved CP-16 predictions are absent")
        pytest.skip("saved production vectors absent; require with CP16_REQUIRE_SAVED_EVIDENCE=1")
    ledger = os.environ.get("CP16_LEDGER")
    assert ledger, "CP16_LEDGER is required before production verification"
    from cp16.budget import Budget
    budget = Budget(ledger)
    assert Path(ledger).is_file(), "existing shared ledger required"
    budget.reserve(reference_passes=1, analysis_passes=1)
    budget.event("independent_saved_vector_analysis", reference_passes=1, analysis_passes=1, policy_days=0)
    frame = canonical(pd.read_parquet(REPORT/"predictions.parquet"))
    saved = canonical(pd.read_parquet(ROOT/"reports/cp15/predictions.parquet",filters=[("policy","in",list(POLICIES[:5]))]))
    validate_vectors(frame,saved)
    metrics,diagnostics,daily = tables(frame)
    equal,criteria,ranking = decision(metrics,diagnostics)
    uncertainty,fingerprint = bootstrap(daily)
    return dict(frame=frame, metrics=pd.concat([metrics,equal],ignore_index=True),diagnostics=diagnostics,
        daily=daily,criteria=criteria,ranking=ranking,uncertainty=uncertainty,fingerprint=fingerprint,
        summary=json.loads((REPORT/"lineage.json").read_text())["research_summary"])


def test_saved_metric_and_diagnostic_tables(evidence):
    compare(pd.read_csv(REPORT/"metrics.csv"),evidence["metrics"],["policy","scope","fold"])
    actual = pd.read_csv(REPORT/"diagnostics.csv",dtype={"group":str})
    assert set(actual.scope)=={"hour","block","peak","recovery","daily"}
    compare(actual.loc[actual.scope.ne("daily")],evidence["diagnostics"],["policy","scope","fold","group"])
    compare(actual.loc[actual.scope.eq("daily")],evidence["daily"],["policy","fold","delivery_date","scope"])
    assert pd.read_csv(REPORT/"failures.csv").empty


def test_saved_all_six_criteria_and_research_summary(evidence):
    compare(pd.read_csv(REPORT/"criteria.csv"),evidence["criteria"],["policy","criterion","metric","scope"])
    summary,criteria = evidence["summary"],evidence["criteria"]
    assert summary["ranking"]==evidence["ranking"]
    assert summary["ranking_rule"]=="S_WIS, S_MAE, P on exact ties; descriptive only"
    assert summary["selection_status"]==("defined" if evidence["ranking"] else "undefined; protocol correction required before selection")
    for p in CANDIDATES:
        part=criteria.loc[criteria.policy.eq(p)]
        assert set(part.criterion)==set(range(1,7))
        status="unassessed" if part.status.eq("unassessed").any() else ("met" if part.passed.all() else "not_met")
        assert summary["original_section8_status"][p]==status
        assert summary["failed_criteria"][p]==sorted(part.loc[~part.passed,"criterion"].unique().tolist())
    assert summary["historical_cp15_product_status"]=="NOT_DEMONSTRATED"
    assert summary["product_delivery_eligibility"]=="not authorized by research evaluation"
    assert summary["primary_contrast"]=="V2-H-V2-P"
    assert summary["secondary_contrasts"]==["V2-H-B2","V2-P-B2"]
    assert summary["primary_weighting"]=="equal-fold B0-normalized eligible-hour losses"
    assert summary["pooled_weighting"]=="eligible hours"
    assert summary["validation"]==dict(production=True,rows=75229,keys_per_policy=10747,
                                       missing_predictions=0,nonfinite_quantiles=0,crossings=0)
    assert summary["support_rule"]==dict(minimum_represented_dates=56,role="reporting only; no product gate")
    assert summary["native_v1_pinball"]=="preserved separately; mean_pinball_7 is not native v1"
    assert summary["inference"]=="exploratory post-selection; no equivalence, absence-of-benefit or absence-of-harm claim"


def test_saved_uncertainty_and_joint_conclusions(evidence):
    compare(pd.read_csv(REPORT/"uncertainty.csv"),evidence["uncertainty"],["scope","candidate","baseline","metric"])
    summary=evidence["summary"]
    assert summary["bootstrap"]==dict(seed=15042,replicates=2000,block_days=7,calendar_days=90,
        index_sha256=evidence["fingerprint"],shared_index_sets=1,
        method="paired noncircular calendar moving-block percentile",undefined_handling="unresolved; no dropping or redrawing")
    for a,b in CONTRASTS:
        selected=evidence["uncertainty"].query("scope == 'equal_fold' and candidate == @a and baseline == @b").set_index("metric")
        joint=selected.status.eq("resolved").all() and selected.loc["WIS","ci_upper"]<0 and selected.loc["MAE","ci_upper"]<=0
        assert summary["joint_conclusions"][f"{a}-{b}"]==("observed joint improvement" if joint else "no demonstrated joint preference")


def test_oracle_hand_calculated_emitted_median_and_wis():
    frame=pd.DataFrame(dict(policy=["V2-H"]*3,fold=["fold_1"]*3,
        timestamp_utc=pd.date_range("2020-07-01",periods=3,freq="h",tz="UTC"),
        delivery_date=[pd.Timestamp("2020-07-01")]*3,y_true=[0.,5.,10.],central=[0.,5.,10.],
        scale=[1.]*3,p025=[1.]*3,p10=[2.]*3,p25=[3.]*3,p50=[4.]*3,
        p75=[5.]*3,p90=[6.]*3,p975=[7.]*3))
    result=summarize(losses(frame))
    close(result["MAE"],11/3)
    close(result["raw_central_MAE"],0)
    close(result["WIS"],(9.05+1.55+16.05)/10.5)
    assert result["hit_count95"]==result["lower_miss_count95"]==result["upper_miss_count95"]==1
    close(result["daily_mean_level_MAE"],1)
    close(result["within_day_shape_MAE"],10/3)


@pytest.mark.parametrize("column",["MAE","WIS","n_hours","hit_count95","represented_dates"])
def test_table_checker_rejects_tampered_numeric_and_population_fields(column):
    expected=pd.DataFrame([dict(policy="V2-H",MAE=1.,WIS=2.,n_hours=24,hit_count95=23,represented_dates='["2020-07-01"]')])
    compare(expected.copy(),expected,["policy"])
    tampered=expected.copy()
    tampered.loc[0,column] = '[]' if column=="represented_dates" else tampered.loc[0,column]+1
    with pytest.raises(AssertionError):
        compare(tampered,expected,["policy"])


def test_undefined_reference_never_becomes_zero_or_epsilon():
    result=safe_ratio(np.array([1.,1.,1.,0.]),np.array([0.,np.nan,2.,0.]))
    assert np.isnan(result[[0,1,3]]).all()
    close(result[2],.5)


def test_research_ranking_prefers_p_on_exact_ties_and_reports_all_criteria():
    rows, peak = [], []
    for policy in POLICIES:
        loss = 80. if policy in CANDIDATES else 100.
        for fold in FOLDS:
            rows.append(dict(policy=policy,fold=fold,scope="per_fold",MAE=loss,WIS=loss,coverage95=.95))
        peak.append(dict(policy=policy,scope="peak",MAE=loss,WIS=loss,coverage95=.95))
    metrics,diagnostics = pd.DataFrame(rows),pd.DataFrame(peak)
    _,criteria,ranking = decision(metrics,diagnostics)
    assert ranking == ["V2-P","V2-H"] and criteria.passed.all()
    # Point improvement cannot outrank a WIS disadvantage in this research rule.
    metrics.loc[metrics.policy.eq("V2-H"),"MAE"] = 50.
    metrics.loc[metrics.policy.eq("V2-H"),"WIS"] = 81.
    assert decision(metrics,diagnostics)[2] == ["V2-P","V2-H"]
    metrics.loc[metrics.policy.eq("V2-H") & metrics.fold.eq("fold_2"),"coverage95"] = .89
    _,criteria,_ = decision(metrics,diagnostics)
    assert criteria.loc[criteria.policy.eq("V2-H") & criteria.criterion.eq(3),"passed"].tolist() == [True,False,True,True,True]


def test_bootstrap_oracle_calendar_missingness_variable_hours_and_tamper():
    records = []
    d = np.arange(90,dtype=float)
    base = 10+d
    counts = np.full(90,24.)
    counts[5],counts[40],counts[17] = 23.,25.,0.
    h = .7*base + .02*d
    for fold,window in WINDOWS.items():
        for day,date in enumerate(pd.date_range(*window)):
            for policy in POLICIES:
                value = h[day] if policy=="V2-H" else (.8*base[day] if policy=="V2-P" else base[day])
                if not counts[day]: value=np.nan
                records.append(dict(policy=policy,fold=fold,delivery_date=str(date.date()),
                                    n_hours=counts[day],MAE=value,WIS=2*value))
    daily = pd.DataFrame(records)
    actual,_ = bootstrap(daily)
    rng = np.random.default_rng(15042)
    normalized_differences = []
    mask = counts > 0
    point = np.dot(h,counts)/np.dot(base,counts)-.8
    for fold in FOLDS:
        # Separate vectorized calculation, unlike scalar replicate implementation.
        starts = rng.integers(0,84,size=(2000,13))
        sampled = (starts[:,:,None]+np.arange(7)).reshape(2000,91)[:,:90]
        weights = counts[sampled]
        hsum = (h[sampled]*weights).sum(axis=1)
        bsum = (base[sampled]*weights).sum(axis=1)
        normalized_differences.append(hsum/bsum-.8)
        present = mask[sampled]
        differences = np.where(present,h[sampled]-.8*base[sampled],0).sum(axis=1)/present.sum(axis=1)
        row = actual.loc[actual.scope.eq(fold) & actual.candidate.eq("V2-H") & actual.baseline.eq("V2-P") & actual.metric.eq("MAE")].iloc[0]
        close(row.difference,np.mean((h-.8*base)[mask]))
        close([row.ci_lower,row.ci_upper],np.percentile(differences,[2.5,97.5]))
    row = actual.loc[actual.scope.eq("equal_fold") & actual.candidate.eq("V2-H") & actual.baseline.eq("V2-P") & actual.metric.eq("MAE")].iloc[0]
    close(row.difference,point)
    close([row.ci_lower,row.ci_upper],np.percentile(np.mean(normalized_differences,axis=0),[2.5,97.5]))
    tampered=actual.copy()
    tampered.loc[0,"ci_upper"] += .001
    with pytest.raises(AssertionError):
        compare(tampered,actual,["scope","candidate","baseline","metric"])
