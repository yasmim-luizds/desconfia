# Desconfia

Este é o projeto que eu e meu grupo estamos desenvolvendo para o Projeto Integrador IV. A ideia do Desconfia é ajudar a perceber sinais de risco em mensagens de texto. A pessoa envia uma mensagem e a aplicação mostra uma classificação, os sinais encontrados, uma explicação e uma sugestão do que fazer.

O resultado é apenas um apoio para a análise. A aplicação pode errar: risco baixo não significa que a mensagem seja segura. Quando houver dúvida, o certo é confirmar por um canal oficial conhecido.

> Para testes e apresentações, use só mensagens inventadas. Não cole conversas reais, senhas, códigos de autenticação, dados bancários, telefones ou outras informações pessoais.

## Branches do grupo

O trabalho ficou separado por frentes. A `main` ainda não recebeu a base C2; o PR #1, de `base-c2` para `main`, continua aberto.

- **Pessoa 1 — Yasmim (`base-c2`):** preparou a branch de integração da C2. Ela reúne a aplicação usada como base do grupo.
- **Pessoa 2 — Kaio (`melhoria-ia`):** melhorou a análise da IA, os testes e as métricas. O PR #2 foi integrado à `melhoria-interface`; depois, essa linha de trabalho chegou à `base-c2` pelo PR #3.
- **Pessoa 3 — Gustavo (`melhoria-interface` e `melhoria-interface-2`):** trabalhou no contraste, fontes, histórico, validação dos formulários, mensagens de erro e tela de resultado. Os PRs #3 e #4 foram integrados à `base-c2`.
- **Pessoa 4 — Hellen (`testes-c2`):** registrou testes funcionais, evidências e a revisão individual da IA. O PR #5 tem como destino `base-c2`; os arquivos dessa branch ainda não estão nesta cópia local de `base-c2`.
- **Pessoa 5 — José (`documentacao`):** esta branch, criada a partir de `base-c2`, reúne a documentação de publicação e o roteiro da demonstração.

## O que dá para fazer

- Criar uma conta, entrar e sair.
- Analisar uma mensagem de texto de até 2.000 caracteres.
- Ver o resultado como risco baixo, médio ou alto, junto com sinais, explicação e recomendação.
- Consultar o histórico da própria conta, enviar feedback e excluir uma análise.
- Usar o modo demonstração sem chave de IA ou configurar a análise real pela API Groq.

A ferramenta só analisa texto. Não lê imagens, áudios, QR Codes nem páginas da internet. A opção disponível para exclusão remove uma análise; a exclusão completa da conta ainda não está implementada como um fluxo documentado.

## O que instalar

Para executar a aplicação no computador, instale Python 3.12 ou superior, Node.js 22 e pnpm 11.25.0. Docker é necessário para testar PostgreSQL com Compose ou construir a imagem.

