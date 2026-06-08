# Descrições Expandidas de Casos de Uso

**Projeto:** Sistema de Denúncia Anônima  
**Disciplina:** Engenharia de Software (CC0116) — Prof. Adolfo Colares — UNIFAP 2026.1  
**Equipe:** Cauan Miranda · Eric Fernandes · Gabriel Lima · Johan Natividade · João Lucas Sena

---

## UC-01 — Registrar Denúncia Anônima

**Ator principal:** Cidadão  
**Pré-condição:** O cidadão acessa o sistema por navegador web; nenhuma autenticação é exigida.  
**Pós-condição:** A denúncia é armazenada no banco de dados com status RECEBIDA e um código de protocolo único é exibido ao cidadão.

### Fluxo Principal

| # | Ator | Ação |
|---|------|------|
| 1 | Cidadão | Acessa a página inicial e clica em "Fazer uma Denúncia" |
| 2 | Sistema | Exibe o formulário com campo de descrição e seleção de categoria |
| 3 | Cidadão | Seleciona a categoria (Corrupção, Assédio, Violência, Irregularidade ou Outros) |
| 4 | Cidadão | Preenche a descrição com pelo menos 10 caracteres |
| 5 | Cidadão | Clica em "Enviar denúncia" |
| 6 | Sistema | Valida os campos obrigatórios (categoria e descrição) |
| 7 | Sistema | Gera um código de protocolo único no formato `DEN-XXXXXXXX` |
| 8 | Sistema | Persiste a denúncia com status RECEBIDA e registra o histórico inicial |
| 9 | Sistema | Exibe o código de protocolo gerado em destaque na tela |

### Fluxo Alternativo A — Campos inválidos

| # | Ator | Ação |
|---|------|------|
| 6a | Sistema | Detecta que a descrição tem menos de 10 caracteres ou categoria não foi selecionada |
| 6b | Sistema | Exibe mensagem de erro indicando o campo inválido |
| 6c | Cidadão | Corrige os dados e retorna ao passo 5 |

### Fluxo Alternativo B — Cidadão desiste

| # | Ator | Ação |
|---|------|------|
| 4b | Cidadão | Fecha a aba ou navega para outra página sem enviar |
| — | Sistema | Nenhum dado é salvo; a sessão é encerrada sem registro |

**Regras de negócio aplicadas:** RN-01 (sem cadastro obrigatório), RN-02 (categoria e descrição são obrigatórias), RN-03 (protocolo único e gerado automaticamente)

---

## UC-02 — Consultar Status por Protocolo

**Ator principal:** Cidadão  
**Pré-condição:** O cidadão possui um código de protocolo gerado previamente pelo sistema.  
**Pós-condição:** O status atual da denúncia e o histórico de atualizações são exibidos ao cidadão.

### Fluxo Principal

| # | Ator | Ação |
|---|------|------|
| 1 | Cidadão | Acessa a página "Consultar Protocolo" |
| 2 | Sistema | Exibe campo para inserção do código de protocolo |
| 3 | Cidadão | Digita o código no formato `DEN-XXXXXXXX` e clica em "Consultar" |
| 4 | Sistema | Busca a denúncia pelo código informado |
| 5 | Sistema | Exibe as informações públicas: protocolo, categoria, data de registro e status atual |
| 6 | Sistema | Exibe o histórico de alterações de status com data e hora de cada transição |

### Fluxo Alternativo A — Protocolo não encontrado

| # | Ator | Ação |
|---|------|------|
| 4a | Sistema | Não encontra nenhuma denúncia com o código informado |
| 4b | Sistema | Exibe mensagem: "Protocolo não encontrado." |
| 4c | Cidadão | Verifica o código e pode tentar novamente |

### Fluxo Alternativo B — Código em formato incorreto

| # | Ator | Ação |
|---|------|------|
| 3a | Cidadão | Digita código sem o prefixo DEN- ou com caracteres inválidos |
| 3b | Sistema | Converte automaticamente para maiúsculas e tenta a busca |
| 3c | Sistema | Se não encontrar, retorna ao fluxo alternativo A |

**Regras de negócio aplicadas:** RN-01 (sem login exigido), RN-04 (comentários internos não são exibidos), RN-10 (histórico preservado e acessível)

---

## UC-03 — Atualizar Status de Denúncia

**Ator principal:** Administrador  
**Pré-condição:** O administrador está autenticado no sistema. A denúncia selecionada existe e possui um status que permite transição.  
**Pós-condição:** O novo status é salvo na denúncia, o histórico é atualizado com data/hora e identificação do administrador, e o cidadão passa a ver o novo status ao consultar o protocolo.

### Fluxo Principal

| # | Ator | Ação |
|---|------|------|
| 1 | Administrador | Acessa o painel de gerenciamento após login |
| 2 | Sistema | Lista todas as denúncias com protocolo, categoria, status e data |
| 3 | Administrador | Aplica filtros opcionais por status ou categoria |
| 4 | Administrador | Clica em "Ver detalhes" em uma denúncia |
| 5 | Sistema | Exibe detalhes completos: descrição, histórico e comentários internos |
| 6 | Administrador | Seleciona o novo status no campo "Atualizar status para..." |
| 7 | Administrador | Clica em "Salvar" |
| 8 | Sistema | Valida se a transição de status é permitida pelas regras de negócio |
| 9 | Sistema | Atualiza o status da denúncia no banco de dados |
| 10 | Sistema | Registra a transição no histórico com data/hora e ID do administrador |
| 11 | Sistema | Fecha o modal e recarrega a listagem atualizada |

### Fluxo Alternativo A — Transição de status inválida

| # | Ator | Ação |
|---|------|------|
| 8a | Sistema | Detecta que a transição solicitada não é permitida (ex: ENCERRADA → EM_ANALISE) |
| 8b | Sistema | Exibe mensagem de erro: "Transição inválida: [status anterior] → [novo status]" |
| 8c | Administrador | Seleciona outro status válido e retorna ao passo 7 |

### Fluxo Alternativo B — Administrador adiciona comentário antes de atualizar

| # | Ator | Ação |
|---|------|------|
| 5b | Administrador | Digita um comentário interno no campo correspondente |
| 5c | Administrador | Clica em "Adicionar" |
| 5d | Sistema | Salva o comentário vinculado à denúncia e ao administrador, com data/hora |
| 5e | Sistema | O comentário é exibido apenas no painel administrativo (nunca ao cidadão) |
| — | — | Fluxo retorna ao passo 6 |

**Regras de negócio aplicadas:** RN-05 (somente admins autenticados), RN-06 (histórico imutável), RN-07 (só o admin responsável gerencia), RN-08 (denúncia encerrada não reabre sem ação explícita), RN-10 (comentários internos nunca visíveis ao denunciante)
