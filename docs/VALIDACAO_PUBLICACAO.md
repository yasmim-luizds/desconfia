# Validação da demonstração e do PostgreSQL — Desconfia

**Testes de Docker/PostgreSQL:** 27/10/2026, no computador local do responsável pela validação, conforme informado ao grupo.
**Atualização deste registro:** 29/10/2026.
**Branch de trabalho:** `publicacao-documentacao`, proposta no [PR #6](https://github.com/yasmim-luizds/desconfia/pull/6).
**Base atualizada:** `base-c2`, commit `1702dc6`, que inclui o merge do PR #5.

## Escopo da execução local e da hospedagem

A demonstração local escolhida para a C2 não é uma publicação na nuvem. Na instalação manual, quando `DATABASE_URL` não está definida, o back-end usa SQLite em `backend/desconfia_local.db`. Essa é a configuração informada para a aplicação no computador da Yasmin.

A validação de PostgreSQL descrita abaixo é uma execução separada com Docker Compose no computador local do responsável. O Compose configura PostgreSQL e passa `DATABASE_URL` ao serviço web. Portanto, o resultado dessa validação não significa que a instalação manual no computador da Yasmin esteja usando PostgreSQL.

A hospedagem local está definida para a demonstração da C2. O planejamento da C3 ainda prevê configurar hospedagem, testar o fluxo publicado e registrar a URL e as condições do provedor. Provedor e URL pública da C3 ainda não estão definidos neste registro.

## Testes automatizados

Na execução registrada nesta branch, os resultados foram:

- Pytest: **33 aprovados**, com 34 avisos de depreciação.
- Vitest: **17 aprovados**.
- Build do Vite: **aprovado**.
- Validação do conjunto sintético: **15 casos válidos**, sem chamadas à IA nem cálculo de métricas.

O workflow `tests.yml` executa Pytest, validação do conjunto e testes e build do front-end. As verificações automatizadas não comprovam a execução do PostgreSQL nem uma publicação na nuvem.

## Resultado informado para Docker, PostgreSQL e persistência

O registro recebido informa que, em 27/10/2026, a imagem Docker foi construída, o PostgreSQL 17.11 ficou saudável e 12 verificações da API passaram com dados sintéticos. O resumo relata cadastro, login, sessão, análise, histórico, feedback, isolamento entre contas e exclusão. Também registra que os dados continuaram disponíveis após reiniciar o serviço web e após reiniciar o container PostgreSQL e depois o serviço web.

O ZIP e os arquivos recebidos não continham a saída bruta do terminal nem capturas da execução do Docker/PostgreSQL. Por isso, este documento registra os resultados informados, mas não apresenta uma transcrição literal como se tivesse sido preservada. As capturas já existentes em `docs/evidencias/` são dos testes funcionais de interface da Pessoa 4; elas não demonstram por si só a conexão ou a persistência em PostgreSQL.

Para conferir e registrar a evidência do PostgreSQL no computador em que o Compose foi executado, os comandos abaixo não exibem senha nem URL de conexão:

```bash
docker compose config -q
docker compose up --build -d
docker compose ps
curl -fsS http://127.0.0.1:8000/health
docker compose exec database pg_isready -U desconfia -d desconfia
docker compose exec web python -c "from app.database import engine; print(engine.dialect.name)"
```

Com uma conta e registros sintéticos criados, conferir o histórico pela aplicação depois de cada reinício:

```bash
docker compose restart web
curl -fsS http://127.0.0.1:8000/health
# Conferir na interface se a análise e o feedback continuam no histórico.

docker compose restart database
# Aguardar o banco ficar saudável e verificar:
docker compose exec database pg_isready -U desconfia -d desconfia
docker compose restart web
curl -fsS http://127.0.0.1:8000/health
# Entrar de novo e conferir se a conta e os registros sintéticos continuam no histórico.
```

Para identificar o banco usado pela instalação manual no computador da gravação, execute dentro de `backend/`:

```bash
python -c "from app.database import engine; print(engine.dialect.name)"
```

O comando imprime apenas o tipo do banco, por exemplo `sqlite` ou `postgresql`, sem revelar credenciais. Para completar a evidência pedida pela professora, anexar as saídas ou capturas reais desses comandos no ambiente em que os testes foram executados, removendo qualquer dado pessoal e segredo. Não inventar nem substituir essa evidência por saídas esperadas.

## Conferência antes da gravação

Não é necessário repetir toda a bateria de testes. No computador usado para a gravação, iniciar a configuração que será apresentada e fazer uma verificação curta: confirmar `/health`, confirmar o modo em `/config`, entrar com uma conta sintética, fazer uma análise demo, conferir histórico e feedback e excluir o registro de teste. Se a demonstração usar a instalação manual, confirmar também o banco ativo com o comando acima. Se usar Docker Compose, confirmar `pg_isready` e que o banco ativo é `postgresql`.

## Evidências funcionais já integradas

O PR #5 da Hellen foi integrado à `base-c2` pelo merge commit `1702dc6`. O relatório [`docs/TESTES_FUNCIONAIS.md`](TESTES_FUNCIONAIS.md) descreve os testes locais em modo demonstração e aponta capturas de cadastro, login, análise, histórico, feedback, exclusão, isolamento de contas e interface móvel em [`docs/evidencias/`](evidencias/). Essas capturas comprovam os fluxos visuais indicados no relatório, mas não comprovam a infraestrutura PostgreSQL.

## Estado das branches e PRs em 29/10/2026

- PR #1, `base-c2` para `main`: aberto na consulta registrada; `main` ainda está separada da integração C2.
- PR #2: integrado à linha de interface.
- PRs #3 e #4: integrados à `base-c2`.
- PR #5, `testes-c2` para `base-c2`: integrado no commit `1702dc6`; os relatórios e capturas da Pessoa 4 estão presentes na base.
- PR #6, documentação: aberto para revisão; a branch de origem é `publicacao-documentacao`.

## Pendências

Ainda dependem de decisão do grupo o prazo de retenção, o contato de privacidade, o procedimento de exclusão completa de conta e o tratamento de backups/logs. Para a C3, ainda será necessário escolher e configurar a hospedagem, testar o fluxo publicado e atualizar a documentação com a URL real. A segunda revisão qualitativa e o consenso também permanecem pendentes.
