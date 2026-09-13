# Desconfia

O **Desconfia** é uma aplicação web desenvolvida para a disciplina **Projeto Integrador IV**, com foco na aplicação de **Inteligência Artificial** e **Testes de Software**.

O projeto tem como objetivo auxiliar usuários na identificação de **indícios de golpes digitais em mensagens de texto**, como conteúdos recebidos por WhatsApp, SMS, e-mail ou redes sociais.

O sistema utiliza um modelo de linguagem por meio da **Groq API** para analisar o conteúdo enviado pelo usuário e apresentar uma avaliação de risco de forma simples e explicativa.

> O Desconfia funciona como uma ferramenta de apoio e prevenção. A análise realizada pelo sistema não representa uma confirmação definitiva de que determinada mensagem seja ou não fraudulenta.

---

## Funcionalidades

O MVP do Desconfia prevê as seguintes funcionalidades:

- Cadastro de usuários;
- Login e autenticação;
- Envio de mensagens textuais para análise;
- Análise utilizando Inteligência Artificial;
- Classificação do risco como **baixo, médio ou alto**;
- Identificação de possíveis sinais de engenharia social;
- Explicação dos fatores considerados na análise;
- Recomendações de segurança;
- Histórico de análises realizadas;
- Feedback do usuário sobre as análises;
- Testes automatizados;
- Avaliação específica do comportamento da IA;
- Deploy da aplicação em ambiente de nuvem.

---

## Como funciona

O usuário poderá inserir no sistema uma mensagem que considere suspeita.

Exemplos de situações que poderão ser analisadas:

- pedidos inesperados de Pix ou transferências;
- mensagens com senso de urgência;
- supostas notificações de bloqueio de contas;
- pedidos de senhas ou códigos de autenticação;
- promessas inesperadas de prêmios ou benefícios;
- tentativa de se passar por familiares, empresas ou instituições.

Após o envio, o backend encaminhará o conteúdo para o modelo de Inteligência Artificial.

O resultado deverá apresentar:

- nível de risco;
- sinais identificados;
- explicação da análise;
- recomendações preventivas.

Exemplo:

```text
Nível de risco: ALTO

Sinais identificados:
- senso de urgência;
- solicitação financeira;
- possível personificação.

Explicação:
A mensagem combina uma mudança inesperada de contato
com uma solicitação de pagamento urgente.

Recomendação:
Confirme a solicitação com a pessoa por outro canal
antes de realizar qualquer pagamento.
````

---

## Tecnologias

### Frontend

* React
* JavaScript
* Vite

### Backend

* Python
* FastAPI

### Banco de dados

* PostgreSQL
* SQLAlchemy

### Inteligência Artificial

* Groq API

### Testes

* Pytest
* Vitest

### Versionamento

* Git
* GitHub

### Deploy

Será utilizado um serviço de nuvem com camada gratuita, definido de acordo com a disponibilidade e os limites existentes durante a etapa de publicação do MVP.

---

## Arquitetura inicial

```text
                    Usuário
                       │
                       ▼
            React + JavaScript + Vite
                   Frontend
                       │
                       │ HTTP/HTTPS
                       ▼
                FastAPI + Python
                    Backend
                  /           \
                 /             \
                ▼               ▼
        PostgreSQL          Groq API
        + SQLAlchemy           IA
```

O **frontend** será responsável pela interface e interação com o usuário.

O **backend** será responsável pela autenticação, regras da aplicação, acesso ao banco de dados e comunicação com a Inteligência Artificial.

O **PostgreSQL** armazenará informações como usuários, histórico de análises e feedbacks.

A **Groq API** será utilizada para realizar a interpretação contextual das mensagens.

---

## Estrutura do projeto

```text
desconfia/
│
├── frontend/
│
├── backend/
│
├── ia-tests/
│   ├── dataset/
│   └── results/
│
├── docs/
│   ├── requirements/
│   └── system/
│
├── .gitignore
└── README.md
```

### `frontend/`

Contém a aplicação web desenvolvida utilizando React, JavaScript e Vite.

### `backend/`

Contém a API desenvolvida em FastAPI, incluindo autenticação, regras da aplicação, integração com PostgreSQL e comunicação com a Groq API.

### `ia-tests/`

Contém os arquivos relacionados à avaliação do comportamento da Inteligência Artificial.

* `dataset/`: casos utilizados para avaliar o modelo;
* `results/`: resultados das execuções e métricas obtidas.

### `docs/`

Contém a documentação técnica do projeto.

* `requirements/`: requisitos funcionais e não funcionais;
* `system/`: arquitetura, decisões técnicas e documentação do sistema.

---

## Testes e avaliação da IA

O projeto utilizará dois tipos principais de avaliação.

### Testes de software

Serão utilizados testes automatizados para verificar partes críticas da aplicação, como:

* cadastro;
* autenticação;
* validação de dados;
* endpoints da API;
* integração com o banco;
* tratamento de erros;
* interface do usuário.

### Avaliação da Inteligência Artificial

Será criado um conjunto de mensagens de teste contendo diferentes situações, como:

* mensagens legítimas;
* mensagens potencialmente fraudulentas;
* casos ambíguos;
* diferentes formas de escrita;
* tentativas de manipulação das instruções da IA.

Entre os aspectos avaliados estarão:

* classificações corretas;
* falsos positivos;
* falsos negativos;
* consistência;
* robustez;
* qualidade das explicações;
* respostas fora do formato esperado.

---

## Segurança e privacidade

O Desconfia será desenvolvido considerando princípios básicos de segurança e privacidade.

Entre os cuidados previstos estão:

* senhas armazenadas utilizando hash;
* chave da Groq API mantida apenas no backend;
* validação das entradas enviadas pelo usuário;
* controle de acesso ao histórico;
* minimização do armazenamento de dados pessoais;
* tratamento de mensagens potencialmente maliciosas;
* proteção contra tentativas de prompt injection;
* comunicação clara sobre as limitações da Inteligência Artificial.

---

## Desenvolvimento com Inteligência Artificial

Ferramentas de Inteligência Artificial poderão ser utilizadas como apoio durante o desenvolvimento do projeto.

Conforme orientação da disciplina, quando uma ferramenta de IA for utilizada em uma atividade de engenharia de software, o **prompt relevante utilizado deverá ser registrado no respectivo commit do Git**.

Exemplo:

```text
feat: adiciona validação do formulário de análise

IA utilizada: ChatGPT

Prompt:
"Implemente uma validação no formulário React para impedir
o envio de mensagens vazias."
```

Dessa forma, o histórico do Git também permitirá acompanhar a utilização de IA durante o desenvolvimento.

---

## Escopo do MVP

O MVP será concentrado na **análise de mensagens textuais**.

Não fazem parte do escopo inicial:

* análise de imagens;
* OCR;
* QR Codes;
* mensagens de áudio;
* vídeos;
* documentos;
* análise automática de sites;
* RAG.

Esses recursos poderão ser considerados como possíveis evoluções futuras.

---

## Equipe

Projeto desenvolvido por alunos da disciplina **Projeto Integrador IV**.

