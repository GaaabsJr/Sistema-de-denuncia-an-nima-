"""
tests/test_denuncia_service.py
Testes unitários do DenunciaService — regras de negócio das denúncias.

Cobre:
  - Registro de denúncia válida
  - Geração de protocolo único
  - Rejeição de descrição curta
  - Rejeição de categoria inválida
  - Consulta por protocolo existente
  - Consulta por protocolo inexistente
  - Listagem de denúncias
  - Atualização de status com transição válida
  - Rejeição de transição de status inválida
  - Adição de comentário interno
  - Rejeição de comentário vazio
"""

import pytest
from src.services.denuncia_service import DenunciaService


@pytest.fixture
def service():
    return DenunciaService()


# ── Registro ──────────────────────────────────────────────────────────────────

def test_registrar_denuncia_valida(service):
    """RF-01, RF-02: deve registrar denúncia anônima com categoria válida."""
    resultado = service.registrar(
        descricao="Servidor público exigiu propina para emitir documento.",
        categoria="CORRUPCAO"
    )
    assert "protocolo" in resultado
    assert resultado["protocolo"].startswith("DEN-")
    assert len(resultado["protocolo"]) == 12  # DEN- + 8 chars


def test_protocolo_gerado_e_unico(service):
    """RF-04: cada denúncia deve receber um protocolo único."""
    r1 = service.registrar("Primeira denúncia de teste aqui.", "ASSEDIO")
    r2 = service.registrar("Segunda denúncia de teste aqui.", "VIOLENCIA")
    assert r1["protocolo"] != r2["protocolo"]


def test_registrar_rejeita_descricao_curta(service):
    """RN-02: descrição deve ter pelo menos 10 caracteres."""
    with pytest.raises(ValueError, match="10 caracteres"):
        service.registrar(descricao="Curta", categoria="OUTROS")


def test_registrar_rejeita_descricao_vazia(service):
    """RN-02: descrição não pode ser vazia."""
    with pytest.raises(ValueError):
        service.registrar(descricao="", categoria="OUTROS")


def test_registrar_rejeita_categoria_invalida(service):
    """RN-02: categoria deve pertencer ao conjunto definido."""
    with pytest.raises(ValueError, match="Categoria inválida"):
        service.registrar(
            descricao="Descrição com tamanho suficiente para o teste.",
            categoria="CATEGORIA_INEXISTENTE"
        )


def test_registrar_aceita_todas_categorias(service):
    """RF-02: todas as categorias válidas devem ser aceitas."""
    categorias = ["CORRUPCAO", "ASSEDIO", "VIOLENCIA", "IRREGULARIDADE", "OUTROS"]
    for cat in categorias:
        r = service.registrar(f"Denúncia de teste para categoria {cat}.", cat)
        assert "protocolo" in r


# ── Consulta por protocolo ────────────────────────────────────────────────────

def test_consultar_protocolo_existente(service):
    """RF-05: deve retornar status e histórico para protocolo válido."""
    r = service.registrar("Denúncia para consulta de protocolo.", "CORRUPCAO")
    resultado = service.consultar_por_protocolo(r["protocolo"])

    assert resultado["protocolo"] == r["protocolo"]
    assert resultado["status"] == "RECEBIDA"
    assert resultado["categoria"] == "CORRUPCAO"
    assert "historico" in resultado


def test_consultar_protocolo_inexistente(service):
    """RF-05: deve lançar erro para protocolo não encontrado."""
    with pytest.raises(ValueError, match="não encontrado"):
        service.consultar_por_protocolo("DEN-00000000")


def test_consultar_ignora_case(service):
    """RF-05: consulta deve funcionar com letras minúsculas."""
    r = service.registrar("Denúncia para teste de case insensitive.", "OUTROS")
    protocolo_lower = r["protocolo"].lower()
    resultado = service.consultar_por_protocolo(protocolo_lower)
    assert resultado["protocolo"] == r["protocolo"]


# ── Listagem ──────────────────────────────────────────────────────────────────

