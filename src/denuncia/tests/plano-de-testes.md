# Plano de Testes

**Projeto:** Sistema de Denúncia Anônima  
**Disciplina:** Engenharia de Software (CC0116) — Prof. Adolfo Colares — UNIFAP 2026.1  
**Equipe:** Cauan Miranda · Eric Fernandes · Gabriel Lima · Johan Natividade · João Lucas Sena  
**Ferramenta:** pytest + pytest-cov  
**Versão:** 1.0

---

## 1. Estratégia de Testes

O projeto adota dois níveis de teste:

- **Testes unitários** (`test_denuncia_service.py`): validam as regras de negócio isoladamente, sem HTTP. Usam banco SQLite em memória via fixture `banco_em_memoria`, garantindo isolamento entre testes.
- **Testes de integração** (`test_api.py`): validam os endpoints da API Flask de ponta a ponta, incluindo autenticação de sessão e serialização JSON.

---

## 2. Como executar

```bash
# Na pasta src/denuncia/
cd src/denuncia

# Rodar todos os testes
pytest tests/ -v

# Rodar com relatório de cobertura
pytest tests/ -v --cov=src --cov-report=term-missing
```

---

## 3. Casos de Teste

### 3.1 Testes Unitários — DenunciaService

| ID | Descrição | Entrada | Saída esperada | RF/RN |
|----|-----------|---------|----------------|-------|
| UT-01 | Registrar denúncia válida | descricao válida + categoria válida | protocolo `DEN-XXXXXXXX` | RF-01, RF-02 |
| UT-02 | Protocolo único por denúncia | 2 registros diferentes | protocolos distintos | RF-04 |
| UT-03 | Rejeitar descrição curta | descrição < 10 chars | `ValueError` | RN-02 |
| UT-04 | Rejeitar descrição vazia | `""` | `ValueError` | RN-02 |
| UT-05 | Rejeitar categoria inválida | categoria inexistente | `ValueError` | RN-02 |
| UT-06 | Aceitar todas as categorias válidas | 5 categorias do sistema | 5 protocolos gerados | RF-02 |
| UT-07 | Consultar protocolo existente | protocolo gerado | status RECEBIDA + histórico | RF-05 |
| UT-08 | Consultar protocolo inexistente | `DEN-00000000` | `ValueError` | RF-05 |
| UT-09 | Consulta insensível a maiúsculas | protocolo em minúsculas | retorno correto | RF-05 |
| UT-10 | Listar todas as denúncias | 2 registros | lista com 2 itens | RF-08 |
| UT-11 | Filtrar por categoria | 1 CORRUPCAO + 1 ASSEDIO | lista com 1 item | RF-10 |
| UT-12 | Filtrar por status | 1 RECEBIDA | lista com 1 / 0 itens | RF-10 |
| UT-13 | Atualizar status válido | RECEBIDA → EM_ANALISE | status atualizado | RF-11 |
| UT-14 | Histórico registrado na atualização | transição de status | histórico com par (ant, novo) | RN-06 |
| UT-15 | Rejeitar transição inválida | RECEBIDA → ENCAMINHADA | `ValueError` | RN-08 |
| UT-16 | Rejeitar atualização em denúncia inexistente | id=9999 | `ValueError` | RF-11 |
| UT-17 | Denúncia encerrada não reabre | ENCERRADA → EM_ANALISE | `ValueError` | RN-08 |
| UT-18 | Adicionar comentário interno | texto válido | comentário salvo | RF-12 |
| UT-19 | Rejeitar comentário vazio | `""` | `ValueError` | RF-12 |
| UT-20 | Comentário não visível na consulta pública | consulta por protocolo | sem campo `comentarios` | RN-04 |

### 3.2 Testes de Integração — API Flask

| ID | Endpoint | Método | Entrada | Saída esperada | RF |
|----|----------|--------|---------|----------------|-----|
| IT-01 | `/api/denuncia/` | POST | dados válidos | 201 + protocolo | RF-01 |
| IT-02 | `/api/denuncia/` | POST | dados inválidos | 400 + erro | RF-01 |
| IT-03 | `/api/denuncia/protocolo/<cod>` | GET | protocolo válido | 200 + status | RF-05 |
| IT-04 | `/api/denuncia/protocolo/<cod>` | GET | protocolo inválido | 404 | RF-05 |
| IT-05 | `/api/admin/login` | POST | credenciais corretas | 200 + dados admin | RF-07 |
| IT-06 | `/api/admin/login` | POST | credenciais erradas | 401 | RF-07 |
| IT-07 | `/api/admin/denuncias` | GET | sem sessão | 401 | RN-05 |
| IT-08 | `/api/admin/denuncias` | GET | com sessão | 200 + lista | RF-08 |
| IT-09 | `/api/admin/denuncias/<id>/status` | PATCH | status válido | 200 | RF-11 |
| IT-10 | `/api/admin/denuncias/<id>/comentario` | POST | texto válido | 200 | RF-12 |

---

## 4. Resultados (última execução)

```
pytest tests/ -v --cov=src --cov-report=term-missing
```
<img width="923" height="775" alt="Captura de Tela 2026-07-14 às 23 25 18" src="https://github.com/user-attachments/assets/cc8d5d30-c27f-4d99-9575-d40f9f884691" />


---

## 5. Cobertura mínima esperada

| Módulo | Cobertura esperada |
|--------|--------------------|
| `services/denuncia_service.py` | ≥ 85% |
| `services/auth_service.py` | ≥ 80% |
| `controllers/denuncia_controller.py` | ≥ 75% |
| `controllers/admin_controller.py` | ≥ 75% |
| `repositories/denuncia_repository.py` | ≥ 70% |
| **Total** | **≥ 70%** |
