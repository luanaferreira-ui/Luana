#!/usr/bin/env python3
"""Varredura de identificadores (telefone e CPF) nos 13 grupos + Slack.
Nada em claro entra no relatorio: tudo e hasheado no ato da leitura."""
import json,re,csv,hashlib,datetime as dt,os
from collections import defaultdict,Counter
WA=os.path.dirname(os.path.abspath(__file__)); RX=os.path.join(os.path.dirname(WA),'raio-x')
SALT="ume-voice-of-retailer-2026"
H=lambda p,d:p+hashlib.sha256((SALT+d).encode()).hexdigest()[:10]

GRP={'UME__CVLB_2':'CVLB','Big_Lar__Cre_dito_Digital_Ume_2':'Big Lar','POLICRED_2':'Policred',
 'UME__SIPOLATTI_FILIAIS':'Sipolatti','Mini_Prec_o__Ume_1':'Mini Preco','UME__MAG_DUARTE_1':'Mag Duarte',
 'UME__TOP_MO_VEIS_1':'Top Moveis','Ume_e_Solar_Moveis_e_Eletros_3':'Solar Moveis','Ume__10Cia':'10&Cia',
 'Novo_Mundo__Ume__Integrac_a_o':'Novo Mundo','Mega_Vint_o__Gerentes_Ume_':'Mega Vintao',
 'Baianao____Ume':'Baianao','NovoLare____Ume':'Novo Lar'}

# ---------- extratores ----------
def fones(t):
    out=set()
    for m in re.finditer(r'(?<![\d])(?:\+?55)?[\s\-(]*(\d{2})[\s\-)]*(9?\d{4})[\s\-.]?(\d{4})(?![\d])',t):
        d=''.join(m.groups())
        if len(d) in (10,11) and 11<=int(d[:2])<=99: out.add(d)
    return out

def dv_ok(c):
    if len(set(c))==1: return False
    for n in (9,10):
        s=sum(int(c[i])*((n+1)-i) for i in range(n))
        r=(s*10)%11%10
        if r!=int(c[n]): return False
    return True

def cpfs(t):
    out=set()
    # formatado: aceita mesmo sem passar no DV (digitacao humana), marca separado
    for m in re.finditer(r'(?<![\d.])(\d{3})\.(\d{3})\.(\d{3})-(\d{2})(?![\d-])',t):
        out.add((''.join(m.groups()),'formatado'))
    # 11 digitos soltos: so com DV valido, para nao pegar id de contrato/boleto
    for m in re.finditer(r'(?<![\d.\-/])(\d{11})(?![\d.\-/])',t):
        c=m.group(1)
        if dv_ok(c) and not (c[:2].isdigit() and c.startswith('55')): out.add((c,'11 digitos'))
    return out

# ---------- motivos ----------
MOT=[
 ("sem retorno da central",r'sem retorno|sem sucesso|n[aã]o (?:obteve|teve) retorno|tentando falar com a central|em contato com a central|nao atend|demora no'),
 ("baixa de pagamento",r'baixa|pagamento n[aã]o (?:identificad|reconhecid|processad|consta)|n[aã]o consta o pagamento|j[aá] paguei|pagou|compensa|comprovante de pag'),
 ("cobranca indevida",r'cobran[cç]a indevida|continuam? (?:me )?cobrando|indevid|contesta[cç][aã]o de parcela|contesta parcela|sem ci[eê]ncia|n[aã]o reconhece a compra'),
 ("codigo / comprovante de compra",r'c[oó]digo (?:de compra|da venda|de valida|para finalizar|do aplicativo|do app)|cod\.? de compra|comprovante de compra|c[oó]digo inv[aá]lido|repasse de venda|ccb'),
 ("boleto / 2a via",r'boleto|2[aª] via|segunda via|linha digit|parcelas em aberto'),
 ("telefone / vinculo",r'troca de n[uú]|desvincul|(?:altera[cç][aã]o|atualiza[cç][aã]o) de (?:telefone|n[uú]mero|contato)|n[uú]mero (?:errado|antigo)|alteracao de numero|atualizar contato'),
 ("cadastro / dados",r'cadastr|atualiza[cç][aã]o de dados|caf|biometri|selfie|cliente n[aã]o encontrado|n[aã]o reconhecendo o cpf|[oó]bito|documento'),
 ("acesso / senha",r'acesso|senha|login|operador|usu[aá]rio'),
 ("desbloqueio",r'desbloque|bloquead|bloqueio'),
 ("cancelamento / estorno",r'cancel|estorn|devolu|produto n[aã]o entregue'),
 ("credito / limite",r'limite|negocia|acordo|renegocia|aprova|recusad|negativ|entrada|an[aá]lise'),
 ("erro / instabilidade",r'erro|instabil|fora do ar|n[aã]o consig|travad|falha|incidente|n[aã]o est[aá] conseguindo|sem conseguir'),
 ("comercial / duvida de operacao",r'representante|comercial|parceria|treinamento|formato de venda|entender|d[uú]vida|insatisfeit')]
