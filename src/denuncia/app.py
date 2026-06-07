"""
app.py — ponto de entrada da aplicação Flask
Sistema de Denúncia Anônima · CC0116 UNIFAP 2026.1
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, render_template
from src.models.database import init_db
from src.controllers.denuncia_controller import bp as denuncia_bp
from src.controllers.admin_controller import bp as admin_bp

app = Flask(__name__,
            template_folder="templates",
            static_folder="static")

app.secret_key = "denuncia-anonima-unifap-2026-dev"


# ── Blueprints ────────────────────────────────────────────────────────────────
app.register_blueprint(denuncia_bp)
app.register_blueprint(admin_bp)


# ── Rota principal (SPA) ──────────────────────────────────────────────────────
@app.get("/")
def index():
    return render_template("index.html")


# ── Inicialização ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    init_db()
    print("\n✅ Sistema de Denúncia Anônima rodando em http://localhost:5000")
    print("   Admin de demo: admin@sistema.gov.br / admin123\n")
    app.run(debug=True, port=5000)
