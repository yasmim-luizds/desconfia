# Testes Funcionais — Desconfia

## 1. Objetivo
Verificar o funcionamento das principais funcionalidades da aplicação Desconfia, incluindo fluxos válidos, entradas inválidas, tratamento de erros e isolamento de dados entre usuários.

## 2. Ambiente de testes
- Responsável: Hellen
- Branch: testes-c2
- Sistema operacional: Windows 11
- Navegador: Google Chrome
- Ambiente: execução local
- Endereço: http://127.0.0.1:8000
- Modo inicial: demonstração (sem IA real)
- Data dos testes: 27/10/2026
- Versão do código (hash do commit): fd4fd72cc79f91fc3b0aa038091ed182b3a5ed6e
- Versão integrada para os testes (hash): e8484f2db26e287caa80bc0f86a5e5df95df9d9c

## 3. Cenários de testes

| ID | Cenário | Passos | Resultado esperado | Resultado obtido | Situação |
|---|---|---|---|---|---|
| TF-01 | Cadastro válido | Preencher cadastro com dados fictícios válidos e confirmar | Conta criada com sucesso | Cadastro concluído; sistema exibiu a área autenticada de análise de mensagens | Aprovado |
| TF-02 | Login válido | Entrar com conta fictícia previamente cadastrada | Acesso autorizado | Login realizado e área autenticada de análise exibida | Aprovado |
| TF-03 | Senha incorreta | Informar e-mail cadastrado e senha incorreta, depois clicar em Entrar | Acesso negado com mensagem adequada | Sistema permaneceu na tela de login e exibiu "E-mail ou senha inválidos" | Aprovado |
| TF-04 | Logout | Clicar em Sair na área autenticada | Sessão encerrada | Aplicação retornou à página inicial com opções Entrar e Criar conta | Aprovado |
| TF-05 | Análise de mensagem | Enviar mensagem sintética com urgência, ameaça de bloqueio e solicitação de Pix | Exibição do resultado de análise | Sistema apresentou risco alto, três sinais identificados, explicação e recomendação preventiva em modo demonstração | Aprovado |
| TF-06 | Mensagem vazia | Deixar o campo de mensagem vazio e marcar a confirmação do modo demonstração | Sistema rejeita a entrada | Botão Analisar mensagem permaneceu visualmente desabilitado com contador 0/2000 | Aprovado na verificação visual |
| TF-06B | Botão habilitado com texto | Digitar a letra A no campo e marcar a confirmação do modo demonstração | Botão Analisar mensagem fica habilitado | Com um caractere no campo, contador exibiu 1/2000 e botão ficou visualmente habilitado | Aprovado na verificação visual |
| TF-07 | Mensagem longa | Colar texto sintético de 2.100 caracteres para verificar o limite máximo permitido pelo campo | Respeitar o limite de 2.000 caracteres | Campo limitou o conteúdo a 2.000 caracteres, exibindo contador 2000/2000 | Aprovado na verificação visual |
| TF-08 | Histórico | Acessar o histórico da conta e abrir a análise salva anteriormente | Histórico correspondente à conta | Sistema exibiu análise de risco alto, informou que o texto original não foi armazenado e permitiu reabrir o resultado com sinais e recomendações | Aprovado |
| TF-08B | Histórico com texto armazenado | Marcar a opção de guardar a mensagem, realizar análise e reabrir pelo histórico | Texto original disponível no histórico | Sistema exibiu a mensagem original salva ao expandir "Mensagem analisada" | Aprovado |
| TF-09 | Feedback | Selecionar Sim em uma análise e clicar em Enviar feedback, sem comentário | Feedback registrado ou confirmação adequada | Sistema exibiu "Obrigado! Seu feedback foi registrado." | Aprovado |
| TF-10 | Exclusão | Solicitar exclusão da análise de risco alto, cancelar e depois confirmar a exclusão | Cancelamento mantém o registro; confirmação remove somente a análise selecionada | Ao cancelar, as duas análises permaneceram no histórico; ao confirmar, a análise de risco alto desapareceu e a de risco baixo permaneceu | Aprovado na verificação visual |
| TF-11 | Isolamento entre contas | Acessar duas contas fictícias, criar análise na Conta B e verificar separadamente os históricos das duas contas | Uma conta não visualiza as análises da outra | Conta B iniciou com histórico vazio e depois exibiu apenas sua análise de risco alto; Conta A manteve somente sua análise de risco baixo | Aprovado na verificação pela interface |
| TF-12 | Indisponibilidade da IA | Executar testes automatizados com respostas simuladas do provedor Groq, incluindo erros HTTP, timeout, ausência de chave e respostas inválidas | Falhas tratadas com erros apropriados, sem retornar uma análise inventada | Arquivo test_ai.py executado com 16 testes aprovados e 1 aviso; cenários de falha simulados passaram | Aprovado na simulação automatizada |
| TF-13 | Interface e acessibilidade | Verificar as telas no computador com zoom de 100%, simular celular com largura de 390 px e testar navegação por teclado | Interface legível, controles acessíveis e ausência de cortes ou sobreposições indevidas | Formulário, histórico e resultado funcionaram nas verificações realizadas; navegação por teclado e foco visível verificados | Aprovado na verificação manual |

