"""
controllers/denuncia_controller.py
Rotas públicas — sem autenticação (cidadão).
"""

from flask import Blueprint, request, jsonify
from src.services.denuncia_service import DenunciaService

bp = Blueprint("denuncia", __name__, url_prefix="/api/denuncia")
_service = DenunciaService()


# RF-01, RF-02: registrar denúncia anônima
@bp.post("/")
def registrar():
    data = request.get_json(silent=True) or {}
    try:
        resultado = _service.registrar(
            descricao=data.get("descricao", ""),
            categoria=data.get("categoria", "")
        )
        return jsonify(resultado), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400


# RF-05: consultar por protocolo (sem login)
@bp.get("/protocolo/<protocolo>")
def consultar(protocolo):
    try:
        return jsonify(_service.consultar_por_protocolo(protocolo))
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404
