# Documento de Requisitos de Software

## 1. Identificação

- **Projeto:** Sistema de Denúncia Anônima
- **Disciplina:** Engenharia de Software
- **Instituição:** Universidade Federal do Amapá (UNIFAP)
- **Semestre:** 2026.1
- **Versão do documento:** 0.2
- **Status:** atualizado com priorização e glossário

---

## 2. Objetivo

Este documento apresenta uma definição inicial dos requisitos do Sistema de Denúncia Anônima. A proposta é registrar uma base organizada para orientar o desenvolvimento, a comunicação entre os integrantes da equipe e as futuras validações do projeto.

---

## 3. Contexto

Cidadãos que testemunham ou sofrem irregularidades frequentemente deixam de denunciá-las por receio de exposição e represálias. O projeto propõe uma plataforma web que permita o registro anônimo e seguro de denúncias, com acompanhamento por código de protocolo, e que ofereça aos administradores ferramentas para gerenciar e encaminhar os casos recebidos de forma organizada.

---

## 4. Escopo Inicial

O sistema deverá oferecer recursos básicos para registro anônimo de denúncias, geração de protocolo, consulta de status por protocolo, cadastro e autenticação de administradores, e painel de gerenciamento de casos.

Nesta versão inicial, o documento não pretende descrever todos os fluxos, regras ou exceções do sistema. Esses pontos deverão ser refinados pela equipe ao longo do projeto.

---

## 5. Partes Interessadas

- **Cidadãos:** usuários que registram denúncias e acompanham seu andamento.
- **Administradores e gestores institucionais:** usuários que recebem, analisam e encaminham as denúncias.
- **Equipe do projeto:** responsáveis por análise, desenvolvimento, testes e documentação.
- **Professor da disciplina:** responsável por avaliação e acompanhamento acadêmico.

---

## 6. Requisitos Funcionais

- **RF-01:** o sistema deve permitir o registro de denúncias sem exigir identificação do usuário.
- **RF-02:** o sistema deve permitir a seleção de categoria ao registrar uma denúncia.
- **RF-03:** o sistema deve permitir o anexo de arquivos de evidência durante o registro da denúncia.
- **RF-04:** o sistema deve gerar um código de protocolo único ao concluir o registro de cada denúncia.
- **RF-05:** o sistema deve permitir a consulta do status de uma denúncia por meio do código de protocolo, sem necessidade de login.
- **RF-06:** o sistema deve permitir o cadastro de administradores.
- **RF-07:** o sistema deve permitir o login de administradores cadastrados.
- **RF-08:** o sistema deve permitir que administradores visualizem todas as denúncias recebidas.
- **RF-09:** o sistema deve permitir que administradores consultem os detalhes completos de uma denúncia.
- **RF-10:** o sistema deve permitir que administradores filtrem denúncias por categoria, status ou data.
- **RF-11:** o sistema deve permitir que administradores atualizem o status de uma denúncia.
- **RF-12:** o sistema deve permitir que administradores adicionem comentários internos a uma denúncia.
- **RF-13:** o sistema deve permitir que administradores encaminhem uma denúncia para outro setor ou responsável.
- **RF-14:** o sistema deve registrar o histórico de alterações de status e encaminhamentos de cada denúncia.

---

## 7. Requisitos Não Funcionais

Os requisitos não funcionais foram categorizados segundo o modelo **FURPS+** (Functionality, Usability, Reliability, Performance, Supportability, +constraints) e escritos de forma mensurável, evitando termos vagos como "rápido" ou "adequado".

