// app.js — lógica do frontend do Sistema de Denúncia Anônima

const API = "";

// ── Utilitários ──────────────────────────────────────────────────────────────

function showPage(id) {
  document.querySelectorAll(".page").forEach(p => p.classList.remove("active"));
  const el = document.getElementById(id);
  if (el) el.classList.add("active");
  window.scrollTo(0, 0);
}

function showAlert(el, msg, type = "danger") {
  el.textContent = msg;
  el.className = `alert alert-${type} show`;
  setTimeout(() => el.classList.remove("show"), 6000);
}

function badgeStatus(status) {
  const map = {
    RECEBIDA:    "badge-recebida",
    EM_ANALISE:  "badge-em_analise",
    ENCAMINHADA: "badge-encaminhada",
    ENCERRADA:   "badge-encerrada"
  };
  const label = { RECEBIDA: "Recebida", EM_ANALISE: "Em análise",
                  ENCAMINHADA: "Encaminhada", ENCERRADA: "Encerrada" };
  return `<span class="badge ${map[status] || ''}">${label[status] || status}</span>`;
}

function fmtData(iso) {
  if (!iso) return "—";
  return new Date(iso).toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" });
}

async function api(method, path, body) {
  const opts = { method, headers: { "Content-Type": "application/json" } };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(API + path, opts);
  const json = await res.json();
  return { ok: res.ok, status: res.status, data: json };
}

// ── Navegação ─────────────────────────────────────────────────────────────────

document.addEventListener("DOMContentLoaded", () => {
  showPage("home");
  verificarSessao();
});

function irPara(pagina) {
  showPage(pagina);
  if (pagina === "admin-painel") carregarDenuncias();
}

// ── HOME ─────────────────────────────────────────────────────────────────────

// ── REGISTRAR DENÚNCIA ───────────────────────────────────────────────────────

const formDenuncia = document.getElementById("form-denuncia");
const alertDenuncia = document.getElementById("alert-denuncia");
const resultadoDenuncia = document.getElementById("resultado-denuncia");

if (formDenuncia) {
  formDenuncia.addEventListener("submit", async (e) => {
    e.preventDefault();
    const btn = formDenuncia.querySelector("button[type=submit]");
    btn.disabled = true;
    btn.textContent = "Enviando...";

    const { ok, data } = await api("POST", "/api/denuncia/", {
      descricao: document.getElementById("descricao").value,
      categoria: document.getElementById("categoria").value
    });

    btn.disabled = false;
    btn.textContent = "Enviar denúncia";

    if (ok) {
      formDenuncia.reset();
      document.getElementById("protocolo-gerado").textContent = data.protocolo;
      resultadoDenuncia.classList.remove("d-none");
      resultadoDenuncia.style.display = "block";
      showAlert(alertDenuncia, "Denúncia registrada com sucesso!", "success");
    } else {
      showAlert(alertDenuncia, data.erro || "Erro ao registrar.");
    }
  });
}

// ── CONSULTAR PROTOCOLO ──────────────────────────────────────────────────────

const formProtocolo = document.getElementById("form-protocolo");
const alertProtocolo = document.getElementById("alert-protocolo");
const resultadoConsulta = document.getElementById("resultado-consulta");

if (formProtocolo) {
  formProtocolo.addEventListener("submit", async (e) => {
    e.preventDefault();
    const codigo = document.getElementById("codigo-protocolo").value.trim().toUpperCase();
    if (!codigo) return;

    const { ok, data } = await api("GET", `/api/denuncia/protocolo/${codigo}`);

    if (ok) {
      resultadoConsulta.style.display = "block";
      document.getElementById("consulta-protocolo").textContent = data.protocolo;
      document.getElementById("consulta-categoria").textContent = data.categoria;
      document.getElementById("consulta-data").textContent = fmtData(data.data_registro);
      document.getElementById("consulta-status").innerHTML = badgeStatus(data.status);

      const hist = document.getElementById("consulta-historico");
      hist.innerHTML = (data.historico || []).map(h => `
        <div class="historico-item">
          <div class="historico-dot"></div>
          <div>
            <strong>${h.status_anterior} → ${h.status_novo}</strong>
            <div class="historico-data">${fmtData(h.data_alteracao)}</div>
          </div>
        </div>
      `).join("") || "<p class='text-muted'>Nenhum histórico.</p>";
    } else {
      resultadoConsulta.style.display = "none";
      showAlert(alertProtocolo, data.erro || "Protocolo não encontrado.");
    }
  });
}

// ── LOGIN ADMIN ───────────────────────────────────────────────────────────────

const formLogin = document.getElementById("form-login");
const alertLogin = document.getElementById("alert-login");

if (formLogin) {
  formLogin.addEventListener("submit", async (e) => {
    e.preventDefault();
    const { ok, data } = await api("POST", "/api/admin/login", {
      email: document.getElementById("email").value,
      senha: document.getElementById("senha").value
    });

    if (ok) {
      document.getElementById("admin-nome-header").textContent = data.admin.nome;
      irPara("admin-painel");
    } else {
      showAlert(alertLogin, data.erro || "Credenciais inválidas.");
    }
  });
}

