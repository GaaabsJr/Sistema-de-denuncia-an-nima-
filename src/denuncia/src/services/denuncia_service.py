"""
services/denuncia_service.py
Regras de negócio para denúncias (SRP — Single Responsibility Principle).
"""

import os
import uuid
from datetime import datetime
from src.repositories.denuncia_repository import (
    DenunciaRepository, ComentarioRepository, HistoricoRepository, EvidenciaRepository
)

CATEGORIAS_VALIDAS = {
    "CORRUPCAO", "ASSEDIO", "VIOLENCIA", "IRREGULARIDADE", "OUTROS"
}

# RF-03 / US-03: formatos e tamanho máximo aceitos para evidências anexadas
EXTENSOES_EVIDENCIA_VALIDAS = {".jpg", ".jpeg", ".png", ".pdf", ".docx", ".mp4"}
TAMANHO_MAXIMO_EVIDENCIA_BYTES = 10 * 1024 * 1024  # 10 MB

# Diretório onde os arquivos de evidência ficam armazenados (fora do repositório)
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "uploads")

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
        self._repo       = DenunciaRepository()
        self._comentario = ComentarioRepository()
        self._historico   = HistoricoRepository()
        self._evidencia   = EvidenciaRepository()

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
        historico   = self._historico.listar_por_denuncia(d["id"])
        evidencias  = self._evidencia.listar_por_denuncia(d["id"])
        return {
            "protocolo":      d["protocolo"],
            "categoria":      d["categoria"],
            "status":         d["status"],
            "data_registro":  d["data_registro"],
            "historico":      historico,
            "evidencias":     [
                {"nome_arquivo": e["nome_arquivo"], "tamanho_bytes": e["tamanho_bytes"],
                 "data_upload": e["data_upload"]}
                for e in evidencias
            ]
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
        d["evidencias"]  = [
            {"id": e["id"], "nome_arquivo": e["nome_arquivo"], "tipo_arquivo": e["tipo_arquivo"],
             "tamanho_bytes": e["tamanho_bytes"], "data_upload": e["data_upload"]}
            for e in self._evidencia.listar_por_denuncia(denuncia_id)
        ]
        return d

    # RF-07: recupera o caminho em disco de uma evidência, para download pelo admin
    def caminho_evidencia(self, evidencia_id: int) -> dict:
        e = self._evidencia.buscar_por_id(evidencia_id)
        if not e:
            raise ValueError("Evidência não encontrada.")
        return e

    # RF-03, US-03: valida formato e tamanho de um anexo de evidência
    def validar_evidencia(self, nome_arquivo: str, tamanho_bytes: int) -> bool:
        extensao = "." + nome_arquivo.rsplit(".", 1)[-1].lower() if "." in nome_arquivo else ""
        if extensao not in EXTENSOES_EVIDENCIA_VALIDAS:
            raise ValueError(
                f"formato não aceito: {extensao or 'sem extensão'}. "
                f"Formatos aceitos: {', '.join(sorted(EXTENSOES_EVIDENCIA_VALIDAS))}"
            )
        if tamanho_bytes > TAMANHO_MAXIMO_EVIDENCIA_BYTES:
            raise ValueError(
                f"tamanho do arquivo excede o máximo permitido de "
                f"{TAMANHO_MAXIMO_EVIDENCIA_BYTES // (1024 * 1024)}MB."
            )
        return True

    # RF-03, US-03: anexa um arquivo de evidência a uma denúncia já registrada
    def anexar_evidencia(self, protocolo: str, nome_arquivo: str, conteudo: bytes) -> dict:
        d = self._repo.buscar_por_protocolo(protocolo.strip().upper())
        if not d:
            raise ValueError("Protocolo não encontrado.")

        tamanho_bytes = len(conteudo)
        self.validar_evidencia(nome_arquivo, tamanho_bytes)  # levanta ValueError se inválido

        extensao = "." + nome_arquivo.rsplit(".", 1)[-1].lower()
        pasta_denuncia = os.path.join(UPLOAD_DIR, d["protocolo"])
        os.makedirs(pasta_denuncia, exist_ok=True)

        nome_armazenado = f"{uuid.uuid4().hex}{extensao}"
        caminho_completo = os.path.join(pasta_denuncia, nome_armazenado)
        with open(caminho_completo, "wb") as f:
            f.write(conteudo)

        data_upload = datetime.now().isoformat()
        self._evidencia.criar(
            denuncia_id=d["id"],
            nome_arquivo=nome_arquivo,
            tipo_arquivo=extensao.lstrip("."),
            tamanho_bytes=tamanho_bytes,
            caminho=caminho_completo,
            data_upload=data_upload
        )
        return {
            "nome_arquivo": nome_arquivo,
            "tamanho_bytes": tamanho_bytes,
            "mensagem": "Evidência anexada com sucesso."
        }

    def _gerar_protocolo(self) -> str:
        return "DEN-" + uuid.uuid4().hex[:8].upper()

    def _buscar_id_por_protocolo(self, protocolo: str) -> int:
        d = self._repo.buscar_por_protocolo(protocolo)
        return d["id"] if d else None