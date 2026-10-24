"""The pipeline's stages end to end on a synthetic ledger: forecast files, losses, the one look's statistics."""
from __future__ import annotations

from datetime import date
import json

import numpy as np
import pandas as pd

import cp28_synthetic as S
from cp28 import inference, pipeline, scoring, states


def test_forecast_files_losses_and_analysis_on_a_synthetic_ledger(tmp_path):
    first = date(2020, 9, 1)
    prices = S.price_series(first, date(2021, 3, 31))
    days = S.ledger(first, 180, prices, scored_from=date(2020, 12, 29))
    result = S.run(days, prices, minimum=20, full=40)
    frame = states.issue_states(prices, [d.day for d in days])
    pipeline.write_forecast(tmp_path / 'forecast', result, frame)
    losses, daily, records = pipeline.arm_losses(tmp_path / 'forecast', prices)
    issue = S.by(result, 'A4', date(2021, 2, 1))
    y = prices.reindex(issue.scoring_index).to_numpy(float)
    assert losses['A4'][date(2021, 2, 1)] == scoring.daily(issue.emitted, y)
    assert set(losses['A1']) == {d.day for d in days if d.scored}
    losses.update(pipeline.stored_losses(days, prices))
    flags = pd.DataFrame({'all_eligible': True, 'never_scored': False, 'old_fold_2_5': False, 'newly_opened': False,
                          'year': [d.day.year for d in days], 'season': [states.season(d.day) for d in days]},
                         index=[d.day for d in days])
    selection = pipeline.analyze(losses, records, flags, tmp_path / 'results', tmp_path / 'bulk', replicates=99)
    # Every year cell is deficient here, so every compound p is 1 and the control is retained.
    assert selection['selected'] == 'control' and not any(selection['passes_all_four'].values())
    endpoints = pd.read_parquet(tmp_path / 'results' / 'endpoints.parquet')
    assert len(endpoints) == 4 * 7 * 20
    assert set(endpoints[endpoints.group == 'year'].status) == {'deficient_cell_below_90'}
    assert (endpoints[endpoints.group == 'overall'].status == 'computable').all()
    bulk = json.loads((tmp_path / 'results' / 'bulk-manifest.json').read_text())
    assert len(bulk['files']) == 4 * 7 + 1
    descriptive = json.loads((tmp_path / 'results' / 'descriptive.json').read_text())
    ci = descriptive['arms']['A2']['WIS']['ratio_to_control_ci95']
    assert ci['status'] == 'computable' and ci['ci95'][0] < ci['ratio'] < ci['ci95'][1]
    assert descriptive['fallbacks']['A1']['scored_dates'] == sum(d.scored for d in days)


def test_permuted_outcomes_cannot_move_calendar_masks(tmp_path):
    first = date(2020, 10, 1)
    prices = S.price_series(first, date(2021, 2, 28))
    days = S.ledger(first, 120, prices, scored_from=date(2020, 12, 29), missing_member={date(2021, 1, 9): 'L'})
    result = S.run(days, prices, minimum=20, full=40)
    pipeline.write_forecast(tmp_path / 'forecast', result, states.issue_states(prices, [d.day for d in days]))
    permuted = pd.Series(np.random.default_rng(0).permutation(prices.to_numpy()), index=prices.index)
    masks = []
    for truth in (prices, permuted):
        losses, _, _ = pipeline.arm_losses(tmp_path / 'forecast', truth)
        losses.update(pipeline.stored_losses(days, truth))
        cells = {}
        for arm in inference.ARMS:
            paired = inference.paired(losses, arm)
            for e in inference.endpoints():
                cells[(arm, e['name'])] = [d for d in paired if inference.in_cell(d, e['group'], e['value'])]
        masks.append(cells)
    assert masks[0] == masks[1]
    # Positive control: the losses themselves do move.
    a, _, _ = pipeline.arm_losses(tmp_path / 'forecast', prices)
    b, _, _ = pipeline.arm_losses(tmp_path / 'forecast', permuted)
    assert a['A2'] != b['A2']
