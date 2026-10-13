# Publicação do Desconfia

A publicação foi adiada a pedido da usuária, que ainda criará as contas necessárias.
Este guia usa Render como exemplo previsto na proposta. Não foram criados serviços,
contas, cobranças ou recursos em nuvem.

## 1. Preparar o repositório

Publique o conteúdo de `desconfia_pronto` como raiz do repositório. Se mantiver essa
pasta dentro de outra, configure-a como Root Directory do serviço e adapte o CI.
Não envie `.env`, `.venv`, `node_modules`, arquivos `.db` ou credenciais.
Inclua `pnpm-lock.yaml`, `Dockerfile`, `frontend`, `backend`, `eval` e `docs`.

## 2. Configurar a Groq

Crie conta em https://console.groq.com, gere uma chave e confira modelo, quota e
limites no painel. O padrão usado é `openai/gpt-oss-20b`, com JSON Schema estrito.
Defina `GROQ_API_KEY` somente no serviço do back-end. Execute a avaliação local
antes de considerar o sistema validado. Modelo e disponibilidade podem mudar.
Documentação: https://console.groq.com/docs/structured-outputs.

## 3. Criar PostgreSQL

No Render, crie um banco PostgreSQL e copie sua conexão interna para `DATABASE_URL`
do serviço web na mesma região. Endereços `postgres://` e `postgresql://` são
normalizados automaticamente para o driver psycopg.

Confira a duração do plano escolhido: na documentação consultada em 27/09/2026,
o PostgreSQL gratuito expira após 30 dias e não oferece backups. Não confie nele
para preservar dados até dezembro sem planejar migração/backup e custos.
Fonte: https://render.com/docs/free.

## 4. Criar o serviço web

Conecte o repositório a um Web Service com runtime Docker. O Dockerfile compila o
React e serve a interface junto com a API, no mesmo domínio. Use `/health` como
health check. Configure no painel:

| Variável | Valor |
|---|---|
| `APP_ENV` | `production` |
| `AI_MODE` | `groq` |
| `DATABASE_URL` | conexão PostgreSQL privada do serviço |
| `GROQ_API_KEY` | chave gerada na sua conta |
| `GROQ_MODEL` | `openai/gpt-oss-20b` ou modelo compatível verificado |
| `DESCONFIA_SECRET_KEY` | segredo aleatório de pelo menos 32 caracteres |
| `CORS_ORIGINS` | URL HTTPS do próprio serviço |

`PORT` é fornecida pela plataforma. O comando usa um worker para respeitar o
limitador atual. Não execute o seed de demonstração em produção. O PostgreSQL
novo começa vazio; crie sua própria conta pela interface.

Veja https://render.com/docs/docker e https://render.com/docs/your-first-deploy.

## 5. Verificar antes da apresentação

1. Abra a URL HTTPS, cadastre duas contas de teste e confira login/logout.
2. Analise uma mensagem sintética, confirme o selo “Análise com IA” e confira
   sinais, explicação e recomendação.
3. Verifique que o histórico de uma conta não aparece na outra.
4. Envie feedback, recarregue e confirme que ele continua registrado.
5. Exclua somente a análise de teste e confira sua remoção.
6. Reinicie o serviço e confira a persistência no PostgreSQL.
7. Execute a eval real e registre modelo, data, falhas e revisão qualitativa.

O plano gratuito pode suspender o serviço após inatividade; a primeira abertura
pode demorar. Revise custos e quotas antes de ativar qualquer plano.
O Dockerfile e o Compose foram preparados, mas precisam ser executados e verificados
em um ambiente com Docker/PostgreSQL; nenhum deploy foi realizado nesta entrega.