## 4. Evidências
- TF-01: [Cadastro aprovado](evidencias/TF-01-cadastro-aprovado.png)
- TF-02: [Login aprovado](evidencias/TF-02-login-aprovado.png)
- TF-03: [Senha incorreta](evidencias/TF-03-senha-incorreta.png)
- TF-04: [Logout aprovado](evidencias/TF-04-logout-aprovado.png)
- TF-05: [Análise de mensagem](evidencias/TF-05-analise-aprovada.png)
- TF-06: [Mensagem vazia](evidencias/TF-06-mensagem-vazia.png)
- TF-06B: [Botão habilitado com texto](evidencias/TF-06-botao-habilitado.png)
- TF-07: [Limite de 2.000 caracteres](evidencias/TF-07-mensagem-longa.png)
- TF-08: [Histórico de análises](evidencias/TF-08-historico.png)
- TF-08 (Resultado reaberto): [Resultado reaberto](evidencias/TF-08-resultado-reaberto.png)
- TF-08B: [Mensagem original armazenada](evidencias/TF-08B-mensagem-armazenada.png)
- TF-09: [Feedback registrado](evidencias/TF-09-feedback-aprovado.png)
- TF-10: [Confirmação de exclusão](evidencias/TF-10-confirmacao-exclusao.png)
- TF-10 (Cancelamento): [Histórico preservado](evidencias/TF-10-cancelamento.png)
- TF-10 (Exclusão): [Análise removida](evidencias/TF-10-exclusao-aprovada.png)
- TF-11: [Histórico inicial da Conta B](evidencias/TF-11-conta-b-historico-vazio.png)
- TF-11: [Análise exclusiva da Conta B](evidencias/TF-11-conta-b-analise.png)
- TF-11: [Histórico isolado da Conta A](evidencias/TF-11-conta-a-isolamento.png)
- TF-12: [Testes automatizados de falhas da IA — 16 aprovados](evidencias/TF-12-testes-ia-aprovados.png)
- TF-13: [Interface no computador](evidencias/TF-13-interface-pc.png)
- TF-13: [Interface no celular](evidencias/TF-13-interface-celular.png)
- TF-13: [Histórico no celular](evidencias/TF-13-historico-celular.png)
- TF-13: [Resultado no celular](evidencias/TF-13-resultado-celular.png)
- TF-13: [Navegação por teclado](evidencias/TF-13-navegacao-teclado.png)

## 5. Defeitos identificados
Registrar ID do teste, descrição, passos de reprodução, comportamento observado, comportamento esperado e link da Issue correspondente.

## 6. Retestes após correções
Registrar os cenários repetidos, a versão testada, o resultado e as evidências.

## 7. Limitações e pendências
- TF-12: O tratamento de falhas da IA foi verificado por testes automatizados com respostas simuladas da API Groq. Foram aprovados 16 testes do arquivo backend/tests/test_ai.py, com um aviso de depreciação. Não foi realizada uma simulação de indisponibilidade real da Groq nem a validação da mensagem de erro pela interface, pois a aplicação foi executada em modo demonstração.
- TF-13 — Interface e acessibilidade: Foram realizadas verificações manuais da interface no computador (zoom de 100%) e em uma tela de celular simulada (largura de 390 px), incluindo formulário, histórico e resultado das análises. Também foram testados a navegação por teclado e o foco visível nos controles. Não foram identificados problemas nas verificações realizadas. O teste não constitui uma auditoria completa de acessibilidade, pois não incluiu avaliação com leitores de tela, análise sistemática de contraste ou verificação integral dos critérios WCAG.