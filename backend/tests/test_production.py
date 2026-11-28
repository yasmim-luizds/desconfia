"""Regression checks for budget, persistence boundaries and authentication."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import os
import subprocess
import sys

import pytest
from fastapi import HTTPException
from jose import jwt
from sqlalchemy import create_engine, select
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app import ai, main, quota
from app.database import Base, get_db
from app.models import AIQuota, Analysis, User
from app.security import SECRET_KEY
from test_api import VERDICT


def test_shared_quota_blocks_other_accounts_without_provider_call(client, auth, monkeypatch):
    monkeypatch.setattr(quota, 'AI_GLOBAL_PER_MINUTE', 1)
    calls = []
    monkeypatch.setattr(ai, 'analyze', lambda text: calls.append(text) or ai.Verdict(**VERDICT))
    assert client.post('/analyses', headers=auth, json={'message_text': 'Pix agora'}).status_code == 201
    other = client.post('/auth/register', json={'full_name': 'Outra Conta', 'email': 'two@example.com', 'password': 'Teste123!'}).json()
    headers = {'Authorization': 'Bearer ' + other['access_token']}
    result = client.post('/analyses', headers=headers, json={'message_text': 'Pix agora'})
    assert result.status_code == 429
    assert 1 <= int(result.headers['Retry-After']) <= 60
    assert result.headers['X-Error-Code'] == 'ai_global_quota_exceeded'
    assert len(calls) == 1
    assert client.get('/analyses', headers=headers).json() == []


def test_provider_failure_consumes_budget_without_saving_result(client, auth, monkeypatch):
    monkeypatch.setattr(quota, 'AI_GLOBAL_PER_DAY', 1)
    def fail(_):
        raise ai.AIError('Serviço indisponível', 503)
    monkeypatch.setattr(ai, 'analyze', fail)
    assert client.post('/analyses', headers=auth, json={'message_text': 'Pix agora'}).status_code == 503
    assert client.post('/analyses', headers=auth, json={'message_text': 'Pix agora'}).status_code == 429
    assert client.get('/analyses', headers=auth).json() == []


def test_demo_does_not_consume_provider_budget(client, auth, monkeypatch):
    monkeypatch.setattr(main, 'AI_MODE', 'demo')
    data = client.post('/analyses', headers=auth, json={'message_text': 'Pix agora'}).json()
    assert data['prompt_version'] is None
    with Session(main.engine) as db:
        assert db.scalars(select(AIQuota)).all() == []


def test_prompt_provenance_survives_history(client, auth, monkeypatch):
    monkeypatch.setattr(ai, 'analyze', lambda _: ai.Verdict(**VERDICT))
    monkeypatch.setattr(ai, 'PROMPT_VERSION', 'test-version')
    data = client.post('/analyses', headers=auth, json={'message_text': 'Pix agora'}).json()
    monkeypatch.setattr(ai, 'PROMPT_VERSION', 'new-version')
    saved = client.get('/analyses/' + data['id'], headers=auth).json()
    assert saved['prompt_version'] == 'test-version'


def test_database_failure_is_safe_and_not_success(client, auth, monkeypatch):
    monkeypatch.setattr(ai, 'analyze', lambda _: ai.Verdict(**VERDICT))
    from sqlalchemy import event
    def fail_insert(conn, cursor, statement, parameters, context, executemany):
        if statement.startswith('INSERT INTO analyses'):
            raise OperationalError('private SQL', {}, Exception('private database detail'))
    event.listen(main.engine, 'before_cursor_execute', fail_insert)
    try:
        result = client.post('/analyses', headers=auth, json={'message_text': 'Pix agora'})
    finally:
        event.remove(main.engine, 'before_cursor_execute', fail_insert)
    assert result.status_code == 503
    assert result.headers['X-Error-Code'] == 'database_unavailable'
    assert 'private' not in result.text
    assert client.get('/analyses', headers=auth).json() == []


def test_expired_and_inactive_user_tokens_are_denied(client, auth):
    user_id = client.get('/me', headers=auth).json()['id']
    expired = jwt.encode({'sub': user_id, 'exp': datetime.now(timezone.utc) - timedelta(seconds=5)}, SECRET_KEY, algorithm='HS256')
    assert client.get('/me', headers={'Authorization': 'Bearer ' + expired}).status_code == 401
    with Session(main.engine) as db:
        db.get(User, user_id).is_active = False
        db.commit()
    assert client.get('/me', headers=auth).status_code == 401


def test_budget_concurrent_and_survives_reconnect(tmp_path, monkeypatch):
    url = 'sqlite:///' + str(tmp_path / 'budget.db')
    engine = create_engine(url, connect_args={'timeout': 15})
    Base.metadata.create_all(engine)
    monkeypatch.setattr(quota, 'AI_GLOBAL_PER_DAY', 4)
    monkeypatch.setattr(quota, 'AI_GLOBAL_PER_MINUTE', 4)
    monkeypatch.setattr(quota, 'time', lambda: 1800000000)
    def attempt(_):
        with Session(engine) as db:
            try:
                quota.reserve_attempt(db)
                return True
            except HTTPException as exc:
                assert exc.status_code == 429
                return False
    with ThreadPoolExecutor(max_workers=8) as pool:
        assert sum(pool.map(attempt, range(12))) == 4
    engine.dispose()
    engine = create_engine(url)
    assert attempt(None) is False
    with Session(engine) as db:
        assert {q.used for q in db.scalars(select(AIQuota))} == {4}
    monkeypatch.setattr(quota, 'time', lambda: 1800000000 + 86400)
    assert attempt(None) is True
    engine.dispose()


@pytest.mark.parametrize('overrides,fragment', [
    ({'GROQ_API_KEY': ''}, 'GROQ_API_KEY'),
    ({'DESCONFIA_SECRET_KEY': 'short'}, 'DESCONFIA_SECRET_KEY'),
    ({'AI_MODE': 'demo'}, 'AI_MODE'),
    ({'AI_GLOBAL_PER_DAY': '0'}, 'AI_GLOBAL_PER_DAY'),
    ({'AI_GLOBAL_PER_MINUTE': 'invalid'}, 'AI_GLOBAL_PER_MINUTE'),
    ({'DATABASE_URL': 'sqlite://'}, 'PostgreSQL'),
])
def test_invalid_production_config_fails_before_serving(overrides, fragment):
    env = {**os.environ, 'APP_ENV': 'production', 'GROQ_API_KEY': 'test-placeholder',
           'DESCONFIA_SECRET_KEY': 'x' * 48, 'AI_MODE': 'groq',
           'DATABASE_URL': 'postgresql+psycopg://test:test@localhost/test', **overrides}
    result = subprocess.run([sys.executable, '-c', 'import app.database'], env=env, capture_output=True, text=True)
    assert result.returncode != 0
    assert fragment in result.stderr
