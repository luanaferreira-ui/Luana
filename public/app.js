'use strict';

/* Painel de Demandas — SPA vanilla. Carrega estado via GET /api/state e
 * redesenha sempre a partir da resposta do servidor (fonte de verdade). */

let S = { corte: '2026-07-01', clusters: [], demandas: [] };
const ui = { escopo: 'todas', cluster: null, conta: '', q: '', agrupar: 'cluster', mostrarConcluidas: false };

const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

function el(tag, cls, text) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text != null) e.textContent = text;
  return e;
}

function norm(s) {
  return String(s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
}

/* ---------- datas (dia-calendário local) ---------- */
function hoje() { const d = new Date(); d.setHours(0, 0, 0, 0); return d; }
function parseData(s) { if (!s) return null; const [y, m, dd] = s.split('-').map(Number); return new Date(y, m - 1, dd); }
function diasAte(s) { const p = parseData(s); if (!p) return null; return Math.round((p - hoje()) / 86400000); }
function isAtrasada(d) { if (d.status === 'feito' || !d.prazo) return false; return parseData(d.prazo) < hoje(); }
function dentro7(d) { if (!d.prazo) return false; const n = diasAte(d.prazo); return n >= 0 && n <= 7; }

function ehMinha(d) { return norm(d.responsavel).startsWith('luana'); }

/* ---------- API ---------- */
async function carregar() {
  const r = await fetch('/api/state');
  S = await r.json();
  render(true);
}
async function api(method, path, body) {
  const r = await fetch(path, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined,
  });
  const j = await r.json();
  if (j && j.ok === false && j.erro) toast(j.erro);
  return j;
}
function aplicar(res) { if (res && Array.isArray(res.demandas)) { S.demandas = res.demandas; render(); } }

const patch = (id, body) => api('PATCH', '/api/demanda/' + encodeURIComponent(id), body).then(aplicar);
const remover = (id) => api('DELETE', '/api/demanda/' + encodeURIComponent(id)).then(aplicar);

/* ---------- filtros / ordenação / agrupamento ---------- */
function passaFiltros(d) {
  if (ui.cluster && d.cluster !== ui.cluster) return false;
  if (ui.conta && d.conta !== ui.conta) return false;
  if (ui.escopo === 'minhas' && !ehMinha(d)) return false;
  if (ui.escopo === 'cobrar' && ehMinha(d)) return false;
  if (ui.q) {
    const hay = norm([d.titulo, d.conta, d.responsavel, d.origem].join(' '));
    if (!hay.includes(norm(ui.q))) return false;
  }
  return true;
}
function abertasVisiveis() {
  return S.demandas.filter((d) => d.status !== 'feito').filter(passaFiltros);
}
function ordenar(arr) {
  return arr.slice().sort((a, b) => {
    const u = (b.urgente ? 1 : 0) - (a.urgente ? 1 : 0);
    if (u) return u;
    const pa = a.prazo || '9999-99-99', pb = b.prazo || '9999-99-99';
    return pa < pb ? -1 : pa > pb ? 1 : 0;
  });
}
function agrupar(arr) {
  if (ui.agrupar === 'cluster') {
    return S.clusters
      .map((c) => ({ nome: c.nome, itens: ordenar(arr.filter((d) => d.cluster === c.id)) }))
      .filter((g) => g.itens.length);
  }
  if (ui.agrupar === 'conta') {
    const contas = [...new Set(arr.map((d) => d.conta))].sort((a, b) => a.localeCompare(b, 'pt'));
    return contas.map((c) => ({ nome: c, itens: ordenar(arr.filter((d) => d.conta === c)) }));
  }
  // por prazo
  const buckets = [
    { nome: 'Atrasadas', test: (d) => isAtrasada(d) },
    { nome: 'Hoje e amanhã', test: (d) => { const n = diasAte(d.prazo); return n === 0 || n === 1; } },
    { nome: 'Esta semana', test: (d) => { const n = diasAte(d.prazo); return n > 1 && n <= 7; } },
    { nome: 'Depois', test: (d) => { const n = diasAte(d.prazo); return n != null && n > 7; } },
    { nome: 'Sem prazo', test: (d) => !d.prazo },
  ];
  return buckets
    .map((b) => ({ nome: b.nome, itens: ordenar(arr.filter(b.test)) }))
    .filter((g) => g.itens.length);
}

