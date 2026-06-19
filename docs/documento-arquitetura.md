# Documento de Arquitetura de Software

**Projeto:** Sistema de Denúncia Anônima  
**Disciplina:** Engenharia de Software (CC0116) — Prof. Adolfo Colares — UNIFAP 2026.1  
**Equipe:** Cauan Miranda · Eric Fernandes · Gabriel Lima · Johan Natividade · João Lucas Sena  
**Versão:** 1.0

---

## 1. Visão Geral

Este documento descreve as decisões arquiteturais do Sistema de Denúncia Anônima: o padrão adotado, a organização em camadas, as tecnologias escolhidas e os princípios de design aplicados no código.

---

## 2. Tecnologias Utilizadas (Tech Stack)

| Camada | Tecnologia | Justificativa |
|--------|------------|---------------|
| **Backend** | Python 3.12 + Flask 3.0 | Linguagem adotada pela equipe na disciplina; Flask é minimalista e permite estruturar o projeto em camadas sem impor convenções rígidas, facilitando o aprendizado e a manutenção |
| **Banco de dados** | SQLite | Não requer instalação de servidor separado, ideal para o contexto acadêmico; banco de dados embutido em arquivo único (`denuncia.db`), fácil de versionar e distribuir |
| **Frontend** | HTML5 + CSS3 + JavaScript puro | Sem dependência de frameworks externos; permite que todos os membros contribuam sem necessidade de configuração de ambiente complexo |
| **Persistência** | sqlite3 (biblioteca padrão do Python) | Integração nativa, sem ORM, tornando as queries SQL visíveis e auditáveis — importante para fins de aprendizado |
| **Autenticação** | Sessões Flask + SHA-256 | Mecanismo simples e seguro para o escopo do projeto; senhas armazenadas como hash, nunca em texto puro |

---

## 3. Padrão Arquitetural — MVC em Camadas

O sistema adota o padrão **MVC (Model-View-Controller)** combinado com uma **arquitetura em camadas**, separando claramente as responsabilidades de cada parte do código.

### 3.1 Camadas do sistema

```
┌─────────────────────────────────────────┐
│           APRESENTAÇÃO (View)           │
│   templates/index.html                  │
│   static/css/style.css                  │
│   static/js/app.js                      │
│   Interface web — HTML, CSS, JavaScript │
└────────────────────┬────────────────────┘
                     │ HTTP (JSON)
┌────────────────────▼────────────────────┐
│          CONTROLE (Controller)          │
│   src/controllers/denuncia_controller   │
│   src/controllers/admin_controller      │
│   Rotas Flask, validação de sessão      │
└────────────────────┬────────────────────┘
                     │ chamadas de método
┌────────────────────▼────────────────────┐
│            SERVIÇO (Service)            │
│   src/services/denuncia_service         │
│   src/services/auth_service             │
│   Regras de negócio, validações         │
└────────────────────┬────────────────────┘
                     │ chamadas de método
┌────────────────────▼────────────────────┐
│         REPOSITÓRIO (Repository)        │
│   src/repositories/denuncia_repository  │
│   src/repositories/admin_repository     │
│   Acesso ao banco de dados (SQL)        │
└────────────────────┬────────────────────┘
                     │ SQL
┌────────────────────▼────────────────────┐
│           DADOS (Model/DB)              │
│   src/models/database.py                │
│   denuncia.db (SQLite)                  │
│   Tabelas: denuncia, evidencia,         │
│   historico_status, comentario_interno, │
│   administrador                         │
└─────────────────────────────────────────┘
```

### 3.2 Responsabilidade de cada camada

| Camada | Responsabilidade | Arquivos |
|--------|-----------------|----------|
| **View** | Renderizar a interface e consumir a API via fetch | `templates/index.html`, `static/` |
| **Controller** | Receber requisições HTTP, verificar autenticação, retornar JSON | `controllers/denuncia_controller.py`, `controllers/admin_controller.py` |
| **Service** | Aplicar regras de negócio, validar dados, orquestrar operações | `services/denuncia_service.py`, `services/auth_service.py` |
| **Repository** | Executar queries SQL, isolar o código de acesso ao banco | `repositories/denuncia_repository.py`, `repositories/admin_repository.py` |
| **Model/DB** | Definir esquema do banco, criar tabelas, fornecer conexão | `models/database.py` |

### 3.3 Fluxo de uma requisição

```
Cidadão (navegador)
    │ POST /api/denuncia/ {descricao, categoria}
    ▼
DenunciaController.registrar()
    │ valida sessão / extrai dados do JSON
    ▼
DenunciaService.registrar(descricao, categoria)
    │ valida campos, gera protocolo, monta objeto
    ▼
DenunciaRepository.criar(...)
    │ INSERT INTO denuncia ...
    ▼
SQLite (denuncia.db)
    │ retorna denuncia_id
    ▼
HistoricoRepository.registrar(...)
    │ INSERT INTO historico_status ...
    ▼
DenunciaService → DenunciaController
    │ retorna {protocolo: "DEN-XXXXXXXX"}
    ▼
Cidadão recebe 201 Created + código de protocolo
```

---

## 4. Design Patterns Aplicados

### 4.1 Repository Pattern

**O que é:** separa a lógica de acesso ao banco de dados do restante da aplicação, criando uma classe dedicada para cada entidade que centraliza todas as operações de persistência.

**Onde está no código:** arquivos `src/repositories/denuncia_repository.py` e `src/repositories/admin_repository.py`.

**Exemplo concreto:**

