"""Avaliação do provedor real; falhas de serviço não contam como classificações."""
import argparse
import json
import logging
import os
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))
from app.ai import analyze, AIError, PROMPT_VERSION
from app.config import GROQ_MODEL

SUSPICIOUS_KINDS = {'suspicious', 'variation'}


def metrics(rows):
    def ratio(n, d):
        return round(n / d, 4) if d else None

    valid = [r for r in rows if isinstance(r.get('result'), dict) and r['result'].get('risk_level') in ('low', 'medium', 'high')]
    failures = len(rows) - len(valid)
    legitimate = [r for r in valid if r['kind'] == 'legitimate' or (r['kind'] == 'variation' and r['expected'] == 'low')]
    suspicious = [r for r in valid if r['kind'] in SUSPICIOUS_KINDS and r['expected'] in ('medium', 'high')]
    attacks = [r for r in valid if r['kind'] == 'adversarial']
    risk = lambda r: r['result']['risk_level']
    correct = sum(risk(r) == r['expected'] for r in valid)
    fp = sum(risk(r) in ('medium', 'high') for r in legitimate)
    fn = sum(risk(r) == 'low' for r in suspicious)
    attack_correct = sum(risk(r) == r['expected'] for r in attacks)

    groups = defaultdict(list)
    for r in rows:
        groups[(r['group'], r.get('repeat', 1))].append(r)
    comparable = [g for g in groups.values() if len(g) > 1 and all(r in valid for r in g)]
    consistent = sum(len({risk(r) for r in g}) == 1 for g in comparable)
    total = len(rows)
    return {
        'total': total,
        'valid_responses': ratio(len(valid), total),
        'valid_response_count': len(valid), 'valid_response_denominator': total,
        'service_failure_count': failures, 'service_failure_denominator': total,
        'service_failure_rate': ratio(failures, total),
        'classification_accuracy': ratio(correct, len(valid)),
        'classification_correct_count': correct, 'classification_denominator': len(valid),
        'false_positive_rate': ratio(fp, len(legitimate)),
        'false_positive_count': fp, 'false_positive_denominator': len(legitimate),
        'false_negative_rate': ratio(fn, len(suspicious)),
        'false_negative_count': fn, 'false_negative_denominator': len(suspicious),
        'adversarial_expected_classification': ratio(attack_correct, len(attacks)),
        'adversarial_correct_count': attack_correct, 'adversarial_denominator': len(attacks),
        'group_consistency': ratio(consistent, len(comparable)),
        'consistent_group_count': consistent, 'comparable_group_denominator': len(comparable),
        'group_excluded_due_to_errors': sum(len(g) > 1 and not all(r in valid for r in g) for g in groups.values()),
        'average_latency_seconds': round(sum(r['latency_seconds'] for r in rows) / total, 3) if total else None,
        'qualitative_review': 'Revisar manualmente linguagem, justificativas, evidências, recomendações e alucinações.',
    }


def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('--validate-only', action='store_true')
    parser.add_argument('--repeats', type=int, default=1)
    parser.add_argument('--delay', type=float, default=6)
    parser.add_argument('--cases', type=Path, default=ROOT / 'eval' / 'cases.json')
    parser.add_argument('--output', type=Path, default=ROOT / 'eval' / 'results-v2.json')
    args = parser.parse_args()
    if args.repeats < 1 or args.delay < 0:
        parser.error('repeats >= 1 e delay >= 0')
    cases = json.loads(args.cases.read_text(encoding='utf-8'))
    if len({c['id'] for c in cases}) != len(cases):
        parser.error('IDs de casos duplicados')
    if not all(c['expected'] in ('low', 'medium', 'high') and 0 < len(c['message']) <= 2000 for c in cases):
        parser.error('Casos inválidos')
    if args.validate_only:
        print(f'{len(cases)} casos válidos. Nenhuma chamada à IA; nenhuma métrica de qualidade calculada.')
        return
    if args.output.resolve() == (ROOT / 'eval' / 'results.json').resolve():
        parser.error('results.json é a linha de base e não pode ser sobrescrito')
    if args.output.exists():
        parser.error('O arquivo de saída já existe. Escolha outro caminho para preservar avaliações anteriores.')
    if not os.getenv('GROQ_API_KEY'):
        parser.error('Configure GROQ_API_KEY em backend/.env antes da avaliação real.')
    rows = []
    for repeat in range(args.repeats):
        for case in cases:
            started = time.monotonic()
            row = {**case, 'repeat': repeat + 1}
            try:
                row['result'] = analyze(case['message']).model_dump(mode='json')
            except AIError as error:
                row['error'] = str(error)
            row['latency_seconds'] = round(time.monotonic() - started, 3)
            rows.append(row)
            report = {'model': GROQ_MODEL, 'prompt_version': PROMPT_VERSION,
                      'timestamp': datetime.now(timezone.utc).isoformat(),
                      'cases_file': args.cases.name, 'metrics': metrics(rows), 'rows': rows}
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
            print(case['id'], 'válido' if 'result' in row else 'erro')
            if args.delay:
                time.sleep(args.delay)
    print(json.dumps(report['metrics'], ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
