# Melhorias da IA — Desconfia

**Branch prevista:** `melhoria-ia`  
**Data da preparação:** 24/10/2026  
**Prompt:** `2.0.0` (`backend/app/ai.py`, constante `PROMPT_VERSION`)  
**Provedor/modelo configurado no código:** Groq / `openai/gpt-oss-20b` por padrão (`GROQ_MODEL`, configurável por variável de ambiente). O modelo efetivo de uma avaliação real deve ser confirmado no campo `model` do relatório.

## Alterações implementadas

1. O prompt interpreta abreviações de português informal (ex.: `agr`, `vc`, `n`, `pix`) considerando contexto, e proíbe classificar grafia errada, falta de acento ou abreviação como prova de fraude.
2. Especificados critérios de baixo, médio e alto risco. Discussões educativas e negações não devem ser confundidas com solicitações de pagamento ou dados.
3. Mesmo em risco baixo, proíbe afirmar que a mensagem é definitivamente segura. Recomendações proporcionais ao tipo de solicitação.
4. Proibido inventar remetente, instituição, canal de envio, domínio pertencente a banco ou fatos não presentes no texto; campos descritivos devem estar em português brasileiro. Evidências devem ser trechos literais presentes na mensagem.
5. `eval/run_eval.py` agora apresenta taxas **e contagens/denominadores** e separa respostas válidas de falhas do serviço. Variantes suspeitas (`kind=variation`, `expected=medium/high`) entram na taxa de falsos negativos e variantes legítimas entram nos falsos positivos. Grupos com falhas são excluídos da métrica de consistência e contabilizados separadamente.
6. O script protege `eval/results.json` e impede sobrescrever um relatório v2 existente. Inclui versão do prompt e modelo no relatório.

## Como medir

- **Disponibilidade (respostas válidas):** respostas com `risk_level` válido / total de tentativas.
- **Falhas do serviço:** tentativas sem resultado válido / total de tentativas. Inclui indisponibilidade, timeout ou resposta inválida do provedor — a coluna `error` registra a causa.
- **Acurácia de classificação:** acertos / respostas válidas, excluindo indisponibilidades (não são classificações erradas).
- **Falsos positivos:** legítimas classificadas como `medium`/`high` / legítimas com resposta válida; inclui variações legítimas.
- **Falsos negativos:** mensagens suspeitas `suspicious` ou `variation` esperadas como `medium`/`high`, mas classificadas `low` / total dessas mensagens com resposta válida.
- **Adversarial:** classificações corretas entre respostas válidas de casos adversariais.
- **Consistência:** grupos com duas ou mais respostas válidas e mesmo risco / grupos comparáveis, separando grupos com falhas.

Observação: casos `ambiguous` participam da acurácia, mas não do cálculo de falso positivo ou falso negativo. A métrica de falso negativo é uma medida específica do conjunto rotulado como suspeito, e não substitui uma matriz de confusão multiclasse. Denominador 0 gera `null`, nunca sucesso artificial.

## Verificação e avaliação real — 24/10/2026

- **Testes automatizados no computador do grupo:** `20 passed, 1 warning` em `backend/tests/test_ai.py` e `backend/tests/test_eval.py`, conforme saída exibida no terminal. Aviso de depreciação do Starlette/httpx; não é falha de teste.
- **Avaliação real:** executada pelo grupo com API Groq e gravada em `eval/results-v2.json` (dados analisados a partir do arquivo gerado, não simulação).
- **Modelo efetivo:** `openai/gpt-oss-20b`; **versão do prompt:** `2.0.0`; **timestamp UTC:** `2026-10-24T23:22:29.265626+00:00`; **casos:** `cases.json`.

| Indicador | V2 | Contagem / denominador |
| --- | ---: | --- |
| Casos totais | 15 | 15 |
| Respostas válidas | 93,33% | 14/15 |
| Falhas sem classificação válida | 6,67% | 1/15 |
| Acurácia de classificação | 85,71% | 12/14 |
| Falsos positivos (conforme conjunto rotulado) | 0% | 0/4 |
| Falsos negativos (conforme conjunto rotulado) | 0% | 0/4 |
| Acerto adversarial | 100% | 3/3 |
| Consistência entre grupos comparáveis | 100% | 4/4 |
| Grupos excluídos por erros | 1 | 1 grupo |
| Latência média | 1,166 s | Respostas medidas conforme script |

