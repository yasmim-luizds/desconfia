# Backend Desconfia

Consulte ../README.md para instalar e executar a versão web.
API: FastAPI; persistência: SQLAlchemy e PostgreSQL (SQLite local opcional).
Configuração: .env.example. Testes: python -m pytest -q.
O ambiente ativo fica em ../.venv; a pasta .venv antiga deste diretório não é utilizada.

## Migrações do banco

Execute os comandos em `backend/` com as dependências instaladas e `DATABASE_URL` apontando para a base correta.

- **Banco novo ou já versionado.** Rode `python -m alembic upgrade head` e confira com `python -m alembic current`. Em uma implantação de instância única, `RUN_MIGRATIONS=true` executa a atualização antes de iniciar a aplicação.
- **Banco legado da C2.** Faça backup e ensaie em uma cópia isolada. Rode `python -m app.adopt_baseline` para conferir e registrar a revisão inicial, depois `python -m alembic upgrade head`. Se a adoção detectar diferenças, revise a cópia antes de seguir.
- **Retorno de versão.** Confira a compatibilidade do código anterior com o esquema atual. As migrações bloqueiam o downgrade destrutivo. Se for necessário recuperar o esquema antigo, restaure o backup em uma base isolada.
