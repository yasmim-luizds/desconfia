"""Real PostgreSQL CI check. Only an explicitly supplied disposable DB is allowed."""
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
import os

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect, select
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session

from app import ai, limits, main, quota
from app.database import get_db
from app.models import AIQuota, AnalysisIndicator, Feedback
from test_api import VERDICT
from test_migrations import run_migration


TEST_TIME = 1_800_000_000


@pytest.mark.skipif(not os.getenv('TEST_POSTGRES_URL'), reason='Disposable PostgreSQL not configured')
def test_postgres_migrations_api_persistence_and_quota(monkeypatch):
    url = os.environ['TEST_POSTGRES_URL']
    parsed = make_url(url)
    assert parsed.get_backend_name() == 'postgresql'
    assert parsed.database == 'desconfia_test', 'Use only the disposable CI database'
    engine = create_engine(url, pool_pre_ping=True)
    try:
        assert inspect(engine).get_table_names() == [], 'Use an empty disposable database'
        run_migration(url, 'alembic', 'upgrade', 'head')
        run_migration(url, 'alembic', 'check')
        exercise_api(engine, monkeypatch)
        exercise_quota(engine, monkeypatch)
    finally:
        engine.dispose()


def exercise_api(engine, monkeypatch):
    def postgres_session():
        with Session(engine) as session:
            yield session

    monkeypatch.setattr(main, 'engine', engine)
    monkeypatch.setattr(main, 'PRODUCTION', True)
    monkeypatch.setattr(ai, 'analyze', lambda _: ai.Verdict(**VERDICT))
    monkeypatch.setattr(quota, 'time', lambda: TEST_TIME)
    monkeypatch.setitem(main.app.dependency_overrides, get_db, postgres_session)
    monkeypatch.setattr(limits, '_entries', OrderedDict())
    credentials = {'email': 'postgres@example.com', 'password': 'Teste123!'}
    with TestClient(main.app) as client:
        assert client.get('/health').json()['database'] == 'connected'
        registration = client.post('/auth/register', json={**credentials, 'full_name': 'Pessoa Teste'})
        assert registration.status_code == 201
        headers = {'Authorization': f"Bearer {registration.json()['access_token']}"}
        response = client.post('/analyses', headers=headers,
                               json={'message_text': 'Faça Pix agora', 'store_message': True})
        assert response.status_code == 201
        analysis = response.json()
        path = f"/analyses/{analysis['id']}"
        feedback = client.post(f'{path}/feedback', headers=headers, json={'is_helpful': True})
        assert feedback.status_code == 201

    engine.dispose()
    with TestClient(main.app) as client:
        login = client.post('/auth/login', json=credentials)
        assert login.status_code == 200
        headers = {'Authorization': f"Bearer {login.json()['access_token']}"}
        saved = client.get('/analyses', headers=headers).json()
        assert saved == [analysis]
        assert saved[0]['indicators'][0]['evidence'] == 'agora'
        assert saved[0]['prompt_version'] == ai.PROMPT_VERSION
        assert client.get(f'{path}/feedback', headers=headers).json() == feedback.json()
        assert client.delete(path, headers=headers).status_code == 204
        assert client.get(path, headers=headers).status_code == 404
    with Session(engine) as session:
        assert session.scalar(select(AnalysisIndicator.id)) is None
        assert session.scalar(select(Feedback.id)) is None


def exercise_quota(engine, monkeypatch):
    now = TEST_TIME + 86400
    monkeypatch.setattr(quota, 'AI_GLOBAL_PER_DAY', 4)
    monkeypatch.setattr(quota, 'AI_GLOBAL_PER_MINUTE', 4)
    monkeypatch.setattr(quota, 'time', lambda: now)

    def reserve(_):
        with Session(engine) as session:
            try:
                quota.reserve_attempt(session)
                return True
            except HTTPException as exc:
                assert exc.status_code == 429
                return False

    with ThreadPoolExecutor(max_workers=8) as pool:
        assert sum(pool.map(reserve, range(12))) == 4
    engine.dispose()
    with Session(engine) as session:
        with pytest.raises(HTTPException) as denied:
            quota.reserve_attempt(session)
        assert denied.value.status_code == 429
    with Session(engine) as session:
        used = session.scalars(select(AIQuota.used).where(AIQuota.window_start >= now // 86400 * 86400))
        assert sorted(used) == [4, 4]
