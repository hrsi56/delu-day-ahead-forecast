from pathlib import Path
import json,csv,hashlib,shutil,time,subprocess
root=Path.cwd();out=root/'reports/v2-causal';ev=root/'docs/track-b/evidence/cp-16'
ledger=Path('/Users/djourno/Downloads/PJM/.local/artifacts/cp-16/budget.json')
d=json.loads(ledger.read_text());lineage=json.loads((out/'lineage.json').read_text());summary=lineage['research_summary']
read=lambda n:list(csv.DictReader((out/n).open()))
metrics=read('metrics.csv');uncertainty=read('uncertainty.csv');criteria=read('criteria.csv')
def table(rows,columns):
 return '| '+' | '.join(columns)+' |\n|'+ '|'.join(['---']*len(columns))+'|\n'+'\n'.join('| '+' | '.join(str(r.get(k,'')) for k in columns)+' |' for r in rows)
resources={**d,'summary':{'historical_policy_days_unchanged':3730,'policy_days_remaining':9000-d['counts']['policy_days'],'peak_monitored_rss_bytes':max(j.get('peak_process_tree_rss_bytes',0) for j in d['jobs']),'peak_monitored_disk_upper_bound_bytes':max(j.get('peak_checkpoint_disk_bytes',0) for j in d['jobs']),'historic_memory_gap':'UNKNOWN; see attempt-1 and resumption-notice. Regeneration is not retrospective compliance.','historic_thread_enforcement':'Unsupported for early Builder jobs; resumed jobs pinned and runtime inspected.','active_effort_upper_bound_seconds':d['effort']['historical_upper_bound_seconds']+time.time()-d['effort']['resumed_epoch'],'approximate_timebox_hours':32,'active_hard_cap_hours':40,'new_output_policies':2,'saved_references':5,'scored_policies':7,'hour_aware_recipes':1,'pooled_controls':1,'outer_selection_trials':0,'component_configurations':2,'feature_recipes':1,'model_seeds':[42],'bootstrap_seeds':[15042],'ensemble_members':2,'unique_date_fold_keys':len({(x['fold'],x['day']) for x in lineage['origins']}),'admission_policy_days_completed':70,'max_CPU_workers_current':1,'BLAS_threads_current':1,'GPU_jobs':0,'cloud_jobs':0,'new_download_bytes':0,'new_sources':0,'weather_probes':0,'neural_candidates':0,'VRE_fits':0,'recombination_searches':0,'economic_runs':0,'operational_days':0,'automated_schedules':0,'remote_mutations':0,'external_cost_USD':0,'new_B0_B1_B3_fits':0,'review_accounting':'Candidate snapshot before final Integration. Final cumulative ledger, including all review attempts, is docs/track-b/evidence/cp-16/resource-final.json at evidence tip.'}}
# Fit timing is measured by the inherited fitter. H/P share components; never sum their repeated shared cost.
fitrows=[]
for f in range(1,6):
 name=f'fold_{f}'
 for p in ('A1','B2'):
  logs=[x for item in lineage['new_components'].values() if item['fold']==name for x in item['fits'][p]]
  fitrows.append({'fold':name,'component':p,'new_hourly_fit_records':len(logs),'primitive_calls':sum(x['solver_calls'] for x in logs),'fit_seconds':sum(x['fit_seconds'] for x in logs)})
