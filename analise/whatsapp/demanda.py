#!/usr/bin/env python3
"""Detector de demanda de suporte, calibrado sobre amostra lida a mao."""
import json,re,os,sys,datetime as dt,statistics as st
from collections import Counter,defaultdict
BASE=os.path.dirname(os.path.abspath(__file__))

# --- ruido: mensagem que NAO abre demanda -------------------------------
RUIDO=[
 r'^\W*(bom dia|boa tarde|boa noite|oi|ol[aá]|opa|bora|show|shoow+|valeu|obrigad[oa]|ok|blz|beleza|isso|perfeito|certo|ótimo|otimo|top|legal|👏|🚀|🎯|🙏|❤️|😍|👍)\W*$',
 r'parab[eé]ns|bora pra cima|vamos avante|abençoad|excelente dia|f[eé]ria|feliz|bom fim de semana',
 r'^\W*\d+\W*$|^\W*$',
 r'^[\W\d]{0,4}(sim|n[aã]o|ok|uhum|certo|entendi|combinado|fechado|show)[\W]{0,4}$',
]
# --- marcadores de pedido ----------------------------------------------
PEDIDO=[
 r'\?',                                        # pergunta direta
 r'\b(preciso|precisamos|poderia|pode(m)?\s|consegue|conseguem|como (fa[cç]o|faz|posso|consigo)|me aju|ajuda|auxili|verific|confer|resolv|libera|envia|manda|gera)\b',
 r'\b(n[aã]o (consig|est[aá]|deu|aparece|carrega|abre|funciona|chega|sai|sobe|entra|reconhec|localiz))\b',
 r'\b(erro|travad|instabil|fora do ar|problema|falha|pendente|urgente|priorid)\b',
 r'\balgu[eé]m\b',
]
RX_RUIDO=re.compile('|'.join(RUIDO),re.I)
RX_PEDIDO=re.compile('|'.join(PEDIDO),re.I)

TAXO=[
 ("erro/instabilidade",   r'instabil|fora do ar|\berro\b|travad|bugad|deu ruim|saldo insuficiente'
                          r'|n[aã]o (est[aá] )?(sai|carrega|abre|funciona|avan[cç]a|configur|aparec|sobe|passa|process|conclu|final|d[aá] certo)'),
 ("pagamento/boleto",     r'boleto|2[aª] via|fatura|pagamento|pagar|paga\b|pagou|baixa|quita|cobran|parcela|carn[eê]|pix|comprovante'),
 ("acesso/senha/operador",r'senha|acesso|login|usu[aá]rio|operador|desbloque|liberar? acesso|entrar no (app|sistema|portal)'),
 ("telefone/vinculo",     r'n[uú]mero (cadastrad|antigo|novo)|troca(r)? (o )?(n[uú]mero|app|aparelho)|desvincul|perdeu o n[uú]mero|chip'
                          r'|c[oó]digo (n[aã]o )?(chega|chegou)|\bsms\b'),
 ("cadastro/biometria",   r'biometria|selfie|documento|cadastro d[oa] (cliente|vendedor)|\bcaf\b|reconhecimento facial|dados (dela|dele|do cliente)'),
 ("credito/limite/regra", r'limite|aprova|reprova|negad|an[aá]lise|score|entrada|financeira|juros|condi[cç][aã]o de venda'
                          r'|cr[eé]dito|n[aã]o est[aá] passando|prazo de pagamento'),
 ("cancelamento/estorno", r'cancel|estorn|desisti|devolu|arrepend'),
 ("codigo/finalizar venda",r'c[oó]digo de (compra|venda|cadastro)|finalizar a venda|cupom|\bimei\b|contrato|n[uú]mero do contrato'),
 ("catalogo/aparelho",    r'n[aã]o (est[aá] |esta )?cadastrad|aparelho|modelo|samsung|motorola|xiaomi|iphone|sku|cat[aá]logo|estoque'),
 ("pdv/integracao",       r'\bpdv\b|integra|\bapi\b|endpoint|logo|configura[cç][aã]o|maquineta|paymobi|\bti\b'),
 ("relatorio/material",   r'relat[oó]rio|lista|planilha|material|ebook|treinamento|chek?list|manual|apura[cç][aã]o|comiss[aã]o|por loja'),
 ("comercial/expansao",   r'expans[aã]o|nova(s)? loja|parceria|representante|comercial|reuni[aã]o|contrato novo'),
 ("gestao do grupo",      r'(colocar?|adicionar?|incluir?) .{0,20}(no|ao) grupo|tirar do grupo|n[aã]o est[aá] no grupo|entrar no grupo'),
 ("status de caso aberto",r'prazo estimado|alguma previs|novidade|retorno sobre|conseguiu (ver|resolver)|j[aá] conseguiu|conseguiram ajuda|ainda n[aã]o'),
]
PEDIDO_PURO=re.compile(r'^\W*(bo[am] (dia|tarde|noite)[\s!,.]*)?'
  r'(pessoal|time|gente|@\S+|\s)*'
  r'(algu[eé]m|por (gentileza|favor)|pfvr|pf|preciso de (ajuda|suporte|auxi?li)|poderia me ajudar|pode(m)? (nos |me )?ajudar|ajuda)'
  r'[\w\s,!?.\u00c0-\u00ff👆🙏]{0,45}$',re.I)

