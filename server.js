'use strict';

/*
 * Painel de Demandas — servidor local mínimo (node:http, zero dependências).
 *
 * O demandas.json é a fonte de verdade e mora no disco. Este processo mantém
 * uma cópia em memória, mas toda mutação é gravada imediatamente:
 *   1. faz backup do arquivo atual em .backup/ (mantém os 20 mais recentes)
 *   2. escreve num arquivo temporário e faz rename (escrita atômica)
 * Assim, se o processo morrer no meio, o disco nunca fica num estado quebrado.
 */

const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');

const ROOT = __dirname;
const DATA_FILE = path.join(ROOT, 'demandas.json');
const BACKUP_DIR = path.join(ROOT, '.backup');
const PUBLIC_DIR = path.join(ROOT, 'public');
const HOST = '127.0.0.1';
const PORT = 4321;
const MAX_BACKUPS = 20;

const STATUS = ['aberto', 'aguardando', 'feito'];

// --- estado em memória (carregado do disco) ---
let state = loadState();
let backupSeq = 0;

function loadState() {
  const data = JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
  if (!Array.isArray(data.demandas)) data.demandas = [];
  if (!Array.isArray(data.clusters)) data.clusters = [];
  // corte é a constante única de período; vem do JSON. Para mover para agosto,
  // basta editar "corte" no demandas.json — nenhum outro lugar precisa mudar.
  if (!data.corte) data.corte = '2026-07-01';
  if (!data.versao) data.versao = 1;
  return data;
}

function clusterIds() {
  return new Set(state.clusters.map((c) => c.id));
}

function persist() {
  // 1. backup do arquivo atual, se existir
  try {
    if (fs.existsSync(DATA_FILE)) {
      if (!fs.existsSync(BACKUP_DIR)) fs.mkdirSync(BACKUP_DIR, { recursive: true });
      const ts = new Date().toISOString().replace(/[:.]/g, '-');
      const seq = String(backupSeq++).padStart(4, '0');
      const prev = fs.readFileSync(DATA_FILE, 'utf8');
      fs.writeFileSync(path.join(BACKUP_DIR, `demandas-${ts}-${seq}.json`), prev);
      pruneBackups();
    }
  } catch (e) {
    console.error('[backup] falhou (seguindo mesmo assim):', e.message);
  }
  // 2. escrita atômica: tmp + rename
  state.atualizado_em = new Date().toISOString().slice(0, 10);
  const out = JSON.stringify(state, null, 2) + '\n';
  const tmp = path.join(ROOT, `.demandas.${process.pid}.tmp`);
  fs.writeFileSync(tmp, out);
  fs.renameSync(tmp, DATA_FILE);
}

function pruneBackups() {
  const files = fs
    .readdirSync(BACKUP_DIR)
    .filter((f) => f.startsWith('demandas-') && f.endsWith('.json'))
    .sort(); // timestamp ISO com largura fixa -> ordem lexical = cronológica
  while (files.length > MAX_BACKUPS) {
    const old = files.shift();
    try {
      fs.unlinkSync(path.join(BACKUP_DIR, old));
    } catch { /* ignore */ }
  }
}

function nextId() {
  let max = -1;
  for (const d of state.demandas) {
    const m = /^d(\d+)$/.exec(d.id || '');
    if (m) max = Math.max(max, parseInt(m[1], 10));
  }
  return 'd' + String(max + 1).padStart(2, '0');
}

function normalizeTitle(s) {
  return String(s || '')
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '') // tira acentos (marcas combinantes)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, ' ') // tira pontuação
    .trim();
}

function isValidDate(s) {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(s));
  if (!m) return false;
  const y = +m[1], mo = +m[2], da = +m[3];
  if (mo < 1 || mo > 12 || da < 1 || da > 31) return false;
  const dt = new Date(Date.UTC(y, mo - 1, da));
  return dt.getUTCFullYear() === y && dt.getUTCMonth() === mo - 1 && dt.getUTCDate() === da;
}

