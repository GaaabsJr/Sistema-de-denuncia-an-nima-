"""
tests/test_api.py
Testes de integração das rotas Flask.
Testa os endpoints da API com o cliente de teste do Flask.

Cobre:
  - POST /api/denuncia/ — registrar denúncia via API
  - GET  /api/denuncia/protocolo/<cod> — consultar por protocolo
  - POST /api/admin/login — autenticação de administrador
  - GET  /api/admin/denuncias — listar denúncias (protegido)
  - PATCH /api/admin/denuncias/<id>/status — atualizar status
  - POST  /api/admin/denuncias/<id>/comentario — adicionar comentário
"""

import pytest
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret"
    with app.test_client() as c:
        yield c


def registrar_denuncia(client, descricao="Denúncia de integração para testes.", categoria="CORRUPCAO"):
    """Utilitário: registra uma denúncia e retorna o protocolo."""
    res = client.post("/api/denuncia/", json={
        "descricao": descricao,
        "categoria": categoria
    })
    return json.loads(res.data)


def login_admin(client):
    """Utilitário: faz login do admin padrão."""
    return client.post("/api/admin/login", json={
        "email": "admin@sistema.gov.br",
        "senha": "admin123"
    })


# ── Rotas públicas ────────────────────────────────────────────────────────────

def test_api_registrar_denuncia(client):
    """RF-01: POST /api/denuncia/ deve retornar 201 e protocolo."""
    res = client.post("/api/denuncia/", json={
        "descricao": "Teste de integração para registro de denúncia.",
        "categoria": "CORRUPCAO"
    })
    assert res.status_code == 201
    data = json.loads(res.data)
    assert "protocolo" in data
    assert data["protocolo"].startswith("DEN-")


def test_api_registrar_denuncia_invalida(client):
    """RF-01: POST com dados inválidos deve retornar 400."""
    res = client.post("/api/denuncia/", json={
        "descricao": "Curta",
        "categoria": "CORRUPCAO"
    })
    assert res.status_code == 400
    data = json.loads(res.data)
    assert "erro" in data


def test_api_consultar_protocolo(client):
    """RF-05: GET /api/denuncia/protocolo/<cod> deve retornar status."""
    d = registrar_denuncia(client)
    res = client.get(f"/api/denuncia/protocolo/{d['protocolo']}")
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data["status"] == "RECEBIDA"
    assert data["protocolo"] == d["protocolo"]


def test_api_consultar_protocolo_invalido(client):
    """RF-05: protocolo inexistente deve retornar 404."""
    res = client.get("/api/denuncia/protocolo/DEN-00000000")
    assert res.status_code == 404


def test_api_anexar_evidencia(client, monkeypatch, tmp_path):
    """RF-03/US-03: POST /api/denuncia/<protocolo>/evidencia deve aceitar e salvar o arquivo."""
    import src.services.denuncia_service as service_module
    monkeypatch.setattr(service_module, "UPLOAD_DIR", str(tmp_path))

    d = registrar_denuncia(client)
    from io import BytesIO
    res = client.post(
        f"/api/denuncia/{d['protocolo']}/evidencia",
        data={"arquivo": (BytesIO(b"conteudo-fake"), "print.png")},
        content_type="multipart/form-data"
    )
    assert res.status_code == 201
    data = json.loads(res.data)
    assert data["nome_arquivo"] == "print.png"

    consulta = client.get(f"/api/denuncia/protocolo/{d['protocolo']}")
    assert len(json.loads(consulta.data)["evidencias"]) == 1


def test_api_anexar_evidencia_formato_invalido(client, monkeypatch, tmp_path):
    """RF-03/US-03: formato não aceito deve retornar 400."""
    import src.services.denuncia_service as service_module
    monkeypatch.setattr(service_module, "UPLOAD_DIR", str(tmp_path))

    d = registrar_denuncia(client)
    from io import BytesIO
    res = client.post(
        f"/api/denuncia/{d['protocolo']}/evidencia",
        data={"arquivo": (BytesIO(b"conteudo"), "virus.exe")},
        content_type="multipart/form-data"
    )
    assert res.status_code == 400


# ── Autenticação ──────────────────────────────────────────────────────────────

def test_api_login_valido(client):
    """RF-07: login com credenciais corretas deve retornar 200."""
    res = login_admin(client)
    assert res.status_code == 200
    data = json.loads(res.data)
    assert "admin" in data
    assert data["admin"]["email"] == "admin@sistema.gov.br"


def test_api_login_invalido(client):
    """RF-07: login com senha errada deve retornar 401."""
    res = client.post("/api/admin/login", json={
        "email": "admin@sistema.gov.br",
        "senha": "senha_errada"
    })
    assert res.status_code == 401


def test_api_rota_protegida_sem_login(client):
    """RN-05: rotas admin sem sessão devem retornar 401."""
    res = client.get("/api/admin/denuncias")
    assert res.status_code == 401


# ── Rotas protegidas ──────────────────────────────────────────────────────────

def test_api_listar_denuncias(client):
    """RF-08: admin autenticado deve listar denúncias."""
    registrar_denuncia(client)
    login_admin(client)
    res = client.get("/api/admin/denuncias")
    assert res.status_code == 200
    data = json.loads(res.data)
    assert len(data) >= 1


def test_api_atualizar_status(client):
    """RF-11: admin deve conseguir atualizar status de denúncia."""
    registrar_denuncia(client)
    login_admin(client)

    lista = json.loads(client.get("/api/admin/denuncias").data)
    denuncia_id = lista[0]["id"]

    res = client.patch(f"/api/admin/denuncias/{denuncia_id}/status",
                       json={"status": "EM_ANALISE"})
    assert res.status_code == 200


def test_api_adicionar_comentario(client):
    """RF-12: admin deve conseguir adicionar comentário interno."""
    registrar_denuncia(client)
    login_admin(client)

    lista = json.loads(client.get("/api/admin/denuncias").data)
    denuncia_id = lista[0]["id"]

    res = client.post(f"/api/admin/denuncias/{denuncia_id}/comentario",
                      json={"texto": "Caso em análise pela equipe."})
    assert res.status_code == 200