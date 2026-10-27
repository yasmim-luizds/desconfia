# Registro de validação histórico - 27/09/2026

## Executado

| Verificação | Resultado |
|---|---|
| Pytest | 27 testes aprovados |
| Vitest | 8 testes aprovados |
| Build Vite | aprovado; bundle de produção gerado |
| Dataset de avaliação | 15 casos válidos, sem chamadas externas |
| Navegador local | cadastro, análise demo, resultado, feedback e histórico verificados |
| Responsividade | histórico e resultado inspecionados em viewport de 390 px; sem overflow horizontal detectado |
| Console do navegador | nenhum erro registrado durante o fluxo verificado |

Os testes do back-end usam um banco SQLite em memória separado do banco existente.
As chamadas à Groq são simuladas com httpx.MockTransport. O teste de navegador usa
mensagens sintéticas e banco isolado `tmp/preview.db`, em modo demonstração.

Cobertura funcional: login, cadastro duplicado/inválido, senha incorreta, preservação
de espaços na senha, hash, mensagem vazia/excessiva, isolamento entre usuários,
paginação, privacidade por padrão, opt-in de armazenamento, feedback único,
exclusão, limite de tentativas, falhas/timeouts/limites do provedor, JSON inválido,
evidências ausentes e separação de instruções e conteúdo não confiável.

Os testes passaram com avisos de depreciação do uso de datetime.utcnow no código
legado e da integração httpx/TestClient nas dependências atuais. Eles não impediram
a execução, mas devem ser tratados numa atualização futura de dependências.

## Não executado

- Chamada real à Groq: não há chave configurada.
- Avaliação de qualidade, viés, alucinação e resistência real a prompt injection:
  exige executar a eval real e a revisão qualitativa.
- Docker/PostgreSQL: ferramentas não disponíveis neste ambiente.
- Deploy em nuvem e execução do workflow no GitHub: dependem das contas e publicação.

Os arquivos de infraestrutura foram preparados, não são evidência de uma
implantação já realizada. Nenhum indicador de impacto social foi inventado.

## Atualização de estado — 27/10/2026

Este registro acima descreve somente a execução de 27/09/2026. Depois dela, foi
realizada uma rodada real V2 da avaliação em 24/10/2026, registrada em
`eval/results-v2.json`. A revisão individual e os testes funcionais foram entregues
na branch `testes-c2` e estão propostos no [PR #5](https://github.com/yasmim-luizds/desconfia/pull/5),
ainda não integrado nesta `base-c2`. A segunda revisão independente e o consenso
continuam pendentes. A amostra V2 contém 15 casos sintéticos e não comprova
qualidade geral do modelo.

O relatório funcional do PR #5 registra testes manuais locais em modo de demonstração
em 27/10/2026. O workflow de CI também teve execuções concluídas com sucesso na
branch `testes-c2`; detalhes e links estão em
`VALIDACAO_PUBLICACAO.md`. Esses resultados, por si só, não verificam Docker,
PostgreSQL nem publicação.

Em 27/10/2026, o Dockerfile foi construído e o PostgreSQL 17.11 ficou saudável.
Doze verificações da API passaram com dados sintéticos. A conta, a análise e o
feedback permaneceram após reiniciar o serviço web; a conta e a análise também
continuaram no volume após reiniciar o container PostgreSQL e o serviço web.
Como a rede bridge padrão foi bloqueada pelas restrições do sandbox, os fluxos foram
testados com um override temporário de rede host, sem alterar `compose.yaml`.

A rede bridge padrão precisa ser validada no computador do grupo. A hospedagem escolhida pelo grupo é local; portanto, não há URL pública planejada.
Os resultados locais e os detalhes da rede estão em `VALIDACAO_PUBLICACAO.md`.