| ID | Categoria FURPS+ | Descrição (mensurável) |
|----|-------------------|--------------------------|
| **RNF-01** | Usability | A interface deve ser responsiva e utilizável sem quebra de layout em resoluções de 360px (celular) a 1920px (desktop). |
| **RNF-02** | Usability | Um cidadão deve conseguir concluir o registro de uma denúncia em no máximo 3 telas/etapas a partir da página inicial, sem necessidade de treinamento prévio. |
| **RNF-03** | Functionality (Security) | O sistema não deve coletar, armazenar ou exibir nenhum dado pessoal identificável do denunciante (nome, e-mail, IP, telefone) em nenhuma tabela do banco ou tela pública — verificável por inspeção do schema em `models/database.py`. |
| **RNF-04** | Functionality (Security) | Senhas de administradores devem ser armazenadas apenas como hash (SHA-256 ou superior), nunca em texto puro; em ambiente de produção, toda comunicação deve usar HTTPS. |
| **RNF-05** | Functionality (Security) | Toda rota sob `/api/admin/*` deve exigir sessão autenticada válida; requisições sem sessão devem retornar HTTP 401 em 100% dos casos (coberto pelos testes IT-07). |
| **RNF-06** | Performance | O tempo de resposta das rotas de registro (`POST /api/denuncia/`) e consulta por protocolo (`GET /api/denuncia/protocolo/<cod>`) deve ser inferior a 2 segundos para 95% das requisições, em ambiente local com carga de até 50 requisições simultâneas. |
| **RNF-07** | Supportability (Maintainability) | O código-fonte deve manter separação em 4 camadas (controller, service, repository, model), com cobertura de testes automatizados de no mínimo 40% nas classes de regra de negócio — meta já superada (92% medido via pytest-cov). |
| **RNF-08** | Supportability | A documentação do projeto deve ser mantida na pasta `docs/` e versionada no mesmo repositório Git do código-fonte, nunca distribuída em arquivos separados. |
| **RNF-09** | Supportability (Extensibility) | A inclusão de uma nova categoria de denúncia ou um novo estado de status deve exigir alteração em no máximo 1 constante/enum do sistema (`CATEGORIAS_VALIDAS` ou `TRANSICOES_VALIDAS`), sem modificar a lógica das classes de serviço — princípio Open/Closed aplicado. |
| **RNF-10** | Reliability | O sistema não deve encerrar ou travar em caso de falha de acesso ao banco de dados; erros devem ser tratados e retornados como HTTP 500 com mensagem padronizada, preservando a sessão do usuário. |

---

## 8. Priorização dos Requisitos

Os requisitos foram classificados em três níveis: **MVP** (entrega mínima funcional), **Desejável** (agrega valor mas não bloqueia o MVP) e **Futuro** (fora do escopo atual, para versões posteriores).

### Requisitos Funcionais

| ID | Descrição resumida | Prioridade |
|----|--------------------|-----------|
| RF-01 | Registro anônimo de denúncias | **MVP** |
| RF-02 | Seleção de categoria | **MVP** |
| RF-04 | Geração de protocolo único | **MVP** |
| RF-05 | Consulta de status por protocolo | **MVP** |
| RF-07 | Login de administrador | **MVP** |
| RF-08 | Visualização de denúncias (admin) | **MVP** |
| RF-11 | Atualização de status (admin) | **MVP** |
| RF-14 | Histórico de alterações | **MVP** |
| RF-03 | Anexo de evidências | Desejável |
| RF-09 | Detalhes completos de denúncia | Desejável |
| RF-10 | Filtros por categoria, status ou data | Desejável |
| RF-12 | Comentários internos (admin) | Desejável |
| RF-06 | Cadastro de novos administradores | Desejável |
| RF-13 | Encaminhamento entre setores | Futuro |

### Requisitos Não Funcionais

| ID | Descrição resumida | Prioridade |
|----|--------------------|-----------|
| RNF-01 | Interface responsiva (360px–1920px) | **MVP** |
| RNF-03 | Nenhum dado pessoal identificável armazenado | **MVP** |
| RNF-05 | Autenticação obrigatória nas rotas `/api/admin/*` | **MVP** |
| RNF-02 | Registro concluído em até 3 telas | Desejável |
| RNF-04 | Senhas em hash + HTTPS em produção | Desejável |
| RNF-06 | Resposta < 2s para 95% das requisições | Desejável |
| RNF-07 | Cobertura de testes ≥ 40% nas classes de negócio | Desejável |
| RNF-08 | Documentação versionada em `docs/` | Desejável |
| RNF-09 | Novas categorias/status via 1 constante (OCP) | Futuro |
| RNF-10 | Falhas de banco tratadas sem travar o sistema | Futuro |

---

## 9. Regras de Negócio Iniciais