/* ---------- render ---------- */
function render(rebuildSelects) {
  renderCounters();
  renderCarne();
  if (rebuildSelects) renderContaSelect();
  renderSegs();
  renderLista();
  renderConcluidas();
}

function counter(label, val, mod) {
  const c = el('div', 'counter' + (mod ? ' ' + mod : ''));
  c.append(el('span', 'c-num', String(val)));
  c.append(el('span', 'c-lab', label));
  return c;
}
function renderCounters() {
  const nf = S.demandas.filter((d) => d.status !== 'feito');
  const atrasadas = nf.filter(isAtrasada).length;
  const venc = nf.filter((d) => !isAtrasada(d) && dentro7(d)).length;
  const feito = S.demandas.filter((d) => d.status === 'feito').length;
  const host = $('#counters'); host.innerHTML = '';
  host.append(counter('Abertas', nf.length));
  host.append(counter('Atrasadas', atrasadas, 'atras'));
  host.append(counter('Vencendo 7d', venc));
  host.append(counter('Concluídas', feito, 'ok'));
  $('#corteInfo').textContent = 'corte ' + S.corte + (S.atualizado_em ? ' · atualizado ' + S.atualizado_em : '');
}

function renderCarne() {
  const host = $('#carne'); host.innerHTML = '';
  for (const c of S.clusters) {
    const itens = S.demandas.filter((d) => d.cluster === c.id);
    const abertas = itens.filter((d) => d.status !== 'feito').length;
    const feito = itens.filter((d) => d.status === 'feito').length;
    const total = itens.length;
    const overdue = itens.some(isAtrasada);
    const ativo = ui.cluster === c.id;
    const f = el('button', 'ficha' + (ativo ? ' on' : '') + (overdue ? ' atras' : ''));
    f.type = 'button';
    f.setAttribute('aria-pressed', ativo ? 'true' : 'false');
    if (c.hint) f.title = c.hint;
    f.append(el('span', 'ficha-nome', c.nome));
    f.append(el('span', 'ficha-num', abertas + '/' + total));
    const bar = el('div', 'bar'); const fill = el('div', 'bar-fill');
    fill.style.width = (total ? Math.round((feito / total) * 100) : 0) + '%';
    bar.append(fill); f.append(bar);
    f.addEventListener('click', () => { ui.cluster = ativo ? null : c.id; render(); });
    host.append(f);
  }
}

function renderContaSelect() {
  const sel = $('#conta');
  const contas = [...new Set(S.demandas.map((d) => d.conta))].sort((a, b) => a.localeCompare(b, 'pt'));
  sel.innerHTML = '';
  const opt0 = el('option', null, 'Todas as contas'); opt0.value = '';
  sel.append(opt0);
  for (const c of contas) { const o = el('option', null, c); o.value = c; sel.append(o); }
  sel.value = ui.conta;
}

function renderSegs() {
  for (const b of $$('#escopo button')) b.setAttribute('aria-pressed', b.dataset.v === ui.escopo ? 'true' : 'false');
  for (const b of $$('#agrupar button')) b.setAttribute('aria-pressed', b.dataset.v === ui.agrupar ? 'true' : 'false');
}

function tag(cls, text) { return el('span', 'tag ' + cls, text); }

