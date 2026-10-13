# Registro de validação - 27/09/2026

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
