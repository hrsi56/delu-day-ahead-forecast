"""Admission, partition projection and immutable inherited-input identity."""
from __future__ import annotations
from datetime import date
import hashlib
import json
from pathlib import Path
import subprocess
import numpy as np
import pandas as pd
from cp15.data import RAW_COLUMNS, prepare, sha, array_hash, history_start, origin_utc
from delu_forecast.folds import load_partition_spec

SUPPLIED = {
 'capstone_v21.md': 'a05700ef6de700a956f6d8725cd45ecbc13f2384f780c309fffc5ba835d80a2d',
 'docs/track-b/capstone_v21-r1-to-v21-r2-amendments.md': '09c663359ac2471a8adbc9865d8cbfa2a25e86062aebf8428411bb74614fadab',
 'docs/track-b/cp-16-v2-brief.md': '1545089898aa47aa5384f5c6bcd07fda5ec7c0c98649cb44f2adba26cd0667ee'}
EVIDENCE = '1bdc75b8ab943092bb8de6ba893defb9e12250d8'


def identities(root):
    root = Path(root)
    p = json.loads((root/'reports/cp15/protocol.json').read_text())
    result = {}
    for name, expected in SUPPLIED.items():
        if sha(root/name) != expected: raise ValueError('wrong supplied input: '+name)
        result[name] = expected
    for name, expected in p['input_sha256'].items():
        if name in ('AGENTS.md','capstone_v21.md'):
            historical = subprocess.check_output(['git','show',f'{EVIDENCE}:{name}'],cwd=root)
            if hashlib.sha256(historical).hexdigest() != expected:
                raise ValueError('inherited historical identity mismatch: '+name)
            result[f'{EVIDENCE}:{name}'] = expected
        else:
            if sha(root/name) != expected: raise ValueError('inherited input mismatch: '+name)
            result[name] = expected
    manifest = json.loads((root/'reports/cp15/artifact-manifest.json').read_text())['artifact_sha256']
    names = ['src/cp15/data.py','src/cp15/models.py','reports/cp15/protocol.json',
             'reports/cp15/predictions.parquet']
    for fold in range(1,6):
        names += [f'reports/cp15/folds/fold_{fold}-{suffix}' for suffix in
                  ('issued.parquet','fits.parquet','run.json')]
    for name in names:
        actual = sha(root/name)
        if actual != manifest[name]: raise ValueError('saved artifact identity mismatch: '+name)
        result[name] = actual
    return p, result


def load(root, before=None):
    p, hashes = identities(root)
    spec = load_partition_spec(root/'data/partitions.json')
    filters = [('delivery_date','>=',date(2019,1,1)),('delivery_date','<=',spec.eda_cutoff)]
    if before is not None: filters.append(('delivery_date','<',before))
    frame = pd.read_parquet(root/'data/snapshot.parquet', columns=RAW_COLUMNS, filters=filters)
    return prepare(frame,p,spec), hashes


def expected(root):
    # Metadata-only projection: no outer outcomes are materialized in preflight.
    return pd.read_parquet(root/'reports/cp15/predictions.parquet',
        columns=['fold','timestamp_utc','delivery_date'], filters=[('policy','==','B0')])


class SavedComponents:
    def __init__(self, root, fold, data):
        self.root, self.fold, self.data = root, fold, data
        self.issued = pd.read_parquet(root/f'reports/cp15/folds/{fold}-issued.parquet',
                                      filters=[('policy','in',['A1','B2'])])
        self.fits = pd.read_parquet(root/f'reports/cp15/folds/{fold}-fits.parquet',
                                    filters=[('policy','in',['A1','B2'])])
    def get(self, day):
        rows = self.data.rows(day)
        issued = self.issued.loc[self.issued.delivery_date.eq(day)]
        if issued.empty: return None
        result = {}; records = {}
        for policy in ('A1','B2'):
            arm = issued.loc[issued.policy.eq(policy)].sort_values('timestamp_utc')
            if not pd.DatetimeIndex(arm.timestamp_utc).equals(self.data.index[rows]):
                raise ValueError('cache target identity mismatch')
            if not arm.origin_utc.eq(origin_utc(day)).all(): raise ValueError('cache origin mismatch')
            if not np.array_equal(arm.scale.to_numpy(),self.data.scale[rows]):
                raise ValueError('cache origin scale mismatch')
            tr = np.flatnonzero((self.data.dates >= np.datetime64(history_start(day,policy))) &
                               (self.data.dates < np.datetime64(day)) & self.data.eligible)
            target = (self.data.y-self.data.level)/self.data.scale if policy=='A1' else self.data.y
            logs = self.fits.loc[self.fits.delivery_date.eq(str(day)) & self.fits.policy.eq(policy)]
            # Legacy Parquet stores ISO dates in fit records.
            if len(logs) != len(np.unique(self.data.hours[rows])): raise ValueError('cache fit record missing')
            check = {'train_rows_sha256':array_hash(tr), 'train_target_sha256':array_hash(target[tr]),
                     'normalization_rows_sha256':array_hash(np.column_stack((self.data.level[tr],self.data.scale[tr])))}
            for key, value in check.items():
                if not logs[key].eq(value).all(): raise ValueError('cache training identity mismatch: '+key)
            result[policy] = arm.central.to_numpy(float)
            if not np.isfinite(result[policy]).all(): raise ValueError('nonfinite cached component')
            records[policy] = logs.to_dict('records')
        return rows, result, records
