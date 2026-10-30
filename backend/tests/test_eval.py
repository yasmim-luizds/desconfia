import importlib.util
from pathlib import Path

import pytest

path = Path(__file__).resolve().parents[2] / 'eval' / 'run_eval.py'
spec = importlib.util.spec_from_file_location('evaluation', path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def row(kind, expected, result=None, group='unit', **kwargs):
    data = {'kind': kind, 'expected': expected, 'group': group, 'latency_seconds': 1, **kwargs}
    if result is not None:
        data['result'] = {'risk_level': result}
    else:
        data['error'] = 'timeout'
    return data


def test_failures_not_counted_as_wrong_classifications():
    rows = [row('legitimate', 'low', 'low'), row('suspicious', 'high', None),
            row('suspicious', 'high', 'high')]
    result = module.metrics(rows)
    assert result['total'] == 3
    assert result['service_failure_count'] == 1
    assert result['service_failure_denominator'] == 3
    assert result['classification_correct_count'] == 2
    assert result['classification_denominator'] == 2
    assert result['classification_accuracy'] == 1
    assert result['valid_responses'] == 0.6667


def test_suspicious_variations_included_in_false_negatives():
    rows = [row('suspicious', 'high', 'high'), row('variation', 'high', 'low'),
            row('variation', 'low', 'high'), row('legitimate', 'low', 'low')]
    result = module.metrics(rows)
    assert result['false_negative_count'] == 1
    assert result['false_negative_denominator'] == 2
    assert result['false_negative_rate'] == 0.5
    assert result['false_positive_count'] == 1
    assert result['false_positive_denominator'] == 2
    assert result['false_positive_rate'] == 0.5


def test_adversarial_and_groups_ignore_failed_calls():
    rows = [row('adversarial', 'high', None, group='attack'),
            row('adversarial', 'high', 'high', group='attack'),
            row('suspicious', 'high', 'high', group='family'),
            row('variation', 'high', 'high', group='family')]
    result = module.metrics(rows)
    assert result['adversarial_correct_count'] == 1
    assert result['adversarial_denominator'] == 1
    assert result['comparable_group_denominator'] == 1
    assert result['group_consistency'] == 1
    assert result['group_excluded_due_to_errors'] == 1


def test_no_valid_rows_have_null_denominators():
    result = module.metrics([row('suspicious', 'high')])
    assert result['classification_accuracy'] is None
    assert result['false_negative_rate'] is None
    assert result['service_failure_rate'] == 1
    assert module.metrics([])['valid_responses'] is None
