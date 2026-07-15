# 🔒 Sistema de Denúncia Anônima

Repositório destinado ao projeto final da disciplina de Engenharia de Software, ministrada pelo Professor Adolfo Colares, na Universidade Federal do Amapá (UNIFAP), no semestre de 2026.1

---

## 👥 Componentes do Grupo

- Cauan Antônio Costa Miranda
- Eric Felipe da Silva Fernandes
- Gabriel Alves Lima
- Johan Mateus de Oliveira Natividade
- João Lucas Farias De Sena

---

## 📚 Sobre o Projeto

Observa-se, no contexto social e institucional, uma demanda crescente por mecanismos seguros e acessíveis que permitam a qualquer cidadão reportar irregularidades, crimes, corrupção ou situações de risco sem que precise se identificar, evitando assim represálias e incentivando a participação ativa na construção de ambientes mais justos e transparentes.

O objetivo deste projeto é desenvolver uma plataforma web de denúncia anônima capaz de receber, organizar e encaminhar relatos de forma segura e confidencial, garantindo o anonimato do denunciante e permitindo que órgãos competentes ou gestores institucionais acompanhem e tratem cada ocorrência registrada com eficiência e responsabilidade.

---

## 📋 Requisitos Funcionais (resumo)

O sistema conta com **14 Requisitos Funcionais** e **10 Requisitos Não Funcionais**, priorizados em MVP / Desejável / Futuro. Abaixo, os principais do MVP — a lista completa, com priorização e regras de negócio, está em [`docs/requisitos-software.md`](docs/requisitos-software.md).

- **RF-01:** Permitir o registro de denúncias anônimas, sem exigir identificação do usuário.
- **RF-02:** Permitir que o denunciante escolha a categoria da denúncia (corrupção, assédio, violência, irregularidade administrativa, outros).
- **RF-04:** Gerar um código único de protocolo ao final de cada denúncia registrada, permitindo o acompanhamento posterior.
- **RF-05:** Permitir que o denunciante consulte o status de sua denúncia por meio do código de protocolo, sem necessidade de cadastro.
- **RF-07:** Permitir o login de administradores cadastrados.
- **RF-08:** Permitir que administradores visualizem todas as denúncias recebidas.
- **RF-11:** Permitir que administradores atualizem o status de uma denúncia.
- **RF-14:** Registrar o histórico de alterações de status e encaminhamentos de cada denúncia.

> 📄 Requisitos completos (RF-01 a RF-14, RNF-01 a RNF-10, regras de negócio e glossário): [`docs/requisitos-software.md`](docs/requisitos-software.md)

---

## 🚀 Tecnologias Utilizadas

| Camada | Tecnologia |
|--------|------------|
| Backend | Python 3.12 + Flask 3.0 |
| Banco de dados | SQLite (arquivo `denuncia.db`, sem ORM) |
| Frontend | HTML5 + CSS3 + JavaScript puro (SPA) |
| Autenticação | Sessões Flask + hash SHA-256 |
| Testes | pytest + pytest-cov |

Justificativa detalhada de cada escolha em [`docs/documento-arquitetura.md`](docs/documento-arquitetura.md).

---

## ▶️ Como Rodar o Projeto

**Pré-requisitos:** Python 3.10+ instalado.

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd Sistema-de-denuncia-anonima/src/denuncia

# 2. Crie e ative um ambiente virtual (recomendado)
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Rode a aplicação
python3 app.py
```

O sistema sobe em **http://localhost:5000**. O banco SQLite (`denuncia.db`) é criado automaticamente na primeira execução.

**Login de administrador para demonstração:**
- E-mail: `admin@sistema.gov.br`
- Senha: `admin123`

---

## 🧪 Como Rodar os Testes

```bash
cd src/denuncia
pip install pytest pytest-cov
pytest tests/ -v --cov=src --cov-report=term-missing
```

Resultado atual: **30 testes automatizados** (20 unitários + 10 de integração), **92% de cobertura**. Detalhes em [`src/denuncia/tests/plano-de-testes.md`](src/denuncia/tests/plano-de-testes.md).

---

## 📁 Documentação

- [Documento de Visão](docs/documento-visao.md)
- [Documento de Requisitos de Software](docs/requisitos-software.md)
- [User Stories e Critérios de Aceitação](docs/user-stories.md)
- [Descrições Expandidas de Casos de Uso](docs/descricoes_casos_de_uso.md)
- [Justificativa de Modelagem (Diagrama de Classes)](docs/justificativa-modelagem.md)
- [Documento de Arquitetura e Design](docs/documento-arquitetura.md)
- [Gestão do Processo (Kanban, backlog, lições aprendidas)](docs/Gestao_do_processo.md)
- [Plano de Testes](src/denuncia/tests/plano-de-testes.md)
- Diagramas UML: [Casos de Uso](docs/diagrama-casos-de-uso.png) · [Classes](docs/diagrama_classes_denuncia.pdf) · [Sequência 1 — Registrar](docs/diagrama_sequencia_1_registrar.pdf) · [Sequência 2 — Atualizar Status](docs/diagrama_sequencia_2_atualizar_status.pdf) · [Atividades](docs/diagrama_atividades.pdf) · [Arquitetura](docs/diagrama_arquitetura_denuncia.png)