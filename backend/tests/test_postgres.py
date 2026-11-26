"""Real PostgreSQL CI check. Only an explicitly supplied disposable DB is allowed."""
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
import os

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect, select, text
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
        exercise_legacy_migration(engine, parsed)
        exercise_api(engine, monkeypatch)
        exercise_quota(engine, monkeypatch)
    finally:
        engine.dispose()


def exercise_legacy_migration(engine, parsed_url):
    with engine.begin() as connection:
        connection.execute(text('CREATE SCHEMA migration_c2'))
    legacy_url = parsed_url.update_query_dict({'options': '-csearch_path=migration_c2'}).render_as_string(hide_password=False)
    legacy_engine = create_engine(legacy_url)
    try:
        run_migration(legacy_url, 'alembic', 'upgrade', '0001')
        with legacy_engine.begin() as connection:
            connection.execute(text("INSERT INTO users VALUES ('legacy-user', 'Pessoa Teste', 'legacy@example.com', 'hash', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"))
            connection.execute(text("INSERT INTO analyses VALUES ('legacy-analysis', 'legacy-user', 'Mensagem sintética', 'high', 'Explicação', 'Recomendação', 'groq', 'modelo', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"))
            connection.execute(text("INSERT INTO analysis_indicators VALUES ('legacy-indicator', 'legacy-analysis', 'urgency', 'Urgência', 'sintética', CURRENT_TIMESTAMP)"))
            connection.execute(text("INSERT INTO feedbacks VALUES ('legacy-feedback', 'legacy-analysis', 'legacy-user', true, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"))
            connection.execute(text('DROP TABLE alembic_version'))
        run_migration(legacy_url, 'app.adopt_baseline')
        run_migration(legacy_url, 'alembic', 'upgrade', 'head')
        run_migration(legacy_url, 'alembic', 'upgrade', 'head')
        run_migration(legacy_url, 'alembic', 'check')
        with legacy_engine.connect() as connection:
            assert connection.execute(text('SELECT version_num FROM alembic_version')).scalar_one() == '0002'
            assert connection.execute(text('SELECT message_text, prompt_version FROM analyses')).one() == ('Mensagem sintética', None)
            assert connection.execute(text('SELECT count(*) FROM users')).scalar_one() == 1
            assert connection.execute(text('SELECT evidence FROM analysis_indicators')).scalar_one() == 'sintética'
            assert connection.execute(text('SELECT is_helpful FROM feedbacks')).scalar_one() is True
            assert connection.execute(text('SELECT count(*) FROM ai_quotas')).scalar_one() == 0
    finally:
        legacy_engine.dispose()


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