def motivo(t):
    for n,rx in MOT:
        if re.search(rx,t,re.I): return n
    return "outros"


VAREJOS={'Sipolatti':r'sipolat','Mag Duarte':r'mag[ae]?zine duarte|mag duarte','Top Moveis':r'top\s?m[oó]veis',
 'Novo Mundo':r'novo mundo','CVLB':r'cvlb|via l[aá]ctea','Big Lar':r'big\s?lar','Policred':r'policred',
 'Mini Preco':r'mini\s?pre[cç]o','Solar Moveis':r'solar m[oó]veis','10&Cia':r'10\s*&?\s*cia',
 'Mega Vintao':r'mega vint','Baianao':r'baian[aã]o','Novo Lar':r'novo\s?lar',
 'Casa e Video':r'casa e v[ií]deo','Pizzely':r'pizzely','Anjuss':r'anjuss','Bruno Eletromoveis':r'bruno eletrom',
 'IVS':r'\bivs\b','Boticario':r'botic[aá]rio','Oticas Nova':r'[oó]ticas? nova','Oticas Mabe':r'[oó]ticas? mabe',
 'FCDL / Lika Variedades':r'fcdl|lika variedades','Smart Curitiba':r'smart curitiba','Casa do Celular':r'casa do celular'}
def varejo_txt(t):
    return {n for n,rx in VAREJOS.items() if re.search(rx,t,re.I)}

ID=defaultdict(lambda: dict(kind='',slack=0,wa=0,varejos=set(),motivos=Counter(),
                            tipos=set(),datas=[],fixo=False))

# ---------- SLACK ----------
n_slack=0
if os.path.exists(os.path.join(RX,'all.tsv')):
    TZ=dt.timezone(dt.timedelta(hours=-3))
    for line in open(os.path.join(RX,'all.tsv'),encoding='utf-8'):
        p=line.rstrip('\n').split('\t')
        if len(p)<5: continue
        n_slack+=1
        ts=dt.datetime.fromtimestamp(float(p[0]),TZ).date(); tit=p[4]
        tipo=("varejo" if re.search(r'ao varejo|varejista|ao vendedor|lojista|central do varejo',tit,re.I)
              else "cliente" if re.search(r'ao cliente|cliente em|cliente na|suporte ao cliente',tit,re.I)
              else "indefinido")
        for f in fones(tit):
            k=ID[H('TEL-',f)]; k['kind']='telefone'; k['slack']+=1
            k['tipos'].add(tipo); k['motivos'][motivo(tit)]+=1; k['datas'].append(ts)
            k['varejos']|=varejo_txt(tit)
        for c,_ in cpfs(tit):
            k=ID[H('CPF-',c)]; k['kind']='cpf'; k['slack']+=1
            k['tipos'].add(tipo); k['motivos'][motivo(tit)]+=1; k['datas'].append(ts)
            k['varejos']|=varejo_txt(tit)

# ---------- WHATSAPP ----------
# motivo vem da DEMANDA em que o identificador aparece (detector ja calibrado);
# identificador citado fora de demanda e marcado como tal.
msgs=json.load(open(os.path.join(WA,'msgs2.json')))
dem=json.load(open(os.path.join(WA,'demandas2.json')))
TRAD={'pagamento/boleto':'boleto / 2a via','erro/instabilidade':'erro / instabilidade',
 'credito/limite/regra':'credito / limite','telefone/vinculo':'telefone / vinculo',
 'acesso/senha/operador':'acesso / senha','catalogo/aparelho':'catalogo / aparelho',
 'relatorio/material':'relatorio / material','codigo/finalizar venda':'codigo / comprovante de compra',
 'cancelamento/estorno':'cancelamento / estorno','status de caso aberto':'status de caso aberto',
 'pdv/integracao':'pdv / integracao','cadastro/biometria':'cadastro / dados',
 'comercial/expansao':'comercial / duvida de operacao','gestao do grupo':'gestao do grupo',
 'pedido sem contexto':'pedido sem contexto','nao classificado':'demanda sem motivo explicito'}
