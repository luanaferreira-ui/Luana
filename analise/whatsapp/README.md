# Voice of Retailer — parte 2: grupos de WhatsApp

Pipeline **incremental**. Para adicionar grupos novos:

1. extraia cada `.zip` em `wa/raw/<nome-do-grupo>/`
2. rode `python3 parse.py` (varre tudo que estiver em `raw/`, reescreve `msgs.json`)
3. rode `python3 lados.py` (classifica Ume x varejo, gera `msgs2.json`)

## Dados

Os exports **não são versionados**. Contêm nome de cliente, telefone, valores e
conversa comercial. Ficam só no diretório de trabalho da sessão.

Telefones são convertidos por hash (`CLI-xxxxxx`) com o **mesmo salt** usado na
parte 1 (Slack), o que permite cruzar o mesmo contato entre os dois canais sem
expor o número.

## Base atual (13 grupos, 14.406 mensagens de conversa)

| grupo | msgs | janela | Ume% |
|---|---:|---|---:|
| UME \| CVLB | 4.033 | 28/04–03/09 | 31% |
| Mega Vintão \| Gerentes Ume | 2.991 | 18/03–04/09 | 47% |
| Big Lar – Crédito Digital Ume | 2.502 | 17/07–03/09 | 36% |
| POLICRED | 1.011 | 27/05–03/09 | 54% |
| UME \\ SIPOLATTI FILIAIS | 904 | 16/06–03/09 | 64% |
| Baianão <> Ume | 554 | 16/05–04/09 | 44% |
| Mini Preço <> Ume | 539 | 06/02–02/09 | 27% |
| UME \| MAG DUARTE | 535 | 20/05–03/09 | 61% |
| UME \| TOP MÓVEIS | 462 | 03/08–03/09 | 45% |
| Ume e Solar Moveis e Eletros | 444 | 13/05–03/09 | 64% |
| Ume – 10&Cia | 185 | 21/07–03/09 | 55% |
| Novo Lar <> Ume | 178 | 16/05–03/09 | 78% |
| Novo Mundo <> Ume – Integração | 68 | 14/08–31/08 | 19% |

Na janela 03/06–03/09 (mesma do Slack): 11.191 mensagens, **680 demandas**
(contra 303 no Slack).

## Três formatos de export

O parser cobre os três que apareceram. Sempre conferir qual chegou:

| formato | cabeçalho | arquivo |
|---|---|---|
| A · pt-BR | `[DD/MM/AAAA, HH:MM:SS] Autor:` | `_chat.txt` |
| B · en-US | `[M/D/AA, H:MM:SS AM] Autor:` | `chat.txt` |
| C · en-US com hífen | `[M/D/AA, H:MM:SS PM] - Autor:` | `chat.txt` |

No formato B/C o autor pode vir como `Você` (é quem exportou — conta Ume) ou
como telefone cru, que é pseudonimizado para `PART-xxxxx`.

## Classificação de lado — não confiar no nome

O prefixo `~` é pushname de contato não salvo e colide entre pessoas diferentes.
A classificação é resolvida por **comportamento**, não por nome:

- quem delega a alguém identificado como Ume, ou distribui material da Ume, é Ume
- quem pergunta sobre a própria meta, as próprias vendas ou a própria filial é varejo

Ambíguos ainda não resolvidos: `Herbert` (152 msgs, agenda treinamentos em dois
grupos) e `~ Bárbara Camilla` (51, fala em visita a filial). Precisam de confirmação
humana.

## Pipeline

    python3 parse.py       # varre raw/, gera msgs.json   (SEM pipe: head mata por SIGPIPE)
    python3 lados.py       # Ume x varejo   -> msgs2.json
    python3 demanda.py     # demandas do varejo -> demandas2.json
    python3 papel_ume.py   # papel da fala da Ume

## Resultado atual (janela 03/06–03/09, mesma do Slack)

- 9.115 mensagens nos 10 grupos
- **606 demandas de suporte** do varejo (contra 303 no Slack no mesmo período)
- primeira resposta da Ume no grupo: mediana 4 min, 55% em ≤5 min, 69% em ≤15 min
- 3% das demandas ficam sem qualquer resposta da Ume

### O grupo não é só suporte

A Ume usa o canal para engajar o varejo, então a fatia dela mistura papéis:

| papel da fala da Ume | % |
|---|---:|
| atendimento | 17% |
| engajamento (meta, ranking, parabéns) | 17% |
| social / ack curto | 7% |
| anexo sem texto | 12% |
| comunicado / treinamento | 1% |
| não classificável por regra | 45% |

**Ler "40% das mensagens são da Ume" como esforço de suporte é errado** — só cerca
de um sexto disso é atendimento.

## Limites conhecidos

- 45% da fala da Ume e 41% das demandas não se classificam por regra. É conversa
  encadeada, sem tema explícito na própria mensagem. Resolver exige leitura.
- "pedido sem contexto" (16% das demandas) é categoria real, não falha: o varejo
  abre com "alguém pode ajudar?" e o problema vem em imagem ou mensagem seguinte.
- `cita canal oficial` (0,5%) e `cliente em loja` (3,8%) são **piso**: só contam
  quando o varejo escreve. Nos prints o número é muito maior.
- Tempo do WhatsApp é **primeira resposta**; o do Slack (parte 1) é **duração da
  thread**. Não são comparáveis diretamente.
