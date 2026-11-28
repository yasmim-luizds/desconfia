"""Avaliação do provedor real; falhas de serviço não contam como classificações."""
import argparse
import hashlib
import json
import logging
import os
import subprocess
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


def metrics(rows, expected_repeats=None):
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

    # Distinto de consistência entre variações: mesmo ID em rodadas diferentes.
    repetitions = defaultdict(list)
    for r in rows:
        if r.get('id') is not None:
            repetitions[r['id']].append(r)
    expected_rounds = set(range(1, expected_repeats + 1)) if expected_repeats is not None else None
    incomplete = [g for g in repetitions.values() if expected_rounds is not None and
                  (len(g) != expected_repeats or {r.get('repeat', 1) for r in g} != expected_rounds)]
    candidates = [g for g in repetitions.values() if g not in incomplete and
                  len({r.get('repeat', 1) for r in g}) >= 2]
    stable_comparable = [g for g in candidates if all(r in valid for r in g)]
    stable_count = sum(len({risk(r) for r in g}) == 1 for g in stable_comparable)
    repeat_excluded = len(candidates) - len(stable_comparable)

    failure_reasons = defaultdict(int)
    for r in rows:
        if r not in valid:
            failure_reasons[r.get('error_code', 'unknown')] += 1
    total = len(rows)
    return {
        'total': total,
        'valid_responses': ratio(len(valid), total),
        'valid_response_count': len(valid), 'valid_response_denominator': total,
        'service_failure_count': failures, 'service_failure_denominator': total,
        'service_failure_rate': ratio(failures, total),
        'failure_categories': dict(sorted(failure_reasons.items())),
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
        'repeat_stability': ratio(stable_count, len(stable_comparable)),
        'stable_repeat_count': stable_count,
        'repeat_stability_denominator': len(stable_comparable),
        'repeat_groups_excluded_due_to_errors': repeat_excluded,
        'repeat_groups_excluded_due_to_incomplete_runs': len(incomplete),
        'group_excluded_due_to_errors': sum(len(g) > 1 and not all(r in valid for r in g) for g in groups.values()),
        'average_latency_seconds': round(sum(r['latency_seconds'] for r in rows) / total, 3) if total else None,
        'qualitative_review': 'Revisar manualmente linguagem, justificativas, evidências, recomendações e alucinações.',
        'adversarial_obedience_review': 'N/A até revisão humana: obediência indevida, formato/idioma e contaminação da justificativa; classificação de risco não basta.',
    }


def source_metadata():
    paths = ['backend/app/ai.py', 'backend/app/config.py', 'backend/app/models.py', 'eval/run_eval.py']
    hashes = {path: hashlib.sha256((ROOT / path).read_text(encoding='utf-8').encode('utf-8')).hexdigest()
              for path in paths}
    try:
        commit = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT,
                                capture_output=True, text=True, timeout=3, check=True).stdout.strip()
        changed = subprocess.run(['git', 'diff', '--quiet', 'HEAD', '--', *paths], cwd=ROOT,
                                 capture_output=True, timeout=3)
        dirty = changed.returncode != 0 if changed.returncode in (0, 1) else None
    except (OSError, subprocess.SubprocessError):
        commit, dirty = None, None
    return {'commit': commit, 'source_dirty': dirty, 'source_sha256': hashes,
            'source_hash_method': 'utf8_text_lf'}


def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('--validate-only', action='store_true')
    parser.add_argument('--repeats', type=int, default=1)
    parser.add_argument('--delay', type=float, default=6)
    parser.add_argument('--stop-on-rate-limit', action='store_true',
                        help='Preserva a tentativa e interrompe a rodada ao receber limite do provedor.')
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
    provenance = source_metadata()
    run_started = datetime.now(timezone.utc).isoformat()
    cases_sha256 = hashlib.sha256(args.cases.read_bytes()).hexdigest()
    rows = []
    for repeat in range(args.repeats):
        for case in cases:
            started = time.monotonic()
            row = {**case, 'repeat': repeat + 1}
            try:
                row['result'] = analyze(case['message']).model_dump(mode='json')
            except AIError as error:
                row['error'] = str(error)
                row['error_code'] = error.code
                row['error_status'] = error.status_code
            row['latency_seconds'] = round(time.monotonic() - started, 3)
            rows.append(row)
            stop = args.stop_on_rate_limit and row.get('error_code') == 'provider_rate_limit'
            report = {'model': GROQ_MODEL, 'prompt_version': PROMPT_VERSION,
                      **provenance, 'timestamp': datetime.now(timezone.utc).isoformat(),
                      'recommendation_source': 'application_policy',
                      'run_started_at': run_started, 'temperature': 0,
                      'repeats_requested': args.repeats, 'delay_seconds': args.delay,
                      'cases_file': args.cases.name, 'cases_sha256': cases_sha256,
                      'expected_attempts': len(cases) * args.repeats,
                      'completed': len(rows) == len(cases) * args.repeats,
                      'stopped_reason': 'provider_rate_limit' if stop else None,
                      'metrics': metrics(rows, expected_repeats=args.repeats), 'rows': rows}
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
            print(case['id'], 'válido' if 'result' in row else 'erro')
            if stop:
                print('Rodada interrompida pelo limite do provedor. Tentativa preservada; sem retentativa automática.')
                raise SystemExit(3)
            if args.delay:
                time.sleep(args.delay)
    print(json.dumps(report['metrics'], ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
