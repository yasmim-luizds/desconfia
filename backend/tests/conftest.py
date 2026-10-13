import os
os.environ['DATABASE_URL'] = 'sqlite://'
os.environ['DESCONFIA_SECRET_KEY'] = 'test-only-secret-not-for-production-123456789'
os.environ['AI_MODE'] = 'groq'
os.environ['APP_ENV'] = 'test'

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.limits import _entries


@pytest.fixture
def client():
    engine = create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    def override_db():
        with Session(engine) as session:
            yield session
    app.dependency_overrides[get_db] = override_db
    _entries.clear()
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
    engine.dispose()


@pytest.fixture
def auth(client):
    result = client.post('/auth/register', json={'full_name': 'Pessoa Teste', 'email': 'teste@example.com', 'password': 'Teste123!'}).json()
    return {'Authorization': f"Bearer {result['access_token']}"}
