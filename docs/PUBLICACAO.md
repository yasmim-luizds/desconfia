# Publicação do Desconfia — C3

## Versão publicada

- Aplicação: [https://desconfia.onrender.com/](https://desconfia.onrender.com/).
- Hospedagem: serviço web Docker no Render.
- Banco persistente: PostgreSQL no Neon.
- Código publicado: [`4b9d1603d5dcdb884e25d659fd15de5e97182fff`](https://github.com/yasmim-luizds/desconfia/commit/4b9d1603d5dcdb884e25d659fd15de5e97182fff), após os PRs #8, #9, #10 e #11.
- Verificação automática dessa versão: [GitHub Actions — backend, frontend, PostgreSQL e imagem Docker aprovados](https://github.com/yasmim-luizds/desconfia/actions/runs/46099940488).

O uso desta entrega é acadêmico, com contas e mensagens sintéticas.

## Configuração do serviço no Render

O `Dockerfile` da raiz compila o frontend e prepara o backend. O FastAPI serve a interface e a API no mesmo endereço. O banco Neon permanece externo ao container da aplicação.

| Campo | Configuração do projeto |
|---|---|
| Repositório | `yasmim-luizds/desconfia` |
| Branch de integração | `main` |
| Runtime / Language | Docker |
| Root Directory | Raiz do repositório; campo vazio |
| Dockerfile Path | `./Dockerfile` |
| Docker Command | Usar o `CMD` do Dockerfile: `sh ./start.sh` |
| Health Check Path | `/health` |

No serviço existente, manter o banco Neon e os segredos já cadastrados. Para reproduzir a configuração, usar as variáveis abaixo em **Environment**. Esta tabela informa nomes e requisitos; os valores secretos são preenchidos no painel.

| Variável | Valor ou origem |
|---|---|
| `APP_ENV` | `production` |
| `AI_MODE` | `groq` |
| `GROQ_MODEL` | `openai/gpt-oss-20b`, modelo da avaliação 2.2.2 |
| `GROQ_API_KEY` | Chave da conta Groq, cadastrada somente no ambiente do backend |
| `DATABASE_URL` | Conexão PostgreSQL do Neon com TLS; o backend aceita `postgresql://` ou `postgresql+psycopg://` |
| `DESCONFIA_SECRET_KEY` | Segredo persistente com pelo menos 32 caracteres |
| `RUN_MIGRATIONS` | `true` para executar Alembic antes da inicialização em banco novo ou já versionado, com uma instância |
| `AI_GLOBAL_PER_MINUTE` | Padrão do código: `20`; limite compartilhado de tentativas |
| `AI_GLOBAL_PER_DAY` | Padrão do código: `200`; limite compartilhado de tentativas |
| `CORS_ORIGINS` | Configurar origens HTTPS exatas quando houver frontend separado |

O Render fornece `PORT`, que é lida por `backend/start.sh`. O processo inicia um worker do Uvicorn. O segredo da aplicação deve permanecer estável entre publicações para preservar a validação dos tokens emitidos.

Para gerar um segredo em ambiente privado:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

## Publicar ou atualizar por commit

1. Abrir o serviço Desconfia no [painel do Render](https://dashboard.render.com/).
2. Em **Settings**, conferir a branch `main`, o runtime Docker e o healthcheck `/health`.
3. Em **Environment**, conferir as variáveis da tabela, mantendo conexão e segredos do serviço existente.
4. Em **Deploys**, selecionar **Manual Deploy → Deploy a specific commit**.
5. Informar o SHA aprovado. Na publicação registrada pela equipe foi usado `4b9d1603d5dcdb884e25d659fd15de5e97182fff`.
6. Selecionar **Deploy Commit** e acompanhar os logs até **Live**. A opção de commit específico desativa os deploys automáticos no painel.
7. Conferir se **Source** identifica o commit escolhido e testar o fluxo descrito na próxima seção.

O Render constrói a imagem pelo `Dockerfile`. O script de início executa as migrações quando configurado e inicia o servidor na porta fornecida pelo serviço. O PostgreSQL persiste no Neon entre substituições do container.

Para atualizações posteriores, usar um commit com verificações aprovadas. A opção **Deploy latest commit** publica o último commit da branch vinculada; **Restart service** reinicia a versão já publicada. As opções estão descritas na [documentação oficial do Render](https://render.com/docs/deploys).

## Banco, migrações e recuperação

As migrações são versionadas em `backend/migrations/`. Os comandos abaixo são executados dentro de `backend/`, com dependências instaladas e `DATABASE_URL` definida em ambiente privado.

Banco novo ou já versionado:

```bash
python -m alembic upgrade head
python -m alembic current
```

Na implantação de instância única, `RUN_MIGRATIONS=true` executa o primeiro comando antes do servidor. Para adotar banco legado da C2, realizar backup e conferir o procedimento em uma cópia isolada:

```bash
python -m app.adopt_baseline
python -m alembic upgrade head
```

A adoção compara o esquema legado antes de registrar a revisão inicial. O [README do backend](../backend/README.md#migrações-do-banco) descreve os critérios. Em recuperação, conferir a compatibilidade entre código e esquema; as migrações bloqueiam downgrade destrutivo. Restaurar backups em uma base isolada permite verificar os registros antes de usar a base recuperada.

A equipe preservou uma [captura do teste de restauração no Neon em 14/11/2026](evidencias/2026-11-14_desconfia_teste-restauracao-neon.png). Esse registro tem data e escopo próprios.

## Evidências da publicação

A equipe forneceu quatro capturas do teste da versão publicada: deploy no Render, resultado da análise, histórico e confirmação do feedback. O deploy identifica o commit `4b9d160`, e os logs exibem respostas HTTP 200 em `/health`. A mensagem fictícia recebeu risco alto, com pedido financeiro e isolamento como sinais.

As verificações executadas foram:

| Verificação | Resultado registrado |
|---|---|
| Publicação Docker no Render | Deploy concluído e serviço Live, commit `4b9d160` |
| Healthcheck | HTTP 200 |
| Mensagem sintética | Risco alto, sinais e recomendação preventiva apresentados |
| Histórico | Análise registrada e exibida na conta de teste |
| Feedback | Confirmação de registro apresentada |
| CI do commit publicado | Backend, frontend, PostgreSQL e imagem Docker aprovados |

A [execução do CI](https://github.com/yasmim-luizds/desconfia/actions/runs/46099940488), os [testes locais integrados](TESTES_C3.md) e a [avaliação da IA](AVALIACAO_FINAL_C3.md) têm escopos identificados. O teste funcional no site é separado da rodada de cinco mensagens da avaliação 2.2.2.

## Conferência do ambiente publicado

Abrir [`/health`](https://desconfia.onrender.com/health) e [`/config`](https://desconfia.onrender.com/config). O primeiro verifica a saúde do serviço; o segundo informa `ai_mode` e o limite de caracteres. Em produção, o modo esperado é `groq`.

Com conta e mensagem sintéticas, entrar, analisar, abrir o histórico e enviar feedback. Conferir o resultado antes de registrar uma nova evidência. O painel **Deploys** identifica a versão em uso e reúne os logs dessa publicação.

## Execução local com Docker Compose

Este procedimento executa a aplicação e um PostgreSQL 17 locais. A instalação manual descrita no [README principal](../README.md#executar-localmente) usa SQLite quando `DATABASE_URL` está ausente.

Na raiz do repositório, copiar `.env.example` para `.env` e preencher localmente:

```dotenv
POSTGRES_PASSWORD=<senha-aleatoria-local>
DESCONFIA_SECRET_KEY=<segredo-aleatorio-local>
AI_MODE=demo
GROQ_API_KEY=
GROQ_MODEL=openai/gpt-oss-20b
```

O Compose recebe `AI_MODE=demo` do arquivo e utiliza PostgreSQL. Para análise real, configurar `AI_MODE=groq` e uma chave Groq válida no arquivo privado.

```bash
docker compose config -q
docker compose up --build -d
docker compose ps
curl -fsS http://127.0.0.1:8000/health
docker compose exec database pg_isready -U desconfia -d desconfia
```

Abrir [http://127.0.0.1:8000](http://127.0.0.1:8000). O volume `postgres_data` armazena os registros do banco local. `docker compose restart web` reinicia a aplicação; `docker compose down` encerra os containers preservando esse volume.

## Referências

- [Arquitetura](ARQUITETURA.md)
- [IA responsável e privacidade](REQUISITOS.md#ia-responsável)
- [Validação da publicação e histórico C2](VALIDACAO_PUBLICACAO.md)
- [Render: publicação](https://render.com/docs/deploys) e [Docker](https://render.com/docs/docker)