- **RN-01:** o registro de denúncias deve ser permitido sem cadastro ou autenticação do cidadão.
- **RN-02:** toda denúncia registrada deve conter ao menos uma categoria e uma descrição para ser concluída.
- **RN-03:** cada denúncia deve receber um código de protocolo único e não reutilizável gerado automaticamente pelo sistema.
- **RN-04:** comentários internos adicionados por administradores não devem ser visíveis na consulta pública por protocolo.
- **RN-05:** somente administradores autenticados devem poder visualizar o conteúdo completo das denúncias.
- **RN-06:** o histórico de status e encaminhamentos de cada denúncia deve ser preservado e não pode ser apagado definitivamente.
- **RN-07:** cada administrador deve gerenciar apenas as denúncias de sua competência ou as que lhe foram encaminhadas, salvo perfis com acesso amplo.
- **RN-08:** uma denúncia encerrada não deve ser reaberta sem ação explícita de um administrador autorizado.
- **RN-09:** arquivos anexados a uma denúncia devem ser armazenados de forma segura e acessíveis somente por administradores autorizados.
- **RN-10:** o sistema não deve exibir dados que possam identificar o denunciante em nenhuma tela acessível publicamente.

---

## 10. Glossário

| Termo | Definição |
|-------|-----------|
| **Denúncia** | Relato anônimo registrado por um cidadão descrevendo uma irregularidade, crime, ato de corrupção ou situação de risco. Cada denúncia recebe um código de protocolo único. |
| **Denunciante** | Cidadão que registra uma denúncia no sistema. Não é necessário se identificar ou criar conta. |
| **Protocolo** | Código alfanumérico único gerado automaticamente pelo sistema ao final de cada registro de denúncia, no formato `DEN-XXXXXXXX`. Serve como chave de rastreamento pública. |
| **Categoria** | Classificação temática da denúncia. As categorias disponíveis são: Corrupção, Assédio, Violência, Irregularidade Administrativa e Outros. |
| **Status** | Estado atual do tratamento de uma denúncia. Os estados possíveis são: `RECEBIDA` (registrada, aguardando análise), `EM_ANALISE` (em processo de investigação), `ENCAMINHADA` (enviada para outro setor) e `ENCERRADA` (caso concluído). |
| **Administrador** | Gestor institucional com acesso autenticado ao painel do sistema. Pode visualizar, atualizar e encaminhar denúncias, além de adicionar comentários internos. |
| **Comentário interno** | Nota adicionada por um administrador a uma denúncia para registro de observações e decisões. Nunca é visível ao denunciante na consulta pública. |
| **Histórico de status** | Registro cronológico de todas as alterações de status sofridas por uma denúncia, incluindo data, hora e administrador responsável. Não pode ser apagado. |
| **Evidência** | Arquivo (imagem, documento ou vídeo) anexado pelo denunciante como suporte à sua denúncia. Armazenado de forma segura e acessível apenas por administradores. |
| **Painel administrativo** | Interface restrita do sistema, acessível apenas por administradores autenticados, onde é possível gerenciar todas as denúncias recebidas. |
| **Anonimato** | Princípio central do sistema: nenhum dado pessoal do denunciante é coletado, armazenado ou exibido em qualquer tela pública do sistema. |

---

## 11. Organização Recomendada do Repositório

```
/
├── README.md
├── docs/
│   ├── requisitos-software.md
│   ├── documento-visao.md
│   ├── user-stories.md
│   ├── descricoes-casos-de-uso.md
│   ├── diagrama-casos-de-uso.png
│   ├── diagrama-classes.pdf
│   ├── diagrama-sequencia-1-registrar.pdf
│   ├── diagrama-sequencia-2-atualizar-status.pdf
│   ├── diagrama-atividades.pdf
│   └── justificativa-modelagem.md
├── src/
│   └── denuncia/
│       ├── app.py
│       ├── src/
│       │   ├── controllers/
│       │   ├── models/
│       │   ├── repositories/
│       │   └── services/
│       ├── static/
│       └── templates/
└── tests/
```

---

## 12. Critérios Básicos de Aceitação

- Cidadãos conseguem registrar uma denúncia sem se identificar.
- O sistema gera e exibe um código de protocolo ao final do registro.
- É possível consultar o status de uma denúncia informando apenas o código de protocolo.
- Administradores conseguem visualizar e gerenciar as denúncias pelo painel.
- O README aponta para a documentação de requisitos.
- A documentação mantém requisitos funcionais e não funcionais identificados por código.
- As histórias de usuário possuem critérios de aceitação básicos.

---

## 13. Pendências para Refinamento

- Detalhar os campos obrigatórios do registro de denúncia e do cadastro de administradores.
- Definir regras de permissão entre diferentes perfis de administrador.
- Definir responsabilidades da equipe por módulo.