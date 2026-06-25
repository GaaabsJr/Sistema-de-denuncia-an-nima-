# Gestão do Processo de Desenvolvimento

**Projeto:** Sistema de Denúncia Anônima  
**Disciplina:** Engenharia de Software (CC0116) — Prof. Adolfo Colares — UNIFAP 2026.1  
**Equipe:** Cauan Miranda · Eric Fernandes · Gabriel Lima · Johan Natividade · João Lucas Sena  
**Versão:** 1.0

---

## 1. Metodologia Adotada — Kanban

A equipe adotou o **Kanban** como metodologia de gestão do processo de desenvolvimento.

### Por que Kanban?

O Kanban foi escolhido por três motivos principais:

- **Flexibilidade:** como o projeto é acadêmico com prazo fixo, o Kanban permitiu adaptar prioridades a cada semana sem a rigidez de sprints formais, respondendo rapidamente às orientações do professor ao longo da disciplina.
- **Visibilidade:** o quadro Kanban deixou claro para todos os membros o que estava sendo feito, o que estava parado e o que ainda faltava, evitando retrabalho e esquecimento de tarefas.
- **Tamanho da equipe:** com 5 integrantes trabalhando de forma assíncrona (em horários e locais diferentes), o Kanban se adaptou melhor do que Scrum, que exige cerimônias regulares difíceis de coordenar fora do horário de aula.

### Princípios aplicados

- Limite de trabalho em progresso (WIP): no máximo 2 tarefas por membro simultaneamente.
- Revisão coletiva antes de mover uma tarefa para "Concluído".
- Toda tarefa originada de um RF ou US foi rastreada com o código correspondente (ex: RF-01, US-03).

---

## 2. Quadro Kanban — Estado Final

| A fazer | Em progresso | Revisão | Concluído |
|---------|-------------|---------|-----------|
| — | — | — | README inicial |
| — | — | — | Documento de Visão |
| — | — | — | Requisitos de Software (RF, RNF, RN) |
| — | — | — | User Stories (US-01 a US-10) |
| — | — | — | Diagrama de Casos de Uso |
| — | — | — | Descrições expandidas de casos de uso |
| — | — | — | Diagrama de Classes |
| — | — | — | Tradução de classes para código Python |
| — | — | — | Justificativa de modelagem |
| — | — | — | Diagramas de Sequência (2) |
| — | — | — | Diagrama de Atividades |
| — | — | — | Documento de Arquitetura |
| — | — | — | Backend Flask (controllers, services, repositories) |
| — | — | — | Frontend HTML/CSS/JS |
| — | — | — | Banco SQLite + modelos |
| — | — | — | Testes unitários (20 casos) |
| — | — | — | Testes de integração (10 casos) |
| — | — | — | Plano de testes |
| — | — | — | Gestão do processo (este documento) |

---

## 3. Product Backlog

Lista priorizada de todas as funcionalidades, derivadas das User Stories, com status de implementação.

| ID | User Story | Prioridade | Status |
|----|-----------|-----------|--------|
| US-01 | Registrar denúncia anônima | MVP | ✅ Concluído |
| US-02 | Selecionar categoria da denúncia | MVP | ✅ Concluído |
| US-04 | Acompanhar denúncia por protocolo | MVP | ✅ Concluído |
| US-05 | Cadastro de administrador | MVP | ✅ Concluído |
| US-06 | Login de administrador | MVP | ✅ Concluído |
| US-07 | Visualização de denúncias recebidas | MVP | ✅ Concluído |
| US-08 | Atualização de status de denúncia | MVP | ✅ Concluído |
| US-03 | Anexo de evidências | Desejável | 🔜 Backlog |
| US-09 | Adição de comentários internos | Desejável | ✅ Concluído |
| US-10 | Encaminhamento de denúncia | Futuro | 🔜 Backlog |

---

## 4. Divisão de Responsabilidades

| Membro | Responsabilidades no projeto |
|--------|------------------------------|
| Cauan Antônio | Documento de Visão · Documento de Requisitos · Gestão do repositório Git |
| Eric Felipe | Diagramas UML (Casos de Uso e Atividades) · Descrições expandidas |
| Gabriel Alves | Backend Flask (controllers e services) · Testes de integração |
| Johan Mateus | Diagrama de Classes · Documento de Arquitetura · Testes unitários |
| João Lucas | Frontend HTML/CSS/JS · Banco de dados SQLite · Plano de testes |

---

## 5. Histórico de Entregas

| Semana | Entregável | Responsável |
|--------|-----------|-------------|
| 1 | README inicial, estrutura do repositório | Toda a equipe |
| 2 | Documento de Visão, Requisitos de Software | Cauan, Eric |
| 3 | User Stories, Diagrama de Casos de Uso | Eric, Gabriel |
| 4 | Diagrama de Classes, tradução para código | Johan, João Lucas |
| 5 | Diagramas de Sequência e Atividades | Eric, Johan |
| 6 | Backend Flask completo, banco SQLite | Gabriel, João Lucas |
| 7 | Frontend, testes, arquitetura, processo | Toda a equipe |

---

## 6. Lições Aprendidas

### O que deu certo

Separar o código em camadas (Controller → Service → Repository) desde o início foi a melhor decisão técnica do projeto. Quando precisamos escrever os testes, a separação já estava feita e os testes unitários rodaram sem precisar de grandes refatorações. A documentação feita antes do código também ajudou — as User Stories e o Diagrama de Classes serviram como guia durante o desenvolvimento e evitaram dúvidas sobre o que implementar.

### O que deu errado

A equipe demorou para começar a fazer commits regulares no repositório. Nos primeiros dias, o trabalho era feito localmente e só commitado de vez em quando, o que dificultou o rastreamento do progresso. Outro ponto foi a dificuldade inicial com o ambiente no Mac — o Python não estava no PATH padrão e o sistema acessível por `localhost` mas não por `127.0.0.1` causou confusão antes de identificar a causa (extensão do navegador sobrescrevendo o CSS).

### O que faríamos diferente

Crearíamos o quadro Kanban no GitHub Projects desde o primeiro dia, em vez de gerenciar as tarefas informalmente por mensagens. Também definiríamos uma convenção de commits desde o início (como Conventional Commits: `feat:`, `docs:`, `test:`) para que o histórico do repositório ficasse mais organizado e profissional. Por fim, escreveríamos pelo menos um teste simples antes de cada funcionalidade nova — a prática de TDD que o professor mencionou faz sentido e facilitaria detectar erros mais cedo.

### Aprendizados técnicos

- Flask com Blueprints permite organizar rotas por domínio de forma limpa e escalável.
- SQLite é suficiente para projetos acadêmicos e não exige configuração de servidor.
- Pytest com fixtures de banco em memória garante testes rápidos e isolados.
- O padrão Repository facilita muito a escrita de testes — basta trocar o banco real pelo banco de teste.
- Documentar antes de codificar não é perda de tempo; é o que evita retrabalho.