import pytest
from app import ai
from app.security import hash_password, verify_password

VERDICT = {'risk_level': 'high', 'explanation': 'Há urgência e solicitação financeira.', 'recommendation': 'Confirme por outro canal.', 'indicators': [{'category': 'urgency', 'description': 'Urgência', 'evidence': 'agora'}]}


def test_registration_login_and_password(client, auth):
    assert client.get('/me', headers=auth).json()['email'] == 'teste@example.com'
    assert client.post('/auth/login', json={'email': 'TESTE@example.com', 'password': 'Teste123!'}).status_code == 200
    assert client.post('/auth/login', json={'email': 'teste@example.com', 'password': 'errada'}).status_code == 401
    assert client.post('/auth/register', json={'full_name': 'Teste', 'email': 'teste@example.com', 'password': 'Teste123!'}).status_code == 409
    hashed = hash_password('Teste123!')
    assert hashed != 'Teste123!' and verify_password('Teste123!', hashed)


@pytest.mark.parametrize('body', [{'full_name': '  ', 'email': 'a@example.com', 'password': 'Teste123!'}, {'full_name': 'Teste', 'email': 'invalido', 'password': 'Teste123!'}, {'full_name': 'Teste', 'email': 'a@example.com', 'password': 'curta'}])
def test_invalid_registration(client, body):
    assert client.post('/auth/register', json=body).status_code == 422


@pytest.mark.parametrize('message', ['', '   ', 'x' * 2001])
def test_invalid_message(client, auth, message):
    assert client.post('/analyses', headers=auth, json={'message_text': message}).status_code == 422


def test_access_control_privacy_feedback_and_delete(client, auth, monkeypatch):
    monkeypatch.setattr(ai, 'analyze', lambda text: ai.Verdict(**VERDICT))
    assert client.get('/analyses').status_code == 401
    assert client.get('/analyses', headers={'Authorization': 'Bearer invalid'}).status_code == 401
    response = client.post('/analyses', headers=auth, json={'message_text': 'Faça Pix agora'})
    assert response.status_code == 201
    analysis = response.json()
    assert analysis['message_text'] == ''
    assert analysis['indicators'][0]['evidence'] is None
    assert analysis['ai_provider'] == 'groq'
    analysis_id = analysis['id']
    other = client.post('/auth/register', json={'full_name': 'Outra Pessoa', 'email': 'outro@example.com', 'password': 'Teste123!'}).json()
    other_auth = {'Authorization': f"Bearer {other['access_token']}"}
    assert client.get('/analyses', headers=other_auth).json() == []
    for method, suffix, body in [('get', '', None), ('delete', '', None), ('get', '/feedback', None), ('post', '/feedback', {'is_helpful': True})]:
        kwargs = {'headers': other_auth}
        if body: kwargs['json'] = body
        assert getattr(client, method)(f'/analyses/{analysis_id}{suffix}', **kwargs).status_code == 404
    assert client.get(f'/analyses/{analysis_id}/feedback', headers=auth).json() is None
    assert client.post(f'/analyses/{analysis_id}/feedback', headers=auth, json={'is_helpful': True}).status_code == 201
    assert client.post(f'/analyses/{analysis_id}/feedback', headers=auth, json={'is_helpful': True}).status_code == 409
    assert client.get(f'/analyses/{analysis_id}/feedback', headers=auth).json()['is_helpful'] is True
    assert client.delete(f'/analyses/{analysis_id}', headers=auth).status_code == 204
    assert client.get('/analyses', headers=auth).json() == []
    assert client.get(f'/analyses/{analysis_id}', headers=auth).status_code == 404


def test_store_opt_in_and_pagination(client, auth, monkeypatch):
    monkeypatch.setattr(ai, 'analyze', lambda text: ai.Verdict(**VERDICT))
    for _ in range(3):
        data = client.post('/analyses', headers=auth, json={'message_text': 'Faça Pix agora', 'store_message': True}).json()
        assert data['message_text'] == 'Faça Pix agora'
        assert data['indicators'][0]['evidence'] == 'agora'
    first = client.get('/analyses?limit=2', headers=auth).json()
    second = client.get('/analyses?limit=2&offset=2', headers=auth).json()
    assert len(first) == 2 and len(second) == 1
    assert {x['id'] for x in first}.isdisjoint({x['id'] for x in second})


def test_provider_error_does_not_save(client, auth, monkeypatch):
    def fail(_): raise ai.AIError('Indisponível', 503)
    monkeypatch.setattr(ai, 'analyze', fail)
    assert client.post('/analyses', headers=auth, json={'message_text': 'Teste'}).status_code == 503
    assert client.get('/analyses', headers=auth).json() == []


def test_rate_limit(client):
    for _ in range(20):
        assert client.post('/auth/login', json={'email': 'x@example.com', 'password': 'wrong'}).status_code == 401
    assert client.post('/auth/login', json={'email': 'x@example.com', 'password': 'wrong'}).status_code == 429


def test_health_and_headers(client):
    response = client.get('/health')
    assert response.json()['database'] == 'connected'
    assert response.headers['x-content-type-options'] == 'nosniff'


def test_password_spaces_are_preserved(client):
    payload = {'full_name': ' Pessoa ', 'email': 'space@example.com', 'password': ' Password123! '}
    assert client.post('/auth/register', json=payload).status_code == 201
    assert client.post('/auth/login', json={'email': payload['email'], 'password': payload['password']}).status_code == 200
    assert client.post('/auth/login', json={'email': payload['email'], 'password': payload['password'].strip()}).status_code == 401
