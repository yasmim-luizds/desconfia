# Roteiro de demonstração — Desconfia

**Duração sugerida:** 5–7 minutos
**Ambiente:** demonstração local da C2 em `http://127.0.0.1:8000`. A instalação manual sem `DATABASE_URL` usa SQLite; o Compose usa PostgreSQL. Não há URL pública para a C2. O planejamento da C3 prevê configurar hospedagem.
**Dados:** usar somente contas e mensagens fictícias. Não inserir mensagens recebidas por pessoas, nomes, telefones, códigos, links reais ou credenciais.

## Antes de começar

Antes de começar, decidir qual ambiente será usado na gravação. No modo demo, definir `AI_MODE=demo`. Na instalação manual, conferir também o banco ativo: sem `DATABASE_URL`, será SQLite. Se usar Docker Compose, confirmar que o PostgreSQL está saudável. Não mostrar credenciais nem apresentar a execução local como publicação em nuvem.

A aplicação oferece triagem automatizada de texto, não uma confirmação de fraude nem aconselhamento financeiro. Uma classificação baixa não garante que uma mensagem seja segura. Para casos reais, confirmar por canal independente conhecido.

## Sequência sugerida

1. **Apresentar o escopo.** Explicar que a demonstração usa dados sintéticos e que a aplicação classifica sinais em risco baixo, médio ou alto. Informar se a tela está em modo demonstração ou conectada à IA.
2. **Criar uma conta de teste e entrar.** Usar endereço fictício reservado para testes e senha temporária, sem reutilizar credenciais pessoais. Demonstrar também logout e retorno ao formulário de login.
3. **Analisar uma mensagem sintética.** Exemplo fictício: “Sua conta será bloqueada hoje. Para liberar o acesso, faça um Pix de R$ 1,00 neste aplicativo de demonstração.” Mostrar risco, sinais, explicação e recomendação. Não declarar que o resultado prova a existência de golpe.
4. **Mostrar privacidade e histórico.** Explicar que o armazenamento da mensagem depende da opção apresentada na interface. Abrir o histórico e destacar que a conta de teste deve ver apenas os próprios registros.
5. **Enviar feedback e remover o registro de teste.** Enviar feedback sem dados pessoais. Excluir a análise criada e confirmar que ela desapareceu. O procedimento de exclusão de conta inteira ainda precisa ser confirmado pelo grupo; não alegar que esse fluxo foi demonstrado se não houver funcionalidade correspondente.
6. **Explicar banco e hospedagem.** A demonstração local é a opção da C2; na instalação manual usada no computador da Yasmin, sem `DATABASE_URL`, o banco é SQLite. O Compose foi usado separadamente para validar PostgreSQL e persistência. Não dizer que a aplicação da gravação está usando PostgreSQL se o ambiente mostrar SQLite. A C3 ainda prevê configurar hospedagem; não há URL pública da C2.
7. **Encerrar com limitações.** Mencionar que a avaliação V2 usou um conjunto pequeno e sintético, que uma revisão independente e o consenso estão pendentes e que o sistema pode errar ou não responder. Evitar alegações de precisão geral, segurança garantida ou impacto social comprovado.

## Dados sintéticos adicionais para perguntas

- **Mensagem sem sinais claros:** “Oi, a reunião de estudo foi transferida para amanhã às 14h. Pode confirmar?”
- **Pedido urgente suspeito:** “Sou eu com outro número. Preciso que você transfira agora; não ligue para confirmar.”
- **Falha controlada:** deixar o campo vazio ou usar o controle de demonstração previsto pela equipe. Não provocar falhas em um serviço externo real durante a apresentação.

## Pendências que não devem ser improvisadas

A execução local corresponde à demonstração da C2. A hospedagem da C3 continua planejada, mas ainda sem provedor ou URL definidos. Retenção de dados, contato de privacidade e escopo da exclusão completa de conta continuam em avaliação; não apresentar decisões que o grupo ainda não tomou.

No computador da gravação, não é necessário repetir toda a bateria: confirme o modo e o banco ativos, abra `/health` e `/config`, e complete um fluxo curto com conta e mensagem sintéticas (cadastro ou login, análise, histórico e feedback).
