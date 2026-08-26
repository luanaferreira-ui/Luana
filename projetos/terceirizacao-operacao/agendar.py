# -*- coding: utf-8 -*-
"""Agenda F1-F4 respeitando dependências (ordem topológica), fase de início e a
capacidade real de cada semana. F5 é ritmo de calendário (o piloto roda no tempo
dele), então mantém as datas e só confere a carga."""
import json, datetime as dt, math
from collections import defaultdict

FERIADOS = {"2026-09-07","2026-10-12","2026-11-02","2026-11-20","2026-12-25",
            "2027-01-01","2027-02-08","2027-02-09","2027-03-26","2027-04-21"}
CAP, INICIO = 8.0, dt.date(2026,8,26)
RECESSO = {(dt.date(2026,12,21)+dt.timedelta(weeks=k)).isoformat() for k in range(3)}
def seg(d): return d - dt.timedelta(days=d.weekday())
def cap(s):
    if s.isoformat() in RECESSO: return 0.0
    if s == seg(INICIO): return 5.0
    return round(CAP*sum(1 for i in range(5) if (s+dt.timedelta(days=i)).isoformat() not in FERIADOS)/5, 1)

plano = json.load(open("plano.json"))
fase_ini = {f["id"]: dt.date.fromisoformat(f["inicio"]) for f in plano["fases"]}
T = {t["id"]: t for t in plano["tarefas"]}
deps = {t["id"]: [d.strip() for d in t["dependencia"].split(",") if d.strip() not in ("—","")] for t in plano["tarefas"]}
prio = {"P0":0,"P1":1,"P2":2}

# ordem topológica, priorizando P0 entre os disponíveis
grau = {i: len([d for d in deps[i] if d in T]) for i in T}
filhos = defaultdict(list)
for i, ds in deps.items():
    for d in ds:
        if d in T: filhos[d].append(i)
pronto = [i for i in T if grau[i] == 0]
ordem = []
while pronto:
    pronto.sort(key=lambda i: (T[i]["fase"], prio[T[i]["prioridade"]], i))
    i = pronto.pop(0); ordem.append(i)
    for f in filhos[i]:
        grau[f] -= 1
        if grau[f] == 0: pronto.append(f)
assert len(ordem) == len(T), "ciclo de dependência"

livre, fim = {}, {}
def restante(s, dono):
    livre.setdefault((s,dono), cap(s))
    return livre[(s,dono)]

for i in ordem:
    t = T[i]
    # mesma pessoa: as horas já são sequenciais, pode ser na mesma semana.
    # pessoas diferentes: só na semana seguinte, senão o handoff não existe de verdade.
    pisos = [fase_ini[t["fase"]]]
    for d in deps[i]:
        if d not in fim: continue
        pisos.append(seg(fim[d]) if T[d]["dono"] == t["dono"] else seg(fim[d]) + dt.timedelta(weeks=1))
    piso = seg(max(pisos))
    if t["fase"] == "F5":                      # calendário manda: espalha para trás do alvo
        alvo = dt.date.fromisoformat(t["data_alvo"])
        n = max(1, math.ceil(t["esforco_h"]/6))
        piso = max(piso, seg(alvo - dt.timedelta(weeks=n-1)))
    s, h, ultima = piso, float(t["esforco_h"]), piso
    while h > 0 and s < dt.date(2028,1,1):
        usa = min(h, restante(s, t["dono"]))
        if usa > 0:
            livre[(s,t["dono"])] -= usa; h -= usa; ultima = s
        s += dt.timedelta(weeks=1)
    fim[i] = ultima + dt.timedelta(days=4)
    t["data_alvo"] = fim[i].isoformat()
    t.pop("data_alvo_agendada", None)

print("Fim real por fase, com 8h/semana de cada uma:")
for f in plano["fases"]:
    its = [t for t in plano["tarefas"] if t["fase"] == f["id"]]
    p0 = max(dt.date.fromisoformat(t["data_alvo"]) for t in its if t["prioridade"] == "P0")
    todos = max(dt.date.fromisoformat(t["data_alvo"]) for t in its)
    f["fim_p0"], f["fim"] = p0.isoformat(), todos.isoformat()
    print(f"  {f['id']} {f['nome']:32} P0 {p0} | tudo {todos}")

print("\nCaminho crítico (a corrente mais longa de dependências):")
memo = {}
def cadeia(i):
    if i in memo: return memo[i]
    best = max([cadeia(d) for d in deps[i] if d in T] or [[]], key=len)
    memo[i] = best + [i]; return memo[i]
cc = max((cadeia(i) for i in T), key=len)
print("  " + " > ".join(cc))
plano["caminho_critico"] = cc

print("\nCarga semanal (h) — cap | Luana | Luiza:")
sem = sorted({s for s,_ in livre})
carga = []
for s in sem:
    c = cap(s)
    lu = round(c - livre.get((s,"Luana"), c), 1)
    li = round(c - livre.get((s,"Luiza"), c), 1)
    if lu or li or c == 0:
        carga.append({"semana": s.isoformat(), "capacidade": c, "Luana": lu, "Luiza": li})
        marca = "  CHEIA" if (lu >= c and c) or (li >= c and c) else ""
        print(f"  {s.strftime('%d/%m'):6} {c:4} | {lu:5} | {li:5}{marca}")
plano["carga_semanal"] = carga
json.dump(plano, open("plano.json","w"), ensure_ascii=False, indent=2)
