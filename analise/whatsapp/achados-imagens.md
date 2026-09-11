# Leitura dos prints — achados (parcial: 9 de 73 lidas)

Regra de PII: nenhum nome, CPF ou telefone reproduzido. Casos identificados por hash.

## A1. A central declara SLA de 12 horas úteis
Print 03/07 17:24 (Sipolatti) — conversa com **Ume – Atendimento ao Varejo** (canal verificado):
> "Prazo de conclusão: A solicitação será encaminhada para análise e poderá ser
> concluída em até 12 horas úteis, após o envio completo das informações."
Conversa original de 11/jun; print postado no grupo em 03/jul, com o varejista
mandando "oi" às 17:24 sem resposta. **22 dias depois, ainda tentando.**

## A2. Regra de acesso que causa o ping-pong de senha
Mesmo print:
> "Por medida de segurança, somente o gerente pode solicitar acesso para a loja.
> Peça para ele entrar em contato através do número cadastrado e clicar na opção
> 'Cadastrar Operador'"
Casa com a pergunta sem resposta no Slack (16/06) sobre reset de senha circular
entre central do varejo e central do cliente.

## A3. O bot atende fora do horário e NÃO resolve — e oferece renegociação
Print 02/09 09:24 (Sipolatti) — **Ume – Apoio Financeiro** (canal verificado), 08:40:
> "Como nossa equipe humana está fora do horário de atendimento, não consigo
> verificar o que aconteceu com o pagamento feito há mais de um mês."
> "Posso te ajudar com outra coisa que esteja ao meu alcance, como gerar um boleto
> para a próxima parcela ou para quitar sua dívida, ou iniciar um processo de
> renegociação?"
RISCO: cliente que pagou e segue cobrado recebe oferta de quitar dívida ou renegociar.
Às 08:40 de um dia útil o canal se declara fora do horário humano.

## A4. Caso completo ponta a ponta, 3 canais, 30 dias (CLI recorrente, Sipolatti)
- 01/08  vencimento da parcela
- 03/08  pagamento em dinheiro no banco (comprovante fotografado)
- 19/08 09:33  varejo posta comprovante no grupo: "mais de 15 dias e nao deram baixa";
        "No atendimento fica só mandando mensagem automática"; "Não consegui resolver por lá"
- 01/09 08:55  MESMO cliente volta à loja. Varejo: "clientes que pagam no sábado estão
        sendo cobrados indevidamente"; "no atendimento de vocês nunca consigo resolver,
        pois fica voltando ao menu"
- 01/09 09:07  cliente conversa com Ume–Atendimento ao Cliente (central responde)
- 01/09 09:09  varejo posta 3 prints no grupo
- 01/09 09:14  "Alguém?????"
- 01/09 09:38  primeira resposta da Ume no grupo (**43 min após a abertura**)
- 01/09 09:56  "Não sei ele foi embora, não podia esperar" -> **cliente perdido**
- 01/09 10:25  escalado ao Slack #ask-retail-priority
- 02/09 08:40  bot diz que equipe humana está fora do horário
- 02/09 15:34  encerrado no Slack: "cliente não atendeu"
**30 dias do pagamento ao encerramento sem resolução. 2 escalações. 1 visita perdida.**

## A5. Falha de produto observada nos prints
- Biometria travada em "Solicite o escaneamento do QR Code / Verificar status da biometria"
- Ativação de licença PAYMOBI presa em "já estamos ativando sua licença..."
- POS em "Configuração ainda não confirmada. Aguarde alguns instantes e tente novamente"
  (varejo esperando >10 min; orientação da Ume foi acionar o livechat e reclamar da demora)

## A6. Frase recorrente do varejo sobre o canal oficial
- "no atendimento de vocês nunca consigo resolver, pois fica voltando ao menu"
- "No atendimento fica só mandando mensagem automática"
- "só conseguimos falar com vocês quando pede prioridade"
- "não é o primeiro cliente que paga no sábado e não dá baixa"
- "Já tem mais de meia hora que estou esperando o atendimento" (03/09)

