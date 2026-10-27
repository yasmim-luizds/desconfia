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
- Data dos testes: a preencher
- Versão do código (hash do commit): fd4fd72cc79f91fc3b0aa038091ed182b3a5ed6e

## 3. Cenários de testes

| ID | Cenário | Passos | Resultado esperado | Resultado obtido | Situação |
|---|---|---|---|---|---|
| TF-01 | Cadastro válido | Preencher cadastro com dados fictícios válidos e confirmar | Conta criada com sucesso | Não executado | Pendente |
| TF-02 | Login válido | Entrar com conta cadastrada | Acesso autorizado | Não executado | Pendente |
| TF-03 | Senha incorreta | Tentar entrar com senha errada | Acesso negado com mensagem adequada | Não executado | Pendente |
| TF-04 | Logout | Sair da conta autenticada | Sessão encerrada | Não executado | Pendente |
| TF-05 | Análise de mensagem | Enviar uma mensagem sintética válida | Exibição do resultado de análise | Não executado | Pendente |
| TF-06 | Mensagem vazia | Tentar analisar texto vazio | Sistema rejeita a entrada | Não executado | Pendente |
| TF-07 | Mensagem longa | Enviar texto que exceda o limite permitido | Validação apropriada | Não executado | Pendente |
| TF-08 | Histórico | Consultar análises feitas pela conta | Histórico correspondente à conta | Não executado | Pendente |
| TF-09 | Feedback | Enviar feedback de uma análise | Feedback registrado ou confirmação adequada | Não executado | Pendente |
| TF-10 | Exclusão | Solicitar exclusão de dados ou conta conforme a interface disponível | Exclusão realizada com confirmação | Não executado | Pendente |
| TF-11 | Isolamento entre contas | Criar duas contas e verificar acesso aos respectivos históricos | Uma conta não acessa os dados da outra | Não executado | Pendente |
| TF-12 | Indisponibilidade da IA | Simular ou observar falha do serviço de IA | Erro tratado sem resultado inventado | Não executado | Pendente |
| TF-13 | Interface e acessibilidade | Conferir telas em computador e celular, teclado e mensagens de estado | Interface legível, acessível e sem cortes indevidos | Não executado | Pendente |

## 4. Evidências
Inserir os nomes e caminhos das capturas de tela, sem senhas ou dados pessoais. Relacionar cada evidência ao ID do teste.

## 5. Defeitos identificados
Registrar ID do teste, descrição, passos de reprodução, comportamento observado, comportamento esperado e link da Issue correspondente.

## 6. Retestes após correções
Registrar os cenários repetidos, a versão testada, o resultado e as evidências.

## 7. Limitações e pendências
Separar funcionalidades indisponíveis, testes não executados, limitações do modo demonstração e atividades dependentes de integração ou correção.