# indice: (grupo, dia) -> lista de (texto da demanda, motivo)
from collections import defaultdict as dd
IDX=dd(list)
for x in dem:
    IDX[(x['grupo'],x['dt'][:10])].append((x['txt'],TRAD.get(x['motivo'],x['motivo'])))
def motivo_wa(m,txt):
    for dtxt,mo in IDX.get((m['grupo'],m['ts'][:10]),()):
        if txt[:60] and txt[:60] in dtxt: return mo
    return None
n_fora=0
for m in msgs:
    g=GRP.get(m['grupo'].replace('WhatsApp_Chat__',''),'?')
    d=dt.datetime.fromisoformat(m['ts']).date(); t=m['txt']
    ids=[(H('TEL-',f),'telefone') for f in fones(t)]+[(H('CPF-',c),'cpf') for c,_ in cpfs(t)]
    if ids:
        mo=motivo_wa(m,t)
        if mo is None: mo='citado fora de demanda'; n_fora+=1
        for key,kind in ids:
            k=ID[key]; k['kind']=kind; k['wa']+=1; k['varejos'].add(g)
            k['motivos'][mo]+=1; k['tipos'].add('cliente (citado no grupo)'); k['datas'].append(d)
            if kind=='telefone':
                f=[x for x in fones(t)]
                if any(y[:2]=='11' and len(y)==10 and y[2] in '234' for y in f): k['fixo']=True
    if m['autor'].startswith('PART-'):
        k=ID['TEL-'+m['autor'][5:]]; k['kind']='telefone'; k['wa']+=1
        k['varejos'].add(g); k['tipos'].add('varejo (participante do grupo)'); k['datas'].append(d)
        mo=motivo_wa(m,t)
        if mo and mo!='demanda sem motivo explicito': k['motivos'][mo]+=1

# ---------- institucional ----------
for v in ID.values():
    if v['kind']=='telefone' and (len(v['varejos'])>=3 or v['fixo']):
        v['tipos']={'institucional / canal divulgado'}

# ---------- saida ----------
rows=[]
for cid,v in ID.items():
    ds=sorted(v['datas'])
    rows.append(dict(identificador_id=cid,tipo_dado=v['kind'],
        quem=' / '.join(sorted(v['tipos'])) or 'indefinido',
        varejo=' / '.join(sorted(v['varejos'])) or '(nao identificado)',
        canais=('ambos' if v['slack'] and v['wa'] else 'slack' if v['slack'] else 'whatsapp'),
        n_slack=v['slack'],n_whatsapp=v['wa'],total=v['slack']+v['wa'],
        primeiro=ds[0].isoformat() if ds else '',ultimo=ds[-1].isoformat() if ds else '',
        motivo_principal=(v['motivos'].most_common(1)[0][0] if v['motivos'] else ''),
        motivos=' | '.join(k for k,_ in v['motivos'].most_common())))
rows.sort(key=lambda r:(r['tipo_dado'],-r['total'],r['identificador_id']))
with open(os.path.join(WA,'identidades.csv'),'w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

tel=[r for r in rows if r['tipo_dado']=='telefone']; cpf=[r for r in rows if r['tipo_dado']=='cpf']
print(f"mensagens WhatsApp: {len(msgs)}   linhas Slack: {n_slack}")
print(f"IDENTIFICADORES DISTINTOS: {len(rows)}  (telefone {len(tel)} | cpf {len(cpf)})\n")
print("== por canal =="); [print(f"  {k:<10}{v:>5}") for k,v in Counter(r['canais'] for r in rows).most_common()]
print("\n== quem =="); [print(f"  {k[:46]:<48}{v:>5}") for k,v in Counter(r['quem'] for r in rows).most_common()]
print("\n== por varejo ==")
cv=Counter(); cvc=Counter()
for r in rows:
    for g in r['varejo'].split(' / '):
        cv[g]+=1
        if r['tipo_dado']=='cpf': cvc[g]+=1
for k,v in cv.most_common(): print(f"  {k:<22}{v:>5}   (cpf {cvc[k]})")
print("\n== motivo principal ==")
for k,v in Counter(r['motivo_principal'] for r in rows).most_common(): print(f"  {k:<34}{v:>5}")
print(f"\naparecem nos dois canais: {sum(1 for r in rows if r['canais']=='ambos')}")
print(f"acionados 2+ vezes      : {sum(1 for r in rows if r['total']>1)}")