function linha(d) {
  const atras = isAtrasada(d);
  const row = el('article', 'row' + (atras ? ' atrasada' : '') + (d.status === 'aguardando' ? ' aguardando' : ''));
  row.dataset.id = d.id;

  // checkbox
  const cb = el('span', 'cb');
  cb.setAttribute('role', 'checkbox');
  cb.setAttribute('aria-checked', 'false');
  cb.setAttribute('aria-label', 'Concluir demanda');
  cb.tabIndex = 0;
  const concluir = () => patch(d.id, { status: 'feito' });
  cb.addEventListener('click', concluir);
  cb.addEventListener('keydown', (e) => { if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); concluir(); } });
  row.append(cb);

  // corpo
  const body = el('div', 'row-body');
  const titulo = el('div', 'titulo', d.titulo);
  titulo.contentEditable = 'true';
  titulo.spellcheck = false;
  titulo.setAttribute('role', 'textbox');
  titulo.setAttribute('aria-label', 'Título (editável)');
  titulo.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') { e.preventDefault(); titulo.blur(); }
    if (e.key === 'Escape') { titulo.textContent = d.titulo; titulo.blur(); }
  });
  titulo.addEventListener('blur', () => {
    const t = titulo.textContent.trim();
    if (t && t !== d.titulo) patch(d.id, { titulo: t });
    else titulo.textContent = d.titulo;
  });
  body.append(titulo);

  const meta = el('div', 'meta');
  meta.append(tag('conta', d.conta));
  meta.append(tag('resp' + (ehMinha(d) ? ' me' : ''), d.responsavel));
  const prazo = el('label', 'prazo' + (atras ? ' atras' : ''));
  const di = document.createElement('input');
  di.type = 'date';
  di.value = d.prazo || '';
  di.setAttribute('aria-label', 'Prazo');
  di.addEventListener('change', () => patch(d.id, { prazo: di.value || null }));
  di.addEventListener('click', () => { if (di.showPicker) { try { di.showPicker(); } catch { /* ok */ } } });
  prazo.append(di);
  if (atras) prazo.append(el('span', 'atraso-tag', 'atrasada'));
  meta.append(prazo);
  body.append(meta);

  if (d.origem) body.append(el('div', 'origem', d.origem));
  row.append(body);

  // ações
  const acts = el('div', 'acts');
  const bWait = el('button', 'act', d.status === 'aguardando' ? '↩ retomar' : '⏸ aguardando');
  bWait.type = 'button';
  bWait.title = 'Aguardando terceiro (travada em alguém)';
  bWait.addEventListener('click', () => patch(d.id, { status: d.status === 'aguardando' ? 'aberto' : 'aguardando' }));
  const bDel = el('button', 'act del', 'remover');
  bDel.type = 'button';
  bDel.addEventListener('click', () => { if (confirm('Remover “' + d.titulo + '”?')) remover(d.id); });
  acts.append(bWait, bDel);
  row.append(acts);

  return row;
}

function renderLista() {
  const host = $('#lista'); host.innerHTML = '';
  const abertas = abertasVisiveis();
  if (!abertas.length) { host.append(el('p', 'vazio', 'Nada por aqui com esses filtros.')); return; }
  for (const g of agrupar(abertas)) {
    const sec = el('section', 'grupo');
    const h = el('h2', 'grupo-h');
    h.append(el('span', 'grupo-nome', g.nome));
    h.append(el('span', 'grupo-cont', g.itens.length + (g.itens.length === 1 ? ' item' : ' itens')));
    sec.append(h);
    for (const d of g.itens) sec.append(linha(d));
    host.append(sec);
  }
}

function renderConcluidas() {
  const done = S.demandas.filter((d) => d.status === 'feito');
  $('#btnConcluidas').textContent = 'Concluídas (' + done.length + ')';
  const wrap = $('#doneWrap');
  wrap.hidden = !ui.mostrarConcluidas;
  if (!ui.mostrarConcluidas) return;
  const host = $('#doneList'); host.innerHTML = '';
  if (!done.length) { host.append(el('p', 'vazio', 'Nenhuma concluída ainda.')); return; }
  for (const d of ordenar(done)) {
    const row = el('div', 'row done');
    const cb = el('span', 'cb on');
    cb.setAttribute('role', 'checkbox');
    cb.setAttribute('aria-checked', 'true');
    cb.setAttribute('aria-label', 'Reabrir demanda');
    cb.tabIndex = 0;
    const reabrir = () => patch(d.id, { status: 'aberto' });
    cb.addEventListener('click', reabrir);
    cb.addEventListener('keydown', (e) => { if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); reabrir(); } });
    const body = el('div', 'row-body');
    body.append(el('div', 'titulo', d.titulo));
    const meta = el('div', 'meta');
    meta.append(tag('conta', d.conta));
    meta.append(tag('resp' + (ehMinha(d) ? ' me' : ''), d.responsavel));
    body.append(meta);
    row.append(cb, body, el('span', 'stamp', 'OK'));
    host.append(row);
  }
}