function publicState() {
  return {
    versao: state.versao,
    corte: state.corte,
    atualizado_em: state.atualizado_em || null,
    clusters: state.clusters,
    demandas: state.demandas,
  };
}

// --- operações ---

function atualizar(id, body) {
  const d = state.demandas.find((x) => x.id === id);
  if (!d) return { ok: false, erro: 'demanda não encontrada' };
  const cids = clusterIds();
  if ('status' in body) {
    if (!STATUS.includes(body.status)) return { ok: false, erro: 'status inválido' };
    d.status = body.status;
  }
  if ('cluster' in body) {
    if (!cids.has(body.cluster)) return { ok: false, erro: 'cluster inválido' };
    d.cluster = body.cluster;
  }
  if ('titulo' in body) {
    const t = String(body.titulo || '').trim();
    if (!t) return { ok: false, erro: 'título vazio' };
    d.titulo = t;
  }
  if ('prazo' in body) {
    const v = body.prazo;
    if (v === null || v === '') d.prazo = null;
    else if (!isValidDate(v)) return { ok: false, erro: 'data inválida' };
    else d.prazo = v; // edição de prazo não aplica corte (só criação/import aplicam)
  }
  if ('urgente' in body) d.urgente = !!body.urgente;
  if ('conta' in body) d.conta = String(body.conta || '').trim() || '—';
  if ('responsavel' in body) d.responsavel = String(body.responsavel || '').trim() || 'Luana';
  persist();
  return { ok: true, demandas: state.demandas };
}

function criar(body) {
  const cids = clusterIds();
  if (!cids.has(body.cluster)) return { ok: false, erro: 'cluster inválido' };
  const titulo = String(body.titulo || '').trim();
  if (!titulo) return { ok: false, erro: 'título vazio' };
  let prazo = null;
  if (body.prazo) {
    if (!isValidDate(body.prazo)) return { ok: false, erro: 'data inválida' };
    if (body.prazo < state.corte) return { ok: false, erro: 'fora do período (anterior ao corte)' };
    prazo = body.prazo;
  }
  const d = {
    id: nextId(),
    titulo,
    cluster: body.cluster,
    conta: String(body.conta || '').trim() || '—',
    responsavel: String(body.responsavel || '').trim() || 'Luana',
    prazo,
    urgente: !!body.urgente,
    status: 'aberto',
    origem: String(body.origem || '').trim() || 'Manual',
  };
  state.demandas.push(d);
  persist();
  return { ok: true, criada: d.id, demandas: state.demandas };
}

function remover(id) {
  const i = state.demandas.findIndex((x) => x.id === id);
  if (i < 0) return { ok: false, erro: 'demanda não encontrada' };
  state.demandas.splice(i, 1);
  persist();
  return { ok: true, demandas: state.demandas };
}

function importar(texto) {
  const cids = clusterIds();
  const linhas = String(texto || '').split(/\r?\n/);
  let novas = 0, repetidas = 0, foraDoPeriodo = 0, ignoradas = 0;
  const vistos = new Set(state.demandas.map((d) => normalizeTitle(d.titulo)));
  const hoje = new Date().toISOString().slice(0, 10);

  for (const linhaRaw of linhas) {
    let s = linhaRaw.trim();
    if (!s) continue;
    // tolera prefixos "- [ ]", "- [x]", "- ", "* "
    s = s.replace(/^[-*]\s*\[[ xX]?\]\s*/, '').replace(/^[-*]\s+/, '').trim();
    if (!s) continue;

    const parts = s.split('|').map((x) => x.trim());
    if (parts.length < 5) { ignoradas++; continue; }

    const cluster = parts[0];
    const conta = parts[1];
    const responsavel = parts[2];
    const dataStr = parts[3];
    const descricao = parts.slice(4).join('|').trim(); // rejunta pipes literais da descrição

    if (!cluster || !cids.has(cluster)) { ignoradas++; continue; }
    if (!descricao) { ignoradas++; continue; }

    let prazo = null;
    if (dataStr) {
      if (!isValidDate(dataStr)) { ignoradas++; continue; }
      prazo = dataStr;
    }
    if (prazo && prazo < state.corte) { foraDoPeriodo++; continue; }

    const key = normalizeTitle(descricao);
    if (vistos.has(key)) { repetidas++; continue; } // não mexe no que já existe
    vistos.add(key);

    state.demandas.push({
      id: nextId(),
      titulo: descricao,
      cluster,
      conta: conta || '—',
      responsavel: responsavel || 'Luana',
      prazo,
      urgente: false,
      status: 'aberto',
      origem: 'Importado ' + hoje,
    });
    novas++;
  }

  if (novas > 0) persist();
  return { ok: true, novas, repetidas, foraDoPeriodo, ignoradas, demandas: state.demandas };
}

