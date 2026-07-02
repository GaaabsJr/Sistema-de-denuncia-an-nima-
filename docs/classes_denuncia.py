
from datetime import datetime
from enum import Enum
import uuid


# ─────────────────────────────────────────
# Enumerações (derivadas do diagrama)
# ─────────────────────────────────────────

class StatusDenuncia(Enum):
    RECEBIDA     = "RECEBIDA"
    EM_ANALISE   = "EM_ANALISE"
    ENCAMINHADA  = "ENCAMINHADA"
    ENCERRADA    = "ENCERRADA"


class CategoriaDenuncia(Enum):
    CORRUPCAO      = "CORRUPCAO"
    ASSEDIO        = "ASSEDIO"
    VIOLENCIA      = "VIOLENCIA"
    IRREGULARIDADE = "IRREGULARIDADE"
    OUTROS         = "OUTROS"


class NivelAcesso(Enum):
    OPERADOR   = "OPERADOR"
    SUPERVISOR = "SUPERVISOR"
    ADMIN      = "ADMIN"


# ─────────────────────────────────────────
# CLASSE 1: Denuncia
# Derivada da US-01 (Registrar Denúncia) e
# US-04 (Consultar Protocolo por código)
# ─────────────────────────────────────────

class Denuncia:
    """
    Representa uma denúncia anônima registrada no sistema.
    Cada denúncia gera um protocolo único para rastreamento público.

    Relacionamentos (do diagrama):
      - __evidencias: List[Evidencia]       → composição (1 para 0..*)
      - __historico: List[HistoricoStatus]  → composição (1 para 1..*)
      - __comentarios: List[ComentarioInterno] → composição (1 para 0..*)
      - __protocolo: Protocolo              → associação (1 para 1)
    """

    def __init__(self, descricao: str, categoria: CategoriaDenuncia):
        # Atributos privados — encapsulamento conforme diagrama (-)
        self.__id: int = None
        self.__protocolo: str = self.__gerar_protocolo()
        self.__descricao: str = descricao
        self.__data_registro: datetime = datetime.now()
        self.__status: StatusDenuncia = StatusDenuncia.RECEBIDA
        self.__categoria: CategoriaDenuncia = categoria

        # Relacionamentos por composição — partes não existem sem a denúncia
        self.__evidencias: list = []        # 0..* Evidencia
        self.__historico: list = []         # 1..* HistoricoStatus
        self.__comentarios: list = []       # 0..* ComentarioInterno

    # ── Método de negócio: geração do protocolo ──
    def __gerar_protocolo(self) -> str:
        """
        Gera um código único de protocolo para rastreamento público.
        Formato: DEN-XXXXXXXX (8 caracteres hex em maiúsculas).
        Derivado de RF-04: o sistema deve gerar código único ao concluir o registro.
        """
        codigo = uuid.uuid4().hex[:8].upper()
        return f"DEN-{codigo}"

    def registrar(self) -> None:
        """
        Finaliza o registro da denúncia, confirmando status inicial.
        Derivado de RF-01 (registrar denúncia anônima).
        """
        self.__status = StatusDenuncia.RECEBIDA
        print(f"[Denuncia] Denúncia registrada com protocolo: {self.__protocolo}")

    def get_status(self) -> StatusDenuncia:
        return self.__status

    def set_status(self, novo_status: StatusDenuncia) -> None:
        """
        Atualiza o status da denúncia.
        Apenas administradores devem chamar este método (RN-08).
        """
        if not isinstance(novo_status, StatusDenuncia):
            raise ValueError("Status inválido.")
        self.__status = novo_status

    # ── Getters públicos (+) ──
    def get_protocolo(self) -> str:
        return self.__protocolo

    def get_descricao(self) -> str:
        return self.__descricao

    def get_categoria(self) -> CategoriaDenuncia:
        return self.__categoria

    def get_data_registro(self) -> datetime:
        return self.__data_registro

    def get_evidencias(self) -> list:
        return list(self.__evidencias)  # retorna cópia defensiva

    def get_historico(self) -> list:
        return list(self.__historico)

    def get_comentarios(self) -> list:
        return list(self.__comentarios)

    def adicionar_evidencia(self, evidencia) -> None:
        self.__evidencias.append(evidencia)

    def adicionar_comentario(self, comentario) -> None:
        self.__comentarios.append(comentario)

    def adicionar_historico(self, registro) -> None:
        self.__historico.append(registro)

    def __repr__(self) -> str:
        return (
            f"Denuncia(protocolo='{self.__protocolo}', "
            f"categoria={self.__categoria.value}, "
            f"status={self.__status.value})"
        )


# ─────────────────────────────────────────
# CLASSE 2: Administrador
# Derivada de US-05 (Cadastrar Conta Admin),
# US-08 (Atualizar Status), US-09 (Comentários),
# US-10 (Encaminhar Denúncia)
# Herda de Usuario (classe abstrata do diagrama)
# ─────────────────────────────────────────