resources['regenerated_main_fit_costs']=fitrows
(out/'resources.json').write_text(json.dumps(resources,indent=2,sort_keys=True)+'\n')
rank=summary['ranking'];s=resources['summary']
text=f'''# CP-16 fixed H/P research comparison — development, post-selection

Engineering status: **pending fresh exact-candidate Integration review**; the terminal verdict and both SHAs are recorded in the canonical checkpoint return. Historical CP-15 product status: **NOT_DEMONSTRATED**, unchanged. New original-§8 diagnostic status: {summary['original_section8_status']}. Product/delivery eligibility: **not authorized by this research evaluation**.

Descriptive H/P ordering: {' then '.join(rank)} (S_WIS, then S_MAE, then P on exact ties). Ranking does not establish a supported winner or select a live policy. Primary conclusion: **{summary['joint_conclusions']['V2-H-V2-P']}**. All intervals are exploratory post-selection; no equivalence, absence-of-benefit or absence-of-harm claim follows.

## Point and interval scores

Each primary score equally averages five fold ratios to B0. MAE uses emitted p50; the central forecast remains separate. Seven-quantile WIS uses interval weights alpha/2, median weight 1/2 and divisor 3.5. Native v1 nine-quantile pinball remains in its original historical files and is not this WIS or mean_pinball_7.

{table([r for r in metrics if r['scope']=='equal_fold'],['policy','S_MAE','S_WIS'])}

Primary H−P and secondary comparisons, with 95% paired percentile intervals:

{table([r for r in uncertainty if r['scope']=='equal_fold'],['candidate','baseline','metric','difference','ci_lower','ci_upper','status'])}

Joint improvement requires WIS upper endpoint <0 AND MAE upper endpoint <=0. Both metrics and their directions are retained without an invented tradeoff weight. Conclusions: {json.dumps(summary['joint_conclusions'],sort_keys=True)}.

## Population and causal construction

All seven policies cover 10,747 identical eligible keys: 2,160 / 2,159 / 2,112 / 2,160 / 2,156, totaling 75,229 policy-target rows. Full fold 3 has 2,112 hours across 88 represented dates; August 15–31 has 408 hours/17 dates. Original missing/excluded hours are preserved; no failed eligible issuance is removed. `failures.csv` records the current run, while historical invalidated failure logs remain in `attempt-1/`.

Both policies use exactly the A1/B2 central 50/50 blend, origin-specific A1 scale, and the same latest 28 complete released error days. H shrinks local-hour quantiles toward pooled values using n/(n+56), with pooled fallback below 14 distinct days; P uses pooled values. Both score their own shifted p50. No clipping, projection or p50 reset is used. All 35 training-only admission dates were completed and frozen before outer comparison. Fixed origins are D−1 11:00 UTC; delivery calendar is Europe/Berlin. D−1 errors cannot update the buffer, D−2 complete errors can; canonical 23/24/25-hour identities and consume-once hold.

## Diagnostics and unchanged quality conditions

`metrics.csv` reports all per-fold and pooled metrics, central/p50 error and centering, RMSE, signed bias, daily level/shape, 50/80/95% coverage and width summaries and tail misses. `diagnostics.csv` carries all 24 local hours, exhaustive night 22–05 / solar 10–16 / shoulder 06–09 and 17–21 blocks, represented dates/hits/widths, daily losses, peak and September recovery slices. At least 56 represented dates is required for supported hour/block comparison statements; fewer is explicitly support-limited. Peak and recovery slices remain descriptive.

`uncertainty.csv` retains all full-fold descriptive paired daily intervals and the primary equal-fold normalized intervals. Seed 15042 produces one shared set of 2,000 noncircular 7-calendar-day block draws per pass; missing dates remain missing. Undefined replicates would be unresolved, never dropped or redrawn. Index identity: {summary['bootstrap']['index_sha256']}.

All six original §8 diagnostics, actuals, limits and comparator identities:

{table(criteria,['policy','criterion','metric','scope','actual','lower_limit','upper_limit','comparator','status'])}

## Resources, defects and limitations

Cumulative candidate policy-days: {d['counts']['policy_days']}/9,000, including the unchanged historical 3,730. Counts and every monitored command are in `resources.json`; review adds to the same ledger and its final evidence snapshot. Candidate machine time: {d['counts']['machine_seconds']/3600:.4f} hours/24. Active effort conservative upper bound: {s['active_effort_upper_bound_seconds']/3600:.2f} hours/40, against the original 32-hour approximate timebox. Resumed jobs are serialized, numerical thread pools1. Peak measured process-tree RSS {s['peak_monitored_rss_bytes']/1024**3:.3f} GiB; disk upper bound {s['peak_monitored_disk_upper_bound_bytes']/1024**3:.3f} GiB (includes entire pre-existing Git store). No downloads, external services, cost, forbidden work or new reference fits.

New main fitting by fold and component (shared by H/P, not charged twice):

{table(fitrows,['fold','component','new_hourly_fit_records','primitive_calls','fit_seconds'])}

H/P emission, data preparation and memory are measured jointly by monitored job, not invented per-policy allocations. B0/B1/B2/B3/A1 are saved vectors with zero new model-fit cost; their original measured costs remain in `reports/cp15/report.md` and fold run logs. Current scoring/reading costs are shared metric-only jobs in the ledger. Reference fits and their costs are not silently treated as newly generated.

The prior interrupted admission and independent FAIL remain preserved, including unknown RSS during the supervisor gap and unsupported early thread-enforcement assertions. Required evidence was regenerated under repaired monitoring; no old gap is claimed cured retrospectively. See `docs/track-b/evidence/cp-16/resumption-notice.md` and `resumption-feasibility.md`. Historical and current accounting are distinguished, with all debits retained. Atomic saves, cache identity, timestamp-resolution persistence and supervisor failure handling were repaired without changing the scientific recipe.

A65 historical vintage availability and revision assumptions remain inherited limitations. All five folds, including fold 3, are development/post-selection evidence; no new confirmatory claim, economics, exposure, service-level guarantee, promotion, CP-17 or publication is authorized. Existing `DATA-LICENSE.md` and source notices remain controlling.
'''
(out/'report.md').write_text(text)
print(json.dumps(summary,indent=2));print('Report and candidate resources generated')
