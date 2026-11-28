# Arquitetura do Desconfia

## Frontend e backend

A interface em React/Vite e a API em FastAPI são servidas no mesmo endereço HTTPS: [Desconfia](https://desconfia.onrender.com/). O Render executa a imagem construída pelo `Dockerfile` da raiz do repositório; o PostgreSQL persistente fica no Neon.

`frontend/src/App.jsx` contém as telas e o estado da sessão. `api.js` envia o token no cabeçalho Authorization e transforma falhas em mensagens legíveis. Os textos retornados pelo servidor são renderizados como texto, nunca como HTML. A chave da Groq e a conexão com o banco ficam no backend.

| Arquivo | Responsabilidade |
|---|---|
| `main.py` | Endpoints, autorização e persistência do fluxo |
| `schemas.py` | Formatos e limites das entradas e respostas |
| `security.py` | Hash de senha, criação e verificação de tokens |
| `ai.py` | Integração com a Groq, prompt, esquema, evidências literais e recomendação preventiva controlada |
| `database.py` e `models.py` | Conexão SQLAlchemy e modelos de usuários, análises, sinais, feedbacks e quota |
| `config.py` | Variáveis de ambiente e validação de produção |
| `limits.py` | Limites por endereço/usuário em memória, em um worker |
| `quota.py` | Reserva atômica de tentativas da IA, persistida no banco |

## Fluxo de uma análise

1. `POST /auth/login` verifica a senha e devolve o token e os dados públicos do usuário.
2. `POST /analyses` confere autenticação, tamanho da mensagem, limites locais e quota global.
3. A Groq gera risco, explicação e indicadores. O conteúdo enviado é tratado como dado não confiável, separado das instruções do analisador.
4. O backend valida formato e citações literais e acrescenta a recomendação preventiva definida pela aplicação conforme o risco.
5. Resultado e sinais são gravados em uma transação. Texto original e evidências são persistidos quando `store_message=true`; explicações e comentários também podem conter informações do texto recebido.
6. O frontend apresenta risco, explicação, sinais e recomendação.
7. `GET /analyses` recupera somente os registros do usuário autenticado, com paginação. `POST /analyses/{id}/feedback` registra feedback; `DELETE /analyses/{id}` exclui a análise, os sinais e os feedbacks relacionados.

Uma falha da IA retorna erro tratado e preserva a integridade dos registros, conforme os [testes da C3](TESTES_C3.md).

## Banco e publicação

Usuário 1:N Análise; Análise 1:N Sinal e Análise 1:N Feedback, com unicidade de análise e usuário. O controle de acesso permite ao dono avaliar sua análise uma vez.

| Ambiente | Aplicação e banco |
|---|---|
| Publicação C3 | Render com Docker e PostgreSQL no Neon |
| Docker Compose local | Aplicação e PostgreSQL 17 em containers, com volume nomeado |
| Execução manual local | SQLite quando `DATABASE_URL` está ausente; PostgreSQL quando configurado |

O Alembic versiona o esquema. `backend/start.sh` pode executar as migrações com `RUN_MIGRATIONS=true` antes de iniciar o Uvicorn em um worker, usando a porta `PORT` do Render. O procedimento está no [guia de publicação](PUBLICACAO.md) e no [README do backend](../backend/README.md).

A versão publicada pela equipe corresponde ao commit `4b9d1603d5dcdb884e25d659fd15de5e97182fff`, após os PRs #8, #9, #10 e #11.

## Testes e avaliação da IA

Pytest verifica contratos e falhas da API; Vitest verifica a interface. Os testes com mocks avaliam o comportamento da aplicação. A avaliação em `eval/` chama a Groq com mensagens sintéticas.

A [avaliação da versão 2.2.2](AVALIACAO_FINAL_C3.md) registrou cinco respostas válidas e quatro classificações esperadas. A revisão qualitativa foi assistida por Codex, com autoria e notas em `eval/revisao-final-222-assistida.json`. A recomendação avaliada é o texto controlado pela aplicação; risco, explicação e sinais são gerados pelo modelo.

A V2 histórica permanece em `eval/results-v2.json` e em `docs/REVISAO_QUALITATIVA_27.10.2026.md`. Cada rodada conserva seu conjunto, versão e denominadores.

Os cuidados de privacidade, vieses e uso de recursos estão consolidados em [IA responsável](REQUISITOS.md#ia-responsável).
