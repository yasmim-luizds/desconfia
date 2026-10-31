# Desconfia

**Antes de clicar, desconfia.**

O Desconfia é uma aplicação web de apoio à identificação de indícios de golpes digitais em mensagens de texto. Desenvolvido no Projeto Integrador IV, o projeto combina Inteligência Artificial, cibersegurança e testes de software para ajudar pessoas a reconhecer sinais de engenharia social e tomar decisões mais informadas.

A pessoa insere uma mensagem recebida por aplicativos de mensagens, SMS, e-mail ou redes sociais. A aplicação analisa o texto e apresenta um nível de risco, os sinais identificados, uma explicação e recomendações preventivas.

> O resultado é uma avaliação de risco, não uma confirmação de fraude. A IA pode errar: risco baixo não garante que uma mensagem seja segura. Confirme solicitações por um canal oficial ou contato previamente conhecido.

## Objetivo e público

Mensagens fraudulentas podem imitar empresas ou pessoas conhecidas, criar urgência, ameaçar o bloqueio de uma conta ou solicitar dinheiro e informações sensíveis. Esses elementos nem sempre são fáceis de reconhecer isoladamente.

O projeto busca oferecer uma segunda análise, com linguagem compreensível, e contribuir para a conscientização sobre os padrões utilizados em golpes digitais. O público considerado inicialmente é formado por estudantes universitários e familiares adultos que utilizam serviços e canais digitais no cotidiano, com diferentes níveis de familiaridade com segurança digital.

A ferramenta apoia a avaliação humana e não substitui os canais oficiais das instituições nem mecanismos especializados de segurança. Seu potencial de apoio à comunidade é um objetivo do projeto; resultados técnicos, por si só, não comprovam redução de golpes ou mudança de comportamento.

## Funcionalidades

- Cadastro, login e logout.
- Análise de mensagens textuais de até 2.000 caracteres.
- Classificação em risco baixo, médio ou alto.
- Apresentação dos sinais identificados e dos trechos que sustentam a análise.
- Explicação do resultado e recomendações preventivas.
- Histórico individual, consulta e exclusão de análises.
- Feedback sobre a utilidade dos resultados.
- Modo de demonstração com regras locais e modo de análise com IA pela Groq API.

O escopo é a análise do texto inserido pelo usuário. A aplicação não lê automaticamente conversas, imagens, capturas de tela, QR Codes, áudios, vídeos ou o conteúdo de páginas externas.

## Como funciona

1. O usuário acessa sua conta e insere uma mensagem para análise.
2. A interface envia a solicitação ao backend.
3. No modo com IA, o backend consulta um modelo de linguagem pela Groq API.
4. O backend valida o formato da resposta e os trechos apresentados como evidência.
5. A interface exibe o resultado, que pode ser consultado no histórico e receber feedback.

O conteúdo da mensagem é tratado como dado para análise. As instruções do modelo e os casos de avaliação consideram tentativas de manipulação por *prompt injection*, sem pressupor proteção absoluta contra esse tipo de ataque.

## Tecnologias

| Componente | Tecnologias |
|---|---|
| Interface | React, JavaScript e Vite |
| Backend | Python e FastAPI |
| Persistência | SQLAlchemy, PostgreSQL e SQLite para execução local |
| Inteligência Artificial | Modelo de linguagem acessado pela Groq API |
| Testes automatizados | Pytest e Vitest |
| Automação e empacotamento | GitHub Actions, Docker e Docker Compose |

Sem a configuração de `DATABASE_URL`, a aplicação utiliza SQLite local. O PostgreSQL é a opção prevista para implantação e também pode ser executado com Docker Compose.

## Executar localmente

Prepare Python 3.12 ou superior, Node.js 22 e pnpm 11.25.0. Os scripts de inicialização instalam as dependências, compilam a interface e iniciam o servidor; a primeira execução precisa de internet.

### Modo demonstração

No Windows, abra `iniciar_demo.bat` na raiz do projeto.

No macOS ou Linux, execute na raiz:

```bash
AI_MODE=demo bash iniciar_local.sh
```

