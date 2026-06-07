"""
services/auth_service.py
Autenticação de administradores (RF-06).
"""

import hashlib
from src.repositories.admin_repository import AdminRepository


class AuthService:

    def __init__(self):
        self._repo = AdminRepository()

    def autenticar(self, email: str, senha: str) -> dict:
        if not email or not senha:
            raise ValueError("E-mail e senha são obrigatórios.")
        admin = self._repo.buscar_por_email(email.strip().lower())
        if not admin:
            raise ValueError("Credenciais inválidas.")
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        if admin["senha_hash"] != senha_hash:
            raise ValueError("Credenciais inválidas.")
        return {
            "id":           admin["id"],
            "nome":         admin["nome"],
            "email":        admin["email"],
            "setor":        admin["setor"],
            "nivel_acesso": admin["nivel_acesso"]
        }
