import os
from pathlib import Path
import subprocess
import sys

import pytest
from sqlalchemy import create_engine, inspect, text

from app.schema import prepare_schema

BACKEND = Path(__file__).resolve().parents[1]


def run_migration(url, *args):
    env = {**os.environ, 'DATABASE_URL': url, 'APP_ENV': 'test'}
    result = subprocess.run([sys.executable, '-m', *args], cwd=BACKEND, env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_fresh_schema_and_existing_c2_data(tmp_path):
    url = 'sqlite:///' + str(tmp_path / 'upgrade.db')
    run_migration(url, 'alembic', 'upgrade', '0001')
    engine = create_engine(url)
    with engine.begin() as c:
        c.execute(text("INSERT INTO users VALUES ('u', 'Teste', 'test@example.com', 'hash', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"))
        c.execute(text("INSERT INTO analyses VALUES ('a', 'u', 'mensagem sintética', 'low', 'explicação', 'recomendação', 'groq', 'modelo', CURRENT_TIMESTAMP, NULL)"))
        c.execute(text('DROP TABLE alembic_version'))  # Simulate the original unversioned C2 schema.
    with pytest.raises(RuntimeError, match='desatualizado'):
        prepare_schema(engine, production=True)
    run_migration(url, 'app.adopt_baseline')
    run_migration(url, 'alembic', 'upgrade', 'head')
    run_migration(url, 'alembic', 'upgrade', 'head')
    prepare_schema(engine, production=True)
    with engine.connect() as c:
        row = c.execute(text('SELECT message_text, prompt_version FROM analyses')).one()
        assert row == ('mensagem sintética', None)
        assert c.execute(text('SELECT count(*) FROM users')).scalar() == 1
    assert 'ai_quotas' in inspect(engine).get_table_names()
    engine.dispose()


def test_empty_db_upgrade(tmp_path):
    url = 'sqlite:///' + str(tmp_path / 'fresh.db')
    run_migration(url, 'alembic', 'upgrade', 'head')
    engine = create_engine(url)
    prepare_schema(engine, production=True)
    run_migration(url, 'alembic', 'check')
    engine.dispose()


def test_empty_local_database_is_created_and_versioned(tmp_path):
    engine = create_engine('sqlite:///' + str(tmp_path / 'local.db'))
    prepare_schema(engine, production=False)
    prepare_schema(engine, production=True)
    with engine.connect() as connection:
        assert connection.execute(text('SELECT version_num FROM alembic_version')).scalar() == '0002'
    engine.dispose()


def test_adoption_refuses_unknown_schema(tmp_path):
    url = 'sqlite:///' + str(tmp_path / 'unknown.db')
    engine = create_engine(url)
    with engine.begin() as c:
        c.execute(text('CREATE TABLE important_data (id INTEGER)'))
    result = subprocess.run([sys.executable, '-m', 'app.adopt_baseline'], cwd=BACKEND,
                            env={**os.environ, 'DATABASE_URL': url, 'APP_ENV': 'test'}, capture_output=True)
    assert result.returncode != 0
    assert inspect(engine).get_table_names() == ['important_data']
    engine.dispose()
