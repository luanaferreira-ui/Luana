'use strict';

/*
 * sync-radar.js — puxa as demandas novas que o radar depositou e importa no
 * painel local, SEM tocar no que já existe.
 *
 * Roda automaticamente antes do servidor (npm start -> prestart). Fluxo:
 *   1. git pull --ff-only  (best-effort; se falhar/offline, segue sem barrar)
 *   2. garante que demandas.json existe (nasce da semente no 1º boot)
 *   3. lê radar-inbox.jsonl (1 demanda em JSON por linha, append-only pelo radar)
 *   4. importa só as que ainda não foram consumidas nem já existem (dedup por
 *      título normalizado), respeitando o corte; grava com backup + rename atômico
 *   5. registra o que consumiu em .radar-consumed.json (local) p/ não repetir
 *
 * O radar NUNCA escreve demandas.json — só a caixa de entrada. Assim o seu
 * arquivo é só seu e o git pull é sempre fast-forward (sem conflito).
 */

const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');

const ROOT = __dirname;
const DATA_FILE = path.join(ROOT, 'demandas.json');
const SEED_FILE = path.join(ROOT, 'demandas.seed.json');
const INBOX_FILE = path.join(ROOT, 'radar-inbox.jsonl');
const CONSUMED_FILE = path.join(ROOT, '.radar-consumed.json');
const BACKUP_DIR = path.join(ROOT, '.backup');

function log(msg) { console.log('  [sync] ' + msg); }

function gitPull() {
  try {
    execFileSync('git', ['pull', '--ff-only'], { cwd: ROOT, stdio: 'pipe', timeout: 20000 });
    log('git pull ok');
  } catch (e) {
    const m = (e.stderr && e.stderr.toString().trim()) || e.message;
    log('git pull pulado (' + m.split('\n')[0] + ') — seguindo com a caixa local');
  }
}

function normalizeTitle(s) {
  return String(s || '')
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, ' ')
    .trim();
}

function isValidDate(s) {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(s));
  if (!m) return false;
  const y = +m[1], mo = +m[2], da = +m[3];
  const dt = new Date(Date.UTC(y, mo - 1, da));
  return dt.getUTCFullYear() === y && dt.getUTCMonth() === mo - 1 && dt.getUTCDate() === da;
}

function nextIdFactory(demandas) {
  let max = -1;
  for (const d of demandas) {
    const m = /^d(\d+)$/.exec(d.id || '');
    if (m) max = Math.max(max, parseInt(m[1], 10));
  }
  return () => 'd' + String(++max).padStart(2, '0');
}

function readInbox() {
  if (!fs.existsSync(INBOX_FILE)) return [];
  return fs.readFileSync(INBOX_FILE, 'utf8')
    .split(/\r?\n/)
    .map((l) => l.trim())
    .filter(Boolean)
    .map((l, i) => { try { return JSON.parse(l); } catch { log('linha ' + (i + 1) + ' da caixa ignorada (JSON inválido)'); return null; } })
    .filter(Boolean);
}

function main() {
  gitPull();

  if (!fs.existsSync(DATA_FILE)) {
    if (fs.existsSync(SEED_FILE)) { fs.copyFileSync(SEED_FILE, DATA_FILE); log('demandas.json criado da semente'); }
    else { log('sem demandas.json e sem semente — nada a fazer'); return; }
  }

  const inbox = readInbox();
  if (!inbox.length) { log('caixa do radar vazia — nada novo'); return; }

  const state = JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
  if (!Array.isArray(state.demandas)) state.demandas = [];
  const corte = state.corte || '2026-07-01';
  const clusterIds = new Set((state.clusters || []).map((c) => c.id));

  const consumed = new Set(fs.existsSync(CONSUMED_FILE) ? JSON.parse(fs.readFileSync(CONSUMED_FILE, 'utf8')) : []);
  const existentes = new Set(state.demandas.map((d) => normalizeTitle(d.titulo)));
  const nextId = nextIdFactory(state.demandas);

  let add = 0, rep = 0, fora = 0, inval = 0;
  const aceitas = [];
  for (const n of inbox) {
    const key = normalizeTitle(n.titulo);
    if (!key) { inval++; continue; }
    if (consumed.has(key)) continue;              // já importada numa rodada anterior
    consumed.add(key);                            // marca como vista (mesmo se recusada, não reprocessa)
    if (!clusterIds.has(n.cluster)) { inval++; continue; }
    if (n.prazo && !isValidDate(n.prazo)) { inval++; continue; }
    if (n.prazo && n.prazo < corte) { fora++; continue; }
    if (existentes.has(key)) { rep++; continue; } // já existe no painel
    existentes.add(key);
    aceitas.push({
      id: nextId(),
      titulo: String(n.titulo).trim(),
      cluster: n.cluster,
      conta: (n.conta && String(n.conta).trim()) || '—',
      responsavel: (n.responsavel && String(n.responsavel).trim()) || 'Luana',
      prazo: n.prazo || null,
      urgente: !!n.urgente,
      status: 'aberto',
      origem: (n.origem && String(n.origem).trim()) || 'Radar',
    });
    add++;
  }

  if (aceitas.length) {
    try {
      if (!fs.existsSync(BACKUP_DIR)) fs.mkdirSync(BACKUP_DIR, { recursive: true });
      const ts = new Date().toISOString().replace(/[:.]/g, '-');
      fs.copyFileSync(DATA_FILE, path.join(BACKUP_DIR, `demandas-${ts}-sync.json`));
    } catch (e) { log('backup falhou (seguindo): ' + e.message); }
    state.demandas.push(...aceitas);
    state.atualizado_em = new Date().toISOString().slice(0, 10);
    const tmp = path.join(ROOT, `.demandas.sync.${process.pid}.tmp`);
    fs.writeFileSync(tmp, JSON.stringify(state, null, 2) + '\n');
    fs.renameSync(tmp, DATA_FILE);
  }
  fs.writeFileSync(CONSUMED_FILE, JSON.stringify([...consumed], null, 2));

  log(`${add} nova(s), ${rep} já existiam, ${fora} fora do período, ${inval} inválida(s). Total agora: ${state.demandas.length}.`);
}

main();