// --- HTTP ---

function sendJson(res, code, obj) {
  const buf = Buffer.from(JSON.stringify(obj));
  res.writeHead(code, { 'Content-Type': 'application/json; charset=utf-8', 'Content-Length': buf.length });
  res.end(buf);
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let data = '';
    let size = 0;
    req.on('data', (c) => {
      size += c.length;
      if (size > 5_000_000) { reject(new Error('corpo grande demais')); req.destroy(); return; }
      data += c;
    });
    req.on('end', () => {
      if (!data) return resolve({});
      try { resolve(JSON.parse(data)); } catch { reject(new Error('JSON inválido')); }
    });
    req.on('error', reject);
  });
}

const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
};

function serveStatic(pathname, res) {
  const rel = pathname === '/' ? '/index.html' : decodeURIComponent(pathname);
  const filePath = path.normalize(path.join(PUBLIC_DIR, rel));
  if (!filePath.startsWith(PUBLIC_DIR)) { res.writeHead(403); return res.end('Forbidden'); }
  fs.readFile(filePath, (err, buf) => {
    if (err) { res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' }); return res.end('Não encontrado'); }
    res.writeHead(200, { 'Content-Type': TYPES[path.extname(filePath)] || 'application/octet-stream' });
    res.end(buf);
  });
}

const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, `http://${HOST}:${PORT}`);
    const p = url.pathname;

    if (req.method === 'GET' && p === '/api/state') {
      return sendJson(res, 200, publicState());
    }
    if (req.method === 'POST' && p === '/api/importar') {
      const body = await readBody(req);
      return sendJson(res, 200, importar(body.texto || ''));
    }
    if (req.method === 'POST' && p === '/api/demanda') {
      const body = await readBody(req);
      const r = criar(body);
      return sendJson(res, r.ok ? 201 : 400, r);
    }

    const m = /^\/api\/demanda\/([^/]+)$/.exec(p);
    if (m) {
      const id = decodeURIComponent(m[1]);
      if (req.method === 'PATCH') {
        const body = await readBody(req);
        const r = atualizar(id, body);
        return sendJson(res, r.ok ? 200 : 400, r);
      }
      if (req.method === 'DELETE') {
        const r = remover(id);
        return sendJson(res, r.ok ? 200 : 404, r);
      }
    }

    if (req.method === 'GET') return serveStatic(p, res);

    res.writeHead(405, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('Método não permitido');
  } catch (e) {
    console.error(e);
    sendJson(res, 500, { ok: false, erro: e.message });
  }
});

server.on('error', (e) => {
  if (e.code === 'EADDRINUSE') {
    console.error(`\nA porta ${PORT} já está em uso. O painel provavelmente já está rodando em http://${HOST}:${PORT}\n`);
    process.exit(1);
  }
  throw e;
});

server.listen(PORT, HOST, () => {
  console.log(`\n  Painel de Demandas rodando em  http://${HOST}:${PORT}`);
  console.log(`  Fonte de verdade: ${DATA_FILE}`);
  console.log(`  ${state.demandas.length} demandas · corte ${state.corte}\n`);
});