| Programa | Para que serve | Download oficial |
|---|---|---|
| Python 3.12+ | API e testes do back-end | [python.org/downloads](https://www.python.org/downloads/) |
| Node.js 22 | Ferramentas do front-end | [nodejs.org/download](https://nodejs.org/en/download) — escolha a linha 22 |
| pnpm 11.25.0 | Dependências e build do front-end | [Instalação do pnpm](https://pnpm.io/installation) |
| Git | Clonar e atualizar o projeto | [git-scm.com/downloads](https://git-scm.com/downloads) |
| Docker | PostgreSQL local e containers | [Docker Desktop](https://docs.docker.com/desktop/) |

Depois de instalar Node.js, instale a versão de pnpm usada pelo projeto:

```bash
npm install -g pnpm@11.25.0
```

Confira se os comandos estão disponíveis:

```bash
python --version
node --version
pnpm --version
```

## Como iniciar em modo demonstração

### Windows

Na pasta do projeto, abra `iniciar_demo.bat`. Na primeira execução, o script instala as dependências, compila o front-end e inicia o servidor. Quando aparecer a mensagem de que está pronto, abra `http://127.0.0.1:8000`. O modo demo usa regras locais, então não precisa de chave Groq. Deixe o terminal aberto enquanto estiver usando; `Ctrl+C` encerra a aplicação.

### macOS ou Linux

No terminal, dentro da pasta do projeto, rode:

```bash
chmod +x iniciar_local.sh
AI_MODE=demo ./iniciar_local.sh
```

Depois, acesse `http://127.0.0.1:8000`. O script prepara o ambiente Python, instala as dependências, compila a interface e inicia a API. Para sair, use `Ctrl+C`.

O modo demo serve para apresentar as telas e o fluxo. Ele não usa um modelo de IA.

### Instalação manual

Se preferir preparar tudo passo a passo, crie um ambiente virtual na pasta do projeto:

```bash
python -m venv .venv
```

Ative-o no PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Ou no macOS/Linux:

```bash
source .venv/bin/activate
```

Instale as dependências e gere o front-end:

```bash
python -m pip install -r backend/requirements.txt
pnpm --dir frontend install --frozen-lockfile
pnpm --dir frontend build
```

Para iniciar a API manualmente, execute:

```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

A documentação interativa da API fica em `http://127.0.0.1:8000/docs`.

## Como ativar a análise com IA

O modo real envia a mensagem ao serviço da Groq pelo back-end. Para usá-lo, é preciso ter uma chave, acesso à internet e quota disponível. Crie a chave no Groq Console e siga estes passos:

1. Copie `backend/.env.example` para `backend/.env`.
2. Preencha `GROQ_API_KEY` e mantenha `AI_MODE=groq`.
3. Gere um segredo local para `DESCONFIA_SECRET_KEY`:

   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(48))"
   ```

4. Inicie com `iniciar_local.bat` no Windows ou `./iniciar_local.sh` no macOS/Linux.

O modelo configurado como padrão é `openai/gpt-oss-20b`. Antes de trocar o modelo ou executar uma avaliação real, confira a documentação da Groq, os limites da conta e o número de chamadas previsto.

A chave deve ficar somente no back-end. Não a coloque em variável `VITE_`, código enviado ao navegador, captura de tela ou commit. Não envie o arquivo `.env` ao GitHub.

## Como testar PostgreSQL com Docker

Sem `DATABASE_URL`, o modo local usa SQLite no arquivo `backend/desconfia_local.db`. Para testar o PostgreSQL previsto para a publicação:

1. Instale e abra Docker Desktop ou Docker Engine.
2. Copie `.env.example` para `.env` na raiz do projeto.
3. Preencha `POSTGRES_PASSWORD` e `DESCONFIA_SECRET_KEY` com valores fortes, só para esse ambiente. Se não tiver uma chave Groq, altere `AI_MODE` para `demo`.
4. Inicie os serviços:

   ```bash
   docker compose up --build
   ```

5. Abra `http://127.0.0.1:8000`. Para encerrar sem apagar o banco, use `docker compose down`.

O Compose define PostgreSQL 17, uma verificação de disponibilidade do banco e o volume `postgres_data`. Não use `docker compose down -v` se quiser guardar os dados: essa opção remove o volume. O arquivo `.env` não deve ser compartilhado nem enviado ao GitHub.

## Como o sistema funciona

A interface foi feita com React e Vite. Ela envia as solicitações ao back-end em FastAPI. O back-end cuida do cadastro, da autenticação, das análises e do banco de dados, usando SQLAlchemy. Quando a IA real está ativada, o servidor conversa com a Groq; a chave não vai para o navegador. No modo demo, regras locais substituem essa chamada.

| Pasta ou arquivo | O que contém |
|---|---|
| `frontend/` | Interface, estilos e testes Vitest |
| `backend/app/` | API, autenticação, integração com IA e acesso ao banco |
| `backend/tests/` | Testes Pytest do back-end |
| `eval/` | Mensagens sintéticas, script de avaliação e resultados registrados |
| `docs/` | Requisitos, arquitetura, testes, publicação e roteiro da apresentação |
| `compose.yaml` | Configuração local da aplicação e do PostgreSQL |
| `Dockerfile` | Instruções para construir a imagem da aplicação |
| `.github/workflows/tests.yml` | Testes automatizados executados pelo GitHub Actions |

## Testes e avaliação

Para rodar os testes automatizados, com Python, Node.js e pnpm instalados:

```bash
cd backend
python -m pytest -q
cd ../frontend
pnpm test
pnpm build
cd ..
python eval/run_eval.py --validate-only
```

O comando `--validate-only` confere os 15 casos sintéticos, mas não chama a IA e não calcula métricas. O workflow do GitHub executa Pytest, essa validação e os testes e build do front-end.

A rodada real V2 foi feita em 24/10/2026 com 15 mensagens sintéticas e uma repetição por caso. Houve 14 respostas válidas de 15 tentativas; 12 das 14 respostas válidas tiveram a classificação esperada pelo conjunto de teste. Uma resposta foi rejeitada por falha na validação das evidências. Esses números descrevem só essa amostra.

A revisão qualitativa individual e os testes funcionais estão registrados na branch `testes-c2` e no PR #5. A segunda revisão independente e o consenso com a Pessoa 2 ainda precisam ser confirmados. Antes de iniciar outra rodada real, leia `eval/README.md`, pois as chamadas podem consumir quota ou gerar custos. Salve resultados novos em outro arquivo; não sobrescreva os anteriores.

## Privacidade e cuidados

Por padrão, a mensagem original não é guardada. A pessoa pode optar por salvá-la no histórico. Mesmo quando o texto original não é salvo, explicações, resultados ou comentários podem acabar contendo dados pessoais. Por isso, nas demonstrações e testes, use mensagens inventadas.

No modo real, o texto é enviado à Groq para análise. O grupo ainda precisa definir o prazo de retenção, o contato para questões de privacidade e o procedimento para exclusão completa de conta. A exclusão de uma análise não significa que uma conta inteira foi apagada.

## Publicação

O grupo escolheu executar a aplicação localmente. A demonstração fica em `http://127.0.0.1:8000`, acessível somente no computador que estiver rodando o Docker Compose; não há URL pública neste plano. As instruções estão em `docs/PUBLICACAO.md`.

Na validação local de 27/10/2026, a imagem Docker foi construída e os fluxos foram verificados com dados sintéticos: cadastro, login, análise, histórico, feedback, isolamento entre contas e exclusão. O PostgreSQL ficou saudável. Depois de reiniciar o serviço web, a análise e o feedback continuaram no histórico. Também foram reiniciados o container PostgreSQL e o serviço web; a conta e a análise continuaram no volume. Ao todo, passaram 12 verificações de API. Os detalhes estão em `docs/VALIDACAO_PUBLICACAO.md`.

O sandbox bloqueou a rede bridge padrão do Docker. Para executar os testes funcionais, foi usado um ajuste temporário de rede, sem alterar `compose.yaml`. Antes da apresentação, falta repetir `docker compose up --build -d` no computador do grupo usando a rede padrão.
