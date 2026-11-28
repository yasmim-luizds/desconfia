import importlib.util
import json
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


def test_repeat_stability_separate_from_variations():
    rows = [
        row('legitimate', 'low', 'low', group='family', id='a', repeat=1),
        row('legitimate', 'low', 'low', group='family', id='b', repeat=1),
        row('legitimate', 'low', 'high', group='family', id='a', repeat=2),
        row('legitimate', 'low', 'low', group='family', id='b', repeat=2),
    ]
    m = module.metrics(rows)
    assert m['repeat_stability'] == 0.5
    assert m['stable_repeat_count'] == 1
    assert m['repeat_stability_denominator'] == 2
    assert m['group_consistency'] == 0.5


def test_repeat_stability_excludes_failed_runs_and_counts_categories():
    rows = [
        row('suspicious', 'high', 'high', group='bank', id='a', repeat=1),
        row('suspicious', 'high', None, group='bank', id='a', repeat=2, error_code='timeout'),
        row('suspicious', 'high', 'high', group='bank', id='b', repeat=1),
        row('suspicious', 'high', 'high', group='bank', id='b', repeat=2),
    ]
    m = module.metrics(rows)
    assert m['repeat_stability'] == 1
    assert m['repeat_stability_denominator'] == 1
    assert m['repeat_groups_excluded_due_to_errors'] == 1
    assert m['failure_categories'] == {'timeout': 1}


def test_repeat_stability_not_applicable_with_one_run_or_empty_data():
    only_once = [row('legitimate', 'low', 'low', id='a', repeat=1)]
    assert module.metrics(only_once)['repeat_stability'] is None
    assert module.metrics(only_once)['repeat_stability_denominator'] == 0
    assert module.metrics([])['repeat_stability'] is None


def test_attack_risk_classification_is_not_attack_obedience_score():
    m = module.metrics([row('adversarial', 'high', 'high', id='x')])
    assert m['adversarial_expected_classification'] == 1
    assert 'N/A' in m['adversarial_obedience_review']


def test_repeat_stability_excludes_interrupted_and_duplicate_rounds():
    interrupted = [row('legitimate', 'low', 'low', id='a', repeat=n) for n in (1, 2)]
    result = module.metrics(interrupted, expected_repeats=3)
    assert result['repeat_stability'] is None
    assert result['repeat_groups_excluded_due_to_incomplete_runs'] == 1
    complete = interrupted + [row('legitimate', 'low', 'low', id='a', repeat=3)]
    assert module.metrics(complete, expected_repeats=3)['repeat_stability'] == 1
    duplicate = interrupted + [row('legitimate', 'low', 'low', id='a', repeat=2)]
    assert module.metrics(duplicate, expected_repeats=3)['repeat_stability'] is None


def test_rate_limit_stops_run_and_preserves_partial_report(monkeypatch, tmp_path):
    cases = tmp_path / 'cases.json'
    output = tmp_path / 'results.json'
    cases.write_text(json.dumps([{'id': 'synthetic', 'kind': 'legitimate', 'group': 'unit',
                                 'message': 'Bom dia', 'expected': 'low'}]), encoding='utf-8')
    calls = []
    def limited(message):
        calls.append(message)
        raise module.AIError('Limite', 429, 'provider_rate_limit')
    monkeypatch.setenv('GROQ_API_KEY', 'synthetic-test-key')
    monkeypatch.setattr(module, 'analyze', limited)
    monkeypatch.setattr(module.sys, 'argv', ['run_eval.py', '--cases', str(cases), '--output', str(output),
                                            '--repeats', '3', '--delay', '0', '--stop-on-rate-limit'])
    with pytest.raises(SystemExit) as stopped:
        module.main()
    assert stopped.value.code == 3
    assert calls == ['Bom dia']
    report = json.loads(output.read_text(encoding='utf-8'))
    assert report['completed'] is False
    assert report['expected_attempts'] == 3
    assert report['stopped_reason'] == 'provider_rate_limit'
    assert report['rows'][0]['error_code'] == 'provider_rate_limit'
    assert report['metrics']['repeat_stability'] is None
    assert report['source_sha256']['backend/app/ai.py']
    assert report['source_hash_method'] == 'utf8_text_lf'