Abra [http://127.0.0.1:8000](http://127.0.0.1:8000) e crie uma conta pela interface. Mantenha o terminal aberto enquanto utiliza o sistema; `Ctrl+C` encerra o servidor.

O modo demonstração usa regras locais, não consulta a Groq e não representa a qualidade de um modelo de IA.

### Análise com IA

1. Se ainda não existir, crie `backend/.env` copiando `backend/.env.example`.
2. Configure `GROQ_API_KEY`, `AI_MODE=groq` e um segredo local em `DESCONFIA_SECRET_KEY`.
3. Para gerar o segredo, execute `python -c "import secrets; print(secrets.token_urlsafe(48))"` e copie o resultado para a configuração local.
4. No Windows, abra `iniciar_local.bat`. No macOS ou Linux, execute `AI_MODE=groq bash iniciar_local.sh`.
5. Acesse [http://127.0.0.1:8000](http://127.0.0.1:8000).

A análise real depende de conexão com a internet, chave válida e disponibilidade do serviço. A chave deve permanecer no backend: não publique arquivos `.env`, credenciais ou capturas que as exponham.

As orientações de infraestrutura, Docker e implantação estão no [guia de publicação](docs/PUBLICACAO.md). Com o servidor em execução, a documentação interativa da API está em [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Testes e avaliação da IA

O desenvolvimento segue uma abordagem incremental: as funcionalidades são implementadas, testadas e aprimoradas progressivamente.

Os testes automatizados verificam comportamentos da API e da interface, como autenticação, validação de entradas, controle de acesso, análises e tratamento de erros. A avaliação da IA é feita separadamente com mensagens sintéticas legítimas, suspeitas, ambíguas, variações linguísticas e casos adversariais.

São observados a correspondência com as classificações esperadas, falsos positivos e negativos, validade das respostas, consistência e comportamento diante de tentativas de manipulação. A revisão qualitativa verifica a fidelidade das explicações ao texto e a coerência das recomendações.

Os procedimentos, critérios e resultados ficam em [eval/](eval/) e nos relatórios em [docs/](docs/). Consulte o [guia de avaliação](eval/README.md) antes de executar chamadas reais. Resultados de amostras controladas não representam uma garantia de precisão em situações reais.

## Privacidade

O projeto adota a minimização dos dados armazenados. Por padrão, o texto original não é guardado; o usuário pode optar por salvá-lo no histórico. Ainda assim, explicações, evidências e comentários podem reproduzir informações presentes na mensagem.

No modo com IA, o texto é enviado à Groq para processamento. Para testes e demonstrações, utilize mensagens inventadas, sem senhas, códigos de autenticação, dados bancários ou outras informações pessoais.

A exclusão de uma análise não equivale à exclusão completa da conta. As condições de retenção e os procedimentos de privacidade devem ser definidos para o ambiente de implantação.

## Organização do repositório

| Caminho | Conteúdo |
|---|---|
| `frontend/` | Interface, estilos e testes do frontend |
| `backend/app/` | API, autenticação, integração com IA e persistência |
| `backend/tests/` | Testes automatizados do backend |
| `eval/` | Casos sintéticos, programa de avaliação e resultados |
| `docs/` | Requisitos, arquitetura, revisões e orientações técnicas |
| `.github/workflows/` | Automação de verificações do projeto |
| `compose.yaml` | Configuração da aplicação e do PostgreSQL com Docker |
| `Dockerfile` | Construção da imagem da aplicação |

## Documentação

- [Requisitos](docs/REQUISITOS.md)
- [Arquitetura](docs/ARQUITETURA.md)
- [Testes funcionais](docs/TESTES_FUNCIONAIS.md)
- [Avaliação da IA](eval/README.md)
- [Publicação e configuração de ambientes](docs/PUBLICACAO.md)
- [Registro dos prompts de desenvolvimento](docs/PROMPTS.md)

## Equipe

Projeto desenvolvido no âmbito da disciplina Projeto Integrador IV por:

- Gustavo Rissoli Vicente
- Hellen Karla Costa Campos Moraes de Melo
- José Henrique Bessi Wolkers
- Kaio Soares Pacheco
- Yasmim Luiz dos Santos