class Administrador:
    """
    Representa um gestor institucional responsável pelo
    gerenciamento das denúncias recebidas no sistema.

    Relacionamentos (do diagrama):
      - gerencia: List[Denuncia]  → associação (0..* para 0..*)
      - escreve: List[ComentarioInterno] → associação (1 para 0..*)
    """

    def __init__(self, nome: str, email: str, senha_hash: str,
                 matricula: str, setor: str, nivel_acesso: NivelAcesso):
        # Atributos herdados de Usuario (protected: #)
        self._id: int = None
        self._nome: str = nome
        self._email: str = email
        self._senha_hash: str = senha_hash
        self._data_cadastro: datetime = datetime.now()

        # Atributos próprios do Administrador (privados: -)
        self.__matricula: str = matricula
        self.__setor: str = setor
        self.__nivel_acesso: NivelAcesso = nivel_acesso
        self.__ativo: bool = True

        # Relacionamento: administrador gerencia denúncias (0..*)
        self.__denuncias_gerenciadas: list = []

    # ── Método herdado de Usuario ──
    def autenticar(self, email: str, senha_hash: str) -> bool:
        """
        Verifica credenciais do administrador.
        Derivado de RF-07 (autenticação de administradores).
        """
        return self._email == email and self._senha_hash == senha_hash

    # ── Métodos de negócio do Administrador ──
    def visualizar_denuncias(self) -> list:
        """
        Retorna a lista de denúncias gerenciadas por este administrador.
        Derivado de RF-08 (visualizar denúncias recebidas).
        """
        return list(self.__denuncias_gerenciadas)

    def atualizar_status(self, denuncia: Denuncia,
                         novo_status: StatusDenuncia) -> None:
        """
        Atualiza o status de uma denúncia.
        Derivado de RF-11 (atualizar status) e RN-06 (histórico preservado).
        """
        if not self.__ativo:
            raise PermissionError("Administrador inativo não pode atualizar denúncias.")

        status_anterior = denuncia.get_status()
        denuncia.set_status(novo_status)

        # Registra transição no histórico (composição do diagrama)
        historico = {
            "status_anterior": status_anterior.value,
            "status_novo": novo_status.value,
            "data_alteracao": datetime.now().isoformat(),
            "administrador": self._nome
        }
        denuncia.adicionar_historico(historico)
        print(f"[Admin] Status de {denuncia.get_protocolo()} "
              f"alterado: {status_anterior.value} → {novo_status.value}")

    def encaminhar(self, denuncia: Denuncia,
                   destino: "Administrador") -> None:
        """
        Encaminha uma denúncia para outro administrador.
        Derivado de RF-13 (encaminhar denúncia) e US-10.
        """
        if not self.__ativo:
            raise PermissionError("Administrador inativo não pode encaminhar denúncias.")

        destino.receber_denuncia(denuncia)
        self.atualizar_status(denuncia, StatusDenuncia.ENCAMINHADA)
        print(f"[Admin] Denúncia {denuncia.get_protocolo()} "
              f"encaminhada para {destino.get_nome()}.")

    def adicionar_comentario(self, denuncia: Denuncia, texto: str) -> None:
        """
        Adiciona comentário interno a uma denúncia.
        Derivado de RF-12 (comentários internos) e RN-04 (não visível ao público).
        """
        comentario = {
            "texto": texto,
            "data_registro": datetime.now().isoformat(),
            "administrador": self._nome,
            "visivel_para_denunciante": False  # RN-04: sempre privado
        }
        denuncia.adicionar_comentario(comentario)
        print(f"[Admin] Comentário interno adicionado em {denuncia.get_protocolo()}.")

    def receber_denuncia(self, denuncia: Denuncia) -> None:
        """Adiciona uma denúncia encaminhada à fila deste administrador."""
        self.__denuncias_gerenciadas.append(denuncia)

    # ── Getters públicos (+) ──
    def get_nome(self) -> str:
        return self._nome

    def get_email(self) -> str:
        return self._email

    def get_matricula(self) -> str:
        return self.__matricula

    def get_setor(self) -> str:
        return self.__setor

    def get_nivel_acesso(self) -> NivelAcesso:
        return self.__nivel_acesso

    def is_ativo(self) -> bool:
        return self.__ativo

    def __repr__(self) -> str:
        return (
            f"Administrador(nome='{self._nome}', "
            f"setor='{self.__setor}', "
            f"nivel={self.__nivel_acesso.value})"
        )


# ─────────────────────────────────────────
# Teste rápido de uso
# ─────────────────────────────────────────

if __name__ == "__main__":
    # Criando uma denúncia anônima
    denuncia = Denuncia(
        descricao="Servidor público exigiu pagamento para emitir documento.",
        categoria=CategoriaDenuncia.CORRUPCAO
    )
    denuncia.registrar()
    print(denuncia)

    # Criando um administrador
    admin = Administrador(
        nome="Carlos Gestor",
        email="carlos@ouvidoria.gov.br",
        senha_hash="hash_seguro_aqui",
        matricula="ADM-001",
        setor="Ouvidoria",
        nivel_acesso=NivelAcesso.SUPERVISOR
    )

    # Autenticação
    ok = admin.autenticar("carlos@ouvidoria.gov.br", "hash_seguro_aqui")
    print(f"\nAutenticação: {'sucesso' if ok else 'falha'}")

    # Fluxo de trabalho
    admin.adicionar_comentario(denuncia, "Caso verificado, indício de corrupção.")
    admin.atualizar_status(denuncia, StatusDenuncia.EM_ANALISE)

    print(f"\nStatus atual: {denuncia.get_status().value}")
    print(f"Histórico: {denuncia.get_historico()}")
    print(f"Comentários internos: {denuncia.get_comentarios()}")
