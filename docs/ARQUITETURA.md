# Como o front-end e o back-end trabalham juntos

## Front-end

`frontend/src/App.jsx` contém as telas e o estado da sessão. A página inicial leva
ao cadastro ou login; após autenticação aparecem análise, histórico e resultado.
O estilo responsivo está em `styles.css`. Componentes usam React e ícones Lucide.
Os textos devolvidos pelo servidor são renderizados como texto, nunca como HTML.

`api.js` centraliza as requisições, envia o token no cabeçalho Authorization e
transforma falhas de conexão/validação em mensagens legíveis. Não há chave da Groq
ou conexão direta com o banco no front-end.

## Back-end

- `main.py`: endpoints, autorização e persistência do fluxo.
- `schemas.py`: formatos e limites das entradas e respostas da API.
- `security.py`: hash de senha, criação e verificação de tokens.
- `ai.py`: fronteira com a Groq, prompt, esquema estruturado e checagem de evidências.
- `database.py`: conexão SQLAlchemy e sessão por requisição.
- `models.py`: usuários, análises, sinais e feedbacks.
- `config.py`: variáveis de ambiente e bloqueios de configuração de produção.
- `limits.py`: controle básico de frequência para o MVP com um worker.

## Exemplo de fluxo

1. `POST /auth/login`: verifica a senha e devolve token e dados públicos do usuário.
2. `POST /analyses`: recebe mensagem e escolha de armazenamento, confere token,
   valida tamanho e limite por minuto, solicita análise à Groq.
3. A Groq devolve JSON. O back-end valida o formato, risco e evidências.
4. Resultado e sinais são gravados em uma transação. Texto/evidências só ficam se
   `store_message=true`. Não há salvamento de resultado em caso de falha da IA.
5. O front-end apresenta risco, explicação, sinais e recomendação.
6. `GET /analyses` recupera somente dados do usuário autenticado, com paginação.
7. `POST /analyses/{id}/feedback` registra uma avaliação. `DELETE /analyses/{id}`
   remove a análise, sinais e feedbacks relacionados.

## Banco

Usuário 1:N Análise; Análise 1:N Sinal; Análise 1:N Feedback na estrutura,
com unicidade de análise + usuário. O controle de acesso permite somente ao dono
avaliar sua análise, resultando em um feedback por análise no fluxo atual.

SQLAlchemy usa os mesmos modelos para SQLite e PostgreSQL. Na execução manual local, sem `DATABASE_URL`, o padrão é SQLite; o Compose define PostgreSQL para a validação desse banco. A demonstração local é o escopo da C2. A hospedagem planejada para a C3 ainda não foi configurada, e nenhum banco local é migrado para a nuvem automaticamente.

## Testes versus avaliação

Pytest verifica contratos e falhas com serviço externo simulado. Vitest verifica
interações das telas. A avaliação em `eval/` chama a Groq real e mede classificações;
revisão humana complementa a análise de explicações, recomendações e alucinações.
Uma suíte de testes passando não comprova qualidade do modelo de IA.

A rodada V2 de 24/10/2026 está registrada em `eval/results-v2.json` para 15 casos
sintéticos. A revisão individual está em `docs/REVISAO_QUALITATIVA_27.10.2026.md`
na branch `testes-c2`; o PR #5 foi integrado à `base-c2` no commit `1702dc6`.
A segunda revisão independente e o consenso ainda estão pendentes. Esses resultados
são exploratórios e não comprovam precisão geral, segurança ou resistência ampla a
ataques.