def motivo(t):
    for n,rx in TAXO:
        if re.search(rx,t,re.I): return n
    if PEDIDO_PURO.match(t.strip()): return "pedido sem contexto"
    return "nao classificado"

CENTRAL=re.compile(r'\bcentral\b|live ?chat|livechat|chatbot|0800|bal[aã]o verde|atendimento (oficial|da ume)',re.I)
LOJA=re.compile(r'cliente (est[aá]|t[aá]|aqui|na loja|em loja|aguard|esper)|em loja|na loja|balc[aã]o|cliente na minha frente',re.I)

def is_demanda(m):
    t=m['txt'].strip()
    if m['media'] or len(t)<10: return False
    if RX_RUIDO.search(t) and len(t)<60: return False
    return bool(RX_PEDIDO.search(t))

msgs=[m for m in json.load(open(f"{BASE}/msgs2.json"))]
for m in msgs: m['dt']=dt.datetime.fromisoformat(m['ts'])
msgs.sort(key=lambda m:m['dt'])
JAN=(dt.datetime(2026,6,3),dt.datetime(2026,9,3,23,59))
por_grupo=defaultdict(list)
for m in msgs: por_grupo[m['grupo']].append(m)

dem=[]
for g,lst in por_grupo.items():
    for i,m in enumerate(lst):
        if m['lado']!='varejo' or not (JAN[0]<=m['dt']<=JAN[1]): continue
        if not is_demanda(m): continue
        # agrupa: se o mesmo autor ja abriu demanda ha <30min, é continuacao
        ant=[d for d in dem if d['grupo']==g and d['autor']==m['autor']
             and (m['dt']-d['dt']).total_seconds()<1800]
        if ant: 
            ant[-1]['msgs']+=1; ant[-1]['txt']+=' || '+m['txt'][:120]; continue
        resp=None
        for x in lst[i+1:]:
            if (x['dt']-m['dt']).total_seconds()>172800: break
            if x['lado']=='ume': resp=x; break
        dem.append(dict(grupo=g,dt=m['dt'],autor=m['autor'],txt=m['txt'][:300],msgs=1,
            motivo=motivo(m['txt']),central=bool(CENTRAL.search(m['txt'])),
            loja=bool(LOJA.search(m['txt'])),
            resp=((resp['dt']-m['dt']).total_seconds()/60) if resp else None))
# reclassifica sobre o TEXTO COMPLETO da demanda (abertura + continuacoes),
# porque no WhatsApp o pedido costuma abrir com "alguem pode ajudar?" e o tema vem depois
def redigir(t):
    t=re.sub(r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b','[CPF]',t)
    t=re.sub(r'(?:\+?55)?[\s\-(]*\d{2}[\s\-)]*9?\d{4}[\s\-.]?\d{4}','[TEL]',t)
    return t
for d in dem:
    d['motivo']=motivo(d['txt'])
    d['txt']=redigir(d['txt'])
    d['central']=bool(CENTRAL.search(d['txt']))
    d['loja']=bool(LOJA.search(d['txt']))
json.dump([{**d,'dt':d['dt'].isoformat()} for d in dem],open(f"{BASE}/demandas2.json",'w'),ensure_ascii=False)

varejo_jan=[m for m in msgs if m['lado']=='varejo' and JAN[0]<=m['dt']<=JAN[1]]
print(f"mensagens do varejo na janela : {len(varejo_jan)}")
print(f"DEMANDAS detectadas           : {len(dem)}   ({100*len(dem)/len(varejo_jan):.0f}% das msgs)")
print(f"  (agrupando continuacoes do mesmo autor em ate 30 min)\n")
print("=== POR GRUPO ===")
for g,n in Counter(d['grupo'] for d in dem).most_common():
    tot=len([m for m in varejo_jan if m['grupo']==g])
    print(f"  {n:>4}  ({100*n/tot:>2.0f}% das msgs varejo)  {g.replace('WhatsApp_Chat__','')[:30]}")
print("\n=== POR MOTIVO ===")
for k,v in Counter(d['motivo'] for d in dem).most_common():
    print(f"  {k:<26} {v:>4}  {100*v/len(dem):>5.1f}%")
print("\n=== RESPOSTA DA UME ===")
r=sorted([d['resp'] for d in dem if d['resp'] is not None])
sem=[d for d in dem if d['resp'] is None]
print(f"  respondidas em ate 48h : {len(r)} ({100*len(r)/len(dem):.0f}%)")
print(f"  sem resposta da Ume    : {len(sem)} ({100*len(sem)/len(dem):.0f}%)")
print(f"  mediana {st.median(r):.0f} min | p75 {r[int(.75*len(r))]:.0f} | p90 {r[int(.90*len(r))]:.0f}")
for lim,l in [(5,'<= 5 min'),(15,'<= 15 min'),(60,'<= 1 h')]:
    print(f"    {l:<10} {sum(1 for x in r if x<=lim):>4}  {100*sum(1 for x in r if x<=lim)/len(r):>5.1f}%")
print(f"\n  cita canal oficial : {sum(d['central'] for d in dem)} ({100*sum(d['central'] for d in dem)/len(dem):.1f}%)")
print(f"  cliente em loja    : {sum(d['loja'] for d in dem)} ({100*sum(d['loja'] for d in dem)/len(dem):.1f}%)")
