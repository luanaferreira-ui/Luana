#!/usr/bin/env python3
"""Separa a fala da Ume nos grupos: atendimento x engajamento x comunicado x social."""
import json,re,os,datetime as dt
from collections import Counter,defaultdict
BASE=os.path.dirname(os.path.abspath(__file__))

ACK=re.compile(r'^\W*(obg|obrigad[oa]|show|oi|ol[aá]|opa|ok|blz|isso|certo|perfeito|exato|top|legal|boa|sim|n[aã]o|hahah?a*|kkk+|ss+im+|👍|👏|🚀|❤️|🙏|😂|✅)[\s\W]{0,6}$',re.I)
SAUDA=re.compile(r'^\W*(bom dia|boa tarde|boa noite)[\s\W\wà-ú]{0,25}$',re.I)

ATENDE=re.compile(
 # instrucao operacional (imperativo ou "pode + verbo")
 r'\b(atualiz|refa[cçz]|fech[ae]|clic|tent[ae]|repet|reenvi|preench|digit|confer|acess[ae]|baix[ae]|abr[ae]|reinici|limp[ae])\w*\b'
 r'|\bpode(m)? (solicitar|pedir|acessar|clicar|tentar|refazer|repetir|baixar|abrir|usar|fazer|entrar|verificar|enviar|chamar)\b'
 # acionamento de canal / encaminhamento
 r'|bal[aã]o verde|\bcentral\b|live ?chat|encaminh|vou (verificar|abrir|pedir|entender|checar)|pedi (a )?prioridade'
 r'|abri (a |o )?(solicita|chamado)|eles v[aã]o verificar|time (vai|est[aá]) (verific|analis|olh)'
 # pedido de evidencia / dado
 r'|me (manda|envia|encaminha|passa)\b|qual o (telefone|cpf|contato|n[uú]mero)|confirma (o|a|se)\b|manda(r)? (o |um )?print'
 # desfecho
 r'|resolvid|foi (enviado|gerado|liberado|aprovado|cancelado)|j[aá] (foi|est[aá]) (resolvid|liberad|enviad|gerad)'
 r'|sem retorno do cliente|cliente n[aã]o (retornou|atendeu)|em contato com o cliente|aguardando (retorno|resposta)'
 # explicacao de regra em resposta
 r'|se (o |a )?cliente|somente o gerente|o pedido para|est[aá] dispon[ií]vel na|segue (o )?link|isso (quer dizer|significa)',re.I)

ENGAJA=re.compile(
 r'parab[eé]ns|bora pra cima|vamos (avante|com tudo|juntos)|excelente (dia|semana)|bom dia (time|pessoal|turma|solar)'
 r'|\bmeta\b|ranking|top \d|acumulado do m[eê]s|campanha|premia|destaque|recorde|com venda\b|vendas do dia'
 r'|100% de oferta|esfor[cç]o da venda|abençoad|clientes aprovados|será que sai|🚀|🎯|🏆|✈️',re.I)
COMUNICA=re.compile(
 r'treinamento|comunicado|informamos|a partir de (hoje|amanh[aã]|segunda)|nova (funcionalidade|regra|vers[aã]o)'
 r'|passo a passo|tutorial|checklist|material|manual|reuni[aã]o|agenda|inscri[cç]|apresenta[cç][aã]o',re.I)

def papel(m):
    t=m['txt'].strip()
    if ACK.match(t) or SAUDA.match(t): return 'social/ack'
    if m['media'] and len(t)<25:       return 'anexo sem texto'
    if ATENDE.search(t):               return 'atendimento'
    if COMUNICA.search(t):             return 'comunicado/treinamento'
    if ENGAJA.search(t):               return 'engajamento'
    return 'outro'

if __name__=='__main__':
    msgs=[m for m in json.load(open(f"{BASE}/msgs2.json"))]
    for m in msgs: m['dt']=dt.datetime.fromisoformat(m['ts'])
    J=(dt.datetime(2026,6,3),dt.datetime(2026,9,3,23,59))
    ume=[m for m in msgs if m['lado']=='ume' and J[0]<=m['dt']<=J[1]]
    for m in ume: m['papel']=papel(m)
    print(f"=== O QUE A UME FALA NOS GRUPOS (n={len(ume)}) ===")
    for k,v in Counter(m['papel'] for m in ume).most_common():
        print(f"  {k:<24} {v:>5}  {100*v/len(ume):>5.1f}%")
    at=sum(m['papel']=='atendimento' for m in ume); en=sum(m['papel']=='engajamento' for m in ume)
    print(f"\n  atendimento {100*at/len(ume):.0f}%  |  engajamento {100*en/len(ume):.0f}%")
    print("\n=== COMPOSICAO DO CANAL POR GRUPO ===")
    print(f"{'grupo':<28}{'msgs':>6}{'varejo':>8}{'atend':>7}{'engaja':>8}{'resto':>7}")
    print("-"*64)
    pg=defaultdict(list)
    for m in msgs:
        if J[0]<=m['dt']<=J[1]: pg[m['grupo']].append(m)
    for g in sorted(pg,key=lambda x:-len(pg[x])):
        s=pg[g]; u=[m for m in s if m['lado']=='ume']
        for m in u: m.setdefault('papel',papel(m))
        a=sum(m['papel']=='atendimento' for m in u); e=sum(m['papel']=='engajamento' for m in u)
        print(f"{g.replace('WhatsApp_Chat__','')[:27]:<28}{len(s):>6}{100*(len(s)-len(u))/len(s):>7.0f}%{100*a/len(s):>6.0f}%{100*e/len(s):>7.0f}%{100*(len(u)-a-e)/len(s):>6.0f}%")