## Pendente de leitura
64 fotos, agrupadas em ~20 casos distintos. Clusters maiores ainda não lidos:
01/09 17:30 (10 fotos, "clientes não conseguem resolver pendências"),
02/09 09:24 (11 fotos, mesmo caso do A3), 24/08 10&Cia (5, condição de venda),
29/08 Top Móveis (6, conferir venda), 04/08 Top Móveis (4, acessos nova financeira).

---

# Colheita de identificadores — 2ª rodada (14 prints lidos)

## A7. O bot responde "você não tem nenhuma compra em aberto" — e a cobrança continua

Padrão confirmado em **dois clientes distintos**, ambos no canal
**Ume – Atendimento ao Cliente** (verificado), roteiro idêntico:

1. bot: "Entendi que você já pagou, mas ainda está recebendo cobranças.
   Foi por PIX ou código de barras?"
2. bot: "se foi por código de barras, pode levar até **3 dias úteis** para compensar"
3. cliente: "código de barras"
4. bot: "**[nome], vi aqui que você não tem nenhuma compra em aberto com a Ume 😀**"

- Cliente A (CPF-9f7b325b64), 19/08 09:43 — pagamento de 03/08, 16 dias antes
- Cliente B (sem CPF visível), 01/09 16:56 — mesma sequência, mesmo dia em que
  o cliente A voltou à loja

A conversa termina ali. A cobrança automática segue disparando. São dois sistemas
da Ume dando respostas opostas sobre o mesmo contrato, no mesmo dia.

## A8. Segundo prazo oficial declarado

Além das **12 horas úteis** para solicitação do varejo (A1), o canal do cliente
declara **3 dias úteis** para compensação de pagamento por código de barras.
Nos dois casos observados o pagamento tinha 16 e 29 dias — muito fora do prazo
declarado, e ainda assim sem baixa.

## A9. A mensagem de cobrança automática tem defeito de template

Print de 15/07: "Confirmação de pagamento Crédito Sipolatti pendente
**OiMaria**, ainda não recebemos a confirmação do seu pagamento."
Saudação e nome colados. Cliente já havia pago em 06/07; a cobrança de 15/07
pedia R$ 297,95 contra os R$ 286,36 pagos — diferença de juros sobre parcela quitada.

## A10. O funil de vendas por filial circula nos grupos

Print de 06/08 (Sipolatti): tabela "Funil de vendas por ponto de venda" com
25 filiais, colunas clientes consultados / aprovados / vendas / valor financiado.
**É o denominador de normalização que falta ao projeto** — e ele já existe,
é gerado internamente e postado no grupo.

## Rendimento da colheita de CPF

14 prints lidos, **2 CPFs** colhidos, ambos de comprovante bancário.
Conversa com a central mostra só o primeiro nome; tela de erro não mostra nada.
Confirma o diagnóstico: o print serve para provar o caso, não para indexar o cliente.

---

# 3ª rodada — o canal Apoio Financeiro, acompanhado por 3 dias

Uma mesma cliente do Sipolatti, parcela de julho paga, acompanhada nos prints:

| quando | o que o canal oficial respondeu |
|---|---|
| 02/09 08:40 | "nossa **equipe humana está fora do horário de atendimento**, não consigo verificar o pagamento feito há mais de um mês" — oferece gerar boleto ou **renegociar** |
| 02/09 09:24 | "**não estou conseguindo fazer a transferência para o atendimento humano** [...] eles estarão disponíveis **amanhã, 03/09, a partir das 8h**" — oferece boleto ou **renegociação** |
| 03/09 09:41 | oferece "o boleto da parcela de setembro **com os encargos atuais**" |
| 03/09 09:42 | cliente: *"Como eu já paguei quero sem juros"* → bot: *"Vou te transferir para um atendente humano. Aguarde um momento."* |
| 03/09 09:51 | cliente: "Oi" |
| 03/09 10:02 | cliente: "Oiiiii" |
| 03/09 10:23 | **41 min sem nenhuma resposta.** Varejo recorre ao grupo: *"Já tem mais de meia hora que estou esperando o atendimento"* |

## A11. A transferência para humano falha e não avisa

Em 02/09 o bot declarou indisponibilidade de handoff **pelo dia inteiro** de um dia
útil. Em 03/09 prometeu transferir e simplesmente não transferiu — a cliente ficou
41 minutos mandando "Oi" para o vazio.

