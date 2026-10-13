# Desconfia

Aplicação web do Projeto Integrador IV para apoiar a identificação de indícios de
golpes em mensagens textuais. Referência principal: relatório de planejamento
Desconfia. A proposta anterior foi usada apenas como apoio.

## Comece aqui no Windows

1. Abra `iniciar_demo.bat` nesta pasta.
2. Aguarde a instalação e a mensagem de que o servidor está disponível.
3. Abra http://127.0.0.1:8000 no navegador.
4. Crie uma conta e use a mensagem de exemplo.

O modo demonstração funciona sem conta na Groq, usando regras locais e um aviso
visível. Ele permite testar as telas; não representa a qualidade de uma IA.
O terminal precisa continuar aberto. Ctrl+C encerra o servidor. A primeira execução
precisa de internet para instalar dependências. O script usa Python/Node instalados
ou, neste computador, os runtimes disponíveis no Codex.

Em outro computador: Python 3.12+, Node.js 22+ e pnpm 11.25.0 (`npm install -g pnpm@11.25.0`).

## Ativar a IA real

1. Crie sua conta na Groq e gere uma chave: https://console.groq.com/keys.
2. Abra `backend/.env`, já preparado neste computador. Em outro computador, copie `backend/.env.example` para `backend/.env`.
3. Preencha `GROQ_API_KEY` e mantenha `AI_MODE=groq`. Um segredo de sessão já foi gerado localmente; em outra instalação, gere `DESCONFIA_SECRET_KEY`.
4. Execute `iniciar_local.bat`. Não use `iniciar_demo.bat` para testar a Groq.

Comando para gerar o segredo (rode localmente e copie o resultado para o arquivo):

```powershell
.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(48))"
```

A chave fica somente no back-end. Não a coloque em variáveis `VITE_`, arquivos
versionados, imagens ou mensagens. O modelo padrão é `openai/gpt-oss-20b`, com
resposta estruturada e validação adicional no servidor. Pode ser trocado por outro
modelo Groq compatível com JSON Schema estrito em `GROQ_MODEL`.
Fonte: https://console.groq.com/docs/structured-outputs.

## Estrutura

| Pasta | Função |
|---|---|
| `frontend/` | React + JavaScript + Vite, interface responsiva |
| `backend/app/` | FastAPI, autenticação, análise, histórico e feedback |
| `backend/tests/` | Testes automatizados com Pytest e serviço de IA simulado |
| `eval/` | Casos sintéticos e avaliação real da Groq |
| `docs/` | Arquitetura, requisitos, privacidade e publicação |
| `mobile/` | Protótipo anterior, preservado; não é a interface web desta entrega |

O fluxo é navegador → FastAPI → Groq → validação → banco → resultado no navegador.
Há cadastro, login, logout, análise, sinais, explicação, recomendação, histórico
paginado, feedback e exclusão de análise. O token fica em memória; atualizar a
página exige novo login. Ele expira em 8 horas. Logout remove a sessão do navegador;
não revoga um token que tenha sido copiado antes de sair.

## Banco

Sem `DATABASE_URL`, usa SQLite local para facilitar a demonstração. A implantação
prevista usa PostgreSQL via psycopg e SQLAlchemy. O modo `APP_ENV=production` exige
PostgreSQL, segredo de pelo menos 32 caracteres e `AI_MODE=groq`.

Para PostgreSQL local com Docker Desktop: copie `.env.example` da raiz para `.env`,
preencha senhas aleatórias alfanuméricas/URL-safe e execute `docker compose up --build`.
Use `AI_MODE=demo` nesse arquivo se ainda não tiver Groq. O volume mantém o banco.
Não execute `docker compose down -v` se quiser preservar os dados.

## Desenvolvimento e testes

Back-end (a partir da pasta `backend`):

```powershell
..\.venv\Scripts\python.exe -m pytest -q
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Front-end (outro terminal, na pasta `frontend`):

```text
pnpm install --frozen-lockfile
pnpm dev
pnpm test
pnpm build
```

O Vite encaminha as chamadas ao back-end em 8000. A versão compilada é servida
pelo próprio FastAPI. Reinicie o back-end se compilou a interface pela primeira vez
depois de iniciar o servidor. API documentada em http://127.0.0.1:8000/docs.

Na raiz: `.\.venv\Scripts\python.exe eval/run_eval.py --validate-only` valida os casos
sem chamadas externas. Leia `eval/README.md` antes de rodar a avaliação real.

## Limites da entrega

- Credencial Groq e conta de hospedagem ainda não fornecidas: chamadas reais,
  métricas de qualidade da IA e publicação dependem dessa configuração.
- Docker/PostgreSQL precisam ser validados em um ambiente que os tenha disponíveis.
- Os testes do serviço externo usam respostas simuladas; não demonstram resistência
  real a prompt injection ou acurácia do modelo.
- A aplicação não analisa imagens, áudio, QR Codes ou conteúdo de páginas externas.
- A criação inicial de tabelas é automática; futuras mudanças de esquema exigem
  migrações planejadas antes de atualizar um banco em produção.

Veja `docs/PUBLICACAO.md` e `docs/REQUISITOS.md` para os próximos passos.
