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

## Estado

- Parser e classificação de lado: prontos e conferidos.
- Classificação de demanda e motivo: **ainda não confiável**. Os grupos são de
  propósito misto (relacionamento, treinamento, onboarding, cobrança de meta),
  e o detector atual confunde saudação e agradecimento com pedido de suporte.
  Precisa de calibração manual sobre uma amostra antes de gerar número.
