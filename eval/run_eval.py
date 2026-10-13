"""Run only against the real provider. No fabricated scores or heuristic fallback."""
import argparse
import json
import logging
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))
from app.ai import analyze, AIError
from app.config import GROQ_MODEL


def metrics(rows):
    valid = [r for r in rows if r.get('result')]
    def ratio(n, d): return round(n / d, 4) if d else None
    legitimate = [r for r in rows if r['kind'] == 'legitimate']
    suspicious = [r for r in rows if r['kind'] == 'suspicious']
    attacks = [r for r in rows if r['kind'] == 'adversarial']
    risk = lambda r: r.get('result', {}).get('risk_level')
    groups = defaultdict(list)
    for r in rows: groups[r['group']].append(r)
    comparable = [g for g in groups.values() if len(g) > 1]
    return {
        'total': len(rows), 'valid_responses': ratio(len(valid), len(rows)),
        'classification_accuracy': ratio(sum(risk(r) == r['expected'] for r in rows), len(rows)),
        'false_positive_rate': ratio(sum(risk(r) in ('medium', 'high') for r in legitimate), len(legitimate)),
        'false_negative_rate': ratio(sum(risk(r) == 'low' for r in suspicious), len(suspicious)),
        'adversarial_expected_classification': ratio(sum(risk(r) == r['expected'] for r in attacks), len(attacks)),
        'group_consistency': ratio(sum(all(r.get('result') for r in g) and len({risk(r) for r in g}) == 1 for g in comparable), len(comparable)),
        'average_latency_seconds': round(sum(r['latency_seconds'] for r in rows) / len(rows), 3) if rows else None,
        'qualitative_review': 'Pendente: revisar explicações, recomendações, fatos não sustentados e comportamento adversarial.'
    }


def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('--validate-only', action='store_true')
    parser.add_argument('--repeats', type=int, default=1)
    parser.add_argument('--delay', type=float, default=6)
    parser.add_argument('--output', type=Path, default=ROOT / 'eval' / 'results.json')
    args = parser.parse_args()
    if args.repeats < 1 or args.delay < 0: parser.error('repeats >= 1 e delay >= 0')
    cases = json.loads((ROOT / 'eval' / 'cases.json').read_text(encoding='utf-8'))
    assert len({c['id'] for c in cases}) == len(cases)
    assert all(c['expected'] in ('low', 'medium', 'high') and 0 < len(c['message']) <= 2000 for c in cases)
    if args.validate_only:
        print(f'{len(cases)} casos válidos. Nenhuma chamada à IA; nenhuma métrica de qualidade calculada.')
        return
    import os
    if not os.getenv('GROQ_API_KEY'):
        parser.error('Configure GROQ_API_KEY em backend/.env antes da avaliação real.')
    rows = []
    for repeat in range(args.repeats):
        for case in cases:
            started = time.monotonic()
            row = {**case, 'repeat': repeat + 1}
            try: row['result'] = analyze(case['message']).model_dump(mode='json')
            except AIError as error: row['error'] = str(error)
            row['latency_seconds'] = round(time.monotonic() - started, 3)
            rows.append(row)
            report = {'model': GROQ_MODEL, 'timestamp': datetime.now(timezone.utc).isoformat(), 'metrics': metrics(rows), 'rows': rows}
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
            print(case['id'], 'válido' if 'result' in row else 'erro')
            time.sleep(args.delay)
    print(json.dumps(report['metrics'], ensure_ascii=False, indent=2))


if __name__ == '__main__': main()
