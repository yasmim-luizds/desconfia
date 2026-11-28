# Validação técnica da candidata 2.2.2

Validação local de uma cópia integrada do backend, interface e IA. O projeto acadêmico utiliza contas e mensagens sintéticas.

| Cenário | Verificação executada | Evidência |
|---|---|---|
| Backend integrado | 70 testes aprovados com SQLite e mocks | [Log](evidencias/c3/retomada-2.2.2/backend.log) |
| Banco novo e atualização legada | Um teste PostgreSQL 17.12 aprovado; usuários, análises, sinais e feedback preservados, upgrades repetidos, conferência Alembic, API e quota | [Log](evidencias/c3/retomada-2.2.2/postgres.log) |
| Cadastro/login e validações | `test_registration_login_and_password`, `test_invalid_registration`, `test_invalid_message` | Suíte backend aprovada |
| Token expirado/inativo e isolamento | `test_expired_and_inactive_user_tokens_are_denied`, `test_access_control_privacy_feedback_and_delete` | Suíte backend aprovada |
| Armazenamento opcional do original e paginação | `test_store_opt_in_and_pagination` | API com provedor mockado |
| Feedback e exclusão de análise | `test_access_control_privacy_feedback_and_delete`; testes da interface para conflito e cancelamento | Suítes aprovadas |
| Falhas e quota | Erros de provedor/banco, limites compartilhados e integridade dos registros quando o provedor falha | Suíte backend aprovada |
| Interface | 29 testes aprovados com mocks/jsdom, inclusive 401/409/429/503/504 | [Log](evidencias/c3/retomada-2.2.2/frontend.log) |
| Build frontend | Concluído com aliases temporários de dependências no ambiente local | [Log](evidencias/c3/retomada-2.2.2/build.log) |
| IA real | Cinco respostas válidas da 2.2.2; quatro riscos esperados e um caso ambíguo divergente | [Sete indicadores](AVALIACAO_FINAL_C3.md) |

As fontes e hashes estão no [registro técnico](evidencias/c3/retomada-2.2.2/validacao-tecnica.json). A branch isolada de IA passou em 53 testes; os 70 acima abrangem sua integração com o backend. Os dois totais representam escopos sobrepostos.

A interface foi executada na cópia 2.2.0, com o mesmo código de frontend `5e55282` usado na candidata 2.2.2. O build local reutilizou dependências por aliases temporários e gerou aviso de tamanho do bundle, preservado no log. A referência de código e a configuração do ambiente acompanham a evidência.

O teste PostgreSQL utilizou cluster local descartável e provedor mockado. As capturas históricas de computador, celular e navegação por teclado estão no PR #9 e em `docs/INTERFACE_C3.md` da branch `c3-interface`.
