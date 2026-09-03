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

## Base atual (10 grupos)

| grupo | msgs | janela | Ume% |
|---|---|---|---|
| UME \| CVLB | 4.134 | 28/04–03/09 | 30% |
| Big Lar – Crédito Digital Ume | 2.502 | 17/07–03/09 | 36% |
| POLICRED | 1.018 | 27/05–03/09 | 53% |
| UME \\ SIPOLATTI FILIAIS | 904 | 16/06–03/09 | 64% |
| Mini Preço <> Ume | 539 | 06/02–02/09 | 27% |
| UME \| MAG DUARTE | 535 | 20/05–03/09 | 54% |
| UME \| TOP MÓVEIS | 464 | 03/08–03/09 | 20% |
| Ume e Solar Moveis e Eletros | 444 | 13/05–03/09 | 64% |
| Ume – 10&Cia | 185 | 21/07–03/09 | 27% |
| Novo Mundo <> Ume – Integração | 68 | 14/08–31/08 | 19% |

Total 10.793 mensagens de conversa. Na janela 03/06–03/09 (mesma do Slack): 9.115.

## Classificação de lado — não confiar no nome

O prefixo `~` é pushname de contato não salvo e colide entre pessoas diferentes.
A classificação é resolvida por **comportamento**, não por nome:

- quem delega a alguém identificado como Ume, ou distribui material da Ume, é Ume
- quem pergunta sobre a própria meta, as próprias vendas ou a própria filial é varejo

Ambíguos ainda não resolvidos: `Herbert` (152 msgs, agenda treinamentos em dois
grupos) e `~ Bárbara Camilla` (51, fala em visita a filial). Precisam de confirmação
humana.

## Estado

- Parser e classificação de lado: prontos e conferidos.
- Classificação de demanda e motivo: **ainda não confiável**. Os grupos são de
  propósito misto (relacionamento, treinamento, onboarding, cobrança de meta),
  e o detector atual confunde saudação e agradecimento com pedido de suporte.
  Precisa de calibração manual sobre uma amostra antes de gerar número.
