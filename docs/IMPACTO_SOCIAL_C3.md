# Impacto social e limitações — Desconfia C3

**Data:** 28/11/2026  
**Responsabilidade:** Frente 5 — Documentação técnica, rastreabilidade, impacto e apresentação  
**Projeto:** Projeto Integrador IV — Desconfia

## 1. Contextualização do problema

Os golpes digitais podem utilizar mensagens que simulam comunicações de bancos, empresas, serviços de entrega ou pessoas conhecidas. Essas mensagens frequentemente exploram urgência, ameaças, promessas de benefícios e solicitações de dinheiro ou informações sensíveis.

Reconhecer esses indícios pode ser difícil, especialmente quando a mensagem apresenta uma situação aparentemente comum ou utiliza linguagem informal.

O Desconfia foi desenvolvido como ferramenta acadêmica de apoio à identificação de sinais de possíveis golpes em mensagens de texto.

## 2. Objetivo social

O objetivo social do Desconfia é contribuir para a conscientização sobre golpes digitais e apoiar decisões mais cuidadosas diante de mensagens potencialmente fraudulentas.

A aplicação permite que uma pessoa insira uma mensagem e receba uma classificação de risco, sinais identificados, explicação e recomendações preventivas.

O sistema não determina se uma mensagem é comprovadamente fraudulenta. Sua finalidade é oferecer informações adicionais para apoiar a avaliação humana.

## 3. Público-alvo

O público inicialmente considerado pelo projeto inclui estudantes universitários e familiares adultos que utilizam aplicativos de mensagens, redes sociais, SMS e outros canais digitais.

A proposta considera pessoas com diferentes níveis de familiaridade com segurança digital, buscando apresentar explicações compreensíveis e recomendações práticas.

Esse público representa o grupo de interesse definido para o projeto, não uma amostra de participantes efetivamente pesquisados.

## 4. Contribuições sociais esperadas

O Desconfia apresenta potencial para:

- Incentivar a identificação de pedidos financeiros urgentes e situações suspeitas.
- Alertar sobre solicitações de senhas, códigos de autenticação e dados pessoais.
- Orientar a confirmação da identidade de remetentes por canais conhecidos ou oficiais.
- Contribuir para o aprendizado sobre padrões de engenharia social.
- Apoiar a reflexão antes de clicar em links, compartilhar informações ou transferir dinheiro.

Essas contribuições representam objetivos e benefícios esperados. Até o momento, a documentação disponível não comprova redução efetiva de golpes ou mudança de comportamento dos usuários.

## 5. Funcionalidades relacionadas ao impacto

O sistema oferece cadastro e autenticação, análise de mensagens textuais, classificação de risco baixo, médio ou alto, identificação de sinais, explicação do resultado e recomendações preventivas.

Também disponibiliza histórico individual de análises, envio de feedback e exclusão de registros.

A aplicação possui modo demonstração e integração com IA pela Groq API. Conforme comunicado da equipe, a versão integrada está publicada em https://desconfia.onrender.com/, com hospedagem no Render e PostgreSQL no Neon.

## 6. Evidências técnicas disponíveis

A validação da candidata C3 2.2.2 registrou 70 testes aprovados de backend, 29 de frontend e um teste PostgreSQL em ambiente local descartável.

A avaliação da IA 2.2.2 apresentou cinco respostas válidas em cinco mensagens sintéticas, sendo quatro classificações correspondentes aos riscos esperados (80%).

A revisão qualitativa documentada foi assistida por Codex e identificou 16 critérios adequados e quatro parciais.

Esses resultados contribuem para verificar funcionalidades e identificar limitações técnicas. Entretanto, não demonstram, isoladamente, impacto social ou eficácia em situações reais.

## 7. Limitações e cuidados

- A IA pode produzir classificações incorretas ou explicações incompletas.
- Risco baixo não garante que uma mensagem seja autêntica ou segura.
- A análise considera o texto fornecido, sem verificar automaticamente a identidade do remetente.
- A ferramenta não analisa diretamente áudios, imagens, vídeos ou o conteúdo de páginas externas.
- Os resultados da avaliação da IA são provenientes de uma amostra pequena de mensagens sintéticas.
- As verificações técnicas não substituem estudos de usabilidade e impacto com participantes reais.
- O uso de mensagens com informações pessoais exige cuidados de privacidade.
- As demonstrações desta entrega utilizam contas e mensagens sintéticas, conforme os [cuidados de IA responsável](REQUISITOS.md#ia-responsável).

## 8. Possibilidades de avaliação futura

Uma avaliação futura do impacto social poderia envolver participantes voluntários, com consentimento e proteção de dados, para observar a compreensão das explicações e das recomendações.

Poderiam ser investigados aspectos como facilidade de utilização, clareza das orientações, identificação de sinais de fraude e diferenças na percepção de risco antes e depois da utilização.

Esse tipo de pesquisa precisaria de planejamento metodológico, critérios de avaliação e registro adequado dos resultados.

Nenhuma pesquisa com participantes reais é declarada como realizada neste documento.

## 9. Considerações finais

O Desconfia representa uma proposta acadêmica de utilização de inteligência artificial e testes de software para apoiar a conscientização sobre golpes digitais.

A documentação da C3 demonstra a existência de funcionalidades implementadas, avaliações técnicas e uma versão publicada, conforme os registros disponíveis.

O impacto social permanece como potencial a ser investigado. O uso responsável da ferramenta exige reconhecer suas limitações e reforçar que decisões envolvendo dinheiro, credenciais ou informações pessoais devem ser confirmadas por canais confiáveis.

## 10. Referências internas

- `README.md`
- `docs/REQUISITOS.md`
- `docs/MATRIZ_RASTREABILIDADE_C3.md`
- `docs/TESTES_C3.md`
- `docs/AVALIACAO_FINAL_C3.md`
- `docs/VALIDACAO_PUBLICACAO.md`

Este documento descreve o impacto social esperado do projeto e não apresenta resultados de pesquisa de campo ou comprovação de eficácia social.