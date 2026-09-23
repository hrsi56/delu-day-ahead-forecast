"""Explicit real-data review reproduction, always invoked through the shared monitor."""
from pathlib import Path
from datetime import date, timedelta
import argparse, os
import numpy as np
from cp16.budget import Budget, atomic, counted_fits
from cp16.inputs import load, SavedComponents
from cp16.execution import check_protocol, compare_fit
from cp15.data import prepare

ROOT=Path(__file__).resolve().parents[2]


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    check_protocol(ROOT);budget=Budget(os.environ['CP16_LEDGER']);data,_=load(ROOT)
    records=[]
    for fold,day in [('fold_1',date(2020,7,1)),('fold_2',date(2021,4,1))]:
        cache=SavedComponents(ROOT,fold,data)
        records.append(compare_fit(cache,data,day,budget,'independent review representative'))
    day=date(2020,7,1);cache=SavedComponents(ROOT,'fold_1',data);rows,original,_=cache.get(day)
    for mode in ('target_and_future_mask','available_d1_mutation'):
        budget.reserve(policy_days=2)
        raw=data.frame.copy()
        if mode=='target_and_future_mask':
            raw.loc[raw.delivery_date>=day,'price_eur_mwh']=np.nan
            raw.loc[raw.delivery_date>day,'load_forecast_mw']=1e8
        else:raw.loc[raw.delivery_date.eq(day-timedelta(days=1)),'price_eur_mwh']+=500
        altered=prepare(raw,data.p,data.spec);result={'control':mode,'max_abs_difference':{}}
        with counted_fits(budget) as fit:
            for policy in ('A1','B2'):
                pred,logs=fit(altered,day,policy,rows=rows)
                delta=float(np.max(np.abs(pred-original[policy])))
                assert delta==0. if mode=='target_and_future_mask' else delta>0.
                result['max_abs_difference'][policy]=delta
        records.append(result)
    atomic(args.output,records);print(records,flush=True)

if __name__=='__main__':main()
