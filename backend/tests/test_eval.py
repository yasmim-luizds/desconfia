import importlib.util
from pathlib import Path

path = Path(__file__).resolve().parents[2] / 'eval' / 'run_eval.py'
spec = importlib.util.spec_from_file_location('evaluation', path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_metrics_count_errors_and_actual_denominators():
    rows = [
        {'kind': 'legitimate', 'group': 'a', 'expected': 'low', 'result': {'risk_level': 'high'}, 'latency_seconds': 1},
        {'kind': 'suspicious', 'group': 'b', 'expected': 'high', 'result': {'risk_level': 'low'}, 'latency_seconds': 1},
        {'kind': 'adversarial', 'group': 'b', 'expected': 'high', 'error': 'timeout', 'latency_seconds': 1},
    ]
    result = module.metrics(rows)
    assert result['classification_accuracy'] == 0
    assert result['false_positive_rate'] == 1
    assert result['false_negative_rate'] == 1
    assert result['valid_responses'] == 0.6667
    assert result['group_consistency'] == 0
    assert module.metrics([])['classification_accuracy'] is None