def test_listar_todas_denuncias(service):
    """RF-08: deve retornar todas as denúncias registradas."""
    service.registrar("Primeira denúncia para listagem total.", "CORRUPCAO")
    service.registrar("Segunda denúncia para listagem total.", "ASSEDIO")
    lista = service.listar()
    assert len(lista) == 2


def test_listar_filtrar_por_categoria(service):
    """RF-10: deve filtrar denúncias por categoria."""
    service.registrar("Denúncia de corrupção para filtro.", "CORRUPCAO")
    service.registrar("Denúncia de assédio para filtro.", "ASSEDIO")
    lista = service.listar(categoria="CORRUPCAO")
    assert len(lista) == 1
    assert lista[0]["categoria"] == "CORRUPCAO"


def test_listar_filtrar_por_status(service):
    """RF-10: deve filtrar denúncias por status."""
    service.registrar("Denúncia para filtro de status.", "VIOLENCIA")
    lista_recebidas = service.listar(status="RECEBIDA")
    lista_analise   = service.listar(status="EM_ANALISE")
    assert len(lista_recebidas) == 1
    assert len(lista_analise)   == 0


# ── Atualização de status ─────────────────────────────────────────────────────

def test_atualizar_status_valido(service):
    """RF-11: deve atualizar status com transição permitida."""
    r = service.registrar("Denúncia para atualização de status.", "CORRUPCAO")
    d = service.listar()[0]
    service.atualizar_status(d["id"], "EM_ANALISE", admin_id=1)

    resultado = service.consultar_por_protocolo(r["protocolo"])
    assert resultado["status"] == "EM_ANALISE"


def test_atualizar_status_registra_historico(service):
    """RN-06: atualização deve registrar histórico com status anterior e novo."""
    r = service.registrar("Denúncia para histórico de status.", "ASSEDIO")
    d = service.listar()[0]
    service.atualizar_status(d["id"], "EM_ANALISE", admin_id=1)

    resultado = service.consultar_por_protocolo(r["protocolo"])
    transicoes = [(h["status_anterior"], h["status_novo"]) for h in resultado["historico"]]
    assert ("RECEBIDA", "EM_ANALISE") in transicoes


def test_atualizar_status_transicao_invalida(service):
    """RN-08: não deve permitir transições de status inválidas."""
    service.registrar("Denúncia para transição inválida de status.", "OUTROS")
    d = service.listar()[0]

    with pytest.raises(ValueError, match="Transição inválida"):
        # RECEBIDA não pode ir direto para ENCAMINHADA
        service.atualizar_status(d["id"], "ENCAMINHADA", admin_id=1)


def test_atualizar_status_denuncia_inexistente(service):
    """RF-11: deve lançar erro para denúncia inexistente."""
    with pytest.raises(ValueError, match="não encontrada"):
        service.atualizar_status(9999, "EM_ANALISE", admin_id=1)


def test_denuncia_encerrada_nao_pode_reabrir(service):
    """RN-08: denúncia encerrada não deve aceitar novos status sem permissão explícita."""
    service.registrar("Denúncia para encerramento e tentativa de reabertura.", "CORRUPCAO")
    d = service.listar()[0]
    service.atualizar_status(d["id"], "EM_ANALISE", admin_id=1)
    service.atualizar_status(d["id"], "ENCERRADA", admin_id=1)

    with pytest.raises(ValueError, match="Transição inválida"):
        service.atualizar_status(d["id"], "EM_ANALISE", admin_id=1)


# ── Comentários internos ──────────────────────────────────────────────────────

def test_adicionar_comentario_interno(service):
    """RF-12: deve salvar comentário interno vinculado à denúncia."""
    service.registrar("Denúncia para comentário interno.", "IRREGULARIDADE")
    d = service.listar()[0]
    service.adicionar_comentario(d["id"], admin_id=1, texto="Caso verificado, encaminhar.")

    detalhes = service.buscar_detalhes(d["id"])
    assert len(detalhes["comentarios"]) == 1
    assert detalhes["comentarios"][0]["texto"] == "Caso verificado, encaminhar."


