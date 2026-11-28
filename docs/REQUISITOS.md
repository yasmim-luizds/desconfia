# Escopo e rastreabilidade

O Desconfia é um projeto acadêmico web de análise textual, demonstrado com contas e mensagens sintéticas. Sua avaliação técnica utiliza conjuntos controlados. Os resultados descrevem a aplicação e o potencial de apoio à comunidade.

| Requisito | Implementação | Verificação |
|---|---|---|
| Cadastro e login | formulários React, `/auth/register`, `/auth/login` | Pytest + Vitest |
| Logout | limpeza de sessão em memória | Vitest |
| Envio textual | validação de 1–2000 caracteres e consentimento na interface | Pytest + Vitest |
| Groq | `backend/app/ai.py`, tratamento de erros, timeout e validação de respostas | C2: testes simulados e rodada V2 em `eval/results-v2.json`; C3: avaliação real da versão 2.2.2 registrada em `docs/AVALIACAO_FINAL_C3.md`, com 5/5 respostas válidas e 4/5 classificações esperadas. A revisão qualitativa foi assistida por Codex. |
| Risco baixo/médio/alto | enum validado, cartão de resultado | Pytest + Vitest |
| Sinais e explicação | categorias validadas, citações verificadas, texto simples | testes de formato; qualidade depende da eval |
| Recomendações | Texto preventivo controlado pela aplicação, escolhido conforme o risco; o modelo gera risco, explicação e sinais | Pytest + Vitest e revisão qualitativa assistida em `eval/revisao-final-222-assistida.json` |
| Histórico | paginação, autorização por usuário, detalhes | Pytest + Vitest |
| Feedback | útil/não útil, comentário opcional, uma avaliação por análise | Pytest + Vitest |
| Minimização | texto/evidências não salvos por padrão, opt-in e exclusão | Pytest |
| Banco PostgreSQL | SQLAlchemy, driver psycopg, `DATABASE_URL`, Docker Compose para execução local e PostgreSQL no Neon na versão publicada | C2: validação local por Docker/PostgreSQL registrada em `VALIDACAO_PUBLICACAO.md`; C3: PostgreSQL no Neon conforme configuração e verificações comunicadas pela equipe. A instalação local sem `DATABASE_URL` utiliza SQLite. |
| Testes | Pytest, Vitest e GitHub Actions | C2: verificações históricas em `VALIDACAO.md`; C3: validação local da candidata 2.2.2 com 70 testes de backend, 29 de frontend e 1 teste PostgreSQL aprovados, conforme `TESTES_C3.md`. Build frontend concluído com ressalvas documentadas. O teste PostgreSQL utilizou ambiente local descartável e provedor simulado; não comprova isoladamente o banco de produção. |
| Eval | Conjuntos sintéticos, métricas e rubrica qualitativa da IA | C2: rodada V2 preservada em `eval/results-v2.json`; C3: avaliação da versão 2.2.2 com 5/5 respostas válidas e 4/5 classificações esperadas (80%), registrada em `docs/AVALIACAO_FINAL_C3.md`. Revisão qualitativa assistida por Codex, com 16 critérios adequados e 4 parciais. Amostra pequena, sem comprovação de desempenho em uso real. |
| Publicação | Dockerfile, configuração de implantação, Render e PostgreSQL no Neon | C2: demonstração local; C3: versão publicada em https://desconfia.onrender.com/, commit `4b9d160`. Healthcheck HTTP 200 e fluxos de análise, histórico e feedback verificados conforme comunicado da equipe. Registro em `VALIDACAO_PUBLICACAO.md`. |

## IA responsável

### Dados sintéticos e privacidade

As demonstrações e a avaliação desta entrega usam contas de teste e mensagens inventadas. Esse é o recorte acadêmico adotado para o tópico de privacidade/LGPD do edital.

No modo `groq`, o texto é enviado à Groq para processamento. A conta utiliza nome, e-mail e senha de teste; a senha é armazenada como hash PBKDF2-SHA256 com sal. O histórico contém resultado, sinais e feedback. Por padrão, o texto original e as citações não são persistidos; a opção `store_message` permite guardá-los. Explicações e comentários também podem reproduzir informações da entrada. A interface orienta a remoção de dados sensíveis e solicita a concordância antes do envio.

A exclusão de uma análise remove seus sinais e feedbacks. As demonstrações utilizam dados sintéticos também nos registros técnicos e nas capturas. Segredos de configuração ficam no ambiente do serviço e fora do repositório.

### Segurança e instruções adversariais

O servidor valida JWT e propriedade dos registros. A sessão do navegador permanece em memória; um token já emitido conserva sua validade até expirar, mesmo após logout.

Mensagens são separadas das instruções do modelo e tratadas como dados não confiáveis. O backend valida esquema, limites e literalidade das citações. A recomendação preventiva é acrescentada pela aplicação, sem incorporar o conselho livre produzido pelo modelo. Os testes incluem tentativas de manipular classificação, idioma e indicadores.

### Ética, vieses e comunicação

A avaliação considera mensagens legítimas, suspeitas, ambíguas, variações linguísticas e ataques. O prompt orienta a interpretar abreviações pelo contexto e a avaliar pedidos e sinais, sem usar ortografia informal como indício de fraude por si só. Os rótulos dos casos são hipóteses do projeto, preservadas nas comparações.

A versão 2.2.2 teve quatro classificações esperadas em cinco respostas válidas. O caso ambíguo divergente e as ressalvas das explicações estão na [avaliação da C3](AVALIACAO_FINAL_C3.md). As notas qualitativas são assistidas e identificam o autor. O tamanho e a composição da amostra delimitam a interpretação dos percentuais.

Risco baixo não garante segurança; risco alto expressa indícios presentes no texto. A comunicação orienta a confirmação por canal independente conhecido e apresenta o impacto social como [potencial de apoio](IMPACTO_SOCIAL_C3.md).

### Chamadas, custo e uso de recursos

O código oferece dois níveis de controle:

| Controle | Padrão do código |
|---|---|
| Autenticação por endereço | 20 tentativas por minuto |
| Análise por usuário | 10 por minuto |
| Tentativas globais de IA, compartilhadas no banco | `AI_GLOBAL_PER_MINUTE=20` e `AI_GLOBAL_PER_DAY=200` |

Os limites globais são configuráveis por variáveis de ambiente e usam janelas UTC. Cada tentativa admitida consome quota, inclusive quando o provedor falha; a resposta ao esgotamento é HTTP 429 com orientação de espera. O limitador local fica em memória no worker da aplicação.

Esses valores são limites da aplicação, distintos da franquia de tokens ou dos limites da conta Groq. O programa de avaliação chama a Groq diretamente e registra quantidade de tentativas, intervalo, modelo e resultados; seu uso de recursos deve ser contabilizado à parte. A opção `--stop-on-rate-limit` interrompe a rodada e preserva a tentativa ao receber limite do provedor.

As demonstrações usam rodadas pequenas e intervalos definidos para controlar o consumo. O uso no provedor pode ser acompanhado pelo painel da conta e pelos registros de tokens, quando fornecidos pela API, preservando mensagens sintéticas e segredos.

## Entregas do projeto

- C2: protótipo, primeiros testes e avaliação V2 preservados nos registros históricos.
- C3: versão publicada no Render com PostgreSQL no Neon, testes, avaliação 2.2.2, matriz de evidências e análise de impacto.

As fontes e os resultados estão nos [testes da C3](TESTES_C3.md), na [avaliação da IA](AVALIACAO_FINAL_C3.md) e no [registro de publicação](VALIDACAO_PUBLICACAO.md).
