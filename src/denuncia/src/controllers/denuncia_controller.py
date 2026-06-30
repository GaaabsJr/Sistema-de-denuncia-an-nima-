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


# RF-03, US-03: anexar evidência a uma denúncia já registrada (sem login)
@bp.post("/<protocolo>/evidencia")
def anexar_evidencia(protocolo):
    arquivo = request.files.get("arquivo")
    if not arquivo or not arquivo.filename:
        return jsonify({"erro": "Nenhum arquivo enviado."}), 400
    try:
        resultado = _service.anexar_evidencia(
            protocolo=protocolo,
            nome_arquivo=arquivo.filename,
            conteudo=arquivo.read()
        )
        return jsonify(resultado), 201
    except ValueError as e:
        status = 404 if "Protocolo não encontrado" in str(e) else 400
        return jsonify({"erro": str(e)}), status