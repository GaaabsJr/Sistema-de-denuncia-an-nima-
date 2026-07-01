# Documento de Requisitos de Software

## 1. Identificação

- **Projeto:** Sistema de Denúncia Anônima
- **Disciplina:** Engenharia de Software
- **Instituição:** Universidade Federal do Amapá (UNIFAP)
- **Semestre:** 2026.1
- **Versão do documento:** 0.1
- **Status:** versão inicial para discussão e complementação pela equipe

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

- **RNF-01:** a plataforma deve ser acessível por navegador web.
- **RNF-02:** a interface deve ser responsiva para computadores, tablets e celulares.
- **RNF-03:** o sistema deve garantir o anonimato do denunciante, não armazenando dados pessoais identificáveis sem consentimento explícito.
- **RNF-04:** o sistema deve utilizar criptografia no armazenamento e na transmissão de dados sensíveis.
- **RNF-05:** o sistema deve utilizar mecanismos de autenticação para controlar o acesso ao painel administrativo.
- **RNF-06:** as páginas de registro e consulta devem apresentar tempo de resposta adequado para uso em produção.
- **RNF-07:** o código-fonte deve ser organizado de forma clara, favorecendo manutenção e evolução.
- **RNF-08:** a documentação deve ser mantida em uma pasta própria do repositório.
- **RNF-09:** o sistema deve ser projetado para permitir inclusão futura de novos perfis, categorias, integrações e fluxos de notificação.
- **RNF-10:** a plataforma deve estar disponível para acesso na maior parte do tempo, garantindo que cidadãos e administradores possam utilizá-la sem interrupções frequentes.

---

## 8. Regras de Negócio Iniciais

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

## 9. Organização Recomendada do Repositório

```
/
├── README.md
├── docs/
│   ├── requisitos-software.md
│   ├── documento-visao.md
│   └── user-stories.md
├── src/
│   ├── frontend/
│   └── backend/
└── tests/
```

A estrutura acima é uma sugestão inicial e pode ser ajustada conforme as tecnologias escolhidas pela equipe.

---

## 10. Critérios Básicos de Aceitação

- Cidadãos conseguem registrar uma denúncia sem se identificar.
- O sistema gera e exibe um código de protocolo ao final do registro.
- É possível consultar o status de uma denúncia informando apenas o código de protocolo.
- Administradores conseguem visualizar e gerenciar as denúncias pelo painel.
- O README aponta para a documentação de requisitos.
- A documentação mantém requisitos funcionais e não funcionais identificados por código.
- As histórias de usuário possuem critérios de aceitação básicos.

---

## 11. Pendências para Refinamento

- Definir tecnologias de frontend, backend e banco de dados.
- Detalhar os campos obrigatórios do registro de denúncia e do cadastro de administradores.
- Definir os estados possíveis do ciclo de vida de uma denúncia.
- Definir regras de permissão entre diferentes perfis de administrador.
- Definir responsabilidades da equipe por módulo.
