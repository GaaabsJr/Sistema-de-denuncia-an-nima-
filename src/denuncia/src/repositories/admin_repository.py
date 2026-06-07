"""
repositories/admin_repository.py
Acesso ao banco de dados para administradores.
"""

from src.models.database import get_connection


class AdminRepository:

    def buscar_por_email(self, email):
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM administrador WHERE email = ? AND ativo = 1", (email,)
        ).fetchone()
        conn.close()
        return dict(row) if row else None

    def buscar_por_id(self, admin_id):
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM administrador WHERE id = ?", (admin_id,)
        ).fetchone()
        conn.close()
        return dict(row) if row else None
