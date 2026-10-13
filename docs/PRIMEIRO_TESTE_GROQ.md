# Primeiro teste real da Groq — 12/10/2026

Integração testada diretamente pela função `app.ai.analyze`, com a chave local
carregada do ambiente. Nenhuma credencial foi incluída neste registro.

- Provedor: Groq.
- Modelo configurado: `openai/gpt-oss-20b`.
- Entrada sintética: “Oi mae, este e meu numero novo. Faca um Pix agora para a conta do meu amigo. Nao me ligue.”
- Resultado validado pelo back-end: risco alto (`high`).
- Sinais: solicitação financeira e urgência.
- Explicação recebida: “O texto contém um pedido imediato de transferência de dinheiro, indicando urgência e solicitação financeira, o que são sinais típicos de engenharia social.”
- Recomendação recebida: “Não realize a transferência. Confirme a identidade do remetente e a legitimidade da solicitação antes de agir.”

A primeira resposta veio em inglês. A instrução de idioma foi reforçada no prompt;
uma nova chamada retornou explicação, recomendação e descrições em português.
Ambas as chamadas passaram pela validação de formato e de citações do back-end.

Este teste confirma a conexão e um caso de análise real. Não substitui a avaliação
completa dos 15 casos, não mede acurácia e não verifica o fluxo web com PostgreSQL.
