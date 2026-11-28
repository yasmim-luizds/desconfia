# Matriz de rastreabilidade e evidências — Desconfia C3

**Data de elaboração:** 28/11/2026
**Frente responsável:** Frente 5 — Documentação técnica, rastreabilidade, impacto e apresentação
**Branch:** `c3-documentacao-impacto`

## 1. Objetivo

Relacionar os requisitos do Desconfia às funcionalidades implementadas, às verificações realizadas e às evidências disponíveis, preservando a diferença entre os testes locais, a avaliação da IA e as verificações informadas sobre o ambiente publicado.

## 2. Matriz de rastreabilidade

| ID | Requisito | Verificação | Evidência |
|---|---|---|---|
| R01 | Cadastro e login | Testes automatizados de autenticação e validação; testes funcionais da C2 | [Testes C3](TESTES_C3.md), [Testes funcionais](TESTES_FUNCIONAIS.md) |
| R02 | Logout | Testes da interface e verificação funcional da C2 | [Testes funcionais](TESTES_FUNCIONAIS.md) |
| R03 | Envio e validação de mensagens | Testes de entradas inválidas e limite de 2.000 caracteres | [Testes C3](TESTES_C3.md), [Testes funcionais](TESTES_FUNCIONAIS.md) |
| R04 | Integração com a Groq | Testes simulados de falhas e rodada real da IA 2.2.2 | [Testes C3](TESTES_C3.md), [Avaliação final C3](AVALIACAO_FINAL_C3.md) |
| R05 | Classificação de risco | Verificação do resultado da IA em cinco mensagens sintéticas | [Avaliação final C3](AVALIACAO_FINAL_C3.md) |
| R06 | Sinais e explicação | Validação técnica de formato e citações; revisão qualitativa assistida | [Avaliação final C3](AVALIACAO_FINAL_C3.md) |
| R07 | Recomendações preventivas | Testes da interface e revisão qualitativa assistida | [Avaliação final C3](AVALIACAO_FINAL_C3.md), [Testes C3](TESTES_C3.md) |
| R08 | Histórico individual | Testes de paginação, isolamento e acesso autorizado | [Testes C3](TESTES_C3.md), [Testes funcionais](TESTES_FUNCIONAIS.md) |
| R09 | Feedback | Testes de envio, conflito e associação à análise | [Testes C3](TESTES_C3.md) |
| R10 | Minimização e exclusão | Testes de armazenamento opcional, controle de acesso e exclusão | [Testes C3](TESTES_C3.md), [Testes funcionais](TESTES_FUNCIONAIS.md) |
| R11 | PostgreSQL | Validação local com PostgreSQL 17.12; implantação Neon informada pela equipe | [Testes C3](TESTES_C3.md), [Validação da publicação](VALIDACAO_PUBLICACAO.md) |
| R12 | Testes automatizados | 70 testes de backend, 29 de frontend e um teste PostgreSQL aprovados na candidata 2.2.2 | [Testes C3](TESTES_C3.md) |
| R13 | Avaliação da IA | Cinco respostas válidas, quatro classificações esperadas e revisão assistida | [Avaliação final C3](AVALIACAO_FINAL_C3.md) |
| R14 | Publicação | Render, PostgreSQL no Neon e verificações comunicadas da versão publicada | [Validação da publicação](VALIDACAO_PUBLICACAO.md), [Guia de publicação](PUBLICACAO.md) |

## 3. Evidências técnicas da C3

O documento `docs/TESTES_C3.md` registra a validação local da candidata 2.2.2:

- Backend: 70 testes aprovados com SQLite e mocks.
- Frontend: 29 testes aprovados com mocks/jsdom.
- PostgreSQL: um teste aprovado com cluster local descartável e provedor simulado.
- Build frontend: concluído, com ressalvas preservadas no relatório.
- IA real: cinco respostas válidas e quatro classificações correspondentes aos riscos esperados.

Os registros técnicos estão referenciados em `docs/TESTES_C3.md`, incluindo logs e identificação da versão do código. Os totais de 53 testes da branch de IA e 70 testes do backend integrado representam escopos sobrepostos e não devem ser somados.

## 4. Avaliação da IA

A versão 2.2.2 foi avaliada com cinco mensagens sintéticas. O resultado registrado foi de 5/5 respostas válidas e 4/5 classificações esperadas (80%).

O caso `ambiguous-4` apresentou divergência entre o risco esperado (médio) e o recebido (baixo). A revisão qualitativa foi assistida por Codex, com 16 critérios adequados, quatro parciais e nenhum inadequado.

A amostra é pequena e não demonstra eficácia geral em mensagens reais. Esses resultados não devem ser confundidos com os testes funcionais realizados no site publicado.

## 5. Publicação da aplicação

Conforme o comunicado da equipe, a aplicação está publicada em:

https://desconfia.onrender.com/

A infraestrutura informada utiliza Render e PostgreSQL no Neon. A versão publicada foi identificada pelo commit `4b9d160`, após a integração dos PRs #8, #9, #10 e #11.

O comunicado registra healthcheck HTTP 200, análise de mensagem sintética, histórico e feedback, além de aprovação das verificações de backend, frontend, PostgreSQL e build Docker no GitHub Actions.

Esses resultados foram comunicados pela equipe. Não representam testes independentes executados nesta revisão documental.

## 6. Limitações e pendências

- A avaliação da IA considera somente cinco mensagens sintéticas e uma execução por mensagem.
- A revisão qualitativa registrada foi assistida por Codex, que também apoiou o desenvolvimento.
- O teste PostgreSQL documentado em `TESTES_C3.md` utilizou ambiente local descartável e não comprova, isoladamente, o banco Neon de produção.
- Os registros históricos da C2 foram preservados e não devem ser confundidos com as verificações da C3.
- As evidências de publicação e de GitHub Actions precisam permanecer associadas aos respectivos registros.
- As decisões institucionais sobre retenção de dados, contato de privacidade, exclusão completa da conta e tratamento de backups/logs devem ser confirmadas pelo grupo antes de afirmar que estão concluídas.

## 7. Referências

- `docs/REQUISITOS.md`
- `docs/TESTES_C3.md`
- `docs/TESTES_FUNCIONAIS.md`
- `docs/AVALIACAO_FINAL_C3.md`
- `docs/PUBLICACAO.md`
- `docs/VALIDACAO_PUBLICACAO.md`
- `eval/results-c3-final-222.json`

Esta matriz consolida evidências documentadas e registros informados pela equipe. Não substitui a análise dos logs, as verificações da implantação ou a avaliação independente da qualidade da IA.