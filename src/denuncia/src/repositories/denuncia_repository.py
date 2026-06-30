"""
repositories/denuncia_repository.py
Acesso ao banco de dados para denúncias.
"""

from src.models.database import get_connection


class DenunciaRepository:

    def criar(self, protocolo, descricao, categoria, data_registro):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO denuncia (protocolo, descricao, categoria, status, data_registro)
            VALUES (?, ?, ?, 'RECEBIDA', ?)
        """, (protocolo, descricao, categoria, data_registro))
        denuncia_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return denuncia_id

    def buscar_por_protocolo(self, protocolo):
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM denuncia WHERE protocolo = ?", (protocolo,)
        ).fetchone()
        conn.close()
        return dict(row) if row else None

    def listar_todas(self, status=None, categoria=None):
        conn = get_connection()
        query = "SELECT * FROM denuncia WHERE 1=1"
        params = []
        if status:
            query += " AND status = ?"
            params.append(status)
        if categoria:
            query += " AND categoria = ?"
            params.append(categoria)
        query += " ORDER BY data_registro DESC"
        rows = conn.execute(query, params).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def atualizar_status(self, denuncia_id, novo_status):
        conn = get_connection()
        conn.execute(
            "UPDATE denuncia SET status = ? WHERE id = ?",
            (novo_status, denuncia_id)
        )
        conn.commit()
        conn.close()

    def buscar_por_id(self, denuncia_id):
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM denuncia WHERE id = ?", (denuncia_id,)
        ).fetchone()
        conn.close()
        return dict(row) if row else None


class EvidenciaRepository:

    def criar(self, denuncia_id, nome_arquivo, tipo_arquivo, tamanho_bytes, caminho, data_upload):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO evidencia
                (denuncia_id, nome_arquivo, tipo_arquivo, tamanho_bytes, caminho, data_upload)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (denuncia_id, nome_arquivo, tipo_arquivo, tamanho_bytes, caminho, data_upload))
        evidencia_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return evidencia_id

    def listar_por_denuncia(self, denuncia_id):
        conn = get_connection()
        rows = conn.execute("""
            SELECT * FROM evidencia WHERE denuncia_id = ? ORDER BY data_upload ASC
        """, (denuncia_id,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]


class ComentarioRepository:

    def criar(self, denuncia_id, admin_id, texto, data):
        conn = get_connection()
        conn.execute("""
            INSERT INTO comentario_interno (denuncia_id, admin_id, texto, data_registro)
            VALUES (?, ?, ?, ?)
        """, (denuncia_id, admin_id, texto, data))
        conn.commit()
        conn.close()

    def listar_por_denuncia(self, denuncia_id):
        conn = get_connection()
        rows = conn.execute("""
            SELECT c.*, a.nome as admin_nome
            FROM comentario_interno c
            JOIN administrador a ON a.id = c.admin_id
            WHERE c.denuncia_id = ?
            ORDER BY c.data_registro ASC
        """, (denuncia_id,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]


class HistoricoRepository:

    def registrar(self, denuncia_id, status_anterior, status_novo, data, admin_id=None):
        conn = get_connection()
        conn.execute("""
            INSERT INTO historico_status
                (denuncia_id, status_anterior, status_novo, data_alteracao, admin_id)
            VALUES (?, ?, ?, ?, ?)
        """, (denuncia_id, status_anterior, status_novo, data, admin_id))
        conn.commit()
        conn.close()

    def listar_por_denuncia(self, denuncia_id):
        conn = get_connection()
        rows = conn.execute("""
            SELECT h.*, a.nome as admin_nome
            FROM historico_status h
            LEFT JOIN administrador a ON a.id = h.admin_id
            WHERE h.denuncia_id = ?
            ORDER BY h.data_alteracao ASC
        """, (denuncia_id,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]