# Registro de uso de IA: frente de interface

**Responsável:** Gustavo Rissoli
**Ferramenta:** Claude (Anthropic), em conversa de chat
**Motivo do registro:** o edital do Projeto Integrador IV (seção 11) exige que todo o processo de engenharia de software feito com apoio de IA seja registrado no repositório, com o prompt usado em cada tarefa.

> **Como ler:** os prompts abaixo estão **resumidos** com as palavras do autor; os trechos entre aspas são literais. Todas as sugestões foram aplicadas manualmente (troca de trechos nos arquivos), lidas, testadas e revisadas pelo autor antes de cada commit.

## Resumo

| ID | Período | Tarefa | Arquivos afetados |
|---|---|---|---|
| P01 | setembro/2026 | Aprender Git e GitHub aplicados ao projeto | nenhum (processo) |
| P02 | 17/10/2026 | Preparar o ambiente e rodar o projeto | nenhum (processo) |
| P03 | 17/10/2026 | Diagnóstico e priorização das melhorias; contraste (Fase 1) | `frontend/src/styles.css` |
| P04 | 24/10/2026 | Tamanho mínimo das fontes (Fase 2) | `frontend/src/styles.css` |
| P05 | 24/10/2026 | Histórico cortado e confirmação de exclusão (Fase 3) | `frontend/src/styles.css`, `frontend/src/App.jsx` |
| P06 | 24 a 27/10/2026 [conferir] | Mensagens de erro (Fase 4a) e aviso visível (Fase 4b) | `frontend/src/api.js`, `frontend/src/api.test.js`, `frontend/src/styles.css` |
| P07 | 24 a 27/10/2026 [conferir] | Investigação do corte na visualização do celular | nenhum |
| P08 | 24 a 27/10/2026 [conferir] | Tela de resultado (Fase 5) | `frontend/src/App.jsx`, `frontend/src/styles.css` |
| P09 | 24 a 27/10/2026 [conferir] | Teclado, foco e estados (Fase 6) | `frontend/src/styles.css` |
| P10 | 24 a 27/10/2026 [conferir] | Correção do título do histórico e validação por campo (Fase 4c) | `frontend/src/App.jsx`, `frontend/src/styles.css`, `frontend/src/validacao.test.jsx` |
| P11 | 24 a 27/10/2026 [conferir] | Mostrar e ocultar senha | `frontend/src/App.jsx`, `frontend/src/validacao.test.jsx` |
| P12 | 24 a 27/10/2026 [conferir] | Atualizar a branch com a base e preparar o Pull Request | nenhum (processo) |
| P13 | 24 a 27/10/2026 [conferir] | Rascunho desta documentação e do registro de prompts | `docs/MELHORIAS_INTERFACE.md`, `docs/PROMPTS_INTERFACE.md` |

## Detalhamento

### P01: Aprender Git e GitHub
- **Prompt (resumo):** o autor pediu orientação para usá-lo de forma voltada ao trabalho, com base no edital e na ideia do grupo; depois pediu um roteiro simples para praticar sem atrapalhar o grupo.
- **Aproveitado:** passo a passo de clone, branch, commit, push e Pull Request.
- **Verificação:** aplicado no repositório do grupo (branches `melhoria-interface` e `melhoria-interface-2` e Pull Requests).

### P02: Preparar o ambiente
- **Prompt (resumo):** pedido de ajuda para instalar as ferramentas, clonar o repositório, rodar a aplicação e percorrer as telas.
- **Aproveitado:** lista de ferramentas (Git, Node.js, VS Code), comandos de clone, uso do pnpm e do modo demonstração.
- **Verificação:** aplicação rodando; `pnpm --dir frontend test` com 8 de 8 testes passando e build sem erros antes de qualquer alteração.

