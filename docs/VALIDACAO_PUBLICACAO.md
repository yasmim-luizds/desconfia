# Validação de publicação — Desconfia

**Data:** 27/10/2026
**Branch de trabalho:** `publicacao-documentacao`, baseada na `base-c2` (`3e1c276`)
**Hospedagem escolhida pelo grupo:** local, informada por José em 27/10/2026
**Endereço local:** `http://127.0.0.1:8000` (acessível apenas no computador que executa a aplicação)
**URL pública:** não se aplica à decisão atual de hospedagem local

## Testes automatizados

As dependências foram instaladas em `.venv` (Python 3.12.3) e com o lockfile do front-end (Node 22.23.4, pnpm 11.25.0):

- Pytest: **33 aprovados**, com 34 avisos de depreciação.
- Vitest: **17 aprovados**.
- Build Vite: **aprovado**.
- Validação do conjunto sintético: **15 casos válidos**, sem chamadas à IA e sem cálculo de métricas.

O workflow `tests.yml` executa Pytest, validação do dataset e testes/build do front-end. As execuções públicas observadas na branch `testes-c2`, no commit `c7ae4d6`, terminaram com sucesso: [execução 40559750063](https://github.com/yasmim-luizds/desconfia/actions/runs/40559750063) e [execução 40559106002](https://github.com/yasmim-luizds/desconfia/actions/runs/40559106002). Esses checks não testam publicação nem execução do serviço com PostgreSQL.

## Docker, PostgreSQL e persistência

A validação foi realizada no computador local do responsável em 27/10/2026. `docker compose config -q` passou e a imagem da aplicação foi construída com sucesso. A versão registrada da imagem PostgreSQL foi **17.11**.

Os testes de Docker, PostgreSQL, fluxos da aplicação e persistência foram executados no computador local do responsável, com dados sintéticos. Não é necessário repetir esses testes no computador do grupo. Nenhum override foi incluído no repositório.

Com `AI_MODE=demo` e somente dados inventados, a verificação `/health` confirmou conexão com PostgreSQL. **12 verificações da API passaram:** cadastro, login, sessão, análise, histórico, criação e leitura de feedback, isolamento entre duas contas e exclusão. Após reiniciar o serviço web, a análise, a mensagem sintética e o feedback permaneceram no histórico.

Também criei uma conta e uma análise sintéticas, reiniciei o container PostgreSQL e depois o serviço web. O banco voltou a ficar saudável, a API reconectou, e o login e a análise continuaram disponíveis no volume nomeado `postgres_data`. Os registros de teste foram removidos ao final da validação.

O grupo pode usar este registro como evidência da validação local. Nenhuma credencial real foi usada ou adicionada ao repositório.

## Testes funcionais entregues pela Pessoa 4

O relatório funcional na branch `testes-c2`, em `docs/TESTES_FUNCIONAIS.md`, registra execução local em modo demonstração, em 27/10/2026, com cadastro, login/logout, análise sintética, histórico, feedback, exclusão e isolamento entre contas. O PR #5 para `base-c2` não está integrado nesta cópia; os resultados são da integrante responsável e não correspondem aos testes executados nesta sessão.

A rodada real V2 está em `eval/results-v2.json`, já presente na `base-c2`. A revisão individual está em `docs/REVISAO_QUALITATIVA_27.10.2026.md` na branch `testes-c2`. A segunda revisão e o consenso com a Pessoa 2 continuam pendentes. A amostra tem 15 casos sintéticos e não demonstra desempenho geral do modelo.

## Hospedagem local e decisões em aberto

A hospedagem local foi escolhida pelo grupo; por isso, não foi criada conta em nuvem nem URL pública. O endereço da demonstração é `http://127.0.0.1:8000` no computador que executa o Compose. A configuração local e os passos para repetir os testes sem o override estão em `docs/PUBLICACAO.md`.

Não há pendência de repetição dos testes no computador do grupo. Retenção de dados, contato de privacidade, exclusão completa de conta e tratamento de backups/logs continuam em avaliação pelo grupo; nenhuma decisão foi presumida neste relatório. A equipe também deve concluir a segunda revisão qualitativa, registrar divergências e consenso e decidir se haverá nova avaliação.

**Conclusão:** o build Docker, a conexão com PostgreSQL, os fluxos locais e a persistência após reinícios foram verificados com dados sintéticos no computador local do responsável. Não é necessário repetir os testes no computador do grupo. A demonstração é local e não possui URL pública.

## Evolução das branches

| Frente | Branch/ref observado | Situação em 27/10/2026 |
|---|---|---|
| Integração da C2 | `base-c2` (`3e1c276`) | Base com app, melhorias de IA/interface, Docker/Compose e workflow. |
| Pessoa 1 — Yasmim | PR #1, `base-c2` para `main` | PR aberto; `main` ainda não contém a base C2. |
| Pessoa 2 — Kaio | `melhoria-ia` (`8f5213b`), PR #2 | Integrado à linha de interface e depois à `base-c2`. |
| Pessoa 3 — Gustavo | `melhoria-interface`, `melhoria-interface-2`; PRs #3 e #4 | Integrados à `base-c2`. |
| Pessoa 4 — Hellen | `testes-c2` (`c7ae4d6`), PR #5 | Quatro commits à frente de `base-c2`; os relatórios não estão nesta base local. GitHub ainda mostrava o PR aberto na última conferência. |
| Pessoa 5 — José | `documentacao` | Branch baseada em `3e1c276`, com esta frente de documentação proposta para revisão contra `base-c2`. |

A `main` permanece separada da C2 até a integração do PR #1. Antes de abrir outro PR, atualize a branch de trabalho com a base acordada e confira o diff para não duplicar alterações.
