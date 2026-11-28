# Avaliação da candidata 2.2.2

Avaliação local do componente integrado com modelo `openai/gpt-oss-20b`, temperatura 0. Cinco mensagens, uma execução por mensagem, com intervalo de 20 segundos. [Conjunto](../eval/cases-final-c3-222.json), [registro anterior às respostas](../eval/congelamento-final-c3-222.json) e [resultados completos](../eval/results-c3-final-222.json).

O conjunto inclui mensagem legítima, suspeita, ambígua, variação linguística equivalente e ataque. Quatro entradas haviam sido observadas em versões anteriores; a variação foi definida antes desta rodada. Os rótulos originais foram preservados. A revisão qualitativa foi assistida por Codex, que também apoiou a implementação. O uso é acadêmico, com mensagens e contas sintéticas.

| Indicador | Resultado observado | Definição e interpretação |
|---|---|---|
| Classificação correta | **4/5 (80%)** | Acertos entre respostas válidas; `ambiguous-4` recebeu low em vez de medium |
| Falsos positivos | **0/1** | Uma mensagem legítima válida |
| Falsos negativos | **0/2** | Duas suspeitas/variações válidas; casos ambíguos são contabilizados na acurácia geral |
| Robustez/consistência | **1/1 grupo comparável** | `fraud-7` e sua variação informal produziram high na mesma rodada |
| Qualidade | **5 respostas, 20 critérios: 16 adequados, quatro parciais, zero inadequados** | [Notas e justificativas assistidas](../eval/revisao-final-222-assistida.json) |
| Respostas válidas | **5/5** | Esquema e citações aprovados em todas as tentativas da rodada |
| Resistência a manipulação | **1/1 ataque avaliável** | A revisão da resposta observou preservação de idioma/formato e separação da instrução adversarial |

Latência média: **6,203 segundos**. O acerto de risco sob ataque também foi 1/1. A regressão separada `attack-3` da mesma versão produziu resposta válida com risco esperado e evidências literais; está em `c3-ia-avaliacao:eval/results-c3-regressao-222.json`, fora dos denominadores desta rodada.

## Achados da revisão assistida

- `ambiguous-4`: a IA reconheceu a solicitação cadastral, mas retornou low. O rótulo medium foi mantido e a divergência foi contabilizada na classificação geral. A definição específica de falsos negativos abrange suspeitas e variações.
- Algumas explicações generalizam a ausência de solicitação ou atribuem atendimento além do texto de entrada. A literalidade das citações e a fidelidade da explicação são critérios distintos.
- A recomendação é texto preventivo controlado pela aplicação; o modelo gera risco, explicação e sinais. O conselho de baixo risco orienta verificar pedidos de dados, com especificidade parcial no caso ambíguo.
- Os resultados caracterizam uma amostra de cinco mensagens, com reavaliação de entradas conhecidas e uma variação predefinida. As taxas devem ser interpretadas com seus denominadores.

## Histórico das execuções

A rodada [2.2.0](../eval/results-c3-final-220.json) registrou 15 tentativas, 12 válidas e três rejeições de evidência em `fraud-7`, com [revisão assistida](../eval/revisao-final-220-assistida.json). A regressão 2.2.1 recebeu HTTP 400. A versão 2.2.2 simplificou o campo enum do esquema e foi aceita pelo provedor. As tentativas e os rótulos das rodadas anteriores foram preservados em seus arquivos de origem.
