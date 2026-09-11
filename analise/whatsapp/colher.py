#!/usr/bin/env python3
"""Registra um identificador colhido de print: guarda so o hash."""
import sys,json,os,re,hashlib
WA=os.path.dirname(os.path.abspath(__file__))
SALT="ume-voice-of-retailer-2026"
REG=os.path.join(WA,"identificadores.json")
def h(kind,v):
    v=re.sub(r'\D','',v)
    return f"{kind}-"+hashlib.sha256((SALT+v).encode()).hexdigest()[:10]
def add(**kw):
    reg=json.load(open(REG)) if os.path.exists(REG) else []
    if kw.get('cpf'): kw['cpf_id']=h('CPF',kw.pop('cpf'))
    if kw.get('tel'): kw['tel_id']=h('',kw.pop('tel'))
    reg=[r for r in reg if r.get('arquivo')!=kw.get('arquivo')]
    reg.append(kw); json.dump(reg,open(REG,'w'),ensure_ascii=False,indent=1)
    return kw
if __name__=='__main__':
    print(json.dumps(add(**json.loads(sys.argv[1])),ensure_ascii=False))
