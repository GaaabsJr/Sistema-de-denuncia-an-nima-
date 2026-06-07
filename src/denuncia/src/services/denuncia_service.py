"""
services/denuncia_service.py
Regras de negócio para denúncias (SRP — Single Responsibility Principle).
"""

import uuid
from datetime import datetime
from src.repositories.denuncia_repository import (
    DenunciaRepository, ComentarioRepository, HistoricoRepository
)

CATEGORIAS_VALIDAS = {
    "CORRUPCAO", "ASSEDIO", "VIOLENCIA", "IRREGULARIDADE", "OUTROS"
}

STATUS_VALIDOS = {
    "RECEBIDA", "EM_ANALISE", "ENCAMINHADA", "ENCERRADA"
}

# Open/Closed Principle: novas categorias podem ser adicionadas sem mudar o serviço
TRANSICOES_VALIDAS = {
    "RECEBIDA":    {"EM_ANALISE", "ENCERRADA"},
    "EM_ANALISE":  {"ENCAMINHADA", "ENCERRADA"},
    "ENCAMINHADA": {"EM_ANALISE", "ENCERRADA"},
    "ENCERRADA":   set()
}


class DenunciaService:

    def __init__(self):
        self._repo      = DenunciaRepository()
        self._comentario = ComentarioRepository()
        self._historico  = HistoricoRepository()

    # RF-01, RF-02: registrar denúncia anônima com categoria
    def registrar(self, descricao: str, categoria: str) -> dict:
        if not descricao or len(descricao.strip()) < 10:
            raise ValueError("A descrição deve ter pelo menos 10 caracteres.")
        if categoria.upper() not in CATEGORIAS_VALIDAS:
            raise ValueError(f"Categoria inválida: {categoria}")

        protocolo = self._gerar_protocolo()
        data      = datetime.now().isoformat()

        self._repo.criar(protocolo, descricao.strip(), categoria.upper(), data)
        self._historico.registrar(
            self._buscar_id_por_protocolo(protocolo),
            "INICIO", "RECEBIDA", data
        )
        return {"protocolo": protocolo}

    # RF-05: consultar status por protocolo (sem login)
    def consultar_por_protocolo(self, protocolo: str) -> dict:
        d = self._repo.buscar_por_protocolo(protocolo.strip().upper())
        if not d:
            raise ValueError("Protocolo não encontrado.")
        historico = self._historico.listar_por_denuncia(d["id"])
        return {
            "protocolo":      d["protocolo"],
            "categoria":      d["categoria"],
            "status":         d["status"],
            "data_registro":  d["data_registro"],
            "historico":      historico
        }

    # RF-07: listar e filtrar denúncias (admin)
    def listar(self, status=None, categoria=None) -> list:
        return self._repo.listar_todas(status, categoria)

    # RF-07: atualizar status (admin)
    def atualizar_status(self, denuncia_id: int, novo_status: str, admin_id: int):
        d = self._repo.buscar_por_id(denuncia_id)
        if not d:
            raise ValueError("Denúncia não encontrada.")
        if novo_status not in STATUS_VALIDOS:
            raise ValueError("Status inválido.")
        if novo_status not in TRANSICOES_VALIDAS.get(d["status"], set()):
            raise ValueError(
                f"Transição inválida: {d['status']} → {novo_status}"
            )
        data = datetime.now().isoformat()
        self._repo.atualizar_status(denuncia_id, novo_status)
        self._historico.registrar(
            denuncia_id, d["status"], novo_status, data, admin_id
        )

    # RF-07: adicionar comentário interno (nunca visível ao denunciante — RN-04)
    def adicionar_comentario(self, denuncia_id: int, admin_id: int, texto: str):
        if not texto or len(texto.strip()) < 3:
            raise ValueError("Comentário muito curto.")
        self._comentario.criar(denuncia_id, admin_id, texto.strip(),
                               datetime.now().isoformat())

    def buscar_detalhes(self, denuncia_id: int) -> dict:
        d = self._repo.buscar_por_id(denuncia_id)
        if not d:
            raise ValueError("Denúncia não encontrada.")
        d["historico"]   = self._historico.listar_por_denuncia(denuncia_id)
        d["comentarios"] = self._comentario.listar_por_denuncia(denuncia_id)
        return d

    def _gerar_protocolo(self) -> str:
        return "DEN-" + uuid.uuid4().hex[:8].upper()

    def _buscar_id_por_protocolo(self, protocolo: str) -> int:
        d = self._repo.buscar_por_protocolo(protocolo)
        return d["id"] if d else None