/* ---------- copiar resumo ---------- */
function copiarResumo() {
  const nf = S.demandas.filter((d) => d.status !== 'feito');
  const porCluster = {};
  for (const d of nf) (porCluster[d.cluster] = porCluster[d.cluster] || []).push(d);
  const out = [];
  for (const c of S.clusters) {
    const arr = porCluster[c.id];
    if (!arr || !arr.length) continue;
    out.push('## ' + c.nome);
    for (const d of ordenar(arr)) {
      out.push(`- [ ] ${d.titulo} — ${d.responsavel} · ${d.conta}${d.prazo ? ' · ' + d.prazo : ''}`);
    }
    out.push('');
  }
  const texto = out.join('\n').trim();
  if (!texto) { toast('Nada aberto para copiar'); return; }
  navigator.clipboard.writeText(texto)
    .then(() => toast('Resumo copiado'))
    .catch(() => toast('Não consegui acessar a área de transferência'));
}

/* ---------- toast ---------- */
let toastT = null;
function toast(msg) {
  const t = $('#toast');
  t.textContent = msg;
  t.hidden = false;
  clearTimeout(toastT);
  toastT = setTimeout(() => { t.hidden = true; }, 1800);
}

/* ---------- wiring ---------- */
function wire() {
  $('#q').addEventListener('input', (e) => { ui.q = e.target.value; renderLista(); });
  $('#conta').addEventListener('change', (e) => { ui.conta = e.target.value; render(); });
  for (const b of $$('#escopo button')) b.addEventListener('click', () => { ui.escopo = b.dataset.v; render(); });
  for (const b of $$('#agrupar button')) b.addEventListener('click', () => { ui.agrupar = b.dataset.v; render(); });

  $('#btnCopiar').addEventListener('click', copiarResumo);
  $('#btnConcluidas').addEventListener('click', () => { ui.mostrarConcluidas = !ui.mostrarConcluidas; renderConcluidas(); });

  // importar
  const dlgI = $('#dlgImportar');
  $('#btnImportar').addEventListener('click', () => { $('#impReport').textContent = ''; dlgI.showModal(); });
  $('#impFechar').addEventListener('click', () => dlgI.close());
  $('#impRun').addEventListener('click', async () => {
    const texto = $('#impText').value;
    if (!texto.trim()) { $('#impReport').textContent = 'Cole ao menos uma linha.'; return; }
    const r = await api('POST', '/api/importar', { texto });
    aplicar(r);
    $('#impReport').textContent =
      `${r.novas} nova(s), ${r.repetidas} repetida(s), ${r.foraDoPeriodo} fora do período, ${r.ignoradas} ignorada(s) por formato.`;
  });

  // nova
  const dlgN = $('#dlgNova');
  $('#btnNova').addEventListener('click', () => {
    const sel = $('#nvCluster'); sel.innerHTML = '';
    for (const c of S.clusters) { const o = el('option', null, c.nome); o.value = c.id; sel.append(o); }
    $('#nvTitulo').value = ''; $('#nvConta').value = ''; $('#nvResp').value = 'Luana'; $('#nvPrazo').value = '';
    $('#nvReport').textContent = '';
    dlgN.showModal();
  });
  $('#nvFechar').addEventListener('click', () => dlgN.close());
  $('#nvRun').addEventListener('click', async () => {
    const body = {
      titulo: $('#nvTitulo').value,
      cluster: $('#nvCluster').value,
      conta: $('#nvConta').value,
      responsavel: $('#nvResp').value,
      prazo: $('#nvPrazo').value || null,
      origem: 'Manual',
    };
    const r = await api('POST', '/api/demanda', body);
    if (r.ok) { aplicar(r); dlgN.close(); toast('Demanda criada'); }
    else $('#nvReport').textContent = r.erro || 'Não deu para criar.';
  });
}

carregar().then(wire);
