"""
controllers/admin_controller.py
Rotas protegidas — requer sessão de administrador (RF-06, RF-07, RF-08).
"""

from flask import Blueprint, request, jsonify, session, send_file
from functools import wraps
from src.services.denuncia_service import DenunciaService
from src.services.auth_service import AuthService

bp = Blueprint("admin", __name__, url_prefix="/api/admin")
_service = DenunciaService()
_auth    = AuthService()


# ── Decorator de autenticação (LSP: qualquer admin autenticado pode usar) ──
def requer_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "admin_id" not in session:
            return jsonify({"erro": "Acesso não autorizado."}), 401
        return f(*args, **kwargs)
    return decorated


# RF-06: login
@bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    try:
        admin = _auth.autenticar(data.get("email", ""), data.get("senha", ""))
        session["admin_id"]   = admin["id"]
        session["admin_nome"] = admin["nome"]
        return jsonify({"mensagem": "Login realizado.", "admin": admin})
    except ValueError as e:
        return jsonify({"erro": str(e)}), 401


@bp.post("/logout")
def logout():
    session.clear()
    return jsonify({"mensagem": "Logout realizado."})


@bp.get("/me")
@requer_login
def me():
    return jsonify({
        "admin_id":   session["admin_id"],
        "admin_nome": session["admin_nome"]
    })


# RF-07: listar denúncias com filtros
@bp.get("/denuncias")
@requer_login
def listar():
    status    = request.args.get("status")
    categoria = request.args.get("categoria")
    return jsonify(_service.listar(status, categoria))


# RF-07: detalhe de uma denúncia (com histórico e comentários)
@bp.get("/denuncias/<int:denuncia_id>")
@requer_login
def detalhe(denuncia_id):
    try:
        return jsonify(_service.buscar_detalhes(denuncia_id))
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404


# RF-07: atualizar status
@bp.patch("/denuncias/<int:denuncia_id>/status")
@requer_login
def atualizar_status(denuncia_id):
    data = request.get_json(silent=True) or {}
    try:
        _service.atualizar_status(
            denuncia_id,
            data.get("status", ""),
            session["admin_id"]
        )
        return jsonify({"mensagem": "Status atualizado."})
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400


# RF-07: adicionar comentário interno
@bp.post("/denuncias/<int:denuncia_id>/comentario")
@requer_login
def comentar(denuncia_id):
    data = request.get_json(silent=True) or {}
    try:
        _service.adicionar_comentario(
            denuncia_id,
            session["admin_id"],
            data.get("texto", "")
        )
        return jsonify({"mensagem": "Comentário adicionado."})
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400


# RF-03/US-03: download de uma evidência anexada (apenas admin autenticado)
@bp.get("/evidencias/<int:evidencia_id>/download")
@requer_login
def baixar_evidencia(evidencia_id):
    try:
        e = _service.caminho_evidencia(evidencia_id)
        return send_file(e["caminho"], download_name=e["nome_arquivo"], as_attachment=True)
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404
    except FileNotFoundError:
        return jsonify({"erro": "Arquivo não encontrado no servidor."}), 404