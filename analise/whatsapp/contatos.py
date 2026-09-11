#!/usr/bin/env python3
"""Lista consolidada de contatos (hash) com tipo, varejo, canal e motivo.
Le os datasets ja gerados; nenhum numero em claro entra ou sai."""
import json,re,csv,hashlib,datetime as dt,os,sys
from collections import defaultdict
WA=os.path.dirname(os.path.abspath(__file__))
RX=os.path.join(os.path.dirname(WA),'raio-x')
SALT="ume-voice-of-retailer-2026"
def h(d): return "CT-"+hashlib.sha256((SALT+d).encode()).hexdigest()[:10]
def fones(t):
    out=set()
    for m in re.finditer(r'(?:\+?55)?[\s\-(]*(\d{2})[\s\-)]*(9?\d{4})[\s\-.]?(\d{4})\b',t):
        d=''.join(m.groups())
        if len(d) in (10,11) and 11<=int(d[:2])<=99: out.add(d)
    return out

C=defaultdict(lambda: dict(slack=0,wa=0,tipos=set(),varejos=set(),motivos=set(),datas=[]))

# ---------- SLACK (tem tipo e motivo classificados) ----------
MOT=[("boleto/2a via",r'boleto|2[aª] via|segunda via|sincronizar boleto'),
 ("baixa de pagamento",r'baixa|pagamento n[aã]o|pagou|compensa'),
 ("codigo de compra",r'c[oó]digo de compra|cod\. de compra|codigo de compra|comprovante de compra|c[oó]digo do app'),
 ("telefone/vinculo",r'troca de n|desvincul|altera[cç][aã]o de telefone|atualiza[cç][aã]o de telefone'),
 ("cadastro/dados",r'cadastr|atualiza[cç][aã]o|caf\b|contesta[cç][aã]o'),
 ("acesso/senha",r'acesso|senha|operador|desbloque'),
 ("cancelamento",r'cancel|estorn'),
 ("credito/limite",r'limite|negocia|acordo|renegocia|aprova'),
 ("erro/instabilidade",r'erro|instabil|n[aã]o consig|bot\b'),
 ("comercial",r'representante|comercial|parceria')]
def motivo(t):
    for n,rx in MOT:
        if re.search(rx,t,re.I): return n
    return "outros"
TZ=dt.timezone(dt.timedelta(hours=-3))
for line in open(os.path.join(RX,'all.tsv'),encoding='utf-8'):
    p=line.rstrip('\n').split('\t')
    if len(p)<5: continue
    ts=dt.datetime.fromtimestamp(float(p[0]),TZ); tit=p[4]
    tipo=("varejo" if re.search(r'ao varejo|varejista|ao vendedor|lojista|central do varejo',tit,re.I)
          else "cliente" if re.search(r'ao cliente|cliente em|cliente na|suporte ao cliente',tit,re.I)
          else "indefinido")
    for f in fones(tit):
        k=C[h(f)]; k['slack']+=1; k['tipos'].add(tipo); k['motivos'].add(motivo(tit))
        k['datas'].append(ts.date())

# ---------- WHATSAPP (tem o varejo pelo grupo) ----------
msgs=json.load(open(os.path.join(WA,'msgs2.json')))
GRP={'UME__CVLB_2':'CVLB','Big_Lar__Cre_dito_Digital_Ume_2':'Big Lar','POLICRED_2':'Policred',
 'UME__SIPOLATTI_FILIAIS':'Sipolatti','Mini_Prec_o__Ume_1':'Mini Preco','UME__MAG_DUARTE_1':'Mag Duarte',
 'UME__TOP_MO_VEIS_1':'Top Moveis','Ume_e_Solar_Moveis_e_Eletros_3':'Solar Moveis','Ume__10Cia':'10&Cia',
 'Novo_Mundo__Ume__Integrac_a_o':'Novo Mundo','Mega_Vint_o__Gerentes_Ume_':'Mega Vintao',
 'Baianao____Ume':'Baianao','NovoLare____Ume':'Novo Lar'}
for m in msgs:
    g=GRP.get(m['grupo'].replace('WhatsApp_Chat__',''),'?')
    d=dt.datetime.fromisoformat(m['ts']).date()
    # telefone citado no texto: quase sempre e de CLIENTE (o varejo fala do cliente)
    for f in fones(m['txt']):
        k=C[h(f)]; k['wa']+=1; k['varejos'].add(g); k['motivos'].add(motivo(m['txt']))
        k['tipos'].add('cliente (citado pelo varejo)'); k['datas'].append(d)
        if f[:2]=='11' and f[2] in '234' and len(f)==10: k['fixo']=True
    # autor identificado por telefone: e do VAREJO (participa do grupo)
    if m['autor'].startswith('PART-'):
        k=C['CT-'+m['autor'][5:]]      # ja vem hasheado do parser
        k['wa']+=1; k['varejos'].add(g); k['tipos'].add('varejo (participante do grupo)')
        k['datas'].append(d)

# --- reclassifica numeros institucionais -------------------------------
# um telefone que aparece em 3+ grupos distintos, ou que e fixo de capital
# (DDD 11 + prefixo 2/3/4), nao e cliente: e canal da Ume ou numero publicado
for cid,v in C.items():
    multi = len(v['varejos'])>=3
    if multi or v.get('fixo'):
        v['tipos']={'institucional / canal divulgado'}
        v['motivos'].add('numero divulgado no grupo')

rows=[]
for cid,v in C.items():
    ds=sorted(v['datas'])
    rows.append(dict(contato_id=cid,
        tipo=' / '.join(sorted(v['tipos'])) or 'indefinido',
        varejo=' / '.join(sorted(v['varejos'])) or '(nao identificado)',
        canais=('ambos' if v['slack'] and v['wa'] else 'slack' if v['slack'] else 'whatsapp'),
        n_slack=v['slack'],n_whatsapp=v['wa'],total=v['slack']+v['wa'],
        primeiro=ds[0].isoformat(),ultimo=ds[-1].isoformat(),
        motivos=' | '.join(sorted(m for m in v['motivos'] if m))))
rows.sort(key=lambda r:(-r['total'],r['contato_id']))
out=os.path.join(WA,'contatos.csv')
with open(out,'w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(f"contatos distintos: {len(rows)}  ->  {out}\n")
from collections import Counter
print("por canal:");  [print(f"   {k:<10}{v:>5}") for k,v in Counter(r['canais'] for r in rows).most_common()]
print("\npor tipo:");  [print(f"   {k[:42]:<44}{v:>5}") for k,v in Counter(r['tipo'] for r in rows).most_common()]
print("\ncom varejo identificado:", sum(1 for r in rows if r['varejo']!='(nao identificado)'))
print("com 2+ contatos          :", sum(1 for r in rows if r['total']>1))
print("\nmotivos mais frequentes:")
mc=Counter(m for r in rows for m in r['motivos'].split(' | ') if m)
[print(f"   {k:<24}{v:>5}") for k,v in mc.most_common(10)]