## A12. A oferta de renegociação e de juros aparece em todos os casos

Nos quatro prints do canal financeiro, a saída oferecida a quem já pagou é sempre
a mesma: **gerar novo boleto (com encargos) ou iniciar renegociação**. Nenhuma
oferece "vou verificar seu comprovante". É o roteiro, não o acaso.

## A13. Três pagamentos comprovados, nenhum baixado

| pago em | valor | dias sem baixa até a cobrança |
|---|---:|---:|
| 01/08/2026 | R$ 140,44 | 31 |
| 03/08/2026 | R$ 226,93 | 29 |
| 06/07/2026 | R$ 286,36 | 9 |

Mediana 29 dias. Todos com comprovante bancário fotografado. Todos do Sipolatti.
Os três contra um prazo de compensação **declarado pelo próprio canal de 3 dias úteis**.

## Limitação de método a partir daqui

O ambiente bloqueia gravar CPF em claro, inclusive para gerar hash — o que está
correto. **Não colho mais CPF.** Os prints com CPF ficam marcados
`cpf_visivel_no_print: true` e o hash fica `PENDENTE-extrair-localmente`.
Para fechar o cruzamento, rodar `colher.py` localmente com o mesmo salt.

---

# 4ª rodada — 33 prints lidos

## A14. O canal encerra o atendimento quando não localiza o cadastro
Print 28/08 (Novo Mundo), canal oficial:
- bot pede "CPF do titular da compra, apenas números, Ex: 10987654321"
- cliente digita o CPF **duas vezes**, no formato exato pedido
- bot: *"Desculpe mas não consegui entender o seu CPF para localizar seu cadastro! 😅"*
- bot: *"Como não conseguimos localizar seu cadastro **não podemos seguir com o atendimento**."*

Terminação por falha de identificação. O cliente não é atendido e não recebe
alternativa. É um modo de falha distinto dos anteriores.

## A15. O ping-pong do reset de senha, agora com evidência dos dois lados
Print 22/06 (Mag Duarte): tela de login do portal com
*"Usuário não cadastrado ou senha incorreta"*, vendedor com cliente em loja.
A própria tela orienta: *"Esqueceu seus dados de acesso? Fale conosco pelo
atendimento ao varejo pelo WhatsApp (11) 4020-4025"*.
É exatamente o canal que, segundo a thread do Slack de 16/06, responde que não
faz esse atendimento e manda procurar a central do cliente.
**O produto manda para um lugar que recusa o pedido.**

## A16. Biometria: três falhas distintas no mesmo fluxo
- *"Falha ao consultar biometria"* (06/08)
- travado em *"Solicite o escaneamento do QR Code / Verificar status da biometria"* (06/08)
- *"Solicitação iniciada em outro dispositivo"* ao passar do aparelho da loja
  para o do cliente (20/05)
O fluxo exige emprestar o aparelho da loja ao cliente ou ler QR Code para
continuar no celular dele — e quebra na passagem.

## A17. Entrada mínima sem explicação
Print 08/08 (Top Móveis): compra de **R$ 2.750,00**, entrada mínima oferecida de
**R$ 1.750,00** — 64% do valor. A tela lista as opções e não explica o motivo nem
oferece caminho alternativo. É o subtipo C do cluster de crédito do material
anterior, agora com número.
Nota: **o portal mascara o CPF na própria tela** (`048.***.***-38`). Os
comprovantes bancários fotografados expõem tudo.

## A18. A base da central existe com os campos certos
Print 06/08: console interno do atendimento, mostrando id do ticket,
"Contactado há poucos segundos", "Criada em", nome do agente e
*"Sistema alterou o status para Abrir 13:34"*.
Confirma que o sistema tem **ticket id, timestamps, status e agente** — os campos
pedidos para o cruzamento. O pedido é viável.

## A19. Exposição de dado de colaborador
Print 04/08 (Top Móveis): planilha `operator_name` + `operator email` com cerca de
33 operadores de loja, compartilhada como imagem num grupo de 30 participantes.
Os acessos ao portal estão atrelados a **e-mails pessoais** (gmail, hotmail, yahoo),
não corporativos — sem revogação quando o colaborador sai.
Nenhum dado reproduzido neste registro.
