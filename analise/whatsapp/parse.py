#!/usr/bin/env python3
"""Parser incremental de exports do WhatsApp. Roda sobre wa/raw/*/_chat.txt."""
import re,os,sys,json,hashlib,datetime as dt

SALT="ume-voice-of-retailer-2026"                 # mesmo salt do Slack -> ids cruzam
def pid(d): return "CLI-"+hashlib.sha256((SALT+d).encode()).hexdigest()[:6]
def aid(n): return "P-"+hashlib.sha256((SALT+"autor"+n).encode()).hexdigest()[:5]

# formato A (export pt-BR):  [DD/MM/AAAA, HH:MM:SS] Autor: texto
LINE_A=re.compile(r'^\[(\d{2})/(\d{2})/(\d{4}), (\d{2}):(\d{2}):(\d{2})\]\s(.*?):\s(.*)$', re.S)
# formato B (export en-US):   [M/D/AA, H:MM:SS AM] Autor: texto
LINE_B=re.compile(r'^\[(\d{1,2})/(\d{1,2})/(\d{2}), (\d{1,2}):(\d{2}):(\d{2})\s?([AP]M)\]\s(.*?):\s(.*)$', re.S|re.I)

def head(line):
    """Devolve (datetime, autor, texto) ou None. Cobre os dois formatos de export."""
    m=LINE_A.match(line)
    if m:
        D,M,Y,h,mi,s_,a,t=m.groups()
        return dt.datetime(int(Y),int(M),int(D),int(h),int(mi),int(s_)),a.strip(),t
    m=LINE_B.match(line)
    if m:
        M,D,Y,h,mi,s_,ap,a,t=m.groups()
        h=int(h)%12+(12 if ap.upper()=='PM' else 0)
        return dt.datetime(2000+int(Y),int(M),int(D),h,int(mi),int(s_)),a.strip(),t
    return None
LINE=LINE_A
SYS=re.compile(r'criou este grupo|adicionou|mudou a descri|mudou o assunto|mudou a imagem|saiu do grupo|^~?\s*[^:]{1,40}\ssaiu$|entrou usando|foi adicionad|removeu|As mensagens e liga|c[oó]digo de seguran|Mensagem apagada|apagou esta mensagem|mudou o n[uú]mero|agora [eé] admin|convite do grupo|Voc[eê] foi adicionad|criptografia de ponta',re.I)
MEDIA=re.compile(r'<anexado:|imagem ocultada|v[ií]deo ocultado|[aá]udio ocultado|figurinha omitida|documento omitido|GIF omitido|sticker omitid',re.I)

def phones(t):
    out=[]
    for m in re.finditer(r'(?:\+?55)?[\s\-\(]*\d{2}[\s\-\)]*\d{4,5}[\s\-\.]?\d{4}',t):
        d=re.sub(r'\D','',m.group(0))
        if d.startswith('55') and len(d)>11: d=d[2:]
        if 10<=len(d)<=11: out.append(d)
    return sorted(set(out))

def parse(path,grupo):
    raw=open(path,encoding='utf-8',errors='replace').read().replace('\r\n','\n').replace('‎','').replace(' ',' ')
    msgs=[];cur=None
    for line in raw.split('\n'):
        h_=head(line)
        if h_:
            if cur: msgs.append(cur)
            ts,autor,txt=h_
            cur=dict(grupo=grupo,ts=ts,autor=autor,txt=txt)
        elif cur is not None:
            cur['txt']+='\n'+line
    if cur: msgs.append(cur)
    for x in msgs:
        if x['autor'].lower() in ('você','voce','you'): x['autor']='Voce (exportador Ume)'
        if re.fullmatch(r'\+?[\d\s\-()]{10,}', x['autor']):
            x['autor']='PART-'+hashlib.sha256((SALT+re.sub(r'\D','',x['autor'])).encode()).hexdigest()[:5]
        x['sys']=bool(SYS.search(x['txt'])) or x['autor']==grupo_subject.get(grupo,'')
        x['media']=bool(MEDIA.search(x['txt']))
        x['len']=len(x['txt'])
    return msgs

grupo_subject={}
BASE=os.path.dirname(os.path.abspath(__file__))
allm=[]
for d in sorted(os.listdir(os.path.join(BASE,'raw'))):
    p=None
    for nome in ('_chat.txt','chat.txt'):
        q=os.path.join(BASE,'raw',d,nome)
        if os.path.exists(q): p=q; break
    if not p: continue
    grupo_subject[d]=''
    for l in open(p,encoding='utf-8',errors='replace'):
        h_=head(l.replace('‎',''))
        if h_: grupo_subject[d]=h_[1]; break
    allm+=parse(p,d)

allm.sort(key=lambda x:x['ts'])
print(f"mensagens totais: {len(allm)}")
print(f"  de sistema     : {sum(m['sys'] for m in allm)}")
print(f"  de conversa    : {sum(not m['sys'] for m in allm)}")
print(f"  com midia      : {sum(m['media'] and not m['sys'] for m in allm)}")
print()
from collections import Counter
for g in sorted(set(m['grupo'] for m in allm)):
    sub=[m for m in allm if m['grupo']==g and not m['sys']]
    if not sub: continue
    d0,d1=sub[0]['ts'].date(),sub[-1]['ts'].date()
    dias=(d1-d0).days+1
    print(f"{g}")
    print(f"   assunto: {grupo_subject[g]}")
    print(f"   {len(sub):>5} msgs | {d0} a {d1} ({dias} dias) | {len(set(m['autor'] for m in sub))} participantes ativos")

print("\n=== AUTORES (todos os grupos, conversa) ===")
for a,n in Counter(m['autor'] for m in allm if not m['sys']).most_common(40):
    print(f"  {n:>5}  {a}")
json.dump([{**m,'ts':m['ts'].isoformat()} for m in allm],
          open(os.path.join(BASE,'msgs.json'),'w'),ensure_ascii=False)
