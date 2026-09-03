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
