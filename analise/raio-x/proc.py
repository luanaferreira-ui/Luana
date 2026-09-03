import csv,re,hashlib,datetime as dt,json,statistics as st
TZ=dt.timezone(dt.timedelta(hours=-3))
SALT="ume-voice-of-retailer-2026"           # local, nao versionado
def pid(digits): return "CLI-"+hashlib.sha256((SALT+digits).encode()).hexdigest()[:6]

def phones(t):
    out=[]
    for m in re.finditer(r'(?:\+?55)?[\s\-\(]*\d{2}[\s\-\)]*\d{4,5}[\s\-\.]?\d{4}', t):
        d=re.sub(r'\D','',m.group(0))
        if d.startswith('55') and len(d)>11: d=d[2:]
        if 10<=len(d)<=11: out.append(d)
    return sorted(set(out))

MOTIVOS=[
 ("boleto/2a via",      r'boleto|2a via|segunda via|sincronizar boleto'),
 ("baixa de pagamento", r'baixa (de|no|na) pag|baixa de boleto|baixa na fatura|pagamento (nao|sem) (reconhec|process|identific|baixa)|pagamento sem baixa|nao deu baixa|pagou boleto'),
 ("codigo de compra",   r'codigo de compra|cod\. de compra|codigo da venda|codigo para finalizar|codigo de validacao|comprovante de compra|codigo do app|codigo para baixar'),
 ("telefone/vinculo",   r'troca de numero|troca de n|desvincular|alteracao de telefone|atualizacao de telefone|altera(cao)? de numero|erro ao trocar'),
 ("cadastro/dados",     r'atualizacao (de )?cadastr|atualizacao cadastral|atualizar cadastro|dados cadastrais|contestacao de cadastro|tentando fazer o cadastro|cadastro nao subiu|caf\b|atualizar contato|atualizacao \+|atualizacao <'),
 ("acesso/senha",       r'acesso|senha|login|desbloqueio|cadastro de operador|operador|app\b'),
 ("cancelamento",       r'cancelamento|cancelar|contestacao de compra|venda duplicada'),
 ("credito/limite",     r'limite|negativa na analise|acordo|renegocia|negociacao de divida|parcelas em aberto'),
 ("erro/instabilidade", r'erro|instabilidade|nao consegue|nao funciona|sem sucesso|nao localizado|demora no locker|nao consta'),
 ("comercial/parceria", r'representante|comercial|parceria|formato de venda|repasse de venda'),
]
def motivo(t):
    for nome,rx in MOTIVOS:
        if re.search(rx,t,re.I): return nome
    return "outros"

RX_LOJA=r'cliente em loja|cliente na loja|clit em loja|cliente em lojas|em loja\b'
RX_URG =r'urgente|prioridade|\[urgente\]|warn'
RX_CENTRAL=r'central|live ?chat|livechat|chat\b|bot\b'
RX_FALHA_CENTRAL=r'sem retorno|sem sucesso|nao respond|nao atende|tentando falar|tentou contato|em contato com a central|nao localizado pelo bot|demora|hora de espera|nao conseguiu enviar'

rows=[]
for line in open(SP_ALL:=__import__('sys').argv[1],encoding='utf-8'):
    p=line.rstrip('\n').split('\t')
    if len(p)<5: continue
    ts,rep,latest,autor,titulo=float(p[0]),int(p[1]),p[2],p[3],p[4]
    t0=dt.datetime.fromtimestamp(ts,TZ)
    dur=None
    if latest:
        t1=dt.datetime.strptime(latest,"%Y-%m-%d %H:%M:%S").replace(tzinfo=TZ)
        dur=(t1-t0).total_seconds()/60
    ruido = bool(re.search(r'RENAME CANAL|MENCAO SEM CONTEUDO|ENCAMINHADO|INCIDENTE|Novas parcerias|Parceria para fortalecer|Processo Solicitacao de cadastro',titulo))
    ph=phones(titulo)
    rows.append(dict(ts=ts,dt=t0,dia=t0.date().isoformat(),hora=t0.hour,rep=rep,dur=dur,
        autor=autor,titulo=titulo,ruido=ruido,
        ids=[pid(x) for x in ph],
        tipo=("varejo" if re.search(r'ao varejo|varejista|ao vendedor|lojista|varejo em contato|central do varejo',titulo,re.I)
              else "cliente" if re.search(r'ao cliente|suporte ao cliente|cliente em|cliente na',titulo,re.I) else "nao classificado"),
        motivo=motivo(titulo),
        em_loja=bool(re.search(RX_LOJA,titulo,re.I)),
        urgente=bool(re.search(RX_URG,titulo,re.I)),
        cita_canal=bool(re.search(RX_CENTRAL,titulo,re.I)),
        falha_central=bool(re.search(RX_FALHA_CENTRAL,titulo,re.I)),
    ))
