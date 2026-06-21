"""
tests/conftest.py
Configuração compartilhada entre todos os testes.
Usa banco SQLite em memória para não interferir com o banco real.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import src.models.database as db_module


@pytest.fixture(autouse=True)
def banco_em_memoria(monkeypatch, tmp_path):
    """
    Redireciona o banco para um arquivo temporário antes de cada teste
    e apaga após. Garante isolamento total entre testes.
    """
    db_temp = str(tmp_path / "test.db")
    monkeypatch.setattr(db_module, "DB_PATH", db_temp)
    db_module.init_db()
    yield
    if os.path.exists(db_temp):
        os.remove(db_temp)