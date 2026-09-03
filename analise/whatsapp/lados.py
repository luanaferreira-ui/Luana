import json,re,os
from collections import Counter
BASE=os.path.dirname(os.path.abspath(__file__))
msgs=[m for m in json.load(open(f"{BASE}/msgs.json")) if not m['sys']]
# roster confirmado do Slack (parte 1)
CS=["thiago corr","fernanda pimentel","pamela","pâmela","lidiany","ariel souza","marina lima",
    "ingrid magalhaes","ingrid magalhães","jaqueline oliveira","livino menezes","elanny",
    "barbara nascimento","bárbara nascimento","amanda lopes","maraiza","luana jeniffer",
    "adelane","suzy","talita souza","maisa","maísa","stefanne","andressa","vanessa mendes",
    # confirmados por comportamento na leitura dos grupos (delegam a Ume, distribuem material Ume):
    "luiza falcone","pedro gedeon","ju ume","priscila ume","gustavo almeida",
    # confirmados pela Luana em 03/09:
    "herbert","bárbara camilla","barbara camilla",
    "gabriel massuda","luana roncato","raphaella","luciedja","caroline galv"]
def lado(a):
    l=a.lower().lstrip('~ ').strip()
    if l=='luana': return 'ume'   # distribui treinamento/checklist Ume em 6 grupos
    if re.search(r'\bume\b|\(corp\)',l): return 'ume'
    for c in CS:
        if c in l: return 'ume'
    return 'varejo'
for m in msgs: m['lado']=lado(m['autor'])
print("=== CLASSIFICACAO DE LADO ===")
c=Counter(m['lado'] for m in msgs)
for k,v in c.items(): print(f"  {k:<8} {v:>5}  {100*v/len(msgs):>5.1f}%")
print("\n=== AUTORES CLASSIFICADOS COMO UME ===")
for a,n in Counter(m['autor'] for m in msgs if m['lado']=='ume').most_common():
    print(f"  {n:>5}  {a}")
print("\n=== TOP AUTORES 'VAREJO' (conferir se algum e Ume) ===")
for a,n in Counter(m['autor'] for m in msgs if m['lado']=='varejo').most_common(14):
    print(f"  {n:>5}  {a}")
json.dump(msgs,open(f"{BASE}/msgs2.json",'w'),ensure_ascii=False)
