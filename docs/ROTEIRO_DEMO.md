# Roteiro de demonstração — Desconfia

**Duração sugerida:** 5–7 minutos
**Ambiente:** local, via Docker Compose, em `http://127.0.0.1:8000`; o endereço só abre no computador da demonstração e não é uma URL pública.
**Dados:** usar somente contas e mensagens fictícias. Não inserir mensagens recebidas por pessoas, nomes, telefones, códigos, links reais ou credenciais.

## Antes de começar

Antes de começar, confirmar que Docker está ativo e escolher com o grupo entre modo demonstração e integração real com IA. Para demo, usar `AI_MODE=demo`; se a equipe ativar a Groq, configurar a chave somente em variável local protegida, conferir quota/custos e não mostrar credenciais na tela. Não apresentar a execução local como produção pública.

A aplicação oferece triagem automatizada de texto, não uma confirmação de fraude nem aconselhamento financeiro. Uma classificação baixa não garante que uma mensagem seja segura. Para casos reais, confirmar por canal independente conhecido.

## Sequência sugerida

1. **Apresentar o escopo.** Explicar que a demonstração usa dados sintéticos e que a aplicação classifica sinais em risco baixo, médio ou alto. Informar se a tela está em modo demonstração ou conectada à IA.
2. **Criar uma conta de teste e entrar.** Usar endereço fictício reservado para testes e senha temporária, sem reutilizar credenciais pessoais. Demonstrar também logout e retorno ao formulário de login.
3. **Analisar uma mensagem sintética.** Exemplo fictício: “Sua conta será bloqueada hoje. Para liberar o acesso, faça um Pix de R$ 1,00 neste aplicativo de demonstração.” Mostrar risco, sinais, explicação e recomendação. Não declarar que o resultado prova a existência de golpe.
4. **Mostrar privacidade e histórico.** Explicar que o armazenamento da mensagem depende da opção apresentada na interface. Abrir o histórico e destacar que a conta de teste deve ver apenas os próprios registros.
5. **Enviar feedback e remover o registro de teste.** Enviar feedback sem dados pessoais. Excluir a análise criada e confirmar que ela desapareceu. O procedimento de exclusão de conta inteira ainda precisa ser confirmado pelo grupo; não alegar que esse fluxo foi demonstrado se não houver funcionalidade correspondente.
6. **Explicar persistência e hospedagem.** O grupo escolheu execução local: abrir `http://127.0.0.1:8000` no computador da apresentação, sem apresentar isso como URL pública. Docker/PostgreSQL e persistência foram testados com dados sintéticos em 27/10/2026 no computador local do responsável. Não é necessário repetir os testes no computador do grupo; apresentar somente as verificações efetivamente realizadas. Os detalhes estão em `VALIDACAO_PUBLICACAO.md`.
7. **Encerrar com limitações.** Mencionar que a avaliação V2 usou um conjunto pequeno e sintético, que uma revisão independente e o consenso estão pendentes e que o sistema pode errar ou não responder. Evitar alegações de precisão geral, segurança garantida ou impacto social comprovado.

## Dados sintéticos adicionais para perguntas

- **Mensagem sem sinais claros:** “Oi, a reunião de estudo foi transferida para amanhã às 14h. Pode confirmar?”
- **Pedido urgente suspeito:** “Sou eu com outro número. Preciso que você transfira agora; não ligue para confirmar.”
- **Falha controlada:** deixar o campo vazio ou usar o controle de demonstração previsto pela equipe. Não provocar falhas em um serviço externo real durante a apresentação.

## Pendências que não devem ser improvisadas

O grupo escolheu execução local, sem URL pública. Retenção de dados, contato de privacidade e escopo da exclusão completa de conta continuam em avaliação. Até haver decisão, descrevê-los como pendentes e não preencher com valores fictícios apresentados como decisões reais.

Antes da apresentação, o grupo deve conferir se a sequência e as limitações continuam correspondendo ao funcionamento da versão demonstrada.