```python
# Em vez de espalhar SQL pelo código de negócio:
# ❌ Forma sem o padrão:
conn = sqlite3.connect("denuncia.db")
conn.execute("SELECT * FROM denuncia WHERE protocolo = ?", (protocolo,))

# ✅ Com Repository Pattern — o Service chama o repositório:
class DenunciaRepository:
    def buscar_por_protocolo(self, protocolo):
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM denuncia WHERE protocolo = ?", (protocolo,)
        ).fetchone()
        conn.close()
        return dict(row) if row else None
```

**Benefício:** se o banco de dados mudar de SQLite para PostgreSQL, apenas os repositórios precisam ser alterados — os serviços e controllers continuam iguais.

---

## 5. Princípios SOLID Aplicados

### 5.1 SRP — Single Responsibility Principle (Princípio da Responsabilidade Única)

> *"Uma classe deve ter apenas um motivo para mudar."*

**Onde está:** cada camada tem uma responsabilidade exclusiva e bem definida.

| Classe | Única responsabilidade |
|--------|----------------------|
| `DenunciaController` | Receber e responder requisições HTTP |
| `DenunciaService` | Aplicar regras de negócio das denúncias |
| `DenunciaRepository` | Executar operações SQL na tabela `denuncia` |
| `AuthService` | Autenticar administradores |

**Exemplo concreto:** o `DenunciaService` não sabe nada sobre HTTP (sem `request`, sem `jsonify`). O `DenunciaController` não contém regras de negócio (sem validação de transição de status). Cada um muda por um único motivo.

```python
# DenunciaService — só regra de negócio, sem HTTP
def atualizar_status(self, denuncia_id, novo_status, admin_id):
    if novo_status not in TRANSICOES_VALIDAS.get(d["status"], set()):
        raise ValueError(f"Transição inválida: {d['status']} → {novo_status}")
    ...

# AdminController — só HTTP, sem regra de negócio
@bp.patch("/denuncias/<int:denuncia_id>/status")
@requer_login
def atualizar_status(denuncia_id):
    _service.atualizar_status(denuncia_id, data.get("status"), session["admin_id"])
    return jsonify({"mensagem": "Status atualizado."})
```

---

### 5.2 OCP — Open/Closed Principle (Princípio Aberto/Fechado)

> *"Uma classe deve estar aberta para extensão, mas fechada para modificação."*

**Onde está:** `src/services/denuncia_service.py` — o dicionário `TRANSICOES_VALIDAS` e o conjunto `CATEGORIAS_VALIDAS` permitem adicionar novos estados e categorias sem alterar a lógica das funções.

**Exemplo concreto:**

```python
# Novas categorias podem ser adicionadas aqui sem tocar nos métodos
CATEGORIAS_VALIDAS = {
    "CORRUPCAO", "ASSEDIO", "VIOLENCIA", "IRREGULARIDADE", "OUTROS"
    # para adicionar "FRAUDE": basta incluir aqui, nenhum método muda
}

# Novas transições de status podem ser adicionadas sem alterar atualizar_status()
TRANSICOES_VALIDAS = {
    "RECEBIDA":    {"EM_ANALISE", "ENCERRADA"},
    "EM_ANALISE":  {"ENCAMINHADA", "ENCERRADA"},
    "ENCAMINHADA": {"EM_ANALISE", "ENCERRADA"},
    "ENCERRADA":   set()
}
```

---

### 5.3 DIP — Dependency Inversion Principle (Princípio da Inversão de Dependência)

> *"Módulos de alto nível não devem depender de módulos de baixo nível. Ambos devem depender de abstrações."*

**Onde está:** o `DenunciaService` depende do `DenunciaRepository` por composição no construtor, não instancia diretamente conexões SQL — a dependência do banco está isolada nos repositórios.

```python
class DenunciaService:
    def __init__(self):
        # Service depende do repositório (abstração), não do SQLite diretamente
        self._repo       = DenunciaRepository()
        self._comentario = ComentarioRepository()
        self._historico  = HistoricoRepository()
```

---

## 6. Decisões de Design

| Decisão | Alternativa descartada | Motivo da escolha |
|---------|----------------------|-------------------|
| API REST com JSON | Templates Jinja2 server-side | Separação clara entre frontend e backend; facilita testes da API isoladamente |
| SQLite sem ORM | SQLAlchemy | Reduz abstração e mantém o SQL visível — melhor para fins de aprendizado e auditoria |
| SHA-256 para senhas | Senha em texto puro | Segurança mínima mesmo em ambiente acadêmico; fácil de implementar sem dependências externas |
| Blueprint do Flask para separar rotas | Todas as rotas em `app.py` | Mantém os controllers organizados por domínio (denúncia vs. admin) |
| SPA (Single Page Application) | Múltiplas páginas HTML | Navegação mais fluida sem recarregamento; JavaScript gerencia as telas via `showPage()` |

---

## 7. Estrutura de Arquivos

```
src/denuncia/
├── app.py                          ← ponto de entrada Flask
├── requirements.txt                ← dependências do projeto
├── denuncia.db                     ← banco SQLite (gerado automaticamente)
├── src/
│   ├── models/
│   │   └── database.py             ← schema do banco + conexão
│   ├── repositories/
│   │   ├── denuncia_repository.py  ← SQL das denúncias, comentários e histórico
│   │   └── admin_repository.py     ← SQL dos administradores
│   ├── services/
│   │   ├── denuncia_service.py     ← regras de negócio das denúncias
│   │   └── auth_service.py         ← autenticação de administradores
│   └── controllers/
│       ├── denuncia_controller.py  ← rotas públicas (/api/denuncia/)
│       └── admin_controller.py     ← rotas protegidas (/api/admin/)
├── templates/
│   └── index.html                  ← SPA principal
└── static/
    ├── css/style.css               ← estilos do sistema
    └── js/app.js                   ← lógica do frontend
```
