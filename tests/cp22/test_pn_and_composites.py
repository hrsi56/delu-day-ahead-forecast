"""PN's two forms, the composites and the ladder (capstone v21-r9 §20.2, §20.7, §20.10 item 3)."""
import numpy as np
import pytest

from cp21.lgbm import GRID, hg_central, hgl_central
from cp22.pn import AVERAGING_TOLERANCE, composite, pn_avg, select

RNG = np.random.default_rng(22)


def test_pn_avg_is_the_mean_of_four_and_inversion_commutes():
    for _ in range(50):
        n = int(RNG.integers(23, 26))
        scale = RNG.uniform(1, 80, n)
        level = RNG.uniform(-50, 400, n)
        z = [RNG.normal(0, 2, n) for _ in GRID]
        eur = [v * scale + level for v in z]
        after = pn_avg(eur)
        before = pn_avg(z) * scale + level
        assert np.max(np.abs(after - before)) <= AVERAGING_TOLERANCE
        assert np.allclose(after, np.mean(eur, axis=0), rtol=0, atol=1e-12)
    with pytest.raises(ValueError):
        pn_avg(eur[:3])
    # positive control: a non-affine map (e.g. clipping) does not commute
    clip = [np.maximum(v, 0) * scale + level for v in z]
    assert np.max(np.abs(pn_avg(clip) - (np.maximum(pn_avg(z), 0) * scale + level))) > 1e-6


def test_selection_lowest_loss_and_tie_to_smaller():
    assert select({'G1': 3., 'G2': 2., 'G3': 2.5, 'G4': 4.}) == 1
    assert select({'G1': 2., 'G2': 2., 'G3': 1., 'G4': 1.}) == 2       # exact tie -> smaller (G3)
    assert select({'G1': 1., 'G2': 1., 'G3': 1., 'G4': 1.}) == 0
    assert [g['id'] for g in GRID] == ['G1', 'G2', 'G3', 'G4']


def test_composite_parity_and_v4_identity():
    n = 24
    a1, b2, m1, m2 = (RNG.normal(80, 30, n) for _ in range(4))
    c_hg = hg_central(a1, b2)
    single = composite(a1, b2, ((m1, 3),))
    pair = composite(a1, b2, ((m1, 6), (m2, 6)))
    assert np.max(np.abs(single - (2 / 3) * c_hg - m1 / 3)) <= 1e-9
    assert np.max(np.abs(pair - (2 / 3) * c_hg - (m1 + m2) / 6)) <= 1e-9
    assert np.array_equal(pair, hgl_central(a1, b2, m1, m2))          # v4's own float expression, bit for bit
    for bad in (((m1, 2),), ((m1, 6),), ((m1, 3), (m2, 3))):
        with pytest.raises(ValueError):
            composite(a1, b2, bad)
    assert not np.allclose(single, composite(a1, b2, ((m2, 3),)))      # positive control: the member matters


#: Each member's three factors (§20.1's ladder). One change per step.
MEMBERS = {'L-N': ('normalized', 'blocks', 'selection'), 'L-R': ('raw', 'blocks', 'selection'),
           'L-P': ('raw', 'pooled', 'selection'), 'PN-sel': ('normalized', 'pooled', 'selection'),
           'PN-avg': ('normalized', 'pooled', 'average')}
POLICY_MEMBERS = {'v4': ('L-N', 'L-R'), 'M': ('PN-sel', 'L-P'), 'A-PN-sel': ('PN-sel',), 'R': ('PN-avg',)}


def _changes(a, b):
    return sum(x != y for x, y in zip(MEMBERS[a], MEMBERS[b]))


def test_ladder_one_change_per_step():
    # v4 -> M: the split removed; each member keeps its representation and its daily selection
    assert [_changes(a, b) for a, b in zip(POLICY_MEMBERS['v4'], POLICY_MEMBERS['M'])] == [1, 1]
    assert all(MEMBERS[a][1] == 'blocks' and MEMBERS[b][1] == 'pooled' for a, b in zip(POLICY_MEMBERS['v4'], POLICY_MEMBERS['M']))
    # M -> A-PN-sel: the raw half dropped, nothing else
    assert set(POLICY_MEMBERS['M']) - set(POLICY_MEMBERS['A-PN-sel']) == {'L-P'} and MEMBERS['L-P'][0] == 'raw'
    # A-PN-sel -> R: averaging instead of daily selection, nothing else
    assert _changes('PN-sel', 'PN-avg') == 1 and MEMBERS['PN-avg'][2] == 'average'
