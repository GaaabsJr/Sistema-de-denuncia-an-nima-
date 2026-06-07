"""
models/database.py
Configuração do banco SQLite e definição das tabelas.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "denuncia.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS denuncia (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            protocolo       TEXT    NOT NULL UNIQUE,
            descricao       TEXT    NOT NULL,
            categoria       TEXT    NOT NULL,
            status          TEXT    NOT NULL DEFAULT 'RECEBIDA',
            data_registro   TEXT    NOT NULL
        );

        CREATE TABLE IF NOT EXISTS evidencia (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            denuncia_id     INTEGER NOT NULL REFERENCES denuncia(id),
            nome_arquivo    TEXT    NOT NULL,
            tipo_arquivo    TEXT    NOT NULL,
            caminho         TEXT    NOT NULL,
            data_upload     TEXT    NOT NULL
        );

        CREATE TABLE IF NOT EXISTS historico_status (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            denuncia_id     INTEGER NOT NULL REFERENCES denuncia(id),
            status_anterior TEXT    NOT NULL,
            status_novo     TEXT    NOT NULL,
            data_alteracao  TEXT    NOT NULL,
            admin_id        INTEGER REFERENCES administrador(id)
        );

        CREATE TABLE IF NOT EXISTS comentario_interno (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            denuncia_id     INTEGER NOT NULL REFERENCES denuncia(id),
            admin_id        INTEGER NOT NULL REFERENCES administrador(id),
            texto           TEXT    NOT NULL,
            data_registro   TEXT    NOT NULL
        );

        CREATE TABLE IF NOT EXISTS administrador (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            nome            TEXT    NOT NULL,
            email           TEXT    NOT NULL UNIQUE,
            senha_hash      TEXT    NOT NULL,
            matricula       TEXT    NOT NULL UNIQUE,
            setor           TEXT    NOT NULL,
            nivel_acesso    TEXT    NOT NULL DEFAULT 'OPERADOR',
            ativo           INTEGER NOT NULL DEFAULT 1
        );
    """)

    # Admin padrão para demo
    cursor.execute(
        "SELECT id FROM administrador WHERE email = ?", ("admin@sistema.gov.br",)
    )
    if not cursor.fetchone():
        import hashlib
        senha = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute("""
            INSERT INTO administrador (nome, email, senha_hash, matricula, setor, nivel_acesso)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ("Administrador Padrão", "admin@sistema.gov.br", senha,
              "ADM-001", "Ouvidoria", "SUPERVISOR"))

    conn.commit()
    conn.close()
