# User Stories e Critérios de Aceitação

## 1. Objetivo

Este documento registra histórias de usuário iniciais para orientar a implementação e validação do Sistema de Denúncia Anônima.

---

## 2. Histórias de Usuário

---

### US-01 - Registro de denúncia anônima

**Como** cidadão,
**quero** registrar uma denúncia sem me identificar,
**para** relatar uma irregularidade com segurança e sem risco de represálias.

**Critérios de aceitação:**

- O sistema deve permitir o envio de denúncias sem exigir cadastro ou login.
- O denunciante deve informar a categoria, descrição e, opcionalmente, anexar evidências.
- O sistema deve validar que a descrição foi preenchida antes de concluir o envio.
- Após o envio, o sistema deve exibir um código de protocolo único para acompanhamento futuro.

---

### US-02 - Escolha de categoria da denúncia

**Como** cidadão,
**quero** selecionar a categoria da minha denúncia,
**para** que ela seja encaminhada ao setor ou responsável correto.

**Critérios de aceitação:**

- O sistema deve exibir uma lista de categorias disponíveis (ex.: corrupção, assédio, violência, irregularidades administrativas).
- O denunciante deve selecionar ao menos uma categoria antes de concluir o registro.
- A categoria selecionada deve ser vinculada à denúncia e visível para o administrador.

---

### US-03 - Anexo de evidências

**Como** cidadão,
**quero** anexar arquivos à minha denúncia,
**para** fornecer evidências que reforcem o relato.

**Critérios de aceitação:**

- O sistema deve aceitar arquivos nos formatos imagem, documento e vídeo.
- O sistema deve informar claramente os formatos e tamanhos máximos aceitos.
- Os arquivos enviados devem ser armazenados de forma segura e vinculados à denúncia correspondente.
- O envio de anexos deve ser opcional.

---

### US-04 - Acompanhamento de denúncia por protocolo

**Como** cidadão que registrou uma denúncia,
**quero** consultar o status da minha denúncia usando o código de protocolo,
**para** saber se ela está sendo tratada, sem precisar me identificar.

**Critérios de aceitação:**

- O sistema deve permitir a consulta por código de protocolo sem exigir login.
- O sistema deve exibir o status atual da denúncia (ex.: recebida, em análise, encerrada).
- O sistema deve exibir mensagem adequada quando o código informado não for encontrado.

---

### US-05 - Cadastro de administrador

**Como** gestor institucional,
**quero** criar uma conta de administrador na plataforma,
**para** acessar e gerenciar as denúncias recebidas.

**Critérios de aceitação:**

- O administrador deve informar dados básicos para cadastro.
- O sistema deve validar campos obrigatórios e impedir cadastros com dados inválidos.
- Após cadastro válido, o administrador deve conseguir acessar o painel de gerenciamento.

---

### US-06 - Login de administrador

**Como** administrador cadastrado,
**quero** fazer login na plataforma,
**para** gerenciar as denúncias registradas.

**Critérios de aceitação:**

- O sistema deve autenticar o administrador com credenciais válidas.
- O sistema deve recusar credenciais inválidas com mensagem de erro apropriada.
- Após login, o administrador deve acessar apenas as funcionalidades de seu perfil.

---

### US-07 - Visualização de denúncias recebidas

**Como** administrador,
**quero** visualizar todas as denúncias registradas na plataforma,
**para** acompanhar e priorizar o tratamento de cada caso.

**Critérios de aceitação:**

- O sistema deve listar as denúncias recebidas com informações resumidas (categoria, data, status).
- O administrador deve conseguir acessar os detalhes completos de cada denúncia.
- A listagem deve permitir ordenação ou filtragem por status e categoria.

---

### US-08 - Atualização de status de denúncia

**Como** administrador,
**quero** atualizar o status de uma denúncia,
**para** refletir o andamento do tratamento do caso.

**Critérios de aceitação:**

- O administrador deve poder alterar o status da denúncia entre os estados disponíveis (ex.: recebida, em análise, encerrada).
- A alteração de status deve ser registrada com data e hora da atualização.
- O novo status deve ser refletido imediatamente na consulta pública por protocolo.

---

### US-09 - Adição de comentários internos

**Como** administrador,
**quero** adicionar comentários internos a uma denúncia,
**para** registrar observações e decisões tomadas durante a análise.

**Critérios de aceitação:**

- O administrador deve poder adicionar comentários visíveis apenas para outros administradores.
- Os comentários devem ser registrados com data, hora e identificação do administrador que os inseriu.
- Os comentários internos não devem ser exibidos na consulta pública por protocolo.

---

### US-10 - Encaminhamento de denúncia

**Como** administrador,
**quero** encaminhar uma denúncia para outro setor ou responsável,
**para** garantir que o caso seja tratado pela área competente.

**Critérios de aceitação:**

- O administrador deve selecionar o setor ou responsável de destino do encaminhamento.
- O sistema deve registrar o histórico de encaminhamentos realizados.
- O administrador de destino deve visualizar a denúncia encaminhada em seu painel.

---

## 3. Observações

As histórias descritas são uma base inicial. A equipe poderá incluir novas histórias, alterar prioridades e detalhar fluxos conforme a definição das tecnologias e regras de negócio.
