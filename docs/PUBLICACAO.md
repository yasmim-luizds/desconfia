# Publicação e execução local do Desconfia

A hospedagem escolhida pelo grupo para a demonstração é local. A aplicação fica acessível somente no computador em que estiver rodando, em `http://127.0.0.1:8000`; isso não cria uma URL pública nem um serviço de nuvem. Este guia segue essa decisão. Render não está selecionado.

## 1. Preparar o repositório

Execute os comandos a partir da raiz do repositório, onde ficam `Dockerfile`, `compose.yaml`, `frontend/`, `backend/`, `eval/` e `docs/`. Não configure `desconfia_pronto` como pasta raiz; ela não existe nesta cópia. Não envie `.env`, `.venv`, `node_modules`, arquivos `.db` ou credenciais.

## 2. Configurar variáveis locais

Copie `.env.example` para `.env` na raiz do projeto. Gere valores fortes e diferentes para a senha do PostgreSQL e para a chave da aplicação, por exemplo:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Preencha o arquivo `.env` localmente:

```dotenv
POSTGRES_PASSWORD=<senha-aleatoria-do-banco>
DESCONFIA_SECRET_KEY=<chave-aleatoria-da-aplicacao>
AI_MODE=demo
GROQ_API_KEY=
GROQ_MODEL=openai/gpt-oss-20b
```

`AI_MODE=demo` permite demonstrar a interface sem uma chave externa; não representa uma análise real por IA. Se o grupo decidir testar a integração real, configure `AI_MODE=groq` e `GROQ_API_KEY` somente no ambiente local protegido, confira quota e custos, e não copie a chave para o front-end ou para o GitHub.

## 3. Iniciar aplicação e PostgreSQL

Valide a configuração e inicie os containers:

```bash
docker compose config -q
docker compose up --build -d
docker compose ps
```

O Compose usa PostgreSQL 17, aguarda o healthcheck do banco antes de iniciar a aplicação e grava os dados no volume nomeado `postgres_data`. Confira a API e o banco:

```bash
curl -fsS http://127.0.0.1:8000/health
docker compose exec database pg_isready -U desconfia -d desconfia
```

Na interface, use apenas contas de teste e mensagens inventadas. A URL `127.0.0.1` só funciona no computador local; outro dispositivo não consegue acessá-la como uma URL pública.

## 4. Testar os fluxos locais

1. Cadastre uma conta fictícia, entre e saia.
2. Analise uma mensagem sintética e confira classificação, sinais, explicação e recomendação.
3. Opte por guardar a mensagem e confirme que ela aparece no histórico dessa conta.
4. Envie feedback, recarregue a página e confira o registro.
5. Crie uma segunda conta e confirme que ela não vê o histórico da primeira.
6. Exclua a análise de teste e confirme que ela desapareceu do histórico.

O sistema oferece exclusão de análise. O procedimento para excluir uma conta completa ainda está em avaliação pelo grupo; não prometa esse fluxo na apresentação.

## 5. Testar persistência

Com uma análise sintética e feedback salvos, reinicie o serviço web e volte a consultar o histórico:

```bash
docker compose restart web
```

Confira também a persistência após reiniciar o PostgreSQL e depois a aplicação:

```bash
docker compose restart database
docker compose restart web
```

Entre novamente e confirme que a conta e os registros de teste continuam no histórico. Para parar os containers preservando os dados, use `docker compose down`. **Não use `docker compose down -v`** quando quiser manter o banco: a opção `-v` remove `postgres_data`.

## 6. Resultado e ambiente desta validação

Em 27/10/2026, a imagem da aplicação foi construída, PostgreSQL 17.11 ficou saudável e 12 verificações da API passaram com dados sintéticos. A persistência foi confirmada após reiniciar o serviço web e, separadamente, o container PostgreSQL e o serviço web.

Os testes de Docker, PostgreSQL, fluxos da aplicação e persistência foram feitos no computador local do responsável, com dados sintéticos. Não há necessidade de repeti-los no computador do grupo. O relatório está em `docs/VALIDACAO_PUBLICACAO.md`.

## 7. Privacidade e decisões do grupo

O grupo informou que retenção de dados, contato para questões de privacidade, exclusão completa de conta e tratamento de backups/logs continuam em avaliação. Esses pontos ficam em aberto até uma decisão do grupo. Use somente contas e mensagens sintéticas durante testes e apresentações.