json.dump([{**r,'dt':r['dt'].isoformat()} for r in rows],open(SP_ALL.replace('all.tsv','dataset.json'),'w'),ensure_ascii=False,indent=1)

uteis=[r for r in rows if not r['ruido']]
print(f"=== BASE ===")
print(f"threads totais            : {len(rows)}")
print(f"  ruido (avisos, rename)  : {sum(r['ruido'] for r in rows)}")
print(f"  demandas de atendimento : {len(uteis)}")
d=sorted(r['dia'] for r in rows); print(f"janela                    : {d[0]} a {d[-1]}")
dias_com_post=len(set(d)); print(f"dias com movimento        : {dias_com_post}")
print(f"media por dia com posts   : {len(uteis)/dias_com_post:.1f}")

def dist(campo,base=uteis):
    from collections import Counter
    c=Counter(r[campo] for r in base); n=len(base)
    for k,v in c.most_common(): print(f"  {k:<22} {v:>4}  {100*v/n:>5.1f}%")

print("\n=== TIPO ==="); dist('tipo')
print("\n=== MOTIVO ==="); dist('motivo')

print("\n=== SINAIS ===")
n=len(uteis)
for lbl,f in [("cliente em loja",'em_loja'),("marcado urgente",'urgente'),
              ("cita central/livechat/bot",'cita_canal'),("cita falha do canal oficial",'falha_central')]:
    v=sum(r[f] for r in uteis); print(f"  {lbl:<28} {v:>4}  {100*v/n:>5.1f}%")

print("\n=== RESPOSTA E DESFECHO ===")
sem=[r for r in uteis if r['rep']==0]
print(f"  threads sem nenhuma resposta : {len(sem)}  ({100*len(sem)/n:.1f}%)")
com=[r for r in uteis if r['dur'] is not None]
durs=sorted(r['dur'] for r in com)
def pct(p): 
    i=min(int(p/100*len(durs)),len(durs)-1); return durs[i]
print(f"  duracao da thread (parent -> ultima resposta), n={len(com)}")
print(f"    mediana        : {st.median(durs):>7.1f} min")
print(f"    media          : {st.mean(durs):>7.1f} min")
print(f"    p75            : {pct(75):>7.1f} min")
print(f"    p90            : {pct(90):>7.1f} min")
print(f"    max            : {durs[-1]:>7.1f} min ({durs[-1]/60:.1f} h)")
for lim,lbl in [(5,"<= 5 min"),(15,"<= 15 min"),(30,"<= 30 min"),(60,"<= 60 min")]:
    v=sum(1 for x in durs if x<=lim); print(f"    {lbl:<14} : {v:>4}  {100*v/len(durs):>5.1f}%")
vira=sum(1 for x in durs if x>240); print(f"    > 4 h          : {vira:>4}  {100*vira/len(durs):>5.1f}%")

print("\n=== SLA PROPOSTO (contra duracao total da thread) ===")
loja=[r['dur'] for r in uteis if r['em_loja'] and r['dur'] is not None]
naoloja=[r['dur'] for r in uteis if not r['em_loja'] and r['dur'] is not None]
if loja:
    print(f"  cliente em loja (meta 5 min), n={len(loja)}")
    print(f"    mediana {st.median(loja):.1f} min | dentro de 5 min: {sum(1 for x in loja if x<=5)}/{len(loja)} = {100*sum(1 for x in loja if x<=5)/len(loja):.1f}%")
print(f"  demais (meta 15 min), n={len(naoloja)}")
print(f"    mediana {st.median(naoloja):.1f} min | dentro de 15 min: {sum(1 for x in naoloja if x<=15)}/{len(naoloja)} = {100*sum(1 for x in naoloja if x<=15)/len(naoloja):.1f}%")

print("\n=== VOLUME POR MES ===")
from collections import Counter
for k,v in sorted(Counter(r['dia'][:7] for r in uteis).items()): print(f"  {k}  {v:>4}")

print("\n=== CLIENTES RECORRENTES (pseudonimizados) ===")
c=Counter(i for r in uteis for i in r['ids'])
rec=[(k,v) for k,v in c.most_common() if v>1]
print(f"  contatos distintos identificados : {len(c)}")
print(f"  contatos que aparecem 2+ vezes   : {len(rec)}  ({100*len(rec)/len(c):.1f}%)")
print(f"  threads envolvendo recorrentes   : {sum(1 for r in uteis if any(c[i]>1 for i in r['ids']))}")
print("  top recorrencia:")
for k,v in rec[:8]: print(f"    {k}  {v} aparicoes")
