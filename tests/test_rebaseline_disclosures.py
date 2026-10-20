"""Reporting qualifications must survive structured and rendered presentation."""
import copy
import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location('rebaseline_disclosures',
    Path(__file__).resolve().parents[1] / 'scripts/render_rebaseline_disclosures.py')
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)


def surfaces():
    original = {'schema': 'cp26-report-v1', 'limitations': ['Existing limitation.'],
                'primary': [{'raw_mean_daily_loss': 18.45974841331334}], 'seed': 20261013}
    report = R.qualify(original, {'fixture': True})
    packet = {'reporting_disclosures': R.records(), 'slots': {'limitations': report['limitations'][:]}}
    text = '\n'.join(R.disclosure_lines())
    return original, report, packet, text, text


def test_four_source_bound_disclosures_preserve_original_science():
    original, report, packet, report_md, packet_md = surfaces()
    R.validate_disclosures(report, packet, report_md, packet_md)
    R.assert_science_unchanged(original, report)
    assert original['limitations'] == ['Existing limitation.']
    assert len(report['reporting_disclosures']) == 4
    assert {x['source']['section'] for x in R.records()} == {'1', '2', '3', '4'}


@pytest.mark.parametrize('index', range(4))
@pytest.mark.parametrize('surface', ('report', 'packet', 'report_md', 'packet_md'))
def test_each_omitted_qualification_is_rejected_on_each_surface(index, surface):
    _, report, packet, report_md, packet_md = surfaces()
    line = R.disclosure_lines()[index]
    if surface == 'report':
        report['limitations'].remove(line)
    elif surface == 'packet':
        packet['slots']['limitations'].remove(line)
    elif surface == 'report_md':
        report_md = report_md.replace(line, '')
    else:
        packet_md = packet_md.replace(line, '')
    with pytest.raises(ValueError, match='missing reporting qualification'):
        R.validate_disclosures(report, packet, report_md, packet_md)


def test_wrong_source_binding_and_changed_numeric_result_are_rejected():
    original, report, packet, report_md, packet_md = surfaces()
    packet['reporting_disclosures'][0]['source']['sha256'] = '0' * 64
    with pytest.raises(ValueError, match='source-bound'):
        R.validate_disclosures(report, packet, report_md, packet_md)
    altered = copy.deepcopy(report)
    altered['primary'][0]['raw_mean_daily_loss'] += 1
    with pytest.raises(ValueError, match='scientific fields'):
        R.assert_science_unchanged(original, altered)