### P03: Diagnóstico, priorização e contraste (Fase 1)
- **Prompt (resumo):** envio das capturas das telas, do relatório do Lighthouse (nota 94, falha de contraste), das capturas de erro e do `styles.css`, pedindo uma lista de melhorias por prioridade.
- **Aproveitado:** lista priorizada, cálculo de contraste de cada par de cor e bloco de regras de cor no final do `styles.css`.
- **Verificação:** razões de contraste recalculadas, Lighthouse subiu para 100, testes e build passando, `git diff` com apenas linhas adicionadas.

### P04: Tamanho mínimo das fontes (Fase 2)
- **Prompt (resumo):** pedido para continuar com a fase seguinte (tamanho dos textos auxiliares) e o que conferir antes do commit.
- **Aproveitado:** bloco de regras de tamanho de fonte no final do `styles.css`.
- **Verificação:** comparação visual com as capturas de "antes" (computador e celular), testes, build e Lighthouse repetido.

### P05: Histórico cortado e confirmação de exclusão (Fase 3)
- **Prompt (resumo):** envio de capturas do histórico e da confirmação de exclusão, com a observação: "Pela tela do celular aparentemente fica cortando, me atentei a isso agora também, ou talvez eu que abria a visualização para celular de forma errada (só apertei F12)"; depois relatou o mesmo problema no computador com dois ou mais itens.
- **Aproveitado:** explicação da causa (colunas `1fr` com texto sem quebra), regras de CSS, duas trocas no `App.jsx` (aviso de ação irreversível e foco no "Cancelar").
- **Verificação:** conferência visual no computador e no celular, testes (incluindo "exige confirmação para excluir"), build.

### P06: Mensagens de erro e aviso visível (Fases 4a e 4b)
- **Prompt (resumo):** envio de `api.js`, `App.test.jsx` e `api.test.js` ("Só para termos certeza? Estamos dando início à parte 4?"), pedindo a melhoria das mensagens de erro.
- **Aproveitado:** novo `api.js` com mensagens por tipo de erro, 4 testes novos e regra de CSS para o aviso de erro ficar fixo no topo.
- **Verificação:** testes passando, backend desligado de propósito para ver a nova mensagem, teste do aviso em tela rolada no celular.

### P07: Investigação do corte na visualização do celular
- **Prompt (resumo):** relato de que, no modo iPhone 16 do F12, ficavam cortados o botão "Criar conta", o fim do aviso de erro e a borda dos campos; resultado do código de diagnóstico no console (`393 393 393`).
- **Aproveitado:** diagnóstico de que a página não ultrapassava a tela e que o corte vinha do espaço do painel do F12 (ajuste de zoom e posição do painel).
- **Verificação:** corte desapareceu após o ajuste; nenhuma alteração de código.

### P08: Tela de resultado (Fase 5)
- **Prompt (resumo):** pedido para avançar à fase da tela de resultado, usando o código do `App.jsx` já enviado, com foco em destacar o risco por texto, ícone e cor, e organizar sinais, explicação e recomendação.
- **Aproveitado:** regras de CSS de hierarquia, ícone no selo de risco, origem da análise em destaque e mudança do bloco "O que fazer agora" para depois do veredito (trocas no `App.jsx`).
- **Verificação:** conferência visual em demonstração com mensagens de risco alto e baixo, testes e build, capturas de antes e depois.

### P09: Teclado, foco e estados (Fase 6)
- **Prompt (resumo):** pedido para fechar a fase de teclado, foco, carregamento e estados vazios.
- **Aproveitado:** contorno de foco nos campos, estado selecionado do feedback em negrito e roteiro de teste só com teclado e com rede lenta.
- **Verificação:** teste realizados com tab, tab + shift e enter ocorreram perfeitamente, testes, build e Lighthouse por tela.