def test_comentario_vazio_rejeitado(service):
    """RF-12: comentário não pode ser vazio."""
    service.registrar("Denúncia para rejeição de comentário vazio.", "OUTROS")
    d = service.listar()[0]

    with pytest.raises(ValueError):
        service.adicionar_comentario(d["id"], admin_id=1, texto="")


def test_comentario_nao_visivel_na_consulta_publica(service):
    """RN-04: comentários internos não devem aparecer na consulta por protocolo."""
    r = service.registrar("Denúncia para verificar privacidade do comentário.", "ASSEDIO")
    d = service.listar()[0]
    service.adicionar_comentario(d["id"], admin_id=1, texto="Comentário confidencial.")

    consulta = service.consultar_por_protocolo(r["protocolo"])
    # consulta pública não expõe comentários
    assert "comentarios" not in consulta


# ── Anexo de evidências (US-03 / RF-03) ─────────────────────────────────────────
# Escritos ANTES da implementação de validar_evidencia() — ciclo TDD (vermelho → verde).

def test_validar_evidencia_formato_aceito(service):
    """RF-03: deve aceitar arquivos com extensão de imagem, documento ou vídeo."""
    assert service.validar_evidencia("foto.jpg", tamanho_bytes=2_000_000) is True
    assert service.validar_evidencia("laudo.pdf", tamanho_bytes=2_000_000) is True
    assert service.validar_evidencia("video.mp4", tamanho_bytes=2_000_000) is True


def test_validar_evidencia_formato_rejeitado(service):
    """RF-03: deve rejeitar extensões fora da lista permitida."""
    with pytest.raises(ValueError, match="formato"):
        service.validar_evidencia("script.exe", tamanho_bytes=1_000)


def test_validar_evidencia_tamanho_maximo_excedido(service):
    """US-03: deve informar claramente o tamanho máximo aceito (10MB)."""
    onze_mb = 11 * 1024 * 1024
    with pytest.raises(ValueError, match="tamanho"):
        service.validar_evidencia("foto.jpg", tamanho_bytes=onze_mb)


# ── Anexar evidência a uma denúncia existente (US-03 / RF-03) ───────────────────
# Escritos ANTES da implementação de anexar_evidencia() — ciclo TDD (vermelho → verde).

def test_anexar_evidencia_sucesso(service, monkeypatch, tmp_path):
    import src.services.denuncia_service as service_module
    monkeypatch.setattr(service_module, "UPLOAD_DIR", str(tmp_path))

    r = service.registrar("Denúncia com evidência anexada em seguida.", "OUTROS")
    resultado = service.anexar_evidencia(r["protocolo"], "foto.jpg", b"conteudo-fake-da-imagem")

    assert resultado["nome_arquivo"] == "foto.jpg"
    assert resultado["tamanho_bytes"] == len(b"conteudo-fake-da-imagem")

    consulta = service.consultar_por_protocolo(r["protocolo"])
    assert len(consulta["evidencias"]) == 1
    assert consulta["evidencias"][0]["nome_arquivo"] == "foto.jpg"


def test_anexar_evidencia_protocolo_inexistente(service, monkeypatch, tmp_path):
    import src.services.denuncia_service as service_module
    monkeypatch.setattr(service_module, "UPLOAD_DIR", str(tmp_path))

    with pytest.raises(ValueError, match="Protocolo não encontrado"):
        service.anexar_evidencia("DEN-00000000", "foto.jpg", b"conteudo")


def test_anexar_evidencia_formato_invalido_nao_grava_arquivo(service, monkeypatch, tmp_path):
    import src.services.denuncia_service as service_module
    monkeypatch.setattr(service_module, "UPLOAD_DIR", str(tmp_path))

    r = service.registrar("Denúncia para testar rejeição de formato.", "OUTROS")
    with pytest.raises(ValueError, match="formato"):
        service.anexar_evidencia(r["protocolo"], "virus.exe", b"conteudo")

    consulta = service.consultar_por_protocolo(r["protocolo"])
    assert len(consulta["evidencias"]) == 0