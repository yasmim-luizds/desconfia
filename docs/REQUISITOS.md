# Escopo e rastreabilidade

O produto é web,
somente texto, com avaliação técnica controlada. Pesquisa com usuários é opcional.
Não há alegação de melhoria comprovada de comportamento da comunidade.

| Requisito | Implementação | Verificação |
|---|---|---|
| Cadastro e login | formulários React, `/auth/register`, `/auth/login` | Pytest + Vitest |
| Logout | limpeza de sessão em memória | Vitest |
| Envio textual | validação de 1–2000 caracteres e consentimento na interface | Pytest + Vitest |
| Groq | `backend/app/ai.py`, tratamento de erros, timeout e validação de respostas | C2: testes simulados e rodada V2 em `eval/results-v2.json`; C3: avaliação real da versão 2.2.2 registrada em `docs/AVALIACAO_FINAL_C3.md`, com 5/5 respostas válidas e 4/5 classificações esperadas. A revisão qualitativa foi assistida por Codex. |
| Risco baixo/médio/alto | enum validado, cartão de resultado | Pytest + Vitest |
| Sinais e explicação | categorias validadas, citações verificadas, texto simples | testes de formato; qualidade depende da eval |
| Recomendações | resultado e prompt preventivo | Vitest; revisão humana na eval |
| Histórico | paginação, autorização por usuário, detalhes | Pytest + Vitest |
| Feedback | útil/não útil, comentário opcional, uma avaliação por análise | Pytest + Vitest |
| Minimização | texto/evidências não salvos por padrão, opt-in e exclusão | Pytest |
| Banco PostgreSQL | SQLAlchemy, driver psycopg, `DATABASE_URL`, Docker Compose para execução local e PostgreSQL no Neon na versão publicada | C2: validação local por Docker/PostgreSQL registrada em `VALIDACAO_PUBLICACAO.md`; C3: PostgreSQL no Neon conforme configuração e verificações comunicadas pela equipe. A instalação local sem `DATABASE_URL` utiliza SQLite. |
| Testes | Pytest, Vitest e GitHub Actions | C2: verificações históricas em `VALIDACAO.md`; C3: validação local da candidata 2.2.2 com 70 testes de backend, 29 de frontend e 1 teste PostgreSQL aprovados, conforme `TESTES_C3.md`. Build frontend concluído com ressalvas documentadas. O teste PostgreSQL utilizou ambiente local descartável e provedor simulado; não comprova isoladamente o banco de produção. |
| Eval | Conjuntos sintéticos, métricas e rubrica qualitativa da IA | C2: rodada V2 preservada em `eval/results-v2.json`; C3: avaliação da versão 2.2.2 com 5/5 respostas válidas e 4/5 classificações esperadas (80%), registrada em `docs/AVALIACAO_FINAL_C3.md`. Revisão qualitativa assistida por Codex, com 16 critérios adequados e 4 parciais. Amostra pequena, sem comprovação de desempenho em uso real. |
| Publicação | Dockerfile, configuração de implantação, Render e PostgreSQL no Neon | C2: demonstração local; C3: versão publicada em https://desconfia.onrender.com/, commit `4b9d160`. Healthcheck HTTP 200 e fluxos de análise, histórico e feedback verificados conforme comunicado da equipe. Registro em `VALIDACAO_PUBLICACAO.md`. |

## Segurança e privacidade

Senhas usam PBKDF2-SHA256 com sal via Passlib; o banco não recebe a senha original.
JWT é validado no servidor; dados pessoais exigem autenticação e verificação de dono.
Limites básicos por minuto: 20 tentativas de autenticação por IP e 10 análises por
usuário. O limitador é em memória, limitado a 10 mil chaves, para um único worker.
Ao escalar para múltiplos processos, substitua-o por armazenamento compartilhado.

A chave Groq nunca vai para o navegador. Mensagens são separadas das instruções do
modelo, sem ferramentas ou navegação externa. O back-end valida enums, limites,
campos extras e se as citações existem no texto. Isso reduz riscos, mas não garante
que a explicação esteja correta ou que todo ataque de prompt injection seja impedido.

Por padrão, o texto original e as citações não ficam no banco; resultados e comentários
ainda podem conter dados pessoais inseridos pelo usuário ou reproduzidos pelo modelo.
O aviso pede remoção antes do envio, e o prompt pede que não sejam reproduzidos.
Não há promessa de anonimização automática. O conteúdo é enviado à Groq quando a
análise real está ativada. Revise os termos do provedor antes da publicação.
O histórico permanece até exclusão manual; definir retenção institucional é uma
decisão pendente do grupo. Excluir uma análise remove também sinais e feedback.

Antes de receber usuários reais, o grupo deve definir responsável pelo tratamento,
contato de privacidade, retenção e procedimento de exclusão de conta. Este MVP não
é uma certificação de conformidade legal. A sessão é em memória e o logout não
invalida tokens já copiados; para revogação imediata, adicionar sessões persistidas.

## Organização para os checkpoints

- C2 (30/10/2026): configurar Groq, testar PostgreSQL, executar os casos de eval,
  revisar resultados e documentar evidências do protótipo funcional.
- C3 (04/12/2026): ampliar e revisar o conjunto, consolidar métricas, configurar
  hospedagem, verificar o fluxo publicado e atualizar a documentação com o provedor e a URL escolhidos.