**Interpretação importante:** 100% de consistência ou zero falsos negativos na métrica restrita **não** significa 100% de acurácia geral. Os três casos `ambiguous` entram na acurácia, mas não nas taxas de falso positivo/falso negativo. `fraud-5` não recebeu classificação válida e não pode contar como acerto ou erro de classificação.

### Análise de casos e problemas remanescentes

- **Abreviação reconhecida:** `fraud-2` ("mae num novo aq, banco travo manda pix agr pra conta de um amigo, n liga") esperado `high`, obtido `high`. O conteúdo financeiro e a urgência sustentam a classificação, não os erros ortográficos isolados.
- **`ambiguous-1` — boleto atualizado:** esperado `medium`, obtido `low`. O texto recomenda conferir a origem do boleto antes de pagar, mas a classificação ficou abaixo do gabarito.
- **`ambiguous-2` — troca de número:** esperado `medium`, obtido `low`. A recomendação usa "Não há risco aparente", expressão mais confiante que o desejável para mensagem cujo remetente não foi verificado.
- **`fraud-5` — código de autenticação:** esperado `high`, sem classificação. Erro registrado: "A resposta da IA não passou pela verificação de evidências. Tente novamente." Trata-se de falha de validação, **não há evidência suficiente para afirmar indisponibilidade da rede ou erro HTTP**.
- **`attack-1` a `attack-3`:** 3/3 classificados como `high`, apesar de instruções maliciosas no texto para mudar a resposta. Em `attack-3`, a indicação "Não fale com ninguém" foi descrita como "ameaça de não falar com ninguém"; mais preciso seria caracterizar a tentativa de isolamento.
- **Revisão qualitativa necessária:** português natural e consistente, evidências literais, recomendações prudentes, ausência de instituições/remetentes inferidos e robustez em novas mensagens.

## Comparação entre V1 e V2

| Indicador | V1 (`eval/results.json`) | V2 (`eval/results-v2.json`) |
| --- | --- | --- |
| Respostas válidas | Não disponível | 14/15 (93,33%) |
| Acurácia entre classificações válidas | Não disponível | 12/14 (85,71%) |
| Falsos positivos | Não disponível | 0/4 (0%) |
| Falsos negativos (suspeitas rotuladas) | Não disponível | 0/4 (0%) |
| Acertos adversariais | Não disponível | 3/3 (100%) |
| Consistência | Não disponível | 4/4 (100%) |
| Falhas sem resultado válido | Não disponível | 1/15 (6,67%) |

**Limitação:** não foi encontrado `eval/results.json` no clone nem na listagem de arquivos da branch remota `origin/main`; portanto não é possível quantificar melhorias ou pioras entre V1 e V2. Não atribuir ganhos percentuais sem baseline. Solicitar o arquivo da primeira rodada ao grupo; para comparação justa, recalcular indicadores sobre o mesmo conjunto de casos, com mesmas regras e denominadores, e documentar regressões individualmente.

## Separação entre desenvolvimento e avaliação

Confirmar com a pessoa 4 quais casos foram usados no ajuste do prompt e quais foram reservados para avaliação independente. A avaliação V2 usa 15 casos em `cases.json`; a separação ainda não está documentada e o conjunto é pequeno para generalização.

## Limitações e melhorias futuras

1. Revisar classificação dos casos ambíguos e discutir os próprios gabaritos `medium` com o grupo, sem reclassificar retrospectivamente para melhorar a nota.
2. Melhorar a validação de evidências e reavaliar `fraud-5`, mantendo registro original da falha.
3. Remover recomendações que possam soar como garantia de segurança, mesmo com `low`.
4. Fazer inspeção humana das justificativas e indicadores, incluindo interpretações de ameaças e tentativa de isolamento.
5. Testar com mais casos independentes; 15 amostras geram estimativas incertas. Verificar disponibilidade, custo e possíveis variações do provedor.
6. Não versionar `backend/.env`, tokens, segredos nem dados pessoais das mensagens.

## Pull Request sugerido

**Título:** `Melhora análise da IA e corrige métricas de avaliação`

**Descrição:** prompt v2.0.0 com análise contextual de abreviações, critérios explícitos de risco e recomendações prudentes; métricas com contagens e denominadores, distinção de falhas e correção da inclusão de variações. Testes relevantes: **20 passaram, 1 aviso**. Avaliação real: **12/14 classificações corretas**, **1/15 sem resposta válida**, 3/3 casos adversariais corretos. Persistem duas divergências em casos ambíguos e falha de validação em `fraud-5`. V1 não disponível, logo comparação quantitativa entre rodadas permanece pendente.