### P10: Título do histórico e validação por campo (Fase 4c)
- **Prompt (resumo):** envio das notas do Lighthouse por tela (histórico 15/16 por títulos fora de ordem) e pedido para fazer a validação por campo; depois: "ao inserir senha com mais de [8] caracteres porém senhas diferentes ainda aparece este 'balão' no topo, isso poderia ser melhorado?".
- **Aproveitado:** troca do `<h3>` por `<span>` no cartão do histórico, validação própria com mensagens abaixo de cada campo, erro de senhas diferentes no campo de confirmação e 3 testes em arquivo novo.
- **Verificação:** testes, build, conferência no navegador (login vazio, senha curta, senhas diferentes, troca entre login e cadastro).

### P11: Mostrar e ocultar senha
- **Prompt (resumo):** pedido para fazer o item opcional de mostrar e ocultar senha.
- **Aproveitado:** estado novo, caixa "Mostrar senha(s)" e teste de alternância.
- **Verificação:** conferência no login e no cadastro, testes e build.

### P12: Atualizar a branch com a base e preparar o Pull Request
- **Prompt (resumo):** pergunta sobre o commit de merge da Yasmim, com a saída dos comandos `git fetch`, `git branch -r --contains` e `git log`, e pedido da ordem correta dos próximos passos.
- **Aproveitado:** ordem de trabalho (commit, merge de `origin/base-c2`, testes, push, Pull Request 2/2) e uso de `git merge --abort` como segurança em caso de conflito.
- **Verificação:** só depois de fazer.

### P13: Documentação
- **Prompt (resumo):** pedido de rascunho do `docs/MELHORIAS_INTERFACE.md` e do registro de prompts.
- **Aproveitado:** estrutura dos dois documentos, tabela de contraste e lista de mudanças.
- **Verificação:** 2026-10-26  feat: opcao de mostrar e ocultar senha no login e cadastro
2026-10-26  Merge remote-tracking branch 'origin/base-c2' into melhoria-interface-2
2026-10-26  docs: corrige guia para novas rodadas de avaliacao
2026-10-26  Merge pull request #3 from yasmim-luizds/melhoria-interface
2026-10-26  Merge pull request #2 from yasmim-luizds/melhoria-ia
2026-10-26  feat: mensagens de validacao por campo no login e cadastro
2026-10-25  fix: usa span na previa do historico para corrigir ordem dos titulos
2026-10-25  style: foco visivel nos campos e estado selecionado alem da cor
2026-10-25  feat: mostra o que fazer agora logo apos o veredito na tela de resultado
2026-10-25  feat: icone no selo de risco e origem da analise em destaque
2026-10-25  style: melhora hierarquia e leitura da tela de resultado
2026-10-24  style: mantem aviso de erro visivel no topo ao aparecer
2026-10-24  feat: mensagens de erro mais claras para servico indisponivel, login e excesso de solicitacoes
2026-10-24  Melhora IA, corrige metricas e documenta avaliacao
2026-10-24  style: melhora historico em telas estreitas e confirmacao de exclusao
2026-10-24  style: aumenta tamanho minimo dos textos auxiliares
2026-10-17  style: melhora contraste dos textos secundarios
2026-10-13  docs: atualiza prompts, requisitos e revisao da avaliacao
2026-10-13  feat: importa base da aplicacao para a C2
2026-09-13  Merge branch 'main' of https://github.com/yasmim-luizds/desconfia
2026-09-13  atualiza estrutura inicial do projeto
2026-09-13  atualiza README do projeto Desconfia
2026-09-13  Initial commit

| P14 | 2026-10-27 | Erro de login e cadastro junto ao botão | frontend/src/App.jsx, frontend/src/styles.css, frontend/src/validacao.test.jsx |

### P14: Erro de login e cadastro junto ao botão
- **Prompt (resumo):** relato de que, ao tentar entrar com a senha errada, a mensagem aparecia como balão no topo da tela, perguntando se isso poderia ser melhorado.
- **Aproveitado:** duas trocas no `App.jsx`, regra de CSS e um teste novo.
- **Verificação:** Ao realizar a conferência no navegador foi constatado que a alteração foi realizada com sucesso.