async function verificarSessao() {
  const { ok, data } = await api("GET", "/api/admin/me");
  if (ok) {
    document.getElementById("admin-nome-header").textContent = data.admin_nome;
  }
}

async function logout() {
  await api("POST", "/api/admin/logout");
  showPage("home");
}

// ── PAINEL ADMIN ──────────────────────────────────────────────────────────────

async function carregarDenuncias() {
  const statusFiltro = document.getElementById("filtro-status")?.value || "";
  const catFiltro    = document.getElementById("filtro-cat")?.value || "";

  let url = "/api/admin/denuncias?";
  if (statusFiltro) url += `status=${statusFiltro}&`;
  if (catFiltro)    url += `categoria=${catFiltro}&`;

  const { ok, data } = await api("GET", url);
  const tbody = document.getElementById("tabela-denuncias");
  if (!tbody) return;

  if (!ok || !data.length) {
    tbody.innerHTML = `<tr><td colspan="5" class="text-muted" style="text-align:center;padding:2rem">
      Nenhuma denúncia encontrada.</td></tr>`;
    return;
  }

  tbody.innerHTML = data.map(d => `
    <tr>
      <td><code>${d.protocolo}</code></td>
      <td>${d.categoria}</td>
      <td>${badgeStatus(d.status)}</td>
      <td>${fmtData(d.data_registro)}</td>
      <td>
        <button class="btn btn-ghost btn-sm" onclick="abrirDetalhe(${d.id})">
          Ver detalhes
        </button>
      </td>
    </tr>
  `).join("");
}

async function abrirDetalhe(id) {
  const { ok, data } = await api("GET", `/api/admin/denuncias/${id}`);
  if (!ok) return alert("Erro ao carregar denúncia.");

  document.getElementById("modal-protocolo").textContent = data.protocolo;
  document.getElementById("modal-categoria").textContent = data.categoria;
  document.getElementById("modal-status").innerHTML = badgeStatus(data.status);
  document.getElementById("modal-data").textContent = fmtData(data.data_registro);
  document.getElementById("modal-descricao").textContent = data.descricao;
  document.getElementById("modal-id").value = id;
  document.getElementById("modal-status-atual").textContent = data.status;

  // histórico
  document.getElementById("modal-historico").innerHTML =
    (data.historico || []).map(h => `
      <div class="historico-item">
        <div class="historico-dot"></div>
        <div>
          <strong>${h.status_anterior} → ${h.status_novo}</strong>
          ${h.admin_nome ? `<span class="text-muted"> · ${h.admin_nome}</span>` : ""}
          <div class="historico-data">${fmtData(h.data_alteracao)}</div>
        </div>
      </div>
    `).join("") || "<p class='text-muted'>Sem histórico.</p>";

  // comentários internos
  document.getElementById("modal-comentarios").innerHTML =
    (data.comentarios || []).map(c => `
      <div style="padding:.5rem 0; border-bottom:1px solid var(--border); font-size:.83rem;">
        <strong>${c.admin_nome}</strong>
        <span class="text-muted"> · ${fmtData(c.data_registro)}</span>
        <p style="margin-top:.25rem">${c.texto}</p>
      </div>
    `).join("") || "<p class='text-muted'>Nenhum comentário.</p>";

  document.getElementById("modal-detalhe").classList.add("show");
}

function fecharModal() {
  document.getElementById("modal-detalhe").classList.remove("show");
}

async function atualizarStatus() {
  const id        = document.getElementById("modal-id").value;
  const novoStatus = document.getElementById("novo-status").value;
  if (!novoStatus) return alert("Selecione um status.");

  const { ok, data } = await api("PATCH", `/api/admin/denuncias/${id}/status`, {
    status: novoStatus
  });

  if (ok) {
    fecharModal();
    carregarDenuncias();
  } else {
    alert(data.erro || "Erro ao atualizar.");
  }
}

async function enviarComentario() {
  const id    = document.getElementById("modal-id").value;
  const texto = document.getElementById("novo-comentario").value.trim();
  if (!texto) return alert("Digite um comentário.");

  const { ok, data } = await api("POST", `/api/admin/denuncias/${id}/comentario`, {
    texto
  });

  if (ok) {
    document.getElementById("novo-comentario").value = "";
    abrirDetalhe(parseInt(id));
  } else {
    alert(data.erro || "Erro ao comentar.");
  }
}

async function copiarProtocolo() {
  const codigo = document.getElementById("protocolo-gerado").textContent.trim();
  const btn = document.getElementById("btn-copiar");
  try {
    await navigator.clipboard.writeText(codigo);
    btn.textContent = " Copiado!";
    setTimeout(() => { btn.textContent = " Copiar código"; }, 2500);
  } catch {
    // fallback para navegadores sem suporte ao clipboard
    const input = document.createElement("input");
    input.value = codigo;
    document.body.appendChild(input);
    input.select();
    document.execCommand("copy");
    document.body.removeChild(input);
    btn.textContent = " Copiado!";
    setTimeout(() => { btn.textContent = "Copiar código"; }, 2500);
  }
}